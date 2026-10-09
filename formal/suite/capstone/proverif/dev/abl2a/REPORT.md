# Link-2b-conjunct-1 memory diagnosis — scratch report

**STATUS: SCRATCH / PROPOSED — 2026-09-20 — produced by the AI collaborator
(Claude Opus 5, capstone builder, directed by the owner instance). Nothing here
is adopted; nothing here is a capstone result; nothing outside this directory
was modified.**

Everything below was run by this session under a **hard 10 GiB virtual-memory
cap** (`ulimit -v 10485760`), `nice -n 19`, `timeout 3600`, ProVerif 2.05,
`-lib ../../../../lib/tessera_theory.pvl`, **one experiment at a time, never
two**. The per-run record is `abl.log` in this directory; every `.out` cited is
here too. **No result below was written without being run.**

---

## 0. A correction to the brief, before anything else

The task named the killer query *"the fourth in declaration order … C-Q1 link
2a, `event(AcceptanceComplete(aid, lyr, authTuple(...))) ==> event(SlotSatisfied(...))`"*.
The **query shape is right; the label is wrong**. In `capstone.pv` the
declaration order is

| # | query | `capstone.pv` |
|---|---|---|
| 1 | `event(ChainBroken(l, LINK_1A))` | :241 |
| 2 | link 1b, `LayerAccepted ==> AuthorityPublished{DNS,Repo}` | :244-247 |
| 3 | **link 2a**, `event(ChainBroken(l, LINK_2A))` | :250 |
| 4 | **link 2b, conjunct 1** (`signers0`), `AcceptanceComplete ==> SlotSatisfied` | :253-256 |
| 5 | link 2b, conjunct 2 (`signers1(fpB)`, slot A) | :257-260 |
| 6 | link 2b, conjunct 3 (`signers1(fpB)`, slot B) | :261-264 |

**Link 2a is query 3 and it LANDS in every one of the eight killed runs.** What
kills them is **query 4 — link 2b's first conjunct**, the `|set| = 1` conjunct.
Cited, from the killed runs' own `.out` files (`-- Query` / `RESULT` lines):

| run | link 2a (query 3) result | query 4 opened at | run ends at |
|---|---|---|---|
| `cap_cc05_a.out` | `is true` :3868 | :3869 | :5046 (EOF, killed) |
| `cap_cc07i_a.out` | `is true` :7613 | :7614 | :10186 |
| `cap_cc07ii_a.out` | `is true` :7441 | :7442 | :9970 |
| `cap_cc14_a.out` | `is true` :5839 | :5840 | :8805 |
| `cap_cc17_a.out` | **`is false`** :6511 | :6512 | :8093 |
| `cap_cc05_b.out` | `is true` :3694 | :3695 | :4757 |
| `cap_cc06_b.out` | `is true` :3757 | :3758 → **`is true` :5060** | :6125 |
| `cap_cc07i_b.out` | `is true` :7411 | :7412 | :11628 |

Two further corrections fall out of that table:

* **`cap_cc06_b` did not die on query 4.** It resolved query 4 `is true`
  (`cap_cc06_b.out:5060`) and died on **query 5**, link 2b conjunct 2
  (`:5061`). Seven of the eight died on query 4; the eighth died on query 5.
  The killer is the **link 2b correspondence group**, not one query.
* **`cap_cc17_a` reds link 2a** (`cap_cc17_a.out:6511`, `is false`), which is
  C-C17's registered red (§9(4), PREDICTIONS.md:2666) **reached before the
  kill** — so that companion's registered red is already on the record from a
  run that was later killed for memory on a *different* query.

The rest of this report says **"link 2b conj 1"** for the query under
diagnosis, and flags the label question as amendment-shaped in §(f).

---

## (a) Diagnosis — what the six companions have in common

