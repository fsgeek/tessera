# Tessera — Phase 0 Pre-Registration, Amendment 11 — P3's verification profile as a floor and a duty; dependency sweeps; consistency repairs; the slot-2 boundary (DRAFT, 2026-10-29)

> **Status: DRAFT by the owner instance (Claude Opus 5.5). Not signed.** This is one consolidated consistency
> amendment. It was revised after the Codex non-author review and its confirmations
> (`docs/reviews/amendment-11/CODEX-REVIEW.md`, `CODEX-CONFIRM*.md`; `DISPOSITION.md`), then consolidated after
> Levadura's consistency panel (obs-0185; `/home/tony/projects/levadura_salvaje/docs/tessera-a11-canary-scorecard.md`).
> The panel's finding ids (c002 to c147) are cited where they apply. The author's first commit containing the final
> text is its signing act. Layered on the original and Amendments 1–10, none of which is edited. Every registered
> sentence this amendment changes is listed in §A11.3. One choice (§A11.5 item 2, the slot-2 custody reading)
> is recorded as an owner decision, Option 1, which the author's signature adopts. It is a retrospective relaxation,
> disclosed below.
>
> **Outcomes informed this amendment** (the original's amendment rule). Each change is disclosed separately.
> - **§A11.2, P3.** The P3 evidence (`formal/p3-verification-profile/`) was built and reviewed before this text.
>   Building it exposed the stale checklist. No P3 result failed and is relabelled here. The floor's shape is the
>   author's proposal of 2026-10-28.
> - **§A11.5 item 2, the slot-2 boundary.** Option 1, the owner's decision adopted by signing, is a **retrospective
>   relaxation** of a deadline-qualified restriction. It is made after the 21 Oct deadline, and after the candidate code
>   (`service/signer-gcp/`) was written and reviewed.
> - **§A11.5 item 5, K-R's enforcement.** The owner's placement decision (2026-10-27) moved KMS signing from the
>   issuer role to a dedicated policy signer and said it changed no registered sentence. It changed the
>   supplement's description of who computes μ and who may sign. The confirmation review found this.
> - **§A11.5 item 3, the spike keys.** The owner's deployment draft had contradicted a registered commitment. That
>   draft is withdrawn. This amendment does not change the spike-key sentence.
> - **The Levadura panel.** It found that this amendment's own K-R change committed §A11.1's defect class three times
>   (scorecard:9-13). The first draft's K-R row left ENCODING-V1 §5.2, the supplement's §1, and the supplement's
>   §11 item 6 naming the issuer as the KMS caller, and §A11.5 item 3 called item 6 "unchanged". The K-R row in
>   §A11.3 now lists all seven locations.
> - **The owner's sweep.** It had not read the frozen specification (`spec.bin`: A9, A10, PROOF, V1-PROFILE,
>   ENCODING-V1, the hybrid supplement; `formal/freeze-v1/FREEZE-RECORD.md:16`) beyond profile §8, nor the hybrid
>   supplement (`docs/reviews/stale-dependencies/SWEEP-2026-10-28.md:3-4`, `:20-21`; scorecard:15-16). Most of the
>   panel's rows below are in that text.

## A11.1 What went wrong

P3's assumption half (A1 §P3, `phase-0-prereg-amendment-1.md:144-148`) requires the verification profile to record
the *exact library and version, accepted signature encodings, public-key validation behavior, low-order-point
handling, cofactor equation variant, and negative test vectors for each*. Two of those fields name concepts of
Ed25519-style curves, which A1 used as its example (`:136`). V1 later registered OpenPGP P-256 and then, on
2026-10-16, the hybrid ML-DSA-65 + P-256 (`formal/p8/HYBRID-REGISTRATION-RECORD.md`). Neither registration re-read the
checklist.

For ML-DSA, the two curve fields have no referent. The other four fields still apply in full. So the checklist
names nothing specific to ML-DSA's own verification pitfalls: it **demands too little**. Nothing had been accepted
on it. The assumption half was open (`formal/PROPERTIES.md:37`) and due after the freeze
(`formal/freeze-v1/FREEZE-RECORD.md:81`).

The method's defect: **a registered decision can change what an earlier registered sentence refers to, and nothing
requires anyone to re-read that sentence.** §A11.4 adds that duty.

## A11.2 P3's verification profile: floor and duty

**The proofs are unchanged.** P3's model half assumes a verifier with stated behaviour. The assumption half is
bounded implementation evidence that the shipped verifier has that behaviour. It does not show that every model
assumption is preserved in general.

