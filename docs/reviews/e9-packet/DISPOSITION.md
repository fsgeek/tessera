# Disposition of the E9 read-packet review (2026-10-21)

Owner: Claude Opus 5.5. Reviewer: Codex ([CODEX-REVIEW.md](CODEX-REVIEW.md)). E9-01 to E9-14: 5 HIGH, 8 MEDIUM,
1 LOW. All accepted. Codex's text was used unless noted below. Edited: `docs/E9-READ-PACKET.md` only (and this file).

## Owner decisions applied

- **Listing cut (E9-01).** The cut is not authorized by the registered text: A9.2's cut order applies only "if the
  30 Oct exit slips" ([correction](../../decisions/2026-10-19-listing-cut.md)). Row 2 is the author's ruling, KEEP
  or CUT, with the owner's recommendation (CUT, on merits). This replaces Codex's ACCEPT/REJECT-the-cut framing.
  KEEP states the owner's work (A10.4.1 in profile and verifier, conformance cases, freeze reassembly) and an exit
  about 29–30 Oct with no spare time, stated as a prediction. This replaces Codex's "four agent-days" estimate.
- **gpgv (E9-05).** The owner pins upstream GnuPG 2.4.4, as `formal/dependency-sources/dependency-manifest.json`
  already does. `docs/V1-PROFILE.md` is not edited now. The packet says the choice is entered in the profile and the
  freeze is reassembled once, after the author's rulings. It is listed as owner work, not an author row.

## Findings

| Finding | Sev. | Disposition |
|---|---|---|
| E9-01 | HIGH | Applied with the owner's framing above. R2 is `service-key listing (AUTHOR RULING): KEEP / CUT`. Opening, rows 1, 16, 19 and 22, the contract's capture row and the freeze objects are marked as dependent. The irreversible consequence is stated. |
| E9-02 | HIGH | Applied verbatim, beside the claim. The capture condition refers to row 2 instead of "the proposed listing cut". |
| E9-03 | HIGH | Applied verbatim. |
| E9-04 | HIGH | Applied to rows 7–14 and 17–20 in Codex's pattern (Claim; Attacker and limits; Evidence, linked; Question). Each claim is taken from the model's reading aid or results file and is no stronger: S-P1 §2d/§3, S-P2 §1d/§2, S-P3 §1d, P4/P5P6/P5c "The claim" sections, first-link Q3 aid, S-P7 §1d/§2, E6a RESULTS §1, sheet E11 interim capstone row, profile §6.4, E18 sign-off. Row 10 states the failure/unperformable/pass precedence and the finite instance. Row 13 separates abstract authority and possession from concrete DNSSEC/git and possession over the actual manifest. Row 11 drops the revocation half (P6), which V1 does not use. |
| E9-05 | HIGH | Applied verbatim to the opening. Next steps rewritten to the same effect and list the remaining owner work. |
| E9-06 | MEDIUM | Applied verbatim in row 5a. |
| E9-07 | MEDIUM | Applied verbatim as row 17's claim and limits. |
| E9-08 | MEDIUM | Applied. The owner made the split Codex asked for now. Statements that exist and need links: the bridge and k = 6 runs (in the P5c and P5P6 aids), E6a (RESULTS §1). Statements that do not exist: first-link Q1, P8's adversary, the full capstone statement. The note on signature/time composition is included. |
| E9-09 | MEDIUM | Applied verbatim, with links to the report and the disposition. |
| E9-10 | MEDIUM | Applied verbatim. |
| E9-11 | MEDIUM | Applied as a **linked mandatory range** (`V1-RELYING-PARTY.md` lines 26–133, about 1,170 words, 8 minutes), not reproduced. Reproducing it would add about 1,200 words to a packet already near its limit. The page's capture paragraph (lines 98–105) is marked as describing CUT. The page itself is not edited (out of scope). |
| E9-12 | MEDIUM | Applied. Every row has a clickable evidence line. The `<name>` placeholder is replaced by nine linked dispositions. Row 5a points to profile §15.9. Rows 23–26 link vector entries, inventory, generator, registration record and freeze-record hash. Row 2's file length is corrected to 52 lines. **Departure:** rows 23–24 link the PROOF.md vector table, not a stored `check.py` output, because none is committed. Codex reran `check.py` (review, last paragraph). |
| E9-13 | MEDIUM | Applied verbatim under the form. The preamble-hash promise is qualified. Row 3's "If you reject, C3 needs INVALID" is removed. |
| E9-14 | LOW | Applied: Codex's M2/M5 text in row 19. "Near the line", "went red", "slack" and "reaches the verdict" are replaced. Row 5 is split into 5a and 5b (form R5a, R5b). Explanations use VALID and CANNOT VERIFY. |

## Owner findings beyond the review

1. **R1 also depends on R2.** The preamble line "An attacker controlling both authority records can issue passing
   receipts…" describes CUT. Under KEEP it no longer describes an authentic release, so R1 returns. The packet says
   this in row 1.
2. **Out-of-scope text that assumes the cut**, to be revised under KEEP: the contract's capture row
   (`docs/V1-CONTRACT.md:72`, "the listing was cut"), `docs/V1-RELYING-PARTY.md:98-105`, and the "Not inputs"
   listing line in `formal/P9-CONTRACT-INSPECTION.md`. Not edited here.
3. **Row 14.** The strict S-P7 variant does not give the attacker an authorized wrapper identity (the honest channel
   vouches only for honest manifests). The row does not say it does.
4. **Row 13.** First-link Q1 has no reading aid. The claim comes from the Q3 aid and the Q1 results table only.

## Check against the contract's capture row

Every "shows / proves / true / rejected / establishes / passes / refuses / protected" in the packet was checked
against `docs/V1-CONTRACT.md` §4. The opening keeps the claim's condition beside it. Both-channel capture is
conditional on R2: under CUT, captor receipts pass (as the contract row says); under KEEP, an authentic release
refuses them. Honest receipts are "protected" only with the keys secret and unmisused (G10). Rows 7, 9 and 13 claim
results with one channel leaked only. Row 18 keeps "capture of both loses unrestricted service-origin assurance".
No remaining sentence says a receipt change is always rejected.

## Length

3,320 words, including 365 words of verbatim preamble and form. The prose is about 2,950 words. The reading time
is about 20 minutes, plus 8 minutes for the row 22 range and 4 minutes for the optional row 2 read.
