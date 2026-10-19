"""Unit tests of the e2e instrument pieces, offline. Real-data tests read archived spike captures only."""
import json
import time

import pytest

from common import PROTO, U, gen, b64d, sha256
import dnssnap
import freeze
import otsutil
import repo as R
import trustcfg


# ------------------------------------------------------------------------------------------------ freeze
def test_freeze_assembles_and_agrees(workdir):
    out = freeze.assemble("HEAD", workdir / "freeze")
    assert freeze.check_agreement(out)
    o = freeze.load(out)
    parts = freeze.parse_parts(o["spec.bin"])
    assert [p for p, _ in parts] == sorted(freeze.SPEC_PATHS, key=str.encode)
    assert o["record"]["namespace"] == "TEST" and "TEST" in o["catalog"]
    assert o["catalog"]["alg"] == gen.ALG_HYBRID
    assert b"TEST ONLY" in o["preamble.bin"]
    deps = json.loads(o["dependency-manifest.json"])
    assert deps["format"] == "tessera-v1-deps/1" and [e["id"] for e in deps["entries"]] == sorted(
        e["id"] for e in deps["entries"])


def test_part_format_rejects_bad_header():
    with pytest.raises(ValueError):
        freeze.parse_parts(b"tessera-v1-part a b 01\nx\n")


# ------------------------------------------------------------------------------------------------ OTS
def _real_spike():
    hdrs = {int(h): bytes.fromhex(v) for h, v in json.loads((PROTO / "spike/out/bitcoin-headers.json").read_text()).items()}
    pins = {int(h): v for h, v in json.loads((PROTO / "spike/out/bitcoin-pins.json").read_text())["headers"].items()}
    return hdrs, pins


def test_real_mainnet_proof_selection_and_txid():
    """A real calendar proof (spike, 2026-10-09) with its archived mainnet headers: lowest-height selection,
    transaction shape and merkle suffix, digest = SHA-256 of the stamped file."""
    hdrs, pins = _real_spike()
    raw = (PROTO / "spike/out/receipt-preimage.bin.ots").read_bytes()
    d, btc, pend = otsutil.parse(raw)
    assert d == sha256((PROTO / "spike/out/receipt-preimage.bin").read_bytes())
    h, T, conf, atts, contra = otsutil.select(btc, hdrs, pins)
    assert h == 970687 and not contra and atts and pend
    txid = otsutil.path_tx(atts[0])
    assert len(txid) == 64
    assert T == int.from_bytes(hdrs[970687][68:72], "little")


def test_ots_grammar_rejections():
    hdrs, pins = _real_spike()
    raw = (PROTO / "spike/out/receipt-preimage.bin.ots").read_bytes()
    with pytest.raises(otsutil.OtsError):
        otsutil.parse(raw + b"\x00")                         # trailing bytes
    with pytest.raises(otsutil.OtsError):
        otsutil.parse(b"X" + raw[1:])                        # magic


def test_selection_without_headers_is_none():
    raw = (PROTO / "spike/out/receipt-preimage.bin.ots").read_bytes()
    _, btc, _ = otsutil.parse(raw)
    assert otsutil.select(btc, {}, {})[0] is None


def test_stub_chain_resumes_from_disk(workdir):
    f = workdir / "x.bin"
    f.write_bytes(b"hello")
    s = otsutil.StubOts(workdir / "stub.json")
    ots = s.stamp(f)
    assert otsutil.parse(ots.read_bytes())[1] == []          # pending only
    s.advance(6)
    s2 = otsutil.StubOts(workdir / "stub.json")              # a new process would do this
    ok, _ = s2.upgrade(ots)
    d, btc, _ = otsutil.parse(ots.read_bytes())
    assert ok and d == sha256(b"hello") and btc[0].height == 950001
    hdrs = s2.headers(range(950001, 950007))
    h, *_ = otsutil.select(btc, hdrs, {k: otsutil.pin_of(v) for k, v in hdrs.items()})
    assert h == 950001 and otsutil.path_tx(btc[0])


# ------------------------------------------------------------------------------------------------ DNS
VALUE = gen.dns_value("ab" * 32, "cd" * 32, "2026-12-01T00:00:00Z", "2026-10-01T00:00:00Z").encode()


