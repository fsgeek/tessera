# Capstone — results

**STATUS: PROPOSED — 2026-09-19; ASSEMBLED FOR LADDER 3, 2026-10-06 — produced by the AI collaborator (Claude Opus 5, builder, 2026-09-19; Claude Opus 5.5, builder, the 2026-10-01 and 2026-10-06 assemblies; directed by the owner instance); not adopted; the commit is the author's.** Predictions frozen at `3568905` (PREDICTIONS.md; amended and confirmed through `32d0581`). Model: `formal/suite/capstone/proverif/capstone.pv`, blob `35d8c7020adc31f714d31b12c34a8eaf68010c9b` (ladder 3: ladder 2's model plus BF-5 and BF-6). *(Dated note 2026-10-06: the ladder-2 assembly of this file, with the skeptic repairs S-1 to S-12, is archived verbatim at `proverif/ladder2/RESULTS-ladder2.md`. Text that ladder 3 superseded was moved there rather than kept inline; where a passage below was cut, a pointer names the archive.)*

**AUTHOR, 2026-10-07: the first and third routed questions are DEFERRED; the second is ruled (P), and the clerical items are accepted.** The capstone stays open
while the throwaway prototype (`prototype/`) is used to find what the model may be missing; results and the
slicing method are preserved (`READ-CAPSTONE-2026-10-06.md`, header).

