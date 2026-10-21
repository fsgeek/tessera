**E18 satisfies A7.8 option (a), within the stated finite bounds.** Option (b) is not supplied or needed. Review dated 2026-10-19, against HEAD `8ea8bfa` and the live artifacts. I reviewed all 46 bundle files and the governing models, configurations, amendments and prior review. I edited no repository files.

TLC was available. Using `/home/tony/.local/lib/tla2tools.jar`, version `2026.07.31.184830`, I completed **25 reruns**: every completed archived configuration, plus P5P6’s main configuration and four individual witnesses. Every expected result reproduced. Inputs, outputs, commands and hashes are retained in the [temporary review directory](/tmp/tessera-e18-8evt4y41/verification-summary.json).

| Model | Bounds | Independent result |
|---|---|---|
| P5c | `DepthK=5, Delta=6, MaxTime=26, MaxAttempts=3` | Six invariants plus `RefusalLatched` pass; **9,099 distinct states**, zero queued |
| Bridge | `KConf=6, DepthK=5, MaxTime=9, MaxBlocks=7, MaxSkew=1, Delta=2, Epsilon=1` | Four invariants pass; **86,849,955 distinct states**, zero queued |
| P5P6 | `MaxTime=6, DeltaMax=3, EpsilonMax=1, RcptTolMax=6` | Seven invariants pass; **4,302,592 distinct states**, zero queued |

P5P6 has no confirmation-depth constant: it checks a free `confirmedAt` input. The bridge checks its derivation from the designated chain block. I therefore reran P5P6 unchanged rather than inventing a `DepthK` parameter.

Every registered witness fires at the applicable bounds:

| Model | Witness | Result |
|---|---|---|
| P5c | `ShipUnreachable` | Fires |
| P5c | `ReissueShipUnreachable` | Fires |
| P5c | `ReorgShipUnreachable` | Fires |
| P5c | `RefusalUnreachable` | Fires |
| P5c | `RefusalAfterReorgUnreachable` | Fires |
| P5c | `RefusalWithLiveAnchorUnreachable` | Fires |
| P5c | `RefusalBuriedAnchorUnreachable` | Fires |
| Bridge | `ShipUnreachable` | Fires |
| Bridge | `BurialGapUnreachable` | Fires |
| Bridge | `NonMonotonicShipUnreachable` | Fires |
| Bridge | `EpsilonSideUnreachable` | Fires |
| Bridge | `WallClockDivergenceUnreachable` | Fires |
| Bridge | `LateBurialArtifactUnreachable` | Fires |
| P5P6 | `AcceptanceUnreachable` | Fires; depth independent |
| P5P6 | `NonMonotonicAcceptUnreachable` | Fires; depth independent |
| P5P6 | `LateBurialCaseUnreachable` | Fires; depth independent |
| P5P6 | `HonestCostCaseUnreachable` | Fires; depth independent |

The recut P5c burial witness has the required chronology: its archived trace reaches `anchorAt = refusedAt = 21`, then depth 5 at time 26. All 347 transitions across the 22 archived witness/companion traces match the model actions and configurations.

The `Delta=3` negative control also reproduces: its three shipping witnesses do **not** fire; its four refusal witnesses do. It supplies no positive shipping evidence.

All companion results reproduce:

- P5c `_Broken`: `NoShippedOrphan` fails—the only invariant it defines.
- P5c `_BrokenSilent`: `NoSilentDeadlock` fails; its remaining five invariants and latch property pass over **11,031 states**.
- Bridge `_BrokenAnchorSubst`: correspondence and late-burial rejection fail separately; remaining checks pass over **86,849,955 states**.
- Bridge `_BrokenWallClock`: honest-ship acceptance fails; remaining checks pass over **83,730,033 states**.
- `_BrokenPin`: the intentional `DepthK=KConf=6` error fails `PinAgreement` before exploration.

Three **low-severity, non-blocking record findings** remain:

- **E18-01 — Low — [prior review:17](/home/tony/projects/tessera/docs/reviews/2026-09-14-codex-review-ledger-and-k6.md:17).** It falsely says `_Broken_Green_k6.*` was added. Those artifacts are absent, and `_Broken` lacks the other invariant definitions. **Closure:** append a dated correction explaining that the resolution was the narrower claim now correctly recorded in `RESULTS-K6.md:47`, not an added isolation run.

- **E18-02 — Low — [run_bridge2.sh:12](/home/tony/projects/tessera/formal/tla/k6-2026-09-14/Bridge/run_bridge2.sh:12).** The archived runner changes into `Bridge/` and invokes local `.tla` filenames, but no models are stored there. It cannot reproduce directly from this checkout as written. **Closure:** provide a temporary-directory runner resolving the repository models, with an explicit source revision/hash manifest. This review independently staged and verified those inputs.

- **E18-03 — Low — [skew-2 output:41](/home/tony/projects/tessera/formal/tla/k6-2026-09-14/Bridge/Bridge_k6_skew2.out.truncated:41), [RESULTS-K6.md:82](/home/tony/projects/tessera/formal/tla/k6-2026-09-14/RESULTS-K6.md:82).** The kill annotation says 19:32 and 329,323,231 distinct states, while recorded progress continues through 19:35:47 and 437,204,801 states. The report also says four workers; the output says twelve. **Closure:** append a correction distinguishing observed progress from the unsupported termination metadata. Both accounts remain incomplete.

A7.8 specifies witness reachability at the chosen bounds; it does not fix `MaxSkew=2`. Consequently, the explicit reduction to ±1 does not prevent option (a). The incomplete ±2 search supplies no green evidence and was not restarted. This sign-off establishes neither arbitrary-skew results nor a parameter-general theorem, deep-reorg security, lifecycle latching, or implementation conformance.

SIGN-OFF: YES


