# Codex review of H2 record — 2026-10-13

Reviewed all 97 lines of `docs/h2-record-2026-10-13.md` against the current working tree at HEAD `b87d192b91d57a578870d9197e05cbf9efc916e7`. Amendment 9 and the schedule are present as untracked drafts; their own status statements govern. This review changes no registration or adoption state. Severity: HIGH affects the outcome or central evidentiary claim; MEDIUM affects attribution, scope or reader trust; LOW is a local citation defect.

The record usefully admits delegated design ownership. Its strongest conclusion nevertheless outruns the registered test, and its replacement success narrative outruns the product test. Those are substantive problems even in an explicitly contestable owner reading.

## Findings

### 1. HIGH — “H2 as registered is falsified” omits the registered examiner and an observed inability to justify

**Location:** H2 record:11–13, 48–49, 65–68, 95–96.

**Evidence:** `docs/phase-0-prereg.md:225–231` requires the same panel of at least three unrelated LLM models used for security review, tasked to interrogate architecture ownership, to find a load-bearing decision the author **cannot justify without reconstructing it from AI reasoning**. The draft substitutes “a review” for that panel and predicts that the author “would” read AI reasoning. AI origin, delegated ownership, and not making every critical decision do not themselves establish inability to justify a decision. The supplied 13 October quotes admit a division of labor; none reports the registered inability. The last live quote explicitly distinguishes agreement from lack of consideration. A9:161–163 preserves the H2 panel.

**Proposed fix:** Quote the complete registered falsification condition. Report “owner assessment: the ownership narrative has diverged; registered H2 adjudication remains pending” unless the panel evidence exists. For formal falsification, link the panel composition and interrogation record, name one concrete load-bearing decision, and record the author's attempted justification and the panel's finding. Do not treat this single review as the completed panel. Delegation can establish a conflict with the README's ownership promise separately.

### 2. HIGH — December's product test cannot adjudicate the new stewardship claim

**Location:** H2 record:70–79, 93–97.

**Evidence:** `docs/V1-SCHEDULE.md:9–16,28` tests product provision, safe relying-party decisions, and operation without Tessera. A9:107–118,169–185 narrows comprehension evidence to one independent human tester on a finite mapping, expressly not relying parties generally. Neither test establishes who caught historical drift, that direction always stayed with the author, or that stewardship is “enough.” A successful product can result from AI design with little author comprehension; a product failure need not falsify the author's steering. Nor does an unsafe accept imply an invalid receipt: cases e, f and i′ deliberately return `VALID_STRICT` while requiring a bounded interpretation or rejection of the contract.

**Proposed fix:** Say December supplies bounded product/usability evidence, not authorship or causal stewardship evidence. Describe unsafe **relying-party decisions on the registered mapping**, not simply unsafe receipts. If a new process hypothesis is desired, explicitly propose it prospectively with its own observable test and adjudicator; do not attach it retrospectively to the product gate or use it to rehabilitate H2.

### 3. MEDIUM — “came from him, in his words” conflates author prompts, adoption and AI choices

**Location:** H2 record:27–38.

**Evidence and attribution audit:**

| Item | Repository support and boundary |
|---|---|
| Purpose: “cheap, easy attestation,” survives exit | Offline/without-service purpose is supported by A9:28–34,107–117 and the schedule:13–15. The exact “cheap, easy attestation” quote was not located elsewhere in the repository. Its source/date needs identification; a general purpose is not evidence for the exact wording. |
| Throwaway prototype | `prototype/README.md:3–13` explicitly says author's suggestion, 6 October, and gives the diagnostic purpose. `formal/suite/capstone/READ-CAPSTONE-2026-10-06.md:78` also credits the idea to him. This supports the suggestion; neither quoted entry proves his precise internal suspicion or that every implementation/test was his. |
| PQ preference | A9:96–97,295–297 quotes the author and explicitly calls it a preference. The conditional hybrid, fallback and pass criteria are OWNER decisions (71–75,293–326). |
| Hardware protection | A9:91–92 quotes the author's requirement. The selected hardware deployment/profile is the owner's implementation of it. |
| Limited key lifetimes | A9:93–95 quotes the author; it explicitly assigns the single window of at most 90 days to the owner. The concern is author's; the window rules and concrete guarantees are OWNER decisions (71–75). |
| Separation of control as “real long-term protection” | A9:238–245 records it as a candidate V2 capability under an OWNER DECISION section (221), with no promise, schedule or gate. No author quote there attributes this thesis to him. V1 expressly claims no separation of control (136,368–372). The draft overstates repo evidence for author origin. |
| Contracts in `content` | A9:85–90 quotes the author's corrective intervention. Cases i/i′ are an owner addition (183–185), not the author's detailed test construction. |
| `wamason.com` | A9:63–64 explicitly records AUTHOR DECISION and quotes him. Supported. |
| Revocation not evaluated, optional add-on | A9:57–59,247 records AUTHOR DECISION B, but his words adopt the presented alternatives; they do not establish that he originated them. The owner/Codex drafting provenance is recorded in `docs/V1-SCHEDULE.md:3–5` and A9:4–8. This is author adoption, not demonstrated author invention. |