**WHERE THE LADDER STANDS (2026-10-06).** Ladder 3 is complete (`ladder.log:96`). **69 of 80 files landed** (`rc=0`), the same 69 that landed in ladder 2, and every one reproduces its ladder-2 `RESULT` lines byte for byte: **no verdict moved under BF-5, BF-6 or BF-7** (*Cross-check*). The other **11** are the ladder-2 degraded mechanism failures. They are **not run under this blob** (the owner instance's disposition), and their ladder-2 failures are cited only as history. **Every strict file — cases (a), (b) and (c) — landed.** Every correct-form query landed as registered (section 1), and both standing witnesses are reachable at a wrapped layer, `L1`, in every landed file (BF-6). Of 77 companion configuration files, **56 are as registered, 10 are divergent (listed in section 2a, not resolved), and 11 are not run under this blob**. Three questions are **ROUTED TO THE AUTHOR**: the disposal of the eleven (*The degraded wave*), which companion-box reading governs, and, new with ladder 3, which key C-Q6's `kX` is under C-C15(i). C-C15(i)'s C-Q6 results are **withheld from discharge** until he rules on the third. The whole-ladder ceiling is **exceeded 6.46 times** over the three ladders (*Not run, and the ceiling*).

**Tooling.** ProVerif 2.05 (`proverif -lib formal/suite/lib/tessera_theory.pvl <file>.pv`), run from
`formal/suite/capstone/proverif/` with `-lib ../../lib/tessera_theory.pvl`. Every run is recorded in
`formal/suite/capstone/proverif/ladder.log` with its exit code, its seconds, its box and the git blob
hash of the `.pv` it ran. **`capstone.pv` HAS CHANGED THREE TIMES, and this is the record of it** (the author's
clarification at §8 item 2: the model is identified by its **contents**, and a model at the registered
path with a different hash is a different model).

| Blob | When | Results standing under it |
|---|---|---|
| `508b901808dc75dab3e86c2385dd8545af4cad0f` | the first build, 2026-09-19 | **NONE.** Three runs completed under it — `capstone` (193 s), `capstone_b` (194 s) and `capstone_d` (1247 s) — and **all three are discarded**, because the degraded run exposed a transcription defect against §1.3's front-end contract (**BF-3** below). Their `.out` files were deleted and their `ladder.log` lines removed. *(REPAIR 2026-10-01, skeptic S-12: the defective (d) model has been rebuilt and run once as scratch, `dev/bf3_rebuild/`; see BF-3.)* |
| `c6969b4cc2f2e30be7a7a950af7609ea75e4c700` | after the BF-3 repair, 2026-09-19. **Ladder 1**: wam-nuc from 2026-09-19T18:33:57Z, then ubuntu24 from 2026-09-20T19:11:23Z (`ladder1/ladder.log:13`, `:68`). Main runner stopped 2026-09-24T15:06:25Z (`owner_interventions.log:10`); its last two runs logged `rc=124` afterwards (`ladder1/ladder.log:107-108`). | **Ladder 1, ARCHIVED as history under `proverif/ladder1/`.** 49 files landed under it (`rc=0`). Every one was re-run under ladder 2 and reproduces its `RESULT` lines byte for byte (*Cross-check*). Ladder-1 outcomes are cited only as that cross-check and as mechanism-failure history. **No cell in sections 1-3 is filled from them.** *(Until 2026-10-01 this cell read “**every result in this file.**”)* |
| `a9fb7da1e4851120677b21dea4a8c98a481ad43a` | **RECUT R-9, 2026-09-24** (the owner instance's decision): `capstone.pv` plus a dated comment block and `set selFun = Term.`; nothing else changes (`diff`: one hunk, 34 lines added, none removed). **Ladder 2**, ubuntu24, launched 2026-09-24T17:15:52Z (`ladder2/ladder.log:1`), `DONE` 2026-10-01 (`ladder2/ladder.log:99`). | **Ladder 2, ARCHIVED as history under `proverif/ladder2/`** (with its README). Every file that landed under it was re-run under ladder 3 and reproduces its `RESULT` lines byte for byte (*Cross-check*). Its eleven degraded mechanism failures are cited only as history. **No cell in sections 1-3 is filled from it.** |
| `35d8c7020adc31f714d31b12c34a8eaf68010c9b` | **REPAIRS BF-5 and BF-6, 2026-10-01.** The owner instance accepted cross-family review findings 2 and 4 as defects of `capstone.pv`. The blob is `capstone.pv` (`a9fb7da1…`) plus three things. (1) A 23-line dated comment block after `set selFun = Term.`. The R-9 block and its setting are kept unchanged. (2) BF-5: a structural innermost-layer selection at the head of `StandingPath`, with its dated comment. (3) BF-6: the `lyr <> L0` guards on the two standing witnesses' emissions, with their dated comments. `diff`: 53 lines added, 2 changed, none removed. C-C7(i)'s files also carry BF-7 (`derive.py`). **Ladder 3**, ubuntu24, launched 2026-10-01T17:59:41Z (`ladder.log:1`), resumed after a host crash 2026-10-04T18:08:12Z (`ladder.log:47`), `DONE` (`ladder.log:96`). | **every result in sections 1-3.** The eleven ladder-2 degraded mechanism failures are **not run under this blob** (the owner instance's disposition). Their cells read *not run under this blob*, and they cite the ladder-2 failure as history, never as a ladder-3 result. |

Each derived file's own blob is recorded on its `ladder.log` line, so every companion result names the
exact text it ran against. The development run kept at `proverif/dev/first.out` was made under the
first blob and is not a result; it is retained only because its `RESULT` lines documented the model's
first clean pass.

Under §8 item 2's clarification the model is identified by its contents, so `35d8c702…` is a **different
model** from `a9fb7da1…`, and every result names its blob. Every derived file changed blob by the same
hunks (C-C7(i)'s also by BF-7); the per-file table is `proverif/ladder3-staging/DERIVATION-CHECK-L3.md`.
Every ladder-3 `rc=0` line's `blob=` was re-checked on 2026-10-06 against `git hash-object` of the `.pv`
beside it: 69 of 69 match (the eleven `NOT-RUN` lines carry no blob).

**How to regenerate this file.** Sections 1, 2, 2a and 3, the cross-check table, the eleven's ladder-2
partial lines and the run list are regenerated by `python3 proverif/dev/assemble_l3.py`, which reads ladder
3's `.out` files and `ladder.log` for every cell, ladder 2's only for the cross-check and the eleven's
history, and ladder 1's only for the ceiling. It also writes `proverif/dev/l3/` (the cross-check per file,
the ladder-2 → ladder-3 `RESULT` line map, and each landed run's standing-witness trace layer).
`dev/assemble_l2.py` made the ladder-2 assembly and is kept unedited.

---

## 0. What was built, and how the other files are derived

`capstone.pv` is **the** composed model, in case **(a)** — strict, DNS channel compromised. It carries
the §1.1 fixture, the §1.2 acceptance path per layer, the §1.3 events, and **every** registered query
of that case in one file. The other cases and every companion are **derived from it** by
`formal/suite/capstone/proverif/derive.py`, which applies named, exact-string edits inside named
blocks of the model and writes a header into each generated file naming its case, what it mutates,
which registered prediction it serves and the registered box. Nothing in `derive.py` edits
`capstone.pv`. The delta for any generated file is therefore readable twice: in `derive.py`'s rule
list, and as `diff capstone.pv <file>`.

- **(a)** strict, `skD` public — `capstone.pv` itself (no copy: the file the registration names is the
  file that runs, so the blob hash is its own).
- **(b)** strict, `skR` public — `capstone_b.pv`, one line.
- **(c)** strict, **both** channel keys public — `cap_cc01_c.pv`, one line. Per §1.1's cases table
  this case **is** companion **C-C1**, not a correct-form run.
- **(d)** degraded, sole channel public — `capstone_d.pv`, a **documented copy**: `derive.py`'s
  `degraded()` transformation and nothing else (one authority channel; one evidence check; `ev` the
  sole term rather than §1.3's pair; `AcceptS` in place of the library's `Accept`; **C-Q1 link 1b and
  C-Q2 not asserted**, per §1.1's cases table and §3; **C-Q6 conjunct 1's unrestricted form not
  asserted**, per §3 §(5)).

`run_ladder.sh` runs the ladder in the registered order (§3), with one departure that is stated
rather than taken silently. The registered order is *"C-Q1's links before every companion; (a), (b),
(d) before (c); C-Q7, C-Q8, C-Q9 before links 3 and 4 and before C-Q6"* (`:301-304`). The last clause
is a **query** order and is honoured by the declaration order inside `capstone.pv`. The first is a
**run** order and is honoured: the case-(a) and case-(b) correct-form runs are a barrier and complete
before any companion starts. **The departure:** cases (c) and (d) are materially more expensive than the
strict correct-form cases — by a factor not yet measured under the repaired model (finding F-3) — so
they run in their own slots **alongside** the strict companion waves rather than in front of them, and the case-(c) and
case-(d) companions wait for them. What "(a), (b), (d) before (c)" protects — that no companion's
colour is read before the correct model's is — is preserved for every case: no companion of a case is
run before that case's correct-form run has completed. What is not preserved is that (d) finishes
before (c) starts; they run concurrently, in separate processes with separate boxes. This is a
scheduling choice and changes no colour. *(Dated note 2026-10-06: that describes ladder 1. Ladder 3
ran (a) and (b), then (d)'s correct form, then the companion waves of (a), (b) and (d), and case (c) alone
last (`ladder.log:4-8`, `:94`). No companion of any case started before that case's correct-form run had
completed.)* `dev/` holds the development scratch, **none of it a result**:

- `dev/first.out` — the first development run, made **before** the ladder and under the **superseded**
  blob `508b9018…`. It is **not** byte-identical to today's `capstone.out` and must not be compared
  with it; it is retained only as the record of the model's first clean pass.
- `dev/cap_cc03_a_BROKEN_FIXTURE.out` — the quarantined run of **BF-1**, kept so the diagnosis can be
  checked against its own output. Also under the superseded blob.
- `dev/summarize.py`, `dev/mkresults.py`, `dev/assemble.py` — transcription helpers that turn the
  `.out` files into the tables below and write them into this file. They decide nothing.
- `dev/ladder.stdout` — the stdout of the superseded launches. The live ladder's is
  `proverif/ladder.launch.log`.
- *(Added 2026-10-01.)* `dev/assemble_l2.py` — the ladder-2 assembler. It keys every `RESULT` line by
  its normalised text and stops on any line it cannot key exactly once — the ladder-1 helper silently
  left six lines unkeyed in every C-C15 file, whose variables recut R-6 renumbers — and it carries the
  per-companion, per-case registration read from §4 / §9's Cases cells, each with its line. It
  compares; it decides nothing.
- `dev/assemble_l3.py` — the ladder-3 assembler: `assemble_l2.py`'s keys and per-case registration
  verbatim, with ladder 3's logs as the cell source; outputs under `dev/l3/`.
- *(Added 2026-10-01.)* `dev/abl2a/` (the strict link-2b diagnosis behind recut R-9), `dev/recut_pre/`
  (the pre-ladder full-file runs under the recut) and `dev/abl_d/` (the degraded-wave diagnosis). Scratch
  runs under memory caps. **None of them is a result**, no cell is filled from them, and none is counted
  in the ceiling.

**TWO READINGS OF THE COMPANION BOX, AND WHICH ONE THIS FILE REPORTS UNDER.** The registration can
be read two ways on how much wall clock a companion is allowed, and the cross-family reviewer will
ask which governs, so both are recorded for every companion run and neither is decided here. *(REPAIR
2026-10-01, skeptic S-4: the choice is now routed to the author, with its effect row by row; see section 3,
*Which box reading each severing depends on*, and *ROUTED TO THE AUTHOR — second question*.)*

- **The per-case-sum reading.** §3's timebox table declares a box per registered query and totals
  them: *"**Total declared, per compromise case** | | **27** | **1185 min (19 h 45 m)**"*
  (`:1595`), with the whole-ladder ceiling *"at most **4 × 1185 = 4740 min (79 h)**"* (`:1599`,
  `:1620`). Each `.pv` here carries **every** registered query of its case, so on this reading a run
  is allowed the sum of the boxes of the queries it carries — 1185 min for a strict case, 1095 min
  for (d), which asserts neither link 1b nor C-Q2. **`run_ladder.sh` enforces this reading**, because
  it is the one a single file carrying every query can be held to.
- **The predicted-red reading.** §4's count paragraph says *"**No companion carries a timebox**:
  §3's timebox table is over registered **queries** only, and **a companion runs inside the box of
  the query it is predicted to red**"* (`:1867-1870`), with the per-companion assignments spelled out
  where they are not obvious — *"C-C17 runs inside link 2a's 45-minute box"* and *"C-C16 runs inside
  link 5's 60-minute box"* (`:1873-1875`), *"C-C18 runs inside C-Q10's 30-minute box"* (`:1875-1876`),
  C-C8's isolation runs *"inside C-Q9's 60-minute box"* (§9(2)). On this reading a companion's box is
  30 to 90 minutes, not 1185.

Section 2 therefore carries **two columns**: `rc` and seconds under the per-case-sum box the ladder
actually enforced, and whether that same run finished inside the box of the query it is predicted to
red. Where a companion is predicted to red more than one query the **strictest** reading is taken —
the **smallest** of their boxes — and the column names which query it is. **Nothing is re-run to
produce this**: both columns are read off the one `ladder.log` line. If the strict reading governs,
section 2's second column is the report under it; if the per-case-sum reading governs, the first
column is.

*(REPAIR 2026-10-01, skeptic S-10.)* Where the registration **assigns** a companion's box in words, section
2's column does not use it: it takes the smallest box among the companion's predicted-red queries, 30
minutes, for three companions the registration assigns elsewhere — C-C17 to link 2a's 45-minute box, C-C16 to
link 5's 60-minute box, and C-C9 to link 2b's, which is 60 minutes (`PREDICTIONS.md:1873-1875`; §3's table,
`:1588`). **No yes/no changes**, checked run by run on ladder 3: C-C9 ran 240, 246 and 1 323 s, inside both 30 and 60
minutes; C-C16 ran 275 and 251 s in strict (inside both) and 6 261 s in (d) (outside both); C-C17 ran
27 085 and 25 996 s (outside both). The generated column is therefore left as it is. Which reading governs
at all is routed to the author (*ROUTED TO THE AUTHOR — second question*), and the row-by-row effect is in
section 3 (*Which box reading each severing depends on*).

**The whole-ladder ceiling.** §3 puts it at *"at most 4 × 1185 = 4740 min (79 h)"* (`:1620`). The
ladder's total wall clock against that ceiling is recorded under **Not run** when it completes, and
if it exceeds the ceiling this file says so plainly.

**Timeboxes, and how they are read here.** §3's table declares a box **per registered query**, 27
entries and 1185 min per compromise case. Each `.pv` here carries **every** registered query of its
case, so each run is given the **per-case sum**: 1185 min for a strict case, 1095 min for (d), which
asserts neither link 1b nor C-Q2. Because a whole-model run's wall clock is an upper bound on every
query's own time, **a run that finishes under 30 minutes is inside the smallest registered box for
every query it carries**; `ladder.log` records the seconds so that can be checked rather than taken
on trust. No companion carries a box of its own (§4, "The count"); it runs inside the box of the
query it is predicted to red, and a fortiori inside the sum.

---

<!--RESULTS-TABLES-->
*(This block was rewritten 2026-10-06 for ladder 3. Every cell is read from ladder 3's `.out` files and
`ladder.log`; ladder 2 is cited only for the eleven files not run under this blob. The ladder-2 tables are
in `proverif/ladder2/RESULTS-ladder2.md`; the cross-check below shows every one of their `RESULT` lines
reproduced byte for byte.)*

## 1. Every registered query, by case

The four correct-form runs: case (a) `capstone.out`, (b) `capstone_b.out`, (c) `cap_cc01_c.out` (case (c)
**is** C-C1, §1.1), (d) `capstone_d.out`. Each row gives the registered prediction with its
`PREDICTIONS.md` line, the observed `.out` line with ProVerif's verdict, and the outcome against the
registered branch. A query is listed only in the cases it is stated for (B-4: `cap_cc01_c.pv` carries the
strict file's C-Q2, C-Q6 and C-Q10, none of which is stated for (c); they appear in section 2's C-C1 row
and are read nowhere). In §3's three-outcome vocabulary every cell here is a **termination**, because
ProVerif resolved each query. No correct-form run had a timeout, and none left a query unresolved
(`cannot be proved` occurs in no ladder-3 `.out`). The two standing-witness rows give the layer of the printed
trace (BF-6): `HonestWrappedStandingAgreed`'s goal event carries it; for `HonestStandingEstablished` it is
the standing path's `estCh` report that the judge consumed.

<!--S1-->
| Registered query | Registered prediction (`PREDICTIONS.md` line) | Case | Observed (`.out` line, verdict) | Outcome in the registered vocabulary |
|---|---|---|---|---|
| C-Q1 link 1a | green, p ~ 0.8 (`:362`) | (a) | `capstone.out:2561` `is true` — GREEN | **as registered** |
| C-Q1 link 1a | green, p ~ 0.8 (`:362`) | (b) | `capstone_b.out:2562` `is true` — GREEN | **as registered** |
| C-Q1 link 1a | green, p ~ 0.8 (`:362`) | (c) | `cap_cc01_c.out:2720` `is true` — GREEN | **as registered** |
| C-Q1 link 1a | green, p ~ 0.8 (`:362`) | (d) | `capstone_d.out:2558` `is true` — GREEN | **as registered** |
| C-Q1 link 1b | `is true` in (a) and (b), p ~ 0.8; `is false` in (c) (`:379`) | (a) | `capstone.out:2728` `is true` — GREEN | **as registered** |
| C-Q1 link 1b | `is true` in (a) and (b), p ~ 0.8; `is false` in (c) (`:379`) | (b) | `capstone_b.out:2731` `is true` — GREEN | **as registered** |
| C-Q1 link 1b | `is true` in (a) and (b), p ~ 0.8; `is false` in (c) (`:379`) | (c) | `cap_cc01_c.out:3278` `is false` — RED | **as registered** |
| C-Q1 link 2a | green, p ~ 0.8 (`:408`) | (a) | `capstone.out:2793` `is true` — GREEN | **as registered** |
| C-Q1 link 2a | green, p ~ 0.8 (`:408`) | (b) | `capstone_b.out:2797` `is true` — GREEN | **as registered** |
| C-Q1 link 2a | green, p ~ 0.8 (`:408`) | (c) | `cap_cc01_c.out:3500` `is true` — GREEN | **as registered** |
| C-Q1 link 2a | green, p ~ 0.8 (`:408`) | (d) | `capstone_d.out:2738` `is true` — GREEN | **as registered** |
| link 2b one-signer conj. | all three conjuncts `is true`, p ~ 0.55 (`:447`) | (a) | `capstone.out:2945` `is true` — GREEN | **as registered** |
| link 2b one-signer conj. | all three conjuncts `is true`, p ~ 0.55 (`:447`) | (b) | `capstone_b.out:2950` `is true` — GREEN | **as registered** |
| link 2b one-signer conj. | all three conjuncts `is true`, p ~ 0.55 (`:447`) | (c) | `cap_cc01_c.out:4839` `is true` — GREEN | **as registered** |
| link 2b one-signer conj. | all three conjuncts `is true`, p ~ 0.55 (`:447`) | (d) | `capstone_d.out:3839` `is true` — GREEN | **as registered** |
| link 2b slot-A conj. | all three conjuncts `is true`, p ~ 0.55 (`:447`) | (a) | `capstone.out:3097` `is true` — GREEN | **as registered** |
| link 2b slot-A conj. | all three conjuncts `is true`, p ~ 0.55 (`:447`) | (b) | `capstone_b.out:3103` `is true` — GREEN | **as registered** |
| link 2b slot-A conj. | all three conjuncts `is true`, p ~ 0.55 (`:447`) | (c) | `cap_cc01_c.out:6178` `is true` — GREEN | **as registered** |
| link 2b slot-A conj. | all three conjuncts `is true`, p ~ 0.55 (`:447`) | (d) | `capstone_d.out:4940` `is true` — GREEN | **as registered** |
| link 2b slot-B conj. | all three conjuncts `is true`, p ~ 0.55 (`:447`) | (a) | `capstone.out:3249` `is true` — GREEN | **as registered** |
| link 2b slot-B conj. | all three conjuncts `is true`, p ~ 0.55 (`:447`) | (b) | `capstone_b.out:3256` `is true` — GREEN | **as registered** |
| link 2b slot-B conj. | all three conjuncts `is true`, p ~ 0.55 (`:447`) | (c) | `cap_cc01_c.out:7517` `is true` — GREEN | **as registered** |
| link 2b slot-B conj. | all three conjuncts `is true`, p ~ 0.55 (`:447`) | (d) | `capstone_d.out:6041` `is true` — GREEN | **as registered** |
| C-Q7 | green, p ~ 0.8 (`:1371`) | (a) | `capstone.out:3314` `is true` — GREEN | **as registered** |
| C-Q7 | green, p ~ 0.8 (`:1371`) | (b) | `capstone_b.out:3322` `is true` — GREEN | **as registered** |
| C-Q7 | green, p ~ 0.8 (`:1371`) | (c) | `cap_cc01_c.out:7739` `is true` — GREEN | **as registered** |
| C-Q7 | green, p ~ 0.8 (`:1371`) | (d) | `capstone_d.out:6221` `is true` — GREEN | **as registered** |
| C-Q8 | green, p ~ 0.75 (`:1391`) | (a) | `capstone.out:3379` `is true` — GREEN | **as registered** |
| C-Q8 | green, p ~ 0.75 (`:1391`) | (b) | `capstone_b.out:3388` `is true` — GREEN | **as registered** |
| C-Q8 | green, p ~ 0.75 (`:1391`) | (c) | `cap_cc01_c.out:7961` `is true` — GREEN | **as registered** |
| C-Q8 | green, p ~ 0.75 (`:1391`) | (d) | `capstone_d.out:6401` `is true` — GREEN | **as registered** |
| C-Q9 | green, p ~ 0.8 (`:1408`) | (a) | `capstone.out:3444` `is true` — GREEN | **as registered** |
| C-Q9 | green, p ~ 0.8 (`:1408`) | (b) | `capstone_b.out:3454` `is true` — GREEN | **as registered** |
| C-Q9 | green, p ~ 0.8 (`:1408`) | (c) | `cap_cc01_c.out:8183` `is true` — GREEN | **as registered** |
| C-Q9 | green, p ~ 0.8 (`:1408`) | (d) | `capstone_d.out:6581` `is true` — GREEN | **as registered** |
| link 3 | green, p ~ 0.8 (`:466`) | (a) | `capstone.out:3509` `is true` — GREEN | **as registered** |
| link 3 | green, p ~ 0.8 (`:466`) | (b) | `capstone_b.out:3520` `is true` — GREEN | **as registered** |
| link 3 | green, p ~ 0.8 (`:466`) | (c) | `cap_cc01_c.out:8405` `is true` — GREEN | **as registered** |
| link 3 | green, p ~ 0.8 (`:466`) | (d) | `capstone_d.out:6761` `is true` — GREEN | **as registered** |
| link 4 | green, p ~ 0.75 (`:479`) | (a) | `capstone.out:3574` `is true` — GREEN | **as registered** |
| link 4 | green, p ~ 0.75 (`:479`) | (b) | `capstone_b.out:3586` `is true` — GREEN | **as registered** |
| link 4 | green, p ~ 0.75 (`:479`) | (c) | `cap_cc01_c.out:8627` `is true` — GREEN | **as registered** |
| link 4 | green, p ~ 0.75 (`:479`) | (d) | `capstone_d.out:6941` `is true` — GREEN | **as registered** |
| link 5 | green, p ~ 0.65 (`:509`) | (a) | `capstone.out:3639` `is true` — GREEN | **as registered** |
| link 5 | green, p ~ 0.65 (`:509`) | (b) | `capstone_b.out:3652` `is true` — GREEN | **as registered** |
| link 5 | green, p ~ 0.65 (`:509`) | (c) | `cap_cc01_c.out:8849` `is true` — GREEN | **as registered** |
| link 5 | green, p ~ 0.65 (`:509`) | (d) | `capstone_d.out:7121` `is true` — GREEN | **as registered** |
| link 6a | green, p ~ 0.85 (`:527`) | (a) | `capstone.out:3704` `is true` — GREEN | **as registered** |
| link 6a | green, p ~ 0.85 (`:527`) | (b) | `capstone_b.out:3718` `is true` — GREEN | **as registered** |
| link 6a | green, p ~ 0.85 (`:527`) | (c) | `cap_cc01_c.out:9071` `is true` — GREEN | **as registered** |
| link 6a | green, p ~ 0.85 (`:527`) | (d) | `capstone_d.out:7301` `is true` — GREEN | **as registered** |
| link 6b | green, p ~ 0.8 (`:583`) | (a) | `capstone.out:3769` `is true` — GREEN | **as registered** |
| link 6b | green, p ~ 0.8 (`:583`) | (b) | `capstone_b.out:3784` `is true` — GREEN | **as registered** |
| link 6b | green, p ~ 0.8 (`:583`) | (c) | `cap_cc01_c.out:9293` `is true` — GREEN | **as registered** |
| link 6b | green, p ~ 0.8 (`:583`) | (d) | `capstone_d.out:7481` `is true` — GREEN | **as registered** |
| C-Q2 | green, p ~ 0.65 (`:599`) | (a) | `capstone.out:3834` `is true` — GREEN | **as registered** |
| C-Q2 | green, p ~ 0.65 (`:599`) | (b) | `capstone_b.out:3850` `is true` — GREEN | **as registered** |
| C-Q3 `ReattributedA` | green, p ~ 0.8 (`:615`) | (a) | `capstone.out:3899` `is true` — GREEN | **as registered** |
| C-Q3 `ReattributedA` | green, p ~ 0.8 (`:615`) | (b) | `capstone_b.out:3916` `is true` — GREEN | **as registered** |
| C-Q3 `ReattributedA` | green, p ~ 0.8 (`:615`) | (c) | `cap_cc01_c.out:9737` `is true` — GREEN | **as registered** |
| C-Q3 `ReattributedA` | green, p ~ 0.8 (`:615`) | (d) | `capstone_d.out:7661` `is true` — GREEN | **as registered** |
| C-Q3 `ReattributedB` | green, p ~ 0.8 (`:615`) | (a) | `capstone.out:3964` `is true` — GREEN | **as registered** |
| C-Q3 `ReattributedB` | green, p ~ 0.8 (`:615`) | (b) | `capstone_b.out:3982` `is true` — GREEN | **as registered** |
| C-Q3 `ReattributedB` | green, p ~ 0.8 (`:615`) | (c) | `cap_cc01_c.out:9959` `is true` — GREEN | **as registered** |
| C-Q3 `ReattributedB` | green, p ~ 0.8 (`:615`) | (d) | `capstone_d.out:7841` `is true` — GREEN | **as registered** |
| C-Q4 `Rescoped` | both green, p ~ 0.75 (`:630`) | (a) | `capstone.out:4029` `is true` — GREEN | **as registered** |
| C-Q4 `Rescoped` | both green, p ~ 0.75 (`:630`) | (b) | `capstone_b.out:4048` `is true` — GREEN | **as registered** |
| C-Q4 `Rescoped` | both green, p ~ 0.75 (`:630`) | (c) | `cap_cc01_c.out:10181` `is true` — GREEN | **as registered** |
| C-Q4 `Rescoped` | both green, p ~ 0.75 (`:630`) | (d) | `capstone_d.out:8021` `is true` — GREEN | **as registered** |
| C-Q4 `InnerSigTransplanted` | both green, p ~ 0.75 (`:630`) | (a) | `capstone.out:4094` `is true` — GREEN | **as registered** |
| C-Q4 `InnerSigTransplanted` | both green, p ~ 0.75 (`:630`) | (b) | `capstone_b.out:4114` `is true` — GREEN | **as registered** |
| C-Q4 `InnerSigTransplanted` | both green, p ~ 0.75 (`:630`) | (c) | `cap_cc01_c.out:10403` `is true` — GREEN | **as registered** |
| C-Q4 `InnerSigTransplanted` | both green, p ~ 0.75 (`:630`) | (d) | `capstone_d.out:8201` `is true` — GREEN | **as registered** |
| C-Q5 | green, p ~ 0.8 (`:689`) | (a) | `capstone.out:4159` `is true` — GREEN | **as registered** |
| C-Q5 | green, p ~ 0.8 (`:689`) | (b) | `capstone_b.out:4180` `is true` — GREEN | **as registered** |
| C-Q5 | green, p ~ 0.8 (`:689`) | (c) | `cap_cc01_c.out:10625` `is true` — GREEN | **as registered** |
| C-Q5 | green, p ~ 0.8 (`:689`) | (d) | `capstone_d.out:8381` `is true` — GREEN | **as registered** |
| `HonestComplete` (1-signer) | reachable, p ~ 0.85 (`:699`) | (a) | `capstone.out:4566` `is false` — REACHABLE | **as registered** |
| `HonestComplete` (1-signer) | reachable, p ~ 0.85 (`:699`) | (b) | `capstone_b.out:4588` `is false` — REACHABLE | **as registered** |
| `HonestComplete` (1-signer) | reachable, p ~ 0.85 (`:699`) | (c) | `cap_cc01_c.out:11192` `is false` — REACHABLE | **as registered** |
| `HonestComplete` (1-signer) | reachable, p ~ 0.85 (`:699`) | (d) | `capstone_d.out:8881` `is false` — REACHABLE | **as registered** |
| `HonestComplete` (2-signer) | reachable, p ~ 0.85 (`:699`) | (a) | `capstone.out:5016` `is false` — REACHABLE | **as registered** |
| `HonestComplete` (2-signer) | reachable, p ~ 0.85 (`:699`) | (b) | `capstone_b.out:5039` `is false` — REACHABLE | **as registered** |
| `HonestComplete` (2-signer) | reachable, p ~ 0.85 (`:699`) | (c) | `cap_cc01_c.out:11802` `is false` — REACHABLE | **as registered** |
| `HonestComplete` (2-signer) | reachable, p ~ 0.85 (`:699`) | (d) | `capstone_d.out:9424` `is false` — REACHABLE | **as registered** |
| C-Q10 | green, p ~ 0.85 (`:1459`) | (a) | `capstone.out:5081` `is true` — GREEN | **as registered** |
| C-Q10 | green, p ~ 0.85 (`:1459`) | (b) | `capstone_b.out:5105` `is true` — GREEN | **as registered** |
| C-Q10 | green, p ~ 0.85 (`:1459`) | (d) | `capstone_d.out:9604` `is true` — GREEN | **as registered** |
| C-Q6 c1 unrestricted | all three conjuncts hold, p ~ 0.5 (unrestricted form strict only) (`:1324`) | (a) | `capstone.out:5171` `is true` — GREEN | **as registered** |
| C-Q6 c1 unrestricted | all three conjuncts hold, p ~ 0.5 (unrestricted form strict only) (`:1324`) | (b) | `capstone_b.out:5196` `is true` — GREEN | **as registered** |
| C-Q6 c1 `skI` | green in (a), (b) and (d) (`:1233`) | (a) | `capstone.out:5249` `is true` — GREEN | **as registered** |
| C-Q6 c1 `skI` | green in (a), (b) and (d) (`:1233`) | (b) | `capstone_b.out:5275` `is true` — GREEN | **as registered** |
| C-Q6 c1 `skI` | green in (a), (b) and (d) (`:1233`) | (d) | `capstone_d.out:9797` `is true` — GREEN | **as registered** |
| C-Q6 c1 `skI2` | green in (a), (b) and (d) (`:1233`) | (a) | `capstone.out:5327` `is true` — GREEN | **as registered** |
| C-Q6 c1 `skI2` | green in (a), (b) and (d) (`:1233`) | (b) | `capstone_b.out:5354` `is true` — GREEN | **as registered** |
| C-Q6 c1 `skI2` | green in (a), (b) and (d) (`:1233`) | (d) | `capstone_d.out:9990` `is true` — GREEN | **as registered** |
| C-Q6 c2 | unreachable in (a), (b) and (d) (`:1245`) | (a) | `capstone.out:5392` `is true` — GREEN | **as registered** |
| C-Q6 c2 | unreachable in (a), (b) and (d) (`:1245`) | (b) | `capstone_b.out:5420` `is true` — GREEN | **as registered** |
| C-Q6 c2 | unreachable in (a), (b) and (d) (`:1245`) | (d) | `capstone_d.out:10170` `is true` — GREEN | **as registered** |
| C-Q6 c3 `ScopeMisreported` | unreachable in (a), (b) and (d) (`:1289`) | (a) | `capstone.out:5457` `is true` — GREEN | **as registered** |
| C-Q6 c3 `ScopeMisreported` | unreachable in (a), (b) and (d) (`:1289`) | (b) | `capstone_b.out:5486` `is true` — GREEN | **as registered** |
| C-Q6 c3 `ScopeMisreported` | unreachable in (a), (b) and (d) (`:1289`) | (d) | `capstone_d.out:10351` `is true` — GREEN | **as registered** |
| `Accept(S) => IssuerSigned` | green in (a)/(b) p ~ 0.85; RED in (c) p ~ 0.9; degraded `AcceptS` form registered RED in (d), the A4.6 cost (`:1569, 1580`) | (a) | `capstone.out:5554` `is true` — GREEN | **as registered** |
| `Accept(S) => IssuerSigned` | green in (a)/(b) p ~ 0.85; RED in (c) p ~ 0.9; degraded `AcceptS` form registered RED in (d), the A4.6 cost (`:1569, 1580`) | (b) | `capstone_b.out:5585` `is true` — GREEN | **as registered** |
| `Accept(S) => IssuerSigned` | green in (a)/(b) p ~ 0.85; RED in (c) p ~ 0.9; degraded `AcceptS` form registered RED in (d), the A4.6 cost (`:1569, 1580`) | (c) | `cap_cc01_c.out:14277` `is false` — RED | **as registered** |
| `Accept(S) => IssuerSigned` | green in (a)/(b) p ~ 0.85; RED in (c) p ~ 0.9; degraded `AcceptS` form registered RED in (d), the A4.6 cost (`:1569, 1580`) | (d) | `capstone_d.out:10976` `is false` — RED | **as registered** |
| `AcceptedUnderHonestKey => IssuerSigned` | green, p ~ 0.85 (`:1570`) | (a) | `capstone.out:5649` `is true` — GREEN | **as registered** |
| `AcceptedUnderHonestKey => IssuerSigned` | green, p ~ 0.85 (`:1570`) | (b) | `capstone_b.out:5681` `is true` — GREEN | **as registered** |
| `AcceptedUnderHonestKey => IssuerSigned` | green, p ~ 0.85 (`:1570`) | (c) | `cap_cc01_c.out:14743` `is true` — GREEN | **as registered** |
| `AcceptedUnderHonestKey => IssuerSigned` | green, p ~ 0.85 (`:1570`) | (d) | `capstone_d.out:11354` `is true` — GREEN | **as registered** |
| `Stripped` | green, p ~ 0.8 (`:1571`) | (a) | `capstone.out:5714` `is true` — GREEN | **as registered** |
| `Stripped` | green, p ~ 0.8 (`:1571`) | (b) | `capstone_b.out:5747` `is true` — GREEN | **as registered** |
| `Stripped` | green, p ~ 0.8 (`:1571`) | (c) | `cap_cc01_c.out:14965` `is true` — GREEN | **as registered** |
| `Stripped` | green, p ~ 0.8 (`:1571`) | (d) | `capstone_d.out:11534` `is true` — GREEN | **as registered** |
| `SignerForged` | green, p ~ 0.8 (`:1572`) | (a) | `capstone.out:5779` `is true` — GREEN | **as registered** |
| `SignerForged` | green, p ~ 0.8 (`:1572`) | (b) | `capstone_b.out:5813` `is true` — GREEN | **as registered** |
| `SignerForged` | green, p ~ 0.8 (`:1572`) | (c) | `cap_cc01_c.out:15187` `is true` — GREEN | **as registered** |
| `SignerForged` | green, p ~ 0.8 (`:1572`) | (d) | `capstone_d.out:11714` `is true` — GREEN | **as registered** |
| `Spliced` | green, p ~ 0.75 (`:1573`) | (a) | `capstone.out:5844` `is true` — GREEN | **as registered** |
| `Spliced` | green, p ~ 0.75 (`:1573`) | (b) | `capstone_b.out:5879` `is true` — GREEN | **as registered** |
| `Spliced` | green, p ~ 0.75 (`:1573`) | (c) | `cap_cc01_c.out:15409` `is true` — GREEN | **as registered** |
| `Spliced` | green, p ~ 0.75 (`:1573`) | (d) | `capstone_d.out:11894` `is true` — GREEN | **as registered** |
| `TypeConfused` | green, p ~ 0.85 (`:1574`) | (a) | `capstone.out:5909` `is true` — GREEN | **as registered** |
| `TypeConfused` | green, p ~ 0.85 (`:1574`) | (b) | `capstone_b.out:5945` `is true` — GREEN | **as registered** |
| `TypeConfused` | green, p ~ 0.85 (`:1574`) | (c) | `cap_cc01_c.out:15631` `is true` — GREEN | **as registered** |
| `TypeConfused` | green, p ~ 0.85 (`:1574`) | (d) | `capstone_d.out:12074` `is true` — GREEN | **as registered** |
| `VersionLied` | green, p ~ 0.85 (`:1575`) | (a) | `capstone.out:5974` `is true` — GREEN | **as registered** |
| `VersionLied` | green, p ~ 0.85 (`:1575`) | (b) | `capstone_b.out:6011` `is true` — GREEN | **as registered** |
| `VersionLied` | green, p ~ 0.85 (`:1575`) | (c) | `cap_cc01_c.out:15853` `is true` — GREEN | **as registered** |
| `VersionLied` | green, p ~ 0.85 (`:1575`) | (d) | `capstone_d.out:12254` `is true` — GREEN | **as registered** |
| `HonestChain(L0)` | reachable in all four cases, p ~ 0.85 (`:1487`) | (a) | `capstone.out:6416` `is false` — REACHABLE | **as registered** |
| `HonestChain(L0)` | reachable in all four cases, p ~ 0.85 (`:1487`) | (b) | `capstone_b.out:6454` `is false` — REACHABLE | **as registered** |
| `HonestChain(L0)` | reachable in all four cases, p ~ 0.85 (`:1487`) | (c) | `cap_cc01_c.out:16456` `is false` — REACHABLE | **as registered** |
| `HonestChain(L0)` | reachable in all four cases, p ~ 0.85 (`:1487`) | (d) | `capstone_d.out:12789` `is false` — REACHABLE | **as registered** |
| `HonestChain(L1)` | reachable in all four cases, p ~ 0.85 (`:1487`) | (a) | `capstone.out:6920` `is false` — REACHABLE | **as registered** |
| `HonestChain(L1)` | reachable in all four cases, p ~ 0.85 (`:1487`) | (b) | `capstone_b.out:6959` `is false` — REACHABLE | **as registered** |
| `HonestChain(L1)` | reachable in all four cases, p ~ 0.85 (`:1487`) | (c) | `cap_cc01_c.out:17121` `is false` — REACHABLE | **as registered** |
| `HonestChain(L1)` | reachable in all four cases, p ~ 0.85 (`:1487`) | (d) | `capstone_d.out:13387` `is false` — REACHABLE | **as registered** |
| `HonestChain(L2)` | reachable in all four cases, p ~ 0.85 (`:1487`) | (a) | `capstone.out:7590` `is false` — REACHABLE | **as registered** |
| `HonestChain(L2)` | reachable in all four cases, p ~ 0.85 (`:1487`) | (b) | `capstone_b.out:7630` `is false` — REACHABLE | **as registered** |
| `HonestChain(L2)` | reachable in all four cases, p ~ 0.85 (`:1487`) | (c) | `cap_cc01_c.out:17950` `is false` — REACHABLE | **as registered** |
| `HonestChain(L2)` | reachable in all four cases, p ~ 0.85 (`:1487`) | (d) | `capstone_d.out:14145` `is false` — REACHABLE | **as registered** |
| `HonestAccepted` | reachable in all four cases, p ~ 0.85 (`:1487`) | (a) | `capstone.out:8032` `is false` — REACHABLE | **as registered** |
| `HonestAccepted` | reachable in all four cases, p ~ 0.85 (`:1487`) | (b) | `capstone_b.out:8073` `is false` — REACHABLE | **as registered** |
| `HonestAccepted` | reachable in all four cases, p ~ 0.85 (`:1487`) | (c) | `cap_cc01_c.out:18552` `is false` — REACHABLE | **as registered** |
| `HonestAccepted` | reachable in all four cases, p ~ 0.85 (`:1487`) | (d) | `capstone_d.out:14680` `is false` — REACHABLE | **as registered** |
| `HonestWrappedAccepted` | reachable in all four cases, p ~ 0.85 (`:1487`) | (a) | `capstone.out:8616` `is false` — REACHABLE | **as registered** |
| `HonestWrappedAccepted` | reachable in all four cases, p ~ 0.85 (`:1487`) | (b) | `capstone_b.out:8658` `is false` — REACHABLE | **as registered** |
| `HonestWrappedAccepted` | reachable in all four cases, p ~ 0.85 (`:1487`) | (c) | `cap_cc01_c.out:19272` `is false` — REACHABLE | **as registered** |
| `HonestWrappedAccepted` | reachable in all four cases, p ~ 0.85 (`:1487`) | (d) | `capstone_d.out:15328` `is false` — REACHABLE | **as registered** |
| `HonestStandingEstablished` | reachable in all four cases, p ~ 0.85 (`:1487`) | (a) | `capstone.out:9138` `is false` — REACHABLE; trace at `L1` (`:9130`) | **as registered** |
| `HonestStandingEstablished` | reachable in all four cases, p ~ 0.85 (`:1487`) | (b) | `capstone_b.out:9181` `is false` — REACHABLE; trace at `L1` (`:9173`) | **as registered** |
| `HonestStandingEstablished` | reachable in all four cases, p ~ 0.85 (`:1487`) | (c) | `cap_cc01_c.out:19954` `is false` — REACHABLE; trace at `L1` (`:19946`) | **as registered** |
| `HonestStandingEstablished` | reachable in all four cases, p ~ 0.85 (`:1487`) | (d) | `capstone_d.out:15945` `is false` — REACHABLE; trace at `L1` (`:15937`) | **as registered** |
| `HonestWrappedStandingAgreed` | reachable in all four cases, p ~ 0.85 (`:1487`) | (a) | `capstone.out:9804` `is false` — REACHABLE; trace at `L1` (`:9800`) | **as registered** |
| `HonestWrappedStandingAgreed` | reachable in all four cases, p ~ 0.85 (`:1487`) | (b) | `capstone_b.out:9849` `is false` — REACHABLE; trace at `L1` (`:9845`) | **as registered** |
| `HonestWrappedStandingAgreed` | reachable in all four cases, p ~ 0.85 (`:1487`) | (c) | `cap_cc01_c.out:20834` `is false` — REACHABLE; trace at `L1` (`:20830`) | **as registered** |
| `HonestWrappedStandingAgreed` | reachable in all four cases, p ~ 0.85 (`:1487`) | (d) | `capstone_d.out:16744` `is false` — REACHABLE; trace at `L1` (`:16740`) | **as registered** |
| S1 | reachable in every correct-form run (`:1516`) | (a) | `capstone.out:10260` `is false` — REACHABLE | **as registered** |
| S1 | reachable in every correct-form run (`:1516`) | (b) | `capstone_b.out:10305` `is false` — REACHABLE | **as registered** |
| S1 | reachable in every correct-form run (`:1516`) | (d) | `capstone_d.out:17223` `is false` — REACHABLE | **as registered** |
| S2 | reachable in every correct-form run (`:1516`) | (a) | `capstone.out:10714` `is false` — REACHABLE | **as registered** |
| S2 | reachable in every correct-form run (`:1516`) | (b) | `capstone_b.out:10759` `is false` — REACHABLE | **as registered** |
| S2 | reachable in every correct-form run (`:1516`) | (d) | `capstone_d.out:17703` `is false` — REACHABLE | **as registered** |
| S3 | reachable in every correct-form run (`:1516`) | (a) | `capstone.out:11029` `is false` — REACHABLE | **as registered** |
| S3 | reachable in every correct-form run (`:1516`) | (b) | `capstone_b.out:11074` `is false` — REACHABLE | **as registered** |
| S3 | reachable in every correct-form run (`:1516`) | (d) | `capstone_d.out:18110` `is false` — REACHABLE | **as registered** |
| S4 | reachable in every correct-form run (`:1516`) | (a) | `capstone.out:11481` `is false` — REACHABLE | **as registered** |
| S4 | reachable in every correct-form run (`:1516`) | (b) | `capstone_b.out:11526` `is false` — REACHABLE | **as registered** |
| S4 | reachable in every correct-form run (`:1516`) | (d) | `capstone_d.out:18586` `is false` — REACHABLE | **as registered** |
| MISMATCH | reachable in every correct-form run (`:1516`) | (a) | `capstone.out:11846` `is false` — REACHABLE | **as registered** |
| MISMATCH | reachable in every correct-form run (`:1516`) | (b) | `capstone_b.out:11891` `is false` — REACHABLE | **as registered** |
| MISMATCH | reachable in every correct-form run (`:1516`) | (d) | `capstone_d.out:19037` `is false` — REACHABLE | **as registered** |

**Tally:** 173 cells as registered, 0 missed, 0 not declared, 0 from a run that did not land.
<!--END-S1-->

## 2. Every companion, by case

There is one row per configuration file. C-C1 runs in (c) only; C-C10's isolation control and C-C14 run in
(a) and (b) only; every other configuration runs in (a), (b) and (d). The `rc`, seconds and peak resident
set (GiB = kB / 1 048 576) are read off `ladder.log`. The box the ladder enforced is 71 100 s strict and
65 700 s degraded, which is section 0's per-case-sum reading. The fourth column gives the
predicted-red-box reading. **Observed reds** lists every safety query and observer that came back
`is false`. In (d) that list includes the registered degraded baseline red `AcceptS => IssuerSigned`
(`PREDICTIONS.md:1580`; §4 builder note (2), `:1788-1791`). The eleven ladder-2 degraded mechanism failures
read **not run under this blob**, with their ladder-3 `NOT-RUN` line and the ladder-2 outcome as history
(`ladder2/ladder.log`); the ladder-2 labels are **timeout (mechanism-viability failure)** and **terminated by
memory guard, classified as mechanism failure (memory)**. The Witnesses column also gives the layer of the two
standing witnesses' printed traces (BF-6). *(REPAIR 2026-10-01, skeptic S-5: the second label is **the owner
instance's clerk disposition**, not the registration's. The registration boxes time only — the word
“memory” does not occur in `PREDICTIONS.md` — and the 80 GB rule and the classification are the owner
instance's (`mem_guard_vm.sh:10-15`). Headroom at each trigger: *The degraded wave*.)*

<!--S2-->
| Companion / configuration | Case | `rc`, seconds, peak (ladder 3 log line) | Inside the box of its predicted-red query? | Observed reds (`.out` line) | Witnesses |
|---|---|---|---|---|---|
| **C-C1** — C-C1, §4 `:1770` | (c) | `rc=0`, 4569 s, 6.2 GiB peak (`ladder.log:94`) | **no**, 4569 s > 30 min (retained `Accept => IssuerSigned`) | C-Q1 link 1b `:3278`, `Accept(S) => IssuerSigned` `:14277`; *not stated for (c):* C-Q6 c1 unrestricted `:12621` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C2** — C-C2, §4 `:1771` | (a) | `rc=0`, 512 s, 0.6 GiB peak (`ladder.log:11`) | yes, 512 s <= 45 min (C-Q3) | none | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C2** — C-C2, §4 `:1771` | (b) | `rc=0`, 429 s, 0.6 GiB peak (`ladder.log:38`) | yes, 429 s <= 45 min (C-Q3) | none | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C2** — C-C2, §4 `:1771` | (d) | not run (`ladder.log:69`); ladder 2, history: timeout (mechanism-viability failure), 65702 s, 21.8 GiB (`ladder2/ladder.log:64`) | - (not run) | **not run under this blob** — no result | - |
| **C-C3** — C-C3, §4 `:1772` | (a) | `rc=0`, 269 s, 0.4 GiB peak (`ladder.log:9`) | yes, 269 s <= 45 min (C-Q5 / link 3) | C-Q9 `:3795`, link 3 `:4199` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C3** — C-C3, §4 `:1772` | (b) | `rc=0`, 267 s, 0.4 GiB peak (`ladder.log:36`) | yes, 267 s <= 45 min (C-Q5 / link 3) | C-Q9 `:3804`, link 3 `:4209` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C3** — C-C3, §4 `:1772` | (d) | not run (`ladder.log:70`); ladder 2, history: timeout (mechanism-viability failure), 65703 s, 26.3 GiB (`ladder2/ladder.log:65`) | - (not run) | **not run under this blob** — no result | - |
| **C-C4** — C-C4, §4 `:1773` | (a) | `rc=0`, 413 s, 0.5 GiB peak (`ladder.log:10`) | yes, 413 s <= 45 min (link 6b / C-Q3) | none | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C4** — C-C4, §4 `:1773` | (b) | `rc=0`, 374 s, 0.5 GiB peak (`ladder.log:37`) | yes, 374 s <= 45 min (link 6b / C-Q3) | none | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C4** — C-C4, §4 `:1773` | (d) | not run (`ladder.log:71`); ladder 2, history: timeout (mechanism-viability failure), 65702 s, 46.9 GiB (`ladder2/ladder.log:63`) | - (not run) | **not run under this blob** — no result | - |
| **C-C5** — C-C5, §4 `:1774` | (a) | `rc=0`, 485 s, 0.8 GiB peak (`ladder.log:12`) | yes, 485 s <= 45 min (link 4) | C-Q8 `:4393`, link 4 `:4998`, `Accept(S) => IssuerSigned` `:7809`, `AcceptedUnderHonestKey => IssuerSigned` `:8280` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C5** — C-C5, §4 `:1774` | (b) | `rc=0`, 452 s, 0.8 GiB peak (`ladder.log:39`) | yes, 452 s <= 45 min (link 4) | C-Q8 `:4333`, link 4 `:4917`, `Accept(S) => IssuerSigned` `:7601`, `AcceptedUnderHonestKey => IssuerSigned` `:8065` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C5** — C-C5, §4 `:1774` | (d) | not run (`ladder.log:72`); ladder 2, history: terminated by memory guard, classified as mechanism failure (memory), 64899 s, 76.5 GiB (`ladder2/ladder.log:66`, `ladder2/ladder.log:78`) | - (not run) | **not run under this blob** — no result | - |
| **C-C6** — C-C6, §4 `:1775` | (a) | `rc=0`, 1682 s, 1.1 GiB peak (`ladder.log:13`) | yes, 1682 s <= 45 min (C-Q7 / link 4) | none | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C6** — C-C6, §4 `:1775` | (b) | `rc=0`, 1522 s, 1.1 GiB peak (`ladder.log:40`) | yes, 1522 s <= 45 min (C-Q7 / link 4) | none | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C6** — C-C6, §4 `:1775` | (d) | not run (`ladder.log:73`); ladder 2, history: timeout (mechanism-viability failure), 65702 s, 25.8 GiB (`ladder2/ladder.log:67`) | - (not run) | **not run under this blob** — no result | - |
| **C-C7(i)** — C-C7(i), §4 `:1776` | (a) | `rc=0`, 2196 s, 3.1 GiB peak (`ladder.log:14`) | **no**, 2196 s > 30 min (retained honest-key authorship) | C-Q8 `:9385`, link 4 `:10116`, `Accept(S) => IssuerSigned` `:13678`, `AcceptedUnderHonestKey => IssuerSigned` `:14185` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C7(i)** — C-C7(i), §4 `:1776` | (b) | `rc=0`, 2199 s, 3.2 GiB peak (`ladder.log:41`) | **no**, 2199 s > 30 min (retained honest-key authorship) | C-Q8 `:9393`, link 4 `:10127`, `Accept(S) => IssuerSigned` `:13707`, `AcceptedUnderHonestKey => IssuerSigned` `:14215` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C7(i)** — C-C7(i), §4 `:1776` | (d) | not run (`ladder.log:74`); ladder 2, history: timeout (mechanism-viability failure), 65702 s, 28.3 GiB (`ladder2/ladder.log:68`) | - (not run) | **not run under this blob** — no result | - |
| **C-C7(ii)** — C-C7(ii), §4 `:1776` | (a) | `rc=0`, 9512 s, 8.7 GiB peak (`ladder.log:17`) | **no**, 9512 s > 45 min (link 4) | C-Q8 `:12156`, link 4 `:13412`, `Accept(S) => IssuerSigned` `:20301`, `AcceptedUnderHonestKey => IssuerSigned` `:21156` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C7(ii)** — C-C7(ii), §4 `:1776` | (b) | `rc=0`, 10549 s, 8.5 GiB peak (`ladder.log:44`) | **no**, 10549 s > 45 min (link 4) | C-Q8 `:12002`, link 4 `:13202`, `Accept(S) => IssuerSigned` `:19758`, `AcceptedUnderHonestKey => IssuerSigned` `:20595` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C7(ii)** — C-C7(ii), §4 `:1776` | (d) | not run (`ladder.log:75`); ladder 2, history: timeout (mechanism-viability failure), 65702 s, 27.4 GiB (`ladder2/ladder.log:79`) | - (not run) | **not run under this blob** — no result | - |
| **C-C8** — C-C8, §4 `:1777` | (a) | `rc=0`, 264 s, 0.4 GiB peak (`ladder.log:15`) | yes, 264 s <= 45 min (C-Q5 / link 3) | C-Q9 `:3795`, link 3 `:4199` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C8** — C-C8, §4 `:1777` | (b) | `rc=0`, 256 s, 0.4 GiB peak (`ladder.log:42`) | yes, 256 s <= 45 min (C-Q5 / link 3) | C-Q9 `:3804`, link 3 `:4209` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C8** — C-C8, §4 `:1777` | (d) | not run (`ladder.log:76`); ladder 2, history: timeout (mechanism-viability failure), 65703 s, 29.3 GiB (`ladder2/ladder.log:80`) | - (not run) | **not run under this blob** — no result | - |
| **C-C8-i** — C-C8-i, §9(2) `:2546` | (a) | `rc=0`, 264 s, 0.4 GiB peak (`ladder.log:16`) | yes, 264 s <= 60 min (C-Q9 (§9(2))) | none | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C8-i** — C-C8-i, §9(2) `:2546` | (b) | `rc=0`, 256 s, 0.4 GiB peak (`ladder.log:43`) | yes, 256 s <= 60 min (C-Q9 (§9(2))) | none | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C8-i** — C-C8-i, §9(2) `:2546` | (d) | not run (`ladder.log:77`); ladder 2, history: terminated by memory guard, classified as mechanism failure (memory), 48680 s, 76.5 GiB (`ladder2/ladder.log:83`) | - (not run) | **not run under this blob** — no result | - |
| **C-C8-ii** — C-C8-ii, §9(2) `:2547` | (a) | `rc=0`, 265 s, 0.4 GiB peak (`ladder.log:19`) | yes, 265 s <= 60 min (C-Q9 (§9(2))) | C-Q9 `:3806`, link 3 `:4210` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C8-ii** — C-C8-ii, §9(2) `:2547` | (b) | `rc=0`, 255 s, 0.3 GiB peak (`ladder.log:46`) | yes, 255 s <= 60 min (C-Q9 (§9(2))) | C-Q9 `:3815`, link 3 `:4220` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C8-ii** — C-C8-ii, §9(2) `:2547` | (d) | not run (`ladder.log:78`); ladder 2, history: terminated by memory guard, classified as mechanism failure (memory), 39900 s, 76.6 GiB (`ladder2/ladder.log:82`) | - (not run) | **not run under this blob** — no result | - |
| **C-C9** — C-C9, §4 `:1778` | (a) | `rc=0`, 240 s, 0.2 GiB peak (`ladder.log:18`) | yes, 240 s <= 30 min (retained `Stripped`) | link 2b slot-B conj. `:3505`, `Stripped` `:6176` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C9** — C-C9, §4 `:1778` | (b) | `rc=0`, 246 s, 0.2 GiB peak (`ladder.log:45`) | yes, 246 s <= 30 min (retained `Stripped`) | link 2b slot-B conj. `:3534`, `Stripped` `:6305` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C9** — C-C9, §4 `:1778` | (d) | `rc=0`, 1323 s, 1.3 GiB peak (`ladder.log:79`) | yes, 1323 s <= 30 min (retained `Stripped`) | link 2b slot-B conj. `:4576`, `Accept(S) => IssuerSigned` `:8075`, `Stripped` `:8749` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C10** — C-C10, §4 `:1779` | (a) | `rc=0`, 4012 s, 6.1 GiB peak (`ladder.log:20`) | **no**, 4012 s > 30 min (retained `Accept => IssuerSigned`) | C-Q1 link 1a `:3004`, C-Q1 link 1b `:3505`, C-Q6 c1 unrestricted `:11510`, `Accept(S) => IssuerSigned` `:12920` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C10** — C-C10, §4 `:1779` | (b) | `rc=0`, 3654 s, 6.2 GiB peak (`ladder.log:55`) | **no**, 3654 s > 30 min (retained `Accept => IssuerSigned`) | C-Q1 link 1a `:3004`, C-Q1 link 1b `:3505`, C-Q6 c1 unrestricted `:11510`, `Accept(S) => IssuerSigned` `:12920` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C10** — C-C10, §4 `:1779` | (d) | `rc=0`, 2908 s, 5.8 GiB peak (`ladder.log:80`) | **no**, 2908 s > 30 min (retained `Accept => IssuerSigned`) | C-Q1 link 1a `:2813`, `Accept(S) => IssuerSigned` `:9739` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C10 isolation control** — C-C10 isolation control, §4 `:1779` | (a) | `rc=0`, 194 s, 0.3 GiB peak (`ladder.log:21`) | yes, 194 s <= 45 min (link 1a) | C-Q1 link 1a `:2861` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C10 isolation control** — C-C10 isolation control, §4 `:1779` | (b) | `rc=0`, 182 s, 0.3 GiB peak (`ladder.log:53`) | yes, 182 s <= 45 min (link 1a) | C-Q1 link 1a `:2861` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C11** — C-C11 (Q2), §4 `:1805` | (a) | `rc=0`, 291 s, 0.3 GiB peak (`ladder.log:23`) | yes, 291 s <= 90 min (C-Q6) | C-Q6 c1 unrestricted `:5640`, C-Q6 c1 `skI` `:6181`, C-Q6 c1 `skI2` `:6714` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C11** — C-C11 (Q2), §4 `:1805` | (b) | `rc=0`, 268 s, 0.4 GiB peak (`ladder.log:56`) | yes, 268 s <= 90 min (C-Q6) | C-Q6 c1 unrestricted `:5662`, C-Q6 c1 `skI` `:6203`, C-Q6 c1 `skI2` `:6736` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C11** — C-C11 (Q2), §4 `:1805` | (d) | `rc=0`, 4248 s, 5.8 GiB peak (`ladder.log:84`) | yes, 4248 s <= 90 min (C-Q6) | C-Q6 c1 `skI` `:10394`, C-Q6 c1 `skI2` `:11048`, `Accept(S) => IssuerSigned` `:12043` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C11 alt. Q4** — C-C11 alternate Q4, §4 `:1805` | (a) | `rc=0`, 299 s, 0.4 GiB peak (`ladder.log:25`) | yes, 299 s <= 90 min (C-Q6) | C-Q6 c1 unrestricted `:5620`, C-Q6 c1 `skI` `:6137`, C-Q6 c1 `skI2` `:6646` | UNREACHABLE: S2 `:11702`, S4 `:12094`; standing traces at `L1`/`L1` |
| **C-C11 alt. Q4** — C-C11 alternate Q4, §4 `:1805` | (b) | `rc=0`, 288 s, 0.4 GiB peak (`ladder.log:57`) | yes, 288 s <= 90 min (C-Q6) | C-Q6 c1 unrestricted `:5644`, C-Q6 c1 `skI` `:6162`, C-Q6 c1 `skI2` `:6672` | UNREACHABLE: S2 `:11747`, S4 `:12141`; standing traces at `L1`/`L1` |
| **C-C11 alt. Q4** — C-C11 alternate Q4, §4 `:1805` | (d) | `rc=0`, 3710 s, 5.9 GiB peak (`ladder.log:82`) | yes, 3710 s <= 90 min (C-Q6) | C-Q6 c1 `skI` `:10239`, C-Q6 c1 `skI2` `:10843`, `Accept(S) => IssuerSigned` `:11835` | UNREACHABLE: S2 `:18311`, S4 `:18909`; standing traces at `L1`/`L1` |
| **C-C11 alt. abl6** — C-C11 alternate abl6, §4 `:1805` | (a) | `rc=0`, 261 s, 0.3 GiB peak (`ladder.log:22`) | yes, 261 s <= 90 min (C-Q6) | C-Q6 c1 unrestricted `:5558`, C-Q6 c1 `skI` `:5996`, C-Q6 c1 `skI2` `:6426` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C11 alt. abl6** — C-C11 alternate abl6, §4 `:1805` | (b) | `rc=0`, 237 s, 0.3 GiB peak (`ladder.log:54`) | yes, 237 s <= 90 min (C-Q6) | C-Q6 c1 unrestricted `:5630`, C-Q6 c1 `skI` `:6071`, C-Q6 c1 `skI2` `:6504` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C11 alt. abl6** — C-C11 alternate abl6, §4 `:1805` | (d) | `rc=0`, 3446 s, 5.9 GiB peak (`ladder.log:81`) | yes, 3446 s <= 90 min (C-Q6) | C-Q6 c1 `skI` `:9971`, C-Q6 c1 `skI2` `:10485`, `Accept(S) => IssuerSigned` `:11452` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C12** — C-C12, §4 `:1806` | (a) | `rc=0`, 456 s, 0.3 GiB peak (`ladder.log:26`) | yes, 456 s <= 90 min (C-Q6) | C-Q6 c1 unrestricted `:6262`, C-Q6 c2 `:6968` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C12** — C-C12, §4 `:1806` | (b) | `rc=0`, 453 s, 0.3 GiB peak (`ladder.log:58`) | yes, 453 s <= 90 min (C-Q6) | C-Q6 c1 unrestricted `:6358`, C-Q6 c2 `:7076` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C12** — C-C12, §4 `:1806` | (d) | `rc=0`, 3818 s, 5.9 GiB peak (`ladder.log:83`) | yes, 3818 s <= 90 min (C-Q6) | C-Q6 c2 `:10789`, `Accept(S) => IssuerSigned` `:11635` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C13(i)** — C-C13(i), §9(1) `:2501` | (a) | `rc=0`, 236 s, 0.4 GiB peak (`ladder.log:24`) | yes, 236 s <= 30 min (retained `TypeConfused`) | link 6a `:4042`, `TypeConfused` `:6460` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C13(i)** — C-C13(i), §9(1) `:2501` | (b) | `rc=0`, 218 s, 0.4 GiB peak (`ladder.log:59`) | yes, 218 s <= 30 min (retained `TypeConfused`) | link 6a `:4046`, `TypeConfused` `:6467` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C13(i)** — C-C13(i), §9(1) `:2501` | (d) | `rc=0`, 3419 s, 6.7 GiB peak (`ladder.log:85`) | **no**, 3419 s > 30 min (retained `TypeConfused`) | link 6a `:7600`, `Accept(S) => IssuerSigned` `:11026`, `TypeConfused` `:12376` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C13(ii)** — C-C13(ii), §9(1) `:2501` | (a) | `rc=0`, 634 s, 1.0 GiB peak (`ladder.log:28`) | yes, 634 s <= 30 min (retained `TypeConfused`) | link 6a `:5147`, `TypeConfused` `:8444` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C13(ii)** — C-C13(ii), §9(1) `:2501` | (b) | `rc=0`, 592 s, 1.0 GiB peak (`ladder.log:60`) | yes, 592 s <= 30 min (retained `TypeConfused`) | link 6a `:5169`, `TypeConfused` `:8505` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C13(ii)** — C-C13(ii), §9(1) `:2501` | (d) | `rc=0`, 7794 s, 9.1 GiB peak (`ladder.log:87`) | **no**, 7794 s > 30 min (retained `TypeConfused`) | link 6a `:10560`, `Accept(S) => IssuerSigned` `:15552`, `TypeConfused` `:17767` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C14** — C-C14, §9(1) `:2502` | (a) | `rc=0`, 41003 s, 31.7 GiB peak (`ladder.log:29`) | **no**, 41003 s > 30 min (retained `Accept => IssuerSigned`) | C-Q1 link 1a `:3495`, C-Q1 link 1b `:4727`, C-Q2 `:30492`, C-Q6 c1 unrestricted `:37364`, `Accept(S) => IssuerSigned` `:41388` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C14** — C-C14, §9(1) `:2502` | (b) | `rc=0`, 39596 s, 31.9 GiB peak (`ladder.log:61`) | **no**, 39596 s > 30 min (retained `Accept => IssuerSigned`) | C-Q1 link 1a `:3501`, C-Q1 link 1b `:4739`, C-Q2 `:30584`, C-Q6 c1 unrestricted `:37512`, `Accept(S) => IssuerSigned` `:41570` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C15(i)** — C-C15(i), §9(1) `:2503` | (a) | `rc=0`, 276 s, 0.4 GiB peak (`ladder.log:27`) | yes, 276 s <= 30 min (retained `SignerForged`) | C-Q1 link 1a `:3341`, C-Q1 link 1b `:3889`, C-Q1 link 2a `:4444`, C-Q9 `:5545`, link 3 `:6102`, link 5 `:6729`, C-Q2 `:7722`, C-Q5 `:8571`, `SignerForged` `:10755` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C15(i)** — C-C15(i), §9(1) `:2503` | (b) | `rc=0`, 261 s, 0.4 GiB peak (`ladder.log:63`) | yes, 261 s <= 30 min (retained `SignerForged`) | C-Q1 link 1a `:3342`, C-Q1 link 1b `:3892`, C-Q1 link 2a `:4448`, C-Q9 `:5558`, link 3 `:6116`, link 5 `:6745`, C-Q2 `:7741`, C-Q5 `:8595`, `SignerForged` `:10791` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C15(i)** — C-C15(i), §9(1) `:2503` | (d) | `rc=0`, 7495 s, 12.4 GiB peak (`ladder.log:86`) | **no**, 7495 s > 30 min (retained `SignerForged`) | C-Q1 link 1a `:3263`, C-Q1 link 2a `:3870`, C-Q7 `:9951`, C-Q9 `:10804`, link 3 `:11413`, link 5 `:12268`, link 6b `:13123`, C-Q3 `ReattributedA` `:13785`, C-Q3 `ReattributedB` `:14486`, C-Q4 `Rescoped` `:15148`, C-Q4 `InnerSigTransplanted` `:15850`, C-Q5 `:16563`, C-Q6 c3 `ScopeMisreported` `:19689`, `Accept(S) => IssuerSigned` `:20442`, `SignerForged` `:21714` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C15(ii)** — C-C15(ii), §9(1) `:2503` | (a) | `rc=0`, 270 s, 0.4 GiB peak (`ladder.log:30`) | yes, 270 s <= 45 min (link 6b) | link 6b `:4638`, C-Q4 `Rescoped` `:5484`, C-Q6 c3 `ScopeMisreported` `:7590` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C15(ii)** — C-C15(ii), §9(1) `:2503` | (b) | `rc=0`, 259 s, 0.4 GiB peak (`ladder.log:62`) | yes, 259 s <= 45 min (link 6b) | link 6b `:4652`, C-Q4 `Rescoped` `:5502`, C-Q6 c3 `ScopeMisreported` `:7618` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C15(ii)** — C-C15(ii), §9(1) `:2503` | (d) | `rc=0`, 3941 s, 5.8 GiB peak (`ladder.log:88`) | **no**, 3941 s > 45 min (link 6b) | link 6b `:8365`, C-Q4 `Rescoped` `:9529`, C-Q6 c3 `ScopeMisreported` `:12646`, `Accept(S) => IssuerSigned` `:13296` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C15(iii)** — C-C15(iii), §9(1) `:2503` | (a) | `rc=0`, 318 s, 0.4 GiB peak (`ladder.log:32`) | yes, 318 s <= 45 min (link 6b) | link 6b `:4745`, C-Q4 `Rescoped` `:5577`, C-Q6 c3 `ScopeMisreported` `:7731`, observer `ScopeIdentityOnly` `:8481` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C15(iii)** — C-C15(iii), §9(1) `:2503` | (b) | `rc=0`, 291 s, 0.4 GiB peak (`ladder.log:64`) | yes, 291 s <= 45 min (link 6b) | link 6b `:4777`, C-Q4 `Rescoped` `:5617`, C-Q6 c3 `ScopeMisreported` `:7791`, observer `ScopeIdentityOnly` `:8545` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C15(iii)** — C-C15(iii), §9(1) `:2503` | (d) | `rc=0`, 4154 s, 5.7 GiB peak (`ladder.log:89`) | **no**, 4154 s > 45 min (link 6b) | link 6b `:8495`, C-Q4 `Rescoped` `:9565`, C-Q6 c3 `ScopeMisreported` `:12704`, `Accept(S) => IssuerSigned` `:14378`, observer `ScopeIdentityOnly` `:13731` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C16** — C-C16, §9(3) `:2609` | (a) | `rc=0`, 275 s, 0.3 GiB peak (`ladder.log:31`) | yes, 275 s <= 30 min (retained `Spliced`) | link 5 `:4014`, `Spliced` `:6605` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C16** — C-C16, §9(3) `:2609` | (b) | `rc=0`, 251 s, 0.3 GiB peak (`ladder.log:65`) | yes, 251 s <= 30 min (retained `Spliced`) | link 5 `:4026`, `Spliced` `:6638` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C16** — C-C16, §9(3) `:2609` | (d) | `rc=0`, 6261 s, 8.2 GiB peak (`ladder.log:90`) | **no**, 6261 s > 30 min (retained `Spliced`) | link 5 `:10261`, `Accept(S) => IssuerSigned` `:15027`, `Spliced` `:16433` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C17** — C-C17, §9(4) `:2666` | (a) | `rc=0`, 27085 s, 18.8 GiB peak (`ladder.log:34`) | **no**, 27085 s > 30 min (retained `SignerForged`) | C-Q1 link 2a `:6530`, `Accept(S) => IssuerSigned` `:26679`, `SignerForged` `:28301` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C17** — C-C17, §9(4) `:2666` | (b) | `rc=0`, 25996 s, 18.5 GiB peak (`ladder.log:67`) | **no**, 25996 s > 30 min (retained `SignerForged`) | C-Q1 link 2a `:6551`, `Accept(S) => IssuerSigned` `:26808`, `SignerForged` `:28443` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C17** — C-C17, §9(4) `:2666` | (d) | not run (`ladder.log:91`); ladder 2, history: terminated by memory guard, classified as mechanism failure (memory), 64379 s, 76.6 GiB (`ladder2/ladder.log:95`) | - (not run) | **not run under this blob** — no result | - |
| **C-C18** — C-C18, §9(5) `:2725` | (a) | `rc=0`, 265 s, 0.4 GiB peak (`ladder.log:33`) | yes, 265 s <= 30 min (C-Q10) | C-Q10 `:5384`, C-Q6 c1 unrestricted `:5780`, C-Q6 c1 `skI` `:6176` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C18** — C-C18, §9(5) `:2725` | (b) | `rc=0`, 266 s, 0.3 GiB peak (`ladder.log:66`) | yes, 266 s <= 30 min (C-Q10) | C-Q10 `:5422`, C-Q6 c1 unrestricted `:5819`, C-Q6 c1 `skI` `:6216` | all 14 declared reachable; standing traces at `L1`/`L1` |
| **C-C18** — C-C18, §9(5) `:2725` | (d) | `rc=0`, 3498 s, 5.9 GiB peak (`ladder.log:92`) | **no**, 3498 s > 30 min (C-Q10) | C-Q10 `:9889`, C-Q6 c1 `skI` `:10372`, `Accept(S) => IssuerSigned` `:11556` | all 14 declared reachable; standing traces at `L1`/`L1` |
<!--END-S2-->

## 2a. Every companion, checked against its registration

**How each row was judged.** The registration for a configuration in a case is its §4 / §9 row **as its
Cases cell states it for that case**. The cell governs per case: see §4's preamble (round 8) and C-C15's
*"SET (2) IS READ PER CASE, AND THE CASES LISTS GOVERN"*. Each row gets three mechanical checks:

1. Every red that the Cases cell registers for that case fired. C-Q3's two roles count as one query.
2. **No** safety query or observer went red unless the case's registration registers it red. This
   applies whether the query is a named set-(2) member or simply unnamed. Either way §4's rule makes it a
   broken-fixture-or-finding item.
3. Every declared honest-flow witness and every vocabulary witness is reachable (C-N1,
   `PREDICTIONS.md:1503-1510`). The one exception is the two that the C-C11 Q4 alternate registers
   unreachable, S2 and S4.

In (d), `AcceptS => IssuerSigned` is required red in every run. Where a cell registers a **fork** (C-C4
strict; C-C15(ii) strict), either branch counts as registered, and the row names the branch observed.
Where a cell leaves a member open, the note column names it and either colour is accepted. **AS
REGISTERED** means all three checks pass. **DIVERGENT** lists each failure exactly. Divergences are
**listed, not resolved**. §4: *"a companion failing outside its set, or a witness dying, is a broken
fixture to be diagnosed and recorded, never a finding until the diagnosis distinguishes a broken fixture
from a real consequence of composition"*.

<!--VERDICTS-->
| Companion / configuration (registration) | Case | Required red in this case, per its Cases cell (everything else declared must be green; every witness reachable) | Verdict against §4 / §9 | Divergences, exactly (broken-fixture-or-finding items under §4, listed and not resolved) | Note from the Cases cell |
|---|---|---|---|---|---|
| **C-C1** — C-C1, §4 `:1770` | (c) | `Accept(S) => IssuerSigned`; C-Q1 link 1b | **AS REGISTERED** | none |  |
| **C-C2** — C-C2, §4 `:1771` | (a) | none (green throughout) | **AS REGISTERED** | none | strict: set (1)'s C-Q3 and link 5 registered GREEN (three lists) |
| **C-C2** — C-C2, §4 `:1771` | (b) | none (green throughout) | **AS REGISTERED** | none | as (a), predicted on channel symmetry |
| **C-C2** — C-C2, §4 `:1771` | (d) | C-Q3 `ReattributedA` or C-Q3 `ReattributedB`; link 5; baseline `AcceptS => IssuerSigned` | **not run under this blob** | none: no result to compare |  |
| **C-C3** — C-C3, §4 `:1772` | (a) | C-Q9; link 3 | **AS REGISTERED** | none | strict MIXED: C-Q5 green |
| **C-C3** — C-C3, §4 `:1772` | (b) | C-Q9; link 3 | **AS REGISTERED** | none | as (a), predicted |
| **C-C3** — C-C3, §4 `:1772` | (d) | C-Q5; C-Q9; link 3; baseline `AcceptS => IssuerSigned` | **not run under this blob** | none: no result to compare |  |
| **C-C4** — C-C4, §4 `:1773` | (a) | FORK: {C-Q4 `Rescoped`; C-Q4 `InnerSigTransplanted`; C-Q3 `ReattributedA` or C-Q3 `ReattributedB`; link 6b; link 5} or green throughout | **AS REGISTERED** (fork branch: green throughout) | none | registered FORK: the five reds, or green throughout (predicted configuration-level reading) |
| **C-C4** — C-C4, §4 `:1773` | (b) | FORK: {C-Q4 `Rescoped`; C-Q4 `InnerSigTransplanted`; C-Q3 `ReattributedA` or C-Q3 `ReattributedB`; link 6b; link 5} or green throughout | **AS REGISTERED** (fork branch: green throughout) | none | registered FORK, as (a) |
| **C-C4** — C-C4, §4 `:1773` | (d) | C-Q4 `Rescoped`; C-Q4 `InnerSigTransplanted`; C-Q3 `ReattributedA` or C-Q3 `ReattributedB`; link 6b; link 5; baseline `AcceptS => IssuerSigned` | **not run under this blob** | none: no result to compare |  |
| **C-C5** — C-C5, §4 `:1774` | (a) | C-Q8; link 4 | **DIVERGENT** | **red not registered in this case:** `Accept(S) => IssuerSigned` `:7809`; **red not registered in this case:** `AcceptedUnderHonestKey => IssuerSigned` `:8280` | strict MIXED: `InnerSigTransplanted` descended green |
| **C-C5** — C-C5, §4 `:1774` | (b) | C-Q8; link 4 | **DIVERGENT** | **red not registered in this case:** `Accept(S) => IssuerSigned` `:7601`; **red not registered in this case:** `AcceptedUnderHonestKey => IssuerSigned` `:8065` | strict MIXED, descended |
| **C-C5** — C-C5, §4 `:1774` | (d) | C-Q4 `InnerSigTransplanted`; C-Q8; link 4; baseline `AcceptS => IssuerSigned` | **not run under this blob** | none: no result to compare |  |
| **C-C6** — C-C6, §4 `:1775` | (a) | none (green throughout) | **AS REGISTERED** | none | green control, predicted (round 9 disposition 4) |
| **C-C6** — C-C6, §4 `:1775` | (b) | none (green throughout) | **AS REGISTERED** | none | green control, predicted |
| **C-C6** — C-C6, §4 `:1775` | (d) | C-Q7; C-Q4 `InnerSigTransplanted`; C-Q8; link 4; baseline `AcceptS => IssuerSigned` | **not run under this blob** | none: no result to compare |  |
| **C-C7(i)** — C-C7(i), §4 `:1776` | (a) | C-Q8; link 4; `AcceptedUnderHonestKey => IssuerSigned`; `Accept(S) => IssuerSigned` | **AS REGISTERED** | none |  |
| **C-C7(i)** — C-C7(i), §4 `:1776` | (b) | C-Q8; link 4; `AcceptedUnderHonestKey => IssuerSigned`; `Accept(S) => IssuerSigned` | **AS REGISTERED** | none |  |
| **C-C7(i)** — C-C7(i), §4 `:1776` | (d) | C-Q8; link 4; `AcceptedUnderHonestKey => IssuerSigned`; baseline `AcceptS => IssuerSigned` | **not run under this blob** | none: no result to compare |  |
| **C-C7(ii)** — C-C7(ii), §4 `:1776` | (a) | C-Q8; link 4; `AcceptedUnderHonestKey => IssuerSigned`; `Accept(S) => IssuerSigned` | **AS REGISTERED** | none | C-Q7 GREEN in strict, a registered per-case outcome |
| **C-C7(ii)** — C-C7(ii), §4 `:1776` | (b) | C-Q8; link 4; `AcceptedUnderHonestKey => IssuerSigned`; `Accept(S) => IssuerSigned` | **AS REGISTERED** | none |  |
| **C-C7(ii)** — C-C7(ii), §4 `:1776` | (d) | C-Q8; link 4; C-Q7; `AcceptedUnderHonestKey => IssuerSigned`; baseline `AcceptS => IssuerSigned` | **not run under this blob** | none: no result to compare |  |
| **C-C8** — C-C8, §4 `:1777` | (a) | C-Q9; link 3 | **AS REGISTERED** | none | (beta)-only strict split: C-Q5 and link 5 green |
| **C-C8** — C-C8, §4 `:1777` | (b) | C-Q9; link 3 | **AS REGISTERED** | none | as (a), descended (cap22i) |
| **C-C8** — C-C8, §4 `:1777` | (d) | C-Q9; C-Q5; link 3; link 5; baseline `AcceptS => IssuerSigned` | **not run under this blob** | none: no result to compare |  |
| **C-C8-i** — C-C8-i, §9(2) `:2546` | (a) | none (green throughout) | **AS REGISTERED** | none | isolation result: all green |
| **C-C8-i** — C-C8-i, §9(2) `:2546` | (b) | none (green throughout) | **AS REGISTERED** | none | isolation result: all green |
| **C-C8-i** — C-C8-i, §9(2) `:2546` | (d) | none (green throughout); baseline `AcceptS => IssuerSigned`; left open: link 5 | **not run under this blob** | none: no result to compare | link 5's `mh` half 'stays the registered (d) red' (:2546) is ambiguous for this configuration |
| **C-C8-ii** — C-C8-ii, §9(2) `:2547` | (a) | C-Q9; left open: link 3 | **AS REGISTERED** | none | link 3 not named in the cell; §3 link 3 says its producer 'is C-Q9' (:464) |
| **C-C8-ii** — C-C8-ii, §9(2) `:2547` | (b) | C-Q9; left open: link 3 | **AS REGISTERED** | none | as (a) |
| **C-C8-ii** — C-C8-ii, §9(2) `:2547` | (d) | C-Q9; baseline `AcceptS => IssuerSigned`; left open: link 3 | **not run under this blob** | none: no result to compare | as (a) |
| **C-C9** — C-C9, §4 `:1778` | (a) | link 2b slot-B conj.; `Stripped` | **AS REGISTERED** | none |  |
| **C-C9** — C-C9, §4 `:1778` | (b) | link 2b slot-B conj.; `Stripped` | **AS REGISTERED** | none |  |
| **C-C9** — C-C9, §4 `:1778` | (d) | link 2b slot-B conj.; `Stripped`; baseline `AcceptS => IssuerSigned` | **AS REGISTERED** | none |  |
| **C-C10** — C-C10, §4 `:1779` | (a) | C-Q1 link 1a; C-Q1 link 1b; `Accept(S) => IssuerSigned` | **DIVERGENT** | **red not registered in this case:** C-Q6 c1 unrestricted `:11510` |  |
| **C-C10** — C-C10, §4 `:1779` | (b) | C-Q1 link 1a; C-Q1 link 1b; `Accept(S) => IssuerSigned` | **DIVERGENT** | **red not registered in this case:** C-Q6 c1 unrestricted `:11510` |  |
| **C-C10** — C-C10, §4 `:1779` | (d) | C-Q1 link 1a; baseline `AcceptS => IssuerSigned` | **AS REGISTERED** | none |  |
| **C-C10 isolation control** — C-C10 isolation control, §4 `:1779` | (a) | C-Q1 link 1a | **AS REGISTERED** | none | MIXED control: link 1a red, link 1b green |
| **C-C10 isolation control** — C-C10 isolation control, §4 `:1779` | (b) | C-Q1 link 1a | **AS REGISTERED** | none |  |
| **C-C11** — C-C11 (Q2), §4 `:1805` | (a) | C-Q6 c1 unrestricted; C-Q6 c1 `skI`; C-Q6 c1 `skI2` | **AS REGISTERED** | none |  |
| **C-C11** — C-C11 (Q2), §4 `:1805` | (b) | C-Q6 c1 unrestricted; C-Q6 c1 `skI`; C-Q6 c1 `skI2` | **AS REGISTERED** | none |  |
| **C-C11** — C-C11 (Q2), §4 `:1805` | (d) | C-Q6 c1 `skI`; C-Q6 c1 `skI2`; baseline `AcceptS => IssuerSigned` | **AS REGISTERED** | none | (d) predicted; unrestricted form not asserted |
| **C-C11 alt. Q4** — C-C11 alternate Q4, §4 `:1805` | (a) | C-Q6 c1 unrestricted; C-Q6 c1 `skI`; C-Q6 c1 `skI2`; registered UNREACHABLE: S2, S4 | **AS REGISTERED** | none |  |
| **C-C11 alt. Q4** — C-C11 alternate Q4, §4 `:1805` | (b) | C-Q6 c1 unrestricted; C-Q6 c1 `skI`; C-Q6 c1 `skI2`; registered UNREACHABLE: S2, S4 | **AS REGISTERED** | none |  |
| **C-C11 alt. Q4** — C-C11 alternate Q4, §4 `:1805` | (d) | C-Q6 c1 `skI`; C-Q6 c1 `skI2`; baseline `AcceptS => IssuerSigned`; registered UNREACHABLE: S2, S4 | **AS REGISTERED** | none |  |
| **C-C11 alt. abl6** — C-C11 alternate abl6, §4 `:1805` | (a) | C-Q6 c1 unrestricted; C-Q6 c1 `skI`; C-Q6 c1 `skI2` | **AS REGISTERED** | none |  |
| **C-C11 alt. abl6** — C-C11 alternate abl6, §4 `:1805` | (b) | C-Q6 c1 unrestricted; C-Q6 c1 `skI`; C-Q6 c1 `skI2` | **AS REGISTERED** | none |  |
| **C-C11 alt. abl6** — C-C11 alternate abl6, §4 `:1805` | (d) | C-Q6 c1 `skI`; C-Q6 c1 `skI2`; baseline `AcceptS => IssuerSigned` | **AS REGISTERED** | none |  |
| **C-C12** — C-C12, §4 `:1806` | (a) | C-Q6 c2; C-Q6 c1 unrestricted | **AS REGISTERED** | none | unrestricted form red as the registered consequence (§3 C-Q6 §(6)) |
| **C-C12** — C-C12, §4 `:1806` | (b) | C-Q6 c2; C-Q6 c1 unrestricted | **AS REGISTERED** | none |  |
| **C-C12** — C-C12, §4 `:1806` | (d) | C-Q6 c2; baseline `AcceptS => IssuerSigned` | **AS REGISTERED** | none |  |
| **C-C13(i)** — C-C13(i), §9(1) `:2501` | (a) | link 6a; `TypeConfused` | **AS REGISTERED** | none |  |
| **C-C13(i)** — C-C13(i), §9(1) `:2501` | (b) | link 6a; `TypeConfused` | **AS REGISTERED** | none |  |
| **C-C13(i)** — C-C13(i), §9(1) `:2501` | (d) | link 6a; `TypeConfused`; baseline `AcceptS => IssuerSigned` | **AS REGISTERED** | none |  |
| **C-C13(ii)** — C-C13(ii), §9(1) `:2501` | (a) | link 6a; `TypeConfused` | **AS REGISTERED** | none | per-layer claim (wrapper layers only) not observable: B-2 |
| **C-C13(ii)** — C-C13(ii), §9(1) `:2501` | (b) | link 6a; `TypeConfused` | **AS REGISTERED** | none |  |
| **C-C13(ii)** — C-C13(ii), §9(1) `:2501` | (d) | link 6a; `TypeConfused`; baseline `AcceptS => IssuerSigned` | **AS REGISTERED** | none |  |
| **C-C14** — C-C14, §9(1) `:2502` | (a) | C-Q2; C-Q1 link 1a; C-Q1 link 1b; `Accept(S) => IssuerSigned` | **DIVERGENT** | **red not registered in this case:** C-Q6 c1 unrestricted `:37364` | the spike's one combined formula; 'this file predicts no different answer than all three' |
| **C-C14** — C-C14, §9(1) `:2502` | (b) | C-Q2; C-Q1 link 1a; C-Q1 link 1b; `Accept(S) => IssuerSigned` | **DIVERGENT** | **red not registered in this case:** C-Q6 c1 unrestricted `:37512` |  |
| **C-C15(i)** — C-C15(i), §9(1) `:2503` | (a) | C-Q9; link 3; C-Q1 link 1a; C-Q1 link 1b; C-Q1 link 2a; link 5; C-Q5; `SignerForged`; left open: C-Q6 c3 `ScopeMisreported` | **DIVERGENT** | **red not registered in this case:** C-Q2 `:7722` | strict: the eight (seven relations) descended red; `Rescoped`, `InnerSigTransplanted`, C-Q3, `TypeConfused`, C-Q7, C-Q8 descended green; link 6b not produced in strict; C-Q6 c3 for (i) in strict is not case-assigned (set (1) says both configurations red it; the D11 sentence says the key half is severed by nothing the strict fixture can present) |
| **C-C15(i)** — C-C15(i), §9(1) `:2503` | (b) | C-Q9; link 3; C-Q1 link 1a; C-Q1 link 1b; C-Q1 link 2a; link 5; C-Q5; `SignerForged`; left open: C-Q6 c3 `ScopeMisreported` | **DIVERGENT** | **red not registered in this case:** C-Q2 `:7741` | as (a) |
| **C-C15(i)** — C-C15(i), §9(1) `:2503` | (d) | link 6b; C-Q4 `Rescoped`; C-Q3 `ReattributedA` or C-Q3 `ReattributedB`; link 5; C-Q7; C-Q4 `InnerSigTransplanted`; C-Q6 c3 `ScopeMisreported`; C-Q1 link 1a; C-Q1 link 2a; C-Q5; `SignerForged`; C-Q9; link 3; baseline `AcceptS => IssuerSigned` | **AS REGISTERED** | none | (d): set (1) plus the round-10/11 predicted reds (the eight less link 1b); `InnerSigTransplanted` from set (1)'s set-completeness note |
| **C-C15(ii)** — C-C15(ii), §9(1) `:2503` | (a) | FORK: {link 6b; C-Q4 `Rescoped`; C-Q6 c3 `ScopeMisreported`} or green throughout | **AS REGISTERED** (fork branch: the registered reds) | none | registered FORK, predicted neither way: red if the depth-2 honest route exists, else green throughout |
| **C-C15(ii)** — C-C15(ii), §9(1) `:2503` | (b) | FORK: {link 6b; C-Q4 `Rescoped`; C-Q6 c3 `ScopeMisreported`} or green throughout | **AS REGISTERED** (fork branch: the registered reds) | none | FORK, as (a) |
| **C-C15(ii)** — C-C15(ii), §9(1) `:2503` | (d) | link 6b; C-Q4 `Rescoped`; C-Q6 c3 `ScopeMisreported`; baseline `AcceptS => IssuerSigned` | **AS REGISTERED** | none |  |
| **C-C15(iii)** — C-C15(iii), §9(1) `:2503` | (a) | C-Q4 `Rescoped`; link 6b; C-Q6 c3 `ScopeMisreported`; observer `ScopeIdentityOnly` | **AS REGISTERED** | none |  |
| **C-C15(iii)** — C-C15(iii), §9(1) `:2503` | (b) | C-Q4 `Rescoped`; link 6b; C-Q6 c3 `ScopeMisreported`; observer `ScopeIdentityOnly` | **AS REGISTERED** | none |  |
| **C-C15(iii)** — C-C15(iii), §9(1) `:2503` | (d) | C-Q4 `Rescoped`; link 6b; C-Q6 c3 `ScopeMisreported`; observer `ScopeIdentityOnly`; baseline `AcceptS => IssuerSigned` | **AS REGISTERED** | none |  |
| **C-C16** — C-C16, §9(3) `:2609` | (a) | link 5; `Spliced` | **AS REGISTERED** | none |  |
| **C-C16** — C-C16, §9(3) `:2609` | (b) | link 5; `Spliced` | **AS REGISTERED** | none |  |
| **C-C16** — C-C16, §9(3) `:2609` | (d) | link 5; `Spliced`; baseline `AcceptS => IssuerSigned` | **AS REGISTERED** | none |  |
| **C-C17** — C-C17, §9(4) `:2666` | (a) | C-Q1 link 2a; `SignerForged` | **DIVERGENT** | **red not registered in this case:** `Accept(S) => IssuerSigned` `:26679` | `PossessionTransplanted` (set 1) is not a capstone query: B-3 |
| **C-C17** — C-C17, §9(4) `:2666` | (b) | C-Q1 link 2a; `SignerForged` | **DIVERGENT** | **red not registered in this case:** `Accept(S) => IssuerSigned` `:26808` |  |
| **C-C17** — C-C17, §9(4) `:2666` | (d) | C-Q1 link 2a; `SignerForged`; baseline `AcceptS => IssuerSigned` | **not run under this blob** | none: no result to compare |  |
| **C-C18** — C-C18, §9(5) `:2725` | (a) | C-Q10; C-Q6 c1 `skI`; C-Q6 c1 unrestricted | **AS REGISTERED** | none |  |
| **C-C18** — C-C18, §9(5) `:2725` | (b) | C-Q10; C-Q6 c1 `skI`; C-Q6 c1 unrestricted | **AS REGISTERED** | none |  |
| **C-C18** — C-C18, §9(5) `:2725` | (d) | C-Q10; C-Q6 c1 `skI`; baseline `AcceptS => IssuerSigned` | **AS REGISTERED** | none |  |

**Counts, per case** (one row per configuration file): (a): 21 as registered, 5 divergent, 0 not run under this blob; (b): 21 as registered, 5 divergent, 0 not run under this blob; (c): 1 as registered, 0 divergent, 0 not run under this blob; (d): 13 as registered, 0 divergent, 11 not run under this blob.
<!--END-VERDICTS-->

### The ten divergent rows, against the registration's own words

**No witness died in any landed run, and no registered red failed to fire in any landed run.** Every
divergence is the same kind: **a red where the case's registration has green, or does not name the
query**. There are 12 such `RESULT` lines across 10 configuration-case rows, the same 12 as ladder 2's (after
BF-4) at the lines below. The divergence diagnosis (`proverif/dev/divergences/DIAGNOSIS.md`) classes them:
**G1** (C-C5, C-C17: authorship correspondences missing from the sets) and **G4** (C-Q2 under C-C15(i) in
strict) are amendment-shaped; **G2** (C-C10, C-C14: C-Q6 conjunct 1 unrestricted) is a **finding** for the
reviewer and the author. None is resolved by this file. The ladder-2 diagnosis of G3 (BF-4) and the
superseded C-C15(i) rows are in `proverif/ladder2/RESULTS-ladder2.md`.

| Configuration, case | Red where the case's registration does not register red (`.out` line) | What the registration says of each |
|---|---|---|
| **C-C5**, (a) and (b) | `Accept => IssuerSigned`: `cap_cc05_a.out:7809`, `cap_cc05_b.out:7601`. `AcceptedUnderHonestKey => IssuerSigned`: `cap_cc05_a.out:8280`, `cap_cc05_b.out:8065`. | Neither query is in C-C5's set (1) or set (2) (`PREDICTIONS.md:1774`). The Cases cell descends C-Q8 red in strict and predicts *"every other member of the retained set column"* green. C-Q8 and link 4 fired red as registered, and `InnerSigTransplanted` stayed green as descended. |
| **C-C10**, (a) and (b) | C-Q6 conjunct 1, unrestricted form: `cap_cc10_a.out:11510`, `cap_cc10_b.out:11510`. | **This is a set-(2) green gone red.** C-C10's set (2) for (a) reads *"predicted green, on the same descent: links 2a–6b, C-Q2–C-Q6, C-Q9"*, and (b) reads the same (`:1779`). Links 1a and 1b and `Accept => IssuerSigned` fired red as registered. |
| **C-C14**, (a) and (b) | C-Q6 conjunct 1, unrestricted form: `cap_cc14_a.out:37364`, `cap_cc14_b.out:37512`. | C-Q6 is not named in C-C14's set (1) or set (2) (`:2502`), and set (2) *"descends from nothing"*. C-Q2, links 1a and 1b and `Accept => IssuerSigned` all fired red, which is the registered *"all three"*. |
| **C-C15(i)**, (a) and (b) | C-Q2: `cap_cc15i_a.out:7722`, `cap_cc15i_b.out:7741`. | C-Q2 is not named for (i) in strict (`:2503`); the diagnosis's G4 reads it as implied by the registration's own sentence (amendment-shaped item 2 under *The degraded wave*). All eight registered strict reds fired. C-Q6 conjunct 3 stayed green (`cap_cc15i_a.out:9925`, `cap_cc15i_b.out:9957`), a member the registration leaves open; C-C15(i)'s C-Q6 cells are **withheld from discharge** (third routed question). |
| **C-C17**, (a) and (b) | `Accept => IssuerSigned`: `cap_cc17_a.out:26679`, `cap_cc17_b.out:26808`. | Not named in C-C17's set (1) or set (2) (`:2666`). The strict descent `cap18e` declares no such query. Link 2a and `SignerForged` fired red as registered, and link 2b's three conjuncts stayed green. |

**What can be said without further diagnosis.** Every off-registration red outside C-C15(i) is one of the
two retained authorship correspondences or the unrestricted C-Q6 standing form, and each of those
quantifies over every acceptance. Every divergent file reproduces its ladder-2 `RESULT` lines byte for byte
(*Cross-check*), so **none of these reds is produced or removed by BF-5, BF-6 or BF-7**.

### Observations the registration asks to be recorded, and readings that could be contested

- **C-C3 and C-C8 coincide in the capstone** (§4 note (1), `PREDICTIONS.md:1781-1787`: *"whether their
  capstone sets coincide is recorded as an observation of the run"*). They coincide because the models
  do. `diff cap_cc03_a.pv cap_cc08_a.pv` differs only in the generated header's FILE, MUTATES, SERVES and
  REGISTERED BOX lines. `derive.py` transcribes both registered mutations to the same model text. Their
  `RESULT` streams are identical in (a) and in (b), and both (d) files are not run under this blob (in ladder 2
  both timed out on link 1a). Whether two
  companions registered *"by different routes"* may share one transcription is a question for the
  reviewer.
- **C-C8's isolation discipline** (§9(2)). C-C8-i and C-C8-ii both ran, and are recorded, in (a) and (b).
  C-C8-i is all green, which is the isolation result. C-C8-ii has C-Q9 red with C-Q5 green, so (β), the
  possession message, is severed by the possession removal alone. In strict, C-Q5 stays green under
  C-C8's combined removal too, which is registered. **(α) is therefore observable only in (d), and in (d)
  C-C8, C-C8-i and C-C8-ii are not run under this blob** (in ladder 2: rc=124, rc=143, rc=143).
- **C-C8-ii's link 3** is red beside C-Q9 (`cap_cc08ii_a.out:4210`, `cap_cc08ii_b.out:4220`). The
  configuration's cell names only C-Q9. §3's link-3 section says its producer *"is C-Q9"* (`:464`), and
  recut R-5 fires both events from the one failed check. This file accepts the red as registered by that
  identity. It is named here so that a reader can disagree.
- **C-C10's distinguishing signal works as registered.** In the companion, link 1b is red
  (`cap_cc10_a.out:3505`), which means the honest channel's check was the one deleted. In the isolation
  control, link 1b is green (`cap_cc10iso_a.out:3010`) and link 1a red (`:2861`), which means the
  compromised channel's check was deleted. The (b) runs give the same at the same lines.
- **The registered forks fell as follows.** C-C4 in (a) and (b) is **green throughout**, the green-control
  branch. C-C15(ii) in (a) and (b) is the **red branch**: link 6b, `Rescoped` and C-Q6 conjunct 3 are red
  (`cap_cc15ii_a.out:4638`, `:5484`, `:7590`), so the depth-2 honest route exists in the strict fixture.
- **C-C11's Q4 alternate.** S2 and S4 are unreachable in all three cases, as registered
  (`cap_cc11q4_a.out:11702`, `:12094`; `cap_cc11q4_b.out:11747`, `:12141`; `cap_cc11q4_d.out:18311`,
  `:18909`). Every other witness is reachable.
- **Case (c) carries an unstated red.** The unrestricted C-Q6 conjunct-1 form is red in `cap_cc01_c.out:12621`.
  C-Q6 is not stated for (c) (B-4), so this is recorded and read nowhere. *(REPAIR 2026-10-01, skeptic S-6:
  the divergence diagnosis's G2 and amendment-shaped item 4 below cite this line. That use is **diagnostic
  only**, a trace read to understand G2; it is not a registered reading and no verdict rests on it.)*
- **Still not observable, as written under Blocked:** C-C7(ii)'s honest-filtered C-Q8 (B-1), C-C13(ii)'s
  per-layer assignment (B-2) and C-C17's `PossessionTransplanted` (B-3).

## 3. The discharge matrix, as run

D1-D11 are §2(a)'s eleven cross-model rows; D12 and D13 are §2(c)'s standing-verdict rows, outside the
matrix and outside its count. For each severing companion every case it runs in is shown, together with
whether that case's registration expects the severing key red. **Nothing below is discharged by this
file**: the commit is the author's and the non-author cross-family review is still owed.

<!--S3-->
| Row | Producer query; GREEN in the correct model? (`capstone.out`, case (a)) | Severing companion(s) | The severing key, per case, observed; and whether the registration expects it red in that case |
|---|---|---|---|
| **D1** | S-P3 Q2 `Reattributed` — C-Q3 `ReattributedA` `capstone.out:3899` `is true`; C-Q3 `ReattributedB` `capstone.out:3964` `is true` | C-C2 | `cap_cc02_a`: C-Q3 `ReattributedA` `:4430` green (registered green in this case); C-Q3 `ReattributedB` `:4528` green (registered green in this case); link 5 `:4038` green (registered green in this case)<br>`cap_cc02_b`: C-Q3 `ReattributedA` `:4254` green (registered green in this case); C-Q3 `ReattributedB` `:4341` green (registered green in this case); link 5 `:3906` green (registered green in this case)<br>`cap_cc02_d`: **not run under this blob** (`ladder.log:69`; ladder 2, history: timeout (mechanism-viability failure), 65702 s, 21.8 GiB (`ladder2/ladder.log:64`)) |
| **D2** | S-P3 Q2 `Reattributed` (C-Q4 `Rescoped`) — C-Q4 `Rescoped` `capstone.out:4029` `is true` | C-C4 | `cap_cc04_a`: C-Q4 `Rescoped` `:4413` green (registered FORK: red, or the configuration green throughout)<br>`cap_cc04_b`: C-Q4 `Rescoped` `:4283` green (registered FORK: red, or the configuration green throughout)<br>`cap_cc04_d`: **not run under this blob** (`ladder.log:71`; ladder 2, history: timeout (mechanism-viability failure), 65702 s, 46.9 GiB (`ladder2/ladder.log:63`)) |
| **D3** | S-P3 Q1(ii) chain correspondence — `Accept(S) => IssuerSigned` `capstone.out:5554` `is true` | C-C1 | `cap_cc01_c`: `Accept(S) => IssuerSigned` `:14277` **RED** (registered red) |
| **D4** | link 1b: S-P3 Q1(ii); link 1a: structural — C-Q1 link 1a `capstone.out:2561` `is true`; C-Q1 link 1b `capstone.out:2728` `is true` | C-C1, C-C10 | `cap_cc01_c`: C-Q1 link 1b `:3278` **RED** (registered red); C-Q1 link 1a `:2720` green (registered green in this case)<br>`cap_cc10_a`: C-Q1 link 1b `:3505` **RED** (registered red); C-Q1 link 1a `:3004` **RED** (registered red)<br>`cap_cc10_b`: C-Q1 link 1b `:3505` **RED** (registered red); C-Q1 link 1a `:3004` **RED** (registered red)<br>`cap_cc10_d`: C-Q1 link 1a `:2813` **RED** (registered red) |
| **D5** | **C-Q7** — C-Q7 `capstone.out:3314` `is true` | C-C5 | `cap_cc05_a`: C-Q4 `InnerSigTransplanted` `:5734` green (registered green in this case)<br>`cap_cc05_b`: C-Q4 `InnerSigTransplanted` `:5597` green (registered green in this case)<br>`cap_cc05_d`: **not run under this blob** (`ladder.log:72`; ladder 2, history: terminated by memory guard, classified as mechanism failure (memory), 64899 s, 76.5 GiB (`ladder2/ladder.log:66`, `ladder2/ladder.log:78`)) |
| **D6** | **C-Q8**, structural — C-Q8 `capstone.out:3379` `is true` | C-C7(i), C-C7(ii) | `cap_cc07i_a`: C-Q8 `:9385` **RED** (registered red); link 4 `:10116` **RED** (registered red)<br>`cap_cc07i_b`: C-Q8 `:9393` **RED** (registered red); link 4 `:10127` **RED** (registered red)<br>`cap_cc07i_d`: **not run under this blob** (`ladder.log:74`; ladder 2, history: timeout (mechanism-viability failure), 65702 s, 28.3 GiB (`ladder2/ladder.log:68`))<br>`cap_cc07ii_a`: C-Q8 `:12156` **RED** (registered red); link 4 `:13412` **RED** (registered red)<br>`cap_cc07ii_b`: C-Q8 `:12002` **RED** (registered red); link 4 `:13202` **RED** (registered red)<br>`cap_cc07ii_d`: **not run under this blob** (`ladder.log:75`; ladder 2, history: timeout (mechanism-viability failure), 65702 s, 27.4 GiB (`ladder2/ladder.log:79`)) |
| **D7** | S-P2 `Stripped` / `SignerForged` + Q6 `Spliced` — `Stripped` `capstone.out:5714` `is true`; `SignerForged` `capstone.out:5779` `is true`; `Spliced` `capstone.out:5844` `is true` | C-C9, C-C16, C-C17 | `cap_cc09_a`: link 2b slot-B conj. `:3505` **RED** (registered red); link 5 `:3859` green (registered green in this case); C-Q1 link 2a `:2765` green (registered green in this case)<br>`cap_cc09_b`: link 2b slot-B conj. `:3534` **RED** (registered red); link 5 `:3912` green (registered green in this case); C-Q1 link 2a `:2779` green (registered green in this case)<br>`cap_cc09_d`: link 2b slot-B conj. `:4576` **RED** (registered red); link 5 `:5266` green (registered green in this case); C-Q1 link 2a `:2602` green (registered green in this case)<br>`cap_cc16_a`: link 2b slot-B conj. `:3241` green (registered green in this case); link 5 `:4014` **RED** (registered red); C-Q1 link 2a `:2776` green (registered green in this case)<br>`cap_cc16_b`: link 2b slot-B conj. `:3247` green (registered green in this case); link 5 `:4026` **RED** (registered red); C-Q1 link 2a `:2779` green (registered green in this case)<br>`cap_cc16_d`: link 2b slot-B conj. `:8430` green (registered green in this case); link 5 `:10261` **RED** (registered red); C-Q1 link 2a `:2850` green (registered green in this case)<br>`cap_cc17_a`: link 2b slot-B conj. `:17719` green (registered green in this case); link 5 `:19693` green (registered green in this case); C-Q1 link 2a `:6530` **RED** (registered red)<br>`cap_cc17_b`: link 2b slot-B conj. `:17755` green (registered green in this case); link 5 `:19753` green (registered green in this case); C-Q1 link 2a `:6551` **RED** (registered red)<br>`cap_cc17_d`: **not run under this blob** (`ladder.log:91`; ladder 2, history: terminated by memory guard, classified as mechanism failure (memory), 64379 s, 76.6 GiB (`ladder2/ladder.log:95`)) |
| **D8** | S-P7 `TypeConfused` — `TypeConfused` `capstone.out:5909` `is true` | C-C13(i), C-C13(ii) | `cap_cc13i_a`: link 6a `:4042` **RED** (registered red)<br>`cap_cc13i_b`: link 6a `:4046` **RED** (registered red)<br>`cap_cc13i_d`: link 6a `:7600` **RED** (registered red)<br>`cap_cc13ii_a`: link 6a `:5147` **RED** (registered red)<br>`cap_cc13ii_b`: link 6a `:5169` **RED** (registered red)<br>`cap_cc13ii_d`: link 6a `:10560` **RED** (registered red) |
| **D9** | first-link Q4 `TwoWorldsBroken` — C-Q2 `capstone.out:3834` `is true` | C-C14 | `cap_cc14_a`: C-Q2 `:30492` **RED** (registered red)<br>`cap_cc14_b`: C-Q2 `:30584` **RED** (registered red) |
| **D10** | **C-Q9** — C-Q9 `capstone.out:3444` `is true` | C-C3, C-C8 | `cap_cc03_a`: C-Q5 `:4849` green (registered green in this case); C-Q9 `:3795` **RED** (registered red)<br>`cap_cc03_b`: C-Q5 `:4869` green (registered green in this case); C-Q9 `:3804` **RED** (registered red)<br>`cap_cc03_d`: **not run under this blob** (`ladder.log:70`; ladder 2, history: timeout (mechanism-viability failure), 65703 s, 26.3 GiB (`ladder2/ladder.log:65`))<br>`cap_cc08_a`: C-Q5 `:4849` green (registered green in this case); C-Q9 `:3795` **RED** (registered red)<br>`cap_cc08_b`: C-Q5 `:4869` green (registered green in this case); C-Q9 `:3804` **RED** (registered red)<br>`cap_cc08_d`: **not run under this blob** (`ladder.log:76`; ladder 2, history: timeout (mechanism-viability failure), 65703 s, 29.3 GiB (`ladder2/ladder.log:80`)) |
| **D11** | S-P7 `Rescoped` (link 6b) — link 6b `capstone.out:3769` `is true` | C-C15(i), C-C15(ii), C-C15(iii) | `cap_cc15i_a`: link 6b `:6873` green (registered green in this case)<br>`cap_cc15i_b`: link 6b `:6891` green (registered green in this case)<br>`cap_cc15i_d`: link 6b `:13123` **RED** (registered red)<br>`cap_cc15ii_a`: link 6b `:4638` **RED** (registered FORK: red, or the configuration green throughout)<br>`cap_cc15ii_b`: link 6b `:4652` **RED** (registered FORK: red, or the configuration green throughout)<br>`cap_cc15ii_d`: link 6b `:8365` **RED** (registered red)<br>`cap_cc15iii_a`: link 6b `:4745` **RED** (registered red)<br>`cap_cc15iii_b`: link 6b `:4777` **RED** (registered red)<br>`cap_cc15iii_d`: link 6b `:8495` **RED** (registered red) |
| **D12** | S-STANDING `Established => Designated` — C-Q6 c1 `skI` `capstone.out:5249` `is true` | C-C11 | `cap_cc11_a`: C-Q6 c1 `skI` `:6181` **RED** (registered red)<br>`cap_cc11_b`: C-Q6 c1 `skI` `:6203` **RED** (registered red)<br>`cap_cc11_d`: C-Q6 c1 `skI` `:10394` **RED** (registered red) |
| **D13** | S-STANDING `StandingUnentitled` — C-Q6 c2 `capstone.out:5392` `is true` | C-C12 | `cap_cc12_a`: C-Q6 c2 `:6968` **RED** (registered red)<br>`cap_cc12_b`: C-Q6 c2 `:7076` **RED** (registered red)<br>`cap_cc12_d`: C-Q6 c2 `:10789` **RED** (registered red) |
<!--END-S3-->

**Rows with no observed severing in any case.** Every producer query is green in the correct model. Four
rows have no severing companion that went red in **any** case run. In each one the registration puts the
consumer's red in **(d) only**, or, for D2, leaves strict as a fork that fell on its green branch, and the (d)
file is not run under this blob:

- **D1.** C-C2 is registered green in strict; `cap_cc02_d` is not run (ladder 2: timed out).
- **D2.** C-C4 fell on its green strict branch; `cap_cc04_d` is not run (ladder 2: timed out).
- **D5.** C-C5's `InnerSigTransplanted` is descended green in strict; `cap_cc05_d` is not run (ladder 2:
  memory failure).
- **D10.** §A3.3 requires a broken companion that *“fails the query consuming the severed link”*
  (`docs/phase-0-prereg-amendment-3.md:223`). D10's consuming query is C-Q5 `SetAltered`, and its producer is
  C-Q9 (`PREDICTIONS.md:640`). **C-Q5 is green in every landed run of D10's severing companions**: C-C3 and
  C-C8 in (a) and (b) (`cap_cc03_a.out:4849`, `cap_cc03_b.out:4869`, `cap_cc08_a.out:4849`,
  `cap_cc08_b.out:4869`) and C-C8's two isolation configurations (`cap_cc08i_a.out:4149`,
  `cap_cc08i_b.out:4169`, `cap_cc08ii_a.out:4860`, `cap_cc08ii_b.out:4880`). Every (d) file of them is not run.
  C-Q9's red in (a) and (b) is the **producer's** query going red under its own companion: it shows the
  producer severed, not the consumer failing. **So D10's consuming-query requirement is unmet in every
  case.** (C-Q5 is red in the ladder only under C-C15(i), in all three cases — `cap_cc15i_a.out:8571`,
  `cap_cc15i_b.out:8595`, `cap_cc15i_d.out:16563` — where it is registered red. C-C15(i) is D11's severing
  companion, not D10's, and this file does not read that red as D10's.)

**D6** is severed in (a) and (b) only (both (d) configurations are not run). **D7's membership half** (C-C17)
is severed in (a) and (b) only; `cap_cc17_d` is not run (its ladder-2 run, a memory failure, printed link 2a
red before the guard fired: *The degraded wave*). Every other row is severed in every case it runs in.

**C-Q6 under ladder 3.** C-Q6 now ranges over innermost layers only (BF-5), and no C-Q6 colour moved between
ladder 2 and ladder 3 in any file (*Cross-check*). For **D11**, C-C15(i)'s C-Q6 cells are **withheld from
discharge** pending the third routed question; D11's link-6b half does not involve the standing key. For
**D12** and **D13** (C-C11, C-C12) the severing reds stand as tabled, over innermost layers.

### Which box reading each severing depends on

Section 0 records two readings of a companion's box. **(P)**, the per-case-sum reading, gives every run the
sum of its case's boxes, 71 100 s strict and 65 700 s degraded; that is what the ladder enforced, and every
landed run is inside it. **(Q)**, the predicted-red-box reading, gives a companion the box of the query it is
predicted to red (§3's table, `PREDICTIONS.md:1586-1595`; the assignments in words at `:1867-1876` and
`:2590`). **Per-query time is not logged**: ProVerif's output carries no timestamps and `ladder.log` records
one wall clock per run. A whole-run time is an upper bound on each query's, so a run that finished inside a
box shows its query did; a run longer than the box shows nothing either way. Under (Q) such a run is
therefore **“not shown inside its box”**, never “shown outside it”. Seconds are ladder 3's `ladder.log` (line
in parentheses). Only runs that carry the row's severing, or that were the row's chance to, are listed.

| Row | Severing companion, case: seconds (`ladder.log` line) and what it shows | The predicted-red query carrying the severing, and its box | (P) per-case sum | (Q) predicted-red box |
|---|---|---|---|---|
| **D1** | C-C2 (a) 512 s (`:11`), (b) 429 s (`:38`): no red, registered green in strict. (d) not run (`:69`). | C-Q3, 45 min; link 5, 60 min | **no severing observed** | **no severing observed** |
| **D2** | C-C4 (a) 413 s (`:10`), (b) 374 s (`:37`): the fork fell on its green branch. (d) not run (`:71`). | C-Q4 `Rescoped`, 60 min | **no severing observed** | **no severing observed** |
| **D3** | C-C1 (c) 4 569 s (`:94`): `Accept(S) ⟹ IssuerSigned` red. | retained query, 30 min (1 800 s) | stands | **not shown inside its box** |
| **D4** | C-C1 (c) 4 569 s (`:94`): link 1b red. C-C10 (a) 4 012 s (`:20`), (b) 3 654 s (`:55`): links 1a and 1b red; (d) 2 908 s (`:80`): link 1a red. | links 1a and 1b, 45 min (2 700 s) | stands in (a), (b), (c), (d) | **not shown inside its box in any case** |
| **D5** | C-C5 (a) 485 s (`:12`), (b) 452 s (`:39`): `InnerSigTransplanted` registered green in strict. (d) not run (`:72`). | C-Q4 `InnerSigTransplanted`, 60 min | **no severing observed** | **no severing observed** |
| **D6** | C-C7(i) (a) 2 196 s (`:14`), (b) 2 199 s (`:41`); C-C7(ii) (a) 9 512 s (`:17`), (b) 10 549 s (`:44`): C-Q8 and link 4 red. Both (d) files not run (`:74`, `:75`). | C-Q8, 60 min (3 600 s); link 4, 45 min (2 700 s) | stands in (a), (b) | **stands** in (a), (b) (by C-C7(i)); (d) not run |
| **D7**, completeness (`Stripped`) | C-C9 (a) 240 s (`:18`), (b) 246 s (`:45`), (d) 1 323 s (`:79`): link 2b slot-B and `Stripped` red. | link 2b, 60 min — *“as C-C9 runs inside link 2b's”* (`:1875`) | stands in (a), (b), (d) | **stands** in (a), (b), (d) |
| **D7**, common content (`Spliced`) | C-C16 (a) 275 s (`:31`), (b) 251 s (`:65`), (d) 6 261 s (`:90`): link 5 and `Spliced` red. | link 5, 60 min (3 600 s) (`:1874`) | stands in (a), (b), (d) | stands in (a), (b); **(d) not shown inside its box** |
| **D7**, membership (`SignerForged`) | C-C17 (a) 27 085 s (`:34`), (b) 25 996 s (`:67`): link 2a and `SignerForged` red. (d) not run (`:91`). | link 2a, 45 min (2 700 s) (`:1873`) | stands in (a), (b) | **not shown inside its box in any case** |
| **D8** | C-C13(i) (a) 236 s (`:24`), (b) 218 s (`:59`), (d) 3 419 s (`:85`); C-C13(ii) (a) 634 s (`:28`), (b) 592 s (`:60`), (d) 7 794 s (`:87`): link 6a and `TypeConfused` red. | link 6a, 45 min (2 700 s); `TypeConfused` 30 min | stands in (a), (b), (d) | stands in (a), (b); **(d) not shown inside its box** |
| **D9** | C-C14 (a) 41 003 s (`:29`), (b) 39 596 s (`:61`): C-Q2 red. | C-Q2, 45 min (2 700 s) | stands in (a), (b) | **not shown inside its box in any case** |
| **D10** | C-C3 (a) 269 s (`:9`), (b) 267 s (`:36`); C-C8 (a) 264 s (`:15`), (b) 256 s (`:42`): the producer C-Q9 red, the **consumer C-Q5 green**. Both (d) files not run (`:70`, `:76`). | consumer C-Q5, 45 min (`:2590`: C-C3 runs inside C-Q5's box); producer C-Q9, 60 min | **consuming-query severing observed in no case**; C-Q9's red inside the box | the same |
| **D11** | C-C15(i) (a) 276 s (`:27`), (b) 261 s (`:63`): link 6b registered green; (d) 7 495 s (`:86`): red. C-C15(ii) (a) 270 s (`:30`), (b) 259 s (`:62`), (d) 3 941 s (`:88`); C-C15(iii) (a) 318 s (`:32`), (b) 291 s (`:64`), (d) 4 154 s (`:89`): link 6b red. | link 6b, 45 min (2 700 s) | stands in (a), (b), (d) | stands in (a), (b) (by (ii) and (iii)); **(d) not shown inside its box** (3 941-7 495 s) |
| **D12** | C-C11 (a) 291 s (`:23`), (b) 268 s (`:56`), (d) 4 248 s (`:84`): C-Q6 conjunct 1 `skI` red; its two alternates the same, 237-3 710 s. | C-Q6, 90 min (5 400 s) | stands in (a), (b), (d) | **stands** in (a), (b), (d) |
| **D13** | C-C12 (a) 456 s (`:26`), (b) 453 s (`:58`), (d) 3 818 s (`:83`): C-Q6 conjunct 2 red. | C-Q6, 90 min (5 400 s) | stands in (a), (b), (d) | **stands** in (a), (b), (d) |

**The effect, summarised.** Under **(P)** every observed severing stands. Under **(Q)**:
- **not shown inside the box in any case:** D3, D4, D9 and D7's membership half — four rows or row halves;
- **shown inside the box in strict, not in (d):** D7's common-content half, D8 and D11 — their (d) runs took
  6 261 s, 3 419-7 794 s and 3 941-7 495 s against 45- or 60-minute boxes;
- **shown inside the box in strict, (d) not run:** D6 (by C-C7(i), 2 196 and 2 199 s);
- **shown inside the box in every case run:** D7's completeness half, D12, D13;
- **no consuming-query severing under either reading:** D1, D2, D5 and D10, the rows option (i) of the
  first routed question concerns.

*(Changed from ladder 2, 2026-10-06: **D6** moved from “not shown inside its box in any case” to “stands in
(a), (b)”. C-C7(i), now carrying BF-7, ran 2 196 and 2 199 s under ladder 3 against 12 423 and 6 139 s under
ladder 2 (`ladder2/ladder.log:14`, `:41`), with the same verdicts. No other row's (Q) cell changed.)*

Which reading governs is routed to the author (*ROUTED TO THE AUTHOR — second question*).

<!--END-RESULTS-TABLES-->

---

## Cross-check: every ladder-2 run against ladder 3

Ladder 3 changes the correct model (BF-5, BF-6) and C-C7(i)'s files (BF-7). The check compares, for all 80
files, ladder 2's `RESULT` stream (`proverif/ladder2/<file>.out`, the BF-4 re-runs for `cap_cc15i_*`) against
ladder 3's, byte for byte, and then **per keyed query**: every `RESULT` line is keyed as in section 1 and the
two ladders' verdicts are compared key by key. A changed verdict would be attributed to BF-5/BF-6 (a C-Q6 key
or one of the two standing witnesses, in any file) or to BF-7 (a `cap_cc07i_*` file), and otherwise flagged
**UNEXPLAINED**. Generated by `dev/assemble_l3.py` (per-file table also in `dev/l3/crosscheck.tsv`). The
ladder-1 → ladder-2 cross-check (49 identical, 7 prefix-consistent, 0 differences) is in
`proverif/ladder2/RESULTS-ladder2.md`.

<!--CROSSCHECK-->
*No file is in the exception table: every file is either identical or not run.*

**Identical byte for byte, every keyed verdict the same (69 files, 3207 verdicts):** `cap_cc01_c`, `cap_cc02_a`, `cap_cc02_b`, `cap_cc03_a`, `cap_cc03_b`, `cap_cc04_a`, `cap_cc04_b`, `cap_cc05_a`, `cap_cc05_b`, `cap_cc06_a`, `cap_cc06_b`, `cap_cc07i_a`, `cap_cc07i_b`, `cap_cc07ii_a`, `cap_cc07ii_b`, `cap_cc08_a`, `cap_cc08_b`, `cap_cc08i_a`, `cap_cc08i_b`, `cap_cc08ii_a`, `cap_cc08ii_b`, `cap_cc09_a`, `cap_cc09_b`, `cap_cc09_d`, `cap_cc10_a`, `cap_cc10_b`, `cap_cc10_d`, `cap_cc10iso_a`, `cap_cc10iso_b`, `cap_cc11_a`, `cap_cc11_b`, `cap_cc11_d`, `cap_cc11abl6_a`, `cap_cc11abl6_b`, `cap_cc11abl6_d`, `cap_cc11q4_a`, `cap_cc11q4_b`, `cap_cc11q4_d`, `cap_cc12_a`, `cap_cc12_b`, `cap_cc12_d`, `cap_cc13i_a`, `cap_cc13i_b`, `cap_cc13i_d`, `cap_cc13ii_a`, `cap_cc13ii_b`, `cap_cc13ii_d`, `cap_cc14_a`, `cap_cc14_b`, `cap_cc15i_a`, `cap_cc15i_b`, `cap_cc15i_d`, `cap_cc15ii_a`, `cap_cc15ii_b`, `cap_cc15ii_d`, `cap_cc15iii_a`, `cap_cc15iii_b`, `cap_cc15iii_d`, `cap_cc16_a`, `cap_cc16_b`, `cap_cc16_d`, `cap_cc17_a`, `cap_cc17_b`, `cap_cc18_a`, `cap_cc18_b`, `cap_cc18_d`, `capstone`, `capstone_b`, `capstone_d`.

**Not run under ladder 3 (11 files):** `cap_cc02_d`, `cap_cc03_d`, `cap_cc04_d`, `cap_cc05_d`, `cap_cc06_d`, `cap_cc07i_d`, `cap_cc07ii_d`, `cap_cc08_d`, `cap_cc08i_d`, `cap_cc08ii_d`, `cap_cc17_d`.

**Tally, per file:** 69 identical byte for byte, 0 identical after normalisation, 0 different, 0 new, 11 not run under ladder 3. **Per query** (files landed in both): 3207 verdicts the same, 0 changed, 0 new, 0 gone. **No verdict changed, so none needs a BF to explain it, and none is UNEXPLAINED.**
<!--END-CROSSCHECK-->

**Result.**

- **69 of 69** files that landed in ladder 2 landed in ladder 3 and are **identical byte for byte**: 3 207
  keyed query verdicts, **0 changed, 0 new, 0 gone**. That includes the four correct-form runs, both C-C7(i)
  strict files (BF-7) and every C-Q6 and standing-witness line in every file (BF-5, BF-6).
- **11** files are not run under ladder 3; their ladder-2 outcome (no result) is history.
- **No new file**, and no `cannot be proved` anywhere in ladder 3.

**So the expected changes are where BF-5/6/7 bite, and none of them is a verdict:** the standing witnesses'
printed traces moved from `L0` (ladder 2, F-2) to `L1` in all 69 landed files (BF-6; `dev/l3/witness_layers.tsv`),
C-Q6 now ranges over innermost layers only (BF-5) with every colour unchanged, and C-C7(i) now carries the
family's frame pattern (BF-7) with every colour unchanged. **Changed verdicts: 0. Explained: 0. UNEXPLAINED:
0.** `RESULT` line *numbers* moved in every file (the new comment blocks and different traces); every
ladder-3 citation in this file is ladder 3's, and the line map is `dev/l3/linemap.tsv`.

---

## The degraded wave: eleven mechanism failures, and a disposal routed to the author

**Under ladder 3 the eleven are not run under this blob** (`ladder.log:69-78`, `:91`; the owner instance's
disposition: the BF-5/6/7 repairs do not touch the envelope saturation the degraded diagnosis located).
**Everything below, up to the first routed question, is ladder-2 history**: in it `ladder.log` means
`proverif/ladder2/ladder.log`, every `.out` line is in `proverif/ladder2/`, and `mem_guard_vm.log` is
`proverif/ladder2/mem_guard_vm.log`.

**What happened.** Of the 24 case-(d) companion files, **13 landed and 11 did not**. Every failure is in
case (d), and every strict file landed. The degraded correct-form run `capstone_d` landed (6 388 s,
6.1 GiB, `ladder.log:7`), so these are companion failures, not a failure of the degraded model.

| File | `ladder.log` | Outcome | Seconds, peak | The query it was on when it ended (last `-- Query` header) |
|---|---|---|---|---|
| `cap_cc02_d` (C-C2) | `:64` | **timeout (mechanism-viability failure)** | 65 702 s, 21.8 GiB | link 1a (`cap_cc02_d.out:2357`), the first query |
| `cap_cc03_d` (C-C3) | `:65` | **timeout (mechanism-viability failure)** | 65 703 s, 26.3 GiB | link 1a (`:2351`) |
| `cap_cc04_d` (C-C4) | `:63` | **timeout (mechanism-viability failure)** | 65 702 s, 46.9 GiB | link 2b slot-A conjunct (`:14785`) |
| `cap_cc05_d` (C-C5) | `:66`, `:78` | **terminated by memory guard, classified as mechanism failure (memory)**; the `MECHFAIL-MEMORY` line records the marker that kept it from being re-run unablated | 64 899 s, 76.5 GiB | link 2b one-signer conjunct (`:7673`) |
| `cap_cc06_d` (C-C6) | `:67` | **timeout (mechanism-viability failure)** | 65 702 s, 25.8 GiB | link 1a (`:2387`) |
| `cap_cc07i_d` (C-C7(i)) | `:68` | **timeout (mechanism-viability failure)** | 65 702 s, 28.3 GiB | link 1a (`:2387`) |
| `cap_cc07ii_d` (C-C7(ii)) | `:79` | **timeout (mechanism-viability failure)** | 65 702 s, 27.4 GiB | link 1a (`:2387`) |
| `cap_cc08_d` (C-C8) | `:80` | **timeout (mechanism-viability failure)** | 65 703 s, 29.3 GiB | link 1a (`:2351`) |
| `cap_cc08i_d` (C-C8-i) | `:83` | **terminated by memory guard, classified as mechanism failure (memory)** | 48 680 s, 76.5 GiB | link 2b one-signer conjunct (`:6091`) |
| `cap_cc08ii_d` (C-C8-ii) | `:82` | **terminated by memory guard, classified as mechanism failure (memory)** | 39 900 s, 76.6 GiB | link 2b one-signer conjunct (`:6751`) |
| `cap_cc17_d` (C-C17) | `:95` | **terminated by memory guard, classified as mechanism failure (memory)** | 64 379 s, 76.6 GiB | link 2b one-signer conjunct (`:5434`) |

The guard's four triggers are in `mem_guard_vm.log:10972` (`cap_cc05_d`), `:16282` (`cap_cc08ii_d`),
`:16574` (`cap_cc08i_d`) and `:19267` (`cap_cc17_d`). Each fired on the per-process rule, resident set
above 80 000 000 kB, and never on the available-memory rule.
*(REPAIR 2026-10-01, skeptic S-5.)* **The rule and the classification are the owner instance's, and each
termination was made with memory to spare.** The registration boxes time only; classifying `rc=143` as a
mechanism failure is the clerk disposition written into `mem_guard_vm.sh`'s header (`:10-15`: *“classified in
RESULTS.md as MECHANISM FAILURE (memory), the registration boxing TIME and not MEMORY”*). At the four triggers
the guest had, by the guard's own line:

| Run | Guard line | Guest `totalMB` | `availMB` at the trigger | Box spent / left |
|---|---|---|---|---|
| `cap_cc05_d` | `mem_guard_vm.log:10972` | 155 473 | 15 509 | 64 899 s of 65 700 (98.8 % spent) |
| `cap_cc08ii_d` | `:16282` | 170 731 | 16 487 | 39 900 s (25 800 s, 39.3 %, left) |
| `cap_cc08i_d` | `:16574` | 119 817 | 32 069 | 48 680 s (17 020 s, 25.9 %, left) |
| `cap_cc17_d` | `:19267` | 124 907 | 39 103 | 64 379 s of 65 700 (98.0 % spent) |

For `cap_cc05_d` and `cap_cc17_d` the classification changes nothing in practice: under 2 % of the box was
left. `cap_cc08ii_d` and `cap_cc08i_d` were stopped with 26-39 % of their box unspent; they are C-C8's two
isolation configurations (§9(2)) and bear on no matrix row directly. Whether they are re-run with the guard
raised is set out under *ROUTED TO THE AUTHOR*. *(A discrepancy in the record, noted and
not corrected: the `MECHFAIL-MEMORY` note at `ladder.log:78` dates `cap_cc05_d`'s `rc=143` to
"2026-09-27". The guard log dates the SIGTERM to 2026-09-28T13:01:30Z. The run had started about
64 899 s earlier, around 2026-09-27T19:00Z, so the note dates the run and not the termination.)*

**Partial lines printed before the end.** These are recorded, and **no cell in sections 1-3 is filled
from them**. This follows this file's standing rule that no result comes from a killed run (*Ladder
restarts*, "Runs killed, and what was done with them"). Whether a `RESULT` line printed before a mechanism
failure may count is for the author to decide. It would bear only on D7's membership half in (d), where
`cap_cc17_d` printed its registered red, link 2a, before the guard fired.

