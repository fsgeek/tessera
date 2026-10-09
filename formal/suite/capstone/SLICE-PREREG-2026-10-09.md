# Capstone — slice reds and the standing-key query: the pre-registration (A8.3, A8.4)

> **Status: PROPOSED.** Drafted 2026-10-09 by the AI collaborator (Claude, Opus 5.5) from
> `docs/phase-0-prereg-amendment-8.md` §A8.3 and §A8.4 (author rulings, 2026-10-09). **The author's first commit
> containing this file freezes it**, and no counted run starts before that commit. Nothing here edits
> `PREDICTIONS.md` (frozen at `3568905`), Amendment 8, a ladder-3 file or `RESULTS.md`. Revised 2026-10-09 to apply
> the required fixes (findings 1–5, 9) of the cross-family review, `proverif/dev/prereg_scratch/codex/REVIEW.md`.
> Paths are relative to `formal/suite/capstone/`. `rl:N` means `proverif/dev/slice_probe/runs.log` line N.

## 1. The claim, in ordinary language

**Claim.** Once authority is captured, the verifier still refuses three things:
- crediting an honest frame to a key the captor holds (D1, D2);
- counting an honest signer under a signer set it never joined, or filling its slot with another key (D10, D7
  membership);
- accepting bytes a signature does not cover, or an honest signature carried onto other bytes (D5, D6).

Each refusal rests on named checks. Each companion removes the check, or the combination of binding routes,
that its registration names; some attacks need several removed together (for example, the frame's manifest-hash
check and the possession-over-manifest check, C-C3). **These runs show that the composed model
then goes red in case (d) on that seam's query**, so the check is load-bearing after capture. That is the
evidence for A8.3's after-capture guarantee.

**Adversary.** Case (d): a sole authority channel whose key `skS` is public. The captor can evidence any tuple,
key or signer set. It also has `dsks`, chosen payloads, the enrolled key `skAdv` and the network. Honest issuer,
attester and wrapper keys stay secret.

**Boundary: reds only.** A slice red is a red of the full registered (d) file, by trace inclusion
(`proverif/dev/slice_probe/REPORT.md` §2; `…/codex/REVIEW.md` items 1–2). A slice shows **no green**: not the
correct model's greens (those come from the landed `capstone_d`, `proverif/ladder.log:7`), no set (2), no set-(3)
witness, no absence of out-of-set reds. The eleven (d) files stay *not run under this blob*, with slice reds
recorded beside them. §5's A8.4 runs are **unsliced**, so their greens are greens.

## 2. The slicing rule

**A slice deletes only:**
- whole top-level components of the main process's **final** parallel composition, the block opening
  `\n  ( !out(honestKeyCh`;
- every query declaration but one, each replaced by `(* query deleted by slice.py *)`.

**Never changed:** process bodies, declarations, destructors, rewrite rules (including the library's `dsks`
reductions), `set` lines, the fixture prefix, and the kept query.

**The slicer** is `proverif/dev/slice_probe/slice.py`, sha256
`6a9ee118b889a4d3af40dd397baba9151f7b2c9a51fb3c4334249c80fbb12d97`, unchanged. Its banner lines
(`EXPLORATORY PROBE … non-discharging`) are comments. Counted status comes from this page, and editing the
script would be a format change (A8.3 condition).

**The slices** (`slice.py:19-53, :73, :79-94`):
- `depth1` deletes `!WrapStage(pk(skS), L1, L2)` and `!SUnwrap(L1, L2)`, and nothing else.
- `depth0` deletes all four wrapper-descent components.
- Both keep every honest process, every judge and the standing path.
- `depth0.cone` and `depth1.cone` also delete every component whose head is not in `CONE_KEEP[query]`
  (`slice.py:33-53`).

**A red counts only with both** `RESULT … is false.` for the kept query and `A trace has been found.`
immediately before that query's own RESULT line (query-specific, not a per-file flag). Anything else is **not shown** (§8): `is true`, `cannot be proved`, a timeout, a memory kill or `rc ≠ 0`.

**Three counting conditions, fixed now.** (T), (H) and (L) are evaluated on the **same violating accepted frame**,
the one responsible for the queried failure. A wrong-half or wrong-layer trace remains an uncounted full-file red.
It does not satisfy the row, and it is no reason to skip the registered fallback.
- **(T), (H): link 5's halves.** `Link5Judge` tests `kfp` and `mh` in one pattern (`proverif/cap_cc02_d.pv:948-951`).
  A link-5 red counts for the frame-to-key half (T) only if the trace's accepted frame has `kfp ≠ fp(kX)`, and
  for the `mh` half (H) only if `mh ≠ h(t)`. Otherwise it reads *link 5 red, half not shown*, the check
  `…/codex2/REVIEW.md:176` made.
