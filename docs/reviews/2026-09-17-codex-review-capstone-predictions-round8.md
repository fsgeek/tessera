# Codex non-author review of the capstone registration, eighth round (2026-09-17)

Reviewer: OpenAI Codex CLI (`gpt-6-astra`), run non-interactively by the
owner instance on 2026-09-17 (19:24–19:32 UTC) against the whole of
`formal/suite/capstone/PREDICTIONS.md` after the round-seven repairs;
scratch diagnostics on family-model copies under
`/tmp/tessera-capstone-r8/`. **The reviewer found the registration not
ready to freeze**, on two findings of the round-seven coverage class,
and confirms all twenty-six earlier accepted findings present except as
these two reopen the case cells. Every run the reviewer cites was
reproduced on our tree
(`formal/suite/ledger-tests-2026-09-14/cap21a`–`cap21e`, twelfth batch
of that directory's README) at the reviewer's own `.out` line numbers.
No capstone model exists; nothing in the repository was run.

## Dispositions (owner instance, 2026-09-17)

Both are **clerk dispositions** of the owner instance. Disposition 2
retires a label rather than fixing one more cell, so that this class of
finding cannot recur.

1. **C-C5's strict "green control" alternative overlooks a same-key
   byte-binding failure.** ACCEPTED. The round-five reasoning for C-C5
   ("the degraded trace runs the `dsks` route, which strict denies")
   explains why `InnerSigTransplanted` can stay green in strict; it says
   nothing about C-Q8 and link 4, whose structural relation an
   **honestly authorized** key can break. Reproduced: with C-Q8's
   structural judge added and restricted to wrapped inner acceptances,
   the strict baseline is green (`cap21b_sp7_strict_base_sigbytes_wrapped.out:594`)
   and C-C5's unbinding makes it **red** in both channel variants
   (`cap21d_sp7_strict_cc5_wrapped.out:869`;
   `cap21e_…_repo.out:868`) while the four S-P7 safety queries stay
   green (`cap21d:898`–`:985`) and both witnesses reachable (`:1336`,
   `:1563`). The attack carries the issuer's honest **wrapper**
   signature, under its honestly authorized key, as the inner signature
   for attacker-built attestation bytes: the same-key-wrapping
   consequence C-C7(ii) already recorded, now at the inner layer, and
   no adversary-enrolled key is needed. **Repair:** C-C5's strict (a)
   and (b) are **mixed, descended**: C-Q8 and link 4 red;
   `InnerSigTransplanted`, C-Q4's `Rescoped`, `TypeConfused`, C-Q3 green;
   witnesses reachable; the whole-configuration green-control
   alternative is withdrawn, quoted. Neither contestable fixture choice
   is reversed.

2. **C-C2 and C-C15(i) still carry "green control, descended" from
   copies that declare none of C-Q7/C-Q8/C-Q9 or the linkage
   conjuncts.** ACCEPTED, and the label is retired. The round-seven rule
   was applied to two cells and the file then claimed no other cell had
   the omission; that claim (`:2902-2904`) was false and is withdrawn,
   quoted. **Repair, global:** "green control, descended" is **no longer
   a label this file uses for a whole configuration**. Every Cases cell
   states its strict outcome **per query**, in three lists — *descended
   green* (naming the run), *descended red* (naming the run),
   *predicted* (naming the basis) — and "green control" survives only as
   a **predicted** configuration-level reading beside those lists,
   never as a descended one. C-C2 (a): descended green on the five
   declared queries and three witnesses (`cap18a`); C-Q8, C-Q9, link 2b
   and every linkage conjunct predicted green. C-C15(i) (a)/(b):
   descended green on the four S-P7 queries and two witnesses
   (`cap14b`, `cap14c`); C-Q7, C-Q8, C-Q9 and the linkage conjuncts
   predicted green, with the basis stated (the inner signature is
   verified under `kW` over `fbI` with byte binding retained, so the
   C-C5 route of finding 1 does not open). Every other cell that names
   a green control is re-read under the retired label. The reviewer's
   own limit is carried: it established missing coverage, not that the
   unqueried relations are false.

3. **The REFUSAL fork stands**, unresolved, owed at the freeze commit;
   the three contestable choices (same-key wrapping, compromised-channel
   enrolment, `ev` as the pair in strict) stand.

**Loop.** One repair pass (Opus), then a ninth owner-run full Codex
pass. Rounds five through eight have all been about the per-case cells
the round-five repair introduced; retiring the descended-configuration
label is intended to close that class rather than repair it one cell
per round.

## Codex review — verbatim

## 1. Query strength and discharge

Repository files remained read-only. Diagnostics used family-model copies and a copied library under `/tmp/tessera-capstone-r8/`; no capstone model was constructed.

Below, **P** = `formal/suite/capstone/PREDICTIONS.md`, **L** = `formal/suite/ledger-tests-2026-09-14/`, and **T** = `/tmp/tessera-capstone-r8/`.

I found two supported defects: a contradicted companion classification and incomplete application of round seven’s query-coverage rule.

## 2. Companion consistency

**1. C-C5’s strict green-control alternative overlooks a same-key byte-binding failure.**

C-C5 permits strict cases (a)/(b) to be green controls because strict authority excludes the DSKS-derived key used by its degraded trace. That explains why `InnerSigTransplanted` can remain green; it does not protect C-Q8 or link 4 against substitution under an honestly authorized key. (`P:1490`; C-Q8’s structural contract at `P:1239–1249`.)

I copied `cap14a_sp7_q1_strict_base.pv`, added C-Q8’s structural judge **restricted to wrapped inner acceptances**, and applied exactly the registered signature-byte unbinding. The fixture, authority checks, possession checks and frame checks remained intact. (`T/cc5_strict_wrapped.pv:193–208`, `:259–263`.)

| Diagnostic | Structural byte binding | Four existing S-P7 safety queries | Honest witnesses |
|---|---|---|---|
| Matched strict baseline | Green | Green | Reachable |
| C-C5, DNS compromised | **Red** | Green | Reachable |
| C-C5, repository compromised | **Red** | Green | Reachable |

Evidence: `T/cc5_base_wrapped.out:594–658`, `:993`, `:1204`; `T/cc5_strict_wrapped.out:869–985`, `:1336`, `:1563`; `T/cc5_strict_repo_wrapped.out:868–982`, `:1333`, `:1559`.

The reconstructed attack uses an **honest wrapper signature under an honestly authorized key** as the inner signature accompanying different, attacker-constructed attestation bytes. Both authority checks pass; no adversary-enrolled key is needed. (`T/cc5_strict_wrapped.out:856–869`.)

**Required repair:** register the strict outcome as mixed: C-Q8/link 4 red, `InnerSigTransplanted` green at this projection. Withdraw the whole-configuration green-control alternative. Neither contestable fixture choice needs reversing.

## 3. Prediction bases and green-control audit

**2. C-C2 and C-C15(i) still claim descended green controls from copies missing capstone queries they can carry.**

The new rule expressly prohibits this, yet its assertion that no other cell has the omission is false. (`P:1465–1482`, `:2902–2904`.)

| Cell | Strict copies | Missing coverage |
|---|---|---|
| **C-C2**, case (a): “GREEN CONTROL, DESCENDED” | `cap18a_sp2_strict_cc2.pv` | C-Q8, C-Q9 and link 2b are required green by the row but are undeclared. The copy queries only `Stripped`, `SignerForged`, `SetAltered`, `Reattributed`, `Spliced` and three witnesses. |
| **C-C15(i)**, cases (a)/(b): “GREEN CONTROL … DESCENDED” | `cap14b_sp7_q1_strict_q6b.pv`, `cap14c_sp7_q1_strict_repo_q6b.pv` | Neither declares generic C-Q7, structural C-Q8/C-Q9, or the structural linkage queries. Both query four S-P7 safety properties and two witnesses. |

Citations: `P:1487`, `:2094`; `L/cap18a_sp2_strict_cc2.pv:143–176`; `L/cap14b_sp7_q1_strict_q6b.pv:113–130`; `L/cap14c_sp7_q1_strict_repo_q6b.pv:113–130`.

C-C15’s separate predicted-retention paragraph does not satisfy the stricter rule governing the **“descended green control”** label: that label requires every capstone query the copy can carry to be declared. Its strict C-Q7 outcome also lacks the explicit prediction qualification given to configuration (ii). (`P:1470–1472`, `:2094`.)

**Required repair:** distinguish demonstrated greens from explicitly predicted greens per query, or instrument the missing relations. I have established missing coverage here, **not that those unqueried relations are false**.

The remaining candidate strict controls in C-C4–C-C6 and C-C15(ii) are labelled predictions; finding 1 falsifies C-C5’s all-green alternative. C-C8’s isolation cells state individual query outcomes rather than descended all-green configurations. (`P:1489–1491`, `:2094`, `:2137–2138`.)

I found no new misquoted result polarity in the cap5a–cap20g diagnostic citations. The defects concern their interpretation and coverage.

## 4. Builder-ready contracts

Finding 1 requires a definite mixed strict assignment for C-C5. Finding 2 requires explicit query-by-query evidence status before the builder can apply the green-control classification.

No further independently supported buildability defect emerged from the repaired join, evidence-pair or layer-grouping contracts.

## 5. Routed and contestable choices

The **REFUSAL fork remains genuine**, with both options and costs stated: exercise the foreign signing domain and add its query/companion, or retain declared-and-unexercised status and leave the tag-severing demonstration unavailable. Its resolution remains owed before freeze. I leave it unresolved. (`P:1715–1718`, `:1722–1743`; `formal/suite/lib/tessera_theory.pvl:66–76`.)

Same-key wrapping and compromised-channel-only enrollment remain explicit. Finding 1 exposes a consequence the enrollment argument does not exclude; it reverses neither choice. (`P:65–67`.)

## 6. Accepted findings and carried-forward corrections

The twenty-six accepted findings were checked against the operative repairs:

| Accepted findings | Verification |
|---|---|
| **R1.1–R1.6** | Content consumer/companion, possession isolation, C-C15 losses, composition join, one-key/one-manifest assignment and withdrawal of “every other choice determined” are present. (`P:428–447`, `:2137–2161`, `:2094`, `:744–881`, `:582–615`, `:1753–1794`.) |
| **R2.1–R2.4** | Independent standing path, C-C15’s C-Q7 loss, same-key wrapping and per-case enrollment are present. (`P:752–837`, `:2094`, `:65–67`.) |
| **R3.1–R3.4** | Layer-preserving projection, scope consumer, immutable-term/removable-check distinction and corrected authorship basis are present. (`P:351–385`, `:976–1016`, `:866–881`, `:1360`.) |
| **R4.1–R4.2** | Pair-scope comparison, identity-only configuration and vocabulary-witness exception are present. (`P:1014–1055`, `:2094`, `:1283–1349`.) |
| **R5.1–R5.2** | Membership severing is repaired; case assignments remain incomplete under findings 1–2 above. (`P:2257`, `:1490`, `:2094`.) |
| **R6.1–R6.6** | Attribution observation, mixed outcomes, case-(c) separation, case-(b) evidence status and C-C10’s deleted-check assignment are present. C-C2’s blanket control label still fails the coverage audit. (`P:473–513`, `:1487–1495`, `:1521–1522`, `:2094`.) |
| **R7.1–R7.2** | Both local repairs are present: strict C-C3 is mixed; strict `ev` is a pair; link 1a is per-channel; C-C10’s control and distinguishing signal are corrected. The new class rule is not applied globally—finding 2. (`P:164–199`, `:279–300`, `:1488`, `:1495`.) |

All three ledger corrections remain honoured: structural exact-byte verification without authorship overclaim, publication provenance as a correspondence, and fresh presentation identity with layer-preserving acceptance grouping. (`P:1239–1249`, `:308–323`, `:115–162`.)

**This registration is not ready to freeze.** The author should see first: **(1)** C-C5’s demonstrated mixed strict outcome, **(2)** the remaining unsupported descended-green-control claims for C-C2 and C-C15(i), and **(3)** the outstanding REFUSAL decision. The third priority is the existing routed decision, not a newly invented defect.