def test_stub_conversion_equals_universe_serialization():
    t = int(time.time())
    cap = dnssnap.stub_capture(VALUE, t)
    body = dnssnap.convert(cap)
    assert body == U.serialize_groups(dnssnap.stub_hierarchy(VALUE, t))
    res = dnssnap.validate(body, dnssnap.stub_root_rdatas(), t)
    assert res["ok"] and res["value"] == VALUE and res["wildcard_free"]
    assert not dnssnap.validate(body, dnssnap.stub_root_rdatas(), t + 40 * 86400)["ok"]   # expired witnesses
    assert not dnssnap.validate(body, [U.zkey("other", 8, 257).rdata()], t)["ok"]          # untrusted root


def test_real_capture_converts_and_validates():
    """The archived live capture of 2026-10-12 (root signed by KSK-2024): root -> wamason.com DNSKEY converts to
    §15.3 groups and validates at its capture time under the real KSK-2024 RDATA from that capture."""
    cap = json.loads((PROTO / "spike/out-ksk2024/dns-snapshot.json").read_text())
    q = dnssnap.QUERIES[:5]
    body = dnssnap.convert(cap, q)
    roots = [r for _, _, rds, _ in dnssnap.groups(body)[:1] for r in rds if r[:2] == b"\x01\x01"]
    res = dnssnap.validate(body, roots, cap["captured_start"], q)
    assert res["ok"], res["errors"]
    assert [w["alg"] for w in res["witnesses"]] == [8, 8, 13, 13, 13]
    assert res["window"][0] <= cap["captured_start"] <= res["window"][1]


def test_wildcard_detected():
    t = int(time.time())
    gs = dnssnap.stub_hierarchy(VALUE, t)
    gs[-1].sigs[0].labels = 2           # TXT RRSIG with Labels < owner label count
    body = U.serialize_groups(gs)
    assert not dnssnap.wildcard_free(body)
    assert not dnssnap.validate(body, dnssnap.stub_root_rdatas(), t)["ok"]


# ------------------------------------------------------------------------------------------------ repository
def test_assertion_value_rules():
    v = R.assertion_value("ab" * 32, "cd" * 32, "2026-10-20T00:00:00Z", "2027-01-18T00:00:00Z")
    assert len(v) == 255 and not v.endswith(b"\n")
    with pytest.raises(R.RepoError):
        R.assertion_value("ab" * 32, "cd" * 32, "2026-10-20T00:00:00Z", "2027-01-19T00:00:01Z")   # > 90 days


def test_repo_key_commit_and_tamper(workdir):
    key = R.make_key(workdir / "key")
    assert key["gnupghome"].startswith(str(workdir))
    ev = R.commit_assertion(key, workdir / "repo", VALUE, workdir / "ev")
    R.stop_agent(key)
    c = (workdir / "ev" / "commit.bin").read_bytes()
    root, sub, blob = ((workdir / "ev" / n).read_bytes() for n in ("tree-root.bin", "tree-sub.bin", "blob.bin"))
    assert U.git_id("commit", c).hex() == ev["commit_id"] and blob == VALUE
    assert (workdir / "ev" / "git-stamp.txt").read_bytes() == (ev["commit_id"] + "\n").encode()
    bad = c.replace(b"TEST: publish", b"TEST: publisH")
    with pytest.raises(R.RepoError):
        R.check_commit(bad, root, sub, blob, key)


# ------------------------------------------------------------------------------------------------ trust
def test_real_root_ksks_from_archive_parse_in_indep_policy():
    if not (trustcfg.ARCHIVE / "sources.json").exists():
        pytest.skip("root anchors not archived (run: e2e/trustcfg.py fetch-roots)")
    import sys
    sys.path.insert(0, str(PROTO / "indep-verifier"))
    from policy import parse_trust
    ks = trustcfg.roots()
    assert [e["name"] for e in ks] == ["KSK-2017", "KSK-2024"]
    assert all(len(e["sources"]) >= 2 for e in ks)     # IANA XML plus at least one archived live RRset
    body = U.Keys.p256("e2e-test-repo", 1790000000).pgp_body
    entry = trustcfg.repo_entry(body, "2026-10-01T00:00:00Z", "TEST", "0" * 64, "test:")
    tb = trustcfg.build({970687: "00" * 32}, "2026-10-19T00:00:00Z", ks, [entry])
    cfg = parse_trust(tb)
    assert cfg["root_ksks"][1]["key_tag"] == "38696" and cfg["_pins"] == {970687: "00" * 32}
    assert b64d(cfg["root_ksks"][0]["dnskey_rdata"])[:4] == b"\x01\x01\x03\x08"
