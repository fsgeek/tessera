"""Structured application log lines (docs/V1-DETECTION-CONTRACT.md gap G1; field reference: ../LOGGING.md).

One JSON object per line on stdout, which Lambda delivers to CloudWatch Logs. Every line carries "event" and "v"
(the schema version) so metric filters can match on them. Logging never changes behaviour: emit() swallows every
failure (BaseException included: a logging fault never replaces an exception or cancels a return), and callers pass only digests, ids, states and reason codes (never request content, request keys or
secrets)."""
import json
import sys

V = 1


def emit(event, **fields):
    try:
        line = json.dumps({"event": event, "v": V, **fields}, sort_keys=True, default=str, separators=(",", ":"))
        sys.stdout.write(line + "\n")                  # one write, no flush: Lambda's runtime captures stdout
    except BaseException:  # noqa: BLE001  a logging failure must never raise into the issuer
        pass
