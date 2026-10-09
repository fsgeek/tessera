EXPLORATORY PROBE 2026-10-04 — non-discharging; not part of any registration

# Can Tamarin find C-C2's registered case-(d) attack? Probe report

*Written 2026-10-04 by the probe agent (Claude Opus 5.5) on wam-nuc (12 cores, 31 GB); saved to disk by the
owner instance because the harness refused the agent's own write. Tamarin 1.12.0 and Maude 3.5.1 are in
`~/.local/opt` with wrappers in `~/.local/bin` (no sudo; GraphViz, used only by the GUI, is absent).
Nothing here discharges a property or changes a registered result; the VM was not touched; nothing is staged
or committed.*

## 1. Outcome

**Partly yes.** Tamarin produced traces for both of C-C2's registered case-(d) reds, but only on cut-down
models chosen by hand (slices that delete whole rules, so every trace is a valid trace of the full Tamarin
model). On the full composed model at the registered depth it ran out of memory in precomputation, before
any search — the same structural cause `abl_d` found for ProVerif.

| What | Model | Result | Wall | Peak memory |
|---|---|---|---|---|
| **C-Q3 `ReattributedA`** (set 1) | depth-0 slice, guided (`attOnly`) | **falsified**, 16 steps | 73 s | 3.9 GB |
| **C-Q3 `ReattributedB`** (set 1) | depth-0 slice, guided (`attOnly`) | **falsified**, 16 steps | 74 s | 4.0 GB |
| **Link 5** (set 1; frame-to-key judge fired) | depth-0 slice, guided (`noD`) | **falsified**, 15 steps | 321 s | 4.6 GB |
| C-Q3 A | depth-1 slice (v3 encoding), guided (`attOnly`) | falsified, 22 steps | 447 s | 19.0 GB |
| Link 1a (where ProVerif stalled) | depth-0 slice, unguided | verified, 6 steps | 200 s | 1.9 GB |
| Any lemma | **full model (depth 2)**, unguided, every encoding | **out of memory** at 6, 8, 20 GB caps | 2–16 min | the cap |
| Precomputation only (v5) | depth 0 / 1 / 2 | 58 s, 3.2 GB / >20 GB / >20 GB | | |
| Precomputation only (v3) | depth 1 / 2 | 492 s, 9.7 GB / >20 GB in 261 s | | |
| Precomputation only, guided `attOnly` | depth 2 (v5 and v3) | >20 GB in 1–4 min | | |

**Correct-form sanity checks** (same file with `-D=CORRECT`, depth-0 slice):

| Lemma | Result | Wall | Peak memory |
|---|---|---|---|
| Link 5 | verified, 16 steps | 131 s | 2.0 GB |
| C-Q3 A / B | verified, 22 / 23 steps | 52 s each | 1.9 GB |
| A4.6 `AcceptS ⟹ IssuerSigned` | falsified, as registered, 12 steps | 101 s | 2.4 GB |
| `HonestAccepted` witness (guided `wit` slice) | reachable, 14 steps | 201 s | 6.2 GB |
| `HonestChain(L0)` witness | out of memory at 5–6 GB; not retried | — | — |

A "verified" in a slice holds for that slice only, not for the full model.

**Are the traces the registered attack?** Yes, for set (1).
- C-Q3: the leaked sole key mints authority evidence for a two-signer tuple over adversary-held keys (here
  `skS` itself). The adversary signs the honest `Attester(skB2)` frame's bytes (naming `fp(pk(skB2))`,
  `h(M2)`) under that key. With the frame pin and `mh` check removed, the frame is accepted in slot A (or B),
  so the judge sees honest bytes accepted under `pk(skS) ≠ pk(skB2)`. This is the shape of the family trace
  `m4_framepin_mh.out:608-616`, made two-signer (the capstone's mutation touches only the two-signer
  branch). No dsks step is needed.
- The depth-1 run found a second C-Q3 route that does use dsks (slot A's key `pk(dsks(sg, r))` borrowing the
  honest signature), which is the route `abl_d` §(a) describes.
- Link 5: an adversary-assembled two-signer bundle whose frame key field is not `fp(kX)`;
  `Link5Judge_kfp` fires.
