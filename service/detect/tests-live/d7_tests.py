"""D7 control-plane tampering tests and live-verified crash recovery.

Safety & ownership guarantees (BRIEF-gemini.md r5, Rules 1, 2, 5, 6):
- Every AWS client is pinned to us-east-2 with no endpoint override honoured
  (global IAM access requires explicit allow_global_iam=True).
- Pre-flight check refuses to start if any AWS resource with this run_id already exists.
- A durable 'creating' ledger intent is flushed BEFORE every AWS create call (including
  dependent resources: KMS grants, API GW usage-plan keys, IAM inline policies, Lambda
  permissions, and IAM access keys without ever logging credential material).
- Every mutation, dependent call, normal cleanup, and crash-recovery action re-verifies
  live AWS ownership by tag (purpose=detection-test AND run_id=<run_id>), name prefix
  (tessera-dtest-<run_id>-*), account ID, and region BEFORE any destructive call.
- Crash recovery reconciles 'creating' intents via live tag/prefix search, refuses any
  unverified/forged ledger identifier without calling AWS mutating APIs, persists
  sanitized results back to the ledger, and reports residuals so the CLI exits non-zero.
- Every test returns structured per-action stimulus results with exact UTC windows and
  target IDs for CloudTrail and SNS correlation.
"""

from __future__ import annotations

import io
import json
import time
import zipfile
from pathlib import Path
from typing import Any

from ledger import RunLedger, load_ledger, save_ledger_dict, utc_now_iso
from observer import (
    find_alarm_topic_arn,
    verify_owned_observer_subscription_live,
    verify_owned_sqs_queue_live,
)
from safety import (
    ALLOWED_REGION,
    PRODUCTION_ALARM_TOPIC_NAME,
    PURPOSE_TAG_KEY,
    PURPOSE_TAG_VALUE,
    RUN_ID_TAG_KEY,
    SafetyViolation,
    assert_ownership_tags,
    assert_throwaway_id_registered,
    assert_throwaway_name,
    locked_boto3_client,
    make_throwaway_name,
    safe_error_label,
    validate_run_id,
)


def _error_code(exc: BaseException) -> str:
    resp = getattr(exc, "response", None)
    if isinstance(resp, dict):
        return str(resp.get("Error", {}).get("Code", ""))
    return ""


def _is_not_found(exc: BaseException) -> bool:
    code = _error_code(exc)
    return code in (
        "NotFoundException",
        "ResourceNotFoundException",
        "NoSuchEntity",
        "NoSuchEntityException",
        "NoSuchBucket",
        "NoSuchTrail",
        "TrailNotFoundException",
        "AWS.SimpleQueueService.NonExistentQueue",
        "QueueDoesNotExist",
        "NotFound",
    )


def _http_ok(resp: Any) -> bool:
    if not isinstance(resp, dict):
        return True
    meta = resp.get("ResponseMetadata")
    if not isinstance(meta, dict):
        return True
    code = meta.get("HTTPStatusCode")
    return code is None or (200 <= int(code) < 300)


def get_caller_identity(session: Any = None) -> tuple[str, str]:
    """Return (account_id, caller_arn) from regional us-east-2 STS."""
    sts = locked_boto3_client("sts", session=session)
    ident = sts.get_caller_identity()
    return str(ident["Account"]), str(ident["Arn"])


def _tags_list_to_dict(tags_list: list[dict[str, Any]] | None, key_field: str = "Key", val_field: str = "Value") -> dict[str, str]:
    out: dict[str, str] = {}
    for item in tags_list or []:
        k = item.get(key_field)
        v = item.get(val_field)
        if isinstance(k, str) and isinstance(v, str):
            out[k] = v
    return out


# ---------------------------------------------------------------------------
# Live ownership verifiers (tag + name + run_id + account + region)
# ---------------------------------------------------------------------------

def _verify_kms_key_owned(kms: Any, key_id: str, run_id: str, account_id: str) -> dict[str, Any]:
    meta = kms.describe_key(KeyId=key_id)["KeyMetadata"]
    if str(meta.get("AWSAccountId")) != account_id:
        raise SafetyViolation("KMS key account mismatch.")
    arn = str(meta.get("Arn") or "")
    if not arn.startswith(f"arn:aws:kms:{ALLOWED_REGION}:{account_id}:key/"):
        raise SafetyViolation("KMS key ARN outside pinned region/account.")
    desc = str(meta.get("Description") or "")
    expected_prefix = f"tessera-dtest-{run_id}-"
    if not desc.startswith(expected_prefix) or "tessera-v1" in desc.lower():
        raise SafetyViolation("KMS key description does not match this run_id throwaway prefix.")
    tags_resp = kms.list_resource_tags(KeyId=meta["KeyId"])
    tags = _tags_list_to_dict(tags_resp.get("Tags"), "TagKey", "TagValue")
    assert_ownership_tags(tags, run_id, f"kms_key:{meta['KeyId']}")
    return meta


def _verify_kms_alias_owned(kms: Any, alias_name: str, run_id: str, account_id: str) -> str | None:
    assert_throwaway_name(alias_name, allow_alias_prefix=True, run_id=run_id)
    paginator = kms.get_paginator("list_aliases")
    for page in paginator.paginate():
        for a in page.get("Aliases", []):
            if a.get("AliasName") == alias_name:
                target_key_id = a.get("TargetKeyId")
                if target_key_id:
                    _verify_kms_key_owned(kms, target_key_id, run_id, account_id)
                return target_key_id
    return None


def _verify_s3_bucket_owned(s3: Any, bucket_name: str, run_id: str, account_id: str) -> None:
    assert_throwaway_name(bucket_name, run_id=run_id)
    loc = s3.get_bucket_location(Bucket=bucket_name, ExpectedBucketOwner=account_id).get(
        "LocationConstraint"
    )
    if loc != ALLOWED_REGION:
        raise SafetyViolation("S3 bucket location is outside us-east-2.")
    tag_resp = s3.get_bucket_tagging(Bucket=bucket_name, ExpectedBucketOwner=account_id)
    tags = _tags_list_to_dict(tag_resp.get("TagSet"))
    assert_ownership_tags(tags, run_id, f"s3_bucket:{bucket_name}")


def _verify_sns_topic_owned(sns: Any, topic_arn: str, run_id: str, account_id: str) -> None:
    assert_throwaway_name(topic_arn, run_id=run_id, account_id=account_id)
    tags = _tags_list_to_dict(sns.list_tags_for_resource(ResourceArn=topic_arn).get("Tags"))
    assert_ownership_tags(tags, run_id, "sns_topic")


def _verify_apigw_rest_api_owned(apigw: Any, api_id: str, run_id: str) -> dict[str, Any]:
    api = apigw.get_rest_api(restApiId=api_id)
    assert_throwaway_name(str(api.get("name") or ""), run_id=run_id)
    assert_ownership_tags(api.get("tags"), run_id, "apigw_rest_api")
    return api


def _verify_apigw_api_key_owned(apigw: Any, key_id: str, run_id: str) -> dict[str, Any]:
    key = apigw.get_api_key(apiKey=key_id, includeValue=False)
    assert_throwaway_name(str(key.get("name") or ""), run_id=run_id)
    assert_ownership_tags(key.get("tags"), run_id, "apigw_api_key")
    return key


def _verify_apigw_usage_plan_owned(apigw: Any, plan_id: str, run_id: str) -> dict[str, Any]:
    plan = apigw.get_usage_plan(usagePlanId=plan_id)
    assert_throwaway_name(str(plan.get("name") or ""), run_id=run_id)
    assert_ownership_tags(plan.get("tags"), run_id, "apigw_usage_plan")
    return plan


def _verify_lambda_owned(lam: Any, fn_name: str, run_id: str, account_id: str) -> dict[str, Any]:
    assert_throwaway_name(fn_name, run_id=run_id)
    fn = lam.get_function(FunctionName=fn_name)
    arn = str(fn.get("Configuration", {}).get("FunctionArn") or "")
    assert_throwaway_name(arn, run_id=run_id, account_id=account_id)
    assert_ownership_tags(fn.get("Tags"), run_id, f"lambda:{fn_name}")
    return fn


def _verify_iam_role_owned(iam: Any, role_name: str, run_id: str, account_id: str) -> dict[str, Any]:
    assert_throwaway_name(role_name, run_id=run_id)
    role = iam.get_role(RoleName=role_name)["Role"]
    arn = str(role.get("Arn") or "")
    assert_throwaway_name(arn, run_id=run_id, account_id=account_id)
    tags = _tags_list_to_dict(role.get("Tags"))
    assert_ownership_tags(tags, run_id, f"iam_role:{role_name}")
    return role


def _verify_iam_user_owned(iam: Any, user_name: str, run_id: str, account_id: str) -> dict[str, Any]:
    assert_throwaway_name(user_name, run_id=run_id)
    user = iam.get_user(UserName=user_name)["User"]
    arn = str(user.get("Arn") or "")
    assert_throwaway_name(arn, run_id=run_id, account_id=account_id)
    tags = _tags_list_to_dict(user.get("Tags"))
    assert_ownership_tags(tags, run_id, f"iam_user:{user_name}")
    return user


def _verify_cloudtrail_owned(ct: Any, trail_name: str, run_id: str, account_id: str) -> dict[str, Any]:
    assert_throwaway_name(trail_name, run_id=run_id)
    trail = ct.get_trail(Name=trail_name)["Trail"]
    if trail.get("HomeRegion") != ALLOWED_REGION:
        raise SafetyViolation("CloudTrail HomeRegion is outside us-east-2.")
    arn = str(trail.get("TrailARN") or "")
    assert_throwaway_name(arn, run_id=run_id, account_id=account_id)
    tag_resp = ct.list_tags(ResourceIdList=[arn]).get("ResourceTagList", [])
    tags = _tags_list_to_dict(tag_resp[0].get("TagsList") if tag_resp else [])
    assert_ownership_tags(tags, run_id, f"cloudtrail:{trail_name}")
    return trail


def _verify_ddb_owned(ddb: Any, tbl_name: str, run_id: str, account_id: str) -> dict[str, Any]:
    assert_throwaway_name(tbl_name, run_id=run_id)
    tbl = ddb.describe_table(TableName=tbl_name)["Table"]
    arn = str(tbl.get("TableArn") or "")
    assert_throwaway_name(arn, run_id=run_id, account_id=account_id)
    tags = _tags_list_to_dict(ddb.list_tags_of_resource(ResourceArn=arn).get("Tags"))
    assert_ownership_tags(tags, run_id, f"dynamodb_table:{tbl_name}")
    return tbl


def _verify_cw_alarm_owned(cw: Any, alarm_name: str, run_id: str, account_id: str) -> dict[str, Any]:
    assert_throwaway_name(alarm_name, run_id=run_id)
    alarms = cw.describe_alarms(AlarmNames=[alarm_name]).get("MetricAlarms", [])
    matched = [a for a in alarms if a.get("AlarmName") == alarm_name]
    if not matched:
        raise KeyError("alarm_not_found")
    arn = str(matched[0].get("AlarmArn") or "")
    assert_throwaway_name(arn, run_id=run_id, account_id=account_id)
    tags = _tags_list_to_dict(cw.list_tags_for_resource(ResourceARN=arn).get("Tags"))
    assert_ownership_tags(tags, run_id, f"cloudwatch_alarm:{alarm_name}")
    return matched[0]


def _verify_log_group_owned(logs: Any, group_name: str, run_id: str, account_id: str) -> dict[str, Any]:
    assert_throwaway_name(group_name, run_id=run_id)
    groups = logs.describe_log_groups(logGroupNamePrefix=group_name).get("logGroups", [])
    matched = [g for g in groups if g.get("logGroupName") == group_name]
    if not matched:
        raise KeyError("log_group_not_found")
    arn = str(matched[0].get("arn") or "").rstrip(":*")
    assert_throwaway_name(arn, run_id=run_id, account_id=account_id)
    tags = logs.list_tags_for_resource(resourceArn=arn).get("tags", {})
    assert_ownership_tags(tags, run_id, f"log_group:{group_name}")
    return matched[0]


def _verify_eb_rule_owned(eb: Any, rule_name: str, run_id: str, account_id: str) -> dict[str, Any]:
    assert_throwaway_name(rule_name, run_id=run_id)
    rule = eb.describe_rule(Name=rule_name)
    arn = str(rule.get("Arn") or "")
    assert_throwaway_name(arn, run_id=run_id, account_id=account_id)
    tags = _tags_list_to_dict(eb.list_tags_for_resource(ResourceARN=arn).get("Tags"))
    assert_ownership_tags(tags, run_id, f"eventbridge_rule:{rule_name}")
    return rule


# ---------------------------------------------------------------------------
# Pre-flight & live run discovery (Findings 5, 6, 7)
# ---------------------------------------------------------------------------

