# Codex cross-family review: V1 derivation

**Verdict: REVISE BEFORE ADOPTION.** A strict, standalone, offline-verifiable V1 is a defensible reduction of Tessera's delivery scope. This draft does not yet specify that reduction faithfully enough to adopt Amendment 9 or discharge its proposed exit gate. The main defects are a false non-repudiation test, an incomplete revocation weakening, overstated authority/time evidence, missing registered commitments, and exit criteria that require implementation evidence before implementation exists. The 30 October date is accepted; the proposed success definition and this amendment are not.

Reviewed on 2026-10-09 against repository HEAD `b87d192`, including the complete derivation draft, `docs/V1-SCHEDULE.md`, the preregistration, Amendments 1–8, `formal/PROPERTIES.md`, `formal/BAND0-EXIT.md`, the implementation specification, prototype findings and relevant implementation/report artifacts, capstone results, and git history. Amendment 8 first appears at `d379062`; the capstone adoption questions remain partly deferred in the recorded 7 October disposition. This is a source-and-record review, not a rerun of the formal suites, an E18 sign-off, or an inspection of a future V1 implementation. “Critical” blocks adoption of the claim or amendment; “High” blocks faithful scope accounting or the stated evidence/gate; “Medium” requires correction without adding a new delivery capability.

## 1. C1 and C3 describe one shared frame; the adopted construction has two signer-specific frames

**Severity: Critical. Location:** `docs/V1-DERIVATION-DRAFT.md:29-31`, `:38`, `:308`.

Amendment 5's adopted reading is common attested content in separate signer-specific frames. Their key-fingerprint fields differ. This is stated explicitly in `docs/implementation-spec.md:432-449`, citing A5.4 and A7.9. Consequently, “Both required keys signed exactly this frame” is false for that construction. The OTS commitment over two frames also needs a defined preimage: stamping two files produces two proofs, not the proposed single receipt proof (`prototype/PHASE3-REPORT.md:162-166`). Choosing a common OpenPGP verification primitive does not settle either byte layout.

**Exact fix:** Replace C1/C3 with: “The verifier reconstructs each required signer's exact frame. Both frames bind the same attested content and common metadata, with the designated signer's fingerprint in its slot. Each required signature verifies over its designated frame.” Require the O-79 map to define requester content versus signer metadata, slot ordering, lengths, and the unambiguous receipt-anchor preimage. If one shared frame is actually intended, name and amend A5.4/P3 instead of treating this as an encoding detail. Keep payload-byte identity distinct from equality of the two complete frames.

## 2. The P6 weakening removes more than the conjunct named in A9.4

**Severity: Critical. Location:** `docs/V1-DERIVATION-DRAFT.md:23`, `:32`, `:217`, `:290-293`, `:313`.

P6 requires both `key_authorized(declared_issue_time)` and no revocation effective at or before the anchor (`docs/phase-0-prereg-amendment-1.md:199-214`). A9.4 names only the latter. A verifier evaluating no revocation cannot claim it checked the former against effective revocations either. Publication of a key is evidence of an authorization assertion, not proof that the assertion was still operative. C4/headline “authority ... shown at issuance” therefore remains stronger than the proposed verifier establishes.

**Exact fix:** State the complete exception: V1 verifies the named historical channel assertions and their bindings, but does not determine whether effective revocation defeats authorization at the declared time or anywhere in the temporal window. Amend both affected P6 conditions for this profile and the corresponding prereg §4.4 interpretation. Change C4/headline to “the named channels authenticated publication of these keys for D, at the specified evidence times; effective revocation is not evaluated.” If retaining the stronger authorization claim, supply authenticated status evidence now. Add a case where revocation precedes declared issuance yet the old publication evidence remains cryptographically valid. A `VALID_STRICT` V1 report must expose its profile-specific reduced meaning prominently.

## 3. The proposed “later capture does not repudiate V1 receipts” test fails its own promise and contradicts Amendment 4

**Severity: Critical. Location:** `docs/V1-DERIVATION-DRAFT.md:294-298`, `:303-304`, `:321`.

A9.4(iii) expressly allows a V1 receipt accepted without status to become `INVALID` when later evidence arrives. That is repudiation of the previous validity result under a stronger assessment, even if disclosed in advance. Moreover, (ii) repeats superseded prose: revocation after the anchor is harmless only if it is also after declared issuance. With anchor=10, declared=12, effective revocation=11, the proposed (ii) says unchanged; adopted A4.3 says invalid (`docs/phase-0-prereg-amendment-4.md:111-123`). The relevant boundary for these two conditions is `max(anchor_time, declared_issue_time)`.

Byte-identical reports are also undefined once evidence, observation fields or software version changes. A finite set of honest AWS receipts tests those fixtures; it does not establish preservation for every possible V1 receipt. Revocation is not the sole possible future ground for invalidity: newly exposed false evidence and changed cryptographic assumptions remain possible.

