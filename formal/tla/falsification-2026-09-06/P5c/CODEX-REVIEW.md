All findings below come from reading the supplied files, not re-running TLC. Output citations use the displayed original line numbers; `tail` identifies the separately numbered final-40-line excerpt.

## 1. Correspondence audit

The main configuration checks five invariants and one action property, at `MaxTime=14, Delta=3, DepthK=2, MaxAttempts=3`; these are finite instances, not a parameter-universal result (`P5c_IssuanceProtocol.cfg:10–28`). The committed output reports no error and 2,190 distinct states (`P5c_IssuanceProtocol.out:14–18`).

- **`NoShippedOrphan`:** `~shippedOrphaned` checks only the harm flag set by the modeled `Reorg`; that action cannot touch a buried anchor (`P5c_IssuanceProtocol.tla:181–186,233–237`). **No matching registered permanence sentence is supplied.** The module quotes an A1.6 assumption—“anchors at depth >= k are treated as permanent”—but A1.6 itself is absent (`P5c_IssuanceProtocol.tla:83–86`). The formula establishes protection against this restricted transition, not package integrity, header authenticity, or general permanent verifiability; those quantities have no representation in the variable list (`P5c_IssuanceProtocol.tla:120–132`; `A1.3.txt:5–14`; `A2.1-A2.3.txt:120–129`).

- **`ShippedIsSound`:** The registered temporal requirements are “`declared_issue_time − ε ≤ anchor_time`”, “`anchor_time ≤ declared_issue_time + δ`”, and “`confirmed_at ≤ declared_issue_time + δ`” (`A2.1-A2.3.txt:143–147`). The formula checks anchor presence, `anchorAt >= declared`, `anchorAt <= declared + Delta`, and sufficient depth (`P5c_IssuanceProtocol.tla:243–248`).
  - Its lower bound is **stronger** than the registered ε-tolerant bound when ε is positive; ε is absent (`P5c_IssuanceProtocol.tla:113–116,246`; `A2.1-A2.3.txt:145`).
  - Its upper anchor bound matches the registered inequality under the declared variable mapping (`P5c_IssuanceProtocol.tla:122–124,247`; `A2.1-A2.3.txt:146`).
  - It has **no confirmation-time conjunct**. Sufficient depth is a different quantity from the designated block’s timestamp (`P5c_IssuanceProtocol.tla:243–248`; `A2.1-A2.3.txt:3–8,147`).
  - Reading the actions supplies an additional argument: one block per tick makes burial occur at `anchorAt + DepthK`, and shipping requires burial and an in-window current time. That implication comes from the transitions, **not the stated invariant alone** (`P5c_IssuanceProtocol.tla:152–154,170–174,205–211`).
  - There is no verifier or issuer/verifier comparison formula for “the verifier evaluates the same conjuncts on the same chain observables” (`A2.1-A2.3.txt:21–28`; `P5c_IssuanceProtocol.tla:120–132,233–282`).

- **`ExpiredCannotShip`:** Registration says expiry applies “only strictly after the boundary, and only to attempts with no timely-latched eligibility” (`A2.1-A2.3.txt:80–82`). The formula instead makes **every currently unshipped attempt** with `now > declared + Delta` unable to execute `Ship`; neither Slack nor eligibility exists (`P5c_IssuanceProtocol.tla:113–132,254–255`). This is stronger against shipping and incompatible with preserving timely eligibility. It is also local to the current declaration: it does not quantify over discarded artifacts (`P5c_IssuanceProtocol.tla:215–220,250–255`).

- **`NoSilentDeadlock`:** Registration narrows the proof to “the refusal state is entered atomically and latches,” while explicitly withholding proof that the crossing occurs (`A2.1-A2.3.txt:201–212`). The formula requires refusal whenever the final current window has expired without shipping; `Tick` implements atomic entry (`P5c_IssuanceProtocol.tla:151–157,263–264`). This matches the **conditional safety construction for this expiry rule**, not registered expiry in full: the latter excludes timely-latched attempts and includes S (`A2.1-A2.3.txt:183–187`). It is not a deadlock predicate or termination property (`P5c_IssuanceProtocol.tla:263–264`).

- **`RefusedOnlyWhenExhausted`:** Registration says “timely-latched eligibility excludes expiry” and makes eligible/finalizing, shipped, and expired/refused mutually exclusive (`A2.1-A2.3.txt:183–187`). The formula checks only `~shipped`, final attempt, and `now > declared + Delta`; it omits the eligible/finalizing alternative and Slack (`P5c_IssuanceProtocol.tla:272–275`). Thus its definition of “exhausted” permits refusal that registration forbids.