def discover_live_run_resources(
    run_id: str,
    account_id: str,
    *,
    session: Any = None,
    include_iam: bool = True,
) -> list[dict[str, str]]:
    """Discover all live AWS resources belonging to run_id via tag and prefix queries."""
    validate_run_id(run_id)
    prefix = f"tessera-dtest-{run_id}-"
    found: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()

    def _add(rtype: str, ident: str, name: str) -> None:
        key = (rtype, ident)
        if key not in seen:
            seen.add(key)
            found.append({"resource_type": rtype, "identifier": ident, "name": name})

    # 1. Resource Groups Tagging API (regional us-east-2)
    tag_api = locked_boto3_client("resourcegroupstaggingapi", session=session)
    for page in tag_api.get_paginator("get_resources").paginate(
        TagFilters=[{"Key": RUN_ID_TAG_KEY, "Values": [run_id]}]
    ):
        for item in page.get("ResourceTagMappingList", []):
            arn = str(item.get("ResourceARN") or "")
            if ":kms:" in arn and ":key/" in arn:
                key_id = arn.split(":key/")[-1]
                _add("kms_key", key_id, f"{prefix}kms")
            elif ":sns:" in arn:
                tname = arn.split(":")[-1]
                if tname.startswith(prefix):
                    _add("sns_topic", arn, tname)
            elif ":sqs:" in arn:
                qname = arn.split(":")[-1]
                if qname.startswith(prefix):
                    rtype = "sqs_observer_queue" if qname.endswith("-obs-q") else "sqs_queue"
                    _add(rtype, qname, qname)
            elif ":s3:::" in arn:
                bname = arn.split(":::")[-1]
                if bname.startswith(prefix):
                    _add("s3_bucket", bname, bname)
            elif ":lambda:" in arn:
                fname = arn.split(":function:")[-1]
                if fname.startswith(prefix):
                    _add("lambda_function", fname, fname)
            elif ":dynamodb:" in arn:
                tname = arn.split(":table/")[-1]
                if tname.startswith(prefix):
                    _add("dynamodb_table", tname, tname)
            elif ":cloudwatch:" in arn:
                aname = arn.split(":alarm:")[-1]
                if aname.startswith(prefix):
                    _add("cloudwatch_alarm", aname, aname)
            elif ":logs:" in arn:
                gname = arn.split(":log-group:")[-1].rstrip(":*")
                if gname.startswith(prefix):
                    _add("log_group", gname, gname)
            elif ":events:" in arn:
                rname = arn.split(":rule/")[-1]
                if rname.startswith(prefix):
                    _add("eventbridge_rule", rname, rname)
            elif ":cloudtrail:" in arn:
                trname = arn.split(":trail/")[-1]
                if trname.startswith(prefix):
                    _add("cloudtrail", trname, trname)

    # 2. Direct per-service scans (covers global IAM, eventual tag indexing, & non-tagged sub-resources)
    sqs = locked_boto3_client("sqs", session=session)
    for url in sqs.list_queues(QueueNamePrefix=prefix).get("QueueUrls", []):
        qname = url.rstrip("/").split("/")[-1]
        if qname.startswith(prefix):
            rtype = "sqs_observer_queue" if qname.endswith("-obs-q") else "sqs_queue"
            _add(rtype, qname, qname)

    sns = locked_boto3_client("sns", session=session)
    prod_topic_arn: str | None = None
    for page in sns.get_paginator("list_topics").paginate():
        for t in page.get("Topics", []):
            arn = str(t.get("TopicArn") or "")
            tname = arn.split(":")[-1]
            if tname == PRODUCTION_ALARM_TOPIC_NAME:
                prod_topic_arn = arn
            elif tname.startswith(prefix):
                _add("sns_topic", arn, tname)
    if prod_topic_arn:
        obs_q_arn = f"arn:aws:sqs:{ALLOWED_REGION}:{account_id}:{make_throwaway_name(run_id, 'obs-q')}"
        for page in sns.get_paginator("list_subscriptions_by_topic").paginate(TopicArn=prod_topic_arn):
            for sub in page.get("Subscriptions", []):
                if sub.get("Protocol") == "sqs" and sub.get("Endpoint") == obs_q_arn:
                    sub_arn = str(sub.get("SubscriptionArn") or "")
                    if sub_arn.startswith(f"{prod_topic_arn}:"):
                        _add(
                            "sns_observer_subscription",
                            sub_arn,
                            f"{make_throwaway_name(run_id, 'obs-q')}->{PRODUCTION_ALARM_TOPIC_NAME}",
                        )

    s3 = locked_boto3_client("s3", session=session)
    for b in s3.list_buckets().get("Buckets", []):
        bname = str(b.get("Name") or "")
        if bname.startswith(prefix):
            _add("s3_bucket", bname, bname)

    kms = locked_boto3_client("kms", session=session)
    for page in kms.get_paginator("list_aliases").paginate():
        for a in page.get("Aliases", []):
            aname = str(a.get("AliasName") or "")
            if aname.startswith(f"alias/{prefix}"):
                _add("kms_alias", aname, aname)
                if a.get("TargetKeyId"):
                    _add("kms_key", str(a["TargetKeyId"]), aname[len("alias/") :])

    apigw = locked_boto3_client("apigateway", session=session)
    for page in apigw.get_paginator("get_rest_apis").paginate():
        for item in page.get("items", []):
            if str(item.get("name") or "").startswith(prefix):
                _add("apigw_rest_api", str(item["id"]), str(item["name"]))
    for page in apigw.get_paginator("get_api_keys").paginate(includeValues=False):
        for item in page.get("items", []):
            if str(item.get("name") or "").startswith(prefix):
                _add("apigw_api_key", str(item["id"]), str(item["name"]))
    for page in apigw.get_paginator("get_usage_plans").paginate():
        for item in page.get("items", []):
            if str(item.get("name") or "").startswith(prefix):
                _add("apigw_usage_plan", str(item["id"]), str(item["name"]))

    lam = locked_boto3_client("lambda", session=session)
    for page in lam.get_paginator("list_functions").paginate():
        for fn in page.get("Functions", []):
            fname = str(fn.get("FunctionName") or "")
            if fname.startswith(prefix):
                _add("lambda_function", fname, fname)

    ct = locked_boto3_client("cloudtrail", session=session)
    for t in ct.list_trails().get("Trails", []):
        tname = str(t.get("Name") or "")
        if tname.startswith(prefix):
            _add("cloudtrail", tname, tname)

    ddb = locked_boto3_client("dynamodb", session=session)
    for page in ddb.get_paginator("list_tables").paginate():
        for tname in page.get("TableNames", []):
            if str(tname).startswith(prefix):
                _add("dynamodb_table", str(tname), str(tname))

    cw = locked_boto3_client("cloudwatch", session=session)
    for page in cw.get_paginator("describe_alarms").paginate(AlarmNamePrefix=prefix):
        for a in page.get("MetricAlarms", []):
            aname = str(a.get("AlarmName") or "")
            if aname.startswith(prefix):
                _add("cloudwatch_alarm", aname, aname)

    logs = locked_boto3_client("logs", session=session)
    for page in logs.get_paginator("describe_log_groups").paginate(logGroupNamePrefix=prefix):
        for g in page.get("logGroups", []):
            gname = str(g.get("logGroupName") or "")
            if gname.startswith(prefix):
                _add("log_group", gname, gname)

    eb = locked_boto3_client("events", session=session)
    for page in eb.get_paginator("list_rules").paginate(NamePrefix=prefix):
        for r in page.get("Rules", []):
            rname = str(r.get("Name") or "")
            if rname.startswith(prefix):
                _add("eventbridge_rule", rname, rname)

    if include_iam:
        iam = locked_boto3_client("iam", session=session, allow_global_iam=True)
        for page in iam.get_paginator("list_roles").paginate():
            for role in page.get("Roles", []):
                rname = str(role.get("RoleName") or "")
                if rname.startswith(prefix):
                    _add("iam_role", rname, rname)
        for page in iam.get_paginator("list_users").paginate():
            for user in page.get("Users", []):
                uname = str(user.get("UserName") or "")
                if uname.startswith(prefix):
                    _add("iam_user", uname, uname)

    return found


def assert_no_existing_run_resources(
    run_id: str,
    account_id: str,
    *,
    session: Any = None,
    include_iam: bool = True,
) -> None:
    """Refuse to start if any AWS resource with this run_id already exists (Finding 5)."""
    existing = discover_live_run_resources(
        run_id, account_id, session=session, include_iam=include_iam
    )
    if existing:
        summary = ", ".join(f"{r['resource_type']}:{r['name']}" for r in existing[:10])
        raise SafetyViolation(
            f"Refusing to start: {len(existing)} existing resource(s) already present for "
            f"run_id={run_id} ({summary}). Choose a fresh run_id or recover the old run first."
        )


def _make_noop_lambda_zip(comment: str) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(
            "index.py",
            f"# {comment}\ndef handler(event, context):\n    return {{'ok': True}}\n",
        )
    return buf.getvalue()


def _wait_lambda_ready(lam: Any, fn_name: str, timeout_s: float = 60.0) -> None:
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        cfg = lam.get_function_configuration(FunctionName=fn_name)
        state = cfg.get("State", "Active")
        update_status = cfg.get("LastUpdateStatus", "Successful")
        if state == "Active" and update_status in ("Successful", None):
            return
        if state == "Failed" or update_status == "Failed":
            raise RuntimeError(f"Throwaway Lambda {fn_name} entered Failed state.")
        time.sleep(2.0)
    raise TimeoutError(f"Timed out waiting for throwaway Lambda {fn_name} to become Active")


def _empty_throwaway_bucket(s3: Any, bucket_name: str, run_id: str, account_id: str) -> None:
    """Empty all object versions AND delete markers after verifying live bucket ownership."""
    _verify_s3_bucket_owned(s3, bucket_name, run_id, account_id)
    paginator = s3.get_paginator("list_object_versions")
    for page in paginator.paginate(Bucket=bucket_name, ExpectedBucketOwner=account_id):
        batch: list[dict[str, str]] = []
        for v in page.get("Versions", []):
            item = {"Key": v["Key"]}
            if v.get("VersionId") and v["VersionId"] != "null":
                item["VersionId"] = v["VersionId"]
            batch.append(item)
        for dm in page.get("DeleteMarkers", []):
            item = {"Key": dm["Key"]}
            if dm.get("VersionId") and dm["VersionId"] != "null":
                item["VersionId"] = dm["VersionId"]
            batch.append(item)
        if batch:
            resp = s3.delete_objects(
                Bucket=bucket_name,
                Delete={"Objects": batch, "Quiet": False},
                ExpectedBucketOwner=account_id,
            )
            errors = resp.get("Errors", [])
            if errors:
                raise RuntimeError(
                    f"S3 bulk delete reported {len(errors)} error(s) on {bucket_name}."
                )


def _stim(
    row_id: str,
    action: str,
    *,
    kind: str,
    resource_name: str,
    target_ids: list[str],
    expected_event_names: list[str],
    expected_event_source: str,
    started_at_utc: str,
    ended_at_utc: str,
    api_call_succeeded: bool,
    contract_latency_s: int = 600,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "row_id": row_id,
        "action": action,
        "kind": kind,
        "resource_name": resource_name,
        "target_ids": [t for t in target_ids if t],
        "expected_event_names": expected_event_names,
        "expected_event_source": expected_event_source,
        "started_at_utc": started_at_utc,
        "ended_at_utc": ended_at_utc,
        "api_call_succeeded": api_call_succeeded,
        "contract_latency_s": contract_latency_s,
        "sns_observable": True,
        "details": details or {},
    }


# ---------------------------------------------------------------------------
# D7 Test Functions
# ---------------------------------------------------------------------------

