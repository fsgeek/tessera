# P9 statelessness — non-discharging TLA+ probe: predictions vs. observed

**STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not
adopted; the commit is the author's.**

**PROBE — NON-DISCHARGING.** Commissioned by Amendment 4 §A4.1 under
the design-probe tier (`docs/reviews/2026-08-29-design-probe-ruling.md`).
*Note 2026-09-06 (after skeptic review):* PROBE.md line 7 calls
Amendment 4 "signed `5188e7a`"; that overstates. Amendment 4 is
committed at `5188e7a` and stamped at `5dfd82b`; its own status line
reads "adopted in session, not yet signed"; whether it is in force is
the author's to state. PROBE.md is left as written — see the review
log for why the correction is recorded here and not appended there.
*Extension 2026-09-06 (third skeptic round):* the same applies to
PROBE.md line 29 ("The author ruled the probe be built anyway"), which
paraphrases A4.1's "Optional TLA+ probes, non-discharging — RULED
(author)" and quotes the author's words from that section; the ruling
is quoted from a document whose own status line reads "not yet
signed", so the reliance at line 29 rests on the same status as the
word "signed" at line 7.
**Asymmetric use rule (A4.1):** *a green result is not evidence and is
not cited by any tracker row; a red result or an unrepresentable-attack
finding is a finding to be dispositioned before exit.* Nothing here
moves any row of `formal/PROPERTIES.md` or any cell of
`formal/COVERAGE-MAP.md`; P9's discharge path remains
**[inspection + vector]**. Predictions were frozen in `PROBE.md`
before the first run; this file records observed outcomes against
them, one tool finding, three findings about the A4.1 vector's
coverage, and the plain-language reading aid.

**Tooling.** TLC as shipped in `/home/tony/.local/lib/tla2tools.jar`,
which reports itself as `TLC2 Version 2026.07.31.184830 (rev: 30cc360)`
— not the `2.19` PROBE.md named from the repository's older committed
outputs; a tooling fact, not a prediction. Every run:
`timeout 600 java -XX:+UseParallelGC -jar tla2tools.jar -config <cfg>
-workers 4 P9_Statelessness.tla` (sanity runs add `-continue` and pass
through `scripts/filter-tlc-output.sh`; the run-2 companion runs do
not — a deviation from PROBE.md's Discipline, recorded in the next
section). Registered timebox 10 min per run; every run finished in
≤ 4 s. Largest state space: 22,518 distinct states (FULL
configuration: `Pure_Full.out`, `Pure_Full_Sanity.out`,
`Pure_Full_Sanity2.out`; REPLAY_LATCH FULL reaches the same count only
in `run1-shadowed/P9_Statelessness_ReplayLatch_Full.out`, run with
`-continue`; the run-2 REPLAY_LATCH outputs stop at 1,178/1,179 states
on the first violation). One module; twenty configurations from run 2
and five from run 3 (single-invariant "holds" checks, below),
twenty-five `.out` files, all in this directory; run 1's nine
superseded configurations and outputs are preserved under
`run1-shadowed/` (see F-T1).
*Correction 2026-09-06 (third skeptic round):* "twenty configurations
from run 2" above is wrong; run 2 was **eighteen** runs (`Starting`
timestamps 18:34:23–18:34:48 in the `.out` files). `Pure_Full.out`
(18:31:36) and `Pure_Vector.out` (18:31:55), with their cfgs (18:31:29),
are run-1 artifacts retained unchanged because the `PURE` main runs
list only `TypeOK`, `Purity`, `Agreement`, none violated, so there was
no shadowing to fix. Twenty-five `.cfg`/`.out` pairs: 2 (run 1,
retained) + 18 (run 2) + 5 (run 3).

## Run 1 was a witness-shadowing failure, preserved

