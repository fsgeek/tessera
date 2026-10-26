#!/usr/bin/env python3
"""Generate the section 15.9 release-format gpgv test vectors.

Everything secret lives in a fresh GNUPGHOME made by `mktemp -d` inside work/
(gitignored). ~/.gnupg is never touched. All keys are THROWAWAY.
Run:  python3 -I generate.py
"""
import hashlib, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "work")
CASES = os.path.join(HERE, "cases")
KEYS = os.path.join(HERE, "keys")


def sh(args, **kw):
    return subprocess.run(args, check=True, capture_output=True, **kw)


def jcs(obj):  # sufficient JCS for ASCII string/null/object values
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def sha(b):
    return hashlib.sha256(b).hexdigest()


def assemble(parts):
    out = b""
    for path in sorted(parts):  # bytewise-sorted (ASCII paths)
        b = parts[path]
        out += b"tessera-v1-part %s %d\n" % (path.encode(), len(b)) + b + b"\n"
    return out


def build_archive(namespace, n):
    """Minimal conforming 15.9 R1/R2 archive: every required part, RELEASE.json generated."""
    catalog = b'{"THROWAWAY":"stand-in catalog"}\n'
    trust = b'{"THROWAWAY":"stand-in trust config","version":"0"}\n'
    consts = (
        'NAMESPACE = "%s"\nTRUST_SHA256 = "%s"\nCATALOG_SHA256 = "%s"\n'
        'CATALOG_BYTES = %r\nUNICODE_VERSION = "16.0.0"\n'
        % (namespace, sha(trust), sha(catalog), catalog)
    ).encode()
    parts = {
        "trust.json": trust,
        "catalog.json": catalog,
        "release_constants.py": consts,
        "requirements.lock": b"# THROWAWAY dependency lock\n",
        "sha1dc/SHA1DC-PIN.md": b"THROWAWAY stand-in pin\n",
        "sha1dc/sha1.c": b"/* THROWAWAY stand-in vendored source */\n",
        "install.sh": b"#!/bin/sh\necho THROWAWAY stand-in installer\n",
        "RELYING-PARTY.txt": b"THROWAWAY stand-in relying-party text\n",
        "verifier/verify.py": b"print('THROWAWAY stand-in verifier code')\n",
    }
    manifest = {
        "format": "tessera-v1-release/1",
        "namespace": namespace,
        "release": str(n),
        "profile": "tessera-v1-strict",
        "source_commit": "0" * 40,
        "trust_config_sha256": sha(trust),
        "trust_config_version": "0",
        "catalog_sha256": sha(catalog),
        "freeze_record_sha256": "0" * 64,
        "parts": {p: sha(b) for p, b in parts.items()},
        "release_key_successor": None,
    }
    parts["RELEASE.json"] = jcs(manifest)
    return assemble(parts)


