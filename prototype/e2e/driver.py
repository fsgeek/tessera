#!/usr/bin/env python3
"""V1 issuer driver (instrument): one receipt from real material, issued in the profile's order (V1-PROFILE §4) plus
the further issuer duties, every stage resumable from files on disk.

Stages (each runs once; its record goes into <run>/state.json and its outputs into <run>/):

  freeze         TEST freeze objects + catalog (freeze.py), or the directory named in run.json
  keys           slot public keys from the signers (real: KMS GetPublicKey; the slot-2 archived capture)
  assertion      the ENC §7 255-byte value for (kms, gpg, window) -> assertion.txt and txt-record.txt
  repo           TEST repository key (fresh GNUPGHOME under work/) and the signed key-assertion commit (repo.py)
  stamp-git      OTS stamp of SHA256(<commit id>\\n)
  wait-git       upgrade until the git proof has k = 6 (h_git + 5 <= tip): chain-order pre-commitment (§4, §6.3)
  frames         manifest frame, common metadata with declared_issue_time = now, both attestation frames
  sign           S_kms, S_gpg and both possession signatures; each verified on the exact bytes, then frozen
  asig           A_sig (ENC §5) and the full receipt check (P8 implementation A) before stamping
  stamp-receipt  one OTS stamp of SHA256(A_sig), only after the k = 6 git confirmation was observed
  dns            DNSSEC capture, §15.3 conversion, no-wildcard check, validation now, TXT value == assertion
  stamp-dns      OTS stamp of SHA256(ENC §6 envelope)
  wait           upgrade the receipt and snapshot proofs until both have k = 6
  headers        headers h..h+5 of each proof's lowest attestation (real: two explorers must agree)
  check          pre-ship checks: selection, contradiction, tx shape + merkle suffix on all three proofs, txid,
                 c1-c3 on receipt and snapshot, h_git + 5 < h_receipt, window, DNSSEC at T_snap, channel equality
  assemble       canonical JCS container (§15.1) -> bundle.json
  trust          §15.5 trust configuration with pins for the three proofs -> trust.json
  release        TEST release record (tessera-v1-test-release/1) signed by a TEST release key -> release.json
  verify         the independent verifier through prototype/differential/adapter.py (T1: the signed TEST release
                 provisions it) -> verdict.json

Modes. `dry`: local TEST signers (conformance tcrypto), stub OTS calendar and chain, stub DNS resolver (TEST
hierarchy), TEST root KSKs; real GnuPG and git for the repository; no network. `real`: AWS KMS ML-DSA-65 (boto3),
the GCP policy signer via SQS, public OTS calendars, live DNS, two-explorer headers, archived IANA root KSKs.

  uv run python e2e/driver.py dry-run [--run DIR]
  uv run python e2e/driver.py init --run DIR --mode real --kms-key-id alias/... --not-before T --not-after T
  uv run python e2e/driver.py run --run DIR [--until STAGE]
  uv run python e2e/driver.py status --run DIR
"""
import argparse
import json
import os
import struct
import subprocess
import sys
import time
from pathlib import Path

from common import (D, PROTO, WORK, U, gen, tc, b64, b64d, jcs, log, now, read_json, sha256, sha256hex,
                    write_atomic, write_json)
import dnssnap
import freeze
import otsutil
import repo as R
import signers as SG
import trustcfg

STAGES = ["freeze", "keys", "assertion", "repo", "stamp-git", "wait-git", "frames", "sign", "asig", "stamp-receipt",
          "dns", "stamp-dns", "wait", "headers", "check", "assemble", "trust", "release", "verify"]
POLICY_VERSION = "tessera-v1-issue-policy/1"


class IssueRefused(Exception):
    pass


class Waiting(Exception):
    """A wait stage timed out; rerun `run` later. Exit code 75."""


