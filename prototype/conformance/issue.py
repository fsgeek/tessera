#!/usr/bin/env python3
"""TEST issuer for the V1 conformance universe: produces complete `tessera-v1-strict` bundles in the profile's
container format (docs/V1-PROFILE.md §15.1) through the documented issue path (§4):

  1. fix manifest and common metadata (declared_issue_time)   2. build both frames      3. sign each frame
  4. verify both signatures over the exact bytes               5. freeze signature bytes 6. build A_sig, stamp it
  7. obtain and validate confirmation/time evidence            8. ship

plus the further issuer duties of §4: chain-order pre-commitment (the key-assertion commit is stamped and
confirmed, k = 6, before the receipt is stamped, so h_git + 5 < h_receipt), the snapshot stamped in the §15.3 body
form with its own proof, c1-c3 checked on the snapshot's own proof, canonical JCS container.

Every key, zone, block and repository here is TEST material. The synthetic chain is not mainnet.

Cases (cases.py) call `issue(**overrides)`; hooks let a case deviate at a named stage, and `adversarial=True`
disables the honest issuer's pre-ship refusals so that negative cases can be built through the same path.

CLI:  prototype/.venv/bin/python prototype/conformance/issue.py --out DIR [--declared 2026-11-10T12:00:00Z]
"""
import argparse
import copy
import hashlib
import json
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tcrypto as tc  # noqa: E402
import universe as U  # noqa: E402
from tcrypto import gen  # noqa: E402

HOUR, DAY = 3600, 86400


class IssueRefused(Exception):
    pass


DEFAULTS = dict(
    timebase="2026-11-10T12:00:00Z",   # anchors the block-time schedule
    declared=None,                     # signed declared_issue_time (defaults to timebase)
    window=None,                       # (not_before, not_after); default (day(timebase) - 9 d, +30 d)
    content={"TEST": "conformance universe: honest requester content", "n": 1},
    installation="classical",          # "classical" (fallback catalog) or "hybrid" (pair id registered and selected)
    kms_scheme="p256",                 # "p256" (rule O, P-256 SPKI) or "mldsa65" (rule R, ML-DSA-65 SPKI; hybrid)
    alg=None, manifest_alg=None,       # alg None: the installation's catalog alg
    binding_forms=["STMT_DIRECT"],
    issuer=U.D, manifest_issuer=None,
    spec_id=U.SPEC_ID, spec_sha256=None, vectors_sha256=None, preamble_sha256=None,
    bundled_spec=None, bundled_vectors=U.VECTORS_BYTES, bundled_preamble=U.PREAMBLE_BYTES,
    bundled_dep=U.DEP_BYTES,
    kms_seed="kms-signer", gpg_seed="gpg-signer", gpg_created=1790000000, repo_seed="repository-key",
    hb=900000, h_git=None, h_snap=None, h_receipt=None,
    times=None,                        # {height: nTime}
    receipt_branches=None, snap_branches=None, git_branches=None,
    chain_extra=(), pins_exclude=(), supply_extra=(), supply_remove=(), header_alt=None, prev_override=None,
    as_of="2026-12-31T00:00:00Z", repo_entries=None, root_ksks=None,
    hooks=None,
    adversarial=False,
)


class Ctx:
    pass


def _day(t):
    return t - t % DAY


