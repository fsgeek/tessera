"""D7 control-plane tampering tests using throwaway tessera-dtest-<run_id>-*
resources strictly in us-east-2.

Every resource created is:
1. Validated against safety.assert_throwaway_name before any mutating call.
2. Tagged purpose=detection-test (and run_id=<run_id>) wherever AWS supports tags.
3. Recorded immediately in RunLedger before proceeding.
4. Cleaned up inside a finally block (with KMS keys scheduled for deletion at the
   7-day minimum and reported as 'scheduled, deletes on <date>' per Rule 6).
"""

from __future__ import annotations

import io
import json
import time
import zipfile
from typing import Any

from ledger import RunLedger, load_ledger, utc_now_iso
from safety import (
    ALLOWED_REGION,
    PURPOSE_TAG_KEY,
    PURPOSE_TAG_VALUE,
    assert_throwaway_id_registered,
    assert_throwaway_name,
    locked_boto3_client,
    make_throwaway_name,
)


def _caller_account_id(session: Any = None) -> str:
    sts = locked_boto3_client("sts", session=session)
    return sts.get_caller_identity()["Account"]


def _caller_arn(session: Any = None) -> str:
    sts = locked_boto3_client("sts", session=session)
    return sts.get_caller_identity()["Arn"]


def _make_noop_lambda_zip(comment: str) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("index.py", f"# {comment}\ndef handler(event, context):\n    return {{'ok': True}}\n")
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
            raise RuntimeError(f"Throwaway Lambda {fn_name} failed: {cfg.get('StateReason')}")
        time.sleep(2.0)
    raise TimeoutError(f"Timed out waiting for throwaway Lambda {fn_name} to become Active")


def run_d7_kms(run_id: str, ledger: RunLedger, *, session: Any = None) -> None:
    """D7-kms-policy, D7-kms-grant, D7-kms-disable, D7-kms-delete on a throwaway KMS key."""
    kms = locked_boto3_client("kms", session=session)
    account_id = _caller_account_id(session=session)
    caller_arn = _caller_arn(session=session)
    name = make_throwaway_name(run_id, "kms")
    alias_name = f"alias/{name}"
    assert_throwaway_name(alias_name, allow_alias_prefix=True)

    owned_keys: set[str] = set()
    key_id: str | None = None
    grant_id: str | None = None
    alias_created = False
    deletion_scheduled = False

    try:
        t0 = utc_now_iso()
        resp = kms.create_key(
            Description=f"{name} (throwaway detection test)",
            KeyUsage="ENCRYPT_DECRYPT",
            KeySpec="SYMMETRIC_DEFAULT",
            Tags=[
                {"TagKey": PURPOSE_TAG_KEY, "TagValue": PURPOSE_TAG_VALUE},
                {"TagKey": "run_id", "TagValue": run_id},
            ],
        )
        key_id = resp["KeyMetadata"]["KeyId"]
        key_arn = resp["KeyMetadata"]["Arn"]
        owned_keys.add(key_id)
        ledger.record_created("kms_key", key_id, name, metadata={"arn": key_arn})

        kms.create_alias(AliasName=alias_name, TargetKeyId=key_id)
        alias_created = True
        ledger.record_created("kms_alias", alias_name, alias_name, metadata={"key_id": key_id})
        ledger.record_event(
            ["D7-kms-create"],
            "kms:CreateKey + CreateAlias",
            resource_name=alias_name,
            started_at_utc=t0,
            ended_at_utc=utc_now_iso(),
            details={"key_id": key_id, "key_arn": key_arn},
        )

        # 1. PutKeyPolicy (preserves root full admin so key is never orphaned)
        assert_throwaway_id_registered(key_id, owned_keys, "kms:PutKeyPolicy")
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
        kms.put_key_policy(KeyId=key_id, PolicyName="default", Policy=json.dumps(policy))
        ledger.record_event(
            ["D7-kms-policy"],
            "kms:PutKeyPolicy",
            resource_name=alias_name,
            started_at_utc=t1,
            ended_at_utc=utc_now_iso(),
            details={"key_id": key_id},
        )

        # 2. CreateGrant (minimal read-only DescribeKey grant to caller)
        assert_throwaway_id_registered(key_id, owned_keys, "kms:CreateGrant")
        t2 = utc_now_iso()
        g_resp = kms.create_grant(
            KeyId=key_id,
            GranteePrincipal=caller_arn,
            Operations=["DescribeKey"],
            Name=name,
        )
        grant_id = g_resp["GrantId"]
        ledger.record_event(
            ["D7-kms-grant"],
            "kms:CreateGrant",
            resource_name=alias_name,
            started_at_utc=t2,
            ended_at_utc=utc_now_iso(),
            details={"key_id": key_id, "grant_id": grant_id},
        )

        # 3. DisableKey
        assert_throwaway_id_registered(key_id, owned_keys, "kms:DisableKey")
        t3 = utc_now_iso()
        kms.disable_key(KeyId=key_id)
        ledger.record_event(
            ["D7-kms-disable"],
            "kms:DisableKey",
            resource_name=alias_name,
            started_at_utc=t3,
            ended_at_utc=utc_now_iso(),
            details={"key_id": key_id},
        )

        # 4. ScheduleKeyDeletion (minimum 7-day window; also performs key cleanup)
        assert_throwaway_id_registered(key_id, owned_keys, "kms:ScheduleKeyDeletion")
        t4 = utc_now_iso()
        del_resp = kms.schedule_key_deletion(KeyId=key_id, PendingWindowInDays=7)
        deletion_scheduled = True
        del_date = del_resp["DeletionDate"].strftime("%Y-%m-%d")
        ledger.record_kms_scheduled_deletion(key_id, del_date)
        ledger.record_event(
            ["D7-kms-delete"],
            "kms:ScheduleKeyDeletion",
            resource_name=alias_name,
            started_at_utc=t4,
            ended_at_utc=utc_now_iso(),
            details={"key_id": key_id, "deletes_on": del_date},
        )
    finally:
        if key_id and grant_id:
            try:
                assert_throwaway_id_registered(key_id, owned_keys, "kms:RevokeGrant")
                kms.revoke_grant(KeyId=key_id, GrantId=grant_id)
            except Exception as exc:
                ledger.add_note(f"kms:RevokeGrant cleanup note for {key_id}: {exc}")
        if alias_created:
            try:
                assert_throwaway_name(alias_name, allow_alias_prefix=True)
                kms.delete_alias(AliasName=alias_name)
                ledger.record_deleted("kms_alias", alias_name)
            except Exception as exc:
                ledger.record_deleted("kms_alias", alias_name, status="cleanup_failed", detail=str(exc))
        if key_id and not deletion_scheduled:
            try:
                assert_throwaway_id_registered(key_id, owned_keys, "kms:ScheduleKeyDeletion")
                del_resp = kms.schedule_key_deletion(KeyId=key_id, PendingWindowInDays=7)
                del_date = del_resp["DeletionDate"].strftime("%Y-%m-%d")
                ledger.record_kms_scheduled_deletion(key_id, del_date)
            except Exception as exc:
                ledger.record_deleted("kms_key", key_id, status="cleanup_failed", detail=str(exc))


