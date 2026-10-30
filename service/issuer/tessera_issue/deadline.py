"""ONE deadline guard for every remote and store request the poller makes (ILC-I-02; docs/reviews/issuer-lifecycle-impl
/CODEX-CONFIRM.md). The poller installs a Deadline for the duration of one poll (pipeline.poll). Every client request
then goes through `call`, which

  (a) refuses to START the request unless its worst-case duration fits the time remaining minus the reserve
      (raising OutOfBudget: the work resumes in the next invocation; nothing is decided on a refused request), and
  (b) passes the request a timeout no larger than what remains: CALL_TIMEOUT holds that value while the request runs,
      and the HTTP and DNS transports cap their total time to it. AWS SDK clients cannot take a per-request timeout;
      their configured worst case (AWS_WORST_S, from the client configuration: attempts x (connect + read) plus the
      retry back-off) is what (a) admits, so it never exceeds what remains either.

The guard sits at the lowest layer, around each single request, so no adapter loop (pagination, deletion rounds,
explorer agreement) can multiply time unchecked:

  DynamoDB, S3, SQS (signer sends and receives), SNS   GuardedClient around each boto3-style client (aws.py, queues.py)
  calendars, explorers                                 guarded_transport in ots.HttpCalendar, chain.ExplorerHeaders
  DNS resolver                                         guarded_transport in dns.LiveDns
  the pre-ship check (local CPU, no timeout knob)      pipeline, with PRESHIP_WORST_S

Per-unit cost figures elsewhere (a header height, a tip) are computed from these worst cases and the configured
explorer count, and are used only to avoid starting a unit that cannot finish; the safety mechanism is this guard.
Outside a poll (the API, tests calling a function directly) no deadline is installed and calls run unguarded."""
import contextvars

from .service import AWS_CLIENT_CONFIG, HTTP_TIMEOUT_S

CURRENT = contextvars.ContextVar("tessera_deadline", default=None)
CALL_TIMEOUT = contextvars.ContextVar("tessera_call_timeout", default=None)


def aws_worst_s(config=AWS_CLIENT_CONFIG):
    """Worst case of one SDK request under the client configuration: every attempt waits its full connect and read
    timeouts, and every retry waits the standard mode's maximum back-off (20 s)."""
    attempts = config["retries"]["total_max_attempts"]
    return attempts * (config["connect_timeout"] + config["read_timeout"]) + (attempts - 1) * 20


AWS_WORST_S = aws_worst_s()
HTTP_WORST_S = HTTP_TIMEOUT_S              # one calendar or explorer request (total, capped by the transport)
DNS_WORST_S = 2 * 10                       # one resolver query: UDP, then TCP if truncated (total, capped)
PRESHIP_WORST_S = 30                       # the verifier library on one bundle; local CPU, measured well below


class OutOfBudget(Exception):
    """The next request does not fit the invocation's remaining time; resumed next poll."""


class Deadline:
    def __init__(self, clock, limit_s, reserve_s):
        self.clock, self.start, self.limit, self.reserve = clock, clock(), limit_s, reserve_s

    def remaining(self):
        return self.limit - (self.clock() - self.start)

    def available(self):
        return self.remaining() - self.reserve

    def ensure(self, worst_s, what=""):
        """Refuse unless `worst_s` fits; used for whole units (a header height) before their first request."""
        if worst_s > self.available():
            raise OutOfBudget(f"{what}: worst case {worst_s:.0f} s, {self.available():.0f} s available; "
                              "resumed next poll")

    def call(self, worst_s, fn, *args, what="", **kwargs):
        self.ensure(worst_s, what)
        token = CALL_TIMEOUT.set(min(worst_s, self.available()))
        try:
            return fn(*args, **kwargs)
        finally:
            CALL_TIMEOUT.reset(token)


def guarded(worst_s, fn, *args, what="", **kwargs):
    """Run one request under the current deadline (if any)."""
    d = CURRENT.get()
    if d is None:
        return fn(*args, **kwargs)
    return d.call(worst_s, fn, *args, what=what, **kwargs)


def ensure(worst_s, what=""):
    d = CURRENT.get()
    if d is not None:
        d.ensure(worst_s, what)


def call_timeout(default):
    """The timeout a transport must use for the request now running: its own, capped by what remains."""
    t = CALL_TIMEOUT.get()
    return default if t is None else max(0.001, min(default, t))


class GuardedClient:
    """A boto3-style client whose every method call is one guarded request of worst case AWS_WORST_S (or `worst_s`).
    Non-callable attributes pass through. Methods the adapters use to build URLs locally (generate_presigned_url)
    make no request and are not guarded."""
    LOCAL = {"generate_presigned_url"}

    def __init__(self, client, kind, worst_s=None):
        object.__setattr__(self, "_client", client)
        object.__setattr__(self, "_kind", kind)
        object.__setattr__(self, "_worst", AWS_WORST_S if worst_s is None else worst_s)

    def __setattr__(self, name, value):            # test hooks patch the wrapped client, not the guard
        setattr(self._client, name, value)

    def __getattr__(self, name):
        attr = getattr(self._client, name)
        if not callable(attr) or name in self.LOCAL:
            return attr

        def call(*args, **kwargs):
            return guarded(self._worst, attr, *args, what=f"{self._kind}.{name}", **kwargs)
        return call


def guarded_transport(transport, kind, worst_s):
    """A transport (method, url, body) or (query) whose every request is guarded."""
    if getattr(transport, "_tessera_guarded", False):
        return transport

    def t(*args):
        return guarded(worst_s, transport, *args, what=kind)
    t._tessera_guarded = True
    return t


class Installed:
    """Context manager: install a Deadline for one poll."""

    def __init__(self, deadline):
        self.deadline, self.token = deadline, None

    def __enter__(self):
        self.token = CURRENT.set(self.deadline)
        return self.deadline

    def __exit__(self, *exc):
        CURRENT.reset(self.token)
        return False