**Proposed fix:** Replace the universal origin claim with “Author suggestions, requirements, corrections and adoptions included…” and attach the above sources individually. Label Decision B as adoption. Attribute the concrete issuance window, conditional signer profile and guarantees to the owner. For separation of control, add a dated author source or say the repository records it as an owner-listed V2 driver. Date/source the purpose quotation; if it too is from the exempt live session, explicitly label it 2026-10-13. Do not present unlocated wording as fabricated; the limitation is public traceability.

### 4. MEDIUM — The “detail” account erases recorded author adoption and substitutes proof fluency for design judgment

**Location:** H2 record:40–49,70–71.

**Evidence:** `formal/spike/DECISION.md:13–22` records an AI tool recommendation ratified by the author after cold model reads. `formal/spike/first-link/DECISION.md:366–371` identifies a cross-review-originated required-set recommendation as ADOPTED by the author. `formal/spike/standing-probe/DECISION.md:378–398` records AI-originated standing selection, author adoption and two independent probes before adoption. First-link DECISION:100–119 records the author's distinction between defending core design decisions and reproducing individual proofs. AI construction of suite artifacts is well supported, but classifying all suite-related work as AI detail and predicting dependence on its reasoning loses these counterexamples.

**Proposed fix:** Distinguish model/code production, AI-originated recommendations adopted after consideration, and later owner-only design decisions. Include the earlier documented adoptions as counterevidence. For any H2 example, establish that it is a load-bearing architectural decision and that independent justification fails; inability to reproduce formal syntax is insufficient. Remove “Each of these is defensible” unless linked to the relevant review evidence and bounded by its assumptions.

### 5. MEDIUM — Proposed and adopted states are blurred, and the signature explanation omits its exception

**Location:** H2 record:4–6,24–25,87–89.

**Evidence:** A9:3–4,20–22 says PROPOSED, binds only on author signing, and says the signature ratifies five parameters as his decisions. A9:217–219 repeats the exception. The H2 draft describes the signature's meaning without this qualification and says provenance labels “follow” A9. Its new automatic one-sentence route to AUTHOR ADOPTED is a proposed policy, not A9's label definition. A9:13–14 already recognizes explicit author adoption; first-link DECISION:133–135 makes endorsement, rather than original authorship, the basis of ADOPTED.

**Proposed fix:** Say “Under proposed A9, if signed, OWNER items mean read/no objection, except the five parameters explicitly put to the author.” Mark the new reason-recording convention as a proposal to strengthen evidence of consideration, not an existing rule or proof of comprehension. Preserve original recommendation provenance when adoption is added. A sentence may document consideration; it cannot automatically discharge H2.

### 6. MEDIUM — Prototype counts are correct but selected presentation makes the check sound more independent and conclusive than it was

**Location:** H2 record:71–79,94–95.

**Evidence:** `prototype/TRIAGE.md:74` confirms 0 WRONG, 21 MISSING (and 50 DEFER). However, TRIAGE:31–37 says exact model abstractions prevented finding WRONG in stubbed areas, real primitives could contradict claims, and the prototype used the same model family as the spec. TRIAGE:96–97 specifically labels authority-channel scope as triage analysis not tested by the prototype. “Recovered it each time” has no enumerated incident/recovery record. “The author … builds the external tests” misattributes construction: prototype reports credit Claude builders, while the schedule:3–5 credits an owner revision of a Codex draft.

**Proposed fix:** Retain the counts with the same-family/stub/triage-analysis limitations. Credit the author with requesting the prototype and accepting the testing direction, and AI with building and analyzing it. Replace universal recovery language with specific documented interventions and their bounded outcomes. Call these implementation-facing checks; distinguish them from an independent tester and from independent model families.

