# Ambiguities and missing normative inputs

These are instrument readings, not owner decisions or amendments. A9 governs.
No bundled object supplies policy. The numbered rows are §15.7 check ids;
`startup` identifies checks that refuse to emit a verdict.

| # | Check id | Question | Reading implemented (fail closed) | File:line |
|---|---|---|---|---|
| A01 | startup | §5/§14.2 supplies no authenticated release/config hash or release-signature format. What configuration is authorized? | The checked-in release is unprovisioned and refuses every config. An explicit local build pins a caller-selected, schema-checked config; this is instrument provisioning, never proof of release authenticity. There is no runtime auto-trust or bundle override. | `release_constants.py:2`; `build_release.py:9`; profile §5, §14.2 items 1–3 |
| A02 | 7.1, 8.3–8.4, 17.4 / startup | The catalog's values are listed, but neither its wire schema nor its actual frozen bytes/hashes exists. How is `--catalog` encoded/authenticated? | A closed canonical JSON `tessera-v1-independent-catalog/1` with exactly one entry and the fields in `policy.CAT_KEYS`; constants must match the profile. Its exact bytes are independently build-pinned and embedded. An external catalog must match that digest, never self-authorize. No catalog is silently fabricated from the bundle. | `policy.py:59`; `release_constants.py:3`; profile §1, §14.2 item 7 |
| A03 | 3.1, 5.1, 7.1, 9 | Originally no assigned pair id, mode/context or SPKI supplement was available. Which hybrid id is codec-known? | Superseded by the supplied supplement and the profile §8 registry owner decision: every installation knows the classical baseline; only an installed catalog selecting the exact hybrid pair registers its codec. Other well-formed ids, including the pair under fallback, remain opaque. The catalog selects semantic support independently of bundle spec lookup. No dated registration is asserted; see A14. | `codec.py:registered_codecs`, `signature_rule`; `verify.py:verify_bundle`; profile §8 Codec registry per installation; supplement §§1–3 |
| A04 | 14.4 | §15.4 requires a pinned SHA-1DC implementation/version/return behavior, but §14.2 item 15 explicitly says these are not supplied. Which detector is normative? | Do not replace SHA-1DC with ordinary SHA-1. Every obtainable git object contributes `UNVERIFIABLE / INDEPENDENT_SHA1DC_UNAVAILABLE`; other independent checks continue. This instrument-only reason is a visible extension because the table has no code for this missing build dependency. No complete in-profile bundle can return VALID_STRICT in this build. | `verify.py:251`; profile §15.4, §14.2 item 15 |
| A05 | startup, 2.1, 3.1, 4.1 | The Unicode 16.0.0 UCD digests and ECMA edition are not yet furnished (§9/§14.2 item 15). How can implementation tables be identified? | Require Python 3.14's Unicode version to be exactly 16.0.0 and explicitly build-pin the local unicodedata binary (the interpreter executable if built in); a different runtime refuses. Implement the profile's explicit ES recipe independently. This pins instrument behavior, not agreement with an absent official UCD digest or future frozen vectors. | `codec.py:60`; `verify.py:285`; `build_release.py:9` |
| A06 | 13.2, 13.5 | A supported malformed RRSIG with fewer than two bytes has no obtainable Type Covered for body grouping. Where does it belong? | Attach to the immediately preceding same-owner group when possible, or a root DNSKEY discriminator if no preceding group exists, then classify as DNSSEC_FORMAT. Impossible transitions remain SNAPSHOT_FORMAT. Only individually unobtainable sort fields fall back to zero/empty; readable tag, inception, expiration and signature are retained, with raw RDATA as serialization tie. Valid candidates dominate malformed extras except global wildcard and noncanonical-name restrictions. | `dnssec.py:78`; `dnssec.py:110`; profile §15.3, §6.1 |
| A07 | 13.3 | Does the global no-wildcard restriction apply when Labels is readable but the rest of the RRSIG is malformed? | Yes. Read Labels independently whenever four RDATA bytes exist; fewer Labels rejects even if the rest cannot parse or another witness validates. | `dnssec.py:93`; profile §15.3 point 4, §6.1 r2-F07 |
| A08 | 13.5, 14.7 | r2-F04 explicitly names *finalized* interval failures, leaving a verifying open entry evaluated before signing_start without a listed interval class. | An authenticated candidate before signing_start is INVALID / KSK_OUTSIDE_RELIANCE_PERIOD or GIT_SIGNER_OUTSIDE_INTERVAL, including open entries; only a time later than as_of and not before start is TRUST_HORIZON. | `dnssec.py:189`; profile §5, §6.3 |
| A09 | 14.1 | Commit author/committer fields are `<bytes>` without a minimum length. Are empty values admitted? | Require a nonempty value after each literal header prefix. Empty values reject as GIT_COMMIT_FORMAT. Names, addresses, clocks and other contents remain uninterpreted. | `git_channel.py:21`; profile §15.4 |
| A10 | 2.1, 2.4 | The container prohibits all JSON numbers, but §2.1 JCS precedes schema and dispatch explicitly inspects only JSON categories 1–5. How are otherwise syntactic numbers classified? | Dispatch admits syntactic number tokens; the container schema rejects every numeric value. JCS spelling is separately checked first. A non-finite numeric conversion makes the canonical check fail as JSON_NONCANONICAL, not OUT_OF_PROFILE. Signed payloads still use the full value-preserving number rule. | `codec.py:86`; `verify.py:144`; profile §3.1, §15.1 |
| A11 | 9.1, 9.4 | §8 places ECDSA r/s range under its rule-O policy list without separately mapping out-of-range codec-valid MPIs to a reason. | Treat r/s outside [1,n−1] as SIG_POLICY, before signature mathematics. Zero fails the codec's exact MPI bit-count rule as SIG_FORMAT. | `codec.py:227`; profile §8 |
| A12 | 13.2, 13.5 | §15.3 requires canonical embedded names but also routes malformed supported RRSIG RDATA to DNSSEC_FORMAT. Is an uppercase/compressed signer name a body or candidate defect? | Resolved by OWNER 2026-10-14, diff-1 F-1: uppercase ASCII or compression pointers inside the signer name are globally SNAPSHOT_FORMAT, even beside a valid witness. Other malformed supported RRSIG RDATA remains candidate-local DNSSEC_FORMAT. | `dnssec.py:canonical_signer`; profile §15.3 point 3, diff-1 F-1 |
| A13 | 13.5 | Does a supported RSA signature with a wrong octet width fail format or mathematics? | Enforce the modulus-sized PKCS#1 signature width, reporting DNSSEC_FORMAT before mathematics. RSA key encoding and 512–4096-bit size limits follow RFC 3110/5702; no leading-zero key octets are accepted. | `dnssec.py:172`; profile §6.1; RFC 5702 §3, RFC 3110 §2 |

