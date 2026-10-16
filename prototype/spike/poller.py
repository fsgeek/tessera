"""THROWAWAY spike step 2 poller: every 30 min for at most 24 h run `ots upgrade` on both proofs, log to ots-upgrade.log.
When both hold a Bitcoin attestation, run finalize.py (headers, pins, offline verify) until it succeeds."""
import subprocess, sys, time, json
from pathlib import Path
HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
LOG = HERE / "ots-upgrade.log"
OTS = "/home/tony/projects/tessera/.venv/bin/ots"
FILES = ["receipt-preimage.bin.ots", "dns-snapshot.json.ots"]
START = time.time(); LIMIT = 24 * 3600; EVERY = 1800
sys.path.insert(0, str(HERE.parents[0]))
from tessera_proto.real import ots as O

def log(s):
    with LOG.open("a") as f:
        f.write(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) + " " + s + "\n")

def state(fn):
    dtf = O.load((OUT / fn).read_bytes())
    ps = O.attestation_paths(dtf.timestamp)
    return [p.height for p in ps if p.kind == "bitcoin"], [p.calendar for p in ps if p.kind == "pending"]

log(f"poller start pid={__import__('os').getpid()}")
first_seen = {}
done = False
while time.time() - START < LIMIT:
    for fn in FILES:
        r = subprocess.run([OTS, "upgrade", fn], cwd=OUT, capture_output=True, text=True, timeout=300)
        btc_h, pend = state(fn)
        if btc_h and fn not in first_seen:
            first_seen[fn] = time.time()
            log(f"FIRST_BITCOIN_ATTESTATION {fn} heights={btc_h}")
        log(f"upgrade {fn} rc={r.returncode} bitcoin_heights={btc_h} pending={len(pend)} :: {(r.stdout+r.stderr).strip().replace(chr(10),' | ')[-300:]}")
    if all(f in first_seen for f in FILES) and (HERE / "finalize.py").exists():
        r = subprocess.run(["uv", "run", "python", str(HERE / "finalize.py")], cwd=HERE.parent, capture_output=True, text=True, timeout=900)
        log(f"finalize rc={r.returncode} :: {(r.stdout + r.stderr).strip()[-600:]}")
        if r.returncode == 0:
            log("COMPLETE"); done = True; break
    time.sleep(EVERY)
if not done:
    log("poller exit: not complete within limit")
