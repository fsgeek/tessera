# Codex review of Amendment 9

2026-10-12. Reviewed the unsigned draft in full, including A9.0–A9.8, the opening, open items, all scenario rows and all 25 changed-sentence rows. Checked the sources named in CODEX-BRIEF.md, with additional checks of the cited standing registration, prototype scenarios and Band 0 exit list. This is a review of the proposed registration, not formal discharge, implementation conformance or acceptance of the owner’s decisions on the author’s behalf.

Reviewed Amendment 9 SHA-256: `19fb77e3c1106ccfae9b5cbf0b789072cfe0b4bc504bfeb1e07b6bd2959ffc2f`. Revised encoding SHA-256: `cfc4ad660f36396a7d25376626e2fed63aedf9cad019c4d0b7431be5c7a09584`; revised proof SHA-256: `dd712c96ed6b05ce2253c9c924c6ef777823c965548127000220b1ebff472b31`.

**Recommendation: repair the wording and the change inventory before signing.** The signature-inclusive anchor is a sound repair under the stated commitment and historical-security assumptions. The main unresolved claim is the issuance window: the actual comparisons do not establish that T is inside it, and the sources do not supply the finite backward-skew bound invoked by the post-exit guarantee. No new mechanism is needed if the claim is narrowed to the comparisons actually made.

Author decisions A/B/C are implemented in substance: no submitter attestation, no standing, no wrappers/renewal, no degraded verification, revocation not evaluated, and a human test with zero unsafe accepts and only d2/h as registered false rejects. Q5 and the dates match the derivation/schedule. The owner labels distinguish implementation choices from author rulings; signing ratifies the instrument rather than retroactively turning owner decisions into prior author rulings. Cases i/i′ are explicitly identified as subsequent owner additions. The quoted A/B/C text has added “Decision A/B/C:” prefixes relative to the quotation excerpts in V1-DERIVATION-DRAFT.md:18-25; those excerpts corroborate substance but do not independently establish the amendment’s claim to quote the original message “in full.”

## Numbered findings

1. **HIGH — “T lies inside the issuance window” is stronger than the registered rule. Disposition: WORDING.**

   **Evidence:** docs/phase-0-prereg-amendment-9.md:25-29, 101-106, 264-266; formal/p8/ENCODING-V1.md:606-620; docs/phase-0-prereg-amendment-2.md:218-224.

   The lower comparison is not-before ≤ declared time, not not-before ≤ T. Let not-before = declared time = 12 October 12:00Z, T = 12 October 11:00Z, and the designated confirmation timestamp = 12:00Z. Both issuance-window comparisons and all three temporal conjuncts hold at ε = 24 h, while T is outside the window. Non-monotonic/inexact chain time is expressly permitted. A9 also makes not-before optional, so there need not be a lower issuance boundary at all.

   **Recommendation:** replace “T lies inside” everywhere with “the declared issue time is not earlier than the optional not-before, and the verified chain-time T is not later than not-after.” Describe the opening window the same way. This preserves D-17 and the owner’s no-margin decision. Adding a new T lower-bound check would be a different mechanism/decision and is unnecessary for the narrowed notary claim.

