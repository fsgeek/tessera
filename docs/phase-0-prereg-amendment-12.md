# Tessera — Phase 0 Pre-Registration, Amendment 12 — V1 implementation: bounded termination; successor windows (DRAFT r3, 2026-11-20)

> **Status: DRAFT r3 by the steward (Claude Opus 5.5, tenure from 2026-11-19). Not signed.** Reviews: r1
> (`CODEX-REVIEW-r1.md`, five HIGH), r2 (`CODEX-REVIEW-r2.md`, four HIGH). r3 narrows each claim to what holds and
> moves what does not yet hold into named implementation duties (map at the end). The two choices the r1 disposition
> put to the author were resolved by him on 2026-11-19 ("As steward, I will abide by your recommendation"), as
> OWNER DECISIONS adopted by his signature. Sections 3–5 are placeholders.
> The author's first commit containing the final text is its signing act (the A11 convention). Layered on the
> original and Amendments 1–11, none of which is edited. Every registered sentence this amendment changes is quoted
> with its locator. All times are UTC.

## A12.1 Bounded termination

**Registered text changed.**
- A2.1 (`phase-0-prereg-amendment-2.md:131-135`): "Timeliness is **latched at eligibility**: an attempt eligible
  within the envelope cannot be expired by later packaging or scheduling delay — eligible/finalizing, shipped, and
  expired/refused are mutually exclusive states".
- A2.1 (`:142-145`): "'every timely-eligible attempt ships' is a contract obligation on the implementation".
- A2.1 (`:156-157`): "so such an attempt latches eligible/finalizing and cannot expire."
- A2.1 (`:157-160`): "Expiry (on the final attempt, refusal) applies only **strictly after** the boundary, and only
  to attempts with no timely-latched eligibility."
- A2.3 (`:261-264`): "an attempt expires when wall time passes `declared + δ + S`, except that timely-latched
  eligibility excludes expiry — eligible/finalizing, shipped, and expired/refused are mutually exclusive states".
- A2.3 (`:288-289`): "termination is a contract obligation on the implementation, not a proven liveness property."

Each is qualified by the same clause: *except that a request's termination bound (A12.1) ends the request and every
attempt it holds, latched or not.* Not changed, and applied as written: A2.1's "may be refused" permission
(`:135-138`) and A2.4's confinement of standing (`:307-315`).

**Why.** The issuer ends an attempt only on complete negative evidence (lifecycle decision rev 5.3.1). A dependency
that fails for good leaves a request open indefinitely, and an open request is a resource an attacker can hold (the
author, 2026-10-30: "Why wouldn't you just define a failure after some finite period of time (the FLP
work-around)? Otherwise, I'd worry that you've created a denial-of-service attack vector.").

**Registered change.**
1. **The bound.** Each request has a termination deadline **L_term = acceptance time + 14 days**, acceptance time as
   recorded by the issuer. 14 days is a **selected cap**, not a derived guarantee: it exceeds the nominal budget
   N × (δ + S) = 12 days (A2.3) by 2 days, but time before, between and after attempts is not bounded by A2.3, so
   no request is promised its full nominal budget within the cap.
2. **The bound overrides the latch.** A request that has not begun its completion commit before L_term ends
   `REFUSED / EVIDENCE_UNAVAILABLE`, and every attempt it holds, latched or not, ends with it.
3. **What the refusal says.** It says the bound was reached. It does not assert that any attempt's lag exceeded S;
   the A2.1 trigger is not invoked. An artifact of such an attempt keeps its cryptographic validity and evidential
   admissibility; not having been shipped inside a receipt, it has no protocol standing, by A2.4 as written.
