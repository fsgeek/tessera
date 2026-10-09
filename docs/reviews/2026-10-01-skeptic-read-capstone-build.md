# Skeptic read — the built capstone and RESULTS.md (2026-10-01)

*Reader: Claude Opus 5 (skeptic; did not build), dispatched by the owner instance (Claude Opus 5.5). Filed verbatim by the owner instance from the reader's returned text; the reader edited nothing in the repo. Scratch runs were in `/tmp` only (`ulimit -v 10 GiB; nice -n 19; timeout 1800`, one at a time, about 8 minutes of solver time): `/tmp/bf3/capstone_d_old.pv` (the pre-BF-3 model rebuilt, case (d)), `/tmp/wit/wit.pv` and `/tmp/wit/wit_d.pv` (the correct model in (a) and (d) with only extra witness queries). None is a ladder result.*

**Verdict in one line:** close to ready for the single Codex review, but not yet: seven findings need a repair pass first (S-1 to S-7). None changes a verdict. Every cited `RESULT` line checked is correct; the problems are in citations, in claims about what the witnesses show, and in what the routed decision says it costs.

## Findings

**S-1 — The BF-3 confirmation cites ladder 1's run under ladder 2's file name. Repair before review.**
- RESULTS.md:1121-1122 confirms the repair with "`capstone_d` logged `rc=0 seconds=4257`" and "`capstone_d.out:10113`".
- 4257 s is ladder 1's run (`ladder1/ladder.log:25`). Ladder 2's run took 6388 s (`ladder.log:7`).
- In the current `capstone_d.out`, line 10113 is a solver progress line. The cited `RESULT` is at `ladder1/capstone_d.out:10113`; ladder 2's is at `capstone_d.out:10341`.
- This contradicts the file's own rule that nothing is read from ladder 1 (RESULTS.md:27).
- **Repair:** cite ladder 2's line 10341 and 6388 s, or put the `ladder1/` prefix on the citation.

**S-2 — The C-C15(i) rows of "the eleven divergent rows" table cite superseded runs without saying so in the path. Repair before review.**
- RESULTS.md:575-576 cite `cap_cc15i_a.out:5436`, `cap_cc15i_b.out:5444`, `cap_cc15i_d.out:10654` and others; in the current files these land on non-`RESULT` lines. The real lines are in `ladder2-superseded/`. The dated note at :553-556 says so, but the cells do not.
- The heading at :551 ("eleven") and the sentence at :567 ("29 such `RESULT` lines … across 11 configuration-case rows") are pre-BF-4 counts. Current: 10 rows, 12 lines (recomputed).
- **Repair:** put `ladder2-superseded/` in those paths, and mark the heading and :567 as superseded with the current numbers.

**S-3 — The wrapped-standing witnesses are only shown at the unwrapped layer L0, and F-2 says "reachable at every layer". Repair before review.**
- The registration defines `HonestWrappedStandingAgreed` as fired "for an honest **wrapped** acceptance" so that a green conjunct 3 "is a severing test that ran" (PREDICTIONS.md:1210-1215), and lists `HonestStandingEstablished` "over a **wrapped** presentation" (:1341).
- In the model neither is restricted to wrapped layers: `ScopeAgreementJudge` pairs at every layer (capstone.pv:1059-1066); the witness query has no layer restriction (capstone.pv:388); `HonestStandingEstablished(pkey, bitstring)` carries no layer argument (capstone.pv:259).
- Both witness traces in the ladder are at L0 (`capstone.out:9576-9578`; `HonestStandingEstablished` over an `L0` standing-path input).
- So F-2's "reachable at every layer" (RESULTS.md:1442-1444) is not shown by the ladder.
- **The property itself holds:** scratch copies querying only `event(HonestWrappedStandingAgreed(a, L1))` and `(a, L2)` came back reachable in (a) and (d) (61 s). Scratch evidence, not a result.
- Related: conjunct 3's query also fires at L0, broader than the registered "over a wrapped presentation"; conservative (a green is harder), but should be recorded.
- **Repair:** narrow F-2 to what the ladder shows; record each witness trace's layer; add Blocked item B-5: the registered wrapped-witness forms have no layer-restricted query, and `HonestStandingEstablished` cannot express "wrapped" without an amendment.

