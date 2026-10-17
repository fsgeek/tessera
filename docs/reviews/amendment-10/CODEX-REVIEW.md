# Codex non-author review — proposed Amendment 10

2026-10-16. **Result: revise before signing.** A10 correctly identifies the six source issues, and its substantive A03 counting argument matches the executable P5c guard. It still overstates capture visibility, unnecessarily excludes honest material signed after credential disclosure, leaves material clock wording unreconciled, mislabels three narrowing rows, and needs a verdict-precedence qualification. These are document findings, not demonstrated implementation failures.

Only this review file was written. A10 remains PROPOSED; A10.4 remains a recommendation awaiting the author's own ruling. This review supplies neither that ruling nor a signing act.

Severity: **HIGH** = unsupported security assurance; **MEDIUM** = incorrect scope, incomplete amendment registration, or normative ambiguity; **LOW** = editorial or evidence-description defect. Each fix below is proposed text for the owner to incorporate into A10, leaving the signed source files standing.

## Basis and evidence

Read A10 in full; all A01–A06 findings in `docs/reviews/plain-pilot/CODEX-REVIEW.md`; A9's opening, claim table, scenario mapping, and every passage A10 changes or invokes; A8 §A8.3/§A8.5; A1 §A1.1, P5 and §A1.6; A2 §A2.1's clock roles and convention pin; the cited encoding owner-name rules; and the profile's qualification, selection, pin and precedence rules. Also read the complete revision-2 pilot and `docs/plain/STE-STYLE.md`.

The governing A9 snapshot is `2ad34890359c446efaebcb116388b8e9ffbf6428`. The workspace A9 is byte-identical to that snapshot. A9's still-PROPOSED header defines the author's first containing commit as its signing act; this review treats A9 as signed on that basis, as requested. It does not independently authenticate the commit's cryptographic signature. Repository HEAD was `44f921e2df2ea963eca7e32ab749349cc29c08ff`.

| Input | SHA-256 |
|---|---|
| A10 | `b4d45307c132d50682a722b88872b61b1c237ddbacae306ef26ab41355e704a7` |
| A9 | `ff09f9b1ff6bb717bcca2c2f803eb8674f4beb2d28e88d5718320fe9b63c9f05` |
| Plain-pilot source review | `6132213e1b24a339537c3e3fac8a8ecd948d4f5f3825556aec0d92e43389705f` |
| Revision-2 pilot | `c94b9d8e7b7519e109ecb37439d0cf2055957c0c6ae280929f1f7a1cd4ea5f50` |
| Style | `96d2d8a19317013c5419ceba3b249ee0eb8008c3efcf4d0264eccdf89e1fe682` |

Locations below use these inspected files. A9 locations and the encoding locations explicitly marked “signing snapshot” were checked with `git show 2ad3489:<path>`, rather than inferred from current line numbers. The cited profile §7.1–§7.2 rules were also present at that commit; the workspace's unrelated profile/encoding changes do not supply new authority for them.

## F01 — HIGH: publication duty does not guarantee visibility after capture

**Location:** A10:23–26, :102, :127–130, :193–194. Source: A9:143, :495–500; A8:123–124.

The proposed boundary says “Such capture is made visible” and the summary says “The public git repository makes those new receipts visible.” A9 registers public publication as an **issuer duty**, explicitly outside what C4 proves. That does not force a credential thief to publish its substitute assertion. Nor does publishing a key assertion publish every receipt made under it. The proposed text turns an operating duty and an opportunity to notice a substituted key into an unconditional adversarial guarantee.

A concrete construction permitted by the stated checks is a captor with both channel credentials making matching DNS evidence and a privately retained, signed git assertion for its own service-slot keys. It anchors the assertion, waits for the registered chain-order gap, and anchors a receipt signed by those keys. The public repository need not contain the private assertion. Assuming eligible trust intervals, supported algorithms and the remaining checks, publication is no verifier obstacle. This is a construction argument from the rules, **not an executed V1 forgery vector**. Capture of only one required channel does not generally suffice.

**Exact fix:** replace the recommended boundary at :127–130 with:

> V1 does not prevent a captor of both required authority-channel credentials from issuing new receipts under a key assertion that names the captor's own keys, even while the original service keys remain uncompromised. Public publication of the key-assertion repository remains an issuer duty (A9.7, “Changed in effect”). If the substituted assertion is publicly published, a third party can inspect the substituted keys. The verifier does not check publication; V1 does not guarantee that a captor publishes the assertion, that capture is detected, or that new receipts are publicly visible.

Change A10.4's heading to `Authority capture: honest signed material protected; publication remains an issuer duty`. Replace the summary's A04 visibility sentences with:

