"""Item 4a: what a DNSSEC "chain snapshot" gives an offline verifier (RFC 4033-4035). THROWAWAY.

capture() (network, run once 2026-10-07) asks a resolver, with the DO bit, for every RRset on a
path from the root to a name and stores the raw DNS responses (wire format, base64) as a fixture.
validate_offline() then re-validates the chain with dnspython, with no network, at a CHOSEN time.

Findings this module demonstrates (see tests/test_phase3.py):
  * wamason.com is not signed: .com returns an authenticated denial (NSEC3, opt-out) of any DS for
    it. The registered evidence 1 (R-4.26) cannot be produced today.
  * the only key an offline verifier needs is the ROOT KSK; it authenticates every signed name on
    the internet, so "the DNS channel's key" (the model's skS / pk(skS)) is not specific to wamason.com.
    What ties a DNSSEC snapshot to an issuer is the owner NAME of the RRset -- a comparison the
    model never makes, against an issuer identity the spec says is "bound, not validated".
  * every RRSIG has an inception/expiration window (days to weeks); RFC 4035 §5.3.1 checks it against
    the validator's current time. A 2106 verifier must instead supply an authenticated time inside
    every window on the chain -- i.e. the snapshot itself must be time-anchored.
"""
from __future__ import annotations

import base64
import json
import time
from pathlib import Path

import dns.dnssec
import dns.flags
import dns.message
import dns.name
import dns.query
import dns.rdataclass
import dns.rdatatype
import dns.rrset

FIXTURES = Path(__file__).resolve().parent / "fixtures"
# IANA root trust anchor KSK-2017 (key tag 20326), DS digest type 2 (SHA-256), from root-anchors.xml.
ROOT_KSK_2017_DS = "E06D44B80B8F1D39A95C0B0D7C65D08458E880409BBC683457104237C7F8EC8D"
ROOT_KSK_2017_TAG = 20326


def _q(name: str, rtype: str, server: str) -> dns.message.Message:
    q = dns.message.make_query(name, rtype, want_dnssec=True)
    q.flags |= dns.flags.CD   # we validate ourselves
    r = dns.query.udp(q, server, timeout=10)
    if r.flags & dns.flags.TC:
        r = dns.query.tcp(q, server, timeout=10)
    return r


def capture(target: str, rtype: str, out: str, server: str = "1.1.1.1") -> dict:
    """Network. Fetch DNSKEY for every zone from root to `target`'s zone, DS for each child, and the
    target RRset (or the denial proof). Store raw wire messages."""
    labels = target.rstrip(".").split(".")
    zones = ["."] + [".".join(labels[i:]) + "." for i in range(len(labels) - 1, -1, -1)]  # root ... target
    msgs = {}
    for z in zones:
        msgs[f"{z} DNSKEY"] = _q(z, "DNSKEY", server)
        if z != ".":
            msgs[f"{z} DS"] = _q(z, "DS", server)
    msgs[f"{target} {rtype}"] = _q(target, rtype, server)
    d = {"captured": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "server": server, "target": target,
         "rtype": rtype, "messages": {k: base64.b64encode(m.to_wire()).decode() for k, m in msgs.items()}}
    (FIXTURES / out).write_text(json.dumps(d, indent=1))
    return d


def load(name: str) -> dict:
    d = json.loads((FIXTURES / name).read_text())
    d["msgs"] = {k: dns.message.from_wire(base64.b64decode(v)) for k, v in d["messages"].items()}
    return d


def _sets(msg: dns.message.Message, section: str = "answer"):
    """Split a section into {(name, type): rrset} and {(name, covered type): rrsig rrset}."""
    data, sigs = {}, {}
    for rr in getattr(msg, section):
        if rr.rdtype == dns.rdatatype.RRSIG:
            sigs[(rr.name, rr.covers)] = rr
        else:
            data[(rr.name, rr.rdtype)] = rr
    return data, sigs


