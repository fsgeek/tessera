# Throwaway prototype — NOT service code

Started 2026-10-06 at the author's suggestion. This directory holds a disposable prototype built from
`docs/implementation-spec.md` *as is*. Per the author's 2026-08-29 clarification, Band 0's "before any code"
covers code intended for the service; this is not that, and nothing here may be copied into the service.
It may be deleted at any time.

**Purpose.** Find where the model or the spec is wrong before the real system is built:
1. Every place a builder has to guess, because the spec or the model abstracts something away (`GUESSES.md`).
2. Whether the symbolic attack traces (`formal/suite/capstone/proverif/dev/slice_probe/out/`) are rejected by
   a verifier built straight from spec §5.
3. Whether consumers (a submitter, a relying party, a 2106 examiner with no service alive) can use what
   comes out.

**Lifetime.** Phase 1 (issuer + verifier + attack replay) is about two days of agent time. Phase 2
(consumers) only if phase 1 is informative. It is scored against `PREDICTIONS.md`, written before any code.

**Phase 2 (2026-10-06).** Consumers in `consumers/`, tests in `tests/test_phase2.py`, results in `PHASE2-REPORT.md`; run `uv run python run_phase2.py`.

**Phase 3 (2026-10-07).** Real mechanisms in `tessera_proto/real/` (RFC 8785 number domain, KMS-style ECDSA/RSA-PSS,
OpenPGP via /usr/bin/gpg in a throwaway GNUPGHOME, OpenTimestamps against archived mainnet headers, offline DNSSEC
and git-commit evidence). Tests in `tests/test_phase3.py`, results in `PHASE3-REPORT.md`; run `uv run python run_phase3.py`.
The stub path stays the default; `TESSERA_PROTO_MODE=real` (or `scenarios.build("real")`) selects the de-stubbed one.
