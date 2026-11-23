"""Observation helpers for SNS (via throwaway SQS), CloudWatch alarm history,
read-only access-log correlation, and exact CloudTrail event lookup.

Hard Safety Rule 1 & 5 compliance:
- Creates ONE throwaway SQS queue (tessera-dtest-<run_id>-obs-q) in us-east-2
  after verifying it does not already exist.
- Writes durable ledger intents BEFORE every create/subscribe call.
- Stores ONLY the queue name (never the SQS URL) in ledger entries and summaries.
- Re-verifies live tag ownership (purpose=detection-test AND run_id=<run_id>) and
  account/region/name BEFORE every SQS mutation, poll, unsubscribe, and delete.
- Subscribes that queue to tessera-v1-alarms (sole narrow exception in Rule 1)
  without touching the topic policy or any existing subscription.
- Before unsubscribing, verifies live subscription attributes (exact topic ARN,
  protocol='sqs', owned SQS endpoint for this run_id).
- Parses SNS messages into strictly allowlisted structured evidence (no raw
  excerpts or URLs stored).
"""

from __future__ import annotations

import json
import re
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Callable

from ledger import RunLedger, utc_now_iso
from safety import (
    ALLOWED_REGION,
    PRODUCTION_ACCESS_LOG_GROUP,
    PRODUCTION_ALARM_TOPIC_NAME,
    PURPOSE_TAG_KEY,
    PURPOSE_TAG_VALUE,
    RUN_ID_TAG_KEY,
    SMOKE_TEST_API_KEY_ID,
    SafetyViolation,
    TopicPolicyChangeRequired,
    assert_ownership_tags,
    assert_throwaway_id_registered,
    assert_throwaway_name,
    locked_boto3_client,
    make_throwaway_name,
    safe_error_label,
)

# Matches the exact EventBridge D7 input_template in service/detect/infra/main.tf:91,118.
_EB_D7_TEXT_RE = re.compile(
    r"Tessera D7 \(control-plane change\):\s*"
    r"(?P<event_name>[A-Za-z0-9_.-]+)\s+on\s+(?P<event_source>[A-Za-z0-9_.-]+)\s+"
    r"by\s+.+?\s+at\s+(?P<event_time>[0-9T:.+-]+Z?);\s*"
    r"error\s+(?P<error_code>[^;]*?);\s*"
    r"CloudTrail event\s+(?P<event_id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})",
    re.IGNORECASE,
)
_UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)
_TOKEN_RE = re.compile(r"^[A-Za-z0-9_.:/-]{1,128}$")


def _iso_from_epoch_ms(ms_str: str | None) -> str | None:
    if not ms_str:
        return None
    try:
        dt = datetime.fromtimestamp(int(ms_str) / 1000.0, tz=timezone.utc)
        return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    except (ValueError, TypeError):
        return None


def _parse_iso_utc(value: str | None) -> datetime | None:
    if not value or not isinstance(value, str):
        return None
    raw = value.strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(raw)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except ValueError:
        return None


def _clean_token(val: Any) -> str | None:
    if not isinstance(val, str):
        return None
    s = val.strip()
    if not s or "://" in s:
        return None
    if _TOKEN_RE.match(s):
        return s
    return None


def _error_code(exc: BaseException) -> str:
    resp = getattr(exc, "response", None)
    if isinstance(resp, dict):
        return str(resp.get("Error", {}).get("Code", ""))
    return ""


def find_alarm_topic_arn(
    sns_client: Any,
    account_id: str,
    topic_name: str = PRODUCTION_ALARM_TOPIC_NAME,
) -> str:
    """Read-only lookup of the production alarm topic ARN in us-east-2 and caller account."""
    expected = f"arn:aws:sns:{ALLOWED_REGION}:{account_id}:{topic_name}"
    paginator = sns_client.get_paginator("list_topics")
    for page in paginator.paginate():
        for t in page.get("Topics", []):
            if t.get("TopicArn") == expected:
                return expected
    raise RuntimeError(f"SNS topic {topic_name!r} not found in {ALLOWED_REGION}.")


