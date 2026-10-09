# Degraded-wave diagnosis, case (d) — scratch report

*Filed 2026-09-29 by the owner instance (Claude Fable 5.1) verbatim from the builder's (Claude Opus 5) returned text; the builder's process could not write files. Two builder processes contributed: the first ran everything through `abl.log:45` and was killed by a Claude Code restart on 2026-09-28 (its detached chain survived and finished); the second reconstructed the first's work from the logs and ran everything from `abl.log:48` on. Every run was one at a time under a 10 GiB memory cap (`ulimit -v 10485760`), `nice 19`, and a `timeout`. Nothing outside `dev/abl_d/` and nothing remote was touched.*

**Status.** Scratch diagnosis, not a result and not adopted. Sources are the ladder-2 blobs, which every run carries with `set selFun = Term.`:
- `cap_cc02_d` e53e37fe
- `cap_cc05_d` 818e616d
- `capstone_d` 5ea1082c

These are hash-identical to the VM copies in `/home/tony/tessera-ladder-vm-backup/proverif/`. Two scripts were added:
- `run1b.sh` is `run1.sh` with the box as `BOX=`.
- `diag2.sh` is `diag.sh` with the query selector as its fourth argument.

`mk.py` gained a `witness` selector.

## 0. Corrections to the brief and the record

1. **`cc04_d` did not die on link 2b conjunct 1.** It landed conj 1 (`vm-backup/cap_cc04_d.out:14784`) and timed out on conj 2 (the `signers1`/slot-A form, `capstone_d.pv:286-289`; query header at `:14785`). The 09-28 16:35 memory note and the brief both say conj 1. `cc05_d` did die on conj 1 (`cap_cc05_d.out:7673`).
2. **Where each run was when it ended:**
   - `cc02_d`, `cc03_d`, `cc06_d`, `cc07i_d` were on link 1a (`.out:2357`, `:2351`, `:2387`, `:2387`).
   - Of the runs interrupted by the host crash, `cc07ii_d` and `cc08_d` were on link 1a.
   - `cc08i_d` had landed 1a and 2a (`:4220`, `:6090`) and was on conj 1.
3. **T2's parse error was already fixed.** The file (43298e6f) reads `pk( *k )`, and a 5-s idle parse check reached `Completing...` (abl.log:80).
4. **D0/D1 summaries were missing** from `diag_summary.log`. Recomputed from the scratchpad traces and appended, marked as recomputed.

## (a) Diagnosis

**Cause in one line:** the degraded setup lets the attacker vouch for any tuple; each failing companion removes the check that stopped a `dsks`-derived key from using a signature it didn't make.

**The mechanism in full.**
- In (d) the sole authority key `skS` is public (`capstone_d.pv:1069-1070`), so check 1 accepts any `authTuple` the attacker mints.
- That includes a two-signer tuple whose slot-B fingerprint is that of a `dsks`-derived key (`tessera_theory.pvl:110-115`).
- In the correct form such a key is still stopped. The only signature it verifies is somebody else's honest `sign((BYTES, frame), sk)`, whose frame names `fp(pk(sk))` and not the derived key. Two checks enforce this: the frame's `=fp(kX)` pin (`:608-611`) and the `=fbA` byte pin (`:619-620`).
- Each failing companion deletes exactly the check that denied the `dsks` key that borrowed signature:
  - C-C2: the frame pin and `mh`.
  - C-C4: the inner pin.
  - C-C5, C-C6, C-C7(i): the byte binding.
- The product of attacker-minted tuples × the fixture's honest `BYTES` signatures × slots × layers then forms a clause family that saturation cannot close.
- In strict (a)/(b) the second, uncompromised channel evidences only `M1`, `M2` and `MW`, so no tuple can name a `dsks` key at all.
- **The degraded delta removes the bound on tuples; the mutation removes the bound on keys. Either alone is finite; together they are not.**

