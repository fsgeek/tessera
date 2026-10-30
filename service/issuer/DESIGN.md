# V1 issuer: design (Phase 1a)

> **Status: OWNER DESIGN, 2026-10-26** (Claude Opus 5.5). Inputs:
> - `docs/V1-SERVICE-CONTRACT.md` and `docs/V1-SERVICE-RESOLUTIONS.md` (stamped at `2411714`): what clients see;
> - the frozen profile (`formal/freeze-v1/`), §4 issue order, §6–§8, §15: what a receipt must be;
> - `prototype/e2e/` and its findings E-01..E-06: what real issuance taught us.
>
> Service code never imports `prototype/`, and the issuer earns its own evidence. Built by one agent against
> stand-in signers. The signer placement question is open with the author and does not change this design.

## Shape

| Part | Role | AWS form (A9.1: API Gateway + Lambda + KMS) |
|---|---|---|
| API | `POST /v1/requests`, `GET /v1/requests/{key}`, `GET /v1/requests/{key}/receipt` | API Gateway (API keys = client credentials) + Lambda |
| Request store | Request key → state, content digest, timestamps, result location | DynamoDB, with TTL for the 30-day expiry and content-free tombstones until closure |
| Result store | Completed receipts | S3, with a lifecycle rule deleting after 30 days |
| Pipeline | Sign → `A_sig` → stamp → confirm → snapshot → headers → pre-ship checks → assemble | Lambda steps, driven by a scheduled poller (every 10 min) that advances each request one stage |
| Signers | Two **policy signers** behind one interface: the issuer enqueues a frame and reads a signed response | SQS request and response queues per slot. The slot-2 signer exists (GCP). The KMS-slot signer runs wherever the author's decision puts it. The issuer holds no signing credential. |
| Window preparation | The git key assertion and its k = 6 pre-commitment, and the DNS record, before the window opens | An operator runbook step, not an API path |

## Client behaviour (from the stamped resolutions)

- **Submit:** raw bytes, at most 1 MiB, with a header `Tessera-Request-Key: <UUID>`.
  - Response 202 ACCEPTED with the key, or 4xx REFUSED with a reason: `TOO_LARGE`, `OUTSIDE_WINDOW`,
    `SIGNING_UNAVAILABLE`, `CLOSING`, `BAD_REQUEST`.
  - The same key with the same content returns the same request. The same key with different content returns 409.
- **States:** ACCEPTED, then COMPLETE or REFUSED (`ATTEMPTS_EXHAUSTED`, `SIGNING_CLOSED`, listing each attempt's
  ending), or FAILED (`CONTENT_UNAVAILABLE`: the content is not available when attempt 1 would start - an upload
  never finished, or completed content lost before attempt 1; no attempt exists). After 30 days: EXPIRED.
  *(Superseded 2026-10-30: "FAILED 24 h after acceptance" contradicted A2 and is withdrawn; see "Issuance lifecycle"
  below.)*
- **Retrieval:** only by the credential that submitted. The response carries the receipt's SHA-256.

## Issuance rules carried from real runs

- **E-01:** the signers are started on demand. No standing scheduler is needed.
- **E-02:**
  - Every request to a signer carries a request id derived from (request key, frame hash).
  - Every response is recorded with the frame hash and signature hash, whether or not it is used.
  - Responses nobody is waiting for are recorded, then deleted.
  - A retry reuses a complete, verified signature set rather than signing again.
- **Ship only complete receipts:** the pre-ship checks of profile §4 and §15.7 run on the assembled bundle with the
  service verifier's own logic, called as a library. A bundle that fails is never shipped. *(Updated 2026-10-30: it
  is no longer FAILED. A failing check that depends only on the attempt's frozen material discards the attempt with
  the reason (step 7); a snapshot failure recaptures the snapshot; anything else is retried. See "Issuance
  lifecycle".)*
- **Window:** signing stops 96 h before not-after, and acceptance stops delta + S + 24 h before that (216 h before
  not-after; L1 as revised, applied in `window.py`). That spacing is an operating allowance, not a processing
  guarantee: allocation can be delayed. An attempt whose T would exceed not-after is not shipped (A9 issuer
  invariant); a request whose next attempt would need signing after the stop is REFUSED `SIGNING_CLOSED`.

## Tests the builder must provide

