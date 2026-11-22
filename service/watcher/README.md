# Detection watcher (the Arariwa, V1)

The independent watcher of `docs/V1-DETECTION-CONTRACT.md`, item 0: (b) a separate Lambda, under its own role,
every 10 minutes, and (a) the trace records it writes. **Built, not deployed.** Nothing below has been seen to fire on
the deployment; the tests here are the owner's unit tests over fakes. The gate's detection tests (item 3) are written
later by another model family.

- `tessera_watch/watcher.py`: one run (order, cursor, D5, D6, D8, trace records).
- `tessera_watch/cloudtrail.py`: listing and parsing the trail's gzipped log files; event classification.
- `tessera_watch/receipts.py`: D8, the relying-party check (as `docs/smoke/2026-11-16-first-receipt/rp_verify.py`).
- `tessera_watch/stores.py`: read-only issuer adapters; the watcher's own state, finding outbox, trace, topic and
  heartbeat.
- `tessera_watch/sanitize.py`: the per-field validators every output passes (or the value is `<withheld>`).
- `tessera_watch/lambda_app.py`: handler, `from_env`, `{"watcher": "install-facts"}`.
- `package.py`: deterministic Lambda zip (as `service/issuer/package.py`), wheels from `requirements-lambda.txt`
  (every artifact hash-pinned); prints its SHA-256.
- Infra: `service/detect/infra/watcher.tf` (role, Lambda, schedule, state and trace buckets, D9 alarm).
- Tests: `.venv/bin/python -m pytest -q` with `PYTHONPATH=.:../verifier:tests` (`uv venv`, then `cryptography==50.0.2`
  and `pytest`); `test_d8.py` runs the frozen verifier's CLI on the real first receipt, with the bundle's own headers as
  a faked explorer, and needs a built verifier (`service/verifier/install.sh`).

## What it detects

| Id | What the watcher does | Fires within (event to email) |
|---|---|---|
| D5 | Every new `SIGLOG#` item: disposition `unrequested`, `malformed` or `bad-signature`; reason `KEY_FP_MISMATCH`, `FRAME_DIGEST_MISMATCH`, `ALG_NOT_ALLOWED`, `DECLARED_TIME_OUTSIDE_EPSILON`, `BAD_REQUEST`, `TRUNCATED`, `UNRECOGNIZED_REASON` or a verifier codec fault code. Only what reaches `SIGLOG#`: a KMS signer startup `KeyMismatch` (no response is sent) is the Lambda `Errors` alarm's; a refusal logged only by a signer, and a GCP `refuse_to_run` with no response, are outside the watcher (the GCP log-based alert is not built). | Until the poller logs the response (≤ 10 min, one poll) plus one watcher interval (≤ 10 min): about 20 min. |
| D6 | Every `kms:Sign` on the v1 key in the issuing account's trail, against the kms signatures the issuer **verified and used** (see the rule below). Alarms: a Sign that no such signature accounts for; a used signature with no Sign; a Sign by any principal other than the signer role; any `AccessDenied` on the key recorded in this account's trail (one made from another AWS account is logged only in that account and is not seen); a job signature never logged in `SIGLOG#`. | A foreign Sign or `AccessDenied`: CloudTrail delivery *(platform; typically within 15 min)* plus ≤ 10 min. An unmatched Sign: 45 min after it plus ≤ 10 min, so ≤ 55 min if the trail delivered it within 45 min and the watcher read it by then. A used signature with no Sign: 47 min after it was logged plus ≤ 10 min. Both only from a complete run (below); a run that is not finalizes nothing and sends no heartbeat. |
| D7 (IAM) | Any event with `eventSource` `iam.amazonaws.com` and `readOnly` false, including attempts that failed. All regions' files are read; global IAM events land in the us-east-1 files of the multi-region trail. | CloudTrail delivery *(platform)* plus ≤ 10 min: about 25 min typically, up to ~1 h as the contract states. |
| D8 | Each newly COMPLETE request: the stored bytes at `result/<rid>/<receipt_sha256>.json` must hash to `receipt_sha256`, the frozen verifier must answer `VALID_STRICT`, and the receipt must be this request's: its attested content's SHA-256 and length, its four signatures' SHA-256, A_sig's SHA-256 and its declared issue time must equal the record's (content, the shipped attempt's jobs, `receipt_id`, `declared_issue_time`), each compared only where the record holds it: with no shipped attempt, or a job without a signature digest, a receipt of another request for the same content passes. Anything else alarms, including a missing object (404) and an object that cannot be read (any other error, reported with its class name). | ≤ 10 min after the COMPLETE commit, plus the check (bounded by what is left of the invocation), when the backlog is under 10 receipts a run. A check that cannot be made, or a receipt deferred behind a backlog, is reported `RECEIPT_UNCHECKED` after at most 6 h; an object that stays unreadable is reported `RECEIPT_OBJECT_UNREADABLE` once and traced `NO_RECEIPT`/`OBJECT_UNREADABLE` after 6 h. |
| D9 | A heartbeat metric (`Tessera/Watcher` `Heartbeat`) after every committed, sound run; the alarm fills each empty 10-minute period with 0 (`FILL`) and fires on three consecutive periods without one. | 30 to 40 min after the last heartbeat, plus CloudWatch's evaluation delay *(platform; typically a minute or two)*, when metrics are ingested on time; a beat ingested late can be evaluated as 0. |

