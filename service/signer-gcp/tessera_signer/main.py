"""Entry point of the Cloud Run job: read the configuration from the environment, check the HSM key, obtain AWS
credentials by web identity federation, and run once. Exit status 0 after a run (refusals included); 2 when the
signer refuses to run at all (configuration or key mismatch), so the job execution shows as failed.

Environment (all required unless a default is shown):
  REQUEST_QUEUE_URL, RESPONSE_QUEUE_URL   the issuer's gpg-slot queues (Terraform output signer_queues.gpg)
  FRAME_BUCKET                            the issuer's result bucket (Terraform output result_bucket); IS-09 frames
  AWS_ROLE_ARN, AWS_AUDIENCE              the web-identity role and the ID-token audience its trust requires
  AWS_CHAIN_ROLE_ARN (optional)           a second role to assume with the first role's credentials
  AWS_REGION_QUEUES (us-east-2)
  KMS_KEY_VERSION                         projects/.../cryptoKeys/<key>/cryptoKeyVersions/<n>
  KEY_CREATED, KEY_FP                     OpenPGP creation time bound into the fingerprint; the pinned gpg-sha256 fp
  SIGN_UNTIL                              the window's signing stop (not-after minus 96 h), RFC 3339 UTC second
  SIGNER_IMAGE (unknown), RUN_SECONDS (40), WAIT_SECONDS (5), VISIBILITY_SECONDS (120)"""
import json
import re
import sys
import time
from dataclasses import dataclass

from tessera_verify.codec import Fault, utc

from .signer import Signer, StartupError

RE_FP = re.compile(r"gpg-sha256:[0-9a-f]{64}")
RE_KEY_VERSION = re.compile(r"projects/[^/]+/locations/[^/]+/keyRings/[^/]+/cryptoKeys/[^/]+/cryptoKeyVersions/[0-9]+")


@dataclass(frozen=True)
class Config:
    request_queue_url: str
    response_queue_url: str
    frame_bucket: str
    key_version: str
    key_created: int
    key_fp: str
    sign_until: int
    aws_role_arn: str
    aws_audience: str
    aws_region: str = "us-east-2"
    aws_chain_role_arn: str | None = None
    image: str = "unknown"
    budget_s: int = 40
    wait_s: int = 5
    visibility_s: int = 120


def config_from_env(env):
    """-> Config, or raises StartupError naming the first bad variable."""
    def need(name):
        v = env.get(name, "")
        if not v:
            raise StartupError(f"{name} is not set")
        return v

    def integer(name, default=None, lo=0, hi=None):
        raw = env.get(name, "") or (None if default is None else str(default))
        if raw is None:
            raise StartupError(f"{name} is not set")
        if not raw.isdigit() or int(raw) < lo or (hi is not None and int(raw) > hi):
            raise StartupError(f"{name}={raw!r} is not an integer in range")
        return int(raw)

    key_version, key_fp = need("KMS_KEY_VERSION"), need("KEY_FP")
    if not RE_KEY_VERSION.fullmatch(key_version):
        raise StartupError("KMS_KEY_VERSION is not a full key-version resource name")
    if not RE_FP.fullmatch(key_fp):
        raise StartupError("KEY_FP is not gpg-sha256:<64 hex>")
    try:
        sign_until = utc(need("SIGN_UNTIL"))
    except Fault:
        raise StartupError("SIGN_UNTIL is not an RFC 3339 UTC second (YYYY-MM-DDTHH:MM:SSZ)") from None
    return Config(request_queue_url=need("REQUEST_QUEUE_URL"), response_queue_url=need("RESPONSE_QUEUE_URL"),
                  frame_bucket=need("FRAME_BUCKET"), key_version=key_version,
                  key_created=integer("KEY_CREATED", lo=1, hi=2**32 - 1), key_fp=key_fp, sign_until=sign_until,
                  aws_role_arn=need("AWS_ROLE_ARN"), aws_audience=need("AWS_AUDIENCE"),
                  aws_region=env.get("AWS_REGION_QUEUES") or "us-east-2",
                  aws_chain_role_arn=env.get("AWS_CHAIN_ROLE_ARN") or None,
                  image=env.get("SIGNER_IMAGE") or "unknown", budget_s=integer("RUN_SECONDS", 40, 1, 3000),
                  wait_s=integer("WAIT_SECONDS", 5, 0, 20), visibility_s=integer("VISIBILITY_SECONDS", 120, 30, 43200))


def log(**fields):
    print(json.dumps(fields, sort_keys=True, default=str), flush=True)


def from_env(env):
    from . import gcp
    cfg = config_from_env(env)
    md = gcp.Metadata()
    kms = gcp.GcpKms(cfg.key_version, md.access_token)
    signer = Signer(cfg, kms, None, None, lambda: int(time.time()), time.monotonic, log)
    signer.load_key()                     # before any AWS credential is obtained or any message is read
    signer.sqs, signer.s3 = gcp.aws_clients(cfg.aws_role_arn, cfg.aws_audience, cfg.aws_region, md.id_token,
                                            gcp.boto3_client, cfg.aws_chain_role_arn)
    return signer


def main(env=None):
    import os
    try:
        signer = from_env(os.environ if env is None else env)
    except StartupError as e:
        log(event="refuse_to_run", error=str(e))
        return 2
    signer.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
