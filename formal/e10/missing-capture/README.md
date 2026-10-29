# A9.4 missing-capture negative control (C7 evidence)

Registered text (`docs/phase-0-prereg-amendment-9.md:281-283`, A9.4, "Contract for later verifiers"):

> Missing status capture does not by itself invalidate a V1 receipt. [...] **This is not non-repudiation.**
> Evidence (C7): for an otherwise valid, fully performable bundle where missing status capture is the sole
> difference, a companion returning `INVALID` or `UNVERIFIABLE` must go red.

Also A9:146 (C7: "Assigned build evidence includes A9.4's missing-capture negative control") and
`docs/V1-PROFILE.md:1248` ("C7 evidence, not a mapping row"), `:1257` (run after exit, 20 Nov).

## Reading

- V1 has no status-capture member. The bundle schema is `{profile, layers[1]}` and "P6 status capture ... DNSSEC
  status capture" is assigned to long-term validation, T4 (A9:236). Every V1 bundle therefore lacks status capture;
  revocation is `NOT_EVALUATED` in every report (A9:255-258, row 7 at A9:471).
- So "missing capture is the sole difference" cannot be built as a with/without-capture pair inside V1: there is
  no V1 bundle that has capture. The control is read as: *an honest, fully performable V1 bundle, which by
  definition has no status capture, must get `VALID_STRICT` (revocation `NOT_EVALUATED`), and a verifier that
  turns that absence into `INVALID` or `UNVERIFIABLE` is wrong and the harness must detect it.* It tests the
  "never a weaker verdict because of missing status capture" clause that binds later verifiers.
- I did not invent a capture member or a V1 field. The companion's list of capture-member names
  (`companion.CAPTURE_MEMBERS`) is the companion's own guess so that "has capture" is well defined; no V1 text
  defines it.

## Contents

- `companion.py`: `real_verifier` (the service verifier CLI in TEST mode, with the fixture's own `release.json`
  and `trust.json` and the universe release key as data) and two broken companions, `companion_invalid` and
  `companion_unverifiable`. Each is the real verifier plus one change: a `VALID_STRICT` on a bundle without
  status capture becomes `INVALID` / `UNVERIFIABLE` with reason `STATUS_CAPTURE_MISSING`. All else passes through.
- `test_missing_capture.py`: six tests. Fixture is `formal/e10/fixtures/E10-POS-01` (honest receipt as shipped),
  read in place, not copied, so it cannot drift from `materialize.py --check`.
- Run: `service/verifier/.venv/bin/python -m pytest formal/e10/missing-capture` (from the repo root, or
  `cd service/verifier` and use `../../formal/e10/missing-capture`).

## What goes red, and why

- Real verifier on E10-POS-01: `VALID_STRICT / OK`, `revocation` and `historical_security` `NOT_EVALUATED`, equal to
  the fixture's `expected.json` on the six stable fields. Not red.
- `companion_invalid` returns `INVALID`; `companion_unverifiable` returns `UNVERIFIABLE`. The test's detector
  (`harness_goes_red`) flags both: "red" means the harness saw a failing verdict on a bundle whose only
  "defect" is absent status capture.
- Two detector controls: a companion that changes nothing is not flagged; and on a bundle that is genuinely
  `UNVERIFIABLE / MEMBER_MISSING:git` (git member removed, re-encoded as JCS) both companions equal the real
  verifier, showing they alter only missing-capture behaviour.

## What this control does NOT show

- Not that the verifier handles status capture when present: V1 defines none and the verifier has no code for it.
- Not that a future verifier (T4) will satisfy the contract; it exercises only the V1 verifier and hand-built
  companions. It is not a model-checked companion and no TLA+/ProverIF companion is involved.
- Not that revocation, key theft or historical security are evaluated (they are `NOT_EVALUATED`), and not
  non-repudiation (A9:281-282).
- The companions are written by the same hand as the detector; the red is the harness detecting a wrong verdict
  that the companion was built to give, not an independent finding. It covers one honest bundle (E10-POS-01),
  not every valid bundle.
- It does not use the frozen catalog or production mode: TEST mode with the conformance universe's catalog and
  key (profile 15.9), so no claim about the production installation.
