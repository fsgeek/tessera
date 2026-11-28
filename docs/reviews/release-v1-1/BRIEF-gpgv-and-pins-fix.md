# Scoped review: the gpgv-free signing session and the unreviewed pins fix (steward, 2026-11-27)

In /home/tony/projects/tessera review only two changes. Read-only; no network. Findings only, with severity,
file:line and a concrete scenario.

1. `git diff 20d5e19 -- docs/ceremony/sign-release.sh` is wrong as a base; use `git diff 408beae 24514f5 --
   docs/ceremony/sign-release.sh docs/V1-RELEASE-PROCEDURE.md docs/ceremony/release-REHEARSAL-SHEET.md
   docs/ceremony/release-v1-1-SHEET.md`. The signing session (offline Tails 7.16, which has `gpg` and `sqv` but no
   `gpgv`) no longer runs `gpgv`. Step 7 now calls `release_tool.rule_o` on the new signature and requires the
   returned issuer fingerprint to equal the signer. Full `gpgv` verification and the changed-byte refusal move to the
   NUC, before `acquire`. Questions: does the session still meet `docs/V1-PROFILE.md` §15.9 R3 ("The signing session
   checks it against rule O before it leaves the session")? Can a signature leave the session, or be published, that
   R3's acceptance would refuse? Did removing steps break anything the script, either sheet or the procedure still
   relies on (step numbers, expected output lines, INPUT contents, `record.txt`)? Is the stated cost honest?
2. `git show 1f9d914 -- service/verifier/release/release_tool.py service/verifier/tests/test_release_tool.py`: the fix
   for the two MEDIUM findings in `docs/reviews/release-v1-1/CODEX-PINS.md`. It was never reviewed after the fix. Do
   the fixes close those findings without opening new ways to publish partial output, drop or alter a pin, or move
   `as_of` backward?

Exit (pre-registered): the steward fixes HIGH and MEDIUM with the smallest change, preferring to remove mechanism;
no further round unless a fix changes the archive. LOW findings are recorded, not fixed before production.
