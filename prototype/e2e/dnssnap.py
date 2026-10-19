"""DNSSEC snapshot: live capture, conversion to the V1-PROFILE §15.3 body, and issuer pre-stamp / pre-ship checks.

capture()       queries a public resolver (default 1.1.1.1) with the DO bit, root down to _tessera-v1.<D> TXT, and
                keeps every response as raw wire (one JSON file). Read-only DNS: it never changes a record.
stub_capture()  the dry-run resolver: the same six responses, built as DNS wire messages from a TEST hierarchy
                (conformance universe zone keys) whose TXT carries the run's real assertion value.
convert()       resolver messages -> §15.3 body: groups in chain order (root DNSKEY; per zone DS then DNSKEY; TXT),
                canonical owner and RDATA (lowercase, uncompressed), RRset in canonical RDATA order without
                duplicates, then its RRSIGs in (key tag, inception, expiration, signature, RDATA) order. TTL of
                every RR in a group = the witness RRSIG's Original TTL.
validate()      parses a body back and validates the chain with dnspython at a given time under the profile's
                algorithm set {8, 13} / DS digests {2, 4}, trusting only the given root KSK RDATA; reports the
                joint window of the selected witnesses and the TXT value; checks the no-wildcard body restriction.
"""
import base64
import struct
import time
from types import SimpleNamespace

import dns.dnssec
import dns.flags
import dns.message
import dns.name
import dns.query
import dns.rdata
import dns.rdataclass
import dns.rdatatype
import dns.rrset

from common import D, TXT_OWNER, U, gen, b64, b64d

QUERIES = [(".", "DNSKEY"), ("com.", "DS"), ("com.", "DNSKEY"), (D + ".", "DS"), (D + ".", "DNSKEY"),
           (TXT_OWNER + ".", "TXT")]
T_TXT, T_DS, T_RRSIG, T_DNSKEY = 16, 43, 46, 48
ALGS, DIGESTS = (8, 13), (2, 4)


class SnapshotError(Exception):
    pass


# ------------------------------------------------------------------------------------------------ capture
def capture(server="1.1.1.1", timeout=10):
    msgs, t0 = {}, int(time.time())
    for n, t in QUERIES:
        q = dns.message.make_query(n, t, want_dnssec=True, use_edns=0, payload=4096)
        q.flags |= dns.flags.CD
        r = dns.query.udp(q, server, timeout=timeout)
        if r.flags & dns.flags.TC:
            r = dns.query.tcp(q, server, timeout=timeout)
        msgs[f"{n} {t}"] = b64(r.to_wire())
    return {"server": server, "captured_start": t0, "captured_end": int(time.time()),
            "queries": [f"{n} {t}" for n, t in QUERIES], "messages": msgs}


def stub_hierarchy(value, t):
    """TEST groups (root .. TXT) at time t, signed by conformance-universe zone keys; TXT = value."""
    import issue as I   # prototype/conformance/issue.py: default_dns_plan
    plan = I.default_dns_plan(SimpleNamespace(T_snap=t, value=value))
    return plan.groups()


def stub_capture(value, t=None):
    t = t or int(time.time())
    msgs = {}
    for (n, typ), g in zip(QUERIES, stub_hierarchy(value, t)):
        rrs = parse_body(U.serialize_groups([g]))
        q = dns.message.make_query(n, typ, want_dnssec=True)
        r = dns.message.make_response(q)
        name = dns.name.from_text(n)
        main = [rr for rr in rrs if rr["type"] != T_RRSIG]
        sigs = [rr for rr in rrs if rr["type"] == T_RRSIG]
        r.answer.append(dns.rrset.from_rdata_list(name, main[0]["ttl"], [_rd(rr["type"], rr["rdata"]) for rr in main]))
        rs = dns.rrset.RRset(name, dns.rdataclass.IN, dns.rdatatype.RRSIG, dns.rdatatype.from_text(typ))
        rs.update_ttl(sigs[0]["ttl"])
        for s in sigs:
            rs.add(_rd(T_RRSIG, s["rdata"]))
        r.answer.append(rs)
        msgs[f"{n} {typ}"] = b64(r.to_wire())
    return {"server": "STUB (TEST hierarchy, conformance universe zone keys)", "captured_start": t,
            "captured_end": t, "queries": [f"{n} {t_}" for n, t_ in QUERIES], "messages": msgs}


def stub_root_rdatas():
    return [U.ksk_a().rdata(), U.ksk_b().rdata()]


# ------------------------------------------------------------------------------------------------ convert
def _rd(rtype, wire):
    return dns.rdata.from_wire(dns.rdataclass.IN, rtype, wire, 0, len(wire))


def _owner_wire(name):
    return name.canonicalize().to_wire()


def convert(cap, queries=QUERIES):
    body = b""
    for n, t in queries:
        m = dns.message.from_wire(b64d(cap["messages"][f"{n} {t}"]))
        name, rtype = dns.name.from_text(n), dns.rdatatype.from_text(t)
        try:
            rrset = m.find_rrset(m.answer, name, dns.rdataclass.IN, rtype)
        except KeyError:
            raise SnapshotError(f"no {t} RRset at {n} in the response (rcode {m.rcode()})") from None
        try:
            sigs = m.find_rrset(m.answer, name, dns.rdataclass.IN, dns.rdatatype.RRSIG, rtype)
        except KeyError:
            raise SnapshotError(f"no RRSIG over {t} at {n}") from None
        ow = _owner_wire(name)
        ttl = min(s.original_ttl for s in sigs)
        rdatas = sorted({rd.to_digestable(dns.name.root) for rd in rrset})
        srd = sorted({(s.key_tag, s.inception, s.expiration, s.signature, s.to_digestable(dns.name.root))
                      for s in sigs})
        for rd in rdatas:
            body += ow + struct.pack(">HHIH", int(rtype), 1, ttl, len(rd)) + rd
        for *_, rd in srd:
            body += ow + struct.pack(">HHIH", T_RRSIG, 1, ttl, len(rd)) + rd
    return body