def run_d7_kms(run_id: str, ledger: RunLedger, *, session: Any = None) -> list[dict[str, Any]]:
    """D7-kms-policy, D7-kms-grant, D7-kms-disable, D7-kms-delete on a throwaway KMS key."""
    kms = locked_boto3_client("kms", session=session)
    account_id, caller_arn = get_caller_identity(session=session)
    name = make_throwaway_name(run_id, "kms")
    alias_name = f"alias/{name}"
    assert_throwaway_name(alias_name, allow_alias_prefix=True, run_id=run_id)

    owned_keys: set[str] = set()
    key_id: str | None = None
    key_arn: str | None = None
    grant_id: str | None = None
    key_intent = ledger.record_intent("kms_key", name)
    alias_intent: str | None = None
    grant_intent: str | None = None
    deletion_scheduled = False
    results: list[dict[str, Any]] = []

    try:
        resp = kms.create_key(
            Description=f"{name} (throwaway detection test)",
            KeyUsage="ENCRYPT_DECRYPT",
            KeySpec="SYMMETRIC_DEFAULT",
            Tags=[
                {"TagKey": PURPOSE_TAG_KEY, "TagValue": PURPOSE_TAG_VALUE},
                {"TagKey": RUN_ID_TAG_KEY, "TagValue": run_id},
            ],
        )
        key_id = resp["KeyMetadata"]["KeyId"]
        key_arn = resp["KeyMetadata"]["Arn"]
        owned_keys.add(key_id)
        ledger.confirm_created(key_intent, key_id, metadata={"key_arn": key_arn})
        _verify_kms_key_owned(kms, key_id, run_id, account_id)

        alias_intent = ledger.record_intent("kms_alias", alias_name, metadata={"key_id": key_id})
        kms.create_alias(AliasName=alias_name, TargetKeyId=key_id)
        ledger.confirm_created(alias_intent, alias_name, metadata={"key_id": key_id})

        # 1. PutKeyPolicy
        assert_throwaway_id_registered(key_id, owned_keys, "kms:PutKeyPolicy")
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
        t1 = utc_now_iso()
        r1 = kms.put_key_policy(KeyId=key_id, PolicyName="default", Policy=json.dumps(policy))
        e1 = utc_now_iso()
        s1 = _stim(
            "D7-kms-policy",
            "kms:PutKeyPolicy",
            kind="d7_eventbridge",
            resource_name=name,
            target_ids=[key_id, key_arn],
            expected_event_names=["PutKeyPolicy"],
            expected_event_source="kms.amazonaws.com",
            started_at_utc=t1,
            ended_at_utc=e1,
            api_call_succeeded=_http_ok(r1),
            details={"key_id": key_id},
        )
        results.append(s1)
        ledger.record_event(["D7-kms-policy"], "kms:PutKeyPolicy", resource_name=name, started_at_utc=t1, ended_at_utc=e1, details={"key_id": key_id})

        # 2. CreateGrant
        assert_throwaway_id_registered(key_id, owned_keys, "kms:CreateGrant")
        _verify_kms_key_owned(kms, key_id, run_id, account_id)
        grant_intent = ledger.record_intent("kms_grant", f"{name}-grant", metadata={"key_id": key_id})
        t2 = utc_now_iso()
        g_resp = kms.create_grant(
            KeyId=key_id,
            GranteePrincipal=caller_arn,
            Operations=["DescribeKey"],
            Name=name,
        )
        e2 = utc_now_iso()
        grant_id = g_resp["GrantId"]
        ledger.confirm_created(grant_intent, grant_id, metadata={"key_id": key_id})
        s2 = _stim(
            "D7-kms-grant",
            "kms:CreateGrant",
            kind="d7_eventbridge",
            resource_name=name,
            target_ids=[key_id, key_arn, grant_id],
            expected_event_names=["CreateGrant"],
            expected_event_source="kms.amazonaws.com",
            started_at_utc=t2,
            ended_at_utc=e2,
            api_call_succeeded=_http_ok(g_resp),
            details={"key_id": key_id, "grant_id": grant_id},
        )
        results.append(s2)
        ledger.record_event(["D7-kms-grant"], "kms:CreateGrant", resource_name=name, started_at_utc=t2, ended_at_utc=e2, details={"key_id": key_id, "grant_id": grant_id})

        # 3. DisableKey
        assert_throwaway_id_registered(key_id, owned_keys, "kms:DisableKey")
        _verify_kms_key_owned(kms, key_id, run_id, account_id)
        t3 = utc_now_iso()
        r3 = kms.disable_key(KeyId=key_id)
        e3 = utc_now_iso()
        s3 = _stim(
            "D7-kms-disable",
            "kms:DisableKey",
            kind="d7_eventbridge",
            resource_name=name,
            target_ids=[key_id, key_arn],
            expected_event_names=["DisableKey"],
            expected_event_source="kms.amazonaws.com",
            started_at_utc=t3,
            ended_at_utc=e3,
            api_call_succeeded=_http_ok(r3),
            details={"key_id": key_id},
        )
        results.append(s3)
        ledger.record_event(["D7-kms-disable"], "kms:DisableKey", resource_name=name, started_at_utc=t3, ended_at_utc=e3, details={"key_id": key_id})

        # 4. RevokeGrant before ScheduleKeyDeletion so no grant lingers on a scheduled key.
        if grant_id:
            _verify_kms_key_owned(kms, key_id, run_id, account_id)
            kms.revoke_grant(KeyId=key_id, GrantId=grant_id)
            ledger.record_deleted("kms_grant", grant_id, intent_id=grant_intent)
            grant_id = None

        # 5. ScheduleKeyDeletion (minimum 7-day window)
        assert_throwaway_id_registered(key_id, owned_keys, "kms:ScheduleKeyDeletion")
        _verify_kms_key_owned(kms, key_id, run_id, account_id)
        t4 = utc_now_iso()
        del_resp = kms.schedule_key_deletion(KeyId=key_id, PendingWindowInDays=7)
        e4 = utc_now_iso()
        deletion_scheduled = True
        del_date = del_resp["DeletionDate"].strftime("%Y-%m-%d")
        ledger.record_kms_scheduled_deletion(key_id, del_date, intent_id=key_intent)
        s4 = _stim(
            "D7-kms-delete",
            "kms:ScheduleKeyDeletion",
            kind="d7_eventbridge",
            resource_name=name,
            target_ids=[key_id, key_arn],
            expected_event_names=["ScheduleKeyDeletion"],
            expected_event_source="kms.amazonaws.com",
            started_at_utc=t4,
            ended_at_utc=e4,
            api_call_succeeded=_http_ok(del_resp),
            details={"key_id": key_id, "deletes_on": del_date},
        )
        results.append(s4)
        ledger.record_event(["D7-kms-delete"], "kms:ScheduleKeyDeletion", resource_name=name, started_at_utc=t4, ended_at_utc=e4, details={"key_id": key_id, "deletes_on": del_date})
    finally:
        if key_id and grant_id:
            try:
                assert_throwaway_id_registered(key_id, owned_keys, "kms:RevokeGrant")
                _verify_kms_key_owned(kms, key_id, run_id, account_id)
                kms.revoke_grant(KeyId=key_id, GrantId=grant_id)
                ledger.record_deleted("kms_grant", grant_id, intent_id=grant_intent, safe=True)
            except Exception as exc:
                ledger.record_deleted("kms_grant", grant_id, status="cleanup_failed", detail=safe_error_label(exc), intent_id=grant_intent, safe=True)
        if alias_intent:
            try:
                if _verify_kms_alias_owned(kms, alias_name, run_id, account_id) is not None:
                    kms.delete_alias(AliasName=alias_name)
                ledger.record_deleted("kms_alias", alias_name, intent_id=alias_intent, safe=True)
            except Exception as exc:
                ledger.record_deleted("kms_alias", alias_name, status="cleanup_failed", detail=safe_error_label(exc), intent_id=alias_intent, safe=True)
        if key_id and not deletion_scheduled:
            try:
                assert_throwaway_id_registered(key_id, owned_keys, "kms:ScheduleKeyDeletion")
                meta = _verify_kms_key_owned(kms, key_id, run_id, account_id)
                if meta.get("KeyState") == "PendingDeletion":
                    del_date = meta["DeletionDate"].strftime("%Y-%m-%d")
                else:
                    del_resp = kms.schedule_key_deletion(KeyId=key_id, PendingWindowInDays=7)
                    del_date = del_resp["DeletionDate"].strftime("%Y-%m-%d")
                ledger.record_kms_scheduled_deletion(key_id, del_date, intent_id=key_intent, safe=True)
            except Exception as exc:
                ledger.record_deleted("kms_key", key_id, status="cleanup_failed", detail=safe_error_label(exc), intent_id=key_intent, safe=True)
    return results


def run_d7_s3(run_id: str, ledger: RunLedger, *, session: Any = None) -> list[dict[str, Any]]:
    """D7-s3-policy-put, D7-s3-policy-delete, and D7-s3-lock on throwaway S3 buckets."""
    s3 = locked_boto3_client("s3", session=session)
    account_id, _ = get_caller_identity(session=session)
    bkt_policy = make_throwaway_name(run_id, "bkt")
    bkt_lock = make_throwaway_name(run_id, "lock-bkt")
    results: list[dict[str, Any]] = []

    # Part A: Bucket policy put & delete (distinct windows per Finding 18)
    bkt_intent = ledger.record_intent("s3_bucket", bkt_policy)
    created_policy_bkt = False
    try:
        assert_throwaway_name(bkt_policy, run_id=run_id)
        s3.create_bucket(
            Bucket=bkt_policy,
            CreateBucketConfiguration={"LocationConstraint": ALLOWED_REGION},
        )
        created_policy_bkt = True
        ledger.confirm_created(bkt_intent, bkt_policy)
        s3.put_bucket_tagging(
            Bucket=bkt_policy,
            ExpectedBucketOwner=account_id,
            Tagging={
                "TagSet": [
                    {"Key": PURPOSE_TAG_KEY, "Value": PURPOSE_TAG_VALUE},
                    {"Key": RUN_ID_TAG_KEY, "Value": run_id},
                ]
            },
        )
        _verify_s3_bucket_owned(s3, bkt_policy, run_id, account_id)

        policy_doc = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "TesseraDtestDenyInsecureTransport",
                    "Effect": "Deny",
                    "Principal": "*",
                    "Action": "s3:*",
                    "Resource": [
                        f"arn:aws:s3:::{bkt_policy}",
                        f"arn:aws:s3:::{bkt_policy}/*",
                    ],
                    "Condition": {"Bool": {"aws:SecureTransport": "false"}},
                }
            ],
        }
        t1 = utc_now_iso()
        r1 = s3.put_bucket_policy(
            Bucket=bkt_policy, Policy=json.dumps(policy_doc), ExpectedBucketOwner=account_id
        )
        e1 = utc_now_iso()
        results.append(
            _stim(
                "D7-s3-policy-put",
                "s3:PutBucketPolicy",
                kind="d7_eventbridge",
                resource_name=bkt_policy,
                target_ids=[bkt_policy, f"arn:aws:s3:::{bkt_policy}"],
                expected_event_names=["PutBucketPolicy"],
                expected_event_source="s3.amazonaws.com",
                started_at_utc=t1,
                ended_at_utc=e1,
                api_call_succeeded=_http_ok(r1),
            )
        )
        ledger.record_event(["D7-s3-policy-put"], "s3:PutBucketPolicy", resource_name=bkt_policy, started_at_utc=t1, ended_at_utc=e1)

        _verify_s3_bucket_owned(s3, bkt_policy, run_id, account_id)
        t_del = utc_now_iso()
        r_del = s3.delete_bucket_policy(Bucket=bkt_policy, ExpectedBucketOwner=account_id)
        e_del = utc_now_iso()
        results.append(
            _stim(
                "D7-s3-policy-delete",
                "s3:DeleteBucketPolicy",
                kind="d7_eventbridge",
                resource_name=bkt_policy,
                target_ids=[bkt_policy, f"arn:aws:s3:::{bkt_policy}"],
                expected_event_names=["DeleteBucketPolicy"],
                expected_event_source="s3.amazonaws.com",
                started_at_utc=t_del,
                ended_at_utc=e_del,
                api_call_succeeded=_http_ok(r_del),
            )
        )
        ledger.record_event(["D7-s3-policy-delete"], "s3:DeleteBucketPolicy", resource_name=bkt_policy, started_at_utc=t_del, ended_at_utc=e_del)
    finally:
        if created_policy_bkt:
            try:
                _verify_s3_bucket_owned(s3, bkt_policy, run_id, account_id)
                s3.delete_bucket(Bucket=bkt_policy, ExpectedBucketOwner=account_id)
                ledger.record_deleted("s3_bucket", bkt_policy, intent_id=bkt_intent, safe=True)
            except Exception as exc:
                ledger.record_deleted("s3_bucket", bkt_policy, status="cleanup_failed", detail=safe_error_label(exc), intent_id=bkt_intent, safe=True)

    # Part B: Object Lock configuration on an EMPTY throwaway bucket
    lock_intent = ledger.record_intent("s3_bucket", bkt_lock, metadata={"object_lock": True})
    created_lock_bkt = False
    try:
        assert_throwaway_name(bkt_lock, run_id=run_id)
        s3.create_bucket(
            Bucket=bkt_lock,
            CreateBucketConfiguration={"LocationConstraint": ALLOWED_REGION},
            ObjectLockEnabledForBucket=True,
        )
        created_lock_bkt = True
        ledger.confirm_created(lock_intent, bkt_lock)
        s3.put_bucket_tagging(
            Bucket=bkt_lock,
            ExpectedBucketOwner=account_id,
            Tagging={
                "TagSet": [
                    {"Key": PURPOSE_TAG_KEY, "Value": PURPOSE_TAG_VALUE},
                    {"Key": RUN_ID_TAG_KEY, "Value": run_id},
                ]
            },
        )
        _verify_s3_bucket_owned(s3, bkt_lock, run_id, account_id)
        t2 = utc_now_iso()
        r2 = s3.put_object_lock_configuration(
            Bucket=bkt_lock,
            ExpectedBucketOwner=account_id,
            ObjectLockConfiguration={
                "ObjectLockEnabled": "Enabled",
                "Rule": {"DefaultRetention": {"Mode": "GOVERNANCE", "Days": 1}},
            },
        )
        e2 = utc_now_iso()
        results.append(
            _stim(
                "D7-s3-lock",
                "s3:PutObjectLockConfiguration",
                kind="d7_eventbridge",
                resource_name=bkt_lock,
                target_ids=[bkt_lock, f"arn:aws:s3:::{bkt_lock}"],
                expected_event_names=["PutObjectLockConfiguration"],
                expected_event_source="s3.amazonaws.com",
                started_at_utc=t2,
                ended_at_utc=e2,
                api_call_succeeded=_http_ok(r2),
            )
        )
        ledger.record_event(["D7-s3-lock"], "s3:PutObjectLockConfiguration", resource_name=bkt_lock, started_at_utc=t2, ended_at_utc=e2)
    finally:
        if created_lock_bkt:
            try:
                _verify_s3_bucket_owned(s3, bkt_lock, run_id, account_id)
                s3.delete_bucket(Bucket=bkt_lock, ExpectedBucketOwner=account_id)
                ledger.record_deleted("s3_bucket", bkt_lock, intent_id=lock_intent, safe=True)
            except Exception as exc:
                ledger.record_deleted("s3_bucket", bkt_lock, status="cleanup_failed", detail=safe_error_label(exc), intent_id=lock_intent, safe=True)
    return results


