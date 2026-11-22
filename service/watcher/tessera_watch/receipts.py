"""D8: re-verify a receipt as a relying party would (docs/smoke/2026-11-16-first-receipt/rp_verify.py).

Trust is built from the window's own entries (the packaged window.json, not the issuer's copy in its bucket) plus pins
of the bundle's Bitcoin headers fetched from two block explorers that must agree. The frozen service verifier
(tessera_verify) is then run as a separate process, in its explicit TEST mode, with a TEST release signed by a fresh
P-256 key made for this one check (the production release does not exist yet; the same as rp_verify.py). Nothing here
imports issuer code: the trust object and the TEST release record are built from the verifier's documented formats.

The one result that passes is stable.verdict == VALID_STRICT. A check that cannot be carried out (explorers down or in
disagreement, the verifier refusing to start) raises Unavailable; it is not a verdict and the caller retries it."""
import base64
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

import tessera_verify
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
from tessera_verify.codec import jcs
from tessera_verify.release_auth import TEST_FORMAT, jcs_ascii

ISSUER_DOMAIN = "wamason.com"                 # the window's issuer domain (V1 contract); the trust object's field
PROFILE = "tessera-v1-strict"
CATALOG_SHA256 = "aaf4306fed070119022c8486219f5160dc869edaa929f323d962fbb679e27fc2"   # formal/freeze-v1/FREEZE-RECORD.md
PASS = "VALID_STRICT"
CODE_RE = re.compile(r"[A-Z][A-Z0-9_]{0,63}")
UA = "tessera-watcher"


class Unavailable(Exception):
    """The check could not be made (not a verdict). .code is a bounded code, never free text."""

    def __init__(self, code):
        super().__init__(code)
        self.code = code


def load_catalog(path):
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != CATALOG_SHA256:
        raise Unavailable("CATALOG_NOT_FROZEN")
    return json.loads(raw)


def load_window(path):
    w = json.loads(Path(path).read_text())
    if w.get("format") != "tessera-v1-window/1" or not isinstance(w.get("trust_base"), dict):
        raise Unavailable("WINDOW_FORMAT")
    return w


def pin_of(header):
    """Block hash in display order (hex), the trust object's header pin."""
    return hashlib.sha256(hashlib.sha256(header).digest()).digest()[::-1].hex()


def bundle_heights(bundle):
    """Heights of the bundle's Bitcoin headers, or [] if the bundle does not parse (the verifier then judges it)."""
    try:
        layers = json.loads(bundle)["layers"]
        return sorted({int(h) for layer in layers for h in layer["headers"]})
    except (ValueError, KeyError, TypeError, AttributeError):
        return []