Normative locators: A01—`docs/V1-PROFILE.md:340`; A02/A03—`docs/V1-PROFILE.md:98`; A04—`docs/V1-PROFILE.md:1271`; A05—`docs/V1-PROFILE.md:927`; A06/A07/A12—`docs/V1-PROFILE.md:1206`; A08—`docs/V1-PROFILE.md:432`; A09/A13—`docs/V1-PROFILE.md:1251`; A10—`docs/V1-PROFILE.md:1131`; A11—`docs/V1-PROFILE.md:824`.

## Follow-up 2026-10-14: diff-1

A12's earlier candidate-local reading is superseded by the explicit owner F-1
rule; the row above records the resolved reading. A06's all-zero fallback is
corrected to preserve each readable G35 field. F-3 under Coverage resolves
header participation: an entry failing row 2.4 contributes CONTAINER_SCHEMA
only and is absent from the shared pool used by rows 10.x, 11.x, 13.4 and 14.6.
The existing schema extraction already implements that rule. These corrections
add no new unresolved ambiguity.

## Follow-up 2026-10-14: requested hybrid support and EA-31

The exact id, 3309-byte length/cap and length error order, pure mode with empty
context, 1974-byte SPKI prefix and SHA-256 fingerprint, and K-R's status as an
assumption are explicit in supplement §§1–4. They required no guessed crypto
parameters or key encoding. FIPS 204 Algorithms 3, 8, 21 and 27 supply the
verification/strict-decoding rules; RFC 9881 §§2,4 supplies the SPKI conventions.

The following records every integration point requiring an instrument reading
of the draft/profile or reconciliation of overlapping text. These are visible
implementation choices, not new owner decisions. A03's former fallback-only
reading and unconditional key-format evaluation are superseded.