**Exact fix:** Choose and name one of two contracts. (a) Preserve an immutable, versioned V1 base evaluation under the same bundle, profile, policy and trust configuration; report later LTV findings in a separate assessment that may contradict authorization without rewriting the base report. Or (b) promise only that missing LTV capture does not by itself invalidate a V1 receipt, and explicitly permit later authenticated adverse evidence to change the stronger assessment. Do not call (b) non-repudiation. Define stable fields, evidence authenticity/freshness, and the interaction with historical authorization. Add vectors for revocation before declared time, between anchor and declared in both orders, after both, absent status, conflicting status, and unauthenticated/backdated status. Preserve the missing-capture broken companion. Label `G_v1` regression evidence, not a proof of the universal contract.

## 4. C4 promises repository publication that the archived git evidence cannot establish

**Severity: High. Location:** `docs/V1-DERIVATION-DRAFT.md:23-24`, `:32`, `:96-116`, `:334`.

The prototype report says plainly that an unpushed commit gives identical archived bytes and that nothing in the evidence proves public publication (`prototype/PHASE3-REPORT.md:190-199`). A signature plus OTS establishes a signed commitment and an existed-by bound under the repository trust key. It does not establish distribution through a public repository at issuance. Git and DNSSEC also require their own historical validity/temporal relationships; an author-chosen commit date is not independent time evidence.

There is an additional implementation gap in the proposed two-hour completion test: `prototype/tessera_proto/real/gitchannel.py:125-134` verifies object IDs and the commit-to-root-tree link, but does not verify every tree-entry link down to the alleged key-publication blob. The collector builds a path from local git; an offline verifier must check the adversarially supplied path itself. Passing this function is insufficient evidence that the signed commit contains the claimed publication.

**Exact fix:** Describe the git channel as an authenticated, time-anchored key assertion rooted in the distributed repository key. If actual public publication is part of V1, define separate publication evidence and its trust assumption. Require complete commit→tree→subtree→blob path verification, exact extraction/comparison of D and the manifest/key set, signature verification, and binding to the commit's OTS proof. Add a detached/substituted-blob negative case. Do not use `gitchannel.py`'s current successful return as the complete channel acceptance criterion.

## 5. M8 contains work needed for V1 now, not just future LTV

**Severity: High. Location:** `docs/V1-DERIVATION-DRAFT.md:34`, `:110-116`, `:283`, `:333`, `:344`.

The future-obligation row sends “archived store in bundle (M8)” to T4 while C4/C6 already depend on historical trust anchors and authenticated DNSSEC time. M8 is not one indivisible T4 feature. The positive-control DNSSEC signatures overlap for only 1.6 days; the snapshot needs authenticated time inside all relevant signature windows (`prototype/PHASE3-REPORT.md:172-188`). A 72-hour receipt-anchor window does not ensure this. Enabling DNSSEC and seeing a resolver AD flag establishes neither offline historical validation nor timely preservation of the snapshot.

**Exact fix:** Split M8. Put historical trust-configuration identity, archived validation material, owner-name/key binding and authenticated snapshot-time/window checks under NEEDED-FOR-V1, C4/C6. Put continuing status capture/freshness and renewal under DESIGN-LEVEL. Define how the snapshot and manifest are anchored, including any additional proofs and temporal checks; distinguish author-evidence proofs from the receipt's own proof. Verify actual issuer-domain snapshots offline. Specify the trust configuration independently of adversarial bundle content; naming it does not mean blindly trusting a bundle-supplied store.

## 6. “Earliest attestation” does not prevent pruning from changing acceptance

**Severity: High. Location:** `docs/V1-DERIVATION-DRAFT.md:33`, `:129-130`, `:340`.

Earliest **presented and verified** attestation is the strongest existed-by bound in that presentation. It is not the earliest attestation ever produced, and the presenter can remove branches. The prototype explicitly records this effect (`prototype/PHASE3-REPORT.md:163`). For example, with declared=100, ε=24 and authentic attestations at 70 and 90, the earliest rule fails the lower window bound at 70; pruning that branch selects 90 and passes it. Thus “the only rule a presenter cannot game by pruning” is false. Pruning can also alter historical-authority/status comparisons.

**Exact fix:** Delete that claim. Specify whether the temporal property is existential over suitable authenticated anchors or deliberately presentation-sensitive. Register the selected interpretation, including selection order relative to header authentication, all three temporal conjuncts and trust policy. Add multi-attestation/pruned-proof companions at both window boundaries and for authority/status comparisons. If requiring a fixed complete attestation set, provide an authenticated commitment/completeness mechanism; do not infer completeness from an OTS file. Retain the honest non-claim: no priority or lower creation-time bound.

