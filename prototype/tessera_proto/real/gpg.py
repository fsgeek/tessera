"""Real OpenPGP signing with /usr/bin/gpg in a throwaway GNUPGHOME under prototype/. THROWAWAY.

The home lives under prototype/.gnupg-phase3/<random>/ (mode 0700) and is removed by `close()`.
Keys are passphraseless and generated per run; nothing touches the user's own keyring.

Also: the OpenPGP signer-slot keys used by the de-stubbed world, and a KMS-backed OpenPGP signer
(the private half in emulated KMS, the OpenPGP packet assembled locally, KMS called with DIGEST).
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import utils

from . import openpgp as P
from .kms import KmsKey

GPG = "/usr/bin/gpg"
PROTO_DIR = Path(__file__).resolve().parents[2]          # prototype/
HOMES_DIR = PROTO_DIR / ".gnupg-phase3"

ALG_PGP_P256 = "OPENPGP4-ECDSA-P256-SHA256"
ALG_PGP_ED25519 = "OPENPGP4-EDDSA-ED25519-SHA256"
PGP_ALGS = {ALG_PGP_P256: (P.PK_ECDSA, P.H_SHA256), ALG_PGP_ED25519: (P.PK_EDDSA_LEGACY, P.H_SHA256)}


def available() -> bool:
    return os.path.exists(GPG)


class GpgHome:
    def __init__(self):
        HOMES_DIR.mkdir(mode=0o700, exist_ok=True)
        self.path = Path(tempfile.mkdtemp(prefix="h", dir=HOMES_DIR))
        os.chmod(self.path, 0o700)
        (self.path / "gpg-agent.conf").write_text("allow-loopback-pinentry\n")

    def run(self, *args: str, input: bytes | None = None, check: bool = True) -> subprocess.CompletedProcess:
        cmd = [GPG, "--homedir", str(self.path), "--batch", "--no-tty", "--pinentry-mode", "loopback",
               "--passphrase", "", *args]
        r = subprocess.run(cmd, input=input, capture_output=True, timeout=120)
        if check and r.returncode != 0:
            raise RuntimeError(f"gpg {' '.join(args)} failed: {r.stderr.decode(errors='replace')}")
        return r

    def gen_key(self, uid: str, algo: str = "nistp256") -> str:
        self.run("--quick-gen-key", uid, algo, "sign", "never")
        out = self.run("--with-colons", "--list-keys", uid).stdout.decode()
        return re.search(r"^fpr:+([0-9A-F]{40}):", out, re.M).group(1)

    def keygrip(self, fpr: str) -> str:
        out = self.run("--with-colons", "--with-keygrip", "--list-secret-keys", fpr).stdout.decode()
        return re.search(r"^grp:+([0-9A-F]{40}):", out, re.M).group(1)

    def export(self, fpr: str) -> bytes:
        return self.run("--export", fpr).stdout

    def import_key(self, data: bytes) -> subprocess.CompletedProcess:
        return self.run("--import", input=data, check=False)

    def detach_sign(self, fpr: str, data: bytes, digest: str = "SHA256") -> bytes:
        return self.run("-u", fpr, "--digest-algo", digest, "--detach-sign", "-o", "-", input=data).stdout

    def verify(self, sig: bytes, data: bytes) -> tuple[bool, str]:
        d = Path(tempfile.mkdtemp(prefix="v", dir=self.path))
        (d / "sig").write_bytes(sig)
        (d / "data").write_bytes(data)
        r = self.run("--status-fd", "1", "--verify", str(d / "sig"), str(d / "data"), check=False)
        shutil.rmtree(d)
        st = r.stdout.decode(errors="replace")
        return ("[GNUPG:] GOODSIG" in st or "[GNUPG:] VALIDSIG" in st) and r.returncode == 0, st

    def agent_pksign(self, fpr: str, digest: bytes) -> tuple[int, int]:
        """Ask gpg-agent to sign a raw SHA-256 digest with the GPG-held key -- no OpenPGP packet, no
        trailer. This is the only way found to get a GPG-custodied key to sign SHA-256(frame) exactly."""
        grip = self.keygrip(fpr)
        script = f"SIGKEY {grip}\nSETHASH --hash=sha256 {digest.hex()}\nPKSIGN\n/bye\n"
        r = subprocess.run(["gpg-connect-agent", "--homedir", str(self.path)], input=script.encode(),
                           capture_output=True, timeout=60)
        # Assuan data lines: "D <percent-escaped bytes>", possibly several; join, then unescape
        raw = b"".join(ln[2:] for ln in r.stdout.split(b"\n") if ln.startswith(b"D "))
        out = re.sub(rb"%([0-9A-Fa-f]{2})", lambda m: bytes([int(m.group(1), 16)]), raw)
        m_r = re.search(rb"\(1:r(\d+):", out)
        m_s = re.search(rb"\(1:s(\d+):", out)
        if not (m_r and m_s):
            raise RuntimeError(f"PKSIGN failed: {out!r} {r.stderr!r}")
        def grab(m):
            n = int(m.group(1))
            return int.from_bytes(out[m.end():m.end() + n], "big")
        return grab(m_r), grab(m_s)

    def close(self):
        subprocess.run(["gpgconf", "--homedir", str(self.path), "--kill", "all"], capture_output=True, timeout=30)
        shutil.rmtree(self.path, ignore_errors=True)


# ------------------------------------------------------------------ signer-slot keys (KeyPair shape)

@dataclass
class GpgSlotKey:
    """Slot key whose private half is held by real gpg. sign() returns an OpenPGP v4 signature packet
    over the given bytes (binary document, SHA-256). pub_raw is the v4 public-key PACKET."""
    label: str
    home: GpgHome
    fpr: str
    alg: str = ALG_PGP_P256
    _pub: bytes = field(default=b"", repr=False)

    @classmethod
    def generate(cls, label: str, home: GpgHome, alg: str = ALG_PGP_P256) -> "GpgSlotKey":
        algo = "nistp256" if alg == ALG_PGP_P256 else "ed25519"
        fpr = home.gen_key(f"Tessera proto {label} {os.urandom(4).hex()} <{label}@proto.invalid>", algo)
        k = P.first_public_key(home.export(fpr))
        return cls(label, home, fpr, alg, P.new_packet(6, k.body))

    @property
    def pub_raw(self) -> bytes:
        return self._pub

    @property
    def fp(self) -> str:
        from ..crypto import fingerprint
        return fingerprint(self.alg, self.pub_raw)

    def sign(self, msg: bytes) -> bytes:
        return P.parse_signature(self.home.detach_sign(self.fpr, msg)).raw


@dataclass
class KmsOpenPGPSlotKey:
    """Slot key whose private half is in (emulated) KMS, producing OpenPGP v4 signatures: the packet
    and trailer are assembled locally and KMS is called with MessageType=DIGEST on
    SHA-256(document || trailer). Same scheme and algorithm id as a gpg nistp256 key."""
    label: str
    kms: KmsKey
    created: int
    alg: str = ALG_PGP_P256

    @classmethod
    def generate(cls, label: str, created: int | None = None) -> "KmsOpenPGPSlotKey":
        return cls(label, KmsKey.create("ECC_NIST_P256"), created or int(time.time()))

    @property
    def key(self) -> P.PublicKey:
        pub = serialization.load_der_public_key(self.kms.get_public_key())
        return P.parse_public_key_body(P.ecdsa_p256_key_body(pub, self.created))

    @property
    def pub_raw(self) -> bytes:
        return P.new_packet(6, self.key.body)

    @property
    def fp(self) -> str:
        from ..crypto import fingerprint
        return fingerprint(self.alg, self.pub_raw)

    def _sign_digest(self, d: bytes) -> tuple[int, int]:
        return utils.decode_dss_signature(self.kms.sign(d, "DIGEST", "ECDSA_SHA_256"))

    def sign(self, msg: bytes, created: int | None = None) -> bytes:
        return P.build_signature(msg, self.key, created or int(time.time()), self._sign_digest)

    def transferable(self, uid: str) -> bytes:
        return P.transferable_public_key(self.key, uid.encode(), self.created, self._sign_digest)


def verify_openpgp_slot(alg: str, pub_packet: bytes, sig_packet: bytes, msg: bytes) -> bool:
    """The verifier side for the OPENPGP4-* algorithm ids: the frame is the OpenPGP 'document'.
    The id pins public-key algorithm and hash; anything else in the packets is refused."""
    try:
        key = P.first_public_key(pub_packet)
        sig = P.parse_signature(sig_packet)
    except (P.PGPError, IndexError, ValueError):
        return False
    pk, h = PGP_ALGS[alg]
    if key.alg != pk or sig.pk_alg != pk or sig.hash_alg != h:
        return False
    return P.verify(sig, key, msg)
