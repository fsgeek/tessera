#!/usr/bin/env python3
"""One network smoke test of the real OTS and header code paths, on 32 random bytes (no Tessera content).

  1. RealOts.stamp() of a file holding 32 random bytes -> public calendars; the issuer reader parses the result
     (pending attestations only, digest = SHA-256 of the file).
  2. btcheaders.tip() and btcheaders.fetch() of the six newest blocks from two explorers; pins and prev links
     checked with the issuer's qualification code.

Writes work/smoke/<timestamp>/. Run once:  uv run python e2e/smoke_network.py
"""
import json
import os
import time

from common import WORK, sha256, write_atomic, write_json, log
import btcheaders
import otsutil


def main():
    d = WORK / "smoke" / time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    f = d / "random32.bin"
    write_atomic(f, os.urandom(32))
    t0 = time.time()
    ots = otsutil.RealOts().stamp(f)
    dig, btc, pend = otsutil.parse(ots.read_bytes())
    stamp = {"file_sha256": sha256(f.read_bytes()).hex(), "proof_digest": dig.hex(), "bitcoin": len(btc),
             "pending": pend, "seconds": round(time.time() - t0, 1), "proof_bytes": len(ots.read_bytes())}
    assert dig == sha256(f.read_bytes()) and pend and not btc
    tip = btcheaders.tip()
    hs = btcheaders.fetch(range(tip - 5, tip + 1))
    pins = {h: otsutil.pin_of(v) for h, v in hs.items()}
    hdr = {"tip": tip, "heights": sorted(hs), "segment_qualifies": otsutil.qualifies(tip - 5, hs, pins),
           "pins": {str(h): p for h, p in pins.items()}}
    assert hdr["segment_qualifies"]
    write_json(d / "smoke.json", {"stamp": stamp, "headers": hdr})
    log(json.dumps({"stamp": stamp, "headers": {k: v for k, v in hdr.items() if k != "pins"}}))


if __name__ == "__main__":
    main()