<!--PARTIALS-->
- `cap_cc02_d` (ladder 2, timeout): no RESULT line before the run ended
- `cap_cc03_d` (ladder 2, timeout): no RESULT line before the run ended
- `cap_cc04_d` (ladder 2, timeout): C-Q1 link 1a `ladder2/cap_cc04_d.out:3676` `is true`, C-Q1 link 2a `ladder2/cap_cc04_d.out:4990` `is true`, link 2b one-signer conj. `ladder2/cap_cc04_d.out:14784` `is true`
- `cap_cc05_d` (ladder 2, memory): C-Q1 link 1a `ladder2/cap_cc05_d.out:5020` `is true`, C-Q1 link 2a `ladder2/cap_cc05_d.out:7672` `is true`
- `cap_cc06_d` (ladder 2, timeout): no RESULT line before the run ended
- `cap_cc07i_d` (ladder 2, timeout): no RESULT line before the run ended
- `cap_cc07ii_d` (ladder 2, timeout): no RESULT line before the run ended
- `cap_cc08_d` (ladder 2, timeout): no RESULT line before the run ended
- `cap_cc08i_d` (ladder 2, memory): C-Q1 link 1a `ladder2/cap_cc08i_d.out:4220` `is true`, C-Q1 link 2a `ladder2/cap_cc08i_d.out:6090` `is true`
- `cap_cc08ii_d` (ladder 2, memory): C-Q1 link 1a `ladder2/cap_cc08ii_d.out:4559` `is true`, C-Q1 link 2a `ladder2/cap_cc08ii_d.out:6750` `is true`
- `cap_cc17_d` (ladder 2, memory): C-Q1 link 1a `ladder2/cap_cc17_d.out:3739` `is true`, C-Q1 link 2a `ladder2/cap_cc17_d.out:5433` `is false`
<!--END-PARTIALS-->