Every finding is written to the watcher's outbox (`findings/` in its state bucket) and as one JSON log line (`"event":
"finding"`) the moment it is found, then published to `tessera-v1-alarms` (subject `Tessera Dn: ... (CODE)`) and deleted
from the outbox only once SNS has accepted it. A finding whose publication fails stays in the outbox and is published by
a later run; that run withholds the heartbeat. A finding that can be neither written to the outbox nor published stops
the run before its commit (`WATCHER_ERROR`, no heartbeat), so the next run reads the same sources and finds it again; it
is lost if its source is gone by then (a `REQ#` item that expired, an object deleted), including after a run that dies
between a failed outbox write and its end. The `WATCHER_ERROR` of a failed run is published directly, best effort, not
queued. The guarantee ends at SNS accepting the message: email to the author needs the confirmed subscription (contract
Status: pending). Its own faults (`W`: a trail file or receipt check that could not be read or made, an issuer record
that is inconsistent, a source that could not be read) go the same way. One `watch_summary` line ends each run.

**Failure isolation.** A failure while checking one trail file, one `SIGLOG#` entry, one request or one trace write
is a `W` finding (the item's id or rid prefix and the exception's class name, never its text); the run goes on,
publishes and commits, and the item is retried next run (a trail record whose classification raises is reported and not
retried; its file is marked read). A request or trace failure leaves the heartbeat. A failed trail file, trail record or
`SIGLOG#` entry, or a trail file left unread for lack of time, makes the run incomplete: it finalizes no D6 outcome
and withholds the heartbeat, so a failure that persists (an entry that always fails, a backlog of trail files after
an outage) is D9's. A failure of a whole source (the table scan, the
trail listing, the outbox listing) is a `W` finding and withholds the heartbeat, as does a failed publication or a
failing verifier self-check (below): the watcher is then blind or mute in part, so D9 fires if it persists. Any other
failure (the state cannot be loaded or committed) ends the run: the handler logs the class name, publishes
`WATCHER_ERROR` with the class name, sends no heartbeat and returns without raising.

**D8, as a relying party.** Trust is built from the packaged `window.json` (the window's entries, not the issuer's
copy in its bucket) plus pins of the bundle's Bitcoin headers fetched from two explorers that must agree. The
verifier runs as a separate process in its explicit TEST mode, with a TEST release signed by a fresh P-256 key made for
that one check (the production release does not exist; the same as `rp_verify.py`). One check has one deadline (what
is left of the invocation less 90 s, at most 360 s), shared by every explorer request and the verifier process. It
starts after the S3 read and hashing of the receipt, and explorer timeouts bound each socket wait, not a whole
response, so a slow S3 read or a slowly delivered explorer response can overrun the invocation (a Lambda timeout: the
`Errors` alarm, no commit, retried next run); a
bundle with more than 32 header heights is reported `RECEIPT_UNCHECKED` at once, without explorer calls. At most 10
checks run per invocation, least recently tried first; the rest carry over. If the check cannot be made (explorers
down or disagreeing, the verifier refusing to start, the deadline), it is not a verdict: a `W` finding is sent once per
reason and the receipt is retried every run; after 6 h it is reported as D8 `RECEIPT_UNCHECKED` and its trace record
says `UNCHECKED`. Every run also performs the verifier's own startup check against the packaged install record; if it
fails (the bootstrap package, or a record sampled on another runtime), `VERIFIER_SELF_CHECK_FAILED` is reported once
and the heartbeat is withheld until the package is rebuilt.

