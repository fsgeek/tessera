The profile is useful evidence, but **not yet sufficient for discharge**. Its main implementation claims hold in the reviewed code; several claims lack tests that distinguish the verifier’s checks from library behavior, and significant rule-O policy behavior is omitted.

I made no repository edits or git writes. Scratch evidence is under [/tmp/tessera-p3-review.ubxLqB](/tmp/tessera-p3-review.ubxLqB).

The requested command passed: **149 tests**. The same suite also passed against regenerated vectors and the Lambda-target cryptography wheel.

| Scratch mutation | Result |
|---|---|
| Remove coordinate range checks | 2 failures: K-04, K-16 |
| Remove key-prefix checks, retain lengths | 5 failures: K-07, K-08, K-10, K-26, K-27 |
| Remove `sig_policy` | 4 failures: O-18..O-20, B05 |
| Remove ML-DSA encoding gate from verification | 7 permissive-backend test failures |
| Remove creation-time policy | **149 pass** |
| Remove issuer-ID/fingerprint structural policy | **149 pass** |
| Remove expiration/unknown-critical policy | **149 pass** |
| Remove Y-coordinate range check | **149 pass** |
| Remove verifier-side curve-equation check | **149 pass** |

Detailed outputs are in [mutation logs](/tmp/tessera-p3-review.ubxLqB/range.log), with sibling logs named for each mutation.

1. **P3R-01 — Medium: rule-O’s accepted-signature profile omits substantial policy.**  
   **Location:** [PROFILE.md:74](/home/tony/projects/tessera/formal/p3-verification-profile/PROFILE.md:74), [test_p3_profile.py:114](/home/tony/projects/tessera/formal/p3-verification-profile/test_p3_profile.py:114).

   **Scenario:** Removing creation-time validation, issuer-metadata structural validation, or the expiration/unknown-critical restriction leaves all 149 tests green. These checks define which otherwise well-formed signatures V1 accepts, under [V1-PROFILE.md:1087](/home/tony/projects/tessera/docs/V1-PROFILE.md:1087). The implementation currently enforces them; this is an evidence gap, not an observed acceptance bug.

   **Fix:** Describe these policies and add correctly signed positive/negative vectors: missing/duplicate/wrong-length creation time; expiration; unknown critical versus noncritical types; malformed/duplicate/inconsistent types 16/33; recognized critical types; and ignored, structurally valid unhashed metadata. Use signatures that would verify if the policy were removed.

2. **P3R-02 — Medium: the tests do not establish that all public-key checks occur before the library.**  
   **Location:** [PROFILE.md:111](/home/tony/projects/tessera/formal/p3-verification-profile/PROFILE.md:111), [PROFILE.md:117](/home/tony/projects/tessera/formal/p3-verification-profile/PROFILE.md:117), [DIVERGENCES.md:10](/home/tony/projects/tessera/formal/p3-verification-profile/DIVERGENCES.md:10).

   **Scenario:** The source does perform coordinate-range and curve-equation validation. However, removing its on-curve check leaves the suite green because the library rejects the existing malformed points. Removing only `Y < p` also survives. Thus “checked by the verifier rather than by library default” is supported by inspection, but not fully by mutation-sensitive tests.

   **Fix:** Add permissive-backend tests, following `TestMLDSAGate`, that assert invalid points are rejected before the EC constructor is called. Exercise X range, Y range, curve membership, and point representation separately. Preserve positive controls that reach the constructor.

3. **P3R-03 — Medium: the disclosed ECDSA equation gap is readily testable.**  
   **Location:** [PROFILE.md:158](/home/tony/projects/tessera/formal/p3-verification-profile/PROFILE.md:158).

   **Scenario:** The quoted probability concerns ordinary signing; it does not prevent constructing a verification vector. I selected an on-curve point with `x(R) = n + 3`, set `r = 3`, `s = 1`, and derived the corresponding public key. The actual service function accepts it. A constructed companion yielding verification point infinity is rejected.

   The existing infinity vectors concern **public-key input**, not infinity arising during the verification equation.

   **Fix:** Record both constructed cases as fixed vectors. They distinguish `x(R) mod n` from an incorrect unreduced comparison and cover equation-result infinity. The construction is in [probe.py](/tmp/tessera-p3-review.ubxLqB/probe.py).

