"""Infrastructure as code (DESIGN.md test group 4). Nothing is applied or planned. Static checks always run;
`terraform fmt -check` and `terraform validate` run only where a terraform binary and an already-initialised
provider exist locally (no download, no account)."""
import re
import shutil
import subprocess
from pathlib import Path

import pytest

from tessera_issue import lambda_app

INFRA = Path(__file__).resolve().parents[1] / "infra"
TF = {f.name: f.read_text() for f in sorted(INFRA.glob("*.tf"))}
ALL = "\n".join(TF.values())


def strip_strings_and_comments(text):
    text = re.sub(r'"(?:[^"\\]|\\.)*"', '""', text)
    return re.sub(r"#[^\n]*", "", text)


def test_files_present_and_balanced():
    assert set(TF) == {"versions.tf", "variables.tf", "main.tf", "outputs.tf"}
    for name, text in TF.items():
        bare = strip_strings_and_comments(text)
        for o, c in ("{}", "[]", "()"):
            assert bare.count(o) == bare.count(c), (name, o)


def test_issuer_has_no_kms_permission_and_no_kms_resource():
    assert not re.search(r"kms:[A-Za-z*]", ALL)
    assert "aws_kms" not in ALL and "kms_master_key_id" not in ALL and "aws:kms" not in ALL
    assert 'sse_algorithm = "AES256"' in ALL and "sqs_managed_sse_enabled    = true" in ALL


def test_request_store_dynamodb_with_ttl_and_pending_index():
    m = TF["main.tf"]
    assert 'resource "aws_dynamodb_table" "requests"' in m
    assert re.search(r'ttl \{\s*attribute_name = "expires_at"\s*enabled\s*= true', m)
    assert 'name            = "pending-index"' in m


def test_result_store_s3_lifecycle_30_days_on_every_prefix():
    m = TF["main.tf"]
    assert re.search(r'for_each = \["content/", "work/", "frames/", "result/"\]', m)
    assert re.search(r"retention = 30", m) and "days = local.retention" in m
    assert "block_public_policy     = true" in m and "aws:SecureTransport" in m


def test_signer_queues_and_wake_topics_per_slot():
    m = TF["main.tf"]
    for r in ('resource "aws_sqs_queue" "requests"', 'resource "aws_sqs_queue" "responses"',
              'resource "aws_sns_topic" "wake"'):
        assert r in m
    assert m.count("for_each                   = toset(local.slots)") == 2
    assert 'slots     = ["kms", "gpg"]' in m


def test_api_gateway_requires_api_keys_on_every_route():
    m = TF["main.tf"]
    assert "api_key_required = true" in m and 'authorization    = "NONE"' in m
    routes = re.search(r"routes = \{(.*?)\n  \}", m, re.S).group(1)
    assert routes.count("method") == 3 and '"POST"' in routes and routes.count('"GET"') == 2
    for path in ('"v1"', '"requests"', '"{key}"', '"receipt"'):
        assert f"path_part   = {path}" in m
    assert 'resource "aws_api_gateway_usage_plan_key" "client"' in m


def test_lambdas_point_at_real_handlers_and_get_every_variable_from_env_reads():
    m = TF["main.tf"]
    for handler in re.findall(r'handler\s+= "tessera_issue\.lambda_app\.(\w+)"', m):
        assert callable(getattr(lambda_app, handler))
    assert 'schedule_expression = "rate(10 minutes)"' in m and "reserved_concurrent_executions = 1" in m
    env_block = re.search(r"lambda_env = \{(.*?)\n  \}", m, re.S).group(1)
    provided = set(re.findall(r"^\s+([A-Z_]+)\s+=", env_block, re.M))
    src = Path(lambda_app.__file__).read_text()
    read = set(re.findall(r'env\["([A-Z_]+)"\]', src)) | set(re.findall(r'env\.get\("([A-Z_]+)"', src))
    assert read <= provided, read - provided


@pytest.mark.skipif(shutil.which("terraform") is None, reason="terraform not installed (offline build host)")
def test_terraform_fmt_and_validate_offline():
    r = subprocess.run(["terraform", "fmt", "-check", "-recursive"], cwd=INFRA, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    if not (INFRA / ".terraform").exists():
        pytest.skip("providers not initialised locally; init would download")
    r = subprocess.run(["terraform", "validate"], cwd=INFRA, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
