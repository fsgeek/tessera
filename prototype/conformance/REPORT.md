# V1 conformance universe and cases (instrument code)

> **STATUS: instrument, 2026-10-14.** TEST material only. Built from `docs/V1-PROFILE.md` (the 2026-10-14
> revision, cited as `P:line`), `docs/phase-0-prereg-amendment-9.md` (governs), `formal/p8/ENCODING-V1.md` (`ENC`)
> and RES §L (`docs/reviews/spec-sufficiency/RESOLUTIONS-DRAFT.md`). Every expectation was derived from the profile
> text, not from any verifier. `prototype/indep-verifier/` was not read.
> **Updated 2026-10-14 after differential run 1** (`prototype/differential/FINDINGS.md`): L-13 and L-14 take T
> from the remaining header entries [OWNER 2026-10-14, diff-1 F-3], and the three L-74 probes are suite cases
> L-74e, L-74l, L-74v [diff-1 F-1]. These five cases cite the profile as revised after diff-1 (lines shifted by
> the diff-1 insertions); every other case's `P:nnn` is a locator into the earlier 2026-10-14 revision.
> **Extended 2026-10-14 (hybrid routing and authority isolation):** 56 new cases in two families, `HY-*`
> (`formal/p8/HYBRID-CONFORMANCE-CASES.md` (a)–(e) under two installations, positive hybrid receipts, hybrid
> semantics negatives) and `AUTH-*` (`prototype/mutation/REPORT.md` observation 3, with an honest twin per attack).
> Their `P:nnn` cite the profile as it stands in the tree on 2026-10-14 (after diff-1). The 286 earlier cases
> regenerate byte-identically. See "Installations", "Hybrid routing family" and "Authority-isolation family" below.

## What is here

| File | Role |
|---|---|
| `tcrypto.py` | Deterministic TEST keys (P-256 via `formal/p8/vectors/gen.py` arithmetic and RFC 6979 nonces; seeded RSA-2048; Ed25519), OpenPGP rule-O packet builder, ASCII armor with CRC-24. |
| `universe.py` | The TEST universe: DNS hierarchy and RRSIG signer, snapshot-body serializer (P§15.3), synthetic Bitcoin chain and OTS proof builder (P§15.2), git objects (P§15.4), trust configuration (P§15.5), TEST release record and catalog stand-in. |
| `issue.py` | TEST issuer: complete V1 bundles in the P§15.1 container through the P§4 issue order, with named hooks so negative cases go through the same path. CLI: `issue.py --out DIR`. |
| `cases.py` | Generates every case into `cases/<ID>/` (bundle, trust config, release, `expected.json`). Deterministic: two runs give byte-identical output. |
| `run.py` | `run.py --verifier CMD` runs `CMD --trust T --bundle B` over every case and reports AGREE / DISAGREE / AMBIG-ONLY / ERROR per case. |
| `selfcheck.py` | Construction self-check of every `VALID_STRICT` case with independent libraries (dnspython DNSSEC, python-opentimestamps, `cryptography` ECDSA and ML-DSA-65, hashlib SHA-1), as named checks; `--isolation` checks that each authority attack fails exactly its named checks. Not a verifier. |
| `cases-index.json`, `universe-catalog.json`, `universe-release-key.json` | Index of cases; the catalog stand-in and the TEST release public key that the verifier under test must treat as compiled in. |
| `universe-catalog-hybrid.json` | The catalog of the hybrid-registered installation (alg = the pair id). Every `installation: hybrid` case also carries it as `cases/<ID>/catalog.json`, and its signed `release.json` compiles it in; `run.py` passes the case's `catalog.json` as `TESSERA_V1_TEST_CATALOG` when present. |

Run (from the repository root; the prototype venv has `cryptography`, `dnspython`, `opentimestamps`, `rfc8785`):

```
prototype/.venv/bin/python prototype/conformance/cases.py          # regenerate cases/ (about 30 s)
prototype/.venv/bin/python prototype/conformance/selfcheck.py --all # 65/65 positive controls pass
prototype/.venv/bin/python prototype/conformance/selfcheck.py --isolation # 11/11 authority attacks fail only where named
prototype/.venv/bin/python prototype/conformance/run.py --verifier "CMD" [--release-checker "CMD"] [--json out.json]
```

## The TEST universe

- **Profile constants.** D = `wamason.com` (the profile constant, P:647-650) with TEST keys only; catalog alg
  `OPENPGP4-ECDSA-P256-SHA256` (fallback branch), δ = 72 h, ε = 24 h, k = 6.
- **DNS.** TEST root with two root KSKs, alg 8 RSA-2048, flags 257: `TEST-KSK-A` mirrors KSK-2017 (policy signing
  start 2018-10-11T16:00:00Z, end 2026-10-11T00:00:00Z, L = 1814400 s, so reliance ends 2026-11-01) and
  `TEST-KSK-B` mirrors KSK-2024 (start 2026-10-11T00:00:00Z, open). Root ZSK alg 8; `com` KSK/ZSK alg 13;
  `wamason.com` KSK/ZSK alg 13; DS digest type 2 (4 and 1 in cases). The honest root DNSKEY RRset publishes both
  KSKs and is signed only by KSK-B (the A9.5 rollover control). TXT `_tessera-v1.wamason.com` carries the 255-byte
  ENC §7 value.
- **Chain.** Synthetic 80-byte headers from height 900000, prev-linked, merkle roots computed from real
  transaction lists, nTime set per height (no PoW: P:772-773 says a hash equal to a pin implies all of it). Honest
  timeline: git assertion anchored at h = 900002 (T_git 2026-11-02T00:20Z), snapshot at 900012 (T_snap
  2026-11-10T10:20Z), receipt at 900024 (T = 2026-11-10T12:20Z), declared 2026-11-10T12:00Z, window
  2026-11-01 .. 2026-12-01. Chain order 900002 + 5 < 900024.
- **OTS.** Proofs in the P§15.2 grammar: digest → append nonce → sha256 → (prepend tx prefix, append tx suffix,
  sha256, sha256) → conventional merkle suffix → Bitcoin attestation. The transaction is a 125-byte non-witness
  transaction whose output is `6a 20 ‖ m`; the receipt txid is the selected path's txid. Three proofs anchor in
  three different transactions.
- **Git.** Root tree {`README`, `tessera-v1`/}, subtree {`key-assertion` 100644}, blob = the DNS value byte for
  byte; commit with one parent and one `gpgsig` (rule O, type 0x00, GnuPG subpacket layout) by the TEST repository
  key; the git stamp's file digest is SHA256 of the 40-hex id plus LF. Container `git.commit`, `git.trees` and
  `git.blob` carry object bodies without the `<type> <len>\0` header (EA-15).
- **Signers.** Fallback: kms and gpg are TEST P-256 keys; `keys.kms` is DER SPKI, `keys.gpg` the bare v4 body.
  Hybrid (`HY-*` cases, 2026-10-14): kms is a TEST ML-DSA-65 key generated by `cryptography` 50.0.2 from a seeded
  32-byte ξ (`tcrypto.MLDSA65Key`); `keys.kms` is `cryptography`'s DER SPKI, asserted equal to the supplement's
  22-byte prefix plus the 1952-byte key (HS §3); gen.py's keygen from the same ξ is asserted to give the same key.
  Every kms signature (attestation and possession) is made by **external μ**, the supplement's only issuer path
  (HS §1, owner decision 6): μ from `cryptography`'s `MLDSAMuHasher` (pure, empty context), cross-checked against
  gen.py's formula, then FIPS 204 Algorithm 7 from μ with rnd = 0 (gen.py `mldsa65_sign_mu`; `cryptography` only
  signs hedged, which would break byte-identical regeneration), then verified over the frame itself by
  `cryptography` before the bytes are frozen. HY-V2's frames are 6753 / 6752 bytes, above KMS's 4096-byte RAW limit.
- **Trust configuration.** P§15.5 byte format, version "1", `as_of` 2026-12-31T00:00:00Z, header pins for every
  chain height of the case, root KSKs as above, one open repository entry from 2026-10-01. Each case carries its
  own configuration (pins differ per case chain).
- **Release.** Each case has `release.json`: a TEST release body (`format: tessera-v1-test-release/1`, the
  compiled `trust_config_sha256`, the catalog and its hash) with a raw ECDSA P-256 signature by the TEST release
  key (`universe-release-key.json`). The release-signature format is OPEN in the profile (P:1053-1057); this is a
  stand-in so the refusal cases can be expressed (EA-01).
- **Objects.** `spec`, `vectors`, `preamble` and `dependency_manifest` are TEST stand-ins (part format of
  P§15.8; dependency manifest in the P§15.6 shape with TEST field values), not the frozen objects (EA-10).

## Installations

A case runs under one of two compiled-in installations (P:114-119, P:134-136; A9.6 "Branch registration"):

| Installation | Catalog `alg` | Codec registry | Spec object | kms key format (P:884-888) |
|---|---|---|---|---|
| classical (every pre-existing case; `-C` suffix) | `OPENPGP4-ECDSA-P256-SHA256` | baseline: classical id (rule O both slots); the pair id is absent (opaque, P:127-130) | `TEST-SPEC.txt` part | P-256 DER SPKI |
| hybrid (`-H` suffix, `HY-V*`, `HY-N*`) | `KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256` | baseline + supplement: classical id (rule O, codec-known, policy-unsupported) and the pair id (rule R kms, rule O gpg) | plus `TEST-HYBRID-SUPPLEMENT.txt` part (P:1550) | ML-DSA-65 DER SPKI (HS §3) |

The hybrid catalog has exactly the classical catalog's fields (only `alg`, `spec_sha256` and the `TEST` label
differ), so a catalog reader needs nothing new. Registration state is read from the catalog (EA-32). Cases built
for the hybrid installation sign the hybrid spec hash, so only the property under test differs from a classical
case. `expected.json` `_meta.installation` names the installation of every new case.

## Issue path

`issue.issue()` follows P§4 in order: fix manifest and common (declared time) → both frames → sign → verify both
signatures over the exact bytes (refuses otherwise) → freeze → `A_sig` and its stamp; possession proofs over
`F_manifest`; the key-publication value; the git key-assertion commit, signed and stamped **first**; the DNSSEC
snapshot converted to the P§15.3 body, enveloped (ENC §6) and stamped with its own proof; then the receipt stamp at
a height that leaves h_git + 5 < h_receipt. Before shipping it checks (P:321-331): all three proofs anchored, chain
order, c1–c3 on the receipt and on the snapshot's own proof, and the issuance window; an honest issue that fails
any of these raises `IssueRefused`. Negative cases set `adversarial=True`, which records the pre-ship results in
`expected.json` (`_meta.issuer_preship`) instead of refusing. The container is emitted as canonical JCS.

## Case format

`cases/<ID>/expected.json` holds the six stable fields at top level (`verdict`, `reason`, `T`, `revocation`,
`historical_security`, `standing`; P:281-294) and `_meta` with the title, the profile lines cited, the derivation,
the ambiguity ids it rests on, and `ambiguous_fields` (fields whose value depends on a reading the profile does not
force; run.py reports a difference only in those as AMBIG-ONLY, not DISAGREE). Refusal cases hold
`{"refusal": "TRUST_CONFIG_UNAUTHENTICATED"}` instead. Release-checker cases hold `previous.json`, `next.json` and
`{"release_check": "ACCEPT"|"REJECT"}`.

## Counts

342 cases: 334 bundle cases (65 `VALID_STRICT`, 203 `INVALID`, 59 `UNVERIFIABLE`, 7 startup refusals) and 8
release-checker cases. The 2026-10-14 extension adds 56 (34 hybrid: 26 routing, 2 positive, 6 semantics; 22
authority isolation: 11 attacks, 11 twins); the other 286 are unchanged. They cover RES §L L-01 to L-111 (L-27/L-28
as the r2-F16 replacements; L-94 not built, below; the hybrid half of L-105 is HY-V1 with HY-N1), the r2 distinguishing cases F01–F15 (ids `ALG-*`, `RC-*`, `F03-*`, `F05-*`,
`F06-*`, `F07-*`, `F08-*`, `F09-*`, `F10-*`, `F12-*`, `F15-*`, `AGG-*`), the A9.1 scenario rows (`A-*`; d1 is
L-06/L-06s, d2 is L-09, c is L-04, h is L-05), and the review controls named in the brief:

| Control | Cases |
|---|---|
| Bad-first / good-second KSK, both orders | L-61a, L-61b |
| Honest old root after retirement within reliance; same evidence after reliance | L-62a (pass), L-62b (fail); L-63 (reliance reason) |
| Nonmonotone nTime pairs | L-32/L-32r, L-33/L-33r, L-34/L-34r, L-38 |
| Chain-order boundary r = g+5 fail / r = g+6 pass | L-30 / L-29 (and L-31) |
| Wildcard RRSIG | L-75, F07-a |
| Non-canonical RRSIG beside a valid witness, each sort position (diff-1 F-1) | L-74e, L-74l, L-74v |
| Unknown-alg canary | ALG-01 (plus L-21, ALG-02..05, L-107) |
| Captured repository signer config attempt | L-51 (and L-52a DNS credential, L-52b AWS account) |
| Rollover control | L-60 (and every honest case) |
| KSK-2017 policy-start boundary | F15-a / F15-b |
| Hybrid routing (a)–(e), both installations | `HY-a*-C`, `HY-b*-H`, `HY-c*-{C,H}`, `HY-d*-{C,H}`, `HY-e*-{C,H}` |
| Full hybrid receipt, external μ above 4 KB | HY-V1, HY-V2 (plus HY-N1..N6) |
| Re-stamped attacker receipt failing only at authority, with honest twins | `AUTH-*`, `AUTH-*-T` |

