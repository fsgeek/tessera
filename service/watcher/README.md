# Detection watcher (the Arariwa, V1)

The independent watcher of `docs/V1-DETECTION-CONTRACT.md`, item 0: (b) a separate Lambda, under its own role,
every 10 minutes, and (a) the trace records it writes. **Built, not deployed.** Nothing below has been seen to fire on
the deployment; the tests here are the owner's unit tests over fakes. The gate's detection tests (item 3) are written
later by another model family.

- `tessera_watch/watcher.py`: one run (order, cursor, D5, D6, D8, trace records).
- `tessera_watch/cloudtrail.py`: listing and parsing the trail's gzipped log files; event classification.
- `tessera_watch/receipts.py`: D8, the relying-party check (as `docs/smoke/2026-11-16-first-receipt/rp_verify.py`).
- `tessera_watch/stores.py`: read-only issuer adapters; the watcher's own state, trace, topic and heartbeat.
- `tessera_watch/lambda_app.py`: handler, `from_env`, `{"watcher": "install-facts"}`.
- `package.py`: deterministic Lambda zip (as `service/issuer/package.py`); prints its SHA-256.
- Infra: `service/detect/infra/watcher.tf` (role, Lambda, schedule, state and trace buckets, D9 alarm).
- Tests: `.venv/bin/python -m pytest -q` with `PYTHONPATH=.:../verifier:tests` (`uv venv`, then `cryptography==50.0.2`
  and `pytest`); `test_d8.py` runs the frozen verifier's CLI on the real first receipt, with the bundle's own headers as
  a faked explorer, and needs a built verifier (`service/verifier/install.sh`).

## What it detects

| Id | What the watcher does | Fires within (event to email) |
|---|---|---|
| D5 | Every new `SIGLOG#` item: disposition `unrequested`, `malformed` or `bad-signature`; reason `KEY_FP_MISMATCH`, `FRAME_DIGEST_MISMATCH`, `ALG_NOT_ALLOWED`, `DECLARED_TIME_OUTSIDE_EPSILON`, `BAD_REQUEST`, `TRUNCATED`, `UNRECOGNIZED_REASON`. | Until the poller logs the response (≤ 10 min, one poll) plus one watcher interval (≤ 10 min): about 20 min. |
| D6 | Every `kms:Sign` on the v1 key in the trail, against the kms signatures in `SIGLOG#` (see the rule below). Alarms: a Sign that no signature accounts for; a signature with no Sign; a Sign by any principal other than the signer role; any `AccessDenied` on the key. | A foreign Sign or `AccessDenied`: CloudTrail delivery *(platform; typically within 15 min)* plus ≤ 10 min. An unmatched Sign: 40 min match window plus ≤ 10 min, so ≤ 50 min if the trail delivered it within the window. A signature with no Sign: 45 min plus ≤ 10 min. |
| D7 (IAM) | Any event with `eventSource` `iam.amazonaws.com` and `readOnly` false, including attempts that failed. All regions' files are read; global IAM events land in the us-east-1 files of the multi-region trail. | CloudTrail delivery *(platform)* plus ≤ 10 min: about 25 min typically, up to ~1 h as the contract states. |
| D8 | Each newly COMPLETE request: the stored bytes at `result/<rid>/<receipt_sha256>.json` must hash to `receipt_sha256`, and the frozen verifier must answer `VALID_STRICT`. Anything else alarms, including a missing object. | ≤ 10 min after the COMPLETE commit, plus seconds for the check. |
| D9 | A heartbeat metric (`Tessera/Watcher` `Heartbeat`) after every *committed* run; a CloudWatch alarm on 30 min without one (missing data is breaching). | ≤ 40 min after the last committed run. |

Every finding is published to `tessera-v1-alarms` (subject `Tessera Dn: ... (CODE)`) and written as one JSON log line
(`"event": "finding"`). Its own faults (`W`: a trail file that does not parse, a receipt check that could not be
made) go the same way. One `watch_summary` line ends each run.

**D8, as a relying party.** Trust is built from the packaged `window.json` (the window's entries, not the issuer's
copy in its bucket) plus pins of the bundle's Bitcoin headers fetched from two explorers that must agree. The
verifier runs as a separate process in its explicit TEST mode, with a TEST release signed by a fresh P-256 key made for
that one check (the production release does not exist; the same as `rp_verify.py`). If the check cannot be made
(explorers down or disagreeing, the verifier refusing to start), it is not a verdict: a `W` finding is sent once per
reason and the receipt is retried every run; after 6 h it is reported as D8 `RECEIPT_UNCHECKED` and its trace record
says `UNCHECKED`. The bootstrap package has no verifier install record, so every check is refused (and reported)
until it is rebuilt with `--install-json`.