def run_d7_s3(run_id: str, ledger: RunLedger, *, session: Any = None) -> None:
    """D7-s3-policy and D7-s3-lock on throwaway S3 buckets in us-east-2."""
    s3 = locked_boto3_client("s3", session=session)
    bkt_policy = make_throwaway_name(run_id, "bkt")
    bkt_lock = make_throwaway_name(run_id, "lock-bkt")

    # Part A: Bucket policy changes
    created_policy_bkt = False
    try:
        assert_throwaway_name(bkt_policy)
        t0 = utc_now_iso()
        s3.create_bucket(
            Bucket=bkt_policy,
            CreateBucketConfiguration={"LocationConstraint": ALLOWED_REGION},
        )
        created_policy_bkt = True
        ledger.record_created("s3_bucket", bkt_policy, bkt_policy)
        s3.put_bucket_tagging(
            Bucket=bkt_policy,
            Tagging={
                "TagSet": [
                    {"Key": PURPOSE_TAG_KEY, "Value": PURPOSE_TAG_VALUE},
                    {"Key": "run_id", "Value": run_id},
                ]
            },
        )
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
        s3.put_bucket_policy(Bucket=bkt_policy, Policy=json.dumps(policy_doc))
        ledger.record_event(
            ["D7-s3-policy"],
            "s3:PutBucketPolicy",
            resource_name=bkt_policy,
            started_at_utc=t1,
            ended_at_utc=utc_now_iso(),
            details={"created_at": t0},
        )
        s3.delete_bucket_policy(Bucket=bkt_policy)
    finally:
        if created_policy_bkt:
            try:
                assert_throwaway_name(bkt_policy)
                s3.delete_bucket(Bucket=bkt_policy)
                ledger.record_deleted("s3_bucket", bkt_policy)
            except Exception as exc:
                ledger.record_deleted("s3_bucket", bkt_policy, status="cleanup_failed", detail=str(exc))

    # Part B: Object Lock configuration on an EMPTY throwaway bucket (zero objects written!)
    created_lock_bkt = False
    try:
        assert_throwaway_name(bkt_lock)
        s3.create_bucket(
            Bucket=bkt_lock,
            CreateBucketConfiguration={"LocationConstraint": ALLOWED_REGION},
            ObjectLockEnabledForBucket=True,
        )
        created_lock_bkt = True
        ledger.record_created("s3_bucket", bkt_lock, bkt_lock, metadata={"object_lock": True})
        s3.put_bucket_tagging(
            Bucket=bkt_lock,
            Tagging={
                "TagSet": [
                    {"Key": PURPOSE_TAG_KEY, "Value": PURPOSE_TAG_VALUE},
                    {"Key": "run_id", "Value": run_id},
                ]
            },
        )
        t2 = utc_now_iso()
        s3.put_object_lock_configuration(
            Bucket=bkt_lock,
            ObjectLockConfiguration={
                "ObjectLockEnabled": "Enabled",
                "Rule": {"DefaultRetention": {"Mode": "GOVERNANCE", "Days": 1}},
            },
        )
        ledger.record_event(
            ["D7-s3-lock"],
            "s3:PutObjectLockConfiguration",
            resource_name=bkt_lock,
            started_at_utc=t2,
            ended_at_utc=utc_now_iso(),
        )
    finally:
        if created_lock_bkt:
            try:
                assert_throwaway_name(bkt_lock)
                s3.delete_bucket(Bucket=bkt_lock)
                ledger.record_deleted("s3_bucket", bkt_lock)
            except Exception as exc:
                ledger.record_deleted("s3_bucket", bkt_lock, status="cleanup_failed", detail=str(exc))