## Verification of the construction

- `selfcheck.py --all`: **65/65** `VALID_STRICT` cases pass with independent libraries (52 earlier, HY-V1, HY-V2
  and the 11 `AUTH-*-T` twins). Since 2026-10-14 the self-check is a list of named checks and also verifies the
  authority conditions: TXT owner = `_tessera-v1.<issuer>`, TXT kms/gpg = manifest fingerprints, a configured
  repository entry for D verifies `gpgsig` and its interval (open end = `as_of`) contains T_git, issuer = pinned D =
  `issuer_domain`, and the issuance window; for the pair id it verifies the kms receipt and possession signatures
  with `cryptography`'s ML-DSA-65 over the exact SPKI. The 52 earlier positive controls still pass with these
  added checks. Also: dnspython validates every
  RRset of the snapshot at T_snap (with RFC 1982 serial arithmetic applied by the self-check, since dnspython
  compares raw 32-bit times and fails across the 2106 wrap, L-82); python-opentimestamps 0.4.5 parses the three
  proofs and every Bitcoin attestation's message equals its header's merkle root; `cryptography` verifies the
  receipt, possession and `gpgsig` signatures; SHA-1 ids and the commit → tree → blob path check out; headers equal
  their pins and are prev-linked; h_git + 5 < h_receipt; blob = TXT value.
- `selfcheck.py --isolation`: **11/11** authority-isolation attacks fail exactly the construction checks named in
  `_meta.isolation.selfcheck_fails` and pass every other (signatures, possession, fingerprints, pins, the three
  OTS proofs, chain order, DNSSEC, owner, keys, git path, repository signer and interval, pinned D, window).
- Negative cases were audited by running the same self-check and confirming that each fails, if at all, at the
  intended defect (or passes where the defect is outside the self-check's scope, e.g. reliance periods, horizons,
  format restrictions). Expectations are **not** cross-validated by a verifier: that is the job of `run.py` against
  the independent verifier.
- `run.py` was exercised with a stub that echoes `expected.json` (all 275 bundle cases of the pre-diff-1 set AGREE; release-checker cases
  SKIP without `--release-checker`), including the materialization of the 2^27 + 1 byte bundle. Re-run 2026-10-14
  over all 334 bundle cases (334 AGREE, 8 SKIP), with the stub also asserting that `TESSERA_V1_TEST_CATALOG` equals
  the catalog inside the case's signed release and that its `alg` is the case's installation's.
- Determinism: regenerating all cases gives byte-identical files; after the 2026-10-14 extension the 286 earlier case
  directories, `cases-index.json`'s first 286 entries, `universe-catalog.json` and `universe-release-key.json` are
  byte-identical to the pre-extension output, and two full regenerations are identical.
- Row-3.1 fixture probe (not a verifier, not shipped): gen.py's `decode_anchor` with the pair id removed from its
  registry for classical-installation cases reproduces each `HY-*` case's intended a_sig codec outcome (opaque
  accepts, rule R / rule O codes), and every `HY-*` possession proof decodes under its manifest alg's rule.

## Not built

1. **L-94 (SHA-1DC collision-pattern object).** Needs a git object (`commit|tree|blob <len>\0…`) that triggers
   SHA-1DC's disturbance-vector detection. The published SHAttered/Shambles blocks only trigger detection after
   their own fixed prefixes, so a git-framed instance needs a fresh chosen-prefix SHA-1 collision computation.
   Not feasible here.
2. ~~**The hybrid half of L-105 and the hybrid signer path.**~~ Built 2026-10-14 against the supplement draft
   (`formal/p8/HYBRID-SUPPLEMENT-DRAFT.md`, OWNER-PROPOSED, not registered): HY-V1/HY-V2 (the ML-DSA-65 SPKI passes
   the key-format check under the hybrid installation) and HY-N1. If the registered supplement differs (pair id,
   SPKI, rule-R codes), the `HY-*` cases are regenerated from `universe.py`/`tcrypto.py`.
3. **L-111's N-01…N-22 and C-N01…C-N22 as bundle cases.** They are P8 codec vectors and live in
   `formal/p8/vectors/golden.json`; L-111a/b/c exercise the number rule inside a receipt payload (accepted
   boundary values, −0, non-canonical spelling). No separate tie case is built at bundle level.
4. **L-53 to L-56 as verifier cases.** They concern the release checker; they are data-only checker cases (run
   with `--release-checker`). L-56's verdict-change half is built as bundle cases L-56a/L-56b.
5. **Real inputs.** No mainnet headers, real root KSK RDATA, real repository or AWS/KMS key: everything is TEST.
6. **F04 repository "mixed" (open-horizon and finalized entries both verifying).** Not constructible: entries
   require unique `key` (P:1308) and a commit carries one `gpgsig`, so two entries cannot both verify one commit.
   The root mixed case is built (L-57c).

## EXPECTATION-AMBIGUITIES

Ids are stable labels, not contiguous. Each is a point where deriving an expectation needed a reading the profile does not force. The case's
`_meta.ambiguities` names the ids; `ambiguous_fields` marks the field that depends on the reading.

- **EA-01 Compiled-in inputs and the CLI.** The trust-config hash and the catalog are compiled into a release
  (P:357-371, P:111-116), and the release-signature format is OPEN (P:1053-1057). The fixed CLI `--trust --bundle`
  has no channel for them. Reading: the verifier under test takes the TEST release from `TESSERA_V1_TEST_RELEASE`
  (signed by the key in `TESSERA_V1_TEST_RELEASE_KEY`) and the catalog from `TESSERA_V1_TEST_CATALOG`; a config
  whose hash is not the one compiled by an authentically signed release is refused (L-50, L-51, L-52a/b).
- **EA-02 Request input.** D4 makes the request a verifier input (P:213-215); the CLI has no request flag.
  Reading: `--request degraded` is appended for L-06 only.
- **EA-03 Output and refusal encoding.** P:289-294 fixes the stable-six JCS object but not where the CLI prints it
  or how a startup refusal (P:365-366, "no verdict") is signalled. Reading: one JSON object on stdout (top level or
  under `stable`/`result`/`report`); refusal = nonzero exit, the code on stdout or stderr, no six-field object.
- **EA-04 Where `REQUEST_UNSUPPORTED` goes.** P:214 calls it a "detail"; it is not a stable field. Reading: reason
  `OUT_OF_PROFILE`; `detail` compared only if the verifier emits one.
- **EA-05 T for dispatch-terminal outcomes.** P:291-293 says T is reported whatever the verdict; P:205 and
  P:1345 say nothing else is evaluated after D1–D4. Reading: T = null for L-01..L-06 (including L-06, whose bytes
  would otherwise give T = 12:20). Marked ambiguous field T.
- **EA-06 T when `headers` fails its schema** (L-13, L-14). **Resolved 2026-10-14 by the owner [diff-1 F-3]:**
  the other reading below is adopted, so L-13/L-14 now expect T = 2026-11-10T12:20:00Z and are no longer
  ambiguous. Original text: The table makes rows 3.1/4.1 available only when "2.4
  passes" for their member but says nothing similar for `headers` in rows 10.x/11.4 (P:1369-1375). Reading: a
  schema-failed `headers` member is not an obtainable input, so T = null; the other reading (ignore only the bad
  entry) gives T = 2026-11-10T12:20:00Z. Marked ambiguous field T.
- **EA-07 Renewal wrapper encoding (case h).** The profile lands h at D3 (P:206-207) but defines no wrapper.
  Reading: a second layer around the original (`layers` of length 2).
- **EA-08 "Both trust-list orders"** (P:394-395) versus the mandatory sort of `root_ksks` (P:1290-1291): a
  conforming config has one order. Reading: the failing candidate sorts first (L-61a) or second (L-61b); this also
  gives both snapshot-body RRSIG orders (sorted by key tag).
- **EA-09 Branch-not-taken alg id.** The hybrid pair id is unregistered (P:139-141). Reading: placeholder
  `TEST-HYBRID-MLDSA65-OPENPGP4-P256`, codec-unknown (opaque codec). Verdict `ALG_UNKNOWN` holds either way
  (P:113-115, P:117-123), but the codec route would differ once a supplement registers the id.
- **EA-10 Stand-in objects.** The spec, vectors, preamble and dependency-manifest objects and the catalog are TEST
  stand-ins; the real vectors object (P:1440-1441) cannot contain these cases, which embed its hash.
- **EA-11 Unsupported RRSIG with an unmatched selector as the only witness** (L-70b). Row 3 needs a matching
  selector (P:540-544), row 5's `DNSSEC_KEY_MISMATCH` speaks of a *supported* witness (P:551-553), and "an
  unrelated unsupported RR does not qualify". No row applies directly. Reading: no usable witness, so
  `UNVERIFIABLE / DNS_EVIDENCE_MISSING`. Alternative: `INVALID / DNSSEC_KEY_MISMATCH` by the fail-closed owner
  choice for unmatched selectors (P:559-560). Marked ambiguous fields verdict and reason. This one changes the
  verdict class.
- **EA-12 Release checker interface.** L-53..L-56 test the release checker (P:479-486), whose interface is not
  specified. Reading: `CMD --previous P --next N` printing ACCEPT or REJECT.
- **EA-13 RRSIG sort key across the 2^32 wrap.** P:1215-1216 sorts RRSIGs by inception and expiration without
  saying raw 32-bit field or resolved time. The issuer sorts by raw field bytes; no case has two RRSIGs whose order
  differs under the two readings (L-82 has one per group).
- **EA-14 "Same evidence after reliance must not pass"** (P:395-397). With L = 21 days, pre-retirement evidence
  anchored after reliance always has an expired RRSIG, so the forced reason is the time class
  (`RRSIG_NOT_VALID_AT_EVAL_TIME`, L-62b), not `KSK_OUTSIDE_RELIANCE_PERIOD`; the latter needs a window longer
  than L (L-63). Not a free choice, but the control's reason is easy to mis-expect.
- **EA-15 Git object encoding in the container.** P:158 says "raw signed commit object"; P:1254 describes the
  commit body "without `commit <len>\0`". Reading: `git.commit`, `git.trees`, `git.blob` carry bodies; the
  verifier adds the header to compute ids.
- **EA-20 Empty snapshot body.** The profile says `LENGTH_CAP` (P:254, P:1245); ENC §6 says 1 ≤ len, and
  `formal/p8/vectors/gen.py` (`decode_snapshot`) reports `SCHEMA`. Reading: the profile governs (L-77).
- **EA-21 Blob with a trailing LF** (CH-02). P:637-639 says the trailing LF "is rejected" without naming a code.
  Reading: row 15.2 `CHANNEL_VALUE_MISMATCH` (the blob is not byte-equal to the DNS value); `GIT_PATH` is a
  conceivable alternative. Marked ambiguous field reason.
- **EA-22 Commit tree id not equal to SHA-1 of `trees[0]`** (GIT-path-c). No dedicated code; reading: P:1272-1273's
  "otherwise `GIT_PATH`". Marked ambiguous field reason.
- **EA-23 ECDSA r or s outside [1, n−1]** (F10-g, r = n). The range is listed among the rule-O policy bullets
  whose failure is `SIG_POLICY` (P:839-840), but it is equally a verification failure (`SIG_INVALID`). Reading:
  `SIG_POLICY`. Marked ambiguous field reason.
- **EA-24 Hybrid key encoding** (L-105). The fallback half uses an ML-DSA-65-shaped SPKI (OID
  2.16.840.1.101.3.4.3.18, 1952-byte key); the exact SPKI awaits the branch supplement.
- **EA-26 Reference reader divergence (finding).** python-opentimestamps 0.4.5 rejects a timestamp at depth 256
  (its limit is 255) while the profile allows depth ≤ 256 counting the root as 0 (P:1170-1171, P:1175). L-87e
  (depth 256) is `VALID_STRICT` by the profile; a verifier built on python-opentimestamps will reject it. The same
  library also accepts redundant LEB128 (L-86, already noted at P:1173-1174) and SHA-1/RIPEMD-160 ops (L-87a/b).
- **EA-27 A9.1 fixtures b and d3.** A9.1 names the outcome but not the fixture. Reading for b: the attacker
  re-signs under its own keys and presents the honest DNS and git evidence (→ `DNS_KEY_MISMATCH`); presenting its
  own DNS chain instead would be `UNVERIFIABLE / NO_TRUSTED_KSK_USABLE`, contradicting A9's `INVALID`. Reading for
  d3 ("one key, one channel"): one attacker key in both slots, honest DNS, git absent → `INVALID /
  DNS_KEY_MISMATCH` dominating `MEMBER_MISSING:git`.