- **`RefusalLatched`:** “The refusal state is entered atomically and latches” is the matching registered claim (`A2.1-A2.3.txt:208–210`). `[][refused => refused']_vars` expresses Boolean persistence, including stuttering; atomic entry is supplied separately by `Tick` and `NoSilentDeadlock` (`P5c_IssuanceProtocol.tla:151–157,263–264,277–282`). It does **not** establish “explicit refusal, durably recorded” as an operational outcome; registration expressly leaves durability, retrieval, and reporting outside this proof (`A2.1-A2.3.txt:189–191,213–215`).

- **Sanity formulas:** All seven are negated reachability witnesses, not registered safety requirements. There is no registered sentence asserting that shipping/refusal is unreachable; their intended outcome is violation (`P5c_IssuanceProtocol_Sanity.cfg:5–14,32–39`; `P5c_IssuanceProtocol.tla:295–301`).

- **Companion configurations:** `_Broken` checks only `NoShippedOrphan`; `_BrokenSilent` checks the main set; `_BrokenSilent_Green` removes only `NoSilentDeadlock`. Their correspondence limitations are therefore those above, with no additional registered property introduced (`P5c_IssuanceProtocol_Broken.cfg:12–13`; `P5c_IssuanceProtocol_BrokenSilent.cfg:15–23`; `P5c_IssuanceProtocol_BrokenSilent_Green.cfg:15–22`).

**Registered clauses without a corresponding checked formula:**

- Conditional shipping opportunity when `B−C <= S`, inclusive boundary eligibility, and persistence of eligibility through scheduling delay (`A2.1-A2.3.txt:45–58,70–83`; `P5c_IssuanceProtocol.tla:233–301`).
- Full three-conjunct issuer/verifier agreement, tolerance-policy handling, and designated-header confirmation-time evaluation (`A2.1-A2.3.txt:14–28,91–101,143–147`; `P5c_IssuanceProtocol.tla:233–282`).
- Header availability, authentication, canonical-chain selection, and bundle/store conflict handling (`A2.1-A2.3.txt:159–167`; `P5c_IssuanceProtocol.tla:120–132,222`).
- Non-waivability and the `INVALID`/`UNVERIFIABLE` partition (`A2.1-A2.3.txt:168–171`; `P5c_IssuanceProtocol.tla:233–282`).
- No standing for operationally abandoned but chain-valid artifacts (`A2.1-A2.3.txt:58–62,151–158`; `P5c_IssuanceProtocol.tla:120–132`).
- The N-attempt bound is enforced by initialization and `Reissue`, but has no separately checked invariant; termination, delivery, and durable storage have no checked formula and are expressly contractual (`P5c_IssuanceProtocol.tla:138,215–220,233–282`; `A2.1-A2.3.txt:183–215`).

## 2. Vacuity

The committed sanity output reports every configured witness violated:

| Reachable predicate | Negated witness and definition | Committed violation |
|---|---|---|
| `shipped` | `ShipUnreachable`, `P5c_IssuanceProtocol.tla:295` | `P5c_IssuanceProtocol_Sanity.out:14` |
| `shipped /\ attempts > 1` | `ReissueShipUnreachable`, `.tla:296` | `_Sanity.out:150` |
| `shipped /\ reorgs > 0` | `ReorgShipUnreachable`, `.tla:297` | `_Sanity.out:71` |
| `refused` | `RefusalUnreachable`, `.tla:298` | `_Sanity.out:262` |
| `refused /\ reorgs > 0` | `RefusalAfterReorgUnreachable`, `.tla:299` | `_Sanity.out:785` |
| `refused /\ anchorAt # NoAnchor` | `RefusalWithLiveAnchorUnreachable`, `.tla:300` | `_Sanity.out:429` |
| `refused /\ depth >= DepthK` | `RefusalBuriedAnchorUnreachable`, `.tla:301` | `_Sanity.out:607` |

Here `.tla` and `_Sanity.out` abbreviate the corresponding full filenames in the first row.

