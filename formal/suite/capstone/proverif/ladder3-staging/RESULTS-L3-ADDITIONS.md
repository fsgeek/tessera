# RESULTS.md additions for ladder 3: a draft, not applied

**STATUS: PROPOSED, 2026-10-01.** Produced by the AI collaborator (Claude Opus 5.5, capstone builder,
directed by the owner instance). Not adopted; the commit is the author's. **Nothing here has been
applied to `formal/suite/capstone/RESULTS.md`.** Each block names the place it goes. The owner instance
applies the blocks when it installs ladder 3. Cells marked `‹…›` can be filled only from ladder 3's own
runs.

Sources: `docs/reviews/2026-10-01-codex-review-capstone-build.md` (findings 1-7 and the owner instance's
Dispositions); `proverif/ladder3-staging/DERIVATION-CHECK-L3.md`; the staged files in
`proverif/ladder3-staging/`.

---

## 1. The blob table: add a fourth row (after the `a9fb7da1…` row)

| Blob | When | Results standing under it |
|---|---|---|
| `35d8c7020adc31f714d31b12c34a8eaf68010c9b` | **REPAIRS BF-5 and BF-6, 2026-10-01.** The owner instance accepted cross-family review findings 2 and 4 as defects of `capstone.pv`. The blob is `capstone.pv` (`a9fb7da1…`) plus three things. (1) A 23-line dated comment block after `set selFun = Term.`. The R-9 block and its setting are kept unchanged. (2) BF-5: a structural innermost-layer selection at the head of `StandingPath`, with its dated comment. (3) BF-6: the `lyr <> L0` guards on the two standing witnesses' emissions, with their dated comments. `diff`: 53 lines added, 2 changed, none removed. **Ladder 3**, ubuntu24, launched ‹time› (`ladder.log:‹n›`). | **every result in sections 1-3, once ladder 3 lands.** The eleven ladder-2 degraded mechanism failures are **not run under this blob** (the owner instance's disposition). Their cells read *not run under this blob*, and they cite the ladder-2 failure as history, never as a ladder-3 result. |

Change the line *"**`capstone.pv` HAS CHANGED TWICE, and this is the record of it**"* to *"THREE TIMES"*,
with a dated note quoting the withdrawn word, on the pattern of the existing note. Change the STATUS
line's blob to `35d8c702…`, with a dated note that names `a9fb7da1…` as ladder 2.

---

## 2. Broken fixtures: three new entries (after BF-4)

Change *"Four have occurred (BF-1 to BF-4 …)"* to *"Seven have occurred (BF-1 to BF-7; until 2026-10-01
this sentence read “Four”)"*. BF-5 and BF-6 are defects of the **correct model**, not of a companion. That
is the same class as BF-3, and the entries say so.

**BF-5: the correct model, every case. The standing path could report at an intermediate wrapper,
not the innermost layer. Found by the cross-family review (finding 2); repaired 2026-10-01; confirmed by
probe; the correct model's 47 verdicts in (a) unchanged.**

**What was wrong.** The registration puts C-Q6's `lyr` at *"the **innermost** layer of the wrapped
presentation"* (`PREDICTIONS.md:782`), and *"at depth 2 the innermost layer is `L2`"* (`:939-940`). The
standing path *"computes over the innermost `(t, ppf, sg, fb)` that it extracts structurally, itself"*
(`:892-894`). `StandingPath` read every layer that its own structural unwrapping (`SUnwrap`) put on
`sStageCh`, at `L0`, `L1` and `L2`. It never required that descent had stopped. So `EstablishedWrapped`
could fire at `L1` while the frame at `L1` was itself a wrapper. The reviewer's probe on ladder-2
`capstone_d.pv` showed this. The trace runs wrapper → wrapper → attestation, and standing is established
at `L1` (`dev/codex/scratch/capstone_d_noninnermost_attest.out:2998`, `:3010`, `:3020`). **So C-Q6 ranged
over standing reports the registration does not define.** A green over that wider domain is conservative.
A red or a witness there may be about the wrong layer.

