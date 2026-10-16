"""THROWAWAY: negative/positive controls for verify_offline.py (no network). Uses the archived mainnet fixtures for the OTS path."""
import copy, json, shutil, sys, tempfile
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_offline as V
from tessera_proto.real import btc
FX = HERE.parent / "tessera_proto" / "real" / "fixtures"
res = []
def expect(name, cond): res.append((name, cond)); print(("ok   " if cond else "FAIL ") + name)
OUT = HERE / "out"; TR = HERE / "trust-config.json"
trust = json.loads(TR.read_text())
# DNSSEC controls
L, g, f = V.run("auto", TR, OUT, quiet=True); expect("baseline: SIG/BYTES/AUTH/DNSSEC pass", all(g[x] == "PASS" for x in ("SIG", "BYTES", "AUTH", "DNSSEC")))
L, g, f = V.run(str(f["joint"][1] + 60), TR, OUT, quiet=True); expect("eval time 60 s after the joint RRSIG expiry (KSK-2017 still in signing period) -> DNSSEC FAIL", g["DNSSEC"] == "FAIL")
L, g, f = V.run(str(f["declared"] - 86400 * 3), TR, OUT, quiet=True); expect("eval time before inception -> DNSSEC FAIL", g["DNSSEC"] == "FAIL")
t2 = copy.deepcopy(trust); t2["root_ksks"] = [x for x in t2["root_ksks"] if x["name"] == "KSK-2024"]
d = Path(tempfile.mkdtemp()); (d / "t.json").write_text(json.dumps(t2))
L, g, f = V.run("auto", d / "t.json", OUT, quiet=True); expect("KSK-2024-only trust before 2026-10-11 -> DNSSEC UNPERFORMABLE", g["DNSSEC"] == "UNPERFORMABLE")
L, g, f = V.run("1791676800", d / "t.json", OUT, quiet=True)   # 2026-10-11T00:00:00Z? KSK-2024 period begins but root DNSKEY not signed by it in this capture
expect("KSK-2024-only at 2026-10-11, capture lacks a 2024 signature -> not PASS", g["DNSSEC"] != "PASS")
t3 = copy.deepcopy(trust); t3["root_ksks"][0]["ds_digest_sha256"] = "00" * 32; t3["root_ksks"] = t3["root_ksks"][:1]
(d / "t3.json").write_text(json.dumps(t3)); L, g, f = V.run("auto", d / "t3.json", OUT, quiet=True)
expect("wrong pinned KSK digest -> DNSSEC not PASS", g["DNSSEC"] != "PASS")
t4 = copy.deepcopy(trust); t4["issuer_domain"] = "example.org"; (d / "t4.json").write_text(json.dumps(t4))
try:   # F4: a typed result is required; an exception is a control failure, not a rejection
    L, g, f = V.run("auto", d / "t4.json", OUT, quiet=True)
    expect("wrong domain D -> AUTH FAIL, DNSSEC typed (not PASS), verdict INVALID, no exception",
           g["AUTH"] == "FAIL" and g["DNSSEC"] != "PASS" and V.verdict(g) == "INVALID")
except Exception as e: expect(f"wrong domain D -> typed result (raised {type(e).__name__}: {e})", False)
print("NOTE: out-ksk2024 has no OTS proof; the capture end used below as T_snap is a TEST FIXTURE stand-in, not a verifier rule (the verifier gives UNVERIFIABLE/SNAPSHOT_NOT_ANCHORED).")
# A9.5 root-KSK rule + snapshot time rule. out-ksk2024/ has no receipt and no OTS proof, so its anchored time is STATED
# (capture end, a stand-in for T_snap) and the DNSSEC/time functions are called directly.
KO = HERE / "out-ksk2024"; ksnap = json.loads((KO / "dns-snapshot.json").read_text()); kT = ksnap["captured_end"]; D0 = trust["issuer_domain"]
def kdns(tr, now):
    L = V.Ledger(); used = V.check_dnssec(ksnap, tr, now, D0, L); return L, used