## 7. C5 and the latency statement conflate chain-time predicates with wall-clock guarantees

**Severity: High. Location:** `docs/V1-DERIVATION-DRAFT.md:33`, `:44`, `:270`, `:371`.

Adopted A2.1 says `confirmed_at` is the designated block-header timestamp, not the wall-clock instant depth k was reached (`docs/phase-0-prereg-amendment-2.md:185-206`). Header timestamps can be non-monotonic. C5's “confirmed ... within δ” suppresses this distinction. The observed 8.6–12.6-hour spacing between attestations is not a latency distribution. δ=72h bounds the acceptance predicate of one attempt; retries, propagation, signer availability and calendars do not yield an end-to-end 72-hour wall-clock SLA. The profile also omits the operational slack parameter S that the registered wall-clock attempt rule uses (`docs/phase-0-prereg-amendment-2.md:106-135`).

**Exact fix:** Say “the authenticated anchor and k-th confirmation header timestamps satisfy the registered three-conjunct consistency predicate.” State Bitcoin timestamp skew, canonical-history/checkpoint assumptions and deeper-than-k reorganization residual beside C5. Include S, its operational clock role and timeout/retry accounting in the ratified profile. Publish measured service latency separately from chain-time acceptance and a bounded refusal deadline. Replace “bounded by δ” with that distinction; say hours are expected, not established as an upper service bound by these observations.

## 8. PoW + linkage + a checkpoint is not a complete header-authentication specification

**Severity: High. Location:** `docs/V1-DERIVATION-DRAFT.md:125-138`, `:340`.

A2 requires header authentication against the canonical history, with pinned policy and conflict rules (`docs/phase-0-prereg-amendment-2.md:197-205`). The proposed done-line omits difficulty/retarget validation, checkpoint position/coverage and what establishes the accepted history. The prototype rejects segments crossing a retarget because it is unimplemented (`prototype/tessera_proto/real/btc.py:84-87`). Its checkpoint mode checks only the selected k-segment against an adjacent or internal pin (`real/anchor.py:85-91`). Merely meeting an attacker-selected `nBits` target is insufficient.

**Exact fix:** Freeze one implementable header policy and its exact limitations. Either distribute authenticated pins covering accepted histories, or specify the full path from the pinned checkpoint, mainnet difficulty/retarget checks, work/history assumptions and bundle/store conflicts. Add forged difficulty, retarget crossing, stale checkpoint, private extension, missing path and store-conflict cases. If unsupported histories return `UNVERIFIABLE`, state that availability limit and test the intended issuance path. Do not call the abbreviated rule complete or treat a regtest PoW check as mainnet authentication evidence.

## 9. C2/C3 exceed the evidence if read as concrete compromise resistance

**Severity: High. Location:** `docs/V1-DERIVATION-DRAFT.md:30-31`, `:73-94`, `:198`, `:308-310`.

The existential presentation boundary is right; submitter identity and replay suitability are correctly excluded. But “and so does a DSKS key” is broader than the existing modeled reattribution result. DSKS remained emulated in the real-mechanism prototype (`prototype/PHASE3-REPORT.md:147-152`). Symbolic binding of existing honest signed bytes does not prove arbitrary concrete stolen-key/fork resistance or that every signature necessarily originated at this API. KMS-backed OpenPGP signs an uninterpretable digest; independent key custody does not establish independent approval of content (`:116-141`). Two keys are also not two independent organizations.

**Exact fix:** State C2/C3 conditionally on the registered signing-key-use and cryptographic assumptions, with the modeled adversary scope named. Say the existing symbolic queries reject reattribution of the modeled existing signed bytes through the required key/frame bindings. Keep concrete fingerprint/hash/library/curve assumptions as H1a evidence, unless deliberately adding an earlier gate. Specify the KMS OpenPGP public-key packet, creation time/fingerprint, trailer processing and historical key-expiry handling before golden bytes freeze. Describe Q5 as preserving custody/failure-domain separation, not independent content authorization. Keep any concrete DSKS demonstration distinguished from the emulated probe.

## 10. C6 omits registered dead-project bundle content and a distinct reconstruction test

**Severity: High. Location:** `docs/V1-DERIVATION-DRAFT.md:34`, `:140-153`, `:208-225`, `:263`, `:349`.

A3.4 registers a signed verification-spec identifier **and hash**, the specification and conformance vectors embedded in each receipt as typed content-addressed objects, a bound purpose preamble, and a declared external-standards dependency closure (`docs/phase-0-prereg-amendment-3.md:290-364`). It separately registers dead-service and dead-project demonstrations (`:371-378`). “Bundle + published verifier + distributed trust configuration” can satisfy dead-service verification while losing dead-project reconstruction. A known verifier on a second machine does not test reconstruction without Tessera-specific context.

