"""E-01 (on-demand slot-2 trigger) and E-02 (no orphans on a sign retry). No AWS, no GCP: subprocess and the policy
client are mocked; the SQS queues are an in-memory fake."""
import base64
import json
import subprocess

import pytest

import driver
import signers as SG
from common import gen, tc, write_json, sha256hex


class FakeClient:
    """Stands in for prototype/policy-signer/client.py. Holds fake request/response queues; `signer_runs` controls
    whether the (simulated) Cloud Run job has processed requests yet."""
    RESP = "fake://responses"

    def __init__(self):
        self.key = tc.P256Key("fixes-test gpg (TEST)", 1790000000)
        self.requests, self.responses, self.deleted, self.aws_calls = [], [], [], []
        self.process_on_trigger = True

    def gpg_key(self):
        return (self.key.x, self.key.y, 1790000000), self.key.fp_gpg

    def enqueue(self, frame, request_id=None):
        self.requests.append((request_id, bytes(frame)))
        return request_id, "mid"

    def process(self):
        for rid, fr in self.requests:
            sig = tc.pgp_sign(fr, self.key, 1790000001)
            self.responses.append({"request_id": rid, "status": "SIGNED", "sig_b64": base64.b64encode(sig).decode(),
                                   "signer": {"clock": "x"}})
        self.requests = []

    def wait(self, rid, timeout=240):
        for r in self.responses:
            if r["request_id"] == rid:
                self.responses.remove(r)
                return dict(r, _waited_s=0)
        raise TimeoutError(rid)

    def aws(self, *args):
        self.aws_calls.append(args)
        if args[1] == "receive-message":
            return {"Messages": [{"Body": json.dumps(r), "ReceiptHandle": "h%d" % i}
                                 for i, r in enumerate(self.responses)]}
        if args[1] == "delete-message":
            h = args[args.index("--receipt-handle") + 1]
            self.responses.pop(int(h[1:]))   # single-message tests only
            return {}
        raise AssertionError(args)


@pytest.fixture
def fake_run(monkeypatch):
    calls = []
    fc = FakeClient()

    def fake_run_(cmd, **kw):
        calls.append(cmd)
        if fc.process_on_trigger:
            fc.process()
        return subprocess.CompletedProcess(cmd, 0, "Execution [x] started", "")
    monkeypatch.setattr(SG.subprocess, "run", fake_run_)
    return fc, calls


def test_trigger_command_once_per_batch(fake_run, workdir):
    fc, calls = fake_run
    g = SG.PolicySignerGpg(trigger=True, client_module=fc)
    g.ledger = SG.Ledger(workdir)
    sigs = g.sign_batch([b"frame-a", b"frame-b"])
    assert len(sigs) == 2 and all(g.verify(m, s) for m, s in zip((b"frame-a", b"frame-b"), sigs))
    assert calls == [["gcloud", "run", "jobs", "execute", "slot2-signer", "--project", "tessera-slot2",
                      "--region", "us-east1", "--async"]]
    trig = json.loads((workdir / "sigs" / "requests.json").read_text())["triggers"]
    assert len(trig) == 1 and trig[0]["returncode"] == 0


def test_trigger_disabled_by_config(fake_run, workdir):
    fc, calls = fake_run
    g = SG.PolicySignerGpg(trigger=False, client_module=fc)
    g.ledger = SG.Ledger(workdir)
    fc.process()   # scheduler-driven signer
    fc.process_on_trigger = False
    fc.enqueue = lambda frame, request_id=None: fc.requests.append((request_id, frame)) or fc.process() or (request_id, "m")
    g.sign(b"x")
    assert calls == []


def test_make_default_on_for_real_and_option_off(monkeypatch):
    seen = []
    monkeypatch.setattr(SG, "AwsKmsMldsa", lambda *a, **k: object())
    monkeypatch.setattr(SG, "PolicySignerGpg", lambda **k: seen.append(k) or object())
    SG.make({"signers": {"kind": "real", "kms_key_id": "k"}})
    SG.make({"signers": {"kind": "real", "kms_key_id": "k", "trigger_slot2": False}})
    assert [s["trigger"] for s in seen] == [True, False]
    assert driver.init.__defaults__ is not None   # init writes trigger_slot2 true (checked in the next test)


def test_trigger_failure_is_an_error(monkeypatch, workdir):
    fc = FakeClient()
    monkeypatch.setattr(SG.subprocess, "run", lambda cmd, **kw: subprocess.CompletedProcess(cmd, 1, "", "denied"))
    g = SG.PolicySignerGpg(client_module=fc)
    g.ledger = SG.Ledger(workdir)
    with pytest.raises(RuntimeError, match="trigger failed"):
        g.sign(b"x")


def test_init_real_writes_trigger_option(workdir):
    d = driver.init(workdir / "r", "real", "alias/x", "2026-10-01T00:00:00Z", "2026-11-01T00:00:00Z")
    assert json.loads((d / "run.json").read_text())["signers"]["trigger_slot2"] is True


