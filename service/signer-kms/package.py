"""Build the KMS signer's Lambda package (infra variable lambda_zip): tessera_sign_kms, tessera_verify (its frame
decoder and signature check) and cryptography for Lambda's Linux. No SHA-1DC detector and no install record: the
signer never verifies a receipt. boto3 comes from the Lambda runtime. Reuses the issuer's builder (same wheel,
platform and deterministic zip).

    python package.py OUT.zip"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "issuer"))
import package as issuer_package  # noqa: E402  service/issuer/package.py


def build(out):
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc", "*.egg-info")
    with tempfile.TemporaryDirectory() as tmp:
        stage = Path(tmp) / "stage"
        subprocess.run(["uv", "pip", "install", "--quiet", "--target", str(stage), "--python-version", "3.14",
                        "--python-platform", issuer_package.PLATFORM, "--only-binary", ":all:",
                        *issuer_package.WHEEL], check=True)
        shutil.copytree(HERE / "tessera_sign_kms", stage / "tessera_sign_kms", ignore=ignore)
        shutil.copytree(issuer_package.VERIFIER / "tessera_verify", stage / "tessera_verify", ignore=ignore)
        return issuer_package.write_zip(stage, out)


if __name__ == "__main__":
    out = Path(sys.argv[1])
    print(f"{out}\nsha256 {build(out)}")
