# Disposition: Codex non-author review of Amendment 10, revision 2 (2026-10-17)

The owner accepted all eight findings. Each is applied with Codex's exact proposed text, to
`docs/phase-0-prereg-amendment-10.md` and `docs/decisions/2026-10-17-a-utc-tolerance-evidence.md` only. A10.1.1, A10.4
and A10.4.2 stay RECOMMENDED and AWAITING AUTHOR RULING.

- **F01 (MEDIUM), ACCEPTED.** Evidence interpretation, the "not censored" sentence and the first conclusion bullet are replaced with Codex's text; the plain UTC evidence bullets are Codex's three; A10.1.1's empirical bullet now carries the same retained-sample, observer-clock and ±7200 s filter qualifications (Codex's evidence wording), and its limits bullet stays.
- **F02 (MEDIUM), ACCEPTED.** Evidence §4 interpretation replaced with Codex's text (559173 of 559718 windows, a diagnostic of observed history only); A10.1.1's "Consensus" and "controls miners" bullets replaced by Codex's single consensus text.
- **F03 (MEDIUM), ACCEPTED.** Evidence case 3 replaced with Codex's text; A10.1.1's "no favourable choice" replaced with Codex's sentence; the α⁶ adaptive-presenter warning is kept.
- **F04 (MEDIUM), ACCEPTED.** The plain custody rule is restated as access limits on the DNS credential, repository key and AWS account, with AWS explained at first use; a one-line lead-in ("The procedure has these contents:") joins it to the existing procedure bullets. The technical custody rule is unchanged.
- **F05 (LOW), ACCEPTED.** Row 24's failure clause replaced with Codex's assumption-versus-bound text; evidence case 2 replaced with Codex's text on forcing failure without attributing miner intent. The necessary-condition wording at evidence §1 is kept.
- **F06 (MEDIUM), ACCEPTED.** Row 32 is GATE | G, with its prerequisites named and no automatic successor project; the plain GATE definition is Codex's; totals are now 15 NARROW-CLAIM, 1 CORRECT, 5 CLARIFY, 10 BROADEN, 4 GATE (rows 32–35); row 33 keeps its stated loss of the added protection.
- **F07 (LOW), ACCEPTED.** Digest replaced by `335249f1…6c0b4c` for `LC_ALL=C bash -c 'cat data/*.csv' | sha256sum` (reproduced by the owner at dataset commit `1bb1c1b`), stated to include the stratum CSVs that the calculation excludes, with a dated correction; §6 gives the same recipe.
- **F08 (LOW), ACCEPTED.** Codex's three U bullets, rollover sentence and glossary entry applied; the remaining unqualified "adds one value, U" sentence is removed. To keep STE-STYLE rule 3, the plain UTC block is split into evidence and output paragraphs and two sentences of the A-UTC block are merged; no meaning changes.
