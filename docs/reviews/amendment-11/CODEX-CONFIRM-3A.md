Independent verification completed read-only; no repository edits or git writes. Scratch: `/tmp/tmp.bt6IqG2thi`.

1. **A11C3A-01 — CONFIRMED: rejection cases.** Independently constructed packages containing each of these entries were rejected at `formal/p3-verification-profile/test_p3_profile.py:81`:

   - `./tessera_verify/codec.py` — the earlier review’s attack
   - `tessera_verify//codec.py`
   - `tessera_verify/../tessera_verify/codec.py`
   - `/tessera_verify/codec.py`
   - `tessera_verify\codec.py`
   - An exact duplicate `tessera_verify/codec.py`

   The symlink entry was rejected separately at `:83`.

2. **A11C3A-02 — CONFIRMED: positive controls.** The clean synthetic package passes. The genuine package built with `service/issuer/.venv/bin/python package.py /tmp/tmp.bt6IqG2thi/p.zip` also passes `check_zip`. Its SHA-256 is `1bfcc569b284a570023cfcf595231525e821e23dd1e2660f5524c2b4dbab6446`. This is a bootstrap package, not evidence of deployment.

3. **A11C3A-03 — CONFIRMED: current tests detect removal of the path assertion.** Used the requested scratch mirror and service symlink; removed only the assertion at `:81`. The A11C01 tests then yielded **3 failed, 5 passed**. All failures were `DID NOT RAISE AssertionError` in `test_A11C01_an_alias_or_duplicate_of_a_verifier_file_is_refused`, for:

   - `./tessera_verify/codec.py`
   - `/tessera_verify/codec.py`
   - `tessera_verify\codec.py`

   Restoring the original recorded binding digest in this mutant reproduced the vacuity mechanism: all six alias packages failed the wheel-digest assertion at `:85`. This independently reproduces the reported failure mechanism; it does not establish the chronology of the owner’s earlier runs.

4. **A11C3A-04 — CONFIRMED: division of checks.** Without the path assertion, `//` and `..` variants fail the file-set comparison at `:88`; the changed exact duplicate fails the content comparison at `:89`. The three aliases above are accepted. The symlink remains rejected by its separate assertion at `:83`.

The requested full suite completed: **1200 passed, 1 skipped, 2 warnings**. The skip is the deployed-package identity check because `TESSERA_LAMBDA_ZIP` was unset. Warnings concern the collected `tested_verifier_files` helper returning a dictionary and the intentionally duplicated ZIP entry.

The additional wording and manifest claims also check out: amendment `:93,150`, deployment script `:31–33`, and deployment guide `:28` contain the stated corrections. All 15 manifest entries verify; its digest matches disposition `:53`.

Owner prechecks applied specifically to `docs/reviews/amendment-11/DISPOSITION.md`’s “Second confirmation” section:

| Check | Result | File:line evidence |
|---|---|---|
| Capture row | **PASS** | Disposition `:35–56` makes bounded package-check claims, with no attacker-key rejection or capture-visibility promise; consistent with `docs/V1-CONTRACT.md:37,72–73`. |
| Trigger clause | **PASS** | Disposition `:35–50` ties the repair to the demonstrated alias attack and reproducible controls; no untriggered registered consequence is invoked. |
| Requester | **PASS** | Disposition `:51–52` reports wording/citation corrections, without deriving signing security from key storage. The cited supplement `:171–176` explicitly addresses who can invoke signing. |
| Binding text | **PASS** | Disposition `:39–56` reports implementation and verification results; it does not promote instance prose or the schedule’s ruling budget into a registered requirement. |

Are the owner’s claims confirmed: **YES, within the tested scope; historical vacuity was reproduced, and deployment identity remains unverified.**