- **EA-31 Key-format rule for a frame alg that is not the catalog id** (HY-ak-C, HY-b1-H). P:886-888 selects the
  kms key rule "by the installed governing spec and slot, never by key bytes alone", P:889-891 says that under the
  fallback *any* `keys.kms` that is not a P-256 DER SPKI, an ML-DSA-65 SPKI included, is `KEY_FORMAT`, and row 5.1's
  inputs are "`keys.<slot>`, installed spec, slot", available whenever the key is present (P:1464), unlike rows
  9.x, which depend on 7.1. Reading (adopted, the profile's text): the installation fixes the kms key format, so a
  genuine hybrid receipt under the classical installation, and a classical receipt with a P-256 kms key under the
  hybrid installation, are `INVALID / KEY_FORMAT`. Other reading: `formal/p8/HYBRID-CONFORMANCE-CASES.md` (a) and
  (b) and Codex HS-04 say key semantics are skipped for a non-catalog id ("no `KEY_FORMAT`"), and the supplement
  §3 phrases the ML-DSA rule as "under the pair id": then both cases are `UNVERIFIABLE / ALG_UNKNOWN`
  (`_meta.alternative`). Marked ambiguous fields verdict and reason; **this changes the verdict class**. Every other
  `HY-*` case puts the installation's own kms key format in `keys.kms`, which passes row 5.1 under both readings,
  so (a)–(e) are tested without depending on EA-31; HY-b2-H is the (b) routing claim with the key dimension
  neutralized.
- **EA-32 Registration state of the installation.** The profile says the catalog holds "the registered pair id
  under the hybrid" (P:114-116) and that the supplement governs only if the branch is taken (P:134-136), but the
  TEST catalog has no registry field, and the differential adapter rejects unknown catalog fields. Reading: the pair
  id is in the codec registry exactly when the compiled catalog's `alg` is the pair id; a registered-but-unselected
  pair id does not exist in V1 (A9.6). No case's verdict depends on a third state.

Observations that are forced by the text but worth stating: a wrong git hash prefix or a non-verifying `gpgsig`
gives `UNVERIFIABLE / GIT_SIGNER_NOT_CONFIGURED` (P:626-627), so a corrupted repository signature never yields
INVALID by itself (GIT-prefix, L-96); and the selected attestation is the lowest qualifying height, so an
unqualified lower attestation is skipped (L-40) while a contradicted one nulls T (L-42, L-109).

## Hybrid routing family (`HY-*`)

Source: `formal/p8/HYBRID-CONFORMANCE-CASES.md` (HC), cases (a)–(e), with the pair id
`KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256` and the codecs and ML-DSA-65 arithmetic of
`formal/p8/vectors/gen.py`. Frames, manifests and `A_sig` are gen.py's encoders; slot rules follow gen.py's
`SIG_RULES` for the hybrid installation, and the opaque codec for an id absent from the installation's registry.

- **(a) before registration** (classical installation): a1 a genuine 3309-byte ML-DSA-65 kms signature, a2 rule-O
  packets (the 119-byte kms packet rule R would reject), a3 1-byte / 65536-byte strings in both slots and both
  possession proofs → `UNVERIFIABLE / ALG_UNKNOWN` with signature and possession rows blocked by 7.1; a4 empty →
  `SIG_EMPTY`, a5 65537 bytes → `LENGTH_CAP` (row 3.1 INVALID outranks 7.1). HY-ak-C is HY-V1's own bundle under the
  classical release: `INVALID / KEY_FORMAT` by P:889-891 (EA-31).
- **(b) after registration** (hybrid installation): HY-b2-H, classical-id frames decoded by rule O, signatures and
  possession that would not verify, kms key in the installation's format → `UNVERIFIABLE / ALG_UNKNOWN` (no
  `SIG_INVALID`, no `POSSESSION_INVALID`, no `SCHEMA`). HY-b1-H is a fallback issuer's receipt as is (P-256 kms key)
  → `INVALID / KEY_FORMAT` (EA-31; HC expects `ALG_UNKNOWN`).
- **(c)** classical-id kms signature failing rule O, each under both installations: 0xC2 header (XA-19 shape)
  `SIG_PACKET`, type 0x01 (XA-22) `SIG_FORMAT`, 1025 bytes (XA-14) `LENGTH_CAP`, empty (XA-11) `SIG_EMPTY`.
- **(d)** `KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA384` (XHR-09) and `X-UNKNOWN-ALG-1` (A-02) consistently in
  frames and manifest, both installations → `UNVERIFIABLE / ALG_UNKNOWN`.
- **(e)** both installations: e1 the M9 shape (kms frame pair id, gpg frame classical, manifest pair id) →
  `RECEIPT_COMMON_MISMATCH`; e2 frames pair id, manifest classical, and e3 two unknown ids →
  `RECEIPT_MANIFEST_MISMATCH`.
- **Positive** (hybrid installation): HY-V1 (779 / 778-byte frames) and HY-V2 (6753 / 6752 bytes) are complete
  receipts through the issuer, honest pre-ship checks on, kms signed by external μ; both pass `selfcheck.py`.
- **Semantics are live** (hybrid installation): HY-N1 P-256 SPKI with the pair id `KEY_FORMAT`; HY-N2 kms
  signature over other bytes `SIG_INVALID`; HY-N3 kms possession over other bytes `POSSESSION_INVALID`; HY-N4 3308
  bytes `SIG_FORMAT`; HY-N5 3310 bytes `LENGTH_CAP`; HY-N6 a valid signature under context `tessera-v1` (XHR-13)
  `SIG_INVALID`.

What HC's "all five cases pass in the profile verifier under both installation states" needs from a verifier:
(c), (d), (e) run under both; (a) is classical-only and (b) hybrid-only by definition. Not built: (a)/(b) under
the *other* installation (they would be ordinary (b)/(a) or (d)-type cases).

## Authority-isolation family (`AUTH-*`)

Source: `prototype/mutation/REPORT.md` observation 3 (a fully re-keyed receipt stopped at
`RECEIPT_ANCHOR_MISMATCH`, so the campaign never showed the authority rows rejecting on their own). In every
attack the attacker issues through `issue.issue()` with its own two P-256 keys: manifest and frames for those keys,
signatures verified, possession proofs, `A_sig`, and a receipt OTS proof in its own transaction, committed into the
case's synthetic chain at h = 900024 under the pinned headers (the TEST universe controls chain generation; on
mainnet anyone can get a transaction mined, and pins cover the real chain). The receipt rows (2–12, except row 8.1 in AUTH-vi,
which is the element under test) and the bundled-object rows (17) therefore pass. Exactly one authority element is wrong, and the reported reason is that
row's under the P§15.7 order. `_meta.isolation` records what the attacker holds, the only failing rows and the
self-check names that must fail.

| Attack | Attacker holds | Wrong element | Expected (row) | Twin (`-T`, VALID_STRICT) |
|---|---|---|---|---|
| AUTH-i | nothing | DNS and git (legitimate, consistent) publish the legitimate keys | `INVALID / DNS_KEY_MISMATCH` (15.1) | records publish the keys that signed |
| AUTH-ii-root | repository key | own root, com and wamason.com zones; no configured KSK | `UNVERIFIABLE / NO_TRUSTED_KSK_USABLE` (13.5) | TXT signed under the trusted path |
| AUTH-ii-ds | repository key | own wamason.com DNSKEY set under the honest DS | `INVALID / DNSKEY_DS_MISMATCH` (13.5) | same |
| AUTH-ii-zsk | repository key | TXT signed by an attacker key outside the validated set | `INVALID / DNSSEC_KEY_MISMATCH` (13.5) | same |
| AUTH-ii-tag | repository key | as ii-zsk, RRSIG carrying the honest ZSK's tag | `INVALID / DNSSEC_SIGNATURE_INVALID` (13.5) | same |
| AUTH-iii | DNS credential | commit signed by its own repository key | `UNVERIFIABLE / GIT_SIGNER_NOT_CONFIGURED` (14.7) | commit signed by the configured key |
| AUTH-iv-end | DNS credential, retired repository key | finalized entry ends 2026-11-01, T_git 2026-11-02T00:20Z | `INVALID / GIT_SIGNER_OUTSIDE_INTERVAL` (14.7) | entry ends 2026-11-03 |
| AUTH-iv-start | DNS credential, repository key | open entry starts 2026-11-03, after T_git | `INVALID / GIT_SIGNER_OUTSIDE_INTERVAL` (14.7) | entry starts 2026-11-01 |
| AUTH-v-eq | both credentials | git anchored at h_receipt − 5 | `INVALID / GIT_NOT_PRECOMMITTED` (14.8) | h_receipt − 6 |
| AUTH-v-after | both credentials | git anchored at h_receipt + 3 | `INVALID / GIT_NOT_PRECOMMITTED` (14.8) | h_receipt − 6 |
| AUTH-vi | its own domain's DNS, repository key | `common.issuer` = `wamason-attacker.com`, trusted DNSSEC path via com | `INVALID / ISSUER_NOT_PINNED` (8.1) | issuer = wamason.com |

Each twin is built by the same call with the one element made right, through the honest issuer's pre-ship refusals
(chain order, anchoring, c1–c3, window), and passes `selfcheck.py`. Attack (i) is the A-b fixture re-done with its
own twin. Twins of different attacks differ in key seeds, so no two case directories are byte-identical. Not built:
(ii)/(iii) under the hybrid installation; the authority rows do not depend on the signer branch.

## Every case

**A9.1 mapping**

| Case | Fixture | Expected | T | Profile citation | EA |
|---|---|---|---|---|---|
| A-a | Honest receipt as shipped (cases a, g) | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:951, P:281-294 |  |
| A-e | Case e: a's bytes; slot-B key revoked out of band inside (declared, anchor] | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:957, P:284 |  |
| A-e2 | Case e': slot-B key revoked before declared (out of band) | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:957, P:284 |  |
| A-f | Case f: impostor's content through the honest service | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:958 |  |
| A-i | Case i: content = a contract plus two valid party signatures | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:960 |  |
| A-i2 | Case i': as i, one party signature does not verify | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:961 |  |
| A-b | Case b: reattribution under attacker keys, honest DNS and git evidence | `INVALID / DNS_KEY_MISMATCH` | 2026-11-10T12:20:00Z | P:952, P:1393, P:684-691 | EA-27 |
| A-d3 | Case d3 / L-17: clone with one key (both slots) and one channel (git absent) | `INVALID / DNS_KEY_MISMATCH` | 2026-11-10T12:20:00Z | P:956, P:263, RES L-17 | EA-27 |

**dispatch**

| Case | Fixture | Expected | T | Profile citation | EA |
|---|---|---|---|---|---|
| L-01 | Non-JSON bytes | `UNVERIFIABLE / OUT_OF_PROFILE` | null | P:209-210, P:1345, RES L-01 | EA-05 (field: T) |
| L-01b | Duplicate top-level member names (ENC 1.4 check 4) | `UNVERIFIABLE / OUT_OF_PROFILE` | null | P:209-210, ENC 1.4 check 4 | EA-05 (field: T) |
| L-01c | UTF-8 BOM before the container | `UNVERIFIABLE / OUT_OF_PROFILE` | null | P:209-210, ENC 1.4 check 2 | EA-05 (field: T) |
| L-01d | Invalid UTF-8 inside a string | `UNVERIFIABLE / OUT_OF_PROFILE` | null | P:209-210, ENC 1.4 check 1 | EA-05 (field: T) |
| L-02 | Container over 2^27 bytes (valid JSON, padded) | `UNVERIFIABLE / OUT_OF_PROFILE` | null | P:209-210, P:255-256, RES L-02 | EA-05 (field: T) |
| L-02b | Container of exactly 2^27 bytes (control: passes D1, then unknown member) | `INVALID / CONTAINER_SCHEMA` | 2026-11-10T12:20:00Z | P:209-210, P:1135-1140, P:186 |  |
| L-03 | Top-level `profile` absent | `UNVERIFIABLE / OUT_OF_PROFILE` | null | P:211, RES L-03 | EA-05 (field: T) |
| L-03b | Top-level `profile` = other label | `UNVERIFIABLE / OUT_OF_PROFILE` | null | P:204-205, P:211 | EA-05 (field: T) |
| L-04 | Two layers (case c, two-layer transplant) | `UNVERIFIABLE / OUT_OF_PROFILE` | null | P:212, P:953, RES L-04 | EA-05 (field: T) |
| L-04b | Zero layers | `UNVERIFIABLE / OUT_OF_PROFILE` | null | P:212 | EA-05 (field: T) |
| L-05 | Renewal wrapper (case h) | `UNVERIFIABLE / OUT_OF_PROFILE` | null | P:206-207, P:212, P:959, RES L-05 | EA-05, EA-07 (field: T) |
| L-06 | Case d1: a's bundle under a degraded request | `UNVERIFIABLE / OUT_OF_PROFILE` | null | P:213-215, P:954, P:967-968, RES L-06 | EA-02, EA-04, EA-05 (field: T) |
| L-06s | Case d1: the same bytes, strict request | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:954, RES L-06 |  |

**container**