def verify_owned_sqs_queue_live(
    sqs_client: Any,
    queue_name: str,
    run_id: str,
    account_id: str,
) -> str:
    """Resolve and verify live that an SQS queue is owned by this run_id and account."""
    assert_throwaway_name(queue_name, run_id=run_id)
    q_url = sqs_client.get_queue_url(
        QueueName=queue_name,
        QueueOwnerAWSAccountId=account_id,
    )["QueueUrl"]
    assert_throwaway_name(q_url, run_id=run_id, account_id=account_id)
    tags = sqs_client.list_queue_tags(QueueUrl=q_url).get("Tags", {})
    assert_ownership_tags(tags, run_id, f"sqs_queue:{queue_name}")
    return q_url


def verify_owned_observer_subscription_live(
    sns_client: Any,
    sqs_client: Any,
    subscription_arn: str,
    *,
    run_id: str,
    account_id: str,
    expected_topic_arn: str,
) -> dict[str, str]:
    """Re-verify live subscription attributes before calling sns:Unsubscribe."""
    if not subscription_arn or not subscription_arn.startswith(f"{expected_topic_arn}:"):
        raise SafetyViolation("SubscriptionArn does not belong to tessera-v1-alarms.")
    attrs = sns_client.get_subscription_attributes(
        SubscriptionArn=subscription_arn
    ).get("Attributes", {})
    if attrs.get("TopicArn") != expected_topic_arn:
        raise SafetyViolation("Live subscription TopicArn mismatch.")
    if attrs.get("Protocol") != "sqs":
        raise SafetyViolation("Refusing to unsubscribe non-SQS subscription (e.g. author email).")
    expected_queue_name = make_throwaway_name(run_id, "obs-q")
    expected_endpoint = f"arn:aws:sqs:{ALLOWED_REGION}:{account_id}:{expected_queue_name}"
    if attrs.get("Endpoint") != expected_endpoint:
        raise SafetyViolation("Live subscription Endpoint does not match this run's observer queue.")
    # If the queue still exists, verify its live ownership tags too.
    try:
        verify_owned_sqs_queue_live(sqs_client, expected_queue_name, run_id, account_id)
    except Exception as exc:
        if _error_code(exc) not in ("AWS.SimpleQueueService.NonExistentQueue", "QueueDoesNotExist"):
            raise
    return attrs


