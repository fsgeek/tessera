"""The secrecy boundary (review H4): a URL, a plaintext request key, request content, an API key value and exception
text placed in every source field the watcher reads (SIGLOG# entries, REQ# records, CloudTrail records, SDK and
verifier exceptions) reach no output: no finding, log line, SNS subject or message, trace record, outbox entry or the
watcher's state. The handler never lets an exception out."""
import io
import json

import pytest

import fakes
from conftest import T0, Env
from tessera_watch import lambda_app
from tessera_watch import receipts as R
from tessera_watch import sanitize as S
from tessera_watch import watcher as W

URL = "https://evil.example/leak?X-Amz-Signature=deadbeef"
REQUEST_KEY = "ca33cc04-6032-4da0-8a7a-7fffd0373dd3"
CONTENT = "the requester's private content"
API_KEY = "tEsTaPiKeYvAlUe0123456789abcdefghijklmn"
EXC_TEXT = "Traceback: secret path /var/task/x and " + URL
SECRETS = [URL, REQUEST_KEY, REQUEST_KEY.replace("-", ""), CONTENT, API_KEY, EXC_TEXT, "evil.example", "Traceback",
           "X-Amz"]
POISON = [URL, REQUEST_KEY, CONTENT, API_KEY, EXC_TEXT]


def outputs(env):
    """Every byte the watcher emitted or stored, as text."""
    parts = [env.out.getvalue()]
    parts += [m["Subject"] + "\n" + m["Message"] for m in env.sns.sent]
    parts += [o["body"].decode() for (b, k), o in env.s3.objects.items() if b in ("trace", "state")]
    return "\n".join(parts)


def assert_clean(env):
    text = outputs(env)
    for s in SECRETS:
        assert s not in text, s


def new_env(**kw):
    env = Env(**kw)
    env.out = io.StringIO()
    return env


SIGLOG_FIELDS = ["slot", "request_id", "status", "reason", "disposition", "attempt", "frame_sha256",
                 "signature_sha256", "reason_sha256"]


@pytest.mark.parametrize("value", POISON)
@pytest.mark.parametrize("field", SIGLOG_FIELDS)
def test_siglog_fields(field, value):
    env = new_env()
    for i, disp in enumerate(["unrequested", "used", "bad-signature"]):
        e = fakes.siglog(T0 - 60, disposition=disp, request_id="req-" + "5" * 40)
        e[field] = value
        env.ddb.put(f"SIGLOG#{i}", e)
    env.ddb.put("SIGLOG#t", dict(fakes.siglog(T0 - 60), at=value))            # an unreadable time
    env.ddb.put("SIGLOG#" + value, fakes.siglog(T0 - 60, disposition="malformed"))   # poison in the item key
    env.run()
    env.clock.t += 2 * 3600
    env.run()
    assert env.sns.sent                                      # the D5 findings are sent, with the values withheld
    assert_clean(env)


REQ_FIELDS = ["cred", "key", "content_sha256", "content_len", "reason", "created_at", "ended_at", "receipt_sha256",
              "stage", "diag"]
ATTEMPT_FIELDS = ["id", "state", "declared_issue_time", "receipt_id"]
JOB_FIELDS = ["slot", "request_id", "frame_sha256", "sig_sha256", "frame"]


def poisoned_request(rid, field=None, value=None, where="req"):
    jobs = {"s_kms": fakes.job("kms", "req-" + "6" * 40, fakes.sha(b"s")),
            "s_gpg": fakes.job("gpg", "req-" + "7" * 40, fakes.sha(b"g"))}
    rec = fakes.request(rid, "COMPLETE", T0 - 300, jobs=jobs, receipt_sha256=fakes.sha(b"bundle"), key=REQUEST_KEY)
    a = rec["attempts"][0]
    if where == "req":
        rec[field] = value
    elif where == "attempt":
        a[field] = value
    elif where == "end":
        a["end"][field] = value
    elif where == "job":
        a["jobs"]["s_kms"][field] = value
        a["jobs"]["s_gpg"][field] = value
    elif where == "jobname":
        a["jobs"][value] = a["jobs"].pop("s_kms")
    return rec


