"""D5 (from SIGLOG#), D6 (slot 1 reconciliation), D7 (IAM writes from the trail): each path positive and negative.
Owner's unit tests over fakes; they show the code's logic, not that any alarm fires on the deployment."""
import io
import json

import pytest

import fakes
from conftest import T0
from tessera_watch import watcher as W


def D(env):
    return [json.loads(m["Message"]) for m in env.sns.sent]


# ------------------------------------------------------------------------------------------------------------- D5
@pytest.mark.parametrize("disposition", ["unrequested", "malformed", "bad-signature"])
def test_d5_dispositions_alarm(env, disposition):
    env.ddb.put("SIGLOG#1", fakes.siglog(T0 - 60, disposition=disposition))
    env.run()
    f = [x for x in D(env) if x["detection"] == "D5"]
    assert [x["code"] for x in f] == ["DISPOSITION_" + disposition.upper().replace("-", "_")]
    assert env.sns.sent[0]["Subject"].startswith("Tessera D5:")


@pytest.mark.parametrize("reason", sorted(W.D5_REASONS))
def test_d5_reasons_alarm(env, reason):
    env.ddb.put("SIGLOG#1", fakes.siglog(T0 - 60, status="REFUSED", disposition="refused", reason=reason))
    env.run()
    assert [x["code"] for x in D(env) if x["detection"] == "D5"] == ["REASON_" + reason]


@pytest.mark.parametrize("reason", ["SIGNING_STOPPED", "FRAME_UNAVAILABLE", "SIGNING_ERROR", "INTERNAL_ERROR", None])
def test_d5_ordinary_refusals_do_not_alarm(env, reason):
    env.ddb.put("SIGLOG#1", fakes.siglog(T0 - 60, slot="gpg", status="REFUSED", disposition="refused", reason=reason))
    env.run()
    assert D(env) == []


@pytest.mark.parametrize("disposition", ["used", "duplicate", "not-waiting", "other-attempt", "superseded:used"])
def test_d5_ordinary_dispositions_do_not_alarm(env, disposition):
    env.ddb.put("SIGLOG#1", fakes.siglog(T0 - 60, slot="gpg", disposition=disposition))
    env.run()
    assert D(env) == []


def test_d5_each_entry_reported_once_across_runs(env):
    env.ddb.put("SIGLOG#1", fakes.siglog(T0 - 60, disposition="unrequested", slot="gpg"))
    env.run()
    env.clock.t += 600
    env.run()
    assert env.codes() == ["DISPOSITION_UNREQUESTED"]


def test_d5_unreadable_siglog_item(env):
    env.ddb.items["SIGLOG#bad"] = {"pk": {"S": "SIGLOG#bad"}, "doc": {"S": "{not json"}}
    env.run()
    for _ in range(3):
        env.clock.t += 2 * W.OVERLAP_S
        env.run()
    assert env.codes() == ["SIGLOG_UNREADABLE"]             # reported once, not again after the watermark moves


# ------------------------------------------------------------------------------------------------------------- D6
def kms_signed(env, pk, at, sig=None, disposition="used", request_id="kms-req-1"):
    e = fakes.siglog(at, sig=sig, disposition=disposition, request_id=request_id)
    env.ddb.put(pk, e)
    return e


def test_d6_matched_one_to_one_no_alarm(env):
    env.trail(T0 - 1800, [fakes.sign_event(T0 - 1900), fakes.sign_event(T0 - 1890)])
    kms_signed(env, "SIGLOG#1", T0 - 1500)
    kms_signed(env, "SIGLOG#2", T0 - 1490, request_id="kms-req-2")
    env.run()
    env.clock.t += 2 * 3600
    env.run()
    assert D(env) == []
    st = env.state()
    assert all(s["sig"] for s in st["signs"].values()) and all(s["event"] for s in st["sigs"].values())


def test_d6_one_more_sign_than_signatures_alarms_after_the_window(env):
    env.trail(T0 - 300, [fakes.sign_event(T0 - 400), fakes.sign_event(T0 - 390)])
    kms_signed(env, "SIGLOG#1", T0 - 200)
    env.run()
    assert D(env) == []                                     # still inside the match window
    env.clock.t = T0 - 390 + W.MATCH_WINDOW_S + 1
    env.run()
    assert env.codes() == ["SIGN_WITHOUT_SIGNED_JOB"]
    env.clock.t += 600
    env.run()
    assert env.codes() == ["SIGN_WITHOUT_SIGNED_JOB"]       # reported once


def test_d6_repeated_siglog_entries_of_one_signature_account_for_one_sign(env):
    env.trail(T0 - 3000, [fakes.sign_event(T0 - 3000), fakes.sign_event(T0 - 2990)])
    h = fakes.sha(b"one signature")
    kms_signed(env, "SIGLOG#USED#x", T0 - 2900, sig=h)
    kms_signed(env, "SIGLOG#2", T0 - 2890, sig=h, disposition="superseded:not-waiting")
    kms_signed(env, "SIGLOG#3", T0 - 2880, sig=h, disposition="duplicate")
    env.clock.t = T0 + W.MATCH_WINDOW_S
    env.run()
    assert env.codes() == ["SIGN_WITHOUT_SIGNED_JOB"]       # two Signs, one signature


def test_d6_a_resend_with_a_new_signature_accounts_for_its_own_sign(env):
    env.trail(T0 - 3000, [fakes.sign_event(T0 - 3000), fakes.sign_event(T0 - 2400)])
    kms_signed(env, "SIGLOG#1", T0 - 2900)
    kms_signed(env, "SIGLOG#2", T0 - 2300, disposition="duplicate")
    env.clock.t = T0 + W.MATCH_WINDOW_S
    env.run()
    assert D(env) == []


