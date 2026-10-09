### What I expected before running the ablations (written before the runs)

Recorded here so the results can be read against an expectation rather than
after the fact. These are the builder's expectations about a **mechanism**, not
predictions about any property, and they register nothing.

* **Ablation 1 — drop the depth-2 layer.** `capstone.pv:1079` instantiates
  `WrapStage` twice, which is what bounds depth at 2 (RESULTS.md R-2). Dropping
  the `L1 -> L2` instance removes one of the three acceptance stages the
  unpinned `checksign` payload is solved at. Expect a large but not decisive
  cut — perhaps a third to a half — because the cost is per-stage and there are
  still two stages.
* **Ablation 2 — drop `skI2`.** Expect the **largest** cut of the four, and the
  least trustworthy: `skI2` is the one-signer manifest `M1`'s only signer
  (§1.1's ONE KEY, ONE MANIFEST), and the query under diagnosis is the
  one-signer conjunct. See (f) F-2.
* **Ablation 3 — drop the second lineage shape (`RefuseIssuer`).** Expect
  **little or no** effect on this query: the standing path runs *parallel to*
  the envelope path (§1.2) and `AcceptanceComplete` / `SlotSatisfied` are
  emitted by the envelope path only. `RefuseIssuer` does also publish frames and
  signatures on `c` (`capstone.pv:430-456`), so it is not literally irrelevant,
  but its contribution is a duplicate of `ShipIssuer`'s.
* **Ablation 4 — drop the `|set| = 2` branch.** Expect a large cut: it deletes
  the branch that carries `kB`, `ppfB`, `sgB`, `fbB` and a second unpinned
  `checksign` payload at every stage. Note it is also the branch **C-C17's own
  mutation lives in**, which is why C-C17 is the wrong second companion for this
  ladder (see §(c)) and `cap_cc14_a` was chosen instead.
