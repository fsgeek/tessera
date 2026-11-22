"""The secrecy boundary of every output (review H4). Each string the watcher emits to a finding, a log line, an SNS
message, a trace record or its own state passes the validator of its field, or is replaced by WITHHELD. A field with
no rule is withheld. Nothing is truncated into shape: a value either matches its rule exactly or does not appear.

So a URL, a plaintext request key, request content, an API key value or exception text placed by a fault or an
attacker in any issuer field (a SIGLOG reason, a request id, a disposition) cannot reach an output: none of them
matches the field's rule. Exceptions are reported by class name only (`error_class`)."""
import re

WITHHELD = "<withheld>"

CODE = re.compile(r"[A-Z0-9_]{1,64}")
HEX64 = re.compile(r"[0-9a-f]{64}")
HEX16 = re.compile(r"[0-9a-f]{16}")
HEX_ANY = re.compile(r"[0-9a-f]{1,64}")
RFC3339 = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
SIGNER_REQUEST_ID = re.compile(r"req-[0-9a-f]{40}|invalid:[0-9a-f]{32}")
ATTEMPT_ID = re.compile(r"a[0-9]{1,3}")
JOB_NAME = re.compile(r"[sp]_(kms|gpg)")
CLASS_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]{0,63}")
EVENT_NAME = re.compile(r"[A-Z][A-Za-z0-9]{0,63}")       # an AWS API action name
ERROR_CODE = re.compile(r"[A-Za-z0-9.]{1,64}")
REGION = re.compile(r"[a-z]{2}(-[a-z]+)+-[0-9]")
# A role or user ARN in this partition: no scheme, no query, no space (the path characters IAM allows).
PRINCIPAL_ARN = re.compile(r"arn:aws:(iam|sts)::[0-9]{12}:[A-Za-z0-9+=,.@/_-]{1,200}")
CONFIG_NAME = re.compile(r"[A-Za-z0-9_-]{1,64}")
STAMP = re.compile(r"[0-9]{8}T[0-9]{4}Z")

IDENTITY_TYPES = frozenset({"Root", "IAMUser", "AssumedRole", "FederatedUser", "AWSAccount", "AWSService",
                            "WebIdentityUser", "SAMLUser", "IdentityCenterUser", "Unknown", "unknown"})
DETECTIONS = frozenset({"D5", "D6", "D7", "D8", "W"})
SLOTS = frozenset({"kms", "gpg"})
SIGLOG_STATUSES = frozenset({"SIGNED", "REFUSED", "OTHER"})
DISPOSITIONS = frozenset({"used", "duplicate", "not-waiting", "other-attempt", "refused", "unrequested", "malformed",
                          "bad-signature", "superseded:not-waiting", "superseded:duplicate", "superseded:used",
                          "superseded:save-conflict", None})
REQUEST_STATES = frozenset({"COMPLETE", "REFUSED", "FAILED"})
ATTEMPT_STATES = frozenset({"open", "latched", "shipped", "expired", "discarded", "unavail"})
RECONCILED = frozenset({"matched", "unmatched", "before-coverage", "pending", "not-counted", "not-logged"})
SOURCES = frozenset({"issuer_table", "trail", "siglog", "request", "outbox", "results", "trace", "heartbeat"})
RECORD_SOURCES = frozenset({"issuer-record", "snapshot"})
BINDING = frozenset({"match", "mismatch", "unreadable", "not-recorded", None})
BINDING_FIELDS = frozenset({"content_sha256", "content_len", "s_kms", "s_gpg", "p_kms", "p_gpg", "receipt_id",
                            "declared_issue_time"})
# Fixed texts written by this package only (they are constants, not data).
NOTES = frozenset({
    "read from the trail: CloudTrail delivery plus up to one watcher interval",
    "TODO: slot 2 reconciliation not built (G4)",
    "TODO: GCP useToSign not read (G4 open)",
})


def is_code(v):
    return isinstance(v, str) and CODE.fullmatch(v) is not None


def _re(rx):
    return lambda v: v if isinstance(v, str) and rx.fullmatch(v) else WITHHELD


def _enum(values):
    return lambda v: v if (v is None or isinstance(v, str)) and v in values else WITHHELD


def _opt(rule):
    return lambda v: None if v is None else rule(v)


def _int(lo=0, hi=10 ** 12):
    return lambda v: v if isinstance(v, int) and not isinstance(v, bool) and lo <= v <= hi else WITHHELD


def _bool(v):
    return v if isinstance(v, bool) else WITHHELD


def code(v):
    return v if is_code(v) else WITHHELD


def rid_prefix(v):
    """A request id is the issuer's 64-hex record id; outputs other than the trace carry its first 16 hex digits."""
    if isinstance(v, str) and (HEX64.fullmatch(v) or HEX16.fullmatch(v)):
        return v[:16]
    return WITHHELD