def main():
    os.makedirs(WORK, exist_ok=True)
    home = sh(["mktemp", "-d", os.path.join(WORK, "gnupghome.XXXXXX")]).stdout.decode().strip()
    os.chmod(home, 0o700)
    env = dict(os.environ, GNUPGHOME=home)
    gpg = ["gpg", "--homedir", home, "--batch", "--no-tty", "--pinentry-mode", "loopback",
           "--passphrase", ""]

    def genkey(uid):
        sh(gpg + ["--quick-generate-key", uid, "nistp256", "sign", "never"], env=env)
        out = sh(gpg + ["--with-colons", "--fingerprint", "--list-keys", uid], env=env).stdout.decode()
        fprs = [l.split(":")[9] for l in out.splitlines() if l.startswith("fpr:")]
        return fprs[0]  # primary only; the key has no subkeys

    fp = {
        "production": genkey("THROWAWAY stand-in PRODUCTION key (not a release key) <throwaway-prod@invalid>"),
        "test": genkey("THROWAWAY TEST release key (not a release key) <throwaway-test@invalid>"),
        "wrong": genkey("THROWAWAY unrelated wrong key (not a release key) <throwaway-wrong@invalid>"),
    }
    os.makedirs(KEYS, exist_ok=True)
    for name, f in fp.items():  # public keys only
        pub = sh(gpg + ["--export", f], env=env).stdout
        assert pub
        with open(os.path.join(KEYS, name + ".pub.pgp"), "wb") as fh:
            fh.write(pub)
    with open(os.path.join(KEYS, "FINGERPRINTS.json"), "w") as fh:
        json.dump(fp, fh, indent=2, sort_keys=True)
        fh.write("\n")

    def sign(key, data_path, sig_path):
        sh(gpg + ["--local-user", fp[key] + "!", "--digest-algo", "SHA256", "--detach-sign",
                  "--output", sig_path, data_path], env=env)

    prod1 = build_archive("PRODUCTION", 1)
    prod2 = build_archive("PRODUCTION", 2)
    test1 = build_archive("TEST", 1)
    names = {"PRODUCTION": "tessera-verifier-v1-%d.parts", "TEST": "tessera-verifier-v1-TEST-%d.parts"}
    P1, P2, T1 = names["PRODUCTION"] % 1, names["PRODUCTION"] % 2, names["TEST"] % 1

    def flip(b, i):
        b = bytearray(b)
        b[i] ^= 0x01
        return bytes(b)

    # case: (archive name, archive bytes, signing archive (name, bytes), signer, sig tweak,
    #        keyring key, gpgv_exit, accept, description)
    # Signature is made over `signed`, then presented with `archive`.
    cases = [
        ("01-valid-production", P1, prod1, prod1, "production", None, "production", "0", True,
         "Valid signature by the production stand-in key over the whole archive; keyring holds only that key."),
        ("02-valid-test", T1, test1, test1, "test", None, "test", "0", True,
         "Valid TEST-key signature over a TEST archive, acquired against an explicitly named TEST keyring (R4 path a). Not a production acceptance."),
        ("03-wrong-key", P1, prod1, prod1, "wrong", None, "production", "nonzero", False,
         "Otherwise valid signature by an unrelated key; production keyring does not hold it (R3: any other key authenticates nothing)."),
        ("04-test-key-as-production", P1, prod1, prod1, "test", None, "production", "nonzero", False,
         "Correctly formed PRODUCTION archive signed only by the TEST key; keyring holds only the production key (R4: refusal is by key)."),
        ("05-truncated-archive", P1, prod1[:-7], prod1, "production", None, "production", "nonzero", False,
         "Archive truncated by 7 bytes; signature is the production signature over the full archive."),
        ("06-signature-over-different-archive", P1, prod1, prod2, "production", None, "production", "nonzero", False,
         "Valid production signature, but over release 2; presented with release 1."),
        ("07-signature-corrupted", P1, prod1, prod1, "production", "flip-last", "production", "nonzero", False,
         "Production signature with one bit flipped in its final byte (inside the s MPI)."),
        ("08-archive-extra-byte", P1, prod1 + b"\n", prod1, "production", None, "production", "nonzero", False,
         "Archive with one appended byte (LF); signature is over the original."),
        ("09-test-key-offered-as-key", P1, prod1, prod1, "test", None, "test", "0", False,
         "PRODUCTION archive signed by the TEST key, and the TEST public key is offered as the keyring (R4 rehearsal: 'including when the TEST public key is offered as the key'). "
         "gpgv itself exits 0 here; the refusal must come from the acquisition-side check that the signer is the R5-authenticated production fingerprint. "
         "Extra case beyond the owner's list."),
    ]
    os.makedirs(CASES, exist_ok=True)
    for (cid, aname, abytes, signed, signer, tweak, ring, gexit, accept, desc) in cases:
        d = os.path.join(CASES, cid)
        os.makedirs(d, exist_ok=True)
        tmp = os.path.join(home, "tosign")
        with open(tmp, "wb") as fh:
            fh.write(signed)
        sigp = os.path.join(d, aname + ".sig")
        sign(signer, tmp, sigp)
        if tweak == "flip-last":
            s = open(sigp, "rb").read()
            open(sigp, "wb").write(flip(s, len(s) - 1))
        with open(os.path.join(d, aname), "wb") as fh:
            fh.write(abytes)
        with open(os.path.join(d, "keyring.pgp"), "wb") as fh:
            fh.write(open(os.path.join(KEYS, ring + ".pub.pgp"), "rb").read())
        exp = {
            "case": cid,
            "description": desc,
            "archive": aname,
            "signature": aname + ".sig",
            "keyring": "keyring.pgp",
            "keyring_holds": ring,
            "signed_by": signer,
            "gpgv_exit": gexit,
            "accept": accept,
            "accept_basis": "section 15.9 R3 acceptance (trusted checker + pinned gpgv exit 0 + keyring holding only the R5-authenticated production key); case 02 is a TEST acceptance under R4(a).",
        }
        with open(os.path.join(d, "expected.json"), "w") as fh:
            json.dump(exp, fh, indent=2)
            fh.write("\n")
    subprocess.run(["gpgconf", "--homedir", home, "--kill", "all"], check=False)
    print("generated %d cases; private keys remain only in %s (gitignored)" % (len(cases), home))


if __name__ == "__main__":
    main()
