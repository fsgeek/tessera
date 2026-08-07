# Survivability mechanisms and capstone spike design — session rulings

**STATUS: DIALOGUE DECISIONS, DOCUMENT PENDING COLD READ.**
Three states apply throughout (per Codex review, adopted): *dialogue
decision* (the author selected it in session), *document pending cold
read* (this record, not yet adopted), *adopted record* (cold-read,
resolved, committed, stamped). Everything below is at most the first
two states.

**STATUS UPDATE (2026-08-07, end of session): AUTHOR ACCEPTED AS
WRITTEN** — see "Tony's notes" at the end of this document, which
also explicitly accept the real-first spike with the ablation
fallback. Adoption completes at the author's signed commit and OTS
stamp.

**Date:** 2026-08-07. **Ruling author:** Tony Mason. **Consultation:**
Claude (Fable 5), same-day dialogue; each item below is tagged with its
origin and its dialogue status. Per the credibility line, nothing here
is load-bearing until the author has read it cold and ratified or
overridden it — dialogue concurrence is not ratification.

Context: first Tessera session after a ten-day pause (NINeS '27
deadline). The 2026-07-28 record was still open — the symbolic-suite
architecture obligation sat uncommitted in `formal/PROPERTIES.md` and
the 2026-07-28 rulings had no ruling doc. Records for both were
drafted alongside this document; all three artifacts share the same
pending-cold-read state and are adopted together or not at all. Business-case questions (PQ signing as a first
value-added service) were explicitly deferred; only technical
obligations appear below.

## 1. Capstone obligation restated at requirement level

*(Assistant-proposed; author called the direction reasonable in
dialogue; ratification pending.)*

The 2026-07-28 dialogue ruling committed to a mechanism
("a capstone model that transcribes the shared library"). The
obligation is restated at the level of what must be true, so that
spike results can change the tactic without amending registered text:

> Band 0 exit is gated on a capstone composition context in which
> **every ledgered cross-model assumption — a fact one symbolic model
> assumes and another must establish — is discharged by a
> machine-checked producer query and carries a broken companion that
> must go red**. Layer 2 assumptions (cryptographic primitive
> security, historical trust-anchor correctness, chain availability,
> implementation fidelity, operational independence of authority
> channels) are **explicitly exposed and unclaimed in the ledger** —
> never discharged, never silently absorbed. Any termination-forced
> scoping is named in-module and disposed by amendment discipline,
> never silently.

*(Scope narrowed on Codex non-author review, 2026-08-07: the prior
"every ledgered assumption" read literally made Band 0 exit
impossible — ProVerif cannot discharge real-world assumptions — or,
worse, invited renaming assumptions until queries appeared to
discharge them. The ledger therefore carries two entry kinds:
dischargeable cross-model obligations and exposed Layer 2
assumptions.)*

The transcription pattern is demoted to a non-binding implementation
note, subject to the mechanism spike (§2). Guard against the known
trade-off: requirement-level text is where theater sneaks in, so the
requirement must be sharp enough to exclude weak readings — the
per-assumption red companion is the anti-theater clause, with the
precision (Codex, incorporated into pending draft): **a broken
companion must fail the query
that actually consumes the severed link**, not merely some unrelated
query elsewhere in the capstone. Amendment 3 registers the obligation
at this level.

**Ledger conservation rule (starting schema for the spike's
interface, per Codex review):** each ledger entry records at least —
consumer property/query; assumed fact; producer module and
event/query (or "Layer 2 — unclaimed"); the shared term or identifier
establishing correspondence; adversary capabilities at the join; the
broken mutation; the expected failing query; any residual Layer 2
assumption.

## 2. Capstone mechanism spike: real-first, ablate on break

*(Fork posed by author with both justifications; assistant voted
real-first; author ratification pending — this was an explicitly
joint decision with the vote recorded.)*

The fork: (a) start with a toy capstone and iterate toward
representative complexity — longer, but watches what breaks; or
(b) build at representative complexity first and, if it breaks,
ablate toward the break point (falling back to build-up if needed).

**Vote: (b), real-first.** Rationale: the spike's purpose is
falsification. A toy capstone cannot fail in the dimension that
matters (ProVerif termination under realistic theory complexity), so
its green bars manufacture confidence; toy-first iteration is
speculative, while ablation from an observed failure is directed by
that failure and converges faster.

Design constraints (predeclared):

