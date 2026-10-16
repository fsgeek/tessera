"""THROWAWAY spike step 4: offline verifier for ONE V1-shaped receipt + DNS snapshot + OTS proofs.
No network: socket creation is blocked and counted, and the count is asserted to be zero at the end.
Inputs: out/receipt.json, out/receipt-preimage.bin(.ots), out/dns-snapshot.json(.ots), trust-config.json,
out/bitcoin-pins.json + out/bitcoin-headers.json (pinned mainnet headers; absent until the anchors confirm).
Repaired 2026-10-13 per docs/reviews/v1-profile/ F1, F3-F6 and F2 as disposed (A9.5 reliance periods). INSTRUMENT code
(A9.2): its outputs are never evidence for a C-row."""
import socket, sys
_NET = {"attempts": 0}
_RealSocket = socket.socket
class _Blocked(_RealSocket):
    def __init__(self, *a, **k):
        _NET["attempts"] += 1
        raise OSError("NETWORK BLOCKED (spike offline verifier)")
def _blocked(*a, **k):
    _NET["attempts"] += 1
    raise OSError("NETWORK BLOCKED (spike offline verifier)")
socket.socket = _Blocked
socket.create_connection = _blocked
socket.getaddrinfo = _blocked
socket.gethostbyname = _blocked

import argparse, base64, datetime as dt, hashlib, json, os
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import dns.dnssec, dns.message, dns.name, dns.rdataclass, dns.rdatatype, dns.rrset
from tessera_proto import frame as F, objects
from tessera_proto.crypto import b64d, fingerprint
from tessera_proto.real import btc, gpg, ots as O
from tessera_proto.real import openpgp as P

PASS, FAIL, UNPERF, INFO = "PASS", "FAIL", "UNPERFORMABLE", "INFO"
VERDICT = {PASS: "VALID", FAIL: "INVALID", UNPERF: "UNVERIFIABLE"}   # R-2.26: a failed check outranks an unperformable one
iso = lambda t: dt.datetime.fromtimestamp(t, dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
parse_iso = lambda s: int(dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.UTC).timestamp())
REQUIRED = ("SIG", "BYTES", "AUTH", "DNSSEC", "OTS.receipt", "OTS.snapshot", "TIME", "NETWORK")

class Ledger:
    """Rows are (check id, status, detail). INFO rows are diagnostics only and never count toward a group (F1, F3)."""
    def __init__(self): self.rows = []
    def add(self, cid, st, detail=""): self.rows.append((cid, st, detail))
    def status(self, prefix):
        s = [r[1] for r in self.rows if r[0].startswith(prefix) and r[1] in (PASS, FAIL, UNPERF)]
        return FAIL if FAIL in s else UNPERF if UNPERF in s or not s else PASS

def verdict(groups, need=REQUIRED):
    s = [groups[g] for g in need]
    return VERDICT[FAIL] if FAIL in s else VERDICT[UNPERF] if UNPERF in s else VERDICT[PASS]