class AlarmObserver:
    """Manages the throwaway SQS subscription on tessera-v1-alarms and polls messages."""

    def __init__(
        self,
        run_id: str,
        ledger: RunLedger,
        account_id: str,
        *,
        session: Any = None,
    ) -> None:
        self.run_id = run_id
        self.ledger = ledger
        self.account_id = account_id
        self.sqs = locked_boto3_client("sqs", session=session)
        self.sns = locked_boto3_client("sns", session=session)
        self.queue_name = make_throwaway_name(run_id, "obs-q")
        self.queue_url: str | None = None
        self.queue_arn: str | None = None
        self.topic_arn: str | None = None
        self.subscription_arn: str | None = None
        self._queue_intent_id: str | None = None
        self._sub_intent_id: str | None = None
        self._owned_sub_arns: set[str] = set()
        self.subscribe_stimulus: dict[str, Any] | None = None
        self.unsubscribe_stimulus: dict[str, Any] | None = None

    def start(self) -> dict[str, Any]:
        """Create throwaway SQS queue (refusing pre-existing) and subscribe to tessera-v1-alarms."""
        assert_throwaway_name(self.queue_name, run_id=self.run_id)
        self.topic_arn = find_alarm_topic_arn(self.sns, self.account_id)

        # Refuse to adopt an existing queue with this run_id.
        try:
            self.sqs.get_queue_url(
                QueueName=self.queue_name,
                QueueOwnerAWSAccountId=self.account_id,
            )
        except Exception as exc:
            if _error_code(exc) not in ("AWS.SimpleQueueService.NonExistentQueue", "QueueDoesNotExist"):
                raise
        else:
            raise SafetyViolation(
                f"Observer queue {self.queue_name} already exists; refusing to adopt it."
            )

        # Write durable intent BEFORE create_queue.
        self._queue_intent_id = self.ledger.record_intent("sqs_observer_queue", self.queue_name)
        resp = self.sqs.create_queue(
            QueueName=self.queue_name,
            Attributes={
                "MessageRetentionPeriod": "86400",
                "ReceiveMessageWaitTimeSeconds": "10",
                "SqsManagedSseEnabled": "true",
            },
            tags={PURPOSE_TAG_KEY: PURPOSE_TAG_VALUE, RUN_ID_TAG_KEY: self.run_id},
        )
        self.queue_url = resp["QueueUrl"]
        assert_throwaway_name(self.queue_url, run_id=self.run_id, account_id=self.account_id)
        # Immediately confirm using queue_name (NEVER store SQS URL in ledger).
        self.ledger.confirm_created(self._queue_intent_id, self.queue_name)

        # Re-verify live tags before reading attributes or modifying queue policy.
        verify_owned_sqs_queue_live(self.sqs, self.queue_name, self.run_id, self.account_id)
        attrs = self.sqs.get_queue_attributes(
            QueueUrl=self.queue_url, AttributeNames=["QueueArn"]
        )["Attributes"]
        self.queue_arn = attrs["QueueArn"]
        assert_throwaway_name(self.queue_arn, run_id=self.run_id, account_id=self.account_id)

        # Verify no existing subscription on tessera-v1-alarms already targets this queue.
        paginator = self.sns.get_paginator("list_subscriptions_by_topic")
        for page in paginator.paginate(TopicArn=self.topic_arn):
            for sub in page.get("Subscriptions", []):
                if sub.get("Endpoint") == self.queue_arn:
                    raise SafetyViolation(
                        "An existing SNS subscription already targets this run's observer queue."
                    )

        # Policy on OUR throwaway SQS queue ONLY (never touches SNS topic policy).
        queue_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "AllowTesseraV1AlarmsPublish",
                    "Effect": "Allow",
                    "Principal": {"Service": "sns.amazonaws.com"},
                    "Action": "sqs:SendMessage",
                    "Resource": self.queue_arn,
                    "Condition": {"ArnEquals": {"aws:SourceArn": self.topic_arn}},
                }
            ],
        }
        verify_owned_sqs_queue_live(self.sqs, self.queue_name, self.run_id, self.account_id)
        self.sqs.set_queue_attributes(
            QueueUrl=self.queue_url,
            Attributes={"Policy": json.dumps(queue_policy)},
        )

        # Write durable intent BEFORE sns:Subscribe.
        self._sub_intent_id = self.ledger.record_intent(
            "sns_observer_subscription",
            f"{self.queue_name}->{PRODUCTION_ALARM_TOPIC_NAME}",
            metadata={"queue_name": self.queue_name, "topic_name": PRODUCTION_ALARM_TOPIC_NAME},
        )
        sub_started = utc_now_iso()
        try:
            sub_resp = self.sns.subscribe(
                TopicArn=self.topic_arn,
                Protocol="sqs",
                Endpoint=self.queue_arn,
                ReturnSubscriptionArn=True,
            )
        except Exception as exc:
            code = _error_code(exc)
            if code in ("AuthorizationError", "AccessDenied", "AuthorizationErrorException"):
                self.ledger.record_deleted(
                    "sns_observer_subscription",
                    self.queue_name,
                    status="not_created",
                    detail=safe_error_label(exc),
                    intent_id=self._sub_intent_id,
                    safe=True,
                )
                raise TopicPolicyChangeRequired(
                    "sns:Subscribe on tessera-v1-alarms was denied. Per Hard Safety Rule 1, "
                    "the test runner refuses to modify the topic policy; stopping and reporting."
                ) from exc
            raise

        self.subscription_arn = sub_resp["SubscriptionArn"]
        sub_ended = utc_now_iso()
        self._owned_sub_arns.add(self.subscription_arn)
        self.ledger.confirm_created(
            self._sub_intent_id,
            self.subscription_arn,
            metadata={"queue_name": self.queue_name, "topic_name": PRODUCTION_ALARM_TOPIC_NAME},
        )

        self.subscribe_stimulus = {
            "row_id": "D7-sns-sub-subscribe",
            "action": "sns:Subscribe (observer SQS queue on tessera-v1-alarms)",
            "kind": "d7_eventbridge",
            "resource_name": self.queue_name,
            "target_ids": [self.queue_arn, self.topic_arn, self.subscription_arn],
            "expected_event_names": ["Subscribe"],
            "expected_event_source": "sns.amazonaws.com",
            "started_at_utc": sub_started,
            "ended_at_utc": sub_ended,
            "api_call_succeeded": True,
            "contract_latency_s": 600,
            "sns_observable": True,
            "details": {
                "topic_name": PRODUCTION_ALARM_TOPIC_NAME,
                "queue_name": self.queue_name,
            },
        }
        self.ledger.record_event(
            ["D7-sns-sub-subscribe"],
            self.subscribe_stimulus["action"],
            resource_name=self.queue_name,
            started_at_utc=sub_started,
            ended_at_utc=sub_ended,
            details=self.subscribe_stimulus["details"],
        )
        return {
            "topic_name": PRODUCTION_ALARM_TOPIC_NAME,
            "queue_name": self.queue_name,
            "subscription_arn": self.subscription_arn,
            "stimulus": self.subscribe_stimulus,
        }

    def poll(
        self,
        duration_s: float = 600.0,
        *,
        stop_when: Callable[[list[dict[str, Any]]], bool] | None = None,
    ) -> list[dict[str, Any]]:
        """Drain SNS notifications from the verified throwaway SQS queue."""
        if not self.queue_url:
            return []
        verified_url = verify_owned_sqs_queue_live(
            self.sqs, self.queue_name, self.run_id, self.account_id
        )
        deadline = time.monotonic() + max(0.0, duration_s)
        collected: list[dict[str, Any]] = []
        while True:
            remaining = deadline - time.monotonic()
            wait_time = min(10, max(0, int(remaining)))
            resp = self.sqs.receive_message(
                QueueUrl=verified_url,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=wait_time,
                AttributeNames=["SentTimestamp"],
            )
            msgs = resp.get("Messages", [])
            for m in msgs:
                received_at = utc_now_iso()
                parsed = parse_sns_sqs_message(
                    body=m.get("Body", ""),
                    sent_timestamp_ms=m.get("Attributes", {}).get("SentTimestamp"),
                    received_at_utc=received_at,
                )
                collected.append(parsed)
                self.ledger.record_sns_message(parsed)
                verify_owned_sqs_queue_live(
                    self.sqs, self.queue_name, self.run_id, self.account_id
                )
                self.sqs.delete_message(
                    QueueUrl=verified_url, ReceiptHandle=m["ReceiptHandle"]
                )
            if stop_when is not None and stop_when(collected):
                break
            if time.monotonic() >= deadline:
                break
            if not msgs and remaining <= 0:
                break
        return collected

    def close(self) -> dict[str, Any] | None:
        """Re-verify live ownership, unsubscribe our subscription, and delete our SQS queue."""
        if self.subscription_arn and self.topic_arn:
            sub_arn = self.subscription_arn
            try:
                assert_throwaway_id_registered(
                    sub_arn, self._owned_sub_arns, "sns:Unsubscribe"
                )
                verify_owned_observer_subscription_live(
                    self.sns,
                    self.sqs,
                    sub_arn,
                    run_id=self.run_id,
                    account_id=self.account_id,
                    expected_topic_arn=self.topic_arn,
                )
                unsub_started = utc_now_iso()
                self.sns.unsubscribe(SubscriptionArn=sub_arn)
                unsub_ended = utc_now_iso()
                self.ledger.record_deleted(
                    "sns_observer_subscription",
                    sub_arn,
                    intent_id=self._sub_intent_id,
                    safe=True,
                )
                self.unsubscribe_stimulus = {
                    "row_id": "D7-sns-sub-unsubscribe",
                    "action": "sns:Unsubscribe (observer SQS queue from tessera-v1-alarms)",
                    "kind": "d7_eventbridge",
                    "resource_name": self.queue_name,
                    "target_ids": [sub_arn, self.topic_arn],
                    "expected_event_names": ["Unsubscribe"],
                    "expected_event_source": "sns.amazonaws.com",
                    "started_at_utc": unsub_started,
                    "ended_at_utc": unsub_ended,
                    "api_call_succeeded": True,
                    "contract_latency_s": 600,
                    "sns_observable": False,
                    "details": {
                        "topic_name": PRODUCTION_ALARM_TOPIC_NAME,
                        "queue_name": self.queue_name,
                        "observation_method": "steward_mailbox_email_only",
                    },
                }
                self.ledger.record_event(
                    ["D7-sns-sub-unsubscribe"],
                    self.unsubscribe_stimulus["action"],
                    resource_name=self.queue_name,
                    started_at_utc=unsub_started,
                    ended_at_utc=unsub_ended,
                    details=self.unsubscribe_stimulus["details"],
                    safe=True,
                )
            except Exception as exc:
                self.ledger.record_deleted(
                    "sns_observer_subscription",
                    sub_arn,
                    status="cleanup_failed",
                    detail=safe_error_label(exc),
                    intent_id=self._sub_intent_id,
                    safe=True,
                )
            finally:
                self.subscription_arn = None

        if self.queue_url or self._queue_intent_id:
            try:
                verified_url = verify_owned_sqs_queue_live(
                    self.sqs, self.queue_name, self.run_id, self.account_id
                )
                self.sqs.delete_queue(QueueUrl=verified_url)
                self.ledger.record_deleted(
                    "sqs_observer_queue",
                    self.queue_name,
                    intent_id=self._queue_intent_id,
                    safe=True,
                )
            except Exception as exc:
                if _error_code(exc) in ("AWS.SimpleQueueService.NonExistentQueue", "QueueDoesNotExist"):
                    self.ledger.record_deleted(
                        "sqs_observer_queue",
                        self.queue_name,
                        intent_id=self._queue_intent_id,
                        safe=True,
                    )
                else:
                    self.ledger.record_deleted(
                        "sqs_observer_queue",
                        self.queue_name,
                        status="cleanup_failed",
                        detail=safe_error_label(exc),
                        intent_id=self._queue_intent_id,
                        safe=True,
                    )
            finally:
                self.queue_url = None
        return self.unsubscribe_stimulus


