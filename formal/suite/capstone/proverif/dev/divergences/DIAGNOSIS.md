# Divergence diagnosis: ladder 2, capstone.pv blob a9fb7da1 (2026-10-01)

STATUS: PROPOSED. Produced by the AI collaborator (Claude Opus 5.5, capstone builder) under PREDICTIONS.md §4's diagnosis rule. Nothing here is adopted. It edits no RESULTS.md, PREDICTIONS.md or .pv file, and it discharges nothing.

Method. For each divergent `RESULT` line I read the counterexample trace that ProVerif printed above it in the ladder-2 `.out`. I diffed every derived file against `capstone.pv` and the relevant `derive.py` function, and checked the family descent files the registration cites in `formal/suite/ledger-tests-2026-09-14/`. One class-A hypothesis was confirmed with diagnostic copies in this directory: `mk_cc15i_kw.py` produces `dv_cc15i_kw_{a,b,d}.pv`, and `dv_cc15i_kw_d_trim.pv` is the (d) copy with its query list trimmed. Each run was `ulimit -v 10 GiB; nice -n 19; timeout 1800` (`runs.log`: 234 s, 232 s and 348 s). `trace.sh FILE LINE` prints the trace steps for any RESULT line.

## Table

| Companion | Case | Query | `.out` line | The trace in one sentence | Class | Group |
|---|---|---|---|---|---|---|
| C-C5 | (a) | `Accept ⟹ IssuerSigned` | `cap_cc05_a.out:7799` | The honest wrapper skW's real signature over its own OT_WRAPPER frame is presented at L0 beside an attacker-built OT_ATTEST frame for idW/MW. Both channels' honest evidence for MW is used. The unbound byte check accepts, so `Accept(…, pk(skW), forged frame)` fires and that frame has no IssuerSigned (trace steps 47–55; trace `:7341-7799`). | C | G1 |
| C-C5 | (a) | `AcceptedUnderHonestKey ⟹ IssuerSigned` | `cap_cc05_a.out:8270` | The same acceptance; JudgeH pairs the honest key pk(skW) with the forged frame. | C | G1 |
| C-C5 | (b) | `Accept ⟹ IssuerSigned` | `cap_cc05_b.out:7591` | The same as (a), with the DNS evidence honest and the repository evidence minted. | C | G1 |
| C-C5 | (b) | `AcceptedUnderHonestKey ⟹ IssuerSigned` | `cap_cc05_b.out:8055` | The same as (a). | C | G1 |
| C-C17 | (a) | `Accept ⟹ IssuerSigned` | `cap_cc17_a.out:26669` | The honestly evidenced M2 is accepted with skI's real slot-A signature and an attacker key `pk(a_10)` in slot B, which signs its own frame and its own POSS over M2. `Accept(…, pk(a_10), fbB)` fires and has no IssuerSigned (trace `:25731-26669`). | C | G1 |
| C-C17 | (b) | `Accept ⟹ IssuerSigned` | `cap_cc17_b.out:26798` | The same; the slot-B key is `pk(a_10)`. | C | G1 |
| C-C10 | (a) | C-Q6 c1, unrestricted | `cap_cc10_a.out:11500` | The run happens entirely on the standing path. An attacker tuple naming the attacker key `pk(a_23)` carries only a minted DNS signature, and nothing checks the repository term. A self-signed TLR and a self-built anchorProof then give `EstablishedWrapped(…, pk(a_23), …)` at L1, with no Designated (trace `:10950-11500`). | B | G2 |
| C-C10 | (b) | C-Q6 c1, unrestricted | `cap_cc10_b.out:11500` | The same, with a minted repository term and nothing checking the DNS term. | B | G2 |
| C-C14 | (a) | C-Q6 c1, unrestricted | `cap_cc14_a.out:37354` | The honest repository statement `sign((STMT_DIGEST, idW), skR)` for MW and a minted DNS one are reused for the attacker tuple `authTuple(idW, fp(pk(a_23)), …)`. The standing path, checking id-only evidence, establishes the attacker key (trace `:36345-37354`). | B | G2 |
| C-C14 | (b) | C-Q6 c1, unrestricted | `cap_cc14_b.out:37502` | The same, with the channels swapped. | B | G2 |
| C-C15(i) | (a) | C-Q7 | `cap_cc15i_a.out:5436` | At L1, AttestStageW verifies skI's honest inner signature under kEncW = pk(skI), but its gsigCh report carries the presented, unchecked key `a_22`, which gives `SigTransplanted(a_22, …)`. | A | G3 |
| C-C15(i) | (a) | C-Q8 | `cap_cc15i_a.out:5991` | The bytesCh report carries presented key `a_20`; skI's signature does not verify under it. | A | G3 |
| C-C15(i) | (a) | link 4 | `cap_cc15i_a.out:7662` | The same bytesCh report, so `ChainBroken(L1, LINK_4)`. | A | G3 |
| C-C15(i) | (a) | C-Q3 `ReattributedA` | `cap_cc15i_a.out:9807` | The acceptCh report carries `a_22`, not the honest signer pk(skI), for skI's honest frame. | A | G3 |
| C-C15(i) | (a) | C-Q3 `ReattributedB` | `cap_cc15i_a.out:10405` | The same on the two-signer branch; the slot-B report key is `a_23`. | A | G3 |
| C-C15(i) | (a) | `Accept ⟹ IssuerSigned` | `cap_cc15i_a.out:13025` | `Accept(…, a_22, skI's frame)` fires and no IssuerSigned exists under `a_22`. | A | G3 |
| C-C15(i) | (a) | `AcceptedUnderHonestKey ⟹ IssuerSigned` | `cap_cc15i_a.out:13594` | The presented key is pk(skW) and the frame is skI's, so JudgeH fires under pk(skW). | A | G3 |
| C-C15(i) | (a) | C-Q2 | `cap_cc15i_a.out:9213` | Two wrapped L1 acceptances (aid_9, aid_10) carry the same unchecked evidence pair `(a_25, a_26)` with two different attacker tuples, which gives TwoWorldsBroken. No key is involved. | C | G4 |
| C-C15(i) | (b) | C-Q7, C-Q8, link 4, C-Q3 ×2, Accept, honest-key | `:5444`, `:6001`, `:7676`, `:9827`, `:10427`, `:13065`, `:13635` | The same shape as (a). I read each goal and the L1 envMat input: the reported keys are the presented `a_22`, `a_20`, `a_23` or pk(skW). | A | G3 |
| C-C15(i) | (b) | C-Q2 | `cap_cc15i_b.out:9231` | The same shape as (a): one evidence pair `(a_25, a_26)`, two tuples. | C | G4 |
| C-C15(i) | (d) | C-Q8 | `cap_cc15i_d.out:10654` | An attacker wrapper key `pk(a_3)` (minted on the sole channel) signs the inner frame, and the bytesCh report carries the presented key `a_23`. | A | G3 |
| C-C15(i) | (d) | link 4 | `cap_cc15i_d.out:12473` | The same report. | A | G3 |
| C-C15(i) | (d) | `AcceptedUnderHonestKey ⟹ IssuerSigned` | `cap_cc15i_d.out:21878` | The presented key is pk(skW); the frame was signed by `a_3`. | A | G3 |