# ---------------------------------------------------------------- 1. signatures and bytes (C1, C3)
def check_signatures(b, L, domain, out):
    layer = b["layer"]; slots = layer["slots"]; man = layer["manifest"]; t = man["tuple"]
    frames, commons, fps = [], [], []
    for s in slots:
        fb, sig, pub = b64d(s["frame_b64"]), b64d(s["sig_b64"]), b64d(s["pubkey_b64"])
        frames.append(fb)
        ok = gpg.verify_openpgp_slot(s["alg"], pub, sig, fb)
        L.add(f"SIG.{s['slot']}.signature", PASS if ok else FAIL, "" if ok else "SIGNATURE_INVALID")
        fr, fails = F.decode(fb)
        L.add(f"BYTES.{s['slot']}.frame_wellformed", PASS if not fails else FAIL, str(fails))
        pl = json.loads(fr.payload)
        commons.append(pl["common"]); fp = fingerprint(s["alg"], pub); fps.append(fp)
        L.add(f"BYTES.{s['slot']}.signer_fp_in_slot", PASS if pl["signer"]["key_fp"] == fp else FAIL, "")
    L.add("BYTES.common_equal", PASS if commons[0] == commons[1] else FAIL)
    L.add("BYTES.tuple_matches_keys", PASS if (t["key_fp"], t["sset"]) == (fps[0], fps[1:]) else FAIL)
    L.add("BYTES.manifest_hash", PASS if commons[0]["manifest_hash"] == objects.manifest_hash(t) else FAIL)
    L.add("AUTH.owner_name_bound", PASS if t["issuer_id"] == domain == commons[0]["issuer_id"] else FAIL,
          f"signed issuer_id={commons[0]['issuer_id']} trust D={domain}")
    pf = objects.possession_frame(t)
    for s, p in zip(slots, man["possession"]):
        ok = gpg.verify_openpgp_slot(s["alg"], b64d(s["pubkey_b64"]), b64d(p["sig_b64"]), pf)
        L.add(f"SIG.{s['slot']}.possession", PASS if ok else FAIL)
    pp = out / b["preimage_file"]
    if not pp.exists():
        L.add("BYTES.anchor_preimage_rebuilt", UNPERF, "EVIDENCE_MISSING (anchor preimage file absent)")
        return None, parse_iso(commons[0]["declared_issue_time"])
    pre = pp.read_bytes()
    want = b"tessera/v0/receipt-digest\x00" + b"".join(len(f).to_bytes(4, "big") + f for f in frames)
    L.add("BYTES.anchor_preimage_rebuilt", PASS if pre == want and hashlib.sha256(pre).hexdigest() == b["receipt_digest"] else FAIL)
    return pre, parse_iso(commons[0]["declared_issue_time"])

# ---------------------------------------------------------------- 2. DNSSEC chain (C4 i)
def _sets(msg, section):
    data, sigs = {}, {}
    for rr in getattr(msg, section):
        (sigs if rr.rdtype == dns.rdatatype.RRSIG else data)[(rr.name, rr.covers if rr.rdtype == dns.rdatatype.RRSIG else rr.rdtype)] = rr
    return data, sigs

def _sig_order(s):
    """Pinned witness-selection order (F5): (key tag, inception, expiration, signature bytes). The first signature in
    this order that validates is THE witness for its RRset; no other offered signature is recorded as used."""
    return (s.key_tag, s.inception, s.expiration, s.signature)

def _one(sigset, s):
    r = dns.rrset.RRset(sigset.name, sigset.rdclass, sigset.rdtype, sigset.covers); r.add(s); return r

def _sig_valid_crypto(rrset, sigset, s, keys_by_zone):
    """Cryptographic validity ONLY, independent of time: validate at the signature's own inception instant (F3)."""
    try: dns.dnssec.validate(rrset, _one(sigset, s), keys_by_zone, now=s.inception); return True
    except dns.dnssec.ValidationFailure: return False

