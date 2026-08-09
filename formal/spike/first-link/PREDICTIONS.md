# First-link mechanism spike — query plan and registered predictions

Status: ADOPTED v3 by author after prior review rounds and corrections.
(v1 and v2 drafted 2026-08-09; revised same day after Codex non-author
review — six findings, all confirmed against the adopted texts,
dispositions in the review log below. Per
the FIRST-LINK-SPIKE.md discipline, predictions are committed BEFORE
any model is run — the author's signing commit freezes this document,
including authority-relevance map v1, and opens the runs).

Governed by: FIRST-LINK-SPIKE.md (adopted `8ae4720`), A3 §A3.2.1
(boundary invariant), §A3.3 (three-outcome timebox discipline),
§A3.9 panel-added exit criteria.

## Target

The §A3.2 witness chain's first link:

> accepted external authority evidence
> → the exact authority statement consumed from the manifest

under the §A3.2.1 boundary invariant:

> Two manifests that differ in any authority-relevant fact must not
> be supportable by the same evidence.

Representative complexity first (registered discipline): the full
six-node witness chain is the structural worst case; queries start
there and ablate toward the break point only on failure.

## Authority-relevance map v1 — FROZEN at the signing commit

The broken companions are judged against this map as frozen. Any
later change to the map is recorded as a **prediction divergence**
(not a refinement) and forces a fresh companion and a Q2 re-run.

Authority-relevant (two manifests differing in any of these are
authority-distinct):
- issuer identity
- signing-key fingerprints (each member of the required-signer set)
- required-signer set composition (the P2 manifest)
- algorithm identifiers for each required signature
- authority-statement version / the exact consumed statement bytes

Non-authoritative (may differ without authority distinction):
- display labels, human-readable names
- optional metadata not consumed by any verification check
- ordering of equivalent manifest entries (canonicalization's
  territory, P8)

