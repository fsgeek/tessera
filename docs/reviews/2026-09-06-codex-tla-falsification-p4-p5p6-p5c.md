# Cross-family falsification reviews: P4, P5/P6, P5c TLA+ models (Codex, gpt-6-astra)

Agreement-gate falsification reviews (`formal/PROPERTIES.md` cross-cutting
list, "Agreement-gate falsification reviews run by non-author models";
`formal/suite/ENUMERATION.md` amendment note 5 item 1, cross-family
first) on the three checked TLA+ models that had never had one:
`P4_VerifierStates`, `P5P6_TemporalRevocation`, `P5c_IssuanceProtocol`.
Dispatched by the AI collaborator on 2026-09-06 under the author's
standing instruction that Codex dispatches run when needed. Nothing here
changes a property status; dispositions below are the collaborator's
and carry no authority until the author reads them. Three items are
routed to the author.

## Reproducibility record

- **Reviewer:** OpenAI Codex CLI 0.153.3, model `gpt-6-astra` (verified
  from each run's log line `model: gpt-6-astra`), three parallel
  non-interactive runs, one per model family. Jailing was by content,
  not by OS sandbox: each run received exactly one prompt with every
  input file inlined (`cat -n`), because Codex's own sandbox cannot
  start on this host. The reviewer had no shell and did not re-run TLC;
  every claim is from reading. Prompt template and all inputs archived
  under `formal/tla/falsification-2026-09-06/{P4,P5P6,P5c}/`.
- **Inputs per jail:** the correct module, every broken companion and
  sanity configuration, the committed `.out` files (trimmed to
  invariant/error/summary lines plus their final forty lines), the
  registered property text (Amendment 1 P4 with §A1.2.1; Amendment 1
  P5/P6 with Amendment 2 §A2.1–A2.2; Amendment 2 §A2.1–A2.3 for P5c),
  and §A1.3. **Not in any jail, and material to two findings:** the
  bridge models `P5cP5P6_Bridge*.tla` and `P5cP5P6_BridgeSlack_Latch.tla`.
  The reviewer therefore reports as uncovered two things those modules
  cover; dispositions say so. Lesson for later jails: include every
  sibling module a header cites.
- **Mechanical checks the collaborator ran on the findings** (TLC
  2.x, `~/.local/lib/tla2tools.jar`, 2026-09-06, outputs archived in
  the same directory): (1) `P5c_IssuanceProtocol_Sanity.cfg` at
  `MaxTime = 12` instead of 14 — `RefusalBuriedAnchorUnreachable` is
  violated 21 times; the reviewer's reachability claim is **confirmed**.
  (2) `git diff 1640781 5db6e94 -- P5c_IssuanceProtocol.tla` contains
  comment lines only; the committed `.out` traces cite pre-edit line
  numbers (`Tick` 137–142 vs. 151–157) for that reason and for no
  other. **Confirmed cosmetic.**

## Consolidated findings and collaborator dispositions

Labels: **Accepted** (a defect in a header, comment, witness, or the
tracker; fix is collaborator work); **Boundary** (true, already a named
abstraction or assigned to another leg; the reading aid must say it);
**Covered elsewhere** (true of the jailed module, false of the tree);
**Rejected** (with reason); **ROUTED** (needs an author act).

### P4 — fail-closed state logic

1. **Precedence when one required check fails and another is
   unperformable is an unratified modelling decision.** The module says
   so in its own comment ("for author ratification", lines 49–52); the
   verdict function returns `INVALID`; §A1.2.1 orders the two cases
   separately and never the combination. **ROUTED (1).** Recommendation:
   ratify `INVALID` as modelled — a definite failure is stronger
   evidence than an open question, both are fail-closed, and the
   alternative makes a verdict depend on evaluation order. One
   sentence, entered as a dated author note in §A1.2.1's vicinity or in
   the next amendment.
2. **A waived check that cannot be performed yields `VALID_DEGRADED`**
   (reviewer's attack 4). P4's sentence "a check that cannot be
   performed yields `UNVERIFIABLE`, never any `VALID` state" is
   unqualified; §A1.2.1's lattice qualifies it to non-waivable checks
   and lists exactly three waivable categories, all declared
   redundancy. Waiving an unperformable redundancy check by explicit
   policy — "accepting fewer than all external manifest-authority
   evidences" when one cannot be fetched — is the lattice's stated
   purpose. **The model agrees with §A1.2.1; P4's sentence is imprecise
   as written.** **ROUTED (2).** Recommendation: a prose-precision
   repair in the A3 §2 style — P4's sentence gains the word *required*
   ("a required check that cannot be performed…"), which is what the
   model checks and what §A1.2.1 already says. Not a weakening; the
   operative claim is unchanged.
3. **Recording and authorization of the waiver are absent; the abstract
   checks `c1`–`c5` are not mapped to §A1.2.1's concrete categories.**
   **Boundary.** Recording is an H1a/Band 1 artifact (A3's refusal and
   verdict-record dispositions); the mapping belongs in the reading
   aid: `c1`,`c2` stand for the non-waivable class (five categories),
   `c3`–`c5` for the three waivable categories; the invariants do not
   depend on the count.
4. **Multi-invariant companion runs stop at the first violation and so
   certify nothing about the other configured invariants** (also true
   of `P5P6_*Broken*`). **Accepted.** P5c already carries the
   `_Green` pattern (companion re-run with the red invariant removed);
   P4 and P5P6 companions get the same. Mechanical; adds `.cfg`/`.out`
   pairs, no model change.
5. **`_Broken`'s "same invariants as the correct module" comment is
   incomplete** (lacks the four exact-classification formulas).
   **Accepted**, comment fix.
6. **Header "the machine-checkable form of P4 and the waiver lattice"
   overstates.** **Accepted.** The header narrows to what the eleven
   formulas discharge over the configured status/waiver assignments;
   the reading aid carries the rest.
7. Bundles, replay, key substitution unrepresentable (attack 6).
   **Boundary** by design: P4 is the state logic; those are P1/P3/P7
   and the symbolic suite, and the coverage map's `Accept` ↔ P4 join
   (author ruling 2026-08-29) is the seam.

### P5/P6 — temporal soundness, revocation

8. **`VerifierOwnsTolerances` compares against the global maxima, not
   the verifier's chosen policy**, so a receipt enlarging δ from 0 to 1
   under `DeltaMax = 3` passes it. **Accepted as fact.** Ownership is
   carried by `ReceiptIndependence` (verdict invariant under every
   receipt-tolerance pair), and the `_BrokenTolStrict` companion shows
   exactly that division. The module's "strictly stronger" comment is
   qualified accordingly; no invariant changes.
9. **`_BrokenTol`'s header names the wrong witness quantity**
   (anchor-to-declared gap; the printed red conjunct is
   confirmedAt-to-declared). **Accepted**, comment fix.
10. **Registered sentence "Revocation effective *after* `anchor_time`
    does not retroactively change the verdict" (Amendment 1 line 212)
    is unqualified**; the model additionally requires
    `revoked > declared`, so when the anchor precedes the declaration
    (possible within ε) a revocation after the anchor but before the
    declared time still invalidates — correctly, per the registered
    two-conjunct rule two lines later. **ROUTED (3).** Recommendation:
    prose-precision repair — "after both `anchor_time` and
    `declared_issue_time`". The model is right; the sentence is loose.
11. **The assumption `signed ≤ anchor` is imposed at initialization and
    is the load-bearing order relation for `ForgeryRejected`; backward
    header skew can violate it.** **Boundary, already registered.**
    This is A2.1's timestamp-skew residual, carried into the first-link
    decision as "δ plus A2.1's skew residuals" (first-link DECISION.md
    §residuals). The module names the assumption (lines 33–36) but does
    not cite the residual; the reading aid will.
12. **Header claims correspondence with P5c's `Ship` is "exact by
    construction".** **Covered elsewhere, header stale.** The tracker
    records that this join was *asserted, not checked* until the bridge
    model (`P5cP5P6_Bridge.tla`, 2026-07-21) checked it as the
    `ShippedDesignatedAgree` invariant with the `_BrokenAnchorSubst`
    companion red. The P5P6 header predates the bridge and should cite
    it instead of claiming construction.
13. `AuthorizedAtDeclared` substitutes `declared < revoked` for
    `key_authorized(declared)`; no activation time. **Boundary**: the
    lifecycle is deferred (docket item 18) and issuer-key lifetime is
    now docket item 26; the reading aid states the substitution.
14. Header availability/authentication, canonical-chain selection,
    depth-k derivation, verdict partition absent. **Boundary,
    assigned**: header authentication is A2.2's H1a obligation; depth
    arithmetic is the bridge's; the partition is P4's.

### P5c — issuance corollary

15. **The `RefusalBuriedAnchorUnreachable` witness does not encode
    chronology and is reachable at `MaxTime = 12`**; the module comment
    and the tracker's "+DepthK headroom = 14 exercises post-refusal
    burial" are false as stated. **Accepted, CONFIRMED by re-run.**
    The witness `refused /\ depth >= DepthK` is satisfied by an anchor
    placed *before* refusal and buried by the final ticks. Fix: a
    recut adding the chronology (e.g. record `depth` at the refusing
    `Tick` and witness `refused /\ depth > depthAtRefusal`), re-run,
    and correct the tracker sentence. Collaborator work; small.
16. **A timely-eligible final attempt can expire (attack 3); registration
    makes eligibility latch-winning.** **Covered elsewhere.** The
    module states latching is deferred (its S = 0, pre-latch instance);
    the latch semantics are modelled and checked in
    `P5cP5P6_BridgeSlack_Latch.tla` (Codex constraint 1, 2026-07-21).
    The P5c header must say which module carries the registered
    lifecycle and that P5c is the earlier instance.
17. **`ShippedIsSound` has no confirmation-time conjunct and no ε; the
    header's "IS the chain-time predicate" is false as an equivalence.**
    **Accepted, header narrows.** A2.1 itself calls the fused guard
    "locally stronger"; the decoupled three-conjunct predicate is the
    bridge's. Same disposition as 16 for where the reader is sent.
18. **`_Broken`'s comment "only inclusion (depth >= 1)" is off by one**
    under the module's convention (inclusion is depth 0). **Accepted**,
    comment fix.
19. **Committed `.out` traces cite stale line numbers.** **Accepted as
    cosmetic, CONFIRMED comment-only.** Outputs will be regenerated
    with the recut in 15.
20. **`DepthK = 2` represents k = 3, not the registered default k = 6;
    finite instance.** **Boundary**; the reading aid states the
    instance and why it suffices for the invariants checked.
21. Post-shipment `Reorg` is never enabled, so `NoShippedOrphan`
    excludes only the harm its permanence assumption disables.
    **Boundary, named** (A1.6 permanence, module lines 83–86); the
    reorg re-verification residual is already tracked as NOT discharged
    (tracker, bridge entry).

## Net effect

No invariant, configuration, or property status changes. Three
registered-text precision items are routed to the author (1, 2, 10),
none of which weakens a claim: one ratifies a precedence the model
already implements, two add a qualifier the registered lattice already
contains. Six header/comment corrections and two mechanical additions
(the `_Green` companion pattern for P4 and P5P6; the P5c chronology
witness recut) are collaborator work and feed the reading aids owed
under ENUMERATION note 5. Two "uncovered" findings were covered by
sibling modules the jail omitted; that is a dispatch defect, recorded.

Under ENUMERATION note 5 item 1 as drafted, this satisfies the
cross-family review condition for P4, P5, P5c, and P6; `discharged`
additionally requires the author's read of each model's plain-language
statement, which does not yet exist for these three modules.

---

## Reviewer output — verbatim

The three documents below are the reviewer's final messages, unedited.

### Reviewer output — P4 (`model: gpt-6-astra`)

## 1. Correspondence audit

All claims below come from reading the supplied files, not re-running TLC. Citations to `.out` use the displayed final-block numbering unless marked **extracted**.

The main configuration checks eleven invariants; the broken configuration checks the first seven; the sanity configuration checks four negated reachability witnesses. (`P4_VerifierStates.cfg:8–19`; `P4_VerifierStates_Broken.cfg:8–15`; `P4_VerifierStates_Sanity.cfg:12–16`)

| Checked formula | Registered sentence it claims to discharge | Correspondence finding |
|---|---|---|
| `Partition` | “The verifier's four states partition all outcomes.” (`REGISTERED-P4.txt:13–14`) | Checks only membership of a derived scalar in four strings. Single-valuedness comes from the function encoding; coverage concerns legal abstract input assignments, not bundle outcomes or execution traces. (`P4_VerifierStates.tla:33–44,56–65,71–73`) |
| `Monotonicity` | “A package failing any non-waivable check is `INVALID` under **every** policy — no degraded policy may promote it (*monotonicity*).” (`REGISTERED-P4.txt:28–30`) | Matches for abstract statuses and **legal** waiver subsets. It neither identifies the registered non-waivable checks nor tests policies attempting to waive them: such policies are excluded from initialization and quantification. (`P4_VerifierStates.tla:25–29,37–42,77–79`; `P4_VerifierStates.cfg:2–3`) |
| `NoSilentPromotion` | “A non-waivable check that *cannot be performed* yields `UNVERIFIABLE`, never any `VALID` state…” (`REGISTERED-P4.txt:30–33`) | Weaker than the literal classification: permits `INVALID` whenever its antecedent holds, without itself requiring a simultaneous failure. It protects only non-waivable checks, whereas P4's earlier sentence says “A check.” (`REGISTERED-P4.txt:14–16`; `P4_VerifierStates.tla:84–87`) |
| `ValidNeedsNonWaivablePass` | “A package failing any non-waivable check is `INVALID` under **every** policy”; an unperformable one yields “never any `VALID` state.” (`REGISTERED-P4.txt:28–33`) | A necessary-condition corollary under the three-status alphabet. Weaker than the prescribed distinctions between `INVALID` and `UNVERIFIABLE`; does not establish that an actual check was performed correctly. (`P4_VerifierStates.tla:31,89–93`) |
| `StrictMeansEverything` | Closest supplied sentence: “A check that cannot be performed yields `UNVERIFIABLE` — never any `VALID` state, under any trace.” (`REGISTERED-P4.txt:14–16`) | Requires all abstract checks to pass for strict validity, including waivable checks. It does not itself require an empty waiver set or establish a default. Its comment invokes §3.1, whose substantive text is not supplied here; the supplied registration does not explicitly define strict validity as “everything passed.” (`P4_VerifierStates.tla:95–98`; `REGISTERED-P4.txt:41–43`) |
| `DegradedNeedsExplicitWaiver` | “`VALID_DEGRADED` arises only from an explicit, recorded policy within A1.2.1's waivable set, never as a default or a fallback.” (`REGISTERED-P4.txt:16–17`) | Checks only that the waiver set is nonempty and legal. “Explicit,” “recorded,” authorization, default selection, and fallback behavior are absent. Nonemptiness is an additional formal interpretation; the registered sentence does not state it expressly. (`P4_VerifierStates.tla:35,40–44,100–103`) |
| `UnverifiableIsHonest` | “A check that cannot be performed yields `UNVERIFIABLE`…” (`REGISTERED-P4.txt:14–15`) | Reverses the implication: `UNVERIFIABLE` requires an unperformable required check. Adds the absence of required failures. Thus it supplies a converse and failure precedence, while alone not guaranteeing the registered forward implication. (`P4_VerifierStates.tla:107–110`) |
| `ExactInvalid` | “A required check that fails yields `INVALID`.” (`REGISTERED-P4.txt:14`) | Strengthens “yields” to iff, forbidding `INVALID` for any other reason. “Required” means precisely `Checks \ waived`; no other rejection causes exist. (`P4_VerifierStates.tla:54,120,124–125`) |
| `ExactUnverifiable` | “A check that cannot be performed yields `UNVERIFIABLE` — never any `VALID` state, under any trace.” (`REGISTERED-P4.txt:14–16`) | Weakens the antecedent to a **required** unperformable check with **no required failure**, and adds the converse. A waived unperformable check can coexist with validity; a required failure overrides unperformability. (`P4_VerifierStates.tla:120–121,127–128,134–135`) |
| `ExactStrict` | Closest supplied sentence: “The verifier's four states partition all outcomes.” (`REGISTERED-P4.txt:13–14`) | Adds a particular classification: strict iff empty waiver set and every check passes. The supplied text does not explicitly specify this biconditional. (`P4_VerifierStates.tla:130–132`) |
| `ExactDegraded` | “`VALID_DEGRADED` arises only from an explicit, recorded policy within A1.2.1's waivable set…” (`REGISTERED-P4.txt:16–17`) | Adds sufficiency: any nonempty legal waiver set with all remaining checks passing **must** yield degraded validity. Omits recording and authorization, and allows waived checks to have any status. It also selects degraded validity when all checks passed but the waiver set is nonempty. (`P4_VerifierStates.tla:40–42,122,134–135`) |

The broken module implements the same first seven formulas, with the same correspondence limitations, against a different verdict function. Its “Same invariants as the correct module” comment is incomplete: it contains none of the four exact-classification formulas checked by the main configuration. (`P4_VerifierStates_Broken.tla:38–73`; `P4_VerifierStates.cfg:16–19`)

The sanity formulas have **no registered sentence claiming that each verdict must be reachable**. They are deliberately false auxiliary assertions: `VerdictNeverStrict`, `VerdictNeverDegraded`, `VerdictNeverInvalid`, and `VerdictNeverUnverifiable` deny the corresponding verdict. Their comments describe this testing purpose. (`P4_VerifierStates.tla:137–148`; `P4_VerifierStates_Sanity.cfg:1–4`)

Registered obligations without a corresponding formula or representation:

- **Recording and authorization:** “Every `VALID_DEGRADED` verdict records the precise waived check set and the policy that authorized the waiver.” The state contains a waiver set, but no record, policy identity, authorization relation, or recording action. (`REGISTERED-P4.txt:41–43`; `P4_VerifierStates.tla:35–44`)
- **The concrete waiver boundary:** registration names canonical integrity, domain separation, framing, key binding, and temporal consistency as non-waivable, and permits only specified redundancy weakening. The configuration supplies anonymous `c1`–`c5`, with only `c1,c2` non-waivable; no mapping establishes either category's correspondence. (`REGISTERED-P4.txt:25–39`; `P4_VerifierStates.cfg:2–3`)
- **Default/fallback behavior and “under any trace”:** there is no policy-selection process or changing execution, only arbitrary initial policies and stuttering. (`REGISTERED-P4.txt:15–17`; `P4_VerifierStates.tla:40–44`)
- **Literal unperformability classification:** the registered unconditional statements are not discharged as written. The model explicitly marks fail-over-unperformable precedence as a decision “for author ratification”; no ratification appears in the supplied registered text. (`REGISTERED-P4.txt:14–16,30–33`; `P4_VerifierStates.tla:49–52,56–63`)

## 2. Vacuity

The intended witnesses are `Verdict = "VALID_STRICT"`, `"VALID_DEGRADED"`, `"INVALID"`, and `"UNVERIFIABLE"`, obtained by falsifying the four `VerdictNever…` assertions. All four fired in the committed output: strict at **extracted line 15**, degraded at **extracted line 19**, invalid at **extracted line 50**, and unverifiable at **extracted line 83**. (`P4_VerifierStates.tla:145–148`; `P4_VerifierStates_Sanity.out`, extracted lines cited)

The displayed tail additionally exhibits all checks unperformable with `waived={c3,c5}`, and reports `VerdictNeverUnverifiable` violated. This directly witnesses the antecedent of `NoSilentPromotion`, not merely the existence of an unverifiable verdict. (`P4_VerifierStates_Sanity.out:8–14`; `P4_VerifierStates.cfg:3`; `P4_VerifierStates.tla:84–87`)

The sanity comment overstates what **four verdict witnesses alone** establish: `Monotonicity` is guarded by a non-waivable failure, which an `INVALID` witness need not contain. Nevertheless, `Init` admits, for example, `status[c1]="fail"`, all others `"pass"`, `waived={}`. The reported 1,944 distinct initial states equal the configured `3^5 × 2^3` assignments, supporting exhaustive coverage of that guard. This is an inference from the formulas and reported enumeration, not a displayed failure-status witness. (`P4_VerifierStates_Sanity.cfg:1–7`; `P4_VerifierStates.tla:31,40–42,77–79`; `P4_VerifierStates.out:25–30`)

Thus no implication antecedent in the **correct configured model** is necessarily unreachable: validity, strict, degraded, and unverifiable are witnessed; non-waivable failure is admitted by exhaustive initialization; non-waivable unperformability is displayed. This says nothing about guards in an implemented verifier or real adversarial executions. (`P4_VerifierStates.tla:77–110`; `P4_VerifierStates_Sanity.out:8–14`; `P4_VerifierStates.out:25–32`)

In the broken module, `UnverifiableIsHonest` **is vacuous**: its verdict function never returns `UNVERIFIABLE`. `DegradedNeedsExplicitWaiver` also cannot expose the omitted-unperformability defect: the broken function still selects degraded only for nonempty `W`, and initialization ensures legality. (`P4_VerifierStates_Broken.tla:28–30,38–43,66–72`)

The sanity output's final “No error has been found” does not erase its explicit invariant violations; the file contains both. The documented intended execution uses `-continue`. (`P4_VerifierStates_Sanity.out:8,16,24,32–33`; `P4_VerifierStates_Sanity.cfg:1–4`)

## 3. Attack attempts

Only `Init → Next → Next…`, with unchanged values, is a model trace. Below, “representable” means an initial assignment and its derived verdict; no attack-induced state change is representable. Invariants check outcomes rather than prevent actions. (`P4_VerifierStates.tla:40–44,65,73–135`)

1. **Waive an integrity failure.** Intended sequence: evaluate `c1="fail"` with other checks passing and `waived={}` → select `waived={c1}` → accept degraded. **UNREPRESENTABLE:** `c1` is non-waivable, so `Init`'s `waived ∈ SUBSET Waivable` conjunct excludes the policy; `Next` also excludes the policy change. With a legal policy, `Monotonicity` requires `INVALID`. Consequently, rejection or normalization of hostile policy input is not tested. (`P4_VerifierStates.cfg:2–3`; `P4_VerifierStates.tla:29,40–44,77–79`; `REGISTERED-P4.txt:25–30`)

2. **Lose a non-waivable check and accept anyway.** Intended sequence: all checks pass → `c1` becomes `"unperformable"` → return valid under `waived={c3}`. The transition is **UNREPRESENTABLE**, but its status/policy endpoint is representable. The `ELSE IF` at lines 59–60 returns `UNVERIFIABLE`; a valid result would falsify the allowed-verdict conjunct of `NoSilentPromotion`, the all-pass consequent of `ValidNeedsNonWaivablePass`, and `ExactUnverifiable`. (`P4_VerifierStates.tla:40–44,56–63,84–93,127–128`)

3. **Combine definite failure with an unperformable non-waivable check.** Initialize `c1="unperformable"`, `c2="fail"`, other checks `"pass"`, `waived={}` → stutter. **Representable; no invariant rejects it.** The first branch produces `INVALID`; `ExactInvalid` requires that result and `ExactUnverifiable` excludes `UNVERIFIABLE`. This violates the literal unconditional unperformable-to-unverifiable sentence, while remaining fail-closed. The model documents the precedence choice but not its ratification. (`P4_VerifierStates.tla:40–44,49–60,124–128`; `REGISTERED-P4.txt:30–33`)

4. **Waive an unperformable check.** Initialize `c5="unperformable"`, all others `"pass"`, `waived={c5}` → stutter. **Representable; no invariant rejects it:** `RequiredUnder` removes `c5`, and `ExactDegraded` requires degraded validity. This conflicts with P4's unqualified “A check that cannot be performed…never any `VALID` state.” The redundancy paragraph may motivate an exception, but no mapping shows that `c5` is an eligible redundancy check. (`P4_VerifierStates.cfg:2–3`; `P4_VerifierStates.tla:54–63,134–135`; `REGISTERED-P4.txt:14–17,35–39`)

5. **Silently create a waiver and omit the audit record.** Intended sequence: `c5` cannot be checked → verifier automatically sets `waived={c5}` → emits `VALID_DEGRADED` without recording consent or authorizing policy. **UNREPRESENTABLE as an authorization/recording attack:** neither event nor record exists. Its status/waiver projection is accepted exactly as in attack 4; `DegradedNeedsExplicitWaiver` checks only the nonempty legal set. (`P4_VerifierStates.tla:35–44,102–103,134–135`; `REGISTERED-P4.txt:16–17,41–43`)

6. **Replay or mutate a valid bundle while retaining successful check results.** Intended sequence: verify a signed bundle → alter its bytes, substitute a key, or replay across a type boundary → reuse cached `"pass"` results → accept strict. **UNREPRESENTABLE:** there are no bundles, keys, signatures, contexts, caches, or corresponding actions. The projection `status[c]="pass"` for every check and `waived={}` necessarily returns strict, with no formula connecting those statuses to the altered object. These are registered adversary capabilities. (`A1.3.txt:5–14`; `P4_VerifierStates.tla:25–44,130–132`)

## 4. Companions

There is one supplied broken companion. Its header expects “NoSilentPromotion, or StrictMeansEverything.” Its committed output reports **only `StrictMeansEverything`** violated, in an initial state with empty waiver set, `c1`–`c4` passing, and `c5` unperformable. This matches one named alternative; the output does not establish that both named invariants failed or that they are the exact set of all failing formulas. (`P4_VerifierStates_Broken.tla:9–12`; `P4_VerifierStates_Broken.out:19–27`)

The displayed counterexample isolates the intended defect: `c5` is required because nothing is waived; the broken function skips unperformability and returns strict. Its strict invariant requires every check to pass. No unrelated failure is needed to explain the observed red result. (`P4_VerifierStates_Broken.tla:34–43,63–64`; `P4_VerifierStates_Broken.out:20–25`)

Reading also supplies an **unreported** counterexample: `c1="unperformable"`, all others `"pass"`, `waived={}` would falsify `NoSilentPromotion`, `ValidNeedsNonWaivablePass`, and `StrictMeansEverything`. These are formula-derived failures, not additional observed TLC results. The expected alternatives therefore are not an exhaustive set of potential failures. (`P4_VerifierStates_Broken.cfg:2–3`; `P4_VerifierStates_Broken.tla:28–30,38–43,54–64`)

There is no whole-companion “could not fail” obstruction: it did fail. However, its unverifiable invariant cannot fail because that verdict is unreachable, and the committed run ends on an initial-state violation without reporting complete enumeration. It cannot certify the other configured invariants as green. (`P4_VerifierStates_Broken.tla:38–43,69–72`; `P4_VerifierStates_Broken.out:14–27`)

## 5. Scoped abstractions

**Named in comments:**

- Verdict computation is a pure function of supplied check outcomes and declared policy; evaluation is instantaneous, without temporal behavior. (`P4_VerifierStates.tla:7–13`)
- Individual verification checks are abstract elements; their results are three-valued; policy is represented by a waived subset, with `{}` called strict. (`P4_VerifierStates.tla:15–19`)
- Initialization enumerates legal policies only; policies naming non-waivable checks are excluded. (`P4_VerifierStates.tla:37–42`)
- Failure-over-unperformability precedence is an explicit modeling decision awaiting author ratification. (`P4_VerifierStates.tla:47–52`)
- The broken companion abstracts fail-open behavior as skipping unperformable checks; it does not model an actual trust-root retrieval operation. (`P4_VerifierStates_Broken.tla:3–7,36–43`)

**Visible but not expressly bounded in the module comments:**

- TLC checks one finite instance: five checks, two non-waivable. The “every combination” claim is exhaustive within that instance, not a demonstrated result for arbitrary set sizes or the registered concrete check inventory. (`P4_VerifierStates.cfg:2–3`; `P4_VerifierStates.tla:8–10,25–27`; `P4_VerifierStates.out:25–32`)
- Status values are unconstrained inputs, independent of evidence, check dependencies, or execution. `"pass"` stands in for the entire successful verification obligation. (`P4_VerifierStates.tla:31,35–42`)
- A waiver set stands in for declaration, authorization, informed consent, and auditable recording; there is no separate representation of these obligations. (`P4_VerifierStates.tla:18–19,35–44`; `REGISTERED-P4.txt:41–43`)
- No binding maps abstract checks to the mandatory integrity, framing, key-binding, and temporal checks, or limits abstract waivable elements to declared redundancy. (`P4_VerifierStates.cfg:2–3`; `REGISTERED-P4.txt:25–39`)
- The adversary is reduced to possible status assignments. Byte alteration, signature stripping/reordering/duplication, adaptive key substitution and self-signing, replay/type reframing, freely crafted anchored manifests, and control of proper subsets of authority channels have no objects or actions. (`A1.3.txt:3–16`; `P4_VerifierStates.tla:25–44`)
- Verdict is derived, not an independently emitted or stored value; output corruption, stale verdict reuse, and mismatch between a computed verdict and its recorded result cannot be expressed. (`P4_VerifierStates.tla:35,56–65`)
- Classification ignores waived-check outcomes entirely and treats every nonempty successful waiver policy as degraded, even when all waived checks passed. (`P4_VerifierStates.tla:54–63,134–135`)

## 6. Verdict on the module header's honesty

**The header overstates correspondence.** Calling the module “the machine-checkable form” of P4 and the waiver lattice exceeds the checked result: recording and authorization are absent, concrete waiver categories are unmapped, and unperformability classification incorporates an explicit additional precedence decision and a required-check restriction. (`P4_VerifierStates.tla:4–10,49–60,102–110`; `REGISTERED-P4.txt:14–17,25–43`)

The header does disclose instantaneous evaluation, abstract checks, and policy-as-set representation. Its enumeration claim is supported for the supplied finite configuration by the reported 1,944 distinct states and completed search. Those results establish the configured abstract classification table, not adversarial trace correspondence or implementation behavior. (`P4_VerifierStates.tla:7–19,40–44`; `P4_VerifierStates.cfg:2–3`; `P4_VerifierStates.out:25–32`)

The strongest defensible reading is: the committed run reports no violation of eleven formulas over the configured legal status/waiver assignments; the sanity output witnesses all four verdicts; the companion exposes one fail-open assignment. Full discharge of the supplied registered wording is not established by these artifacts. (`P4_VerifierStates.cfg:8–19`; `P4_VerifierStates.out:25–32`; `P4_VerifierStates_Sanity.out`, extracted lines 15,19,50,83; `P4_VerifierStates_Broken.out:19–25`)
### Reviewer output — P5P6 (`model: gpt-6-astra`)

## 1. Correspondence audit

All findings are from reading the supplied files, **not re-running TLC**. Citations to `.out` files use their numbered “final 40 lines.” For compact citations, `M` means `P5P6_TemporalRevocation.tla`; `R` means `REGISTERED-P5-P6.txt`; other filenames are written explicitly.

The main configuration checks seven state invariants. It checks no temporal property, and the sole transition preserves every variable. Thus the checked behavior is enumeration of fixed assignments, not an issuance or adversarial execution protocol. (`P5P6_TemporalRevocation.cfg:7–17`; `M:74–86`)

- **`ForgeryRejected`** corresponds to the attack described as “a key revoked inside the δ window could sign *after* revocation while declaring a time just before it,” and its remedy, “no revocation effective at or before anchor_time.” (`R:45–52`)
  The formula rejects every assignment with `revoked <= signed`, including equality and cases outside that particular backdating scenario. Its proof depends entirely on the initialization constraint `signed <= anchor` and acceptance requiring `revoked > anchor`. It does not establish the anchor constraint, signature authenticity, or that revocation is authentic. It addresses post-revocation signing, not forgery generally. (`M:24–25,74–79,116–136`)

- **`WindowRespected`** corresponds exactly, algebraically, to the registered scalar inequalities “declared_issue_time − ε ≤ anchor_time ≤ declared_issue_time + δ,” extended by “confirmed_at ≤ declared_issue_time + δ.” (`R:6`; `A2.1-A2.2.txt:143–147`)
  It expresses a necessary condition on acceptance, using the selected verifier policy. It does not establish that `confirmedAt` actually comes from the designated block, that depth exists, or that headers are authentic. The inequalities are already acceptance conjuncts, so this checks their preservation in the assembled predicate. (`M:104–123,141–144`; `A2.1-A2.2.txt:159–167`)

- **`VerifierOwnsTolerances`** claims correspondence to “δ and ε belong to the verifier, not the receipt” and “no degraded policy may enlarge δ or ε beyond the strict maxima.” (`R:15–23`)
  Its actual quantity is the accepted timestamp gap versus **global maxima**, not versus the verifier’s chosen tolerances. Receipt-driven enlargement from policy δ = 0 to effective δ = 1 can satisfy this invariant when `DeltaMax = 3`. Ownership therefore does not follow from this formula alone. There is also no degraded policy or waiver state. (`M:151–155`; `P5P6_TemporalRevocation.cfg:2–5`)
  The constants stand in for the registered magnitudes; the check does not validate 72/24 hours or their ratification. (`M:21–23`; `R:19–24`)

- **`AbandonedArtifactRejected`** corresponds to “The **chain-late subclass** … (`confirmed_at > declared + δ`) is **rejected outright**.” (`A2.1-A2.2.txt:151–158`)
  Its antecedent additionally requires an in-window anchor, making the standalone invariant narrower than rejection of every chain-late artifact. The actual acceptance predicate rejects all chain-late assignments regardless of anchor position. No abandonment, issuance attempt, shipping, or standing is represented; the formula recognizes a timestamp pattern. (`M:104–107,164–168`)
  Its δ is the verifier’s policy, so lateness under a stricter verifier need not imply abandonment under the issuance policy. The amendment expressly allows this disagreement. (`M:80–81,165–167`; `A2.1-A2.2.txt:23–28`)

- **`ReceiptIndependence`** corresponds to “it may not choose its own temporal tolerances.” (`R:15–18`)
  It requires verdict equality under every bounded pair of receipt-tolerance arguments, capturing both enlargement and narrowing. It does not quantify over receipt bytes, policy-version selection, or other receipt-controlled inputs. (`M:178–180`; `R:15–17`)
  Independence is stronger than merely forbidding receipt-induced enlargement, but it is **not logically stronger than the maxima invariant without additional assumptions**: a predicate ignoring receipt arguments could still accept outside the maxima. The comment’s “strictly stronger” wording needs that qualification. (`M:151–155,170–180`)

- **`AuthorizedAtDeclared`** corresponds to “key_authorized(declared_issue_time).” (`R:51`)
  The formula substitutes `declared < revoked`. This is equivalent only under an additional interpretation that the key is otherwise authorized throughout all modeled pre-revocation times. There is no activation time, authorization grant, scope, manifest entry, or key identity. Terminal revocation alone does not establish initial authorization. (`M:43–45,67–83,184–185`; `R:58–66`)

- **`HonestCostIsExactlyTheWindow`** corresponds to “it can fail honest receipts whose key was revoked between declaration and anchor confirmation.” (`R:68–73`)
  The formula says that temporally passing, pre-revocation-signed, declaration-authorized but rejected assignments have `revoked <= anchor`. The declaration authorization premise supplies the other endpoint, yielding `(declared, anchor]`. This is a one-way implication, though the converse follows from the acceptance definition under the same premises. (`M:116–123,192–197`)
  “Honest” means only the specified scalar premises; it does not include successful issuance or authenticated evidence. “Everything else honest is accepted” in the comment omits the formula’s declaration-authorization restriction. Also, `anchor` is the inclusion block timestamp, while `confirmedAt` is the k-th-confirmation timestamp: the formula does **not** measure cost through confirmation or wall-clock burial. (`M:33–42,187–197`)

The companion configurations check variants of these same invariants; their acceptance definitions change the correspondence as detailed in section 4. (`P5P6_TemporalRevocation_Broken.cfg:10–11`; `P5P6_TemporalRevocation_BrokenTol.cfg:10–11`; `P5P6_TemporalRevocation_BrokenTolStrict.cfg:13–17`; `P5P6_TemporalRevocation_BrokenConf.cfg:15–18`)

The sanity configuration checks four negated witness predicates, not registered safety obligations. Their registered connections and observed failures are addressed below. (`P5P6_TemporalRevocation_Sanity.cfg:1–7,17–21`; `M:199–214`)

**Registered clauses with no corresponding formula in this file set:**

- Receipt policy-version and observed-delay recording; degraded-policy handling; non-waivability; actual tolerance magnitudes and ratification. Only bounded strict-path arithmetic appears. (`R:15–26`; `M:60–83,104–123`)
- Depth k, inclusion/confirmation-height arithmetic, reorgs, shipping only after confirmation, discarding, and re-issuance. `confirmedAt` is an unconstrained input, not computed from a chain. (`R:28–39`; `A2.1-A2.2.txt:3–8,131–137`; `M:74–86`)
- Issuer/verifier comparison on the same observations and issuance policy; slack, observation lag, live opportunity, latch priority, expiry, mutual exclusion, and protocol standing. (`A2.1-A2.2.txt:14–28,29–85,91–101`; `M:67–86,104–123`)
- Header availability, authentication, canonical-chain selection, work validation, store identity, conflict resolution, and the `INVALID`/`UNVERIFIABLE` partition. The model has only a Boolean acceptance predicate over supplied scalars. (`A2.1-A2.2.txt:159–171`; `M:67–68,104–123`)
- Lifecycle enforcement, new fingerprints and manifest entries after re-keying, and explicit verdict stability across revocation updates. One fixed cutoff substitutes for lifecycle behavior. (`R:54–66`; `M:43–45,79,85–86`)
- The adversary’s byte alteration, signature-set manipulation, key substitution/DSKS, replay/type reframing, crafted manifests/anchors, and channel compromise have no corresponding actions or object representations. (`A1.3.txt:5–16`; `M:67–86`)

## 2. Vacuity

The four expected reachable predicates are:

| Witness predicate | Evidence that its negation went red |
|---|---|
| `StrictAccept /\ confirmedAt < anchor` | 267,932 reported violations of `NonMonotonicAcceptUnreachable`. (`M:203–204`; `P5P6_TemporalRevocation_Sanity.out:15`) |
| `StrictAccept` | 441,098 reported violations of `AcceptanceUnreachable`. (`M:205`; `P5P6_TemporalRevocation_Sanity.out:12`) |
| In-window anchor with `confirmedAt > declared + polDelta` | 267,736 reported violations of `LateBurialCaseUnreachable`. (`M:206–209`; `P5P6_TemporalRevocation_Sanity.out:14`) |
| `TemporalOK /\ signed < revoked /\ revoked > declared /\ ~StrictAccept` | 101,528 reported violations of `HonestCostCaseUnreachable`. (`M:210–214`; `P5P6_TemporalRevocation_Sanity.out:13`) |

These counts confirm that the **provided summary reports** all four witnesses firing. Individual assignments were elided, so their contents cannot be inspected in this output. The file reports a completed depth-one enumeration with zero queued states. (`P5P6_TemporalRevocation_Sanity.out:10–23`)

Acceptance witnesses cover the antecedents of `WindowRespected`, `VerifierOwnsTolerances`, and `AuthorizedAtDeclared`; the other predicates cover the abandonment and honest-cost antecedents. `ReceiptIndependence` has no implication antecedent, and its argument domains are nonempty. (`M:141–155,164–185,192–214`; `P5P6_TemporalRevocation.cfg:5`)

**`ForgeryRejected` has no dedicated sanity witness.** Its antecedent is nevertheless satisfiable directly in `Init`: set `declared=signed=anchor=confirmedAt=revoked=0` and both policy tolerances to zero. This is a reading-derived witness, not an individually printed main-run state. (`M:74–83,135–136`)

No checked implication has an antecedent that reading shows to be unreachable. There are no action guards to become enabled: `Next` only stutters. This means the witnesses establish scalar-case coverage, not the reachability of operational eligibility, shipping, revocation, or attack actions. (`M:85–86,135–214`)

## 3. Attack attempts

Tuple notation below is `(declared, signed, anchor, confirmedAt, revoked; polDelta, polEps; rcptDelta, rcptEps)`. Every representable model trace is `Init(tuple) → Next(tuple) → …`; the narrative actions are not transitions in this model. (`M:67–86`)

1. **Revoke, then sign while claiming an earlier date.** Narrative: declare 0 → revoke at 1 → sign at 1 → anchor at 1, with confirmation timestamp 1. Use `(0,1,1,1,1;1,0;0,0)`.
   **Representable as a fixed assignment.** All temporal conjuncts pass; `revoked > anchor` rejects because `1 > 1` is false. The actual revoke/sign sequence is unrepresentable. (`M:74–86,104–118`)

2. **Enlarge the receipt’s tolerance.** Declare/sign/anchor at 0 → obtain confirmation timestamp 4 → claim receipt δ = 4. Use `(0,0,0,4,7;0,0;4,0)`.
   **Representable as a fixed assignment.** Receipt δ is ignored; `confirmedAt <= declared + polDelta` rejects `4 <= 0`. This is also the shape of the printed enlargement counterexample, with revocation set to 1 there. (`M:65,74–83,104–107`; `P5P6_TemporalRevocation_BrokenTol.out:26–35`)

3. **Publish a chain-late, never-shipped receipt.** Declare/sign/anchor at 0 → confirmation timestamp 1 → publish after discarding. Use `(0,0,0,1,1;0,0;0,0)`.
   **Timestamp assignment representable; discarding and publication UNREPRESENTABLE.** The third temporal conjunct rejects. This is the exact scalar assignment printed for the missing-confirmation companion. (`M:67–86,104–107`; `P5P6_TemporalRevocation_BrokenConf.out:24–33`)

4. **Exploit backward header time to hide post-revocation signing.** Declare 1 → revoke at wall time 2 → sign at wall time 3 → later mine headers timestamped 1. Desired tuple: `(1,3,1,1,2;0,0;0,0)`.
   **UNREPRESENTABLE:** `signed <= anchor` excludes it before verification, although the acceptance conjuncts would all pass on these scalars. The amendment acknowledges backward-skewed header timestamps; it does not establish this module’s cross-clock signing bound. Thus the signing theorem is conditional on the named anchor assumption, not a check of its applicability to actual signing time. (`M:30–42,78,104–118`; `A2.1-A2.2.txt:113–119`)

5. **Present a privately mined or unauthenticated in-window header segment.** Sign at 1 → fabricate/select header timestamps 1 → submit `(1,1,1,1,7;0,0;0,0)`.
   **The malicious provenance is UNREPRESENTABLE; its timestamp projection is accepted.** There is no provenance variable or rejecting conjunct. This is precisely the kind of false acceptance the amendment identifies for naive stateless evaluation. (`M:65,67–83,104–123`; `A2.1-A2.2.txt:120–129,159–167`)

6. **Sign before the key becomes authorized.** Sign/declare at 1 → anchor at 2 → grant authorization only at 3; no revocation. Projection: `(1,1,2,2,7;1,0;0,0)`.
   **The authorization grant and pre-grant status are UNREPRESENTABLE; the projection is accepted.** `revoked > declared` supplies no test of whether authorization had begun. This exposes the additional assumption required to equate it with `key_authorized(declared_issue_time)`. (`R:51`; `M:65,67–83,104–123`)

7. **Supply an anchor that has not reached k confirmations.** Declare/sign/include at 1 → present only the inclusion header while assigning `confirmedAt=1`. Projection: `(1,1,1,1,7;0,0;0,0)`.
   **Shallow depth and missing designated evidence are UNREPRESENTABLE; the projection is accepted.** No height, depth, header sequence, or evidence-availability conjunct rejects it. (`R:28–35`; `A2.1-A2.2.txt:159–171`; `M:67–83,104–123`)

8. **Revoke after the anchor but before a post-dated declaration.** Anchor/sign at 0 → revoke at 1 → declared time 1. Use `(1,0,0,0,1;0,1;0,0)`.
   **Representable and rejected by `revoked > declared`; `revoked > anchor` passes.** This exposes a qualification missing from the registered sentence “Revocation effective *after* `anchor_time` does not retroactively change the verdict”: when the anchor precedes declaration, a later revocation can still invalidate authorization at declaration. The explicit registered two-conjunct rule agrees with the model; that unqualified sentence does not. (`R:51–56`; `M:104–118`)

## 4. Companions

- **`Broken`: observed red set `{ForgeryRejected}`**, exactly the singleton configured and predicted. The printed assignment has declaration 0, signing/revocation/anchor 1, confirmation timestamp 0, and policy δ = 1. Temporal checks pass; point-only authorization accepts `1 > 0`, exposing the omitted anchor authorization check. (`P5P6_TemporalRevocation_Broken.cfg:10–11`; `P5P6_TemporalRevocation_Broken.tla:3–15,43–56`; `P5P6_TemporalRevocation_Broken.out:27–36`)
  It demonstrably could fail. Its counterexample permits non-monotonic timestamps, but the defect does not depend on that: setting `confirmedAt=1` preserves acceptance and the violation under the written formulas. (`P5P6_TemporalRevocation_Broken.tla:29–38,43–56`)

- **`BrokenTol`: observed red set `{VerifierOwnsTolerances}`**, exactly the configured and predicted invariant. The witness enlarges confirmation allowance to 4 while policy δ is 0 and the configured maximum is 3. (`P5P6_TemporalRevocation_BrokenTol.cfg:2–11`; `P5P6_TemporalRevocation_BrokenTol.out:26–35`)
  The header predicts an excessive **anchor-to-declared** gap; the printed gap is zero. The red conjunct is instead `confirmedAt - declared <= DeltaMax`. The general enlargement defect is exhibited, but the stated witness quantity is wrong. (`P5P6_TemporalRevocation_BrokenTol.tla:10–13,48–51,62–66`)
  This companion could fail and did. However, enlargement that stays below global maxima cannot fail this invariant merely for exceeding the selected policy; that is a limitation of its catcher. (`P5P6_TemporalRevocation_BrokenTol.tla:62–66`)

- **`BrokenTolStrict`: observed red set `{ReceiptIndependence}`**, matching the named expected failure. The run stops at an initial-state violation, so the output does **not** establish exhaustive green results for the three other configured invariants. (`P5P6_TemporalRevocation_BrokenTolStrict.cfg:1–3,13–17`; `P5P6_TemporalRevocation_BrokenTolStrict.out:24–35`)
  Reading explains the failure: with `confirmedAt=1`, declaration/anchor 0, policy δ = 1 and receipt δ = 0, the current verdict rejects; substituting receipt δ = 1 accepts. The unchanged revocation rule and `Min` bounds also explain algebraically why the three safety invariants cannot detect this narrowing defect. (`P5P6_TemporalRevocation_BrokenTolStrict.out:25–33`; `P5P6_TemporalRevocation_BrokenTolStrict.tla:50–87`)
  Its claimed distinction between parties “checking promptly” and others is unmodeled: verification time is absent and the anchor-to-declared gap is fixed. (`P5P6_TemporalRevocation_BrokenTolStrict.tla:8–13,33–48`)

- **`BrokenConf`: observed red set `{AbandonedArtifactRejected}`**, matching the named expected failure. The initial-state witness has anchor/declaration 0, confirmation timestamp 1, policy δ = 0, and revocation 1. Omitting the confirmation conjunct makes it accepted. (`P5P6_TemporalRevocation_BrokenConf.cfg:1–5,15–18`; `P5P6_TemporalRevocation_BrokenConf.out:24–33`; `P5P6_TemporalRevocation_BrokenConf.tla:56–83`)
  The stopped output does **not** establish exhaustive green results for `ForgeryRejected` and `ReceiptIndependence`. Reading supports them: signing remains bounded by anchor, authorization still checks anchor, and receipt arguments remain unused. Neither can detect the missing confirmation conjunct. (`P5P6_TemporalRevocation_BrokenConf.out:24–35`; `P5P6_TemporalRevocation_BrokenConf.tla:40–75`)
  “Only” this invariant fails is relative to the selected suite: the header itself acknowledges that the main `WindowRespected` and `VerifierOwnsTolerances` would also detect confirmation violations on suitable assignments. (`P5P6_TemporalRevocation_BrokenConf.tla:15–24`)

None of the four companions was prevented from failing by an unrelated restriction: each supplied output contains its targeted failure. The multi-invariant companion runs establish the reported first failure, not an exhaustive classification of every configured invariant. (`P5P6_TemporalRevocation_Broken.out:27–38`; `P5P6_TemporalRevocation_BrokenTol.out:26–37`; `P5P6_TemporalRevocation_BrokenTolStrict.out:24–35`; `P5P6_TemporalRevocation_BrokenConf.out:24–35`)

## 5. Scoped abstractions

**Named in comments:**

- Verifier-side scope; issuance behavior assigned elsewhere. (`M:9–19`)
- Small integer time and scaled tolerance maxima; signature checks assumed passing. (`M:21–25`)
- Adversarial declared time; actual signing time hidden from the verifier. (`M:28–32,55–56`)
- The anchor-as-signing-upper-bound assumption, imposed as a state constraint. (`M:33–36,70–78`)
- Designated confirmation timestamp supplied without ordering against anchor. (`M:37–42,72–77`)
- Terminal revocation represented by one timestamp; a sentinel for never revoked. (`M:43–45,65`)
- Verifier-selected bounded policies and adversarial receipt tolerance fields, intentionally ignored. (`M:46–54,80–83,88–103`)
- Strict temporal/authorization projection of `VALID_STRICT`. (`M:89–90,120–123`)

**Additional abstractions or restrictions not explicitly scoped as such:**

- A static truth-table model: no changing time, lifecycle actions, multiple attempts, or interacting issuer/verifier states. (`M:67–86`)
- Authorization before revocation is implicit; no grant, activation, expiry, identity, manifest, or authority-channel state exists. (`M:67–83,116–118`; `A1.3.txt:8–16`)
- Revocation and chain observations are supplied directly, with no evidence authentication, missing-data case, fork selection, or store disagreement. (`M:67–83`; `A2.1-A2.2.txt:159–171`)
- No derivation of `confirmedAt` from h and k; no constraint that it belongs to the same chain or anchor, or that sufficient blocks exist. (`M:74–78`; `A2.1-A2.2.txt:3–8`)
- Signing time is numerically ordered against header time without an explicit clock conversion or skew model, although confirmation/observation clock differences are material in the amendment. (`M:30–42,78`; `A2.1-A2.2.txt:29–43,113–119`)
- Boolean rejection merges invalidity, unverifiability, and any other rejection reason; protocol standing is absent. (`M:120–123`; `A2.1-A2.2.txt:58–62,168–171`)
- “Unconstrained” declarations and “possibly enormous” receipt tolerances are actually limited to `0..6`; policy ε is `0..1`, δ is `0..3`. No unbounded result is recorded. (`M:28–29,49–50,74–83`; `P5P6_TemporalRevocation.cfg:2–5`)
- No receipt byte binding or adversarial transformations connect the supplied scalars to signed artifacts. Assuming signatures pass does not model which fields those signatures authenticate. (`M:24–25,67–86`; `A1.3.txt:5–14`)

## 6. Verdict on the module header’s honesty

**The header overstates what this supplied check establishes.** The recorded result is no invariant error across 4,302,592 distinct fixed assignments in one bounded configuration, with the output’s stated fingerprint-collision estimates. It is not a checked cross-module correspondence or an operational adversary model. (`P5P6_TemporalRevocation.out:31–39`; `P5P6_TemporalRevocation.cfg:2–17`; `M:85–86`)

The claim that correspondence with `P5c` shipping is “exact by construction” is unsupported by any formula here. The supplied amendment explicitly distinguishes P5c’s fused-clock guard from the decoupled bridge and scopes issuer/verifier agreement to the issuance policy’s tolerances. This module contains neither comparison. (`M:15–19,67–86,104–123`; `A2.1-A2.2.txt:23–28,91–101`)

“Discharges the VERIFIER-SIDE face of P5” needs narrowing to the **scalar temporal/authorization predicate under the named and implicit assumptions**. The registered verifier-side evidence and verdict-partition obligations are absent. (`M:9–15,104–123`; `A2.1-A2.2.txt:159–171`)

The comments also overreach in calling timestamp patterns discarded-attempt artifacts, in describing honest cost through confirmation while testing the inclusion timestamp, and in suggesting any receipt-tolerance routing breaks the maxima invariant. The supplied narrowing companion directly demonstrates the last distinction. (`M:49–54,157–168,187–197`; `P5P6_TemporalRevocation_BrokenTolStrict.tla:54–87`)

The most consequential unresolved correspondence is **actual signing time ≤ anchor header timestamp**. The model names this assumption, but the supplied materials do not establish its validity against backward timestamp skew. Without it, the central post-revocation-signing implication loses its supporting order relation; the relevant attack is excluded at initialization. (`M:30–36,78,129–136`; `A2.1-A2.2.txt:113–119`)
### Reviewer output — P5c (`model: gpt-6-astra`)

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