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
import base64
import json
import subprocess
import time
import uuid
from pathlib import Path

from common import PROTO, gen, tc, log, now, read_json, sha256hex, write_json


SLOT2_JOB = {"name": "slot2-signer", "project": "tessera-slot2", "region": "us-east1"}


class Ledger:
    """Every signature the run has ever produced or found, and every slot-2 request id it has enqueued (E-02).
    <run>/sigs/orphans.json: {"signatures": [{source, request_id?, frame_sha256, signature_sha256, at, ...}]}
    <run>/sigs/requests.json: {"requests": {request_id: {frame_sha256, resolved}}, "triggers": [...]}
    Both are written atomically on every change, so a crash mid-stage loses nothing already recorded."""

    def __init__(self, run_dir):
        self.orph, self.req = Path(run_dir, "sigs", "orphans.json"), Path(run_dir, "sigs", "requests.json")

    def _load(self, f, empty):
        return read_json(f) if f.exists() else empty

    def signature(self, source, frame, sig, **extra):
        d = self._load(self.orph, {"signatures": []})
        sh = sha256hex(bytes(sig))
        if any(e["signature_sha256"] == sh and e["frame_sha256"] == sha256hex(frame) for e in d["signatures"]):
            return
        d["signatures"].append({"source": source, "frame_sha256": sha256hex(frame), "signature_sha256": sh,
                                "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), **extra})
        write_json(self.orph, d)

    def signature_hashes(self, source, frame_sha256, sig_sha256, **extra):    # for files found on disk
        d = self._load(self.orph, {"signatures": []})
        if any(e["signature_sha256"] == sig_sha256 and e["frame_sha256"] == frame_sha256 for e in d["signatures"]):
            return
        d["signatures"].append({"source": source, "frame_sha256": frame_sha256, "signature_sha256": sig_sha256,
                                "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), **extra})
        write_json(self.orph, d)

    def add_request(self, rid, frame):
        d = self._load(self.req, {"requests": {}, "triggers": []})
        d["requests"][rid] = {"frame_sha256": sha256hex(frame), "resolved": False}
        write_json(self.req, d)

    def resolve(self, rid):
        d = self._load(self.req, {"requests": {}, "triggers": []})
        if rid in d["requests"]:
            d["requests"][rid]["resolved"] = True
            write_json(self.req, d)

    def pending(self):
        d = self._load(self.req, {"requests": {}, "triggers": []})
        return {k: v for k, v in d["requests"].items() if not v["resolved"]}

    def trigger(self, entry):
        d = self._load(self.req, {"requests": {}, "triggers": []})
        d["triggers"].append(entry)
        write_json(self.req, d)


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
    ledger = None            # set by the sign stage (signers.Ledger)

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
        if self.ledger is not None:                      # E-02(b): recorded before any check, kept even if the stage fails
            self.ledger.signature("kms-sign", msg, sig)
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
    (prototype/spike-pq/out-gcp/capture.json); the signer itself refuses frames outside its policy.

    E-01: the signer only runs on Cloud Scheduler ticks (normally paused). With trigger=True each request batch is
    followed by one explicit `gcloud run jobs execute ... --async` (logged), so the scheduler stays paused.
    E-02: request ids are written to <run>/sigs/requests.json before enqueue; before a batch, responses to ids this run
    enqueued earlier are drained from the response queue and every signature found is recorded in orphans.json."""
    slot, real = "gpg", True
    ledger = None            # set by the sign stage (signers.Ledger)

    def __init__(self, trigger=True, job=None, client_module=None):
        if client_module is None:
            import sys
            sys.path.insert(0, str(PROTO / "policy-signer"))
            import client   # prototype/policy-signer/client.py (aws CLI, profile tessera)
        else:
            client = client_module
        self.client = client
        self.trigger_on_demand, self.job = trigger, {**SLOT2_JOB, **(job or {})}
        (x, y, created), self.fp = client.gpg_key()
        self.point, self.created = (x, y), created
        self.key_bytes = gen.openpgp_v4_body(gen._point(x, y), created)
        assert gen.fp_gpg(gen._point(x, y), created) == self.fp

    # -- E-01
    def trigger(self):
        if not self.trigger_on_demand:
            log("slot-2 on-demand trigger disabled by run.json; relying on the scheduler")
            return
        j = self.job
        cmd = ["gcloud", "run", "jobs", "execute", j["name"], "--project", j["project"], "--region", j["region"],
               "--async"]
        log("triggering slot-2 signer on demand:", " ".join(cmd))
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if self.ledger is not None:
            self.ledger.trigger({"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "cmd": cmd,
                                 "returncode": p.returncode})
        if p.returncode:
            raise RuntimeError(f"slot-2 trigger failed ({p.returncode}): {p.stderr.strip()[:300]}")
        log("slot-2 trigger accepted:", (p.stdout + p.stderr).strip()[:200])

    # -- E-02(a)
    def drain(self, max_polls=10):
        """Read the response queue; for every message whose request_id this run enqueued earlier and has not resolved,
        record the signature and delete the message. Other messages are left alone."""
        if self.ledger is None:
            return 0
        found = 0
        for _ in range(max_polls):
            pend = self.ledger.pending()
            if not pend:
                break
            msgs = self.client.aws("sqs", "receive-message", "--queue-url", self.client.RESP,
                                   "--max-number-of-messages", "10", "--wait-time-seconds", "2",
                                   "--visibility-timeout", "30").get("Messages", [])
            if not msgs:
                break
            for m in msgs:
                body = json.loads(m["Body"])
                rid = body.get("request_id")
                if rid not in pend:
                    continue
                if body.get("status") == "SIGNED" and body.get("sig_b64"):
                    self.ledger.signature_hashes("slot2-orphan-response", pend[rid]["frame_sha256"],
                                                 sha256hex(base64.b64decode(body["sig_b64"])), request_id=rid)
                self.ledger.resolve(rid)
                self.client.aws("sqs", "delete-message", "--queue-url", self.client.RESP,
                                "--receipt-handle", m["ReceiptHandle"])
                found += 1
        if found:
            log(f"drained {found} earlier slot-2 response(s); see sigs/orphans.json")
        return found

    def sign_batch(self, msgs):
        """Sign several frames in one request batch: drain, enqueue all, one trigger, wait for all."""
        self.drain()
        rids = []
        for m in msgs:
            rid = "req-" + uuid.uuid4().hex
            if self.ledger is not None:
                self.ledger.add_request(rid, m)         # recorded BEFORE the enqueue
            self.client.enqueue(m, rid)
            rids.append(rid)
        self.trigger()
        out = []
        for rid, m in zip(rids, msgs):
            r = self.client.wait(rid)
            if self.ledger is not None:
                self.ledger.resolve(rid)
            if r.get("status") == "SIGNED" and r.get("sig_b64"):
                sig = base64.b64decode(r["sig_b64"])
                if self.ledger is not None:
                    self.ledger.signature("slot2-response", m, sig, request_id=rid)
            out.append((rid, r))
        self.drain()                                    # catch responses to earlier ids processed by this execution
        res = []
        for (rid, r), m in zip(out, msgs):
            if r.get("status") != "SIGNED":
                raise RuntimeError(f"policy signer refused: {r.get('reason')} {r.get('detail')}")
            sig = base64.b64decode(r["sig_b64"])
            if not self.verify(m, sig):
                raise RuntimeError("policy-signer signature does not verify")
            res.append(sig)
        return res

    def sign(self, msg):
        return self.sign_batch([msg])[0]

    def verify(self, msg, sig):
        return gen.verify_openpgp4(msg, sig, self.point)


def make(cfg):
    """cfg['signers'] = {"kind": "test"} | {"kind": "real", "kms_key_id": ..., "aws_profile": ..., "region": ...}"""
    s = cfg["signers"]
    if s["kind"] == "test":
        return TestKms(), TestGpg()
    if s["kind"] == "real":
        return (AwsKmsMldsa(s["kms_key_id"], s.get("region", "us-east-2"), s.get("aws_profile", "tessera")),
                PolicySignerGpg(trigger=s.get("trigger_slot2", True), job=s.get("slot2_job")))
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
