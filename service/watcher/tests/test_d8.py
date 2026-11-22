"""D8: re-verification of COMPLETE receipts. The real first production receipt (docs/smoke/2026-11-16-first-receipt)
is verified by the frozen verifier's CLI, with explorers faked from the bundle's own headers (no network)."""
import json
import os
from pathlib import Path

import pytest

import fakes
from conftest import SMOKE, T0, Env
from tessera_watch import receipts as R
from tessera_watch import watcher as W

MAIN_INSTALL = Path("/home/tony/projects/tessera/service/verifier/install.json")
INSTALL = Path(os.environ.get("TESSERA_VERIFY_INSTALL_JSON") or (
    Path(__file__).resolve().parents[2] / "verifier" / "install.json"))
if not INSTALL.is_file():
    INSTALL = MAIN_INSTALL                                    # a worktree has no built verifier; use main's build
BUNDLE = (SMOKE / "receipt.json").read_bytes()
HEADERS = {int(h): bytes.fromhex(v) for h, v in json.loads(BUNDLE)["layers"][0]["headers"].items()}


def explorer(headers=HEADERS, broken=None, lie=None):
    def get(url):
        api, _, rest = url.partition("/block")
        if broken and api == broken:
            raise OSError("down")
        if rest.startswith("-height/"):
            h = int(rest.rsplit("/", 1)[-1])
            hdr = (lie if (lie and api == "https://b.example") else headers)[h]
            return R.pin_of(hdr)
        bh = rest.split("/")[1]
        for src in (headers, lie or {}):
            for v in src.values():
                if R.pin_of(v) == bh:
                    return v.hex()
        raise OSError("unknown block")
    return get


RID = "c" * 64
CONTENT = (SMOKE / "content.txt").read_bytes()


def real_verify(get):
    cli = lambda d, timeout: R.run_cli(d, install_json=INSTALL, timeout=timeout)          # noqa: E731
    return lambda bundle, window, catalog, as_of, explorers, **k: R.verify(bundle, window, catalog, as_of, explorers,
                                                                           get=get, cli=cli, **k)


def complete(env, bundle, rid=RID, digest=None, bind_to=None):
    """A COMPLETE record for `bundle`. With bind_to (a receipt), the record holds that receipt's commitments, as the
    issuer's record of the request that produced it does."""
    digest = digest or fakes.sha(bundle)
    env.s3.put("results", f"result/{rid}/{digest}.json", bundle)
    rec = fakes.request(rid, "COMPLETE", T0 - 300, receipt_sha256=digest)
    if bind_to is not None:
        b = R.binding(bind_to)
        rec["content_sha256"], rec["content_len"] = b["content_sha256"], b["content_len"]
        a = rec["attempts"][0]
        a["declared_issue_time"], a["receipt_id"] = b["declared_issue_time"], b["receipt_id"]
        a["jobs"] = {n: fakes.job(n[2:], "req-%040d" % i, h) for i, (n, h) in enumerate(sorted(b["sigs"].items()))}
    env.ddb.put("REQ#" + rid, rec)
    return digest


def test_real_receipt_verifies_valid_strict_no_alarm():
    env = Env(verify=real_verify(explorer()))
    complete(env, BUNDLE, bind_to=BUNDLE)
    jobs = json.loads(env.ddb.items["REQ#" + RID]["doc"]["S"])["attempts"][0]["jobs"]
    for i, n in enumerate(("s_kms", "p_kms")):                # the issuer's "used" entries and their Signs
        env.ddb.put(f"SIGLOG#USED#{n}", fakes.siglog(T0 - 3000 + i, request_id=jobs[n]["request_id"],
                                                     sig=jobs[n]["sig_sha256"]))
    env.trail(T0 - 3000, [fakes.sign_event(T0 - 3050), fakes.sign_event(T0 - 3040)])
    env.run()
    assert env.sns.sent == []
    t = env.traces()[f"trace/{RID}.json"]
    assert t["verification"]["verdict"] == "VALID_STRICT" and t["anchor_heights"] == sorted(HEADERS)
    assert t["verification"]["binding"] == "match"
    assert t["receipt_sha256"] == fakes.sha(BUNDLE) == "aca4dfb2c8abb3b2d970ee9d9ab10a5438704845a19e89e9d64f84e647ed9f83"