def issue(**kw):
    p = copy.deepcopy({k: v for k, v in DEFAULTS.items() if k != "hooks"})
    hooks = kw.pop("hooks", None) or {}
    for k in kw:
        if k not in DEFAULTS:
            raise KeyError(k)
    p.update(kw)
    c = Ctx()
    c.p, c.hooks = p, hooks
    H = lambda name, *a: hooks[name](c, *a) if name in hooks else None  # noqa: E731

    if p["alg"] is None:
        p["alg"] = U.catalog_alg(p["installation"])
    if p["bundled_spec"] is None:
        p["bundled_spec"] = U.spec_bytes(p["installation"])
    tb = U.ts(p["timebase"])
    c.declared = p["declared"] or p["timebase"]
    hb = p["hb"]
    c.h_git = p["h_git"] if p["h_git"] is not None else hb + 2
    c.h_snap = p["h_snap"] if p["h_snap"] is not None else hb + 12
    c.h_receipt = p["h_receipt"] if p["h_receipt"] is not None else hb + 24
    times = dict(p["times"] or {})

    def ntime(h):
        if h in times:
            return times[h]
        if h < hb + 10:
            return tb - 8 * DAY - 12 * HOUR + (h - hb) * 600
        return tb - 2 * HOUR + (h - (hb + 10)) * 600

    c.ntime = ntime
    nb, na = p["window"] or (U.rfc3339(_day(tb) - 9 * DAY), U.rfc3339(_day(tb) + 21 * DAY))
    c.window = (nb, na)

    # ---- 1. keys, manifest and common metadata --------------------------------------------------------------
    c.kms = U.Keys.mldsa65(p["kms_seed"]) if p["kms_scheme"] == "mldsa65" else U.Keys.p256(p["kms_seed"])
    c.gpg = U.Keys.p256(p["gpg_seed"], p["gpg_created"])
    c.repo = U.Keys.p256(p["repo_seed"], 1759276800)
    H("keys")
    c.manifest_value = {"alg": p["manifest_alg"] or p["alg"], "issuer": p["manifest_issuer"] or p["issuer"],
                        "key_fp": c.kms.fp_kms, "sset": [c.gpg.fp_gpg], "ver": "map-v1"}
    H("manifest_value")
    c.F_manifest = gen.frame(gen.T_MANIFEST, U.jcs(c.manifest_value))
    H("manifest_frame")
    c.common = {
        "alg": p["alg"], "binding_forms": p["binding_forms"], "content": p["content"],
        "declared_issue_time": c.declared, "issuer": p["issuer"],
        "manifest_sha256": hashlib.sha256(c.F_manifest).hexdigest(),
        "preamble_sha256": p["preamble_sha256"] or hashlib.sha256(U.PREAMBLE_BYTES).hexdigest(),
        "profile": U.PROFILE,
        "spec": {"id": p["spec_id"],
                 "sha256": p["spec_sha256"] or hashlib.sha256(U.spec_bytes(p["installation"])).hexdigest()},
        "vectors_sha256": p["vectors_sha256"] or hashlib.sha256(U.VECTORS_BYTES).hexdigest(),
    }
    H("common")
    c.common_kms = c.common
    c.common_gpg = c.common
    H("common_slots")

    # ---- 2. frames ---------------------------------------------------------------------------------------------
    def attest(common, fp):
        return gen.frame(gen.T_ATTEST, U.jcs({"common": common, "signer": {"key_fp": fp}}))

    c.F_kms = attest(c.common_kms, c.kms.fp_kms)
    c.F_gpg = attest(c.common_gpg, c.gpg.fp_gpg)
    H("frames")

    # ---- 3. sign; 4. verify; 5. freeze ---------------------------------------------------------------------------
    sig_time = U.ts(c.declared) if 0 <= U.ts(c.declared) < U.U32 else tb
    c.sig_time = sig_time
    c.S_kms = kms_sign(c, c.F_kms)
    c.S_gpg = tc.pgp_sign(c.F_gpg, c.gpg, sig_time)
    H("sign")
    if not p["adversarial"]:
        if not (kms_verify(c, c.F_kms, c.S_kms) and gen.verify_openpgp4(c.F_gpg, c.S_gpg, (c.gpg.x, c.gpg.y))):
            raise IssueRefused("step 4: a signature does not verify over its exact frame bytes")
    c.S_kms, c.S_gpg = bytes(c.S_kms), bytes(c.S_gpg)          # step 5: frozen

    # ---- 6. A_sig ---------------------------------------------------------------------------------------------
    c.A_sig = gen.encode_anchor(c.F_kms, c.S_kms, c.F_gpg, c.S_gpg)
    H("asig")
    c.receipt_digest = hashlib.sha256(c.A_sig).digest()
    H("receipt_digest")

    # possession proofs over F_manifest (rule O per slot, A9 / P§8)
    c.P_kms = kms_sign(c, c.F_manifest)
    c.P_gpg = tc.pgp_sign(c.F_manifest, c.gpg, sig_time)
    H("possession")

    # ---- authority evidence: the key-publication value (ENC §7) ---------------------------------------------
    c.value = gen.dns_value(c.kms.fp_kms.split(":")[1], c.gpg.fp_gpg.split(":")[1], na, nb).encode()
    H("value")
    c.blob = c.value
    H("blob_value")

    # ---- git key assertion (P§6.3, P§15.4) ---------------------------------------------------------------------
    t_git = ntime(c.h_git)
    c.git = build_git(c, t_git)
    H("git")
    finalize_git(c)
    H("git_final")

    # ---- DNSSEC snapshot (P§15.3) -------------------------------------------------------------------------------
    c.T_snap = ntime(c.h_snap)
    c.plan = default_dns_plan(c)
    H("dns_plan")
    c.body = U.serialize_groups(c.plan.groups())
    H("dns_body")
    c.envelope = gen.header(gen.T_SNAPSHOT) + struct.pack(">I", len(c.body)) + c.body
    H("dns_envelope")

    # ---- stamps: git first (chain order), then snapshot, then receipt -----------------------------------------
    c.chain = U.Chain(ntime)
    for h, prev in (p["prev_override"] or {}).items():
        c.chain.prev_override[h] = prev
    c.git_digest = hashlib.sha256(c.git["id"].hex().encode() + b"\n").digest()
    c.snap_digest = hashlib.sha256(c.envelope).digest()
    H("digests")
    c.proofs = {"git": U.Proof(c.git_digest, "git"), "snap": U.Proof(c.snap_digest, "snap"),
                "receipt": U.Proof(c.receipt_digest, "receipt")}
    c.branches = {"git": p["git_branches"] or [{"h": c.h_git}],
                  "snap": p["snap_branches"] or [{"h": c.h_snap}],
                  "receipt": p["receipt_branches"] or [{"h": c.h_receipt}]}
    heights = {hb}
    for name, brs in c.branches.items():
        for i, b in enumerate(brs):
            b.setdefault("label", f"b{i}")
            kind = b.get("kind", "btc")
            if kind == "btc":
                c.proofs[name].add_btc(c.chain, b["h"], label=b["label"], variant=b.get("variant", "std"),
                                       pre=b.get("pre", "nonce"), suffix=b.get("suffix", "conventional"),
                                       contradict=b.get("contradict", False), post=b.get("post", ()))
                heights.add(b["h"])
                if b.get("headers", True) is True:
                    heights.update(range(b["h"], b["h"] + 6))
            elif kind == "pending":
                c.proofs[name].add_pending(**b.get("args", {}))
            elif kind == "raw":
                c.proofs[name].add_raw(b["ops"], b["att"])
    heights.update(p["chain_extra"])
    heights.update(p["supply_extra"])
    c.lo, c.hi = min(heights), max(heights)
    H("chain_pre_build")
    c.chain.build(c.lo, c.hi)
    for pr in c.proofs.values():
        pr.finish(c.chain)
    H("proof_objects")
    c.ots = {k: v.serialize() for k, v in c.proofs.items()}
    H("ots")

    # ---- headers supplied and pins ----------------------------------------------------------------------------
    supplied = set()
    for name, brs in c.branches.items():
        for b in brs:
            if b.get("kind", "btc") != "btc":
                continue
            hd = b.get("headers", True)
            if hd is True:
                supplied.update(range(b["h"], b["h"] + 6))
            elif hd:
                supplied.update(hd)
    supplied.update(p["supply_extra"])
    supplied.difference_update(p["supply_remove"])
    c.supplied = supplied
    c.header_bytes = {h: c.chain.headers[h] for h in sorted(supplied)}
    for h, hdr in (p["header_alt"] or {}).items():
        c.header_bytes[h] = hdr
    c.pins = {str(h): U.pin_of(c.chain.headers[h]) for h in range(c.lo, c.hi + 1) if h not in set(p["pins_exclude"])}
    H("pins")

    # ---- 7. validate confirmation and time evidence (honest issuer duties, P§4) ------------------------------
    c.T = expected_T(c)
    hsel, _ = selected(c, "receipt")
    sel = [b for b in c.branches["receipt"] if b.get("kind", "btc") == "btc" and not b.get("contradict")]
    at = [b for b in sel if b["h"] == hsel] or sorted(sel, key=lambda b: b["h"])
    c.txid = c.proofs["receipt"].txids[at[0]["label"]] if at else "00" * 32
    H("txid")
    c.preship = preship(c)
    if not p["adversarial"]:
        bad = [k for k, v in c.preship.items() if v is False]
        if bad:
            raise IssueRefused("pre-ship checks failed: " + ", ".join(bad))

    # ---- 8. ship: canonical container --------------------------------------------------------------------------
    b64 = U.b64
    c.layer = {
        "a_sig": b64(c.A_sig),
        "dependency_manifest": b64(p["bundled_dep"]),
        "dns": {"ots": b64(c.ots["snap"]), "snapshot_body": b64(c.body)},
        "git": {"blob": b64(c.git["blob"]), "commit": b64(c.git["commit"]), "object_format": "sha1",
                "ots": b64(c.ots["git"]), "trees": [b64(c.git["root"]), b64(c.git["sub"])]},
        "headers": {str(h): v.hex() for h, v in sorted(c.header_bytes.items())},
        "issuer_record": {"observed_anchor_delay_s": str(max(0, (c.T if c.T is not None else 0) - U.ts(c.declared))
                                                         if 0 <= U.ts(c.declared) else "0"),
                          "policy_version": "tessera-v1-issue-policy/1"},
        "keys": {"gpg": b64(c.gpg.pgp_body), "kms": b64(c.kms.spki)},
        "manifest": b64(c.F_manifest),
        "possession": {"gpg": b64(c.P_gpg), "kms": b64(c.P_kms)},
        "preamble": b64(p["bundled_preamble"]),
        "receipt_anchor": {"ots": b64(c.ots["receipt"]), "txid": c.txid},
        "spec": b64(p["bundled_spec"]),
        "vectors": b64(p["bundled_vectors"]),
    }
    H("layer")
    c.container = {"layers": [c.layer], "profile": U.PROFILE}
    H("container")
    c.bundle = U.jcs(c.container)
    H("bundle_bytes")

    # ---- trust configuration and TEST release ---------------------------------------------------------------
    c.trust = U.trust_config(c.pins, as_of=p["as_of"], repo_entries=p["repo_entries"], root_ksks=p["root_ksks"])
    H("trust")
    c.trust_bytes = U.jcs(c.trust)
    H("trust_bytes")
    c.release = U.make_release(c.trust_bytes, catalog_obj=U.catalog(p["installation"]))
    H("release")
    return c


