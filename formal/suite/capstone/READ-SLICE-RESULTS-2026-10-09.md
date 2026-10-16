# Capstone — reading the slice batch and the standing-key query (A8.3, A8.4), 2026-10-09

> Read 2026-10-09 by the AI collaborator (Claude, Opus 5.5) against `SLICE-PREREG-2026-10-09.md` (frozen at
> `d379062`) and `docs/phase-0-prereg-amendment-8.md` §A8.3–A8.4. Sources: `proverif/slice/counted.log` (cited `log:N`)
> and `proverif/slice/out/` (cited `file:N`). The counting conditions (T), (H), (L) were judged by hand on each trace,
> on the violating accepted frame that causes the queried failure. No run, re-run or edit was made in reading.

## What was established

After authority capture (the authority key `skS` disclosed, honest signing keys secret), removing the registered
checks makes the composed verifier accept what it should refuse, on **30 of the 33 registered rows**. On those
rows, **the removed check, or the removed combination of binding routes, matters after capture**. Where a
companion removes several routes together, the result shows the combination matters, not that each constituent
check is independently necessary (for example, row 3, where frame-to-key and manifest-hash binding fail
together). *(Wording corrected 2026-10-09 after a review by Codex at the author's request.)* The three rows not shown are all wrapped-inner members (rows 12, 14,
15). Their traces violate at the outer layer L0, never at a wrapped layer, so they do not meet the registered
(L) condition. Separately, the standing path **can** certify a different key from the one the innermost acceptance
verified under: C-Q6k is red under C-C15(i) in case (d), and green with a reachable witness in the 12 other files.

## Per seam (counted rows; "shown" = `is false` with its own trace and every row condition met)

- **D1 (C-C2): 3 of 3 shown.** Rows 1, 2 (`cap_cc02_d__depth0__cq3a.out:2398`, `__cq3b.out:2398`). Row 3, link 5,
  satisfies **(T)**. Primary `cap_cc02_d__depth0__link5.out`: the accepted L0 frame (`:2318`), sent to the judge (`:2334`),
  has `kfp = a_3`, a fresh captor value, while `kX = pk(a_7)`. So `kfp ≠ fp(kX)` (`:2339-2340`). Fallback
  `…depth0.cone__link5.out:766, :782, :787-788` is the same (`kfp = a_2`, `kX = pk(a_6)`). In both, `mh` is also a free
  value, so the trace breaks both halves at once. (T) as registered is met; the `kfp` half is not shown in isolation.
- **D2 (C-C4): 5 of 6 shown.** Rows 7–11 (`cap_cc04_d__depth1__cq4r.out:3105`, `__cq4s:3153`, `__cq3a:2978`,
  `__cq3b:3018`, `__link6b:3067`). **Row 12 (link 5, T+L) NOT SHOWN: the frame is at L0.** Primary
  `cap_cc04_d__depth1__link5.out:2907, :2917, :2922-2923` and fallback `…depth1.cone__link5.out:1074, :1084, :1089-1090`
  both accept a captor-keyed OT_ATTEST frame at **L0/BASE**, with no wrapper descent. Its `kfp ≠ fp(kX)` holds (and `mh`
  differs too). (T) is met; (L) fails on both. This is an uncounted L0 consequence, and no further fallback exists.
- **D5 (C-C5; C-C6 as producer): 3 of 5 shown.** Row 13 (`cap_cc05_d__depth1__cq4s.out:3918`), row 16
  (`cap_cc06_d__depth0__cq7.out:2849`), row 17 (fallback, below). **Rows 14 (C-Q8, L) and 15 (link 4, L) NOT SHOWN: the
  frame is at L0.**
  - Row 14: in `cap_cc05_d__depth1__cq8.out:3682, :3692, :3697-3698` and `…depth1.cone__cq8.out:1229, :1239, :1244-1245`,
    a captor key signs unrelated bytes, and the frame is accepted at L0.
  - Row 15, primary `cap_cc05_d__depth1__link4.out:3723, :3733, :3740-3741`: the honest wrapper's (`skW`) signature over
    its OT_WRAPPER frame is accepted at **L0** for a different OT_ATTEST frame. Fallback `…depth1.cone__link4.out:1229,
    :1239, :1246-1247`: a captor key, at L0.
  - For C-C5: shown, C-Q4 `InnerSigTransplanted`; unshown, C-Q8 and link 4. This is not a complete companion discharge.
- **D6 (C-C6, C-C7(i), C-C7(ii)): 10 of 10 shown.** Rows 16, 18 (`cap_cc06_d__depth0__cq8.out:2835`), 19 (`…link4:2837`),
  20 (`cap_cc07i_d__depth0__cq8.out:2104`), 21 (`…link4:2122`), 22 (`cap_cc07i_d__depth1__auhk.out:2690`), 23
  (`cap_cc07ii_d__depth0__cq8.out:2482`), 24 (`…link4:2497`), 25 and 26 (fallbacks, below).
- **D7 membership (C-C17): 2 of 2 shown.** Row 32 (`cap_cc17_d__depth0__link2a.out:2159`), row 33
  (`cap_cc17_d__depth1__sf.out:2663`).