The three runs interrupted by the 2026-09-28 host crash (`cap_cc07ii_d`, `cap_cc08_d`, `cap_cc08i_d`,
about six hours into their boxes, with no `rc`) are **not** results and are not counted in the ceiling.
Their partial outputs are kept as `*.interrupted-by-host-crash.out`, and all three were re-run in full
(rows above).

**The diagnosis, summarised** (`proverif/dev/abl_d/REPORT.md` §(a); scratch, one run at a time under a
10 GiB cap, not a result). In (d) the sole authority key is public, so check 1 accepts any tuple the
attacker mints. That includes a two-signer tuple whose slot-B fingerprint belongs to a `dsks`-derived
key. Each failing companion of the first six deletes exactly the check that denied such a key a borrowed
honest signature: the frame pin and `mh` (C-C2), the inner pin (C-C4), or the byte binding (C-C5, C-C6,
C-C7(i)). C-C3, and C-C8 with it, open a second route through fingerprint-only honest possession. The
report's words: *"The degraded delta removes the bound on tuples; the mutation removes the bound on keys.
Either alone is finite; together they are not."* Measured in verbose traces, 85 % and 84 % of the
saturated clauses carry a `dsks` term in `cc02_d` and `cc05_d`, against 1 % in `capstone_d`. Companions
whose mutation reaches `WrapStage` stall on link 1a. Those confined to `AttestStage` pass links 1a and 2a
and die on the first goal with a structured `authTuple` (link 2b). The report itself calls this *"an
explanation fitted to these observations"*. **The five later failures fit it only in part.** C-C7(ii)
and C-C8 stall on link 1a, as the split predicts. C-C8-i, C-C8-ii and C-C17 each mutate **both**
`AttestStage` and `WrapStage`. By `diff capstone_d.pv cap_<c>_d.pv` the edits fall at `capstone_d.pv`
lines 578-611 and 674-711 for C-C8-i, 580-618 and 676-718 for C-C8-ii, and 607 and 705 for C-C17,
against `AttestStage` at `:564` and `WrapStage` at `:659`. Yet all three passed links 1a and 2a and died
on link 2b's one-signer conjunct. C-C8-ii opens the honest-possession route that the diagnosis assigns
to C-C3 and C-C8, and C-C8-i was diagnosed as opening *neither* route (§(a)). The diagnosis as written
does not account for these three.

