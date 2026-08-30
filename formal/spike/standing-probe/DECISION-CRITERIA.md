# Standing-evidence mechanism decision — criteria and selection rule

**Status: PROPOSED (clerk-drafted 2026-08-29; revised toward
stand-alone 2026-08-30 on a blind external review). Becomes REGISTERED
on the author's commit, which affirms that the author had not read
`RESULTS-PROBE.md` at the time of registration.** Edit before
committing; the registration is the commit, not this draft. One
wording decision is left for the author in the body (R2, marked).

**Provenance, stated because it matters here.** The AI collaborator
that built and ran the probe (Claude) has read its results. The
reviewer that shaped this document's structure (Codex, 2026-08-29) had
not; the blind reviewer whose findings drove the 2026-08-30 revision
had not; the author has not. Structure follows Codex's blind draft.
Claude's contributions are: pinning terms to registered text; the
glossary and restatements below (from registered text only); the
candidate sketches — of which the terminal-lineage-record sketch is
**copied from `PROBE.md` §Fixture, frozen before the probe ran**, so
that a non-blind hand did not write it; and one flagged dissent (R2).

Pattern: `formal/spike/first-link/DECISION.md` — criteria fixed before
evidence, scoring on record, rejected alternatives named.

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
  statement version — `formal/spike/first-link/PREDICTIONS.md`). The
  **entitled key** is the issuer key that tuple names — the same key
  whose signature the evidence chain accepts (A3 §A3.2 item 3) and
  which must prove possession by manifest self-signature (A1 §A1.5
  item 3, P10). This document assumes one entitled key per lineage;
  a candidate that needs more must say so under G0.
- **Adversary (A1 §A1.3).** Alters any bytes after issue; strips,
  reorders, duplicates signatures; substitutes keys, including after
  seeing valid signatures, and self-signs freely with keys it holds;
  replays valid objects in other contexts and re-frames across P7 type
  boundaries; crafts manifests and anchors anything; controls any
  proper subset of the external authority channels, never all.
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
- **The S-series (first-link `DECISION.md`, exit condition 3).**
  Three registered standing test conditions with mandatory distinct
  reason codes: **S1** lineage present, artifact *is* the shipped
  anchor → standing, `TERMINAL_DISPOSITION_SHOWN`; **S2** lineage
  present, artifact *superseded* → no standing, `SUPERSEDED`; **S3**
  lineage absent, artifact presented alone → no standing,
  `NO_TERMINAL_DISPOSITION_EVIDENCE`. **The collapsing negative
  control:** a deliberately broken verifier that emits one reason code
  for S2 and S3 must *fail* a discrimination check; if it passes, the
  check is not testing what it claims.
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

**Terminal lineage record (TLR).** *(Sketch copied from `PROBE.md`
§Fixture, frozen 2026-08-29 before the probe ran.)* An issuer-signed
object created at terminal disposition, carrying at minimum: issuance
identity (a binding to the artifact — the exact form is one of the
probe's outputs), attempt lineage (attempt identities with anchor
references and per-attempt dispositions), and terminal disposition
(`SHIPPED <attempt>` or `REFUSED`). Signer: the entitled key. Verifier
computes: signature under the entitled key; whether the presented
artifact's identity appears in the lineage; whether it is the terminal
one. Does not claim: that the issuer has not signed a second,
contradictory record; anything about attempts absent from the lineage.

**Capability.** *(Clerk sketch, 2026-08-30; not prototyped.)* A
single-purpose token signed by the entitled key at terminal
disposition, naming the designated artifact's identity and
disposition, carried with that artifact. Signer: the entitled key.
Verifier computes: token signature; token identity equals the
presented artifact's identity; disposition. Carries no lineage — so
whether S2 (superseded, lineage present) remains distinguishable from
S3 depends on lineage being supplied some other way, which the
candidate must specify. Does not claim: anything about other attempts;
non-equivocation.

**Transparency witness.** *(Clerk sketch, 2026-08-30; not
prototyped.)* An append-only log, operated by Tessera or a third
party, records each lineage's terminal disposition under the entitled
key; standing evidence is an inclusion proof (log signature, Merkle
path, log head) carried in the bundle. Signers: the entitled key (the
entry) and the log (the head). Verifier computes: inclusion proof
against a log key or root in the trust configuration; the entry's
identity and disposition against the artifact. Closes equivocation to
the extent the log is consistent — a contradictory second disposition
requires a second log entry, visible to anyone auditing the log — at
the price of a trusted, surviving log. Does not claim: log
availability or honesty beyond what the trust configuration asserts.

