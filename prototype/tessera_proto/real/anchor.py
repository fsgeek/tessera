"""Verifier stage (h) and standing step 8 over a real-format OTS anchor. THROWAWAY.

Same check ids and semantics as the stub (`verifier._temporal`), with these real-mechanism rules:

  V33a  the OTS proof's file digest equals this receipt's digest (G-19's two-frame preimage, kept),
        and at least one BitcoinBlockHeaderAttestation's merkle root equals the bundled header's.
        A proof holding only PendingAttestations cannot be evaluated: UNVERIFIABLE (ANCHOR_PENDING_ONLY).
        A proof usually holds SEVERAL Bitcoin attestations (one per calendar, at different heights).
        The spec's `anchor_time` is singular; this module takes the EARLIEST verified attestation
        (the strongest true "existed by" statement) and records the others. GUESS G-55.
        If the bundle names a txid, it must be a transaction on the chosen attestation's path (G-42).
  V37   headers h..h+k-1 present in the bundle (R-3.48 candidate: the k-header segment is embedded).
  V38   two policies (TrustConfig.header_policy):
          "pin-every-header" -- phase 1's G-31: every header's hash equals the store's pin
          "checkpoint+pow"   -- R-3.48 candidate: headers link to a pinned header, each meets its
                                own nBits target, nBits constant inside the retarget period
        Both also require linkage and PoW. On REGTEST difficulty PoW proves nothing; on mainnet it does.
  V33-V36 as the stub, with anchor_time = nTime(h), confirmed_at = nTime(h+k-1).
"""
from __future__ import annotations

import base64

from . import btc, ots

PASS, FAIL, UNPERF = "pass", "fail", "unperformable"


def _headers(anchor: dict) -> dict[int, btc.Header]:
    out = {}
    for h, hx in (anchor.get("headers_hex") or {}).items():
        try:
            out[int(h)] = btc.Header.parse(bytes.fromhex(hx))
        except ValueError:
            pass
    return out


def evaluate(anchor: dict, digest_hex: str, store: dict[int, str], k: int, policy: str) -> dict:
    """Pure evaluation of an OTS anchor; returns a dict of check outcomes and facts."""
    r: dict = {"checks": {}, "facts": {}}
    c = r["checks"]
    try:
        dtf = ots.load(base64.b64decode(anchor["ots_b64"]))
    except Exception:  # noqa: BLE001
        c["V33a"] = (FAIL, "ANCHOR_PROOF_MALFORMED")
        return r
    hs = _headers(anchor)
    chk = ots.check(dtf, None, hs, bytes.fromhex(digest_hex))
    bit = [b for b in chk.bitcoin]
    r["facts"]["ots"] = {"bitcoin_attestations": [b["height"] for b in bit], "pending": chk.pending,
                         "verified": [b["height"] for b in chk.verified()]}
    if not chk.file_digest_ok:
        c["V33a"] = (FAIL, "ANCHOR_NOT_OVER_THIS_RECEIPT")
        return r
    if not bit:
        c["V33a"] = (UNPERF, "ANCHOR_PENDING_ONLY")
        return r
    if not any(b["header_present"] for b in bit):
        c["V37"] = (UNPERF, "HEADERS_UNAVAILABLE")
        c["V33a"] = (UNPERF, "ANCHOR_BLOCK_HEADER_UNAVAILABLE")
        return r
    e = chk.earliest()
    if e is None:
        c["V33a"] = (FAIL, "ANCHOR_MERKLE_ROOT_MISMATCH")
        return r
    h = e["height"]
    if anchor.get("txid") and anchor["txid"] not in e["txids"]:
        c["V33a"] = (FAIL, "TXID_NOT_ON_ATTESTATION_PATH")
        return r
    need = list(range(h, h + k))
    if any(x not in hs for x in need):
        c["V37"] = (UNPERF, "HEADERS_UNAVAILABLE")
        c["V33a"] = (PASS, "")
        return r
    c["V37"] = (PASS, "")
    ok, why = btc.check_segment(hs, h, h + k - 1)
    if not ok:
        c["V38"] = (FAIL if not why.startswith("RETARGET") else UNPERF, why)
    elif policy == "pin-every-header":
        bad = [x for x in need if x in store and store[x] != hs[x].hash_hex]
        missing = [x for x in need if x not in store]
        c["V38"] = (FAIL, "HEADER_STORE_CONFLICT") if bad else \
            (UNPERF, "HEADER_NOT_IN_TRUST_STORE") if missing else (PASS, "")
    elif policy == "checkpoint+pow":
        bad = [x for x in need if x in store and store[x] != hs[x].hash_hex]
        linked = (h - 1) in store and hs[h].prev[::-1].hex() == store[h - 1]
        pinned_inside = any(x in store for x in need)
        c["V38"] = (FAIL, "HEADER_STORE_CONFLICT") if bad else \
            (PASS, "EXTENDED_BY_POW_FROM_PINNED_HEADER") if (linked or pinned_inside) else \
            (UNPERF, "SEGMENT_NOT_LINKED_TO_ANY_PINNED_HEADER")
    else:
        raise ValueError(policy)
    c["V33a"] = (PASS, "")
    r["facts"].update(anchor_time=hs[h].time, confirmed_at=hs[h + k - 1].time, height=h,
                      mtp=btc.median_time_past(hs, h))
    return r


