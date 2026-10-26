#!/usr/bin/env python3
"""E10 materializer (concretizer): turns the vector specifications in formal/e10/vectors/ into concrete TEST-universe
fixtures, in the layout prototype/conformance/run.py consumes.

Oracle and construction are kept apart (A1.7 item 2):
  - the expected report of every executable subcase is DATA in the vector file (`subcases[].expected`: the six
    stable fields plus `utc_assessment`); this program copies it into the fixture's expected.json and never computes
    a verdict or reason;
  - the construction is CODE here (`BUILD[<subcase id>]`), through the TEST issuer's documented issue path
    (prototype/conformance/issue.py) plus named post-issue edits.
The only value this program checks against the issuer's own schedule is T / utc_upper_bound: where the subcase's
expected T is non-null and the fixture came from the issuer, T must equal nTime(h*) of the issuer plan and
utc_upper_bound must equal issue.expected_U (A10.1.1). A mismatch stops the run.

Usage (repository root):
  prototype/.venv/bin/python formal/e10/materialize.py [--out formal/e10/fixtures] [--only SUBID,SUBID]
  prototype/.venv/bin/python formal/e10/materialize.py --check      # rebuild into a temp dir, compare MANIFEST.json
Run against a verifier (here the independent verifier through the differential adapter):
  A="prototype/indep-verifier/.venv/bin/python prototype/differential/adapter.py"
  prototype/.venv/bin/python prototype/conformance/run.py --verifier "$A" --cases formal/e10/fixtures \\
      --json formal/e10/fixtures/RUN-INDEP.json
Everything built here is TEST material (synthetic chain, TEST keys, TEST release). It exercises the vector's
construction, not the AWS service; the live runs (20 Nov) are a separate obligation.
"""
import argparse
import base64
import copy
import hashlib
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CONF = ROOT / "prototype" / "conformance"
sys.path.insert(0, str(CONF))
import cases as C  # noqa: E402  (importing registers the 352 conformance builders; writes nothing)
import issue as I  # noqa: E402
import tcrypto as tc  # noqa: E402
import universe as U  # noqa: E402
from tcrypto import gen  # noqa: E402

VECTORS = HERE / "vectors"
HB, TB, DELTA, EPS = 900000, U.ts("2026-11-10T12:00:00Z"), U.DELTA, U.EPS
FIELDS = ("verdict", "reason", "T", "revocation", "historical_security", "standing")


# ------------------------------------------------------------------------------------------------ helpers
def b64(b):
    return base64.b64encode(b).decode()


def L(c):
    return c.container["layers"][0]


def rebuild(c):
    c.bundle = U.jcs(c.container)
    return c


def base():
    """A-a: the honest receipt as shipped."""
    return I.issue()


def post(fn, src=None):
    """Post-issue edit of a copy of `src` (default A-a): the L0 shape. The receipt proof is unchanged."""
    c = copy.deepcopy(src or base())
    fn(c)
    return rebuild(c)


def attest(common, fp):
    return gen.frame(gen.T_ATTEST, U.jcs({"common": common, "signer": {"key_fp": fp}}))


def set_asig(c, f0, s0, f1, s1):
    L(c)["a_sig"] = b64(gen.encode_anchor(f0, s0, f1, s1))


def conf(cid):
    """Reuse a conformance case's construction unchanged. Returns (result, installation, request)."""
    spec = next(s for s in C.CASES if s["id"] == cid)
    return spec["fn"](), spec["installation"], spec["request"]


def captor_value(c):
    return gen.dns_value(c.kms.fp_kms.split(":")[1], c.gpg.fp_gpg.split(":")[1], c.window[1], c.window[0]).encode()


def honest_value(c):
    C._honest_value(c)


CAPTOR = dict(kms_seed="e10-captor-kms", gpg_seed="e10-captor-gpg")


# ------------------------------------------------------------------------------------------------ builders
def _tmp(times, **kw):
    return lambda: I.issue(times=times, **kw)


def _content_edit(c):
    alt = dict(c.common, content={"TEST": "altered after signing"})
    return attest(alt, c.kms.fp_kms), attest(alt, c.gpg.fp_gpg)


def sp1_01_restamped():
    def sign(c):
        c.F_kms, c.F_gpg = _content_edit(c)          # frames changed after signing; signatures kept; A_sig stamped
    return I.issue(adversarial=True, hooks={"sign": sign})


