"""Packaging: the Lambda layout matches lambda_app, the staged sources hold no issuer code, and the zip is
deterministic (same bytes, same SHA-256, for the same inputs)."""
import importlib.util
import zipfile
from pathlib import Path

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
                                      "TRACE_RETAIN_UNTIL": "2028-03-07T00:00:00Z",
                                      "EXPLORERS": '["https://a", "https://b"]', "CLIENT_KEY_IDS": '{"x": "id"}'})
    assert cfg.kms_aliases == ("alias/tessera-v1-kms",) and cfg.explorers == ("https://a", "https://b")
    assert cfg.window["not_after"] == "2027-02-01T00:00:00Z" and cfg.client_key_ids == {"x": "id"}
