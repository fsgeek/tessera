#!/usr/bin/env python3
"""Construction self-check for the TEST universe (instrument code, not a V1 verifier).

For bundles whose expected verdict is VALID_STRICT, cross-checks the construction with independent libraries,
so that the positive controls are genuinely positive and not artefacts of the issuer's own arithmetic:
  - signatures and possession proofs: `cryptography` ECDSA, and `cryptography` ML-DSA-65 for the hybrid kms slot
    (not gen.py's arithmetic);
  - authority: TXT owner = _tessera-v1.<issuer>, TXT keys = manifest fingerprints, a configured repository entry
    for D verifies gpgsig with T_git in its interval, issuer = pinned D, issuance window;
  - OTS proofs: python-opentimestamps 0.4.5 deserializer (the profile's reference reader, P§15.2);
  - DNSSEC: dnspython 2.8 `dns.dnssec.validate` at T_snap, DS via `dns.dnssec.make_ds`;
  - git: SHA-1 ids by hashlib, `gpgsig` by `cryptography`;
  - headers against pins and prev links.
It deliberately checks only what a positive control needs. It does not decide verdicts.

Usage: selfcheck.py CASE_DIR [CASE_DIR ...]   (or --all to check every VALID_STRICT case)
       selfcheck.py --isolation   (authority-isolation cases: exactly the checks named in
                                   `_meta.isolation.selfcheck_fails` fail, every other check passes)
"""
import base64
import hashlib
import io
import json
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import universe as U  # noqa: E402
from tcrypto import gen  # noqa: E402

import dns.dnssec  # noqa: E402
import dns.name  # noqa: E402
import dns.rdata  # noqa: E402
import dns.rdataclass  # noqa: E402
import dns.rdatatype  # noqa: E402
import dns.rrset  # noqa: E402
import rfc8785  # noqa: E402
from cryptography.hazmat.primitives import hashes  # noqa: E402
from cryptography.hazmat.primitives.asymmetric import ec, mldsa  # noqa: E402
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed, encode_dss_signature  # noqa: E402
from opentimestamps.core.notary import BitcoinBlockHeaderAttestation, PendingAttestation  # noqa: E402
from opentimestamps.core.serialize import BytesDeserializationContext  # noqa: E402
from opentimestamps.core.timestamp import DetachedTimestampFile  # noqa: E402


def d64(s):
    return base64.b64decode(s, validate=True)


def pgp_verify(doc, sig, point):
    """Independent rule-O verification with `cryptography`."""
    hashed, r, s = gen.decode_sig_openpgp4(sig)
    body_off = 2 if sig[0] == 0x88 else 3
    typ = sig[body_off + 1]
    head = bytes([4, typ, 19, 8]) + struct.pack(">H", len(hashed)) + hashed
    h = hashlib.sha256(doc + head + b"\x04\xff" + struct.pack(">I", len(head))).digest()
    pub = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), point)
    try:
        pub.verify(encode_dss_signature(r, s), h, ec.ECDSA(Prehashed(hashes.SHA256())))
        return True
    except Exception:
        return False


KNOWN = []


def _own_ots(ots):
    """Minimal independent OTS reader, used only when python-opentimestamps 0.4.5 hits its depth limit of 255
    (the profile allows depth 256, P§15.2)."""
    i = [0]

    def u():
        v, sh = 0, 0
        while True:
            c = ots[i[0]]
            i[0] += 1
            v |= (c & 0x7F) << sh
            if not c & 0x80:
                return v
            sh += 7

    def vb():
        n = u()
        b = ots[i[0]:i[0] + n]
        i[0] += n
        return b
    i[0] = 31
    assert u() == 1 and ots[i[0]] == 8
    i[0] += 1
    digest = ots[i[0]:i[0] + 32]
    i[0] += 32
    out = []

    def ts(msg):
        while True:
            more = ots[i[0]] == 0xFF
            if more:
                i[0] += 1
            t = ots[i[0]]
            i[0] += 1
            if t == 0:
                tag = ots[i[0]:i[0] + 8]
                i[0] += 8
                pay = vb()
                out.append((msg, tag, pay))
            elif t == 8:
                ts(hashlib.sha256(msg).digest())
            elif t in (0xF0, 0xF1):
                a = vb()
                ts(msg + a if t == 0xF0 else a + msg)
            else:
                raise ValueError(t)
            if not more:
                return
    ts(digest)
    return digest, out