Every one of the 29 divergent RESULT lines is in this table, and each was checked to be `is false` at the cited line.

*(REPAIR 2026-10-01, after the skeptic read `docs/reviews/2026-10-01-skeptic-read-capstone-build.md`; a gap that read did not name, found by the builder while repairing S-2.)* The C-C15(i) rows above cite the pre-BF-4 runs. Those files are now `proverif/ladder2-superseded/cap_cc15i_{a,b,d}.out`, and every C-C15(i) line number in this table and in G3/G4 below (other than the `dv_cc15i_kw_*` copies) refers to them; at the same numbers the current `cap_cc15i_*.out` files hold non-`RESULT` lines. On the repaired runs only G4's C-Q2 remains, at `cap_cc15i_a.out:7712` and `cap_cc15i_b.out:7731`.

## G1 (class C): authorship correspondences missing from C-C5's and C-C17's sets

Both companions remove the binding that makes acceptance imply that the accepting key signed those bytes. C-C5 removes "signed bytes = presented bytes", and C-C17 removes "slot-B key = the key the tuple names". The authorship correspondence therefore falls by construction under the attack each row itself registers.

C-C5's Cases cell states the attack (`PREDICTIONS.md:1774`): *"the issuer's honest wrapper signature, made under its honestly authorized key, is carried as the inner signature accompanying different, attacker-built attestation bytes"*. That is the trace, except that it takes skW (the separate honest wrapper) at L0 rather than an inner layer. L0 is in scope because the mutated AttestStage is S-P7's InnerCheck, which the base path shares. The family copy shares it the same way (`cap21d_sp7_strict_cc5_wrapped.pv:204-224`, `:211` `anyb`). So the fixture is not broken, and no excluded capability is used: skW and its Wrapper are §1.1 fixture, both channels' evidence for MW is honest, and nothing is enrolled.