| Case | Fixture | Expected | T | Profile citation | EA |
|---|---|---|---|---|---|
| L-07 | Re-indented container | `INVALID / JSON_NONCANONICAL` | 2026-11-10T12:20:00Z | P:187-188, P:1136-1137, P:1346, RES L-07 |  |
| L-08 | Unknown member in the layer | `INVALID / CONTAINER_SCHEMA` | 2026-11-10T12:20:00Z | P:186, P:1349, RES L-08 |  |
| L-09 | Case d2: `git` absent | `UNVERIFIABLE / MEMBER_MISSING:git` | 2026-11-10T12:20:00Z | P:175-181, P:955, P:1347, RES L-09 |  |
| L-10 | Nested `git.ots` absent | `UNVERIFIABLE / MEMBER_MISSING:git.ots` | 2026-11-10T12:20:00Z | P:175-182, RES L-10 |  |
| L-11 | `git.object_format` absent | `UNVERIFIABLE / GIT_OBJECT_FORMAT_MISSING` | 2026-11-10T12:20:00Z | P:176-177, P:628-629, RES L-11 |  |
| L-12 | `git.object_format` = "sha256" | `UNVERIFIABLE / GIT_OBJECT_FORMAT` | 2026-11-10T12:20:00Z | P:182-184, P:1348, RES L-12 |  |
| L-13 | Header height key "01" | `INVALID / CONTAINER_SCHEMA` | 2026-11-10T12:20:00Z | P:1213-1214, P:1235, P:1455, P:828-829 (diff-1 F-3), RES L-13 |  |
| L-14 | Header height 4294967296 | `INVALID / CONTAINER_SCHEMA` | 2026-11-10T12:20:00Z | P:1213-1214, P:1455, P:828-829 (diff-1 F-3), RES L-14 |  |
| L-15 | `issuer_record` absent | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:178-179, P:190-194, RES L-15 |  |
| L-16 | `issuer_record.policy_version` malformed | `INVALID / CONTAINER_SCHEMA` | 2026-11-10T12:20:00Z | P:179-180, P:1155, RES L-16 |  |
| F03-a | `issuer_record: {}` | `INVALID / CONTAINER_SCHEMA` | 2026-11-10T12:20:00Z | P:179-180, P:1139-1140 |  |
| F03-b | `keys: null` | `INVALID / CONTAINER_SCHEMA` | 2026-11-10T12:20:00Z | P:177-178, P:1138-1139 |  |
| F03-c | `vectors` absent and `preamble` non-string | `INVALID / CONTAINER_SCHEMA` | 2026-11-10T12:20:00Z | P:179-181, P:263 |  |
| F03-d | `git.object_format: null` | `INVALID / CONTAINER_SCHEMA` | 2026-11-10T12:20:00Z | P:184-185, P:1139 |  |
| F03-e | `dns.ots` and `git.ots` both absent | `UNVERIFIABLE / MEMBER_MISSING:dns.ots` | 2026-11-10T12:20:00Z | P:181-182, P:1347 |  |
| F03-f | Base64 member with nonzero pad bits | `INVALID / CONTAINER_SCHEMA` | 2026-11-10T12:20:00Z | P:1134-1135 |  |
| F03-g | A JSON number inside the container | `INVALID / CONTAINER_SCHEMA` | 2026-11-10T12:20:00Z | P:171, P:1133-1134 |  |
| F03-h | `receipt_anchor.txid` in uppercase hex | `INVALID / CONTAINER_SCHEMA` | 2026-11-10T12:20:00Z | P:1150 |  |
| F03-i | `git.trees` with three elements | `INVALID / CONTAINER_SCHEMA` | 2026-11-10T12:20:00Z | P:1153 |  |
| F03-j | `possession.kms` absent | `UNVERIFIABLE / MEMBER_MISSING:possession.kms` | 2026-11-10T12:20:00Z | P:175-182, P:1148 |  |

**binding forms**

| Case | Fixture | Expected | T | Profile citation | EA |
|---|---|---|---|---|---|
| L-18 | binding_forms ["STMT_DIGEST"] | `UNVERIFIABLE / BINDING_FORM_UNSUPPORTED` | 2026-11-10T12:20:00Z | P:678-681, P:1363, RES L-18 |  |
| L-19 | binding_forms ["STMT_OTHER"] | `UNVERIFIABLE / BINDING_FORM_UNKNOWN` | 2026-11-10T12:20:00Z | P:678-681, RES L-19 |  |
| L-20 | binding_forms ["STMT_DIGEST","STMT_DIRECT"] | `UNVERIFIABLE / BINDING_FORM_UNSUPPORTED` | 2026-11-10T12:20:00Z | P:678-681, RES L-20 |  |

**algorithm**

| Case | Fixture | Expected | T | Profile citation | EA |
|---|---|---|---|---|---|
| L-21 | Branch-not-taken alg (hybrid pair id placeholder), rule-O signature bytes | `UNVERIFIABLE / ALG_UNKNOWN` | 2026-11-10T12:20:00Z | P:113-115, P:117-123, P:1358, RES L-21 | EA-09 |
| ALG-01 | Unknown-alg canary with opaque 300-byte signatures | `UNVERIFIABLE / ALG_UNKNOWN` | 2026-11-10T12:20:00Z | P:113-115, P:220-222, ENC 5.2:442 |  |
| ALG-02 | Unknown alg with an empty kms signature (codec-invalid) | `INVALID / SIG_EMPTY` | 2026-11-10T12:20:00Z | P:1350, ENC 5:388-389 |  |
| ALG-03 | Unknown alg with a 65537-byte gpg signature (codec-invalid) | `INVALID / LENGTH_CAP` | 2026-11-10T12:20:00Z | P:1350, ENC 5.2:442 |  |
| ALG-04 | Frames carry an unknown alg; manifest carries the catalog alg | `INVALID / RECEIPT_MANIFEST_MISMATCH` | 2026-11-10T12:20:00Z | P:694-699, P:1357, P:121 |  |
| ALG-05 | Frames carry the catalog alg; manifest carries an unknown alg | `INVALID / RECEIPT_MANIFEST_MISMATCH` | 2026-11-10T12:20:00Z | P:694-699, P:1357 |  |

**spec binding**

| Case | Fixture | Expected | T | Profile citation | EA |
|---|---|---|---|---|---|
| L-22 | Wrong common.spec.id | `INVALID / SPEC_ID` | 2026-11-10T12:20:00Z | P:97, P:1360, RES L-22 |  |
| L-23 | Unknown spec hash (self-consistent bundled spec) | `UNVERIFIABLE / SPEC_UNKNOWN` | 2026-11-10T12:20:00Z | P:97-98, P:103-108, P:1361, RES L-23 |  |
| F12-a | Unknown spec plus altered bundled preamble | `INVALID / BUNDLE_OBJECT_HASH` | 2026-11-10T12:20:00Z | P:103-108, P:1396 |  |
| F12-b | Unknown spec plus unmatched dependency-manifest bytes | `UNVERIFIABLE / SPEC_UNKNOWN` | 2026-11-10T12:20:00Z | P:106-107, P:906-907, P:1397 |  |
| L-24 | Signed vectors_sha256 != catalog (bundled vectors self-consistent) | `INVALID / SPEC_OBJECT_MISMATCH` | 2026-11-10T12:20:00Z | P:98-99, P:1362, RES L-24 |  |
| L-24b | Signed preamble_sha256 != catalog | `INVALID / SPEC_OBJECT_MISMATCH` | 2026-11-10T12:20:00Z | P:98-99, P:1362 |  |
| L-25 | Bundled preamble bytes altered | `INVALID / BUNDLE_OBJECT_HASH` | 2026-11-10T12:20:00Z | P:100-101, P:1396, RES L-25 |  |
| L-25b | Bundled spec bytes altered | `INVALID / BUNDLE_OBJECT_HASH` | 2026-11-10T12:20:00Z | P:103-104, P:1396 |  |
| L-25c | Bundled dependency manifest altered | `INVALID / BUNDLE_OBJECT_HASH` | 2026-11-10T12:20:00Z | P:905-906, P:1397 |  |

**pinned D**

| Case | Fixture | Expected | T | Profile citation | EA |
|---|---|---|---|---|---|
| L-26 | issuer = other domain, git absent | `INVALID / ISSUER_NOT_PINNED` | 2026-11-10T12:20:00Z | P:647-650, P:1359, RES L-26 |  |
| L-26b | issuer = other domain, all evidence present | `INVALID / ISSUER_NOT_PINNED` | 2026-11-10T12:20:00Z | P:647-650, P:1359 |  |

**chain order**

| Case | Fixture | Expected | T | Profile citation | EA |
|---|---|---|---|---|---|
| L-27 | T_git = declared + 1 s (> declared), h_git + 5 < h_receipt | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:652-660, RES L-27 (replacement) |  |
| L-28 | T_git > receipt T, h_git + 5 < h_receipt | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:652-660, RES L-28 (replacement) |  |
| L-29 | h_git + 5 = h_receipt - 1 (r = g + 6) | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:655-656, P:1392, RES L-29 |  |
| L-30 | h_git + 5 = h_receipt (r = g + 5) | `INVALID / GIT_NOT_PRECOMMITTED` | 2026-11-10T12:20:00Z | P:655-656, P:1392, RES L-30 |  |
| L-31 | Codex F01 schedule: receipt h nTime 11:55, declared 12:00, git at j > h nTime 11:59 | `INVALID / GIT_NOT_PRECOMMITTED` | 2026-11-10T11:55:00Z | P:655-656, RES L-31 |  |

**time**

| Case | Fixture | Expected | T | Profile citation | EA |
|---|---|---|---|---|---|
| L-32 | Nonmonotone pair at c1: h1 < h2, nTime(h1) = declared - eps - 1, nTime(h2) = declared - eps | `INVALID / TIME_BEFORE_DECLARED_EPSILON` | 2026-11-09T11:59:59Z | P:713-718, P:724-727, RES L-32 |  |
| L-32r | Reverse pair: nTime(h1) = declared - eps, nTime(h2) = declared - eps - 1 | `VALID_STRICT / OK` | 2026-11-09T12:00:00Z | P:713-718 |  |
| L-33 | Nonmonotone pair at c2: nTime(h1) = declared + delta + 1, nTime(h2) = declared + delta | `INVALID / TIME_AFTER_DECLARED_DELTA` | 2026-11-13T12:00:01Z | P:713-718, P:720-722, RES L-33 |  |
| L-33r | Reverse pair at c2 boundary | `VALID_STRICT / OK` | 2026-11-13T12:00:00Z | P:720-722 |  |
| L-34 | Nonmonotone pair at not-after: nTime(h1) = not-after + 1, nTime(h2) = not-after | `INVALID / ISSUANCE_WINDOW` | 2026-11-10T13:00:01Z | P:585-587, P:713-718, RES L-34 |  |
| L-34r | Reverse pair at not-after | `VALID_STRICT / OK` | 2026-11-10T13:00:00Z | P:585-587 |  |
| W-01 | declared = issuance-not-before (inclusive) | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:585-587 |  |
| W-02 | declared = issuance-not-before - 1 s | `INVALID / ISSUANCE_WINDOW` | 2026-11-10T12:20:00Z | P:585-587 |  |
| L-35 | Two qualifying attestations at the same height | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:724-727, RES L-35 |  |
| L-36 | confirmed_at = declared + delta | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:728-731, RES L-36 |  |
| L-36b | confirmed_at = declared + delta + 1 | `INVALID / CONFIRMATION_LATE` | 2026-11-10T12:20:00Z | P:728-731, RES L-36 |  |
| L-37 | Fifth successor inside delta, sixth outside (h+6 header supplied) | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:728-729, RES L-37 |  |
| L-38 | confirmed_at < T (nonmonotone) | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:730-731, RES L-38 |  |
| L-39 | Qualifying branch plus an attestation at q > h with no headers | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:737-741, RES L-39 |  |
| L-40 | Plus an attestation at q < h with partial pinned headers (q, q+1) | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:737-741, P:774-775, RES L-40 |  |
| L-41 | Plus an attestation at q whose supplied header is unpinned | `UNVERIFIABLE / HEADERS_NOT_COVERED` | 2026-11-10T12:20:00Z | P:487-489, P:763-764, P:1370, RES L-41 |  |
| L-42 | Plus a contradicted branch at q (pinned header, merkle != message) | `INVALID / OTS_MERKLE_MISMATCH` | null | P:742-743, P:291-293, P:1374, RES L-42 |  |
| L-43 | Pending-only receipt proof | `UNVERIFIABLE / ANCHOR_PENDING_ONLY` | null | P:743-745, P:1375, RES L-43 |  |
| L-43b | Bitcoin attestation without its headers | `UNVERIFIABLE / HEADERS_MISSING` | null | P:743-745, P:1375 |  |
| L-44 | Holder-upgraded proof: original witness plus new branches without headers | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:737-741, RES L-44 |  |
| L-45 | Missing intermediate height between supplied headers | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:771-772, RES L-45 |  |
| L-46 | Adjacent supplied pair with wrong prev (pinned) | `INVALID / HEADER_CHAIN_BROKEN` | 2026-11-10T12:20:00Z | P:771-772, P:1371, RES L-46 |  |
| L-47 | Supplied header at a pinned height with another hash | `INVALID / HEADER_CONFLICTS_PIN` | 2026-11-10T12:20:00Z | P:765-767, P:1369, RES L-47 |  |
| L-48 | h..h+5 segment crosses a 2016-block boundary (901152) | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:773-775, RES L-48 |  |
| L-49 | Receipt passes c3, snapshot fails c3 | `INVALID / SNAPSHOT_TIME` | 2026-11-10T12:20:00Z | P:795-796, P:1384, RES L-49 |  |
| SNAP-c1 | Snapshot T_snap = declared - eps - 1 | `INVALID / SNAPSHOT_TIME` | 2026-11-10T12:20:00Z | P:781-783, P:795-796 |  |
| SNAP-c1b | Snapshot T_snap = declared - eps (boundary) | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:781-783 |  |
| SNAP-c2 | Snapshot T_snap = declared + delta + 1 | `INVALID / SNAPSHOT_TIME` | 2026-11-10T12:20:00Z | P:781-783, P:795-796 |  |

**trust config**