def ots_check(ots, digest, headers):
    try:
        f = DetachedTimestampFile.deserialize(BytesDeserializationContext(ots))
    except Exception as e:  # noqa: BLE001
        if "recursion depth" not in str(e):
            raise
        KNOWN.append("python-opentimestamps 0.4.5 rejects depth 256 (its limit is 255); profile allows 256")
        dg, out = _own_ots(ots)
        assert dg == digest
        atts = []
        for msg, tag, pay in out:
            if tag == bytes.fromhex("0588960d73d71901"):
                h = pay[0] if pay[0] < 128 else U._read_varuint(pay)[0]
                atts.append((h, h in headers and headers[h][36:68] == msg))
        return atts
    assert f.file_digest == digest, "OTS file digest"
    atts = []
    for msg, att in f.timestamp.all_attestations():
        if isinstance(att, BitcoinBlockHeaderAttestation):
            h = att.height
            ok = h in headers and headers[h][36:68] == msg
            atts.append((h, ok))
        elif isinstance(att, PendingAttestation):
            atts.append(("pending", True))
    return atts


def split_rrs(body):
    i, out = 0, []
    while i < len(body):
        j = i
        while body[j] != 0:
            j += 1 + body[j]
        owner = body[i:j + 1]
        rtype, rclass, ttl, rdlen = struct.unpack(">HHIH", body[j + 1:j + 11])
        rd = body[j + 11:j + 11 + rdlen]
        assert len(rd) == rdlen
        out.append((owner, rtype, ttl, rd))
        i = j + 11 + rdlen
    return out


def wire_to_name(w):
    labels, i = [], 0
    while w[i]:
        labels.append(w[i + 1:i + 1 + w[i]])
        i += 1 + w[i]
    return dns.name.Name(labels + [b""])


class _Inside:
    """`now` stand-in for dnspython after the window was checked with RFC 1982 serial arithmetic here
    (dnspython compares raw 32-bit values, which is wrong across the 2106 wrap; P§7.3)."""
    def __lt__(self, o): return False
    def __gt__(self, o): return False


