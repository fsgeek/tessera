"""Window preparation data: the issuer loads it as data and refuses inconsistent authority evidence."""
import copy

import pytest

from tessera_issue import window as W
from tessera_issue.encode import EncodeError, assertion_value


def test_window_round_trips_and_checks(loc):
    w = loc.iss.window
    again = W.load_json(w.to_json())
    assert again.assertion == w.assertion and again.git == w.git and again.h_git == w.h_git
    assert len(w.assertion) == 255 and w.git["blob"] == w.assertion


@pytest.mark.parametrize("break_it", ["blob", "assertion", "ots", "format"])
def test_inconsistent_window_is_refused(loc, break_it):
    import json
    o = json.loads(loc.iss.window.to_json())
    if break_it == "blob":
        o["git"]["blob"] = o["git"]["trees"][1]
    elif break_it == "assertion":
        o["assertion"] = o["assertion"].replace("issuance-not-after=2026", "issuance-not-after=2027")
    elif break_it == "ots":
        o["git"]["ots"], o["git"]["commit"] = o["git"]["ots"], o["git"]["trees"][0]
    else:
        o["format"] = "other"
    with pytest.raises((W.WindowError, EncodeError, ValueError)):
        W.load_json(json.dumps(o))


def test_window_longer_than_90_days_or_noncanonical_is_refused(loc):
    w = loc.iss.window
    with pytest.raises(EncodeError):
        assertion_value(w.kms_fp, w.gpg_fp, "2026-11-01T00:00:00Z", "2027-02-01T00:00:00Z")
    with pytest.raises((EncodeError, ValueError)):
        assertion_value(w.kms_fp, w.gpg_fp, "2026-11-01T00:00:00+00:00", "2026-12-01T00:00:00Z")