The descent declares no authorship query. `cap21d`/`cap21e` declare C-Q8's judge, four S-P7 queries and two witnesses, and nothing else; the row says so itself. For C-C17, `cap18e_sp2_strict_cc17.pv` emits `IssuerSigned` (`:298`) and `Accept2S` (`:355`) but declares no correspondence (results `:513-2086`).

*(REPAIR 2026-10-01, skeptic S-6.)* That the descent declares no authorship query explains why the sets omit it; it does not make the red composition-only, and G1 does not rest on that. The S-P1 family itself shows authorship going red under byte unbinding: `d6e_sp1_q8all_samekey_unbound.out:809`, authorship `is false`, cited at `PREDICTIONS.md:1570` as *"C-C7(i)'s registered red"*. So the C-C5 red is a single-family consequence of the very binding C-C5 removes, which is why G1 is classed as a registration defect (a set omission, class C) and not as a finding.

This is the defect class that §4's round-7 rule names (*"a family copy's declared queries are not the capstone's query set"*). The same omission was already repaired once, for C-C7, by skeptic read S-4 (`PREDICTIONS.md:1776`): *"It was in no set, which under §4's replacement rule makes the builder read a registered severing as a broken fixture."* It was never carried to C-C5 or C-C17.

C-C5's honest-key red also contradicts the retained-query table (`:1570`). That table registers honest-key authorship green "all four" and names the composed exception only under C-C7(ii). C-C5's row calls its own attack *"the same-key-wrapping consequence C-C7(ii) already records, … now at the inner layer"*.

C-C17's honest-key form stays green (`cap_cc17_a.out:27241`) because the attacker's slot-B key is not honest. The unrestricted form is the SignerForged severing seen through a quantifier over every acceptance.

## G2 (class B): C-Q6 conjunct 1 (unrestricted) under the evidence-weakening companions

Both C-C10 and C-C14 traces run entirely through the standing path: Front → SUnwrap → StandingPath → StandingDecide. No envelope event occurs. The standing path does its own check 1. This is registered: the C-Q6 mapping row at `PREDICTIONS.md:1018` says the `t = tI` join is enabled by *"the evidence checks — check 1 of §1.2 …; removed by C-C10 (and subverted by C-C14)"*, and C-C14's row says *"in both the authority-channel processes and the capstone's check 1"* (`:2502`). So `derive.py`'s global replace (`_drop_ev`, `cc14`) is the registered mutation, not an excess one.

Once check 1 no longer pins the tuple, any attacker can present a tuple that names its own key. It can sign its own TLR (`fp(kT) = kfpr`, `kT = kX`), forge an `anchorProof`, and obtain ESTABLISHED for a key no honest process designated. The honest-key forms stay green in all four runs (`cap_cc10_a.out:11697`, `:11894`; `cap_cc14_a.out:38010`, `:38666`; and the same in (b)). So this is not a severing of D12. It is the standing-path analogue of the unrestricted `Accept ⟹ IssuerSigned`, which both companions already register red.

