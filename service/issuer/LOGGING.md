# Issuer application log lines (detection contract gap G1)

Both Lambdas write one JSON object per line to stdout (CloudWatch Logs). Every line has `"event"` and `"v"` (schema
version, currently `1`); fields are only ever added within a version. Lines carry digests, ids, states and reason
codes. They never carry request content, content digests, the request key, the API key or any secret. Logging is
best effort: a logging failure is swallowed and changes no behaviour or state (`tessera_issue/logs.py`).

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

`request_transition`: one per committed change of a request's state, current attempt, or attempt state.
`rid`, `from_state`, `to_state`, `from_attempt`, `to_attempt` (attempt id such as `a1`; empty before attempt 1),
`from_astate`, `to_astate` (`open`, `latched`, `shipped`, `expired`, `discarded`, or empty), `stage` (stage after the
write, null when ended), `reason` (request refusal/failure reason, or the reason the previous attempt ended; null if
none). Logged after the guarded write succeeds. A failed (superseded) write logs nothing.

`request_stage`: one per stage change inside ACCEPTED within one request's turn. `rid`, `attempt` (number), `from_stage`,
`to_stage`.

`signer_response`: one per SIGLOG# item written (logged after the item is durable). `slot`, `request_id` (signer
request id, or `invalid:<hash>` if the response id was malformed), `status` (`SIGNED`, `REFUSED`, `OTHER`), `reason`
(bounded code, `UNRECOGNIZED_REASON` if unrecognized, null), `disposition` (`used`, `unrequested`, `malformed`,
`bad-signature`, `refused`, `duplicate`, `not-waiting`, `other-attempt`, `superseded:<outcome>`), `frame_sha256`,
`signature_sha256`, `attempt`, `recovered` (true for a reconciled stored signature).

`poll_summary`: one per `poll()` run, including a run that raises. The summary dict: `drained`, `cleaned`,
`advanced` (rid -> [stage before, stage or state after]), and when present `out_of_time`, `deferred`.

`poller_note`: each in-memory note the poller records. `msg` (truncated to 500 characters).
