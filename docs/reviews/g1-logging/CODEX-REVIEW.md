# G1 logging review — findings

Reviewed `a874852` as merged in `c6d86eb`; the reviewed files are unchanged at the current HEAD. The detection contract is a steward draft, not a registered amendment or proof that an alarm fires.

## Findings

### P1 — Poller notes disclose arbitrary exception text

`service/issuer/tessera_issue/pipeline.py:231` and `:461` pass exceptions from stores and signer adapters into `Issuer.note`; `service/issuer/tessera_issue/service.py:54-57` emits their string representation. The same occurs for cleanup and snapshot failures (`pipeline.py:309`, `:381`, `:823`). An AWS or HTTP exception containing a pre-signed URL, credentials, request content, or a content-addressed object key can therefore put those bytes in CloudWatch. Truncating at 500 characters is not redaction: a secret near the beginning survives. This contradicts `service/issuer/LOGGING.md:3-6`. The successful-content test at `tests/test_logging.py:68-74` does not inject an exception carrying a secret.

### P1 — Synchronous logging can change deadline-sensitive execution

`service/issuer/tessera_issue/logs.py:15-17` serializes, writes, and flushes synchronously without a time bound. Calls occur after a fence or other guarded write (`pipeline.py:257-261`), between durable SIGLOG and recording the signature (`pipeline.py:553-566`), before SQS acknowledgment (`pipeline.py:454-456`), and before an API response or exception is returned (`lambda_app.py:91-97`). A slow or blocked stdout can consume the poll budget or Lambda timeout after a fence or SIGLOG write, preventing subsequent work or acknowledgment; it can also delay or prevent an API response. The deadline's adapter worst-case calculation (`pipeline.py:395-404`) does not account for logging. Catching exceptions cannot bound a call that does not return. `test_logging.py:105-119` injects immediate serialization failure, not a slow write or flush.

### P2 — Logging can replace an exception or abort processing

`logs.py:18` catches `Exception`, not `BaseException`. For example, if stdout raises `SystemExit` while the API wrapper is reporting an existing `RuntimeError`, `_api_log` also catches only `Exception` (`lambda_app.py:68-80`), so the logging exception replaces the original instead of the bare re-raise at `:94`. In `poll` the same failure in the `finally` (`pipeline.py:178-181`) replaces an existing exception or cancels a successful return. A `BaseException` during `_siglog` occurs after the durable write but before signature recording and acknowledgment. This is distinct from ordinary `OSError`, which is swallowed; the failure test never reaches its broken stdout because `json.dumps` is patched to raise first (`test_logging.py:105-115`).

### P2 — Stage lines can omit committed changes and describe failed ones

`pipeline.py:244-254` emits a stage line only when the entire stage function returns normally, comparing its initial and final in-memory values. In `st_frames`, `frames` → `signing` is committed at `:704-708` before signer sends at `:709-712`; if a send raises, the committed stage change has no `request_stage` line. Conversely a failed guarded save raises `Superseded` after mutating the local record (`:257-260`), and `advance` catches it at `:249-250`; `_serve_requests` then reports the mutated local stage in `poll_summary.advanced` at `:224-233`, even though the write lost. A successful `_end_attempt` may commit a new `frames` stage inside response draining (`:526-530`, `:312-330`) without going through `advance` at all. The API's successful `upload` → `frames` save also bypasses it (`api.py:98-103`). Thus neither stage lines nor summaries are a complete or reliable committed-stage history. Guarded lifecycle transitions themselves are emitted from `_commit` after successful saves; a failed guarded write must not emit one.

### P2 — Durable SIGLOG and CloudWatch line are not atomic

`pipeline.py:563-568` writes the item first and only then emits the line. If the process times out or stdout fails after `siglog_add`, the item exists without a corresponding line. In particular, on redelivery a used signature can be found by `siglog_has` and skip `_siglog` (`:541-555`), so that line need not be recovered. Best-effort logging also deliberately swallows ordinary output errors (`logs.py:18-19`), making the unconditional one-line-per-item claim in `LOGGING.md:35` false. D5's planned watcher reads SIGLOG (`docs/V1-DETECTION-CONTRACT.md:60,74`); a CloudWatch metric filter alone cannot be treated as equivalent durable coverage or a demonstrated alarm.

### P2 — Signer-controlled reason is bounded by syntax, not an allowlist

`pipeline.py:128` and `:468-475` accept any uppercase alphanumeric/underscore string of up to 64 characters as a reason, and `_siglog` emits it at `:566-568`. A compromised or faulty signer can put a secret or request content fitting that grammar, for example `SECRET_CONTENT_123`, into `reason`; it appears in the line and can also propagate into an attempt end reason. An unrecognized but syntactically valid reason is not mapped to `UNRECOGNIZED_REASON`, contrary to `LOGGING.md:36-37`; therefore D5's `UNRECOGNIZED_REASON` filter misses it. The known D5 codes themselves pass through, and invalid syntax maps to that code, subject to the delivery gap above.

### P3 — Coverage and metric-filter claims exceed the tests

`test_logging.py:68-96` exercises a normal completion and one unrequested KMS response, not the D5 malformed, bad-signature, each refusal reason, both real signer suites, recovered signatures, superseded results, failed saves, or interruption between SIGLOG and emission. `:60-65` checks an ordinary handler exception only; `:99-102` uses a harmless note; `:105-119` does not exercise stdout write or flush independently. The build explicitly calls for tests across both signer suites (`docs/V1-DETECTION-CONTRACT.md:69-71`). The documented sample filters reference top-level JSON fields that are present in successfully emitted matching lines (`LOGGING.md:8-9`, `pipeline.py:566-568`, `lambda_app.py:72-75`), but no CloudWatch filter or deployed delivery was tested here. D3/D4's per-key and invitation checks require their separately specified access-log and watcher work (`docs/V1-DETECTION-CONTRACT.md:58-59,73`); a `cred` digest alone is not a demonstrated per-key alarm.

## Owner prechecks

1. **Capture row — PASS** for this review's claims: it makes no claim that DNS and git capture rejects or exposes attacker keys. The governing limit is explicit at `docs/V1-CONTRACT.md:35-37,72`; `docs/V1-DETECTION-CONTRACT.md:77-79` excludes that capture.
2. **Trigger clause — PASS** for the authorities used here: D5's listed reasons and dispositions are examined as draft detection targets (`docs/V1-DETECTION-CONTRACT.md:60`), not as an asserted fired alarm; the documented SIGLOG and output failure scenarios state their actual triggers.
3. **Requester — PASS** for this review's scope: no key-storage or signer-custody security conclusion is made. D5 includes responses from work submitted to the signer, and the issuer routes signer responses at `pipeline.py:486-510`; account-level requester capture remains excluded by `docs/V1-DETECTION-CONTRACT.md:77-79`.
4. **Binding text — PASS** for this review's scope: G1/D3-D5 are identified as a draft (`docs/V1-DETECTION-CONTRACT.md:1,69-75`), and `LOGGING.md` is evaluated against its own implementation claims, not presented as a signed requirement. No schedule budget or 24-hour FAILED rule is used as authority.
