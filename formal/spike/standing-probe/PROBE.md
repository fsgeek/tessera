# Standing-evidence design probe — declaration

**Status: DECLARED before any code is written.** This file is complete
and committed before the first line of probe code exists; the
committing order is the freeze. **Tier: design probe** under the
2026-08-29 author clarification
(`docs/reviews/2026-08-29-design-probe-ruling.md`) — executable,
non-production, non-conformance-claiming, **non-discharging**. Outcomes
are evidence about the *shape* of a standing-evidence construction,
never about any registered property. No line of this probe is intended
for use in the Tessera service. Construction begins only after the
author's signing commit on the ruling record.

## Purpose

Decision support for the A3 §A3.7.1 construction choice. The
registered invariant:

> Cryptographic validity alone confers no protocol standing. Any
> artifact claiming standing must present verifiable standing evidence
> binding its issuance identity, attempt lineage, and terminal
> disposition. Missing standing evidence leaves the artifact
> evidentially admissible but without protocol standing.

A3.7.1 names candidate constructions — terminal lineage record,
capability, transparency witness, other — and selects none. Panel
criterion 4 (`FIRST-LINK-SPIKE.md`, signed `8ae4720`) requires the
*chosen* construction to be modeled in the symbolic suite before Band
0 exit. The abstract selection dialogue stalled on 2026-08-29 (record:
`formal/suite/ENUMERATION.md`, Q3 correction; Codex diagnosis, same
day): the question had become "what does a verifier holding an
abandoned attempt actually lack, and what must a record bind to
supply it?" — which is answered by holding one, not by naming nouns.

This probe supplies the contact. It builds the smallest executable
issuer/verifier pair in which the A2.4 situation — two
cryptographically valid issuance artifacts for one content, exactly
one shipped — can be produced and presented, and asks what the
verifier can and cannot say, with and without one candidate record.

## Fixture

Python 3.14, standard library plus the already-present `pycryptodome`
(Ed25519 via `Cryptodome.Signature.eddsa`; transitive dependency of the
OTS client — acceptable at probe tier, re-pin if anything graduates).
No network. Everything external is a stub, named as such in code.

- **Issuer**: one Ed25519 key pair; an authority tuple in the map-v1
  shape *(issuer id, key fingerprint, signer set, algorithm,
  version)*; a **manifest self-signature over the tuple** — the design
  encoding of A1 §A1.5 item 3, *not* the spike's fingerprint-only
  encoding (guide correction, 2026-08-27); an attestation signature
  over framed bytes, domain-tagged.
- **Authority channels**: two in-memory signed statements over the
  tuple (stub DNS, stub repository), each with its own key.
- **Chain stub**: a list of blocks with heights and timestamps;
  *anchor* = insert the attestation handle into the next block;
  *bury* = append blocks; *reorg* = orphan the block containing a
  given anchor. Depth `k` and window `δ` are probe constants, not the
  registered parameters.
- **Lifecycle**: attempt 1 anchored, then orphaned by reorg (or
  late-buried) — abandoned; attempt 2 anchored, buried to depth `k`
  within `δ` — shipped. Both bundles are cryptographically valid. This
  is the A2.4 residue made concrete.
- **Verifier**: stateless; consumes a bundle; emits *two orthogonal
  outputs*, per A3.7.1 and A3.8: an envelope verdict (a simplified
  P4 partition — `VALID_STRICT` / `INVALID` / `UNVERIFIABLE`) and a
  **standing report** (`ESTABLISHED` / `ABSENT` / `UNVERIFIABLE`) with
  a reason code. It must never fold the second into the first.
- **Candidate under test: the terminal lineage record (TLR)** — an
  issuer-signed object created at terminal disposition, carrying at
  minimum: issuance identity (a binding to the artifact — the exact
  form is one of the probe's outputs), attempt lineage (attempt ids
  with anchor references and per-attempt dispositions), and terminal
  disposition (`SHIPPED <attempt id>` or `REFUSED`). Only this
  candidate is built. If it proves insufficient, a second candidate
  gets its own declared probe — the spike pattern; a probe that tests
  three constructions at once decides by convenience.

**Scope exclusions, named:** no real chain, no OTS, no DNSSEC; no
wrapping/P7 layering beyond the single transplant case in Q3; no
refusal-record state machines (A3.7.2) beyond the one join question in
Q7; no performance, no persistence, no API.

## Questions (frozen), with predictions

Predictions carry rough probabilities. The outcome vocabulary is
below; "as predicted" is not a virtue — the probe earns its keep on
the branches that *are not* predicted.

**Q1 — Baseline: what the verifier sees with no standing mechanism.**
Present attempt 1 alone and attempt 2 alone. Record every field the
verifier reads and every field that differs between the two bundles.
- Prediction: both `VALID_STRICT`; the differing fields are the
  declared time and the anchor reference only; nothing in either bundle
  says "shipped." Standing: `ABSENT` /
  `NO_TERMINAL_DISPOSITION_EVIDENCE` for **both** — S3 is the *only*
  thing the verifier can honestly say, and it says it for the artifact
  Tessera actually designated too. (p ≈ 0.9 as predicted; p ≈ 0.1 the
  fixture accidentally leaks disposition through some field — itself
  a finding about which fields must be kept out of the artifact.)

