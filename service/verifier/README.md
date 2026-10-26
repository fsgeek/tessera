# tessera-verify: the V1 service verifier

The service verifier for the `tessera-v1-strict` profile (Phase 1a, `formal/freeze-v1/FREEZE-RECORD.md`). Given a
trust configuration and a bundle it prints one canonical JSON object: the six stable fields under `stable`, and the
section 7.4 `utc_assessment` beside them. It is ported by copying source from the instrument
(`prototype/indep-verifier/`), as the owner's reading of A9.2 allows, and then adapted. It imports nothing from
`prototype/` or `formal/spike*/`, at run time or build time (`tests/test_independence.py` checks this).

**Its evidence is its own.** Nothing from the instrument's test results or conformance results counts for this
code. The tests, the conformance run and any later E10 or P9 evidence are for these bytes.

## Install and run

Needs `uv` or `python3.14` (Unicode 16.0.0 tables), `cc` and `make`.

```sh
bash install.sh                      # .venv, pinned cryptography, SHA-1DC built from vendor/, install.json
.venv/bin/tessera-verify --help
.venv/bin/python -m pytest tests     # unit tests, independence check, all 352 conformance cases
```

`vendor/sha1collisiondetection/` is the pinned upstream source (commit `a06f1adb...`, `vendor/SHA1DC-PIN.md`);
`install.sh` re-checks the six source digests before building it.

`install.json` is the per-installation record (profile 15.9 R2): interpreter and Unicode facts and the SHA-1DC binary
path and hash, written on the installing machine, unsigned, outside any signed archive, git-ignored. The verifier
checks it at start and `--diagnostics` reports its SHA-256 on stderr.

```sh
tessera-verify --trust TRUST --bundle BUNDLE [--catalog CATALOG] [--request strict]   # production (default)
tessera-verify --mode test --test-release R --test-release-key K --trust TRUST --bundle BUNDLE
tessera-verify --previous PRIOR_TRUST --next NEXT_TRUST                               # prints ACCEPT or REJECT
```

- **Production is the default (15.9).** It uses only the bindings in `tessera_verify/release_constants.py`
  (`NAMESPACE = "PRODUCTION"`, trust hash, catalog bytes) and refuses any TEST flag or `TESSERA_V1_TEST_*` variable
  with `TEST_AUTHORITY_REFUSED`.
- **TEST only by `--mode test`**, with a `tessera-v1-test-release/1` record and key. It provisions the bindings in
  memory for one process and never edits `release_constants.py`. An installation compiled as PRODUCTION refuses it.
  This record is the section 3.5 harness interface, not a release.
- The catalog is the frozen flat object (`catalog.json`). **Delta (`utc_delta_s`) and m (`utc_m`) are read from it**
  and nothing compiles them in; a missing or malformed value, or m different from k = 6, is
  `CATALOG_UNAUTHENTICATED`. The assumption id is derived from them (`A-UTC-7200-6` for the frozen catalog).
- Startup refusals exit 2 with the code on stderr and no verdict on stdout. INVALID and UNVERIFIABLE are exit 0.
- The service-key listing is not in V1 (author ruling, E9 row 2) and is not implemented.

## Tests

`tests/` holds the ported unit tests (codec, parsers, boundaries, hybrid pair, UTC assessment, release
authentication) rewritten for this package, plus `test_cli.py`, `test_frozen_catalog.py` (reads
`formal/freeze-v1/objects/` as a fixture only), `test_independence.py` and `test_conformance.py`.
`tests/conformance_runner.py` reads each case in `prototype/conformance/cases/` as data (trust, release, bundle or
recipe, request, `expected.json`) and the universe release public key, runs the CLI in explicit TEST mode as a
subprocess, and compares with `expected.json`. It never imports instrument code. Run it alone with
`python tests/conformance_runner.py --jobs 6`.

## Not yet done

- **No production release key and no release signing.** Section 15.9 R3 (detached OpenPGP signature over the
  archive, `gpgv` acceptance, trusted acquisition-side checker), the key ceremony, bootstrap record and rehearsal
  come after the freeze. A source tree is unprovisioned, so production mode refuses with
  `TRUST_CONFIG_UNAUTHENTICATED` until a release generates `release_constants.py`.
- No release assembler: `RELEASE.json`, the `.parts` archive, the dependency lock part, and `install.sh` checks of
  R2's binding equalities. No production `trust.json`.
- SHA-1DC absent or non-functional is a startup refusal (R2, "else the existing startup refusals"): exit 2,
  `SHA1DC_UNAVAILABLE` on stderr, no verdict. The instrument's verdict-level SHA-1DC-unavailable code is removed.
- E10 evidence (vectors against AWS) and the P9 code inspection are not done.
