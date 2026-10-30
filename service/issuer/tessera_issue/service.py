"""The issuer's wiring: one object holding the window, the frozen objects, the stores, the signers, the calendars,
the header source, the DNS source, the pre-ship checker and the clock. API handlers and the poller take it."""
import time
from dataclasses import dataclass, field

from .util import HOUR, SystemClock, random_bytes

# The registered lifecycle (A2.1-A2.3 with A9.2's parameters; docs/decisions/2026-10-29-issuance-lifecycle.md). There is
# no request deadline: the former 24-hour FAILED rule (S4) contradicted A2 and is withdrawn.
N_ATTEMPTS = 3                      # A2.3 / A9.2: at most N attempts per request
SLACK_S = 24 * HOUR                 # A2.1 / A9.2: S; an attempt's boundary is B = declared + delta + S
POLL_INTERVAL_S = 600               # the poller's schedule (infra: rate(10 minutes)); indexes failed_intervals, which
                                    # is diagnostic only while design step 5 is gated
# ILI-05 / ILC-I-02: one poll runs inside one Lambda invocation (timeout 300 s, infra/main.tf). deadline.py guards
# every request the poller makes: it starts a request only if the request's worst case fits the time left minus the
# reserve, and caps the request's timeout to what is left. Running out of time never ends an attempt.
POLLER_TIMEOUT_S = 300
POLL_BUDGET_S = 290                 # the invocation's usable time (lambda_app lowers it to the time actually left)
POLL_RESERVE_S = 10                 # kept free after the last request: returning the poll's summary
HTTP_TIMEOUT_S = 20                 # one calendar or explorer request, total (ots.urllib_transport caps the total)
# CF3-01, ILC-I-02: the SDK's own time per AWS request (connection, response wait, retries and back-off). Passed to
# botocore.config.Config; deadline.AWS_WORST_S is computed from it.
AWS_CLIENT_CONFIG = {"connect_timeout": 3, "read_timeout": 8,
                     "retries": {"mode": "standard", "total_max_attempts": 3}}
RETENTION_S = 30 * 24 * HOUR        # S5: lookup and retrieval for 30 days after the request ends
WRITE_LEASE_S = 15 * 60             # CF-02: the longest a Lambda invocation can run (AWS maximum); every issuer write
                                    # happens inside one, so none lands later than this after its writer saw the request
SIGNER_RETRY_S = 30 * 60            # re-send an unanswered signer request (same request id) after 30 min


@dataclass
class Issuer:
    window: object
    frozen: object
    requests: object                 # RequestStore
    results: object                  # ResultStore
    signers: dict                    # {"kms": SlotSigner, "gpg": SlotSigner}
    calendars: list
    headers: object                  # HeaderSource
    dns: object                      # SnapshotSource
    preship: object                  # PreShip
    clock: object = field(default_factory=SystemClock)
    closing: bool = False            # operator: closure announced and reached -> CLOSING
    signing_available: bool = True   # operator: a signer is known to be down -> SIGNING_UNAVAILABLE
    nonce: object = field(default=lambda: random_bytes(16))
    signer_retry_s: int = SIGNER_RETRY_S
    budget_s: float = POLL_BUDGET_S  # ILI-05: one poll's work budget (lambda_app lowers it to the time remaining)
    rng: object = field(default_factory=lambda: __import__("random").SystemRandom())   # ILC-I6: drain's first slot
    elapsed_clock: object = field(default=time.monotonic)   # ILC-I2-01: the invocation deadline's clock (monotonic;
                                                            # the stand-in issuer uses its fake clock)
    log: list = field(default_factory=list)

    def note(self, *a):
        self.log.append(" ".join(str(x) for x in a))

    @property
    def tombstone_until(self):
        """Content-free key records are kept until issuance closes, and long enough to answer EXPIRED for every
        request of the window (owner choice: not-after + 30 days + 1 day)."""
        return self.window.na + RETENTION_S + 24 * HOUR
