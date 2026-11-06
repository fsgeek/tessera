# Review brief: the ceremony operator sheet (owner, 2026-11-06)

`docs/ceremony/OPERATOR-SHEET.md` is now what the author types, by hand, on an offline Tails machine (GnuPG 2.4.x
probably; recorded at step 1). It replaces `CEREMONY.md` revision 5 as the operator form; `CEREMONY.md` holds the
reasoning and your earlier reviews (CODEX-REVIEW, CODEX-CONFIRM 1–3). Changes of substance: one backup per key (owner
decision, recorded in CEREMONY.md); LUKS type via `cryptsetup status` on the mapper (luksDump on the mapper failed
in the author's run); the fresh-boot tests merged into one boot (card alone with only the public key imported, then
the backup restore). Read-only except your report. Check every command literally as typed: does each one do what
the sheet says on GnuPG 2.4 and Tails, is any variable unset where used (each boot is a new shell), can any step
lose the only proven copy, and does step 12's card test really use the card (not a local secret key). Severity,
line, concrete failing scenario. Keep it short: findings only. Write docs/reviews/ceremony/CODEX-OPERATOR-SHEET.md.
