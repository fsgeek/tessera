"""Deployment packaging: the install-facts bootstrap (the Lambda's install.json is generated where it runs, as
install.sh does on any other machine) and the package builder's checks. Building the full zip downloads the Linux
wheel, so that path is exercised by package.py itself, not here."""
import hashlib
import json
import sys
import zipfile
from pathlib import Path

import pytest

from tessera_issue import lambda_app

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import package  # noqa: E402

VERIFIER_INSTALL = HERE.parent / "verifier" / "install.json"


def test_install_facts_event_answers_without_building_the_issuer(monkeypatch, tmp_path):
    binary = tmp_path / "sha1dcsum"
    binary.write_bytes(b"not run")
    monkeypatch.setattr(lambda_app, "SHA1DC_BINARY", str(binary))
    monkeypatch.setattr(lambda_app, "_issuer", lambda: pytest.fail("the issuer must not be built"))
    facts = lambda_app.poller_handler({"tessera": "install-facts"}, None)
    assert facts["sha1dc_binary"] == str(binary)
    assert facts["sha1dc_binary_sha256"] == hashlib.sha256(b"not run").hexdigest()
    assert facts["python"] == "3.14" and facts["format"] == "tessera-v1-install/1"


def test_any_other_event_still_polls(monkeypatch):
    seen = []
    monkeypatch.setattr(lambda_app, "_issuer", lambda: seen.append(1) or object())
    monkeypatch.setattr(lambda_app.pipeline, "poll", lambda iss: {"advanced": {}})
    assert lambda_app.poller_handler({"source": "aws.events"}, None) == {"advanced": {}}
    assert seen == [1]


def lambda_record(**over):
    rec = json.loads(VERIFIER_INSTALL.read_text())
    rec.update(sha1dc_binary=lambda_app.SHA1DC_BINARY, unicode_module_sha256="ab" * 32)
    rec.update(over)
    return rec


def test_install_record_for_lambda_is_checked_before_packaging(tmp_path):
    good = tmp_path / "install.json"
    good.write_text(json.dumps(lambda_record()))
    assert package.check_install_record(good)["sha1dc_binary"] == lambda_app.SHA1DC_BINARY
    for bad in (lambda_record(sha1dc_binary="/home/tony/x"), lambda_record(sha1dc_binary_sha256="00" * 32),
                lambda_record(python="3.13"), {**lambda_record(), "extra": 1}):
        p = tmp_path / "bad.json"
        p.write_text(json.dumps(bad))
        with pytest.raises(SystemExit):
            package.check_install_record(p)


def test_zip_is_deterministic_and_keeps_the_binary_executable(tmp_path):
    src = tmp_path / "stage"
    (src / "a").mkdir(parents=True)
    (src / "a" / "x.py").write_text("x = 1\n")
    (src / "bin").mkdir()
    (src / "bin" / "tool").write_bytes(b"\x7fELF")
    (src / "bin" / "tool").chmod(0o755)
    one, two = package.write_zip(src, tmp_path / "1.zip"), package.write_zip(src, tmp_path / "2.zip")
    assert one == two
    with zipfile.ZipFile(tmp_path / "1.zip") as z:
        assert z.namelist() == ["a/x.py", "bin/tool"]
        assert (z.getinfo("bin/tool").external_attr >> 16) & 0o111


def test_package_and_lambda_agree_on_the_binary_path():
    assert package.LAMBDA_BINARY == lambda_app.SHA1DC_BINARY
    assert lambda_app.SHA1DC_BINARY.startswith("/var/task/")