class Run:
    def __init__(self, d):
        self.d = Path(d)
        self.cfg = read_json(self.d / "run.json")
        sf = self.d / "state.json"
        self.state = read_json(sf) if sf.exists() else {}
        self._ots = None

    def p(self, *a):
        return self.d.joinpath(*a)

    def save(self):
        write_json(self.p("state.json"), self.state)

    @property
    def dry(self):
        return self.cfg["mode"] == "dry"

    @property
    def ots(self):
        if self._ots is None:
            self._ots = otsutil.StubOts(self.p("stub-chain.json")) if self.dry else otsutil.RealOts()
        return self._ots

    def tip(self):
        if self.dry:
            return self.ots.tip()
        import btcheaders
        return btcheaders.tip()

    def fetch_headers(self, heights):
        if self.dry:
            return self.ots.headers(heights)
        import btcheaders
        return btcheaders.fetch(heights)

    def freeze_objects(self):
        return freeze.load(self.state["freeze"]["dir"])

    def keys(self):
        k = read_json(self.p("keys.json"))
        body = b64d(k["gpg_key_b64"])
        k["gpg_created"] = struct.unpack(">I", body[1:5])[0]
        pt = body[17:]
        k["gpg_xy"] = (int.from_bytes(pt[1:33], "big"), int.from_bytes(pt[33:65], "big"))
        k["kms_spki"] = b64d(k["kms_key_b64"])
        return k

    def signers(self):
        return SG.make(self.cfg)

    def root_ksks(self):
        if self.cfg["roots"]["kind"] == "test":
            return U.trust_config({"0": "0" * 64})["root_ksks"]
        arch = Path(self.cfg["roots"].get("archive") or trustcfg.ARCHIVE)
        if not (arch / "sources.json").exists():
            trustcfg.fetch_roots(arch)
        return trustcfg.roots(arch)

    def trusted_root_rdatas(self):
        return [b64d(e["dnskey_rdata"]) for e in self.root_ksks()]


# ------------------------------------------------------------------------------------------------ stages
def st_freeze(r):
    d = r.cfg.get("freeze_dir")
    if not d or not Path(d, "freeze-record.json").exists():
        d = str(freeze.assemble(r.cfg.get("freeze_commit", "HEAD"), d))
    freeze.check_agreement(d)
    rec = read_json(Path(d, "freeze-record.json"))
    return {"dir": d, "commit": rec["commit"], "catalog_sha256": rec["objects"]["catalog.json"]["sha256"]}


def st_keys(r):
    kms, gpg = r.signers()
    k = {"kms_fp": kms.fp, "kms_key_b64": b64(kms.key_bytes), "gpg_fp": gpg.fp, "gpg_key_b64": b64(gpg.key_bytes),
         "signers": r.cfg["signers"]["kind"]}
    gen.check_key_kms(kms.key_bytes, kms.fp)
    write_json(r.p("keys.json"), k)
    return {"kms_fp": kms.fp, "gpg_fp": gpg.fp}


def st_assertion(r):
    k = r.keys()
    w = r.cfg["window"]
    v = R.assertion_value(k["kms_fp"].split(":")[1], k["gpg_fp"].split(":")[1], w["not_before"], w["not_after"])
    write_atomic(r.p("assertion.txt"), v)
    write_atomic(r.p("txt-record.txt"), f"name:  _tessera-v1.{D}.\ntype:  TXT\nvalue: (one character-string, exactly "
                 f"{len(v)} bytes, no quotes split)\n{v.decode()}\n")
    return {"value_sha256": sha256hex(v), "len": len(v)}


def st_repo(r):
    key = R.make_key(r.cfg.get("repo_key_dir") or r.p("repo-key"))
    ev = R.commit_assertion(key, r.cfg.get("repo_dir") or r.p("issuer-repo"), r.p("assertion.txt").read_bytes(),
                            r.p("git"))
    R.stop_agent(key)
    return {"commit_id": ev["commit_id"], "repo_key_fpr": key["fpr_v4"], "repo_key_created": key["created_rfc3339"]}


def _stamp(r, path):
    ots = r.ots.stamp(path)
    d, _, _ = otsutil.parse(Path(ots).read_bytes())
    if d != sha256(Path(path).read_bytes()):
        raise IssueRefused(f"{ots}: file digest is not SHA-256 of the stamped file")
    return {"ots": str(ots), "stamped_at": U.rfc3339(now()), "tip_at_stamp": r.tip()}


def st_stamp_git(r):
    return _stamp(r, r.p("git", "git-stamp.txt"))


def _wait(r, files):
    poll, deadline = r.cfg.get("poll_s", 300), time.time() + r.cfg.get("max_wait_s", 4 * 3600)
    while True:
        tip = r.tip()
        status = {}
        for f in files:
            r.ots.upgrade(f)
            status[str(f)] = otsutil.k6_ready(f, tip)
        if all(ok for ok, _ in status.values()):
            return {"tip": tip, "lowest_heights": {Path(f).name: h for f, (_, h) in status.items()}}
        if r.dry:
            r.ots.advance(1)
            continue
        if time.time() > deadline:
            raise Waiting(f"not yet k=6 at tip {tip}: {status}")
        log(f"waiting for k=6 at tip {tip}: {status}; next poll in {poll} s")
        time.sleep(poll)