| Case | Fixture | Expected | T | Profile citation | EA |
|---|---|---|---|---|---|
| L-50 | Config hash not compiled into the release | refusal `TRUST_CONFIG_UNAUTHENTICATED` | — | P:365-366, RES L-50 |  |
| L-50b | Compiled config that fails the 15.5 schema (root_ksks unsorted) | refusal `TRUST_CONFIG_UNAUTHENTICATED` | — | P:365-366, P:1291-1295 |  |
| L-50c | Compiled config whose repository key is not a valid P-256 point | refusal `TRUST_CONFIG_UNAUTHENTICATED` | — | P:858-861 |  |
| L-50d | Compiled config containing a JSON number | refusal `TRUST_CONFIG_UNAUTHENTICATED` | — | P:1283, P:1287-1288 |  |
| L-51 | Captured repository signer signs a config (own KSK, repository key, pins) | refusal `TRUST_CONFIG_UNAUTHENTICATED` | — | P:372-373, P:357-364, RES L-51 |  |
| L-52a | Captured DNS credential (wamason.com ZSK) signs a config | refusal `TRUST_CONFIG_UNAUTHENTICATED` | — | P:372-373, RES L-52 |  |
| L-52b | Issuing AWS account (kms signer) signs a config | refusal `TRUST_CONFIG_UNAUTHENTICATED` | — | P:372-373, RES L-52 |  |
| L-56a | Pin append, before: h* segment supplied but unpinned | `UNVERIFIABLE / HEADERS_NOT_COVERED` | 2026-11-10T13:20:00Z | P:484-486, P:487-489, RES L-56 |  |
| L-56b | Pin append, after: the same bundle under the appended config | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:484-486, RES L-56 |  |
| L-57 | Snapshot after as_of under the open KSK-B | `UNVERIFIABLE / TRUST_HORIZON` | 2026-11-10T12:20:00Z | P:474-478, P:434-437, RES L-57 |  |
| L-57b | Git T_git after as_of under the open repository key | `UNVERIFIABLE / TRUST_HORIZON` | 2026-11-10T12:20:00Z | P:474-478, P:618-621, P:1391 |  |
| L-57c | Mixed root: finalized KSK-A outside reliance + open KSK-B after as_of | `UNVERIFIABLE / TRUST_HORIZON` | 2026-11-10T12:20:00Z | P:429-438 |  |
| L-58 | Presented root KSK-B with REVOKE set (signing with it) | `UNVERIFIABLE / NO_TRUSTED_KSK_USABLE` | 2026-11-10T12:20:00Z | P:455-457, P:427-428, RES L-58 |  |
| L-59 | Presented root KSK-B RDATA differs from config (flags 256) | `UNVERIFIABLE / NO_TRUSTED_KSK_USABLE` | 2026-11-10T12:20:00Z | P:455-456, RES L-59 |  |
| L-60 | Rollover control: KSK-A published but not signing | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:393-394, RES L-60 |  |
| L-61a | Failing trusted candidate (KSK-A, corrupt) sorted first, KSK-B validates | `VALID_STRICT / OK` | 2026-10-20T12:20:00Z | P:390-391, P:394-395, RES L-61 | EA-08 |
| L-61b | Failing trusted candidate (KSK-B, corrupt) sorted second, KSK-A validates | `VALID_STRICT / OK` | 2026-10-20T12:20:00Z | P:390-391, P:394-395, RES L-61 | EA-08 |
| L-62a | Honest old root: KSK-A signed before retirement, anchored after, within reliance | `VALID_STRICT / OK` | 2026-10-15T12:20:00Z | P:383-391, P:395-397, RES L-62 |  |
| L-62b | Same old-root evidence (window Oct 1-22) anchored after reliance | `INVALID / RRSIG_NOT_VALID_AT_EVAL_TIME` | 2026-11-10T12:20:00Z | P:395-397, P:429-440, RES L-62 | EA-14 |
| L-63 | Retired KSK-A, RRSIG window valid, T_snap outside reliance | `INVALID / KSK_OUTSIDE_RELIANCE_PERIOD` | 2026-11-10T12:20:00Z | P:420-421, P:432-438, RES L-63 |  |
| F15-a | KSK-A policy signing_start boundary: T_snap = 2018-10-11T16:00:00Z | `VALID_STRICT / OK` | 2018-10-11T20:20:00Z | P:467-469 |  |
| F15-b | KSK-A policy signing_start boundary: T_snap = 2018-10-11T15:59:59Z | `INVALID / KSK_OUTSIDE_RELIANCE_PERIOD` | 2018-10-11T20:20:00Z | P:467-469, P:432-438 |  |

**release checker**

| Case | Fixture | Expected | T | Profile citation | EA |
|---|---|---|---|---|---|
| L-53 | Changing L of a closed KSK | checker `REJECT` | — | P:479-486, RES L-53 |  |
| L-54 | Closing KSK-B so that its reliance end (end + L) < previous as_of | checker `REJECT` | — | P:481-483, RES L-54 |  |
| L-54b | Closing the repository key below previous as_of | checker `REJECT` | — | P:481-483 |  |
| L-54c | Closing KSK-B with end + L >= previous as_of (control) | checker `ACCEPT` | — | P:481-483 |  |
| L-55a | as_of decreasing | checker `REJECT` | — | P:480, RES L-55 |  |
| L-55b | Existing pin hash changed | checker `REJECT` | — | P:484, RES L-55 |  |
| L-55c | Entry removed (KSK-A) | checker `REJECT` | — | P:484, RES L-55 |  |
| L-56c | Pin append (new heights) | checker `ACCEPT` | — | P:484-486, RES L-56 |  |

**DNSSEC**

| Case | Fixture | Expected | T | Profile citation | EA |
|---|---|---|---|---|---|
| L-64 | Mixed DS types 2 and 4, only type 4 matching | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:517-519, RES L-64 |  |
| L-65 | DS type 4 only, matching | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:517-519, RES L-65 |  |
| L-66 | DS type 1 only (matching selectors) | `UNVERIFIABLE / DNSSEC_ALGORITHM_UNSUPPORTED` | 2026-11-10T12:20:00Z | P:540-544, RES L-66 |  |
| L-67 | Supported nonmatching DS plus unsupported DS | `UNVERIFIABLE / DNSSEC_ALGORITHM_UNSUPPORTED` | 2026-11-10T12:20:00Z | P:540-544, RES L-67 |  |
| L-68 | All DS supported (type 2), none matching | `INVALID / DNSKEY_DS_MISMATCH` | 2026-11-10T12:20:00Z | P:553, RES L-68 |  |
| L-68b | All DS supported (types 2 and 4), none matching | `INVALID / DNSKEY_DS_MISMATCH` | 2026-11-10T12:20:00Z | P:553 |  |
| L-69 | TXT: valid alg-13 RRSIG plus an alg-15 RRSIG | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:525, RES L-69 |  |
| L-70 | TXT signed only by an alg-15 key present in the zone's DNSKEY set | `UNVERIFIABLE / DNSSEC_ALGORITHM_UNSUPPORTED` | 2026-11-10T12:20:00Z | P:540-544, P:564-566, RES L-70 |  |
| L-70b | TXT signed only by an alg-15 key absent from the zone (unrelated unsupported RRSIG) | `UNVERIFIABLE / DNS_EVIDENCE_MISSING` | 2026-11-10T12:20:00Z | P:538-544, P:551-553 | EA-11 (field: verdict, reason) |
| L-71a | TXT RRset without its witness RRSIG | `UNVERIFIABLE / DNS_EVIDENCE_MISSING` | 2026-11-10T12:20:00Z | P:526, P:800-802, RES L-71 |  |
| L-71b | Root DNSKEY without RRSIG | `UNVERIFIABLE / NO_TRUSTED_KSK_USABLE` | 2026-11-10T12:20:00Z | P:427-428, P:800-802, RES L-71 |  |
| L-72 | Sequence ending before the TXT group | `UNVERIFIABLE / DNS_EVIDENCE_MISSING` | 2026-11-10T12:20:00Z | P:1225-1226, P:1383, RES L-72 |  |
| L-73a | Truncated RR (last RDATA one byte short) | `INVALID / SNAPSHOT_FORMAT` | 2026-11-10T12:20:00Z | P:1237-1239, RES L-73 |  |
| L-73b | Forbidden RR type (A at wamason.com) | `INVALID / SNAPSHOT_FORMAT` | 2026-11-10T12:20:00Z | P:1243-1244, RES L-73 |  |
| L-73c | Duplicate RR in the wamason.com DNSKEY group | `INVALID / SNAPSHOT_FORMAT` | 2026-11-10T12:20:00Z | P:1219-1221, P:1237-1238, RES L-73 |  |
| L-73d | Misordered groups (com DNSKEY before com DS) | `INVALID / SNAPSHOT_FORMAT` | 2026-11-10T12:20:00Z | P:1212-1213, P:1237-1238, RES L-73 |  |
| L-74 | Uppercase signer name inside TXT RRSIG RDATA | `INVALID / SNAPSHOT_FORMAT` | 2026-11-10T12:20:00Z | P:1210-1211, RES L-74 |  |
| L-74e | Valid TXT witness plus uppercase-signer TXT RRSIG (inception one day earlier: sorts first) | `INVALID / SNAPSHOT_FORMAT` | 2026-11-10T12:20:00Z | P:1294-1295, P:1330-1336 (diff-1 F-1), P:1485, RES L-74 |  |
| L-74l | Valid TXT witness plus uppercase-signer TXT RRSIG (inception one second later: sorts last) | `INVALID / SNAPSHOT_FORMAT` | 2026-11-10T12:20:00Z | P:1294-1295, P:1330-1336 (diff-1 F-1), P:1485, RES L-74 |  |
| L-74v | Valid TXT witness plus uppercase-signer TXT RRSIG (same inception: issuer sort order) | `INVALID / SNAPSHOT_FORMAT` | 2026-11-10T12:20:00Z | P:1294-1295, P:1330-1336 (diff-1 F-1), P:1485, RES L-74 |  |
| L-75 | Wildcard TXT RRSIG (Labels 2 < 3) as the only witness | `INVALID / DNS_WILDCARD` | 2026-11-10T12:20:00Z | P:567-568, P:1246-1248, RES L-75 |  |
| F07-a | Valid explicit TXT witness plus a wildcard RRSIG | `INVALID / DNS_WILDCARD` | 2026-11-10T12:20:00Z | P:569-577 |  |
| L-76 | Malformed TXT value (v=tessera2) with DNSSEC unperformable (root unsigned) | `INVALID / DNS_VERSION` | 2026-11-10T12:20:00Z | P:250-252, P:1383, RES L-76 |  |
| L-77 | Empty snapshot body | `INVALID / LENGTH_CAP` | 2026-11-10T12:20:00Z | P:254, P:1245, RES L-77 | EA-20 |
| L-78 | Extra expired TXT RRSIG beside a valid one | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:786-789, RES L-78 |  |
| L-79 | TXT RRSIG inception exactly 2^31 from T_snap | `INVALID / RRSIG_TIME_AMBIGUOUS` | 2026-11-10T12:20:00Z | P:809-814, RES L-79 |  |
| L-80 | TXT RRSIG inception > expiration | `INVALID / RRSIG_INTERVAL_REVERSED` | 2026-11-10T12:20:00Z | P:811-812, RES L-80 |  |
| L-81 | TXT RRSIG inception = expiration = T_snap | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:812-814, RES L-81 |  |
| L-82 | 2106 rollover: RRSIG expirations wrap past 2^32 around T_snap | `VALID_STRICT / OK` | 2106-02-07T05:20:00Z | P:809-814, RES L-82 | EA-13 |
| DNS-sig | TXT RRSIG cryptographically invalid | `INVALID / DNSSEC_SIGNATURE_INVALID` | 2026-11-10T12:20:00Z | P:555 |  |
| DNS-expired | Only TXT RRSIG expired at T_snap | `INVALID / RRSIG_NOT_VALID_AT_EVAL_TIME` | 2026-11-10T12:20:00Z | P:549-550 |  |
| DNS-rootsig | Root RRSIG by KSK-B cryptographically invalid | `INVALID / TRUSTED_KSK_SIGNATURE_INVALID` | 2026-11-10T12:20:00Z | P:424-426, P:439-440 |  |
| F05-a | TXT signer DNSKEY has Zone Key flag clear | `INVALID / DNSSEC_KEY_MISMATCH` | 2026-11-10T12:20:00Z | P:551-553, P:559-560 |  |
| F05-b | TXT signer DNSKEY has protocol 2 | `INVALID / DNSSEC_KEY_MISMATCH` | 2026-11-10T12:20:00Z | P:551-553 |  |
| F05-c | TXT RRSIG Labels 4 > owner label count 3 | `INVALID / DNSSEC_RRSIG_METADATA` | 2026-11-10T12:20:00Z | P:554 |  |
| F05-d | TXT RRSIG alg 13 with a 63-byte signature | `INVALID / DNSSEC_FORMAT` | 2026-11-10T12:20:00Z | P:555, P:1239-1240 |  |
| F05-e | Parent-blocked child (DS type 1 only) with a locally invalid TXT signature | `INVALID / DNSSEC_SIGNATURE_INVALID` | 2026-11-10T12:20:00Z | P:545-548, P:556-558 |  |
| F05-f | TXT RRSIG key tag matching no DNSKEY | `INVALID / DNSSEC_KEY_MISMATCH` | 2026-11-10T12:20:00Z | P:551-553, P:559-560 |  |
| F06-a | Root-only -> TXT (TXT signed directly by the root ZSK) | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:1226-1228 |  |
| F06-b | Missing last DNSKEY group (wamason.com DNSKEY) | `UNVERIFIABLE / DNS_EVIDENCE_MISSING` | 2026-11-10T12:20:00Z | P:1224-1226, P:538-539 |  |
| F06-c | Missing DS group (wamason.com DS) | `UNVERIFIABLE / DNS_EVIDENCE_MISSING` | 2026-11-10T12:20:00Z | P:1224-1226, P:538-539 |  |
| F06-d | Missing root DNSKEY group | `UNVERIFIABLE / NO_TRUSTED_KSK_USABLE` | 2026-11-10T12:20:00Z | P:1224-1226 |  |
| F06-e | Wrong-owner TXT (_tessera-v2.wamason.com) | `INVALID / DNS_OWNER` | 2026-11-10T12:20:00Z | P:1231-1232, P:504-505 |  |
| F06-f | Malformed TXT character-string (length byte runs past RDATA) | `INVALID / DNS_RDATA` | 2026-11-10T12:20:00Z | P:1239-1240, ENC 7:557-558 |  |
| F06-g | TXT RDATA with two character-strings | `INVALID / DNS_STRINGS` | 2026-11-10T12:20:00Z | ENC 7:557-558 |  |
| F06-h | Two TXT RRs at the owner | `INVALID / DNS_RRSET` | 2026-11-10T12:20:00Z | P:252, ENC 7:557 |  |
| F07-b | Primary-key tie (same tag/inception/expiration/signature), canonical RDATA order | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:1218-1221 |  |
| F07-c | Primary-key tie in the reverse order | `INVALID / SNAPSHOT_FORMAT` | 2026-11-10T12:20:00Z | P:1218-1221, P:1237-1238 |  |
| F07-d | Duplicate TXT RRSIG | `INVALID / SNAPSHOT_FORMAT` | 2026-11-10T12:20:00Z | P:1220-1221 |  |

