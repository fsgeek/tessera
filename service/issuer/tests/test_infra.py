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


def test_result_store_lifecycle_expires_only_cleanup_due_objects():
    """Rewritten for the registered lifecycle (design revision 5.3.1, ILC3-04 / ILC4-01; was
    test_result_store_s3_lifecycle_30_days_on_every_prefix): the former rule expired every object under content/,
    work/, frames/ and result/ 31 days after creation, whatever state its request was in, and could delete a live
    attempt's material. Now no rule expires an object by prefix or age alone; the only expiration is filtered on the
    cleanup-due tag, which the cleanup obligation sets when deletion is due, and the poller may set that tag."""
    from tessera_issue.stores import CLEANUP_TAG
    m = TF["main.tf"]
    block = re.search(r'resource "aws_s3_bucket_lifecycle_configuration" "results" \{(.*?)\n\}', m, re.S).group(1)
    rules = re.findall(r"\n  rule \{(.*?)\n  \}", block, re.S)
    expiring = [r for r in rules if "expiration" in r]
    assert len(expiring) == 1 and "dynamic" not in block and "noncurrent" not in block
    tag = re.search(r'tag \{\s*key\s*= "([^"]+)"\s*value = "([^"]+)"', expiring[0])
    assert tag and (tag.group(1), tag.group(2)) == CLEANUP_TAG
    assert "prefix" not in expiring[0] and "and {" not in expiring[0]
    for r in rules:
        if r is not expiring[0]:
            assert "expiration" not in r and "abort_incomplete_multipart_upload" in r
    for prefix in ("content/", "work/", "frames/", "result/"):
        assert prefix not in block
    objects = re.search(r'sid\s+= "Objects"\s*actions\s+= \[([^\]]*)\]', m).group(1)
    assert '"s3:PutObjectTagging"' in objects
    assert "block_public_policy     = true" in m and "aws:SecureTransport" in m


def test_signer_queues_and_wake_topics_per_slot():
    m = TF["main.tf"]
    for r in ('resource "aws_sqs_queue" "requests"', 'resource "aws_sqs_queue" "responses"',
              'resource "aws_sns_topic" "wake"'):
        assert r in m
    assert m.count("for_each                   = toset(local.slots)") == 2
    assert re.search(r'slots\s+= \["kms", "gpg"\]', m)


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


def test_SG05_both_functions_are_pinned_to_the_install_record_runtime():
    m = (INFRA / "main.tf").read_text()
    block = re.search(r'resource "aws_lambda_runtime_management_config" "pinned" \{(.*?)\n\}', m, re.S).group(1)
    assert 'update_runtime_on   = "Manual"' in block and "var.runtime_version_arn" in block
    assert "aws_lambda_function.api." in block and "aws_lambda_function.poller." in block