def run_d7_sns(run_id: str, ledger: RunLedger, *, session: Any = None) -> None:
    """D7-sns-topic on a throwaway SNS topic (production topic is never modified)."""
    sns = locked_boto3_client("sns", session=session)
    topic_name = make_throwaway_name(run_id, "topic")
    topic_arn: str | None = None

    try:
        assert_throwaway_name(topic_name)
        t0 = utc_now_iso()
        resp = sns.create_topic(
            Name=topic_name,
            Tags=[
                {"Key": PURPOSE_TAG_KEY, "Value": PURPOSE_TAG_VALUE},
                {"Key": "run_id", "Value": run_id},
            ],
        )
        topic_arn = resp["TopicArn"]
        assert_throwaway_name(topic_arn)
        ledger.record_created("sns_topic", topic_arn, topic_name)

        t1 = utc_now_iso()
        sns.set_topic_attributes(
            TopicArn=topic_arn,
            AttributeName="DisplayName",
            AttributeValue="tessera-dtest",
        )
        ledger.record_event(
            ["D7-sns-topic"],
            "sns:CreateTopic + SetTopicAttributes",
            resource_name=topic_name,
            started_at_utc=t0,
            ended_at_utc=utc_now_iso(),
            details={"topic_arn": topic_arn, "set_attr_at": t1},
        )
    finally:
        if topic_arn:
            try:
                assert_throwaway_name(topic_arn)
                sns.delete_topic(TopicArn=topic_arn)
                ledger.record_deleted("sns_topic", topic_arn)
            except Exception as exc:
                ledger.record_deleted("sns_topic", topic_arn, status="cleanup_failed", detail=str(exc))


def run_d7_apigw(run_id: str, ledger: RunLedger, *, session: Any = None) -> None:
    """D7-apigw-key and D7-apigw-plan on throwaway REST API, API key, and usage plan."""
    apigw = locked_boto3_client("apigateway", session=session)
    api_name = make_throwaway_name(run_id, "api")
    key_name = make_throwaway_name(run_id, "key")
    plan_name = make_throwaway_name(run_id, "plan")

    owned_apis: set[str] = set()
    owned_keys: set[str] = set()
    owned_plans: set[str] = set()

    api_id: str | None = None
    key_id: str | None = None
    plan_id: str | None = None
    plan_key_attached = False

    try:
        assert_throwaway_name(api_name)
        assert_throwaway_name(key_name)
        assert_throwaway_name(plan_name)

        api_resp = apigw.create_rest_api(
            name=api_name,
            description="Throwaway Tessera detection test API",
            tags={PURPOSE_TAG_KEY: PURPOSE_TAG_VALUE, "run_id": run_id},
        )
        api_id = api_resp["id"]
        owned_apis.add(api_id)
        ledger.record_created("apigw_rest_api", api_id, api_name)

        t_key = utc_now_iso()
        key_resp = apigw.create_api_key(
            name=key_name,
            description="Throwaway detection test key",
            enabled=False,
            tags={PURPOSE_TAG_KEY: PURPOSE_TAG_VALUE, "run_id": run_id},
        )
        # Never read or log key_resp['value'] (Rule 5).
        key_id = key_resp["id"]
        owned_keys.add(key_id)
        ledger.record_created("apigw_api_key", key_id, key_name)

        assert_throwaway_id_registered(key_id, owned_keys, "apigateway:UpdateApiKey")
        apigw.update_api_key(
            apiKey=key_id,
            patchOperations=[{"op": "replace", "path": "/description", "value": "updated-dtest"}],
        )
        ledger.record_event(
            ["D7-apigw-key"],
            "apigateway:CreateApiKey + UpdateApiKey",
            resource_name=key_name,
            started_at_utc=t_key,
            ended_at_utc=utc_now_iso(),
            details={"key_id": key_id},
        )

        t_plan = utc_now_iso()
        plan_resp = apigw.create_usage_plan(
            name=plan_name,
            description="Throwaway detection test usage plan",
            throttle={"rateLimit": 1.0, "burstLimit": 1},
            tags={PURPOSE_TAG_KEY: PURPOSE_TAG_VALUE, "run_id": run_id},
        )
        plan_id = plan_resp["id"]
        owned_plans.add(plan_id)
        ledger.record_created("apigw_usage_plan", plan_id, plan_name)

        assert_throwaway_id_registered(plan_id, owned_plans, "apigateway:UpdateUsagePlan")
        apigw.update_usage_plan(
            usagePlanId=plan_id,
            patchOperations=[{"op": "replace", "path": "/description", "value": "updated-dtest"}],
        )
        apigw.create_usage_plan_key(usagePlanId=plan_id, keyId=key_id, keyType="API_KEY")
        plan_key_attached = True
        ledger.record_event(
            ["D7-apigw-plan"],
            "apigateway:CreateUsagePlan + UpdateUsagePlan + CreateUsagePlanKey",
            resource_name=plan_name,
            started_at_utc=t_plan,
            ended_at_utc=utc_now_iso(),
            details={"plan_id": plan_id, "api_id": api_id},
        )
    finally:
        if plan_key_attached and plan_id and key_id:
            try:
                assert_throwaway_id_registered(plan_id, owned_plans, "apigateway:DeleteUsagePlanKey")
                apigw.delete_usage_plan_key(usagePlanId=plan_id, keyId=key_id)
            except Exception as exc:
                ledger.add_note(f"apigateway:DeleteUsagePlanKey cleanup error: {exc}")
        if plan_id:
            try:
                assert_throwaway_id_registered(plan_id, owned_plans, "apigateway:DeleteUsagePlan")
                apigw.delete_usage_plan(usagePlanId=plan_id)
                ledger.record_deleted("apigw_usage_plan", plan_id)
            except Exception as exc:
                ledger.record_deleted("apigw_usage_plan", plan_id, status="cleanup_failed", detail=str(exc))
        if key_id:
            try:
                assert_throwaway_id_registered(key_id, owned_keys, "apigateway:DeleteApiKey")
                apigw.delete_api_key(apiKey=key_id)
                ledger.record_deleted("apigw_api_key", key_id)
            except Exception as exc:
                ledger.record_deleted("apigw_api_key", key_id, status="cleanup_failed", detail=str(exc))
        if api_id:
            try:
                assert_throwaway_id_registered(api_id, owned_apis, "apigateway:DeleteRestApi")
                apigw.delete_rest_api(restApiId=api_id)
                ledger.record_deleted("apigw_rest_api", api_id)
            except Exception as exc:
                ledger.record_deleted("apigw_rest_api", api_id, status="cleanup_failed", detail=str(exc))


