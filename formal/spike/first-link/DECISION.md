# First-link mechanism decision: transcription binding — DECIDED

> **STATUS: DECIDED.** The author's decision was entered 2026-08-13 at
> commit `459aff0` ("Author decision entered in favor of these changes
> (after many adversarial rounds and detailed reviews.)"), OpenTimestamps-
> stamped and anchored. That commit discharges item 5 of §"What remains
> before this document can be signed" — the author's verification that
> the 2026-08-12 rulings and the five remediation items were incorporated
> faithfully. No item remains open.

> **Header correction, 2026-08-13 — recorded, not silently applied.**
> The status block below read `DRAFT … UNSIGNED` at the time of
> `459aff0` and remained so afterward: the document said it was unsigned
> while its own commit entered the decision. The staleness was not
> surfaced to the author until after that commit had been made. He
> confirmed in session that the header was stale and that the commit
> message is the ratification — **RULED (author)**, his words: "stale
> header that wasn't mentioned to me until *after* the commit was done."
>
> The discrepancy is written down rather than quietly repaired, for the
> same reason §"How the decision was made" records its own failures: in
> a document whose credibility rests on labels tracking provenance
> exactly, a status label contradicting its commit is an instance of the
> defect class this record exists to catch, not an untidiness. The
> failure to report it before the commit was the AI collaborator's.
>
> **The stale block is retained verbatim below as history.** It is no
> longer the status of this document.

> *(Draft status block as it stood at `459aff0`, retained verbatim:)*
>
> **STATUS: DRAFT — clerk-drafted 2026-08-12, UNSIGNED; author rulings
> incorporated for review 2026-08-12.** All seven registered criteria
> are now scored, including criterion 6 on the author's 2026-08-09 read
> (ratified at `15a26dd`). The author review produced findings that
> **narrow what this spike decides**: the transcription-binding family
> is selected, while the envelope permits more than one authenticated
> binding form. The author ruled on that form boundary and the five
> documentation remediations in dialogue on 2026-08-12; the
> required-set ruling followed on 2026-08-13 after a Claude / ChatGPT
> cross-review. **A second cross-review on 2026-08-13 found that
> drafted recommendations had been recorded with the grammar of author
> decisions.** Provenance labels were added in response (see below),
> the binding-form lifecycle material was demoted to `RECOMMENDED —
> NOT ADOPTED` and withdrawn from consequences. The author then ruled
> that material **deferred** on 2026-08-13 — plan retained, nothing
> implemented, tracked as band-1 docket item 18 — which also moots the
> custody fork. **One item remains open: the author's verification
> that all rulings and remediations were incorporated faithfully.**
> Until that read, this document remains `DRAFT` and unsigned.

Committed per the DECISION.md pattern registered in
`formal/spike/first-link/PREDICTIONS.md` §"Mechanism selection":
criteria fixed before evidence, scoring on record, rejected
alternatives named.

## Provenance labels used in this document

Added 2026-08-13 after a cross-review finding that drafted
recommendations had acquired the grammar of author decisions. Every
load-bearing statement below carries exactly one label:

- **RULED (author)** — the author stated the decision himself, in his
  own words, with his own reasons. Ratification is his.
- **ADOPTED (author)** — the author endorsed a recommendation put to
  him. Binding, but the reasoning originated elsewhere and the
  endorsement is what makes it his.
- **RECOMMENDED** — drafted and reviewed, **not adopted**. Carries no
  authority and may not be propagated into consequences.
- **PROPOSED** — drafted and contested, or drafted and untested.

Absence of a label means unlabelled draft prose, not implicit
adoption. Apparent convergence between reviewers is not ratification;
this distinction is the credibility line, and the failure that
prompted these labels was mine.

## Proposed decision

**Transcription binding** is the first-link mechanism discharging the
§A3.2.1 boundary invariant: authority evidence commits to the exact
versioned map-v1 authority-relevant statement through one or more
authenticated, domain-separated binding forms declared inside the
signed envelope.

The direct form commits to the canonical authority-statement
representation; the digest form commits to a declared digest of that
same representation. Both are permitted protocol forms. An envelope
carries a **signed, nonempty required set** of binding-form
identifiers, and a verifier must validate **every** member of that
set — partial success is not success. The full rule, its verdict
mapping, and its precedence are in §"Binding-form disposition".

Candidates rejected: digest publication, separately hashed manifest
core, and strengthened variants. **"Authorized tuple" is deferred, not
rejected** — see §"Rejected alternatives", where the classification and
its non-blocking status are recorded.

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
dependency the criterion exists to forbid unless the exact referenced
representation remains obtainable — an obligation with no owner until
band-1 docket item 17 is answered, and one that "obtainable" was
quietly carrying. Both binding forms commit to the same
representation; digest binding additionally depends on the declared
concrete hash assumptions. See below.

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

## Binding-form disposition (author ruling 2026-08-12)

**The finding.** `h` is declared `fun h(bitstring): bitstring` — a free
constructor with no equations — and is therefore injective in the
symbolic model. Consequently `h(t) = h(t′) ⟺ t = t′`, and Q3 is
isomorphic to Q1. **Q3 demonstrates no property Q1 does not.**

**What follows.** The instrument cannot distinguish the two forms in
either direction. It cannot exhibit their operational differences,
and its term algebra supplies injective construction for both the tuple
and `h`. P8 must supply an unambiguous canonical byte representation
for **both** forms in the implementation. Digest binding additionally
depends on the declared concrete hash algorithm's collision and
second-preimage resistance; the free symbolic constructor does not
discharge that Layer 2 assumption.

Tessera records the representation version, binding form, hash
algorithm where applicable, and the guarantees claimed at issuance.
It supports algorithm agility but does not promise that an issuance-
time assumption remains adequate forever. Future examining parties
decide whether the preserved evidence remains adequate under their
own policies and stakes. Tessera minimizes dependence on its continued
operation, goodwill, or existence; it does not promise perpetual
availability, cryptographic adequacy, or acceptance.

**History.** This was the digest-versus-tuple fork flagged as a
blocking decision on 2026-08-07. It could not be resolved by the
queries alone — the abstraction that makes the models tractable is the
same abstraction that erases the operational distinction. The author
considered four dispositions:

- **(i) Direct tuple.** Select only Q1's form. Smaller proof surface,
  but freezes out a future compact or non-disclosing commitment form.
- **(ii) Digest.** Take the compactness and non-disclosure benefits,
  add the declared concrete hash dependency to the capstone ledger,
  and sequence P8 before any Band 1 envelope freeze.
- **(iii) Defer to Band 1** with the fork named and both forms held
  open. Weakest option: the format freeze would decide by default.
- **(iv) Domain-separate authenticated forms inside the envelope.**
  Selected, with the author's correction that the protocol permits
  both rather than registering only one legal form now.

### Selected: authenticated, domain-separated forms

**The observation that makes this possible (author, 2026-08-12).**
Anything fixed at attestation time and later used to interpret,
verify, scope, or evaluate the attestation must be authenticated inside
the envelope; outside statements are fungible testimony. The artifact-
derived attestation handle is the narrow exception because its linkage
is inherent. The binding form therefore belongs inside the signed
bytes. It currently is not.
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

**Map v1 ruling.** Binding-form tags are authenticated verification
semantics, not authority-relevant identity fields. Distinct tags do
not change map v1 and do not trigger its divergence rule or a Q2 rerun.
Cross-form substitution is a separate P7/P8 obligation and must carry
a negative control before more than one form is implemented.

### Verifier boundary — the required-set ruling

**ADOPTED 2026-08-13 (author), resolving the singular-versus-set
defect.** Converged across a Claude / ChatGPT cross-review and put to
the author, who adopted it ("there's convergence, the ayllu has
decided"). Labelled ADOPTED rather than RULED because the reasoning
originated in the cross-review, not with the author; the endorsement is
what makes it binding. The disagreement is recorded alongside the
outcome because that is what makes the adoption defensible.

> An envelope carries a signed, nonempty required set of binding-form
> identifiers. A verifier must successfully validate every required
> form; partial success is not success. A well-formed identifier that
> is unknown to the verifier, or known but unsupported, makes the
> binding assessment `UNVERIFIABLE` with an appropriate reason. A
> missing, malformed, duplicate, substituted, or inconsistently
> encoded member — or an empty required set — makes it `INVALID`. P8
> defines the set's canonical encoding, ordering, uniqueness, and
> bounds. No inference, negotiation, normalization, or fallback is
> permitted during verification.

**Precedence.** `INVALID` dominates `UNVERIFIABLE`. Where a required
set contains both an unknown identifier and a malformed member, the
verdict is `INVALID`: a provable defect settles the artifact
regardless of what else cannot be evaluated, it is fail-closed in the
direction P4 already establishes, and without the rule two conforming
implementations can disagree on the same input — which conformance
vectors would then be unable to pin.

**Distinct reason codes for the two `UNVERIFIABLE` cases.** *Unknown
identifier* and *known but unsupported* must not share a reason code.
The difference is evidence a future examiner may need — the first says
the artifact uses something this verifier has never heard of, the
second that the verifier chose not to implement a form it knows.

**Why unknown identifiers are `UNVERIFIABLE` and not `INVALID`.**
Otherwise a verifier built in 2026 declares every envelope using a
form registered in 2030 invalid — a false negative against a sound
artifact, which is the failure `UNVERIFIABLE` exists to prevent.
Unknown-to-me is not the same fact as malformed. This is the
extensibility asymmetry: what forms exist is revisable, what the
envelope can express is not.

**Why P8 must own the set's encoding.** Not signature malleability —
the signature binds particular bytes, and no re-encoding verifies
against an old signature. The failure is **semantic identity and
interoperability**: two byte-distinct envelopes may carry the same
abstract required set, both validly signed. (An earlier draft called
this a manufacturing mechanism for A2's equivocation residue. That
borrowed a stronger threat label than the evidence supports — A2's
residue turns on receipts with *different declared times*, and encoding
ambiguity does not by itself produce contradictory authority
statements.) The harm that is established: artifact identity becomes
unreliable, and the standing tests S1–S3 turn on identifying *which*
artifact is the shipped anchor. Canonical encoding, ordering,
uniqueness, and bounds forecloses it.

**Cost, stated plainly.** `{direct, digest}` requires both and is
therefore *not* a compact substitute for `{digest}` — it is an
explicitly stronger and larger construction. The three legal
configurations each carry a legible price: `{direct}` takes no
*additional binding-form* hash assumption — the artifact still uses
hashes and fingerprints elsewhere — `{digest}` takes the additional
collision and second-preimage assumption in exchange for compactness,
and `{direct, digest}` takes both forms' guarantees and both forms'
bytes.

Because the required set is itself signed, removing a member changes
the signed envelope rather than silently weakening it.

### Form lifecycle and the reference-verifier obligation

> **RULED 2026-08-13 (author): DEFERRED — plan retained, nothing
> implemented.** Author's reasoning, in his words: *"Every additional
> complication we add now increases the complexity of the baseline
> service. I like knowing we have plans for dealing with additional
> features moving forward — that's the architect within me — but
> implementing these early needs a real reason and I don't see that
> right now."* He has also stated he does not intend to retire a form
> in the foreseeable future.
>
> **Everything below is retained as the plan and implements nothing.**
> It carries no authority over the baseline service. Tracked as band-1
> docket item 18 so it cannot silently drop.
>
> **Why deferral is free rather than merely cheap** (checked, not
> assumed): the lifecycle is inert until a second binding form is
> actually implemented, which is separately gated on the P7/P8
> cross-form substitution negative control; and the extensibility
> asymmetry's trap does not apply,
> because legitimacy can ride the key chain — which must be preserved
> regardless — so **no envelope field is required under any live
> candidate.** Had one been required, deferral would have been
> irreversible and this ruling would be wrong.
>
> An earlier version of this document propagated this material into
> §"Consequences if signed" before any ruling existed. That
> propagation was withdrawn and the withdrawal recorded.

The permission to use two forms creates a fragmentation hazard that is
interoperability, not security: if implementations may each support a
different subset, a bundle exists that some verifiers cannot check.
For a design whose relying party is the product surface, that weakens
the year-ten story directly.

**Form states.** A binding form is in exactly one state:

- **registered** — identifier and semantics reserved; not permitted in
  any envelope. Reservation is what makes later addition unambiguous.
- **issuable** — permitted in the required set of new envelopes, after
  that form's prerequisites discharge (for more than one implemented
  form, the P7/P8 cross-form substitution negative control).
- **retired** — no longer permitted in new envelopes. Retirement
  forbids new issuance but preserves the form's specification,
  conformance vectors, registry history, and reference-verifier
  support for previously issued envelopes. **Retirement does not
  preserve the form's cryptographic adequacy or require a relying
  party to accept it** — a form may be retired precisely because its
  algorithm became unsafe, or because its implementation became unsafe
  to execute.

**Issuance validity is judged against issuance-time registry state.**
Whether a form was issuable is not intrinsic to the envelope. A
present-day verifier must not judge a 2028 artifact using 2035 registry
state.

> A required-set member that was not issuable under the authenticated
> registry version applicable at issuance makes the artifact `INVALID`.
> Subsequent retirement does not retroactively invalidate it.

**The registry epoch must be inside the envelope.** A verifier cannot
infer which registry version applied by comparing a timestamp against
registry history — inference is forbidden by the verifier boundary
above, and the same principle that puts the binding form inside the
signed bytes applies here: anything later used to interpret the
attestation must be authenticated within it. An envelope therefore
declares the registry version or policy epoch it was issued under. A
declared registry version the verifier does not hold is `UNVERIFIABLE`
with its own reason code — the verifier lacks the history, the artifact
is not defective. This creates a dependency on the versioned historical
trust/registry store of band-1 docket item 8, and makes that store a
custody subject — band-1 docket item 17.

**Declaration alone permits rollback (cross-review finding,
2026-08-13).** A declared epoch does not establish that the epoch was
*applicable*. An issuer — or anyone holding the signing key — could
emit a newly signed envelope using a **retired** form while declaring
an older epoch under which that form was still issuable, and a verifier
checking only the declaration would accept it. Retirement would then
be unenforceable, which is the whole point of retiring a form whose
algorithm became unsafe.

> The declared epoch MUST be checked for correspondence with the
> artifact's **independently established issuance interval**. If the
> declared epoch is inconsistent with that interval, or the form was
> not issuable under the epoch that actually applied, the artifact is
> `INVALID`. If the correspondence cannot be established at all, the
> result is `UNVERIFIABLE`.

**CORRECTED 2026-08-13 (cross-review).** An earlier draft claimed the
temporal anchor closes this, on the reasoning that "an artifact whose
anchor places it after epoch *E* closed cannot truthfully declare *E*."
**That is false.** OpenTimestamps establishes that an artifact existed
*no later than* the anchored time — an upper bound. An artifact
anchored after *E* closed may have existed earlier and been anchored
late, so a late anchor neither refutes nor corroborates an old
declaration. The anchor alone supplies the wrong bound.

**The lower bound exists already, and it is not the anchor.** A2.1,
adopted 2026-07-21 and modeled in `P5c_IssuanceProtocol.tla`,
`P5P6_TemporalRevocation.tla`, and the bridge, fixes one predicate for
issuer and verifier:

> `confirmed_at := timestamp(block h+k−1) ≤ declared + δ`

An artifact declaring an issuance time far earlier than its anchor
fails this predicate: with `declared` in a closed epoch and the block
timestamp long after, `timestamp > declared + δ` and the artifact is
already rejected under adopted semantics. **Backdating beyond δ is
therefore refused by machinery this document need not add.** The epoch
rule composes with it: the declared epoch must contain the declared
issuance time, and A2.1 pins the declared issuance time to within δ of
**the designated chain-time proxy**.

That proxy is not an exact clock, and this document must not imply it
is. A prior draft said "a chain time no forger can fabricate," which
overstates: what no forger can do is place bytes in a *past block*
(P5); the *timestamp* of a block carries latitude, which is why the
bridge model deliberately treats block timestamps as **skewed and
non-monotonic**, decoupled from the tick clock
(`formal/tla/P5cP5P6_Bridge.tla`). The epoch constraint therefore
inherits A2.1's registered timestamp-skew residuals rather than
standing on an exact bound.

**Named residual, stated rather than closed.** Backdating *within* δ
remains possible. A key holder anchoring at most δ after an epoch
closes can declare a time just inside it and use a form retired at that
boundary. The exposure is therefore **δ plus A2.1's skew residuals**,
not a sharp δ-wide wall — with the working default δ = 72h, "roughly
three days, widened by chain-timestamp latitude," not "exactly 72
hours." Closing it would require a trustworthy lower bound or an
ordered issuance record — genuinely new scope, and **not proposed
here**. The honest statement: retirement is enforceable against honest
issuers and against backdating beyond that window, and is not
enforceable against a compromised still-valid signing key operating
inside it.

Where the anchor's interval is itself unavailable, the epoch check
degrades to `UNVERIFIABLE` along with everything else depending on it.

**Reference-verifier support is append-only, at the shared binding
layer.** Every maintained reference-verifier tier must have access to
the maintained shared implementation of every form that has **ever**
been issuable. Retirement stops new issuance; it must not orphan
artifacts issued while the form was live. The obligation sits on the
shared binding layer rather than on each tier independently — the tiers
differ in evidentiary depth, not in binding-form parsing, and requiring
per-tier implementations would be an architectural commitment nothing
here motivates. Third-party verifiers remain free to implement a subset
and return `UNVERIFIABLE` with the known-but-unsupported reason code;
the reference implementation is the escape that keeps every artifact
checkable by someone.

**The invariant, narrowed so it is actually true and testable.** The
broad form — *Tessera never emits an envelope its reference verifier
cannot check* — is defeated by missing external evidence, unavailable
custody, or unsupported historical runtime dependencies, none of which
are binding-form properties. The binding-form invariant is:

> Tessera must never issue an envelope whose required binding-form set
> the maintained reference verifier cannot parse and evaluate when
> supplied the required evidence.

CI enforcement, required **before** a form becomes issuable:

- positive and negative vectors for each lifecycle state;
- vectors for every issuable individual form;
- multi-form required-set vectors before any multi-form issuance;
- cases for unknown, known-but-unsupported, duplicate, malformed,
  retired-at-issuance, and registered-but-not-issuable members;
- every maintained tier passing these through the shared binding layer.

A form transitioning to issuable without its vectors is a build
failure, not a review finding.

Permitting both forms does not make a direct-form artifact inherit the
digest form's additional hash assumption: an adversary cannot change
the authenticated form without invalidating the signature. Relying-
party policy may nevertheless distinguish the evidentiary adequacy of
the forms, and the assessment reports which form and dependencies were
evaluated.

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

## Remediation (incorporated 2026-08-12; pending author verification)

Verified against the files 2026-08-12. All are prose-versus-code
mismatches in the model headers or the ledger; none is a model defect,
and none changes a run result. The corrections below were incorporated
after explicit author disposition; the author-review quotation above
remains verbatim.

1. **Q1 header conflates evidence with publication.** The verifier
   requires *both* channels' evidence to bind the tuple (q1 line 88);
   the query concludes a *disjunction* over publication events (q1
   line 61). Both are correct and they are about different objects —
   the 2026-08-09 recut made the publication conclusion disjunctive
   because a compromised channel's publication is forgeable-around.
   The header now distinguishes them: strict mode validates both
   evidence objects, while provenance under proper-subset compromise
   establishes that at least one uncompromised channel published the
   accepted statement.
2. **"Same issuer identity and required-key relation" overclaims.**
   Only the fingerprint is independently compared. The headers now
   state the binding claim and its semantic boundary.
3. **"Six-node chain" versus five declared events.** Adopt the
   author's phrasing: five event kinds with two authority-publication
   branches.
4. **Capstone ledger entry 1 overclaims the adversary.** Replace "the
   adversary controls any strict subset" with the exhaustive-by-
   enumeration statement for n = 2, and note that it does not
   generalize to additional authority branches. New channels or
   instances require reassessment; instance count alone does not prove
   compromise independence.
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
- **Authorized tuple** — **DEFERRED, NOT REJECTED** (reclassified
  2026-08-13; an earlier draft listed it as rejected while
  simultaneously describing it as an unresolved open question, which
  is a contradiction this section cannot carry). Not modeled, because
  no Q4 failure required it. Author finding 3 makes the classification
  live: since what Q1 actually proved is direct tuple signing, the
  distance between "authorized tuple" and the selected family may be
  smaller than a rejection implies — they may be the same construction
  under two names. Resolving it requires the candidate definitions,
  which PREDICTIONS.md does not restate at sufficient precision.
  **Classified non-blocking for signature:** criterion 0 is discharged
  for the selected family regardless of how this resolves, and
  registration required an alternative to be modeled only on a Q4
  failure, which did not occur. If it later resolves to "same
  construction," that is a naming correction, not a mechanism change.
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
- Direct and digest are permitted authenticated protocol forms. An
  envelope carries a signed, nonempty **required set** of form
  identifiers and a verifier must validate every member; partial
  success is not success. Every form has a distinct signed domain
  identifier, exact-form verification, and no inference, negotiation,
  normalization, or fallback. `INVALID` dominates `UNVERIFIABLE`;
  unknown and known-but-unsupported forms carry distinct reason codes.
- P8 additionally defines the required set's canonical encoding,
  ordering, uniqueness, and bounds — without which two byte-distinct
  envelopes can carry one abstract set, making artifact identity
  unreliable and undermining the standing tests, which turn on
  identifying which artifact is the shipped anchor.
- *(WITHDRAWN from consequences 2026-08-13.* The binding-form
  lifecycle, registry-epoch, append-only-support, and CI-gate material
  **was** `RECOMMENDED — NOT ADOPTED` when it was withdrawn from here,
  and was **subsequently ruled DEFERRED** the same day — plan retained,
  nothing implemented, tracked as band-1 docket item 18. Its current
  state is deferred, not merely unadopted; this paragraph is history.
  It remains drafted in §"Form lifecycle and the
  reference-verifier obligation". Recorded as a withdrawal rather than
  deleted, because the propagation happened and the record should show
  it.)
- P8 supplies the canonical encoding used by both forms. Digest binding
  additionally carries the declared concrete hash-resistance assumption.
- Map v1 is unchanged; form tags alone require no Q2 rerun. P7/P8 must
  carry a cross-form substitution negative control before more than one
  form is implemented.
- Band-1 docket item 9 (bundle-size budget) interacts with both: it
  may motivate digest binding, but content addressing must not make the
  exact committed representation unavailable to a future verifier —
  custody of that representation is band-1 docket item 17, which must
  be answered before any Band 1 freeze.
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
4. ~~Author's ruling on the digest/direct-tuple disposition and its two
   sub-rulings.~~ **DONE 2026-08-12:** both forms permitted with
   authenticated domain identifiers inside the envelope; map v1
   unchanged; no Q2 rerun for tags alone; exact-form verification with
   no fallback; cross-form substitution routed to P7/P8.
5. ~~Author verification that the 2026-08-12 rulings and all five
   remediation items were incorporated faithfully.~~ **DONE
   2026-08-13** — decision entered at `459aff0`, stamped and anchored.
   The status header was not updated at that commit and continued to
   read `DRAFT`/unsigned; corrected 2026-08-13 on the author's
   statement that the header was stale. See the header correction at
   the top of this document.
6. ~~Author ruling on §"Form lifecycle and the reference-verifier
   obligation".~~ **RULED 2026-08-13: DEFERRED.** Plan retained,
   nothing implemented; tracked as band-1 docket item 18. The δ-width
   rollback residual needs no acceptance, because nothing implements
   retirement.
7. ~~Selection between custody forks (A) and (B).~~ **MOOT under item
   6's deferral.** That fork asked whether a self-contained-tier
   verdict judges issuance-time binding-form validity. With **no form
   lifecycle or issuance-state distinction implemented**, there is no
   such judgment to make. It revives only if item 18 is taken up.

**Non-blocking, recorded so it is not mistaken for an oversight:** the
"authorized tuple" classification (deferred, not rejected) does not
gate signature — see §"Rejected alternatives" for why.
