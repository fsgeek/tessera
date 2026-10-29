**Verdict: A11C-01 is closed for the bounded package-identity claim; Amendment 11 is ready for the author’s rulings and signature. P3 discharge remains pending deployment evidence.**

1. **A11C4-01 — CONFIRMED: amendment wording.** [§A11.2 item 3(c)](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:69) implements A11C3B-05/06’s evidence chain: recorded packager output → tested verifier bytes and F1 binding → exact archive digest → AWS-reported digest for every covered function. It expressly disclaims extractor agreement. It establishes neither post-extraction identity nor runtime module loading. Omitting “version” fits the current deployment’s unpublished functions; the record must identify the functions actually compared.

2. **A11C4-02 — CONFIRMED: digest comparison and negative controls.** [The helper](/home/tony/projects/tessera/formal/p3-verification-profile/test_p3_profile.py:579) correctly computes `base64(SHA256(zip_bytes).digest())`, consistent with AWS’s package-hash field and [documented response examples](https://awscli.amazonaws.com/v2/documentation/api/2.22.8/reference/lambda/update-function-code.html).

   I built the real package with the requested issuer command. Its SHA-256 was `1bfcc569b284a570023cfcf595231525e821e23dd1e2660f5524c2b4dbab6446`; base64 was `G/zFabKEpXACPPz1lSMVJegh4j3R4mYPVSTCtNurZEY=`.

   | Supplied digests | Actual deployment-identity test |
   |---|---|
   | Both match | PASS |
   | API differs | FAIL |
   | Poller differs | FAIL |
   | Hexadecimal digest | FAIL |

   This build is bootstrap evidence, with no Lambda installation record; these controls establish comparison behavior, not actual deployment.

3. **A11C4-03 — CONFIRMED: deployment coverage.** [DEPLOY step 10](/home/tony/projects/tessera/service/issuer/DEPLOY.md:70) covers API and poller. [Terraform](/home/tony/projects/tessera/service/issuer/infra/main.tf:330) deploys the same ZIP to both.

   **The separate signer packages are not needed for this P3 verification-profile discharge.** Although both signers perform self-checks, the issuer independently [verifies returned signatures](/home/tony/projects/tessera/service/issuer/tessera_issue/signers.py:37) and runs bundle verification before shipping. This discharge does not certify deployed signer policy, signing correctness, or requester controls; those retain their separate obligations.

4. **A11C4-04 — Low, nonblocking limitation: coverage is supplied by the operator.** [The test](/home/tony/projects/tessera/formal/p3-verification-profile/test_p3_profile.py:180) checks every **supplied** digest but cannot establish that every required function was supplied. Both a single matching digest and `matching_digest,` pass. Step 10 and the amendment’s named-function record supply that completeness check. The owner’s mismatch claim is confirmed; a passing test alone is insufficient evidence of complete coverage.

5. **A11C4-05 — CONFIRMED: manifest and suite.** All 15 manifest entries verify. The manifest SHA-256 is `844cb7ff8df59f047d2ea48536ddb30bad5b3e93684acbce6a4dad1241aee42d`, matching [the amendment](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:58). The requested full suite yielded **1201 passed, 1 skipped, 2 warnings**. Deployment identity skipped because deployment variables were unset. The warnings are the previously recorded collected helper returning a dictionary and intentional duplicate ZIP entry. No new blocking defect found.

Owner prechecks applied specifically to §A11.2 item 3(c):

| Check | Result | File:line and reason |
|---|---|---|
| Capture row | **PASS** | Amendment [69](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:69): artifact identity makes no attacker-key rejection or capture-visibility claim; consistent with V1-CONTRACT:37,72. |
| Trigger clause | **PASS** | Amendment [71](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:71): comparison is explicitly after deployment; no deployment or discharge is asserted here. |
| Requester | **PASS** | Amendment [74](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:74): package identity derives no signing-security claim from key storage and makes no requester authorization claim. |
| Binding text | **PASS** | Amendment [3](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:3), [69](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:69): proposed requirements remain explicitly unsigned; the reviewer recommendation is not presented as existing registered authority. |

Repository and git remained read-only. [Controls and results](/tmp/tessera-a11c4.oybANU5V/controls.json) and [full suite output](/tmp/tessera-a11c4.oybANU5V/floor.log) are in the fresh scratch directory. No AWS calls were made.