2. **HIGH — Guarantee 2 invokes an A2.1 skew bound that is not registered; 96 h is an operating margin, not a proved real-time deadline. Disposition: WORDING.**

   **Evidence:** docs/phase-0-prereg-amendment-9.md:268-269, 277, 289-292; docs/phase-0-prereg-amendment-2.md:113-124, 190-196; docs/phase-0-prereg-amendment-1.md:173-184; formal/p8/ENCODING-V1.md:638-649.

   A2.1 explicitly says consensus supplies no finite bound on B − C and separates observation delay, clock error and backward timestamp skew. Neither ε = 24 h nor S = 24 h is a universal bound on how far true inclusion time can exceed a header timestamp. The predicate constrains chain timestamps against a declared time; it does not authenticate the thief’s declared time against UTC. Thus “no receipt passes with T > not-after” follows directly, but “no mint passes after true not-after plus the A2.1 skew bound” does not follow from these sources. ENCODING-V1 repeats the same unsupported inference, so agreement between the two documents is not independent evidence.

   The 96 h stop is larger than δ = 72 h, correcting the earlier 48 h choice. But δ already includes timestamp skew in A1, and is a declared-time-to-chain-time tolerance, not “the longest registered gap from signing to anchor” in wall time. Adding 24 h is an owner-selected operational reserve. It guarantees neither completion nor shipping by retirement; the retained no-ship/reissue rule supplies the safe failure behavior.

   **Recommendation:** state guarantee 2 solely in chain time: even possession of every slot key cannot make a receipt pass with verified T after its authenticated not-after, under continuing anchor/history and authority assumptions. State separately that translating this into a finite UTC cutoff requires an additional explicit backward-skew assumption that V1 does not establish. Retain the 96 h operating choice but remove its purported derivation as a hard signing-to-anchor bound. Amend the matching ENCODING-V1 rationale when the owner disposes this finding; this review does not edit it.

3. **HIGH — A9.7 is not a complete inventory of effective changes. Disposition: WORDING.**

   **Evidence:** docs/phase-0-prereg-amendment-9.md:8-9, 173-179, 191-196, 300-343, compared with the sources below.

   The broad profile exception makes several intended changes understandable, but the promise that every changed registered sentence is listed is false. Add the omitted sentences or explicitly map duplicate formulations to their existing replacement rows:

   - **The same independence claim outside row 15:** docs/phase-0-prereg.md:304-305 says the signatures’ validity “does not share a failure domain.” That is incompatible with the classical fallback’s shared P-256 failure (A9:294-296). Corresponding spec formulations include docs/implementation-spec.md:226 and :604-610. Extend row 15 to the additional registered original sentence; record spec consequences without pretending that its restatements are new author rulings.
   - **Public repository publication:** docs/phase-0-prereg-amendment-1.md:434-438 requires “the public git commit publishing the same fingerprints”; docs/phase-0-prereg.md:300-302 also says public repositories. C4 now expressly does not establish public publication (A9:114). State whether public publication remains an issuer duty whose occurrence the verifier does not prove, or is removed for V1. The current opening’s “two public channels” (A9:27) must follow that disposition.
   - **P7’s wrapper-half discharge/vector:** docs/phase-0-prereg-amendment-6.md:43-57 explicitly assigns the control/companions and H1a vector. A9:195 postpones them, but no A9.7 row names the A6 sentence. Row 13’s integrated-lifecycle model is a different obligation.
   - **The A8.4 model query:** docs/phase-0-prereg-amendment-8.md:95-98 registers the new query and its batch. A9:191 moves it; row 16 cites only the separate specification edits at A8:100-106. Add the query itself.
   - **Waived-evidence observation record:** docs/phase-0-prereg-amendment-5.md:145-154 registers both the observation and the H1a record format. A9:196 moves “A5.3 record,” but no changed-sentence row identifies that source. The A1 waiver lattice in A9.3 is also absent from A9.7 (A1:301-327).
   - **Phase 1a opening sentence:** docs/phase-0-prereg.md:730-732 says “Only then does Phase 1a begin,” with an explicit signed opening commit. Row 2 stops at :724. Extend it to say which prerequisite changes and whether the signed opening act remains; A9 preserves it only implicitly through the schedule.
   - **The canonical-payload reading:** docs/phase-0-prereg-amendment-7.md:33-39 incorporates the original precision rule and says signatures and anchors commit to the signed frame. Rows 22–24 change those readings but do not name their later registered restatement.

   E10’s extraction timing and the exit-status reading also change in effect: formal/BAND0-EXIT.md:69-70, 96-97; docs/implementation-spec.md:2197-2198. These are explicitly clerk readings rather than new registered theorem statements. Include them in a separate process-reading inventory, as the derivation itself acknowledged at docs/V1-DERIVATION-DRAFT.md:212-216. Do not inflate the count of registered changes with proposals. Recompute the summary after completing the inventory.