1. **Fields kept.** All six of A1's fields stay. For each algorithm in the governing specification they are read as
   follows:

   | A1 field | ECDSA P-256 (rule O) | ML-DSA-65 (rule R) |
   |---|---|---|
   | exact library and version | `cryptography` and its bundled OpenSSL, identified by wheel tag and native-library SHA-256 | same |
   | accepted signature encodings | OpenPGP v4 packet; MPI rules; r, s ∈ [1, n−1]; rule-O policy | exact 3309 bytes; strict hint and z encoding |
   | public-key validation | exact uncompressed point; coordinates < p; on the curve; checked before the library | exact SPKI; no algebraic validation exists |
   | low-order-point handling | cofactor 1: infinity rejected as a key and as the equation's result; invalid-curve points rejected | no referent. Replaced by: degenerate-key behaviour recorded |
   | cofactor equation variant | cofactor 1: a single variant; x(R) reduced mod n | no referent. Replaced by: the FIPS 204 interface (pure, empty context), with every other interface rejected |
   | negative vectors for each | owner vectors plus Wycheproof | owner vectors plus Wycheproof |

2. **Floor (registered).** The evidence is the files listed in
   `formal/p3-verification-profile/FLOOR-MANIFEST.sha256`, whose SHA-256 is fixed at signing. At this draft it is
   `844cb7ff8df59f047d2ea48536ddb30bad5b3e93684acbce6a4dad1241aee42d`, covering 15 files. They hold:
   - the owner harness (`test_p3_profile.py`): 123 owner vectors (F2 65, F3 37, F4 8, F5 13; PROFILE.md:22-25) in
     224 tests, 223 passing. `test_deployed_zip_identity` is skipped until a deployed package is supplied
     (PROFILE.md §8, :274-281). §6 mutates nine verifier checks, and removing each one turns tests red
     (PROFILE.md:243-258);
   - Wycheproof commit `d17cc89fa5c8f4f4d378b5385ebf75da5d0926c9`, three files pinned by SHA-256: 968 tests.
     - **ML-DSA-65** runs end to end through the verifier. Two disagreements, tcId 3 and 4, are V1 policy (empty
       context only).
     - **ECDSA P-256** runs through the verifier's key validation, MPI rules, range policy and verification, with
       the digest substituted. 219 non-strict DER cases are tested at library level only. 21 P1363 strings of the
       wrong length reach neither interface. There are no disagreements.
3. **Discharge.** Adopting this floor is not discharging P3. P3's assumption half is discharged only when:
   - (a) the manifest verifies;
   - (b) every test in it passes;
   - (c) the exact deployable zip produced by the recorded `service/issuer/package.py` build is retained with its
     SHA-256. Its verifier files are byte-identical to the tree the passing floor run exercised, and its
     `cryptography` binding and wheel tag match F1. After deployment, that zip's SHA-256, base64-encoded, matches
     AWS's `CodeSha256` for every function to which the discharge applies (`test_deployed_zip_identity`). The
     record names the source and test inputs, the packager, the archive digest, the AWS functions and the
     comparison result. This establishes deployment-package identity under the recorded build and AWS's reported
     digest. It does **not** assert that ZIP extractors agree on an archive's contents: they can disagree, and
     Lambda's extractor is not publicly documented (`docs/reviews/amendment-11/CODEX-CONFIRM-3B.md`). The
     packager writes fresh canonical entries, which is what limits that exposure;
   - (d) no disagreement or finding affecting a required behaviour is unresolved. A recorded defect blocks
     discharge until it is fixed and re-tested.
4. **Operational duty (not a registered result).** The floor's checks, and the latest published vectors for each
   algorithm in use, are re-run when one of the following happens. Each trigger states what it detects. Each run is
   recorded with its date, inputs and outcome, and attested by the operator.
   - **The tested code changes** (a verifier release, or a change to the signature library's version or build). This
     is required, not chosen: the floor's evidence is bound to specific bytes (the manifest hash and F1's wheel
     digest), and other bytes are not covered by it.
   - **The published vectors for an algorithm in use change** (new or changed Wycheproof files for ML-DSA-65 or
     ECDSA P-256/SHA-256). This catches new public knowledge of verification pitfalls. Commits that touch other
     algorithms are not triggers.
   - **A published advisory or erratum names the signature library, its bundled OpenSSL, or a standard in use**
     (FIPS 204; the OpenPGP or ECDSA specifications V1 cites). This catches new knowledge that never reaches the
     vector suite.
   - **A calendar backstop, at least every three months.** This is an operating guess, not a derived interval: it
     covers sources the triggers above do not watch. After a year of run records, the owner reviews whether any run
     found something the event triggers missed, and adjusts the interval on that evidence.