def parse_sns_sqs_message(
    *,
    body: str,
    sent_timestamp_ms: str | None,
    received_at_utc: str,
) -> dict[str, Any]:
    """Parse an SNS-over-SQS envelope into allowlisted structured evidence ONLY.

    Never stores raw message excerpts or URLs (Rule 5).
    """
    record: dict[str, Any] = {
        "received_at_utc": received_at_utc,
        "sqs_sent_at_utc": _iso_from_epoch_ms(sent_timestamp_ms),
        "sns_message_id": None,
        "sns_timestamp_utc": None,
        "message_format": "unrecognized",
        "identifiers": {},
    }
    try:
        envelope = json.loads(body)
    except json.JSONDecodeError:
        return record
    if not isinstance(envelope, dict):
        return record

    record["sns_message_id"] = _clean_token(envelope.get("MessageId"))
    record["sns_timestamp_utc"] = _clean_token(envelope.get("Timestamp"))
    inner_raw = envelope.get("Message")
    if not isinstance(inner_raw, str):
        return record

    # 1. EventBridge D7 transformed plain-text sentence (service/detect/infra/main.tf:91,118)
    m = _EB_D7_TEXT_RE.search(inner_raw)
    if m:
        err_val = m.group("error_code").strip()
        record["message_format"] = "eventbridge_d7_text"
        record["identifiers"] = {
            "event_name": m.group("event_name"),
            "event_source": m.group("event_source"),
            "event_time": m.group("event_time"),
            "error_code": None if not err_val or err_val.lower() in ("null", "none", "") else _clean_token(err_val),
            "cloudtrail_event_id": m.group("event_id").lower(),
        }
        return record

    # 2. JSON inner payloads (CloudWatch Alarm, EventBridge raw, or Watcher finding)
    try:
        inner = json.loads(inner_raw)
    except json.JSONDecodeError:
        return record
    if not isinstance(inner, dict):
        return record

    identifiers: dict[str, Any] = {}
    if "AlarmName" in inner:
        record["message_format"] = "cloudwatch_alarm"
        for src_k, dst_k in (
            ("AlarmName", "alarm_name"),
            ("OldStateValue", "old_state"),
            ("NewStateValue", "new_state"),
            ("StateChangeTime", "state_change_time"),
        ):
            tok = _clean_token(inner.get(src_k))
            if tok is not None:
                identifiers[dst_k] = tok
        record["identifiers"] = identifiers
        return record

    detail = inner.get("detail")
    if isinstance(detail, dict) and "eventID" in detail:
        record["message_format"] = "eventbridge_raw"
        ev_id = detail.get("eventID")
        if isinstance(ev_id, str) and _UUID_RE.match(ev_id):
            identifiers["cloudtrail_event_id"] = ev_id.lower()
        for src_k, dst_k in (
            ("eventName", "event_name"),
            ("eventTime", "event_time"),
            ("eventSource", "event_source"),
            ("errorCode", "error_code"),
        ):
            tok = _clean_token(detail.get(src_k))
            if tok is not None:
                identifiers[dst_k] = tok
        record["identifiers"] = identifiers
        return record

    # Watcher finding JSON (service/watcher/tessera_watch/watcher.py)
    if any(k in inner for k in ("detection", "finding_id", "fid", "event_id", "eventID")):
        record["message_format"] = "watcher_finding"
        ev_id = inner.get("event_id") or inner.get("eventID")
        if isinstance(ev_id, str) and _UUID_RE.match(ev_id):
            identifiers["cloudtrail_event_id"] = ev_id.lower()
        for src_k, dst_k in (
            ("detection", "detection"),
            ("code", "code"),
            ("event_name", "event_name"),
            ("eventName", "event_name"),
            ("event_time", "event_time"),
            ("eventTime", "event_time"),
            ("finding_id", "finding_id"),
            ("fid", "finding_id"),
            ("region", "region"),
            ("error_code", "error_code"),
        ):
            if dst_k not in identifiers:
                tok = _clean_token(inner.get(src_k))
                if tok is not None:
                    identifiers[dst_k] = tok
        record["identifiers"] = identifiers
        return record

    return record


