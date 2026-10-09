### (e) draft — recommendation

**Recommended: add `set selFun = Term.` to the capstone's models — uniformly,
to every case and every companion, not only to the ones that died — log it in
`RESULTS.md`'s "Recuts (encoding, not property)" section with the manual's
soundness sentence quoted, and re-run the eight killed companions.** Four
things carry it. **(1) It lands the query that killed them**, with no fixture
ablation at all: `S3_selFunTerm.pv` rc=0, 1355 s, 8.28 GB, where the identical
file without the line is `Fatal error: out of memory` at 9.44 GB
(`E0_cc07ii_iso.out:3557`). **(2) It gives the same answer as the registration's
own remedy**: `is true` under the setting (`S3_selFunTerm.out:4362`) and
`is true` under registered ablation step 1 (`E1_cc07ii.out:3390`) — two
independent routes, one answer. **(3) It costs no property.** The depth-2 layer,
`skI2`, both lineage shapes and the `|set| = 2` branch all stay in the model, so
`HonestChain(L2, t)`, C-C15(ii)'s middle-layer scope, C-Q6's depth-2 half and
C-C17's own mutation are all still exercised; nothing in §1.1's fixture, §1.2's
seven checks, §3's queries or §4/§9's predictions moves, and the file's text
outside the one added line is byte-identical. **(4) The control says it changes
no outcome**: `cap_cc09_a` — a companion that already landed — re-run with the
line and nothing else gives **all 47 RESULT lines identical** to the committed
run (`S8_ctl_cc09_selFunTerm.pv`, rc=0, 193 s, 0.22 GB, against the committed
297 s and 0.47 GB), so on this model the setting is faster, smaller and
outcome-identical. And the manual is explicit that this class of setting *"may
result in more or fewer false attacks, but they never sacrifice soundness … when
ProVerif says that a property is satisfied, then the model really does guarantee
that property, regardless of how ProVerif has been configured"*. **What it could
still cost, stated:** `Term` drops the `Maxsize` tie-break, which the manual says
*"sometimes gives impressive speedups"*; some other query could therefore get
**slower** under it, or return `cannot be proved` where the default proves. That
is a false attack, not a false proof, and it would be visible as a changed
result — which is why the recommendation is to apply it **uniformly and re-run
everything**, so that every cell in `RESULTS.md` is made under one
configuration, rather than to sprinkle it on the runs that died.

**The alternative I did NOT recommend, and why. Taking the registered ablation
at step 1.** It works — both companions land at step 1, C-C7(ii) at 1490 s /
8.23 GB and C-C14 at **81 s / 1.51 GB** — and it is what §3 tells the builder to
do. I do not recommend it **as the disposition** because it buys the landing by
deleting the depth-2 layer, which is the thing this model exists to compose
(`RESULTS.md` R-2; §1.1's *"depth ≤ 2"*). A companion disposed that way yields a
**depth-1** result that cannot speak to C-C15(ii), to C-Q6's depth-2 half or to
C-N1's `HonestChain(L2, t)`, and eight of the sixty-odd companion runs would
then be answering a different question from the rest. **It should be kept in
reserve exactly as registered:** if the setting fails on some companion, §3's
order is the disposition and **step 1 is where it breaks** — that is now
measured, not guessed, and this report is the record of it. **A second
alternative, also not recommended as a substitute: more memory.** The author has
already decided to move the ladder to a larger machine
(`owner_interventions.log:2`). That is worth doing and is complementary, but it
is not a disposition: `cap_cc17_a` was still inserting rules at 31 GB with its
base flat (`cap_cc17_a.out:8089-8093`), so no particular ceiling is known to
suffice, whereas under `selFun = Term` the saturation visibly **converged** (the
queue fell from 18 000-25 000 to 2 076 and then to completion). Buying silence
with RAM would also leave the registration's timeout rule undischarged: §3 asks
for a break point to be **recorded**, and this report records one either way.