5. **What a later finding changes.**
   - **A security-policy finding** (an algorithm, parameter or key later judged weak) never rewrites a V1 verdict.
     It reaches relying parties as a historical-security result, beside the verdict and its stable fields
     (A9.4, `phase-0-prereg-amendment-9.md:267-283`).
   - **An implementation-conformance defect** (the verifier disagrees with the governing specification, for example
     by accepting a malformed or prohibited case the specification rejects, A9:278) is not preserved as V1
     behaviour. It is fixed in a signed release, which names the affected releases and says what changed. A silent
     change to the verifier is never permitted.

## A11.3 Registered sentences changed

Profile locators are at the frozen commit `270ca49`. The live `docs/V1-PROFILE.md` is byte-identical to it. Kinds
follow A9.7. In rows 3, 4, 7 and 8 the "Was" cell spans several passages, so it is a paraphrase; only the words in
quotation marks are exact.

| # | Source | Was | Now |
|---|---|---|---|
| 1 | `phase-0-prereg.md:401-404` (c147) | "KMS/GPG domain separation (§3.1) reduces correlated compromise; … the §4.2 threat model and TTL bound the local-key blast radius" | (V1) "separate technical custody domains under a single controller (C3 non-claim, A9:449-453); OpenTimestamps constrains backdating; the slot-2 key is non-exportable hardware outside the issuing AWS account (A9.6, A9:375-376), which prevents key export, not misuse; there is no local service key in V1". Kind R, beside A9.7 row 15 |
| 2 | `phase-0-prereg.md:640-643` (c111, §6 restatement) | "Rejected in favor of dual-signing (C) across independent failure domains" | (V1) as A9.7 row 15 (A9:479): narrowed to C3's non-claim, separate technical failure domains under a single controller, with no separation of control or independent fates (A9:449-451). Kind R, row 15 extended |
| 3 | `phase-0-prereg-amendment-1.md:144-148` | the six fields, the two curve fields named in Ed25519's terms | the six fields as read in §A11.2 item 1; the floor and discharge conditions of items 2–3 |
| 4 | `phase-0-prereg-amendment-1.md:182`, `:494-495`; `phase-0-prereg-amendment-2.md:111-112`, `:268-269` (c032) | δ, ε (and k, N, S) "ratified (or revised, on the record) at Band 0 exit" | for `tessera-v1-strict`: ratified by the author's signature on A9 (A9.2, A9:223-225: δ = 72 h, ε = 24 h, k = 6, N = 3, S = 24 h). Outside V1: unchanged, still at Band 0 exit. Kind G |
| 5 | `phase-0-prereg-amendment-1.md:444-448` (c023) | "at issue time, two channels with independent operational failure modes asserted the same key authority"; "tampering with both external channels, at or before issue time" | (V1) "two channels asserted the same key authority at their evidence times (A9 C4): the git assertion by chain order before the receipt's anchor; DNSSEC at the snapshot's own anchored time, which establishes no publication before issue (A9:143)". Kind W, already in effect from A9's signature and listed late here |
| 6 | `phase-0-prereg-amendment-2.md:299-301` (c007) | "(the OTS proof over its canonical bytes)" | (V1) "(the OTS proof over `SHA256(A_sig)`, which commits to both frames and their exact detached signatures, A9.5)" (A9:290-292). The rest of A2.4, including one proof per receipt and the txid as identity handle, is unchanged. Kind K, as A9.7 row 24 (A9:488) for the sister sentences |
| 7 | `phase-0-prereg-amendment-9.md:389-392`; `270ca49:docs/V1-PROFILE.md:1017-1040` (custody record, :1024-1025, :1033-1040) and `:1428-1436` (§14.2 item 5) (c062) | the boundary as "the selected, deadline-qualified custody implementation", described through `prototype/policy-signer/` with its 2026-10-14 evidence | **Option 1 (§A11.5 item 2; owner decision, adopted by signing).** The deadline qualification attaches to the selected custody option and boundary, and the named replacement `service/signer-gcp/` runs under conditions (i)–(iv). *(Option 2, not taken: these sentences unchanged, and the registered fallback, A9:372-374, taken.)* |
| 8 | `phase-0-prereg-amendment-10.md:443-447`, `:449-457`, `:462` (A10.4 option (e), A10.4.1); A10.7 rows 25–33 and 37–39 (`:761-769`, `:773-775`); the plain-language summary `:106-124`, the additions list `:213-226`, the row-26 note `:432`, the closing summary `:795-799` and the reconciliation item `:810-812` (c018, c103; A11X-02, A11XC-01) | option (e) AUTHOR ADOPTED with A10.4.1; the listing cut only "for schedule reasons" (`:455-456`); "rows 25–33 and 37–39 only on (e)" (`:446-447`) | (V1) option (e) is narrowed by the author's E9 row 2 ruling of 2026-10-23 (`docs/reviews/e9-packet/AUTHOR-RULINGS.md:5-12`). It is an author scope decision, not the schedule cut order. A10.4.1 and rows 25–32 and 37–39 do not apply to V1. The passages at `:106-124` ("Key substitution: option (e)", "the limits", "time"), `:213-226` (the listing's field, check, reason codes and invariants) and `:432` describe the listing as a V1 mechanism. They are kept as the dated record of the 2026-10-18 adoption, with the author's words, and are superseded as descriptions of V1: in V1 no verifier rejects a receipt for keys missing from a list, no listing pre-commitment or listing-evidence preservation duty exists, and after capture of both authority channels a receipt under the attacker's own keys passes (`docs/V1-CONTRACT.md` §2 after G10, §4). The closing summary's listing mechanisms and "option (e) deliberately rejects new cases: receipts under unlisted keys, and receipts whose listing was not pre-committed" (`:795-799`) are superseded for V1 in the same way, and the listing parts of the reconciliation item at `:810-812` (the listing-evidence package, the listing subchecks and their total-order rows, the C0/C1 bootstrap) are withdrawn as V1 work. Every other mention of A10.4.1 in A10 (the status block `:13-28`, the author's quotations `:273` and `:620`, the "no longer open" note `:805`, and the mechanism section `:462-611`, all of A10.4.1) is the dated record of the adoption or the mechanism text itself, superseded for V1 by this row. The frozen copies in `formal/freeze-v1/objects/spec.bin` are covered by the same disposition; their bytes are not edited. The owner grepped every registered and frozen text for the listing's vocabulary on 2026-10-29, and no other mention remains undisposed. Release-key custody (A10.4.2) is separate and unchanged. Option (a) applies (rows 15–16). A10.4.2 (rows 34–36) is unchanged. Row 33 stands as registered cut-order text, since (e) is narrowed, not withdrawn. Its "second item cut is the service-key listing" has no referent in V1. Its other sentences (option (a) applies, the absence of new-key protection is stated, no cure for release-key independence) are met by the ruling and profile §5 (`270ca49:docs/V1-PROFILE.md:619-623`). Profile :619-622 and :1258-1262 are then consistent as written. Kind C/W, recorded here because no signed change table lists it |
| 9 | `phase-0-prereg-amendment-10.md:675` | "as amended by rows 15 and 25" | "as amended by row 15" (row 25 does not apply to V1; row 8 above) |
| 10 | `formal/p8/PROOF.md:134-135`, `:485` (c088; A11X-04) | :134-135 "no V1 check reads them"; :485 "No check reads it, and B never computes it." | "no V1 check relies on them as a hash or for key selection: the profile checks only their structure (length, version octet, consistency with type 16; V1-PROFILE §8, `270ca49:docs/V1-PROFILE.md:1105-1107`) and never compares them with the transported key". At :485, "No check reads it" becomes "No V1 check relies on it as a SHA-1 value; the profile validates its structure only (as above)"; "B never computes it" stays, as a statement about implementation B. Assumption (H) is unaffected: SHA-1's properties are not relied on. Kind K |
| 11 | `formal/p8/ENCODING-V1.md:334` (c002, §3.2 `alg` row) | "The id names the scheme: 'a v4 OpenPGP binary-document signature whose document is the frame, ECDSA P-256, SHA-256' (G-57 kept)." | "An id names its scheme. The classical id `OPENPGP4-ECDSA-P256-SHA256` names 'a v4 OpenPGP binary-document signature whose document is the frame, ECDSA P-256, SHA-256' (G-57 kept). The pair id V1 issues (`:322-323`) names ML-DSA-65, pure mode, empty context (rule R) in slot `kms` and that OpenPGP scheme (rule O) in slot `gpg` (§5.2; HYBRID-SUPPLEMENT §1)." Kind K |
| 12 | **K-R.** `formal/p8/HYBRID-SUPPLEMENT.md:61-64`, `:152-153`, `:173-174`, `:524`, `:533`, `:274-276` (the supplement's copy of the E§5.2 replacement text); `formal/p8/ENCODING-V1.md:557-559` (c004, c008, c011, c097, c108; A11X-01) | :61 "it is the issuer's only path"; :63-64 "the issuer always computes `μ` … and sends `μ`"; :152-153 "Every issuer KMS `Sign` call on the key is `MessageType EXTERNAL_MU`, with `μ` computed by the issuer from such an `F`"; :173-174 "(K-R) is an issuer-code and IAM assumption: the key policy grants `kms:Sign` only to the issuer role, and the issuer code builds only V1 frames"; :524 "the issuer always uses EXTERNAL_MU for the kms slot, attestations and possession alike"; :533 "`kms:Sign` only for the issuer role"; ENC:557-558 and its copy at supplement :274-275 "The issuer obtains `S_kms` (attestation and possession) from KMS with `MessageType EXTERNAL_MU` only, sending μ" | In each sentence, the actor that computes `μ` and calls `kms:Sign` is the KMS-slot policy signer (`service/signer-kms/`). It runs in the issuing AWS account under its own IAM role. It computes `μ` only from an `F` it has validated: tag, alg, key fingerprint, ε (attestation frames only; manifests carry no declared time, HYBRID-SUPPLEMENT:495), `sign_by`, the signing stop (`service/signer-kms/tessera_sign_kms/signer.py:176-185`). Its role is the only `kms:Sign` principal, and the issuer roles hold no KMS permission (`service/signer-kms/infra/main.tf:33-34`; `service/issuer/infra/main.tf:181`). :173-174 reads: "(K-R) is a signer-code and IAM assumption: the key policy grants `kms:Sign` only to the KMS-slot policy signer's role, and that signer signs only V1 frames it has validated." **The (K-R) restrictions are unchanged** (:151-153, :157): the key signs only V1 tagged strings, in pure mode with the empty context, and is used by no other protocol or service. Only the actor that enforces them changes, so the wording of :152-153 changes as stated. The historical capture labels "selected issuer path" and "issuer-computed μ" (:76, :353, :412, :478) describe the 2026-10-13/14 captures and still fit (A11X-01, A11X-05). EXTERNAL_MU only, for attestations and possession alike, is unchanged. The verifier side is unchanged. Kind R |
| 13 | `formal/p8/HYBRID-SUPPLEMENT.md:154-155` (c121) | "They satisfy the same assumption, because the message is a V1 tagged string." | "The genuine-frame RAW captures (SIG-G1, P-G1) satisfy the same assumption. SIG-H5 (RAW) and SIG-H6 (EXTERNAL_MU) were made over spike frames tagged `tessera-v1/receipt`, which is not in T (:344-345), under the spike key. That key is never a production key and is deleted under §11 item 6 (§A11.5 item 3), so (K-R) for the production key is unaffected." Kind K |
| 14 | `270ca49:docs/V1-PROFILE.md:1244-1245` (c041, d3) | "one attacker key in both slots, honest DNS evidence, `git` absent: `INVALID / DNS_KEY_MISMATCH` (row 15.1)" | "Under the pair id: the attacker's own key of the right type in each slot (ML-DSA-65 SPKI in kms, P-256 v4 body in gpg; :1064-1065), with consistent manifest, possession and signatures, honest DNS evidence, `git` absent: `INVALID / DNS_KEY_MISMATCH` (row 15.1), dominating `UNVERIFIABLE / MEMBER_MISSING:git`." The A9.1 outcome, INVALID, is unchanged. The fixture bytes are regenerated. Kind K (fixture only) |
| 15 | `270ca49:docs/V1-PROFILE.md:1029` (custody record) | "HYBRID-SUPPLEMENT §9 item 6", a stale locator | `formal/p8/HYBRID-SUPPLEMENT.md` §11 item 6, the spike-key sentence at :525-526. The frozen bytes are unchanged; this corrects the locator only |

## A11.4 Dependency duty for registered decisions

When a registered decision changes a parameter (an algorithm, a custody form, a channel, a horizon, a scope, a key),
the owner sweeps the registered texts for sentences whose referent the change alters. Each one is recorded as
amended, superseded, still fitting or open, before the decision's change is treated as complete. An owner decision
that touches a registered parameter is checked against those texts before it is recorded.

## A11.5 Results of the first sweep (2026-10-28)

The sweep covered the original, Amendments 1–10, the freeze, the tracker and the author-rulings files
(`docs/reviews/stale-dependencies/SWEEP-2026-10-28.md`). The owner checked each finding against its source. The
review added item 3. The sweep did not read the rest of the frozen specification or the hybrid supplement
(`SWEEP-2026-10-28.md:3-4`, `:20-21`). The Levadura panel read them. Its findings are §A11.3 rows 1, 2, 4–6, 8 and
10–14, §A11.6 and §A11.7.

**Scope from now on.** Every sweep under §A11.4 reads the frozen specification object in full (`spec.bin`: A9, A10,
PROOF, V1-PROFILE, ENCODING-V1 and the hybrid supplement; `formal/freeze-v1/FREEZE-RECORD.md:16`), as well as the
original, every amendment, the freeze record, the tracker and the author-rulings files.

1. **H3 (`phase-0-prereg.md:232-248`): not amended.** H3 is a hypothesis with a stated falsifier. Its examples are
   AWS-based, but they do not restrict it to AWS. It is measured over the whole deployed system, every provider
   included. A measurement protocol is recorded before measurement. It covers retained resources (including the
   compliance-locked trail bucket), defines the demonstration and idle periods, and reports the three numbers
   separately. A slot-2 signer and an issuer poller that run through the operating window conflict with "idle
   compute exactly $0". If that or another number fails, H3 is reported as falsified. The operating window is not
   redefined as a demonstration to avoid this.
2. **The slot-2 enforcement boundary: an owner decision (Option 1), adopted by the author's signature.** A9.6 requires the final custody implementation to
   be deadline-qualified (`phase-0-prereg-amendment-9.md:389-392`). The frozen record keeps "the selected,
   deadline-qualified custody implementation" (`270ca49:docs/V1-PROFILE.md:1024-1025`). It describes it through
   `prototype/policy-signer/` (:1033-1037), which met the deadline on 2026-10-14 (:1038-1040; §14.2 item 5,
   :1429-1435). That qualification stands as historical evidence.

   Production cannot run the prototype. Instrument code under `prototype/` stays instrument code, and service code
   that ports it must earn its own evidence on its own bytes (`formal/freeze-v1/FREEZE-RECORD.md:62-64`). Nothing an
   instrument produces discharges an obligation (A9:198-200). The E9 ruling R5b (`docs/reviews/e9-packet/AUTHOR-RULINGS.md:54`)
   allows porting instrument code with evidence earned on the resulting bytes. It does not address A9.6's
   deadline-qualified custody, so it does not settle this question. The registered texts do not say whether a
   post-deadline port counts as "the selected, deadline-qualified custody implementation". Each reading keeps a
   different registered text. A choice is needed, and the relaxation it makes needs the author's signature.

   > **OWNER DECISION FOR THE AUTHOR'S SIGNATURE (2026-10-29): Option 1.** Asked whether this is irreversible or
   > scope-changing, the owner answered no to both for Option 1. It changes no V1 scope. The practical lock-in is
   > the first production receipt under the hybrid keys, at deployment, not this text, and a later amendment can
   > revisit it before then. Option 2 is the scope change (it drops PQ and amends the freeze) and buys no claim V1
   > makes. The authority Option 1 needs is the author's signature on this amendment. **Signing adopts Option 1.**
   > If the author disagrees, the text changes before signing. Both options are kept below as stated before the
   > choice.
   >
   > **Option 1: the custody implementation is the custody option and boundary (port permitted; keeps the hybrid).**
   > A signed row says the A9.6 deadline qualification (A9:389-392; `270ca49:docs/V1-PROFILE.md:1024-1025`,
   > `:1429-1435`) attaches to the selected custody option and boundary: GCP Cloud KMS HSM, P-256, non-exportable,
   > behind a queue-pulling policy signer with the A9.6 checks (A9:382-388). The 2026-10-14 instrument run evidenced
   > that option, and A9.2 lets an instrument select among registered branches (A9:198-199). Production runs the
   > service port `service/signer-gcp/`, provided that before the first shipped receipt:
   > - (i) it preserves **every A9.6 custody and policy requirement**: complete-frame validation; the declared-time
   >   check on its own clock before signing; the issuing account able to enqueue but not to invoke the key, change
   >   the policy or clock, or obtain key-use credentials; and the key dedicated to V1 type-0x00 documents. It also
   >   preserves every property in the frozen custody record (`270ca49:docs/V1-PROFILE.md:1017-1040`) except the
   >   identity of the implementation, its 2026-10-14 deadline evidence and its prototype paths, which this option
   >   replaces;
   > - (ii) the external custody record names the deployed implementation, its image digest and its configuration;
   > - (iii) deployed evidence is earned on the new bytes. That means: a deployed positive signature that verifies
   >   offline; deployed refusals for a malformed frame, a wrong tag, a wrong alg, a wrong fingerprint and a declared
   >   time outside ε; a review of every principal that can cause a signature or administer the signer
   >   (`service/issuer/DEPLOY.md` step 8); and verified retirement of every other signing path (step 7);
   > - (iv) all of it identifies the tested image and configuration.
   >
   > This keeps FREEZE-RECORD.md:62, A9.2 and A9.6's custody and policy requirements. It overrides the code-identity
   > reading of "the selected, deadline-qualified custody implementation" (profile :1024-1025) and of A9.6's "final
   > custody implementation" (A9:389-390). Cost: it is a retrospective relaxation, made after the deadline and after
   > the candidate code existed. It is disclosed as such in the header.
   >
   > **Option 2: the code-identity reading is kept (A9.6 fallback).** No port can be deadline-qualified, and the
   > prototype cannot run production, so the hybrid's custody condition cannot be met. A9.6's own consequence
   > applies: "otherwise the registered fallback is taken" (A9:391; cut order A9:211-212). That is classical P-256
   > in both slots (A9:372-374), with slot 2 still under A9.6 custody through a ported service signer. The fallback
   > has no 21 Oct custody deadline. This keeps A9.6, A9.2 and FREEZE-RECORD.md:62 literally. Cost: it drops the PQ
   > slot. A9:346-350 records PQ as the author's stated preference, not a claim requirement, and the first item cut.
   > It changes the frozen catalog's `alg` (`formal/freeze-v1/objects/catalog.json`; FREEZE-RECORD.md:16, :20), so
   > the freeze must be amended or redone before issuing. The 2026-10-16 hybrid registration becomes moot.
   >
   > Chosen: **Option 1**, by the owner, adopted by the author's signature on this amendment.

   **Why the owner chose Option 1.** It keeps every custody and policy requirement and re-earns all evidence on the
   bytes that run. Option 2 keeps the deadline text literally but gives up the author's stated preference and
   reopens the freeze. Until this amendment is signed, issuance does not start (§A11.7, `service/issuer/DEPLOY.md`
   step 0).
3. **The spike keys (`formal/p8/HYBRID-SUPPLEMENT.md` §11 item 6, :524-526).** The spike-key sentence (:525-526)
   is **unchanged**: "Both spike keys are deleted after the re-capture verifies, once the review clears." The
   item's first sentence (:524), "the issuer always uses EXTERNAL_MU for the kms slot", is changed by §A11.3 row 12
   (K-R). The owner's deployment draft (2026-10-27) reused the spike keys as production keys. That contradicted
   this commitment, and the draft is withdrawn. Production uses new keys (`service/issuer/DEPLOY.md`), recorded in
   the external custody record before use.
4. **A dangling cross-reference (`phase-0-prereg-amendment-10.md:675`).** Row 25 does not apply to V1 (E9 row 2,
   2026-10-23; §A11.3 row 8). This is a CLARIFY: the fallback cites row 15 only (§A11.3 row 9).
5. **K-R's enforcement (`formal/p8/HYBRID-SUPPLEMENT.md:61-64`, `:148-174`, `:524`, `:533`;
   `formal/p8/ENCODING-V1.md:557-559`): amended in wording, the assumption unchanged.** (K-R) itself stands: the
   ML-DSA-65 key signs only V1 tagged strings, in pure mode with the empty context, under EXTERNAL_MU, for no other
   protocol. What changes is who enforces it. The supplement and ENCODING-V1 §5.2 name the issuer as the computer
   of `μ` and the issuer role as the only `kms:Sign` principal. In V1 as designed (deployment pending), a
   dedicated policy signer validates the complete frame (tag, alg, key fingerprint, ε for attestation frames only,
   `sign_by`, the signing stop) *before* computing `μ`. Manifests carry no declared time, so ε does not apply to
   possession signing (HYBRID-SUPPLEMENT:495; `service/signer-kms/tessera_sign_kms/signer.py:180-184`). The
   signer's role is the only `kms:Sign` principal (`service/signer-kms/`; key policy in
   `service/signer-kms/infra/main.tf`). This narrows what a captured issuer role alone can get signed. It does not
   change the supplement's stated limit: "whoever may call `kms:Sign` on the key can sign any message by computing
   `μ`" (:171-172). An administrator of the account can still grant that (`PutKeyPolicy`), which is C3.