- **(L): registered wrapped-inner members, rows 12, 14 and 15.** Count only a reconstructed trace whose violating
  accepted frame is an OT_ATTEST frame at L1 or L2 reached through wrapper descent in that intake. An L0 violation
  is recorded as an additional uncounted mutation consequence. Queries and process bodies are unchanged. Letting L0
  satisfy these members would need an explicit amendment of their registered scope, not an interpretive note. These
  rows have no `depth0.cone` fallback (§3).
- **(I): row 31** shows C-C8-ii's by-construction C-Q9 red only (§6).

**Forbidden constructs** (trace inclusion is argued only without them, `REPORT.md` §2): `get … else` on tables,
`sync`, phases, restrictions/axioms/lemmas, `nounif`/`not` assumptions, equivalence queries. A hit removes that
source's rows.

**Structural audit, per counted source, recorded in `proverif/slice/AUDIT.txt` before any of its slices is
read.** This repeats `…/codex/REVIEW.md` items 1 and 6.
(1) **Identity:** `slice.py --identity SRC` prints `OK` and the source's `git hash-object` equals its §3 blob
(too weak alone, codex finding 6). (2) **Prefix byte check** (`codex/exact-prefix.py`'s check over
`proverif/slice/gen/`): every byte outside the deleted queries and the final parallel block equals the source.
(3) **Component check** (`codex/audit.py`): each kept component is an unchanged, in-order, replicated member of
the source's final composition. (4) **Construct scan** (`codex/audit.py`, comment-aware) of source and library;
the only `set` line is `set selFun = Term.`. (5) Each slice's `git hash-object` starts with its §3/§4 prefix.
Any failure removes that source's rows, never re-cut under this page. The audit is executed by
`proverif/slice/run_counted.py` (§9), before any run and again on each file's blob after its run.

## 3. The counted-run table

**Sources:** `proverif/<src>.pv` at the **ladder-3 blobs** (`proverif/ladder3-staging/DERIVATION-CHECK-L3.md`).
Their sha256 values equal those audited 2026-10-05 (`…/codex/provenance.txt`).
cc02 `221b997477a282092c8e9e2e5eec718523eee873` · cc03 `cc6f21c8928a00021820ee6f6617c8cdbe283140` ·
cc04 `a88ded5036dbfe14f9ea79ba66d5b3f22286d12a` · cc05 `897f56809be6b8e8f315a34de88d452455505525` ·
cc06 `ee1bce1be260392bea5e052d6baa52aecf566226` · cc07i `ff70204731186f62d7f5f1c5d98ed33ea7718073` ·
cc07ii `14434b6185ef96684aaecc13b883c86dc9fe4f52` · cc08 `0406e86f91951d419b9c9dfb1a506efe05f8634c` ·
cc08ii `d862bf69b234bddeed681ae1a1f1c99df71edac1` · cc17 `19b706af3d835c32355c288f23def063d3cf5676` ·
capstone_d `527ff7e35d9cda12377046295bd2c24e4bd34f92`.

**Rule against cone-too-tight greens.** Each row's **primary** is the widest slice expected to land, with every
honest process kept: `depth1` if the member is wrapped (`ScopeJudge`, `SigJudge` need `wctx`), registered at the
inner layer, or lost its producer in a cone; `depth0` otherwise. Each row also has a narrower **fallback**, registered now. **Run the fallback unless the primary has rc=0, a
reconstructed false result for the kept query, and a trace satisfying every row-specific counting condition.** Where the cone
went green in the pilot (rows 22, 33), or would delete a needed producer (rows 25, 26), the fallback is `depth0`.
For rows with a counting condition (3, 12, 14, 15, 30), the script cannot read the trace, so it always runs the
fallback and the reader applies T/H/L to each trace. A red on either slice counts only if it meets the row's
conditions. **Green on both is "not shown", never green.** For rows 12, 14 and 15 the fallback is `depth1.cone`, and
**no further fallback exists** (`depth0` variants would delete the wrapper descent that (L) requires). The pilot runs (`rl:`, 2026-10-04/05)
informed these choices and are **not counted**.

Blobs are `git hash-object` prefixes of
`slice.py proverif/<src>.pv <slice> <key> proverif/slice/gen/<src>__<slice>__<key>.pv`. "Predicted" is red for
every row. The "Registered at" column gives the `PREDICTIONS.md` line that row descends from.