def root_dnskey_check(keys, rs, trust, now, L):
    """A9.5 root-KSK rule (OWNER DECISION 2026-10-13): the root DNSKEY set is valid at `now` iff SOME trusted KSK whose
    RELIANCE period [signing start, reliance end] contains `now` validates it. Existential and order-independent (F1):
    every trusted KSK and every RRSIG it might have made is examined, each outcome is an INFO row, and exactly ONE
    required row is written afterwards. Observations kept apart (F3): key absent/digest mismatch; key present but no
    RRSIG carries its tag; RRSIG cryptographically invalid; RRSIG valid but `now` outside its own inception/expiration;
    RRSIG valid and in its window but `now` outside the KSK's reliance period; winner. A key tag alone proves nothing:
    the reliance reason is emitted only for a signature that verified."""
    root = dns.name.root
    winners, obs = [], {"outside_reliance": [], "rrsig_window": [], "sig_invalid": []}
    for ksk in trust["root_ksks"]:
        lo = parse_iso(ksk["signing_valid_from"])
        rel_hi = parse_iso(ksk["reliance_valid_until"]) if ksk.get("reliance_valid_until") else None
        sig_hi = parse_iso(ksk["signing_valid_until"]) if ksk.get("signing_valid_until") else None
        in_rel = lo <= now and (rel_hi is None or now <= rel_hi)
        present = [k for k in keys if dns.dnssec.key_id(k) == ksk["key_tag"] and k.algorithm == ksk["algorithm"]
                   and dns.dnssec.make_ds(root, k, "SHA256").digest.hex().upper() == ksk["ds_digest_sha256"]]
        tagged = sorted((s for s in rs if s.key_tag == ksk["key_tag"] and s.algorithm == ksk["algorithm"]), key=_sig_order)
        base = f"in_reliance_period={in_rel} key_present_and_matches_pinned_digest={bool(present)} rrsigs_with_tag={len(tagged)}"
        if not present:
            L.add(f"DNSSEC.root.{ksk['name']}", INFO, f"INFORMATIONAL_key_not_in_set_or_digest_mismatch {base}"); continue
        if not tagged:
            L.add(f"DNSSEC.root.{ksk['name']}", INFO, f"INFORMATIONAL_published_not_signing {base}"); continue
        tk = dns.rrset.RRset(root, dns.rdataclass.IN, dns.rdatatype.DNSKEY); tk.add(present[0])
        for s in tagged:
            sid = f"inception={iso(s.inception)} expiration={iso(s.expiration)}"
            made_while_signing = lo <= s.inception and (sig_hi is None or s.inception <= sig_hi)
            if not _sig_valid_crypto(keys, rs, s, {root: tk}):
                obs["sig_invalid"].append(ksk["name"])
                L.add(f"DNSSEC.root.{ksk['name']}", INFO, f"CANDIDATE_SIGNATURE_INVALID {sid} {base}"); continue
            in_win = s.inception <= now <= s.expiration
            if not in_win: obs["rrsig_window"].append(ksk["name"])
            if not in_rel: obs["outside_reliance"].append(ksk["name"])
            tag = "CANDIDATE_VALIDATES" if in_win and in_rel else "CANDIDATE_VERIFIED_NOT_USABLE"
            L.add(f"DNSSEC.root.{ksk['name']}", INFO, f"{tag} rrsig_window_contains_eval={in_win} {sid} "
                  f"inception_within_signing_period={made_while_signing} {base}")
            if in_win and in_rel: winners.append((ksk, s))
    if winners:
        ksk, s = min(winners, key=lambda w: _sig_order(w[1]))
        L.add("DNSSEC.root.dnskey_rrset", PASS, f"validated by {ksk['name']} ({ksk['key_tag']}); {len(winners)} usable witness(es)")
        return [("root DNSKEY", s.inception, s.expiration, s.key_tag)]
    # No usable trusted KSK. R-2.26 split, by what was actually established (profile §5, OWNER DECISION 2026-10-13):
    if obs["outside_reliance"]:
        L.add("DNSSEC.root.dnskey_rrset", FAIL, f"KSK_OUTSIDE_RELIANCE_PERIOD {sorted(set(obs['outside_reliance']))} (verified signature)")
    elif obs["rrsig_window"]:
        L.add("DNSSEC.root.dnskey_rrset", FAIL, f"RRSIG_NOT_VALID_AT_EVAL_TIME {sorted(set(obs['rrsig_window']))} (verified signature)")
    elif obs["sig_invalid"]:
        L.add("DNSSEC.root.dnskey_rrset", FAIL, f"TRUSTED_KSK_SIGNATURE_INVALID {sorted(set(obs['sig_invalid']))}")
    else:
        L.add("DNSSEC.root.dnskey_rrset", UNPERF, "NO_TRUSTED_KSK_USABLE (signed only by keys this trust config does not hold, or unsigned)")
    return []