**Anchor identity: excluded from this map, by citation.** A3.1's
coverage map assigns anchor identity → A2.4 and manifest authority →
P10: the anchor transaction id is defended by its own chain
relationship, not by the first link. (Clerk determination from
registered text, concurring with the Codex review's technical
leaning; the author's signing commit ratifies or overrides it.)

## Tooling

ProVerif 2.05 (DECISION.md, ratified). Adversary: A1.3, with the
panel-registered capability made explicit in every query's ledger
entry: the adversary controls any strict subset of authority
channels, never all.

**Channel coverage (both compromise cases, independently — ALL
queries).** The two authority channels (DNS evidence, repository
evidence) are not symmetric — different formats, different binding
surfaces. Every query in the ladder, correct models included, runs
twice: once with the DNS channel adversary-controlled, once with the
repository channel adversary-controlled, full timebox per variant.
Correct baselines matter here as much as attacks: a negative
experiment is evidence only against a matching correct form, so each
Q2/Q4 channel variant pairs with the exactly corresponding Q1/Q3
variant, and the evidence matrix stays obvious (2 channels × 4
queries). A generic single-channel abstraction is not accepted as
representing both. Rejection is modeled as
non-acceptance (tool-spike idiom); verdict partition remains TLA+
territory.

## Query ladder, timeboxes, predictions

Predictions registered with rough probabilities. Outcome vocabulary
is the registered three: **violation** (counterexample trace),
**timeout** (mechanism failure — evidence about the tool/encoding,
never about the property), **termination** (evidence for the checked
abstraction only). Timeboxes are per run (channel variants each get
the full box).

**Q1 — correct model, full-chain linkage correspondence.**
The six-node chain encoded as a correspondence: acceptance of framed
bytes implies the linked chain of events back to accepted external
authority evidence, with these exact shared terms crossing the
links — **same authority statement** (the exact consumed statement,
NOT the whole manifest; manifests may differ in map-non-authoritative
fields), same issuer identity and required-key relation, same
accepted key through possession and signature, same signed framed
bytes.
- Timebox: 15 minutes per variant; both channel variants run.
- Prediction: terminates, property holds, both variants. (p ≈ 0.7;
  p ≈ 0.2 violation — most likely an encoding defect per the
  tool-spike round-1 pattern, but disposition requires trace
  inspection and may reveal a genuine model/design mismatch;
  p ≈ 0.1 timeout.)

**Q2 — two-worlds broken companion (binding weakened).**
Mutation: authority evidence commits to a proper subset of map v1
(e.g. issuer identity only, not key fingerprints). Run in both
channel-compromise variants. Required result: the linkage query
FAILS — a trace where one evidence object supports two manifests
differing only in a map-v1 authority-relevant field.
- Timebox: 15 minutes per variant.
- Prediction: violation found in both variants, traces readable.
  (p ≈ 0.75; p ≈ 0.15 the mutation needs one recut; p ≈ 0.05 only
  one channel variant exhibits the attack — itself a finding worth
  a ledger entry; p ≈ 0.05 timeout.) Per the Grok panel criterion:
  if no such companion can be produced at all, that is an amendment
  trigger, not a shrug.

**Q3 — candidate mechanism: transcription binding.**
The non-binding candidate from §A3.3: evidence commits to the exact
authority statement (digest of the map-v1 authority-relevant tuple).
Full-chain query on the correct model with the mechanism in place.
- Timebox: 30 minutes per variant; both channel variants run.
- Prediction: terminates, property holds, both variants. (p ≈ 0.6;
  p ≈ 0.25 violation — most likely an encoding defect, but
  disposition requires trace inspection and may reveal a mechanism/
  design mismatch; p ≈ 0.15 timeout — the binding term enlarges
  message structure; state-space risk concentrates here.)

**Q4 — two-worlds ATTACK OBJECTIVE against the intact mechanism.**
Distinct from Q2's mutation, explicitly: Q4 leaves the Q3 binding
mechanism fully intact and asks whether the A1.3 adversary
(controlling one channel; both variants run) can nevertheless cause
one evidence object to support two manifests differing in a map-v1
authority-relevant field. Nothing is removed; the adversary must beat
the mechanism, not its absence. Correct and broken artifacts are
thereby unmistakably distinguishable: Q2 breaks the model, Q4 breaks
(or fails to break) the mechanism.
- Timebox: 30 minutes per variant.
- Prediction: no attack found, terminating, both variants.
  (p ≈ 0.55; p ≈ 0.2 a REAL attack surfaces — the outcome that earns
  the spike its keep and forces mechanism revision; p ≈ 0.25
  timeout.) Q4 carries the highest genuine uncertainty and is the
  reason the spike exists.

**Ablation rule (on any timeout):** shorten the chain from the
evidence end (drop nodes toward signature→bytes), re-run, and record
the break point. The ledger entry for the timed-out query records
"mechanism failure at N nodes," never a property claim.

**Ordering rule:** Q1 before Q2; Q3 before Q4. Map v1 freezes at the
signing commit, before Q2 exists; post-freeze map changes are
prediction divergences forcing fresh companions.

## Mechanism selection — candidates and criteria (registered before evidence, per the DECISION.md pattern)

Candidates on the table before any run:
1. **Transcription binding** (§A3.3's non-binding candidate; Q3/Q4's
   subject).
2. **Digest publication** (the A3.2.1 docketed option, still live as
   a candidate — the override deferred selection, it did not reject).
3. **Authorized tuple** (the other docketed option, same status).
4. **Separately hashed manifest core** (authority-relevant fields
   sub-hashed as a distinct object).
5. **A strengthened variant of any of the above**, if the experiment
   exposes the need.

Criteria, in order — **criterion 0 is a gate, not a weight**:
0. Satisfies the §A3.2.1 boundary invariant under Q4-style attack in
   both channel variants. A candidate failing this is ineligible;
   no other virtue compensates.
1. No manifest/evidence self-reference (the defect that forced the
   A3.2.1 override).
2. Exact correspondence with frozen map v1 — binds all
   authority-relevant fields, no non-authoritative field smuggled in.
3. Sound under each single-channel compromise, for both channels.
4. Evidence independently reconstructable from the preserved bundle
   (survivability claim 1 compatibility).
5. Compatible with standing evidence and A2.4's exactly-one-shipped-
   anchor rule (see exit conditions below).
6. Author readability and conformance-test clarity (the agreement-
   gate requirement, as in the tool spike).

If a candidate other than transcription binding must be modeled, its
queries get registered predictions in an addendum to this document
BEFORE running, same discipline.

## Non-query exit conditions (spike completion requirements, per FIRST-LINK-SPIKE.md — not dischargeable by Q1–Q4)

1. **The standing/A2.4 tension is resolved within the spike:** the
   decision document states explicitly how abandoned-artifact-alone
   standing evaluation coexists with exactly-one-shipped-anchor, for
   the selected mechanism. If they cannot coexist, the decision
   document names which registered statement requires amendment,
   before any implementation.
2. **The selected mechanism's effect on abandoned-artifact-alone
   evaluation is stated** — what a verifier holding only the
   abandoned artifact can and cannot establish.
3. **Standing test conditions registered in both forms:**
   lineage-present and lineage-absent (the hard alone-case is
   mandatory, per the DeepSeek panel criterion).
4. Predictions-vs-observed recorded per query, including the channel
   variants separately.

## Ledger scaffolding

Each query lands one capstone-ledger entry with the A3.3 conservation
fields: consumer property/query; assumed fact; producer module;
shared binding term; adversary capabilities at the join (explicitly:
which authority channel is compromised); residual Layer 2 assumption.

## Exit

The spike exits per FIRST-LINK-SPIKE.md: mechanism decision document
(criteria above, scoring recorded after evidence), map v1 plus any
divergence record, correct + broken `.pv` + `.out` committed,
predictions-vs-observed per query, and the non-query exit conditions
above discharged. Predicted overall outcome, for the record:
transcription binding survives Q4 in both variants and is selected
under the registered criteria (p ≈ 0.5), with the most likely
alternative being a strengthened variant after a Q4 attack (p ≈ 0.2).

## Review log

- 2026-08-09, Codex (non-author, cold to this document's drafting):
  six findings — map not frozen before Q2 / anchor question open;
  Q1 bound "same manifest" against the registered "exact authority
  statement"; Q4's mutation language self-contradictory; selection
  criteria absent (retrospective-selection risk); standing/A2.4
  resolution deferred beyond the spike against the adopted text;
  single-channel abstraction unjustified for asymmetric channels.
  All six confirmed against the adopted sources and incorporated in
  this v2. The anchor-identity disposition is by citation to A3.1's
  coverage map (anchor identity → A2.4), concurring with the
  reviewer's leaning.
- 2026-08-09, Codex round 2: five findings closed; one baseline-
  coverage clarification (correct models must run per-channel so
  every attack variant has a matching correct baseline — applied to
  Q1/Q3 and the channel-coverage rule; evidence matrix is 2 channels
  × 4 queries) and one non-blocking epistemic wording improvement
  (an unexpected Q1 violation is not pre-classified as an encoding
  defect; disposition requires trace inspection — applied to Q1 and,
  for consistency, Q3). Approved subject to these, both applied in
  this revision.
- 2026-08-09, Author reviewed and approved.  This authorizes moving
  to the next phase of work by freezing the predictions and
  authority-relevance map v1. As a result this opens the model runs.