**D6, the reconciliation rule.** CloudTrail records a `kms:Sign` with the key, algorithm and caller, but not the
message or the signature, so matching is by time and count only. What is reconciled is kms:Sign events against
signatures the issuer verified and used: one distinct `signature_sha256` with at least one `SIGLOG#` entry with slot
`kms`, status `SIGNED` and disposition `used`, and no entry for it timed more than 5 min ahead of the watcher's clock.
A signature recorded on a kms job of a `REQ#` record does not count by itself (the issuer logs `used` before it records
the job), so a deleted `used` entry leaves its Sign unmatched even while the job and other rows of that digest remain.
A `duplicate`, `not-waiting`, `other-attempt`, `unrequested`, `malformed` or `bad-signature` response never makes a
signature count (a `duplicate` is logged before its signature is verified). A used signature of an attempt that did
not ship counts; its trace record says so. A counted signature's time is the earliest time of any of its `SIGLOG#` kms
`SIGNED` entries other than `unrequested`, `malformed` and `bad-signature` (an earlier `duplicate` or unused row of
the same digest included), taken until its match is final. In that order, each counted signature takes the earliest
free signer-role Sign in `[time − 40 min, time + 2 min]`. The matching is recomputed every complete run over everything
not yet final, so a Sign the trail delivers late still takes its place in the order (and the Sign a non-final
signature takes can change); a signature's match becomes final 47 min after its time (2 min skew plus the 45 min
bound), and a Sign with no signature is declared unmatched 45 min after its time. The 45 min bound covers CloudTrail's
delivery and the watcher's reading together: a Sign not yet read when the signature's match becomes final does not
take it. Outcomes become final only in a complete run (the trail listed and every file in reach read, the scan and
every `SIGLOG#` entry read); otherwise nothing becomes final until the next complete run. A Sign by another principal
is alarmed and never matched. The Sign event id attributed to a signature in a trace record follows this
rule; it is not evidence of which signature the Sign produced, and the signer-role attribution identifies the KMS
caller, not who submitted the work (anything that can write the KMS request queue can cause a Sign).

Faults that also raise D6 (by design: a Sign no used signature accounts for): the KMS signer withholding a signature
made after the signing stop (`service/signer-kms/README.md`, "What it assumes"); a signer redelivery after a Sign whose
response was not sent, or whose response the issuer logged as a duplicate (the next delivery signs again); the poller
not draining responses for more than 40 min; a Sign delivered by CloudTrail more than 45 min late after its slot in the
order was finalized, or read by the watcher only after that (then reported, possibly twice).

## Trace records (item 0(a))

One JSON object per request that reached COMPLETE, REFUSED or FAILED, at `trace/<rid>.json` in the watcher's own
bucket, Object Lock COMPLIANCE until the window's not-after plus 400 days (`2028-03-07T00:00:00Z` for the current
window). The date is computed by the watcher from the `window.json` packaged in its zip and the constant 400
(`lambda_app.TRACE_RETENTION_DAYS`), and by Terraform from the same record and the same constant
(`local.trace_retention_days`); neither is a deploy input, so a later deploy cannot move it. The bucket's default
retention is COMPLIANCE, 400 days, for anything put without a date; versioning is on. The bucket policy refuses a put
without a lock mode, without a retain-until date, or with a date before the floor; a put by any principal but the
watcher role; and, to every principal, a delete (so no delete marker can hide the current key), a version delete and a
change of the lock configuration. Written once per terminal request, retried every run until written: an existing
record is kept, never replaced. The watcher's role holds `s3:PutObjectRetention` on `trace/*`, which S3 requires for
a put that sets a retain-until date. **Residual:** an administrator of the account can first rewrite the bucket policy
(`PutBucketPolicy`, a D7 event) and then place a delete marker or a second version under the key; the first version
stays locked and readable by version id.