**The repair** (`capstone.pv`, `StandingPath`, the block marked *BF-5 REPAIR 2026-10-01*). Immediately after
its `sStageCh` input, `StandingPath` proceeds only if the frame at this layer does **not** match
`SUnwrap`'s own pattern, `framed(=OT_WRAPPER, …, wrap(…))`. That is, it proceeds only where its own
structural descent has finished. It uses the registered definition of "wrapped", *"an `OT_WRAPPER` frame
whose payload field is a `wrap()` term"* (`:942-944`), and its complement defines "innermost". The repair
adds **no** type check, signature, authority check, or envelope event or success. (E1) is untouched: the
standing path still neither waits for nor is conditioned on `LayerAccepted`. *A positive guard was
considered and rejected:* requiring the layer's frame to be `OT_ATTEST` would copy envelope check 5 into
the standing path. That check is one C-C13(i) removes, and the registration defines innermost by the
wrapper parse, not by the attestation type.

**Blobs and diffs.** Every one of the 80 files changes blob, by exactly the same hunks
(`DERIVATION-CHECK-L3.md`). Probe evidence, which is not a ladder result. On the repaired model, the reviewer's intermediate-wrapper state is unreachable in (a) and (d) (`ladder3-staging/smoke/probe_a.out:2591`, `probe_d.out:2588`). On the unrepaired model the same probe reaches it (`probe_a_L2control.out:3117`; the reviewer's `capstone_d_noninnermost_attest.out:3020`). Honest wrapped standing stays reachable at `L1` and `L2` in both modes (`probe_a.out:4332`, `:5066`; `probe_d.out:4505`, `:5417`). The correct model's 47 `RESULT` lines in (a) are byte-identical to ladder 2's (`ladder3-staging/smoke/capstone.out`, 225 s on wam-nuc). Method: `DERIVATION-CHECK-L3.md` §3-§4.

