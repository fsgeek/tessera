# Owner disposition: Amendment 9 reviews (2026-10-12)

Owner: Claude Opus 5.5. Sources: CODEX-REVIEW.md (9 findings), SKEPTIC.md (23 findings).

## Codex
All nine are accepted as WORDING, with the reviewer's proposed text unless an owner call below overrides it.
Finding 3: the A9.7 inventory is completed from Codex's "Complete changed-sentence audit" section.

## Skeptic: owner calls
| # | Disposition |
|---|---|
| 1 | WORDING, adopted. The token stops key export, not misuse. Whoever controls the queue (an AWS takeover) has signing capability for both slots. "Signing capability for every required slot" is used throughout. MECHANISM, small: the token-side signer refuses a declared time outside ε of its own clock. That limits a takeover to current-time minting. Separation of control stays a V2 driver. |
| 2, 10, 12 | MECHANISM. **A single issuance window for V1 of at most 90 days.** The registered invariant is `issuance-not-after − issuance-not-before ≤ 90 days`, so not-before becomes mandatory. No overlap. Before the window ends, either a rotation mechanism is registered (multiple records or per-key owner names) or issuance stops. Operating numbers (the retirement margin, a 30-day cadence) leave the instrument and go to the operations runbook. The retirement rule stays only as an invariant: an attempt whose T would exceed not-after is not shipped. |
| 3 | MECHANISM plus WORDING, adopted. A single gate: no V1 issuer or verifier code before the whole 30 Oct exit. Instrument code is defined by location (`prototype/`, `formal/spike*/`), and service code never imports it. Row 1 is relabelled W (weakening), with the reason: P8 rests on a prose proof plus vectors, time-boxed, not a machine-checked proof. The author commits `prototype/spike*`. |
| 4 | REJECT the cut; ADOPT the cut order (finding 18). The hybrid stays conditional. Its provenance is recorded as the author's stated preference (2026-10-12: *"I think we should build our V1 with a PQ implementation"*), not a claim requirement. It is the first item cut if 30 Oct slips. |
| 5 | WORDING: a published window cannot be shortened; detection changes no V1 verdict. |
| 6 | MECHANISM, adopted: the fallback is defined without a token type ("`gpg` slot on author-controlled hardware, key generated non-exportable"). The YubiKey is named in the runbook. |
| 7, 8, 9 | WORDING, adopted. 7: cite the offline pre-spike. 8: guarantee 2 is the C4 window rule. 9: an ML-DSA-65 cutoff and the classical slot remain. |
| 11 | OMIT from the instrument; it moves to the operations runbook. |
| 13, 14 | WORDING, adopted: "given the same trust configuration"; V2 items are "candidate capabilities, no obligation". |
| 15 | OMIT the hardware specifics from the instrument. Root backup goes in the runbook (ceremony before first use). |
| 16 | WORDING, adopted: n = 1 human tester ("Aki Doe"), the independence criteria from docs/V1-TESTER-BRIEF.md, and evidence stated as one tester, not a population. |
| 17 | WORDING, adopted. For OWNER items, the author's signature means "the author has read and does not object". It does not convert them into author rulings. |
| 18 | MECHANISM, adopted: the cut order is registered as PQ hybrid → (nothing else; the anchor, root-KSK rule and stamp target are required). |
| 19–23 | WORDING, adopted as proposed. |

Superseded owner statements from earlier on 2026-10-12: 30-day overlapping windows; the 48 h and then 96 h retirement margin as a registered parameter; the exit procedure in the instrument.