def run_d7_sns(run_id: str, ledger: RunLedger, *, session: Any = None) -> list[dict[str, Any]]:
    """D7-sns-topic-attr (incl. Policy), D7-sns-sub-throwaway (Subscribe/Unsubscribe), D7-sns-topic-delete."""
    sns = locked_boto3_client("sns", session=session)
    sqs = locked_boto3_client("sqs", session=session)
    account_id, _ = get_caller_identity(session=session)
    topic_name = make_throwaway_name(run_id, "topic")
    sub_q_name = make_throwaway_name(run_id, "sns-sub-q")

    topic_intent = ledger.record_intent("sns_topic", topic_name)
    sub_q_intent: str | None = None
    topic_arn: str | None = None
    sub_q_url: str | None = None
    sub_arn: str | None = None
    topic_deleted = False
    results: list[dict[str, Any]] = []

    try:
        assert_throwaway_name(topic_name, run_id=run_id)
        resp = sns.create_topic(
            Name=topic_name,
            Tags=[
                {"Key": PURPOSE_TAG_KEY, "Value": PURPOSE_TAG_VALUE},
                {"Key": RUN_ID_TAG_KEY, "Value": run_id},
            ],
        )
        topic_arn = resp["TopicArn"]
        assert_throwaway_name(topic_arn, run_id=run_id, account_id=account_id)
        ledger.confirm_created(topic_intent, topic_arn)

        # 1. SetTopicAttributes (Policy change on throwaway topic — matches D7 topic-policy event)
        _verify_sns_topic_owned(sns, topic_arn, run_id, account_id)
        t_attr = utc_now_iso()
        topic_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "TesseraDtestOwnerOnly",
                    "Effect": "Allow",
                    "Principal": {"AWS": f"arn:aws:iam::{account_id}:root"},
                    "Action": "sns:GetTopicAttributes",
                    "Resource": topic_arn,
                }
            ],
        }
        r_attr = sns.set_topic_attributes(
            TopicArn=topic_arn,
            AttributeName="Policy",
            AttributeValue=json.dumps(topic_policy),
        )
        e_attr = utc_now_iso()
        results.append(
            _stim(
                "D7-sns-topic-attr",
                "sns:SetTopicAttributes (Policy)",
                kind="d7_eventbridge",
                resource_name=topic_name,
                target_ids=[topic_arn, topic_name],
                expected_event_names=["SetTopicAttributes"],
                expected_event_source="sns.amazonaws.com",
                started_at_utc=t_attr,
                ended_at_utc=e_attr,
                api_call_succeeded=_http_ok(r_attr),
            )
        )
        ledger.record_event(["D7-sns-topic-attr"], "sns:SetTopicAttributes (Policy)", resource_name=topic_name, started_at_utc=t_attr, ended_at_utc=e_attr)

        # 2. Throwaway topic Subscribe & Unsubscribe (observed while main observer is alive, Finding 18)
        sub_q_intent = ledger.record_intent("sqs_queue", sub_q_name)
        sub_q_url = sqs.create_queue(
            QueueName=sub_q_name,
            Attributes={"SqsManagedSseEnabled": "true"},
            tags={PURPOSE_TAG_KEY: PURPOSE_TAG_VALUE, RUN_ID_TAG_KEY: run_id},
        )["QueueUrl"]
        assert_throwaway_name(sub_q_url, run_id=run_id, account_id=account_id)
        ledger.confirm_created(sub_q_intent, sub_q_name)
        verify_owned_sqs_queue_live(sqs, sub_q_name, run_id, account_id)
        sub_q_arn = sqs.get_queue_attributes(QueueUrl=sub_q_url, AttributeNames=["QueueArn"])["Attributes"]["QueueArn"]
        assert_throwaway_name(sub_q_arn, run_id=run_id, account_id=account_id)

        _verify_sns_topic_owned(sns, topic_arn, run_id, account_id)
        t_sub = utc_now_iso()
        sub_resp = sns.subscribe(
            TopicArn=topic_arn,
            Protocol="sqs",
            Endpoint=sub_q_arn,
            ReturnSubscriptionArn=True,
        )
        e_sub = utc_now_iso()
        sub_arn = sub_resp["SubscriptionArn"]
        results.append(
            _stim(
                "D7-sns-sub-throwaway-subscribe",
                "sns:Subscribe (throwaway topic)",
                kind="d7_eventbridge",
                resource_name=topic_name,
                target_ids=[topic_arn, sub_q_arn, sub_arn],
                expected_event_names=["Subscribe"],
                expected_event_source="sns.amazonaws.com",
                started_at_utc=t_sub,
                ended_at_utc=e_sub,
                api_call_succeeded=_http_ok(sub_resp),
            )
        )
        ledger.record_event(["D7-sns-sub-throwaway-subscribe"], "sns:Subscribe (throwaway topic)", resource_name=topic_name, started_at_utc=t_sub, ended_at_utc=e_sub)

        _verify_sns_topic_owned(sns, topic_arn, run_id, account_id)
        t_unsub = utc_now_iso()
        r_unsub = sns.unsubscribe(SubscriptionArn=sub_arn)
        e_unsub = utc_now_iso()
        sub_arn = None
        results.append(
            _stim(
                "D7-sns-sub-throwaway-unsubscribe",
                "sns:Unsubscribe (throwaway topic)",
                kind="d7_eventbridge",
                resource_name=topic_name,
                target_ids=[topic_arn, sub_q_arn],
                expected_event_names=["Unsubscribe"],
                expected_event_source="sns.amazonaws.com",
                started_at_utc=t_unsub,
                ended_at_utc=e_unsub,
                api_call_succeeded=_http_ok(r_unsub),
            )
        )
        ledger.record_event(["D7-sns-sub-throwaway-unsubscribe"], "sns:Unsubscribe (throwaway topic)", resource_name=topic_name, started_at_utc=t_unsub, ended_at_utc=e_unsub)

        # 3. DeleteTopic (explicitly timed window)
        _verify_sns_topic_owned(sns, topic_arn, run_id, account_id)
        t_del = utc_now_iso()
        r_del = sns.delete_topic(TopicArn=topic_arn)
        e_del = utc_now_iso()
        topic_deleted = True
        ledger.record_deleted("sns_topic", topic_arn, intent_id=topic_intent)
        results.append(
            _stim(
                "D7-sns-topic-delete",
                "sns:DeleteTopic",
                kind="d7_eventbridge",
                resource_name=topic_name,
                target_ids=[topic_arn, topic_name],
                expected_event_names=["DeleteTopic"],
                expected_event_source="sns.amazonaws.com",
                started_at_utc=t_del,
                ended_at_utc=e_del,
                api_call_succeeded=_http_ok(r_del),
            )
        )
        ledger.record_event(["D7-sns-topic-delete"], "sns:DeleteTopic", resource_name=topic_name, started_at_utc=t_del, ended_at_utc=e_del)
    finally:
        if sub_arn and topic_arn:
            try:
                _verify_sns_topic_owned(sns, topic_arn, run_id, account_id)
                sns.unsubscribe(SubscriptionArn=sub_arn)
            except Exception as exc:
                ledger.add_note(f"throwaway sns:Unsubscribe failed: {safe_error_label(exc)}", safe=True)
        if topic_arn and not topic_deleted:
            try:
                _verify_sns_topic_owned(sns, topic_arn, run_id, account_id)
                sns.delete_topic(TopicArn=topic_arn)
                ledger.record_deleted("sns_topic", topic_arn, intent_id=topic_intent, safe=True)
            except Exception as exc:
                ledger.record_deleted("sns_topic", topic_arn, status="cleanup_failed", detail=safe_error_label(exc), intent_id=topic_intent, safe=True)
        if sub_q_url or sub_q_intent:
            try:
                verified_url = verify_owned_sqs_queue_live(sqs, sub_q_name, run_id, account_id)
                sqs.delete_queue(QueueUrl=verified_url)
                ledger.record_deleted("sqs_queue", sub_q_name, intent_id=sub_q_intent, safe=True)
            except Exception as exc:
                if _is_not_found(exc):
                    ledger.record_deleted("sqs_queue", sub_q_name, intent_id=sub_q_intent, safe=True)
                else:
                    ledger.record_deleted("sqs_queue", sub_q_name, status="cleanup_failed", detail=safe_error_label(exc), intent_id=sub_q_intent, safe=True)
    return results


def run_d7_apigw(run_id: str, ledger: RunLedger, *, session: Any = None) -> list[dict[str, Any]]:
    """D7-apigw-key and D7-apigw-plan with per-action windows and live ownership checks."""
    apigw = locked_boto3_client("apigateway", session=session)
    api_name = make_throwaway_name(run_id, "api")
    key_name = make_throwaway_name(run_id, "key")
    plan_name = make_throwaway_name(run_id, "plan")

    owned_apis: set[str] = set()
    owned_keys: set[str] = set()
    owned_plans: set[str] = set()

    api_intent = ledger.record_intent("apigw_rest_api", api_name)
    key_intent: str | None = None
    plan_intent: str | None = None
    attach_intent: str | None = None

    api_id: str | None = None
    key_id: str | None = None
    plan_id: str | None = None
    plan_key_attached = False
    results: list[dict[str, Any]] = []

    try:
        api_resp = apigw.create_rest_api(
            name=api_name,
            description="Throwaway Tessera detection test API",
            tags={PURPOSE_TAG_KEY: PURPOSE_TAG_VALUE, RUN_ID_TAG_KEY: run_id},
        )
        api_id = api_resp["id"]
        owned_apis.add(api_id)
        ledger.confirm_created(api_intent, api_id)

        key_intent = ledger.record_intent("apigw_api_key", key_name)
        t_ck = utc_now_iso()
        key_resp = apigw.create_api_key(
            name=key_name,
            description="Throwaway detection test key",
            enabled=False,
            tags={PURPOSE_TAG_KEY: PURPOSE_TAG_VALUE, RUN_ID_TAG_KEY: run_id},
        )
        e_ck = utc_now_iso()
        key_id = key_resp["id"]
        owned_keys.add(key_id)
        ledger.confirm_created(key_intent, key_id)

        assert_throwaway_id_registered(key_id, owned_keys, "apigateway:UpdateApiKey")
        _verify_apigw_api_key_owned(apigw, key_id, run_id)
        t_uk = utc_now_iso()
        r_uk = apigw.update_api_key(
            apiKey=key_id,
            patchOperations=[{"op": "replace", "path": "/description", "value": "updated-dtest"}],
        )
        e_uk = utc_now_iso()
        results.append(
            _stim(
                "D7-apigw-key-create",
                "apigateway:CreateApiKey",
                kind="d7_eventbridge",
                resource_name=key_name,
                target_ids=[key_id, key_name],
                expected_event_names=["CreateApiKey"],
                expected_event_source="apigateway.amazonaws.com",
                started_at_utc=t_ck,
                ended_at_utc=e_ck,
                api_call_succeeded=_http_ok(key_resp),
            )
        )
        results.append(
            _stim(
                "D7-apigw-key-update",
                "apigateway:UpdateApiKey",
                kind="d7_eventbridge",
                resource_name=key_name,
                target_ids=[key_id, key_name],
                expected_event_names=["UpdateApiKey"],
                expected_event_source="apigateway.amazonaws.com",
                started_at_utc=t_uk,
                ended_at_utc=e_uk,
                api_call_succeeded=_http_ok(r_uk),
            )
        )
        ledger.record_event(["D7-apigw-key-create", "D7-apigw-key-update"], "apigateway:CreateApiKey + UpdateApiKey", resource_name=key_name, started_at_utc=t_ck, ended_at_utc=e_uk, details={"key_id": key_id})

        plan_intent = ledger.record_intent("apigw_usage_plan", plan_name)
        t_cp = utc_now_iso()
        plan_resp = apigw.create_usage_plan(
            name=plan_name,
            description="Throwaway detection test usage plan",
            throttle={"rateLimit": 1.0, "burstLimit": 1},
            tags={PURPOSE_TAG_KEY: PURPOSE_TAG_VALUE, RUN_ID_TAG_KEY: run_id},
        )
        e_cp = utc_now_iso()
        plan_id = plan_resp["id"]
        owned_plans.add(plan_id)
        ledger.confirm_created(plan_intent, plan_id)

        assert_throwaway_id_registered(plan_id, owned_plans, "apigateway:UpdateUsagePlan")
        _verify_apigw_usage_plan_owned(apigw, plan_id, run_id)
        t_up = utc_now_iso()
        r_up = apigw.update_usage_plan(
            usagePlanId=plan_id,
            patchOperations=[{"op": "replace", "path": "/description", "value": "updated-dtest"}],
        )
        e_up = utc_now_iso()

        # Verify BOTH plan and key live before attaching (Finding 5)
        _verify_apigw_usage_plan_owned(apigw, plan_id, run_id)
        _verify_apigw_api_key_owned(apigw, key_id, run_id)
        attach_intent = ledger.record_intent(
            "apigw_usage_plan_key", f"{plan_name}:{key_name}", metadata={"plan_id": plan_id, "key_id": key_id}
        )
        t_att = utc_now_iso()
        r_att = apigw.create_usage_plan_key(usagePlanId=plan_id, keyId=key_id, keyType="API_KEY")
        e_att = utc_now_iso()
        plan_key_attached = True
        ledger.confirm_created(attach_intent, f"{plan_id}:{key_id}")

        results.append(
            _stim(
                "D7-apigw-plan-update",
                "apigateway:UpdateUsagePlan",
                kind="d7_eventbridge",
                resource_name=plan_name,
                target_ids=[plan_id, plan_name],
                expected_event_names=["UpdateUsagePlan"],
                expected_event_source="apigateway.amazonaws.com",
                started_at_utc=t_up,
                ended_at_utc=e_up,
                api_call_succeeded=_http_ok(r_up),
            )
        )
        results.append(
            _stim(
                "D7-apigw-plan-key",
                "apigateway:CreateUsagePlanKey",
                kind="d7_eventbridge",
                resource_name=plan_name,
                target_ids=[plan_id, key_id],
                expected_event_names=["CreateUsagePlanKey"],
                expected_event_source="apigateway.amazonaws.com",
                started_at_utc=t_att,
                ended_at_utc=e_att,
                api_call_succeeded=_http_ok(r_att),
            )
        )
        ledger.record_event(["D7-apigw-plan-update", "D7-apigw-plan-key"], "apigateway:CreateUsagePlan + UpdateUsagePlan + CreateUsagePlanKey", resource_name=plan_name, started_at_utc=t_cp, ended_at_utc=e_att, details={"plan_id": plan_id, "api_id": api_id})
    finally:
        if plan_key_attached and plan_id and key_id:
            try:
                assert_throwaway_id_registered(plan_id, owned_plans, "apigateway:DeleteUsagePlanKey")
                assert_throwaway_id_registered(key_id, owned_keys, "apigateway:DeleteUsagePlanKey")
                _verify_apigw_usage_plan_owned(apigw, plan_id, run_id)
                _verify_apigw_api_key_owned(apigw, key_id, run_id)
                apigw.delete_usage_plan_key(usagePlanId=plan_id, keyId=key_id)
                ledger.record_deleted("apigw_usage_plan_key", f"{plan_id}:{key_id}", intent_id=attach_intent, safe=True)
            except Exception as exc:
                ledger.record_deleted("apigw_usage_plan_key", f"{plan_id}:{key_id}", status="cleanup_failed", detail=safe_error_label(exc), intent_id=attach_intent, safe=True)
        if plan_id:
            try:
                assert_throwaway_id_registered(plan_id, owned_plans, "apigateway:DeleteUsagePlan")
                _verify_apigw_usage_plan_owned(apigw, plan_id, run_id)
                apigw.delete_usage_plan(usagePlanId=plan_id)
                ledger.record_deleted("apigw_usage_plan", plan_id, intent_id=plan_intent, safe=True)
            except Exception as exc:
                ledger.record_deleted("apigw_usage_plan", plan_id, status="cleanup_failed", detail=safe_error_label(exc), intent_id=plan_intent, safe=True)
        if key_id:
            try:
                assert_throwaway_id_registered(key_id, owned_keys, "apigateway:DeleteApiKey")
                _verify_apigw_api_key_owned(apigw, key_id, run_id)
                apigw.delete_api_key(apiKey=key_id)
                ledger.record_deleted("apigw_api_key", key_id, intent_id=key_intent, safe=True)
            except Exception as exc:
                ledger.record_deleted("apigw_api_key", key_id, status="cleanup_failed", detail=safe_error_label(exc), intent_id=key_intent, safe=True)
        if api_id:
            try:
                assert_throwaway_id_registered(api_id, owned_apis, "apigateway:DeleteRestApi")
                _verify_apigw_rest_api_owned(apigw, api_id, run_id)
                apigw.delete_rest_api(restApiId=api_id)
                ledger.record_deleted("apigw_rest_api", api_id, intent_id=api_intent, safe=True)
            except Exception as exc:
                ledger.record_deleted("apigw_rest_api", api_id, status="cleanup_failed", detail=safe_error_label(exc), intent_id=api_intent, safe=True)
    return results


