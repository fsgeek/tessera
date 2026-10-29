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
- **States:** ACCEPTED, then COMPLETE, REFUSED or FAILED (24 h after acceptance, with a reason). After 30 days: EXPIRED.
- **Retrieval:** only by the credential that submitted. The response carries the receipt's SHA-256.

## Issuance rules carried from real runs

- **E-01:** the signers are started on demand. No standing scheduler is needed.
- **E-02:**
  - Every request to a signer carries a request id derived from (request key, frame hash).
  - Every response is recorded with the frame hash and signature hash, whether or not it is used.
  - Responses nobody is waiting for are recorded, then deleted.
  - A retry reuses a complete, verified signature set rather than signing again.
- **Ship only complete receipts:** the pre-ship checks of profile §4 and §15.7 run on the assembled bundle with the
  service verifier's own logic, called as a library. A bundle that fails is FAILED, never shipped.
- **Window:** acceptance stops 120 h before not-after, and signing stops at 96 h. A request that cannot complete in
  time is FAILED, not shipped late.

## Tests the builder must provide

1. **Unit tests** for every state transition, including duplicate keys and key/content mismatch.
2. **A local end-to-end test** with stand-in signers and stand-in chain and calendar. It drives a request to COMPLETE
   and verifies the bundle with `service/verifier` (`--mode test`) as `VALID_STRICT`.
3. **Fault tests:** a signer timeout followed by a late answer (E-02); a lost API response, then lookup by key; the
   24 h failure; the stop margin.
4. **Infrastructure as code (Terraform)** that a later step applies to AWS. Nothing is applied by the builder.

## Changes after review

Codex review `docs/reviews/issuer/CODEX-REVIEW.md` (IS-01 to IS-11); dispositions and test names in
`docs/reviews/issuer/DISPOSITION.md`. Only the changes that alter this design are listed here.

- **IS-03 (signer contract):** each policy signer enforces the signing stop itself, immediately before it signs: its
  own configured stop (the window's not-after minus 96 h) and a per-request `sign_by` the issuer now adds to every
  request (the earlier of the signing stop and acceptance + 24 h). Past either, it answers `REFUSED`
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
  rules stay as a 31-day backstop.
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
