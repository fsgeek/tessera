# Codex review — A9 slot-2 custody delta

2026-10-13. Scope: `delta.diff` against the current proposed A9. Read A9 §A9.0, §A9.2, §A9.3 and §A9.6 in full, the opening claim/adversary/boundaries and C1–C7, ENCODING-V1 §3.3 and §5.2–5.4, and P8 PROOF's assumptions and relevant signature discussion. Searched `docs/` and `formal/` Markdown for `gpg`, `token`, `YubiKey` and `author-controlled`, and inspected the P8 codec/vector references. No implementation or provider deployment was tested. Only this review file is edited.

**Verdict:** provider-neutral custody is compatible with the existing claims and rule O. The delta does not establish that every non-AWS HSM deployment preserves the existing signer policy. Resolve the enforcement-boundary and deadline findings below before describing the alternatives as interchangeable. No demonstrated counterexample to C1–C7 follows from the text edit alone.

Severity: HIGH = an allowed deployment can lose an explicitly retained protection; MEDIUM = registration/evidence or governing-document inconsistency; LOW = clarification without a changed verdict.

## 1. HIGH — Non-AWS key location does not preserve the declared-time enforcement boundary

**Location:** A9:299–301, 322–328, 335–339; C3 at :136 and :376–380; PROOF:109–110.

The declared-time paragraph is unchanged: the second signer inspects the frame and compares `declared_issue_time` with its own clock, within ε. Its meaning remains issuer-side refusal, not a verifier check, proof of actual issue time, or lower time bound. But the new alternative specifies only key custody. A cloud KMS/HSM normally accepts a digest/signing request; it does not parse a V1 frame or apply this clock rule.

Concrete allowed failure: run the queue consumer and OpenPGP adapter in the issuing AWS account, give it direct use-to-sign permission at the non-AWS provider, and retain an HSM-generated non-exportable key. An AWS takeover replaces the adapter, bypasses the clock check and requests signatures on backdated frames. Hardware location and non-exportability still meet the custody paragraph. The original queue-fed external signer protection no longer holds. This also exposes PROOF assumption (K): a generic signing endpoint does not itself restrict a key to V1 tagged type-0x00 documents. A token likewise needs host-side policy; hardware alone never enforced these conditions.

This is an underspecified deployment boundary, not proof that every HSM choice breaks C2 or C5. Their registered key-use and commitment assumptions remain conditional. Nor does it alter C4's verifier window rule or turn ε into a bound on Bitcoin backward skew.

**Proposed exact fix:** append to the slot-2 custody paragraph:

> In either custody option, a queue-pulling policy signer outside the issuing AWS account validates the complete V1 frame and enforces the declared-time check using its own clock before requesting a signature. The issuing AWS account can enqueue frames but cannot invoke the slot-2 key directly, change that policy or clock, or obtain the policy signer's key-use credentials. The slot-2 key is dedicated to V1 tagged type-0x00 documents (attestation and manifest-possession). The dated custody record names this enforcement boundary and its access policy. Non-exportability protects against key export, not signing misuse through the permitted queue path.

Also append to the declared-time paragraph:

> For an HSM-backed key, this refusal is enforced by the policy signer, not by the HSM's generic signing API.

If AWS can administer that signer or call the key directly, the owner must instead explicitly withdraw the protection; calling that deployment equivalent would change the retained mechanism.

## 2. MEDIUM — A custody choice made after 21 Oct cannot supply the hybrid's required deployed-slot evidence by 21 Oct

**Location:** A9:303–317, 322–334; A9.2:189–206.

Owner selection before 30 Oct is not intrinsically a freeze violation: both custody alternatives are now explicitly registered, and the owner records which was chosen before the freeze. A9.2 permits instrument outputs to select registered branches, provided instrument code stays in its permitted locations and is never imported by service code.

There is nevertheless a deadline ambiguity. The hybrid pass condition requires a real P-256 signature from the second slot **as deployed**, and the selected byte profile/key-use evidence, all by 21 Oct. Testing a token by 21 Oct and choosing an untested HSM adapter on 29 Oct does not meet that condition for the final deployed pair. The supplement cannot waive it: its authorization is bounded to the pair identifier/mode/context, the rule-R edit and completed pass evidence, “and nothing else”. Custody selection does not authorize changing rule O or silently extending the spike deadline. The fallback has no equivalent 21 Oct condition, but still needs the whole 30 Oct exit.