**DNS record**

| Case | Fixture | Expected | T | Profile citation | EA |
|---|---|---|---|---|---|
| DNS-wlen | Window of 90 days + 1 s in both channels | `INVALID / DNS_WINDOW_LENGTH` | 2026-11-10T12:20:00Z | P:583-584, ENC 7:612 |  |
| DNS-wlen90 | Window of exactly 90 days (control) | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:583-584 |  |
| DNS-keys | Both channels publish another kms fingerprint | `INVALID / DNS_KEY_MISMATCH` | 2026-11-10T12:20:00Z | P:684-691, P:1393 |  |
| DNS-profile | Both channels publish profile=tessera-v1-other | `INVALID / DNS_PROFILE` | 2026-11-10T12:20:00Z | ENC 7:609 |  |
| CH-01 | Git blob carries a different window than DNS | `INVALID / CHANNEL_VALUE_MISMATCH` | 2026-11-10T12:20:00Z | P:646, P:1394 |  |
| CH-02 | Git blob = DNS value plus trailing LF | `INVALID / CHANNEL_VALUE_MISMATCH` | 2026-11-10T12:20:00Z | P:637-639, P:1394 | EA-21 (field: reason) |

**proofs**

| Case | Fixture | Expected | T | Profile citation | EA |
|---|---|---|---|---|---|
| SNAP-stamp | Snapshot proof digest = SHA256(body), not of the ENC 6 envelope | `INVALID / SNAPSHOT_STAMP_MISMATCH` | 2026-11-10T12:20:00Z | P:1177-1179, P:1381 |  |
| SNAP-pending | Snapshot proof pending-only | `UNVERIFIABLE / SNAPSHOT_NOT_ANCHORED` | 2026-11-10T12:20:00Z | P:450-451, P:744-745, P:1381 |  |
| SNAP-shape | Snapshot proof: digest double-hashed then a transaction (txid-subset shape fails) | `INVALID / OTS_TX_SHAPE` | 2026-11-10T12:20:00Z | P:753-757, P:1203-1206 |  |
| GIT-shape | Git proof: digest double-hashed then a transaction | `INVALID / OTS_TX_SHAPE` | 2026-11-10T12:20:00Z | P:753-757, P:1390 |  |
| GIT-pending | Git proof pending-only | `UNVERIFIABLE / GIT_NOT_ANCHORED` | 2026-11-10T12:20:00Z | P:744-745, P:1390 |  |
| GIT-stamp | Git proof digest over the commit id without LF | `INVALID / GIT_STAMP_MISMATCH` | 2026-11-10T12:20:00Z | P:629-630, P:1179 |  |

**OTS**

| Case | Fixture | Expected | T | Profile citation | EA |
|---|---|---|---|---|---|
| L-83 | receipt_anchor.txid != path-derived txid | `INVALID / ANCHOR_TXID_MISMATCH` | 2026-11-10T12:20:00Z | P:1189-1190, P:1376, RES L-83 |  |
| L-84 | Codex F09 proof: digest double-hashed into a commitment, then a real transaction | `INVALID / ANCHOR_TXID_MISMATCH` | 2026-11-10T12:20:00Z | P:1184-1191, RES L-84 |  |
| L-85 | SegWit-serialized transaction preimage | `INVALID / ANCHOR_TXID_MISMATCH` | 2026-11-10T12:20:00Z | P:1186-1188, RES L-85 |  |
| F09-a | Transaction with non-shortest CompactSize input count | `INVALID / ANCHOR_TXID_MISMATCH` | 2026-11-10T12:20:00Z | P:1188, P:1192-1193 |  |
| F09-b | Multi-input / multi-output, non-125-byte transaction (control) | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:1184-1191 |  |
| F09-c | Non-conventional merkle suffix (single sha256) | `INVALID / ANCHOR_TXID_MISMATCH` | 2026-11-10T12:20:00Z | P:1197-1200 |  |
| F08-a | Two paths at the selected height: one satisfies the txid subset, one does not | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:750-753, P:1190-1191 |  |
| L-86 | Redundant LEB128 (height varuint with an extra zero group) | `INVALID / OTS_FORMAT` | null | P:1173-1174, RES L-86 |  |
| L-87a | SHA-1 op (0x02) | `INVALID / OTS_FORMAT` | null | P:1163, P:1177, RES L-87 |  |
| L-87b | RIPEMD-160 op (0x03) | `INVALID / OTS_FORMAT` | null | P:1163, P:1177, RES L-87 |  |
| L-87c | Unknown attestation tag | `INVALID / OTS_FORMAT` | null | P:1177, RES L-87 |  |
| L-87d | Depth bound exceeded (pending branch at depth 257) | `INVALID / OTS_FORMAT` | null | P:1170-1171, P:1175, RES L-87 |  |
| L-87e | Depth bound edge (pending branch at depth 256, control) | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:1170-1171, P:1175 | EA-26 |
| F09-d | Bitcoin attestation message of 33 bytes | `INVALID / OTS_FORMAT` | null | P:1169-1170 |  |
| F09-e | Pending payload not consumed (extra byte after the URI) | `INVALID / OTS_FORMAT` | null | P:1167-1169 |  |
| F09-f | Receipt proof with exactly 65536 op items (bound edge, control) | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:1171-1172, P:1175 |  |
| F09-g | Receipt proof with 65537 op items | `INVALID / OTS_FORMAT` | null | P:1171-1172, P:1175 |  |
| F09-h | Receipt proof with exactly 4096 attestations (bound edge, control) | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:1175 |  |
| F09-i | Receipt proof with 4097 attestations | `INVALID / OTS_FORMAT` | null | P:1175 |  |
| L-88 | Receipt OTS digest != SHA256(a_sig): S_gpg re-serialized after stamping | `INVALID / RECEIPT_ANCHOR_MISMATCH` | null | P:1178-1179, P:703-706, P:291-293, RES L-88 |  |
| SNAP-otsfmt | Snapshot proof with redundant LEB128 | `INVALID / OTS_FORMAT` | 2026-11-10T12:20:00Z | P:1173-1174, P:1381 |  |

**git**

| Case | Fixture | Expected | T | Profile citation | EA |
|---|---|---|---|---|---|
| L-89 | Merge commit with two distinct parents | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:1256, RES L-89 |  |
| L-90 | Repeated identical parent | `INVALID / GIT_COMMIT_FORMAT` | 2026-11-10T12:20:00Z | P:1256-1258, RES L-90 |  |
| L-91a | `encoding` header | `INVALID / GIT_COMMIT_FORMAT` | 2026-11-10T12:20:00Z | P:1257-1258, RES L-91 |  |
| L-91b | Second `gpgsig` | `INVALID / GIT_COMMIT_FORMAT` | 2026-11-10T12:20:00Z | P:1257-1258, RES L-91 |  |
| L-91c | Unsigned commit (no gpgsig) | `INVALID / GIT_COMMIT_FORMAT` | 2026-11-10T12:20:00Z | P:1255, P:595 |  |
| L-91d | `gpgsig-sha256` header | `INVALID / GIT_COMMIT_FORMAT` | 2026-11-10T12:20:00Z | P:1257 |  |
| L-92a | Armor header line | `INVALID / GIT_SIG_FORMAT` | 2026-11-10T12:20:00Z | P:1263, RES L-92 |  |
| L-92b | Armor CRC mismatch | `INVALID / GIT_SIG_FORMAT` | 2026-11-10T12:20:00Z | P:1263-1264, RES L-92 |  |
| L-92c | 77-character base64 line | `INVALID / GIT_SIG_FORMAT` | 2026-11-10T12:20:00Z | P:1261-1262, RES L-92 |  |
| L-92d | Armor without CRC line (control) | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:1262 |  |
| L-92e | Armor base64 with nonzero pad bits | `INVALID / GIT_SIG_FORMAT` | 2026-11-10T12:20:00Z | P:1265-1266 |  |
| L-92f | Git signature type 0x01 (text) | `INVALID / GIT_SIG_FORMAT` | 2026-11-10T12:20:00Z | P:1264, P:625-627 |  |
| L-92g | Git signature with an unknown critical hashed subpacket | `INVALID / GIT_SIG_FORMAT` | 2026-11-10T12:20:00Z | P:625-627, P:836-837 |  |
| L-93a | Root tree entries not in git order | `INVALID / GIT_TREE_FORMAT` | 2026-11-10T12:20:00Z | P:1269-1271, RES L-93 |  |
| L-93b | Tree mode 040000 | `INVALID / GIT_TREE_FORMAT` | 2026-11-10T12:20:00Z | P:1269, RES L-93 |  |
| L-95 | Signer verifies, T_git outside a finalized interval | `INVALID / GIT_SIGNER_OUTSIDE_INTERVAL` | 2026-11-10T12:20:00Z | P:615-617, P:618-622, RES L-95 |  |
| L-96 | No configured signer verifies (commit signed by another key) | `UNVERIFIABLE / GIT_SIGNER_NOT_CONFIGURED` | 2026-11-10T12:20:00Z | P:615-617, RES L-96 |  |
| GIT-prefix | Git signature hash prefix wrong | `UNVERIFIABLE / GIT_SIGNER_NOT_CONFIGURED` | 2026-11-10T12:20:00Z | P:625-627, P:855-857 |  |
| GIT-path-a | Blob at tessera-v1/key-assertion.txt | `INVALID / GIT_PATH` | 2026-11-10T12:20:00Z | P:1272-1273 |  |
| GIT-path-b | Leaf mode 100755 | `INVALID / GIT_PATH` | 2026-11-10T12:20:00Z | P:637-639, P:1272-1273 |  |
| GIT-path-c | Commit names a tree id other than trees[0] | `INVALID / GIT_PATH` | 2026-11-10T12:20:00Z | P:1272-1273 | EA-22 (field: reason) |
| GIT-path-d | git.trees in the order [sub, root] | `INVALID / GIT_PATH` | 2026-11-10T12:20:00Z | P:1272-1273 |  |

**signature profile**

| Case | Fixture | Expected | T | Profile citation | EA |
|---|---|---|---|---|---|
| L-97 | Hashed creation time marked critical | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:834-835, RES L-97 |  |
| L-98 | Critical bit on the unhashed issuer key ID | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:838, RES L-98 |  |
| L-99 | Unknown critical hashed subpacket | `INVALID / SIG_POLICY` | 2026-11-10T12:20:00Z | P:836-837, P:840, RES L-99 |  |
| L-100 | Hashed signature-expiration (type 3) | `INVALID / SIG_POLICY` | 2026-11-10T12:20:00Z | P:835, RES L-100 |  |
| L-101 | Two type-2 subpackets | `INVALID / SIG_POLICY` | 2026-11-10T12:20:00Z | P:834, RES L-101 |  |
| L-102a | Type 2 with 3 data octets | `INVALID / SIG_POLICY` | 2026-11-10T12:20:00Z | P:834, RES L-102 |  |
| L-102b | Type 2 with 5 data octets | `INVALID / SIG_POLICY` | 2026-11-10T12:20:00Z | P:834, RES L-102 |  |
| L-103 | No type 2 | `INVALID / SIG_POLICY` | 2026-11-10T12:20:00Z | P:834, RES L-103 |  |
| L-104a | Subpacket length 191, one-octet (shortest) form | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:869-873, RES L-104 |  |
| L-104b | Subpacket length 192, two-octet (shortest) form | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:869-873, RES L-104 |  |
| L-104c | Subpacket length 191 in five-octet form | `INVALID / SIG_FORMAT` | 2026-11-10T12:20:00Z | P:869-873, P:1350, RES L-104 |  |
| L-104d | Subpacket length 192 in five-octet form | `INVALID / SIG_FORMAT` | 2026-11-10T12:20:00Z | P:869-873, P:1350, RES L-104 |  |
| F10-a | Zero-data critical type 33 | `INVALID / SIG_POLICY` | 2026-11-10T12:20:00Z | P:847-848 |  |
| F10-b | Two type-33 subpackets | `INVALID / SIG_POLICY` | 2026-11-10T12:20:00Z | P:845-846 |  |
| F10-c | Hashed type 16 inconsistent with type 33 | `INVALID / SIG_POLICY` | 2026-11-10T12:20:00Z | P:846-847 |  |
| F10-d | Hashed type 16 with 7 octets | `INVALID / SIG_POLICY` | 2026-11-10T12:20:00Z | P:845 |  |
| F10-e | Type 33 whose first octet is 05 | `INVALID / SIG_POLICY` | 2026-11-10T12:20:00Z | P:845-846 |  |
| F10-f | Wrong hash-prefix octets on the gpg receipt signature | `INVALID / SIG_INVALID` | 2026-11-10T12:20:00Z | P:855-857, P:1365 |  |
| F10-g | r = n in the gpg receipt signature | `INVALID / SIG_POLICY` | 2026-11-10T12:20:00Z | P:839-840 | EA-23 (field: reason) |
| SIG-type1 | Receipt signature type 0x01 | `INVALID / SIG_FORMAT` | 2026-11-10T12:20:00Z | ENC 5.2:468, P:1350 |  |
| SIG-newhdr | Receipt signature with OpenPGP-format header 0xC2 | `INVALID / SIG_PACKET` | 2026-11-10T12:20:00Z | ENC 5.2:447-451, P:1350 |  |