4. **P3R-04 — Medium: F1 records the development environment without connecting it to deployment evidence.**  
   **Location:** [PROFILE.md:60](/home/tony/projects/tessera/formal/p3-verification-profile/PROFILE.md:60), [package.py:25](/home/tony/projects/tessera/service/issuer/package.py:25), [package.py:83](/home/tony/projects/tessera/service/issuer/package.py:83).

   **Scenario:** A version/backend tripwire sensibly detects drift in the environment running the tests. It does not itself characterize another installation. `package.py` independently resolves a platform-specific wheel; its install-record fields do not record cryptography or OpenSSL.

   **Current verification:** I reproduced that wheel selection. Both installations report `cryptography 50.0.2` and `OpenSSL 4.0.3 29 Sep 2026`; both use `cp311-abi3-manylinux_2_34_x86_64`. Their `_rust.abi3.so` files have identical SHA-256:
   `1e5d23fa66915204b9b67202a46993844d81cda56f6ad52cead2def37617ee29`.
   All 149 tests pass using the downloaded wheel. **No venv-versus-selected-wheel OpenSSL gap was found.** This was not a deployed Lambda invocation.

   **Fix:** Record tested wheel identity/digest, platform, backend and results, and connect the deployed artifact to that record. Keep separate records for genuinely different supported builds. Cryptography’s wheels bundle OpenSSL, so Lambda’s system OpenSSL alone is not the relevant identity. [Official installation documentation](https://cryptography.io/en/latest/installation/#static-wheels).

5. **P3R-05 — Low: O-02’s “high-S twin” label is reversed.**  
   **Location:** [PROFILE.md:77](/home/tony/projects/tessera/formal/p3-verification-profile/PROFILE.md:77), [gen_vectors.py:129](/home/tony/projects/tessera/formal/p3-verification-profile/gen_vectors.py:129).

   **Scenario:** Recorded O-01 is high-S; O-02 is low-S. Together they correctly demonstrate acceptance of both, so the policy conclusion holds.

   **Fix:** Normalize the generated baseline to low-S before creating its high-S twin, or label them simply as complementary twins and assert that one is above `n/2`.

6. **P3R-06 — Low: the claimed pipeline order differs from bundle execution.**  
   **Location:** [PROFILE.md:27](/home/tony/projects/tessera/formal/p3-verification-profile/PROFILE.md:27), [test_p3_profile.py:51](/home/tony/projects/tessera/formal/p3-verification-profile/test_p3_profile.py:51).

   **Scenario:** The helper runs signature parsing → signature policy → key parsing → verification. Bundle processing validates keys at row 5.1 before signature policy at row 9.1. Consequently, isolated vectors do not establish combined-failure precedence, despite the “row order” wording.

   **Fix:** Describe this as a function-level harness and reserve precedence claims for bundle tests. Add combined-failure cases if claiming that coverage.

The translation table is a **reasonable, explicitly contestable owner reading**, not a concealed amendment. P-256’s cofactor-one explanation is sound: finite valid points have prime order, and public-key infinity is excluded by the accepted representation. For ML-DSA, point torsion and elliptic-curve cofactor equations genuinely do not apply. Exact decoding and the pure/HashML-DSA/context interface are appropriate replacement concerns. Acceptance of an all-zero encoded key establishes decoding behavior, not a security guarantee about that key; the profile acknowledges this boundary.

High-S/low-S acceptance, bare DER versus raw signatures, nonminimal MPI encoding, ML-DSA contexts, external-μ interoperability, ML-DSA adjacent key lengths, and public-key infinity **already have coverage**. The important omissions are those identified above. The translation’s sufficiency still requires the author’s recorded ruling, as §4 itself says.

The vectors do exercise the service’s actual functions: `parse_signature`, `sig_policy`, `public_key`, `signature_verifies`, `verify_bundle`, and `parse_trust`. They are not merely cryptography tests. Direct-library characterization is clearly separated in `TestLibraryBehaviour`; input construction also uses cryptography appropriately. The permissive-backend ML-DSA tests are particularly effective: removing the service gate fails them even though OpenSSL independently rejects the malformed signatures.

Owner prechecks:

| Check | PROFILE.md | DIVERGENCES.md |
|---|---|---|
| **1. Capture row** | **PASS**, [line 141](/home/tony/projects/tessera/formal/p3-verification-profile/PROFILE.md:141): rejection concerns substitution into existing honest signed material; it does not claim fresh attacker-key receipts fail after dual capture. | **PASS**, [lines 7–12](/home/tony/projects/tessera/formal/p3-verification-profile/DIVERGENCES.md:7): bounded codec/validation claims; no capture-detection claim. |
| **2. Trigger clause** | **PASS**, [lines 3–9](/home/tony/projects/tessera/formal/p3-verification-profile/PROFILE.md:3): evidence is drafted, not discharged. The 20 November obligation is registered in A9’s “After exit” provision. | **PASS**, [lines 22–24](/home/tony/projects/tessera/formal/p3-verification-profile/DIVERGENCES.md:22): withdrawn release format and installed-verifier restriction match R3/R4, including the source-checkout instrument exception. |
| **3. Requester** | **PASS**, [lines 35–47](/home/tony/projects/tessera/formal/p3-verification-profile/PROFILE.md:35): verification behavior is described without deriving signer independence from key storage. | **PASS**, [lines 16–24](/home/tony/projects/tessera/formal/p3-verification-profile/DIVERGENCES.md:16): caller-supplied matching key is explicit; no storage-based authorization inference. |
| **4. Binding text** | **PASS**, [lines 6–9 and 129–132](/home/tony/projects/tessera/formal/p3-verification-profile/PROFILE.md:129): registered obligation is distinguished from owner interpretation. | **PASS**, [lines 7 and 22–23](/home/tony/projects/tessera/formal/p3-verification-profile/DIVERGENCES.md:7): cited requirements trace to V1 profile/frozen encoding rules; no ruling-budget requirement is imported. |

**Verdict: No—retain P3 as checked until the coverage gaps and deployment evidence are addressed and the author records acceptance of the translation.**