def _value_contains_target(obj: Any, targets: list[str]) -> str | None:
    """Recursively check parsed JSON structures for exact target identifier matches."""
    if isinstance(obj, str):
        for t in targets:
            if t and (obj == t or obj.endswith(f"/{t}") or obj.endswith(f":{t}")):
                return t
        return None
    if isinstance(obj, dict):
        for v in obj.values():
            found = _value_contains_target(v, targets)
            if found:
                return found
        return None
    if isinstance(obj, list):
        for item in obj:
            found = _value_contains_target(item, targets)
            if found:
                return found
        return None
    return None


def lookup_cloudtrail_events(
    *,
    event_names: list[str],
    start_utc: datetime,
    end_utc: datetime,
    target_ids: list[str],
    expected_event_source: str | None = None,
    session: Any = None,
) -> list[dict[str, Any]]:
    """Read-only paginated CloudTrail LookupEvents matching exact action, window, target, and outcome."""
    ct = locked_boto3_client("cloudtrail", session=session)
    window_start = start_utc - timedelta(seconds=10)
    window_end = end_utc + timedelta(seconds=30)
    targets = [t for t in target_ids if t]

    matches: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    paginator = ct.get_paginator("lookup_events")

    # Query per event name when exact; for Lambda versioned names, query without EventName filter
    # and match by prefix over the tight UTC window.
    is_lambda = expected_event_source == "lambda.amazonaws.com"
    queries: list[list[dict[str, str]]] = (
        [[{"AttributeKey": "EventSource", "AttributeValue": "lambda.amazonaws.com"}]]
        if is_lambda
        else [[{"AttributeKey": "EventName", "AttributeValue": en}] for en in event_names]
    )

    for attrs in queries:
        for page in paginator.paginate(
            LookupAttributes=attrs,
            StartTime=window_start,
            EndTime=window_end,
        ):
            for ev in page.get("Events", []):
                ev_id = ev.get("EventId")
                if not ev_id or ev_id in seen_ids:
                    continue
                raw_json = ev.get("CloudTrailEvent")
                if not isinstance(raw_json, str):
                    continue
                try:
                    parsed = json.loads(raw_json)
                except json.JSONDecodeError:
                    continue
                ev_name = str(parsed.get("eventName") or "")
                ev_src = str(parsed.get("eventSource") or "")
                if expected_event_source and ev_src != expected_event_source:
                    continue
                if is_lambda:
                    if not any(ev_name.startswith(p) for p in event_names):
                        continue
                else:
                    if ev_name not in event_names:
                        continue
                ev_time = _parse_iso_utc(parsed.get("eventTime"))
                if ev_time and not (window_start <= ev_time <= window_end):
                    continue

                matched_target = (
                    _value_contains_target(parsed.get("requestParameters"), targets)
                    or _value_contains_target(parsed.get("responseElements"), targets)
                    or _value_contains_target(parsed.get("resources"), targets)
                )
                if targets and not matched_target:
                    continue

                err_code = _clean_token(parsed.get("errorCode"))
                seen_ids.add(ev_id)
                matches.append(
                    {
                        "event_id": ev_id.lower(),
                        "event_name": ev_name,
                        "event_source": ev_src,
                        "event_time_utc": parsed.get("eventTime"),
                        "error_code": err_code,
                        "succeeded": err_code is None,
                        "matched_target": matched_target,
                    }
                )
    return matches


