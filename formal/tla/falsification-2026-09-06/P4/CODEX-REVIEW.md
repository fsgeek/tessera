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