| # | src | Member (query key) | Registered at | Seam | Primary (blob) | Fallback (blob) | Pilot that informed it |
|---|---|---|---|---|---|---|---|
| 1 | `cc02` | C-Q3 `ReattributedA` `cq3a` | `:1771` | D1 | `depth0` `ac503c7b846c` | `depth0.cone` `c584a5ba5ff6` | rl:22 red 98 s; rl:5 cone red (`codex/reruns.jsonl:1`) |
| 2 | `cc02` | C-Q3 `ReattributedB` `cq3b` | `:1771` | D1 | `depth0` `50c737ef874c` | `depth0.cone` `67d208fe1705` | rl:28 red 98 s; rl:4 cone red |
| 3 | `cc02` | link 5, frame-to-key half (T) `link5` | `:1771` | D1 | `depth0` `80565865a82c` | `depth0.cone` `b6e1a73cfd4b` | rl:29 red 95 s; rl:8 cone red (`codex2/reruns.jsonl:1`) |
| 4 | `cc03` | C-Q5 `SetAltered` `cq5` | `:1772` | D10 | `depth0` `6b872a344cf9` | `depth0.cone` `dc2f376b6f3f` | rl:48 cone red 2 s (`codex2/reruns.jsonl:3`) |
| 5 | `cc03` | C-Q9 `PossessionUnbound` `cq9` | `:1772` | D10 | `depth0` `584d546f423d` | `depth0.cone` `1b8d25bed5c6` | rl:49 cone red 2 s |
| 6 | `cc03` | link 3 `link3` | `:1772` | D10 | `depth0` `b72b391168ff` | `depth0.cone` `ee472558263a` | rl:50 cone red 2 s |
| 7 | `cc04` | C-Q4 `Rescoped` `cq4r` | `:1773` | D2 | `depth1` `6d983e303c83` | `depth1.cone` `53ab5342291d` | rl:53 depth1.cone red 50 s |
| 8 | `cc04` | C-Q4 `InnerSigTransplanted` `cq4s` | `:1773` | D2 | `depth1` `6032588fa662` | `depth1.cone` `ff19bb9fcb44` | rl:54 depth1.cone red 48 s |
| 9 | `cc04` | C-Q3 `ReattributedA` `cq3a` | `:1773` | D2 | `depth1` `0c408a276ff0` | `depth0.cone` `2dd8092e7f55` | rl:51 depth0.cone red 30 s |
| 10 | `cc04` | C-Q3 `ReattributedB` `cq3b` | `:1773` | D2 | `depth1` `84238b87ddac` | `depth0.cone` `479ee6bb52c5` | none; both slots' pins are removed (`diff capstone_d.pv cap_cc04_d.pv`), as in C-C2 (rl:4) |
| 11 | `cc04` | link 6b `link6b` | `:1773` | D2 | `depth1` `64e498bd11dd` | `depth1.cone` `01cd6119b7cb` | rl:55 depth1.cone red 50 s |
| 12 | `cc04` | link 5, frame-to-key half (T, L) `link5` | `:1773` | D2 | `depth1` `f38434bb632c` | `depth1.cone` `00e030c71801` | rl:52 depth0.cone red 11 s (pilot only; not a counted fallback, depth0 cannot show (L)) |
| 13 | `cc05` | C-Q4 `InnerSigTransplanted` `cq4s` | `:1774` | D5 | `depth1` `60b55de0d5f6` | `depth1.cone` `24a025091a69` | rl:58 depth1.cone red 55 s (`codex/reruns.jsonl:2`) |
| 14 | `cc05` | C-Q8 (L) `cq8` | `:1774` | D5 | `depth1` `84cc80c69f3f` | `depth1.cone` `acb4be7ab5c0` | rl:56 depth0.cone red 33 s |
| 15 | `cc05` | link 4 (L) `link4` | `:1774` | D5 | `depth1` `e72e0979bb48` | `depth1.cone` `f356100d1d83` | rl:57 depth0.cone red 33 s |
| 16 | `cc06` | C-Q7 `SigTransplanted` `cq7` | `:1775` | D5 producer; D6 | `depth0` `3618b24d162a` | `depth0.cone` `3cdfad38cc34` | rl:59 cone red 89 s |
| 17 | `cc06` | C-Q4 `InnerSigTransplanted` `cq4s` | `:1775` | D5 | `depth1` `3024bc7ad1a4` | `depth1.cone` `394ea939af7e` | rl:62 depth1.cone red 476 s, 1.2 GB |
| 18 | `cc06` | C-Q8, registered "predicted also" `cq8` | `:1775` | D6 | `depth0` `811d35231815` | `depth0.cone` `a71b2e08c523` | rl:60 cone red 89 s |
| 19 | `cc06` | link 4, registered "predicted also" `link4` | `:1775` | D6 | `depth0` `bc9507e12c98` | `depth0.cone` `86a65192582e` | rl:61 cone red 88 s |
| 20 | `cc07i` | C-Q8 `cq8` | `:1776` | D6 | `depth0` `22d8f4c8e79c` | `depth0.cone` `7cfe8ae67105` | rl:64 cone red 2 s |
| 21 | `cc07i` | link 4 `link4` | `:1776` | D6 | `depth0` `89dbf482f43c` | `depth0.cone` `cf2be810b936` | rl:65 cone red 2 s |
| 22 | `cc07i` | `AcceptedUnderHonestKey ⟹ IssuerSigned` `auhk` | `:1776` | D6 | `depth1` `27b0ecfa8921` | `depth0` `a9a7bb6802bc` | rl:90 depth0 red 5 s (`codex2/reruns.jsonl:2`); rl:63 cone **green**, too tight |
| 23 | `cc07ii` | C-Q8 `cq8` | `:1776` | D6 | `depth0` `53ca3a4979fb` | `depth0.cone` `e45ec71596f5` | rl:66 cone red 35 s |
| 24 | `cc07ii` | link 4 `link4` | `:1776` | D6 | `depth0` `3d362bb65f75` | `depth0.cone` `1df0636d3f2c` | rl:67 cone red 35 s |
| 25 | `cc07ii` | C-Q7 `SigTransplanted`, composed `cq7` | `:1776` (`cap7b…:528`) | D6 | `depth1` `92df4463a957` | `depth0` `0cdac76a5600` | none; the cone deletes `Wrapper` (`codex2/REVIEW.md:124`) |
| 26 | `cc07ii` | `AcceptedUnderHonestKey ⟹ IssuerSigned`, composed `auhk` | `:1776` (`cap7b…:1072`) | D6 | `depth1` `66b3f4820431` | `depth0` `4a661cde309d` | none; as row 25 |
| 27 | `cc08` | C-Q9 `PossessionUnbound` `cq9` | `:1777` | D10 | `depth0` `c2890fb37398` | `depth0.cone` `e5d9382f98bf` | rl:69 cone red 2 s |
| 28 | `cc08` | C-Q5 `SetAltered` `cq5` | `:1777` | D10 | `depth0` `075cb7a1798b` | `depth0.cone` `b32167506feb` | rl:68 cone red 2 s |
| 29 | `cc08` | link 3 `link3` | `:1777` | D10 | `depth0` `93775ea7d0d5` | `depth0.cone` `7bce4dff12e5` | rl:70 cone red 2 s |
| 30 | `cc08` | link 5, `mh` half (H) `link5` | `:1777` | D10 | `depth0` `a8763382be7f` | `depth0.cone` `7097a42f7ca2` | rl:71 cone red 1 s |
| 31 | `cc08ii` | C-Q9, red by construction (I) `cq9` | `:2547` | none (D10 isolation) | `depth0` `42e3a2f497ac` | `depth0.cone` `076df2a51830` | rl:72 cone red 2 s |
| 32 | `cc17` | link 2a `link2a` | `:2666` | D7 membership | `depth0` `67a063a370f1` | `depth0.cone` `6600bf9c9701` | rl:73 cone red 3 s |
| 33 | `cc17` | `SignerForged` `sf` | `:2666` | D7 membership | `depth1` `65a537177e1d` | `depth0` `3736046199cf` | rl:91 depth0 red 10 s (`codex/reruns.jsonl:3`); rl:74 cone **green**, too tight |