The dependence is shown without any mutation by case (c). With both channels leaked, `cap_cc01_c.out:12611` is red while `:12847` and `:13083` stay green, which is the unstated (c) red B-4 records. *(REPAIR 2026-10-01, skeptic S-6: C-Q6 is not stated for (c) and RESULTS.md reads that line nowhere; its use here is **diagnostic only**, a trace read to understand G2, not a registered reading. G2's classification does not depend on it.)* The isolation control `cap_cc10iso_a.out:5035` is green, because the honest channel's check is retained.

The single-family descents could not exhibit this. C-C10 descends from S-P1 strict copies (`cap17e`, `cap20g`), and C-C14 from the first-link spike, which declares exactly two queries. Neither has a standing path. C-C10's set (2) predicted C-Q6 green *"on the same descent"* (`:1779`), and C-C14's set (2) does not name C-Q6.

This is the consequence of composition that §4 reserves for a finding. The standing verdict's unrestricted form rests on authority evidence exactly as `Accept ⟹ IssuerSigned` does, so it inherits that query's §1.1 dependence (`:1570`: *"The (a)/(b) green depends on §1.1's reading of 'adversary-enrolled'"*).

*(REPAIR 2026-10-01, skeptic S-6. The paragraphs above say the families could not exhibit this, which is right; read as "only the composition could show it", they overstate, because the **registration** already encodes the dependence. The C-Q6 mapping row names check 1 as the check that pins the standing path's `t`, "removed by **C-C10** (and subverted by **C-C14**)" (`PREDICTIONS.md:1018`), and the unrestricted form is stated for strict cases only. The corrected statement:)* **the composition confirms a dependence the registration encoded but mis-predicted in C-C10's set (2)** (`:1779`, green "on the same descent", a descent with no standing path). The amendment-shaped route this leaves — C-Q6 conjunct 1 unrestricted into C-C10's set (1) for (a)/(b), and into C-C14's — is RESULTS.md's amendment-shaped item 5, a clerk finding not entered.

## G3 (class A): C-C15(i)'s transcription reports the presented inner key, not the wrapper key

`derive.py:cc15i` (`:605-632`) builds AttestStageW. It verifies the inner signature under kEncW, and re-keys only the scope reports (`ATTRIB_BOTH`) and `sigCh`. LayerAccepted, Accept, link2aCh, possCh, bytesCh, link5Ch, slotCh, setCh, acceptCh, acceptKeyCh, gsigCh and chainCh still carry kA or kB. After the mutation those are presented keys that no check touches (`diff capstone.pv cap_cc15i_a.pv`, `+682-771`).

The registration states the report contract the other way. It says *"the inner acceptance of this configuration reports the **presented inner** `(kW, tI, ppfI)`"* (`PREDICTIONS.md:2503`, the Cases cell). Its registered strict SignerForged route is the slot *"reported as satisfied by the **wrapper** key"*. The family descents report kW everywhere: `cap25a_sp7_strict_q6b_sigjudges.pv:331-336` has `AcceptInner(…, kW, …)`, `acceptCh`/`Report`/`pqCh`/`genericAccepted` with kW. That is where C-Q7 and C-Q8 were descended green (`cap25a:1306`, `:1317`).

Every G3 trace turns on exactly this: the inner signature verifies under pk(skI), or `pk(a_3)` in (d), while the judge sees an unrelated presented key. The derived file therefore mutates more than the registered severing.

Confirmation run. In `dv_cc15i_kw_{a,b,d}`, kEncW replaces kA/kB in AttestStageW's events and reports only, never in a check (the diff is in `mk_cc15i_kw.py`).

- **(a):** C-Q7 `:4908`, C-Q8 `:4980`, link 4 `:6164`, C-Q3 `:7784`/`:7856`, `Accept ⟹ IssuerSigned` `:10016` and honest-key authorship `:10114` all go GREEN. Every registered strict red still fires: link 1a `:3331`, link 1b `:3879`, link 2a `:4434`, C-Q9 `:5535`, link 3 `:6092`, link 5 `:6719`, C-Q5 `:8561` and SignerForged `:10745`. Every witness is still reachable (`:11410-16676`).
- **(b):** identical RESULT sets (C-Q7 `:4919`, C-Q8 `:4992`, link 4 `:6179`, C-Q3 `:7804`/`:7877`, Accept `:10049`, honest-key `:10148`, all green).
- **(d), trimmed copy:** C-Q8 `:3595`, link 4 `:3843` and honest-key authorship `:6367` go GREEN. C-Q7 `:3348` and C-Q3 `:4505`/`:5206` stay red, which (d) registers. C-Q7 takes the registered D-4 `dsks` route on a wrapper key minted on the sole channel. `AcceptS` `:5959` stays red as the (d) baseline. The witnesses are reachable at `:7033`, `:7636` and `:8381`.

## G4 (class C): C-Q2 under C-C15(i) in strict

C-Q2 stays red in the repaired copies (`dv_cc15i_kw_a.out:7712`, `dv_cc15i_kw_b.out:7731`), with the same trace: one unchecked evidence pair and two attacker tuples. So it is a consequence of the registered mutation and not of G3.

The registration's own sentence entails it: *"this mutation checks none of [the presented inner terms] … Every registered relation over the reported inner terms is therefore exposed"* (`:2503`). C-Q2 (D9's pair judge over `(evD, evR, t)`) is such a relation. Yet it is in neither set (1) nor set (2) for (i). No descent copy (`cap22e`–`cap25b`, `cap14b`) declares a C-Q2 judge, which is the round-7 class again. C-Q2 is not stated for (d), so this item exists in (a)/(b) only.

## C-C15(i) and conjunct 3: the registration contradicts itself in strict (class C; not a divergence)

Set (1) says both configurations red C-Q6 conjunct 3, with (i) reporting `(kW, idW) ≠ (kI, idI)` (`:2503`). The same row's strict Cases cell says *"the key half [is severed] by nothing the strict fixture can present, so D11's discharge in (a)/(b) rests on (iii)"*. The runs agree with the Cases cell: conjunct 3 is green in `cap_cc15i_a.out:12469` and `cap_cc15i_b.out:12508` (and in both repaired copies), and red in (d) at `cap_cc15i_d.out:20377`.

Why the strict fixture forces green (a reading of the model, not a run): AttestStageW accepts the inner signature only under kEncW. The standing path pins `sg = sgI` by term equality inside a core whose lineage the TLR signs under `kT = kX`, with `fp(kT) = kfpr` of a tuple both channels evidence. In strict that is an honest key, so `kEncW = kX`. One key holds one manifest (skI ↔ M2/issuerId2), so the wrapper's identity equals the standing path's.

Set (1)'s conjunct-3 membership for (i) needs case assignment to (d) only. The assembler was right to leave it open rather than score it.

## What each class implies for the record

- **A (G3; C-C15(i), 17 RESULT lines in (a), (b) and (d)): repair the fixture and re-run.** In `derive.py:cc15i`, report kEncW in place of kA/kB in AttestStageW's events and reports, exactly as `mk_cc15i_kw.py` does, keeping the scope reports as they are. Regenerate `cap_cc15i_{a,b,d}.pv` and re-run all three. The repaired copies predict that run: about 4 min each for (a)/(b), and (d) took 7468 s in the ladder. Record the broken fixture and its repair in RESULTS.md, as `cap_cc03_a` was. The diagnostic copies are evidence, not ladder results.
- **B (G2; C-C10 (a)/(b), C-C14 (a)/(b)): a finding for the reviewer and the author.** C-Q6 conjunct 1's unrestricted form is red whenever authority evidence can be had for an attacker-key tuple. That is the standing-path twin of `Accept ⟹ IssuerSigned`, and case (c) shows it unmutated. It reaches C-C10's set (2) as a registered green gone red. *(REPAIR 2026-10-01, skeptic S-6: the case-(c) clause is diagnostic only; the finding is a dependence the registration encoded at `PREDICTIONS.md:1018` and mis-predicted in C-C10's set (2); and it now has an amendment-shaped route, RESULTS.md item 5.)*
- **C (G1: C-C5 (a)/(b) ×2 and C-C17 (a)/(b); G4: C-C15(i) C-Q2 (a)/(b); conjunct 3 for (i) in strict): amendment-shaped items.** These are labelled per DECISION.md provenance, never entered as author rulings:
  - add the two authorship correspondences to C-C5's set (1) for (a)/(b), and the unrestricted one to C-C17's;
  - add C-Q2 to C-C15(i)'s set (1) for (a)/(b);
  - case-assign conjunct 3 for (i) to (d).

  The C-C7 S-4 repair is the precedent for the first.
- **D: none.** Every item was settled by its trace, and G3 was also settled by a run.