def principal(v):
    if isinstance(v, str) and (PRINCIPAL_ARN.fullmatch(v) or v in IDENTITY_TYPES):
        return v
    return WITHHELD


def class_name(exc):
    """The class name of an exception, never its text."""
    n = type(exc).__name__
    return n if CLASS_NAME.fullmatch(n) else WITHHELD


def split_code(v):
    """An issuer reason such as SIGNER_REFUSED:KEY_FP_MISMATCH -> ("SIGNER_REFUSED", "KEY_FP_MISMATCH"); each part is a
    code or WITHHELD. None -> (None, None)."""
    if v is None:
        return None, None
    if not isinstance(v, str):
        return WITHHELD, None
    head, sep, tail = v.partition(":")
    return code(head), (code(tail) if sep else None)


def heights(v):
    if isinstance(v, list) and all(isinstance(h, int) and not isinstance(h, bool) and 0 <= h < 10 ** 7 for h in v):
        return v
    return None if v is None else WITHHELD


def dispositions(v):
    if not isinstance(v, list):
        return WITHHELD
    return [_enum(DISPOSITIONS)(d) for d in v]


def mismatches(v):
    if not isinstance(v, list):
        return WITHHELD
    return [d if d in BINDING_FIELDS else WITHHELD for d in v]


RULES = {
    "detection": _enum(DETECTIONS),
    "code": code, "reason": _opt(code), "reason_detail": _opt(code), "verdict": _opt(code),
    "verifier_verdict": _opt(code), "outcome": _opt(code),
    "rid": rid_prefix,
    "item": _re(HEX_ANY),
    "receipt_sha256": _opt(_re(HEX64)), "stored_sha256": _re(HEX64), "signature_sha256": _opt(_re(HEX64)),
    "frame_sha256": _opt(_re(HEX64)), "credential_digest": _opt(_re(HEX64)), "content_sha256": _opt(_re(HEX64)),
    "request_key_sha256": _opt(_re(HEX64)), "receipt_id": _opt(_re(HEX64)), "watcher_version": _re(HEX64),
    "slot": _opt(_enum(SLOTS)), "status": _opt(_enum(SIGLOG_STATUSES)), "disposition": _enum(DISPOSITIONS),
    "dispositions": dispositions, "state": _opt(_enum(REQUEST_STATES | ATTEMPT_STATES)),
    "request_id": _opt(_re(SIGNER_REQUEST_ID)), "signer_request_id": _opt(_re(SIGNER_REQUEST_ID)),
    "attempt": _opt(_re(ATTEMPT_ID)), "id": _opt(_re(ATTEMPT_ID)), "job": _re(JOB_NAME),
    "at": _opt(_re(RFC3339)), "event_time": _opt(_re(RFC3339)), "logged_at": _opt(_re(RFC3339)),
    "checked_at": _opt(_re(RFC3339)), "written_at": _re(RFC3339), "created_at": _opt(_re(RFC3339)),
    "ended_at": _opt(_re(RFC3339)), "declared_issue_time": _opt(_re(RFC3339)), "T": _opt(_re(RFC3339)),
    "file_time": _opt(_re(STAMP)),
    "event_id": _opt(_re(UUID)), "cloudtrail_sign_event_id": _opt(_re(UUID)),
    "event_name": _opt(_re(EVENT_NAME)), "error_code": _opt(_re(ERROR_CODE)), "region": _opt(_re(REGION)),
    "principal": principal, "error_class": _re(CLASS_NAME),
    "api_key_id": _opt(_re(CONFIG_NAME)), "client": _opt(_re(CONFIG_NAME)),
    "content_len": _opt(_int()), "bound_s": _int(), "anchor_heights": heights, "pending": _int(),
    "reconciled": _enum(RECONCILED), "source": _enum(SOURCES), "record_source": _enum(RECORD_SOURCES),
    "binding": _enum(BINDING), "mismatch": mismatches, "latency_note": _enum(NOTES),
    "gcp_use_to_sign": _enum(NOTES), "slot2_reconciliation": _enum(NOTES), "format": _enum({"tessera-v1-trace/1"}),
    "before_coverage": _bool,
}


def clean(name, value):
    """The value of one named field, or WITHHELD. A field with no rule is withheld whatever its value."""
    rule = RULES.get(name)
    if rule is None:
        return WITHHELD
    try:
        return rule(value)
    except Exception:  # noqa: BLE001  a validator never raises into the caller
        return WITHHELD


def clean_fields(d):
    """Every field of a flat dict through clean(); a `reason` that carries a sub-code is split (split_code)."""
    out = {}
    for k, v in d.items():
        if k == "reason" and isinstance(v, str) and ":" in v:
            out["reason"], out["reason_detail"] = split_code(v)
        else:
            out[k] = clean(k, v)
    return out