Fields: credential digest, API key id and client name (from `client_api_key_ids` when the digest matches one; the
issuer's record holds only the digest), request id, SHA-256 of the request key, content SHA-256 and length, state and
reason (a sub-code such as `SIGNER_REFUSED:KEY_FP_MISMATCH` is split into `reason` and `reason_detail`), created and
ended times, each attempt (id, state, declared issue time, `receipt_id`, end) with its jobs (slot, signer request id,
frame SHA-256, signature SHA-256) and, for kms jobs, every kms signature logged for that signer request id with its
reconciliation (`matched` with the attributed Sign event id, `unmatched`, `before-coverage`, `not-counted` for one the
issuer did not use, `not-logged` for a job signature never in `SIGLOG#`), receipt SHA-256, the verification (verdict,
reason, binding `match`/`mismatch`/`unreadable`), and anchor heights and T only for a receipt bound to this request. A
receipt that verifies but is another request's is recorded as `NOT_BOUND` with the fields that differ, never with its
anchors. Every value passes its field's validator or is `<withheld>`: never request content, the plaintext request key,
an API key value, a URL. The record is written from a validated snapshot taken when the watcher first sees the request
terminal; a later change to the `REQ#` item is not traced. `record_source` is `snapshot` when the `REQ#` item expired
before the record could be written. A record waits for its kms signatures to be final, and for a job signature to appear
in `SIGLOG#` (at most 30 min), at most 67 min after the watcher first sees the request ended; after that it is written
as it stands, so a signature can show `pending` (for example while runs are incomplete). Signatures are joined to a job
by its signer request id: a job signature whose digest is in `SIGLOG#` only under another signer request id is shown
neither as matched nor as `not-logged`.

## The cursors, and what a run can miss

The state is one JSON object in the watcher's own state bucket, written with S3 conditional puts (If-Match on the
ETag read; If-None-Match for the first, which the first run makes before reading anything, so its coverage start
survives a crash), and the Lambda has reserved concurrency 1. The bucket policy refuses writes to it by any principal
but the watcher role. A run writes each finding to the outbox when found, publishes, commits the state, then sends
the heartbeat. A crash before the commit leaves the old state, so the next run reads the same trail files and items
again: a finding can repeat, and one already in the outbox is published even if its cause has gone.

No cursor moves by an issuer-supplied time. A `REQ#` or `SIGLOG#` item is new while its key is not in the watcher's
seen set, and a key leaves the seen set only when its item is no longer in the scan (every run scans the whole table,
strongly consistent); an issuer time more than 5 min ahead of the watcher's clock is a `W` finding
(`ISSUER_TIME_IN_FUTURE`) and such a signature never counts for D6. Trail files are read once each, by key, from the
trail cursor: the watcher's own clock minus 1 h at its last commit, held back to the oldest file it has not yet read
(a file that keeps failing is retried until 24 h after its key time, then reported `TRAIL_FILE_ABANDONED`; so a file
first read after a longer outage is abandoned on its first error). Keys are read in key-time order across regions, so
a run that runs out of time leaves the cursor at or before every file it did not reach. An outage of any length loses
no file that can be read. What can still be missed: a trail file that appears in the bucket more than an hour after
its key timestamp while the cursor has passed it.

## What it does not detect (stated)

- **Same-account limitation.** The watcher runs in the issuing AWS account. An administrator of that account can stop,
  rewrite or delete it, its buckets' policies (not the locked object versions) and its alarms. D7 makes those changes
  noisy and D9 makes silence an alarm, but neither defeats a careful administrator-level attacker. That is the
  operational-posture gate's subject.