**The buried-refusal witness does not establish its advertised chronology.** It says only `refused /\ depth >= DepthK`; it does not record whether burial or anchoring occurred after refusal (`P5c_IssuanceProtocol.tla:165–169,301`). A reader-derived trace reaches it at **MaxTime=12**: `Tick×4; Reissue; Tick×4; Reissue; Anchor` at `declared=now=8`; `Tick×4` reaches `now=12, depth=2, refused=TRUE`. Every step follows the supplied actions (`P5c_IssuanceProtocol.tla:151–174,215–220`).

Consequently, the assertion that this witness is unreachable at 12, or catches missing post-refusal headroom, is false. Fourteen permits the intended chronology, but the predicate does not test it (`P5c_IssuanceProtocol.cfg:6–9`; `P5c_IssuanceProtocol_Sanity.cfg:11–14`; `P5c_IssuanceProtocol.tla:165–169,301`).

Shipping witnesses defeat simple `shipped=FALSE` vacuity for `ShippedIsSound`; refusal witnesses exercise refusal-dependent checks. The displayed sanity tail explicitly reaches the final-expired antecedent with refusal true (`P5c_IssuanceProtocol.tla:243–248,263–282`; `P5c_IssuanceProtocol_Sanity.out:tail:25–34`).

Nevertheless, **post-shipment `Reorg` is never enabled**: shipping requires `depth >= DepthK`, whereas reorganization requires `depth < DepthK`. Thus `NoShippedOrphan` excludes only harms whose sole producing transition has been disabled by the permanence assumption; it does not exercise deep-reorganization resistance (`P5c_IssuanceProtocol.tla:182–185,207,237`).

`ExpiredCannotShip` is a direct contradiction between its antecedent and `Ship`’s time guard, even for hypothetical states unrelated to reachability. Its success does not independently validate the expiry definition (`P5c_IssuanceProtocol.tla:208,254–255`).

**Evidence limitation:** committed traces cite older source locations: sanity calls `Tick` lines 137–142, while the supplied `Tick` is lines 151–157. The files alone do not establish source identity between these runs and the supplied revision (`P5c_IssuanceProtocol_Sanity.out:tail:25`; `P5c_IssuanceProtocol.tla:151–157`).

## 3. Attack attempts

1. **Ship shallow, then orphan.** From initialization: `Anchor(now=0); Tick(now=1,depth=1); Ship; Reorg`. The prefix is representable; main `Ship` rejects the attempted step at `depth >= DepthK` with `DepthK=2`. The broken model admits it and sets the harm flag on reorganization (`P5c_IssuanceProtocol.cfg:13`; `P5c_IssuanceProtocol.tla:134–139,170–185,205–208`; `P5c_IssuanceProtocol_Broken.tla:63`; `_Broken.out:tail:15–35`).

2. **Deep reorganization after compliant shipping.** `Anchor(0); Tick(1); Tick(2,depth=2); Ship; Reorg` that removes the buried block. **UNREPRESENTABLE:** `Reorg` fails its `depth < DepthK` conjunct. No invariant rejects a represented deep-reorg result; the environment forbids the event (`P5c_IssuanceProtocol.tla:151–185,205–211`).

3. **Expire a timely-eligible final attempt.** `Tick×4; Reissue(declared=4,attempts=2); Tick×4; Reissue(declared=8,attempts=3); Tick(now=9); Anchor(9); Tick(10,depth=1); Tick(11,depth=2); Tick(12)`. At 11 the fused-clock interpretation gives `C=B=11=declared+Delta`, so eligibility is timely even at S=0. The next tick sets refusal. **Representable; no checked conjunct rejects it.** `RefusedOnlyWhenExhausted` accepts the result. Registration requires boundary eligibility to latch and prevent precisely this expiry (`P5c_IssuanceProtocol.tla:151–174,215–220,263–282`; `A2.1-A2.3.txt:76–83`).

4. **Supply a backdated header.** Declare at wall time 0, then `Anchor(anchor_time=−2)` under ε=1. Registration’s lower bound rejects it. **UNREPRESENTABLE:** `Anchor` assigns `anchorAt'=now=0`; no action accepts a separately chosen block timestamp (`A2.1-A2.3.txt:145`; `P5c_IssuanceProtocol.tla:134–139,170–174,222`).

5. **Time passes without confirmations.** `Anchor(0);` advance wall time to 1 while retaining `depth=0`, then continue through the deadline without burial. **UNREPRESENTABLE after inclusion:** every time-advancing step increments subthreshold depth. Delaying initial anchoring is representable but does not model this interleaving (`P5c_IssuanceProtocol.tla:151–160,222`).

