# Codex non-author review of the capstone registration, fifteenth round (2026-09-18) — clerical confirmation after round fourteen

Reviewer: OpenAI Codex CLI (`gpt-6-astra`), `codex exec`, run
non-interactively by the successor owner instance on 2026-09-18
(00:23–00:26 UTC) against the whole of
`formal/suite/capstone/PREDICTIONS.md` (3989 lines), diffing it against
a byte-exact copy of the file as round fourteen reviewed it. Subject:
the **four clerical edits** the successor made on arrival (review log
extended to rounds 13 and 14; the skeptic's reading table recomputed
after the round-13 shift; the round-14 record's batch and copy counts
corrected; the two reads of the author's handoff note archived), not
the registration's substance. **Lines 1–2008 byte-identical; no query,
companion, probability, timebox, set or Cases cell moved; ranges and
counts verified; one packaging dependency** (this record did not yet
exist when the handoff named it). Its judgment, verbatim: *"The
registration remains ready to freeze subject to the author's items."*
No models were written or run.

## Disposition (owner instance, 2026-09-18)

Findings 1–4 and 6: confirmations, nothing to do. **Finding 5
ACCEPTED**: the handoff's staging block named this record before it
existed; archiving it here, and entering the round's line in the
registration's review log, closes that dependency. The review log line
is the last edit to the file before the author's read, and this record
is the last review record; the loop on the registration's text ends
here. Findings per round, fifteen rounds: 6, 4, 4, 2, 2, 6, 2, 2, 3, 2,
1, 0, 3, 0, 0 — the three of round thirteen were corrections of the
skeptic repair, and rounds twelve, fourteen and fifteen found nothing
in the registration.

## Codex review — verbatim

1. **Registration diff passes.** Against the supplied round-14 snapshot, the only changes are “Twelve” → “Fourteen,” the two review-log bullets, and the reading-table corrections and explanation. Lines 1–2008 are byte-identical. No query, companion, probability, timebox, set membership, or Cases cell changed or was reordered. Later material shifts down two line numbers because of the inserted bullets. (`formal/suite/capstone/PREDICTIONS.md:2024`, `:2046–2047`, `:3958–3975`.)

2. **Reading ranges and counts pass.** Counting whitespace-separated words over the inclusive ranges gives:

   | Passage | Range | Words |
   |---|---|---:|
   | Freeze statement | 1885–1906 | 200 |
   | Routed items | 1907–2008 | 893 |
   | Adversary and Wrapper rows | 77 and 79 | 621 |
   | Evidence/report contracts and event table | 188–261 | 893 |
   | Optional discharge matrix passage | 1778–1810 | 1,126 |

   The first four total **2,607**, correctly summarized as approximately 2,600; the optional passage adds approximately 1,100. The ranges reach the stated passages, including the event table’s end at line 261. (`formal/suite/capstone/PREDICTIONS.md:3959–3975`.)

3. **Review-log additions pass.** Round 13 records three accepted corrections and a verdict that the then-current registration needed those corrections; its new bullet accurately reports three accepted corrections without claiming approval. Round 14 records zero new findings and readiness subject to the author’s items, including the `cap25`/`cap26` reruns. (`formal/suite/capstone/PREDICTIONS.md:2046–2047`; `docs/reviews/2026-09-17-codex-review-capstone-predictions-round13.md:19–41`, `:110`; `docs/reviews/2026-09-17-codex-review-capstone-predictions-round14.md:7–17`.)

4. **Archive-count correction passes.** README batches five through seventeen are thirteen batches. Direct filesystem enumeration finds **99 `cap*.pv` files**, spanning `cap1`–`cap26`; the directory’s **130 total models** are a different count. The corrected round-14 paragraph therefore states the right collection and totals. (`formal/suite/ledger-tests-2026-09-14/README.md:107`, `:520`; `docs/reviews/2026-09-17-codex-review-capstone-predictions-round14.md:32–35`.)

5. **One current-tree packaging defect remains.** The handoff’s `git add` command names `docs/reviews/2026-09-18-codex-review-capstone-predictions-round15.md`, which does not yet exist. As written, that command would fail on the missing pathspec. Its “17 review records” expectation and statement that the fifteenth pass confirms the file anticipate an archive not yet present. Current porcelain status contains **210 changed/untracked files, including 16 review records**, none staged; every existing changed path falls within the listed package. Archive this report and its disposition before treating that command and confirmation sentence as final. All handoff locators into the registration still reach their stated passages. (`formal/suite/capstone/READ-FREEZE-2026-09-17.md:148–156`, `:167–173`, `:187–189`.)

6. **No contradiction with the registration’s freeze statement or earlier repairs found.** The clerical registration changes leave §8 and the repair sections unchanged and do not resolve the REFUSAL fork or any contestable choice. The new archive contains both handoff reviews and their dispositions. This confirmation used file inspection and counting only; no models were written or run. (`formal/suite/capstone/PREDICTIONS.md:1885–1906`, `:3977–3989`; `docs/reviews/2026-09-17-codex-review-capstone-read-freeze.md:10`, `:74`, `:93–95`.)

The registration **remains ready to freeze subject to the author’s items**. The only additional matter the author must see is the packaging dependency above: the handoff currently describes this confirmation and its archive as complete before that archive exists. No additional substantive decision emerged from these clerical edits.
