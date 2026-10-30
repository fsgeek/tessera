# Service clock tolerance (2026-10-27)

> **Status: OWNER DECISION, CLARIFY**, by the owner instance (Claude Opus 5.5), 2026-10-27. It concerns the
> service-level times in the owner's resolutions (`docs/V1-SERVICE-RESOLUTIONS.md`, stamped at `2411714`): S4, S5,
> S6 and L1. It changes no receipt guarantee. No guarantee in `docs/V1-CONTRACT.md` depends on these times, and the
> verifier checks none of them. It follows three Codex confirmation rounds on the issuer (`docs/reviews/issuer/
> CODEX-CONFIRM.md`, `-2.md`, `-3.md`). The third swept the whole package and found that the remaining problem is a
> limit, not a bug (CF3-01).

## The limit

The issuer decides on its own clock, and every decision is now taken on a clock reading made after the records it
depends on (CF2-02, CF3-02, CF3-03). But the write that makes a decision visible can take effect later than that
reading, and no client-side check can bound when AWS commits a request already sent. AWS documents that a write
reported as failed may still have succeeded.

## What the issuer bounds

- **Its own time per AWS call.** Connection 5 s, response 20 s, 4 attempts in standard retry mode: about 3 minutes
  at most (`tessera_issue/lambda_app.py`, `AWS_CLIENT_CONFIG`; a test keeps it under a third of the lease).
- **Completion.** *(Superseded 2026-10-29: the 24-hour completion deadline is withdrawn; see
  `docs/decisions/2026-10-29-issuance-lifecycle.md`. COMPLETE now follows a latch, and the latch is not raced, so the
  CF2-01 lease margin no longer applies to completion. The earlier text read: "COMPLETE is confirmed only when at least the 15-minute writer lease remains before the 24-hour deadline (CF2-01). Inside the last lease a finished request stays ACCEPTED, and at the deadline it is FAILED.")*
- **Late writers.** Cleanup keeps deleting until 15 minutes after an end (CF-02).

## The stated tolerance

Each service-level transition (COMPLETE, an attempt's expiry or discard, REFUSED, the 30-day retention and deletion, the acceptance
stop, and the 5-minute receipt links) may become visible up to **15 minutes** after the time it records. This
assumes AWS commits or rejects every request within 15 minutes of its being sent.

For the acceptance stop this is harmless by design: acceptance stops 120 hours before the window ends, and signing
stops at 96 hours (L1), so a late admission has 24 hours of slack. Those 96 hours are the runbook's operating margin,
an owner control, and not a registered rule (L1 says so). For signing itself, the check that counts is the signer's
own `sign_by` and signing stop, enforced at the signer (IS-03, IS-09). That too is an owner operating control. Both
signers now enforce it (`service/signer-kms`, `service/signer-gcp`), and this tolerance does not touch it.
(Corrected 2026-10-27 after the signer review's binding-text precheck: this first called it "the binding check".)

## Why stop here

Each review round found one more site of the same shape. A protocol that did not depend on commit time would need
the store to time-stamp commits authoritatively. That is redesign for a 15-minute fuzz on service promises that no
receipt depends on. The author's yardstick: *"build something that works, with known limitations."* If AWS ever
violates the assumption, a symptom is a status change that appears up to minutes late. No receipt is affected.