1. **Unit tests** for every state transition, including duplicate keys and key/content mismatch.
2. **A local end-to-end test** with stand-in signers and stand-in chain and calendar. It drives a request to COMPLETE
   and verifies the bundle with `service/verifier` (`--mode test`) as `VALID_STRICT`.
3. **Fault tests:** a signer timeout followed by a late answer (E-02); a lost API response, then lookup by key; the
   24 h failure (superseded: stalls now keep the request open; see "Issuance lifecycle"); the stop margin.
4. **Infrastructure as code (Terraform)** that a later step applies to AWS. Nothing is applied by the builder.

## Changes after review

Codex review `docs/reviews/issuer/CODEX-REVIEW.md` (IS-01 to IS-11); dispositions and test names in
`docs/reviews/issuer/DISPOSITION.md`. Only the changes that alter this design are listed here.

- **IS-03 (signer contract):** each policy signer enforces the signing stop itself, immediately before it signs: its
  own configured stop (the window's not-after minus 96 h) and a per-request `sign_by` the issuer now adds to every
  request (the earlier of the signing stop and acceptance + 24 h; *superseded 2026-10-30: now the signing stop
  only, the 24 h bound is withdrawn*). Past either, it answers `REFUSED`
  (`SIGNING_STOPPED`). The stand-in signer does this. **Open:** the deployed slot-2 signer and the KMS-slot signer
  are outside `service/issuer` and must adopt the same check before issuance.
- **IS-05 (submission order):** the API creates the request record first (state ACCEPTED, stage `upload`), then
  stores the content, then moves the stage to `frames`. A retry with the same key and content finishes an
  interrupted upload. The poller fails an upload still unfinished after 15 min (`CONTENT_UNAVAILABLE`).
- **IS-04 (tombstone):** the request record and its key tombstone are written in one DynamoDB transaction. A
  repeat submission repairs a missing tombstone.
- **IS-06 (retrieval; owner decision, supersedes the earlier Range approach):** a receipt (about 5 MB, since every
  bundle carries the frozen spec and vectors) is retrieved with ONE plain GET, as docs/V1-SERVICE-RESOLUTIONS.md
  S2/S5 describe. `GET /v1/requests/{key}/receipt` checks that the caller's credential owns the request and that it
  is COMPLETE and not EXPIRED; only then it mints a fresh pre-signed S3 GET URL valid for 300 seconds and answers
  303 to it, with the receipt's SHA-256 in `Tessera-Receipt-SHA256`. No URL is minted for another credential (404),
  an expired request (410) or a non-complete one (409); the lifetime is never above 300 s; minted URLs are never
  stored or reused. The receipt object is deleted 30 days after the end, so later URLs fail. The Range requirement
  and 416 `RANGE_REQUIRED` are removed.
- **IS-07 (deletion):** S3 lifecycle is no longer the deletion mechanism. Ending a request first records a
  cleanup obligation (`CLEAN#<rid>`, kept apart from the record). Each poll retries the obligation until a listing
  shows nothing left: content, work files and frames at the end; the receipt 30 days after the end. Lifecycle
  rules stay as a 31-day backstop. *(Superseded 2026-10-30, revision 5.3.1: no age rule; the backstop expires
  only objects the obligation has tagged cleanup-due.)*
- **IS-09 (large frames):** a signer request whose inline message would exceed 256 KiB carries `frame_ref` (an
  immutable object `frames/<rid>/<sha256>`) and `frame_sha256` instead of `frame_b64`. The signer refuses unless
  the object's SHA-256 matches. Signer roles get read access to `frames/*` only. **Open:** the deployed signers
  must accept `frame_ref`.
- **IS-01, IS-08 (signature bookkeeping):** a verified response is logged as "used" before its signature becomes
  eligible. Each signature is stored under its own name (`sig-<job>-<sha256>`), and its job is merged into the
  record with compare-and-set retries. Sealing requires the log record. Before any re-send, a stored signature
  that verifies and is logged is adopted.
- **IS-02:** COMPLETE is decided on a fresh clock in the terminal transition, and `ended_at` is the actual
  transition time.

Codex confirmation review `docs/reviews/issuer/CODEX-CONFIRM.md` (CF-01 to CF-05); dispositions in the same file.

- *(CF-01, CF2-01 and the deadline half of CF-02 are superseded 2026-10-30 by "Issuance lifecycle" below: there is no
  deadline, `api.settle` and the unconfirmed COMPLETE are removed, and COMPLETE is one guarded terminal write.)*
- **CF-01 (completion at the deadline; supersedes the IS-02 bullet above):** ending a request persists the cleanup
  obligation first and reads the clock only after that. COMPLETE is then committed *unconfirmed* and settled
  (`api.settle`): whoever reads the committed record and then reads the clock before the deadline confirms it
  (`confirmed_at`, and `ended_at` = that reading, so it is never earlier than the commit); at or after the deadline
  an unconfirmed COMPLETE becomes FAILED `NOT_COMPLETE_WITHIN_24H`. Both are compare-and-set writes, so they never
  both win. Status and retrieval report COMPLETE only once it is confirmed (an unconfirmed one reads as ACCEPTED, and
  the status call settles it first). The poller (in the issuer's own invocation) and the cleanup obligation settle a
  completion an interrupted invocation left. A delayed obligation or terminal write ends as FAILED, and a completion
  a client saw before the deadline stays COMPLETE. *(Corrected 2026-10-27, CF2-01: this bullet first said "no timing
  assumption is needed". That was wrong. The confirmation is itself a write, and it can commit after the deadline.
  See the CF2-01 bullet.)*
- **CF2-01 (confirmation at the deadline, `CODEX-CONFIRM-2.md`):** the confirmation is confirmed only when decided
  at least `WRITE_LEASE_S` before the deadline. It therefore commits before the deadline *if* AWS commits or rejects
  every request within the lease, which is the same assumption as CF-02. That assumption is stated, not established
  (CF3-01): `docs/decisions/2026-10-27-service-clock-tolerance.md`. `ended_at` is the decision's reading, which is
  never earlier than the first COMPLETE write but may precede the confirmation's commit by up to the tolerance
  (CF3-04). Inside the last lease a completed request stays unconfirmed (it reads as ACCEPTED), and at
  the deadline it is FAILED `NOT_COMPLETE_WITHIN_24H`. Cleanup waits until it is settled.
- **CF2-02, CF3-02, CF3-03 (clock after reads):** `status`, `receipt`, `submit` and repeat submissions read the
  clock after the records they decide on, so a slow read cannot carry a stale clock past expiry or the acceptance
  stop. What remains (a write committing later than its decision) is the stated tolerance.
- **CF-02 (late writers):** every issuer write runs inside a Lambda invocation that saw the request ACCEPTED, so none
  lands later than `WRITE_LEASE_S` (15 min, the Lambda maximum; a test checks every Terraform timeout is within it)
  after the end was first seen. The first cleanup pass after the end records `fence_until` in the obligation; until
  then each poll deletes again, and only a listing taken after it discharges the obligation. This also covers writes
  that commit although their caller saw an error.
- **CF-03 (expiry at minting):** the receipt endpoint re-reads the record and the clock after the object check and
  mints no URL once the request has expired. The 300-second URL design is unchanged.
- **CF-04 (deletion errors):** `S3ResultStore.delete` raises on any per-object error in a DeleteObjects response and
  stops after a bounded number of rounds. The obligation is kept and the poller goes on to the other obligations.

## Issuance lifecycle (2026-10-30)

Implements `docs/decisions/2026-10-29-issuance-lifecycle.md` (revision 5.3.1) and its "Implementation boundary until
the author decides"; the checked protocol is `formal/tla/issuer-lifecycle/IssuerLifecycleR53.tla`. Tests:
`tests/test_lifecycle.py` (one group per brief item); deadline tests in `test_faults.py`, `test_review_fixes.py`,
`test_confirm_fixes.py`, `test_states.py` and `test_infra.py` are rewritten and say so in their docstrings.

- **Attempts** (`tessera_issue/lifecycle.py`): a request has attempts 1..3 (`attempts`, `cur`). Each has its own
  declared issue time (its allocation time), frames, signing jobs (request ids scoped by attempt), A_sig, a fresh stamp,
  evidence, latch and end; its objects live under `work/<rid>/a<n>/`. A signer response is routed by attempt; one for
  an attempt that is not current is logged `other-attempt` and ignored.
- **One writer.** Only the poller makes lifecycle transitions. `api.status` and `api.receipt` write nothing; `settle`
  and `fail_after` are gone. Every poller write is guarded on (request state, current attempt id, current attempt
  state) and the version (`stores.lifecycle_guard`; DynamoDB conditions on the item attributes `lstate`, `latt`,
  `lastate` and `version`).
- **Fence.** Before fetching evidence for an attempt (stages `evidence`, `finalize`, `snapshot`), the poller commits a
  guarded version bump and proceeds only if it committed.
- **Eligibility and latch.** The attempt's proof must stamp SHA-256 of its own A_sig; the verifier's `select` picks the
  lowest qualifying height among attestations whose full pinned, linked h..h+5 segment was obtained; the three A2.2
  conjuncts are evaluated on it. On eligibility, at any time while the attempt is open, the poller writes the
  presentation (proof pruned to the selected height, with its six headers) as an immutable digest-named object, then
  commits the latch with `observed_at` and its reference.
- **Ending.** Only complete negative evidence (every stamped calendar attested, every attestation's segment obtained,
  the selected presentation failing a conjunct) ends an open attempt: DISCARDED at or before B, EXPIRED after it.
  The end and the next attempt's allocation are one guarded write; after attempt 3 the same write records REFUSED
  `ATTEMPTS_EXHAUSTED`; if the next attempt would need signing after the stop, REFUSED `SIGNING_CLOSED`. A signer
  refusal discards that (unsigned) attempt the same way.
- **After the latch** (step 7; ILI-01, ILI-02, ILC-I-01). Transient failures are retried indefinitely. The pre-ship
  check returns the verifier's per-row ledger, and `pipeline.classify_preship` decides in this preference order (not
  by the first failing check):
  1. If ANY failing check is INVALID on frozen material, that check decides, wherever it falls: the attempt's frames,
     frozen signatures, A_sig, manifest and keys; the preserved receipt presentation (rows 11.x-12.x, including
     OTS_MERKLE_MISMATCH and the transaction-shape/txid check); the window's frozen git material (rows 14.1-14.6 and
     14.8); 16.1 (unless a snapshot row also fails). The attempt is discarded, reason `PRESHIP:INVALID/<code>@<row>`.
  2. Else, if a check INVALID on the snapshot's own bytes fails (13.1, 13.2, 13.3, 13.6, 13.7, 15.1, 15.2, 13.4's
     SNAPSHOT_STAMP_MISMATCH / OTS_FORMAT, and 13.5's RRSIG-time reasons), this snapshot can never pass: it is recaptured, or the attempt is
     discarded `SNAPSHOT_IMPOSSIBLE` if no lawful snapshot can be obtained any more (below).
  3. Everything else is retried, keeping the current snapshot: headers and pins, container, catalog and trust
     configuration (14.7), every configuration-dependent snapshot result (13.5 except its RRSIG-time reasons, which
     are in rule 2 - `validate_snapshot` against the configured root KSKs, reliance periods and trust horizon - and
     13.4's header outcomes), and every UNVERIFIABLE result outside rule 2.
  T > not-after discards (`T_AFTER_NOT_AFTER`).
- **SNAPSHOT_IMPOSSIBLE** (ILI-02, ILC-I-01, ILC-I-04). Discards only when both are proven from evidence: the snapshot
  being replaced failed a byte-only check (rule 2) and its proof is complete, so it can never pass; and the median
  time past of the eleven authenticated, linked headers ending five below the tip is later than declared + delta, so
  every new anchor fails row 13.7 (Bitcoin consensus: a block's time exceeds the median of its eleven predecessors,
  which never decreases). It is evaluated where the failure is found (finalization) and again before every recapture
  (the snapshot stage), so captures that keep being rejected cannot hold the attempt once it is proven. Elapsed time
  never discards. Assumption, as in the V1 contract: **no reorganisation of 6 or more blocks** (A1.6); it also
  underlies the header checkpoints.
- **Limits awaiting the author's termination decision (outside the step-5 gate).** These are disclosed limits, NOT
  satisfied obligations: each can keep a request open indefinitely, which leaves A2.3's termination obligation
  (`phase-0-prereg-amendment-2.md:288`) unmet in that case. Disclosure discharges nothing; an author decision (or an
  owner rule within registered text) is needed if they must end. From Codex's round-2 table E
  (`docs/reviews/issuer-lifecycle-impl/CODEX-CONFIRM-2.md`):

  | Path | Kind |
  |---|---|
  | A stage repeatedly needs more requests than one invocation admits before its durable completion (a very slow store or dependency; the measured envelope is below) | stated slow-store limit (a progress limitation; overrun is a tolerated hard kill, below) |
  | Snapshot recapture where impossibility cannot be proved: pending snapshot proof, unobtainable median-time-past headers, or insufficient chain progress | stated limit (absence of an impossibility proof never authorizes a discard) |
  | A latched attempt's snapshot proof never becomes usable; a preserved presentation or assembly object permanently missing | stated external-evidence / storage limit |
  | Unrepaired catalog or trust configuration (including configuration-dependent 13.5 outcomes), verifier unavailability, or persistent header / presentation disagreement | stated operator / dependency limit (no age-based ending is authorized) |
  | Persistent store or queue failures, failed guarded commits, or stage exceptions before a terminal write | operational limitation (no general termination guarantee; signing closure cannot complete a transition whose reads or writes stay unavailable) |
  | The chain never reaches the git pre-commitment depth, or no calendar ever accepts a stamp | dependency limit before evidence processing |

- **Presentation** (ILI-01, ILI-06). The latched presentation keeps only branches at the selected height whose
  attested message is that block's merkle root; contradicted branches there are dropped (counted in the latch as
  `contradicted_pruned`) and the pruned presentation is re-checked contradiction-free. Complete evidence in which every
  attestation is contradicted ends the attempt `EVIDENCE_CONTRADICTED` (discarded at or before B, expired after);
  incomplete or non-qualifying evidence stays open (ILI-03).
