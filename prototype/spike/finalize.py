"""THROWAWAY spike (NETWORK, run by poller.py or by hand): once both OTS proofs hold a Bitcoin attestation and k=6 headers
exist, fetch the needed mainnet headers ONCE from two independent explorers (must agree), pin them by hash, write
out/bitcoin-headers.json + out/bitcoin-pins.json, write out/latency.json, then run the offline verifier in a fresh process.
Exit 0 only if the offline verifier passes every required group."""
import json, subprocess, sys, time, urllib.request
from pathlib import Path
HERE = Path(__file__).resolve().parent; OUT = HERE / "out"
sys.path.insert(0, str(HERE.parent))
from tessera_proto.real import ots as O, btc
K = 6
def get(base, path):
    with urllib.request.urlopen(urllib.request.Request(base + path, headers={"User-Agent": "tessera-spike"}), timeout=30) as r:
        return r.read().decode().strip()
A, B = "https://blockstream.info/api", "https://mempool.space/api"
heights = {}
for fn in ("receipt-preimage.bin.ots", "dns-snapshot.json.ots"):
    ps = O.attestation_paths(O.load((OUT / fn).read_bytes()).timestamp)
    heights[fn] = sorted(p.height for p in ps if p.kind == "bitcoin")
    if not heights[fn]: print("no bitcoin attestation yet:", fn); sys.exit(2)
tip = int(get(A, "/blocks/tip/height"))
need = sorted({x for hs in heights.values() for h in hs for x in range(h, h + K)})
if max(need) > tip: print(f"waiting for depth: need height {max(need)}, tip {tip}"); sys.exit(2)
hdrs, pins, src = {}, {}, {}
for h in need:
    ha = get(A, f"/block-height/{h}"); hb = get(B, f"/block-height/{h}")
    if ha != hb: print("EXPLORERS DISAGREE at", h, ha, hb); sys.exit(3)
    xa = get(A, f"/block/{ha}/header"); xb = get(B, f"/block/{hb}/header")
    if xa != xb: print("HEADER BYTES DISAGREE at", h); sys.exit(3)
    hdrs[h] = xa; pins[str(h)] = ha
    assert btc.Header.parse(bytes.fromhex(xa)).hash_hex == ha
(OUT / "bitcoin-headers.json").write_text(json.dumps({str(h): x for h, x in hdrs.items()}, indent=1))
(OUT / "bitcoin-pins.json").write_text(json.dumps({"version": "spike-pins-1", "network": "bitcoin-mainnet",
    "fetched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "sources": [A, B], "tip_at_fetch": tip,
    "rule": "every header used by a proof must equal the pinned hash here", "headers": pins}, indent=1))
def hdr(h): return btc.Header.parse(bytes.fromhex(hdrs[h]))
lat = {}
for fn, sub in (("receipt-preimage.bin.ots", "receipt-submit.epoch"), ("dns-snapshot.json.ots", "dns-submit.epoch")):
    s0, s1 = [int(x) for x in (OUT / sub).read_text().split()]
    h = heights[fn][0]
    lat[fn] = {"submitted_epoch": s0, "attested_heights": heights[fn], "first_attestation_height": h,
               "first_attestation_block_time": hdr(h).time, "submission_to_first_attestation_block_time_s": hdr(h).time - s0,
               "k6_height": h + K - 1, "k6_block_time": hdr(h + K - 1).time, "submission_to_k6_block_time_s": hdr(h + K - 1).time - s0}
(OUT / "latency.json").write_text(json.dumps(lat, indent=1)); print(json.dumps(lat, indent=1))
r = subprocess.run([sys.executable, str(HERE / "verify_offline.py")], capture_output=True, text=True)
(OUT / "verify-final.txt").write_text(r.stdout + r.stderr); print(r.stdout[-1500:], r.stderr[-500:]); sys.exit(r.returncode)