All six companions — **C-C5, C-C6, C-C7(i), C-C7(ii), C-C14, C-C17** — do the
same structural thing, and it is the thing ProVerif's saturation is most
sensitive to: **each of them deletes the one equality that had held a variable
of the acceptance path RIGID, i.e. pinned to a closed term or to the fixture's
finite set of honest terms, and leaves a free variable in its place.** Four of
them (C-C5, C-C6, C-C7(i), C-C7(ii)) do it to the **payload of a `checksign`**:
`capstone.pv:561` reads `let (=BYTES, =fbA) = checksign(sgA, kA) in`, which
forces the signed payload to unify with the *one* presented-bytes term, so the
attacker's entire `sign(x, sk)` space collapses to a single instance;
`derive.py:338-366` replaces that pin with a free variable (`anybA`, C-C5), or
with a free variable plus a **disjunctive waiver** (`sbA = fbA || …`, C-C6 and
C-C7(ii)), or with an equality on a *different, derived* field
(`sigFrameKfp(sbA, kA) = fp(kA)`, C-C7(i), whose `otherwise` clause at
`derive.py:249-255` returns `fp(k)` for **any non-`framed` term**, so every
non-frame payload passes). C-C14 (`derive.py:481-511`) does it to check 1: the
authority evidence's payload pin falls from `=h(t)` — a rigid term over **all
five** D-2 fields, which in strict pins `t` to the three fixture manifests
`M1`/`M2`/`MW` because the repository key is honest — to `=idE`, **one field**,
so `t` becomes an `authTuple` with four free fields. C-C17
(`derive.py:524-528`) does it to check 3: dropping `if fp(kB) = kfprB then`
frees **`kB`**, so `checksign(ppfB, kB)` and `checksign(sgB, kB)` must be solved
for every attacker key rather than for the one the signed set names. In every
case the term set unifiable with the tuple facts (`AcceptanceComplete`'s
`authTuple(…)`) and with the slot facts (`SlotSatisfied`'s `fpA`) grows from a
handful of fixture instances to the attacker's whole constructed-term space, and
the saturation churns instead of converging: the killed runs' own tails show the
rule base and the queue both **flat** while hundreds of thousands of further
rules are inserted and discarded (`cap_cc07ii_a.out:9966-9970` — 505 200 rules
inserted, base stuck at 133 841, queue at 31 584; `cap_cc17_a.out:8089-8093` —
315 800 inserted, base stuck at 74 145, queue at 15 920), with the resident set
climbing all the while. **Memory, not time, is the binding resource**, and it is
spent on the term structure ProVerif has to keep, not on a growing base. **Why the link-2b conjuncts and not links 1a/2a:** queries 1
and 3 are `event(ChainBroken(l, LINK_*))`, a goal fact with **one** variable, so
ProVerif abstracts the whole acceptance away as soon as it reaches the judge;
query 2 (link 1b) has a nine-argument premise but a conclusion mentioning only
`t`, which the honest `AuthorityPublished*` facts pin to three ground terms and
close fast. Query 4 is the **first** goal whose fact carries a *structured,
partly instantiated* argument — `authTuple(id, fpA, signers0, alg, ver)` — with
`fpA` **shared between premise and conclusion**; ProVerif cannot abstract the
tuple, so every derivation of `AcceptanceComplete` must be kept with its tuple
instance, and the mutation's newly-free variables are exactly the tuple's and
the key's. **Why `cap_cc06_a` still landed** (rc=0, 15 228 s, **20.8 GiB** —
`ladder.log`, `peakRSSkB=21769120`): C-C6 is the same disjunctive-waiver shape as C-C7(ii), but its
waiver condition, `sigFrameKfp(sbA, kA) <> fp(kA)`, is a disequality on the
signed frame's **key-fingerprint** field against `fp(kA)` — a term the rest of
the path still pins — so the waived branch stays tied to the accepting key and
ProVerif can close branches on it; C-C7(ii)'s waiver, `sigFrameOt(sbA) <>
OT_ATTEST`, is a disequality on the **objType** field against a constant,
leaving all six key- and manifest-bearing fields of the signed frame free. That
is a difference of degree, not of kind: `cap_cc06_a` needed 20.8 GiB and 4 h 14
on a 31 GiB machine, and its case-(b) twin `cap_cc06_b` **was killed** at 19.9 GiB
on query 5 — the same phenomenon, landing on one side of the machine's ceiling
and not the other.

---

## (b) Every experiment run

**Protocol.** `run1.sh` in this directory is the only runner used:

```
( ulimit -v 10485760;
  /usr/bin/time -f %M -o <n>.rss nice -n 19 timeout 3600 \
    proverif -lib ../../../../lib/tessera_theory.pvl <n>.pv > <n>.out 2>&1 )
