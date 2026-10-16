# Review: anchoring Tessera V1 signatures

2026-10-12. Scope: the draft V1 encoding and claims named in CODEX-BRIEF.md. This is a specification review, not an implementation exploit demonstration or a formal discharge. The full ENCODING-V1.md was read; relevant proof, decoder and vector sources were inspected. No model runs were needed for the conclusions below.

The owner's mechanism diagnosis is correct. Accept the signature-inclusive anchor, correct the one-key attack example, and narrow the post-break claim. A timestamp of unsigned frames cannot establish that their signatures existed at that time. A timestamp of signed artifacts can preserve historical evidence under explicit historical security and continuing anchor assumptions; it is not an unconditional 2106 guarantee.

1. **HIGH — The current preimage permits pre-staging followed by later signing. Disposition: MECHANISM.**

   **Evidence:** formal/p8/ENCODING-V1.md:307-319 specifies an anchor containing only two frames; :211-224 places declared time and public bindings in those frames. docs/V1-DERIVATION-DRAFT.md:39-56 connects presentation, signatures and T. docs/implementation-spec.md:316 expressly allows crafting manifests and anchoring anything; :689-692 distinguishes declared time from anchored existence.

   Construct both frames at time T using an authentic historical manifest/key set, arbitrary previously unissued content, known spec/vector/preamble hashes, and a declared time satisfying the temporal window. Obtain the public OTS stamp and the required confirmation evidence then. Preserve the contemporary authority evidence. Later, acquire signing capability for both required keys and sign these unchanged frames. All frame hashes and time predicates remain unchanged; the old stamp proves only that the frames existed. Neither a signed declared time nor an OpenPGP signature creation time proves when a signature was generated after its key becomes forgeable. The assembled bundle can meet the stated V1 checks without any Tessera issuance event for that content by T.

   **Recommendation:** include each required attestation signature in the receipt anchor and require the verifier to reconstruct that preimage from the exact signatures it verifies. C5 should explicitly include signature existence by T; C2/C3's historical inference must name pre-T security assumptions. Under an assumption that issuer keys remain unforgeable forever, this attack is outside scope; it is nevertheless the concrete gap in the proposed later-compromise/later-break guarantee.

2. **MEDIUM — One later stolen key is insufficient for the stated strict attack. Disposition: WORDING.**

   **Evidence:** docs/V1-DERIVATION-DRAFT.md:54, :63-66 requires both slots in strict mode; formal/p8/ENCODING-V1.md:301-305 fixes both manifest slots and possession proofs.

   The brief's singular “a Tessera signing key” overstates the theft case. For arbitrary new content, the attacker needs both attestation signatures. A later general P-256 break supplies both capabilities from their public keys; theft requires both keys, or another route to the other required signature. One compromised slot plus an unavailable uncompromised slot does not pass strict verification. Existing manifest possession signatures can be reused; they need not be forged for this attack.

   **Recommendation:** state “later obtains signing capability for every required slot.” Keep separate custody as a real barrier to single-key theft, while noting that both slots share the same algorithmic failure domain.

3. **HIGH — The authority anchors do not already bind receipt signing to T. Disposition: REJECT.**

   **Evidence:** docs/V1-DERIVATION-DRAFT.md:55 authenticates K for D at authority evidence times, :93 describes the snapshot-time rule; formal/p8/ENCODING-V1.md:297-305 defines a manifest containing keys/issuer/algorithm, :325-330 gives the snapshot a separate anchor, and :354-360 defines a key-publication record with no receipt digest.

   Reject the proposed rebuttal that DNSSEC snapshot anchoring or the signed, anchored git assertion closes this attack. An attacker can reuse authentic contemporary evidence that the actual Tessera keys were authorized for D. The commit→tree→blob checks authenticate the assertion, not the later attestation signatures. The snapshot's RRSIG windows and anchor constrain that snapshot, not the receipt signatures. The manifest hash, slot fingerprints, profile, algorithm and declared time can all be correctly pre-staged. No specified authority statement commits to this receipt's signatures or its issuance event.

   **Recommendation:** retain both authority checks, but identify their distinct role. A contemporaneous authenticated authority statement committing to the signed receipt could alternatively supply the missing binding; the current key-only statements do not.

