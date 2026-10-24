# Locator refresh: signed A9 and A10 citations in the V1 spec texts

Targets: `docs/V1-PROFILE.md`, `formal/p8/ENCODING-V1.md`, `formal/p8/PROOF.md`.
A9 (`docs/phase-0-prereg-amendment-9.md`, 532 lines) and A10 (`docs/phase-0-prereg-amendment-10.md`, 816 lines) are
unchanged since their signing commits (`git diff 2ad3489 --` and `git diff 9ade764 --` on the files are empty).
Each new locator was found by locating the cited words in the signed text. The pre-revision copy
`docs/reviews/a9-final-delta/A9-before-2026-10-13.md` was used to see what an old number meant where the citing
sentence was ambiguous. Line numbers in the table for "File line" are the citing line in the file after the edit
(no line moved; only locator text changed).

## Counts

- Locators checked: 137 (profile 136, PROOF 1, ENCODING-V1 0). Comma forms such as `A9:173, 179` count as two.
- Changed: 111 locators in 108 table rows (the three comma forms at lines 220, 633 and 1284 are one row each), all in `docs/V1-PROFILE.md`.
- Unchanged: 26 (already correct, or deliberately historical).
- Unresolved: 0.
- ENCODING-V1.md: no numeric `A9:n` or `A10:n` locators exist (only section references such as A9.5, A9.6, A9.8, A10.1, A10.5), so nothing changed and no CHANGELOG line was added.

## Unchanged

Already correct against the signed text (20 A10 locators and A9:24, A9:24-26): profile lines 68 (A9:24), 73 (A9:24-26), 119, 979 (A10:284-285, 343-344),
310, 318, 319, 326, 976, 983, 988, 991, 995, 1000, 1004, 1005, 1343, 1346, 1347 (all A10), and
`formal/p8/PROOF.md` line 462 (A10:248-249, the backward-skewed-header sentence).

Left on purpose because they record a stale or old locator as history, not as a live pointer: profile line 58
(A9:338-340, "cited ... which in the reviewed snapshot is"), line 408 (the dated correction quoting the old item 5 text
`A9:217`), and line 1013 (the "was cited A9:338-340, a stale locator" note).

## Changes

