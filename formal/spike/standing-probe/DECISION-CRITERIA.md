# Standing-evidence mechanism decision — criteria and selection rule

**Status: PROPOSED (clerk-drafted 2026-08-29). Becomes REGISTERED on
the author's commit, which affirms that the author had not read
`RESULTS-PROBE.md` at the time of registration.** Edit before
committing; the registration is the commit, not this draft.

**Provenance, stated because it matters here.** The AI collaborator
that built and ran the probe (Claude) has read its results. The
reviewer that shaped this document's structure (Codex, 2026-08-29) had
not, and neither had the author. The gates, required properties,
comparative criteria, and decision rule below follow Codex's blind
draft; Claude's contribution is confined to pinning terms to
registered text and to one flagged dissent (criterion R2), which the
author should weigh knowing it comes from a non-blind party.

Pattern: `formal/spike/first-link/DECISION.md` — criteria fixed before
evidence, scoring on record, rejected alternatives named.

## Candidates

Per A3 §A3.7.1: **terminal lineage record**, **capability**,
**transparency witness**, and **other**. A candidate under "other"
must be concretely specified — its evidence object, who signs it,
what a verifier computes from it — *before* scoring begins, or it is
not a candidate. Candidates are scored on their design, not on whether
a probe happened to prototype them.

## Gates (mandatory; a candidate failing any gate is ineligible)

**G0 — The A3.7.1 invariant, authenticated.** Standing evidence is
cryptographically authenticated by the authority entitled to declare
terminal disposition — *the issuer key the authority tuple names*
(P10; the same key whose signature the chain accepts, A3.2 item 3) —
and binds the artifact-derived issuance identity, the attempt lineage,
and the terminal disposition. Well-formed assertions by any other party
do not satisfy this gate.

**G1 — Artifact-derived identity.** The issuance identity that standing
evidence binds is computed by the verifier from the artifact's signed
bytes, never read from a label presented alongside the artifact. A
construction whose identity can be re-declared by a presenter fails
this gate (A3.9's transplant companion must go red against it).

**G2 — Offline verification.** Standing is evaluable from the bundle
plus the verifier's trust configuration (A3.8) and nothing else. No
lookup, no live service, no custodian query at verification time
(§A3.4 survivability floor).

**G3 — The S-series discriminates.** Presented alone (S3),
superseded-with-lineage (S2), and designated-with-lineage (S1) yield
distinct reason codes; the collapsing negative control (DECISION.md
exit condition 3) fails against the candidate's verifier. Standing is
reported orthogonally to the P4 verdict and never alters it.

**G4 — Explicit equivocation boundary.** The candidate states exactly
what it does *not* close of A2's open residue — in particular, what a
verifier holding one bundle can and cannot establish when the
entitled key has issued contradictory terminal claims. A candidate is
not required to close the residue; it is required to name its
boundary, and a candidate whose boundary statement is missing or
overclaims fails.

## Required engineering properties (mandatory, judged pass/fail)

**R1 — Symbolic modelability.** The construction is modelable in the
symbolic suite under the A1.3 adversary at legible size, with its
transplant companion — panel criterion 4 (`FIRST-LINK-SPIKE.md`,
`8ae4720`) requires it before Band 0 exit.

**R2 — Refusal-record consistency.** The candidate's relationship to
the A3.7.2 portable refusal record is explicit, and the two derive a
lineage's terminal disposition from the same signed fact, so that they
cannot *honestly* disagree. Whether one object or two is not itself
preferred.

> *Flagged dissent (Claude, non-blind).* Codex's draft read "cannot
> produce contradictory terminal claims without detection." An
> entitled key that can equivocate between two standing records can
> equivocate between a standing record and a refusal record; no
> offline construction detects that by itself, so "without detection"
> either fails every offline candidate or duplicates G4. The wording
> above requires consistency *by construction* and leaves dishonest
> contradiction to G4's boundary. The author decides which wording is
> registered.

**R3 — Deterministic failure reporting.** Malformed, internally
inconsistent, mis-signed, or non-matching standing evidence each
produce a defined, distinct outcome; no inference, fallback, or
normalization at verification (the first-link verifier-boundary rule,
applied to standing).

## Comparative criteria (used only among candidates passing every gate and required property)

**C1 — Intrinsic operational simplicity.** Number of objects, signing
events, and verifier steps the construction adds — *intrinsic* to the
design, not arising from which candidate was prototyped.

**C2 — Trusted-component and custody burden.** How many parties must
be honest or available, at issuance and over the survivability
horizon, for the construction's claims to hold; what a custodian must
retain (band-1 docket item 17).

**C3 — Failure visibility.** When the construction's assumptions fail,
does a relying party see `UNVERIFIABLE`/`ABSENT` with a reason, or a
false `ESTABLISHED`?

**C4 — Author readability, falsifiable.** The author can explain,
without the implementation or an AI present, what evidence is
verified, who could forge or equivocate about it, what an artifact
presented alone establishes, and what remains unproved. Scored by the
author writing that paragraph, not by the author's sense that he
could.

## Selection rule (registered before scoring)

1. Reject every candidate that fails a gate or a required property.
   A rejected candidate's failing criterion is named.
2. If exactly one candidate survives, it is selected, and its G4
   boundary statement enters the relying-party story verbatim.
3. If more than one survives, select the least complex (C1, C2)
   construction whose residuals are explicit — **unless** the survivors
   differ materially on security (G4 boundaries) or custody (C2), in
   which case scoring stops and the choice is put to the author as a
   named fork, not reduced to a score.
4. If none survives, no mechanism is selected; the failing criteria
   are recorded, and the outcome is routed to amendment discipline
   (which registered statement must change), not to a relaxed gate.
5. Scoring is performed against the probe's results and the record,
   by the collaborator, on record; the author reads the scoring cold
   and ratifies or overrides, per the DECISION.md pattern.

## Explicitly NOT criteria

Reuse of probe code; similarity to the probe fixture; convenience
arising merely because one candidate was prototyped; proof speed;
whether a query happened to verify (the negative controls exist for
that).

## Sequence from here

Author edits and commits this file (registration) → author reads
`RESULTS-PROBE.md` → collaborator drafts the decision document scoring
every candidate under these criteria → author cold read → decision
entered. A candidate under "other," if any, is specified before the
scoring draft begins.
