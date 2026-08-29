# Standing-evidence design probe — predictions vs. observed

**PROBE — NON-DISCHARGING.** Design evidence about the *shape* of a
terminal-lineage-record construction, under
`docs/reviews/2026-08-29-design-probe-ruling.md`. Nothing here changes
any status in `PROPERTIES.md` or discharges any registered property.
Findings are routed to a standing-mechanism decision document whose
criteria the author registers **before** reading this file.

Run 2026-08-29, Python 3.14.6, pycryptodome 3.23.0, no network. Code in
`probe/` (`probe.py` fixture, `run_probe.py` runner); raw outputs
`probe/run1_fixture_failure.out` and `probe/run2.out`. Construction plus
both runs: well inside the one-session timebox.

**Run 1 was a fixture failure, preserved.** Every signature check
returned false, honest channel evidence included — pycryptodome 3.23
imports DER-encoded Ed25519 public keys but not raw 32-byte points, and
the fixture used raw. Fixed by switching to DER (`probe.py` comment at
the site). Outcome-3 flavour, caught inside the timebox; recorded
because a probe whose first run is all-red and whose second run is
all-green should show its work.

## Fixture note that matters for reading everything below

The A2.4 residue — two cryptographically valid artifacts for one
content, one shipped — is produced by an attempt that is **late by the
issuer's clock** (so the issuer abandons it and reissues) but **buried
within δ by chain time** (so a verifier accepts it). An attempt whose
anchor is *orphaned* fails the temporal test and returns `INVALID`
(Q1 contrast line); that is not the residue and never was.

## Predictions vs. observed

| Q | Predicted (frozen) | Observed |
|---|--------------------|----------|
| Q1 baseline | both `VALID_STRICT`; only declared time + anchor differ; nothing says "shipped"; standing `ABSENT`/`NO_TERMINAL_DISPOSITION_EVIDENCE` for **both** (p≈0.9) | **as predicted.** Differing core field: `declared` only (anchor heights differ outside the core). Attempt 1 `confirmed_at` 55 ≤ declared 0 + δ 60: accepted. The shipped artifact, alone, also has no standing. |
| Q2 TLR S1/S2/S3 | three distinct outputs (p≈0.7); TLR lacks a needed field (p≈0.25) | **as predicted, first try.** `ESTABLISHED`/`TERMINAL_DISPOSITION_SHOWN`; `ABSENT`/`SUPERSEDED`; `ABSENT`/`NO_TERMINAL_DISPOSITION_EVIDENCE`. Envelope verdict unchanged across all three (`VALID_STRICT`) — orthogonality held. |
| Q3 transplant | handle-bound: both rejected with a distinct reason; ordinal-bound: (b) accepted (p≈0.8) | **as predicted, and stronger:** with handle binding (a) → `STANDING_EVIDENCE_MISMATCH`, (b) → `SUPERSEDED`; with ordinal binding **both** (a) and (b) → `ESTABLISHED`. No P7 layer notion was needed to pose (b). |
| Q4 collapsing control | fires (p≈0.95) | **fired.** Collapsed verifier: S2 and S3 both `NO_STANDING`; discrimination check FAIL. Correct verifier: PASS. |
| Q5 equivocation | undetectable alone (p≈0.9) | **as predicted.** Each bundle, alone, `ESTABLISHED`. See finding F1. |
| Q6 external dependency | none (p≈0.85) | **none.** Pre-bundle inputs: trust configuration only (channel public keys, `k`, `δ`). Everything else read from the bundle; list in `run2.out`. |
| Q7 refusal join | same shape or strict subset (p≈0.6) | **overlap, not subset.** Shared: attempt identity, disposition. TLR lacks: disclosable reasons, public commitment value. Refusal record lacks: full attempt lineage with anchor references. See finding F2. |

**Outcome classification (declared vocabulary): outcome 1, shape
established** — with two construction findings (F1, F2) that fall
short of outcome 2's "the TLR needed something A3.7.1 did not name"
but belong in the decision's criteria.

## What the TLR had to be (observed, not argued)

1. **Identity derived from the signed bytes.** The load-bearing thing
   in Q3 is that an attempt's identity is `sha256(signed core)` —
   computed by the verifier from what it holds — never a label
   presented alongside the artifact. The ordinal variant is not a
   weaker binding; it is no binding, and it accepts every transplant.
   This is what "binding its issuance identity" in A3.7.1 has to mean
   concretely. Any identity declared rather than derived is a
   transplant surface.
2. **A lineage of (identity, disposition) pairs**, signed. The
   abandoned attempt's presence in the lineage, with its disposition,
   is what makes S2 (`SUPERSEDED`) discriminable from S3.
3. **A terminal disposition naming the shipped identity**, or
   `REFUSED`.
4. **Signed by the accepted key** — the key the authority tuple names.
   A TLR under any other key is `UNVERIFIABLE`/
   `STANDING_EVIDENCE_SIGNATURE_INVALID`.
5. **Carried in the shipped bundle.** Q1's quiet consequence: the
   artifact Tessera designated has no standing *either* until its
   TLR travels with it. Standing evidence is a bundle member created
   at terminal disposition, not a lookup.

**Not load-bearing in this fixture:** the per-attempt `anchor_ref`
inside the lineage. The verifier never read it; the artifact's own
anchor is checked by the envelope test. Informational, or drop it.

## Findings the predictions did not name

**F1 — The verifier lacks a TLR well-formedness check.** In Q5,
TLR-B names attempt 1 as shipped while its own lineage entry for
attempt 1 still reads `ABANDONED_ISSUER_TIMEOUT`, and the verifier
returned `ESTABLISHED`. Internally inconsistent standing evidence
should be its own outcome — `STANDING_EVIDENCE_MALFORMED` or similar,
in the `INVALID`-dominates spirit of the first-link decision — and
the S-series vectors should include it. Not a security finding (the
issuer signed both halves); a conformance finding. Not fixed in the
probe: the questions were frozen, and the point of a probe is to show
what it found, not to tidy it.

**F2 — There are four standing conditions, not three.** A holder of
any attempt from a *refused* lineage gets `ABSENT`/`ISSUANCE_REFUSED`
— distinct from `SUPERSEDED` and from
`NO_TERMINAL_DISPOSITION_EVIDENCE`. DECISION.md's S1–S3 do not cover
this holder. Either an S4 is registered or the decision document says
why a refused-lineage holder is not a standing case (they are — the
refusal record is where they learn their disposition, and Q7 shows the
two records overlap without either containing the other). Routed with
Q7's join question: one object or two.

**F3 — Equivocation is the construction's boundary, stated exactly.**
A TLR closes "which of two valid artifacts did the issuer designate"
against everyone *except the issuer key itself*. Two TLRs from one
key are individually valid and mutually contradictory, and a verifier
holding one bundle cannot know the other exists. That is A2's open
residue, unchanged; a transparency witness is the class of
construction that would close it, at the survivability cost the
record already names. The decision must weigh this explicitly rather
than let the TLR's clean S1–S3 result imply more than it shows.

## Boundaries of this evidence

Stub canonicalization, stub fingerprint, stub chain, stub channels,
one issuer, one signer, no P7 layering, no A3.7.2 state machines, no
real anchoring. Every green here is about the *shape* of a record and
what a verifier can compute from a bundle; none of it is evidence that
any implementation conforms to any model, and none of it will be
carried into Phase 1a. If a construction is selected, the suite model
(S-STANDING) and the Phase 1a code are written from the decision.
