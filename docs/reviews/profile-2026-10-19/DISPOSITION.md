# Disposition: Codex profile review 2026-10-19 (PR-01 to PR-13)

**Status: OWNER-DISPOSED 2026-10-19** (owner instance, Claude Opus 5.5). Review: `CODEX-REVIEW.md` (2 HIGH, 7 MEDIUM,
4 LOW). Every finding was checked against the registered text it cites (A9 at `2ad3489`, A10 at `9ade764`,
`formal/p8/HYBRID-SUPPLEMENT.md`). All 13 are accepted. None was rejected. Edits are tagged `[OWNER 2026-10-19,
PR-nn]` in place, with dated "Was:" text. No registered file was edited (A9, A10, the supplement and the registration
record are unchanged in `git status`).

Files edited: `docs/V1-PROFILE.md`, `formal/p8/PROOF.md` (CHANGELOG entry added), `formal/p8/ENCODING-V1.md`
(CHANGELOG entry added), `docs/V1-RELYING-PARTY.md` (PR-01 sweep only).

## Findings

| ID | Sev | Disposition | Where applied |
|---|---|---|---|
| PR-01 | HIGH | ACCEPT, NARROW-CLAIM. A10:244-249 and rows 5–9 (A10:737+) confirm it. Codex's text applied; sweep below | Profile §11 rows a/g, i; PROOF (iv)(d); ENC §5, §7.1; RP row i |
| PR-02 | HIGH | ACCEPT. A10:631 requires approval bound to the exact archive. The R1/R2 fixed point is real | Profile §15.9 R1 |
| PR-03 | MEDIUM | ACCEPT. A10:300-302. Codex's text applied. The independent verifier already emits the wrapper with a null bound for D1–D4 (`verify.py:162-166`, `test_utc_assessment.test_dispatch_terminal`) | Profile §3.4, §7.4 null rule, §13 note 14 |
| PR-04 | MEDIUM | ACCEPT. Rule O (ENC §5.2) rejects new-format headers and multiple packets; `gpgv` does not. Codex's text applied, joined with PR-05's "currently authenticated key" | Profile §15.9 R3 "Acceptance" |
| PR-05 | MEDIUM | ACCEPT. A9:326-332 and A10:624. Codex's text applied to §5, R3 and R5 | Profile §5 bootstrap bullet; R3; R5 |
| PR-06 | MEDIUM | ACCEPT. HYBRID-SUPPLEMENT §9 item 6 (:525) directs deletion of both spike keys; A9.6 (:375) needs the custody choice in the profile, which stays. Codex's text applied | Profile §8 slot-2 custody record |
| PR-07 | MEDIUM | ACCEPT. A9:290 commits receipt signatures, not possession signatures (profile §9, mutation class A2); unsupported algs are unperformable (EA-31). Codex's text applied | Profile §13 note 13 |
| PR-08 | MEDIUM | ACCEPT. Chose the "parts" option: signed A10 bytes and current PROOF.md become spec-object parts; the current proof hash is recorded in the freeze record beside the supplement's baseline `06910a5f…`, outside every part | Profile §15.8 new bullet; §14.2 item 7 |
| PR-09 | MEDIUM | ACCEPT. A10:237 (T is header time, not UTC) and the witness rule (§7.3). Codex's text applied | Profile §5 "2026-10-11 switch" |
| PR-10 | LOW | ACCEPT. `gen_manifest.py:220` says IEEE 754 was not fetched. Codex's text applied | Profile §15.6 |
| PR-11 | LOW | ACCEPT. A10:635-639. Section renamed; item 1 split into frozen contents and pre-release execution; the 2026-10-14 item text kept below the split | Profile §14.2 heading, intro, item 1 |
| PR-12 | LOW | ACCEPT, all four. A9 status from `HYBRID-REGISTRATION-RECORD.md:3`; ENC:177-180 and D-1 confirmed corrected; manifest built (`formal/dependency-sources/`); 2.4.4 pin marked provisional | Profile status, §0 table, §13 note 6, §9, §15.9 R3 |
| PR-13 | LOW | ACCEPT. Connective error confirmed (huge negative exponents round to finite zero). Codex's text applied; a justification, not a claim | PROOF §5 repair paragraph |

## PR-01: every occurrence examined

Changed:
1. `docs/V1-PROFILE.md` §11 row a, g: "presented to Tessera by T" → before the selected block was mined; T not a UTC
   upper bound (A10 row 5).
2. `docs/V1-PROFILE.md` §11 row i: "existed by T" → same form (A10 row 6).
3. `formal/p8/PROOF.md` (iv)(d): "existed by time T", "existed by T", "first produced after T", "produced honestly
   before T" → relations to mining of the selected inclusion block (A10 rows 7–9); UTC is separate and conditional
   on A-UTC, and P8 makes no UTC statement. Narrower, not wider.
4. `formal/p8/ENCODING-V1.md` §5: "a new, later time bound" → a new anchor in a block mined later; header time need
   not be later. (Outside the literal search terms; same defect.)
5. `formal/p8/ENCODING-V1.md` §7.1 rationale: "the anchor prevents claiming an earlier T" → an earlier block; a later
   block's header time can be earlier. (Outside the literal search terms; same defect.)
6. `docs/V1-RELYING-PARTY.md` row i: "existed by T" → before the block whose chain time is T; T is not a real-time
   bound.

Checked and left (not UTC claims): RP row a/g ("no later than chain time T", A10 row 3's form); RP items 5–6 and the
"T is a chain time" paragraph; `V1-CONTRACT.md` G5–G7 and :47 (already correct); ENC §7.1 "verified T is after the
window … in chain time"; ENC §5 "inherit an old time bound"; profile §7.3 "not at T of the receipt" and §7.4's
conditional U claim; PROOF §4 "a stamp's time bound makes signing honest" (a non-claim).

## PR-02: instrument check (listed, not edited)

No instrument builds the R1 archive, writes `RELEASE.json` or reads `source_commit`, so nothing is contradicted by
the fix. `prototype/e2e/driver.py` `st_release` and `prototype/indep-verifier/release_auth.py` use the withdrawn
`tessera-v1-test-release/1` record, which §15.9 R3 keeps only as the §3.5 instrument interface; that divergence and
the `--production` flag were already in §15.9's "Instrument work" list. Added to that list (not frozen text): the
assembler must generate `RELEASE.json` (PR-02); an acquisition-side rule-O checker and successor-lineage handling
are new (PR-04, PR-05); `prototype/e2e/freeze.py` `SPEC_PATHS` lacks A10 and `PROOF.md` (PR-08). The e2e TEST spec
hash will change on its next run because the profile, ENC and PROOF bytes changed; that is a TEST object.

## Verification after the edits

- `formal/p8/vectors/check.py`: B 71/71, 173/173, 5/5 baseline; 35/35, 63/63, 1/1, 6/6 hybrid.
- `formal/p8/vectors/test_check.py`: 6 tests OK (3 skipped).
- `prototype/indep-verifier`: `.venv/bin/python -m unittest discover -s tests`, 112 tests OK (1 skipped).
- No code reads the changed sentences. Code that names these files cites them in comments or TEST stand-in text
  (`prototype/conformance/universe.py`), or hashes their bytes into a TEST spec object (`prototype/e2e/freeze.py`).
