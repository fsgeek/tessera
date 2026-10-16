# spike-pq REPORT (THROWAWAY INSTRUMENT SPIKE - never ships)

Run: `cd prototype/spike-pq && uv run python spike_pq.py` (output in run.log). No network at verification time.
Versions: Python 3.14.6; cryptography 50.0.2 (ML-DSA only, incl. sign_mu/verify_mu/MLDSAMuHasher; no SLH-DSA);
dilithium-py 1.4.0 (pure Python ML-DSA, sign_external_mu); slh-dsa 0.2.5 (module `slhdsa`, LGPL, mypyc-compiled).
pqcrypto 1.0.0 installs but `pqcrypto.sign` is empty (no signature schemes). liboqs-python skipped: no cmake.

Frames: ENCODING-V1 section 3 shape (u8 taglen, tag, u16 ver=1, u32 len, approximate-JCS payload). Toy: 2 KB content -> 2402-byte frame; 6000-byte content -> 6354-byte frame.

1. SLH-DSA (FIPS 205, pure, empty ctx): PASS for signing+verifying; NOT independent (single implementation, slh-dsa). sha2_128s sig 7856 B, sha2_128f sig 17088 B; tampered frame rejected.
2. ML-DSA-65 pure empty ctx: PASS, two independent implementations, both directions (cryptography <-> dilithium-py). pk 1952 B, sig 3309 B; tamper rejected.
3. External mu on 6354-byte frame: PASS. mu = SHAKE256(SHAKE256(pk,64) || 00 00 || M, 64) computed by hand equals dilithium-py's prehash_external_mu; cryptography sign_mu(mu) signature verifies as a normal ML-DSA signature over the full message in both cryptography and dilithium-py; dilithium-py sign_external_mu verifies in cryptography. (Not tested against real AWS KMS.)
4. Anchor preimage = header("tessera-v1/receipt-anchor") || 0x02 || for each slot: u32 len(F) || F || u32 len(sig) || sig (my extension of section 5, which as written holds only frames). 2 KB content, F_kms with ML-DSA-65 sig (3309), F_gpg slot with SLH-DSA sig:
   - ML-DSA-65 + SLH-DSA-SHA2-128s: 16011 bytes
   - ML-DSA-65 + SLH-DSA-SHA2-128f: 25243 bytes
   (frames 2402 + 2401, header 26, framing 17.) Anchor digest is still SHA-256, so OTS cost is unchanged.

Caveats: JCS approximated with json.dumps(sort_keys); the GPG slot is modelled as a bare SLH-DSA signature, not OpenPGP-wrapped. SLH-DSA timing here: 128s sign ~3 s, 128f ~0.14 s.
Housekeeping: `uv add` initially registered spike-pq as a workspace member of prototype/pyproject.toml and modified prototype/uv.lock; both were reverted to HEAD content, and spike-pq declares an empty workspace of its own.

## KMS half (2026-10-13, owner instance tessera-e4): PASS

Run: `uv run python spike_kms.py` (capture + offline verify; `spike_kms.py verify` re-verifies from `out-kms/capture.json`
alone). Log: `run-kms.log`. Account 477139661040, us-east-2, key `alias/tessera-pq-spike`
(e4a7deb4-f90a-4cac-85d3-6de71f2886bb, ML_DSA_65, origin AWS_KMS, tags project=tessera, purpose=pq-spike).
- RAW sign over a 2402-byte V1-shaped frame: verifies in cryptography 50.0.2 and dilithium-py 1.4.0 (independent).
- EXTERNAL_MU sign over a 6354-byte frame, mu computed locally from the KMS public key: the signature verifies as a
  normal ML-DSA-65 signature over the *full* frame in both implementations.
- Tamper of either frame rejected by both. pk 1952 B, sig 3309 B.
- KMS rejects RAW above 4096 bytes ("Member must have length less than or equal to 4096"), confirming the split.
Remaining for the 21 Oct pass condition: a real P-256 signature from the YubiKey via gpg, the pair algorithm id,
the mixed pairing through R-3.12 and P3, and rule R vectors. Delete the key (ScheduleKeyDeletion) when the spike closes.

## Slot-2 half on GCP Cloud KMS HSM (2026-10-14, owner instance tessera-e4): PASS

Run: `prototype/.venv/bin/python prototype/spike-pq/spike_gcp.py` (capture plus offline verify); `... spike_gcp.py verify`
re-verifies from `out-gcp/capture.json` alone. Project tessera-slot2, us-east1, key ring tessera-v1, key slot2-spike v1:
protection HSM, EC_SIGN_P256_SHA256, attestation format CAVIUM_V2_COMPRESSED (Marvell/Cavium LiquidSecurity: input to
the runbook's monoculture check).
- A real V1 attest frame (golden F-01's common block, `signer.key_fp` = `fp_gpg` of the HSM point and key creation
  time) signed through the HSM. gcloud hashes the OpenPGP v4 preimage (frame || v4 head || trailer) with SHA-256;
  the HSM signs that digest, which equals `gen.openpgp_v4_sig_digest`.
- Serialized as rule O with the P8 reference encoder (one v4 type-0x00 packet, 119 bytes, GnuPG 2.4.4 subpacket
  layout); accepted by the P8 rule-O codec.
- Verifies in two independent implementations: P8 gen.py's pure-Python ECDSA, and cryptography/OpenSSL. Tamper is
  rejected by both.
Pass-condition status (A9.6): the KMS ML-DSA-65 half and this slot-2 half are both real and verified. Still owed by
21 Oct: the pair algorithm identifier with mode and context; the mixed pairing through R-3.12 and P3; the ML-DSA-65
SPKI/fingerprint encoding; rule R golden and rejection vectors with an agreement run. Delete both spike keys when
the spike closes.

## Genuine V1 hybrid re-capture (2026-10-14, owner instance tessera-e4): PASS

`prototype/.venv/bin/python prototype/spike-pq/spike_v1_hybrid.py` signed genuine V1 hybrid frames (id
KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256, per formal/p8/HYBRID-SUPPLEMENT-DRAFT.md) with both real keys:
AWS KMS ML-DSA-65 (e4a7deb4-…, alias/tessera-pq-spike) and GCP HSM P-256 (tessera-slot2/slot2-spike v1).
- Small receipt (frame 758 B, kms RAW): the full receipt is accepted by codec A and codec B; the kms signature verifies in
  cryptography and dilithium-py. Anchor sha256 89dac77b…2e37.
- Big receipt (frame 6753 B, kms EXTERNAL_MU): the same; anchor sha256 a4c24658…013d.
- Manifest possession, kms and gpg: verifies in A and B; kms also in cryptography and dilithium-py.
This replaces the earlier KMS evidence over toy `tessera-v1/receipt` frames. The issuer uses EXTERNAL_MU always
(owner decision 6); the RAW capture shows the two paths are interchangeable for the verifier.
Spike keys are kept until the supplement's non-author review clears, then scheduled for deletion.
