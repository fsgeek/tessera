Two HIGH findings prevent treating the relying-party draft as ready. No files were edited. Profile citations below refer to `8ea8bfa`; this review does not establish the 4 December comprehension criterion.

1. **XP-01 — HIGH — The stated conditions do not support all the service-origin claims.**  
   **Location:** [docs/V1-RELYING-PARTY.md:69](/home/tony/projects/tessera/docs/V1-RELYING-PARTY.md:69), together with lines 32–35.  
   The four listed conditions can all hold while an attacker captures both authority channels and issues under its own keys. The authentic verifier then returns VALID, although the original service never received or signed the content. Lines 76–79 disclose this attack but do not qualify the earlier “each statement … is true” assertion. The list also omits the registered signature and git-link security assumptions.  
   **Registered text:** A9 [lines 45–52](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:45); A10 [lines 417–430](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-10.md:417), especially the express new-receipt limitation.  
   **Replacement:** “The service-origin claims also require that the authority records named the service’s actual keys and that the registered signature and git-link security assumptions hold.”

2. **XP-02 — HIGH — A published key is insufficient bootstrap authority.**  
   **Location:** [docs/V1-RELYING-PARTY.md:89](/home/tony/projects/tessera/docs/V1-RELYING-PARTY.md:89).  
   Checking a signature using a key obtained alongside a substituted release authenticates neither. “Not marked TEST” also does not establish production authority: an attacker can remove that label. The missing instruction concerns authenticating the initial production key, rather than merely checking a signature.  
   **Registered text:** A10 [lines 644–655](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-10.md:644): production authentication requires the independently authenticated production key and rejects TEST authority, including overrides. Actual key creation/publication may remain deferred under lines 668–673.  
   **Replacement:** “Check the release signature with an independently authenticated production release key, and reject TEST keys.”

3. **XP-03 — MEDIUM — The case descriptions generalize beyond their fixtures.**  
   **Location:** [docs/V1-RELYING-PARTY.md:118](/home/tony/projects/tessera/docs/V1-RELYING-PARTY.md:118), also lines 120 and 122.  
   Re-signing with attacker keys does not universally produce INVALID: the retained authority evidence matters. Likewise, a strict retry produces VALID in d1 because it uses the unchanged honest receipt, not because any refused request becomes valid under strict verification.  
   **Registered text:** A9 [lines 178–182](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:178). The cited evidence fixes the distinguishing details in `docs/V1-PROFILE.md@8ea8bfa:1055–1069`.  
   **Replacement before the table:** “Case b retains honest DNS and git evidence; d3 retains honest DNS evidence and omits git; d1 uses honest receipt a.”

4. **XP-04 — MEDIUM — U lacks the validity warning and a precise identification of its six blocks.**  
   **Location:** [docs/V1-RELYING-PARTY.md:58](/home/tony/projects/tessera/docs/V1-RELYING-PARTY.md:58).  
   “One of six blocks” leaves the assumed segment unidentified. The guide later warns about T accompanying INVALID, but does not explain that a reported U also fails to establish a valid service receipt when the verdict is INVALID or CANNOT VERIFY.  
   **Registered text:** A10 [lines 277–283](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-10.md:277) identifies the selected block and five successors; [lines 300–305](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-10.md:300) states the non-valid-verdict limitation.  
   **Replacement:** “Use U only with a VALID receipt and A-UTC for the selected Bitcoin block and its five successors.”

5. **XP-05 — MEDIUM — The required historical-security instructions are missing.**  
   **Location:** [docs/V1-RELYING-PARTY.md:52](/home/tony/projects/tessera/docs/V1-RELYING-PARTY.md:52).  
   Reporting `historical_security: NOT_EVALUATED` states the omission but does not tell a later examiner what evidence to supply. A9 expressly requires that documentation.  
   **Registered text:** A9 [lines 259–265](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:259), supplemented by [lines 273–277](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:273): authenticated algorithm/key cutoffs, chain-time uncertainty and separate theft assessment.  
   **Replacement:** “To assess historical security, obtain authenticated safe-before cutoffs for each algorithm and key, and compare them with T using the registered chain-time uncertainty.”

6. **XP-06 — MEDIUM — The E8 table inventories L-05 but does not write its correspondence.**  
   **Location:** [formal/E8-E7-E11-SHEET.md:22](/home/tony/projects/tessera/formal/E8-E7-E11-SHEET.md:22).  
   Naming P4 invariants and symbolic families repeats the ledger inventory. It leaves unstated which symbolic fact corresponds to strict success and how non-acceptance relates to failed versus unperformable checks. The ledger explicitly says its enumeration does not write that mapping (`formal/suite/LEDGER.md:935–937`). This needs a prose correspondence, not a claim of proved composition.  
   **Registered text:** A1 [lines 397–406](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-1.md:397); the V1 sheet remains required by A9 [lines 205–208](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:205).  
   **Replacement:** “L-05 maps strict `Accept` to P4 with no waivers and every required check passed; failed checks map to INVALID, while unperformable checks without failures map to UNVERIFIABLE, a distinction ProVerif’s silent stopping does not itself establish.”