**§3's two disposals, tried** (`abl_d` §(c), §(e), §(f)):

- **Change of tactic.** No sound setting lands the isolated `cc02_d` link 1a within the box and the
  10 GiB cap. The baseline A0 already carries recut R-9's `Term` and times out. Four more settings were
  tried: the default `TermMaxsize` (ladder 1), `redundantHypElim`, `nounif` on `fp(pk(*k))`, and `nounif`
  narrowed to `dsks` fingerprints (§(e)).
- **Ablation, in §3's order** (`PREDICTIONS.md:301-303`). Step 1 lands `cc02_d`'s link 1a in isolation
  (2 418 s), but the whole file has **no admissible break point**: at step 1 the one-signer conjunct of
  link 2b runs out of memory, it does so again at steps 1-2 and 1-3, and step 4 lands it only by deleting
  the mutation (F1234 is identical to the ablated control). `cc05_d`'s conjunct 1 breaks only at step 4
  (§(c)). Ablation also collides with C-N1. Step 1 alone kills `HonestChain(L2)`, and steps 1-4 kill six
  honest-flow witnesses even in the ablated control, so any ablated run is a broken fixture under C-N1 as
  frozen (§(f) items 1 and 4).
- **The registration has no third disposal** (§(f) item 7). §3 registers a timeout as *"mechanism-viability
  failure, evidence about the tool or the encoding and **never** about the property, disposed by ablation
  or a change of tactic"* (`:297-300`).

**The prediction, scored.** `DEGRADED-WAVE-PREDICTION-2026-09-29.md` was written before the eighteen
remaining degraded runs launched (`ladder.log:71`).

| Predicted | Observed |
|---|---|
| *"Likely to time out"*: C-C7(ii), C-C8, C-C8(ii), C-C17 | **All four failed.** C-C7(ii) and C-C8 timed out at the box; C-C8(ii) and C-C17 were terminated by the memory guard. The mode was right for two and the failure was right for all four. |
| *"May land as `capstone_d` did"*: the standing, type and scope mutations, C-C9 through C-C18 (other than C-C17) | **All thirteen landed**, in 1 377 s to 7 942 s: C-C9, C-C10, C-C11 and its two alternates, C-C12, C-C13(i)/(ii), C-C15(i)/(ii)/(iii), C-C16, C-C18. |
| No prediction for `cap_cc08i_d` | **Failed**: terminated by the guard on link 2b's one-signer conjunct. |

Score: 17 of 17 predicted dispositions held, counting land or fail. The predicted mode, *time out*,
held for 2 of the 4 failures. The one configuration left unpredicted failed.
*(REPAIR 2026-10-01, skeptic S-9.)* Two qualifications. First, the thirteen were predicted only as *“may
land”*, which is hedged: it would not have been falsified by a failure, so counting the thirteen landings as
predictions that held overstates the score. The unhedged part is the four *“likely to time out”*, all of
which failed. (The prediction's *“C-C9 through C-C18”* also contains C-C17, which its *“likely to time out”*
list names; the table above reads C-C17 under the latter.) Second, *“written before”* rests on a file
timestamp alone. The file is untracked. Its heading says *“2026-09-29 04:30 UTC”*; its modification time is
2026-09-29T04:26:12.93Z (`stat`), 1.1 s before the launch comment at `ladder.log:71` (04:26:14Z). The
heading's 04:30 is later than both and is not the time of writing.

### ROUTED TO THE AUTHOR — the disposal of the eleven degraded mechanism failures