def st_wait_git(r):
    out = _wait(r, [r.p("git", "git-stamp.txt.ots")])
    out["h_git_lowest"] = out["lowest_heights"]["git-stamp.txt.ots"]
    return out


def txt_preflight(r):
    """Real mode, before declared_issue_time is fixed: the published TXT must already validate and equal the
    assertion, so that no receipt is signed and stamped while its DNS evidence cannot exist."""
    value = r.p("assertion.txt").read_bytes()
    cap = dnssnap.capture(r.cfg["dns"]["server"])
    try:
        res = dnssnap.validate(dnssnap.convert(cap), r.trusted_root_rdatas(), now())
    except dnssnap.SnapshotError as e:
        raise IssueRefused(f"TXT preflight: {e}; publish txt-record.txt first") from None
    if not res["ok"] or res["value"] != value:
        raise IssueRefused(f"TXT preflight: published value does not validate or differs: {res['errors']}")


def st_frames(r):
    if not r.dry:
        txt_preflight(r)
    fo, k = r.freeze_objects(), r.keys()
    cat = fo["catalog"]
    declared = U.rfc3339(now())
    w = r.cfg["window"]
    if not U.ts(w["not_before"]) <= U.ts(declared) <= U.ts(w["not_after"]):
        raise IssueRefused(f"declared {declared} outside the window {w}")
    fm = gen.encode_manifest(cat["alg"], D, k["kms_fp"], k["gpg_fp"])
    common = {"alg": cat["alg"], "binding_forms": ["STMT_DIRECT"], "content": r.cfg["content"],
              "declared_issue_time": declared, "issuer": D, "manifest_sha256": sha256hex(fm),
              "preamble_sha256": cat["preamble_sha256"], "profile": gen.PROFILE,
              "spec": {"id": cat["spec_id"], "sha256": cat["spec_sha256"]}, "vectors_sha256": cat["vectors_sha256"]}
    assert sha256hex(fo["preamble.bin"]) == cat["preamble_sha256"] and sha256hex(fo["spec.bin"]) == cat["spec_sha256"]
    write_atomic(r.p("frames", "manifest.bin"), fm)
    write_atomic(r.p("frames", "f_kms.bin"), gen.encode_attest(common, k["kms_fp"]))
    write_atomic(r.p("frames", "f_gpg.bin"), gen.encode_attest(common, k["gpg_fp"]))
    write_json(r.p("frames", "common.json"), common)
    return {"declared_issue_time": declared, "f_kms_len": len(r.p("frames", "f_kms.bin").read_bytes())}


SIG_FILES = ("s_kms.bin", "s_gpg.bin", "p_kms.bin", "p_gpg.bin")


def _sign_jobs(r):
    fm, fk, fg = (r.p("frames", n).read_bytes() for n in ("manifest.bin", "f_kms.bin", "f_gpg.bin"))
    return (("s_kms.bin", fk, 0), ("s_gpg.bin", fg, 1), ("p_kms.bin", fm, 0), ("p_gpg.bin", fm, 1))


def _verified_set_on_disk(r, kms, gpg):
    """E-02(c): the four frozen signatures, if all exist and each verifies over its exact bytes; else None."""
    if not all(r.p("sigs", n).exists() for n in SIG_FILES):
        return None
    out = {}
    for name, msg, slot in _sign_jobs(r):
        b = r.p("sigs", name).read_bytes()
        try:
            gen.decode_sig(b, gen.ALG_HYBRID, slot)
        except gen.Reject:
            return None
        if not (kms, gpg)[slot].verify(msg, b):
            return None
        out[name] = b
    return out


