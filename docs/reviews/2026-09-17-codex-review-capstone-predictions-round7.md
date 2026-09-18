# Codex non-author review of the capstone registration, seventh round (2026-09-17)

Reviewer: OpenAI Codex CLI (`gpt-6-astra`), run non-interactively by the
owner instance on 2026-09-17 (19:07–19:15 UTC) against the whole of
`formal/suite/capstone/PREDICTIONS.md` after the round-six repairs;
scratch diagnostics on family-model copies under
`/tmp/tessera-capstone-r7/`. **The reviewer found the registration not
ready to freeze**, on two findings of one class: a strict copy that
**declares no capstone query** was read as an all-green control. It
confirms the round-six link-6b repair, the case-(b) descent, the case-(c)
withdrawal, the mixed C-C7 and C-C8 cells, and all twenty-four earlier
accepted findings except the two cells below. Every run the reviewer
cites was reproduced on our tree
(`formal/suite/ledger-tests-2026-09-14/cap20a`–`cap20g`, eleventh batch
of that directory's README) at the reviewer's own `.out` line numbers.
No capstone model exists; nothing in the repository was run.

## Dispositions (owner instance, 2026-09-17)

Both are **clerk dispositions** of the owner instance. Disposition 2
fixes one contract term (what `ev` is in strict) and is marked
**contestable**.

1. **C-C3's strict "green control" contradicts C-Q9.** ACCEPTED. The
   strict copy `cap18b` declares neither C-Q9 nor a possession-binding
   judge; its mutation produces and accepts `(POSS, fp(k))` where C-Q9
   and link 3 require `(POSS, t)`. Reproduced: with the per-slot
   possession report and the C-Q9 judge added and nothing else changed,
   **C-Q9 is red** (`cap20a_sp2_strict_cc3_q9.out:1319`) while
   `SetAltered` and the other three stay green (`:414`–`:439`) and the
   witnesses stay reachable (`:616`, `:848`, `:1091`); restoring
   possession-over-tuple with the frame's manifest-hash guard still
   absent makes C-Q9 **green** (`cap20b…out:1098`, witness `:1090`).
   **Repair:** C-C3's strict (a) is **mixed, descended**: C-Q5 green,
   **C-Q9 and link 3 red** — the (α)/(β) split C-C8's cell already
   records; (b) predicted the same way; the "green control, descended"
   wording is withdrawn, quoted, in the Cases cell and the round-six
   scratch table. **And the class rule goes into §4's preamble:** *a
   family copy's declared queries are not the capstone's query set; a
   configuration may be called a green control only over the
   capstone's queries, each of which is either declared in the copy or
   predicted and marked so; "descended green control" is written only
   when every capstone query the copy can carry is declared in it.*

2. **C-C10's isolation control does sever link 1a, and the evidence
   term `ev` was unspecified in strict.** ACCEPTED, with a contract
   term fixed, **contestable**. In the control (compromised channel's
   check deleted) the verifier checks `evR` but emits `AcceptS(ev, …)`
   carrying the unchecked `ev`. Reproduced: a structural link-1a judge
   over the carried term is **green** on the strict baseline
   (`cap20c_sp1_strict_base_evidence_either.out:585`; channel-specific
   form `cap20d…out:589`) and **red** on the control
   (`cap20e…out:732`, either-key form; `cap20f…out:737`,
   channel-specific), with publication provenance green (`cap20e:572`,
   `cap20f:577`) and honest acceptance reachable (`:556`, `:560`); on
   C-C10's strict form (honest check deleted) it is red too
   (`cap20g…out:1055`) beside link 1b (`:887`) and unrestricted
   authorship (`:728`). **The contract term:** in strict, `ev` in
   `LayerAccepted` is the **pair** of evidence terms the acceptance
   carried, one per channel, and link 1a requires **each** to verify
   over the consumed `t` under its own channel key (the
   channel-specific form, `cap20d`); in degraded it is the sole term.
   This is what §1.3 already says in words ("the accepted evidence
   term this acceptance consumed"), made exact for two channels, and it
   is the reading under which deleting either check reds link 1a — the
   right property for a binding link. **Repair:** §1.3 states the pair;
   link 1a's query states the per-channel form; C-C10's isolation
   control is registered **mixed**: link 1a **red** (descended `cap20f`,
   `cap20e`), **link 1b and unrestricted authorship green**
   (`cap17d:547`, `:539`), everything else green; its purpose sentence
   changes from "if all green, the wrong check was deleted" to "if link
   1b is red, the honest check was deleted (the companion); if link 1b
   is green and link 1a red, the compromised check was (the control)";
   the withdrawn "severs nothing" is quoted.

3. **The REFUSAL fork stands**, unresolved, owed at the freeze commit;
   the two contestable choices stand, and the reviewer names the fork
   as "the existing author decision, not a newly invented defect".

**Loop.** One repair pass (Opus), then an eighth owner-run full Codex
pass. Round seven's findings are the last two cells of the round-five
case assignment that were not written from a run carrying the
capstone's query; nothing else in the file drew a finding.

## Codex review — verbatim

## 1. Query strength and discharge

I found two defects in the companion registrations, detailed below. Both arise from treating a family model’s declared queries as the complete capstone query set.

The revised link 6b now consumes the envelope path’s own attribution report and compares it with that path’s inner frame. C-Q6 conjunct 3 separately compares the two paths’ reports. The round-6 objection to their conflation is repaired. (`formal/suite/capstone/PREDICTIONS.md:179`, `:425–465`, `:947–968`.)

Below, **P** denotes `formal/suite/capstone/PREDICTIONS.md`, **L** denotes `formal/suite/ledger-tests-2026-09-14/`, and **T** denotes `/tmp/tessera-capstone-r7/`. Repository files remained unchanged; diagnostic models and outputs were created only under **T**. No capstone model was constructed or run.

## 2. Companion consistency

### Finding 1 — C-C3’s strict “green control” contradicts C-Q9

C-C3 registers strict case (a) as **GREEN CONTROL, DESCENDED**, and predicts the same for (b). The definition requires every query green. But `cap18b` declares neither C-Q9 nor its equivalent possession-binding judge. The row acknowledges missing `Spliced` coverage while overlooking this more consequential omission. (P:1381–1384, P:1421, P:2698; L`cap18b_sp2_strict_cc3.pv:93–110`.)

The mutation produces and accepts `(POSS, fp(k))`. C-Q9 and link 3 require `(POSS, t)` for the accepted manifest. Strict authority verification can preserve `SetAltered` without repairing that structural mismatch. (L`cap18b_sp2_strict_cc3.pv:132`, `:149`, `:168–169`; P:350–360, P:1212–1219.)

I copied `cap18b`, added the registered per-slot possession report and structural judge, and left its fixture and verifier unchanged:

| Diagnostic | C-Q9 equivalent | Honest acceptance |
|---|---|---|
| C-C3 strict mutation | **Red** | Reachable |
| Same model, possession-over-tuple restored; frame manifest hash still absent | **Green** | Reachable |

Evidence: T`cc3_strict_q9.out:1319`, `:1091`; T`cc3_strict_q9_poss_restored.out:1098`, `:1090`. The original four safety queries remain green in the mutant. (T`cc3_strict_q9.out:414–439`.)

**Required repair:** register strict C-C3 as mixed: C-Q5 green, C-Q9/link 3 red. Withdraw the all-green inference in both Cases cells and the scratch-run summary. This is the same separation already correctly recognized for strict C-C8. (P:1426.)

### Finding 2 — C-C10’s opposite-check deletion does sever evidence binding

The revised principal mutation correctly deletes the honest channel’s check. However, its new opposite-deletion control is registered as green and said to “sever nothing.” The cited run establishes publication provenance, authorship and signature-query outcomes; it does not query link 1a’s evidence-binding relation. (P:1428, P:2695; L`cap17d_sp1_strict_cc10_drop_compromised.pv:207–263`.)

In that control, the verifier checks `evR` but emits `AcceptS(ev, t, …)` carrying the unchecked `ev`. An attacker can retain a valid tuple and its honest-channel evidence while replacing `ev` with an arbitrary term. Publication provenance remains true; the carried evidence is unbound. (L`cap17d_sp1_strict_cc10_drop_compromised.pv:267–277`; P:243–249.)

I added a structural judge over that existing accepted evidence. To avoid imposing a stronger channel-specific requirement, the judge accepts evidence verifying over the consumed tuple under **either** authority key:

| Diagnostic | Evidence binding | Publication provenance |
|---|---|---|
| Matched strict baseline | **Green** | — |
| Compromised-channel check deleted | **Red** | **Green** |

Evidence: T`cap17a_sp1_strict_judges_base_either.out:585`; T`cap17d_sp1_strict_cc10_drop_compromised_either.out:732`, `:572`. Honest acceptance remains reachable in both. (`:571` and `:556`, respectively.)

**Required repair:** register this control’s mixed outcome. Alternatively, explicitly specify a different evidence-selection contract and justify it. Switching the observation to the retained, checked evidence would be an additional contract choice; it does not follow from merely deleting the opposite check.

## 3. Prediction bases and Cases audit

The unsupported strict assertions found are the **complete green-control claims in findings 1 and 2**. Their cited query results are accurately transcribed; the inference to unqueried consuming relations is false.

The other tenth-batch corrections match their named results: C-C2’s declared queries are green; C-C8 and C-C7 are mixed as recorded; C-C16 and C-C17 have their recorded reds; C-C10’s principal strict mutation has red provenance and unrestricted authorship with its named retained guarantees green. (P:1420, P:1425–1428, P:2116–2150, P:2190; P:2693–2703.)

Strict outcomes without a corresponding strict diagnostic remain explicitly **predictions** in C-C4–C-C6, C-C9, C-C13, C-C15(ii), and C-C8’s isolation configurations. Channel-symmetric case-(b) predictions are distinguished from recorded runs. These are not additional descent defects. (P:1422–1424, P:1427, P:1456, P:2027, P:2049–2114.)

The added `_repo` citations correctly support the recorded case-(b) outcomes for C-C11 and C-C15(iii), including their differing output-line offsets. C-C12’s case (b) remains predicted rather than falsely attributed to a nonexistent repository-compromised run. (P:1454–1455, P:2027.)

I found no additional cited run contradicting a registered probability’s stated basis.

## 4. Builder completeness

Finding 2 leaves a consequential observation choice: **which evidence term does the opposite-deletion control report to link 1a?** The principal mutation specifies the deleted check’s evidence; the control cannot receive an all-green outcome merely by silently observing another term. This needs resolution in the registration. (P:1428.)

No further independently supported buildability defect emerged from the repaired event contracts.

## 5. Routed and fixture choices

The `REFUSAL` fork is genuine and presents both options and their costs: exercise the domain with an honest signer and acquire an early refusal fixture, or leave it unexercised and lose the load-bearing tag demonstration. The file reserves that decision to the author and requires an amendment before freeze if a query and companion are added. I do not resolve it. (P:1655–1676; `formal/suite/lib/tessera_theory.pvl:66–76`.)

Same-key wrapping and compromised-channel-only adversary enrollment remain explicit fixture choices. I found no new inconsistency requiring either choice to be reversed. (P:65–67.) Finding 2’s evidence-selection issue is the additional substantive choice that must not be left to the builder.

## 6. Earlier findings and carried-forward corrections

The three ledger corrections remain honored: structural C-Q8, publication provenance as a correspondence, and acceptance/layer identity in the chain reports. (P:1191–1201, P:260–275, P:115–180, P:303–347.)

Of the twenty-four accepted findings:

| Earlier findings | Verification |
|---|---|
| Round 1, findings 1–6 | Repairs present. |
| Round 2, findings 1–4 | Repairs present; the two contestable fixture choices remain explicit. |
| Round 3, findings 1–4 | Repairs present. |
| Round 4, findings 1–2 | Repairs present. |
| Round 5, finding 1 | Membership companion and its consequential failed set present. |
| Round 5, finding 2 | **Incomplete:** Cases coverage exists, but findings 1–2 above invalidate two green-control assignments. |
| Round 6, finding 1 | Attribution-based link 6b repaired. |
| Round 6, finding 2 | **Incomplete:** strict C-C3 is still misclassified. |
| Round 6, findings 3–5 | Mixed C-C7 outcomes, case-(c) withdrawal, and repository-compromised descent repaired. |
| Round 6, finding 6 | Principal mutation repaired; **new isolation-control claim defective**, as finding 2 shows. |

Repair locations: P:2226–2233, P:2291–2297, P:2377–2381, P:2468–2471, P:2190, P:2562–2564, P:2672–2677. These judgments concern the current operative contracts, not merely their disposition labels.

**This registration is not ready to freeze.** The author’s three priorities are: **(1)** replace C-C3’s strict all-green assignment with the C-Q5/C-Q9 split demonstrated above; **(2)** correct C-C10’s isolation-control outcome and fix its evidence-observation contract; **(3)** decide the explicitly routed `REFUSAL` fork before freezing. The third item is the existing author decision, not a newly invented defect.

