# Standing-evidence mechanism decision — criteria and selection rule

> **STATUS: REGISTERED at `74ee46e` (2026-08-30, "Applied another
> round of edits to clarify the decision framework"), OTS-stamped
> `c207ed9`.** The author stated in session that this commit is the
> registration and that he had not read `RESULTS-PROBE.md` at the time
> of it; the commit message does not carry that affirmation in words,
> so it is recorded here, on the author's statement, the same day.
>
> **Header correction, same day, recorded not silently applied.** The
> status block below read `PROPOSED` at the registering commit — the
> same defect class the first-link decision recorded at `459aff0`. The
> stale block is retained verbatim beneath this note as history; it is
> no longer the status of this document. Changes from here on follow
> amend-don't-rewrite: appended, dated, labeled.

> *(Status block as it stood at `74ee46e`, retained verbatim:)*
>
> **Status: PROPOSED (drafted by the AI collaborator 2026-08-29; revised toward
> stand-alone 2026-08-30 on a series of blind external reviews). Becomes REGISTERED
> on the author's commit, which affirms that the author had not read
> `RESULTS-PROBE.md` at the time of registration.** Edit before
> committing; the registration is the commit, not this draft. The one
> wording decision the draft carried (R2) was ruled by the author on
> 2026-08-30 and is recorded in the body.

**Provenance, stated because it matters here.** The AI collaborator
that built and ran the probe (Claude) has read its results. The
reviewer that shaped this document's structure (Codex, 2026-08-29) had
not.

On 2026-08-30 the document was iteratively handed to three blind
reviewers.  The first blind reviewer was Grok, and its feedback
was incorporated into a committed update.  The second
blind reviewer was Gemini, and its feedback was also incorporated
into a separate committed update.  The third blind reviewer,
**a separate Claude instance** using a different framework,
blind to results and to this session's context, so its review is
a same-model check and weaker as an independence test than
the other two (A1.7's correlated-blind-spot concern), though it found
the transparency-witness G0 overclaim the other two missed — had not;
the author has not. Changes made and captured in a separate commit.
The structure follows Codex's blind draft. Claude's contributions
are: pinning terms to registered text; the glossary and restatements
below (from registered text only); the candidate sketches — of
which the terminal-lineage-record sketch is **copied from
`PROBE.md` §Fixture, frozen before the probe ran**, so
that a non-blind hand did not write it; and one flagged dissent (R2).

Drafting throughout was by Claude, the AI collaborator. Its
observations carry no authority; every load-bearing statement in this
file carries a provenance label under the DECISION.md scheme, and an
unlabeled sentence is draft prose, not an adopted position.

Pattern: `formal/spike/first-link/DECISION.md` — criteria fixed before
evidence, scoring on record, rejected alternatives named.

---

## What this document decides, in plain language

**Tessera** is an attestation service: a neutral third party binds a
package of bytes to a fixed point in time, so that a later reader can
check that *this* content was presented *then* — without needing
Tessera to still exist. It issues signed artifacts anchored to a
public chain; a verifier checks them offline from a bundle.

Because anchoring can be slow, Tessera may anchor the same content
more than once — abandoning an attempt its own clock judged late and
reissuing — and a later verifier can end up holding an artifact from
an abandoned attempt that is nonetheless cryptographically valid. The
record calls this the A2 residue. The question this document governs
is: **what evidence lets a verifier tell the artifact Tessera actually
designated from a valid one it abandoned, and how will Tessera choose
among the ways of supplying that evidence?** The choice is called the
standing-evidence mechanism. This file fixes the criteria and the
selection rule *before* the evidence from a design probe is read, so
that the choice cannot be fitted to the results after the fact.

---

## 0. Terms, restated so this file carries its own meaning

Citations remain the authority; the restatements exist so the gates
mean something if a citation target moves.

- **Artifact / bundle.** An issuance artifact is a signed attestation
  object (framed bytes, authority statement, issuer signatures, anchor
  reference). A bundle is the artifact plus everything a verifier needs
  to evaluate it offline: archived authority evidence, archived chain
  headers, and — if the candidate supplies one — standing evidence.
- **P4 verdict.** The envelope-verification result: `VALID_STRICT`,
  `VALID_DEGRADED` (only under an explicit recorded waiver), `INVALID`
  (a required check failed), `UNVERIFIABLE` (a check could not be
  performed). A1 §A1.2 P4. Standing is **not** a fifth state; it is
  reported beside the verdict and never alters it (A3 §A3.7.1).
- **Protocol standing.** Whether an artifact is the one Tessera
  actually designated for its content, as opposed to a
  cryptographically valid artifact from an attempt Tessera abandoned.
  Reported as `ESTABLISHED`, `ABSENT`, or `UNVERIFIABLE`, with a
  reason. A3 §A3.7.1: "Cryptographic validity alone confers no
  protocol standing."
- **Attempt lineage.** The sequence of issuance attempts for one
  content: each attempt anchored, then either buried in time (shipped),
  abandoned by the issuer (late by its clock; reissued), or refused
  after the attempt bound. A2 §A2.2–A2.4 confine standing to exactly
  one shipped anchor without deduplicating content — hence two valid
  artifacts can exist for one content (the A2 residue).
- **Terminal disposition.** The lineage's end state as declared by the
  issuer: which attempt shipped, or that issuance was refused.
- **The A2 residue (equivocation).** Because two cryptographically
  valid artifacts can exist for one content (above), and because the
  entitled key that declares which one shipped can sign more than one
  such declaration, a verifier holding one bundle may be unable to
  tell that a contradictory declaration exists. Amendment 2 left this
  open by design; A3 §A3.7.1 confines it without closing it. G4 asks
  each candidate to say precisely how much of this it leaves open.
- **Band 0 / Band 0 exit.** The project's formal-foundation phase: the
  central guarantees are established by machine-checked models before
  any code intended for the service is written (`docs/phase-0-prereg.md`;
  scope of "any code" clarified 2026-08-29, `634c2f2`). Band 0 exit is
  the signed commit that opens implementation; several obligations,
  including R1 below, must be discharged before it.
- **Issuance identity.** The identity of one attempt's artifact. G1
  fixes how it is obtained.
- **Standing evidence.** Whatever object the candidate supplies to let
  a verifier report standing. The invariant it must satisfy (A3
  §A3.7.1): *any artifact claiming standing must present verifiable
  standing evidence binding its issuance identity, attempt lineage,
  and terminal disposition; missing evidence leaves the artifact
  evidentially admissible but without protocol standing.*
- **Authority tuple / entitled key.** The authority statement the
  external channels publish (map v1: issuer identity, signing-key
  fingerprint(s), required-signer set, algorithm identifiers,
  statement version; *non-authoritative* and outside the binding:
  display labels, optional metadata no check consumes, ordering of
  equivalent entries — `formal/spike/first-link/PREDICTIONS.md`,
  frozen at `64c80c8`). The **entitled key** is the issuer key that tuple names — the same key
  whose signature the evidence chain accepts (A3 §A3.2 item 3) and
  which must prove possession by manifest self-signature (A1 §A1.5
  item 3, P10). This document assumes one entitled key per lineage;
  a candidate that needs more must say so under G0.
- **Adversary (A1 §A1.3).** Alters any bytes after issue; strips,
  reorders, duplicates signatures; substitutes keys, including after
  seeing valid signatures, and self-signs freely with keys it holds;
  replays valid objects in other contexts and re-frames across P7 type
  boundaries (P7, wrapper/object-type soundness: presenting a signed
  object of one kind — an inner attestation, a receipt, a wrapper — as
  if it were another, so that a signature made for one role is read in
  a different one); crafts manifests and anchors anything; controls
  any proper subset of the external authority channels, never all.
- **Trust configuration (A3 §A3.8).** What the verifier holds before
  seeing a bundle: channel public keys, the depth `k` and window `δ`,
  governing specification and policy. An input, not a fetch.
- **Survivability floor (A3 §A3.4).** For every artifact class,
  guarantees are limited to creation and observable protocol
  obligations, verifiable handoff when acknowledged, portable identity,
  and visible failure while an observer holding the relevant state
  survives; continued availability after handoff is conditional on
  custody. "Custody burden" in C2 means what some party must retain
  under that floor for the candidate's claims to keep holding.
- **The S-series.** Registered in the first-link `DECISION.md` under
  the heading *"Standing test conditions (registered exit condition
  3)"* — there, and not in a standing document, because resolving
  standing was an exit condition of the first-link spike; the
  executable form is `PROBE.md` Q2/Q4. Three standing test conditions
  with mandatory distinct reason codes: **S1** lineage present, artifact *is* the shipped
  anchor → standing, `TERMINAL_DISPOSITION_SHOWN`; **S2** lineage
  present, artifact *superseded* → no standing, `SUPERSEDED`; **S3**
  lineage absent, artifact presented alone → no standing,
  `NO_TERMINAL_DISPOSITION_EVIDENCE`. **The collapsing negative
  control, as a test:** build a verifier variant identical to the
  candidate's except that its S2 and S3 branches return the same
  reason code; run S2 and S3 through it; assert
  `reason(S2) ≠ reason(S3)`. On the variant that assertion must
  **fail**; on the correct verifier it must pass. A control on which
  the assertion passes is not testing what it claims.
- **Transplant (A3 §A3.9).** Moving standing evidence from a valid
  artifact onto a different one — the named broken companion for the
  suite's standing model, expected to go red.
- **Portable refusal record (A3 §A3.7.2).** Created atomically with a
  `REFUSED` terminal state: attempt identity, disposition, disclosable
  reasons, verification evidence, plus a non-identifying public
  commitment value; handed off to a custodian (the submitter by
  default).

---

## 1. Candidates

Per A3 §A3.7.1. Each is held to the same bar: evidence object, who
signs it, what the verifier computes, what it does *not* claim. A
candidate not specified to this bar before scoring is not a candidate.
Candidates are scored on their design, not on whether a probe
prototyped them.

**Forward reference.** Candidate sketches are subject to the gates in
§2. Where a gate fixes a term a sketch left open, the sketch is read
as amended by that gate, and the sketch says so at the point of
amendment — the TLR's issuance-identity form is the instance. Nothing
in a sketch is rewritten silently; a sketch that had to be changed
after registration carries a dated note, per amend-don't-rewrite.

**Terminal lineage record (TLR).** *(Sketch copied from `PROBE.md`
§Fixture, frozen 2026-08-29 before the probe ran; one clause
completed from G1, not from results.)* An issuer-signed object created
at terminal disposition, carrying at minimum: issuance identity — the
frozen sketch left its form to the probe; **for scoring, the form is
fixed by G1: a digest of the artifact's signed core, computed by the
verifier** — attempt lineage (attempt identities with anchor
references and per-attempt dispositions), and terminal disposition
(`SHIPPED <attempt>` or `REFUSED`). Signer: the entitled key. Verifier
computes: signature under the entitled key; whether the presented
artifact's identity appears in the lineage; whether it is the terminal
one. Does not claim: that the issuer has not signed a second,
contradictory record; anything about attempts absent from the lineage.
*G0 story:* the record itself is the standing object; it binds all
three of identity, lineage, and disposition under the entitled key.
*G4 sentence:* a verifier holding one bundle can establish that
**this** record, under the entitled key, binds **this** artifact and
names its disposition; it cannot establish that no second record
exists.

**Capability — a design-space alternative, expected to fail G0.**
*(Drafted by the AI collaborator 2026-08-30; reframed the same day on the author's
read; not prototyped.)* A single-purpose token signed by the entitled
key at terminal disposition, naming the designated artifact's identity
and disposition, issued **only** to the designated artifact and
carried with it. Signer: the entitled key. Verifier computes: token
signature; token identity equals the presented artifact's identity;
disposition. **By design it carries no lineage** — that is what
distinguishes it from a TLR; a capability that listed superseded
identities would be a TLR under another name. Consequently an
abandoned artifact holds no token, and the verifier cannot tell S2
(superseded) from S3 (presented alone): both are "no token present."

This is specified as a design-space alternative, not as a contender.
Because it omits lineage by design, it is **expected to fail G0**
(§2), which requires the attempt lineage to be bound, and G3, which
requires S2 and S3 to be distinguished. It is included to demonstrate
*why lineage binding is non-optional* — the failure is shown against a
fully specified construction rather than asserted — and to foreclose
the objection that an unspecified capability might have passed.
Scoring records the failure at the gate that catches it; no
comparative criterion is applied. Does not claim: anything about other
attempts; non-equivocation. *G0 story:* the token binds identity and
disposition under the entitled key and does not bind lineage; G0
requires all three. *G4 sentence:* a verifier holding one bundle can
establish that this token, under the entitled key, designates this
artifact; it cannot establish that no second token exists, nor that
any other attempt existed at all.

**Transparency witness.** *(Drafted by the AI collaborator 2026-08-30; not
prototyped.)* An append-only log, operated by Tessera or a third
party, records for each lineage an **entry** signed by the entitled
key carrying the same three things a TLR carries — the designated
artifact's identity, the attempt lineage (identities with
dispositions), and the terminal disposition — so that the entry *is* a
TLR published rather than merely carried; standing evidence is that
entry plus an inclusion proof (Merkle path, signed log head) carried
in the bundle. Signers: the entitled key (the entry) and the log (the
head). Verifier computes: the entry's signature under the entitled
key; whether the presented artifact's identity appears in the entry's
lineage and is its terminal one; the inclusion proof against a log
key or root in the trust configuration. *(Corrected 2026-08-30 on
blind review: an earlier sketch recorded only the terminal
disposition in the entry while the G0 story claimed lineage was
bound.)* Closes equivocation to
the extent the log is consistent — a contradictory second disposition
requires a second log entry, visible to anyone auditing the log — at
the price of a trusted, surviving log. Does not claim: log
availability or honesty beyond what the trust configuration asserts.
*G0 story:* the standing object is the **log entry**, signed by the
entitled key and binding identity, lineage, and disposition; the log
head is a second signer that authenticates *inclusion*, not
disposition — G0 is satisfied by the entry, and the head is scored
under G2/C2. *G4 sentence:* a verifier holding one bundle can
establish that this entry is included under the configured log head;
it cannot establish log uniqueness — that no second head, or second
entry under the same head, carries a contradictory disposition —
unless the trust configuration already asserts a single consistent
log and the verifier can reach it, which is the consistency query G2
permits to sit outside the standing report.

