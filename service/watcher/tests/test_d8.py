"""D8: re-verification of COMPLETE receipts. The real first production receipt (docs/smoke/2026-11-16-first-receipt)
is verified by the frozen verifier's CLI, with explorers faked from the bundle's own headers (no network)."""
import json
import os
from pathlib import Path

import pytest

import fakes
from conftest import SMOKE, T0, Env
from tessera_watch import receipts as R
from tessera_watch import watcher as W

MAIN_INSTALL = Path("/home/tony/projects/tessera/service/verifier/install.json")
INSTALL = Path(os.environ.get("TESSERA_VERIFY_INSTALL_JSON") or (
    Path(__file__).resolve().parents[2] / "verifier" / "install.json"))
if not INSTALL.is_file():
    INSTALL = MAIN_INSTALL                                    # a worktree has no built verifier; use main's build
BUNDLE = (SMOKE / "receipt.json").read_bytes()
HEADERS = {int(h): bytes.fromhex(v) for h, v in json.loads(BUNDLE)["layers"][0]["headers"].items()}


def explorer(headers=HEADERS, broken=None, lie=None):
    def get(url):
        api, _, rest = url.partition("/block")
        if broken and api == broken:
            raise OSError("down")
        if rest.startswith("-height/"):
            h = int(rest.rsplit("/", 1)[-1])
            hdr = (lie if (lie and api == "https://b.example") else headers)[h]
            return R.pin_of(hdr)
        bh = rest.split("/")[1]
        for src in (headers, lie or {}):
            for v in src.values():
                if R.pin_of(v) == bh:
                    return v.hex()
        raise OSError("unknown block")
    return get


def real_verify(get):
    cli = lambda d: R.run_cli(d, install_json=INSTALL, timeout=300)          # noqa: E731
    return lambda bundle, window, catalog, as_of, explorers: R.verify(bundle, window, catalog, as_of, explorers,
                                                                      get=get, cli=cli)


def complete(env, bundle, rid="rid1", digest=None):
    digest = digest or fakes.sha(bundle)
    env.s3.put("results", f"result/{rid}/{digest}.json", bundle)
    env.ddb.put("REQ#" + rid, fakes.request(rid, "COMPLETE", T0 - 300, receipt_sha256=digest))
    return digest


def test_real_receipt_verifies_valid_strict_no_alarm():
    env = Env(verify=real_verify(explorer()))
    complete(env, BUNDLE)
    env.run()
    assert env.sns.sent == []
    t = env.traces()["trace/rid1.json"]
    assert t["verification"]["verdict"] == "VALID_STRICT" and t["anchor_heights"] == sorted(HEADERS)
    assert t["receipt_sha256"] == fakes.sha(BUNDLE) == "aca4dfb2c8abb3b2d970ee9d9ab10a5438704845a19e89e9d64f84e647ed9f83"


def test_tampered_receipt_alarms_d8():
    bad = bytearray(BUNDLE)
    i = BUNDLE.find(b'"a_sig":"') + 200
    bad[i] = ord("A") if bad[i] != ord("A") else ord("B")
    env = Env(verify=real_verify(explorer()))
    complete(env, bytes(bad))
    env.run()
    assert [json.loads(m["Message"])["detection"] for m in env.sns.sent] == ["D8"]
    assert env.codes()[0].startswith("VERDICT_") and env.codes()[0] != "VERDICT_VALID_STRICT"
    assert env.traces()["trace/rid1.json"]["verification"]["verdict"] != "VALID_STRICT"


def test_wrong_header_pins_do_not_verify():
    """An explorer pair that agrees on headers other than the bundle's: the receipt does not verify."""
    lie = {h: v[:4] + bytes(32) + v[36:] for h, v in HEADERS.items()}
    env = Env(verify=real_verify(explorer(headers=lie)))
    complete(env, BUNDLE)
    env.run()
    assert [json.loads(m["Message"])["detection"] for m in env.sns.sent] == ["D8"]


def test_explorers_disagree_is_unavailable_not_a_verdict():
    lie = {h: v[:4] + bytes(32) + v[36:] for h, v in HEADERS.items()}
    with pytest.raises(R.Unavailable) as e:
        R.explorer_headers(sorted(HEADERS), ["https://a.example", "https://b.example"], explorer(lie=lie))
    assert e.value.code == "EXPLORERS_DISAGREE"


