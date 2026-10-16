"""THROWAWAY spike step 3 (NETWORK): capture wamason.com's live DNSSEC chain, root down, raw wire, with the DO bit.
Writes out/dns-snapshot.json. Every RRset and RRSIG returned in answer+authority is kept (wire format, base64)."""
import base64, json, time
from pathlib import Path
import dns.flags, dns.message, dns.query, dns.rdatatype

SERVER = "1.1.1.1"
OUT = Path(__file__).resolve().parent / "out"
QUERIES = [(".", "DNSKEY"), ("com.", "DS"), ("com.", "DNSKEY"), ("wamason.com.", "DS"), ("wamason.com.", "DNSKEY"),
           ("wamason.com.", "SOA"), ("wamason.com.", "NS"), ("wamason.com.", "TXT"),
           ("_tessera.wamason.com.", "TXT"), ("tessera.wamason.com.", "TXT")]

def q(name, rtype):
    m = dns.message.make_query(name, rtype, want_dnssec=True, use_edns=0, payload=4096)
    m.flags |= dns.flags.CD
    r = dns.query.udp(m, SERVER, timeout=10)
    if r.flags & dns.flags.TC:
        r = dns.query.tcp(m, SERVER, timeout=10)
    return r

t0 = int(time.time())
msgs, t_each = {}, {}
for n, t in QUERIES:
    msgs[f"{n} {t}"] = q(n, t); t_each[f"{n} {t}"] = int(time.time())
t1 = int(time.time())
d = {"captured_start": t0, "captured_end": t1, "server": SERVER, "queries": [f"{n} {t}" for n, t in QUERIES],
     "query_time": t_each, "messages": {k: base64.b64encode(m.to_wire()).decode() for k, m in msgs.items()}}
(OUT / "dns-snapshot.json").write_text(json.dumps(d, indent=1))
for k, m in msgs.items():
    print(k, "rcode", dns.rcode.to_text(m.rcode()), "ans", len(m.answer), "auth", len(m.authority))
print("captured", t0, t1)
