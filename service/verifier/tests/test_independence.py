"""A9.2 / owner reading (docs/V1-FREEZE-OPEN.md): service code may copy instrument source but never imports it.
This check greps the package, the installer and the project file, parses every import, and loads the package in a
fresh interpreter to see which module files actually get imported."""
import ast
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'tessera_verify'
FORBIDDEN = re.compile(r'prototype|spike', re.I)
SERVICE_FILES = sorted(PACKAGE.glob('*.py')) + [ROOT / 'install.sh', ROOT / 'pyproject.toml', ROOT / 'requirements.txt']


class IndependenceTests(unittest.TestCase):
    def test_package_is_not_empty(self):
        self.assertGreaterEqual(len(list(PACKAGE.glob('*.py'))), 10)

    def test_grep_finds_no_reference_to_prototype_or_spike(self):
        hits = [f'{f.name}:{n}: {line.strip()}' for f in SERVICE_FILES for n, line in enumerate(f.read_text().splitlines(), 1) if FORBIDDEN.search(line)]
        self.assertEqual(hits, [])

    def test_every_import_is_stdlib_cryptography_or_the_package(self):
        allowed_external = set(sys.stdlib_module_names) | {'cryptography'}
        for f in PACKAGE.glob('*.py'):
            for node in ast.walk(ast.parse(f.read_text())):
                if isinstance(node, ast.Import):
                    for a in node.names:
                        self.assertIn(a.name.split('.')[0], allowed_external, f'{f.name}: import {a.name}')
                elif isinstance(node, ast.ImportFrom):
                    if node.level: continue                       # relative: inside this package
                    self.assertIn((node.module or '').split('.')[0], allowed_external | {'tessera_verify'}, f'{f.name}: from {node.module}')

    def test_loaded_modules_come_from_the_service_tree_only(self):
        code = ('import json,sys\nimport tessera_verify.cli, tessera_verify.verify, tessera_verify.release_auth\n'
                'print(json.dumps([getattr(m,"__file__",None) or "" for n,m in sys.modules.items() if n.split(".")[0]=="tessera_verify"]))')
        out = subprocess.run([sys.executable, '-I', '-c', code], capture_output=True, text=True, cwd=str(ROOT.parent.parent), check=True)
        files = [Path(p).resolve() for p in json.loads(out.stdout) if p]
        self.assertGreater(len(files), 8)
        for p in files: self.assertTrue(p.is_relative_to(PACKAGE), str(p))
        # And nothing resolvable at the repository's prototype/ or spike directories is on the path in that run.
        path = subprocess.run([sys.executable, '-I', '-c', 'import sys;print("\\n".join(sys.path))'], capture_output=True, text=True, cwd=str(ROOT.parent.parent)).stdout
        self.assertFalse(FORBIDDEN.search(path), path)

    def test_no_conformance_or_fixture_input_at_run_time(self):
        # The only places the service tree may name the frozen objects are tests; the package never reads them.
        for f in PACKAGE.glob('*.py'): self.assertNotIn('freeze-v1', f.read_text(), f.name)


if __name__ == '__main__': unittest.main()