def kroot(L): return {r[0]: r for r in L.rows if r[0].startswith("DNSSEC.root.")}
L, used = kdns(trust, kT); r = kroot(L)
expect("rollover control: KSK-2024 signing, KSK-2017 published-not-signing, shipped two-KSK config -> DNSSEC PASS", L.status("DNSSEC") == "PASS")
expect("rollover control: KSK-2017 reported informational, not FAIL", r["DNSSEC.root.KSK-2017"][1] == "INFO" and "published_not_signing" in r["DNSSEC.root.KSK-2017"][2])
k17 = trust["root_ksks"][0]
expect("shipped config separates publication, signing and reliance; KSK-2017 signing ends 2026-10-11, reliance ends 2026-11-01 (= +21 d max observed RRSIG validity), published until 2027-03-22",
       k17["signing_valid_until"] == "2026-10-11T00:00:00Z" and k17["reliance_valid_until"] == "2026-11-01T00:00:00Z"
       and V.parse_iso(k17["reliance_valid_until"]) == V.parse_iso(k17["signing_valid_until"]) + k17["max_root_dnskey_rrsig_validity_s"]
       and k17["published_until"] == "2027-03-22T00:00:00Z")
a_k = {"T": kT, "confirmed_at": kT + 3600}; c = V.Ledger(); V.check_snapshot_time(kT, a_k, trust["params"], used, c)
expect("rollover control: snapshot time inside every RRSIG window and tolerance -> TIME/T_snap PASS", c.status("TIME") == "PASS" and c.status("DNSSEC") == "PASS")
# negative: snapshot anchored time outside an RRSIG window (joint window ends 2026-10-13T01:06:44Z)
c = V.Ledger(); V.check_snapshot_time(kT, {"T": 1791853604 + 3 * 3600, "confirmed_at": 1791853604 + 4 * 3600}, trust["params"], used, c)
expect("negative: snapshot anchored time after joint RRSIG window end -> T_snap FAIL", c.status("DNSSEC") == "FAIL")
L2, _ = kdns(trust, 1791853604 + 3 * 3600); expect("negative: validation at a time past the RRSIG expiry -> DNSSEC FAIL", L2.status("DNSSEC") == "FAIL")
# negative: outside the declared tolerance [declared - eps, declared + delta]
c = V.Ledger(); V.check_snapshot_time(kT - 4 * 86400, {"T": kT, "confirmed_at": kT + 3600}, trust["params"], used, c)
expect("negative: T_snap > declared + delta (inside window) -> TIME FAIL", c.status("TIME") == "FAIL" and c.status("DNSSEC") == "PASS")
c = V.Ledger(); V.check_snapshot_time(kT + 2 * 86400, {"T": kT, "confirmed_at": kT + 3600}, trust["params"], used, c)
expect("negative: T_snap < declared - eps (inside window) -> TIME FAIL", c.status("TIME") == "FAIL" and c.status("DNSSEC") == "PASS")
# negative: root DNSKEY set validated only by a trusted KSK outside its reliance period
t5 = copy.deepcopy(trust); t5["root_ksks"][1]["signing_valid_from"] = "2026-10-12T12:00:00Z"   # KSK-2024 signed, but its period starts after kT
L5, _ = kdns(t5, kT); r5 = kroot(L5)
expect("negative (a): only VERIFIED signature is by a KSK outside its reliance period -> FAIL (INVALID), KSK_OUTSIDE_RELIANCE_PERIOD",
       L5.status("DNSSEC") == "FAIL" and V.VERDICT[L5.status("DNSSEC")] == "INVALID" and any("KSK_OUTSIDE_RELIANCE_PERIOD" in x[2] for x in L5.rows)
       and "CANDIDATE_VERIFIED_NOT_USABLE" in r5["DNSSEC.root.KSK-2024"][2] and "in_reliance_period=False" in r5["DNSSEC.root.KSK-2024"][2])
# negative: KSK-2017 treated as signing (old config) must not matter; KSK-2017-only config cannot validate a 2024-signed set
t6 = copy.deepcopy(trust); t6["root_ksks"] = t6["root_ksks"][:1]; L6, _ = kdns(t6, kT)
expect("negative (b): KSK-2017-only trust, set signed only by unlisted KSK-2024 -> UNPERFORMABLE (UNVERIFIABLE), NO_TRUSTED_KSK_USABLE",
       L6.status("DNSSEC") == "UNPERFORMABLE" and V.VERDICT[L6.status("DNSSEC")] == "UNVERIFIABLE" and any("NO_TRUSTED_KSK_USABLE" in x[2] for x in L6.rows))
