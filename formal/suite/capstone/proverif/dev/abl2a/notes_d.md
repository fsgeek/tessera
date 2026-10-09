### (d) draft — solver settings, with no fixture ablation at all

All of these were applied to `E0_cc07ii_iso.pv` — the isolated file that **dies**
— by adding lines and changing **nothing** else (`mkset.py`). Defaults are from
the ProVerif 2.05 manual; `manual_notes.md` in this directory carries the
quotations and the extraction line numbers.

**Four of the brief's five candidates are no-ops or off-target, by the manual,
and were not run:**

| candidate | why not run |
|---|---|
| `set redundancyElim = simple` | **the default is already `best`** (manual: *"By default, set redundancyElim = best."*). The candidate would **weaken** the current configuration. |
| `set preciseActions = false` | **that IS the default.** (`preciseActions = true` would *raise* precision at a cost; the file `S5_preciseActions.pv` is built and left **unrun**.) |
| `set simplifyDerivation = false` | an **attack-reconstruction** setting (manual heading *"Attack reconstruction settings"*). The kills happen during **saturation**, before any derivation is reconstructed. |
| `set nounifIgnoreNtimes = n` | affects only `nounif`/`noselect` declarations carrying `ignoreAFewTimes`; with no such declaration in the file it does nothing. |

**What was run:**

* **`set redundantHypElim = true.`** (default `beginOnly`; chosen in place of the
  redundancy candidate because the manual promises *"huge speedups"* on *"big
  examples, in particular when they contain many events"*, which is exactly this
  model). **FAILED, AND MADE IT WORSE:** `S2_redundantHypElim.pv` rc=134,
  **974 s** to the same `Fatal error: out of memory` at 9.43 GB — against
  **1683 s** for the same file without it. The extra subsumption test costs time
  and buys no reduction: at 148 000 rules its base is 55 638, against 56 632 at
  155 000 rules unset. Not recommended.
* **`set selFun = Term.`** (default `TermMaxsize`). **THIS WORKS.**
  `S3_selFunTerm.pv` rc=0, **1355 s**, **8.28 GB peak**, and the query lands
  **`is true`** (`S3_selFunTerm.out:4362`) — **the same answer the registered
  ablation gives** (`E1_cc07ii.out:3390`). It converges rather than churning:
  at 20 min the queue had fallen to 2 076 rules and kept falling, where the
  default configuration's queue sat at 18 000-25 000 until the kill.
