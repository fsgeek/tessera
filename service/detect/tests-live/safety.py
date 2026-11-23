"""Built-in hard safety guards for Tessera V1 live detection tests.

Enforces Hard Safety Rules 1-6 from docs/reviews/detection-tests/BRIEF-gemini.md (r5):
- Region locked strictly to us-east-2 with no AWS endpoint override honoured.
- Global IAM client access requires explicit opt-in (allow_global_iam=True) and is
  pinned to iam.amazonaws.com.
- All created/mutated/deleted resources must match tessera-dtest-<run_id>-*, pass
  live tag ownership checks (purpose=detection-test AND run_id=<run_id>), and never
  reference production tessera-v1-* resources (narrow exception: subscribing and
  unsubscribing our verified throwaway SQS queue on tessera-v1-alarms, without
  touching its topic policy or any existing subscription).
- API calls are pinned to the exact us-east-2 API Gateway host and /v1 stage from
  TESSERA_API, never follow redirects, and allow ONLY read-only GET
  /v1/requests/<uuid> and malformed 400 POST /v1/requests with a missing or
  non-UUID Tessera-Request-Key (rejected before any DynamoDB write). Any POST
  the issuer records (such as D3b oversized 413) is forbidden and removed.
- Single process-wide client-side rate limiter strictly below 5 rps / burst 1.
- Strict redaction ensures no URL, credential, API key, SQS URL, or raw exception
  text is ever written to stdout, stderr, logs, or ledger files.
"""

from __future__ import annotations

import os
import re
import threading
import time
import urllib.parse
import uuid
from dataclasses import dataclass, field
from typing import Any, Iterable

ALLOWED_REGION = "us-east-2"
RESOURCE_PREFIX = "tessera-dtest-"
PURPOSE_TAG_KEY = "purpose"
PURPOSE_TAG_VALUE = "detection-test"
RUN_ID_TAG_KEY = "run_id"
PRODUCTION_ALARM_TOPIC_NAME = "tessera-v1-alarms"
PRODUCTION_ACCESS_LOG_GROUP = "/aws/apigateway/tessera-v1-issuer-access"
SMOKE_TEST_API_KEY_ID = "g8plxeex43"

# Usage plan limit is 5 rps, burst 20. Hard ceiling in code stays strictly below.
HARD_MAX_RPS = 4.5
HARD_MAX_BURST = 1

# Exact official AWS hostnames permitted by this test suite.
# Regional services are pinned to us-east-2; IAM is AWS's global service and
# requires allow_global_iam=True.
ALLOWED_AWS_ENDPOINTS: dict[str, str] = {
    "sts": f"sts.{ALLOWED_REGION}.amazonaws.com",
    "kms": f"kms.{ALLOWED_REGION}.amazonaws.com",
    "s3": f"s3.{ALLOWED_REGION}.amazonaws.com",
    "sns": f"sns.{ALLOWED_REGION}.amazonaws.com",
    "sqs": f"sqs.{ALLOWED_REGION}.amazonaws.com",
    "apigateway": f"apigateway.{ALLOWED_REGION}.amazonaws.com",
    "lambda": f"lambda.{ALLOWED_REGION}.amazonaws.com",
    "cloudtrail": f"cloudtrail.{ALLOWED_REGION}.amazonaws.com",
    "dynamodb": f"dynamodb.{ALLOWED_REGION}.amazonaws.com",
    "cloudwatch": f"monitoring.{ALLOWED_REGION}.amazonaws.com",
    "logs": f"logs.{ALLOWED_REGION}.amazonaws.com",
    "events": f"events.{ALLOWED_REGION}.amazonaws.com",
    "resourcegroupstaggingapi": f"tagging.{ALLOWED_REGION}.amazonaws.com",
    "iam": "iam.amazonaws.com",
}