### 7. MEDIUM — H0's honest-stop clause is repurposed as an H2 continuation rationale; elapsed time is not H2's test

**Location:** H2 record:16,68,81–83.

**Evidence:** `docs/phase-0-prereg.md:734–735` reads “**If H0 cannot be met**, the project does not proceed as designed — and that is a valid, honest outcome…” The quoted fragment removes this specific antecedent and adds “is” inside the quotation. It does not supply an H2 disposition or authorize continuation following H2 falsification. The 4–6-week plan is exempt live-session testimony, but no elapsed-time condition occurs in registered H2:225–231. The schedule:3,28 does support accepted dates and an author ship-or-stop decision. Initiation on 10 June (`README.md:22`) makes “fifth month” consistent with 13 October.

**Proposed fix:** Quote the H0 sentence accurately and explicitly call it an analogy about honest reporting, not an H2 rule. Keep schedule divergence separate from H2 adjudication. State continuation as the accepted V1 schedule/author decision, preserving A9:161–163's separation of V1 from the original product/H2 done-line.

### 8. MEDIUM — Excluding raw review findings concentrates narrative control in the instance whose ownership is under review

**Location:** H2 record:87–91.

**Evidence:** The owner writes the outcome, chooses which outputs the author sees, and proposes that review findings are never routed, while using a one-sentence adoption convention to strengthen author labels. A hostile reader could reasonably see this as an accountability shortcut: unfavorable evidence may be filtered into conclusions before the author considers it. A9:216 still calls for author accept/reject per E9 row; first-link DECISION:110–119 preserves independent author assessment from readable claim statements. Neither requires rote reading of all prover output.

**Proposed fix:** Keep concise summaries, but link full findings and contrary evidence, route authorship/credibility disputes and direction-changing findings explicitly, and preserve required independent author judgments. Say the sentence records a considered reason, not that low effort guarantees the process is “not theater.” No blanket requirement to read every vector or proof is needed.

### 9. LOW — Opening quotation is from README, and the signature phrase is a paraphrase presented as quotation

**Location:** H2 record:4–5,25.

**Evidence:** “The journal is measured against that record, including honest divergence” is exact after whitespace normalization at `README.md:44–45`, not in the preregistration. Prereg:7–8 expresses a similar thought in different words. A9:20–21 says “the author has read them and does not object”; “read and does not object” is a shortened paraphrase, not an exact excerpt.

**Proposed fix:** Cite README:42–45 for the opening quote (or quote prereg:7–8 accurately), and remove quotation marks from the signature paraphrase or copy the exact source wording.

## Remaining quotation/citation checks

- H2's substantive sentence and the “finds a load-bearing decision…” excerpt match prereg:225–231 after line-wrap normalization. The cited range is correct. The omitted panel requirement is finding 1, not a transcription discrepancy.
- The credibility-line excerpt matches prereg:87–89 after normalization; the cited 86–89 range is correct.
- The 17 September delegation quote has repository corroboration in `docs/requests/2026-09-30-reply-to-governance-consent-calibration-study.md:5`. A9:15–17 dates its own ownership assignment to 12 October; explain the earlier delegation and later Q1 return rather than silently treating those dates as identical.
- The 12 October Q1 quote matches A9:66–69 exactly after normalization. “Before any code” is exact at prereg:102 and A9:189; the replacement is an OWNER decision, as the draft says.
- “Decision B” correctly identifies the A9:57–59 decision. Its origin/adoption distinction is finding 3.
- “AI … never contributes ownership” is an explicitly elided rendering of README:13–17, not the literal registered H2 sentence. The proposed README should distinguish its stronger ownership promise from H2's independent-justification test.
- The 13 October author quotations, including the 4–6-week plan, are accepted as supplied live-session testimony. No unsourced finding is made against them. The tension between “considered the option” and the owner's inference that independent justification would fail is covered by finding 1.
- The December date acceptance is supported by schedule:3 and A9:120–121. The documentation/tools/offline summary is supported by schedule:13–15,28 and A9:110–117; claiming one test establishes general stewardship is not.

Overall disposition: revise before presenting this as a registered H2 result or adopting the proposed README. Preserve the admission of delegated ownership, but separate it from an unperformed independent-justification test and from the future bounded product evidence.
