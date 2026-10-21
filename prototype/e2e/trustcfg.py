#!/usr/bin/env python3
"""Trust configuration builder (V1-PROFILE §5, §15.5) from real material.

  fetch-roots   download IANA root-anchors.xml, root-anchors.p7s and icannbundle.pem into an archive directory with
                URL, fetch time and SHA-256 (sources.json); never overwrites an archived file.
  roots         build the two root KSK entries (KSK-2017, KSK-2024) from the archive: full DNSKEY RDATA from the
                XML's PublicKey/Flags (RFC 9718 format), DS SHA-256 cross-checked against the XML digest, and the
                RDATA cross-checked byte for byte against the archived live root DNSKEY RRsets of the spike captures.
                The .p7s is checked with `openssl cms -verify` against icannbundle.pem when openssl is present;
                that CA bundle was fetched over the same HTTPS channel, so this is NOT the profile's independent
                bootstrap (§5 "recorded bootstrap procedure"); the record says so.
  build         assemble the §15.5 object (JCS, closed schema): root KSKs, repository key entry, header pins, as_of.

Signing periods are the profile's PROPOSED acceptance-policy endpoints (§5; OPEN, §14.2 item 3), not sourced
signing events: KSK-2017 [2018-10-11T16:00:00Z, 2026-10-11T00:00:00Z], KSK-2024 [2026-10-11T00:00:00Z, open),
reliance lifetime L = 1814400 s (21 days observed).

  uv run python e2e/trustcfg.py fetch-roots [--archive DIR]
  uv run python e2e/trustcfg.py roots [--archive DIR]
"""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

import dns.message

from common import PROTO, WORK, U, b64, b64d, jcs, sha256hex, write_atomic, write_json, read_json, log

ROOT_URLS = {"root-anchors.xml": "https://data.iana.org/root-anchors/root-anchors.xml",
             "root-anchors.p7s": "https://data.iana.org/root-anchors/root-anchors.p7s",
             "icannbundle.pem": "https://data.iana.org/root-anchors/icannbundle.pem"}
ARCHIVE = WORK / "root-anchors"
SPIKE_CAPTURES = [PROTO / "spike" / "out" / "dns-snapshot.json", PROTO / "spike" / "out-ksk2024" / "dns-snapshot.json"]
POLICY = {   # name -> (signing_start, signing_end, publication, revocation): profile §5 PROPOSED values
    # 2026-10-19: KSK-2017 publication corrected from 2017-08-11 to 2017-07-11 (ICANN); sources in formal/trust-sources/
    20326: ("KSK-2017", "2018-10-11T16:00:00Z", "2026-10-11T00:00:00Z", "2017-07-11T00:00:00Z", "2027-01-11T00:00:00Z"),
    38696: ("KSK-2024", "2026-10-11T00:00:00Z", None, "2025-01-11T00:00:00Z", None),   # publication sourced: formal/trust-sources/VALUES.md
}
RELIANCE_L = "1814400"


def fetch_roots(archive=ARCHIVE):
    archive = Path(archive)
    archive.mkdir(parents=True, exist_ok=True)
    src_file = archive / "sources.json"
    sources = read_json(src_file) if src_file.exists() else {}
    for name, url in ROOT_URLS.items():
        if (archive / name).exists():
            continue
        req = urllib.request.Request(url, headers={"User-Agent": "tessera-e2e-instrument"})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        write_atomic(archive / name, data)
        sources[name] = {"uri": url, "sha256": sha256hex(data), "fetched": U.rfc3339(int(time.time())),
                         "length": len(data)}
        log(f"archived {url} sha256 {sources[name]['sha256']}")
    write_json(src_file, sources)
    return sources


