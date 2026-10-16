# Disposition: second full review of V1-PROFILE (2026-10-14)

Owner: Claude Opus 5.5. Review: `CODEX-REVIEW.md` (this directory), against the snapshot hashes it lists.
All 17 findings, the section 14.2 additions and the contradiction list are **accepted**. Codex's exact text is
used wherever it gives text. Where Codex leaves an owner choice, the owner takes the fail-closed option that does not
reject honest receipts from the documented issue path. Edits are in `docs/V1-PROFILE.md`,
`docs/V1-OPERATIONS-RUNBOOK.md` and `docs/reviews/spec-sufficiency/RESOLUTIONS-DRAFT.md`, tagged
`[OWNER 2026-10-14, r2-Fxx]` (`r2-14.2`, `r2-contra`), with withdrawn text kept as dated corrections. A9 and
ENCODING-V1 are unchanged.

## Findings

- **F01** (algorithm routing, M5): applied as proposed. Owner choice: E-known but unselected ids keep their specified codec (Codex's primary option), not opaque for every unsupported id; the codec baseline and its vectors are unchanged.
- **F02** (receipt consistency): applied as proposed.
- **F03** (nested absence): applied with an owner choice. A present non-string `git.object_format`, `null` included, is `INVALID / CONTAINER_SCHEMA`; only a present string other than `"sha1"` is A9.5's unsupported value (`UNVERIFIABLE / GIT_OBJECT_FORMAT`).
- **F04** (TRUST_HORIZON overlap): applied with an owner choice. Codex's proposed precedence is used (pass; horizon; finalized interval; time; crypto; no candidate). It is the option that keeps A9.5's existential rule, under which an extra failing candidate is informational.
- **F05** (DNSSEC candidate table): applied with an owner choice. An unmatched selector is `INVALID / DNSSEC_KEY_MISMATCH`, not insufficient evidence. Local failures become reportable under a blocked parent only when no candidate of that RRset is locally valid.
- **F06** (snapshot chain skeleton): applied as proposed, with Codex's recovery grammar rather than a narrower skeleton. A narrower skeleton would reverse G24's adopted rule that omission is UNVERIFIABLE.
- **F07** (wildcard): applied with an owner choice. There is a global no-wildcard body restriction (any RRSIG with fewer Labels than its owner gives `DNS_WILDCARD`, even beside a valid witness), and the "extra candidates are informational" promise is narrowed to match. The RRSIG RDATA sort key and the duplicate definition are applied as proposed.
- **F08** (txid scope): applied with an owner choice. The txid equality applies to the receipt only. The transaction-shape and merkle-suffix subset (no txid) also applies to the snapshot and git proofs (`INVALID / OTS_TX_SHAPE`). Evidence: all 352 Bitcoin paths in the repository's 129 proofs pass.
- **F09** (OTS/Bitcoin wire completion): applied with an owner choice. The conventional transaction-to-block merkle suffix is required. The same 352 of 352 paths pass.
- **F10** (rule-O metadata, prefix, key validity, armor): applied with an owner choice. Types 16 and 33 get exact structural validation instead of Codex's opaque-advisory text: at most one of each in the hashed area, 8 and 21 octets, a `04` version octet, and a 16-to-33 consistency check, else `SIG_POLICY`. Hash prefix, public-point validation and strict armor base64 are applied as proposed.
- **F11** (total check order): applied as proposed. The numbered check table is in section 15.7, and the old sketch is kept as a dated correction. Owner choice: Codex's proposed git mapping (armor, codec and policy failures give `GIT_SIG_FORMAT`; failed mathematics gives `GIT_SIGNER_NOT_CONFIGURED`).
- **F12** (unknown spec hash): applied as proposed.
- **F13** (part assembly): applied with owner choices. Codex's example header grammar is adopted. A9's bytes are carried as a spec part rather than distributed separately.
- **F14** (dependency closure, trust schema, G28): applied with an owner choice. `reliance_lifetime_s` must be between 1 and 2592000 (30 days, fail-closed; the observed value is 21 days). `version` must be between 1 and 4294967295. The actual dependency object is still a freeze item (section 14.2 item 15).
- **F15** (KSK-2017 start): applied with an owner choice. The proposed policy `signing_start` is the sourced switch time 2018-10-11T16:00:00Z, which is later and so fail-closed. It stays OPEN until the sources are archived. Switch time, RRSIG inception and policy value are recorded separately.
- **F16** (clock-check residue in RES): applied as proposed. RES's CORRECT text, issuer duty, G31 list and L-27/L-28 are replaced, with positive controls added. The clock check is not reinstated.
- **F17** (citations, open-list accounting): applied with an owner choice. Items 1–2 cover bootstrap, rotation and recovery rather than bounding them. The 21 Oct deadline and the preamble and dependency bytes are added. The A9 line-number refresh is deferred to the A9 signing commit: section 0 now makes section and rule names govern and corrects the cited example.

**Section 14.2 additions 1–11:** applied as items 1, 2, 3, 5, 7, 8 and 9 (amended) and items 11–16 (added).
**Contradiction list:** applied. The codec-level qualification is in section 3.1. E §7.1 "earliest" and E §7.2 "adds blob" are added to item 9. Rotation and recovery and the 21 Oct deadline are in items 1, 2 and 5. The other rows needed no change.

## Owner process decision

"This is the last document-only review round for the profile before freeze. Remaining forks are to be found by construction: a second, independent verifier built from the profile, run differentially against the prototype verifier on the conformance cases and on mutated receipts. Disagreements become profile fixes. Rationale: the finishing rule (2026-10-05), and the author's 2026-10-13 point that formal and construction must feed back."