1. **Representative target: the linked evidence floor chain**
   (Ruling 2 of `2026-07-28-identity-boundary-evidence-floors-ruling.md`)
   — the newest ruling and the structural worst case: linkage is
   where compositional seams and termination pressure live.
   Registered prediction: if an assumption cracks first, it is the
   linked-floor chain.
2. **The spike and the assumption-ledger interface are one artifact.**
   The drafted assumes-from-elsewhere ledger format is the spike's
   scaffolding; a throwaway format would validate nothing. The
   recorded sequence (A3 → ledger interface → scaffold) merges its
   middle step into the spike rather than gaining a step.
3. **Per-query timebox declared before running, with three named
   outcomes** (repaired on Codex review — the prior text called a
   timeout "a red result," conflating two different meanings of red):
   - **query violation** — a model counterexample; falsification
     evidence about the modeled property;
   - **timeout past the declared timebox** — a mechanism-viability
     failure of the chosen composition tactic, not evidence the
     property is false; disposition is ablation or a different
     tactic;
   - **successful termination** — evidence only for the checked
     abstraction.
   A broken companion "going red" means the first outcome on its
   targeted query, never the second.
4. **Predictions registered before running**, per house practice
   (pattern: `2026-07-21-claude-predictions-bridge-bench.md`).

## 3. Conformance vectors: fixed floor plus custodial rotation

*(Author's design principle; assistant withdrew its generator
proposal in dialogue.)*

