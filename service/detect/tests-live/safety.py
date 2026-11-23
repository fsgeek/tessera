"""Built-in hard safety guards for Tessera V1 live detection tests.

Enforces Hard Safety Rules 1-6 from docs/reviews/detection-tests/BRIEF-gemini.md:
- Region locked strictly to us-east-2.
- All created/mutated/deleted resources must match tessera-dtest-<run_id>-*.
- Production resources (tessera-v1-*, alias/tessera-v1-kms, etc.) may never be
  mutated, deleted, disabled, or invoked with side effects (narrow exception:
  subscribing/unsubscribing our own throwaway SQS queue on tessera-v1-alarms,
  without touching its topic policy or existing subscriptions).
- API calls are restricted to read-only GET /v1/requests/{uuid} and POST
  /v1/requests payloads guaranteed to be refused (400 malformed or 413 > 1 MiB).
  Any 2xx response to a POST aborts the run immediately.
- Client-side rate limiter strictly below the usage plan's 5 rps / burst 20.
- Redaction helper ensures TESSERA_API, TESSERA_SMOKE_KEY, and any transient
  AWS credentials are never written to stdout, logs, or ledger files.
"""

from __future__ import annotations

import os
import re
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Iterable

ALLOWED_REGION = "us-east-2"
RESOURCE_PREFIX = "tessera-dtest-"
PURPOSE_TAG_KEY = "purpose"
PURPOSE_TAG_VALUE = "detection-test"
PRODUCTION_ALARM_TOPIC_NAME = "tessera-v1-alarms"

# Issuer submission max body size is 1 MiB (1,048,576 bytes).
ISSUER_MAX_BODY_BYTES = 1_048_576
# Oversized D3b payload: strictly > 1 MiB, safely < 6 MiB Lambda sync limit
# (1,100,000 raw bytes ~ 1.47 MiB base64 in API Gateway Lambda proxy).
OVERSIZED_PAYLOAD_BYTES = 1_100_000

# Usage plan limit is 5 rps, burst 20. Hard ceiling in code stays strictly below.
HARD_MAX_RPS = 4.5
HARD_MAX_BURST = 1