@pytest.mark.parametrize("disposition", ["unrequested", "malformed", "bad-signature"])
def test_d6_non_job_responses_do_not_account_for_a_sign(env, disposition):
    env.trail(T0 - 3000, [fakes.sign_event(T0 - 3000)])
    kms_signed(env, "SIGLOG#1", T0 - 2900, disposition=disposition)
    env.clock.t = T0 + W.MATCH_WINDOW_S
    env.run()
    assert "SIGN_WITHOUT_SIGNED_JOB" in env.codes()


def test_d6_sign_after_its_signature_or_too_early_does_not_match(env):
    env.trail(T0 - 5000, [fakes.sign_event(T0 - 5000)])        # far before: outside [at - window, at + skew]
    kms_signed(env, "SIGLOG#1", T0 - 5000 + W.MATCH_WINDOW_S + 60)
    env.clock.t = T0 + 2 * 3600
    env.run()
    assert sorted(env.codes()) == ["SIGNATURE_WITHOUT_SIGN_EVENT", "SIGN_WITHOUT_SIGNED_JOB"]


def test_d6_signature_without_sign_event_after_lag(env):
    env.run()                                                   # first run: coverage starts at T0 - LOOKBACK
    kms_signed(env, "SIGLOG#1", T0 + 100)
    env.clock.t = T0 + 100 + W.CT_LAG_S - 1
    env.run()
    assert D(env) == []
    env.clock.t = T0 + 100 + W.CT_LAG_S + 1
    env.run()
    assert env.codes() == ["SIGNATURE_WITHOUT_SIGN_EVENT"]


def test_d6_signature_before_trail_coverage_is_not_an_alarm(env):
    kms_signed(env, "SIGLOG#1", T0 - 5 * 86400)
    env.run()
    assert D(env) == []
    assert env.state()["sigs"][next(iter(env.state()["sigs"]))]["before_coverage"] is True


def test_d6_gpg_signatures_are_not_reconciled_against_kms(env):
    env.ddb.put("SIGLOG#1", fakes.siglog(T0 - 3000, slot="gpg"))
    env.clock.t = T0 + 2 * 3600
    env.run()
    assert D(env) == []


def test_d6_sign_by_other_principal_alarms_and_is_not_matched(env):
    env.trail(T0 - 300, [fakes.sign_event(T0 - 400, role=fakes.OTHER_ROLE)])
    kms_signed(env, "SIGLOG#1", T0 - 200)
    env.run()
    assert env.codes() == ["SIGN_BY_OTHER_PRINCIPAL"]
    env.clock.t += W.CT_LAG_S + 60
    env.run()
    assert env.codes() == ["SIGN_BY_OTHER_PRINCIPAL", "SIGNATURE_WITHOUT_SIGN_EVENT"]
    f = D(env)[0]
    assert f["principal"] == fakes.OTHER_ROLE and f["event_name"] == "Sign"


def test_d6_access_denied_on_key_alarms(env):
    env.trail(T0 - 300, [fakes.sign_event(T0 - 400, role=fakes.OTHER_ROLE, error="AccessDenied")])
    env.run()
    assert env.codes() == ["ACCESS_DENIED_ON_KEY"]


def test_d6_no_trail_events_no_siglog_no_alarm(env):
    env.trail(T0 - 300, [fakes.sign_event(T0 - 400, key="arn:aws:kms:us-east-2:1:key/other")])
    env.run()
    assert D(env) == []
    assert len(env.cw.beats) == 1


def test_d6_late_trail_file_still_matches(env):
    kms_signed(env, "SIGLOG#1", T0 - 600)
    env.run()
    env.clock.t = T0 + 900                                     # the file arrives 25 min after the Sign
    env.trail(T0 + 800, [fakes.sign_event(T0 - 700)])
    env.run()
    env.clock.t = T0 + 3 * 3600
    env.run()
    assert D(env) == []


# ------------------------------------------------------------------------------------------------------------- D7
def test_d7_iam_write_alarms_with_latency_note(env):
    env.trail(T0 - 300, [fakes.iam_event(T0 - 400, name="UpdateAssumeRolePolicy")], region="us-east-1")
    env.run()
    f = D(env)
    assert [x["code"] for x in f] == ["IAM_WRITE"] and f[0]["event_name"] == "UpdateAssumeRolePolicy"
    assert "delivery" in f[0]["latency_note"]
    assert env.sns.sent[0]["Subject"] == "Tessera D7: IAM change in the issuing account (IAM_WRITE)"


def test_d7_iam_reads_do_not_alarm(env):
    env.trail(T0 - 300, [fakes.iam_event(T0 - 400, name="ListRoles", read_only=True)], region="us-east-1")
    env.run()
    assert D(env) == []


def test_findings_are_logged_as_json_lines_too(env):
    env.out = io.StringIO()
    env.trail(T0 - 300, [fakes.iam_event(T0 - 400)], region="us-east-1")
    env.run()
    lines = [json.loads(x) for x in env.out.getvalue().splitlines()]
    assert [x["event"] for x in lines] == ["finding", "watch_summary"]
    assert lines[0]["detection"] == "D7" and lines[0]["v"] == 1


def test_unreadable_trail_file_is_reported_once(env):
    env.s3.put("trail", fakes.trail_key(T0 - 300), b"garbage")
    env.run()
    env.clock.t += 600
    env.run()
    assert env.codes() == ["TRAIL_FILE_UNREADABLE"]
