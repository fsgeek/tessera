The revision substantially resolves the earlier review, but **is not ready for signature**: the new discharge rule still lacks a binding between the tested verifier code and deployed code, and the expanded sweep found an unaccounted registered KMS-role commitment.

Read-only review completed. Scratch was confined to `/tmp/tmp.4xaTjTpu57`; no repository edits or git writes were made.

**A. Earlier findings**

References below use `A11` for [the revised amendment](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md).

| Finding | Status | Evidence |
|---|---|---|
| A11-01 — floor and discharge prerequisites | **PARTIAL** | A11:41–69 retains the fields, pins the floor, separates adoption from discharge, and blocks unresolved defects. The deployed-code binding remains insufficient; see A11C-01 below. |
| A11-02 — retrospective custody exception | **CLOSED** | A11:12–14 explicitly discloses the late, outcome-informed relaxation. A11:112–120 distinguishes historical qualification from replacement qualification and explains why R5b does not settle it. |
| A11-03 — spike-key deletion | **CLOSED** | A11:137–140 preserves deletion. [DEPLOY.md:18](/home/tony/projects/tessera/service/issuer/DEPLOY.md:18) now requires new production keys; lines 23–30 prescribe replacement and deletion. Actual deletion remains an operational obligation, not a completed fact. |
| A11-04 — complete enforcement boundary | **CLOSED** | A11:121–130 incorporates every A9.6 requirement and requires deployed positive/refusal evidence, requester/admin review, retirement, and image/configuration identification. This closes the wording finding; it does not establish deployment conformance. |
| A11-05 — policy versus implementation defects | **CLOSED** | A11:74–81 separates later security assessments from implementation-conformance defects and requires explicit release corrections. |
| A11-06 — 219/21 vector split | **CLOSED** | A11:60–62 states precisely which cases reach the library and which reach neither interface. |
| A11-07 — retrospective disclosure and vacuity | **CLOSED** | A11:8–16 separately discloses the changes; A11:27 retains the four applicable ML-DSA fields. The stale PENDING statement is gone. |
| H3 notes | **CLOSED in the amendment** | A11:105–111 uses “AWS-based,” includes every provider and retained resources, requires a prior measurement protocol, and prohibits redefining the window to avoid falsification. |
| Citation notes | **CLOSED** | A11:89–90 pins the historical profile and corrects the supplement locator; A11:135 identifies S1 as an unregistered owner operational resolution. |

The supporting sweep still needs editorial reconciliation: [SWEEP:11](/home/tony/projects/tessera/docs/reviews/stale-dependencies/SWEEP-2026-10-28.md:11) continues to describe H3 as assuming an all-AWS demonstration and “AWS-only wording,” contrary to the corrected amendment’s reading.

**Manifest verification:** all **15 entries passed** `sha256sum -c`. The manifest’s own SHA-256 is:

`c571ee99f55d46a4b2dceb399c872c71f829a60290c20ce933ef2e960969b4d5`

This matches A11:55.

**B. Defect in the revised discharge rule**

**A11C-01 — High: the prescribed deployment identity check does not bind the tested verifier implementation to deployment.**

[A11:63](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:63) now establishes explicit discharge conditions, including `test_deployed_zip_identity`. But:

- [test_p3_profile.py:62](/home/tony/projects/tessera/formal/p3-verification-profile/test_p3_profile.py:62) checks only the zip’s cryptography native-binding hash and wheel tag.
- [test_p3_profile.py:25](/home/tony/projects/tessera/formal/p3-verification-profile/test_p3_profile.py:25) selects the working-tree verifier; lines 39–43 import its behavior.
- [test_p3_profile.py:151](/home/tony/projects/tessera/formal/p3-verification-profile/test_p3_profile.py:151) applies that limited zip check to the supplied artifact.

Consequently, a tested checkout and deployed zip can contain different verifier Python code while sharing the same cryptography wheel. The prescribed checks can pass without establishing that the deployed implementation exhibits the tested behavior.

**Required repair:** make discharge require either running the floor against verifier code extracted from the authenticated deployed artifact, or verifying an explicit identity binding between all tested verifier code and that artifact. Preserve the separate requirement to establish that the supplied artifact is actually deployed.

This is a remaining inadequacy in A11-01 made consequential by the revision’s explicit discharge rule, rather than evidence that a current deployment is defective.

**C. Expanded registered-record sweep**

**1. Additional unresolved commitment: K-R assigns signing authority and μ computation to the issuer.**

Registered side:

- [HYBRID-SUPPLEMENT.md:61](/home/tony/projects/tessera/formal/p8/HYBRID-SUPPLEMENT.md:61) specifies issuer computation of external μ.
- [HYBRID-SUPPLEMENT.md:151](/home/tony/projects/tessera/formal/p8/HYBRID-SUPPLEMENT.md:151) expressly makes issuer-computed μ part of K-R.
- [HYBRID-SUPPLEMENT.md:170](/home/tony/projects/tessera/formal/p8/HYBRID-SUPPLEMENT.md:170) specifies `kms:Sign` only for the issuer role and issuer code constructing V1 frames.
- [HYBRID-SUPPLEMENT.md:533](/home/tony/projects/tessera/formal/p8/HYBRID-SUPPLEMENT.md:533) repeats the issuer-role policy commitment.

