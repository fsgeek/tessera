# Review brief: the ceremony step-runner script (owner, 2026-11-06)

`docs/ceremony/tessera-ceremony.sh` now performs the ceremony steps on an offline Tails session (GnuPG 2.4.x,
YubiKey 5, OpenPGP 3.4); `docs/ceremony/OPERATOR-SHEET.md` is what the author follows; `CEREMONY.md` holds the
reasoning (see its "Scripted form" note) and your earlier reviews are alongside this brief. Read-only except your
report. The author will read the script before running it, so clarity matters as well as correctness.

Check, citing lines, with severity and a concrete failing scenario:
1. Every step does what its messages say, on GnuPG 2.4 and Tails; `set -u` with no `set -e` is deliberate (each
   check calls `fail` explicitly): find any unchecked command whose failure lets a step print PASS.
2. No path can lose the only proven copy of a key, and no step resets a card that holds the run's key.
3. The script never writes secret material anywhere but the LUKS volume `/media/amnesia/$L-PRIV`, and never writes
   to the public stick anything but `key.pub.asc`, `proof.txt`, `proof.txt.asc`.
4. `step_tests`: does `grep -qi 'time'` on stderr reliably identify a YubiKey touch timeout under GnuPG 2.4
   (what does gpg actually print)? `step_verify`: does the card test use the card and not a local secret key?
5. `gpg --quick-generate-key NAME nistp256 sign never` produces a key whose signatures the V1 verifier accepts
   (the owner checked one on GnuPG 2.4.4 with the verifier's code; confirm from the profile §15.4 requirements).
6. Anything the author, reading it once, could misunderstand.
Write docs/reviews/ceremony/CODEX-SCRIPT.md. Findings only, short.
