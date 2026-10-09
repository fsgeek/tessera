# Capstone — results

**STATUS: PROPOSED — 2026-09-19; ASSEMBLED FOR LADDER 2, 2026-10-01 — produced by the AI collaborator (Claude Opus 5, builder, 2026-09-19; Claude Opus 5.5, builder, the 2026-10-01 assembly; both directed by the owner instance); not adopted; the commit is the author's.** Predictions frozen at `3568905` (PREDICTIONS.md; amended and confirmed through `32d0581`). Model: `formal/suite/capstone/proverif/capstone.pv`, blob `a9fb7da1e4851120677b21dea4a8c98a481ad43a` (ladder 2, recut R-9). *(REPAIR PASS 2026-10-01: after the skeptic read `docs/reviews/2026-10-01-skeptic-read-capstone-build.md`
(findings S-1 to S-12), the builder repaired this file; every repaired passage carries a dated note “REPAIR
2026-10-01, skeptic S-n”, and superseded text is kept and marked rather than deleted.)* *(Dated note 2026-10-01: until this assembly the line named blob `c6969b4cc2f2e30be7a7a950af7609ea75e4c700`, which is ladder 1's model, archived under `proverif/ladder1/`.)*

**WHERE THE LADDER STANDS (2026-10-01).** Ladder 2 is complete and nothing in it is unrun; ladder 1 was not completed but stopped by the owner instance on 2026-09-24 (`owner_interventions.log:10`) and archived *(REPAIR 2026-10-01, skeptic S-11; the withdrawn words, quoted: “Both ladders are complete; nothing is unrun.”)*. Under ladder 2 (the
model every cell below is read from) **69 of 80 files landed** and **11 did not**: all eleven are case-(d)
companions, seven at the 65 700 s box (`rc=124`) and four terminated by the 80 GB memory guard
(`rc=143`). **Every strict file — cases (a), (b) and (c) — landed.** Every correct-form query landed as
registered (section 1). Of 77 companion configuration files, **56 are as registered, 10 are divergent
(listed in section 2a, not resolved), and 11 are mechanism failures with no result**. *(Updated
2026-10-01 after the BF-4 repair: C-C15(i)'s three files were a broken fixture, diagnosed, regenerated
and re-run (*Broken fixtures*, BF-4). C-C15(i) (d) is now as registered, and C-C15(i) (a)/(b) stay
divergent on C-Q2 alone. Before the repair this sentence read 55 as registered and 11 divergent.)* The eleven degraded
failures cannot be disposed of by either of §3's two disposals, and that question is **ROUTED TO THE
AUTHOR** (*The degraded wave*). *(Added 2026-10-01, REPAIR, skeptic S-4: a second question is routed beside
it — which reading of a companion's box governs — because it carries the severing of D3, D4, D6, D9 and
D7's membership half in every case, and of D7's common-content half, D8 and D11 in (d).)* The whole-ladder ceiling is **exceeded 5.60 times** over both ladders
(*Not run, and the ceiling*).

**Tooling.** ProVerif 2.05 (`proverif -lib formal/suite/lib/tessera_theory.pvl <file>.pv`), run from
`formal/suite/capstone/proverif/` with `-lib ../../lib/tessera_theory.pvl`. Every run is recorded in
`formal/suite/capstone/proverif/ladder.log` with its exit code, its seconds, its box and the git blob
hash of the `.pv` it ran. **`capstone.pv` HAS CHANGED TWICE, and this is the record of it** *(dated 2026-10-01; the withdrawn words, quoted: “HAS CHANGED ONCE”)* (the author's
clarification at §8 item 2: the model is identified by its **contents**, and a model at the registered
path with a different hash is a different model).

| Blob | When | Results standing under it |
|---|---|---|
| `508b901808dc75dab3e86c2385dd8545af4cad0f` | the first build, 2026-09-19 | **NONE.** Three runs completed under it — `capstone` (193 s), `capstone_b` (194 s) and `capstone_d` (1247 s) — and **all three are discarded**, because the degraded run exposed a transcription defect against §1.3's front-end contract (**BF-3** below). Their `.out` files were deleted and their `ladder.log` lines removed. *(REPAIR 2026-10-01, skeptic S-12: the defective (d) model has been rebuilt and run once as scratch, `dev/bf3_rebuild/`; see BF-3.)* |
| `c6969b4cc2f2e30be7a7a950af7609ea75e4c700` | after the BF-3 repair, 2026-09-19. **Ladder 1**: wam-nuc from 2026-09-19T18:33:57Z, then ubuntu24 from 2026-09-20T19:11:23Z (`ladder1/ladder.log:13`, `:68`). Main runner stopped 2026-09-24T15:06:25Z (`owner_interventions.log:10`); its last two runs logged `rc=124` afterwards (`ladder1/ladder.log:107-108`). | **Ladder 1, ARCHIVED as history under `proverif/ladder1/`.** 49 files landed under it (`rc=0`). Every one was re-run under ladder 2 and reproduces its `RESULT` lines byte for byte (*Cross-check*). Ladder-1 outcomes are cited only as that cross-check and as mechanism-failure history. **No cell in sections 1-3 is filled from them.** *(Until 2026-10-01 this cell read “**every result in this file.**”)* |
| `a9fb7da1e4851120677b21dea4a8c98a481ad43a` | **RECUT R-9, 2026-09-24** (the owner instance's decision): `capstone.pv` plus a dated comment block and `set selFun = Term.`; nothing else changes (`diff`: one hunk, 34 lines added, none removed). **Ladder 2**, ubuntu24, launched 2026-09-24T17:15:52Z (`ladder.log:1`), `DONE` 2026-10-01 (`ladder.log:99`). | **every result in sections 1-3.** |

Each derived file's own blob is recorded on its `ladder.log` line, so every companion result names the
exact text it ran against. The development run kept at `proverif/dev/first.out` was made under the
first blob and is not a result; it is retained only because its `RESULT` lines documented the model's
first clean pass.

*(Added 2026-10-01.)* Under §8 item 2's clarification the model is identified by its contents, so
`a9fb7da1…` is a **different model** from `c6969b4c…`, and every result names its blob. Every derived
file changed blob in the same way and only in that way; the per-file old/new blob table is
`proverif/ladder2-staging/DERIVATION-CHECK.md`. Every ladder-2 `ladder.log` line's `blob=` was re-checked
on 2026-10-01 against `git hash-object` of the `.pv` beside it: 80 of 80 match.

**How to finish the ladder and regenerate this file.** `bash proverif/run_ladder.sh` resumes (it
appends to `ladder.log` and skips any file already logged); `python3 proverif/dev/assemble.py`
rewrites sections 1-3 and the Not-run list from the `.out` files and touches nothing else.
*(Dated note 2026-10-01: the paragraph above describes ladder 1 in flight. Ladder 2 is complete and
nothing is outstanding; ladder 1 was stopped by the owner instance, not completed (`owner_interventions.log:10`)
*(REPAIR 2026-10-01, skeptic S-11; the withdrawn words, quoted: “Both ladders are complete and nothing is
outstanding.”)*. Sections 1, 2, 2a and 3, the cross-check table, the failed runs' partial lines
and the run list are regenerated by `python3 proverif/dev/assemble_l2.py`, which reads ladder 2's `.out`
files and `ladder.log` for every cell and ladder 1's only for the cross-check; `dev/assemble.py` made
the ladder-1 interim tables and now refuses to run, with the reason in its header.)*

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
scheduling choice and changes no colour. *(Dated note 2026-10-01: that describes ladder 1. Ladder 2 ran
(a) and (b), then (d)'s correct form, then the companion waves of (a), (b) and (d), and case (c) alone
last among the correct-form and C-C1 runs. It ran on 2026-09-28 after the host crash, and the eighteen
remaining degraded companions followed it (`ladder.log:4-7`, `:70`, `:71`). No companion of any case
started before that case's correct-form run had completed.)* `dev/` holds the development scratch, **none of it a result**:

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
`:1588`). **No yes/no changes**, checked run by run: C-C9 ran 252, 255 and 1 377 s, inside both 30 and 60
minutes; C-C16 ran 284 and 273 s in strict (inside both) and 6 671 s in (d) (outside both); C-C17 ran
27 503 and 27 084 s (outside both). The generated column is therefore left as it is. Which reading governs
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
*(This block was rewritten 2026-10-01 for ladder 2. The ladder-1 interim tables it replaces were
generated, and most of their cells read* not run*; their source runs are archived under
`proverif/ladder1/`, and the cross-check below shows that every ladder-1 `RESULT` line that landed is
reproduced byte for byte under ladder 2. Nothing in this block is read from ladder 1.)*

## 1. Every registered query, by case

The four correct-form runs: case (a) `capstone.out`, (b) `capstone_b.out`, (c) `cap_cc01_c.out` (case (c)
**is** C-C1, §1.1), (d) `capstone_d.out`. Each row gives the registered prediction with its
`PREDICTIONS.md` line, the observed `.out` line with ProVerif's verdict, and the outcome against the
registered branch. A query is listed only in the cases it is stated for (B-4: `cap_cc01_c.pv` carries the
strict file's C-Q2, C-Q6 and C-Q10, none of which is stated for (c); they appear in section 2's C-C1 row
and are read nowhere). In §3's three-outcome vocabulary every cell here is a **termination**, because
ProVerif resolved each query. No correct-form run had a timeout, and none left a query unresolved
(`cannot be proved` occurs in no ladder-2 `.out`).

<!--S1-->
| Registered query | Registered prediction (`PREDICTIONS.md` line) | Case | Observed (`.out` line, verdict) | Outcome in the registered vocabulary |
|---|---|---|---|---|
| C-Q1 link 1a | green, p ~ 0.8 (`:362`) | (a) | `capstone.out:2551` `is true` — GREEN | **as registered** |
| C-Q1 link 1a | green, p ~ 0.8 (`:362`) | (b) | `capstone_b.out:2552` `is true` — GREEN | **as registered** |
| C-Q1 link 1a | green, p ~ 0.8 (`:362`) | (c) | `cap_cc01_c.out:2710` `is true` — GREEN | **as registered** |
| C-Q1 link 1a | green, p ~ 0.8 (`:362`) | (d) | `capstone_d.out:2548` `is true` — GREEN | **as registered** |
| C-Q1 link 1b | `is true` in (a) and (b), p ~ 0.8; `is false` in (c) (`:379`) | (a) | `capstone.out:2718` `is true` — GREEN | **as registered** |
| C-Q1 link 1b | `is true` in (a) and (b), p ~ 0.8; `is false` in (c) (`:379`) | (b) | `capstone_b.out:2721` `is true` — GREEN | **as registered** |
| C-Q1 link 1b | `is true` in (a) and (b), p ~ 0.8; `is false` in (c) (`:379`) | (c) | `cap_cc01_c.out:3268` `is false` — RED | **as registered** |
| C-Q1 link 2a | green, p ~ 0.8 (`:408`) | (a) | `capstone.out:2783` `is true` — GREEN | **as registered** |
| C-Q1 link 2a | green, p ~ 0.8 (`:408`) | (b) | `capstone_b.out:2787` `is true` — GREEN | **as registered** |
| C-Q1 link 2a | green, p ~ 0.8 (`:408`) | (c) | `cap_cc01_c.out:3490` `is true` — GREEN | **as registered** |
| C-Q1 link 2a | green, p ~ 0.8 (`:408`) | (d) | `capstone_d.out:2728` `is true` — GREEN | **as registered** |
| link 2b one-signer conj. | all three conjuncts `is true`, p ~ 0.55 (`:447`) | (a) | `capstone.out:2935` `is true` — GREEN | **as registered** |
| link 2b one-signer conj. | all three conjuncts `is true`, p ~ 0.55 (`:447`) | (b) | `capstone_b.out:2940` `is true` — GREEN | **as registered** |
| link 2b one-signer conj. | all three conjuncts `is true`, p ~ 0.55 (`:447`) | (c) | `cap_cc01_c.out:4829` `is true` — GREEN | **as registered** |
| link 2b one-signer conj. | all three conjuncts `is true`, p ~ 0.55 (`:447`) | (d) | `capstone_d.out:3829` `is true` — GREEN | **as registered** |
| link 2b slot-A conj. | all three conjuncts `is true`, p ~ 0.55 (`:447`) | (a) | `capstone.out:3087` `is true` — GREEN | **as registered** |
| link 2b slot-A conj. | all three conjuncts `is true`, p ~ 0.55 (`:447`) | (b) | `capstone_b.out:3093` `is true` — GREEN | **as registered** |
| link 2b slot-A conj. | all three conjuncts `is true`, p ~ 0.55 (`:447`) | (c) | `cap_cc01_c.out:6168` `is true` — GREEN | **as registered** |
| link 2b slot-A conj. | all three conjuncts `is true`, p ~ 0.55 (`:447`) | (d) | `capstone_d.out:4930` `is true` — GREEN | **as registered** |
| link 2b slot-B conj. | all three conjuncts `is true`, p ~ 0.55 (`:447`) | (a) | `capstone.out:3239` `is true` — GREEN | **as registered** |
| link 2b slot-B conj. | all three conjuncts `is true`, p ~ 0.55 (`:447`) | (b) | `capstone_b.out:3246` `is true` — GREEN | **as registered** |
| link 2b slot-B conj. | all three conjuncts `is true`, p ~ 0.55 (`:447`) | (c) | `cap_cc01_c.out:7507` `is true` — GREEN | **as registered** |
| link 2b slot-B conj. | all three conjuncts `is true`, p ~ 0.55 (`:447`) | (d) | `capstone_d.out:6031` `is true` — GREEN | **as registered** |
| C-Q7 | green, p ~ 0.8 (`:1371`) | (a) | `capstone.out:3304` `is true` — GREEN | **as registered** |
| C-Q7 | green, p ~ 0.8 (`:1371`) | (b) | `capstone_b.out:3312` `is true` — GREEN | **as registered** |
| C-Q7 | green, p ~ 0.8 (`:1371`) | (c) | `cap_cc01_c.out:7729` `is true` — GREEN | **as registered** |
| C-Q7 | green, p ~ 0.8 (`:1371`) | (d) | `capstone_d.out:6211` `is true` — GREEN | **as registered** |
| C-Q8 | green, p ~ 0.75 (`:1391`) | (a) | `capstone.out:3369` `is true` — GREEN | **as registered** |
| C-Q8 | green, p ~ 0.75 (`:1391`) | (b) | `capstone_b.out:3378` `is true` — GREEN | **as registered** |
| C-Q8 | green, p ~ 0.75 (`:1391`) | (c) | `cap_cc01_c.out:7951` `is true` — GREEN | **as registered** |
| C-Q8 | green, p ~ 0.75 (`:1391`) | (d) | `capstone_d.out:6391` `is true` — GREEN | **as registered** |
| C-Q9 | green, p ~ 0.8 (`:1408`) | (a) | `capstone.out:3434` `is true` — GREEN | **as registered** |
| C-Q9 | green, p ~ 0.8 (`:1408`) | (b) | `capstone_b.out:3444` `is true` — GREEN | **as registered** |
| C-Q9 | green, p ~ 0.8 (`:1408`) | (c) | `cap_cc01_c.out:8173` `is true` — GREEN | **as registered** |
| C-Q9 | green, p ~ 0.8 (`:1408`) | (d) | `capstone_d.out:6571` `is true` — GREEN | **as registered** |
| link 3 | green, p ~ 0.8 (`:466`) | (a) | `capstone.out:3499` `is true` — GREEN | **as registered** |
| link 3 | green, p ~ 0.8 (`:466`) | (b) | `capstone_b.out:3510` `is true` — GREEN | **as registered** |
| link 3 | green, p ~ 0.8 (`:466`) | (c) | `cap_cc01_c.out:8395` `is true` — GREEN | **as registered** |
| link 3 | green, p ~ 0.8 (`:466`) | (d) | `capstone_d.out:6751` `is true` — GREEN | **as registered** |
| link 4 | green, p ~ 0.75 (`:479`) | (a) | `capstone.out:3564` `is true` — GREEN | **as registered** |
| link 4 | green, p ~ 0.75 (`:479`) | (b) | `capstone_b.out:3576` `is true` — GREEN | **as registered** |
| link 4 | green, p ~ 0.75 (`:479`) | (c) | `cap_cc01_c.out:8617` `is true` — GREEN | **as registered** |
| link 4 | green, p ~ 0.75 (`:479`) | (d) | `capstone_d.out:6931` `is true` — GREEN | **as registered** |
| link 5 | green, p ~ 0.65 (`:509`) | (a) | `capstone.out:3629` `is true` — GREEN | **as registered** |
| link 5 | green, p ~ 0.65 (`:509`) | (b) | `capstone_b.out:3642` `is true` — GREEN | **as registered** |
| link 5 | green, p ~ 0.65 (`:509`) | (c) | `cap_cc01_c.out:8839` `is true` — GREEN | **as registered** |
| link 5 | green, p ~ 0.65 (`:509`) | (d) | `capstone_d.out:7111` `is true` — GREEN | **as registered** |
| link 6a | green, p ~ 0.85 (`:527`) | (a) | `capstone.out:3694` `is true` — GREEN | **as registered** |
| link 6a | green, p ~ 0.85 (`:527`) | (b) | `capstone_b.out:3708` `is true` — GREEN | **as registered** |
| link 6a | green, p ~ 0.85 (`:527`) | (c) | `cap_cc01_c.out:9061` `is true` — GREEN | **as registered** |
| link 6a | green, p ~ 0.85 (`:527`) | (d) | `capstone_d.out:7291` `is true` — GREEN | **as registered** |
| link 6b | green, p ~ 0.8 (`:583`) | (a) | `capstone.out:3759` `is true` — GREEN | **as registered** |
| link 6b | green, p ~ 0.8 (`:583`) | (b) | `capstone_b.out:3774` `is true` — GREEN | **as registered** |
| link 6b | green, p ~ 0.8 (`:583`) | (c) | `cap_cc01_c.out:9283` `is true` — GREEN | **as registered** |
| link 6b | green, p ~ 0.8 (`:583`) | (d) | `capstone_d.out:7471` `is true` — GREEN | **as registered** |
| C-Q2 | green, p ~ 0.65 (`:599`) | (a) | `capstone.out:3824` `is true` — GREEN | **as registered** |
| C-Q2 | green, p ~ 0.65 (`:599`) | (b) | `capstone_b.out:3840` `is true` — GREEN | **as registered** |
| C-Q3 `ReattributedA` | green, p ~ 0.8 (`:615`) | (a) | `capstone.out:3889` `is true` — GREEN | **as registered** |
| C-Q3 `ReattributedA` | green, p ~ 0.8 (`:615`) | (b) | `capstone_b.out:3906` `is true` — GREEN | **as registered** |
| C-Q3 `ReattributedA` | green, p ~ 0.8 (`:615`) | (c) | `cap_cc01_c.out:9727` `is true` — GREEN | **as registered** |
| C-Q3 `ReattributedA` | green, p ~ 0.8 (`:615`) | (d) | `capstone_d.out:7651` `is true` — GREEN | **as registered** |
| C-Q3 `ReattributedB` | green, p ~ 0.8 (`:615`) | (a) | `capstone.out:3954` `is true` — GREEN | **as registered** |
| C-Q3 `ReattributedB` | green, p ~ 0.8 (`:615`) | (b) | `capstone_b.out:3972` `is true` — GREEN | **as registered** |
| C-Q3 `ReattributedB` | green, p ~ 0.8 (`:615`) | (c) | `cap_cc01_c.out:9949` `is true` — GREEN | **as registered** |
| C-Q3 `ReattributedB` | green, p ~ 0.8 (`:615`) | (d) | `capstone_d.out:7831` `is true` — GREEN | **as registered** |
| C-Q4 `Rescoped` | both green, p ~ 0.75 (`:630`) | (a) | `capstone.out:4019` `is true` — GREEN | **as registered** |
| C-Q4 `Rescoped` | both green, p ~ 0.75 (`:630`) | (b) | `capstone_b.out:4038` `is true` — GREEN | **as registered** |
| C-Q4 `Rescoped` | both green, p ~ 0.75 (`:630`) | (c) | `cap_cc01_c.out:10171` `is true` — GREEN | **as registered** |
| C-Q4 `Rescoped` | both green, p ~ 0.75 (`:630`) | (d) | `capstone_d.out:8011` `is true` — GREEN | **as registered** |
| C-Q4 `InnerSigTransplanted` | both green, p ~ 0.75 (`:630`) | (a) | `capstone.out:4084` `is true` — GREEN | **as registered** |
| C-Q4 `InnerSigTransplanted` | both green, p ~ 0.75 (`:630`) | (b) | `capstone_b.out:4104` `is true` — GREEN | **as registered** |
| C-Q4 `InnerSigTransplanted` | both green, p ~ 0.75 (`:630`) | (c) | `cap_cc01_c.out:10393` `is true` — GREEN | **as registered** |
| C-Q4 `InnerSigTransplanted` | both green, p ~ 0.75 (`:630`) | (d) | `capstone_d.out:8191` `is true` — GREEN | **as registered** |
| C-Q5 | green, p ~ 0.8 (`:689`) | (a) | `capstone.out:4149` `is true` — GREEN | **as registered** |
| C-Q5 | green, p ~ 0.8 (`:689`) | (b) | `capstone_b.out:4170` `is true` — GREEN | **as registered** |
| C-Q5 | green, p ~ 0.8 (`:689`) | (c) | `cap_cc01_c.out:10615` `is true` — GREEN | **as registered** |
| C-Q5 | green, p ~ 0.8 (`:689`) | (d) | `capstone_d.out:8371` `is true` — GREEN | **as registered** |
| `HonestComplete` (1-signer) | reachable, p ~ 0.85 (`:699`) | (a) | `capstone.out:4556` `is false` — REACHABLE | **as registered** |
| `HonestComplete` (1-signer) | reachable, p ~ 0.85 (`:699`) | (b) | `capstone_b.out:4578` `is false` — REACHABLE | **as registered** |
| `HonestComplete` (1-signer) | reachable, p ~ 0.85 (`:699`) | (c) | `cap_cc01_c.out:11182` `is false` — REACHABLE | **as registered** |
| `HonestComplete` (1-signer) | reachable, p ~ 0.85 (`:699`) | (d) | `capstone_d.out:8871` `is false` — REACHABLE | **as registered** |
| `HonestComplete` (2-signer) | reachable, p ~ 0.85 (`:699`) | (a) | `capstone.out:5006` `is false` — REACHABLE | **as registered** |
| `HonestComplete` (2-signer) | reachable, p ~ 0.85 (`:699`) | (b) | `capstone_b.out:5029` `is false` — REACHABLE | **as registered** |
| `HonestComplete` (2-signer) | reachable, p ~ 0.85 (`:699`) | (c) | `cap_cc01_c.out:11792` `is false` — REACHABLE | **as registered** |
| `HonestComplete` (2-signer) | reachable, p ~ 0.85 (`:699`) | (d) | `capstone_d.out:9414` `is false` — REACHABLE | **as registered** |
| C-Q10 | green, p ~ 0.85 (`:1459`) | (a) | `capstone.out:5071` `is true` — GREEN | **as registered** |
| C-Q10 | green, p ~ 0.85 (`:1459`) | (b) | `capstone_b.out:5095` `is true` — GREEN | **as registered** |
| C-Q10 | green, p ~ 0.85 (`:1459`) | (d) | `capstone_d.out:9594` `is true` — GREEN | **as registered** |
| C-Q6 c1 unrestricted | all three conjuncts hold, p ~ 0.5 (unrestricted form strict only) (`:1324`) | (a) | `capstone.out:5161` `is true` — GREEN | **as registered** |
| C-Q6 c1 unrestricted | all three conjuncts hold, p ~ 0.5 (unrestricted form strict only) (`:1324`) | (b) | `capstone_b.out:5186` `is true` — GREEN | **as registered** |
| C-Q6 c1 `skI` | green in (a), (b) and (d) (`:1233`) | (a) | `capstone.out:5239` `is true` — GREEN | **as registered** |
| C-Q6 c1 `skI` | green in (a), (b) and (d) (`:1233`) | (b) | `capstone_b.out:5265` `is true` — GREEN | **as registered** |
| C-Q6 c1 `skI` | green in (a), (b) and (d) (`:1233`) | (d) | `capstone_d.out:9787` `is true` — GREEN | **as registered** |
| C-Q6 c1 `skI2` | green in (a), (b) and (d) (`:1233`) | (a) | `capstone.out:5317` `is true` — GREEN | **as registered** |
| C-Q6 c1 `skI2` | green in (a), (b) and (d) (`:1233`) | (b) | `capstone_b.out:5344` `is true` — GREEN | **as registered** |
| C-Q6 c1 `skI2` | green in (a), (b) and (d) (`:1233`) | (d) | `capstone_d.out:9980` `is true` — GREEN | **as registered** |
| C-Q6 c2 | unreachable in (a), (b) and (d) (`:1245`) | (a) | `capstone.out:5382` `is true` — GREEN | **as registered** |
| C-Q6 c2 | unreachable in (a), (b) and (d) (`:1245`) | (b) | `capstone_b.out:5410` `is true` — GREEN | **as registered** |
| C-Q6 c2 | unreachable in (a), (b) and (d) (`:1245`) | (d) | `capstone_d.out:10160` `is true` — GREEN | **as registered** |
| C-Q6 c3 `ScopeMisreported` | unreachable in (a), (b) and (d) (`:1289`) | (a) | `capstone.out:5447` `is true` — GREEN | **as registered** |
| C-Q6 c3 `ScopeMisreported` | unreachable in (a), (b) and (d) (`:1289`) | (b) | `capstone_b.out:5476` `is true` — GREEN | **as registered** |
| C-Q6 c3 `ScopeMisreported` | unreachable in (a), (b) and (d) (`:1289`) | (d) | `capstone_d.out:10341` `is true` — GREEN | **as registered** |
| `Accept(S) => IssuerSigned` | green in (a)/(b) p ~ 0.85; RED in (c) p ~ 0.9; degraded `AcceptS` form registered RED in (d), the A4.6 cost (`:1569, 1580`) | (a) | `capstone.out:5544` `is true` — GREEN | **as registered** |
| `Accept(S) => IssuerSigned` | green in (a)/(b) p ~ 0.85; RED in (c) p ~ 0.9; degraded `AcceptS` form registered RED in (d), the A4.6 cost (`:1569, 1580`) | (b) | `capstone_b.out:5575` `is true` — GREEN | **as registered** |
| `Accept(S) => IssuerSigned` | green in (a)/(b) p ~ 0.85; RED in (c) p ~ 0.9; degraded `AcceptS` form registered RED in (d), the A4.6 cost (`:1569, 1580`) | (c) | `cap_cc01_c.out:14267` `is false` — RED | **as registered** |
| `Accept(S) => IssuerSigned` | green in (a)/(b) p ~ 0.85; RED in (c) p ~ 0.9; degraded `AcceptS` form registered RED in (d), the A4.6 cost (`:1569, 1580`) | (d) | `capstone_d.out:10966` `is false` — RED | **as registered** |
| `AcceptedUnderHonestKey => IssuerSigned` | green, p ~ 0.85 (`:1570`) | (a) | `capstone.out:5639` `is true` — GREEN | **as registered** |
| `AcceptedUnderHonestKey => IssuerSigned` | green, p ~ 0.85 (`:1570`) | (b) | `capstone_b.out:5671` `is true` — GREEN | **as registered** |
| `AcceptedUnderHonestKey => IssuerSigned` | green, p ~ 0.85 (`:1570`) | (c) | `cap_cc01_c.out:14733` `is true` — GREEN | **as registered** |
| `AcceptedUnderHonestKey => IssuerSigned` | green, p ~ 0.85 (`:1570`) | (d) | `capstone_d.out:11344` `is true` — GREEN | **as registered** |
| `Stripped` | green, p ~ 0.8 (`:1571`) | (a) | `capstone.out:5704` `is true` — GREEN | **as registered** |
| `Stripped` | green, p ~ 0.8 (`:1571`) | (b) | `capstone_b.out:5737` `is true` — GREEN | **as registered** |
| `Stripped` | green, p ~ 0.8 (`:1571`) | (c) | `cap_cc01_c.out:14955` `is true` — GREEN | **as registered** |
| `Stripped` | green, p ~ 0.8 (`:1571`) | (d) | `capstone_d.out:11524` `is true` — GREEN | **as registered** |
| `SignerForged` | green, p ~ 0.8 (`:1572`) | (a) | `capstone.out:5769` `is true` — GREEN | **as registered** |
| `SignerForged` | green, p ~ 0.8 (`:1572`) | (b) | `capstone_b.out:5803` `is true` — GREEN | **as registered** |
| `SignerForged` | green, p ~ 0.8 (`:1572`) | (c) | `cap_cc01_c.out:15177` `is true` — GREEN | **as registered** |
| `SignerForged` | green, p ~ 0.8 (`:1572`) | (d) | `capstone_d.out:11704` `is true` — GREEN | **as registered** |
| `Spliced` | green, p ~ 0.75 (`:1573`) | (a) | `capstone.out:5834` `is true` — GREEN | **as registered** |
| `Spliced` | green, p ~ 0.75 (`:1573`) | (b) | `capstone_b.out:5869` `is true` — GREEN | **as registered** |
| `Spliced` | green, p ~ 0.75 (`:1573`) | (c) | `cap_cc01_c.out:15399` `is true` — GREEN | **as registered** |
| `Spliced` | green, p ~ 0.75 (`:1573`) | (d) | `capstone_d.out:11884` `is true` — GREEN | **as registered** |
| `TypeConfused` | green, p ~ 0.85 (`:1574`) | (a) | `capstone.out:5899` `is true` — GREEN | **as registered** |
| `TypeConfused` | green, p ~ 0.85 (`:1574`) | (b) | `capstone_b.out:5935` `is true` — GREEN | **as registered** |
| `TypeConfused` | green, p ~ 0.85 (`:1574`) | (c) | `cap_cc01_c.out:15621` `is true` — GREEN | **as registered** |
| `TypeConfused` | green, p ~ 0.85 (`:1574`) | (d) | `capstone_d.out:12064` `is true` — GREEN | **as registered** |
| `VersionLied` | green, p ~ 0.85 (`:1575`) | (a) | `capstone.out:5964` `is true` — GREEN | **as registered** |
| `VersionLied` | green, p ~ 0.85 (`:1575`) | (b) | `capstone_b.out:6001` `is true` — GREEN | **as registered** |
| `VersionLied` | green, p ~ 0.85 (`:1575`) | (c) | `cap_cc01_c.out:15843` `is true` — GREEN | **as registered** |
| `VersionLied` | green, p ~ 0.85 (`:1575`) | (d) | `capstone_d.out:12244` `is true` — GREEN | **as registered** |
| `HonestChain(L0)` | reachable in all four cases, p ~ 0.85 (`:1487`) | (a) | `capstone.out:6406` `is false` — REACHABLE | **as registered** |
| `HonestChain(L0)` | reachable in all four cases, p ~ 0.85 (`:1487`) | (b) | `capstone_b.out:6444` `is false` — REACHABLE | **as registered** |
| `HonestChain(L0)` | reachable in all four cases, p ~ 0.85 (`:1487`) | (c) | `cap_cc01_c.out:16446` `is false` — REACHABLE | **as registered** |
| `HonestChain(L0)` | reachable in all four cases, p ~ 0.85 (`:1487`) | (d) | `capstone_d.out:12779` `is false` — REACHABLE | **as registered** |
| `HonestChain(L1)` | reachable in all four cases, p ~ 0.85 (`:1487`) | (a) | `capstone.out:6910` `is false` — REACHABLE | **as registered** |
| `HonestChain(L1)` | reachable in all four cases, p ~ 0.85 (`:1487`) | (b) | `capstone_b.out:6949` `is false` — REACHABLE | **as registered** |
| `HonestChain(L1)` | reachable in all four cases, p ~ 0.85 (`:1487`) | (c) | `cap_cc01_c.out:17111` `is false` — REACHABLE | **as registered** |
| `HonestChain(L1)` | reachable in all four cases, p ~ 0.85 (`:1487`) | (d) | `capstone_d.out:13377` `is false` — REACHABLE | **as registered** |
| `HonestChain(L2)` | reachable in all four cases, p ~ 0.85 (`:1487`) | (a) | `capstone.out:7580` `is false` — REACHABLE | **as registered** |
| `HonestChain(L2)` | reachable in all four cases, p ~ 0.85 (`:1487`) | (b) | `capstone_b.out:7620` `is false` — REACHABLE | **as registered** |
| `HonestChain(L2)` | reachable in all four cases, p ~ 0.85 (`:1487`) | (c) | `cap_cc01_c.out:17940` `is false` — REACHABLE | **as registered** |
| `HonestChain(L2)` | reachable in all four cases, p ~ 0.85 (`:1487`) | (d) | `capstone_d.out:14135` `is false` — REACHABLE | **as registered** |
| `HonestAccepted` | reachable in all four cases, p ~ 0.85 (`:1487`) | (a) | `capstone.out:8022` `is false` — REACHABLE | **as registered** |
| `HonestAccepted` | reachable in all four cases, p ~ 0.85 (`:1487`) | (b) | `capstone_b.out:8063` `is false` — REACHABLE | **as registered** |
| `HonestAccepted` | reachable in all four cases, p ~ 0.85 (`:1487`) | (c) | `cap_cc01_c.out:18542` `is false` — REACHABLE | **as registered** |
| `HonestAccepted` | reachable in all four cases, p ~ 0.85 (`:1487`) | (d) | `capstone_d.out:14670` `is false` — REACHABLE | **as registered** |
| `HonestWrappedAccepted` | reachable in all four cases, p ~ 0.85 (`:1487`) | (a) | `capstone.out:8606` `is false` — REACHABLE | **as registered** |
| `HonestWrappedAccepted` | reachable in all four cases, p ~ 0.85 (`:1487`) | (b) | `capstone_b.out:8648` `is false` — REACHABLE | **as registered** |
| `HonestWrappedAccepted` | reachable in all four cases, p ~ 0.85 (`:1487`) | (c) | `cap_cc01_c.out:19262` `is false` — REACHABLE | **as registered** |
| `HonestWrappedAccepted` | reachable in all four cases, p ~ 0.85 (`:1487`) | (d) | `capstone_d.out:15318` `is false` — REACHABLE | **as registered** |
| `HonestStandingEstablished` | reachable in all four cases, p ~ 0.85 (`:1487`) | (a) | `capstone.out:9067` `is false` — REACHABLE | **as registered** |
| `HonestStandingEstablished` | reachable in all four cases, p ~ 0.85 (`:1487`) | (b) | `capstone_b.out:9110` `is false` — REACHABLE | **as registered** |
| `HonestStandingEstablished` | reachable in all four cases, p ~ 0.85 (`:1487`) | (c) | `cap_cc01_c.out:19883` `is false` — REACHABLE | **as registered** |
| `HonestStandingEstablished` | reachable in all four cases, p ~ 0.85 (`:1487`) | (d) | `capstone_d.out:15874` `is false` — REACHABLE | **as registered** |
| `HonestWrappedStandingAgreed` | reachable in all four cases, p ~ 0.85 (`:1487`) | (a) | `capstone.out:9580` `is false` — REACHABLE | **as registered** |
| `HonestWrappedStandingAgreed` | reachable in all four cases, p ~ 0.85 (`:1487`) | (b) | `capstone_b.out:9625` `is false` — REACHABLE | **as registered** |
| `HonestWrappedStandingAgreed` | reachable in all four cases, p ~ 0.85 (`:1487`) | (c) | `cap_cc01_c.out:20635` `is false` — REACHABLE | **as registered** |
| `HonestWrappedStandingAgreed` | reachable in all four cases, p ~ 0.85 (`:1487`) | (d) | `capstone_d.out:16550` `is false` — REACHABLE | **as registered** |
| S1 | reachable in every correct-form run (`:1516`) | (a) | `capstone.out:10036` `is false` — REACHABLE | **as registered** |
| S1 | reachable in every correct-form run (`:1516`) | (b) | `capstone_b.out:10081` `is false` — REACHABLE | **as registered** |
| S1 | reachable in every correct-form run (`:1516`) | (d) | `capstone_d.out:17029` `is false` — REACHABLE | **as registered** |
| S2 | reachable in every correct-form run (`:1516`) | (a) | `capstone.out:10490` `is false` — REACHABLE | **as registered** |
| S2 | reachable in every correct-form run (`:1516`) | (b) | `capstone_b.out:10535` `is false` — REACHABLE | **as registered** |
| S2 | reachable in every correct-form run (`:1516`) | (d) | `capstone_d.out:17509` `is false` — REACHABLE | **as registered** |
| S3 | reachable in every correct-form run (`:1516`) | (a) | `capstone.out:10804` `is false` — REACHABLE | **as registered** |
| S3 | reachable in every correct-form run (`:1516`) | (b) | `capstone_b.out:10849` `is false` — REACHABLE | **as registered** |
| S3 | reachable in every correct-form run (`:1516`) | (d) | `capstone_d.out:17915` `is false` — REACHABLE | **as registered** |
| S4 | reachable in every correct-form run (`:1516`) | (a) | `capstone.out:11256` `is false` — REACHABLE | **as registered** |
| S4 | reachable in every correct-form run (`:1516`) | (b) | `capstone_b.out:11301` `is false` — REACHABLE | **as registered** |
| S4 | reachable in every correct-form run (`:1516`) | (d) | `capstone_d.out:18391` `is false` — REACHABLE | **as registered** |
| MISMATCH | reachable in every correct-form run (`:1516`) | (a) | `capstone.out:11621` `is false` — REACHABLE | **as registered** |
| MISMATCH | reachable in every correct-form run (`:1516`) | (b) | `capstone_b.out:11666` `is false` — REACHABLE | **as registered** |
| MISMATCH | reachable in every correct-form run (`:1516`) | (d) | `capstone_d.out:18842` `is false` — REACHABLE | **as registered** |

**Tally:** 173 cells as registered, 0 missed, 0 not declared, 0 from a failed run.
<!--END-S1-->

## 2. Every companion, by case

There is one row per configuration file. C-C1 runs in (c) only; C-C10's isolation control and C-C14 run in
(a) and (b) only; every other configuration runs in (a), (b) and (d). The `rc`, seconds and peak resident
set (GiB = kB / 1 048 576) are read off `ladder.log`. The box the ladder enforced is 71 100 s strict and
65 700 s degraded, which is section 0's per-case-sum reading. The fourth column gives the
predicted-red-box reading. **Observed reds** lists every safety query and observer that came back
`is false`. In (d) that list includes the registered degraded baseline red `AcceptS => IssuerSigned`
(`PREDICTIONS.md:1580`; §4 builder note (2), `:1788-1791`). A degraded companion that did not land reads
**timeout (mechanism-viability failure)** or **terminated by memory guard, classified as mechanism failure
(memory)**, and it has no result. *(REPAIR 2026-10-01, skeptic S-5: the second label is **the owner
instance's clerk disposition**, not the registration's. The registration boxes time only — the word
“memory” does not occur in `PREDICTIONS.md` — and the 80 GB rule and the classification are the owner
instance's (`mem_guard_vm.sh:10-15`). Headroom at each trigger: *The degraded wave*.)*

<!--S2-->
| Companion / configuration | Case | `rc`, seconds, peak (ladder 2 log line) | Inside the box of its predicted-red query? | Observed reds (`.out` line) | Witnesses |
|---|---|---|---|---|---|
| **C-C1** — C-C1, §4 `:1770` | (c) | `rc=0`, 4279 s, 6.0 GiB peak (`ladder.log:70`) | **no**, 4279 s > 30 min (retained `Accept => IssuerSigned`) | C-Q1 link 1b `:3268`, `Accept(S) => IssuerSigned` `:14267`; *not stated for (c):* C-Q6 c1 unrestricted `:12611` | all 14 declared reachable |
| **C-C2** — C-C2, §4 `:1771` | (a) | `rc=0`, 959 s, 0.6 GiB peak (`ladder.log:11`) | yes, 959 s <= 45 min (C-Q3) | none | all 14 declared reachable |
| **C-C2** — C-C2, §4 `:1771` | (b) | `rc=0`, 450 s, 0.6 GiB peak (`ladder.log:38`) | yes, 450 s <= 45 min (C-Q3) | none | all 14 declared reachable |
| **C-C2** — C-C2, §4 `:1771` | (d) | `rc=124`, 65702 s, 21.8 GiB peak (`ladder.log:64`) | **no**, 65702 s > 45 min (C-Q3) | **timeout (mechanism-viability failure)** — no result | - |
| **C-C3** — C-C3, §4 `:1772` | (a) | `rc=0`, 488 s, 0.4 GiB peak (`ladder.log:9`) | yes, 488 s <= 45 min (C-Q5 / link 3) | C-Q9 `:3785`, link 3 `:4189` | all 14 declared reachable |
| **C-C3** — C-C3, §4 `:1772` | (b) | `rc=0`, 271 s, 0.4 GiB peak (`ladder.log:36`) | yes, 271 s <= 45 min (C-Q5 / link 3) | C-Q9 `:3794`, link 3 `:4199` | all 14 declared reachable |
| **C-C3** — C-C3, §4 `:1772` | (d) | `rc=124`, 65703 s, 26.3 GiB peak (`ladder.log:65`) | **no**, 65703 s > 45 min (C-Q5 / link 3) | **timeout (mechanism-viability failure)** — no result | - |
| **C-C4** — C-C4, §4 `:1773` | (a) | `rc=0`, 846 s, 0.5 GiB peak (`ladder.log:10`) | yes, 846 s <= 45 min (link 6b / C-Q3) | none | all 14 declared reachable |
| **C-C4** — C-C4, §4 `:1773` | (b) | `rc=0`, 370 s, 0.5 GiB peak (`ladder.log:37`) | yes, 370 s <= 45 min (link 6b / C-Q3) | none | all 14 declared reachable |
| **C-C4** — C-C4, §4 `:1773` | (d) | `rc=124`, 65702 s, 46.9 GiB peak (`ladder.log:63`) | **no**, 65702 s > 45 min (link 6b / C-Q3) | **timeout (mechanism-viability failure)** — no result | - |
| **C-C5** — C-C5, §4 `:1774` | (a) | `rc=0`, 944 s, 0.8 GiB peak (`ladder.log:12`) | yes, 944 s <= 45 min (link 4) | C-Q8 `:4383`, link 4 `:4988`, `Accept(S) => IssuerSigned` `:7799`, `AcceptedUnderHonestKey => IssuerSigned` `:8270` | all 14 declared reachable |
| **C-C5** — C-C5, §4 `:1774` | (b) | `rc=0`, 442 s, 0.8 GiB peak (`ladder.log:39`) | yes, 442 s <= 45 min (link 4) | C-Q8 `:4323`, link 4 `:4907`, `Accept(S) => IssuerSigned` `:7591`, `AcceptedUnderHonestKey => IssuerSigned` `:8055` | all 14 declared reachable |
| **C-C5** — C-C5, §4 `:1774` | (d) | `rc=143/MECHFAIL-MEMORY`, 64899 s, 76.5 GiB peak (`ladder.log:66`, `ladder.log:78`) | **no**, 64899 s > 45 min (link 4) | **terminated by memory guard, classified as mechanism failure (memory)** — no result | - |
| **C-C6** — C-C6, §4 `:1775` | (a) | `rc=0`, 3195 s, 1.1 GiB peak (`ladder.log:13`) | **no**, 3195 s > 45 min (C-Q7 / link 4) | none | all 14 declared reachable |
| **C-C6** — C-C6, §4 `:1775` | (b) | `rc=0`, 1496 s, 1.1 GiB peak (`ladder.log:40`) | yes, 1496 s <= 45 min (C-Q7 / link 4) | none | all 14 declared reachable |
| **C-C6** — C-C6, §4 `:1775` | (d) | `rc=124`, 65702 s, 25.8 GiB peak (`ladder.log:67`) | **no**, 65702 s > 45 min (C-Q7 / link 4) | **timeout (mechanism-viability failure)** — no result | - |
| **C-C7(i)** — C-C7(i), §4 `:1776` | (a) | `rc=0`, 12423 s, 5.3 GiB peak (`ladder.log:14`) | **no**, 12423 s > 30 min (retained honest-key authorship) | C-Q8 `:12003`, link 4 `:13241`, `Accept(S) => IssuerSigned` `:19867`, `AcceptedUnderHonestKey => IssuerSigned` `:20559` | all 14 declared reachable |
| **C-C7(i)** — C-C7(i), §4 `:1776` | (b) | `rc=0`, 6139 s, 5.4 GiB peak (`ladder.log:41`) | **no**, 6139 s > 30 min (retained honest-key authorship) | C-Q8 `:11849`, link 4 `:13032`, `Accept(S) => IssuerSigned` `:19319`, `AcceptedUnderHonestKey => IssuerSigned` `:19992` | all 14 declared reachable |
| **C-C7(i)** — C-C7(i), §4 `:1776` | (d) | `rc=124`, 65702 s, 28.3 GiB peak (`ladder.log:68`) | **no**, 65702 s > 30 min (retained honest-key authorship) | **timeout (mechanism-viability failure)** — no result | - |
| **C-C7(ii)** — C-C7(ii), §4 `:1776` | (a) | `rc=0`, 13333 s, 8.5 GiB peak (`ladder.log:17`) | **no**, 13333 s > 45 min (link 4) | C-Q8 `:12146`, link 4 `:13402`, `Accept(S) => IssuerSigned` `:20291`, `AcceptedUnderHonestKey => IssuerSigned` `:21146` | all 14 declared reachable |
| **C-C7(ii)** — C-C7(ii), §4 `:1776` | (b) | `rc=0`, 9009 s, 8.5 GiB peak (`ladder.log:44`) | **no**, 9009 s > 45 min (link 4) | C-Q8 `:11992`, link 4 `:13192`, `Accept(S) => IssuerSigned` `:19748`, `AcceptedUnderHonestKey => IssuerSigned` `:20585` | all 14 declared reachable |
| **C-C7(ii)** — C-C7(ii), §4 `:1776` | (d) | `rc=124`, 65702 s, 27.4 GiB peak (`ladder.log:79`) | **no**, 65702 s > 45 min (link 4) | **timeout (mechanism-viability failure)** — no result | - |
| **C-C8** — C-C8, §4 `:1777` | (a) | `rc=0`, 502 s, 0.4 GiB peak (`ladder.log:15`) | yes, 502 s <= 45 min (C-Q5 / link 3) | C-Q9 `:3785`, link 3 `:4189` | all 14 declared reachable |
| **C-C8** — C-C8, §4 `:1777` | (b) | `rc=0`, 261 s, 0.4 GiB peak (`ladder.log:42`) | yes, 261 s <= 45 min (C-Q5 / link 3) | C-Q9 `:3794`, link 3 `:4199` | all 14 declared reachable |
| **C-C8** — C-C8, §4 `:1777` | (d) | `rc=124`, 65703 s, 29.3 GiB peak (`ladder.log:80`) | **no**, 65703 s > 45 min (C-Q5 / link 3) | **timeout (mechanism-viability failure)** — no result | - |
| **C-C8-i** — C-C8-i, §9(2) `:2546` | (a) | `rc=0`, 516 s, 0.4 GiB peak (`ladder.log:16`) | yes, 516 s <= 60 min (C-Q9 (§9(2))) | none | all 14 declared reachable |
| **C-C8-i** — C-C8-i, §9(2) `:2546` | (b) | `rc=0`, 262 s, 0.4 GiB peak (`ladder.log:43`) | yes, 262 s <= 60 min (C-Q9 (§9(2))) | none | all 14 declared reachable |
| **C-C8-i** — C-C8-i, §9(2) `:2546` | (d) | `rc=143`, 48680 s, 76.5 GiB peak (`ladder.log:83`) | **no**, 48680 s > 60 min (C-Q9 (§9(2))) | **terminated by memory guard, classified as mechanism failure (memory)** — no result | - |
| **C-C8-ii** — C-C8-ii, §9(2) `:2547` | (a) | `rc=0`, 277 s, 0.3 GiB peak (`ladder.log:19`) | yes, 277 s <= 60 min (C-Q9 (§9(2))) | C-Q9 `:3796`, link 3 `:4200` | all 14 declared reachable |
| **C-C8-ii** — C-C8-ii, §9(2) `:2547` | (b) | `rc=0`, 272 s, 0.3 GiB peak (`ladder.log:46`) | yes, 272 s <= 60 min (C-Q9 (§9(2))) | C-Q9 `:3805`, link 3 `:4210` | all 14 declared reachable |
| **C-C8-ii** — C-C8-ii, §9(2) `:2547` | (d) | `rc=143`, 39900 s, 76.6 GiB peak (`ladder.log:82`) | **no**, 39900 s > 60 min (C-Q9 (§9(2))) | **terminated by memory guard, classified as mechanism failure (memory)** — no result | - |
| **C-C9** — C-C9, §4 `:1778` | (a) | `rc=0`, 252 s, 0.2 GiB peak (`ladder.log:18`) | yes, 252 s <= 30 min (retained `Stripped`) | link 2b slot-B conj. `:3495`, `Stripped` `:6166` | all 14 declared reachable |
| **C-C9** — C-C9, §4 `:1778` | (b) | `rc=0`, 255 s, 0.2 GiB peak (`ladder.log:45`) | yes, 255 s <= 30 min (retained `Stripped`) | link 2b slot-B conj. `:3524`, `Stripped` `:6295` | all 14 declared reachable |
| **C-C9** — C-C9, §4 `:1778` | (d) | `rc=0`, 1377 s, 1.3 GiB peak (`ladder.log:81`) | yes, 1377 s <= 30 min (retained `Stripped`) | link 2b slot-B conj. `:4566`, `Accept(S) => IssuerSigned` `:8065`, `Stripped` `:8739` | all 14 declared reachable |
| **C-C10** — C-C10, §4 `:1779` | (a) | `rc=0`, 4257 s, 6.1 GiB peak (`ladder.log:20`) | **no**, 4257 s > 30 min (retained `Accept => IssuerSigned`) | C-Q1 link 1a `:2994`, C-Q1 link 1b `:3495`, C-Q6 c1 unrestricted `:11500`, `Accept(S) => IssuerSigned` `:12910` | all 14 declared reachable |
| **C-C10** — C-C10, §4 `:1779` | (b) | `rc=0`, 4202 s, 6.2 GiB peak (`ladder.log:47`) | **no**, 4202 s > 30 min (retained `Accept => IssuerSigned`) | C-Q1 link 1a `:2994`, C-Q1 link 1b `:3495`, C-Q6 c1 unrestricted `:11500`, `Accept(S) => IssuerSigned` `:12910` | all 14 declared reachable |
| **C-C10** — C-C10, §4 `:1779` | (d) | `rc=0`, 3173 s, 5.8 GiB peak (`ladder.log:84`) | **no**, 3173 s > 30 min (retained `Accept => IssuerSigned`) | C-Q1 link 1a `:2803`, `Accept(S) => IssuerSigned` `:9729` | all 14 declared reachable |
| **C-C10 isolation control** — C-C10 isolation control, §4 `:1779` | (a) | `rc=0`, 207 s, 0.3 GiB peak (`ladder.log:21`) | yes, 207 s <= 45 min (link 1a) | C-Q1 link 1a `:2851` | all 14 declared reachable |
| **C-C10 isolation control** — C-C10 isolation control, §4 `:1779` | (b) | `rc=0`, 200 s, 0.3 GiB peak (`ladder.log:48`) | yes, 200 s <= 45 min (link 1a) | C-Q1 link 1a `:2851` | all 14 declared reachable |
| **C-C11** — C-C11 (Q2), §4 `:1805` | (a) | `rc=0`, 304 s, 0.3 GiB peak (`ladder.log:23`) | yes, 304 s <= 90 min (C-Q6) | C-Q6 c1 unrestricted `:5630`, C-Q6 c1 `skI` `:6171`, C-Q6 c1 `skI2` `:6704` | all 14 declared reachable |
| **C-C11** — C-C11 (Q2), §4 `:1805` | (b) | `rc=0`, 282 s, 0.3 GiB peak (`ladder.log:50`) | yes, 282 s <= 90 min (C-Q6) | C-Q6 c1 unrestricted `:5652`, C-Q6 c1 `skI` `:6193`, C-Q6 c1 `skI2` `:6726` | all 14 declared reachable |
| **C-C11** — C-C11 (Q2), §4 `:1805` | (d) | `rc=0`, 4403 s, 5.8 GiB peak (`ladder.log:86`) | yes, 4403 s <= 90 min (C-Q6) | C-Q6 c1 `skI` `:10384`, C-Q6 c1 `skI2` `:11038`, `Accept(S) => IssuerSigned` `:12033` | all 14 declared reachable |
| **C-C11 alt. Q4** — C-C11 alternate Q4, §4 `:1805` | (a) | `rc=0`, 320 s, 0.3 GiB peak (`ladder.log:25`) | yes, 320 s <= 90 min (C-Q6) | C-Q6 c1 unrestricted `:5610`, C-Q6 c1 `skI` `:6127`, C-Q6 c1 `skI2` `:6636` | UNREACHABLE: S2 `:11479`, S4 `:11870` |
| **C-C11 alt. Q4** — C-C11 alternate Q4, §4 `:1805` | (b) | `rc=0`, 310 s, 0.4 GiB peak (`ladder.log:52`) | yes, 310 s <= 90 min (C-Q6) | C-Q6 c1 unrestricted `:5634`, C-Q6 c1 `skI` `:6152`, C-Q6 c1 `skI2` `:6662` | UNREACHABLE: S2 `:11523`, S4 `:11916` |
| **C-C11 alt. Q4** — C-C11 alternate Q4, §4 `:1805` | (d) | `rc=0`, 4244 s, 6.0 GiB peak (`ladder.log:88`) | yes, 4244 s <= 90 min (C-Q6) | C-Q6 c1 `skI` `:10229`, C-Q6 c1 `skI2` `:10833`, `Accept(S) => IssuerSigned` `:11825` | UNREACHABLE: S2 `:18116`, S4 `:18713` |
| **C-C11 alt. abl6** — C-C11 alternate abl6, §4 `:1805` | (a) | `rc=0`, 270 s, 0.3 GiB peak (`ladder.log:22`) | yes, 270 s <= 90 min (C-Q6) | C-Q6 c1 unrestricted `:5548`, C-Q6 c1 `skI` `:5986`, C-Q6 c1 `skI2` `:6416` | all 14 declared reachable |
| **C-C11 alt. abl6** — C-C11 alternate abl6, §4 `:1805` | (b) | `rc=0`, 275 s, 0.3 GiB peak (`ladder.log:49`) | yes, 275 s <= 90 min (C-Q6) | C-Q6 c1 unrestricted `:5620`, C-Q6 c1 `skI` `:6061`, C-Q6 c1 `skI2` `:6494` | all 14 declared reachable |
| **C-C11 alt. abl6** — C-C11 alternate abl6, §4 `:1805` | (d) | `rc=0`, 3769 s, 5.9 GiB peak (`ladder.log:85`) | yes, 3769 s <= 90 min (C-Q6) | C-Q6 c1 `skI` `:9961`, C-Q6 c1 `skI2` `:10475`, `Accept(S) => IssuerSigned` `:11442` | all 14 declared reachable |
| **C-C12** — C-C12, §4 `:1806` | (a) | `rc=0`, 485 s, 0.4 GiB peak (`ladder.log:26`) | yes, 485 s <= 90 min (C-Q6) | C-Q6 c1 unrestricted `:6252`, C-Q6 c2 `:6958` | all 14 declared reachable |
| **C-C12** — C-C12, §4 `:1806` | (b) | `rc=0`, 459 s, 0.3 GiB peak (`ladder.log:53`) | yes, 459 s <= 90 min (C-Q6) | C-Q6 c1 unrestricted `:6348`, C-Q6 c2 `:7066` | all 14 declared reachable |
| **C-C12** — C-C12, §4 `:1806` | (d) | `rc=0`, 4349 s, 6.1 GiB peak (`ladder.log:89`) | yes, 4349 s <= 90 min (C-Q6) | C-Q6 c2 `:10779`, `Accept(S) => IssuerSigned` `:11625` | all 14 declared reachable |
| **C-C13(i)** — C-C13(i), §9(1) `:2501` | (a) | `rc=0`, 256 s, 0.4 GiB peak (`ladder.log:24`) | yes, 256 s <= 30 min (retained `TypeConfused`) | link 6a `:4032`, `TypeConfused` `:6450` | all 14 declared reachable |
| **C-C13(i)** — C-C13(i), §9(1) `:2501` | (b) | `rc=0`, 233 s, 0.4 GiB peak (`ladder.log:51`) | yes, 233 s <= 30 min (retained `TypeConfused`) | link 6a `:4036`, `TypeConfused` `:6457` | all 14 declared reachable |
| **C-C13(i)** — C-C13(i), §9(1) `:2501` | (d) | `rc=0`, 3760 s, 6.6 GiB peak (`ladder.log:87`) | **no**, 3760 s > 30 min (retained `TypeConfused`) | link 6a `:7590`, `Accept(S) => IssuerSigned` `:11016`, `TypeConfused` `:12366` | all 14 declared reachable |
| **C-C13(ii)** — C-C13(ii), §9(1) `:2501` | (a) | `rc=0`, 672 s, 1.0 GiB peak (`ladder.log:28`) | yes, 672 s <= 30 min (retained `TypeConfused`) | link 6a `:5137`, `TypeConfused` `:8434` | all 14 declared reachable |
| **C-C13(ii)** — C-C13(ii), §9(1) `:2501` | (b) | `rc=0`, 634 s, 1.0 GiB peak (`ladder.log:55`) | yes, 634 s <= 30 min (retained `TypeConfused`) | link 6a `:5159`, `TypeConfused` `:8495` | all 14 declared reachable |
| **C-C13(ii)** — C-C13(ii), §9(1) `:2501` | (d) | `rc=0`, 7942 s, 9.1 GiB peak (`ladder.log:92`) | **no**, 7942 s > 30 min (retained `TypeConfused`) | link 6a `:10550`, `Accept(S) => IssuerSigned` `:15542`, `TypeConfused` `:17757` | all 14 declared reachable |
| **C-C14** — C-C14, §9(1) `:2502` | (a) | `rc=0`, 43842 s, 30.8 GiB peak (`ladder.log:29`) | **no**, 43842 s > 30 min (retained `Accept => IssuerSigned`) | C-Q1 link 1a `:3485`, C-Q1 link 1b `:4717`, C-Q2 `:30482`, C-Q6 c1 unrestricted `:37354`, `Accept(S) => IssuerSigned` `:41378` | all 14 declared reachable |
| **C-C14** — C-C14, §9(1) `:2502` | (b) | `rc=0`, 41473 s, 31.0 GiB peak (`ladder.log:56`) | **no**, 41473 s > 30 min (retained `Accept => IssuerSigned`) | C-Q1 link 1a `:3491`, C-Q1 link 1b `:4729`, C-Q2 `:30574`, C-Q6 c1 unrestricted `:37502`, `Accept(S) => IssuerSigned` `:41560` | all 14 declared reachable |
| **C-C15(i)** — C-C15(i), §9(1) `:2503` | (a) | `rc=0`, 287 s, 0.4 GiB peak (`ladder.log:101`; supersedes the broken-fixture run `ladder.log:27` (BF-4, under *Broken fixtures*)) | yes, 287 s <= 30 min (retained `SignerForged`) | C-Q1 link 1a `:3331`, C-Q1 link 1b `:3879`, C-Q1 link 2a `:4434`, C-Q9 `:5535`, link 3 `:6092`, link 5 `:6719`, C-Q2 `:7712`, C-Q5 `:8561`, `SignerForged` `:10745` | all 14 declared reachable |
| **C-C15(i)** — C-C15(i), §9(1) `:2503` | (b) | `rc=0`, 279 s, 0.4 GiB peak (`ladder.log:102`; supersedes the broken-fixture run `ladder.log:54` (BF-4, under *Broken fixtures*)) | yes, 279 s <= 30 min (retained `SignerForged`) | C-Q1 link 1a `:3332`, C-Q1 link 1b `:3882`, C-Q1 link 2a `:4438`, C-Q9 `:5548`, link 3 `:6106`, link 5 `:6735`, C-Q2 `:7731`, C-Q5 `:8585`, `SignerForged` `:10781` | all 14 declared reachable |
| **C-C15(i)** — C-C15(i), §9(1) `:2503` | (d) | `rc=0`, 7825 s, 12.4 GiB peak (`ladder.log:103`; supersedes the broken-fixture run `ladder.log:91` (BF-4, under *Broken fixtures*)) | **no**, 7825 s > 30 min (retained `SignerForged`) | C-Q1 link 1a `:3253`, C-Q1 link 2a `:3860`, C-Q7 `:9941`, C-Q9 `:10794`, link 3 `:11403`, link 5 `:12258`, link 6b `:13113`, C-Q3 `ReattributedA` `:13775`, C-Q3 `ReattributedB` `:14476`, C-Q4 `Rescoped` `:15138`, C-Q4 `InnerSigTransplanted` `:15840`, C-Q5 `:16553`, C-Q6 c3 `ScopeMisreported` `:19679`, `Accept(S) => IssuerSigned` `:20432`, `SignerForged` `:21704` | all 14 declared reachable |
| **C-C15(ii)** — C-C15(ii), §9(1) `:2503` | (a) | `rc=0`, 296 s, 0.4 GiB peak (`ladder.log:31`) | yes, 296 s <= 45 min (link 6b) | link 6b `:4628`, C-Q4 `Rescoped` `:5474`, C-Q6 c3 `ScopeMisreported` `:7580` | all 14 declared reachable |
| **C-C15(ii)** — C-C15(ii), §9(1) `:2503` | (b) | `rc=0`, 284 s, 0.3 GiB peak (`ladder.log:58`) | yes, 284 s <= 45 min (link 6b) | link 6b `:4642`, C-Q4 `Rescoped` `:5492`, C-Q6 c3 `ScopeMisreported` `:7608` | all 14 declared reachable |
| **C-C15(ii)** — C-C15(ii), §9(1) `:2503` | (d) | `rc=0`, 4091 s, 5.9 GiB peak (`ladder.log:90`) | **no**, 4091 s > 45 min (link 6b) | link 6b `:8355`, C-Q4 `Rescoped` `:9519`, C-Q6 c3 `ScopeMisreported` `:12635`, `Accept(S) => IssuerSigned` `:13285` | all 14 declared reachable |
| **C-C15(iii)** — C-C15(iii), §9(1) `:2503` | (a) | `rc=0`, 343 s, 0.4 GiB peak (`ladder.log:32`) | yes, 343 s <= 45 min (link 6b) | link 6b `:4735`, C-Q4 `Rescoped` `:5567`, C-Q6 c3 `ScopeMisreported` `:7721`, observer `ScopeIdentityOnly` `:8471` | all 14 declared reachable |
| **C-C15(iii)** — C-C15(iii), §9(1) `:2503` | (b) | `rc=0`, 316 s, 0.4 GiB peak (`ladder.log:59`) | yes, 316 s <= 45 min (link 6b) | link 6b `:4767`, C-Q4 `Rescoped` `:5607`, C-Q6 c3 `ScopeMisreported` `:7781`, observer `ScopeIdentityOnly` `:8535` | all 14 declared reachable |
| **C-C15(iii)** — C-C15(iii), §9(1) `:2503` | (d) | `rc=0`, 4290 s, 5.7 GiB peak (`ladder.log:93`) | **no**, 4290 s > 45 min (link 6b) | link 6b `:8485`, C-Q4 `Rescoped` `:9555`, C-Q6 c3 `ScopeMisreported` `:12693`, `Accept(S) => IssuerSigned` `:14366`, observer `ScopeIdentityOnly` `:13719` | all 14 declared reachable |
| **C-C16** — C-C16, §9(3) `:2609` | (a) | `rc=0`, 284 s, 0.3 GiB peak (`ladder.log:30`) | yes, 284 s <= 30 min (retained `Spliced`) | link 5 `:4004`, `Spliced` `:6595` | all 14 declared reachable |
| **C-C16** — C-C16, §9(3) `:2609` | (b) | `rc=0`, 273 s, 0.3 GiB peak (`ladder.log:57`) | yes, 273 s <= 30 min (retained `Spliced`) | link 5 `:4016`, `Spliced` `:6628` | all 14 declared reachable |
| **C-C16** — C-C16, §9(3) `:2609` | (d) | `rc=0`, 6671 s, 8.1 GiB peak (`ladder.log:94`) | **no**, 6671 s > 30 min (retained `Spliced`) | link 5 `:10251`, `Accept(S) => IssuerSigned` `:15017`, `Spliced` `:16423` | all 14 declared reachable |
| **C-C17** — C-C17, §9(4) `:2666` | (a) | `rc=0`, 27503 s, 18.8 GiB peak (`ladder.log:34`) | **no**, 27503 s > 30 min (retained `SignerForged`) | C-Q1 link 2a `:6520`, `Accept(S) => IssuerSigned` `:26669`, `SignerForged` `:28291` | all 14 declared reachable |
| **C-C17** — C-C17, §9(4) `:2666` | (b) | `rc=0`, 27084 s, 19.3 GiB peak (`ladder.log:61`) | **no**, 27084 s > 30 min (retained `SignerForged`) | C-Q1 link 2a `:6541`, `Accept(S) => IssuerSigned` `:26798`, `SignerForged` `:28433` | all 14 declared reachable |
| **C-C17** — C-C17, §9(4) `:2666` | (d) | `rc=143`, 64379 s, 76.6 GiB peak (`ladder.log:95`) | **no**, 64379 s > 30 min (retained `SignerForged`) | **terminated by memory guard, classified as mechanism failure (memory)** — no result | - |
| **C-C18** — C-C18, §9(5) `:2725` | (a) | `rc=0`, 275 s, 0.3 GiB peak (`ladder.log:33`) | yes, 275 s <= 30 min (C-Q10) | C-Q10 `:5373`, C-Q6 c1 unrestricted `:5769`, C-Q6 c1 `skI` `:6165` | all 14 declared reachable |
| **C-C18** — C-C18, §9(5) `:2725` | (b) | `rc=0`, 261 s, 0.3 GiB peak (`ladder.log:60`) | yes, 261 s <= 30 min (C-Q10) | C-Q10 `:5411`, C-Q6 c1 unrestricted `:5808`, C-Q6 c1 `skI` `:6205` | all 14 declared reachable |
| **C-C18** — C-C18, §9(5) `:2725` | (d) | `rc=0`, 3662 s, 5.8 GiB peak (`ladder.log:96`) | **no**, 3662 s > 30 min (C-Q10) | C-Q10 `:9878`, C-Q6 c1 `skI` `:10361`, `Accept(S) => IssuerSigned` `:11545` | all 14 declared reachable |
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
| **C-C2** — C-C2, §4 `:1771` | (d) | C-Q3 `ReattributedA` or C-Q3 `ReattributedB`; link 5; baseline `AcceptS => IssuerSigned` | **timeout (mechanism-viability failure)** | none: no result to compare |  |
| **C-C3** — C-C3, §4 `:1772` | (a) | C-Q9; link 3 | **AS REGISTERED** | none | strict MIXED: C-Q5 green |
| **C-C3** — C-C3, §4 `:1772` | (b) | C-Q9; link 3 | **AS REGISTERED** | none | as (a), predicted |
| **C-C3** — C-C3, §4 `:1772` | (d) | C-Q5; C-Q9; link 3; baseline `AcceptS => IssuerSigned` | **timeout (mechanism-viability failure)** | none: no result to compare |  |
| **C-C4** — C-C4, §4 `:1773` | (a) | FORK: {C-Q4 `Rescoped`; C-Q4 `InnerSigTransplanted`; C-Q3 `ReattributedA` or C-Q3 `ReattributedB`; link 6b; link 5} or green throughout | **AS REGISTERED** (fork branch: green throughout) | none | registered FORK: the five reds, or green throughout (predicted configuration-level reading) |
| **C-C4** — C-C4, §4 `:1773` | (b) | FORK: {C-Q4 `Rescoped`; C-Q4 `InnerSigTransplanted`; C-Q3 `ReattributedA` or C-Q3 `ReattributedB`; link 6b; link 5} or green throughout | **AS REGISTERED** (fork branch: green throughout) | none | registered FORK, as (a) |
| **C-C4** — C-C4, §4 `:1773` | (d) | C-Q4 `Rescoped`; C-Q4 `InnerSigTransplanted`; C-Q3 `ReattributedA` or C-Q3 `ReattributedB`; link 6b; link 5; baseline `AcceptS => IssuerSigned` | **timeout (mechanism-viability failure)** | none: no result to compare |  |
| **C-C5** — C-C5, §4 `:1774` | (a) | C-Q8; link 4 | **DIVERGENT** | **red not registered in this case:** `Accept(S) => IssuerSigned` `:7799`; **red not registered in this case:** `AcceptedUnderHonestKey => IssuerSigned` `:8270` | strict MIXED: `InnerSigTransplanted` descended green |
| **C-C5** — C-C5, §4 `:1774` | (b) | C-Q8; link 4 | **DIVERGENT** | **red not registered in this case:** `Accept(S) => IssuerSigned` `:7591`; **red not registered in this case:** `AcceptedUnderHonestKey => IssuerSigned` `:8055` | strict MIXED, descended |
| **C-C5** — C-C5, §4 `:1774` | (d) | C-Q4 `InnerSigTransplanted`; C-Q8; link 4; baseline `AcceptS => IssuerSigned` | **terminated by memory guard, classified as mechanism failure (memory)** | none: no result to compare |  |
| **C-C6** — C-C6, §4 `:1775` | (a) | none (green throughout) | **AS REGISTERED** | none | green control, predicted (round 9 disposition 4) |
| **C-C6** — C-C6, §4 `:1775` | (b) | none (green throughout) | **AS REGISTERED** | none | green control, predicted |
| **C-C6** — C-C6, §4 `:1775` | (d) | C-Q7; C-Q4 `InnerSigTransplanted`; C-Q8; link 4; baseline `AcceptS => IssuerSigned` | **timeout (mechanism-viability failure)** | none: no result to compare |  |
| **C-C7(i)** — C-C7(i), §4 `:1776` | (a) | C-Q8; link 4; `AcceptedUnderHonestKey => IssuerSigned`; `Accept(S) => IssuerSigned` | **AS REGISTERED** | none |  |
| **C-C7(i)** — C-C7(i), §4 `:1776` | (b) | C-Q8; link 4; `AcceptedUnderHonestKey => IssuerSigned`; `Accept(S) => IssuerSigned` | **AS REGISTERED** | none |  |
| **C-C7(i)** — C-C7(i), §4 `:1776` | (d) | C-Q8; link 4; `AcceptedUnderHonestKey => IssuerSigned`; baseline `AcceptS => IssuerSigned` | **timeout (mechanism-viability failure)** | none: no result to compare |  |
| **C-C7(ii)** — C-C7(ii), §4 `:1776` | (a) | C-Q8; link 4; `AcceptedUnderHonestKey => IssuerSigned`; `Accept(S) => IssuerSigned` | **AS REGISTERED** | none | C-Q7 GREEN in strict, a registered per-case outcome |
| **C-C7(ii)** — C-C7(ii), §4 `:1776` | (b) | C-Q8; link 4; `AcceptedUnderHonestKey => IssuerSigned`; `Accept(S) => IssuerSigned` | **AS REGISTERED** | none |  |
| **C-C7(ii)** — C-C7(ii), §4 `:1776` | (d) | C-Q8; link 4; C-Q7; `AcceptedUnderHonestKey => IssuerSigned`; baseline `AcceptS => IssuerSigned` | **timeout (mechanism-viability failure)** | none: no result to compare |  |
| **C-C8** — C-C8, §4 `:1777` | (a) | C-Q9; link 3 | **AS REGISTERED** | none | (beta)-only strict split: C-Q5 and link 5 green |
| **C-C8** — C-C8, §4 `:1777` | (b) | C-Q9; link 3 | **AS REGISTERED** | none | as (a), descended (cap22i) |
| **C-C8** — C-C8, §4 `:1777` | (d) | C-Q9; C-Q5; link 3; link 5; baseline `AcceptS => IssuerSigned` | **timeout (mechanism-viability failure)** | none: no result to compare |  |
| **C-C8-i** — C-C8-i, §9(2) `:2546` | (a) | none (green throughout) | **AS REGISTERED** | none | isolation result: all green |
| **C-C8-i** — C-C8-i, §9(2) `:2546` | (b) | none (green throughout) | **AS REGISTERED** | none | isolation result: all green |
| **C-C8-i** — C-C8-i, §9(2) `:2546` | (d) | none (green throughout); baseline `AcceptS => IssuerSigned`; left open: link 5 | **terminated by memory guard, classified as mechanism failure (memory)** | none: no result to compare | link 5's `mh` half 'stays the registered (d) red' (:2546) is ambiguous for this configuration |
| **C-C8-ii** — C-C8-ii, §9(2) `:2547` | (a) | C-Q9; left open: link 3 | **AS REGISTERED** | none | link 3 not named in the cell; §3 link 3 says its producer 'is C-Q9' (:464) |
| **C-C8-ii** — C-C8-ii, §9(2) `:2547` | (b) | C-Q9; left open: link 3 | **AS REGISTERED** | none | as (a) |
| **C-C8-ii** — C-C8-ii, §9(2) `:2547` | (d) | C-Q9; baseline `AcceptS => IssuerSigned`; left open: link 3 | **terminated by memory guard, classified as mechanism failure (memory)** | none: no result to compare | as (a) |
| **C-C9** — C-C9, §4 `:1778` | (a) | link 2b slot-B conj.; `Stripped` | **AS REGISTERED** | none |  |
| **C-C9** — C-C9, §4 `:1778` | (b) | link 2b slot-B conj.; `Stripped` | **AS REGISTERED** | none |  |
| **C-C9** — C-C9, §4 `:1778` | (d) | link 2b slot-B conj.; `Stripped`; baseline `AcceptS => IssuerSigned` | **AS REGISTERED** | none |  |
| **C-C10** — C-C10, §4 `:1779` | (a) | C-Q1 link 1a; C-Q1 link 1b; `Accept(S) => IssuerSigned` | **DIVERGENT** | **red not registered in this case:** C-Q6 c1 unrestricted `:11500` |  |
| **C-C10** — C-C10, §4 `:1779` | (b) | C-Q1 link 1a; C-Q1 link 1b; `Accept(S) => IssuerSigned` | **DIVERGENT** | **red not registered in this case:** C-Q6 c1 unrestricted `:11500` |  |
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
| **C-C14** — C-C14, §9(1) `:2502` | (a) | C-Q2; C-Q1 link 1a; C-Q1 link 1b; `Accept(S) => IssuerSigned` | **DIVERGENT** | **red not registered in this case:** C-Q6 c1 unrestricted `:37354` | the spike's one combined formula; 'this file predicts no different answer than all three' |
| **C-C14** — C-C14, §9(1) `:2502` | (b) | C-Q2; C-Q1 link 1a; C-Q1 link 1b; `Accept(S) => IssuerSigned` | **DIVERGENT** | **red not registered in this case:** C-Q6 c1 unrestricted `:37502` |  |
| **C-C15(i)** — C-C15(i), §9(1) `:2503` | (a) | C-Q9; link 3; C-Q1 link 1a; C-Q1 link 1b; C-Q1 link 2a; link 5; C-Q5; `SignerForged`; left open: C-Q6 c3 `ScopeMisreported` | **DIVERGENT** | **red not registered in this case:** C-Q2 `:7712` | strict: the eight (seven relations) descended red; `Rescoped`, `InnerSigTransplanted`, C-Q3, `TypeConfused`, C-Q7, C-Q8 descended green; link 6b not produced in strict; C-Q6 c3 for (i) in strict is not case-assigned (set (1) says both configurations red it; the D11 sentence says the key half is severed by nothing the strict fixture can present) |
| **C-C15(i)** — C-C15(i), §9(1) `:2503` | (b) | C-Q9; link 3; C-Q1 link 1a; C-Q1 link 1b; C-Q1 link 2a; link 5; C-Q5; `SignerForged`; left open: C-Q6 c3 `ScopeMisreported` | **DIVERGENT** | **red not registered in this case:** C-Q2 `:7731` | as (a) |
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
| **C-C17** — C-C17, §9(4) `:2666` | (a) | C-Q1 link 2a; `SignerForged` | **DIVERGENT** | **red not registered in this case:** `Accept(S) => IssuerSigned` `:26669` | `PossessionTransplanted` (set 1) is not a capstone query: B-3 |
| **C-C17** — C-C17, §9(4) `:2666` | (b) | C-Q1 link 2a; `SignerForged` | **DIVERGENT** | **red not registered in this case:** `Accept(S) => IssuerSigned` `:26798` |  |
| **C-C17** — C-C17, §9(4) `:2666` | (d) | C-Q1 link 2a; `SignerForged`; baseline `AcceptS => IssuerSigned` | **terminated by memory guard, classified as mechanism failure (memory)** | none: no result to compare |  |
| **C-C18** — C-C18, §9(5) `:2725` | (a) | C-Q10; C-Q6 c1 `skI`; C-Q6 c1 unrestricted | **AS REGISTERED** | none |  |
| **C-C18** — C-C18, §9(5) `:2725` | (b) | C-Q10; C-Q6 c1 `skI`; C-Q6 c1 unrestricted | **AS REGISTERED** | none |  |
| **C-C18** — C-C18, §9(5) `:2725` | (d) | C-Q10; C-Q6 c1 `skI`; baseline `AcceptS => IssuerSigned` | **AS REGISTERED** | none |  |

**Counts, per case** (one row per configuration file): (a): 21 as registered, 5 divergent, 0 mechanism failure; (b): 21 as registered, 5 divergent, 0 mechanism failure; (c): 1 as registered, 0 divergent, 0 mechanism failure; (d): 13 as registered, 0 divergent, 11 mechanism failure.
<!--END-VERDICTS-->

### The eleven divergent rows, against the registration's own words

*(REPAIR 2026-10-01, skeptic S-2. The heading above and the counts sentence below are **pre-BF-4 and
superseded**: on the current runs the divergent rows are **ten**, carrying **12** `RESULT` lines —
C-C5 (a)/(b) 2 + 2, C-C10 (a)/(b) 1 + 1, C-C14 (a)/(b) 1 + 1, C-C15(i) (a)/(b) 1 + 1 (C-Q2 only), C-C17
(a)/(b) 1 + 1 — recomputed from section 2a's verdict table (5 divergent in (a), 5 in (b)). The C-C15(i)
cells of the table below now carry the `ladder2-superseded/` prefix their line numbers belong to.)*

*(Dated note 2026-10-01, after the divergence diagnosis (`proverif/dev/divergences/DIAGNOSIS.md`) and the
BF-4 repair. **G3 is repaired.** The two C-C15(i) rows in the table below describe the superseded
broken-fixture runs, and their `.out` line numbers refer to `proverif/ladder2-superseded/`. On the
repaired fixture, C-C15(i) (d) is **as registered**, and C-C15(i) (a)/(b) keep exactly one divergent red,
C-Q2 (`cap_cc15i_a.out:7712`, `cap_cc15i_b.out:7731`). The 17 G3 `RESULT` lines cleared (7 in (a), 7 in
(b), 3 in (d)). The divergent rows are therefore now **ten**, carrying **12** `RESULT` lines. Still open,
and not resolved by this file: **G2** (C-C10 and C-C14 in (a)/(b), C-Q6 conjunct 1 unrestricted) is a
**finding** for the reviewer and the author; **G1** (the two authorship correspondences missing from
C-C5's set and the unrestricted one from C-C17's), **G4** (C-Q2 under C-C15(i) in strict) and the
**C-C15(i) conjunct-3** item (set (1) against the strict Cases cell) are **amendment-shaped**, to be
labelled per DECISION.md provenance and never entered as author rulings.)*

**No witness died in any landed run, and no registered red failed to fire in any landed run.** Every
divergence is the same kind: **a red where the case's registration has green, or does not name the
query**. There are 29 such `RESULT` lines (27 if C-Q3's two roles are counted as one query) across
11 configuration-case rows. *(Superseded, REPAIR 2026-10-01, skeptic S-2: those counts include the 17 G3
lines that BF-4 cleared. Current: 12 lines across 10 rows.)*

| Configuration, case | Red where the case's registration does not register red (`.out` line) | What the registration says of each |
|---|---|---|
| **C-C5**, (a) and (b) | `Accept => IssuerSigned`: `cap_cc05_a.out:7799`, `cap_cc05_b.out:7591`. `AcceptedUnderHonestKey => IssuerSigned`: `cap_cc05_a.out:8270`, `cap_cc05_b.out:8055`. | Neither query is in C-C5's set (1) or set (2) (`PREDICTIONS.md:1774`). The Cases cell descends C-Q8 red in strict and predicts *"every other member of the retained set column"* green. C-Q8 and link 4 fired red as registered, and `InnerSigTransplanted` stayed green as descended. |
| **C-C10**, (a) and (b) | C-Q6 conjunct 1, unrestricted form: `cap_cc10_a.out:11500`, `cap_cc10_b.out:11500`. | **This is a set-(2) green gone red.** C-C10's set (2) for (a) reads *"predicted green, on the same descent: links 2a–6b, C-Q2–C-Q6, C-Q9"*, and (b) reads the same (`:1779`). Links 1a and 1b and `Accept => IssuerSigned` fired red as registered. |
| **C-C14**, (a) and (b) | C-Q6 conjunct 1, unrestricted form: `cap_cc14_a.out:37354`, `cap_cc14_b.out:37502`. | C-Q6 is not named in C-C14's set (1) or set (2) (`:2502`), and set (2) *"descends from nothing"*. C-Q2, links 1a and 1b and `Accept => IssuerSigned` all fired red, which is the registered *"all three"*. |
| **C-C15(i)**, (a) and (b) — **superseded runs** (BF-4) | C-Q7: `ladder2-superseded/cap_cc15i_a.out:5436`, `ladder2-superseded/cap_cc15i_b.out:5444`. C-Q8: `:5991`, `:6001`. Link 4: `:7662`, `:7676`. C-Q2: `:9213`, `:9231`. C-Q3, both roles: `:9807` and `:10405`, `:9827` and `:10427`. `Accept => IssuerSigned`: `:13025`, `:13065`. `AcceptedUnderHonestKey => IssuerSigned`: `:13594`, `:13635`. *(All in `ladder2-superseded/`. On the repaired runs only C-Q2 remains: `cap_cc15i_a.out:7712`, `cap_cc15i_b.out:7731`.)* | **C-Q7 and C-Q8** are **descended GREEN in (a) and (b)** by the dated note of 2026-09-17 (`cap25a_sp7_strict_q6b_sigjudges.out:1306`, `:1317`; `cap25b…` the same lines), so these are reds against descended greens. **C-Q8 and link 4** are also named members of (i)'s set (2) for (a)/(b) (*"C-Q8, link 2b, link 4, `Stripped`, `Spliced` and `VersionLied`"*). **C-Q3** is in (i)'s set (1) but is **descended green in strict** (`cap14b_sp7_q1_strict_q6b.out:568`), and the Cases lists govern per case. **C-Q2** and the two **authorship** correspondences are not named for (i). All eight registered strict reds fired: C-Q9, link 3, links 1a, 1b and 2a, link 5, C-Q5 and `SignerForged`. Link 6b, `Rescoped`, `InnerSigTransplanted` and `TypeConfused` stayed green as registered. C-Q6 conjunct 3 stayed green, a member the registration leaves open (see the verdict table's note). |
| **C-C15(i)**, (d) — **superseded run** (BF-4; on the repaired run this row is as registered) | C-Q8: `ladder2-superseded/cap_cc15i_d.out:10654`. Link 4: `:12473`. `AcceptedUnderHonestKey => IssuerSigned`: `:21878` (all in `ladder2-superseded/`). | **C-Q8 and link 4 are set-(2) greens gone red.** (i)'s set (2) in (d) reads *"the remaining six — C-Q8, link 2b, link 4, `Stripped`, `Spliced`, `VersionLied` — stand"* (`:2503`). Honest-key authorship is not named. All thirteen registered (d) reds fired, together with the baseline `AcceptS` red. |
| **C-C17**, (a) and (b) | `Accept => IssuerSigned`: `cap_cc17_a.out:26669`, `cap_cc17_b.out:26798`. | Not named in C-C17's set (1) or set (2) (`:2666`). The strict descent `cap18e` declares no such query. Link 2a and `SignerForged` fired red as registered, and link 2b's three conjuncts stayed green. |

**What can be said without diagnosing.** First, every off-registration red outside C-C15(i) is one of
the two retained authorship correspondences or the unrestricted C-Q6 standing form, and each of those
quantifies over every acceptance. Second, every divergent file that also landed in ladder 1 reproduces
there byte for byte (*Cross-check*: `cap_cc05_{a,b}`, `cap_cc10_{a,b}`, `cap_cc15i_{a,b}`,
`cap_cc17_{a,b}`), so **none of these reds is produced by recut R-9**. `cap_cc14_{a,b}` and
`cap_cc15i_d` have no landed ladder-1 run to compare. **Each item is owed a diagnosis under §4 before any
reading, and none has been made.** That diagnosis is builder and owner work, not an author decision.
*(2026-10-01: the diagnosis has since been made, in `proverif/dev/divergences/DIAGNOSIS.md`; G3 was a
broken fixture and is repaired (BF-4); see the dated note above the table.)*

### Observations the registration asks to be recorded, and readings that could be contested

- **C-C3 and C-C8 coincide in the capstone** (§4 note (1), `PREDICTIONS.md:1781-1787`: *"whether their
  capstone sets coincide is recorded as an observation of the run"*). They coincide because the models
  do. `diff cap_cc03_a.pv cap_cc08_a.pv` differs only in the generated header's FILE, MUTATES, SERVES and
  REGISTERED BOX lines. `derive.py` transcribes both registered mutations to the same model text. Their
  `RESULT` streams are identical in (a) and in (b), and both (d) runs timed out on link 1a. Whether two
  companions registered *"by different routes"* may share one transcription is a question for the
  reviewer.
- **C-C8's isolation discipline** (§9(2)). C-C8-i and C-C8-ii both ran, and are recorded, in (a) and (b).
  C-C8-i is all green, which is the isolation result. C-C8-ii has C-Q9 red with C-Q5 green, so (β), the
  possession message, is severed by the possession removal alone. In strict, C-Q5 stays green under
  C-C8's combined removal too, which is registered. **(α) is therefore observable only in (d), and in (d)
  C-C8, C-C8-i and C-C8-ii all failed** (rc=124, rc=143, rc=143).
- **C-C8-ii's link 3** is red beside C-Q9 (`cap_cc08ii_a.out:4200`, `cap_cc08ii_b.out:4210`). The
  configuration's cell names only C-Q9. §3's link-3 section says its producer *"is C-Q9"* (`:464`), and
  recut R-5 fires both events from the one failed check. This file accepts the red as registered by that
  identity. It is named here so that a reader can disagree.
- **C-C10's distinguishing signal works as registered.** In the companion, link 1b is red
  (`cap_cc10_a.out:3495`), which means the honest channel's check was the one deleted. In the isolation
  control, link 1b is green (`cap_cc10iso_a.out:3000`) and link 1a red (`:2851`), which means the
  compromised channel's check was deleted. The (b) runs give the same at the same lines.
- **The registered forks fell as follows.** C-C4 in (a) and (b) is **green throughout**, the green-control
  branch. C-C15(ii) in (a) and (b) is the **red branch**: link 6b, `Rescoped` and C-Q6 conjunct 3 are red
  (`cap_cc15ii_a.out:4628`, `:5474`, `:7580`), so the depth-2 honest route exists in the strict fixture.
- **C-C11's Q4 alternate.** S2 and S4 are unreachable in all three cases, as registered
  (`cap_cc11q4_a.out:11479`, `:11870`; `cap_cc11q4_b.out:11523`, `:11916`; `cap_cc11q4_d.out:18116`,
  `:18713`). Every other witness is reachable.
- **Case (c) carries an unstated red.** The unrestricted C-Q6 conjunct-1 form is red in `cap_cc01_c.out:12611`.
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
| **D1** | S-P3 Q2 `Reattributed` — C-Q3 `ReattributedA` `capstone.out:3889` `is true`; C-Q3 `ReattributedB` `capstone.out:3954` `is true` | C-C2 | `cap_cc02_a`: C-Q3 `ReattributedA` `:4420` green (registered green in this case); C-Q3 `ReattributedB` `:4518` green (registered green in this case); link 5 `:4028` green (registered green in this case)<br>`cap_cc02_b`: C-Q3 `ReattributedA` `:4244` green (registered green in this case); C-Q3 `ReattributedB` `:4331` green (registered green in this case); link 5 `:3896` green (registered green in this case)<br>`cap_cc02_d`: **timeout (mechanism-viability failure)** |
| **D2** | S-P3 Q2 `Reattributed` (C-Q4 `Rescoped`) — C-Q4 `Rescoped` `capstone.out:4019` `is true` | C-C4 | `cap_cc04_a`: C-Q4 `Rescoped` `:4403` green (registered FORK: red, or the configuration green throughout)<br>`cap_cc04_b`: C-Q4 `Rescoped` `:4273` green (registered FORK: red, or the configuration green throughout)<br>`cap_cc04_d`: **timeout (mechanism-viability failure)** |
| **D3** | S-P3 Q1(ii) chain correspondence — `Accept(S) => IssuerSigned` `capstone.out:5544` `is true` | C-C1 | `cap_cc01_c`: `Accept(S) => IssuerSigned` `:14267` **RED** (registered red) |
| **D4** | link 1b: S-P3 Q1(ii); link 1a: structural — C-Q1 link 1a `capstone.out:2551` `is true`; C-Q1 link 1b `capstone.out:2718` `is true` | C-C1, C-C10 | `cap_cc01_c`: C-Q1 link 1b `:3268` **RED** (registered red); C-Q1 link 1a `:2710` green (registered green in this case)<br>`cap_cc10_a`: C-Q1 link 1b `:3495` **RED** (registered red); C-Q1 link 1a `:2994` **RED** (registered red)<br>`cap_cc10_b`: C-Q1 link 1b `:3495` **RED** (registered red); C-Q1 link 1a `:2994` **RED** (registered red)<br>`cap_cc10_d`: C-Q1 link 1a `:2803` **RED** (registered red) |
| **D5** | **C-Q7** — C-Q7 `capstone.out:3304` `is true` | C-C5 | `cap_cc05_a`: C-Q4 `InnerSigTransplanted` `:5724` green (registered green in this case)<br>`cap_cc05_b`: C-Q4 `InnerSigTransplanted` `:5587` green (registered green in this case)<br>`cap_cc05_d`: **terminated by memory guard, classified as mechanism failure (memory)** |
| **D6** | **C-Q8**, structural — C-Q8 `capstone.out:3369` `is true` | C-C7(i), C-C7(ii) | `cap_cc07i_a`: C-Q8 `:12003` **RED** (registered red); link 4 `:13241` **RED** (registered red)<br>`cap_cc07i_b`: C-Q8 `:11849` **RED** (registered red); link 4 `:13032` **RED** (registered red)<br>`cap_cc07i_d`: **timeout (mechanism-viability failure)**<br>`cap_cc07ii_a`: C-Q8 `:12146` **RED** (registered red); link 4 `:13402` **RED** (registered red)<br>`cap_cc07ii_b`: C-Q8 `:11992` **RED** (registered red); link 4 `:13192` **RED** (registered red)<br>`cap_cc07ii_d`: **timeout (mechanism-viability failure)** |
| **D7** | S-P2 `Stripped` / `SignerForged` + Q6 `Spliced` — `Stripped` `capstone.out:5704` `is true`; `SignerForged` `capstone.out:5769` `is true`; `Spliced` `capstone.out:5834` `is true` | C-C9, C-C16, C-C17 | `cap_cc09_a`: link 2b slot-B conj. `:3495` **RED** (registered red); link 5 `:3849` green (registered green in this case); C-Q1 link 2a `:2755` green (registered green in this case)<br>`cap_cc09_b`: link 2b slot-B conj. `:3524` **RED** (registered red); link 5 `:3902` green (registered green in this case); C-Q1 link 2a `:2769` green (registered green in this case)<br>`cap_cc09_d`: link 2b slot-B conj. `:4566` **RED** (registered red); link 5 `:5256` green (registered green in this case); C-Q1 link 2a `:2592` green (registered green in this case)<br>`cap_cc16_a`: link 2b slot-B conj. `:3231` green (registered green in this case); link 5 `:4004` **RED** (registered red); C-Q1 link 2a `:2766` green (registered green in this case)<br>`cap_cc16_b`: link 2b slot-B conj. `:3237` green (registered green in this case); link 5 `:4016` **RED** (registered red); C-Q1 link 2a `:2769` green (registered green in this case)<br>`cap_cc16_d`: link 2b slot-B conj. `:8420` green (registered green in this case); link 5 `:10251` **RED** (registered red); C-Q1 link 2a `:2840` green (registered green in this case)<br>`cap_cc17_a`: link 2b slot-B conj. `:17709` green (registered green in this case); link 5 `:19683` green (registered green in this case); C-Q1 link 2a `:6520` **RED** (registered red)<br>`cap_cc17_b`: link 2b slot-B conj. `:17745` green (registered green in this case); link 5 `:19743` green (registered green in this case); C-Q1 link 2a `:6541` **RED** (registered red)<br>`cap_cc17_d`: **terminated by memory guard, classified as mechanism failure (memory)** |
| **D8** | S-P7 `TypeConfused` — `TypeConfused` `capstone.out:5899` `is true` | C-C13(i), C-C13(ii) | `cap_cc13i_a`: link 6a `:4032` **RED** (registered red)<br>`cap_cc13i_b`: link 6a `:4036` **RED** (registered red)<br>`cap_cc13i_d`: link 6a `:7590` **RED** (registered red)<br>`cap_cc13ii_a`: link 6a `:5137` **RED** (registered red)<br>`cap_cc13ii_b`: link 6a `:5159` **RED** (registered red)<br>`cap_cc13ii_d`: link 6a `:10550` **RED** (registered red) |
| **D9** | first-link Q4 `TwoWorldsBroken` — C-Q2 `capstone.out:3824` `is true` | C-C14 | `cap_cc14_a`: C-Q2 `:30482` **RED** (registered red)<br>`cap_cc14_b`: C-Q2 `:30574` **RED** (registered red) |
| **D10** | **C-Q9** — C-Q9 `capstone.out:3434` `is true` | C-C3, C-C8 | `cap_cc03_a`: C-Q5 `:4839` green (registered green in this case); C-Q9 `:3785` **RED** (registered red)<br>`cap_cc03_b`: C-Q5 `:4859` green (registered green in this case); C-Q9 `:3794` **RED** (registered red)<br>`cap_cc03_d`: **timeout (mechanism-viability failure)**<br>`cap_cc08_a`: C-Q5 `:4839` green (registered green in this case); C-Q9 `:3785` **RED** (registered red)<br>`cap_cc08_b`: C-Q5 `:4859` green (registered green in this case); C-Q9 `:3794` **RED** (registered red)<br>`cap_cc08_d`: **timeout (mechanism-viability failure)** |
| **D11** | S-P7 `Rescoped` (link 6b) — link 6b `capstone.out:3759` `is true` | C-C15(i), C-C15(ii), C-C15(iii) | `cap_cc15i_a`: link 6b `:6863` green (registered green in this case)<br>`cap_cc15i_b`: link 6b `:6881` green (registered green in this case)<br>`cap_cc15i_d`: link 6b `:13113` **RED** (registered red)<br>`cap_cc15ii_a`: link 6b `:4628` **RED** (registered FORK: red, or the configuration green throughout)<br>`cap_cc15ii_b`: link 6b `:4642` **RED** (registered FORK: red, or the configuration green throughout)<br>`cap_cc15ii_d`: link 6b `:8355` **RED** (registered red)<br>`cap_cc15iii_a`: link 6b `:4735` **RED** (registered red)<br>`cap_cc15iii_b`: link 6b `:4767` **RED** (registered red)<br>`cap_cc15iii_d`: link 6b `:8485` **RED** (registered red) |
| **D12** | S-STANDING `Established => Designated` — C-Q6 c1 `skI` `capstone.out:5239` `is true` | C-C11 | `cap_cc11_a`: C-Q6 c1 `skI` `:6171` **RED** (registered red)<br>`cap_cc11_b`: C-Q6 c1 `skI` `:6193` **RED** (registered red)<br>`cap_cc11_d`: C-Q6 c1 `skI` `:10384` **RED** (registered red) |
| **D13** | S-STANDING `StandingUnentitled` — C-Q6 c2 `capstone.out:5382` `is true` | C-C12 | `cap_cc12_a`: C-Q6 c2 `:6958` **RED** (registered red)<br>`cap_cc12_b`: C-Q6 c2 `:7066` **RED** (registered red)<br>`cap_cc12_d`: C-Q6 c2 `:10779` **RED** (registered red) |
<!--END-S3-->

**Rows with no observed severing in any case.** Every producer query is green in the correct model. Four
row halves have no severing companion that went red in **any** case. In each one the registration puts
the consumer's red in **(d) only**, or, for D2, leaves strict as a fork that fell on its green branch:

- **D1.** C-C2 is registered green in strict, and `cap_cc02_d` timed out.
- **D2.** C-C4 fell on its green strict branch, and `cap_cc04_d` timed out.
- **D5.** C-C5's `InnerSigTransplanted` is descended green in strict, and `cap_cc05_d` is a memory
  failure.
- **D10's (α) half, C-Q5.** C-Q5 is green in strict under both C-C3 and C-C8, and both (d) runs timed out.
  D10's (β) half, C-Q9, is red in (a) and (b).
  *(REPAIR 2026-10-01, skeptic S-7. The two lines above, kept as written, read as if D10 were half
  discharged. **It is not, in any case.** §A3.3 requires a broken companion that *“fails the query
  consuming the severed link”* (`docs/phase-0-prereg-amendment-3.md:223`). D10's consuming query is C-Q5
  `SetAltered`, and its producer is C-Q9 (`PREDICTIONS.md:640`). **C-Q5 is green in every landed run of
  D10's severing companions**: C-C3 and C-C8 in (a) and (b) (`cap_cc03_a.out:4839`, `cap_cc03_b.out:4859`,
  `cap_cc08_a.out:4839`, `cap_cc08_b.out:4859`) and C-C8's two isolation configurations
  (`cap_cc08i_a.out:4139`, `cap_cc08i_b.out:4159`, `cap_cc08ii_a.out:4850`, `cap_cc08ii_b.out:4870`). Every
  (d) run of them failed. C-Q9's red in (a) and (b) is the **producer's** query going red under its own
  companion: it shows the producer severed, not the consumer failing. **So D10's consuming-query requirement
  is unmet in every case**, which is what option (i) under* The degraded wave *would concede for D10. (C-Q5
  is red in the ladder only under C-C15(i), in all three cases — `cap_cc15i_a.out:8561`,
  `cap_cc15i_b.out:8585`, `cap_cc15i_d.out:16553` — where it is registered red. C-C15(i) is D11's severing
  companion, not D10's, and this file does not read that red as D10's.))*

**D6** is severed in (a) and (b) only (both (d) configurations timed out). **D7's membership half** (C-C17)
is severed in (a) and (b) only. Its (d) run is a memory failure, although a partial line shows link 2a red
before the guard fired (*The degraded wave*). Every other row is severed in every case it runs in.
### Which box reading each severing depends on *(added 2026-10-01, REPAIR, skeptic S-4)*

Section 0 records two readings of a companion's box and decides neither. **(P)**, the per-case-sum reading,
gives every run the sum of its case's boxes, 71 100 s strict and 65 700 s degraded; that is what the ladder
enforced, and every landed run is inside it. **(Q)**, the predicted-red-box reading, gives a companion the
box of the query it is predicted to red (§3's table, `PREDICTIONS.md:1586-1595`; the assignments in words at
`:1867-1876` and `:2590`). **Per-query time is not logged**: ProVerif's output carries no timestamps and
`ladder.log` records one wall clock per run. A whole-run time is an upper bound on each query's, so a run
that finished inside a box shows its query did; a run longer than the box shows nothing either way. Under
(Q) such a run is therefore **“not shown inside its box”**, never “shown outside it”. Seconds are
`ladder.log`'s (line in parentheses). Only runs that carry the row's severing, or that were the row's chance
to, are listed.

| Row | Severing companion, case: seconds (`ladder.log` line) and what it shows | The predicted-red query carrying the severing, and its box | (P) per-case sum | (Q) predicted-red box |
|---|---|---|---|---|
| **D1** | C-C2 (a) 959 s (`:11`), (b) 450 s (`:38`): no red, registered green in strict. (d) `rc=124`, 65 702 s (`:64`). | C-Q3, 45 min; link 5, 60 min | **no severing observed** | **no severing observed** |
| **D2** | C-C4 (a) 846 s (`:10`), (b) 370 s (`:37`): the fork fell on its green branch. (d) `rc=124` (`:63`). | C-Q4 `Rescoped`, 60 min | **no severing observed** | **no severing observed** |
| **D3** | C-C1 (c) 4 279 s (`:70`): `Accept(S) ⟹ IssuerSigned` red. | retained query, 30 min (1 800 s) | stands | **not shown inside its box** |
| **D4** | C-C1 (c) 4 279 s (`:70`): link 1b red. C-C10 (a) 4 257 s (`:20`), (b) 4 202 s (`:47`): links 1a and 1b red; (d) 3 173 s (`:84`): link 1a red. | links 1a and 1b, 45 min (2 700 s) | stands in (a), (b), (c), (d) | **not shown inside its box in any case** |
| **D5** | C-C5 (a) 944 s (`:12`), (b) 442 s (`:39`): `InnerSigTransplanted` registered green in strict. (d) `rc=143` (`:66`). | C-Q4 `InnerSigTransplanted`, 60 min | **no severing observed** | **no severing observed** |
| **D6** | C-C7(i) (a) 12 423 s (`:14`), (b) 6 139 s (`:41`); C-C7(ii) (a) 13 333 s (`:17`), (b) 9 009 s (`:44`): C-Q8 and link 4 red. Both (d) runs `rc=124` (`:68`, `:79`). | C-Q8, 60 min (3 600 s); link 4, 45 min | stands in (a), (b) | **not shown inside its box in any case** |
| **D7**, completeness (`Stripped`) | C-C9 (a) 252 s (`:18`), (b) 255 s (`:45`), (d) 1 377 s (`:81`): link 2b slot-B and `Stripped` red. | link 2b, 60 min — *“as C-C9 runs inside link 2b's”* (`:1875`) | stands in (a), (b), (d) | **stands** in (a), (b), (d) |
| **D7**, common content (`Spliced`) | C-C16 (a) 284 s (`:30`), (b) 273 s (`:57`), (d) 6 671 s (`:94`): link 5 and `Spliced` red. | link 5, 60 min (3 600 s) (`:1874`) | stands in (a), (b), (d) | stands in (a), (b); **(d) not shown inside its box** |
| **D7**, membership (`SignerForged`) | C-C17 (a) 27 503 s (`:34`), (b) 27 084 s (`:61`): link 2a and `SignerForged` red. (d) `rc=143` (`:95`). | link 2a, 45 min (2 700 s) (`:1873`) | stands in (a), (b) | **not shown inside its box in any case** |
| **D8** | C-C13(i) (a) 256 s (`:24`), (b) 233 s (`:51`), (d) 3 760 s (`:87`); C-C13(ii) (a) 672 s (`:28`), (b) 634 s (`:55`), (d) 7 942 s (`:92`): link 6a and `TypeConfused` red. | link 6a, 45 min (2 700 s); `TypeConfused` 30 min | stands in (a), (b), (d) | stands in (a), (b); **(d) not shown inside its box** |
| **D9** | C-C14 (a) 43 842 s (`:29`), (b) 41 473 s (`:56`): C-Q2 red. | C-Q2, 45 min (2 700 s) | stands in (a), (b) | **not shown inside its box in any case** |
| **D10** | C-C3 (a) 488 s (`:9`), (b) 271 s (`:36`); C-C8 (a) 502 s (`:15`), (b) 261 s (`:42`): the producer C-Q9 red, the **consumer C-Q5 green**. Both (d) runs `rc=124` (`:65`, `:80`). | consumer C-Q5, 45 min (`:2590`: C-C3 runs inside C-Q5's box); producer C-Q9, 60 min | **consuming-query severing observed in no case** (S-7); C-Q9's red inside the box | the same |
| **D11** | C-C15(i) (a) 287 s (`:101`), (b) 279 s (`:102`): link 6b registered green; (d) 7 825 s (`:103`): red. C-C15(ii) (a) 296 s (`:31`), (b) 284 s (`:58`), (d) 4 091 s (`:90`); C-C15(iii) (a) 343 s (`:32`), (b) 316 s (`:59`), (d) 4 290 s (`:93`): link 6b red. | link 6b, 45 min (2 700 s) | stands in (a), (b), (d) | stands in (a), (b) (by (ii) and (iii)); **(d) not shown inside its box** (4 091-7 825 s) |
| **D12** | C-C11 (a) 304 s (`:23`), (b) 282 s (`:50`), (d) 4 403 s (`:86`): C-Q6 conjunct 1 `skI` red; its two alternates the same, 270-4 244 s. | C-Q6, 90 min (5 400 s) | stands in (a), (b), (d) | **stands** in (a), (b), (d) |
| **D13** | C-C12 (a) 485 s (`:26`), (b) 459 s (`:53`), (d) 4 349 s (`:89`): C-Q6 conjunct 2 red. | C-Q6, 90 min (5 400 s) | stands in (a), (b), (d) | **stands** in (a), (b), (d) |

**The effect, summarised.** Under **(P)** every observed severing stands. Under **(Q)**:
- **not shown inside the box in any case:** D3, D4, D6, D9 and D7's membership half — five rows or row
  halves;
- **shown inside the box in strict, not in (d):** D7's common-content half, D8 and D11 — their (d) runs took
  6 671 s, 3 760-7 942 s and 4 091-7 825 s against 45- or 60-minute boxes;
- **shown inside the box in every case run:** D7's completeness half, D12, D13;
- **no consuming-query severing under either reading:** D1, D2, D5 and D10, the rows option (i) of the
  first routed question concerns.

Which reading governs is routed to the author (*ROUTED TO THE AUTHOR — second question*).

<!--END-RESULTS-TABLES-->

---

## Cross-check: every ladder-1 run against ladder 2

Recut R-9 is sound, but it can cost completeness (ProVerif manual §6.6; recut R-9 below). A query proved
under the default selection function could therefore come back `cannot be proved` under `Term`, or a
result could otherwise move. The check compares, for every file that has an `.out` under `ladder1/`, its
`RESULT` stream against ladder 2's, line by line. It was recomputed on 2026-10-01 from the files; the
staged expectation was not taken on trust.

<!--CROSSCHECK-->
| File | Ladder-1 disposition (`ladder1/ladder.log` line) | Ladder-2 disposition | RESULT lines, ladder 1 / ladder 2 | Comparison |
|---|---|---|---|---|
| `cap_cc01_c` | rc=143 `:24` | landed | 3 / 47 | **prefix-consistent**: ladder 1's 3 lines are ladder 2's first 3 |
| `cap_cc02_a` | rc=143 `:20`, rc=0 `:32` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc02_b` | rc=0 `:59` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc02_d` | rc=124 `:108` | timeout | 0 / 0 | no `RESULT` line in either ladder |
| `cap_cc03_a` | rc=143 `:23`, rc=0 `:30` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc03_b` | rc=0 `:57` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc03_d` | rc=124 `:107` | timeout | 0 / 0 | no `RESULT` line in either ladder |
| `cap_cc04_a` | rc=143 `:22`, rc=0 `:31` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc04_b` | rc=0 `:58` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc05_a` | rc=143 `:21`, rc=137 `:33`, rc=0 `:78` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc05_b` | rc=137 `:60`, rc=0 `:84` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc06_a` | rc=143 `:19`, rc=0 `:35` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc06_b` | rc=137 `:61`, rc=0 `:85` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc07i_a` | rc=143 `:18`, rc=137 `:34`, rc=124 `:79` | landed | 4 / 47 | **prefix-consistent**: ladder 1's 4 lines are ladder 2's first 4 |
| `cap_cc07i_b` | rc=143 `:62`, rc=124 `:87` | landed | 4 / 47 | **prefix-consistent**: ladder 1's 4 lines are ladder 2's first 4 |
| `cap_cc07ii_a` | rc=137 `:38`, rc=143 `:81` | landed | 3 / 47 | **prefix-consistent**: ladder 1's 3 lines are ladder 2's first 3 |
| `cap_cc07ii_b` | rc=143 `:63`, rc=143 `:86` | landed | 3 / 47 | **prefix-consistent**: ladder 1's 3 lines are ladder 2's first 3 |
| `cap_cc08_a` | rc=0 `:37` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc08_b` | rc=0 `:89` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc08i_a` | rc=0 `:36` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc08i_b` | rc=0 `:64` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc08ii_a` | rc=0 `:40` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc08ii_b` | rc=143 `:65`, rc=0 `:88` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc09_a` | rc=0 `:39` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc09_b` | rc=143 `:66`, rc=0 `:90` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc10_a` | rc=0 `:41` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc10_b` | rc=143 `:67`, rc=0 `:91` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc10iso_a` | rc=0 `:42` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc10iso_b` | rc=0 `:92` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc11_a` | rc=0 `:44` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc11_b` | rc=0 `:95` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc11abl6_a` | rc=0 `:43` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc11abl6_b` | rc=0 `:93` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc11q4_a` | rc=0 `:46` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc11q4_b` | rc=0 `:94` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc12_a` | rc=0 `:47` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc12_b` | rc=0 `:97` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc13i_a` | rc=0 `:45` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc13i_b` | rc=0 `:96` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc13ii_a` | rc=0 `:49` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc13ii_b` | rc=0 `:98` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc14_a` | rc=137 `:50`, rc=143 `:80` | landed | 3 / 47 | **prefix-consistent**: ladder 1's 3 lines are ladder 2's first 3 |
| `cap_cc14_b` | rc=143 `:99` | landed | 3 / 47 | **prefix-consistent**: ladder 1's 3 lines are ladder 2's first 3 |
| `cap_cc15i_a` | rc=0 `:48` | landed; compared against the superseded pre-BF-4 ladder-2 run (`ladder2-superseded/cap_cc15i_a.out`), the fixture ladder 1 ran | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc15i_b` | rc=0 `:100` | landed; compared against the superseded pre-BF-4 ladder-2 run (`ladder2-superseded/cap_cc15i_b.out`), the fixture ladder 1 ran | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc15ii_a` | rc=0 `:52` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc15ii_b` | rc=0 `:101` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc15iii_a` | rc=0 `:51` | landed | 49 / 49 | **identical** (byte-for-byte) |
| `cap_cc15iii_b` | rc=0 `:102` | landed | 49 / 49 | **identical** (byte-for-byte) |
| `cap_cc16_a` | rc=0 `:53` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc16_b` | rc=0 `:103` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc17_a` | rc=137 `:55`, rc=0 `:82` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc17_b` | rc=0 `:105` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc18_a` | rc=0 `:54` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `cap_cc18_b` | rc=0 `:104` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `capstone` | rc=0 `:15` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `capstone_b` | rc=0 `:16` | landed | 47 / 47 | **identical** (byte-for-byte) |
| `capstone_d` | rc=0 `:25` | landed | 44 / 44 | **identical** (byte-for-byte) |

**Tally:** both-empty 2, identical 49, landed-l1 49, not-landed-l1 9, prefix 7.
<!--END-CROSSCHECK-->

**Result.**

- **49 of 49** files that landed in ladder 1 (`rc=0`) are **identical byte for byte**.
- **7** files that ladder 1 killed, terminated or timed out are **prefix-consistent**: their ladder-1
  partial `RESULT` lines are exactly the first lines of ladder 2's landed stream. The seven are
  `cap_cc01_c` (3 of 47), `cap_cc07i_a` and `cap_cc07i_b` (4 each), `cap_cc07ii_a`, `cap_cc07ii_b`,
  `cap_cc14_a` and `cap_cc14_b` (3 each).
- **2** files, `cap_cc02_d` and `cap_cc03_d`, have **no** `RESULT` line in either ladder; they timed out on
  link 1a in both.
- **0** differences, and no `cannot be proved` anywhere in ladder 2.

*(The expectation handed to this assembly was 49 identical, 6 prefix-consistent and 0 differences. The
recount gives 7 prefix-consistent, and the seventh is case (c)'s `cap_cc01_c`, which ladder 1 terminated
at 3 of 47.)* **Consequence:** on every file where both ladders produced results, the change of tactic
moved no verdict. Ladder 2 also landed every strict run that ladder 1 lost to its mechanism failures.

*(Dated note 2026-10-01, BF-4: `cap_cc15i_a` and `cap_cc15i_b` are compared against their superseded
pre-repair ladder-2 runs in `proverif/ladder2-superseded/`, because those ran the same fixture as
ladder 1. The repaired files have no ladder-1 counterpart, so the 49 identities still hold fixture for
fixture.)*

---

## The degraded wave: eleven mechanism failures, and a disposal routed to the author

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
- `cap_cc02_d` (timeout): no RESULT line before the run ended
- `cap_cc03_d` (timeout): no RESULT line before the run ended
- `cap_cc04_d` (timeout): C-Q1 link 1a `cap_cc04_d.out:3676` `is true`, C-Q1 link 2a `cap_cc04_d.out:4990` `is true`, link 2b one-signer conj. `cap_cc04_d.out:14784` `is true`
- `cap_cc05_d` (memory): C-Q1 link 1a `cap_cc05_d.out:5020` `is true`, C-Q1 link 2a `cap_cc05_d.out:7672` `is true`
- `cap_cc06_d` (timeout): no RESULT line before the run ended
- `cap_cc07i_d` (timeout): no RESULT line before the run ended
- `cap_cc07ii_d` (timeout): no RESULT line before the run ended
- `cap_cc08_d` (timeout): no RESULT line before the run ended
- `cap_cc08i_d` (memory): C-Q1 link 1a `cap_cc08i_d.out:4220` `is true`, C-Q1 link 2a `cap_cc08i_d.out:6090` `is true`
- `cap_cc08ii_d` (memory): C-Q1 link 1a `cap_cc08ii_d.out:4559` `is true`, C-Q1 link 2a `cap_cc08ii_d.out:6750` `is true`
- `cap_cc17_d` (memory): C-Q1 link 1a `cap_cc17_d.out:3739` `is true`, C-Q1 link 2a `cap_cc17_d.out:5433` `is false`
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
change of tactic. The diagnosis shows that neither disposes of these (`abl_d` §(c), §(e), §(f)), and the
registration has no third disposal. **What rides on it:** D1, D2, D5 and D10's (α) half have no observed
severing in any case without these runs (section 3), and D6 and D7's membership half are severed in strict
only. *(REPAIR 2026-10-01, skeptic S-7 and S-4: for D10 the whole consuming-query requirement is unmet in
every case, not an “(α) half” — C-Q5 is green in every landed run of C-C3, C-C8 and C-C8's isolation
configurations (section 3, the repair note under* Rows with no observed severing*). And under the
predicted-red-box reading five further rows or row halves (D3, D4, D6, D9, D7's membership half) rest on runs
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
  leaves D3, D4, D6, D9 and D7's membership half on runs not shown inside their box as well.)*
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
  registration of its own or an amendment. The (d) seams stay open until it lands.

**Re-running C-C8-i and C-C8-ii in (d) with the memory guard raised — the facts** *(added 2026-10-01,
REPAIR, skeptic S-5)*. Two of the four guard terminations stopped a run with box left: `cap_cc08ii_d` at
39 900 s (39.3 % of its box unspent) and `cap_cc08i_d` at 48 680 s (25.9 % unspent), each with 16-32 GB
still available on the guest (*The degraded wave*, the headroom table). The 80 GB rule is the owner
instance's, not the registration's, so raising it would move no box, model, query or prediction. Against
that: (1) both are **isolation configurations** of C-C8 (§9(2)), which bear on no matrix row directly; D10's
consuming query would still need C-C8 itself or C-C3 in (d), both of which timed out at the full box
(`rc=124`); (2) both ended on link 2b's one-signer conjunct (`cap_cc08i_d.out:6091`, `cap_cc08ii_d.out:6751`),
the query on which `cap_cc05_d` and `cap_cc17_d` were also terminated, with under 2 % of their box left, and
on which `cc02_d` at ablation step 1 ran out of memory under a 10 GiB cap (`abl_d` F1); how long either
spent on that query is not known, because per-query time is not logged; (3) at the four triggers the guest
held 120-171 GB in all (`totalMB`), and how far its dynamic memory can grow is not recorded in this file.
This file offers the re-run neither as an option nor as part of one; the builder makes no recommendation on
it.
**The owner instance's disposition follows.**

**The owner instance's recommendation (2026-10-01; a recommendation, not a ruling).** **(i) now, with
(iii) docketed for after the exit, and not (ii).**

- **Why not (ii).** The only whole-file evidence is against it: `cc02_d` at step 1 ran out of memory on
  link 2b, and `cc05_d` was unchanged by steps 1 to 1-3. It would cost up to about 200 h of solver time
  for an outcome the diagnosis already predicts, after a ceiling exceeded 5.6-fold. And it buys its
  landings by amending C-N1, the rule that keeps an ablated green from being mistaken for a result.
- **Why (i).** It states in the record exactly what the composed model did and did not show. The
  severing of these eleven seams in case (d) rests on the family-level degraded runs the registration
  already cites, and the capstone adds no composed (d) evidence for them. That is the termination-forced
  scoping A3 §A3.3 anticipates ("named in-module and disposed by amendment discipline, never silently").
- **What (i) costs, stated without softening.** For four ledger rows, D1, D2, D5 and D10's (α) half, the
  gate's broken-companion requirement would be met by family-level evidence alone, not by a companion
  that fails the consuming query **in the composed model**. *(REPAIR 2026-10-01, skeptic S-7, a factual
  correction inserted by the builder; the recommendation is the owner instance's and is not changed by it:
  for D10 it is the whole requirement, not a half — C-Q5, D10's consuming query, is green in every landed
  run of D10's severing companions, and C-Q9's red is the producer's own.)* That is a narrowing of what §A3.3 asks, and
  the amendment has to say so in those words. It is the author's to accept or refuse.
- **Why (iii) later, not now.** A Tamarin model of just the degraded companions would be an independent
  tool reading the same claim, which the record would welcome. But it is weeks of work with its own
  registration and review, and the exit does not need it if (i) is accepted. Docket it as cross-tool
  corroboration for the four rows above.

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
   (`cap_cc01_c.out:12611`) *is read here **diagnostically only**; C-Q6 is not stated for (c) (B-4), and no
   verdict rests on it.*
5. **C-C10's and C-C14's C-Q6 conjunct 1, unrestricted** *(added 2026-10-01, REPAIR, skeptic S-6; a clerk
   finding of the owner instance's builder, **not entered**, for the author's amendment if he agrees)*.
   Item 4 says set (2) was wrong but proposed no route, which left C-C10 (a)/(b) DIVERGENT with no way to
   close. The amendment-shaped item: **move C-Q6 conjunct 1's unrestricted form from C-C10's set (2) to its
   set (1) in (a) and (b)**, registered red on the dependence `:1018` already encodes, and **add it to
   C-C14's set (1) in (a) and (b)**, where set (2) does not name C-Q6. Neither touches (d), where the
   unrestricted form is not asserted. The honest-key forms stay in both companions' green lists, which the
   runs agree with (`cap_cc10_a.out:11697`, `:11894`; `cap_cc14_a.out:38010`, `:38666`; the same in (b)),
   so D12's severing (C-C11) is unaffected. Whether G2 is then also carried as a finding (item 4) is
   separate, and is the reviewer's and the author's.


### ROUTED TO THE AUTHOR — second question: which companion-box reading governs *(added 2026-10-01, REPAIR, skeptic S-4)*

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
Neither reading makes any sentence false; they differ on which sentence sets a companion's limit.

**The effect, row by row** (section 3, *Which box reading each severing depends on*; per-query time is not
logged, so under (Q) a run longer than its box is *“not shown inside its box”*, not *“shown outside it”*):

| Row | Under (P) | Under (Q) |
|---|---|---|
| D1, D2, D5 | no severing observed in any case | no severing observed in any case |
| D3 | severed in (c) | not shown inside its box (4 279 s against 30 min) |
| D4 | severed in (a), (b), (c), (d) | not shown inside its box in any case (3 173-4 279 s against 45 min) |
| D6 | severed in (a), (b) | not shown inside its box in any case (6 139-13 333 s against 60 min) |
| D7, completeness (C-C9) | severed in (a), (b), (d) | the same: 252-1 377 s, inside 60 min |
| D7, common content (C-C16) | severed in (a), (b), (d) | (a), (b) inside; (d) not shown inside (6 671 s against 60 min) |
| D7, membership (C-C17) | severed in (a), (b) | not shown inside its box in any case (27 084-27 503 s against 45 min) |
| D8 | severed in (a), (b), (d) | (a), (b) inside; (d) not shown inside (3 760 and 7 942 s against 45 min) |
| D9 | severed in (a), (b) | not shown inside its box in any case (41 473-43 842 s against 45 min) |
| D10 | consuming query C-Q5 red in no case (S-7); producer C-Q9 red in (a), (b) | the same; C-Q9's red inside 60 min |
| D11 | severed in (a), (b), (d) | (a), (b) inside (C-C15(ii), (iii)); (d) not shown inside (4 091-7 825 s against 45 min) |
| D12, D13 | severed in (a), (b), (d) | the same: every run inside C-Q6's 90 min |

**What either choice costs.** If **(P)** governs, every severing observed in sections 2-3 stands as observed,
and the remaining gaps are those of the first question (D1, D2, D5, D10). If **(Q)** governs, five rows or
row halves (D3, D4, D6, D9, D7's membership half) have no severing shown inside its box in any case, and
three more (D7's common-content half, D8, D11) have none shown in (d); those would need either a disposal
under §3 (the registered outcome for a run that exceeds its box is a timeout, disposed by ablation or a
change of tactic) or an amendment. No re-run is proposed here: the ladder's output carries no per-query time,
and timing one query alone would need a file carrying that query alone, which is not the registered file.

**The owner instance's recommendation (2026-10-01; a recommendation, not a ruling): (P).**

- **Sentence 3 explains itself as accounting.** It says companions run inside a query's box *“so the
  1155-minute per-case total and the 26 entries are unchanged”*. The clause after *“so”* is the point
  being made: companions add no entries to the ceiling. Sentence 1 is the only one framed as a rule for
  runs, and it says *“per run, each compromise case getting the full box”*.
- **The builder chose (P) before any result existed.** `run_ladder.sh`'s header (2026-09-19) gives every
  file the per-case sum and records the predicted-red reading beside it. That ordering is what a frozen
  registration exists to protect: the reading was not chosen after seeing which rows it saves.
- **What (P) does not claim.** It does not claim any companion's predicted-red query finished inside 30
  to 60 minutes. Per-query time was never logged, so no reader can say. A reader who holds (Q) has a fair
  textual case. Under (Q), the record is not that eight row-halves failed; it is that they are not shown
  inside a box that nothing measured.
- **Whichever the author rules, the ambiguity is a defect of the registration and goes to the method.**
  The next registration should say which box a companion runs under, in one sentence, and the runner
  should log per-query time. The capstone did neither, and this question exists because of that.

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

`proverif/ladder.log` is a single file written by several launches, and this section reconciles it so
no reader has to infer the history from header lines.

*(Dated note 2026-10-01: everything from here to the subsection "After 2026-09-19" is **ladder 1's**
history on wam-nuc. That log is now `proverif/ladder1/ladder.log`, and its first header block is the
reconciliation written below. Phrases such as "these two results stand and are the only ones in this
file" were true when written and are superseded: no cell is now read from ladder 1. The text is kept as
written.)*

**What happened.** The runner was restructured four times on 2026-09-19 between 17:50 and 18:07 UTC.
Every restructuring was **scheduling only**: no box, no model, no query, no companion and no
registered prediction changed, and `capstone.pv` was not touched at any point (its blob is the same
before and after). The launches, and why each was superseded:

| Launch (UTC) | Superseded because |
|---|---|
| 17:50:28 | Ran `capstone.pv` and `capstone_b.pv` to completion — **these two results stand and are the only ones in this file** — then began case (d) in a blocking wave, which would have held every companion behind the single most expensive run. Restructured so (c) and (d) run alongside the companion waves. |
| 17:55:26 | `wave()` used a bare `wait`, which blocks on **all** background jobs and so blocked the companion waves behind the (c) and (d) runs after all. Restructured to wait on each wave's own PIDs. |
| 17:57:21 | Its parent shell was killed while restructuring, leaving six case-(a) companion runs **orphaned** (`ppid 1`): they would have run to completion with nothing to write their `ladder.log` line, and the next launch would have started duplicates. Killed. |
| 17:57:48 and 18:05:50 | Carried an intermediate version of the script in which case (c) was still a blocking wave, so wave 3 never started. Killed and replaced by the final version. |
| 18:06:37 | Ran well: `capstone_d` completed under it (`rc=0`, 1247 s) and six case-(a) companions were in flight. **Killed at 18:29:30 by the builder**, deliberately, to make the BF-3 repair — see the two rows below. |
| **18:29:30 — the kill, and its cause** | **Not a session teardown and not the kernel** (26 GB free, no OOM in `dmesg`). It was the builder's own command: `for p in $(pgrep -f "^bash run_ladder.sh"); do kill -9 $p; done; for p in $(ps -o pid= -C timeout) $(ps -o pid= -C proverif); do kill -9 $p; done`, run to stop the ladder before repairing `capstone.pv`. **Six runs were killed with no `ladder.log` line at all and are recorded here so the reader knows they existed:** `cap_cc01_c`, `cap_cc02_a`, `cap_cc04_a`, `cap_cc05_a`, `cap_cc06_a`, `cap_cc07i_a` — each about 22 minutes in, none complete. A seventh, `cap_cc03_a`, was 386 s into its re-run and left an `rc=137` line, since removed. Their partial `.out` files were deleted. |
| **19:11:24 — the owner instance's kill, for memory** | **Not the builder and not the kernel — the owner instance, deliberately, to keep the choice out of the kernel's hands.** At ~19:10 the machine was at **30 of 31 GB used, 0 GB available, 5.4 of 8 GB swap**, with eight ProVerif runs in flight whose resident sets were `capstone_d` **9.0 GB**, `cap_cc01_c` **7.5 GB**, `cap_cc04_a` 3.7, `cap_cc02_a` 3.0, `cap_cc06_a` 2.5, `cap_cc05_a` 2.1, `cap_cc07i_a` 1.7, `cap_cc03_a` 1.0. The kernel OOM killer would have picked a victim within minutes — most likely the largest run, at random and **unrecorded**. The owner instance sent `SIGSTOP` to the ladder script (3913937) and `SIGTERM` to the **six case-(a) companions**; `capstone_d` and `cap_cc01_c` were left untouched and their wrapper subshells resumed, so they will log on completion. 13 GB available afterwards. **The six `rc=143 seconds=1869` lines STAY in `ladder.log`** — no hand edit this time — as the honest record that those runs existed and were killed; the runner now reruns any file whose logged `rc` is 137 or 143. |
| **The design error, named** | An **8-wide** companion wave. A mutant's ProVerif process grows to **3-9 GB** — the correct model's does not — and eight of them exceed this machine. `JOBS` is now **3** for companion waves: twelve cores is not the limit, 31 GB is. |
| **19:25:50 — the owner instance terminates case (c)** | **The owner instance's decision, in their words:** `cap_cc01_c` was terminated with `SIGTERM`; its wrapper logged `rc=143 seconds=2732` and **that line stays**. Reason: *20 GB resident, swapping, 3 of 47 queries at 44 min, a companion case; keeping it endangered `capstone_d`, the run whose result matters.* After: `capstone_d` alone at 11.0 GB, 18 GB available, swap 2 GB. |
| **The pre-authorized rule for `capstone_d`, so nobody judges at the edge** | `capstone_d` runs to its registered box (1095 min) **unless** `free` shows **available < 1 GB AND swap free < 1 GB** with `capstone_d` the **only** ProVerif process; at that point it is terminated with `SIGTERM` (`rc=143`) and the run is classified here as **MECHANISM FAILURE (memory)** — stating that the registration boxes **time and not memory** — with §3's ablation order applied **as if the box had expired** and the memory figures recorded beside it. **The kernel is not waited for**, because a kernel OOM kill yields no `rc` line, no classification and no record. The check is **mechanical, not anyone's judgement**: `proverif/mem_guard.sh` polls every 30 s and appends every check to `proverif/mem_guard.log`, so the reader can see the rule being applied — `19:28:09 availMB=14844 swapfreeMB=5321 proverifProcs=1 capstone_d_rssMB=14686`. If it fires it also writes `capstone_d.mechfail`, which stops the runner blindly repeating the same unablated run. *(One correction, disclosed: the guard's first version matched `pgrep -f "proverif .*capstone_d.pv"`, which also matches the `timeout` **wrapper** — killing that would have orphaned ProVerif rather than terminated it. The pattern is now anchored, `^proverif`, and the RSS it reports is the solver's.)* |
| **20:11:43 — the live ladder** | The paused script 3913937 was killed (`Ts`, **no live children** — `pgrep -c proverif` was 0 at the time) and the ladder relaunched once. **Scheduling only; no run was affected**, since every run it had started had already logged its own `rc` line. `mem_guard.sh` had already exited on its own, cleanly and without firing (`19:51:41 capstone_d no longer running; guard exits without firing`), and it is `capstone_d`-specific by construction, so it cannot fire on another process. |
| **18:40 — the superseded ladder** | The first restart that is **not** scheduling: `capstone.pv` itself was repaired (BF-3), so its blob changed from `508b9018…` to `c6969b4c…` and **every earlier run was discarded** — all `.out` files deleted, `ladder.log` reset. Launched exactly once, fully detached: `setsid nohup bash run_ladder.sh > ladder.launch.log 2>&1 < /dev/null &`. |

**The detachment check, pasted as run.** The ladder is in **its own session**, parented to `init`, and
is **not** a child or session member of the builder's shell:

```
my shell: pid=3914191 pgid=3914191 sid=3914191

    PID    PPID    PGID     SID COMMAND
3913953 3913951 3913951 3913937 proverif -lib ../../lib/tessera_theory.pvl capstone.pv
3913954 3913952 3913952 3913937 proverif -lib ../../lib/tessera_theory.pvl capstone_b.pv

    PID    PPID    PGID     SID COMMAND
3913937       1 3913937 3913937 bash run_ladder.sh
```

(One stray `proverif` on `cap_cc14_a.pv` in session `3908682` is a leftover of the type-check sweep,
not a ladder run: it writes to no `.out`, and under the rule below it has been **left alone** rather
than killed.)

**The three scheduling changes the memory event forced** (`run_ladder.sh`, header; no box, model,
query or prediction moves): **(a)** a `ladder.log` line whose `rc` is 137 or 143 records a **killed
run, not a result** — it stays as history and the file is **rerun**, which the skip guard now
implements. *(The guard is written as three `grep` stages on purpose. The obvious two-stage form,
`grep -E "^<file> rc=" ladder.log | grep -qvE "rc=(137|143) "`, is wrong on this system: `grep -qv`
returns **0 on empty input** here, so a file with **no** log line at all would have been read as
"already landed" and the relaunched ladder would have run **nothing**. Caught by testing the guard
against the real log before relaunching — `cap_cc11_a`, which has never run, was being reported as
SKIP.)*; **(b)** `JOBS` for companion waves drops from 6 to **3**, and **case (c) is
moved LAST and runs ALONE**, not in a wave, with the whole machine — it is the largest process in the
suite, and §3's ordering rule *"(a), (b), (d) before (c)"* puts it there anyway. If it cannot finish
alone within its box or within memory, that is a **mechanism failure** under the same rule, and §3's
ablation order applies to it as a companion; **(c)** each run's **peak
resident set** is recorded in its `ladder.log` line (`/usr/bin/time -f %M`, kB, alongside a
`<file>.rss`), so a reader can see what each companion cost in memory as well as in seconds.

**THE RULE, adopted after the 18:29:30 kill and binding on the rest of this build.** *A running
ProVerif is not killed again for any reason short of a demonstrated broken fixture.* If a derivation
defect is found while runs are in flight, the affected runs are **let finish**, their outputs are
**quarantined afterwards**, and they are **re-run** — the cost of a wasted run is minutes, the cost of
a kill is every in-flight run's wall clock plus a hole in the record. The 18:29:30 kill violated this
rule before it was written: BF-3 was a demonstrated defect, but the six runs it destroyed were not
runs of the defective path and would have completed and been quarantined at no loss. **The builder's
judgement was wrong and the rule now stands in its place.**

**Runs killed, and what was done with them.** `capstone_d` (killed 3 times), `cap_cc01_c` (3), and the
six case-(a) companions `cap_cc02_a`, `cap_cc03_a`, `cap_cc04_a`, `cap_cc05_a`, `cap_cc06_a`,
`cap_cc07i_a` (1 each). **The `.out` of every killed run was deleted before the relaunch, and no
result, line number or seconds figure anywhere in this file comes from a killed run.** Every killed
run is being re-run from the start by the live ladder.

**`ladder.log` was edited by hand, exactly twice, and this is the disclosure.** Two `rc=137` lines
(`cap_cc01_c` and `capstone_d`, the `SIGKILL` exit written when a restructure killed them mid-run)
were removed, because leaving them would have made the resumable runner skip those two runs
altogether; and the superseded header lines were removed, leaving one. The removals are recorded in
`ladder.log`'s own header block as well as here. **No `rc=0` line has ever been removed, added or
altered.**

**Reconciling the builder's interim report.** An interim report to the owner instance said eight runs
had been in flight for about fifty minutes. **That was wrong**: at the moment it was written those
runs had been in flight for about **seven** minutes (`ps -o etimes`). The error was the builder's —
elapsed time was stated from impression rather than read off the process table — and it was the
owner instance that caught the discrepancy. Two findings had rested on it and are corrected below
(**F-3** and **F-7**): the direction of the effect stands and is measured; **the magnitude does
not, and is now stated as not yet measured.**

### After 2026-09-19: the machine change, ladder 1's stop, ladder 2, the host crash *(added 2026-10-01)*

| When (UTC) | What, and why | Record |
|---|---|---|
| **2026-09-20T18:31:33 and 18:42:28** | The owner instance sent SIGTERM to `cap_cc07i_b` at 28.9 GB for memory, after the kernel had OOM-killed three ProVerif runs that day. It also stopped `cap_cc07ii_b` for scheduling ahead of the planned move. **Not results.** | `owner_interventions.log:1-2`; `ladder1/ladder.log:62-63` (`rc=143`) |
| **2026-09-20T19:10:41 to 19:11:23: the machine change** | The owner instance halted the wam-nuc ladder with four SIGTERMs (`cap_cc08_b`, `cap_cc08ii_b`, `cap_cc09_b`, `cap_cc10_b`; reason *machine change*). `cap_cc08_b` has no `ladder.log` line, because its logger had been killed by a mis-targeted stop command. The ladder resumed on **ubuntu24**, which is wam-desktop: a Hyper-V guest with dynamic memory, 64 cores and Ubuntu 24.04. The ProVerif 2.05 binary was copied from wam-nuc and validated there first (`capstone.pv`: 47 `RESULT` lines identical). `JOBS=2`. A relaunch followed at 19:12:31 for a scheduling-only wave-counter fix. **Same blob `c6969b4c…`; scheduling only.** Runs logged `rc=137`/`rc=143` on wam-nuc were re-run on ubuntu24 under the runner rule. | `owner_interventions.log:3-8`; `ladder1/ladder.log:68`, `:73` |
| **The memory guard on ubuntu24** | `mem_guard_vm.sh` sends SIGTERM to the largest ProVerif iff (available < 3 000 MB **and** total ≥ 90 000 MB) **or** its RSS > 80 000 000 kB. The guest's maximum was recorded as 96 GB on 2026-09-20. The guard logs show `totalMB` at 156 961 already on 2026-09-21 (`ladder1/mem_guard_vm.log:2822`) and at 170 731 on 2026-09-30 (`mem_guard_vm.log:16282`), so the 96 GB figure did not hold for most of either ladder. Every guard termination in ladder 2 fired on the per-process 80 GB rule. | `mem_guard_vm.sh:9-13`; `mem_guard_vm.log:1` |
| **2026-09-24T15:06:25: ladder 1 stopped** | The owner instance sent SIGTERM to the main `run_ladder.sh` (pid 9943) so that no further degraded pair would launch. `cap_cc02_d` and `cap_cc03_d` were left inside their boxes and logged `rc=124` later. The reason: the same three companions (C-C7(i), C-C7(ii), C-C14) had failed in both strict cases, and the degraded companions were heavier still (`cap_cc02_d` at 70+ GB after 16.4 h). **Not a result.** | `owner_interventions.log:10`; `ladder1/ladder.log:107-108` |
| **2026-09-24T17:15:52: ladder 2** | **A new model, not a restart of the old one.** It is blob `a9fb7da1…` (recut R-9). Ladder 1's `.pv`, `.out`, `.rss` and `ladder.log`, the ubuntu24 log and the guard logs are archived **unmodified** under `proverif/ladder1/`. Ladder 2 began from an **empty** `ladder.log`, so the runner skipped nothing. Machine ubuntu24, `JOBS=3`, `mem_guard_vm.sh` re-armed (thresholds above). Same boxes (71 100 s strict, 65 700 s degraded), same runner and same wave order. | `owner_interventions.log:11`; `ladder.log:1-3`; `mem_guard_vm.log:1` |
| **2026-09-28T13:01:30: `cap_cc05_d` terminated by the guard** | RSS 80 172 020 kB, on link 2b's one-signer conjunct. | `mem_guard_vm.log:10972`; `ladder.log:66` |
| **2026-09-28T16:32:25: main runner stopped** | The owner instance sent SIGTERM to the main `run_ladder.sh` (880969) after all six of the first degraded companions ended at their box or at the guard. The trio then in flight (`cap_cc07ii_d`, `cap_cc08_d`, `cap_cc08i_d`) was left to run to its box. The remaining fifteen degraded companions and case (c) were not launched by that runner. Disposal of the degraded wave went to diagnosis (`dev/abl_d/`). **Not a result.** | `owner_interventions.log:12` |
| **2026-09-28, 11:44:53 local (about 18:45 UTC): the Hyper-V host crashed** | The guest rebooted. The trio in flight, about six hours into its boxes, ended with no `rc`. Their partial outputs are kept as `*.interrupted-by-host-crash.out`, and they are **unrun** in the log's terms. The owner re-armed the guard at 18:59:57Z and launched **case (c)** alone with `run_one.sh`, which writes the runner's exact logging line. `cap_cc01_c` landed: `rc=0`, 4 279 s, 6.0 GiB. | `ladder.log:69-70`; `owner_interventions.log:13`; `mem_guard_vm.log:11642` |
| **2026-09-29T04:26:14: the remaining eighteen** | This launch came after `DEGRADED-WAVE-PREDICTION-2026-09-29.md` was written. The eighteen unobserved degraded companions, the crash-interrupted trio among them, ran unablated through `run_ladder.sh` with `JOBS=3`. A `cap_cc05_d.mechfail` marker made the runner log `MECHFAIL-MEMORY` instead of repeating an 18 h unablated run. The five `rc=124` siblings were skipped as landed-with-outcome. | `ladder.log:71-78`; `owner_interventions.log:14` |
| **2026-09-30T09:46:11, 12:12:30 and 2026-10-01T10:43:44** | The guard terminated `cap_cc08ii_d`, `cap_cc08i_d` and `cap_cc17_d`, each above 80 000 000 kB RSS. | `mem_guard_vm.log:16282`, `:16574`, `:19267`; `ladder.log:82-83`, `:95` |
| **2026-10-01: `DONE`** | The runner finished. Every one of the 80 files has a ladder-2 line. | `ladder.log:99` |

**No `ladder.log` line of ladder 2 was edited by hand.** The comment lines at `ladder.log:1`, `:69` and
`:71` were written by the owner instance at the time, as part of each launch or event.

---

## Broken fixtures, diagnosed and repaired

§4's replacement rule: *"a companion failing outside its set, or a witness dying, is a broken fixture
to be diagnosed and recorded, never a finding until the diagnosis distinguishes a broken fixture from
a real consequence of composition the single-family run could not exhibit"* (`:1668-1672`). Four
have occurred (BF-1 to BF-4; until 2026-10-01 this sentence read *“One occurred”*), and each is
recorded here with its diagnosis and its repair rather than absorbed.

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
alarm further than it went: on the repaired model, `capstone_d` logged `rc=0 seconds=6388` (`ladder.log:7`) with
**`RESULT not event(ScopeMisreported(...)) is true`** at `capstone_d.out:10341` — conjunct 3
**green in (d)**, exactly as §3 §(5) registers it. *(REPAIR 2026-10-01, skeptic S-1: until this repair the
sentence cited ladder 1's run under ladder 2's file name — “`rc=0 seconds=4257`” and “`capstone_d.out:10113`”.
Those are `ladder1/ladder.log:25` and `ladder1/capstone_d.out:10113`, the same `RESULT` line under blob
`c6969b4c…`; ladder 2 reproduces it, and the confirmation now rests on ladder 2's run, as this file's rule
requires.)* The only false property in that run is the
**registered** degraded red, the A4.6 cost at `PREDICTIONS.md:1579` (`capstone_d.out:10966`). The prediction did not miss; the
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
`RESULT` lines exactly **one** differs from ladder 2's `capstone_d.out`: conjunct 3,
`RESULT not event(ScopeMisreported(...)) is false` (`dev/bf3_rebuild/capstone_d_pre_bf3.out:5796`), with
the trace this section describes — the standing path reporting `(aid_7, L0, pk(a_16), a_15)` over
`authTuple(a_15, fp(pk(a_16)), …)` and the envelope path `(aid_7, L0, pk(a_4), a_3)` over
`authTuple(a_3, fp(pk(a_4)), signers0, a_2, a_5)` (`:5784-5796`). The skeptic made the same rebuild
independently in `/tmp` (its `.pv` differs from this one in whitespace only, and its 44 `RESULT` lines are
identical). **What the rebuild adds:** the red sits at `L0`, an unwrapped layer, outside conjunct 3's
registered *“over a wrapped presentation”* scope; the query as declared is broader than that (finding F-2's
repair note and B-5), so the red was reachable to the query at all only because the query is not
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
defect.)*

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
- **Old runs**, kept as evidence of the defect in `proverif/ladder2-superseded/` (with a README), and **no
  cell is filled from them**: (a) `ladder.log:27`, `rc=0`, 295 s, 0.4 GiB; (b) `:54`, `rc=0`, 279 s,
  0.4 GiB; (d) `:91`, `rc=0`, 7468 s, 12.3 GiB. Their `ladder.log` lines stay as history above the comment
  line `# BF-4 REPAIR 2026-10-01T14:35:53Z …` (`ladder.log:100`). The assembler treats every earlier run of
  a stem named in such a line as superseded: its time still counts in the ceiling, and it fills no cell.
- **New runs** on ubuntu24, with the same `run_one.sh` and the same boxes: (a) `ladder.log:101`, `rc=0`,
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
   `rc=0`, 43 842 s, 30.8 GiB (`ladder.log:29`), and in (b) 41 473 s (`:56`).
3. **Staging smoke test** (`ladder2-staging/smoke.log:1`): 47 `RESULT` lines identical to ladder 1's
   `capstone.out`.
4. **The ladder-wide cross-check** (section *Cross-check*). All 49 files that landed in ladder 1 are
   identical byte for byte. The 7 that ladder 1 lost are prefix-consistent. There are **0 differences
   and no `cannot be proved`**, so on this suite the setting cost nothing that the cross-check can see.

**Under ladder 2 every strict file landed**, including the three companions whose failures motivated the
recut, and case (c). The setting did **not** dispose of the degraded failures (*The degraded wave*).

---

## Blocked

Nothing in the registration was found unbuildable as written. Four items *(five since 2026-10-01: B-5, REPAIR, skeptic S-3)* are recorded here because
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
`HonestStandingEstablished` cannot say “wrapped”** *(added 2026-10-01, REPAIR, skeptic S-3)*. §3 registers
`HonestWrappedStandingAgreed` for *“an honest **wrapped** acceptance”* (`PREDICTIONS.md:1210-1215`) and
`HonestStandingEstablished` *“over a **wrapped** presentation”* (`:1341`). The capstone declares
`event(HonestWrappedStandingAgreed(a, l))` with `l` free (`capstone.pv:388`), and
`HonestStandingEstablished(pkey, bitstring)` has no layer argument (`capstone.pv:259`), so neither query can
be made to show the wrapped case, and every ladder trace for both is at `L0` (F-2's repair note). **The
smallest change:** register, by amendment, `HonestWrappedStandingAgreed(a, L1)` and `(a, L2)` as the
witness's two conjuncts (as link 2b is registered as three), and either give `HonestStandingEstablished` a
layer argument or name the wrapped form of the witness by `HonestWrappedStandingAgreed` alone. Adding a
layer argument to an event changes the model and its blob, so closing this is **amendment-shaped**, not the
builder's. No colour in sections 1-3 moves; what is missing is the evidence that the two witnesses are
reachable where the registration defines them.

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
note 2026-10-01: the 374 s and 392 s are ladder 1's. Under ladder 2 the same 47 resolve in **487 s** (a)
and **483 s** (b) (`ladder.log:5`, `:4`), the degraded correct form's 44 in **6 388 s** (`:7`), and case
(c)'s 47 in **4 279 s** (`:70`). The finding stands for every correct-form run in both ladders. **It does
not extend to companions in (d)**, where eleven of twenty-four failed (*The degraded wave*).)* The composed model's term space is the product the registration
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
*(REPAIR 2026-10-01, skeptic S-3. “Reachable at every layer” above **overstates what the ladder shows**
and is narrowed here; the sentence is kept as written.)* What the ladder shows: `HonestChain` is reachable
at `L0`, `L1` and `L2`, each by its own query; `HonestAccepted` is reachable; `HonestWrappedAccepted` is
reachable on a genuinely wrapped acceptance (its judge fires only on a `wctx` context, and the printed trace
names the wrapper key `pk(skW)`, `capstone.out:8602`). **The two standing witnesses are reachable, but every
trace the ladder printed for them is at `L0`, an unwrapped presentation**, while the registration defines
them for the wrapped case — `HonestWrappedStandingAgreed` *“fired … when the two reports agree for an
honest **wrapped** acceptance”*, so that a green conjunct 3 *“is a severing test that ran”*
(`PREDICTIONS.md:1210-1215`), and `HonestStandingEstablished` *“over a **wrapped** presentation”* (`:1341`):

| Case | `HonestWrappedStandingAgreed`: goal event in the trace | `HonestStandingEstablished`: the standing path's `estCh` report in the trace |
|---|---|---|
| (a) | `(aid_7, L0)`, `capstone.out:9576` | `(aid_7, L0, pk(skI2), …)`, `capstone.out:9059` |
| (b) | `(aid_7, L0)`, `capstone_b.out:9621` | `(aid_7, L0, pk(skI2), …)`, `capstone_b.out:9102` |
| (c) | `(aid_7, L0)`, `cap_cc01_c.out:20631` | `(aid_7, L0, pk(skI2), …)`, `cap_cc01_c.out:19875` |
| (d) | `(aid_7, L0)`, `capstone_d.out:16546` | `(aid_7, L0, pk(skI2), …)`, `capstone_d.out:15866` |

All eight are `skI2`'s one-signer `M1` tuple presented unwrapped. ProVerif prints one trace per reachable
event, so this shows reachability at `L0` and says nothing either way about `L1` or `L2`. The model does not
restrict either witness to wrapped layers: `ScopeAgreementJudge` pairs at every layer
(`capstone.pv:1059-1066`), the witness query has no layer restriction (`capstone.pv:388`), and
`HonestStandingEstablished(pkey, bitstring)` carries no layer argument at all (`capstone.pv:259`). **So the
ladder does not show either standing witness reachable at a wrapped layer.** *Scratch evidence, not a
result:* the skeptic's `/tmp` copies of the correct model with only extra layer-restricted queries,
`event(HonestWrappedStandingAgreed(a, L1))` and `(a, L2)`, came back reachable in (a) and (d)
(`/tmp/wit/wit.out`, `/tmp/wit/wit_d.out`, 61 s; read by the builder on 2026-10-01). No cell is filled from
it. **The same breadth applies to conjunct 3's query:** `not event(ScopeMisreported(a, l, k, ii, ka, ia))`
(`capstone.pv:367`) fires at `L0` as well, broader than the registered *“over a wrapped presentation”*. That
is conservative for a green (a green over every layer is a green over the wrapped ones), and it is why
BF-3's defect showed at `L0` (BF-3, *rebuilt*). The gap is recorded as **B-5**.

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
orders of magnitude slower".)* *(Dated note 2026-10-01: **the multiplier is now measured**, under
ladder 2. Strict correct form: 487 s. Strict companions: 200 s (`cap_cc10iso_b`) to 43 842 s
(`cap_cc14_a`). 41 of the 52 strict companion runs finished inside 30 minutes and 44 inside 4 257 s.
The other eight are C-C7(i), C-C7(ii), C-C17 and C-C14 in (a) and (b), at 6 139 s to 43 842 s. Degraded correct form: 6 388 s, **13×** the strict one. Case (c): 4 279 s.
Landed degraded companions: 1 377 s to 7 942 s. Eleven degraded companions did not finish in 65 700 s.
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
costs produced is stated under* Not run, and the ceiling*: 559.7 % over both ladders, 556.8 % before the
three BF-4 re-runs.)*

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
ablation. In ladder 2, eleven degraded companions failed, and neither of §3's disposals disposes of them
(*The degraded wave*). The cost shape this finding describes is visible there: the failing degraded runs
stall on link 1a or link 2b, and neither query is in any failing companion's set (1).)*

**F-6 — three registered sentences have no consumer in the registered query set.** §4's C-C7(ii)
sentence about a *honest-filtered* C-Q8, §9(1)'s C-C13(ii) per-layer assignment of link 6a's red, and
§9(4)'s C-C17 consequence on `PossessionTransplanted` each state an outcome for a relation that §3
does not register as a capstone query. They are recorded under **Blocked** (B-1, B-2, B-3) with the
smallest change that would close each. None of them is a defect of the model; each is a place where
the registration's prose ran ahead of its query list.

**F-9 — the change of tactic moved no verdict, and it landed every strict run** *(added 2026-10-01)*.
Recut R-9 (`set selFun = Term.`) reproduces byte for byte every `RESULT` line of the 49 files that landed
under the default selection function (*Cross-check*). It turned every strict mechanism failure of ladder 1
into a landing: C-C7(i), C-C7(ii) and C-C14 in (a) and (b), and case (c). *(REPAIR 2026-10-01, skeptic S-8:
“and case (c)” is withdrawn as credit to the recut. In ladder 1 case (c) was not a mechanism failure: the
owner instance terminated it at 2 732 s on the 31 GB machine (`ladder1/ladder.log:24`), and it was never re-run
under ladder 1's model. Ladder 2 landed it in 4 279 s on ubuntu24, but there is no ladder-1 run on that
machine to compare, so nothing shows the recut was what it needed.)* The effect on cost is not uniform. Over
the 49 files that landed in both ladders, ladder 2's time ranges from 1/34 of ladder 1's (`cap_cc05_b`:
15 191 s to 442 s) to 1.5 times it (`capstone_d`: 4 257 s to 6 388 s). The correct forms and C-C10 got
slower, and the heaviest companions got much faster: `cap_cc05_a` took 17 934 s and 22.1 GiB in ladder 1
(`ladder1/ladder.log:78`) and 944 s and 0.8 GiB in ladder 2 (`ladder.log:12`). Part of ladder 1 ran on
wam-nuc and all of ladder 2 on ubuntu24, so this is not a controlled comparison. On this suite the completeness the manual says the setting may
cost was not observed to be lost.

**F-10 — the degraded companions fail on link 1a or link 2b, queries outside every failing companion's registered failed set** *(added 2026-10-01)*.
Eleven of twenty-four case-(d) companion runs ended without a result. Six stalled on link 1a, the first
query, and five on link 2b's one-signer or slot-A conjunct (*The degraded wave*). The degraded correct
form itself lands in 6 388 s. The diagnosis (`dev/abl_d/REPORT.md`) explains the first six by the
product of attacker-mintable tuples in (d) and a mutation that unbinds a key. It does not explain three
of the later five. This is the registration's own mechanism-viability outcome, and §3 has no disposal
for it. **It is not a property result**, and nothing in this file reads it as one.

---

## Not run, and the ceiling

*(Rewritten 2026-10-01. The section as written 2026-09-19 follows, kept and marked superseded.)*

**All 80 files ran under ladder 2, so no file is unrun.** 69 landed (`rc=0`). The other 11 are all
case-(d) companions. Seven reached the 65 700 s box (`rc=124`). Four were terminated by the 80 GB memory
guard (`rc=143`). For `cap_cc05_d`, the `rc=143` line is followed by the runner's `MECHFAIL-MEMORY` line
(`ladder.log:78`), which records the marker placed so the file was not re-run unablated. **None of the
eleven has a result**, and their disposal is routed to the author (*The degraded wave*). **No box was
raised for any run, in either ladder.**

<!--NOTRUNLIST-->
**Landed under ladder 2 (69 of 80):** `cap_cc01_c`, `cap_cc02_a`, `cap_cc02_b`, `cap_cc03_a`, `cap_cc03_b`, `cap_cc04_a`, `cap_cc04_b`, `cap_cc05_a`, `cap_cc05_b`, `cap_cc06_a`, `cap_cc06_b`, `cap_cc07i_a`, `cap_cc07i_b`, `cap_cc07ii_a`, `cap_cc07ii_b`, `cap_cc08_a`, `cap_cc08_b`, `cap_cc08i_a`, `cap_cc08i_b`, `cap_cc08ii_a`, `cap_cc08ii_b`, `cap_cc09_a`, `cap_cc09_b`, `cap_cc09_d`, `cap_cc10_a`, `cap_cc10_b`, `cap_cc10_d`, `cap_cc10iso_a`, `cap_cc10iso_b`, `cap_cc11_a`, `cap_cc11_b`, `cap_cc11_d`, `cap_cc11abl6_a`, `cap_cc11abl6_b`, `cap_cc11abl6_d`, `cap_cc11q4_a`, `cap_cc11q4_b`, `cap_cc11q4_d`, `cap_cc12_a`, `cap_cc12_b`, `cap_cc12_d`, `cap_cc13i_a`, `cap_cc13i_b`, `cap_cc13i_d`, `cap_cc13ii_a`, `cap_cc13ii_b`, `cap_cc13ii_d`, `cap_cc14_a`, `cap_cc14_b`, `cap_cc15i_a`, `cap_cc15i_b`, `cap_cc15i_d`, `cap_cc15ii_a`, `cap_cc15ii_b`, `cap_cc15ii_d`, `cap_cc15iii_a`, `cap_cc15iii_b`, `cap_cc15iii_d`, `cap_cc16_a`, `cap_cc16_b`, `cap_cc16_d`, `cap_cc17_a`, `cap_cc17_b`, `cap_cc18_a`, `cap_cc18_b`, `cap_cc18_d`, `capstone`, `capstone_b`, `capstone_d`

**Mechanism failures under ladder 2 (11 of 80), no result:** `cap_cc02_d` (timeout), `cap_cc03_d` (timeout), `cap_cc04_d` (timeout), `cap_cc05_d` (memory), `cap_cc06_d` (timeout), `cap_cc07i_d` (timeout), `cap_cc07ii_d` (timeout), `cap_cc08_d` (timeout), `cap_cc08i_d` (memory), `cap_cc08ii_d` (memory), `cap_cc17_d` (memory)
<!--END-NOTRUNLIST-->

**Runs that appear in no log, and are therefore not counted below:**

- the three runs under the superseded blob `508b9018…` (*Ladder restarts*);
- the six runs killed at 18:29:30 on 2026-09-19 with no line;
- `cap_cc08_b`'s wam-nuc run, terminated 2026-09-20T19:10:41Z after its logger was already gone
  (`owner_interventions.log:8`);
- the three degraded runs interrupted by the 2026-09-28 host crash, about six hours into their boxes;
- every diagnostic run under `dev/` (`abl2a`, `recut_pre`, `abl_d`) and the staging smoke test.

### The whole-ladder ceiling

<!--CEILING-->
**The whole-ladder ceiling, taken over BOTH ladders, is EXCEEDED by 1 307 493 s: 1 591 893 s against
284 400 s, or 559.7 % (5.60 times).** *(Updated 2026-10-01 for the three BF-4 re-runs, 8 391 s. Before
them this sentence read 1 583 502 s, 556.8 %, 5.57 times.)* The ceiling is §3's *"at most 4 × 1185 = 4740 min (79 h)"*, that is
284 400 s (`PREDICTIONS.md:1620`). Solver time is the sum of the `seconds=` fields of the two ladder logs.
Killed, guard-terminated and timed-out runs all count, because the ceiling bounds what the ladder may
spend, not what it keeps.

| Ladder, machine | Log lines | Seconds | Of the ceiling |
|---|---|---|---|
| **Ladder 1** (blob `c6969b4c…`, `ladder1/ladder.log`) | 76 | **625 756** | **220.0 %** |
| — wam-nuc, 31 GB (`:15-67`) | 47 | 146 721: 28 landed (61 787), 7 `rc=137` (57 290), 12 `rc=143` (27 644) | 51.6 % |
| — ubuntu24 (`:78-108`) | 29 | 479 035: 21 landed (128 704), 4 `rc=124` (273 617), 4 `rc=143` by the 80 GB guard (76 714) | 168.4 % |
| **Ladder 2** (blob `a9fb7da1…`, `ladder.log`), all on ubuntu24 | 84 (80 files; `cap_cc05_d` has two, and each `cap_cc15i` file has two: the superseded BF-4 run and its re-run) | **966 137**: 72 landed (288 363), 7 `rc=124` (459 916), 4 `rc=143` (217 858), 1 `MECHFAIL-MEMORY` (0) | **339.7 %** |
| **Both ladders** | 160 | **1 591 893** | **559.7 %** |

*(Arithmetic, reproducible: `awk '/seconds=/{match($0,/seconds=[0-9]+/); s+=substr($0,RSTART+8,RLENGTH-8)} END{print s}' ladder1/ladder.log ladder.log`
prints 1591893. Run on each log alone, it prints 625756 and 966137. Lines 15-67 of `ladder1/ladder.log`
are wam-nuc's and lines 78-108 are ubuntu24's.)*

**Why the ceiling was exceeded: the registration prices time per query and does not price memory
(finding F-8).** Three costs outside the per-query boxes account for most of the total:

1. **Memory on the first machine.** On 31 GB, companions were killed before they could finish: ladder 1's
   19 `rc=137`/`rc=143` lines on wam-nuc account for 84 934 s and produced no result.
2. **Ladder 1's strict link-2b mechanism failures.** C-C7(i) and C-C7(ii) in (a) and (b), and C-C14, ran
   to the box or the guard on ubuntu24 before the change of tactic disposed of them (recut R-9).
3. **The degraded wave.** Each degraded run is allowed 65 700 s. In ladder 2 the eleven failing degraded
   runs alone consumed **677 774 s (238.3 % of the ceiling)**. Ladder 1's two degraded runs added
   131 407 s.

**Ladder 1 alone had already exceeded the ceiling** when its main runner was stopped: 494 349 s, 173.8 %,
before its last two degraded runs logged. The owner instance moved to ladder 2 knowing this. Every run in
both ladders ran inside its own registered per-run box (71 100 s strict, 65 700 s degraded). The eleven
`rc=124` lines (four in ladder 1, seven in ladder 2) are those boxes expiring, and no box was raised.
<!--END-CEILING-->

### As written 2026-09-19, while ladder 1 was in flight — SUPERSEDED, kept as written

*(Its generated figures are frozen as they stood: the ceiling line and the landed/outstanding list below are ladder 1's of 2026-09-19 and are no longer regenerated.)*

No timebox was skipped and no run exceeded its box: `ladder.log` records `rc` and seconds for every
run that has landed, and every `rc` there is `0`.

What is **not run** is the remainder of the ladder, which is **still running, detached**, at the time
this file was written. `run_ladder.sh` is resumable — it appends to `ladder.log` and skips any file
already logged — so the outstanding runs complete on their own and this file is regenerated with
`python3 dev/assemble.py`, which rewrites sections 1-3 from the `.out` files and touches nothing else.

**Solver time consumed that produced no result.** The six case-(a) companions terminated at
19:11:24 had each consumed **1869 s** — **11 214 s in all** — and they produce **no result**: their
`rc=143` lines are in `ladder.log` as history, no cell anywhere is filled from them, and each file is
rerun from the start. That time **counts against the 4740-min ceiling** as consumed solver time, and
the accounting above includes it, because the ceiling bounds what the ladder is permitted to spend,
not what it is permitted to keep.

**Why they are not run yet, stated rather than glossed:** findings F-3 and F-7. A companion, and
either of the two cases in which the adversary can mint authority evidence, is materially more
expensive than a strict correct-form run — by a factor this file does not yet state, because none had
landed — and the ladder is 78 runs. **This is not a timeout:** the registered boxes are 1185 min per
strict case and 1095 min for (d), every run in flight is inside its box, and §3's ablation order is
therefore **not** triggered — no ablation has been performed and none is owed. It is a report written
while the ladder is in flight.

**The whole-ladder ceiling (§3, `:1620`: "at most 4 × 1185 = 4740 min (79 h)").** The ladder's total
wall clock is the sum of the `seconds=` fields in `ladder.log` — with the note that the ladder runs up
to six files concurrently, so the *sum* is the figure to compare against the ceiling (which is a sum
of per-run boxes) and the *elapsed* wall clock is smaller. **Accounted so far: 18969 s of solver time against the 284400 s (4740 min) ceiling -- 6.67%, **within the ceiling**.** Of that, 5023 s over 3 run(s) that LANDED and 13946 s over 7 run(s) that were KILLED and produce no result (their rc=137/143 lines stay in ladder.log as history and each file is rerun).
When the ladder completes, `python3 dev/assemble.py` rewrites this figure; **if it exceeds 4740 min this file says so in this paragraph, plainly, and does not round it
away.**

**Never read across cases.** No cell in section 1, 2 or 3 is filled from another case's trace. A cell
is descended by its own run or it says *not run* (the lesson of capstone round 6).

The runs that had landed when this file was written, and the runs outstanding:

**Landed (10 of 80):** `cap_cc01_c`, `cap_cc02_a`, `cap_cc03_a`, `cap_cc04_a`, `cap_cc05_a`, `cap_cc06_a`, `cap_cc07i_a`, `capstone`, `capstone_b`, `capstone_d`

**Outstanding (70 of 80), marked *not run* in every table above:** `cap_cc02_b`, `cap_cc02_d`, `cap_cc03_b`, `cap_cc03_d`, `cap_cc04_b`, `cap_cc04_d`, `cap_cc05_b`, `cap_cc05_d`, `cap_cc06_b`, `cap_cc06_d`, `cap_cc07i_b`, `cap_cc07i_d`, `cap_cc07ii_a`, `cap_cc07ii_b`, `cap_cc07ii_d`, `cap_cc08_a`, `cap_cc08_b`, `cap_cc08_d`, `cap_cc08i_a`, `cap_cc08i_b`, `cap_cc08i_d`, `cap_cc08ii_a`, `cap_cc08ii_b`, `cap_cc08ii_d`, `cap_cc09_a`, `cap_cc09_b`, `cap_cc09_d`, `cap_cc10_a`, `cap_cc10_b`, `cap_cc10_d`, `cap_cc10iso_a`, `cap_cc10iso_b`, `cap_cc11_a`, `cap_cc11_b`, `cap_cc11_d`, `cap_cc11abl6_a`, `cap_cc11abl6_b`, `cap_cc11abl6_d`, `cap_cc11q4_a`, `cap_cc11q4_b`, `cap_cc11q4_d`, `cap_cc12_a`, `cap_cc12_b`, `cap_cc12_d`, `cap_cc13i_a`, `cap_cc13i_b`, `cap_cc13i_d`, `cap_cc13ii_a`, `cap_cc13ii_b`, `cap_cc13ii_d`, `cap_cc14_a`, `cap_cc14_b`, `cap_cc15i_a`, `cap_cc15i_b`, `cap_cc15i_d`, `cap_cc15ii_a`, `cap_cc15ii_b`, `cap_cc15ii_d`, `cap_cc15iii_a`, `cap_cc15iii_b`, `cap_cc15iii_d`, `cap_cc16_a`, `cap_cc16_b`, `cap_cc16_d`, `cap_cc17_a`, `cap_cc17_b`, `cap_cc17_d`, `cap_cc18_a`, `cap_cc18_b`, `cap_cc18_d`