No primary was piloted except rows 1–3. **Not sliceable (no such capstone query):** C-C7(ii)'s honest-filtered
C-Q8 (`:1776`; the capstone has only structural `SigBytesUnbound`) and C-C17's `PossessionTransplanted` (`:2666`;
absent from `cap_cc17_d.pv`, whose SERVES line names link 2a and `SignerForged`). A8.2 G1's additions are strict-only.

## 4. Controls

The same slices of `capstone_d.pv` are run with each query used in §3. **Predicted `is true`**, except the
**A4.6** positive control `a46` (`AcceptS ⟹ IssuerSigned`). That control is registered red for the correct
degraded form (`PREDICTIONS.md:1579-1580`; `proverif/capstone_d.out:10976`). **41 controls: 39 green, 2 red.** The three added `depth1.cone` controls match the `depth1.cone` fallbacks of rows 12,
14 and 15.

| Slice | n | key `blob` |
|---|---|---|
| `depth0` | 13 | a46 `ce8425b8161c` (**red**), auhk `07167cf52c6b`, cq3a `105a5e95d929`, cq3b `247d25114b09`, cq5 `781b1177c4ec`, cq7 `19f97a91b24e`, cq8 `9d40c3b0f6cd`, cq9 `e51ea6c68581`, link2a `236a61e28c13`, link3 `aae329a35334`, link4 `9e2f5844d3ef`, link5 `1660117c6b83`, sf `4da8dc84f47a` |
| `depth0.cone` | 10 | cq3a `19d82d04a81b`, cq3b `f42baa859d77`, cq5 `1a410a82d714`, cq7 `81353a324273`, cq8 `43541baa6b13`, cq9 `d38507d9e607`, link2a `fc821c72c7e1`, link3 `d1159a6c0163`, link4 `52ada03c42fb`, link5 `500574acfeba` |
| `depth1` | 12 | a46 `22b33f7d8efb` (**red**), auhk `bf0b3fbf3f56`, cq3a `24b2b1a60956`, cq3b `bef7752c6eca`, cq4r `fd70a0fe26d6`, cq4s `e16413c160c0`, cq7 `15c794b87008`, cq8 `436d2bb37d00`, link4 `bed4edf2272d`, link5 `58959c93fa17`, link6b `250f5854fbad`, sf `098510c464ac` |
| `depth1.cone` | 6 | cq4r `096127503cb6`, cq4s `d7de55ea1401`, cq8 `6ee8f064ab2e`, link4 `da806e94002a`, link5 `af9cca859bc4`, link6b `a366ef8bde0c` |

