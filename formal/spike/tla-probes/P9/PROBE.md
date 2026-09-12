# P9 statelessness — non-discharging TLA+ probe: declaration

**STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not
adopted; the commit is the author's.**

**Tier: design probe, non-discharging**, commissioned by Amendment 4
§A4.1 (`docs/phase-0-prereg-amendment-4.md`, signed `5188e7a`) under
the design-probe tier of `docs/reviews/2026-08-29-design-probe-ruling.md`
and the PROBE.md pattern of `formal/spike/standing-probe/PROBE.md`.
This file is complete before the first TLC run; the committing order
is the freeze. Questions and predicted branches below are not revised
after a run — a miss is recorded as a miss.

**Asymmetric use rule (A4.1, verbatim in effect):** *a green result is
not evidence and is not cited by any tracker row; a red result or an
unrepresentable-attack finding is a finding to be dispositioned before
exit.* Nothing in this directory moves any row of
`formal/PROPERTIES.md`; P9's discharge path is
**[inspection + vector]** (A4.1) and stays so whatever this probe
reports.

## Purpose

A4.1 predicted that a TLA+ model of P9 — *"the verdict is a pure
function of the bundle and the verifier's declared policy — no
service-side state, no live network dependency, appears in the
decision"* (Amendment 1 §A1.2 P9; the checkable form of §4.4's hard
rule) — "would be stateless because its author wrote it stateless",
the companion-that-cannot-fail pattern. The author ruled the probe be
built anyway: *"If they don't find anything, we don't use it as
evidence. If they do find something, we can act upon that between now
and exit."*

The probe is therefore designed to be able to fail, and to say
exactly what a P9 model can and cannot show. Concretely it asks
three things a green correct model does not answer by itself:

1. Is the P9 invariant, as stated, **discriminating** — does it go
   red on verifiers that are stateful in the ways the design forbids?
2. Does the A4.1 discharge vector — *the same bundle and declared
   policy, verified on two isolated machines with no network, must
   yield the same verdict, and a verifier that consults any optional
   service must fail the vector* — actually **catch** each of those
   stateful verifiers, or only some of them?
3. Is the correct model's green **trivial** (definitional), and if so,
   what is the residual content of the probe?

## Fixture

One TLA+ module, `P9_Statelessness.tla`, model-checked by TLC 2.19
(`/home/tony/.local/lib/tla2tools.jar`). A `Verifier` constant selects
the decision rule; every other part of the state machine is shared,
so the correct verifier and its companions run over the **same**
state space with the **same** consult path available. This is what
"not stateless by construction" means here: the correct model
contains a reachable action that reads service state; statelessness
is a property of what the verdict *uses*, not of what the model
*can do*.

- **Bundle and policy** — the archived bundle abstracted, as in
  `formal/tla/P4_VerifierStates.tla`, to per-check outcomes
  `bundle ∈ [Checks → {pass, fail, unperformable}]`, with the declared
  policy `policy ⊆ Waivable`. Both are chosen at `Init` (every
  combination) and **never change** during a behavior: the vector's
  "same bundle and declared policy".
- **`PureVerdict`** — P4's verdict function transcribed verbatim: the
  verdict computed from bundle and policy **alone**. The P4 partition
  is P4's model's business (checked there, 11 invariants); it is
  copied here, not re-checked. Join: coverage-map row 10.
- **Service** — one optional external thing the verifier might touch:
  `service ∈ {authorized, revoked, unreachable}`, standing for any
  live dependency (Tessera's own service, a live revocation status, a
  live authority channel, a transparency log). `ServiceChange` moves
  it freely at any time, including between a consult and a decision.
  A configuration may restrict `ServiceStates` to `{unreachable}`
  — the service is dead throughout: §4.4's "verify with the service
  dead".
