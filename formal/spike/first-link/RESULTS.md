# First-link mechanism spike — predictions vs. observed

**Status: FINAL (query evidence).** All eight strict-mode runs were
independently reproduced by Codex (2026-08-09, same ProVerif 2.05,
matching outputs). Codex's review identified the single-evidence
coverage gap (ledger entry 4); PREDICTIONS-ADDENDUM-1 was registered,
author-ratified, and its ten runs completed 2026-08-09 — dispositions
in the addendum section below. Non-query spike-exit items (decision
document, standing/A2.4 statement) remain and are tracked in
PREDICTIONS.md/FIRST-LINK-SPIKE.md.

Run date: 2026-08-09. ProVerif 2.05, built from source on this
machine (opam/OCaml 4.14.2, no-root path — toolchain re-established;
the tool-spike install lived on the other machine of the split).
All `.pv` and `.out` files in `proverif/`; run-1 evidence preserved
as `*_run1.out` where a recut occurred. Every run terminated in
seconds; no timebox was approached; the ablation rule was never
invoked.

## Ladder outcomes (2 channels × 4 queries — all eight runs)

| Query | Variant | Predicted (frozen) | Observed |
|-------|---------|--------------------|----------|
| Q1 chain, correct model | DNS-comp. | holds p≈0.7 / violation p≈0.2 / timeout p≈0.1 | run 1: **violation** (p≈0.2 branch); run 2 after registered-branch recut: **holds** |
| Q1 | repo-comp. | same | same, both runs |
| Q2 broken companion | DNS-comp. | violation found p≈0.75 | **violation + TwoWorldsBroken reachable** — required result |
| Q2 | repo-comp. | same | same |
| Q3 mechanism, correct | DNS-comp. | holds p≈0.6 | **holds** |
| Q3 | repo-comp. | same | **holds** |
| Q4 attack vs intact mechanism | DNS-comp. | no attack p≈0.55 / real attack p≈0.2 / timeout p≈0.25 | **no attack — TwoWorldsBroken unreachable** |
| Q4 | repo-comp. | same | same |

Overall registered prediction (p≈0.5): transcription binding survives
Q4 in both variants — **observed**.

## Finding 1 (Q1 run 1): the formal content of "never all"

The conjunctive conclusion — acceptance implies BOTH channels'
publication events — was falsified in both variants by the same
trace shape: the adversary holding a leaked channel key forges its
own copy of evidence *for the honest tuple* and never lets that
channel's honest process run. The accepted statement is still
exactly the honest tuple (the uncompromised channel pins it), but a
compromised channel's publication event is forgeable-around by
definition.

Disposition (the registered p≈0.2 branch: trace inspection, not
pre-classification): encoding overclaim revealing design content.
What the two-channel strict rule actually guarantees under the A1.3
"never all" adversary is:

> at least one UNCOMPROMISED channel published this exact authority
> tuple

— a disjunctive, variant-independent claim. The recut (see comment
block in each chain-query file; run-1 evidence preserved) disjoins
the channel-publication conclusion and keeps the possession and
signature links conjunctive. This sentence belongs in the capstone
ledger and, eventually, in the relying-party story: presented
evidence artifacts are not individually provenance-guaranteed;
the *statement* is.

## Finding 2 (Q2): the two-worlds attack needs no channel compromise

The broken companion's attack derivation uses only *honest* evidence
objects — the weakened binding (issuer identity only) lets the
attacker substitute their own key fingerprint under evidence every
verifier accepts, with no leaked key involved. The channel-compromise
variants were run per registration, but the binding weakness alone is
sufficient. Ledger consequence: the first-link binding defends
against a strictly stronger adversary than channel compromise —
losing it is worse than losing a channel.

## Q2 attack instantiation (authority-relevant difference confirmed)

One evidence pair `sign((STMT,issuerId),skD), sign((STMT,issuerId),skR)`
supports both `(issuerId, fp(pk(k_att)), ss', alg', ver')` and
`(issuerId, fp(pk(skI)), ssetH, algH, verH)` — tuples differing in
the **key fingerprint** (and free fields), all map-v1
authority-relevant. Judged against frozen map v1: a genuine
two-worlds companion. The Grok panel criterion is satisfied; no
amendment trigger.

## Ledger entries (A3.3 conservation fields)

1. **Q1/Q3 chain correspondence.** Consumer: §A3.2 witness chain,
   first link. Assumed fact: at least one authority channel
   uncompromised (A1.3 "never all", cited explicitly per the DeepSeek
   panel criterion — the adversary controls any strict subset).
   Producer: `q1_chain_*.pv` / `q3_mechanism_*.pv`, chain
   correspondence query. Shared terms: authority tuple, accepted key,
   framed bytes. Adversary at the join: one channel key leaked (both
   variants run). Residual Layer 2: none for Q1 (specification-level);
   for Q3, **collision resistance of the concrete digest** — symbolic
   h is injective by construction; discharged by cited external
   hardness assumptions per prereg §8, never by these models.