def test_retry_drains_orphan_responses_and_records_them(fake_run, workdir):
    fc, calls = fake_run
    fc.process_on_trigger = False
    g = SG.PolicySignerGpg(trigger=True, client_module=fc)
    g.ledger = SG.Ledger(workdir)
    with pytest.raises(TimeoutError):                       # attempt 1: signer not running, wait times out
        g.sign_batch([b"frame-1"])
    (rid, frame), = fc.requests
    assert list(g.ledger.pending()) == [rid]
    fc.process()                                            # scheduler resumed later: response now sits in the queue
    fc.process_on_trigger = True
    g.sign_batch([b"frame-1"])                              # attempt 2
    orph = json.loads((workdir / "sigs" / "orphans.json").read_text())["signatures"]
    hit = [e for e in orph if e["source"] == "slot2-orphan-response"]
    assert len(hit) == 1 and hit[0]["request_id"] == rid and hit[0]["frame_sha256"] == sha256hex(b"frame-1")
    assert len(hit[0]["signature_sha256"]) == 64
    assert g.ledger.pending() == {}
    assert fc.responses == []                               # orphan response deleted from the queue


class FakeKms:
    slot, real = "kms", True

    def __init__(self):
        self.k = tc.MLDSA65Key("fixes-test kms (TEST)")
        self.fp, self.key_bytes = self.k.fp_kms, self.k.spki
        self.ledger, self.n = None, 0

    def sign(self, msg):
        self.n += 1
        sig = self.k.sign(msg)
        self.ledger.signature("kms-sign", msg, sig)
        return sig

    def verify(self, msg, sig):
        return self.k.verify(msg, sig)


def _prep_run(workdir, monkeypatch, gpg_sign_ok=True):
    """A Run with frames/keys on disk and fake real-style signers."""
    kms = FakeKms()
    g = driver.SG.TestGpg()
    d = workdir / "run"
    write_json(d / "run.json", {"mode": "dry", "signers": {"kind": "test"}})
    write_json(d / "keys.json", {"kms_fp": kms.fp, "kms_key_b64": base64.b64encode(kms.key_bytes).decode(),
                                 "gpg_fp": g.fp, "gpg_key_b64": base64.b64encode(g.key_bytes).decode()})
    (d / "frames").mkdir()
    fm = gen.encode_manifest(gen.ALG_HYBRID, "wamason.com", kms.fp, g.fp)
    common = {"alg": gen.ALG_HYBRID, "binding_forms": ["STMT_DIRECT"], "content": {"TEST": 1},
              "declared_issue_time": "2026-10-19T00:00:00Z", "issuer": "wamason.com",
              "manifest_sha256": sha256hex(fm), "preamble_sha256": "00" * 32, "profile": gen.PROFILE,
              "spec": {"id": "s", "sha256": "11" * 32}, "vectors_sha256": "22" * 32}
    (d / "frames" / "manifest.bin").write_bytes(fm)
    (d / "frames" / "f_kms.bin").write_bytes(gen.encode_attest(common, kms.fp))
    (d / "frames" / "f_gpg.bin").write_bytes(gen.encode_attest(common, g.fp))
    r = driver.Run(d)
    state = {"gpg_attempts": 0, "ok": gpg_sign_ok}

    class Gpg:
        slot, real, fp, key_bytes, ledger = "gpg", True, g.fp, g.key_bytes, None

        def sign(self, msg):
            state["gpg_attempts"] += 1
            if not state["ok"]:
                raise TimeoutError("no response")
            return g.sign(msg)

        def verify(self, m, s):
            return g.verify(m, s)
    gpg = Gpg()
    monkeypatch.setattr(r, "signers", lambda: (kms, gpg))
    return r, kms, gpg, state


def test_failed_attempt_kms_signatures_recorded_then_retry(workdir, monkeypatch):
    r, kms, gpg, st = _prep_run(workdir, monkeypatch, gpg_sign_ok=False)
    with pytest.raises(TimeoutError):
        driver.st_sign(r)
    first = json.loads((r.d / "sigs" / "orphans.json").read_text())["signatures"]
    assert len(first) == 2 and {e["source"] for e in first} == {"kms-sign"}        # KMS sigs kept despite failure
    assert not (r.d / "sigs" / "s_kms.bin").exists()
    st["ok"] = True
    info = driver.st_sign(r)
    assert set(info) == set(driver.SIG_FILES)
    second = json.loads((r.d / "sigs" / "orphans.json").read_text())["signatures"]
    assert len(second) >= 2 and kms.n == 4     # (test ML-DSA is deterministic so identical sigs dedupe; real KMS is not)


def test_sign_stage_idempotent_when_verified_set_exists(workdir, monkeypatch):
    r, kms, gpg, st = _prep_run(workdir, monkeypatch)
    info1 = driver.st_sign(r)
    n_kms, n_gpg = kms.n, st["gpg_attempts"]
    info2 = driver.st_sign(r)
    assert info2["reused"] is True and kms.n == n_kms and st["gpg_attempts"] == n_gpg   # no new signing at all
    assert {k: v for k, v in info2.items() if k != "reused"} == info1


def test_corrupt_set_is_resigned_and_old_hash_recorded(workdir, monkeypatch):
    r, kms, gpg, st = _prep_run(workdir, monkeypatch)
    driver.st_sign(r)
    f = r.d / "sigs" / "s_kms.bin"
    old = f.read_bytes()
    f.write_bytes(old[:-1] + bytes([old[-1] ^ 1]))
    n = kms.n
    info = driver.st_sign(r)
    assert "reused" not in info and kms.n == n + 2
    orph = json.loads((r.d / "sigs" / "orphans.json").read_text())["signatures"]
    assert any(e["source"] == "replaced-on-disk" and e["file"] == "s_kms.bin" for e in orph)
