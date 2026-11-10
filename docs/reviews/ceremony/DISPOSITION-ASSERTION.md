# Disposition: Codex key-assertion review (owner, 2026-11-10)

| Finding | Disposition |
|---|---|
| CA-01 HIGH: raw payload reaches the terminal before validation; escape sequences can show B while signing A | Fixed: `sign-assertion.sh` checks the whole payload first (printable ASCII and LF only, < 1 KiB, exact 8-line structure, exact identities and message, value grammar, 255 bytes) and then prints only the parsed fields. Tested: Codex's escape-sequence payload is refused before display. |
| CA-02 MEDIUM: assembly accepts any key as "the root" | Fixed: `key_assertion.py assemble` pins `ROOT_FPR = 6BDA…D30A`. Tested: a non-root key is refused. |
| CA-03 MEDIUM: no SHA-1DC check | Fixed: assembly configures the verifier's pinned detector from `service/verifier/install.json` and scans the commit, both trees and the blob. Tested with a temporary test-key pin: PASS. |
| CA-04 MEDIUM: fingerprints are requester assertions; not disclosed | Fixed by disclosure: the sheet and the signing prompt say the signature authorizes the keys for the window and does not prove who holds them; fingerprints shown and compared in full. No independent basis exists in V1; recorded as a limit. |
