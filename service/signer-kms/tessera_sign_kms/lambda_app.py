"""Lambda entry point: `handler`, invoked by the SQS event source mapping on the kms slot's request queue (infra/).
from_env() builds the signer from environment variables set by infra/; boto3 is imported only here.

Environment: KMS_KEY_ID (key id or ARN), KEY_FP (the pinned spki-sha256 fingerprint; the signer does not start
without it or if KMS's key differs), SIGN_UNTIL (RFC 3339: the window's signing stop, not-after minus 96 h, IS-03),
RESPONSE_QUEUE_URL, FRAMES_BUCKET (the issuer's result bucket; only frames/* is readable, IS-09).

The mapping reports partial batch failures (ReportBatchItemFailures): a message whose handling raised Retry, or whose
response could not be sent, is returned in batchItemFailures and SQS delivers it again; every other message is
answered on the response queue and then deleted by the mapping."""
import json
import os
import sys

from .signer import MAX_FRAME, KmsSigner, Retry

_SIGNER = None

# As the issuer's lambda_app (CF3-01): bound the client's own time per AWS call.
AWS_CLIENT_CONFIG = {"connect_timeout": 5, "read_timeout": 20,
                     "retries": {"mode": "standard", "total_max_attempts": 3}}


def log_line(entry):
    print(json.dumps(entry, sort_keys=True), file=sys.stdout, flush=True)


def _not_found(exc):
    code = getattr(exc, "response", {}).get("Error", {}).get("Code")
    return code in ("NoSuchKey", "404", "NotFound") or type(exc).__name__ == "NoSuchKey"


def s3_fetch(client, bucket):
    """IS-09: frame reference -> the object's bytes, None if there is no such object; other errors raise."""
    def fetch(ref):
        try:
            body = client.get_object(Bucket=bucket, Key=ref)["Body"]
        except Exception as e:  # noqa: BLE001
            if _not_found(e):
                return None
            raise
        return body.read(MAX_FRAME + 1)
    return fetch


class SqsResponses:
    def __init__(self, client, url):
        self.client, self.url = client, url

    def send(self, body):
        return self.client.send_message(QueueUrl=self.url, MessageBody=body)["MessageId"]


def from_env(env=None, session=None, clock=None):
    """-> (signer, responses)."""
    env = os.environ if env is None else env
    kw = {}
    if session is None:                                # the Lambda path; tests pass a fake session
        import boto3
        from botocore.config import Config
        session = boto3.session.Session()
        kw["config"] = Config(**AWS_CLIENT_CONFIG)
    kms, s3, sqs = (session.client(n, **kw) for n in ("kms", "s3", "sqs"))
    if clock is None:
        import time
        clock = lambda: int(time.time())               # noqa: E731
    from .signer import ts
    signer = KmsSigner(kms, env["KMS_KEY_ID"], env.get("KEY_FP", ""), ts(env["SIGN_UNTIL"]),
                       s3_fetch(s3, env["FRAMES_BUCKET"]), clock, log_line)
    return signer, SqsResponses(sqs, env["RESPONSE_QUEUE_URL"])


def handle_event(signer, responses, event):
    """SQS event -> {"batchItemFailures": [...]}. Plain function; handler binds the signer."""
    failures = []
    for rec in event.get("Records") or []:
        mid = rec.get("messageId")
        try:
            count = int((rec.get("attributes") or {}).get("ApproximateReceiveCount", "1"))
        except ValueError:
            count = 1
        try:
            resp = signer.handle(rec.get("body"), count, mid)
            responses.send(json.dumps(resp, sort_keys=True))
        except Retry:
            failures.append({"itemIdentifier": mid})
        except Exception as e:  # noqa: BLE001  the response was not sent: deliver the request again
            log_line({"event": "response-not-sent", "message_id": mid, "detail": f"{type(e).__name__}: {e}"})
            failures.append({"itemIdentifier": mid})
    return {"batchItemFailures": failures}


def handler(event, context):
    global _SIGNER
    if _SIGNER is None:
        _SIGNER = from_env()
    return handle_event(*_SIGNER, event)