4. **HIGH — The fix works only with an exact, bounded signature representation and matching verification path. Disposition: MECHANISM.**

   **Evidence:** formal/p8/ENCODING-V1.md:279-290 specifies v4 binary-document signatures and their hashed trailer; :307-319 specifies the existing length-prefixed anchor; :455-460 leaves container and signature verification details outside P8. formal/p8/vectors/check.py:528-540 currently accepts a receipt encoding without signature arguments.

   A suitable proposed layout is:

   ```text
   A_sig = header(receipt-anchor-tag) || 0x02
           || u32(len(F_kms)) || F_kms || u32(len(S_kms)) || S_kms
           || u32(len(F_gpg)) || F_gpg || u32(len(S_gpg)) || S_gpg
   ```

   Here S is exactly one detached binary OpenPGP signature packet in a pinned serialization, not armor, a display string, or a container that admits extra signatures. Specify allowed packet framing, signature size caps, nonempty signatures, exact consumption and rejection of extra/truncated bytes. Verification must use the very S bytes committed by A_sig and the designated F/key, not a separately selected or reconstructed signature. Slot order remains manifest order. With these rules the decoder is a left inverse on ordered frame/signature byte tuples; digest binding additionally requires the relevant SHA-256 collision/preimage resistance. Later forging a signature cannot make its new bytes fit an old commitment, absent a break of that binding or anchor.

   **Recommendation:** adopt this layout or an equally precise one. Change/version the anchor construction unambiguously; no fallback accepting frame-only anchors under the strengthened claim. As this is still a draft, replacing the unissued layout is simpler than migration. OTS proof bytes, txid, confirmation headers and other outputs of anchoring remain outside its preimage: including the resulting proof would create a circular dependency.

5. **MEDIUM — W1 becomes exact-copy integrity, not a forgery bypass; the identifier rule needs clarification. Disposition: WORDING.**

   **Evidence:** prototype/FINDINGS-BY-TIER.md:12 records ECDSA (r, n−s) and OpenPGP unhashed-area malleability; formal/p8/ENCODING-V1.md:288-290 says unhashed subpackets carry no meaning and no V1 identifier derives from signature bytes. docs/V1-DERIVATION-DRAFT.md:85-86 repeats the identifier obligation.

   After the fix, changing s to n−s, editing an unhashed subpacket, changing packet serialization or regenerating a randomized signature changes the committed artifact. Even if the new signature verifies mathematically, it must fail the old receipt anchor. This does not let an attacker attach a fresh forgery to the old T. It does let a mirror damage a copy; preservation must retain exact committed bytes, as it already must for frames. A later re-stamp of the modified copy gives a new time bound and does not restore historical protection.

   **Recommendation:** keep semantic/standing/attempt identifiers independent of signature bytes, but explicitly permit the anchor digest to commit to them. If “no V1 identifier” includes that digest, reconcile the wording rather than claim it remains literally unchanged. Do not require signatures to be intrinsically unique. Low-s normalization alone does not resolve OpenPGP serialization/unhashed-area malleability; avoid normalization after stamping. Unhashed fields remain semantically inert even though their exact bytes are committed.

6. **MEDIUM — Signing must finish before stamping; no second receipt anchor is necessary. Disposition: MECHANISM.**

   **Evidence:** docs/implementation-spec.md:419-426 requires framed commitments and layout vectors; :679-687 requires one shipped receipt proof and excludes txid from signed bytes. docs/V1-DERIVATION-DRAFT.md:68 requires a complete receipt before shipping; formal/p8/ENCODING-V1.md:318-330 already distinguishes the receipt anchor from the DNSSEC snapshot anchor.

   The dependency order becomes: fix manifest/common metadata and declared time; build both frames; produce and verify both detached signatures; freeze their bytes; stamp A_sig; obtain and validate confirmation/time evidence; ship the complete receipt. Receipt signatures must not include their own eventual anchor time/proof. A retry that changes any committed frame or signature needs a fresh matching stamp and must obey the existing reissue/temporal rules. Signing and any normalization must precede the stamp, not be performed opportunistically while packaging after confirmation.

   **Recommendation:** replace the one receipt anchor's target; do not add one OTS proof per signer or keep an old frame-only receipt proof alongside it. R-3.42 is compatible with one composite anchor. Authority evidence can retain its separate evidence anchors under the existing object-scope reading. Clarify R-3.9 as signatures committing to frames and the receipt anchor committing to frames plus signatures; this strengthens frame coverage rather than dropping it. Record adoption without silently changing registered history.