**Other.** Must be specified to the same bar — object, signer,
verifier computation, non-claims — before scoring begins.

---

## 2. Gates (mandatory; a candidate failing any gate is ineligible)

**G0 — The A3.7.1 invariant, authenticated.** The component of the
standing evidence that *carries the terminal-disposition claim* — the
object the verifier reads the disposition from — is cryptographically
authenticated by the **entitled key** (§0) and binds the
artifact-derived issuance identity, the attempt lineage, and the
terminal disposition. A disposition claim signed by any other party —
a channel, a custodian, a log operator, or the adversary's own key —
does not satisfy this gate, and no accompanying signature can
substitute for the entitled key's. Accompanying signatures by other
parties over *other* facts (an inclusion proof, a custody
acknowledgment) neither satisfy nor violate G0; they are scored where
their fact belongs (G2, C2). A candidate whose standing evidence has
more than one signer must say in its sketch which component carries
the disposition claim. *(A3 §A3.7.1; P10; A3 §A3.2 item 3. Wording
sharpened 2026-08-30 on the author's read: the earlier text could be
read as failing any multi-signer evidence object, which would have
failed the transparency witness on its log-head signature rather than
on any property of its disposition claim.)*

**G1 — Artifact-derived identity.** The issuance identity that standing
evidence binds is *computed by the verifier from the artifact's signed
bytes* (a digest of the signed core), never read from a label,
ordinal, or field presented alongside the artifact. A construction
whose identity a presenter can re-declare fails. **The transplant
companion, as a test:** take standing evidence issued for a valid
artifact and present it with a *different* artifact — other content,
or an abandoned attempt relabelled as the designated one. The
candidate's correct verifier must report standing `ABSENT` with a
mismatch reason (the transplant is *rejected*); a broken verifier
built on presenter-declared identity must report `ESTABLISHED` (the
transplant is *accepted*) — that acceptance is the failure the
companion exists to exhibit. A candidate whose correct verifier
accepts the transplant fails G1. *(A3 §A3.9.)*