**The question.** Eleven case-(d) companion configurations have no result: C-C2, C-C3, C-C4, C-C5,
C-C6, C-C7(i), C-C7(ii), C-C8, C-C8-i, C-C8-ii and C-C17. §3 disposes of a timeout by ablation or a
change of tactic. The tactics and ablations tried (`abl_d` §(c), §(e), §(f)) did not resolve the sampled
failures without unacceptable witness or mutation loss; that is not shown for all eleven, and it is not an
impossibility result *(restated 2026-10-01, cross-family finding 6; the withdrawn words: “The diagnosis shows
that neither disposes of these”)*. The registration has no third disposal. **What rides on it:** D1, D2, D5 and D10's (α) half have no observed
severing in any case without these runs (section 3), and D6 and D7's membership half are severed in strict
only. *(REPAIR 2026-10-01, skeptic S-7 and S-4: for D10 the whole consuming-query requirement is unmet in
every case, not an “(α) half” — C-Q5 is green in every landed run of C-C3, C-C8 and C-C8's isolation
configurations (section 3, the repair note under* Rows with no observed severing*). And under the
predicted-red-box reading four further rows or row halves (D3, D4, D9, D7's membership half) rest on runs
not shown inside their box in any case; that is the second routed question below.)* The options are laid out below with their costs. **The builder makes no recommendation; the owner
instance will add its own.**

- **(i) Carry the eleven degraded seams as exposed and undischarged in case (d), resting on the
  family-level evidence, by amendment.** Each affected Cases cell already cites a degraded family run as
  its (d) descent (for example `m4_framepin_mh`, `s4_innerfp_mh`, `s1_sig_unbound`, `d5d`, `d6e`/`d6d`/`cap7b`,
  `d10b`, `cap2`/`cap3`, `cap13b`), and those runs would stand in for the capstone's own. *Cost:* one
  amendment and no solver time. *What it gives up:* the capstone's composed (d) evidence for those eleven
  configurations, and with it any capstone severing of D1, D2, D5 and D10 (α). *(REPAIR 2026-10-01, skeptic
  S-7: stated plainly, D10's consuming query C-Q5 is green in every landed run of its severing companions,
  so for D10 option (i) concedes the **whole** consuming-query requirement in every case, not a half. Option
  (i) concedes the same for D1, D2 and D5. If the predicted-red-box reading governs (second question), it
  leaves D3, D4, D9 and D7's membership half on runs not shown inside their box as well.)*
- **(ii) Amend §3 to name ablation's witness consequences, and re-run at step 1 where the case-(d) red
  stays observable.** `abl_d` §(f) item 2 says step 1 keeps L0→L1 and leaves the (d) reds of C-C2 through
  C-C7(i) structurally observable, because each descends from a family model of depth ≤ 1. That is six of
  the eleven. Step 1 is not neutral wave-wide: it breaks C-C15(ii) and C-C13(ii), which need depth 2, but
  both of those landed unablated in (d) and need no ablation. `abl_d` says nothing about C-C7(ii), C-C8,
  C-C8-i, C-C8-ii and C-C17, which failed after it was written. Their (d) descents are likewise S-P1 or
  S-P2 models without a wrapper, but that is the builder's reading and has not been shown. *Cost:* an
  amendment to §3 and to C-N1's no-exception rule, because step 1 kills `HonestChain(L2)` (W1:4058).
  The evidence so far is against step 1 landing a **whole** degraded file: `cc02_d` at step 1 ran out of
  memory on link 2b after 6 997 s under a 10 GiB cap (F1), and `cc05_d`'s conjunct 1 was unchanged by
  steps 1 to 1-3. The run cost is up to eleven boxes of 65 700 s, about 200 h if all fail. Step 4 is not
  available, because it erases two-signer-only mutations (C-C2 shown; C-C16 and C-C17 by their MUTATES
  lines) and kills six witnesses. The out-of-set reds of the ablated `cc05_d` (C-Q7, honest-key
  authorship) would also need diagnosis first (§(f) item 5).
- **(iii) Use a second tool (Tamarin) for just those companions, later.** *Cost:* a new model of the
  composed degraded fixture in another formalism. That model brings its own transcription-fidelity risk,
  its own review and an unknown solver cost, and it sits outside the frozen registration, so it needs a
  registration of its own or an amendment. The (d) seams stay open until it lands. *(Probed 2026-10-04,
  `tamarin-probe/REPORT.md`: C-C2's (d) reds came out in about a minute each, but only on hand-guided
  depth-0 slices. The full composed model ran out of memory in Tamarin's precomputation at the registered
  depth, for the same wrapper-depth reason as ProVerif. Tamarin is not a drop-in fix.)*
- **(iv) Descend the set-(1) reds of the eleven from process-deletion slices of their own registered files,
  by amendment** *(added 2026-10-06 by the owner instance)*. A slice is the registered `.pv` with whole
  top-level parallel components (honest processes, wrapper stages) and all but one query deleted. Nothing
  else changes. Every trace of a slice is a trace of the full file, so a reconstructed `is false` in a slice
  is a red of the registered composed model. A green in a slice means nothing. Evidence:
  `proverif/dev/slice_probe/REPORT.md`. The cross-family review (`…/codex/REVIEW.md`) found the method
  *sound with conditions*: 93 slices regenerated byte for byte, no construct in these files that lets
  deletion add behaviour, reruns confirmed, and C-C2's C-Q3 A and C-C5's `InnerSigTransplanted` traces are
  the registered mechanisms.
  - **What it gives.** Every slice-addressable set-(1) red of ten of the eleven landed with a trace, in
    seconds to 8 min and at most 1.3 GB. That gives composed (d) evidence for D1 (C-C2), D2 (C-C4), D5
    (C-C5), D6 (C-C7(i), C-C7(ii)) and D7's membership half (C-C17). For D10 it gives the **consuming
    query C-Q5 red** under C-C3 and C-C8: the requirement that is unmet in every case today. Correct-form
    controls on the same slices are green.
  - **What it does not give.** Greens (set (2)), the absence of out-of-set reds, and C-C8-i (registered
    greens only). Those cells stay "not run under this blob".
  - **Cost.** An amendment saying that a slice red with a reconstructed trace may descend a (d) set-(1)
    cell, and nothing else. Minutes of solver time. A cross-family read of the exit-bearing traces
    (`…/codex2/REVIEW.md`). A fresh structural audit of `slice.py` if the source format ever changes.

**Re-running C-C8-i and C-C8-ii in (d) with the memory guard raised — the facts** *(added 2026-10-01,
REPAIR, skeptic S-5)*. Two of the four guard terminations stopped a run with box left: `cap_cc08ii_d` at
39 900 s (39.3 % of its box unspent) and `cap_cc08i_d` at 48 680 s (25.9 % unspent), each with 16-32 GB
still available on the guest (*The degraded wave*, the headroom table). The 80 GB rule is the owner
instance's, not the registration's, so raising it would move no box, model, query or prediction. Against
that: (1) both are **isolation configurations** of C-C8 (§9(2)), which bear on no matrix row directly; D10's
consuming query would still need C-C8 itself or C-C3 in (d), both of which timed out at the full box
(`rc=124`); (2) both ended on link 2b's one-signer conjunct (`ladder2/cap_cc08i_d.out:6091`, `ladder2/cap_cc08ii_d.out:6751`),
the query on which `cap_cc05_d` and `cap_cc17_d` were also terminated, with under 2 % of their box left, and
on which `cc02_d` at ablation step 1 ran out of memory under a 10 GiB cap (`abl_d` F1); how long either
spent on that query is not known, because per-query time is not logged; (3) at the four triggers the guest
held 120-171 GB in all (`totalMB`), and how far its dynamic memory can grow is not recorded in this file.
This file offers the re-run neither as an option nor as part of one; the builder makes no recommendation on
it.
**The owner instance's disposition follows.**

**The owner instance's recommendation (2026-10-06; a recommendation, not a ruling; replaces the 2026-10-01
recommendation of (i), archived in `proverif/ladder2/RESULTS-ladder2.md`).** **(iv)**, with (i) for whatever
(iv) cannot reach. Not (ii); (iii) only as optional later corroboration.

- **Why (iv).** It is the only option that gives the capstone's own composed model a red for D1, D2, D5,
  D10's consuming query, D6 in (d) and D7's membership half in (d). It needs no second tool, no transcription
  and no C-N1 exception, because it never asks a slice for a green or a witness. It costs minutes of solver
  time against a ceiling already exceeded 6.46-fold.
- **What (iv) still leaves to (i).** The greens and out-of-set results of the eleven (d) files, and C-C8-i,
  stay "not run under this blob" on family evidence. No row's severing rests on them.
- **Why not (i) alone.** It would meet the broken-companion requirement for four rows by family evidence
  only, a narrowing of §A3.3, when composed evidence is now available for minutes of solver time.
- **The amendment's words have to be narrow.** A slice red with a reconstructed trace may descend a (d)
  set-(1) cell. It never descends a green, a witness requirement or a set (2). The slicer is validated per
  source format, not in general.

> **AUTHOR ACCEPTED 2026-10-07: items 1–3 and 5 below (G1, G4, conjunct 3 to (d) only, C-C10/C-C14 C-Q6
> unrestricted into set (1)); item 4 (G2) stands as a finding.** His words: *"the clerical issues and their
> proposed resolution seem reasonable to me."* Amendment text to be drafted with (P), for signature.

**Amendment-shaped items from the divergence diagnosis** (`proverif/dev/divergences/DIAGNOSIS.md`;
**clerk findings of the owner instance, not entered, for the author's amendment if he agrees**):

1. **G1.** Add the authorship correspondences (`Accept ⟹ IssuerSigned`, honest-key authorship) to
   C-C5's set (1), and the unrestricted form to C-C17's, in the strict cases. They fall by construction,
   and C-C5's own cell describes the attack (`PREDICTIONS.md:1774`). The 2026-09-17 skeptic repair S-4
   made this exact correction for C-C7 and was not carried to these two.
2. **G4.** Add C-Q2 to C-C15(i)'s set (1) in cases (a) and (b). The registration's own sentence implies
   it (`:2503`), and it is not caused by BF-4 (red before and after the repair).
3. **Conjunct 3 under C-C15(i).** Assign set (1)'s conjunct-3 membership to case (d) only. The runs
   agree with the strict Cases cell (green in strict, red in (d)), and set (1) contradicts that cell.
4. **G2 is a finding, not an amendment.** With the standing path's own check 1 removed (C-C10) or
   subverted (C-C14), C-Q6 conjunct 1's unrestricted form goes red, while the honest-key forms stay
   green. The unrestricted standing verdict depends on authority evidence exactly as
   `Accept ⟹ IssuerSigned` does; case (c) shows the same red unmutated. No single-family model has a
   standing path, so only the composition could show it. For C-C10 it is a set-(2) green gone red, and
   the registration's set (2) was wrong in that respect. The reviewer reads it as a finding; the
   plain-language statement must carry it.
   *(REPAIR 2026-10-01, skeptic S-6. “Only the composition could show it” is right about the families
   and wrong about the registration, and is replaced by:)* **The composition confirms a dependence the
   registration encoded but mis-predicted in C-C10's set (2).** Encoded twice: §3's C-Q6 mapping row names
   check 1 as the check that pins the standing path's `t`, *“removed by C-C10 (and subverted by C-C14)”*
   (`PREDICTIONS.md:1018`), and the registration states the unrestricted form for the strict cases only,
   which carries the same dependence on authority evidence. Mis-predicted once: C-C10's set (2) names
   C-Q6 green *“on the same descent”* (`:1779`), a descent with no standing path. *The case-(c) line*
   (`cap_cc01_c.out:12621`) *is read here **diagnostically only**; C-Q6 is not stated for (c) (B-4), and no
   verdict rests on it.*
5. **C-C10's and C-C14's C-Q6 conjunct 1, unrestricted** *(added 2026-10-01, REPAIR, skeptic S-6; a clerk
   finding of the owner instance's builder, **not entered**, for the author's amendment if he agrees)*.
   Item 4 says set (2) was wrong but proposed no route, which left C-C10 (a)/(b) DIVERGENT with no way to
   close. The amendment-shaped item: **move C-Q6 conjunct 1's unrestricted form from C-C10's set (2) to its
   set (1) in (a) and (b)**, registered red on the dependence `:1018` already encodes, and **add it to
   C-C14's set (1) in (a) and (b)**, where set (2) does not name C-Q6. Neither touches (d), where the
   unrestricted form is not asserted. The honest-key forms stay in both companions' green lists, which the
   runs agree with (`cap_cc10_a.out:11707`, `:11904`; `cap_cc14_a.out:38020`, `:38676`; the same in (b)),
   so D12's severing (C-C11) is unaffected. Whether G2 is then also carried as a finding (item 4) is
   separate, and is the reviewer's and the author's.


### ROUTED TO THE AUTHOR — second question: whether to amend the companion allowance to the per-case sum (P), or keep the registered predicted-red box (Q) *(added 2026-10-01, skeptic S-4; restated 2026-10-01, cross-family finding 5)*

> **AUTHOR RULED 2026-10-07: amend the companion allowance to (P), the per-case sum, as recommended.** His
> words: *"I have no objection to accepting your recommendation for (2)."* The amendment text is still to be
> drafted, as an exception entered after the freeze, and goes to him for signature.

**The question.** How much wall clock is a companion run allowed: the sum of its case's boxes, or the box of
the query it is predicted to red? Section 0 records both readings and this file has not chosen between
them. The choice carries matrix rows, so it is the author's. The builder presents it and makes no
recommendation; **the owner instance's recommendation, if any, is added by the owner instance.**

**The registration's sentences, verbatim.**

1. §3, the ladder (`PREDICTIONS.md:305-310`): *“**Timeboxes** are per run, each compromise case getting the
   full box, and are raised above the families' 15 to 30 minutes because the capstone's term space is the
   product of what the families ran separately (seven check groups, three layers, two slots, two channels,
   two issuers, a two-entry lineage, and correspondences with an acceptance-identifier grouping no family
   model carried).”*
2. §3, *“What the total is, and is not”* (`:1617-1621`): *“**1185 min is the per-case sum** *(1155 before
   the 2026-09-18 amendment added C-Q10)*. Each compromise case gets the full box, so the declared
   wall-clock ceiling for the ladder is the per-case sum taken over the cases each query is stated for:
   **at most 4 × 1185 = 4740 min (79 h)** …”*
3. §4, *“The count”* (`:1867-1876`): *“**No companion carries a timebox**: §3's timebox table is over
   registered **queries** only, and a companion runs inside the box of the query it is predicted to red, so
   the 1155-minute per-case total and the 26 entries are unchanged by these three additions, by C-C16,
   **by C-C17** *(REPAIR 2026-09-17, Codex round 5 finding 1)*, and by C-C8's two isolation configurations.
   **C-C17 runs inside link 2a's 45-minute box** (§3) and **C-C16 runs inside link 5's 60-minute box** (§3),
   as C-C9 runs inside link 2b's; **C-C18 runs inside C-Q10's 30-minute box** (§3), the box the 2026-09-18
   amendment added for the query and not for the companion …”* — with §3's amendment note (`:1612`): *“No
   companion gains a box: C-C18 runs inside C-Q10's.”*, and §9(2) (`:2590`): the isolation configurations
   *“carry no timebox of their own — they run inside C-Q9's 60-minute box (§3), as C-C3's do inside
   C-Q5's.”* (Section 0's phrase *“No companion carries a box of its own”* is this file's paraphrase of
   sentence 3.)

**How each sentence bears.** Sentence 1 sets boxes *“per run”* and gives *“each compromise case … the full
box”*; it does not distinguish correct-form runs from companions. Sentence 2 defines the full box as the
per-case sum. Sentence 3 is about companions specifically, and says both that the companions add nothing to
the total — the reason it gives — and that a companion *“runs inside the box of the query it is predicted to
red”*, naming boxes of 30 to 60 minutes. **(P), the per-case-sum reading,** takes sentence 3 as an
accounting statement (companions add no entries) and sentences 1-2 as the run limit. **(Q), the
predicted-red-box reading,** takes sentence 3's *“runs inside the box of”* as the run limit for a companion.
*(WITHDRAWN 2026-10-01: cross-family review finding 5, ACCEPTED by the owner instance; the withdrawn
sentence: “Neither reading makes any sentence false; they differ on which sentence sets a companion's limit.”
**What was wrong:** (Q) is the reading the registration's own words support. It calls the entries
"separately timeboxed" and puts each conjunct inside its entry's box (`PREDICTIONS.md:1632-1641`). It then
gives each companion **its predicted-red query's box** and names C-C17's 45 minutes and C-C16's 60
(`:1867-1876`). Under (P) those two sentences become accounting statements, which they do not say they are.
The two readings are **not** equally faithful. (P) is a departure from the frozen text, and accepting it is an
amendment.)*

**The effect, row by row** (section 3, *Which box reading each severing depends on*; per-query time is not
logged, so under (Q) a run longer than its box is *“not shown inside its box”*, not *“shown outside it”*):

| Row | Under (P) | Under (Q) |
|---|---|---|
| D1, D2, D5 | no severing observed in any case | no severing observed in any case |
| D3 | severed in (c) | not shown inside its box (4 569 s against 30 min) |
| D4 | severed in (a), (b), (c), (d) | not shown inside its box in any case (2 908-4 569 s against 45 min) |
| D6 | severed in (a), (b) | (a), (b) inside (C-C7(i), 2 196 and 2 199 s against 45 and 60 min); (d) not run |
| D7, completeness (C-C9) | severed in (a), (b), (d) | the same: 240-1 323 s, inside 60 min |
| D7, common content (C-C16) | severed in (a), (b), (d) | (a), (b) inside; (d) not shown inside (6 261 s against 60 min) |
| D7, membership (C-C17) | severed in (a), (b) | not shown inside its box in any case (25 996-27 085 s against 45 min) |
| D8 | severed in (a), (b), (d) | (a), (b) inside; (d) not shown inside (3 419 and 7 794 s against 45 min) |
| D9 | severed in (a), (b) | not shown inside its box in any case (39 596-41 003 s against 45 min) |
| D10 | consuming query C-Q5 red in no case (S-7); producer C-Q9 red in (a), (b) | the same; C-Q9's red inside 60 min |
| D11 | severed in (a), (b), (d) | (a), (b) inside (C-C15(ii), (iii)); (d) not shown inside (3 941-7 495 s against 45 min) |
| D12, D13 | severed in (a), (b), (d) | the same: every run inside C-Q6's 90 min |

**What either choice costs.** If **(P)** governs, every severing observed in sections 2-3 stands as observed,
and the remaining gaps are those of the first question (D1, D2, D5, D10). If **(Q)** governs, four rows or
row halves (D3, D4, D9, D7's membership half) have no severing shown inside its box in any case, and
three more (D7's common-content half, D8, D11) have none shown in (d); those would need either a disposal
under §3 (the registered outcome for a run that exceeds its box is a timeout, disposed by ablation or a
change of tactic) or an amendment. No re-run is proposed here: the ladder's output carries no per-query time,
and timing one query alone would need a file carrying that query alone, which is not the registered file.

**The owner instance's recommendation (2026-10-01; a recommendation, not a ruling), RESTATED: AMEND the
companion allowance to (P).** *(Restated 2026-10-01 under cross-family finding 5. The withdrawn heading,
quoted: "The owner instance's recommendation (2026-10-01; a recommendation, not a ruling): (P)." Its withdrawn
first bullet is in `proverif/ladder2/RESULTS-ladder2.md`.)*

- **What the amendment does.** It replaces §4's *"a companion runs inside the box of the query it is
  predicted to red"* (`:1867-1876`) as a **run limit**. The replacement says *"a companion runs under its
  case's per-case sum, as the correct-form run does; it adds no entry to the ceiling"*. It is an
  **exception entered after the freeze**, and is not a reading of the frozen text.
- **What it preserves.** Every severing observed in sections 2-3 stands as observed, under the per-case
  allowance every file actually ran under. On the ladder-3 record that is D3 in (c), D4 in all four cases,
  D9 and D7's membership half in (a) and (b), and D7's common-content half, D8 and D11 in (d). (These
  rows are as in the effect table, re-read from ladder 3.)
- **What it relinquishes.** It gives up the registered claim that each of those severings shows inside a
  **30 to 60 minute** box. Per-query time was never logged, so no run shows it. Under the frozen text
  those runs are *"not shown inside the box"*. That is not the same as being shown outside it, and no
  property is relabelled false.
- **What still holds from the original bullets.** The builder chose (P) for `run_ladder.sh` on
  2026-09-19, before any result existed. That reduces outcome-driven selection. It does **not** turn
  (P) into the frozen instruction. The method lesson stands as written: a registration states its
  companion box in one sentence, and the runner logs per-query time.
- **The builder chose (P) before any result existed.** `run_ladder.sh`'s header (2026-09-19) gives every
  file the per-case sum and records the predicted-red reading beside it. That ordering is what a frozen
  registration exists to protect: the reading was not chosen after seeing which rows it saves.
- **What (P) does not claim.** It does not claim any companion's predicted-red query finished inside 30
  to 60 minutes. Per-query time was never logged, so no reader can say. A reader who holds (Q) has a fair
  textual case. Under (Q), the record is not that seven row-halves failed; it is that they are not shown
  inside a box that nothing measured.
- **Whichever the author rules, the ambiguity is a defect of the registration and goes to the method.**
  The next registration should say which box a companion runs under, in one sentence, and the runner
  should log per-query time. The capstone did neither, and this question exists because of that.

### ROUTED TO THE AUTHOR — third question. Under C-C15(i), which key is C-Q6's `kX`? *(added 2026-10-01; cross-family review finding 1)*

**The conflict.** The registration fixes C-Q6's `kX` in two ways that agree in the correct model and come
apart under C-C15(i).

1. *"**`kX`** — the accepting key, `LayerAccepted`'s own name for it. For C-Q6 it is the **innermost
   accepting key**: the `kI` of S-P7's `InnerCheck`, not the wrapper's `kW`. … the join's whole point is
   that it is the **same** argument"* (`PREDICTIONS.md:786-791`). The join table's row is *"`kI`, the
   inner accepting key | `kX` | **`kX = kI`**"*, and it is **immutable**: *"no companion removes it —
   removing one does not sever a producer fact, it un-joins the composition and makes C-Q6 vacuous"*
   (`:1005-1009`, `:1019`).
2. C-C15(i)'s own cell (`:2503`). *"the inner signature verified under `kW` instead of `kI`"*; *"the inner
   acceptance of this configuration reports the **presented inner** `(kW, tI, ppfI)`"* (the report
   contract BF-4 implemented); and, for conjunct 3, *"**(i)** reports the **wrapper** frame's key **and
   identity**, so `(kA, idA) = (kW, idW) ≠ (kI, idI) = (kX, id)` … in both the standing path's own
   extraction is untouched and reports `(kX, id) = (kI, idI)`"*. With conjuncts 1 and 2 predicted green
   *"because … the standing path … is **untouched by a scope mutation**"*.

Under C-C15(i), the key the inner acceptance **verifies under**, and that `LayerAccepted` carries, is
`kW`. The standing path is registered as untouched, and it computes against the **presented** inner key
`kI`. Sentence 1 requires those two to be "the same argument". Sentence 2 requires them to differ: it
predicts conjunct 3 red *because* they differ. The reviewer's run shows exactly that. One intake and layer
accepts under `pk(a_4)` and establishes standing under `pk(a_20)`
(`dev/codex/scratch/cc15i_d_keyjoin.out:3528`, `:3550`, `:3562`).

**Why the builder cannot repair it.** The builder judges this a registration conflict, not an encoding
defect. There are only three ways to make the standing key equal the accepting key under (i):

- the standing path reads the envelope's accepting key, which (E1) forbids;
- the companion also re-keys the standing path to `kW`, which contradicts sentence 2 ("untouched";
  `(kA, idA) ≠ (kX, id)`) and removes the key half of conjunct 3's registered red;
- the inner acceptance verifies under `kI`, which is no longer Q6b's mutation. That shape is configuration
  (iii).

Every one of them breaks a registered sentence. The current files follow sentence 2 and the literal "the
`kI` of S-P7's `InnerCheck`" of sentence 1. In Q6b, `InnerCheck`'s `kI` is a presented input that the
mutation leaves unused (`s-p7/proverif/sp7_q6b_companion_key_outermost.pv:181-198`). So `kX = kI` holds
as a **term** equality: both paths take the same presented `kI` from the one intake. What the files cannot
also satisfy is sentence 1's "accepting key … `LayerAccepted`'s own name … the same argument". Configurations
(ii) and (iii) leave the inner verification key alone, and **the conflict is confined to (i)**.

**The two readings the author can choose between.**

- **(A) `kI` is the presented innermost key.** This is the term `InnerCheck` is handed. Sentence 1's
  "accepting key" wording is amended to say so. C-C15(i) as built then preserves the join, and its C-Q6
  results read as registered.
- **(B) `kI` is the key the innermost acceptance actually verified under.** Then C-C15(i)'s registered
  severing cannot preserve the join, and (i) must be re-specified for C-Q6. One way is that C-Q6's
  conjuncts are not asserted of (i), and D11's C-Q6 half rests on (ii) and (iii).

**What C-C15(i)'s C-Q6 results can and cannot mean until the author rules.** They are **withheld from
discharge** (the owner instance's disposition 1).

- **Conjunct 3** is red in (d) (`cap_cc15i_d.out:19689`) and left open in strict. The red can
  show that the envelope's attribution `(kW, idW)` and the standing report `(kI, idI)` differ for one intake
  and layer. That is the sense sentence 2 registers. It **cannot** show a join-preserving severing under
  reading (B), because under (B) the two reports are about different keys by construction, and that red
  needs no scope severing to fire.
- **Conjuncts 1 and 2** are green. They remain statements about the standing path over the presented
  innermost terms. They do not certify composition with the key the envelope actually accepted under.
- **What does not move.** D11's link-6b half rests on C-C15(i) (d)'s link 6b red and on (ii) and (iii), and
  none of that involves the standing key. D11's strict discharge already rests on (iii)
  (`PREDICTIONS.md:2503`). D12 and D13 rest on C-C11 and C-C12, not on C-C15.
- **Not done, and not to be done:** making standing wait for envelope success (E1).

**The owner instance's recommendation (2026-10-06; a recommendation, not a ruling): (A).**
- **It matches what was built.** The files follow sentence 1's literal "the `kI` of S-P7's `InnerCheck`",
  and the join's purpose (C-Q6 is not vacuous, because standing and acceptance speak of the same presented
  inner term) holds as a term equality.
- **It loses nothing the exit needs.** D11's strict discharge rests on (iii), its link-6b half needs no
  standing key, and D12/D13 rest on other companions (see *What does not move* above).
- **What it costs.** C-Q6 under C-C15(i) certifies the standing path over the presented inner key, not over
  the key the envelope actually verified under. The gap between those two is exactly what conjunct 3's (d)
  red shows. That is the mutation being caught, which is the point of a severing companion.
- **(B)** would re-specify a companion for no row's benefit.

## The owner instance's disposition: C-C8-i and C-C8-ii in (d) are not re-run with the guard raised

*(2026-10-01, a clerk disposition of the owner instance, answering the facts recorded under the first
routed question; contestable by the author without an amendment.)* Neither run bears on a matrix row: D10's
consuming query needs C-C3 or C-C8 itself, and both timed out at the full box. Both ended on the query on
which every other degraded failure of this shape also stalled. A re-run with the guard raised could at best
land two isolation configurations that the routed disposal would still have to carry. And it would spend up
to about 9 h of solver time against a ceiling already exceeded 5.6-fold. The 80 GB guard is recorded as the
owner instance's rule, with the headroom at each trigger stated, so a reader can see what was given up. **If
the author wants them run, they are run**; it would be a scheduling change, not an amendment.

---

## Ladder restarts

Ladder 1's launch history on wam-nuc of 2026-09-19 (the four restructurings, the 18:29:30 kill, the owner
instance's memory kills, the detachment check, the hand edits to ladder 1's log, and **THE RULE** that a
running ProVerif is not killed short of a demonstrated broken fixture) is ladder-1 history and is kept, as
written, in `proverif/ladder2/RESULTS-ladder2.md`, *Ladder restarts*. That log is `proverif/ladder1/ladder.log`.
No cell is read from ladder 1.

### After 2026-09-19: the machine change, ladder 1's stop, ladder 2, ladder 3, the host crashes *(added 2026-10-01; ladder-2 rows cite `proverif/ladder2/`)*

| When (UTC) | What, and why | Record |
|---|---|---|
| **2026-09-20T18:31:33 and 18:42:28** | The owner instance sent SIGTERM to `cap_cc07i_b` at 28.9 GB for memory, after the kernel had OOM-killed three ProVerif runs that day. It also stopped `cap_cc07ii_b` for scheduling ahead of the planned move. **Not results.** | `owner_interventions.log:1-2`; `ladder1/ladder.log:62-63` (`rc=143`) |
| **2026-09-20T19:10:41 to 19:11:23: the machine change** | The owner instance halted the wam-nuc ladder with four SIGTERMs (`cap_cc08_b`, `cap_cc08ii_b`, `cap_cc09_b`, `cap_cc10_b`; reason *machine change*). `cap_cc08_b` has no `ladder.log` line, because its logger had been killed by a mis-targeted stop command. The ladder resumed on **ubuntu24**, which is wam-desktop: a Hyper-V guest with dynamic memory, 64 cores and Ubuntu 24.04. The ProVerif 2.05 binary was copied from wam-nuc and validated there first (`capstone.pv`: 47 `RESULT` lines identical). `JOBS=2`. A relaunch followed at 19:12:31 for a scheduling-only wave-counter fix. **Same blob `c6969b4c…`; scheduling only.** Runs logged `rc=137`/`rc=143` on wam-nuc were re-run on ubuntu24 under the runner rule. | `owner_interventions.log:3-8`; `ladder1/ladder.log:68`, `:73` |
| **The memory guard on ubuntu24** | `mem_guard_vm.sh` sends SIGTERM to the largest ProVerif iff (available < 3 000 MB **and** total ≥ 90 000 MB) **or** its RSS > 80 000 000 kB. The guest's maximum was recorded as 96 GB on 2026-09-20. The guard logs show `totalMB` at 156 961 already on 2026-09-21 (`ladder1/mem_guard_vm.log:2822`) and at 170 731 on 2026-09-30 (`ladder2/mem_guard_vm.log:16282`), so the 96 GB figure did not hold for most of either ladder. Every guard termination in ladder 2 fired on the per-process 80 GB rule. | `mem_guard_vm.sh:9-13`; `ladder2/mem_guard_vm.log:1` |
| **2026-09-24T15:06:25: ladder 1 stopped** | The owner instance sent SIGTERM to the main `run_ladder.sh` (pid 9943) so that no further degraded pair would launch. `cap_cc02_d` and `cap_cc03_d` were left inside their boxes and logged `rc=124` later. The reason: the same three companions (C-C7(i), C-C7(ii), C-C14) had failed in both strict cases, and the degraded companions were heavier still (`cap_cc02_d` at 70+ GB after 16.4 h). **Not a result.** | `owner_interventions.log:10`; `ladder1/ladder.log:107-108` |
| **2026-09-24T17:15:52: ladder 2** | **A new model, not a restart of the old one.** It is blob `a9fb7da1…` (recut R-9). Ladder 1's `.pv`, `.out`, `.rss` and `ladder.log`, the ubuntu24 log and the guard logs are archived **unmodified** under `proverif/ladder1/`. Ladder 2 began from an **empty** `ladder.log`, so the runner skipped nothing. Machine ubuntu24, `JOBS=3`, `mem_guard_vm.sh` re-armed (thresholds above). Same boxes (71 100 s strict, 65 700 s degraded), same runner and same wave order. | `owner_interventions.log:11`; `ladder2/ladder.log:1-3`; `ladder2/mem_guard_vm.log:1` |
| **2026-09-28T13:01:30: `cap_cc05_d` terminated by the guard** | RSS 80 172 020 kB, on link 2b's one-signer conjunct. | `ladder2/mem_guard_vm.log:10972`; `ladder2/ladder.log:66` |
| **2026-09-28T16:32:25: main runner stopped** | The owner instance sent SIGTERM to the main `run_ladder.sh` (880969) after all six of the first degraded companions ended at their box or at the guard. The trio then in flight (`cap_cc07ii_d`, `cap_cc08_d`, `cap_cc08i_d`) was left to run to its box. The remaining fifteen degraded companions and case (c) were not launched by that runner. Disposal of the degraded wave went to diagnosis (`dev/abl_d/`). **Not a result.** | `owner_interventions.log:12` |
| **2026-09-28, 11:44:53 local (about 18:45 UTC): the Hyper-V host crashed** | The guest rebooted. The trio in flight, about six hours into its boxes, ended with no `rc`. Their partial outputs are kept as `*.interrupted-by-host-crash.out`, and they are **unrun** in the log's terms. The owner re-armed the guard at 18:59:57Z and launched **case (c)** alone with `run_one.sh`, which writes the runner's exact logging line. `cap_cc01_c` landed: `rc=0`, 4 279 s, 6.0 GiB. | `ladder2/ladder.log:69-70`; `owner_interventions.log:13`; `ladder2/mem_guard_vm.log:11642` |
| **2026-09-29T04:26:14: the remaining eighteen** | This launch came after `DEGRADED-WAVE-PREDICTION-2026-09-29.md` was written. The eighteen unobserved degraded companions, the crash-interrupted trio among them, ran unablated through `run_ladder.sh` with `JOBS=3`. A `cap_cc05_d.mechfail` marker made the runner log `MECHFAIL-MEMORY` instead of repeating an 18 h unablated run. The five `rc=124` siblings were skipped as landed-with-outcome. | `ladder2/ladder.log:71-78`; `owner_interventions.log:14` |
| **2026-09-30T09:46:11, 12:12:30 and 2026-10-01T10:43:44** | The guard terminated `cap_cc08ii_d`, `cap_cc08i_d` and `cap_cc17_d`, each above 80 000 000 kB RSS. | `ladder2/mem_guard_vm.log:16282`, `:16574`, `:19267`; `ladder2/ladder.log:82-83`, `:95` |
| **2026-10-01: `DONE`** | The runner finished. Every one of the 80 files has a ladder-2 line. | `ladder2/ladder.log:99` |

| **2026-10-01T17:59:41: ladder 3** | **A new model, not a restart of the old one.** The blob is `35d8c702…` (BF-5, BF-6), and C-C7(i)'s files also carry BF-7. Ladder 2's `.pv`, `.out`, `.rss`, `ladder.log` and guard log are archived **unmodified** under `proverif/ladder2/` (with a README). Ladder 3 begins from an empty `ladder.log`. **Scope, decided by the owner instance:** the 69 files that landed in ladder 2 are re-run. The eleven ladder-2 degraded mechanism failures (`cap_cc02_d`, `cap_cc03_d`, `cap_cc04_d`, `cap_cc05_d`, `cap_cc06_d`, `cap_cc07i_d`, `cap_cc07ii_d`, `cap_cc08_d`, `cap_cc08i_d`, `cap_cc08ii_d`, `cap_cc17_d`) are **not** re-run: each carries a `.notrun` marker, and the runner logs `rc=NOT-RUN` for it. Machine ubuntu24, `JOBS=3`, `mem_guard_vm.sh` re-armed, with the same boxes, runner and wave order. | `owner_interventions.log:15`; `ladder.log:1-3`; `mem_guard_vm.log:1` |
| **About 2026-10-02T23:23: the Hyper-V host became unresponsive** | The author reset the host; the guest went down with `cap_cc10_b` about 50 minutes in. Its partial output is kept as `cap_cc10_b.interrupted-by-host-crash.out` and is **unrun**, not a result; nothing reads it. The 40 files that had landed stand. | `ladder.log:47` |
| **2026-10-04T18:08:12: ladder 3 resumed** | The owner instance resumed the runner on the same blob and re-armed the guard. `cap_cc10_b` re-ran in full (`rc=0`, 3 654 s). **Scheduling only.** The `NOT-RUN` lines that follow are the resume logging the eleven markers; the RESTART comment calls them "repeated", but each stem has exactly **one** `NOT-RUN` line in the log (the runner had not reached wave 5 before the crash), and the assembler collapses any repeat. | `ladder.log:47-49`, `:55`; `mem_guard_vm.log:3517` |
| **`DONE`** | 69 `rc=0` lines and 11 `rc=NOT-RUN` lines, one per file. The guard never fired in ladder 3 (no `TRIGGER MET` in `mem_guard_vm.log`); the largest peak was `cap_cc14_b`, 31.9 GiB. | `ladder.log:96` |

**No `ladder.log` line of ladder 2 was edited by hand.** The comment lines at `ladder2/ladder.log:1`, `:69` and
`:71` were written by the owner instance at the time, as part of each launch or event. The comment lines of ladder 3's log
(`ladder.log:1`, `:47`) are the owner instance's.

---

## Broken fixtures, diagnosed and repaired

§4's replacement rule: *"a companion failing outside its set, or a witness dying, is a broken fixture
to be diagnosed and recorded, never a finding until the diagnosis distinguishes a broken fixture from
a real consequence of composition the single-family run could not exhibit"* (`:1668-1672`). Seven
have occurred (BF-1 to BF-7), and each is recorded here with its diagnosis and its repair rather than absorbed.

**BF-1 — C-C3, case (a), first run: every acceptance-dependent witness unreachable, no registered red.**
The run completed (`rc=0`, 717 s under the superseded blob `508b9018…`, companion blob `8e45eb76…`;
**that 717 s is not a cost datum for a working companion — the mutation accepted nothing, which is why
it was fast**) with **none** of set (1) — C-Q5, C-Q9, link 3 —
red, and with `HonestChain(L0)`, `HonestChain(L1)`, `HonestChain(L2)`, `HonestAccepted`,
`HonestWrappedAccepted`, both `HonestComplete` set sizes and `HonestWrappedStandingAgreed` all
**unreachable** (`dev/cap_cc03_a_BROKEN_FIXTURE.out:4070`, `:4136`, `:5110`, `:5176`, `:5242`,
`:5308`, `:5374`, `:5830`). Only `HonestStandingEstablished` and the five vocabulary witnesses
survived — the standing path being the one path that does not depend on an envelope acceptance. By
C-N1's rule *"a run in which any registered witness is unreachable is a broken fixture and not a
result"* (`:1487-1490`), and the honest-flow witnesses are the kind to which **no exception applies**
(`:1494-1500`).

**The diagnosis, checked against the family source rather than assumed.** The D-3 under-encoding is a
mutation of the **fixture** as well as of the verifier. S-P2's own Q5-C2 companion changes the honest
signer's possession object — `let ppf = sign((POSS, fp(pk(sk))), sk) in`,
`sp2_q5_c2_fponly_frame_nomh.pv:117` — **as well as** the two verifier checks at `:133` and
`:151-152`; and the library's D-3 note is why (`lib/tessera_theory.pvl:37-45`: possession is over the
manifest, and *"a model signing POSS over a fingerprint alone is a broken companion by definition"*).
`derive.py`'s `poss_fponly` had mutated the **verifier only**, so the honest signers went on producing
`(POSS, m)` that the mutated verifier could never accept: nothing was accepted at all, and every
witness that depends on an acceptance died with it. **That is a transcription defect in the
companion, not a consequence of composition and not a property result.**

**The repair.** `poss_fponly` now changes the signer's possession object too, and is the only change;
`cap_cc03_*`, `cap_cc08_*` and `cap_cc08ii_*` were regenerated (the three companions that use it —
`cap_cc08i_*`, the manifest-hash-only isolation, does **not** and is untouched, which the generated
files confirm). The broken run's `.out` is kept at `dev/cap_cc03_a_BROKEN_FIXTURE.out` and its
`ladder.log` line was removed, so **no result in this file comes from it**; `cap_cc03_a` is being
re-run against the repaired file. §9(2)'s discipline stands unchanged: **both** C-C8 isolation
configurations are run before C-C8's reds are counted.

**BF-2 — the same class, caught by audit before it ran: C-C11's Q4 alternate.** After BF-1 the
builder audited every mutation for the same defect — *does the honest flow still complete, and does
the registered consequence still follow?* One more was wrong. The Q4 alternate had been transcribed
by neutralising the terminal **test** while keeping the `terminal = TERM_REFUSED` branch above it,
which would have left the **S4** vocabulary witness `(ABSENT, ISSUANCE_REFUSED)` **reachable**. §4's
C-C11 row registers **S2 and S4 both unreachable** under this alternate, and the family does it by
replacing the **whole** `StandingDecide` body — `d` and `terminal` *"received and never read"*
(`ss_q4_companionC_terminal_unchecked.pv:234-237`), which is what makes both branches cease to exist.
`derive.py` now replaces the whole body. **This one never ran**: it was repaired before wave 3 reached
`cap_cc11q4_a`, so there is no quarantined `.out` for it. Recorded because the audit that found it was
prompted by BF-1, and because a reader checking the ladder should know two mutations were repaired,
not one.

**The audit's result on the other twenty-four configurations.** Every other mutation only **loosens**
a check the honest flow already satisfies, or changes only what is *reported*, so no honest witness
depends on it: C-C2, C-C4, C-C8-i, C-C9, C-C10 and its control, C-C12, C-C13(i)/(ii), C-C16, C-C17 and
C-C18 drop or unpin a check; C-C5, C-C6 and C-C7(i)/(ii) weaken the byte binding in a way the honest
case still satisfies; C-C14 changes the authority processes **and** the verifier together, which is
the same both-sides discipline BF-1 was missing; C-C11 and its abl6 alternate move where a value is
read from, not whether it exists; and C-C15's three configurations change attribution, with the honest
wrapped witness surviving (i) **only because §1.1 chose same-key wrapping** — `skI` wrapping its own
attestation is what keeps the reported wrapper key equal to the honest inner key. That last is the
fixture choice §1.1 defends at `:79-90`, doing exactly the work it was registered to do.