def st_sign(r):
    kms, gpg = r.signers()
    k = r.keys()
    if kms.fp != k["kms_fp"] or gpg.fp != k["gpg_fp"]:
        raise IssueRefused("signer keys changed since the keys stage")
    ledger = SG.Ledger(r.d)
    kms.ledger = gpg.ledger = ledger
    have = _verified_set_on_disk(r, kms, gpg)
    if have is not None:                         # idempotent per frame: no KMS call, no queue request, no trigger
        log("sign: complete verified signature set already on disk; reusing it")
        return {**{n: sha256hex(b) for n, b in have.items()}, "reused": True}
    for name, msg, _ in _sign_jobs(r):           # stale or partial files are about to be replaced: keep their hashes
        f = r.p("sigs", name)
        if f.exists():
            ledger.signature_hashes("replaced-on-disk", sha256hex(msg), sha256hex(f.read_bytes()), file=name)
    jobs = _sign_jobs(r)
    out = {}
    out["s_kms.bin"] = kms.sign(jobs[0][1])
    out["p_kms.bin"] = kms.sign(jobs[2][1])
    if hasattr(gpg, "sign_batch"):               # one request batch, one slot-2 trigger
        out["s_gpg.bin"], out["p_gpg.bin"] = gpg.sign_batch([jobs[1][1], jobs[3][1]])
    else:
        out["s_gpg.bin"], out["p_gpg.bin"] = gpg.sign(jobs[1][1]), gpg.sign(jobs[3][1])
    for name, msg, slot in jobs:
        gen.decode_sig(out[name], gen.ALG_HYBRID, slot)              # slot rule codec (R for kms, O for gpg)
        if not (kms, gpg)[slot].verify(msg, out[name]):
            raise IssueRefused(f"step 4: {name} does not verify over its exact bytes")
    for n, b in out.items():                                           # step 5: frozen
        write_atomic(r.p("sigs", n), bytes(b))
    return {n: sha256hex(b) for n, b in out.items()}


def st_asig(r):
    k = r.keys()
    fm, fk, fg = (r.p("frames", n).read_bytes() for n in ("manifest.bin", "f_kms.bin", "f_gpg.bin"))
    sk, sg, pk, pg = (r.p("sigs", n).read_bytes() for n in ("s_kms.bin", "s_gpg.bin", "p_kms.bin", "p_gpg.bin"))
    a = gen.encode_anchor(fk, sk, fg, sg)
    gq = (k["gpg_xy"][0], k["gpg_xy"][1], k["gpg_created"])
    gen.check_receipt(fm, fk, sk, fg, sg, a, (k["kms_spki"], gq))     # raises gen.Reject
    gen.check_possession(fm, 0, pk, k["kms_spki"])
    gen.check_possession(fm, 1, pg, gq)
    write_atomic(r.p("a_sig.bin"), a)
    return {"a_sig_sha256": sha256hex(a), "receipt_id": sha256hex(a), "len": len(a)}


def st_stamp_receipt(r):
    hg = r.state["wait-git"]["h_git_lowest"]
    tip = r.tip()
    if not hg + 5 <= tip:
        raise IssueRefused(f"chain order: git proof not yet k=6 (h_git {hg}, tip {tip})")
    return _stamp(r, r.p("a_sig.bin"))


def _jsonable(res):
    return {**res, "value": res["value"].decode("ascii", "replace") if res["value"] is not None else None}


def st_dns(r):
    value = r.p("assertion.txt").read_bytes()
    cap = dnssnap.stub_capture(value) if r.cfg["dns"]["kind"] == "stub" else dnssnap.capture(r.cfg["dns"]["server"])
    write_json(r.p("dns", "capture.json"), cap)
    body = dnssnap.convert(cap)
    res = dnssnap.validate(body, r.trusted_root_rdatas(), now())
    write_json(r.p("dns", "validate-at-capture.json"), _jsonable(res))
    if not res["ok"] or res["value"] != value:
        raise IssueRefused(f"snapshot does not validate now or TXT != assertion: {res['errors']}; recapture")
    write_atomic(r.p("dns", "snapshot-body.bin"), body)
    write_atomic(r.p("dns", "snapshot-envelope.bin"), dnssnap.envelope(body))
    return {"server": cap["server"], "joint_window": [U.rfc3339(x) for x in res["window"]], "body_len": len(body)}


def st_stamp_dns(r):
    return _stamp(r, r.p("dns", "snapshot-envelope.bin"))


def st_wait(r):
    return _wait(r, [r.p("a_sig.bin.ots"), r.p("dns", "snapshot-envelope.bin.ots")])


PROOFS = {"receipt": "a_sig.bin.ots", "snapshot": "dns/snapshot-envelope.bin.ots", "git": "git/git-stamp.txt.ots"}


