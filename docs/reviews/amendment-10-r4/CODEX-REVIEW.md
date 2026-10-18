# Amendment 10, fourth review: chain-order pre-commitment of the listing

2026-10-18. **Result: revise before adoption.** The inequality is sound for authentic anchors on the same Bitcoin history: a configuration created after a receipt's inclusion cannot acquire an earlier commitment without breaking the commitment/history assumptions. The present addition does not completely establish that premise against the stated release-key thief. There is also a first-release bootstrap cost and an incomplete offline-evidence/reporting contract.

This review raises one HIGH and three MEDIUM findings. The fixes below are proposed corrections, not author rulings. Option (e) remains AWAITING AUTHOR RULING.

## Scope and evidence

Reviewed A10's plain “Key substitution: time” paragraph, A10.4.1 including its new pre-commitment rule, A10.5, rows 37–39 and the change accounting; A9 at signing commit `2ad3489`; V1-PROFILE §3.3–§3.4, §5, §7.1–§7.2, §14.2 and §15.2/§15.5/§15.7; and the preceding A10 review/disposition records where relevant. Locations below are lines in the reviewed working-tree files.

Repository HEAD: `7d7f94d797048f96df9a2b129962a5604439f4ae`. A10 is an untracked proposed document, so HEAD does not identify its bytes.

| Artifact | SHA-256 reviewed |
|---|---|
| `docs/phase-0-prereg-amendment-10.md` | `bb8b5efbc1b04542e4cd4c70391855df35bb3b663c4a2bcd24248aea7bfca6b4` |
| `docs/V1-PROFILE.md` | `08bf19180aa84b1b9866ca1cba05788ac88c644370346acc35aa934676fc220f` |
| `docs/phase-0-prereg-amendment-9.md` at `2ad3489` | `ff09f9b1ff6bb717bcca2c2f803eb8674f4beb2d28e88d5718320fe9b63c9f05` |

These are document/construction checks. No formal model or implementation was run, and no cryptographic exploit was executed.

## Findings and exact fixes

### R4-01 — HIGH: checking only the listing pins leaves the comparison forgeable; the authentic key fingerprint does not authenticate historical releases

**Locations:** A10 :111–112, :477–481; row 37 (:672). Governing checks: V1-PROFILE :789–815, :818–834.

The draft correctly notices that the thief can sign false pins. Its remedy checks “the pins used by the listing proof” against Bitcoin or an earlier held release. The comparison also consumes the receipt anchor. Authenticating only one operand is insufficient.

For example, after theft the attacker can genuinely stamp a new first-listing configuration at current height H. The attacker then supplies fabricated receipt headers at H+6 through H+11, pins their hashes in the forged release chain, and sets their header times inside the old issuance window. A counterfeit old-window receipt and its OTS path can be constructed against those fabricated merkle roots. The listing's genuine H through H+5 pins pass the stated independent check, and H+5 < H+6 passes. V1 deliberately performs no PoW, nBits or retarget validation: equality with a supplied pin substitutes for those checks. Corresponding false authority-history pins/trust entries can support the counterfeit DNS/git evidence in a fork from version 1. This attack needs no change to an intact honest receipt's signed bytes; it supplies a new counterfeit for the old window under the thief's keys.

Checking against “an earlier release it holds” works only if that release is independently known to be genuine and already covers the required heights. Merely having a release earlier in the presented chain, or one signed with the right key, does not supply this fact after key theft. Most importantly, the genuine bootstrap **key fingerprint** cannot distinguish two release chains signed by that same key. The thief in this threat model has that key, not a substituted initial key.

**Exact fix:** replace :477–481 and row 37's non-claim with:

> The retrospective protection requires a conforming verifier and independently authenticated Bitcoin history for both selected anchors and their six-header segments. The receipt, listing, snapshot and git proofs must use the same independently authenticated history. For this theft protection, a signature under the possibly stolen release key is not sufficient pin authentication. Compare every used pin with independently validated Bitcoin history, or with a previously retained, independently authenticated genuine release that covers that height. An earlier release with no pin at the height supplies no witness. A party unable to establish this history has not established the retrospective protection. Authenticating only the bootstrap public-key fingerprint does not distinguish a fork signed with the stolen genuine key. An independently retained genuine release/configuration commitment can distinguish such a fork to the extent of its recorded contents and ancestry.

Keep A9's separate distribution-compromise boundary: an attacker-signed executable can simply omit the rule. State that the new historical check is evaluated by a trusted conforming verifier; it does not authenticate arbitrary newly acquired code after release-key theft.

Replace the plain paragraph with:

> A release must list the exact keys and window before the receipt's Bitcoin anchor. To check this after release-key theft, keep the first listing release and its proof, and authenticate the Bitcoin history for both anchors independently of the stolen key. The release-key fingerprint alone cannot identify a forged release history.

Apply the same scope to the technical claim and row 37. Do not claim an unconditional later-theft guarantee while treating its required history authentication as an optional holder action. This correction requires no UTC claim.

### R4-02 — MEDIUM: the initial listing release cannot qualify its own future stamp using its own pin set

