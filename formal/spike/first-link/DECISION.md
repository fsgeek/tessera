# First-link mechanism decision: transcription binding

> **STATUS: DRAFT — clerk-drafted 2026-08-12, UNSIGNED.** All seven
> registered criteria are now scored, including criterion 6 on the
> author's 2026-08-09 read (ratified at `15a26dd`). The author review
> produced findings that **narrow what this spike decides**: the
> transcription-binding *family* is selected; the digest-versus-direct-
> tuple form within it is **not** decided here and is disposed
> explicitly below. Two documentation defects in the model files are
> listed as remediation and are not blockers to signature.

Committed per the DECISION.md pattern registered in
`formal/spike/first-link/PREDICTIONS.md` §"Mechanism selection":
criteria fixed before evidence, scoring on record, rejected
alternatives named.

## Proposed decision

**Transcription binding** — authority evidence commits to the exact
map-v1 authority-relevant tuple — is the first-link mechanism
discharging the §A3.2.1 boundary invariant.

**Explicitly NOT decided here:** whether that commitment is to the
tuple directly (`sign((STMT, t), k)`, the Q1 form) or to its digest
(`sign((STMT, h(t)), k)`, the Q3 form). See §"Undischarged: digest
versus direct tuple".

Candidates rejected: digest publication, authorized tuple, separately
hashed manifest core, and strengthened variants (see §"Rejected
alternatives").

## How the decision was made (division of labor, honestly)

The spike ran per its frozen pre-registration: Q1–Q4 across two
channel-compromise variants, plus Addendum 1's Q5–Q8 single-evidence
coverage. Predictions were registered before every run, including the
overall selection prediction (p ≈ 0.5 for transcription binding
surviving Q4 in both variants). Scoring below was performed by the AI
collaborator (Claude) against criteria the author registered before
any evidence existed.

The author read the correct models on 2026-08-09, asked questions,
requested changes that were made, and ratified at commit `15a26dd`
("Initial run results, revisions based upon those results, and an
addendum to the predictions. Author ratified."). His written
assessment was recorded 2026-08-12 and is reproduced verbatim in
§"Author review". **That review changed this document**: findings 3
and 7 below are not readability observations, and they narrowed the
scope of what the spike is claimed to have decided. The AI-drafted
scoring did not catch either. Recorded because the division of labor
is only meaningful if its failures are visible.

Candidates 2–5 were not modeled. This is per registration: modeling an
alternative was required only on a Q4 failure, which did not occur.
Their comparison below is therefore criteria-level, not evidential —
recorded as such rather than dressed as a bake-off.

## Criterion 0 — the gate (discharged, for the family)

> Satisfies the §A3.2.1 boundary invariant under Q4-style attack in
> both channel variants. A candidate failing this is ineligible; no
> other virtue compensates.

Discharged on all three legs, within the checked symbolic abstraction:

1. **Strict Q4, both variants** — `TwoWorldsBroken` unreachable against
   the intact mechanism under DNS-compromise and repo-compromise
   (`q4_attack_*.out`).
2. **Q6, both channels × both compromise states** — unreachable ×4.
   Per ledger addendum entry 6 this result is *unconditional*: it does
   not depend on the A1.3 "never all" assumption. The boundary
   invariant holds per-object even under full compromise of the
   accepted channel.
3. **Q7/Q8 contrasts** — fired as designed.

The gate's negative control is genuine: Q2's broken companion produced
a real two-worlds attack (one evidence pair supporting two tuples
differing in **key fingerprint**, a frozen-map-v1 authority-relevant
field), judged against map v1 as frozen. The Grok panel criterion is
satisfied; no amendment trigger fired.

**Scope narrowing (author finding 3).** Because `h` is a free
constructor and therefore injective in the symbolic model, the gate is
discharged identically for both the direct-tuple and digest forms. It
does not select between them.

## Scoring against criteria 1–6

**1. No manifest/evidence self-reference — PASS (by construction).**
Transcription binding has the evidence carry the authority tuple (or
its digest) directly rather than referencing a manifest digest, so the
circularity that forced the §A3.2.1 override cannot arise. Scored from
the model construction; no query was registered against it.

**2. Exact correspondence with frozen map v1 — PASS (evidential).**
Map v1 survived every run unchanged — no divergence record was
required. The Q2 companion's mutation (binding issuer identity only) is
a proper subset of map v1, and the resulting attack turned on a
map-v1 authority-relevant field. Correspondence was exercised in both
directions: the intact mechanism binds the mapped fields, and weakening
the binding below the map is what breaks it.

*Qualification (author finding, "bound but not semantically
validated"):* the tuple's fields are **bound**, not **validated**. Only
the key fingerprint is compared against the accepted key; `issuerId`,
`sset`, `alg`, and `ver` are carried through the binding without any
policy check. Correspondence with map v1 is a binding claim only. The
q1 header's phrase "same issuer identity and required-key relation"
overclaims this and is listed for remediation.

**3. Sound under each single-channel compromise, both channels —
PASS (evidential), with the encoding qualified.** Every ladder query
ran in both variants with identical outcomes; Addendum 1 extended
coverage to the single-evidence acceptance path the pair-judge encoding
did not reach.

*Qualification (author finding 7):* the models leak one specific
channel key per variant. For n = 2 authority channels this **is**
exhaustive over strict subsets — {}, {DNS}, {repo} — so the A1.3
adversary is covered by enumeration. But it is instantiated, not
quantified: nothing in the models states the general claim, and the
enumeration does not survive the addition of further authority
publication branches. Capstone ledger entry 1's phrase "the adversary
controls any strict subset" overclaims what is encoded and is listed
for correction below.

**4. Evidence independently reconstructable from the preserved bundle
— PASS, WEAKLY (not query-discharged).** No registered query tests
reconstructability; the criterion is satisfied by construction —
transcription places the authority content in the evidence, so a
preserved bundle carries what a verifier needs without an external
lookup. Recorded honestly as a construction-level judgment. If Band 1
introduces a bundle-size budget that pushes transcribed content behind
a content-addressed reference (band-1 docket item 9), this criterion
must be re-scored, because the reference reintroduces the external
dependency the criterion exists to forbid. **This criterion is also
where the digest/direct-tuple fork bites** — see below.

**5. Compatible with standing evidence and A2.4's exactly-one-shipped-
anchor rule — PASS (ruled 2026-08-12).** Transcription binding operates
on the first link (evidence → authority tuple); A2.4's residue is a
lineage question (which of two valid receipts has standing). The two
are orthogonal, and the alone-case is answered by §A3.7.1 without
amendment. Carries one obligation onto the standing mechanism:
reason-carrying output. See §"Standing / A2.4".

**6. Author readability and conformance-test clarity — PASS WITH
FINDINGS (author).** Author's assessment, read 2026-08-09, ratified at
`15a26dd`, recorded 2026-08-12: *"The readability is mixed. The primary
issue is that the prose disagrees with the code."* Full review
reproduced verbatim in §"Author review"; remediation items listed in
§"Remediation". The author's requested changes during the 2026-08-09
read were made before that commit, so they do not appear as a diff —
the ratification, not a diff, is the record of them.

## Undischarged: digest versus direct tuple (author finding 3)

**The finding.** `h` is declared `fun h(bitstring): bitstring` — a free
constructor with no equations — and is therefore injective in the
symbolic model. Consequently `h(t) = h(t′) ⟺ t = t′`, and Q3 is
isomorphic to Q1. **Q3 demonstrates no property Q1 does not.**

**What follows.** The instrument cannot distinguish the two forms in
either direction. It cannot exhibit the digest form's benefits, which
are operational rather than security-theoretic (bundle compactness,
non-disclosure of the tuple), and it cannot exhibit the digest form's
risks, which it assumes away: serialization and encoding ambiguity,
concrete collisions, and distinct encodings producing one digest.

**The dependency nobody recorded.** Those assumed-away risks are
exactly **P8** (canonicalization injectivity + framing), which is
`open` in `formal/PROPERTIES.md`. The digest form's real-world
soundness is therefore conditional on an undischarged property; the
direct-tuple form is not. No capstone-ledger entry records this. It
should.

**History.** This is the digest-versus-tuple fork flagged as a blocking
decision on 2026-08-07. It was not resolved by this spike and could not
have been — the abstraction that makes the models tractable is the same
abstraction that erases the distinction.

**Disposition options (author's ruling required; not ruled here):**

- **(i) Direct tuple.** Select what Q1 actually proved. Avoids the P8
  dependency entirely. Cost: bundles carry full authority tuples,
  which pushes against band-1 docket item 9's size budget.
- **(ii) Digest.** Take the compactness and non-disclosure benefits,
  with a capstone-ledger entry making the mechanism's soundness
  explicitly conditional on P8, and P8 sequenced before any Band 1
  envelope freeze.
- **(iii) Defer to Band 1** with the fork named and both forms held
  open. Weakest option: the format freeze is the irreversible moment,
  so deferring past it decides by default.
- **(iv) RECOMMENDED — domain-separate the forms; register one as
  legal now.** See below. Dominates (i)–(iii): it removes the
  irreversibility without taking on the P8 dependency today.

### (iv) Domain separation, with a single legal form registered

**The observation that makes this possible (author, 2026-08-12).**
Anything outside the envelope is unattested testimony; the binding
form must therefore be inside the signed bytes. It currently is not.
`q1` emits `sign((STMT, t), skD)` and `q3` emits
`sign((STMT, h(t)), skD)` — **the same domain-separation tag**. The
file headers list three tags (`STMT`, `POSS`, `BYTES`) separating
authority evidence from possession from framed bytes; none separates
the two binding forms. Within a single-form deployment this is
harmless and the spike never needed it. The moment both forms are
legal, the signed bytes stop saying which form they are.

**The construction.** Distinct tags per form — `STMT_DIRECT` versus
`STMT_DIGEST` — making the two forms cryptographically
non-interchangeable. A digest binding cannot be read as a direct one
because the tag will not match.

**Why this is not a map v1 change.** The binding form is carried by
the domain-separation tag, not by an authority-relevant field, so map
v1 is untouched and the frozen-map divergence rule does not fire. *This
is a derived conclusion, not a verified one:* the map-freeze rule was
written before binding-form tags were at issue, and reading it the
other way reinstates the fresh-companion and Q2 re-run cost. Flagged
for the author rather than assumed.

**What domain separation does NOT close.** It closes *confusion*, not
*downgrade*. If both forms are legal, an adversary presents whichever
carries the weaker dependency and the deployment inherits the minimum.
Legality is therefore a policy and trust-configuration question,
separate from the cryptographic one:

> **Register the direct-tuple form as the sole legal form now, with the
> tag namespace reserved.** A second form may be added later without
> ambiguity, because the tag distinguishing it already exists.

This is the extensibility asymmetry applied one layer down: what must
be decided before the envelope freeze is *that the form is
distinguished in the signed bytes*; which forms are legal is freely
revisable afterwards. Selecting direct-tuple now also avoids taking on
the P8 dependency at all until measurement justifies it.

**A collapse worth noting.** Without domain separation, the
form-confusion risk is itself a P8 question — whether `h(t)` can be
parsed as a well-formed tuple is encoding ambiguity, the same property
the digest form already depends on. Domain separation separates the two
risks; absent it they are one risk.

**Not a defect in the spike.** Each model implements exactly one form,
so no model is wrong. This is a design requirement for implementation
that the spike had no occasion to encode, recorded here so it is not
discovered at the envelope freeze.

## Author review (verbatim, as written 2026-08-12)

Reproduced without edit, including typographical errors, per the
amend-do-not-rewrite discipline.

> The readability is mixed.  the primary issue is that the prose disagrees
> with the code; this could be due to different ontologies across the cases.
>
> Example (Q1): Q1 DNS lines 9-18 (line 9) and the verifier checks both signatures (line 88)
> but the query says || (or) on the query (line 61).
>
> While intentional, this is not clear and could be confusing to a future reader.
>
> For Q3, the model implicitly assumes an ideal injective hash.  It does not model
> serialization or encoding ambiguity, concrete hash collisions, or differing
> encodings generating the same digest.  The comments acknowledge this residual
> assumption, but Q3's result should be explicit about this to avoid confusion.
>
> Since Q1 already signs the tupe $t$, Q3's query isn't demonstrating a stronger
> property than Q1. If the claim hashing has benefit is to be made, it will
> need to live elsewhere, since it isn't here.
>
> The model doesn't prove that issuerId is independently valid; sst, alg, and/or
> ver satisfy policy; or the tuple corresponds to an independently supplied manifest.
>
> Since this is a binding/provenance model, the boundary needs to be clearly identified.
>
> The fields id, ss, alg, and ver are bound but not semantically validated.  Only kfpr is used in
> a comparison with the relevant key.  That's fine but the comment overclaims by saying
> the "same issuer identity and required-key relation" which suggests a strong guarantee
> than what the model itself checks.
>
> The six-node chain is not evidend from the ProVerif since it only declares five kinds of
> event. The text could be better described as a five-event model with two authority
> publication branches. [Note: this ties into our discussion earlier today that this
> doesn't prohibit adding further authority publication branches.]
>
> The compromise assumption is seriousy restricted.  The files model one specific DNS
> compromise and one specific repository compromise by leaking one key (q1 DNS line 107,
> q1 repo line 107).  These do not formally encode the claim that this encodes an
> adversarial instance where it controls _any_ strict subset.
>
> Suggestion for future improvement: add a plain-language statement in front of
> each query that says "This model proves..."

## Remediation (documentation defects; not blockers to signature)

Verified against the files 2026-08-12. All are prose-versus-code
mismatches in the model headers or the ledger; none is a model defect,
and none changes a run result.

1. **Q1 header conflates evidence with publication.** The verifier
   requires *both* channels' evidence to bind the tuple (q1 line 88);
   the query concludes a *disjunction* over publication events (q1
   line 61). Both are correct and they are about different objects —
   the 2026-08-09 recut made the publication conclusion disjunctive
   because a compromised channel's publication is forgeable-around.
   The header does not distinguish them. Fix the header, not the model.
2. **"Same issuer identity and required-key relation" overclaims.**
   Only the fingerprint is compared. Restate as a binding claim.
3. **"Six-node chain" versus five declared events.** Adopt the
   author's phrasing: a five-event model with two authority
   publication branches.
4. **Capstone ledger entry 1 overclaims the adversary.** Replace "the
   adversary controls any strict subset" with the exhaustive-by-
   enumeration statement for n = 2, and note that it does not
   generalize to additional authority branches.
5. **Adopt the author's suggestion:** a plain-language "This model
   proves…" statement at the head of every query, and for Q3 an
   explicit statement of what the injective-`h` idealization removes.

## Standing / A2.4 (registered exit condition 1)

The registration requires this document to state how
abandoned-artifact-alone standing evaluation coexists with A2.4's
exactly-one-shipped-anchor rule for the selected mechanism — and, if
they cannot coexist, to name which registered statement requires
amendment **before implementation**.

**What the record already says.** A2.4 confines standing —
cryptographically valid, evidentially admissible, *no protocol
standing* — but, per Amendment 2's own 2026-07-21 correction, it does
**not** deduplicate content. The residue A2 explicitly leaves open is
two verifiable receipts for the same content with different declared
times; closure by a lineage/equivocation-evidence mechanism or an
explicit dedup rule is registered as an Amendment 3 obligation.
§A3.7.1 then holds that no artifact lacking terminal-disposition
evidence can claim protocol standing.

**What this spike contributes.** Transcription binding does not close
that residue and does not need to: it operates on the first link
(evidence → authority tuple), while the residue is a lineage question
(which of two valid receipts has standing). The mechanism is
*orthogonal* to A2.4 rather than in tension with it — but orthogonality
is only adequate if the alone-case is answerable.

**RULED 2026-08-12 (author): no amendment required; §A3.7.1 stands.**

For an abandoned artifact presented alone, terminal-disposition
evidence is by definition absent, and §A3.7.1 already answers the
case: the artifact has no protocol standing. An abandoned artifact is
not certified by the attestation service. Nothing prevents a client
from accepting it on its own judgment, but Tessera must not claim an
affirmative standing signal it did not issue. No registered statement
requires amendment.

**Drafting correction, recorded because it caused the confusion.** An
earlier draft posed the alternative as whether the alone-case "demands
an affirmative standing signal." That framing was wrong and no one
holds that position. The registered concern (Kimi 1 / Grok 3, carried
into this spike's exit criteria) is **testability**, not entitlement: a
standing test whose answer is unconditionally "no" regardless of input
is not a test, and vacuity is a failure mode this record checks for
everywhere else.

**The correct statement of the concern, and its resolution.** The
alone-case is the *only* case in which the standing test performs
work — where lineage context is present, a verifier can simply look.
So the mechanism's discriminating power lives entirely in the case
whose verdict is always negative. Resolution: **the verdict is always
"no protocol standing," and the test MUST emit the reason.** These are
distinct facts about a holder's situation and must not collapse into
one output:

- no standing because *no lineage context was presented* (the
  alone-case), versus
- no standing because *lineage was presented and this artifact was
  superseded*.

**Who is injured if they collapse.** A relying party holding a
chain-valid but discarded receipt — precisely A2's open residue. That
holder would be unable to distinguish "you did not show me enough"
from "this one lost." Structurally the same defect as an unqualified
`VALID` that does not carry what it failed to check.

**Obligation this places on the standing mechanism:** reason-carrying
output is a conformance requirement, not a rendering nicety. It
belongs with the §A3.9 obligation that standalone protocol-standing
evidence be reported orthogonally to the P4 verdict and tested on an
abandoned artifact presented alone.

## What a verifier holding only the abandoned artifact can and cannot establish (registered exit condition 2)

- **CAN establish, unconditionally:** the boundary invariant — that
  this evidence supports exactly one authority tuple. Per ledger
  addendum entry 6, Q6's unreachability holds even under full
  compromise of the accepted channel and does not rest on A1.3's
  "never all."
- **CANNOT establish without an honesty assumption:** provenance —
  that an honest channel published this tuple. Q5 requires "the
  accepted channel is honest"; under compromise it goes red exactly as
  registered, with the waiver cost machine-documented.

Stated for the relying-party story: **the mechanism owes the
statement's uniqueness unconditionally, and owes its provenance only
under the honesty assumption.** Per Finding 1's recut, the two-channel
strict rule guarantees *at least one uncompromised channel published
this exact authority tuple* — a disjunctive, variant-independent claim.
Presented evidence artifacts are not individually
provenance-guaranteed; the *statement* is.

## Standing test conditions (registered exit condition 3)

Registered 2026-08-12, in both forms. Per the DeepSeek panel
criterion, **every** standing / dead-project test records whether the
artifact was presented with or without lineage context; the
lineage-absent case is mandatory and is the hard case.

| # | Form | Presented with lineage? | Standing verdict | Required reason code |
|---|------|--------------------------|------------------|----------------------|
| S1 | Lineage-present, artifact **is** the shipped anchor | yes | **standing** | `TERMINAL_DISPOSITION_SHOWN` |
| S2 | Lineage-present, artifact **superseded** by the shipped anchor | yes | **no standing** | `SUPERSEDED` |
| S3 | Lineage-absent — abandoned artifact presented **alone** | no | **no standing** | `NO_TERMINAL_DISPOSITION_EVIDENCE` |

**The discriminating requirement.** S2 and S3 both return "no standing"
and MUST return *different* reason codes. A standing mechanism that
collapses them is vacuous in exactly the way the panel criterion
warned about.

**Negative control.** A broken companion in which S2 and S3 emit the
same reason code MUST fail the discrimination check. If it passes, the
check is not testing what it claims.

**Orthogonality condition (A3 §A3.9; band-1 docket item 16).** All
three conditions are evaluated with the standing result reported
*orthogonally to the P4 verdict*. S3 in particular must leave an old
bundle's `VALID_STRICT` unaffected while the standing report is
negative and any custodial-record check reports `UNVERIFIABLE`.

## Rejected alternatives (criteria-level, not evidential)

- **Digest publication** (A3.2.1 docketed option). Deferred, not
  rejected, by the §A3.2.1 override. Fails criterion 4 in the form the
  override was written to escape: a digest requires the referent to be
  independently obtainable, reintroducing the external dependency.
  **Note:** distinct from the Q3 digest *binding* form, where the
  tuple travels in the bundle and only the commitment is hashed.
- **Authorized tuple** (the other docketed option). Not distinguishable
  from transcription binding on criteria 0–4 without modeling; not
  modeled, because no Q4 failure required it. **Open question raised
  by author finding 3:** since what Q1 actually proved is direct tuple
  signing, the distance between "authorized tuple" and the selected
  family may be smaller than this rejection implies. Resolving it
  requires the candidate definitions, which are not restated in
  PREDICTIONS.md at sufficient precision. Flagged, not resolved.
- **Separately hashed manifest core.** Adds a second object and a
  second binding to audit, against criterion 6, with no criterion-0
  advantage exhibited.
- **Strengthened variants.** The registered p ≈ 0.2 branch (a
  strengthened variant after a Q4 attack) did not fire; Q4 produced no
  attack in either variant, so no strengthening was indicated.

## Explicitly NOT criteria

Following the tool-spike discipline: proof speed, whether the property
verified (the negative controls fired, so no tool-shopping signal
exists), and ecosystem popularity.

## Consequences if signed

- Transcription binding is the §A3.2.1 first-link mechanism; changing
  it later requires a signed amendment naming the blocker.
- The digest/direct-tuple form remains open and must be ruled before
  any Band 1 envelope format freeze.
- If the digest form is selected, P8 acquires a dependent and must be
  sequenced before that freeze.
- Band-1 docket item 9 (bundle-size budget) interacts with both: it
  pushes toward the digest form and against criterion 4.
- The Kimi-2 integrated adversarial lifecycle model (A3 §A3.9) is
  triggered on this spike's completion and is mandatory before the H1a
  crypto-core freeze.
- The unconditional/conditional split above is the input the
  relying-party story has been missing (Sol's 2026-07-28 findings).

## What remains before this document can be signed

1. ~~Author cold read; criterion 6 scored.~~ **DONE** — read
   2026-08-09, ratified `15a26dd`, assessment recorded 2026-08-12.
2. ~~Author's ruling on the standing/A2.4 fork.~~ **DONE 2026-08-12:**
   §A3.7.1 stands, no amendment; reason-carrying output required.
3. ~~Standing test conditions in both forms.~~ **DONE** — S1–S3 above.
4. **OPEN — author's ruling on the digest/direct-tuple disposition.**
   Recommended: **(iv)** — domain-separate the binding forms in the
   signed bytes, register direct-tuple as the sole legal form now,
   reserve the tag namespace. Two sub-rulings ride on it: (a) whether
   a tag change escapes the frozen-map divergence rule (drafter says
   yes, derived not verified — if no, budget a fresh companion and a
   Q2 re-run); and (b) confirmation that domain separation becomes a
   registered requirement rather than an implementation note, since
   nothing else forces it before the envelope freeze.

Remediation items 1–5 are documentation fixes to the model headers and
ledger; they may be done before or after signature, but not silently.