def run_d7_lambda(run_id: str, ledger: RunLedger, *, session: Any = None) -> None:
    """D7-lambda-config, D7-lambda-code, and D7-sup-lambda-perm on a throwaway Lambda."""
    iam = locked_boto3_client("iam", session=session)
    lam = locked_boto3_client("lambda", session=session)
    role_name = make_throwaway_name(run_id, "fn-role")
    fn_name = make_throwaway_name(run_id, "fn")
    dummy_bkt_arn = f"arn:aws:s3:::{make_throwaway_name(run_id, 'dummy-src')}"

    role_created = False
    fn_created = False

    try:
        assert_throwaway_name(role_name)
        assert_throwaway_name(fn_name)
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
                {"Key": "run_id", "Value": run_id},
            ],
        )
        role_arn = r_resp["Role"]["Arn"]
        role_created = True
        ledger.record_created("iam_role", role_name, role_name, metadata={"arn": role_arn})

        # Wait briefly for IAM role propagation before CreateFunction.
        time.sleep(10.0)

        lam.create_function(
            FunctionName=fn_name,
            Runtime="python3.12",
            Role=role_arn,
            Handler="index.handler",
            Code={"ZipFile": _make_noop_lambda_zip("v1")},
            Description="Throwaway Tessera detection test function",
            Timeout=3,
            MemorySize=128,
            Tags={PURPOSE_TAG_KEY: PURPOSE_TAG_VALUE, "run_id": run_id},
        )
        fn_created = True
        ledger.record_created("lambda_function", fn_name, fn_name)
        _wait_lambda_ready(lam, fn_name)

        # 1. UpdateFunctionConfiguration
        t_cfg = utc_now_iso()
        lam.update_function_configuration(FunctionName=fn_name, Timeout=4)
        ledger.record_event(
            ["D7-lambda-config"],
            "lambda:UpdateFunctionConfiguration",
            resource_name=fn_name,
            started_at_utc=t_cfg,
            ended_at_utc=utc_now_iso(),
        )
        _wait_lambda_ready(lam, fn_name)

        # 2. UpdateFunctionCode
        t_code = utc_now_iso()
        lam.update_function_code(
            FunctionName=fn_name,
            ZipFile=_make_noop_lambda_zip("v2"),
        )
        ledger.record_event(
            ["D7-lambda-code"],
            "lambda:UpdateFunctionCode",
            resource_name=fn_name,
            started_at_utc=t_code,
            ended_at_utc=utc_now_iso(),
        )
        _wait_lambda_ready(lam, fn_name)

        # 3. AddPermission (supplementary check per Brief)
        t_perm = utc_now_iso()
        lam.add_permission(
            FunctionName=fn_name,
            StatementId="tessera-dtest-perm",
            Action="lambda:InvokeFunction",
            Principal="s3.amazonaws.com",
            SourceArn=dummy_bkt_arn,
        )
        ledger.record_event(
            ["D7-sup-lambda-perm"],
            "lambda:AddPermission",
            resource_name=fn_name,
            started_at_utc=t_perm,
            ended_at_utc=utc_now_iso(),
        )
        lam.remove_permission(FunctionName=fn_name, StatementId="tessera-dtest-perm")
    finally:
        if fn_created:
            try:
                assert_throwaway_name(fn_name)
                lam.delete_function(FunctionName=fn_name)
                ledger.record_deleted("lambda_function", fn_name)
            except Exception as exc:
                ledger.record_deleted("lambda_function", fn_name, status="cleanup_failed", detail=str(exc))
        if role_created:
            try:
                assert_throwaway_name(role_name)
                iam.delete_role(RoleName=role_name)
                ledger.record_deleted("iam_role", role_name)
            except Exception as exc:
                ledger.record_deleted("iam_role", role_name, status="cleanup_failed", detail=str(exc))


