"""Cursor durability: a run that crashes before its commit leaves the old state, so the next run re-processes the same
trail files and issuer items (findings repeat, never vanish; trace records are written once); no cursor moves by an
issuer-supplied time (review H2) and nothing unseen is dropped when windows move (M2); a concurrent commit is refused;
the heartbeat follows a sound commit only."""
import json

import pytest

import fakes
from conftest import T0
from tessera_watch import watcher as W

STATE = ("state", "state/watcher.json")


class Crash(Exception):
    pass


def crash_commit(env):
    """Fail the state commit only (the If-Match put), not the first run's create or the outbox."""
    env.s3.fail_put = lambda b, k: Crash() if (b, k) == STATE and STATE in env.s3.objects else None


def test_crash_before_commit_reprocesses_trail_and_siglog(env):
    env.trail(T0 - 300, [fakes.iam_event(T0 - 400)], region="us-east-1")
    env.ddb.put("SIGLOG#1", fakes.siglog(T0 - 60, slot="gpg", disposition="unrequested"))
    crash_commit(env)
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


def test_first_run_creates_its_state_before_reading_so_coverage_survives_a_crash(env):
    crash_commit(env)
    with pytest.raises(Crash):
        env.run()
    assert env.state()["coverage_start"] == T0 - W.LOOKBACK_S
    env.s3.fail_put = None
    env.clock.t += 3 * 3600
    env.run()
    assert env.state()["coverage_start"] == T0 - W.LOOKBACK_S


def test_publish_failure_keeps_findings_in_the_outbox_and_withholds_the_heartbeat(env):
    env.trail(T0 - 300, [fakes.iam_event(T0 - 400)], region="us-east-1")
    env.sns.fail = True
    env.run()                                             # the run commits; nothing is lost
    assert env.sns.sent == [] and len(env.outbox()) == 1 and env.cw.beats == []
    env.sns.fail = False
    env.clock.t += 600
    env.run()
    assert env.codes() == ["IAM_WRITE"] and env.outbox() == [] and len(env.cw.beats) == 1


def test_one_failed_publish_does_not_stop_the_others(env):
    env.trail(T0 - 300, [fakes.iam_event(T0 - 400), fakes.iam_event(T0 - 390, name="CreateRole")],
              region="us-east-1")
    real, calls = env.sns.publish, []

    def flaky(**kw):
        calls.append(1)
        if len(calls) == 1:
            raise fakes.ClientError("InternalError")
        return real(**kw)
    env.sns.publish = flaky
    env.run()
    assert len(env.sns.sent) == 1 and len(env.outbox()) == 1
    env.sns.publish = real
    env.clock.t += 600
    env.run()
    assert sorted(json.loads(m["Message"])["event_name"] for m in env.sns.sent) == ["CreateAccessKey", "CreateRole"]


def test_finding_is_durable_before_a_trace_write_and_survives_a_crash(env):
    """M3: D8 finds corrupt bytes; the trace write then fails and the run dies before publishing. The finding was
    already in the outbox, so the next run publishes it even if the corrupt object is gone by then."""
    env.s3.put("results", "result/%s/%s.json" % ("a" * 64, "0" * 64), b"corrupt")
    env.ddb.put("REQ#" + "a" * 64, fakes.request("a" * 64, "COMPLETE", T0 - 300, receipt_sha256="0" * 64))
    env.s3.fail_put = lambda b, k: Crash() if b == "trace" else None
    real = env.sns.publish

    def die(**kw):
        raise KeyboardInterrupt                           # the invocation is killed mid-publication
    env.sns.publish = die
    with pytest.raises(KeyboardInterrupt):
        env.run()
    assert len(env.outbox()) >= 1
    env.sns.publish, env.s3.fail_put = real, None
    del env.s3.objects[("results", "result/%s/%s.json" % ("a" * 64, "0" * 64))]
    env.clock.t += 600
    env.run()
    assert "RECEIPT_BYTES_DIGEST_MISMATCH" in env.codes()


def test_crash_after_trace_write_does_not_duplicate_it(env):
    rid = "b" * 64
    env.s3.put("results", "result/%s/%s.json" % (rid, fakes.sha(b"b")), b"b")
    env.ddb.put("REQ#" + rid, fakes.request(rid, "COMPLETE", T0 - 300, receipt_sha256=fakes.sha(b"b")))
    crash_commit(env)
    with pytest.raises(Crash):
        env.run()
    assert len(env.traces()) == 1
    env.s3.fail_put = None
    env.run()
    trace_puts = [v for v in env.s3.versions if v[0] == "trace"]
    assert len(trace_puts) == 1 and env.state()["pending"] == {}


def test_a_trail_file_that_fails_to_read_is_reported_and_retried(env):
    k = env.trail(T0 - 300, [fakes.iam_event(T0 - 400)], region="us-east-1")
    real = env.s3.get_object

    def flaky(Bucket, Key):
        if Bucket == "trail":
            raise fakes.ClientError("SlowDown")
        return real(Bucket, Key)
    env.s3.get_object = flaky
    env.run()                                             # isolated: the run commits and heartbeats
    assert env.codes() == ["TRAIL_FILE_UNREADABLE"] and len(env.cw.beats) == 1
    msg = json.loads(env.sns.sent[0]["Message"])
    assert msg["error_class"] == "ClientError" and msg["region"] == "us-east-1" and k not in json.dumps(msg)
    env.s3.get_object = real
    env.clock.t += 600
    env.run()
    assert env.codes() == ["TRAIL_FILE_UNREADABLE", "IAM_WRITE"] and k in env.state()["trail"]["files"]