```

(The task's `-lib ../../../lib/…` would resolve to `formal/suite/capstone/lib`,
which does not exist; from `dev/abl2a/` the shared library is four levels up.
Nothing else about the command changed.) `abl.log` records, per run, the UTC
start, the `git hash-object` blob, `MemAvailable` at start, the rc, the wall
seconds, `/usr/bin/time`'s `%M` peak RSS in kB, and the `RESULT` lines.

**Every file below is built by `mk.py` / `mkset.py` in this directory from a
`cap_*.pv` in the parent, read-only.** `mk.py` asserts that each ablation's
anchor occurs exactly once before substituting, so no ablation can silently
remove more than it names; `diff` against the isolated file is in `abl.log`'s
sibling `*.pv` and was checked by hand for each.

| file | source | what changed | blob | rc | s | peak RSS | link-2b-conj-1 result |
|---|---|---|---|---|---|---|---|
| `E0_cc07ii_iso.pv` | `cap_cc07ii_a.pv` | isolated: every query but link 2b conjunct 1 deleted; nothing else changed | `e22133273667` | 134 | 1683 | 9.44 GiB | **no result — Fatal error: out of memory** (`E0_cc07ii_iso.out:3557`); saturation had reached 209800 rules inserted. Base: 65760 rules (695 with conclusion selected). Queue: 25282 rules. |
| `E1_cc07ii.pv` | `E0_cc07ii_iso.pv` | + ablation 1: the depth-2 layer dropped (the L1->L2 WrapStage and SUnwrap instances) | `3bcf4c108fee` | 0 | 1490 | 8.23 GiB | **`is true`** — `E1_cc07ii.out:3390` |
| `F0_cc14_iso.pv` | `cap_cc14_a.pv` | isolated: every query but link 2b conjunct 1 deleted; nothing else changed | `70a5b7cc9f52` | 134 | 443 | 9.44 GiB | **no result — Fatal error: out of memory** (`F0_cc14_iso.out:3469`); saturation had reached 191800 rules inserted. Base: 53209 rules (4995 with conclusion selected). Queue: 13529 rules. |
| `F1_cc14.pv` | `F0_cc14_iso.pv` | + ablation 1 | `60a12d76622f` | 0 | 81 | 1.51 GiB | **`is true`** — `F1_cc14.out:2630` |
| `S2_redundantHypElim.pv` | `E0_cc07ii_iso.pv` | `set redundantHypElim = true.` added, nothing else (default is beginOnly) | `d785779abf6b` | 134 | 974 | 9.44 GiB | **no result — Fatal error: out of memory** (`S2_redundantHypElim.out:3476`); saturation had reached 193600 rules inserted. Base: 61653 rules (695 with conclusion selected). Queue: 19530 rules. |
| `S3_selFunTerm.pv` | `E0_cc07ii_iso.pv` | `set selFun = Term.` added, nothing else (default is TermMaxsize) | `eb63544710b8` | 0 | 1355 | 8.28 GiB | **`is true`** — `S3_selFunTerm.out:4362` |
| `S8_ctl_cc09_selFunTerm.pv` | `cap_cc09_a.pv` | CONTROL: the FULL landed companion C-C9, all 47 queries, `set selFun = Term.` added and nothing else | `eddd0dbe4cdd` | 0 | 193 | 0.22 GiB | **47 of 47 results, ALL IDENTICAL to the committed `cap_cc09_a.out`** (`diff` of the two RESULT streams is empty); committed run was 297 s / 0.45 GiB |
| `S7_cc14_selFunTerm.pv` | `F0_cc14_iso.pv` | `set selFun = Term.` added, nothing else | `00eb2d982a55` | 134 | 1411 | 9.44 GiB | **no result — Fatal error: out of memory** (`S7_cc14_selFunTerm.out:4692`); saturation had reached 436400 rules inserted. Base: 49235 rules (4445 with conclusion selected). Queue: 15556 rules. |
| `S6_nounif_stageL2.pv` | `E0_cc07ii_iso.pv` | `set selFun = NounifsetMaxsize.` + a nounif on mess(stageCh, (.., L2, ..)) -- the fact ablation 1 removes, here only made unselectable | `5c0b84f60f01` | 134 | 1127 | 9.44 GiB | **no result — Fatal error: out of memory** (`S6_nounif_stageL2.out:3557`); saturation had reached 209600 rules inserted. Base: 65588 rules (695 with conclusion selected). Queue: 25282 rules. |
| `S9_nounif_sigs.pv` | `E0_cc07ii_iso.pv` | `set selFun = NounifsetMaxsize.` + nounif (star variables) on attacker(sign((BYTES|POSS|STMT_DIGEST, *x), *k)) -- the 45% of selections verboseRules found | `c9e4224c9d6e` | 134 | 354 | 9.44 GiB | **no result — Fatal error: out of memory** (`S9_nounif_sigs.out:2776`); saturation had reached 53000 rules inserted. Base: 30001 rules (7582 with conclusion selected). Queue: 70258 rules. |
| `S10_cc05_selFunTerm.pv` | `G0_cc05_iso.pv` | `set selFun = Term.` added, nothing else | `fabbe061a556` | 0 | 40 | 0.74 GiB | **`is true`** — `S10_cc05_selFunTerm.out:2743` |
| `S11_cc17_selFunTerm.pv` | `H0_cc17_iso.pv` | `set selFun = Term.` added, nothing else | `ed638f4a5a83` | 134 | 1543 | 9.43 GiB | **no result — Fatal error: out of memory** (`S11_cc17_selFunTerm.out:3873`); saturation had reached 277800 rules inserted. Base: 38472 rules (4035 with conclusion selected). Queue: 10307 rules. |
| `G0_cc05_iso.pv` | `cap_cc05_a.pv` | isolated: every query but link 2b conjunct 1 deleted; nothing else changed | `bca157db44fb` | 134 | 949 | 9.43 GiB | **no result — Fatal error: out of memory** (`G0_cc05_iso.out:3447`); saturation had reached 191400 rules inserted. Base: 53055 rules (1225 with conclusion selected). Queue: 7510 rules. |
| `H0_cc17_iso.pv` | `cap_cc17_a.pv` | isolated: every query but link 2b conjunct 1 deleted; nothing else changed | `432be65a8592` | 134 | 421 | 9.43 GiB | **no result — Fatal error: out of memory** (`H0_cc17_iso.out:3109`); saturation had reached 125000 rules inserted. Base: 34145 rules (2457 with conclusion selected). Queue: 7190 rules. |
| `G1_cc05.pv` | `G0_cc05_iso.pv` | + ablation 1: the depth-2 layer dropped | `71ed3316a826` | 0 | 422 | 3.87 GiB | **`is true`** — `G1_cc05.out:2787` |
| `H1_cc17.pv` | `H0_cc17_iso.pv` | + ablation 1: the depth-2 layer dropped | `d79d259577ba` | 0 | 131 | 1.71 GiB | **`is true`** — `H1_cc17.out:2516` |

**How to read the SECONDS column — a fairness caveat.** The owner's ladder was
running three concurrent ProVerif jobs on this machine until it was halted at
**19:10:41 UTC** for the move to ubuntu24 (`owner_interventions.log`). So
`E0_cc07ii_iso` (18:37-19:05) and part of `E1_cc07ii` (19:06-19:30) ran against
that load, and **everything from `F0_cc14_iso` (19:31) onward ran on a quiet
machine**. All runs were `nice -n 19`, and `MemAvailable` at each start is in
`abl.log` (24.3 GiB for E0, 28-28.5 GiB for the rest), so no run was memory-starved
— but **seconds are not strictly comparable across that boundary**, and the two
earliest rows are if anything flattered *against*, not for. The rc=134/rc=0
outcomes and the peak-RSS figures are unaffected: the cap is a per-process
`ulimit -v`, not a share of the machine.

**UNITS.** Every memory figure in this report is **GiB = kB / 2^20**, computed
from `/usr/bin/time -f %M`. The brief and `ladder.log`'s readers have
sometimes quoted the same `peakRSSkB` values as kB / 10^6 (so 30 723 792 kB
appears as "30.7 GB" there and as **29.3 GiB** here). The underlying kB
figures are unchanged and are in `ladder.log` and `abl.log`; the cap used
here, `ulimit -v 10485760`, is **10 GiB** exactly.

**How to read the peak-RSS column.** It is `/usr/bin/time -f %M` in kB, divided
by 1 048 576. A row with rc=134 is a run **killed by the 10 GiB cap** — OCaml's
`Fatal error: out of memory`, the `.out` line cited in the last column — and its
peak RSS is therefore the cap, not a measurement of what the run needed. **The
cap was never raised.** A row with rc=0 landed inside both the cap and the
3600 s box.

**The un-ablated, un-set baselines, gathered in one place** (all four isolated
files die, all at the cap):

| companion | isolated, nothing added | + registered ablation 1 | + `set selFun = Term.` |
|---|---|---|---|
| **C-C5** | OOM, 949 s | **lands, 422 s, 3.87 GiB, `is true`** | **lands, 40 s, 0.74 GiB, `is true`** |
| **C-C7(ii)** | OOM, 1683 s | **lands, 1490 s, 8.23 GiB, `is true`** | **lands, 1355 s, 8.28 GiB, `is true`** |
| **C-C14** | OOM, 443 s | **lands, 81 s, 1.51 GiB, `is true`** | OOM, 1411 s |
| **C-C17** | OOM, 421 s | **lands, 131 s, 1.71 GiB, `is true`** | OOM, 1543 s |

**Every landing, by either route, is `is true`.** Where both routes land, they
agree; where only one lands, it is the registered ablation.

---

## (c) The break point in the registered order

**On every companion tried, the break point is STEP 1 — "drop the depth-2
layer" — and nothing beyond it is needed.** The task asked for two companions;
because step 1 landed so cheaply, two more were run at no great cost, and all
four agree:

| companion | isolated dies at | step 1 lands at | steps 2, 3, 4 |
|---|---|---|---|
| **C-C7(ii)** (`cap_cc07ii_a`) | 9.44 GiB, 1683 s | 1490 s, 8.23 GiB | **not run** |
| **C-C14** (`cap_cc14_a`) | 9.44 GiB, 443 s | 81 s, 1.51 GiB | **not run** |
| **C-C5** (`cap_cc05_a`) | 9.43 GiB, 949 s | 422 s, 3.87 GiB | **not run** |
| **C-C17** (`cap_cc17_a`) | 9.43 GiB, 421 s | 131 s, 1.71 GiB | **not run** |

"Break point recorded" means the order stops at the first step that lands, so
steps 2-4 were not run on any of them. Their files are built and parse-checked
and are left here **unrun** (`E12_cc07ii.pv`, `E123_cc07ii.pv`,
`E1234_cc07ii.pv`, `F12_cc14.pv`, `F123_cc14.pv`, `F1234_cc14.pv`) so the owner
can see exactly what steps 2-4 would have been under this reading of §3.

**How each ablation was read, since §3 states them in four words each.**
Step 1 = delete the `L1 -> L2` instances of `WrapStage` and `SUnwrap` from the
fixture (`capstone.pv:1079-1080`), which bounds depth at 1; `L0 -> L1` stays.
Step 2 = delete `skI2`'s publication, its `honestKeyCh` / `honestMemberCh`
entries and its `ShipIssuer` / `RefuseIssuer` instances, leaving the manifest
`M1` (which names `fp(pk(skI2))`) in place, because the step names the key, not
the manifest. Step 3 = delete the `RefuseIssuer` instances — §1.1's *"both
terminal dispositions present across the fixture"*, of which `RefuseIssuer`'s
`lineage2(ABANDONED, ABANDONED)` / `TERM_REFUSED` is the second, `ShipIssuer`'s
`lineage2(ABANDONED, SHIPPED)` / `TERM_SHIPPED` the first. Step 4 = delete the
two-signer branch of `AttestStage` and of `WrapStage` in full. **Steps 2-4 were
not exercised, so these readings are recorded but untested.**

**What step 1 costs, stated plainly.** It bounds the model's depth at **1**.
Every claim the capstone makes *at* `L2` is outside such a run: §1.3's
three-layer `lyr`, C-N1's `HonestChain(L2, t)` witness, C-C15(ii)'s "middle
layer rather than innermost" scope, and the depth-2 half of C-Q6. That is the
registered price of step 1, and §3 already says what such a run is worth: a
timeout is *"evidence about the tool or the encoding and **never** about the
property"* (`PREDICTIONS.md:298-299`), and the ablated run is evidence of the same kind.

**Two cautions on these numbers.** First, every one is for **one query in a file
containing only that query**, under a **10 GiB** cap that is tighter than the
owner's 31 GiB machine — they identify what makes this conjunct unaffordable,
not what a whole companion file costs. Second, `C-C17`'s own mutation lives in
the `|set| = 2` branch (`derive.py:524-528`), which is what **step 4** deletes;
so had the order run that far on C-C17 it would have deleted the companion
itself. That is a reason to prefer C-C14 as the second companion — which is what
the task asked for and what was done — and a thing worth the owner's eye.

---

## (d) Solver settings and `nounif`, with no fixture ablation at all

Every file in this section is `E0_cc07ii_iso.pv` (or the matching isolated file
of another companion) with **lines added and nothing else changed**
(`mkset.py`). Defaults are from the ProVerif 2.05 manual; `manual_notes.md` in
this directory carries the quotations with the extraction line numbers, and the
extracted text is in this session's scratchpad.

### Four of the brief's five candidates are no-ops or off-target, by the manual

| candidate | why it was not run |
|---|---|
| `set redundancyElim = simple` | **the default is already `best`** — manual, verbatim: *"By default, set redundancyElim = best."* The candidate would **weaken** the current configuration, not strengthen it. |
| `set preciseActions = false` | **that IS the default.** (`= true` *raises* precision at a cost; `S5_preciseActions.pv` is built and left **unrun**.) |
| `set simplifyDerivation = false` | an **attack-reconstruction** setting, under the manual's heading *"Attack reconstruction settings"*. The kills happen during **saturation**, before any derivation is reconstructed. |
| `set nounifIgnoreNtimes = n` | affects only `nounif`/`noselect` declarations carrying the `ignoreAFewTimes` option (default n = 1). With no such declaration in the file it does nothing. |

### What was run, and what happened

**1. `set redundantHypElim = true.` (default `beginOnly`) — FAILED, AND MADE IT
WORSE.** Chosen in place of the redundancy candidate because the manual promises
*"huge speedups"* on *"big examples, in particular when they contain many events
(or blocking facts)"*, which is this model exactly.
`S2_redundantHypElim.pv`: rc=134, **974 s** to `Fatal error: out of memory`,
against **1683 s** for the identical file without it. The extra subsumption test
costs time and buys nothing: at 148 000 rules its base is 55 638, against 56 632
at 155 000 rules unset.

**2. `set selFun = Term.` (default `TermMaxsize`) — THIS WORKS, ON TWO OF THE
FOUR.** It lands **C-C7(ii)** (1355 s, 8.28 GiB, `is true`,
`S3_selFunTerm.out:4362`) and **C-C5** (**40 s, 0.74 GiB**, `is true`,
`S10_cc05_selFunTerm.out:2743`, against 949 s to OOM unset — a 24-fold
speed-up, and it finishes inside 0.74 GiB where the un-set run had consumed
all 10 GiB). It does **not** land **C-C14**
(`S7_cc14_selFunTerm.pv`, OOM at 1411 s) or **C-C17**
(`S11_cc17_selFunTerm.pv`, OOM at 1543 s) — though on both it buys roughly
3-4x more time before the same wall (C-C14: 443 s → 1411 s; C-C17: 421 s →
1543 s). **Where it lands, it converges rather than churning:** on C-C7(ii) the
queue fell to 2 076 rules at 20 minutes and then to completion, where the
default configuration's queue sat at 18 000-25 000 until the kill.

**3. THE CONTROL, and it is the important row.** `cap_cc09_a` — a companion that
**already landed**, all 47 queries — re-run with `set selFun = Term.` added and
nothing else (`S8_ctl_cc09_selFunTerm.pv`): **all 47 RESULT lines identical** to
the committed `cap_cc09_a.out` (a `diff` of the two RESULT streams is empty),
in **193 s / 0.22 GiB** against the committed **297 s / 0.45 GiB**. On this model
the setting is faster, smaller and outcome-identical.

**4. `nounif` — TRIED TWICE, FAILED TWICE, and the second failure is
informative.**

* **The targeted one.** `S6_nounif_stageL2.pv` sets `selFun = NounifsetMaxsize`
  and declares `nounif …; mess(stageCh, (aq, L2, cq, kq, iq, faq, saq, fbq, sbq)).`
  — an attempt to get ablation 1's effect **without removing the depth-2 layer
  from the model**, by making the layer-pipeline fact unattractive to the
  selection function instead of deleting it. **It changed nothing at all:** rc=134
  at 1127 s, and the saturation trace is **byte-identical** to the un-set run for
  the first 200 progress lines (`diff` of the `rules inserted` lines is empty),
  dying at the same output line (`:3557` in both). Either that `mess` fact is
  never a selectable hypothesis in the clauses that matter, or the pattern never
  matched; **I did not establish which**, and a reader should treat this as an
  experiment that did not fire rather than as evidence about `nounif`.
* **The one chosen by the manual's own procedure.** The manual says (§6.7.2):
  *"one typically uses set verboseRules = true. to display the clauses generated
  by ProVerif. One can then observe the loops that occur, and one can try to
  avoid them by using a nounif declaration that prevents the selection of the
  literal that causes the loop."* Done: a **300-second diagnostic** with
  `verboseRules` on the isolated file (`diag.sh`, 772 MB of output, since
  deleted) shows **90 129 selections**, of which **40 687 (45%) are on
  `attacker(sign(...))` facts** — split `STMT_DIGEST` 14 344, `BYTES` 13 836,
  `POSS` 12 480, i.e. **exactly the three signature families §(a) says the
  mutations unpin**, and only 568 clauses with the conclusion selected. The
  diagnostic also shows why memory goes: the clauses carry dozens of
  `attacker(...)` hypotheses each and page-long disequality constraints.
  `S9_nounif_sigs.pv` therefore declares, with **star variables** so the
  declarations match concrete terms and not only variables,
  `nounif …; attacker(sign((BYTES, *xb), *kb)).` and the same for `POSS` and
  `STMT_DIGEST`. **It made things much worse:** rc=134 at **354 s** — the
  fastest death of any run here — with the queue blown out to **70 258** rules
  against 25 282 unset. Forbidding the selection of those facts forces the
  conclusion to be selected instead, and the resulting clauses are bigger.

### What these settings do to the tool's completeness, precisely

* **`set selFun = Term.` cannot make a `true` wrong.** The manual, verbatim,
  §6.6: *"The performance settings may result in more or fewer false attacks,
  but they never sacrifice soundness. It follows that when ProVerif says that a
  property is satisfied, then the model really does guarantee that property,
  regardless of how ProVerif has been configured using the settings presented
  here."* The selection function governs **which literal resolution unifies
  upon**; it changes no clause, no model and no query. **What it can cost:**
  `Term` gives ordinary hypotheses weight 0 instead of their size, dropping the
  `Maxsize` tie-break that the manual says *"sometimes gives impressive
  speedups"*. So some other query could get **slower** under it, or could return
  `cannot be proved` where the default proves — **a false attack, never a false
  proof.** A false attack is visible: it is a changed result, which is what the
  control run is for.
* **`nounif` is weaker than that, and the manual says so in terms.** §6.7.2:
  ***"The nounif declarations help the saturation procedure to terminate but
  they may lower the precision of ProVerif by preventing resolution steps."***
  A `nounif` sets the weight of matching facts to −6000 so they are not
  selected; the hypothesis then survives into the saturated clause, and ProVerif
  can end up unable to discharge it and report `cannot be proved` on a property
  that in fact holds — the manual carries a worked example of exactly that. It
  can also **fail to terminate**. It still cannot produce a false `true`, being
  covered by the same §6.6 sentence. **Neither `nounif` tried here is
  recommended, and neither is needed.**
* **`maxDepth` / `maxHyp` were not tried and are not recommended.** The manual:
  they enforce termination *"at the cost of precision"*, `maxDepth` *"makes
  clauses more general"*, `maxHyp` removes *"arbitrary hypotheses"*, and *"This
  setting is not recommended: it often causes too much imprecision."*

### Is `set selFun = Term.` an encoding recut, or something more?

**It is less than a recut, and it must be logged as one anyway.** It changes no
line of the fixture, no check, no event, no query, no companion, no probability
and no timebox; the model text outside the one added line is byte-identical, and
the control shows 47 of 47 outcomes unchanged. In kind it belongs with the
ladder's other tool-invocation decisions — `-lib`, `JOBS=3`, the timeout, the
`mem_guard` thresholds — which the owner's own script calls *"scheduling …
they change no box, model, query or prediction"*. **But it is unlike those in
one respect that matters: it changes the verification procedure itself**, so a
result obtained under it is not literally the same computation as one obtained
without it. §8 item (3) offers only two boxes, recut or amendment, and this is
plainly **not** an amendment — it touches no property, no query's shape and no
registered prediction. **So: log it in `RESULTS.md`'s "Recuts (encoding, not
property)" section**, name it in the ladder header and in every `.out` it
applies to, and state its scope exactly. The one thing that would be wrong is to
apply it **only** to the runs that died, leaving the table made under two
configurations.

---

## (e) Recommendation

**Recommended, in one move with two parts: add `set selFun = Term.` to every
capstone model file — uniformly, correct-form cases and companions alike, not
only to the eight that died — log it in `RESULTS.md`'s "Recuts (encoding, not
property)" section with the manual's soundness sentence quoted beside it, re-run
the ladder under it, and dispose whatever still fails by §3's registered order,
whose break point is now measured at step 1.** Five things carry the first
part. **(1) It lands two of the four killed companions tested with no fixture
ablation at all** — C-C5 in 40 s and 0.74 GiB where the same file without the
line dies at 9.43 GiB, and C-C7(ii) in 1355 s and 8.28 GiB where it dies at
9.44 GiB. **(2) It costs no property whatever**: the depth-2 layer, `skI2`, both
lineage shapes and the `|set| = 2` branch all stay in the model, so
`HonestChain(L2, t)`, C-C15(ii)'s middle-layer scope, C-Q6's depth-2 half and
C-C17's own mutation are all still exercised. **(3) The control says it changes
no outcome**: C-C9's full 47-query run reproduces every committed result exactly,
faster and in half the memory. **(4) Where both routes land, they agree** —
`is true` under the setting and `is true` under the ablation, on both C-C5 and
C-C7(ii). **(5) The manual forecloses the only failure mode that would matter:
no setting can make a `true` wrong.** And the second part is not a fallback
bolted on — it is what §3 already instructs (`PREDICTIONS.md:301-303`), and this report supplies the thing
§3 asks for and nobody had yet: **the break point, measured rather than
guessed, at step 1, on four companions.**

**The alternative I did NOT recommend, and why: take the registered ablation at
step 1 for all eight, and skip the setting.** It is the more *reliable* of the
two — it landed 4 of 4 where the setting landed 2 of 4, and it landed C-C14 in
81 s and C-C17 in 131 s, faster than anything else here. I do not recommend it
**as the first move** because it buys the landing by deleting the depth-2 layer,
which is the thing this model exists to compose (`RESULTS.md` R-2; §1.1's
*"depth ≤ 2"*). A companion disposed that way yields a **depth-1** result that
cannot speak to C-C15(ii), to C-Q6's depth-2 half or to C-N1's
`HonestChain(L2, t)`, and eight of the sixty-odd companion runs would then be
answering a narrower question than the rest — a difference that would have to be
carried in every cell they touch. Since the setting is free, outcome-neutral on
the control, and removes the need to ablate at least two of the eight, the
ablation should be spent only where it is actually owed. **A second alternative, and it has grown stronger
while this work ran: more memory.** The ladder was **halted at 19:10:41 UTC and
moved to ubuntu24, 96 GB** (`owner_interventions.log`, four entries at that
timestamp) — three times this machine. At 96 GB several of the eight kills may
simply not recur, and that changes the arithmetic of the recommendation but not
its direction, for three reasons. First, **no ceiling is known to suffice**:
`cap_cc17_a` was still inserting rules at **29.7 GiB** with its base **flat**
(`cap_cc17_a.out:8089-8093`) — a run that is not converging does not have a
memory requirement, it has an appetite. Second, the setting is **free and
outcome-neutral**, and it is not a smaller version of more RAM: it turned C-C5
from *"more than 10 GiB"* into **0.74 GiB and 40 seconds**, which is a change of
kind, and it will make every run on the new machine cheaper whether or not any
of them needed it. Third, **buying silence with RAM leaves §3's rule
undischarged**: §3 asks for a break point to be **recorded**, not for the
symptom to go away, and eight runs have already been disposed of as mechanism
failures without one. This report supplies it either way. **If the owner takes
only one thing from this report, it should be the break point in §(c), which is
owed to the registration regardless of what machine the ladder runs on.** **One thing I would not do:** treat any of these ablated or
re-tuned runs as property evidence. §3 is explicit that a timeout — and, by the
owner's ruling, a memory kill — is *"never about the property"*
(`PREDICTIONS.md:298-299`), and every
landing recorded here is `is true` on **one conjunct of link 2b in a file
stripped of every other query**. They say what the mechanism costs. They do not
fill a cell.

---

## (f) Amendment-shaped, stated as such and NOT taken

**F-1 — the registered ablation order cannot touch the cause it is applied to,
and that it works anyway is luck worth naming.** §3's order is four **fixture**
thinnings. §(a) says the cause is a **verifier** mutation that frees a variable
in the acceptance path — and no step in the order touches the mutation, because
a companion's mutation is what the companion **is**. The order works only by
shrinking the space the freed variable ranges over, and on the evidence here
step 1 shrinks it enough on all four companions tried. **It might not on a fifth**
(four of the eight killed runs were not tested here at all: `cap_cc07i_a`,
`cap_cc05_b`, `cap_cc06_b`, `cap_cc07i_b`), and if the order ran out, §3 has no
further step. Adding one would be an **amendment to §3's ablation rule**. Not
taken, and not needed on this evidence.

**F-2 — step 2 (`skI2`) would remove the one-signer branch's only honest
attester, and the query under ablation IS the one-signer conjunct.** §1.1 fixes
*"the one-signer manifest `M1` names `fp(pk(skI2))`, and `skI2` signs `M1` and
nothing else"*, under **ONE KEY, ONE MANIFEST**. With `skI2` gone,
`AttestStage`'s one-signer branch has no honest `OT_ATTEST` producer for `M1`;
the only other `signers0` manifests are `MW` (whose key runs `Wrapper` only, so
it produces `OT_WRAPPER` frames and fails the branch's `otA = OT_ATTEST` guard)
and the adversary's self-signed `MA` (which cannot pass strict check 1 while the
repository key is honest). **A green at step 2 could therefore be a vacuity, not
a proof** — the step would have removed the witness the query is about, and the
C-N1 witnesses that would detect it are deleted from the isolated files by the
brief's own instruction. **This is amendment-shaped** because it bears on what
§3's *"Ablation on any timeout, in order, break point recorded"*
(`PREDICTIONS.md:301-303`) means when a
step removes the ablated query's own witness: a break point reached vacuously is
not a break point. **It did not arise** — step 1 landed everywhere, so step 2 was
never run — but it would arise the moment the order had to go further, and it is
recorded now rather than discovered then. Not taken.

**F-3 — link 2b's three conjuncts are three separate `query` declarations**
(`capstone.pv:253-264`). The manual (§6.7.2, "Grouping queries") says
independent declarations *"are evaluated by rebuilding a new set of clauses from
scratch for each"*, and advises grouping *"queries that involve the same
events"* — which these three are, `AcceptanceComplete` and `SlotSatisfied` and
nothing else. Grouping them would be a **pure encoding question with identical
results**, so a **recut, not an amendment**; but it would not lower the peak of
any single conjunct's saturation, which is what kills, so it is recorded and
**not** recommended as the fix. **Not taken.**

**F-4 — a label already on the record, and it is not cosmetic.** The brief, the
owner's intervention log and the project memory all name the killer *"link
2a"*. §0 shows it is **link 2b conjunct 1** in seven of the eight runs and
**link 2b conjunct 2** in the eighth, and that **link 2a itself lands in all
eight**. §3 registers link 2a and link 2b **separately, with different
predictions, residuals and timeboxes** — link 2a green at p ≈ 0.8, 45 min
(`PREDICTIONS.md:408-410`); link 2b all three conjuncts `is true` at p ≈ 0.55,
60 min (`PREDICTIONS.md:447-457`) — so **which link a mechanism failure is
disposed under decides which registered row carries the note.** Recording it
against link 2b is a **correction of fact, not an amendment**, and any
`RESULTS.md` cell already written against link 2a needs the same correction.
**Not taken** — `RESULTS.md` is outside this scratch directory and not mine to
edit.

**F-5 — NOT amendment-shaped, and worth saying because it looks as if it might
be: the registration priced this exact failure in advance.** Link 2b's residual
reads *"0.10 timeout, concentrated here because a correspondence with a
fresh-name antecedent is the most expensive shape in the model"*
(`PREDICTIONS.md:453-456`) — the **highest** timeout residual on the ladder,
placed on **this** query, for **this** reason, before the model existed. The
mechanism failure that killed eight runs is therefore the residual the
registration itself priced, and disposing it by §3's own ablation rule needs no
amendment at all. The same row also names, inside its **0.35 recut** residual,
*"the `SlotSatisfied` projection or an `AcceptanceComplete` arity change"* — so
if the owner ever wants an encoding route rather than an ablation or a setting,
the registration has pre-named one. **I did not test it and do not recommend it
blind:** an arity change to `AcceptanceComplete` would alter the text of a
registered query, and whether the row's own words license that as a recut, or
whether §8(3)'s *"a recut of … a query's shape … is an amendment"* governs, is
the author's call and not the builder's. **Not taken.**

---

## Everything in this directory

Experiment inputs and outputs are all here. `abl.log` is the per-run record;
`table.md` is generated from it by `assemble.py`, which reads every number back
out of the files this session's runner wrote rather than taking any by hand.
`mk.py` builds the isolated and ablated files (asserting that each ablation's
anchor occurs exactly once, so no ablation can silently remove more than it
names); `mkset.py` adds solver settings and `nounif` declarations and nothing
else; `run1.sh` is the only experiment runner; `chain.sh` / `chain_all.sh` run a
list strictly one at a time; `diag.sh` ran the one `verboseRules` diagnostic.
Built and deliberately **left unrun**: `E12/E123/E1234_cc07ii.pv` and
`F12/F123/F1234_cc14.pv` (ablation steps 2-4, not reached because step 1
landed), `S5_preciseActions.pv` (the default is already `false`, and `true`
raises cost), and `S4_nounif_envMat.pv` (a second `nounif`, on
`mess(envMat, ...)`, queued behind `S3_selFunTerm.pv`, which landed and
stopped its chain — after `S6` and `S9` had both shown `nounif` to be the
wrong lever here, it was not worth a slot). `manual_notes.md` holds the ProVerif manual citations. `notes_*.md` are working
drafts, superseded by this file. The 772 MB `D1_verboseRules.out` was deleted
after its histogram was taken; the histogram is quoted in §(d).

**Nothing outside this directory was created, modified or deleted**, and no
process of the owner's running ladder was touched. `git status` at the end of
this work is identical to `git status` at its start.
