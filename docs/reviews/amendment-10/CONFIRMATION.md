# Confirmation — Amendment 10 revisions

2026-10-16. **Result: F01–F08 APPLIED.** The added stage-3 rule is consistent with V1-PROFILE and changes no registered verdict. The nineteen-row change table matches the amendment body and A9 at its signing snapshot. No new HIGH issue found.

Confirmation pass only against `CODEX-REVIEW.md`, `DISPOSITION.md`, and the revised `docs/phase-0-prereg-amendment-10.md`. Only this confirmation file was written. A10 remains **PROPOSED**; A10.4 and rows 15–16 remain **AWAITING AUTHOR RULING**. Confirmation of the recommended text does not supply that ruling or a signing act.

## Findings

Locations below refer to the inspected revised A10; row numbers are its current A10.7 numbers, not the original draft's numbers.

| Finding | Status | Confirmation |
|---|---|---|
| F01 — Publication does not guarantee visibility | APPLIED | A10:134–168 has the revised heading and conditional-publication boundary. It identifies both-channel capture, permits captor-created receipts under substituted keys, preserves publication as an issuer duty, and explicitly disclaims guaranteed publication, capture detection and public receipt visibility. The summary (:29–35) and row 16 agree. The author's quotation is retained expressly as motivation, not evidence (:146–151). |
| F02 — Honest material before or after disclosure | APPLIED | The recommended clause (:155–159) protects honestly signed frames before or after credential disclosure while the original service keys and signing capability remain uncompromised. Options (a)–(d) distinguish this from a deliberate pre-capture restriction and from unsupported protection for arbitrary captor-created receipts (:174–179). The summary and row 15 agree. The backdating exclusion and guarantee 2's authority-capture proviso remain (:170–172). The conditional V2 obligation (:181–182) adds no V1 rule. |
| F03 — Narrowing labels and counts | APPLIED | The CORRECT definition excludes claim reduction (:45–46). A10.3 and rows 13–14 are NARROW-CLAIM/R, as is success-definition row 2. The equality-case narrowing and unchanged model/assumption are explicit (:125–131). Totals are correctly recalculated at :267–269. |
| F04 — Complete clock correction inventory | APPLIED | Rows 5–9 contain the five requested source registrations and replacements; row 9 covers all three `before T` occurrences. Row 2 supplies an explicit replacement. A10.1 makes these qualifications operative (:70–95), preserves scenario i's party-signature duty and `historical_security: NOT_EVALUATED`, and leaves mapping verdicts, fixtures and case membership unchanged. The inherited A1.6 wording is expressly qualified for V1 (:93–95, :261–264). |
| F05 — Precedence and independent checks | APPLIED | The paragraph before the stages (:192–196) preserves dependencies, dispatch, reason precedence and independently performable checks; UNVERIFIABLE is not an early return. Stage 2 retains merkle contradiction as INVALID. Stage 4, the cases and row 18 all preserve A4.2's failed-check precedence. Stage 3's additional sentence is consistent with the profile; see below. |
| F06 — Assembled C5 claim | APPLIED | A10:83–91 gives one assembled C5 claim cell that distinguishes the selected block, its header time T and the qualifying attestation. Rows 4 and 17 both point to that same replacement, avoiding conflicting overlapping edits. Existing non-claims remain, with the reorganization residual separately amended by row 14. |
| F07 — Arithmetic-witness evidence scope | APPLIED | A10:108–110 limits the witnesses to the two window comparisons and three A2 temporal comparisons, and explicitly says they are neither executed receipt vectors nor evidence of honest shipment. |
| F08 — Plain-summary corrections | APPLIED | The opening is replaced (:16–17); Bitcoin, chain time and k are explained (:19–20); DNS is expanded at first use and the required owner is stated in code formatting (:38–39). The summary uses “service”, avoids “git” and the unexplained parameter/vector inventory, visibly attributes A02's source wording, and follows F01/F02's corrected capture scope. The corrected kinds are defined at :41–46. No style-guide edit is needed for these fixes. |

## Added stage-3 rule

**Consistent; no verdict change.** A10:208–209 says: “A failed check at h* never moves selection to a higher height.” V1-PROFILE §7.1 fixes h* as the lowest qualifying height (:770–802), selects it before the receipt txid check, and expressly forbids switching to a higher height to find a matching txid (:807–815). The same paragraph applies the transaction-shape/merkle-suffix subset at the snapshot and git proofs' own selected heights. Section 15.2 states the general path rule explicitly: “a failing path never moves selection to a higher height” (:1309–1312). Section 7.2 independently checks every supplied header against pins and every supplied consecutive-height link (:820–834).

The addition preserves the distinction between qualification and subsequent checks. An incomplete lower branch can be nonqualifying, allowing selection of a higher qualifying branch. Once h* is selected, a later time, transaction/path, or other required-check failure does not demote that anchor and trigger reselection. Contradicted branches and supplied-header failures retain their independent consequences; they cannot be hidden by selecting another anchor.