**possession**

| Case | Fixture | Expected | T | Profile citation | EA |
|---|---|---|---|---|---|
| POS-a | kms possession signature over another document | `INVALID / POSSESSION_INVALID` | 2026-11-10T12:20:00Z | P:840-842, P:1368 |  |
| POS-b | gpg possession signature with hashed type 3 | `INVALID / SIG_POLICY` | 2026-11-10T12:20:00Z | P:862-864, P:1367 |  |
| POS-c | gpg possession signature with header 0xC2 | `INVALID / SIG_PACKET` | 2026-11-10T12:20:00Z | P:862-865, P:1366 |  |

**keys**

| Case | Fixture | Expected | T | Profile citation | EA |
|---|---|---|---|---|---|
| L-105 | ML-DSA-65 SPKI in keys.kms under the fallback | `INVALID / KEY_FORMAT` | 2026-11-10T12:20:00Z | P:826-830, RES L-105 | EA-24 |
| KEY-a | keys.gpg is another valid key | `INVALID / KEY_MISMATCH` | 2026-11-10T12:20:00Z | P:829-830, P:1354 |  |
| KEY-b | keys.gpg with the 0x99 prefix | `INVALID / KEY_FORMAT` | 2026-11-10T12:20:00Z | P:825-826 |  |
| KEY-c | keys.gpg point off the curve | `INVALID / KEY_FORMAT` | 2026-11-10T12:20:00Z | P:858-861 |  |
| KEY-d | Both slots carry other valid keys | `INVALID / KEY_MISMATCH` | 2026-11-10T12:20:00Z | P:1354, P:1338 |  |

**receipt consistency**

| Case | Fixture | Expected | T | Profile citation | EA |
|---|---|---|---|---|---|
| RC-a | Frames disagree on content; manifest issuer also mismatches | `INVALID / RECEIPT_COMMON_MISMATCH` | 2026-11-10T12:20:00Z | P:694-699, P:1356 |  |
| RC-b | Bad common.manifest_sha256 | `INVALID / RECEIPT_MANIFEST_MISMATCH` | 2026-11-10T12:20:00Z | P:696-698, P:1352 |  |
| RC-c | Frames swapped between slots (each signed by its slot key) | `INVALID / RECEIPT_SLOT` | 2026-11-10T12:20:00Z | P:694-695, P:1355 |  |
| RC-d | Common issuer != manifest issuer | `INVALID / RECEIPT_MANIFEST_MISMATCH` | 2026-11-10T12:20:00Z | P:696, P:1357 |  |

**codec**

| Case | Fixture | Expected | T | Profile citation | EA |
|---|---|---|---|---|---|
| CODEC-a | Frame canonicalization version 2 | `INVALID / CV_UNKNOWN` | 2026-11-10T12:20:00Z | P:218-219, P:1350 |  |
| CODEC-b | Anchor count byte 3 | `INVALID / ANCHOR_COUNT` | 2026-11-10T12:20:00Z | ENC 5:383, P:1350 |  |
| CODEC-c | Withdrawn frame-only anchor tag | `INVALID / TAG_UNKNOWN` | 2026-11-10T12:20:00Z | ENC 5.1, P:218-219 |  |
| CODEC-d | Trailing byte after the second signature in a_sig | `INVALID / TRAILING` | 2026-11-10T12:20:00Z | ENC 5:391-392 |  |
| CODEC-e | Signed common.profile other than tessera-v1-strict | `INVALID / SCHEMA` | 2026-11-10T12:20:00Z | P:218-219 |  |
| CODEC-f | First a_sig frame carries the manifest tag | `INVALID / TAG_MISMATCH` | 2026-11-10T12:20:00Z | P:235, ENC 2:215-218 |  |

**aggregation**

| Case | Fixture | Expected | T | Profile citation | EA |
|---|---|---|---|---|---|
| L-106 | KEY_MISMATCH plus a bad git signature (CRC) | `INVALID / KEY_MISMATCH` | 2026-11-10T12:20:00Z | P:1354, P:1386, RES L-106 |  |
| L-107 | Unknown alg plus an independent failure (preamble altered) | `INVALID / BUNDLE_OBJECT_HASH` | 2026-11-10T12:20:00Z | P:263, P:1396, RES L-107 |  |
| L-108 | Bad attestation signature plus a usable receipt anchor | `INVALID / SIG_INVALID` | 2026-11-10T12:20:00Z | P:1365, P:291-293, RES L-108 |  |
| L-109 | Receipt proof with a contradicted lower branch | `INVALID / OTS_MERKLE_MISMATCH` | null | P:291-293, P:742-743, RES L-109 |  |
| AGG-a | POSSESSION_INVALID + DNS_WILDCARD + GIT_PATH | `INVALID / POSSESSION_INVALID` | 2026-11-10T12:20:00Z | P:1368, P:1380, P:1389 |  |
| AGG-b | SNAPSHOT_TIME + GIT_COMMIT_FORMAT | `INVALID / SNAPSHOT_TIME` | 2026-11-10T12:20:00Z | P:1384, P:1385 |  |
| AGG-c | SPEC_UNKNOWN + GIT_PATH | `INVALID / GIT_PATH` | 2026-11-10T12:20:00Z | P:263, P:1389 |  |
| AGG-d | MEMBER_MISSING:git + ALG_UNKNOWN | `UNVERIFIABLE / MEMBER_MISSING:git` | 2026-11-10T12:20:00Z | P:1347, P:1358 |  |
| AGG-e | TXT absent + git pending-only | `UNVERIFIABLE / DNS_EVIDENCE_MISSING` | 2026-11-10T12:20:00Z | P:1382-1383, P:1390 |  |
| AGG-f | ISSUANCE_WINDOW + BUNDLE_OBJECT_HASH | `INVALID / ISSUANCE_WINDOW` | 2026-11-10T12:20:00Z | P:1395, P:1396 |  |
| AGG-g | HEADER_CONFLICTS_PIN + SIG_INVALID | `INVALID / SIG_INVALID` | 2026-11-10T12:20:00Z | P:1365, P:1369 |  |
| AGG-h | DNS_KEY_MISMATCH + CHANNEL_VALUE_MISMATCH + ISSUANCE_WINDOW | `INVALID / DNS_KEY_MISMATCH` | 2026-11-10T12:20:00Z | P:1393-1395 |  |

**field grammar**

| Case | Fixture | Expected | T | Profile citation | EA |
|---|---|---|---|---|---|
| L-110a | declared_issue_time year 0000 | `INVALID / SCHEMA` | 2026-11-10T12:20:00Z | P:938, RES L-110 |  |
| L-110b | declared_issue_time year 0001 (codec accepts) | `INVALID / TIME_AFTER_DECLARED_DELTA` | 2026-11-10T12:20:00Z | P:938, P:720-722, RES L-110 |  |
| L-110c | declared_issue_time year 9999 (codec accepts) | `INVALID / TIME_BEFORE_DECLARED_EPSILON` | 2026-11-10T12:20:00Z | P:938, P:720-722, RES L-110 |  |
| L-110d | Numeric top label in issuer (wamason.123) | `INVALID / ISSUER_NOT_PINNED` | 2026-11-10T12:20:00Z | P:938-941, RES L-110 |  |

**numbers**

| Case | Fixture | Expected | T | Profile citation | EA |
|---|---|---|---|---|---|
| L-111a | Content with ES-boundary numbers (1e21, 5e-324, 1.2345678901234568e20, 9.8, 100) | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:918-936, RES L-111 |  |
| L-111b | Payload number -0 | `INVALID / JSON_NUMBER` | 2026-11-10T12:20:00Z | P:918-921, ENC 1.2 |  |
| L-111c | Payload number spelled 1E2 (value-preserving, non-canonical) | `INVALID / JSON_NONCANONICAL` | 2026-11-10T12:20:00Z | ENC 1.4 check 7, P:1350 |  |

**hybrid routing**

| Case | Inst. | Fixture | Expected | T | Profile citation | EA |
|---|---|---|---|---|---|---|
| HY-a1-C | classical | (a1) Pair id before registration: 3309-byte kms signature (genuine ML-DSA-65 bytes), rule-O gpg | `UNVERIFIABLE / ALG_UNKNOWN` | 2026-11-10T12:20:00Z | P:114-119, P:120-126, P:1469, P:127-130, P:225-228, P:280-283, P:1461, P:1475-1479, P:741-750, HC (a) |  |
| HY-a2-C | classical | (a2) Pair id before registration: rule-O packets in both slots (kms 119-byte class) | `UNVERIFIABLE / ALG_UNKNOWN` | 2026-11-10T12:20:00Z | P:114-119, P:120-126, P:1469, P:127-130, P:1461, HC (a) |  |
| HY-a3-C | classical | (a3) Pair id before registration: arbitrary 1-byte kms and 65536-byte gpg signatures and possession proofs | `UNVERIFIABLE / ALG_UNKNOWN` | 2026-11-10T12:20:00Z | P:114-119, P:120-126, P:1469, P:127-130, P:1461, P:1477, HC (a) |  |
| HY-a4-C | classical | (a) Pair id before registration: empty kms signature | `INVALID / SIG_EMPTY` | 2026-11-10T12:20:00Z | P:127-130, P:225-226, P:1461, P:269-272, HC (a) |  |
| HY-a5-C | classical | (a) Pair id before registration: 65537-byte gpg signature | `INVALID / LENGTH_CAP` | 2026-11-10T12:20:00Z | P:127-130, P:225-226, P:1461, P:269-272, HC (a) |  |
| HY-ak-C | classical | (a) A genuine hybrid receipt (ML-DSA-65 SPKI in keys.kms, hybrid spec hash) presented to the classical installation | `INVALID / KEY_FORMAT` | 2026-11-10T12:20:00Z | P:884-891, P:1464, P:127-130, P:269-272, P:1469, HC (a) | EA-31 (fields: verdict, reason; alt UNVERIFIABLE / ALG_UNKNOWN) |
| HY-b1-H | hybrid | (b) Classical-id receipt as a fallback issuer emits it (P-256 kms SPKI, valid rule-O signatures) under the hybrid installation | `INVALID / KEY_FORMAT` | 2026-11-10T12:20:00Z | P:884-891, P:1464, P:120-126, P:1469, P:269-272, HC (b) | EA-31 (fields: verdict, reason; alt UNVERIFIABLE / ALG_UNKNOWN) |
| HY-b2-H | hybrid | (b) Classical-id frames, rule-O signatures that do not verify, kms key in the installation's format (ML-DSA-65 SPKI) | `UNVERIFIABLE / ALG_UNKNOWN` | 2026-11-10T12:20:00Z | P:120-126, P:884-888, P:1461, P:1464-1469, P:1475-1479, P:741-750, HC (b) |  |
| HY-c1-C | classical | (c) Classical-id receipt, XA-19 shape: kms packet under an OpenPGP-format 0xC2 header (classical installation) | `INVALID / SIG_PACKET` | 2026-11-10T12:20:00Z | P:120-123, P:225-226, P:1461, P:269-272, HC (c) |  |
| HY-c2-C | classical | (c) Classical-id receipt, XA-22 shape: kms signature type 0x01 (classical installation) | `INVALID / SIG_FORMAT` | 2026-11-10T12:20:00Z | P:120-123, P:225-226, P:1461, P:269-272, HC (c) |  |
| HY-c3-C | classical | (c) Classical-id receipt, XA-14 shape: kms signature of 1025 bytes (above the rule-O cap 1024) (classical installation) | `INVALID / LENGTH_CAP` | 2026-11-10T12:20:00Z | P:120-123, P:225-226, P:1461, P:269-272, HC (c) |  |
| HY-c4-C | classical | (c) Classical-id receipt, XA-11 shape: empty kms signature (classical installation) | `INVALID / SIG_EMPTY` | 2026-11-10T12:20:00Z | P:120-123, P:225-226, P:1461, P:269-272, HC (c) |  |
| HY-c1-H | hybrid | (c) Classical-id receipt, XA-19 shape: kms packet under an OpenPGP-format 0xC2 header (hybrid installation) | `INVALID / SIG_PACKET` | 2026-11-10T12:20:00Z | P:120-123, P:225-226, P:1461, P:269-272, HC (c) |  |
| HY-c2-H | hybrid | (c) Classical-id receipt, XA-22 shape: kms signature type 0x01 (hybrid installation) | `INVALID / SIG_FORMAT` | 2026-11-10T12:20:00Z | P:120-123, P:225-226, P:1461, P:269-272, HC (c) |  |
| HY-c3-H | hybrid | (c) Classical-id receipt, XA-14 shape: kms signature of 1025 bytes (above the rule-O cap 1024) (hybrid installation) | `INVALID / LENGTH_CAP` | 2026-11-10T12:20:00Z | P:120-123, P:225-226, P:1461, P:269-272, HC (c) |  |
| HY-c4-H | hybrid | (c) Classical-id receipt, XA-11 shape: empty kms signature (hybrid installation) | `INVALID / SIG_EMPTY` | 2026-11-10T12:20:00Z | P:120-123, P:225-226, P:1461, P:269-272, HC (c) |  |
| HY-d1-C | classical | (d) Frames and manifest all carry KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA384 (near-miss pair id (P8 XHR-09)); classical installation | `UNVERIFIABLE / ALG_UNKNOWN` | 2026-11-10T12:20:00Z | P:117, P:120-126, P:1461, P:1469, P:741-750, HC (d) |  |
| HY-d2-C | classical | (d) Frames and manifest all carry X-UNKNOWN-ALG-1 (P8 A-02); classical installation | `UNVERIFIABLE / ALG_UNKNOWN` | 2026-11-10T12:20:00Z | P:117, P:120-126, P:1461, P:1469, P:741-750, HC (d) |  |
| HY-d1-H | hybrid | (d) Frames and manifest all carry KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA384 (near-miss pair id (P8 XHR-09)); hybrid installation | `UNVERIFIABLE / ALG_UNKNOWN` | 2026-11-10T12:20:00Z | P:117, P:120-126, P:1461, P:1469, P:741-750, HC (d) |  |
| HY-d2-H | hybrid | (d) Frames and manifest all carry X-UNKNOWN-ALG-1 (P8 A-02); hybrid installation | `UNVERIFIABLE / ALG_UNKNOWN` | 2026-11-10T12:20:00Z | P:117, P:120-126, P:1461, P:1469, P:741-750, HC (d) |  |
| HY-e1-C | classical | (e1) kms frame pair id, gpg frame classical id, manifest pair id (M9 shape, P8 XHR-08); classical installation | `INVALID / RECEIPT_COMMON_MISMATCH` | 2026-11-10T12:20:00Z | P:123-124, P:751-759, P:1467, P:269-272, HC (e) |  |
| HY-e2-C | classical | (e2) Both frames pair id, manifest classical id; classical installation | `INVALID / RECEIPT_MANIFEST_MISMATCH` | 2026-11-10T12:20:00Z | P:123-124, P:751-759, P:1468, P:269-272, HC (e) |  |
| HY-e3-C | classical | (e3) Both frames X-UNKNOWN-ALG-1, manifest X-UNKNOWN-ALG-2; classical installation | `INVALID / RECEIPT_MANIFEST_MISMATCH` | 2026-11-10T12:20:00Z | P:123-124, P:751-759, P:1468, HC (e) |  |
| HY-e1-H | hybrid | (e1) kms frame pair id, gpg frame classical id, manifest pair id (M9 shape, P8 XHR-08); hybrid installation | `INVALID / RECEIPT_COMMON_MISMATCH` | 2026-11-10T12:20:00Z | P:123-124, P:751-759, P:1467, P:269-272, HC (e) |  |
| HY-e2-H | hybrid | (e2) Both frames pair id, manifest classical id; hybrid installation | `INVALID / RECEIPT_MANIFEST_MISMATCH` | 2026-11-10T12:20:00Z | P:123-124, P:751-759, P:1468, P:269-272, HC (e) |  |
| HY-e3-H | hybrid | (e3) Both frames X-UNKNOWN-ALG-1, manifest X-UNKNOWN-ALG-2; hybrid installation | `INVALID / RECEIPT_MANIFEST_MISMATCH` | 2026-11-10T12:20:00Z | P:123-124, P:751-759, P:1468, HC (e) |  |