## A11.6 Clarifications

These are readings, not changes. Each narrows or clarifies only and adds no claim.

1. **ENCODING-V1 §5.2 rule O *Reasons* (c021). Narrowing.** "ENCODING-V1 §5.2 rule O *Reasons*
   (`formal/p8/ENCODING-V1.md:538-544`) record the 2026-10-12 GnuPG observation that motivated the legacy-header
   form. Rule O itself is unchanged. Under the pair id, the gpg slot's packet is assembled by the slot-2 policy
   signer (profile §8 custody record, `270ca49:docs/V1-PROFILE.md:1033-1036`), and it is a Tessera-assembled packet
   held to the same form as :541 requires. :541's 'KMS slot's packet' describes the classical id only, because
   under the pair id the kms slot emits rule R and has no packet."
2. **W1 and receipt identity (c033). Clarifying.** "Profile §6 W1 (`270ca49:docs/V1-PROFILE.md:850-851`) 'is not an
   identifier' has the sense of its cited source ENC §3.5 (`formal/p8/ENCODING-V1.md:400-402`): no semantic,
   standing or attempt identifier, and no identifier of the statement, is derived from signature bytes. §9's 'A
   receipt's identity is SHA256(A_sig)' (:1183-1187) is an exact-bytes identity for deduplicating and referring to
   one receipt's claim-bearing bytes. Two receipts of one statement with different valid signatures are different
   receipts. Neither text widens the other."