def check_dnssec(snap, trust, now, domain, L):
    """Validate root -> ... -> D at time `now`. Returns [(label, inception, expiration, key_tag)] of the ONE witness
    RRSIG selected per required RRset (F5). Missing evidence is UNPERFORMABLE, never an exception (F4)."""
    M = {}
    for k, v in snap.get("messages", {}).items():
        try: M[k] = dns.message.from_wire(base64.b64decode(v))
        except Exception as e: L.add(f"DNSSEC.message_wellformed.{k}", FAIL, f"SNAPSHOT_MESSAGE_MALFORMED {type(e).__name__}")
    used = []
    def msg(key, cid):
        if key not in M:
            if key not in snap.get("messages", {}): L.add(cid, UNPERF, f"EVIDENCE_MISSING (snapshot has no '{key}' message)")
            return None
        return M[key]
    def val(cid, label, rrset, sigset, keys_by_zone, only_tags=None, ok_detail=""):
        """Required RRset check. Missing RRset / RRSIG / keys -> UNPERFORMABLE; offered signatures all fail -> FAIL."""
        if rrset is None: L.add(cid, UNPERF, "EVIDENCE_MISSING (RRset absent)"); return False
        if sigset is None: L.add(cid, UNPERF, "EVIDENCE_MISSING (no RRSIG)"); return False
        if any(v is None for v in keys_by_zone.values()): L.add(cid, UNPERF, "EVIDENCE_MISSING (signer keys unavailable)"); return False
        cand = sorted((s for s in sigset if only_tags is None or s.key_tag in only_tags), key=_sig_order)
        if not cand: L.add(cid, UNPERF, "EVIDENCE_MISSING (no RRSIG by an allowed key)"); return False
        why = []
        for s in cand:
            try:
                dns.dnssec.validate(rrset, _one(sigset, s), keys_by_zone, now=now)
                used.append((label, s.inception, s.expiration, s.key_tag)); L.add(cid, PASS, ok_detail or f"witness tag {s.key_tag}")
                return True
            except dns.dnssec.ValidationFailure as e: why.append(f"{s.key_tag}: {e}")
        L.add(cid, FAIL, "; ".join(why)); return False
    root = dns.name.root
    m = msg(". DNSKEY", "DNSSEC.root.dnskey_rrset")
    root_keys = None
    if m is not None:
        kd, ks = _sets(m, "answer")
        root_keys = kd.get((root, dns.rdatatype.DNSKEY)); rs = ks.get((root, dns.rdatatype.DNSKEY))
        if root_keys is None or rs is None:
            L.add("DNSSEC.root.dnskey_rrset", UNPERF, "NO_TRUSTED_KSK_USABLE (root DNSKEY RRset or its RRSIG missing from the snapshot)")
        else:
            used += root_dnskey_check(root_keys, rs, trust, now, L)
    # The chain below continues even if the root check did not pass, so an independently failing lower check still
    # yields INVALID (precedence, F4). It uses the PRESENTED root keys; the root row alone decides their authority.
    labels = domain.rstrip(".").split(".")
    zones = [".".join(labels[i:]) + "." for i in range(len(labels) - 1, -1, -1)]
    zone_keys = {root: root_keys}; parent = root
    for z in zones:
        zn = dns.name.from_text(z)
        mds = msg(f"{z} DS", f"DNSSEC.{z}.ds")
        dd, dsg = _sets(mds, "answer") if mds is not None else ({}, {})
        ds = dd.get((zn, dns.rdatatype.DS))
        if mds is not None: val(f"DNSSEC.{z}.ds", f"{z} DS", ds, dsg.get((zn, dns.rdatatype.DS)), {parent: zone_keys.get(parent)}, ok_detail=f"signed by {parent}")
        mk = msg(f"{z} DNSKEY", f"DNSSEC.{z}.dnskey_matches_ds")
        kd, ks = _sets(mk, "answer") if mk is not None else ({}, {})
        zk = kd.get((zn, dns.rdatatype.DNSKEY))
        if mk is not None and (zk is None or ds is None):
            L.add(f"DNSSEC.{z}.dnskey_matches_ds", UNPERF, "EVIDENCE_MISSING (DS or DNSKEY RRset absent)")
        linked = []
        if zk is not None and ds is not None:
            dsset = {(d.key_tag, d.digest_type, d.digest) for d in ds}
            def _ds_ok(k):
                return any(d[0] == dns.dnssec.key_id(k) and d[1] in (2, 4) and dns.dnssec.make_ds(zn, k, {2: "SHA256", 4: "SHA384"}[d[1]]).digest == d[2] for d in dsset)
            linked = [k for k in zk if _ds_ok(k)]
            L.add(f"DNSSEC.{z}.dnskey_matches_ds", PASS if linked else FAIL, f"tags={[dns.dnssec.key_id(k) for k in linked]}")
        if linked:
            lk = dns.rrset.RRset(zn, dns.rdataclass.IN, dns.rdatatype.DNSKEY)
            for k in linked: lk.add(k)
            val(f"DNSSEC.{z}.dnskey_selfsigned", f"{z} DNSKEY", zk, ks.get((zn, dns.rdatatype.DNSKEY)), {zn: lk}, {dns.dnssec.key_id(k) for k in linked})
        zone_keys[zn] = zk if linked else None; parent = zn
    dn = dns.name.from_text(domain)
    for rt in ("SOA", "NS", "TXT"):
        r = dns.rdatatype.from_text(rt); cid = f"DNSSEC.target.{rt}"
        m = msg(f"{domain}. {rt}", cid)
        if m is None: continue
        d, s = _sets(m, "answer")
        val(cid, f"{domain} {rt}", d.get((dn, r)), s.get((dn, r)), {dn: zone_keys.get(dn)}, ok_detail=f"signed by {dn}")
    # key-publication record (spike names, derived from D; the V1 owner name is _tessera-v1.<D>, profile §6.1)
    found_key = False
    for q in (f"_tessera.{domain}. TXT", f"tessera.{domain}. TXT"):
        qn = dns.name.from_text(q.split()[0])
        m = msg(q, f"DNSKEY_PUBLICATION.message.{q}")
        if m is None: continue
        d, s = _sets(m, "answer")
        if (qn, dns.rdatatype.TXT) in d:
            found_key = True
            val(f"DNSSEC.keyrecord.{q}", q, d[(qn, 16)], s.get((qn, 16)), {dn: zone_keys.get(dn)}, ok_detail=d[(qn, 16)].to_text())
            continue
        ad, asg = _sets(m, "authority")
        nsec = ad.get((qn, dns.rdatatype.NSEC))
        if val(f"DNSSEC.keyrecord_absent_nsec.{q}", q + " NSEC", nsec, asg.get((qn, dns.rdatatype.NSEC)), {dn: zone_keys.get(dn)}):
            bm = {t for w in nsec[0].windows for t in [w[0] * 256 + i * 8 + b for i, byte in enumerate(w[1]) for b in range(8) if byte & (0x80 >> b)]}
            absent = dns.rdatatype.TXT not in bm and dns.rdatatype.CNAME not in bm
            L.add(f"DNSSEC.keyrecord_absent.{q}", PASS if absent else FAIL, "authenticated NODATA: NSEC type bitmap lacks TXT/CNAME")
    L.add("DNSKEY_PUBLICATION.key_txt_record_present", PASS if found_key else UNPERF,
          "" if found_key else "NO key-publication TXT record exists in the zone: C4(i) cannot establish K for D")
    return used

