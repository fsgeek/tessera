# P3 verification-profile review: owner disposition (2026-10-27)

Owner instance (Claude Opus 5.5). The review is `CODEX-REVIEW.md` (P3R-01..06, verdict "retain P3 as checked") and
the subject is `formal/p3-verification-profile/`. All six findings were applied by the profile's author (an owner
sub-agent), so the profile tests now give 223 passed, 1 skipped. The skip waits on a deployed zip. The verifier suite
is unchanged at 135. All four owner prechecks passed. No defect in the verifier was found; every finding was a gap in
the evidence.

| ID | Sev | Disposition |
|---|---|---|
| P3R-01 | Med | 22 rule-O policy vectors (P-01..P-25). Each negative is correctly signed and verifies when `sig_policy` is skipped. |
| P3R-02 | Med | `TestPointBeforeConstructor` replaces the EC constructor with a stand-in that accepts anything. X range, Y range (new K-36, K-37), curve membership and representation are each rejected before it, and positive controls reach it. |
| P3R-03 | Med | E-10 (x(R) = n + 3, accepted: the reduction mod n) and E-11 (the equation's result is infinity, rejected) are fixed vectors. The "untestable" claim is withdrawn. |
| P3R-04 | Med | F1 records the wheel tag and the `_rust.abi3.so` digest. Tests check the venv and the zip `service/issuer/package.py` builds. The deployed-zip test runs with `TESSERA_LAMBDA_ZIP` at the deployment session. The suggested change to `package.py` (refuse a mismatch with F1) is not made: `test_lambda_package_wheel_identity` already checks the zip `package.py` builds, and coupling the build to a formal record adds nothing that test doesn't give (owner). |
| P3R-05 | Low | Signing is normalised to low-S. A test asserts that O-01 is low-S and O-02 high-S. |
| P3R-06 | Low | The helper is described as a function-level harness. Precedence is claimed only from bundle tests (new B08). |

**Mutation sensitivity.** All five mutations that survived the review now fail tests (PROFILE.md §6). The owner
reproduced (d), removing `y < P`, independently in a mirrored scratch tree: 4 failed, K-36 and K-37, matching the
table. A first attempt imported the real verifier and passed; the profile's test puts `service/verifier` first on
`sys.path`, so a mutation must be tested in a mirrored tree.

**Not moved.** P3 stays `checked`. Discharge needs (1) the author's ruling on the translation, PROFILE.md §4 (lines
198-216), which is a reading of Ed25519-era registered words; and (2) the deployed-zip identity test run at the
deployment session.
