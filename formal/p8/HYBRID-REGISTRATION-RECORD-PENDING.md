# Branch-registration record (A9.6): PENDING the author's A9 signing commit

**Status: prepared 2026-10-14 by the owner instance; not yet effective.** A9.6 authorizes this supplement only once
A9 is signed, and requires it to name the exact ENCODING-V1 and specification hashes. Fill the bracketed fields from
the signing commit, then commit this record in the same act as, or immediately after, A9.

- **Branch taken:** HYBRID. Pair id `KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256`; pure ML-DSA-65, empty context.
- **Supplement:** `formal/p8/HYBRID-SUPPLEMENT-DRAFT.md`, renamed `HYBRID-SUPPLEMENT.md` at registration, SHA-256
  [fill].
- **Baseline:** ENCODING-V1 at A9 signing commit [commit id], SHA-256 [fill]; the E§5.2 edit text as in supplement §7.
- **Specification:** the frozen V1 verification-spec object, hash entered at the 30 Oct freeze (the supplement's §9).
- **Pass-condition evidence (A9.6), all by 2026-10-14, ahead of 21 Oct:**
  1. Pair id with mode and context: supplement §1–2.
  2. Mixed pairing through R-3.12 and P3: supplement §5; `formal/suite/s-p3/proverif/hybrid/` (H1 holds; H2–H4
     red as predicted).
  3. Real KMS ML-DSA-65 over a genuine V1 frame, external μ above 4 KB, verifying offline in two implementations:
     `formal/p8/evidence/v1-hybrid-2026-10-14/` (A/B 27/27; cryptography plus dilithium-py).
  4. Real P-256 from the gpg slot as deployed: `prototype/policy-signer/EVIDENCE.md` (Cloud Run job through the
     queue; refusals for ε, tag and key_fp; access boundary).
  5. Full selected byte profile specified and tested: hybrid vectors 35 golden / 63 reject, codec agreement, fuzz
     90,400 cases with 0 disagreements; profile-conformance cases (a)–(e) plus hybrid positive and negative cases;
     independent verifier and conformance suite 342/342 (`prototype/differential/results-run5.json`).
- **Reviews:** `docs/reviews/hybrid-supplement/` (CODEX-REVIEW HS-01…06, applied; DECISIONS).
