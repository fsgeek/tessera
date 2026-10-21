Completed the [full report](/home/tony/projects/tessera/prototype/p8-falsify/REPORT.md), including every proof step, seven numbered findings, exact lines, reproduction commands, outputs, and test counts.

No encoding collision or differing successful decode was found. Findings include a concrete counterexample to Lemma 9’s unrestricted claim, oversized-exponent crashes, rejection-order disagreement, and missing standalone payload size enforcement.

All 106 golden and 236 rejection vectors passed. Additional testing included 106,185 seeded cases, 60,884 exhaustive mutations, and 3,000 Hypothesis pairs. All review artifacts are under `prototype/p8-falsify/`.

VERDICT: SURVIVED WITH GAPS (P8F-01–04; text defects P8F-05–07)


