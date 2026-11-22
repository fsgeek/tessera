"""Build the watcher's Lambda package (detect infra variable watcher_zip): tessera_watch, the frozen service verifier
tessera_verify (the only code shared with the issuer), cryptography for Lambda's Linux, the frozen catalog, the
window record, the SHA-1DC detector and the Lambda's own verifier install.json.

    python package.py OUT.zip                       # bootstrap package: no install.json, so every D8 check is refused
    python package.py OUT.zip --install-json FILE   # deployable package

Same discipline as service/issuer/package.py (deterministic zip: sorted entries, fixed time, modes 644/755; the
SHA-256 is printed and must be recorded). The install record is per installation: deploy the bootstrap package, invoke
the watcher with {"watcher": "install-facts"}, save the answer as FILE, and build again with it. The watcher's
runtime version is pinned in infra like the issuer's. Needs uv (for the Linux wheel) and a built verifier
(service/verifier/install.sh)."""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
VERIFIER = HERE.parent / "verifier"
CATALOG = HERE.parent.parent / "formal" / "freeze-v1" / "objects" / "catalog.json"
WINDOW = HERE.parent / "issuer" / "config" / "window.json"          # the window record (data, not issuer code)
LAMBDA_BINARY = "/var/task/tessera-verify/bin/sha1dcsum"            # = lambda_app.SHA1DC_BINARY (a test checks)
WHEEL = ["cryptography==50.0.2"]
PLATFORM = "x86_64-manylinux_2_34"
FIELDS = {"format", "python", "unicode_version", "unicode_module_sha256", "sha1dc_upstream_commit", "sha1dc_binary",
          "sha1dc_binary_sha256"}


def die(msg):
    raise SystemExit("package: " + msg)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def pinned_binary():
    rec = json.loads((VERIFIER / "install.json").read_text())
    binary = Path(rec["sha1dc_binary"])
    if not binary.is_file() or sha256(binary) != rec["sha1dc_binary_sha256"]:
        die("SHA-1DC binary missing or not the pinned build; run service/verifier/install.sh")
    return binary, rec


def check_install_record(path):
    try:
        rec = json.loads(Path(path).read_text())
    except (OSError, ValueError) as e:
        die(f"install record unreadable: {e}")
    _, local = pinned_binary()
    if not isinstance(rec, dict) or set(rec) != FIELDS or rec["format"] != "tessera-v1-install/1":
        die("install record: wrong fields or format")
    if rec["sha1dc_binary"] != LAMBDA_BINARY or rec["sha1dc_binary_sha256"] != local["sha1dc_binary_sha256"]:
        die("install record: not this package's SHA-1DC binary")
    for k in ("python", "unicode_version", "sha1dc_upstream_commit"):
        if rec[k] != local[k]:
            die(f"install record: {k} {rec[k]!r} differs from the verifier's {local[k]!r}")
    return rec


def write_zip(stage, out):
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(p for p in Path(stage).rglob("*") if p.is_file()):
            info = zipfile.ZipInfo(f.relative_to(stage).as_posix(), (1980, 1, 1, 0, 0, 0))
            info.external_attr = (0o100755 if f.stat().st_mode & 0o111 else 0o100644) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, f.read_bytes())
    return sha256(out)


def stage_sources(stage):
    """Everything except the third-party wheel and the detector (shared by build and the tests)."""
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc", "*.egg-info")
    shutil.copytree(HERE / "tessera_watch", stage / "tessera_watch", ignore=ignore)
    shutil.copytree(VERIFIER / "tessera_verify", stage / "tessera_verify", ignore=ignore)
    (stage / "freeze-v1" / "objects").mkdir(parents=True)
    shutil.copyfile(CATALOG, stage / "freeze-v1" / "objects" / "catalog.json")
    (stage / "config").mkdir()
    shutil.copyfile(WINDOW, stage / "config" / "window.json")


def build(out, install_json=None):
    binary, _ = pinned_binary()
    rec = check_install_record(install_json) if install_json else None
    with tempfile.TemporaryDirectory() as tmp:
        stage = Path(tmp) / "stage"
        subprocess.run(["uv", "pip", "install", "--quiet", "--target", str(stage), "--python-version", "3.14",
                        "--python-platform", PLATFORM, "--only-binary", ":all:", *WHEEL], check=True)
        stage_sources(stage)
        dest = stage / LAMBDA_BINARY.removeprefix("/var/task/")
        dest.parent.mkdir(parents=True)
        shutil.copyfile(binary, dest)
        dest.chmod(0o755)
        if rec:
            (dest.parent.parent / "install.json").write_text(json.dumps(rec, indent=1, sort_keys=True) + "\n")
        return write_zip(stage, out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("out")
    ap.add_argument("--install-json")
    a = ap.parse_args(argv)
    digest = build(Path(a.out), a.install_json)
    kind = "deployable" if a.install_json else "BOOTSTRAP (no install.json: D8 checks are refused until rebuilt)"
    print(f"{a.out}: {kind}\nsha256 {digest}\nwindow.json sha256 {sha256(WINDOW)}\ncatalog sha256 {sha256(CATALOG)}")


if __name__ == "__main__":
    sys.exit(main())