# ------------------------------------------------------------------------------------------------- helpers
def kms_sign(c, msg):
    """Slot kms: rule O (OpenPGP P-256) for a P-256 key; rule R (raw ML-DSA-65 by EXTERNAL_MU) for an ML-DSA key."""
    if isinstance(c.kms, tc.MLDSA65Key):
        return c.kms.sign(msg)
    return tc.pgp_sign(msg, c.kms, c.sig_time)


def kms_verify(c, msg, sig):
    if isinstance(c.kms, tc.MLDSA65Key):
        return c.kms.verify(msg, sig)
    return gen.verify_openpgp4(msg, sig, (c.kms.x, c.kms.y))


class Plan:
    NAMES = ("root", "com_ds", "com_dnskey", "w_ds", "w_dnskey", "txt")

    def __init__(self):
        self.g = {}
        self.order = list(self.NAMES)

    def groups(self):
        return [self.g[n] for n in self.order if n in self.g]


def zone_keys():
    return dict(rzsk=U.zkey("root-ZSK", 8, 256), com_ksk=U.zkey("com-KSK", 13, 257),
                com_zsk=U.zkey("com-ZSK", 13, 256), w_ksk=U.zkey("wamason-KSK", 13, 257),
                w_zsk=U.zkey("wamason-ZSK", 13, 256))