**Verbose traces** (manual §6.7.2's procedure, 300 s each, `diag_summary.log`):

| trace | file / query | clauses | with a `dsks` term | of those, on `signers1` | of those, slot B = `fp(pk(dsks…))` |
|---|---|---|---|---|---|
| D0 | cc02_d, 1a | 161,643 | 137,406 (85%) | 137,175 | 103,778 |
| D3 | cc07i_d, 1a | 205,582 | 78,765 (38%) | 73,601 | 40,783 |
| D4 | cc06_d, 1a | 110,410 | 80,705 (73%) | 77,369 | 37,806 |
| D5 | cc05_d, conj 1 | 111,855 | 93,813 (84%) | 90,466 | 68,670 |
| D1 | capstone_d, 1a (landed, 23 s) | 35,046 | 206 (1%) | 79 | 0 |
| D2 | cc03_d, 1a | 196,504 | 214 (0%) | 83 | 0 |

- The most-selected literal in D0 is `attacker(fp(pk(dsks(sign((BYTES,framed…))))))` (14,387 selections). Next come `attacker(fp(pk(k_1)))` and the honest `OT_WRAPPER` BYTES signatures (12,226).
- `dsks` terms are never nested (maximum depth 1). The growth is in **width**: up to 38 / 59 / 47 distinct `dsks` terms in one clause (D0 / D3 / D4). This is a combinatorial family, not a loop.
- **C-C3 is a second route that uses no `dsks` at all.** It makes possession fingerprint-only, so an honest key's one possession signature serves every tuple naming that key, and the `mh` guards are gone. In D2, 185,204 of 196,504 clauses (94%) carry an honest `sign((POSS, fp(pk(sk))), sk)`, and 160,455 carry an `OT_WRAPPER` frame. C-C8 uses the same route.

**Why the depth-2 layer matters for C-C2 but not for C-C5.**
- C-C2 mutates the two-signer branch of **both** `AttestStage` and `WrapStage`.
- `X_cc02d_1a_wrapreverted` restores the pins in `WrapStage` only; `AttestStage` keeps the mutation. This is a diagnostic, not a registered ablation.
- On link 1a:

| run | what is present | outcome |
|---|---|---|
| X | mutation only in `AttestStage` | lands, 492 s / 1.13 GiB (abl.log:25, `.out:3505`) |
| A1 | ablation step 1 | lands, 2418 s / 2.14 GiB (abl.log:20, `:4283`) |
| A0 | mutation and depth-2 layer both present | times out, 3600 s / 6.71 GiB |

- So the multiplier is the wrapper handing a `dsks`-accepted frame's inner blob down `stageCh` to the next layer (`capstone_d.pv:708-709`, `:767-768`).
- C-C5's mutation is only in `AttestStage` (`cap_cc05_d.pv:596`, `:634-635`), which feeds no further layer. Dropping depth 2 changed nothing on its conj 1: B0 / B1 / B12 / B123 ran out of memory at 2354 / 2348 / 2774 / 2729 s. Deleting the two-signer branch lands it in 14 s, which fits D5 (96% of its `dsks` clauses are on `signers1`).

**Why C-C4 and C-C5 pass link 1a but die on a 2b conjunct.** This is the same split.
- Companions whose mutation reaches `WrapStage` **and** opens one of the two routes stall on link 1a: C-C2, C-C3, C-C6, C-C7(i), and C-C7(ii)/C-C8 among the interrupted runs.
- C-C4 (`cap_cc04_d.pv:592`, `:622-623`) and C-C5 are confined to `AttestStage`. They close 1a and 2a, whose goal is a one-variable `ChainBroken` (dev/abl2a/REPORT.md:97-110). They then die on the first goal carrying a structured `authTuple`: conj 1 for C-C5, conj 2 for C-C4.
- Exception: `cc08i_d` drops `mh` in both stages yet passed 1a, because it opens neither route.
- This is an explanation fitted to these observations. Only C-C2's half was tested directly (by X).

## (b) Every experiment

rc: 0 = landed, 124 = timeout, 134 = out of memory at the cap, 143 = SIGTERM. Steps 1–4 are the ablations of PREDICTIONS.md:301-303. Full blobs are on the `# START` lines of `abl.log`.

**First builder process (through abl.log:45)**

| file | delta | blob | rc | s | peak RSS | result | .out line |
|---|---|---|---|---|---|---|---|
| D0–D4 | cc02_d / capstone_d / cc03_d / cc07i_d / cc06_d, 1a, verbose | e021d7fc / 1abde712 / 981db40f / dd5da022 / 03a8a12a | cut at 300 s (D1 landed in 23 s) | — | — | D1 `is true` | abl.log:1-10 |
| A0_cc02d_1a | 1a only | d9a5701e | 124 | 3600 | 6.71 GiB | none (555,400 rules / base 54,402 / queue 24,674) | abl.log:17 |
| A1 (void) | step 1, overlapped A0 through a `pgrep` bug | bf063699 | 143 | 17 | — | VOID | abl.log:13-14 |
| **A1_cc02d_1a** | 1a, step 1 | bf063699 | **0** | **2418** | 2.14 GiB | `LINK_1A is true` | :4283 |
| X_cc02d_1a_wrapreverted | 1a, mutation reverted in `WrapStage` only | e4588075 | 0 | 492 | 1.13 GiB | `LINK_1A is true` | :3505 |
| B0_cc05d_c1 | conj 1 only | 8ba17b8d | 134 | 2354 | 9.44 GiB | out of memory | :4041 |
| B1 / B12 / B123 | + steps 1 / 1-2 / 1-3 | cd91edc6 / 373080a4 / a25f1099 | 134 each | 2348 / 2774 / 2729 | 9.44 GiB each | out of memory | :3750 / :3734 / :3625 |
| **B1234_cc05d_c1** | + steps 1-4 | bed3cc48 | **0** | **14** | 0.19 GiB | conj 1 `is true` | :1523 |

**Second builder process (from abl.log:48)**

| file | delta | blob | rc | s | peak RSS | result | .out line |
|---|---|---|---|---|---|---|---|
| D5 / D6 | cc05_d / capstone_d, conj 1, verbose | 4db35fa1 / c5d047e5 | cut (D6 at the 3 GB output cap) | 300 / 293 | — | none | abl.log:49-52 |
| **F1234_cc05d_all** | cc05_d, all 44 queries, steps 1-4 | 9fa436ad | **0** | 240 | 0.21 GiB | 44 lines, see (d) | :1410-8531 |
| **G1234_capd_all** | capstone_d, all 44, steps 1-4 (**ablated control**) | ac8f9cde | 0 | 55 | 0.07 GiB | 44 lines | :1376-5256 |
| **F1_cc02d_all** | cc02_d, all 44, step 1, box 7200 s | 625eacbf | **134** | 6997 | 9.40 GiB | 1a true, 2a true, then out of memory on conj 1 | :4283, :6514, :8094 |
| F1234_cc02d_all | cc02_d, all 44, steps 1-4 | e97048a7 | 0 | 54 | 0.07 GiB | 44 lines, identical to G1234 | — |
| C12_cc02d_c1 | cc02_d conj 1, steps 1-2 | 04a148f9 | 134 | 2058 | 9.44 GiB | out of memory | :3237 |
| C123_cc02d_c1 | cc02_d conj 1, steps 1-3 | 1e0c92be | 134 | 2116 | 9.44 GiB | out of memory | :3128 |
| T1 | cc02_d 1a + `set redundantHypElim = true.` | e8542d0c | 124 | 3600 | 6.65 GiB | none (553,000 / 54,249 / 24,604) | abl.log:87 |
| T2 | cc02_d 1a + `nounif k:skey; attacker(fp(pk( *k ))).` | 43298e6f | 124 | 3601 | 7.79 GiB | none (424,600 / 56,485 / **48,788**) | abl.log:90 |
| T3 | cc02_d 1a + `nounif s,r:bitstring; attacker(fp(pk(dsks( *s, *r )))).` | 6e790770 | 124 | 3600 | 5.90 GiB | none (552,400 / 46,273 / 25,614) | abl.log:93; :5122 |
| **W1_capd_witness** | capstone_d, the nine honest-flow witness queries only, step 1 | 45fa69f0 | 0 | 49 | 0.14 GiB | 8 reachable; **`HonestChain(L2)` unreachable** | :4058 |

Generated and never run: A12/A123/A1234_cc02d_1a, F12/F123_cc02d_all.

## (c) Break points, in the registered order

- **cc02_d, link 1a in isolation: step 1** (abl.log:23).
- **cc02_d, whole file: no admissible break point.**
  - At step 1, 1a and 2a land and conj 1 runs out of memory (F1).
  - Conj 1 in isolation also fails at steps 1-2 and 1-3.
  - Step 4 "lands" it, but only by deleting the mutation (see (d)).
- **cc05_d, conj 1: step 4** (abl.log:48). Steps 1 through 1-3 had no effect.

## (d) The ablated companions' full result sets

**cc05_d at steps 1-4, compared with the ablated control.** Same 44 queries, same order. Five results differ; each is red in the companion and green in the control:

| query | companion line | control line | in C-C5's set (1)? |
|---|---|---|---|
| C-Q7 `SigTransplanted` | `:2198` | `:1539` | no |
| C-Q8 `SigBytesUnbound` | `:2520` | `:1565` | yes |
| link 4 | `:3005` | `:1643` | yes |
| C-Q4 `InnerSigTransplanted` | `:3854` | `:1825` | yes |
| `AcceptedUnderHonestKey ⟹ IssuerSigned` | `:5061` | `:2359` | no |

Everything else is the same in both runs:
- Links 1a, 2a, 2b (all three forms), 3, 5, 6a and 6b are green, as are C-Q3, C-Q9, `Rescoped`, `SetAltered`, `TagConfused`, C-Q6's honest-key forms, `Stripped`, `SignerForged`, `Spliced`, `TypeConfused` and `VersionLied`.
- The registered (d) red `AcceptS ⟹ IssuerSigned` is false in both (`:4686` / `:2330`).
- **Six honest-flow witnesses are unreachable in both runs:**
  - `HonestComplete`, one-signer (`:3974` / `:1877`)
  - `HonestComplete`, two-signer (`:4034` / `:1903`)
  - `HonestChain(L1)` (`:5834` / `:2894`)
  - `HonestChain(L2)` (`:5894` / `:2920`)
  - `HonestWrappedAccepted` (`:6367` / `:3325`)
  - `HonestWrappedStandingAgreed` (`:6869` / `:3759`)

**Did C-C5's registered (d) reds go red? Yes, all three of set (1).** Set (2) stayed green.
- **Set (3) failed:** `HonestWrappedAccepted` is unreachable, and the ablated control shows it's the ablation's doing, not the mutation's.
- C-N1 says honest-flow witnesses "must survive every companion … No exception applies to this kind" (PREDICTIONS.md:1503-1510). By that rule this run is a broken fixture, not a result.
- Two reds fall outside set (1), which §4 says must be diagnosed before any reading. Not diagnosed here.

**cc02_d.**
- At step 1, only `LINK_1A is true` (`:4283`) and `LINK_2A is true` (`:6514`) landed; then out of memory (`:8094`).
- At steps 1-4 the result stream is identical to the control **by construction**. The mutation lives only in the `|set|=2` branches (`cap_cc02_d.pv:623-624`, `:719-722`). `diff G1234_capd_all.pv F1234_cc02d_all.pv` shows only the 15-line header comment.
- **Did C-C2's (d) reds (C-Q3, link 5's frame-to-key half) go red? No.** Neither run can speak to them: at step 1 the run never reached them, and at step 4 the mutation no longer exists.