def run_d7_iam_role(run_id: str, ledger: RunLedger, *, session: Any = None) -> None:
    """D7-iam-role (watcher multi-region trail path, up to ~1 h)."""
    iam = locked_boto3_client("iam", session=session)
    role_name = make_throwaway_name(run_id, "role")
    policy_name = make_throwaway_name(run_id, "inline")

    role_created = False
    policy_attached = False
    try:
        assert_throwaway_name(role_name)
        assert_throwaway_name(policy_name)
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
        t0 = utc_now_iso()
        r_resp = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust),
            Description="Throwaway IAM role for Tessera D7 watcher detection test",
            Tags=[
                {"Key": PURPOSE_TAG_KEY, "Value": PURPOSE_TAG_VALUE},
                {"Key": "run_id", "Value": run_id},
            ],
        )
        role_created = True
        ledger.record_created("iam_role", role_name, role_name, metadata={"arn": r_resp["Role"]["Arn"]})

        deny_all = {
            "Version": "2012-10-17",
            "Statement": [{"Effect": "Deny", "Action": "*", "Resource": "*"}],
        }
        iam.put_role_policy(
            RoleName=role_name,
            PolicyName=policy_name,
            PolicyDocument=json.dumps(deny_all),
        )
        policy_attached = True

        iam.delete_role_policy(RoleName=role_name, PolicyName=policy_name)
        policy_attached = False

        ledger.record_event(
            ["D7-iam-role"],
            "iam:CreateRole + PutRolePolicy + DeleteRolePolicy + DeleteRole",
            resource_name=role_name,
            started_at_utc=t0,
            ended_at_utc=utc_now_iso(),
            details={"note": "IAM events are read by watcher from multi-region trail (up to ~1 h)."},
        )
    finally:
        if policy_attached:
            try:
                assert_throwaway_name(role_name)
                iam.delete_role_policy(RoleName=role_name, PolicyName=policy_name)
            except Exception as exc:
                ledger.add_note(f"iam:DeleteRolePolicy cleanup note for {role_name}: {exc}")
        if role_created:
            try:
                assert_throwaway_name(role_name)
                iam.delete_role(RoleName=role_name)
                ledger.record_deleted("iam_role", role_name)
            except Exception as exc:
                ledger.record_deleted("iam_role", role_name, status="cleanup_failed", detail=str(exc))


def run_d7_iam_access_key(run_id: str, ledger: RunLedger, *, session: Any = None) -> None:
    """D7-iam-accesskey (opt-in): create zero-perm throwaway user + access key, delete immediately.

    Hard Safety Rule 5: AccessKeyId and SecretAccessKey are NEVER printed, logged,
    or written to the ledger.
    """
    iam = locked_boto3_client("iam", session=session)
    user_name = make_throwaway_name(run_id, "user")
    user_created = False
    access_key_id: str | None = None

    try:
        assert_throwaway_name(user_name)
        t0 = utc_now_iso()
        iam.create_user(
            UserName=user_name,
            Tags=[
                {"Key": PURPOSE_TAG_KEY, "Value": PURPOSE_TAG_VALUE},
                {"Key": "run_id", "Value": run_id},
            ],
        )
        user_created = True
        ledger.record_created("iam_user", user_name, user_name)

        ak_resp = iam.create_access_key(UserName=user_name)
        access_key_id = ak_resp["AccessKey"]["AccessKeyId"]
        # Immediately discard secret material; never log either ID or secret.
        ak_resp.clear()
        ledger.record_event(
            ["D7-iam-accesskey"],
            "iam:CreateAccessKey + DeleteAccessKey (zero-perm throwaway user)",
            resource_name=user_name,
            started_at_utc=t0,
            ended_at_utc=utc_now_iso(),
            details={"note": "Credentials discarded immediately; never recorded (Rule 5)."},
        )
    finally:
        if access_key_id and user_created:
            try:
                assert_throwaway_name(user_name)
                iam.delete_access_key(UserName=user_name, AccessKeyId=access_key_id)
            except Exception as exc:
                ledger.add_note(f"iam:DeleteAccessKey cleanup error for {user_name}: {exc}")
            finally:
                access_key_id = None
        if user_created:
            try:
                assert_throwaway_name(user_name)
                iam.delete_user(UserName=user_name)
                ledger.record_deleted("iam_user", user_name)
            except Exception as exc:
                ledger.record_deleted("iam_user", user_name, status="cleanup_failed", detail=str(exc))