def _resolve(v, t):
    x = v + ((t - v + (1 << 31)) // (1 << 32)) * (1 << 32)
    assert abs(x - t) < (1 << 31)
    return x


def _validate(rrset, sigs, keys, t_snap):
    """Pass if some RRSIG has inception <= T_snap <= expiration (serial arithmetic) and verifies."""
    errs = []
    for s in sigs:
        if not (_resolve(s.inception, t_snap) <= t_snap <= _resolve(s.expiration, t_snap)):
            errs.append("window")
            continue
        try:
            dns.dnssec.validate_rrsig(rrset, s, keys, now=_Inside())
            return
        except dns.dnssec.ValidationFailure as e:
            errs.append(str(e))
    raise dns.dnssec.ValidationFailure("no RRSIG valid at T_snap: " + ",".join(errs))


def dnssec_check(body, t_snap, root_rdatas):
    rrs = split_rrs(body)
    groups = {}
    for owner, rtype, ttl, rd in rrs:
        name = wire_to_name(owner)
        if rtype == U.T_RRSIG:
            covered = struct.unpack(">H", rd[:2])[0]
            key = (name, covered, "sig")
        else:
            key = (name, rtype, "rr")
        rdo = dns.rdata.from_wire(dns.rdataclass.IN, rtype, rd, 0, len(rd))
        groups.setdefault(key, (ttl, []))[1].append(rdo)

    def rrset(name, t, kind):
        ttl, rds = groups[(name, t, kind)]
        rt = dns.rdatatype.RRSIG if kind == "sig" else t
        return dns.rrset.from_rdata_list(name, ttl, rds) if rds else None

    root = dns.name.root
    keys = {}
    dk = rrset(root, U.T_DNSKEY, "rr")
    # root: only trusted RDATA may validate
    trusted = [r for r in dk if r.to_wire() in root_rdatas]
    assert trusted, "no trusted root KSK in the DNSKEY RRset"
    _validate(dk, rrset(root, U.T_DNSKEY, "sig"), {root: dns.rrset.from_rdata_list(root, 1, trusted)}, t_snap)
    keys[root] = dk
    zones = sorted({n for (n, t, k) in groups if t == U.T_DNSKEY and n != root}, key=len)
    for z in zones:
        parent = z.parent()
        while parent not in keys:
            parent = parent.parent()
        ds = rrset(z, U.T_DS, "rr")
        _validate(ds, rrset(z, U.T_DS, "sig"), {parent: keys[parent]}, t_snap)
        zk = rrset(z, U.T_DNSKEY, "rr")
        ok = [k for k in zk for d in ds
              if d.digest_type in (2, 4) and dns.dnssec.make_ds(z, k, d.digest_type) == d]
        assert ok, f"no DNSKEY of {z} matches a DS"
        _validate(zk, rrset(z, U.T_DNSKEY, "sig"), {z: dns.rrset.from_rdata_list(z, 1, ok)}, t_snap)
        keys[z] = zk
    txt = [(n, t) for (n, t, k) in groups if t == U.T_TXT and k == "rr"]
    assert len(txt) == 1
    n = txt[0][0]
    sigs = rrset(n, U.T_TXT, "sig")
    signer = list(sigs)[0].signer
    _validate(rrset(n, U.T_TXT, "rr"), sigs, {signer: keys[signer]}, t_snap)
    return list(rrset(n, U.T_TXT, "rr"))[0].strings[0]


def _mldsa_verify(spki, msg, sig):
    """Independent rule-R verification with `cryptography` (FIPS 204 pure ML-DSA-65, empty context) over the exact
    SPKI of the hybrid supplement §3 (22-byte prefix, 1952-byte key)."""
    if len(spki) != 1974 or spki[:22] != bytes.fromhex("308207b2300b0609608648016503040312038207a100"):
        return False
    if len(sig) != 3309:
        return False
    try:
        mldsa.MLDSA65PublicKey.from_public_bytes(spki[22:]).verify(sig, msg)
        return True
    except Exception:  # noqa: BLE001
        return False


def _txt_value(v):
    out = {}
    for part in v.decode("ascii").split(";"):
        k, _, val = part.partition("=")
        out[k] = val
    return out


def _git_sig(commit):
    head, _, msg = commit.partition(b"\n\n")
    hl = head.split(b"\n")
    sig_lines, payload_lines, in_sig = [], [], False
    for ln in hl:
        if ln.startswith(b"gpgsig "):
            in_sig = True
            sig_lines.append(ln[7:])
        elif in_sig and ln.startswith(b" "):
            sig_lines.append(ln[1:])
        else:
            in_sig = False
            payload_lines.append(ln)
    payload = b"\n".join(payload_lines) + b"\n\n" + msg
    arm = [x for x in sig_lines if x and not x.startswith(b"-----") and not x.startswith(b"=")]
    return payload, base64.b64decode(b"".join(arm))


# Named construction checks. A positive control must pass all of them; an authority-isolation case
# (expected.json `_meta.isolation.selfcheck_fails`) must fail exactly the named ones and pass every other.
CHECKS = ("container_jcs", "receipt_signatures", "possession", "key_fingerprints", "header_pins", "ots_receipt",
          "ots_snapshot", "ots_git", "chain_order", "dnssec", "txt_owner", "txt_keys", "git_path", "repo_signer",
          "repo_interval", "issuer_pinned", "issuance_window")


def check(case_dir, collect=False):
    """Run every named check. collect=False: raise at the first failure (positive controls). collect=True: return
    {name: None | failure text} for all checks (a check whose input an earlier check could not produce is
    recorded as failing with 'blocked')."""
    case_dir = Path(case_dir)
    raw = (case_dir / "bundle.json").read_bytes()
    trust = json.loads((case_dir / "trust.json").read_bytes())
    res, st = {}, {}

    def run(name, fn):
        try:
            out = fn()
            if out is False:
                raise AssertionError(name)
            res[name] = None
            return out
        except Exception as e:  # noqa: BLE001
            if not collect:
                raise AssertionError(f"{name}: {type(e).__name__} {e}") from e
            res[name] = f"{type(e).__name__} {e}"
            return None

    cont = json.loads(raw)
    L = cont["layers"][0]
    run("container_jcs", lambda: rfc8785.dumps(cont) == raw)
    a_sig = d64(L["a_sig"])
    (f0, s0), (f1, s1) = gen.decode_anchor(a_sig)
    common = gen.decode_frame(f0, gen.T_ATTEST)["common"]
    fm = d64(L["manifest"])
    man = gen.decode_frame(fm, gen.T_MANIFEST)
    kms_key, gpg_body = d64(L["keys"]["kms"]), d64(L["keys"]["gpg"])
    gpt = gpg_body[17:]
    hybrid = common["alg"] == U.ALG_HYBRID

    def kms_ok(msg, sig):
        return _mldsa_verify(kms_key, msg, sig) if hybrid else pgp_verify(msg, sig, kms_key[26:])
    run("receipt_signatures", lambda: kms_ok(f0, s0) and pgp_verify(f1, s1, gpt))
    run("possession", lambda: kms_ok(fm, d64(L["possession"]["kms"])) and pgp_verify(fm, d64(L["possession"]["gpg"]), gpt))
    run("key_fingerprints", lambda: man["key_fp"] == "spki-sha256:" + hashlib.sha256(kms_key).hexdigest()
        and man["sset"][0] == "gpg-sha256:" + hashlib.sha256(gpg_body).hexdigest())
    headers = {int(h): bytes.fromhex(v) for h, v in L["headers"].items()}

    def pins():
        for h, hdr in headers.items():
            assert trust["header_pins"][str(h)] == U.pin_of(hdr), f"pin {h}"
            if h - 1 in headers:
                assert hdr[4:36] == U.sha256d(headers[h - 1]), f"prev link {h}"
    run("header_pins", pins)

    def lowest(atts):
        hs = [h for h, ok in atts if h != "pending" and ok and all(h + i in headers for i in range(6))]
        return min(hs)
    body = d64(L["dns"]["snapshot_body"])
    env = gen.header(gen.T_SNAPSHOT) + struct.pack(">I", len(body)) + body
    commit = d64(L["git"]["commit"])
    cid = U.git_id("commit", commit)
    st["hr"] = run("ots_receipt", lambda: lowest(ots_check(d64(L["receipt_anchor"]["ots"]),
                                                            hashlib.sha256(a_sig).digest(), headers)))
    st["hs"] = run("ots_snapshot", lambda: lowest(ots_check(d64(L["dns"]["ots"]), hashlib.sha256(env).digest(),
                                                             headers)))
    st["hg"] = run("ots_git", lambda: lowest(ots_check(d64(L["git"]["ots"]),
                                                        hashlib.sha256(cid.hex().encode() + b"\n").digest(), headers)))

    def need(*ks):
        for k in ks:
            if st.get(k) is None:
                raise AssertionError("blocked: " + k + " unavailable")
    run("chain_order", lambda: (need("hg", "hr"), st["hg"] + 5 < st["hr"])[1])

    def t_of(h):
        return struct.unpack("<I", headers[h][68:72])[0]

    def dnssec():
        need("hs")
        root_rdatas = {d64(k["dnskey_rdata"]) for k in trust["root_ksks"]}
        return dnssec_check(body, t_of(st["hs"]), root_rdatas)
    txt = run("dnssec", dnssec)
    # the TXT value as presented (row 13.6 parses it whether or not DNSSEC validated, P§3.2 `DNS_*` record class)
    rrs = split_rrs(body)
    txt_rrs = [(o, rd) for (o, t, ttl, rd) in rrs if t == U.T_TXT]
    owner_w, txt_rd = txt_rrs[0]
    presented = txt_rd[1:1 + txt_rd[0]]
    if txt is not None:
        assert txt == presented
    tv = _txt_value(presented)
    run("txt_owner", lambda: wire_to_name(owner_w) == dns.name.from_text("_tessera-v1." + common["issuer"]))
    run("txt_keys", lambda: ("spki-sha256:" + tv["kms"], "gpg-sha256:" + tv["gpg"]) == (man["key_fp"], man["sset"][0]))

    def git_path():
        lines = commit.split(b"\n")
        tree = bytes.fromhex(lines[0].split(b" ")[1].decode())
        root_t, sub_t = d64(L["git"]["trees"][0]), d64(L["git"]["trees"][1])
        assert U.git_id("tree", root_t) == tree
        assert U.git_id("tree", sub_t).hex() in root_t.hex()
        blob = d64(L["git"]["blob"])
        assert U.git_id("blob", blob).hex() in sub_t.hex()
        assert blob == presented, "git blob equals the DNS TXT value"
    run("git_path", git_path)
    payload, gsig = _git_sig(commit)
    verifying = [e for e in trust["repository_keys"]
                 if e["domain"] == trust["issuer_domain"] and pgp_verify(payload, gsig, d64(e["key"])[17:])]
    run("repo_signer", lambda: bool(verifying))

    def repo_interval():
        need("hg")
        t_git = t_of(st["hg"])
        for e in verifying:
            end = e["signing_end"] or trust["as_of"]
            if U.ts(e["signing_start"]) <= t_git <= U.ts(end):
                return True
        raise AssertionError("no verifying repository entry's interval contains T_git " + U.rfc3339(t_git))
    run("repo_interval", repo_interval)
    run("issuer_pinned", lambda: common["issuer"] == U.D == trust["issuer_domain"] == man["issuer"])

    def window():
        need("hr")
        return U.ts(tv["issuance-not-before"]) <= U.ts(common["declared_issue_time"]) and \
            t_of(st["hr"]) <= U.ts(tv["issuance-not-after"])
    run("issuance_window", window)
    info = {"alg": "hybrid" if hybrid else "classical", "h_receipt": st["hr"], "h_snap": st["hs"], "h_git": st["hg"]}
    if st["hs"] is not None:
        info["T_snap"] = U.rfc3339(t_of(st["hs"]))
    return (res, info) if collect else info


def main():
    args = sys.argv[1:]
    if args == ["--isolation"]:
        # every case that declares an isolation expectation (authority-isolation family)
        bad = n = 0
        for p in sorted((HERE / "cases").glob("*/expected.json")):
            meta = json.loads(p.read_text())["_meta"]
            iso = meta.get("isolation")
            if not iso or "selfcheck_fails" not in iso:
                continue
            n += 1
            res, info = check(p.parent, collect=True)
            fails = sorted(k for k, v in res.items() if v)
            want = sorted(iso["selfcheck_fails"])
            ok = fails == want
            bad += not ok
            print("OK  " if ok else "FAIL", p.parent.name, "fails:", fails or "none", "" if ok else f"(want {want})",
                  {k: res[k] for k in fails} if not ok else "")
        print(f"{n - bad}/{n} authority-isolation cases fail exactly their named construction checks")
        sys.exit(1 if bad else 0)
    if args == ["--all"]:
        args = [str(p.parent) for p in sorted((HERE / "cases").glob("*/expected.json"))
                if json.loads(p.read_text()).get("verdict") == "VALID_STRICT"
                and (p.parent / "bundle.json").exists()]
    bad = 0
    for a in args:
        try:
            KNOWN.clear()
            r = check(a)
            print("OK  ", Path(a).name, r, ("NOTE: " + "; ".join(set(KNOWN))) if KNOWN else "")
        except Exception as e:  # noqa: BLE001
            bad += 1
            print("FAIL", Path(a).name, type(e).__name__, e)
    print(f"{len(args) - bad}/{len(args)} positive controls pass the construction self-check")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