@pytest.mark.parametrize("value", POISON)
@pytest.mark.parametrize("where,field", [("req", f) for f in REQ_FIELDS] + [("attempt", f) for f in ATTEMPT_FIELDS]
                         + [("end", "reason"), ("end", "outcome")] + [("job", f) for f in JOB_FIELDS]
                         + [("jobname", None)])
def test_request_fields(where, field, value):
    env = new_env()
    rid = "a" * 64
    env.s3.put("results", f"result/{rid}/{fakes.sha(b'bundle')}.json", b"bundle")
    env.ddb.put("REQ#" + rid, poisoned_request(rid, field, value, where))
    env.ddb.put("REQ#" + value, dict(fakes.request("b" * 64, "REFUSED", T0, key=REQUEST_KEY), rid=value))
    env.ddb.put("REQ#" + "c" * 64, dict(fakes.request("c" * 64, "FAILED", T0, key=REQUEST_KEY),
                                        reason="SIGNER_REFUSED:" + value))
    for t in (T0, T0 + 3 * 3600, T0 + 8 * 3600):
        env.clock.t = t
        env.run()
    assert env.traces()                                      # the trace records are written, with values withheld
    assert_clean(env)


CT_FIELDS = ["eventID", "eventTime", "eventName", "awsRegion", "errorCode", "errorMessage", "userAgent",
             "sourceIPAddress", "requestID"]


@pytest.mark.parametrize("value", [URL, CONTENT, EXC_TEXT, REQUEST_KEY.upper()])
@pytest.mark.parametrize("field", CT_FIELDS + ["userIdentity.arn", "sessionIssuer.arn", "requestParameters.keyId",
                                               "requestParameters.userName"])
def test_cloudtrail_fields(field, value):
    env = new_env()
    recs = [fakes.sign_event(T0 - 400, role=fakes.OTHER_ROLE), fakes.sign_event(T0 - 400, error="AccessDenied"),
            fakes.iam_event(T0 - 400), fakes.sign_event(T0 - 400)]
    for r in recs:
        if field == "userIdentity.arn":
            r["userIdentity"]["arn"] = value
            r["userIdentity"]["type"] = value
            r["userIdentity"]["sessionContext"]["sessionIssuer"]["arn"] = value
        elif field == "sessionIssuer.arn":
            r["userIdentity"]["sessionContext"]["sessionIssuer"]["arn"] = value
        elif "." in field:
            r["requestParameters"][field.split(".")[1]] = value
        else:
            r[field] = value
    env.trail(T0 - 300, recs, region="us-east-1")
    env.run()
    env.clock.t += 2 * 3600
    env.run()
    assert_clean(env)


class Leaky(Exception):
    pass


@pytest.mark.parametrize("bucket", ["results", "trail", "trace", "outbox-list", "outbox-put"])
def test_sdk_exception_text_never_reaches_an_output(bucket):
    env = new_env()
    rid = "a" * 64
    env.s3.put("results", f"result/{rid}/{fakes.sha(b'bundle')}.json", b"bundle")
    env.ddb.put("REQ#" + rid, fakes.request(rid, "COMPLETE", T0 - 300, receipt_sha256=fakes.sha(b"bundle")))
    env.trail(T0 - 300, [fakes.iam_event(T0 - 400)], region="us-east-1")
    get, put, lst = env.s3.get_object, env.s3.put_object, env.s3.list_objects_v2
    if bucket in ("results", "trail"):
        env.s3.get_object = lambda Bucket, Key: (_ for _ in ()).throw(Leaky(EXC_TEXT)) if Bucket == bucket \
            else get(Bucket, Key)
    elif bucket == "trace":
        env.s3.fail_put = lambda b, k: Leaky(EXC_TEXT) if b == "trace" else None
    elif bucket == "outbox-list":
        env.s3.list_objects_v2 = lambda **kw: (_ for _ in ()).throw(Leaky(EXC_TEXT)) \
            if kw.get("Prefix") == "findings/" else lst(**kw)
    else:
        env.s3.fail_put = lambda b, k: Leaky(EXC_TEXT) if k.startswith("findings/") else None
    env.run()
    assert_clean(env)
    assert "Leaky" in outputs(env)                           # the class name is what is said


