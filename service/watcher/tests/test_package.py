"""Packaging: the Lambda layout matches lambda_app, the staged sources hold no issuer code, the wheels are locked with
hashes, the whole build (resolved wheels included) is deterministic, and the install-record check refuses a record
that is not this package's (review M8)."""
import importlib.util
import json
import shutil
import zipfile
from pathlib import Path

import pytest

from tessera_watch import lambda_app, receipts

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("watch_package", ROOT / "package.py")
package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package)


def test_binary_path_matches_lambda_app():
    assert package.LAMBDA_BINARY == lambda_app.SHA1DC_BINARY


def test_staged_sources_layout_and_no_issuer_code(tmp_path):
    stage = tmp_path / "stage"
    stage.mkdir()
    package.stage_sources(stage)
    tops = {p.name for p in stage.iterdir()}
    assert tops == {"tessera_watch", "tessera_verify", "freeze-v1", "config"}
    assert not list(stage.rglob("tessera_issue*"))
    frozen = {p.name for p in (stage / "freeze-v1" / "objects").iterdir()}
    assert frozen == {p.name for p in package.FROZEN.iterdir()}       # the whole frozen tree, as the issuer stages it
    assert receipts.load_catalog(stage / "freeze-v1" / "objects" / "catalog.json")
    assert receipts.load_window(stage / "config" / "window.json")["not_after"] == "2027-02-01T00:00:00Z"


def test_zip_is_deterministic(tmp_path):
    stage = tmp_path / "stage"
    stage.mkdir()
    package.stage_sources(stage)
    a, b = tmp_path / "a.zip", tmp_path / "b.zip"
    assert package.write_zip(stage, a) == package.write_zip(stage, b)
    with zipfile.ZipFile(a) as z:
        names = z.namelist()
        assert names == sorted(names) and all(i.date_time == (1980, 1, 1, 0, 0, 0) for i in z.infolist())


def test_config_from_env_reads_the_packaged_window_and_catalog(tmp_path, monkeypatch):
    stage = tmp_path / "stage"
    stage.mkdir()
    package.stage_sources(stage)
    monkeypatch.setattr(lambda_app, "TASK", stage)
    cfg = lambda_app.config_from_env({"ACCOUNT_ID": "1", "KMS_KEY_ARN": "arn:aws:kms:us-east-2:1:key/k",
                                      "KMS_ALIASES": "alias/tessera-v1-kms", "SIGNER_ROLE_ARN": "arn:role",
                                      "EXPLORERS": '["https://a", "https://b"]', "CLIENT_KEY_IDS": '{"x": "id"}'})
    assert cfg.kms_aliases == ("alias/tessera-v1-kms",) and cfg.explorers == ("https://a", "https://b")
    assert cfg.window["not_after"] == "2027-02-01T00:00:00Z" and cfg.client_key_ids == {"x": "id"}
    assert cfg.retain_until == "2028-03-07T00:00:00Z"                  # from the packaged window, not the environment


def test_wheels_are_locked_with_hashes_and_installed_only_from_the_lock(tmp_path):
    lines = package.LOCK.read_text().splitlines()
    pins = [x.split(" ")[0] for x in lines if x and not x.startswith((" ", "#"))]
    assert pins == ["cffi==2.1.1", "cryptography==50.0.2", "pycparser==3.12"]
    for pin in pins:
        block = lines[lines.index(pin + " \\") + 1:]
        assert block[0].strip().startswith("--hash=sha256:"), pin
    cmd = package.install_command(tmp_path)
    assert "--require-hashes" in cmd and "--no-deps" in cmd and cmd[cmd.index("-r") + 1] == str(package.LOCK)
    assert "cryptography==50.0.2" in (ROOT.parent / "verifier" / "requirements.txt").read_text()


MAIN_INSTALL = Path("/home/tony/projects/tessera/service/verifier/install.json")


def local_install():
    return package.INSTALL_RECORD if Path(package.INSTALL_RECORD).is_file() else MAIN_INSTALL


@pytest.mark.skipif(shutil.which("uv") is None or not local_install().is_file(), reason="needs uv and a built verifier")
def test_full_build_with_resolved_wheels_is_deterministic(tmp_path, monkeypatch):
    monkeypatch.setattr(package, "INSTALL_RECORD", local_install())
    a, b = package.build(tmp_path / "a.zip"), package.build(tmp_path / "b.zip")
    assert a == b
    with zipfile.ZipFile(tmp_path / "a.zip") as z:
        names = z.namelist()
    assert any(n.startswith("cryptography-50.0.2.dist-info/") for n in names)
    assert any(n.startswith("cffi-2.1.1.dist-info/") for n in names)
    assert package.LAMBDA_BINARY.removeprefix("/var/task/") in names


def good_record(monkeypatch, tmp_path):
    monkeypatch.setattr(package, "INSTALL_RECORD", local_install())
    local = json.loads(local_install().read_text())
    rec = dict(local, sha1dc_binary=package.LAMBDA_BINARY)
    return rec


@pytest.mark.skipif(not local_install().is_file(), reason="needs a built verifier")
@pytest.mark.parametrize("change", [None, "fields", "format", "binary_path", "binary_sha", "python", "unicode_version",
                                    "commit"])
def test_install_record_check(change, monkeypatch, tmp_path):
    rec = good_record(monkeypatch, tmp_path)
    if change == "fields":
        rec["extra"] = 1
    elif change == "format":
        rec["format"] = "tessera-v1-install/0"
    elif change == "binary_path":
        rec["sha1dc_binary"] = "/tmp/sha1dcsum"
    elif change == "binary_sha":
        rec["sha1dc_binary_sha256"] = "0" * 64
    elif change == "python":
        rec["python"] = "3.13"
    elif change == "unicode_version":
        rec["unicode_version"] = "15.0.0"
    elif change == "commit":
        rec["sha1dc_upstream_commit"] = "0" * 40
    p = tmp_path / "install.json"
    p.write_text(json.dumps(rec))
    if change is None:
        assert package.check_install_record(p) == rec
    else:
        with pytest.raises(SystemExit):
            package.check_install_record(p)


def test_selfcheck_reports_the_verifiers_startup_refusal(tmp_path):
    check = lambda_app.selfcheck(str(tmp_path / "absent.json"))
    assert check() in ("INSTALL_RECORD_MISSING", "RUNTIME_UNSUPPORTED", "UNICODE_TABLES_UNSUPPORTED")
    p = tmp_path / "install.json"
    p.write_text(json.dumps({"format": "tessera-v1-install/1"}))
    assert lambda_app.selfcheck(str(p))() in ("INSTALL_RECORD_INVALID", "RUNTIME_UNSUPPORTED",
                                              "UNICODE_TABLES_UNSUPPORTED")


def test_a_failed_selfcheck_is_reported_once_and_withholds_the_heartbeat(env):
    env.selfcheck = lambda: "UNICODE_TABLES_UNSUPPORTED"
    env.run()
    env.clock.t += 600
    env.run()
    assert env.codes() == ["VERIFIER_SELF_CHECK_FAILED"] and env.cw.beats == []
    env.selfcheck = lambda: None
    env.clock.t += 600
    env.run()
    assert len(env.cw.beats) == 1
