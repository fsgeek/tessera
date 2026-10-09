# Draft additions to RESULTS.md for ladder 2

**STATUS: PROPOSED DRAFT, 2026-09-24. Produced by the AI collaborator (capstone builder, directed by
the owner instance). Not adopted. The commit is the author's.** This file is text for the owner to
paste into `formal/suite/capstone/RESULTS.md`. It does not edit that file. Placeholders are written
`⟨LIKE THIS⟩` and must be filled from runs before anything is pasted. Nothing below reports a result
that was not run. "Mirror" means `/home/tony/tessera-ladder-vm-backup/proverif/`, the copy of the
ubuntu24 ladder directory. Its `ladder.log` has 106 lines, and the line numbers below refer to it.
Lines 1-67 of that log are byte-identical to wam-nuc's `proverif/ladder.log`.

---

## (a) The header's blob table

The sentence above the table currently reads **"`capstone.pv` HAS CHANGED ONCE, and this is the
record of it"**. It becomes **"`capstone.pv` HAS CHANGED TWICE"**. Replace the table's second row and
add a third:

| Blob | When | Results standing under it |
|---|---|---|
| `508b901808dc75dab3e86c2385dd8545af4cad0f` | the first build, 2026-09-19 | **NONE.** *(row unchanged)* |
| `c6969b4cc2f2e30be7a7a950af7609ea75e4c700` | after the BF-3 repair, 2026-09-19. **Ladder 1**: wam-nuc from 18:33:57 UTC, then ubuntu24 from 2026-09-20T19:11:23Z. Stopped 2026-09-24T15:06:25Z (`proverif/owner_interventions.log:10`). | **Ladder 1, ARCHIVED as history under `proverif/ladder1/`.** ⟨N⟩ runs landed under it. Every landed run is **re-run under ladder 2 as a cross-check**, and its RESULT lines must reproduce. Ladder-1 outcomes are cited as the cross-check and as mechanism-failure history. **No cell in sections 1-3 is filled from them.** |
| `a9fb7da1e4851120677b21dea4a8c98a481ad43a` | **RECUT R-9, 2026-09-24** (the owner instance's decision): `capstone.pv` plus a dated comment block and `set selFun = Term.`. Nothing else changes (`diff`: one hunk, 34 lines added, none removed). **Ladder 2.** | **every result in sections 1-3.** |

Add after the paragraph that follows the table:

> Under §8 item 2's clarification the model is identified by its contents, so `a9fb7da1…` is a
> **different model** from `c6969b4c…` and every result names its blob. Every derived file changed
> blob in the same way and only in that way. The per-file old/new blob table is
> `proverif/ladder2-staging/DERIVATION-CHECK.md` ⟨path after install⟩.

---

## (b) "Recuts (encoding, not property)" entry

**R-9: `set selFun = Term.`, applied uniformly to every case and companion file (2026-09-24, the
owner instance's decision; ladder 2).**

*What was recut.* One line was added to `capstone.pv`, `set selFun = Term.`, together with a dated
comment block. The line is the file's first non-comment line. `derive.py` was not changed. It copies
the line into every derived file, so all 80 `.pv` files carry it. Checked with `diff` against each
file's ladder-1 version: every file has exactly one hunk of 34 added lines, the same text in each,
with nothing removed. No process, check, event, query, fixture, companion mutation, registered
prediction or timebox changed.

*Why.* In ladder 1 the same three companions failed in both strict cases, as **mechanism failures on
C-Q1 link 2b conjunct 1**. The query is identified in `dev/abl2a/REPORT.md` §0. It is the fourth
query in declaration order, not link 2a, and link 2a lands in every killed run.

| companion | case (a) | case (b) |
|---|---|---|
| C-C7(i) `cap_cc07i` | `rc=124 seconds=71105 peakRSSkB=64988588`, timeout at the 71100 s box (mirror `ladder.log:79`) | `rc=124 seconds=71105 peakRSSkB=66335336` (`:87`) |
| C-C7(ii) `cap_cc07ii` | `rc=143 seconds=25426 peakRSSkB=80131372` (`:81`), SIGTERM by the 80 GB guard (`mem_guard_vm.log:3213`) | `rc=143 seconds=24435 peakRSSkB=80044452` (`:86`; `mem_guard_vm.log:5621`) |
| C-C14 `cap_cc14` | `rc=143 seconds=13667 peakRSSkB=80310108` (`:80`; `mem_guard_vm.log:2822`) | `rc=143 seconds=13186 peakRSSkB=80621176` (`:99`; `mem_guard_vm.log:7879`) |

The same runs had already died on wam-nuc (31 GB) at 17-31 GB: `:34`, `:38`, `:50` (`rc=137`) and
`:62` (`rc=143`). The degraded companions were heavier again. `cap_cc02_d` held 72 GB resident after
16 h (`mem_guard_vm.log`, last lines, 2026-09-24T15:05:20Z, `rssMB=72389`). The owner stopped launches
of further degraded companions at 15:06:25Z (`owner_interventions.log:10`).

§3's outcome vocabulary registers a timeout as *"mechanism-viability failure, evidence about the tool
or the encoding and **never** about the property, disposed by ablation **or a change of tactic**"*
(`PREDICTIONS.md:297-300`). This recut is that change of tactic. It is not an amendment, because it
touches no property, no query's shape and no registered prediction (§8 item 3).

*What the setting does.* ProVerif saturates the model's Horn clauses by resolution. In each clause
the **selection function** chooses the hypothesis that resolution unifies on. ProVerif 2.05's default
is `TermMaxsize`. `Term` gives every ordinary hypothesis weight 0 instead of its size, which drops the
preference for large facts (manual extract :8040, :8047-8050, recorded in
`dev/abl2a/manual_notes.md:20-23`). The setting changes which clauses are derived on the way to the
fixpoint and how many there are. It does not change the clauses the model generates, and it does not
change what a query asks.

*The soundness argument.* ProVerif manual 2.05, §6.6, verbatim: *"The performance settings may result
in more or fewer false attacks, but they never sacrifice soundness. It follows that when ProVerif says
that a property is satisfied, then the model really does guarantee that property, regardless of how
ProVerif has been configured using the settings presented here."* The manual is not installed on this
machine: `proverif -help` lists only options and `~/.opam` holds only the OCaml manual. The quotation
is from the manual PDF (https://bblanche.gitlabpages.inria.fr/proverif/manual.pdf, fetched 2026-09-20),
as recorded in `dev/abl2a/manual_notes.md:6-11`. **Consequence:** under `Term`, an `is true` stays
correct. The one thing the setting can cost is completeness. A query that the default proves could
come back `cannot be proved` (a false attack), or it could get slower. Either would show up as a
changed RESULT line, and the controls below are there to catch it.

*Why uniformly.* If the setting were applied only to the runs that died, the tables would be built
under two configurations (`dev/abl2a/REPORT.md:381-384`). Applied to all 80 files, every companion
still differs from its correct form by its mutation alone. The alternative was ablation step 1
(drop the depth-2 layer). It lands more reliably, but it deletes the layer this model exists to
compose. It is reserved for whatever still fails under ladder 2, by §3's order
(`REPORT.md` §(e), `:388-450`).

*The controls.*
1. **Pre-ladder control, isolated files** (`dev/abl2a/`, 10 GiB cap). `cap_cc09_a` had landed in
   ladder 1. Re-run with the one line added (`S8_ctl_cc09_selFunTerm.pv`), it reproduced **all 47
   RESULT lines identically**, in 193 s and 0.22 GiB against 297 s and 0.45 GiB unset
   (`REPORT.md:296-302`). On the isolated link-2b file, C-C5 landed in 40 s and 0.74 GiB, where the
   unset run died out of memory at 949 s. C-C7(ii) landed in 1355 s and 8.28 GiB (`REPORT.md:283-295`).
2. **Pre-ladder full files** (`dev/recut_pre/chain.log:2-4`, wam-nuc, 16 GiB cap).
   `cap_cc07ii_a` with the line added: `rc=0 seconds=6267 peakRSSkB=8861688`, 47 results.
   `cap_cc07i_a` with the line added: `rc=0 seconds=3868 peakRSSkB=5588312`, 47 results.
   `cap_cc14_a` with the line added: `rc=134` at 2798 s, when it reached the 16 GiB cap. **C-C14 is
   not shown to land under the setting.** It may again be a mechanism failure in ladder 2, and in that
   case §3's ablation order applies to it.
3. **Staging smoke test** of the ladder-2 `capstone.pv` (blob `a9fb7da1…`): see
   `DERIVATION-CHECK.md` §3. wam-nuc, 8 GiB cap: `rc=0 seconds=224 peakRSSkB=340072
   blob=a9fb7da1e4851120677b21dea4a8c98a481ad43a results=47` (`ladder2-staging/smoke.log:1`). All 47
   RESULT lines are identical to ladder 1's `capstone.out`, whose run took 374 s (`ladder.log:15`).
4. **The ladder-wide cross-check (ladder 2 itself).** Every file that landed in ladder 1 is re-run
   under ladder 2, and its RESULT stream must be identical to its archived ladder-1 `.out`. Compare
   with `diff <(grep '^RESULT' proverif/ladder1/<f>.out) <(grep '^RESULT' proverif/<f>.out)`.
   ⟨Fill in: K of N identical. List every difference, each classified as a false attack under `Term`
   (a ladder-1 `is true` that became `cannot be proved`), or anything else, which would be a finding
   and must be reported, not absorbed.⟩

*What a reader should check.*
- `diff proverif/ladder1/capstone.pv proverif/capstone.pv` shows one hunk of added lines only. The
  same holds for every derived file. The table is in `DERIVATION-CHECK.md`.
- `ladder.log`'s header line names blob `a9fb7da1e4851120677b21dea4a8c98a481ad43a`, and every result
  cell cites a ladder-2 line.
- The cross-check (control 4) is complete for every ladder-1 `rc=0` file, with zero unexplained
  differences.
- No cell is filled from `proverif/ladder1/`.
- Any ladder-2 `is true` holds under the §6.6 sentence. Any ladder-2 `cannot be proved` on a query
  that was `is true` in ladder 1 is the setting's completeness cost. It is not a violation, and it is
  disposed as a mechanism outcome, not a property outcome.

---

## (c) "Ladder restarts" rows

Append to the table. The ubuntu24 move is not yet recorded in the section as it stands.

| Launch (UTC) | Superseded because |
|---|---|
| **2026-09-20T19:10:41 to 19:11:23: the machine change** | The owner instance halted the wam-nuc ladder (`owner_interventions.log:3-8`: four SIGTERMs at 19:10:41 on `cap_cc08_b`, `cap_cc08ii_b`, `cap_cc09_b`, `cap_cc10_b`, reason *machine change*; `cap_cc08_b` has no `ladder.log` line, see the 19:11:22 note there). The ladder resumed on **ubuntu24** (wam-desktop: Hyper-V guest, dynamic memory up to 96 GB, 64 cores, Ubuntu 24.04), with the ProVerif 2.05 binary copied from wam-nuc and validated there first (`capstone.pv`: 47 RESULT lines identical). `JOBS=2`. Mirror `ladder.log:68`. A relaunch followed at 19:12:31 for the scheduling-only wave-counter fix (`:73`). **Same blob `c6969b4c…`. Scheduling only.** Runs with `rc=137/143` on wam-nuc were rerun on ubuntu24 under the runner rule. Memory guard on ubuntu24: `mem_guard_vm.sh`, SIGTERM the largest ProVerif process if RSS > 80 GB or available memory < 3000 MB. |
| **2026-09-24T15:06:25: ladder 1 stopped** | The owner instance sent SIGTERM to the main `run_ladder.sh` (pid 9943) so that no further degraded pair would launch. `cap_cc02_d` and `cap_cc03_d` were left running inside their boxes, to log their own `rc` (`owner_interventions.log:10`). Reason: the same three companions had failed in both strict cases, and the degraded companions were heavier again (`cap_cc02_d` at 70+ GB after 16.4 h). **Not a result.** |
| **⟨date⟩: ladder 2** | **A new model, not a restart of the old one.** Blob `a9fb7da1…` (recut R-9). Ladder 1's `.pv`, `.out`, `.rss` and `ladder.log`, plus the ubuntu24 `ladder.log` and guard logs, are archived **unmodified** under `proverif/ladder1/`. Ladder 2 starts from an **empty** `ladder.log`, so `run_ladder.sh` skips nothing. Its skip guard reads only the local `ladder.log`, and with no `.mechfail` files present nothing is marked in advance. Machine: ⟨host⟩, `JOBS=`⟨n⟩, memory guard ⟨script and thresholds⟩. Same boxes (71100 s strict, 65700 s degraded), same runner (byte-identical), same wave order. |

---

## (d) The ceiling paragraph (replaces the text between `<!--CEILING-->` and `<!--END-CEILING-->`)

> **The whole-ladder ceiling (§3, `PREDICTIONS.md:1620`: "at most 4 × 1185 = 4740 min (79 h)", that is,
> 284 400 s), taken over BOTH ladders: EXCEEDED.** Solver time is the sum of the `seconds=` fields in
> the ladder logs. Killed and timed-out runs count, because the ceiling bounds what the ladder may
> spend, not what it keeps.
>
> - **Ladder 1** (blob `c6969b4c…`, archived): **494 349 s** (8 239 min) over 74 logged runs, as of
>   mirror `ladder.log:106`. That is **173.8 % of the ceiling on its own**, 209 949 s over it.
>   - On **wam-nuc**, 146 721 s over 47 runs: 28 landed (`rc=0`, 61 787 s), 7 killed `rc=137`
>     (57 290 s), 12 terminated `rc=143` (27 644 s).
>   - On **ubuntu24**, 347 628 s over 27 runs: 21 landed (128 704 s), 2 timed out `rc=124`
>     (142 210 s), 4 terminated by the 80 GB guard `rc=143` (76 714 s).
>   - To add: the degraded runs in flight when ladder 1 was stopped (`cap_cc02_d`, `cap_cc03_d`),
>     ⟨s⟩ s when they log. The runs killed before any `ladder.log` line was written (the 18:29:30 kill,
>     `cap_cc08_b` at 19:10:41) and the three superseded-blob runs are not in any log and are not
>     counted.
> - **Ladder 2** (blob `a9fb7da1…`): ⟨L2⟩ s over ⟨n⟩ runs.
> - **Both ladders: ⟨494 349 + in-flight + L2⟩ s, ⟨x⟩ % of 284 400 s. The ceiling was exceeded, and
>   it was already exceeded by ladder 1 alone.** The owner instance moved to ladder 2 knowing this.
>   Continuing ladder 1 through the degraded wave would have added days for a foreseeable outcome: the
>   same three companions failing again, on files heavier still. No box was raised. Every run in both
>   ladders ran inside its own registered per-run box (71 100 s strict, 65 700 s degraded), and the two
>   `rc=124` lines are those boxes expiring.

*(Arithmetic, reproducible:
`awk '/seconds=/{match($0,/seconds=[0-9]+/); s+=substr($0,RSTART+8,RLENGTH-8)} END{print s}' ladder.log`
over the mirror gives 494349. Lines 1-67 of the mirror are wam-nuc's log, and lines 68-106 are
ubuntu24's.)*
