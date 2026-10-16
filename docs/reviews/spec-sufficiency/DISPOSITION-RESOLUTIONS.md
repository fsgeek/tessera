# Owner disposition of CODEX-REVIEW-RESOLUTIONS (2026-10-14)

- F01 HIGH: accepted, and strengthened. A9 now requires **chain-order pre-commitment**: git anchor height + 5 < receipt anchor height (BROADEN). A9's summary sentence and C4 say "in chain order", not UTC. The draft's G02 CORRECT text is replaced by Codex's wording. Issuer duty (runbook): wait for the key-assertion stamp to reach k=6 before issuing in a window.
- F02 HIGH: accepted. A9 C6 now names the selected anchor as the referent; Codex's G05 text and its conformance cases are adopted.
- F03 HIGH: accepted. A9 C5 now reads "lowest block height"; T and confirmed_at both come from that attestation; nonmonotone tests added; the "about 2 h" bound removed.
- F04 CRITICAL (conditional): accepted. A9.5 now has "Trust-configuration authority": independent release allowlisting (each verifier release compiles in its config hash), signed by a release key that no authority-channel credential can use, with distribution compromise as a stated boundary. Custody of that key is OPEN, for the author (see the note to Tony): YubiKey 2 is not in hand. A test is required in which a captured repository signer tries to authorize a config.
- F05 HIGH: accepted as proposed (root passes only under A9.5 reliance; explicit DS outcomes; DS type 4 retained; the allowlist recorded as a visible owner scope choice).
- F06 HIGH: accepted as proposed (fixed reporting order; early exit only when every stable field is settled).
- F07–F13 MEDIUM: accepted as proposed. G23: INVALID chosen (a conflicting pinned header is contradictory evidence).
- Change accounting: accepted. §K's blanket "none" is withdrawn. New completion choices are labelled OWNER CHOICE (supported-path limits), not CLARIFY. "No signed byte change" is narrowed to "no attestation-frame layout change".