ks2 = copy.deepcopy(ksnap); ks2["messages"] = dict(ksnap["messages"]); ks2["messages"][". DNSKEY"] = ksnap["messages"]["com. DS"]
L7 = V.Ledger(); V.check_dnssec(ks2, trust, kT, D0, L7)
expect("negative (b): root DNSKEY RRset/RRSIG missing from snapshot -> UNVERIFIABLE, NO_TRUSTED_KSK_USABLE", L7.status("DNSSEC") == "UNPERFORMABLE" and any("NO_TRUSTED_KSK_USABLE" in x[2] for x in L7.rows))
# tampered signature
o2 = Path(tempfile.mkdtemp())
for fn in ("receipt-preimage.bin", "receipt-preimage.bin.ots", "dns-snapshot.json", "dns-snapshot.json.ots"): shutil.copy(OUT / fn, o2 / fn)
b = json.loads((OUT / "receipt.json").read_text()); s = bytearray(__import__("base64").b64decode(b["layer"]["slots"][1]["sig_b64"])); s[-3] ^= 1
b["layer"]["slots"][1]["sig_b64"] = __import__("base64").b64encode(bytes(s)).decode(); (o2 / "receipt.json").write_text(json.dumps(b))
L, g, f = V.run("auto", TR, o2, quiet=True); expect("flipped bit in slot-B signature -> SIG FAIL", g["SIG"] == "FAIL")
# OTS + pins on archived mainnet fixtures (same check_ots/conjuncts code path)
hd = json.loads((FX / "btc_headers_956576_956644.json").read_text())["headers"]
hdrs = {int(h): btc.Header.parse(bytes.fromhex(v["header_hex"])) for h, v in hd.items()}
pins = {"headers": {str(h): x.hash_hex for h, x in hdrs.items()}}
ots_b = (FX / "commit-03cd3db.txt.ots").read_bytes(); fb = (FX / "commit-03cd3db.txt").read_bytes()
L = V.Ledger(); a = V.check_ots("fx", ots_b, fb, hdrs, pins, 6, L)
expect("fixture: real mainnet OTS proof verifies to pinned headers", a is not None and L.status("OTS.fx") == "PASS")
print("   fixture attestations:", a)
bad = {"headers": dict(pins["headers"])}; bad["headers"][str(a["height"] + 2)] = "00" * 32
L = V.Ledger(); a2 = V.check_ots("fx", ots_b, fb, hdrs, bad, 6, L); expect("pin conflicting with presented header -> att FAIL", any(r[1] == "FAIL" for r in L.rows))
miss = {"headers": {k: v for k, v in pins["headers"].items() if int(k) != a["height"] + 1}}
L = V.Ledger(); V.check_ots("fx", ots_b, fb, hdrs, miss, 6, L); expect("header absent from pins -> HEADERS_NOT_COVERED (UNPERFORMABLE)", any(r[1] == "UNPERFORMABLE" and "NOT_COVERED" in r[2] for r in L.rows))
L = V.Ledger(); V.check_ots("fx", ots_b, fb + b"x", hdrs, pins, 6, L); expect("wrong file bytes -> digest FAIL", L.status("OTS.fx.digest") == "FAIL")
c = V.Ledger(); V.conjuncts("fx", a["T"] - 100, a, 72 * 3600, 24 * 3600, c); expect("three conjuncts hold at declared ~ T", c.status("TIME") == "PASS")
c = V.Ledger(); V.conjuncts("fx", a["T"] - 73 * 3600, a, 72 * 3600, 24 * 3600, c); expect("T later than declared+delta -> c2 FAIL", c.status("TIME") == "FAIL")
c = V.Ledger(); V.conjuncts("fx", a["T"] + 25 * 3600, a, 72 * 3600, 24 * 3600, c); expect("T earlier than declared-eps -> c1 FAIL", c.status("TIME") == "FAIL")
# ======================================================================== docs/reviews/v1-profile/ controls (2026-10-13)
# All variants are built in memory or in temp dirs; no fixture file is edited.
import base64 as _b64, itertools
import dns.message, dns.name, dns.rdatatype
def _msg(sn, key): return dns.message.from_wire(_b64.b64decode(sn["messages"][key]))
def _put(sn, key, m): sn["messages"][key] = _b64.b64encode(m.to_wire()).decode()
def _sigrr(m, name, covers, section="answer"):
    return next(rr for rr in getattr(m, section) if rr.rdtype == dns.rdatatype.RRSIG and rr.covers == covers and rr.name == dns.name.from_text(name))