4. **MEDIUM — The immutable encoding reference conflicts with the registered future hybrid branch update. Disposition: WORDING.**

   **Evidence:** docs/phase-0-prereg-amendment-9.md:120, 250-262, 357; formal/p8/ENCODING-V1.md:424-426, 464-476; formal/p8/PROOF.md:514-516.

   The profile incorporates ENCODING-V1 “at the signing commit,” but that version has no assigned PQ pair id and neither codec implements rule R. A9 then requires the owner to register the pair and edit §5.2 before the later freeze, without another amendment. Both branches can be preregistered, but those later bytes are not the encoding bytes at the signing commit. Taken literally, the hybrid either stays unknown/UNVERIFIABLE or relies on an unincorporated later document.

   **Recommendation:** explicitly authorize a dated, bounded branch-registration supplement before freeze, naming its exact encoding/spec hash and the completed pass-condition evidence. Clarify that the signing-commit baseline plus that supplement governs the selected branch. Keep the fallback automatic if any condition misses 21 Oct. This records the already intended update rather than adding another author approval gate.

5. **MEDIUM — The hybrid pass condition must cover manifest possession proofs and the full selected byte profile. Disposition: WORDING.**

   **Evidence:** docs/phase-0-prereg-amendment-9.md:254-257; formal/p8/ENCODING-V1.md:343-354, 424-426; formal/p8/PROOF.md:105-109, 514-516; prototype/spike-pq/REPORT.md:8-17.

   A9 correctly chooses one pair identifier and requires real KMS/hardware signatures. However, E§4 still specifies each manifest possession proof as an OpenPGP signature, and PROOF’s key-use assumption still says each V1 slot signs only OpenPGP type-0x00 documents. That does not describe the raw ML-DSA KMS slot. The reported PQ spike used approximate JCS, no real KMS, and a bare SLH-DSA portable slot, not this selected pair. It is useful feasibility evidence, not evidence that the hybrid V1 profile is complete.

   **Recommendation:** make “mixed-format pairing passes” explicitly include both attestation and manifest-possession verification, slot key/fingerprint encodings, key-use assumptions appropriate to each slot, and golden/rejection vectors with an agreement run for the registered rule R. These are obligations of the intended hybrid, not a requirement to change the fallback or build a new mechanism. Do not cite the present spike as satisfaction of that condition.

6. **MEDIUM — The later-verifier contract omits the fixed-input condition. Disposition: WORDING.**

   **Evidence:** docs/phase-0-prereg-amendment-9.md:116, 124-126, 219-222; docs/phase-0-prereg-amendment-5.md:81-89; docs/phase-0-prereg-amendment-3.md:503-508; docs/V1-DERIVATION-DRAFT.md:244.

   “A later verifier given a V1 bundle returns the same verdict” is too broad. The bundle alone does not fix policy, supported algorithms or trust configuration. Adding pins can turn HEADERS_NOT_COVERED into a performable check; a policy prohibiting an algorithm can change its result. Both are consistent with the pure-function contract. The derivation explicitly qualified future inner-assessment preservation by “identical declared inputs.” Missing status capture is only one possible source of unperformability.

   **Recommendation:** preserve the stable assessment under the same governing V1 specification, policy, trust configuration and other declared inputs. Define the stable field set in the profile. Scope the missing-capture negative control to an otherwise valid, fully performable bundle, where missing capture is the sole difference. Place that named control among C7’s assigned build evidence; it is required in A9.4 but not named in A9.2’s gate list. A separately stronger assessment may change with later evidence.