def test_stored_bytes_must_hash_to_receipt_sha256(env):
    complete(env, b'{"layers":[]}', digest="0" * 64)
    env.run()
    assert env.codes() == ["RECEIPT_BYTES_DIGEST_MISMATCH"]


def test_missing_receipt_object(env):
    env.ddb.put("REQ#rid1", fakes.request("rid1", "COMPLETE", T0 - 300, receipt_sha256="1" * 64))
    env.run()
    assert env.codes() == ["RECEIPT_OBJECT_MISSING"]


def test_complete_without_digest(env):
    env.ddb.put("REQ#rid1", fakes.request("rid1", "COMPLETE", T0 - 300, receipt_sha256=None))
    env.run()
    assert env.codes() == ["COMPLETE_WITHOUT_RECEIPT_DIGEST"]


def test_valid_strict_stub_no_alarm(env):
    complete(env, b"bundle")
    env.run()
    assert env.sns.sent == [] and len(env.traces()) == 1


@pytest.mark.parametrize("verdict", ["INVALID", "UNVERIFIABLE", "VALID"])
def test_any_other_verdict_alarms(verdict):
    env = Env(verify=lambda *a, **k: {"verdict": verdict, "reason": "X", "heights": [], "T": None})
    complete(env, b"bundle")
    env.run()
    assert env.codes() == ["VERDICT_" + verdict]


def test_unavailable_check_is_retried_then_bounded():
    state = {"fail": True}

    def verify(*a, **k):
        if state["fail"]:
            raise R.Unavailable("EXPLORER_UNAVAILABLE")
        return {"verdict": "VALID_STRICT", "reason": "OK", "heights": [], "T": None}
    env = Env(verify=verify)
    complete(env, b"bundle")
    env.run()
    assert env.codes() == ["RECEIPT_CHECK_UNAVAILABLE"] and env.traces() == {}
    env.clock.t += 600
    env.run()
    assert env.codes() == ["RECEIPT_CHECK_UNAVAILABLE"]          # reported once per reason
    assert "rid1" in env.state()["pending"]
    env.clock.t = T0 + W.D8_GIVE_UP_S + 1
    env.run()
    assert env.codes() == ["RECEIPT_CHECK_UNAVAILABLE", "RECEIPT_UNCHECKED"]
    assert env.traces()["trace/rid1.json"]["verification"]["verdict"] == "UNCHECKED"


def test_unavailable_then_recovers_without_d8(env):
    calls = []

    def verify(*a, **k):
        calls.append(1)
        if len(calls) == 1:
            raise R.Unavailable("VERIFIER_REFUSED:INSTALL_RECORD_MISSING")
        return {"verdict": "VALID_STRICT", "reason": "OK", "heights": [], "T": None}
    env.verify = verify
    complete(env, b"bundle")
    env.run()
    env.clock.t += 600
    env.run()
    assert env.codes() == ["RECEIPT_CHECK_UNAVAILABLE"] and len(env.traces()) == 1


def test_verifier_refusal_code_is_bounded(tmp_path):
    def cli(d):
        return 2, "", "INSTALL_RECORD_MISSING\n"
    with pytest.raises(R.Unavailable) as e:
        R.verify(BUNDLE, Env().cfg.window, Env().cfg.catalog, "2026-11-22T00:00:00Z",
                 ["https://a.example", "https://b.example"], get=explorer(), cli=cli)
    assert e.value.code == "VERIFIER_REFUSED:INSTALL_RECORD_MISSING"

    def cli2(d):
        return 2, "", "INPUT_IO_ERROR: [Errno 2] /tmp/secret/path https://x?sig=abc"
    with pytest.raises(R.Unavailable) as e:
        R.verify(BUNDLE, Env().cfg.window, Env().cfg.catalog, "2026-11-22T00:00:00Z",
                 ["https://a.example", "https://b.example"], get=explorer(), cli=cli2)
    assert e.value.code == "VERIFIER_REFUSED:INPUT_IO_ERROR"


def test_verification_budget_leaves_receipts_pending(env):
    complete(env, b"bundle")
    env.make(remaining=lambda: 1000).run()
    assert "rid1" in env.state()["pending"] and env.traces() == {}
    env.run()
    assert env.state()["pending"] == {} and len(env.traces()) == 1


def test_catalog_must_be_the_frozen_one(tmp_path):
    p = tmp_path / "catalog.json"
    p.write_text("{}")
    with pytest.raises(R.Unavailable):
        R.load_catalog(p)