@pytest.mark.parametrize("exc", [Leaky(EXC_TEXT), R.Unavailable(EXC_TEXT), R.Unavailable("VERIFIER_REFUSED:" + URL),
                                 R.Uncheckable(URL)])
def test_verifier_exception_text_never_reaches_an_output(exc):
    def verify(*a, **k):
        raise exc
    env = new_env(verify=verify)
    rid = "a" * 64
    env.s3.put("results", f"result/{rid}/{fakes.sha(b'bundle')}.json", b"bundle")
    env.ddb.put("REQ#" + rid, fakes.request(rid, "COMPLETE", T0 - 300, receipt_sha256=fakes.sha(b"bundle")))
    env.run()
    env.clock.t += W.D8_GIVE_UP_S + 1
    env.run()
    assert env.sns.sent and env.traces()
    assert_clean(env)


def test_scan_and_publish_exception_text_never_reaches_an_output():
    env = new_env()
    env.ddb.scan = lambda **kw: (_ for _ in ()).throw(Leaky(EXC_TEXT))
    env.run()
    env.sns.publish = lambda **kw: (_ for _ in ()).throw(Leaky(EXC_TEXT))
    env.clock.t += 600
    env.run()
    assert_clean(env)


def test_outbox_entries_are_validated_again_on_the_way_out():
    """An outbox object altered by a principal that could write the state bucket carries nothing out."""
    env = new_env()
    env.s3.put("state", "findings/x.json", json.dumps({"detection": URL, "code": CONTENT, "reason": EXC_TEXT,
                                                       "rid": REQUEST_KEY, "extra": API_KEY}).encode())
    env.run()
    assert len(env.sns.sent) == 1
    assert_clean(env)


def test_published_message_is_the_logged_line():
    env = new_env()
    env.trail(T0 - 300, [fakes.iam_event(T0 - 400), fakes.sign_event(T0 - 400, role=fakes.OTHER_ROLE)],
              region="us-east-1")
    env.ddb.put("SIGLOG#1", fakes.siglog(T0 - 60, disposition="unrequested", reason="SIGNER_REFUSED:BAD_REQUEST"))
    env.run()
    logged = sorted(json.dumps(x, sort_keys=True) for x in map(json.loads, env.out.getvalue().splitlines())
                    if x["event"] == "finding")
    sent = sorted(json.dumps(json.loads(m["Message"]), sort_keys=True) for m in env.sns.sent)
    assert logged == sent and len(sent) == 3


def test_handler_never_raises_and_says_only_the_class_name():
    out, sent = io.StringIO(), []

    class Topic:
        def publish(self, subject, message):
            sent.append(subject + message)

    def build(remaining):
        raise Leaky(EXC_TEXT)
    r = lambda_app.handler({}, None, build=build, topic=Topic(), out=out)
    assert r == {"event": "watcher_error", "v": 1, "error_class": "Leaky", "heartbeat": False}
    text = out.getvalue() + "".join(sent)
    assert "WATCHER_ERROR" in text and "Leaky" in text and EXC_TEXT not in text and "evil" not in text


def test_handler_survives_a_failing_topic_and_base_exceptions():
    def build(remaining):
        raise SystemExit(EXC_TEXT)

    class Topic:
        def publish(self, subject, message):
            raise Leaky(EXC_TEXT)
    out = io.StringIO()
    r = lambda_app.handler({}, None, build=build, topic=Topic(), out=out)
    assert r["error_class"] == "SystemExit" and EXC_TEXT not in out.getvalue()


def test_every_finding_field_has_a_rule():
    """A field added to a finding without a rule is withheld; this lists the fields the code emits so a new one is seen."""
    import ast
    import inspect
    names = set()
    for node in ast.walk(ast.parse(inspect.getsource(W))):
        if isinstance(node, ast.Call) and getattr(node.func, "attr", "") in ("find", "find_once", "item_failed"):
            names |= {k.arg for k in node.keywords if k.arg}
    assert names <= set(S.RULES), names - set(S.RULES)