**Exact fix:** Carry these bundle obligations into the V1 format, P8/O-79 map, C6 evidence list, vector plan and 2106-examiner protocol. Test dead-service execution and dead-project reconstruction separately with recorded evaluation conditions. If any are intentionally removed, add individual omission rows and explicit A9 overrides; do not imply that preserving the published executable is equivalent. This is the most substantial missing commitment in the fourteen-row list.

## 11. Strict-only support is reasonable; the blanket out-of-profile verdict silently changes P4 precedence

**Severity: High. Location:** `docs/V1-DERIVATION-DRAFT.md:35`, `:46`, `:184`, `:253-255`, `:301`, `:313`.

Rejecting unsupported wrappers or waiver requests is an honest capability restriction. It does not justify overwriting a definite failed required check with `UNVERIFIABLE` whenever some other field is unsupported. Adopted A4.2 requires `INVALID` when one required check fails and another is unperformable (`docs/phase-0-prereg-amendment-4.md:88-109`). “Anything else gets UNVERIFIABLE” neither defines profile-dispatch scope nor preserves that rule. Missing required signatures and missing required authority evidence also have different registered meanings; d2/d3 cannot simply be lumped together without inspecting their actual inputs.

**Exact fix:** Define the outer profile-dispatch result separately from in-profile required-check aggregation. For recognized V1 objects, preserve FAIL-over-UNPERFORMABLE precedence. For unsupported profiles/layers, return a scoped unsupported assessment without asserting their validity. Distinguish an unsupported verification request from a fresh strict request over the same intact bundle. Add a mixed failed/unsupported case and missing-signature versus missing-evidence cases to E6a. If changing P4 itself, list a second explicit property weakening instead of claiming only P6 changes.

## 12. C7 is an acceptance test, not a consequence of typed verdicts; its offline and revocation instructions conflict

**Severity: High. Location:** `docs/V1-DERIVATION-DRAFT.md:35`, `:155-169`, `:256`, `:351`, `:369`.

A typed result makes distinctions expressible and testable; it does not by itself make a relying party's decision safe. In case e the proposed verifier deliberately accepts the bytes while not evaluating a fact that defeats authorization in the original construction. Telling the user to “check the issuer's revocation publication” introduces a current external source precisely where the offline claim promises no network. That advice may also be impossible when Tessera has disappeared. The prototype tests expose interpretation errors; they do not already establish non-expert success.

**Exact fix:** Define the safe decision for each scenario and each transaction question. For e: the base bytes/signature/publication/time checks pass; historical non-revocation is **not established**, so a transaction requiring it must not rely on that result alone. Describe external status checking as an optional stronger workflow, with authenticated evidence requirements and an explicit unavailable outcome. Phrase C7 as the December acceptance criterion until tested. Name the non-expert integrator, documentation-only conditions and scoring rule. A fresh model is useful additional evidence; replacing the scheduled non-expert integrator with it changes the adopted success proposal and must be explicitly ruled.

## 13. Changing expectations is insufficient: the ten scenario fixtures do not fit the proposed profile

**Severity: High. Location:** `docs/V1-DERIVATION-DRAFT.md:225`, `:250-257`, `:366`.

The actual a fixture includes a TLR; d1 uses that complete bundle under a degraded policy; d3 is an attacker clone with one signing key/one channel and its own TLR; f's original expected standing is also `ESTABLISHED` (`prototype/consumers/scenarios.py:72-117`). Under literal “no TLR, no waivers” the unchanged a/d1 bundles cannot simultaneously be V1 `VALID_STRICT`. Removing only a/e/h expectations misses these contradictions. The original wrapper attacks should remain unsupported-profile tests, not be erased. These prototype expectations are previously observed test artifacts, not registered original product obligations of the same kind as the other thirteen rows.

**Exact fix:** Register a V1 scenario mapping before V1 runs that gives, for every a,b,c,d1,d2,d3,e,f,g,h case: exact fixture transformation or preserved bytes, profile, verification request, expected base verdict, standing/status fields and safe decision. For d1 explicitly refuse the waiver request and separately evaluate a strict request. Preserve the original prototype scenarios/results as history. Include the real-mechanism mirror/authority attacks and model-derived vectors in the larger conformance set without pretending they prove universal user comprehension. Put the prospective test registration in its own category in the omission inventory.

## 14. The omitted-commitment inventory misses independent adopted obligations

**Severity: High. Location:** `docs/V1-DERIVATION-DRAFT.md:208-225`, `:274-288`, `:315-316`.

Beyond the bundle/reconstruction requirements in finding 10, the following require an explicit retained requirement or named override:

