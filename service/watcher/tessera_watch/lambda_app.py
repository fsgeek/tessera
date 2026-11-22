"""Lambda entry point. Environment (set by service/detect/infra; names and identifiers only, no secret):

ACCOUNT_ID, KMS_KEY_ARN, KMS_ALIASES (comma-separated), SIGNER_ROLE_ARN, REQUEST_TABLE, RESULTS_BUCKET, TRAIL_BUCKET,
TRAIL_PREFIX, STATE_BUCKET, STATE_KEY, TRACE_BUCKET, ALARM_TOPIC_ARN, EXPLORERS (JSON list), CLIENT_KEY_IDS (JSON
{client name: API key id}), TESSERA_VERIFY_INSTALL_JSON, WATCHER_VERSION.

The trace records' retain-until date is not configuration: it is computed here from the packaged window record plus
TRACE_RETENTION_DAYS (contract item 0(a): the window's not-after + 400 days), the same rule the bucket policy enforces
(service/detect/infra/watcher.tf), so neither a deploy input nor a later deploy can move it (review M6).

{"watcher": "install-facts"} returns the facts this Lambda's verifier install.json must record (profile 15.9 R2), as
the issuer's poller does: deploy the bootstrap package, invoke with this event, rebuild with --install-json.

The handler never lets an exception out (review H4): the Lambda runtime would log its text. It logs the class name,
publishes a WATCHER_ERROR finding with the class name only, sends no heartbeat (D9 fires if it persists) and returns."""
import datetime as dt
import hashlib
import json
import os
import sys
from pathlib import Path

from . import receipts, stores
from . import sanitize as S
from .watcher import Config, Finding, Watcher, log

TASK = Path(os.environ.get("LAMBDA_TASK_ROOT", "/var/task"))
SHA1DC_BINARY = "/var/task/tessera-verify/bin/sha1dcsum"        # = package.LAMBDA_BINARY (a test checks)
TRACE_RETENTION_DAYS = 400                                      # = watcher.tf local.trace_retention_days (a test checks)


def retain_until(window):
    """The window's issuance not-after plus TRACE_RETENTION_DAYS, RFC 3339 (2028-03-07T00:00:00Z for the current one)."""
    na = dt.datetime.strptime(window["not_after"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.UTC)
    return (na + dt.timedelta(days=TRACE_RETENTION_DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")


def config_from_env(env):
    window = receipts.load_window(TASK / "config" / "window.json")
    return Config(
        account=env["ACCOUNT_ID"], kms_key_arn=env["KMS_KEY_ARN"],
        kms_aliases=tuple(a for a in env.get("KMS_ALIASES", "").split(",") if a),
        signer_role_arn=env["SIGNER_ROLE_ARN"], trail_prefix=env.get("TRAIL_PREFIX", ""),
        explorers=tuple(json.loads(env["EXPLORERS"])) if env.get("EXPLORERS") else Config.explorers,
        client_key_ids=json.loads(env.get("CLIENT_KEY_IDS") or "{}"),
        window=window,
        catalog=receipts.load_catalog(TASK / "freeze-v1" / "objects" / "catalog.json"),
        retain_until=retain_until(window), watcher_version=env.get("WATCHER_VERSION", ""))


def selfcheck(install_json):
    """The verifier's own startup check, as each D8 verifier process will run it (review M8): a stale or absent install
    record (another runtime's Unicode tables, a missing detector) makes every D8 check refuse. -> None, or its code."""
    def check():
        try:
            from tessera_verify import install_record
            install_record.load_and_apply(install_json)
            return None
        except Exception as e:  # noqa: BLE001
            c = getattr(e, "code", None)
            return c if S.is_code(c) else "SELF_CHECK_" + S.class_name(e).upper()[:40]
    return check


def from_env(env=None, remaining=lambda: 1e9):
    import boto3                                                    # only here: tests use fakes
    env = os.environ if env is None else env
    cfg = config_from_env(env)
    s3, ddb = boto3.client("s3"), boto3.client("dynamodb")
    until = dt.datetime.strptime(cfg.retain_until, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.UTC)
    install = env.get("TESSERA_VERIFY_INSTALL_JSON")

    def verify(bundle, window, catalog, as_of, explorers, budget_s=None):
        return receipts.verify(bundle, window, catalog, as_of, explorers, budget_s=budget_s, tmp="/tmp",
                               cli=lambda d, timeout: receipts.run_cli(d, install_json=install, timeout=timeout))

    return Watcher(cfg, stores.IssuerTable(ddb, env["REQUEST_TABLE"]), stores.Results(s3, env["RESULTS_BUCKET"]),
                   stores.TrailBucket(s3, env["TRAIL_BUCKET"]),
                   stores.StateObject(s3, env["STATE_BUCKET"], env.get("STATE_KEY", "state/watcher.json")),
                   stores.TraceBucket(s3, env["TRACE_BUCKET"], until),
                   stores.Topic(boto3.client("sns"), env["ALARM_TOPIC_ARN"]),
                   stores.Heartbeat(boto3.client("cloudwatch")), verify=verify, remaining=remaining,
                   outbox=stores.Outbox(s3, env["STATE_BUCKET"]), selfcheck=selfcheck(install))


def install_facts():
    from tessera_verify import install_record
    digest = hashlib.sha256(open(SHA1DC_BINARY, "rb").read()).hexdigest()
    return install_record.current_facts(SHA1DC_BINARY, digest)


def report_failure(exc, topic=None, out=None):
    """A failure of the run as a whole: class name only, to the log and (best effort) the alarm topic."""
    cls = S.class_name(exc)
    f = Finding("W", "WATCHER_ERROR", {"error_class": cls})
    log(f.line(), out)
    try:
        t = topic() if callable(topic) else topic
        if t is not None:
            t.publish(f.subject(), json.dumps(f.line(), sort_keys=True, indent=1))
    except BaseException as e:  # noqa: BLE001
        log({"event": "publish_failed", "v": 1, "error_class": S.class_name(e)}, out)
    return {"event": "watcher_error", "v": 1, "error_class": cls, "heartbeat": False}


def _topic_from_env():
    import boto3
    return stores.Topic(boto3.client("sns"), os.environ["ALARM_TOPIC_ARN"])


def handler(event, context, build=None, topic=_topic_from_env, out=None):
    try:
        if isinstance(event, dict) and event.get("watcher") == "install-facts":
            return install_facts()                                 # operator only; the schedule never sends it
        remaining = getattr(context, "get_remaining_time_in_millis", lambda: 1e9)
        return (build or from_env)(remaining=remaining).run()
    except BaseException as e:  # noqa: BLE001  never re-raised: the runtime would log the exception's text
        try:
            return report_failure(e, topic, out or sys.stdout)
        except BaseException:  # noqa: BLE001
            return {"event": "watcher_error", "v": 1, "heartbeat": False}
