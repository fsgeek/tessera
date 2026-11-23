"""Observation helpers for SNS (via throwaway SQS), CloudWatch alarm history,
and CloudTrail EventId lookup.

Hard Safety Rule 1 compliance:
- Creates ONE throwaway SQS queue (tessera-dtest-<run_id>-obs-q) in us-east-2.
- Attaches a queue policy ONLY on the throwaway SQS queue.
- Subscribes that queue to tessera-v1-alarms (the sole narrow exception in Rule 1)
  without touching the topic policy or any existing subscription.
- If sns:Subscribe fails with AuthorizationError/AccessDenied, stops immediately
  with TopicPolicyChangeRequired rather than modifying the topic policy.
- Always unsubscribes ONLY the SubscriptionArn we created and deletes the queue
  in close() (called from a finally block).
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timedelta, timezone
from typing import Any

from ledger import RunLedger, utc_now_iso
from safety import (
    PURPOSE_TAG_KEY,
    PURPOSE_TAG_VALUE,
    PRODUCTION_ALARM_TOPIC_NAME,
    SafetyViolation,
    TopicPolicyChangeRequired,
    assert_throwaway_id_registered,
    assert_throwaway_name,
    locked_boto3_client,
    make_throwaway_name,
)


def _iso_from_epoch_ms(ms_str: str | None) -> str | None:
    if not ms_str:
        return None
    try:
        dt = datetime.fromtimestamp(int(ms_str) / 1000.0, tz=timezone.utc)
        return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    except (ValueError, TypeError):
        return None


def find_alarm_topic_arn(sns_client: Any, topic_name: str = PRODUCTION_ALARM_TOPIC_NAME) -> str:
    """Read-only lookup of the production alarm topic ARN by name."""
    suffix = f":{topic_name}"
    paginator = sns_client.get_paginator("list_topics")
    for page in paginator.paginate():
        for t in page.get("Topics", []):
            arn = t["TopicArn"]
            if arn.endswith(suffix):
                return arn
    raise RuntimeError(f"SNS topic ending with {suffix!r} not found in us-east-2.")


class AlarmObserver:
    """Manages the throwaway SQS subscription on tessera-v1-alarms and polls messages."""

    def __init__(self, run_id: str, ledger: RunLedger, *, session: Any = None) -> None:
        self.run_id = run_id
        self.ledger = ledger
        self.sqs = locked_boto3_client("sqs", session=session)
        self.sns = locked_boto3_client("sns", session=session)
        self.queue_name = make_throwaway_name(run_id, "obs-q")
        self.queue_url: str | None = None
        self.queue_arn: str | None = None
        self.topic_arn: str | None = None
        self.subscription_arn: str | None = None
        self._owned_sub_arns: set[str] = set()

    def start(self) -> dict[str, str]:
        """Create throwaway SQS queue and subscribe it to tessera-v1-alarms."""
        assert_throwaway_name(self.queue_name)
        self.topic_arn = find_alarm_topic_arn(self.sns)

        resp = self.sqs.create_queue(
            QueueName=self.queue_name,
            Attributes={
                "MessageRetentionPeriod": "86400",
                "ReceiveMessageWaitTimeSeconds": "10",
                # SSE-SQS default requires no KMS key policy change on the SNS topic.
                "SqsManagedSseEnabled": "true",
            },
            tags={PURPOSE_TAG_KEY: PURPOSE_TAG_VALUE, "run_id": self.run_id},
        )
        self.queue_url = resp["QueueUrl"]
        assert_throwaway_name(self.queue_url)
        attrs = self.sqs.get_queue_attributes(
            QueueUrl=self.queue_url, AttributeNames=["QueueArn"]
        )["Attributes"]
        self.queue_arn = attrs["QueueArn"]
        assert_throwaway_name(self.queue_arn)
        self.ledger.record_created(
            "sqs_observer_queue",
            self.queue_url,
            self.queue_name,
            metadata={"queue_arn": self.queue_arn},
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
        self.sqs.set_queue_attributes(
            QueueUrl=self.queue_url,
            Attributes={"Policy": json.dumps(queue_policy)},
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
            code = getattr(exc, "response", {}).get("Error", {}).get("Code", "")
            if code in ("AuthorizationError", "AccessDenied", "AuthorizationErrorException"):
                raise TopicPolicyChangeRequired(
                    "sns:Subscribe on tessera-v1-alarms was denied. Per Hard Safety Rule 1, "
                    "the test runner refuses to modify the topic policy; stopping and reporting."
                ) from exc
            raise

        self.subscription_arn = sub_resp["SubscriptionArn"]
        sub_ended = utc_now_iso()
        self._owned_sub_arns.add(self.subscription_arn)
        self.ledger.record_created(
            "sns_observer_subscription",
            self.subscription_arn,
            f"{self.queue_name}->tessera-v1-alarms",
            metadata={"topic_arn": self.topic_arn, "queue_arn": self.queue_arn},
        )
        # Subscribing to tessera-v1-alarms is itself a PRODUCTION PATH D7-sns-sub event!
        self.ledger.record_event(
            ["D7-sns-sub"],
            "sns:Subscribe (observer SQS queue on tessera-v1-alarms)",
            resource_name=self.queue_name,
            started_at_utc=sub_started,
            ended_at_utc=sub_ended,
            details={
                "topic_arn": self.topic_arn,
                "subscription_arn": self.subscription_arn,
                "queue_arn": self.queue_arn,
                "note": "Narrow Rule 1 exception; exercises production alarm topic directly.",
            },
        )
        return {
            "topic_arn": self.topic_arn,
            "queue_url": self.queue_url,
            "queue_arn": self.queue_arn,
            "subscription_arn": self.subscription_arn,
        }

    def poll(self, duration_s: float = 30.0) -> list[dict[str, Any]]:
        """Drain SNS notifications delivered to the throwaway SQS queue."""
        if not self.queue_url:
            return []
        deadline = time.monotonic() + max(0.0, duration_s)
        collected: list[dict[str, Any]] = []
        while True:
            remaining = deadline - time.monotonic()
            wait_time = min(10, max(0, int(remaining)))
            resp = self.sqs.receive_message(
                QueueUrl=self.queue_url,
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
                self.sqs.delete_message(
                    QueueUrl=self.queue_url, ReceiptHandle=m["ReceiptHandle"]
                )
            if time.monotonic() >= deadline:
                break
            if not msgs and remaining <= 0:
                break
        return collected

    def close(self) -> None:
        """Always unsubscribe ONLY our subscription and delete our throwaway SQS queue."""
        if self.subscription_arn:
            try:
                assert_throwaway_id_registered(
                    self.subscription_arn,
                    self._owned_sub_arns,
                    "sns:Unsubscribe",
                )
                unsub_started = utc_now_iso()
                self.sns.unsubscribe(SubscriptionArn=self.subscription_arn)
                unsub_ended = utc_now_iso()
                self.ledger.record_deleted("sns_observer_subscription", self.subscription_arn)
                self.ledger.record_event(
                    ["D7-sns-sub"],
                    "sns:Unsubscribe (observer SQS queue from tessera-v1-alarms)",
                    resource_name=self.queue_name,
                    started_at_utc=unsub_started,
                    ended_at_utc=unsub_ended,
                    details={
                        "topic_arn": self.topic_arn,
                        "subscription_arn": self.subscription_arn,
                        "note": "Check author mailbox for Unsubscribe D7 notification.",
                    },
                )
            except Exception as exc:
                self.ledger.record_deleted(
                    "sns_observer_subscription",
                    self.subscription_arn,
                    status="cleanup_failed",
                    detail=str(exc),
                )
            finally:
                self.subscription_arn = None

        if self.queue_url:
            try:
                assert_throwaway_name(self.queue_url)
                self.sqs.delete_queue(QueueUrl=self.queue_url)
                self.ledger.record_deleted("sqs_observer_queue", self.queue_url)
            except Exception as exc:
                self.ledger.record_deleted(
                    "sqs_observer_queue",
                    self.queue_url,
                    status="cleanup_failed",
                    detail=str(exc),
                )
            finally:
                self.queue_url = None


def parse_sns_sqs_message(
    *,
    body: str,
    sent_timestamp_ms: str | None,
    received_at_utc: str,
) -> dict[str, Any]:
    """Parse an SNS-over-SQS envelope and extract correlating identifiers."""
    record: dict[str, Any] = {
        "received_at_utc": received_at_utc,
        "sqs_sent_at_utc": _iso_from_epoch_ms(sent_timestamp_ms),
        "sns_message_id": None,
        "sns_timestamp_utc": None,
        "subject": None,
        "identifiers": {},
        "raw_message_excerpt": None,
    }
    try:
        envelope = json.loads(body)
    except json.JSONDecodeError:
        record["raw_message_excerpt"] = body[:1000]
        return record

    record["sns_message_id"] = envelope.get("MessageId")
    record["sns_timestamp_utc"] = envelope.get("Timestamp")
    record["subject"] = envelope.get("Subject")
    inner_raw = envelope.get("Message", "")
    record["raw_message_excerpt"] = inner_raw[:1500] if isinstance(inner_raw, str) else str(inner_raw)[:1500]

    identifiers: dict[str, Any] = {}
    if isinstance(inner_raw, str):
        try:
            inner = json.loads(inner_raw)
        except json.JSONDecodeError:
            inner = None
        if isinstance(inner, dict):
            # CloudWatch Alarm notification format
            if "AlarmName" in inner:
                identifiers["alarm_name"] = inner.get("AlarmName")
                identifiers["new_state"] = inner.get("NewStateValue")
                identifiers["state_change_time"] = inner.get("StateChangeTime")
            # EventBridge raw CloudTrail event format
            detail = inner.get("detail")
            if isinstance(detail, dict):
                if "eventID" in detail:
                    identifiers["cloudtrail_event_id"] = detail.get("eventID")
                if "eventName" in detail:
                    identifiers["event_name"] = detail.get("eventName")
                if "eventTime" in detail:
                    identifiers["event_time"] = detail.get("eventTime")
                if "eventSource" in detail:
                    identifiers["event_source"] = detail.get("eventSource")
            # Flat/transformed EventBridge or Watcher JSON payload
            for key in (
                "eventID",
                "event_id",
                "eventName",
                "event_name",
                "eventTime",
                "event_time",
                "finding_id",
                "kind",
                "resource",
                "role_name",
                "user_name",
            ):
                if key in inner and key not in identifiers:
                    identifiers[key] = inner[key]
    record["identifiers"] = identifiers
    return record


def lookup_cloudtrail_event_id(
    event_name: str,
    start_time: datetime,
    *,
    resource_substring: str | None = None,
    session: Any = None,
) -> str | None:
    """Read-only CloudTrail LookupEvents to record the exact eventID for correlation."""
    ct = locked_boto3_client("cloudtrail", session=session)
    end_time = datetime.now(timezone.utc) + timedelta(minutes=1)
    resp = ct.lookup_events(
        LookupAttributes=[{"AttributeKey": "EventName", "AttributeValue": event_name}],
        StartTime=start_time - timedelta(seconds=30),
        EndTime=end_time,
        MaxResults=25,
    )
    for ev in resp.get("Events", []):
        raw = ev.get("CloudTrailEvent", "")
        if resource_substring and resource_substring not in raw:
            continue
        return ev.get("EventId")
    return None


def describe_recent_alarm_transitions(
    since_utc: datetime,
    *,
    alarm_name_prefix: str = "tessera-v1-",
    session: Any = None,
) -> list[dict[str, Any]]:
    """Read-only poll of CloudWatch alarm history for StateUpdatedTimestamp correlation."""
    cw = locked_boto3_client("cloudwatch", session=session)
    alarms: list[str] = []
    paginator = cw.get_paginator("describe_alarms")
    for page in paginator.paginate(AlarmNamePrefix=alarm_name_prefix):
        for a in page.get("MetricAlarms", []):
            alarms.append(a["AlarmName"])

    transitions: list[dict[str, Any]] = []
    for name in alarms:
        hist = cw.describe_alarm_history(
            AlarmName=name,
            HistoryItemType="StateUpdate",
            StartDate=since_utc,
            MaxRecords=10,
        )
        for item in hist.get("AlarmHistoryItems", []):
            ts = item.get("Timestamp")
            ts_iso = ts.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ") if ts else None
            data = {}
            try:
                data = json.loads(item.get("HistoryData", "{}"))
            except json.JSONDecodeError:
                pass
            new_state = data.get("newState", {}).get("stateValue")
            old_state = data.get("oldState", {}).get("stateValue")
            transitions.append(
                {
                    "alarm_name": name,
                    "state_updated_timestamp": ts_iso,
                    "old_state": old_state,
                    "new_state": new_state,
                    "summary": item.get("HistorySummary"),
                }
            )
    return transitions