# ---------------------------------------------------------------- 3. OTS to pinned headers (C5)
def check_ots(tag, ots_bytes, file_bytes, hdrs, pins, k, L):
    """Returns the authenticated anchor, or None. Absent proof or absent stamped file -> UNPERFORMABLE (F4); a proof
    that is present but malformed, or whose digest does not match, is FAIL and yields NO evaluation time (F4)."""
    if ots_bytes is None: L.add(f"OTS.{tag}.proof_present", UNPERF, "EVIDENCE_MISSING (no OTS proof)"); return None
    if file_bytes is None: L.add(f"OTS.{tag}.stamped_bytes_present", UNPERF, "EVIDENCE_MISSING (stamped file absent)"); return None
    try: dtf = O.load(ots_bytes)
    except Exception as e: L.add(f"OTS.{tag}.proof_wellformed", FAIL, f"PROOF_MALFORMED {type(e).__name__}"); return None
    chk = O.check(dtf, file_bytes, hdrs)
    L.add(f"OTS.{tag}.digest_matches", PASS if chk.file_digest_ok else FAIL)
    if not chk.file_digest_ok: return None
    if not chk.bitcoin:
        L.add(f"OTS.{tag}.attestation", UNPERF, f"ANCHOR_PENDING_ONLY ({len(chk.pending)} pending calendars)"); return None
    good = []
    for b in chk.bitcoin:
        h = b["height"]; need = range(h, h + k)
        if not all(x in hdrs for x in need): L.add(f"OTS.{tag}.att@{h}", UNPERF, "HEADERS_NOT_IN_BUNDLE"); continue
        if not b["merkle_ok"]: L.add(f"OTS.{tag}.att@{h}", FAIL, "MERKLE_ROOT_MISMATCH"); continue
        ok, why = btc.check_segment(hdrs, h, h + k - 1)
        if not ok: L.add(f"OTS.{tag}.att@{h}", FAIL, why); continue
        miss = [x for x in need if str(x) not in pins["headers"]]
        bad = [x for x in need if str(x) in pins["headers"] and pins["headers"][str(x)] != hdrs[x].hash_hex]
        if bad: L.add(f"OTS.{tag}.att@{h}", FAIL, f"HEADER_CONFLICTS_WITH_PIN {bad}"); continue
        if miss: L.add(f"OTS.{tag}.att@{h}", UNPERF, f"HEADERS_NOT_COVERED {miss}"); continue
        L.add(f"OTS.{tag}.att@{h}", PASS, f"merkle root ok; PoW+linkage ok; {k} headers equal pins; nTime={iso(hdrs[h].time)}")
        good.append(h)
    if not good: return None
    h = min(good)
    return {"height": h, "T": hdrs[h].time, "confirmed_at": hdrs[h + k - 1].time, "all": good}