**Pilot:** `is true` for every cone control (rl:7, :9, :10, :76-88) and for `depth0` cq3a, cq3b, link5, auhk, sf
(rl:25-27, :92, :93); `depth0` a46 red (rl:24); the rest not piloted. **Order:** controls, primaries, fallbacks, then A8.4. **The control gate:** a control red, or a provenance
mismatch, stops the batch. An unavailable or inconclusive control (timeout, memory kill, rc ≠ 0, `cannot be
proved`, or no single RESULT line) leaves the gate **incomplete**: the batch **pauses**, no primary or fallback is
run, and no result is read or counted until the author rules. The A4.6 control is red only with its reconstructed
trace. For A4.6, timeout or cannot-prove is an **inconclusive positive control**, distinct from a proved green.

## 5. A8.4's query (C-Q6k): the standing key is the key the innermost acceptance verified under

**Where the keys are** (`proverif/capstone.pv`):
- **Verified key.** It is the `kX` of `LayerAccepted(aid, lyr, t, ev, slot, kX, ppf, sg, fb)` (`:241-245`).
  `AttestStage` checks `checksign(sgA, kA)` and then emits with `kX = kA` (`:618-619`; two-signer `:657-660`).
  `slot` is `t`'s slot-A fingerprint `kfprA`.
- **Under C-C15(i)** the verified key is `kEncW`, the wrapper key: `proverif/cap_cc15i_d.pv:707-708, :745-747`;
  `cap_cc15i_a.pv:724-725, :763-765`.
- **Standing key.** It is the `kT` of `EstablishedWrapped(aid, lyr, t, kT, core, ESTABLISHED)` (`:278-279`,
  emitted `:844`). `kT = kX` (`:898`), where `kX` is the presented key from `stdMat` (`:877`), and
  `core = attemptCore(=t, =ppfI, =sgI, _)` (`:884`).
- Both paths take `aid`, `lyr`, `t` and keys from Front's one read (`:567-577`).

**No event is needed, and the standing path is untouched.** The block below is inserted immediately before
`(* ---- the REQUIRED retained queries`:
```
query aid: bitstring, lyr: bitstring, id: bitstring, kf: bitstring, ss: bitstring,
      al: bitstring, vr: bitstring, kS: pkey, ppf: bitstring, sg: bitstring,
      dcl: bitstring, ev: bitstring, kV: pkey, ppfV: bitstring, fb: bitstring;
  event(EstablishedWrapped(aid, lyr, authTuple(id, kf, ss, al, vr), kS,
          attemptCore(authTuple(id, kf, ss, al, vr), ppf, sg, dcl), ESTABLISHED))
  && event(LayerAccepted(aid, lyr, authTuple(id, kf, ss, al, vr), ev, kf, kV, ppfV, sg, fb))
  ==> kS = kV.
```
**The witness A8.4w** is the same premise with `kV` replaced by `kS` and no conclusion, as a reachability query.
It must be REACHABLE. Its full text is in the script.

**What the query joins on:** intake `aid`, layer `lyr`, tuple `t`, slot A (`slot = kf`) and the standing core's
**signature term** `sg`. Together these pin the **innermost** acceptance. Standing establishes only at the
innermost layer (BF-5, `:858-876`), and `sg = sgI` is an immutable join term (`PREDICTIONS.md:1005-1019`).

**Rejected: the `ScopeKeyOnly` observer** (`:288`). It compares the scope **report**, which C-C15(ii)
re-sources (`kEncW` on `scopeEnvelope`) while still verifying under `kA`.