Current owner side:

- [signer-placement decision:19](/home/tony/projects/tessera/docs/decisions/2026-10-27-v1-signer-placement.md:19) assigns signing to a separate signer role and keeps issuer roles without KMS permissions.
- [signer-kms/README.md:3](/home/tony/projects/tessera/service/signer-kms/README.md:3) describes that separate Lambda and role; line 30 places external-μ signing there.
- [DEPLOY.md:49](/home/tony/projects/tessera/service/issuer/DEPLOY.md:49) installs the signer-only key policy.

The placement decision nevertheless says it **“changes no registered sentence”** at [line 4](/home/tony/projects/tessera/docs/decisions/2026-10-27-v1-signer-placement.md:4).

This may preserve or strengthen the intended restriction on signed messages, but it changes the registered description of its enforcement. I found no explicit registered supersession covering it. A11’s [change table:85](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:85) also omits it.

**Disposition needed:** explicitly reconcile K-R’s issuer/code/role wording with the dedicated policy signer, retaining pure mode, empty context, frame validation, key dedication, and the stated administrative-capture limitation. This is an existing deployment drift newly found by this confirmation sweep.

**2. Spike-key correction remains inconsistent in subordinate deployment instructions.**

Registered side: [HYBRID-SUPPLEMENT.md:524](/home/tony/projects/tessera/formal/p8/HYBRID-SUPPLEMENT.md:524) requires deletion after the stated conditions.

Current owner documents still contain:

- [deploy.sh:30](/home/tony/projects/tessera/service/signer-gcp/deploy.sh:30): `KEY=slot2-spike`, described as the key V1 uses today, with the historical creation time and fingerprint.
- [signer-gcp/README.md:200](/home/tony/projects/tessera/service/signer-gcp/README.md:200): deployment instructions granting the production runtime access to `slot2-spike`.

[DEPLOY.md:25](/home/tony/projects/tessera/service/issuer/DEPLOY.md:25) explicitly requires replacing those values, so this does **not** reopen A11-03’s policy decision. It leaves stale executable defaults and contradictory subordinate instructions. Reconcile them before deployment.

**3. Retained obligations that remain pending, rather than contradicted or waived.**

[FREEZE-RECORD.md:84](/home/tony/projects/tessera/formal/freeze-v1/FREEZE-RECORD.md:84) still requires the GCP VPC Service Controls perimeter and an unsolicited-response policy before the first public verifier release. The current deployment checklist’s omission of these is not a registered cancellation. They remain release gates.

The registration record’s placeholder specification hash is already handled by [FREEZE-RECORD.md:25](/home/tony/projects/tessera/formal/freeze-v1/FREEZE-RECORD.md:25); it is not an additional unresolved defect.

I found no further contradictory commitment in the requested records and comparisons. Draft/PENDING predecessors and archived captures were treated as historical evidence, not fresh production requirements.

**Freeze verification:** reassembly from `270ca49` reproduced all five objects byte-for-byte. Their recorded hashes and lengths match; all **6 specification parts and 387 vector parts** match that commit. The frozen profile’s historical-key versus production-key distinction at `270ca49:docs/V1-PROFILE.md:1023–1030` supports using new production keys.

**Owner prechecks on the revised amendment**

| Check | Result | Evidence |
|---|---|---|
| Capture row | **PASS** | A11:37–39 makes a bounded implementation-evidence claim; A11:121–130 specifies custody controls without promising attacker-key rejection or capture visibility. Consistent with [V1-CONTRACT.md:37](/home/tony/projects/tessera/docs/V1-CONTRACT.md:37) and :72. |
| Trigger clause | **PASS** | A11:112–120 explicitly says historical qualification does not qualify the replacement. A11:141–142 uses the explicit author CUT, not an unoccurred schedule-slip trigger. |
| Requester | **PASS** | A11:122–129 covers the enqueue path, prohibited direct/admin capabilities, every signature-causing principal, and alternative signing paths. |
| Binding text | **PASS** | A11:135 expressly identifies S1 as unregistered. A11:112 labels the custody exception as a proposed author ruling; the amendment does not invoke the withdrawn ruling budget. |

**D. Signature readiness**

The unresolved author ruling in §A11.5 item 2 is **not itself a review defect**. The revision now presents the retrospective exception and its consequences clearly enough for an author decision. Signing the final amendment should explicitly record whether that proposal is adopted; reviewer closure cannot supply that decision.

Before signature, repair A11C-01 and account for the registered K-R role/computation change. Neither passing hashes nor the proposed slot-2 ruling resolves those issues.

**Verdict: NOT READY FOR SIGNATURE — repair the deployed-code evidence binding and reconcile K-R’s registered issuer-role commitment.**