- **Signing closure** (ILI-04). Durable signatures (stored and logged "used") are reconciled before closure is
  decided; a complete recovered set is sealed whatever the window.
- **Content** (ILI-08). Content is checked before attempt 1 is allocated (`FAILED CONTENT_UNAVAILABLE`, no attempt).
  After allocation, lost content is recovered from an earlier attempt's attestation frame (it carries the bytes);
  if none decodes to the content digest, no attempt can ever be built, and the ending write discards the attempt and
  refuses the request `REFUSED CONTENT_UNAVAILABLE` (end-and-refuse, like `SIGNING_CLOSED`).
- **Invocation budget: a PROGRESS mechanism, not a bound** (ILI-05, ILC-I-02, ILC-I2-01; owner decision: the earlier
  "never overrun" claim is withdrawn). One deadline (`tessera_issue/deadline.py`), measured on a monotonic clock,
  admits every request the poller makes: DynamoDB, S3 (including the body read of `get_object`, inside the same guarded
  request) and SQS and SNS through `GuardedClient` around each SDK client; calendars, explorers and the resolver through
  `guarded_transport`; the pre-ship check directly. A request starts only if its configured worst case fits the time
  left minus a 10 s reserve, and the HTTP and DNS transports are given a timeout capped to what remains. Worst cases
  count the configured explorers and the SDK's retry attempts (`attempts x (connect + read) + back-off` = 73 s). Its
  purpose is that every invocation leaves durable progress: headers are checkpointed per height and as linked
  segments, a stale stored set is invalidated durably (ILC-I-03), the evidence already held is evaluated before any
  pending calendar is asked (ILC-I-05), calendar requests stop while one checkpoint write still fits (ILC-I2-03),
  requests are enumerated in bounded pages from a durable position moved before each request (ILC-I2-04), and draining
  signer responses has a cooperative allocation of a third of an invocation (ILC-I2-04, ILC-I3-02). It drains OLDEST
  FIRST (ILC-I6, ILC-I7, owner decisions): a round receives a batch from a slot, then from the next slot only while
  that receive PLUS one message's complete worst-case handling (every guarded request of the handling, and the
  acknowledgement, from the adapters' worst cases) still fit; it then handles the received messages across slots in
  order of their SQS `SentTimestamp` (equal times interleave the slots), the oldest always first. A message left
  unhandled becomes visible again and grows older. The slot received from first is chosen at random each round;
  with the AWS adapters' worst cases the rule admits one receive per round. **Handling is resumable per guarded call, and every completed step is observable** (ILC-I8, ILC-I9,
  owner decisions): a signer response's handling is index lookup and record read; frame read and verification, THEN
  the signature object under its digest-named key (only verified signatures are written there, so its existence
  means "verified"); the "used" log entry; the guarded record update; the acknowledgement, last. Each step is
  idempotent and durable, and a later delivery skips every completed step and never repeats it: a record that already
  holds the signature leaves only the acknowledgement; on a redelivery (SQS `ApproximateReceiveCount` > 1) the used
  log is read first (logged: go to the record update) and then the verified object is checked (present: go to the log
  write, without reading the frame or writing the object again). Request servicing's `_reconcile` adopts a stored
  (verified) signature, logging it first if its entry is missing. **The capacity condition, in admission terms:**
  every AWS request is admitted only if its configured worst case, 73 s (3 attempts x (3 s connect + 8 s read) + 2 x
  20 s back-off), fits the time left. Each poll advances at least one incomplete step of a waiting response provided
  the budget fits the receive, the reads that locate the next incomplete step (index lookup, record read, and on a
  redelivery the used-log read and the verified-object check; for the signature step, the frame read it verifies
  against), and ONE guarded call's admission (73 s of headroom) for that step. Actual latency and admission headroom
  are different quantities: a call whose actual latency is far below 73 s is still refused when less than 73 s
  remains. Draining is starvation-free with probability 1 provided that condition holds; below it, progress waits
  for faster dependencies (the stated capacity limit). The share is checked between
  messages, never before a round's oldest one, without reserving a message's remaining cost, so one slow message can
  overrun it; it is not a total-time claim. Removed earlier: the schedule-derived starting slot, the per-slot shares,
  and the durable rotation. Running out of time never ends an attempt.
  **An overrun is a hard kill, and the protocol tolerates it:** the fence, the guarded writes and the checkpoints make
  a killed invocation's leftovers harmless. **Known limits on the deadline's precision** (not chased): the HTTP
  transport's socket timeout applies per blocking operation, so a server dripping bytes can exceed the request's
  total; a DNS query is a composite of UDP and TCP operations, each with its own allowance, and hostname resolution is
  not covered; an SDK request's connect and read timeouts are not a total-operation deadline (streamed bodies); the
  pre-ship check is local CPU with a 30 s admission estimate and no interruption. Measured progress envelope (tests):
  with any one client slow, every invocation stays within its deadline in the tests' fakes, and a request still
  completes with every DynamoDB request taking 20 s, every S3 request 10 s, every SQS or SNS request 60 s, every
  calendar, explorer or resolver request 15 s, or a 25 s pre-ship check; at DynamoDB 30 s or S3 20 s per request a
  stage can need more requests than one invocation admits and the request stalls (listed above).
