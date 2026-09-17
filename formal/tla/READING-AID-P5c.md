# Reading aid — P5c_IssuanceProtocol (issuance corollary: depth k, re-issue, refusal), Part A

**STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not adopted; the commit is the author's.**

*Repairs 2026-09-06 (skeptic findings on the TLA+ aids; applied by the AI
collaborator, PROPOSED):* "committed `.out`/trace" wording corrected to
regenerated, uncommitted working-tree files ("committed script" at the
vacuity paragraph is correct — `scripts/filter-tlc-output.sh` is in git);
Part B stated as not yet dispatched; checks row 5 no longer claims
`_BrokenSilent` certifies `RefusedOnlyWhenExhausted`; cites corrected:
PROPERTIES note `:212–235`, `RefusalLatched` at `amendment-2.md:286`,
`NoAnchor` Used column (226, 261). No module, cfg or `.out` changed.

Testimony under `formal/suite/ENUMERATION.md` amendment note 5 item 2
(lines 297–312): a reading aid for non-expert readers, reviewed by the
lower-ceiling reader probe, **not a gate for exit**, never a verdict on
the proof. Nothing here changes a module, a cfg, or a `.out`.

**Model.** `formal/tla/P5c_IssuanceProtocol.tla` with
`P5c_IssuanceProtocol.cfg` (main: six invariants and one action
property), `_Sanity.cfg` (seven vacuity witnesses, `-continue`, piped
through `scripts/filter-tlc-output.sh`); companions
`P5c_IssuanceProtocol_Broken.tla` (ships shallow) with `_Broken.cfg`,
and `P5c_IssuanceProtocol_BrokenSilent.tla` (separately enabled
`Refuse`) with `_BrokenSilent.cfg` and `_BrokenSilent_Green.cfg`. The
module was **recut on 2026-09-06** (review item 15): one recording
variable `refusedAt`, one guard invariant `RefusalTimeConsistent`, one
witness rewritten (header 127–146). Line numbers are from the
**current** working-tree text; every `.out` in this family was
regenerated against it and its cfgs (FIXES log 254–265; trace line
references checked by hand, FIXES 107–114). All `.out`, `_Green`
cfg/out pairs and archived runs cited below are uncommitted working-tree
files (`git status` 2026-09-06; the commit is the author's); "regenerated" below means "as regenerated in the
working tree". All runs use `-deadlock`
(terminal states deadlock at the `MaxTime` bound by design, 279–281;
FIXES 18–19).

**Provenance of the parts.** Part A (this file) is by the AI
collaborator (Claude, Fable 5.1). Part B — the blind explanation by a
non-author model of a different family — is to be dispatched separately
and has not been dispatched as of 2026-09-06; it is not in this file;
disagreements are to be recorded at the top of this file, as `READING-AID-Q3.md` does. Probe result: two runs 2026-09-06; see the next two paragraphs.

**Probe result (2026-09-06, `falsification-2026-09-06/P5c/PROBE-haiku-2026-09-06.md`; PROPOSED, AI collaborator).**
A Haiku reader given the module alone stated only the shipping half of
the claim (`ShippedIsSound`, `NoShippedOrphan`) and omitted the refusal
half (`NoSilentDeadlock`, `RefusedOnlyWhenExhausted`, `RefusalLatched`);
given this aid it stated both halves, quantified the instance and quoted
the registered sentence — the aid did work on the claim. On the
adversary and the three boundaries both readers were right, so the
probe did not discriminate there; the condition-1 answer cites header
lines (54–60, 248–258), so that condition saw the commented module, not
a stripped one, and the P5c header is itself a strong aid. No aided
answer was wrong where the module-only answer was right. One aided
slip, for the reader in a hurry: **the single clock (block time = wall
time, one block per tick) is NOT why there are no signatures, keys,
headers or verdicts here** — those are absent because the model has no
bytes and no A1.3 adversary at all (Boundaries, "No adversary in the
A1.3 sense"; Part B 388); the clock abstraction removes only timestamp
skew and the ε side. The aided reader also reported "no contradictions
between aid and module" while Part B 362 records one (cfg 32 and module
175 say "durable", exceeding the narrowed claim).

**Probe result, run 2 (2026-09-06, same file, "Run 2"; PROPOSED, AI
collaborator).** A second pair of fresh Haiku contexts, dispatched after
the paragraph above was in the aid. On the **claim** the probe did not
discriminate and the aided answer was the narrower one: both readers
stated the shipping half; the module-only reader also named
`NoSilentDeadlock`, the aided reader named no refusal invariant, though
it reported relying on the plain-language statement whose opening
clauses are the refusal half. Nothing it said was false, so the aid is
not defective by ENUMERATION's test, but run 1's claim discrimination
did not replicate (1 of 2). The proposed repair is a one-line lead on
the *Claim* paragraph — "two halves: shipping (checks rows 1–3) and
refusal (rows 4–6)" — not applied here. The aid **did work** on the
initialization sub-question (module-only: the `Reorg` precondition,
both runs; aided: `Init`'s clean start, Part B 419 in this file) and on boundary
precision (module-only attached the refusal latch to `ShippedIsSound`;
`RefusalLatched` 337 is the latch; aided cited items 16, 17, 21 with
correct lines). Run 1's aided slip did not recur: the aided reader
attributed the absence of bytes and keys to the model's variables, not
to the single clock, and it found the "durable" wording note. Both
readers asked for a concrete case where `Ship`'s fused guard and the
A2.1 predicate diverge; the review record supplies one (reviewer §6,
line 573: `Anchor(0); Tick×4` — designated-block timestamp 2 ≤ δ = 3,
but `now = 4` disables `Ship`), which this aid should carry in checks
row 2. Condition 1 was again the commented module, not a stripped one.

**Registered text read against.** Amendment 1 P5's issuance-protocol
corollary (`docs/phase-0-prereg-amendment-1.md:186–197`) and A1.6
(`:477–510`, permanence at `:504–505`); Amendment 2 §A2.1
(`docs/phase-0-prereg-amendment-2.md:78–217`), §A2.3 (`:252–295`, model
note `:278–293`); `formal/PROPERTIES.md` P5c bullets (`:158–166`,
`:179–235`, the 2026-09-06 note at `:212–235`). Review record:
`docs/reviews/2026-09-06-codex-tla-falsification-p4-p5p6-p5c.md`, items
15–21 (lines 149–183) and the verbatim reviewer output for P5c (lines
455–581). Item numbers below are that record's.

---

## Typing / idiom note

- **This module has real actions** (reading guide 148–154). A state is
  an assignment to the ten `VARIABLES` (166–177); `Init` (182–187) is a
  single state; `Next` (277) is a disjunction of five actions — `Tick`,
  `Anchor`, `Reorg`, `Ship`, `Reissue`. A **behaviour** is a sequence of
  states each reached from the last by one action; TLC explores every
  behaviour up to the `MaxTime` bound. Unlike the P4 and P5P6
  truth-tables, a violation here comes with a **trace** (`State 1 …
  State n`, each labelled with the action and its module line — e.g.
  `<Tick line 200 …>`).
- **Primes.** In an action, `x'` is the value of `x` in the next state;
  `UNCHANGED <<…>>` lists what does not move. An action is **enabled**
  in a state when its unprimed conjuncts hold; `ENABLED Ship` (310) is
  that predicate as a formula.
- **Scheduling is nondeterministic; nothing is fair.** When several
  actions are enabled TLC explores all of them, and an enabled action
  may be postponed forever (header 62–69). So no "eventually" claim is
  made or checked; only safety — "no reachable state is bad".
- **An invariant** must hold in every reachable state. **An action
  property** `[][P]_vars` (337, cfg `PROPERTIES` 33–34) must hold across
  every step: here "no step unsets `refused`".
- **Atomic entry.** `Tick` sets `refused'` in the same transition that
  carries the clock past the final window (203–204), so the state
  "window expired, no refusal recorded" cannot exist (192–198). The
  `_BrokenSilent` companion gives `Refuse` its own action instead
  (`_BrokenSilent.tla` 98–103) and that state becomes reachable.
- **Sanity witnesses** (359–369) are deliberately false assertions
  `~(…)`; run with `-continue`, TLC reports every violating state and a
  **violation is the healthy result** — it proves shipping and refusal
  are actually reachable, so the implication-shaped invariants are not
  vacuous (348–358). Ordering matters because TLC reports only the first
  failing invariant per state (Sanity cfg 16–22).
- **`_Broken` / `_Green`** as in the other aids: a companion goes red on
  a named invariant and discharges nothing of the property; a `_Green`
  cfg re-runs it with the red invariant removed to isolate the break
  among the checked set (`_BrokenSilent_Green.cfg` 5–9; item 4 scoping,
  `_BrokenSilent.tla` 18–24).
- **Traces are not run-stable under `-workers 4`.** TLC stops at the
  first violation any worker reaches, so the printed counterexample and
  the "states generated" count of a red run vary with scheduling; the
  verdict, the set of red invariants, and complete-search state counts
  do not. A trace in a regenerated `.out` (working tree, uncommitted as
  of 2026-09-06) is "one such trace" (FIXES log 233–252).
- **Single clock.** Block timestamp = wall time = tick; one block per
  tick (header 79–82, 148–151). Under the clock-roles ruling this clock
  reads as the **wall clock** and expiry `now > declared + Delta` is the
  S = 0 instance of the lifecycle envelope (header 34–45;
  `amendment-2.md:106–110`).

## Cast

Line numbers are `P5c_IssuanceProtocol.tla` unless a file is named.

| Name | What it is in the design (plain words) | Defined | Used |
|---|---|---|---|
| `MaxTime` | the clock bound. Must be ≥ `MaxAttempts·(Delta+1)` = 12 or the final window cannot expire and every refusal invariant passes vacuously; 14 adds `DepthK` headroom for post-refusal burial (header 93–101; cfg 1–14) | 158; cfg 16 | 200 |
| `Delta` | δ, scaled (header 3–5; `amendment-1.md:186–189`) | 158; cfg 17 | 204, 263, 271, 302, 310, 319, 330 |
| `DepthK` | burial depth counted in blocks AFTER inclusion (depth 0 = just included); `DepthK = k − 1` (header 26–29; `amendment-2.md:208–212`); `ASSUME DepthK # 0` (160) | 158; cfg 18 | 202, 237, 262, 303, 369 |
| `MaxAttempts` | N, the attempt bound — protocol semantics per A2.3, not a search bound (header 29–32, 87–93; `amendment-2.md:260–262, 278–279`) | 158; cfg 19 | 203, 272, 319, 329 |
| `NoAnchor` | sentinel: no anchor in the chain | 163 | 184, 226, 237, 239, 261, 273, 300, 364 |
| `NoRefusal` | sentinel: no refusal recorded (recut 2026-09-06) | 164 | 187, 345 |
| `now` | the single clock (wall = chain, see idiom note) | 167; 183 | 200–206, 227, 263, 271, 273, 310, 319, 330, 346 |
| `declared` | `declared_issue_time` of the CURRENT attempt; `Reissue` redeclares it (273) | 168; 183 | 204, 263, 271, 273, 301–302, 310, 319, 330 |
| `anchorAt` | block time of the current anchor, or `NoAnchor` | 169; 184 | 202, 226–227, 237, 239, 261, 273, 300–302, 364, 369 |
| `depth` | confirmations after inclusion, capped at `DepthK` (189–190) | 170; 184 | 202, 227, 237, 239, 262, 273, 303, 369 |
| `shipped` | issuance completed | 171; 185 | 203, 226, 240, 261, 264, 271, 299, 310, 319, 328, 359–361 |
| `shippedOrphaned` | **the harm flag**: a SHIPPED receipt's anchor was orphaned; must stay `FALSE` (172; 288–291) | 172; 185 | 240, 292 |
| `attempts` | issuance attempts so far, `1..MaxAttempts` | 173; 186 | 203, 272, 274, 319, 329, 360 |
| `reorgs` | reorg count, capped at 2 — for the reachability witnesses only (238) | 174; 186 | 238–239, 361, 363 |
| `refused` | the abstract refusal record of A2.3 / round-3 ruling 4 (175; header 47–61) | 175; 187 | 203–206, 318–330, 337, 345–346, 362–369 |
| `refusedAt` | the clock value at which the refusing `Tick` entered the refusal; `NoRefusal` before (recut, item 15) | 176–177; 187 | 206, 345–346, 369 |
| `Init` | `now = declared = 0`, no anchor, first attempt, nothing shipped or refused | 182–187 | cfg 21 |
| `Tick` | time advances one unit; an included anchor gains one confirmation (202); **atomic refusal entry** when the final attempt's window is crossed (203–204); stamps `refusedAt` (206) | 199–207 | 277 |
| `Anchor` | the OTS calendar lands the stamp in a block, at any time (delays = the action not firing yet); deliberately NOT guarded on `~refused` — the A2.4 discarded-attempt case stays reachable (209–224) | 225–229 | 277 |
| `Reorg` | orphans any anchor shallower than `DepthK`; depth ≥ k is permanent **by assumption** (A1.6 `amendment-1.md:504–505`; comment 231–235); latches the harm flag if the receipt had shipped (240) | 236–241 | 277 |
| `Ship` | issuance completes under the STRICT rule: buried at `DepthK` AND `now ≤ declared + Delta` (243–246). Boundary race at `now = declared + Delta`, intentional (248–259) | 260–266 | 277, 310 |
| `Reissue` | window expired, attempts remain: discard, redeclare at `now` | 270–275 | 277 |
| `Next` | the five actions | 277 | cfg 22 |
| `NoShippedOrphan` … `RefusalTimeConsistent` | the six invariants (checks table) | 292, 298–303, 309–310, 318–319, 327–330, 344–346 | cfg 25–30 |
| `RefusalLatched` | the action property: no step unsets `refused` | 337 | cfg 33–34 |
| `ShipUnreachable` … `RefusalBuriedAnchorUnreachable` | seven vacuity witnesses | 359–369 | Sanity cfg 42–48 |
| `_Broken.Ship` | ships at `depth >= 1` — one block after inclusion, shallower than `DepthK` (item 18 correction, `_Broken.tla` 17–25, 72–74) | `_Broken.tla` 75–81 | 90 |
| `_BrokenSilent.Tick`, `Refuse` | `Tick` records nothing; a separate `Refuse` records the refusal "whenever it gets around to it" (`_BrokenSilent.tla` 26–27, 58–59, 95–97) | `_BrokenSilent.tla` 60–65, 98–103 | 105 |

## Checks table

| # | Invariant / property (lines) | Registered sentence it discharges | What the review found it does NOT discharge | Companion behaviour |
|---|---|---|---|---|
| 1 | `NoShippedOrphan` (292) | P5 corollary: "a one-confirmation anchor orphaned by a transient reorganization would leave an already-shipped receipt permanently unverifiable, so a receipt never ships on a shallow anchor" (`amendment-1.md:189–193`). Holds because `Ship` needs `depth >= DepthK` (262) and `Reorg` touches only `depth < DepthK` (237). **Load-bearing** for the Gemini-named harm. | **Item 21 (Boundary):** post-shipment `Reorg` is never enabled, so the invariant excludes only the harm its permanence assumption disables; deep-reorganisation resistance is not exercised (reviewer 515). The A1.6 permanence sentence was not in the jail (463). No package integrity, header authenticity, or general permanent verifiability (463). | **RED in `_Broken`** — `Anchor` at 0 → `Tick` (now 1, depth 1) → `Ship` → `Reorg`, `shippedOrphaned = TRUE` (`_Broken.out:25`, trace `Anchor line 60 / Tick line 51 / Ship line 76 / Reorg line 66`). Green in `_BrokenSilent_Green`. |
| 2 | `ShippedIsSound` (298–303) | "issuance is not complete until the anchor is **confirmed** — buried at a minimum confirmation depth k — within δ of `declared_issue_time`" (`amendment-1.md:186–189`); A2.1's rule (`amendment-2.md:85–89`). | **Item 17 (Accepted, header narrowed):** no confirmation-time conjunct and no ε; its lower bound `anchorAt >= declared` is stronger than the registered ε-tolerant bound; "Ship's guard IS the chain-time predicate" holds only under the single-clock abstraction — A2.1 calls the fused guard "locally stronger" (header 108–117; `amendment-2.md:175–178`; reviewer 465–470). No issuer/verifier comparison here — that is the bridge's `ShippedDesignatedAgree` (item 12 in the P5P6 review). | Green in `_BrokenSilent_Green`. |
| 3 | `ExpiredCannotShip` (309–310) | "the failed attempt is discarded, not shipped" (`amendment-1.md:194–196`). | **Item 16 (Covered elsewhere):** registered expiry applies "only **strictly after** the boundary, and only to attempts with no timely-latched eligibility" (`amendment-2.md:154–159`); here every unshipped attempt past the window cannot ship — stronger, the S = 0 pre-latch instance (header 118–126); a timely-eligible final attempt CAN be expired here (reviewer attack 3, 527). Local to the current declaration; does not quantify over discarded artifacts (472). Its antecedent directly contradicts `Ship`'s guard, so its success does not independently validate the expiry definition (517). | Green in `_BrokenSilent_Green`. |
| 4 | `NoSilentDeadlock` (318–319) | A2.3 model note: "the refusal state is entered atomically" — the conditional safety half (`amendment-2.md:278–290`); round-3 ruling 4 construction (header 47–61). **Load-bearing** for atomic entry. | Not that the crossing occurs — `Tick` is postponable, no fairness (header 62–69; `amendment-2.md:288–289` "termination is a contract obligation"); not registered expiry in full (latch, S) (reviewer 474); not a deadlock or termination predicate (474). | **RED in `_BrokenSilent`** — final state `now 12, declared 8, attempts 3, shipped FALSE, refused FALSE`; `Refuse` never fired in the printed run (`_BrokenSilent.out:25, 195–219`; one such trace, FIXES 233–252). |
| 5 | `RefusedOnlyWhenExhausted` (327–330) | A2.3: "issuance makes at most **N attempts** … Exhausting them obligates the implementation to terminate issuance in an explicit refusal" (`amendment-2.md:260–266`); contains shipped/refused mutual exclusion as a corollary (comment 321–326). | Omits the eligible/finalizing alternative and Slack: registration says "timely-latched eligibility excludes expiry" (`amendment-2.md:154–158`), so this instance's "exhausted" permits refusal registration forbids (reviewer 476; item 16). | Not certified by `_BrokenSilent` (red run, 241 states left on queue, `_BrokenSilent.out:219`); **green** in `_BrokenSilent_Green` (`_BrokenSilent_Green.out:25, 29`) — `Refuse`'s guard is the honest exhaustion condition (`_BrokenSilent.tla` 95–100). |
| 6 | `RefusalLatched` (337; action property) | "…and latches" (`amendment-2.md:286`, model note `:278–293`; header 55–56). | Boolean persistence including stuttering; does NOT establish "explicit refusal, durably recorded" as an operational outcome — durability, retrieval, reporting are expressly outside this proof (header 56–61; `amendment-2.md:288–293`; reviewer 478). | Green (`PROPERTIES`) in `_BrokenSilent_Green`. |
| 7 | `RefusalTimeConsistent` (344–346; recut) | No registered sentence. A guard on the recording variable so that a broken `refusedAt` (stuck at `NoRefusal = −1`) cannot make `anchorAt >= refusedAt` trivially true and silently restore the chronology-free witness (comment 339–343). | — (an internal consistency check, not a property claim). | Green in `_BrokenSilent_Green` (`Refuse` stamps `refusedAt' = now`, `_BrokenSilent.tla` 101). |

**Vacuity witnesses** (359–369). All seven fire at `MaxTime = 14`
(`P5c_IssuanceProtocol_Sanity.out`, 506 repeats elided by the committed
script; FIXES 190–194). No registered sentence says shipping or refusal
is unreachable (reviewer 480). The recut `RefusalBuriedAnchorUnreachable`
(368–369) requires the anchor to have landed at or after the refusal
instant and then reached full depth; it is **unreachable at `MaxTime`
= 12 and 13 and fires at 14** (`falsification-2026-09-06/P5c/recut/`;
header 139–140). The regenerated trace (working tree, uncommitted):
refusal enters at `now = 12`
(`refusedAt = 12`, State 15), `Anchor` at 12 (State 16), `depth = 2` at
`now = 14` (State 18) (`_Sanity.out` from line 865). Before the recut
the witness `~(refused /\ depth >= DepthK)` fired at 12 (21 violations;
item 15 CONFIRMED) because an anchor placed before the refusal and
buried by the final ticks satisfied it.

**Registered clauses with no checked formula** (reviewer 486–491): the
conditional shipping-opportunity guarantee `B − C ≤ S`, inclusive
boundary eligibility, and the latch (→ `P5cP5P6_BridgeSlack_Latch.tla`,
item 16); the full three-conjunct issuer/verifier agreement, tolerance
handling, designated-header evaluation (→ `P5cP5P6_Bridge.tla`, item
17); header availability/authentication (→ A2.2 H1a obligation);
non-waivability and the `INVALID`/`UNVERIFIABLE` partition (→ P4); no
standing for abandoned-but-chain-valid artifacts (→ A2.4 / Amendment 3
standing); the N-attempt bound is enforced by `Init` and `Reissue` (272)
with no separate invariant; termination, delivery, durable storage are
contractual (`amendment-2.md:288–293`).

## Finite instance

`MaxTime = 14`, `Delta = 3`, `DepthK = 2`, `MaxAttempts = 3` (cfg
16–19). **`DepthK = 2` represents k = 3** (`DepthK = k − 1`,
`amendment-2.md:208–212`), **not the registered strict default k = 6**
(which would be `DepthK = 5`, header 29) — item 20, Boundary.
`MaxAttempts = 3` is A2.3's working default N = 3 (`amendment-2.md:270`).
Main: 3606 generated / 2190 distinct, green on six invariants and the
action property (`P5c_IssuanceProtocol.out:25, 29`); the count is
unchanged by the recut because `refusedAt` is determined by the rest of
the state (FIXES 47).

What the record says about why this instance is the one checked: the
module's own constraint `MaxTime ≥ MaxAttempts·(Delta+1)` = 12, without
which the refusal invariants are vacuous, plus `DepthK` headroom = 14
for the post-refusal burial path (header 93–101; cfg 1–14) — with the
`_Sanity` witnesses guarding both misconfigurations. The invariants
compare `depth` to `DepthK` symbolically (202, 237, 262, 303, 369),
never to a numeral. The review states these are "finite instances, not
a parameter-universal result" (reviewer 461) and that `ASSUME DepthK #
0` (160) means k = 1 cannot be instantiated (569). **No
parameter-independence argument exists in the record; this aid supplies
none.**

Runs in the current record (FIXES 47, 115–127, 186–194): main
**green**; `_Sanity` all seven witnesses at 14, six at 12 and 13;
`_Broken` **red** `NoShippedOrphan`; `_BrokenSilent` **red**
`NoSilentDeadlock`; `_BrokenSilent_Green` **green** (3874/2400, grew
from 3825/2310 because `refusedAt` now varies with when `Refuse` fires).
`_Broken.cfg` configures one invariant, so its item-4 `_Green` set is
empty (FIXES 49, 128–132).

## Boundaries

From the review's **Boundary** / **Covered elsewhere** dispositions,
the module's named abstractions (78–101), and the header correction:

- **Item 20.** Finite instance: `DepthK = 2` is k = 3, not k = 6; see
  above.
- **Item 21.** Reorgs never exceed depth k: A1.6's "anchors at depth ≥
  k are treated as permanent" (`amendment-1.md:504–505`) is a
  PRECONDITION of `Reorg` (237; comment 231–235), not a result. The
  reorg re-verification residual is tracked as NOT discharged
  (`formal/PROPERTIES.md:110–113`, bridge entry). The broken companion
  shows what the depth-k rule buys GIVEN that assumption (header 85–86).
- **Item 16 → `P5cP5P6_BridgeSlack_Latch.tla`.** Eligibility latching is
  the registered lifecycle (`amendment-2.md:154–159`); this module is the
  earlier S = 0, pre-latch instance in which a timely-eligible final
  attempt can be expired by a `Tick` scheduled before `Ship` (header
  118–126; the boundary race at 248–259).
- **Item 17 → `P5cP5P6_Bridge.tla`.** The decoupled three-conjunct
  verifier predicate and its agreement with `Ship` are checked there
  (`ShippedDesignatedAgree`, `_BrokenAnchorSubst` red), not here (header
  108–117; `formal/PROPERTIES.md:90–131`).
- **Single clock.** Block timestamps equal real time; Bitcoin timestamp
  skew is verifier-side, absorbed into ε (A1.6); issuance-side anchors
  never precede declaration, so the ε side does not appear (header
  79–82).
- **Liveness unclaimed.** `Reissue` and `Tick` are postponable; a run
  can stall mid-loop; the final crossing is not guaranteed to occur;
  "eventually ships" is not checked (header 62–69, 91–93; reviewer
  attack 8, 537).
- **Refusal is a Boolean**, not a record: storage durability,
  retrievability, and reporting are Amendment 3 handoff obligations
  (header 55–61).
- **No adversary in the A1.3 sense.** No bytes, signatures, keys,
  manifests, type boundaries, authority channels, or adversarial input
  actions; none of A1.3's capabilities is encoded (reviewer 565). No
  block identities or heights, competing chains, header source, or
  explicit `confirmed_at` — timestamps and depth stand in (566). No
  eligibility/observation event, `B − C` measurement, verifier policy,
  verdict, or standing state (567). No retained retry lineage,
  concurrent artifacts, crash/recovery, or delivery transition (568).
- **Mechanism.** First-reported counterexamples are not run-stable under
  `-workers 4` (FIXES 233–252); the regenerated traces (working tree,
  uncommitted as of 2026-09-06) are "one such trace".

## Plain-language statement (collaborator; cited; Part B pending)

*Claim* — what the module itself says IS claimed (header 69–76), as
checked: within the configured instance, no reachable state has the
final attempt's window expired without the refusal recorded
(`NoSilentDeadlock`); the refusal is recorded only when the final
attempt's window has expired with nothing shipped, as this instance
defines exhaustion (`RefusedOnlyWhenExhausted`); once recorded it is
never unset (`RefusalLatched`); a shipped receipt's anchor is buried at
depth k within δ of its own declared time under the single clock
(`ShippedIsSound`) and is never orphaned by the reorgs the model
permits (`NoShippedOrphan`); an attempt past its window cannot ship
(`ExpiredCannotShip`). Six invariants and one action property, green
over 2190 states (`out:25, 29`); shipping and refusal are both
reachable, in seven witnessed shapes.

*Adversary.* None in the A1.3 sense (reviewer 565). The environment is
the chain — `Tick`, `Anchor` delays, shallow `Reorg` — and the
scheduler, which may postpone any enabled action.

*Boundary.* Permanence beyond depth k is assumed (item 21); k = 3 is
checked, not k = 6 (item 20); latching, slack, and decoupled clocks live
in the bridge modules (items 16, 17); termination, durability, and
delivery are contract obligations (A2.3 model note), not results.

---

# Part B — blind explanation (Codex CLI 0.153.3, model gpt-6-astra, 2026-09-06, verbatim)

> Written by a non-author model of a different family, jailed to the current modules, configurations, trimmed committed TLC outputs, the registered text, and Amendment 4 — no repository, results, or review access. Its English is evidence of what the modules *say*. Where it disagrees with Part A, the disagreement is a finding to disposition, not a defect to hide. Dispatch prompt archived at `formal/tla/falsification-2026-09-06/P5c/PART-B-PROMPT.md`.

## Reading notes

- A **state** is one snapshot of the ten variables; a **behaviour** is a sequence of snapshots beginning at `Init`, with successive changes allowed by `Next`. Here those changes advance time, include or orphan an anchor, ship, or retry; primes mean the next snapshot and `UNCHANGED` preserves listed fields. (`P5c_IssuanceProtocol.tla:166–207`, `P5c_IssuanceProtocol.tla:225–277`.)
- An **INVARIANT** is a condition TLC checks in every reachable state of the configured finite instance, not a proof for every parameter choice or an implementation. The main configuration selects six; the committed run exhausts its queue without an error. (`P5c_IssuanceProtocol.cfg:15–30`, `P5c_IssuanceProtocol.out.trimmed:30–37`.)
- A **truth-table model**, whose `Next` only stutters (leaves the snapshot unchanged), can check predicates across its allowed initial assignments but cannot demonstrate a lifecycle through changing states. P5c is expressly the other case: one initial snapshot and five state-changing actions. (`P5c_IssuanceProtocol.tla:11–13`, `P5c_IssuanceProtocol.tla:182–207`, `P5c_IssuanceProtocol.tla:277`; `P5c_IssuanceProtocol.out.trimmed:30`.)
- A **sanity/witness configuration** asserts that useful situations are unreachable; its **VIOLATION** is healthy because a counterexample reaches one. All seven witnesses fail here, covering shipping, retries, reorgs and refusal, including a late anchor buried after refusal; these are existence checks, not guarantees that every run reaches them. (`P5c_IssuanceProtocol_Sanity.cfg:1–22`, `P5c_IssuanceProtocol.tla:359–369`, `P5c_IssuanceProtocol_Sanity.out.trimmed:2–14`.)
- A **_Broken companion** deliberately changes a rule so a named check must catch the defect. A **_Green isolation configuration** checks the other listed conditions on that broken model: its clean run isolates the failure only within that checked set, not across every imaginable property. (`P5c_IssuanceProtocol_Broken.cfg:12–13`, `P5c_IssuanceProtocol_BrokenSilent.cfg:19–28`, `P5c_IssuanceProtocol_BrokenSilent_Green.cfg:5–27`, `P5c_IssuanceProtocol_BrokenSilent_Green.out.trimmed:31–35`.)
- **CONSTANTS** fix the experiment: time ceiling 14, deadline allowance 3 ticks, burial threshold 2 blocks after inclusion, and at most 3 attempts. Thus this instance uses Bitcoin confirmation count k = 3, not the strict working default k = 6; `MaxTime` bounds exploration, whereas `MaxAttempts` represents protocol policy. (`P5c_IssuanceProtocol.cfg:15–19`, `REGISTERED.txt:131–137`, `REGISTERED.txt:201–202`.)
- **PROPERTIES** also checks `RefusalLatched`: once refusal is true, every subsequent step preserves it. This is a transition safety check, not eventual progress or durable storage; `ENABLED Ship` elsewhere means that a shipping transition is possible from this snapshot. (`P5c_IssuanceProtocol.cfg:32–34`, `P5c_IssuanceProtocol.tla:309–310`, `P5c_IssuanceProtocol.tla:332–337`.)

## Cast

The thing being judged is the **current issuance attempt and its shipping/refusal outcome**, represented principally by `shipped`, `refused`, and that attempt's declaration, anchor and depth; there is no verifier verdict variable. The table lists locally declared names, using the main module for shared definitions; companion differences follow it. (`P5c_IssuanceProtocol.tla:166–180`, `P5c_IssuanceProtocol.tla:298–346`.)

| Variable, constant or defined operator | Plain design meaning | Defined at file:line | Used at file:line |
|---|---|---|---|
| `MaxTime` | Exploration clock ceiling | `P5c_IssuanceProtocol.tla:158` | `P5c_IssuanceProtocol.tla:200`; `P5c_IssuanceProtocol.cfg:16` |
| `Delta` | Attempt's deadline allowance | `P5c_IssuanceProtocol.tla:158` | `P5c_IssuanceProtocol.tla:203–204`, `P5c_IssuanceProtocol.tla:263` |
| `DepthK` | Required blocks after inclusion; depth saturation limit | `P5c_IssuanceProtocol.tla:158` | `P5c_IssuanceProtocol.tla:202`, `P5c_IssuanceProtocol.tla:237`, `P5c_IssuanceProtocol.tla:262` |
| `MaxAttempts` | Protocol attempt limit | `P5c_IssuanceProtocol.tla:158` | `P5c_IssuanceProtocol.tla:203`, `P5c_IssuanceProtocol.tla:272` |
| `now` | Monotonic integer wall clock, also the block clock here | `P5c_IssuanceProtocol.tla:167` | `P5c_IssuanceProtocol.tla:201`, `P5c_IssuanceProtocol.tla:227` |
| `declared` | Current attempt's declared issue time | `P5c_IssuanceProtocol.tla:168` | `P5c_IssuanceProtocol.tla:263`, `P5c_IssuanceProtocol.tla:273` |
| `anchorAt` | Current anchor's inclusion time, or absent sentinel | `P5c_IssuanceProtocol.tla:169` | `P5c_IssuanceProtocol.tla:227`, `P5c_IssuanceProtocol.tla:300–302` |
| `depth` | Blocks after inclusion, capped at threshold | `P5c_IssuanceProtocol.tla:170` | `P5c_IssuanceProtocol.tla:202`, `P5c_IssuanceProtocol.tla:262` |
| `shipped` | Issuance has completed | `P5c_IssuanceProtocol.tla:171` | `P5c_IssuanceProtocol.tla:264`, `P5c_IssuanceProtocol.tla:299` |
| `shippedOrphaned` | Harm flag: an already-shipped anchor was orphaned | `P5c_IssuanceProtocol.tla:172` | `P5c_IssuanceProtocol.tla:240`, `P5c_IssuanceProtocol.tla:292` |
| `attempts` | Attempts begun, counting the first as 1 | `P5c_IssuanceProtocol.tla:173` | `P5c_IssuanceProtocol.tla:186`, `P5c_IssuanceProtocol.tla:274` |
| `reorgs` | Reorg counter, limited to two; also witness history | `P5c_IssuanceProtocol.tla:174` | `P5c_IssuanceProtocol.tla:238–239`, `P5c_IssuanceProtocol.tla:361–363` |
| `refused` | Abstract refusal flag, not a storage record | `P5c_IssuanceProtocol.tla:175` | `P5c_IssuanceProtocol.tla:203–206`, `P5c_IssuanceProtocol.tla:332–337` |
| `refusedAt` | Clock value recorded on entering refusal | `P5c_IssuanceProtocol.tla:176–177` | `P5c_IssuanceProtocol.tla:206`, `P5c_IssuanceProtocol.tla:369` |
| `NoAnchor` | −1 means no current anchor | `P5c_IssuanceProtocol.tla:163` | `P5c_IssuanceProtocol.tla:184`, `P5c_IssuanceProtocol.tla:226` |
| `NoRefusal` | −1 means no recorded refusal time | `P5c_IssuanceProtocol.tla:164` | `P5c_IssuanceProtocol.tla:187`, `P5c_IssuanceProtocol.tla:345` |
| `vars` | Whole snapshot, used to recognize unchanged steps | `P5c_IssuanceProtocol.tla:179–180` | `P5c_IssuanceProtocol.tla:337` |
| `Init` | Start at time zero on an empty first attempt | `P5c_IssuanceProtocol.tla:182–187` | `P5c_IssuanceProtocol.cfg:21` |
| `Tick` | Advance clock/depth; atomically refuse on final expiry | `P5c_IssuanceProtocol.tla:199–207` | `P5c_IssuanceProtocol.tla:277` |
| `Anchor` | Include the current stamp at the current clock time | `P5c_IssuanceProtocol.tla:225–229` | `P5c_IssuanceProtocol.tla:277` |
| `Reorg` | Remove a shallow anchor and record any shipping harm | `P5c_IssuanceProtocol.tla:236–241` | `P5c_IssuanceProtocol.tla:277` |
| `Ship` | Complete only with sufficient depth before expiry | `P5c_IssuanceProtocol.tla:260–266` | `P5c_IssuanceProtocol.tla:277`, `P5c_IssuanceProtocol.tla:310` |
| `Reissue` | Replace expired attempt with fresh declaration and no anchor | `P5c_IssuanceProtocol.tla:270–275` | `P5c_IssuanceProtocol.tla:277` |
| `Next` | Any one enabled lifecycle action may happen next | `P5c_IssuanceProtocol.tla:277` | `P5c_IssuanceProtocol.cfg:22` |
| `NoShippedOrphan` | No recorded post-shipping orphan harm | `P5c_IssuanceProtocol.tla:292` | `P5c_IssuanceProtocol.cfg:25` |
| `ShippedIsSound` | Shipped anchor exists, is in-window and sufficiently deep | `P5c_IssuanceProtocol.tla:298–303` | `P5c_IssuanceProtocol.cfg:26` |
| `ExpiredCannotShip` | An unshipped expired attempt has no shipping transition | `P5c_IssuanceProtocol.tla:309–310` | `P5c_IssuanceProtocol.cfg:27` |
| `NoSilentDeadlock` | Final expiry without shipping already has refusal recorded | `P5c_IssuanceProtocol.tla:318–319` | `P5c_IssuanceProtocol.cfg:28` |
| `RefusedOnlyWhenExhausted` | Refusal implies final expired attempt and no shipping | `P5c_IssuanceProtocol.tla:327–330` | `P5c_IssuanceProtocol.cfg:29` |
| `RefusalTimeConsistent` | Refusal/time-sentinel agreement; recorded time is in range | `P5c_IssuanceProtocol.tla:344–346` | `P5c_IssuanceProtocol.cfg:30` |
| `RefusalLatched` | Refusal cannot be unset on subsequent steps | `P5c_IssuanceProtocol.tla:337` | `P5c_IssuanceProtocol.cfg:34` |
| `ShipUnreachable` | Denies any shipping witness | `P5c_IssuanceProtocol.tla:359` | `P5c_IssuanceProtocol_Sanity.cfg:44` |
| `ReissueShipUnreachable` | Denies shipping on a later attempt | `P5c_IssuanceProtocol.tla:360` | `P5c_IssuanceProtocol_Sanity.cfg:43` |
| `ReorgShipUnreachable` | Denies shipping after any reorg | `P5c_IssuanceProtocol.tla:361` | `P5c_IssuanceProtocol_Sanity.cfg:42` |
| `RefusalUnreachable` | Denies any refusal witness | `P5c_IssuanceProtocol.tla:362` | `P5c_IssuanceProtocol_Sanity.cfg:48` |
| `RefusalAfterReorgUnreachable` | Denies refusal after any reorg | `P5c_IssuanceProtocol.tla:363` | `P5c_IssuanceProtocol_Sanity.cfg:45` |
| `RefusalWithLiveAnchorUnreachable` | Denies refusal with an anchor present; no chronology test | `P5c_IssuanceProtocol.tla:364` | `P5c_IssuanceProtocol_Sanity.cfg:47` |
| `RefusalBuriedAnchorUnreachable` | Denies refusal with a fully buried anchor included at/after refusal time | `P5c_IssuanceProtocol.tla:368–369` | `P5c_IssuanceProtocol_Sanity.cfg:46` |
| `_Broken.Ship` | Weakened burial guard: depth 1 suffices | `P5c_IssuanceProtocol_Broken.tla:75–81` | `P5c_IssuanceProtocol_Broken.tla:90` |
| `_BrokenSilent.Tick` | Advances clock/depth without entering refusal | `P5c_IssuanceProtocol_BrokenSilent.tla:60–65` | `P5c_IssuanceProtocol_BrokenSilent.tla:105` |
| `_BrokenSilent.Refuse` | Separate, postponable refusal transition | `P5c_IssuanceProtocol_BrokenSilent.tla:98–103` | `P5c_IssuanceProtocol_BrokenSilent.tla:105` |

Companion copies retain the meanings above: `_Broken` declares the same constants/variables and lifecycle operators but only the harm invariant; `_BrokenSilent` declares the same constants/variables and all six main invariants plus the latch property. Their respective `Next` operators are selected by their configurations, including `_Green`. (`P5c_IssuanceProtocol_Broken.tla:29–93`, `P5c_IssuanceProtocol_Broken.cfg:9–13`; `P5c_IssuanceProtocol_BrokenSilent.tla:37–136`, `P5c_IssuanceProtocol_BrokenSilent.cfg:16–28`, `P5c_IssuanceProtocol_BrokenSilent_Green.cfg:16–27`.)
`_Broken.vars` is unused: unlike the main and silent companion, that module defines no latch property using its snapshot tuple. (`P5c_IssuanceProtocol_Broken.tla:40–95`.)

## What each invariant checks

These are the six entries under `INVARIANTS`, not the separate `RefusalLatched` property. Quotes below are from the supplied registered excerpt; where there is no direct sentence, the correspondence is explicitly indirect. (`P5c_IssuanceProtocol.cfg:24–34`.)

| Invariant | Plain-language claim enforced | Registered sentence or quoted clause supported | What it does NOT establish |
|---|---|---|---|
| `NoShippedOrphan` | No reachable snapshot records orphaning of a shipped anchor. (`P5c_IssuanceProtocol.tla:236–240`, `P5c_IssuanceProtocol.tla:292`.) | Indirect support for “Issuance is complete only if” the confirmation deadline holds; that sentence does not itself state reorg permanence. (`REGISTERED.txt:10–12`.) | No proof that deep reorgs cannot occur: their exclusion is a precondition of `Reorg`, attributed to A1.6 in the module. (`P5c_IssuanceProtocol.tla:83–86`, `P5c_IssuanceProtocol.tla:237`.) |
| `ShippedIsSound` | Shipping implies an existing anchor between declaration and declaration + Delta, buried to DepthK. (`P5c_IssuanceProtocol.tla:298–303`.) | “Issuance is complete only if” `confirmed_at ≤ declared_issue_time + δ`; also the anchor-time bounds in A2.2. (`REGISTERED.txt:10–12`, `REGISTERED.txt:143–147`.) | The invariant contains no confirmation-time variable or epsilon allowance; the confirmation deadline follows from the actions under the single-clock abstraction, not from this formula alone. No decoupled-clock verifier agreement. (`P5c_IssuanceProtocol.tla:108–117`, `REGISTERED.txt:98–101`.) |
| `ExpiredCannotShip` | An unshipped current attempt past its deadline cannot take `Ship`. (`P5c_IssuanceProtocol.tla:309–310`.) | “If the predicate fails at issuance time, the attempt is discarded and re-issued per the P5 corollary, subject to the attempt bound of A2.3.” (`REGISTERED.txt:83–85`.) | No eventual retry; no old receipt identities or later publication/standing checks. It checks current-action availability, directly reflecting Ship's deadline guard. (`P5c_IssuanceProtocol.tla:260–275`, `P5c_IssuanceProtocol.tla:62–67`; `REGISTERED.txt:59–62`.) |
| `NoSilentDeadlock` | Once the final attempt has expired without shipping, refusal is already true. (`P5c_IssuanceProtocol.tla:318–319`.) | “the transition expiring the final attempt's window records the refusal in the same step”. (`REGISTERED.txt:202–205`.) | No guarantee that this crossing happens; not a general deadlock detector, nor the registered timely-eligibility exception. (`REGISTERED.txt:208–212`, `REGISTERED.txt:183–188`; `P5c_IssuanceProtocol.tla:118–126`.) |
| `RefusedOnlyWhenExhausted` | Refusal means final attempt, expired window, and no shipping. (`P5c_IssuanceProtocol.tla:327–330`.) | “Exhausting them obligates the implementation to terminate issuance in an explicit refusal”; this invariant supplies the converse guard against premature refusal. (`REGISTERED.txt:188–191`.) | No termination or delivery, and no protection for timely-latched eligibility: that state is absent here. (`REGISTERED.txt:183–190`, `REGISTERED.txt:208–215`; `P5c_IssuanceProtocol.tla:118–126`.) |
| `RefusalTimeConsistent` | Refusal exists exactly when its time is non-sentinel; that time lies between zero and now. (`P5c_IssuanceProtocol.tla:344–346`.) | No direct registered timestamp sentence; supports the instrumentation of “the refusal state is entered atomically and latches”. (`REGISTERED.txt:208–209`; `P5c_IssuanceProtocol.tla:339–343`.) | Alone, does not establish the exact entry time or timestamp persistence: an incorrect in-range time could pass. Exact initial stamping comes from `Tick`; the invariant protects the chronology witness against sentinel failure. (`P5c_IssuanceProtocol.tla:206`, `P5c_IssuanceProtocol.tla:339–346`.) |

Stale wording: the configuration's “Durably recorded” comment and variable's “durable refusal record” exceed the explicitly narrowed logical-persistence claim. (`P5c_IssuanceProtocol.cfg:32`, `P5c_IssuanceProtocol.tla:175`, `P5c_IssuanceProtocol.tla:332–336`.)

## The claim

For this bounded, single-clock, pre-latch issuance model, a shipped attempt has an in-window, sufficiently buried anchor that permitted reorgs cannot orphan, an expired unshipped attempt cannot ship, and final expiry without shipping atomically enters a refusal that persists and excludes shipping. (`P5c_IssuanceProtocol.tla:199–207`, `P5c_IssuanceProtocol.tla:236–277`, `P5c_IssuanceProtocol.tla:292–337`, `P5c_IssuanceProtocol.tla:118–126`.)

The committed clean run reports 2,190 distinct states, 3,606 generated states and an empty queue with all six invariants and the latch property selected; the action definitions supply the transition interpretation of those checks. This covers time 0–14, Delta 3, DepthK 2 (k = 3), at most three attempts and at most two reorgs, not arbitrary bounds or deployment values. TLC reports an optimistic fingerprint-collision miss estimate of 1.7×10⁻¹³. (`P5c_IssuanceProtocol.out.trimmed:30–37`, `P5c_IssuanceProtocol.cfg:15–34`, `P5c_IssuanceProtocol.tla:182–207`, `P5c_IssuanceProtocol.tla:237–238`, `REGISTERED.txt:131–135`.)

## The adversary and the abstraction

There is no explicit attacker variable: adversarial choice is modeled as arbitrary selection among enabled actions, including delaying inclusion, causing up to two shallow reorgs, and scheduling Tick before Ship at the deadline. Reissue and Tick have no progress guarantee, so the process may stall without reaching final exhaustion. (`P5c_IssuanceProtocol.tla:62–67`, `P5c_IssuanceProtocol.tla:225–277`.)

The load-bearing **initial conditions** are `Init`: **clean start** (no shipped receipt, orphan harm or refusal), **fresh first attempt** (attempts = 1, declaration/time = 0), and **no initial anchor/history** (absent anchor, depth/reorgs = 0, absent refusal time). These are imposed, not recovered from arbitrary corrupted state. Parameter well-formedness is separately imposed by `ASSUME`; the actual finite values come from the configuration. (`P5c_IssuanceProtocol.tla:158–187`, `P5c_IssuanceProtocol.cfg:15–19`.)

The other load-bearing restrictions are action rules, not initialization assumptions: **single clock and one-block-per-tick deepening**, **depth-threshold permanence**, **guarded shipping**, **fresh declaration/reset on retry**, and **atomic refusal entry**. An adversary cannot change timestamps independently, orphan a deep anchor, bypass Ship, reset refusal, or inject an arbitrary old receipt into the current attempt. Those possibilities have no transitions or fields here. (`P5c_IssuanceProtocol.tla:166–180`, `P5c_IssuanceProtocol.tla:199–207`, `P5c_IssuanceProtocol.tla:225–275`.)

## Why the broken companion fails

- **`_Broken`: insufficient burial before shipping.** It allows depth 1 where the configuration requires 2: one block after inclusion, not inclusion itself. The retained trace shows depth 1 unshipped, then shipped, then a Reorg with anchorAt = −1 and shippedOrphaned = TRUE; TLC names **`NoShippedOrphan`** as violated. Only that invariant is selected, so this run does not isolate the defect against the main six-check set. (`P5c_IssuanceProtocol_Broken.tla:17–25`, `P5c_IssuanceProtocol_Broken.tla:75–81`, `P5c_IssuanceProtocol_Broken.cfg:6–13`, `P5c_IssuanceProtocol_Broken.out.trimmed:2`, `P5c_IssuanceProtocol_Broken.out.trimmed:7–41`.)
- **`_BrokenSilent`: refusal is a separate action.** Tick crosses the final deadline without recording refusal; Refuse may act later. TLC names **`NoSilentDeadlock`** as violated: the retained final snapshot has now = 12, declared = 8, attempts = 3, shipped = FALSE and refused = FALSE, beyond 8 + 3. Even eventual scheduling of Refuse would leave this intervening bad state. (`P5c_IssuanceProtocol_BrokenSilent.tla:60–65`, `P5c_IssuanceProtocol_BrokenSilent.tla:98–105`, `P5c_IssuanceProtocol_BrokenSilent.cfg:12`, `P5c_IssuanceProtocol_BrokenSilent.out.trimmed:2`, `P5c_IssuanceProtocol_BrokenSilent.out.trimmed:31–41`.)
- **Isolation evidence:** `_BrokenSilent_Green` omits only `NoSilentDeadlock` from the main set and retains `RefusalLatched`; its clean run explores 2,400 distinct states with an empty queue. This establishes that the other selected checks survive this mutation. (`P5c_IssuanceProtocol_BrokenSilent_Green.cfg:19–27`, `P5c_IssuanceProtocol_BrokenSilent_Green.out.trimmed:30–37`.)

## What this result does not show

- No full registered lifecycle correspondence: this S = 0, pre-latch model permits a timely-eligible final attempt to lose to Tick, whereas registration makes timely eligibility latch-winning. (`P5c_IssuanceProtocol.tla:118–126`, `REGISTERED.txt:70–85`.)
- No unbounded termination, eventual shipping, retry scheduling or guaranteed refusal delivery; no storage durability or retrieval proof. (`REGISTERED.txt:208–215`, `P5c_IssuanceProtocol.tla:62–67`, `P5c_IssuanceProtocol.tla:332–336`.)
- No timestamp-skew, header authentication, canonical-chain selection or cryptographic verification model; these ten variables and five actions abstract such machinery away, while registration explicitly names header provenance as an obligation. (`P5c_IssuanceProtocol.tla:166–277`, `REGISTERED.txt:120–129`.)
- No conclusion about deep reorgs, more than two reorgs, arbitrary time horizons, or all parameter values. No ordinary deadlock-freedom claim: the module instructs disabling TLC's deadlock check for bounded terminal states; the trimmed output does not preserve the launch command. (`P5c_IssuanceProtocol.tla:237–238`, `P5c_IssuanceProtocol.tla:279–281`, `P5c_IssuanceProtocol.cfg:15–19`, `P5c_IssuanceProtocol.out.trimmed:7–38`.)
- No eventual re-anchoring or lineage/standing enforcement across retained failed receipts: Reissue overwrites the current declaration and anchor. The supplied registration routes later publication/standing elsewhere. (`P5c_IssuanceProtocol.tla:270–275`, `REGISTERED.txt:59–62`.)
- Witnesses establish selected reachable situations, not exhaustive adversarial coverage. The recut buried-anchor witness requires anchorAt ≥ refusedAt and depth ≥ DepthK; the retained trace reaches anchorAt = refusedAt = 12 and depth 2 at time 14. Runs at bounds 12 and 13 are described in comments but are not supplied as separate outputs here. (`P5c_IssuanceProtocol.tla:127–140`, `P5c_IssuanceProtocol.tla:368–369`, `P5c_IssuanceProtocol_Sanity.out.trimmed:43–53`.)

## Correspondence to the registered text

The checks support A2.1's issuance deadline under its explicitly stronger single-clock interpretation, the A2.2 anchor-window bounds in that abstraction, and A2.3's conditional atomic-refusal safety half; they do not establish the full three-conjunct verifier agreement, latched lifecycle, or implementation termination/delivery obligations. (`REGISTERED.txt:98–101`, `REGISTERED.txt:143–147`, `REGISTERED.txt:183–215`; `P5c_IssuanceProtocol.tla:108–126`.)
Amendment 4 §A4.2 ratifies INVALID precedence for a failed required check combined with an unperformable one and qualifies P4's sentence to a “required” check; §A4.3 changes revocation immunity to revocation after **both** anchor and declaration, but neither changes a sentence implemented by this P5c family, whose checks contain no verdict partition or revocation logic. (`AMENDMENT-4.txt:84–119`, `P5c_IssuanceProtocol.tla:292–346`.)
Provenance caveat: the task identifies Amendment 4 as signed on 2026-09-06, while the supplied extract retains “DRAFT — adopted in session, not yet signed”; local correction comments likewise retain “PROPOSED, not adopted”, so those labels should not be mistaken for independently verified current signing status. (`AMENDMENT-4.txt:1–10`, `P5c_IssuanceProtocol.tla:103–107`, `P5c_IssuanceProtocol.cfg:10–14`.)

## Note 2026-09-14 — evidence at the registered depth k = 6 (appended by the AI collaborator; PROPOSED; the commit is the author's)

Item 20's boundary ("`DepthK = 2` represents k = 3, not the registered
strict default k = 6") is now answered by `formal/tla/k6-2026-09-14/`
(Amendment 7 §A7.8, exit item E18): at `Delta = 6, MaxTime = 26,
DepthK = 5, MaxAttempts = 3` the main configuration is green on all
six invariants and `RefusalLatched`, all seven `_Sanity` witnesses
fire, `_Broken` is red on exactly `NoShippedOrphan`, `_BrokenSilent`
on exactly `NoSilentDeadlock`, and `_BrokenSilent_Green` is green.
**Constraint on any instance, found the same day:** `Ship` needs
`depth >= DepthK` inside the window `now <= declared + Delta`, and
depth grows one per `Tick`, so an instance with `Delta < DepthK` never
ships; at `Delta = 3, DepthK = 5` the three ship witnesses survive and
the three ship invariants hold vacuously (`k6-2026-09-14/P5c/P5c_k6_d3_Sanity.out`).
Choose `Delta ≥ DepthK` and `MaxTime = MaxAttempts · (Delta + 1) +
DepthK`. The committed instance is unchanged; nothing above is edited.
(Bridge, same day: the k = 6 instance of `P5cP5P6_Bridge.tla` closes
only with block-timestamp skew ±1 at `MaxBlocks = 7`; at ±2 the space
exceeded 329 M distinct states without closing. All six bridge witnesses
and the three companions behave as registered at skew ±1 —
`formal/tla/k6-2026-09-14/RESULTS-K6.md` §3.)