**Proposed exact fix:** append to the custody paragraph:

> For the hybrid, the final custody implementation must have completed the deployed-slot pass-condition evidence by 21 Oct. The owner may defer selection until before 30 Oct only among custody implementations that each met that deadline; otherwise the registered fallback is taken. A custody selection changes neither rule O nor any claim, pass condition or exit obligation. Record the selected implementation and its evidence references, dated, in the profile before the freeze for either algorithm branch.

No expansion of the hybrid supplement is necessary if rule O stays identical. A changed serialization, fingerprint definition or key-use contract would exceed this bounded selection mechanism and require its own authorization. The existing raw-ML-DSA versus PROOF-(K) mismatch predates this delta and is already explicitly assigned to the hybrid pass condition at A9:313–315; the HSM option does not resolve or newly create it.

## 3. MEDIUM — Governing encoding and current V1 documents still prescribe the token/local option

**Location:** ENCODING-V1:441; V1-PROFILE:348–349; V1-OPERATIONS-RUNBOOK:11–13, 18–20, 32–35, 48–52, 58–61; V1-DERIVATION-DRAFT:47, 64, 249–251.

ENCODING-V1's hybrid row still says “rule O (P-256, hardware token; owner decision 2026-10-12 replaced SLH-DSA)”. This is a normative table in A9's governing encoding baseline, not merely an old review quote. The new custody choice needs to be reconciled with it. The profile's fallback still requires gpg on author-controlled hardware. The runbook partially recognizes the new token branch at :25, yet unconditionally specifies YubiKey 1 at :11, calls the HSM migration “Path past V1”, titles §3 “Token-side”, and prescribes a token reset at exit. These instructions are inconsistent for an HSM selection.

**Proposed exact fixes (not applied):**

- ENCODING-V1:441: replace `rule O (P-256, hardware token; owner decision 2026-10-12 replaced SLH-DSA)` with `rule O (OpenPGP P-256; slot-2 custody per A9.6; owner decision 2026-10-12 replaced SLH-DSA)`.
- V1-PROFILE:348–349: replace the fallback bullet with `- Fallback: both slots OpenPGP P-256 (rule O), KMS-backed for kms, and slot-2 custody per A9.6 for gpg. The dated pre-freeze custody record identifies the selected implementation.` Retain an updated source citation.
- Runbook:11: replace the bullet label with `**If token custody is selected: YubiKey 1, the gpg signing token.**`; :18: replace the label with `**Loss of the selected slot-2 token.**`.
- Replace the runbook's “Path past V1” bullet (:32–35) with `**Alternative V1 custody (A9.6):** an HSM-generated non-exportable P-256 key at a non-AWS provider, used through the external queue-pulling policy signer. The dated profile choice records the provider, key version, policy boundary, OpenPGP adapter and immutable public-key packet. Its authority is evidenced through the same DNSSEC and signed, anchored git key-publication record.`
- Runbook §3: rename `Token-side declared-time check` to `Slot-2 declared-time check`; append `For HSM custody, the external policy signer enforces this check before submitting the OpenPGP digest; AWS has no direct key-use permission.`
- Runbook §4 item 2: replace the second-key instruction with `initiate destruction of the selected slot-2 key (token applet reset, or the non-AWS provider's key-version destruction procedure)`; item 3: replace `the token reset is done` with `the selected slot-2 key's destruction has completed`.
- Derivation draft :47: replace `cloud HSM and local hardware token` with `AWS KMS and the selected slot-2 custody`; :64 and :250–251: replace the local-hardware sentences with `The gpg slot uses rule O under A9.6's selected slot-2 custody, through a queue-pulling policy signer outside the issuing AWS account.` Mark this as a dated reconciliation of a draft, preserving its decision history.

GnuPG's observed header at ENCODING-V1:471–477 and PROOF:475 is valid experimental evidence; it need not be erased. Original preregistration, earlier amendments, review quotes/dispositions and earlier spike evidence should likewise remain as history. `gpgsig` in the git channel refers to the repository signature, not the attestation slot's custody. “Token” in JCS number parsing is unrelated.