def run_d7_lambda(run_id: str, ledger: RunLedger, *, session: Any = None) -> list[dict[str, Any]]:
    """D7-lambda-config, D7-lambda-code, and D7-sup-lambda-perm on a throwaway Lambda."""
    iam = locked_boto3_client("iam", session=session, allow_global_iam=True)
    lam = locked_boto3_client("lambda", session=session)
    account_id, _ = get_caller_identity(session=session)
    role_name = make_throwaway_name(run_id, "fn-role")
    fn_name = make_throwaway_name(run_id, "fn")
    dummy_bkt_arn = f"arn:aws:s3:::{make_throwaway_name(run_id, 'dummy-src')}"

    role_intent = ledger.record_intent("iam_role", role_name)
    fn_intent: str | None = None
    perm_intent: str | None = None
    role_created = False
    fn_created = False
    results: list[dict[str, Any]] = []

    try:
        trust = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": "lambda.amazonaws.com"},
                    "Action": "sts:AssumeRole",
                }
            ],
        }
        r_resp = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust),
            Description="Zero-permission throwaway Lambda role for Tessera detection test",
            Tags=[
                {"Key": PURPOSE_TAG_KEY, "Value": PURPOSE_TAG_VALUE},
                {"Key": RUN_ID_TAG_KEY, "Value": run_id},
            ],
        )
        role_arn = r_resp["Role"]["Arn"]
        role_created = True
        ledger.confirm_created(role_intent, role_name, metadata={"role_arn": role_arn})

        time.sleep(10.0)

        fn_intent = ledger.record_intent("lambda_function", fn_name)
        lam.create_function(
            FunctionName=fn_name,
            Runtime="python3.12",
            Role=role_arn,
            Handler="index.handler",
            Code={"ZipFile": _make_noop_lambda_zip("v1")},
            Description="Throwaway Tessera detection test function",
            Timeout=3,
            MemorySize=128,
            Tags={PURPOSE_TAG_KEY: PURPOSE_TAG_VALUE, RUN_ID_TAG_KEY: run_id},
        )
        fn_created = True
        ledger.confirm_created(fn_intent, fn_name)
        _wait_lambda_ready(lam, fn_name)

        # 1. UpdateFunctionConfiguration
        _verify_lambda_owned(lam, fn_name, run_id, account_id)
        t_cfg = utc_now_iso()
        r_cfg = lam.update_function_configuration(FunctionName=fn_name, Timeout=4)
        e_cfg = utc_now_iso()
        results.append(
            _stim(
                "D7-lambda-config",
                "lambda:UpdateFunctionConfiguration",
                kind="d7_eventbridge",
                resource_name=fn_name,
                target_ids=[fn_name, f"arn:aws:lambda:{ALLOWED_REGION}:{account_id}:function:{fn_name}"],
                expected_event_names=["UpdateFunctionConfiguration"],
                expected_event_source="lambda.amazonaws.com",
                started_at_utc=t_cfg,
                ended_at_utc=e_cfg,
                api_call_succeeded=_http_ok(r_cfg),
            )
        )
        ledger.record_event(["D7-lambda-config"], "lambda:UpdateFunctionConfiguration", resource_name=fn_name, started_at_utc=t_cfg, ended_at_utc=e_cfg)
        _wait_lambda_ready(lam, fn_name)

        # 2. UpdateFunctionCode
        _verify_lambda_owned(lam, fn_name, run_id, account_id)
        t_code = utc_now_iso()
        r_code = lam.update_function_code(FunctionName=fn_name, ZipFile=_make_noop_lambda_zip("v2"))
        e_code = utc_now_iso()
        results.append(
            _stim(
                "D7-lambda-code",
                "lambda:UpdateFunctionCode",
                kind="d7_eventbridge",
                resource_name=fn_name,
                target_ids=[fn_name, f"arn:aws:lambda:{ALLOWED_REGION}:{account_id}:function:{fn_name}"],
                expected_event_names=["UpdateFunctionCode"],
                expected_event_source="lambda.amazonaws.com",
                started_at_utc=t_code,
                ended_at_utc=e_code,
                api_call_succeeded=_http_ok(r_code),
            )
        )
        ledger.record_event(["D7-lambda-code"], "lambda:UpdateFunctionCode", resource_name=fn_name, started_at_utc=t_code, ended_at_utc=e_code)
        _wait_lambda_ready(lam, fn_name)

        # 3. AddPermission (supplementary)
        _verify_lambda_owned(lam, fn_name, run_id, account_id)
        perm_intent = ledger.record_intent("lambda_permission", f"{fn_name}:tessera-dtest-perm")
        t_perm = utc_now_iso()
        r_perm = lam.add_permission(
            FunctionName=fn_name,
            StatementId="tessera-dtest-perm",
            Action="lambda:InvokeFunction",
            Principal="s3.amazonaws.com",
            SourceArn=dummy_bkt_arn,
        )
        e_perm = utc_now_iso()
        ledger.confirm_created(perm_intent, f"{fn_name}:tessera-dtest-perm")
        results.append(
            _stim(
                "D7-sup-lambda-perm",
                "lambda:AddPermission",
                kind="d7_eventbridge",
                resource_name=fn_name,
                target_ids=[fn_name, "tessera-dtest-perm"],
                expected_event_names=["AddPermission"],
                expected_event_source="lambda.amazonaws.com",
                started_at_utc=t_perm,
                ended_at_utc=e_perm,
                api_call_succeeded=_http_ok(r_perm),
            )
        )
        ledger.record_event(["D7-sup-lambda-perm"], "lambda:AddPermission", resource_name=fn_name, started_at_utc=t_perm, ended_at_utc=e_perm)

        _verify_lambda_owned(lam, fn_name, run_id, account_id)
        lam.remove_permission(FunctionName=fn_name, StatementId="tessera-dtest-perm")
        ledger.record_deleted("lambda_permission", f"{fn_name}:tessera-dtest-perm", intent_id=perm_intent)
    finally:
        if fn_created:
            try:
                _verify_lambda_owned(lam, fn_name, run_id, account_id)
                lam.delete_function(FunctionName=fn_name)
                ledger.record_deleted("lambda_function", fn_name, intent_id=fn_intent, safe=True)
            except Exception as exc:
                ledger.record_deleted("lambda_function", fn_name, status="cleanup_failed", detail=safe_error_label(exc), intent_id=fn_intent, safe=True)
        if role_created:
            try:
                _verify_iam_role_owned(iam, role_name, run_id, account_id)
                iam.delete_role(RoleName=role_name)
                ledger.record_deleted("iam_role", role_name, intent_id=role_intent, safe=True)
            except Exception as exc:
                ledger.record_deleted("iam_role", role_name, status="cleanup_failed", detail=safe_error_label(exc), intent_id=role_intent, safe=True)
    return results


def run_d7_iam_role(run_id: str, ledger: RunLedger, *, session: Any = None) -> list[dict[str, Any]]:
    """D7-iam-role (global IAM via watcher multi-region trail, contract latency up to 1 h)."""
    iam = locked_boto3_client("iam", session=session, allow_global_iam=True)
    account_id, _ = get_caller_identity(session=session)
    role_name = make_throwaway_name(run_id, "role")
    policy_name = make_throwaway_name(run_id, "inline")

    role_intent = ledger.record_intent("iam_role", role_name)
    pol_intent: str | None = None
    role_created = False
    policy_attached = False
    results: list[dict[str, Any]] = []

    try:
        trust = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Deny",
                    "Principal": {"Service": "lambda.amazonaws.com"},
                    "Action": "sts:AssumeRole",
                }
            ],
        }
        t_cr = utc_now_iso()
        r_resp = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust),
            Description="Throwaway IAM role for Tessera D7 watcher detection test",
            Tags=[
                {"Key": PURPOSE_TAG_KEY, "Value": PURPOSE_TAG_VALUE},
                {"Key": RUN_ID_TAG_KEY, "Value": run_id},
            ],
        )
        e_cr = utc_now_iso()
        role_created = True
        role_arn = r_resp["Role"]["Arn"]
        ledger.confirm_created(role_intent, role_name, metadata={"role_arn": role_arn})

        _verify_iam_role_owned(iam, role_name, run_id, account_id)
        deny_all = {
            "Version": "2012-10-17",
            "Statement": [{"Effect": "Deny", "Action": "*", "Resource": "*"}],
        }
        pol_intent = ledger.record_intent("iam_role_policy", f"{role_name}:{policy_name}")
        t_put = utc_now_iso()
        r_put = iam.put_role_policy(
            RoleName=role_name,
            PolicyName=policy_name,
            PolicyDocument=json.dumps(deny_all),
        )
        e_put = utc_now_iso()
        policy_attached = True
        ledger.confirm_created(pol_intent, f"{role_name}:{policy_name}")

        _verify_iam_role_owned(iam, role_name, run_id, account_id)
        t_delp = utc_now_iso()
        r_delp = iam.delete_role_policy(RoleName=role_name, PolicyName=policy_name)
        e_delp = utc_now_iso()
        policy_attached = False
        ledger.record_deleted("iam_role_policy", f"{role_name}:{policy_name}", intent_id=pol_intent)

        results.append(
            _stim(
                "D7-iam-role-put-policy",
                "iam:PutRolePolicy (throwaway role, global IAM -> watcher trail)",
                kind="d7_watcher_iam",
                resource_name=role_name,
                target_ids=[role_name, role_arn, policy_name],
                expected_event_names=["PutRolePolicy"],
                expected_event_source="iam.amazonaws.com",
                started_at_utc=t_put,
                ended_at_utc=e_put,
                api_call_succeeded=_http_ok(r_put),
                contract_latency_s=3600,
            )
        )
        results.append(
            _stim(
                "D7-iam-role-delete-policy",
                "iam:DeleteRolePolicy (throwaway role, global IAM -> watcher trail)",
                kind="d7_watcher_iam",
                resource_name=role_name,
                target_ids=[role_name, role_arn, policy_name],
                expected_event_names=["DeleteRolePolicy"],
                expected_event_source="iam.amazonaws.com",
                started_at_utc=t_delp,
                ended_at_utc=e_delp,
                api_call_succeeded=_http_ok(r_delp),
                contract_latency_s=3600,
            )
        )
        ledger.record_event(
            ["D7-iam-role-put-policy", "D7-iam-role-delete-policy"],
            "iam:CreateRole + PutRolePolicy + DeleteRolePolicy + DeleteRole",
            resource_name=role_name,
            started_at_utc=t_cr,
            ended_at_utc=e_delp,
            details={"note": "Global IAM writes are read by watcher from multi-region trail (up to 1 h)."},
        )
    finally:
        if policy_attached:
            try:
                _verify_iam_role_owned(iam, role_name, run_id, account_id)
                iam.delete_role_policy(RoleName=role_name, PolicyName=policy_name)
                ledger.record_deleted("iam_role_policy", f"{role_name}:{policy_name}", intent_id=pol_intent, safe=True)
            except Exception as exc:
                ledger.record_deleted("iam_role_policy", f"{role_name}:{policy_name}", status="cleanup_failed", detail=safe_error_label(exc), intent_id=pol_intent, safe=True)
        if role_created:
            try:
                _verify_iam_role_owned(iam, role_name, run_id, account_id)
                iam.delete_role(RoleName=role_name)
                ledger.record_deleted("iam_role", role_name, intent_id=role_intent, safe=True)
            except Exception as exc:
                ledger.record_deleted("iam_role", role_name, status="cleanup_failed", detail=safe_error_label(exc), intent_id=role_intent, safe=True)
    return results