**BF-6: the correct model, every case. The two standing witnesses were emitted at `L0`. Found by the
skeptic read (S-3, F-2's repair note) and the cross-family review (finding 4); repaired 2026-10-01.**

**What was wrong.** `HonestWrappedStandingAgreed` is registered for *"an honest wrapped acceptance"*
(`PREDICTIONS.md:1210-1212`). `HonestStandingEstablished` is registered *"over a **wrapped**
presentation"* (`:1341`). Both emission sites allowed `L0` (ladder-2 `capstone.pv:1054`, `:1064`), and every
ladder-2 trace for both was at `L0` (F-2's table). So the *"as registered"* witness classifications in
section 1 (`RESULTS.md:342-349`) were too strong. C-N1 requires these witnesses in **every** companion
(`:1503`).

**The repair.** Both judges already hold the layer. `StandingJudge` receives `lyr` on `estCh`, and
`ScopeAgreementJudge` receives `l` on `scopeStanding`. Each emission is guarded with `if lyr <> L0` (or `l <>
L0`), as `StandingUnentitledWrapped`'s emission already was. **No query, no event signature and no
registered text changes.** The pair judge `ScopeMisreported` is **not** guarded. These are the
cross-family reviewer's own guards (`dev/codex/scratch/capstone_wrapped_witness.pv:1054`, `:1064`). On
ladder-2 baseline (a), with those guards alone, both witnesses were reachable at `L1` and all 47 verdicts
matched (`capstone_wrapped_witness.out:9124`, `:9132`, `:9794`, `:9798`). Ladder 3 is what checks the
witnesses in every companion, as C-N1 requires.

**BF-7: C-C7(i), all three cases. The companion also accepted signed payloads that are not frames.
Found by the cross-family review (finding 3); repaired 2026-10-01 in `derive.py`.**

**What was wrong.** C-C7(i)'s registered mutation is *"the signature must verify under `kX` over *some*
frame naming `fp(kX)`, not over the presented bytes"* (`PREDICTIONS.md:1776`). The family descent
destructures the signed payload as a frame:
`let framed(otS, algS, idS, =fp(kX), mhS, cvS, plS) = fbS in`
(`ledger-tests-2026-09-14/d6e_sp1_q8all_samekey_unbound.pv:258`; the same line is in
`cap17b_sp1_strict_cc7i.pv:293`). `derive.py:cc07i` used `if sigFrameKfp(sbA, kA) = fp(kA)`. That
companion-local accessor's catch-all returns `fp(k)` for a **non-frame** payload, so any signed non-frame
passed (ladder-2 `derive.py:248-260`, `:351-360`). The companion therefore also removed the signed-frame
requirement. The reviewer did not show that this changed a strict verdict or caused `cap_cc07i_d`'s
timeout, and this report does not claim it either.

**The repair** (`derive.py:cc07i`, under a dated comment). The family's pattern match is transcribed:
`let framed(sfoA, sfaA, sfiA, =fp(kA), sfmA, sfcA, sfpA) = sbA in`, and the same for slot B. This is done in
the attestation and wrapper blocks. The unused accessors are no longer added to this companion. In each C-C7(i)
file, BF-7 is +6/−20 lines on top of the BF-5/BF-6 hunks.

**The audit of the same accessor elsewhere.** C-C6 (`cc06`) and C-C7(ii) (`cc07ii`) also use the
catch-all accessors, and they are **not** changed. In both, a non-frame signed payload makes the waiver's
condition false, so acceptance then requires `sb_ = fb_`. Every block the edit touches has already
destructured `fb_` as a `framed(…)` term, so the two can never be equal. A non-frame is therefore
rejected, as the families' pattern match rejects it (`d5a_sp1_condunbind.pv:207-210`,
`cap22b_sp7_strict_cc6.pv:232-235`, `d6d_sp1_q8_type_conditional_unbound.pv:276-280`,
`cap17c_sp1_strict_cc7ii.pv:305-309`). This reasoning is recorded as a note in `derive.py` below `cc07ii`.
No other companion uses the accessors.

**Ladder 3 status of C-C7(i).** `cap_cc07i_a` and `cap_cc07i_b` re-run under ladder 3. `cap_cc07i_d` was
a ladder-2 mechanism failure (`rc=124`, `ladder.log:68`), so it is one of the eleven not re-run. Its
regenerated file is staged, but this blob gives it no result.

---

## 3. Ladder restarts: add a row to *After 2026-09-19*

| When (UTC) | What, and why | Record |
|---|---|---|
| **‹2026-10-0x›: ladder 3** | **A new model, not a restart of the old one.** The blob is `35d8c702…` (BF-5, BF-6), and C-C7(i)'s files also carry BF-7. Ladder 2's `.pv`, `.out`, `.rss` and `ladder.log` are archived **unmodified** under `proverif/ladder2/` (‹path as installed›). Ladder 3 begins from an empty `ladder.log`. **Scope, decided by the owner instance:** the 69 files that landed in ladder 2 are re-run. The eleven ladder-2 degraded mechanism failures (`cap_cc02_d`, `cap_cc03_d`, `cap_cc04_d`, `cap_cc05_d`, `cap_cc06_d`, `cap_cc07i_d`, `cap_cc07ii_d`, `cap_cc08_d`, `cap_cc08i_d`, `cap_cc08ii_d`, `cap_cc17_d`) are **not** re-run, and their cells read *not run under this blob*. Machine ubuntu24, `JOBS=‹n›`, `mem_guard_vm.sh` re-armed, with the same boxes, runner and wave order. | `owner_interventions.log:‹n›`; `ladder.log:1-‹n›` |

---

## 4. Blocked: withdraw B-5 in place

Put this immediately under B-5's heading. Keep B-5's text as written.

> *(WITHDRAWN 2026-10-01: cross-family review finding 4, ACCEPTED by the owner instance. **What was
> wrong:** B-5 said the existing query signatures cannot show "wrapped", and that closing the gap is
> "**amendment-shaped**, not the builder's". That necessity claim is false. Both judges already receive
> the layer, so guarding the two **emissions** with `lyr <> L0` makes each witness wrapped-only, with no
> query, event signature or registered sentence changed. The reviewer's strict run showed it
> (`dev/codex/scratch/capstone_wrapped_witness.out:9132`, `:9798`). The repair is BF-6 (*Broken
> fixtures*). Separate `L1` and `L2` witness conjuncts would be an additional strengthening, which this file
> does not propose. Nothing is routed for amendment from B-5.)*

Also change the Blocked preamble's *"(five since 2026-10-01: B-5 …)"* to *"(five since 2026-10-01; B-5
withdrawn the same day, BF-6)"*. In F-2's repair note, add after *"The gap is recorded as **B-5**."*:
*"(Dated note 2026-10-01: B-5 is withdrawn; the emission guard is BF-6, and ladder 3's traces for both
witnesses are at ‹layers, from ladder-3 outputs›.)"*