def default_dns_plan(c):
    t = c.T_snap
    c.root_inc, c.root_exp = t - 9 * DAY, t + 12 * DAY       # 21-day window, as observed for the real root
    c.inc, c.exp = t - 5 * DAY, t + 10 * DAY
    k = zone_keys()
    c.zk = k
    G, S = U.Group, U.Sig
    pl = Plan()
    pl.g["root"] = G(".", U.T_DNSKEY, [U.ksk_a().rdata(), U.ksk_b().rdata(), k["rzsk"].rdata()],
                     [S(U.ksk_b(), c.root_inc, c.root_exp, signer=".")], ttl=172800)
    pl.g["com_ds"] = G("com", U.T_DS, [U.ds_rdata("com", k["com_ksk"].rdata(), 2)],
                       [S(k["rzsk"], c.inc, c.exp, signer=".")], ttl=86400)
    pl.g["com_dnskey"] = G("com", U.T_DNSKEY, [k["com_ksk"].rdata(), k["com_zsk"].rdata()],
                           [S(k["com_ksk"], c.inc, c.exp, signer="com")], ttl=86400)
    pl.g["w_ds"] = G("wamason.com", U.T_DS, [U.ds_rdata("wamason.com", k["w_ksk"].rdata(), 2)],
                     [S(k["com_zsk"], c.inc, c.exp, signer="com")], ttl=86400)
    pl.g["w_dnskey"] = G("wamason.com", U.T_DNSKEY, [k["w_ksk"].rdata(), k["w_zsk"].rdata()],
                         [S(k["w_ksk"], c.inc, c.exp, signer="wamason.com")], ttl=3600)
    pl.g["txt"] = G("_tessera-v1.wamason.com", U.T_TXT, [gen.dns_rdata(c.value)],
                    [S(k["w_zsk"], c.inc, c.exp, signer="wamason.com")], ttl=300)
    return pl


