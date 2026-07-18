# External Review: Phase 0 Pre-Registration Amendment 1

Review artifact, committed per Amendment 1 §A1.7. This review was conducted by the AI partner **Antigravity** to identify any remaining gaps, inconsistencies, or overclaims in the revised draft of [phase-0-prereg-amendment-1.md](../phase-0-prereg-amendment-1.md).

---

## Reproducibility Record

- **Reviewer Model:** Antigravity (Gemini 3.5 Flash)
- **Date:** 2026-07-03
- **Reviewed Inputs:**
  - Base Pre-Registration: [phase-0-prereg.md](../phase-0-prereg.md) (commit `75207ba`)
  - Amendment 1 Draft: [phase-0-prereg-amendment-1.md](../phase-0-prereg-amendment-1.md) (as of 2026-07-03)
- **Configuration:** Default reasoning settings (Medium temperature).
- **Prior Transcripts:** The reviewer analyzed the prior GPT-5.5 round 1 and round 2 reviews.

---

## Disposition summary (author + AI collaborator, 2026-07-03)

All six findings were verified against the amendment text and
incorporated; three needed corrections to the proposed fix, recorded here
so the divergence between finding and disposition is auditable:

1. **Wrapper re-serialization (P7) — confirmed, blocking.** Incorporated
   as opaque byte-string embedding only. The review's alternative fix
   ("or commit to its cryptographic hash") was **rejected**: hash-only
   commitment requires the inner bytes to travel outside the bundle,
   breaking the self-containment that P9 exists to guarantee.
2. **Anchor confirmation depth (P5) — confirmed, blocking.** Incorporated:
   "confirmed" now means buried at minimum depth k (strict default k = 6,
   ratified with δ/ε at Band 0 exit); shallow or reorged anchors force
   re-issue. One nuance: the "permanently `UNVERIFIABLE`" consequence
   applies only to receipts *shipped* before depth — which is precisely
   why depth belongs in the issuance-completion rule.
3. **Key-lifecycle monotonicity (P6) — confirmed in substance; placement
   corrected.** The review proposed filing it under the Bitcoin Layer 2
   assumptions. It is not a cryptographic assumption; it is an issuer
   key-management **design commitment** (revocation is terminal; re-keying
   mints a new key with a new fingerprint and manifest entry). Stated in
   P6, where the interval semantics live, as a rule the model assumes and
   operational policy enforces.
4. **Length-prefix placement (P8) — confirmed; wording corrected.** The
   review's text had the *verifier* constructing and signing the frame;
   the **issuer** signs — the verifier independently reconstructs and
   rejects mismatch. The frame is also wider than a length prefix:
   `type_tag || canonicalization_version || payload_length || payload`,
   with the exact binary layout fixed, with golden vectors, before the
   Band 1 freeze.
5. **Historical trust-anchor store (A1.5) — confirmed.** Incorporated,
   with one added clause: the store is verifier-side trust
   *configuration*, distributed with the verifier — not service-side
   state — so P9 is not violated.
6. **Cross-model divergence (A1.4) — confirmed.** Incorporated: the
   informal written proof must include an explicit correspondence mapping
   between TLA+ transitions and the symbolic tool's rules/facts; the
   conformance vectors test both against the same implementation, which
   bounds but does not eliminate the risk.

---

## Overall Assessment

The revised [phase-0-prereg-amendment-1.md](../phase-0-prereg-amendment-1.md) is a highly rigorous, mature, and sound framework. It successfully addresses the previous adversarial rounds, hardening the agreement gate and establishing a solid mathematical basis for the verifier state machine and temporal parameters.

However, as a falsification exercise, this review has identified **three blocking findings** and **three precision/clarity fixes** that must be resolved before the amendment is signed and anchored.

---

## Blocking Findings (Falsification Gaps)

### 1. Canonicalization Preservation inside Wrappers (P7/P8 Structural Gap)
* **The Gap:** P7 states: *"A wrapper commits to the inner package's bytes and records both inner and outer canonicalization versions. Wrapping never alters the inner package's independently-computed verdict — the wrapper attests the inner bytes..."*
  If the wrapper encodes the inner package as a standard nested JSON object/dictionary, JCS serialization (RFC 8785) of the outer wrapper under potentially different canonicalization rules will re-serialize the inner package's values. If the two canonicalization versions differ (e.g., float representation, Unicode escaping, key order), the canonical bytes of the inner package will change. This will permanently break the inner signatures, violating P7's core guarantee that wrapping never alters the inner verdict.
* **The Solution:** The wrapper must treat the inner package as an opaque byte sequence (e.g., a base64-encoded string of its JCS-canonical bytes) or commit to its cryptographic hash rather than embedding it as a nested JSON object.
* **Proposed Text Edit to P7:**
  ```diff
  - A wrapper commits to the inner package's bytes and records both inner and outer canonicalization versions.
  + A wrapper commits to the inner package's bytes by wrapping them as an opaque, encoded string (e.g., base64 of its JCS bytes) or by cryptographic hash, and records both inner and outer canonicalization versions. This ensures outer canonicalization rules cannot re-serialize or alter the inner package's byte stream.
  ```

### 2. Reorganization Depth and Anchor Confirmation Policy (P5 Temporal Gap)
* **The Gap:** P5 states: *"issuance is not complete until the anchor confirms within δ of declared_issue_time."*
  However, it does not define what "confirms" means in the context of the Bitcoin blockchain. If a receipt is issued after just 1 block confirmation, a transient blockchain reorganization (reorg) could orphan that block. If the OTS transaction is lost in the reorg, the receipt becomes permanently `UNVERIFIABLE`.