| # | Check id | Question / tension | Reading implemented | Location and source |
|---|---|---|---|---|
| A14 | 3.1, 7.1 / build | The prior candidate instrument compiled both codecs into a global registry despite the draft registration status. How is installation registration determined? | Resolved by OWNER 2026-10-14, differential run 4, profile §8 Codec registry per installation: derive supplements solely from the installed catalog alg. Classical or unknown alg adds no supplement; the exact hybrid alg adds its pair codec to the baseline. A fallback installation treats both hybrid slots as opaque with cap 65536 and semantics give ALG_UNKNOWN. A hybrid installation retains classical rule O. This supersedes the previous compile-both reading; no bundle or source-code availability registers a codec. | `codec.py:BASELINE_CODECS`, `registered_codecs`; `verify.py:verify_bundle`; profile §8, lines 900–905; supplement §§1–3 |
| A15 | 3.1, 9.3 versus 5.x, 9.1–9.2, 9.4–9.5 | EA-31 says unsupported signatures and possession are not evaluated, while r2-F01 requires their own codecs and row 9.3 lists only presence as its prerequisite. | Interpret non-evaluation as semantic non-evaluation. Receipt and possession codecs still run within the installation registry, including codec-known unselected ids. Hybrid ids are opaque under fallback, while classical ids retain rule O under hybrid. Unsupported key parsing, fingerprint binding and signature/possession policy/math do not run. Codec-invalid bytes still contribute INVALID and independent schema/hash checks still run. | `verify.py:verify_bundle`; `codec.py:parse_signature`, `read_anchor`; profile §1 r2-F01, §8 EA-31 and Codec registry per installation, §15.7 rows 3.1/9.3 |
| A16 | 5.1–5.2, 7.1 | Row 7.1 follows key rows in reporting order but is their new prerequisite. What if common algorithms differ or receipt decoding fails? | Determine support from each decoded slot's own `common.alg` and the installation catalog before key evaluation. Use the selected installation id for supported-slot keys. Skip the other slot's key semantics; common/manifest equality still rejects independently. If no receipt decodes, row 7.1 is unavailable and both key rows stay blocked; a manifest alone cannot authorize a key-format check. Reporting order remains unchanged. | `verify.py:verify_bundle`; profile §8 EA-31, §15.7 rows 5.1/5.2/6.2/6.3/7.1; supplement §5 |
| A17 | 9.1, 9.4 and 9.2, 9.5 | The profile has policy rows for both signatures, but the §8 policy is explicitly rule O and supplement §2 sends malformed ML-DSA internals to verification failure. | Raw rule R has no additional OpenPGP policy, so these policy rows pass vacuously for codec-valid rule R. Strict hint counts/order/duplicates/padding and z bound run at mathematical verification, before the backend, and map to SIG_INVALID / POSSESSION_INVALID. No internal FIPS decoding defect becomes SIG_POLICY or a codec failure. | `codec.py:sig_policy`, `mldsa65_encoding_valid`, `signature_verifies`; profile §8, §15.7; supplement §2 and decision 3 |
| A18 | 7.1, 8.3 / build | The draft/profile provides no actual frozen hybrid catalog bytes, hashes or new installation transport. Does support depend on bundled spec lookup or inferred registration? | Retain A02's one-entry authenticated/provisioned catalog interface. Its alg selects support and the installation's registered supplements independently of bundled spec hash lookup. A selected registered alg can still undergo semantics with SPEC_UNKNOWN. An unknown catalog alg registers no supplement and cannot manufacture support. The checked-in release remains unprovisioned; no real frozen catalog or dated registration is fabricated. | `policy.py:parse_catalog`; `build_release.py`; `codec.py:registered_codecs`; `verify.py:verify_bundle`; profile §8, §14.2; supplement §§1,9 |

K-R is recorded in REPORT.md, not implemented as a check: receipt bytes cannot
establish exclusive issuer/IAM key use, EXTERNAL_MU use at signing, or the
absence of signatures in other protocols. No assumption failure code is invented.

## Follow-up 2026-10-14: owner registry decision, differential run 4

A14's global compile-both reading is superseded by the explicit §8 owner
decision, not a new ambiguity or inferred registration date. A03, A15 and A18
above now reflect the installed registry. The catalog alg registers supplements
before receipt decoding, and the same immutable registry governs possession
codecs even when only the manifest alg is available. A16's support prerequisites
and A17's supported rule-R verification mapping remain in force.

The supplement's presence in source does not grant fallback installations
knowledge of its pair id. Both hybrid slots therefore use opaque framing and
its 65536-byte cap under fallback, while hybrid installations retain classical
rule O from ENCODING-V1. ALG_UNKNOWN remains a semantic result; SIG_EMPTY,
LENGTH_CAP, truncation and independent invalid findings still apply normally.
The catalog transport and authentication remain the existing A02 instrument
choice. This correction adds no unresolved ambiguity or release-authority claim.
