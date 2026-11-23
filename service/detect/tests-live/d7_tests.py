"""D7 control-plane tampering tests on throwaway resources, and tag-only crash recovery.

Steward removal pass (2026-11-23):
- REMOVED: every call to the production alarm topic or its subscriptions; all IAM
  mutations (throwaway roles, inline policies, users, access keys); S3 bucket and
  CloudTrail tests (a bucket exists untagged between CreateBucket and PutBucketTagging,
  so tag search cannot find it after a lost reply); the throwaway Lambda (needs an IAM
  role); KMS alias and grant, API Gateway REST API and usage-plan key, and the
  throwaway-topic subscription (none is taggable, so none can be found by tag search).
- Every remaining resource is tagged in its create call (purpose=detection-test and
  run_id=<run_id>) and is a type the Resource Groups Tagging API indexes in us-east-2.
- A durable intent is flushed BEFORE each create. A create that fails with a definite
  client (4xx) error closes as not_created; any other failure leaves the intent
  'unresolved', which counts as a residual until recovery finds it by tag search.
- Recovery discovers ONLY by live tag search (both tags) in us-east-2, re-verifies
  ownership on the service itself before deleting, never closes an intent on a search
  miss, and reports residuals so the CLI exits non-zero.
- Ledger identifiers are resource names or opaque IDs (KMS key ID, API Gateway ID),
  never ARNs or URLs.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from ledger import RunLedger, load_ledger, save_ledger_dict, utc_now_iso
from safety import (
    ALLOWED_REGION,
    PURPOSE_TAG_KEY,
    PURPOSE_TAG_VALUE,
    RUN_ID_TAG_KEY,
    SafetyViolation,
    assert_ownership_tags,
    assert_throwaway_name,
    locked_boto3_client,
    make_throwaway_name,
    safe_error_label,
    validate_run_id,
)

RESOURCE_TYPES = (
    "kms_key",
    "sns_topic",
    "apigw_api_key",
    "apigw_usage_plan",
    "sqs_queue",
    "dynamodb_table",
    "cloudwatch_alarm",
    "log_group",
    "eventbridge_rule",
)

_NOT_FOUND_CODES = frozenset(
    {
        "NotFoundException",
        "ResourceNotFoundException",
        "NotFound",
        "AWS.SimpleQueueService.NonExistentQueue",
        "QueueDoesNotExist",
    }
)


def _error_code(exc: BaseException) -> str:
    resp = getattr(exc, "response", None)
    if isinstance(resp, dict):
        return str(resp.get("Error", {}).get("Code", ""))
    return ""


def _http_status(exc: BaseException) -> int | None:
    resp = getattr(exc, "response", None)
    if isinstance(resp, dict):
        code = resp.get("ResponseMetadata", {}).get("HTTPStatusCode")
        if isinstance(code, int):
            return code
    return None


def _is_not_found(exc: BaseException) -> bool:
    return _error_code(exc) in _NOT_FOUND_CODES


def _definitely_not_created(exc: BaseException) -> bool:
    """True only for an AWS client error with a 4xx status: the create was rejected."""
    status = _http_status(exc)
    return status is not None and 400 <= status < 500


def _http_ok(resp: Any) -> bool:
    if not isinstance(resp, dict):
        return True
    meta = resp.get("ResponseMetadata")
    if not isinstance(meta, dict):
        return True
    code = meta.get("HTTPStatusCode")
    return code is None or (200 <= int(code) < 300)


def _tags(run_id: str) -> list[dict[str, str]]:
    return [
        {"Key": PURPOSE_TAG_KEY, "Value": PURPOSE_TAG_VALUE},
        {"Key": RUN_ID_TAG_KEY, "Value": run_id},
    ]


def _tags_map(run_id: str) -> dict[str, str]:
    return {PURPOSE_TAG_KEY: PURPOSE_TAG_VALUE, RUN_ID_TAG_KEY: run_id}


def get_caller_identity(session: Any = None) -> tuple[str, str]:
    """Return (account_id, caller_arn) from regional us-east-2 STS."""
    sts = locked_boto3_client("sts", session=session)
    ident = sts.get_caller_identity()
    return str(ident["Account"]), str(ident["Arn"])


def _tags_list_to_dict(
    tags_list: list[dict[str, Any]] | None, key_field: str = "Key", val_field: str = "Value"
) -> dict[str, str]:
    out: dict[str, str] = {}
    for item in tags_list or []:
        k = item.get(key_field)
        v = item.get(val_field)
        if isinstance(k, str) and isinstance(v, str):
            out[k] = v
    return out


def _sns_topic_arn(account_id: str, name: str) -> str:
    return f"arn:aws:sns:{ALLOWED_REGION}:{account_id}:{name}"


# ---------------------------------------------------------------------------
# Live ownership verifiers (service-side tags + name + run_id + account + region)
# ---------------------------------------------------------------------------

def _verify_kms_key_owned(kms: Any, key_id: str, run_id: str, account_id: str) -> dict[str, Any]:
    meta = kms.describe_key(KeyId=key_id)["KeyMetadata"]
    if str(meta.get("AWSAccountId")) != account_id:
        raise SafetyViolation("KMS key account mismatch.")
    arn = str(meta.get("Arn") or "")
    if not arn.startswith(f"arn:aws:kms:{ALLOWED_REGION}:{account_id}:key/"):
        raise SafetyViolation("KMS key ARN outside pinned region/account.")
    desc = str(meta.get("Description") or "")
    if not desc.startswith(f"tessera-dtest-{run_id}-") or "tessera-v1" in desc.lower():
        raise SafetyViolation("KMS key description does not match this run_id throwaway prefix.")
    tags = _tags_list_to_dict(kms.list_resource_tags(KeyId=meta["KeyId"]).get("Tags"), "TagKey", "TagValue")
    assert_ownership_tags(tags, run_id, "kms_key")
    return meta


def _verify_sns_topic_owned(sns: Any, topic_name: str, run_id: str, account_id: str) -> str:
    assert_throwaway_name(topic_name, run_id=run_id)
    arn = _sns_topic_arn(account_id, topic_name)
    tags = _tags_list_to_dict(sns.list_tags_for_resource(ResourceArn=arn).get("Tags"))
    assert_ownership_tags(tags, run_id, "sns_topic")
    return arn


def _verify_apigw_api_key_owned(apigw: Any, key_id: str, run_id: str) -> dict[str, Any]:
    key = apigw.get_api_key(apiKey=key_id, includeValue=False)
    assert_throwaway_name(str(key.get("name") or ""), run_id=run_id)
    assert_ownership_tags(key.get("tags"), run_id, "apigw_api_key")
    return key


def _verify_apigw_usage_plan_owned(apigw: Any, plan_id: str, run_id: str) -> dict[str, Any]:
    plan = apigw.get_usage_plan(usagePlanId=plan_id)
    assert_throwaway_name(str(plan.get("name") or ""), run_id=run_id)
    assert_ownership_tags(plan.get("tags"), run_id, "apigw_usage_plan")
    if plan.get("apiStages"):
        raise SafetyViolation("Throwaway usage plan unexpectedly has API stages attached.")
    return plan


def verify_owned_sqs_queue_live(sqs: Any, queue_name: str, run_id: str, account_id: str) -> str:
    """Resolve and verify live that an SQS queue is owned by this run_id and account."""
    assert_throwaway_name(queue_name, run_id=run_id)
    q_url = sqs.get_queue_url(QueueName=queue_name, QueueOwnerAWSAccountId=account_id)["QueueUrl"]
    assert_throwaway_name(q_url, run_id=run_id, account_id=account_id)
    tags = sqs.list_queue_tags(QueueUrl=q_url).get("Tags", {})
    assert_ownership_tags(tags, run_id, "sqs_queue")
    return q_url


def _verify_ddb_owned(ddb: Any, tbl_name: str, run_id: str, account_id: str) -> dict[str, Any]:
    assert_throwaway_name(tbl_name, run_id=run_id)
    tbl = ddb.describe_table(TableName=tbl_name)["Table"]
    arn = str(tbl.get("TableArn") or "")
    assert_throwaway_name(arn, run_id=run_id, account_id=account_id)
    tags = _tags_list_to_dict(ddb.list_tags_of_resource(ResourceArn=arn).get("Tags"))
    assert_ownership_tags(tags, run_id, "dynamodb_table")
    return tbl


def _verify_cw_alarm_owned(cw: Any, alarm_name: str, run_id: str, account_id: str) -> dict[str, Any] | None:
    assert_throwaway_name(alarm_name, run_id=run_id)
    alarms = cw.describe_alarms(AlarmNames=[alarm_name]).get("MetricAlarms", [])
    matched = [a for a in alarms if a.get("AlarmName") == alarm_name]
    if not matched:
        return None
    arn = str(matched[0].get("AlarmArn") or "")
    assert_throwaway_name(arn, run_id=run_id, account_id=account_id)
    tags = _tags_list_to_dict(cw.list_tags_for_resource(ResourceARN=arn).get("Tags"))
    assert_ownership_tags(tags, run_id, "cloudwatch_alarm")
    if matched[0].get("AlarmActions") or matched[0].get("OKActions") or matched[0].get("InsufficientDataActions"):
        raise SafetyViolation("Throwaway alarm unexpectedly has actions.")
    return matched[0]


def _verify_log_group_owned(logs: Any, group_name: str, run_id: str, account_id: str) -> dict[str, Any] | None:
    assert_throwaway_name(group_name, run_id=run_id)
    groups = logs.describe_log_groups(logGroupNamePrefix=group_name).get("logGroups", [])
    matched = [g for g in groups if g.get("logGroupName") == group_name]
    if not matched:
        return None
    arn = str(matched[0].get("arn") or "")
    if arn.endswith(":*"):
        arn = arn[:-2]
    assert_throwaway_name(arn, run_id=run_id, account_id=account_id)
    tags = logs.list_tags_for_resource(resourceArn=arn).get("tags", {})
    assert_ownership_tags(tags, run_id, "log_group")
    return matched[0]


def _verify_eb_rule_owned(eb: Any, rule_name: str, run_id: str, account_id: str) -> dict[str, Any]:
    assert_throwaway_name(rule_name, run_id=run_id)
    rule = eb.describe_rule(Name=rule_name)
    arn = str(rule.get("Arn") or "")
    assert_throwaway_name(arn, run_id=run_id, account_id=account_id)
    tags = _tags_list_to_dict(eb.list_tags_for_resource(ResourceARN=arn).get("Tags"))
    assert_ownership_tags(tags, run_id, "eventbridge_rule")
    return rule


# ---------------------------------------------------------------------------
# Tag-only live discovery (us-east-2, purpose AND run_id)
# ---------------------------------------------------------------------------

def _classify_tagged_arn(arn: str, run_id: str, account_id: str) -> dict[str, str]:
    """Map one tag-search ARN to (resource_type, identifier, name). Unknown -> 'unknown'."""
    prefix = f"tessera-dtest-{run_id}-"
    parts = arn.split(":", 5)
    unknown = {"resource_type": "unknown", "identifier": "", "name": "unrecognized-tagged-resource"}
    if len(parts) < 6 or parts[0] != "arn" or parts[1] != "aws" or parts[3] != ALLOWED_REGION:
        return unknown
    service, acct, resource = parts[2], parts[4], parts[5]
    if service == "apigateway":
        if acct:
            return unknown
        for marker, rtype in (("/apikeys/", "apigw_api_key"), ("/usageplans/", "apigw_usage_plan")):
            if resource.startswith(marker):
                rid = resource[len(marker):]
                if rid and "/" not in rid:
                    return {"resource_type": rtype, "identifier": rid, "name": rid}
        return unknown
    if acct != account_id:
        return unknown
    if service == "kms" and resource.startswith("key/"):
        key_id = resource[len("key/"):]
        return {"resource_type": "kms_key", "identifier": key_id, "name": f"{prefix}kms"}
    named = {
        "sns": ("sns_topic", ""),
        "sqs": ("sqs_queue", ""),
        "dynamodb": ("dynamodb_table", "table/"),
        "cloudwatch": ("cloudwatch_alarm", "alarm:"),
        "logs": ("log_group", "log-group:"),
        "events": ("eventbridge_rule", "rule/"),
    }
    if service in named:
        rtype, marker = named[service]
        if not resource.startswith(marker):
            return unknown
        name = resource[len(marker):]
        if name.endswith(":*"):
            name = name[:-2]
        if not name.startswith(prefix):
            return unknown
        return {"resource_type": rtype, "identifier": name, "name": name}
    return unknown


def discover_live_run_resources(run_id: str, account_id: str, *, session: Any = None) -> list[dict[str, str]]:
    """Find live resources carrying BOTH tags for run_id via the us-east-2 tagging API only."""
    validate_run_id(run_id)
    tag_api = locked_boto3_client("resourcegroupstaggingapi", session=session)
    found: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for page in tag_api.get_paginator("get_resources").paginate(
        TagFilters=[
            {"Key": PURPOSE_TAG_KEY, "Values": [PURPOSE_TAG_VALUE]},
            {"Key": RUN_ID_TAG_KEY, "Values": [run_id]},
        ]
    ):
        for item in page.get("ResourceTagMappingList", []):
            entry = _classify_tagged_arn(str(item.get("ResourceARN") or ""), run_id, account_id)
            key = (entry["resource_type"], entry["identifier"])
            if key not in seen:
                seen.add(key)
                found.append(entry)
    return found


def assert_no_existing_run_resources(run_id: str, account_id: str, *, session: Any = None) -> None:
    """Refuse to start if any resource tagged with this run_id already exists."""
    existing = discover_live_run_resources(run_id, account_id, session=session)
    if existing:
        raise SafetyViolation(
            f"Refusing to start: {len(existing)} tagged resource(s) already present for this run_id."
        )


# ---------------------------------------------------------------------------
# Shared create/cleanup helpers
# ---------------------------------------------------------------------------

def _create_failed(ledger: RunLedger, rtype: str, name: str, intent_id: str, exc: BaseException) -> None:
    status = "not_created" if _definitely_not_created(exc) else "unresolved"
    ledger.record_deleted(rtype, name, status=status, detail=safe_error_label(exc), intent_id=intent_id, safe=True)


def _cleanup(ledger: RunLedger, rtype: str, name: str, intent_id: str, fn: Any) -> None:
    try:
        status, detail = fn()
        ledger.record_deleted(rtype, name, status=status, detail=detail, intent_id=intent_id, safe=True)
    except Exception as exc:
        ledger.record_deleted(rtype, name, status="cleanup_failed", detail=safe_error_label(exc), intent_id=intent_id, safe=True)


def _stim(
    row_id: str,
    action: str,
    *,
    resource_name: str,
    target_ids: list[str],
    expected_event_names: list[str],
    expected_event_source: str,
    started_at_utc: str,
    ended_at_utc: str,
    api_call_succeeded: bool,
    contract_latency_s: int = 600,
) -> dict[str, Any]:
    return {
        "row_id": row_id,
        "action": action,
        "kind": "d7_eventbridge",
        "resource_name": resource_name,
        "target_ids": [t for t in target_ids if t],
        "expected_event_names": expected_event_names,
        "expected_event_source": expected_event_source,
        "started_at_utc": started_at_utc,
        "ended_at_utc": ended_at_utc,
        "api_call_succeeded": api_call_succeeded,
        "contract_latency_s": contract_latency_s,
    }


def _timed(call: Any) -> tuple[str, Any, str]:
    t0 = utc_now_iso()
    r = call()
    return t0, r, utc_now_iso()


# ---------------------------------------------------------------------------
# D7 tests
# ---------------------------------------------------------------------------

def run_d7_kms(run_id: str, ledger: RunLedger, *, session: Any = None) -> list[dict[str, Any]]:
    """D7-kms-policy, D7-kms-disable, D7-kms-delete on a throwaway key tagged at creation."""
    kms = locked_boto3_client("kms", session=session)
    account_id = str(ledger.account_id)
    name = make_throwaway_name(run_id, "kms")
    results: list[dict[str, Any]] = []
    key_id: str | None = None
    scheduled = False

    intent = ledger.record_intent("kms_key", name)
    try:
        resp = kms.create_key(
            Description=f"{name} (throwaway detection test)",
            KeyUsage="ENCRYPT_DECRYPT",
            KeySpec="SYMMETRIC_DEFAULT",
            Tags=[{"TagKey": t["Key"], "TagValue": t["Value"]} for t in _tags(run_id)],
        )
    except Exception as exc:
        _create_failed(ledger, "kms_key", name, intent, exc)
        raise
    key_id = str(resp["KeyMetadata"]["KeyId"])
    ledger.confirm_created(intent, key_id)

    try:
        _verify_kms_key_owned(kms, key_id, run_id, account_id)
        policy = {
            "Version": "2012-10-17",
            "Id": name,
            "Statement": [
                {
                    "Sid": "TesseraDtestRootAdmin",
                    "Effect": "Allow",
                    "Principal": {"AWS": f"arn:aws:iam::{account_id}:root"},
                    "Action": "kms:*",
                    "Resource": "*",
                }
            ],
        }
        t, r, e = _timed(lambda: kms.put_key_policy(KeyId=key_id, PolicyName="default", Policy=json.dumps(policy)))
        results.append(_stim("D7-kms-policy", "kms:PutKeyPolicy", resource_name=name, target_ids=[key_id],
                             expected_event_names=["PutKeyPolicy"], expected_event_source="kms.amazonaws.com",
                             started_at_utc=t, ended_at_utc=e, api_call_succeeded=_http_ok(r)))
        ledger.record_event(["D7-kms-policy"], "kms:PutKeyPolicy", resource_name=name, started_at_utc=t, ended_at_utc=e)

        _verify_kms_key_owned(kms, key_id, run_id, account_id)
        t, r, e = _timed(lambda: kms.disable_key(KeyId=key_id))
        results.append(_stim("D7-kms-disable", "kms:DisableKey", resource_name=name, target_ids=[key_id],
                             expected_event_names=["DisableKey"], expected_event_source="kms.amazonaws.com",
                             started_at_utc=t, ended_at_utc=e, api_call_succeeded=_http_ok(r)))
        ledger.record_event(["D7-kms-disable"], "kms:DisableKey", resource_name=name, started_at_utc=t, ended_at_utc=e)

        _verify_kms_key_owned(kms, key_id, run_id, account_id)
        t, r, e = _timed(lambda: kms.schedule_key_deletion(KeyId=key_id, PendingWindowInDays=7))
        scheduled = True
        ledger.record_kms_scheduled_deletion(key_id, r["DeletionDate"].strftime("%Y-%m-%d"), intent_id=intent)
        results.append(_stim("D7-kms-delete", "kms:ScheduleKeyDeletion", resource_name=name, target_ids=[key_id],
                             expected_event_names=["ScheduleKeyDeletion"], expected_event_source="kms.amazonaws.com",
                             started_at_utc=t, ended_at_utc=e, api_call_succeeded=_http_ok(r)))
        ledger.record_event(["D7-kms-delete"], "kms:ScheduleKeyDeletion", resource_name=name, started_at_utc=t, ended_at_utc=e)
    finally:
        if not scheduled:
            _cleanup(ledger, "kms_key", name, intent, lambda: _delete_verified("kms_key", key_id, run_id, account_id, session=session))
    return results


def run_d7_sns(run_id: str, ledger: RunLedger, *, session: Any = None) -> list[dict[str, Any]]:
    """D7-sns-topic-attr and D7-sns-topic-delete on a throwaway topic (no subscriptions)."""
    sns = locked_boto3_client("sns", session=session)
    account_id = str(ledger.account_id)
    name = make_throwaway_name(run_id, "topic")
    results: list[dict[str, Any]] = []
    deleted = False

    intent = ledger.record_intent("sns_topic", name)
    try:
        resp = sns.create_topic(Name=name, Tags=_tags(run_id))
    except Exception as exc:
        _create_failed(ledger, "sns_topic", name, intent, exc)
        raise
    if resp.get("TopicArn") != _sns_topic_arn(account_id, name):
        raise SafetyViolation("Created topic ARN does not match the pinned region/account/name.")
    ledger.confirm_created(intent, name)

    try:
        arn = _verify_sns_topic_owned(sns, name, run_id, account_id)
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "TesseraDtestOwnerOnly",
                    "Effect": "Allow",
                    "Principal": {"AWS": f"arn:aws:iam::{account_id}:root"},
                    "Action": "sns:GetTopicAttributes",
                    "Resource": arn,
                }
            ],
        }
        t, r, e = _timed(lambda: sns.set_topic_attributes(TopicArn=arn, AttributeName="Policy", AttributeValue=json.dumps(policy)))
        results.append(_stim("D7-sns-topic-attr", "sns:SetTopicAttributes (Policy)", resource_name=name, target_ids=[arn, name],
                             expected_event_names=["SetTopicAttributes"], expected_event_source="sns.amazonaws.com",
                             started_at_utc=t, ended_at_utc=e, api_call_succeeded=_http_ok(r)))
        ledger.record_event(["D7-sns-topic-attr"], "sns:SetTopicAttributes (Policy)", resource_name=name, started_at_utc=t, ended_at_utc=e)

        arn = _verify_sns_topic_owned(sns, name, run_id, account_id)
        t, r, e = _timed(lambda: sns.delete_topic(TopicArn=arn))
        deleted = True
        ledger.record_deleted("sns_topic", name, intent_id=intent)
        results.append(_stim("D7-sns-topic-delete", "sns:DeleteTopic", resource_name=name, target_ids=[arn, name],
                             expected_event_names=["DeleteTopic"], expected_event_source="sns.amazonaws.com",
                             started_at_utc=t, ended_at_utc=e, api_call_succeeded=_http_ok(r)))
        ledger.record_event(["D7-sns-topic-delete"], "sns:DeleteTopic", resource_name=name, started_at_utc=t, ended_at_utc=e)
    finally:
        if not deleted:
            _cleanup(ledger, "sns_topic", name, intent, lambda: _delete_verified("sns_topic", name, run_id, account_id, session=session))
    return results


def run_d7_apigw(run_id: str, ledger: RunLedger, *, session: Any = None) -> list[dict[str, Any]]:
    """D7-apigw-key-create, D7-apigw-key-update, D7-apigw-plan-update (no plan-key attachment)."""
    apigw = locked_boto3_client("apigateway", session=session)
    account_id = str(ledger.account_id)
    key_name = make_throwaway_name(run_id, "key")
    plan_name = make_throwaway_name(run_id, "plan")
    results: list[dict[str, Any]] = []
    key_id: str | None = None
    plan_id: str | None = None
    key_intent: str | None = None
    plan_intent: str | None = None

    try:
        key_intent = ledger.record_intent("apigw_api_key", key_name)
        try:
            t, key_resp, e = _timed(lambda: apigw.create_api_key(
                name=key_name, description="Throwaway detection test key", enabled=False, tags=_tags_map(run_id)))
        except Exception as exc:
            _create_failed(ledger, "apigw_api_key", key_name, key_intent, exc)
            key_intent = None
            raise
        key_id = str(key_resp["id"])
        ledger.confirm_created(key_intent, key_id)
        results.append(_stim("D7-apigw-key-create", "apigateway:CreateApiKey", resource_name=key_name, target_ids=[key_id, key_name],
                             expected_event_names=["CreateApiKey"], expected_event_source="apigateway.amazonaws.com",
                             started_at_utc=t, ended_at_utc=e, api_call_succeeded=_http_ok(key_resp)))
        ledger.record_event(["D7-apigw-key-create"], "apigateway:CreateApiKey", resource_name=key_name, started_at_utc=t, ended_at_utc=e)

        _verify_apigw_api_key_owned(apigw, key_id, run_id)
        t, r, e = _timed(lambda: apigw.update_api_key(
            apiKey=key_id, patchOperations=[{"op": "replace", "path": "/description", "value": "updated-dtest"}]))
        results.append(_stim("D7-apigw-key-update", "apigateway:UpdateApiKey", resource_name=key_name, target_ids=[key_id, key_name],
                             expected_event_names=["UpdateApiKey"], expected_event_source="apigateway.amazonaws.com",
                             started_at_utc=t, ended_at_utc=e, api_call_succeeded=_http_ok(r)))
        ledger.record_event(["D7-apigw-key-update"], "apigateway:UpdateApiKey", resource_name=key_name, started_at_utc=t, ended_at_utc=e)

        plan_intent = ledger.record_intent("apigw_usage_plan", plan_name)
        try:
            plan_resp = apigw.create_usage_plan(
                name=plan_name, description="Throwaway detection test usage plan",
                throttle={"rateLimit": 1.0, "burstLimit": 1}, tags=_tags_map(run_id))
        except Exception as exc:
            _create_failed(ledger, "apigw_usage_plan", plan_name, plan_intent, exc)
            plan_intent = None
            raise
        plan_id = str(plan_resp["id"])
        ledger.confirm_created(plan_intent, plan_id)

        _verify_apigw_usage_plan_owned(apigw, plan_id, run_id)
        t, r, e = _timed(lambda: apigw.update_usage_plan(
            usagePlanId=plan_id, patchOperations=[{"op": "replace", "path": "/description", "value": "updated-dtest"}]))
        results.append(_stim("D7-apigw-plan-update", "apigateway:UpdateUsagePlan", resource_name=plan_name, target_ids=[plan_id, plan_name],
                             expected_event_names=["UpdateUsagePlan"], expected_event_source="apigateway.amazonaws.com",
                             started_at_utc=t, ended_at_utc=e, api_call_succeeded=_http_ok(r)))
        ledger.record_event(["D7-apigw-plan-update"], "apigateway:UpdateUsagePlan", resource_name=plan_name, started_at_utc=t, ended_at_utc=e)
    finally:
        if plan_id and plan_intent:
            _cleanup(ledger, "apigw_usage_plan", plan_name, plan_intent,
                     lambda: _delete_verified("apigw_usage_plan", plan_id, run_id, account_id, session=session))
        if key_id and key_intent:
            _cleanup(ledger, "apigw_api_key", key_name, key_intent,
                     lambda: _delete_verified("apigw_api_key", key_id, run_id, account_id, session=session))
    return results


def _run_single_named(
    run_id: str,
    ledger: RunLedger,
    *,
    rtype: str,
    suffix: str,
    create: Any,
    act: Any,
    row_id: str,
    action: str,
    event_name: str,
    event_source: str,
    create_is_stimulus: bool = False,
    session: Any = None,
) -> list[dict[str, Any]]:
    """Create one tagged, named throwaway resource, perform one action, delete it."""
    account_id = str(ledger.account_id)
    name = make_throwaway_name(run_id, suffix)
    intent = ledger.record_intent(rtype, name)
    try:
        t, r, e = _timed(lambda: create(name))
    except Exception as exc:
        _create_failed(ledger, rtype, name, intent, exc)
        raise
    ledger.confirm_created(intent, name)
    results: list[dict[str, Any]] = []
    try:
        if not create_is_stimulus:
            t, r, e = _timed(lambda: act(name, account_id))
        results.append(_stim(row_id, action, resource_name=name, target_ids=[name],
                             expected_event_names=[event_name], expected_event_source=event_source,
                             started_at_utc=t, ended_at_utc=e, api_call_succeeded=_http_ok(r)))
        ledger.record_event([row_id], action, resource_name=name, started_at_utc=t, ended_at_utc=e)
    finally:
        _cleanup(ledger, rtype, name, intent, lambda: _delete_verified(rtype, name, run_id, account_id, session=session))
    return results


def run_d7_sup_sqs(run_id: str, ledger: RunLedger, *, session: Any = None) -> list[dict[str, Any]]:
    sqs = locked_boto3_client("sqs", session=session)

    def create(name: str) -> Any:
        url = sqs.create_queue(QueueName=name, Attributes={"SqsManagedSseEnabled": "true"}, tags=_tags_map(run_id))["QueueUrl"]
        assert_throwaway_name(url, run_id=run_id, account_id=str(ledger.account_id))
        return {}

    def act(name: str, account_id: str) -> Any:
        url = verify_owned_sqs_queue_live(sqs, name, run_id, account_id)
        return sqs.set_queue_attributes(QueueUrl=url, Attributes={"VisibilityTimeout": "45"})

    return _run_single_named(run_id, ledger, rtype="sqs_queue", suffix="q", create=create, act=act,
                             row_id="D7-sup-sqs", action="sqs:SetQueueAttributes",
                             event_name="SetQueueAttributes", event_source="sqs.amazonaws.com", session=session)


def run_d7_sup_ddb(run_id: str, ledger: RunLedger, *, session: Any = None) -> list[dict[str, Any]]:
    ddb = locked_boto3_client("dynamodb", session=session)

    def create(name: str) -> Any:
        resp = ddb.create_table(
            TableName=name,
            AttributeDefinitions=[{"AttributeName": "pk", "AttributeType": "S"}],
            KeySchema=[{"AttributeName": "pk", "KeyType": "HASH"}],
            BillingMode="PAY_PER_REQUEST",
            Tags=_tags(run_id),
        )
        return resp

    def act(name: str, account_id: str) -> Any:
        ddb.get_waiter("table_exists").wait(TableName=name)
        _verify_ddb_owned(ddb, name, run_id, account_id)
        return ddb.update_time_to_live(TableName=name, TimeToLiveSpecification={"Enabled": True, "AttributeName": "ttl"})

    return _run_single_named(run_id, ledger, rtype="dynamodb_table", suffix="tbl", create=create, act=act,
                             row_id="D7-sup-ddb", action="dynamodb:UpdateTimeToLive",
                             event_name="UpdateTimeToLive", event_source="dynamodb.amazonaws.com", session=session)


def run_d7_sup_cw(run_id: str, ledger: RunLedger, *, session: Any = None) -> list[dict[str, Any]]:
    cw = locked_boto3_client("cloudwatch", session=session)

    def create(name: str) -> Any:
        return cw.put_metric_alarm(
            AlarmName=name,
            AlarmDescription="Throwaway Tessera detection test alarm (no actions)",
            MetricName="DtestDummy",
            Namespace="Tessera/DetectionTest",
            Statistic="Sum",
            Period=300,
            EvaluationPeriods=1,
            Threshold=1.0,
            ComparisonOperator="GreaterThanOrEqualToThreshold",
            Tags=_tags(run_id),
        )

    return _run_single_named(run_id, ledger, rtype="cloudwatch_alarm", suffix="alarm", create=create, act=None,
                             row_id="D7-sup-cw", action="cloudwatch:PutMetricAlarm", event_name="PutMetricAlarm",
                             event_source="monitoring.amazonaws.com", create_is_stimulus=True, session=session)


def run_d7_sup_logs(run_id: str, ledger: RunLedger, *, session: Any = None) -> list[dict[str, Any]]:
    logs = locked_boto3_client("logs", session=session)

    def create(name: str) -> Any:
        return logs.create_log_group(logGroupName=name, tags=_tags_map(run_id))

    def act(name: str, account_id: str) -> Any:
        if _verify_log_group_owned(logs, name, run_id, account_id) is None:
            raise SafetyViolation("Throwaway log group not found for ownership check.")
        return logs.put_retention_policy(logGroupName=name, retentionInDays=1)

    return _run_single_named(run_id, ledger, rtype="log_group", suffix="logs", create=create, act=act,
                             row_id="D7-sup-logs", action="logs:PutRetentionPolicy",
                             event_name="PutRetentionPolicy", event_source="logs.amazonaws.com", session=session)


def run_d7_sup_eb(run_id: str, ledger: RunLedger, *, session: Any = None) -> list[dict[str, Any]]:
    eb = locked_boto3_client("events", session=session)

    def create(name: str) -> Any:
        return eb.put_rule(
            Name=name,
            EventPattern=json.dumps({"source": ["tessera.dtest.noop"]}),
            State="DISABLED",
            Description="Throwaway Tessera detection test rule",
            Tags=_tags(run_id),
        )

    return _run_single_named(run_id, ledger, rtype="eventbridge_rule", suffix="rule", create=create, act=None,
                             row_id="D7-sup-eb", action="events:PutRule", event_name="PutRule",
                             event_source="events.amazonaws.com", create_is_stimulus=True, session=session)


# ---------------------------------------------------------------------------
# Verified delete (used by normal cleanup and by recovery)
# ---------------------------------------------------------------------------

def _delete_verified(rtype: str, ident: str | None, run_id: str, account_id: str, *, session: Any = None) -> tuple[str, str]:
    """Delete ONE resource after live service-side ownership verification.

    Returns (status, detail). Raises SafetyViolation if verification fails.
    """
    if not ident:
        raise SafetyViolation("Missing identifier for verified delete.")
    if rtype == "kms_key":
        kms = locked_boto3_client("kms", session=session)
        meta = _verify_kms_key_owned(kms, ident, run_id, account_id)
        if meta.get("KeyState") == "PendingDeletion":
            return "scheduled_deletion", f"scheduled, deletes on {meta['DeletionDate'].strftime('%Y-%m-%d')}"
        resp = kms.schedule_key_deletion(KeyId=meta["KeyId"], PendingWindowInDays=7)
        return "scheduled_deletion", f"scheduled, deletes on {resp['DeletionDate'].strftime('%Y-%m-%d')}"
    if rtype == "sns_topic":
        sns = locked_boto3_client("sns", session=session)
        try:
            arn = _verify_sns_topic_owned(sns, ident, run_id, account_id)
        except Exception as exc:
            if _is_not_found(exc):
                return "deleted", "already_gone"
            raise
        sns.delete_topic(TopicArn=arn)
        return "deleted", "deleted"
    if rtype == "apigw_api_key":
        apigw = locked_boto3_client("apigateway", session=session)
        try:
            _verify_apigw_api_key_owned(apigw, ident, run_id)
        except Exception as exc:
            if _is_not_found(exc):
                return "deleted", "already_gone"
            raise
        apigw.delete_api_key(apiKey=ident)
        return "deleted", "deleted"
    if rtype == "apigw_usage_plan":
        apigw = locked_boto3_client("apigateway", session=session)
        try:
            _verify_apigw_usage_plan_owned(apigw, ident, run_id)
        except Exception as exc:
            if _is_not_found(exc):
                return "deleted", "already_gone"
            raise
        apigw.delete_usage_plan(usagePlanId=ident)
        return "deleted", "deleted"
    if rtype == "sqs_queue":
        sqs = locked_boto3_client("sqs", session=session)
        try:
            url = verify_owned_sqs_queue_live(sqs, ident, run_id, account_id)
        except Exception as exc:
            if _is_not_found(exc):
                return "deleted", "already_gone"
            raise
        sqs.delete_queue(QueueUrl=url)
        return "deleted", "deleted"
    if rtype == "dynamodb_table":
        ddb = locked_boto3_client("dynamodb", session=session)
        try:
            _verify_ddb_owned(ddb, ident, run_id, account_id)
        except Exception as exc:
            if _is_not_found(exc):
                return "deleted", "already_gone"
            raise
        ddb.delete_table(TableName=ident)
        return "deleted", "deleted"
    if rtype == "cloudwatch_alarm":
        cw = locked_boto3_client("cloudwatch", session=session)
        if _verify_cw_alarm_owned(cw, ident, run_id, account_id) is None:
            return "deleted", "already_gone"
        cw.delete_alarms(AlarmNames=[ident])
        return "deleted", "deleted"
    if rtype == "log_group":
        logs = locked_boto3_client("logs", session=session)
        if _verify_log_group_owned(logs, ident, run_id, account_id) is None:
            return "deleted", "already_gone"
        logs.delete_log_group(logGroupName=ident)
        return "deleted", "deleted"
    if rtype == "eventbridge_rule":
        eb = locked_boto3_client("events", session=session)
        try:
            _verify_eb_rule_owned(eb, ident, run_id, account_id)
        except Exception as exc:
            if _is_not_found(exc):
                return "deleted", "already_gone"
            raise
        eb.delete_rule(Name=ident)
        return "deleted", "deleted"
    raise SafetyViolation("Refusing unknown resource type during delete.")


# ---------------------------------------------------------------------------
# Tag-only crash recovery
# ---------------------------------------------------------------------------

_CLEAN_STATUSES = ("deleted", "scheduled_deletion", "not_created")
_OPAQUE_ID_TYPES = ("kms_key", "apigw_api_key", "apigw_usage_plan")


def _safe_name(name: Any, run_id: str) -> str:
    try:
        return assert_throwaway_name(str(name or ""), run_id=run_id)
    except SafetyViolation:
        return "<invalid-name>"


def _safe_type(rtype: Any) -> str:
    return str(rtype) if rtype in RESOURCE_TYPES else "<unknown-type>"


def cleanup_from_ledger_file(
    ledger_path: Any,
    *,
    session: Any = None,
    secrets: Iterable[str] = (),
) -> dict[str, Any]:
    """Tag-search-only recovery for one ledger. ok=False on any refused, failed, or residual item."""
    path = Path(ledger_path)
    raw = load_ledger(path)
    run_id = validate_run_id(str(raw.get("run_id") or ""))
    account_id, _ = get_caller_identity(session=session)
    if raw.get("account_id") != account_id:
        raise SafetyViolation("Ledger account_id is missing or does not match the current caller account.")

    resources: list[dict[str, Any]] = raw.setdefault("resources", [])
    intent_types = {r.get("resource_type") for r in resources}
    actions: list[str] = []
    refused: list[str] = []
    failed: list[str] = []

    live = discover_live_run_resources(run_id, account_id, session=session)
    for item in live:
        rtype = item["resource_type"]
        shown = "(tagged)" if rtype in _OPAQUE_ID_TYPES else _safe_name(item["name"], run_id)
        label = f"{_safe_type(rtype)} {shown}"
        if rtype == "unknown" or rtype not in intent_types:
            refused.append(f"refused_no_matching_intent {label}")
            continue
        try:
            status, detail = _delete_verified(rtype, item["identifier"], run_id, account_id, session=session)
        except SafetyViolation as exc:
            refused.append(f"refused_unverified {label}: {safe_error_label(exc)}")
            continue
        except Exception as exc:
            failed.append(f"failed {label}: {safe_error_label(exc)}")
            continue
        actions.append(f"{detail} {label}")
        # Close the matching entry: by identifier if recorded, else the open intent of that type.
        target = None
        for entry in resources:
            if entry.get("resource_type") == rtype and entry.get("identifier") == item["identifier"]:
                target = entry
                break
        if target is None:
            for entry in resources:
                if entry.get("resource_type") == rtype and entry.get("status") not in _CLEAN_STATUSES and not entry.get("identifier"):
                    target = entry
                    break
        if target is not None:
            target["status"] = status
            target["identifier"] = target.get("identifier") or item["identifier"]
            target["deleted_at_utc"] = utc_now_iso()
            target["detail"] = detail

    # Residuals: anything still tagged live (except keys pending deletion), plus any ledger
    # entry that is not provably clean. A search miss never closes an intent.
    residuals: list[str] = []
    kms = None
    for item in discover_live_run_resources(run_id, account_id, session=session):
        if item["resource_type"] == "kms_key":
            try:
                kms = kms or locked_boto3_client("kms", session=session)
                if kms.describe_key(KeyId=item["identifier"])["KeyMetadata"].get("KeyState") == "PendingDeletion":
                    continue
            except Exception:
                pass
        residuals.append(f"live:{_safe_type(item['resource_type'])}")
    for entry in resources:
        if entry.get("status") not in _CLEAN_STATUSES:
            residuals.append(f"ledger:{_safe_type(entry.get('resource_type'))}:{_safe_name(entry.get('name'), run_id)}:{entry.get('status')}")

    ok = not refused and not failed and not residuals
    raw.setdefault("recovery_runs", []).append(
        {
            "at_utc": utc_now_iso(),
            "ok": ok,
            "actions_count": len(actions),
            "refused_count": len(refused),
            "failed_count": len(failed),
            "residual_count": len(residuals),
            "residuals": residuals,
        }
    )
    save_ledger_dict(path, raw, secrets)
    return {"run_id": run_id, "ok": ok, "actions": actions, "refused": refused, "failed": failed, "residuals": residuals}
