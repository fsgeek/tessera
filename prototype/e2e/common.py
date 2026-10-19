"""Shared helpers for the V1 end-to-end issuer instrument (prototype/e2e).

INSTRUMENT CODE under A9.2: it lives under prototype/, service code never imports it, and it is evidence for nothing.
Every object it freezes is in the TEST namespace (see freeze.py); every key it makes is a TEST key.
"""
import base64
import hashlib
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent            # prototype/e2e
PROTO = HERE.parent                                # prototype
REPO = PROTO.parent                                # repository root
WORK = HERE / "work"                               # all mutable state lives here (git-ignored by convention)

for p in (REPO / "formal" / "p8" / "vectors", PROTO / "conformance", HERE):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import gen  # noqa: E402  P8 implementation A (encoders, rule O / rule R, DNS value)
import tcrypto as tc  # noqa: E402  TEST cryptography of the conformance universe
import universe as U  # noqa: E402  TEST universe (part format, Chain, Proof, trust/release stand-ins)

D = "wamason.com"
TXT_OWNER = "_tessera-v1." + D
DELTA, EPS, K = U.DELTA, U.EPS, U.K
ts, rfc3339 = U.ts, U.rfc3339


def sha256(b):
    return hashlib.sha256(b).digest()


def sha256hex(b):
    return hashlib.sha256(b).hexdigest()


def sha256d(b):
    return sha256(sha256(b))


def b64(b):
    return base64.b64encode(b).decode()


def b64d(s):
    return base64.b64decode(s, validate=True)


def jcs(v):
    return gen.jcs(v)


def now():
    return int(time.time())


def write_atomic(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_bytes(data if isinstance(data, bytes) else data.encode())
    os.replace(tmp, path)


def write_json(path, obj):
    write_atomic(path, json.dumps(obj, indent=1, sort_keys=True) + "\n")


def read_json(path):
    return json.loads(Path(path).read_text())


def log(*a):
    print("[e2e]", *a, flush=True)
