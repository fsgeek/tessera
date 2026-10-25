# Disposition: Codex review of `docs/V1-SERVICE-CONTRACT.md` (SC-01 to SC-21)

2026-10-24, Claude Opus 5.5 (owner instance). Review: `CODEX-REVIEW.md` in this directory. Controlling text: A9,
A10, `docs/V1-CONTRACT.md`, with the listing cut by the author's E9 row-2 ruling. Codex's replacement text was used
unless noted, sometimes shortened without changing meaning. No Undecided item was decided. Clause ids whose
meaning changed were retired and replaced; the map is in the contract's "Retired ids" section.

| Finding | Severity | Disposition | Clause ids affected |
|---|---|---|---|
| SC-01 S1.1 size cap is the encoded payload | Medium | Applied | S1.1 retired → S1.9 |
| SC-02 S1.2 transport not atomic | Medium | Applied | S1.2 retired → S1.10; F1.6 reference updated (wording) |
| SC-03 lost response; "not receipted later" was extra | Medium | Applied; the expected refusal reasons kept | S1.4 retired → S1.11 |
| SC-04 §5 overstated A9.1 latency | Medium | Applied: "stated latency", its endpoints, conditions and missed-latency outcome Undecided | S1.3 retired → S1.12; §5 |
| SC-05 A1.2 required unchanged live records | Medium | Applied. Checked: A9.6 "a published window cannot be shortened"; publication is an issuer duty | A1.2 retired → A1.8 |
| SC-06 offline checking needs installed verifier and covering trust data | **High** | Applied, including "installation is not offline" (V1-PROFILE R6, install-time retrieval); qualification carried to S1.15, A1.11, F1.13, F1.14, F1.16 | A1.3 retired → A1.9; S1.8 → S1.15; A1.5 → A1.11; F1.1 → F1.13; F1.2 → F1.14; F1.7 → F1.16 |
| SC-07 release-authority boundary missing | **High** | Applied. Checked: A9.5 trust-configuration authority; A10 TEST-key rejection. Fingerprint sentence retained | A1.4 retired → A1.10 |
| SC-08 digest is not secrecy | Medium | Applied | S1.6 retired → S1.14 |
| SC-09 "from signing" and run timings leak internals | Medium | Applied: run measurements and startup wait removed from the contract | S1.3 retired → S1.12 |
| SC-10 "issuing account" is architecture-specific | Medium | Applied, including F1.6 wording ("A required signature cannot be obtained", same meaning, id kept) | F1.8 retired → F1.17; F1.6 (wording) |
| SC-11 handoff depends on internal material | **High** | Applied in part: Appendix A restates guarantees, conditions, verdicts, time semantics and non-claims from `V1-CONTRACT.md` §2–§3 without implementation detail (no cloud account, no scenario letters other than "two registered honest cases"). **Deferred, not rejected:** assembling a handoff packet with the remaining format and verification requirements is outside this document and this edit | A1.1 retired → A1.7; Appendix A (new) |
| SC-12 no request lifecycle | Medium | Applied as one Undecided list; idempotence now by request identity and by content | S1.5 retired → S1.13 |
| SC-13 window and charging terms | Medium | Applied: window terms into L1.4; charging terms appended to S1.7 as further Undecided items (no promise changed, id kept) | L1.4; S1.7 (extended) |
| SC-14 retention beyond successful delivery | Medium | Applied | S1.14 |
| SC-15 holder acquisition and original-proof guidance | Medium | Applied. Checked: A9.6 relying-party text on `ISSUANCE_WINDOW` from a later proof; V1-CONTRACT §3 on T across proofs | A1.12 (new) |
| SC-16 90-day limit read as service lifetime | Medium | Applied | L1.1 retired → L1.4; F1.7 → F1.16; §5 |
| SC-17 slow chain need not end in delivery | Medium | Applied | F1.3 retired → F1.15 |
| SC-18 "nothing visible" vs. no detection guarantee | Medium | Applied; table preamble states no row guarantees detection; known-capture notice stays Undecided | A1.6 retired → A1.13; F1.8 → F1.17; F1.9 → F1.18; F1.10 → F1.19 |
| SC-19 "honest receipts stay protected" unconditional | **High** | Applied: F1.18 cites G10 under its conditions (Appendix A states them: keys secret and unmisused, release boundary intact); table-wide "keeps every assumption it does not relax"; "Every receipt already issued" replaced by "Preserved receipts" (defined) | F1.9 retired → F1.18; F1.1, F1.2, F1.7 retired (above) |
| SC-20 "only holders who installed no later release" | Medium | Applied | F1.10 retired → F1.19 |
| SC-21 clock faults anywhere in window | Medium | Applied. Checked: A9 declared-time check, ε = 24 h (A9.2) | F1.12 retired → F1.20 |

**Counts.** 21 findings (4 High, 17 Medium): 20 applied, 1 applied in part (SC-11, packet assembly deferred), 0
rejected. Unchanged ids: S1.7 (extended), L1.2, L1.3, F1.4, F1.5, F1.6 (wording), F1.11 (reference only).

**Absolute-word check.** Remaining "never", "always", "stay(s)" and "promise(s)" were checked against the
registered text: id policy (header); "receipts stay checkable as in A1.9" (conditional on A1.9); "never changes the
verdict" for U (V1-CONTRACT G6, A10.1.1); "keys stay secret and unmisused" (condition of G10, A10.4); the rest are
headings or Undecided questions. The unconditional "never a partial receipt", "never affects receipts already
delivered", "Refused content is not receipted later" and "Only holders ... are unaffected" were removed.

**Length.** Original 89 lines / 1,086 words; revised 146 lines / about 1,840 words (1.7x). Without Appendix A
(required by SC-11) the body is about 1.4x.