**S-4 — Which box reading governs carries the discharge of five more matrix rows, and it is not routed to the author. Repair before review.**
- RESULTS.md:114 leaves the two readings of the companion box undecided.
- Under the predicted-red reading (PREDICTIONS.md:1867-1870), every strict severing for these rows comes from a run that did not finish inside its predicted-red query's box: D3 and D4 (C-C1 at 4279 s; C-C10 in (a)/(b)/(d)); D6 (C-C7(i), C-C7(ii) at 6139-13333 s); D9 (C-C14 ≈ 43 000 s); D7's membership half (C-C17 ≈ 27 000 s).
- Per-query time is not logged, so this does not prove the query itself overran; but under that reading these five rows rest on runs not shown inside their box — the same standing option (i) gives D1, D2, D5, D10.
- The routed cost (RESULTS.md:908-913) names only four rows.
- **Repair:** a row-by-row table of which reading each severing depends on; then route the choice of reading to the author, or state from §3's "Timeboxes are per run" (:304-305) why the per-case-sum reading is the registered one.

**S-5 — The four memory-guard terminations are the owner's rule, made with memory to spare. Repair before review (wording).**
- The registration bounds time only; "memory" does not appear in PREDICTIONS.md. Classifying `rc=143` as a mechanism failure is a clerk disposition (`mem_guard_vm.sh` header).
- At each of the four ladder-2 triggers, 15-39 GB were still available on a 120-171 GB guest (`mem_guard_vm.log:10972`, `:16282`, `:16574`, `:19267`).
- `cap_cc05_d` (64899 s) and `cap_cc17_d` (64379 s): no difference, >98% of the box spent. `cap_cc08ii_d` (39900 s) and `cap_cc08i_d` (48680 s) were stopped with 26-39% of their box left; they are isolation configurations and bear on no matrix row directly.
- **Repair:** label the classification as the owner's, state the headroom, and say in the routed section why re-running those two with the cap raised is not offered.

**S-6 — G1 vs G2: the classifications hold, but G2's wording and its loose end need fixing. Repair before review.**
- G2's "only the composition could show it" (RESULTS.md:928-934; DIAGNOSIS.md:59) is right about the families, but the registration's own C-Q6 mapping row names C-C10 and C-C14 as removing the check that pins C-Q6's `t` (PREDICTIONS.md:1018), and restricting the unrestricted form to strict cases encodes the same dependence. Better wording: composition confirms a dependence the registration encoded but mis-predicted in C-C10's set (2).
- Item 4 says "set (2) was wrong" but proposes no amendment, so C-C10 (a)/(b) stays DIVERGENT with no route to close it.
- G2 leans on `cap_cc01_c.out:12611`, which B-4 and RESULTS.md:167, :618 say is "read nowhere".
- G1 as "registration defect" is defensible; the S-P1 family itself shows authorship going red under byte unbinding (`d6e`, `:809`, cited at PREDICTIONS.md:1570), so it is not composition-only; DIAGNOSIS should cite that.
- G4 and C-C15(i) conjunct 3 are correctly classed. None of the three "registration defect" labels hides a broken fixture.
- **Repair:** reword G2; add an amendment-shaped item for C-C10's set (2); mark the case-(c) line as diagnostic, not a registered reading.

**S-7 — D10's "(β) half" reads as partial discharge. Repair before review (wording).**
- §A3.3 requires a companion that "fails the query consuming the severed link" (`docs/phase-0-prereg-amendment-3.md:223`). D10's consuming query is C-Q5 `SetAltered`.
- C-Q5 is green in every landed run; C-Q9's red is the producer's own companion.
- So D10's consuming-query requirement is unmet in every case, which is what option (i) would concede for D10. RESULTS.md:655-656 and :908 say "D10's (α) half" instead.
- **Repair:** say this plainly in §3 and in the cost of option (i).

**S-8 — F-9 credits the recut for landing case (c), which was never a ladder-1 mechanism failure. Note.** In ladder 1, case (c) was an owner kill at 2732 s on the 31 GB machine (`ladder1/ladder.log:24`), never re-run; no control.

**S-9 — The degraded-wave prediction score. Note.** "17 of 17" (:859) counts the hedged "may land" as a prediction that held. The prediction file's heading says 04:30 UTC; the launch was 04:26:14Z (`ladder.log:71`); the file's mtime, 04:26:12.9, is 1.1 s before the launch. The file is untracked, so "written before" rests on that mtime alone.

**S-10 — The predicted-red box column uses the smallest box, not the registration's stated assignments. Note.** The registration assigns C-C17 to link 2a's 45-minute box, C-C16 to link 5's 60-minute box and C-C9 to link 2b's (PREDICTIONS.md:1872-1875); section 2 uses 30 minutes for all three (RESULTS.md:134). No yes/no changes.