7. **XP-07 — MEDIUM — The E7 row marked OK does not distinguish its registered queries or expose C2.**  
   **Location:** [formal/E8-E7-E11-SHEET.md:53](/home/tony/projects/tessera/formal/E8-E7-E11-SHEET.md:53).  
   Q1d is a model containing multiple queries, rather than one lemma. Its unrestricted authorship correspondence, honest-key binding correspondence and reachability witness have different meanings (`sp1_q1_strict_dns_compromised.pv:144–154`). The sheet maps only C1, leaving the service-presentation claim C2 invisible.  
   **Registered text:** A1 [lines 391–395](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-1.md:391) requires a mapping per symbolic lemma; A3 [lines 68–74](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-3.md:68) identifies existential issuance-event authenticity; A9 [line 141](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:141) registers C2.  
   **Replacement:** “For Q1d and Q1r, query (i) maps to P1’s existential issuance-event authenticity (C2), query (ii) to honest-key byte binding (C1), and query (iii) supplies a reachability witness.”

8. **XP-08 — MEDIUM — The E11 index still lacks a statement for the V1 capstone evidence it uses.**  
   **Location:** [formal/E8-E7-E11-SHEET.md:89](/home/tony/projects/tessera/formal/E8-E7-E11-SHEET.md:89).  
   The missing statement is honestly disclosed, but the sheet nevertheless relies on strict capstone results at lines 63–67. An index of other families cannot substitute for a claim/adversary/boundary statement covering that composed evidence. This does not require closing the full capstone.  
   **Registered text:** A4 [lines 127–135](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-4.md:127); A9 [lines 207–208](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:207).  
   **Replacement statement:** “The strict capstone tests one-acceptance linkage against attackers holding one or both authority credentials; both-channel capture loses unrestricted service-origin assurance, and no result establishes time, concrete encoding or implementation conformance.”

9. **XP-09 — LOW — The runtime dependencies do affect acceptance.**  
   **Location:** [formal/P9-CONTRACT-INSPECTION.md:34](/home/tony/projects/tessera/formal/P9-CONTRACT-INSPECTION.md:34).  
   “No verdict effect” is incorrect for Unicode tables and ES serialization. They determine accepted strings and numbers. The cited startup-refusal rule concerns mismatching Unicode tables; it does not establish that the formatter has no decision effect.  
   **Registered text:** A9 [lines 145 and 149](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:145); cited evidence: `docs/V1-PROFILE.md@8ea8bfa:1010–1027`.  
   **Replacement:** “Unicode tables and ES serialization affect acceptance and belong to the fixed verifier/runtime; mismatching Unicode tables cause startup refusal rather than a receipt verdict.”

10. **XP-10 — LOW — F4 incorrectly says the code inspection has no governing sentence.**  
    **Location:** [formal/P9-CONTRACT-INSPECTION.md:71](/home/tony/projects/tessera/formal/P9-CONTRACT-INSPECTION.md:71).  
    A missing consolidated profile sentence does not leave the inspection without a rule: P9 explicitly forbids service-side state and live network dependencies, C6 defines the inputs, and A10 expressly forbids consulting the current clock.  
    **Registered text:** A1 [lines 278–281](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-1.md:278); A9 [line 145](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:145); A10 [lines 307–308](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-10.md:307).  
    **Replacement:** “The code inspection is governed by P9, C6 and A10’s no-current-clock rule; the profile should consolidate these requirements beside its input enumeration.”

11. **XP-11 — LOW — E7 introduces an unnecessary requirement for separate mapping sentences.**  
    **Location:** [formal/E8-E7-E11-SHEET.md:54](/home/tony/projects/tessera/formal/E8-E7-E11-SHEET.md:54), also lines 60–62.  
    Q1r explicitly inherits Q1d’s tables with the channels exchanged (`suite/s-p1/READING-AIDS.md:368–378`). “No own sentence” does not itself establish a missing mapping. E7 also concerns symbolic lemmas; absent P-numbers on individual TLA+ invariant rows are not additional E7 requirements.  
    **Registered text:** A1 [lines 391–395](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-1.md:391); `formal/BAND0-EXIT.md:67`.  
    **Replacement:** “E7 requires a mapping for each symbolic lemma; explicit inherited mappings count, and the TLA+ invariant rows provide context rather than additional E7 prerequisites.”

12. **XP-12 — LOW — The Q6 adversary citation is missing although the statement exists.**  
    **Location:** [formal/E8-E7-E11-SHEET.md:77](/home/tony/projects/tessera/formal/E8-E7-E11-SHEET.md:77).  
    The dash leaves the adversary component unindexed. Q6’s claim explicitly identifies degraded mode with the sole authority channel compromised; the detailed inherited capabilities are also available.  
    **Registered text:** A4 [lines 132–135](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-4.md:132). Cited evidence: `suite/s-p2/READING-AIDS.md:736–738` and `:251–256`.  
    **Replacement:** “Q6 adversary: sole authority channel compromised (:736–738), with the inherited capabilities at :251–256.”

13. **XP-13 — LOW — Essential technical terms appear before explanation.**  
    **Location:** [docs/V1-RELYING-PARTY.md:34](/home/tony/projects/tessera/docs/V1-RELYING-PARTY.md:34), continuing through lines 35–36, 64–65 and 107.  
    Keys/signatures, DNS, git, Bitcoin, SHA-256, frames and OpenTimestamps enter operational instructions without first-use explanations. Defining `A_sig` using undefined “frames” does not resolve this for the registered non-expert reader.  
    **Requirement:** [docs/plain/STE-STYLE.md:20](/home/tony/projects/tessera/docs/plain/STE-STYLE.md:20), rules 5–6, and [lines 39–40](/home/tony/projects/tessera/docs/plain/STE-STYLE.md:39); audience fixed by A9 [lines 119–121](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:119).  
    **Replacement at the first frame-dependent explanation:** “A frame is the exact bytes that one service key signs; it fixes the content and the receipt’s common information.” Apply the same first-use treatment to the other listed terms.