def test_each_trail_file_read_once(env):
    env.trail(T0 - 300, [fakes.iam_event(T0 - 400)], region="us-east-1")
    env.run()
    env.clock.t += 600
    env.run()
    assert env.codes() == ["IAM_WRITE"]
    assert sum(1 for b, k in env.s3.gets if b == "trail") == 1


def test_trail_cursor_moves_by_the_watchers_clock_so_an_outage_loses_no_file(env):
    """M2: the watcher is down for two days; a file delivered just after its last commit is older than any 24 h
    look-back when it comes back, and is still read."""
    env.run()
    env.trail(T0 + 120, [fakes.iam_event(T0 + 60)], region="us-east-1")
    env.clock.t = T0 + 2 * 86400
    env.run()
    assert env.codes() == ["IAM_WRITE"]
    assert env.state()["trail"]["cursor"] == T0 + 2 * 86400 - W.TRAIL_LAG_S


def test_the_trail_cursor_does_not_pass_a_file_that_failed(env):
    env.run()
    env.trail(T0 + 120, [fakes.iam_event(T0 + 60)], region="us-east-1")
    real = env.s3.get_object
    env.s3.get_object = lambda Bucket, Key: (_ for _ in ()).throw(fakes.ClientError("SlowDown")) \
        if Bucket == "trail" else real(Bucket, Key)
    env.clock.t = T0 + 6 * 3600
    env.run()
    assert env.state()["trail"]["cursor"] <= T0 + 120
    env.s3.get_object = real
    env.clock.t += 600
    env.run()
    assert "IAM_WRITE" in env.codes()


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


def test_a_terminal_record_seen_late_is_processed_whatever_its_time(env):
    """H2/M2: no watermark by issuer time; a record that ended hours before it became visible still gets its trace."""
    r1, r0 = "1" * 64, "0" * 64
    env.ddb.put("REQ#" + r1, fakes.request(r1, "REFUSED", T0 - 100, reason="TOO_LARGE"))
    env.run()
    env.clock.t += 6 * 3600
    env.ddb.put("REQ#" + r0, fakes.request(r0, "REFUSED", T0 - 5 * 3600, reason="TOO_LARGE"))
    env.run()
    assert set(env.traces()) == {f"trace/{r1}.json", f"trace/{r0}.json"}
    env.clock.t += 600
    env.run()
    assert len([v for v in env.s3.versions if v[0] == "trace"]) == 2


def test_a_future_issuer_time_is_a_finding_not_a_watermark(env):
    far, later = "f" * 64, "e" * 64
    env.ddb.put("REQ#" + far, fakes.request(far, "REFUSED", T0 + 30 * 86400, reason="TOO_LARGE"))
    env.run()
    assert "ISSUER_TIME_IN_FUTURE" in env.codes()
    env.clock.t += 600
    env.ddb.put("REQ#" + later, fakes.request(later, "REFUSED", T0 + 100, reason="TOO_LARGE"))
    env.run()
    assert f"trace/{later}.json" in env.traces()


def test_seen_keys_are_forgotten_only_when_the_item_leaves_the_table(env):
    r1 = "1" * 64
    env.ddb.put("REQ#" + r1, fakes.request(r1, "REFUSED", T0 - 100, reason="TOO_LARGE"))
    env.ddb.put("SIGLOG#1", fakes.siglog(T0 - 60, slot="gpg"))
    env.run()
    env.clock.t += 40 * 86400
    env.run()
    st = env.state()
    assert r1 in st["req"]["seen"] and len(st["siglog"]["seen"]) == 1
    del env.ddb.items["REQ#" + r1]
    env.clock.t += 600
    env.run()
    assert r1 not in env.state()["req"]["seen"]
    assert len([v for v in env.s3.versions if v[0] == "trace"]) == 1


def test_live_requests_are_not_traced(env):
    rec = fakes.request("1" * 64, "ACCEPTED", T0)
    rec["ended_at"] = None
    env.ddb.put("REQ#" + "1" * 64, rec)
    env.run()
    assert env.traces() == {} and env.state()["pending"] == {}


def test_heartbeat_after_each_committed_run(env):
    for _ in range(3):
        env.run()
        env.clock.t += 600
    assert [ns for ns, _ in env.cw.beats] == ["Tessera/Watcher"] * 3
    assert env.cw.beats[0][1][0]["MetricName"] == "Heartbeat"


def test_a_source_that_cannot_be_read_is_a_finding_and_withholds_the_heartbeat(env):
    env.ddb.scan = lambda **kw: (_ for _ in ()).throw(fakes.ClientError("AccessDeniedException"))
    env.run()
    msg = json.loads(env.sns.sent[0]["Message"])
    assert msg["code"] == "SOURCE_UNAVAILABLE" and msg["source"] == "issuer_table" and env.cw.beats == []


def test_watcher_never_writes_to_issuer_stores(env):
    r1 = "1" * 64
    env.ddb.put("REQ#" + r1, fakes.request(r1, "REFUSED", T0 - 100, reason="TOO_LARGE"))
    env.ddb.put("SIGLOG#1", fakes.siglog(T0 - 60))
    env.s3.put("results", f"result/{r1}/x.json", b"x")
    env.run()
    assert {c for c, _ in env.ddb.calls} == {"scan"}
    assert {b for b, k, _ in env.s3.versions} <= {"state", "trace"}
    assert json.dumps(env.state())                         # state is plain JSON