2. **Q2 broken companion.** Mutation: evidence binds issuer identity
   only (proper subset of map v1). Expected failing query: chain
   correspondence + TwoWorldsBroken reachability — both failed/fired
   as required, both variants. Does not discharge anything; exists to
   prove the queries can go red.
3. **Q4 attack objective.** Consumer: §A3.2.1 boundary invariant.
   Mechanism intact; TwoWorldsBroken unreachable, both variants.
   Same Layer 2 residual as Q3 (digest collision resistance).
4. **Judge encoding note — CORRECTED 2026-08-09 (Codex independent
   review).** The two-worlds condition is mechanized as a
   private-channel judge over accepted records (evidence pair,
   tuple); "evidence object" is represented as the evidence *pair*
   consumed by one acceptance. A prior version of this entry claimed
   the per-single-evidence formulation was "strictly implied" by the
   pair result. **That claim is false** (counterexample: DNS evidence
   weakly bound, repository evidence strongly bound — one DNS object
   supports two authority-distinct tuples, but the two acceptances
   carry different repository objects, so no shared pair exists; the
   pair judge stays green over a vulnerable single-evidence path).
   The pair result covers strict two-channel mode only. Since A3.2
   permits `VALID_DEGRADED` with fewer-but-never-zero external
   evidences, single-evidence acceptance is a live verdict path
   requiring its own coverage: see PREDICTIONS-ADDENDUM-1.md.

## Addendum 1 — single-evidence coverage: predictions vs. observed

All ten runs 2026-08-09, each terminating in seconds; no timebox
approached. Models and `.out` evidence in `proverif/` (q5*, q6*, q7,
q8).

| Query | Predicted (frozen) | Observed |
|-------|--------------------|----------|
| Q5a DNS-only, honest | holds p≈0.7 | **holds** |
| Q5b DNS-only, compromised | **EXPECTED violation** p≈0.8 (the waiver cost) | **violation, as registered** |
| Q5r honest | holds p≈0.7 | **holds** |
| Q5r compromised | expected violation p≈0.8 | **violation, as registered** |
| Q6 × 4 (single-object two-worlds, mechanism intact, honest+compromised, both channels) | unreachable p≈0.75 each | **unreachable, all four** |
| Q7 contrast (DNS weak / repo strong) | Single REACHABLE p≈0.8 AND Pair UNREACHABLE p≈0.75 | **exact contrast observed** |
| Q8 contrast (repo weak / DNS strong) | same | **exact contrast observed** |

**Disposition, Q5b/Q5r-compromised (the registered red):** when the
sole accepted evidence channel is the compromised one, no provenance
guarantee survives — now machine-documented, not just stated. This
is the formal price of waiving the redundant authority channel; it
maps to the A1.2.1 lattice (the waiver is recorded, the risk is the
relying party's accepted risk) and enters the relying-party story:
`VALID_DEGRADED` with a single external evidence means *the
surviving channel is your provenance root; if it was compromised,
you have none.* The boundary invariant, by contrast, survived even
there (Q6 compromised variants unreachable): one object, one digest,
one tuple — the mechanism's unconditional half.

**Disposition, Q7/Q8 (the contrast):** the pair-judge blind spot now
exists as machine evidence — TwoWorldsSingle reachable while
TwoWorldsPair stays unreachable in the same model. The retracted
RESULTS.md implication ("pair coverage implies single coverage") is
refuted by executable counterexample, both asymmetry directions.

**Ledger addendum entries:** (5) Q5/Q6 consume the same Layer 2
digest-collision-resistance residual as Q3/Q4. (6) Q6's unconditional
result explicitly does NOT depend on the A1.3 "never all" assumption
— the boundary invariant holds per-object even under full compromise
of the accepted channel; only provenance (Q5) needs "the accepted
channel is honest." This split — what the mechanism owes
unconditionally vs. what honesty assumptions buy — is the addendum's
core design content, and belongs in the decision document and the
relying-party story.

**Criterion 0 status (the mechanism-selection gate):** all three
legs green — strict Q4 unreachable (both variants), Q6 unreachable
(both channels, both compromise states), Q7/Q8 contrasts fired as
designed. Transcription binding is eligible for selection.

## What remains before spike exit (non-query conditions, per the
frozen registration)

- Mechanism decision document (DECISION.md pattern): scoring
  transcription binding against the seven registered criteria;
  criterion 0 (the gate) is discharged on all three legs — strict Q4
  (both variants), Q6 (both channels, both compromise states), and
  the Q7/Q8 contrasts — within the checked symbolic abstraction.
  (This sentence originally cited Q4 alone, written before the
  addendum; corrected 2026-08-09 per Codex round-2 review.)
  Candidates 2–5 were not required to be modeled (no Q4 failure);
  their comparison is criteria-level and goes in the decision
  document. Author cold read of the correct models precedes
  ratification, per the tool-spike precedent.
- Standing/A2.4 coexistence statement for the selected mechanism.
- Standing test conditions registered in lineage-present and
  lineage-absent forms.
- Authority-relevance map: **no divergence** — map v1 survived the
  runs unchanged; the Q2 companion was judged against it as frozen.
