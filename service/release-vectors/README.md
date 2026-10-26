# Release-format gpgv test vectors (profile section 15.9 R3)

Section 15.9 accepts a distribution build of `gpgv` only if it reproduces upstream GnuPG 2.4.4's exit status on these
vectors. Pin: `formal/dependency-sources/MANIFEST.md`, entry `gpgv`.

**All keys here are THROWAWAY.** Three keys (stand-in "production", TEST, unrelated "wrong"), each v4 ECDSA P-256,
primary only, user id labelled THROWAWAY. None is or will be a release key. Private keys exist only in a fresh
`mktemp -d` GNUPGHOME under `work/` (gitignored; `~/.gnupg` is never touched). Only public keys (`keys/`), archives,
signatures, keyrings and `expected.json` are committed.

## Contents
- `generate.py` builds the keys, a minimal section 15.9 archive (15.8 part format, all required parts, generated
  `RELEASE.json`), and `cases/NN-name/{archive, archive.sig, keyring.pgp, expected.json}`. Regenerating makes new keys
  and signatures (ECDSA is non-deterministic), so commit regenerated output as a set.
- `run.py <gpgv>` runs `gpgv --keyring ... sig archive` per case with a scratch `--homedir`, reports match/mismatch
  against `gpgv_exit` (`"0"` or `"nonzero"`); exit 1 on any mismatch.
- `RESULTS.txt` records runs for Ubuntu's gpgv and upstream 2.4.4.

## Cases (9)
valid production; valid TEST (TEST keyring named explicitly); wrong key; TEST key as production (production keyring
only); truncated archive; signature over a different archive; corrupted signature; archive with an extra byte; and
09, TEST key offered as the keyring: gpgv exits 0 but `accept` is false, because acceptance also needs the signer to be
the R5-authenticated production fingerprint, which gpgv does not check. `expected.json` records both `gpgv_exit` and
`accept`. The acceptance-side checker (rule O grammar, fingerprint) is not tested here.

## Run
    python3 -I run.py /usr/bin/gpgv
    LD_LIBRARY_PATH=<libs> python3 -I run.py <path to upstream gpgv>
Upstream build used: the 2.4.4 tarball (sha256 matches the manifest) plus local builds of its libraries into
`work/up/inst`; no root needed.
