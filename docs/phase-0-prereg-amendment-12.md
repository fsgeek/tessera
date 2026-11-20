# Tessera — Phase 0 Pre-Registration, Amendment 12 — V1 implementation: bounded termination; successor windows (r5 for signing, 2026-11-20)

> **Status: r5, ready for the author's signature (steward, Claude Opus 5.5, tenure from 2026-11-19). Not signed.**
> Reviews: r1 (five HIGH), r2 (four), r3 (three against promises), r4 final scoped round (two against promises, one
> duty), all in `docs/reviews/amendment-12/`. By the exit pre-registered in `BRIEF-r4.md`, r5 deletes the two
> remaining promises found false and keeps only what holds; there is no further round. Disposition: `DISPOSITION.md`. The two choices the r1 disposition
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
2. **The bound overrides the latch.** An invocation whose clock reads at or after a request's L_term may end that
   request only `REFUSED / EVIDENCE_UNAVAILABLE`, and every attempt it holds, latched or not, ends with it. Which
   ending a request has is whichever terminal write becomes durable first (5).
3. **What the refusal says.** It says the bound was reached. It does not assert that any attempt's lag exceeded S;
   the A2.1 trigger is not invoked. An artifact of such an attempt keeps its cryptographic validity and evidential
   admissibility; not having been shipped inside a receipt, it has no protocol standing, by A2.4 as written.
4. **What is promised, and what is not.**
   - *Safety (promised).* A request is never both COMPLETE and REFUSED, and no client credential obtains a receipt for
     a request whose durable state is not COMPLETE (construction rules in 5).
   - *The rule (promised).* An invocation whose clock reading is at or after L_term attempts no completion for that
     request; it attempts the refusal. The clock is the Lambda wall clock; skew within the registered ε is assumed and
     monotonicity across invocations is not, so a request may be treated by one invocation as past L_term and by a
     later one, whose clock reads earlier, as before it; the rule binds each invocation by its own reading.
   - *Not promised.* That a completion attempted before L_term becomes durable (an invocation can die or be fenced;
     the request is then refused at a later visit); that a refusal becomes durable by any time after L_term; that
     termination occurs at all if the poller or its dependencies (window configuration in S3, request store and
     index, the cleanup-obligation write) do not return, or if the poller's per-run budget never reaches the request.
     Nor is it promised that no COMPLETE becomes durable after L_term in real time: a completion write made before
     L_term can commit after it, and a later invocation whose clock reads earlier may complete. L_term governs what
     each invocation attempts by its own reading; it is not a real-time cutoff.
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
   - *Refusal begins with a fence (duty).* The refusal is made by fence-then-commit (`pipeline.py:255-261`). A
     pending earlier write can win before the fence; the fence then fails, and the invocation rereads the durable
     state and acts on it (a durable COMPLETE stands). After the fence succeeds, older record writes fail their guard.
     S3 puts are not fenced by it: each receipt object's name is computed by its writer from the SHA-256 of its own
     bytes, so a stale put of different bytes lands at a different name and cannot replace the object the durable
     COMPLETE record names; the API checks the fetched object's hash against that record before minting a URL.
   - *Access boundary and residual.* The results bucket is private; client credentials reach a receipt only through
     a URL the API mints for a durably COMPLETE request. An object left by a turn whose commit did not land is not
     reachable by any client credential, and persists until cleanup succeeds; cleanup can fail indefinitely, retaining
     its obligation (`pipeline.py:276-279,308-335`). A principal with S3 read access to the bucket (the operator, the
     issuer's roles) can read such an object, and it may verify; it was not shipped inside a receipt and has no
     protocol standing, as A2.1 (`:135-138`) and A2.4 already provide for chain-valid artifacts of unshipped attempts.
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
10. **Gates before the bound is enabled in production** (none is present today). The `formal/tla/issuer-lifecycle/` model gains the deadline, the
    cut as a read followed by a separate, possibly delayed write, a stale worker whose write is delayed across
    another invocation, content-addressed objects and URL fetch. It is checked for: (a) never both COMPLETE and
    REFUSED; (b) every fetch returns the object whose hash the durable COMPLETE record names, including under a stale put
    delayed past the winning commit, and a fence that loses to an earlier write ends in the durable winner's state; (c) no completion
    attempted by an invocation reading at or after L_term. Broken companions (fixed-key object; no cut) must go red on (b) and (c). Codex reviews
    the code change with the model's result. Detection D10 (`docs/V1-DETECTION-CONTRACT.md`) is extended to alarm on
    any request open past L_term + 1 hour, built, deployed and seen to fire under the gate's item 3. This is future
    work, not an existing proof or a present control.

## A12.2 Successor windows (sequential replacement)

**Registered text changed.**
- A9 (`phase-0-prereg-amendment-9.md:409-418`): "This amendment registers the first issuance window only; it does
  not yet authorize successor issuance. … Without that registration, issuance stops at the first window's end."
- ENCODING-V1 §7.1 (`formal/p8/ENCODING-V1.md:713-715`, frozen copy `formal/freeze-v1/objects/spec.bin:4091-4093`):
  "For V1 there is one window, of at most 90 days (`DNS_WINDOW_LENGTH`), with no overlapping successor: before it
  ends, either a rotation mechanism is registered or issuance stops".
- Profile (`docs/V1-PROFILE.md:725-726`, frozen copy `spec.bin:725-727`): "V1 has one window and no overlap."

Found by searching the registered and frozen text for "one window", "single window" and "successor". Not operative,
and not changed: A10.4.1's "V1's configuration lists exactly one entry, authorized at the freeze" and "This cannot
occur in V1, which has one window" (`phase-0-prereg-amendment-10.md:582-584,600-601`; `spec.bin:2608-2610,2627`)
belong to the service-key listing option, which the author cut on 2026-10-23
(`docs/decisions/2026-10-19-listing-cut.md`); historical descriptions of A9's first registration
(`formal/p8/ENCODING-V1.md:46`; `formal/p8/PROOF.md:55,507`) remain true of that registration.

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
   obtain one stays open until one of its existing endings applies (`SNAPSHOT_IMPOSSIBLE` only where its evidence
   predicate establishes impossibility, `pipeline.py:1185-1215`) or until L_term. That residual is unchanged by
   rotation. The old request set is closed only after the old acceptance stop plus the API function's maximum
   invocation time, so no in-flight old API invocation can accept after the steward records the drain.
5. **New side: an acceptance fence.** The issuer accepts under the successor only after, in order: the successor's
   not-before has arrived by the issuer's clock (the API's existing not-before check, `api.py:127-134`, kept as a
   duty); the successor commit has k = 6 confirmations (A9 C4); the successor record is published; a deployment switches the issuer's
   window configuration (a new function version, so no warm invocation keeps the old configuration,
   `lambda_app.py:43,61-65`); and the issuer itself has captured and validated a snapshot of the successor record
   through its configured resolver, no earlier than the old record's TTL after publication. A successor request can
   still meet a stale cached answer; the issuer retries on mismatch (`pipeline.py:739-748`), and any loss beyond that
   is the ordinary snapshot residual of 4. The chain-order check `h_git + 5 < h_receipt` (`V1-PROFILE.md:798-808`)
   still applies to every receipt.