The first pass listed `Purity` and `Agreement` in one cfg per
companion, and all eight sanity witnesses in one cfg, each run with
`-continue`. Every companion output reported `Purity` violated and
said nothing about `Agreement`; the sanity outputs reported at most
four of eight witnesses. Cause (F-T1 below): TLC reports **one**
violated invariant per violating state — the first in cfg order — and
`-continue` does not revisit the others. `Agreement` can be violated
only in a state where some verdict differs from another, which also
violates `Purity`, listed before it; `NeverAllRuns` (two runs done) is
violated only in states that also violate a run-record witness listed
above it. Run 2 gives each companion invariant its own cfg and splits
the witnesses into two ordered lists (`_Sanity`: `NeverValidStrict`,
`NeverRepeatMachine`, `NeverTwoMachines`, `NeverDecidedDead`,
`NeverConsulted`; `_Sanity2`: `NeverAllRuns`,
`NeverDecidedUnconsulted`, `NeverDecidedConsulted`), each entry placed
where some state violates it and none listed above it. The `.tla`
module was not changed between runs; only cfg composition was. This
is an encoding change to the *checking arrangement*, not to any
prediction — PROBE.md named a single `_Sanity` cfg and is left as
written.

**Deviation from PROBE.md Discipline (lines 244–247), recorded
2026-09-06 after skeptic review.** Run-2 companion runs (`*_Full.out`,
`*_Vector.out`, `*_Agreement.out` for the three companions) do not use
`-continue` or the filter, because each cfg lists one invariant of
interest and a single violation is the whole result; run 1
(`run1-shadowed/`) did use both. The `P9_Statelessness_TTrace_*` files
TLC wrote alongside the run-2 companion runs were not kept; the `.out`
lines naming them are TLC's, not a citation. The same holds for run 3's
`states/` scratch directory (empty, removed).
*Note 2026-09-06 (third skeptic round):* PROBE.md Discipline (line 241)
says every result in this file is labeled `PROBE — NON-DISCHARGING`.
The label appears once, at line 6, and is read as governing every
entry in this file — the predictions-vs-observed table, F1–F4, F-T1,
the routed options, the reading aid, and the review log; no row or
finding carries it individually.

## Run 3 — single-invariant "holds" checks (2026-09-06, after skeptic review)

Two of the table's "holds" claims — `NeverRepeatMachine` in VECTOR
(Q2) and `NeverDecidedUnconsulted` for the consulting companions
(Q6) — were inferred in run 2 from silence inside a multi-witness
list, the inference F-T1 warns against. The inference is sound here
(in VECTOR a state violating `NeverRepeatMachine` with no `VALID_STRICT`
verdict satisfies `NeverValidStrict`, the only entry above it, and
would be reported as `NeverRepeatMachine`; in `_Sanity2` any `cons = FALSE` record violates `NeverAllRuns`
at length 1 and is reported), but F-T1's own remedy is one cfg each,
so run 3 adds five configurations, module unchanged:
`Pure_Vector_RepeatMachine` (green, 450 states — clean termination),
`LiveFallback_DecidedUnconsulted` (green, 14,562 states),
`LiveFailclosed_DecidedUnconsulted` (green, 15,498 states), and, because
PROBE.md Q6 says `LIVE_*` and run 2 ran the sanity lists for
`LIVE_FALLBACK` only, `LiveFailclosed_Sanity` / `_Sanity2` (with
`-continue` and the filter: `NeverConsulted`, `NeverDecidedDead`,
`NeverValidStrict`, `NeverTwoMachines`, `NeverRepeatMachine`,
`NeverDecidedConsulted`, `NeverAllRuns` violated; `NeverDecidedUnconsulted`
silent, now backed by its own cfg). No prediction or outcome changes;
the Q2 and Q6 rows below cite the new files.

*Correction 2026-09-06 (third skeptic round; amend-don't-rewrite, the
sentence above is left as written):* the `_Sanity2` half of the
parenthetical soundness argument is misstated. `NeverAllRuns ==
Len(verdicts) < MaxRuns` (module line 235); a state with one
`cons = FALSE` record has `Len(verdicts) = 1 < MaxRuns = 2` and so
**satisfies** `NeverAllRuns` rather than violating it. TLC therefore
reaches `NeverDecidedUnconsulted`, listed second in `_Sanity2`, and
would report it if violated — which is why its silence in
`LiveFallback_Sanity2.out` was sound. The conclusion stands; it is
backed directly by the run-3 single-invariant cfgs
(`LiveFallback_DecidedUnconsulted.out`,
`LiveFailclosed_DecidedUnconsulted.out`, both green), not by the
argument as originally written.

## Predictions vs. observed

