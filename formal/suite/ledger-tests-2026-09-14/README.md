# Ledger severing tests, 2026-09-14 — scratch copies, archived as review inputs

STATUS: PROPOSED — produced by the AI collaborator (Claude Opus 5, directed
by the owner instance) while repairing `formal/suite/LEDGER.md` after the
Codex review of the same day (`docs/reviews/2026-09-14-codex-review-ledger-and-k6.md`);
not adopted; the commit is the author's. **Nothing here is a suite model
or a registered companion.** Each `.pv` is a copy of a committed family
model (`base_*.pv` unchanged; `m*_`, `s*_` mutated as its header says)
run with `proverif -lib formal/suite/lib/tessera_theory.pvl` (ProVerif
2.05) to test one severing claim before it was written into LEDGER.md;
the `.out` beside each is the run. LEDGER.md cites these files by name
and `.out` line. They discharge nothing; they are the evidence that the
register's "expected red" cells were checked rather than asserted, per
the review's finding that "this check alone suffices" does not imply
"removing this check breaks protection".

## Second batch, 2026-09-15 — the D5 producer question

Added while repairing `formal/suite/LEDGER.md` after the **second**,
full non-author review of the same file
(`docs/reviews/2026-09-15-codex-full-review-ledger.md`, six findings,
all accepted). Same discipline as the first batch: copies only, run
with `proverif -lib formal/suite/lib/tessera_theory.pvl` (ProVerif
2.05), each `rc=0`, nothing registered, no repository model edited or
run, no family file changed.

These four runs answer finding 1 — whether S-P1's honest-key authorship
theorem supplies what S-P7's `InnerSigTransplanted` query consumes.
They reproduce the reviewer's diagnostic on our own tree, extend it to
S-P3's `Reattributed` fact, and check the feasibility of the producer
query the ledger now says the capstone must register (C-Q7).

