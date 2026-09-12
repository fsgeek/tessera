# run4/ — archived TLC outputs of run 4 (2026-09-06 19:18–19:19Z)

**STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not
adopted; the commit is the author's. PROBE — NON-DISCHARGING.**

These are the `.out` files exactly as `run-probe.sh` wrote them in run 4
(the second collaborator pass, `RESULTS-PROBE.md` addendum), copied here
unmodified before run 5 regenerated the working-directory `.out` files
(PROBE.md post-run note 3 item 7). Purpose: make the run 4 → run 5 diff
checkable by a reader, which the run 3 → run 4 claim was not (run 3's
outputs were not retained). Diff against the parent directory with, e.g.

    diff <(grep -vE 'seed|pid|Finished in|Starting|tlc-[0-9]+|^### run-probe|states generated' run4/X.out) \
         <(grep -vE 'seed|pid|Finished in|Starting|tlc-[0-9]+|^### run-probe|states generated' X.out)

Each file carries its own STATUS line and P4 join-source line at the top.