- **D10 (C-C3, C-C8): 7 of 7 shown.** Rows 4–6 (`cap_cc03_d__depth0__cq5.out:2201`, `__cq9:2129`, `__link3:2197`) and
  27–29 (`cap_cc08_d__depth0__cq9.out:2129`, `__cq5:2201`, `__link3:2197`). Row 30, link 5, satisfies **(H), with the
  half isolated.**
  - Primary `cap_cc08_d__depth0__link5.out:2179, :2189, :2194-2195`: the **honest issuer's** (`skI2`) frame is accepted
    at L0 under a captor-evidenced tuple whose version is `a_9`. The frame's `kfp = fp(pk(skI2)) = fp(kX)`, so the key
    half is intact, but its `mh = h(authTuple(…, verH)) ≠ h(t)`.
  - Fallback `…depth0.cone__link5.out:676, :686, :691-692`: `kfp = fp(kX)`, `mh = a_3`. Also (H).
- **D10 isolation (C-C8-ii), row 31 (I): shown.** C-Q9 only (`cap_cc08ii_d__depth0__cq9.out:2117`).
- **D11 / C-Q6 (C-C15(i)): shown.** C-Q6k is red in `a84_cap_cc15i_d` (below).

**Unconditioned rows.** Every `RESULT` line cited above reads `is false.`, and the line before it in the same out file
is `A trace has been found.` (checked in the out files, not only the log). **Three timeouts** occurred, each `rc=124`
at the 3600 s box with no `RESULT` line. Each was then shown by its registered fallback:
- row 17 (`log:110`, 4.9 GB) by `depth1.cone`, `cap_cc06_d__depth1.cone__cq4s.out:1886`;
- row 25 (`log:118`) by `depth0`, `cap_cc07ii_d__depth0__cq7.out:2497`;
- row 26 (`log:119`) by `depth0`, `cap_cc07ii_d__depth0__auhk.out:2511`.

Fallbacks also ran for rows 3, 12, 14, 15 and 30. The script always runs them on conditioned rows.

## The controls

The gate closed (`log:85`): **41 controls, 39 `is true`, 2 red as registered.** The A4.6 positive control is red with
its own trace at both depths: `capstone_d__depth0__a46.out:2067` and `__depth1__a46.out:2437`. So neither slice
depth is too tight for it. No green-predicted control went red. The provenance checks read `OK` on every line.

## C-Q6k (A8.4)

**Red in `a84_cap_cc15i_d`** (`a84_cap_cc15i_d.out:3869-3870`; its A8.4w is also reachable, `:5041-5042`).
The trace runs as follows:
- The honest issuer `skI2` signs its frame.
- From that one signature, the captor derives a key `pk(dsks(sgI, a_11))` under which the honest signature also
  verifies (the library's registered DSKS capability). Using `skS`, it evidences a wrapper tuple naming that key.
- It wraps the honest frame and signature. At **L1**, C-C15(i) verifies the inner signature under that **wrapper key**
  (`:3843`). Standing establishes at the same `aid`, L1, tuple, slot and `sg` under **`pk(skI2)`**, the key the tuple
  names (`:3865`). Standing key ≠ verified key.
- The prereg's B3 sketch (captor-signed inner frame, pilot) predicted the red, not this mechanism.

**Greens, each with its own A8.4w witness trace** (C-Q6k `is true` line; A8.4w trace and `is false`):
`capstone` 2640; 3293-3294 · `capstone_b` 2642; 3297-3298 · `cap_cc01_c` 3369; 4342-4343 · `capstone_d` 3184;
4063-4064 · `cap_cc15i_a` 2883; 3510-3511 · `cap_cc15i_b` 2884; 3512-3513 · `cap_cc15ii_a` 2956; 3612-3613 ·
`cap_cc15ii_b` 2957; 3614-3615 · `cap_cc15ii_d` 3491; 4378-4379 · `cap_cc15iii_a` 2966; 3633-3634 · `cap_cc15iii_b`
2969; 3639-3640 · `cap_cc15iii_d` 3504; 4405-4406 (all `a84_<src>.out`). No `cannot be proved` appears in any of them.
All 12 greens are non-vacuous, and no correct-form file is red.

## What was not shown, and the registered residuals

- **Not shown: rows 12, 14, 15.** Each has a counted-form red only at L0. (L) holds on neither registered slice, and
  no further fallback exists. Letting L0 count would need an explicit amendment of their scope (§2).
- **Uncounted L0 consequences, recorded:**
  - C-C4: link 5 at L0, both halves broken.
  - C-C5: C-Q8 at L0 under a captor key; link 4 at L0, including an honest wrapper signature carried onto other bytes.
- **No query exists** for C-C7(ii)'s honest-filtered C-Q8 or for C-C17's `PossessionTransplanted`. Nothing was run
  for either.
- **Carried on family evidence**, *not run under this blob*: C-C8-i's greens and C-C8-ii's required C-Q5 green. No row
  rests on them.
- **No green, set (2) or set-(3) witness descends from a slice.** The 39 green controls are a gate, not greens of the
  eleven files, which stay *not run under this blob* with these slice reds recorded beside them.
- **Row 3 is shown under (T) as registered, but its trace also breaks `mh`.** No trace isolates the `kfp` half.

## What these results do not establish

- **Temporal soundness or backdating.** That belongs to the temporal-anchor models (P5/P6, TLA+), which these runs
  do not exercise.
- **Anything beyond the stated capture model.** That model is: authority-channel credentials disclosed, honest
  signing keys secret. These results say nothing about institutional takeover in general, signing-key compromise,
  or a captor issuing new attestations.
- **Capstone closure.** The eleven (d) files remain unrun as wholes; the residuals above stand; the ten divergent
  configurations of `RESULTS.md` §2a are not re-read here.
- **Anything about V1.**