def build_git(c, t_git):
    blob = c.blob
    readme = b"TEST issuer repository for the Tessera V1 conformance universe.\n"
    g = {"blob": blob}
    g["sub_entries"] = [("100644", "key-assertion", U.git_id("blob", blob))]
    g["root_entries_extra"] = [("100644", "README", U.git_id("blob", readme))]
    g["sub_sort"] = g["root_sort"] = True
    when = max(t_git - 2 * HOUR, 0)
    g["headers_before"] = None     # filled in finalize_git (needs the root tree id)
    g["parents"] = [hashlib.sha1(b"TEST parent commit").hexdigest()]
    g["ident"] = f"TEST Issuer <test-issuer@wamason.com> {when} +0000".encode()
    g["extra_headers"] = []        # inserted after committer, before gpgsig
    g["message"] = b"TEST: publish the tessera-v1 key assertion\n"
    g["sig_args"] = {}
    g["armor_args"] = {}
    g["sign_key"] = c.repo
    g["gpgsig_count"] = 1
    g["sig_created"] = min(max(when, 0), U.U32 - 1)
    return g


def finalize_git(c):
    g = c.git
    sub = U.tree_body(g["sub_entries"], sort=g["sub_sort"])
    g["sub"] = g.get("sub_override", sub)
    root_entries = g["root_entries_extra"] + [g.get("root_dir_entry", ("40000", "tessera-v1", U.git_id("tree", g["sub"])))]
    root = U.tree_body(root_entries, sort=g["root_sort"])
    g["root"] = g.get("root_override", root)
    tree_id = g.get("commit_tree_id", U.git_id("tree", g["root"]).hex())
    hdrs = [f"tree {tree_id}\n".encode()] + [f"parent {pp}\n".encode() for pp in g["parents"]] + [
        b"author " + g["ident"] + b"\n", b"committer " + g["ident"] + b"\n"] + g["extra_headers"]
    payload = b"".join(hdrs) + b"\n" + g["message"]
    sig = tc.pgp_sign(payload, g["sign_key"], g["sig_created"], **g["sig_args"])
    g["sig"] = sig
    arm = tc.armor(sig, **g["armor_args"])
    g["armored"] = arm
    gs = U.gpgsig_header(arm) * g["gpgsig_count"]
    if "commit_override" in g:
        commit = g["commit_override"]
    else:
        commit = b"".join(hdrs) + gs + b"\n" + g["message"]
    g["commit"] = commit
    g["payload"] = payload
    g["id"] = U.git_id("commit", commit)
    c.blob_final = g["blob"]


