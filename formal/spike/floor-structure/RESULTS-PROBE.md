# Floor-structure viability probe — outcomes

Run date: 2026-08-09. TLC 2026.07.31 snapshot (see PROBE.md toolchain
note; differs from Band-0's TLC 2.19 — re-pin before any graduation).
Both runs completed in ~1 s wall each; the 30-minute timebox was not
approached. Full logs: `FloorLink_Probe.out`,
`FloorLink_Probe_Sanity.out`.

**Outcome: declared outcome 1 — contrast expressed.**

## Main cfg (must hold)

Green over all 128 configurations (the full declared state space):
`HierarchyLinkedRelevant`, `HierarchyRelevantCard`,
`LinkedNeverForeignOnly`, `LinkedPossessionInternal`. The hierarchy
`Linked ⇒ CountedRelevant ⇒ CountedCard` holds; the witness runs
below show every inclusion is strict.

## Sanity cfg (must fire — TLC violating each is the healthy result)

All four witnesses fired. Canonical traces (first exhibited by TLC):

- **W-honest** (`LinkedUnsatisfiable` violated): acc = (s1, k1),
  poss = k1, evidence {[stmt s1, fp k1]} — the linked floor is
  satisfiable; the greens above are not vacuous.
- **W-foreign** (`CardNeverAcceptsForeignOnly` violated):
  acc = (s1, k1), evidence {[stmt s2, fp k1]} — the cardinality
  floor accepts while every evidence object supports a different
  statement. The registered A3.2 "why linked, not counted"
  configuration now exists as a machine trace instead of prose.
- **W-cross** (`RelevantNeverAcceptsOpenChain` violated):
  acc = (s1, k1), poss = k1, evidence {[stmt s1, fp k2],
  [stmt s2, fp k1]} — each relevance counter finds a satisfying
  object, but no single object closes the chain: the ∃∧∃ vs ∃(∧)
  quantifier-scope failure, the same error class as the retracted
  pair-judge implication (first-link RESULTS.md ledger 4), here
  appearing in the floor itself. Even the steelman repair of
  counting admits it.
- **W-possession** (`RelevantNeverAcceptsForeignPossession`
  violated): acc = (s1, k1), poss = k2, evidence {[stmt s1, fp k1]}
  — chain closed, possession by a foreign key; counting never sees
  A3.2 item 3.

## Reading (bounded, per the declaration)

The linked-vs-counted distinction is mechanizable in TLA+ at minimal
complexity without degenerating: the three floors are pairwise
separated by exhibited configurations, and the counted floors'
failure modes — including the one the 2026-07-28 ruling states only
in prose — are machine traces a reader can inspect. The declared
toyness caveat stands: the linked floor's own greens are largely
definitional pins; the evidentiary weight is the witness traces.
This is viability evidence FOR Path B **at this complexity only**.
Whether linkage stays expressible at representative complexity (two
channels, first link, per-layer) remains open and belongs to the
capstone sidecar. No registered property is touched.

## Incidental finding (tooling, routed to author disposition)

`scripts/filter-tlc-output.sh` performed no filtering on the sanity
run: its pattern matches TLC's next-state violation format
(`Error: Invariant X is violated.`) but not the initial-state format
these degenerate models emit (`Error: Invariant X is violated by the
initial state:`). Consequence: sanity `.out` files from
initial-state models (this probe, and by the same mechanism the P4
sanity run) are full dumps, not the first-violation-per-invariant
form the record-norms ruling intended. Nothing is wrong with the
evidence — it is over-complete, not under-complete — but the script
does not implement the ruling for this model shape. Disposition is
the author's (fix the pattern, or accept full dumps for
initial-state models).

## Review log

- 2026-08-09, Codex (non-author, post-run): runs independently
  reproduced; model sound within scope; outcome classification and
  scope claims endorsed; strict hierarchy confirmed. Two carried-
  forward items, both accepted: (1) these exact runs are never to be
  promoted to registered property evidence — the representative-
  complexity successor must be committed before execution; (2) the
  successor's registered question is the integrated one this probe
  excluded by design: *can a legal degraded policy waive redundant
  paths while a zero-complete-chain valid verdict stays unreachable
  for every contributing layer?* — with a broken companion that
  reaches `VALID_DEGRADED` on individually plausible check results
  with no complete surviving chain. Claude addition to the same
  successor registration: it must also carry the producer-outcome
  status mapping (holds/violation/timeout → pass/fail/unperformable),
  the third axis of the seam, with its own broken companion
  (producer-unavailable mapped to pass must go red).

## Freeze-order note

PROBE.md was authored complete before the first TLC invocation;
model and cfgs second; runs third; this file last. The session
transcript evidences that order. The strict committed-freeze form
(declaration committed before runs) was not available to a
single-session probe — the author's signing commit can attest the
order only on the transcript's authority, and probe tier claims
nothing that depends on it.