> The service must publish its authority record. A third party can inspect a substituted key if that record is public. The verifier does not check publication. V1 does not guarantee that an attacker publishes the record.

Row 11 must point to this same boundary. Retain the author's quotation as motivation, not evidence that the desired visibility property is established.

## F02 — MEDIUM: “before the capture” gives up more than the tested property requires

**Location:** A10:23–24, :102, :120–123, :136–138; row 10. Source: A8:72–77; `formal/suite/capstone/SLICE-PREREG-2026-10-09.md`:12–30.

A8.3 protects **honest frames, signer sets and signatures** under credential disclosure; it does not restrict these to receipts issued before disclosure. The distinction is honest service material versus captor-created material, not simply old versus new receipts. In the actual `capstone_d.pv` fixture, :1121 publishes the authority secret before the replicated honest issuer processes at :1128–1130 run. In strict both-channel-capture companion `cap_cc01_c.pv`, :1148 publishes both secrets before the honest signing processes at :1156–1158. These fixtures do not model a pre-capture signing phase.

The before-capture restriction is explicitly labelled NARROW-CLAIM, so it is not concealed. It is nevertheless an additional reduction that A04's source finding does not require, and the options do not distinguish retaining protection for honest post-capture frames from promising presentation for arbitrary captor-created receipts. The latter has no blocking invariant; that does not imply the former must be abandoned. This observation does not promote slice reds to proof of all correct-form properties or to V1 implementation evidence.

**Exact fix:** replace :120–123 with:

> anyone who captures authority-channel credentials (the DNS credential or the repository key, including both together) while the original service keys stay secret and their signing capability stays uncompromised (A8.3's sense of capture), as to frames honestly signed by those service keys, whether before or after credential disclosure: such a captor cannot reattribute those frames to other keys or another service, alter their honest signer sets, or carry their signatures onto other bytes or keys (A8.3);

Replace the options at :136–138 with:

> (a) Adopt the bounded honest-material claim above, with the new-receipt limitation and conditional publication statement. (b) Deliberately restrict even that claim to receipts honestly issued before capture; this gives up the honest post-capture material covered by A8.3's stated property and must be recorded as an additional author choice. (c) Extend presentation protection to arbitrary new receipts under captor-selected keys; this needs a named blocking invariant that V1 does not have, and is not supported by this amendment. (d) Rule other text. Rows 10–11 take effect only on the author's ruling.

Update the summary and heading consistently. Keep the explicit statement that A8.3 does not test backdating, and keep guarantee 2's authority-capture proviso. Nothing here requires adding a mechanism to rescue option (c).

## F03 — MEDIUM: three table rows narrow claims under other labels

**Location:** A10:34–36, :83, :187, :191–192, :206–207.

Rows 8–9 remove the exactly-k reorganization case from A9's literally claimed protection. That is a claim reduction even though it faithfully corrects the boundary to match the model. A10 itself acknowledges this at :47–48. Calling it CORRECT does not satisfy the requested distinction. Row 4 applies the same removal of a UTC interpretation to the success definition that rows 1–3 correctly label NARROW-CLAIM; leaving the sentence's bytes unchanged does not leave its claimed meaning unchanged.

**Exact fix:** label A10.3 and rows 8–9 **NARROW-CLAIM**. Label row 4 **NARROW-CLAIM**, A9.7 kind **R**. Use this definition at :36:

> CORRECT: the wording disagreed with a registered rule or model. The correction follows that rule or model without reducing the claim.

Add to A10.3:

> This narrows A9's literal prose claim at equality. It changes neither the model nor its permanence assumption, and withdraws no checked model result.

Before the additional rows required by F04, the corrected fourteen-row totals are **ten NARROW-CLAIM, one CORRECT, three CLARIFY**. Recalculate the final counts after all table changes. Row 14 can remain CORRECT: A9 already adopts the exact prefixed owner in the signing-snapshot encoding. Row 7 merely retains the term for the two values; rows 12–13 can remain CLARIFY if they preserve the existing checks and precedence as in F05.

## F04 — MEDIUM: the clock correction omits registered uses of the same unsupported bound

**Location:** A10.1 and A10.7, especially :64, :184–187, :199–204. Omitted source: A9 at `2ad3489`:177, :186, :294–295, :433–439.

The table's **existing source locators are correct**. A whitespace-normalized comparison found every quoted source span in its cited signing-snapshot line range. But “rows 1–4” do not inventory every A9 sentence whose meaning must change under A10.1:

- Scenario a/g says the bytes were “presented to Tessera by T” (:177).
- Scenario i says the signed contract “existed by T” (:186).
- Issue order says “A signature made after T cannot fit the anchor” (:294–295).
- Guarantee 1 says “anchored by T”, and locates its historical assumptions and excluded unauthorized signing “before T” (:433–439).

The issue-order sentence is particularly concrete: a signature made after a backward-skewed header's nominal UTC time, but before the block is mined, **can** fit the block's anchor. Replacing only the headline and C5 leaves this false literal reading standing. The scenario sentences are part of the registered safe decisions, so an amendment claiming to list every changed registered sentence cannot silently reinterpret them. Qualifying those decisions changes their explanatory claims, not their verdicts or case membership.

**Exact fix:** add signing-snapshot source rows and operative replacements in A10.1 for these passages:

| Source | Exact replacement for the identified words |
|---|---|
| A9:177, `these bytes were presented to Tessera by T` | `these bytes were presented to Tessera before the selected Bitcoin block was mined; its header time T is not a UTC upper bound` |
| A9:186, `this signed contract existed by T.` | `this signed contract existed before the selected Bitcoin block was mined; its header time T is not a UTC upper bound.` |
| A9:294–295, `A signature made after T cannot fit the anchor.` | `A signature made after the selected Bitcoin inclusion block was mined cannot fit that block's anchor under the registered commitment and history assumptions.` |
| A9:433, `A receipt whose exact signatures are anchored by T` | `A receipt whose exact signatures are committed by the selected Bitcoin inclusion block` |
| A9:436–439, each `before T` | `before inclusion in that block` |

Preserve each sentence's remaining conditions, the parties' signature-checking duty in scenario i, and `historical_security: NOT_EVALUATED`. Label these scope qualifications NARROW-CLAIM/R. Give row 4 an explicit replacement, for example `before the selected Bitcoin block was mined; its header time T is not a UTC upper bound`, rather than “the sentence stays”. Update A10.1's row references and the totals. Do not edit A9 or change the mapping's verdicts, fixtures or safe-decision categories.

A1.6:485–505 contains older compressed clock/depth language too. A10 explicitly leaves A1 standing. State that this is a V1 qualification of the inherited clock wording, rather than claiming that unchanged historical prose itself proves a UTC bound. No model equation needs to change to make this documentary boundary honest.

## F05 — MEDIUM: row 13's unconditional UNVERIFIABLE conflicts with a performable failed check

**Location:** A10:148–165, :196. Source: A9:287 (A4.2 precedence); profile:789–802, :818–834, :1497–1509.

The qualification and lowest-height selection conditions match the cited profile, including the covered h=100 plus headerless h=90 example. However, row 13 says “if no attestation qualifies, or a supplied header is unpinned, the result is UNVERIFIABLE.” That is too strong. A sole attestation contradicted by its pinned header fails `OTS_MERKLE_MISMATCH` and leaves no qualifying attestation. Stage 2 correctly identifies INVALID; row 13 then prescribes UNVERIFIABLE. Similarly, an unpinned header can coexist with another independently performable failed required check. A4.2 still requires INVALID to win.

The stages also need to be identified as selection logic, not a new early-return verification procedure. The profile independently checks all supplied consecutive-height links (`HEADER_CHAIN_BROKEN`), OTS grammar and stamp digests, and selected-height transaction/path requirements. Failure to qualify must not suppress those checks or let a verifier jump to a higher height to evade a failed selected-path check.

**Exact fix:** insert before the stages:

> These stages explain qualification and selection within the existing verifier. They do not replace other registered checks, their dependencies, or dispatch and reason-code precedence. A failure of an independently performable required check takes precedence over an unperformable check under A4.2. The header-pool link checks, OTS grammar and stamp checks, and selected-height transaction/path checks remain unchanged. A stage's UNVERIFIABLE entry is an unperformable-check result, not an early return that suppresses other checks.

Replace row 13's first replacement sentence with:

> An attestation beyond the newest pin never qualifies. If no attestation qualifies, or a supplied header is at a height with no pin, the applicable check is unperformable (A10.5 stages 1, 4); the overall verdict is UNVERIFIABLE unless another independently performable required check fails, in which case it is INVALID under A4.2. Existing reason-code precedence is unchanged.

Retain the stage-2 merkle contradiction failure and the second row-13 sentence's exceptions. Apply the same qualification to the prose “Cases” and stage 4. This preserves the existing verdict contract; it does not add a new check.

## F06 — LOW: composing the C5 replacements still identifies T with an attestation

**Location:** A10:186, :195; A9:144 at the signing snapshot.

Rows 3 and 12 replace overlapping parts of the same C5 sentence. Applying both literally yields “no later than T in chain time, the qualifying attestation ...”. T is a header time, not an attestation. The original sentence already had this compressed apposition; the proposed exact replacement still does not express the type distinction stated correctly in A10.1 and A10.5.

**Exact fix:** supply one assembled replacement for C5's claim cell, and point both affected table entries to it (or consolidate them):

> The frames **and their exact signatures** existed before the selected Bitcoin block was mined. T is that block's header time, not a UTC upper bound. The selected block belongs to the qualifying Bitcoin attestation at the lowest block height in the presented OTS proof, under A10.5's stages; T and its confirmations come from that same attestation. The three-conjunct predicate holds at k = 6. Header times need not be monotone; selection uses chain order, not the least header time (OWNER DECISION 2026-10-14, F03).

Keep the existing non-claims, with the reorganization residual amended separately. This gives the body and table a single reviewable replacement and retains the original selection provenance.

## F07 — LOW: arithmetic witnesses are described as passing every registered check

**Location:** A10:77–78. Source finding A02:543–550 of the plain-pilot review.

The source review expressly calls its examples arithmetic witnesses, not executed receipt vectors or evidence of an honest shipment. A10 says they “satisfy every registered check.” The examples establish the two window comparisons and all three A2 time comparisons; they contain no signatures, authority paths or complete verifier input with which to establish the other checks.

**Exact fix:** replace the sentence with:

> The review's two arithmetic witnesses satisfy the two window comparisons and all three A2 temporal comparisons. They are not executed receipt vectors or evidence that an honest issuer ships those values.

The surrounding inclusive bounds, absent T-versus-not-before comparison, absent declared-versus-not-after comparison, and separate issuer stop duty are otherwise faithful.

## F08 — LOW: the plain summary does not yet meet its dictionary and first-use rules

**Location:** A10:12–36. Style rules 4–6; dictionary:48, :89–90, :103–114.

The summary fits the sentence-length limits under whitespace counting, its paragraphs fit six sentences, it uses lists, and it contains no forbidden “should”, “may” or “shall”. No body section-number cross-reference needs moving. It nevertheless uses Bitcoin, git and DNS without first-use explanations, uses “issuer” where the dictionary requires “service”, and uses project vocabulary “parameter” and “test vector” without dictionary entries. Its quoted “the keys can issue receipts” can remain a visibly attributed problematic source expression, but it should not become the summary's own description of the actor. The unsupported visibility assertion is F01, not merely a style issue.

**Exact fix within A10 only:**

- Replace :14–15 with: `This amendment corrects six wording problems in Amendment 9. It adds no mechanism. The verifier uses the same checks and gives the same verdicts. A review of the plain version of Amendment 9 found the six problems.` Keep the precise parameter/vector/encoding inventory in the technical body.
- Before the bullets, add: `Bitcoin is a public system that adds blocks to a chain. A block header states a chain time. This value is not a measurement of real time. The registered number k is six.`
- In A04 use the corrected sentences in F01, with “service” instead of “issuer”. If retaining “git”, first add: `Git stores versions of files and links them with hashes.`
- Before the A06 name explanation, add: `DNS (the Domain Name System) holds one authority record.` State the active rule as: `The verifier must check the DNS owner name _tessera-v1.wamason.com.` Use code formatting for the name in the actual document.
- Preserve the distinction between NARROW-CLAIM and the other kinds with F03's corrected definition. Revise the A04 summary to protect honest signed material under F02, or explicitly identify the author's additional before-capture restriction if chosen.

These additions use the supplied dictionary and leave `STE-STYLE.md` untouched. They do not certify all of that dictionary's proposed entries for publication.

## A01–A06 disposition and requested checks

| Item | Evidence check | Assessment |
|---|---|---|
| A01 | A9:36–37, :114, :133, :144, :294–295, :433–446; A2.1 clock roles | Existence before inclusion is supported under the commitment/history assumptions; a finite UTC upper bound is not. Direction correct; complete the inventory and assembled text under F03, F04, F06. |
| A02 | A9:419–426, :441–447; source arithmetic witnesses | Two inclusive asymmetric comparisons are correct; no new comparison or tighter tolerance is introduced. Correct the evidence wording under F07. |
| A03 | A1.6:504–508; A2.1:208–214; actual P5c actions and configurations | Exactly-k orphaning is excluded by assumption, not proved impossible. Proposed boundary matches executable coverage; relabel under F03. |
| A04 | A8.3:72–77; A8.5:123–124; capture fixtures; A9 publication duty and trust rules | Honest-material binding and arbitrary new issuance are distinct. The recommendation needs F01/F02; the author still decides. |
| A05 | Profile §7.1–§7.2 and precedence table at both signing snapshot and workspace | Candidate qualification and selection order are already specified. Preserve all independent checks and A4.2 precedence under F05, and assemble C5 correctly under F06. |
| A06 | Signing-snapshot ENCODING-V1:551–553, :623–624; A9:414–415 | Correct: owner is `_tessera-v1.<common.issuer>`, label-sequence comparison ignoring ASCII case; V1 value `_tessera-v1.wamason.com`. No owner check or encoding changes. |

### A03: direct model check, rather than reliance on its comments

`formal/tla/P5c_IssuanceProtocol.tla`:26–29 explicitly pins depth to blocks **after** inclusion. The executable actions implement that convention:

- `Anchor`, :225–229, sets `depth = 0` at inclusion.
- `Tick`, :199–207, increments included-anchor depth up to `DepthK`.
- `Reorg`, :236–241, requires `depth < DepthK`.
- `Ship`, :260–266, requires `depth >= DepthK`.

Consequently with k=6 and DepthK=5, a five-confirmation anchor has depth=4 and can be orphaned; a six-confirmation anchor has depth=5 and cannot. Removing six old tip blocks at that moment would remove the anchor, and is outside this model's transition relation. The model has no separate variable for the number of old blocks a reorganization removes: A10 defines that ordinary-language quantity and relates it to the guarded anchor depth.

Both `_Broken.tla`:65–70 and `_BrokenSilent.tla`:73–78 retain the same strict reorganization guard; their mutations do not test orphaning an anchor at the permanence threshold. The default P5c config uses DepthK=2, so it is not itself a six-confirmation instantiation. The actual `k6-2026-09-14/P5c/P5c_k6_d3.cfg` and `P5c_k6_d6.cfg` both use DepthK=5. The archived d6 output reports completion without an error; that is an inspected historical result, not a fresh run. The bridge explicitly omits reorgs (`P5cP5P6_Bridge.tla`:65–69). None of these files supplies equality-case orphaning coverage.

This supports A10's “never covered” statement **for the cited P5c/bridge model family and registered permanence assumption**. It is not a proof that Bitcoin cannot reorganize by six blocks. Some model comments use “depth k” loosely; the executable guards and A2's explicit mapping are the load-bearing evidence.

### Mechanisms, checks, parameters and encodings

No mechanism, formal action, cryptographic algorithm, tolerance, k/N/S value, frame, `A_sig` encoding, authority-record grammar, vector or registered verdict mapping is newly introduced by the proposed corrections. The selection conditions and reason codes in A10.5 already exist in the signing-snapshot profile. F05 identifies a contradictory prose verdict instruction that prevents an unconditional “no verdict change” pass as drafted; its fix preserves the existing rule. F04 changes the explanation of registered safe decisions without changing their outcomes. No additional model run or vector is required to correct these documentary defects.

The current table is not ready to sign as a complete inventory: all fourteen existing locators/quotations match, but F04 adds missing registrations, F03 changes kinds, and F06 supplies the assembled replacement. Rows 10–11 honestly remain conditional on the author's ruling. The final table and summary must be regenerated from the author's chosen A04 text and the completed clock inventory.

## Brief re-check — A9 plain pilot, revision 2

**No remaining ADDS, DROPS or CHANGES found within its stated scope:** A9's opening claim/adversary/boundaries and C1–C7, with the source rules those clauses invoke. Rechecked the restored assumptions, issuance-event wording, both signature frames, C3 control/misuse limits, complete git path and six-confirmation chain-order gap, temporal comparisons, all-supplied-header rule, C6 limits, C7's bounded human-test criterion, and missing-status-capture negative control. The earlier F01–F23/O01–O05 omissions and changes are repaired in this revision.

The A01–A06 markers visibly retain the unresolved signed-source issues. In particular, “deeper than k”, the existing “no later than T” claim, the neutral “DNS owner name for wamason.com”, and the ambiguous selected-anchor wording are not counted again as new translation defects. A10's proposed resolutions do not govern this pilot yet. This is a faithfulness finding for the specified excerpt, not a certification of the whole A9, every dictionary entry, or full style compliance of revision 2.

## Validation limits

Source-span/line matching and input hashes were checked mechanically; claim boundaries, style and proposed fixes were reviewed manually. Actual model source and archived run output were inspected. No ProVerif/TLC model, V1 implementation, cryptographic assumption, publication enforcement, or human test was newly executed or discharged by this review. No signed source, pilot, style guide, profile, encoding or model was edited.