def test_tampered_receipt_alarms_d8():
    bad = bytearray(BUNDLE)
    i = BUNDLE.find(b'"a_sig":"') + 200
    bad[i] = ord("A") if bad[i] != ord("A") else ord("B")
    env = Env(verify=real_verify(explorer()))
    complete(env, bytes(bad))
    env.run()
    assert [json.loads(m["Message"])["detection"] for m in env.sns.sent] == ["D8"]
    assert env.codes()[0].startswith("VERDICT_") and env.codes()[0] != "VERDICT_VALID_STRICT"
    assert env.traces()[f"trace/{RID}.json"]["verification"]["verdict"] != "VALID_STRICT"


def test_binding_reads_the_real_receipts_commitments():
    b = R.binding(BUNDLE)
    assert b["content_sha256"] == fakes.sha(CONTENT) and b["content_len"] == len(CONTENT)
    assert b["declared_issue_time"] == "2026-11-16T12:56:33Z" and set(b["sigs"]) == {"s_kms", "s_gpg", "p_kms", "p_gpg"}
    assert R.binding(b"{}") is None and R.binding(b"not json") is None


def test_a_valid_receipt_of_another_request_is_not_traced_as_this_ones():
    """M9: another request's valid receipt copied to this request's path, with its digest recorded: VALID_STRICT from
    the verifier, but its content and signatures are not this record's, so D8 fires and the trace holds no anchors."""
    env = Env(verify=real_verify(explorer()))
    complete(env, BUNDLE)                                     # the record's own content and jobs differ
    env.run()
    assert "RECEIPT_NOT_THIS_REQUEST" in env.codes()
    t = env.traces()[f"trace/{RID}.json"]
    v = t["verification"]
    assert v["verdict"] == "NOT_BOUND" and v["verifier_verdict"] == "VALID_STRICT" and v["binding"] == "mismatch"
    assert "content_sha256" in v["mismatch"] and t["anchor_heights"] is None and t["T"] is None


def test_wrong_header_pins_do_not_verify():
    """An explorer pair that agrees on headers other than the bundle's: the receipt does not verify."""
    lie = {h: v[:4] + bytes(32) + v[36:] for h, v in HEADERS.items()}
    env = Env(verify=real_verify(explorer(headers=lie)))
    complete(env, BUNDLE)
    env.run()
    assert [json.loads(m["Message"])["detection"] for m in env.sns.sent] == ["D8"]


def test_explorers_disagree_is_unavailable_not_a_verdict():
    lie = {h: v[:4] + bytes(32) + v[36:] for h, v in HEADERS.items()}
    with pytest.raises(R.Unavailable) as e:
        R.explorer_headers(sorted(HEADERS), ["https://a.example", "https://b.example"], explorer(lie=lie))
    assert e.value.code == "EXPLORERS_DISAGREE"


def test_stored_bytes_must_hash_to_receipt_sha256(env):
    complete(env, b'{"layers":[]}', digest="0" * 64)
    env.run()
    assert env.codes() == ["RECEIPT_BYTES_DIGEST_MISMATCH"]


def test_missing_receipt_object(env):
    env.ddb.put("REQ#" + RID, fakes.request(RID, "COMPLETE", T0 - 300, receipt_sha256="1" * 64))
    env.run()
    assert env.codes() == ["RECEIPT_OBJECT_MISSING"]
    assert env.traces()[f"trace/{RID}.json"]["verification"]["verdict"] == "NO_RECEIPT"