def sp1_01_unstamped():
    def f(c):
        fk, fg = _content_edit(c)
        set_asig(c, fk, c.S_kms, fg, c.S_gpg)
    return post(f)


def sp1_02():
    def sign(c):
        payload = U.jcs({"common": c.common_kms, "signer": {"key_fp": c.kms.fp_kms}})
        c.S_kms = tc.pgp_sign(payload, c.kms, c.sig_time)
    return I.issue(adversarial=True, hooks={"sign": sign})


def sp1_03():
    def blob(c):                                      # git keeps the honest assertion; DNS names the captor's keys
        k, g = U.Keys.p256("kms-signer"), U.Keys.p256("gpg-signer", 1790000000)
        c.blob = gen.dns_value(k.fp_kms.split(":")[1], g.fp_gpg.split(":")[1], c.window[1], c.window[0]).encode()
    return I.issue(**CAPTOR, adversarial=True, hooks={"blob_value": blob})


def sp1_04():
    def value(c):                                     # DNS keeps the honest record; git names the captor's keys
        c._captor = captor_value(c)
        honest_value(c)

    def blob(c):
        c.blob = c._captor
    return I.issue(**CAPTOR, adversarial=True, hooks={"value": value, "blob_value": blob})


def sp2_01():
    def f(c):
        out = gen.header(gen.T_ANCHOR) + bytes([1])
        for part in (c.F_kms, c.S_kms):
            out += len(part).to_bytes(4, "big") + part
        L(c)["a_sig"] = b64(out)
    return post(f)


def sp2_02():
    def f(c):
        full = gen.encode_anchor(c.F_kms, c.S_kms, c.F_gpg, c.S_gpg)
        cut = len(gen.header(gen.T_ANCHOR)) + 1 + 4 + len(c.F_kms) + 4 + len(c.S_kms)
        L(c)["a_sig"] = b64(full[:cut])
    return post(f)


def sp2_03():
    return post(lambda c: set_asig(c, c.F_kms, c.S_kms, c.F_gpg, b""))


def _sp2_04_hooks():
    att = U.Keys.p256("e10-attacker-gpg", 1790000000)

    def keys(c):
        c.gpg_honest, c.gpg = c.gpg, att

    def mv(c):
        c.manifest_value["sset"] = [c.gpg_honest.fp_gpg]   # the honest manifest

    return {"keys": keys, "manifest_value": mv, "value": honest_value}


def sp2_04_restamped():
    return I.issue(adversarial=True, hooks=_sp2_04_hooks())


def sp2_04_unstamped():
    r = sp2_04_restamped()

    def f(c):
        L(c)["keys"]["gpg"] = L(r)["keys"]["gpg"]
        L(c)["possession"]["gpg"] = L(r)["possession"]["gpg"]
        set_asig(c, c.F_kms, c.S_kms, r.F_gpg, r.S_gpg)
    return post(f)


def sp2_05():
    def f(c):
        mv = copy.deepcopy(c.manifest_value)
        mv["sset"] = [U.Keys.p256("other-gpg", 1790000000).fp_gpg]
        L(c)["manifest"] = b64(gen.frame(gen.T_MANIFEST, U.jcs(mv)))
    return post(f)


def sp2_06_l3():
    def cs(c):
        c.common_gpg = dict(c.common, content={"TEST": "other content"})
    return I.issue(adversarial=True, hooks={"common_slots": cs})


def sp2_06_l0():
    r2 = I.issue(content={"TEST": "other content"})
    return post(lambda c: set_asig(c, c.F_kms, c.S_kms, r2.F_gpg, r2.S_gpg))


def sp3_01_l0():
    # E10R-05: the same receipt's S_kms (a service-key signature over F_kms, not F_manifest) as possession.kms.
    return post(lambda c: L(c)["possession"].__setitem__("kms", b64(c.S_kms)))


def cap_02():
    return post(lambda c: set_asig(c, c.F_kms, c.P_kms, c.F_gpg, c.S_gpg))


def cap_03():
    r2 = I.issue(content={"TEST": "receipt R2: other content"})
    return post(lambda c: set_asig(c, c.F_kms, r2.S_kms, c.F_gpg, c.S_gpg))