**Other.** Must be specified to the same bar — object, signer,
verifier computation, non-claims — before scoring begins.

---

## 2. Gates (mandatory; a candidate failing any gate is ineligible)

**G0 — The A3.7.1 invariant, authenticated.** Standing evidence is
cryptographically authenticated by the **entitled key** (§0) and binds
the artifact-derived issuance identity, the attempt lineage, and the
terminal disposition. A well-formed assertion signed by any other
party — including a channel, a custodian, or the adversary's own key —
does not satisfy this gate. *(A3 §A3.7.1; P10; A3 §A3.2 item 3.)*

**G1 — Artifact-derived identity.** The issuance identity that standing
evidence binds is *computed by the verifier from the artifact's signed
bytes* (a digest of the signed core), never read from a label,
ordinal, or field presented alongside the artifact. A construction
whose identity a presenter can re-declare fails; the transplant
companion (§0) must go red against the correct construction and green
against this failure. *(A3 §A3.9.)*

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
exit condition 3; A3 §A3.7.1.)*

**G4 — Explicit equivocation boundary.** The candidate states exactly
what a verifier holding one bundle can and cannot establish when the
entitled key has issued contradictory terminal claims for one lineage.
A candidate is not required to close the A2 residue; it is required to
name its boundary. A missing or overclaiming boundary statement fails.
*(A3 §A3.7 item 1, the residue A2.4 leaves open.)*

---

## 3. Required engineering properties (mandatory, judged pass/fail)

**R1 — Symbolic modelability.** The construction and its transplant
companion can be written as a ProVerif model over the suite's shared
theory library under the §0 adversary, of a size the author can read
(the first-link models — roughly a hundred lines each — are the
reference), with the companion red on a named query and the correct
model green. Panel criterion 4 requires the chosen mechanism modeled
before Band 0 exit. *(`FIRST-LINK-SPIKE.md` at `8ae4720`, criterion 4;
`formal/suite/ENUMERATION.md` S-STANDING slot.)*

**R2 — Refusal-record consistency.** The candidate's relationship to
the portable refusal record (§0) is explicit, and — 

> **[AUTHOR DECIDES WORDING AT REGISTRATION — delete one]**
>
> **(a) Codex, blind:** — the two cannot produce contradictory terminal
> claims without detection.
>
> **(b) Claude, non-blind dissent:** — the two derive a lineage's
> terminal disposition from the same signed fact, so that they cannot
> *honestly* disagree; dishonest contradiction is equivocation and is
> governed by G4's boundary statement.
>
> *Dissent rationale:* an entitled key that can equivocate between two
> standing records can equivocate between a standing record and a
> refusal record; no offline construction detects that by itself, so
> (a) either fails every offline candidate or duplicates G4. The
> blind reviewer of 2026-08-30 concurred that (a) "would have collapsed
> every offline candidate" and asked that the choice be made in the
> registering commit, not later.

Whether standing evidence and refusal record are one object or two is
not itself preferred.

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
checkable (band-1 docket item 17: retention and retrieval
responsibility for anything a verifier must fetch is currently
unassigned).

**C3 — Failure visibility.** When the construction's assumptions fail
— key compromise, custodian loss, log unavailability — does a relying
party see `ABSENT`/`UNVERIFIABLE` with a reason, or a false
`ESTABLISHED`?

**C4 — Author readability, falsifiable.** The author can explain,
without the implementation or an AI present: what evidence is
verified; who could forge or equivocate about it; what an artifact
presented alone establishes; and what remains unproved. Scored by the
author writing that paragraph, not by his sense that he could.

---

## 5. Selection rule (registered before scoring)

1. Reject every candidate that fails a gate (§2) or a required
   property (§3). The failing criterion is named.
2. If exactly one candidate survives, it is selected, and its G4
   boundary statement enters the relying-party story verbatim.
3. If more than one survives, select the least complex (C1, C2)
   construction whose residuals are explicit — **unless** the
   survivors differ materially on security (G4 boundaries) or custody
   (C2). *Materiality is the author's declaration, not the scorer's.*
   In that case scoring stops and the choice is put to the author as a
   named fork, not reduced to a score.
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

Author edits (including the R2 choice) and commits — registration →
author reads `RESULTS-PROBE.md` → collaborator drafts the decision
document scoring every candidate under §2–§5, labeling evidential
versus criteria-level scoring per rule 5 → author cold read → decision
entered. A candidate under "other," if any, is specified to §1's bar
before the scoring draft begins.