| Commitment omitted from the accounting | Governing evidence | Exact disposition needed |
|---|---|---|
| Service forward-link/successor-slot registration, comparison and slot-bearing golden vector **before format freeze**, independent of S-STANDING | `formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:159-206`; `docs/implementation-spec.md:651-656` | Retain that scheduled registration/vector, or explicitly defer this adopted pre-freeze obligation to a service-succession capability. Deferring TLR/standing alone does not defer it. |
| Signed/timestamped service review recency and staleness invariant | `docs/phase-0-prereg.md:564-572` | Name §4.7 separately. Retain the operational requirement or explicitly defer it; moving the §5 product done-line does not by itself withdraw this hard rule. |
| H3's standard-price cycle <$25, persistent footprint <$5/month, and idle compute $0 | `docs/phase-0-prereg.md:232-248` | Carry these as V1 operational acceptance/accounting requirements, or amend them individually. An unspecified monthly cap is not their substitute. |
| H1a break-chain attack | `docs/phase-0-prereg.md:203-205`; A9.5's rewritten suite | Keep break-chain attacks for retained receipt/authority/anchor chains. Only wrapper-specific instances can follow the wrapper deferral. |
| Custodial parameter-schema/clock-role ratification at Band 0 | `docs/phase-0-prereg-amendment-3.md:435-451` | Name its trigger change if moved with tending. Do not silently leave the original Band 0 timing operative while calling exit complete. |
| Full refusal-record decomposition and both atomic-entry/re-entry companions | `docs/phase-0-prereg-amendment-3.md:816-828` and A3.7.2 | Carry all of these to the named future capability, not only record/commitment text at :572-580. Keep V1's bounded local refusal behavior separately required. |
| The original numeric-domain rejection rule | `docs/phase-0-prereg-amendment-1.md:255-275`; prereg §4.3 | If “value-preserving” changes exact-double representability to decimal round-trip preservation, explicitly amend the accepted domain. Define what equality means for injectivity, including alternate JSON spellings. |

The independent-model red-bar/CI separation rule (`docs/phase-0-prereg.md:548-553`) and unloggable-key constraints remain retained operational requirements; the implementation plan must carry them even though they need not become extra formal exit gates. Likewise, moving the product done-line does not demonstrate the original PCI/scale/ownership objectives: mark those outcomes unfulfilled at V1 rather than claiming original project completion.

**Exact fix:** Add a source-to-disposition inventory covering these commitments, finding 10 and the existing fourteen rows. Use “retained now,” “trigger explicitly moved,” “withdrawn,” or “weakened”; do not infer disposition solely from a future-capability label.

## 15. Audit of all fourteen listed omissions: several citations and dispositions are incomplete

**Severity: Medium, with the substantive High defects cross-referenced. Location:** `docs/V1-DERIVATION-DRAFT.md:210-225`.

| Row | Review | Exact fix |
|---|---|---|
| 1, original §8 gate | Correct source; this is a replacement profile gate, not original H0 resolution. | Say original broader H0 remains unresolved; identify the new authorized V1 exception. |
| 2, capstone gate | Real obligation, but strict-only must account for retained divergent companions and withheld rulings, not just d's eleven. | Use full A3 filename; adopt the retained query/companion/disposition matrix described in finding 17. |
| 3, product done-line | Legitimate scope separation; does not dispose of independent §4.7/H3/primary objectives. | Add the independent dispositions in finding 14 and state original product success is not achieved by V1. |
| 4, H1a degradation | Honest removal of unsupported capability tests; rewritten suite also drops break-chain. | Retain applicable break-chain tests; explicitly relocate only degraded/wrapper cases. |
| 5, H1b | Explicit prospective withdrawal is understandable, not evidence of falsification or success. | Retain the recorded withdrawal and original hypothesis history. |
| 6, P6 | Incomplete weakening and superseded temporal citation. | Cite full A1 path plus A4.3; amend both authorization/status conditions as in findings 2–3. |
| 7, production PQ | Correct if V1 is expressly a demonstration, not the registered production version. | Use full A3 path and preserve that production trigger. |
| 8, standing | Deferring the mechanism/model is real; the orthogonal invariant is still satisfied by honest `ABSENT` reporting. | Separate omitted standing capability/model gate from retained assessment separation. Cite `formal/spike/FIRST-LINK-SPIKE.md` and full A3 path. Disclose the authentic-but-abandoned artifact residue. |
| 9, refusal record | Correct direction, incomplete source/obligation. | Cite the complete A3.7.2 decomposition plus :816-828, including delivery/publication/retention and both companions. |
| 10, lifecycle | Actual trigger is before **H1a crypto-core freeze**, deliberately not Band 0 exit. Draft identifies the V1 profile freeze with H1a while the exit opens H1a later. | Distinguish 30 October format/profile freeze from subsequent implemented crypto-core freeze; explicitly override the lifecycle trigger for the reduced capability. |
| 11, renewal | Correct non-offering; an independent custodian can later renew. | Say V1 offers no renewal protocol and no wrapper interpretation. Keep conditional custody/algorithm dependencies and future inner-verdict preservation tests. |
| 12, local GPG | Proposed outside-AWS placement preserves the intended custody distinction. | Carry its availability/queue/key-use requirements; if AWS placement is chosen, explicitly amend independence. |
| 13, A8.4 edits | Genuine trigger change, but contradicts “A8 unchanged.” | Cite full A8 path/section and list exactly which clauses are postponed. |
| 14, prototype expectations | Wrong category and incomplete fixture changes; missing file path. | Cite `prototype/consumers/scenarios.py:72-133`, register the full V1 mapping prospectively, and preserve prior tests/results. |