- **Snapshot capture does not gate the receipt** (ILC-I2-05). Stamping moves the attempt to evidence whether or not
  the DNSSEC snapshot capture succeeded; capture is retried in each evidence poll (early, since its anchor must be
  timely) and, if the attempt latches without one, before finalization (stage `snapshot`). A receipt's latch or
  conclusive negative is never held up by the snapshot. If no snapshot was ever captured and the median-time-past
  bound excludes every timely anchor, the attempt is discarded `SNAPSHOT_IMPOSSIBLE` (`NO_SNAPSHOT`).
- **13.5 by reason** (ILC-I2-02). `RRSIG_NOT_VALID_AT_EVAL_TIME`, `RRSIG_INTERVAL_REVERSED` and
  `RRSIG_TIME_AMBIGUOUS` depend on the snapshot's own RRSIG times against its anchored time: a recapture can repair
  them (and they count for the impossibility proof). Every other 13.5 outcome (configured KSK intervals, reliance
  periods, trust horizon, and conservatively the chain of trust built on them) is configuration-dependent and retried.
- **Bounded external fields** (ILI-07). Signer request ids, statuses and reasons are validated; an unrecognised or
  oversized reason becomes `UNRECOGNIZED_REASON` and the original is stored by reference (`diag-<sha256>`, with its
  digest and length). The DynamoDB fake rejects items over 400 KiB.
- **GATED.** `EVIDENCE_UNAVAILABLE` is not implemented in any form. An attempt whose evidence never completes stays
  open. `unavailable_since` and `failed_intervals` (runs of `fetch_start // 600`) are written for diagnosis only.
  Nothing here claims termination.
- **Storage.** No age rule applies to live objects: the S3 lifecycle rule expires only objects tagged `cleanup-due`,
  which the cleanup obligation sets just before deleting (content, work and frames at the end; the receipt 30 days
  after `ended_at`).
- **Public view.** ACCEPTED shows `attempt` {number, of, state} and, for an open attempt, `expiry_boundary` (B) with a
  note that the twelve-day budget is nominal; REFUSED lists each attempt's outcome and reason.