6. **The gap, stated.** Each window change has a period with no new acceptances, from the last actual acceptance
   under the old window to the first under the successor. Its minimum follows from dates alone: the last old
   acceptance is at least 216 h before the old not-after (L1), and no successor acceptance precedes the successor
   not-before (item 5), which is strictly later than the old not-after (item 3). So, **by the issuer's clock readings**, the gap
   exceeds 9 days. In real time it can be shorter by the clocks' skew and by the time between an acceptance's clock
   read and its write; no real-time minimum is promised. Its
   maximum is not promised: it depends on the drain (A12.1 promises no time by which old requests end), publication,
   propagation and deployment.
7. **Telling clients (contract duty).** `docs/V1-CONTRACT.md` §3 gains: *"Issuance runs in windows of at most 90
   days. Between windows there is a period of at least nine days in which new requests are refused; receipts already
   issued are unaffected."* At least 14 days before an acceptance stop, the steward tells every client with a key,
   directly and on the service page: the last acceptance time, the reason, and the earliest date successor
   acceptance can open, updated when it opens.
8. **Rotation registration, before the first successor issuance.** The steward records the dated registration A9
   requires. Each negative vector applies **one logical mutation** to a valid receipt, regenerating the evidence that
   depends on it (signatures, anchors, a time-compatible snapshot) so that every unrelated predicate still passes,
   and requires non-acceptance, naming the expected first reason where the verifier's check order determines it:
   - a receipt from each window verifies under its own snapshot and commit (positive; no mutation);
   - old window's keys, T later than the old not-after → `ISSUANCE_WINDOW`;
   - new window's keys, declared issue time earlier than the new not-before → `ISSUANCE_WINDOW`;
   - new-window receipt with the old window's DNS snapshot, time-compatible with the receipt (commit unchanged) →
     not accepted (expected `DNS_KEY_MISMATCH` or `CHANNEL_VALUE_MISMATCH`);
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
permitted stops are used: acceptance stops 2027-01-23T00:00Z, signing 2027-01-28T00:00Z, and the client notice is due
by 2027-01-09. Preparation (new service keys; a root signing session for the successor commit, which needs k = 6
before first issuance; the rotation registration of 8) should be complete by about that date. A request accepted at
the stop has L_term 2027-02-06T00:00Z, after which an invocation reading its clock attempts only its refusal; when it
ends, and so when the drain ends, is not promised. Successor acceptance opens at the fence of 5, no earlier than the successor not-before.

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
| r3 R3-01 tie | change 4: a rule on each invocation's behaviour; outcomes in flight not promised |
| r3 R3-02 detection, cleanup | change 4 not promised; change 5 residual (S3 principals; A2.1/A2.4); change 10 D10 as a gate |
| r3 R3-03 fence | change 5: refusal begins with the existing fence; objects by content addressing |
| r3 R3-04 gap minimum | items 5 (not-before in the fence), 4 (old API invocations drained), 6 (minimum from dates) |
| r3 R3-05 dates | item 6 maximum not promised; consequence paragraph |
| r3 R3-06 inventory | A12.2 inventory: frozen profile copy; A10.4.1 not operative (listing cut); historical text |
| r4 R4-01 absolute deadline | changes 2, 4: per-invocation rule and durable winner; real-time cutoff disclaimed |
| r4 R4-02 real-time gap | item 6: minimum by issuer clock readings; real-time minimum not promised; consequence paragraph |
| r4 R4-03 fence and objects | change 5 fence duty (reread on loss; hash-named objects, hash checked before URL); change 10 (b) |
| r3 R3-07 vectors | item 8: logical mutation with regenerated evidence; time-compatible snapshot; SNAPSHOT_IMPOSSIBLE wording |