Every `amendment-N.md` shorthand in this table should be replaced with the actual repository path, using the pattern docs/phase-0-prereg-amendment-N.md. They are not files at the paths currently given. References to a named section can supplement, not replace, the precise source of the changed obligation.

## 16. Full classification audit: phase, substance and evidence are being mixed

**Severity: High. Location:** `docs/V1-DERIVATION-DRAFT.md:175-206`, `:259-288`.

NEEDED-FOR-V1 should mean required by the offered claim/capability, not necessarily required before starting implementation. PROCESS is still mandatory when it is an adopted review gate. The following audits every row; proposed design deferrals are conditional on a complete adopted A9, not effective already.

| Draft row | Correct classification / correction |
|---|---|
| E1 P1–P5/P5c/P7-type/P10 | NEEDED-FOR-V1 formal evidence, with exact retained query scope. Preserve P4 precedence, operational refusal bounds and all temporal conjuncts. |
| E1 P6 | DESIGN-LEVEL full-status/LTV mechanism; the explicit removal from V1 validity is a weakening, not accomplished by classification alone. |
| E2 SC | DESIGN-LEVEL standing mechanism after explicit trigger change. Retain honest orthogonal absence reporting. |
| E3 P8 | NEEDED-FOR-V1 and appropriately pre-format-freeze. Include both frames, receipt preimage, signed spec binding and numeric domain. |
| E4 P9 | NEEDED-FOR-V1; separate prospective design inspection from actual verifier inspection/dead-service execution. |
| E5 strict a/b/c | NEEDED-FOR-V1 scoped capstone evidence; c is the compromised-both-channels negative control, not a successful authority guarantee. |
| E5 d/slices | DESIGN-LEVEL degraded evidence; completing a running batch is record housekeeping, not V1 closure. Single-channel-capture resistance is already in strict a/b, so “after-capture guarantee” is too broad a capability name for d. |
| E6a | NEEDED-FOR-V1 fail-closed transition, with precedence and correct dispatch scope. |
| E6b | DESIGN-LEVEL portable/public refusal construction. Basic bounded, durable local refusal remains NEEDED-FOR-V1 operated issuance behavior. |
| E7 | PROCESS, required for retained queries. |
| E8 | NEEDED-FOR-V1 correspondence argument; not machine-checked composition by itself. Name actual producer/consumer checks and residual implementation gap. |
| E9 | PROCESS, mandatory for the retained gate. Batch the reading, not disposition of unresolved findings. |
| E10 | NEEDED-FOR-V1 H1a conformance evidence. A1.7 puts extraction in H1a; extraction at Band 0 is BAND0-EXIT reading (b), not a separate registered amendment requirement. Explicitly change that reading if extraction moves to November; keep P8's layout-fixing vectors before format freeze. |
| E11 | PROCESS: required proof index/traceability. It is not the C6 offline dependency evidence. The embedded normative spec belongs to C6. |
| E12 | NEEDED-FOR-V1 relying-party interpretation and acceptance test. |
| E13 | PROCESS, refresh for the reduced profile, publish excluded/open cells rather than label all coverage done. |
| E14 | NEEDED-FOR-V1 declared parameters plus PROCESS ratification. Include S and distinguish clock roles. |
| E15 | PROCESS, still requires recorded author disposition of the first-link residual. E9 can host that act but does not close it automatically. |
| E16 | NEEDED-FOR-V1 implementable profile. A 400-line ceiling is an editorial preference, not an acceptance requirement. |
| E17 | PROCESS, signed reduced-profile exit; not discharge of unoffered capabilities. |
| E18 | NEEDED-FOR-V1 depth evidence; reviewer sign-off is PROCESS. Include it explicitly in A9.2 rather than listing it as merely procedural. |
| P3 assumption half | NEEDED-FOR-V1 concrete H1a evidence. Moving it earlier is an added exit gate, not required by the registered phase placement; justify or keep it at implementation acceptance. |
| A2.2 vector cases | NEEDED-FOR-V1 temporal/header conformance evidence; declare specification/extraction/execution milestones separately. |
| W1 in S-STANDING | DESIGN-LEVEL when standing is absent; signature-independent V1 identifiers and argument about retained strict queries remain NEEDED-FOR-V1. |
| Integrated lifecycle | DESIGN-LEVEL full lifecycle after an explicit trigger override. P5c plus strict capstone is complementary evidence, not a checked integrated issue→refuse→verify adversarial model. Do not introduce that new reduced integrated-model gate without deciding it is needed. |

