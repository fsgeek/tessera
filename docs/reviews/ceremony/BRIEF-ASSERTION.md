# Review brief: key-assertion signing (owner, 2026-11-10)

Files: `service/issuer/tools/key_assertion.py` (NUC: builds the 255-byte value, blob, trees and the unsigned git
commit; later inserts the detached signature as `gpgsig` and checks with the verifier's code) and
`docs/ceremony/sign-assertion.sh` (Tails, offline: shows the commit, recomputes the tree from the value in the
message, signs with YubiKey A, root fingerprint 6BDA21559F18D5DB8E1312C363210B5FF92AD30A). Operator sheet:
`docs/ceremony/ASSERTION-SHEET.md`. Requirements: `docs/V1-PROFILE.md` §6.3 and §15.4 (git evidence grammar,
path, rule-O signature, SHA-1DC ids), ENCODING-V1 §7 (value), `service/issuer/tessera_issue/window.py` (what the
issuer later loads), `docs/V1-OPERATIONS-RUNBOOK.md` §5 (k = 6 chain-order pre-commitment). The owner ran a software-
key end to end: build, recompute MATCH, tampered tree refused, assemble PASS, `git fsck` clean.

Read-only except your report. Findings only, with severity, line and a concrete failing scenario:
1. Does the assembled commit satisfy §15.4 exactly (header order and set, gpgsig armor grammar incl. CRC line,
   message bytes, trailing newline, ids), and will `window.py` accept the evidence as built?
2. Does the Tails script's recomputation actually bind what the author reads (the value in the message) to what the
   root signs (the tree)? Any way a payload can show one value and sign a tree for another, or show text the
   terminal renders misleadingly (control characters, CR, long lines)?
3. Anything in the author/committer identity, timestamp or message that the profile or verifier rejects.
4. The requester problem: the service-key fingerprints come from the NUC. State plainly what the root's signature
   does and does not establish, and whether the procedure says so.
Write docs/reviews/ceremony/CODEX-ASSERTION.md.