def run_d7_iam_access_key(run_id: str, ledger: RunLedger, *, session: Any = None) -> list[dict[str, Any]]:
    """D7-iam-accesskey (opt-in): durable intent before create, live enumerate-and-delete in finally.

    Hard Safety Rule 5: AccessKeyId and SecretAccessKey are NEVER printed, logged,
    or written to the ledger.
    """
    iam = locked_boto3_client("iam", session=session, allow_global_iam=True)
    account_id, _ = get_caller_identity(session=session)
    user_name = make_throwaway_name(run_id, "user")

    user_intent = ledger.record_intent("iam_user", user_name)
    key_intent: str | None = None
    user_created = False
    results: list[dict[str, Any]] = []

    try:
        u_resp = iam.create_user(
            UserName=user_name,
            Tags=[
                {"Key": PURPOSE_TAG_KEY, "Value": PURPOSE_TAG_VALUE},
                {"Key": RUN_ID_TAG_KEY, "Value": run_id},
            ],
        )
        user_created = True
        user_arn = u_resp["User"]["Arn"]
        ledger.confirm_created(user_intent, user_name, metadata={"user_arn": user_arn})

        _verify_iam_user_owned(iam, user_name, run_id, account_id)
        # Durable intent keyed ONLY by user_name (zero credential material recorded, Finding 12).
        key_intent = ledger.record_intent(
            "iam_access_key",
            user_name,
            metadata={"credential_material_logged": False},
        )
        t_ak = utc_now_iso()
        ak_resp = iam.create_access_key(UserName=user_name)
        e_ak = utc_now_iso()
        ak_ok = _http_ok(ak_resp)
        # Immediately clear returned credential material in memory.
        if isinstance(ak_resp, dict):
            if isinstance(ak_resp.get("AccessKey"), dict):
                ak_resp["AccessKey"].clear()
            ak_resp.clear()
        ledger.confirm_created(key_intent, user_name)

        results.append(
            _stim(
                "D7-iam-accesskey",
                "iam:CreateAccessKey (zero-perm throwaway user, global IAM -> watcher trail)",
                kind="d7_watcher_iam",
                resource_name=user_name,
                target_ids=[user_name, user_arn],
                expected_event_names=["CreateAccessKey"],
                expected_event_source="iam.amazonaws.com",
                started_at_utc=t_ak,
                ended_at_utc=e_ak,
                api_call_succeeded=ak_ok,
                contract_latency_s=3600,
                details={"credential_material_logged": False},
            )
        )
        ledger.record_event(
            ["D7-iam-accesskey"],
            "iam:CreateAccessKey (zero-perm throwaway user)",
            resource_name=user_name,
            started_at_utc=t_ak,
            ended_at_utc=e_ak,
            details={"credential_material_logged": False},
        )
    finally:
        if user_created:
            # Always enumerate live access keys on the verified throwaway user so even a lost
            # create_access_key response cannot strand an active credential (Finding 12).
            keys_cleaned = True
            try:
                _verify_iam_user_owned(iam, user_name, run_id, account_id)
                for meta in iam.list_access_keys(UserName=user_name).get("AccessKeyMetadata", []):
                    iam.delete_access_key(UserName=user_name, AccessKeyId=meta["AccessKeyId"])
                remaining = iam.list_access_keys(UserName=user_name).get("AccessKeyMetadata", [])
                if remaining:
                    keys_cleaned = False
                    if key_intent:
                        ledger.record_deleted(
                            "iam_access_key", user_name, status="cleanup_failed",
                            detail="ResidualAccessKey", intent_id=key_intent, safe=True,
                        )
                elif key_intent:
                    ledger.record_deleted("iam_access_key", user_name, intent_id=key_intent, safe=True)
            except Exception as exc:
                keys_cleaned = False
                if key_intent:
                    ledger.record_deleted(
                        "iam_access_key", user_name, status="cleanup_failed",
                        detail=safe_error_label(exc), intent_id=key_intent, safe=True,
                    )

            if keys_cleaned:
                try:
                    _verify_iam_user_owned(iam, user_name, run_id, account_id)
                    iam.delete_user(UserName=user_name)
                    ledger.record_deleted("iam_user", user_name, intent_id=user_intent, safe=True)
                except Exception as exc:
                    ledger.record_deleted(
                        "iam_user", user_name, status="cleanup_failed",
                        detail=safe_error_label(exc), intent_id=user_intent, safe=True,
                    )
            else:
                ledger.record_deleted(
                    "iam_user", user_name, status="cleanup_failed",
                    detail="AccessKeyCleanupFailed", intent_id=user_intent, safe=True,
                )
    return results


def run_d7_cloudtrail(run_id: str, ledger: RunLedger, *, session: Any = None) -> list[dict[str, Any]]:
    """D7-ct-update, D7-ct-selectors, D7-ct-stop (API call only; trail never started), D7-ct-delete."""
    s3 = locked_boto3_client("s3", session=session)
    ct = locked_boto3_client("cloudtrail", session=session)
    account_id, _ = get_caller_identity(session=session)
    bkt_name = make_throwaway_name(run_id, "ct-bkt")
    trail_name = make_throwaway_name(run_id, "trail")
    trail_arn = f"arn:aws:cloudtrail:{ALLOWED_REGION}:{account_id}:trail/{trail_name}"

    bkt_intent = ledger.record_intent("s3_bucket", bkt_name)
    trail_intent: str | None = None
    bkt_created = False
    trail_created = False
    trail_deleted = False
    results: list[dict[str, Any]] = []

    try:
        s3.create_bucket(
            Bucket=bkt_name,
            CreateBucketConfiguration={"LocationConstraint": ALLOWED_REGION},
        )
        bkt_created = True
        ledger.confirm_created(bkt_intent, bkt_name)
        s3.put_bucket_tagging(
            Bucket=bkt_name,
            ExpectedBucketOwner=account_id,
            Tagging={
                "TagSet": [
                    {"Key": PURPOSE_TAG_KEY, "Value": PURPOSE_TAG_VALUE},
                    {"Key": RUN_ID_TAG_KEY, "Value": run_id},
                ]
            },
        )
        _verify_s3_bucket_owned(s3, bkt_name, run_id, account_id)

        ct_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "AWSCloudTrailAclCheck",
                    "Effect": "Allow",
                    "Principal": {"Service": "cloudtrail.amazonaws.com"},
                    "Action": "s3:GetBucketAcl",
                    "Resource": f"arn:aws:s3:::{bkt_name}",
                    "Condition": {"StringEquals": {"aws:SourceArn": trail_arn}},
                },
                {
                    "Sid": "AWSCloudTrailWrite",
                    "Effect": "Allow",
                    "Principal": {"Service": "cloudtrail.amazonaws.com"},
                    "Action": "s3:PutObject",
                    "Resource": f"arn:aws:s3:::{bkt_name}/AWSLogs/{account_id}/*",
                    "Condition": {
                        "StringEquals": {
                            "s3:x-amz-acl": "bucket-owner-full-control",
                            "aws:SourceArn": trail_arn,
                        }
                    },
                },
            ],
        }
        s3.put_bucket_policy(Bucket=bkt_name, Policy=json.dumps(ct_policy), ExpectedBucketOwner=account_id)

        trail_intent = ledger.record_intent("cloudtrail", trail_name)
        ct.create_trail(
            Name=trail_name,
            S3BucketName=bkt_name,
            IsMultiRegionTrail=False,
            TagsList=[
                {"Key": PURPOSE_TAG_KEY, "Value": PURPOSE_TAG_VALUE},
                {"Key": RUN_ID_TAG_KEY, "Value": run_id},
            ],
        )
        trail_created = True
        ledger.confirm_created(trail_intent, trail_name, metadata={"trail_arn": trail_arn})

        _verify_cloudtrail_owned(ct, trail_name, run_id, account_id)
        t_upd = utc_now_iso()
        r_upd = ct.update_trail(Name=trail_name, EnableLogFileValidation=True)
        e_upd = utc_now_iso()
        results.append(
            _stim(
                "D7-ct-update",
                "cloudtrail:UpdateTrail",
                kind="d7_eventbridge",
                resource_name=trail_name,
                target_ids=[trail_name, trail_arn],
                expected_event_names=["UpdateTrail"],
                expected_event_source="cloudtrail.amazonaws.com",
                started_at_utc=t_upd,
                ended_at_utc=e_upd,
                api_call_succeeded=_http_ok(r_upd),
            )
        )
        ledger.record_event(["D7-ct-update"], "cloudtrail:UpdateTrail", resource_name=trail_name, started_at_utc=t_upd, ended_at_utc=e_upd)

        _verify_cloudtrail_owned(ct, trail_name, run_id, account_id)
        t_sel = utc_now_iso()
        r_sel = ct.put_event_selectors(
            TrailName=trail_name,
            EventSelectors=[{"ReadWriteType": "ReadOnly", "IncludeManagementEvents": True}],
        )
        e_sel = utc_now_iso()
        results.append(
            _stim(
                "D7-ct-selectors",
                "cloudtrail:PutEventSelectors",
                kind="d7_eventbridge",
                resource_name=trail_name,
                target_ids=[trail_name, trail_arn],
                expected_event_names=["PutEventSelectors"],
                expected_event_source="cloudtrail.amazonaws.com",
                started_at_utc=t_sel,
                ended_at_utc=e_sel,
                api_call_succeeded=_http_ok(r_sel),
            )
        )
        ledger.record_event(["D7-ct-selectors"], "cloudtrail:PutEventSelectors", resource_name=trail_name, started_at_utc=t_sel, ended_at_utc=e_sel)

        # Finding 11: record honest logging status before/after StopLogging (trail was never started).
        _verify_cloudtrail_owned(ct, trail_name, run_id, account_id)
        before_logging = bool(ct.get_trail_status(Name=trail_name).get("IsLogging", False))
        t_stop = utc_now_iso()
        r_stop = ct.stop_logging(Name=trail_name)
        e_stop = utc_now_iso()
        after_logging = bool(ct.get_trail_status(Name=trail_name).get("IsLogging", False))
        results.append(
            _stim(
                "D7-ct-stop",
                "cloudtrail:StopLogging (API call on unstarted throwaway trail; does not stop active log delivery)",
                kind="d7_eventbridge",
                resource_name=trail_name,
                target_ids=[trail_name, trail_arn],
                expected_event_names=["StopLogging"],
                expected_event_source="cloudtrail.amazonaws.com",
                started_at_utc=t_stop,
                ended_at_utc=e_stop,
                api_call_succeeded=_http_ok(r_stop),
                details={
                    "was_logging_before_stop": before_logging,
                    "is_logging_after_stop": after_logging,
                    "scope_note": "Exercises detection of cloudtrail:StopLogging API call only.",
                },
            )
        )
        ledger.record_event(["D7-ct-stop"], "cloudtrail:StopLogging (unstarted trail)", resource_name=trail_name, started_at_utc=t_stop, ended_at_utc=e_stop, details={"was_logging_before_stop": before_logging, "is_logging_after_stop": after_logging})

        _verify_cloudtrail_owned(ct, trail_name, run_id, account_id)
        t_del = utc_now_iso()
        r_del = ct.delete_trail(Name=trail_name)
        e_del = utc_now_iso()
        trail_deleted = True
        ledger.record_deleted("cloudtrail", trail_name, intent_id=trail_intent)
        results.append(
            _stim(
                "D7-ct-delete",
                "cloudtrail:DeleteTrail",
                kind="d7_eventbridge",
                resource_name=trail_name,
                target_ids=[trail_name, trail_arn],
                expected_event_names=["DeleteTrail"],
                expected_event_source="cloudtrail.amazonaws.com",
                started_at_utc=t_del,
                ended_at_utc=e_del,
                api_call_succeeded=_http_ok(r_del),
            )
        )
        ledger.record_event(["D7-ct-delete"], "cloudtrail:DeleteTrail", resource_name=trail_name, started_at_utc=t_del, ended_at_utc=e_del)
    finally:
        if trail_created and not trail_deleted:
            try:
                _verify_cloudtrail_owned(ct, trail_name, run_id, account_id)
                ct.delete_trail(Name=trail_name)
                ledger.record_deleted("cloudtrail", trail_name, intent_id=trail_intent, safe=True)
            except Exception as exc:
                ledger.record_deleted("cloudtrail", trail_name, status="cleanup_failed", detail=safe_error_label(exc), intent_id=trail_intent, safe=True)
        if bkt_created:
            try:
                _empty_throwaway_bucket(s3, bkt_name, run_id, account_id)
                s3.delete_bucket(Bucket=bkt_name, ExpectedBucketOwner=account_id)
                ledger.record_deleted("s3_bucket", bkt_name, intent_id=bkt_intent, safe=True)
            except Exception as exc:
                ledger.record_deleted("s3_bucket", bkt_name, status="cleanup_failed", detail=safe_error_label(exc), intent_id=bkt_intent, safe=True)
    return results