def run_d7_cloudtrail(run_id: str, ledger: RunLedger, *, session: Any = None) -> None:
    """D7-ct-update, D7-ct-selectors, D7-ct-stop, D7-ct-delete on a throwaway trail (opt-in).

    Never touches the production trail or production trail bucket.
    """
    s3 = locked_boto3_client("s3", session=session)
    ct = locked_boto3_client("cloudtrail", session=session)
    account_id = _caller_account_id(session=session)
    bkt_name = make_throwaway_name(run_id, "ct-bkt")
    trail_name = make_throwaway_name(run_id, "trail")
    trail_arn = f"arn:aws:cloudtrail:{ALLOWED_REGION}:{account_id}:trail/{trail_name}"

    bkt_created = False
    trail_created = False
    trail_deleted = False

    try:
        assert_throwaway_name(bkt_name)
        assert_throwaway_name(trail_name)
        s3.create_bucket(
            Bucket=bkt_name,
            CreateBucketConfiguration={"LocationConstraint": ALLOWED_REGION},
        )
        bkt_created = True
        ledger.record_created("s3_bucket", bkt_name, bkt_name)
        s3.put_bucket_tagging(
            Bucket=bkt_name,
            Tagging={
                "TagSet": [
                    {"Key": PURPOSE_TAG_KEY, "Value": PURPOSE_TAG_VALUE},
                    {"Key": "run_id", "Value": run_id},
                ]
            },
        )
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
        s3.put_bucket_policy(Bucket=bkt_name, Policy=json.dumps(ct_policy))

        ct.create_trail(
            Name=trail_name,
            S3BucketName=bkt_name,
            IsMultiRegionTrail=False,
            TagsList=[
                {"Key": PURPOSE_TAG_KEY, "Value": PURPOSE_TAG_VALUE},
                {"Key": "run_id", "Value": run_id},
            ],
        )
        trail_created = True
        ledger.record_created("cloudtrail", trail_name, trail_name, metadata={"arn": trail_arn})

        t_upd = utc_now_iso()
        ct.update_trail(Name=trail_name, EnableLogFileValidation=True)
        ledger.record_event(
            ["D7-ct-update"],
            "cloudtrail:UpdateTrail",
            resource_name=trail_name,
            started_at_utc=t_upd,
            ended_at_utc=utc_now_iso(),
        )

        t_sel = utc_now_iso()
        ct.put_event_selectors(
            TrailName=trail_name,
            EventSelectors=[{"ReadWriteType": "ReadOnly", "IncludeManagementEvents": True}],
        )
        ledger.record_event(
            ["D7-ct-selectors"],
            "cloudtrail:PutEventSelectors",
            resource_name=trail_name,
            started_at_utc=t_sel,
            ended_at_utc=utc_now_iso(),
        )

        t_stop = utc_now_iso()
        ct.stop_logging(Name=trail_name)
        ledger.record_event(
            ["D7-ct-stop"],
            "cloudtrail:StopLogging",
            resource_name=trail_name,
            started_at_utc=t_stop,
            ended_at_utc=utc_now_iso(),
        )

        t_del = utc_now_iso()
        ct.delete_trail(Name=trail_name)
        trail_deleted = True
        ledger.record_deleted("cloudtrail", trail_name)
        ledger.record_event(
            ["D7-ct-delete"],
            "cloudtrail:DeleteTrail",
            resource_name=trail_name,
            started_at_utc=t_del,
            ended_at_utc=utc_now_iso(),
        )
    finally:
        if trail_created and not trail_deleted:
            try:
                assert_throwaway_name(trail_name)
                ct.delete_trail(Name=trail_name)
                ledger.record_deleted("cloudtrail", trail_name)
            except Exception as exc:
                ledger.record_deleted("cloudtrail", trail_name, status="cleanup_failed", detail=str(exc))
        if bkt_created:
            try:
                assert_throwaway_name(bkt_name)
                _empty_throwaway_bucket(s3, bkt_name)
                s3.delete_bucket(Bucket=bkt_name)
                ledger.record_deleted("s3_bucket", bkt_name)
            except Exception as exc:
                ledger.record_deleted("s3_bucket", bkt_name, status="cleanup_failed", detail=str(exc))


def _empty_throwaway_bucket(s3: Any, bucket_name: str) -> None:
    assert_throwaway_name(bucket_name)
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket_name):
        objs = [{"Key": o["Key"]} for o in page.get("Contents", [])]
        if objs:
            s3.delete_objects(Bucket=bucket_name, Delete={"Objects": objs})


def run_d7_sup_sqs(run_id: str, ledger: RunLedger, *, session: Any = None) -> None:
    """D7-sup-sqs: supplementary check on throwaway SQS queue."""
    sqs = locked_boto3_client("sqs", session=session)
    q_name = make_throwaway_name(run_id, "q")
    q_url: str | None = None
    try:
        assert_throwaway_name(q_name)
        t0 = utc_now_iso()
        q_url = sqs.create_queue(
            QueueName=q_name,
            tags={PURPOSE_TAG_KEY: PURPOSE_TAG_VALUE, "run_id": run_id},
        )["QueueUrl"]
        assert_throwaway_name(q_url)
        ledger.record_created("sqs_queue", q_url, q_name)
        sqs.set_queue_attributes(QueueUrl=q_url, Attributes={"VisibilityTimeout": "45"})
        ledger.record_event(
            ["D7-sup-sqs"],
            "sqs:CreateQueue + SetQueueAttributes",
            resource_name=q_name,
            started_at_utc=t0,
            ended_at_utc=utc_now_iso(),
        )
    finally:
        if q_url:
            try:
                assert_throwaway_name(q_url)
                sqs.delete_queue(QueueUrl=q_url)
                ledger.record_deleted("sqs_queue", q_url)
            except Exception as exc:
                ledger.record_deleted("sqs_queue", q_url, status="cleanup_failed", detail=str(exc))


