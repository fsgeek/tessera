You are a cross-family reviewer for Project Tessera (repo /home/tony/projects/tessera). Prior review: dev/slice_probe/codex/REVIEW.md (you or a sibling found the slice method sound with conditions and confirmed C-C2 C-Q3 A and C-C5 InnerSigTransplanted traces). Narrow task now: for each slice red below, read the reconstructed trace in dev/slice_probe/out/ (file stems in runs.log / gen_ext/) and decide whether it instantiates the REGISTERED case-(d) attack mechanism of that companion (formal/suite/capstone/PREDICTIONS.md: the companion's MUTATES lines, its (d) set (1), and the family trace its (d) Cases cell cites; open that family .out under formal/suite/ledger-tests-2026-09-14/ or wherever the citation points).

Traces to judge (these carry Band 0 exit rows):
- D10: C-C3 C-Q5 SetAltered (depth0.cone) and C-C8 C-Q5 (depth0.cone). Crucial: is C-Q5's red the CONSUMER failing because the severed link (producer C-Q9) let altered sets through, or something else?
- D2: C-C4 C-Q4 Rescoped and link 6b (depth1.cone).
- D6: C-C7(i) C-Q8 and link 4 (depth0.cone) and AcceptedUnderHonestKey ==> IssuerSigned (depth0); C-C7(ii) C-Q8 and link 4.
- D7 membership: C-C17 link 2a (depth0.cone) and SignerForged (depth0).
- D1: C-C2 link 5 (the earlier review did C-Q3 A only).

For each: verdict (registered mechanism / different but valid attack within case (d) / artifact), 3-6 lines of plain-language trace summary with out-file line numbers, and whether the slice removed anything the registered attack needs (it must not matter, but note it). Re-run any one you doubt with ~/.local/bin/proverif (timeout 1800; lib path as run.sh uses).
No VM access, no staging/commits, write only under dev/slice_probe/codex2/. Output codex2/REVIEW.md: a table first, then per-trace notes. Be blunt.