**D6, the reconciliation rule.** CloudTrail records a `kms:Sign` with the key, algorithm and caller, but not the
message or the signature, so matching is by time and count only. A kms signature is one distinct `signature_sha256`
in `SIGLOG#` with status `SIGNED`, excluding `unrequested`, `malformed` and `bad-signature` (repeats of one signature,
such as `used` then `superseded:...`, or a redelivered `duplicate`, are one signature; a resend that produced a new
signature is another). In order of when the issuer first logged them, each signature takes the earliest unmatched
signer-role Sign in `[logged − 40 min, logged + 2 min]`. A Sign by another principal is alarmed and never matched. The
Sign event id attributed to a signature in a trace record follows this rule; it is not evidence of which signature the
Sign produced.

Faults that also raise D6 (by design: a Sign no job accounts for): the KMS signer withholding a signature made after
the signing stop (`service/signer-kms/README.md`, "What it assumes"); a signer redelivery after a Sign whose
response was not sent (the next delivery signs again); the poller not draining responses for more than 40 min.

## Trace records (item 0(a))

One JSON object per request that reached COMPLETE, REFUSED or FAILED, at `trace/<rid>.json` in the watcher's own
bucket, Object Lock COMPLIANCE until the window's not-after plus 400 days (`2028-03-07T00:00:00Z` for the current
window; computed in Terraform from `service/issuer/config/window.json`, variable `trace_retention_days_after_window`;
the bucket policy refuses a put without that lock). Written once: an existing record is kept, never replaced.

Fields: credential digest, API key id and client name (from `client_api_key_ids` when the digest matches one; the
issuer's record holds only the digest), request id, SHA-256 of the request key, content SHA-256 and length, state and
reason, created and ended times, each attempt with its jobs (slot, signer request id, frame SHA-256, signature
SHA-256) and, for kms jobs, every signature logged for that signer request id with its attributed Sign event id
(`matched`, `unmatched`, `before-coverage`), receipt SHA-256, anchor heights and T, and the verification verdict.
Never request content, the plaintext request key, an API key value, a URL. A record waits for its kms signatures to
be matched or declared unmatched (at most 85 min after the watcher first sees the request ended).

## The cursor, and why a run never skips

The state is one JSON object in the watcher's own state bucket, written with S3 conditional puts (If-Match on the
ETag read; If-None-Match for the first), and the Lambda has reserved concurrency 1. A run publishes its findings,
then commits the state, then sends the heartbeat. A crash before the commit leaves the old state, so the next run reads
the same trail files and items again: a finding can repeat, never vanish; a trace record is written once. Each
terminal request the run sees is either done or pending in the committed state. The `REQ#` and `SIGLOG#` watermarks
look back 1 h (an item commits seconds after its clock is read). Trail files are read once each, by key, within a 24 h
look-back.

## What it does not detect (stated)

- **Same-account limitation.** The watcher runs in the issuing AWS account. An administrator of that account can stop,
  rewrite or delete it, its buckets' policies (not the locked objects) and its alarms. D7 makes those changes noisy and
  D9 makes silence an alarm, but neither defeats a careful administrator-level attacker. That is the operational-posture
  gate's subject.
- **Slot 2 (GCP `useToSign`)** is not reconciled: **TODO**, waiting for G4 (Cloud KMS Data Access logs). Trace
  records say so per gpg job.
- **Only what the trail and the stores show.** A Sign CloudTrail never delivers is invisible to D6 except as a
  signature without a Sign; a trail file delivered more than 24 h after its key time is never read; a stopped trail is
  D7's EventBridge rule, not the watcher's. The trail's digest files (log file validation) are not checked.
- **Before coverage.** Signatures logged before the watcher's first trail window (its first run minus 24 h) are not
  reconciled (`before-coverage`), so the first production receipt's Signs (2026-11-16) are not matched unless the first
  run is within 24 h of them.
- **Requests that ended before deployment** and whose `REQ#` item has already expired (30 days) get no trace record.
- **D1-D4, D10 and the rest of D7** are not the watcher's: metric filters and EventBridge rules in `service/detect/infra`.
- **The watcher reads the plaintext request key** (a DynamoDB Scan returns the whole `REQ#` item) to hash it; it never
  writes or logs it. Its role cannot be narrowed to exclude it without an issuer change.

## Deploy (not done)

`service/detect/infra` gains required variables `watcher_zip`, `results_bucket` (the issuer's `result_bucket`
output) and `trail_bucket` (`service/signer-kms` output); `client_api_key_ids` comes from the issuer's output of that
name; `runtime_version_arn` as for the issuer. Bootstrap: `python package.py OUT.zip`, apply, invoke with
`{"watcher": "install-facts"}`, save the answer, rebuild with `--install-json`, apply with `runtime_version_arn` set.
Then confirm the first `watch_summary` line and the heartbeat. Record each zip's SHA-256.
