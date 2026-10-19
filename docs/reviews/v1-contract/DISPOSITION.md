# Disposition of the Codex review of `docs/V1-CONTRACT.md` (2026-10-19)

Owner: Claude Opus 5.5. Reviewer: Codex (gpt-6.1-sol, reasoning effort high), `CODEX-REVIEW.md`.

All 25 findings accepted and applied, each as WORDING (the contract had overstated or omitted registered text; no
registered sentence changes). Codex's replacement sentences were shortened for the one-page form; the meaning was kept.

| Finding | Severity | Applied where |
|---|---|---|
| VC-01 | HIGH | §2 "Conditions" paragraph |
| VC-02 | HIGH | §2 lead-in (archived listing evidence); §4 "Tessera disappears" |
| VC-03 | HIGH | §4 release-key theft row |
| VC-04 | HIGH | §4 split into "authority not captured" and "both captured" rows; captured channels alone do not prevent acceptance (`AUTH-i-T` expects `VALID_STRICT`) |
| VC-05 | HIGH | G10 rewritten as anti-reattribution, not continued acceptance |
| VC-06 | HIGH | G9: "missing required evidence prevents acceptance"; a valid receipt leaves §3 unestablished |
| VC-07 | HIGH | §5 G5 row: existence before the block is an assumption |
| VC-08 | MEDIUM | G9: no receipt verdict without authenticated trust configuration |
| VC-09 | MEDIUM | New G11 with its authorization and pre-commitment conditions |
| VC-10 | MEDIUM | Listing-cut paragraph after the table |
| VC-11 | MEDIUM | G6 |
| VC-12 | MEDIUM | G9 (standing); §3 "Standing" |
| VC-13 | MEDIUM | §3 "algorithm or a key" |
| VC-14 | MEDIUM | §3 first bullet (replay) |
| VC-15 | MEDIUM | §3 "Any lower time bound or priority" |
| VC-16 | MEDIUM | G7 |
| VC-17 | MEDIUM | G5; §3 "Stability of T and U" |
| VC-18 | MEDIUM | G4 evidence times; §3 DNSSEC bullet |
| VC-19 | MEDIUM | §3 "Visibility" |
| VC-20 | MEDIUM | §6 pass rule and tester criteria |
| VC-21 | MEDIUM | §5 G8 row |
| VC-22 | MEDIUM | §5 G7 row |
| VC-23 | MEDIUM | §5 G4 row |
| VC-24 | MEDIUM | §5 G10 row |
| VC-25 | LOW | §5 G1, G3, G9 rows |

**Owner note.** VC-04 is the finding that matters most outside this page. The one-page draft said an attacker
using its own keys is rejected. The registered text and the conformance suite (`AUTH-i-T`) say a captor of both
channels gets `VALID_STRICT` without the listing. The draft got that wrong because the plain-language rule
was easier to state than the registered one. That is the failure this page exists to prevent, so it is recorded
here.