def run_d7_sup_sqs(run_id: str, ledger: RunLedger, *, session: Any = None) -> list[dict[str, Any]]:
    """D7-sup-sqs: supplementary check on throwaway SQS queue (stores queue name, never URL)."""
    sqs = locked_boto3_client("sqs", session=session)
    account_id, _ = get_caller_identity(session=session)
    q_name = make_throwaway_name(run_id, "q")
    q_intent = ledger.record_intent("sqs_queue", q_name)
    q_url: str | None = None
    results: list[dict[str, Any]] = []

    try:
        q_url = sqs.create_queue(
            QueueName=q_name,
            Attributes={"SqsManagedSseEnabled": "true"},
            tags={PURPOSE_TAG_KEY: PURPOSE_TAG_VALUE, RUN_ID_TAG_KEY: run_id},
        )["QueueUrl"]
        assert_throwaway_name(q_url, run_id=run_id, account_id=account_id)
        ledger.confirm_created(q_intent, q_name)

        # Verify live tags BEFORE set_queue_attributes (Finding 5).
        verified_url = verify_owned_sqs_queue_live(sqs, q_name, run_id, account_id)
        t1 = utc_now_iso()
        r1 = sqs.set_queue_attributes(QueueUrl=verified_url, Attributes={"VisibilityTimeout": "45"})
        e1 = utc_now_iso()
        results.append(
            _stim(
                "D7-sup-sqs",
                "sqs:SetQueueAttributes",
                kind="d7_eventbridge",
                resource_name=q_name,
                target_ids=[q_name, f"arn:aws:sqs:{ALLOWED_REGION}:{account_id}:{q_name}"],
                expected_event_names=["SetQueueAttributes"],
                expected_event_source="sqs.amazonaws.com",
                started_at_utc=t1,
                ended_at_utc=e1,
                api_call_succeeded=_http_ok(r1),
            )
        )
        ledger.record_event(["D7-sup-sqs"], "sqs:SetQueueAttributes", resource_name=q_name, started_at_utc=t1, ended_at_utc=e1)
    finally:
        if q_url:
            try:
                verified_url = verify_owned_sqs_queue_live(sqs, q_name, run_id, account_id)
                sqs.delete_queue(QueueUrl=verified_url)
                ledger.record_deleted("sqs_queue", q_name, intent_id=q_intent, safe=True)
            except Exception as exc:
                ledger.record_deleted("sqs_queue", q_name, status="cleanup_failed", detail=safe_error_label(exc), intent_id=q_intent, safe=True)
    return results


def run_d7_sup_ddb(run_id: str, ledger: RunLedger, *, session: Any = None) -> list[dict[str, Any]]:
    """D7-sup-ddb: supplementary check on throwaway DynamoDB table (UpdateTimeToLive)."""
    ddb = locked_boto3_client("dynamodb", session=session)
    account_id, _ = get_caller_identity(session=session)
    tbl_name = make_throwaway_name(run_id, "tbl")
    tbl_intent = ledger.record_intent("dynamodb_table", tbl_name)
    created = False
    results: list[dict[str, Any]] = []

    try:
        ddb.create_table(
            TableName=tbl_name,
            AttributeDefinitions=[{"AttributeName": "pk", "AttributeType": "S"}],
            KeySchema=[{"AttributeName": "pk", "KeyType": "HASH"}],
            BillingMode="PAY_PER_REQUEST",
            Tags=[
                {"Key": PURPOSE_TAG_KEY, "Value": PURPOSE_TAG_VALUE},
                {"Key": RUN_ID_TAG_KEY, "Value": run_id},
            ],
        )
        created = True
        ledger.confirm_created(tbl_intent, tbl_name)
        ddb.get_waiter("table_exists").wait(TableName=tbl_name)

        _verify_ddb_owned(ddb, tbl_name, run_id, account_id)
        t_ttl = utc_now_iso()
        r_ttl = ddb.update_time_to_live(
            TableName=tbl_name,
            TimeToLiveSpecification={"Enabled": True, "AttributeName": "ttl"},
        )
        e_ttl = utc_now_iso()
        results.append(
            _stim(
                "D7-sup-ddb",
                "dynamodb:UpdateTimeToLive",
                kind="d7_eventbridge",
                resource_name=tbl_name,
                target_ids=[tbl_name, f"arn:aws:dynamodb:{ALLOWED_REGION}:{account_id}:table/{tbl_name}"],
                expected_event_names=["UpdateTimeToLive"],
                expected_event_source="dynamodb.amazonaws.com",
                started_at_utc=t_ttl,
                ended_at_utc=e_ttl,
                api_call_succeeded=_http_ok(r_ttl),
            )
        )
        ledger.record_event(["D7-sup-ddb"], "dynamodb:UpdateTimeToLive", resource_name=tbl_name, started_at_utc=t_ttl, ended_at_utc=e_ttl)
    finally:
        if created:
            try:
                _verify_ddb_owned(ddb, tbl_name, run_id, account_id)
                ddb.delete_table(TableName=tbl_name)
                ledger.record_deleted("dynamodb_table", tbl_name, intent_id=tbl_intent, safe=True)
            except Exception as exc:
                ledger.record_deleted("dynamodb_table", tbl_name, status="cleanup_failed", detail=safe_error_label(exc), intent_id=tbl_intent, safe=True)
    return results


def run_d7_sup_cw(run_id: str, ledger: RunLedger, *, session: Any = None) -> list[dict[str, Any]]:
    """D7-sup-cw: supplementary check on throwaway CloudWatch alarm."""
    cw = locked_boto3_client("cloudwatch", session=session)
    account_id, _ = get_caller_identity(session=session)
    alarm_name = make_throwaway_name(run_id, "alarm")
    alarm_intent = ledger.record_intent("cloudwatch_alarm", alarm_name)
    created = False
    results: list[dict[str, Any]] = []

    try:
        t0 = utc_now_iso()
        r0 = cw.put_metric_alarm(
            AlarmName=alarm_name,
            AlarmDescription="Throwaway Tessera detection test alarm (no actions)",
            MetricName="DtestDummy",
            Namespace="Tessera/DetectionTest",
            Statistic="Sum",
            Period=300,
            EvaluationPeriods=1,
            Threshold=1.0,
            ComparisonOperator="GreaterThanOrEqualToThreshold",
            Tags=[
                {"Key": PURPOSE_TAG_KEY, "Value": PURPOSE_TAG_VALUE},
                {"Key": RUN_ID_TAG_KEY, "Value": run_id},
            ],
        )
        e0 = utc_now_iso()
        created = True
        ledger.confirm_created(alarm_intent, alarm_name)
        results.append(
            _stim(
                "D7-sup-cw",
                "cloudwatch:PutMetricAlarm",
                kind="d7_eventbridge",
                resource_name=alarm_name,
                target_ids=[alarm_name],
                expected_event_names=["PutMetricAlarm"],
                expected_event_source="monitoring.amazonaws.com",
                started_at_utc=t0,
                ended_at_utc=e0,
                api_call_succeeded=_http_ok(r0),
            )
        )
        ledger.record_event(["D7-sup-cw"], "cloudwatch:PutMetricAlarm", resource_name=alarm_name, started_at_utc=t0, ended_at_utc=e0)
    finally:
        if created:
            try:
                _verify_cw_alarm_owned(cw, alarm_name, run_id, account_id)
                cw.delete_alarms(AlarmNames=[alarm_name])
                ledger.record_deleted("cloudwatch_alarm", alarm_name, intent_id=alarm_intent, safe=True)
            except Exception as exc:
                ledger.record_deleted("cloudwatch_alarm", alarm_name, status="cleanup_failed", detail=safe_error_label(exc), intent_id=alarm_intent, safe=True)
    return results


def run_d7_sup_logs(run_id: str, ledger: RunLedger, *, session: Any = None) -> list[dict[str, Any]]:
    """D7-sup-logs: supplementary check on throwaway CloudWatch Logs group."""
    logs = locked_boto3_client("logs", session=session)
    account_id, _ = get_caller_identity(session=session)
    group_name = make_throwaway_name(run_id, "logs")
    lg_intent = ledger.record_intent("log_group", group_name)
    created = False
    results: list[dict[str, Any]] = []

    try:
        logs.create_log_group(
            logGroupName=group_name,
            tags={PURPOSE_TAG_KEY: PURPOSE_TAG_VALUE, RUN_ID_TAG_KEY: run_id},
        )
        created = True
        ledger.confirm_created(lg_intent, group_name)

        _verify_log_group_owned(logs, group_name, run_id, account_id)
        t1 = utc_now_iso()
        r1 = logs.put_retention_policy(logGroupName=group_name, retentionInDays=1)
        e1 = utc_now_iso()
        results.append(
            _stim(
                "D7-sup-logs",
                "logs:PutRetentionPolicy",
                kind="d7_eventbridge",
                resource_name=group_name,
                target_ids=[group_name],
                expected_event_names=["PutRetentionPolicy"],
                expected_event_source="logs.amazonaws.com",
                started_at_utc=t1,
                ended_at_utc=e1,
                api_call_succeeded=_http_ok(r1),
            )
        )
        ledger.record_event(["D7-sup-logs"], "logs:PutRetentionPolicy", resource_name=group_name, started_at_utc=t1, ended_at_utc=e1)
    finally:
        if created:
            try:
                _verify_log_group_owned(logs, group_name, run_id, account_id)
                logs.delete_log_group(logGroupName=group_name)
                ledger.record_deleted("log_group", group_name, intent_id=lg_intent, safe=True)
            except Exception as exc:
                ledger.record_deleted("log_group", group_name, status="cleanup_failed", detail=safe_error_label(exc), intent_id=lg_intent, safe=True)
    return results


def run_d7_sup_eb(run_id: str, ledger: RunLedger, *, session: Any = None) -> list[dict[str, Any]]:
    """D7-sup-eb: supplementary check on throwaway EventBridge rule."""
    eb = locked_boto3_client("events", session=session)
    account_id, _ = get_caller_identity(session=session)
    rule_name = make_throwaway_name(run_id, "rule")
    eb_intent = ledger.record_intent("eventbridge_rule", rule_name)
    created = False
    results: list[dict[str, Any]] = []

    try:
        t0 = utc_now_iso()
        r0 = eb.put_rule(
            Name=rule_name,
            EventPattern=json.dumps({"source": ["tessera.dtest.noop"]}),
            State="DISABLED",
            Description="Throwaway Tessera detection test rule",
            Tags=[
                {"Key": PURPOSE_TAG_KEY, "Value": PURPOSE_TAG_VALUE},
                {"Key": RUN_ID_TAG_KEY, "Value": run_id},
            ],
        )
        e0 = utc_now_iso()
        created = True
        ledger.confirm_created(eb_intent, rule_name)
        results.append(
            _stim(
                "D7-sup-eb",
                "events:PutRule",
                kind="d7_eventbridge",
                resource_name=rule_name,
                target_ids=[rule_name],
                expected_event_names=["PutRule"],
                expected_event_source="events.amazonaws.com",
                started_at_utc=t0,
                ended_at_utc=e0,
                api_call_succeeded=_http_ok(r0),
            )
        )
        ledger.record_event(["D7-sup-eb"], "events:PutRule", resource_name=rule_name, started_at_utc=t0, ended_at_utc=e0)
    finally:
        if created:
            try:
                _verify_eb_rule_owned(eb, rule_name, run_id, account_id)
                eb.delete_rule(Name=rule_name)
                ledger.record_deleted("eventbridge_rule", rule_name, intent_id=eb_intent, safe=True)
            except Exception as exc:
                ledger.record_deleted("eventbridge_rule", rule_name, status="cleanup_failed", detail=safe_error_label(exc), intent_id=eb_intent, safe=True)
    return results


# ---------------------------------------------------------------------------
# Live-Verified Crash-Recovery Cleanup (Findings 2, 5, 6, 7, 9, 12)
# ---------------------------------------------------------------------------

_CLEANUP_ORDER: dict[str, int] = {
    "sns_observer_subscription": 10,
    "kms_grant": 20,
    "kms_alias": 25,
    "kms_key": 30,
    "apigw_usage_plan_key": 35,
    "apigw_usage_plan": 40,
    "apigw_api_key": 45,
    "apigw_rest_api": 50,
    "lambda_permission": 55,
    "lambda_function": 60,
    "cloudtrail": 65,
    "s3_bucket": 70,
    "sns_topic": 75,
    "sqs_queue": 80,
    "sqs_observer_queue": 85,
    "dynamodb_table": 90,
    "cloudwatch_alarm": 95,
    "log_group": 100,
    "eventbridge_rule": 105,
    "iam_role_policy": 110,
    "iam_role": 115,
    "iam_access_key": 120,
    "iam_user": 125,
}