The contamination paradox: the dead-project test's stand-in verifier
degrades as models train on the public repo — an uncontaminated
*verifier* cannot be guaranteed. Custodial challenge-minting
**reduces prior-exposure and rote-memorization risk**; it does not
guarantee novelty (reframed on Codex review — a candidate may have
retrieval access, later fine-tuning, or no stable cutoff, so "created
after the training cutoff" is not proof of non-memorization). Each
rotation therefore records its evaluation conditions: creation time,
disclosure state, candidate access, and the competency the challenge
is meant to exercise — novelty tests generalization and
reconstruction competence, not contamination alone. A challenge is
never declared uncontaminated merely because it is recent.

Two layers with different survival properties:

1. **Fixed floor in the bundle:** a committed set of conformance
   vectors, including the INVALID/UNVERIFIABLE traps. Memorizable,
   and that is acceptable — a floor only needs to catch a naive
   fail-open verifier.
2. **Novelty minted outside the bundle, as custodial practice:** new
   challenges constructed periodically by the then-current custodians.
   A rejected alternative is recorded (claim narrowed in Codex review
   round 2): a bundled challenge generator does not by itself
   guarantee non-exposure — its published cases and case distribution
   can be trained against — though a property-based generator with a
   large space or undisclosed seeds can still produce novel cases. It
   therefore cannot *replace* custodial rotation, which is the
   defensible form of the earlier "defeats itself" claim. The
   author's principle governs: defer the decision process to future
   entities with standing to amend, rather than automating it.

When an existing verifier fails a newly minted challenge, the failure
is a **measurement with three readings**, disposed under amendment
discipline: (a) the verifier was pattern-matching — contamination
exposed, the test working; (b) the challenge exceeds the declared
Designated Community competence — discard it or amend the
declaration; (c) the bundle genuinely lacks what the challenge needs
— a real survivability gap; fix the bundle.

## 4. Tending attestation (the renewal heartbeat)

*(Author-proposed mechanism, this session.)*

Custodians periodically attest that renewal tasks (timestamp
re-anchoring, algorithm re-wrapping, challenge rotation) were
performed. The red bar fires on **absence or staleness** of the
attestation, never on its truth — this is the identity boundary
applied inward: Tessera attests what was presented, and the tending
record is the same epistemology. What the mechanism buys: an untended
renewal chain currently fails *silent* (nobody notices until a
verifier hits a dead algorithm years later); the heartbeat converts
that into failing *visible* with a named claimant on the record —
fail-closed, applied in time.

**Scope correction and open design questions (Codex review,
incorporated into pending draft):** "silence is not contained in the
bundle." A stateless
verifier examining an old self-contained bundle cannot detect the
absence of a later event unless handed a current checkpoint,
succession record, or policy horizon — so the heartbeat is
**custodial-health monitoring machinery, not stateless-verifier
machinery**, unless A3 explicitly gives verifiers such an input.
Four questions A3 must answer before this obligation is registrable:
who observes that a tending attestation was expected; where the
expected cadence is declared; relative to which trusted time source
staleness is judged; and whether staleness affects receipt
verification, custodial-health reporting, or both. The cadence gets
**its own parameter and clock/trust assumptions** — δ, ε, and k
encode specific issuance/Bitcoin meanings and are not reused; only
the temporal modeling *pattern* carries over.

## 5. Post-quantum agility: prove the seam now, defer the algorithm

*(Author-proposed shape; assistant refinement: the permanent canary.)*

Motivation (refined in Codex review round 2 — OTS is a
timestamp/commitment mechanism, not a signature provider, and does
not belong in the signing-leg sentence): the portable signing leg
currently uses GPG, whose selected profile provides no PQ signature
algorithm; OTS remains the independent temporal-anchor mechanism and
does not fill that signing gap. (Corrected on verification
2026-08-07: A1 §3.1 already records that KMS supports post-quantum
ML-DSA (FIPS 204) key specs — confirmed against current AWS
documentation in round 2 — so the cloud leg's PQ path is an
integration, not a build; the real gap is the portable GPG leg.)
The ruling shape: **deferred from the proof of concept, gates the
production version** — the demonstrated capacity to add an algorithm
is the "future resistant" claim, not a bet on which algorithm
survives.

What Band 0 must carry now for that deferral to be safe:

1. **Algorithm agility in the signed bytes** — per P3, the signed
   bytes already include an algorithm identifier. (Repaired on Codex
   review: the prior text said the P8 framed envelope carries it,
   which is false — P8's frame is
   `type_tag || canonicalization_version || payload_length || payload`,
   verified against A1. The identifier lives inside the canonical
   payload per P3. This is a specification seam: **A3 must pin the
   identifier's exact location** — frame field or mandatory
   canonical-payload field — rather than leave it split across two
   property statements.)
2. **Unknown algorithm → UNVERIFIABLE — for exactly one case** (verdict
   boundary refined on Codex review): a well-formed, correctly bound,
   but unsupported algorithm identifier. All of the following remain
   INVALID: missing identifier; identifier/signature encoding
   mismatch; malformed parameters; an identifier prohibited by
   applicable policy; substitution of the signed identifier; a known
   algorithm whose signature fails. Landed twice: as a software
   red-bar test verifying the signing-provider API and model with the
   PQ implementation stubbed; and in the formal model as a
   P4-partition transition with a broken companion (a verifier that
   fail-opens past an unknown algorithm must go red).
3. **The canary never graduates:** a permanently reserved unrecognized
   algorithm identifier stays in the test suite even after a real PQ
   provider (ML-DSA / SLH-DSA class; FIPS 204/205 final) slots in —
   the UNVERIFIABLE path is tested forever, not just during the gap.
4. **Hybrid classical+PQ dual signing:** docketed for Amendment 3
   discussion, deferred with a clear conscience.

## 6. The custodial dependency, named

*(Joint; the load-bearing honesty clause of the survivability story.)*

"Attestation survives Tessera's termination" splits into **three**
claims with different truth conditions (expanded from two on Codex
review — being bytes guarantees portability, not survival; if every
copy disappears, the artifact does too):

1. **Portability / self-containment:** a possessed bundle can be
   verified without Tessera.
2. **Availability:** a copy remains obtainable only through retention
   and custody — custody is necessary *immediately*, not merely past
   the first algorithm death.
3. **Long-horizon evidentiary continuity:** validation across
   cryptographic decay requires renewal by custodians **before** the
   old mechanism becomes unreliable — matching RFC 4998's renewal
   "when necessary" and RFC 4810's required cryptographic-maintenance
   policy.

Amendment 3 should say this out loud rather than inherit it silently
from the ERS citation: the Designated Community is not only the
bundle's *audience* but its *custodian* — for availability from day
one, and for evidentiary continuity at every algorithm transition.
Structural guardrail, amendable by future decision makers as they
learn more.

## Amendment 3 docket additions arising from this session

- Capstone obligation at requirement level, with the two-kind ledger
  and conservation rule (§1).
- Evidence-floor linkage proved by the capstone, not just
  cardinalities (07-28 Ruling 2) — including the **chain-linkage
  mechanism fork** (07-28 doc, Ruling 2 item 5): A1 §A1.5's two
  external authority evidences (DNSSEC chain snapshot; anchored
  repository publication — the bundle carries them but is not a
  third authority) authorize issuer-key fingerprints, not exact
  manifest digests, so A3 must either extend the publication
  mechanism to commit to manifest digests, or restate the chain's
  first link as authorizing an exact tuple (issuer identity, key
  fingerprint, validity/epoch) that the manifest contains.
  Proof-of-possession must be by the **same key** whose signature is
  accepted.
- Floor/degraded-policy interaction made explicit (Codex,
  incorporated):
  redundant authority channels may be waived; the final complete
  chain may not be; when every external channel is unavailable the
  verdict is UNVERIFIABLE, not VALID_DEGRADED.
- Per-attestation-layer verdicts: independent layer verdicts vs one
  aggregate — A3 decides; existing P7 language favors independent.
- Conformance vectors: fixed floor + custodial rotation with recorded
  evaluation conditions, and the three-reading disposition rule (§3).
- Tending attestation obligations (§4) — joins the existing
  refusal-record storage/reporting docket line; must answer the four
  observer/cadence/clock/effect questions and register the cadence's
  own parameter.
- Algorithm-agility obligations, the refined verdict boundary, the
  algorithm-identifier location pin (P3 payload field vs frame
  field), and the permanent canary (§5).
- The custodial-dependency declaration (§6, three-claim form) folded
  into the Designated Community declaration.

## Assistant's self-corrections on the record

Recorded because predictions-first discipline applies to reasoning,
not just benches: (1) the assistant's initial spike proposal (toy
scale) was withdrawn as unable to fail in the dimension that matters;
(2) its generator-in-bundle proposal was withdrawn as
self-defeating; (3) its claim that the spike must precede the A3 text
freeze was withdrawn — requirement-level obligation text (§1) removes
the coupling.