def describe_alarm_states(
    alarm_names: list[str],
    *,
    session: Any = None,
) -> dict[str, str]:
    """Read-only check of current CloudWatch alarm StateValue for named alarms."""
    if not alarm_names:
        return {}
    cw = locked_boto3_client("cloudwatch", session=session)
    states: dict[str, str] = {}
    resp = cw.describe_alarms(AlarmNames=alarm_names)
    for a in resp.get("MetricAlarms", []):
        states[a["AlarmName"]] = a.get("StateValue", "UNKNOWN")
    return states


def wait_for_alarms_ok(
    alarm_names: list[str],
    *,
    timeout_s: float = 900.0,
    poll_interval_s: float = 30.0,
    session: Any = None,
    sleeper: Any = time.sleep,
) -> dict[str, str]:
    """Require a verified OK baseline for target alarms before firing a threshold stimulus."""
    if not alarm_names:
        return {}
    deadline = time.monotonic() + max(0.0, timeout_s)
    while True:
        states = describe_alarm_states(alarm_names, session=session)
        missing = [n for n in alarm_names if n not in states]
        if missing:
            raise RuntimeError(f"Expected CloudWatch alarm(s) not found: {missing}")
        not_ok = {n: s for n, s in states.items() if s != "OK"}
        if not not_ok:
            return states
        if time.monotonic() >= deadline:
            raise RuntimeError(
                f"Alarms did not reach clean OK baseline within {timeout_s}s: {not_ok}"
            )
        sleeper(min(poll_interval_s, max(1.0, deadline - time.monotonic())))