**Exact fix:** Rebuild the table with columns for capability, classification, original deadline, V1 deadline, evidence type and A9 override. Remove catchall “A9.3 list” from the count: the displayed rows contain six DESIGN rows, not seven independent rows. Recount after reclassification. Keep the slice-batch read and future T4 construction off the V1 critical path. Remove the “worthwhile only if T4 ... is real” condition at :370, or explicitly adopt it as a new V1 gate; as written it reintroduces the deferred ambition through the value judgment.

## 17. “173/173 strict verdicts” misstates the capstone record and hides outstanding strict evidence decisions

**Severity: High. Location:** `docs/V1-DERIVATION-DRAFT.md:85`, `:182`, `:265`, `:354`.

The results section's correct-form table covers four configurations, including d and case c's negative-control role (`formal/suite/capstone/RESULTS.md:167-173`); these are query outcomes, not 173 issued-receipt verdicts. Counting its as-registered rows gives a=47, b=47, c=35, d=44: the strict a/b/c subset is 129 rows, not 173. Its summary separately records 69/80 files landed, 56 companion configurations as registered, 10 divergent, 11 not run under the current blob, and withheld C-C15(i) C-Q6 results pending author ruling (`:5-9`). All strict files landing does not dispose of every strict companion/query issue. Amendment 8's existence in git is not capstone discharge.

**Exact fix:** Quote the result categories accurately. Supply a retained V1 query/companion matrix keyed to the exact ladder-3 blobs, including expected red/green polarity, divergent outcomes and pending rulings. For each excluded standing/degraded/wrapper query, say why it cannot support or defeat C1–C7. For each retained divergence, record author disposition or repair and any required rerun. Do not promise “no further capstone work” before that classification and the strict signature-malleability argument are reviewed. Keep “no row discharged” until the actual row-specific prerequisites are met.

## 18. A9 does not implement its stated gate, and “unchanged” misdescribes its supersession

**Severity: High. Location:** `docs/V1-DERIVATION-DRAFT.md:260-272`, `:276-288`, `:312-316`.

A9.2 omits E18/full-depth review, the table's newly early P3 assumption gate and an explicit disposition of E10 reading (b). Conversely, the work plan says all V1 rows will be discharged even where implementation evidence is deferred. A9.3 says items retain their original text while moving deadlines originally tied to Band 0/H1a; retaining text without an explicit supersession leaves contradictory triggers. “A8 unchanged” conflicts with postponing its A8.4 query/spec obligations. “No other registered sentence is struck” is technically evasive when gates, demonstrations and triggers are being replaced. The change may be warranted; it must be reconstructible.

**Exact fix:** Give A9 a clause-level supersession table: source clause, old trigger/condition, V1 replacement, retained future trigger, and kind of change. Distinguish (1) property weakening, (2) removed offered capability, (3) evidence/gate reduction, (4) hypothesis withdrawal, and (5) changed test registration. Enumerate the actual pre-Phase-1a gate and the later H1a/December acceptance gates. State that original H0/capstone/design obligations are not globally discharged. Use “A8 remains the source record; these specified obligations are postponed for V1” instead of “unchanged.” Batch author review only after reviewers' surviving counterexamples have concrete dispositions.

## 19. The 30 October plan is not credible as an unconditional completion plan

**Severity: High. Location:** `docs/V1-DERIVATION-DRAFT.md:331-359`.

The date can remain a ceiling. The present effort sum is not a dependency schedule. Parallel agents cannot remove the serial dependency profile decisions→two-frame/preimage encoding→P8 vectors/proof→conformance/correspondence/reviews→author adjudication→signed exit. Nor can they provide actual P9 inspection evidence for code not planned until November. Marking all V1 rows `discharged` on 27 October is wrong where P3 assumptions, code inspection or conformance execution remain outstanding.

Specific underestimated items:

