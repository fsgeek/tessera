"""The registered attempt lifecycle's record shape, shared by the poller (the only lifecycle writer) and the read-only
API view. docs/decisions/2026-10-29-issuance-lifecycle.md; formal/tla/issuer-lifecycle/IssuerLifecycleR53.tla.

A request record carries `attempts` (1..N, oldest first) and `cur`, the number of its current attempt (0 before the
poller starts attempt 1). Each attempt holds its own declared issue time, signing jobs, proofs, latch and end, and all
its stored objects live under `work/<rid>/<attempt id>/`. Attempt states are the model's: "open", "latched",
"shipped", and the ended states "expired" and "discarded". ("unavail", EVIDENCE_UNAVAILABLE, is gated off until the
author decides design step 5, and nothing here can produce it.) Only the current attempt is open or latched (OneLive);
earlier ones are ended (PastAttemptsEnded)."""
from .service import N_ATTEMPTS, SLACK_S
from .util import DELTA, rfc3339, ts

OPEN, LATCHED, SHIPPED, EXPIRED, DISCARDED = "open", "latched", "shipped", "expired", "discarded"
ENDED = (EXPIRED, DISCARDED)
OUTCOME = {EXPIRED: "EXPIRED", DISCARDED: "DISCARDED"}
NOMINAL_NOTE = ("An unlatched attempt can expire only after this boundary (its declared issue time + 72 h + 24 h), "
                "and only on complete evidence that it fails the temporal predicate; until then it stays open. "
                f"{N_ATTEMPTS} attempts give a nominal budget of twelve days, which is not a bound on when the "
                "request ends.")


def attempt_id(n):
    return f"a{n}"


def new_attempt(n, now):
    """Attempt n, allocated at `now`, which is its declared issue time (the model's decl[i + 1] = now)."""
    return {"n": n, "id": attempt_id(n), "state": OPEN, "allocated_at": now, "declared_issue_time": rfc3339(now),
            "jobs": {}, "proofs": {}, "receipt_id": None, "latch": None, "end": None,
            "unavailable_since": None, "failed_intervals": []}


def current(rec):
    """The current attempt, or None before attempt 1 is started."""
    n = rec.get("cur") or 0
    return rec["attempts"][n - 1] if n else None


def B_of(att):
    """B = declared + delta + S (A2.1): eligibility observed at or before B is timely; expiry only strictly after."""
    return ts(att["declared_issue_time"]) + DELTA + SLACK_S


def attempt_reasons(rec):
    """Per-attempt endings, as the refusal lists them."""
    return [{"attempt": a["n"], "outcome": OUTCOME[a["state"]], "reason": a["end"]["reason"]}
            for a in rec.get("attempts") or [] if a["state"] in ENDED]


def public_attempt(rec):
    """Design step 9: attempt i of N, and for an open, unlatched attempt its B with the nominal-budget note."""
    a = current(rec)
    if a is None:
        return {"number": 1, "of": N_ATTEMPTS, "state": "starting"}
    v = {"number": a["n"], "of": N_ATTEMPTS, "state": a["state"]}
    if a["state"] == OPEN:
        v["expiry_boundary"] = rfc3339(B_of(a))
        v["note"] = NOMINAL_NOTE
    return v
