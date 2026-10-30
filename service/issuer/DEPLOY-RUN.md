# Deployment run record (first V1 deployment)

Append-only. Each entry: date, step, what was run, the values it produced, and who ran it.

## 2026-10-30 — before the session (owner, no credentials)

Base: `8bcfcda` plus the issuer/signer interface fix (`docs/reviews/issuer-signer-interface/`).

1. **Verifier install.** Already installed; `sha1dcsum` SHA-256 `3fa8472a23ff8ecc6c91b5193bc6e6e7a7ef1a1bbfbbff769a89bda0634dd5fb`
   matches `service/verifier/install.json`.
2. **Suites.** The first run failed both signer suites (signer-kms 2, signer-gcp 7). One cause was a real defect:
   the issuer's attempt-prefixed frame names, which both production signers refuse, would have refused every
   request over 256 KiB. Fixed, confirmed by Codex, and covered by a retained pipeline test (disposition in
   `docs/reviews/issuer-signer-interface/DISPOSITION.md`). After the fix: issuer 235, signer-kms 48, signer-gcp 121,
   verifier 135 (77 subtests), all passing.
3. **Packages** (deterministic: a rebuild of the issuer bootstrap gave the same digest).
   - `service/issuer/dist/issuer-bootstrap.zip` SHA-256 `7789cfbb00e913cae222483ef4d894343bd52be49274be5cd13e2c984183748b`
     (BOOTSTRAP: no `install.json`, so pre-ship refuses until rebuilt in step 4)
   - `service/signer-kms/dist/signer-kms.zip` SHA-256 `3c5d812747f4efd84ca6339efa07d616e3bdff52d1a9330744ab9eea313f2923`

AWS session: `aws sts get-caller-identity --profile tessera` → account 477139661040,
`AccountFullAccessRole` (author login, 2026-10-30).

Next: step 1 (`terraform plan` for the issuer bootstrap), read together with the author.