## (e) Sound tactic alone, on the isolated cc02_d link 1a with no ablation

- **Baseline:** A0 times out at 3600 s / 6.71 GiB with nothing landed. Also on record: the default `selFun = TermMaxsize` (ladder 1) ran `cap_cc02_d` to rc=124 at 65,700 s / 76 GB with zero results (`ladder1/ladder.log`).
- **T1** (`redundantHypElim`): no effect. Its trajectory matches A0 to within 0.5%.
- **T2** (`nounif` on `fp(pk(*k))`): worse. The queue doubled, just as abl2a's `nounif` on the signature families did (dev/abl2a/REPORT.md:317-323).
- **T3** (`nounif` narrowed to `dsks` fingerprints): 15% smaller base and 12% less memory, but no landing.

**What these settings can and cannot do.**
- All three are sound. Manual §6.6: "never sacrifice soundness". `redundantHypElim` only replaces a clause with an equivalent one (manual extract :7617-7630).
- `nounif` "may lower the precision of ProVerif by preventing resolution steps" (§6.7.2, :8196-8198). So a `cannot be proved` under a `nounif` would not be evidence of an attack.
- Under `selFun = Term`, `nounif` weights are honoured (manual :8040-8050), so T2 and T3 did take effect. They took effect on a family that is wide rather than looping, which is the case the manual's procedure doesn't cover.