**BF-3 — the correct model, case (d): `ScopeMisreported` reachable, and it was the BUILDER'S bug, not
a prediction miss. REPAIRED AND CONFIRMED BY RUN.** *(Confirmation first, so no reader carries the
alarm further than it went: on the repaired model, `capstone_d` logged `rc=0 seconds=3805` (`ladder.log:7`) with
**`RESULT not event(ScopeMisreported(...)) is true`** at `capstone_d.out:10351` — conjunct 3
**green in (d)**, exactly as §3 §(5) registers it; ladders 1 and 2 gave the same line. The only false property in that run is the
**registered** degraded red, the A4.6 cost at `PREDICTIONS.md:1579` (`capstone_d.out:10976`). The prediction did not miss; the
builder's front end was wrong, and the repair is confirmed by the run rather than by argument.)* The degraded correct-form run came back with C-Q6's **conjunct 3 red**
(`ScopeMisreported` reachable), where §3 §(5) registers it *"unreachable in (a), (b) and (d) — the
same mode coverage as conjunct 2"*. Every witness was reachable, so C-N1's rule did **not** classify
it as a broken fixture, and it presented as the ladder's first genuine miss. **The trace says
otherwise.** At `(aid_7, L0)` — not even a wrapped layer — the envelope path accepted over
`authTuple(a_3, fp(pk(a_4)), signers0, a_2, a_5)` and reported `(pk(a_4), a_3)`, while the standing
path reported `(pk(a_16), a_15)` over a **different** tuple `authTuple(a_15, fp(pk(a_16)), …)`, both
with evidence forged under the leaked sole channel key. **The two paths had consumed different
presented terms for the same presentation.**

**The diagnosis.** §1.3 fixes the front end: *"a front-end process that reads the presented bundle
**once** and forwards it on private channels to the envelope path and the standing path in
parallel"*, and (E1) has the standing path compute over what it extracts *"from the **same bundle**
the front-end forwarded to it"* (`:151-160`, `:900-906`). The builder's `Front` forwarded only the
frames and signatures; each path then read its own `(t, ev, kX, ppf)` from the public channel. **That
is precisely the artifact-A / artifact-B substitution §3 C-Q6 (4) says the join must exclude** — and
which (E1) excludes *"by the shared fresh intake name and the structural extraction"*. In strict it
never bit, because both paths must use an honestly-evidenced tuple; in degraded the sole channel is
forgeable and the adversary can hand the two paths different tuples. The reviewer's own projection,
which the registration descends conjunct 3 at, forwards the **whole** bundle to both paths
(`cap15a_ss_q1_pairjudge_correct.pv`, `Front`).

**The repair.** The bundle is now read **once** and its per-layer material forwarded on `envMat` and
`stdMat`, one copy to each path, with `standCore` carrying the core and the standing evidence. Both
paths consume the **same** presented terms; neither waits for the other, neither path's report is
conditioned on the other's success, and no verifier check was added — the round-two independence that
lets C-C12 fail is untouched. `capstone.pv`'s blob changed from `508b9018…` to `c6969b4c…`,
**so all three completed runs were discarded** and the ladder restarted from the top. **No prediction
moved, and conjunct 3 is still registered unreachable in (a), (b) and (d); whether it is will be read
off the repaired run, not off this one.**

**BF-3's evidence, rebuilt** *(REPAIR 2026-10-01, skeptic S-12)*. The pre-repair runs' `.out` files were
deleted on 2026-09-19 (blob table above), so the defect's trace stood on this file's word alone. It has been
rebuilt from the tree, as diagnostic scratch and **not a result** (not counted in the ceiling):
`proverif/dev/bf3_rebuild/mk_bf3_rebuild.py` takes the current `capstone.pv`, removes recut R-9's 34-line
block (asserting the result hashes to ladder 1's `c6969b4c…`, and that `derive.py`'s `degraded()` of it hashes
to ladder 1's `capstone_d` blob `d4f0851d…`, `ladder1/ladder.log:25`), undoes exactly the BF-3 repair (the
Front reads only the frames and signatures from `c`, and the two envelope stages and the standing path each
read their own material from `c`, as the printed process at `dev/first.out:406` shows; the three reads are
written exactly as `derive.py:184-191` still matches them), and derives case (d) with `degraded()`. Under the
default selection function it ran once, `rc=0`, 356 s, 2.6 GiB (`dev/bf3_rebuild/run.log`). Of its 44
`RESULT` lines exactly **one** differs from `ladder2/capstone_d.out` (and so from ladder 3's, which is identical): conjunct 3,
`RESULT not event(ScopeMisreported(...)) is false` (`dev/bf3_rebuild/capstone_d_pre_bf3.out:5796`), with
the trace this section describes — the standing path reporting `(aid_7, L0, pk(a_16), a_15)` over
`authTuple(a_15, fp(pk(a_16)), …)` and the envelope path `(aid_7, L0, pk(a_4), a_3)` over
`authTuple(a_3, fp(pk(a_4)), signers0, a_2, a_5)` (`:5784-5796`). The skeptic made the same rebuild
independently in `/tmp` (its `.pv` differs from this one in whitespace only, and its 44 `RESULT` lines are
identical). **What the rebuild adds:** the red sits at `L0`, an unwrapped layer, outside conjunct 3's
registered *“over a wrapped presentation”* scope; the query as declared is broader than that (finding F-2), so the red was reachable to the query at all only because the query is not
layer-restricted. The repair is right regardless: §1.3's one-read contract is violated at every layer. The
Front's original source formatting and comment are not recoverable; its printed process is.

**What this vindicates, and it is worth saying.** §9(2) required C-C8's two isolation runs
specifically so that its *"both together"* minimality would be **shown rather than asserted**, and
C-N1's witness rule is what caught this. The registration's own machinery detected a builder's error
on the first companion that landed.

**BF-4 — C-C15(i), all three cases: the transcription reported the presented inner key, not the
wrapper key. Found by the divergence diagnosis, REPAIRED AND CONFIRMED BY RUN (2026-10-01).**
*(Confirmation first: on the repaired files, all 17 out-of-set reds that the defect produced are green,
every registered red still fires, and every witness is reachable. C-C15(i) (d) is now **as registered**;
C-C15(i) (a)/(b) keep one divergent red, C-Q2, which the diagnosis classes as G4 and which is not this
defect.)* *(Every run and `.out` line cited in BF-4 is ladder 2's, under `proverif/ladder2/`. Ladder 3
reproduces the three repaired files' `RESULT` lines byte for byte (*Cross-check*).)*

**What was wrong.** `derive.py:cc15i` builds `AttestStageW`, which verifies the inner signature under the
enclosing wrapper key `kEncW` and never matches the presented inner terms. It re-keyed only the scope
reports (`ATTRIB_BOTH`) and `sigCh` to `kEncW`. Every other event and report in the stage —
`LayerAccepted`, `Accept`, `link2aCh`, `possCh`, `bytesCh`, `link5Ch`, `slotCh`, `setCh`, `acceptCh`,
`acceptKeyCh`, `gsigCh`, `chainCh` — still carried the presented `kA`/`kB`, which after the mutation no
check touches. That contradicts the registered report contract, *"the inner acceptance of this
configuration reports the **presented inner** `(kW, tI, ppfI)`"* (`PREDICTIONS.md:2503`, the Cases
cell), and the family descent, which reports `kW` everywhere
(`cap25a_sp7_strict_q6b_sigjudges.pv:331-336`) and is where C-Q7 and C-Q8 were descended green. The
judges then saw a signature verified under one key and reported under an unrelated presented key, so the
file mutated more than the registered severing. **A transcription defect in the companion, not a
consequence of composition.**

**How it was found.** Section 2a listed C-C15(i)'s reds against the registration without resolving
them. The divergence diagnosis (`proverif/dev/divergences/DIAGNOSIS.md`, group G3, class A) read each
trace: every one of the 17 lines turns on the inner signature verifying under `pk(skI)` (or `pk(a_3)` in
(d)) while the judge sees the presented key. It then confirmed the reading by run, on diagnostic copies
`dev/divergences/dv_cc15i_kw_{a,b,d}` built by `dev/divergences/mk_cc15i_kw.py` (a trimmed copy for
(d)). Those copies are evidence, not ladder results.

**The repair.** `derive.py:cc15i` now ends with `_report_wrapper_key`, under a dated comment block
(*"REPAIR 2026-10-01 (broken fixture BF-4 …)"*). Inside `AttestStageW` only, on every line that is an
`event` or an `out(`, `kA` and `kB` become `kEncW`. No check changes, the correct `AttestStage` is
untouched, and the scope reports were already `kEncW`. This is exactly the change `mk_cc15i_kw.py` made.
Only `cap_cc15i_{a,b,d}.pv` were regenerated. A full `derive.py` run reproduces the other 76 generated
files byte for byte (checked with `git hash-object`).

- **The diff**, against each ladder-2 file: 27 lines changed, 27 removed and 27 added, all in
  `AttestStageW`'s two acceptance branches (one-signer and two-signer). That is 6 event lines and 21
  report lines, `kA`/`kB` → `kEncW`. Against the diagnostic copy, after the generated header, the
  regenerated file is **byte-identical** in all three cases. The only difference is the header comment:
  the ladder file's generated header (15 lines with its trailing blank) against the copy's 2-line
  `DIAGNOSTIC COPY` header.
- **Blobs.** (a) `9a19904bb64e3944c6735c8feab2808693dd281f` → `b5dbf3d233b9e91f198ed2342c3896d8bedff32b`;
  (b) `5bd381d16a199442b4b84ce7a2fb0de110da615f` → `95426aeef93dbbe72118e6f89e2f5cadc871ea01`;
  (d) `03365225821bafbd55fb25f7a15dd939b7f30d70` → `bc00b8310f7f77211c4ce540ede7f318a3e688ac`.
  `capstone.pv` (`a9fb7da1…`) and `PREDICTIONS.md` are unchanged.
- **Old runs**, kept as evidence of the defect in `proverif/ladder2/superseded-by-BF-4/` (with a README), and **no
  cell is filled from them**: (a) `ladder2/ladder.log:27`, `rc=0`, 295 s, 0.4 GiB; (b) `:54`, `rc=0`, 279 s,
  0.4 GiB; (d) `:91`, `rc=0`, 7468 s, 12.3 GiB. Their `ladder.log` lines stay as history above the comment
  line `# BF-4 REPAIR 2026-10-01T14:35:53Z …` (`ladder2/ladder.log:100`). The assembler treats every earlier run of
  a stem named in such a line as superseded: its time still counts in the ceiling, and it fills no cell.
- **New runs** on ubuntu24, with the same `run_one.sh` and the same boxes: (a) `ladder2/ladder.log:101`, `rc=0`,
  287 s, 0.38 GiB; (b) `:102`, `rc=0`, 279 s, 0.37 GiB; (d) `:103`, `rc=0`, 7825 s, 12.4 GiB. 47, 47 and
  44 `RESULT` lines. (a) and (b) reproduce the diagnostic copies' `RESULT` lines byte for byte. *(The
  80 GB memory guard was re-armed at 14:56:15Z, about 20 minutes after the runs started. It never came
  near triggering: the (d) peak was 12.4 GiB.)*
- **Cleared (reds the defect produced, now green).** *(REPAIR 2026-10-01, skeptic S-11: the heading read
  “Cleared (out-of-set reds now green)”. C-Q3 is not out of set: it is in C-C15(i)'s set (1), and green in
  strict only through the per-case Cases cell, which descends it green there. The other entries are out of
  set in the cases listed.)* (a): C-Q7 `cap_cc15i_a.out:4908`, C-Q8 `:4980`, link 4 `:6164`,
  C-Q3 `ReattributedA` `:7784` and `ReattributedB` `:7856`, `Accept => IssuerSigned` `:10016`, and
  `AcceptedUnderHonestKey => IssuerSigned` `:10114`. (b): the same seven at `:4919`, `:4992`, `:6179`,
  `:7804`, `:7877`, `:10049` and `:10148`. (d): C-Q8 `cap_cc15i_d.out:10188`, link 4 `:11651`, and
  `AcceptedUnderHonestKey => IssuerSigned` `:20840`.
- **Registered reds, all still firing.** (a): link 1a `:3331`, link 1b `:3879`, link 2a `:4434`, C-Q9
  `:5535`, link 3 `:6092`, link 5 `:6719`, C-Q5 `:8561`, `SignerForged` `:10745`. (b): `:3332`, `:3882`,
  `:4438`, `:5548`, `:6106`, `:6735`, `:8585`, `:10781`. (d): all thirteen of the case's registration, plus
  the baseline — link 1a `:3253`, link 2a `:3860`, C-Q7 `:9941` (the registered D-4 route), C-Q9
  `:10794`, link 3 `:11403`, link 5 `:12258`, link 6b `:13113`, C-Q3 `:13775`/`:14476`, `Rescoped`
  `:15138`, `InnerSigTransplanted` `:15840`, C-Q5 `:16553`, C-Q6 conjunct 3 `:19679`, `SignerForged`
  `:21704`, and the baseline `AcceptS => IssuerSigned` `:20432`. Every honest-flow and vocabulary witness
  is reachable in all three runs.
- **Still open, and not this defect.** C-Q2 is red in (a) `:7712` and (b) `:7731` with the trace the
  diagnosis read (G4: one unchecked evidence pair, two attacker tuples, no key involved). C-Q6 conjunct 3
  is green in (a) `:9915` and (b) `:9947`; the registration leaves it open in strict (the conjunct-3
  item). Both are amendment-shaped (class C), are listed in section 2a, and are not resolved here.


**BF-5: the correct model, every case. The standing path could report at an intermediate wrapper,
not the innermost layer. Found by the cross-family review (finding 2); repaired 2026-10-01; confirmed by
probe; the correct model's 47 verdicts in (a) unchanged.**

**What was wrong.** The registration puts C-Q6's `lyr` at *"the **innermost** layer of the wrapped
presentation"* (`PREDICTIONS.md:782`), and *"at depth 2 the innermost layer is `L2`"* (`:939-940`). The
standing path *"computes over the innermost `(t, ppf, sg, fb)` that it extracts structurally, itself"*
(`:892-894`). `StandingPath` read every layer that its own structural unwrapping (`SUnwrap`) put on
`sStageCh`, at `L0`, `L1` and `L2`. It never required that descent had stopped. So `EstablishedWrapped`
could fire at `L1` while the frame at `L1` was itself a wrapper. The reviewer's probe on ladder-2
`capstone_d.pv` showed this. The trace runs wrapper → wrapper → attestation, and standing is established
at `L1` (`dev/codex/scratch/capstone_d_noninnermost_attest.out:2998`, `:3010`, `:3020`). **So C-Q6 ranged
over standing reports the registration does not define.** A green over that wider domain is conservative.
A red or a witness there may be about the wrong layer.

**The repair** (`capstone.pv`, `StandingPath`, the block marked *BF-5 REPAIR 2026-10-01*). Immediately after
its `sStageCh` input, `StandingPath` proceeds only if the frame at this layer does **not** match
`SUnwrap`'s own pattern, `framed(=OT_WRAPPER, …, wrap(…))`. That is, it proceeds only where its own
structural descent has finished. It uses the registered definition of "wrapped", *"an `OT_WRAPPER` frame
whose payload field is a `wrap()` term"* (`:942-944`), and its complement defines "innermost". The repair
adds **no** type check, signature, authority check, or envelope event or success. (E1) is untouched: the
standing path still neither waits for nor is conditioned on `LayerAccepted`. *A positive guard was
considered and rejected:* requiring the layer's frame to be `OT_ATTEST` would copy envelope check 5 into
the standing path. That check is one C-C13(i) removes, and the registration defines innermost by the
wrapper parse, not by the attestation type.

**Blobs and diffs.** Every one of the 80 files changes blob, by exactly the same hunks
(`DERIVATION-CHECK-L3.md`). Probe evidence, which is not a ladder result. On the repaired model, the reviewer's intermediate-wrapper state is unreachable in (a) and (d) (`ladder3-staging/smoke/probe_a.out:2591`, `probe_d.out:2588`). On the unrepaired model the same probe reaches it (`probe_a_L2control.out:3117`; the reviewer's `capstone_d_noninnermost_attest.out:3020`). Honest wrapped standing stays reachable at `L1` and `L2` in both modes (`probe_a.out:4332`, `:5066`; `probe_d.out:4505`, `:5417`). The correct model's 47 `RESULT` lines in (a) are byte-identical to ladder 2's (`ladder3-staging/smoke/capstone.out`, 225 s on wam-nuc). Method: `DERIVATION-CHECK-L3.md` §3-§4. **Ladder 3:** all 69 landed files reproduce ladder 2's `RESULT` lines byte for byte, and no C-Q6 colour moved in any file (*Cross-check*).