_RUN_ID_RE = re.compile(r"^[a-z0-9]{4,16}$")
_NAME_RE = re.compile(r"^tessera-dtest-[a-z0-9]{4,16}-[a-z0-9][a-z0-9._-]{0,60}$")
_ACCOUNT_ID_RE = re.compile(r"^\d{12}$")
_STATUS_PATH_RE = re.compile(
    r"^/v1/requests/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)
_APIGW_HOST_RE = re.compile(
    rf"^[a-z0-9]{{10}}\.execute-api\.{re.escape(ALLOWED_REGION)}\.amazonaws\.com$",
    re.IGNORECASE,
)
_SQS_PATH_RE = re.compile(
    r"^/(\d{12})/(tessera-dtest-[a-z0-9]{4,16}-[a-z0-9][a-z0-9._-]{0,60})$"
)
_SQS_URL_REDACT_RE = re.compile(
    r"https?://sqs\.[a-z0-9-]+\.amazonaws\.com/\d{12}/([A-Za-z0-9._-]+)",
    re.IGNORECASE,
)
_URL_RE = re.compile(r"https?://[^\s\"'<>)\]}]+", re.IGNORECASE)
_AWS_KEY_RE = re.compile(r"\b(?:AKIA|ASIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA)[A-Z0-9]{16}\b")
_ERROR_CODE_RE = re.compile(r"^[A-Za-z0-9_.-]{1,64}$")

_SENSITIVE_DICT_KEYS = frozenset(
    {
        "secretaccesskey",
        "x-api-key",
        "apikeyvalue",
        "value",
        "authorization",
        "token",
        "password",
        "queue_url",
        "queueurl",
        "url",
        "endpoint",
        "base_url",
        "accesskeyid",
        "access_key_id",
        "raw_message_excerpt",
    }
)


class SafetyViolation(RuntimeError):
    """Raised whenever an action would violate a hard safety rule."""


class TopicPolicyChangeRequired(RuntimeError):
    """Raised if subscribing the observer SQS queue would require changing
    tessera-v1-alarms' topic policy (forbidden by Rule 1)."""


def validate_run_id(run_id: str) -> str:
    if not isinstance(run_id, str) or not _RUN_ID_RE.match(run_id):
        raise SafetyViolation(
            f"Invalid run_id: must match {_RUN_ID_RE.pattern}"
        )
    return run_id


def make_throwaway_name(run_id: str, suffix: str) -> str:
    """Build a validated throwaway resource name: tessera-dtest-<run_id>-<suffix>."""
    validate_run_id(run_id)
    cleaned = suffix.strip().lower()
    name = f"{RESOURCE_PREFIX}{run_id}-{cleaned}"
    assert_throwaway_name(name, run_id=run_id)
    return name


def assert_region(region: str | None) -> str:
    """Refuse any AWS region other than us-east-2 (Rule 2)."""
    if region != ALLOWED_REGION:
        raise SafetyViolation(
            f"Region locked to {ALLOWED_REGION!r}; refusing region={region!r}"
        )
    return region


def assert_aws_env_safe() -> None:
    """Verify ambient AWS env vars do not point outside us-east-2 or override endpoints."""
    for var in ("AWS_REGION", "AWS_DEFAULT_REGION"):
        val = os.environ.get(var)
        if val and val != ALLOWED_REGION:
            raise SafetyViolation(
                f"Environment variable {var} disagrees with locked region {ALLOWED_REGION!r}."
            )

    for var in ("AWS_ENDPOINT_URL", "AWS_USE_FIPS_ENDPOINT", "AWS_USE_DUALSTACK_ENDPOINT"):
        if os.environ.get(var, "").strip():
            raise SafetyViolation(
                f"AWS endpoint override environment variable {var} is forbidden."
            )

    for var, val in os.environ.items():
        if var.startswith("AWS_ENDPOINT_URL_") and val.strip():
            raise SafetyViolation(
                f"Service endpoint override environment variable {var} is forbidden."
            )

    sts_mode = os.environ.get("AWS_STS_REGIONAL_ENDPOINTS", "").strip().lower()
    if sts_mode and sts_mode != "regional":
        raise SafetyViolation(
            "AWS_STS_REGIONAL_ENDPOINTS must be unset or 'regional'."
        )


# Backwards-compatible alias for existing callers/tests.
assert_env_region_safe = assert_aws_env_safe


def assert_throwaway_name(
    identifier: str,
    *,
    allow_alias_prefix: bool = False,
    run_id: str | None = None,
    account_id: str | None = None,
) -> str:
    """Refuse any mutating/delete target that is not a tessera-dtest-* resource (Rules 1 & 2).

    When run_id and/or account_id are supplied, enforces exact run and account ownership.
    """
    if not identifier or not isinstance(identifier, str):
        raise SafetyViolation("Empty or non-string resource identifier refused.")

    if run_id is not None:
        validate_run_id(run_id)
        required_prefix = f"{RESOURCE_PREFIX}{run_id}-"
    else:
        required_prefix = RESOURCE_PREFIX

    if account_id is not None and not _ACCOUNT_ID_RE.match(account_id):
        raise SafetyViolation("Invalid AWS account_id supplied to safety guard.")

    if "tessera-v1" in identifier.lower():
        raise SafetyViolation("Refusing to mutate/delete production resource reference.")

    candidate = identifier
    if allow_alias_prefix and candidate.startswith("alias/"):
        candidate = candidate[len("alias/") :]

    if candidate.startswith("arn:"):
        parts = candidate.split(":")
        if len(parts) < 6 or parts[0] != "arn" or parts[1] != "aws":
            raise SafetyViolation("Malformed or non-commercial AWS ARN refused.")
        arn_service = parts[2]
        arn_region = parts[3]
        arn_account = parts[4]

        if arn_service in ("iam", "s3"):
            if arn_region and arn_region != ALLOWED_REGION:
                raise SafetyViolation(f"ARN region outside {ALLOWED_REGION!r} refused.")
        else:
            if arn_region != ALLOWED_REGION:
                raise SafetyViolation(f"ARN region outside {ALLOWED_REGION!r} refused.")

        if account_id is not None:
            if arn_service == "s3":
                if arn_account and arn_account != account_id:
                    raise SafetyViolation("ARN account does not match caller account.")
            else:
                if arn_account != account_id:
                    raise SafetyViolation("ARN account does not match caller account.")

        resource_part = ":".join(parts[5:])
        segment = resource_part.split("/")[-1].split(":")[-1]
        if not segment.startswith(required_prefix) or not _NAME_RE.match(segment):
            raise SafetyViolation("ARN resource does not match required throwaway prefix.")
        return identifier

    if candidate.startswith("https://") or candidate.startswith("http://"):
        parsed = urllib.parse.urlsplit(candidate)
        expected_sqs_host = ALLOWED_AWS_ENDPOINTS["sqs"]
        if (
            parsed.scheme != "https"
            or parsed.username is not None
            or parsed.password is not None
            or parsed.port is not None
            or parsed.query
            or parsed.fragment
            or (parsed.hostname or "").lower() != expected_sqs_host
        ):
            raise SafetyViolation("Non-pinned or malformed SQS URL refused.")
        m = _SQS_PATH_RE.match(parsed.path)
        if not m:
            raise SafetyViolation("SQS URL path failed strict throwaway pattern.")
        url_account, queue_name = m.group(1), m.group(2)
        if account_id is not None and url_account != account_id:
            raise SafetyViolation("SQS URL account does not match caller account.")
        if not queue_name.startswith(required_prefix):
            raise SafetyViolation("SQS queue name does not match required run prefix.")
        return identifier

    if not candidate.startswith(required_prefix):
        raise SafetyViolation("Resource name does not match required throwaway prefix.")
    if not _NAME_RE.match(candidate):
        raise SafetyViolation("Resource name failed strict throwaway pattern.")
    return identifier


def assert_ownership_tags(tags: dict[str, str] | None, run_id: str, context: str) -> None:
    """Verify live AWS tags prove purpose=detection-test AND run_id=<run_id>."""
    validate_run_id(run_id)
    if not isinstance(tags, dict):
        raise SafetyViolation(f"Missing tags for live ownership check ({context}).")
    if tags.get(PURPOSE_TAG_KEY) != PURPOSE_TAG_VALUE:
        raise SafetyViolation(
            f"Live tag {PURPOSE_TAG_KEY!r} mismatch for {context}; refusing mutation/delete."
        )
    if tags.get(RUN_ID_TAG_KEY) != run_id:
        raise SafetyViolation(
            f"Live tag {RUN_ID_TAG_KEY!r} mismatch for {context}; refusing mutation/delete."
        )


def assert_throwaway_id_registered(
    resource_id: str,
    registered_ids: set[str],
    resource_kind: str,
) -> str:
    """For AWS resources identified by opaque IDs, refuse to act unless registered."""
    if not resource_id or resource_id not in registered_ids:
        raise SafetyViolation(
            f"Refusing {resource_kind} operation on unregistered resource ID."
        )
    return resource_id


def validate_tessera_api_url(raw_url: str) -> tuple[str, str, str]:
    """Validate and pin TESSERA_API to an exact us-east-2 API Gateway /v1 stage URL.

    Returns (normalized_base_url, pinned_host, base_path).
    """
    cleaned = (raw_url or "").strip().rstrip("/")
    if not cleaned:
        raise SafetyViolation("TESSERA_API must be a non-empty https:// API Gateway URL.")
    parsed = urllib.parse.urlsplit(cleaned)
    if parsed.scheme != "https":
        raise SafetyViolation("TESSERA_API must use https://.")
    if parsed.username is not None or parsed.password is not None:
        raise SafetyViolation("TESSERA_API must not contain credentials/userinfo.")
    if parsed.port not in (None, 443):
        raise SafetyViolation("TESSERA_API must not specify a non-443 port.")
    if parsed.query or parsed.fragment:
        raise SafetyViolation("TESSERA_API must not contain query parameters or fragments.")
    host = (parsed.hostname or "").lower()
    if not _APIGW_HOST_RE.match(host):
        raise SafetyViolation(
            f"TESSERA_API host must be a {ALLOWED_REGION} execute-api.amazonaws.com endpoint."
        )
    base_path = parsed.path.rstrip("/")
    if base_path != "/v1":
        raise SafetyViolation(
            "TESSERA_API stage path must be exactly '/v1'."
        )
    normalized = f"https://{host}{base_path}"
    return normalized, host, base_path


def assert_safe_api_request(
    method: str,
    path: str,
    *,
    headers: dict[str, str],
    body: bytes | None,
    using_smoke_key: bool,
    post_refusal_mode: str | None = None,
    target_url: str | None = None,
    pinned_host: str | None = None,
    base_path: str = "/v1",
) -> None:
    """Enforce Hard Safety Rule 3 (r5) before every HTTP call to TESSERA_API.

    Allowed:
    - Read-only GET /v1/requests/<uuid>
    - POST /v1/requests ONLY in malformed_400 mode (missing or provably non-UUID
      Tessera-Request-Key, rejected at api.py:118-120 before any DynamoDB write).
    Any recorded POST (including oversized 413) is forbidden.
    """
    if target_url is not None:
        if not pinned_host:
            raise SafetyViolation("pinned_host is required when validating target_url.")
        parsed = urllib.parse.urlsplit(target_url)
        if parsed.scheme != "https":
            raise SafetyViolation("HTTP target must use https://.")
        if parsed.username is not None or parsed.password is not None:
            raise SafetyViolation("HTTP target must not contain userinfo.")
        if parsed.port not in (None, 443):
            raise SafetyViolation("HTTP target must not use a non-443 port.")
        if parsed.query or parsed.fragment:
            raise SafetyViolation("HTTP target must not contain query or fragment.")
        if (parsed.hostname or "").lower() != pinned_host.lower():
            raise SafetyViolation("HTTP target host does not match pinned TESSERA_API host.")
        expected_full_path = f"{base_path.rstrip('/')}{path}"
        if parsed.path != expected_full_path:
            raise SafetyViolation("HTTP target path does not match pinned stage + path.")

    method_up = method.upper()
    if method_up == "GET":
        if not _STATUS_PATH_RE.match(path):
            raise SafetyViolation(
                "GET path refused: only read-only /v1/requests/<uuid> is permitted."
            )
        return

    if method_up == "POST":
        if path != "/v1/requests":
            raise SafetyViolation("POST path refused: only /v1/requests is permitted.")
        if not using_smoke_key:
            raise SafetyViolation(
                "POST /v1/requests without TESSERA_SMOKE_KEY is forbidden by Rule 3."
            )
        if post_refusal_mode != "malformed_400":
            raise SafetyViolation(
                "POST refused: under Rule 3 (r5), only malformed_400 (non-UUID "
                "Tessera-Request-Key rejected before any record write) is permitted."
            )
        # Verify Tessera-Request-Key is missing or provably non-UUID so the issuer
        # rejects it at api.py:118-120 before any DynamoDB read or write.
        req_key = None
        for k, v in headers.items():
            if k.lower() == "tessera-request-key":
                req_key = v
                break
        if req_key is not None:
            try:
                uuid.UUID(req_key)
            except ValueError:
                return  # Provably invalid UUID -> 400 before any record write.
            raise SafetyViolation(
                "malformed_400 POST has a valid UUID Tessera-Request-Key; refusing!"
            )
        return

    raise SafetyViolation(f"HTTP method {method_up!r} is forbidden by Rule 3.")


def assert_post_was_refused(status_code: int, context: str) -> None:
    """Fail closed immediately if any POST ever receives a 2xx acceptance (Rule 3)."""
    if 200 <= status_code < 300:
        raise SafetyViolation(
            f"CRITICAL RULE 3 BREACH PREVENTED ({context}): POST returned HTTP {status_code}."
        )


@dataclass
class RateLimiter:
    """Process-wide pacer enforcing Rule 4 (always strictly below 5 rps, burst 1)."""

    rps: float = 2.0
    _last_ts: float = field(default=0.0, init=False, repr=False)
    _clock: Any = field(default=time.monotonic, repr=False)
    _sleeper: Any = field(default=time.sleep, repr=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False, repr=False)

    def __post_init__(self) -> None:
        self._validate_rps(self.rps)

    @staticmethod
    def _validate_rps(rps: float) -> None:
        if rps <= 0 or rps > HARD_MAX_RPS:
            raise SafetyViolation(
                f"Requested rps={rps} violates hard safety range (0, {HARD_MAX_RPS}] "
                "(usage plan limit is 5 rps)."
            )

    @property
    def min_interval_s(self) -> float:
        return 1.0 / self.rps

    def wait(self, *, rps: float | None = None) -> None:
        """Wait using the process-wide timestamp so back-to-back rows never burst."""
        if rps is not None:
            self._validate_rps(rps)
            effective_interval = max(self.min_interval_s, 1.0 / rps)
        else:
            effective_interval = self.min_interval_s

        with self._lock:
            now = self._clock()
            if self._last_ts > 0:
                elapsed = now - self._last_ts
                remaining = effective_interval - elapsed
                if remaining > 0:
                    self._sleeper(remaining)
            self._last_ts = self._clock()


@dataclass
class SmokeTestQuotaTracker:
    """Tracks cumulative daily requests sent with TESSERA_SMOKE_KEY (100/day quota)."""

    max_requests: int = 60
    prior_count: int = 0
    count: int = 0

    def __post_init__(self) -> None:
        if self.prior_count < 0 or self.count < 0 or self.max_requests < 0:
            raise SafetyViolation("Quota tracker counts must be non-negative.")

    @property
    def total_daily_count(self) -> int:
        return self.prior_count + self.count

    def ensure_headroom(self, needed: int, context: str = "") -> None:
        if self.total_daily_count + needed > self.max_requests:
            raise SafetyViolation(
                f"Smoke-test quota guard tripped ({context}): "
                f"prior={self.prior_count} + run={self.count} + needed={needed} "
                f"> max_requests={self.max_requests}."
            )

    def consume(self, n: int = 1) -> int:
        if self.total_daily_count + n > self.max_requests:
            raise SafetyViolation(
                f"Smoke-test quota guard tripped: {self.total_daily_count + n} "
                f"> max_requests={self.max_requests}. "
                "Pass --include-quota-exhaustion only when intentionally running D4c last."
            )
        self.count += n
        return self.total_daily_count

    def raise_cap_for_d4c(self, new_max: int = 120) -> None:
        if new_max > 120:
            raise SafetyViolation("D4c hard cap may never exceed 120 total daily requests.")
        if new_max > self.max_requests:
            self.max_requests = new_max


def safe_error_label(exc: BaseException) -> str:
    """Return ONLY the exception class name (and sanitized AWS error code if present).

    Never returns str(exc) so transport/SDK error messages containing URLs or secrets
    cannot leak to stdout, stderr, or ledger files (Rule 5).
    """
    cls_name = type(exc).__name__
    resp = getattr(exc, "response", None)
    if isinstance(resp, dict):
        err = resp.get("Error")
        if isinstance(err, dict):
            code = err.get("Code")
            if isinstance(code, str) and _ERROR_CODE_RE.match(code):
                return f"{cls_name}({code})"
    return cls_name


def _expand_secrets(secrets: Iterable[str]) -> list[str]:
    expanded: list[str] = []
    for s in secrets:
        if not s:
            continue
        expanded.append(s)
        if "://" in s:
            parsed = urllib.parse.urlsplit(s)
            if parsed.hostname:
                expanded.append(parsed.hostname)
    # Longest first so full URLs redact before substrings.
    return sorted(set(expanded), key=len, reverse=True)


def sanitize_value(value: Any, secrets: Iterable[str] = ()) -> Any:
    """Recursively redact secrets, ALL URLs, SQS URLs, and AWS key IDs (Rule 5).

    Sanitizes both dict keys and values.
    """
    secret_list = _expand_secrets(secrets)
    return _sanitize_inner(value, secret_list)


def _sanitize_str(text: str, secret_list: list[str]) -> str:
    out = text
    for s in secret_list:
        out = out.replace(s, "[REDACTED]")
    out = _SQS_URL_REDACT_RE.sub(r"sqs-queue:\1", out)
    out = _URL_RE.sub("[REDACTED_URL]", out)
    out = _AWS_KEY_RE.sub("[REDACTED_AWS_KEY_ID]", out)
    return out


def _sanitize_inner(value: Any, secret_list: list[str]) -> Any:
    if isinstance(value, str):
        return _sanitize_str(value, secret_list)
    if isinstance(value, dict):
        sanitized: dict[str, Any] = {}
        for k, v in value.items():
            clean_k = _sanitize_str(str(k), secret_list)
            if clean_k.lower() in _SENSITIVE_DICT_KEYS:
                sanitized[clean_k] = "[REDACTED]"
            else:
                sanitized[clean_k] = _sanitize_inner(v, secret_list)
        return sanitized
    if isinstance(value, list):
        return [_sanitize_inner(item, secret_list) for item in value]
    if isinstance(value, tuple):
        return [_sanitize_inner(item, secret_list) for item in value]
    return value


def _verify_client_endpoint(client: Any, service_name: str, expected_host: str) -> None:
    meta = getattr(client, "meta", None)
    if meta is None:
        return
    region = getattr(meta, "region_name", None)
    if region is not None and region != ALLOWED_REGION:
        raise SafetyViolation(
            f"AWS client for {service_name} resolved outside {ALLOWED_REGION!r}."
        )
    ep = getattr(meta, "endpoint_url", None)
    if ep is not None:
        parsed = urllib.parse.urlsplit(str(ep))
        if (
            parsed.scheme != "https"
            or (parsed.hostname or "").lower() != expected_host.lower()
            or parsed.port not in (None, 443)
        ):
            raise SafetyViolation(
                f"AWS client for {service_name} resolved to disallowed endpoint."
            )


def locked_boto3_client(
    service_name: str,
    *,
    session: Any = None,
    allow_global_iam: bool = False,
) -> Any:
    """Create a boto3 client strictly bound to us-east-2 with no endpoint override (Rule 2)."""
    assert_aws_env_safe()
    if service_name not in ALLOWED_AWS_ENDPOINTS:
        raise SafetyViolation(f"AWS service {service_name!r} is not on the allowed list.")
    if service_name == "iam" and not allow_global_iam:
        raise SafetyViolation(
            "IAM is a global account-wide service; allow_global_iam=True is required."
        )

    expected_host = ALLOWED_AWS_ENDPOINTS[service_name]
    expected_endpoint = f"https://{expected_host}"

    if session is None:
        import boto3  # Imported lazily so offline unit tests run without boto3.
        from botocore.config import Config

        cfg = Config(region_name=ALLOWED_REGION, retries={"max_attempts": 1})
        client = boto3.client(
            service_name,
            region_name=ALLOWED_REGION,
            endpoint_url=expected_endpoint,
            config=cfg,
        )
    else:
        try:
            client = session.client(
                service_name,
                region_name=ALLOWED_REGION,
                endpoint_url=expected_endpoint,
            )
        except TypeError:
            client = session.client(service_name, region_name=ALLOWED_REGION)

    _verify_client_endpoint(client, service_name, expected_host)
    return client
