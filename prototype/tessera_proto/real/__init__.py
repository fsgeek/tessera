"""PHASE 3: real, standards-conformant mechanisms replacing the phase-1 stubs (THROWAWAY).

Nothing here is service code. Modules:

  canonical  RFC 8785 (JCS) number-domain readings, compared with the spec's precision rule (§3.1)
  openpgp    RFC 4880 / RFC 9580 v4 signature and key packets: parse, build, verify, fingerprint
  kms        AWS-KMS-style signing emulated locally with `cryptography` (ECDSA_SHA_256, RSASSA_PSS_SHA_256;
             RAW vs DIGEST message types). No AWS.
  gpg        /usr/bin/gpg in a throwaway GNUPGHOME under prototype/ (keygen, detached sign, gpg-agent PKSIGN)
  btc        Bitcoin block-header parsing, proof of work, linkage, merkle trees; a regtest-difficulty chain
  ots        OpenTimestamps proofs (python-opentimestamps): verify the repo's real Bitcoin-anchored stamps
             against archived mainnet headers; build real-format proofs on the regtest chain
  dnssec     RFC 4033-4035 offline validation of captured DNS answers (dnspython)
  gitchannel git commit-signature evidence: exactly what a signed commit covers, offline
  algs       registers the real signature algorithms with the phase-1 verifier
  world      the de-stubbed world: KMS-backed OpenPGP slot A, real-gpg slot B, OTS-on-regtest anchor

The flag: `tessera_proto.real.MODE` is read by `consumers.scenarios.build()`; default "stub". Set the
environment variable TESSERA_PROTO_MODE=real, or call `scenarios.build(mode="real")`. The phase-1 and
phase-2 tests always run the stub path.
"""
import os

MODE = os.environ.get("TESSERA_PROTO_MODE", "stub")
