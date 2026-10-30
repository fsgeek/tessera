"""A complete local issuer on stand-ins: in-memory stores and queues, stand-in signers (TEST keys), the stand-in
calendar and chain, the TEST DNS hierarchy. Used by the tests and for local runs.

  python -m tessera_issue.local --freeze FROZEN_OBJECTS_DIR --out DIR     # one receipt, offline"""
import argparse
import json
from dataclasses import dataclass
from pathlib import Path

from . import api, freeze, pipeline
from .chain import ExplorerHeaders
from .dns import LiveDns
from .ots import HttpCalendar
from .preship import PreShip
from .queues import InMemoryQueue
from .service import Issuer
from .signers import SlotSigner, StandInSigner
from .stand_in import World
from .stores import InMemoryRequestStore, InMemoryResultStore
from .util import DAY, FakeClock, rfc3339, ts


@dataclass
class Local:
    iss: Issuer
    world: World
    workers: dict          # slot -> StandInSigner
    clock: FakeClock

    def tick(self, run_signers=True, mine=True, step=600):
        """One poller period: signers answer what is queued, the poller runs, ten minutes pass, a block is mined."""
        if run_signers:
            for w in self.workers.values():
                w.process()
        out = pipeline.poll(self.iss)
        self.clock.advance(step)
        if mine:
            self.world.chain.mine(1)
        return out

    def run_until_done(self, rid, max_ticks=200, **kw):
        for _ in range(max_ticks):
            rec = self.iss.requests.get(rid)
            if rec["state"] != "ACCEPTED":
                return rec
            self.tick(**kw)
        return self.iss.requests.get(rid)


def build(objects_dir, start="2026-11-02T00:00:00Z", window_days=30, wire=False, seed="stand-in"):
    """wire=True puts the real protocol clients (HttpCalendar, ExplorerHeaders over two explorers, LiveDns) in
    front of the stand-ins, so the issuer reaches them only through the calendar, explorer and resolver protocols."""
    clock = FakeClock(ts(start))
    world = World(clock, seed)
    nb = rfc3339(ts(start) - DAY)
    window = world.prepare_window(nb, rfc3339(ts(nb) + window_days * DAY))
    frozen = freeze.load(objects_dir)
    queues = {s: (InMemoryQueue(clock), InMemoryQueue(clock)) for s in ("kms", "gpg")}
    wakes = []
    signers = {"kms": SlotSigner("kms", world.kms_key.spki, *queues["kms"], wake=wakes.append),
               "gpg": SlotSigner("gpg", world.gpg_key.pgp_body, *queues["gpg"], wake=wakes.append)}
    if wire:
        cal = HttpCalendar(world.calendar.uri, world.calendar.serve)
        hdr = ExplorerHeaders(["https://explorer-a.invalid/api", "https://explorer-b.invalid/api"],
                              world.chain.serve_esplora)
        dns = LiveDns(world.dns.serve(clock))
    else:
        cal, hdr, dns = world.calendar, world.chain, world.dns
    iss = Issuer(window=window, frozen=frozen, requests=InMemoryRequestStore(), results=InMemoryResultStore(),
                 signers=signers, calendars=[cal], headers=hdr, dns=dns,
                 preship=PreShip(frozen, window.trust_base), clock=clock)
    iss.wakes = wakes
    iss.elapsed_clock = clock                        # the stand-in's monotonic clock is its fake clock
    import random
    iss.rng = random.Random(seed)                    # reproducible drain order in local runs and tests
    workers = {s: StandInSigner(s, k, *queues[s], clock, sign_until=window.sign_until, fetch=iss.results.get_ref)
               for s, k in (("kms", world.kms_key), ("gpg", world.gpg_key))}
    return Local(iss, world, workers, clock)


def main():
    import uuid
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--freeze", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--content", default="TEST content for a local stand-in issuance\n")
    a = ap.parse_args()
    loc = build(a.freeze)
    key = str(uuid.uuid4())
    r = api.submit(loc.iss, "local-credential", key, a.content.encode())
    print(r.status, json.dumps(r.body))
    rec = loc.run_until_done(api.record_id("local-credential", key))
    print(json.dumps(api.view(rec, loc.clock())))
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    if rec["state"] == "COMPLETE":
        r = api.receipt(loc.iss, "local-credential", key)        # 303; the stand-in follows the one URL
        data = loc.iss.results.fetch_url(r.headers["Location"], loc.clock())
        (out / "bundle.json").write_bytes(data)
    return 0 if rec["state"] == "COMPLETE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
