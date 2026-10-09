"""Provenance script (run once, 2026-10-07, network): fetch raw 80-byte Bitcoin mainnet headers from
the Blockstream Esplora API and archive them as a fixture. The tests never touch the network; they
check every archived header's proof of work and linkage themselves, so the API is not trusted for
anything the tests assert beyond "these are the headers at these heights" (which PoW + linkage +
the OTS merkle-root match corroborate)."""
import json, sys, time, urllib.request

API = "https://blockstream.info/api"

def get(path):
    with urllib.request.urlopen(API + path, timeout=30) as r:
        return r.read().decode()

def main(lo, hi, out):
    hs = {}
    for h in range(lo, hi + 1):
        bh = get(f"/block-height/{h}").strip()
        hs[h] = {"hash": bh, "header_hex": get(f"/block/{bh}/header").strip()}
        time.sleep(0.15)
    json.dump({"source": API, "fetched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "network": "bitcoin-mainnet", "headers": hs}, open(out, "w"), indent=1)

if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
