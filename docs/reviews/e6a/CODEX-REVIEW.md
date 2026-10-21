The registered E6a obligation survived this review, with one documentation gap.

- **E6A-01 — LOW — inaccurate conformance-to-model mapping.** [RESULTS.md:126](/home/tony/projects/tessera/formal/tla/E6a/RESULTS.md:126) places `ALG-03` under “absent signature,” but [cases-index.json:410](/home/tony/projects/tessera/prototype/conformance/cases-index.json:410) specifies a **nonempty, 65,537-byte signature**, rejected with `LENGTH_CAP`. Likewise, [RESULTS.md:128](/home/tony/projects/tessera/formal/tla/E6a/RESULTS.md:128) associates `HY-N4` with malformed algorithm identifiers; [cases-index.json:2623](/home/tony/projects/tessera/prototype/conformance/cases-index.json:2623) specifies a **truncated signature**, rejected with `SIG_FORMAT`. The verdict/code pairs agree, but these case-to-state links overstate codec coverage: the model distinguishes absent signatures from semantic verification failures, without a separate signature-codec defect class. **Closes with:** correct those mappings and explicitly mark these codec cases outside the abstraction, or add the corresponding input class and checks.

The substantive checks held:

- **Registration and companions:** unknown, well-formed, correctly bound algorithms give `UNVERIFIABLE` when no independent failure exists; definite failure takes precedence; unknown algorithms never yield a valid verdict. FailOpen goes red. The mixed failed/unperformable and missing-signature versus missing-evidence companions named by the derivation are present and effective.
- **Invariant strength:** the raw-input `Exact*` properties constrain both acceptance and rejection. Two additional wrong variants under `/tmp` went red: copying kms classifications into gpg violated `MixedFailedMissingEvidenceInvalid`; rejecting an opaque unknown-algorithm signature violated `UnknownAlgGivesUnverifiable`.
- **Reproduction:** the unchanged harness, run from a temporary copy using `~/.local/lib/tla2tools.jar`, TLC **2026.07.31.184830**, reproduced **all 495 summary rows exactly**, including results, violated invariants and recorded state counts. Both correct models passed all 32 invariants over **7,938 / 15,876 distinct states**. All seven companions’ exact red sets reproduced in both instances.
- **P4:** its bytes match `HEAD`, SHA-256 `899ebd01…a609`; all five regression runs reproduced. No other reason-code mismatch was found in the cited cases.

These remain bounded classification results for two slots and two evidence members. They establish neither byte-level conformance nor adoption/discharge.

[Verification evidence](/tmp/e6a-review.pHBhmY/verification.json) · [Rerun summary](/tmp/e6a-review.pHBhmY/tla/E6a/runs/SUMMARY.tsv). No repository files were edited; all reviewed input hashes remained unchanged.

VERDICT: SURVIVED WITH GAPS (E6A-01: codec-case mapping).

