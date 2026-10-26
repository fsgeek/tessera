"""MZ-02: materialize.py --check must detect changed, missing and unexpected files in the existing fixtures.
Works on a temporary copy; the repository fixtures are never written.  Run (repo root):
  prototype/.venv/bin/python formal/e10/test_materialize_check.py
The fresh build is stubbed with the pristine saved manifest so the test isolates the on-disk inspection."""
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import materialize as M  # noqa: E402

FIX = Path(__file__).resolve().parent / "fixtures"


class CheckDetects(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="e10-checktest-")
        self.out = Path(self.tmp.name) / "fixtures"
        shutil.copytree(FIX, self.out)
        self.saved = json.loads((FIX / "MANIFEST.json").read_text())
        self._orig = M.materialize
        M.materialize = lambda out, only=None: self.saved     # a fresh build identical to the saved manifest

    def tearDown(self):
        M.materialize = self._orig
        self.tmp.cleanup()

    def test_pristine_copy_passes(self):
        r = M.check_dirs(self.out)
        self.assertFalse(any(r.values()), r)

    def test_changed(self):
        f = self.out / "E10-TMP-10" / "bundle.json"
        f.write_bytes(f.read_bytes() + b" ")
        r = M.check_dirs(self.out)
        self.assertEqual(r["changed"], ["E10-TMP-10/bundle.json"])
        self.assertEqual(M.check(self.out), 1)

    def test_missing(self):
        (self.out / "E10-TMP-10" / "trust.json").unlink()
        r = M.check_dirs(self.out)
        self.assertEqual(r["missing"], ["E10-TMP-10/trust.json"])
        self.assertEqual(M.check(self.out), 1)

    def test_unexpected(self):
        (self.out / "E10-TMP-10" / "stray.txt").write_text("x")
        r = M.check_dirs(self.out)
        self.assertEqual(r["unexpected"], ["E10-TMP-10/stray.txt"])
        self.assertEqual(M.check(self.out), 1)

    def test_run_record_excluded(self):
        (self.out / M.RUN_RECORD).write_text("{}")
        self.assertFalse(any(M.check_dirs(self.out).values()))


if __name__ == "__main__":
    unittest.main()
