# Tessera — Phase 0 Pre-Registration, Amendment 2 — DRAFT

> **Status: DRAFT.** Not signed, not in force. Per Amendment 1 precedent,
> this draft goes through falsification-style non-author review (the A1.7
> discipline, applied to the amendment itself) before the author signs,
> commits, and OTS-anchors it. Review artifacts and dispositions land in
> `docs/reviews/` either way.
>
> **What this document is.** The second amendment to the Phase 0
> pre-registration (`phase-0-prereg.md`, commit `75207ba`), layered on
> Amendment 1 (`phase-0-prereg-amendment-1.md`, commit `03cd3db`). The
> original and prior amendments are never edited; this document states what
> changes, and why, on the record.
>
> **Provenance.** Building the P5c issuance-protocol state machine
> (`formal/tla/P5c_IssuanceProtocol.tla`) forced a precision the registered
> prose did not have: "confirmed … within δ" admits a strict reading (depth
> k *reached* by `declared_issue_time + δ`) and a permissive one (block
> time in-window, depth reached whenever). The fork was flagged in the
> module header per the recorded-decision rule, and resolved by the author
> on 2026-07-07 after an adversarial ratification dialogue with the AI
> collaborator (Claude, per §0/§6 division of labor). All decisions herein
> are the author's (Tony Mason).

---

## A2.0 What the model surfaced, and a correction registered with it

The state machine did what pre-registering models is for: it made a prose
ambiguity mechanically undeniable. The author ratifies the **strict**
reading — restated below on a chain-visible observable so that the issuer
and the verifier check the *same predicate*.

One correction from the ratification dialogue is registered alongside,
because leaving it implicit would invite a misreading of what the strict
rule protects. Consider the **abandoned-anchor artifact**: an issuance
attempt whose anchor lands in an in-window block but buries slowly; the
strict issuer discards and re-issues, yet the discarded transaction
persists and typically confirms later, so a complete, chain-verifiable
(receipt, anchor) pair exists that was never shipped. Checked against the
registered properties: this artifact violates **none of them**. The
anchor's security content is the block time alone — backdating is bounded
because no forger can place bytes in a past block (P5), and P6's
uncertainty window is bounded by `anchor_time` because signing precedes
block inclusion. *When* depth k was reached enters neither argument. What
the depth-k-within-δ rule actually protects is different: no shipped
receipt can be orphaned by a tolerated reorganization (the P5c
`NoShippedOrphan` invariant), and the issuer's evidence trail stays free
of receipts whose completion needs explaining. The residue the artifact
does create — two verifiable receipts for the same content with different
declared times — is closed by A2.2 and A2.4 below.

The ratified form strengthens P5 with a new verifier-side conjunct and
adds obligations; under A1.2's change discipline that requires this
amendment. Nothing is weakened; the A1.1 falsifier is not triggered.

---

## A2.1 "Confirmed within δ": one predicate, both sides

**Vocabulary.** The anchor transaction is included in the block at height
`h`. Confirmation count follows the Bitcoin convention: the including
block is the first confirmation, so `c = tip_height − h + 1`, and the
block that grants the k-th confirmation has height `h + k − 1`. Define

    confirmed_at  :=  timestamp(block at height h + k − 1)

**The rule.** Issuance is complete only if

    confirmed_at  ≤  declared_issue_time + δ

The issuer evaluates this predicate before shipping; the verifier
evaluates the **identical predicate on the identical observable** at
verification (A2.2). If it fails at issuance time, the attempt is
discarded and re-issued per the P5 corollary, subject to the attempt
bound of A2.3.

**Why chain time on both sides.** A wall-clock ship rule ("ship if depth k
by `now ≤ declared + δ`") and a block-timestamp verifier check can
disagree at the δ boundary by the consensus-bounded skew (block timestamps
may run up to about two hours ahead of network-adjusted time). Defining
the rule once, on the chain-visible quantity, removes the divergence: **no
honestly-shipped receipt can fail the verifier's confirmation conjunct, by
construction**, and the model's `Ship` action and the verifier predicate
become the same statement about the same observable — the exact
correspondence A1.4 demands.

**Named residuals.**

- *Adversarial timestamping.* A miner can set `timestamp(h + k − 1)`
  forward within the consensus bound, pushing an honest issuance into the
  tail case. This is a griefing surface bounded to hours against δ = 72
  hours; it can force a re-issue, never a false verdict.
- *Non-monotonic timestamps.* Block timestamps are not monotonic;
  `confirmed_at` may even precede `anchor_time`. The predicate is a single
  comparison on one designated block and is well-defined regardless; no
  monotonicity is assumed.

**Model-convention pin (off-by-one, fixed here so it cannot drift).**
P5c's `depth` variable counts blocks mined *after* inclusion (`depth = 0`
at inclusion), so `depth ≥ DepthK` corresponds to `c ≥ DepthK + 1`. The
correspondence mapping instantiates **`DepthK = k − 1`** (for the strict
default k = 6: `DepthK = 5`). δ, ε, k remain ratified (or revised, on the
record) at Band 0 exit, as registered; δ's 72-hour sizing already included
aggregation-to-confirmation lag, so this amendment does not move it.