**Derived files.** `proverif/a84/a84_<src>.pv` is the source with one header comment prepended, every query
replaced by a comment (`slice.py`'s regex), and the block inserted. Nothing else changes, and the sources are
untouched.
- The script is `proverif/dev/prereg_scratch/derive_a84.py`, sha256
  `de35439b35889f1475afef012b968f03e3f90cdd2b7cc4c4b9ddad3b5af92b6d`. Its block text is the registered text.
- The files were parsed and type-checked with the main process replaced by `0`, which is not a model run
  (`…/prereg_scratch/parsecheck/`).

| `a84_` + source | Case | Source blob | Derived blob | C-Q6k | A8.4w | Basis |
|---|---|---|---|---|---|---|
| `capstone` | (a) | `35d8c7020adc` | `905671ffa536` | **green** | reachable | B1 |
| `capstone_b` | (b) | `79cf13133ae8` | `6f8f6ef14402` | **green** | reachable | B1 |
| `cap_cc01_c` | (c) | `36e1b35ac4b7` | `988df7018def` | **green** | reachable | B1. (c)'s correct verifier is C-C1's file; it differs from `capstone.pv` only in the leak line and the header |
| `capstone_d` | (d) | `527ff7e35d9c` | `992d3d990ed1` | **green** | reachable | B1 |
| `cap_cc15i_a` / `_b` | (a) / (b) | `ccaba043b7b9` / `28a45fcd329d` | `b9dec2e3e1b7` / `38f5bf8f920d` | **green** | reachable | B2 |
| `cap_cc15i_d` | (d) | `93e8a663712` | `3aa19ab3c8a8` | **RED** | reachable | B3 |
| `cap_cc15ii_a` / `_b` / `_d` | (a) / (b) / (d) | `1b8faa4d5bdd` / `574f91ad3184` / `94efa8f27d24` | `2b503bd06818` / `35c8e5b60138` / `34f0d345b883` | **green** | reachable | B4 |
| `cap_cc15iii_a` / `_b` / `_d` | (a) / (b) / (d) | `f862c7513ca7` / `02443a3a4f12` / `053e3de4a5a4` | `37b2f5ad49ca` / `69c1c5836013` / `195785c16948` | **green** | reachable | B5 |

- **B1.** `kV = kA` comes from the same Front tuple as the standing `kX`: equal by construction. Corroborated by
  `ScopeMisreported` `is true` (`capstone.out:5457`, `capstone_b.out:5486`, `cap_cc01_c.out:13538`,
  `capstone_d.out:10351`), which any two-key premise instance would fire; co-occurrence by
  `HonestWrappedStandingAgreed` reachable (`:9804`, `:9849`, `:20834`, `:16744`).
- **B2.** Strict (i): the outer wrapper is evidenced on both channels, so `kEncW ∈ {pk(skI), pk(skW)}`; standing
  needs an honest `ShipIssuer` TLR, so `kS ∈ {pk(skI), pk(skI2)}` with `sg` made under `kS`; `checksign(sg, kEncW)`
  then forces `kEncW = kS`. Corroborated by `ScopeMisreported` `is true` (`cap_cc15i_a.out:9925`, `_b.out:9957`),
  whose scope report carries the same `kEncW` (`cap_cc15i_a.pv:747`).
- **B3.** In (d) the captor evidences a tuple naming `pk(a_20)` and signs the inner frame under the wrapper key
  `pk(a_4)`: accepted under `pk(a_4)`, established under `pk(a_20)`, same `aid`, `lyr`, `t`, slot, `sg`. **(d)
  only**, agreeing with A8.2 item 3. Pilot, not counted (the `ScopeKeyOnly` observer, another blob):
  `proverif/dev/codex/scratch/cc15i_d_keyjoin.out:3528`, `:3550`, `:3562`.
- **B4.** (ii) re-sources only the scope report. Both inner layers verify under `kA`: `AttestStage` below L2 and
  `AttestStageW` at L2 (`cap_cc15ii_d.pv:608`, `:689-777`). It is therefore as in B1.
- **B5.** (iii) moves only the identity. `ScopeKeyOnly` is `is true` (`cap_cc15iii_a.out:7809`, `_b.out:7871`,
  `_d.out:12905`).

**The witness is read in every green-predicted A8.4 file** (all but `a84_cap_cc15i_d`). Each requires a
reconstructed A8.4w reachability result (`RESULT not (premise-with-equal-keys) is false.` with its own `A trace has
been found.` before it). Traces are detected per query: the log records C-Q6k and A8.4w separately, and a file-level
flag is not used. If A8.4w is proved unreachable, the witness prediction is **falsified** and the non-vacuous green
is **withheld** pending diagnosis. If it is inconclusive, non-vacuity is **not shown**. C-Q6k's own reconstructed red
witnesses its own premise but does not satisfy the separate equal-key witness prediction. A8.4w shows one joined
instance, not non-vacuity at every depth, signer or route. C-Q6k's red under C-C15(i) in (d), with green everywhere
else, is the checked property A8.4 calls for. The derived files are also held at `proverif/slice/a84/`, byte-identical
(blobs in the table), where the runner audits and runs them.

## 6. Not counted, and why

- **C-C8-i** (`PREDICTIONS.md:2546`), all greens; **C-C8-ii**'s required C-Q5 green (only its C-Q9 red is
  sliced, row 31). Both are carried on family evidence, *not run under this blob* (A8.3); no row rests on them.