* **The Solution:** We must define a minimum confirmation depth (e.g., 6 confirmations, ~1 hour) before the anchor is considered "confirmed" and the receipt is finalized for shipping.
* **Proposed Text Edit to P5 (Issuance-protocol corollary):**
  ```diff
  - issuance is not complete until the anchor confirms within δ of declared_issue_time.
  + issuance is not complete until the anchor achieves a secure confirmation depth (minimum 6 blocks on the Bitcoin mainnet) within δ of declared_issue_time.
  ```

### 3. Key Lifecycle Monotonicity (P6 State Machine Gap)
* **The Gap:** P6 requires `key_authorized(declared_issue_time) ∧ no revocation effective at or before anchor_time`.
  If a key undergoes a temporary revocation and is subsequently re-authorized (e.g., a temporary suspension or key rotation mistake that is reverted), point-in-time checks become non-monotonic. A revocation event at $T_{revocation} \le anchor\_time$ would permanently invalidate the receipt even if the key was active and authorized during a later valid window containing both the declared and anchor times.
* **The Solution:** The system must explicitly assume key lifecycle monotonicity: once a key is revoked, it remains revoked permanently and can never be re-authorized.
* **Proposed Text Edit to A1.6 (Layer 2 assumptions, extended):**
  ```diff
  - consensus rules (median-time-past, the two-hour future bound) bound but do not eliminate skew — absorbed into δ and ε; and the proof-of-work history remains intact and available over the adjudication horizon.
  + consensus rules (median-time-past, the two-hour future bound) bound but do not eliminate skew — absorbed into δ and ε; the proof-of-work history remains intact and available over the adjudication horizon; and key authorizations are monotonic (once revoked, a key is permanently revoked and can never be re-authorized).
  ```

---

## Precision and Wording Fixes

### 4. Length Prefix Binding (P8 Ambiguity)
* **The Gap:** P8 states: *"canonical() is injective on its accepted payload domain, and the encoding is boundary-unambiguous (length bound into the bytes... rejection is required for... length-prefix mismatch)."*
  Since RFC 8785 (JCS) produces standard JSON without a length header, the spec does not explain where the length prefix is injected.
* **The Solution:** Clarify that the verifier constructs the JCS bytes, calculates the length, prepends the length prefix, and signs/anchors the concatenated `length_prefix || JCS_bytes` structure.
* **Proposed Wording Edit to P8:**
  ```diff
  - (length bound into the bytes; a parser cannot disagree about where the payload ends).
  + (the verifier prepends a length prefix to the JCS-canonicalized bytes, and the signatures and anchor commit to the concatenated length_prefix || JCS_bytes structure, preventing parser disagreement about where the payload ends).
  ```

### 5. Historical Trust-Anchor Database (A1.5 Archival Detail)
* **The Gap:** DNSSEC snapshots are validated against historical DNS root keys (KSK). If the verifier is offline and "dead" per P9, it must still verify snapshots years later after the DNS root keys have rolled over.
* **The Solution:** Explicitly note that the offline verifier must maintain a historical trust-anchor store (an archive of historically trusted roots) to successfully evaluate archived DNSSEC snapshots and repository GPG keys.
* **Proposed Wording Edit to A1.5 (Trust-anchor recursion):**
  ```diff
  - A verifier decades later needs trustworthy knowledge of those historical anchors — which is itself a historical-authority question.
  + A verifier decades later needs trustworthy knowledge of those historical anchors — requiring the verifier software to maintain a database of historical trust-anchors (DNS root keys and repository GPG keys) or rely on periodic wrapping.
  ```

### 6. Cross-Model Divergence Risk (A1.4 Tooling Gap)
* **The Gap:** By splitting verification between TLA+ (state machine) and Tamarin/ProVerif (active adversary protocol), there is a risk that the two symbolic models represent slightly different behaviors, leading to a false sense of security.
* **The Solution:** Require the informal written proof to map TLA+ state transitions to Tamarin/ProVerif protocol facts/rules to ensure semantic equivalence.
* **Proposed Wording Edit to A1.4 (The readability trade-off, named):**
  ```diff
  - every symbolic-verifier lemma carries a prose mapping back to the A1.2 property it discharges, and the informal written proof (H0 requirement 3) covers the composition argument in the author's own words regardless of tool.
  + every symbolic-verifier lemma carries a prose mapping back to the A1.2 property it discharges, the informal written proof (H0 requirement 3) covers the composition argument in the author's own words, and we explicitly map TLA+ state transitions to symbolic protocol facts to prevent cross-model representation divergence.
  ```

---

## Verdict Summary

| Section | Target | Severity | Finding |
| :--- | :--- | :---: | :--- |
| **P7** | Wrapper soundness | **Blocking** | Outer canonicalization re-serializes nested JSON, altering inner bytes. |
| **P5** | Temporal soundness | **Blocking** | Reorgs could drop 1-confirmation anchors, making receipts unverifyable. |
| **A1.6** | Layer 2 assumptions | **Blocking** | Re-activation of revoked keys violates static point-in-time checks. |
| **P8** | Canonicalization | *Precision* | Location of length prefix is unspecified relative to JCS. |
| **A1.5** | Manifest authority | *Precision* | Offline verifiers need a database of historical roots to check DNSSEC. |
| **A1.4** | Tooling | *Precision* | Divergence between TLA+ state variables and Tamarin protocol facts. |
