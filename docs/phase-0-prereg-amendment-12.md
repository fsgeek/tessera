# Tessera — Phase 0 Pre-Registration, Amendment 12 — V1 implementation: bounded termination; successor windows (DRAFT r2, 2026-11-20)

> **Status: DRAFT r2 by the steward (Claude Opus 5.5, tenure from 2026-11-19). Not signed.** r1 (2026-11-17) was
> reviewed by Codex (`docs/reviews/amendment-12/CODEX-REVIEW.md`: five HIGH); r2 answers each finding (map at the
> end) and awaits Codex re-review. The two choices the disposition put to the author were resolved by him on
> 2026-11-19 ("As steward, I will abide by your recommendation"), as OWNER DECISIONS adopted by his signature.
> Sections 3–5 are placeholders.
> The author's first commit containing the final text is its signing act (the A11 convention). Layered on the
> original and Amendments 1–11, none of which is edited. Every registered sentence this amendment changes is quoted
> with its locator.

## A12.1 Bounded termination

**Registered text changed.**
- A2.1 (`phase-0-prereg-amendment-2.md:131-135`): "Timeliness is **latched at eligibility**: an attempt eligible
  within the envelope cannot be expired by later packaging or scheduling delay — eligible/finalizing, shipped, and
  expired/refused are mutually exclusive states".
- A2.1 (`:142-145`): "'every timely-eligible attempt ships' is a contract obligation on the implementation".
- A2.1 (`:156-157`): "so such an attempt latches eligible/finalizing and cannot expire."
- A2.3 (`:261-264`): "an attempt expires when wall time passes `declared + δ + S`, except that timely-latched
  eligibility excludes expiry — eligible/finalizing, shipped, and expired/refused are mutually exclusive states".
- A2.3 (`:288-289`): "termination is a contract obligation on the implementation, not a proven liveness property."

Not changed, and applied as written: A2.1's "may be refused" permission (`:135-138`) and A2.4's confinement of
standing (`:307-315`).