def run_d7_sup_ddb(run_id: str, ledger: RunLedger, *, session: Any = None) -> None:
    """D7-sup-ddb: supplementary check on throwaway DynamoDB table (UpdateTimeToLive)."""
    ddb = locked_boto3_client("dynamodb", session=session)
    tbl_name = make_throwaway_name(run_id, "tbl")
    created = False
    try:
        assert_throwaway_name(tbl_name)
        t0 = utc_now_iso()
        ddb.create_table(
            TableName=tbl_name,
            AttributeDefinitions=[{"AttributeName": "pk", "AttributeType": "S"}],
            KeySchema=[{"AttributeName": "pk", "KeyType": "HASH"}],
            BillingMode="PAY_PER_REQUEST",
            Tags=[
                {"Key": PURPOSE_TAG_KEY, "Value": PURPOSE_TAG_VALUE},
                {"Key": "run_id", "Value": run_id},
            ],
        )
        created = True
        ledger.record_created("dynamodb_table", tbl_name, tbl_name)
        ddb.get_waiter("table_exists").wait(TableName=tbl_name)

        t_ttl = utc_now_iso()
        ddb.update_time_to_live(
            TableName=tbl_name,
            TimeToLiveSpecification={"Enabled": True, "AttributeName": "ttl"},
        )
        ledger.record_event(
            ["D7-sup-ddb"],
            "dynamodb:CreateTable + UpdateTimeToLive",
            resource_name=tbl_name,
            started_at_utc=t_ttl,
            ended_at_utc=utc_now_iso(),
            details={"created_at": t0},
        )
    finally:
        if created:
            try:
                assert_throwaway_name(tbl_name)
                ddb.delete_table(TableName=tbl_name)
                ledger.record_deleted("dynamodb_table", tbl_name)
            except Exception as exc:
                ledger.record_deleted("dynamodb_table", tbl_name, status="cleanup_failed", detail=str(exc))


def run_d7_sup_cw(run_id: str, ledger: RunLedger, *, session: Any = None) -> None:
    """D7-sup-cw: supplementary check on throwaway CloudWatch alarm."""
    cw = locked_boto3_client("cloudwatch", session=session)
    alarm_name = make_throwaway_name(run_id, "alarm")
    created = False
    try:
        assert_throwaway_name(alarm_name)
        t0 = utc_now_iso()
        cw.put_metric_alarm(
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
                {"Key": "run_id", "Value": run_id},
            ],
        )
        created = True
        ledger.record_created("cloudwatch_alarm", alarm_name, alarm_name)
        ledger.record_event(
            ["D7-sup-cw"],
            "cloudwatch:PutMetricAlarm + DeleteAlarms",
            resource_name=alarm_name,
            started_at_utc=t0,
            ended_at_utc=utc_now_iso(),
        )
    finally:
        if created:
            try:
                assert_throwaway_name(alarm_name)
                cw.delete_alarms(AlarmNames=[alarm_name])
                ledger.record_deleted("cloudwatch_alarm", alarm_name)
            except Exception as exc:
                ledger.record_deleted("cloudwatch_alarm", alarm_name, status="cleanup_failed", detail=str(exc))


def run_d7_sup_logs(run_id: str, ledger: RunLedger, *, session: Any = None) -> None:
    """D7-sup-logs: supplementary check on throwaway CloudWatch Logs group."""
    logs = locked_boto3_client("logs", session=session)
    # No leading slash so log group name starts strictly with tessera-dtest-.
    group_name = make_throwaway_name(run_id, "logs")
    created = False
    try:
        assert_throwaway_name(group_name)
        t0 = utc_now_iso()
        logs.create_log_group(
            logGroupName=group_name,
            tags={PURPOSE_TAG_KEY: PURPOSE_TAG_VALUE, "run_id": run_id},
        )
        created = True
        ledger.record_created("log_group", group_name, group_name)
        logs.put_retention_policy(logGroupName=group_name, retentionInDays=1)
        ledger.record_event(
            ["D7-sup-logs"],
            "logs:CreateLogGroup + PutRetentionPolicy + DeleteLogGroup",
            resource_name=group_name,
            started_at_utc=t0,
            ended_at_utc=utc_now_iso(),
        )
    finally:
        if created:
            try:
                assert_throwaway_name(group_name)
                logs.delete_log_group(logGroupName=group_name)
                ledger.record_deleted("log_group", group_name)
            except Exception as exc:
                ledger.record_deleted("log_group", group_name, status="cleanup_failed", detail=str(exc))


def run_d7_sup_eb(run_id: str, ledger: RunLedger, *, session: Any = None) -> None:
    """D7-sup-eb: supplementary check on throwaway EventBridge rule."""
    eb = locked_boto3_client("events", session=session)
    rule_name = make_throwaway_name(run_id, "rule")
    created = False
    try:
        assert_throwaway_name(rule_name)
        t0 = utc_now_iso()
        eb.put_rule(
            Name=rule_name,
            EventPattern=json.dumps({"source": ["tessera.dtest.noop"]}),
            State="DISABLED",
            Description="Throwaway Tessera detection test rule",
            Tags=[
                {"Key": PURPOSE_TAG_KEY, "Value": PURPOSE_TAG_VALUE},
                {"Key": "run_id", "Value": run_id},
            ],
        )
        created = True
        ledger.record_created("eventbridge_rule", rule_name, rule_name)
        ledger.record_event(
            ["D7-sup-eb"],
            "events:PutRule + DeleteRule",
            resource_name=rule_name,
            started_at_utc=t0,
            ended_at_utc=utc_now_iso(),
        )
    finally:
        if created:
            try:
                assert_throwaway_name(rule_name)
                eb.delete_rule(Name=rule_name)
                ledger.record_deleted("eventbridge_rule", rule_name)
            except Exception as exc:
                ledger.record_deleted("eventbridge_rule", rule_name, status="cleanup_failed", detail=str(exc))