def describe_recent_alarm_transitions(
    since_utc: datetime,
    *,
    alarm_names: list[str] | None = None,
    alarm_name_prefix: str = "tessera-v1-",
    session: Any = None,
) -> list[dict[str, Any]]:
    """Read-only poll of CloudWatch alarm history for StateUpdatedTimestamp correlation."""
    cw = locked_boto3_client("cloudwatch", session=session)
    if alarm_names is not None:
        names = list(alarm_names)
    else:
        names = []
        paginator = cw.get_paginator("describe_alarms")
        for page in paginator.paginate(AlarmNamePrefix=alarm_name_prefix):
            for a in page.get("MetricAlarms", []):
                names.append(a["AlarmName"])

    transitions: list[dict[str, Any]] = []
    for name in names:
        hist = cw.describe_alarm_history(
            AlarmName=name,
            HistoryItemType="StateUpdate",
            StartDate=since_utc,
            MaxRecords=20,
        )
        for item in hist.get("AlarmHistoryItems", []):
            ts = item.get("Timestamp")
            ts_iso = ts.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ") if ts else None
            data = {}
            try:
                data = json.loads(item.get("HistoryData", "{}"))
            except json.JSONDecodeError:
                pass
            transitions.append(
                {
                    "alarm_name": name,
                    "state_updated_timestamp": ts_iso,
                    "old_state": data.get("oldState", {}).get("stateValue"),
                    "new_state": data.get("newState", {}).get("stateValue"),
                }
            )
    return transitions


