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