def test_unreadable_receipt_object_is_a_d8_finding_and_the_run_goes_on(env):
    """H1: a GetObject that fails (here AccessDenied, as without ListBucket) is reported for that receipt, unrelated
    findings are still published, the state is committed and the heartbeat sent."""
    env.ddb.put("REQ#" + RID, fakes.request(RID, "COMPLETE", T0 - 300, receipt_sha256="1" * 64))
    env.trail(T0 - 300, [fakes.iam_event(T0 - 400)], region="us-east-1")
    real = env.s3.get_object

    def denied(Bucket, Key):
        if Bucket == "results":
            raise fakes.ClientError("AccessDenied")
        return real(Bucket, Key)
    env.s3.get_object = denied
    env.run()
    assert sorted(env.codes()) == ["IAM_WRITE", "RECEIPT_OBJECT_UNREADABLE"] and len(env.cw.beats) == 1
    assert RID in env.state()["pending"]
    env.clock.t = T0 + W.D8_GIVE_UP_S + 1
    env.run()
    assert env.traces()[f"trace/{RID}.json"]["verification"]["reason"] == "OBJECT_UNREADABLE"


def test_complete_without_digest(env):
    env.ddb.put("REQ#" + RID, fakes.request(RID, "COMPLETE", T0 - 300, receipt_sha256=None))
    env.run()
    assert env.codes() == ["COMPLETE_WITHOUT_RECEIPT_DIGEST"]


def test_valid_strict_stub_no_alarm(env):
    complete(env, b"bundle")
    env.run()
    assert env.sns.sent == [] and len(env.traces()) == 1


@pytest.mark.parametrize("verdict", ["INVALID", "UNVERIFIABLE", "VALID"])
def test_any_other_verdict_alarms(verdict):
    env = Env(verify=lambda *a, **k: {"verdict": verdict, "reason": "X", "heights": [], "T": None, "binding": None})
    complete(env, b"bundle")
    env.run()
    assert env.codes() == ["VERDICT_" + verdict]


def test_unavailable_check_is_retried_then_bounded():
    state = {"fail": True}

    env = Env()
    stub = env.verify

    def verify(*a, **k):
        if state["fail"]:
            raise R.Unavailable("EXPLORER_UNAVAILABLE")
        return stub(*a, **k)
    env.verify = verify
    complete(env, b"bundle")
    env.run()
    assert env.codes() == ["RECEIPT_CHECK_UNAVAILABLE"] and env.traces() == {}
    env.clock.t += 600
    env.run()
    assert env.codes() == ["RECEIPT_CHECK_UNAVAILABLE"]          # reported once per reason
    assert RID in env.state()["pending"]
    env.clock.t = T0 + W.D8_GIVE_UP_S + 1
    env.run()
    assert env.codes() == ["RECEIPT_CHECK_UNAVAILABLE", "RECEIPT_UNCHECKED"]
    assert env.traces()[f"trace/{RID}.json"]["verification"]["verdict"] == "UNCHECKED"


def test_unavailable_then_recovers_without_d8(env):
    calls, stub = [], env.verify

    def verify(*a, **k):
        calls.append(1)
        if len(calls) == 1:
            raise R.Unavailable("VERIFIER_REFUSED:INSTALL_RECORD_MISSING")
        return stub(*a, **k)
    env.verify = verify
    complete(env, b"bundle")
    env.run()
    env.clock.t += 600
    env.run()
    assert env.codes() == ["RECEIPT_CHECK_UNAVAILABLE"] and len(env.traces()) == 1


def test_verifier_refusal_code_is_bounded(tmp_path):
    def cli(d, timeout):
        return 2, "", "INSTALL_RECORD_MISSING\n"
    with pytest.raises(R.Unavailable) as e:
        R.verify(BUNDLE, Env().cfg.window, Env().cfg.catalog, "2026-11-22T00:00:00Z",
                 ["https://a.example", "https://b.example"], get=explorer(), cli=cli)
    assert e.value.code == "VERIFIER_REFUSED:INSTALL_RECORD_MISSING"

    def cli2(d, timeout):
        return 2, "", "INPUT_IO_ERROR: [Errno 2] /tmp/secret/path https://x?sig=abc"
    with pytest.raises(R.Unavailable) as e:
        R.verify(BUNDLE, Env().cfg.window, Env().cfg.catalog, "2026-11-22T00:00:00Z",
                 ["https://a.example", "https://b.example"], get=explorer(), cli=cli2)
    assert e.value.code == "VERIFIER_REFUSED:INPUT_IO_ERROR"


