**Verdict: not ready for the author’s signature.**

- **A11D-01 — FAIL: stale choice wording remains.** [A11:227–230](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:227) still says “a recommendation, not a decision” and “Until the author rules,” contradicting the new owner decision. Also update “If the author picks Option 1” at [line 17](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:17). No custody-choice blank remains. “Deployment pending” at line 243 describes deployment status and is appropriate.

- **A11D-02 — PASS: disclosure and authority preserved.** The retrospective relaxation, its post-deadline timing and already-written candidate code remain disclosed. The decision block explicitly requires the author’s signature; [DEPLOY step 0](/home/tony/projects/tessera/service/issuer/DEPLOY.md:39) gates deployment on signing. The owner’s decision alone does not amend registered text.

- **A11D-03 — PASS: Option 2 remains accurate.** Its substantive description is unchanged: classical P-256 in both slots, retained slot-2 custody, no hybrid custody deadline, and an amended or rebuilt freeze before issuance. Row 7 identifies it as the alternative not taken.

- **A11D-04 — PASS: no other A11 changes found.** Compared the complete amendment captured in the preceding `codex-confirm-item4.log` with the current file: differences are confined to the named custody edits. DEPLOY’s tracked diff adds only step 0; its previous wording was not available as a complete snapshot for an exact comparison.

No repository files or git state were written.

