"""Run all conformance cases against the SERVICE verifier, reading the case files as data (conformance_runner.py).
Every case must agree with its expected.json; the count is pinned so a missing or extra case is a failure."""
import json
import os
import unittest
from collections import Counter
from pathlib import Path
import conformance_runner as runner

EXPECTED_CASES = 352


class ConformanceTests(unittest.TestCase):
    def test_all_cases_agree_with_expected_json(self):
        self.assertTrue(runner.DEFAULT_CASES.is_dir(), f'case data missing: {runner.DEFAULT_CASES}')
        results = runner.run_all(jobs=int(os.environ.get('TESSERA_CONFORMANCE_JOBS', '4')))
        counts = Counter(r['outcome'] for r in results)
        out = os.environ.get('TESSERA_CONFORMANCE_JSON')
        if out: Path(out).write_text(json.dumps(results, indent=1) + '\n')
        bad = [r for r in results if r['outcome'] != 'AGREE']
        self.assertEqual(len(results), EXPECTED_CASES)
        self.assertEqual(bad, [], dict(counts))
        self.assertEqual(counts['AGREE'], EXPECTED_CASES)


if __name__ == '__main__': unittest.main()
