# Scoped safety confirmation: detection tests after fixes (steward, 2026-11-23)

In /home/tony/projects/tessera, commit 0610236 applies Gemini's fixes (`docs/reviews/detection-tests/FIXES.md`) to the
findings in `docs/reviews/detection-tests/CODEX-REVIEW.md`; the brief is r5 (`BRIEF-gemini.md`: no recorded POST).
Review `git show 0610236` and the code in `service/detect/tests-live/`. Read-only except your report; no AWS calls.
**Safety only**: for findings 1-12 report CONFIRMED / PARTIAL / NOT FIXED with file:line and a concrete scenario, and
sweep for any remaining path that could touch a production resource, act outside us-east-2, send the key elsewhere,
exceed the rate rule, create a record in the production request table, leave a resource untracked, or write a secret
or URL. Fidelity is out of scope for this round.
Exit (pre-registered): the steward fixes any NOT FIXED or new safety HIGH with the smallest change (or removes the
capability) and reruns the offline tests; then the author decides on the live run. No further round.
Write docs/reviews/detection-tests/CODEX-CONFIRM.md. Findings only.