- Each trace reads every one-shot private message once, so neither relies on the persistent-fact modelling
  of private channels (FIDELITY A3).

**Why the full model fails.**
- Wrapper depth multiplies the cost of Tamarin's source precomputation.
- In the depth-0 search, any honest process that signs over attacker-chosen input (`ShipIssuer`,
  `RefuseIssuer`, `ForeignIssuer` or `Wrapper`) blows up the default search on its own (shown by bisection).
- Each such signature is a candidate source for every signature goal, and with dsks it also yields an
  attacker key: Tamarin's form of `abl_d`'s width family.

## 2. Modelling effort

- About 3¼ h of agent time. Solver attempts in `runs/attempts.tsv` total about 2.7 h wall (many in
  parallel), plus about 1 h of precomputation and bisection runs.
- `cap_cc02_d.spthy`: 1221 lines, 126 rules, about 650 written by hand (`cap_cc02_d.pv` is 1155 lines).
- Four encoding revisions, each a performance change argued to preserve semantics (FIDELITY.md,
  "Encoding revisions"): v1→v2 one step per acceptance check; v2→v3 unroll the recursive wrapper
  hand-down (after a Haskell `<<loop>>` in precomputation); v3→v5 two explicit rules per signature check
  (honest key, dsks); v4 was worse and dropped.
- Not written: lemmas for the .pv's other ~40 queries (about one line each), and any review of the
  transcription.

## 3. Fidelity concerns, ranked

1. **Unreviewed hand transcription.** About 650 lines with no second reader and no mechanical cross-check.
   Before any trace is cited, someone should read `AttestCheck1_*`, `AttestTwo_*`, `A2_chk*`,
   `Link5Judge_*` and `SP3Judge_*` against the .pv.
2. **Hand-chosen guidance.** The slices were chosen by someone who already knew the expected attack shape.
   The traces are valid in the full model; Tamarin finding them unaided is not shown.
3. **Private channels as persistent facts (A3)**, which is ProVerif's own clause abstraction. The traces were
   checked by hand for double reads.
4. **Untyped, right-nested tuples (A1, A2).** These over-approximate; neither trace uses an arity or type
   confusion.
5. **Standing-path else-branches approximated on tags (A7–A10).** Irrelevant to these lemmas, but they would
   matter for C-Q6-family companions.

## 4. Implications for the other ten (an estimate)

Each companion shares the base model and needs its mutation transcribed (about 0.5 h) plus its set-(1)
lemmas.
- **Reds visible at the outer layer (L0) look tractable with guidance:** about 0.5–2 h each, minutes of
  solver time, under 10 GB. By their set-(1) relations: C-C3, C-C7(i), C-C8, C-C8-i, C-C8-ii, C-C17, and
  C-C6's C-Q7 half. Caveat: C-C3 and C-C8 use the "honest POSS signature serves every tuple" route, so their
  slice must keep the right honest signer.
- **Reds that need a wrapped layer look intractable as modelled:** C-C4, C-C5's C-Q4 part (its C-Q8 and
  link 4 events may fire at L0, since `AttestStage` is shared), C-C6's InnerSigTransplanted half, and
  possibly C-C7(ii). At depth 1 one guided lemma needed 19 GB; at depth 2 precomputation exceeded 20 GB every
  time. Source lemmas, an oracle, restructuring or a bigger machine would be needed: days per family, with
  uncertain success.
- **Total:** about 1–2 days for the six or seven L0-visible companions, including one independent review of
  the shared base. The wrapped-layer ones are open-ended. A second-tool registration or amendment would be
  needed on top (RESULTS.md §ROUTED (iii)).

**Bottom line.** For C-C2, a working Tamarin transcription took an afternoon, and the registered (d) reds
come out in about a minute each, but only with human guidance on a depth-0 slice. At the registered depth,
the composed model defeats Tamarin's precomputation for the same reason it defeats ProVerif. Tamarin is not
a drop-in replacement here. At best it gives corroboration at reduced depth, which needs its own fidelity
review.

Files: `cap_cc02_d.spthy` (and depth/guidance slices), `FIDELITY.md`, `slice.py`, `run_lemma.sh`,
`runs/attempts.tsv`, `runs/precompute.log`, `traces/`.