def _cleanup_single_verified(
    rtype: str,
    ident: str,
    name: str,
    run_id: str,
    account_id: str,
    *,
    session: Any = None,
) -> tuple[str, str]:
    """Delete ONE resource strictly after live AWS ownership verification.

    Returns (new_status, safe_message). Raises SafetyViolation if live verification fails.
    """
    if rtype == "sns_observer_subscription":
        sns = locked_boto3_client("sns", session=session)
        sqs = locked_boto3_client("sqs", session=session)
        topic_arn = find_alarm_topic_arn(sns, account_id)
        try:
            verify_owned_observer_subscription_live(
                sns, sqs, ident, run_id=run_id, account_id=account_id, expected_topic_arn=topic_arn
            )
        except Exception as exc:
            if _is_not_found(exc):
                return "deleted", f"already_gone {rtype} {name}"
            raise
        sns.unsubscribe(SubscriptionArn=ident)
        return "deleted", f"deleted {rtype} {name}"

    if rtype in ("sqs_queue", "sqs_observer_queue"):
        sqs = locked_boto3_client("sqs", session=session)
        # Always recover by queue NAME, never trusting a ledger URL (Finding 9).
        q_name = name if name.startswith(f"tessera-dtest-{run_id}-") else ident
        assert_throwaway_name(q_name, run_id=run_id)
        try:
            q_url = verify_owned_sqs_queue_live(sqs, q_name, run_id, account_id)
        except Exception as exc:
            if _is_not_found(exc):
                return "deleted", f"already_gone {rtype} {q_name}"
            raise
        sqs.delete_queue(QueueUrl=q_url)
        return "deleted", f"deleted {rtype} {q_name}"

    if rtype == "sns_topic":
        sns = locked_boto3_client("sns", session=session)
        try:
            _verify_sns_topic_owned(sns, ident, run_id, account_id)
        except Exception as exc:
            if _is_not_found(exc):
                return "deleted", f"already_gone {rtype} {name}"
            raise
        sns.delete_topic(TopicArn=ident)
        return "deleted", f"deleted {rtype} {name}"

    if rtype == "s3_bucket":
        s3 = locked_boto3_client("s3", session=session)
        try:
            _empty_throwaway_bucket(s3, ident, run_id, account_id)
        except Exception as exc:
            if _is_not_found(exc):
                return "deleted", f"already_gone {rtype} {ident}"
            raise
        s3.delete_bucket(Bucket=ident, ExpectedBucketOwner=account_id)
        return "deleted", f"deleted {rtype} {ident}"

    if rtype == "kms_alias":
        kms = locked_boto3_client("kms", session=session)
        target_key = _verify_kms_alias_owned(kms, ident, run_id, account_id)
        if target_key is None:
            return "deleted", f"already_gone {rtype} {ident}"
        kms.delete_alias(AliasName=ident)
        return "deleted", f"deleted {rtype} {ident}"

    if rtype == "kms_grant":
        # Grants are revoked during kms_key cleanup after live key verification.
        return "deleted", f"reconciled_with_parent {rtype} {name}"

    if rtype == "kms_key":
        kms = locked_boto3_client("kms", session=session)
        meta = _verify_kms_key_owned(kms, ident, run_id, account_id)
        for page in kms.get_paginator("list_grants").paginate(KeyId=meta["KeyId"]):
            for g in page.get("Grants", []):
                kms.revoke_grant(KeyId=meta["KeyId"], GrantId=g["GrantId"])
        if meta.get("KeyState") == "PendingDeletion":
            del_date = meta["DeletionDate"].strftime("%Y-%m-%d")
            return "scheduled_deletion", f"scheduled, deletes on {del_date}"
        resp = kms.schedule_key_deletion(KeyId=meta["KeyId"], PendingWindowInDays=7)
        del_date = resp["DeletionDate"].strftime("%Y-%m-%d")
        return "scheduled_deletion", f"scheduled, deletes on {del_date}"

    if rtype == "apigw_usage_plan_key":
        return "deleted", f"reconciled_with_parent {rtype} {name}"

    if rtype == "apigw_usage_plan":
        apigw = locked_boto3_client("apigateway", session=session)
        try:
            _verify_apigw_usage_plan_owned(apigw, ident, run_id)
        except Exception as exc:
            if _is_not_found(exc):
                return "deleted", f"already_gone {rtype} {name}"
            raise
        for k in apigw.get_usage_plan_keys(usagePlanId=ident).get("items", []):
            _verify_apigw_api_key_owned(apigw, k["id"], run_id)
            apigw.delete_usage_plan_key(usagePlanId=ident, keyId=k["id"])
        apigw.delete_usage_plan(usagePlanId=ident)
        return "deleted", f"deleted {rtype} {name}"

    if rtype == "apigw_api_key":
        apigw = locked_boto3_client("apigateway", session=session)
        try:
            _verify_apigw_api_key_owned(apigw, ident, run_id)
        except Exception as exc:
            if _is_not_found(exc):
                return "deleted", f"already_gone {rtype} {name}"
            raise
        apigw.delete_api_key(apiKey=ident)
        return "deleted", f"deleted {rtype} {name}"

    if rtype == "apigw_rest_api":
        apigw = locked_boto3_client("apigateway", session=session)
        try:
            _verify_apigw_rest_api_owned(apigw, ident, run_id)
        except Exception as exc:
            if _is_not_found(exc):
                return "deleted", f"already_gone {rtype} {name}"
            raise
        apigw.delete_rest_api(restApiId=ident)
        return "deleted", f"deleted {rtype} {name}"

    if rtype == "lambda_permission":
        return "deleted", f"reconciled_with_parent {rtype} {name}"

    if rtype == "lambda_function":
        lam = locked_boto3_client("lambda", session=session)
        try:
            _verify_lambda_owned(lam, ident, run_id, account_id)
        except Exception as exc:
            if _is_not_found(exc):
                return "deleted", f"already_gone {rtype} {ident}"
            raise
        lam.delete_function(FunctionName=ident)
        return "deleted", f"deleted {rtype} {ident}"

    if rtype == "iam_role_policy":
        return "deleted", f"reconciled_with_parent {rtype} {name}"

    if rtype == "iam_role":
        iam = locked_boto3_client("iam", session=session, allow_global_iam=True)
        try:
            _verify_iam_role_owned(iam, ident, run_id, account_id)
        except Exception as exc:
            if _is_not_found(exc):
                return "deleted", f"already_gone {rtype} {ident}"
            raise
        for p in iam.list_role_policies(RoleName=ident).get("PolicyNames", []):
            iam.delete_role_policy(RoleName=ident, PolicyName=p)
        iam.delete_role(RoleName=ident)
        return "deleted", f"deleted {rtype} {ident}"

    if rtype == "iam_access_key":
        iam = locked_boto3_client("iam", session=session, allow_global_iam=True)
        try:
            _verify_iam_user_owned(iam, ident, run_id, account_id)
        except Exception as exc:
            if _is_not_found(exc):
                return "deleted", f"already_gone {rtype} {ident}"
            raise
        for k in iam.list_access_keys(UserName=ident).get("AccessKeyMetadata", []):
            iam.delete_access_key(UserName=ident, AccessKeyId=k["AccessKeyId"])
        return "deleted", f"deleted {rtype} for {ident}"

    if rtype == "iam_user":
        iam = locked_boto3_client("iam", session=session, allow_global_iam=True)
        try:
            _verify_iam_user_owned(iam, ident, run_id, account_id)
        except Exception as exc:
            if _is_not_found(exc):
                return "deleted", f"already_gone {rtype} {ident}"
            raise
        for k in iam.list_access_keys(UserName=ident).get("AccessKeyMetadata", []):
            iam.delete_access_key(UserName=ident, AccessKeyId=k["AccessKeyId"])
        iam.delete_user(UserName=ident)
        return "deleted", f"deleted {rtype} {ident}"

    if rtype == "cloudtrail":
        ct = locked_boto3_client("cloudtrail", session=session)
        try:
            _verify_cloudtrail_owned(ct, ident, run_id, account_id)
        except Exception as exc:
            if _is_not_found(exc):
                return "deleted", f"already_gone {rtype} {ident}"
            raise
        ct.delete_trail(Name=ident)
        return "deleted", f"deleted {rtype} {ident}"

    if rtype == "dynamodb_table":
        ddb = locked_boto3_client("dynamodb", session=session)
        try:
            _verify_ddb_owned(ddb, ident, run_id, account_id)
        except Exception as exc:
            if _is_not_found(exc):
                return "deleted", f"already_gone {rtype} {ident}"
            raise
        ddb.delete_table(TableName=ident)
        return "deleted", f"deleted {rtype} {ident}"

    if rtype == "cloudwatch_alarm":
        cw = locked_boto3_client("cloudwatch", session=session)
        try:
            _verify_cw_alarm_owned(cw, ident, run_id, account_id)
        except KeyError:
            return "deleted", f"already_gone {rtype} {ident}"
        cw.delete_alarms(AlarmNames=[ident])
        return "deleted", f"deleted {rtype} {ident}"

    if rtype == "log_group":
        logs = locked_boto3_client("logs", session=session)
        try:
            _verify_log_group_owned(logs, ident, run_id, account_id)
        except KeyError:
            return "deleted", f"already_gone {rtype} {ident}"
        logs.delete_log_group(logGroupName=ident)
        return "deleted", f"deleted {rtype} {ident}"

    if rtype == "eventbridge_rule":
        eb = locked_boto3_client("events", session=session)
        try:
            _verify_eb_rule_owned(eb, ident, run_id, account_id)
        except Exception as exc:
            if _is_not_found(exc):
                return "deleted", f"already_gone {rtype} {ident}"
            raise
        eb.delete_rule(Name=ident)
        return "deleted", f"deleted {rtype} {ident}"

    raise SafetyViolation(f"Refusing unknown resource type {rtype!r} during recovery.")


def cleanup_from_ledger_file(
    ledger_path: Any,
    *,
    session: Any = None,
    discover_live: bool = True,
) -> dict[str, Any]:
    """Live-verified crash recovery: reconciles intents, verifies every target, persists results.

    Never trusts a ledger name-to-ID mapping alone. Refuses any unverified target without
    calling mutating AWS APIs. Returns ok=False if any refused, failed, or residual item remains.
    """
    path = Path(ledger_path)
    raw = load_ledger(path)
    run_id = validate_run_id(str(raw.get("run_id") or ""))
    account_id, _ = get_caller_identity(session=session)
    if raw.get("account_id") and raw["account_id"] != account_id:
        raise SafetyViolation("Ledger account_id does not match current AWS caller account.")

    resources: list[dict[str, Any]] = raw.setdefault("resources", [])

    # Step 1: Discover live AWS resources for run_id to reconcile any 'creating' intents
    # whose create committed before a crash or lost response (Finding 6).
    if discover_live:
        live_items = discover_live_run_resources(run_id, account_id, session=session)
        known_pairs = {
            (r.get("resource_type"), r.get("identifier"))
            for r in resources
            if r.get("identifier")
        }
        for item in live_items:
            pair = (item["resource_type"], item["identifier"])
            if pair not in known_pairs:
                # Reconcile an existing 'creating' intent if one matches by type + name.
                matched_intent = None
                for entry in resources:
                    if (
                        entry.get("status") == "creating"
                        and entry.get("resource_type") == item["resource_type"]
                        and entry.get("name") == item["name"]
                    ):
                        matched_intent = entry
                        break
                if matched_intent is not None:
                    matched_intent["identifier"] = item["identifier"]
                    matched_intent["status"] = "active"
                else:
                    resources.append(
                        {
                            "resource_type": item["resource_type"],
                            "identifier": item["identifier"],
                            "name": item["name"],
                            "status": "active",
                            "created_at_utc": None,
                            "deleted_at_utc": None,
                            "detail": "discovered_live_during_recovery",
                            "metadata": {},
                        }
                    )
                known_pairs.add(pair)

    # Step 2: Sort active/creating/cleanup_failed entries in safe dependency order.
    pending_indices = [
        idx
        for idx, entry in enumerate(resources)
        if entry.get("status") not in ("deleted", "scheduled_deletion", "not_created")
    ]
    pending_indices.sort(key=lambda idx: _CLEANUP_ORDER.get(resources[idx].get("resource_type", ""), 999))

    actions: list[str] = []
    refused: list[str] = []
    failed: list[str] = []

    for idx in pending_indices:
        entry = resources[idx]
        rtype = str(entry.get("resource_type") or "")
        ident = entry.get("identifier")
        name = str(entry.get("name") or "")

        # A 'creating' intent with no identifier and nothing found by live discovery was never created.
        if entry.get("status") == "creating" and not ident:
            entry["status"] = "not_created"
            entry["deleted_at_utc"] = utc_now_iso()
            entry["detail"] = "no_live_resource_found_for_intent"
            actions.append(f"reconciled not_created {rtype} {name}")
            continue

        try:
            new_status, msg = _cleanup_single_verified(
                rtype, str(ident), name, run_id, account_id, session=session
            )
            entry["status"] = new_status
            entry["deleted_at_utc"] = utc_now_iso()
            entry["detail"] = msg
            actions.append(msg)
        except SafetyViolation as exc:
            label = safe_error_label(exc)
            entry["status"] = "refused_unverified"
            entry["detail"] = label
            msg = f"refused_unverified {rtype} {name}: {label}"
            refused.append(msg)
            actions.append(msg)
        except Exception as exc:
            label = safe_error_label(exc)
            entry["status"] = "cleanup_failed"
            entry["detail"] = label
            msg = f"failed {rtype} {name}: {label}"
            failed.append(msg)
            actions.append(msg)

    # Step 3: Post-cleanup live residual verification sweep (Finding 7).
    residuals: list[str] = []
    if discover_live:
        kms = locked_boto3_client("kms", session=session)
        for item in discover_live_run_resources(run_id, account_id, session=session):
            if item["resource_type"] == "kms_key":
                try:
                    meta = kms.describe_key(KeyId=item["identifier"])["KeyMetadata"]
                    if meta.get("KeyState") == "PendingDeletion":
                        continue
                except Exception:
                    pass
            residuals.append(f"{item['resource_type']}:{item['name']}")

    ok = (not refused) and (not failed) and (not residuals)
    recovery_record = {
        "at_utc": utc_now_iso(),
        "ok": ok,
        "actions_count": len(actions),
        "refused_count": len(refused),
        "failed_count": len(failed),
        "residual_count": len(residuals),
        "residuals": residuals,
    }
    raw.setdefault("recovery_runs", []).append(recovery_record)
    save_ledger_dict(path, raw)

    return {
        "run_id": run_id,
        "ok": ok,
        "actions": actions,
        "refused": refused,
        "failed": failed,
        "residuals": residuals,
    }