**Q2 — The TLR discriminates S1 / S2 / S3.** Attempt 2 + TLR; attempt
1 + TLR; attempt 1 alone.
- Prediction: `ESTABLISHED` / `TERMINAL_DISPOSITION_SHOWN`; `ABSENT` /
  `SUPERSEDED`; `ABSENT` / `NO_TERMINAL_DISPOSITION_EVIDENCE` — three
  distinct outputs from three presentations (p ≈ 0.7 first try;
  **p ≈ 0.25 the TLR as sketched in A3.7.1 lacks a field the verifier
  needs to make S2 discriminable** — the most valuable branch, because
  it says what "binding its issuance identity" has to mean concretely;
  p ≈ 0.05 the fixture cannot express it).

**Q3 — Transplant (A3.9's named companion).** Attach attempt 2's TLR
to (a) a bundle for different content and (b) a wrapper around
attempt 1 that carries attempt 2's TLR. Then build the broken variant:
a TLR that does *not* bind the artifact identity.
- Prediction: with binding, both transplants → `ABSENT` with a
  distinct reason (`STANDING_EVIDENCE_MISMATCH` or similar); without
  binding, transplant (b) is **accepted** — the binding is
  load-bearing and the probe shows what it must be a binding *to*
  (p ≈ 0.8; p ≈ 0.15 the wrapper case needs a layer notion the
  fixture lacks — deferred to P7; p ≈ 0.05 other).

**Q4 — The collapsing negative control (DECISION.md exit condition
3).** A verifier variant that emits one reason code for S2 and S3.
- Prediction: the discrimination check fails on it (p ≈ 0.95). This
  is a test of the test; it exists so the S1–S3 vectors, when they
  are written for H1a, are known to be able to go red.

**Q5 — Equivocation: what the TLR does not close.** The issuer signs
two TLRs designating different attempts as shipped.
- Prediction: a verifier holding either bundle alone cannot detect it
  (p ≈ 0.9). Reading: this is A2's open residue and the seam where a
  transparency witness would do work a TLR cannot. Recorded as a
  boundary of the construction, not a defect of the probe — and as the
  one fact the mechanism decision must weigh against survivability.

**Q6 — External dependency count.** For Q1–Q3, count what the
verifier obtained from outside the bundle.
- Prediction: nothing (p ≈ 0.85). This is the survivability
  compatibility criterion, observed rather than argued.

**Q7 — The refusal join.** Run a lifecycle in which every attempt
fails; the issuer emits a TLR with disposition `REFUSED`. Compare its
fields with A3.7.2's portable refusal record.
- Prediction: the same object shape, or a strict subset (p ≈ 0.6);
  p ≈ 0.4 they diverge in a way that says the two records should be
  one construction or explicitly two — either answer is useful, and
  the question is open-ended by design.

## Three named outcomes (declared before building)

1. **Shape established.** Q1–Q6 as predicted or with predicted
   branches; the TLR's required fields, its artifact binding, and its
   boundary (Q5) are written down from observation. Reading: evidence
   *for the shape* of a terminal-lineage-record construction, to be
   scored under the DECISION.md pattern against whatever criteria the
   author registers before reading these results. Not a selection.
2. **Construction finding.** The TLR needed something A3.7.1's sketch
   did not name (the Q2 p ≈ 0.25 branch), or the transplant defense
   required a layer notion (Q3), or the refusal join diverged (Q7).
   Reading: the probe earned its keep; the finding goes into the
   decision document's criteria, and possibly into a second declared
   probe for a second candidate.
3. **Expressiveness failure.** The fixture could not be built within
   the timebox, or the questions could not be posed to it. Reading:
   evidence about the probe, not about any construction; record and
   stop.

## Timebox and discipline

- Construction: one working session. Runs: seconds. If construction
  exceeds the session, stop and record outcome 3 — a probe that takes
  a week is Phase 1 wearing a costume.
- Every result labeled `PROBE — NON-DISCHARGING` in the results file.
- Code lives in `formal/spike/standing-probe/probe/`; results in
  `RESULTS-PROBE.md` in this directory, predictions-vs-observed per
  question, same table form as the spike.
- Nothing here changes `PROPERTIES.md`. Findings are routed to a
  standing-mechanism decision document (DECISION.md pattern), whose
  criteria the author registers **before** reading `RESULTS-PROBE.md`.
- The probe is quarantined after use: kept for the record, marked
  non-production, never imported by anything in Phase 1a.

## Provenance

Clerk-drafted (Claude) 2026-08-29 under the author's delegation of
sequencing, on Codex's same-day recommendation that the standing
question be taken to an executable fixture, and on the floor-structure
probe's declaration form. The decision to run a probe rather than
continue abstract selection is the collaborator's, on the record as
such. Construction gated on the author's signing commit on
`docs/reviews/2026-08-29-design-probe-ruling.md`.