| File | Line | Old | New | Cited words |
|---|---|---|---|---|
| docs/V1-PROFILE.md | 67 | A9:12-18 | A9:16-22 | Decision labels: AUTHOR DECISION, OWNER DECISION, RECOMMENDED |
| docs/V1-PROFILE.md | 87 | A9:296-303 | A9:309-325 | reliance-period rule in A9.5 (root-KSK rule, OWNER DECISION 2026-10-13) |
| docs/V1-PROFILE.md | 99 | A9:142 | A9:148 | Profile id tessera-v1-strict inside the signed bytes |
| docs/V1-PROFILE.md | 138 | A9:143-144 | A9:149-150 | Encoding: ENCODING-V1 at the signing commit, D-1 to D-17 |
| docs/V1-PROFILE.md | 139 | A9:321-326 | A9:395-400 | dated branch-registration supplement governs hybrid branch |
| docs/V1-PROFILE.md | 141 | A9:155 | A9:161 | Mode: strict only, no wrappers/renewal/TLR/waiver; VALID_DEGRADED never returned |
| docs/V1-PROFILE.md | 142 | A9:123-140 | A9:128-146 | Claim and sub-claims C1 to C7 |
| docs/V1-PROFILE.md | 143 | A9:147 | A9:153 | Authority: DNSSEC for D plus git key assertion, n = 2 |
| docs/V1-PROFILE.md | 144 | A9:158-159 | A9:164-165 | Issuance: operated API; receipt ships only when complete |
| docs/V1-PROFILE.md | 146 | A9:217-219 | A9:223-225 | Parameters: delta, epsilon, k, N, S ratified by signature |
| docs/V1-PROFILE.md | 168 | A9:311-312 | A9:364-366 | manifest frame and possession signature verification (pass condition) |
| docs/V1-PROFILE.md | 171 | A9:282-284 | A9:297-299 | git key-assertion evidence; stamp targets signed commit id |
| docs/V1-PROFILE.md | 173 | A9:150 | A9:156 | headers must be in pinned set (HEADERS_NOT_COVERED) |
| docs/V1-PROFILE.md | 174 | A9:152-153 | A9:158-159 | spec bytes, content-addressed |
| docs/V1-PROFILE.md | 175 | A9:152-153 | A9:158-159 | conformance vector bytes, content-addressed |
| docs/V1-PROFILE.md | 176 | A9:153 | A9:159 | bound plain-language purpose preamble |
| docs/V1-PROFILE.md | 177 | A9:153-154 | A9:159-160 | dependency manifest |
| docs/V1-PROFILE.md | 211 | A9:148 | A9:154 | trust configuration ships with verifier, never from the bundle |
| docs/V1-PROFILE.md | 218 | A9:272 | A9:287 | unrecognized label gives UNVERIFIABLE / OUT_OF_PROFILE (Dispatch) |
| docs/V1-PROFILE.md | 219 | A9:272 | A9:287 | out-of-profile gives same result at dispatch |
| docs/V1-PROFILE.md | 220 | A9:173, 179 | A9:179, 185 | Cases c (two-layer transplant) and h (renewal wrapper) |
| docs/V1-PROFILE.md | 248 | A9:155 | A9:161 | No wrapper stage: one layer only |
| docs/V1-PROFILE.md | 251 | A9:137 | A9:143 | Authority stage: channels, issuance window (C4; verifier rule) |
| docs/V1-PROFILE.md | 251 | A9:338-340 | A9:419-421 | Authority stage: channels, issuance window (C4; verifier rule) |
| docs/V1-PROFILE.md | 254 | A9:138 | A9:144 | Temporal: three-conjunct predicate at k = 6 (C5) |
| docs/V1-PROFILE.md | 255 | A9:248-252 | A9:255-258 | Revocation not evaluated (A9.4 Weakened) |
| docs/V1-PROFILE.md | 258 | A9:338-340 | A9:419-421 | issuance-window check is part of stage (e) (C4 verifier rule) |
| docs/V1-PROFILE.md | 277 | A9:155 | A9:161 | no waiver set, degraded branch never applies |
| docs/V1-PROFILE.md | 278 | A9:176 | A9:182 | INVALID dominates UNVERIFIABLE (case d3, A4.2 precedence) |
| docs/V1-PROFILE.md | 297 | A9:156 | A9:162 | six stable fields; later-verifier contract |
| docs/V1-PROFILE.md | 297 | A9:262-268 | A9:268-283 | six stable fields; later-verifier contract |
| docs/V1-PROFILE.md | 299 | A9:248-252 | A9:255-258 | revocation: NOT_EVALUATED |
| docs/V1-PROFILE.md | 301 | A9:253-259 | A9:259-265 | historical_security: authenticated safe-before cutoff per algorithm and key |
| docs/V1-PROFILE.md | 302 | A9:166-167 | A9:172-173 | Standing ABSENT/NOT_ISSUED_IN_PROFILE |
| docs/V1-PROFILE.md | 330 | A9:344-345 | A9:425-426 | ISSUANCE_WINDOW from later proof; ask holder for original proof |
| docs/V1-PROFILE.md | 331 | A9:413-418 | A9:495-500 | verifier cannot check public publication of the git commit |
| docs/V1-PROFILE.md | 368 | A9:278-281 | A9:293-296 | issue order (eight steps) |
| docs/V1-PROFILE.md | 369 | A9:277 | A9:292 | frame-only anchor is withdrawn, no fallback |
| docs/V1-PROFILE.md | 371 | A9:341-342 | A9:422-423 | attempt whose T would exceed not-after is not shipped |
| docs/V1-PROFILE.md | 372 | A9:327-330 | A9:401-405 | gpg signer refuses declared_issue_time more than epsilon from its clock |
| docs/V1-PROFILE.md | 373 | A9:260 | A9:266 | issuer never re-authorizes a key |
| docs/V1-PROFILE.md | 373 | A9:413-418 | A9:495-500 | public publication of the commit stays an issuer duty |
| docs/V1-PROFILE.md | 398 | A9:148 | A9:154 | trust configuration never read from the bundle |
| docs/V1-PROFILE.md | 402 | A9:148-149 | A9:154-155 | Root KSK-2017 |
| docs/V1-PROFILE.md | 403 | A9:148-149 | A9:154-155 | Root KSK-2024 |
| docs/V1-PROFILE.md | 404 | A9:63-65 | A9:68-69 | D = wamason.com (AUTHOR DECISION Q5) |
| docs/V1-PROFILE.md | 405 | A9:149 | A9:155 | signed, versioned set of pinned mainnet header hashes |
| docs/V1-PROFILE.md | 447 | A9:153 | A9:154-155 | KSK signing and reliance periods kept apart from publication and revocation |
| docs/V1-PROFILE.md | 447 | A9:302-303 | A9:324-325 | KSK signing and reliance periods kept apart from publication and revocation |
| docs/V1-PROFILE.md | 458 | A9:296-303 | A9:309-325 | root-KSK rule, existential and order-independent (F1, F2) |
| docs/V1-PROFILE.md | 460 | A9:307-308 | A9:341-342 | Rollover control: one KSK published but not signing must pass |
| docs/V1-PROFILE.md | 532 | A9:150-151 | A9:156-157 | unlisted rollover gives UNVERIFIABLE |
| docs/V1-PROFILE.md | 612 | A9:150 | A9:156 | bundle header with no pin gives HEADERS_NOT_COVERED |
| docs/V1-PROFILE.md | 633 | A9:137, 147 | A9:143, 153 | Both channels must pass (n = 2); neither commits to any receipt |
| docs/V1-PROFILE.md | 634 | A9:332-333 | A9:407-408 | both channels carry the same issuance window |
| docs/V1-PROFILE.md | 645 | A9:137 | A9:143 | DNSSEC chain validated at snapshot own anchored time; root rule |
| docs/V1-PROFILE.md | 645 | A9:285-287 | A9:309-310 | DNSSEC chain validated at snapshot own anchored time; root rule |
| docs/V1-PROFILE.md | 726 | A9:334-337 | A9:409-411 | 90-day window invariant, DNS_WINDOW_LENGTH, one window |
| docs/V1-PROFILE.md | 729 | A9:338-340 | A9:419-421 | INVALID / ISSUANCE_WINDOW verifier rule |
| docs/V1-PROFILE.md | 730 | A9:360-366 | A9:441-447 | guarantee 2: UTC cutoff needs a backward-skew bound |
| docs/V1-PROFILE.md | 732 | A9:343 | A9:424 | A published window cannot be shortened |
| docs/V1-PROFILE.md | 733 | A9:341-342 | A9:422-423 | window dates and stop margin are operating numbers |
| docs/V1-PROFILE.md | 737 | A9:282-284 | A9:297-299 | OTS stamp targets signed commit object id |
| docs/V1-PROFILE.md | 745 | A9:284 | A9:299 | SHA-1 linkage is a stated residual |
| docs/V1-PROFILE.md | 779 | A9:334-337 | A9:409-411 | one window per record |
| docs/V1-PROFILE.md | 780 | A9:334-337 | A9:409-411 | one window per record (rotation mechanism) |
| docs/V1-PROFILE.md | 792 | A9:333 | A9:408 | git value and DNS value identical, window included |
| docs/V1-PROFILE.md | 817 | A9:202 | A9:208 | statements M2 and M5 (exit gate) |
| docs/V1-PROFILE.md | 823 | A9:137 | A9:143 | verifier fixes the required set (C4) |
| docs/V1-PROFILE.md | 853 | A9:280-281 | A9:295-296 | signature identifiers independent of bytes; anchor digest may commit to them |
| docs/V1-PROFILE.md | 866 | A9:138 | A9:144 | No lower bound and no priority; header times are chain-time proxies (C5) |
| docs/V1-PROFILE.md | 869 | A9:99 | A9:105-106 | k = 6 under DepthK = k - 1 (earlier owner decisions carried in) |
| docs/V1-PROFILE.md | 911 | A9:150 | A9:156 | bundle header outside pins gives HEADERS_NOT_COVERED |
| docs/V1-PROFILE.md | 934 | A9:99-101 | A9:104-106 | DNSSEC snapshot rule: owner decision carried in, not routed |
| docs/V1-PROFILE.md | 948 | A9:137 | A9:143 | DNSSEC evaluated at snapshot own anchored time (C4) |
| docs/V1-PROFILE.md | 1015 | A9:298-302 | A9:351-356 | hybrid: kms ML-DSA-65, gpg P-256; one pair algorithm id |
| docs/V1-PROFILE.md | 1060 | A9:136 | A9:142 | two keys separate technical failure domains under one controller (C3) |
| docs/V1-PROFILE.md | 1060 | A9:368-372 | A9:449-453 | two keys separate technical failure domains under one controller (C3) |
| docs/V1-PROFILE.md | 1134 | A9:248-252 | A9:255-258 | Revocation is not evaluated |
| docs/V1-PROFILE.md | 1138 | A9:153-154 | A9:159-160 | A9 names eight dependency-manifest entries |
| docs/V1-PROFILE.md | 1144 | A9:298-319 | A9:351-374 | signature algorithms: P-256 fallback, ML-DSA-65 under hybrid |
| docs/V1-PROFILE.md | 1149 | A9:150 | A9:159-160 | Bitcoin headers, as a dependency-manifest entry (owner correction 2026-10-24, FC-01; the agent first mapped it to A9:156) |
| docs/V1-PROFILE.md | 1188 | A9:290-292 | A9:343-344 | Custody: long-horizon validity depends on manifest and exact bytes; no renewal |
| docs/V1-PROFILE.md | 1194 | A9:438-443 | A9:519-524 | number rule: accept exactly when RFC 8785 preserves value (A9.8) |
| docs/V1-PROFILE.md | 1197 | A9:405-406 | A9:486-487 | replaces the IEEE 754 double rule (A9.7 rows 22-23) |
| docs/V1-PROFILE.md | 1198 | A9:440-443 | A9:521-524 | A9.8 replacement text |
| docs/V1-PROFILE.md | 1221 | A9:165-167 | A9:171-173 | every row: profile, NOT_EVALUATED fields, standing |
| docs/V1-PROFILE.md | 1222 | A9:169-181 | A9:175-187 | eleven rows cover thirteen cases |
| docs/V1-PROFILE.md | 1247 | A9:112-116 | A9:117-118 | zero unsafe accepts; false rejects only on d2 and h |
| docs/V1-PROFILE.md | 1248 | A9:183-186 | A9:189-191 | registered prediction: headline-only reader fails e and f |
| docs/V1-PROFILE.md | 1249 | A9:140 | A9:146 | C7 evidence: missing-capture negative control |
| docs/V1-PROFILE.md | 1249 | A9:267-268 | A9:281-283 | C7 evidence: missing-capture negative control |
| docs/V1-PROFILE.md | 1256 | A9:199-204 | A9:205-210 | exit statements M2, M5, E6a, E12 are 30 Oct items |
| docs/V1-PROFILE.md | 1257 | A9:208-210 | A9:214-216 | After exit: AWS vectors, missing-capture control, dead-service test |
| docs/V1-PROFILE.md | 1259 | A9:205-207 | A9:211-213 | Cut order if 30 Oct slips |
| docs/V1-PROFILE.md | 1270 | A9:152-154 | A9:158-160 | bundle members: spec, vectors, preamble, dependency manifest |
| docs/V1-PROFILE.md | 1271 | A9:148-151 | A9:154-157 | trust configuration items: two KSKs, repository key, pin set |
| docs/V1-PROFILE.md | 1272 | A9:156 | A9:162 | Stable output fields |
| docs/V1-PROFILE.md | 1273 | A9:153-154 | A9:159-160 | Dependency manifest entries |
| docs/V1-PROFILE.md | 1275 | A9:278-281 | A9:293-296 | Issue-order steps |
| docs/V1-PROFILE.md | 1276 | A9:169-181 | A9:175-187 | Scenario rows / cases |
| docs/V1-PROFILE.md | 1278 | A9:217 | A9:223-225 | Parameters (E14) |
| docs/V1-PROFILE.md | 1282 | A9:137 | A9:143 | verifier fixes the required set |
| docs/V1-PROFILE.md | 1284 | A9:134, 138 | A9:140, 144 | anchor covers frames and exact signatures (C1, C5) |
| docs/V1-PROFILE.md | 1286 | A9:298-326 | A9:351-400 | signers (P-256 only superseded): signer profile through branch registration |
| docs/V1-PROFILE.md | 1286 | A9:217-219 | A9:223-225 | parameters ratified |
| docs/V1-PROFILE.md | 1287 | A9:302-303 | A9:324-325 | signing and reliance periods apart from publication and revocation |
| docs/V1-PROFILE.md | 1292 | A9:405-406 | A9:486-487 | A9.7 rows 22 and 23 |

## Lower-confidence mappings (judgment, not unresolved)

- Line 168, manifest frame and possession signature: A9 has no sentence naming the manifest frame in the profile list; the old A9:311-312 was the pass-condition bullet on "attestation and manifest-possession verification", now 364-366.
- Lines 612/911/173, pin coverage: mapped to A9:156 (HEADERS_NOT_COVERED), where the old number pointed. Line 1149 sits in the dependency-manifest table, whose A9 list entry is at A9:160. Line 1149 (the dependency-manifest table) is A9:159-160, corrected by the owner (FC-01).
- Line 869, the three-conjunct predicate: old A9:99 was the "Earlier owner decisions carried in" paragraph (k = 6, DepthK = k - 1), now 105-106.
- Lines 1144 and 1286, signer profile ranges: mapped to the A9.6 signer text (351-374 and 351-400). The spans grew with the slot-2 custody text.
- Line 1249: C7 row (146) and the "Evidence (C7)" sentence (281-283).
- Lines 87 and 458: the A9.5 root-KSK rule as a whole (309-325).

## Not changed, for the author

Profile §0 now records the completed refresh against the signed A9 and A10 texts (owner, 2026-10-24, FC-01).