- **Every set (2) and every set (3)** of the eleven. A8.3: *"A slice result **never** descends a green, a witness
  requirement or a set (2)."* A witness a slice reaches is recorded, not counted.
- **Out-of-set failures.** Unqueried out-of-set failures are not measured; scoped out-of-set failures of kept
  queries are recorded and not counted.
- **The pilot runs** (`proverif/dev/slice_probe/`) and the reviewers' reruns of them.
- **The ladder-2 partial `RESULT` lines.** A8.3 does not rule on them.

## 7. Machine and boxes

**Machine:** wam-nuc, 31 GB RAM, no VM. ProVerif 2.05, sha256
`ff1dff7a9819e3efd0e841deff8d2ef2a28bc18010d1775e7a20f84b5c6cf5a0`; `-lib formal/suite/lib/tessera_theory.pvl`,
sha256 `7cf45a21b8c8b8f6ae68283a0407cbf4da047b8a9d4a120089b0612e325fa993`; each file's own `set` line.

**Boxes, per run**, enforced by `systemd-run --user --scope -p MemoryMax=… -p MemorySwapMax=0` and `timeout`:

| Run | MemoryMax / timeout | Basis |
|---|---|---|
| `depth0`, `depth0.cone` | **4 GB / 1800 s** | pilot peak 0.76 GB |
| `depth1`, `depth1.cone` | **8 GB / 3600 s** | pilot peak 1.25 GB |
| A8.4 files | **16 GB / 7200 s**, one at a time | the full-query (d) runs peaked at 6.2–12.4 GiB |

Concurrent slice runs: the sum of their `MemoryMax` values is at most 24 GB.

Each box's wall time is enforced as `timeout --kill-after=10s N` (10 s forced-kill grace beyond N; §9).