def st_headers(r):
    heights = set()
    for name, f in PROOFS.items():
        _, btc, _ = otsutil.parse(r.p(f).read_bytes())
        h = min(a.height for a in btc)
        heights.update(range(h, h + 6))
    hdrs = r.fetch_headers(sorted(heights))
    write_json(r.p("headers.json"), {str(h): v.hex() for h, v in sorted(hdrs.items())})
    return {"heights": sorted(heights)}


def preship(r):
    """Honest-issuer pre-ship checks (§4). -> (report dict, facts dict)."""
    hdrs = {int(h): bytes.fromhex(v) for h, v in read_json(r.p("headers.json")).items()}
    pins = {h: otsutil.pin_of(v) for h, v in hdrs.items()}
    common = read_json(r.p("frames", "common.json"))
    d = U.ts(common["declared_issue_time"])
    w = r.cfg["window"]
    expect = {"receipt": sha256(r.p("a_sig.bin").read_bytes()),
              "snapshot": sha256(r.p("dns", "snapshot-envelope.bin").read_bytes()),
              "git": sha256(r.p("git", "git-stamp.txt").read_bytes())}
    rep, facts = {}, {}
    for name, f in PROOFS.items():
        dig, btc, _ = otsutil.parse(r.p(f).read_bytes())
        rep[f"{name}_digest"] = dig == expect[name]
        h, T, conf, atts, contra = otsutil.select(btc, hdrs, pins)
        rep[f"{name}_no_contradiction"] = not contra
        rep[f"{name}_anchored"] = h is not None
        txids = []
        for a in atts:
            try:
                txids.append(otsutil.path_tx(a))
            except otsutil.OtsError:
                pass
        rep[f"{name}_tx_shape_and_suffix"] = bool(txids)
        facts[name] = {"h": h, "T": T, "confirmed_at": conf, "txid": txids[0] if txids else None}
        if name in ("receipt", "snapshot") and h is not None:
            rep[f"{name}_c1"] = d - U.EPS <= T
            rep[f"{name}_c2"] = T <= d + U.DELTA
            rep[f"{name}_c3"] = conf <= d + U.DELTA
    fr, fg, fs = facts["receipt"], facts["git"], facts["snapshot"]
    if fr["h"] is not None and fg["h"] is not None:
        rep["chain_order_h_git_plus_5_lt_h_receipt"] = fg["h"] + 5 < fr["h"]
    if fr["T"] is not None:
        rep["window"] = U.ts(w["not_before"]) <= d and fr["T"] <= U.ts(w["not_after"])
    body = r.p("dns", "snapshot-body.bin").read_bytes()
    rep["snapshot_wildcard_free"] = dnssnap.wildcard_free(body)
    if fs["T"] is not None:
        v = dnssnap.validate(body, r.trusted_root_rdatas(), fs["T"])
        rep["dnssec_valid_at_T_snap"] = v["ok"]
        rep["dns_value_equals_git_blob"] = v["value"] == r.p("git", "blob.bin").read_bytes()
        rep["dns_value_equals_manifest_keys"] = v["value"] == r.p("assertion.txt").read_bytes()
    return rep, facts


def st_check(r):
    rep, facts = preship(r)
    write_json(r.p("preship.json"), {"checks": rep, "facts": facts})
    bad = [k for k, v in rep.items() if v is not True]
    if bad:
        raise IssueRefused("pre-ship checks failed: " + ", ".join(bad))
    return {"T": U.rfc3339(facts["receipt"]["T"]), "h_receipt": facts["receipt"]["h"], "h_git": facts["git"]["h"],
            "h_snapshot": facts["snapshot"]["h"], "txid": facts["receipt"]["txid"], "checks": len(rep)}


