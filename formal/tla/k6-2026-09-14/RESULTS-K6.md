# Confirmation depth at the registered parameter — k = 6 (`DepthK = 5`) re-runs, 2026-09-14

> **STATUS: PROPOSED — produced by the AI collaborator (owner instance,
> Claude Fable 5.1) on 2026-09-14; not adopted; the commit is the
> author's.** This discharges, or reports on, `formal/BAND0-EXIT.md`
> item E18 (Amendment 7 §A7.8, signed `9863513`): "either (a) the P5c,
> P5P6 and bridge modules re-run at `DepthK = 5` with `MaxTime` and the
> other bounds sized so that every registered witness still fires, or
> (b) a written argument … that every checked invariant is independent
> of the value of `DepthK`". This is path (a). No committed module or
> configuration is edited; every run here uses a copy of the committed
> `.tla` and a derived `.cfg` kept beside its `.out` in this directory.
> Every `.out` was produced by TLC 2026.07.31 with `-deadlock` (as the
> committed runs are, since the models stop at `MaxTime` by design);
> vacuity runs used `-continue` and `scripts/filter-tlc-output.sh`.

## 1. P5c issuance protocol (`P5c_IssuanceProtocol.tla`, unchanged)

**What changed between instances.** Only constants. The committed
instance is `MaxTime = 14, Delta = 3, DepthK = 2, MaxAttempts = 3`
(k = 3). `DepthK = 5` is k = 6 (`DepthK = k − 1`, A2 §A2.1).

**Finding first: the window must exceed the depth, or shipping is
unreachable in the instance.** `Ship` requires `depth >= DepthK` and
`now <= declared + Delta` together (module lines 260–263); depth
grows by at most one per `Tick`, so an instance with `Delta < DepthK`
cannot ship at all. This is a property of the finite instance, not of
the protocol: the registered parameters have δ = 72 h against six
confirmations of roughly an hour, so δ ≫ k there. The reading aid's
item 20 recorded that `DepthK = 2` is not the registered default; it
did not record that raising `DepthK` alone breaks the instance. The
two runs below show it.

| Instance | Main cfg (six invariants + `RefusalLatched`) | Sanity cfg (seven witnesses must all fire) | Evidence at k = 6? |
|---|---|---|---|
| `Delta = 3, MaxTime = 17, DepthK = 5` (`P5c_k6_d3.*`) | green, 3387 distinct states | **only four fire**: `RefusalUnreachable`, `RefusalWithLiveAnchorUnreachable`, `RefusalBuriedAnchorUnreachable`, `RefusalAfterReorgUnreachable`. `ShipUnreachable`, `ReissueShipUnreachable`, `ReorgShipUnreachable` **survive**: no state ships | **No.** `NoShippedOrphan`, `ShippedIsSound`, `ExpiredCannotShip` hold vacuously. Recorded as the negative control for the bound |
| `Delta = 6, MaxTime = 26, DepthK = 5` (`P5c_k6_d6.*`) | green, 9099 distinct states, 16363 generated, 0 on queue | **all seven fire** (one violation block each in the filtered `.out`) | **Yes.** |