def cap_04():
    def poss(c):
        c.P_kms = I.kms_sign(c, c.kms.fp_kms.encode())
    return I.issue(adversarial=True, hooks={"possession": poss})


def e6a_02():
    def f(c):
        set_asig(c, c.F_kms, b"", c.F_gpg, b"")
        del L(c)["dns"], L(c)["git"]
    return post(f)


def e6a_03():
    def f(c):
        del L(c)["dns"], L(c)["git"]
    return post(f)


def e6a_04():
    src = I.issue(alg="X-UNKNOWN-ALG-1", adversarial=True)

    def f(c):
        set_asig(c, c.F_kms, b"", c.F_gpg, b"")
        del L(c)["dns"], L(c)["git"]
    return post(f, src)


def e6a_06():
    def f(c):
        cg = {k: v for k, v in c.common.items() if k != "alg"}
        set_asig(c, c.F_kms, c.S_kms, attest(cg, c.gpg.fp_gpg), c.S_gpg)
        del L(c)["dns"], L(c)["git"]
    return post(f)


def e6a_07():
    return post(lambda c: L(c).pop("a_sig"))


def tmp_09():
    return post(lambda c: L(c)["issuer_record"].__setitem__("delta_s", "999999999"))


def p7_04():
    return post(lambda c: set_asig(c, c.F_manifest, c.P_kms, c.F_gpg, c.S_gpg))


def g10_01():
    honest = base()

    def asig(c):
        c.A_sig = honest.A_sig                     # honest frames and signatures; captor manifest, keys, possession
    return I.issue(**CAPTOR, adversarial=True, hooks={"asig": asig})


def g10_02():
    honest = base()

    def mv(c):
        c.manifest_value = copy.deepcopy(honest.manifest_value)   # the honest manifest

    def asig(c):
        c.A_sig = honest.A_sig
    return I.issue(**CAPTOR, adversarial=True, hooks={"manifest_value": mv, "asig": asig})


def _g10_03_hooks(restamp):
    honest = base()

    def sign(c):
        c.S_kms, c.S_gpg = honest.S_kms, honest.S_gpg   # frames name the captor; honest signature bytes kept
    h = {"sign": sign}
    if not restamp:
        def rd(c):
            c.receipt_digest = hashlib.sha256(honest.A_sig).digest()   # the proof still covers the honest A_sig
        h["receipt_digest"] = rd
    return h


def g10_03_restamped():
    return I.issue(**CAPTOR, adversarial=True, hooks=_g10_03_hooks(True))


def g10_03_unstamped():
    return I.issue(**CAPTOR, adversarial=True, hooks=_g10_03_hooks(False))


def _embed(inner_id):
    def f():
        inner, _, _ = conf(inner_id)
        inner_bytes = inner.bundle if hasattr(inner, "bundle") else inner["bundle"]
        content = {"TEST": "opaque embedded receipt", "inner_b64": b64(inner_bytes)}
        c = I.issue(content=content)
        # harness check (not a verdict): extract the inner bytes from the OUTER BUNDLE's signed kms frame and
        # require byte identity with the standalone inner bundle
        a = base64.b64decode(json.loads(c.bundle)["layers"][0]["a_sig"])
        i = len(gen.header(gen.T_ANCHOR)) + 1
        fk = a[i + 4:i + 4 + int.from_bytes(a[i:i + 4], "big")]
        j = len(gen.header(gen.T_ATTEST)) + 2
        payload = fk[j + 4:j + 4 + int.from_bytes(fk[j:j + 4], "big")]
        got = base64.b64decode(json.loads(payload)["common"]["content"]["inner_b64"])
        assert got == inner_bytes, (inner_id, "embedded bytes changed")
        c.e10_extract_sha256 = hashlib.sha256(got).hexdigest()
        return c
    return f


def p7_02_reserialized():
    inner, _, _ = conf("L-07")
    c = copy.deepcopy(inner)
    c.bundle = U.jcs(json.loads(inner.bundle))       # the red bar: parse, then re-emit canonical JSON
    return c


def tmp_11():
    """Withhold ONLY the six receipt headers h*..h*+5 from the already-issued honest fixture (MZ-01): trust (pins
    included), release and every other member stay byte-identical to A-a."""
    c = copy.deepcopy(base())
    for h in range(HB + 24, HB + 30):
        del L(c)["headers"][str(h)]
    return rebuild(c)


