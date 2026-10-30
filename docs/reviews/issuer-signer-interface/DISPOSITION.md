# Disposition: issuer <-> signer interface review (owner, 2026-10-30)

Codex report: `CODEX-REVIEW.md`. Brief: `BRIEF.md`. The fix as reviewed: `FIX.diff`.

| Finding | Disposition |
|---|---|
| Fix (frame name = `sha256(frame)`) | **Confirmed** by Codex: no loss of attempt isolation, cleanup, sealing, retry or IAM behaviour. Kept. |
| Interface sweep (B) | No other issuer/signer mismatch found across request, response, queue-metadata and grant boundaries. |
| ISI-01 (Low): GCP coverage substituted the frame producer | **Fixed.** `service/signer-gcp/tests/test_pipeline_roundtrip.py` runs both production signer classes behind the issuer's real pipeline, inline and 1 MiB, to COMPLETE and VALID_STRICT, plus the redelivery-count check. Control: with only the issuer fix reverted, the 1 MiB case ends `REFUSED ATTEMPTS_EXHAUSTED`. |
| ISI-02 part 1: K-R enforcement "in unsigned Amendment 11" | **Reviewer error, caused by our record.** A11 was signed at `f01e086`; the signing commit is its signing act (A11 preamble), and §A11.5 item 5 amends the K-R enforcement to the signer role. The file's header still says "DRAFT … Not signed" because signed text is not edited. The README status row now says so, so the next reader is not misled. |
| ISI-02 part 2: indefinitely open attempts vs A2.3 | **Known and open**: the author's termination decision (handoff 2026-10-30). Owner proposal: a fixed wall-clock bound ending in an explicit refusal, in one V1 implementation amendment. |
| Precheck 4 FAIL | Same two items as ISI-02; the first is resolved as above, the second is the open decision. |

Suites after disposition: issuer 235, signer-kms 48, signer-gcp 121, verifier 135 (77 subtests), all passing.
