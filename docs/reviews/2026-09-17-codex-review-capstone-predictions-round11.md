# Codex non-author review of the capstone registration, eleventh round (2026-09-17)

Reviewer: OpenAI Codex CLI (`gpt-6-astra`), run non-interactively by the
owner instance on 2026-09-17 (20:37–20:48 UTC) against the whole of
`formal/suite/capstone/PREDICTIONS.md` after the round-ten repairs;
scratch diagnostics on family-model copies under
`/tmp/tessera-capstone-r11/`. **The reviewer found the registration not
ready to freeze on one finding**, and wrote: *"Only one new defect is
established, so I cannot honestly supply three independent findings."*
It confirms all thirty-three earlier accepted findings present, the
round-ten repairs correctly registered, and the README's degraded/strict
labelling of `cap23g`/`cap23h` correct after the same-day correction.
The one run it cites was reproduced on our tree
(`formal/suite/ledger-tests-2026-09-14/cap24a`–`cap24c`, fifteenth
batch of that directory's README) at the reviewer's own `.out` line
numbers. No capstone model exists; nothing in the repository was run.

## Dispositions (owner instance, 2026-09-17)

1. **C-C15(i) still predicts `SignerForged` green by reasoning about
   the checked outer tuple.** ACCEPTED. The cell's retained-list
   justification called `SignerForged` a relation over the outer tuple;
   under §1.3's report contract the inner acceptance reports its own
   presented tuple and manifest-named slot, unchecked by this mutation.
   Reproduced with S-P2's membership observer (the registered
   `MemberJudge` relation, `s-p2/PREDICTIONS.md:270-273`) added to the
   round-ten copies: the correct strict baseline keeps `SignerForged`
   unreachable (`cap24a_sp7_strict_base_member.out:1421`); C-C15(i)
   makes it **reachable** in both channel variants
   (`cap24b_sp7_strict_q6b_member.out:3211`; `cap24c_…_repo.out:3211`),
   with the four S-P7 queries green (`:708`–`:738`) and both witnesses
   reachable (`:1014`, `:1221`). The trace (`cap24b:3199-3211`): valid
   same-key wrapping credentials retained, the **other** honest issuer's
   manifest presented as the inner tuple, and its named slot reported
   as satisfied by the wrapper key — `SignerForged(M2, pk(skI1))`. No
   adversary-enrolled identity, neither contestable choice reversed.
   **Repair:** `SignerForged` moves from *predicted green* to
   **descended red** in C-C15(i)'s strict lists for (a) and (b), and to
   *predicted red* in (d) under the contract; the outer-tuple
   justification is withdrawn, quoted; the reviewer's own limits are
   carried — the exploratory completeness (link 2b) result is **not** a
   finding because the family projection lacks the capstone's retained
   two-signer set logic, and `Stripped` red is **not** inferred from the
   membership result; both stay predicted.

2. **The REFUSAL fork stands**, unresolved, owed at the freeze commit;
   the four contestable choices stand.

**Loop.** One repair pass (Opus), then a twelfth owner-run full Codex
pass. Findings per round have been 4, 3+1, 2, 2, 6, 2, 2, 3, 2, 1; the
composition contract has drawn no finding since round four; rounds nine
to eleven have been the report contract's consequences propagating
through one companion's predictions.

## Codex review — verbatim

## 1. Query adequacy

No additional run-backed defect established in the query forms. Finding 1 concerns a companion’s retained guarantee under the registered reporting contract.

## 2. Companion outcomes

**1. C-C15(i) still predicts `SignerForged` green by reasoning about the checked outer tuple, although the judge must observe the presented inner tuple.**

The retained-list justification explicitly calls `SignerForged` a relation over the **outer** tuple. The reporting contract instead requires the inner acceptance’s own presented tuple and its manifest-named slot, even when those terms are unchecked. These instructions give different results. (`formal/suite/capstone/PREDICTIONS.md:2173`, `:164–169`, `:201–240`.)

