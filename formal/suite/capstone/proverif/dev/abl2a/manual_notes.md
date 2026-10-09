# ProVerif 2.05 manual, the settings that matter here
Source: https://bblanche.gitlabpages.inria.fr/proverif/manual.pdf, fetched
2026-09-20; text extracted with `pdftotext`. Line numbers below are of that
extraction (kept in this session's scratchpad, not in the repo).

* **§6.6, "Precision, performance, and termination settings" (extract :7518-7521),
  verbatim:** *"The performance settings may result in more or fewer false
  attacks, but they never sacrifice soundness. It follows that when ProVerif
  says that a property is satisfied, then the model really does guarantee that
  property, regardless of how ProVerif has been configured using the settings
  presented here."*
* **§4 (extract :3350-3354), verbatim:** *"ProVerif is sound, but not complete.
  … when ProVerif says that a property is satisfied, then the model really does
  guarantee that property. However, ProVerif is not complete; that is, ProVerif
  may not be capable of proving a property that holds."*
* **`redundancyElim` — DEFAULT IS ALREADY `best`** (extract :7613: *"By default,
  set redundancyElim = best."*). The brief's candidate `set redundancyElim =
  simple` would therefore **weaken** the current configuration, not strengthen
  it. Not run; recorded as a no-op/regression by documentation.
* **`selFun` — DEFAULT IS `TermMaxsize`** (extract :8040, :8047-8050, "(the
  default)"). The candidate `TermMaxsize` is a no-op. `Term` differs: with
  `Term`/`Nounifset` all non-special hypotheses have weight 0 instead of their
  size, so large facts are no longer preferred.
* **`redundantHypElim` — default `beginOnly`; `true` is stronger** (extract
  :7617-7630): a clause `H && H' -> C` with `σH ⊆ H'` is replaced by `H' -> C`,
  *"since there are implications in both directions between these clauses"* —
  i.e. **the replacement is an equivalence, not an approximation**. The manual:
  *"on big examples, in particular when they contain many events (or blocking
  facts), this technique can yield huge speedups."* The capstone is exactly that
  kind of example.
* **`preciseActions` — default `false`** (extract :7525-7535). `true` **raises**
  precision (fewer false attacks) at a cost; it is not a memory reducer.
* **`simplifyDerivation` — an ATTACK-RECONSTRUCTION setting** (extract
  :7760-7768, under the heading *"Attack reconstruction settings"*). The kills
  happen during saturation, before any derivation is reconstructed, so it cannot
  help. Not run.
* **`maxDepth` / `maxHyp`** (extract :7560-7582): they enforce termination *"at
  the cost of precision"*; `maxDepth` *"makes clauses more general"*, `maxHyp`
  *"arbitrary hypotheses are removed from clauses"*. Manual: *"This setting is
  not recommended: it often causes too much imprecision."*
* **`nounif` (§6.7.2)**: `nounif`/`noselect` *"adjust the selection function to
  give weight −w to facts that match F"* (extract :8160-8162) — they change
  **which literal resolution unifies upon** and nothing else about the model.
  Manual, verbatim (extract :8196-8198): ***"The nounif declarations help the
  saturation procedure to terminate but they may lower the precision of ProVerif
  by preventing resolution steps."*** A worked case where a `nounif` is the
  reason a true query is **not** provable is at extract :6431 / :8309.
* **`nounifIgnoreNtimes` — default 1** (extract :7716). It only has an effect on
  `nounif`/`noselect` declarations carrying the `ignoreAFewTimes` option, which
  in turn is only accepted with a negative weight; with no `nounif` in the file
  it does nothing. The brief's candidate `set nounifIgnoreNtimes` **alone** is
  therefore a no-op. Not run alone.
* **The manual's own procedure for choosing a `nounif`** (extract :8346-8349):
  *"one typically uses set verboseRules = true. to display the clauses generated
  by ProVerif. One can then observe the loops that occur, and one can try to
  avoid them by using a nounif declaration that prevents the selection of the
  literal that causes the loop."*