def _p7s_check(archive):
    if not shutil.which("openssl"):
        return "openssl not present: .p7s not checked"
    r = subprocess.run(["openssl", "cms", "-verify", "-inform", "DER", "-in", str(archive / "root-anchors.p7s"),
                        "-content", str(archive / "root-anchors.xml"), "-CAfile", str(archive / "icannbundle.pem"),
                        "-binary", "-purpose", "any", "-out", "/dev/null"], capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip().splitlines()
    return ("verified" if r.returncode == 0 else "FAILED") + " (openssl cms -verify; CA bundle from the same " \
        "HTTPS channel, not an independent bootstrap): " + (out[-1] if out else "")


def _spike_root_rdatas():
    """{path: (sha256 of the file, [root DNSKEY RDATA with flags 257])} from the archived live captures."""
    out = {}
    for p in SPIKE_CAPTURES:
        if not p.exists():
            continue
        cap = json.loads(p.read_text())
        m = dns.message.from_wire(b64d(cap["messages"][". DNSKEY"]))
        rds = [rd.to_digestable() for rr in m.answer if rr.rdtype == 48 for rd in rr if rd.flags & 1]
        out[str(p.relative_to(PROTO.parent))] = (sha256hex(p.read_bytes()), rds)
    return out


def roots(archive=ARCHIVE):
    archive = Path(archive)
    sources = read_json(archive / "sources.json")
    xml = (archive / "root-anchors.xml").read_bytes()
    assert sha256hex(xml) == sources["root-anchors.xml"]["sha256"]
    assert b"<!DOCTYPE" not in xml and b"<!ENTITY" not in xml, "refusing DTD/entities in root-anchors.xml"
    tree = ET.fromstring(xml)
    p7s = _p7s_check(archive)
    spike = _spike_root_rdatas()
    entries = []
    for kd in tree.iter("KeyDigest"):
        tag, alg = int(kd.findtext("KeyTag")), int(kd.findtext("Algorithm"))
        if tag not in POLICY:
            continue
        flags, pub = int(kd.findtext("Flags")), b64d("".join(kd.findtext("PublicKey").split()))
        rd = flags.to_bytes(2, "big") + bytes([3, alg]) + pub
        assert U.key_tag(rd) == tag, f"key tag mismatch for {tag}"
        assert int(kd.findtext("DigestType")) == 2
        ds = hashlib.sha256(b"\x00" + rd).hexdigest()
        assert ds == kd.findtext("Digest").strip().lower(), f"DS digest mismatch for {tag}"
        name, start, end, pubd, rev = POLICY[tag]
        srcs = [{"description": f"IANA root-anchors.xml KeyDigest id={kd.get('id')} (PublicKey, Flags, DS digest "
                                f"cross-checked); .p7s: {p7s}; fetched {sources['root-anchors.xml']['fetched']}",
                 "sha256": sources["root-anchors.xml"]["sha256"], "uri": ROOT_URLS["root-anchors.xml"]}]
        for path, (h, rds) in spike.items():
            if rd in rds:
                srcs.append({"description": f"archived live root DNSKEY RRset (spike capture) contains this RDATA "
                                            f"byte for byte", "sha256": h, "uri": "repo:" + path})
        entries.append({"algorithm": str(alg), "dnskey_rdata": b64(rd), "ds_sha256": ds, "key_tag": str(tag),
                        "name": name, "publication": pubd, "reliance_lifetime_s": RELIANCE_L, "revocation": rev,
                        "signing_end": end, "signing_start": start, "sources": srcs})
    assert {e["key_tag"] for e in entries} == {str(t) for t in POLICY}, "root-anchors.xml lacks a policy KSK"
    entries.sort(key=lambda e: (U.ts(e["signing_start"]), int(e["key_tag"]), b64d(e["dnskey_rdata"])))
    write_json(archive / "root-ksks.json", entries)
    return entries


def repo_entry(pgp_body, signing_start, source_desc, source_sha256, source_uri, end=None):
    return {"domain": "wamason.com", "key": b64(pgp_body), "signing_end": end, "signing_start": signing_start,
            "sources": [{"description": source_desc, "sha256": source_sha256, "uri": source_uri}]}


def build(pins, as_of, root_ksks, repo_entries, version="1", previous=None):
    """The §15.5 object as JCS bytes. pins: {height(int|str): display hash}."""
    obj = {"as_of": as_of, "format": "tessera-v1-trust/1", "header_pins": {str(h): v for h, v in pins.items()},
           "issuer_domain": "wamason.com", "previous_sha256": previous or "0" * 64, "profile": "tessera-v1-strict",
           "repository_keys": sorted(repo_entries, key=lambda e: (U.ts(e["signing_start"]), b64d(e["key"]))),
           "root_ksks": root_ksks, "version": version}
    for e in root_ksks:
        assert re.fullmatch(r"[0-9a-f]{64}", e["ds_sha256"])
    return jcs(obj)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["fetch-roots", "roots"])
    ap.add_argument("--archive", default=str(ARCHIVE))
    a = ap.parse_args()
    if a.cmd == "fetch-roots":
        fetch_roots(a.archive)
    e = roots(a.archive)
    for x in e:
        log(f"{x['name']} tag {x['key_tag']} alg {x['algorithm']} ds {x['ds_sha256'][:16]}... "
            f"[{x['signing_start']}, {x['signing_end']}] sources {len(x['sources'])}")
        for s in x["sources"]:
            log("   -", s["uri"], s["description"][:120])


if __name__ == "__main__":
    main()
