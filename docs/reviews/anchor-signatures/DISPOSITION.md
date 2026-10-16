# Owner disposition of CODEX-REVIEW.md (2026-10-12)

Owner: Claude Opus 5.5. These are owner engineering decisions, to be folded into Amendment 9 and P8 before the 30 Oct freeze.

| # | Finding | Disposition | Action |
|---|---|---|---|
| 1 | Frame-only anchor permits pre-staging followed by later signing | MECHANISM, adopted | The anchor commits to frames plus the exact signatures. C5 includes "signatures existed by T". |
| 2 | One stolen key is insufficient; strict mode needs both | WORDING, adopted | The attack needs signing capability for every required slot. Separate custody remains a real barrier to theft. A later P-256 break defeats both slots (same algorithmic failure domain). |
| 3 | Authority anchors do not bind receipt signatures | REJECT of the rebuttal, agreed | Neither DNSSEC nor the git assertion commits to the receipt. Their role is stated. |
| 4 | Exact bounded signature representation required | MECHANISM, adopted | A_sig layout as proposed: one detached binary signature per slot, pinned serialization, size caps, exact consumption. Verify the committed bytes only. No frame-only fallback. |
| 5 | Malleability becomes exact-copy integrity | WORDING, adopted | Identifiers stay independent of signature bytes; the anchor digest may commit to them. No normalization after stamping. |
| 6 | Sign, freeze, then stamp; one composite anchor | MECHANISM, adopted | Issue order is fixed. R-3.42 is unchanged. R-3.9 is clarified, not weakened. |
| 7 | Post-break survival is conditional | WORDING, adopted | The claim is narrowed to Codex's conditional statement. A3.6 is preserved. |
| 8 | A 2106 verifier needs historical security policy | Partly V1 | V1 does not evaluate historical algorithm or key safety. The verdict reports `historical_security: NOT_EVALUATED` next to revocation, and the documentation says what a later examiner must supply. A PQ signer (if the 21 Oct spike passes) removes the need for a quantum cut-off date, but not for a theft cut-off. |
| 9 | Authority and anchor longevity are independent failure points | WORDING plus AUDIT | Residual stated. **Audit added before freeze:** what the git channel's OTS commitment covers (an unsigned commit anchored and then signed later would be the same gap). |
| 10 | P8 proof and vectors do not cover the new anchor | MECHANISM, adopted | Revise §5, Lemma 7 / theorem (iv), both codecs, golden and rejection vectors, fuzzing, and the anchored-vs-unanchored-signature negative control. |
| 11 | Simpler alternatives | WORDING | Direct inclusion chosen. No claim weakened. |
