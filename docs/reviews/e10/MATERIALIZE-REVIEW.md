**MZ-01 — MEDIUM — TMP-11 changes trust as well as withholding headers.**  
[materialize.py:357](/home/tony/projects/tessera/formal/e10/materialize.py:357) follows the vector’s TEST recipe, but that recipe exceeds its stated `remove_headers` mutation: trust pins 900025–900029 also disappear, changing the authenticated release. Restoring only the headers produces `UNVERIFIABLE / HEADERS_NOT_COVERED`; restoring headers and original trust produces `VALID_STRICT / OK`.

**Fix:** remove the six headers from an already-issued honest fixture, preserving its trust, release and other members. Reconcile the vector recipe and add a header-restoration control.

**MZ-02 — MEDIUM — `--check` does not inspect existing fixture bytes.**  
[materialize.py:553](/home/tony/projects/tessera/formal/e10/materialize.py:553) compares the rebuilt manifest with the saved manifest. In a `/tmp` copy, I changed one bundle, deleted another and added an unexpected file; `--check` still exited 0 with no differences.

**Fix:** enumerate and hash existing outputs, validate them against the saved manifest, then compare with the fresh build. Detect changed, missing and unexpected files, retaining the explicit run-record exclusion.

Validation at commit `1472cec22d5cf18dee96fed5a92daa0f3a7cfed7`:

- No other unintended mutation identified after reviewing every builder and inspecting SERVICE row diagnostics.
- All 68 `expected.json` reports match their vector’s six stable fields and `utc_assessment`; detail metadata also matches.
- Rebuilt under `/tmp`: **281/281 generated files byte-identical**, including `MANIFEST.json`. `RUN-INDEP.json` is a separate saved execution record.
- All six TEST issuer oracles match: isolated c2 refusal, c3 refusal and missing-confirmation refusal, each with a shipping control.
- SERVICE ran through the conformance runner using the requested executable and explicit `--mode test`.

The [complete per-fixture report](/tmp/tessera-mz-review-ohrm59/review-results.json) contains each fixture’s expected and observed six fields, UTC assessment and individual agreement flags.

No repository files edited. AWS execution and P9 environment sequences remain untested.

**VERDICT: ACCEPTABLE AFTER MZ-01 and MZ-02.**  
**service verifier: 68/68 agree**