7. **MEDIUM — A PQ receipt slot does not eliminate quantum historical-security cutoffs for the entire receipt. Disposition: WORDING.**

   **Evidence:** docs/phase-0-prereg-amendment-9.md:214-217, 250-257, 283-285; docs/reviews/anchor-signatures/DISPOSITION.md:14; formal/p8/PROOF.md:93-103; docs/phase-0-prereg-amendment-3.md:473-482.

   The amendment faithfully repeats the owner disposition, but “A PQ leg removes the need for a quantum cutoff” has excessive scope. It can remove dependence on P-256’s security for an attack requiring fabrication of both attestation slots, provided ML-DSA remains secure. It does not establish historically trustworthy authority assertions or retire the classical gpg, repository/DNSSEC and SHA-1 dependency assumptions. Nor is ML-DSA guaranteed immune to every future quantum attack. A9’s per-algorithm/per-key statement and NOT_EVALUATED field are otherwise appropriate.

   **Recommendation:** say that a surviving PQ attestation slot prevents a P-256 break alone from supplying every required attestation signature; historical authority, per-key custody and continuing commitment/history security remain assumptions. Keep historical security NOT_EVALUATED and the portable-PQ production obligation. Do not add historical-security policy evaluation to V1.

8. **MEDIUM — “Repository key used only for rotations” contradicts the exit statement it must sign. Disposition: WORDING.**

   **Evidence:** docs/phase-0-prereg-amendment-9.md:270-275; formal/p8/ENCODING-V1.md:659-660.

   The offline repository root is restricted to rotations, but the exit procedure requires a signed, anchored end-of-issuance statement, which is not a rotation. The signer's identity is not otherwise specified. Also “destroy the keys (KMS scheduled deletion)” conflates initiating a deletion workflow with completed destruction.

   **Recommendation:** allow the offline root’s explicitly named key-publication/rotation and end-of-issuance acts. Distinguish disabling issuance and scheduling deletion from confirmed destruction, and record completion as an operational fact. Keep the end statement outside the V1 verifier; no new status lookup or refusal/standing mechanism is needed.

9. **LOW — Several table quotations and line ranges are imprecise. Disposition: WORDING.**

   **Evidence:** docs/phase-0-prereg-amendment-9.md:307-331 and the source audit below.

   Row 4’s quoted heading is at prereg:589, outside :590-617. Row 5’s “for each attack family” starts at :203, outside its one-line citation :205. Row 9’s quoted “Revocation is time-relative” is at :537, outside :539-546. Row 24’s quoted “a framed envelope” completes at A1:259, outside :255-258. Row 15 says “fail for uncorrelated reasons,” whereas prereg:294 says “They fail for *uncorrelated* reasons”; the intended paraphrase is faithful but should not be presented as exact source words. Row 12’s local-state excerpt ends before publication = PENDING at A3:581, though its second citation does cover the full invariant.

   **Recommendation:** extend those ranges, mark paraphrases as paraphrases, and distinguish source citation from replacement pointer. Confirm the full-message quotation against the original author message if available; the supplied derivation supports the decisions but only quotes excerpts. These are mechanical repairs, not new routed decisions.

## Complete changed-sentence audit

“Matches” means the cited passage contains the stated substance; it does not certify that the inventory is complete. The replacement is interpreted together with A9’s body. Findings 3 and 9 identify missing formulations and exact-quote defects.

