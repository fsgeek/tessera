# Real-world spike (THROWAWAY, not service code), started 2026-10-09 22:33Z

Status: COMPLETE 2026-10-10T00:03Z (see Latency section at the end; ignore "pending" wording above).
(submitted 22:33Z). A background poller (pid in `poller.pid`, `ots-upgrade.log`) runs `ots upgrade` every 30 min for up to
24 h; when both proofs hold a Bitcoin attestation and k=6 headers exist it runs `finalize.py`, which fetches the headers
once from two explorers (must agree), pins them by hash (`out/bitcoin-pins.json`), writes `out/latency.json`, and runs
`verify_offline.py` into `out/verify-final.txt`. `ots-upgrade.log` ends in COMPLETE when that passes.
The latency numbers and the final verdict are therefore NOT in this file yet; read `out/latency.json`, `out/verify-final.txt`.

## Files
`issue.py` (sign), `capture_dns.py`, `verify_offline.py` (+ `trust-config.json`), `selftest.py` (15 controls, all pass),
`poller.py`, `finalize.py`. Artifacts in `out/`: `receipt.json`, `receipt-preimage.bin(.ots)`, `dns-snapshot.json(.ots)`.
Run: `cd prototype && uv run python spike/verify_offline.py`.

## What worked (verified offline, socket creation blocked and asserted zero)
- Receipt: one OT_ATTEST bundle for wamason.com, two frames, slot A = KMS-style ECDSA P-256 OpenPGP (emulated KMS, DIGEST),
  slot B = real gpg 2.4.4 nistp256. Both signatures, both possession proofs, frame well-formedness, equal common bytes,
  tuple/fingerprint binding, manifest hash, owner name D == signed issuer_id, anchor preimage rebuilt: all PASS.
- Anchoring: `ots stamp` on the 1264-byte preimage (receipt digest cedc7e31...b9da) and on the DNS snapshot file; four
  public calendars accepted both (network works).
- DNSSEC: live chain captured root -> com -> wamason.com (Cloudflare-hosted, alg 13, DS tag 2371 at .com). Validated offline
  against a trust config with KSK-2017 (20326) and KSK-2024 (38696) by pinned IANA DS digests (the 38696 digest I wrote
  from memory matched the key in the live root DNSKEY set). At eval time 23:03Z the chain is SECURE; joint RRSIG window
  [2026-10-09 21:07:27Z, 2026-10-10 23:33:22Z] = 26.4 h over the 10 RRSIGs used.
- Controls (selftest.py): eval after expiry / before inception -> FAIL; KSK-2024-only trust before 10-11 -> UNPERFORMABLE; wrong
  pinned digest -> not PASS; flipped signature bit -> FAIL; the OTS+pin path on archived real mainnet proofs passes, and
  conflicting pin / absent pin / wrong file / each of the three conjuncts' failure give the expected typed result.

## What did not / mismatches with C1-C7
- **C4(i) cannot be completed: no key-publication TXT record exists.** `wamason.com TXT` holds only SPF and Google
  verification; `_tessera.` and `tessera.` return authenticated NODATA (NSEC, Cloudflare compact denial, validated). Also the
  spec names no record name or format for the fingerprints (R-4.26 says only "DNSSEC records publishing the fingerprints").
  Verdict row `DNSKEY_PUBLICATION: UNPERFORMABLE`. The authority tuple's K is therefore not authenticated by DNS, only the
  owner name check (D bound in signed bytes == trust config D) and the DNSSEC chain.
- C4(ii) git channel not exercised (out of scope; manifest `evidences` empty).
- KSK-2024 path is untested on real data: it signs the root from 2026-10-11, so the capture carries only a KSK-2017
  signature. Tested only with controls. Re-run the capture after 10-11 to see both/either.