It also preserves **same-height aggregation**: a failing individual path does not defeat another satisfying qualifying path at exactly h*. The sentence prohibits moving to a higher height; it does not prohibit trying another path at the selected height. Thus, if qualifying receipt attestations exist at heights 100 and 200 but the txid subset can be satisfied only at 200, the receipt still fails `ANCHOR_TXID_MISMATCH` at 100. If another qualifying path at 100 satisfies that subset, the subset passes. Snapshot/git shape failures are similarly aggregated at their own h*, with `OTS_TX_SHAPE` if every qualifying path there fails. These are consequences of the existing profile, not newly executed vectors.

The verdict/reason contract remains the profile's §15.7 (:1461–1465, :1497–1518): the first failed required check takes precedence over unperformability; existing dependencies and reason ordering remain. The addition introduces no new failure condition, reason code or verdict, and does not change any F01–F08 disposition above.

## Nineteen-row reconciliation

**PASS.** Checked every row against the body and `git show 2ad3489:docs/phase-0-prereg-amendment-9.md`. Every quoted source span matches its cited range after whitespace normalization. Row 16 is correctly identified as an insertion into the boundaries, not a quotation of a missing sentence. Row 9's source range contains exactly three `before T` occurrences.

| Row | A9 source at `2ad3489` | Body correspondence | Result |
|---|---|---|---|
| 1 | :36–37 | A10.1, opening clock claim | PASS |
| 2 | :114 | A10.1, explicit success-definition qualification | PASS |
| 3 | :133 | A10.1, signed-frame clock claim | PASS |
| 4 | :144, C5 claim | A10.1, assembled C5 cell | PASS |
| 5 | :177 | A10.1, scenario a/g qualification | PASS |
| 6 | :186 | A10.1, scenario i qualification; party-signature duty retained | PASS |
| 7 | :294–295 | A10.1, issue-order qualification | PASS |
| 8 | :433 | A10.1, guarantee 1 inclusion-block wording | PASS |
| 9 | :436–439 | A10.1, three historical-condition qualifications | PASS |
| 10 | :36 | A10.2, stated window and unchanged two comparisons | PASS |
| 11 | :441 | A10.2, narrower guarantee 2 heading; body/proviso retained | PASS |
| 12 | :407 | A10.2, window name retained with its limited meaning | PASS |
| 13 | :49–50 | A10.3, residual includes equality | PASS |
| 14 | :144, C5 residual | A10.3, same equality boundary | PASS |
| 15 | :41–42 | A10.4, honest-material adversary clause; ruling pending | PASS |
| 16 | :45–52, insertion | A10.4, new-receipt limitation and conditional publication; ruling pending | PASS |
| 17 | :144, C5 selection wording | Same assembled C5 replacement as row 4; A10.5 stages | PASS |
| 18 | :145, C6 | A10.5, qualification, pin coverage and A4.2 precedence | PASS |
| 19 | :143, C4 | A10.6, fixed prefixed owner and label-sequence comparison | PASS |

The table has nineteen sequentially numbered data rows, each with six cells. Its kinds and A9.7 letters agree: **15 NARROW-CLAIM/R** (1–11, 13–16), **1 CORRECT/K** (19), **3 CLARIFY/K** (12, 17, 18). The body section references, assembled C5 cross-references, conditional status of rows 15–16 and closing totals match. Row 19 also agrees with signing-snapshot ENCODING-V1:551–553 and :623–624; it changes no encoding rule.

## Evidence and limits

Repository HEAD during inspection: `44f921e2df2ea963eca7e32ab749349cc29c08ff`. A9 signing snapshot: `2ad34890359c446efaebcb116388b8e9ffbf6428`. Workspace A9 is byte-identical to that snapshot. Profile §7.1–§7.2 is also byte-identical between that snapshot and the inspected workspace, so the selection conclusion does not rely on the workspace's unrelated profile changes.

| Inspected input | SHA-256 |
|---|---|
| Revised A10 | `37257b9b5471bf7302e2eeeb2c64736a45980da765dcda56c3fd232608a0bdd5` |
| Original Codex review | `bc9d055499a4086b25684618baa25a3c2ea34fcce67fcb71d2d670bdfb35a146` |
| Disposition | `c900bed764345659dc0d1eb456ce5a902ff0e46a3ed8f5f1e88f980e20dce9be` |
| A9, snapshot and workspace | `ff09f9b1ff6bb717bcca2c2f803eb8674f4beb2d28e88d5718320fe9b63c9f05` |

Source-span matching, row structure/counts, kind letters and snapshot equality were checked mechanically; finding application, body/table correspondence and selection semantics were checked manually. This is textual confirmation only. No model, verifier implementation, cryptographic guarantee, publication enforcement or human test was newly run or discharged, and no new design review was undertaken beyond checking for HIGH issues.