def correlate_access_logs(
    start_utc: datetime,
    end_utc: datetime,
    request_ids: list[str],
    *,
    log_group: str = PRODUCTION_ACCESS_LOG_GROUP,
    session: Any = None,
) -> list[dict[str, Any]]:
    """Read-only lookup in API Gateway access logs matching our exact x-amzn-requestid list."""
    if not request_ids:
        return []
    wanted = set(request_ids)
    logs = locked_boto3_client("logs", session=session)
    start_ms = int((start_utc - timedelta(seconds=15)).timestamp() * 1000)
    end_ms = int((end_utc + timedelta(seconds=120)).timestamp() * 1000)

    matched: list[dict[str, Any]] = []
    paginator = logs.get_paginator("filter_log_events")
    for page in paginator.paginate(
        logGroupName=log_group,
        startTime=start_ms,
        endTime=end_ms,
    ):
        for ev in page.get("events", []):
            try:
                line = json.loads(ev.get("message", "{}"))
            except json.JSONDecodeError:
                continue
            rid = line.get("requestId")
            if rid in wanted:
                matched.append(
                    {
                        "request_id": rid,
                        "time_ms": line.get("time"),
                        "api_key_id": _clean_token(line.get("apiKeyId")),
                        "method": _clean_token(line.get("method")),
                        "route": _clean_token(line.get("route")),
                        "status": _clean_token(str(line.get("status", ""))),
                        "error": _clean_token(line.get("error")),
                    }
                )
    return matched


def count_today_smoke_requests(
    *,
    smoke_key_id: str = SMOKE_TEST_API_KEY_ID,
    log_group: str = PRODUCTION_ACCESS_LOG_GROUP,
    session: Any = None,
) -> int:
    """Read-only count of today's UTC access-log entries for smoke-test (Rule 4 / Finding 8)."""
    now = datetime.now(timezone.utc)
    day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    logs = locked_boto3_client("logs", session=session)
    count = 0
    paginator = logs.get_paginator("filter_log_events")
    for page in paginator.paginate(
        logGroupName=log_group,
        startTime=int(day_start.timestamp() * 1000),
        endTime=int((now + timedelta(seconds=60)).timestamp() * 1000),
        filterPattern=f'{{ $.apiKeyId = "{smoke_key_id}" }}',
    ):
        count += len(page.get("events", []))
    return count
