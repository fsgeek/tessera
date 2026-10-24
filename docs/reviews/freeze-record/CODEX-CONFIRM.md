The record is ready to sign. FR-01–FR-06 are resolved; I found no new overclaim in the opening’s permissions or non-claims.

| Prior finding | Resolution in FREEZE-RECORD.md |
|---|---|
| FR-01 | Signed amendment commits and completed locator refresh identified, lines 3–12. |
| FR-02 | Hybrid specification hash, ENCODING hash reference, registered baseline and change accounting reconciled, lines 25–29. |
| FR-03 | E10 extraction, P3 assumptions, bounded refusal and P9 execution evidence restored, lines 80–83. |
| FR-04 | E18-02 remains explicitly open and non-blocking; owner deferral supersedes the packet instruction, lines 31–34. |
| FR-05 | R23’s corrected signature-binding interpretation included, lines 52–53. |
| FR-06 | Instrument outputs may select registered branches but supply no C-row evidence or discharge, lines 73–74. |

I checked ten A9 citation sites in the frozen profile: lines **87, 146, 168, 173, 458, 869, 1144, 1149, 1249 and 1286**, covering every lower-confidence mapping category. I also checked A10 references at **979 and 1000**. The targets support their respective uses. At line 869, A9 supplies the `k`/`DepthK` convention; the adjacent SPEC references supply the three conjuncts. A9 and A10 are byte-identical to their respective signing-commit versions.

Independent byte verification passed:

- All five object sizes and SHA-256 hashes match the Markdown record, `objects/` and JSON.
- All **393 inventory entries** match their recorded blob IDs, sizes and hashes at the named commit.
- JSON names exactly `270ca49bc1384a1ec716b6312f381b2230bb5277`.
- The historical ENCODING baseline hash matches its registered-version bytes.
- In a temporary detached worktree, `assemble.py --repo <worktree> --check <repository>/formal/freeze-v1` returned **agreement OK**. Fresh assembly reproduced all five objects and JSON byte for byte. The worktree was removed.
- Vector checks passed: baseline **71/71, 173/173, 5/5**; hybrid **35/35, 63/63, 1/1**, plus **6/6** demonstrations.

**FC-01 — Low, non-blocking — Locator log contains stale descriptions.**  
[LOCATORS.md:114](/home/tony/projects/tessera/docs/reviews/freeze-record/LOCATORS.md:114) and line 145 describe profile line 1149 as targeting A9:156. The frozen profile correctly uses **A9:159–160**. Line 153 also says the profile’s approximate-locator notice was left untouched, although §0 now records the refresh.

**Replacement:** Update the line-1149 mapping to `A9:159-160`, distinguish that dependency-manifest citation from the pin-coverage citations, and replace the final note with: “Profile §0 now records the completed refresh against the signed A9 and A10 texts.”

This log correction does not require changing the frozen objects or delaying signature. No repository files were edited. Formal models and the recorded dry run were not rerun.

READY TO SIGN: YES


