# Scoped review: the pins subcommand and candidate 4 (steward, 2026-11-24)

In /home/tony/projects/tessera review only the `pins` subcommand added to `service/verifier/release/release_tool.py`
(commit cb474356), its tests, and the trust-file change in `service/verifier/release/v1-1/trust.json`, against
`docs/V1-PROFILE.md` header pins and release invariants (pins unique per height, existing pins immutable, nothing
removed, as_of nondecreasing). Read-only except your report; no network. With severity, file:line, scenario: can it
write a pin that differs from the chain both explorers agree on, alter or drop an existing pin, set an as_of the
profile forbids, or write partial output on failure? Is the steward's as_of rule (newest pinned header time) stated
honestly as an owner choice? Exit (pre-registered): the steward fixes HIGH/MEDIUM with the smallest change before
Wednesday's refresh; no further round. Write docs/reviews/release-v1-1/CODEX-PINS.md. Findings only.

