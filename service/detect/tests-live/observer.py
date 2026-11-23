"""Read-only evidence helpers: CloudWatch alarm state and history, API Gateway
access-log correlation, and exact CloudTrail event lookup.

Steward removal pass (2026-11-23): the SQS observer subscription on the production
alarm topic, its teardown and recovery, and SNS message parsing are REMOVED. Nothing
in this suite subscribes to, unsubscribes from, or otherwise calls tessera-v1-alarms
or any of its subscriptions. Delivery evidence comes only from read-only
DescribeAlarmHistory and the steward's mailbox read.
"""

from __future__ import annotations

import json
import re
import time
from datetime import datetime, timedelta, timezone
from typing import Any

from safety import (
    PRODUCTION_ACCESS_LOG_GROUP,
    SMOKE_TEST_API_KEY_ID,
    locked_boto3_client,
)

_TOKEN_RE = re.compile(r"^[A-Za-z0-9_.:/-]{1,128}$")


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
