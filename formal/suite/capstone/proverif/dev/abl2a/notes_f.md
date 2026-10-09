### (f) draft — amendment-shaped, stated and NOT taken

**F-1 — the registered ablation order cannot touch the cause it is being
applied to.** §3's order is *"drop the depth-2 layer, then `skI2`, then the
second lineage shape, then the `|set| = 2` branch"* — four **fixture**
thinnings. The diagnosis in §(a) says the cause is a **verifier** mutation that
frees a variable in the acceptance path; no step in the order touches the
mutation, because a companion's mutation is what the companion **is**. The
order can therefore only work by shrinking the fixture the freed variable ranges
over. Whether that is enough is an empirical question (§(c)). **If it is not**,
the registration has no further step, and adding one — e.g. "then run each
link-2b conjunct as its own file" or "then drop the second authority channel" —
would be an **amendment to §3's ablation rule**, appended and dated. Not taken
here.

**F-2 — ablation 2 (`skI2`) removes the one-signer branch's only honest
attester, and the query under ablation is the one-signer conjunct.** §1.1 fixes
*"the one-signer manifest `M1` names `fp(pk(skI2))`, and `skI2` signs `M1` and
nothing else"*, under the **ONE KEY, ONE MANIFEST** rule. With `skI2` gone,
`capstone.pv`'s `AttestStage` one-signer branch has no honest `OT_ATTEST`
producer for `M1` at all; the only remaining `signers0` manifests are `MW`
(whose key `skW` runs `Wrapper` only, so it produces `OT_WRAPPER` frames and
fails the branch's `otA = OT_ATTEST` guard) and the adversary's self-signed `MA`
(which cannot pass strict check 1, because the repository key is honest). So a
**green at ablation 2 may be a vacuity, not a proof** — the ablation has
removed the witness the query is about. The registration's C-N1 witnesses
(`HonestChain`, `HonestComplete`) are exactly what would detect that, and the
isolated file has them deleted **by the brief's own instruction** ("ONLY the
link-2a query"). **This is amendment-shaped** because it bears on what §3's
sentence *"Ablation on any timeout, in order, break point recorded"* means when
a step removes the ablated query's own witness: a break point reached
vacuously is not a break point. Not taken; but see §(e) — the recommendation
does not rest on a green at ablation 2 without a witness re-run.

**F-3 — link 2b's three conjuncts are three separate `query` declarations.**
`capstone.pv:253-264`. The ProVerif manual (§6.7.2, "Grouping queries") says
independent `query` declarations *"are evaluated by rebuilding a new set of
clauses from scratch for each"*, and advises grouping *"queries that involve the
same events"* — which these three are (`AcceptanceComplete`, `SlotSatisfied`,
and nothing else). Grouping them into one declaration is a **pure encoding
question** with identical results, so it would be a **recut, not an
amendment** — but it changes nothing about the peak of a single conjunct's
saturation, which is what kills, so it is recorded and not recommended as the
fix.

**F-4 — a label already on the record.** `owner_interventions.log:2` and the
memory note both name the killer *"link 2a"*. §0 above shows it is link 2b
conjunct 1 (and, for `cap_cc06_b`, conjunct 2). Correcting a log line is
clerical. But **§3 registers link 2a and link 2b separately, with different
predictions, different residuals and different timeboxes** (link 2a: green
p ≈ 0.8, 45 min, PREDICTIONS.md:407-410; link 2b: its own row), so **which link
a mechanism failure is disposed under is not cosmetic** — it decides which
registered row carries the "timeout, disposed by ablation" note. Recording it
against link 2b is a correction of fact, not an amendment; any RESULTS.md cell
already written against link 2a needs the same correction.