def temporal(anchor, frames, common, trust, policy, cks, facts, prefix=""):
    """Drop-in for verifier._temporal when anchor['format'] == 'ots-bitcoin'."""
    from .. import objects
    delta = policy.delta if policy.delta is not None else trust.delta
    eps = policy.epsilon if policy.epsilon is not None else trust.epsilon
    k = trust.k
    pid = lambda x: f"{prefix}{x}"  # noqa: E731
    try:
        declared = objects.parse_ts(common.get("declared_issue_time", ""))
        cks.add(pid("TIME"), PASS)
    except ValueError:
        cks.add(pid("TIME"), FAIL, "DECLARED_TIME_MALFORMED")
        return
    r = evaluate(anchor, objects.receipt_digest(frames), trust.header_store, k,
                 getattr(trust, "header_policy", "pin-every-header"))
    for cid, (st, why) in r["checks"].items():
        cks.add(pid(cid), st, why)
    facts["ots"] = r["facts"].get("ots")
    if "anchor_time" not in r["facts"]:
        return
    at, ca = r["facts"]["anchor_time"], r["facts"]["confirmed_at"]
    facts["anchor_time"], facts["confirmed_at"], facts["declared"] = at, ca, declared
    cks.add(pid("V33"), PASS if declared - eps <= at else FAIL, "" if declared - eps <= at else "P5_ANCHOR_BEFORE_WINDOW")
    cks.add(pid("V34"), PASS if at <= declared + delta else FAIL, "" if at <= declared + delta else "P5_ANCHOR_AFTER_WINDOW")
    cks.add(pid("V35"), PASS if ca <= declared + delta else FAIL, "" if ca <= declared + delta else "P5_CONFIRMATION_LATE")
    cks.add(pid("V36"), PASS)


def tlr_anchor_ok(anchor: dict, tlr_frame: bytes, dterm: int, trust) -> bool:
    from .. import objects
    r = evaluate(anchor, objects.receipt_digest([tlr_frame]), trust.header_store, trust.k,
                 getattr(trust, "header_policy", "pin-every-header"))
    if any(st != PASS for st, _ in r["checks"].values()) or "anchor_time" not in r["facts"]:
        return False
    at, ca = r["facts"]["anchor_time"], r["facts"]["confirmed_at"]
    return dterm - trust.epsilon <= at <= dterm + trust.delta and ca <= dterm + trust.delta
