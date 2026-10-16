# Differential run 1 (2026-10-14): independent verifier vs conformance suite

Saved by the owner from the run agent's final report; the harness blocked the agent from writing this file.

Totals: 283 cases. 280 AGREE, 2 AMBIG-ONLY, 1 DISAGREE. VALID_STRICT 52/52 agree; no negative case accepted. Release checker 8/8.
L-51, L-52a and L-52b are refused at the adapter (release authentication is external to the indep verifier, its A01), so they don't exercise the verifier.

- F-1, L-74, profile ambiguity, VALID_STRICT split by probe. An uppercase signer name in the RRSIG RDATA. Conformance expected SNAPSHOT_FORMAT (P:1210-1211); indep gave DNSSEC_FORMAT (P:1238-1240). PROBE-74e (bad RRSIG sorts first, honest witness present) gave VALID_STRICT on indep. OWNER: apply the proposed fix (non-canonical names in RDATA, signer name included, are SNAPSHOT_FORMAT whatever other witnesses are present). Fail-closed.
- F-2, indep bug: dnssec.py:109-110 sort-key fallback applied to readable fields, so the verdict depends on order. Instrument bug; fix in indep before run 2.
- F-3, L-13/L-14, AMBIG-ONLY (EA-06), T differs. OWNER: adopt the indep reading (a schema-failing headers entry is not a supplied header; it contributes CONTAINER_SCHEMA only, and rows 10.x/11.x/13.4/14.6 use the remaining entries); conformance updates the expected T.
- Not covered: L-94 (no git-framed SHA-1 collision exists), the hybrid path, L-111 codec vectors, real mainnet/KSK inputs.
- SHA-1DC pinned: cr-marcstevens/sha1collisiondetection a06f1adbe5522f3c939cd6a3f13d5ec7f4c1a988 (prototype/vendor/SHA1DC-PIN.md). It detects raw shattered-1.pdf; it does not detect the same collision git-framed (the header misaligns it), as expected.
