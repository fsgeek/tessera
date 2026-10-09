"""Print the phase-2 consumer results (THROWAWAY). Usage: uv run python run_phase2.py"""
from consumers import examiner as E
from consumers import relying_party as R
from consumers import scenarios

sc = scenarios.build()
print("=== SUBMITTER")
sub = sc.submitter
out_bundle = sc.cases["g"].bundle
sub.self_check(out_bundle, "at-ship")                       # with the verifier release it already had
sub.self_check(out_bundle, "at-ship", trust=sc.trust())     # with a refreshed release
sub.self_check(sc.cases["a"].bundle, "completed", trust=sc.trust())
sub.find_my_statement(sc.cases["a"].bundle, sc.honest_payload)
sub.portable_kit(sc.cases["a"].bundle, sc.honest_release)
print(sub.log.render())

print("\n=== RELYING PARTY (today)")
rp, results, rev = R.run_all(sc)
print(f"{'case':4s} {'policy':9s} {'layers (verification / standing)':78s} {'naive':28s} careful")
for r in results:
    lay = "; ".join(f"{v.split('(')[0]}/{s}" for v, s, _ in r.layers)
    print(f"{r.case:4s} {r.policy:9s} {lay:78s} {r.outcome(r.naive):28s} {r.outcome(r.careful)}")
print("revocation view:", {k: rev[k] for k in ("bundle_members_carrying_revocation", "reported_REV_checks",
                                               "verdict_as_reported", "verdict_if_REV_unperformable",
                                               "verdict_with_G27_extension")})
print(rp.log.render())

print("\n=== 2106 EXAMINER")
store = E.archived_store(sc.world)
for label, b in (("honest complete (a)", sc.cases["a"].bundle), ("revoked in window (e)", sc.cases["e"].bundle),
                 ("as shipped (g)", sc.cases["g"].bundle)):
    for mode, sup in (("as is", None), ("complete spec", E.complete_spec_supplement(sc.world))):
        ex = E.examine(b, store, sup)
        bl = [s.name for s in ex.steps if s.status == "blocked"]
        print(f"{label:24s} {mode:14s} verdict={ex.verdict:13s} trusting-reconstructions={ex.verdict_if_trusting_reconstructions:42s} blocked={bl}")
ex = E.examine(sc.cases["a"].bundle, store)
for row in ex.table():
    print(f"  {row[1]:13s} {row[0]:62s} {row[2]}")
print(ex.log.render())
print("\nWhat the stubbed anchor hides:")
for k, v in E.STUB_HIDES:
    print(f"  - {k}: {v}")