I added S-P2’s membership observer to copies of `cap23b`, `cap23d` and `cap23f`, leaving their fixtures and verifier checks unchanged. The observer pairs an honest `(key, manifest)` with the reported `(tuple, slot fingerprint, accepting key)` and fires when another key satisfies that honest signer’s slot—the registered `MemberJudge` relation. (`formal/suite/s-p2/PREDICTIONS.md:271–276`; `/tmp/tessera-capstone-r11/member_q6b.pv:171–182`.)

| Copy | `SignerForged` |
|---|---|
| Correct strict baseline | Unreachable — `/tmp/tessera-capstone-r11/member_base.out:1421` |
| C-C15(i), DNS compromised | **Reachable** — `/tmp/tessera-capstone-r11/member_q6b.out:3211` |
| C-C15(i), repository compromised | **Reachable** — `/tmp/tessera-capstone-r11/member_q6b_repo.out:3211` |

The trace retains valid same-key wrapping credentials, presents the other honest issuer’s manifest as the inner tuple, and reports its named slot as satisfied by the wrapper key. The membership judge detects precisely that mismatch. It requires neither an adversary-enrolled honest-channel identity nor reversal of the same-key wrapping choice. (`/tmp/tessera-capstone-r11/member_q6b.out:3199–3211`.)

Both honest witnesses remain reachable in both mutants; the original four S-P7 safety queries remain green. This is an additional observable consequence of the specified mutation, not a dead fixture. (`/tmp/tessera-capstone-r11/member_q6b.out:708–738`, `:1014`, `:1221`; corresponding repository output at the same lines.)

**Required repair:** remove `SignerForged` from C-C15(i)’s strict retained-green list and record the demonstrated family-copy relation. Reporting only the checked outer tuple would contradict §1.3. These runs establish neither a capstone result nor a degraded-mode result.

## 3. Predictions and evidence

Finding 1 contradicts a stated green prediction and its basis. No separate numerical-probability defect established.

The checked diagnostic citations resolve to their intended evidence. In particular, the registration correctly treats `cap23d/f` as strict and `cap23g/h` as degraded despite the latter filenames. (`formal/suite/capstone/PREDICTIONS.md:3345–3347`, `:3362–3365`; `formal/suite/ledger-tests-2026-09-14/README.md:450–455`.)

## 4. Buildability

No additional independently established finding.

I do **not** count the exploratory completeness failure as a second defect: that family projection lacks the capstone’s retained two-signer set logic. It therefore cannot settle C-C15(i)’s link-2b prediction. Nor do I infer `Stripped` red from the membership result.

## 5. Routed and hidden choices

The `REFUSAL` fork remains genuine: both options, their costs, and the requirement for author disposition before freezing are explicit. I leave it unresolved. (`formal/suite/capstone/PREDICTIONS.md:1794–1822`.)

The two contestable fixture choices remain explicit and are not reversed here. Finding 1 survives them. (`formal/suite/capstone/PREDICTIONS.md:65–67`.)

## 6. Earlier accepted findings

The requested repairs for the thirty-three accepted findings are present; finding 1 extends the retained-list audit rather than reversing an earlier disposition. The three ledger corrections remain operative: structural exact-byte checking, publication provenance as a correspondence, and fresh intake identifiers with layer-indexed completion. (`formal/suite/capstone/PREDICTIONS.md:115–162`, `:350–365`, `:393–438`, `:1280–1300`.)

Specifically, round 10’s five additional C-C15(i) reds are registered in strict and predicted in degraded, and C-C13(ii)’s type failure is assigned only to the affected wrapper layers. (`formal/suite/capstone/PREDICTIONS.md:3345–3347`.)

**This registration is not ready to freeze. Only one new defect is established, so I cannot honestly supply three independent findings. The author should see first: the demonstrated `SignerForged` contradiction; its cause—the surviving outer-tuple justification conflicts with the inner reporting contract; and the still-required `REFUSAL` ruling. All new runs used family copies under `/tmp`; no repository file was changed and no capstone model was built.**

