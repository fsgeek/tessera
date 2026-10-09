"""Print the phase-3 results (THROWAWAY). Usage: uv run python run_phase3.py
Network: none. gpg: /usr/bin/gpg in a throwaway GNUPGHOME under prototype/.gnupg-phase3/ (removed at exit)."""
import time

from consumers import examiner as E
from consumers import relying_party as R
from consumers import scenarios
from tessera_proto.real import btc, canonical, dnssec, gitchannel, ots, pairings, rerun
from tessera_proto.real import world as RW
from tessera_proto.verifier import verify_bundle

FX = "tessera_proto/real/fixtures/"


def ts(t):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(t))


print("=== 1. CANONICAL FORM: number literals under three readings and the rfc8785 package")
for lit, row in canonical.classify(canonical.PROBE_LITERALS).items():
    print(f"  {lit:24s} " + "  ".join(f"{k}={v}" for k, v in row.items()))
bad = [r for r in canonical.appendix_b_results() if r[1] != r[3]]
print(f"  RFC 8785 Appendix B subset: {len(canonical.RFC8785_APPENDIX_B)} vectors; rfc8785 package mismatches: {len(bad)}")

print("\n=== 3. OPENTIMESTAMPS: the repo's real Bitcoin-anchored stamps")
for f, hf in (("commit-03cd3db.txt", "btc_headers_956576_956644.json"), ("commit-fcaa11b.txt", "btc_headers_959013_959094.json")):
    hs = btc.load_mainnet(hf)
    c = ots.check(ots.load(open(FX + f + ".ots", "rb").read()), open(FX + f, "rb").read(), hs)
    print(f"  {f}: file digest ok={c.file_digest_ok}; header segment PoW+linkage={btc.check_segment(hs, min(hs), max(hs))}")
    for b in sorted(c.bitcoin, key=lambda x: x["height"]):
        print(f"    height {b['height']} merkle_ok={b['merkle_ok']} nTime={ts(b['time'])} txid={b['txids'][-1][:16]}...")
    v = sorted(b["time"] for b in c.verified())
    print(f"    {len(v)} attestations; candidate anchor_time spread {(v[-1] - v[0]) / 3600:.1f} h")

print("\n=== 4. AUTHORITY CHANNELS (captured 2026-10-07, validated offline)")
for f in ("dnssec_wamason.com_TXT.json", "dnssec_ietf.org_TXT.json"):
    fx = dnssec.load(f)
    lo, hi = dnssec.common_window(fx)
    for label, now in (("at capture", (lo + hi) / 2), ("in 2106", 4_291_000_000)):
        r = dnssec.validate_offline(fx, now)
        print(f"  {f:30s} {label:10s} {r['status']:9s} {r['ledger'][-1][0][:90]}")
    print(f"    every RRSIG on the chain valid together only {ts(lo)} .. {ts(hi)} ({(hi - lo) / 86400:.1f} days)")
ev = gitchannel.collect("03cd3db06d4261ace0c8e8c9f18dcdb34d78e8a9", "docs/phase-0-prereg-amendment-1.md")
print("  git commit 03cd3db:", gitchannel.verify_offline(ev, open(FX + "tyst-commit-signing-key.pub.gpg", "rb").read()))

try:
    print("\n=== 2. SIGNATURE PAIRINGS under R-3.12 (one algorithm across slots)")
    w = RW.make_world_real()
    for name, keys in pairings.pairings(RW.gpg_home()).items():
        for per in (False, True):
            b = pairings.build_pair_layer(w, keys, {"x": "y"}, 1_790_000_000, per_slot_alg=per)
            L = verify_bundle(b, w.trust(), evaluate_standing=False)["layers"][0]
            print(f"  {name:38s} per-slot-alg={per!s:5s} {L['verification']:13s} failed={L['failed']}")

    print("\n=== 5. CONSUMERS: stub vs de-stubbed")
    out = {}
    for mode in ("stub", "real"):
        sc = scenarios.build(mode)
        rp, results, rev = R.run_all(sc)
        out[mode] = {(r.case, r.policy): r for r in results}
        if mode == "real":
            for k, case in rerun.extra_cases(sc).items():
                for pol in ("strict",):
                    r = rp.run(case, pol)
                    out[mode][(k, pol)] = r
            print("  submitter self-checks (real):", rerun.submitter_self_checks(sc))
            print("  attack replays (real): correct verdict, failed checks, mutant verdict, goal event on mutant")
            for k, v in rerun.replay_pairs(sc).items():
                print(f"    {k}: {v}")
            store = E.archived_store(sc.world)
            for m, sup in (("as is", None), ("complete", E.complete_spec_supplement(sc.world))):
                ex = E.examine(sc.cases["a"].bundle, store, sup)
                print(f"  examiner (real, {m}): {ex.verdict}; blocked={[s.name for s in ex.blocked()]}")
                print(f"    unlisted standards: {ex.unlisted}")
    print(f"  {'case':4s} {'policy':9s} {'stub (verification/standing)':44s} {'real':44s} naive/careful(real)")
    for key in sorted(out["real"]):
        rr = out["real"][key]
        rs = out["stub"].get(key)
        f = lambda r: "; ".join(f"{v.split('(')[0]}/{s}" for v, s, _ in r.layers) if r else "-"  # noqa: E731
        print(f"  {key[0]:4s} {key[1]:9s} {f(rs):44s} {f(rr):44s} {rr.outcome(rr.naive)} / {rr.outcome(rr.careful)}")
finally:
    RW.close()