3. **"Both OpenPGP adapters" (c056). Narrowing.** "Profile §6 issuer duties 'Both OpenPGP adapters'
   (`270ca49:docs/V1-PROFILE.md:386-387`) and 'both OpenPGP adapters and the repository signer' (:392-393) mean
   every OpenPGP signer in use. Under the pair id that is the gpg slot's policy signer (and the repository signer).
   The kms slot emits rule R, to which the rule-O policy does not apply. Both apply under the classical id."

**Not confirmed: c145.** It read profile §14.2 item 1's "YubiKey 2 is not in hand" (`270ca49:docs/V1-PROFILE.md:1396-1397`)
as naming YubiKey 2 the release key. No text does. The runbook says the release key is "Not YubiKey 2"
(`docs/V1-OPERATIONS-RUNBOOK.md:125`). Nothing is needed.

## A11.7 Owner-document repairs (not registered text)

These are owner documents. The owner makes each repair outside this amendment. They are listed so the record shows
where each one belongs.

- **c016.** `docs/V1-SERVICE-RESOLUTIONS.md:23` (S4): the 24-hour terminal FAILED conflicts with A2's
  `declared + δ + S` expiry (`phase-0-prereg-amendment-2.md:260-264`, 96 h at A9.2's values) and A9:422. S4 keeps
  "usually complete within 3 hours" as a non-guaranteed figure. A request ends only by the registered lifecycle:
  COMPLETE, or REFUSED when its N attempts are exhausted (A2.3). The issuer had no attempts, no latch and no
  refusal, so this is more than an edit. The owner's design is `docs/decisions/2026-10-29-issuance-lifecycle.md`,
  reviewed in `docs/reviews/issuance-lifecycle/`. This amendment does not
  restate that design, which is still under review; the design document governs its own content. Whatever it
  settles must meet A2.1 and A2.3 as registered, including the latch that excludes expiry (A2.1 `:153-160`) and "every
  timely-eligible attempt ships" (`:143-145`). **Signing this amendment does not accept any residual the design
  states** (at present, an on-time observation lost before it is persisted, followed by permanent loss of the
  evidence, which could end in refusal). Such a residual is assessed in the lifecycle work, against the registered
  text, and needs its own author decision if it remains. Matching edits: CL-03 items
  1 and 2 (`docs/V1-CLARIFICATIONS.md`), the clock-tolerance decision, `service/issuer/DESIGN.md`, and the issuer
  code and tests (inventory in the design). A shorter hard bound needs a signed amendment (A2.1 `:139-142`).
- **c036.** `service/issuer/DEPLOY.md`: a gate before the session's first step makes the whole deployment wait for
  the §A11.5 item 2 ruling, recorded in this amendment's signed text. Until then, issuance cannot start. No prototype fallback is added. Under Option 2, steps 5–7 and the key section are
  rewritten for the classical fallback.
- **c093.** `formal/PROPERTIES.md:167-168`: add S, and record that for `tessera-v1-strict` all five parameters were
  ratified by the author's signature on A9 (A9:223-225). The Band 0 exit item stays open outside V1 (§A11.3 row 4).
- **c136.** `docs/V1-SERVICE-RESOLUTIONS.md:26` (S7): replace "(H3)" with a cost derived from H3's three
  measurements, stated with its derivation. Per-receipt cost is not an H3 number (`phase-0-prereg.md:232-248`).

Repairs to this draft itself, applied above: c004 (row 12's locators and item 5's range), c030 (Option 1 condition
(i)), c055 (§A11.2 item 2's counts), c062 (row 7's sources), c097 (item 3), c108 (ε in row 12 and item 5), and
c006 (the barred prototype default removed from item 2).
