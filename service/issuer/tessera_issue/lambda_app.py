"""Lambda entry points: api_handler (API Gateway REST proxy; the API key id is the client credential) and
poller_handler (EventBridge schedule, every 10 minutes; reserved concurrency 1). from_env() builds the issuer from
environment variables set by infra/; boto3 is imported only here.

Environment: REQUEST_TABLE, RESULT_BUCKET, FREEZE_DIR (packaged frozen objects), WINDOW_OBJECT (default
config/window.json in RESULT_BUCKET), KMS_REQUEST_QUEUE_URL, KMS_RESPONSE_QUEUE_URL, GPG_REQUEST_QUEUE_URL,
GPG_RESPONSE_QUEUE_URL, KMS_WAKE_TOPIC_ARN, GPG_WAKE_TOPIC_ARN (optional), OTS_CALENDARS, EXPLORERS (comma lists),
DNS_RESOLVER, CLOSING, SIGNING_AVAILABLE ("true"/"false"), TESSERA_VERIFY_INSTALL_JSON (the packaged verifier's
install record, for the pre-ship checks)."""
import base64
import json
import os

from . import api, freeze, pipeline, window as window_mod
from .aws import DynamoRequestStore, S3ResultStore, SnsWake
from .chain import ExplorerHeaders
from .dns import LiveDns, udp_tcp_transport
from .ots import HttpCalendar, urllib_transport
from .preship import PreShip
from .queues import SqsQueue
from .service import Issuer
from .signers import SlotSigner

_ISSUER = None


def from_env(env=None, session=None):
    env = os.environ if env is None else env
    if session is None:
        import boto3
        session = boto3.session.Session()
    ddb, s3, sqs, sns = (session.client(n) for n in ("dynamodb", "s3", "sqs", "sns"))
    results = S3ResultStore(s3, env["RESULT_BUCKET"])
    win = window_mod.load_json(results.get_config(env.get("WINDOW_OBJECT", "window.json")).decode())
    frozen = freeze.load(env["FREEZE_DIR"])
    wake = SnsWake(sns, {"kms": env.get("KMS_WAKE_TOPIC_ARN"), "gpg": env.get("GPG_WAKE_TOPIC_ARN")})
    signers = {"kms": SlotSigner("kms", win.kms_key, SqsQueue(sqs, env["KMS_REQUEST_QUEUE_URL"]),
                                 SqsQueue(sqs, env["KMS_RESPONSE_QUEUE_URL"]), wake),
               "gpg": SlotSigner("gpg", win.gpg_key, SqsQueue(sqs, env["GPG_REQUEST_QUEUE_URL"]),
                                 SqsQueue(sqs, env["GPG_RESPONSE_QUEUE_URL"]), wake)}
    http = urllib_transport()
    return Issuer(window=win, frozen=frozen, requests=DynamoRequestStore(ddb, env["REQUEST_TABLE"]), results=results,
                  signers=signers,
                  calendars=[HttpCalendar(u, http) for u in env["OTS_CALENDARS"].split(",") if u],
                  headers=ExplorerHeaders([u for u in env["EXPLORERS"].split(",") if u], http),
                  dns=LiveDns(udp_tcp_transport(env.get("DNS_RESOLVER", "1.1.1.1"))),
                  preship=PreShip(frozen, win.trust_base, env.get("TESSERA_VERIFY_INSTALL_JSON")),
                  closing=env.get("CLOSING", "false") == "true",
                  signing_available=env.get("SIGNING_AVAILABLE", "true") == "true")


def _issuer():
    global _ISSUER
    if _ISSUER is None:
        _ISSUER = from_env()
    return _ISSUER


def handle_api_event(iss, event):
    """API Gateway REST proxy event -> proxy response. Plain function; api_handler binds the issuer."""
    method = event.get("httpMethod")
    resource = event.get("resource") or ""
    headers = {k.lower(): v for k, v in (event.get("headers") or {}).items()}
    cred = ((event.get("requestContext") or {}).get("identity") or {}).get("apiKeyId")
    key = (event.get("pathParameters") or {}).get("key")
    if method == "POST" and resource == "/v1/requests":
        raw = event.get("body") or ""
        try:
            body = base64.b64decode(raw, validate=True) if event.get("isBase64Encoded") else raw.encode("utf-8")
        except ValueError:
            body = None
        if body is None:
            resp = api.Response(400, {"state": "REFUSED", "reason": "BAD_REQUEST"})
        else:
            resp = api.submit(iss, cred, headers.get("tessera-request-key"), body)
    elif method == "GET" and resource == "/v1/requests/{key}":
        resp = api.status(iss, cred, key)
    elif method == "GET" and resource == "/v1/requests/{key}/receipt":
        resp = api.receipt(iss, cred, key)
    else:
        resp = api.Response(404, {"error": "NOT_FOUND"})
    status, hdrs, data = api.encode(resp)
    return {"statusCode": status, "headers": hdrs, "body": data.decode("utf-8"), "isBase64Encoded": False}


def api_handler(event, context):
    return handle_api_event(_issuer(), event)


def poller_handler(event, context):
    out = pipeline.poll(_issuer())
    return json.loads(json.dumps(out, default=str))
