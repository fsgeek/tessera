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

## CL-03 — "bounded local refusal" (A9.2 after-exit list) (2026-10-27, OWNER, NARROW-CLAIM, contestable)

**Text.** A9.2 lists "bounded local refusal" for 20 Nov (`phase-0-prereg-amendment-9.md:214-215`) and defines it
nowhere. A9.7 row 12 (`:476`) replaces A3's refusal-record decomposition (`phase-0-prereg-amendment-3.md:572-581`: a
portable record, a public commitment, and delivery and publication states) with "Bounded local refusal returned
by the API", class **C**: a capability not offered by V1. A9.3 (`:238`) moves the portable form to the later
"Portable refusal records".

**Reading.** In V1 a refusal is *local*: it is returned by the API to the requesting credential and kept as
operator state. It is not a signed or portable record, and it carries no commitment and no publication. It is
*bounded* in three ways:

1. **Closed reasons.** Refusals are typed from a fixed set: REFUSED with `TOO_LARGE`, `OUTSIDE_WINDOW`, `CLOSING`,
   `SIGNING_UNAVAILABLE` or `BAD_REQUEST`, and FAILED with a stated reason. Nothing else is said about a refused
   request.
2. **Bounded in time.** Every accepted request ends COMPLETE or FAILED within 24 hours of acceptance (S4), within
   the stated service clock tolerance (`docs/decisions/2026-10-27-service-clock-tolerance.md`).
3. **Bounded in scope.** By A9's issuer invariant, a refusal never concerns a shipped receipt
   (`phase-0-prereg-amendment-9.md:165`).

**Evidence.** The issuer's state and refusal tests (`service/issuer/tests/`) show it locally. The E10 issuing
vectors show it again when they run against the deployed API. A refusal claims nothing to anyone but the requester,
and the contract says so (`docs/V1-CONTRACT.md` §3).

**Why it is a reading.** "Bounded" has three plausible senses, and this takes all three, which is the narrowest
claim. If the author meant something else, the frozen text governs and the question goes to him.
