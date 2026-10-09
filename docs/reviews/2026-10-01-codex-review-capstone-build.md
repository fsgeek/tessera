# Codex cross-family review of the built capstone (2026-10-01)

*Reviewer: Codex CLI 0.155.1, model gpt-6-astra (session 01a0f882-2e50-7071-b5a7-7aae800246f6), run by the owner instance with `codex exec --dangerously-bypass-approvals-and-sandbox`. Prompt: `formal/suite/capstone/proverif/dev/codex/prompt-build-round1.md`. Full transcript: `formal/suite/capstone/proverif/dev/codex/review-build-round1.out`. The reviewer's scratch models are in `/tmp/tessera-cross-family-20261001/` (not in the repo). Its final message follows verbatim. Dispositions are entered at the end by the owner instance.*

**The verdict transcription is reliable, but the capstone is not yet ready for the author’s plain-language acceptance read.** I found additional contract defects in standing-layer selection, C-C15(i)’s key join, and C-C7(i)’s mutation. The wrapped-witness repair and timebox recommendation also need correction.

I made **no repository edits**. Scratch models and outputs are in `/tmp/tessera-cross-family-20261001`.

**What I verified**

By reading and mechanical comparison:

- `PREDICTIONS.md` matches frozen commit `3568905`.
- Regenerating in `/tmp` reproduced **all 80 model files byte-for-byte**.
- The current baseline hashes to `a9fb7da1…`; removing only R-9’s comment/setting block reproduces `c6969b4c…`.
- The fresh wrapped-witness repair preserved all **47 baseline RESULT lines**. These checks are recorded at [mechanical-audit.txt:1](/tmp/tessera-cross-family-20261001/mechanical-audit.txt:1).
- I checked the mutation functions, 190 explicit verdict citations, all 66 landed companion rows’ false-result lists, and their 924 witness results. I found no polarity/count transcription error. This does **not** establish that every queried event implements its registered meaning—the findings below distinguish those questions.

The central envelope construction otherwise follows the registration: Front forwards one intake’s material independently to both paths; acceptance checks precede `LayerAccepted`; one- and two-signer branches share the layer acceptance/reporting machinery; standing does not wait for envelope success. The relevant implementation is [capstone.pv:530](/home/tony/projects/tessera/formal/suite/capstone/proverif/capstone.pv:530), [capstone.pv:576](/home/tony/projects/tessera/formal/suite/capstone/proverif/capstone.pv:576), [capstone.pv:675](/home/tony/projects/tessera/formal/suite/capstone/proverif/capstone.pv:675), and [capstone.pv:832](/home/tony/projects/tessera/formal/suite/capstone/proverif/capstone.pv:832). I found no additional fixture-key or BF-3 forwarding defect there.

**Fresh ProVerif evidence**

I ran four scratch files serially, each with this command form from the repository root:

```bash
ulimit -v 10485760
timeout 1800 proverif -lib formal/suite/lib/tessera_theory.pvl \
  /tmp/tessera-cross-family-20261001/FILE.pv \
  > /tmp/tessera-cross-family-20261001/FILE.out 2>&1
```

Every run exited `0`.

| `FILE` | Change and result |
|---|---|
| `capstone_wrapped_witness` | Baseline strict model; added `lyr <> L0`/`l <> L0` guards only to the two witness emissions. Both witnesses remain reachable at **L1**: [output:9124](/tmp/tessera-cross-family-20261001/capstone_wrapped_witness.out:9124), [RESULT:9132](/tmp/tessera-cross-family-20261001/capstone_wrapped_witness.out:9132), [output:9794](/tmp/tessera-cross-family-20261001/capstone_wrapped_witness.out:9794), [RESULT:9798](/tmp/tessera-cross-family-20261001/capstone_wrapped_witness.out:9798). All 47 verdicts match baseline. |
| `capstone_d_noninnermost` | Degraded baseline; replaced the query list with one private observer, without changing verifier checks. Standing establishes on a frame that is still a wrapper: [output:2970](/tmp/tessera-cross-family-20261001/capstone_d_noninnermost.out:2970), [RESULT:2990](/tmp/tessera-cross-family-20261001/capstone_d_noninnermost.out:2990). |
| `capstone_d_noninnermost_attest` | Strengthened that observer to require the intermediate wrapper to contain an `OT_ATTEST` frame. Trace explicitly has wrapper → wrapper → attestation, yet emits `EstablishedWrapped` at **L1**: [output:2998](/tmp/tessera-cross-family-20261001/capstone_d_noninnermost_attest.out:2998), [output:3010](/tmp/tessera-cross-family-20261001/capstone_d_noninnermost_attest.out:3010), [RESULT:3020](/tmp/tessera-cross-family-20261001/capstone_d_noninnermost_attest.out:3020). |
| `cc15i_d_keyjoin` | Repaired C-C15(i), degraded; replaced queries with the existing `ScopeKeyOnly` observer. Same intake/layer accepts under `pk(a_4)` but establishes standing under `pk(a_20)`: [output:3528](/tmp/tessera-cross-family-20261001/cc15i_d_keyjoin.out:3528), [output:3550](/tmp/tessera-cross-family-20261001/cc15i_d_keyjoin.out:3550), [RESULT:3562](/tmp/tessera-cross-family-20261001/cc15i_d_keyjoin.out:3562). |

