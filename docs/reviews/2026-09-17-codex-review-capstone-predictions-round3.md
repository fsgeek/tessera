# Codex non-author review of the capstone registration, third round (2026-09-17)

Reviewer: OpenAI Codex CLI (`gpt-6-astra`), run non-interactively by the
owner instance on 2026-09-17 (17:40–17:48 UTC) against the whole of
`formal/suite/capstone/PREDICTIONS.md` after the round-two repairs, with
both earlier records
(`docs/reviews/2026-09-16-codex-review-capstone-predictions.md`,
`…-round2.md`) as its starting point; scratch diagnostics on family-model
copies under `/tmp/tessera-capstone-r3/`. **The reviewer found the
registration not ready to freeze**: three registration defects and one
basis defect, all in the parts round two rewrote. Every factual claim
below was checked against the tree before disposition, and every run the
reviewer cites was reproduced on our tree
(`formal/suite/ledger-tests-2026-09-14/cap9*`–`cap11*`, seventh batch of
that directory's README) at the reviewer's own `.out` line numbers. No
capstone model exists; nothing in the repository was run. The reviewer
also confirms, in its §6, that all ten accepted findings of rounds one
and two are repaired except where the three findings below reopen them
(R1.4 and R2.1 through finding 3), and that the two contestable fixture
choices of round two are stated so a builder cannot misread them.

## Dispositions (owner instance, 2026-09-17)

All four are **clerk dispositions** of the owner instance. None fixes a
fixture meaning; finding 2's repair is an **addition beyond
`LEDGER.md` §6** and is marked as such in the file.

1. **Link 2b's permitted projection loses the layer.** ACCEPTED.
   Reproduced: `cap9_sp2_slots_projection_no_lyr.out` — two layers
   sharing the intake `aid` and the tuple `t`, slot B reported at one
   layer only: the projected correspondence (no `lyr`) stays **`is
   true`** (`:1239`) while the layer-indexed one is **`is false`**
   (`:1454`), witnesses reachable (`:675`, `:913`, `:1162`). Round two's
   intake `aid` made this possible: within one presentation the layers
   share the name, and same-key wrapping plus one-key/one-manifest let
   the wrapper and inner layers share `t`. **Repair:** (a) the permitted
   projection retains the layer — `SlotSatisfied(aid, lyr, t, slot)`;
   the C-Q1 link-2b text and C-C9's sets say so. (b) §1.3's round-two
   sentence *"a bundle still yields at most one acceptance"* is wrong
   for a wrapped bundle and is withdrawn, quoted: a wrapped bundle yields
   **one acceptance per layer**, each with its own
   `AcceptanceComplete(aid, lyr, t)`; the per-acceptance name the ledger's
   carried-forward correction requires ("one fresh name per acceptance,
   shared across its slots") is the **pair `(aid, lyr)`** — `aid` fresh
   per presentation, `lyr` distinguishing the layers within it. That is
   what the correction's freshness demands and what the projection must
   preserve.

2. **C-Q6 no longer consumes scope, so C-C15 has no standing
   consumer.** ACCEPTED. Round two made the standing path extract the
   innermost terms itself and consume no envelope event, which is right
   for D13 (C-C12 can now fail: `cap11a…out:1307`) and wrong for D11's
   conditional half: nothing in C-Q6's two conjuncts observes the
   envelope's **attribution**, so C-C15's scope mutations — which
   change the reported key and leave the innermost material unchanged
   (`sp7_q5c_companion_one_level_in.pv:229-241`) — cannot red C-Q6.
   Reproduced at the reviewer's projection:
   `cap10_ss_q3_scope_report_only.out` — only the envelope's reported
   attribution key changed — makes `ScopeMisreported` **reachable**
   (`:779`) while wrapped designation (`:798`, `:811`), entitled-key
   safety (`:856`) and honest standing (`:1205`) stay green/reachable.
   **Repair, an ADDITION beyond `LEDGER.md:1294` and marked so:** C-Q6
   gains a **third conjunct, scope agreement**, in S-P7's `ScopeJudge`
   house form — a judge that reads, on private channels, the standing
   path's report `(aid, lyr, kX)` and the envelope path's attribution
   report `(aid, lyr, kA, idA)` (the `scopeCh` report S-P7's models
   already emit) and fires `ScopeMisreported(aid, lyr, kX, kA)` when
   `kA ≠ kX`; **unreachable** in (a), (b) and (d). The judge waits for
   both reports; **neither path waits for the other**, so the round-two
   independence stands and D13's severing is not re-shadowed. Its
   witness: `HonestWrappedStandingAgreed(aid, lyr)`, fired by the judge
   when the two reports agree for an honest wrapped acceptance. C-C15
   is re-specified: **set (1)** for both configurations gains the
   scope-agreement conjunct (the wrong attribution is exactly what the
   judge sees; (i) `kW ≠ kI`, (ii) `kM ≠ kI`) and **loses** *"C-Q6's
   standing conjunct"*, which moves to **set (2)** together with the
   entitled-key conjunct, both predicted green (the standing path is
   untouched by a scope mutation; `cap10:798`, `:811`, `:856` at the
   projection); the withdrawn membership is quoted. D11's matrix cell
   names the third conjunct as the consumer of its conditional half.
   No timeboxed entry is added: the conjunct belongs to C-Q6, whose 90
   min stands.

3. **The mapping still carries the fingerprint precondition E5's
   withdrawal removed; and C-C12 retains `kT = kX`.** ACCEPTED, both
   parts. Reproduced on the reviewer's structural-join rewrite of the
   SS.Q3 companion (fresh intake name, front-end forwarding in parallel,
   structural wrapper extraction, `attemptCore` pinned to the
   presentation's own `t`, `ppf`, `sg`): **the structural join works** —
   `cap11a_ss_q3_structural_join.out`: wrapped designation **`is
   false`** as C-C12 requires (`:735`), `StandingUnentitled`
   **reachable** (`:1307`), honest standing reachable (`:1657`), and the
   artifact-A/artifact-B substitution **unreachable** (`:756`); adding the
   mapping's `fp(kX) = kfpr` as a guard (`cap11b…out`) suppresses the
   companion again (`:495` `is true`, `:553` unreachable); relaxing the
   `sg` pin (`cap11c…out`) makes the substitution **reachable** (`:847`)
   while designation stays true (`:495`), so the signature-term pin is
   load-bearing, not decoration. **Repair:** the representation-mapping
   table is split into two columns per row — the **term equality**
   (immutable; it defines the join; never removed by any companion) and
   the **verifier check** it enables (the correct verifier's; removable
   by the named companion): `kX = kI` | `fp(kX) = kfpr`, check 7, removed
   by C-C12; `ppf = ppfI` | `checksign(ppf, kX) = (POSS, t)`, link 3,
   removed by C-C3/C-C8; `fb = fbI` | `checksign(sg, kX) = (BYTES, fb)`,
   link 4, removed by C-C5/C-C7; `sg = sgI` | none — the pin itself;
   `t = tI` | the evidence checks. The introduction's *"all four
   required"* is corrected to name the **five term equalities** as
   required and the checks as the verifier's. E5's withdrawal text is
   corrected: C-C12 removes **`fp(kT) = kfpr` only** and **retains
   `kT = kX`** (`ss_q3_companionB_entitled_via_envelope.pv:259-265`,
   `if kT = kX then` at `:263`); the sentence *"exactly the check C-C12
   removes"* is withdrawn, quoted.

4. **A basis generalization contradicted by round two's own
   evidence.** ACCEPTED. The retained-query table's honest-key
   authorship cell says *"green in every mutant that reds C-Q7"*;
   `cap7b…out:528` and `:1072` red both together under C-C7(ii) with the
   same-key wrapper signer. The generalization is withdrawn, quoted, and
   replaced by what the runs show: green in the S-P1-only mutant that
   reds C-Q7 (`d5d…out:414` red, `:422` green; `d6e` is not an instance
   either way — its C-Q7 is green at `:274` and its authorship red at
   `:809`), red beside C-Q7 under C-C7(ii) in the composed fixture
   (`cap7b`). The p ≈ 0.85 baseline prediction stands;
   only its supporting sentence changes.

5. **The REFUSAL fork stands** as the one routed item; the two
   contestable fixture choices of round two stand as stated; the
   reviewer confirms both are now explicit and does not reverse them.

**Loop.** One repair pass on the registration (Opus, briefed from these
dispositions, in the file's "Repairs after …" pattern), then a fourth
owner-run full Codex pass. The three findings are all in the part of
the contract round two rewrote, which is the expected shape of a
convergent loop: each round's findings are on the previous round's
repair, not on untouched text.

## Codex review — verbatim

## 1. Query strength and discharge

Repository files were read only. All new probes used family-model copies under `/tmp/tessera-capstone-r3/`; no capstone model was built. Below, **P** means `formal/suite/capstone/PREDICTIONS.md`.

**1. Link 2b’s permitted projection loses the layer needed to establish per-layer completeness.**

The revised contract shares an intake `aid` across the presentation. Same-key wrapping and one-key/one-manifest permit inner and outer layers to share `t` too. Nevertheless, the permitted projection is still `SlotSatisfied(aid, t, slot)`, without `lyr`. A report from another layer can therefore satisfy the projected completeness correspondence. The full `LayerAccepted` formulation retains the layer; the expressly permitted projection does not. (`P:66–67`, `P:125–149`, `P:263–280`.)

On a copy of the cited S-P2 completeness diagnostic, I added two layers sharing `aid` and `t`, with slot B reported only at one layer. The projected correspondence remained **true**, while the otherwise identical layer-indexed correspondence was **false**. Honest witnesses remained reachable. This tests the observation schema, not a complete wrapped verifier. (`/tmp/tessera-capstone-r3/slots_projection.pv:245–255`, `:329–338`; `slots_projection.out:1239`, `:1454`, `:675`, `:913`, `:1162`.)

**Required repair:** retain `lyr` in the projection, or explicitly require distinct layer-specific event names. Intake freshness prevents replay mixing; it does not prevent mixing layers within one presentation.

**2. C-Q6’s revised independence leaves C-C15 without its registered standing consumer.**

E1 now requires the standing path to extract innermost terms independently and consume no envelope-success event. C-Q6 queries only that path’s selected key and core. Yet C-C15 still requires both envelope-scope mutations to falsify C-Q6’s standing conjunct, and D11 claims that consumption if C-Q6 terminates. (`P:571–582`, `P:702–723`, `P:1531`, `P:1049`.)

The problem is concrete for C-C15(ii): its source retains verification under `kI`, changes the attribution report to `kM`, and continues reporting the verified signature under `kI`. An independent standing extractor receives unchanged innermost material. Nothing in C-Q6’s formulas observes the wrong attribution report. (`formal/suite/s-p7/proverif/sp7_q5c_companion_one_level_in.pv:229–241`.)

A bounded projection confirms the missing dependency: changing only the envelope’s reported key made `ScopeMisreported` reachable while wrapped designation, entitled-key safety, and honest standing stayed green/reachable. This is a report-only scope diagnostic, not a reproduction of the complete depth-2 companion. (`/tmp/tessera-capstone-r3/scope_report_only.pv:316–319`; `scope_report_only.out:779`, `:798`, `:811`, `:856`, `:1205`.)

**Required repair:** specify the scope observation that C-Q6 consumes and the exact C-C15 mutation that falsifies it, preserving standing’s independence from envelope success. Termination alone cannot establish D11’s conditional half.

## 2. Companion consistency

**3. E5 was withdrawn locally but remains a required equality in the representation mapping.**

The withdrawal says `fp(kX) = kfpr` appears **only** among removable verifier checks, never in the emission contract. The subsequent mapping still requires `kX = kI`, **“with `fp(kX) = kfpr` from `t`.”** Its introduction says the connecting equalities are required. A builder following that mapping can reproduce the precise shadowing defect the repair intends to remove. (`P:627–645`, `P:647–671`.)

I tested the requested rewrite on an S-STANDING Q3 copy with fresh intake identifiers, parallel private forwarding, structural wrapper extraction, and the tuple/proof/signature core pins:

| Observation | Structural join | Same join plus mapping’s fingerprint condition |
|---|---|---|
| Wrapped designation correspondence | **False**, as C-C12 requires | **True** |
| `StandingUnentitled` | **Reachable** | **Unreachable** |
| Honest standing | Reachable | Reachable |
| Core substitution | Unreachable | Unreachable |

Evidence: `/tmp/tessera-capstone-r3/joined.out:735`, `:756`, `:1307`, `:1657`; `joined_pin.out:495`, `:514`, `:553`, `:902`.

The structural repair itself therefore works at this projection. Removing its signature-term pin makes substitution reachable while designation remains true, confirming that the pin supplies a necessary binding rather than decoration. (`/tmp/tessera-capstone-r3/unjoined.out:495`, `:847`.)

There is also a mutation-boundary conflict: E5’s withdrawal calls **both** equalities “exactly the check C-C12 removes,” but C-C12 explicitly retains `kT = kX`, as does its source. (`P:630–634`, `P:971`; `formal/suite/s-standing/proverif/ss_q3_companionB_entitled_via_envelope.pv:259–265`.)

**Required repair:** distinguish immutable presentation-term equalities from removable verifier checks throughout the mapping, and state that C-C12 retains `kT = kX`.

## 3. Prediction bases

The cap5a–cap8b citations match the recorded results, including cap7c and cap7d. Those follow-ups support the stated unchanged S-P1 outcomes for C-C6 and C-C7(i); they do not establish unqueried composition guarantees. The file correctly labels those broader guarantees as predictions. (`formal/suite/ledger-tests-2026-09-14/README.md:159–168`; `P:940–941`, `P:1751–1760`.)

One remaining basis statement is contradicted by that same evidence: the retained-query table says honest-key authorship is green “in every mutant that reds C-Q7.” C-C7(ii)’s repaired prediction and cap7b explicitly falsify both. The baseline prediction is not thereby disproved, but this supporting generalization must be removed. (`P:870`, `P:941`; `formal/suite/ledger-tests-2026-09-14/cap7b_sp1_q8_wrapper_signer_type_conditional.out:528`, `:1072`.)

## 4. Builder-ready contracts

Findings **1–3** require registration decisions before implementation: a layer-preserving completeness schema, a falsifiable scope consumer, and one consistent boundary between standing instrumentation and removable checks.

The two contestable fixture choices themselves are now explicit:

- Same-key wrapping is specified, its alternative and witness cost are stated, and C-C7(ii)’s expanded failed set is recorded. (`P:67`, `P:941`.)
- Adversary enrollment is restricted per compromise case, with no uncompromised authority process publishing the adversary’s manifest. (`P:65`, `P:869`.)

Neither choice is resolved or reversed here. Their stated consequences do not cure the separate completeness and standing-consumption defects above.

## 5. Routed and hidden choices

The **REFUSAL fork remains genuine**, with both options and costs stated. Exercising the foreign signing domain enables its tag-removal companion; leaving it unexercised leaves that test unavailable. I do not resolve it. (`P:1158–1179`; `formal/suite/lib/tessera_theory.pvl:66–76`.)

The file openly identifies the two contestable fixture choices. However, resolving findings **1–3** must not be delegated silently as encoding work: the alternatives change what can be proved or which companion can fail.

## 6. Accepted repairs and carried-forward corrections

| Accepted finding | Verification |
|---|---|
| R1.1: D7 common-content consumer | Repaired: link 5 and C-C16. `P:326–334`, `:1045`, `:1633`. |
| R1.2: C-C8 isolation contradiction | Repaired: possession-message and set-integrity obligations separated. `P:1573–1598`. |
| R1.3: C-C15 retained key-binding guarantees | Repaired: C-Q3 and link 5 removed from configuration (i)’s retained set. `P:1531`. |
| R1.4: C-Q6 composition join | Terms specified; repair remains incomplete under findings 2–3. `P:512–774`. |
| R1.5: one-key/one-manifest fixture | Repaired explicitly. `P:66`, `:429–460`. |
| R1.6: all other choices determined | Withdrawn; consequential choices identified. `P:1189–1253`. |
| R2.1: E1 shadows C-C12 | Structural rewrite succeeds in the bounded test; required mapping still contradicts it—finding 3. |
| R2.2: C-C15(i) retains C-Q7 | Repaired, with correct cap6 evidence. `P:1531`. |
| R2.3: same-key wrapping unspecified | Choice and C-C7 consequences explicit; cap7c/cap7d correctly cited. `P:67`, `:940–941`. |
| R2.4: adversary enrollment unspecified | Per-case choice explicit and supported by cap8. `P:65`, `:869`. |

The structural C-Q8 correction and link-1b correspondence correction remain honoured. Freshness and slot sharing remain explicit, but the intake revision requires the additional layer distinction in finding 1. (`P:815–827`, `P:234–249`, `P:125–154`.)

**This registration is not ready to freeze. The author should see first: finding 2, C-Q6’s missing falsifiable consumption of scope; finding 3, the surviving fingerprint precondition that can suppress C-C12 again; and finding 1, the completeness projection that can borrow another layer’s slot report. These are registration defects demonstrated or isolated on family-model copies, not capstone results.**