4. **What is promised, and under what assumptions.**
   - *Safety (promised).* A request is never both COMPLETE and REFUSED, and no client path yields a receipt for a
     request whose durable state is not COMPLETE (construction rules in 5).
   - *The cut (promised).* No completion commit is **begun** at or after L_term, by the issuer's clock (Lambda wall
     clock, synchronised by the platform; the issuer assumes its skew stays within the registered ε and is not
     monotonic across invocations). A completion commit begun before L_term may become durable shortly after it;
     that request ends COMPLETE. The promise is about when completion may start, not about commit latency.
   - *Termination (conditional, no real-time bound).* A request open at L_term is refused at the first poll that
     visits it at or after L_term and completes the refusal's writes. That requires the poller to run and its
     dependencies to be available: the window configuration in S3 (read at cold start), the request store and its
     index, and the cleanup-obligation write that precedes every terminal write. It also requires the poller's
     per-run budget to reach the request; the poller pages active requests and may defer work. **No bound after
     L_term is promised.** Detection D10 (`docs/V1-DETECTION-CONTRACT.md`) alarms on any request open past
     L_term + 1 hour, so a request the bound did not end is seen, not silent.
5. **Construction rules (implementation duties; not all present in the deployed code).**
   - *Who writes what.* The API creates a request (ACCEPTED, or REFUSED at acceptance) and records upload completion
     with a version compare-and-set (`api.py:98-106,127-145`). Every later lifecycle transition, including every
     terminal transition after acceptance, is made only by the poller, one invocation at a time (reserved
     concurrency 1, `infra/main.tf:365`), with a compare-and-set on version and lifecycle guard (`aws.py:88-104`);
     a killed invocation's pending writes are fenced by the next invocation's version bump (`pipeline.py:255-261`).
   - *The cut, in code.* Before the COMPLETE commit, the poller reads its clock after the receipt object is stored;
     if that reading is at or after L_term it commits the refusal instead. (Today `_ship` has no such check,
     `pipeline.py:1222-1228`, and `_end_request` refuses to end a latched attempt, `:269-271`; both change.)
   - *Receipt objects are content-addressed.* The receipt is stored at a key derived from its SHA-256
     (`result/<rid>/<receipt_sha256>.json`), and the API mints a URL only for the key named by the durable COMPLETE
     record's `receipt_sha256`. A stale worker's delayed put can then never replace the object a client fetches.
     (Today the key is fixed, `result/<rid>/receipt.json`, and the bucket is unversioned, `infra/main.tf:89-93`;
     this is a defect in the deployed code, corrected under this duty whether or not A12 is signed.)
   - *Access boundary.* The results bucket is private; only the API role mints URLs, and only for COMPLETE. An object
     left by a turn whose commit did not land is not reachable by any client path; it persists until cleanup
     succeeds, which is eventual, not immediate.
6. **Which rule governs.** The request-level bound is the only new ending. The lifecycle design's per-attempt
   sampled-failure `EVIDENCE_UNAVAILABLE` rule (lifecycle decision `:80-105`) stays gated off.
7. **Interaction with the signing stop.** Under L1 (an operating control, `V1-SERVICE-RESOLUTIONS.md:42`), the last
   acceptance is at least 216 h before not-after and signing stops 96 h before not-after; L1 permits earlier stops.
   A request accepted at the latest permitted moment has 5 days of signing; a later attempt needing signing after the
   stop ends the request `REFUSED / SIGNING_CLOSED` as today. Its L_term falls about 5 days after not-after; between
   the signing stop and L_term only already-signed attempts can complete, and only receipts that pass the window
   checks (C4) are shipped.
8. **What it costs, stated.** A request that would eventually have qualified, including one already latched, can be
   refused. That is a liveness loss, never a delivered false receipt. Clients resubmit.
9. **What it does not change.** Safety properties, the expiry-on-complete-negative rule before L_term, the window's
   signing stop, and the verifier.
10. **Before the bound is enabled in production.** The `formal/tla/issuer-lifecycle/` model gains the deadline, the
    cut as a read followed by a separate, possibly delayed write, a stale worker whose write is delayed across
    another invocation, content-addressed objects and URL fetch. It is checked for: (a) never both COMPLETE and
    REFUSED; (b) every fetch returns the object whose hash the durable COMPLETE record names; (c) no completion
    begun at or after L_term. Broken companions (fixed-key object; no cut) must go red on (b) and (c). Codex reviews
    the code change with the model's result. This is future work, not an existing proof.

