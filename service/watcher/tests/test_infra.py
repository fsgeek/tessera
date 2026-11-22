"""The watcher's Terraform (service/detect/infra/watcher.tf), read as text: its role writes only its own stores and
the alarm topic, reads the issuer's stores, and the trace bucket is Object Lock COMPLIANCE."""
import json
import re
from pathlib import Path

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
    assert writes == {"s3:PutObject", "s3:PutObjectRetention", "sns:Publish", "cloudwatch:PutMetricData"}
    for sid, (acts, body) in st.items():
        if any(a.startswith("s3:Put") for a in acts):
            assert "aws_s3_bucket.trace" in body or "aws_s3_bucket.watcher_state" in body, sid
            assert "var.results_bucket" not in body and "var.trail_bucket" not in body, sid
        if "sns:Publish" in acts:
            assert "aws_sns_topic.alarms.arn" in body
        if any(a.startswith("dynamodb:") for a in acts):
            assert set(acts) <= {"dynamodb:Scan", "dynamodb:GetItem", "dynamodb:DescribeTable"}


def test_results_bucket_read_is_result_prefix_only():
    st = statements()
    (body,) = [b for acts, b in st.values() if "var.results_bucket" in b]
    assert '/result/*' in body


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


def test_retention_is_computed_from_the_window_record():
    assert "jsondecode(file(" in TF and "not_after" in TF and "var.trace_retention_days_after_window" in TF
    win = json.loads((Path(__file__).resolve().parents[2] / "issuer" / "config" / "window.json").read_text())
    assert win["not_after"] == "2027-02-01T00:00:00Z"