**G2 — Offline verification.** Standing is evaluable from the bundle
plus the trust configuration (§0) and nothing else: no lookup, no live
service, no custodian query at verification time. A candidate whose
*consistency* claim needs an external query (e.g. the transparency
witness's equivocation check) may still pass G2 if its *standing*
report does not, provided G4 states the split. *(A3 §A3.8; §A3.4.)*

**G3 — The S-series discriminates.** S1, S2, and S3 (§0) yield three
distinct (standing, reason) outputs from the candidate's verifier; the
collapsing negative control fails against it; and the P4 verdict is
identical across all three presentations. *(First-link `DECISION.md`
§"Standing test conditions (registered exit condition 3)"; `PROBE.md`
Q2/Q4; A3 §A3.7.1.)*

**G4 — Explicit equivocation boundary, including in time.** The
candidate states exactly what a verifier holding one bundle can and
cannot establish when the entitled key has issued contradictory
terminal claims for one lineage — **and** when such a claim was signed
*after* the lineage's anchoring window, by a holder of the entitled
key at a time when no living authority can revoke it (the service may
be dead; the key may have leaked years later). Artifacts are
time-bounded by anchoring (A2.1: declared time within δ of chain
time); standing evidence is created after the anchor confirms and is
not bounded by anything unless the candidate binds it — by anchoring
the evidence itself, by binding it into an anchored object, or by
stating plainly that it is unbounded. A candidate is not required to
close the A2 residue or the post-mortem case; it is required to name
its boundary in both. A missing or overclaiming boundary statement
fails. *(A3 §A3.7 item 1, the residue A2.4 leaves open; A2.1 temporal
predicate; §A3.4 floor. Temporal clause added 2026-08-30 on a blind
project-level review — the criteria as first drafted asked what, not
when.)*

---

## 3. Required engineering properties (mandatory, judged pass/fail)

**R1 — Symbolic modelability.** The construction and its transplant
companion can be written as a ProVerif model over the suite's shared
theory — as yet unextracted (`formal/suite/ENUMERATION.md` §1), so for
this decision "the theory" means the first-link spike's declarations:
a public channel; signature primitives `sign`/`checksign`/`pk` with
the single equation `checksign(sign(m,k), pk(k)) = m`; an injective
fingerprint `fp`; an injective digest `h`; domain-separation tags one
per signed object kind; the map-v1 tuple constructor; and events for
authority publication, possession, signing, and acceptance — under
the §0 adversary, of a size the author can read
(the first-link models — roughly a hundred lines each — are the
reference), with the companion red on a named query and the correct
model green. Panel criterion 4 requires the chosen mechanism modeled
before Band 0 exit. *(`FIRST-LINK-SPIKE.md` at `8ae4720`, criterion 4;
`formal/suite/ENUMERATION.md` S-STANDING slot.)*

**R2 — Refusal-record consistency.** The candidate's relationship to
the portable refusal record (§0) is explicit: the two derive a
lineage's terminal disposition from the same signed fact, so that they
cannot *honestly* disagree. Dishonest contradiction is equivocation,
and is governed by G4's boundary statement rather than by this
property. Whether standing evidence and the refusal record are one
object or two is not itself preferred.

> **RULED (author), 2026-08-30, at registration.** Two wordings were
> drafted: (a) Codex, blind — "the two cannot produce contradictory
> terminal claims without detection"; (b) Claude, non-blind dissent —
> the wording above. The author asked whether (a) is false for every
> offline candidate, the TLR included; it is: an entitled key can sign
> a standing record and a refusal record that contradict, and a
> verifier holding one bundle cannot detect it, so (a) either fails
> every candidate G2 admits or is G4 restated as a closure requirement
> G4 itself disclaims. Three reviewers blind to the probe results
> (Grok, Gemini, a separate Claude instance) reached the same reading.
> The author struck (a) and kept (b); the decision is his, on the
> question he put.

**R3 — Deterministic failure reporting.** Malformed, internally
inconsistent, mis-signed, non-matching, and absent standing evidence
each produce a defined, distinct outcome; no inference, fallback, or
normalization at verification. *(The first-link verifier-boundary
rule — "no inference, negotiation, normalization, or fallback" —
applied to standing.)*

---

## 4. Comparative criteria (only among candidates passing §2 and §3)

**C1 — Intrinsic operational simplicity.** Objects, signing events,
and verifier steps the construction adds by its design. *Intrinsic*
means present in any faithful implementation; a cost that exists only
because of how a prototype happened to be built is not intrinsic.
Example of the distinction: "the TLR requires one additional signing
event at terminal disposition" is intrinsic; "the probe's TLR carried
anchor references the verifier never read" is accidental.

**C2 — Trusted-component and custody burden.** How many parties must
be honest, and how many must survive, for the construction's claims to
hold — at issuance and over the horizon the survivability floor (§0)
governs; and what a custodian must retain for the claims to remain
checkable. The sharp question is whether the construction **creates a
new custody subject** — bytes some party must retain and serve beyond
the bundle. Evidence carried in the bundle (G2) should create none; a
construction that depends on a surviving log or registry does, and
that subject then has no assigned owner (band-1 docket item 17:
retention and retrieval responsibility for anything a verifier must
fetch from outside the envelope is currently unassigned). Score the
construction's own custody demand, not its resemblance to item 17.

**C3 — Failure visibility.** When the construction's assumptions fail
— key compromise, custodian loss, log unavailability — does a relying
party see `ABSENT`/`UNVERIFIABLE` with a reason, or a false
`ESTABLISHED`?

**C4 — Author readability, falsifiable.** The author writes at least
one paragraph, without AI assistance, explaining: what evidence is
verified; who could forge or equivocate about it; what an artifact
presented alone establishes; and what remains unproved. The paragraph
is the score: it is compared against the candidate's sketch and G4
sentence, and the candidate fails C4 if the author cannot write it or
if what he writes misstates what the construction establishes.

---

## 5. Selection rule (registered before scoring)

1. Reject every candidate that fails a gate (§2) or a required
   property (§3). The failing criterion is named.
2. If exactly one candidate survives, it is selected, and its G4
   boundary statement enters the relying-party story verbatim.
3. If more than one survives, select the least complex (C1, C2)
   construction whose residuals are explicit — **unless** the
   survivors differ materially on security (G4 boundaries) or custody
   (C2). The scorer's duty is to *flag* a candidate material
   difference and route it; *materiality is the author's declaration,
   not the scorer's*, made on the cold read. When flagged, scoring
   stops short of a selection and the choice is put to the author as
   a named fork, not reduced to a score.
4. If none survives, no mechanism is selected; the failing criteria
   are recorded, and the outcome is routed to amendment discipline —
   which registered statement must change — never to a relaxed gate.
5. **Evidence channel, bounded.** The probe (`PROBE.md`, frozen) was
   permitted to implement *one* candidate, the terminal lineage record.
   Scoring of that candidate against §2–§4 may cite `RESULTS-PROBE.md`;
   scoring of every other candidate is **criteria-level, not
   evidential**, and the decision document must label it so (the
   first-link decision's own practice for unmodeled alternatives). A
   scorer who finds an unprototyped candidate failing a gate on
   design grounds alone must show the failure from the candidate's
   sketch, not from the absence of a probe.
6. Scoring is performed by the collaborator, on record; the author
   reads it cold and ratifies or overrides, per the DECISION.md
   pattern.

---

## 6. Registration semantics

- **Registered where:** this repository, this file, the author's
  commit. The commit message affirms the author had not read
  `RESULTS-PROBE.md` at registration.
- **Cited corpus, pinned:** the registered statements this file
  restates are those adopted at A1 `03cd3db`, A2 `62f0c5f`, A3
  `8ae4720`, the first-link decision `459aff0`, and the design-probe
  ruling `634c2f2`. If any of them is later amended in a way that
  changes a restatement above, that is a rule-4 event for this
  decision: the criteria are re-registered before scoring resumes, not
  silently reread.
- **Changes after registration** follow amend-don't-rewrite: appended,
  dated, labeled; the original stays.

## 7. Explicitly NOT criteria

Reuse of probe code; similarity to the probe fixture; convenience
arising merely because one candidate was prototyped; proof speed;
whether a query happened to verify (the negative controls exist for
that).

## 8. Sequence from here

Author edits and commits — registration →
author reads `RESULTS-PROBE.md` → collaborator drafts the decision
document scoring every candidate under §2–§5, labeling evidential
versus criteria-level scoring per rule 5 → author cold read → decision
entered. A candidate under "other," if any, is specified to §1's bar
before the scoring draft begins.