def test_verification_budget_leaves_receipts_pending(env):
    complete(env, b"bundle")
    env.make(remaining=lambda: 1000).run()
    assert RID in env.state()["pending"] and env.traces() == {}
    env.run()
    assert env.state()["pending"] == {} and len(env.traces()) == 1


def test_catalog_must_be_the_frozen_one(tmp_path):
    p = tmp_path / "catalog.json"
    p.write_text("{}")
    with pytest.raises(R.Unavailable):
        R.load_catalog(p)


def test_refusal_reason_is_split_into_codes_in_the_finding(env):
    calls, stub = [], env.verify

    def verify(*a, **k):
        raise R.Unavailable("VERIFIER_REFUSED:INSTALL_RECORD_MISSING")
    env.verify = verify
    complete(env, b"bundle")
    env.run()
    m = json.loads(env.sns.sent[0]["Message"])
    assert m["reason"] == "VERIFIER_REFUSED" and m["reason_detail"] == "INSTALL_RECORD_MISSING"


def test_d8_per_run_bound_carries_the_rest_over_least_recently_tried_first(env):
    """M4: at most MAX_VERIFY_PER_RUN checks a run; the rest stay pending and are checked by later runs."""
    n = W.MAX_VERIFY_PER_RUN + 3
    for i in range(n):
        rid = "%064x" % (i + 1)
        complete(env, b"bundle-%d" % i, rid=rid)
    env.run()
    assert len(env.traces()) == W.MAX_VERIFY_PER_RUN and len(env.state()["pending"]) == 3
    env.clock.t += 600
    env.run()
    assert len(env.traces()) == n and env.state()["pending"] == {}


def test_d8_backlog_is_bounded_by_a_finding(env):
    complete(env, b"bundle")
    env.make(remaining=lambda: 1000).run()                    # never time to verify
    env.clock.t = T0 + W.D8_GIVE_UP_S + 1
    env.make(remaining=lambda: 1000).run()
    assert env.codes() == ["RECEIPT_UNCHECKED"]
    assert env.traces()[f"trace/{RID}.json"]["verification"]["reason"] == "D8_BACKLOG"


def test_too_many_heights_is_unchecked_at_once_without_explorer_calls():
    layers = [{"headers": {str(h): "00" * 80 for h in range(R.MAX_HEIGHTS + 1)}}]
    bundle = json.dumps({"layers": layers}).encode()
    calls = []
    env = Env(verify=lambda b, w, c, a, e, **k: R.verify(b, w, c, a, e, get=lambda u: calls.append(u), **k))
    complete(env, bundle)
    env.run()
    assert env.codes() == ["RECEIPT_UNCHECKED"] and calls == []


@pytest.mark.parametrize("headers", [[float("inf")], ["1e400"], {"Infinity": "00"}, [True], ["-1"], {"99999999": ""}])
def test_odd_heights_are_left_to_the_verifier_never_raise(headers):
    bundle = json.dumps({"layers": [{"headers": headers}]}).encode()
    assert R.bundle_heights(bundle) == []


def test_the_check_deadline_bounds_explorer_work():
    clock = [0.0]

    def slow_get(url):
        clock[0] += 30
        return "0" * 64
    d = R.Deadline(50, clock=lambda: clock[0])
    with pytest.raises(R.Unavailable) as e:
        R.explorer_headers([1, 2, 3], ["https://a.example", "https://b.example"], slow_get, d)
    assert e.value.code in ("CHECK_DEADLINE", "EXPLORER_BAD_HEADER")