def envelope(body):
    return gen.encode_snapshot(body)        # ENC §6: header || u32 len || body


# ------------------------------------------------------------------------------------------------ parse + validate
def _name(b, i):
    labels = []
    while True:
        n = b[i]
        i += 1
        if n == 0:
            return tuple(labels), i
        if n > 63:
            raise SnapshotError("compressed or bad label")
        lab = b[i:i + n]
        if any(65 <= c <= 90 for c in lab):
            raise SnapshotError("uppercase label")
        labels.append(lab)
        i += n


def parse_body(body):
    rrs, i = [], 0
    while i < len(body):
        owner, i = _name(body, i)
        rtype, cls, ttl, ln = struct.unpack(">HHIH", body[i:i + 10])
        i += 10
        rd = body[i:i + ln]
        if len(rd) != ln or cls != 1:
            raise SnapshotError("truncated RR or class")
        i += ln
        rrs.append({"owner": owner, "type": rtype, "ttl": ttl, "rdata": rd})
    return rrs


def _text(labels):
    return ".".join(x.decode() for x in labels) + "." if labels else "."


def groups(body):
    """[(owner, covered type, [rdata], [rrsig rdata])] in body order."""
    out = []
    for rr in parse_body(body):
        cov = struct.unpack(">H", rr["rdata"][:2])[0] if rr["type"] == T_RRSIG else rr["type"]
        if out and out[-1][0] == rr["owner"] and out[-1][1] == cov:
            g = out[-1]
        else:
            g = (rr["owner"], cov, [], [])
            out.append(g)
        (g[3] if rr["type"] == T_RRSIG else g[2]).append(rr["rdata"])
    return out


def wildcard_free(body):
    for rr in parse_body(body):
        if rr["type"] == T_RRSIG and rr["rdata"][3] < len(rr["owner"]):
            return False
    return True


def validate(body, trusted_root_rdatas, at, queries=QUERIES):
    """Validate root -> TXT at time `at`. -> dict(ok, errors, window=(max inception, min expiration), value)."""
    res = {"ok": False, "errors": [], "witnesses": [], "value": None, "wildcard_free": wildcard_free(body)}
    gs = groups(body)
    order = [(_text(o), t) for o, t, _, _ in gs]
    want = [(n, dns.rdatatype.from_text(t)) for n, t in queries]
    if order != want:
        res["errors"].append(f"group order {order} != {want}")
        return res
    zone_keys = {}            # name -> rdataset of authenticated DNSKEY rdata
    ds_of = {}
    windows = []

    def rrset_of(owner, t, rdatas):
        return dns.rrset.from_rdata_list(dns.name.from_text(owner), 3600, [_rd(t, r) for r in rdatas])

    def witness(rrset, sigs, keyset_name, keyrdatas):
        keys = {dns.name.from_text(keyset_name): rrset_of(keyset_name, T_DNSKEY, keyrdatas)}
        for s in sorted(sigs, key=lambda r: (r[16:18], r[12:16], r[8:12], r)):
            rs = _rd(T_RRSIG, s)
            if rs.algorithm not in ALGS or rs.signer != dns.name.from_text(keyset_name):
                continue
            try:
                dns.dnssec.validate_rrsig(rrset, rs, keys, now=at)
            except dns.dnssec.ValidationFailure:
                continue
            return rs
        return None

    for owner, t, rdatas, sigs in gs:
        name = _text(owner)
        rrset = rrset_of(name, t, rdatas)
        if name == "." and t == T_DNSKEY:
            trusted = [r for r in rdatas if r in set(trusted_root_rdatas)]
            w = witness(rrset, sigs, ".", trusted) if trusted else None
            if w:
                zone_keys["."] = rdatas
        elif t == T_DS:
            parent = dns.name.from_text(name).parent().to_text()
            w = witness(rrset, sigs, parent, zone_keys.get(parent, [])) if parent in zone_keys else None
            if w:
                ds_of[name] = [_rd(T_DS, r) for r in rdatas if r[3] in DIGESTS]
        elif t == T_DNSKEY:
            matching = []
            for r in rdatas:
                k = _rd(T_DNSKEY, r)
                for ds in ds_of.get(name, []):
                    alg = {2: "SHA256", 4: "SHA384"}[ds.digest_type]
                    if dns.dnssec.make_ds(name, k, alg) == ds:
                        matching.append(r)
            w = witness(rrset, sigs, name, matching) if matching else None
            if w:
                zone_keys[name] = rdatas
        else:  # TXT, signed by its zone
            zone = dns.name.from_text(name).parent().to_text()
            w = witness(rrset, sigs, zone, zone_keys.get(zone, [])) if zone in zone_keys else None
            if w and len(rdatas) == 1:
                rd = rdatas[0]
                if rd[0] + 1 == len(rd):
                    res["value"] = rd[1:]
        if w is None:
            res["errors"].append(f"{name} {dns.rdatatype.to_text(t)}: no validating witness at {at}")
        else:
            windows.append((w.inception, w.expiration))
            res["witnesses"].append({"rrset": f"{name} {dns.rdatatype.to_text(t)}", "alg": w.algorithm,
                                     "key_tag": w.key_tag, "inception": w.inception, "expiration": w.expiration})
    if windows:
        res["window"] = (max(a for a, _ in windows), min(b for _, b in windows))
    need_txt = queries[-1][1] == "TXT"
    res["ok"] = not res["errors"] and res["wildcard_free"] and (res["value"] is not None or not need_txt)
    return res