_RUN_ID_RE = re.compile(r"^[a-z0-9]{4,16}$")
_NAME_RE = re.compile(r"^tessera-dtest-[a-z0-9]{4,16}-[a-z0-9][a-z0-9._-]{0,60}$")
_STATUS_PATH_RE = re.compile(
    r"^/v1/requests/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)
_AWS_KEY_RE = re.compile(r"\b(?:AKIA|ASIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA)[A-Z0-9]{16}\b")


class SafetyViolation(RuntimeError):
    """Raised whenever an action would violate a hard safety rule."""


class TopicPolicyChangeRequired(RuntimeError):
    """Raised if subscribing the observer SQS queue would require changing
    tessera-v1-alarms' topic policy (forbidden by Rule 1)."""


def validate_run_id(run_id: str) -> str:
    if not _RUN_ID_RE.match(run_id):
        raise SafetyViolation(
            f"Invalid run_id {run_id!r}: must match {_RUN_ID_RE.pattern}"
        )
    return run_id


def make_throwaway_name(run_id: str, suffix: str) -> str:
    """Build a validated throwaway resource name: tessera-dtest-<run_id>-<suffix>."""
    validate_run_id(run_id)
    cleaned = suffix.strip().lower()
    name = f"{RESOURCE_PREFIX}{run_id}-{cleaned}"
    assert_throwaway_name(name)
    return name


def assert_region(region: str | None) -> str:
    """Refuse any AWS region other than us-east-2 (Rule 2)."""
    if region != ALLOWED_REGION:
        raise SafetyViolation(
            f"Region locked to {ALLOWED_REGION!r}; refusing region={region!r}"
        )
    return region


def assert_env_region_safe() -> None:
    """Verify ambient AWS region env vars do not point outside us-east-2."""
    for var in ("AWS_REGION", "AWS_DEFAULT_REGION"):
        val = os.environ.get(var)
        if val and val != ALLOWED_REGION:
            raise SafetyViolation(
                f"Environment variable {var}={val!r} disagrees with locked region "
                f"{ALLOWED_REGION!r}. Unset it or set it to {ALLOWED_REGION}."
            )


def assert_throwaway_name(
    identifier: str,
    *,
    allow_alias_prefix: bool = False,
) -> str:
    """Refuse any mutating/delete target that is not a tessera-dtest-* resource (Rules 1 & 2)."""
    if not identifier or not isinstance(identifier, str):
        raise SafetyViolation("Empty or non-string resource identifier refused.")

    lower = identifier.lower()
    if "tessera-v1" in lower:
        raise SafetyViolation(
            f"Refusing to mutate/delete production resource reference: {identifier!r}"
        )

    candidate = identifier
    if allow_alias_prefix and candidate.startswith("alias/"):
        candidate = candidate[len("alias/") :]

    # If an ARN or SQS URL is passed, extract the resource segment and verify it
    # starts with tessera-dtest-.
    if candidate.startswith("arn:"):
        parts = candidate.split(":")
        if len(parts) < 6:
            raise SafetyViolation(f"Malformed ARN refused: {identifier!r}")
        arn_region = parts[3]
        if arn_region and arn_region != ALLOWED_REGION:
            raise SafetyViolation(
                f"ARN region {arn_region!r} is outside locked region {ALLOWED_REGION!r}: {identifier!r}"
            )
        resource_part = ":".join(parts[5:])
        # Handle forms like role/tessera-dtest-..., function:tessera-dtest-...,
        # trail/tessera-dtest-..., rule/tessera-dtest-..., table/tessera-dtest-...,
        # or plain topic/queue/bucket name.
        segment = resource_part.split("/")[-1].split(":")[-1]
        if not segment.startswith(RESOURCE_PREFIX):
            raise SafetyViolation(
                f"ARN resource {segment!r} does not start with {RESOURCE_PREFIX!r}: {identifier!r}"
            )
        return identifier

    if candidate.startswith("https://sqs."):
        if f".{ALLOWED_REGION}." not in candidate:
            raise SafetyViolation(
                f"SQS URL outside {ALLOWED_REGION!r} refused: {identifier!r}"
            )
        queue_name = candidate.rstrip("/").split("/")[-1]
        if not queue_name.startswith(RESOURCE_PREFIX):
            raise SafetyViolation(
                f"SQS queue {queue_name!r} does not start with {RESOURCE_PREFIX!r}"
            )
        return identifier

    if not candidate.startswith(RESOURCE_PREFIX):
        raise SafetyViolation(
            f"Resource {identifier!r} does not start with {RESOURCE_PREFIX!r}"
        )
    if not _NAME_RE.match(candidate):
        raise SafetyViolation(
            f"Resource name {candidate!r} failed strict throwaway pattern {_NAME_RE.pattern}"
        )
    return identifier


def assert_throwaway_id_registered(
    resource_id: str,
    registered_ids: set[str],
    resource_kind: str,
) -> str:
    """For AWS resources identified by opaque IDs (KMS KeyId, API GW IDs,
    SubscriptionArn), refuse to act unless the ID was created by this run."""
    if not resource_id or resource_id not in registered_ids:
        raise SafetyViolation(
            f"Refusing {resource_kind} operation on unregistered ID {resource_id!r}. "
            "Only IDs created by this run may be modified or deleted."
        )
    return resource_id


def assert_safe_api_request(
    method: str,
    path: str,
    *,
    headers: dict[str, str],
    body: bytes | None,
    using_smoke_key: bool,
    post_refusal_mode: str | None = None,
) -> None:
    """Enforce Hard Safety Rule 3 before every HTTP call to TESSERA_API."""
    method_up = method.upper()
    if method_up == "GET":
        if not _STATUS_PATH_RE.match(path):
            raise SafetyViolation(
                f"GET path {path!r} refused: only read-only /v1/requests/<uuid> is permitted."
            )
        return

    if method_up == "POST":
        if path != "/v1/requests":
            raise SafetyViolation(f"POST path {path!r} refused.")
        if not using_smoke_key:
            raise SafetyViolation(
                "POST /v1/requests without TESSERA_SMOKE_KEY is forbidden by Rule 3."
            )
        if post_refusal_mode == "malformed_400":
            # POST /v1/requests accepts raw bytes, so a valid Tessera-Request-Key
            # UUID with small bytes WOULD BE ACCEPTED FOR ISSUANCE!
            # Enforce that Tessera-Request-Key is missing or provably non-UUID.
            req_key = None
            for k, v in headers.items():
                if k.lower() == "tessera-request-key":
                    req_key = v
                    break
            if req_key is not None:
                try:
                    uuid.UUID(req_key)
                except ValueError:
                    return  # Provably invalid UUID -> issuer must refuse 400.
                raise SafetyViolation(
                    "malformed_400 POST has a valid UUID Tessera-Request-Key; "
                    "because POST accepts raw bytes, this could be accepted for issuance!"
                )
            return

        if post_refusal_mode == "oversized_413":
            if body is None or len(body) <= ISSUER_MAX_BODY_BYTES:
                raise SafetyViolation(
                    f"oversized_413 POST body length {0 if body is None else len(body)} "
                    f"is not strictly greater than {ISSUER_MAX_BODY_BYTES} bytes!"
                )
            return

        raise SafetyViolation(
            f"POST refused: unknown or missing post_refusal_mode={post_refusal_mode!r}"
        )

    raise SafetyViolation(f"HTTP method {method_up!r} is forbidden by Rule 3.")


def assert_post_was_refused(status_code: int, context: str) -> None:
    """Fail closed immediately if any POST ever receives a 2xx acceptance (Rule 3)."""
    if 200 <= status_code < 300:
        raise SafetyViolation(
            f"CRITICAL RULE 3 BREACH PREVENTED ({context}): POST returned HTTP {status_code}! "
            "Aborting entire test run immediately."
        )


@dataclass
class RateLimiter:
    """Strict client-side pacer enforcing Rule 4 (always strictly below 5 rps, burst 20)."""

    rps: float
    _last_ts: float = field(default=0.0, init=False, repr=False)
    _clock: Any = field(default=time.monotonic, repr=False)
    _sleeper: Any = field(default=time.sleep, repr=False)

    def __post_init__(self) -> None:
        if self.rps <= 0 or self.rps > HARD_MAX_RPS:
            raise SafetyViolation(
                f"Requested rps={self.rps} violates hard safety range (0, {HARD_MAX_RPS}] "
                "(usage plan limit is 5 rps)."
            )

    @property
    def min_interval_s(self) -> float:
        return 1.0 / self.rps

    def wait(self) -> None:
        now = self._clock()
        if self._last_ts > 0:
            elapsed = now - self._last_ts
            remaining = self.min_interval_s - elapsed
            if remaining > 0:
                self._sleeper(remaining)
        self._last_ts = self._clock()


@dataclass
class SmokeTestQuotaTracker:
    """Tracks cumulative requests sent with TESSERA_SMOKE_KEY to guard the 100/day quota."""

    max_requests: int = 60
    count: int = 0

    def consume(self, n: int = 1) -> int:
        if self.count + n > self.max_requests:
            raise SafetyViolation(
                f"Smoke-test quota guard tripped: {self.count + n} > max_requests={self.max_requests}. "
                "Pass --include-quota-exhaustion only when intentionally running D4c last."
            )
        self.count += n
        return self.count


def sanitize_value(value: Any, secrets: Iterable[str] = ()) -> Any:
    """Recursively redact secrets, API URLs, and AWS key IDs (Rule 5)."""
    secret_list = [s for s in secrets if s]
    if isinstance(value, str):
        out = value
        for s in secret_list:
            out = out.replace(s, "[REDACTED]")
        out = _AWS_KEY_RE.sub("[REDACTED_AWS_KEY_ID]", out)
        return out
    if isinstance(value, dict):
        sanitized: dict[str, Any] = {}
        for k, v in value.items():
            kl = str(k).lower()
            if kl in ("secretaccesskey", "x-api-key", "apikeyvalue", "value") and isinstance(v, str):
                sanitized[k] = "[REDACTED]"
            else:
                sanitized[k] = sanitize_value(v, secret_list)
        return sanitized
    if isinstance(value, list):
        return [sanitize_value(item, secret_list) for item in value]
    return value


def locked_boto3_client(service_name: str, *, session: Any = None) -> Any:
    """Create a boto3 client strictly locked to us-east-2 (Rule 2)."""
    assert_env_region_safe()
    if session is None:
        import boto3  # Imported lazily so offline unit tests run without boto3.

        return boto3.client(service_name, region_name=ALLOWED_REGION)
    return session.client(service_name, region_name=ALLOWED_REGION)