6. **Replay a discarded attempt after retry.** `Anchor(0); Tick×4; Reissue(declared=4);` publish the old declaration/anchor as a separate artifact. **UNREPRESENTABLE:** reissue overwrites the sole declaration and anchor; there is no artifact collection or publication action. `ExpiredCannotShip` cannot reject publication of an object no longer represented (`P5c_IssuanceProtocol.tla:120–132,215–222,254–255`; `A1.3.txt:11–14`; `A2.1-A2.3.txt:58–62`).

7. **Present a fabricated canonical-looking header or alter a shipped receipt.** `Anchor(0); Tick×2; Ship;` substitute headers giving `confirmed_at=2`, or change receipt bytes. **UNREPRESENTABLE:** neither bytes, headers, canonicality, nor verification inputs exist. No conjunct rejects these registered adversary operations (`P5c_IssuanceProtocol.tla:120–132,222`; `A1.3.txt:5–10,13–16`; `A2.1-A2.3.txt:120–129`).

8. **Stall without refusal.** Remain at initialization forever by stuttering, or postpone reissue after the first expiry. No fairness or eventual-refusal property is configured; the header expressly allows these behaviors. No checked safety conjunct rejects them (`P5c_IssuanceProtocol.cfg:16–28`; `P5c_IssuanceProtocol.tla:62–67,263–282`; `A2.1-A2.3.txt:208–212`).

## 4. Companions

- **`_Broken`:** The output reports `NoShippedOrphan` red, exactly its sole configured and named invariant. Its displayed trace ships at `depth=1` and then reorganizes to `shippedOrphaned=TRUE` (`P5c_IssuanceProtocol_Broken.cfg:12–13`; `P5c_IssuanceProtocol_Broken.tla:10–15`; `P5c_IssuanceProtocol_Broken.out:14,tail:15–35`). No isolation claim about the other main properties is supported because they are neither defined nor configured here (`P5c_IssuanceProtocol_Broken.tla:76–81`).

- **The shallow companion can fail for the intended defect at the committed constants.** It is not blocked by the time horizon or reorg-count limit: the trace uses `now=1,reorgs=1` (`P5c_IssuanceProtocol_Broken.out:tail:27–35`). But with allowed `DepthK=1`, its changed guard becomes identical to the main guard and the advertised failure disappears. A green run would therefore not necessarily mean “the depth-k rule buys nothing,” contrary to its unconditional comment (`P5c_IssuanceProtocol_Broken.tla:10–12,21–22,54–55,63`).

- **Its defect description is off by one.** “Only inclusion (depth >= 1)” does not describe this convention: inclusion sets depth 0. The mutation ships after one subsequent block, i.e. two Bitcoin confirmations (`P5c_IssuanceProtocol_Broken.tla:4–5,47–49,60–63`; `A2.1-A2.3.txt:131–135`).

- **`_BrokenSilent`:** The red output names `NoSilentDeadlock`; the final state has `now=12,declared=8,attempts=3,shipped=FALSE,refused=FALSE` (`P5c_IssuanceProtocol_BrokenSilent.out:14,tail:26–35`). The separate Green configuration checks all remaining main invariants and `RefusalLatched`; its output reports no error and 2,310 distinct states. Together the committed outputs support exactly the named checked-set isolation, subject to source-version limitations (`P5c_IssuanceProtocol_BrokenSilent_Green.cfg:15–22`; `_BrokenSilent_Green.out:14–18`).

- **The silent failure does not require indefinite postponement or lack of fairness.** The crossing `Tick` itself produces the violating state; a `Refuse` immediately afterward cannot erase that safety violation. The final state is not necessarily deadlocked—`Refuse` is enabled there (`P5c_IssuanceProtocol_BrokenSilent.tla:53–58,91–98,117–118`). The actual defect is non-atomic entry, as the companion also states (`P5c_IssuanceProtocol_BrokenSilent.tla:23–24`).

## 5. Scoped abstractions

**Named in module comments:**