def with_extra_sig(sn, key, name, covers, make):
    """Copy of snapshot `sn` whose RRSIG set for (name, covers) in message `key` also holds make(existing_rrsig)."""
    s2 = copy.deepcopy(sn); m = _msg(s2, key); rr = _sigrr(m, name, covers); base = list(rr)[0]
    rr.add(make(base)); _put(s2, key, m); return s2
def root_row(L): return next(r for r in L.rows if r[0] == "DNSSEC.root.dnskey_rrset")
osnap = json.loads((OUT / "dns-snapshot.json").read_text())
L0, g0, f0 = V.run("auto", TR, OUT, quiet=True); T0 = f0["eval"]          # the out/ snapshot's own anchored time
K17, K24 = trust["root_ksks"][0], trust["root_ksks"][1]
DK = dns.rdatatype.DNSKEY

# --- F1: existential, order-independent root rule. Bad candidate first, good second, in BOTH trust-list orders.
# (i) out/ capture: KSK-2017's genuine RRSIG re-tagged 38696 (cryptographically invalid for KSK-2024); KSK-2024's
#     signing start moved to 1 Oct so both candidates are eligible at T0 (Codex F1 reproduction).
bad24 = with_extra_sig(osnap, ". DNSKEY", ".", DK, lambda s: s.replace(key_tag=38696))
for order in ((K24, K17), (K17, K24)):
    tt = copy.deepcopy(trust); tt["root_ksks"] = [copy.deepcopy(x) for x in order]
    for x in tt["root_ksks"]:
        if x["name"] == "KSK-2024": x["signing_valid_from"] = "2026-10-01T00:00:00Z"
    L = V.Ledger(); V.check_dnssec(bad24, tt, T0, D0, L)
    expect(f"F1 bad KSK-2024 candidate + good KSK-2017, trust order {[x['name'] for x in order]} -> root PASS, DNSSEC PASS",
           root_row(L)[1] == "PASS" and "KSK-2017" in root_row(L)[2] and L.status("DNSSEC") == "PASS"
           and any(r[0] == "DNSSEC.root.KSK-2024" and "CANDIDATE_SIGNATURE_INVALID" in r[2] for r in L.rows))
# (ii) out-ksk2024 capture: KSK-2024's genuine RRSIG re-tagged 20326 (invalid for KSK-2017, which is present and in reliance).
bad17 = with_extra_sig(ksnap, ". DNSKEY", ".", DK, lambda s: s.replace(key_tag=20326))
for order in ((K17, K24), (K24, K17)):
    tt = copy.deepcopy(trust); tt["root_ksks"] = [copy.deepcopy(x) for x in order]
    L = V.Ledger(); V.check_dnssec(bad17, tt, kT, D0, L)
    expect(f"F1 bad KSK-2017 candidate + good KSK-2024, trust order {[x['name'] for x in order]} -> root PASS, DNSSEC PASS",
           root_row(L)[1] == "PASS" and "KSK-2024" in root_row(L)[2] and L.status("DNSSEC") == "PASS")

# --- F2 / A9.5 reliance period: honest old root (KSK-2017, signed 2026-10-01, before retirement) with a fresh lower
# chain (out-ksk2024, 2026-10-12). Root ZSK 8763 is in both root sets, so the composite is an honest cached-root case.
mixed = copy.deepcopy(ksnap); mixed["messages"][". DNSKEY"] = osnap["messages"][". DNSKEY"]
rel_end = V.parse_iso(K17["reliance_valid_until"]); sig_end = V.parse_iso(K17["signing_valid_until"])
expect("fixture sanity: kT is after KSK-2017's signing end and before its reliance end", sig_end < kT < rel_end)
L = V.Ledger(); used_m = V.check_dnssec(mixed, trust, kT, D0, L)
expect("F2 honest old-root/new-leaf, anchor after retirement, within reliance -> DNSSEC PASS, root validated by KSK-2017",
       L.status("DNSSEC") == "PASS" and root_row(L)[1] == "PASS" and "KSK-2017" in root_row(L)[2])
c = V.Ledger(); V.check_snapshot_time(kT, {"T": kT, "confirmed_at": kT + 3600}, trust["params"], used_m, c)
expect("F2 honest old-root/new-leaf: T_snap inside every witness window (root 10-01..10-22, leaf ..10-13) -> PASS", c.status("DNSSEC") == "PASS")
L = V.Ledger(); V.check_dnssec(mixed, trust, rel_end + 1, D0, L)
expect("F2 honest old-root evaluated 1 s after KSK-2017's reliance end -> root not PASS, DNSSEC not PASS",
       root_row(L)[1] != "PASS" and L.status("DNSSEC") != "PASS")