Outcome vocabulary: **violation** / **timeout** / **termination**.
"Red" = violation, "green" = termination with no error. Every run
terminated; no timeouts.

| Q | Kind · configuration | Predicted (frozen) | Observed | Outcome |
|---|---|---|---|---|
| Q1 | `PURE` · FULL | `Purity`, `Agreement` hold (0.95); green is definitional | **green**, 22,518 states (`Pure_Full.out`); `Pure_Vector.out` also green, 450 states | as predicted — **and definitional** (F1) |
| Q2 | `PURE` · FULL sanity | all eight witnesses violated (0.9) | **all eight violated** (`Pure_Full_Sanity.out`, `_Sanity2.out`): consult path reachable; a verdict reached with the service unreachable; the pure verifier decides both without and *after* consulting | as predicted |
| Q2 | `PURE` · VECTOR sanity | all violated except `NeverRepeatMachine`, which holds (0.9) | **seven violated; `NeverRepeatMachine` holds** (`Pure_Vector_Sanity.out`, `_Sanity2.out`; the hold is a clean single-invariant termination in `Pure_Vector_RepeatMachine.out`, run 3) | as predicted — fresh machines confirmed |
| Q3 | `LIVE_FALLBACK` · FULL | `Purity` red, `Agreement` red, trace through `Consult` with `view = revoked` (0.9) | **both red** (`LiveFallback_Full.out` depth 4: `Consult` reads `revoked`, `Decide` → `INVALID` on an all-pass strict bundle; `_Full_Agreement.out` depth 8: run 1 with service unreachable → `VALID_STRICT`, `ServiceChange` to `revoked`, run 2 → `INVALID`) | as predicted |
| Q3 | `LIVE_FALLBACK` · VECTOR | both green (0.85) — the vector cannot see this class | **both green** (`LiveFallback_Vector.out`, `_Vector_Agreement.out`, 234 states each) | as predicted — **F2** |
| Q4 | `LIVE_FAILCLOSED` · FULL | both red (0.85) | **both red** (`LiveFailclosed_Full.out`; `_Full_Agreement.out` depth 8: `VALID_DEGRADED` then, after the service dies, `UNVERIFIABLE`) | as predicted |
| Q4 | `LIVE_FAILCLOSED` · VECTOR | `Purity` red, `Agreement` green (0.8) | **`Purity` red** (`LiveFailclosed_Vector.out` depth 4: bundle determines `INVALID`, verifier returns `UNVERIFIABLE`); **`Agreement` green** (`_Vector_Agreement.out`) | as predicted — **F3** |
| Q5 | `REPLAY_LATCH` · FULL | both red, second run on the same machine (0.9) | **both red** (`ReplayLatch_Full.out` depth 5: `mA` twice, `VALID_STRICT` then `INVALID`; `_Full_Agreement.out`) | as predicted |
| Q5 | `REPLAY_LATCH` · VECTOR | both green (0.85) | **both green** (`ReplayLatch_Vector.out`, `_Vector_Agreement.out`) | as predicted — **F4** |
| Q6 | `LIVE_*` · sanity | `NeverConsulted`, `NeverDecidedConsulted` violated; `NeverDecidedUnconsulted` holds (0.9) | **as stated** for `LIVE_FALLBACK` (`LiveFallback_Sanity.out`, `_Sanity2.out`; hold confirmed alone in `LiveFallback_DecidedUnconsulted.out`, run 3) and for `LIVE_FAILCLOSED` (`LiveFailclosed_Sanity.out`, `_Sanity2.out`, `LiveFailclosed_DecidedUnconsulted.out`, all run 3 — run 2 had covered `LIVE_FALLBACK` only): neither companion decides without consulting; the consulting path is on every path to its verdict | as predicted |

**Outcome classification (declared vocabulary): outcome 1 — shape
established, green trivial**, with the three VECTOR-column findings
(F2–F4) landing on their predicted branches. Per PROBE.md's outcome 1
text and A4.1: the green is filed and not cited; F2–F4 are routed
below for the author's disposition. No finding is against P9 itself.

## Findings

