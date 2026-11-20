# Issuer application log lines (detection contract gap G1)

Both Lambdas write one JSON object per line to stdout (CloudWatch Logs). Every line has `"event"` and `"v"` (schema
version, currently `1`); fields are only ever added within a version. Lines carry digests, ids, states and reason
codes. They never carry request content, content digests, the request key, the API key or any secret. Logging is
best effort: a logging failure (any `BaseException` raised by logging itself) is swallowed and changes no behaviour or
state; it never replaces an exception in flight or cancels a return (`tessera_issue/logs.py`). Exception text is never
logged, only class names (see `poller_note`). Each line is one `sys.stdout.write`; there is no flush and no thread.

Metric filter examples: `{ $.event = "signer_response" && $.disposition = "unrequested" }`,
`{ $.event = "api" && $.reason = "TOO_LARGE" }`.

## API Lambda: `api` (exactly one per request handled, including requests that raise)

| field | meaning |
|---|---|
| `method`, `route` | HTTP method; API Gateway resource (`/v1/requests`, `/v1/requests/{key}`, `/v1/requests/{key}/receipt`) |
| `status` | HTTP status returned (500 if the handler raised; the exception is re-raised) |
| `reason` | reason or error code of the answer: `TOO_LARGE`, `BAD_REQUEST`, `OUTSIDE_WINDOW`, `CLOSING`, `SIGNING_UNAVAILABLE`, `KEY_CONTENT_MISMATCH`, `UNAUTHENTICATED`, `NOT_FOUND`, `EXCEPTION`; null if none |
| `state` | request state in the answer (`ACCEPTED`, `REFUSED`, `COMPLETE`, `EXPIRED`, ...); null if none |
| `cred` | SHA-256 credential digest (`api.cred_digest`); null if no credential |
| `rid` | request record id (SHA-256 of credential digest and key); null if the key was missing or not a UUID |
| `content_len` | length in bytes of the POST body; null for GET |
| `error` | exception class name (only when `reason` is `EXCEPTION`) |

## Poller Lambda

`request_transition`: one per committed change of a request's state, current attempt, or attempt state, emitted from
`pipeline._commit`.
`rid`, `from_state`, `to_state`, `from_attempt`, `to_attempt` (attempt id such as `a1`; empty before attempt 1),
`from_astate`, `to_astate` (`open`, `latched`, `shipped`, `expired`, `discarded`, or empty), `stage` (stage after the
write, null when ended), `reason` (request refusal/failure reason, or the reason the previous attempt ended; null if
none). Logged after the guarded write succeeds. A failed (superseded) write logs nothing.

`request_stage`: one per committed stage change inside ACCEPTED, emitted from `pipeline._commit` after the guarded save
succeeds, comparing the stage last read or committed with the committed one. A save that fails (superseded) emits
nothing; a committed change is logged even if the stage function raises afterwards. `rid`, `attempt` (number),
`from_stage`, `to_stage`. Not covered: the API's own `upload` -> `frames` save (`api._finish_upload`), which is
visible in its `api` line only.

`signer_response`: one per SIGLOG# item the issuer writes, emitted after the item is durable and best effort: the line
can be missing (a timeout or stdout failure after the write, or a redelivery that finds the SIGLOG# item already
present). The durable record is SIGLOG#, which the planned detection watcher reads (docs/V1-DETECTION-CONTRACT.md D5);
a metric filter on this line is a convenience, not durable coverage. `slot`, `request_id` (signer request id, or
`invalid:<hash>` if the response id was malformed), `status` (`SIGNED`, `REFUSED`, `OTHER`), `reason` (a code from the
known set of both signers' refusal reasons and the issuer's own codes, `pipeline.KNOWN_SIGNER_REASONS`; any other
value, malformed or merely well-formed, is logged and stored as `UNRECOGNIZED_REASON` and the raw value is kept only
as a diagnostic object, never logged; null if none), `disposition` (`used`, `unrequested`, `malformed`,
`bad-signature`, `refused`, `duplicate`, `not-waiting`, `other-attempt`, `superseded:<outcome>`), `frame_sha256`,
`signature_sha256`, `attempt`, `recovered` (true for a reconciled stored signature).

`poll_summary`: one per `poll()` run, including a run that raises. The summary dict: `drained`, `cleaned`,
`advanced` (rid -> [stage before, stage or state after]; "after" is the COMMITTED value, so a lost or failed save leaves
it equal to "before"), `committed` (the number of requests whose committed stage or state changed this run), and when
present `out_of_time`, `deferred`.

`poller_note`: each in-memory note the poller records. `msg` is a fixed message tag plus short safe identifiers (request
id prefix of 12 hex characters, slot, stage) and exception CLASS names. It never contains an exception's text (which
can carry pre-signed URLs, credentials or object keys); the in-memory note list is never emitted or returned.
`msg` is truncated to 200 characters.

## Residuals

- Logging is synchronous and best effort. A blocked stdout pipe blocks the function like any other write; logging adds
  no thread, timeout or flush, and a logging failure is swallowed, not retried.
- The poll budget keeps margin (`POLL_RESERVE_S`), but the deadline guard's worst-case arithmetic does not account for
  time spent in a log write.
- A line can be missing after a durable write (see `signer_response`); SIGLOG# is the record.