BUILD = {
    # temporal (TEST chain times; L4)
    "E10-TMP-01": _tmp({HB + 29: TB + DELTA + 1}, adversarial=True),
    "E10-TMP-02": _tmp({HB + 24: TB + 129600, HB + 29: TB + 388800}, adversarial=True),
    "E10-TMP-03": _tmp({HB + 24: TB + DELTA + 1, HB + 29: TB + DELTA - 1}, adversarial=True),
    "E10-TMP-04": _tmp({HB + 29: TB + 1200 - 3600}),
    "E10-TMP-05": _tmp({HB + 24: TB - EPS}),
    "E10-TMP-06": _tmp({HB + 24: TB + DELTA, HB + 29: TB + DELTA}),
    "E10-TMP-07": lambda: I.issue(content={"TEST": "receipt-declared tolerances", "delta_s": "999999999",
                                           "epsilon_s": "999999999"}, times={HB + 29: TB + DELTA + 1},
                                  adversarial=True),
    "E10-TMP-08": lambda: I.issue(content={"TEST": "receipt-declared tolerances", "delta_s": "0", "epsilon_s": "0"},
                                  times={HB + 29: TB + DELTA}),
    "E10-TMP-09": tmp_09,
    "E10-TMP-10": base,
    "E10-TMP-11": tmp_11,
    "E10-TMP-11.control": base,
    "E10-TMP-12": lambda: I.issue(supply_remove=[HB + 29], adversarial=True),
    # P4
    "E10-P4-01": lambda: post(lambda c: L(c).pop("git")),
    "E10-P4-02": lambda: I.issue(receipt_branches=[{"kind": "pending"}], adversarial=True),
    "E10-P4-03.degraded": base,
    "E10-P4-03.strict-control": base,
    "E10-P4-04": "conf:A-d3",
    # E6a
    "E10-E6A-01.i": "conf:HY-b2-H",
    "E10-E6A-01.ii": "conf:HY-e1-C",
    "E10-E6A-02": e6a_02,
    "E10-E6A-03": e6a_03,
    "E10-E6A-04": e6a_04,
    "E10-E6A-05": "conf:L-03b",
    "E10-E6A-06": e6a_06,
    "E10-E6A-07": e6a_07,
    # S-P1
    "E10-SP1-01.unstamped": sp1_01_unstamped,
    "E10-SP1-01.restamped": sp1_01_restamped,
    "E10-SP1-02": sp1_02,
    "E10-SP1-03": sp1_03,
    "E10-SP1-04": sp1_04,
    # S-P2
    "E10-SP2-01": sp2_01,
    "E10-SP2-02": sp2_02,
    "E10-SP2-03": sp2_03,
    "E10-SP2-04.restamped": sp2_04_restamped,
    "E10-SP2-04.unstamped": sp2_04_unstamped,
    "E10-SP2-05": sp2_05,
    "E10-SP2-06.L3": sp2_06_l3,
    "E10-SP2-06.L0": sp2_06_l0,
    # S-P3 / possession / capstone
    "E10-SP3-01.L0": sp3_01_l0,
    "E10-SP3-01.POS-a": "conf:POS-a",
    "E10-POS-01": base,
    "E10-CAP-01": "conf:AUTH-i-T",
    "E10-CAP-02": cap_02,
    "E10-CAP-03": cap_03,
    "E10-CAP-04": cap_04,
    "E10-G10-01": g10_01,
    "E10-G10-02": g10_02,
    "E10-G10-03.restamped": g10_03_restamped,
    "E10-G10-03.unstamped": g10_03_unstamped,
    # P7 analogue
    "E10-P7-01.inner-A-a": "conf:A-a",
    "E10-P7-01.inner-KEY-a": "conf:KEY-a",
    "E10-P7-01.inner-L-07": "conf:L-07",
    "E10-P7-01.inner-L-09": "conf:L-09",
    "E10-P7-01.outer-A-a": _embed("A-a"),
    "E10-P7-01.outer-KEY-a": _embed("KEY-a"),
    "E10-P7-01.outer-L-07": _embed("L-07"),
    "E10-P7-01.outer-L-09": _embed("L-09"),
    "E10-P7-02.inner-L-07": "conf:L-07",
    "E10-P7-02.reserialized": p7_02_reserialized,
    "E10-P7-03.L-04": "conf:L-04",
    "E10-P7-03.L-05": "conf:L-05",
    "E10-P7-04": p7_04,
    # P9 (the bundles; the environment is the live harness's, see each vector's `sequence`)
    "E10-P9-01.A-a": "conf:A-a",
    "E10-P9-01.L-36b": "conf:L-36b",
    "E10-P9-01.L-09": "conf:L-09",
    "E10-P9-02.A-a": "conf:A-a",
    "E10-P9-02.L-36b": "conf:L-36b",
    "E10-P9-03.A-a": "conf:A-a",
}

