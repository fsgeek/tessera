# V1 clarifications after the freeze

> The V1 profile is frozen inside the signed spec object (`formal/freeze-v1/FREEZE-RECORD.md`, opening commit
> `52ee179`). Frozen text is not edited. This log records owner readings of frozen text that Phase 1a needs, each
> dated, sourced and labelled. A reading may narrow or clarify; it never widens a claim. The next spec version
> absorbs the readings, or rejects them. Where a reading and the frozen text truly conflict, the frozen text governs
> and the conflict goes to the author.

## CL-01 — §15.9 "reproduces … exit status" means zero versus non-zero (2026-10-26, OWNER, CLARIFY)

The acceptance rule turns only on success (exit 0) versus failure. A distribution `gpgv` conforms if, on every
release-format vector (`service/release-vectors/`), it returns zero exactly where upstream GnuPG 2.4.4 does. Exact
non-zero codes are recorded but do not decide conformance. Evidence: both builds agree on all nine vectors, exact
codes included (`service/release-vectors/RESULTS.txt`).

## CL-02 — `gpgv` exit 0 is necessary, not sufficient (2026-10-26, OWNER, CLARIFY)

§15.9 R3/R5: acceptance also needs the signing key's primary identity to be the R5-authenticated production key. A
TEST key in the keyring makes `gpgv` exit 0 (vector 09), and the release is still refused. A valid TEST signature is
accepted only on the explicit TEST provisioning path of R4(a) (vector 02), never in production mode.
