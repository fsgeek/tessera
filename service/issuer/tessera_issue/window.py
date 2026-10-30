"""The issuance window and its authority evidence, prepared by the operator before the window opens (DESIGN.md
"Window preparation": a runbook step, not an API path) and loaded by the issuer as data.

window.json: {"format": "tessera-v1-window/1", "not_before", "not_after", "keys": {"kms", "gpg"} (base64),
"assertion" (the 255-byte value), "git": {"commit", "trees": [root, sub], "blob", "ots"} (base64),
"trust_base": {"root_ksks": [...], "repository_keys": [...]} (profile 15.5 entries the pre-ship check uses)}.

Margins (V1-SERVICE-RESOLUTIONS L1, revised 2026-10-29): signing stops 96 h before not-after; acceptance stops
delta + S + 24 h before signing stops (216 h before not-after). This is an operating allowance, not a processing
guarantee: it leaves a first attempt started promptly room for its nominal delta + S before signing stops, but
allocation can be delayed (polling, outages, a slow upload), and a later attempt that would need signing after the
stop is refused SIGNING_CLOSED (A2.3 budgets are nominal, not wall-clock bounds)."""
import json
from dataclasses import dataclass

from tessera_verify.git_channel import object_id, parse_commit, verify_path
from tessera_verify.codec import Fault

from . import ots
from .encode import assertion_value, fp_gpg, fp_kms
from .service import SLACK_S
from .util import DELTA, HOUR, b64d, b64e, sha256, ts

SIGN_MARGIN = 96 * HOUR
ACCEPT_MARGIN = SIGN_MARGIN + DELTA + SLACK_S + 24 * HOUR          # L1: 216 h


class WindowError(Exception):
    pass


@dataclass
class Window:
    not_before: str
    not_after: str
    kms_key: bytes
    gpg_key: bytes
    assertion: bytes
    git: dict                   # bytes values: commit, trees (list of 2), blob, ots
    trust_base: dict

    @property
    def nb(self):
        return ts(self.not_before)

    @property
    def na(self):
        return ts(self.not_after)

    @property
    def accept_until(self):
        return self.na - ACCEPT_MARGIN

    @property
    def sign_until(self):
        return self.na - SIGN_MARGIN

    @property
    def kms_fp(self):
        return fp_kms(self.kms_key)

    @property
    def gpg_fp(self):
        return fp_gpg(self.gpg_key)

    @property
    def git_stamp_input(self):
        return (object_id("commit", self.git["commit"]) + "\n").encode()

    @property
    def h_git(self):
        return ots.lowest_btc_height(self.git["ots"])

    def to_json(self):
        g = self.git
        return json.dumps({"format": "tessera-v1-window/1", "not_before": self.not_before, "not_after": self.not_after,
                           "keys": {"kms": b64e(self.kms_key), "gpg": b64e(self.gpg_key)},
                           "assertion": self.assertion.decode("ascii"),
                           "git": {"commit": b64e(g["commit"]), "trees": [b64e(t) for t in g["trees"]],
                                   "blob": b64e(g["blob"]), "ots": b64e(g["ots"])},
                           "trust_base": self.trust_base}, sort_keys=True, indent=1)

    def check(self):
        """Self-consistency (no chain access): value, keys, git path, blob, the git proof's digest."""
        if self.assertion != assertion_value(self.kms_fp, self.gpg_fp, self.not_before, self.not_after):
            raise WindowError("assertion value does not match the keys and window")
        g = self.git
        if g["blob"] != self.assertion:
            raise WindowError("git blob differs from the assertion value")
        try:
            tree, _, _ = parse_commit(g["commit"])
            verify_path(tree, g["trees"], g["blob"])
        except Fault as e:
            raise WindowError("git evidence: " + e.code) from None
        digest, _ = ots.parse_file(g["ots"])
        if digest != sha256(self.git_stamp_input):
            raise WindowError("git proof does not stamp the commit id")
        if self.accept_until <= self.nb:
            raise WindowError("window shorter than the acceptance margin")
        return self


def load_json(text):
    o = json.loads(text)
    if o.get("format") != "tessera-v1-window/1":
        raise WindowError("window format")
    g = o["git"]
    return Window(o["not_before"], o["not_after"], b64d(o["keys"]["kms"]), b64d(o["keys"]["gpg"]),
                  o["assertion"].encode("ascii"),
                  {"commit": b64d(g["commit"]), "trees": [b64d(t) for t in g["trees"]], "blob": b64d(g["blob"]),
                   "ots": b64d(g["ots"])}, o["trust_base"]).check()
