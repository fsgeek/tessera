# Disposition: Codex script review (owner, 2026-11-06)

Exit rule (stated to the author before this review returned): after this review, fix HIGH findings and run; no further
review rounds on the ceremony. Cheap, clear MEDIUM fixes are made too; rehearsal run 1 is their test.

| Finding | Disposition |
|---|---|
| HIGH backup retry after `tocard` destroys the export / certifies a stub | Fixed: `backup` refuses when the card holds the key, when `RESTORE_OK` is set, and when `secret.asc` already exists. |
| HIGH `card` reset advice can target this run's key | Fixed: `card` refuses reset advice when the card holds this run's fingerprint. |
| MEDIUM interactive steps print PASS on failure | Partly: slot check reads the signature slot only; PIN policy needs a positive `forced` readback. `pins` still cannot verify that PINs changed (by design: no PIN value is ever read back); the operator sheet's photo and the policy step's PIN prompts are the check. |
| MEDIUM unchecked infrastructure (`save`, `sync`, `sha256sum`, `mktemp`) | Fixed for `save`, `sync`, the public hash and `mktemp`; `generate` refuses if the keyring already holds a key. The `ip` pipeline is left as is (an `ip` failure is visible on screen). |
| MEDIUM touch timeout by substring | Fixed: `LC_ALL=C`; requires `signing failed: Timeout` (GnuPG's mapping of the card's ACK timeout). Run 1 records the actual text. |
| MEDIUM verify: card absent, stub backup | Fixed: the backup test refuses if a card is present and if the imported secret is a card stub; the keyring must be on tmpfs. |
| LOW secret-storage wording | Fixed in the header. |
