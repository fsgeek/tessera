# Codex non-author review of the capstone registration, seventeenth round (2026-09-18) — confirmation of the amendment repairs

Reviewer: OpenAI Codex CLI (`gpt-6-astra`), `codex exec`, run
non-interactively by the owner instance on 2026-09-18 (22:33–22:39 UTC)
against the whole of `formal/suite/capstone/PREDICTIONS.md` after the
round-16 and skeptic-read repairs, with the pre-amendment copy to diff
against. **Three findings, all accepted; five confirmations** (the
ledger refolding; the counts under their supersession clauses; C-Q10's
coverage statement with `cap27g`/`cap27h` re-run, all 28 `RESULT` lines
matching; C-C18's case qualification and projection; preservation of
every dated section). Verdict: *“not yet ready to freeze”* pending the
three; *“neither the ruling nor those choices needs reopening.”*

## Dispositions (owner instance, 2026-09-18)

All clerk dispositions; none touches a query, a probability, a
residual, a timebox, the ruling or the four contestable choices.

1. **The citation sweep over-reached** (finding 1): eleven bare
   references that were ledger, model or output lines had been
   renumbered as if they were this file's own — `:2213-2247`,
   `:2165-2211` (×2), `:198-238` (all `LEDGER.md`), `:244` and `:240`
   (model lines), `:590` (an `.out` line), `:483`/`:744-750`
   (`LEDGER.md`), and six `:243` (the spike's `.out`). ACCEPTED, **all
   reverted to their original numbers**. Two genuine self-references
   had landed short of their passages: the event table's pointer to
   the envelope attribution report now reads `:1146-1151`, and the four
   pointers to C-N1's rule now cite the operative sentence
   (`:1489-1490`) or its qualification (`:1503-1510`) rather than the
   quoted withdrawn reading. C-C15's row, which the sweep had missed,
   now cites `:369-378` and `:91`. The owner instance's classification
   of bare cites was the error; the reviewer's table is the record.
2. **The handoff note's inline ranges were stale** (finding 2).
   ACCEPTED, all ten updated; the note now says rounds sixteen to
   eighteen and twenty-one records.
3. **§7's “opaque to every check” lacked the qualification given to
   §1.1 and §8** (finding 3). ACCEPTED, qualified the same way.
4. **Findings 4–8 — confirmations.** Recorded. Finding 8's
   qualification is right: the sweep's replacements in §9's rows and
   preamble are disclosed edits, not undisclosed ones.

**Round 18**, a confirmation of these three corrections, follows.

## Codex review — verbatim

1. **The citation-renumbering repair introduced errors and is not ready to freeze.** Several references treated as intra-file citations actually name unchanged ledger, model, or output lines.

   | Citation location | Current reference | Verified target |
   |---|---|---|
   | `formal/suite/capstone/PREDICTIONS.md:373` | `:2372-2406` | `formal/suite/LEDGER.md:2213-2247`, the non-event/provenance correction |
   | `formal/suite/capstone/PREDICTIONS.md:476`, `:1384` | `:2324-2370` | `formal/suite/LEDGER.md:2165-2211`, the structural-predicate/authorship distinction |
   | `formal/suite/capstone/PREDICTIONS.md:514` | `:205-245` | `formal/suite/LEDGER.md:198-238`, the single-removal matrix |
   | `formal/suite/capstone/PREDICTIONS.md:559` | `:251` | `formal/suite/ledger-tests-2026-09-14/cap14d_sp7_q1_strict_q6a.pv:244`, the mutated `scopeCh` output; line 251 is `TypeConfused` |
   | `formal/suite/capstone/PREDICTIONS.md:873` | `:597` | `formal/suite/ledger-tests-2026-09-14/cap26b_ss_q1_pairjudge_correct_observers.out:590`, the unreachable key observer; line 597 concerns the agreement witness |
   | `formal/suite/capstone/PREDICTIONS.md:1130` | `:247` | `formal/suite/s-p7/proverif/sp7_q5c_companion_one_level_in.pv:240`, the mutated `scopeCh` output; line 247 is `TypeConfused` |
   | `formal/suite/capstone/PREDICTIONS.md:1334` | `:490`, `:751-757` | `formal/suite/LEDGER.md:483`, `:744-750`, the missing composition consumer |
   | `formal/suite/capstone/PREDICTIONS.md:2469` | Six occurrences of `:250` | `formal/spike/first-link/proverif/q2_broken_dns_compromised.out:243` and `q2_broken_repo_compromised.out:243` |

   **Those six `:250` references are not §1.3 report-contract citations.** They identify the spike’s combined-chain result. Both outputs say `RESULT … is false` at line 243; line 250 says `Derivation:`.

   Two genuine self-reference repairs also need adjustment. `formal/suite/capstone/PREDICTIONS.md:265` points to `:925-930`, which contains the C-C12 discussion and E2, not the envelope attribution report; that report is at `:1146-1151`. The four references to `:1498-1499`—at `:1345`, `:1490`, `:1509`, and `:2468`—land inside the quotation of the **withdrawn unrestricted reading**. Cite the operative rule at `:1489-1490` and its honest-flow qualification at `:1503-1510`.

   The requested `:1906`, `:563-574`, and `:314-318` targets are correct. However, C-C15’s same row still carries unrepaired self-references `:362-371` and `:90`; the corresponding passages are now `:369-378` and the degraded-case row `:91` (`formal/suite/capstone/PREDICTIONS.md:2470`).

2. **The handoff’s new table is accurate, but its inline reading directions remain stale.** These references in `formal/suite/capstone/READ-FREEZE-2026-09-17.md` need correction:

   | Handoff line | Current range | Current registration target |
   |---|---|---|
   | 47 | `1844-1882` | `1955-2001` |
   | 60 | `1958-1981` | `2111-2134` |
   | 63 | `1958` | `2111` |
   | 69 | `1973`; `667` | `2126`; `674` |
   | 81 | `1982` | `2135` |
   | 90 | `1995` | `2148` |
   | 102 | `188-212` | `195-219` |
   | 104 | `213-254` | `220-261` |
   | 110 | `1932-1938` | `2085-2091` |
   | 150 | `1885-1906` | `2004-2027` |

   Actual `wc -w` results confirm every entry in the new table: **383, 224, 1268, 621, 893, 615**, totaling **4004 words** (`formal/suite/capstone/READ-FREEZE-2026-09-17.md:181-188`). The C-C18 range `:2656-2720` also lands correctly. The in-file second recompute correctly gives §5’s `:1884-1921` as **1185 words** (`formal/suite/capstone/PREDICTIONS.md:4199`).

   Expanding the staging block without executing it covers **230 of 231 changed/untracked paths**, excluding exactly `docs/band-1-docket.md`. It currently covers **19 review records**; twenty requires this round’s record to exist (`formal/suite/capstone/READ-FREEZE-2026-09-17.md:158-167`). The statements that round seventeen’s findings are already applied and that reviews approved the current file must reflect this report before the author receives the handoff (`:128-139`).

3. **The “opaque to every check” repair remains incomplete in live §7.** The fixture row and §8 now correctly explain that C-C18 interprets the body as a TLR, never as a refusal record (`formal/suite/capstone/PREDICTIONS.md:82`, `:2061-2066`). But §7 still says the body is “opaque to every check” without qualification (`:1984-1987`). Apply the same qualification there. The refusal-record non-claim remains sound; this does not reopen the ruling.

4. **The ledger refolding itself is confirmed.** `formal/suite/LEDGER.md` has **2281 lines**, matching HEAD; only lines **385 and 1277** differ. The instruction cited as `:1276` begins there, with its ruling note on the following line.

   I checked all **53 explicit live `LEDGER.md:N` occurrences**, covering 34 distinct targets. The requested substantive samples resolve: `formal/suite/LEDGER.md:1294` (C-Q6), `:1315` (`LayerAccepted`), `:1371` (degraded unrestricted red), `:1474-1476` (set re-specification), `:1505-1520` (transcribed companions), `:1555-1559` (REFUSAL prohibition), `:1276-1277` (instruction and ruling), and `:385` (REFUSAL row). Additional checked targets include `:1285`, `:1286`, `:1287`, `:1288`, `:1289`, `:1290`, `:1291`, `:1292`, `:1293`, `:1295`, and `:1425-1447`.

   The remaining ledger-citation failures are the **bare references mistakenly renumbered** in finding 1, not continued ledger displacement.

5. **The count repairs are effective under the explicit supersession clauses.** The live total is **27 entries, 1185 minutes per case, 4740 minutes maximum**, and **eighteen companions** (`formal/suite/capstone/PREDICTIONS.md:1587-1613`, `:1836-1841`). The two repaired entry-count sentences carry their former figures explicitly (`:846`, `:1632`).

   Old figures remain locally—for example at `:1870`—but the clause at `:1603-1609` expressly supersedes such live strays. I found no remaining old total or companion count outside the dated material that escapes those clauses. This confirms supersession, not literal removal of every old numeral.

6. **C-Q10’s coverage statement and reproduced counterexample are confirmed.** I reran `/tmp` copies of cap27g/cap27h using ProVerif 2.05 and a copied library. Both exited successfully; **all 28 `RESULT` lines matched their archives, including line numbers**. After removing their added provenance headers, both sources are byte-identical to the round-16 originals.

   The control excludes foreign-tag envelope acceptance and `TagConfused` (`formal/suite/ledger-tests-2026-09-14/cap27g_ss_q1d_degraded_foreign_tag_envelope_observer.out:1859`, `:1865`). The mutant admits the REFUSAL envelope acceptance while `TagConfused` remains unreachable (`formal/suite/ledger-tests-2026-09-14/cap27h_ss_q1d_degraded_foreign_tag_envelope_bytes_tag_unbound.out:2016`, `:2022`). Its only executable change removes the envelope’s BYTES equality (`cap27h_ss_q1d_degraded_foreign_tag_envelope_bytes_tag_unbound.pv:408-413`).

   The coverage statement accurately assigns the consumers to C-Q10, C-Q8, C-Q9 and link 1a (`formal/suite/capstone/PREDICTIONS.md:1431-1452`). C-Q8’s rejection follows from its registered relation; these diagnostics do **not** claim to execute C-Q8 or the capstone.

7. **C-C18’s case qualification and projection are confirmed.** Set (2) restricts link 1b, C-Q2 and strict unrestricted authorship to (a)/(b), preserving the degraded baseline cost (`formal/suite/capstone/PREDICTIONS.md:2692`). This agrees with C-Q1’s two forms (`:314-318`), C-Q2’s restriction (`:595-597`), and the retained-query table and degraded exclusion (`:1569-1581`). The key mapping and standalone-family versus predicted-join distinction are explicit (`:2674-2688`). The ordinal is also corrected (`:2658-2662`).

8. **Preservation is confirmed, with one qualification to the requested diff criterion.** Lines **1–81 are byte-identical** to the pre-amendment copy. All thirteen dated repair sections are byte-identical (`formal/suite/capstone/PREDICTIONS.md:2721-4036`), as is the first skeptic log (`:2212-2428`). The second skeptic log preserves its prior bytes and adds the dated recompute at `:4199`.

   The literal claim that every removing hunk lies in §§1–8 or the review log is **false**: replacements also occur in §9’s dated preamble and C-C13–C-C15 rows (`:2439-2440`, `:2468-2470`). These correspond to the listed preamble qualification and citation sweep; they are not undisclosed substantive changes. Some sweep replacements are nevertheless wrong, as finding 1 documents.

**This registration is not yet ready to freeze.** First repair the citation sweep, the handoff’s stale inline directions and premature approval statements, and §7’s remaining opacity sentence; then confirm the corrected targets and archive this review. The author should first see these bounded defects alongside the confirmed C-Q10 coverage limit and C-C18 case/projection repairs. Once corrected, readiness remains subject to the four contestable choices and the offered path veto; neither the ruling nor those choices needs reopening in this review.