These are **diagnostic runs**, not replacement ladder results. In particular, the witness repair was freshly tested only in baseline case (a).

**Verdict spot-checks and divergence classifications**

The following includes every current divergent companion/case combination—ten combinations containing twelve divergent query cells. `false` below is the recorded ProVerif polarity.

| Divergent cells | Recorded evidence | Assessment |
|---|---|---|
| C-C5 (a): unrestricted and honest-key authorship false | [7799](/home/tony/projects/tessera/formal/suite/capstone/proverif/cap_cc05_a.out:7799), [8270](/home/tony/projects/tessera/formal/suite/capstone/proverif/cap_cc05_a.out:8270) | G1 classification supported |
| C-C5 (b): same two false | [7591](/home/tony/projects/tessera/formal/suite/capstone/proverif/cap_cc05_b.out:7591), [8055](/home/tony/projects/tessera/formal/suite/capstone/proverif/cap_cc05_b.out:8055) | G1 supported |
| C-C17 (a), (b): unrestricted authorship false | [a:26669](/home/tony/projects/tessera/formal/suite/capstone/proverif/cap_cc17_a.out:26669), [b:26798](/home/tony/projects/tessera/formal/suite/capstone/proverif/cap_cc17_b.out:26798) | G1 supported |
| C-C10 (a), (b): unrestricted C-Q6 conjunct 1 false | [a:11500](/home/tony/projects/tessera/formal/suite/capstone/proverif/cap_cc10_a.out:11500), [b:11500](/home/tony/projects/tessera/formal/suite/capstone/proverif/cap_cc10_b.out:11500) | G2 mechanism supported |
| C-C14 (a), (b): same conjunct false | [a:37354](/home/tony/projects/tessera/formal/suite/capstone/proverif/cap_cc14_a.out:37354), [b:37502](/home/tony/projects/tessera/formal/suite/capstone/proverif/cap_cc14_b.out:37502) | G2 mechanism supported |
| C-C15(i) (a), (b): `TwoWorldsBroken` false | [a:7712](/home/tony/projects/tessera/formal/suite/capstone/proverif/cap_cc15i_a.out:7712), [b:7731](/home/tony/projects/tessera/formal/suite/capstone/proverif/cap_cc15i_b.out:7731) | G4 supported |

Additional checked cells bring this explicit sample above twenty:

| Cell(s) | Reading |
|---|---|
| Baseline link 1b; slot-B completeness | Both true: [2718](/home/tony/projects/tessera/formal/suite/capstone/proverif/capstone.out:2718), [3239](/home/tony/projects/tessera/formal/suite/capstone/proverif/capstone.out:3239) |
| Baseline C-Q8; C-Q9 | Both true: [3369](/home/tony/projects/tessera/formal/suite/capstone/proverif/capstone.out:3369), [3434](/home/tony/projects/tessera/formal/suite/capstone/proverif/capstone.out:3434) |
| Baseline C-Q6 unrestricted; conjunct 3 | Both true: [5161](/home/tony/projects/tessera/formal/suite/capstone/proverif/capstone.out:5161), [5447](/home/tony/projects/tessera/formal/suite/capstone/proverif/capstone.out:5447) |
| Degraded baseline unrestricted/honest-key authorship | False/true respectively: [10966](/home/tony/projects/tessera/formal/suite/capstone/proverif/capstone_d.out:10966), [11344](/home/tony/projects/tessera/formal/suite/capstone/proverif/capstone_d.out:11344) |
| C-C9 (d), slot-B completeness | False: [4566](/home/tony/projects/tessera/formal/suite/capstone/proverif/cap_cc09_d.out:4566) |
| C-C10 isolation (a), links 1a/1b | False/true: [2851](/home/tony/projects/tessera/formal/suite/capstone/proverif/cap_cc10iso_a.out:2851), [3000](/home/tony/projects/tessera/formal/suite/capstone/proverif/cap_cc10iso_a.out:3000) |
| C-C15(ii) (a), link 6b/scope mismatch | Both false: [4628](/home/tony/projects/tessera/formal/suite/capstone/proverif/cap_cc15ii_a.out:4628), [7580](/home/tony/projects/tessera/formal/suite/capstone/proverif/cap_cc15ii_a.out:7580) |
| C-C11-q4 (a), S2/S4 reachability | Both true, meaning **unreachable**, as the vocabulary exception permits: [11479](/home/tony/projects/tessera/formal/suite/capstone/proverif/cap_cc11q4_a.out:11479), [11870](/home/tony/projects/tessera/formal/suite/capstone/proverif/cap_cc11q4_a.out:11870) |
| C-C18 (a), tag confusion | False: [5373](/home/tony/projects/tessera/formal/suite/capstone/proverif/cap_cc18_a.out:5373) |