**F1 — The correct model's green is definitional, exactly as A4.1
predicted; here is what the probe shows instead.** `PURE`'s `Decide`
appends `PureVerdict`; `Purity` asks whether each appended verdict
equals `PureVerdict`; `Agreement` asks whether values all equal to one
thing equal each other. TLC's exploration of 22,518 states over
service dynamics, consult interleavings, and two machines adds no
content to `x = x`. The probe is not theater only because the *same*
state space carries three verifiers that are not pure, and the
invariant separates them (Q3–Q5 FULL: all six reds). So the honest
sentence for what a P9 model can show is: **the invariant is
discriminating over the stateful-verifier classes one chooses to
write down, and nothing about the reference verifier.** Whether the
reference verifier is `PURE` is a fact about its code, which is why
A4.1 discharges P9 by inspection plus vector. Two witnesses are worth
keeping as the dead-service demonstration's shape (A3 §A3.5
"dead-service test"): `NeverDecidedDead` — a `VALID_DEGRADED` verdict
reached with `service = unreachable` and no consult
(`Pure_Full_Sanity.out`); and `NeverDecidedConsulted` — the pure
verifier reads `revoked` from the service and returns `VALID_STRICT`
anyway (`Pure_Full_Sanity2.out`): the log feed of A4 §A4.6 read and
ignored, in one state.

**F2 — The A4.1 vector, as worded, cannot detect a consulting verifier
that falls back to the archived evidence when the service is
unreachable.** (Q3 VECTOR, predicted branch.) `LIVE_FALLBACK` is the
soft-fail pattern — "check online if you can, otherwise proceed" — and
on two isolated machines with no network it is indistinguishable from
`PURE`: both invariants green, 234 states. The clause "a verifier that
consults any optional service must fail the vector" is therefore not
delivered by the clause before it for this class. What does see it:
a run with the service **reachable and contradicting the bundle**
(FULL: `Purity` red at depth 4), or the inspection leg (A4.1 part (i),
the input enumeration re-checked against the reference verifier at
H1a). Classification: an *unrepresentable-attack* finding in A4.1's
sense — the vector cannot represent this violation — offered as the
collaborator's reading; whether it is one is the author's call.

**F3 — The vector's agreement clause passes a fail-closed consulting
verifier; the vector needs its expected verdict.** (Q4 VECTOR,
predicted branch.) `LIVE_FAILCLOSED` returns `UNVERIFIABLE` on both
machines when the service is dead: they agree with each other
(`Agreement` green) and disagree with what the bundle and policy
determine (`Purity` red — the trace has a bundle that determines
`INVALID` reported as `UNVERIFIABLE`). §4.4's hard rule is violated by
a verifier that is fail-closed and looks safe. The two-machine vector
catches it only if the vector carries the verdict that bundle + policy
determine — the oracle every conformance vector carries anyway — and
compares each machine to *that*, not only to the other machine.

**F4 — Verifier-local history is outside what two fresh machines
observe.** (Q5 VECTOR, predicted branch.) `REPLAY_LATCH` turns a second
presentation of the same bundle on one machine into `INVALID`; the
vector's two fresh machines never present twice, so both invariants
are green. A "verify the same bundle twice on one machine, expect the
same verdict" case would see it (FULL: red at depth 5). A3 §A3.1.1
scopes replay handling to *caller policy*, so this class is a P9
violation even though its intent is benign.

**F-T1 — Tool: TLC reports one violated invariant per state.** With
`-continue`, an invariant listed after another that the same states
violate is never reported; silence is not unreachability. Consequence
for this project's `_Sanity` pattern (P4, P5c, bridge): a witness list
is sound only if each entry has a state that violates it and none
listed above it. P4's four witnesses are mutually exclusive by
construction (one verdict per state), so the existing runs are not
affected; this probe's were not. Suite note offered for the TLA+ side,
parallel to S-P3's recut-1 note for ProVerif judges: **order witness
lists so each has an exclusive firing state, or give each its own cfg;
record which.** Evidence: `run1-shadowed/` (nine `.out` files), and
run 2's identical distinct-state counts under the split lists.
*Note 2026-09-06 (third skeptic round):* the "existing runs are not
affected" sentence above argues from mutual exclusivity, which holds
only for P4; the P5c, bridge, BridgeSlack, BridgeSlack_Latch, and P5P6
lists are not mutually exclusive by construction (e.g. P5c lists
`ShipUnreachable` after `ReorgShipUnreachable` / `ReissueShipUnreachable`).
The claim rests instead on a direct check, made by the skeptic and
repeated by the AI collaborator 2026-09-06: every witness listed in
each of the six `formal/tla/*_Sanity.cfg` files is reported as
violated in its `.out` (P4 4/4, P5c 7/7, Bridge 6/6, BridgeSlack_Latch
2/2, BridgeSlack 4/4, P5P6 4/4). True, but for the empirical reason,
not the structural one.

