# Codex non-author review of the capstone registration, twelfth round (2026-09-17) — ready to freeze, subject to the author's items

Reviewer: OpenAI Codex CLI (`gpt-6-astra`), run non-interactively by the
owner instance on 2026-09-17 (20:53–21:03 UTC) against the whole of
`formal/suite/capstone/PREDICTIONS.md` after the round-eleven repair;
scratch diagnostics under `/tmp/tessera-capstone-r12-4akx1iw4/`. **The
reviewer found no new run-backed defect** and wrote: *"This registration
is ready to freeze from this non-author review, subject to the REFUSAL
ruling, the author's disposition of the four contestable choices, and
the stated pre-freeze review prerequisites."* It also **re-ran all 87
archived diagnostic copies** (`cap5`–`cap24`) under ProVerif 2.05 and
reports every `RESULT` line matching its archive, and it checked all
eleven disposition records against the operative text and found all
thirty-four accepted findings' repairs present. The four control runs it
made were reproduced on our tree
(`formal/suite/ledger-tests-2026-09-14/cap25a`–`cap25d`, sixteenth
batch of that directory's README). No capstone model exists; nothing in
the repository was run.

## Dispositions (owner instance, 2026-09-17)

1. **No finding to disposition.** The reviewer's four control runs
   (C-Q7's and C-Q8's relations observed on C-C15(i)'s strict copies,
   both green, with each observer's negative control red) let two of
   configuration (i)'s *predicted* greens become **descended** greens;
   that is a strengthening, entered in the file as a dated note, not a
   repair.

2. **What the reviewer says the author should see first**, carried
   verbatim as the shape of the freeze read: *"the REFUSAL decision and
   its costs; the four outcome-sensitive contract choices; and the
   remaining distinction between descended relations and
   predictions — especially C-C15(i)'s `Stripped` and link 2b."*

3. **What still stands between this file and the freeze commit**, per
   its own freeze statement (§8): the full non-author pass — **this
   one**; a **full skeptic read** of the file as it now stands — the
   skeptic log is dated 2026-09-15 and predates eleven rounds of repair,
   so a fresh full read is owed and is dispatched by the owner instance
   the same evening; and the routed `REFUSAL` item, answered by the
   author.

**Loop, closed.** Twelve rounds, thirty-four accepted findings, findings
per round 4, 3+1, 2, 2, 6, 2, 2, 3, 2, 1, 0. The composition contract has
drawn no finding since round four; rounds five to eleven were the
per-case bookkeeping the owner introduced in round five and its
consequences. The stopping condition set in the round-one record — the
reviewer says ready, or the remaining findings are things the build
must decide — is met on the first horn.

## Codex review — verbatim

## 1. Query forms and matrix discharge

**No new run-backed defect found.** I found no additional query/consumer mismatch warranting a repair.

I tested the remaining strict C-C15(i) signature predictions on `/tmp` copies of cap24a/b/c, adding signature-term and structural byte-binding observers. Both relations remain green in the baseline and both single-channel-compromise variants; honest witnesses remain reachable. The observers detect their respective negative controls:

- Byte unbinding makes the byte relation red: `/tmp/tessera-capstone-r12-4akx1iw4/sig_bytes_control.out:2249`.
- Both-channel compromise makes signature transplantation red: `/tmp/tessera-capstone-r12-4akx1iw4/sig_transplant_control.out:2505`.
- Single-channel results: `/tmp/tessera-capstone-r12-4akx1iw4/sig_cc15_dns.out:1306`, `:1317`; `sig_cc15_repo.out:1306`, `:1317`.

These are family-copy diagnostics, **not capstone results or discharge**.

Below, **P** denotes `formal/suite/capstone/PREDICTIONS.md`; **D** denotes `formal/suite/ledger-tests-2026-09-14/`.

## 2. Companion outcomes and witnesses

**The round-11 repair is honoured.** C-C15(i)’s `SignerForged` is descended red in strict cases (a)/(b), predicted red in degraded, and no longer justified as a relation over the checked outer tuple. The matched baseline is green, and both strict mutants retain their honest witnesses. (`P:2173`; `P:3411–3436`; `D/cap24a_sp7_strict_base_member.out:1421`; `D/cap24b_sp7_strict_q6b_member.out:3211`; `D/cap24c_sp7_strict_q6b_member_repo.out:3211`.)

`Stripped` and link 2b remain predictions. I do not infer their failure from a membership observer on a family projection lacking the capstone’s retained two-signer logic. (`P:3428–3433`; `P:3501–3504`.)

I found no further demonstrated inconsistency in failed sets, retained guarantees, or witnesses. The operative rule correctly distinguishes individual descended results from untested composition predictions. (`P:1526–1561`.)

## 3. Prediction bases and diagnostic citations

I reran **all 87 cap5–cap24 diagnostic copies** under ProVerif 2.05 with the copied shared library. Every run returned `rc=0`; every `RESULT` line matched its archive. The run summary is `/tmp/tessera-capstone-r12-4akx1iw4/rerun-summary.json:1`.

I checked README batches six through fifteen and the registration’s diagnostic references. **No new citation error or run-contradicted operative prediction found.** In particular:

- C-C7(i)’s honest-filtered and structural C-Q8 references are correctly distinguished. (`P:3215`; `D/cap17b_sp1_strict_cc7i.out:533`, `:709`.)
- C-C8’s strict manifest-hash relation is green despite C-Q9 being red. (`P:3214`; `D/cap22h_sp2_strict_cc8_mh.out:1466`, `:1478`.)
- cap23g/h support **degraded**, wrapper-layer type conclusions; their filenames do not establish strict descent. (`P:2171`; `D/README.md:453–454`.)

This verifies the cited basis, not the calibration of probabilities for the unwritten composition model.

## 4. Builder completeness

**No new construction-blocking omission established.** The contract fixes fresh intake identity, layer-indexed acceptance, strict evidence pairs, presented-layer reports under mutations, and independent standing/envelope processing. It separates immutable join terms from removable verifier checks. (`P:115–162`; `P:176–241`; `P:794–923`.)

The two round-2 choices remain explicit: same-key wrapping and compromised-channel-only enrolment per case. I found no new inconsistency requiring either choice to be reversed. (`P:65–78`.)

## 5. Routed and contestable choices

The **REFUSAL fork remains genuine and unresolved**:

- Exercising an honest REFUSAL signer enables a load-bearing tag test but introduces a symbolic fixture ahead of E6.
- Leaving it unexercised preserves that boundary but leaves the tag property inert.

Both costs and the prohibition on builder selection are explicit. (`P:1801–1822`.)

The four contestable choices are visible: same-key wrapping, compromised-channel-only enrolment, paired strict evidence, and presented-layer reporting under companions. Their alternatives can change outcomes; they are not presented as author rulings. (`P:176–241`; `P:3172–3179`; `P:3434–3436`.) I found no additional hidden consequential fork.

## 6. Earlier accepted findings and ledger corrections

I checked all eleven disposition records against the operative text. **All 34 accepted findings have their required repairs present**, including subsequent corrections to earlier repairs:

| Round | Accepted findings | Repair verification anchors |
|---|---:|---|
| 1 | 6 | `P:2374–2379` |
| 2 | 4 | `P:2439–2442` |
| 3 | 4 | `P:2525–2528` |
| 4 | 2 | `P:2616–2617` |
| 5 | 2 | `P:2709–2710` |
| 6 | 6 | `P:2818–2823` |
| 7 | 2 | `P:2940–2941` |
| 8 | 2 | `P:3076–3077` |
| 9 | 3 | `P:3213–3215` |
| 10 | 2 | `P:3345–3347` |
| 11 | 1 | `P:3460–3461` |

The three ledger corrections also remain operative: C-Q8 asserts verification over exact bytes, not authorship; link 1b is a publication correspondence; acceptance identity cannot be the replayable package term and retains layer separation. (`P:1279–1291`; `P:350–359`; `P:115–162`.)

**This registration is ready to freeze from this non-author review, subject to the REFUSAL ruling, the author’s disposition of the four contestable choices, and the stated pre-freeze review prerequisites (`P:1794–1797`). There are no three new defects to supply. The author should see first: the REFUSAL decision and its costs; the four outcome-sensitive contract choices; and the remaining distinction between descended relations and predictions—especially C-C15(i)’s `Stripped` and link 2b.**

