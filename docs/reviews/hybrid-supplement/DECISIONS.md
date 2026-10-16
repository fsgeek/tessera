# Owner decisions on the hybrid supplement draft (2026-10-14)
1. Real-frame evidence: re-capture genuine V1 hybrid frames with both real keys (prototype/spike-pq/spike_v1_hybrid.py) before 21 Oct. Blocked only on the AWS session refresh.
2. The gpg-slot evidence is the GCP Cloud KMS HSM (slot-2 custody chosen 2026-10-13); no token capture.
3. Malformed ML-DSA internals = SIG_INVALID; the codec stays length-only (PROOF Lemma 7a unchanged).
4. Identifier: KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256, as proposed.
5. The key encoding and K-R stay in the supplement, which is bounded as A9.6 authorizes.
6. The issuer ALWAYS uses EXTERNAL_MU for the kms slot, one code path whatever the frame size (owner choice; the verifier is unaffected because the signature is standard). The non-author review is dispatched. vectors_sha256 covers the hybrid files at freeze. Delete both spike keys after the re-capture verifies.