def cleanup_from_ledger_file(ledger_path: Any, *, session: Any = None) -> list[str]:
    """Crash-recovery sweep: deletes active/cleanup_failed resources recorded in a ledger.

    Refuses any resource whose name does not start with tessera-dtest- (except
    the observer SNS subscription whose name starts with tessera-dtest-*).
    """
    from pathlib import Path

    raw = load_ledger(Path(ledger_path))
    actions: list[str] = []
    for entry in reversed(raw.get("resources", [])):
        if entry.get("status") in ("deleted", "scheduled_deletion"):
            continue
        rtype = entry["resource_type"]
        ident = entry["identifier"]
        name = entry.get("name", "")
        if rtype != "sns_observer_subscription":
            assert_throwaway_name(name, allow_alias_prefix=(rtype == "kms_alias"))
        else:
            if not name.startswith("tessera-dtest-"):
                raise RuntimeError(f"Refusing to unsubscribe non-dtest subscription: {name!r}")

        try:
            if rtype == "sns_observer_subscription":
                locked_boto3_client("sns", session=session).unsubscribe(SubscriptionArn=ident)
            elif rtype in ("sqs_queue", "sqs_observer_queue"):
                assert_throwaway_name(ident)
                locked_boto3_client("sqs", session=session).delete_queue(QueueUrl=ident)
            elif rtype == "sns_topic":
                assert_throwaway_name(ident)
                locked_boto3_client("sns", session=session).delete_topic(TopicArn=ident)
            elif rtype == "s3_bucket":
                assert_throwaway_name(ident)
                s3 = locked_boto3_client("s3", session=session)
                _empty_throwaway_bucket(s3, ident)
                s3.delete_bucket(Bucket=ident)
            elif rtype == "kms_alias":
                assert_throwaway_name(ident, allow_alias_prefix=True)
                locked_boto3_client("kms", session=session).delete_alias(AliasName=ident)
            elif rtype == "kms_key":
                resp = locked_boto3_client("kms", session=session).schedule_key_deletion(
                    KeyId=ident, PendingWindowInDays=7
                )
                actions.append(
                    f"scheduled kms_key {ident} ({name}) deletes on {resp['DeletionDate'].strftime('%Y-%m-%d')}"
                )
                continue
            elif rtype == "lambda_function":
                assert_throwaway_name(ident)
                locked_boto3_client("lambda", session=session).delete_function(FunctionName=ident)
            elif rtype == "iam_role":
                assert_throwaway_name(ident)
                iam = locked_boto3_client("iam", session=session)
                for p in iam.list_role_policies(RoleName=ident).get("PolicyNames", []):
                    iam.delete_role_policy(RoleName=ident, PolicyName=p)
                iam.delete_role(RoleName=ident)
            elif rtype == "iam_user":
                assert_throwaway_name(ident)
                iam = locked_boto3_client("iam", session=session)
                for k in iam.list_access_keys(UserName=ident).get("AccessKeyMetadata", []):
                    iam.delete_access_key(UserName=ident, AccessKeyId=k["AccessKeyId"])
                iam.delete_user(UserName=ident)
            elif rtype == "cloudtrail":
                assert_throwaway_name(ident)
                locked_boto3_client("cloudtrail", session=session).delete_trail(Name=ident)
            elif rtype == "dynamodb_table":
                assert_throwaway_name(ident)
                locked_boto3_client("dynamodb", session=session).delete_table(TableName=ident)
            elif rtype == "cloudwatch_alarm":
                assert_throwaway_name(ident)
                locked_boto3_client("cloudwatch", session=session).delete_alarms(AlarmNames=[ident])
            elif rtype == "log_group":
                assert_throwaway_name(ident)
                locked_boto3_client("logs", session=session).delete_log_group(logGroupName=ident)
            elif rtype == "eventbridge_rule":
                assert_throwaway_name(ident)
                locked_boto3_client("events", session=session).delete_rule(Name=ident)
            elif rtype == "apigw_usage_plan":
                locked_boto3_client("apigateway", session=session).delete_usage_plan(usagePlanId=ident)
            elif rtype == "apigw_api_key":
                locked_boto3_client("apigateway", session=session).delete_api_key(apiKey=ident)
            elif rtype == "apigw_rest_api":
                locked_boto3_client("apigateway", session=session).delete_rest_api(restApiId=ident)
            else:
                actions.append(f"skipped unknown type {rtype} {ident}")
                continue
            actions.append(f"deleted {rtype} {name} ({ident})")
        except Exception as exc:
            actions.append(f"failed {rtype} {name} ({ident}): {exc}")
    return actions
