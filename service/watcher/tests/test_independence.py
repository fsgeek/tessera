"""Independence (contract item 0(b)): the watcher shares no code with the issuer beyond the frozen service verifier.
Every import is parsed; the package is loaded in a fresh interpreter to see which files it actually imports."""
import ast
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "tessera_watch"
ALLOWED = set(sys.stdlib_module_names) | {"cryptography", "tessera_verify", "tessera_watch", "boto3", "botocore"}


def test_every_import_is_stdlib_cryptography_verifier_or_the_package():
    for f in PACKAGE.glob("*.py"):
        for node in ast.walk(ast.parse(f.read_text())):
            if isinstance(node, ast.Import):
                for a in node.names:
                    assert a.name.split(".")[0] in ALLOWED, f"{f.name}: import {a.name}"
            elif isinstance(node, ast.ImportFrom) and not node.level:
                assert (node.module or "").split(".")[0] in ALLOWED, f"{f.name}: from {node.module}"


def test_no_issuer_or_instrument_reference_in_the_package():
    for f in PACKAGE.glob("*.py"):
        text = f.read_text()
        assert "tessera_issue" not in text.replace("service/issuer/tessera_issue", ""), f.name
        assert "prototype" not in text and "spike" not in text.lower(), f.name
        assert "sys.path" not in text, f.name


def test_loaded_modules_are_the_watcher_and_the_verifier_only():
    code = ("import json,sys\nimport tessera_watch.watcher, tessera_watch.lambda_app, tessera_watch.receipts\n"
            "print(json.dumps(sorted(n for n in sys.modules if n.split('.')[0].startswith('tessera'))))")
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True)
    tops = {n.split(".")[0] for n in json.loads(out.stdout)}
    assert tops == {"tessera_watch", "tessera_verify"}
