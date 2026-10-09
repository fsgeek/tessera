EXPLORATORY PROBE 2026-10-04 — non-discharging; not part of any registration

# Do ProVerif process slices land the degraded companions' registered reds? Probe report

*Probe agent (Claude Opus 5.5) on wam-nuc, ProVerif 2.05, `-lib formal/suite/lib/tessera_theory.pvl`, each
file's own `set` lines. Runs 2026-10-04 21:46Z to 2026-10-05 (paused ~18 h on a permission prompt). Saved to
disk by the owner instance from the agent's returned text, condensed; the agent's full text is in the session
record. Nothing staged or committed; VM untouched. Per-run lines: `runs.log`.*

## 1. Outcome for C-C2 (case d)

ProVerif found all three of C-C2's registered set-(1) reds, each `is false` with "A trace has been found.",
on every slice tried. There was no "cannot be proved" anywhere. The full model, with nothing deleted and one
query kept, still timed out at 2 h (7.7 GiB, ~670 k rules, the same trajectory as `abl_d`'s A0). So
deleting processes is what makes the runs land; cutting to one query does not.

| Slice (what is deleted) | C-Q3 A | C-Q3 B | Link 5 | A4.6 control |
|---|---|---|---|---|
| `depth0.cone` (all but Front, AttestStage, the judge, Attester(skB2)) | 29 s / 329 MB | 29 s / 319 MB | 8 s / 197 MB | 12 s / 226 MB |
| `depth0.attOnly` (≈ Tamarin attOnly) | 34 s / 308 MB | 35 s / 307 MB | 34 s / 308 MB | 37 s / 357 MB |
| `depth0` (wrapper stages only; every honest process kept) | 98 s / 521 MB | 98 s / 552 MB | 95 s / 554 MB | 110 s / 576 MB |
| `depth2.cone` | 498 s / 920 MB | 491 s / 932 MB | 119 s / 577 MB | 125 s / 598 MB |
| `depth2.attOnly` | 499 s / 936 MB | 489 s / 945 MB | 421 s / 921 MB | 501 s / 982 MB |
| `none` (nothing deleted, one query; 13 GB, 2 h) | timeout 7200 s / 7.7 GiB | not run | timeout 7200 s / 7.6 GiB | not run |

**Correct-form control** (`capstone_d.pv`, same slices): C-Q3 A/B and link 5 are `is true` everywhere
(1–7 s). A4.6 is `is false` everywhere, as registered for the correct form. **Identity:** `slice.py --identity`
reproduces both sources byte for byte, and all 48 slices regenerate byte-identically.

**C-Q3 is the registered attack.** Trace at `out/cap_cc02_d__depth0.cone__cq3a.out:888-959`.
1. The honest Attester(skB2) signs its frame (naming `fp(pk(skB2))`, `h(M2)`).
2. With `skS` public, the attacker mints evidence for its own two-signer tuple over keys it holds.
3. It signs the honest frame's bytes, unchanged, under one of those keys.
4. With the pin and `mh` check removed, AttestStage accepts the frame in slot A at L0.
5. SP3Judge fires `ReattributedA`.

No dsks step is involved. This is the Tamarin shape and the family trace `m4_framepin_mh.out:600-616`, made
two-signer. **Link 5 caveat:** the .pv's judge covers `kfp` and `mh` in one pattern, so the red does not
single out the frame-to-key half; the trace leaves `kfp` free.

## 2. Soundness: a red in a slice is a red of the full model

`slice.py` deletes query declarations and whole top-level components of the main process's final parallel
composition. Nothing else is touched: no process bodies, declarations, rewrite rules, `set` lines or fixture
prefix. So the full model is `C[S | R]` and the slice is `C[S]`.

1. Any execution of `C[S]` is an execution of `C[S | R]` in which `R` stays idle. ProVerif has no
   fairness or progress obligation.
2. That execution has the same events and the same attacker knowledge.
3. Falsifying `not event(E)` or `A ==> B` is a property of a single trace.
4. ProVerif prints `is false` only with a trace reconstructed in the file's semantics.

**Can deletion add behaviour?** Checked against these files and the library.
- **`else` branches** depend only on terms and rewrite rules, which are untouched. This is why Tamarin's
  dsks-reduction removal is not mirrored here: deleting rewrite rules *would* add traces.
- **One-shot private messages:** a kept reader taking a message is also a full-model run. A sender with no
  reader blocks, which only removes traces. Every process is replicated.
- **Absent constructs that would break the argument:** `get … else` on tables, `sync`, phases,
  restrictions/axioms/lemmas, `nounif`/`not` assumptions, and equivalence queries. A future companion using
  any of them needs its own argument.

**Limits.**
- A green in a slice means nothing, and neither does a witness the slice fails to reach.
- *(Corrected 2026-10-05 per Codex `codex/REVIEW.md` finding 7.)* The same inclusion carries over any
  reconstructed red (registered or out-of-set) and any witness event actually reached. What it cannot give is
  a green, the absence of out-of-set reds, or the completeness of a companion's required results (set (2)).
  This probe established set-(1) reds only.
- The argument relies on ProVerif's trace reconstruction, which the ladder's own reds rely on too.
- Whether a slice red may stand for the registered run is for the registration to decide.

## 3. Why it works

Saturation cost is the clause width of the whole process, nearly independent of the query. Deleting
processes removes the width sources directly. Wrapper layers are the largest multiplier (C-Q3 ~100 s at
depth 0 against ~500 s at depth 2); extra honest issuers are next (~34 s against ~98 s). The full model's
blow-up appears to need the extra issuers *and* depth 2 together.

## 4. The other ten: extension beyond the brief (traces NOT yet reviewed against family traces)

Caps were 4 GB / 900 s (6 GB / 1800 s for the `depth0` reruns). Every result below is `is false` with a
trace.

| Companion | Set-(1) member(s) | Slice | Wall / RSS |
|---|---|---|---|
| C-C3 | C-Q5, C-Q9, link 3 | depth0.cone | 2 s / 85 MB each |
| C-C4 | C-Q4 Rescoped, C-Q4 InnerSigTransplanted, link 6b (wrapped) | depth1.cone | ~50 s / ~340 MB |
| C-C4 | C-Q3 A, link 5 | depth0.cone | 30 s / 11 s |
| C-C5 | C-Q4 InnerSigTransplanted (wrapped; the dsks route `abl_d` predicted) | depth1.cone | 55 s / 352 MB |
| C-C5 | C-Q8, link 4 | depth0.cone | 33 s / 370 MB |
| C-C6 | C-Q7; C-Q8 and link 4 (predicted members) | depth0.cone | ~89 s / ~0.7 GB |
| C-C6 | C-Q4 InnerSigTransplanted (wrapped) | depth1.cone | 476 s / 1.2 GB |
| C-C7(i) | C-Q8, link 4 | depth0.cone | 2 s |
| C-C7(i) | AcceptedUnderHonestKey ⟹ IssuerSigned | depth0 (the cone gave a meaningless green) | 5 s / 117 MB |
| C-C7(ii) | C-Q8, link 4 | depth0.cone | 35 s / ~546 MB |
| C-C8 | C-Q9, C-Q5, link 3; link 5 (`mh` half) | depth0.cone | 1–2 s |
| C-C8-ii | C-Q9 | depth0.cone | 2 s |
| C-C17 | link 2a | depth0.cone | 3 s |
| C-C17 | SignerForged | depth0 (the cone gave a meaningless green) | 10 s / 184 MB |

**Correct-form controls** on the same slices and queries are all `is true`.

**Not addressable by slicing:**
- C-C8-i (greens only);
- C-C8-ii's required C-Q5 green;
- C-C7(ii)'s composed C-Q7 and honest-key authorship (not run);
- every companion's set (2), set (3) and out-of-set reds.

**Failure mode.** A cone that is too tight gives a meaningless green; widen it. `depth0`/`depth1` with every
honest process kept costs only ~100 s / 0.6 GB.

**Cost to do properly (estimate):**
- ~0.5–1 h per companion to read its trace against the family trace;
- ~1 h once for an independent check of `slice.py` and §2;
- negligible machine time;
- plus a registration change saying a slice red covers set (1) only.

## 5. Files

`slice.py`, `run.sh`, `gen/` (48 C-C2 and control slices), `gen_ext/` (45 extension slices), `diffs/`,
`out/` (a banner was prepended after the runs; cited lines are post-prepend), `runs.log`.