7. **HIGH — Post-break survival is conditional on historically trustworthy signing and a surviving temporal commitment. Disposition: WORDING.**

   **Evidence:** docs/V1-DERIVATION-DRAFT.md:54 says nothing about key lifecycle after T; :56 gives chain-time, presentation and reorganization residuals; :65-66 specifies offline trust configuration and no renewal/revocation evaluation. formal/p8/PROOF.md:60-70 separates hash binding from signature assumptions. docs/phase-0-prereg-amendment-3.md:473-482 explicitly says OTS does not fill a signing gap and keeps PQ a production gate.

   Correct conditional statement: an exact signature demonstrably existing before signing capability became available to the adversary cannot be manufactured afterward and substituted into that old receipt while the commitment and temporal evidence remain secure. Historical authenticity additionally requires the appropriate signing/key-use assumptions before that bound, authentic historical key authority, and no relevant pre-bound compromise. A later P-256 break need not invalidate such historical evidence by itself. It does not cure earlier theft, unauthorized pre-T signing, misissuance, or whole-author-sphere capture. It does not prove the issuer itself obtained the OTS stamp or uniquely issued the bundle.

   The timestamp analogy is sound but limited: [RFC 5126 §6.1.1](https://www.rfc-editor.org/rfc/rfc5126.html#section-6.1.1) timestamps the signature value. [RFC 3161 §1](https://www.rfc-editor.org/rfc/rfc3161.html#section-1) describes historical existence evidence. Tessera's Bitcoin/OTS trust and time model is different from a TSA's; this fix is not CAdES compliance.

   **Recommendation:** replace an unqualified “classical signatures survive later breaks” with the conditional statement above. Preserve A3.6's PQ deferral/gate. The fix protects historical signatures against later fabrication; it does not permit secure new classical issuance after a break and does not establish perpetual preservation.

8. **HIGH — A 2106 verifier needs historical security policy, not merely an announced break date. Disposition: MECHANISM.**

   **Evidence:** docs/V1-DERIVATION-DRAFT.md:55-57, :65-69 defines offline authority/time checks with revocation NOT_EVALUATED; docs/phase-0-prereg-amendment-3.md:503-508 distinguishes unsupported algorithms, prohibited algorithms and failed signatures.

   To use the strengthened authenticity claim after a break, a verifier needs independently trusted policy/evidence establishing a conservative safe historical interval for the signing algorithm and relevant keys, plus historical authority validity and trustworthy anchored existence before its end. The public discovery date is not proof that secret attacks were impossible earlier. For key theft, discovery/decommission dates likewise do not establish the first possible compromise time. A safe-before cutoff may instead be a declared trust assumption, which must be visible. Per-key assumptions matter; both signatures existing by T does not itself prove both keys were honest until T.

   Compare the trusted existence upper bound with the cutoff, accounting for the registered chain-time uncertainty: a Bitcoin header timestamp is not an exact external UTC clock. If there is no defensible time bound strictly before the cutoff, the historical conclusion is not established. Because T is the earliest attestation in the presented proof, pruning away an earlier attestation can remove this evidence; it cannot legitimately move a new signature into the past. Use only verified presented attestations and fail to establish the historical conclusion when the needed earlier proof is absent.

   **Recommendation:** specify where authenticated, versioned historical security policy comes from in an offline verifier and how uncertainty is reported. Do not treat a syntactically valid signature under a now-broken algorithm as sufficient, or silently turn NOT_EVALUATED revocation into historical assurance. Existing A3 policy prohibitions must be reconciled with any policy allowing historical use. If this policy is outside V1 scope, keep the benefit conditional in prose and expose the missing assessment; do not claim that the current verifier establishes it.

9. **HIGH — Authority and anchor longevity remain independent failure points. Disposition: WORDING.**

   **Evidence:** docs/V1-DERIVATION-DRAFT.md:55-57, :62, :65-66 depends on DNSSEC, the repository key, SHA-1 git linkage, OTS and pinned Bitcoin history, with no renewal. formal/p8/ENCODING-V1.md:325-330 anchors snapshot bytes; formal/p8/PROOF.md:60-64 expressly excludes git linkage from P8's SHA-256-only scope.

   Signature inclusion addresses attestation signing, not every dependency. Historical DNSSEC evidence must preserve its signed records and chain; historical git evidence must bind the signature and the exact commit→tree→blob path used to assert keys. Independently check what its OTS commitment covers: an unsigned commit alone permits a comparable later-signing gap, and even an anchored signed commit does not upgrade SHA-1 links to SHA-256 bindings. This is a separate obligation, not a demonstrated authority exploit here. Historical root/repository-key trust remains external to the receipt.

   Later ability to rewrite accepted chain history, exploit OTS/hash commitments, substitute hash-linked objects, or corrupt the trusted pins can defeat the argument despite signature timestamps. Quantum ability to forge P-256 signatures does not automatically imply those breaks, but neither does signature inclusion guarantee their absence. [RFC 4998 §1.2](https://www.rfc-editor.org/rfc/rfc4998.html#section-1.2) distinguishes timestamp renewal from hash-tree renewal when preservation dependencies weaken.

   **Recommendation:** state the continuing hash/anchor/history and authority-binding residual explicitly. Do not introduce a renewal service as an implicit V1 gate; V1 deliberately excludes renewal. Audit the git anchor target and snapshot body coverage before claiming end-to-end post-break survivability.

10. **MEDIUM — P8's existing proof and vectors cannot be cited as evidence for the new anchor. Disposition: MECHANISM.**

    **Evidence:** formal/p8/PROOF.md:40-49 defines Anc and accepted receipts without signatures; :209-217 proves injectivity only for frame pairs; :258-268 and :283-289 state that narrower theorem. formal/p8/vectors/gen.py:303, :354, :649, :814-823 implements/tests the old anchor. formal/p8/vectors/check.py:481-506, :528-540 independently implements that same layout. formal/p8/vectors/fuzz.py:3-5, :32-56 fuzzes JSON ingestion and frames, not anchors or signatures.

    **Recommendation:** revise the encoding map, §5, W1 wording and D-8; extend the accepted tuple/domain to exact signatures; revise Lemma 7 and theorem (iv) to recover ordered frame/signature tuples. The receipt structure is then `(M,C,S_kms,S_gpg)`, not a deterministic function of `(M,C)` alone. Keep the byte codec's injectivity distinct from signature unforgeability and temporal composition. Update both independent codecs and the golden anchor/receipt digests, rejection vectors and their boundary offsets. Add malformed signature-length, empty/extra packet, swapped signature/slot, replaced signature, truncation and trailing-byte cases. Extend differential fuzzing to the composite anchor.

    Add a cryptographic integration negative control: two valid signatures over the same frame (or a valid malleated form), only one anchored; the other must fail the old anchor despite signature verification succeeding. Separately demonstrate the old-layout pre-stage/later-sign case and rejection under the new layout. Existing green vectors only establish the current codec agreement; no updated tests or proofs were run in this review.

11. **LOW — Simpler alternatives either preserve this mechanism or reduce the claim. Disposition: WORDING.**

    **Evidence:** docs/V1-DERIVATION-DRAFT.md:39-56 states the combined authenticity/time claim; formal/p8/ENCODING-V1.md:307-319 already provides one ordered composite preimage; docs/phase-0-prereg-amendment-3.md:473-482 bounds the PQ commitment.

    The smallest mechanism change is the two extra length-prefixed detached signatures. Hashing a precisely encoded signed-receipt core is equivalent, provided the core excludes its own OTS proof and unsigned transport decoration. Using fixed-width signature hashes can shorten the preimage but adds an explicit hash binding and representation obligation; it is not an unconditional injective encoding of signatures. Anchoring signatures alone can bind documents under additional signature/hash assumptions, but retains less explicit frame evidence and is not a simpler P8 proof.

    The truly simpler scope alternative is to claim only “these frames existed by T; their signatures verify now,” assuming present unforgeability and making no assertion that signing/presentation occurred by T. That abandons the disputed historical guarantee and is unattractive for the stated notary claim. Adding PQ alone delays an algorithmic failure but does not solve later theft of every required key with frame-only anchoring.

    **Recommendation:** prefer direct signature inclusion. Route any choice to weaken the combined historical claim to the author explicitly; do not present it as an equivalent repair.