**Verdict: no sound tactic tried (four settings, counting the default) lands link 1a within the box and the 10 GiB cap.**

## (e') Recommendation for the degraded wave

**The 6 observed failures:** don't push them to step 4.
- Record them as the §3 outcome "timeout = mechanism-viability failure, evidence about the tool … never about the property".
- Attach this diagnosis and the break-point record: C-C2 has no admissible break; C-C5 breaks only at step 4, which C-N1 makes a broken fixture.
- Route the disposal question to the author, because §3 offers only ablation or a change of tactic, and neither worked here.

**The 3 crash-interrupted and 15 never-launched companions:** run them in their registered, unablated form, since ablation is registered only on an observed timeout. Use the diagnosis as a written-in-advance prediction of which will time out:
- Likely to time out: those whose mutation opens the `dsks` route or the honest-possession route. From their MUTATES lines, not run: C-C7(ii), C-C8, C-C8(ii), C-C17.
- May land as `capstone_d` did (1.8 h): the standing, type and scope mutations, C-C9 through C-C18.

**Alternative not recommended:** complete the §3 order to step 4 for every failing degraded companion and enter the ablated landings (such as F1234_cc05d's three reds) as their (d) results.
- Step 4 deletes C-C2's mutation outright.
- Steps 2+4 kill six honest-flow witnesses even in the control.
- Those runs are broken fixtures by C-N1 and cannot count as severings.

Adding memory is also not recommended: the VM gave these runs 22–49 GB for 18.25 h with nothing landed on 1a.

## (f) Amendment-shaped items, stated and not taken

1. **§3's ablation order conflicts with C-N1's no-exception rule.**
   - Step 1 alone kills exactly one honest-flow witness, `HonestChain(L2)` (W1:4058; the other eight stay reachable).
   - Steps 1-4 kill six (G1234).
   - So any ablated run is a broken fixture under C-N1 as frozen, unless the registration names ablation consequences the way it does for vocabulary witnesses (PREDICTIONS.md:1511-1524).
2. **Step 1 leaves the (d) reds of C-C2 through C-C7(i) structurally observable.**
   - Every (d) red descends from a model of depth ≤ 1: `m4_framepin_mh` and `sp2_q5_c2…` (S-P2, no wrapper); `s4_innerfp_mh` and `s1_sig_unbound` (S-P7, "nesting depth 1", header line 6); `d5d` and `d6e` (S-P1, no wrapper).
   - Step 1 keeps L0→L1.
   - It is **not** neutral wave-wide: C-C15(ii) ("at depth 2 the scope is taken from the MIDDLE layer") and C-C13(ii)'s per-depth reds need depth 2.
3. **Step 4 erases any mutation confined to the two-signer branch.** For C-C2 this is shown (F1234 ≡ G1234). For C-C16 and C-C17 it follows from their MUTATES lines (not run). An ablated landing there is green by construction.
4. **None of the six companions is a green control in (d).** Each Cases cell reads "(d) red, descended" (PREDICTIONS.md:1771-1776). An ablated all-green landing for any of them, which is exactly what F1234_cc02d is, would be a failure to reproduce a registered red, never a severing.
5. **The out-of-set reds need diagnosis first.** C-Q7 and `AcceptedUnderHonestKey ⟹ IssuerSigned` in F1234_cc05d need diagnosis under §4 before any reading.
6. **F1's box departs from the registered box.** F1 used 7200 s, not the 45-min box registered for C-C2's query.
7. **§3 has no third disposal.** A timeout that neither ablation nor a sound tactic disposes of has no registered outcome; that is the author's call.

---

**Five-line summary**
1. **Cause:** with `skS` public in (d), any tuple can be evidenced, including two-signer tuples naming `dsks`-derived keys. Each failing companion removes the pin that denied such a key a borrowed honest signature (C-C3 and C-C8 use fingerprint-only honest possession instead), and wrapper layers multiply the effect. That's 85%/84% `dsks` clauses on `signers1` in cc02 and cc05, against 1% in `capstone_d`.
2. **Break points:** cc02_d link 1a breaks at step 1 (2418 s), but its whole file doesn't (conj 1 runs out of memory at steps 1, 1-2 and 1-3), and step 4 deletes its mutation. cc05_d conj 1 breaks only at step 4; its full set lands all 44, with C-C5's three set-(1) reds, but six honest-flow witnesses are dead in the ablated control too.
3. **Sound tactic alone:** no. `redundantHypElim`, `nounif` on `fp(pk(*k))`, `nounif` on `dsks` fingerprints, and the default `TermMaxsize` (ladder 1) all time out on isolated link 1a.
4. **Recommendation:** record the 6 as §3 mechanism-viability timeouts and route their disposal to the author; run the 18 not-yet-run companions unablated, with this diagnosis as a prediction. Don't push to step 4 and don't report ablated landings as (d) results.
5. **Amendment-shaped:** §3's ablation steps conflict with C-N1 (step 1 costs `HonestChain(L2)`; steps 1-4 cost six witnesses). Step 1 keeps the six companions' (d) reds observable but breaks C-C15(ii) and C-C13(ii). Step 4 erases two-signer-only mutations. None of these companions is a green control in (d). §3 has no disposal for an undisposable timeout.
