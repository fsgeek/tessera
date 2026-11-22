"""Lambda entry point. Environment (set by service/detect/infra; names and identifiers only, no secret):

ACCOUNT_ID, KMS_KEY_ARN, KMS_ALIASES (comma-separated), SIGNER_ROLE_ARN, REQUEST_TABLE, RESULTS_BUCKET, TRAIL_BUCKET,
TRAIL_PREFIX, STATE_BUCKET, STATE_KEY, TRACE_BUCKET, TRACE_RETAIN_UNTIL (RFC 3339), ALARM_TOPIC_ARN, EXPLORERS (JSON
list), CLIENT_KEY_IDS (JSON {client name: API key id}), TESSERA_VERIFY_INSTALL_JSON, WATCHER_VERSION.

{"watcher": "install-facts"} returns the facts this Lambda's verifier install.json must record (profile 15.9 R2), as
the issuer's poller does: deploy the bootstrap package, invoke with this event, rebuild with --install-json."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path

from . import receipts, stores
from .watcher import Config, Watcher

TASK = Path(os.environ.get("LAMBDA_TASK_ROOT", "/var/task"))
SHA1DC_BINARY = "/var/task/tessera-verify/bin/sha1dcsum"        # = package.LAMBDA_BINARY (a test checks)


def config_from_env(env):
    return Config(
        account=env["ACCOUNT_ID"], kms_key_arn=env["KMS_KEY_ARN"],
        kms_aliases=tuple(a for a in env.get("KMS_ALIASES", "").split(",") if a),
        signer_role_arn=env["SIGNER_ROLE_ARN"], trail_prefix=env.get("TRAIL_PREFIX", ""),
        explorers=tuple(json.loads(env["EXPLORERS"])) if env.get("EXPLORERS") else Config.explorers,
        client_key_ids=json.loads(env.get("CLIENT_KEY_IDS") or "{}"),
        window=receipts.load_window(TASK / "config" / "window.json"),
        catalog=receipts.load_catalog(TASK / "freeze-v1" / "objects" / "catalog.json"),
        retain_until=env["TRACE_RETAIN_UNTIL"], watcher_version=env.get("WATCHER_VERSION", ""))


def from_env(env=None, remaining=lambda: 1e9):
    import boto3                                                    # only here: tests use fakes
    env = os.environ if env is None else env
    cfg = config_from_env(env)
    s3, ddb = boto3.client("s3"), boto3.client("dynamodb")
    until = dt.datetime.strptime(cfg.retain_until, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.UTC)
    install = env.get("TESSERA_VERIFY_INSTALL_JSON")

    def verify(bundle, window, catalog, as_of, explorers):
        return receipts.verify(bundle, window, catalog, as_of, explorers,
                               cli=lambda d: receipts.run_cli(d, install_json=install, timeout=300), tmp="/tmp")

    return Watcher(cfg, stores.IssuerTable(ddb, env["REQUEST_TABLE"]), stores.Results(s3, env["RESULTS_BUCKET"]),
                   stores.TrailBucket(s3, env["TRAIL_BUCKET"]),
                   stores.StateObject(s3, env["STATE_BUCKET"], env.get("STATE_KEY", "state/watcher.json")),
                   stores.TraceBucket(s3, env["TRACE_BUCKET"], until),
                   stores.Topic(boto3.client("sns"), env["ALARM_TOPIC_ARN"]),
                   stores.Heartbeat(boto3.client("cloudwatch")), verify=verify, remaining=remaining)


def install_facts():
    from tessera_verify import install_record
    digest = hashlib.sha256(open(SHA1DC_BINARY, "rb").read()).hexdigest()
    return install_record.current_facts(SHA1DC_BINARY, digest)


def handler(event, context):
    if isinstance(event, dict) and event.get("watcher") == "install-facts":
        return install_facts()                                     # operator only; the schedule never sends it
    remaining = getattr(context, "get_remaining_time_in_millis", lambda: 1e9)
    return from_env(remaining=remaining).run()