# issuer-side TEST oracles (ISS-01..03): the TEST issuer's pre-ship decision, plus a success control
ISSUER = {
    "E10-ISS-01.test-refuse": dict(times={HB + 24: TB + DELTA + 1, HB + 29: TB + DELTA - 1}),
    "E10-ISS-01.test-control": dict(times={HB + 24: TB + DELTA, HB + 29: TB + DELTA}),
    "E10-ISS-02.test-refuse": dict(times={HB + 24: TB + 129600, HB + 29: TB + 388800}),
    "E10-ISS-02.test-control": dict(times={HB + 24: TB + 129600, HB + 29: TB + DELTA}),
    "E10-ISS-03.test-refuse": dict(supply_remove=[HB + 29]),
    "E10-ISS-03.test-control": dict(),
}


# ------------------------------------------------------------------------------------------------ writer
def load_subcases():
    out = []
    for f in sorted(VECTORS.glob("E10-*.json")):
        v = json.loads(f.read_text())
        for s in v.get("subcases", []):
            out.append((v, s))
    return out


def build(sid):
    b = BUILD[sid]
    if isinstance(b, str):
        return conf(b.split(":", 1)[1])
    return b(), None, None


def write_fixture(out, v, s):
    sid = s["id"]
    res, inst, conf_request = build(sid)
    exp = s["expected"]
    request = s.get("request", conf_request)
    d = out / sid
    d.mkdir(parents=True, exist_ok=True)
    if isinstance(res, dict):
        bundle = res["bundle"]
        honest = I.issue(installation=inst or "classical")
        trust_b, rel, ctx = honest.trust_bytes, honest.release, None
    else:
        bundle, trust_b, rel, ctx = res.bundle, res.trust_bytes, res.release, res
    # the one derived check: T and U against the issuer's own plan, where the fixture is issuer output
    if ctx is not None and exp["T"] is not None:
        assert U.rfc3339(ctx.T) == exp["T"], (sid, "T", U.rfc3339(ctx.T), exp["T"])
        Uv = I.expected_U(ctx)
        assert exp["utc_assessment"]["utc_upper_bound"] == U.rfc3339(Uv), (sid, "U", U.rfc3339(Uv))
    assert (exp["T"] is None) == (exp["utc_assessment"]["utc_upper_bound"] is None), (sid, "U null iff T null")
    (d / "bundle.json").write_bytes(bundle)
    (d / "trust.json").write_bytes(trust_b)
    (d / "release.json").write_bytes(U.jcs(rel))
    if inst == "hybrid":
        (d / "catalog.json").write_text(json.dumps(U.catalog("hybrid"), indent=1, sort_keys=True) + "\n")
    if request and request != "strict":
        (d / "request.txt").write_text(request + "\n")
    meta = {"id": sid, "vector": v["id"], "kind": "bundle", "group": "E10", "title": s.get("title", v["title"]),
            "construction": s["construction"], "coverage": s["coverage"], "cite": [], "derivation":
            "expected copied from formal/e10/vectors/" + v["id"] + ".json subcases[]", "ambiguities": [],
            "ambiguous_fields": []}
    if exp.get("detail"):
        meta["detail"] = exp["detail"]
    if inst:
        meta["installation"] = inst
    if ctx is not None and hasattr(ctx, "preship"):
        meta["issuer_preship"] = ctx.preship
    if hasattr(res, "e10_extract_sha256"):
        meta["embedded_inner_sha256"] = res.e10_extract_sha256
    body = {f: exp[f] for f in FIELDS}
    body["utc_assessment"] = exp["utc_assessment"]
    body["_meta"] = meta
    (d / "expected.json").write_text(json.dumps(body, indent=1, sort_keys=True) + "\n")