## A12.2 Successor windows (sequential replacement)

**Registered text changed.**
- A9 (`phase-0-prereg-amendment-9.md:409-418`): "This amendment registers the first issuance window only; it does
  not yet authorize successor issuance. … Without that registration, issuance stops at the first window's end."
- ENCODING-V1 §7.1 (`formal/p8/ENCODING-V1.md:713-715`, frozen copy `formal/freeze-v1/objects/spec.bin:4091-4093`):
  "For V1 there is one window, of at most 90 days (`DNS_WINDOW_LENGTH`), with no overlapping successor: before it
  ends, either a rotation mechanism is registered or issuance stops".
- Profile (`docs/V1-PROFILE.md:725-726`): "V1 has one window and no overlap."

Qualification: *each key-publication record carries exactly one window; windows succeed one another without
overlap, under A12.2.* The frozen byte and check rules, the frozen spec bytes and the verifier are unchanged; only
the global "one window" statement is qualified. The profile's path requirement (`V1-PROFILE.md:778-780`) is met by
keeping the same path.

**Registered change.** Successor issuance is authorized by **sequential replacement**, as A9 sketched it:
1. **Same DNS owner and git path** (`_tessera-v1.wamason.com`; `tessera-v1/key-assertion`).
2. **New service keys for each window** (a new KMS ML-DSA-65 key and a new slot-2 HSM key). The repository root
   signs the new key-assertion commit.
3. **Strictly sequential windows:** `next.not-before > previous.not-after` (both endpoints inclusive); each window at
   most 90 days.
4. **Old side: drain, then replace.** The DNS owner holds exactly one TXT record (multiple records fail
   `DNS_RRSET`). The successor record replaces the previous one only after every request accepted under the previous
   window is terminal, as recorded by the steward from the issuer's records. This keeps the old record available to
   old attempts while they run. It does **not** make every old attempt able to obtain a usable snapshot: a snapshot
   must still fall within its attempt's declared-time interval (`verify.py:256-257`), and an attempt that cannot
   obtain one ends `SNAPSHOT_IMPOSSIBLE` as today (`pipeline.py:1205-1215`). That residual is unchanged by rotation.
5. **New side: an acceptance fence.** The issuer accepts under the successor only after, in order: the successor
   commit has k = 6 confirmations (A9 C4); the successor record is published; a deployment switches the issuer's
   window configuration (a new function version, so no warm invocation keeps the old configuration,
   `lambda_app.py:43,61-65`); and the issuer itself has captured and validated a snapshot of the successor record
   through its configured resolver, no earlier than the old record's TTL after publication. A successor request can
   still meet a stale cached answer; the issuer retries on mismatch (`pipeline.py:739-748`), and any loss beyond that
   is the ordinary snapshot residual of 4. The chain-order check `h_git + 5 < h_receipt` (`V1-PROFILE.md:798-808`)
   still applies to every receipt.
6. **The gap, stated.** Each window change has a period with no new acceptances: from the **last actual acceptance**
   under the old window (no later than 216 h before not-after; L1 permits earlier) until the acceptance fence of 5
   opens. It is at least 9 days. Its end depends on the drain (up to 14 days after the last old acceptance, longer if
   A12.1's termination assumptions fail), publication, propagation and deployment; no fixed end is promised.
7. **Telling clients (contract duty).** `docs/V1-CONTRACT.md` §3 gains: *"Issuance runs in windows of at most 90
   days. Between windows there is a period of at least nine days in which new requests are refused; receipts already
   issued are unaffected."* At least 14 days before an acceptance stop, the steward tells every client with a key,
   directly and on the service page: the last acceptance time, the reason, and the earliest date successor
   acceptance can open, updated when it opens.
8. **Rotation registration, before the first successor issuance.** The steward records the dated registration A9
   requires. Each vector applies **one** mutation to an otherwise valid receipt (valid substituted snapshot or
   commit, matching proofs and headers, every unrelated check passing) and requires non-acceptance, naming the
   expected first reason where the verifier's check order determines it:
   - a receipt from each window verifies under its own snapshot and commit;
   - old window's keys, T later than the old not-after → `ISSUANCE_WINDOW`;
   - new window's keys, declared issue time earlier than the new not-before → `ISSUANCE_WINDOW`;
   - new-window receipt with the old window's DNS snapshot (commit unchanged) → not accepted (expected
     `DNS_KEY_MISMATCH` or `CHANNEL_VALUE_MISMATCH`);
   - new-window receipt with the old window's commit (snapshot unchanged) → not accepted;
   - new-window receipt failing `h_git + 5 < h_receipt` → not accepted.
   The verifier does **not** compare T with not-before, bound declared time by not-after, or compare windows across
   receipts (A10.2, `phase-0-prereg-amendment-10.md:358-373`); no vector claims otherwise. The model's property is an
   **issuer** property, on the issuer's clock: *the issuer requests signatures under a window's keys only while that
   window is its active window and before its signing stop, and accepts under the successor only after the drain of
   4 and the fence of 5.* Its result is recorded before the first successor issuance.