def conjuncts(tag, declared, a, delta, eps, L):
    c1, c2, c3 = declared - eps <= a["T"], a["T"] <= declared + delta, a["confirmed_at"] <= declared + delta
    L.add(f"TIME.{tag}.c1_T>=declared-eps", PASS if c1 else FAIL, f"T-declared={a['T']-declared}s")
    L.add(f"TIME.{tag}.c2_T<=declared+delta", PASS if c2 else FAIL)
    L.add(f"TIME.{tag}.c3_conf<=declared+delta", PASS if c3 else FAIL, f"confirmed_at-declared={a['confirmed_at']-declared}s")

def check_snapshot_time(declared, a, p, used, L, captured_end=None):
    """The snapshot's own anchored time a['T'] (from its OTS proof; not the receipt's T, not wall-clock) must lie inside
    every witness RRSIG window and within [declared - eps, declared + delta], where `declared` is the RECEIPT's signed
    declared_issue_time (DD:94, profile §7.3; F6). Capture-to-anchor latency is a separate INFO observation."""
    conjuncts("snapshot", declared, a, p["delta_s"], p["epsilon_s"], L)
    if captured_end is not None:
        L.add("DIAGNOSTIC.snapshot_capture_to_anchor", INFO, f"T_snap-captured_end={a['T']-captured_end}s (observation, not the C4 predicate)")
    if used:
        lo = max(u[1] for u in used); hi = min(u[2] for u in used)
        L.add("DNSSEC.T_snap_inside_joint_window", PASS if lo <= a["T"] <= hi else FAIL, f"T_snap={iso(a['T'])} window=[{iso(lo)}, {iso(hi)}]")

def _read(p): return p.read_bytes() if p.exists() else None

