"""The watcher's Terraform (service/detect/infra/watcher.tf), read as text: its role writes only its own stores and
the alarm topic, reads the issuer's stores, and the trace bucket is Object Lock COMPLIANCE."""
import json
import re
from pathlib import Path

from tessera_watch import lambda_app

TF = (Path(__file__).resolve().parents[2] / "detect" / "infra" / "watcher.tf").read_text()


def statements():
    """sid -> (actions, resources text) for the watcher role's policy document."""
    doc = TF[TF.index('data "aws_iam_policy_document" "watcher"'):]
    doc = doc[:doc.index("\n}\n")]
    out = {}
    for m in re.finditer(r'statement \{\s*sid\s*=\s*"(\w+)"(.*?)\n  \}', doc, re.S):
        acts = re.search(r"actions\s*=\s*\[(.*?)\]", m.group(2), re.S).group(1)
        out[m.group(1)] = ([a.strip().strip('"') for a in acts.split(",") if a.strip()], m.group(2))
    return out


def test_role_actions_are_reads_on_issuer_stores_and_writes_on_its_own():
    st = statements()
    writes = {a for acts, _ in st.values() for a in acts if not re.match(
        r"(dynamodb:(Scan|GetItem|DescribeTable)|s3:(GetObject|ListBucket)|logs:(CreateLogStream|PutLogEvents))$", a)}
    assert writes == {"s3:PutObject", "s3:DeleteObject", "sns:Publish", "cloudwatch:PutMetricData"}
    for sid, (acts, body) in st.items():
        if "s3:DeleteObject" in acts:
            assert "aws_s3_bucket.watcher_state.arn}/findings/*" in body and len(re.findall(r"arn", body)) == 1, sid
        if any(a.startswith("s3:Put") or a.startswith("s3:Delete") for a in acts):
            assert "aws_s3_bucket.trace" in body or "aws_s3_bucket.watcher_state" in body, sid
            assert "var.results_bucket" not in body and "var.trail_bucket" not in body, sid
        if "sns:Publish" in acts:
            assert "aws_sns_topic.alarms.arn" in body
        if any(a.startswith("dynamodb:") for a in acts):
            assert set(acts) <= {"dynamodb:Scan", "dynamodb:GetItem", "dynamodb:DescribeTable"}


def test_results_bucket_read_is_result_prefix_only_and_listing_is_unconditional():
    st = statements()
    bodies = {sid: (acts, b) for sid, (acts, b) in st.items() if "var.results_bucket" in b}
    assert set(bodies) == {"ReceiptsRead", "ReceiptsList"}
    assert bodies["ReceiptsRead"][0] == ["s3:GetObject"] and "/result/*" in bodies["ReceiptsRead"][1]
    assert bodies["ReceiptsList"][0] == ["s3:ListBucket"] and "condition" not in bodies["ReceiptsList"][1]


def policy(name):
    doc = TF[TF.index(f'data "aws_iam_policy_document" "{name}"'):]
    return doc[:doc.index("\n}\n")]


def test_trace_bucket_policy_refuses_unlocked_short_foreign_puts_and_any_delete():
    p = policy("trace_bucket")
    for sid in ("DenyPutWithoutComplianceLock", "DenyPutWithoutLockMode", "DenyPutWithoutRetainUntil",
                "DenyPutRetainedTooShort", "DenyPutByOthers", "DenyDeleteAndLockChanges"):
        assert f'sid       = "{sid}"' in p, sid
    assert re.search(r'test\s*=\s*"Null"\s*variable\s*=\s*"s3:object-lock-retain-until-date"', p)
    assert re.search(r'"ArnNotEquals"\s*variable\s*=\s*"aws:PrincipalArn"\s*values\s*=\s*\[aws_iam_role.watcher.arn\]', p)
    deny = p[p.index('"DenyDeleteAndLockChanges"'):]
    assert all(a in deny[:400] for a in ('"s3:DeleteObject"', '"s3:DeleteObjectVersion"',
                                          '"s3:PutBucketObjectLockConfiguration"'))
    assert "condition" not in deny                         # for every principal, without exception
    assert "aws_s3_bucket_object_lock_configuration.trace" in TF[TF.index('resource "aws_s3_bucket_policy" "trace"'):]


def test_state_bucket_writes_only_by_the_watcher():
    p = policy("state_bucket")
    assert '"DenyWritesByOthers"' in p and "aws_iam_role.watcher.arn" in p


def test_trace_bucket_object_lock_compliance():
    b = TF[TF.index('resource "aws_s3_bucket" "trace" {'):]
    assert re.search(r"object_lock_enabled\s*=\s*true", b[:b.index("\n}\n")])
    lock = TF[TF.index('resource "aws_s3_bucket_object_lock_configuration" "trace"'):]
    assert 'mode = "COMPLIANCE"' in lock[:400]


def test_schedule_and_heartbeat_alarm():
    assert 'schedule_expression = "rate(10 minutes)"' in TF
    hb = TF[TF.index('resource "aws_cloudwatch_metric_alarm" "watcher_heartbeat"'):]
    hb = hb[:hb.index("\n}\n")]
    assert 'treat_missing_data  = "breaching"' in hb and "aws_sns_topic.alarms.arn" in hb
    assert re.search(r"period\s*=\s*600", hb) and re.search(r"evaluation_periods\s*=\s*3", hb)
    assert 'expression  = "FILL(hb, 0)"' in hb and re.search(r"datapoints_to_alarm\s*=\s*3", hb)


def test_retention_is_computed_from_the_window_record_with_a_fixed_constant():
    assert "jsondecode(file(" in TF and "not_after" in TF and "local.trace_retention_days * 24" in TF
    assert "var.trace_retention" not in TF and "TRACE_RETAIN_UNTIL" not in TF
    days = int(re.search(r"trace_retention_days\s*=\s*(\d+)", TF).group(1))
    assert days == lambda_app.TRACE_RETENTION_DAYS == 400
    win = json.loads((Path(__file__).resolve().parents[2] / "issuer" / "config" / "window.json").read_text())
    assert win["not_after"] == "2027-02-01T00:00:00Z"
    assert lambda_app.retain_until(win) == "2028-03-07T00:00:00Z"
    lock = TF[TF.index('resource "aws_s3_bucket_object_lock_configuration" "trace"'):]
    assert "days = local.trace_retention_days" in lock[:600]