---

## 5. C-C15(i)'s accepting-key join: ROUTED TO THE AUTHOR (a third routed question)

Put this after the second routed question. `DERIVATION-CHECK-L3.md` §6 carries a summary of it.

### ROUTED TO THE AUTHOR: third question. Under C-C15(i), which key is C-Q6's `kX`? *(added 2026-10-01; cross-family review finding 1)*

**The conflict.** The registration fixes C-Q6's `kX` in two ways that agree in the correct model and come
apart under C-C15(i).

1. *"**`kX`** — the accepting key, `LayerAccepted`'s own name for it. For C-Q6 it is the **innermost
   accepting key**: the `kI` of S-P7's `InnerCheck`, not the wrapper's `kW`. … the join's whole point is
   that it is the **same** argument"* (`PREDICTIONS.md:786-791`). The join table's row is *"`kI`, the
   inner accepting key | `kX` | **`kX = kI`**"*, and it is **immutable**: *"no companion removes it —
   removing one does not sever a producer fact, it un-joins the composition and makes C-Q6 vacuous"*
   (`:1005-1009`, `:1019`).
2. C-C15(i)'s own cell (`:2503`). *"the inner signature verified under `kW` instead of `kI`"*; *"the inner
   acceptance of this configuration reports the **presented inner** `(kW, tI, ppfI)`"* (the report
   contract BF-4 implemented); and, for conjunct 3, *"**(i)** reports the **wrapper** frame's key **and
   identity**, so `(kA, idA) = (kW, idW) ≠ (kI, idI) = (kX, id)` … in both the standing path's own
   extraction is untouched and reports `(kX, id) = (kI, idI)`"*. With conjuncts 1 and 2 predicted green
   *"because … the standing path … is **untouched by a scope mutation**"*.

Under C-C15(i), the key the inner acceptance **verifies under**, and that `LayerAccepted` carries, is
`kW`. The standing path is registered as untouched, and it computes against the **presented** inner key
`kI`. Sentence 1 requires those two to be "the same argument". Sentence 2 requires them to differ: it
predicts conjunct 3 red *because* they differ. The reviewer's run shows exactly that. One intake and layer
accepts under `pk(a_4)` and establishes standing under `pk(a_20)`
(`dev/codex/scratch/cc15i_d_keyjoin.out:3528`, `:3550`, `:3562`).

**Why the builder cannot repair it.** The builder judges this a registration conflict, not an encoding
defect. There are only three ways to make the standing key equal the accepting key under (i):

- the standing path reads the envelope's accepting key, which (E1) forbids;
- the companion also re-keys the standing path to `kW`, which contradicts sentence 2 ("untouched";
  `(kA, idA) ≠ (kX, id)`) and removes the key half of conjunct 3's registered red;
