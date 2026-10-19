"""Pluggable slot signers for the hybrid pair KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256.

Each signer exposes: slot ("kms" | "gpg"), fp (the manifest fingerprint string), key_bytes (the bundle `keys.<slot>`
value: ML-DSA-65 SPKI DER for kms, v4 P-256 public-key body for gpg), sign(frame) -> signature bytes, and
verify(msg, sig) -> bool. Every signature is verified locally before the driver freezes it.

  TestKms / TestGpg       dry run: conformance-universe TEST keys (tcrypto), no network
  AwsKmsMldsa             slot kms: AWS KMS ML-DSA-65 via boto3, EXTERNAL_MU always (supplement §1, owner
                          decision 6). NOT RUN by this build (credentials expired; owner step).
  PolicySignerGpg         slot gpg: the deployed GCP policy signer through SQS (prototype/policy-signer/client.py).
                          NOT RUN by this build (owner step).
"""
import json
import time
from pathlib import Path

from common import PROTO, gen, tc


class TestKms:
    slot, real = "kms", False

    def __init__(self, seed="e2e-dry-run kms (TEST)"):
        self.k = tc.MLDSA65Key(seed)
        self.fp, self.key_bytes = self.k.fp_kms, self.k.spki

    def sign(self, msg):
        return self.k.sign(msg)

    def verify(self, msg, sig):
        return self.k.verify(msg, sig)


class TestGpg:
    slot, real = "gpg", False

    def __init__(self, seed="e2e-dry-run gpg (TEST)", created=None):
        self.k = tc.P256Key(seed, created or 1790000000)
        self.fp, self.key_bytes = self.k.fp_gpg, self.k.pgp_body
        self.point = (self.k.x, self.k.y)

    def sign(self, msg):
        return tc.pgp_sign(msg, self.k, int(time.time()))

    def verify(self, msg, sig):
        return gen.verify_openpgp4(msg, sig, self.point)


class AwsKmsMldsa:
    """AWS KMS ML-DSA-65 (pure, empty context). Signs mu = H(H(pk, 64) || 0x00 0x00 || msg, 64) with MessageType
    EXTERNAL_MU and SigningAlgorithm ML_DSA_SHAKE_256, then checks the signature over the full message locally."""
    slot, real = "kms", True

    def __init__(self, key_id, region="us-east-2", profile="tessera"):
        import boto3   # lazy: only the real run needs it (uv run --with boto3 ...)
        self.kms = boto3.Session(profile_name=profile, region_name=region).client("kms")
        self.key_id = self.kms.describe_key(KeyId=key_id)["KeyMetadata"]["KeyId"]   # never creates
        self.key_bytes = self.kms.get_public_key(KeyId=self.key_id)["PublicKey"]
        self.pk = gen.decode_spki_mldsa65(self.key_bytes)                          # KEY_FORMAT gate
        self.fp = gen.fp_spki(self.key_bytes)

    def sign(self, msg):
        mu = gen.mldsa65_external_mu(self.pk, msg)
        sig = self.kms.sign(KeyId=self.key_id, Message=mu, MessageType="EXTERNAL_MU",
                            SigningAlgorithm="ML_DSA_SHAKE_256")["Signature"]
        if not self.verify(msg, sig):
            raise RuntimeError("KMS signature does not verify over the full message")
        return sig

    def verify(self, msg, sig):
        from cryptography.hazmat.primitives import serialization
        try:
            serialization.load_der_public_key(self.key_bytes).verify(sig, msg)
            return True
        except Exception:  # noqa: BLE001
            return False


class PolicySignerGpg:
    """The slot-2 policy signer (GCP HSM P-256) through the SQS queue. The public key is the archived slot-2 capture
    (prototype/spike-pq/out-gcp/capture.json); the signer itself refuses frames outside its policy."""
    slot, real = "gpg", True

    def __init__(self):
        import sys
        sys.path.insert(0, str(PROTO / "policy-signer"))
        import client   # prototype/policy-signer/client.py (aws CLI, profile tessera)
        self.client = client
        (x, y, created), self.fp = client.gpg_key()
        self.point, self.created = (x, y), created
        self.key_bytes = gen.openpgp_v4_body(gen._point(x, y), created)
        assert gen.fp_gpg(gen._point(x, y), created) == self.fp

    def sign(self, msg):
        import base64
        _, _, r = self.client.submit(msg, "e2e")
        if r.get("status") != "SIGNED":
            raise RuntimeError(f"policy signer refused: {r.get('reason')} {r.get('detail')}")
        sig = base64.b64decode(r["sig_b64"])
        if not self.verify(msg, sig):
            raise RuntimeError("policy-signer signature does not verify")
        return sig

    def verify(self, msg, sig):
        return gen.verify_openpgp4(msg, sig, self.point)


def make(cfg):
    """cfg['signers'] = {"kind": "test"} | {"kind": "real", "kms_key_id": ..., "aws_profile": ..., "region": ...}"""
    s = cfg["signers"]
    if s["kind"] == "test":
        return TestKms(), TestGpg()
    if s["kind"] == "real":
        return (AwsKmsMldsa(s["kms_key_id"], s.get("region", "us-east-2"), s.get("aws_profile", "tessera")),
                PolicySignerGpg())
    raise ValueError(s["kind"])


def offline_public(cfg):
    """Slot public data without any cloud call: for a real config, the archived spike captures (the KMS key's SPKI
    from out-kms/capture.json, the slot-2 key from out-gcp/capture.json). Used to precompute the assertion value."""
    if cfg["signers"]["kind"] == "test":
        k, g = TestKms(), TestGpg()
        return {"kms_fp": k.fp, "gpg_fp": g.fp}
    import base64
    cap_k = json.loads((PROTO / "spike-pq" / "out-kms" / "capture.json").read_text())
    cap_g = json.loads((PROTO / "spike-pq" / "out-gcp" / "capture.json").read_text())
    return {"kms_fp": gen.fp_spki(base64.b64decode(cap_k["spki_b64"])), "gpg_fp": cap_g["key_fp"],
            "source": "archived spike captures; valid only if the owner signs with alias/tessera-pq-spike and slot2-spike"}
