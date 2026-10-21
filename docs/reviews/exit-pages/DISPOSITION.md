# Disposition of the Codex review of the exit pages (XP-01 to XP-13)

Review: `docs/reviews/exit-pages/CODEX-REVIEW.md`. Pages: RP = `docs/V1-RELYING-PARTY.md`, P9 = `formal/P9-CONTRACT-INSPECTION.md`, SHEET = `formal/E8-E7-E11-SHEET.md`. Each finding was checked against the registered text it cites before it was applied. No finding was rejected.

| Finding | Severity | Disposition | Where |
|---|---|---|---|
| XP-01 | HIGH | Applied. Two conditions added (authority records named the actual keys; registered signature and git-link assumptions hold). Statements 2, 3, 4 point to them. Honest-receipt protection now says it holds only while service keys stay secret and unmisused (A10:417-430). | RP "What a VALID V1 receipt tells you", "Conditions", "Capture" paragraph; ref R2a |
| XP-02 | HIGH | Applied. Steps now require an independently authenticated production release key, reject TEST keys, and warn about a key that comes with the release. Open item on the unpublished key kept. | RP "Before you check a receipt"; R17 |
| XP-03 | MEDIUM | Applied. Fixture sentence before the table; rows b, d1, d3 reworded to match the fixtures (PROF@8ea8bfa:1055-1069). | RP case table; R21a |
| XP-04 | MEDIUM | Applied. U use limited to a VALID receipt plus A-UTC for the selected block and its five successors; non-valid-verdict warning added. | RP "Real time" |
| XP-05 | MEDIUM | Applied. "Historical security" paragraph tells a later examiner what to supply (A9:259-277). | RP; R28 |
| XP-06 | MEDIUM | Applied. Prose L-05 correspondence added, with no claim of proved composition. | SHEET after E8 table |
| XP-07 | MEDIUM | Applied. Q1d and Q1r row names queries (i), (ii), (iii) and maps C2 and C1; Q1r marked OK (inherited). | SHEET E7 table |
| XP-08 | MEDIUM | Applied as an interim statement (Codex text) in the E11 index. The gap list says it is not the full capstone statement. This statement is owner-written and needs review. | SHEET E11 table and gap list |
| XP-09 | LOW | Applied. Input 6 now says the tables and ES serialization affect acceptance; Result item 2 includes the runtime. | P9 row 6, Result |
| XP-10 | LOW | Applied. F4 now names P9, C6 and A10's no-clock rule as the governing text. | P9 F4 |
| XP-11 | LOW | Applied. E7 intro states that inherited mappings count and TLA+ rows are context. Q1r changed from GAP to OK (inherited). Other GAP rows (S-P2, S-P3, S-P7, first-link Q1) were not changed: Codex did not address them, and the owner should re-check whether they also inherit. | SHEET E7 intro and rows |
| XP-12 | LOW | Applied. Q6 adversary cell filled. | SHEET E11 table |
| XP-13 | LOW | Applied. Two paragraphs explain key, signature, SHA-256, DNS, DNSSEC, git, Bitcoin, OpenTimestamps and frame before first use. | RP before the numbered statements |

## Extra fixes from the top-to-bottom read of RP against V1-CONTRACT.md (sections 2, 3, 4)

1. Statement 6 now says the two window checks do not show that signing happened inside the window (G7).
2. Case a, g now says "under the conditions above" and no longer states "given to the service" alone.
3. CANNOT VERIFY row now covers out-of-profile receipts, and "ask for missing files" applies only if files are missing.
4. Honest-receipt protection now carries the "service keys stay secret" condition (G10, section 4).

## For the owner

- SHEET XP-08 interim capstone statement needs an author or non-author read.
- SHEET E7 GAP rows for S-P2, S-P3, S-P7 and first-link Q1 may also rest on inherited mappings (XP-11 logic). Not checked.
- RP terms paragraphs are new text. The 4 Dec comprehension test is not established by this review.