**Locations:** A10 :465–476, :488–490; rows 38–39 (:673–674). Governing checks: V1-PROFILE :789–793, :826–834, :1422–1423.

The “honest cost: none” argument establishes a desired chronology, but not that the installed evidence can verify it. The initial release's configuration C0 must be fixed before SHA256(C0) is stamped. Its Bitcoin inclusion and five successor headers therefore do not yet exist when C0's pins are fixed. Putting the hashes of those future headers into C0 would require solving a cryptographic self-reference. Its own authentic pin set cannot qualify its listing proof. Publication and six confirmations alone do not cure that missing coverage.

A later installed configuration can cover those headers, so this is repairable without an endless sequence: only the **first-listing** release needs to precede the receipt. The addition does not currently state that bootstrap sequence. The wait, extra release and retained evidence are real costs, even if they fit the schedule. Also, row 39's unqualified “the release listing a key pair” should not impose a before-first-receipt deadline on every later release that retains that pair.

**Exact fix:** replace the honest-cost statement and expand row 39 with:

> Initial-window bootstrap: publish the authenticated initial listing release C0 and stamp SHA256(C0). After its selected inclusion block and five successors exist, publish an append-only release C1 whose configuration pins those six headers and whose installed listing evidence includes C0 and its completed proof. Before issuing the first receipt, make that usable release/evidence available. The receipt must select a height strictly greater than h_C0+5. C1 retains the exact entry unchanged; its own later stamp is not the first-listing witness for that entry. This adds a confirmation wait, at least one pin-extension release for bootstrap, and custody of the listing evidence. Under this sequence an honest first-window receipt can satisfy the rule.

Use “the release that **first** lists the exact entry” in row 39 and the holder instruction. For later windows, require an installed configuration with coverage of the first-listing stamp before issuance; do not imply that merely submitting or publishing a release stamp supplies that coverage. Keep the single-window and separately registered successor boundaries.

### R4-03 — MEDIUM: configuration plus proof is not a complete 2106 verification package or declared input set

**Locations:** A10 :469–471, :475–486; row 38 (:673); A10.5 :594–607. Governing contract: A9@`2ad3489` :267–283, :326–340; V1-PROFILE :298–303, :399–403, :1411–1424.

Row 38 supplies the first-listing configuration and OTS proof. Qualification also requires the raw h_release through h_release+5 headers. The existing receipt bundle need not contain those earlier heights: its required header coverage is for receipt, snapshot and git proofs. A10.5 still explicitly describes those three proofs and uses **bundled** headers. Pins contain hashes, not the missing 80-byte headers.

Nor does a configuration containing an entry, plus a timestamp, establish that this is an authenticated release in the installed chain or the release that **first** introduced the entry. The current `previous_sha256` field commits to a predecessor but does not supply it. The new rule specifies neither the necessary ancestry evidence nor a checked first-listing reference. A 2106 holder told to keep any release “that lists” the keys could retain only a later listing and lose the actual witness.

Finally, proof upgrades, sidecar headers and independently supplied historical pins can change qualification and the reason while the receipt and main trust-configuration bytes remain identical. A9.4 permits this only as a change in **declared inputs**. A10 currently names no identity/version contract for these new inputs; the six stable fields themselves need not change.

**Exact fix:** extend :469–471 and row 38 to require an installed, archived listing-evidence package outside the receipt bundle. Specify all of these contents and rules:

- The canonical first-listing configuration, its authenticated release/archive binding and signatures, its completed OTS proof, and raw headers for its selected six-header segment. Apply A10.5's selection rules to this fourth proof using a specified installed header pool; state how that pool combines with bundle headers and how conflicting duplicates are handled.
- A release-authenticated manifest mapping each exact service-key/window tuple to the first-listing configuration's SHA-256. The release checker establishes that reference against the authenticated predecessor chain, verifying that the entry is absent before its introducing release and retained unchanged afterward. Preserve the intervening configurations and authentication/key-transition evidence needed to reproduce that check; never fetch them implicitly from Tessera during offline verification.
- Independently authenticated history/pin evidence as required by R4-01, plus the independently retained bootstrap record identifying the production key and original genuine baseline. A signature freshly verifiable under the stolen key is not historical provenance. Retain the actual verifier/specification/catalog and current configuration used for the original verdict, alongside the receipt bundle and its original three proofs/headers. Keep any separate safe-before/theft-cutoff assessment outside the stable six, as A9.4 requires.
- Declare the exact listing-evidence manifest, proof/header bytes and independent-history inputs as verification inputs. Record their content hashes with the existing configuration/spec diagnostics. Exact reproduction requires the same bytes and policy; replacing a proof, supplying missing headers or changing history witnesses is a declared-input change. No network lookup may silently affect the stable result.

Update the plain holder instruction and row 39 to tell the holder to preserve this package with the receipt. Distinguish failure to retain evidence from evidence of fraud. These are required inputs to the proposed check, not a new claim that dead-project reconstruction has already been demonstrated.

### R4-04 — MEDIUM: the two codes do not define the new check's failure cases or its place in stable reporting

**Locations:** A10 :472–473, :483–486, :672, :676–695. Governing reporting rules: V1-PROFILE :253–255, :276–303, :1459–1528.