def qualifies(c, h, msg_ok=True):
    for i in range(6):
        hh = h + i
        if hh not in c.header_bytes or str(hh) not in c.pins:
            return False
        if U.pin_of(c.header_bytes[hh]) != c.pins[str(hh)]:
            return False
        if i and c.header_bytes[hh][4:36] != U.sha256d(c.header_bytes[hh - 1]):
            return False
    return msg_ok


def proof_attestations(c, name):
    """[(height, message, is_btc)] from the built proof paths (issuer view)."""
    pr = c.proofs[name]
    out = []
    for ops, att in pr.paths:
        if att[1] != U.TAG_BTC:
            continue
        msg = U.run_ops([o for o in ops if o[0] != "raw"], pr.digest)
        out.append((U._read_varuint(att[2])[0], msg))
    return out


def selected(c, name):
    """Lowest qualifying height (P§7.1), or None. Also returns contradiction flag."""
    contradicted = False
    qual = []
    for h, msg in proof_attestations(c, name):
        if h in c.header_bytes and str(h) in c.pins and U.pin_of(c.header_bytes[h]) == c.pins[str(h)]:
            if c.header_bytes[h][36:68] != msg:
                contradicted = True
                continue
            if len(msg) == 32 and qualifies(c, h):
                qual.append(h)
    return (min(qual) if qual else None), contradicted


def expected_T(c):
    h, contra = selected(c, "receipt")
    if contra or h is None:
        return None
    return c.chain.ntime(h)


def expected_U(c):
    """A10.1.1 / profile 7.4: U = 7200 + max nTime(h* .. h*+5), unbounded int; None exactly when T is None."""
    if expected_T(c) is None:
        return None
    h, _ = selected(c, "receipt")
    return U.UTC_DELTA_S + max(c.chain.ntime(i) for i in range(h, h + U.UTC_M))


def preship(c):
    """Honest-issuer pre-ship checks (P§4). Values: True / False."""
    d = U.ts(c.declared)
    out = {}
    hr, _ = selected(c, "receipt")
    hs, _ = selected(c, "snap")
    hg, _ = selected(c, "git")
    out["receipt_anchored"] = hr is not None
    out["snapshot_anchored"] = hs is not None
    out["git_anchored"] = hg is not None
    if hr is not None and hg is not None:
        out["chain_order_h_git_plus_5_lt_h_receipt"] = hg + 5 < hr
    for nm, h in (("receipt", hr), ("snapshot", hs)):
        if h is None:
            continue
        T, conf = c.chain.ntime(h), c.chain.ntime(h + 5)
        out[f"{nm}_c1"] = d - U.EPS <= T
        out[f"{nm}_c2"] = T <= d + U.DELTA
        out[f"{nm}_c3"] = conf <= d + U.DELTA
    if hr is not None:
        out["window"] = U.ts(c.window[0]) <= d and c.chain.ntime(hr) <= U.ts(c.window[1])
    return out


def write_case_files(c, outdir):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "bundle.json").write_bytes(c.bundle)
    (outdir / "trust.json").write_bytes(c.trust_bytes)
    (outdir / "release.json").write_bytes(U.jcs(c.release))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True)
    ap.add_argument("--declared", default=DEFAULTS["timebase"])
    a = ap.parse_args()
    c = issue(timebase=a.declared)
    write_case_files(c, a.out)
    print(json.dumps({"T": U.rfc3339(c.T), "h_git": c.h_git, "h_snap": c.h_snap, "h_receipt": c.h_receipt,
                      "preship": c.preship, "bundle_bytes": len(c.bundle)}, indent=1))


if __name__ == "__main__":
    main()