def validate_offline(fx: dict, now: float) -> dict:
    """Walk root -> zones -> target with dnspython's RRSIG validation at time `now`. Returns a
    per-step ledger and a final status: SECURE (positive RRset validated), INSECURE (authenticated
    proof that the zone is unsigned), or BOGUS (some signature failed: at `now` that includes expiry)."""
    ledger = []
    msgs = fx["msgs"]
    zone_keys: dict[dns.name.Name, dns.rrset.RRset] = {}
    root = dns.name.root
    # 1. root DNSKEY against the trust anchor
    kd, ks = _sets(msgs[". DNSKEY"])
    keys = kd[(root, dns.rdatatype.DNSKEY)]
    ksk = [k for k in keys if dns.dnssec.key_id(k) == ROOT_KSK_2017_TAG]
    ds_ok = bool(ksk) and dns.dnssec.make_ds(root, ksk[0], "SHA256").digest.hex().upper() == ROOT_KSK_2017_DS
    ledger.append(("root KSK matches IANA anchor 20326", ds_ok))
    try:
        dns.dnssec.validate(keys, ks[(root, dns.rdatatype.DNSKEY)], {root: keys}, now=now)
        ledger.append(("root DNSKEY RRset self-signed", True))
    except dns.dnssec.ValidationFailure as e:
        ledger.append((f"root DNSKEY RRset self-signed: {e}", False))
        return {"status": "BOGUS", "ledger": ledger}
    zone_keys[root] = keys
    parent = root
    zones = [k.split()[0] for k in fx["messages"] if k.endswith(" DNSKEY")]
    for z in zones[1:]:
        zn = dns.name.from_text(z)
        dsmsg = msgs[f"{z} DS"]
        dd, dsig = _sets(dsmsg)
        if (zn, dns.rdatatype.DS) not in dd:
            # authenticated denial of DS => insecure delegation (RFC 4035 §5.2)
            ad, asig = _sets(dsmsg, "authority")
            ok = True
            for (n, t), rr in ad.items():
                if t in (dns.rdatatype.NSEC3, dns.rdatatype.NSEC, dns.rdatatype.SOA):
                    try:
                        dns.dnssec.validate(rr, asig[(n, t)], {parent: zone_keys[parent]}, now=now)
                    except (dns.dnssec.ValidationFailure, KeyError) as e:
                        ok = False
                        ledger.append((f"denial record {n} {dns.rdatatype.to_text(t)}: {e}", False))
            n3 = [rr for (n, t), rr in ad.items() if t == dns.rdatatype.NSEC3]
            ledger.append((f"no DS for {z}: authenticated denial via {len(n3)} NSEC3 record(s) signed by {parent}", ok))
            return {"status": "INSECURE" if ok else "BOGUS", "ledger": ledger, "insecure_at": z}
        try:
            dns.dnssec.validate(dd[(zn, dns.rdatatype.DS)], dsig[(zn, dns.rdatatype.DS)], {parent: zone_keys[parent]}, now=now)
            ledger.append((f"DS {z} signed by {parent}", True))
        except dns.dnssec.ValidationFailure as e:
            ledger.append((f"DS {z} signed by {parent}: {e}", False))
            return {"status": "BOGUS", "ledger": ledger}
        kd, ks = _sets(msgs[f"{z} DNSKEY"])
        keys = kd[(zn, dns.rdatatype.DNSKEY)]
        ds_digests = {(d.key_tag, d.digest) for d in dd[(zn, dns.rdatatype.DS)]}
        linked = any((dns.dnssec.key_id(k), dns.dnssec.make_ds(zn, k, d.digest_type).digest) in ds_digests
                     for k in keys for d in dd[(zn, dns.rdatatype.DS)])
        ledger.append((f"{z} DNSKEY matches a DS in {parent}", linked))
        try:
            dns.dnssec.validate(keys, ks[(zn, dns.rdatatype.DNSKEY)], {zn: keys}, now=now)
            ledger.append((f"{z} DNSKEY RRset self-signed", True))
        except dns.dnssec.ValidationFailure as e:
            ledger.append((f"{z} DNSKEY self-signed: {e}", False))
            return {"status": "BOGUS", "ledger": ledger}
        if not linked:
            return {"status": "BOGUS", "ledger": ledger}
        zone_keys[zn] = keys
        parent = zn
    tmsg = msgs[f"{fx['target']} {fx['rtype']}"]
    td, tsig = _sets(tmsg)
    tn = dns.name.from_text(fx["target"])
    rr = td.get((tn, dns.rdatatype.from_text(fx["rtype"])))
    if rr is None:
        return {"status": "BOGUS", "ledger": ledger + [("target RRset missing", False)]}
    try:
        dns.dnssec.validate(rr, tsig[(tn, rr.rdtype)], {parent: zone_keys[parent]}, now=now)
        ledger.append((f"{fx['target']} {fx['rtype']} signed by {parent}", True))
    except (dns.dnssec.ValidationFailure, KeyError) as e:
        ledger.append((f"{fx['target']} {fx['rtype']}: {e}", False))
        return {"status": "BOGUS", "ledger": ledger}
    return {"status": "SECURE", "ledger": ledger, "rrset": rr.to_text(), "owner": str(rr.name)}


def rrsig_windows(fx: dict) -> list[tuple[str, int, int]]:
    """(covered RRset, inception, expiration) for every RRSIG captured."""
    out = []
    for k, m in fx["msgs"].items():
        for sec in (m.answer, m.authority):
            for rr in sec:
                if rr.rdtype == dns.rdatatype.RRSIG:
                    for sig in rr:
                        out.append((f"{rr.name} {dns.rdatatype.to_text(sig.type_covered)}", sig.inception, sig.expiration))
    return out


def common_window(fx: dict) -> tuple[int, int]:
    w = rrsig_windows(fx)
    return max(x[1] for x in w), min(x[2] for x in w)