| Item | Why the estimate is insufficient | Exact planning fix |
|---|---|---|
| Review/disposition, 0.5 day; A9 ruling, 1 hour | This amendment still has substantive claim/trigger/test choices beyond clerical edits. | Budget a revised draft and independent re-review before signature; keep a routed decision inventory within the author's budget. |
| Git channel, 2 hours | Current verifier lacks full path validation; publication semantics and historical trust-key rules are unsettled. | Include format/tests/full offline verification or reduce the claim explicitly. |
| DNSSEC, 1 hour + propagation | Offline chain capture and authenticated snapshot time are required, not just zone activation. Snapshot validity can be shorter than δ. | Add capture/anchor/refresh validation and registrar contingency, with an observed overlap-window criterion. |
| Profile 2 days + P8 4 days | Numeric-domain choice, OpenPGP fingerprint/metadata, two-frame preimage and embedded spec binding affect the bytes under proof. | Settle these inputs first; timebox proof plus independent counterexample review with explicit failure outcome. Four days is an estimate, not existing evidence of tractability. |
| Spec fixes, 2.5 days | Includes header authentication and temporal/authority semantics, not only sentence edits. | Separate policy choice, implementation consequence, registered model/vector consequences and independent review. |
| E6a, 0.5 day | Profile dispatch plus mixed-failure precedence needs a defined claim before its companion is meaningful. | Specify the partition/witnesses and then size modeling/review. |
| P9 inspection, 0.5 day | No frozen V1 verifier exists at this milestone. | Inspect the prospective dependency contract at exit; inspect actual code and run the two-machine/dead-service tests at H1a, leaving implementation status open until then. |
| E8/E7/E11, 2 days | A correspondence argument must account for the actual retained joins, not simply index green models. | Name each join and severing evidence or explicitly declare the remaining unproved composition; schedule review after the profile settles. |
| Author E9, 2 hours | Full surviving findings plus newly completed P8/P9/E6/E8 work cannot be assumed to fit one sitting without a prepared decision surface. | Prepare the concrete row-by-row packet early and budget unresolved decisions/re-review; do not use the time limit to waive evidence. |

**Exact fix:** Publish a dependency schedule with parallelizable work, named owners, latest start/finish dates and explicit fallback outcomes. Preserve the accepted 30 October profile milestone, but distinguish formal/profile exit from implemented evidence. If the critical path misses, apply the already stated cut-or-stop rule. Move design-batch housekeeping off that path. Do not add new integrated models, full LTV or original product gates merely to answer this review.

## 20. Long-horizon assumptions are understated, and no-wrapper support needs a precise future-compatibility boundary

**Severity: Medium. Location:** `docs/V1-DERIVATION-DRAFT.md:42`, `:222`, `:283`, `:303-305`, `:370`.

ECDSA P-256 and SHA-256 are not the whole dependency set. The archived repository construction links the OTS-stamped commit ID to its contents through SHA-1; DNSSEC chains may use RSA/SHA-256 and ECDSA; OpenPGP fingerprints/packet semantics, historical trust anchors and Bitcoin history are also material (`prototype/PHASE3-REPORT.md:181-202`). Retention alone does not preserve authority when those assumptions fail. Strict-only and no wrappers are honest non-offerings, but “later renewal ... never alters its verdict” is scoped to the unchanged inner assessment, not a guarantee that every future verifier/trust policy produces identical results.

**Exact fix:** List the actual V1 dependency/assumption manifest with exact algorithms, formats, trust configuration and historical-time interpretation. Say no renewal/standing service is offered by this profile, while independent custodians may preserve or renew its bytes under later protocols. Require later wrapper support to preserve the inner V1 assessment under identical declared inputs and report outer/LTV assessments separately. Do not present that future implementation property as already checked. State the shelf-life dependency plainly without making delivery of T4 a hidden V1 condition.

## 21. Preserve the sound boundaries, while correcting current-evidence language

**Severity: Medium. Location:** `docs/V1-DERIVATION-DRAFT.md:21-46`, `:52`, `:365-371`.

The draft is right to exclude payload truth, submitter identity, transactional replay suitability, lower-bound creation time, priority, domain-holder honesty, complete-author-sphere compromise resistance and standing when no standing evidence is issued. It is right that omission of mandatory status checks requires an amendment; unavailable required checks cannot quietly become a valid result. It is right to keep dates separate from definition adoption and to avoid treating the formal foundation as an operated service.

Those truths do not establish a deployed V1. “Formally grounded, offline, fail-closed verification” describes the intended bounded construction and existing model-local evidence; concrete implementation conformance and relying-party safety remain future tests. The unsigned issuer-domain observation is recorded on 7 October, not a live 9 October DNS measurement. “Says nothing useful” for an `UNVERIFIABLE` receipt is also too strong: it can expose successful byte/signature/time checks while refusing an overall authorization verdict.

**Exact fix:** Keep the explicit non-claims and status vocabulary. Date the DNS observation. Replace the present-tense delivery assessment with “V1 would demonstrate these checks if the listed formal/profile evidence and implemented acceptance tests pass.” Describe `UNVERIFIABLE` as an incomplete overall claim with useful scoped check results. Make the verdict and documentation identify the offered profile, evaluated dimensions, omitted dimensions, temporal semantics and assumptions directly. No liability hedge is needed: state exactly which facts the artifacts establish and which have not been tested.