| Row | Source check and replacement assessment |
|---|---|
| 1 | prereg:102-107 matches the abbreviated quotation. Code/gate/H1b replacements are explicit; preserve instrument-versus-service distinction. |
| 2 | prereg:714-724 matches. V1 exception is explicit; include :730-732 and clarify the signed opening act (finding 3). |
| 3 | A3:220-231 matches. This is a replacement exit condition, not capstone discharge. Correct-form greens alone do not supply producer/consumer severing evidence; A9:175 correctly retains that debt. |
| 4 | prereg:590-617 contains the done criteria and start of kill criterion, but heading is :589. Later product distinction is explicit. |
| 5 | prereg:205 contains the degradation clause; expand to :203-208. Strict attack families remain and degradation moves. |
| 6 | prereg:210-224 matches H1b and its clock. Withdrawn-for-V1, not falsified, is consistently stated. |
| 7 | A1:199-214 matches original P6. Formula uses abbreviated `declared`; A9.4 correctly removes both effective-revocation conditions while retaining authority checks. |
| 8 | A4:111-123 matches the “after both” repair. A9.4 correctly uses max(anchor, declared); not merely revocation after anchor. |
| 9 | prereg:539-546 contains the invalidity consequence; heading is :537. Same weakening as rows 7/8. |
| 10 | FIRST-LINK-SPIKE:50-56 matches the before-exit modeling requirement. Standing capability deferral is explicit. |
| 11 | A3:531-557 matches. Constant ABSENT with a profile-specific reason preserves orthogonality; missing standing still confers none. This is non-offering, not an erasure of the invariant. |
| 12 | A3:572-580 and :816-828 substantiate decomposition/companions; include :581. Portable machinery moves; bounded refusal, terminal latch and N remain V1 operations. |
| 13 | A3:783-806 matches; explicitly was not a Band 0 exit obligation. Its pre-H1a trigger moves, and profile freeze is distinguished from crypto-core freeze. |
| 14 | A3:273-278 matches renewal-before-unreliability. V1 excludes renewal and retains custody/dependency residuals, without claiming unconditional continuity. |
| 15 | prereg:292-299 matches substance, with the quote repair in finding 9. C3 narrows independence honestly; :304-305 also needs listing. |
| 16 | A8:100-106 matches spec edits. Query at :95-98 is a separate omitted change (finding 3). |
| 17 | scenarios.py:72-133 matches historical expectations for a–h, including c/degraded/e/standing. New V1 predictions deliberately differ; e′ and i/i′ are additions, not old results. |
| 18 | A3:371-378 matches both demonstrations. Dead-service remains; clean-room reconstruction is explicitly unestablished and deferred. |
| 19 | implementation-spec:651-656 and standing-probe/AMENDMENTS-2026-08-31:159-206 match the author-adopted successor-slot registration and chosen payload location. Capability and format-freeze trigger move. |
| 20 | prereg:564-572 matches recurring review-recency invariant. Explicitly not offered in V1, not falsely claimed satisfied. |
| 21 | A3:435-451 matches custodial schema/clock-role ratification. Capability-trigger replacement is explicit. |
| 22 | prereg:501-505 matches original exact-double rule and string encoding. Value-preserving replacement is explicit; other rejection conditions remain. |
| 23 | A1:268-270 matches exact-double rejection. Same replacement, rather than quietly changing the registered domain. |
| 24 | A1:255-258 starts the quote; include :259-264. Direct frame commitment is retained inside A_sig, with exact signatures added and no old-layout fallback. |
| 25 | A3:480-482 matches deployment-profile/later-amendment deferral. Conditional hybrid adoption fits that route and leaves the production PQ gate standing; supplement coherence needs finding 4. |

The stated kind counts match the current 25-row table: ten G, six C (row 19 is both), one H, three W rows for one P6 weakening, one narrowed claim, four R/K replacement rows, and one T. Their arithmetic is not evidence that all changed sentences were enumerated.

## Section, claim and evidence coverage

