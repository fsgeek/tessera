import json
from pathlib import Path

import pytest

import fakes
from tessera_watch import receipts, stores
from tessera_watch.watcher import Config, Watcher

ROOT = Path(__file__).resolve().parents[1]                 # service/watcher
REPO = ROOT.parents[1]
WINDOW = REPO / "service" / "issuer" / "config" / "window.json"
CATALOG = REPO / "formal" / "freeze-v1" / "objects" / "catalog.json"
SMOKE = REPO / "docs" / "smoke" / "2026-11-16-first-receipt"
T0 = 1795000000                                            # 2026-11-17T...Z, a fixed clock base


class Clock:
    def __init__(self, t=T0):
        self.t = t

    def __call__(self):
        return self.t


class Env:
    """A watcher over fakes; `make()` builds a fresh Watcher on the same stores (one per run, as Lambda does)."""

    def __init__(self, verify=None):
        self.s3, self.ddb, self.sns, self.cw = fakes.FakeS3(), fakes.FakeDynamo(), fakes.FakeSNS(), fakes.FakeCW()
        self.clock = Clock()
        self.verify = verify or (lambda bundle, *a, **k: {"verdict": "VALID_STRICT", "reason": "OK",
                                                          "heights": [1, 2], "T": "2026-11-16T14:35:57Z"})
        self.cfg = Config(account=fakes.ACCOUNT, kms_key_arn=fakes.KEY_ARN, kms_aliases=(fakes.ALIAS,),
                          signer_role_arn=fakes.SIGNER_ROLE, explorers=("https://a.example", "https://b.example"),
                          client_key_ids={"smoke-test": "abc123key"}, window=receipts.load_window(WINDOW),
                          catalog=receipts.load_catalog(CATALOG), retain_until="2028-03-07T00:00:00Z",
                          watcher_version="test")
        self.until = "2028-03-07T00:00:00Z"

    def make(self, remaining=lambda: 1e9):
        return Watcher(self.cfg, stores.IssuerTable(self.ddb, "requests"), stores.Results(self.s3, "results"),
                       stores.TrailBucket(self.s3, "trail"), stores.StateObject(self.s3, "state", "state/watcher.json"),
                       stores.TraceBucket(self.s3, "trace", self.until), stores.Topic(self.sns, "arn:topic"),
                       stores.Heartbeat(self.cw), clock=self.clock, verify=self.verify, remaining=remaining,
                       out=self.out)

    out = None

    def run(self):
        return self.make().run()

    def trail(self, t, records, region=fakes.REGION):
        key = fakes.trail_key(t, region)
        self.s3.put("trail", key, fakes.trail_file(records))
        return key

    def codes(self, sent=None):
        return [json.loads(m["Message"])["code"] for m in (self.sns.sent if sent is None else sent)]

    def traces(self):
        return {k: json.loads(o["body"]) for (b, k), o in self.s3.objects.items() if b == "trace"}

    def state(self):
        return json.loads(self.s3.objects[("state", "state/watcher.json")]["body"])


@pytest.fixture
def env():
    return Env()