9. **Adversary scope, stated.** Rotation does not address (a) capture of both the DNS zone and the repository root,
   which lets an attacker publish its own keys and window and mint receipts that pass (V1-CONTRACT's capture row);
   or (b) a requester inside the issuing account, who can obtain signatures from both slots within their policies
   (A9 `:382-388`, `:401-404`). The property in 8 holds for the issuer as deployed, not against these.

**Consequence for V1's first window** (not-before 2026-11-15T00:00Z, not-after 2027-02-01T00:00Z). If the latest
permitted stops are used: acceptance stops 2027-01-23T00:00Z, signing 2027-01-28T00:00Z, the client notice is due by
2027-01-09, and preparation (new service keys; a root signing session for the successor commit, which needs k = 6
before first issuance; the rotation registration of 8) should be complete by about the same date. The drain ends
when the last old request is terminal: about 2027-02-06 if that request runs to its bound and A12.1's assumptions
hold. Successor acceptance opens at the fence of 5, after that. An earlier stop moves every date earlier.

## A12.3 The canary's open findings (placeholder)
Levadura's beyond-window report on the 13 findings needing an amendment beyond A11 (obs-0185), when it arrives.

## A12.4 Operational posture (placeholder)
The V1 contract's limits gain: one operational machine today holds the administration of both signers (the AWS
management account login and the GCP project owner); the gate before reliance (DEPLOY.md) and its status.

## A12.5 Root rotation (placeholder)
Cryptoperiod (at most two years), triggers, procedure (a commit by the outgoing root naming its successor; a release
adding the new entry and closing the old interval), and how relying parties learn of it.

## Finding map
| Finding | Where answered |
|---|---|
| r1 A12-01 latch override | A12.1 inventory and qualifying clause; change 2 |
| r1 A12-02 elapsed time ≠ excess lag | change 3 |
| r1 A12-03, r2 R2-01 tie and durability | change 4 (cut on commit *start*, clock assumption), change 5 (cut in code), change 10 |
| r2 R2-02 no real-time bound | change 4 termination: conditional, dependencies named, no bound after L_term, D10 alarm; change 5 who writes what |
| r2 R2-03 object not fenced | change 5: content-addressed receipts (deployed defect, fixed regardless), access boundary; change 10 (b) |
| r1 A12-04 cap, signing stop | changes 1, 6, 7 |
| r1 A12-05, r2 R2-04 cutover | A12.2 items 4 (drain; snapshot residual stated) and 5 (acceptance fence) |
| r1 A12-06, r2 R2-07 vectors | item 8 (single mutation, non-acceptance, first reason where determined) |
| r1 A12-07, r2 R2-06 gap and dates | items 6, 7 (contract text and client notice); consequence paragraph (conditional dates) |
| r1 A12-08, r2 R2-05 inventory | A12.1 adds A2.1 `:157-160`; A12.2 adds ENCODING-V1 §7.1, frozen spec, profile |
| Prechecks 1, 3 | item 9 |
| Prechecks 2, 4 | changes 3, 4; inventories |