**BF-6: the correct model, every case. The two standing witnesses were emitted at `L0`. Found by the
skeptic read (S-3, F-2's repair note) and the cross-family review (finding 4); repaired 2026-10-01.**

**What was wrong.** `HonestWrappedStandingAgreed` is registered for *"an honest wrapped acceptance"*
(`PREDICTIONS.md:1210-1212`). `HonestStandingEstablished` is registered *"over a **wrapped**
presentation"* (`:1341`). Both emission sites allowed `L0` (ladder-2 `capstone.pv:1054`, `:1064`), and every
ladder-2 trace for both was at `L0` (F-2's table). So ladder 2's *"as registered"* classifications of the two
standing witnesses in section 1 were too strong. C-N1 requires these witnesses in **every** companion
(`:1503`).

**The repair.** Both judges already hold the layer. `StandingJudge` receives `lyr` on `estCh`, and
`ScopeAgreementJudge` receives `l` on `scopeStanding`. Each emission is guarded with `if lyr <> L0` (or `l <>
L0`), as `StandingUnentitledWrapped`'s emission already was. **No query, no event signature and no
registered text changes.** The pair judge `ScopeMisreported` is **not** guarded. These are the
cross-family reviewer's own guards (`dev/codex/scratch/capstone_wrapped_witness.pv:1054`, `:1064`). On
ladder-2 baseline (a), with those guards alone, both witnesses were reachable at `L1` and all 47 verdicts
matched (`capstone_wrapped_witness.out:9124`, `:9132`, `:9794`, `:9798`). Ladder 3 is what checks the
witnesses in every companion, as C-N1 requires. **Ladder 3's result:** both witnesses are reachable in all
69 landed files, and every printed trace is at `L1` (section 1; `dev/l3/witness_layers.tsv`); no verdict moved.

**BF-7: C-C7(i), all three cases. The companion also accepted signed payloads that are not frames.
Found by the cross-family review (finding 3); repaired 2026-10-01 in `derive.py`.**

**What was wrong.** C-C7(i)'s registered mutation is *"the signature must verify under `kX` over *some*
frame naming `fp(kX)`, not over the presented bytes"* (`PREDICTIONS.md:1776`). The family descent
destructures the signed payload as a frame:
`let framed(otS, algS, idS, =fp(kX), mhS, cvS, plS) = fbS in`
(`ledger-tests-2026-09-14/d6e_sp1_q8all_samekey_unbound.pv:258`; the same line is in
`cap17b_sp1_strict_cc7i.pv:293`). `derive.py:cc07i` used `if sigFrameKfp(sbA, kA) = fp(kA)`. That
companion-local accessor's catch-all returns `fp(k)` for a **non-frame** payload, so any signed non-frame
passed (ladder-2 `derive.py:248-260`, `:351-360`). The companion therefore also removed the signed-frame
requirement. The reviewer did not show that this changed a strict verdict or caused `cap_cc07i_d`'s
timeout, and this report does not claim it either.

**The repair** (`derive.py:cc07i`, under a dated comment). The family's pattern match is transcribed:
`let framed(sfoA, sfaA, sfiA, =fp(kA), sfmA, sfcA, sfpA) = sbA in`, and the same for slot B. This is done in
the attestation and wrapper blocks. The unused accessors are no longer added to this companion. In each C-C7(i)
file, BF-7 is +6/−20 lines on top of the BF-5/BF-6 hunks.

**The audit of the same accessor elsewhere.** C-C6 (`cc06`) and C-C7(ii) (`cc07ii`) also use the
catch-all accessors, and they are **not** changed. In both, a non-frame signed payload makes the waiver's
condition false, so acceptance then requires `sb_ = fb_`. Every block the edit touches has already
destructured `fb_` as a `framed(…)` term, so the two can never be equal. A non-frame is therefore
rejected, as the families' pattern match rejects it (`d5a_sp1_condunbind.pv:207-210`,
`cap22b_sp7_strict_cc6.pv:232-235`, `d6d_sp1_q8_type_conditional_unbound.pv:276-280`,
`cap17c_sp1_strict_cc7ii.pv:305-309`). This reasoning is recorded as a note in `derive.py` below `cc07ii`.
No other companion uses the accessors.

**Ladder 3 status of C-C7(i).** `cap_cc07i_a` and `cap_cc07i_b` re-run under ladder 3. `cap_cc07i_d` was
a ladder-2 mechanism failure (`rc=124`, `ladder2/ladder.log:68`), so it is one of the eleven not re-run. Its
regenerated file is installed, but this blob gives it no result. **Ladder 3:** `cap_cc07i_a` and `cap_cc07i_b` landed
(`ladder.log:14`, `:41`) and reproduce ladder 2's `RESULT` lines byte for byte.

---

## Recuts (encoding, not property)

On the S-P3 pattern (`s-p3/RESULTS.md:38-73`). Each of the following is a way of **saying the same
thing** so that the model type-checks or terminates. **None of them changes a property, a query's
shape, or a registered prediction.** Where the registration was silent, the house pattern of the
sibling families was followed and is named.

**R-1 — the wrapper's inner blob carries the inner OBJECT's signer slots.** S-P7's embedding is
`wrap(cvInner, (fbI, sgI))` — one inner frame and one inner signature
(`sp7_q2_degraded_compromised.pv:317-334`). The capstone's inner layer performs **S-P2's set logic**,
so a wrapped inner object whose manifest is the two-signer `M2` has **two** frames and **two**
signatures. The constructor is unchanged, `wrap(bitstring, bitstring)`; what widens is the opaque
blob, from `(fbI, sgI)` to `(fbIA, sgIA, fbIB, sgIB)`. Encoding only: the blob is opaque to every
check exactly as before, the type equalities of §3 C-Q6 (3) are untouched, and no query moves.

**R-2 — the layer pipeline.** ProVerif has no recursion, and the families hand-write each depth
(S-P7's `VerifierWrapped` / `VerifierWrapped2`). The capstone instead carries the layer index on a
private channel `stageCh`: the front end emits the outermost object at `L0`, `WrapStage(L0, L1)` and
`WrapStage(L1, L2)` each accept one wrapper layer and emit the layer inside it, and `AttestStage`
accepts an attestation layer at whatever index it is handed. **Having exactly two `WrapStage`
instances is what bounds the depth at 2** (L-13's named scoping), exactly as S-P7's two hand-written
paths do. `AttestStage` is shared by the base path and by the innermost layer of a wrapped
presentation, as S-P7's `InnerCheck` is shared by `VerifierBase` and `VerifierWrapped` — which is
why C-C4 and C-C5, registered as mutations "inside `InnerCheck`", are single edits here too.

**R-3 — one `Rescoped`, not `RescopedD1` / `RescopedD2`.** §3 C-Q4 names `Rescoped` "at depths 1 and
2"; S-P7 splits it per depth because its two depths are two hand-written processes. Under R-2 one
judge covers both, and the layer index is in `LayerAccepted`, `ScopeReported` and `ChainBroken`. The
per-depth split of §3's producer column (`RescopedD1` / `RescopedD2`) is therefore a naming of S-P7's
models, not a query the capstone owes separately.

**R-4 — `wctx` records the IMMEDIATELY ENCLOSING wrapper, not the outermost.** S-P7 depth 2 uses
`wctx2(kO, idO, kM, idM)`. Under R-2 the context handed to the layer inside is
`wctx(kThisLayer, idThisLayer, fbThisLayer)`, so at `L2` the context **is** the middle wrapper —
which is precisely what C-C15(ii)'s "scope taken from the middle layer rather than the innermost"
needs, and what C-C15(i) needs at `L1`. Depth is carried by the layer index. `HonestWrappedAccepted`
at depth 2 therefore names the middle wrapper rather than the outermost; it is a witness, and its
reachability is what is registered.

**R-5 — link 3 and C-Q9 are one judge, and link 4 and C-Q8 are one judge.** §9 states it in terms:
"link 3's relation **IS** C-Q9's". The capstone fires `ChainBroken(lyr, LINK_3)` and
`PossessionUnbound(kX, t, ppf)` from the same failure of `checksign(ppf, kX) = (POSS, t)`, and
`ChainBroken(lyr, LINK_4)` and `SigBytesUnbound(kX, sg, fb)` from the same failure of
`checksign(sg, kX) = (BYTES, fb)`. Both remain **separate registered queries** with separate events
and separate results; what is shared is the report channel and the destructor's `else` branch — which
is what gives link 3 and link 4 the "including the case where it does not verify at all" clause §3
requires of them.

**R-6 — C-C15 is the one companion that needs a block duplication rather than a line edit.** S-P7's
Q6b, Q5c and Q6a mutate the **wrapped** path and leave `VerifierBase` alone. Since R-2 shares one
`AttestStage`, the C-C15 files **split** it: the correct stage keeps the cases the configuration does
not touch (`ctx = BASE` for (i) and (iii), `lyr <> L2` for (ii)) and a copy, `AttestStageW`, carries
the mutation for the rest. Nothing else in the model changes, and the split is written out in
`derive.py`'s `_split_attest`. *(Dated note 2026-10-01: for C-C15(i) the copy also reports the wrapper
key `kEncW` in place of the presented `kA`/`kB` in every event and report of `AttestStageW`, and in no
check. That is the BF-4 repair, under* Broken fixtures*.)*

**R-7 — a placeholder enclosing key at `L0`.** `stageCh` carries the enclosing wrapper's key and
identity so that R-6's split has them in scope. At `L0` there is no enclosing wrapper and the front
end supplies the public free name `kNone`, which no honest process holds and which nothing verifies
under. It is read by no check of the correct model.

**R-8 — `ReasonSink`.** S-STANDING's `ReasonJudge` (B9, reason-code discrimination) is **not** a
registered capstone query. Its channel still needs a reader, or the standing path's reason-code
report would block; the capstone declares a consuming sink and no query. B9 is not claimed here.

**R-9 — `set selFun = Term.`, applied uniformly to every case and companion file** *(added 2026-10-01;
the recut is of 2026-09-24, the owner instance's decision; it defines ladder 2).*

*What was recut.* One line, `set selFun = Term.`, was added to `capstone.pv` together with a dated
comment block. It is the file's first non-comment line. `derive.py` was not changed. It copies the line
into every derived file, so all 80 `.pv` files carry it. Each file was checked with `diff` against its
ladder-1 version: every file has exactly one hunk of 34 added lines, the same text in each, and nothing
removed (`proverif/ladder2-staging/DERIVATION-CHECK.md`). No process, check, event, query, fixture,
companion mutation, registered prediction or timebox changed.

*Why.* In ladder 1 the same three companions failed in both strict cases, each as a **mechanism failure
on C-Q1 link 2b conjunct 1**: the fourth query in declaration order, not link 2a, which lands in every
killed run (`dev/abl2a/REPORT.md` §0).

| Companion | Case (a) | Case (b) |
|---|---|---|
| C-C7(i) `cap_cc07i` | `rc=124 seconds=71105 peakRSSkB=64988588`, timeout at the 71 100 s box (`ladder1/ladder.log:79`) | `rc=124 seconds=71105 peakRSSkB=66335336` (`:87`) |
| C-C7(ii) `cap_cc07ii` | `rc=143 seconds=25426 peakRSSkB=80131372` (`:81`), SIGTERM by the 80 GB guard (`ladder1/mem_guard_vm.log:3213`) | `rc=143 seconds=24435 peakRSSkB=80044452` (`:86`; `ladder1/mem_guard_vm.log:5621`) |
| C-C14 `cap_cc14` | `rc=143 seconds=13667 peakRSSkB=80310108` (`:80`; `ladder1/mem_guard_vm.log:2822`) | `rc=143 seconds=13186 peakRSSkB=80621176` (`:99`; `ladder1/mem_guard_vm.log:7879`) |

The same runs had already died on wam-nuc (31 GB) at 17-31 GB (`ladder1/ladder.log:34`, `:38`, `:50`, all
`rc=137`, and `:62`, `rc=143`). §3 registers a timeout as *"mechanism-viability failure, evidence about
the tool or the encoding and **never** about the property, disposed by ablation **or a change of
tactic**"* (`PREDICTIONS.md:297-300`). This recut is that change of tactic. It is not an amendment,
because it touches no property, no query's shape and no registered prediction (§8 item 3).

*What the setting does.* ProVerif saturates the model's Horn clauses by resolution. In each clause the
**selection function** picks the hypothesis that resolution unifies on. ProVerif 2.05's default is
`TermMaxsize`. `Term` gives every ordinary hypothesis weight 0 instead of its size, which removes the
preference for large facts (manual extract :8040 and :8047-8050, recorded in
`dev/abl2a/manual_notes.md:20-23`). The setting changes which clauses are derived on the way to the
fixpoint and how many. It changes neither the clauses the model generates nor what a query asks.

*The soundness argument.* The ProVerif 2.05 manual, §6.6, verbatim: *"The performance settings may
result in more or fewer false attacks, but they never sacrifice soundness. It follows that when ProVerif
says that a property is satisfied, then the model really does guarantee that property, regardless of how
ProVerif has been configured using the settings presented here."* The quotation was taken from the
manual PDF on 2026-09-20 and is recorded in `dev/abl2a/manual_notes.md:6-11`. **Consequence:** under
`Term` an `is true` stays correct. The setting can cost only completeness: a false attack (`cannot be
proved`) or a slower run.

*Why uniformly.* Applied only to the runs that died, the setting would build the tables under two
configurations (`dev/abl2a/REPORT.md:381-384`). Applied to all 80 files, every companion still differs
from its correct form by its mutation alone. The alternative was ablation step 1, which deletes the
depth-2 layer this model exists to compose. It was held in reserve for whatever still failed.

*The controls, and what ladder 2 showed.*

1. **Pre-ladder, isolated files** (`dev/abl2a/`, 10 GiB cap). `cap_cc09_a` with the line added reproduced
   all 47 `RESULT` lines identically (`REPORT.md:296-302`). C-C5's isolated link-2b file landed in 40 s;
   unset, it had died of memory at 949 s.
2. **Pre-ladder, full files** (`dev/recut_pre/chain.log:2-4`, 16 GiB cap). `cap_cc07ii_a` and
   `cap_cc07i_a` landed. `cap_cc14_a` reached the cap (`rc=134` at 2 798 s). **In ladder 2 it landed**:
   `rc=0`, 43 842 s, 30.8 GiB (`ladder2/ladder.log:29`), and in (b) 41 473 s (`:56`).
3. **Staging smoke test** (`ladder2-staging/smoke.log:1`): 47 `RESULT` lines identical to ladder 1's
   `capstone.out`.
4. **The ladder-wide cross-check** (ladder 1 against ladder 2, in `proverif/ladder2/RESULTS-ladder2.md`, *Cross-check*). All 49 files that landed in ladder 1 are
   identical byte for byte. The 7 that ladder 1 lost are prefix-consistent. There are **0 differences
   and no `cannot be proved`**, so on this suite the setting cost nothing that the cross-check can see.

**Under ladder 2 every strict file landed**, including the three companions whose failures motivated the
recut, and case (c). The setting did **not** dispose of the degraded failures (*The degraded wave*).

---

## Blocked

Nothing in the registration was found unbuildable as written. Four items *(five since 2026-10-01; B-5 withdrawn the same day, BF-6)* are recorded here because
they are gaps between what the registration asks to be **observed** and what the registered query set
**declares**, and closing any of them would mean adding a query, which is not the builder's to do.
*(Checked 2026-10-01 against ladder 2: all four stand exactly as written; no fact in them changed. The
disposal of the degraded wave is not a block on building — the model was built and ran — and it is
routed in its own section.)*

**B-1 — the "honest-filtered C-Q8" of §4's C-C7 row is not a registered query.** §3 registers C-Q8 as
**structural**: *"The judge has **no honest-signature filter** and fires including the case where `sg`
does not verify under `kX` at all"* (`:1378-1386`). §4's C-C7 row nevertheless states an outcome for a
second, **honest-filtered** C-Q8 in the capstone — *"the **round-3 honest-filtered C-Q8** (`:711` `is
false`) **beside** the structural C-Q8"*, and closes *"**A green honest-filtered C-Q8 in the
capstone's (ii) is a divergence from this registration, not a success**"* (`:1776`). The capstone
declares the structural form only, because that is what §3 registers, so **that sentence has no
consumer here**: `cap_cc07ii_{a,b,d}` report the structural C-Q8 and nothing else. **The smallest
change that would unblock it:** register, by amendment, a second C-Q8 judge filtered on
`honestSigCh`-released signature terms — three lines beside `GenericSigJudge` — and say which of the
two §4's C-C7(ii) sentence is about. Nothing else moves.

**B-2 — link 6a is registered as one query, and §9(1)'s C-C13(ii) cell makes a PER-LAYER claim.**
§3's links are each *"a separate ProVerif query"* (`:314-327`) and `ChainBroken(lyr, link)` carries the
layer, but the registered query quantifies over `lyr`. C-C13(ii)'s cell requires the red to be *"at the
WRAPPER LAYERS ONLY ... and NEVER the innermost attestation layer"* (`:2501`). A single
`event(ChainBroken(l, LINK_6A))` query cannot separate those; what it yields is one counterexample
trace, whose layer can be read off the trace but which says nothing about the other layers. This
report therefore records **which layer the trace names** for C-C13(ii) and marks the per-layer claim
**not observed as a query**. **The smallest change:** register `ChainBroken(L0, LINK_6A)`,
`ChainBroken(L1, LINK_6A)` and `ChainBroken(L2, LINK_6A)` as three conjuncts of link 6a, exactly as
link 2b is registered as three conjuncts — per-layer resolution is already §2's encoding rule (2), and
no probability or timebox would move.

**B-3 — C-C17's recorded consequence `PossessionTransplanted` is not a capstone query.** §9(4)'s C-C17
cell registers, as *"A RECORDED CONSEQUENCE, NEVER AN ASSUMED RETENTION"*, that
`PossessionTransplanted` becomes reachable under that companion (`cap13b…:1657`). S-P3's
`PossessionTransplanted` is **not** among §3's registered queries — §3 C-Q9 says in terms that it *"is
**not** this relation's producer: it compares keys only"* — and §"The REQUIRED retained queries" does
not list it. The capstone therefore does not declare it and this report cannot record its colour.
**The smallest change:** add `PossessionTransplanted` to the retained-query table with its own
prediction, or restate C-C17's consequence against C-Q9, which the capstone does declare.

**B-5 — the registered wrapped-standing witnesses have no layer-restricted query, and
`HonestStandingEstablished` cannot say “wrapped”** *(added 2026-10-01, skeptic S-3)*. *(WITHDRAWN 2026-10-01:
cross-family review finding 4, ACCEPTED by the owner instance. **What was wrong:** B-5 said the existing query
signatures cannot show "wrapped", and that closing the gap is "**amendment-shaped**, not the builder's". That
necessity claim is false. Both judges already receive the layer, so guarding the two **emissions** with
`lyr <> L0` makes each witness wrapped-only, with no query, event signature or registered sentence changed.
The reviewer's strict run showed it (`dev/codex/scratch/capstone_wrapped_witness.out:9132`, `:9798`). The
repair is BF-6 (*Broken fixtures*); under ladder 3 both witnesses are reachable at `L1` in every landed file.
Separate `L1` and `L2` witness conjuncts would be an additional strengthening, which this file does not
propose. Nothing is routed for amendment from B-5. B-5's withdrawn text is in
`proverif/ladder2/RESULTS-ladder2.md`.)*

**B-4 — case (c) has no registered C-Q6, C-Q10 or C-Q2, but `cap_cc01_c.pv` declares them.**
§1.1's cases table states C-Q1-strict *"including link 1b"* for (a), (b) and (c); §3 states C-Q2 for
(a) and (b), C-Q6 for (a), (b) and (d), and C-Q10 for (a), (b) and (d). Case (c) is therefore a run of
**fewer** entries than the file carries. Rather than build a fourth query set, `cap_cc01_c.pv` carries
the strict set unchanged and this report **reads only the entries (c) is stated for**; the others are
recorded in the table as observed and marked *not a registered entry in this case*. No registered
prediction is read off them.

---

## Findings

Numbered, factual, one paragraph each. A finding is something **observed that the registration did
not predict**, including predictions that missed.

**F-1 — the composition terminates, and the mechanism-viability risk the registration priced highest
did not materialise in strict mode.** §3 prices timeout mass per query, and puts the largest of it on
C-Q6 (0.15, *"the largest timeout mass on the ladder"*, `:1330`) and on link 2b (0.10, *"concentrated
here because a correspondence with a fresh-name antecedent is the most expensive shape in the model"*,
`:454`). Observed: the strict correct-form runs resolve **every** declared query — all 47 of them,
including C-Q6's five and link 2b's three — in **374 s** (case (a)) and **392 s** (case (b)), with no
timeout and no *"cannot be proved"*. *(Under the superseded first blob the same 47 resolved in 193 s
and 194 s; both builds land this finding, and the repaired figures are the ones that stand.)* *(Dated
note 2026-10-06: the 374 s and 392 s are ladder 1's. Under ladder 3 the same 47 resolve in **262 s** (a)
and **264 s** (b) (`ladder.log:4`, `:5`), the degraded correct form's 44 in **3 805 s** (`:7`), and case
(c)'s 47 in **4 569 s** (`:94`). The finding stands for every correct-form run in all three ladders. **It does
not extend to companions in (d)**, where eleven of twenty-four failed in ladder 2 and are not run under
ladder 3 (*The degraded wave*).)* The composed model's term space is the product the registration
warned of (seven check groups, three layers, two slots, two channels, two issuers, a two-entry
lineage, correspondences under a fresh acceptance identifier), and ProVerif absorbed it.

**F-2 — every strict correct-form prediction landed, including the three the registration priced
lowest.** C-Q6 (p ~ 0.5), link 2b (p ~ 0.55) and link 5 (p ~ 0.65) are the three lowest numbers on
the ladder, and all three are green in (a) and (b), as are the six other links, C-Q2, C-Q3's two
roles, C-Q4's two judges, C-Q5, C-Q7, C-Q8, C-Q9, C-Q10 and all seven retained queries. Every C-N1
honest-flow witness is reachable at every layer — `HonestChain` at `L0`, `L1` **and** `L2`,
`HonestAccepted`, `HonestWrappedAccepted`, `HonestStandingEstablished` and
`HonestWrappedStandingAgreed` — and all five vocabulary witnesses are reachable. **No run of the
correct model is a broken fixture.**
*(Dated note 2026-10-06. Under ladder 2 this paragraph was narrowed (skeptic S-3): every trace the ladder
printed for the two standing witnesses was at `L0`, an unwrapped presentation, while the registration defines
them for the wrapped case — `HonestWrappedStandingAgreed` *“fired … when the two reports agree for an honest
**wrapped** acceptance”* (`PREDICTIONS.md:1210-1215`), `HonestStandingEstablished` *“over a **wrapped**
presentation”* (`:1341`). That narrowing and its `L0` table are in `proverif/ladder2/RESULTS-ladder2.md`. BF-6
guards both emissions to `lyr <> L0`, and under ladder 3 the sentence above holds as written:)*
`HonestWrappedAccepted` is reachable on a genuinely wrapped acceptance (its judge fires only on a `wctx`
context, and the printed trace names the wrapper key `pk(skW)`, `capstone.out:8612`), and **both standing
witnesses are reachable at `L1`**, the innermost attestation inside a wrapper:

| Case | `HonestWrappedStandingAgreed`: goal event in the trace | `HonestStandingEstablished`: the standing path's `estCh` report in the trace |
|---|---|---|
| (a) | `L1`, `capstone.out:9800` | `L1`, `capstone.out:9130` |
| (b) | `L1`, `capstone_b.out:9845` | `L1`, `capstone_b.out:9173` |
| (c) | `L1`, `cap_cc01_c.out:20830` | `L1`, `cap_cc01_c.out:19946` |
| (d) | `L1`, `capstone_d.out:16740` | `L1`, `capstone_d.out:15937` |

Every one of the other 65 landed files shows the same (section 2's Witnesses column). ProVerif prints one
trace per reachable event, so this shows reachability at `L1` and says nothing either way about `L2`. **The
same breadth remains in conjunct 3's query:** `not event(ScopeMisreported(a, l, k, ii, ka, ia))` fires at
`L0` as well, broader than the registered *“over a wrapped presentation”*. That is conservative for a green
(a green over every layer is a green over the wrapped ones), and it is why BF-3's defect showed at `L0`
(BF-3, *rebuilt*). BF-6 deliberately leaves the pair judge unguarded.

**F-3 — cost is dominated by the COMPROMISE CASE and by the presence of a severed check, not by the
query.** The registration's residual decompositions are per query; the observed cost is not.
**Measured:** the two strict single-leak correct-form cases resolve all 47 queries in **374 s** and
**392 s** under the repaired model (`c6969b4c…`) — and in 193 s and 194 s under the superseded one
(`508b9018…`), so §1.3's front-end contract, which routes the bundle's per-layer material through
private channels instead of letting each path read its own copy, **roughly doubles the cost of the
correct model**. That is a fact about the registered contract, not about any query. **Observed but NOT yet measured:** cases (c) — both channel keys public — and (d) —
degraded, the sole channel public — and every companion are **slower by a factor this file cannot
yet state**, because none of them had completed when it was written. What was actually seen, at about
**seven minutes** of elapsed time (`ps -o etimes`, not impression — see *Ladder restarts*): the
degraded correct-form run had resolved **2 of 47** queries, case (c) **3 of 47**, and the six case-(a)
companions between **0 and 12 of 47**, where the correct strict model resolves all 47 in 193 s — and
**those observations were made under the superseded blob `508b9018…` and are retained only as the
order-of-magnitude picture they gave; they are not results and none of them is quoted in a table**. The
direction is unambiguous and the mechanism is plain — once the adversary can mint authority evidence,
or once a check is removed, the reachable state space every query is solved against grows, and so
does the trace reconstruction the three-outcome vocabulary asks for. **The multiplier is left blank
until the runs land**, which is what the **Not run** section is for. *(Corrected 2026-09-19 after the
owner instance caught a mis-stated elapsed time; the withdrawn claim, quoted: "are between one and two
orders of magnitude slower".)* *(Dated note 2026-10-06: **the multiplier is now measured**, under
ladder 3. Strict correct form: 262 s. Strict companions: 182 s (`cap_cc10iso_b`) to 41 003 s
(`cap_cc14_a`). 42 of the 52 strict companion runs finished inside 30 minutes and 46 inside 4 012 s.
The other six are C-C7(ii), C-C17 and C-C14 in (a) and (b), at 9 512 s to 41 003 s. Degraded correct form: 3 805 s, **15×** the strict one. Case (c): 4 569 s.
Landed degraded companions: 1 323 s to 7 794 s. Eleven degraded companions did not finish in 65 700 s in ladder 2 and are not run under ladder 3.
The direction this finding stated holds, and the spread is now on the record in section 2.)*

**F-4 — the registration does not say what a WRAPPED TWO-SIGNER object looks like, and the capstone
is the first model where the question arises.** S-P7's embedding carries one inner frame and one
inner signature; S-P2's set logic gives a two-signer manifest two frames and two signatures; §1.1
composes both and §1.2 puts the set logic on every layer. The blob therefore had to widen (recut R-1).
This is an encoding consequence of the composition, and it is exactly the kind of thing the capstone
exists to surface: **no single-family model could have raised it.**

**F-5 — §1.1's same-key wrapping forces the WRAPPER layer to be a two-signer acceptance, which §1.1
does not say.** The chain is: `skI` wraps its own attestation (§1.1's wrapper row); `skI`'s manifest
is the two-signer `M2` (§1.1's required-signer row); ONE KEY, ONE MANIFEST forbids `skI` a second
manifest; and §1.2's check 3 requires **every** required slot satisfied. So an `OT_WRAPPER` frame
under `skI` is accepted over `M2` and needs `skB2` to co-sign it. The fixture here therefore runs
`Wrapper(skB2, …)` beside `Wrapper(skI, …)`, and the honest wrapped witness is a two-slot acceptance
at both layers. §1.3 comes within one sentence of saying so — *"the wrapper layer and the inner layer
be accepted over the same tuple `t` … the same issuer key, the same manifest `M2` and the same
required set appear at both layers"* (`:206-210`) — but the fixture consequence, a second honest
wrapper process, is not stated anywhere and had to be derived.

**F-8 — MEMORY, not wall clock, is this composition's binding resource, and the registration prices
neither.** §3's timeboxes bound **time**; nothing in the registration bounds **memory**, and memory is
what has twice stopped this ladder. Measured resident sets, 2026-09-19: the correct strict model's
process is small enough never to have been noticed; a **companion** grows to **1.0-3.7 GB**; the
**degraded** correct-form run to **9 GB**; and **case (c) — both channel keys public — to over 20 GB
and still running**, the largest single process of the whole suite. At 19:10 eight concurrent runs put
the machine at 0 GB available and 5.4 of 8 GB swap; at 19:24, with only the two protected runs left,
it was at **0.2 GB available and 5.3 GB of swap** again, `cap_cc01_c` at **20.0-20.6 GB** and
`capstone_d` at **8.5-9.2 GB and rising**. **The two runs that were killed for it, with their numbers.** `cap_cc01_c`
(case (c)) reached **20.6 GB resident at 3 of 47 queries**, 44 minutes in, and was terminated for it;
`capstone_d` (case (d)) was measured climbing **12.7 → 14.7 GB in thirty seconds** while holding at
3 of 47. Neither was slow in the sense §3 prices; both were **large**. **What a future builder needs,
and should be given by amendment rather than rediscovered:** (1) a **memory box per run** beside the
time box, since a run that exceeds memory dies without an `rc` line unless something like
`mem_guard.sh` is watching; and (2) a concurrency rule of the form
**`JOBS = floor(RAM / largest observed run)`** — on this machine, with case (c) at 20.6 GB, that is
**1** for case (c) and 3 for a companion wave, not the 6 or 8 a core count suggests. **The
consequence for anyone re-running this ladder:** the concurrency that fits is set by 31 GB divided by
the largest run, not by the core count, and case (c) alone can approach the machine. A ceiling expressed only in minutes (4740) does not bound what this
model actually consumes, and a kernel OOM kill — unlike a timeout — produces no `rc` line, no
classification and no record at all. **This is a gap in the registration's mechanism-viability
apparatus, not a defect of the model**, and it is the single thing a future builder most needs to know
before choosing `JOBS`.
*(Dated note 2026-10-01, the facts since: on ubuntu24 the 80 GB per-process guard terminated **four
ladder-1 runs** and **four ladder-2 runs**. The seven ladder-2 timeouts peaked at 21.8-46.9 GiB. Memory
and the per-run box, not the query, decided every mechanism failure in both ladders. The ceiling these
costs produced is stated under* Not run, and the ceiling*: 646.4 % over the three ladders. The guard never
fired in ladder 3, whose largest peak was 31.9 GiB.)*

**F-7 — what a severed check costs falls on EVERY query, not on the query that sees it.** The
registration prices its timeout risk per query and per formula shape — link 2b's fresh-name
antecedent, C-Q6's lineage inside a wrapper. The observed driver is neither. **In the correct strict
model link 1a is resolved in the first seconds of a 374 s run; in a companion it is the query the run
sits on**: at about seven minutes of elapsed time `cap_cc07i_a` had not yet resolved link 1a and
`cap_cc02_a` had resolved 2 of its 47, though neither companion mutates anything link 1a observes.
What grows under a severed check is not that query but the reachable state space **every** query is
solved against. **This is a shape of cost the registration does not price anywhere**, and it is the
one a future builder most needs: the companion ladder's wall clock is set by *how many checks are
missing*, not by *which queries are registered red*. **No ablation is owed**: §3's ablation order
fires on a timeout, and no run has timed out — the boxes are 1185 min per strict case and 1095 for
(d). *(Corrected 2026-09-19: the withdrawn claim, quoted, rested on a mis-stated elapsed time —
"spends tens of minutes on its FIRST query" and "the companion ladder is days". Seven minutes is what
was observed; how long a companion takes is not yet measured.)* *(Dated note 2026-10-01: **"No ablation is
owed … no run has timed out" is superseded.** In ladder 1, C-C7(i) timed out in (a) and (b), and C-C7(ii)
and C-C14 were terminated by the guard; they were disposed of by a change of tactic (recut R-9), not by
ablation. In ladder 2, eleven degraded companions failed; the tactics and ablations tried did not resolve
the sampled failures without unacceptable witness or mutation loss, which is not an impossibility result
(*The degraded wave*; restated 2026-10-01, cross-family finding 6, the withdrawn words: “neither of §3's
disposals disposes of them”). The cost shape this finding describes is visible there: the failing degraded runs
stall on link 1a or link 2b, and neither query is in any failing companion's set (1).)*

**F-6 — three registered sentences have no consumer in the registered query set.** §4's C-C7(ii)
sentence about a *honest-filtered* C-Q8, §9(1)'s C-C13(ii) per-layer assignment of link 6a's red, and
§9(4)'s C-C17 consequence on `PossessionTransplanted` each state an outcome for a relation that §3
does not register as a capstone query. They are recorded under **Blocked** (B-1, B-2, B-3) with the
smallest change that would close each. None of them is a defect of the model; each is a place where
the registration's prose ran ahead of its query list.

**F-9 — the change of tactic moved no verdict, and it landed every strict run** *(added 2026-10-01)*.
Recut R-9 (`set selFun = Term.`) reproduces byte for byte every `RESULT` line of the 49 files that landed
under the default selection function (ladder 1 against ladder 2, `proverif/ladder2/RESULTS-ladder2.md`,
*Cross-check*). It turned every strict mechanism failure of ladder 1
into a landing: C-C7(i), C-C7(ii) and C-C14 in (a) and (b), and case (c). *(REPAIR 2026-10-01, skeptic S-8:
“and case (c)” is withdrawn as credit to the recut. In ladder 1 case (c) was not a mechanism failure: the
owner instance terminated it at 2 732 s on the 31 GB machine (`ladder1/ladder.log:24`), and it was never re-run
under ladder 1's model. Ladder 2 landed it in 4 279 s on ubuntu24, but there is no ladder-1 run on that
machine to compare, so nothing shows the recut was what it needed.)* The effect on cost is not uniform. Over
the 49 files that landed in both ladders, ladder 2's time ranges from 1/34 of ladder 1's (`cap_cc05_b`:
15 191 s to 442 s) to 1.5 times it (`capstone_d`: 4 257 s to 6 388 s). The correct forms and C-C10 got
slower, and the heaviest companions got much faster: `cap_cc05_a` took 17 934 s and 22.1 GiB in ladder 1
(`ladder1/ladder.log:78`) and 944 s and 0.8 GiB in ladder 2 (`ladder2/ladder.log:12`). Part of ladder 1 ran on
wam-nuc and all of ladder 2 on ubuntu24, so this is not a controlled comparison. On this suite the completeness the manual says the setting may
cost was not observed to be lost.

**F-10 — the degraded companions fail on link 1a or link 2b, queries outside every failing companion's registered failed set** *(added 2026-10-01)*.
In ladder 2, eleven of twenty-four case-(d) companion runs ended without a result; they are not run under
ladder 3. Six stalled on link 1a, the first
query, and five on link 2b's one-signer or slot-A conjunct (*The degraded wave*). The degraded correct
form itself lands in 6 388 s (3 805 s under ladder 3). The diagnosis (`dev/abl_d/REPORT.md`) explains the first six by the
product of attacker-mintable tuples in (d) and a mutation that unbinds a key. It does not explain three
of the later five. This is the registration's own mechanism-viability outcome, and §3 has no disposal
for it. **It is not a property result**, and nothing in this file reads it as one.

---

## Not run, and the ceiling

*(Rewritten 2026-10-06 for ladder 3. The ladder-2 version, and the section as written 2026-09-19, are in
`proverif/ladder2/RESULTS-ladder2.md`.)*

**69 files landed under ladder 3 (`rc=0`), and 11 are not run under this blob.** The eleven are the ladder-2
degraded mechanism failures; each has one `rc=NOT-RUN` line (`ladder.log:69-78`, `:91`), and each cell
citing it gives the ladder-2 outcome as history: seven reached the 65 700 s box (`rc=124`) and four were
terminated by the 80 GB memory guard (`rc=143`; `cap_cc05_d`'s is followed by a `MECHFAIL-MEMORY` line,
`ladder2/ladder.log:78`). **None of the eleven has a result**, and their disposal is routed to the author
(*The degraded wave*). **No box was raised for any run, in any ladder.**

<!--NOTRUNLIST-->
**Landed under ladder 3 (69 of 80):** `cap_cc01_c`, `cap_cc02_a`, `cap_cc02_b`, `cap_cc03_a`, `cap_cc03_b`, `cap_cc04_a`, `cap_cc04_b`, `cap_cc05_a`, `cap_cc05_b`, `cap_cc06_a`, `cap_cc06_b`, `cap_cc07i_a`, `cap_cc07i_b`, `cap_cc07ii_a`, `cap_cc07ii_b`, `cap_cc08_a`, `cap_cc08_b`, `cap_cc08i_a`, `cap_cc08i_b`, `cap_cc08ii_a`, `cap_cc08ii_b`, `cap_cc09_a`, `cap_cc09_b`, `cap_cc09_d`, `cap_cc10_a`, `cap_cc10_b`, `cap_cc10_d`, `cap_cc10iso_a`, `cap_cc10iso_b`, `cap_cc11_a`, `cap_cc11_b`, `cap_cc11_d`, `cap_cc11abl6_a`, `cap_cc11abl6_b`, `cap_cc11abl6_d`, `cap_cc11q4_a`, `cap_cc11q4_b`, `cap_cc11q4_d`, `cap_cc12_a`, `cap_cc12_b`, `cap_cc12_d`, `cap_cc13i_a`, `cap_cc13i_b`, `cap_cc13i_d`, `cap_cc13ii_a`, `cap_cc13ii_b`, `cap_cc13ii_d`, `cap_cc14_a`, `cap_cc14_b`, `cap_cc15i_a`, `cap_cc15i_b`, `cap_cc15i_d`, `cap_cc15ii_a`, `cap_cc15ii_b`, `cap_cc15ii_d`, `cap_cc15iii_a`, `cap_cc15iii_b`, `cap_cc15iii_d`, `cap_cc16_a`, `cap_cc16_b`, `cap_cc16_d`, `cap_cc17_a`, `cap_cc17_b`, `cap_cc18_a`, `cap_cc18_b`, `cap_cc18_d`, `capstone`, `capstone_b`, `capstone_d`

**Not run under this blob (11 of 80); the ladder-2 outcome is history:** `cap_cc02_d` (ladder 2: timeout), `cap_cc03_d` (ladder 2: timeout), `cap_cc04_d` (ladder 2: timeout), `cap_cc05_d` (ladder 2: memory), `cap_cc06_d` (ladder 2: timeout), `cap_cc07i_d` (ladder 2: timeout), `cap_cc07ii_d` (ladder 2: timeout), `cap_cc08_d` (ladder 2: timeout), `cap_cc08i_d` (ladder 2: memory), `cap_cc08ii_d` (ladder 2: memory), `cap_cc17_d` (ladder 2: memory)
<!--END-NOTRUNLIST-->

**Runs that appear in no log, and are therefore not counted below:**

- the three runs under the superseded blob `508b9018…` (*Ladder restarts*);
- the six runs killed at 18:29:30 on 2026-09-19 with no line;
- `cap_cc08_b`'s wam-nuc run, terminated 2026-09-20T19:10:41Z after its logger was already gone
  (`owner_interventions.log:8`);
- the three degraded runs interrupted by the 2026-09-28 host crash, about six hours into their boxes;
- `cap_cc10_b`'s ladder-3 run interrupted by the 2026-10-02 host crash, about 50 minutes in
  (`cap_cc10_b.interrupted-by-host-crash.out`, not read);
- every diagnostic run under `dev/` (`abl2a`, `recut_pre`, `abl_d`) and the staging smoke test.

### The whole-ladder ceiling

<!--CEILING-->
**The whole-ladder ceiling, taken over all THREE ladders, is EXCEEDED by 1 554 002 s: 1 838 402 s against
284 400 s, or 646.4 % (6.46 times).** The ceiling is §3's *"at most 4 × 1185 = 4740 min (79 h)"*, that is
284 400 s (`PREDICTIONS.md:1620`). Solver time is the sum of the `seconds=` fields of the three ladder logs.
Killed, guard-terminated, timed-out and superseded (BF-4) runs all count, because the ceiling bounds what the
ladder may spend, not what it keeps. `NOT-RUN` lines carry `seconds=0`.

| Ladder, machine | Log lines | Seconds | Of the ceiling |
|---|---|---|---|
| **Ladder 1** (blob `c6969b4c…`, `ladder1/ladder.log`), wam-nuc then ubuntu24 | 76 | **625 756** | **220.0 %** |
| **Ladder 2** (blob `a9fb7da1…`, `ladder2/ladder.log`), ubuntu24 | 84 (80 files; `cap_cc05_d` has two lines, each `cap_cc15i` file two) | **966 137**: 72 landed (288 363), 7 `rc=124` (459 916), 4 `rc=143` (217 858), 1 `MECHFAIL-MEMORY` (0) | **339.7 %** |
| **Ladder 3** (blob `35d8c702…`, `ladder.log`), ubuntu24 | 80 (69 `rc=0`, 11 `rc=NOT-RUN`) | **246 509**: 69 landed (246 509), 11 not run (0) | **86.7 %** |
| **All three ladders** | 240 | **1 838 402** | **646.4 %** |

*(Arithmetic, reproducible: `awk '/seconds=/{match($0,/seconds=[0-9]+/); s+=substr($0,RSTART+8,RLENGTH-8)} END{print s}' ladder1/ladder.log ladder2/ladder.log ladder.log`
prints 1838402. Run on each log alone, it prints 625756, 966137 and 246509. The ladder-1 split by machine
is in `proverif/ladder2/RESULTS-ladder2.md`.)*

**Why the ceiling was exceeded: the registration prices time per query and does not price memory
(finding F-8).** Four costs outside the per-query boxes account for most of the total:

1. **Memory on the first machine.** On 31 GB, companions were killed before they could finish: ladder 1's
   19 `rc=137`/`rc=143` lines on wam-nuc account for 84 934 s and produced no result.
2. **Ladder 1's strict link-2b mechanism failures.** C-C7(i) and C-C7(ii) in (a) and (b), and C-C14, ran
   to the box or the guard on ubuntu24 before the change of tactic disposed of them (recut R-9).
3. **The degraded wave.** Each degraded run is allowed 65 700 s. In ladder 2 the eleven failing degraded
   runs alone consumed **677 774 s (238.3 % of the ceiling)**. Ladder 1's two degraded runs added
   131 407 s.
4. **Model repairs after review.** Ladder 3 re-ran the 69 landed files under BF-5/6/7, 246 509 s
   (86.7 %), and moved no verdict.

**Ladder 1 alone had already exceeded the ceiling** when its main runner was stopped: 494 349 s, 173.8 %,
before its last two degraded runs logged. Every run in all three ladders ran inside its own registered
per-run box (71 100 s strict, 65 700 s degraded). The eleven `rc=124` lines (four in ladder 1, seven in
ladder 2) are those boxes expiring, and no box was raised.
<!--END-CEILING-->

---

## Deferred (not repaired)

*(Finishing rule, 2026-10-05: items noticed during the ladder-3 assembly that change no verdict and no cell;
one line each, not repaired.)*

- `ladder.log:47` says the eleven `rc=NOT-RUN` lines are "repeated" after the restart; each stem has exactly one such line (the runner had not reached wave 5 before the crash). The assembler collapses repeats anyway; none occurred.
- `owner_interventions.log` has no entry for the 2026-10-02 host crash or the 2026-10-04 resume; the only record is the comment at `ladder.log:47` and the guard's re-arm line (`mem_guard_vm.log:3517`).
- The ~50 minutes `cap_cc10_b` spent before the 2026-10-02 crash have no `seconds=` line and are not in the ceiling, as with ladder 2's three crash-interrupted runs.
- Ladder-3 run times differ from ladder 2's on the same machine in both directions (e.g. `cap_cc07i_a` 12 423 → 2 196 s, `capstone_d` 6 388 → 3 805 s, `cap_cc01_c` 4 279 → 4 569 s); not diagnosed. Only D6's (Q) cell depends on it.
- Historical sections (Ladder restarts before ladder 3, BF-1 to BF-4, Recuts, Blocked B-1 to B-4, the degraded wave, the C-C8 disposition's "5.6-fold") keep ladder-2/ladder-1 citations and figures as written; their file prefixes were corrected where the log moved, nothing else.