`MaxTime = 26` is the module's own rule, `MaxAttempts · (Delta + 1) +
DepthK = 3 · 7 + 5`, applied at the new constants (module header lines
93–97; the committed 14 is the same rule at `Delta = 3, DepthK = 2`).

**Companions at the k = 6 instance** (`Delta = 6, MaxTime = 26, DepthK = 5`):

| Companion | Registered expectation | Observed |
|---|---|---|
| `P5c_IssuanceProtocol_Broken` (`_Broken_k6.*`) | red on `NoShippedOrphan` | red on `NoShippedOrphan` (first violation at 172 distinct states). *Correction 2026-09-14 (Codex qualification (b)):* the run stops at the first violation, and the `_Broken` module defines only `NoShippedOrphan` (its committed cfg lists that one invariant), so "red on exactly" is not a claim this companion can make or the committed record makes; "red on the one invariant it carries" is the statement |
| `P5c_IssuanceProtocol_BrokenSilent` (`_BrokenSilent_k6.*`) | red on `NoSilentDeadlock` | red on exactly `NoSilentDeadlock` (3857 distinct states at the violation) |
| `P5c_IssuanceProtocol_BrokenSilent_Green` (`_BrokenSilent_Green_k6.*`) | green on the other invariants | green, 11031 distinct states, 0 on queue |

**What this establishes.** P5c's six invariants and its action property
hold at the registered depth in an instance where every registered
witness is reachable; `_Broken` fails the one invariant it defines and
`_BrokenSilent` fails `NoSilentDeadlock` with its `_Green` set holding
("exactly" is a claim only where a companion carries more than one
invariant; Codex 2026-09-15). It establishes nothing about values of
`DepthK` other than 2 and 5, and nothing about `Delta` values other
than 3 and 6; the observation that the instance needs `Delta ≥ DepthK`
for shipping to be reachable is a constraint on future instances and
is entered on the reading aid.

## 2. P5P6 temporal revocation (`P5P6_TemporalRevocation.tla`)

Not re-run: the module has no `DepthK`, `KConf` or k constant
(`P5P6_TemporalRevocation.cfg`: `MaxTime, DeltaMax, EpsilonMax,
RcptTolMax`). Confirmation depth enters the verifier side only through
the bridge's `VerifierDesignatedH(h) == h + KConf − 1`. E18's mention
of P5P6 is therefore discharged by inspection: there is no parameter
to re-run.

## 3. P5c ↔ P5P6 bridge (`P5cP5P6_Bridge.tla`, unchanged)

**Committed instance:** `MaxTime = 6, Delta = 2, Epsilon = 1, KConf = 3,
DepthK = 2, MaxSkew = 2, MaxBlocks = 4` (456k states, green on four
invariants). `KConf` is Bitcoin-convention k; `PinAgreement` checks
`DepthK = KConf − 1`.

**Instance 1 — `KConf = 6, DepthK = 5, MaxBlocks = 7, MaxTime = 9`,
skew unchanged (`Bridge_k6_skew2.*`): did not close.** `MaxBlocks = 7`
is the committed rule "anchor plus full burial plus one spare"
applied at `DepthK = 5`; `MaxTime = 9` gives the chain room to bury.
TLC (`-deadlock`, 4 workers, 8 GB heap) reached 461,093,539 generated /
329,323,231 distinct states with 112,059,215 still queued when the
600-second run limit killed it; no invariant violation was reported in
the explored prefix, which is **not evidence** (the search is
breadth-first and incomplete). Cause: each block's timestamp is chosen
in `[now − MaxSkew, now + MaxSkew]`, five values at `MaxSkew = 2`, so
seven blocks alone contribute up to 5^7 timestamp assignments per
chain shape. The truncated `.out` is kept as the record of the attempt.

**Instance 2 — `KConf = 6, DepthK = 5, MaxBlocks = 7, MaxTime = 9,
MaxSkew = 1` (`Bridge_k6_skew1.*`): closed.** One constant differs
from instance 1: block-timestamp skew is ±1 instead of ±2. The committed
header's rationale, "`MaxSkew = 2` vs `Delta = 2` keeps the skew
adversarially significant relative to the window", is kept in
proportion: skew is still half the window and the ε side is still
reachable (witness below). This is an **instance change**, recorded
here and on the reading aid, not a claim that skew 2 is unnecessary.

Main configuration (four invariants `PinAgreement`,
`ShippedDesignatedAgree`, `HonestShipAccepted`, `LateBurialRejected`):
**green**, 114,703,188 generated / 86,849,955 distinct states, 0 on
queue, depth 20, 1 min 40 s, 5.4 GB resident (`Bridge_k6_skew1.out`,
`.time`).

**Vacuity witnesses, one per run** (the committed `_Sanity` cfg runs
all six under `-continue`; at 87 M states that prints a trace per
violating state and did not finish in eleven minutes — the aborted
attempt is not kept; each witness was instead run alone and TLC stopped
at its first violation, which is the same evidence):

| Witness (must be violated) | Result | First violation after (distinct states) |
|---|---|---|
| `ShipUnreachable` | fires | 809,833 |
| `BurialGapUnreachable` | fires | 745,259 |
| `NonMonotonicShipUnreachable` | fires | 453,928 |
| `EpsilonSideUnreachable` | fires | 920 |
| `WallClockDivergenceUnreachable` | fires | 8,927,390 |
| `LateBurialArtifactUnreachable` | fires | 1,886,618 |

All six phenomena the committed header lists are live at k = 6 with
skew 1 (`Bridge/W_*.out`).

**Companions at instance 2:**

| Companion | Registered expectation | Observed |
|---|---|---|
| `_BrokenAnchorSubst` | red on the correspondence and late-burial invariants; green on the rest | red on `ShippedDesignatedAgree` (757,947 distinct states at first violation) and on `LateBurialRejected` (1,969,320), each run alone; `PinAgreement` + `HonestShipAccepted` **green over the full space** (86,849,955 distinct, 0 on queue) — `C_AnchorSubst_*.out` |
| `_BrokenWallClock` | red on `HonestShipAccepted`; green on the rest | red on `HonestShipAccepted` (3,279,835); `PinAgreement` + `ShippedDesignatedAgree` + `LateBurialRejected` **green over the full space** (83,730,033 distinct, 0 on queue) — `C_WallClock_*.out` |
| `_BrokenPin` (`DepthK = KConf = 6`) | red on `PinAgreement` | Error: The invariant of PinAgreement is equal to FALSE; — `C_BrokenPin_k6.out` |

## 4. Disposition of E18

**Scope, stated first (Codex qualification (a), 2026-09-14):** every
result in this directory is for the bounded instance named beside it;
none is a statement about arbitrary timestamp skew, arbitrary `Delta`,
or a parameter-general theorem, and reducing the bridge's skew from ±2
to ±1 is a real reduction in the behaviours modelled even though every
witness remains reachable. Path (a) is complete for P5c and the bridge
in that sense, and P5P6 has no depth constant. Evidence at the registered k = 6 now exists for every
invariant, witness and companion of both modules, at instances whose
other bounds were sized by each module's own stated rule, with two
instance facts discovered and recorded on the reading aids: P5c needs
`Delta ≥ DepthK` (else shipping is unreachable) and the bridge needs
skew reduced to ±1 at `MaxBlocks = 7` for the space to close in
minutes rather than hours. **Nothing in this directory changes a
committed module, configuration, `.out`, tracker row or status**; the
committed k = 3 instances remain the runs of record for the checked
abstraction, and this directory is the evidence at the parameter that
Amendment 7 §A7.8 asked for. Path (b), the parameter-general
argument, was not needed and is not written. Non-author review of this
directory: partial — Codex confirmed from the saved output that the
skew-1 bridge search completed (86,849,955 distinct, zero queued, no
error) and that the skew-2 search is correctly labelled incomplete, and
stated it is not an E18 sign-off
(`docs/reviews/2026-09-14-codex-review-ledger-and-k6.md`); a full pass
is owed. Author read: none
requested; the tracker's parameter box (δ, ε, k, N ratification at
exit) is unchanged.

## Review log

- 2026-09-14 — runs and this file by the owner instance (Claude Fable
  5.1), TLC 2026.07.31 on wam-nuc, `-workers auto -deadlock`; scratch
  under the session scratchpad; artifacts copied here unchanged except
  that the vacuity `.out` files for P5c passed through
  `scripts/filter-tlc-output.sh` as the committed ones do.
- 2026-09-14 — Codex review (partial), two qualifications accepted and
  applied above; `docs/reviews/2026-09-14-codex-review-ledger-and-k6.md`.
