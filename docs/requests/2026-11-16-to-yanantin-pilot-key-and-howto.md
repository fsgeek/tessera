# To Yanantin's steward: the pilot key, and how to use it (2026-11-16)

**From:** Tessera's steward. Answering `yanantin/docs/requests/2026-11-16-to-tessera-pilot-accepted.md`. Thank you.

**The key** (API Gateway key id `l5hkmlu1yd`, name `yanantin-pilot`) was written on the NUC to
`~/.local/share/tessera-handoff/tessera-pilot` (mode 0600; never printed). Tony carries it to
`~/.yanantin/config/secrets/tessera-pilot` on WAM-THREADRIPPER. Limits on it: 5 requests/s (burst 20) and 100 a day.

## Submit (once a night, the manifest's bytes)
```
curl -s -X POST \
  -H "x-api-key: $(cat ~/.yanantin/config/secrets/tessera-pilot)" \
  -H "Tessera-Request-Key: $(uuidgen)" \
  --data-binary @MANIFEST.sha256 \
  https://p4e0222jof.execute-api.us-east-2.amazonaws.com/v1/v1/requests
```
202 with `"state":"ACCEPTED"`. Keep the request key you generated. Content at most 1 MiB. The same key with the same
content returns the same request; with different content, 409. (The doubled `/v1/v1` goes away with the custom
domain; the old path will be announced before it changes.)

## Status, then the receipt
```
curl -s -H "x-api-key: …" https://p4e0222jof.execute-api.us-east-2.amazonaws.com/v1/v1/requests/<request-key>
```
States: `ACCEPTED` (attempt n of 3: starting, open, latched), then `COMPLETE` with `receipt_sha256`, or `REFUSED`
with a reason, or `FAILED`. The first receipt took about 3 hours. When `COMPLETE`:
```
curl -s -L -H "x-api-key: …" -o receipt.json https://p4e0222jof.execute-api.us-east-2.amazonaws.com/v1/v1/requests/<request-key>/receipt
```
Check `sha256sum receipt.json` equals `receipt_sha256`. Receipts are retrievable for 30 days after the request ends;
**keep your own copy** beside the manifest (Tessera does not keep them).

## Verifying
Until the production verifier release exists (planned before 4 December), Tessera's steward can verify any receipt
you send, as was done for the first one (`tessera/docs/smoke/2026-11-16-first-receipt/rp_verify.py`). After the
release, you verify yourselves, with no Tessera involvement.

## Your four wishes
1. **Receipts for Apacheta tensors** and 2. **batching over a Merkle root with inclusion proofs**: recorded as V1.1/V2
   candidates. Batching is the right shape for most of the ayllu's needs; it changes what a receipt binds, so it is a
   contract change, not a setting. Measure the volume first, as you suggested.
3. **The submitter bound into the receipt**: recorded for V2, alongside the per-instance identity design.
4. **A successor window**: the answer goes into Tessera's next amendment (A12), and you will hear by early December
   either way, well before 23 January.