- **Consult** — an action any verifier kind may take during a run:
  `consulted := TRUE`, `view := service`. In the design this is the
  observability/log feed of A4.6 ("may feed a log and may never feed
  a verdict") and coverage-map row 14; the correct verifier is
  allowed to take it, and P9 says the verdict ignores what it read.
- **Machines and runs** — verification runs happen on machines
  `Machines`; each run is `StartRun(m) → [Consult] → Decide`, and
  appends a record `(machine, verdict, service-at-decision,
  consulted?)` to `verdicts`. `MaxRuns` bounds the count.
  `seen[m]` is machine-local memory that this bundle was verified on
  `m` before. `RepeatOnMachine` allows or forbids a second run on the
  same machine (the vector's "two isolated machines" are two *fresh*
  machines: `RepeatOnMachine = FALSE`).
- **Verifier kinds** (the `Verifier` constant):
  - `PURE` — the correct verifier: `Decide` yields `PureVerdict`,
    may or may not have consulted.
  - `LIVE_FALLBACK` — always consults; if the service says `revoked`
    the verdict is `INVALID`, otherwise `PureVerdict` (a live lookup
    that silently falls back to the archived evidence when the
    service is unreachable).
  - `LIVE_FAILCLOSED` — always consults; if the service is
    `unreachable` the verdict is `UNVERIFIABLE`, otherwise
    `PureVerdict` (fail-closed on a dead service — the "safe-looking"
    violation of §4.4).
  - `REPLAY_LATCH` — never needs to consult; if this machine has
    verified this bundle before, `INVALID`, otherwise `PureVerdict`
    (verifier-local history entering the verdict; A3 §A3.1.1 scopes
    replay to *caller policy*, which is why this is a violation).

**Invariants:**

- `Purity` — **the P9 invariant as commissioned**: every recorded
  verdict equals `PureVerdict`. (The verdict computed from bundle +
  policy alone; nothing about `service`, `view`, or `seen` appears in
  the right-hand side.)
- `Agreement` — **A4.1's vector, first clause**: all recorded verdicts
  are equal to one another. This invariant does not mention
  `PureVerdict`; it is the black-box, oracle-free form of the vector.

**Sanity witnesses** (`_Sanity` configurations, run with `-continue`;
a *violation* is the healthy result, P4 pattern): `NeverConsulted`
(the consult path is reachable), `NeverDecidedDead` (a verdict is
reached with the service unreachable — the dead-service test shape),
`NeverDecidedUnconsulted` (the pure verifier decides without
consulting), `NeverDecidedConsulted` (the pure verifier also decides
*after* consulting — the interesting witness), `NeverAllRuns`,
`NeverTwoMachines`, `NeverRepeatMachine` (must be violated in FULL,
must **hold** in VECTOR — fresh machines), `NeverValidStrict`.

**Configurations:**

- **FULL** — `Checks = {c1, c2}`, `NonWaivable = {c1}`,
  `Machines = {mA, mB}`, `ServiceStates = {authorized, revoked,
  unreachable}`, `MaxRuns = 2`, `RepeatOnMachine = TRUE`. The service
  is live and changing; runs may repeat on one machine or cross
  machines.
- **VECTOR** — as FULL but `ServiceStates = {unreachable}` and
  `RepeatOnMachine = FALSE`: two fresh machines, no network, one run
  each. This is the A4.1 vector's situation, modeled literally.

**Scope exclusions, named:** no adversary (P9 is a purity claim, not
a security claim; the symbolic suite owns adversaries); no bundle
contents beyond per-check outcomes; no temporal window or anchoring
(P5/P5c/bridge own those, and their own headers *assume* P9); no
wrapper layering (P7's "inner bytes travel inside the bundle, or P9's
self-containment fails" is a bundle-content claim this abstraction
cannot see); no model of *what* a verifier does with the log feed.

## Questions (frozen), with predictions

Outcome vocabulary is the registered three: **violation** (TLC
counterexample), **timeout** (mechanism failure — evidence about the
tool or encoding, never about the property), **termination** (holds
over the checked abstraction only). Timebox: 10 minutes per run
(`timeout 600`); expected seconds.

**Q1 — Correct verifier, FULL: `Purity` and `Agreement` hold.**
- Prediction: both hold, terminating (p ≈ 0.95; p ≈ 0.05 an encoding
  slip in the machine/run bookkeeping produces a spurious red,
  dispositioned by trace and recut as an encoding defect). **Expected
  finding on the branch that holds: the green is definitional** —
  `PURE`'s `Decide` *is* `PureVerdict`, so `Purity` reduces to
  `x = x` and `Agreement` to `x = x`. TLC exploring the service
  dynamics and consult interleavings adds no content to that; the
  content of the probe lives in Q2–Q5. Recording this is the point
  A4.1 made in advance, and it is recorded whether or not Q3–Q5 add
  anything.

**Q2 — Correct verifier, sanity: the consult path is reachable and
the dead-service verdict is reachable.**
- Prediction: `NeverConsulted`, `NeverDecidedConsulted`,
  `NeverDecidedUnconsulted`, `NeverDecidedDead`, `NeverAllRuns`,
  `NeverTwoMachines`, `NeverRepeatMachine`, `NeverValidStrict` all
  violated in FULL (p ≈ 0.9). In VECTOR: all violated except
  `NeverRepeatMachine`, which must hold (p ≈ 0.9). If `NeverConsulted`
  is **not** violated in the correct model, the correct model is
  stateless by construction in the trivial sense and the probe is
  theater; that would be recorded as outcome 3 for the probe design.

**Q3 — Companion `LIVE_FALLBACK`.**
- FULL: `Purity` **red** and `Agreement` **red**, with the trace
  passing through `Consult` with `view = revoked` (p ≈ 0.9; p ≈ 0.1
  encoding slip).
- VECTOR: `Purity` **green** and `Agreement` **green** (p ≈ 0.85).
  Reading if so: **the A4.1 vector, as worded, cannot detect a
  consulting verifier that falls back to the archived evidence when
  the service is unreachable** — on two machines with no network it
  behaves exactly like the pure verifier. Only a run with the service
  *reachable and contradicting the bundle*, or the inspection leg
  (A4.1 part (i)), sees it. If this branch lands it is a finding
  about the vector's design, of the "unrepresentable attack" kind,
  routed for disposition before exit.

**Q4 — Companion `LIVE_FAILCLOSED`.**
- FULL: `Purity` **red**, `Agreement` **red** (p ≈ 0.85; the
  `Agreement` red needs a `ServiceChange` between two runs, which
  the FULL configuration permits).
- VECTOR: `Purity` **red** but `Agreement` **green** (p ≈ 0.8):
  both machines return `UNVERIFIABLE`, agree with each other, and
  disagree with the verdict the bundle and policy determine. Reading
  if so: **the vector needs an expected-verdict oracle** — the
  "must yield the same verdict" clause alone passes a fail-closed
  consulting verifier; the vector must carry the verdict that
  bundle + policy determine (as any conformance vector carries its
  expected output) to fail it. Same routing as Q3 if it lands.

**Q5 — Companion `REPLAY_LATCH`.**
- FULL: `Purity` **red**, `Agreement` **red**, the trace showing a
  second run on the same machine (p ≈ 0.9).
- VECTOR: both **green** (p ≈ 0.85): two fresh machines never
  exercise the latch. Reading if so: verifier-local history is
  outside what the two-machine vector observes; a "verify twice on
  one machine" case would see it. Routed with Q3/Q4.

**Q6 — Shape check on the consulting companions.** In `LIVE_*`
sanity runs, `NeverConsulted` and `NeverDecidedConsulted` are
violated (the consulting path is exercised on the way to a verdict)
and `NeverDecidedUnconsulted` **holds** (those companions never decide
without consulting) (p ≈ 0.9). This is the "sanity witness that the
consulting path is reachable in the companion" the commission asked
for.

## Three named outcomes (declared before building)

1. **Shape established, green trivial.** Q1 green and definitional;
   Q2 witnesses fire; Q3–Q5 companions red on `Purity` in FULL;
   the VECTOR column shows which companions the A4.1 vector catches.
   Reading: the probe found nothing against P9 (green is not
   evidence, per A4.1) and produced a statement of what a P9 model
   can and cannot show plus, if the VECTOR predictions land, a
   finding about the vector's coverage to disposition before exit.
2. **Probe finding.** A companion the invariant cannot make red (the
   invariant is not discriminating), or a red in the correct model
   that survives trace inspection (an actual P9 defect at this
   abstraction — an amendment trigger, not a recut), or the VECTOR
   column differing from prediction in a direction that changes what
   the vector is for.
3. **Expressiveness failure.** A timeout, or the questions cannot be
   posed to the fixture. Evidence about the probe, not about P9;
   record and stop.

## Discipline

- Every result in `RESULTS-PROBE.md` is labeled
  `PROBE — NON-DISCHARGING`; both files carry the asymmetric use rule
  in their header.
- Companion runs use `-continue` so that both `Purity` and
  `Agreement` are reported independently; their outputs pass through
  `scripts/filter-tlc-output.sh`. Correct-model main runs do not use
  `-continue` (a green is a clean termination); sanity runs do.
- `.out` files are committed beside the `.cfg` files that produced
  them; the full TLC output reproduces from `.tla` + `.cfg`.
- Nothing here changes `PROPERTIES.md` or `COVERAGE-MAP.md`. A
  finding is routed to the author for disposition; a green is filed
  and not cited.
- Amend-don't-rewrite applies to this file from its first commit.

## Provenance

Drafted by the AI collaborator (Claude, Fable 5.1) 2026-09-06 from
Amendment 4 §A4.1, the standing probe's declaration form, and
`P4_VerifierStates.tla` (whose header already carries P9 as a
premise). The choice of the three companion kinds and the two
configurations is the collaborator's, on the record as such; the
author decides what, if anything, a finding here changes.