**hybrid positive**

| Case | Inst. | Fixture | Expected | T | Profile citation | EA |
|---|---|---|---|---|---|---|
| HY-V1 | hybrid | Full hybrid receipt through the issuer: kms ML-DSA-65 (rule R, EXTERNAL_MU), gpg P-256 (rule O); 779 / 778-byte frames | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:114-119, P:134-136, P:148, P:878-880, P:884-888, P:905-907, HS §1-§3, A9.6 (A9:351-362) |  |
| HY-V2 | hybrid | Full hybrid receipt with frames over 4096 bytes (6753 / 6752), signed by external mu | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:114-119, P:134-136, P:148, P:878-880, P:884-888, P:905-907, HS §1-§3, A9.6 (A9:351-362), A9:361-362 |  |

**hybrid semantics**

| Case | Inst. | Fixture | Expected | T | Profile citation | EA |
|---|---|---|---|---|---|---|
| HY-N1 | hybrid | Pair id with a P-256 SPKI in keys.kms (fingerprints consistent; 3309-byte kms signature) | `INVALID / KEY_FORMAT` | 2026-11-10T12:20:00Z | P:884-889, P:1464, HS §3 |  |
| HY-N2 | hybrid | kms ML-DSA-65 signature over another frame (anchor rebuilt) | `INVALID / SIG_INVALID` | 2026-11-10T12:20:00Z | P:1476, HS §2 |  |
| HY-N3 | hybrid | kms possession proof over other bytes | `INVALID / POSSESSION_INVALID` | 2026-11-10T12:20:00Z | P:905-907, P:1479 |  |
| HY-N4 | hybrid | kms signature truncated to 3308 bytes | `INVALID / SIG_FORMAT` | 2026-11-10T12:20:00Z | P:134-136, P:1461, HS §2 (XH-01..04) |  |
| HY-N5 | hybrid | kms signature with a trailing byte (3310 bytes) | `INVALID / LENGTH_CAP` | 2026-11-10T12:20:00Z | P:134-136, P:1461, HS §2 (XH-01..04) |  |
| HY-N6 | hybrid | kms signature valid under the nonempty context 'tessera-v1' (XHR-13) | `INVALID / SIG_INVALID` | 2026-11-10T12:20:00Z | P:1476, HS §1 (empty context) |  |

**authority isolation**

| Case | Inst. | Fixture | Expected | T | Profile citation | EA |
|---|---|---|---|---|---|---|
| AUTH-i | classical | Attacker-keyed receipt, re-stamped; both channels publish the legitimate keys | `INVALID / DNS_KEY_MISMATCH` | 2026-11-10T12:20:00Z | P:741-750, P:1504, P:1038-1043, P:253-256, P:269-272, P:1442-1447, A9:143, A9:153, prototype/mutation/REPORT.md obs. 3 |  |
| AUTH-i-T | classical | Honest twin of AUTH-i: the same attacker keys, published in DNS and git (the attacker holds both channel credentials) | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:741-750, P:1504, P:1038-1043, P:269-272 |  |
| AUTH-ii-root | classical | Attacker-keyed receipt; DNS: the attacker's own root, com and wamason.com zones (no configured root KSK); git assertion valid | `UNVERIFIABLE / NO_TRUSTED_KSK_USABLE` | 2026-11-10T12:20:00Z | P:466-469, P:470-484, P:557-561, P:590-593, P:1042-1043, P:1493, P:555-556, A9:309-324, P:253-256, P:269-272, P:1442-1447, A9:143, A9:153, prototype/mutation/REPORT.md obs. 3 |  |
| AUTH-ii-root-T | classical | Honest twin of AUTH-ii-root: the TXT signed under the trusted path (the honest wamason.com ZSK) | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:466-469, P:470-484, P:557-561, P:590-593, P:1042-1043, P:1493, P:555-556, A9:309-324, P:269-272 |  |
| AUTH-ii-ds | classical | Attacker-keyed receipt; DNS: honest root and com, the honest wamason.com DS, the attacker's own wamason.com DNSKEY set; git assertion valid | `INVALID / DNSKEY_DS_MISMATCH` | 2026-11-10T12:20:00Z | P:578-600, P:1493, P:555-556, A9:309-324, P:253-256, P:269-272, P:1442-1447, A9:143, A9:153, prototype/mutation/REPORT.md obs. 3 |  |
| AUTH-ii-ds-T | classical | Honest twin of AUTH-ii-ds: the TXT signed under the trusted path (the honest wamason.com ZSK) | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:578-600, P:1493, P:555-556, A9:309-324, P:269-272 |  |
| AUTH-ii-zsk | classical | Attacker-keyed receipt; DNS: honest chain to the wamason.com DNSKEY set; TXT signed by an attacker key outside it; git assertion valid | `INVALID / DNSSEC_KEY_MISMATCH` | 2026-11-10T12:20:00Z | P:594-600, P:604-605, P:609-613, P:1493, P:555-556, A9:309-324, P:253-256, P:269-272, P:1442-1447, A9:143, A9:153, prototype/mutation/REPORT.md obs. 3 |  |
| AUTH-ii-zsk-T | classical | Honest twin of AUTH-ii-zsk: the TXT signed under the trusted path (the honest wamason.com ZSK) | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:594-600, P:604-605, P:609-613, P:1493, P:555-556, A9:309-324, P:269-272 |  |
| AUTH-ii-tag | classical | Attacker-keyed receipt; DNS: as ii-zsk, but the attacker's RRSIG carries the honest ZSK's key tag; git assertion valid | `INVALID / DNSSEC_SIGNATURE_INVALID` | 2026-11-10T12:20:00Z | P:594-598, P:466-467, P:1493, P:555-556, A9:309-324, P:253-256, P:269-272, P:1442-1447, A9:143, A9:153, prototype/mutation/REPORT.md obs. 3 |  |
| AUTH-ii-tag-T | classical | Honest twin of AUTH-ii-tag: the TXT signed under the trusted path (the honest wamason.com ZSK) | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:594-598, P:466-467, P:1493, P:555-556, A9:309-324, P:269-272 |  |
| AUTH-iii | classical | Attacker-keyed receipt; DNS valid; git assertion signed by the attacker's own repository key | `UNVERIFIABLE / GIT_SIGNER_NOT_CONFIGURED` | 2026-11-10T12:20:00Z | P:668-670, P:671-677, P:1502, A9:333-338, P:253-256, P:269-272, P:1442-1447, A9:143, A9:153, prototype/mutation/REPORT.md obs. 3 |  |
| AUTH-iii-T | classical | Honest twin of AUTH-iii: the commit signed by the configured repository key | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:668-670, P:671-677, P:1502, A9:333-338, P:269-272 |  |
| AUTH-iv-end | classical | Attacker-keyed receipt; git assertion by the configured key after its finalized signing_end | `INVALID / GIT_SIGNER_OUTSIDE_INTERVAL` | 2026-11-10T12:20:00Z | P:668-677, P:1502, P:1419, A9:333-338, P:253-256, P:269-272, P:1442-1447, A9:143, A9:153, prototype/mutation/REPORT.md obs. 3 |  |
| AUTH-iv-end-T | classical | Honest twin of AUTH-iv-end: the same finalized entry ending 2026-11-03T00:00:00Z (after T_git) | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:668-677, P:1502, P:1419, A9:333-338, P:269-272 |  |
| AUTH-iv-start | classical | Attacker-keyed receipt; git assertion by the configured key before its signing_start (open entry) | `INVALID / GIT_SIGNER_OUTSIDE_INTERVAL` | 2026-11-10T12:20:00Z | P:671-679, P:519-521, P:1502, P:253-256, P:269-272, P:1442-1447, A9:143, A9:153, prototype/mutation/REPORT.md obs. 3 |  |
| AUTH-iv-start-T | classical | Honest twin of AUTH-iv-start: the open entry starting 2026-11-01T00:00:00Z (before T_git) | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:671-679, P:519-521, P:1502, P:269-272 |  |
| AUTH-v-eq | classical | Attacker-keyed receipt; git assertion anchored at h_receipt - 5 (not 6 blocks before) | `INVALID / GIT_NOT_PRECOMMITTED` | 2026-11-10T12:20:00Z | P:709-714, P:1503, A9:143, P:253-256, P:269-272, P:1442-1447, A9:153, prototype/mutation/REPORT.md obs. 3 |  |
| AUTH-v-eq-T | classical | Honest twin of AUTH-v-eq: h_git = 900018 (h_git + 5 < h_receipt) | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:709-714, P:1503, A9:143, P:269-272 |  |
| AUTH-v-after | classical | Attacker-keyed receipt; git assertion anchored after the receipt (h_git = h_receipt + 3) | `INVALID / GIT_NOT_PRECOMMITTED` | 2026-11-10T12:20:00Z | P:709-717, P:1503, A9:143, P:253-256, P:269-272, P:1442-1447, A9:153, prototype/mutation/REPORT.md obs. 3 |  |
| AUTH-v-after-T | classical | Honest twin of AUTH-v-after: the assertion anchored at 900018 | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:709-717, P:1503, A9:143, P:269-272 |  |
| AUTH-vi | classical | Attacker-keyed receipt for its own domain wamason-attacker.com, with a trusted DNSSEC path and a git assertion under the configured repository key | `INVALID / ISSUER_NOT_PINNED` | 2026-11-10T12:20:00Z | P:697-708, P:727-731, P:549-550, P:1470, A9:32, A9:68, P:253-256, P:269-272, P:1442-1447, A9:143, A9:153, prototype/mutation/REPORT.md obs. 3 |  |
| AUTH-vi-T | classical | Honest twin of AUTH-vi: issuer = wamason.com with the wamason.com chain | `VALID_STRICT / OK` | 2026-11-10T12:20:00Z | P:697-708, P:727-731, P:549-550, P:1470, A9:32, A9:68, P:269-272 |  |