tr_short = copy.deepcopy(trust); tr_short["root_ksks"][0]["reliance_valid_until"] = "2026-10-11T12:00:00Z"
L = V.Ledger(); V.check_dnssec(mixed, tr_short, kT, D0, L)
expect("F2 isolate the reliance gate: same honest old root, RRSIG still in its window, reliance end moved before kT -> FAIL KSK_OUTSIDE_RELIANCE_PERIOD",
       root_row(L)[1] == "FAIL" and "KSK_OUTSIDE_RELIANCE_PERIOD" in root_row(L)[2])
L = V.Ledger(); V.check_dnssec(osnap, trust, V.parse_iso("2026-10-12T00:00:00Z"), D0, L)
expect("F2 withdrawn cutoff: out/ root set at 2026-10-12T00:00:00Z (was KSK_OUTSIDE_SIGNING_PERIOD) -> root PASS", root_row(L)[1] == "PASS")

# --- F3: the period reason only for a VERIFIED signature; a tag is not authorship.
t17 = copy.deepcopy(trust); t17["root_ksks"] = [t17["root_ksks"][0]]; t17["root_ksks"][0]["reliance_valid_until"] = "2026-10-11T12:00:00Z"
L = V.Ledger(); V.check_dnssec(bad17, t17, kT, D0, L)
expect("F3 forged retired tag (invalid RRSIG tagged 20326) on a set signed only by an unlisted key -> not KSK_OUTSIDE_RELIANCE_PERIOD; TRUSTED_KSK_SIGNATURE_INVALID",
       root_row(L)[1] == "FAIL" and "TRUSTED_KSK_SIGNATURE_INVALID" in root_row(L)[2] and "RELIANCE" not in root_row(L)[2])
corrupt = copy.deepcopy(ksnap); m = _msg(corrupt, ". DNSKEY"); rr = _sigrr(m, ".", DK); s0 = list(rr)[0]
sb_ = bytearray(s0.signature); sb_[10] ^= 1; rr.remove(s0); rr.add(s0.replace(signature=bytes(sb_))); _put(corrupt, ". DNSKEY", m)
L = V.Ledger(); V.check_dnssec(corrupt, t5, kT, D0, L)
expect("F3 corrupted signature by a trusted KSK outside its reliance period -> TRUSTED_KSK_SIGNATURE_INVALID, not the period reason",
       root_row(L)[1] == "FAIL" and "TRUSTED_KSK_SIGNATURE_INVALID" in root_row(L)[2])
mixed_el = copy.deepcopy(t5); mixed_el["root_ksks"][0]["reliance_valid_until"] = "2026-11-01T00:00:00Z"
L = V.Ledger(); V.check_dnssec(with_extra_sig(mixed, ". DNSKEY", ".", DK, lambda s: s), mixed_el, kT, D0, L)
expect("F3 mixed: eligible KSK-2017 witness present -> PASS regardless of other candidates", root_row(L)[1] == "PASS")

# --- F4: missing evidence is UNVERIFIABLE, typed, never an exception.
def copy_out(skip):
    o = Path(tempfile.mkdtemp())
    for fn in ("receipt.json", "receipt-preimage.bin", "receipt-preimage.bin.ots", "dns-snapshot.json", "dns-snapshot.json.ots", "bitcoin-pins.json", "bitcoin-headers.json"):
        if fn not in skip: shutil.copy(OUT / fn, o / fn)
    return o
try:
    L, g, f = V.run("auto", TR, copy_out({"dns-snapshot.json.ots"}), quiet=True)
    expect("F4 snapshot OTS proof absent -> no crash; OTS.snapshot and DNSSEC UNPERFORMABLE (SNAPSHOT_NOT_ANCHORED); verdict UNVERIFIABLE",
           g["OTS.snapshot"] == "UNPERFORMABLE" and g["DNSSEC"] == "UNPERFORMABLE" and any("SNAPSHOT_NOT_ANCHORED" in r[2] for r in L.rows)
           and V.verdict(g) == "UNVERIFIABLE" and f["eval"] is None)
