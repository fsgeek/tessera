"""Static checks of the signer's Terraform (infra/) and, again from here, of the issuer's (service/issuer/infra):
issuer roles hold no kms: action; the only grant of kms:Sign is the key policy's, to the signer role; everyone else
is denied it; the trail keeps KMS events and writes to an Object Lock COMPLIANCE bucket. Nothing is applied or
planned; fmt/validate run only where terraform and an initialised provider exist locally."""
import re
import shutil
import subprocess
from pathlib import Path

import pytest

from tessera_sign_kms import lambda_app

ROOT = Path(__file__).resolve().parents[1]
INFRA = ROOT / "infra"
ISSUER_INFRA = ROOT.parent / "issuer" / "infra"
TF = {f.name: f.read_text() for f in sorted(INFRA.glob("*.tf"))}
ALL = "\n".join(TF.values())
ISSUER = "\n".join(f.read_text() for f in sorted(ISSUER_INFRA.glob("*.tf")))


def block(text, kind, name):
    """The body of `<kind> "<type>" "<name>" {...}` (kind like 'data "aws_iam_policy_document"'), by brace matching."""
    m = re.search(re.escape(f'{kind} "{name}"') + r"\s*\{", text)
    assert m, (kind, name)
    i, depth = m.end(), 1
    while depth:
        depth += {"{": 1, "}": -1}.get(text[i], 0)
        i += 1
    return text[m.end():i - 1]


def statements(doc):
    out, i = [], 0
    while (m := re.search(r"\n  statement \{", doc[i:])):
        start, depth, j = i + m.end(), 1, i + m.end()
        while depth:
            depth += {"{": 1, "}": -1}.get(doc[j], 0)
            j += 1
        out.append(doc[start:j - 1])
        i = j
    return out


def test_files_present():
    assert set(TF) == {"versions.tf", "variables.tf", "main.tf", "outputs.tf"}


def test_issuer_roles_still_have_no_kms_action():
    assert ISSUER and not re.search(r"kms:[A-Za-z*]", ISSUER)


def test_only_the_key_policy_mentions_kms_actions():
    key_doc = block(ALL, 'data "aws_iam_policy_document"', "key")
    outside = re.sub(r"#[^\n]*", "", ALL.replace(key_doc, ""))           # code, not comments
    assert not re.search(r"kms:[A-Za-z*]", outside), "a kms: action outside the key policy"
    assert "kms:*" not in ALL and "kms:Get*" not in ALL and "kms:CreateGrant" not in ALL
    for name in ("signer", "lambda_assume", "trail_bucket"):
        assert "kms:" not in block(ALL, 'data "aws_iam_policy_document"', name)


def test_only_the_signer_role_is_allowed_kms_sign_and_everyone_else_is_denied():
    sts = statements(block(ALL, 'data "aws_iam_policy_document"', "key"))
    allows = [s for s in sts if "kms:Sign" in s and 'effect    = "Deny"' not in s]
    denies = [s for s in sts if "kms:Sign" in s and 'effect    = "Deny"' in s]
    assert len(allows) == 1 and len(denies) == 1
    assert re.search(r'actions\s*=\s*\["kms:Sign", "kms:GetPublicKey"\]', allows[0])
    assert re.search(r"identifiers = \[aws_iam_role\.signer\.arn\]", allows[0])
    assert "kms:GetPublicKey" not in "".join(s for s in sts if s is not allows[0])
    d = denies[0]
    assert 'identifiers = ["*"]' in d and 'test     = "ArnNotEquals"' in d and '"aws:PrincipalArn"' in d
    assert "values   = [aws_iam_role.signer.arn]" in d
    assert "resource \"aws_kms_key_policy\" \"signer\"" in ALL
    assert 'resource "aws_kms_key" ' not in ALL                     # never creates a key


def test_signer_role_is_assumable_by_lambda_only_and_reads_frames_only():
    assert re.search(r'identifiers = \["lambda\.amazonaws\.com"\]', block(ALL, 'data "aws_iam_policy_document"',
                                                                      "lambda_assume"))
    doc = block(ALL, 'data "aws_iam_policy_document"', "signer")
    assert re.findall(r'"s3:[A-Za-z]+"', doc) == ['"s3:GetObject"'] and "/frames/*" in doc
    assert '"sqs:SendMessage"' in doc and "data.aws_sqs_queue.responses.arn" in doc


def test_trail_keeps_management_events_including_kms_in_a_compliance_locked_bucket():
    trail = block(ALL, 'resource "aws_cloudtrail"', "signer")
    assert re.search(r'equals = \["Management"\]', trail) and "exclude_management_event_sources" not in trail
    assert "read_write_type" not in trail                         # read events (kms:Sign) are not filtered out
    assert "is_multi_region_trail         = true" in trail and "enable_log_file_validation    = true" in trail
    assert "object_lock_enabled = true" in block(ALL, 'resource "aws_s3_bucket"', "trail")
    lock = block(ALL, 'resource "aws_s3_bucket_object_lock_configuration"', "trail")
    assert 'mode = "COMPLIANCE"' in lock and "days = var.trail_retention_days" in lock
    assert 'status = "Enabled"' in block(ALL, 'resource "aws_s3_bucket_versioning"', "trail")
    assert not re.search(r"^\s*default\s*=", block(ALL, "variable", "trail_retention_days"), re.M)   # a conscious, irreversible choice


def test_lambda_handler_env_and_event_source():
    fn = block(ALL, 'resource "aws_lambda_function"', "signer")
    handler = re.search(r'handler\s+= "tessera_sign_kms\.lambda_app\.(\w+)"', fn).group(1)
    assert callable(getattr(lambda_app, handler))
    env_block = re.search(r"signer_env = \{(.*?)\n  \}", ALL, re.S).group(1)
    provided = set(re.findall(r"^\s+([A-Z_]+)\s+=", env_block, re.M))
    src = Path(lambda_app.__file__).read_text()
    read = set(re.findall(r'env\["([A-Z_]+)"\]', src)) | set(re.findall(r'env\.get\("([A-Z_]+)"', src))
    assert read == provided, read ^ provided
    esm = block(ALL, 'resource "aws_lambda_event_source_mapping"', "requests")
    assert '["ReportBatchItemFailures"]' in esm and "data.aws_sqs_queue.requests.arn" in esm
    timeout = int(re.search(r"timeout\s+= (\d+)", fn).group(1))
    visibility = int(re.search(r'aws_sqs_queue" "requests".*?visibility_timeout_seconds = (\d+)', ISSUER, re.S).group(1))
    assert timeout <= visibility                                    # SQS requires it for an event source mapping


@pytest.mark.skipif(shutil.which("terraform") is None, reason="terraform not installed (offline build host)")
def test_terraform_fmt_and_validate_offline():
    r = subprocess.run(["terraform", "fmt", "-check", "-recursive"], cwd=INFRA, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    if not (INFRA / ".terraform").exists():
        pytest.skip("providers not initialised locally; init would download")
    r = subprocess.run(["terraform", "validate"], cwd=INFRA, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