**Runner.** `proverif/slice/run_counted.py` (§9) replaces the pilot `run.sh`. It runs each file under the boxes
above, one log line per run in `proverif/slice/counted.log` (row id, file, blob after the run, rc, wall, peak RSS,
each query's RESULT with whether a trace was reconstructed for that query). A blob differing from the manifest
**stops the batch**. Worst case, every primary at its box: ≈ 23.5 h, plus fallbacks (rows 12, 14, 15 now at the
`depth1` box), plus ≤ 26 h for A8.4.

## 8. What would falsify the registration

- **A predicted red that is not shown on both registered slices** is reported as **not shown** for that member,
  never as green or as evidence against the guarantee. For (T) and (H), "not shown" includes a red whose half is
  not visible in the trace.
  - If **no** registered set-(1) member of a companion is shown, composed degraded severing evidence remains
    **withheld**. The existing family evidence is reported separately, and any proposed narrowing of §A3.3 is
    routed to the author for an explicit amendment. Nothing here narrows §A3.3 automatically.
  - If only some members are shown, the read note lists the **shown** and the **unshown** members, and does not
    imply complete companion discharge.
- **Any red in a green-predicted control is a defect, and it stops the batch.** By trace inclusion it would be a
  red of `capstone_d.pv`, whose landed run is green on all these queries (`proverif/ladder.log:7`). So the
  slicer, the audit or the run is wrong. No companion result is read until the cause is diagnosed and this page
  is amended.
- **A green (proved true) A4.6 control** is recorded as a slice too tight at that depth, and the rows on that slice
  are read with that caveat. It does not stop the batch. **A4.6 false requires its reconstructed trace.**
- **An unavailable or inconclusive control** (including a timeout or cannot-prove A4.6) leaves the control gate
  incomplete: the batch pauses and the results are withheld, as in §4.
- **A8.4.** A C-Q6k red in a correct-form file is a **finding against the standing path**, routed to the
  author; an unreachable A8.4w there makes that green vacuous (broken fixture). The same holds for every green-predicted
  A8.4 file: unreachable A8.4w falsifies its prediction and withholds the green; inconclusive means non-vacuity is not
  shown. C-Q6k not shown in
  `a84_cap_cc15i_d` leaves it without a severing companion, and D11's C-Q6 half stays withheld. Any other red
  is a **divergence**, recorded with its trace.
- **The registration is also void if:** a counted run starts before the freezing commit, a slice is not
  regenerated from the §3 blobs, or `slice.py`, a source or the library changes during the batch.

## 9. Runner and pre-run audit (recorded before the first counted run)

- **Script:** `proverif/slice/run_counted.py`, sha256 `2b54f1e94eaa1acdd036b93582484207a0cdf53127542edf46c9a06ba114d609` (supersedes `b3344b65…`, which Codex's narrow review found defective; repairs listed below).
- **Manifest:** `proverif/slice/MANIFEST.tsv`, sha256 `80cdfbd728dc5162eec567cf57c0ba89ccbfe3240bf5ef7e336e2830a4a0f6ba` (unchanged; now pinned in the runner and
  checked before parsing).
  One line per counted and control file: kind, row id, file, expected blob, source and its blob, slice, query, counting
  condition, expected result. 41 controls, 33 primaries, 33 fallbacks, 13 A8.4 files. The counted slice files are in
  `proverif/slice/gen/` (107, byte-identical to `dev/prereg_scratch/gen/`, with the three `depth1.cone` fallbacks and
  three controls added by the unchanged `slice.py`), the A8.4 files in `proverif/slice/a84/`.
- **Before any run** (`--audit-only`; nonzero exit on any failure): the four tool sha256 pins (§2, §5, §7); the
  manifest counts; the directory listings; the 23 source blobs; all 107 slice blobs; each slice byte-equal to `slice.py`
  output and passing ported prefix and component checks; the construct scan and the `set selFun = Term.`-only rule; each
  A8.4 file byte-equal to `derive_a84.py` output. Checked counts must be nonzero and equal the manifest counts. The audit parses the manifest once, from the bytes whose
  sha256 it verified. The `set` scan takes every `set … .` directive from comment-stripped text, whitespace-normalised
  and in order: none in the library, exactly `set selFun = Term.` in a model file (indentation is irrelevant).
- **Order and stops:** controls first. A control red or a provenance mismatch stops the batch; an inconclusive control
  pauses it with results withheld (§4). Then the primaries, then the fallbacks under §3's trigger, then A8.4. The script
  refuses to start over any existing `counted.log` (even empty) or a non-empty `out/`, and removes nothing. It takes an
  exclusive `flock` on `slice/` before testing or creating anything, creates `counted.log` with mode `x`, and holds the
  lock to exit (a second batch is refused). `--jobs` must be at least 1.
- **Provenance during the batch:** the audit freezes a map (every model blob, the library, ProVerif, `slice.py`,
  `derive_a84.py`, the manifest, every source blob, the runner). It is checked before every launch (under the launch
  lock, after memory is acquired), after every run, before the control gate closes and before completion. A mismatch
  means no launch, one shared stop, all results withheld, and the actual hashes in the log. **Limit:** these are
  boundary checks; they detect persistent changes, not a change-and-restore during a subprocess.
- **Stop and kill:** the stop state is shared by memory acquisition and launch; waiters wake on stop and launch nothing;
  a launch lock serialises the final stop check with subprocess creation; a run's memory is returned only after its
  stop decision is recorded and its process group is killed. Runs in flight at detection finish. Each run is
  `timeout --kill-after=10s N`: the hard ceiling is N + 10 s (the box N is unchanged; the 10 s is a cleanup grace).
- **A8.4 tags:** a run with `rc≠0`, a provenance mismatch or other than exactly the two expected RESULTs is tagged
  uncountable (partial RESULTs are diagnostics). A safety false without its own trace is `NOT_SHOWN`; a safety true is
  `GREEN_NONVACUOUS_ELIGIBLE` only if the witness is reachable with its own trace, else the green is withheld.
- **Validation (no ProVerif run):** `--audit-only` output, saved in `proverif/slice/AUDIT.txt`:
  `CHECKED {tool pins 4, gen dir listing 1, a84 dir listing 1, library scan 1, sources 23, slice blobs 107, slice == slice.py output 107, exact prefix 107, components 107, one kept query 107, slice construct scan 107, a84 blobs 13, a84 == derive output 13, a84 construct scan 13}`
  (plus `manifest pin 1`) then `AUDIT PASSED; runner sha256 2b54f1e9…d609 ; manifest sha256 80cdfbd7…f6ba`. A dry run
  prints the 126-line plan.
- **Repair tests** (`proverif/dev/prereg_scratch/fixcheck/`, copies only, no ProVerif): Codex's mutation suite against the
  fixed runner, 12 of 12 as required (baseline passes; blob, prefix, component, query, prohibited-slice, extra-set-slice,
  prohibited-library, extra-set-library, **indented-set library**, **control-expectation change** and **condition removal**
  all rejected, the last two by the manifest pin; blob-repinned cases are rejected by the deeper checks with the
  manifest repinned in the copy); Codex's helper probes plus new ones, 29 of 29 (including the **A8.4 rc=124** case, now
  uncountable); stop-race, launch-lock, provenance-before-launch/during-run, orphan-kill, batch-lock (in-process and
  cross-process), empty-log, `--jobs` and kill-grace tests, 32 of 32 (stub commands through a test-only argument of
  `run_one` that `--execute` never passes).
