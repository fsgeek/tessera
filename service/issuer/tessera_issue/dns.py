"""DNSSEC snapshot capture (profile 15.3) behind one interface: capture(now) -> snapshot body bytes.

LiveDns asks a resolver (over an injected transport: query wire -> response wire) for the six RRsets from the root
DNSKEY down to _tessera-v1.<D> TXT with the DO and CD bits, and converts the answers to the 15.3 body: groups in
chain order, canonical (lowercase, uncompressed) owners, RDATA sorted without duplicates, then RRSIGs sorted by
(key tag, inception, expiration, signature, RDATA), every TTL equal to the group's least Original TTL.
Validation is not done here: the pipeline validates with the service verifier's DNSSEC code before stamping."""
import os
import socket
import struct

from .util import D

T_TXT, T_DS, T_RRSIG, T_DNSKEY, T_OPT = 16, 43, 46, 48, 41
QUERIES = [(".", T_DNSKEY), ("com.", T_DS), ("com.", T_DNSKEY), (D + ".", T_DS), (D + ".", T_DNSKEY),
           ("_tessera-v1." + D + ".", T_TXT)]


class DnsError(Exception):
    pass


class SnapshotSource:
    def capture(self, now):
        raise NotImplementedError


def name_wire(name):
    name = name.rstrip(".").lower()
    if not name:
        return b"\x00"
    return b"".join(bytes([len(x)]) + x.encode("ascii") for x in name.split(".")) + b"\x00"


def make_query(name, rtype, qid=None):
    qid = int.from_bytes(os.urandom(2), "big") if qid is None else qid
    head = struct.pack(">HHHHHH", qid, 0x0110, 1, 0, 0, 1)            # RD, CD; one question; one additional (OPT)
    opt = b"\x00" + struct.pack(">HHIH", T_OPT, 4096, 0x00008000, 0)   # EDNS0, payload 4096, DO
    return head + name_wire(name) + struct.pack(">HH", rtype, 1) + opt


def _read_name(msg, i, depth=0):
    labels = []
    while True:
        if i >= len(msg) or depth > 64:
            raise DnsError("bad name")
        n = msg[i]
        if n & 0xC0 == 0xC0:
            ptr = ((n & 0x3F) << 8) | msg[i + 1]
            rest, _ = _read_name(msg, ptr, depth + 1)
            return labels + rest, i + 2
        i += 1
        if n == 0:
            return labels, i
        labels.append(msg[i:i + n].lower())
        i += n


def parse_answers(msg):
    """-> (truncated flag, [(owner labels tuple, type, ttl, rdata)]) from the answer section."""
    if len(msg) < 12:
        raise DnsError("short message")
    _, flags, qd, an, _, _ = struct.unpack(">HHHHHH", msg[:12])
    if flags & 0x000F:
        raise DnsError(f"rcode {flags & 0xF}")
    i = 12
    for _ in range(qd):
        _, i = _read_name(msg, i)
        i += 4
    out = []
    for _ in range(an):
        owner, i = _read_name(msg, i)
        rtype, cls, ttl, ln = struct.unpack(">HHIH", msg[i:i + 10])
        i += 10
        rd = msg[i:i + ln]
        if len(rd) != ln:
            raise DnsError("truncated RDATA")
        i += ln
        if cls == 1:
            out.append((tuple(owner), rtype, ttl, rd))
    return bool(flags & 0x0200), out


def truncated(msg):
    """The TC bit from the header alone: a truncated answer may end inside a record."""
    if len(msg) < 12:
        raise DnsError("short message")
    return bool(struct.unpack(">H", msg[2:4])[0] & 0x0200)


def _canonical_rrsig(rd):
    """Lowercase the signer name inside RRSIG RDATA (it is never compressed, RFC 4034 3.1.7)."""
    labels, end = _read_name(rd, 18)
    return rd[:18] + b"".join(bytes([len(x)]) + x for x in labels) + b"\x00" + rd[end:]


def group_bytes(owner, rtype, rdatas, rrsigs):
    ow = name_wire(owner)
    ttl = min(struct.unpack(">I", s[4:8])[0] for s in rrsigs)
    out = b""
    for rd in sorted(set(rdatas)):
        out += ow + struct.pack(">HHIH", rtype, 1, ttl, len(rd)) + rd
    for rd in sorted(set(rrsigs), key=lambda r: (r[16:18], r[12:16], r[8:12], r[r.index(b"\x00", 18) + 1:], r)):
        out += ow + struct.pack(">HHIH", T_RRSIG, 1, ttl, len(rd)) + rd
    return out


def convert(responses):
    """responses: [(name, type, response wire)] in QUERIES order -> 15.3 body."""
    body = b""
    for name, rtype, wire in responses:
        _, rrs = parse_answers(wire)
        want = tuple(x.encode() for x in name.rstrip(".").lower().split(".") if x)
        rds = [rd for o, t, _, rd in rrs if o == want and t == rtype]
        sigs = [_canonical_rrsig(rd) for o, t, _, rd in rrs if o == want and t == T_RRSIG
                and struct.unpack(">H", rd[:2])[0] == rtype]
        if not rds or not sigs:
            raise DnsError(f"no signed {rtype} RRset at {name}")
        body += group_bytes(name, rtype, rds, sigs)
    return body


class LiveDns(SnapshotSource):
    """Resolver capture for the deployed issuer. transport(query wire) -> response wire."""

    def __init__(self, transport):
        from .deadline import DNS_WORST_S, guarded_transport
        self.transport = guarded_transport(transport, "dns", DNS_WORST_S)          # ILC-I-02: each query

    def capture(self, now):
        responses = []
        for name, rtype in QUERIES:
            responses.append((name, rtype, self.transport(make_query(name, rtype))))
        return convert(responses)


def udp_tcp_transport(server="1.1.1.1", timeout=10):
    """Real resolver access (not used by the tests): UDP, then TCP when truncated. ILC-I-02: the query's TOTAL time is
    at most 2 x timeout (deadline.DNS_WORST_S), capped by what the poller's deadline leaves; every blocking operation
    gets only the time remaining of that total."""
    import time
    from .deadline import call_timeout

    def t(q):
        end = time.monotonic() + call_timeout(2 * timeout)

        def left():
            rest = end - time.monotonic()
            if rest <= 0:
                raise DnsError("resolver query over its time")
            return min(timeout, rest)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(left())
            s.sendto(q, (server, 53))
            r, _ = s.recvfrom(65535)
        if truncated(r):                       # IS-11: header TC bit, before any record is parsed
            with socket.create_connection((server, 53), timeout=left()) as s:
                s.sendall(struct.pack(">H", len(q)) + q)
                s.settimeout(left())
                n = struct.unpack(">H", s.recv(2))[0]
                r = b""
                while len(r) < n:
                    s.settimeout(left())
                    chunk = s.recv(n - len(r))
                    if not chunk:
                        raise DnsError("TCP response truncated")
                    r += chunk
        return r
    return t