**Why.** The issuer ends an attempt only on complete negative evidence (lifecycle decision rev 5.3.1). A dependency
that fails for good (calendars that never answer, explorers that never agree, an object store that stays down)
leaves a request open indefinitely: the obligation of A2.3 is unmet for that case, and an open request is a
resource an attacker can hold (the author, 2026-10-30: "Why wouldn't you just define a failure after some finite
period of time (the FLP work-around)? Otherwise, I'd worry that you've created a denial-of-service attack
vector.").

**Registered change.**
1. **The bound.** Each request has a termination deadline **L_term = acceptance time + 14 days**, on the issuer's
   wall clock (the clock that records acceptance). 14 days is a **selected cap**, not a derived guarantee: it
   exceeds the nominal budget N × (δ + S) = 12 days (A2.3) by 2 days, but the time before, between and after
   attempts is not bounded by A2.3, so no request is promised its full nominal budget within the cap.
2. **The bound overrides the latch.** At L_term the latch protection above yields: a request not COMPLETE at L_term
   ends `REFUSED / EVIDENCE_UNAVAILABLE`, and every attempt it holds, **latched or not**, ends with it. "Every
   timely-eligible attempt ships" becomes "every timely-eligible attempt ships, if it can be shipped before
   L_term". The mutual exclusion of eligible/finalizing, shipped and expired/refused is unchanged at every instant;
   only the protection against ending a latched attempt is cut off at L_term.
3. **What the refusal says.** It says the bound was reached. It does **not** assert that any attempt's lag exceeded
   S, and the A2.1 trigger is not invoked. An artifact of such an attempt keeps its cryptographic validity and its
   evidential admissibility; because it was not shipped inside a receipt, it has no protocol standing, by A2.4 as
   written.
4. **The transition (durability and fencing).** These are the construction rules; they restate the deployed
   lifecycle's mechanism and add the deadline:
   - *Single writer.* Only the poller writes lifecycle state, one invocation at a time (reserved concurrency 1,
     `service/issuer/infra/main.tf:365`), and every write is a compare-and-set on the request's version and
     lifecycle guard (`tessera_issue/aws.py:88-104`). An invocation killed mid-turn is fenced: its pending writes
     carry an older version and fail (`pipeline.py:255-261`).
   - *Tie rule.* The COMPLETE commit is made only if the wall clock, read after the receipt object is stored and
     immediately before the commit, is **strictly before** L_term. At or after L_term the poller commits the
     refusal instead. Exactly one of COMPLETE and REFUSED is ever durable for a request (compare-and-set).
   - *Delivery fence.* A receipt is delivered only by the API, and only for a request whose durable state is
     COMPLETE (`api.py:167-184`). A receipt object stored by a turn whose COMPLETE commit did not land is never
     served, and the request's results are deleted by cleanup (`pipeline.py:322`). So no receipt is delivered for
     a refused request, whatever an in-flight worker had done.
   - *Availability assumption.* The refusal is durable at the first poll at or after L_term at which the poller runs
     and the request store accepts writes. The poller is scheduled every 10 minutes; under that assumption a
     request is terminal by **L_term + 10 minutes**. If the store or the poller is unavailable from L_term onward,
     no terminal state can be recorded until it returns; meanwhile no receipt can be delivered either, because
     delivery requires the durable COMPLETE state. Termination is therefore guaranteed **conditional on eventual
     availability of the poller and the request store**; it is not guaranteed against their permanent loss.
5. **Which rule governs.** The request-level bound is the only new ending. The lifecycle design's per-attempt
   sampled-failure `EVIDENCE_UNAVAILABLE` rule (lifecycle decision `:80-105`) stays gated off; enabling it would be
   a separate decision.
6. **Interaction with the signing stop.** Under L1 (an operating control, `V1-SERVICE-RESOLUTIONS.md:42`), the last
   acceptance is at least 216 h before not-after and signing stops 96 h before not-after. A request accepted at the
   last moment therefore has 5 days of signing; a later attempt that would need signing after the stop ends the
   request `REFUSED / SIGNING_CLOSED` as today. Its L_term falls about 5 days after not-after; between the signing
   stop and L_term only already-signed attempts can complete, and only receipts that pass the window checks (C4)
   are shipped.
7. **What it costs, stated.** A request that would eventually have qualified, including one already latched, can
   be refused. That is a liveness loss; by the tie rule and delivery fence it is never a delivered false receipt.
   Clients resubmit.
8. **What it does not change.** Safety properties, the expiry-on-complete-negative rule before L_term, the window's
   signing stop, and the verifier.
9. **Implementation duty, before the bound is enabled in production.** The `formal/tla/issuer-lifecycle/` model
   gains the deadline, the tie rule, a stalled worker that resumes after L_term, and the delivery fence, and is
   checked for: (a) never both COMPLETE and REFUSED; (b) no delivery for a request not durably COMPLETE; (c) under
   the availability assumption, every request is terminal by L_term + one poll interval. A broken companion
   (completion without the tie rule) must go red on (a) or (b). This is future work, not an existing proof; the
   code change is reviewed by Codex with the model's result.

## A12.2 Successor windows (sequential replacement)

**Registered text changed.** A9 (`phase-0-prereg-amendment-9.md:409-418`): "This amendment registers the first
issuance window only; it does not yet authorize successor issuance. … Without that registration, issuance stops at
the first window's end." The frozen profile's "V1 has one window and no overlap" (`V1-PROFILE.md:726`) is
descriptive of the first registration; its byte and check rules are not changed by this amendment.

**Registered change.** Successor issuance is authorized by **sequential replacement**, as A9 sketched it, keeping
the frozen V1 byte and check profile and verifier:
1. **Same DNS owner and git path** (`_tessera-v1.wamason.com`; `tessera-v1/key-assertion`).
2. **New service keys for each window** (a new KMS ML-DSA-65 key and a new slot-2 HSM key). The repository root
   signs the new key-assertion commit.
3. **Strictly sequential windows:** `next.not-before > previous.not-after` (both endpoints inclusive); each window at
   most 90 days.
4. **Drain, then replace.** The DNS owner holds exactly one TXT record (multiple records fail `DNS_RRSET`). The
   successor record replaces the previous one only after **every request accepted under the previous window is
   terminal**, recorded by the steward from the issuer's records. By A12.1 that is no later than the last
   acceptance + 14 days + one poll interval, under its availability assumption. This keeps an in-flight old attempt
   able to capture a snapshot matching its own window until it ends.
5. **Pre-commitment per window.** The successor's commit is OTS-stamped and reaches k = 6 confirmations before its
   first issuance (A9 C4), and its window opens no earlier than that. This does not replace the profile's chain-order
   check `h_git + 5 < h_receipt` (`V1-PROFILE.md:798-808`), which every receipt still passes on its own.
6. **The gap, stated.** Under L1 and the drain rule, each window change leaves a period with no new acceptances:
   from the old acceptance stop (at least 216 h before not-after) until the successor record is published and the
   issuer accepts under it. It is **at least 9 days** and, if an old request runs to its bound, **about 14 days**
   plus the operator's time to publish. Clients are told the dates in advance (closure is announced 14 days ahead,
   L1). Shortening the gap is an L1 operating change, outside this amendment; removing it needs overlapping
   windows, which the frozen V1 verifier cannot express (a V2 matter).
