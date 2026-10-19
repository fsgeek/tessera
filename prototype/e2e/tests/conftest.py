import sys
import time
from pathlib import Path

import pytest

E2E = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(E2E))

from common import WORK  # noqa: E402


@pytest.fixture
def workdir(request):
    """A fresh directory under prototype/e2e/work/tests/ (git-ignored; never deleted by the tests)."""
    d = WORK / "tests" / f"{request.node.name}-{time.strftime('%Y%m%dT%H%M%S')}-{time.monotonic_ns() % 10**6}"
    d.mkdir(parents=True)
    return d
