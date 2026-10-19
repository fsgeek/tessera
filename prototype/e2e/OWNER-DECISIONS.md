# Owner decisions for the first real TEST run (2026-10-19)

Owner: Claude Opus 5.5. Instrument run under A9.2; evidence for nothing.

1. **No service-key listing, no `utc_assessment`** in the first receipt. It is a pipeline proof. The listing is
   decided before the first production receipt, the last point at which it can still protect anything
   (`docs/decisions/2026-10-19-horizon-cost.md`).
2. **kms slot:** the existing spike key `alias/tessera-pq-spike` (AWS KMS ML-DSA-65, us-east-2). **gpg slot:** the
   deployed policy signer `slot2-signer` (GCP project tessera-slot2; job present, scheduler PAUSED, checked
   2026-10-19 read-only). The TXT fingerprints were computed offline from the spike captures; the `keys` stage
   checks them against KMS `GetPublicKey` and refuses on mismatch.
3. **Window:** 2026-10-19T00:00:00Z to 2026-10-26T23:59:59Z. Short on purpose: a published window cannot be
   shortened, and this TEST record occupies the production owner name `_tessera-v1.wamason.com` until it ends. A
   production verifier rejects these receipts anyway, because the TEST repository key is not in its trust
   configuration.
4. **Repository key:** the throwaway TEST P-256 key in `work/`, not YubiKey 2.

TXT value (255 bytes, one character-string): `work/runs/real-1/txt-record.txt`.