**S-11 — Small wording problems. Note.** "Both ladders are complete" (RESULTS.md:5, :45): ladder 1 was stopped by the owner (`owner_interventions.log:10`). BF-4's "Cleared (out-of-set reds now green)" (:1215) includes C-Q3, which is in C-C15(i)'s set (1); it is green in strict only through the per-case Cases cell.

**S-12 — BF-3's evidence was deleted but can be rebuilt; the reader rebuilt it. Note, in BF-3's favour.** The pre-repair model rebuilt as the ladder-1 text with the Front reverted (ladder-1 hash `c6969b4c…`; reverted `capstone_d_old.pv` `7d14ec3a`), default selection function, 6 minutes, differs from ladder 2's `capstone_d` in exactly one `RESULT` line: conjunct 3 `is false`, with the trace BF-3 describes (`(aid_7, L0)`, `authTuple(a_3, fp(pk(a_4))…)` against `authTuple(a_15, fp(pk(a_16))…)`, `/tmp/bf3/capstone_d_old.out:5756-5794`). That red sits at L0, outside conjunct 3's registered wrapped scope; the repair is right regardless. **Repair:** keep the rebuild script, or cite this run.

## Checked and found correct

- **R-9's model change.** `capstone.pv` with its 34-line recut block removed hashes to `c6969b4c…`. Printed initial processes in `ladder1/capstone.out` and `capstone.out` are identical. `ladder2-staging/` matches every current `.pv` except the three BF-4 files. The only change to `derive.py` is BF-4.
- **R-9's cross-check**, recomputed: 49 identical, 7 prefix-consistent, 2 empty; `cap_cc15i_{a,b}` match ladder 1 against `ladder2-superseded/`; no `cannot be proved` anywhere.
- **R-9's controls**: the C-C9 selection-function control is identical to ladder 1; `recut_pre`'s cc07i_a and cc07ii_a runs are identical to ladder 2; the soundness quote is as recorded; nothing is read as stronger because of the recut.
- **BF-3 is exactly §1.3's contract**: the printed-process diff between `dev/first.out` and ladder 1 shows only the one-read Front with private forwarding and the three paths reading from `envMat`/`stdMat`/`standCore` instead of `c`. No check added. Matches `cap15a…pv:390-396` and §1.3/(E1) (PREDICTIONS.md:144-150, :898-906).
- **BF-4 touches reports only** (27 for 27 lines, every one an `event`/`out`, `kA`/`kB` → `kEncW`), matches the registered contract (:2503) and the descent (`cap25a…pv:331-336`), and hides no registered red.
- **G4 and conjunct 3 for C-C15(i)** are correctly classed.
- **All 201 `.out:line` verdict citations** in sections 1, 2, 2a, 3 land on `RESULT` lines with the stated verdict.
- **Section 2's observed-reds column** equals the non-witness `is false` lines of every landed `.out`; witness counts correct.
- **Every cell comes from its own `rc=0` run**; no killed or partial run fills a cell.
- **ladder.log line numbers and blobs**: all 80 latest `blob=` values equal the hash of the current `.pv`.
- **Counts:** 69/11, 56/10/11, 173 cells, 7 `rc=124` + 4 `rc=143`.
- **Ceiling arithmetic:** 1,591,893 s; 625,756 and 966,137 per ladder; wam-nuc 146,721; ubuntu24 479,035; degraded failures 677,774 and 131,407; 559.7%.
- **Provenance labels**: the owner's recommendation is labelled a recommendation, the amendment items clerk findings not entered; nothing uses the grammar of an author ruling.

## Verdict

RESULTS.md is not yet ready for the single cross-family (Codex) review. The underlying record is sound: every verdict cell traces to its own landed run; the recut moved no verdict; BF-3's repair is exactly §1.3's contract, independently reproduced; BF-4 is confined to reports and matches the registered contract; the numbers recompute. What must change first is narrow: fix the two citation problems (S-1, S-2); stop claiming wrapped-layer witness reachability the ladder did not show and record the layer gap (S-3); and make the routed decision complete and honest about its cost — route the box-reading question with its effect on D3, D4, D6, D7-membership and D9 (S-4), label the memory-guard terminations as the owner's disposition (S-5), state D10's consuming-query gap plainly (S-7), tighten G2 and give C-C10's set (2) a route (S-6). S-8 to S-12 are notes the reviewer can see as they stand. After that pass, the file should go to Codex.