## 4. LOW — “Independent failure domain” needs the same limited reading for both options

**Location:** A9:300–301, 322–328, 376–380.

A token on an external host and an HSM at a different provider can provide separate technical key-custody domains. Neither gives independent signing fates: the common AWS-fed queue can cause both keys to sign, both keys remain under one controller, and a P-256 break defeats both fallback slots. C3 explicitly retains these limits. A non-AWS provider name alone does not establish independence of the signer host, administration, IAM, clock or availability. Nor is end-to-end issuance availability independent of AWS when AWS supplies the queue.

**Proposed exact fix:** replace `in a failure domain independent of the issuing AWS account` at A9:300 with `in a separate technical key-custody domain outside the issuing AWS account`; append to slot-2 custody:

> Separate technical custody does not imply independent availability, independent signing fates, separate control or independent approval of content; C3 applies to both options.

This preserves the defensible custody distinction and avoids reading it as a stronger guarantee. Finding 1 specifies the separate policy boundary necessary for the existing clock protection.

## Rule O feasibility and claim audit

**A cloud HSM key can produce rule O through an adapter; its raw ECDSA output is not itself rule O.** For example, Google documents P-256/SHA-256 asymmetric signing and HSM protection, and its ECDSA API returns DER-encoded signatures. RFC 9580 specifies that OpenPGP signs the hash of the document plus signature metadata and trailer. These together support the feasibility inference, not a tested Tessera deployment. Sources: [Google algorithms](https://docs.cloud.google.com/kms/docs/algorithms), [Google signing API](https://docs.cloud.google.com/kms/docs/create-validate-signatures), [RFC 9580 §5.2.4](https://www.rfc-editor.org/rfc/rfc9580.html#section-5.2.4).

The adapter must hash the exact frame with v4 type-0x00/ECDSA/SHA-256 metadata, hashed subpackets and trailer; ask the HSM to sign that digest without accidentally hashing it again; convert the ECDSA result to canonical OpenPGP MPIs r/s; add the digest's left 16 bits and subpacket areas; emit exactly one shortest legacy-header packet within the 1024-byte cap; and freeze those bytes before stamping. Both attestation and manifest-possession signatures must verify under the designated key. RFC 6979 test-vector nonces are not a rule-O production requirement.

For the gpg slot, exporting the HSM's public point is sufficient to construct the v4 public-key packet body at ENCODING-V1 §3.3; exporting a private key is unnecessary. Fix and retain one u32 creation value and packet body when publishing the key. Compute `gpg-sha256` over that entire body, including creation time, not over provider SPKI, resource name or the SHA-1 fingerprint printed by GnuPG. Reconstructing the body with a new creation timestamp changes the designated fingerprint even with the same point. The packet creation value is key metadata, not an authenticated issue-time measurement. Missing GnuPG-specific issuer subpackets is not inherently a failure: rule O checks their structural encoding, and PROOF explicitly says the GnuPG SHA-1 issuer fingerprint subpacket is not read by a V1 check.

The existing KMS-backed classical slot already demonstrates that rule O's contract is about bytes and signature semantics rather than invoking the gpg executable. The remaining token-specific table wording is finding 3. Dedicated key use (K) remains an operational assumption for either custody option; do not infer it from generic HSM signing support.

**Answers to the requested checks:**

1. C1–C7, the adversary paragraph, the C3 single-controller/no-independent-fates non-claim and the declared-time rule are not substantively changed by the delta. C3's final custody example changes. Their evidence and operational assumptions must still be met; finding 1 prevents treating mere key location as enforcement.
2. Rule O is feasible with an HSM adapter under the exact unchanged byte contract. No P8 injectivity argument requires a token or gpg executable. Key-use restrictions, type-0x00, immutable packet creation metadata/fingerprint and pre-stamp serialization still apply.
3. Separate technical custody is possible with either option; broad independence from AWS or independent fates is not established. See findings 1 and 4.
4. Pre-freeze owner selection is authorized by the newly enumerated alternatives; it does not authorize post-deadline evidence or additional encoding changes. See finding 2.
5. Current encoding/profile/runbook/draft inconsistencies are listed in finding 3. Historical documents are not silently rewritten. A9 remains PROPOSED in the inspected file; this review does not claim adoption, P8 discharge or deployment conformance.