---

## A2.2 P5, amended: the strict temporal check gains a third conjunct

`VALID_STRICT` now requires all of:

    declared_issue_time − ε  ≤  anchor_time                       (unchanged)
    anchor_time              ≤  declared_issue_time + δ           (unchanged)
    confirmed_at             ≤  declared_issue_time + δ           (new)

Consequences, stated explicitly:

- The abandoned-anchor artifact of A2.0 is **rejected outright** — its
  `confirmed_at` exceeds its own window. Within this system the conjunct
  rejects *only* such artifacts: strict issuance ships nothing that fails
  it (A2.1).
- **Evidence obligation.** The verifier must evaluate `confirmed_at`
  statelessly (P9): block headers `h … h + k − 1` are available either
  archived in the bundle or from the verifier-distributed header store the
  anchor check already requires — the same trust-configuration pattern as
  A1.5's historical trust-anchor store. This joins the H1a evidence
  obligations.
- **Waiver status.** Temporal-anchor consistency is already non-waivable
  (A1.2.1); the new conjunct is part of it. The P4 partition applies
  inside it: performed-and-failed → `INVALID`; unperformable (headers
  unavailable) → `UNVERIFIABLE`; neither is promotable.

---

## A2.3 The re-issue loop terminates: bounded attempts, fail-closed refusal

As registered, the P5 corollary's re-issue rule was an unbounded loop, and
its dominant triggers — fee spikes, congestion, calendar outage — are
*correlated across attempts*: retrying under the same conditions is not a
fresh draw, so "re-issue until it works" can livelock. Fail-closed means
issuance must be able to end in refusal, not only in success.

Amended: issuance makes at most **N attempts**. Exhausting them terminates
issuance in an **explicit, reported refusal** — a first-class protocol
outcome, not an error path. N is a protocol constant ratified at Band 0
exit alongside δ, ε, k (working default **N = 3**; at δ = 72h that bounds
the issuance process at nine days).

Model note: P5c's `MaxAttempts` is hereby promoted from a state-space
bound to protocol semantics. The unbounded "eventually ships" liveness
claim remains explicitly unproven (bounded model); the discharged claims
are safety claims, and this amendment adds *termination by construction*
rather than a proven liveness property.

---

## A2.4 Anchor identity and declared-time confinement

- **A receipt's anchor is the proof it ships with.** A shipped receipt
  contains exactly one anchor proof (the OTS proof over its canonical
  bytes) together with the anchor transaction's id, which serves as the
  **retrieval handle** back to the chain. Verification evaluates the
  shipped proof and no other; an anchor not shipped inside a receipt has
  **no standing** in verification or dispute — in particular, a discarded
  attempt's transaction confirming later confers nothing. The handle
  requires no new assumption: a txid is the double-SHA-256 of the
  transaction, so txid → transaction → committed bytes rests on the
  SHA-256 resistance already cited in Layer 2, and the OTS proof's merkle
  path binds the anchored bytes to the block independently of the handle.
  (The txid necessarily lives in the bundle outside the signed bytes — the
  anchor is computed over those bytes, so the txid exists only after them;
  the wrapper discipline of P7 makes the containment tamper-evident.)
- **Declared times are existed-by claims, and only that.**
  `declared_issue_time` asserts the artifact existed by that time;
  re-declaration on re-issue moves it forward, which weakens and never
  falsifies. **No verifier policy, and no downstream marketplace rule, may
  order competing receipts by declared time** (first-to-file semantics):
  the re-issue mechanism necessarily gives the issuer discretion over
  declared times within the retry schedule, and priority ordering would
  convert that discretion into a manipulation surface. This confinement is
  a design commitment in the P6 monotonicity style — assumed by the model,
  enforced by policy, deliberately not filed under Layer 2.

---

## A2.5 New model obligations

- **Verifier-side family (P5/P6):** add the `confirmed_at` observable and
  the A2.2 conjunct under the existing verifier-owns-tolerances
  discipline; a broken companion omitting the conjunct must accept the
  abandoned-anchor artifact — witnessing exactly the gap A2.0 records.
  Standing working rules apply (broken companions, `_Sanity` vacuity
  witnesses for every defined-predicate antecedent).
- **P5c:** the header's semantic-fork paragraph resolves to
  ratified-strict in the A2.1 chain-time form; `MaxAttempts` semantics
  per A2.3; `DepthK = k − 1` convention per A2.1.
- **Conformance vectors (A1.7):** extracted traces must include the new
  conjunct's reject case (late-burial artifact → `INVALID`) and its
  unperformable case (missing headers → `UNVERIFIABLE`).

---

## A2.6 What changed, and what did not

This amendment **strengthens** P5 (a third strict conjunct), **adds**
obligations (header evidence for stateless confirmation checking, the
attempt bound with reported refusal, the anchor-standing rule, the
declared-time confinement commitment, new conformance-vector cases), and
**registers** a correction that narrows what the strict rule may be
claimed to protect. No property is weakened, no capability excluded, no
construction changed: the A1.1 falsifier is not triggered. The bands,
hypotheses, hard invariants, and division of labor are unchanged.