I agree with **G1** as omitted registered consequences of the chosen mutations, rather than baseline model defects; **G2** as confirmation of an encoded but mispredicted authority-evidence dependence; **G3** as a real reporting defect correctly repaired by BF-4; and **G4** as another omitted consequence. The supporting explanations are at [DIAGNOSIS.md:39](/home/tony/projects/tessera/formal/suite/capstone/proverif/dev/divergences/DIAGNOSIS.md:39), [57](/home/tony/projects/tessera/formal/suite/capstone/proverif/dev/divergences/DIAGNOSIS.md:57), [69](/home/tony/projects/tessera/formal/suite/capstone/proverif/dev/divergences/DIAGNOSIS.md:69), and [83](/home/tony/projects/tessera/formal/suite/capstone/proverif/dev/divergences/DIAGNOSIS.md:83).

The strict conjunct-3 contradiction is also real: the Cases cell and failed-set assignment disagree. But assigning that red to (d) alone does **not** resolve the separate immutable-key conflict demonstrated below. Thus “registration defect” is appropriate for the named prediction omissions, but insufficient as the disposition of C-C15(i)’s complete composition contract. See [DIAGNOSIS.md:89](/home/tony/projects/tessera/formal/suite/capstone/proverif/dev/divergences/DIAGNOSIS.md:89).

**R-9 assessment — NOTE**

