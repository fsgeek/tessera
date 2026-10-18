# Confirmation: Amendment 10, revision 2 corrections

2026-10-17. **Result: F01–F08 APPLIED. No new HIGH issue found in this confirmation pass.**

This is the requested confirmation against `CODEX-REVIEW.md` and `DISPOSITION.md` in this directory. It is not a new full review or an author ruling. A10.1.1, A10.4 and A10.4.2 remain recommendations awaiting the author's ruling. Confirmation of A10's custody gate does not establish that the separate custody procedure meets it.

## Inputs and scope

Read the current `docs/phase-0-prereg-amendment-10.md`, the eight original findings and their disposition. Read the affected passages of `docs/decisions/2026-10-17-a-utc-tolerance-evidence.md` to confirm the findings that also, or exclusively, apply there. Checked the affected plain-language structure against `docs/plain/STE-STYLE.md`. Current line numbers below refer to these working-tree files; “evidence” means the tolerance evidence file.

Repository HEAD: `7d7f94d797048f96df9a2b129962a5604439f4ae`. A10 SHA-256: `d830bd99a412e13d30152f7d3d8c518ba5bd8435ec67e018269aeebf4d3f772c`. Evidence SHA-256: `9c0af26221166cb5ab3fafeb1ef94ae473c90d411c4c7fc682469b83d4e4406a`.

## Finding-by-finding confirmation

| Finding | Status | Confirmation |
|---|---|---|
| F01 — empirical qualifications | **APPLIED** | A10:74–78 has the three requested plain evidence bullets. A10:272–289 retains the selected-sample, incomplete-window, observer-clock and quality-filter qualifications. Evidence:104–109 has the requested conditional interpretation; :115–117 replaces the “not censored” inference; :163–166 has the qualified conclusion. These passages no longer claim that the observations establish A-UTC. |
| F02 — counterfactual MTP inference | **APPLIED** | A10:281–285 uses the requested consensus text. Evidence:154–159 treats the count as a diagnostic of actual predecessor timestamps and explicitly denies the inference about control outside the six blocks. The fixed-predecessor conditional at evidence:146–148 is consistent with this qualification. |
| F03 — favourable proof presentation | **APPLIED** | A10:270–272 says selection fixes the result within a presentation, while allowing choice among presentations. Evidence:46–50 has the requested replacement. Evidence:43–44 retains the warning that the fixed-experiment α⁶ illustration is not an adaptive-adversary security probability. |
| F04 — access paths, rather than people | **APPLIED** | A10:109–120 explains AWS at first use and gives the requested credential/account access limits and procedure contents. It no longer excludes an authorized person merely because that person also holds operational credentials. The technical gate at :468–479 retains the access-boundary requirement. |
| F05 — assumption failure versus numerical-bound failure | **APPLIED** | Row 24, A10:562, specifies all six lags exceeding 7200 seconds, distinguishes loss of the conditional guarantee from a necessarily false computed bound, and uses the requested text. Evidence:39–41 distinguishes forcing failure from attributing miner intent. Evidence:24–27 retains the necessary-condition and sufficient-assumption distinction. |
| F06 — GATE classification and accounting | **APPLIED** | A10:137–138 gives the requested GATE definition. Row 32 at :570 is GATE/G, names the new timing prerequisites and preserves the separately registered rotation condition. Row 33 at :571 states its conditional loss of protection. The 35 table rows reproduce as 15 NARROW-CLAIM, 1 CORRECT, 5 CLARIFY, 10 BROADEN and 4 GATE; :590–592 lists the matching totals and rows. |
| F07 — concatenated-data digest | **APPLIED** | This finding has no direct A10 replacement. Evidence:70–74 records the full requested `335249f1…6c0b4c` digest, the C-locale command, inclusion of stratum files in the digest, exclusion from the calculation, and a dated correction. Evidence:176–178 repeats the recipe. This confirms the textual correction against F07's previously reproduced value; the external dataset was not downloaded or rehashed in this pass. |
| F08 — adjacent A-UTC qualification | **APPLIED** | A10:61, :82–84, :87–89 and :146 contain the requested U definition, output bullets, rollover sentence and glossary meaning. The unqualified “adds one value, U” sentence is absent. A10:64–70 retains the assumption and its non-check. The distinction between computing a value and establishing its UTC-bound interpretation remains explicit. |

## Three small additions or adjustments recorded in the disposition

1. **Extended technical empirical bullet — checked, no defect.** A10:272–280 carries F01's interpretation into the technical justification. The additional qualifications agree with evidence:104–109 and preserve the existing limitations at A10:286–289. They do not turn the observations into validation of the tolerance.
2. **Procedure lead-in — checked, no defect.** “The procedure has these contents:” at A10:116 connects the access limits to the following procedure bullets. It changes neither authorization nor the custody requirement.
3. **Plain UTC layout and sentence adjustment — checked, no defect.** Evidence and output are separate blocks at A10:72–85. The two clauses of the author's-signature explanation are together in the final assumption bullet at :70. The affected blocks stay within the six-sentence limit and retain the assumption, non-check and conditional claim. The removed standalone “adds one value, U” sentence supplied no unique obligation.

## Limits

No new issue below HIGH was raised. No new HIGH issue was found in the checked corrections. No statistical reproduction, formal model, verifier implementation, custody ceremony or hardware test was run. The separate full custody review is in `docs/reviews/custody/CODEX-REVIEW.md`; its conclusions do not reopen this restricted confirmation or constitute an author ruling on A10.
