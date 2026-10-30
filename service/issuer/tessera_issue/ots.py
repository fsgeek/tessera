"""OpenTimestamps for the issuer: proof trees in the closed V1 grammar (profile 15.2: sha256, append, prepend;
Bitcoin and pending attestations), stamping through calendars, upgrading pending attestations, and k = 6
readiness. Reading for checks uses the service verifier's own parser (tessera_verify.anchors).

Calendar interface (the public calendar protocol): submit(message) -> serialized timestamp from that message
(POST <cal>/digest); fetch(commitment) -> serialized timestamp or None while pending (GET <cal>/timestamp/<hex>).
HttpCalendar speaks it over an injected transport; StandInCalendar (stand_in.py) serves it locally."""
from tessera_verify.anchors import BTC, MAGIC, PENDING, parse_ots
from tessera_verify.codec import Fault

from .util import sha256


class OtsError(ValueError):
    pass


def _varuint(n):
    out = b""
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out += bytes([b | 0x80])
        else:
            return out + bytes([b])


def _varbytes(b):
    return _varuint(len(b)) + b


class _Reader:
    def __init__(self, data):
        self.d, self.i = data, 0

    def byte(self):
        if self.i >= len(self.d):
            raise OtsError("truncated")
        self.i += 1
        return self.d[self.i - 1]

    def take(self, n):
        if self.i + n > len(self.d):
            raise OtsError("truncated")
        self.i += n
        return self.d[self.i - n:self.i]

    def varuint(self):
        v = sh = 0
        while True:
            c = self.byte()
            v |= (c & 0x7F) << sh
            sh += 7
            if not c & 0x80:
                return v
            if sh > 35:
                raise OtsError("varuint")


class Node:
    """A timestamp node: items are ("att", tag, payload) or ("op", opcode, arg, child)."""

    def __init__(self):
        self.items = []

    def op(self, opcode, arg=b""):
        for it in self.items:
            if it[0] == "op" and it[1] == opcode and it[2] == arg:
                return it[3]
        child = Node()
        self.items.append(("op", opcode, arg, child))
        return child

    def att(self, tag, payload):
        if ("att", tag, payload) not in self.items:
            self.items.append(("att", tag, payload))

    def merge(self, other):
        for it in other.items:
            if it[0] == "att":
                self.att(it[1], it[2])
            else:
                self.op(it[1], it[2]).merge(it[3])

    def ser(self):
        out = b""
        for i, it in enumerate(self.items):
            if i < len(self.items) - 1:
                out += b"\xff"
            if it[0] == "att":
                out += b"\x00" + it[1] + _varbytes(it[2])
            else:
                out += bytes([it[1]]) + (_varbytes(it[2]) if it[1] != 0x08 else b"") + it[3].ser()
        return out


def apply(opcode, arg, msg):
    return sha256(msg) if opcode == 0x08 else msg + arg if opcode == 0xF0 else arg + msg


def parse_timestamp(data):
    """Serialized timestamp (no file header) -> Node. Raises OtsError outside the grammar."""
    r = _Reader(data)
    node = _parse(r, 0)
    if r.i != len(data):
        raise OtsError("trailing bytes")
    return node


def _parse(r, depth):
    if depth > 256:
        raise OtsError("depth")
    node = Node()
    while True:
        more = r.d[r.i:r.i + 1] == b"\xff"
        if more:
            r.i += 1
        op = r.byte()
        if op == 0x00:
            tag = r.take(8)
            if tag not in (BTC, PENDING):
                raise OtsError("attestation tag outside the V1 grammar")
            node.items.append(("att", tag, r.take(r.varuint())))
        elif op in (0x08, 0xF0, 0xF1):
            arg = b"" if op == 0x08 else r.take(r.varuint())
            node.items.append(("op", op, arg, _parse(r, depth + 1)))
        else:
            raise OtsError(f"op {op:#x} outside the V1 grammar")
        if not more:
            return node


def parse_file(raw):
    """-> (digest, root Node)."""
    if not raw.startswith(MAGIC) or raw[len(MAGIC):len(MAGIC) + 2] != b"\x01\x08":
        raise OtsError("not an OTS file of major version 1 with a SHA-256 file hash")
    i = len(MAGIC) + 2
    return raw[i:i + 32], parse_timestamp(raw[i + 32:])


def serialize_file(digest, root):
    return MAGIC + b"\x01\x08" + digest + root.ser()


def pending_uri(payload):
    r = _Reader(payload)
    return r.take(r.varuint()).decode("ascii", "replace")


def pending_payload(uri):
    return _varbytes(uri.encode("ascii"))


def walk(node, msg):
    """Yield (node, message at node)."""
    stack = [(node, msg)]
    while stack:
        n, m = stack.pop()
        yield n, m
        for it in n.items:
            if it[0] == "op":
                stack.append((it[3], apply(it[1], it[2], m)))


def stamp(digest, calendars, nonce):
    """One stamp: file digest -> append(nonce) -> sha256 -> each calendar's timestamp. -> file bytes."""
    if len(digest) != 32 or len(nonce) != 16:
        raise OtsError("digest and nonce lengths")
    root = Node()
    m = sha256(digest + nonce)
    node = root.op(0xF0, nonce).op(0x08)
    got = 0
    for cal in calendars:
        try:
            node.merge(parse_timestamp(cal.submit(m)))
            got += 1
        except (OtsError, OSError, CalendarError):
            continue
    if not got:
        raise OtsError("no calendar accepted the stamp")
    return serialize_file(digest, root)


def upgrade(raw, calendars):
    """Replace each pending attestation whose calendar now has a complete timestamp. -> (new bytes, changed)."""
    new, changed, _, _ = upgrade_bounded(raw, calendars)
    return new, changed