except Exception as e: expect(f"F4 snapshot OTS proof absent -> typed result (raised {type(e).__name__}: {e})", False)
try:
    L, g, f = V.run("auto", TR, copy_out({"receipt-preimage.bin.ots"}), quiet=True)
    expect("F4 receipt OTS proof absent -> no crash; OTS.receipt UNPERFORMABLE; verdict UNVERIFIABLE", g["OTS.receipt"] == "UNPERFORMABLE" and V.verdict(g) == "UNVERIFIABLE")
except Exception as e: expect(f"F4 receipt OTS proof absent -> typed result (raised {type(e).__name__}: {e})", False)
try:
    nod = copy.deepcopy(ksnap); del nod["messages"][". DNSKEY"]; L = V.Ledger(); V.check_dnssec(nod, trust, kT, D0, L)
    expect("F4 '. DNSKEY' message absent -> DNSSEC UNPERFORMABLE (EVIDENCE_MISSING), no KeyError",
           L.status("DNSSEC") == "UNPERFORMABLE" and "EVIDENCE_MISSING" in root_row(L)[2])
    nos = copy.deepcopy(ksnap); del nos["messages"]["wamason.com. SOA"]; L = V.Ledger(); V.check_dnssec(nos, trust, kT, D0, L)
    expect("F4 child 'wamason.com. SOA' message absent -> UNPERFORMABLE, not FAIL", L.status("DNSSEC") == "UNPERFORMABLE")
except Exception as e: expect(f"F4 missing DNS message -> typed result (raised {type(e).__name__}: {e})", False)
o = copy_out(set()); (o / "dns-snapshot.json.ots").write_bytes((OUT / "receipt-preimage.bin.ots").read_bytes())
L, g, f = V.run("auto", TR, o, quiet=True)
expect("F4 snapshot proof present but for other bytes -> OTS.snapshot FAIL, and no authenticated evaluation time", g["OTS.snapshot"] == "FAIL" and f["snapshot_anchor"] is None)

# --- F5: only the successful witness is recorded; extra bad signatures do not narrow the joint window.
L = V.Ledger(); used_ok = V.check_dnssec(ksnap, trust, kT, D0, L)
ex = with_extra_sig(ksnap, "wamason.com. SOA", "wamason.com.", dns.rdatatype.SOA, lambda s: s.replace(expiration=kT - 3600))
L = V.Ledger(); used_ex = V.check_dnssec(ex, trust, kT, D0, L)
c = V.Ledger(); V.check_snapshot_time(kT, {"T": kT, "confirmed_at": kT + 3600}, trust["params"], used_ex, c)
expect("F5 valid + expired SOA RRSIG -> DNSSEC PASS, witnesses identical to the clean capture, T_snap check PASS",
       L.status("DNSSEC") == "PASS" and used_ex == used_ok and c.status("DNSSEC") == "PASS")
cs = with_extra_sig(ksnap, "wamason.com. SOA", "wamason.com.", dns.rdatatype.SOA, lambda s: s.replace(signature=bytes(len(s.signature))))
L = V.Ledger(); used_cs = V.check_dnssec(cs, trust, kT, D0, L)
expect("F5 valid + corrupt SOA RRSIG -> DNSSEC PASS, one witness per RRset", L.status("DNSSEC") == "PASS" and used_cs == used_ok)

# --- F6: the snapshot tolerance is against the RECEIPT's signed declared_issue_time, not the capture time.
snap_row = next(r for r in L0.rows if r[0] == "TIME.snapshot.c1_T>=declared-eps")
expect("F6 run(): snapshot conjuncts use receipt declared_issue_time (T_snap - declared), not captured_end",
       snap_row[2] == f"T-declared={f0['snapshot_anchor']['T'] - f0['declared']}s" and f0["snapshot_anchor"]["T"] - f0["declared"] != f0["snapshot_anchor"]["T"] - osnap["captured_end"])
c = V.Ledger(); V.check_snapshot_time(f0["declared"] + 30 * 86400, f0["snapshot_anchor"], trust["params"], [], c, captured_end=osnap["captured_end"])
expect("F6 receipt declared 30 d after an otherwise-good snapshot anchor -> TIME FAIL (capture/anchor pair alone is fine)", c.status("TIME") == "FAIL")
print(sum(1 for _, c in res if c), "/", len(res)); sys.exit(0 if all(c for _, c in res) else 1)