- the inner acceptance verifies under `kI`, which is no longer Q6b's mutation. That shape is configuration
  (iii).

Every one of them breaks a registered sentence. The current files follow sentence 2 and the literal "the
`kI` of S-P7's `InnerCheck`" of sentence 1. In Q6b, `InnerCheck`'s `kI` is a presented input that the
mutation leaves unused (`s-p7/proverif/sp7_q6b_companion_key_outermost.pv:181-198`). So `kX = kI` holds
as a **term** equality: both paths take the same presented `kI` from the one intake. What the files cannot
also satisfy is sentence 1's "accepting key … `LayerAccepted`'s own name … the same argument". Configurations
(ii) and (iii) leave the inner verification key alone, and **the conflict is confined to (i)**.

**The two readings the author can choose between.**

- **(A) `kI` is the presented innermost key.** This is the term `InnerCheck` is handed. Sentence 1's
  "accepting key" wording is amended to say so. C-C15(i) as built then preserves the join, and its C-Q6
  results read as registered.
- **(B) `kI` is the key the innermost acceptance actually verified under.** Then C-C15(i)'s registered
  severing cannot preserve the join, and (i) must be re-specified for C-Q6. One way is that C-Q6's
  conjuncts are not asserted of (i), and D11's C-Q6 half rests on (ii) and (iii).