The soundness claim is right. `selFun = Term` changes resolution selection, not the process or query definitions. The official [ProVerif 2.05 manual, §§6.6–6.7](https://bblanche.gitlabpages.inria.fr/proverif/manual.pdf) supports soundness of successful proofs under these performance settings; `cannot be proved` must remain distinct from a reconstructed attack.

I independently reproduced the cross-check classification: **49 identical result sequences, seven matching prefixes, two empty comparisons, no differences**, comparing C-C15(i)’s appropriate pre-BF-4 versions. Together with the exact baseline hash comparison, that is adequate for the limited claim that R-9 changed no **observed** verdict. It cannot establish equivalence of uncompleted runs or prove termination. That matches the qualified statement at [RESULTS.md:1625](/home/tony/projects/tessera/formal/suite/capstone/RESULTS.md:1625).

**(a) Findings**

1. **DEFECT — C-C15(i) still violates the immutable accepting-key join. Run-backed.**

   Registration defines C-Q6’s key as the actual innermost accepting key and explicitly makes `kX = kI` immutable under every companion: [PREDICTIONS.md:786](/home/tony/projects/tessera/formal/suite/capstone/PREDICTIONS.md:786), [1005](/home/tony/projects/tessera/formal/suite/capstone/PREDICTIONS.md:1005), [1019](/home/tony/projects/tessera/formal/suite/capstone/PREDICTIONS.md:1019).

   BF-4 correctly makes inner acceptance report `kEncW`, the key that actually verifies the signature: [cap_cc15i_d.pv:684](/home/tony/projects/tessera/formal/suite/capstone/proverif/cap_cc15i_d.pv:684). Standing still takes the presented key from `stdMat` and retains `kT = kX`: [cap_cc15i_d.pv:915](/home/tony/projects/tessera/formal/suite/capstone/proverif/cap_cc15i_d.pv:915), [938](/home/tony/projects/tessera/formal/suite/capstone/proverif/cap_cc15i_d.pv:938).

   The fresh trace shows different actual acceptance/standing keys for the same `aid_8,L1`, not merely different attribution labels. Therefore this companion changes more than a producer check while preserving the registered join.

   **Consequence:** C-C15(i)’s degraded C-Q6 result cannot currently certify a join-preserving severing. Resolve the contract conflict explicitly; do not repair it by making standing wait for envelope success, which E1 forbids.

2. **DEFECT — standing can establish at an intermediate wrapper instead of the innermost layer. Run-backed.**

   Registration requires the innermost layer and explicitly identifies L2 at depth two: [PREDICTIONS.md:781](/home/tony/projects/tessera/formal/suite/capstone/PREDICTIONS.md:781), [939](/home/tony/projects/tessera/formal/suite/capstone/PREDICTIONS.md:939). `StandingPath` can consume any `sStageCh` layer without requiring structural descent to finish; `EstablishedWrapped` tests only `lyr <> L0`: [capstone.pv:793](/home/tony/projects/tessera/formal/suite/capstone/proverif/capstone.pv:793), [820](/home/tony/projects/tessera/formal/suite/capstone/proverif/capstone.pv:820), [832](/home/tony/projects/tessera/formal/suite/capstone/proverif/capstone.pv:832).

   The strengthened fresh probe exhibits wrapper → wrapper → attestation but establishes at L1.

   **Consequence:** C-Q6 ranges over additional, unregistered standing reports. A green over that broader domain can be conservative; a red or witness may concern the wrong layer. This is a structural-selection defect, not a demand for standing to verify envelope signatures. The C-Q6 severing traces need to be checked after correcting the structural selection.

3. **DEFECT — C-C7(i) also accepts signed payloads that are not frames. Text-backed.**

   The registered mutation requires a signature over **some frame naming `fp(kX)`**: [PREDICTIONS.md:1776](/home/tony/projects/tessera/formal/suite/capstone/PREDICTIONS.md:1776). Its family descent explicitly destructures the signed frame: [d6e_sp1_q8all_samekey_unbound.pv:258](/home/tony/projects/tessera/formal/suite/ledger-tests-2026-09-14/d6e_sp1_q8all_samekey_unbound.pv:258).

   The derived companion instead uses `sigFrameKfp`, whose fallback returns `fp(k)` for a **non-frame** payload. The ensuing equality therefore succeeds automatically: [derive.py:248](/home/tony/projects/tessera/formal/suite/capstone/proverif/derive.py:248), [351](/home/tony/projects/tessera/formal/suite/capstone/proverif/derive.py:351).

   **Consequence:** it additionally removes the signed-frame requirement. This matters particularly when degraded evidence authorizes attacker keys. I have not shown that it changes an existing strict verdict or causes the degraded timeout; those would be stronger, unsupported claims. Restore the registered frame requirement and revalidate the affected files.

4. **DEFECT / OVERCLAIM — the wrapped witnesses are incorrectly emitted, and B-5 misclassifies the necessary repair. Run-backed.**

   Both witnesses must describe wrapped presentations: [PREDICTIONS.md:1210](/home/tony/projects/tessera/formal/suite/capstone/PREDICTIONS.md:1210), [1341](/home/tony/projects/tessera/formal/suite/capstone/PREDICTIONS.md:1341). Their emission sites currently allow L0: [capstone.pv:1046](/home/tony/projects/tessera/formal/suite/capstone/proverif/capstone.pv:1046), [1059](/home/tony/projects/tessera/formal/suite/capstone/proverif/capstone.pv:1059).

   B-5 says the existing signatures cannot show “wrapped” and proposes amendment/new query arguments: [RESULTS.md:1686](/home/tony/projects/tessera/formal/suite/capstone/RESULTS.md:1686). That necessity claim is false. Both judges already receive the layer; guarding emission fixes this aspect without changing either query signature. My full strict run demonstrates it.

   **Consequence:** the current “as registered” witness classifications at [RESULTS.md:342](/home/tony/projects/tessera/formal/suite/capstone/RESULTS.md:342) are too strong. C-N1 requires these honest-flow witnesses in **every companion**: [PREDICTIONS.md:1503](/home/tony/projects/tessera/formal/suite/capstone/PREDICTIONS.md:1503). Baseline success alone does not close that obligation. Requiring separate L1 and L2 witnesses would be an additional strengthening, not necessary merely to express “wrapped.”

5. **OVERCLAIM — P is presented as equally faithful to the frozen timebox contract. Text-backed.**

   The registration calls the entries separately timeboxed and puts conjuncts inside their entry’s box: [PREDICTIONS.md:1632](/home/tony/projects/tessera/formal/suite/capstone/PREDICTIONS.md:1632). It then expressly assigns companions their predicted-red query’s box, naming C-C17’s 45 minutes and C-C16’s 60 minutes: [PREDICTIONS.md:1867](/home/tony/projects/tessera/formal/suite/capstone/PREDICTIONS.md:1867).

   Against that, “neither reading makes any sentence false” and the recommendation’s accounting interpretation are not defensible as equivalently faithful readings: [RESULTS.md:1123](/home/tony/projects/tessera/formal/suite/capstone/RESULTS.md:1123), [1160](/home/tony/projects/tessera/formal/suite/capstone/RESULTS.md:1160). Choosing P before observing results reduces outcome-driven selection; it does not amend a frozen instruction.

   **Consequence:** accepting P should be an explicit amendment/exception with its preserved and relinquished evidence stated. The report is right to say that absent per-query timing, longer runs are **not shown inside** the smaller boxes; I do not relabel their properties false.

6. **OVERCLAIM — “neither” ablation nor tactic can dispose of the eleven failures exceeds the experiments. Text-backed.**

   The categorical sentence is at [RESULTS.md:974](/home/tony/projects/tessera/formal/suite/capstone/RESULTS.md:974). The diagnosis demonstrates failure of particular attempts, chiefly C-C2/C-C5 probes under specified limits; its own narrower conclusion is “no sound tactic **tried**”: [abl_d/REPORT.md:85](/home/tony/projects/tessera/formal/suite/capstone/proverif/dev/abl_d/REPORT.md:85), [154](/home/tony/projects/tessera/formal/suite/capstone/proverif/dev/abl_d/REPORT.md:154).

   The honest statement is that **the tested tactics did not resolve the sampled failures without unacceptable witness/mutation loss**. It is not an impossibility result for all eleven.

   The underlying operational facts are accurately disclosed: seven timeouts, four owner-guard terminations, and spare guest memory at all four guard triggers: [RESULTS.md:854](/home/tony/projects/tessera/formal/suite/capstone/RESULTS.md:854), [869](/home/tony/projects/tessera/formal/suite/capstone/RESULTS.md:869). Those are mechanism failures, not property evidence.

   The recommendation to take option (i) is honest **with its repairs read as governing**: it relinquishes composed severing for D1, D2, D5 and **all of D10’s consumer requirement**, plus degraded coverage for D6 and D7 membership. Family evidence does not become composed evidence. The proposed narrowing is expressly acknowledged at [RESULTS.md:1038](/home/tony/projects/tessera/formal/suite/capstone/RESULTS.md:1038). “Weeks” for a Tamarin follow-up remains an estimate, not a measured cost.

7. **NOTE — the existing evidence remains substantial, but conditional.**

   BF-4’s reporting correction, R-9’s soundness, and the named divergence mechanisms survive this review. The repaired D10 explanation correctly refuses to treat a producer’s own red as a failed consumer: [RESULTS.md:687](/home/tony/projects/tessera/formal/suite/capstone/RESULTS.md:687). No baseline cryptographic counterexample was established by my fresh probes. The defects concern whether the built events and companions satisfy the exact registered composition and non-vacuity contracts.

**(b) Discharge rows I agree with, and disputes**

Strictly, RESULTS itself says that **nothing is discharged by the file alone**, pending review and author adoption: [RESULTS.md:654](/home/tony/projects/tessera/formal/suite/capstone/RESULTS.md:654). I agree.

The table below gives the **observed severing evidence available for discharge**, subject to the global wrapped-witness repair. P means accepting the longer allowance by explicit disposition; Q means the registered predicted-red boxes. The underlying row/case and timing accounting is at [RESULTS.md:662](/home/tony/projects/tessera/formal/suite/capstone/RESULTS.md:662) and [RESULTS.md:1135](/home/tony/projects/tessera/formal/suite/capstone/RESULTS.md:1135).

| Row | Under P | Under Q | My agreement/dispute |
|---|---|---|---|
| D1 | None | None | Agree |
| D2 | None | None | Agree |
| D3 | (c) | Not shown inside box | Agree with observed evidence |
| D4 | (a), (b), (c), (d) | Not shown inside box | Agree; (d) supplies link 1a, not strict link 1b |
| D5 | None | None | Agree |
| D6 | (a), (b) | Not shown inside box | Recorded reds agree; C-C7(i)’s mutation needs correction before certification |
| D7 completeness | (a), (b), (d) | Same | Agree |
| D7 common content | (a), (b), (d) | (a), (b) | Agree |
| D7 membership | (a), (b) | Not shown inside box | Agree; therefore whole D7 lacks degraded discharge |
| D8 | (a), (b), (d) | (a), (b) | Agree with aggregate link-6a evidence; per-layer resolution remains the report’s disclosed limitation |
| D9 | (a), (b) | Not shown inside box | Agree |
| D10 | None | None | Agree: producer C-Q9 reds do not discharge consumer C-Q5 |
| D11 | Report claims (a), (b), (d) | Report claims (a), (b) | C-C15(ii)/(iii) link-6b evidence stands; **withhold full C-Q6 composition discharge**, especially C-C15(i)/(d), pending key-join and standing-selection resolution |
| D12 | Report claims (a), (b), (d) | Same | Recorded reds agree; **withhold final registered-scope discharge** pending innermost selection and wrapped witnesses |
| D13 | Report claims (a), (b), (d) | Same | Same qualification as D12 |

Thus the report’s matrix is substantially accurate as a **catalogue of observed producer/consumer verdicts**. It is not yet a completed discharge argument for the exact frozen contracts. Neither box choice repairs model fidelity or supplies missing witnesses.

**(c) Fitness verdict**

**Not yet fit for the author’s plain-language acceptance read.** The results preserve failures and corrections well, and the principal recorded verdicts are trustworthy. Before that read, the builder should resolve the accepting-key contradiction, make standing select the registered innermost presentation, restore C-C7(i)’s signed-frame requirement, and validate genuinely wrapped witnesses across the required files. The author’s two decisions should then be presented plainly: whether to narrow the composed-evidence requirement for the unresolved degraded runs, and whether to amend the companion time allowance. Neither decision should be asked to absorb an uncorrected implementation defect. After those repairs and scoped revalidation, the existing evidence can support a bounded symbolic-composition claim with explicit open rows; it does not yet support that claim as currently packaged.



---

## Dispositions (the owner instance, Claude Opus 5.5, 2026-10-01; clerk dispositions, not author rulings)

1. **Finding 1, C-C15(i)'s accepting-key join: ACCEPTED.** The builder determines whether the conflict is in the encoding (repairable as a broken fixture) or in the registration (C-C15(i)'s severing cannot preserve the immutable `kX = kI` join as registered at `PREDICTIONS.md:1005`, `:1019`), in which case it is routed to the author as amendment-shaped and C-C15(i)'s C-Q6 results are withheld from discharge until he rules. Standing is not made to wait for envelope success (E1).
2. **Finding 2, standing establishes at an intermediate wrapper: ACCEPTED as a defect of `capstone.pv`** (BF-5). The registered contract is the innermost layer (`PREDICTIONS.md:781`, `:939`); the repair is structural selection only, never an envelope check on the standing path.
3. **Finding 3, C-C7(i) accepts non-frame signed payloads: ACCEPTED as a broken fixture** (derive.py's `sigFrameKfp` fallback); the registered signed-frame requirement is restored and the affected files regenerated.
4. **Finding 4, the wrapped witnesses are emitted at L0: ACCEPTED as a defect of `capstone.pv`**; the emissions are guarded to wrapped layers, which needs no amendment; B-5 is withdrawn in place.
5. **Finding 5, the box reading: ACCEPTED.** The owner's recommendation of (P) is restated as a recommendation to **amend** to (P), with the evidence it preserves and the evidence it relinquishes stated; the text that called the two readings equally faithful is withdrawn in place.
6. **Finding 6, "neither disposal can": ACCEPTED.** Restated as "the tactics and ablations tried did not resolve the sampled failures without unacceptable witness or mutation loss"; it is not an impossibility result.
7. **Finding 7: noted.**

**Consequence for the ladder.** Findings 2 and 4 change `capstone.pv`, so its blob changes and every file derived from it is a different model. **Ladder 3** re-runs every file that landed in ladder 2 under the repaired model, on ubuntu24. The eleven degraded files that were mechanism failures in ladder 2 are **not** re-run: the repairs touch standing selection, witness emission and C-C7(i)'s envelope check, not the envelope saturation the degraded diagnosis located; the routed disposal (option (i)) carries them on family evidence in any case; and re-running them would cost about three days to re-observe a predicted timeout. Their cells under ladder 3 read **not run under this blob**, citing their ladder-2 mechanism failure as history, never as a ladder-3 result. After ladder 3, **one narrow Codex confirmation** checks only these repairs; it is not a second full review.