- **Opening / A9.0:** claim, adversary and boundaries are in ordinary language and in the requested order. Correct the issuance-window claim (1), public-channel wording (3) and quantum-cutoff scope (7). Owner and author provenance is substantively separated; earlier E18 convention is carried in, not a fresh parameter ruling.
- **A9.1 / C1–C7:** C1 agrees with revised A_sig/Lemma 7; C2 is existential under honest historical key use, not submitter identity or unique shipment; C3 requires both slots without independent control; C4 requires both authentic authority paths and possession; C5 preserves presentation-sensitive T and the three conjuncts at k = 6; C6 retains external trust configuration and pin-coverage limits; C7 is explicitly a future human acceptance criterion. These are conditional target claims, not established implementation results. No new scope promise is needed.
- **Scenario rows:** a/g, b, c, d1/d2/d3, e/e′, f, h and i/i′ were all checked. INVALID precedence in d3 is coherent for a V1-dispatched missing-signature case despite unavailable authority evidence. e/e′ deliberately do not evaluate revocation. i/i′ distinguish timestamped contract bytes from the relying party’s party-signature check. The initial “strict request in every row” should allow d1’s explicitly described preliminary degraded request. A9.4’s missing-capture test and the larger E10 suite remain separate from comprehension testing.
- **A9.2:** the bounded gate, per-claim code rule and instrument exception match the derivation; `checked` is not `discharged`. The closure rule admits assigned-evidence gaps as well as concrete attacks, which is essential. Apply it to the gaps above without expanding the finish line. For implementation, name each claim’s exit prerequisites: a checked P1 alone is not a checked C1 while P8 is open. E9’s accept/reject outcome must be recorded before the signed V1 exit; the derivation schedules that read on 28 Oct. The rule does not authorize shipping on partial gates.
- **A9.3:** standing, LTV, succession, portable refusal, lifecycle/wrapping, degraded verification, channel diversity and portable PQ are retained as named future capabilities. V2 separation/identity/renewal/revocation are not release commitments. Inventory omissions are finding 3, not reasons to implement these capabilities now.
- **A9.4:** both P6 conditions are honestly weakened; monotonic key lifecycle remains. NOT_EVALUATED does not prove historical safety or non-repudiation. Stable results require fixed declared inputs (6).
- **A9.5:** exact signature inclusion, sign–verify–freeze–stamp, one composite receipt anchor, exact committed-byte verification and signed-commit-id anchoring match revised ENCODING-V1/PROOF. No frame-only fallback is allowed. The existential KSK rule correctly avoids treating a published nonsigning KSK as a failure; validity still requires the other DNSSEC chain/time checks. The spike’s re-capture is real rollover evidence, but unstamped and not a complete V1 receipt.
- **A9.6:** guarantee 1 is appropriately conditional and does not establish historical honesty, issuer-obtained stamping or uniqueness. Interpret “by T” with C5’s chain-time uncertainty, not as exact UTC. Guarantee 2 needs finding 2. Hybrid/fallback, custody and exit are explicit owner choices; findings 4/5/8 reconcile their detail without adding a new service.
- **A9.7:** every row was checked above; exact ranges and omissions need repair. “Named and not changed” is coherent when scoped to the later product/general profile, not an assertion that unresolved H0 has been discharged for V1.
- **A9.8 / open items:** the value-preserving rule is supported by E§1.2, PROOF Lemmas 2/3 and the vectors. Q4, the conditional pair id and token selection remain open; the amendment does not invent answers.

## Verification performed and limits

Ran `python3 -B formal/p8/vectors/check.py` against the existing artifacts: exit 0; **71/71 golden round-trips, 170/170 rejections with matching reason codes, 5/5 valid-but-unanchored-signature negative controls**. These independently exercised the revised signature-inclusive codec and window comparison evidence. No vector files were regenerated. The hybrid/raw rule R is not covered by that result.

Also ran `PYTHONDONTWRITEBYTECODE=1 uv run --no-project --with rfc8785==0.1.4 python -B formal/p8/vectors/fuzz.py`: exit 0, **60,000 cases, zero disagreements**. Its 20,000 composite-anchor cases included 3,858 accepted tuples and the reported signature/framing rejection categories. Agreement remains bounded evidence, not independence of authorship or a proof of cryptographic security.

The prose proof distinguishes codec injectivity, SHA-256 binding, signature unforgeability and temporal composition; this review does not collapse those into discharge. No new ProVerif/TLA+ run, AWS/hardware integration, human relying-party test or dead-service demonstration was performed. The classical spike lacked the key TXT publication and git channel; the PQ spike was a throwaway feasibility experiment. Their green portions do not establish C1–C7 end to end. The remaining registered freeze/build tests must supply that evidence.
