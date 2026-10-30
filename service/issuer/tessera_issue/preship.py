"""Pre-ship checks (profile 4 and 15.7): the assembled bundle is verified with the service verifier's own logic,
called as a library, under the issuer's check configuration: the window's root KSK and repository-key entries plus
pins for exactly the headers the issuer fetched and checked. Anything but VALID_STRICT / OK is not shipped.

The SHA-1DC detector the verifier needs is configured from the verifier's per-installation record (install.json,
profile 15.9 R2); without a functional detector the check refuses to run (PreShipUnavailable), never passes."""
from tessera_verify import install_record
from tessera_verify.codec import Fault
from tessera_verify.policy import parse_trust
from tessera_verify.verify import verify_bundle

from .chain import pin_of
from .util import D, PROFILE, jcs, rfc3339


class PreShipUnavailable(Exception):
    pass


def trust_object(trust_base, pins, as_of):
    return {"as_of": as_of, "format": "tessera-v1-trust/1",
            "header_pins": {str(h): v for h, v in sorted(pins.items())} or {"0": "0" * 64},
            "issuer_domain": D, "previous_sha256": "0" * 64, "profile": PROFILE,
            "repository_keys": trust_base["repository_keys"], "root_ksks": trust_base["root_ksks"], "version": "1"}


def check_config(trust_base, pins, as_of):
    """The parsed configuration (service verifier parser), or raises Fault."""
    return parse_trust(jcs(trust_object(trust_base, pins, as_of)))


class PreShip:
    def __init__(self, frozen, trust_base, install_record_path=None):
        self.frozen, self.trust_base, self.path = frozen, trust_base, install_record_path
        self._ready = False

    def _setup(self):
        if not self._ready:
            try:
                install_record.load_and_apply(self.path)
            except Fault as e:
                raise PreShipUnavailable(e.code) from None
            self._ready = True

    def check(self, bundle, headers, now, diagnostics=False):
        """-> (stable six, utc_assessment), or with diagnostics (stable six, utc_assessment, ledger): the verifier's
        per-row checks, which the poller classifies by evidence dependency (ILI-01). headers: {height: 80 bytes} the
        issuer fetched and checked."""
        self._setup()
        latest = max(int.from_bytes(h[68:72], "little") for h in headers.values())
        config = check_config(self.trust_base, {h: pin_of(v) for h, v in headers.items()}, rfc3339(max(now, latest)))
        try:
            return verify_bundle(bundle, config, self.frozen.parsed_catalog, utc=True, diagnostics=diagnostics)
        except Fault as e:                      # e.g. SHA1DC_UNAVAILABLE raised by the engine itself
            raise PreShipUnavailable(e.code) from None
