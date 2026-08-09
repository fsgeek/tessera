# Floor-structure viability probe — declaration

Status: DECLARED before any run (this file is written and complete
before TLC is first invoked on the probe model; the session
transcript and, on author signature, the committing order evidence
the freeze). Tier: **viability probe** — outcomes are evidence about
the *viability of a modeling approach*, never about any registered
property. Nothing here discharges, weakens, or touches any A1.2
obligation.

## Purpose

Decision support for the open fork on the P4/A3.2 correspondence
(2026-08-09 discussion, Claude/Codex review exchange):

- **Path A** — bridge only; the TLA+ layer never owns evidence-chain
  structure.
- **Path B** — bridge plus a TLA+ model that owns linked-floor
  structure (candidate part of the P1/P7 TLA+ discharge shape).

The most likely break point of Path B is representational: "linked"
either degenerates into a definitional boolean (a toy — readable
false assurance) or bloats into a re-implementation of attacker
deduction in the wrong tool. This probe stresses that break point at
minimal complexity, fail-fast, before any schedule is committed.

## Fixture

The registered rationale of A3.2 ("Why linked, not counted",
`docs/phase-0-prereg-amendment-3.md`) and the 2026-07-28 Ruling 2
(floors are LINKED — one evidence chain — not counted), mechanized
as a contrast over one minimal state space:

- An acceptance consuming an authority statement and a key
  (`accStmt`, `accKey`), a possession proof (`possKey`), and a set
  of external evidence objects, each binding a (statement,
  key-fingerprint) pair. Symbolic fingerprints are injective (same
  abstraction as the spike's symbolic hash). Artifact validity is
  implicit — every present object is assumed verified as an
  artifact; *linkage between valid artifacts* is the entire
  question.
- Three floor predicates, in claimed strictness order:
  1. `CountedCard` — "≥ 1 external evidence" (A3.2's quoted counted
     floor).
  2. `CountedRelevant` — the steelman repair of counting (per the
     mechanism-review rule: model the simplest plausible
     alternative, not the strawman): each counter individually
     relevance-checked (some evidence for this statement AND some
     evidence for this key).
  3. `Linked` — one shared evidence witness closing statement and
     key together, plus chain-internal possession (A3.2 item 3).

Scope exclusions, named: no attacker deduction (constructibility
remains ProVerif's), no waiver-lattice interaction (that join is the
bridge's job), no per-layer quantification (A3.2 item 4 deferred),
no chain depth beyond one link (representative complexity is the
capstone sidecar's question, not this probe's).

## What must hold and what must fire

Must-HOLD (main cfg, all configurations): the floor hierarchy
`Linked ⇒ CountedRelevant ⇒ CountedCard`, plus definitional pins in
the P4 `Exact*` style (they guard future edits, not present depth —
declared as such, so a green here is not mistaken for depth).

Must-FIRE witnesses (sanity cfg, `-continue`; TLC *violating* each
is the healthy result, per the vacuity-witness convention):

- **W-honest**: a `Linked` configuration exists (the floor is
  satisfiable — not vacuous).
- **W-foreign**: `CountedCard` accepts a configuration whose entire
  evidence set supports a *different* statement than the accepted
  one — the registered aTLS-genus configuration, as a machine trace
  instead of prose.
- **W-cross**: `CountedRelevant` accepts a configuration with no
  single shared witness (evidence for the statement and evidence
  for the key are *different objects*) — the ∃∧∃ vs ∃(∧)
  quantifier-scope failure; the same error class as the retracted
  pair-judge implication, appearing here in the floor itself.
- **W-possession**: `CountedRelevant` accepts a closed chain whose
  possession proof is by a foreign key — counting never sees A3.2
  item 3.

Each witness maps to registered text; the mapping is in the module
comments (per the prose-mapping obligation's spirit).

## Three named outcomes (declared before running)

1. **Contrast expressed.** Main cfg green AND all four witnesses
   fire with concrete traces, within timebox. Reading: the
   linked-vs-counted distinction is mechanizable in TLA+ at minimal
   complexity, and the counted floors' failure modes exist as
   machine traces (currently prose-only in the record). This is
   viability evidence FOR Path B *at this complexity only*; whether
   linkage stays expressible at representative complexity (two
   channels, first link, per-layer) remains open and belongs to the
   capstone sidecar. The declared toyness caveat: the linked floor's
   own green is largely definitional here; the evidentiary weight is
   in the witness traces.
2. **Degeneracy.** Any witness fails to fire — a floor collapses
   into a neighbor at this state space (e.g. `CountedRelevant` ≡
   `Linked`), so the contrast has no content at minimal complexity.
   Reading: Path B's standalone value is not demonstrated; evidence
   toward bridge-only, pending a richer fixture if the author wants
   one.
3. **Viability failure.** TLC cannot parse/run/complete within the
   timebox. Ablate and retry once; if it persists, record a
   viability failure — no evidence about floors at all.

## Timebox and toolchain

Timebox: 30 minutes wall-clock for all TLC runs combined; expected
well under one minute (state space ≈ 128 configurations at the
declared constants: two statements, two keys).

Toolchain note: this machine (post-split) had no TLA+ tools; TLC was
installed today (`~/.local/lib/tla2tools.jar`, reports version
2026.07.31 snapshot) and differs from the Band-0 runs' TLC 2.19.
Acceptable at probe tier; if any artifact here graduates toward
registered evidence, re-pin the version first.

## Exit effect

None on any registered obligation. The outcome feeds exactly one
thing: the author's ruling on Path A vs Path B (and the shape of the
ledger obligation to be registered against the open cross-model
correspondence tracker item). RESULTS-PROBE.md records outcomes
separately so this declaration stays as-authored.