7. **Rotation registration, before the first successor issuance.** The steward records the dated registration A9
   requires, with vectors that test the predicates the frozen verifier actually checks:
   - a receipt from each window verifies under its own snapshot and commit;
   - a receipt under the old window's keys with T later than the old not-after → `INVALID / ISSUANCE_WINDOW`;
   - a receipt under the new window's keys with declared issue time earlier than the new not-before →
     `INVALID / ISSUANCE_WINDOW`;
   - a receipt under one window's keys presented with the other window's record or commit → rejected (authority
     mismatch);
   - a new-window receipt failing `h_git + 5 < h_receipt` → rejected.
   The verifier does **not** compare T with not-before, bound declared time by not-after, or compare windows across
   receipts (A10.2, `phase-0-prereg-amendment-10.md:358-373`); no vector claims otherwise. The model's property is
   an **issuer** property, on the issuer's wall clock: *the issuer requests signatures under a window's keys only
   while that window is the issuer's active window and before its signing stop, and accepts under the successor
   only after the drain and the replacement.* It is checked with its result recorded before the first successor
   issuance.
8. **Adversary scope, stated.** Rotation does not address (a) capture of both the DNS zone and the repository root,
   which lets an attacker publish its own keys and window and mint receipts that pass (V1-CONTRACT's capture row);
   or (b) a requester inside the issuing account, who can obtain signatures from both slots within their policies
   (A9 `:382-388`, `:401-404`). The issuer property in 7 holds for the issuer as deployed, not against these.

**Consequence for V1's first window** (not-before 2026-11-15, not-after 2027-02-01): acceptance stops by
2027-01-23 and signing on 2027-01-28. Continuing requires, prepared by about 2027-01-09: new service keys, a root
signing session for the successor commit (k = 6 before first issuance), the rotation registration of 7, and the
DNS replacement after the drain (no earlier than the last old request's end, at most about 2027-02-06). The
successor window's acceptances begin after that.

## A12.3 The canary's open findings (placeholder)
Levadura's beyond-window report on the 13 findings needing an amendment beyond A11 (obs-0185), when it arrives.

## A12.4 Operational posture (placeholder)
The V1 contract's limits gain: one operational machine today holds the administration of both signers (the AWS
management account login and the GCP project owner); the gate before reliance (DEPLOY.md) and its status.

## A12.5 Root rotation (placeholder)
Cryptoperiod (at most two years), triggers, procedure (a commit by the outgoing root naming its successor; a release
adding the new entry and closing the old interval), and how relying parties learn of it.

## Finding map (r1 review → r2)
| Finding | Where answered |
|---|---|
| A12-01 latch override unregistered | A12.1 inventory; change 2 (resolved choice 1) |
| A12-02 elapsed time ≠ excess lag | change 3: refusal by the bound, A2.1 trigger not invoked; A2.4 applied as written |
| A12-03 no durable transition or fence | change 4 (single writer, tie rule, delivery fence, availability assumption); change 9 model duty |
| A12-04 14 days not a guarantee; signing stop | change 1 (selected cap); change 6; change 5 (which rule governs) |
| A12-05 DNS replacement strands in-flight work | A12.2 item 4 (drain, then replace) |
| A12-06 vectors overstate the verifier | item 7 restated to checked predicates and an issuer property; item 5 keeps the chain-order check |
| A12-07 continuity overstated | item 6 states the gap (resolved choice 2); consequence paragraph |
| A12-08 inventory | A12.1 inventory; A9 locator `:409-418`; profile's "one window" reconciled |
| Prechecks 1, 3 | item 8 |
| Precheck 2, 4 | change 3; A12.1 inventory |