def upgrade_bounded(raw, calendars, keep_going=None, start=0):
    """upgrade(), asking keep_going() before each calendar request and beginning with the pending attestation at index
    `start` (mod their number), so a caller that keeps the returned position durably serves every pending calendar in
    turn across invocations instead of revisiting the same first ones (ILC-I-05). When keep_going() answers False
    the remaining pending attestations are left as they are.
    -> (new bytes, changed, finished: every pending attestation was asked, next start position)."""
    by_uri = {c.uri: c for c in calendars}
    digest, root = parse_file(raw)
    pending = [(node, msg, it) for node, msg in list(walk(root, digest)) for it in list(node.items)
               if it[0] == "att" and it[1] == PENDING and pending_uri(it[2]) in by_uri]
    n = len(pending)
    changed, finished, nxt = False, True, 0
    for j in range(n):
        k = (start + j) % n
        node, msg, it = pending[k]
        if keep_going is not None and not keep_going():
            finished, nxt = False, k
            break
        try:
            got = by_uri[pending_uri(it[2])].fetch(msg)
        except (OSError, CalendarError):
            got = None
        if got:
            sub = parse_timestamp(got)
            node.items.remove(it)
            node.merge(sub)
            changed = True
    return serialize_file(digest, root), changed, finished, nxt


def lowest_btc_height(raw):
    """Lowest Bitcoin attestation height in the proof, or None (read with the verifier's parser)."""
    try:
        p = parse_ots(raw)
    except Fault as e:
        raise OtsError(e.code) from None
    return min((a.height for a in p.bitcoin), default=None)


def prune_to_height(raw, height, merkle_root=None):
    """Keep only the branches ending in a Bitcoin attestation at `height` (and, when merkle_root is given, whose
    attested message IS that block's merkle root: a contradicted branch is dropped). The preserved presentation of a
    latch is pruned this way, so whatever headers later travel with it, its lowest qualifying height (and so T) cannot
    move to another attestation (profile 7.1: T is presentation-sensitive), and it carries no contradiction.
    -> (file bytes, number of contradicted attestations at `height` dropped)."""
    digest, root = parse_file(raw)
    dropped = [0]

    def keep(node, msg):
        items = []
        for it in node.items:
            if it[0] == "att":
                if it[1] == BTC and _Reader(it[2]).varuint() == height:
                    if merkle_root is None or msg == merkle_root:
                        items.append(it)
                    else:
                        dropped[0] += 1
            elif keep(it[3], apply(it[1], it[2], msg)):
                items.append(it)
        node.items = items
        return bool(items)
    if not keep(root, digest):
        raise OtsError(f"no qualifying Bitcoin attestation at height {height}")
    return serialize_file(digest, root), dropped[0]


def k6_ready(raw, tip):
    h = lowest_btc_height(raw)
    return (h is not None and h + 5 <= tip), h


class CalendarError(Exception):
    pass


class HttpCalendar:
    """The public calendar protocol over an injected transport(method, url, body) -> (status, bytes)."""

    def __init__(self, uri, transport):
        from .deadline import HTTP_WORST_S, guarded_transport
        self.uri = uri.rstrip("/")
        self.transport = guarded_transport(transport, "calendar", HTTP_WORST_S)     # ILC-I-02

    def submit(self, message):
        status, body = self.transport("POST", self.uri + "/digest", message)
        if status != 200:
            raise CalendarError(f"calendar {self.uri} submit: HTTP {status}")
        return body

    def fetch(self, commitment):
        status, body = self.transport("GET", self.uri + "/timestamp/" + commitment.hex(), None)
        if status == 404:
            return None
        if status != 200:
            raise CalendarError(f"calendar {self.uri} fetch: HTTP {status}")
        return body


def _sock_timeout(response, seconds):
    """Give the response's socket only the time left of the request's total (CPython's http.client layout)."""
    try:
        response.fp.raw._sock.settimeout(seconds)
    except AttributeError:
        pass


def urllib_transport(timeout=None):
    """Real HTTP for the deployed issuer (not used by the tests). ILC-I-02: the request's TOTAL time is bounded by its
    timeout (service.HTTP_TIMEOUT_S), capped by what the poller's deadline leaves (deadline.call_timeout): the socket
    timeout covers each blocking operation, and the body is read in chunks against the total."""
    import time
    import urllib.error
    import urllib.request
    from .deadline import call_timeout
    from .service import HTTP_TIMEOUT_S

    def t(method, url, body):
        total = call_timeout(timeout or HTTP_TIMEOUT_S)
        end = time.monotonic() + total
        req = urllib.request.Request(url, data=body, method=method,
                                     headers={"Accept": "application/vnd.opentimestamps.v1",
                                              "User-Agent": "tessera-issuer/1"})
        try:
            with urllib.request.urlopen(req, timeout=total) as r:
                out = b""
                while len(out) < (1 << 20):
                    left = end - time.monotonic()
                    if left <= 0:
                        raise TimeoutError(f"{url}: over {total:.0f} s")
                    _sock_timeout(r, left)
                    chunk = r.read(min(65536, (1 << 20) - len(out)))
                    if not chunk:
                        break
                    out += chunk
                return r.status, out
        except urllib.error.HTTPError as e:
            return e.code, b""
    return t


def txid_of(att):
    """Display txid of the transaction on an attestation path (verifier Attestation): the first consecutive
    SHA-256 pair's input, as profile 15.2 defines it; None if the path has none."""
    from tessera_verify.anchors import sha256d
    p = att.path
    for i in range(len(p) - 1):
        if p[i][0] == p[i + 1][0] == 0x08:
            return sha256d(p[i][2])[::-1].hex()
    return None
