"""The final pass's four fixes (docs/reviews/watcher/CODEX-CONFIRM.md, "New HIGH"): no D6 outcome from a run with a
partial read; no trail file skipped by a time-budget cutoff; no finding lost when both the outbox and SNS fail.
(The trace PUT permission is test_infra's.) Owner's unit tests over fakes."""
import json

import pytest

import fakes
from conftest import T0
from tessera_watch import watcher as W

STATE = ("state", "state/watcher.json")


def d6(env):
    return [c for c in env.codes() if c.startswith(("SIGN", "SIGNATURE"))]


def test_a_trail_listing_failure_at_the_horizon_finalizes_nothing(env):
    env.run()                                                  # coverage starts
    h = fakes.sha(b"used")
    env.trail(T0 + 120, [fakes.sign_event(T0 + 100)])
    env.ddb.put("SIGLOG#1", fakes.siglog(T0 + 200, sig=h, request_id="kms-req-1"))
    real = env.s3.list_objects_v2

    def down(**kw):
        if kw["Bucket"] == "trail":
            raise fakes.ClientError("SlowDown")
        return real(**kw)
    env.s3.list_objects_v2 = down
    env.clock.t = T0 + 200 + W.SIG_HORIZON_S + W.SIGN_HORIZON_S
    env.run()
    assert d6(env) == [] and env.state()["sigs"][h]["final"] is None
    env.s3.list_objects_v2 = real
    env.clock.t += 600
    env.run()
    assert d6(env) == [] and env.state()["sigs"][h]["final"] == "matched"


def test_a_siglog_entry_that_fails_finalizes_nothing(env, monkeypatch):
    env.run()
    h = fakes.sha(b"used")
    env.trail(T0 + 120, [fakes.sign_event(T0 + 100)])
    env.ddb.put("SIGLOG#1", fakes.siglog(T0 + 200, sig=h, request_id="kms-req-1"))
    real = W.Watcher.on_siglog

    def boom(self, *a, **k):
        raise RuntimeError("one entry")
    monkeypatch.setattr(W.Watcher, "on_siglog", boom)
    env.clock.t = T0 + 200 + W.SIG_HORIZON_S + W.SIGN_HORIZON_S
    env.run()
    assert d6(env) == [] and "ITEM_CHECK_FAILED" in env.codes()
    monkeypatch.setattr(W.Watcher, "on_siglog", real)
    env.clock.t += 600
    env.run()
    assert d6(env) == [] and env.state()["sigs"][h]["final"] == "matched"


def test_a_budget_cutoff_does_not_skip_an_earlier_file_of_another_region(env):
    """east 3 h ago (read), east 70 min ago and west 100 min ago: the cutoff after one file must hold the cursor at the
    west file, the earliest unread, not at the cut east key (path order would put west last)."""
    env.trail(T0 - 3 * 3600, [fakes.iam_event(T0 - 3 * 3600 - 60)], region="us-east-1")
    env.trail(T0 - 70 * 60, [fakes.iam_event(T0 - 71 * 60, name="CreateRole")], region="us-east-1")
    west = env.trail(T0 - 100 * 60, [fakes.iam_event(T0 - 101 * 60, name="AttachRolePolicy")], region="us-west-2")
    calls = []

    def remaining():
        calls.append(1)
        return 1e9 if len(calls) == 1 else 1000               # time for one file only
    env.make(remaining=remaining).run()
    assert env.state()["trail"]["cursor"] <= T0 - 100 * 60 and west not in env.state()["trail"]["files"]
    env.clock.t += 600
    env.run()
    assert sorted(json.loads(m["Message"])["event_name"] for m in env.sns.sent) == \
        ["AttachRolePolicy", "CreateAccessKey", "CreateRole"]


def test_a_finding_neither_queued_nor_published_stops_the_commit(env):
    env.run()
    k = env.trail(T0 + 120, [fakes.iam_event(T0 + 60)], region="us-east-1")
    env.s3.fail_put = lambda b, key: fakes.ClientError("InternalError") if key.startswith("findings/") else None
    env.sns.fail = True
    env.clock.t += 600
    beats = len(env.cw.beats)
    with pytest.raises(RuntimeError):
        env.run()
    assert k not in env.state()["trail"]["files"] and len(env.cw.beats) == beats
    env.s3.fail_put, env.sns.fail = None, False
    env.clock.t += 600
    env.run()
    assert env.codes() == ["IAM_WRITE"]