def write_issuer(out, sid, kw):
    d = out / sid
    d.mkdir(parents=True, exist_ok=True)
    try:
        c = I.issue(**kw)
        r = {"ships": True, "preship": c.preship, "T": U.rfc3339(c.T)}
    except I.IssueRefused as e:
        c = I.issue(adversarial=True, **kw)
        r = {"ships": False, "refusal": str(e), "preship": c.preship}
    r["_meta"] = {"id": sid, "kind": "issuer_oracle", "issue_kwargs": {k: (
        {str(h): U.rfc3339(t) for h, t in v.items()} if k == "times" else v) for k, v in kw.items()},
        "note": "TEST issuer (prototype/conformance/issue.py) pre-ship decision only; not the AWS issuer. run.py "
                "skips this directory (no expected.json)."}
    (d / "issuer-oracle.json").write_text(json.dumps(r, indent=1, sort_keys=True) + "\n")


def manifest(out):
    files = {}
    for p in sorted(out.rglob("*")):
        if p.is_file() and p.name not in ("MANIFEST.json", "RUN-INDEP.json"):
            files[str(p.relative_to(out))] = hashlib.sha256(p.read_bytes()).hexdigest()
    src = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
           for p in [Path(__file__).resolve(), *sorted(VECTORS.glob("*.json")), CONF / "issue.py",
                     CONF / "cases.py", CONF / "universe.py", CONF / "tcrypto.py"]}
    return {"schema": "tessera-e10-fixtures/1", "sources": src, "files": files}


def materialize(out, only=None):
    out.mkdir(parents=True, exist_ok=True)
    subs = load_subcases()
    ids = [s["id"] for _, s in subs]
    assert len(ids) == len(set(ids)), "duplicate subcase id"
    missing = [i for i in ids if i not in BUILD] + [i for i in BUILD if i not in ids]
    assert not missing, ("subcase/builder mismatch", missing)
    for v, s in subs:
        if only and s["id"] not in only:
            continue
        write_fixture(out, v, s)
        print("fixture", s["id"], flush=True)
    for sid, kw in ISSUER.items():
        if only and sid not in only:
            continue
        write_issuer(out, sid, kw)
        print("issuer ", sid, flush=True)
    m = manifest(out)
    (out / "MANIFEST.json").write_text(json.dumps(m, indent=1, sort_keys=True) + "\n")
    return m


RUN_RECORD = "RUN-INDEP.json"    # explicit exclusion: a saved execution record, not a generated file


def hash_dir(out):
    """Every file actually present under `out`, relative path -> sha256, excluding MANIFEST.json and the run record."""
    return {str(p.relative_to(out)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(out.rglob("*")) if p.is_file() and p.name not in ("MANIFEST.json", RUN_RECORD)}


def check_dirs(out):
    """Returns a report dict: existing bytes vs saved MANIFEST (changed/missing/unexpected), then saved vs fresh."""
    want = json.loads((out / "MANIFEST.json").read_text())
    have = hash_dir(out)
    r = {"changed": sorted(k for k in have if k in want["files"] and have[k] != want["files"][k]),
         "missing": sorted(k for k in want["files"] if k not in have),
         "unexpected": sorted(k for k in have if k not in want["files"])}
    with tempfile.TemporaryDirectory(prefix="e10-check-") as t:
        got = materialize(Path(t))
    r["files_differing"] = sorted(k for k in set(want["files"]) | set(got["files"])
                                  if want["files"].get(k) != got["files"].get(k))
    r["sources_differing"] = sorted(k for k in want["sources"] if want["sources"][k] != got["sources"].get(k))
    return r


def check(out):
    r = check_dirs(out)
    print(json.dumps(r, indent=1))
    return 1 if any(r.values()) else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(HERE / "fixtures"))
    ap.add_argument("--only")
    ap.add_argument("--check", action="store_true", help="hash --out's files, validate against its saved MANIFEST, "
                    "then compare with a fresh build in a temp dir (changed/missing/unexpected files all fail)")
    a = ap.parse_args()
    only = set(a.only.split(",")) if a.only else None
    if a.check:
        sys.exit(check(Path(a.out)))
    m = materialize(Path(a.out), only)
    print(f"{len(m['files'])} files; MANIFEST.json written")


if __name__ == "__main__":
    main()
