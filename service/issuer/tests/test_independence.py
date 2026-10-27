"""Service code never imports instrument code (A9.2; the owner's reading in docs/V1-FREEZE-OPEN.md): the issuer
package and the infrastructure are grepped, every import is parsed, and the package is loaded in a fresh interpreter
to see which files it actually imports. It may depend on the service verifier (tessera_verify) as a library."""
import ast
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "tessera_issue"
FORBIDDEN = re.compile(r"prototype|spike", re.I)
SERVICE_FILES = sorted(PACKAGE.glob("*.py")) + [ROOT / "pyproject.toml"] + sorted((ROOT / "infra").glob("*.tf"))
ALLOWED = set(sys.stdlib_module_names) | {"cryptography", "tessera_verify", "tessera_issue", "boto3"}


class IndependenceTests(unittest.TestCase):
    def test_package_is_not_empty(self):
        self.assertGreaterEqual(len(list(PACKAGE.glob("*.py"))), 15)

    def test_grep_finds_no_reference_to_prototype_or_spike(self):
        hits = [f"{f.name}:{n}: {line.strip()}" for f in SERVICE_FILES
                for n, line in enumerate(f.read_text().splitlines(), 1) if FORBIDDEN.search(line)]
        self.assertEqual(hits, [])

    def test_tests_import_nothing_from_the_instrument_either(self):
        for f in Path(__file__).parent.glob("*.py"):
            for node in ast.walk(ast.parse(f.read_text())):
                names = [a.name for a in node.names] if isinstance(node, ast.Import) else \
                        [node.module or ""] if isinstance(node, ast.ImportFrom) else []
                for n in names:
                    self.assertFalse(FORBIDDEN.search(n), f"{f.name}: import {n}")
                    self.assertNotIn("formal", n.split("."), f"{f.name}: import {n}")

    def test_every_import_is_stdlib_cryptography_verifier_or_the_package(self):
        for f in PACKAGE.glob("*.py"):
            for node in ast.walk(ast.parse(f.read_text())):
                if isinstance(node, ast.Import):
                    for a in node.names:
                        self.assertIn(a.name.split(".")[0], ALLOWED, f"{f.name}: import {a.name}")
                elif isinstance(node, ast.ImportFrom) and not node.level:
                    self.assertIn((node.module or "").split(".")[0], ALLOWED, f"{f.name}: from {node.module}")

    def test_no_sys_path_manipulation(self):
        for f in PACKAGE.glob("*.py"):
            self.assertNotIn("sys.path", f.read_text(), f.name)

    def test_loaded_modules_come_from_the_service_tree_only(self):
        code = ("import json,sys\nimport tessera_issue.api, tessera_issue.pipeline, tessera_issue.local, "
                "tessera_issue.aws, tessera_issue.lambda_app\n"
                "print(json.dumps([getattr(m,'__file__',None) or '' for n,m in sys.modules.items() "
                "if n.split('.')[0] in ('tessera_issue','tessera_verify')]))")
        out = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True,
                             cwd=str(ROOT.parent.parent), check=True)
        files = [Path(p).resolve() for p in json.loads(out.stdout) if p]
        self.assertGreater(len(files), 15)
        service = ROOT.parent
        for p in files:
            self.assertTrue(p.is_relative_to(service / "issuer" / "tessera_issue")
                            or p.is_relative_to(service / "verifier" / "tessera_verify"), str(p))
        path = subprocess.run([sys.executable, "-I", "-c", 'import sys;print("\\n".join(sys.path))'],
                              capture_output=True, text=True, cwd=str(ROOT.parent.parent)).stdout
        self.assertFalse(FORBIDDEN.search(path), path)

    def test_frozen_objects_are_named_only_by_tests(self):
        for f in PACKAGE.glob("*.py"):
            self.assertNotIn("freeze-v1", f.read_text(), f.name)


if __name__ == "__main__":
    unittest.main()
