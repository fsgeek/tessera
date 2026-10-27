import uuid
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]                 # service/issuer
REPO = ROOT.parents[1]
FROZEN = REPO / "formal" / "freeze-v1" / "objects"        # read as data: the objects the receipts bind
VERIFIER_CLI = REPO / "service" / "verifier" / ".venv" / "bin" / "tessera-verify"


@pytest.fixture
def loc():
    from tessera_issue import local
    return local.build(FROZEN)


@pytest.fixture
def key():
    return str(uuid.uuid4())