- **Resource separation, not observation integrity.** The watcher's role cannot write any issuer store, and no issuer
  role can write the watcher's buckets. That separates resources; it does not make the issuer's records trustworthy.
  `REQ#` and `SIGLOG#` are written by the issuer's own principals, and **a principal able to write the issuer table
  can suppress D5 and D8 for the rows it deletes or alters before the watcher reads them** (and can shape the trace
  record of a row it alters). The independent evidence is CloudTrail: a deleted or never-written `SIGLOG#` `used` entry
  (with no other `used` entry of that digest) still leaves its `kms:Sign`, which surfaces as an unmatched Sign under
  D6. A deleted or altered COMPLETE row whose `used` entries remain is not seen by D6: it suppresses D8 and shapes or
  withholds the trace record. The poller can also write
  `SIGLOG#` `used` entries that account for Signs it caused through the KMS request queue; D6 then sees matching counts.
- **Slot 2 (GCP `useToSign`)** is not reconciled: **TODO**, waiting for G4 (Cloud KMS Data Access logs). Trace
  records say so per gpg job.
- **Only what the trail and the stores show.** A Sign CloudTrail never delivers is invisible to D6 except as a
  signature without a Sign; a stopped trail is D7's EventBridge rule, not the watcher's. The trail's digest files (log
  file validation) are not checked.
- **Before coverage.** Signatures logged before the watcher's first trail window (its first run minus 24 h) are not
  alarmed: one with no Sign is recorded `before-coverage` (so the first production receipt's Signs, 2026-11-16, are not
  matched unless the first run is within 24 h of them). Such a signature still takes part in the matching, so it can
  take a Sign just after the boundary (within its +2 min) that is then not reported unmatched. A signature logged after
  coverage starts whose Sign fell just before it alarms (a possible false alarm at bootstrap only).
- **Requests that ended before deployment** and whose `REQ#` item has already expired (30 days) get no trace record.
- **D9 measures sustained silence.** Intermittent timeouts or throttles between sound runs do not fire it; errors and
  timeouts are the Lambda `Errors` alarm's (D10; the handler never raises, so only timeouts and runtime faults count
  there). A run failure the handler catches counts in neither: if its best-effort `WATCHER_ERROR` publish also fails
  and the runs around it heartbeat, that failed invocation is not signalled. A disabled schedule fires D9.
- **The secrecy boundary is by shape.** A value that matches its field's rule passes whatever its origin: an
  uppercase or alphanumeric secret written into a `SIGLOG#` reason (code shape) reaches the log, SNS, the outbox and
  the trace; a secret shaped like a digest, a UUID, an id or a role ARN passes those fields, from the issuer's records
  or from CloudTrail. The state (not the findings) holds full trail S3 keys, so a key with text before a valid
  CloudTrail file name is persisted there. A verifier `Unavailable` code, or a code-shaped first token on the verifier
  CLI's stderr, is kept in the pending state and sent as a finding's reason (and, after 6 h, traced); the verifier's
  verdict, reason and T are kept in the pending state before the trace's validation. A failure while the handler
  module is imported (before the handler can catch it, e.g. a verifier dependency failing to load) reaches the Lambda
  runtime log with its text. An outbox entry is revalidated on the way out; fields without a rule are dropped.
- **D1-D4 (not built yet), D10 and the rest of D7** are not the watcher's: metric filters and EventBridge rules in
  `service/detect/infra`.
- **The watcher reads the plaintext request key** (a DynamoDB Scan returns the whole `REQ#` item) to hash it; it never
  writes or logs it. Its role cannot be narrowed to exclude it without an issuer change.

## Deploy (not done)

`service/detect/infra` gains required variables `watcher_zip`, `results_bucket` (the issuer's `result_bucket`
output) and `trail_bucket` (`service/signer-kms` output); `client_api_key_ids` comes from the issuer's output of that
name. Bootstrap: `python package.py OUT.zip`, apply (until the deployable package is applied the self-check fails, so
`VERIFIER_SELF_CHECK_FAILED` is sent once and D9 fires), invoke with `{"watcher": "install-facts"}` and save the answer,
read the runtime the facts were sampled on (`aws lambda get-function-configuration --function-name tessera-v1-watcher
--query RuntimeVersionConfig.RuntimeVersionArn --output text`, as `service/issuer/DEPLOY.md` step 3), rebuild with
`--install-json`, apply with `runtime_version_arn` set to that ARN. Then confirm the first `watch_summary` line with
`"heartbeat": true`, and the heartbeat alarm's OK. Record each zip's SHA-256.