“Under the registered failure precedence” preserves INVALID over UNVERIFIABLE, but does not insert new checks into the profile's **total reason order**. That table has no listing rows. For identical inputs failing both listing order and issuance-window checks, one implementation could report `LISTING_NOT_PRECOMMITTED`, another `ISSUANCE_WINDOW`. Both obey verdict-class precedence while disagreeing on a stable field.

The new text also leaves present-but-malformed proof, wrong stamped digest, no qualifying attestation, absent headers and incorrect first-listing evidence without explicit outcomes. Those must not be collapsed into “ordering fails”: if either height is unavailable, the comparison is unperformable. A missing proof must not suppress an independent INVALID result or receipt-anchor evaluation needed to report T.

**Exact fix:** register a complete reporting insertion after existing row 15.2 and before 16.1, preserving all existing rows' relative order. Put the tuple classifier first, followed by these listing subchecks in the stated order:

| Listing subcheck | Proposed outcome |
|---|---|
| First-listing configuration/reference authentic and internally consistent | Provisioning prerequisite under the existing trust-authentication refusal rule; missing or invalid required configuration/manifest gives `TRUST_CONFIG_UNAUTHENTICATED`, no receipt verdict. This does not include the separately supplied OTS proof, whose absence is handled below. |
| Listing OTS proof present | Absent: `UNVERIFIABLE / LISTING_PROOF_MISSING` |
| OTS grammar/bounds/message sizes | Malformed: `INVALID / OTS_FORMAT` |
| Detached file digest equals SHA256 of the canonical first-listing configuration bytes | Mismatch: `INVALID / LISTING_STAMP_MISMATCH` (additional proposed code) |
| No contradicted branch | `INVALID / OTS_MERKLE_MISMATCH` |
| Qualifying attestation and selected h_release | None: `UNVERIFIABLE / HEADERS_MISSING`, or `ANCHOR_PENDING_ONLY` for pending-only proof |
| Selected-height transaction/path subset | Apply the snapshot/git parts (1), (2), (4), with `INVALID / OTS_TX_SHAPE`; no receipt-txid comparison |
| h_release+5 < h_receipt | False with both heights available: `INVALID / LISTING_NOT_PRECOMMITTED`; otherwise blocked by the earlier unavailable input, with no invented order-failure reason |

Extend header rows 10.1–10.3 to the explicitly defined installed listing-header inputs. Specify deterministic source/path ties for duplicate/conflicting evidence. Give every new row its necessary-input dependencies; the tuple match uses the parsed domain/fingerprints/window, not successful DNSSEC authentication as a prerequisite. Register the classifier's position too, rather than leaving `SERVICE_KEYS_NOT_LISTED` unordered. Apply the existing first-failed/else-first-unperformable aggregation, and continue independent receipt-anchor evaluation to determine T.

Add agreement cases for missing listing proof plus an invalid signature; bad listing order plus `ISSUANCE_WINDOW`; wrong listing digest; missing listing headers; and the first-window C0/C1 sequence. These are prospective conformance obligations, not results of this review.

Limit :483's append-stability assertion explicitly to the original **tuple classifier**. Do not extend it to the height comparison: pin extensions can qualify a previously nonqualifying earlier attestation and change the selected height. Preserve A9.4's exact-output promise for identical complete declared inputs, and the separation of historical-security assessments. Update row 37 and the mechanism accounting for the selected complete error taxonomy; the concrete correction above adds `LISTING_STAMP_MISMATCH`, making four new reason codes for A10.4.1 rather than three. Make these profile changes after the author's ruling, as A10 already requires.

## Checks without an additional finding

**Inequality and commitment target.** The strict comparison has the same off-by-one convention as existing C4: confirmation six is h_release+5, and equality with h_receipt must fail. Stamping the full configuration hash binds the exact domain, both fingerprints and both window endpoints; stamping only a release name/version or a mutable pointer would not. Under authentic shared history and the continuing hash/history assumptions, a thief cannot backdate a newly constructed configuration into a fixed, genuinely past receipt anchor. This establishes commitment ordering, not UTC, first publication, or general safety after distribution compromise.

**A9 source rows.** Checked directly with `git show 2ad3489:docs/phase-0-prereg-amendment-9.md`. Row 37 correctly cites C4 at :143 and its git `height + 5` rule. Row 38 correctly cites the trust-configuration bullet starting at :154. Row 39 correctly quotes the issuer invariant at :165. Their added text remains subject to the findings above; the source references themselves need no correction.

**Counts and status.** Mechanically parsed all table rows: IDs 1–39 occur exactly once. The stated totals are correct: 15 NARROW-CLAIM, 1 CORRECT, 5 CLARIFY, 13 BROADEN, 5 GATE. The existing accounting includes the new stamping/order mechanism and both newly proposed codes, for three new A10.4.1 codes in the reviewed draft. Rows 37–39 remain BROADEN and option-(e)-only, awaiting author ruling. No count defect is raised. The fixes above would require corresponding evidence/provisioning and reason-code accounting updates.

Only this review file was written. No amendment, profile, custody procedure, model or prior review was edited.
