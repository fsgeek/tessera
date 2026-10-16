Full review, repo /home/tony/projects/tessera. Edit nothing except the output file.
Subject: work done 2026-10-13 by a resumed owner session (uncommitted):
(a) docs/V1-PROFILE.md (read in full) against docs/phase-0-prereg-amendment-9.md (governs), formal/p8/ENCODING-V1.md, docs/V1-DERIVATION-DRAFT.md;
(b) step 11: prototype/tessera_proto/real/gitchannel.py (git diff) and prototype/tests/test_gitpath.py;
(c) step 12: prototype/spike/verify_offline.py check_dnssec and related changes (prototype/spike/ is untracked; read SPIKE-REPORT.md for context).
Owner decisions to test adversarially: (1) key file at fixed path tessera-v1/key-assertion, byte-identical to the DNS TXT value, no trailing bytes; (2) issuer domain D pinned in the verifier trust configuration as (D, repository root key), checked against D in signed bytes; (3) root KSK: only-valid-signature-from-trusted-KSK-outside-signing-period => INVALID, signed only by unknown keys or unsigned => UNVERIFIABLE; (4) DNS snapshot without its own timestamp proof => UNVERIFIABLE, no substitute time; (5) KSK-2017 signing period ends 2026-10-11T23:59:59Z.
For each: is it sound, does it contradict A9 or P8, does it create a false accept or an avoidable false reject (especially for a 2106 verifier), and is the INVALID/UNVERIFIABLE split right. Run `uv run pytest -q` in prototype/ and the spike selftest if cheap. Also list any place V1-PROFILE.md states something as decided that A9 leaves open.
Write findings with severity and proposed fix to docs/reviews/v1-profile/CODEX-REVIEW.md.