def run(eval_arg, trust_path, out_dir, quiet=False):
    """eval_arg 'auto' evaluates DNSSEC at the snapshot's own anchored time. Any other value is a DIAGNOSTIC OVERRIDE for
    controls only: it is never a V1 time source and a run using it is not a verification result (F4)."""
    L = Ledger(); out = Path(out_dir)
    trust = json.loads(Path(trust_path).read_text()); D = trust["issuer_domain"]; p = trust["params"]; k = p["k"]
    pre = declared = snap = None
    rb = _read(out / "receipt.json")
    if rb is None: L.add("SIG.receipt_present", UNPERF, "EVIDENCE_MISSING (receipt.json absent)")
    else: pre, declared = check_signatures(json.loads(rb), L, D, out)
    sb = _read(out / "dns-snapshot.json")
    if sb is None: L.add("DNSSEC.snapshot_present", UNPERF, "EVIDENCE_MISSING (dns-snapshot.json absent)")
    else:
        try: snap = json.loads(sb)
        except ValueError: L.add("DNSSEC.snapshot_wellformed", FAIL, "SNAPSHOT_MALFORMED")
    pins = hdrs = None
    if (out / "bitcoin-pins.json").exists() and (out / "bitcoin-headers.json").exists():
        pins = json.loads((out / "bitcoin-pins.json").read_text())
        hdrs = {int(h): btc.Header.parse(bytes.fromhex(x)) for h, x in json.loads((out / "bitcoin-headers.json").read_text()).items()}
        L.add("PINS.header_hashes_present", PASS, f"pins sha256={hashlib.sha256((out/'bitcoin-pins.json').read_bytes()).hexdigest()[:16]}.. n={len(pins['headers'])}")
    else:
        pins, hdrs = {"headers": {}}, {}
    ar = check_ots("receipt", _read(out / "receipt-preimage.bin.ots"), pre, hdrs, pins, k, L)
    as_ = check_ots("snapshot", _read(out / "dns-snapshot.json.ots"), sb, hdrs, pins, k, L)
    if ar and declared is not None: conjuncts("receipt", declared, ar, p["delta_s"], p["epsilon_s"], L)
    if eval_arg == "auto":
        now, basis = (as_["T"], "snapshot's anchored time T_snap") if as_ else (None, "snapshot not anchored: no evaluation time, no stand-in")
    else:
        now, basis = int(eval_arg), "DIAGNOSTIC OVERRIDE stated by caller (never a V1 time source)"
        L.add("DIAGNOSTIC.eval_time_override", INFO, f"eval={iso(now)}: this run is a control, not a verification result")
    used = []
    if snap is None:
        pass
    elif now is None:
        L.add("DNSSEC.eval_time", UNPERF, "SNAPSHOT_NOT_ANCHORED (UNVERIFIABLE: missing anchor is missing evidence)")
    else:
        used = check_dnssec(snap, trust, now, D, L)
    if used:
        lo = max(u[1] for u in used); hi = min(u[2] for u in used)
        L.add("DNSSEC.eval_time_inside_every_used_RRSIG_window", PASS if lo <= now <= hi else FAIL,
              f"eval={iso(now)} [{basis}] joint window [{iso(lo)}, {iso(hi)}] = {(hi-lo)/3600:.1f} h over {len(used)} witness RRSIGs")
    if as_:
        if declared is None: L.add("TIME.snapshot.declared_available", UNPERF, "EVIDENCE_MISSING (no receipt declared_issue_time)")
        else: check_snapshot_time(declared, as_, p, used, L, captured_end=snap.get("captured_end") if snap else None)
    L.add("NETWORK.socket_attempts_zero", PASS if _NET["attempts"] == 0 else FAIL, f"attempts={_NET['attempts']}")
    assert _NET["attempts"] == 0, "network was touched"
    groups = {g: L.status(g) for g in ("SIG", "BYTES", "AUTH", "DNSSEC", "DNSKEY_PUBLICATION", "OTS.receipt", "OTS.snapshot", "TIME", "NETWORK")}
    if not quiet:
        for r in L.rows: print(f"{r[1]:13} {r[0]}  {r[2]}")
        print("\nGROUPS", json.dumps(groups)); print("eval_time", iso(now) if now is not None else None, "-", basis)
        print("spike verdict over", REQUIRED, "=", verdict(groups), "(excludes DNSKEY_PUBLICATION and the git channel: not a V1 or C4 result)")
    return L, groups, {"receipt_anchor": ar, "snapshot_anchor": as_, "eval": now, "declared": declared,
                       "joint": (lo, hi) if used else None, "override": eval_arg != "auto"}

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--eval-time", default="auto", help="DIAGNOSTIC ONLY; never a V1 time source")
    ap.add_argument("--trust", default=str(HERE / "trust-config.json")); ap.add_argument("--out", default=str(HERE / "out")); a = ap.parse_args()
    L, g, f = run(a.eval_time, a.trust, a.out)
    if f["override"]: print("DIAGNOSTIC OVERRIDE: exit 3, not a verification result"); sys.exit(3)
    sys.exit(0 if all(g[x] == PASS for x in REQUIRED) else 1)
