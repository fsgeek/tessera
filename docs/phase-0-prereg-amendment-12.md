# Tessera — Phase 0 Pre-Registration, Amendment 12 — V1 implementation: bounded termination; successor windows (DRAFT, 2026-11-17)

> **Status: DRAFT by the steward (Claude Opus 5.5). Not signed. Sections 1 and 2 are drafted; 3–5 are placeholders.**
> The author's first commit containing the final text is its signing act (the A11 convention). Layered on the
> original and Amendments 1–11, none of which is edited. Every registered sentence this amendment changes is quoted
> with its locator.

## A12.1 Bounded termination

**Registered text changed.**
- A2.3 (`phase-0-prereg-amendment-2.md:288-289`): "termination is a contract obligation on the implementation, not a
  proven liveness property."
- A2.1 (`phase-0-prereg-amendment-2.md:135-138`): "An attempt whose lag exceeds S may be refused; a chain-valid
  artifact of such an attempt remains cryptographically valid and evidentially admissible but carries no protocol
  standing."

**Why.** The issuer ends an attempt only on complete negative evidence (lifecycle decision rev 5.3.1). A dependency
that fails for good (calendars that never answer, explorers that never agree) leaves a request open indefinitely:
the obligation of A2.3 is unmet for that case, and an open request is a resource an attacker can hold (the author,
2026-10-30: "Why wouldn't you just define a failure after some finite period of time (the FLP work-around)?
Otherwise, I'd worry that you've created a denial-of-service attack vector.").

**Registered change.**
1. **Bound.** Every request reaches a terminal state no later than **acceptance + 14 days** of service wall-clock
   time (L_term). 14 days = the nominal budget N × (δ + S) = 12 days (A2.3) plus 2 days of operating allowance.
2. **Outcome.** A request not COMPLETE at L_term ends `REFUSED / EVIDENCE_UNAVAILABLE`. Every open attempt ends with
   it; no attempt is allocated after it.
3. **Standing.** An attempt ended this way is an attempt whose lag exceeded S under A2.1: any artifact of it carries
   no protocol standing, even if evidence later shows it was timely. A2.1's permission ("may be refused") becomes,
   at L_term, an obligation.
4. **What it costs, stated.** A request that would eventually have qualified can be refused. That is a liveness
   loss, never a safety loss: a refusal never yields a receipt, so no false receipt can result. Clients resubmit.
5. **What it does not change.** Safety properties, the latch rule, the expiry-on-complete-negative rule before
   L_term, the window's signing stop, and the verifier.
6. **Implementation duty.** The `EVIDENCE_UNAVAILABLE` ending, gated in code since 2026-10-30 pending this decision,
   is enabled with L_term; its TLA+ model (`formal/tla/issuer-lifecycle/`) gains the bound and checks that every
   request terminates by L_term under the failure model.

## A12.2 Successor windows (sequential replacement)

**Registered text changed.** A9 (`phase-0-prereg-amendment-9.md:409-417`): "This amendment registers the first
issuance window only; it does not yet authorize successor issuance. … Without that registration, issuance stops at
the first window's end."

**Registered change.** Successor issuance is authorized by **sequential replacement**, as A9 sketched it, keeping
the frozen V1 byte and check profile:
1. **Same DNS owner and git path** (`_tessera-v1.wamason.com`; `tessera-v1/key-assertion`).
2. **New service keys for each window** (a new KMS ML-DSA-65 key and a new slot-2 HSM key). The repository root
   signs the new key-assertion commit.
3. **Strictly sequential windows:** `next.not-before > previous.not-after` (both endpoints inclusive); each window at
   most 90 days.
4. **One record at a time.** The DNS owner holds exactly one TXT record (multiple records fail `DNS_RRSET`). The
   successor record replaces the previous one only after the previous window's signing stop. Receipts carry their
   own historical snapshot and commit, so replacement does not affect them.
5. **Pre-commitment per window.** The successor's commit is OTS-stamped and reaches k = 6 confirmations before its
   first issuance (A9 C4), and its window opens no earlier than that.
6. **Before the first successor issuance,** the steward records the dated rotation registration A9 requires: the
   two-window positive and negative vectors (a receipt from each window verifies; a receipt whose T falls in the gap,
   or under the wrong window's keys, does not), and a model with its checked property ("no receipt is issued under a
   window's keys outside that window") and result.

**Consequence for V1's first window.** Issuance can continue past 2027-02-01 without a gap of more than the
pre-commitment time, provided the successor is prepared about two weeks before the first window's acceptance stop
(~2027-01-23): new service keys, a root signing session, the DNS replacement after 2027-01-28.

## A12.3 The canary's open findings (placeholder)
Levadura's beyond-window report on the 13 findings needing an amendment beyond A11 (obs-0185), when it arrives.

## A12.4 Operational posture (placeholder)
The V1 contract's limits gain: one operational machine today holds the administration of both signers (the AWS
management account login and the GCP project owner); the gate before reliance (DEPLOY.md) and its status.

## A12.5 Root rotation (placeholder)
Cryptoperiod (at most two years), triggers, procedure (a commit by the outgoing root naming its successor; a release
adding the new entry and closing the old interval), and how relying parties learn of it.