def http_get(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:      # noqa: S310  fixed https explorer bases
        return r.read(1 << 16).decode("ascii").strip()


def explorer_headers(heights, explorers, get=http_get):
    """{height: 80-byte header}, each fetched from every explorer; all must agree (rp_verify.py's rule)."""
    if len(explorers) < 2:
        raise Unavailable("EXPLORERS_TOO_FEW")
    out = {}
    for h in heights:
        got = []
        for api in explorers:
            try:
                bh = get(f"{api}/block-height/{int(h)}")
                if not re.fullmatch(r"[0-9a-f]{64}", bh):
                    raise ValueError("hash")
                hdr = bytes.fromhex(get(f"{api}/block/{bh}/header"))
            except Exception:  # noqa: BLE001  any failure of one explorer: the check is not possible now
                raise Unavailable("EXPLORER_UNAVAILABLE") from None
            if len(hdr) != 80 or pin_of(hdr) != bh:
                raise Unavailable("EXPLORER_BAD_HEADER")
            got.append(hdr)
        if any(g != got[0] for g in got):
            raise Unavailable("EXPLORERS_DISAGREE")
        out[h] = got[0]
    return out


def trust_bytes(window, headers, as_of):
    pins = {str(h): pin_of(v) for h, v in sorted(headers.items())} or {"0": "0" * 64}
    return jcs({"as_of": as_of, "format": "tessera-v1-trust/1", "header_pins": pins, "issuer_domain": ISSUER_DOMAIN,
                "previous_sha256": "0" * 64, "profile": PROFILE,
                "repository_keys": window["trust_base"]["repository_keys"],
                "root_ksks": window["trust_base"]["root_ksks"], "version": "1"})


def test_release(trust, catalog):
    """A tessera-v1-test-release/1 record and key file, signed by a P-256 key made for this check and discarded."""
    cat = dict(catalog, TEST="frozen catalog provisioned for a watcher relying-party check; TEST authority only")
    body = {"catalog": cat, "catalog_sha256": hashlib.sha256(jcs_ascii(cat)).hexdigest(), "format": TEST_FORMAT,
            "trust_config_sha256": hashlib.sha256(trust).hexdigest()}
    key = ec.generate_private_key(ec.SECP256R1())
    r, s = decode_dss_signature(key.sign(jcs_ascii(body), ec.ECDSA(hashes.SHA256())))
    spki = key.public_key().public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
    spki_sha = hashlib.sha256(spki).hexdigest()
    rel = {"release": body, "signature": {"alg": "ECDSA-P256-SHA256", "r_s_hex": (r.to_bytes(32, "big") +
                                                                                 s.to_bytes(32, "big")).hex(),
                                          "signer_spki_sha256": spki_sha}}
    keyfile = {"TEST": "TEST release key of one watcher check", "spki_b64": base64.b64encode(spki).decode(),
               "spki_sha256": spki_sha}
    return json.dumps(rel).encode(), json.dumps(keyfile).encode()


def run_cli(workdir, install_json=None, timeout=600, python=None):
    """The verifier's CLI, as a separate process (as rp_verify.py runs it). -> (exit code, stdout, stderr)."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("TESSERA_V1_TEST_")}
    env["PYTHONPATH"] = str(Path(tessera_verify.__file__).resolve().parent.parent)   # where this process found it
    if install_json:
        env["TESSERA_VERIFY_INSTALL_JSON"] = str(install_json)
    w = Path(workdir)
    p = subprocess.run([python or sys.executable, "-m", "tessera_verify", "--mode", "test",
                        "--test-release", str(w / "release.json"), "--test-release-key", str(w / "release-key.json"),
                        "--trust", str(w / "trust.json"), "--bundle", str(w / "receipt.json")],
                       capture_output=True, text=True, timeout=timeout, cwd=str(w), env=env)
    return p.returncode, p.stdout, p.stderr


def verify(bundle, window, catalog, as_of, explorers, get=http_get, cli=run_cli, tmp=None):
    """-> {"verdict", "reason", "heights"}; raises Unavailable if no verdict could be obtained."""
    heights = bundle_heights(bundle)
    headers = explorer_headers(heights, explorers, get)
    trust = trust_bytes(window, headers, as_of)
    rel, key = test_release(trust, catalog)
    with tempfile.TemporaryDirectory(dir=tmp) as d:
        for name, data in (("trust.json", trust), ("release.json", rel), ("release-key.json", key),
                           ("receipt.json", bundle)):
            (Path(d) / name).write_bytes(data)
        try:
            code, out, err = cli(d)
        except subprocess.TimeoutExpired:
            raise Unavailable("VERIFIER_TIMEOUT") from None
    if code != 0:
        first = (err or "").strip().split(":")[0].strip()
        raise Unavailable("VERIFIER_REFUSED:" + (first if CODE_RE.fullmatch(first) else "UNKNOWN"))
    try:
        stable = json.loads(out)["stable"]
        verdict, reason = stable["verdict"], stable["reason"]
    except (ValueError, KeyError, TypeError):
        raise Unavailable("VERIFIER_OUTPUT") from None
    bounded = lambda v: v if isinstance(v, str) and CODE_RE.fullmatch(v.replace("/", "_")) else "UNPARSEABLE"  # noqa: E731
    return {"verdict": bounded(verdict), "reason": bounded(reason), "heights": heights, "T": stable.get("T")}