## Non-author review round 1 (Codex, 2026-08-07)

Codex reviewed all three drafted artifacts (relayed by the author;
verdict: "do not record these three artifacts unchanged... I found no
reason to discard the core decisions"). The assistant's dispositions,
received-with-verification:

(Terminology per round 2: "incorporated" and "assistant accepted
after verification" — **"adopted" is reserved for the author's
adoption**, which has not occurred.)

- **Assistant accepted after source verification:** the external
  authority mechanism publishes key fingerprints, not manifest
  digests — chain-linkage fork registered (citation corrected in
  round 2 to A1 §A1.5: DNSSEC snapshot + anchored repository
  publication; the bundle carries the evidences but is not a third
  authority); P8's frame carries no algorithm identifier while P3's
  signed bytes do (checked against `phase-0-prereg-amendment-1.md`)
  — location pin registered; KMS ML-DSA support already recorded in
  A1 §3.1 — motivation corrected.
- **Assistant accepted as drafting defects in its own text:**
  "every ledgered assumption" over-breadth (§1); two meanings of
  "red" (§2); ratification-state inconsistency (status headers, both
  ruling docs); over-absolute novelty claim (§3); δ/ε/k reuse wording
  and the heartbeat's missing observer/clock model (§4); two-claim
  survivability split (§6).
- **Incorporated as clarifications:** ledger conservation rule;
  severed-link companion precision; per-layer verdict decision;
  floor/degraded/UNVERIFIABLE interaction; provenance portability
  statement (07-28 doc).
- **Left to the author (correctly):** the floor-formulation fork and
  every A3 registration. (Update, same day: the author dissolved the
  formulation fork in dialogue — the forms are complementary
  altitudes, both register in A3, bound by a mapping clause; see the
  07-28 doc, Ruling 2 item 5. The digest-vs-tuple and
  adoption-route decisions remain open for cold read.)

## Non-author review round 2 (Codex, same day)

Verdict on the round-1 repairs: "nearly ready," four record-level
cleanups, all incorporated after verification: (1) the adoption-route
choice framed explicitly, with the recommended minimal adopted floor
statement recorded in the 07-28 doc's status block; (2) "adopted"
vocabulary reserved for the author throughout; (3) the
authority-mechanism citation corrected to A1 §A1.5 (verified against
source — two external evidences, fingerprints not digests, bundle as
carrier); (4) the tooling sentence repaired — OTS is a
temporal-anchor mechanism, not a signature provider, and the KMS
ML-DSA claim was reconfirmed against current AWS documentation.
Optional narrowing also incorporated: a bundled generator "cannot
replace custodial rotation" (defensible) rather than "defeats
itself" (over-broad). Codex's closing position: comfortable
recording the three artifacts as an adopted session record with
explicitly docketed Amendment 3 decisions, after these changes.

## Tony's notes

This document had its "cold read" and then went through multiple rounds
of adversarial review, and further revision.  Thus, subsequent reads
are not cold reads any longer.

The only remaining clarification appears to be the capstone mechanism
spike, and I accept the proposal to build the full example with a
fallback mechanism for analyzing potential failure.

Thus, I accept this as written.