**What C-C15(i)'s C-Q6 results can and cannot mean until the author rules.** They are **withheld from
discharge** (the owner instance's disposition 1).

- **Conjunct 3** is red in (d) (`cap_cc15i_d.out:19679` in ladder 2) and left open in strict. The red can
  show that the envelope's attribution `(kW, idW)` and the standing report `(kI, idI)` differ for one intake
  and layer. That is the sense sentence 2 registers. It **cannot** show a join-preserving severing under
  reading (B), because under (B) the two reports are about different keys by construction, and that red
  needs no scope severing to fire.
- **Conjuncts 1 and 2** are green. They remain statements about the standing path over the presented
  innermost terms. They do not certify composition with the key the envelope actually accepted under.
- **What does not move.** D11's link-6b half rests on C-C15(i) (d)'s link 6b red and on (ii) and (iii), and
  none of that involves the standing key. D11's strict discharge already rests on (iii)
  (`PREDICTIONS.md:2503`). D12 and D13 rest on C-C11 and C-C12, not on C-C15.
- **Not done, and not to be done:** making standing wait for envelope success (E1).

---

## 6. Finding 5, the box reading: restatement in place

In *ROUTED TO THE AUTHOR — second question*, mark the sentence at `RESULTS.md:1130` *"Neither reading
makes any sentence false; they differ on which sentence sets a companion's limit."* **withdrawn in place**:

> *(WITHDRAWN 2026-10-01: cross-family review finding 5, ACCEPTED by the owner instance. **What was
> wrong:** (Q) is the reading the registration's own words support. It calls the entries "separately
> timeboxed" and puts each conjunct inside its entry's box (`PREDICTIONS.md:1632-1641`). It then gives each
> companion **its predicted-red query's box** and names C-C17's 45 minutes and C-C16's 60
> (`:1867-1876`). Under (P) those two sentences become accounting statements, which they do not say they
> are. The two readings are **not** equally faithful. (P) is a departure from the frozen text, and
> accepting it is an amendment.)*

Replace the owner instance's recommendation heading and its first bullet. Keep the old text, marked
superseded, as in the file's other withdrawals:

> **The owner instance's recommendation (2026-10-01; a recommendation, not a ruling), RESTATED: AMEND the
> companion allowance to (P).** *(Restated 2026-10-01 under cross-family finding 5. The withdrawn heading,
> quoted: "The owner instance's recommendation (2026-10-01; a recommendation, not a ruling): (P).")*
>
> - **What the amendment does.** It replaces §4's *"a companion runs inside the box of the query it is
>   predicted to red"* (`:1867-1876`) as a **run limit**. The replacement says *"a companion runs under its
>   case's per-case sum, as the correct-form run does; it adds no entry to the ceiling"*. It is an
>   **exception entered after the freeze**, and is not a reading of the frozen text.
> - **What it preserves.** Every severing observed in sections 2-3 stands as observed, under the per-case
>   allowance every file actually ran under. On the ladder-3 record that is D3 in (c), D4 in all four cases,
>   D6 and D9 and D7's membership half in (a) and (b), and D7's common-content half, D8 and D11 in (d). (These
>   rows are as in the effect table, re-read from ladder 3.)
> - **What it relinquishes.** It gives up the registered claim that each of those severings shows inside a
>   **30 to 60 minute** box. Per-query time was never logged, so no run shows it. Under the frozen text
>   those runs are *"not shown inside the box"*. That is not the same as being shown outside it, and no
>   property is relabelled false.
> - **What still holds from the original bullets.** The builder chose (P) for `run_ladder.sh` on
>   2026-09-19, before any result existed. That reduces outcome-driven selection. It does **not** turn
>   (P) into the frozen instruction. The method lesson stands as written: a registration states its
>   companion box in one sentence, and the runner logs per-query time.

Change the second question's lead *"which companion-box reading governs"* to *"whether to amend the
companion allowance to the per-case sum (P), or keep the registered predicted-red box (Q)"*.

---

## 7. Finding 6, "neither disposal can": restatements in place

Three places. Keep each original sentence and add a dated note beside it.

- **Header, `RESULTS.md:15-16`** (*"The eleven degraded failures cannot be disposed of by either of §3's
  two disposals"*): add *(Restated 2026-10-01, cross-family finding 6: **the tactics and ablations tried did
  not resolve the sampled failures without unacceptable witness or mutation loss.** That is not an
  impossibility result for all eleven. The diagnosis (`dev/abl_d/REPORT.md:85`, `:154`) tested particular
  attempts, chiefly on C-C2 and C-C5 under stated limits, and its own conclusion is "no sound tactic
  **tried**".)*
- **The routed question, `RESULTS.md:976`** (*"The diagnosis shows that neither disposes of these"*):
  replace the clause in a dated note with *"the tactics and ablations tried (`abl_d` §(c), §(e), §(f)) did
  not resolve the sampled failures without unacceptable witness or mutation loss; that is not shown for all
  eleven, and it is not an impossibility result"*. Keep the original, quoted.
- **F-5's dated note, `RESULTS.md:1858`** (*"neither of §3's disposals disposes of them"*): the same
  restatement, by a dated note.

The disposal recommendation (option (i)) is unchanged. The note should add what the reviewer read as
governing. Option (i) relinquishes composed severing for **D1, D2, D5 and all of D10's consumer
requirement**, and degraded coverage for **D6 and D7's membership half**. Family evidence does not become
composed evidence. "Weeks" for a Tamarin follow-up is an estimate, not a measured cost.

---

## 8. Consequential notes for sections 1-3 (to make when ladder 3 is assembled)

- Section 1, rows `RESULTS.md:342-349` (the two standing witnesses): refill from ladder 3, with the
  layer of each printed trace. Under BF-6 they can only be `L1` or `L2`.
- Section 3, rows D11, D12 and D13: add *"C-C15(i)'s C-Q6 cells are withheld from discharge pending the
  third routed question"* (D11). For D12 and D13, add *"C-Q6 now ranges over innermost layers only
  (BF-5)"*. Any C-Q6 colour that moved between ladder 2 and ladder 3 is listed and explained.
- Section 2a: re-derive the divergence table from ladder 3. A divergence that disappears or appears under
  BF-5 is recorded as such, and is never carried over silently from ladder 2.
