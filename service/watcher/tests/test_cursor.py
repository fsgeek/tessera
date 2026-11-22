"""Cursor durability: a run that crashes before its commit leaves the old state, so the next run re-processes the same
trail files and issuer items (findings repeat, never vanish; trace records are written once); the watermarks never
pass an item that is neither done nor pending; a concurrent commit is refused; the heartbeat follows a commit only."""
import json

import pytest

import fakes
from conftest import T0
from tessera_watch import watcher as W


class Crash(Exception):
    pass


def test_crash_before_commit_reprocesses_trail_and_siglog(env):
    env.trail(T0 - 300, [fakes.iam_event(T0 - 400)], region="us-east-1")
    env.ddb.put("SIGLOG#1", fakes.siglog(T0 - 60, slot="gpg", disposition="unrequested"))
    env.s3.fail_put = lambda b, k: Crash() if b == "state" else None
    with pytest.raises(Crash):
        env.run()
    assert sorted(env.codes()) == ["DISPOSITION_UNREQUESTED", "IAM_WRITE"] and env.cw.beats == []
    env.s3.fail_put = None
    env.clock.t += 600
    env.run()
    assert sorted(env.codes()) == ["DISPOSITION_UNREQUESTED", "DISPOSITION_UNREQUESTED", "IAM_WRITE", "IAM_WRITE"]
    env.clock.t += 600
    env.run()
    assert len(env.sns.sent) == 4 and len(env.cw.beats) == 2


def test_crash_while_publishing_reprocesses(env):
    env.trail(T0 - 300, [fakes.iam_event(T0 - 400)], region="us-east-1")
    env.sns.fail = True
    with pytest.raises(Exception):
        env.run()
    assert ("state", "state/watcher.json") not in env.s3.objects
    env.sns.fail = False
    env.run()
    assert env.codes() == ["IAM_WRITE"]


def test_crash_after_trace_write_does_not_duplicate_it(env):
    env.s3.put("results", "result/rid1/%s.json" % fakes.sha(b"b"), b"b")
    env.ddb.put("REQ#rid1", fakes.request("rid1", "COMPLETE", T0 - 300, receipt_sha256=fakes.sha(b"b")))
    env.s3.fail_put = lambda b, k: Crash() if b == "state" else None
    with pytest.raises(Crash):
        env.run()
    assert len(env.traces()) == 1
    env.s3.fail_put = None
    env.run()
    trace_puts = [v for v in env.s3.versions if v[0] == "trace"]
    assert len(trace_puts) == 1 and env.state()["pending"] == {}


def test_crash_in_trail_read_skips_nothing(env):
    k = env.trail(T0 - 300, [fakes.iam_event(T0 - 400)], region="us-east-1")
    real = env.s3.get_object

    def flaky(Bucket, Key):
        if Bucket == "trail":
            raise fakes.ClientError("SlowDown")
        return real(Bucket, Key)
    env.s3.get_object = flaky
    with pytest.raises(fakes.ClientError):
        env.run()
    env.s3.get_object = real
    env.run()
    assert env.codes() == ["IAM_WRITE"] and k in env.state()["ct_files"]


def test_each_trail_file_read_once(env):
    env.trail(T0 - 300, [fakes.iam_event(T0 - 400)], region="us-east-1")
    env.run()
    env.clock.t += 600
    env.run()
    assert env.codes() == ["IAM_WRITE"]
    assert sum(1 for b, k in env.s3.gets if b == "trail") == 1


def test_concurrent_run_commit_is_refused_and_no_heartbeat(env):
    env.run()
    first = env.make()
    load = first.state_store.load

    def load_then_other_run_commits():
        got = load()
        env.make().run()                                  # another run commits between our load and our save
        return got
    first.state_store.load = load_then_other_run_commits
    with pytest.raises(fakes.ClientError):
        first.run()
    assert len(env.cw.beats) == 2                         # the first run and the interleaved one; not the refused one


def test_stale_etag_is_refused(env):
    env.run()
    _, etag = env.make().state_store.load()
    env.clock.t += 600
    env.run()                                             # another commit moves the ETag
    with pytest.raises(fakes.ClientError):
        env.make().state_store.save({"v": 1}, etag)


def test_first_write_is_create_only(env):
    store = env.make().state_store
    store.save(W.empty_state(T0), None)
    with pytest.raises(fakes.ClientError):
        store.save(W.empty_state(T0), None)


def test_late_committed_terminal_record_within_overlap_is_processed(env):
    env.ddb.put("REQ#r1", fakes.request("r1", "REFUSED", T0 - 100, reason="TOO_LARGE"))
    env.run()
    env.clock.t += 600
    env.ddb.put("REQ#r0", fakes.request("r0", "REFUSED", T0 - 200, reason="TOO_LARGE"))   # ended earlier, seen later
    env.run()
    assert set(env.traces()) == {"trace/r1.json", "trace/r0.json"}
    env.clock.t += 600
    env.run()
    assert len([v for v in env.s3.versions if v[0] == "trace"]) == 2


def test_records_already_past_the_overlap_are_not_reprocessed(env):
    env.ddb.put("REQ#r1", fakes.request("r1", "REFUSED", T0 - 100, reason="TOO_LARGE"))
    env.run()
    env.clock.t += 2 * W.OVERLAP_S
    env.ddb.put("REQ#r2", fakes.request("r2", "REFUSED", T0 + 2 * W.OVERLAP_S - 50, reason="TOO_LARGE"))
    env.run()
    env.clock.t += 600
    env.run()
    st = env.state()
    assert "r1" not in st["req"]["seen"] and len(env.traces()) == 2
    assert len([v for v in env.s3.versions if v[0] == "trace"]) == 2


def test_live_requests_are_not_traced(env):
    rec = fakes.request("r1", "ACCEPTED", T0)
    rec["ended_at"] = None
    env.ddb.put("REQ#r1", rec)
    env.run()
    assert env.traces() == {} and env.state()["pending"] == {}


def test_heartbeat_after_each_committed_run(env):
    for _ in range(3):
        env.run()
        env.clock.t += 600
    assert [ns for ns, _ in env.cw.beats] == ["Tessera/Watcher"] * 3
    assert env.cw.beats[0][1][0]["MetricName"] == "Heartbeat"


def test_watcher_never_writes_to_issuer_stores(env):
    env.ddb.put("REQ#r1", fakes.request("r1", "REFUSED", T0 - 100, reason="TOO_LARGE"))
    env.ddb.put("SIGLOG#1", fakes.siglog(T0 - 60))
    env.s3.put("results", "result/r1/x.json", b"x")
    env.run()
    assert {c for c, _ in env.ddb.calls} == {"scan"}
    assert {b for b, k, _ in env.s3.versions} <= {"state", "trace"}
    assert json.dumps(env.state())                         # state is plain JSON