def st_assemble(r):
    fo, k = r.freeze_objects(), r.keys()
    hdrs = read_json(r.p("headers.json"))
    facts = read_json(r.p("preship.json"))["facts"]
    common = read_json(r.p("frames", "common.json"))
    rd = lambda *a: r.p(*a).read_bytes()  # noqa: E731
    layer = {
        "a_sig": b64(rd("a_sig.bin")),
        "dependency_manifest": b64(fo["dependency-manifest.json"]),
        "dns": {"ots": b64(rd("dns", "snapshot-envelope.bin.ots")), "snapshot_body": b64(rd("dns", "snapshot-body.bin"))},
        "git": {"blob": b64(rd("git", "blob.bin")), "commit": b64(rd("git", "commit.bin")), "object_format": "sha1",
                "ots": b64(rd("git", "git-stamp.txt.ots")),
                "trees": [b64(rd("git", "tree-root.bin")), b64(rd("git", "tree-sub.bin"))]},
        "headers": hdrs,
        "issuer_record": {"observed_anchor_delay_s": str(max(0, facts["receipt"]["T"] - U.ts(common["declared_issue_time"]))),
                          "policy_version": POLICY_VERSION},
        "keys": {"gpg": k["gpg_key_b64"], "kms": k["kms_key_b64"]},
        "manifest": b64(rd("frames", "manifest.bin")),
        "possession": {"gpg": b64(rd("sigs", "p_gpg.bin")), "kms": b64(rd("sigs", "p_kms.bin"))},
        "preamble": b64(fo["preamble.bin"]),
        "receipt_anchor": {"ots": b64(rd("a_sig.bin.ots")), "txid": facts["receipt"]["txid"]},
        "spec": b64(fo["spec.bin"]),
        "vectors": b64(fo["vectors.bin"]),
    }
    bundle = jcs({"layers": [layer], "profile": gen.PROFILE})
    write_atomic(r.p("bundle.json"), bundle)
    return {"bundle_sha256": sha256hex(bundle), "bytes": len(bundle), "receipt_id": sha256hex(rd("a_sig.bin"))}


def st_trust(r):
    hdrs = {int(h): bytes.fromhex(v) for h, v in read_json(r.p("headers.json")).items()}
    key = read_json(Path(r.cfg.get("repo_key_dir") or r.p("repo-key"), "repo-key.json"))
    latest = max(struct.unpack("<I", v[68:72])[0] for v in hdrs.values())
    as_of = U.rfc3339(max(now(), latest))     # >= every anchored time used, so open entries are not at the horizon
    entry = trustcfg.repo_entry(b64d(key["pgp_body_b64"]), key["created_rfc3339"],
                                "TEST repository key (throwaway GnuPG P-256, prototype/e2e); exported public key",
                                key["export_sha256"], "file:" + key["export_file"])
    tb = trustcfg.build({h: otsutil.pin_of(v) for h, v in hdrs.items()}, as_of, r.root_ksks(), [entry])
    write_atomic(r.p("trust.json"), tb)
    return {"trust_sha256": sha256hex(tb), "as_of": as_of, "pins": len(hdrs), "roots": r.cfg["roots"]["kind"]}


def release_key():
    """The TEST release key (P-256), one per work/ tree. Private seed is TEST material under work/ (git-ignored)."""
    f = WORK / "test-release-key" / "seed.TEST-PRIVATE"
    if not f.exists():
        import secrets
        write_atomic(f, secrets.token_hex(32))
        os.chmod(f, 0o600)
    k = tc.P256Key("e2e TEST release key " + f.read_text().strip())
    pub = {"TEST": "TEST release key of the prototype/e2e pipeline proof; never a production release key",
           "spki_b64": b64(k.spki), "spki_sha256": sha256hex(k.spki)}
    write_json(WORK / "test-release-key" / "release-key.json", pub)
    return k, pub


def st_release(r):
    k, pub = release_key()
    rel = U.make_release(r.p("trust.json").read_bytes(), signer=k, catalog_obj=r.freeze_objects()["catalog"])
    write_atomic(r.p("release.json"), jcs(rel))
    write_json(r.p("release-key.json"), pub)
    return {"release_key_spki_sha256": pub["spki_sha256"], "trust_config_sha256": rel["release"]["trust_config_sha256"]}


def verify_with_indep(trust, bundle, release, release_key_file):
    env = dict(os.environ, TESSERA_V1_TEST_RELEASE=str(release), TESSERA_V1_TEST_RELEASE_KEY=str(release_key_file))
    p = subprocess.run([sys.executable, str(PROTO / "differential" / "adapter.py"), "--trust", str(trust),
                        "--bundle", str(bundle)], env=env, capture_output=True, text=True, timeout=600)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def st_verify(r):
    rc, out, err = verify_with_indep(r.p("trust.json"), r.p("bundle.json"), r.p("release.json"), r.p("release-key.json"))
    res = {"exit": rc, "stdout": out, "stderr": err}
    write_json(r.p("verdict.json"), res)
    if rc != 0:
        raise IssueRefused(f"verifier refused to run (exit {rc}): {err}")
    whole = json.loads(out)
    # The verifier prints {"stable": six, "utc_assessment": {...}} (profile 3.5, 7.4); U never enters the verdict.
    v = dict(whole.get("stable", whole))
    if "utc_assessment" in whole:
        v["utc_assessment"] = whole["utc_assessment"]
    log("independent verifier:", out)
    if v["verdict"] != "VALID_STRICT":
        raise IssueRefused(f"verdict {v['verdict']} / {v['reason']}")
    return v