- Fused wall/block time; one block per tick; no timestamp skew or ε-side issuance cases; S=0 lifecycle instance; eligibility latching deferred (`P5c_IssuanceProtocol.tla:23–44,79–82,103–106`).
- Buried anchors permanent by assumption; shallow-only reorganization; capped reorg count for reachability witnesses (`P5c_IssuanceProtocol.tla:83–86,128,176–183`).
- Finite time horizon, capped depth, integral boundary scheduling; N treated as protocol semantics rather than merely a search bound (`P5c_IssuanceProtocol.tla:87–101,124,141–142,193–204`).
- Arbitrarily delayed initial anchoring through postponement of `Anchor` (`P5c_IssuanceProtocol.tla:159–160`).
- Atomic abstract refusal and Boolean persistence; storage, retrieval, reporting, and liveness excluded (`P5c_IssuanceProtocol.tla:47–76,277–282`).
- Current-attempt-only state and destructive replacement on retry; bounded terminal deadlocks with deadlock checking disabled (`P5c_IssuanceProtocol.tla:122–123,213–226`).
- `_Broken` retains those transition simplifications except its depth guard; `_BrokenSilent` substitutes separately scheduled refusal without fairness (`P5c_IssuanceProtocol_Broken.tla:13–15,39–76`; `P5c_IssuanceProtocol_BrokenSilent.tla:5–11,26–27,53–98`).

**Visible abstractions not explicitly scoped as such by the module:**

- No package bytes, signatures, keys, manifests, context/type boundaries, authority channels, or adversarial input actions. None of A1.3’s six capabilities is directly encoded (`A1.3.txt:3–16`; `P5c_IssuanceProtocol.tla:120–132,222`).
- No block identities/heights, competing chains, header source, chain-work comparison, or explicit `confirmed_at`; timestamps and depth stand in for these structures (`A2.1-A2.3.txt:3–8,120–129`; `P5c_IssuanceProtocol.tla:120–132`).
- No separate eligibility/observation event or B−C measurement, no verifier policy or verdict, and no standing state (`A2.1-A2.3.txt:23–28,45–62,168–171`; `P5c_IssuanceProtocol.tla:120–132`).
- No retained retry lineage, multiple concurrently pending artifacts, crash/recovery, or delivery transition; actions update a single shared state atomically (`P5c_IssuanceProtocol.tla:120–132,151–222`).
- The depth assumption excludes `DepthK=0`, so the registered mapping cannot instantiate k=1; the checked `DepthK=2` represents k=3, not the stated strict default k=6 (`P5c_IssuanceProtocol.tla:115–116`; `P5c_IssuanceProtocol.cfg:13`; `A2.1-A2.3.txt:131–135`).

## 6. Verdict on the module header's honesty

**The header overstates correspondence in specific places.** “Ship’s ‘now <= declared + Delta’ at depth k IS the chain-time predicate” is false as an equivalence even with fused clocks. `Anchor(0); Tick×4` gives burial timestamp 2 within δ=3, but current time 4 disables shipping. Registration itself correctly calls this guard “locally stronger” (`P5c_IssuanceProtocol.tla:23–25,42–43,151–154,205–208`; `A2.1-A2.3.txt:98–101`).

The header acknowledges that eligibility latching is absent, but that makes this **an incomplete S=0 instance**, not the registered lifecycle specialized only by Slack. Its boundary-race comment expressly permits expiry after timely eligibility; registration expressly supersedes that race with latch-winning eligibility (`P5c_IssuanceProtocol.tla:34–44,193–204`; `A2.1-A2.3.txt:70–83`). Attack 3 reaches the mismatch while satisfying the checked formulas.

The refusal proof-versus-contract wording accurately limits the result to atomic Boolean entry and persistence. However, “genuine exhaustion” means only the model’s deadline condition, which lacks the registered eligibility exception (`P5c_IssuanceProtocol.tla:55–72,272–282`; `A2.1-A2.3.txt:183–187`).

The claimed verifier handoff is not checked here: no verifier relation or explicit confirmation timestamp appears. Permanence is assumed, and the actual result is that shipping respects that assumption (`P5c_IssuanceProtocol.tla:13–15,83–86,120–132,233–248`).

The claimed post-refusal witness coverage is stronger than its formula, and the claimed necessity of MaxTime=14 for that witness is contradicted by the readable MaxTime=12 trace in §2 (`P5c_IssuanceProtocol.tla:93–101,165–169,301`).

Finally, the teaching annotation labels itself non-discharging and retracts its earlier burial-delay alarm. Its external-run claims cannot supply missing evidence here; its statement that anchor and confirmation times “may coincide” under this single clock is incompatible with positive `DepthK` and one tick per subsequent block (`P5c_IssuanceProtocol.READ-AND-CHALLENGE.md:3–11,184–189,223–234`; `P5c_IssuanceProtocol.tla:115,152–154,172`).