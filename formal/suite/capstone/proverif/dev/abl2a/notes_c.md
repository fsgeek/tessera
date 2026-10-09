### (c) draft — the break point in the registered order

**`cap_cc07ii_a` (C-C7(ii), case (a)): the break point is STEP 1 — "drop the
depth-2 layer".** Cited:

* isolated, no ablation: `E0_cc07ii_iso.pv` — rc=134, 1683 s, **9.44 GB peak**,
  **zero results**, `Fatal error: out of memory` at `E0_cc07ii_iso.out:3557`,
  the saturation having reached 209 800 rules inserted with a base of 65 760.
  **One conjunct of link 2b, on its own, exhausts 10 GB in 28 minutes** — and
  link 2b's whole registered timebox for all three conjuncts is 60 min
  (`PREDICTIONS.md:457`).
* step 1 applied: `E1_cc07ii.pv` — rc=0, **1490 s**, **8.23 GB peak**, and the
  query **lands `is true`** (`E1_cc07ii.out:3390`).
* **Steps 2, 3 and 4 were therefore not run on this companion**, which is what
  "break point recorded" means: the order stops at the first step that lands.
  The files for them are built and parse-checked (`E12_cc07ii.pv`,
  `E123_cc07ii.pv`, `E1234_cc07ii.pv`) and are left here unrun.

**What step 1 costs, stated plainly.** Dropping the `L1 -> L2` `WrapStage` and
`SUnwrap` instances bounds the model's depth at **1**, not 2. Every claim the
capstone makes *at* `L2` — §1.3's three-layer `lyr`, C-N1's `HonestChain(L2, t)`
witness, C-C15(ii)'s "middle layer rather than innermost" scope, and the whole
depth-2 half of C-Q6 — is **outside** an ablated run. That is the registered
price of step 1 and the registration names it as the price; the ablated run is
evidence about the **mechanism**, and, per §3, *"never about the property"*.

**`cap_cc14_a` (C-C14, case (a)): the break point is ALSO STEP 1, and far more
cheaply.** Cited:

* isolated, no ablation: `F0_cc14_iso.pv` — rc=134, **443 s**, **9.43 GB peak**,
  zero results, `Fatal error: out of memory` (`F0_cc14_iso.out`). C-C14 exhausts
  10 GB **four times faster** than C-C7(ii) does, which fits §(a): C-C14 unpins
  the whole five-field tuple at check 1, the earliest and widest pin in the
  path, while C-C7(ii) unpins a payload several checks later.
* step 1 applied: `F1_cc14.pv` — rc=0, **81 s**, **1.51 GB peak**, the query
  **lands `is true`** (`F1_cc14.out:2630`).

**So the break point is the same for both companions tried: step 1 of the
registered order, and nothing beyond it is needed.** Steps 2-4 were not run on
either; their files are built, parse-checked and left unrun here
(`E12/E123/E1234_cc07ii.pv`, `F12/F123/F1234_cc14.pv`).

**A caution about the two numbers.** Both landings are for **one query in a
file containing only that query**, under a **10 GB** cap that is tighter than
the owner's machine. They say the depth-2 layer is what makes this conjunct
unaffordable; they do **not** say a whole ablated companion file lands, because
the other 46 queries of a companion have their own costs — though on the
evidence of `ladder.log` those other queries were already landing before the
kill in every one of the eight runs.
