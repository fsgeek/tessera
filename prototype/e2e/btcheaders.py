"""Mainnet header fetch with two-source agreement (the logic of prototype/spike/finalize.py).

Each header is fetched from two independent explorers; the block hash at the height and the raw 80 header bytes
must agree, and the bytes must hash to that block hash. Network: the real run and the one smoke test only.
"""
import urllib.request

from otsutil import pin_of

SOURCES = ("https://blockstream.info/api", "https://mempool.space/api")


class HeaderDisagreement(Exception):
    pass


def _get(base, path):
    req = urllib.request.Request(base + path, headers={"User-Agent": "tessera-e2e-instrument"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode().strip()


def tip():
    a, b = (int(_get(s, "/blocks/tip/height")) for s in SOURCES)
    return min(a, b)


def fetch(heights):
    """{height: 80-byte header} for every height, two sources agreeing."""
    out = {}
    for h in sorted(set(heights)):
        ha, hb = (_get(s, f"/block-height/{h}") for s in SOURCES)
        if ha != hb:
            raise HeaderDisagreement(f"block hash at {h}: {ha} vs {hb}")
        xa, xb = (_get(s, f"/block/{ha}/header") for s in SOURCES)
        if xa != xb:
            raise HeaderDisagreement(f"header bytes at {h}")
        hdr = bytes.fromhex(xa)
        if len(hdr) != 80 or pin_of(hdr) != ha:
            raise HeaderDisagreement(f"header at {h} does not hash to its block hash")
        out[h] = hdr
    return out