| File | Copy of | Mutation / addition | Result |
|---|---|---|---|
| `d5a_sp1_condunbind.pv/.out` | `s-p1/proverif/sp1_q2_degraded_compromised.pv` | `VerifierS`'s `let (=BYTES, =fb) = checksign(sg, kX)` becomes a **conditional** binding: the presented bytes must equal the signed bytes only when the signed frame's own `kfp` field matches the verifying key | S-P1 Q2(i) `AcceptedUnderHonestKey ==> IssuerSigned` **still `is true`** (`:195`); `HonestAccepted` reachable (`:371`); Q2(ii) `is false` as registered (`:521`) |
| `d5b_sp7_condunbind.pv/.out` | `s-p7/proverif/sp7_q2_degraded_compromised.pv` | the same conditional binding inside `InnerCheck`, **plus** S-P1's honest-key authorship judge and query transcribed in (new private channels `honestKeyChD5`, `acceptKeyChD5`) | authorship **`is true`** (`:654`), `Reattributed` **`is true`** (`:1060`), **`InnerSigTransplanted` `is false`** (`:1037`); `TypeConfused` (`:677`), `Rescoped` (`:700`), `VersionLied` (`:1599`) true; witnesses reachable (`:1370`, `:1576`) |
| `d5c_sp1_sigjudge.pv/.out` | `sp1_q2_degraded_compromised.pv`, verifier and every registered query **unmutated** | **adds** the signature-**term** judge (S-P7's `SigJudge` shape) and the query `SigTransplanted(kX, sg)` — the C-Q7 shape | `SigTransplanted` **unreachable, `is true`** (`:203`); Q2(i) `is true` (`:210`); witness reachable (`:386`) |
| `d5d_sp1_sigjudge_condunbind.pv/.out` | `d5c_sp1_sigjudge.pv` | the same conditional unbinding | `SigTransplanted` **reachable, `is false`** (`:414`) while Q2(i) stays `is true` (`:422`); witness reachable (`:599`) |

Read together: the relation S-P7 consumes is falsifiable, the committed
producer queries do not range over it, and a query that does is green
on the committed verifier. `d5c`'s `SigTransplanted` result is **not**
an S-P1 result and no S-P1 file records it; it is a feasibility check
on a query the capstone must register for itself.

## Third batch, 2026-09-15 (round 3) — the D6 and D10 producer questions

Added while repairing `formal/suite/LEDGER.md` after the **third**
non-author round (`docs/reviews/2026-09-15-codex-full-review-ledger-round3.md`,
six findings, all accepted) and the same day's full skeptic read. Same
discipline as the first two batches: copies only, run with
`proverif -lib formal/suite/lib/tessera_theory.pvl` (ProVerif 2.05),
each `rc=0`, nothing registered, no repository model edited or run, no
family file changed.

These four runs answer findings 1 and 2 — whether the producers the
register had named for D6 and D10 establish what those joins' consumers
actually consume. In both cases they do not, and in both cases a query
that does is green on the committed verifier. They are the evidence
behind the register's new rule: a join with no producer in the tree is
recorded as "producer to be registered in the capstone", with the exact
relation stated, and nothing else claimed.

| File | Copy of | Mutation / addition | Result |
|---|---|---|---|
| `d6a_sp1_q8_base.pv/.out` | `d5c_sp1_sigjudge.pv` (itself an unmutated copy of `s-p1/proverif/sp1_q2_degraded_compromised.pv` plus the C-Q7 signature-term judge) | **adds** the **C-Q8** three-place judge — `event SigBytesUnbound(pkey, bitstring, bitstring)` over *(accepting key, signature term, presented framed bytes)*; verifier and every registered query unmutated | C-Q7 `SigTransplanted` **`is true`** (`:244`), C-Q8 `SigBytesUnbound` **`is true`** (`:250`), Q2(i) `is true` (`:258`), witness reachable (`:435`), Q2(ii) `is false` (`:586`) as registered |
| `d6b_sp1_q8_samekey_unbound.pv/.out` | `d6a_sp1_q8_base.pv` | **same-key byte unbinding**: the attestation signature must verify under `kX` over *some* frame naming `fp(kX)`, no longer over the **presented** bytes. Every other check retained | **C-Q7 stays `is true`** (`:246`) while **C-Q8 `is false`** (`:427`) and **Q2(i) `is false`** (`:593`); witness reachable (`:773`). *C-Q7 is blind to different bytes under the same key; C-Q8 is not* |
| `d10a_sp2_q9_base.pv/.out` | `s-p2/proverif/sp2_q2_degraded_compromised.pv`, verifier and every registered query **unmutated** | **adds** two judges: S-P3's `PossJudge` shape (`PossessionTransplanted`, keys only) and the **C-Q9** judge `event PossessionUnbound(pkey, bitstring, bitstring)` over *(accepting key, accepted manifest, accepted possession proof)*, fed from every acceptance point | all five S-P2 safety queries `is true` (`:457, :464, :471, :478, :1097`), `PossessionTransplanted` **`is true`** (`:1104`), C-Q9 **`is true`** (`:1111`), both `HonestComplete` reachable (`:643`, `:861`), `HonestAccepted` reachable (`:1090`) |
| `d10b_sp2_q9_manifest_unbound.pv/.out` | `d10a_sp2_q9_base.pv` | **both manifest-binding protections removed together**: possession made fingerprint-only (library D-3 under-encoding) **and** the frames' `mh = h(t)` guards dropped; frames, per-slot `=fp(kX)` pins, tuple fingerprint matches and the three §A5.4 content guards retained | **`PossessionTransplanted` stays `is true`** (`:1297`) while **`SetAltered` `is false`** (`:673`) and **C-Q9 `is false`** (`:1462`); `Stripped` (`:454`), `SignerForged` (`:464`), `Reattributed` (`:683`), `Spliced` (`:1287`) still true; both `HonestComplete` (`:851`, `:1072`) and `HonestAccepted` (`:1277`) reachable |

`d6a`/`d6b`'s C-Q8 results and `d10a`/`d10b`'s C-Q9 results are **not**
S-P1, S-P2 or S-P3 results and no family file records them; they are
feasibility checks on queries the capstone must register for itself.

## Fourth batch, 2026-09-15 (round 4) — the proof contract, not the register

Added while repairing `formal/suite/LEDGER.md` after the **fourth**
non-author round (`docs/reviews/2026-09-15-codex-full-review-ledger-round4.md`,
four findings, all accepted). Same discipline as the first three
batches: copies only, run with
`proverif -lib formal/suite/lib/tessera_theory.pvl` (ProVerif 2.05),
each `rc=0`, nothing registered, no repository model edited or run, no
family file changed.

All four of that round's findings are defects in the **proposed proof
contract** — C-Q1 and C-Q8 — not in the register's entries or in the
construction. These seven runs are the evidence for them. Three
(`d6c`, `d6d`, `d6e`) concern C-Q8's quantifier; two (`cq1a`, `cq1b`)
C-Q1's accepted-evidence binding; two (`cq1c`, `cq1d`) C-Q1's
required-set completeness.

| File | Copy of | Mutation / addition | Result |
|---|---|---|---|
| `d6c_sp1_q8_judge_all.pv/.out` | `d6a_sp1_q8_base.pv` (itself an unmutated copy of the committed `s-p1/proverif/sp1_q2_degraded_compromised.pv` plus the C-Q7 and round-3 C-Q8 judges) | **adds** the **rewritten C-Q8**: a structural judge over *every* accepted `(key, signature, presented frame)` triple, including failed verification, with no honest-signature filter | C-Q7 `is true` (`:272`), round-3 C-Q8 `is true` (`:278`), **rewritten C-Q8 `is true`** (`:284`), Q2(i) `is true` (`:292`), witness reachable (`:469`), Q2(ii) `is false` (`:620`) as registered |
| `d6d_sp1_q8_type_conditional_unbound.pv/.out` | `d6c_sp1_q8_judge_all.pv` | **the reviewer's escape:** byte equality between the signed and the presented frame is required only when the signed frame's `objType` is `OT_ATTEST`, and is waived for every other signed frame type. Every honest signature in this fixture is over an `OT_ATTEST` frame | **round-3 honest-filtered C-Q8 stays `is true`** (`:315`) while **the rewritten C-Q8 is `is false`** (`:507`); C-Q7 `is true` (`:308`), honest-key authorship `is true` (`:515`), witness reachable (`:692`). *The quantifier gap, shown* |
| `d6e_sp1_q8all_samekey_unbound.pv/.out` | `d6c_sp1_q8_judge_all.pv` | **C-C7 configuration (i)**, the same-key byte unbinding `d6b` makes, now run against the rewritten judge | **rewritten C-Q8 `is false`** (`:643`), round-3 form `is false` (`:455`), Q2(i) `is false` (`:809`), **C-Q7 stays `is true`** (`:274`), witness reachable (`:989`) |
| `cq1a_sp1_evidence_base.pv/.out` | `d6c_sp1_q8_judge_all.pv`, verifier and every registered query **unmutated** | **adds** C-Q1's **link-1a** evidence-binding conjunct: the acceptance report carries the accepted evidence term, and a judge requires `checksign(ev, pkCh) = (STMT_DIGEST, h(t))` for the accepted `t`, including non-verification. Degraded mode, sole channel compromised | C-Q7 (`:304`), round-3 C-Q8 (`:310`), rewritten C-Q8 (`:316`), **link 1a** (`:322`) and Q2(i) (`:330`) all `is true`; witness reachable (`:507`) |
| `cq1b_sp1_evidence_unchecked.pv/.out` | `cq1a_sp1_evidence_base.pv` | **only** the degraded verifier's evidence check removed; every other check retained | **link 1a `is false`** (`:466`) while **C-Q7 (`:301`), both C-Q8 forms (`:307`, `:313`) and honest-key authorship (`:474`) stay `is true`** and the witness stays reachable (`:638`) |
| `cq1c_sp2_slots_base.pv/.out` | `d10a_sp2_q9_base.pv` (itself an unmutated copy of the committed `s-p2/proverif/sp2_q2_degraded_compromised.pv` plus the `PossJudge` and C-Q9 judges) | **adds** C-Q1's **link-2b** completeness conjunct: an acceptance identifier per acceptance, a slot record per signer slot under it, `AcceptanceComplete(aid, t)` after them, and three correspondences demanding a record for every required slot | all four S-P2 safety queries (`:471`, `:478`, `:485`, `:492`), `Spliced` (`:1133`), `PossessionTransplanted` (`:1140`), C-Q9 (`:1147`) and **all three link-2b conjuncts** (`:1161`, `:1175`, `:1189`) `is true`; witnesses reachable (`:663`, `:889`, `:1126`) |
| `cq1d_sp2_slots_missing.pv/.out` | `cq1c_sp2_slots_base.pv` | **the one-signer branch's required-set requirement dropped** (`=signers0` → `ss`); every per-slot check retained | **link-2b slot-B conjunct `is false`** (`:1519`) and `Stripped` `is false` (`:643`), while the per-slot conjuncts survive — link-2b one-signer (`:1333`) and slot A (`:1353`), `SignerForged` (`:650`), `SetAltered` (`:657`), `Reattributed` (`:664`), **`Spliced`** (`:1305`), `PossessionTransplanted` (`:1312`) and **C-Q9** (`:1319`) all `is true`; witnesses reachable (`:835`, `:1061`, `:1298`) |

The rewritten-C-Q8, link-1a and link-2b results are **not** S-P1 or
S-P2 results and no family file records them; they are feasibility and
discrimination checks on conjuncts the capstone must register for
itself.

## Fifth batch, 2026-09-16 — the capstone registration's three showable findings

Added while repairing `formal/suite/capstone/PREDICTIONS.md` after the
**first non-author round on the capstone registration**
(`docs/reviews/2026-09-16-codex-review-capstone-predictions.md`, six
findings, all accepted). Same discipline as the first four batches:
copies only, run with `proverif -lib formal/suite/lib/tessera_theory.pvl`
(ProVerif 2.05), each `rc=0`, nothing registered, **no capstone model
written or run**, no repository model edited or run, no family file
changed.

Three of the four reproduce the reviewer's own `/tmp` diagnostics on
our tree (findings 1, 2 and 5); the fourth, `cap3`, the reviewer did
not make — it is the isolation configuration the repair needed and
whose outcome no run on the record settled.

| File | Copy of | Mutation | Result |
|---|---|---|---|
| `cap1_sp2_content_unchecked.pv/.out` | `cq1c_sp2_slots_base.pv` | the three 2026-09-12 §A5.4 cross-slot **content** equalities — `ota = otb`, `cva = cvb`, `pla = plb` — deleted from `Verifier2S`, and nothing else | **`Spliced` `is false`** (`:1337`, reachable) while **all three link-2b completeness conjuncts stay `is true`** (`:1366`, `:1381`, `:1396`); `Stripped` (`:465`), `SignerForged` (`:472`), `SetAltered` (`:479`), `Reattributed` (`:486`), `PossessionTransplanted` (`:1344`) and C-Q9 (`:1351`) all `is true`; witnesses reachable (`:657`, `:886`, `:1126`). *Completeness cannot carry the common-content fact; the capstone's link 5 must, and now registers companion C-C16* |
| `cap2_sp2_poss_fponly.pv/.out` | `d10a_sp2_q9_base.pv` | **the possession binding alone** made fingerprint-only (`sign((POSS, fp(pk(sk))), sk)` and `let (=POSS, =fp(kX)) = checksign(ppfX, kX)`); the frames' `mh = h(t)` guards, per-slot pins, tuple fingerprint matches and the three §A5.4 guards all retained | **C-Q9 `is false`** (`:1263`) while **`SetAltered` stays `is true`** (`:471`); `Stripped` (`:457`), `SignerForged` (`:464`), `Reattributed` (`:478`), `Spliced` (`:1097`), `PossessionTransplanted` (`:1104`) `is true`; witnesses reachable (`:643`, `:861`, `:1090`); baseline `d10a_sp2_q9_base.out:1111` `is true`. *Possession unbinding alone falsifies the exact possession-message relation, by construction; set integrity survives it* |
| `cap3_sp2_mh_guards_dropped.pv/.out` | `d10a_sp2_q9_base.pv` | **the frames' manifest-hash guards alone** — `if mha = h(t)` / `if mhb = h(t)` deleted on both the one- and two-signer branch; **possession over the accepted manifest under the accepting key retained in full**, as is everything else | **C-Q9 `is true`** (`:1115`) **and `SetAltered` `is true`** (`:468`); `Stripped` (`:452`), `SignerForged` (`:460`), `Reattributed` (`:476`), `Spliced` (`:1099`), `PossessionTransplanted` (`:1107`) `is true`; witnesses reachable (`:642`, `:861`, `:1091`). *The one single removal from the pair that can be required to keep C-Q9 green — the capstone's re-specified C-C8-i* |
| `cap4_sp2_shared_slotA_key.pv/.out` | `d10a_sp2_q9_base.pv` | **the fixture only, not the verifier**: the two-signer manifest `M2`'s first required slot re-keyed from `skA2` to `skA1`, the key that already signs the one-signer manifest `M1`, so one honest key signs two honest manifests. Every verifier check, judge and query untouched | **`SetAltered` `is false`** (`:640`, reachable) with `Stripped` (`:455`), `SignerForged` (`:462`), `Reattributed` (`:647`), `Spliced` (`:1260`), `PossessionTransplanted` (`:1267`) and C-Q9 (`:1274`) all `is true` and witnesses reachable (`:810`, `:1026`, `:1253`). *S-P2's `MemberJudge` needs the one-key/one-manifest fixture restriction; without it the judge reds with no check removed* |

These four results are **not** S-P2 results and no family file records
them, and they are **not** capstone results — no capstone model exists.
They are the evidence behind four repairs to
`formal/suite/capstone/PREDICTIONS.md`, recorded in that file's
"Repairs after the 2026-09-16 Codex review" section.

## Sixth batch, 2026-09-17 — the capstone registration's second round

Added while dispositioning the **second non-author round on the
capstone registration**
(`docs/reviews/2026-09-16-codex-review-capstone-predictions-round2.md`,
four findings, all accepted). Same discipline as the first five
batches: copies only, run with `proverif -lib
formal/suite/lib/tessera_theory.pvl` (ProVerif 2.05), each `rc=0`,
nothing registered, **no capstone model written or run**, no repository
model edited or run, no family file changed.

Eight of the ten are the reviewer's own `/tmp` diagnostics
(`/tmp/tessera-capstone-r2-299yxsvr/`) copied **byte for byte** under a
provenance header and re-run on our tree; every `RESULT` line lands at
the line number the reviewer cited. The reviewer's `theory.pvl` was
byte-identical to `lib/tessera_theory.pvl`, and its two "base" copies
were byte-identical to the committed models they name. The other two
(`cap7c`, `cap7d`) the reviewer did not make: they ask whether the
same-key wrapper signer of finding 3 also disturbs C-C6 and C-C7(i).
It does not.

| File | Copy of | Mutation | Result |
|---|---|---|---|
| `cap5a_ss_q3_companionB_asis.pv/.out` | `s-standing/proverif/ss_q3_companionB_entitled_via_envelope.pv`, **unchanged** | none — the committed C-C12 source re-run as the baseline | `StandingUnentitled` reachable (`:860`); unrestricted `Established ⟹ Designated` `is false` (`:628`); honest-key forms `is true` (`:642`, `:656`); `HonestStandingEstablished` reachable (`:1157`) |
| `cap5b_ss_q3_e1_projection.pv/.out` | `cap5a` | **one guard added to the standing path**, `if fp(kX) = kfpr then` before the report — the necessary condition of C-Q6's E1 (a `LayerAccepted` for the same `t` and `kX`); nothing else | `StandingUnentitled` **unreachable** (`:476`); unrestricted form **`is true`** (`:449`); honest-key forms `is true` (`:459`, `:469`); honest standing still reachable (`:773`). *E1 as written shadows C-C12 — the SS.Q3 p ≈ 0.2 branch, reproduced by event dependency instead of process order* |
| `cap6a_sp7_q2_sigjudge.pv/.out` | `s-p7/proverif/sp7_q2_degraded_compromised.pv` (correct model, degraded, depth 1) | **adds** the C-Q7 signature-term judge (`GenericSigJudge`, `SigTransplanted`); verifier and every registered query unmutated | `SigTransplanted` **unreachable** (`:1099`); every registered query as committed (`:539`, `:552`, `:565`, `:578`, `:1086`); witnesses reachable (`:877`, `:1073`) |
| `cap6b_sp7_q6b_sigjudge.pv/.out` | `s-p7/proverif/sp7_q6b_companion_key_outermost.pv` (C-C15(i)'s source) | **adds** the same C-Q7 judge; the companion's own mutation unchanged | `SigTransplanted` **reachable** (`:1809`), with `Rescoped` (`:781`) and `InnerSigTransplanted` (`:1070`) red as committed, `TypeConfused` green (`:501`), witnesses reachable (`:1329`, `:1520`). *C-C15(i) cannot retain C-Q7* |
| `cap7a_sp1_q8_wrapper_signer_base.pv/.out` | `d6c_sp1_q8_judge_all.pv` (S-P1 Q2 + C-Q7 + both C-Q8 judges) | **adds** an honest `OT_WRAPPER` signer (`ForeignIssuer`) under the **same** issuer key `skI` and manifest `m`, releasing its signature and bytes to every judge; **pins** the presented frame's type to `OT_ATTEST` (where `d6c` read `ot`); byte binding **correct** | C-Q7 (`:310`), round-3 C-Q8 (`:316`), structural C-Q8 (`:322`) and honest-key authorship (`:330`) all `is true`; witness reachable (`:507`); Q2(ii) `is false` (`:658`) as registered. *The signer alone breaks nothing under correct byte binding* |
| `cap7b_sp1_q8_wrapper_signer_type_conditional.pv/.out` | `d6d_sp1_q8_type_conditional_unbound.pv` (C-C7(ii)'s source) | the same wrapper signer and `OT_ATTEST` pin added to the **type-conditional** byte unbinding | **C-Q7 `is false`** (`:528`), **both** C-Q8 forms `is false` (`:711`, `:904`), **honest-key authorship `is false`** (`:1072`, trace `:1032-1072`: an adversary-built `OT_ATTEST` frame under `pk(skI)` carrying the issuer's honest **wrapper** signature); witness reachable (`:1250`). *C-C7(ii)'s registered retained set does not survive a same-key wrapper signer* |
| `cap7c_sp1_condunbind_wrapper_signer.pv/.out` | `d5d_sp1_sigjudge_condunbind.pv` (C-C6's mutation + the C-Q7 judge) | the same wrapper signer and `OT_ATTEST` pin added to C-C6's **conditional** unbinding | **identical to `d5d` result for result**: C-Q7 `is false` (`:448` ↔ `d5d:414`), honest-key authorship `is true` (`:456` ↔ `:422`), witness reachable (`:633` ↔ `:599`), Q2(ii) `is false` (`:784` ↔ `:750`). *C-C6 keys on the signed frame's `kfp`, which the wrapper frame names; unchanged* |
| `cap7d_sp1_q8_samekey_unbound_wrapper_signer.pv/.out` | `d6e_sp1_q8all_samekey_unbound.pv` (C-C7(i) against every judge) | the same wrapper signer and `OT_ATTEST` pin added to C-C7(i)'s **same-key** unbinding | **identical to `d6e` result for result**: C-Q7 `is true` (`:312` ↔ `d6e:274`), both C-Q8 forms `is false` (`:493`, `:681` ↔ `:455`, `:643`), authorship `is false` (`:847` ↔ `:809`), witness reachable (`:1027` ↔ `:989`), Q2(ii) `is false` (`:1206` ↔ `:1168`). *C-C7(i) demands the signed frame name `fp(kX)`; unchanged* |
| `cap8a_sp1_q1_strict_base.pv/.out` | `s-p1/proverif/sp1_q1_strict_dns_compromised.pv`, **unchanged** | none — the committed strict baseline re-run | `Accept ⟹ IssuerSigned` `is true` (`:201`); honest-key authorship `is true` (`:208`); witness reachable (`:396`) |
| `cap8b_sp1_q1_strict_adversary_enrolled.pv/.out` | `cap8a` | **the fixture only**: an adversary key `skAdv` (published) with tuple `mAdv` under a distinct identity, for which **both honest authority processes** publish evidence; verifier and every query unmutated | **`Accept ⟹ IssuerSigned` `is false`** (`:398`) while honest-key authorship stays `is true` (`:405`) and the witness reachable (`:601`). *A genuinely enrolled adversary key falsifies the strict unrestricted baseline with no verifier change; "adversary-enrolled" must mean compromised-channel enrolment only* |

These ten results are **not** S-P1, S-P7 or S-STANDING results and no
family file records them, and they are **not** capstone results — no
capstone model exists. They are the evidence behind the four
dispositions of the round-two record and the repairs to
`formal/suite/capstone/PREDICTIONS.md` recorded in that file's
"Repairs after the 2026-09-16 Codex review, second round" section.

## Seventh batch, 2026-09-17 — the capstone registration's third round

Added while dispositioning the **third non-author round on the
capstone registration**
(`docs/reviews/2026-09-17-codex-review-capstone-predictions-round3.md`,
three findings and one basis defect, all accepted). Same discipline:
copies only, run with `proverif -lib formal/suite/lib/tessera_theory.pvl`
(ProVerif 2.05), each `rc=0`, nothing registered, **no capstone model
written or run**, no repository model edited or run, no family file
changed. All five are the reviewer's own `/tmp` diagnostics
(`/tmp/tessera-capstone-r3/`) copied **byte for byte** under a
provenance header and re-run on our tree; every `RESULT` line lands at
the line number the reviewer cited. Three of them (`cap11a`–`cap11c`)
are the reviewer's **structural-join rewrite** of the SS.Q3 companion —
the round-two repair of C-Q6's E1 built on a family-model copy: a
front-end mints a fresh intake name and forwards the bundle on private
channels to the standing and envelope paths in parallel; the standing
path destructures the wrapper itself and pins `attemptCore` to the
presentation's own `t`, `ppf` and `sg`. They are the first runs on the
record in which that join exists in any model.

| File | Copy of | Mutation | Result |
|---|---|---|---|
| `cap9_sp2_slots_projection_no_lyr.pv/.out` | `cq1c_sp2_slots_base.pv` | **two layers** (`L0`, `L1`) sharing one intake `aid` and one tuple `t`; slot B reported at `L1` only; the link-2b correspondence stated twice — **projected without `lyr`** (`SlotSatisfied(aid, t, slot)`, as the file permits) and **layer-indexed** (`LayerSlot(aid, lyr, t, slot)`) | projected form **`is true`** (`:1239`) while the layer-indexed form is **`is false`** (`:1454`); every S-P2 query and the three original link-2b conjuncts unchanged (`:483`–`:504`, `:1169`–`:1225`); witnesses reachable (`:675`, `:913`, `:1162`). *The projection can borrow another layer's slot report; it must keep `lyr`* |
| `cap10_ss_q3_scope_report_only.pv/.out` | `cap11b` (the structural join **with** the fingerprint guard) | **only the envelope's reported attribution key changed** (`reportK = pk(dsks(sg, decl))` in place of `kX`) and a scope-agreement judge added that fires `ScopeMisreported(kX, reportK)` when they differ; standing path untouched | **`ScopeMisreported` reachable** (`:779`) while wrapped designation (`:798`, `:811`), the substitution guard (`:817`), entitled-key safety (`:856`) and honest standing (`:1205`) stay green/reachable. *A scope mutation leaves every C-Q6 conjunct green; C-Q6 needs a scope consumer* |
| `cap11a_ss_q3_structural_join.pv/.out` | `s-standing/proverif/ss_q3_companionB_entitled_via_envelope.pv` (C-C12's source) | the **structural join** as above: `Front` process, `standingIn`/`envelopeIn` private channels, `wrap()` destructuring in both paths, `let attemptCore(=t, =ppfI, =sgI, decl) = core`, `EstablishedWrapped(intake, L1, t, kT, core, ESTABLISHED)` emitted by the standing path alone, a `Substituted(core, expected)` guard; **no** fingerprint precondition | wrapped designation **`is false`** (`:735`) as C-C12 requires; honest-key form `is true` (`:749`); **`Substituted` unreachable** (`:756`); `StandingUnentitled` **reachable** (`:1307`); honest standing reachable (`:1657`). *The round-two structural repair works at this projection* |
| `cap11b_ss_q3_structural_join_fp_pin.pv/.out` | `cap11a` | one guard added, `if fp(kX) = kfpr then` — the mapping row's *"with `fp(kX) = kfpr` from `t`"* read as a precondition | wrapped designation **`is true`** (`:495`); `Substituted` unreachable (`:514`); **`StandingUnentitled` unreachable** (`:553`); honest standing reachable (`:902`). *The fingerprint clause, kept anywhere in the join, re-shadows C-C12* |
| `cap11c_ss_q3_structural_join_sg_unpinned.pv/.out` | `cap11b` | the `attemptCore` signature-term pin `=sgI` relaxed to a free `otherSg` (fingerprint guard retained) | **`Substituted` reachable** (`:847`) while wrapped designation stays `is true` (`:495`). *The `sg = sgI` term equality is load-bearing: without it a core over a different signature passes* |

These five results are **not** S-P2 or S-STANDING results and no family
file records them, and they are **not** capstone results — no capstone
model exists. They are the evidence behind the four dispositions of the
round-three record and the repairs to
`formal/suite/capstone/PREDICTIONS.md` recorded in that file's
"Repairs after the 2026-09-17 Codex review, third round" section.

## Eighth batch, 2026-09-17 — the capstone registration's fourth round

Added while dispositioning the **fourth non-author round on the
capstone registration**
(`docs/reviews/2026-09-17-codex-review-capstone-predictions-round4.md`,
two findings, both accepted). Same discipline: copies only, run with
`proverif -lib formal/suite/lib/tessera_theory.pvl` (ProVerif 2.05),
each `rc=0`, nothing registered, **no capstone model written or run**,
no repository model edited or run, no family file changed. All seven
are the reviewer's own `/tmp` diagnostics (`/tmp/tessera-capstone-r4/`)
copied **byte for byte** under a provenance header and re-run on our
tree; every `RESULT` line lands at the line number the reviewer cited.
`cap12a` is the reviewer's construction of the **round-three contract on
the correct S-STANDING strict model**: the structural join of
`cap11a` plus the **paired scope-agreement judge** of C-Q6's conjunct 3,
reading `(aid, lyr, …)` reports from both paths on private channels
(`scopeStanding`, `scopeEnvelope`) and firing `ScopeMisreported` or the
witness `HonestWrappedStandingAgreed`. `cap12b`–`cap12d` are its
controls; `cap12e`–`cap12g` are the two findings.

| File | Copy of | Mutation | Result |
|---|---|---|---|
| `cap12a_ss_q1_join_correct.pv/.out` | `s-standing/proverif/ss_q1_strict_dns_compromised.pv` (correct strict model) | the structural join + paired scope-agreement judge; **all checks correct** | wrapped designation `is true` (`:542`, `:556`); `Substituted` unreachable (`:563`); **`ScopeMisreported` unreachable** (`:570`); identity judge unreachable (`:577`); **`HonestWrappedStandingAgreed` reachable** (`:958`); `StandingUnentitled` unreachable (`:998`); honest standing reachable (`:1348`) |
| `cap12b_ss_q1_join_cc12.pv/.out` | `cap12a` | **C-C12's mutation** — the standing path's `fp(kT) = kfpr` check removed, nothing else | wrapped designation **`is false`** (`:782`), honest-key form `is true` (`:797`); `ScopeMisreported` **unreachable** (`:813`); **`StandingUnentitled` reachable** (`:1762`); agreement witness reachable (`:1204`); honest standing reachable (`:2113`). *D13 still severable beside conjunct 3* |
| `cap12c_ss_q1_join_scope_key.pv/.out` | `cap12a` | **key-scope mutation** — the envelope's attribution report names a DSKS-derived key in place of `kX` when the wrapper identity differs; standing path untouched | **`ScopeMisreported` reachable** (`:947`); every C-Q6 conjunct 1/2 form `is true` (`:548`, `:562`); `StandingUnentitled` unreachable (`:1378`); agreement witness reachable (`:1334`). *Conjunct 3 severable on its own* |
| `cap12d_ss_q1_join_cc12_scope_key.pv/.out` | `cap12b` | both mutations | `ScopeMisreported` reachable (`:1192`) **and** `StandingUnentitled` reachable (`:2140`); agreement witness reachable (`:1581`). *The two severings are independent* |
| `cap12e_ss_q1_join_scope_identity.pv/.out` | `cap12a` | **identity-only scope mutation** — the envelope's attribution report names the **wrapper's identity** `iw` in place of the inner `id`; the key unchanged; a `ScopeIdentityWrong(aid, lyr)` judge added | all three C-Q6 conjuncts green (`:542`, `:556`, **key-only `ScopeMisreported` unreachable `:570`**) while **`ScopeIdentityWrong` reachable** (`:945`); `Substituted` unreachable (`:563`); honest standing reachable (`:1718`). *A key-only judge misses identity-only re-scoping* |
| `cap12f_sp7_q6a_keyjudge.pv/.out` | `s-p7/proverif/sp7_q6a_companion_identity_outermost.pv` (S-P7's identity-from-outermost companion) | **adds** a key-only scope judge (`KeyOnlyScopeWrong`) beside the committed full `Rescoped` query; the companion's mutation unchanged | **key-only judge `is true`** (`:1339`) while the committed **`Rescoped` `is false`** (`:818`); `HonestWrappedAccepted` reachable (`:1130`), `HonestAccepted` reachable (`:1326`). *The family's own companion is exactly the case the key-only judge cannot see* |
| `cap12g_ss_q1_join_terminal_unchecked.pv/.out` | `cap12a` | **S-STANDING Q4's mutation** — `StandingDecide` ignores the terminal disposition and reports `ESTABLISHED` after lineage membership | the wrapped standing correspondence **`is false`**, unrestricted (`:810`) and honest-key (`:1136`) forms alike; S-STANDING's own honest-key forms `is false` too (`:2190`, `:2514`); `Substituted`, `ScopeMisreported`, identity judge unreachable (`:1144`, `:1152`, `:1160`); agreement witness reachable (`:1542`); honest standing reachable (`:2873`); **S2 and S4 vocabulary witnesses unreachable** (`:3217`, `:3413`) — the branches no longer exist, as the committed `ss_q4…out:1708`, `:1838` already records. *C-C11's Q4 alternate must register that disappearance as a consequence* |

These seven results are **not** S-STANDING or S-P7 results and no family
file records them, and they are **not** capstone results — no capstone
model exists. They are the evidence behind the dispositions of the
round-four record and the repairs to
`formal/suite/capstone/PREDICTIONS.md` recorded in that file's
"Repairs after the 2026-09-17 Codex review, fourth round" section.

## Ninth batch, 2026-09-17 — the capstone registration's fifth round

Added while dispositioning the **fifth non-author round on the
capstone registration**
(`docs/reviews/2026-09-17-codex-review-capstone-predictions-round5.md`,
two findings, both accepted). Same discipline: copies only, run with
`proverif -lib formal/suite/lib/tessera_theory.pvl` (ProVerif 2.05),
each `rc=0`, nothing registered, **no capstone model written or run**,
no repository model edited or run, no family file changed. Thirteen are
the reviewer's own `/tmp` diagnostics (`/tmp/tessera-capstone-r5/`)
copied **byte for byte** under a provenance header and re-run on our
tree, every `RESULT` line at the line number the reviewer cited; the
fourteenth (`cap14d`) the reviewer did not make.

| File | Copy of | Mutation | Result |
|---|---|---|---|
| `cap13a_sp2_membership_base.pv/.out` | `cq1c_sp2_slots_base.pv` | the slot report names the **manifest-named** slot `kfprA`/`kfprB` (as the capstone's `LayerAccepted` contract requires; `cq1c` reported `fp(kA)`), and a structural slot-to-key judge `SlotKeyWrong` added; verifier unmutated | all green: four S-P2 queries (`:481`–`:502`), `Spliced` (`:1143`), `PossessionTransplanted` (`:1150`), C-Q9 (`:1157`), three link-2b conjuncts (`:1171`, `:1185`, `:1199`), **slot-to-key `is true`** (`:1206`); witnesses reachable (`:673`, `:899`, `:1136`) |
| `cap13b_sp2_membership_unbound.pv/.out` | `cap13a` | **S-P2 Q4's mutation** — only slot B's `fp(kB) = kfprB` removed on the two-signer branch; every signature, possession, frame and common-content check retained | **slot-to-key `is false`** (`:1972`); **`SignerForged` reachable** (`:730`); **`PossessionTransplanted` reachable** (`:1657`, a consequence the family's Q4 model, which declares no `PossJudge`, could not record); all three link-2b conjuncts `is true` (`:1685`, `:1722`, `:1759`); `Stripped` (`:481`), `SetAltered` (`:739`), `Reattributed` (`:749`), `Spliced` (`:1398`), C-Q9 (`:1666`) green; witnesses reachable (`:922`, `:1150`, `:1389`). *D7's membership half needs its own companion; completeness and content companions do not sever it* |
| `cap14a_sp7_q1_strict_base.pv/.out` | `s-p7/proverif/sp7_q1_strict_dns_compromised.pv`, **unchanged** | none — the committed correct STRICT model re-run | all four queries green (`:560`, `:574`, `:588`, `:602`); `HonestWrappedAccepted` (`:935`), `HonestAccepted` (`:1144`) reachable |
| `cap14b_sp7_q1_strict_q6b.pv/.out` | `cap14a` | **Q6b's mutation transcribed onto the STRICT model** — the inner check inlined, the inner signature verified under the wrapper key `kW`, inner `kfp`/`id`/`mh` read but not matched; both outer authority checks and the same-key wrapper signer retained; DNS leaked | **every query green** — `TypeConfused` (`:541`), `Rescoped` (`:550`), `InnerSigTransplanted` (`:559`), `Reattributed` (`:568`) — and both witnesses reachable (`:843`, `:1047`). *In strict, with no authorized adversary wrapper key, C-C15(i) has nothing to exploit* |
| `cap14c_sp7_q1_strict_repo_q6b.pv/.out` | `cap14b` | the same, repository channel leaked | identical, line for line (`:541`–`:1047`) |
| `cap14d_sp7_q1_strict_q6a.pv/.out` | `cap14a` | **Q6a's mutation transcribed onto the STRICT model** (not the reviewer's run) — the inner check inlined byte for byte, except that the scope report (and `AcceptInner`) name the **wrapper's** identity `idW` instead of the inner `idI`; key retained | **`Rescoped` reachable** (`:892`; trace `:880-892`: honest wrapper `skW2` wraps I2's honest attestation and the inner is attributed to `(pk(skI2), idW2)`, the **honest-only route**); `InnerSigTransplanted` (`:906`), `Reattributed` (`:920`), `TypeConfused` (`:558`) green; witnesses reachable (`:1185`, `:1394`). *Configuration (iii) fires in strict where (i) cannot; D11's strict discharge rests on it* |
| `cap15a_ss_q1_pairjudge_correct.pv/.out` | `cap12a` | the paired scope judge now compares the **`(key, identity)` pair** — conjunct 3 in its round-4 form; all checks correct | pair mismatch unreachable (`:570`), unentitled unreachable (`:998`), substitution excluded (`:563`), agreement witness reachable (`:958`); five vocabulary witnesses reachable (`:1685`–`:2775`) |
| `cap15b_ss_q1_pairjudge_identity.pv/.out` | `cap15a` | **identity-only** scope mutation, with a separate **key-only** judge kept as a control | **pair mismatch reachable** (`:953`) while the key-only control stays **green** (`:576`); unentitled unreachable (`:1746`); agreement witness reachable (`:1706`). *The identity comparison is what fires* |
| `cap15c_ss_q1_pairjudge_key.pv/.out` | `cap15a` | key-only scope mutation | pair mismatch reachable (`:947`); unentitled unreachable (`:1378`); witness reachable (`:1334`) |
| `cap15d_ss_q1_pairjudge_cc12.pv/.out` | `cap15a` | C-C12's mutation only | pair mismatch unreachable (`:813`); **unentitled reachable** (`:1762`); witness reachable (`:1204`) |
| `cap15e_ss_q1_pairjudge_cc12_key.pv/.out` | `cap15d` | C-C12's mutation plus the key-scope mutation | both reachable (`:1192`, `:2140`); witness reachable (`:1581`) |
| `cap16a_ss_q1_pairjudge_cc11_declared.pv/.out` | `cap15a` | **C-C11 proper** — S-STANDING Q2's mutation, the TLR names attempts by labels read from the bundle | standing correspondences red (`:766`, `:1012`, `:1696`, `:1942`, `:2188`); scope conjunct green (`:1026`); honest standing (`:2581`), agreement witness (`:1450`) and **all five vocabulary witnesses** (`:2826`, `:3067`, `:3258`, `:3497`, `:3738`) reachable |
| `cap16b_ss_q1_pairjudge_cc11_unsigned.pv/.out` | `cap15a` | **C-C11 alternate abl6** — the TLR unsigned | the same shape: correspondences red (`:762`–`:2156`); honest standing (`:2548`), agreement witness (`:1436`) and all five vocabulary witnesses (`:2790`–`:3665`) reachable |
| `cap16c_ss_q1_pairjudge_cc11_terminal.pv/.out` | `cap15a` | **C-C11 alternate Q4** — terminal disposition unchecked | correspondences red (`:810`–`:2514`); honest standing (`:2873`) and agreement witness (`:1542`) reachable; **S2 and S4 unreachable** (`:3217`, `:3413`), the other three vocabulary witnesses reachable (`:3208`, `:3404`, `:3652`). *Exactly the registered consequence, nothing else* |

These fourteen results are **not** S-P2, S-P7 or S-STANDING results and
no family file records them, and they are **not** capstone results — no
capstone model exists. They are the evidence behind the dispositions of
the round-five record and the repairs to
`formal/suite/capstone/PREDICTIONS.md` recorded in that file's
"Repairs after the 2026-09-17 Codex review, fifth round" section.

## Tenth batch, 2026-09-17 — the capstone registration's sixth round

Added while dispositioning the **sixth non-author round on the
capstone registration**
(`docs/reviews/2026-09-17-codex-review-capstone-predictions-round6.md`,
six findings, all accepted). Same discipline: copies only, run with
`proverif -lib formal/suite/lib/tessera_theory.pvl` (ProVerif 2.05),
each `rc=0`, nothing registered, **no capstone model written or run**,
no repository model edited or run, no family file changed. Fourteen are
the reviewer's own `/tmp` diagnostics (`/tmp/tessera-capstone-r6/`)
copied **byte for byte** under a provenance header and re-run on our
tree, every `RESULT` line at the line number the reviewer cited; four
(`*_repo`) the reviewer did not make — the **repository-compromised
variants** of `cap14d` and `cap16a/b/c`, differing from their DNS
variants by one line (`out(c, skR)` for `out(c, skD)`), which finding 5
asked for so that case (b) is descended rather than asserted.

**The lesson of this batch, recorded so it is not relearned:** the
round-five repair filled strict-case cells by reading degraded traces;
four of those readings were wrong. **A strict outcome is descended by a
strict run or it is predicted.** Every strict cell in the registration
now cites a file in this batch.

| File | Copy of | Mutation | Result |
|---|---|---|---|
| `cap17a_sp1_strict_judges_base.pv/.out` | `s-p1/proverif/sp1_q1_strict_dns_compromised.pv` | **strict** S-P1 with the C-Q7 judge, both C-Q8 judges and the same-key `OT_WRAPPER` signer added (the `cap7a` additions, on the strict model); all checks correct | all green: C-Q7 (`:338`), both C-Q8 (`:344`, `:350`), honest-key authorship (`:358`), unrestricted authorship (`:555`); witness reachable (`:547`) |
| `cap17b_sp1_strict_cc7i.pv/.out` | `cap17a` | **C-C7(i)** same-key byte unbinding | **C-Q7 green** (`:340`); **both C-Q8 red** (`:533`, `:709`); **honest-key authorship red** (`:887`); unrestricted red (`:1243`); witness reachable (`:1079`). *Mixed, not a green control* |
| `cap17c_sp1_strict_cc7ii.pv/.out` | `cap17a` | **C-C7(ii)** type-conditional byte unbinding | the same shape: C-Q7 green (`:375`); both C-Q8 red (`:570`, `:748`); authorship red (`:928`); witness reachable (`:1118`) |
| `cap17d_sp1_strict_cc10_drop_compromised.pv/.out` | `cap17a` | **C-C10 with the COMPROMISED channel's evidence check removed**; a publication-provenance correspondence (link 1b's shape) added | **everything green**, including provenance (`:547`) and unrestricted authorship (`:539`); witness reachable (`:531`). *Removing the forgeable channel's check severs nothing* |
| `cap17e_sp1_strict_cc10_drop_honest.pv/.out` | `cap17a` | **C-C10 with the HONEST channel's evidence check removed** | **provenance red** (`:858`), **unrestricted authorship red** (`:699`); honest-key authorship (`:355`), C-Q7 and both C-Q8 (`:335`, `:341`, `:347`) green; witness reachable (`:540`). *This is C-C10's strict form* |
| `cap18a_sp2_strict_cc2.pv/.out` | `m4_framepin_mh.pv` (C-C2's source) | the second, uncompromised authority process and check added (**strict**, DNS leaked); C-C2's mutation retained | **all green** — `Stripped` (`:411`), `SignerForged` (`:424`), `SetAltered` (`:437`), `Reattributed` (`:450`), `Spliced` (`:1129`); witnesses reachable (`:633`, `:869`, `:1116`). *C-C2 is a green control in strict* |
| `cap18b_sp2_strict_cc3.pv/.out` | `s-p2/proverif/sp2_q5_c2_fponly_frame_nomh.pv` (C-C3's source) | made strict the same way | **all green** (`:381`, `:388`, `:395`, `:402`); witnesses reachable (`:578`, `:809`, `:1051`); this source declares no `Spliced` query, so C-C3's `Spliced` green in strict is predicted, not descended. *C-C3 is a green control in strict; matches S-P2's own strict ablation d9* |
| `cap18c_sp2_strict_cc8.pv/.out` | `d10b_sp2_q9_manifest_unbound.pv` (C-C8's source) | made strict the same way | **mixed**: `SetAltered` green (`:509`), `PossessionTransplanted` green (`:1202`), **C-Q9 red** (`:1431`); the rest green (`:487`, `:498`, `:520`, `:1191`); witnesses reachable (`:701`, `:935`, `:1180`). *C-C8's (β) obligation reds in strict, its (α) does not* |
| `cap18d_sp2_strict_cc16.pv/.out` | `cap1_sp2_content_unchecked.pv` (C-C16's source) | made strict the same way | **`Spliced` red** (`:1430`); link-2b conjuncts green (`:1456`, `:1468`, `:1480`); the rest green; witnesses reachable (`:701`, `:942`, `:1194`). *C-C16's strict red reproduces, by a route other than cap1's displayed trace* |
| `cap18e_sp2_strict_cc17.pv/.out` | `cap13b_sp2_membership_unbound.pv` (C-C17's source) | made strict the same way | **`SignerForged` red** (`:775`), **`PossessionTransplanted` red** (`:1754`), **slot-to-key red** (`:2086`); link-2b conjuncts green (`:1781`, `:1813`, `:1845`); witnesses reachable (`:981`, `:1222`, `:1474`). *C-C17 reds in strict as in degraded* |
| `cap19a_sp7_strict_both_leaked_base.pv/.out` | `cap14a` (correct strict S-P7) | **both** channel keys leaked — case (c) | all four queries green (`:562`, `:576`, `:589`, `:603`); witnesses reachable (`:927`, `:1139`) |
| `cap19b_sp7_strict_both_leaked_q6b.pv/.out` | `cap14b` (Q6b on strict) | both keys leaked — C-C15(i) in case (c) | **`Rescoped`** (`:843`), **`InnerSigTransplanted`** (`:1151`), **`Reattributed`** (`:1450`) reachable; witnesses reachable (`:1728`, `:1935`). *The attacker's authorized wrapper key restores the attack; (c) is not (a)/(b)* |
| `cap19c_sp7_strict_frame_judge_base.pv/.out` | `cap14a` | a literal **inner-frame-field judge** added — frame identity vs tuple identity, frame fingerprint vs accepting key: link 6b as the file wrote it | judge green (`:587`); all else as `cap14a` |
| `cap19d_sp7_strict_frame_judge_q6a.pv/.out` | `cap14d` (Q6a on strict) | the same judge on the identity-from-outermost mutant | **judge still green** (`:585`) while **`Rescoped` red** (`:933`); witnesses reachable (`:1226`, `:1435`). *Link 6b as written cannot see the attribution Q6a changes* |
| `cap14d_sp7_q1_strict_q6a_repo.pv/.out` | `cap14d` | the repository key leaked instead of the DNS key | `Rescoped` red (`:893`); `:907`, `:921`, `:558` green; witnesses (`:1186`, `:1395`). *Case (b) of C-C15(iii), descended* |
| `cap16a_…_cc11_declared_repo`, `cap16b_…_cc11_unsigned_repo`, `cap16c_…_cc11_terminal_repo` `.pv/.out` | `cap16a`, `cap16b`, `cap16c` | the repository key leaked instead of the DNS key | **RESULT polarities identical query for query** to the DNS variants — `cap16a_repo` and `cap16c_repo` at the same line numbers, `cap16b_repo` offset by **+1** from its third `RESULT` line onward (`:1009`, `:1016`, `:1023`, `:1437` … against the DNS `:1008`, `:1015`, `:1022`, `:1436` …). *Case (b) of C-C11's three forms, descended. C-C12 has no `_repo` run, so its (b) stays predicted* |

These eighteen results are **not** family results and no family file
records them, and they are **not** capstone results — no capstone model
exists. They are the evidence behind the dispositions of the round-six
record and the repairs to `formal/suite/capstone/PREDICTIONS.md`
recorded in that file's "Repairs after the 2026-09-17 Codex review,
sixth round" section.

## Eleventh batch, 2026-09-17 — the capstone registration's seventh round

Added while dispositioning the **seventh non-author round on the
capstone registration**
(`docs/reviews/2026-09-17-codex-review-capstone-predictions-round7.md`,
two findings, both accepted). Same discipline: copies only, run with
`proverif -lib formal/suite/lib/tessera_theory.pvl` (ProVerif 2.05),
each `rc=0`, nothing registered, **no capstone model written or run**,
no repository model edited or run, no family file changed. All seven
are the reviewer's own `/tmp` diagnostics (`/tmp/tessera-capstone-r7/`)
copied **byte for byte** under a provenance header and re-run on our
tree, every `RESULT` line at the line number the reviewer cited.

**The lesson of this batch:** a family copy's declared queries are not
the capstone's query set. `cap18b` (C-C3 strict) declared no C-Q9;
`cap17d` (C-C10's control) declared no link-1a judge; both were read as
all-green controls. Adding the missing judge reds each.

| File | Copy of | Mutation | Result |
|---|---|---|---|
| `cap20a_sp2_strict_cc3_q9.pv/.out` | `cap18b_sp2_strict_cc3.pv` (C-C3 strict) | the per-slot possession report and the **C-Q9 structural judge** (`PossessionUnbound`) added; fixture and verifier unchanged | **C-Q9 red** (`:1319`) while `Stripped`, `SignerForged`, `SetAltered`, `Reattributed` stay green (`:414`, `:422`, `:430`, `:439`); witnesses reachable (`:616`, `:848`, `:1091`). *C-C3 in strict is mixed: (α) set integrity green, (β) possession-message relation red* |
| `cap20b_sp2_strict_cc3_q9_poss_restored.pv/.out` | `cap20a` | possession-over-tuple **restored**; the frame's manifest-hash guard still absent | **C-Q9 green** (`:1098`); the four safety queries green (`:414`–`:438`); witnesses reachable (`:615`, `:847`, `:1090`). *The red is the fingerprint-only possession, not the missing hash guard* |
| `cap20c_sp1_strict_base_evidence_either.pv/.out` | `cap17a_sp1_strict_judges_base.pv` | a structural **link-1a judge** over the accepted evidence term, accepting evidence that verifies over the consumed tuple under **either** authority key | judge green (`:585`); all else as `cap17a` (`:362`–`:382`, `:571`, `:579`) |
| `cap20d_sp1_strict_base_evidence.pv/.out` | `cap17a` | the same judge in its **channel-specific** form (each carried term under its own channel key) | judge green (`:589`); all else as `cap17a` |
| `cap20e_sp1_strict_cc10_drop_compromised_either.pv/.out` | `cap17d_sp1_strict_cc10_drop_compromised.pv` (C-C10's isolation control) | the either-key link-1a judge added | **link-1a judge red** (`:732`) while publication provenance (`:572`) and unrestricted authorship (`:564`) stay green; witness reachable (`:556`). *The control is mixed, not green* |
| `cap20f_sp1_strict_cc10_drop_compromised_evidence.pv/.out` | `cap17d` | the channel-specific link-1a judge added | **red** (`:737`); provenance green (`:577`); witness reachable (`:560`) |
| `cap20g_sp1_strict_cc10_drop_honest_evidence.pv/.out` | `cap17e_sp1_strict_cc10_drop_honest.pv` (C-C10's strict form) | the channel-specific link-1a judge added | **link 1a red** (`:1055`) beside link 1b (`:887`) and unrestricted authorship (`:728`) red; honest-key authorship (`:384`), C-Q7 and both C-Q8 (`:364`–`:376`) green; witness reachable (`:569`) |

These seven results are **not** S-P1 or S-P2 results and no family file
records them, and they are **not** capstone results — no capstone model
exists. They are the evidence behind the dispositions of the
round-seven record and the repairs to
`formal/suite/capstone/PREDICTIONS.md` recorded in that file's
"Repairs after the 2026-09-17 Codex review, seventh round" section.

## Twelfth batch, 2026-09-17 — the capstone registration's eighth round

Added while dispositioning the **eighth non-author round on the
capstone registration**
(`docs/reviews/2026-09-17-codex-review-capstone-predictions-round8.md`,
two findings, both accepted). Same discipline: copies only, run with
`proverif -lib formal/suite/lib/tessera_theory.pvl` (ProVerif 2.05),
each `rc=0`, nothing registered, **no capstone model written or run**,
no repository model edited or run, no family file changed. All five are
the reviewer's own `/tmp` diagnostics (`/tmp/tessera-capstone-r8/`)
copied **byte for byte** under a provenance header and re-run on our
tree, every `RESULT` line at the line number the reviewer cited.

| File | Copy of | Mutation | Result |
|---|---|---|---|
| `cap21a_sp7_strict_base_sigbytes.pv/.out` | `cap14a_sp7_q1_strict_base.pv` (correct strict S-P7) | **C-Q8's structural signature/bytes judge** (`BytesUnbound`) added over every accepted `(key, signature, presented bytes)` triple; nothing else | judge green (`:592`); the four S-P7 queries green (`:606`–`:648`); witnesses reachable (`:981`, `:1190`) |
| `cap21b_sp7_strict_base_sigbytes_wrapped.pv/.out` | `cap21a` | the judge **restricted to wrapped inner acceptances** (the report carries the wrapper context) | judge green (`:594`); the rest as `cap21a` (`:610`–`:658`, `:993`, `:1204`) |
| `cap21c_sp7_strict_cc5.pv/.out` | `cap21a` | **C-C5's mutation**: `let (=BYTES, =fbI) = checksign(sgI, kI)` becomes `let (=BYTES, anyb) = …` inside `InnerCheck`; strict, DNS leaked | **judge red** (`:808`) while `TypeConfused`, `Rescoped`, `InnerSigTransplanted`, `Reattributed` stay green (`:832`–`:904`); witnesses reachable (`:1250`, `:1472`) |
| `cap21d_sp7_strict_cc5_wrapped.pv/.out` | `cap21b` | C-C5's mutation, judge restricted to wrapped inner acceptances | **judge red** (`:869`); the four S-P7 queries green (`:898`, `:927`, `:956`, `:985`); witnesses reachable (`:1336`, `:1563`). *In strict, C-C5 reds C-Q8/link 4 through an honest wrapper signature under an honestly authorized key; `InnerSigTransplanted` stays green. Mixed, not a green control* |
| `cap21e_sp7_strict_cc5_wrapped_repo.pv/.out` | `cap21d` | the repository key leaked instead of the DNS key | the same: judge red (`:868`); S-P7 queries green (`:897`–`:982`); witnesses reachable (`:1333`, `:1559`). *Case (b), descended* |

These five results are **not** S-P7 results and no family file records
them, and they are **not** capstone results — no capstone model exists.
They are the evidence behind the dispositions of the round-eight record
and the repairs to `formal/suite/capstone/PREDICTIONS.md` recorded in
that file's "Repairs after the 2026-09-17 Codex review, eighth round"
section.

## Thirteenth batch, 2026-09-17 — the capstone registration's ninth round

Added while dispositioning the **ninth non-author round on the
capstone registration**
(`docs/reviews/2026-09-17-codex-review-capstone-predictions-round9.md`,
three findings, all accepted, plus the requested C-C6 test). Same
discipline: copies only, run with `proverif -lib
formal/suite/lib/tessera_theory.pvl` (ProVerif 2.05), each `rc=0`,
nothing registered, **no capstone model written or run**, no repository
model edited or run, no family file changed. All ten are the reviewer's
own `/tmp` diagnostics (`/tmp/tessera-capstone-r9/`) copied **byte for
byte** under a provenance header and re-run on our tree, every `RESULT`
line at the line number the reviewer cited.

| File | Copy of | Mutation | Result |
|---|---|---|---|
| `cap22a_sp7_strict_cc6_base.pv/.out` | `cap21b_sp7_strict_base_sigbytes_wrapped.pv`, **unchanged** | none — the baseline for the C-C6 question | all green (`:594`–`:658`); witnesses reachable (`:993`, `:1204`) |
| `cap22b_sp7_strict_cc6.pv/.out` | `cap22a` | **C-C6's conditional byte unbinding** inside `InnerCheck` (byte equality demanded only when the signed frame's own `kfp` matches the verifying key); same-key wrapping retained; DNS leaked | **all green** — wrapped C-Q8 (`:692`), `TypeConfused` (`:722`), `Rescoped` (`:752`), `InnerSigTransplanted` (`:782`), `Reattributed` (`:812`); witnesses reachable (`:1161`, `:1386`). *C-C5's strict route does not open under C-C6: the same-key wrapper frame names the verifying key, so equality is demanded* |
| `cap22c_sp7_strict_cc6_repo.pv/.out` | `cap22b` | the repository key leaked instead | the same (`:693`–`:817`, `:1167`, `:1393`) |
| `cap22d_sp7_strict_base_q9.pv/.out` | `cap14a_sp7_q1_strict_base.pv` | the **C-Q9 structural possession judge** added, firing including on verification failure; the inner acceptance reports its checked inner `(kI, tI, ppfI)` | C-Q9 green (`:1186`); all else as `cap14a` (`:588`–`:630`, `:963`, `:1172`) |
| `cap22e_sp7_strict_q6b_q9_inner.pv/.out` | `cap14b_sp7_q1_strict_q6b.pv` (C-C15(i) on strict) | the C-Q9 judge added; the inner acceptance reports the **presented inner** `(kW, tI, ppfI)` — the terms it was about, never checked by this mutant | **C-Q9 red** (`:1334`) while the four S-P7 queries stay green (`:569`–`:596`) and witnesses reachable (`:871`, `:1075`) |
| `cap22f_sp7_strict_q6b_q9_inner_repo.pv/.out` | `cap22e` | the repository key leaked instead | the same (`:1334`; `:569`–`:596`; `:871`, `:1075`). *Case (b), descended* |
| `cap22g_sp7_strict_q6b_q9_outer.pv/.out` | `cap22e` | the inner acceptance reports the **checked outer** `(kW, tW, ppfW)` instead | **C-Q9 green** (`:1084`). *The rejected report reading: it hides the companion's failure by reporting what the verifier did check* |
| `cap22h_sp2_strict_cc8_mh.pv/.out` | `cap18c_sp2_strict_cc8.pv` (C-C8 strict) | a judge reporting each accepted slot's `(t, frame)` and firing on **`mh ≠ h(t)`** added | **manifest-hash judge green** (`:1478`) while C-Q9 stays red (`:1466`); the rest green (`:512`–`:549`, `:1224`, `:1236`); witnesses reachable (`:731`, `:966`, `:1212`) |
| `cap22i_sp2_strict_cc8_mh_repo.pv/.out` | `cap22h` | the repository key leaked instead | the same (`:1477`; `:1465`; witnesses `:730`, `:965`, `:1211`) |
| `cap22j_sp2_degraded_cc8_mh.pv/.out` | `d10b_sp2_q9_manifest_unbound.pv` (C-C8's degraded source) | the same manifest-hash judge, as the control | **judge red** (`:1665`), `SetAltered` red (`:701`), C-Q9 red (`:1499`); witnesses reachable (`:882`, `:1105`, `:1311`). *In degraded the dropped guard is exploitable; in strict the honest channel's tuple pin keeps `mh = h(t)`* |

These ten results are **not** S-P7 or S-P2 results and no family file
records them, and they are **not** capstone results — no capstone model
exists. They are the evidence behind the dispositions of the round-nine
record and the repairs to `formal/suite/capstone/PREDICTIONS.md`
recorded in that file's "Repairs after the 2026-09-17 Codex review,
ninth round" section.

## Fourteenth batch, 2026-09-17 — the capstone registration's tenth round

Added while dispositioning the **tenth non-author round on the capstone
registration**
(`docs/reviews/2026-09-17-codex-review-capstone-predictions-round10.md`,
two findings, both accepted). Same discipline: copies only, run with
`proverif -lib formal/suite/lib/tessera_theory.pvl` (ProVerif 2.05),
each `rc=0`, nothing registered, **no capstone model written or run**,
no repository model edited or run, no family file changed. All eight are
the reviewer's own `/tmp` diagnostics (`/tmp/tessera-capstone-r10/`)
copied **byte for byte** under a provenance header and re-run on our
tree, every `RESULT` line at the line number the reviewer cited.

| File | Copy of | Mutation | Result |
|---|---|---|---|
| `cap23a_sp7_strict_base_observers.pv/.out` | `cap14a_sp7_q1_strict_base.pv` (correct strict S-P7) | five **structural observers on the inner acceptance's reported terms** added — link 1b (the inner tuple has a prior authority publication), link 5 (inner frame `mh = h(tI)`), link 2a's primary-slot relation (`fp(k) = kfpr`), link 1a (presented inner evidence verifies over `tI`), C-Q5's relation (an honest accepting key reports its sole signed manifest) — plus the C-Q9 judge; nothing else | all green (`:1302`, `:1325`, `:1339`, `:1353`, `:1367`, `:1381`); the four S-P7 queries green (`:700`–`:742`); witnesses reachable (`:1077`, `:1288`) |
| `cap23b_sp7_strict_base_observers_tuple.pv/.out` | `cap23a` | the reports restricted to well-formed `authTuple` terms | all green (`:1306`, `:1329`, `:1343`, `:1357`, `:1371`, `:1385`); witnesses (`:1081`, `:1292`) |
| `cap23c_sp7_strict_q6b_observers.pv/.out` | `cap23a` | **C-C15(i)'s mutation** (Q6b on strict): outer tuple, evidence and possession checked, inner signature verified under `kW`, the presented inner tuple and evidence unchecked; the inner acceptance **reports the presented inner terms** per §1.3's contract; DNS leaked | **C-Q9 red** (`:1471`), **link 1b red** (`:1727`), **link 5 `mh` red** (`:1987`), **link 2a red** (`:2267`), **link 1a red** (`:2523`), **C-Q5 red** (`:2811`); the four S-P7 queries green (`:682`–`:712`); witnesses reachable (`:996`, `:1203`) |
| `cap23d_sp7_strict_q6b_observers_tuple.pv/.out` | `cap23c` | reports restricted to well-formed tuples | the same: `:1459`, **`:1735`, `:2017`, `:2297`, `:2573`, `:2883`** red; `:686`–`:716` green; witnesses `:992`, `:1199`. *The route needs no adversary key: an honest same-key wrapper's valid inner signature and outer credentials retained, the presented inner tuple and evidence replaced* |
| `cap23e_sp7_strict_q6b_observers_repo.pv/.out` | `cap23c` | the repository key leaked instead | identical line for line to `cap23c` |
| `cap23f_sp7_strict_q6b_observers_tuple_repo.pv/.out` | `cap23d` | the repository key leaked instead | identical line for line to `cap23d` (`:1735`, `:2017`, `:2297`, `:2573`, `:2883` red). *Case (b), descended* |
| `cap23g_sp7_strict_type_base.pv/.out` | `s-p7/proverif/sp7_q2_degraded_compromised.pv` — **DEGRADED, sole channel leaked, NOT the strict model; the file name is wrong and is kept so cites stay stable** *(corrected 2026-09-17 after the round-10 repair step caught it)* | separate structural observers for the **inner** frame's type relation and the **outer** wrapper's type relation (the A5.5 version judge carried) | both green (`:1111`, `:1124`); `VersionLied` green (`:1098`); the rest as `cap14a` |
| `cap23h_sp7_strict_type_outer.pv/.out` | the reviewer's own `type_outer` diagnostic — the same **degraded** model as `cap23g` (not a one-line edit of it: 229 vs 407 lines; the A5.5 version judge dropped) *(corrected 2026-09-17, as above)* | **ablation a10's mutation** — the outer `=OT_WRAPPER` equality relaxed, the inner `=OT_ATTEST` retained (C-C13(ii)) | **inner type relation green** (`:1313`) while the **outer is red** (`:1520`); `TypeConfused` red in aggregate (`:749`); witnesses reachable (`:1100`, `:1298`). *The type failure is at the wrapper layer only. Degraded run: this descends C-C13(ii)'s case (d); its strict cases stay predicted* |

These eight results are **not** S-P7 results and no family file records
them, and they are **not** capstone results — no capstone model exists.
They are the evidence behind the dispositions of the round-ten record
and the repairs to `formal/suite/capstone/PREDICTIONS.md` recorded in
that file's "Repairs after the 2026-09-17 Codex review, tenth round"
section.

## Fifteenth batch, 2026-09-17 — the capstone registration's eleventh round

Added while dispositioning the **eleventh non-author round on the
capstone registration**
(`docs/reviews/2026-09-17-codex-review-capstone-predictions-round11.md`,
one finding, accepted). Same discipline: copies only, run with
`proverif -lib formal/suite/lib/tessera_theory.pvl` (ProVerif 2.05),
each `rc=0`, nothing registered, **no capstone model written or run**,
no repository model edited or run, no family file changed. All three
are the reviewer's own `/tmp` diagnostics (`/tmp/tessera-capstone-r11/`)
copied **byte for byte** under a provenance header and re-run on our
tree, every `RESULT` line at the line number the reviewer cited. (The
reviewer's directory also held an uncited `cc4_strict` probe and the
intermediate `base`/`q6b` copies carrying an exploratory link-2b
completeness projection that the reviewer expressly declined to count
as a finding; they are preserved in the owner's session scratchpad and
not archived here.)

| File | Copy of | Mutation | Result |
|---|---|---|---|
| `cap24a_sp7_strict_base_member.pv/.out` | `cap23b_sp7_strict_base_observers_tuple.pv` (correct strict S-P7 with the round-10 observers) | **S-P2's membership observer** added — the registered `MemberJudge` relation: an honest `(key, manifest)` paired with the reported `(tuple, slot fingerprint, accepting key)`, `SignerForged` firing when another key satisfies that honest signer's slot | **`SignerForged` unreachable** (`:1421`); the four S-P7 queries green (`:726`–`:768`); witnesses reachable (`:1103`, `:1314`) |
| `cap24b_sp7_strict_q6b_member.pv/.out` | `cap23d_sp7_strict_q6b_observers_tuple.pv` (C-C15(i) on strict, presented inner terms reported) | the same membership observer; DNS leaked | **`SignerForged` reachable** (`:3211`; trace `:3199-3211`: `SignerForged(M2, pk(skI1))` — the wrapper key `skI1` reported as satisfying issuer 2's manifest slot); S-P7 queries green (`:708`–`:738`); witnesses reachable (`:1014`, `:1221`) |
| `cap24c_sp7_strict_q6b_member_repo.pv/.out` | `cap24b` | the repository key leaked instead | identical line for line (`:3211`). *Case (b), descended* |

These three results are **not** S-P7 results and no family file records
them, and they are **not** capstone results — no capstone model exists.
They are the evidence behind the disposition of the round-eleven record
and the repair to `formal/suite/capstone/PREDICTIONS.md` recorded in
that file's "Repairs after the 2026-09-17 Codex review, eleventh round"
section.

## Sixteenth batch, 2026-09-17 — the capstone registration's twelfth round (no finding)

Added after the **twelfth non-author round on the capstone
registration**
(`docs/reviews/2026-09-17-codex-review-capstone-predictions-round12.md`),
which found **no new run-backed defect**, re-ran all 87 archived
`cap5`–`cap24` copies with every `RESULT` matching, and judged the file
ready to freeze subject to the author's items. Same discipline as every
batch. All four are the reviewer's own `/tmp` diagnostics
(`/tmp/tessera-capstone-r12-4akx1iw4/`) copied **byte for byte** under a
provenance header and re-run on our tree, every `RESULT` line at the
line number the reviewer cited. They are controls, not findings: they
let two of C-C15(i)'s strict *predicted* greens become *descended*.

| File | Copy of | Mutation | Result |
|---|---|---|---|
| `cap25a_sp7_strict_q6b_sigjudges.pv/.out` | `cap24b_sp7_strict_q6b_member.pv` (C-C15(i) on strict, presented inner terms reported, membership observer) | a **signature-term observer** (C-Q7's relation) and a **structural byte-binding observer** (C-Q8's relation) added; DNS leaked | **both green** (`:1306`, `:1317`); the four S-P7 queries green (`:777`–`:810`); witnesses reachable (`:1087`, `:1295`); `SignerForged` red as in `cap24b` (`:3315`) |
| `cap25b_sp7_strict_q6b_sigjudges_repo.pv/.out` | `cap25a` | the repository key leaked instead | the same (`:1306`, `:1317` green; `:3314` red). *Case (b), descended* |
| `cap25c_sp7_strict_q6b_sigjudges_bytes_control.pv/.out` | `cap25a` | the inner signature unbound from the presented bytes — the byte observer's negative control | **byte observer red** (`:2249`); signature-term observer green (`:1948`); `Rescoped` and `Reattributed` red (`:1106`, `:1446`); witnesses reachable (`:1727`, `:1936`) |
| `cap25d_sp7_strict_q6b_sigjudges_transplant_control.pv/.out` | `cap25a` | both channel keys leaked (case (c)) — the signature-term observer's negative control | **signature-term observer red** (`:2505`); byte observer green (`:2517`); `Rescoped`, `InnerSigTransplanted`, `Reattributed` red (`:1088`, `:1399`, `:1701`); witnesses reachable (`:1982`, `:2194`) |

These four results are **not** S-P7 results and no family file records
them, and they are **not** capstone results — no capstone model exists.

## Seventeenth batch, 2026-09-17 — the capstone registration's thirteenth round (post-skeptic confirmation)

Added while dispositioning the **thirteenth non-author round**
(`docs/reviews/2026-09-17-codex-review-capstone-predictions-round13.md`,
three bounded corrections of the skeptic repair). Same discipline as
every batch. All four are the reviewer's own `/tmp` diagnostics
(`/tmp/tessera-capstone-r13-w3lu9otg/`) copied **byte for byte** under a
provenance header and re-run on our tree, every `RESULT` line at the
line number the reviewer cited.

| File | Copy of | Mutation | Result |
|---|---|---|---|
| `cap26a_sp3_degraded_publication_baseline.pv/.out` | `s-p3/proverif/sp3_q2_degraded_compromised.pv`, **unmutated** | link 1b's publication-provenance correspondence added as an observer; nothing else | **`is false`** (`:676`) on the unmutated degraded baseline; `HonestAccepted` reachable (`:376`). *Link 1b is a degraded baseline cost, not a severing; it belongs in no degraded companion set* |
| `cap26b_ss_q1_pairjudge_correct_observers.pv/.out` | `cap15a_ss_q1_pairjudge_correct.pv` | the two registered isolation observers `ScopeKeyOnly(aid, lyr, kX, kA)` / `ScopeIdentityOnly(aid, lyr, id, idA)` declared beside the six-place pair judge; correct checks | pair judge, identity observer, key observer all unreachable (`:576`, `:583`, `:590`); witnesses reachable (`:971`, `:1361`) |
| `cap26c_ss_q1_pairjudge_identity_observers.pv/.out` | `cap15b_ss_q1_pairjudge_identity.pv` (identity-only scope mutation) | the same two observers | pair judge red (`:959`), **identity observer red** (`:1334`), key observer green (`:1341`); witnesses (`:1719`, `:2109`) |
| `cap26d_ss_q1_pairjudge_key_observers.pv/.out` | `cap15c_ss_q1_pairjudge_key.pv` (key-only scope mutation) | the same two observers | pair judge red (`:955`), **key observer red** (`:1340`), identity observer green (`:963`); witnesses (`:1719`, `:2114`). *Each observer fires on exactly its own half* |

These four results are **not** family results and no family file
records them, and they are **not** capstone results — no capstone model
exists.

## Eighteenth batch, 2026-09-18 — the capstone registration's `REFUSAL`-fork amendment (author ruling (i), scoped)

Added while entering the **author's ruling of 2026-09-18** on the
capstone registration's one routed item (`PREDICTIONS.md` §8 item 1:
the `REFUSAL` tag, option (i), scoped — an honest `REFUSAL`-tagged
signer as a foreign-tag source, nothing about the refusal record). Same
discipline as every batch: copies only, run with `proverif -lib
formal/suite/lib/tessera_theory.pvl` (ProVerif 2.05), each `rc=0`,
seconds each, nothing registered by a run, **no capstone model written
or run**, no repository model edited or run, no family file changed.
Two are the 2026-09-06 cross-family reviewer's **committed** scratch
fixtures (`s-standing/proverif/falsification-2026-09-06/scratch/`, item
27 of that review) copied **byte for byte** under a provenance header
and re-run on our tree, the reviewer's cited `RESULT` landing at his
line (`a_foreign_tag.out:1953` ↔ `cap27a…out:1953`); four are copies of
the **committed** strict and degraded S-STANDING models as they stand
today with the same foreign-tag signer and the D-6 tag judge added.

| File | Copy of | Mutation | Result |
|---|---|---|---|
| `cap27a_ss_foreign_tag_reviewer_fixture.pv/.out` | `scratch/a_foreign_tag.pv`, **unchanged** | none — strict (DNS leaked), honest `sign((REFUSAL, body), skH1)` over a TLR-shaped body, verifier unchanged | (i) `is true` (`:469`); (ii) `is true` (`:479`, `:489`); (iii) unreachable (`:496`); witnesses reachable (`:793`–`:1939`); the attack unreachable (`:1953`) |
| `cap27b_ss_foreign_tag_reviewer_tlr_tag_unbound.pv/.out` | `scratch/m_foreign_tlr_tag.pv`, **unchanged** | the reviewer's mutant — **only** the standing path's `TLR` tag check unbound | (i) **`is false`** (`:595`); (ii) `skH1` **`is false`** (`:734`), `skH2` `is true` (`:744`); (iii) unreachable (`:751`); witnesses reachable (`:1048`–`:2194`); the attack **reachable** (`:2340`) |
| `cap27c_ss_q1_strict_foreign_tag_correct.pv/.out` | `s-standing/proverif/ss_q1_strict_dns_compromised.pv` (committed) | `ForeignIssuer(skH1)` + private `tagCh` + `TagJudge` / `TagConfused` added; the standing path reports the parsed tag in parallel with its continuation; **no check changed** | all S-STANDING queries as committed (`:529`–`:556`); witnesses (`:855`–`:2024`); B9 (`:2031`); `Aliased` unreachable (`:2038`); **`TagConfused` unreachable (`:2045`)** |
| `cap27d_ss_q1_strict_foreign_tag_tlr_tag_unbound.pv/.out` | `cap27c` | **only** the `TLR` tag check unbound (C-C18, case (a)) | (i) `is false` (`:670`); (ii) `skH1` **`is false`** (`:824`), `skH2` `is true` (`:834`); (iii) unreachable (`:841`); witnesses (`:1140`–`:2309`); B9 (`:2316`); `Aliased` unreachable (`:2323`); **`TagConfused` reachable (`:2471`)** |
| `cap27e_ss_q1d_degraded_foreign_tag_correct.pv/.out` | `s-standing/proverif/ss_q1d_degraded_compromised.pv` (committed) | as `cap27c`, on the degraded model | (i) `is false` (`:666`) — the registered degraded cost, as on the baseline (`ss_q1d_degraded_compromised.out:640`); (ii) `is true` (`:675`, `:684`); (iii) unreachable (`:690`); witnesses (`:976`–`:1835`); `Aliased` unreachable (`:1847`); **`TagConfused` unreachable (`:1853`)** |
| `cap27f_ss_q1d_degraded_foreign_tag_tlr_tag_unbound.pv/.out` | `cap27e` | **only** the `TLR` tag check unbound (C-C18, case (d)) | (ii) `skH1` **`is false`** (`:807`), `skH2` `is true` (`:816`); (iii) unreachable (`:822`); witnesses (`:1108`–`:1967`); `Aliased` unreachable (`:1979`); **`TagConfused` reachable (`:2135`)** |
| `cap27g_ss_q1d_degraded_foreign_tag_envelope_observer.pv/.out` | `cap27e` — the **round-16** reviewer's `/tmp/tessera-round16-qba73enf/tag_scope_control.pv`, byte for byte | an envelope-side observer `EnvelopeForeignAccepted(kX, tag)` beside the correct `BYTES` tag check; no check changed | as `cap27e`; observer unreachable (`:1859`); `TagConfused` unreachable (`:1865`) |
| `cap27h_ss_q1d_degraded_foreign_tag_envelope_bytes_tag_unbound.pv/.out` | `cap27g` — the reviewer's `tag_scope_mutant.pv`, byte for byte | **only** the envelope's `BYTES` tag equality removed; standing path untouched | observer **reachable** (`:2016`); `TagConfused` unreachable (`:2022`); every other polarity unchanged — C-Q10 does not see the envelope's consumer (C-Q8 does) |

These eight results (the last two added after Codex round 16, at the
reviewer's own `.out` line numbers) are **not** S-STANDING results and
no family file records them, and they are **not** capstone results — no
capstone model exists. They are the descent of C-Q10's prediction and
C-C18's sets in
`PREDICTIONS.md` §3, §9(5) and the amendment section dated 2026-09-18,
and nothing in them is evidence about the refusal record.
