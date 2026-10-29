"""Service code never imports instrument code (A9.2): the package, its build files and tests are grepped, every
import is parsed, and the package is loaded in a fresh interpreter to see which files it actually imports."""
import ast
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "tessera_signer"
FORBIDDEN = re.compile(r"prototype|spike", re.I)
SERVICE_FILES = sorted(PACKAGE.glob("*.py")) + [ROOT / "pyproject.toml", ROOT / "Dockerfile", ROOT / "requirements.txt"]
ALLOWED = set(sys.stdlib_module_names) | {"cryptography", "tessera_verify", "tessera_signer", "boto3"}


def _imports(f):
    for node in ast.walk(ast.parse(f.read_text())):
        if isinstance(node, ast.Import):
            yield from (a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0:
            yield node.module or ""


def test_no_reference_to_prototype_or_spike():
    hits = [f"{f.name}:{n}: {line.strip()}" for f in SERVICE_FILES
            for n, line in enumerate(f.read_text().splitlines(), 1) if FORBIDDEN.search(line)]
    assert hits == []


def test_every_import_is_stdlib_cryptography_verifier_boto3_or_the_package():
    for f in PACKAGE.glob("*.py"):
        for name in _imports(f):
            assert name.split(".")[0] in ALLOWED, f"{f.name}: import {name}"


def test_tests_import_nothing_from_the_instrument_or_formal():
    for f in Path(__file__).parent.glob("*.py"):
        for name in _imports(f):
            assert not FORBIDDEN.search(name) and "formal" not in name.split("."), f"{f.name}: import {name}"


def test_loaded_files_are_package_verifier_or_third_party():
    code = ("import json, sys, tessera_signer.main, tessera_signer.signer, tessera_signer.gcp\n"
            "print(json.dumps(sorted(m.__file__ for m in list(sys.modules.values()) if getattr(m, '__file__', None))))")
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True, cwd=ROOT,
                         env={"PYTHONPATH": f"{ROOT}:{ROOT.parent / 'verifier'}"})
    for path in json.loads(out.stdout):
        assert not FORBIDDEN.search(path) and "/formal/" not in path and "/service/issuer/" not in path, path
