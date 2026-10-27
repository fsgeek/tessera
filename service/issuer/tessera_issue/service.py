"""The issuer's wiring: one object holding the window, the frozen objects, the stores, the signers, the calendars,
the header source, the DNS source, the pre-ship checker and the clock. API handlers and the poller take it."""
from dataclasses import dataclass, field

from .util import HOUR, SystemClock, random_bytes

DEADLINE_S = 24 * HOUR              # S4: not COMPLETE 24 h after acceptance -> FAILED
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
    log: list = field(default_factory=list)

    def note(self, *a):
        self.log.append(" ".join(str(x) for x in a))

    @property
    def tombstone_until(self):
        """Content-free key records are kept until issuance closes, and long enough to answer EXPIRED for every
        request of the window (owner choice: not-after + 30 days + 1 day)."""
        return self.window.na + RETENTION_S + 24 * HOUR