## What the probe routes (PROPOSED; the author decides)

A4.1's rule says a red or unrepresentable-attack finding is
dispositioned before exit. F2–F4 are findings about the **discharge
vector's coverage**, not about P9's truth. Options the record could
take, none selected here:

1. **Accept as scoped.** The two-machine no-network vector is the
   dead-service demonstration (A3 §A3.5) and catches `LIVE_FAILCLOSED`
   given F3's oracle; the inspection leg (A4.1 part (i)) carries the
   `LIVE_FALLBACK` and `REPLAY_LATCH` classes. Record that division in
   the H1a vector's description so no reader thinks the vector alone
   discharges P9.
2. **Extend the H1a vector set** with two cases the FULL configuration
   exhibits: (a) *service reachable and contradicting the bundle* — a
   stub service answering `revoked` (or anything) for a bundle whose
   archived evidence determines a valid verdict; the verdict must be
   unchanged; (b) *same bundle verified twice on one machine*; verdicts
   must be equal. Both are cheap and black-box.
3. **State the oracle** (F3) in the vector's text regardless of 1 or 2:
   "must yield the same verdict, **and that verdict is the one the
   bundle and declared policy determine**."
4. **Detect the network attempt itself** in the no-network vector (the
   model's `cons` field, `Decide` line 167; `NeverDecidedConsulted`
   fires for `LIVE_FALLBACK` in `LiveFallback_Sanity2.out` line 20).
   Not offered as a discriminator because A4 §A4.6 permits a pure
   verifier to attempt the observability feed ("may feed a log and may
   never feed a verdict"); it separates consulting from non-consulting
   verifiers, not pure from impure.

Any of these is an H1a-track note or a clarification of A4.1's
wording; none weakens a property, and the collaborator does not read
any as needing an amendment. That reading is routed, not decided.

## Reading aid (testimony, not a gate — ENUMERATION note 5 item 2)

**Typing note.** TLA+ is untyped; `TypeOK` is the only place the
shapes are stated and TLC checks it as an invariant. `TypeOK` is
exhaustively green in `Pure_Full.out` and `Pure_Vector.out` and in the
run-1 companion outputs under `run1-shadowed/` (full exploration with
`-continue`); in the run-2 companion runs, which list it before
`Purity` and stop at the first `Purity` violation, it is green over the
prefix explored before that violation (301, 94, 1,178 states). `bundle` is a function from check names to
one of three strings; `policy` is a set of check names; `verdicts` is
a sequence of records with four fields; model values `c1`, `c2`, `mA`,
`mB` are opaque names supplied by the cfg. String constants
(`"PURE"`, service states) are compared by equality only.

**Cast.** Line numbers refer to `P9_Statelessness.tla`.

| Name | What it stands for in the design | Built | Consumed |
|---|---|---|---|
| `bundle`, `policy` | the archived bundle (abstracted to per-check outcomes, as P4 does) and the declared policy; "the same bundle and declared policy" of the vector | `Init` 128–129, never changed | `PureVerdict` 103–110 |
| `PureVerdict` | the verdict bundle + policy determine — P4's function, transcribed | 103–110 | `Rule` 115; `Purity` 219 |
| `service` | any live thing a verifier might touch: Tessera itself, a revocation status, a live authority channel, a log | `Init` 130; `ServiceChange` 175–177 | `Consult` 158 |
| `Consult`, `consulted`, `view` | the verifier's toolchain reading the service — A4 §A4.6's log feed, coverage-map row 14 | 154–159 | `Rule` 116–117 (companions only); witnesses |
| `Machines`, `machine`, `seen` | the isolated machines of the vector; per-machine memory of having verified this bundle | `StartRun` 140–148; `Decide` 168 | `Rule` 118 (`REPLAY_LATCH` only); `StartRun` 143 |
| `verdicts` | the record of completed runs: machine, verdict, service state at decision, consulted? | `Decide` 166–167 | every invariant |
| `Verifier`, `Rule` | which decision rule this configuration checks: the correct one or a companion | cfg; 114–118 | `Decide` 167 |
| `Purity` | the P9 invariant as commissioned | 218–219 | main cfgs |
| `Agreement` | A4.1's vector, first clause, oracle-free | 223–224 | `_Agreement` cfgs |

**Checks table.** Which parts carry the result, and which are carried
for other purposes (S-P3 F7 pattern):

| Check / element | LOAD-BEARING for | CARRIED |
|---|---|---|
| `Purity` | Q3–Q5 reds; F2, F3 | — |
| `Agreement` | F3 (its green against `Purity`'s red is the finding) | — |
| `Consult` reachable in `PURE` | the model not being stateless by construction (Q2) | — |
| `ServiceChange` between runs | `Agreement` reds in FULL | — |
| `RepeatOnMachine` | F4 | — |
| `PureVerdict`'s partition | — | P4's (checked in `P4_VerifierStates.tla`; copied here) |
| `TypeOK` | — | bookkeeping |
| Deadlock check (`Done`) | — | bookkeeping |

**Plain-language claim.** *Over this model, a verifier whose decision
rule reads only the bundle and the declared policy produces the same
verdict on every machine and under every history of the service,
including a dead one; three verifiers whose rules read the service, or
the machine's memory, do not, and the P9 invariant separates them.*

**Plain-language adversary.** None. P9 is a purity claim; there is no
attacker here, only a changing environment (the service) and a
possibly stateful verifier. The symbolic suite owns adversaries.

**Plain-language boundary.** The model says nothing about whether
Tessera's reference verifier is the pure one — that is inspection's
job (A4.1 part (i)) — and nothing about bundle contents, temporal
anchoring, wrapper self-containment (P7), or what the log feed is
used for. Its green is not evidence (A4.1). What it shows is which
stateful-verifier classes the two-machine no-network vector can and
cannot see (F2–F4), and that the vector needs its expected verdict
(F3).

## Boundaries of this evidence

Two checks, one waivable; three service states; two machines; two
runs per behavior; a transcribed rather than re-checked verdict
function; no adversary; no bundle structure. Every green here is
about the checking arrangement; none of it will be carried into Phase
1a, cited by a tracker row, or read as P9 evidence. The companions are
the collaborator's choice of three stateful classes and are not a
taxonomy of all the ways a verifier can be stateful.

## Review log

- 2026-09-06 — PROBE.md written and frozen before any run; module and
  configurations built; run 1 showed witness shadowing (F-T1), nine
  files preserved under `run1-shadowed/`; run 2 with split
  configurations, all twenty runs terminated in ≤ 4 s, every
  predicted branch landed; this file written from the `.out` files in
  this directory (uncommitted; the commit is the author's) by the AI
  collaborator. No author read yet.
- 2026-09-06 — skeptic review (a separate AI reviewer, verified
  findings; four record-accuracy defects, four nits, no result
  disputed) applied by the AI collaborator: the "signed" correction
  above; the `-continue`/filter deviation and the discarded TTrace
  files recorded; the 22,518 REPLAY_LATCH attribution corrected to
  `run1-shadowed/`; the `TypeOK` prefix-only note; run 3's five
  single-invariant / `LIVE_FAILCLOSED` sanity cfgs run and cited;
  routing option 4 added; "committed" corrected. **Freeze:** PROBE.md,
  the module, every cfg/out, and this file are untracked together, so
  a single author commit cannot carry the committing order the
  design-probe ruling names as the freeze. The freeze rests on session
  order and file modification times (PROBE.md 18:30 < module 18:31 <
  first TLC start 18:31:36 in `Pure_Full.out` < this file 18:37), not
  on commit order; PROBE.md's stale details (TLC "2.19", a single
  `_Sanity` cfg, companion `-continue`) are left uncorrected as
  evidence it was not revised after the runs, and the skeptic's
  "signed" correction is recorded here rather than appended to PROBE.md
  for the same reason — an append would move its modification time
  past every run. Recommended to the author (the standing probe's
  precedent, `424934d` then `3f46f85`): commit PROBE.md alone first,
  the rest of the directory second; the "signed" note can then be
  appended to PROBE.md in the second commit as a dated note. Module
  unchanged throughout; no prediction revised.
- 2026-09-06 (later, ~19:15) — second-instance verification by the AI
  collaborator (a fresh session given the same A4.1 commission; it found
  this directory already built and verified rather than rebuilt).
  Checked: (a) every commission element is present — the `consulted`
  variable and `Consult` action reading `service` (module 154–159), the
  P9 invariant as "verdict = verdict from bundle + policy alone"
  (`Purity`, 218–219), companions whose verdict reads what was consulted
  (`Rule`, 116–117), the PURE verifier's consult path shown reachable
  (Q2, `NeverConsulted` / `NeverDecidedConsulted` violated in
  `Pure_Full_Sanity*.out`), the companions' consulting path shown to lie
  on every path to their verdict (Q6), the trivial-green finding (F1),
  the asymmetric use rule and PROPOSED status in both file headers and
  the module header; (b) the traces cited in the table and in F1–F4
  against the `.out` files (`LiveFallback_Full` depth 4, `view =
  "revoked"` → `INVALID` on an all-pass strict bundle;
  `LiveFailclosed_Vector` depth 4, bundle `c2 = "fail"`, policy `{}` →
  `UNVERIFIABLE` where `PureVerdict` is `INVALID`; `ReplayLatch_Full`
  depth 5, `mA` twice; both `_Full_Agreement` traces via `ServiceChange`
  between runs; `Pure_Full_Sanity` `NeverDecidedDead` = `VALID_DEGRADED`
  at `service = "unreachable"`, `cons = FALSE`; `Pure_Full_Sanity2`
  `NeverDecidedConsulted` = `VALID_STRICT` after reading `"revoked"`;
  `LiveFallback_Sanity2.out` line 20) — all as stated; (c) every module
  line number in the cast table — all correct; (d) independent
  reproduction of eight configurations (`Pure_Full`, `Pure_Full_Sanity`
  with `-continue` and the filter, `Pure_Vector_RepeatMachine`,
  `LiveFallback_Vector`, `LiveFallback_DecidedUnconsulted`,
  `LiveFailclosed_Vector`, `LiveFailclosed_Vector_Agreement`,
  `ReplayLatch_Full`) from copies of the module and cfgs in a scratch
  directory, same jar, `timeout 600`, each ≤ 4 s: identical violated
  invariants and identical distinct-state counts in every full
  exploration; the `ReplayLatch_Full` red stopped at 1,179 states
  against the recorded 1,178. **Tool note, small:** with `-workers 4`
  and no `-continue`, the distinct-state count printed at a first
  violation is worker-timing dependent and is not a reproducibility
  check; only full explorations (greens, and `-continue` runs) have a
  stable count. The reproduction outputs were not added to this
  directory, so the file set stays exactly what the skeptic review saw;
  the module and PROBE.md were not touched. No prediction, outcome, or
  finding changes; this entry is the only edit.
- 2026-09-06 (third skeptic round) — a further skeptic pass returned one
  defect and five nits, no result disputed; applied by the AI
  collaborator as dated notes, nothing rewritten: (1) the `_Sanity2`
  soundness argument in the run-3 section corrected (`NeverAllRuns`
  holds, not fails, at length 1; the conclusion stands on the run-3
  cfgs); (2) run 2 was eighteen runs, not twenty — the first review-log
  entry's "all twenty runs" and the Tooling paragraph's "twenty
  configurations from run 2" are both corrected by the note under
  Tooling (25 files = 2 + 18 + 5); (3) the header label is recorded as
  governing every entry; (4) the "signed" note extended to PROBE.md
  line 29; (5) F-T1's "not affected" claim re-based on the direct check
  of the six `formal/tla/*_Sanity` outputs. (6) The skeptic's freeze
  item is an author action (commit PROBE.md alone first, then the rest)
  already recommended in the entry above; no file change. No module,
  cfg, or `.out` touched; PROBE.md untouched; no prediction, outcome, or
  finding changes.