FUNCS = {s: globals()["st_" + s.replace("-", "_")] for s in STAGES}


def run(d, until=None):
    r = Run(d)
    for s in STAGES:
        if s in r.state:
            continue
        log(f"stage {s} ...")
        t0 = time.time()
        info = FUNCS[s](r)
        info["_done"] = U.rfc3339(now())
        info["_seconds"] = round(time.time() - t0, 2)
        r.state[s] = info
        r.save()
        log(f"stage {s} done: {json.dumps({k: v for k, v in info.items() if not k.startswith('_')})[:300]}")
        if s == until:
            break
    return r


def init(d, mode, kms_key_id=None, not_before=None, not_after=None, freeze_dir=None, freeze_commit="HEAD",
         dns_server="1.1.1.1", content=None):
    d = Path(d)
    if (d / "run.json").exists():
        raise SystemExit(f"{d} already initialised")
    t = now()
    if mode == "dry":
        nb, na = U.rfc3339(t - t % 86400 - 86400), U.rfc3339(t - t % 86400 + 30 * 86400)
    else:
        if not (kms_key_id and not_before and not_after):
            raise SystemExit("real mode needs --kms-key-id, --not-before and --not-after (the published TXT window)")
        nb, na = not_before, not_after
    cfg = {
        "mode": mode, "created": U.rfc3339(t), "freeze_dir": freeze_dir, "freeze_commit": freeze_commit,
        "window": {"not_before": nb, "not_after": na},
        "content": content or {"TEST": "Tessera V1 end-to-end pipeline proof; not a keepsake", "run": d.name,
                               "mode": mode},
        "signers": {"kind": "test"} if mode == "dry" else {"kind": "real", "kms_key_id": kms_key_id,
                                                           "aws_profile": "tessera", "region": "us-east-2",
                                                           "trigger_slot2": True},
        "dns": {"kind": "stub"} if mode == "dry" else {"kind": "real", "server": dns_server},
        "ots": {"kind": "stub" if mode == "dry" else "real"},
        "roots": {"kind": "test"} if mode == "dry" else {"kind": "real", "archive": str(trustcfg.ARCHIVE)},
        "poll_s": 300, "max_wait_s": 4 * 3600,
    }
    write_json(d / "run.json", cfg)
    return d


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a1 = sub.add_parser("dry-run")
    a1.add_argument("--run")
    a2 = sub.add_parser("init")
    a2.add_argument("--run", required=True)
    a2.add_argument("--mode", choices=["dry", "real"], required=True)
    a2.add_argument("--kms-key-id")
    a2.add_argument("--not-before")
    a2.add_argument("--not-after")
    a2.add_argument("--freeze-dir")
    a2.add_argument("--freeze-commit", default="HEAD")
    a3 = sub.add_parser("run")
    a3.add_argument("--run", required=True)
    a3.add_argument("--until", choices=STAGES)
    a4 = sub.add_parser("status")
    a4.add_argument("--run", required=True)
    a = ap.parse_args()
    try:
        if a.cmd == "dry-run":
            d = Path(a.run or WORK / "runs" / ("dry-" + time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())))
            init(d, "dry")
            r = run(d)
            print(json.dumps(r.state["verify"], sort_keys=True))
        elif a.cmd == "init":
            init(a.run, a.mode, a.kms_key_id, a.not_before, a.not_after, a.freeze_dir, a.freeze_commit)
        elif a.cmd == "run":
            run(a.run, a.until)
        elif a.cmd == "status":
            r = Run(a.run)
            for s in STAGES:
                print(f"{s:14s} {'done ' + r.state[s]['_done'] if s in r.state else '-'}")
    except Waiting as e:
        log("WAITING:", e)
        return 75
    except IssueRefused as e:
        log("REFUSED:", e)
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