- **Stale-by-design RRSIGs:** the resolver returned cached Cloudflare signatures (inception 10-08 21:33Z, expiry 10-10
  23:33Z): the usable window is ~26 h, shorter than delta = 72 h and about epsilon + 2 h. Cloudflare, not Route 53, hosts the zone
  (NS kanye/courtney.ns.cloudflare.com), so the "measure Route 53 windows" item measures Cloudflare: 2 d 2 h signatures,
  re-signed on a schedule, ZSK window ~50 h; DNSKEY RRSIG 2 months; com DS RRSIG 7 d; root DNSKEY 21 d; root DS-for-com 13 d.
  The binding window is the leaf (SOA/NS/TXT/NSEC). The snapshot fits only if its first Bitcoin attestation block time is
  <= 2026-10-10 23:33Z; otherwise the issuer must re-capture (the draft's rule). Result recorded in `out/verify-final.txt`.
- Verifier robustness: a trust config whose D is not in the snapshot raised KeyError instead of a typed verdict (the verifier
  assumes the snapshot's query set); a V1 verifier needs a typed `UNVERIFIABLE`.
- M9 (known): KMS ECDSA + gpg pairing only passes as P4' (both OpenPGP); used here.
- The KMS is emulated (local key), not AWS; AWS Lambda/KMS latency and OpenPGP packet construction there are not measured.
- Header rule used: every header must equal a pin; PoW and linkage also checked; no retarget logic (fine under full pins).

## Latency (final; replaces the pending notes above)
Anchoring is COMPLETE (log: COMPLETE 2026-10-10T00:03:54Z). Both proofs hold two mainnet attestations (heights 970687, 970690);
earliest used, headers h..h+5 pinned by hash and cross-checked between two explorers.
- Submission 22:33:09Z -> first Bitcoin attestation (block 970687, nTime 22:53:30Z): **1221 s (20.4 min)** for the receipt, 1208 s for the snapshot.
- Submission -> k=6 (block 970692, nTime 23:41:32Z): **4103 s (68 min)**.
- Poller observed the completed proof at 00:03Z (30-min poll granularity), so wall-clock "proof in hand" is <= 90 min; true availability is earlier. Block nTime values are chain-time proxies.
- A second attestation came 27 min later (970690); one calendar was quicker than the rest, as predicted (G-55/M3).
- Conjuncts: c1 T-declared = +1224 s, c2 pass (<< 72 h), c3 confirmed-declared = 4106 s. All pass.

## Snapshot vs RRSIG window
T_snap = 22:53:30Z on 9 Oct lies inside the joint window [21:07:27Z, 23:33:22Z next day] (26.4 h): it fits, with 24.7 h to spare and 1.8 h after
the latest inception. The leaf (Cloudflare) RRSIG is the binding expiry; the snapshot must be anchored within ~26 h of capture, and a
slow calendar (> ~24 h) would break it. Here the margin is ample; the 72 h delta is never the binding constraint.

## Final offline verdict (out/verify-final.txt)
SIG, BYTES, AUTH, DNSSEC, OTS.receipt, OTS.snapshot, TIME, NETWORK: PASS. DNSKEY_PUBLICATION: UNPERFORMABLE (no key TXT record).
Overall: the exit code is 0 for the required groups, but C4(i) is NOT established until a key record is published.

## KSK-2024 re-capture (2026-10-12, out-ksk2024/)
Re-captured root -> com -> wamason.com at 2026-10-12T00:06:44Z (`capture_dns_ksk2024.py`; `out/` untouched, no OTS stamp).
The root DNSKEY set holds 38696 (KSK-2024), 20326 (KSK-2017) and 8763 (ZSK), with ONE RRSIG, by 38696 (10-11 to 11-01).
KSK-2017 is still published but no longer signs. Joint window 10-11 16:00Z to 10-13 01:06Z.
- KSK-2024-only trust config: DNSSEC PASS. The KSK-2024 path is now exercised on real data.
- The shipped two-KSK trust config: DNSSEC **FAIL, a false reject.** `verify_offline.py:99` fails a trusted KSK that is
  in its configured period and present but did not sign, and the group inherits the FAIL even though KSK-2024 validated the set.
  Two defects: (1) the rule must be "some trusted KSK usable at the evaluation time validates the root DNSKEY set";
  a trusted KSK that did not sign is informational, not FAIL. (2) `trust-config.json` gives KSK-2017
  `signing_valid_until` = 2027-01-11, its revocation date, but it stopped signing at 2026-10-11. "Published" and
  "signing" are different periods, and the config conflates them.
- **V1 requirement:** the V1 verifier's root rule is existential over trusted KSKs. A control case is a snapshot taken during
  a rollover in which one trusted KSK is published but not signing. Without that control, every V1 receipt issued from
  2026-10-11 would be falsely rejected.
