# The suite ledger — entered register (A3.3 conservation fields)

> **STATUS: PROPOSED — 2026-09-14 — drafted by the AI collaborator
> (Claude Opus 5, directed by the owner instance); not adopted; the
> commit is the author's.** This file is the *entered* register that
> `formal/BAND0-EXIT.md` item E5(a) owes: every ledger entry offered by
> the five suite families and the first-link spike, carried across with
> the A3.3 conservation fields, classified by kind, and — for the
> cross-model kind — assembled into the draft discharge matrix the
> capstone must turn green. **It registers nothing and discharges
> nothing.** Nothing here is discharged until `formal/suite/capstone.pv`
> exists and runs; the "expected red" column is a prediction, not a
> result. Where this file and a family's `RESULTS.md` disagree, the
> family file wins and the disagreement is a defect here. No family file
> is edited by this work. Amend-don't-rewrite applies from this file's
> first commit. **Repaired in place on 2026-09-14** after a non-author
> review that declined to confirm the first draft; see the final
> section, "Repairs after the 2026-09-14 Codex review", for every edit
> and the runs that back it. **Repaired again in place on 2026-09-15**
> after the second, full non-author review
> (`docs/reviews/2026-09-15-codex-full-review-ledger.md`, six findings,
> all accepted by the owner instance); see "Repairs after the
> 2026-09-15 Codex full review" for every edit and every run.
> **Repaired a fourth time in place on 2026-09-15** after the third
> non-author round
> (`docs/reviews/2026-09-15-codex-full-review-ledger-round3.md`, six
> findings, all accepted) and the same day's full skeptic read. **That
> repair changes the file's shape, not only its cells:** §2 is split
> into the cross-model matrix **2(a)**, the rows **2(b)**
> held out by R-1 as written (D1, D2), and **2(c)**, conditional on R-3; joins with no producer in the tree are recorded as
> *"producer to be registered in the capstone"* with the exact relation
> stated and nothing else claimed (**C-Q8** for D6, **C-Q9** for D10);
> C-Q1 is written as a query contract; and R-1, R-2 and R-3 are stated
> once each with their combined consequences in one table. See
> "Repairs after the 2026-09-15 Codex round 3 and skeptic read".
> **Repaired a fifth time in place on 2026-09-15** after the fourth
> non-author round
> (`docs/reviews/2026-09-15-codex-full-review-ledger-round4.md`, four
> findings, all accepted). **That repair changes the proof contract,
> not the register's entries:** **C-Q8** is rewritten as a structural
> judge over *every* accepted `(key, signature, presented bytes)`
> triple including failed verification (the honest-filtered form is
> withdrawn); **C-Q1's link 1 splits into 1a/1b** so accepted-evidence
> binding is asserted in **both** modes, **link 2 splits into 2a/2b**
> so required-set completeness is asserted within one acceptance, and
> **link 6 splits into 6a/6b** so object type and innermost-issuer
> scope have separate producers; `LayerAccepted` gains an **acceptance
> identifier** and the **accepted evidence term**; and **D11 moves from
> §2(c) into the matrix**, because C-Q1 consumes scope unconditionally,
> so **R-3 now decides only L-16/L-17**. The matrix was **nine rows** at
> that repair; it is **eleven** under the author's ruling below.
> Three companions are added or re-specified (**C-C7** rewritten,
> **C-C9**, **C-C10**). See "Repairs after the 2026-09-15 Codex round 4".

> **RULED (author), 2026-09-15 — outcome 5.** The three forks routed in
> §5 are decided. The author's words, in session: *"Having understood
> this, I think composition is the right answer here."* and *"I am
> satisfied with outcome 5, and merely restate my concerns that the real
> burden for testing these claims will fall on the adjudicator."*
> **R-1 = Reading B (composed); R-2 = yes; R-3 = formulation W** —
> outcome 5 of §5's combined-consequences table. **The instrument: this
> file's default reading changes to outcome 5.** The cross-model matrix
> §2(a) is **D1–D11, eleven rows**; **§2(b) is vacated and empty** (D1
> and D2 are matrix rows, with `m4`/`s4` registered as the capstone's own
> companions C-C2 and C-C4); **§2(c) carries D12 and D13 as rows**, both
> NOT YET SHOWN. The capstone's `PREDICTIONS.md` is drafted from §6 under
> this reading. **The file is still PROPOSED and still registers and
> discharges nothing** — what the ruling settles is classification, not
> any discharge. **The commit is the author's.** Recorded under the
> `formal/spike/first-link/DECISION.md` provenance labels; the full block,
> with the author's carried concern, is at the head of §5.

**Vocabulary, stated once.** In this file **"producer" and "consumer"
name *models*** — the model that *proves* a fact, and the model that
*assumes* it. They never name parties, people or organisations.
*(The author found "producer" ambiguous, 2026-09-15: it is an abstract
provider of information, not an actor.)*

## The gate this file serves

Amendment 3 §A3.3 (`docs/phase-0-prereg-amendment-3.md:220-230`),
verbatim: *(line range corrected — skeptic 2026-09-15; `:216-229` pointed at
the paragraph above the blockquote)*

> Band 0 exit is gated on a capstone composition context in which
> every ledgered **cross-model** assumption — a fact one symbolic
> model assumes and another must establish — is discharged by a
> machine-checked producer query and carries a broken companion that
> **fails the query consuming the severed link**. Layer 2 assumptions
> (cryptographic primitive security, historical trust-anchor
> correctness, chain availability, implementation fidelity,
> operational independence of authority channels) are explicitly
> exposed and unclaimed in the ledger — never discharged, never
> silently absorbed. Any termination-forced scoping is named in-module
> and disposed by amendment discipline, never silently.

**Conservation fields** (A3 §A3.3, `:232-238`): consumer property/query;
assumed fact; producer module and event/query (or "Layer 2 —
unclaimed"); the shared term establishing correspondence; adversary
capabilities at the join; residual Layer 2 assumption; and, for a
cross-model entry, the broken mutation and expected failing query.

## The rule that decides entry vs. non-entry

Amendment 7 §A7.10 (`docs/phase-0-prereg-amendment-7.md:240-258`,
ADOPTED (author), signed 2026-09-14), the author's words:

> *"B for S-P1. Authorship and key binding compose as complementary
> claims. We should not create a dependency if said dependency cannot
> falsify the claim of the consumer. Different consumers will need
> their own dependency analysis."*

Applied here: an offered entry becomes a **CROSS-MODEL** entry only
where severing the producer's fact would falsify the consumer's own
registered query. Where it would not, the entry is recorded
**COMPLEMENTARY** — no severing companion is claimed and it is not a
capstone discharge-matrix row. Each consumer of a shared producer fact
gets its own determination; the four consumers of L-01 do not move
together.

## Entry kinds

| Kind | Meaning | Capstone consequence |
|---|---|---|
| **CROSS-MODEL** | A fact one symbolic model assumes and another must establish, where severing it falsifies the consumer's registered query | A discharge-matrix row: producer query + severing companion that fails the *consumer's* query |
| **COMPLEMENTARY** | An offered relation whose severing does not falsify the named consumer's registered query (A7 §A7.10), or whose only consumer is prose | No row, no companion claimed; composed at the capstone as two independent axes |
| **LAYER-2(a)** — permanent external assumption | A fact on the A3 §A3.3 list — cryptographic primitive security, historical trust-anchor correctness, chain availability, implementation fidelity, operational channel independence — plus ENUM §3's concrete-digest item. Nothing this project can build discharges it; it is discharged, if at all, by cited external results | Exposed and unclaimed, permanently; never a row |
| **LAYER-2(b)** — internal proof obligation carried as an assumption | A fact **this project owes** and is carrying as an assumption until the artifact that settles it exists: canonical encoding / framing injectivity and what a fingerprint or a core hashes, pre-P8 (`formal/BAND0-EXIT.md` **E3**, the P8 framing proof, its golden vectors and its review); and the §A3.7.2 extended atomic-entry invariant (**E6**, two TLA+ additions). *Split from (a) on 2026-09-15, finding 6: the first draft filed these under "forever", which would permanently exempt work the project has already booked.* | Exposed and unclaimed **today**; never a row; each cites the exit item that discharges it, and each is re-read when that item lands. **The word "forever" does not apply to this class** |
| **CROSS-FORMALISM** | A TLA+ ↔ symbolic join (ENUM §4, `ENUMERATION.md:135-147`) | Producer names a TLA+ module and invariant; **never** marked symbolically discharged — mislabelling one is the checkmark-relay red bar (Sol finding 2) |

## Index — offered entry → register number

| Source (file:lines) | Offered as | Register |
|---|---|---|
| `s-p3/RESULTS.md:203-216` | entry 1, key-binding relation | **L-01** |
| `s-p3/RESULTS.md:217-227` | entry 2, possession binds manifest | **L-02** |
| `s-p3/RESULTS.md:228-231` | entry 3, no cross-formalism join | **L-03** |
| `s-p1/RESULTS.md:330-344` | entry 1, key binding (complementary) | **L-01** (consumer row) |
| `s-p1/RESULTS.md:345-383` | entry 2, first link | **L-04** |
| `s-p1/RESULTS.md:384-403` | entry 3, `Accept`/`AcceptS` ↔ P4 | **L-05** |
| `s-p1/RESULTS.md:404-424` | entry 4, integrity / authorship | **L-06** |
| `s-p1/RESULTS.md:425-469` | entry 5, key-use discipline | **L-07** |
| `s-p2/RESULTS.md:251-258` | Consumed 1, key binding | **L-01** (consumer row) |
| `s-p2/RESULTS.md:259-267` | Consumed 2, possession | **L-02** (consumer row) |
| `s-p2/RESULTS.md:268-274` | Consumed 3, P8 set encoding | **L-08** |
| `s-p2/RESULTS.md:275-283` | Consumed 4, `Accept` ↔ P4 | **L-05** |
| `s-p2/RESULTS.md:286-299` | Produced 1, set completeness | **L-09** |
| `s-p2/RESULTS.md:300-311` | Produced 2, set integrity | **L-10** |
| `s-p2/RESULTS.md:312-316` | Produced 3, no other cross-formalism join | **L-11** |
| `s-p7/RESULTS.md:495-517` | entry 1, type soundness | **L-12** |
| `s-p7/RESULTS.md:518-544` | entry 2, scope relation | **L-13** |
| `s-p7/RESULTS.md:545-568` | entry 3, commitment relation | **L-14** |
| `s-p7/RESULTS.md:569-594` | Consumed from elsewhere (S-P3 1, S-P3 2, S-P1 4, S-P1 5) | **L-01, L-02, L-06, L-07** (consumer rows) |
| `s-p7/RESULTS.md:592-594` | Cross-formalism joins: none consumed | **L-15** |
| `s-standing/RESULTS.md:434-452` | P-1, standing relation | **L-16** |
| `s-standing/RESULTS.md:454-466` | P-2, entitled key in the standing path | **L-17** |
| `s-standing/RESULTS.md:467-479` | P-3, degraded boundary | **L-18** |
| `s-standing/RESULTS.md:483-494` | C-1, key binding | **L-01** (consumer row) |
| `s-standing/RESULTS.md:495-507` | C-2, TLR anchor temporal validity | **L-19** |
| `s-standing/RESULTS.md:508-515` | C-3, canonicalization injectivity | **L-20** |
| `s-standing/RESULTS.md:516-526` | C-4, type soundness of TLR / wrappers | **L-13** (consumer row) |
| `s-standing/RESULTS.md:527-538` | C-5, SC-2 one-signing-act commitment | **L-21** |
| `first-link/RESULTS.md:86-104` | entry 1, Q1/Q3 chain correspondence | **L-04** |
| `first-link/RESULTS.md:105-109` | entry 2, Q2 broken companion | **L-22** |
| `first-link/RESULTS.md:110-112` | entry 3, Q4 attack objective | **L-23** |
| `first-link/RESULTS.md:113-128` | entry 4, judge encoding note (CORRECTED) | **L-24** |
| `first-link/RESULTS.md:163-164` | addendum 5, Q5/Q6 digest residual | **L-25** |
| `first-link/RESULTS.md:164-171` | addendum 6, Q6 is unconditional | **L-26** |

---

# 1. Register

## L-01 — Key-binding relation (hub: one producer, four consumer determinations)

| Field | Value |
|---|---|
| **Kind** | Producer entry; each consumer determined separately below |
| **Assumed fact** (quoted, `s-p3/RESULTS.md:206-209`) | *"acceptance of framed bytes under `kX` implies the bytes' committed `(issuerId, kfp)` is `(id, fp(kX))`, and honest bytes are never accepted under a key other than their signer's"* |
| **Producer** | S-P3 Q2, `Reattributed` unreachable — `sp3_q2_degraded_compromised.out:195` (`PossessionTransplanted` `:200`, witness `:376`); strict form Q1 both variants, `sp3_q1_strict_dns_compromised.out:223` *(line citations added 2026-09-15; the draft named the model and not the result line)* |
| **Shared term** | *"accepted key, issuer identity, framed bytes"* (`s-p3:209-210`) |
| **Adversary at the join** | *"A1.3 with item 3 expressible (D-4), sole channel compromised, possession free"* (`s-p3:210-212`) |
| **Severing companion (producer side)** | S-P3 Q3, `sp3_q3_companionA_frame_unbound.pv` (frame unbound) → `Reattributed` red, `sp3_q3_companionA_frame_unbound.out:359` `is false`, witness reachable `:532` (`s-p3:212-213`) |
| **Residual Layer 2** | L2-b `fp` collision resistance and what a fingerprint hashes (canonical encoding pre-P8); L2-c `h` idealization; L2-f deterministic signatures; L2-d frame layout (P8); L2-e verification profile, P3 `[assumption]` half, H1a (cryptographic primitive security) — `s-p3:213-216` |
| **Source** | `formal/suite/s-p3/RESULTS.md:203-216`; the four-statement record obligation at `:232-250` |

### L-01 consumer determinations (A7 §A7.10, one analysis each)

| Consumer | Consumer query | Decision | Reasoning | Source |
|---|---|---|---|---|
| **S-P1** | Q2(i) `AcceptedUnderHonestKey ⟹ IssuerSigned` | **COMPLEMENTARY** | Ruled by the author: the two are complementary axes, and S-P1 states that *"**No severing companion fails an S-P1 query** (judge H is keyed on honest keys and is blind to honest bytes accepted under an adversary key by construction)"* | `s-p1:330-344`; A7 §A7.10, `a7:242-252`; `docs/implementation-spec.md:1525-1533` |
| **S-P2** | Q2 carried `Reattributed` judge (`sp2_q2_degraded_compromised.pv:268-273`, query `:143-144`), unreachable in all eight models *(line citation corrected — skeptic 2026-09-15: the draft carried the family file's `:229-233`, a **pre-addendum** position; after the 2026-09-12 §A5.4 addendum those lines are the three content guards and the `Accept2S` outputs)* | **CROSS-MODEL — RULED (author), 2026-09-15.** *R-1 = Reading B (composed) and R-2 = "yes", so this consumer determination is CROSS-MODEL and the row is in §2(a). It was COMPLEMENTARY under A7 §A7.10 applied to the models as they stand, and ROUTED (R-1 × R-2) in §2(b) until the ruling; the reasoning that held it there is kept below as the record.* | **Repaired 2026-09-14 after the Codex review.** The first draft read S-P2's dependency statement (*"the frame's fingerprint field alone carries `Reattributed`"*) as "removing that field breaks the protection". It does not — *alone sufficient* is not *individually necessary*. The binding is defended by two independent routes (matrix below), exactly as S-P3's F3 states. Severing the **complete** relation does falsify S-P2's own registered query, so the entry stands as CROSS-MODEL, with a corrected companion. **[A7 §A7.10 applied by the skeptic, 2026-09-15: this reasoning does not establish the rule's antecedent.]** What `m4` severs is S-P2's *own transcribed* checks inside `sp2_q2_degraded_compromised.pv`. Severing the **producer** — S-P3's Q2, or S-P3's model entire — changes nothing in S-P2's model and leaves `Reattributed` green at `base_sp2.out:397`. So "severing the producer falsifies the consumer's query" is shown only under R-1's Reading B, where what is consumed is the *security* of a transcribed check rather than the check. The row is therefore **COMPLEMENTARY today**: the rule's antecedent is not met. It is a row only under Reading B — the capstone composing both families' checks into one verifier, where `m4` becomes the capstone's own companion (C-C2) — **and** only if R-2 also answers "yes", since `m4` is a two-removal severing of jointly-sufficient pins. D1 was held out of the matrix in §2(b) accordingly. **The author ruled both forks on 2026-09-15 — R-1 = Reading B, R-2 = "yes" (outcome 5) — so this reasoning is superseded: D1 is a firm row of §2(a), §2(b) is vacated, and `m4` is registered as the capstone's own companion C-C2. The paragraph is kept as the record of what was put to the author.** See §5's combined-consequences table, row 5 | `s-p2:251-258`, `:233-239`; `s-p3:195-199` (F3); scratch matrix below |
| **S-P7** | Q2 `Rescoped`, key half | **CROSS-MODEL — RULED (author), 2026-09-15.** *R-1 = Reading B (composed) and R-2 = "yes", so this consumer determination is CROSS-MODEL and the row is in §2(a). It was COMPLEMENTARY under A7 §A7.10 applied to the models as they stand, and ROUTED (R-1 × R-2) in §2(b) until the ruling; the reasoning that held it there is kept below as the record.* | **Repaired 2026-09-14.** The first draft named **Q6b** as the severing companion. Q6b is not one: it reads key and authority from the *outermost* frame, which severs the **scope** relation (which frame governs), not S-P3's key-binding fact — a different failure, so its red does not discharge this join. The correct companion severs the complete binding relation inside `InnerCheck` (`s4_innerfp_mh` shape); it turns `Rescoped` red. The *outer* checks are carried/inert (a13) and contribute no dependency. **[A7 §A7.10 applied by the skeptic, 2026-09-15: as in the S-P2 row, `s4` severs S-P7's own transcribed checks, not the producer. Severing S-P3's Q2 leaves `Rescoped` green at `base_sp7.out:540`.]** **Restated 2026-09-15 round 3:** this row was **COMPLEMENTARY today** and became a row only under Reading B **and** R-2 "yes", with `s4` as the capstone's own companion (C-C4); D2 was held out in §2(b). **RULED (author), 2026-09-15: Reading B and "yes" — outcome 5. D2 is a firm row of §2(a), §2(b) is vacated, and `s4` is registered as C-C4. The paragraph is kept as the record of what was put to the author.** See §5's combined-consequences table, row 5. | `s-p7:518-544`, `:569-575`; scratch matrix above |
| **S-STANDING** | Q1 (i)/(ii)/(iii), all variants | **COMPLEMENTARY** | S-STANDING states *"the envelope path carries S-P3's checks verbatim and this model does not re-prove them"*, and the 2026-09-12 disposition 2 confirms *"the standing path alone does not check the frame identity — which is `ENUMERATION` note 4 item 2 working as intended"*; no standing query is downstream of the relation | `s-standing:483-494`, `:1268-1283` |

**Narrowing applied.** S-P7's model header once read *"the wrapper's authorship is S-P3 entry 1, consumed"*; the author's 2026-09-12 C5 read returned NO and the line was repaired to *"the wrapper's KEY BINDING is S-P3 entry 1, consumed; its AUTHORSHIP is S-P1's, per S-P3 F7"*. This register uses the repaired wording: authorship is L-06, not L-01. (`s-p7:1173-1202`)

### L-01 severing evidence — single-removal matrix (scratch runs, 2026-09-14)

Run by the AI collaborator on **copies** in `formal/suite/ledger-tests-2026-09-14/`
(archived from the session scratchpad), `proverif -lib …/tessera_theory.pvl`, ProVerif 2.05.
**No repository model was edited or run.** These are unregistered
ledger-verification probes, evidence about the *checking arrangement*,
never about a registered query; they are not a family result and no
family file records them.

**In S-P2** (`sp2_q2_degraded_compromised.pv` copied to `base_sp2.pv`). Baseline: `Reattributed` unreachable (`base_sp2.out:397`), `HonestAccepted` reachable (`:1007`).

| Mutation | `Reattributed` | Other queries | File |
|---|---|---|---|
| none (baseline) | unreachable `:397` | all green; witnesses reachable | `base_sp2.out` |
| frame pin `=fp(kA)`/`=fp(kB)` removed | **still unreachable** `:399` | unchanged | `m1_framepin.out` |
| manifest-hash equality `mh_ = h(t)` removed | **still unreachable** `:394` | unchanged | `m2_mh.out` |
| tuple fingerprint match `fp(k_) = kfpr_` removed | **still unreachable** `:645` | `SignerForged` red `:619` | `m3_tuplefp.out` |
| frame pin **+** manifest hash | **reachable** `:620` | `Stripped` `:379`, `SignerForged` `:392`, `SetAltered` `:405`, `Spliced` `:1263` all green; both `HonestComplete` (`:791`, `:1015`) and `HonestAccepted` (`:1250`) reachable | `m4_framepin_mh.out` |
| frame pin **+** tuple fingerprint match | **reachable** `:870` | `SignerForged` also red `:621` | `m5_framepin_tuplefp.out` |
| manifest hash **+** tuple fingerprint match (pin kept) | **still unreachable** `:649` | `SignerForged` red `:621` | `m6_mh_tuplefp.out` |
| all three (the complete binding relation) | **reachable** `:860` | `SignerForged` also red `:625` | `m7_all_three.out` |

**The structure the matrix shows**, and what the register now records:
re-attribution is blocked by *the frame's fingerprint pin* **or** by
*the manifest-hash equality together with the tuple fingerprint match*
— neither route needs the other, and no single removal opens the
attack. This is S-P3's F3 transcribed: *"the tuple fingerprint match
and the manifest-hash check together compensate for its absence, and
neither alone does"*.

**In S-P7** (`sp7_q2_degraded_compromised.pv` copied to `base_sp7.pv`; the same relation inside `InnerCheck`). Baseline: `Rescoped` unreachable (`base_sp7.out:540`), witnesses reachable (`:865`, `:1061`).

| Mutation | `Rescoped` | Other queries | File |
|---|---|---|---|
| inner `=fp(kI)` pin removed | **still unreachable** `:540` | every query green; both witnesses reachable | `s3_innerfp.out` |
| inner pin **+** `mhI = h(tI)` | **reachable** `:864` | `InnerSigTransplanted` `:1207` and `Reattributed` `:1431` also red; `TypeConfused` `:526`, `VersionLied` `:1949` green; witnesses reachable `:1734`, `:1933` | `s4_innerfp_mh.out` |
| inner pin **+** `mhI` **+** `fp(kI) = kfprI` | **reachable** `:869` | same polarity as above | `s5_innerfp_mh_tfp.out` |

Same two-route structure, and the same correction: the inner pin alone
is not the load.

## L-02 — Possession binds the manifest to the named key

| Field | Value |
|---|---|
| **Kind** | Producer entry; consumer determinations below |
| **Assumed fact** (quoted, `s-p3:222-224`) | *"an accepted possession proof under `kX` is a signature over the accepted manifest, which names `fp(kX)`"* |
| **Producer for S-P3's own, narrower fact** | S-P3 Q2/Q4 correct form, `PossessionTransplanted` unreachable — `sp3_q2_degraded_compromised.out:200` — *"an A1.5/P10 result carried in S-P3"* (`s-p3:217-221`). **Scoped 2026-09-15 round 3, finding 2: S-P3's `PossJudge` compares KEYS ONLY.** Its text is `in(honestPossCh, (kH, p)); in(possCh, (kX, =p)); if kX = kH then 0 else event PossessionTransplanted(kX, p)` (`sp3_q2_degraded_compromised.pv:137-141`): the honest proof term `p` and the two keys. **Neither the event nor the query mentions the accepted manifest.** |
| **The relation S-P2's consumer requires** (named 2026-09-15 round 3, finding 2, in the library's terms) | For a completed acceptance that reports key `kX` and accepted manifest `t`: the accepted possession proof `ppf` satisfies **`checksign(ppf, kX) = (POSS, t)` for the same `t` the verifier accepted** — possession is proved over the **accepted manifest**, under the **accepting key**, and the two are the same acceptance's. This is a three-place relation over *(accepting key, accepted manifest, accepted possession proof)*; `PossessionTransplanted` is a two-place observation of *(original key, accepted key)* and is blind to it |
| **Producer for that relation** | **NONE COMMITTED — provisional; producer to be registered in the capstone.** Shown, not asserted: with **both** manifest-binding protections removed together (possession made fingerprint-only per the library's D-3 under-encoding, and the frames' `mh = h(t)` guards dropped), **S-P3's `PossessionTransplanted` stays green** while **S-P2's `SetAltered` goes red** in the same model — `d10b_sp2_q9_manifest_unbound.out:1297` `is true` against `:673` `is false`, with `Stripped` `:454`, `SignerForged` `:464`, `Reattributed` `:683`, `Spliced` `:1287` all still true and all three witnesses reachable (`:851`, `:1072`, `:1277`). This reproduces the reviewer's round-3 finding-2 diagnostic on our tree. The named theorem therefore **cannot** supply what the consumer needs. **Independent of R-2:** R-2 decides whether L-02 → S-P2 is a row at all; this row records that, if it is one, its producer does not yet exist |
| **The query the capstone must add** (C-Q9, §6) | A **possession-over-the-accepted-manifest** judge. **Event signature:** `event PossessionUnbound(pkey, bitstring, bitstring)` — *(accepting key, accepted manifest/authority tuple, accepted possession proof)*. **Fixture wiring:** the verifier reports `(kX, t, ppf)` on a private channel at **each** acceptance point (both the n = 1 and n = 2 branches, once per signer slot); the judge fires `PossessionUnbound(kX, t, ppf)` when `checksign(ppf, kX)` is not `(POSS, t)` — including when it does not verify at all. **Registered unreachable.** **Honest witness:** both `HonestComplete` witnesses (one-signer and two-signer) and `HonestAccepted` reachable in the same fixture. **Feasibility checked on a copy, not registered:** green on the committed S-P2 verifier (`d10a_sp2_q9_base.out:1111` `is true`, with all five S-P2 safety queries green `:457, :464, :471, :478, :1097`, `PossessionTransplanted` `:1104` green, witnesses `:643`, `:861`, `:1090`), and **red** under the combined manifest-unbinding that leaves `PossessionTransplanted` green (`d10b_sp2_q9_manifest_unbound.out:1462` `is false`). C-Q9 is therefore a query that **does** range over the term D10 consumes, where `PossessionTransplanted` does not |
| **Shared term** | *"accepted key, manifest"*; library tag `POSS` (D-3, possession is over the MANIFEST, not the fingerprint) |
| **Adversary at the join** | As L-01: A1.3, DSKS expressible (D-4), sole channel compromised, possession free |
| **Severing companion (producer side)** | S-P3 Q4, `sp3_q4_companionB_possession_unnamed.pv` (naming check dropped) → `PossessionTransplanted` red, via `dsks`: `.out:383` `is false`, with `Reattributed` `:195` still true and the witness reachable `:559` (`s-p3:226-227`) |
| **Residual Layer 2** | As L-01 |
| **Source** | `formal/suite/s-p3/RESULTS.md:217-227`; library D-3, `lib/tessera_theory.pvl:36-45` |

| Consumer | Consumer query | Decision | Reasoning | Source |
|---|---|---|---|---|
| **S-P2** | Q5 `SetAltered` | **CROSS-MODEL — RULED (author), 2026-09-15 (R-2 = "yes": a jointly-sufficient pin IS a dependency).** *Was ROUTED (R-2) until the ruling; the reasoning is kept below. The producer defect is untouched by the ruling — see the row's last paragraph.* | S-P2 records *"C3 is the configuration in which this link alone carries `SetAltered`; C2 severs it (with the hash) and goes red"*, and the dependency statement says *"the frame's manifest hash and possession-over-manifest each alone carry `SetAltered` and neither is needed while the other stands"*. Severing possession **alone** does not falsify the query; severing it turns the query red only once the hash pin is already gone. Whether a jointly-sufficient pin is a dependency under A7 §A7.10 is the author's call. **Producer repaired 2026-09-15 round 3 (finding 2):** even if R-2 makes this a row, its producer is **not** S-P3's `PossessionTransplanted` — that theorem compares keys only and survives the mutation that reds `SetAltered` (`d10b_sp2_q9_manifest_unbound.out:1297` green, `:673` red). The producer is **to be registered in the capstone**, as **C-Q9**. The two questions are independent | `s-p2:259-267`, `:233-239` |
| **S-P7** | none | **COMPLEMENTARY** | S-P7 records the consumption and immediately narrows it: *"a08 shows it carried for these queries"* — inert; no S-P7 query is falsified by severing | `s-p7:573-574` *(corrected from `:576-578` — skeptic 2026-09-15)* |

## L-03 / L-11 / L-15 — Negative cross-formalism records

No assumed fact, no producer, no consumer; each exists so the capstone
does not open a TLA+ row that no family consumes.

| Register | Family | Quoted |
|---|---|---|
| **L-03** | S-P3 | *"nothing in S-P3 assumes anchor validity; no TLA+ join is consumed. Recorded so the capstone does not look for one."* (`s-p3:228-231`) |
| **L-11** | S-P2 | *"nothing in S-P2 assumes anchor validity or a refusal state; no TLA+ join is consumed other than the `Accept` ↔ P4 partition (consumed entry 4). Recorded so the capstone does not look for another."* (`s-p2:312-316`) |
| **L-15** | S-P7 | *"**Cross-formalism joins: none consumed** (A7 ruling: the §4 refusal-latch join belongs to S-STANDING). Recorded so the capstone does not look for one here."* (`s-p7:592-594`) |

**Correction of record carried by L-15.** `ENUMERATION.md:141-143` names
*"refusal/standing state (producer: P5c refusal latch) consumed by
S-P7's standing claims"*, and COVERAGE-MAP rows 6 and 7 repeat it. The
A7 ruling moved that join to S-STANDING (L-21). The capstone follows
the ruling; the ENUM and map sentences are superseded in substance and
left as written.

## L-04 — First link: at least one authority channel uncompromised

Offered from both sides: the spike produces it, S-P1 consumes it. One entry.

| Field | Value |
|---|---|
| **Kind** | **CROSS-MODEL** |
| **Assumed fact** (quoted, `s-p1:347-349`; *corrected from `:349-351` — skeptic 2026-09-15*) | *"strict acceptance implies an uncompromised channel published the accepted tuple (A1.3 'never all', n = 2 enumerated, not generalized)"*; spike form: *"at least one authority channel uncompromised (A1.3 'never all', cited explicitly per the DeepSeek panel criterion — the adversary controls any strict subset)"* (`first-link:87-89`; *corrected from `:88-91` — skeptic 2026-09-15*) |
| **Consumer property/query** | (a) S-P1 Q1(i) `Accept ⟹ IssuerSigned`, `sp1_q1_strict_dns_compromised.pv:145-146`, RESULT true at `sp1_q1_*.out:201`. (b) the §A3.2 witness chain, first link — the capstone's linkage query (`first-link:86-87`) |
| **Producer module and query** | S-P3 Q1(ii), `Accept ⟹ (AuthorityPublishedDNS ∨ AuthorityPublishedRepo) ∧ IssuerPossession ∧ IssuerSigned`, `sp3_q1_strict_dns_compromised.pv:91-96` and `sp3_q1_strict_repo_compromised.pv:91-96`, RESULT `is true` at `sp3_q1_strict_dns_compromised.out:424` and `sp3_q1_strict_repo_compromised.out:424`; originally the spike's `q1_chain_*.pv` / `q3_mechanism_*.pv` chain correspondence |
| **Shared term** | the manifest `t` (S-P1); *"authority tuple, accepted key, framed bytes"* (spike) |
| **Adversary at the join** | *"A1.3 items 1–6 with D-4, one of two channel keys public (both variants run; `sp1_q1_strict_dns_compromised.pv:208` / `…repo…pv:208`)"* |
| **Broken mutation** | *"both channel keys public in the Q1 form (`out(c, skD); out(c, skR)` in place of the single leak at line 208)"* |
| **Expected failing query** | Q1(i) `Accept ⟹ IssuerSigned`, *"red via impersonation under the adversary's own key (the Q2(ii) trace shape, `sp1_q2_*.out:354`), with the headline Q1(ii) expected to stay green and N1 reachable"* |
| **Severing companion** | **To be built in the capstone.** S-P1 labels it *"an unrun, labelled prediction, not evidence"* and *"**Not run** (the skeptic's fix said 'run nothing'); nothing is claimed from it"* |
| **Residual Layer 2** | L2-c `h` idealization / concrete digest collision resistance; L2-b `fp` collision resistance; **L2-h** n = 2 enumerated, not generalized (A1.3 item 6; the 2026-08-12 documentation correction: *"for n = 2, the honest baseline and the two single-channel-compromise variants exhaust the proper subsets. This is finite enumeration, not a quantified result"*) |
| **Decision (A7 §A7.10)** | CROSS-MODEL: severing the fact (both channels compromised) turns S-P1's own registered Q1(i) red by the family's own named prediction — the falsification test is met on the face of the entry |
| **Source** | `formal/suite/s-p1/RESULTS.md:345-383`; `formal/spike/first-link/RESULTS.md:86-104`; the disjunctive recut, `first-link:50-61` |

## L-05 — `Accept` / `AcceptS` ↔ P4 verdict partition

Offered by S-P1 and S-P2 from the same (consumer) side; one entry, both cited.

| Field | Value |
|---|---|
| **Kind** | **CROSS-FORMALISM** — never symbolically dischargeable |
| **Assumed fact** (quoted, `s-p1:385-389`) | *"every symbolic path that stops short of the acceptance event lands in `INVALID` or `UNVERIFIABLE` in P4's model, never in a valid verdict; `Accept` (strict) / `AcceptS` (degraded) correspond to `VALID_STRICT` / `VALID_DEGRADED`, the latter only under an explicit recorded waiver"* |
| **Consumer** | S-P1 (F5's *"provided the verdict says it is degraded"*); S-P2 — *"Every S-P2 path that stops short of `Accept1S`/`Accept2S` on a stripped or substituted set is a performed-and-failed check; its `INVALID` landing is P4's model's"*; S-STANDING's §A4.6 proviso (`AcceptS` fired, neither queried nor shown reachable) |
| **Producer** | `formal/tla/P4_VerifierStates.tla` — invariants `Partition`, `NoSilentPromotion`, `ExactInvalid`, `ExactUnverifiable`; degraded clause joins `DegradedNeedsExplicitWaiver` (COVERAGE-MAP amendment note 3, row 2) |
| **Shared term** | the acceptance predicate |
| **Adversary at the join** | *"A1.3 items 1–6 with D-4, both modes (strict: one of two channel keys public; degraded: the sole channel key public)"*; on the TLA+ side, P4's own adversary — *"cross-formalism, not compared here"* |
| **Severing companion** | **None claimable.** ProVerif cannot consume a TLA+ result (ENUM §4) |
| **Residual** | *"the `Accept`/`AcceptS` ↔ P4 acceptance-predicate mapping is prose (A3.3 standing rule, ENUMERATION §4), never symbolic … and no query on either side discharges it"*. Not a Layer 2 item; it is E8's correspondence-mapping obligation |
| **Source** | `formal/suite/s-p1/RESULTS.md:384-403`; `formal/suite/s-p2/RESULTS.md:275-283`; `formal/suite/s-standing/RESULTS.md:556-563`; `ENUMERATION.md:135-147`; COVERAGE-MAP rows 1, 4 |

## L-06 — Integrity / authorship correspondence

| Field | Value |
|---|---|
| **Kind** | Producer entry for Q2(i)'s own, narrower fact; **no producer exists for either of the two relations its cross-model consumers require** — see the four rows below (2026-09-15, finding 1, split again in round 3). Consumer determinations below |
| **Assumed fact for consumers** (quoted, `s-p1:404-405`, `:409-410`; *the consumer half was cited `:413-414`, which is the severing-companion sentence — corrected, skeptic 2026-09-15*) | producer Q2(i) *"`AcceptedUnderHonestKey ⟹ IssuerSigned`, `sp1_q2_*.out:173`"*; for consumers: *"accepted signature verifying under that key → the exact framed bytes"* |
| **Two relations, not one** (split 2026-09-15 round 3, finding 1; the draft called them *equivalent* and they are not) | For a completed acceptance that reports key `kX`, carries the signature term `sg` and presents framed bytes `fb`: **(R-bytes)** — *the D6 relation* — `checksign(sg, kX) = (BYTES, fb)` over the **presented** `fb`: the signature accepted over `fb` under `kX` **verifies under `kX` over exactly `fb`**, not over some other bytes that same key once signed. **Corrected 2026-09-15 after the author's ruling (non-author reviewer, Codex; owner accepted):** the previous gloss — *"was produced by `kX`'s holder"* — **overstates what the predicate establishes**. C-Q8 as rewritten checks that the signature *verifies under the accepted key over exactly the presented bytes* and nothing more. The library permits a signature to verify under an **alternative** key: `checksign(sign(m, k), pk(dsks(sign(m, k), r))) = m` (`formal/suite/lib/tessera_theory.pvl:110-115`, the registered D-4 / A1.3 item 3 capability), so verification under `kX` does **not** entail production by `kX`'s holder. **Authorship remains S-P1's separate obligation** (Q2(i), honest-key-restricted) and **anti-transplant remains C-Q7's**; neither is merged into this relation and neither is weakened by the correction. **(R-key)** — *the D5 transplant scope* — no honest signer's **signature term** is carried into a completed acceptance reported under a key other than that signer's (`fb`'s fourth field `= fp(kX)` is the in-bytes half of it). **They are different properties.** A three-place relation over *(accepting key, signature term, presented framed bytes)* is R-bytes; a two-place observation of *(accepting key, signature term)* is R-key and is **blind to different bytes under the same key**. S-P1's Q2(i) is a **third**, narrower sentence — `AcceptedUnderHonestKey(k, fb) ⟹ IssuerSigned(k, fb)`, quantified over honest keys, ranging over the **bytes** and never over the **signature term** |
| **Producer for Q2(i)'s own (narrower) fact** | S-P1 Q2(i), `sp1_q2_degraded_compromised.pv`, RESULT true at `sp1_q2_*.out:173` |
| **Producer for R-key (D5)** | **NONE COMMITTED — provisional; producer to be registered in the capstone.** No query of S-P1, S-P3, S-P2 or S-STANDING ranges over the signature term. Shown, not asserted: under a *conditional* unbinding (the presented bytes must equal the signed bytes only when the signed frame's own `kfp` matches the verifying key), **S-P1's Q2(i) stays green** (`d5a_sp1_condunbind.out:195` `is true`; witness `:371`) and **S-P3's `Reattributed` stays green** while **S-P7's `InnerSigTransplanted` goes red** in the same model (`d5b_sp7_condunbind.out`: authorship `:654` true, `Reattributed` `:1060` true, `InnerSigTransplanted` `:1037` false, `Rescoped` `:700` and `TypeConfused` `:677` true, witnesses `:1370`, `:1576`). This reproduces the reviewer's 2026-09-15 diagnostic and extends it to S-P3's fact. The narrower theorem therefore **cannot** supply what the consumer needs |
| **The query the capstone must add for R-key** (C-Q7, §6) | A signature-**term** judge on the producer side — S-P7's `SigJudge` shape run against S-P1's base verifier: the honest issuer releases `sg = sign((BYTES, fb), skI)` on a private channel to the judge; the verifier reports `(acceptedKey, sg)` at its acceptance point; `SigTransplanted(kX, sg)` fires when `kX ≠ pk(skI)`. Registered **unreachable**, with the honest-flow witness reachable. **Feasibility checked on a copy, not registered:** unreachable in the committed S-P1 verifier (`d5c_sp1_sigjudge.out:203` `is true`, Q2(i) `:210` true, witness `:386`), and **reachable** under the conditional unbinding that leaves Q2(i) green (`d5d_sp1_sigjudge_condunbind.out:414` `is false`, Q2(i) `:422` still true, witness `:599`). **Scope, stated 2026-09-15 round 3, finding 1: C-Q7 serves D5 and D5 only.** It observes `(acceptedKey, signature)` and therefore **cannot see different bytes presented under the same key**. Shown on a copy: under a **same-key byte unbinding** (the signature must verify under `kX` over *some* frame naming `fp(kX)`, not over the presented bytes), C-Q7's `SigTransplanted` stays **green** (`d6b_sp1_q8_samekey_unbound.out:246` `is true`) while S-P1's own Q2(i) authorship goes **red** (`:593` `is false`) — the reviewer's same-key-unbinding diagnostic, reproduced on our tree. The register therefore does **not** name C-Q7 as D6's producer |
| **Producer for R-bytes (D6)** | **NONE COMMITTED — provisional; producer to be registered in the capstone.** No query of S-P1, S-P2, S-P3, S-P7 or S-STANDING ranges over the triple *(accepting key, signature term, presented framed bytes)*, and **C-Q7 does not either** (row above). Nothing is claimed for D6 beyond the relation as stated — and, **corrected 2026-09-15 after the ruling**, that relation is the **exact-bytes** statement, not an authorship statement: *a signature accepted under key `kX` over presented bytes `fb` verifies under `kX` over **exactly** `fb`* (`checksign(sg, kX) = (BYTES, fb)`). It does **not** say who produced `sg`; `tessera_theory.pvl:110-115` lets a signature verify under a DSKS-derived alternative key. Authorship is S-P1's (Q2(i)); anti-transplant is C-Q7's (S-P1 Q2(i) and C-Q7 are unchanged) |
| **The query the capstone must add for R-bytes** (C-Q8, §6) | A **three-place** judge over the accepting key, the signature term and the presented framed bytes. **Event signature:** `event SigBytesUnbound(pkey, bitstring, bitstring)` — *(accepting key, signature term, presented framed bytes)*. **Fixture wiring:** the honest issuer releases the triple `(pk(skI), sign((BYTES, fb), skI), fb)` on a private channel; the verifier reports `(kX, sg, fb)` at its acceptance point, `fb` being the bytes it accepted; the judge fires `SigBytesUnbound(kX, sg, fb)` when the accepted signature term is an honest signer's and **either** `kX ≠ pk(skI)` **or** `fb` is not the frame that signer signed. **Registered unreachable.** **Honest witness:** `HonestAccepted(kH, fbH)` reachable in the same fixture (C-N1's per-fixture honest-flow requirement). **Feasibility checked on a copy, not registered:** green on the committed S-P1 verifier (`d6a_sp1_q8_base.out:250` `is true`, with C-Q7 `:244` and Q2(i) `:258` also true, witness `:435`), and **red** under the same-key byte unbinding that leaves C-Q7 green (`d6b_sp1_q8_samekey_unbound.out:427` `is false`, C-Q7 `:246` still `is true`, Q2(i) `:593` `is false`, witness `:773`). C-Q8 is therefore a query that **does** range over the term D6 consumes, where neither Q2(i) nor C-Q7 does. **REWRITTEN 2026-09-15 round 4 (finding 1).** The wiring above — *"the judge fires … when the accepted signature term is **an honest signer's** and either …"* — is **withdrawn**: it quantifies over honest-released signature terms, so an acceptance whose signature the **attacker** made is outside the judge's observation and a mutation that unbinds those escapes it. The registered C-Q8 is **structural**: the verifier reports the triple `(kX, sg, fb)` at **every** acceptance point whoever made `sg`, and the judge fires unless `checksign(sg, kX)` is exactly `(BYTES, fb)`, **including when `sg` does not verify under `kX` at all**. Shown on copies: under the reviewer's escape — byte equality kept for `OT_ATTEST` frames, waived for every other signed frame type — the withdrawn form stays `is true` (`d6d_sp1_q8_type_conditional_unbound.out:315`) while the rewritten judge is `is false` (`:507`), C-Q7 (`:308`) and honest-key authorship (`:515`) stay `is true` and the witness is reachable (`:692`); the rewritten judge is green on the committed verifier (`d6c_sp1_q8_judge_all.out:284`, witness `:469`) and red under C-C7's same-key unbinding too (`d6e_sp1_q8all_samekey_unbound.out:643`). **The honest-origin/transplant claim stays C-Q7's and is not merged into C-Q8** |
| **Shared term** | for Q2(i): *"accepted key, framed bytes"*. For **R-key** (D5): **the signature term `sign((BYTES, fb), skI)` together with the reported key** — a strictly larger correspondence than the one Q2(i) and L-01 share. For **R-bytes** (D6): **the accepting key, the signature term and the presented framed bytes, as one triple** — larger again, and the one C-Q7 does not carry |
| **Adversary at the join** | *"A1.3 items 1–6 with D-4, sole channel compromised"* |
| **Severing companion (producer side)** | *"Q3 (`sp1_q3_companionA_sig_unbound.pv`, signature unbound from presented bytes) → headline red (`.out:331`)"* |
| **Residual Layer 2** | L2-a signature unforgeability (Dolev–Yao; *"confirmed as the load by probes p6/p7 — F2"*); L2-f deterministic signatures; **L2-d** canonical encoding — P8's injectivity obligation, *"term equality stands in for canonical-byte equality until P8's proof exists; then this entry cites the proof, never silently absorbs it"* — **now §3(b), discharged by BAND0-EXIT E3**, which is exactly the sentence quoted here; L2-c `h` idealization; L2-d frame layout; L2-g implementation fidelity |
| **Source** | `formal/suite/s-p1/RESULTS.md:404-424` |

| Consumer | Consumer query | Decision | Reasoning | Source |
|---|---|---|---|---|
| **S-P7** | Q2 `InnerSigTransplanted` | **CROSS-MODEL — PROVISIONAL: producer to be registered in the capstone** (repaired 2026-09-15, finding 1) | S-P7 consumes it explicitly — *"the check's *security* is consumed from S-P1, never re-proved here"*. **Repaired 2026-09-14:** the first draft named Q6b as the companion; the reviewer is right that *"a DSKS transplant accepted under another key does not, by itself, falsify P1's authorship-under-an-honest-key claim. Removing a signature check and permitting key substitution are different failures."* The companion that severs **this** fact is S-P1's Q3 mutation transcribed into `InnerCheck` — the signature no longer bound to the presented bytes (`let (=BYTES, anyb) = checksign(sgI, kI)`). Run in scratch: `InnerSigTransplanted` **reachable** (`s1_sig_unbound.out:897`), red on **exactly** that query (`TypeConfused` `:537`, `Rescoped` `:560`, `Reattributed` `:920`, `VersionLied` `:1464` green; witnesses reachable `:1233`, `:1442`). S-P7's own ablation a11 (check *removed* rather than unbound) reaches the same query (`s2_sig_removed.out:852`) but severs an S-P7 check, not S-P1's fact. **Repaired 2026-09-15 (finding 1):** C-C5's red is now tagged as **evidence that byte binding matters** — it shows the consumer's query is falsifiable by severing the binding — **not as the discharge of this join**, because the fact it severs is not the one S-P1's committed query establishes. The row's producer is the capstone's C-Q7 (above), which does not yet exist; the row is **provisional** until it does. **Scoped 2026-09-15 round 3 (finding 1): C-Q7 serves this row only.** It is not D6's producer, and this row does not borrow D6's | `s-p7:578-590` (the quoted sentence is at `:580-582`); scratch runs `d5a`–`d5d`, 2026-09-15. *`:43-48` dropped — skeptic 2026-09-15: it is the predictions-vs-observed table and supports nothing in this row* |
| **S-P2** | none | **COMPLEMENTARY** | S-P2 declines the relation: *"Authorship — that bytes accepted under an honest named key were signed by that key (F6, d4): S-P1"*, and diagnostic d4 shows that with no signature check at all *"no S-P2 judge fires and both witnesses remain reachable"* — severing authorship falsifies nothing S-P2 registers | `s-p2:331-332` *(corrected from `:326-328` — skeptic 2026-09-15)*, `:196-207` |
| **capstone** | the §A3.2 chain's last link | **CROSS-MODEL — PROVISIONAL on the same producer** (repaired 2026-09-15) | The chain link *"accepted signature verifying under that key → the exact framed bytes"* is a registered capstone obligation (A3 §A3.3, ENUM §3); severing it falsifies the linkage query by construction. **But the link as worded *is* the relation named above, and S-P1's Q2(i) does not establish it** (`d5a`/`d5d`). **Repaired 2026-09-15 round 3 (finding 1): the producer is NOT C-Q7.** The last chain link is **R-bytes** — *a signature accepted under key `kX` over presented bytes `fb` verifies under `kX` over **exactly** `fb`* (`checksign(sg, kX) = (BYTES, fb)`; **exact-bytes wording corrected 2026-09-15 after the ruling — the previous "produced by `kX`'s holder" overstated the predicate, since `tessera_theory.pvl:110-115` permits verification under an alternative key**) — and C-Q7 observes `(acceptedKey, signature)` only, so it cannot see different bytes presented under the same key (`d6b_sp1_q8_samekey_unbound.out:246` green while authorship `:593` is red). **Producer: to be registered in the capstone**, as **C-Q8** (above, §6), **in its round-4 rewritten form** — a structural judge over every accepted triple including failed verification, not over honest-released signature terms (round 4, finding 1). Nothing else is claimed for this row | `s-p1:409-410` *(corrected from `:411-414` — skeptic 2026-09-15)*; `ENUMERATION.md:113-120`; scratch `d5a`–`d5d` |

## L-07 — Key-use discipline

| Field | Value |
|---|---|
| **Kind** | **LAYER-2(a)** (implementation fidelity) — the family says so in terms — **but only for the endpoints the suite does not model** (narrowed 2026-09-15, finding 2; the modelled endpoints are the enumeration below) |
| **Consumer property/query** | *"P1 [model] binding, every S-P1 correspondence — Q1(i)/(ii) and Q2(i) alike"*; also consumed by S-P7 with L-06 |
| **Assumed fact as S-P1 states it** (quoted, `s-p1:432-437`) | *"an issuer key signs only framed objects under the `BYTES` domain tag (and its own manifest under `POSS`) — never a raw payload, never bytes of another shape, at any endpoint anywhere in the system"* |
| **Correction of that statement** (2026-09-15, finding 2) | **The global whitelist as quoted is false in the composed fixture.** S-STANDING signs `sign((TLR, body), skI)` under the same issuer key (`ss_q1_strict_dns_compromised.pv:290, :310`; also `ss_q4_companionC_terminal_unchecked.pv:198`), which the two-tag whitelist forbids. The register replaces the whitelist with the **enumeration of legitimate signing domains** below, taken from the library's own tag declarations (`lib/tessera_theory.pvl`, D-1, D-3, D-6), and states the composed property in terms of it |
| **Producer** | *"**none — Layer 2 / implementation fidelity, unclaimed.** No symbolic model in this suite quantifies over the endpoints that hold an issuer key"* |
| **Shared term / adversary** | *"the honest issuer key `pk(skI)`/`pk(skI2)` and the `IssuerSigned` event"*; A1.3 items 1–6 with D-4, chosen-message issuer |
| **Severing witness (run, not a registered companion)** | The reviewer's A8 composition break: a second honest endpoint under the same key signing a payload-only message → `RESULT event(AcceptedUnderHonestKey(k,fb_5)) ==> event(IssuerSigned(k,fb_5)) is false.` (`falsification-2026-09-06/scratch/a8_cross_broken_endpoint.pv`, `.out:428`). *"the added endpoint is broken by construction and the committed fixture is not falsified"*. Discharge route: the H1a red-bar vector — *"an issuing endpoint is asked to sign unframed bytes under an issuer key — the reference issuer must **refuse**"* |
| **Residual Layer 2** | **L2-g(a)** implementation fidelity (*"the whole of it — this assumption is a statement about code, not about cryptography"*); **L2-l(a)** cross-protocol domain separation (library D-6 note; S-STANDING review item 27) |
| **Decision** | **LAYER-2(a)**, exposed and unclaimed, **and narrowed on 2026-09-15**: key-use discipline is Layer 2 **only for endpoints outside the modelled ones**. Inside the modelled endpoints the discipline is not an assumption at all — it is the enumeration below, each domain exercised by a named family in a committed model, and domain separation across those tags is a *composed property the capstone must preserve*, not a fact to be assumed. It is still **not** a cross-model entry and no capstone row is claimed: no producer query quantifies over endpoints. S-P7 consumes it and records that *"the assumption holds here by construction and is not tested"* |
| **Source** | `formal/suite/s-p1/RESULTS.md:425-469`; `formal/suite/s-p7/RESULTS.md:583-592`; library D-6 note, `lib/tessera_theory.pvl:62-76`; the tag declarations at `lib/tessera_theory.pvl:149-155` |

### L-07 — the legitimate signing domains (enumeration, 2026-09-15)

Every domain-separation tag the library declares, the message shape
signed under it, the key that signs it, and the family whose committed
models exercise it. Counted mechanically across the suite's committed
`.pv` files: `sign((BYTES, …))` 201 occurrences, `sign((POSS, …))` 170,
`sign((STMT_DIGEST, …))` 140, `sign((TLR, …))` 30, and **no other
`sign((TAG, …))` form anywhere**.

> **[UNSUPPORTED — skeptic 2026-09-15: the four counts, and the "no
> other form anywhere" clause.]** The counted scope is not stated and no
> scope reproduces the figures. Re-counted this session over
> `formal/suite/{s-p1,s-p2,s-p3,s-p7,s-standing,lib}`, all `*.pv`
> (916 files): `BYTES` 2009, `POSS` 1733, `STMT_DIGEST` 1629, `TLR` 248,
> `REFUSAL` **2**, `STMT_DIRECT` 0. Over the top-level `proverif/*.pv`
> only (43 models): 97 / 80 / 71 / 16 / 0 / 0. The nearest scope tried
> (top-level + ablations + probes + diagnostics + S-P3 run1/run2) gives
> 197 / 168 / 138 / 28 — close to but not equal to the cited figures.
> The **qualitative** claim the row rests on survives: the only signing
> tags used anywhere in the suite are `BYTES`, `POSS`, `STMT_DIGEST`,
> `TLR` and `REFUSAL`, and `STMT_DIRECT` is signed nowhere. The
> quantitative claim is not supported as written and either needs its
> scope named or should be dropped; the "no other form **anywhere**"
> clause is false as stated because `sign((REFUSAL, …))` does occur —
> see the `REFUSAL` row.

| Tag (library) | Message shape | Signing key | Exercised by |
|---|---|---|---|
| `STMT_DIRECT` (D-1) | `(STMT_DIRECT, t)` — the authority tuple bound directly | an **authority-channel** key `skS`, never an issuer key | **Declared and unexercised in the suite.** Every suite model uses the digest form; the only mention is a comment (`sp7_q2_degraded_compromised.pv:76`). A capstone or later model that binds directly must use this tag, not `STMT_DIGEST` |
| `STMT_DIGEST` (D-1) | `(STMT_DIGEST, h(t))` — the digest of the authority tuple | an **authority-channel** key `skS` | S-P1, S-P2, S-P3, S-P7, S-STANDING — every model's `AuthorityS` |
| `POSS` (D-3) | `(POSS, m)` — the issuer's own **manifest**, never a fingerprint | the **issuer** key `skI` | S-P1, S-P2, S-P3, S-P7, S-STANDING. A model signing `POSS` over a fingerprint alone is a broken companion **by library definition** |
| `BYTES` | `(BYTES, fb)` — the seven-field `framed(objType, alg, issuerId, kfp, manifestHash, canonVer, payload)` | the **issuer** key `skI`; in S-P7 also a **wrapper** key `skW` over an `OT_WRAPPER` frame, and an `OT_REVIEWREC` signer | S-P1, S-P2, S-P3, S-P7, S-STANDING. Separation *between object kinds* inside this domain is the frame's `objType` field (D-5), not a second tag — which is exactly what S-P7's `TypeConfused` query tests |
| `TLR` (D-6) | `(TLR, (lineage, terminal, declaration))` — the terminal lineage record | the **issuer** key `skI` — the same key that signs `BYTES` and `POSS` | **S-STANDING** (`ss_q1_*.pv:290, :310`). This is the signature the old whitelist wrongly excluded |
| `REFUSAL` (D-6) | the portable refusal record | the **issuer** key | **Declared and unexercised in every committed suite model.** *Narrowed — skeptic 2026-09-15: "anywhere in the suite" is false. `out(c,sign((REFUSAL,body),skI))` appears at `s-standing/proverif/falsification-2026-09-06/scratch/a_foreign_tag.pv:342` and `…/m_foreign_tlr_tag.pv:342` — the reviewer's foreign-tag fixtures, which are exactly the fixtures the paragraph below cites as showing the tag check load-bearing under composition. They are scratch, not models, and nothing registered runs them; the claim is true of the committed models and false of the tree.* Its producer is the A3.9 refusal-decomposition obligation, BAND0-EXIT **E6** (see L-21). Nothing here may claim it checked |

**The composed property.** What the composition must preserve is
**domain separation across these six tags**: a signature made under one
tag never parses as a signature under another, so an issuer key signing
a `TLR` body cannot be replayed as a `BYTES` attestation or a `POSS`
proof, and vice versa. In each single-family fixture this separation is
**inert** — no honest signer emits a foreign tag over another kind's
body — and the library's D-6 note records that it is **load-bearing
under composition**: with an honest `REFUSAL`-tagged signer over a
TLR-shaped body added (the reviewer's `a_foreign_tag` fixture), removing
only the tag check turns the strict standing correspondence red. That
is the capstone's job, and it is L2-l's standing caution against every
single-removal "inert" label.

**What remains Layer 2.** Only the endpoints the suite does not model:
that no *other* endpoint holding an issuer key signs anything outside
this enumeration. No symbolic model in this suite quantifies over such
endpoints, so this half has no producer and is LAYER-2(a)
(implementation fidelity). Its discharge route is the H1a red-bar
vector — *"an issuing endpoint is asked to sign unframed bytes under an
issuer key — the reference issuer must **refuse**"* — outside Band 0.

## L-08 — P8 canonical encoding of the required signature set

| Field | Value |
|---|---|
| **Kind** | **LAYER-2(b)** — internal proof obligation carried as an assumption (canonical encoding pre-P8; cross-track). *Reclassified 2026-09-15, finding 6: discharged by `formal/BAND0-EXIT.md` **E3**, not "forever".* |
| **Consumer** | S-P2's set queries `Stripped`, `SignerForged` |
| **Assumed fact** (quoted, `s-p2:268-274`) | *"P8 canonical encoding of the required set — Layer 2, cross-track, never symbolically discharged … reorder has no query; the set is positional (`signers0`/`signers1`, Q2 lines 82-83); bounds beyond n = 2 and uniqueness are P8's"* |
| **Producer** | None — *"Cites P8 **[proof]** (open) until it exists"* |
| **Shared term** | the `sset` family of `authTuple` |
| **Adversary at the join** | *"A1.3 item 2 at the byte level (reorder, duplicate) — not representable here; Layer 2, unclaimed"* |
| **Residual** | L2-d canonical encoding pre-P8; COVERAGE-MAP row 9 (*"no proof, no vectors"*) |
| **Decision** | **LAYER-2(b)** — no producer query exists on any leg; entering it as cross-model would be the silent-absorption the gate forbids. Unclaimed **today**; when E3's proof and golden vectors exist this entry cites them |
| **Source** | `formal/suite/s-p2/RESULTS.md:268-274`; COVERAGE-MAP row 9 |

## L-09 — Set-completeness relation

| Field | Value |
|---|---|
| **Kind** | **CROSS-MODEL** (consumer: the capstone) |
| **Assumed fact for consumers** (quoted, `s-p2:287-290`) | *"acceptance for manifest `m` implies a signature over the exact framed bytes from every signer `m`'s signed set names, each under that signer's own key, for \|set\| ≤ 2"* — read with §A5.4's meaning: *"every required signer's frame over the same content, in its own frame"* |
| **Producer — cardinality and membership** | S-P2 Q2, `Stripped` and `SignerForged` unreachable (`sp2_q2_degraded_compromised.out:378, 384`). *Line numbers repaired 2026-09-15: the draft cited `:354, 360`, which are the **pre-addendum** positions; the 2026-09-12 §A5.4 addendum shifted every RESULT line in that `.out` (the family file records the current ones at `s-p2/RESULTS.md:671`).* |
| **Producer — common content** (added 2026-09-15, finding 3) | **S-P2 Q6, `Spliced` unreachable** in the same (amended) correct model: `sp2_q2_degraded_compromised.out:1013` `RESULT not event(Spliced(t,fa,fb)) is true`, with `Stripped`/`SignerForged`/`SetAltered`/`Reattributed` unreachable (`:378, :384, :390, :397`) and both `HonestComplete` witnesses reachable (`:561, :778`). Registered green 2026-09-12; `formal/suite/s-p2/RESULTS.md:671` (post-freeze addendum table) and `:676-686`. *The draft promised "every required signer's frame over the same content" while naming only `Stripped` and `SignerForged` as producers — which was precisely the C8 finding.* **Authorship of those bytes under the named key is not produced here; it stays in L-06** |
| **Shared-term mapping for the common-content half** | The **six non-fingerprint fields of the seven-field `framed` constructor, equal across the two signer slots**, established in two different ways and both required: (a) `alg`, `issuerId` and `manifestHash` are pinned to the **shared authority tuple `t`** by the pre-existing per-slot destructuring `let framed(ota, =alg, =id, =fp(kX), mha, cva, pla) = fa in  if mha = h(t)` (`sp2_q2_degraded_compromised.pv:221-224`, the two slots' destructurings and their two `mh = h(t)` checks), so they are equal across slots by construction; (b) `objType`, `canonVer` and `payload` are equated **explicitly** by the §A5.4 addendum's three guards `if ota = otb then` / `if cva = cvb then` / `if pla = plb then` (`:228-230`), which the model's own comment describes as *"the three non-fingerprint frame fields not already pinned through the shared tuple"*. The **seventh** field, `kfp`, is deliberately **not** equal — each slot keeps its own `=fp(kA)` / `=fp(kB)` — which is the L-01 binding, not this relation. The judge is `ContentJudge` on `contentCh`, firing `Spliced(t, fa, fb)` on any of the three disagreements (`:279-284`), fed by the single `out(contentCh, (t, fa, fb))` at the one `Accept2S` point (`:235`) |
| **Consumers named** | *"the capstone (A3.2 chain, per signer, item 3); S-P1 (integrity over bytes presupposes which signatures are required over them); S-P7 (per-layer completeness, A3.2 item 4)"* |
| **Shared term** | *"`authTuple`'s `sset` family, `framed`, the verified keys"* |
| **Adversary at the join** | *"A1.3 with DSKS, sole channel compromised"* |
| **Severing companions** | *"Q3 (cardinality half → `Stripped` red), Q4 (membership half → `SignerForged` red)"* — verified: `sp2_q3_companion_cardinality_ignored.out:520` `Stripped` false with `SignerForged` `:526`, `SetAltered` `:532`, `Reattributed` `:538` true and both witnesses reachable `:702, :922`; `sp2_q4_companion_slot_unbound.out:601` `SignerForged` false with `Stripped` `:353`, `SetAltered` `:608`, `Reattributed` `:615` true and witnesses `:780, :1001`. For the common-content half, Q6-C (`sp2_q6_companion_content_unchecked.out:1213`, red on `Spliced` only, other four true at `:372, :379, :386, :393`, witnesses `:558, :779, :1011`) |
| **Residual Layer 2** | L2-b `fp` idealization (*"the slot match is key equality only under it"*); L2-c `h` idealization; L2-d P8 set encoding (L-08); authorship of the bytes under the named key → **L-06, not Layer 2** (clerk note: the family lists it among residuals; it is another family's producer entry, so it is carried as L-06 and not absorbed) |
| **Decision (A7 §A7.10)** | CROSS-MODEL for the capstone only. **S-P1 is COMPLEMENTARY** — it records *"Multi-signer completeness — S-P2's"* under what it does not discharge, so no S-P1 query is falsified. **S-P7 is COMPLEMENTARY** — no S-P7 query states per-layer completeness (the package-completeness cell is open, COVERAGE-MAP row 8 note 1) |
| **Source** | `formal/suite/s-p2/RESULTS.md:286-299`; §A5.4 reading, `:827-843`; `s-p1:489`; `s-p7:626-631` *(both corrected — skeptic 2026-09-15: `s-p1:485` is the replay sentence and `s-p7:597-598` is the opacity bullet; the quoted declination is at `s-p1:489` and the package-completeness cell at `s-p7:626-631`)* |

## L-10 — Set integrity around an honest key

| Field | Value |
|---|---|
| **Kind** | **COMPLEMENTARY** |
| **Assumed fact** (quoted, `s-p2:301-304`) | *"no honest key is accepted as a signer of a manifest it never signed — the sole-channel adversary cannot alter the signer set or version around an honest key"* |
| **Producer** | S-P2 Q2, `SetAltered` unreachable (`sp2_q2_degraded_compromised.out:390`; *repaired 2026-09-15 from the pre-addendum `:366`*) |
| **Consumer** | *"the relying-party story's degraded-mode cost statement (note 2, last bullet; A4 §A4.6)"* — prose, not a query |
| **Shared term** | *"the manifest term (`authTuple`), `POSS`, the frame's `mh` field"* |
| **Adversary at the join** | A1.3 with DSKS, sole channel compromised |
| **Severing companion** | *"Q5-C2 (both pins removed → red); isolation: C1 and C3 (either pin alone → green)"* — exists and is red, but on S-P2's own query |
| **Residual Layer 2** | L2-c `h` idealization (frame pin); L2-a signature unforgeability (possession pin) |
| **Decision (A7 §A7.10)** | COMPLEMENTARY: the only named consumer is the relying-party story. A prose consumer has no query to falsify, so no capstone row is claimed. The relation is nonetheless the one L-02's routed question turns on |
| **Source** | `formal/suite/s-p2/RESULTS.md:300-311` |

## L-12 — Type-soundness relation

| Field | Value |
|---|---|
| **Kind** | **CROSS-MODEL** (consumer: the capstone) |
| **Assumed fact** (quoted, `s-p7:509-511`) | *"acceptance of framed bytes on a path *as* type `T` implies the bytes' committed `objType` is `T`"* |
| **Producer** | S-P7 Q2/Q1, `TypeConfused` unreachable (`sp7_q2_degraded_compromised.out:527`; *repaired 2026-09-15 from `:505`, which is not a RESULT line*; Q1 `sp7_q1_strict_dns_compromised.out:560`); Q5 at both depths |
| **Consumers named** | *"S-P2 (a signature set over a manifest is not one over an attestation — but see the open cell: the manifest is a non-framed kind), the capstone's per-layer linkage"*. **S-P1 declines the relation** (`s-p1/PREDICTIONS.md` 450-453, frozen `5188e7a`: *"S-P1 consumes nothing from S-P7"*) |
| **Shared term** | *"`objType` in the frame"* |
| **Adversary at the join** | *"A1.3 with DSKS, sole channel compromised, adversary-chosen payloads (a payload may be a `wrap()` term)"* |
| **Severing companions** | *"Q3 (base path) → `TypeConfused` red; ablation a10 (wrapped path) → red"* — Q3 = `sp7_q3_companion_type_unchecked`, `TypeConfused` reachable: `.out:509` is the *goal-reachable* line and `.out:727` the `RESULT … is false`, with `Rescoped` `:744` and `InnerSigTransplanted` `:761` still true and both witnesses reachable `:1067, :1267` *(clarified 2026-09-15: the draft's "509, 727" read as two RESULT lines, which it is not)*; a10 = `ablations/a10_no_wrapper_type.out:723` `is false`, with `Rescoped` `:738`, `InnerSigTransplanted` `:753`, `Reattributed` `:768` still true and both witnesses reachable `:1072, :1270` *(line added — skeptic 2026-09-15)* |
| **Residual Layer 2** | L2-i P8 type-tag bytes *"and that the enumeration's bytes are these eight and no others"*; L2-c `h`, L2-b `fp` idealization; L2-f deterministic signatures; **non-framed kinds unrepresentable (open coverage cell)** |
| **Decision (A7 §A7.10)** | CROSS-MODEL for the capstone's per-layer linkage. **S-P2 is COMPLEMENTARY**: the manifest is a non-framed kind, S-P7's own entry flags the open cell, and no S-P2 query asks a type question (the `ota = otb` equality of Q6 is a within-frame slot comparison, not this relation). **S-P1 is COMPLEMENTARY** by its own frozen declination |
| **Source** | `formal/suite/s-p7/RESULTS.md:495-517`; the 2026-09-06 correction of the consumer list, `:495-506`; COVERAGE-MAP row 8 amendment note 1 |

## L-13 — Scope relation: standing binds to the innermost issuance identity

Offered from both sides: S-P7 produces the identity relation, S-STANDING records the same join as consumer entry C-4. One entry, both cited.

| Field | Value |
|---|---|
| **Kind** | **CROSS-MODEL — restated 2026-09-15 round 4 (finding 2).** *Carried in **§2(a)**, the cross-model matrix, as **D11**.* The round-3 file filed this entry as *"COMPLEMENTARY today; CROSS-MODEL if the capstone registers a wrapped-standing query — ROUTED (R-3)"* and parked it in §2(c). That was wrong: **C-Q1 consumes the innermost-issuer scope relation unconditionally**, as its **link 6b** (§6), in both the strict and the degraded form and under every R-3 formulation. So L-13 has an unconditional capstone consumer and is CROSS-MODEL today. **Its second consumer, C-Q6's wrapped-standing linkage, is still conditional on R-3**, and that half alone is what R-3 now decides for this entry. **R-3 decides only L-16 and L-17** (§5) |
| **Assumed fact** (quoted, `s-p7:527-537`) | *"acceptance of a wrapped presentation with inner bytes `fbI` attributes `fbI` to `(idI, kI)` where `fbI`'s committed `(issuerId, kfp)` is `(idI, fp(kI))`, and honest inner bytes are never attributed to another pair; the honest inner signature term is never **accepted** under another key"* (corrected 2026-09-06, cross-family review item 19: first *"never verified"*) |
| **Consumer-side statement** (quoted, `s-standing:517-523`) | C-4: *"a TLR is never accepted as another object type … a wrapped bundle's standing is evaluated against the innermost issuance identity (F5 boundary). This model exhibits the identity-binding half; the re-scoping half is S-P7's."* |
| **Producer** | S-P7 Q2 and Q5, `Rescoped`/`RescopedD1`/`RescopedD2` unreachable; `InnerSigTransplanted` unreachable (`sp7_q2_degraded_compromised.out:540` and `:553`; *repaired 2026-09-15 from `:518, 531`, neither of which is a RESULT line*) |
| **Shared term** | *"attributed key, attributed identity, inner framed bytes, inner signature term"*; on the consumer side *"the `TLR` domain-separation tag and the object type (`OT_TLR`, declared and unexercised)"* |
| **Adversary at the join** | *"A1.3 with DSKS, sole channel compromised, adversary-authorized wrapper, depth ≤ 2"*; consumer side: *"A1.3 item 4 (re-frames objects across the P7 type boundaries)"* |
| **Severing companions** | *"Q6a (identity, `Rescoped` red, no DSKS), Q6b (key/authority — `Rescoped` red by the re-sign route, no DSKS; `InnerSigTransplanted` red **via `dsks`**), Q5c (depth, `RescopedD2` red only)"* — all three exist and are red; verified 2026-09-15: Q6a `.out:806` `Rescoped` false with `TypeConfused` `:503` and `InnerSigTransplanted` `:819` true, witnesses `:1118, :1314`; Q6b `.out:769` `Rescoped` false **and** `:1058` `InnerSigTransplanted` false, `TypeConfused` `:489` true, witnesses `:1317, :1508`; Q5c `.out:1131` `RescopedD2` false only, `RescopedD1` `:690` and `InnerSigTransplanted` `:1169` true, witnesses `:1496, :1876, :2097` |
| **Residual Layer 2** | As L-12, plus **depth bounded at 2** (named scoping); L2-b `fp` collision resistance and what a fingerprint hashes (P8) |
| **Decision (A7 §A7.10)** | **Repaired 2026-09-14.** The first draft said *"S-STANDING's fixture contains no wrapper"* — inaccurate: S-STANDING declares `wrapCore` and its companion exercises a **wrapper-shaped transplant** (`S/wrap_routes.out:1827, 1944, 1951` — verified: `:1827` `is true`, `:1944` `is false`, `:1951` `is true`; `s-standing:1335-1348`, *corrected from `:1338-1352` — skeptic 2026-09-15*). What S-STANDING's wrapper-shaped term establishes is that a core presented under a `wrapCore` shape gains no established standing — by `h` injectivity (F5), inside S-STANDING's own algebra. What it does **not** establish is the **composition**: S-P7's wrapper *processing* (unwrap, inner attribution, depth) feeding S-STANDING's standing assessment. No S-STANDING registered query ranges over that composition, so severing S-P7's scope relation falsifies none of them, and under the rule as written the pair is **COMPLEMENTARY**. It becomes CROSS-MODEL the moment the capstone registers a wrapped-standing linkage query over the composed fixture — which the A7 2026-09-06 ruling (*"S-STANDING carries the wrapper-shaped transplant; S-P7 supplies the identity relation it composes with"*) points toward but does not require. Routed. **[Consistency, skeptic 2026-09-15 — REPAIRED 2026-09-15 round 3.]** The defect as recorded: this entry is COMPLEMENTARY today, yet D11 sat inside §2, a table whose preamble read *"CROSS-MODEL entries only"*, while L-16 and L-17 — routed on the same question — were given **no** row and their D12/D13 existed only as §5 prose; the register used both conventions at once and the §2 count of 11 depended on which was chosen. **The repair:** §2 is split, and L-13, L-16 and L-17 are carried together in **§2(c), "Conditional on R-3"**, outside the cross-model matrix and outside its counts, as D11, D12 and D13. One convention, applied to all three. Also note: S-STANDING *does* carry one registered query over a wrapper term — `EstablishedWrapped ⟹ Designated` — but only inside the **companion** `ss_q2_companionA_identity_declared.pv` (`.out:1176`, red as registered), so there is no green producer of it and the "no query ranges over the composition" finding is unchanged. **[Routing restated 2026-09-15 round 4, finding 2.]** Everything above about the *composition* stands: no S-STANDING query ranges over S-P7's wrapper processing feeding S-STANDING's assessment, and that gap is still R-3's. What the round-3 text got wrong is the **consequence**: it concluded that L-13's capstone consumption waits on R-3. It does not. C-Q1's link 6b — *for `lyr ≠ L0` the inner frame's `(issuerId, kfp)` is the innermost issuance identity, not the wrapper's* — consumes this relation under every formulation, so severing S-P7's scope relation falsifies C-Q1 whether or not C-Q6 is ever written. **L-13 is CROSS-MODEL today, D11 is a matrix row, and R-3 reaches only L-16 and L-17.** The link is also shown to be **independent of link 6a (object type)** by S-P7's own Q6b companion: `TypeConfused` stays `is true` (`sp7_q6b_companion_key_outermost.out:489`) while `Rescoped` goes `is false` (`:769`) and both honest witnesses stay reachable (`:1317`, `:1508`) |
| **Source** | `formal/suite/s-p7/RESULTS.md:518-544`; `formal/suite/s-standing/RESULTS.md:516-526`; ENUMERATION note 4 item 2 |

## L-14 — Commitment relation (by construction, not a producer)

| Field | Value |
|---|---|
| **Kind** | **COMPLEMENTARY** — the family gives every conservation field as "none" |
| **Assumed fact** | *"none stated (no query asserts 'wrapping never alters the inner verdict'; the witness/control pair below is companion evidence only)"* |
| **Producer / consumer** | *"none; by construction, not a producer"* / *"none; **S-P1 may not consume**"* |
| **Shared term / adversary** | *"inner framed bytes"*; as L-13, and strict mode for Q4 per divergence 1 |
| **Companion evidence (not discharge)** | `HonestWrappedAccepted` reachable (Q1, Q2, Q5, Q4-isolation, Q4-control); Q4's two-version red as the control. *"discharges nothing of the property"* |
| **Residual Layer 2** | L2-j opacity of the concrete embedding (P8/H1a) — *"the largest Layer 2 residual here"* |
| **Decision** | Entered as a **no-dependency record**, not a row. The red-bar risk is a reader taking the by-construction encoding for a producer query; the entry exists to prevent it |
| **Source** | `formal/suite/s-p7/RESULTS.md:545-568` |

## L-16 — P-1, standing relation

| Field | Value |
|---|---|
| **Kind** | **CROSS-MODEL — RULED (author), 2026-09-15 (R-3 = formulation W: the composition query concludes in a standing verdict)**. *Was COMPLEMENTARY today / ROUTED (R-3) until the ruling; the reasoning is kept below. The consuming query still exists in no model, so the row is NOT YET SHOWN.*. *Added 2026-09-15 (finding 4): the draft classified this COMPLEMENTARY without recording that R-3's answer can consume it. Under R-3 formulation W it becomes **D12**, carried in **§2(c)**; under formulation N it stays as written. Both outcomes are in §5's combined-consequences table. Round 3: D12's full row is now written out in §2(c) rather than existing only as §5 prose.* |
| **Assumed fact for consumers** (quoted, `s-standing:435-440`) | *"an `ESTABLISHED` standing report computed against an honest entitled key `kH` for an artifact with derived identity `aid` implies the issuer holding `kH` signed one TLR whose lineage contains `aid` and whose terminal designates `aid`"* |
| **Producer** | S-STANDING Q1 (i)/(ii), both variants, `Established ==> Designated` true (`ss_q1_strict_dns_compromised.out:503, :513, :523`); N1 reachable (`:829`) |
| **Consumers named** | *"the A3.8 base assessment's `protocol_standing` dimension; the relying-party story …; the integrated adversarial lifecycle model (A3.9, pre-H1a-freeze) …; S-P7's innermost-identity claim"* |
| **Shared term** | *"entitled key, derived identity `h(core)`, TLR"* |
| **Adversary at the join** | *"A1.3 with DSKS expressible (D-4), one of two channels compromised (both variants), possession free"* |
| **Severing companions** | *"Q2 (identity declared) → (i)/(ii) red; Q4 (terminal unchecked) → (i)/(ii) red; ablation abl6 (TLR unsigned) → red"* — all exist and are red; verified 2026-09-15: Q2 `.out:630, :808, :986` all `is false` with `StandingUnentitled` `:1182` still true and the witness reachable `:1514`; Q4 `.out:576, :849, :1123` all `is false`, `StandingUnentitled` `:1129` true, witness `:1425`; abl6 `ablations/abl6_no_tlr_signature.out:616, :788, :960` all `is false`, `StandingUnentitled` `:966` true, witness `:1297` *(abl6 lines added — skeptic 2026-09-15; the row said "red" with no result cited)* |
| **Residual Layer 2** | L2-c `h` injectivity — *"**the whole load of the transplant result**"*; L2-b `fp` injectivity; L2-d P8's *"what bytes are the core"* and their canonical encoding (L-20); L2-f deterministic signatures; **lineages of exactly two entries (n = 2 does not generalize)** — named scoping |
| **Decision (A7 §A7.10)** | COMPLEMENTARY **as the register stands**: every named consumer is prose (A3.8 assessment, relying-party story), a post-Band-0 model (A3.9, explicitly not a Band 0 gate), or S-P7 — which registers no standing query (*"What S-P7 does not discharge: Standing, lineage, terminal disposition, the TLR"*). No **currently registered** query is falsified by severing. **Routed with R-3:** a composition query whose conclusion is a standing verdict *is* falsified by severing, and this entry becomes D12 |
| **Source** | `formal/suite/s-standing/RESULTS.md:434-452`; `formal/suite/s-p7/RESULTS.md:611` |

## L-17 — P-2, entitled key inside the standing path

| Field | Value |
|---|---|
| **Kind** | **CROSS-MODEL — RULED (author), 2026-09-15 (R-3 = formulation W: the composition query concludes in a standing verdict)**. *Was COMPLEMENTARY today / ROUTED (R-3) until the ruling; the reasoning is kept below. The consuming query still exists in no model, so the row is NOT YET SHOWN.*. *Added 2026-09-15 (finding 4): under R-3 formulation W it becomes **D13**, carried in **§2(c)**; under N it stays as written. Round 3: D13's full row is now written out in §2(c).* |
| **Assumed fact** (quoted, `s-standing:456-458`) | *"`Established(kX, t, aid)` implies `fp(kX) = kfpr(t)` for the evidenced `t`"* |
| **Producer** | S-STANDING Q1 (iii), `StandingUnentitled` unreachable, both variants and Q1d (`ss_q1_strict_dns_compromised.out:530`, `ss_q1_strict_repo_compromised.out:530`, `ss_q1d_degraded_compromised.out:664` — *the repo and Q1d lines added, skeptic 2026-09-15*) |
| **Consumer** | *"the H1a conformance profile (the blind re-scoring's note, ENUMERATION note 4 item 2, becomes a checked shape)"* — a vector-track consumer, not a symbolic query |
| **Shared term** | *"the accepted standing key `kX`; the evidenced tuple `t` (its `kfpr` field)"* |
| **Adversary at the join** | *"A1.3, one of two channels compromised (both strict variants) and, for Q1d, the sole channel compromised; DSKS expressible (D-4); possession free"* |
| **Severing companion** | *"Q3 → `StandingUnentitled` red"* — `ss_q3_companionB_entitled_via_envelope.out:860` `is false`, with Q1(i) `:628` also red and (ii)/(iii)'s per-key forms `:642, :656` still true, witness reachable `:1157` |
| **Residual Layer 2** | L2-b `fp` idealization (library header); **L-01** for what *"the evidenced tuple names the key"* rests on (carried as a register entry, not absorbed as Layer 2) |
| **Decision (A7 §A7.10)** | COMPLEMENTARY **as the register stands** — the consumer is the H1a profile, which has no query to falsify. **Routed with R-3:** under formulation W the capstone's composition query consumes the entitled-key half and this entry becomes D13 |
| **Source** | `formal/suite/s-standing/RESULTS.md:454-466` |

## L-18 — P-3, degraded boundary (a cost, not a guarantee)

| Field | Value |
|---|---|
| **Kind** | **COMPLEMENTARY** — a registered cost, never a row, by the family's own statement |
| **Assumed fact** (quoted, `s-standing:469-476`) | *"in degraded mode with the sole channel compromised, no `ESTABLISHED` is computed against an honest key for an identity that key's holder did not designate, and none against a key the presented tuple does not name; the unrestricted sentence does **not** hold (Q1d (i) red) and is the A4.6 cost"* |
| **Producer / consumer** | S-STANDING Q1d (ii), (iii) → *"the relying-party story's degraded-mode paragraph"* (prose). Verified, skeptic 2026-09-15: `ss_q1d_degraded_compromised.out` (i) `:640` `is false` (the registered A4.6 cost), (ii) `:649` and `:658` `is true`, (iii) `StandingUnentitled` `:664` `is true`, witness `:950` reachable *(no result line was cited)* |
| **Severing companion** | *"No severing companion is owed for a cost"* |
| **Adversary at the join** | *"A1.3 with the *sole* authority channel compromised — a fixture strictly stronger than item 6's 'proper subset' (S-P3 F6); DSKS expressible; possession free"*. Residual: as L-16 |
| **Source** | `formal/suite/s-standing/RESULTS.md:467-479` |

## L-19 — C-2, TLR anchor temporal validity

| Field | Value |
|---|---|
| **Kind** | **CROSS-FORMALISM** — never symbolically dischargeable |
| **Assumed fact** (quoted, `s-standing:498-499`; *corrected from `:500-503` — skeptic 2026-09-15*) | *"a TLR reported `ESTABLISHED` passed that predicate"* — the A2.1 confirmation predicate applied per SC-1 to the TLR's own anchor against `declTerminal` |
| **Producer** | *"the A2.1 predicate as modeled in the P5c bridge family"* — `formal/tla/P5c_IssuanceProtocol.tla` (`ShippedIsSound`, `ExpiredCannotShip`) with `formal/tla/P5cP5P6_Bridge.tla` (`PinAgreement`, `ShippedDesignatedAgree`, `LateBurialRejected`); whether SC-1 needs its own TLA+ instance is COVERAGE-MAP row 13's open cell (disposition B8) |
| **Shared term** | *"anchor valid"* |
| **Adversary at the join** | *"A1.3 item 5 (the adversary anchors anything; anchoring proves existence at a time, not authority); time is not represented here"* |
| **Severing companion** | None claimable |
| **Residual** | L2-k historical trust-anchor correctness and L2-m chain availability (A1.6 Bitcoin/OTS, the `[assumption]` half of rows 5–6); the symbolic model's *"anchor-proof check is inert (abl2) and its `STANDING_EVIDENCE_TEMPORAL_MISMATCH` code is vocabulary only"* |
| **Red bar** | *"**Must never be marked discharged by anything in this directory**"* (ENUMERATION §4; Sol finding 2) |
| **Source** | `formal/suite/s-standing/RESULTS.md:495-507`; `ENUMERATION.md:135-147`; COVERAGE-MAP rows 5, 6, 13 |

## L-20 — C-3, canonicalization injectivity and the core's byte composition

| Field | Value |
|---|---|
| **Kind** | **LAYER-2(b)** — internal proof obligation carried as an assumption (canonical encoding pre-P8). *Reclassified 2026-09-15, finding 6: discharged by `formal/BAND0-EXIT.md` **E3**.* |
| **Assumed fact** (quoted, `s-standing:509-513`) | *"two distinct attempts have distinct cores and the verifier reconstructs the core bytes exactly; `attemptCore(t, ppf, sg, decl)` is a perfectly parsed 4-tuple, not a byte format"* |
| **Producer** | None — P8, *"Layer 2 — unclaimed"* |
| **Shared term** | *"the core bytes and their digest `h(core)`"* |
| **Adversary at the join** | *"A1.3 item 1 (alters any bytes after issue)"* |
| **Residual** | L2-d canonical encoding and the core's byte composition (P8); COVERAGE-MAP row 9 |
| **Decision** | **LAYER-2(b)**, discharged by E3. Note the coupling: L-16 states that `h` injectivity is *"the whole load of the transplant result"*, and this entry is the unclaimed assumption that makes the symbolic `h` stand for the concrete digest. The `h`-hardness half of that coupling is **L2-c, LAYER-2(a)** and stays permanent; only the *what-bytes-are-the-core* half moves to (b) |
| **Source** | `formal/suite/s-standing/RESULTS.md:508-515` |

## L-21 — C-5, SC-2's one-signing-act commitment

| Field | Value |
|---|---|
| **Kind** | **CROSS-FORMALISM** — producer not yet built |
| **Assumed fact** (quoted, `s-standing:528-530`) | *"the TLR's terminal disposition *is* the disposition fact the A3.7.2 refusal record also projects"* |
| **Producer** | *"Not modeled; the A3.9 refusal-decomposition obligation (TLA+)"* — nearest existing producer is the P5c refusal latch (`P5c_IssuanceProtocol.tla`, `RefusedOnlyWhenExhausted`, action `RefusalLatched`), the §4 join the A7 ruling assigns to S-STANDING (see L-15). The §A3.7.2 extended atomic-entry invariant is BAND0-EXIT item E6 and has no TRK row |
| **Shared term** | *"the terminal disposition"* |
| **Adversary at the join** | *"none symbolic (a specification commitment, not an attack surface here)"* |
| **Residual** | *"Layer 2 — unclaimed until the A3.9 TLA+ obligation"* — registered 2026-09-15 as **L2-n, LAYER-2(b)**, discharged by `formal/BAND0-EXIT.md` **E6** |
| **Decision** | CROSS-FORMALISM, not LAYER-2: the producer is a named TLA+ obligation, not a primitive assumption. It cannot be a capstone row — ProVerif cannot consume it — and its producer does not yet exist (E6) |
| **Source** | `formal/suite/s-standing/RESULTS.md:527-538`; `formal/BAND0-EXIT.md` E6; COVERAGE-MAP row 6 OPEN cell |

## L-22 — first-link Q2 broken companion

| Field | Value |
|---|---|
| **Kind** | **COMPLEMENTARY** (companion record; no assumed fact) |
| **Quoted** | *"Mutation: evidence binds issuer identity only (proper subset of map v1). Expected failing query: chain correspondence + TwoWorldsBroken reachability — both failed/fired as required, both variants. Does not discharge anything; exists to prove the queries can go red."* |
| **Finding carried** | *"the first-link binding defends against a strictly stronger adversary than channel compromise — losing it is worse than losing a channel"* (`first-link:70-72`; *corrected from `:66-70` — skeptic 2026-09-15*) — the companion's attack uses only honest evidence objects |
| **Role in the matrix** | It is the severing companion for **L-23**, not for L-04 |
| **Source** | `formal/spike/first-link/RESULTS.md:105-109`, `:63-70` |

## L-23 — first-link Q4 attack objective / §A3.2.1 boundary invariant

| Field | Value |
|---|---|
| **Kind** | **CROSS-MODEL** (consumer: the capstone) |
| **Assumed fact** | The §A3.2.1 boundary invariant holds: one evidence object supports exactly one authority-relevant tuple. Quoted: *"Mechanism intact; TwoWorldsBroken unreachable, both variants"* |
| **Consumer** | *"§A3.2.1 boundary invariant"* — carried into the capstone's linkage query for the first link |
| **Producer** | first-link `q4_*` (attack objective), `TwoWorldsBroken` unreachable, both variants (`q4_attack_{dns,repo}_compromised.out:97`); Q6 × 4 unreachable, single-object form (`q6_single_dns_honest.out:91`, `q6_single_dns_compromised.out:93`, `q6r_single_repo_honest.out:91`, `q6r_single_repo_compromised.out:93`) *(lines added — skeptic 2026-09-15)* |
| **Shared term** | the authority tuple and its evidence object (map v1, frozen) |
| **Adversary at the join** | one channel key leaked (both variants); per L-26 the Q6 half holds *"even under full compromise of the accepted channel"* |
| **Severing companion** | **L-22** (Q2, evidence binds issuer identity only) — exists, red on chain correspondence (`q2_broken_{dns,repo}_compromised.out:243`) + `TwoWorldsBroken` (`:464`), both variants *(lines added — skeptic 2026-09-15)* |
| **Expected red at the capstone** | the capstone's first-link linkage query, under the L-22 mutation transcribed |
| **Residual Layer 2** | L2-c concrete digest collision resistance (*"Same Layer 2 residual as Q3"*) |
| **Scope limit carried from L-24** | the pair result covers strict two-channel mode only; single-evidence acceptance has its own coverage (Addendum 1) |
| **Source** | `formal/spike/first-link/RESULTS.md:110-112`, `:113-128`, `:129-161` |

## L-24 / L-25 / L-26 — first-link scope and residual records

| Register | Kind | Quoted | Effect on the register |
|---|---|---|---|
| **L-24** | COMPLEMENTARY (scope record; a retraction) | *"A prior version of this entry claimed the per-single-evidence formulation was 'strictly implied' by the pair result. **That claim is false** … The pair result covers strict two-channel mode only."* (`first-link:113-128`) | The capstone's boundary judge is the **pair** form only; single-evidence acceptance is a live `VALID_DEGRADED` path with its own coverage (Q5–Q8, Addendum 1), and Q5b/Q5r-compromised is a **registered red** — *"when the sole accepted evidence channel is the compromised one, no provenance guarantee survives"* (the A1.2.1 waiver cost, not a defect) |
| **L-25** | **LAYER-2** (cryptographic primitive security) | *"(5) Q5/Q6 consume the same Layer 2 digest-collision-resistance residual as Q3/Q4."* (`first-link:163-164`) | No producer: *"symbolic h is injective by construction; discharged by cited external hardness assumptions per prereg §8, never by these models"* — L2-c |
| **L-26** | COMPLEMENTARY (narrowing record on L-04) | *"(6) Q6's unconditional result explicitly does NOT depend on the A1.3 'never all' assumption — the boundary invariant holds per-object even under full compromise of the accepted channel; only provenance (Q5) needs 'the accepted channel is honest.'"* (`first-link:164-171`) | L-04's operational-channel-independence residual (L2-h) is scoped to the **provenance** half of the chain; the capstone must not attach L2-h to the boundary row (D9) |

---

# 2. Discharge matrix (draft)

**Nothing in any table below is discharged.** Every "expected red" is
either (i) shown by a committed family `.out` on the **consumer's own**
query, (ii) shown by a 2026-09-14 or 2026-09-15 scratch run on a copy
(unregistered probe; the capstone must still register it), or (iii)
marked **NOT YET SHOWN**. *Repaired 2026-09-14 after the first Codex
review: the first draft asserted five reds it had not run, and named
companions that severed a different fact from the one the row claims.*

**Shape changed 2026-09-15, round 3 (finding 5 + the skeptic's D11
convention finding).** The draft kept one table declared *"CROSS-MODEL
entries only"* while parking inside it rows whose CROSS-MODEL status a
routed fork had not decided, and parking outside it other rows routed
on the **same** fork. Both conventions were in use at once. The table is
now split three ways, and every entry sits in exactly one part:

- **2(a) — the cross-model matrix.** Rows whose CROSS-MODEL status the
  record settles. **Eleven rows** — D1–D11 — under the author's ruling
  of 2026-09-15 *(nine at round 4, which moved **D11** in; D1 and D2
  joined them when R-1 was ruled Reading B and R-2 "yes")*.
- **2(b) — VACATED.** This part held D1 and D2 out of the matrix while
  R-1 was open. **R-1 is ruled Reading B (composed), 2026-09-15**, and
  R-2 is ruled "yes", so D1 and D2 are matrix rows in 2(a) and **2(b) is
  empty**. Its preamble is kept as the record of why they were once held
  out, and of what the ruling changed.
- **2(c) — the standing-verdict rows.** D12 and D13, whose existence R-3
  decided: **R-3 is ruled formulation W, 2026-09-15**, so both are rows.
  Their consuming query exists in no model, so both are **NOT YET
  SHOWN**. They are rows of 2(c), outside the cross-model matrix and
  outside its count.

**Shape changed again 2026-09-15, round 4 (finding 2): D11 moves from
2(c) into the matrix.** The round-3 file put D11 (L-13, the
innermost-issuer scope relation) in 2(c) because its only named
consumer was C-Q6, whose existence R-3 decides. That was wrong once
C-Q1's contract was read properly: **C-Q1 consumes scope
unconditionally**, in both its strict and its degraded form, and under
every R-3 formulation, as its link 6b — *for `lyr ≠ L0` the inner
frame's `(issuerId, kfp)` is the innermost issuance identity, not the
wrapper's*. Severing S-P7's scope relation falsifies C-Q1's link 6b
whether or not the capstone ever registers C-Q6. So L-13's consumption
does **not** wait on R-3, D11 is a matrix row in every outcome, and
**R-3 now decides only the standing conjuncts** — L-16 and L-17, rows
D12 and D13 (§5, R-3). D11 keeps its second, conditional consumer
(C-Q6's wrapped-standing linkage) and that half is still conditional;
the row is in the matrix on the C-Q1 half, which is not.

**The register's default reading, stated once so the counts have a
referent — RULED (author), 2026-09-15: outcome 5.** The three forks are
no longer open and the counts below are no longer a clerk's default.
**R-1 = Reading B, "composed"** — the capstone builds one verifier
carrying both families' checks, so L-01 → S-P2 and L-01 → S-P7 are
capstone-internal joins and **D1 and D2 are matrix rows**, with `m4` and
`s4` registered as the capstone's own companions **C-C2** and **C-C4**.
**R-2 = "yes"** — a jointly-sufficient pin is a dependency, so **D10 is
a matrix row** (and D1/D2 clear the second condition R-1 Reading B
leaves them). **R-3 = formulation W** — the capstone's composition query
concludes in a *standing verdict*, so L-16 and L-17 are consumed and
**D12 and D13 are rows of §2(c)**. D11 is a matrix row under every
outcome and is unaffected (round 4, finding 2: C-Q1's link 6b consumes
L-13's scope relation unconditionally). The author's words and the
instrument are at the head of §5; the outcome is **row 5** of §5's
combined-consequences table. **Ruling the forks settles classification
and nothing else** — no row below is discharged, and the three rows
whose producer does not yet exist (D5, D6, D10) are `prov(P)` under this
reading exactly as they were under every other.

## 2(a). The cross-model matrix

CROSS-MODEL entries only, under the ruled reading above (outcome 5).
**D1 and D2 were moved in here from §2(b) on 2026-09-15 by the author's
ruling** — R-1 = Reading B (composed), R-2 = "yes" — and their cells are
carried across as written, with the R-1/R-2 conditions marked as ruled
rather than open.


| # | Consumer entry (query) | Producer query (state today) | Severing companion — the mutation that removes **the named producer fact** | Expected red | Evidence state | What `capstone.pv` must transcribe |
|---|---|---|---|---|---|---|
| **D1** *(moved from §2(b) 2026-09-15 by the author's ruling: R-1 = Reading B **and** R-2 = "yes" — outcome 5)* | L-01 → S-P2 Q2 carried `Reattributed` (`sp2_q2_degraded_compromised.pv:268-273`; corrected from the pre-addendum `:229-233`, skeptic 2026-09-15) | S-P3 Q2 `Reattributed` unreachable — **exists, green**. *Under Reading A this was not the row's producer: severing it leaves the consumer's query green (`base_sp2.out:397`). Under the **ruled** Reading B the capstone composes both families' checks into one verifier, the producer's fact and the consumer's query live in the same model, and severing the one does falsify the other* | **C-C2**, the minimal two-removal severing of the complete binding relation: frame pin `=fp(k_)` **+** manifest-hash equality. **Not** the frame pin alone — that leaves the query green. *(Corrected — skeptic 2026-09-15: this cell once offered "or all three removals with the tuple fingerprint match" as an alternative, which §6's C-C2 **withdrew** under finding 5 because `m7_all_three.out:625` reds `SignerForged`, a guarantee this row requires green. §2 and §6 agree.)* Under the ruling, `m4` **is the capstone's own companion** | `Reattributed` | **SHOWN IN SCRATCH** — `m4_framepin_mh.out:620` reachable, red on exactly `Reattributed`, witnesses reachable `:791`, `:1015`, `:1250`; `m7_all_three.out:860` also reachable but additionally reds `SignerForged` `:625`. Capstone must register it | `framed` (7-arg, model-local, NOT promoted — copy verbatim), `authTuple` (D-2), `fp`, `h`, `dsks` (D-4), `sset` slot pattern. **History:** the 2026-09-14 draft counted this row firm; the first 2026-09-15 repair made it provisional on R-2 alone; round 3 held it out of the matrix under R-1 "as written". **The author ruled both forks on 2026-09-15 — Reading B and "yes" — so the row is firm and this is its final classification under §5.** |
| **D2** *(moved from §2(b) 2026-09-15 by the author's ruling: R-1 = Reading B **and** R-2 = "yes" — outcome 5)* | L-01 → S-P7 Q2 `Rescoped` (key half) | S-P3 Q2 `Reattributed` unreachable — **exists, green**. *As for D1: severing it leaves the consumer's query green in the uncomposed models (`base_sp7.out:540`); under the ruled Reading B the join is internal to the capstone's single verifier* | **C-C4**, the same complete severing inside `InnerCheck`: inner `=fp(kI)` pin **+** `mhI = h(tI)`. **Not Q6b** — Q6b severs the scope relation, a different fact. Under the ruling, `s4` **is the capstone's own companion** | `Rescoped` | **SHOWN IN SCRATCH** — `s4_innerfp_mh.out:864` reachable (inner pin alone leaves it green, `s3_innerfp.out:540`); `InnerSigTransplanted` `:1207` and `Reattributed` `:1431` also red, so it is **not** red on exactly one query — see C-C4's three-set specification in §6. Capstone must register it | `framed`, `fp`, `h`, `wrap()` + `InnerCheck` idiom, `dsks`, `OT_ATTEST`/`OT_WRAPPER` (D-5). **History as for D1; ruled firm 2026-09-15 (outcome 5).** |
| **D3** | L-04 → S-P1 Q1(i) `Accept ⟹ IssuerSigned` (`.out:201` true) | S-P3 Q1(ii) chain correspondence, `sp3_q1_strict_{dns,repo}_compromised.out:424` — **exists, green** | **C-C1**, both channel keys public: `out(c, skD); out(c, skR)` in place of the single leak | Q1(i) `Accept ⟹ IssuerSigned` red; `AcceptedUnderHonestKey ⟹ IssuerSigned` green; N1 reachable | **SHOWN IN SCRATCH** — `s6_bothchannels.out:361` `is false` (baseline `base_sp1q1.out:201` `is true`); honest-key correspondence stays green `:368`; `HonestAccepted` reachable `:559`. This is the family's own registered-but-unrun prediction, now observed on a copy; S-P1's record is unchanged and still reads *"Not run"* | `STMT_DIRECT`/`STMT_DIGEST` (D-1), `authTuple` (D-2), `POSS` over the manifest (D-3), both channel keys, `h` |
| **D4** | L-04 → capstone first link (§A3.2 item 1), **now two conjuncts** (round 4, finding 3): C-Q1's **link 1a** (the accepted evidence is bound to this acceptance's statement, asserted in **both** modes) and **link 1b** (an uncompromised authority channel published the tuple, strict only) | as D3 — **exists, green** for link 1b. Link 1a names no producer and claims none: it is a structural conjunct of the capstone's own verifier | **Two companions, one per conjunct.** Link 1b: as D3 (**C-C1**). Link 1a: **C-C10** (§6, new round 4, finding 3) — the degraded verifier's evidence check removed and nothing else, which reds the evidence-binding conjunct (`cq1b_sp1_evidence_unchecked.out:466` `is false`) while C-Q7 (`:301`), both C-Q8 forms (`:307`, `:313`) and honest-key authorship (`:474`) keep their baseline outcomes and the witness stays reachable (`:638`). **C-C1 does not reach link 1a** | the capstone linkage query's first link, **both conjuncts** | **NOT YET SHOWN** — the consuming query does not exist. The mutation is verified (D3); the consumer is not built | as D3 |
| **D5** *(provisional — producer not yet registered)* | L-06 → S-P7 Q2 `InnerSigTransplanted` | **NOT YET REGISTERED.** S-P1 Q2(i) `AcceptedUnderHonestKey ⟹ IssuerSigned` (`sp1_q2_*.out:173`) exists and is green but **does not establish the relation this row consumes** — shown 2026-09-15: under a conditional unbinding, Q2(i) stays green (`d5a_sp1_condunbind.out:195`) and S-P3's `Reattributed` stays green while `InnerSigTransplanted` goes red (`d5b_sp7_condunbind.out:654, :1060, :1037`). The producer is **C-Q7**, the signature-term judge the capstone must register (L-06; feasibility `d5c_sp1_sigjudge.out:203` green, `d5d_sp1_sigjudge_condunbind.out:414` red). **C-Q7 serves this row only** (round 3, finding 1): it observes `(acceptedKey, signature)` and is blind to different bytes under the same key, so it is **not** D6's producer | **C-C5**, S-P1's Q3 mutation transcribed into `InnerCheck`: the inner signature no longer bound to the presented bytes. **Not Q6b** — key substitution and an unbound signature are different failures | `InnerSigTransplanted` | **MUTATION SHOWN, PRODUCER NOT REGISTERED** — `s1_sig_unbound.out:897` reachable, red on **exactly** `InnerSigTransplanted` (`TypeConfused` `:537`, `Rescoped` `:560`, `Reattributed` `:920`, `VersionLied` `:1464` green), both witnesses reachable `:1233`, `:1442`. *Retagged 2026-09-15 (finding 1): this is evidence that **byte binding matters** — the consumer query is falsifiable by severing it — **not** the discharge of the join, because no committed producer query establishes the severed fact.* The capstone must register **both** C-Q7 and this companion | `framed`, `sign`/`checksign`, `BYTES` tag, `wrap()`, `InnerCheck`, `dsks` (D-4) |
| **D6** *(provisional — producer not yet registered)* | L-06 → capstone chain last link — the **R-bytes** relation (L-06): **a signature accepted under key `kX` over presented bytes `fb` verifies under `kX` over exactly `fb`** — `checksign(sg, kX) = (BYTES, fb)`. *(Wording corrected 2026-09-15 after the ruling: the cell read "was produced by `kX`'s holder over exactly `fb`", which overstates what C-Q8's predicate establishes — `tessera_theory.pvl:110-115` permits a signature to verify under an alternative key. Authorship stays S-P1's Q2(i); anti-transplant stays C-Q7's.)* | **NOT YET REGISTERED — producer to be registered in the capstone.** *Repaired 2026-09-15 round 3 (finding 1): the previous cell read "as D5", i.e. C-Q7. **C-Q7 is not this row's producer.** It observes `(acceptedKey, signature)` and cannot see different bytes presented under the **same** key: under a same-key byte unbinding, C-Q7 stays green (`d6b_sp1_q8_samekey_unbound.out:246` `is true`) while S-P1's own authorship goes red (`:593` `is false`).* The producer the capstone must register is **C-Q8** (§6), the three-place judge over *(accepting key, signature term, presented framed bytes)*. **Rewritten 2026-09-15 round 4 (finding 1):** C-Q8 must be a **structural** judge over **every** accepted triple, **including failed verification**, not a judge over honest-released signature terms — the round-3, honest-filtered form is escaped by keeping byte equality for `OT_ATTEST` frames and waiving it for every other signed frame type, which leaves that form green (`d6d_sp1_q8_type_conditional_unbound.out:315` `is true`) while the exact byte relation fails (`:507` `is false`) and the honest witness stays reachable (`:692`). Feasibility of the rewritten judge: green on the committed verifier (`d6c_sp1_q8_judge_all.out:284`), red under both companion configurations (`d6d:507`, `d6e_sp1_q8all_samekey_unbound.out:643`). Nothing further is claimed | **C-C7** (§6), **now two configurations** (round 4, finding 1): **(i)** the same-key byte unbinding — the signature must verify under `kX` over *some* frame naming `fp(kX)`, not over the presented bytes (`d6e:643` red, C-Q7 green `:274`, witness `:989`); **(ii)** the **type-conditional** unbinding — byte equality kept for `OT_ATTEST` frames only (`d6d:507` red while the withdrawn round-3 form `:315`, C-Q7 `:308` and honest-key authorship `:515` all stay green, witness `:692`). S-P1 Q3 `sp1_q3_companionA_sig_unbound` also exists and is red (`.out:331`) but on S-P1's own query, and it is the **full**, not the same-key, unbinding | the capstone linkage query's last link | **NOT YET SHOWN** — the consuming query does not exist | as D5, plus the honest issuer's release of the `(key, signature term, signed frame)` triple on a private channel |
| **D7** | L-09 → capstone per-signer chain (§A3.2 item 3) | S-P2 Q2 `Stripped`/`SignerForged` unreachable (`sp2_q2_degraded_compromised.out:378, :384`) **plus S-P2 Q6 `Spliced` unreachable (`.out:1013`, green as registered 2026-09-12)** for the common-content half — **all three exist, green**. *Added 2026-09-15 (finding 3); line numbers repaired from the pre-addendum `:354, 360`* | **C-C9** (§6, new round 4, finding 4) — the one-signer branch's required-set requirement dropped, which falsifies **C-Q1's link-2b completeness conjunct** (`cq1d_sp2_slots_missing.out:1519` `is false`) as well as `Stripped` (`:643` `is false`) while every per-slot conjunct, `Spliced` (`:1305`) and both `HonestComplete` witnesses (`:835`, `:1061`) survive. *Re-specified this round: the row previously named only S-P2's own companions, which red `Stripped` but say nothing about C-Q1's completeness conjunct.* The family-local contrasts remain: S-P2 Q3 (→ `Stripped` red, `.out:520`; "354–520" in the family file is the **trace span**, not a RESULT line), Q4 (→ `SignerForged` red, `.out:601`), Q6-C (→ `Spliced` red, `.out:1213`) — **exist, red**, on S-P2's own queries | the capstone's per-signer link | **NOT YET SHOWN** — the consuming query does not exist | `authTuple` `sset` family, positional `signers0`/`signers1`, `framed`, the three §A5.4 content equalities `ota = otb` / `cva = cvb` / `pla = plb`, **and** the three fields pinned through the shared tuple (`=alg`, `=id`, `mh = h(t)`) — together the six non-fingerprint frame fields (L-09 shared-term mapping). Authorship of those bytes is **L-06's**, not this row's |
| **D8** | L-12 → capstone per-layer chain (§A3.2 item 4) | S-P7 Q2/Q1 `TypeConfused` unreachable (`sp7_q2_degraded_compromised.out:527` / `sp7_q1_strict_dns_compromised.out:560`; *`:505` repaired 2026-09-15*); Q5 both depths — **exists, green** | S-P7 Q3 → `TypeConfused` reachable (`.out:509` goal, `:727` RESULT) — **exists, red**, on S-P7's own query; ablation a10 for the wrapped path | the capstone's per-layer link | **NOT YET SHOWN** — the consuming query does not exist | `OT_*` constants (D-5), `framed`, `wrap()`, `InnerCheck` |
| **D9** | L-23 → capstone first-link boundary (§A3.2.1) | first-link Q4, `TwoWorldsBroken` unreachable both variants (`q4_attack_dns_compromised.out:97`, `q4_attack_repo_compromised.out:97`, both `is true`); Q6 × 4 unreachable (`q6_single_dns_honest.out:91`, `q6_single_dns_compromised.out:93`, `q6r_single_repo_honest.out:91`, `q6r_single_repo_compromised.out:93`) — **exists, green** *(lines added — skeptic 2026-09-15; the row named models and not results)* | first-link Q2 companion (evidence binds issuer identity only) → chain correspondence `is false` (`q2_broken_dns_compromised.out:243`, `q2_broken_repo_compromised.out:243`) **and** `TwoWorldsBroken` `is false` (`:464` both variants) — **exists, red**, on the spike's own queries | the capstone's boundary judge | **NOT YET SHOWN** — the consuming query does not exist | `STMT_DIGEST` (D-1), `authTuple` (D-2), `h`, the two-worlds private-channel judge over the evidence **pair** (per L-24: pair form only) |
| **D10** *(a matrix row: R-2 RULED "yes", 2026-09-15; still **provisional — producer not yet registered**)* | L-02 → S-P2 Q5 `SetAltered` | **NOT YET REGISTERED — producer to be registered in the capstone.** *Repaired 2026-09-15 round 3 (finding 2): the previous cell read "S-P3 Q2/Q4 `PossessionTransplanted` unreachable (`sp3_q2_degraded_compromised.out:200`) — exists, green". **That theorem is not this row's producer.** Its judge compares the proof term's original and accepted **keys** (`sp3_q2_degraded_compromised.pv:137-141`) and neither its event nor its query mentions the accepted manifest: with both manifest-binding protections removed it stays green (`d10b_sp2_q9_manifest_unbound.out:1297` `is true`) while `SetAltered` goes red (`:673` `is false`).* The relation the consumer needs is **possession over the accepted manifest under the accepting key** — `checksign(ppf, kX) = (POSS, t)` for the same `t` the verifier accepted — and the producer the capstone must register is **C-Q9** (§6); feasibility `d10a_sp2_q9_base.out:1111` green, `d10b_sp2_q9_manifest_unbound.out:1462` red. **Independent of R-2** | **C-C3**, both pins removed (Q5-C2 shape): the frame's manifest-hash equality **and** possession-over-manifest | `SetAltered` | **SHOWN, COMMITTED** — `sp2_q5_c2_fponly_frame_nomh.out:535` reachable; isolation configs green, each route surviving the other's removal (C1 `…c1_fponly_frame_mh.out:366`, C3 `…c3_manifestposs_frame_nomh.out:363`) | `POSS` over the manifest (D-3), the frame's `mh` field, `authTuple`, `h` |
| **D11** *(moved into the matrix 2026-09-15 round 4, finding 2; was in §2(c))* | L-13 → **C-Q1's link 6b, the innermost-issuer scope conjunct** (§6) — *and*, conditionally, C-Q6's wrapped-standing linkage | S-P7 Q2/Q5 `Rescoped`/`RescopedD1`/`RescopedD2` unreachable (`sp7_q2_degraded_compromised.out:540`) — **exists, green** | S-P7 Q6a / Q6b / Q5c — **exist, red**, on S-P7's own queries. **Q6b is the one that establishes 6b is a separate conjunct from 6a:** it reads key and authority from the *outermost* frame, so `TypeConfused` stays unreachable (`sp7_q6b_companion_key_outermost.out:489` `is true`) while `Rescoped` becomes reachable (`:769` `is false`) and both honest witnesses stay reachable (`:1317`, `:1508`) | C-Q1's `ChainBroken` at link 6b; and, under R-3, C-Q6's scope conjunct | **NOT YET SHOWN** — C-Q1 does not exist, so `ChainBroken` is declared in no model. The **producer** exists and is green, and the **separation** from link 6a is shown on committed S-P7 output (`sp7_q6b…out:489` against `:769`). *Why it is a row and not a 2(c) entry: C-Q1 consumes scope unconditionally, under both C-Q1 forms and under every R-3 formulation, so this consumption does not wait on R-3 (round 4, finding 2). Its second consumer, C-Q6, still does, and that half stays conditional.* | `wrap()`, `attemptCore`, `h(core)`, `TLR` tag (D-6), `OT_TLR`, `InnerCheck`, the inner frame's `(issuerId, kfp)` |

## 2(b). VACATED — D1 and D2 are matrix rows (author's ruling, 2026-09-15)

**This part is empty.** It held D1 and D2 out of the cross-model matrix
while R-1 was open. **The author ruled R-1 = Reading B (composed) and
R-2 = "yes" on 2026-09-15 — outcome 5 — so both are rows of §2(a)**,
with `m4` and `s4` registered as the capstone's own companions **C-C2**
and **C-C4**. The two rows were moved into §2(a) with their cells
carried across as written; nothing in them was rewritten except the
R-1/R-2 conditions, which are now marked ruled.

**The record of why they were once held out, kept.** Under A7 §A7.10 as
the author wrote it, a dependency exists where severing the
**producer's** fact would falsify the **consumer's** own registered
query. In the models *as they stand* it would not: each consumer
*transcribes* S-P3's checks into its own model, and severing S-P3 — its
query, or the model entire — changes nothing in the consumer and leaves
the consumer's query green (`base_sp2.out:397`, `base_sp7.out:540`).
What `m4` and `s4` sever is the **consumer's own transcribed** checks.
That observation is unchanged and still true of the family models. What
the ruling settles is the **capstone's** fixture: it composes the
families' checks into one verifier, so the producer's fact and the
consumer's query are in the same model, the join is internal to it, and
the two mutations become that model's own companions. The author's
words: *"Having understood this, I think composition is the right answer
here."*

## 2(c). The standing-verdict rows — D12 and D13 (L-16, L-17)

*Restated 2026-09-15 round 4, finding 2: **D11 has left this table for
the matrix**, because C-Q1's link 6b consumes L-13's scope relation
under every formulation and so does not wait on R-3. What remains here
is exactly what R-3 decides — the **standing conjuncts**.*

**RULED (author), 2026-09-15 — R-3 = formulation W (outcome 5).** The
capstone's composition query concludes in a *standing verdict*, so L-16's
designation relation and L-17's entitled-key relation are consumed and
**D12 and D13 are rows.** They are **rows of 2(c)**, not of the
cross-model matrix, and are **not** in its count: in every formulation,
including the ruled one, the **consumer does not exist in any model** —
no query on either side ranges over the composition of S-P7's wrapper
processing with S-STANDING's standing assessment. Their producers and
companions all exist and are the right colour; what is missing is the
consumer, and building it is now a registered capstone obligation
(§6, C-Q6, **written in formulation W**). Both rows are therefore
**NOT YET SHOWN**. *(Under formulation N, and under the degenerate
no-composition-query case, this table would have been empty; the author
ruled W.)* L-16 and L-17 sit here together, which retires the convention
defect the skeptic recorded on 2026-09-15 (complementary L-13 inside a
table declared "CROSS-MODEL entries only", while equally conditional
L-16 and L-17 sat outside it) — now by the opposite route, since L-13
is a settled matrix row and L-16/L-17 are rows of their own part.

| # | Consumer entry (query) | Producer query (state today) | Severing companion | Expected red | Evidence state | What `capstone.pv` must transcribe |
|---|---|---|---|---|---|---|
| **D12** *(a row: R-3 ruled formulation W, 2026-09-15)* | L-16 → the capstone's composition query, standing-verdict half: *an `ESTABLISHED` report over a **wrapped** presentation implies the **innermost** issuer designated the reported identity* | S-STANDING Q1(i)/(ii), both variants, `Established ⟹ Designated` — `ss_q1_strict_dns_compromised.out:503, :513, :523` — **exists, green**; N1 reachable `:829` | S-STANDING Q2 (identity declared, `ss_q2_companionA_identity_declared.out:630, :808, :986`), Q4 (terminal unchecked, `ss_q4_companionC_terminal_unchecked.out:576, :849, :1123`), ablation abl6 (TLR unsigned, `abl6_no_tlr_signature.out:616, :788, :960`) — **exist, red**, on S-STANDING's own queries | the composition query's standing-verdict conjunct | **NOT YET SHOWN** — the consuming query does not exist in any model | `wrapCore`, `attemptCore`, `h(core)`, `TLR` tag (D-6), the lineage/terminal/declaration triple; L-16's residual (`h` injectivity, L2-c) and the two-entry-lineage scoping |
| **D13** *(a row: R-3 ruled formulation W, 2026-09-15)* | L-17 → the capstone's composition query, entitled-key half: *the key the report is computed against is the one the evidenced tuple names* | S-STANDING Q1(iii), `StandingUnentitled` unreachable, both variants and Q1d — `ss_q1_strict_dns_compromised.out:530`, `ss_q1_strict_repo_compromised.out:530`, `ss_q1d_degraded_compromised.out:664` — **exists, green** | S-STANDING Q3, `ss_q3_companionB_entitled_via_envelope.out:860` `is false` — **exists, red**, on S-STANDING's own query | the composition query's entitled-key conjunct | **NOT YET SHOWN** — the consuming query does not exist in any model | `authTuple`'s `kfpr` field, `fp`, the standing envelope path |

**Counts** (restated 2026-09-15 after **the author's ruling**, outcome 5
— R-1 = Reading B, R-2 = "yes", R-3 = formulation W. The 2026-09-14,
the first 2026-09-15, the round-3 and the round-4 counts are superseded
and their correction history is kept below). **Every count here is
stated for the register's ruled default reading**, which is **row 5** of
§5's combined-consequences table. There is no longer an open fork for
the counts to be conditional on; what is still provisional is
**producers**, not classification — D5, D6 and D10 are rows whose
producer the capstone must still register.

| Axis | Rows | Which |
|---|---|---|
| Rows in the cross-model matrix, **2(a)** | **11** | **D1, D2**, D3, D4, D5, D6, D7, D8, D9, D10, D11 |
| **Firm** — classification settled, producer registered and green, nothing routed | **8** | **D1**, **D2**, D3, D4, D7, D8, D9, D11 |
| **Provisional — producer to be registered in the capstone** — `prov(P)` | **3** | D5 (**C-Q7**), D6 (**C-Q8**), D10 (**C-Q9**) |
| **Provisional on a routed fork** | **0** | None. R-1, R-2 and R-3 are ruled; `prov(R-2)` is retired |
| Producer query **exists and is green** | **8 of 11** | D1, D2, D3, D4, D7, D8, D9, D11. **Not** D5, D6, D10 — none of their producers exists |
| Severing shown red on the **consumer's own** query | **5** | D1 (scratch, `m4:620`), D2 (scratch, `s4:864`), D3 (scratch, `s6:361`), D5 (scratch, `s1:897`), D10 (committed, `sp2_q5_c2:535`) |
| Red on **exactly** the consumer's query, nothing else | **4** | D1 (`m4:620`), D3 (`s6:361`), D5 (`s1:897`), D10 (`sp2_q5_c2:535`). **Not D2**: `s4` reds three queries by design (C-C4's set (1)) |
| **NOT YET SHOWN** — the consuming query does not exist | **6** | D4, D6, D7, D8, D9, D11 |
| Companion red on the **producer's own** query only, i.e. not a discharge under A3.3 | **5** in 2(a) | D6 (S-P1 Q3, a *contrast* only — D6's own companion is C-C7), D7 (S-P2 Q3/Q4/Q6-C, contrasts; its registered companion is **C-C9**), D8, D9, D11 (S-P7 Q6a/Q6b/Q5c). **Not D1 or D2**: C-C2 and C-C4 are red on the **consumer's** query |
| Held out by R-1, **2(b)** | **0** | **VACATED** — D1 and D2 are matrix rows under the ruling |
| Rows of **2(c)**, the standing-verdict part | **2** | D12, D13 (R-3 ruled **W**; both NOT YET SHOWN, both outside the matrix count) |
| **Producer green across the whole register** — rows whose producer exists and is green, counting 2(c) | **10 of 13** | the eight matrix rows above **plus D12 and D13**, whose S-STANDING producers exist and are green (`ss_q1_*.out:503, :513, :523`, `:530`; `ss_q1d_*.out:664`). **Not** D5, D6, D10 |
| Entries in the register that are **not** rows in any table | — | every COMPLEMENTARY, LAYER-2(a), LAYER-2(b) and CROSS-FORMALISM entry of §1 |

**NOT YET SHOWN, spelled out.** Within 2(a) the rows whose **consuming
query does not exist** are D4, D6, D7, D8, D9 and D11 — six. The other
**five** are shown to the extent the record allows: D1 in scratch
(`m4_framepin_mh.out:620`) and D2 in scratch (`s4_innerfp_mh.out:864`),
both on the consumer's own query, both now matrix rows under the
ruling; D3 in scratch (`s6_bothchannels.out:361`); D5's *mutation* in
scratch (`s1_sig_unbound.out:897`) while its producer is unregistered;
D10's *consumer red* committed
(`sp2_q5_c2_fponly_frame_nomh.out:535`) while its producer is
unregistered. In 2(c) D12 and D13 are NOT YET SHOWN for the same reason
— their consuming query exists in no model — but they are not matrix
rows and are not in the matrix count.

**Correction history of these counts.** *2026-09-14 → first 2026-09-15
restatement:* (1) D1 and D2 were counted firm; they have the same
two-route shape as D10 and R-2 was held to decide all three (finding 4).
(2) "Producer exists and is green: 11 of 11" was false for D5 and D6
once the producer fact was named exactly (finding 1); it became 9 of 11.
(3) "Red on exactly the consumer's query: D1, D3, D5" omitted **D10**,
whose committed `.out` shows `SetAltered` red alone
(`sp2_q5_c2_fponly_frame_nomh.out:535`, with `Stripped` `:349`,
`SignerForged` `:356`, `Reattributed` `:542` true and both witnesses
reachable `:706, :925`). *First 2026-09-15 restatement → round 3:*
(4) D1 and D2 leave the matrix under R-1 as written (skeptic finding 2;
the rule's antecedent is not met), so the matrix is 8 rows, not 11, and
R-2 now reaches D10 only. (5) D10's producer was counted "exists and is
green"; it does not exist (round-3 finding 2), so "producer exists and
is green" falls from 9 of 11 to **5 of 8**. (6) D6's producer was
counted as D5's (C-Q7); it is **C-Q8**, which does not exist either
(round-3 finding 1). (7) D11 leaves the matrix for 2(c) and is joined
there by D12 and D13, so no complementary-today entry sits in a table
declared "CROSS-MODEL entries only". *Round 3 → **round 4**:*
(8) **D11 returns to the matrix** — C-Q1's link 6b consumes L-13's
scope relation unconditionally, so its consumption never depended on
R-3 (round-4 finding 2). The matrix is **9 rows**, firm rises to **6**,
producer-green to **6 of 9**, NOT YET SHOWN to **6**,
companion-on-producer's-own-query to **5**, and §2(c) falls to **2**.
Round 3's "producer green 5 of 8 / NOT YET SHOWN 5 / conditional on
R-3 3" are superseded by these. *Round 4 → **the author's ruling,
2026-09-15**:* (9) **R-1 is ruled Reading B and R-2 "yes"** (outcome 5),
so **D1 and D2 return to the matrix** and §2(b) is vacated: the matrix is
**11 rows**, firm rises to **8**, producer-green to **8 of 11**, severing
shown red on the consumer's own query to **5**, red-on-exactly-the-
consumer's-query to **4** (D2 is excluded — `s4` reds three queries by
design), and companion-on-producer's-own-query stays **5**. (10) **R-3 is
ruled formulation W**, so §2(c)'s two entries are **rows**, not
conditional entries; the number is unchanged at **2** and they remain
outside the matrix count. NOT YET SHOWN within 2(a) is unchanged at
**6**, because D1's and D2's consuming queries exist and are committed.
Round 4's "9 rows / firm 6 / producer-green 6 of 9" are superseded by
these.

**What the forks did to these counts** was written once, for all eight
outcomes, in §5's "Combined consequences" table; **the author ruled
outcome 5 on 2026-09-15** and the counts above are that row's. The table
is kept as the record of the decision, with row 5 marked. Nothing in
this section anticipates anything further.

# 3. Layer 2 register — exposed and unclaimed

Deduplicated. Each item is named against the A3 §A3.3 list
(`a3:222-227`) as extended by ENUM §3 (`ENUMERATION.md:129-134`).
**None of these is discharged by anything in this suite.**

**Split into two classes, 2026-09-15 (finding 6).** The reviewer is
right that the draft's single class, tagged *"never discharged,
forever"*, swept in obligations the project has already booked on its
own exit list. The classes differ in who can ever discharge the item
and whether "forever" is true of it:

- **(a) Permanent external assumption.** Nothing this project builds
  can discharge it. It is discharged, if at all, by cited external
  results — cryptographic hardness, the behaviour of a public chain,
  the fidelity of code to spec, the independence of operational
  channels. *Forever* is accurate here: no Band 0 or Band 1 artifact
  retires it.
- **(b) Internal proof obligation currently carried as an assumption.**
  The project owes an artifact that settles it, the artifact is on
  `formal/BAND0-EXIT.md`, and when it lands **this entry cites the
  proof instead of assuming the fact**. *Forever does not apply.* Each
  row names its exit item.

## 3(a). Permanent external assumptions

| Id | Assumption | A3.3 / ENUM §3 category | Entries resting on it |
|---|---|---|---|
| **L2-a** | Signature unforgeability (Dolev–Yao idealization); DSKS granted but bounded by D-4 | cryptographic primitive security | L-01, L-02, L-06, L-09, L-10, L-13, L-16 |
| **L2-b** | `fp` collision resistance / injectivity | cryptographic primitive security | L-01, L-02, L-04, L-06, L-09, L-12, L-13, L-16, L-17 |
| **L2-c** | `h` idealization; concrete digest collision resistance | cryptographic primitive security | L-01, L-04, L-06, L-09, L-10, L-12, L-16, L-20, L-23, L-25 |
| **L2-e** | The verification profile — P3's `[assumption]` half (library, version, accepted encodings, public-key validation, low-order points, cofactor); H1a evidence | cryptographic primitive security | L-01, L-02 |
| **L2-f** | Deterministic signatures (*"conservative for the judge"*) | cryptographic primitive security | L-01, L-06, L-12, L-16 |
| **L2-g** | Implementation fidelity — including **key-use discipline for endpoints the suite does not model** (L-07, narrowed 2026-09-15: the modelled endpoints' discipline is the L-07 signing-domain enumeration, a composed property, not an assumption) | implementation fidelity | L-06, **L-07** |
| **L2-h** | Operational independence of authority channels; A1.3 "never all" as **n = 2 finite enumeration, not a quantified result** | operational channel independence | L-04 (provenance half only — narrowed by L-26) |
| **L2-k** | Historical trust-anchor correctness | historical trust-anchor correctness | L-19 (A1.6 Bitcoin/OTS `[assumption]`) |
| **L2-m** | Chain availability (headers obtainable; no reorg re-verification) | chain availability | L-19 |
| **L2-l** | Cross-protocol domain separation — the tag's work is *"cross-protocol, invisible to any one family"* (library D-6 note; S-STANDING review item 27; S-P1 single-removal matrix) | implementation fidelity (composition) | L-07, and as a standing caution on every single-removal "inert" label |

## 3(b). Internal proof obligations currently carried as assumptions

Each is **exposed and unclaimed today**, never a matrix row, and each
names the exit item that discharges it. When that item lands, the
entries below cite it and stop assuming the fact — *"then this entry
cites the proof, never silently absorbs it"* (L-06's own wording).
**"Forever" does not apply to this table.**

| Id | Obligation carried as an assumption | Discharged by | Entries resting on it |
|---|---|---|---|
| **L2-d** | Canonical encoding / framing injectivity; frame layout; set encoding; the core's byte composition; and the canonical-encoding half of **L2-b** (*what* a fingerprint hashes) | **`formal/BAND0-EXIT.md` E3** — the P8 framing proof (injectivity over the accepted domain, boundary-unambiguous frame), with (a) the criteria-before-evidence decision on the proof's form, (b) the proof, (c) the golden vectors that fix frame layout and identifier encoding, (d) non-author falsification review, (e) the author's read. Status today: **not begun**, TRK `open` | L-01, L-06, L-08, L-09, L-16, L-20; L-02, L-13 via L2-b |
| **L2-i** | P8 type-tag bytes; that the enumerated signed-object set is these eight and no others | **E3** (same proof; §A3.6.1 fixes the identifier encoding and golden vectors before exit) | L-12, L-13 |
| **L2-j** | Opacity of any concrete embedding; canonicalization semantics; what changes between canonicalization versions | **E3** | L-13, L-14 |
| **L2-n** *(new, 2026-09-15)* | The §A3.7.2 **extended atomic-entry invariant** — `REFUSED` ⇒ record + commitment + delivery `PENDING` + publication `PENDING` — carried by L-21 as *"Layer 2 — unclaimed until the A3.9 TLA+ obligation"* | **`formal/BAND0-EXIT.md` E6** — P5c gains the invariant with its two companions, both red; reading aids; review; author read. Status today: **not begun**, no TRK row (BAND0-EXIT finding 1) | **L-21**; and the `REFUSAL` tag row of the L-07 enumeration, which no suite model exercises |

**Consequence for the gate.** A3 §A3.3 requires Layer 2 assumptions to
be *"explicitly exposed and unclaimed … never discharged, never
silently absorbed"*. Table 3(a) satisfies that permanently. Table 3(b)
satisfies it **today** and converts to a citation when E3 and E6 land;
neither table ever produces a discharge-matrix row, and no capstone
query may mark either one checked.

**Named scoping, NOT Layer 2** (A3 §A3.3 last sentence: *"named
in-module and disposed by amendment discipline, never silently"*):
`|set| ≤ 2` (L-09); depth bounded at 2 (L-13); lineages of exactly two
attempts (L-16); n = 2 channels (L-04, which is *also* L2-h); non-framed
kinds unrepresentable (L-12, open coverage cell). These are termination-
and fixture-forced boundaries, not assumptions about the world, and the
capstone inherits every one of them.

---

# 4. Cross-formalism joins (TLA+ ↔ symbolic)

ENUM §4: *"ProVerif cannot consume a TLA+ result."* Every row below is
**never** marked symbolically discharged; mislabelling one is the
checkmark-relay red bar (Sol finding 2).

| Register | Join | Symbolic side (consumer) | TLA+ producer module and invariants | Shared term | Status |
|---|---|---|---|---|---|
| **L-05** | `Accept` / `AcceptS` ↔ P4 verdict partition | S-P1 (all five models; F5 depends on it), S-P2 (`Accept1S`/`Accept2S`) | `formal/tla/P4_VerifierStates.tla` — `Partition`, `NoSilentPromotion`, `ExactInvalid`, `ExactUnverifiable`; degraded clause `DegradedNeedsExplicitWaiver`, `ExactDegraded` | the acceptance predicate | Carried in the written proof and COVERAGE-MAP row 1; agreement **unchecked** (legend: "unchecked: Accept ↔ P4") |
| **L-05** (third face) | `AcceptS` ↔ §A4.6's "marked degraded" proviso | S-STANDING — *"this model's envelope path fires the degraded-shape event `AcceptS`, which is neither queried nor shown reachable in the `.out`"* | same module | `AcceptS` | Assumed met by P4, **not shown**; a reachability witness would be a registered addition, not a recut |
| **L-19** | TLR anchor temporal validity (A2.1 predicate per SC-1) | S-STANDING C-2 — anchor-proof check inert (abl2), reason code vocabulary only | `P5c_IssuanceProtocol.tla` (`ShippedIsSound`, `ExpiredCannotShip`) + `P5cP5P6_Bridge.tla` (`PinAgreement`, `ShippedDesignatedAgree`, `LateBurialRejected`); `P5P6_TemporalRevocation.tla` (`ForgeryRejected`, `WindowRespected`, `AuthorizedAtDeclared`) | "anchor valid" | Whether SC-1 needs its own TLA+ instance is COVERAGE-MAP row 13's **open cell** (disposition B8) |
| **L-21** | Refusal latch → terminal disposition (SC-2's one signing act) | S-STANDING C-5 | `P5c_IssuanceProtocol.tla` — `RefusedOnlyWhenExhausted`, `NoSilentDeadlock`, action `RefusalLatched`; the §A3.7.2 extended atomic-entry invariant is **not built** (BAND0-EXIT E6) | the terminal disposition | Producer incomplete; join cannot be written in full until E6 |
| **L-03** | (negative) S-P3 assumes no anchor validity | — | — | — | Recorded so the capstone does not look for one |
| **L-11** | (negative) S-P2 consumes no join but L-05 | — | — | — | Recorded |
| **L-15** | (negative) S-P7 consumes none — the refusal-latch join belongs to S-STANDING per the A7 ruling | — | — | — | Recorded; supersedes `ENUMERATION.md:141-143` and COVERAGE-MAP rows 6–7 in substance, both left as written |

**E8 consequence.** Every row above is a line item of BAND0-EXIT item
E8 (the TLA+ ↔ symbolic correspondence mapping, A1 §A1.4). This file
does not write that mapping; it enumerates what the mapping must cover.

---

# 5. Routed to the author

**RULED (author), 2026-09-15 — outcome 5.** *(Provenance label per
`formal/spike/first-link/DECISION.md`: **RULED (author)** — the author
decided, in session, in his own words. Nothing below is a clerk's
reading of a discussion.)*

The author's words, verbatim:

> *"Having understood this, I think composition is the right answer
> here."*

> *"I am satisfied with outcome 5, and merely restate my concerns that
> the real burden for testing these claims will fall on the
> adjudicator."*

**The ruling, named against the three forks below:**

- **R-1 = Reading B — "composed."** The capstone builds **one** verifier
  carrying both families' checks. L-01 → S-P2 and L-01 → S-P7 become
  joins internal to that model; **D1 and D2 are matrix rows**, with `m4`
  and `s4` registered as the capstone's own companions **C-C2** and
  **C-C4**.
- **R-2 = "yes."** A jointly-sufficient pin **is** a dependency.
  **D10 is a matrix row**, and D1/D2 clear the second condition Reading B
  leaves them.
- **R-3 = formulation W.** The capstone's composition query concludes in
  a **standing verdict**. L-16 and L-17 are consumed; **D12 and D13 are
  rows of §2(c)**.

That is **outcome 5** of the combined-consequences table at the end of
this section, whose row 5 is marked as the ruled outcome.

**The instrument — what the ruling changes and what it does not.**

1. **This file's default reading changes to outcome 5.** Every count in
   §2 is restated for it; §2(b) is vacated; §2(c)'s two entries are
   rows. The header carries the same statement.
2. **The capstone's `PREDICTIONS.md` is drafted from §6 accordingly** —
   C-Q6 written in **formulation W**, C-Q3 and C-Q4 registered as the
   composed verifier's own key-binding and wrapped-attribution judges
   rather than as conditional additions, and C-C2/C-C4 registered as the
   capstone's companions.
3. **The commit is the author's.** This file remains **PROPOSED**. The
   ruling settles **classification**; it discharges nothing, registers
   nothing, and turns no cell green. D5, D6 and D10 are rows whose
   **producer does not yet exist** under this reading exactly as under
   every other — C-Q7, C-Q8 and C-Q9 must still be built and run.

**The author's carried concern, recorded as he stated it and not
dissolved:** *"the real burden for testing these claims will fall on the
adjudicator."* Composition settles where the ledger puts these rows; it
does not settle who bears the cost of testing what the rows assert. That
cost lands on the adjudicator — the relying party of item 27's
vocabulary ruling, not the verifier — and the register does not claim
otherwise. Nothing in §6 relieves it.

**The fork statements and the combined-consequences table below are
left as written.** They are the record of the decision — what was put to
the author, in the form it was put — and are not rewritten to match the
answer. Only row 5 of the table is marked.

---

Three items. Each is a fork where A7 §A7.10's application is arguable
both ways. Nothing else here needs a ruling. **Each is stated once, in
its honest form, and their combined consequences are written as one
table at the end of this section** — the previous drafts stated R-1's
consequences in three places that contradicted each other, and
conditioned D1/D2 on R-1 in one place and on R-2 in another (round 3,
finding 5). *(All three are now **RULED**; see the block above.)*

**R-1 — Does the capstone's composition turn a transcribed check into
a cross-model join?** (L-01 → S-P2, L-01 → S-P7; affects **D1** and
**D2**.) S-P2 and S-P7 both *transcribe* S-P3's key-binding checks into
their own models and re-run the judge.

**The register's honest statement of where this stands, 2026-09-15
round 3.** *Under A7 §A7.10 as the author wrote it, D1 and D2 are
COMPLEMENTARY today.* The rule's antecedent is "severing the producer's
fact falsifies the consumer's own registered query", and for these two
rows it is **not met**: severing S-P3 — its Q2 query, or the S-P3 model
entire — changes nothing inside `sp2_q2_degraded_compromised.pv` or
`sp7_q2_degraded_compromised.pv`, and both consumer queries stay green
(`base_sp2.out:397` `Reattributed` `is true`; `base_sp7.out:540`
`Rescoped` `is true`). What the two-removal mutations `m4` and `s4`
sever is the **consumer's own transcribed** checks, not the producer's
fact. That is why D1 and D2 now sit in §2(b), held out of the matrix,
rather than inside a table declared "CROSS-MODEL entries only".

**What would make them rows.** They become **capstone-internal joins**
if the capstone's fixture composes the families' checks into **one
verifier** — one acceptance path carrying S-P3's key binding, S-P2's
set logic and S-P7's wrapper processing together, which is what ENUM §3
("one model") permits and what C-Q1 presupposes. In a composed fixture
the producer's fact and the consumer's query are in the same model, so
severing the one does falsify the other, and the two-removal mutations
**`m4` and `s4` become the capstone's own companions** (registered as
C-C2 and C-C4). Whether to compose that way is **the capstone's design
choice**, not a fact the record settles — which is exactly why this is
routed and not decided here.

**The two readings, named for the table below.**

- **Reading A — "as written".** Apply A7 §A7.10 to the models as they
  stand. The antecedent fails; L-01 → S-P2 and L-01 → S-P7 are
  COMPLEMENTARY; **D1 and D2 are not rows.** *This is the register's
  default for the counts in §2.*
- **Reading B — "composed".** The capstone builds one verifier carrying
  both families' checks; the join becomes internal to that model; **D1
  and D2 are rows**, with `m4`/`s4` as their companions, *provided R-2
  also answers "yes"* — both mutations are two-removal severings of
  jointly-sufficient pins, which is precisely R-2's question.

**What the register does not claim.** *The 2026-09-14 and first
2026-09-15 drafts offered D5 as evidence for Reading B, and offered D1
and D2 as independent corroboration. Both are withdrawn.* D5's producer
fact, once named exactly, is established by no committed query (finding
1), so D5 is an open producer question, not a worked example — and
**R-1's answer does not change D5's state**: under either reading D5
needs C-Q7 registered before it is anything at all. D1 and D2 cannot
corroborate Reading B either, because Reading B is what decides their
classification: citing them would be circular (skeptic, 2026-09-15).

**The one piece of non-circular evidence, put to the author as what it
is.** S-P7's own record sentence: *"the check's **security** is
consumed from S-P1, never re-proved here"* (`s-p7:580-582`). That is a
family's statement about what it takes itself to consume. It is a
statement, not a run. It is the whole of the case for Reading B that
does not presuppose Reading B.

**R-2 — Is a jointly-sufficient pin a dependency?** (L-02 → S-P2;
affects **D10**, and D1/D2 in combination with R-1 Reading B.) S-P2
records that *"the frame's manifest hash and possession-over-manifest
each alone carry `SetAltered` and neither is needed while the other
stands"*, and its committed ladder shows it: either route alone holds
(C1 `sp2_q5_c1_fponly_frame_mh.out:366`, C3
`sp2_q5_c3_manifestposs_frame_nomh.out:363` — `SetAltered`
unreachable), and only the combined removal exposes the attack (C2
`sp2_q5_c2_fponly_frame_nomh.out:535` — `SetAltered` reachable). A7
§A7.10 says a dependency exists where severing *would falsify* — silent
on defence in depth. **The reviewer's recommendation, accepted:
whatever the ruling, represent the redundancy explicitly** — record
both routes, show each survives the other's removal, and require the
combined removal to expose the attack. §6 registers the consumer query
`SetAltered` (C-Q5) and its honest-flow witness (C-Q5w) accordingly,
whether or not R-2 makes D10 a row.

**The combined-removal companion is the operative one.** C-C3 removes
*both* routes together; the isolation configurations C1 and C3 are what
show it is a severing and not a broken fixture. That three-set
specification is in §6 and is verified against committed `.out` lines.

**D10's producer defect is independent of R-2 and stays whichever way
R-2 goes** (round 3, finding 2). D10's producer was named as S-P3's
`PossessionTransplanted` unreachability. That judge compares the proof
term's **original and accepted keys** — `if kX = kH then 0 else event
PossessionTransplanted(kX, p)` (`sp3_q2_degraded_compromised.pv:137-141`)
— and neither its event nor its query mentions the accepted manifest.
With both manifest-binding protections removed together it stays green
while the consumer goes red: `d10b_sp2_q9_manifest_unbound.out:1297`
`is true` against `:673` `is false`. So if R-2 answers "yes", D10 is a
row **whose producer does not exist**; the producer to be registered in
the capstone is **C-Q9** (§6), and its relation is *possession over the
accepted manifest under the accepting key* — `checksign(ppf, kX) =
(POSS, t)` for the same `t` the verifier accepted. If R-2 answers "no",
L-02 → S-P2 is COMPLEMENTARY, D10 leaves the matrix, and C-Q9 is still
worth registering for C-Q1's per-layer possession link (D4, D7).

**R-3 — Must the capstone register a wrapped-standing composition
query, and with which conclusion?** (**L-16 and L-17 only**; affects
**D12** and **D13**, both in §2(c).) **Restated 2026-09-15 round 4
(finding 2): R-3 no longer reaches L-13 or D11.** C-Q1 consumes the
innermost-issuer scope relation unconditionally as its link 6b, in both
the strict and the degraded form and under every R-3 formulation, so
L-13 is consumed by C-Q1 whatever the author decides here and **D11 is
a matrix row in all eight outcomes** (§2(a)). What R-3 decides is
exactly the **standing conjuncts**: whether the capstone's composition
query concludes in a *standing verdict* — in which case L-16's
designation relation and L-17's entitled-key relation are consumed and
D12/D13 exist — or stops at the attributed identity, in which case they
stay COMPLEMENTARY. *(The round-3 statement bundled D11 in here; that
was the routing defect the round-4 review found. D11's **second**
consumer, C-Q6's wrapped-standing linkage, is still conditional on R-3;
its **first**, C-Q1's link 6b, is not, and one unconditional consumer
is enough to make it a row.)* S-STANDING *does* carry a
wrapper-shaped term: it declares `wrapCore`, and its companion
exercises a wrapper-shaped transplant, established unreachable for
`ESTABLISHED` by `h` injectivity inside S-STANDING's own algebra
(`wrap_routes.out:1827, :1944, :1951`). The gap is not the absence of a
wrapper — it is the **composition** of S-P7's wrapper *processing*
(unwrap, inner attribution, depth ≤ 2) with S-STANDING's standing
assessment, which the existing wrapper-shaped term does not establish
and no query on either side ranges over. So severing S-P7's scope
relation falsifies no S-STANDING query, and the pair is COMPLEMENTARY
under the rule as written — while the A7 ruling of 2026-09-06
(*"S-STANDING carries the wrapper-shaped transplant; S-P7 supplies the
identity relation it composes with"*) describes a composition that
exists in no model.

**The two formulations.** Both presuppose that the capstone registers
C-Q6 at all; the degenerate third case — **no composition query** — is
recorded after the table.

- **Formulation W (wide) — the conclusion is a standing verdict.**
  E.g. *"an `ESTABLISHED` report computed over a **wrapped**
  presentation implies the **innermost** issuer designated the reported
  identity, and the key it is computed against is the one the evidenced
  tuple names."* Severing S-STANDING's P-1 falsifies the first
  conjunct; severing P-2 falsifies the second. **L-16 and L-17 are
  consumed by the composition query** and become **D12** and **D13**
  (§2(c)). Both producers and both companions
  already exist and are the right colour; what does not exist is the
  consuming query, so both enter as **NOT YET SHOWN**. The
  capstone then also inherits L-16's residual — `h` injectivity as
  *"the whole load of the transplant result"* (L2-c) — and the
  two-entry-lineage scoping.
- **Formulation N (narrow) — the conclusion stops at the attributed
  identity.** E.g. *"a wrapped presentation's inner bytes are
  attributed to the innermost `(idI, kI)`"*, with the standing verdict
  supplied as a fixed input rather than computed. Severing P-1 or P-2
  changes nothing the query asserts, so **L-16 and L-17 stay
  COMPLEMENTARY** and **§2(c) is empty**. *(Round 4: N used to "yield
  D11 only". D11 is now a matrix row independent of R-3, so N yields
  nothing here at all.)*

§6's C-Q6 is written so that either formulation drops into it; whichever
is chosen must be written into the query text **before predictions
freeze**, because §2(c)'s size follows from it. **What no longer follows
from it is the matrix count** (round 4, finding 2): D11 is a row in
every outcome.

## Combined consequences — the eight R-1 × R-2 × R-3 outcomes

*Written once, as one table, because the three forks interact and the
previous drafts stated their consequences in three places that
contradicted each other (round 3, finding 5).* **Statuses:** *firm* =
classification settled, producer registered and green; *prov(P)* =
a row whose **producer must still be registered in the capstone**;
*complementary* = an entry, not a row; *not a row* = outside every
table. *(§2 used **prov(R-2)** — a row whose membership R-2 would decide — for
D10 while R-2 was **open**. R-2 is ruled "yes", so that tag is retired;
it never appeared in the table below, because every row here has R-2
resolved.)* Rows D3, D4, D7,
D8, D9 **and D11** are **firm in all eight outcomes** and are not repeated per
column. **The register's default reading is now outcome 5 — RULED
(author), 2026-09-15: R-1 = B, R-2 = yes, R-3 = W** — and §2's counts
are **row 5's**: 11 matrix rows, 2 entries in §2(c), §2(b) vacated. *(The
clerk's pre-ruling default was R-1 = A with R-2 and R-3 open, whose
counts were those of outcomes 1 and 2; it is superseded.)*
*Rewritten 2026-09-15 round 4 (finding 2): D11 moves from a §2(c)
column into the firm base, which raises every outcome's matrix count by
one and empties §2(c) under formulation N.*

| # | R-1 | R-2 | R-3 | D1, D2 | D5, D6 | D10 | D11 | D12, D13 | Rows in the cross-model matrix | §2(c) entries |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | A — as written | yes | W | complementary (not a row) | prov(P): C-Q7 / C-Q8 | prov(P): C-Q9 | **firm — matrix row** (C-Q1 link 6b) | §2(c) rows | **9** — D3–D11 | **2** |
| 2 | A — as written | yes | N | complementary (not a row) | prov(P) | prov(P): C-Q9 | **firm — matrix row** | complementary | **9** — D3–D11 | **0** |
| 3 | A — as written | no | W | complementary (not a row) | prov(P) | complementary (not a row) | **firm — matrix row** | §2(c) rows | **8** — D3–D9, D11 | **2** |
| 4 | A — as written | no | N | complementary (not a row) | prov(P) | complementary (not a row) | **firm — matrix row** | complementary | **8** — D3–D9, D11 | **0** |
| **5 — RULED (author), 2026-09-15. THE RULED OUTCOME.** | **B — composed** | **yes** | **W** | **firm** (companions `m4`/`s4` = C-C2/C-C4) | prov(P) | prov(P): C-Q9 | **firm — matrix row** | §2(c) rows | **11** — D1–D11 | **2** |
| 6 | B — composed | yes | N | **firm** (companions `m4`/`s4`) | prov(P) | prov(P): C-Q9 | **firm — matrix row** | complementary | **11** — D1–D11 | **0** |
| 7 | B — composed | no | W | complementary (not a row) — R-2 blocks them | prov(P) | complementary (not a row) | **firm — matrix row** | §2(c) rows | **8** — D3–D9, D11 | **2** |
| 8 | B — composed | no | N | complementary (not a row) — R-2 blocks them | prov(P) | complementary (not a row) | **firm — matrix row** | complementary | **8** — D3–D9, D11 | **0** |

**Reading the table.**

1. **D5 and D6 are `prov(P)` in every outcome.** No fork touches them.
   They need C-Q7 and C-Q8 registered before they are anything at all.
   *Nothing about R-1 changes D5, and D5 is not evidence about R-1.*
2. **D10's producer defect survives every outcome too.** R-2 decides
   only whether D10 is a row; if it is, it is `prov(P)` on C-Q9.
3. **D1 and D2 need *both* R-1 Reading B and R-2 "yes"** (outcomes 5
   and 6). Either one alone leaves them out. This is the propagation
   the earlier drafts got wrong in both directions.
4. **R-3 never changes the matrix count**, because D12 and D13 are
   in §2(c) in every outcome in which they exist and **D11 is in the
   matrix in every outcome**. R-3 changes how many §2(c) entries there
   are: **two** under W, **none** under N. *(Round 4: the round-3
   reading — "three under W, one under N" — counted D11 in §2(c); it
   no longer belongs there.)*
5. **The degenerate R-3 case — no composition query at all.** Then
   L-16 and L-17 are COMPLEMENTARY, §2(c) is empty, D12
   and D13 do not exist, and the **standing** composition is prose in the
   relying-party story, which BAND0-EXIT E5 does not cover. **L-13 and
   D11 are unaffected**: C-Q1's link 6b consumes the scope relation
   whatever happens to C-Q6 (round 4, finding 2). This is not
   a ninth row because it is the prior question, not a third value of
   the formulation fork.
6. **A coupling the author should see.** Any capstone that builds C-Q6
   has composed two families' fixtures into one model. That is not by
   itself Reading B — C-Q6 composes S-P7's wrapper processing with
   S-STANDING's assessment, a different composition from merging
   S-P3's key-binding checks into one acceptance path — but a capstone
   willing to do the one may have no principled reason to refuse the
   other. Outcomes 3, 4, 7 and 8 are coherent; outcomes 1 and 2 are
   coherent; the author should decide the composition question
   deliberately rather than by accident of which query gets written
   first.


**Not routed, recorded as facts.** L-07 (key-use discipline) has no
producer anywhere and is Layer 2 by the family's own statement; its
discharge route is the H1a red-bar vector, outside Band 0. L-21's
producer (the §A3.7.2 extended atomic-entry invariant) does not exist —
that is BAND0-EXIT item E6, already on the list.

---

# 6. What `capstone.pv` must contain

Derived from §2, **under the author's ruled reading of 2026-09-15 —
outcome 5** (R-1 = Reading B "composed", R-2 = "yes", R-3 = formulation
W; §5). This is the minimum; the capstone may carry more. **Three
consequences of the ruling are load-bearing for a builder:** the fixture
is **one composed verifier** carrying S-P3's key binding, S-P2's set
logic and S-P7's wrapper processing on one acceptance path (Reading B —
which is what C-Q1 already presupposed); **C-C2 and C-C4 are the
capstone's own companions**, not conditional additions; and **C-Q6 is
written in formulation W**, concluding in a standing verdict. **The
capstone's `PREDICTIONS.md` is drafted from this section** and freezes
before any run.

**Library transcription** (`proverif -lib formal/suite/lib/tessera_theory.pvl`,
one model, ENUM §3): `c`, `skey`/`pkey`/`pk`, `sign`/`checksign`,
`fp`, `h`; `POSS` and `BYTES`; **D-1** `STMT_DIRECT`/`STMT_DIGEST`
(using the spike's single `STMT` is a build failure); **D-2**
`authTuple` as a `[data]` constructor; **D-3** possession over the
**manifest**, never the fingerprint; **D-4** `dsks(s, r)`; **D-5** the
eight `OT_*` constants; **D-6** the `TLR` and `REFUSAL` tags — with the
note that the tag check is *inert in every single-family fixture and
load-bearing under composition*, which is precisely what the capstone
is for. The capstone's fixture must exercise **the L-07 signing-domain
enumeration** (§1, L-07): `STMT_DIGEST` under an authority-channel key,
`POSS` and `BYTES` and `TLR` under the **same** issuer key, and it must
record `STMT_DIRECT` and `REFUSAL` as declared-and-unexercised rather
than silently omitting them. The seven-argument `framed` constructor is **NOT promoted**:
copy it verbatim into the capstone, as S-P1 and S-P2 copied it.

**Queries the capstone must register** (predictions frozen first,
per-query timebox declared, three named outcomes — ENUM §5):

| # | Query | Serves |
|---|---|---|
| **C-Q1** | The §A3.2 linkage query. *One sentence is not a build plan (round 3, finding 4); **C-Q1's full contract — event signatures, per-layer correspondence, strict/degraded split, fixture, expected outcome — is written out immediately below this table.*** *Rewritten again 2026-09-15 round 4: `LayerAccepted` gains an **acceptance identifier** and the **accepted evidence term**; link 1 splits into 1a (evidence bound to this acceptance, **both** modes) and 1b (honest publication, strict only); link 2 splits into 2a (per-slot membership) and 2b (**required-set completeness within one acceptance**); link 6 splits into 6a (object type) and 6b (**innermost-issuer scope**).* | D4, D6, D7, D8, **D11** |
| C-Q2 | The §A3.2.1 boundary judge over the evidence **pair** (per L-24, pair form only; the single-evidence form is Addendum 1's and is not implied) | D9 |
| C-Q3 | The multi-signer key-binding judge — S-P2's carried `Reattributed` over the capstone's set fixture | **D1** — a matrix row under the ruling (R-1 = Reading B, R-2 = "yes", 2026-09-15); it was registered regardless even while R-1 was open, because C-Q1's per-signer link reads the same binding. Its companion is **C-C2** |
| C-Q4 | The wrapped-attribution judges — `Rescoped` and `InnerSigTransplanted` over a capstone fixture carrying both an issuer key and a wrapper key | D5; and **D2** — a matrix row under the ruling (2026-09-15). D2's companion is **C-C4**, whose set (1) reds three queries by design |
| **C-Q7** | **The signature-TERM judge (2026-09-15, finding 1)** — the *producer* of **R-key**, D5's transplant scope: the honest issuer releases `sg = sign((BYTES, fb), skI)` to a private judge; the verifier reports `(acceptedKey, sg)` at its acceptance point; `event SigTransplanted(pkey, bitstring)` fires when `kX ≠ pk(skI)`; registered **unreachable**, honest-flow witness reachable. Shared term: **the signature term together with the reported key**. **Scope, round 3, finding 1: C-Q7 serves D5's transplant scope and nothing else.** It observes `(acceptedKey, signature)` and **cannot see different bytes presented under the same key** — shown on a copy, where a same-key byte unbinding leaves C-Q7 green (`d6b_sp1_q8_samekey_unbound.out:246`) while S-P1's own authorship goes red (`:593`). It is **not** D6's producer. **Kept separate at round 4 (finding 1):** C-Q7 is an **honest-origin / transplant** claim and is *supposed* to quantify over honest-released signature terms — that is what "transplant" means. C-Q8 is a **structural judge over every accepted triple** and quantifies over none. The round-4 repair rewrites C-Q8 and leaves C-Q7 exactly as it stands; the two are registered as separate queries with separate companions (C-C6, C-C7) | D5 |
| **C-Q8** | **The signature/bytes judge — REWRITTEN 2026-09-15 round 4, finding 1.** *(The round-3 form quantified over honest-released signature terms. It is **withdrawn**: a judge that only inspects triples whose signature term an honest issuer released cannot see an acceptance whose signature the **attacker** made, so a mutation that unbinds those escapes it. Round 3's shape is kept below only as the thing the rewritten query must **not** be.)* The *producer* of **R-bytes**, the §A3.2 chain's last link (D6), which no committed query and no other capstone query establishes. The relation, in the library's terms: *for **every** acceptance, the signature `sg` accepted under key `kX` over presented framed bytes `fb` satisfies `checksign(sg, kX) = (BYTES, fb)` for the **presented** `fb`*. **Event signature:** `event SigBytesUnbound(pkey, bitstring, bitstring)` — *(accepting key, signature term, presented framed bytes)*. **Wiring (rewritten):** the verifier reports the triple `(kX, sg, fb)` at **every** acceptance point, for every layer and every signer slot, whoever made `sg`; the judge is a **structural** test with **no honest-signature filter** — it fires `SigBytesUnbound(kX, sg, fb)` unless `checksign(sg, kX)` is exactly `(BYTES, fb)`, **including the case where `sg` does not verify under `kX` at all** (the destructor's `else` branch). No honest issuer's private release feeds it; the honest-origin and transplant claims are **C-Q7's** and stay separate. **Fixture:** C-Q1's, §6(4) below, all four compromise cases. **Compromise cases:** (a) strict `skD` public, (b) strict `skR` public, (c) strict both public, (d) degraded sole channel public — the relation is structural, so it is registered unreachable in **all four**. **Registered unreachable.** **Honest witnesses:** `HonestAccepted(kH, fbH)` and C-Q1's `HonestChain` reachable in the same fixture. **Feasibility and discrimination, checked on copies (round 4):** green on the committed S-P1 verifier (`d6c_sp1_q8_judge_all.out:284` `is true`, witness `:469`); **red** under the reviewer's escape — byte equality kept for signatures over `OT_ATTEST` frames, unbinding permitted for every other signed frame type — which the **withdrawn round-3 form passes**: `d6d_sp1_q8_type_conditional_unbound.out:507` `is false` (rewritten) against `:315` `is true` (round-3 honest-filtered) and `:308` `is true` (C-Q7), with honest-key authorship still `is true` `:515` and the witness reachable `:692`; and **red** under C-C7's same-key byte unbinding as well (`d6e_sp1_q8all_samekey_unbound.out:643` `is false`, C-Q7 still `is true` `:274`, witness `:989`). **Without C-Q8, D6 has no producer and is not a row — it is an open obligation** | D6 (and C-Q1's link 4) |
| **C-Q9** | **The possession/manifest judge (new, 2026-09-15 round 3, finding 2)** — the *producer* of what D10's consumer needs, which S-P3's `PossessionTransplanted` does not establish. The relation: *for a completed acceptance reporting key `kX` and accepted manifest `t`, the accepted possession proof `ppf` satisfies `checksign(ppf, kX) = (POSS, t)` for the same `t` the verifier accepted.* **Event signature:** `event PossessionUnbound(pkey, bitstring, bitstring)` — *(accepting key, accepted manifest/authority tuple, accepted possession proof)*. **Wiring:** the verifier reports `(kX, t, ppf)` on a private channel at **every** acceptance point, once per signer slot; the judge fires when `checksign(ppf, kX)` is not `(POSS, t)`, including when it does not verify at all. **Registered unreachable.** **Honest witness:** both `HonestComplete` witnesses (one- and two-signer) and `HonestAccepted` reachable. Feasibility on a copy: green on the committed S-P2 verifier (`d10a_sp2_q9_base.out:1111`), red under the combined manifest-unbinding that leaves `PossessionTransplanted` green (`d10b_sp2_q9_manifest_unbound.out:1462` against `:1297`). **Independent of R-2**: R-2 decides whether D10 is a row, C-Q9 decides whether it has a producer; and C-Q1's per-layer possession link needs C-Q9 whatever R-2 says | D10, and C-Q1's possession link (D4, D7) |
| C-Q5 | **`SetAltered`** — S-P2's `MemberJudge` shape: no honest key is reported as a signer of a manifest it never signed. *Added 2026-09-14: the first draft required companion C-C3 to falsify this query and never registered it.* Registered with C-Q5w below whether or not R-2 makes D10 a row, so the redundancy is represented rather than assumed | D10 |
| C-Q5w | **The honest-flow witness for C-Q5** — `HonestComplete` over each set size (one-signer and two-signer manifests), reachable in the correct model and in **both** isolation configurations (either pin alone), so that C-C3's red is a severing and not a broken fixture | D10 |
| C-Q6 | *(§2(c); **R-3 RULED formulation W**, author, 2026-09-15)* wrapped-standing linkage over the **composed** fixture: S-P7's wrapper processing feeding S-STANDING's standing assessment, standing binding to the innermost issuance identity. **It is written in formulation W** — the conclusion is a **standing verdict**: *"an `ESTABLISHED` report computed over a **wrapped** presentation implies the **innermost** issuer designated the reported identity, and the key it is computed against is the one the evidenced tuple names."* It therefore **consumes L-16 and L-17**, which are rows **D12** and **D13** of §2(c), and the capstone inherits L-16's residual — `h` injectivity as *"the whole load of the transplant result"* (L2-c) — and the two-entry-lineage scoping. *(Formulation N, which stops at the attributed identity and consumes neither, is not built.)* The formulation is fixed before predictions freeze, as the ruling requires. **Round 4, finding 2: C-Q6 is D11's *second* consumer, not its only one** — C-Q1's link 6b consumes L-13's scope relation unconditionally, so D11 is a matrix row whether or not C-Q6 is ever registered | D11's conditional half (+ D12, D13 under W) |
| C-N1 | A vacuity witness per fixture — honest-flow acceptance emitted by the judge, never bare acceptance (S-P3 recut 3, carried to every family) | all |

### C-Q1 — the query contract

*Written 2026-09-15 round 3 (finding 4). The draft gave C-Q1 one
sentence and made it serve D4, D6, D7 and D8 without an event
signature, an explicit correspondence, or a strict/degraded split —
and findings 1 and 2 turned on exactly the distinctions that sentence
elided. A builder cannot write this query from the old cell. Below is
what must be fixed before predictions freeze.* **C-Q1 is not written
here; its contract is.**

**(1) Event signatures** — in the library's terms (`lib/tessera_theory.pvl`
D-1…D-6 and the model-local seven-field `framed`, copied verbatim, NOT
promoted). The capstone's verifier emits one report per completed
acceptance, per layer, carrying *every* term the chain links:

| Event | Arguments | Emitted where |
|---|---|---|
| `AuthorityEvidence(bitstring, bitstring, pkey)` | authority tuple `t`, the evidence term `ev = sign((STMT_DIGEST, h(t)), skCh)` (or `(STMT_DIRECT, t)` — D-1), the channel key the evidence verified under | after the evidence check, before anything else is read |
| `LayerAccepted(bitstring, bitstring, bitstring, bitstring, bitstring, pkey, bitstring, bitstring, bitstring)` *(two arguments added 2026-09-15 round 4: the **acceptance identifier** — finding 4 — and the **accepted evidence term** — finding 3)* | **acceptance identifier `aid`** — **a fresh name (`new aid: bitstring`) minted once per completed acceptance, and nothing else.** *(Corrected 2026-09-15 after the author's ruling — non-author reviewer, Codex; owner accepted. The round-4 cell offered the **aggregate package term** as an equal alternative; it is **not an acceptance identifier**. Replaying the same package gives **distinct acceptance executions the same term**, so a completeness conjunct (link 2b) could be satisfied by slot reports drawn from different executions. Completeness means **every required slot was checked in THIS execution**, which only a per-acceptance fresh name expresses. "Serve equally" is withdrawn, and with it the instruction to choose between them before predictions freeze — there is nothing to choose.)* layer id (`L0` for the base object, `L1`/`L2` for wrapper depths — named constants, depth bounded at 2 per L-13), authority tuple `t`, **the accepted evidence term `ev`** (or a reference naming the `AuthorityEvidence` report this acceptance consumed), signer-slot identifier (`kfpr` as the signed set names it — `signers0` / `signers1(·)`, D-2), the accepting key `kX`, the possession proof `ppf`, the signature term `sg`, the **presented** framed bytes `fb` | **once per signer slot** of that layer's acceptance, all slots of one acceptance carrying the **same `aid`**, in the S-P3 recut-1 idiom (report outputs parallel with continuations) |
| `AcceptanceComplete(bitstring, bitstring, bitstring)` *(new 2026-09-15 round 4, finding 4)* | acceptance identifier `aid`, layer id, authority tuple `t` | at the **single** acceptance point of that layer, **after** every `LayerAccepted` report of that acceptance; it is the antecedent of the completeness correspondence (link 2b) |
| `ChainBroken(bitstring, bitstring)` | layer id, the name of the link that failed | fired by the judge; **this is the query's subject** for links 1a, 2a, 3, 4, 5, 6a, 6b. *(Corrected 2026-09-15 after the ruling: **link 1b is not among them** — it is a correspondence, like link 2b, because no judge can observe that a publication event never occurred.)* |
| `HonestChain(bitstring, bitstring)` | layer id, authority tuple | the honest-flow witness; **must be reachable** (C-N1) |

**(2) The correspondence, per layer.** `ChainBroken` must be
**unreachable**, and the **link-1b** provenance correspondence (strict
only) and the **link-2b** completeness correspondences must hold;
equivalently, for every `LayerAccepted(aid, lyr, t, ev, slot, kX, ppf,
sg, fb)` the judge observes, **all nine** links hold, each named so a
builder knows which term carries it. *(Round 4 raises the count from
six to nine: link 1 splits into 1a/1b — finding 3; link 2 splits into
2a/2b — finding 4; link 6 splits into 6a/6b — finding 2.)*

| # | Link | Stated over the terms above | Producer today |
|---|---|---|---|
| 1a | **evidence → this acceptance** *(new, round 4, finding 2 of the dispositions / review finding 3)* | the evidence term `ev` **this** acceptance carried is evidence over **the statement this acceptance consumed**: `checksign(ev, kCh) = (STMT_DIGEST, h(t))` — or `(STMT_DIRECT, t)`, D-1 — for the accepted `t` and some authority-channel key `kCh` the fixture declares, **including the case where `ev` does not verify at all** (the destructor's `else` branch). A declared-but-unconsumed `AuthorityEvidence` event does **not** discharge this link: the binding is to `aid`, not to the existence of a validation somewhere in the trace | **Structural — the capstone's own verifier**, in the same class as links 2a, 3, 4, 5, 6a, 6b: a relation among terms the verifier itself checked. No external producer is named and none is claimed. Its severing companion is **C-C10** |
| 1b | **authority → tuple** *(what link 1 used to be, minus 1a; **re-specified as a correspondence 2026-09-15 after the author's ruling** — non-author reviewer, Codex; owner accepted)* | **A correspondence, not a `ChainBroken` conjunct.** A judge inside the model cannot observe that a publication event *never occurred*; it can only observe what this acceptance carried. So 1b is asserted the way ProVerif asserts provenance — **acceptance implies a prior authority-publication event for the consumed tuple**: `event(LayerAccepted(aid, lyr, t, ev, slot, kX, ppf, sg, fb)) ==> (event(AuthorityPublishedDNS(t)) \|\| event(AuthorityPublishedRepo(t)))`, in the library's own event names (`lib/tessera_theory.pvl:190-191`), quantified over every acceptance the judge observes and registered `is true`. *(The withdrawn wording — "the accepted `t` is the tuple an uncompromised authority channel **published**" as a conjunct the judge tests, firing `ChainBroken` when it fails — asked the judge for a negative observation it cannot make. The correspondence form is exactly S-P3 Q1(ii)'s own shape, which is why Q1(ii) is its producer.)* **Strict only**, per the strict/degraded contract below | S-P3 Q1(ii), green (D3/D4) |
| 2a | **tuple → slot** | `t`'s signer set names `slot`, and `fp(kX) = slot` — the per-slot fingerprint match, read from the **signed** tuple | S-P2 Q2 `SignerForged`, green (D7) |
| 2b | **required set → completeness** *(new, round 4, finding 4)* | **a `LayerAccepted` record for *every* required slot of `t`, grouped under the same `aid`.** As a correspondence, one conjunct per required-set shape: `event(AcceptanceComplete(aid, lyr, authTuple(id, fpA, signers0, alg, ver))) ==> event(LayerAccepted(aid, lyr, …, fpA, …))`, and for `signers1(fpB)` **both** `… ==> event(LayerAccepted(aid, lyr, …, fpA, …))` **and** `… ==> event(LayerAccepted(aid, lyr, …, fpB, …))`. *Per-slot membership (2a) does not imply this: every reported slot can belong to the manifest and match its key while a required slot has no report at all.* In practice the capstone may project `LayerAccepted` to a two-place `SlotSatisfied(aid, t, slot)` for the antecedent's sake; the obligation is the same | S-P2 Q2 `Stripped`, green (D7). Its severing companion is **C-C9** |
| 3 | **slot → possession** | `checksign(ppf, kX) = (POSS, t)` — possession over the **accepted manifest**, under the **accepting key**, D-3 | **NONE — C-Q9** (round 3, finding 2) |
| 4 | **possession → signing** | `checksign(sg, kX) = (BYTES, fb)` over the **presented** `fb` — the R-bytes relation, for **every** accepted triple including one whose signature does not verify | **NONE — C-Q8 as rewritten** (round 3, finding 1; rewritten round 4, finding 1) |
| 5 | **signing → bytes** | `fb = framed(ot, alg, id, fp(kX), h(t), cv, pl)`: the frame's fourth field is the accepting key's fingerprint and its fifth is the accepted tuple's hash; and, for `\|set\| = 2`, the six non-fingerprint fields agree across slots (L-09's shared-term mapping: `alg`, `issuerId`, `manifestHash` pinned through `t`; `objType`, `canonVer`, `payload` equated by the §A5.4 guards) | **Two halves, two answers.** Cross-slot agreement: S-P2 Q2 + Q6 `Spliced`, green (D7). Frame-to-key (`kfp = fp(kX)`): that is L-01's key binding, whose producer S-P3 Q2 `Reattributed` is green — **and **R-1 is ruled Reading B (author, 2026-09-15), so S-P3 Q2 IS this link's producer** — the capstone's single composed verifier carries S-P3's key binding, which is exactly what Reading B means, and D1/D2 are matrix rows on it (§2(a)). *(Under the superseded Reading A the capstone would have had to establish this half in its own verifier with no producer named.)* |
| 6a | **bytes → layer TYPE** *(split from link 6, round 4, finding 2)* | `ot` is the object type this layer was processed *as* (D-5 `OT_*`) | S-P7 Q2/Q1 `TypeConfused`, green (**D8**) |
| 6b | **bytes → innermost-issuer SCOPE** *(split from link 6, round 4, finding 2)* | for `lyr ≠ L0`, the inner frame's `(issuerId, kfp)` is the **innermost** issuance identity, not the wrapper's — the attribution the layer is scoped to | S-P7 Q2/Q5 `Rescoped` / `RescopedD1` / `RescopedD2`, green (**D11**). **A separate property from 6a, and shown to be separate by S-P7's own Q6b companion**, which reads key and authority from the *outermost* frame: `TypeConfused` stays unreachable (`sp7_q6b_companion_key_outermost.out:489` `is true`) while `Rescoped` becomes reachable (`:769` `is false`) and both honest witnesses stay reachable (`:1317`, `:1508`). **D8's type producer does not supply this conjunct** |

**Two of the nine links have no producer today.** Links 3 and 4 are
exactly the two near-miss producers rounds 2 and 3 found (`C-Q9`,
`C-Q8`). **C-Q1 cannot be registered as discharging D4, D6, D7, D8 or
D11 until C-Q8 and C-Q9 are registered and green**, and the register
claims nothing else for it. Link 1a names **no** producer at all and
claims none: it is a structural conjunct of the capstone's own verifier,
and what the register owes for it is a companion (C-C10), not a
producer query.

**(3) The strict/degraded contract.** The register requires strict
first-link provenance through D4 while several fixtures run a
*compromised sole channel*, in which unrestricted authorship is already
red in the committed baseline (`sp1_q2_degraded_compromised.out:499`;
also `d5c_sp1_sigjudge.out:536`). A builder must know which conclusions
need an honest authority channel and which are structural binding
requirements that must hold regardless:

*Repaired 2026-09-15 round 4 (finding 3): the round-3 table dropped
**the whole of link 1** in degraded mode, which dropped
accepted-evidence binding with it. That is weaker than A3 §A3.2's chain,
which begins with **accepted external evidence bound to the consumed
statement** and is **fewer-but-never-zero** under waiver
(`docs/phase-0-prereg-amendment-3.md:115-120`, `:142-150`). Only the
**honest-publication conclusion** is dropped.*

| Conclusion | Mode | Needs an honest authority channel? |
|---|---|---|
| Link **1a**, **evidence → this acceptance** | strict **and** degraded | **No — a structural binding requirement, asserted in both modes.** It says the evidence *this* acceptance carried is evidence over *this* acceptance's statement; it says nothing about who published it. Degraded mode has fewer evidences, never zero (A3 §A3.2), so the binding is asserted over the one that was accepted |
| Link **1b**, **authority → tuple** (the honest-publication conclusion) | strict only | **Yes.** In degraded-compromised mode the sole channel signs anything, so 1b is not asserted; C-Q1's degraded form drops **1b and only 1b** from link 1, and says so in the query text |
| Links 2a, 2b, 3, 4, 5, 6a, 6b | strict **and** degraded | **No — structural binding requirements.** Each is a relation among terms the verifier itself checked; none quantifies over channel honesty. They must hold in both modes, and a degraded run in which any of them fails is a defect, not a waiver cost |
| The unrestricted form — *any* acceptance implies the accepting key's holder signed | degraded-compromised | **Registered red** (the A4.6 cost, S-P1 Q2(ii)). C-Q1 must **not** assert it, and must carry the honest-key restriction the way S-P1's Q2(i) does |

**Shown on copies, round 4 (finding 3):** in the **degraded**,
sole-channel-compromised fixture, removing *only* the verifier's
evidence check turns an explicit evidence-binding query from green to
red while every other conclusion keeps its baseline outcome —
`cq1a_sp1_evidence_base.out:322` `is true` → `cq1b_sp1_evidence_unchecked.out:466`
`is false`, with C-Q7 (`:301`), the withdrawn round-3 C-Q8 (`:307`),
the rewritten C-Q8 (`:313`) and honest-key authorship (`:474`) all
still `is true`, the honest witness reachable (`:638`) and Q2(ii) `is
false` as registered (`:776`). The same conclusions in the unmutated
baseline: `:304`, `:310`, `:316`, `:330`, `:507`, `:658`. **So link 1a
is a separate obligation from links 2a–6b and from link 1b, and the
degraded form must carry it.**

The two forms are separate registered queries — **C-Q1-strict** and
**C-Q1-degraded** — with the same events and the same judge, differing
only in **link 1b** — link 1a is asserted in both (round 4, finding 3)
— and in the fixture's channel leak. Predictions freeze
separately for each (ENUM §5).

**(4) The fixture.** One model (ENUM §3), the library transcribed as
listed above, and: two authority-channel keys `skD`, `skR` (strict; the
degraded form has one); an issuer key `skI` and a second issuer `skI2`
(N2); a second required signer `skB2` for the `|set| = 2` branch; a
wrapper key `skW` over an `OT_WRAPPER` frame (S-P7's shape, depth ≤ 2);
`dsks` available to the adversary (D-4); adversary-chosen payloads
throughout. **Compromise cases, each its own run:** (a) strict, `skD`
public; (b) strict, `skR` public; (c) strict, **both** public — the
C-C1 companion, which must break **link 1b** and nothing else — in
particular it must leave **link 1a** green, which is why 1a has its own
companion **C-C10**; (d) degraded,
the sole channel public. The L-07 signing-domain enumeration must be
exercised in the same fixture: `STMT_DIGEST` under a channel key;
`POSS`, `BYTES` and `TLR` under the **same** issuer key; `STMT_DIRECT`
and `REFUSAL` recorded as declared-and-unexercised.

**(5) Expected outcome.** `ChainBroken` **unreachable** in (a), (b) and
(d) — for C-Q1-degraded in (d), with link **1b** dropped and link 1a
retained (finding 3) — **the link-1b provenance correspondence `is true`
in (a) and (b)** and not asserted in (d) *(corrected 2026-09-15: 1b is a
correspondence, not a `ChainBroken` conjunct)*, **every link-2b
completeness correspondence `is true`** in all four cases (finding 4),
and `HonestChain`
**reachable** in every one of the four, at every layer the fixture
exercises (`L0`, `L1`, and `L2` for the depth-2 case). **Named
witnesses:** `HonestChain(L0, t)`, `HonestChain(L1, t)`,
`HonestChain(L2, t)`, C-N1's per-fixture `HonestAccepted`, and both
set-size `HonestComplete` witnesses over the `|set| = 1` and `|set| = 2`
branches (C-Q5w). A run in which any of them is unreachable is a broken
fixture and not a result. **Nothing here is a prediction of the
answer**; ENUM §5's three named outcomes and the per-query timebox are
declared before the run.

### REQUIRED capstone queries — the retained checks

*Listed 2026-09-15 round 3 (finding 4). These appear in §2's rows and
in the companion requirements below, which makes them **required**, not
optional additions. The draft's minimum table did not name them, so a
builder reading only that table would omit queries the companions must
falsify or preserve.* All are registered in the capstone in addition to
C-Q1…C-Q9 and C-N1.

| Query | Shape | Why required |
|---|---|---|
| `Accept ⟹ IssuerSigned` (strict) | **D3's own query**, S-P1 Q1(i) transcribed | C-C1 must **falsify** it; D3 is a matrix row and had no entry in the minimum table |
| `AcceptedUnderHonestKey ⟹ IssuerSigned` | S-P1 Q2(i), honest-key authorship | C-C1 must **preserve** it (green); C-C6 exists to show it stays green while C-Q7 goes red |
| `Stripped` | S-P2 `SetJudge`: an honest manifest accepted with fewer signers than it names | C-C2's set (2) requires it green; C-C3's set (2) requires it green; D7's producer |
| `SignerForged` | S-P2 `MemberJudge`: a slot the signed set assigns to an honest signer, satisfied by another key | same; and it is why C-C2's three-removal variant was withdrawn (`m7_all_three.out:625`) |
| `Spliced` | S-P2 Q6 `ContentJudge` over the two frames of one acceptance | C-C2's set (2) requires it green; **absent from the C1/C2/C3 ladder models**, so the capstone's transcription must add it to C-C3's set (2) as well |
| `TypeConfused` | S-P7 Q2/Q1: acceptance *as* type `T` implies the bytes' `objType` is `T` | C-C4's and C-C5's set (2) require it green; D8's producer |
| `VersionLied` | S-P7's canonicalization-version judge | C-C4's and C-C5's set (2) require it green |
| `Rescoped` | S-P7 Q2: standing/attribution binds to the innermost issuance identity | C-C5's set (2) requires it green; C-C4 **fails** it by design |
| **C-Q5 `SetAltered`** | S-P2 `MemberJudge`: no honest key is reported as a signer of a manifest it never signed | already registered above as C-Q5; repeated here because C-C3 must falsify it and C-C8 must **preserve** the distinction between it and C-Q9 |

**Every one of these is a query the capstone registers with a frozen
prediction.** Naming them here does not predict their colour.


**Companions the capstone must build.** *Rewritten 2026-09-15 (finding
5): the draft's blanket instruction — each companion red on "exactly
its named query" — contradicted its own evidence, since C-C4 reds three
queries and C-C2's three-removal variant reds `SignerForged`, which the
same row requires green.* Each companion is now specified by **three
sets**, all three verified against a `.out` and cited by line:

1. **Expected failed-query set** — every query the mutation turns red.

   **Rule replaced, 2026-09-15 round 3 (finding 3).** The draft said:
   *"and no other. A red outside this set is a broken fixture, not a
   severing."* **That rule is withdrawn.** Every set below is specified
   against a **family-local** run — one family's model, one family's
   query names, one family's fixture — and a family-local run cannot
   establish an exhaustive result set for the enlarged, composed
   fixture. A capstone query that no family model declares (C-Q1's
   `ChainBroken`, C-Q6, C-Q8, C-Q9) cannot appear in a set derived from
   a model that does not declare it, and a composed fixture can red a
   query for a reason the single-family run could not exhibit. In
   place of the withdrawn rule:

   - each set below is **valid as specified today, against the cited
     `.out`, for the family-local run it names** — and is cited that
     way, never as a capstone-wide result;
   - each set **MUST be re-specified against the capstone's own query
     names once C-Q1…C-Q9 exist**, before predictions freeze, and the
     re-specification is itself a registered step;
   - until then, a red outside a listed set is **an unresolved
     observation**: it may be a broken fixture, or it may be a real
     consequence of composition the family-local run could not show.
     It is investigated and recorded, not silently classified.

2. **Guarantees that must stay green** — the queries whose truth the
   mutation must not disturb, which is what shows the companion severs
   *the named fact* and not the model.
3. **Witnesses that must stay reachable** — the honest-flow events,
   which is what shows the model still admits an honest run.

Each must sever **the named producer fact** — not merely turn some
consumer query red. *Repaired 2026-09-14: C-C2 as first drafted did not
sever anything, and D2/D5's companions named a different failure.*

| # | Companion | Mutation | (1) Expected failed-query set | (2) Must stay green | (3) Witnesses that must stay reachable | Row | Verified against |
|---|---|---|---|---|---|---|---|
| **C-C1** | Both channel keys public, strict form | `out(c, skD); out(c, skR)` in place of the single leak | **Two queries, not one** *(corrected 2026-09-15 round 3, finding 3: the draft listed `Accept ⟹ IssuerSigned` **only**, although this companion serves **both** D3 and D4, and D4 separately requires the capstone's linkage query to fail).* **(a)** `Accept ⟹ IssuerSigned` — **shown** red family-locally (`s6_bothchannels.out:361` `is false`), which is D3's requirement. **(b)** **C-Q1's link-1b correspondence `is false`** — `event(LayerAccepted(aid, lyr, t, …)) ==> (event(AuthorityPublishedDNS(t)) || event(AuthorityPublishedRepo(t)))`, which this mutation falsifies because with both channel keys public the adversary can produce accepted evidence for a tuple **no honest channel process ever published**, so an acceptance exists with no antecedent event. *(Re-specified 2026-09-15 after the ruling, with link 1b: the cell read "`ChainBroken` at link 1b, reachable". 1b is a **correspondence**, not a `ChainBroken` conjunct — a judge cannot observe a publication event's non-occurrence — so what the companion must expose is the correspondence going `is false`, not a `ChainBroken` firing.)* This is D4's requirement, and the one the capstone must add. *(Round 4, finding 3: "link 1" is now **link 1b** only. This mutation publishes both channel keys; it does not touch the evidence-to-acceptance binding, so **link 1a stays green under it** and D4's evidence conjunct needs its own companion, **C-C10**.)* It is **NOT YET SHOWN**: `ChainBroken` is declared in no model, so no `.out` can carry it. The register does not identify (b) with (a), and does not claim (a) discharges D4 | `AcceptedUnderHonestKey ⟹ IssuerSigned` (`:368` `is true`); and, in the capstone, **link 1a and links 2a–6b** of C-Q1 (the structural binding requirements, §6's strict/degraded contract), which this mutation must **not** disturb | `HonestAccepted` (`:559`); in the capstone, `HonestChain` at every layer | D3, D4 | scratch `s6_bothchannels.out`; baseline `base_sp1q1.out:201, :208, :396`. **Family-local; set (a) re-specified against the capstone's query names once C-Q1 exists** |
| **C-C2** | **The minimal two-removal severing**, multi-signer fixture: the frame's `=fp(k_)` pin **and** the manifest-hash equality. *Changed 2026-09-15 (finding 5): the "or all three with the tuple fingerprint match" alternative is **withdrawn** — `m7_all_three.out` reds `SignerForged` at `:625`, which set (2) requires green.* | not S-P3 Q3's single removal — that leaves the query green (`m1_framepin.out:399`) | `Reattributed` **only** (`m4_framepin_mh.out:620` `is false`) | `Stripped` (`:379`), `SignerForged` (`:392`), `SetAltered` (`:405`), `Spliced` (`:1263`) — all `is true` | both `HonestComplete` (`:791` one-signer, `:1015` two-signer) and `HonestAccepted` (`:1250`) | D1 | scratch `m4_framepin_mh.out`; baseline `base_sp2.out:378, :384, :390, :397, :561, :778, :1007, :1013` . **Family-local run; MUST be re-specified against the capstone's query names once C-Q1…C-Q9 exist (round 3, finding 3).** |
| **C-C3** | *(R-2 ruled "yes", 2026-09-15 — no longer provisional on a fork; D10's producer C-Q9 is still to be registered)* Both `SetAltered` routes removed: the frame's manifest-hash pin **and** possession-over-manifest | Q5-C2 shape | `SetAltered` **only** (`sp2_q5_c2_fponly_frame_nomh.out:535` `is false`) | `Stripped` (`:349`), `SignerForged` (`:356`), `Reattributed` (`:542`) — all `is true`. **`Spliced` is not a query in the C1/C2/C3 ladder models** (they predate the §A5.4 addendum); the capstone's transcription, which will carry it, must add it to this set | both `HonestComplete` (`:706`, `:925`) and `HonestAccepted` (`:1100`); **and the same three witnesses in both isolation configurations** — C1 `sp2_q5_c1_fponly_frame_mh.out:536, :756, :987` with `SetAltered` green `:366`, C3 `sp2_q5_c3_manifestposs_frame_nomh.out:534, :753, :983` with `SetAltered` green `:363` | D10 | committed `sp2_q5_c2_fponly_frame_nomh.out`, `…c1….out`, `…c3….out` . **Family-local run; MUST be re-specified against the capstone's query names once C-Q1…C-Q9 exist (round 3, finding 3).** |
| **C-C4** | The complete key-binding relation removed inside `InnerCheck`: inner `=fp(kI)` pin **and** `mhI = h(tI)` | not the inner pin alone — every query stays green (`s3_innerfp.out:527`–`:566`) | **three queries, by design**: `Rescoped` (`s4_innerfp_mh.out:864`), `InnerSigTransplanted` (`:1207`), `Reattributed` (`:1431`) — all `is false`. *The draft's "exactly its named query" was false of this companion and is withdrawn; the row it serves (D2) is the `Rescoped` half, and the other two reds are consequences of severing the same relation, not separate severings* | `TypeConfused` (`:526`), `VersionLied` (`:1949`) | `HonestWrappedAccepted` (`:1734`), `HonestAccepted` (`:1933`) | D2 | scratch `s4_innerfp_mh.out`; baseline `base_sp7.out:527, :540, :553, :566, :865, :1061, :1074`; isolation `s3_innerfp.out` . **Family-local run; MUST be re-specified against the capstone's query names once C-Q1…C-Q9 exist (round 3, finding 3).** |
| **C-C5** | The inner signature unbound from the presented bytes — S-P1 Q3's mutation transcribed into `InnerCheck` | `let (=BYTES, anyb) = checksign(sgI, kI)` | `InnerSigTransplanted` **only** (`s1_sig_unbound.out:897` `is false`) | `TypeConfused` (`:537`), `Rescoped` (`:560`), `Reattributed` (`:920`), `VersionLied` (`:1464`) | `HonestWrappedAccepted` (`:1233`), `HonestAccepted` (`:1442`) | D5 — **as evidence that byte binding matters, not as the discharge** (finding 1) | scratch `s1_sig_unbound.out`; contrast `s2_sig_removed.out:852` (a11 shape: same query red, but by severing an S-P7 check) . **Family-local run; MUST be re-specified against the capstone's query names once C-Q1…C-Q9 exist (round 3, finding 3).** |
| **C-C6** *(new, 2026-09-15, finding 1)* | The **conditional** unbinding: the presented bytes must equal the signed bytes only when the signed frame's own `kfp` matches the verifying key | the reviewer's 2026-09-15 diagnostic, reproduced | **C-Q7 `SigTransplanted`** (`d5d_sp1_sigjudge_condunbind.out:414` `is false`) and, in the S-P7 fixture, `InnerSigTransplanted` (`d5b_sp7_condunbind.out:1037` `is false`) | **the whole point of this companion**: `AcceptedUnderHonestKey ⟹ IssuerSigned` stays `is true` (`d5a:195`, `d5b:654`, `d5d:422`) and `Reattributed` stays `is true` (`d5b:1060`), together with `TypeConfused` (`d5b:677`), `Rescoped` (`d5b:700`), `VersionLied` (`d5b:1599`) | `HonestAccepted` (`d5a:371`, `d5b:1576`, `d5d:599`), `HonestWrappedAccepted` (`d5b:1370`) | *(Set (1) completeness — skeptic 2026-09-15: `AcceptS ⟹ IssuerSigned` is also `is false` in `d5a:521`, `d5c:536` and `d5d:750`. It is **not** a red this mutation causes: it is `is false` in the unmutated committed producer too (`sp1_q2_degraded_compromised.out:499`), the registered Q2(ii) cost. Recorded here so the set is not read as exhaustive of the `.out`.)* D5, D6 — it is the companion **for C-Q7**, and the proof that S-P1's Q2(i) is not C-Q7's producer | scratch `d5a_sp1_condunbind.out`, `d5b_sp7_condunbind.out`, `d5c_sp1_sigjudge.out`, `d5d_sp1_sigjudge_condunbind.out` . **Family-local run; MUST be re-specified against the capstone's query names once C-Q1…C-Q9 exist (round 3, finding 3).** |
| **C-C7** *(new, 2026-09-15 round 3, finding 1; **re-specified against the rewritten C-Q8**, round 4, finding 1)* | **Two configurations, both required**, because the rewritten C-Q8 must be shown to catch what the withdrawn form missed. **(i) The same-key byte unbinding:** the attestation signature must verify under `kX` over *some* frame naming `fp(kX)`, but no longer over the **presented** bytes (`let (=BYTES, fbS: bitstring) = checksign(sg, kX) in let framed(otS, algS, idS, =fp(kX), mhS, cvS, plS) = fbS in`). **(ii) The type-conditional unbinding** *(new, round 4)*: byte equality between the signed and the presented frame is required **only** when the signed frame's `objType` is `OT_ATTEST`, and is waived for every other signed frame type — the reviewer's round-4 escape | (i) the reviewer's round-3 finding-1 diagnostic; (ii) the reviewer's round-4 finding-1 escape, both reproduced on our tree | **(i)** **C-Q8 as rewritten** (`d6e_sp1_q8all_samekey_unbound.out:643` `is false`), the withdrawn round-3 form (`:455` `is false`) and, as a consequence in the same model, S-P1's own `AcceptedUnderHonestKey ⟹ IssuerSigned` (`:809` `is false`). **(ii)** **C-Q8 as rewritten, and it alone** (`d6d_sp1_q8_type_conditional_unbound.out:507` `is false`) | **the whole point of this companion**: in (i), **C-Q7 `SigTransplanted` stays `is true`** (`d6e:274`) — C-Q7 is not C-Q8's substitute. In (ii), **the withdrawn round-3, honest-filtered C-Q8 stays `is true`** (`d6d:315`), **C-Q7 stays `is true`** (`d6d:308`) and **honest-key authorship stays `is true`** (`d6d:515`) — which is the demonstration that the round-3 quantifier let a real unbinding through and the rewritten judge does not | (i) `HonestAccepted` (`d6e:989`); (ii) `HonestAccepted` (`d6d:692`) | D6 — it is the companion **for C-Q8**, the proof that C-Q7 is not D6's producer, and (configuration ii) the proof that the honest-filtered form of C-Q8 is not the structural producer either | baseline `d6c_sp1_q8_judge_all.out` (C-Q7 `:272`, round-3 C-Q8 `:278`, rewritten C-Q8 `:284`, Q2(i) `:292` all `is true`, witness `:469`); mutants `d6e_sp1_q8all_samekey_unbound.out`, `d6d_sp1_q8_type_conditional_unbound.out`. Superseded baseline: `d6a_sp1_q8_base.out` (`:244`, `:250`, `:258`, `:435`), whose C-Q8 is the withdrawn form. *Set (1) note, as for C-C6: `AcceptS ⟹ IssuerSigned` is also `is false` (`d6c:620`, `d6d:876`, `d6e:1168`) in the mutants **and** in the baseline — the registered Q2(ii) cost, not a red these mutations cause.* **Family-local; re-specified against the capstone's query names once C-Q8 exists** |
| **C-C8** *(new, 2026-09-15 round 3, finding 2)* | **Both manifest-binding protections removed together** — the companion **for C-Q9**: possession made fingerprint-only (`let (=POSS, =fp(kX)) = checksign(ppfX, kX)`, the library's D-3 under-encoding, a broken companion *by library definition*) **and** the frames' `mh = h(t)` guards dropped. The seven-field frames, the per-slot `=fp(kX)` pins, the tuple fingerprint matches and the three §A5.4 content guards are all **retained** | the reviewer's round-3 finding-2 diagnostic, reproduced on our tree | **C-Q9 `PossessionUnbound`** (`d10b_sp2_q9_manifest_unbound.out:1462` `is false`) and, as the consumer consequence, **`SetAltered`** (`:673` `is false`) | **the whole point of this companion**: **S-P3's `PossessionTransplanted` stays `is true`** (`d10b:1297`) — the demonstration that the key-only theorem is not C-Q9's substitute — together with `Stripped` (`:454`), `SignerForged` (`:464`), `Reattributed` (`:683`), `Spliced` (`:1287`) | both `HonestComplete` (`d10b:851` one-signer, `:1072` two-signer) and `HonestAccepted` (`:1277`) | D10 — it is the companion **for C-Q9**, and the proof that `PossessionTransplanted` is not D10's producer | scratch `d10a_sp2_q9_base.out` (baseline: all five S-P2 queries `:457, :464, :471, :478, :1097` `is true`, `PossessionTransplanted` `:1104`, C-Q9 `:1111` `is true`, witnesses `:643, :861, :1090`), `d10b_sp2_q9_manifest_unbound.out`. **Family-local; re-specified against the capstone's query names once C-Q9 exists** |
| **C-C9** *(new, 2026-09-15 round 4, finding 4)* | **The required-set requirement dropped from the one-signer branch** — the companion **for C-Q1's link 2b**, and **D7's re-specified companion**: `Verifier1S`'s `let authTuple(id, kfprA, =signers0, alg, ver) = t in` becomes `let authTuple(id, kfprA, ss, alg, ver) = t in`, so a two-signer manifest can complete through the one-signer branch. **Every per-slot check is retained** — each reported slot still belongs to the manifest and still matches its key — which is exactly why per-slot membership (link 2a) cannot stand in for completeness | the reviewer's round-4 finding-4 diagnostic, reproduced on our tree | **C-Q1's link-2b completeness correspondence for the two-signer required set** (`cq1d_sp2_slots_missing.out:1519` `is false` — the slot-B conjunct) **and** S-P2's `Stripped` (`:643` `is false`) | the point of the companion: **the per-slot conjuncts survive** — link 2b's slot-A conjunct (`:1353`) and the one-signer conjunct (`:1333`) stay `is true`, as do `SignerForged` (`:650`), `SetAltered` (`:657`), `Reattributed` (`:664`), **`Spliced`** (`:1305`), `PossessionTransplanted` (`:1312`) and **C-Q9** (`:1319`) | both `HonestComplete` (`cq1d:835` one-signer, `:1061` two-signer) and `HonestAccepted` (`:1298`) | **D7** — it now falsifies **C-Q1's completeness conjunct**, not only `Stripped` (round 4, finding 4); S-P2's own Q3/Q4/Q6-C stay as the family-local contrasts | baseline `cq1c_sp2_slots_base.out` (`Stripped` `:471`, `SignerForged` `:478`, `SetAltered` `:485`, `Reattributed` `:492`, `Spliced` `:1133`, `PossessionTransplanted` `:1140`, C-Q9 `:1147`, and all three link-2b conjuncts `:1161`, `:1175`, `:1189` — every one `is true`; witnesses `:663`, `:889`, `:1126`); mutant `cq1d_sp2_slots_missing.out`. **Family-local; re-specified against the capstone's query names once C-Q1 exists** |
| **C-C10** *(new, 2026-09-15 round 4, finding 3)* | **The degraded verifier's evidence check removed, and nothing else** — the companion **for C-Q1's link 1a**: `let (=STMT_DIGEST, =h(t)) = checksign(ev, pkS) in` is deleted from the degraded verifier, so the accepted evidence term is carried into the acceptance unexamined. Tuple fingerprint, possession over the manifest, the attestation signature over the presented bytes, the in-bytes P3 binding and `mh = h(t)` are all **retained** | the reviewer's round-4 finding-3 diagnostic, reproduced on our tree | **C-Q1's link-1a evidence-binding conjunct** (`cq1b_sp1_evidence_unchecked.out:466` `is false`) | the point of the companion: **every other conclusion keeps its baseline outcome** — C-Q7 (`:301`), the withdrawn round-3 C-Q8 (`:307`), **the rewritten C-Q8** (`:313`) and honest-key authorship (`:474`) all still `is true` | `HonestAccepted` (`cq1b:638`) | **D4** — it is the companion for the evidence conjunct of C-Q1's first link, which C-C1 (both channel keys public) does **not** reach: C-C1 breaks link **1b**, publication, and leaves 1a standing | baseline `cq1a_sp1_evidence_base.out` (C-Q7 `:304`, round-3 C-Q8 `:310`, rewritten C-Q8 `:316`, **link 1a** `:322`, Q2(i) `:330` — every one `is true`; witness `:507`); mutant `cq1b_sp1_evidence_unchecked.out`. *Set (1) note, as for C-C6/C-C7: `AcceptS ⟹ IssuerSigned` is `is false` in the mutant (`:776`) **and** in the baseline (`:658`) — the registered Q2(ii) cost, not a red this mutation causes.* **Family-local; re-specified against the capstone's query names once C-Q1 exists** |

**Companions that exist and are red on their own family's query**, to be
transcribed rather than rebuilt, but which do **not** yet discharge
anything: S-P2 Q3/Q4/Q6-C (D7 — *contrasts only from round 4: D7's
registered companion is **C-C9**, which falsifies C-Q1's completeness
conjunct and not only `Stripped`*), S-P7 Q3 + ablation a10 (D8), first-link
Q2 (D9), S-P1 Q3 (D6 — but only as a *contrast*, not as D6's companion,
which is **C-C7**; and note that S-P1 Q3's *full* unbinding reds
S-P1's own Q2(i) at `sp1_q3_companionA_sig_unbound.out:331`, whereas
C-C6's *conditional* unbinding does not; the two are different
mutations and only the second isolates the relation D6 names), S-P7
Q6a/Q6b/Q5c (D11); and, **R-3 being ruled formulation W** (author,
2026-09-15), S-STANDING Q2/Q4/abl6 (D12) and Q3 (D13). The capstone's work is to
show the same mutation red on the **consuming** query, which is the
A3.3 gate text's actual demand. **Q6b is not a companion for D2 or
D5** — it severs the scope relation and permits key substitution, not
the key-binding or authorship facts those rows name.

**What the capstone must not do**: mark L-05, L-19 or L-21
discharged (cross-formalism — red bar); absorb any L2-a…L2-n item into
a checked cell (including the §3(b) rows — they are unclaimed **today**
and become *citations* when E3 and E6 land, never checked cells here);
treat L-14's by-construction encoding as a producer; read L-01 as
discharging S-P1's authorship (A7 §A7.10 — they are complementary, and
the discharge matrix carries no cross-model key-binding row between
S-P3 and S-P1); **read S-P1's Q2(i) as the producer of the §A3.2
chain's last link or of `InnerSigTransplanted`** (finding 1 — it is
not); **read C-Q7 as the producer of the §A3.2 chain's last link**
(round 3, finding 1 — it is not; C-Q7 observes `(acceptedKey,
signature)` and is blind to different bytes under the same key; **C-Q8**
is that link's producer); **read S-P3's `PossessionTransplanted` as the
producer of `SetAltered`** (round 3, finding 2 — it is not; it compares
keys only; **C-Q9** is); **read any companion's family-local failed-query
set as exhaustive for the composed fixture** (round 3, finding 3);
**build C-Q8 in its round-3, honest-filtered form** (round 4, finding 1
— a judge that only inspects triples whose signature an honest issuer
released is escaped by unbinding the rest: `d6d:315` green while
`d6d:507` is red; the registered C-Q8 is the structural judge over
*every* accepted triple, including failed verification); **assign
C-Q1's link 6b innermost-issuer scope conjunct to D8's type producer**
(round 4, finding 2 — `TypeConfused` and `Rescoped` are independent,
`sp7_q6b_companion_key_outermost.out:489` against `:769`; 6b's producer
is S-P7 Q2/Q5, D11); **drop C-Q1's evidence binding in the degraded
form** (round 4, finding 3 — only link 1b, honest publication, is
dropped; link 1a is asserted in both modes, A3 §A3.2's
fewer-but-never-zero, and a declared-but-unconsumed `AuthorityEvidence`
event does not close it); **read C-Q1's per-slot correspondence as
expressing required-set completeness** (round 4, finding 4 — it does
not: `cq1d:1353` green while `cq1d:1519` is red; link 2b, grouped under
one acceptance identifier, is the completeness conjunct); **restate the L-07 whitelist in its two-tag form** (it
is false of the composed fixture — S-STANDING signs `(TLR, body)` under
the issuer key); or **claim the `REFUSAL` domain checked** — no committed
model in this suite signs one (*narrowed — skeptic 2026-09-15: two
S-STANDING falsification **scratch** fixtures do,
`a_foreign_tag.pv:342` and `m_foreign_tlr_tag.pv:342`; neither is a
model and neither is registered*).

---

## Review log

- **2026-09-14** — drafted by the AI collaborator (Claude Opus 5),
  directed by the owner instance, from: `s-p3/RESULTS.md`,
  `s-p1/RESULTS.md`, `s-p2/RESULTS.md`, `s-p7/RESULTS.md`,
  `s-standing/RESULTS.md` (ledger sections, "does not discharge"
  sections, and both cross-family-review disposition sections),
  `formal/spike/first-link/RESULTS.md` and `DECISION.md`,
  `ENUMERATION.md` §§3–4 and notes 1–6, `formal/COVERAGE-MAP.md` rows
  and amendment notes 1–5, `lib/tessera_theory.pvl` header (D-1…D-6),
  `docs/implementation-spec.md` §5.5, A3 §A3.3 and A7 §A7.10.
  **No model was run. No family file was edited. No status was
  changed.** Non-author falsification review: **NOT RUN**. Author
  read: **owed** — the three routed items, and the matrix as a whole
  (BAND0-EXIT E5(a), then E5(c)).
- **2026-09-14, later** — non-author falsification review **RUN**
  (Codex CLI `gpt-6-astra`, `docs/reviews/2026-09-14-codex-review-ledger-and-k6.md`);
  the reviewer recommended **not** confirming the register as written.
  Every finding accepted by the owner instance and repaired in place;
  the repairs and the verification runs that back them are listed in
  the final section. The bullet above is left as written per
  amend-don't-rewrite: its *"No model was run"* and *"Non-author
  falsification review: NOT RUN"* describe the first draft and are
  superseded by this line. A **further** non-author review of the
  repaired file is owed before the capstone plan freezes; the author's
  read of the three routed items and of the matrix is still owed.
- **2026-09-15** — the owed **full** non-author review **RUN** against
  the whole document (Codex CLI `gpt-6-astra`, run by the author,
  `docs/reviews/2026-09-15-codex-full-review-ledger.md`), with one
  targeted diagnostic on a copy of the S-P7 model. The reviewer would
  **not** approve the register as the capstone plan. Six findings, all
  accepted by the owner instance and repaired in place; see "Repairs
  after the 2026-09-15 Codex full review". A **process finding** is
  recorded with them: the owner routed only §5 to the author and had
  not run a full non-author pass first. From this review on, a document
  goes to the author only after a full Codex pass run by the owner and
  a full skeptic read. Still owed: a further non-author pass over
  *this* repaired file, a full skeptic read, and the author's read of
  R-1/R-2/R-3 and of the matrix (BAND0-EXIT E5(a), then E5(c)).
- **2026-09-15, later** — the owed **third** non-author round **RUN**
  against the whole file by the owner instance (Codex CLI
  `gpt-6-astra`, `codex exec`,
  `docs/reviews/2026-09-15-codex-full-review-ledger-round3.md`), with
  paired diagnostics on copies; and the owed **full skeptic read** RUN
  the same day (its log is the last section of this file). The reviewer
  would **not** approve the register as the capstone plan. Six findings,
  all accepted, plus the skeptic's three consequential findings —
  repaired in place; see "Repairs after the 2026-09-15 Codex round 3
  and skeptic read". **The pattern the three rounds expose, recorded as
  the finding it is:** the register kept naming *near-miss* producers —
  committed theorems adjacent to, but strictly narrower than, the
  relation a join's consumer needs (D5, D6, D10). The fourth repair
  stops that: a join with no producer in the tree is recorded as
  *"producer to be registered in the capstone"*, with the exact
  relation stated in the library's terms, and nothing else claimed.
  Still owed: a non-author pass over *this* repaired file, a skeptic
  read of it, and the author's read of R-1/R-2/R-3 and of the matrix
  (BAND0-EXIT E5(a), then E5(c)).
- **2026-09-15, later still** — the owed **fourth** non-author round
  **RUN** against the whole file by the owner instance (Codex CLI
  `gpt-6-astra`, `codex exec`,
  `docs/reviews/2026-09-15-codex-full-review-ledger-round4.md`), with
  six diagnostics on copies. The reviewer would **not** approve the
  register as the capstone plan. **Four findings, all accepted**, and
  all four are defects in the **proposed proof contract** (C-Q1, C-Q8),
  not in the register's entries, its producer–consumer determinations
  or the construction: the reviewer re-checked every matrix row,
  every companion and every count and found the rest consistent. Repaired
  in place; see "Repairs after the 2026-09-15 Codex round 4". **The
  reviewer terminated the review loop:** after this repair the three
  routed forks go to the author, and the contract (C-Q1–C-Q9,
  companions C-C1–C-C10) is re-verified by a non-author pass when the
  capstone's `PREDICTIONS.md` is drafted and before it is frozen, which
  is where a contract defect would otherwise bite. **E18 sign-off is
  separately owed.** Still owed: a skeptic read of *this* repaired file,
  the author's read of R-1/R-2/R-3 and of the matrix (BAND0-EXIT E5(a),
  then E5(c)), and the pre-freeze contract re-verification just named.

---

## Repairs after the 2026-09-14 Codex review

**Source:** `docs/reviews/2026-09-14-codex-review-ledger-and-k6.md`
(OpenAI Codex CLI, `gpt-6-astra`, non-author; run by the author against
the first draft of this file). The reviewer's recommendation was **not
to confirm the ledger as written**; the owner instance accepted every
finding. This file is an unfrozen PROPOSED draft, so the repairs are
made in place and listed here. **No repository file other than this one
was edited, and no repository model was run.** The verification runs
below were made on **copies** in `formal/suite/ledger-tests-2026-09-14/`
(archived from the session scratchpad, `proverif -lib …/lib/tessera_theory.pvl`, ProVerif
2.05); they are unregistered ledger-verification probes — evidence
about the checking arrangement, never about a registered query — and no
family file records them.

| # | Finding | Repair |
|---|---|---|
| 1 | **The S-P2 severing test was wrong.** Removing the frame-fingerprint comparisons from every signer slot leaves `Reattributed` unreachable and honest acceptance reachable; the manifest-hash and manifest-key checks preserve the binding. *"'This check alone suffices' does not imply 'removing this check breaks protection.'"* | L-01's S-P2 determination rewritten; a new **§ L-01 severing evidence — single-removal matrix** added with all seven S-P2 mutants and three S-P7 mutants, showing the two-route structure (frame pin **or** manifest hash + tuple fingerprint match) that is S-P3's F3 applied to S-P2. Companion **C-C2** redefined as the complete relation removal. The entry stays CROSS-MODEL — the complete severing *does* falsify S-P2's query — but the evidence for it is now run, not inferred |
| 2 | **D5: a DSKS transplant under another key does not falsify P1's authorship-under-an-honest-key claim.** *"Removing a signature check and permitting key substitution are different failures."* | D5 and L-06's S-P7 row rewritten: **Q6b is withdrawn as the companion** for D5 (and, by the same reasoning, for D2). The companion that severs the named fact is S-P1's Q3 mutation transcribed into `InnerCheck` (**C-C5**), run in scratch and red on **exactly** `InnerSigTransplanted`. The entry stays CROSS-MODEL on repaired evidence. The same objection applied to D2, which the reviewer did not raise: **C-C4** replaces Q6b there too |
| 3 | **R-2: represent the redundant protection explicitly, and §6 omits the `SetAltered` query C-C3 must falsify.** | R-2's statement now records both routes with the committed isolation evidence (C1 `:366`, C3 `:363`, C2 `:535`). §6 gains **C-Q5** (`SetAltered`) and **C-Q5w** (its honest-flow witness, reachable in the correct model *and* in both isolation configurations), registered whether or not R-2 makes D10 a row. R-2 also now records that the same question decides D1 and D2 |
| 4 | **R-3: *"S-STANDING's fixture contains no wrapper"* is inaccurate** — it declares `wrapCore` and its companion exercises a wrapper-shaped transplant. | L-13's decision row and R-3's statement corrected: the wrapper-shaped term exists and establishes what it establishes (no `ESTABLISHED` over a `wrapCore` core, by `h` injectivity, inside S-STANDING's own algebra); the gap is the **composition** of S-P7's wrapper processing with S-STANDING's standing assessment, which that term does not establish. C-Q6 reworded to name the composed fixture. The fork itself is unchanged |
| 5 | **General: "expected red" asserted without a run.** | The discharge matrix gains an **evidence-state column** with three honest values. Five rows are now shown (D1, D2, D3, D5 in scratch; D10 committed); **six are marked NOT YET SHOWN** (D4, D6, D7, D8, D9, D11) — in every case because the consumer is the capstone and its query does not exist. The counts paragraph is restated against this |

**Scratch runs, 2026-09-14** (all `rc=0`, each ≤ a few seconds; files in
`formal/suite/ledger-tests-2026-09-14/`, archived from the session scratchpad as review inputs, not suite models):

| File | Mutation of | Result |
|---|---|---|
| `base_sp2.out` | — | `Reattributed` unreachable `:397`; `HonestAccepted` reachable `:1007` |
| `m1_framepin.out` | S-P2 frame pin | `Reattributed` **still unreachable** `:399` |
| `m2_mh.out` | S-P2 manifest hash | **still unreachable** `:394` |
| `m3_tuplefp.out` | S-P2 tuple fp match | **still unreachable** `:645`; `SignerForged` red `:619` |
| `m4_framepin_mh.out` | pin + manifest hash | **`Reattributed` reachable** `:620`, red on exactly it; witnesses `:791`, `:1015`, `:1250` |
| `m5_framepin_tuplefp.out` | pin + tuple fp | reachable `:870`; `SignerForged` also red |
| `m6_mh_tuplefp.out` | mh + tuple fp | **still unreachable** `:649` |
| `m7_all_three.out` | complete relation | reachable `:860`; `SignerForged` also red `:625` |
| `base_sp7.out` | — | all four unreachability queries green `:527`–`:566`; witnesses `:865`, `:1061` |
| `s1_sig_unbound.out` | inner signature unbound (C-C5) | **`InnerSigTransplanted` reachable** `:897`, red on exactly it; witnesses `:1233`, `:1442` |
| `s2_sig_removed.out` | inner signature check removed (a11 shape) | `InnerSigTransplanted` reachable `:852` — reaches the same query by severing an S-P7 check, not S-P1's fact |
| `s3_innerfp.out` | inner `=fp(kI)` pin | **every query still green** `:527`–`:566` |
| `s4_innerfp_mh.out` | inner pin + `mhI` (C-C4) | `Rescoped` `:864`, `InnerSigTransplanted` `:1207`, `Reattributed` `:1431` red; `TypeConfused` `:526`, `VersionLied` `:1949` green |
| `s5_innerfp_mh_tfp.out` | all three, inner | same polarity `:869`, `:1216`, `:1444` |
| `base_sp1q1.out` | — | Q1(i) `is true` `:201` |
| `s6_bothchannels.out` | both channel keys public (C-C1) | **Q1(i) `is false`** `:361`; honest-key correspondence green `:368`; `HonestAccepted` reachable `:559` — the family's registered-but-unrun prediction, observed on a copy; S-P1's record is unchanged and still reads *"Not run"* |

**What this review did not settle.** The reviewer endorses the
*principle* that transcription alone does not settle R-1, and endorses
the intended R-2 and R-3 work; the three routed forks are unchanged in
existence and sharpened in statement. This is not a confirmation of the
register, and it is not an E18 sign-off (the reviewer says so in terms).
A further non-author review of the repaired file is owed before the
capstone plan freezes.

---

## Repairs after the 2026-09-15 Codex full review

**Source:** `docs/reviews/2026-09-15-codex-full-review-ledger.md`
(OpenAI Codex CLI, `gpt-6-astra`, non-author; run by the author against
the whole of the 2026-09-14 repaired draft). The reviewer would not yet
approve the register as the capstone plan; the owner instance accepted
all six findings. This file is an unfrozen PROPOSED draft, so the
repairs are made in place and listed here. **No repository file other
than this one and the ledger-tests README was edited, and no repository
model was run.** The verification runs below were made on **copies** in
`formal/suite/ledger-tests-2026-09-14/`
(`proverif -lib formal/suite/lib/tessera_theory.pvl`, ProVerif 2.05,
each `rc=0`); they are unregistered ledger-verification probes —
evidence about the checking arrangement, never about a registered query
— and no family file records them.

### Edits by finding

| # | Finding | Repair |
|---|---|---|
| **1** | **D5 names an insufficient producer fact.** S-P1's honest-key authorship theorem is narrower than what S-P7's `InnerSigTransplanted` consumes; the reviewer's mutation kept authorship green and made the transplant reachable. | L-06 gains a field naming **the exact relation the consumer requires** in the library's terms: `checksign(sg, kX) = (BYTES, fb)` over the **presented** bytes, and `fb`'s fourth field `= fp(kX)`, so no other key's signature is accepted over those bytes — equivalently, no honest signer's **signature term** is carried into an acceptance reported under another key. **Producer search, answered:** no committed query of S-P1 or S-P3 (or S-P2 or S-STANDING) ranges over the signature term, and the mutation `d5b` shows S-P1's Q2(i) *and* S-P3's `Reattributed` both green while the consumer goes red. So **D5 is marked provisional, "producer to be registered in the capstone"**, and the query the capstone must add is stated and feasibility-checked as **C-Q7** (§6). **D6 goes provisional with it** — the §A3.2 chain's last link is that same relation, and the draft's "as D5 — exists, green" producer cell was false. *[Superseded in part, round 3: the last link is **not** the same relation as D5's, and C-Q7 is **not** D6's producer. D6's producer is **C-Q8**. See "Repairs after the 2026-09-15 Codex round 3 and skeptic read", finding 1.]* **C-C5 is retagged** as evidence that byte binding matters, not as the discharge; **C-C6** is added as C-Q7's companion. **D5 is removed from R-1's supporting argument.** |
| **2** | **L-07's global key-use whitelist contradicts S-STANDING's `sign((TLR, body), skI)`.** | The whitelist is replaced by **the enumeration of legitimate signing domains from the library's tags** — `STMT_DIRECT`, `STMT_DIGEST`, `POSS`, `BYTES`, `TLR`, `REFUSAL` — each with its message shape, its signing key and the family that signs it, with `STMT_DIRECT` and `REFUSAL` recorded as **declared and unexercised**. **Domain separation across these six tags** is named as the composed property the capstone must preserve (inert per family, load-bearing under composition, library D-6 note). Key-use discipline stays LAYER-2 **only for endpoints outside the modelled ones**. Counted mechanically: `BYTES` 201, `POSS` 170, `STMT_DIGEST` 140, `TLR` 30 occurrences of `sign((TAG, …))` across the committed suite models, and no other form. |
| **3** | **L-09 promises common content without naming the query that establishes it.** | L-09 gains a second producer row: **S-P2 Q6, `Spliced` unreachable** (`sp2_q2_degraded_compromised.out:1013`, green as registered 2026-09-12, `s-p2/RESULTS.md:671`), with its **shared-term mapping**: the six non-fingerprint `framed` fields equal across slots — `alg`, `issuerId`, `manifestHash` pinned through the shared tuple by the pre-existing per-slot checks, and `objType`, `canonVer`, `payload` equated by the §A5.4 guards; `kfp` deliberately **not** equal (that is L-01). **Authorship stays in L-06.** D7's producer cell carries all three queries. |
| **4** | **Ruling consequences not propagated.** | **D1 and D2 are moved to provisional on R-2** (they have the same two-route shape as D10), and every count is restated in a table. **R-3 now writes both outcomes** for L-16/L-17: formulation **W** (conclusion is a standing verdict) consumes them and adds rows **D12**/**D13**, whose producers and companions already exist and are the right colour; formulation **N** (conclusion stops at the attributed identity) leaves them COMPLEMENTARY and adds D11 only. L-16 and L-17 carry the routing in their Kind and Decision fields. **R-1 no longer cites D5.** §2 (matrix + counts), §3 (Layer 2), §5 (routed) and §6 (capstone contents) were re-read against each other afterwards. *The instruction for this repair referred to "§7"; this document has six numbered sections, so the consistency pass covered §§2, 3, 5 and 6 and the two appendices.* |
| **5** | **§6's companion instructions contradict their evidence.** | "Red on exactly its named query" is **withdrawn**. Each companion is now specified by three sets — expected failed-query set, guarantees that must stay green, witnesses that must stay reachable — every one verified against a `.out` and cited by line. **C-C2 becomes the minimal two-removal mutation** (frame pin + manifest hash); the three-removal alternative is withdrawn because `m7_all_three.out:625` reds `SignerForged`, which set (2) requires green. **C-C4 is documented as failing three queries by design.** C-C3 gains its two isolation configurations and a note that `Spliced` is absent from the ladder models and must be added on transcription. |
| **6** | **"Layer 2 forever" includes internal obligations.** | The kinds table splits **LAYER-2(a)** (permanent external: primitive security, historical trust-anchor correctness, chain availability, implementation fidelity, operational channel independence) from **LAYER-2(b)** (internal proof obligations carried as assumptions), and §3 splits into two tables. **3(b)** holds L2-d, L2-i, L2-j (canonical encoding pre-P8 → **BAND0-EXIT E3**, the P8 framing proof) and the new **L2-n** (the §A3.7.2 extended atomic-entry invariant → **E6**), each citing the item that discharges it. **"Forever" is removed from (b)** and stated to apply only to (a). L2-b's canonical-encoding half is moved to L2-d; L2-g is narrowed per finding 2. |

### Hostile re-read of the whole document (2026-09-15)

Every row asserting an expected red, a producer fact, a shared term or
a count was checked against a `.out`. Eight defects found and fixed
beyond the six findings:

| Where | Defect | Fix |
|---|---|---|
| L-09, D7 | `Stripped`/`SignerForged` cited at `sp2_q2_degraded_compromised.out:354, 360` | **Pre-addendum line numbers.** The 2026-09-12 §A5.4 addendum shifted every RESULT line in that `.out`; corrected to `:378, :384` (the family file's own current numbers, `s-p2/RESULTS.md:671`) |
| L-10 | `SetAltered` cited at `.out:366` | Same cause; corrected to `:390` |
| L-12, D8 | `TypeConfused` unreachable cited at `sp7_q2…out:505` | `:505` is not a RESULT line; corrected to `:527` |
| L-13 | `Rescoped` / `InnerSigTransplanted` cited at `sp7_q2…out:518, 531` | Neither is a RESULT line; corrected to `:540` and `:553` |
| L-12 | Q3's red cited as "`.out` 509, 727", reading as two RESULT lines | `:509` is the *goal-reachable* line and `:727` the RESULT; stated as such |
| §2 counts | "Red on *exactly* the consumer's query: D1, D3, D5" | **Omitted D10**, which is red on `SetAltered` alone (`sp2_q5_c2_fponly_frame_nomh.out:535`, others true at `:349, :356, :542`, witnesses `:706, :925, :1100`). Count is 4 |
| §2 counts | "Producer query exists and is green: 11 of 11" | False for D5 and D6 once the producer fact was named exactly; **9 of 11** |
| Two citations that *look* wrong and are not | `sp1_q2_*.out:354` (L-04's expected-failing-query cell) and `.out 354-520` (D7's Q3 companion) are neither RESULT lines | **Checked: both are correct as quoted.** They are **trace** lines/spans, and both are the family files' own wording (`s-p1/RESULTS.md:376`, `s-p2/RESULTS.md:45`). D7's cell now says so and adds the RESULT lines `:520` / `:601` |
| L-01, L-02, L-13, L-16, L-17 | Producers and companions named by **model**, with no RESULT line | Every one now carries its `.out` line, verified this session: `sp3_q2:195, :200, :376`; `sp3_q3:359, :532`; `sp3_q4:383, :195, :559`; `sp7_q6a:806, :503, :819`; `sp7_q6b:769, :1058`; `sp7_q5c:1131, :690`; `ss_q1:503, :513, :523, :530, :829`; `ss_q2:630, :808, :986`; `ss_q3:860, :628, :642, :656`; `ss_q4:576, :849, :1123` |

**Rows still marked NOT YET SHOWN, unchanged and honest:** D4, D6, D7,
D8, D9, D11 — in every case the consumer is the capstone and its query
does not exist. **Rows newly marked provisional:** D1, D2 (R-2), D5, D6
(producer). **Not asserted anywhere in this file:** that any join is
discharged, that C-Q7 exists, that D12/D13 exist, or that the `REFUSAL`
domain is checked.

### Scratch runs, 2026-09-15

New files in `formal/suite/ledger-tests-2026-09-14/`, each a copy of a
committed model with a header comment naming the model it copies and
the mutation it makes. All `rc=0`, each a few seconds.

| File | Copy of | Mutation / addition | Result (`.out` line) |
|---|---|---|---|
| `d5a_sp1_condunbind.pv/.out` | `s-p1/proverif/sp1_q2_degraded_compromised.pv` | `let (=BYTES, =fb) = checksign(sg, kX)` → **conditional** binding: presented bytes must equal signed bytes only when the signed frame's `kfp` matches the verifying key | **S-P1 Q2(i) `AcceptedUnderHonestKey ⟹ IssuerSigned` still `is true`** (`:195`); `HonestAccepted` reachable (`:371`); Q2(ii) `is false` as registered (`:521`). *The producer's own query survives the mutation that severs the relation D5 names* |
| `d5b_sp7_condunbind.pv/.out` | `s-p7/proverif/sp7_q2_degraded_compromised.pv` | the same conditional binding inside `InnerCheck`, **plus** S-P1's honest-key authorship judge and query transcribed in, so producer facts and consumer query are observed in one model | **authorship `is true` (`:654`)**, **`Reattributed` `is true` (`:1060`)**, **`InnerSigTransplanted` `is false` (`:1037`)**; `TypeConfused` (`:677`), `Rescoped` (`:700`), `VersionLied` (`:1599`) true; witnesses reachable (`:1370`, `:1576`). *Reproduces the reviewer's diagnostic and extends it: S-P3's fact holds too* |
| `d5c_sp1_sigjudge.pv/.out` | `sp1_q2_degraded_compromised.pv`, verifier and every registered query **unmutated** | **adds** the signature-**term** judge and the query `SigTransplanted(kX, sg)` — the C-Q7 shape | **`SigTransplanted` unreachable, `is true` (`:203`)**; Q2(i) `is true` (`:210`); witness reachable (`:386`). *C-Q7 is feasible on S-P1's existing fixture* |
| `d5d_sp1_sigjudge_condunbind.pv/.out` | `d5c_sp1_sigjudge.pv` | the same conditional unbinding | **`SigTransplanted` reachable, `is false` (`:414`)** while **Q2(i) stays `is true` (`:422`)**; witness reachable (`:599`). *C-Q7 does establish the relation; Q2(i) does not* |

Together the four runs are the finding-1 argument in full: the relation
S-P7 consumes is falsifiable (`d5b`, `d5d`), the committed producer
queries do not range over it (`d5a`, `d5b`), and a query that does is
green on the committed verifier (`d5c`). **No new claim is made about
any registered query, and no family file records these runs.**

**What this review did not settle.** The reviewer's recommendations on
R-1, R-2 and R-3 coincide with the owner's and are recorded in §5; the
three forks remain the author's. This is not a confirmation of the
register. A further non-author pass over the repaired file, a full
skeptic read, and the author's read are all still owed before the
capstone plan freezes.

---

## Skeptic log (2026-09-15)

Full adversarial read of every register entry L-01…L-26, every matrix
row D1–D11, every companion C-C1…C-C6, every capstone query
C-Q1…C-Q7/C-N1 and every count *(the register's state at the time of
this read; the fourth repair later added C-Q8, C-Q9, C-C7, C-C8, D12
and D13)*. Method: each cited `.out` line, `.pv`
line and `RESULTS.md`/amendment/spec line range was opened and compared
with the sentence that cites it; every "green", "red", "unreachable",
"reachable" and "shared term" claim was resolved to a `RESULT` line
(the full `RESULT` set of each cited `.out` was read, not just the
cited line, so that "red on exactly X" could be falsified if false).
**No model was run this session** — every claim in the file resolved to
an existing committed or ledger-tests `.out`, so no new run was needed
and none was made. No repository file other than this one was edited.
Edits are in place and minimal; the three routed forks are untouched.

| # | Entry / row | Change | Why | Checked against |
|---|---|---|---|---|
| 1 | §"The gate this file serves" | A3 §A3.3 verbatim re-cited `:220-230`; conservation fields `:232-238` | `:216-229` names the paragraph above the blockquote | `docs/phase-0-prereg-amendment-3.md:214-238` |
| 2 | L-01, S-P1 consumer row | `implementation-spec.md:1522-1531` → `:1525-1533` | the key-binding ruling note begins at `:1525`; `:1522` is the verifier/adjudicator row | `docs/implementation-spec.md:1518-1533` |
| 3 | L-01, S-P2 consumer row; D1 | carried-judge citation `sp2_q2…pv:229-233` → `:268-273` (query `:143-144`) | pre-addendum position carried from the family file; after §A5.4 those lines are the content guards and `Accept2S` outputs | `s-p2/proverif/sp2_q2_degraded_compromised.pv:228-235, :143-144, :268-273` |
| 4 | L-01, S-P2 and S-P7 consumer rows | **A7 §A7.10 applied by the skeptic**: recorded that `m4`/`s4` sever the *consumer's own transcribed* checks, not the producer, and that severing the producer leaves both consumer queries green | the rule's antecedent is "severing the producer falsifies the consumer's query"; the cited evidence does not establish it | `base_sp2.out:397`; `base_sp7.out:540`; `m4_framepin_mh.out:620`; `s4_innerfp_mh.out:864` |
| 5 | L-02, S-P7 consumer row | source `s-p7:576-578` → `:573-574` | the `a08` sentence is at `:573-574` | `s-p7/RESULTS.md:569-578` |
| 6 | L-04 | assumed-fact quote `s-p1:349-351` → `:347-349`; spike quote `first-link:88-91` → `:87-89` | both ranges started one line past the quote | `s-p1/RESULTS.md:345-352`; `first-link/RESULTS.md:86-92` |
| 7 | L-06, assumed-fact row and capstone consumer row | consumer-half quote `s-p1:413-414` / `:411-414` → `:409-410` | `:413-414` is the severing-companion sentence, not the chain link | `s-p1/RESULTS.md:404-415` |
| 8 | L-06, S-P7 consumer row | `s-p7:43-48` dropped; the quoted sentence located at `:580-582` | `:43-48` is the predictions-vs-observed table and supports nothing in the row | `s-p7/RESULTS.md:43-48, :578-590` |
| 9 | L-06, S-P2 consumer row | `s-p2:326-328` → `:331-332` | the "Authorship … S-P1" declination is at `:331-332` | `s-p2/RESULTS.md:317-333` |
| 10 | L-07, signing-domain enumeration | `[UNSUPPORTED]` marker on the four `sign((TAG,…))` counts and on "no other form anywhere" | no stated or reconstructible scope yields 201/170/140/30; the tree gives 2009/1733/1629/248, the 43 top-level models 97/80/71/16; and `sign((REFUSAL,…))` does occur | recount over `formal/suite/{s-p1,s-p2,s-p3,s-p7,s-standing,lib}/**/*.pv` (916 files) and over `*/proverif/*.pv` (43) |
| 11 | L-07, `REFUSAL` row; §6 "must not do" list | "unexercised anywhere in the suite" narrowed to "in every committed model", with the two scratch occurrences named | the reviewer's foreign-tag fixtures sign a `REFUSAL` body — the same fixtures this entry cites two paragraphs above | `s-standing/proverif/falsification-2026-09-06/scratch/a_foreign_tag.pv:342`; `…/m_foreign_tlr_tag.pv:342` |
| 12 | L-09 | sources `s-p1:485` → `:489`, `s-p7:597-598` → `:626-631` | `s-p1:485` is the replay sentence; `s-p7:597-598` is the opacity bullet, not the package-completeness cell | `s-p1/RESULTS.md:483-489`; `s-p7/RESULTS.md:596-631` |
| 13 | L-12 | a10 given its RESULT line and full polarity | the row claimed "red" with no result cited | `s-p7/proverif/ablations/a10_no_wrapper_type.out:723, :738, :753, :768, :1072, :1270` |
| 14 | L-13, decision row | `s-standing:1338-1352` → `:1335-1348`; the three `wrap_routes` polarities stated; **consistency note added** on D11 vs D12/D13 and on S-STANDING's companion-only `EstablishedWrapped` query | the entry is COMPLEMENTARY today yet already holds a row in a table declared "CROSS-MODEL entries only", while L-16/L-17 — routed on the same question — hold none | `s-standing/RESULTS.md:1335-1348`; `…/scratch/wrap_routes.out:1827, :1944, :1951`; `ss_q2_companionA_identity_declared.out:1176, :2685`; `ss_q2…pv` (sole file declaring `EstablishedWrapped`) |
| 15 | L-16 | abl6's three RESULT lines, its retained guarantee and its witness added | the companion was asserted red with no result cited | `s-standing/proverif/ablations/abl6_no_tlr_signature.out:616, :788, :960, :966, :1297` |
| 16 | L-17 | repo-variant and Q1d producer lines added | "both variants and Q1d" cited one `.out` line | `ss_q1_strict_repo_compromised.out:530`; `ss_q1d_degraded_compromised.out:664` |
| 17 | L-18 | the registered cost given its RESULT lines | a registered red with no cited result | `ss_q1d_degraded_compromised.out:640, :649, :658, :664, :950` |
| 18 | L-19 | assumed-fact quote `s-standing:500-503` → `:498-499` | the quoted sentence is at `:498-499` | `s-standing/RESULTS.md:495-507` |
| 19 | L-22 | finding quote `first-link:66-70` → `:70-72` | the quoted ledger consequence is at `:70-72` | `formal/spike/first-link/RESULTS.md:63-72` |
| 20 | L-23, D9 | producer and companion given committed RESULT lines for both variants and all four Q6 runs | §2's rule requires a committed `.out` behind every green/red; these two cells named models only | `q4_attack_{dns,repo}_compromised.out:97`; `q2_broken_{dns,repo}_compromised.out:243, :464`; `q6_single_dns_{honest:91,compromised:93}.out`; `q6r_single_repo_{honest:91,compromised:93}.out` |
| 21 | D1, companion cell | the withdrawn "or all three removals" alternative removed | §6's C-C2 withdrew it under finding 5 (`m7` reds `SignerForged`, which this row requires green); §2 still offered it | `m7_all_three.out:625`; §6 C-C2 |
| 22 | §5, R-1 | recorded that the remaining argument is **circular** | with D5 withdrawn, Reading B rests on D1/D2, whose CROSS-MODEL status Reading B decides; the one non-circular item is S-P7's own consumption sentence | `s-p7:580-582`; `base_sp2.out:397`; `base_sp7.out:540` |
| 23 | §6, C-C6 | set (1) annotated: `AcceptS ⟹ IssuerSigned` is red in the mutant **and** in the unmutated producer | so the three-set specification is not read as exhaustive of the `.out` | `d5a:521`, `d5c:536`, `d5d:750`; `sp1_q2_degraded_compromised.out:499` |

**Checked and found correct — no edit made.** Every ledger-tests
citation (`base_sp1q1`, `base_sp2`, `base_sp7`, `m1`–`m7`, `s1`–`s6`,
`d5a`–`d5d`): all 60-odd cited line numbers and polarities are exact,
and the full `RESULT` set of each file agrees with the "red on exactly"
and "stays green" claims made of it. Every committed-model citation in
L-01, L-02, L-09, L-10, L-12, L-13, L-16, L-17, D3, D7, D8, D10 and
§6's C-C1…C-C5 is exact. The §2 counts table is internally consistent
and agrees with the matrix cell by cell (11 rows; 5 firm + 3 R-2 + 2
producer + 1 R-3; producer green 9 of 11; red-on-exactly 4 — D1, D3,
D5, D10, each verified; NOT YET SHOWN 6). §3(a)/(b) exhaust
L2-a…L2-n with no item in both, and every (b) row names its exit item
(E3, E6), whose text matches `formal/BAND0-EXIT.md:63, :66`. §4's six
TLA+ invariant names all exist in their named modules. The A7 §A7.10
blockquote is verbatim from `docs/phase-0-prereg-amendment-7.md:242-246`
and is the author's own words; the two Codex reviews are quoted
accurately and labelled as non-author readings; nothing is marked
ADOPTED or RULED beyond what the record carries.

> **[Superseded by the round-3 repair, 2026-09-15.]** The counts
> verified two sentences above — 11 matrix rows, 5 firm + 3 R-2 + 2
> producer + 1 R-3, producer green 9 of 11, red-on-exactly 4, NOT YET
> SHOWN 6 — were correct against the file **as this skeptic read found
> it**, and are left as written per amend-don't-rewrite. They are
> **not** the file's current counts. The fourth repair, made the same
> day after the third Codex round, splits §2 into 2(a)/2(b)/2(c), holds
> D1 and D2 out under R-1 as written, and withdraws D10's producer: the
> matrix is now **8 rows**, firm **5**, provisional-on-producer **3**,
> provisional-on-R-2 **1**, producer green **5 of 8**, red-on-exactly
> **3**, NOT YET SHOWN **5**, held out by R-1 **2**, conditional on R-3
> **3**. See §2's counts table and §5's "Combined consequences".

**NOT YET SHOWN / unclaimed, confirmed as honest.** D4, D6, D7, D8, D9,
D11 — in each case the consumer is the capstone and its query does not
exist. D5/D6's producer (C-Q7) does not exist. No new NOT YET SHOWN
marker was needed: every remaining colour claim in the file resolved to
a real `RESULT` line.

**One item outside this file, for the owner.** `formal/BAND0-EXIT.md`
E5's description of this register is now stale — it reads "the
capstone's minimum query list C-Q1–C-Q4", while §6 now registers
C-Q1–C-Q4, **C-Q5, C-Q5w, C-Q6, C-Q7** and C-N1, and its kind tallies
("7 cross-model determinations, 11 complementary, 5 Layer 2, 3
cross-formalism") predate the 2026-09-15 repairs. Not edited here; the
skeptic's scope is this file.

---

## Repairs after the 2026-09-15 Codex round 3 and skeptic read

**Sources:** `docs/reviews/2026-09-15-codex-full-review-ledger-round3.md`
(OpenAI Codex CLI, `gpt-6-astra`, non-author; run non-interactively by
the owner instance against the whole file after the third repair and
the 2026-09-15 skeptic read; six findings, all accepted) and the
**Skeptic log (2026-09-15)** at the end of this file, whose three
consequential findings — R-1's remaining argument circular, A7 §A7.10's
antecedent not established for D1/D2, and the D11 convention — are
repaired here together with the review's. The reviewer would not
approve the register as the capstone plan.

This file is an unfrozen PROPOSED draft, so the repairs are made in
place and listed below. **No repository file other than this one and
the ledger-tests README was edited, and no repository model was run.**
The four verification runs were made on **copies** in
`formal/suite/ledger-tests-2026-09-14/`
(`proverif -lib formal/suite/lib/tessera_theory.pvl`, ProVerif 2.05,
each `rc=0`, each a few seconds); they are unregistered
ledger-verification probes — evidence about the checking arrangement,
never about a registered query — and no family file records them.

**The finding behind the findings.** Three rounds and a skeptic read
all landed on the same shape: a join whose consumer needs relation *X*
was given a producer that establishes a strictly narrower relation *Y*,
where *Y* is adjacent enough to read as *X* on a fast pass. D5 (Q2(i)
for the signature term), D6 (C-Q7 for the presented bytes) and D10
(`PossessionTransplanted` for the accepted manifest) are three
instances. **The rule this repair adopts:** a join with **no producer
in the tree** is recorded as *"producer to be registered in the
capstone"*, with the exact relation the consumer needs stated in the
library's terms, and **nothing else is claimed** — no near-miss
theorem is named, no adjacent query is offered as a substitute.

### Edits by finding

| # | Finding | Repair |
|---|---|---|
| **1** | **C-Q7 does not establish D6's exact signature/bytes relation.** Binding a signature to the presented bytes and preventing an honest signature term's acceptance under another key are different properties; C-Q7 observes `(acceptedKey, signature)` only and cannot see different bytes under the **same** key. | L-06's single "relation the consumer requires" row is **split into two**: **R-bytes** (D6 — *a signature accepted over presented bytes `fb` under key `kX` was produced by `kX`'s holder over exactly `fb`*, i.e. `checksign(sg, kX) = (BYTES, fb)` over the **presented** `fb`) and **R-key** (D5's transplant scope). The draft called them *equivalent*; they are not, and the row now says so. **C-Q7 is scoped to D5 only**, with the same-key blindness stated explicitly and shown on a copy (`d6b:246` green while authorship `:593` is red). **D6's producer is "to be registered in the capstone"** — the D6 row in §2(a), L-06's capstone consumer row and the §6 "must not do" list all now say C-Q7 is *not* it. The query that would establish R-bytes is specified as **C-Q8** with its event signature `SigBytesUnbound(pkey, bitstring, bitstring)` — *(accepting key, signature term, presented framed bytes)* — its fixture wiring, its honest witness (`HonestAccepted` reachable), and its companion **C-C7**. Feasibility checked on copies: `d6a:250` green on the committed verifier, `d6b:427` red under the same-key unbinding that leaves C-Q7 green. |
| **2** | **D10's named producer, `PossessionTransplanted`, does not establish possession over the accepted manifest.** S-P3's judge compares the proof term's original and accepted **keys**; neither its report nor its test contains the accepted manifest. | L-02's producer row is **scoped** with the judge's actual text (`sp3_q2_degraded_compromised.pv:137-141`) and the sentence *"neither the event nor the query mentions the accepted manifest"*. Three rows added: the relation S-P2's consumer requires (`checksign(ppf, kX) = (POSS, t)` for the same `t` the verifier accepted), the finding that **no committed query establishes it**, and the query the capstone must add, **C-Q9**, with event signature `PossessionUnbound(pkey, bitstring, bitstring)` — *(accepting key, accepted manifest, accepted possession proof)* — its wiring at every acceptance point, its honest witnesses, and its companion **C-C8**. D10's producer cell in §2(a) now reads **NOT YET REGISTERED**. **Independent of R-2**, and said so in three places: R-2 decides whether D10 is a row, C-Q9 decides whether it has a producer. Shown on copies: `d10b:1297` `PossessionTransplanted` green while `:673` `SetAltered` red and `:1462` C-Q9 red. |
| **3** | **Companion failed-query sets are family-local, presented as exhaustive for the capstone.** | §6's rule *"A red outside this set is a broken fixture, not a severing"* is **withdrawn**. In its place: each set is valid **as specified today, against the cited `.out`, for the family-local run it names**; each **MUST be re-specified against the capstone's own query names once C-Q1…C-Q9 exist**, before predictions freeze, as a registered step; and until then a red outside a listed set is an **unresolved observation**, investigated and recorded, never silently classified. Every companion row now carries the tag *"Family-local; re-specified against the capstone's query names once …"*. **C-C1's expected set gains D4's linkage failure explicitly**: it is now two queries — (a) `Accept ⟹ IssuerSigned`, shown red family-locally, and (b) **C-Q1's `ChainBroken` at link 1, reachable**, marked NOT YET SHOWN because `ChainBroken` is declared in no model. The register does **not** identify (b) with (a). |
| **4** | **C-Q1 is not builder-ready; required retained queries are unlisted.** | C-Q1 is rewritten as a **query contract** (§6, new subsection): **(1)** event signatures — `AuthorityEvidence`, `LayerAccepted` (layer, tuple, signer slot, accepting key, possession proof, signature term, presented frame), `ChainBroken`, `HonestChain` — in the library's terms; **(2)** the correspondence as **six named per-layer links**, each stated over those terms with its producer today, which makes visible that **links 3 and 4 have no producer** (C-Q9, C-Q8) and that C-Q1 cannot discharge D4/D6/D7/D8 until they exist; **(3)** the **strict/degraded contract** — link 1 needs an honest authority channel and is dropped in the degraded form; links 2–6 are structural binding requirements that hold in both modes; the unrestricted form is the registered A4.6 red and C-Q1 must not assert it; the two forms are separate registered queries, **C-Q1-strict** and **C-Q1-degraded**; **(4)** the fixture — keys, channels, wrapper, `dsks`, and four named compromise cases; **(5)** the expected outcome — `ChainBroken` unreachable, `HonestChain` reachable at every layer of every case. A second new subsection lists the **REQUIRED retained queries** the companions must falsify or preserve: `Accept ⟹ IssuerSigned` (D3's own), `AcceptedUnderHonestKey ⟹ IssuerSigned`, `Stripped`, `SignerForged`, `Spliced`, `TypeConfused`, `VersionLied`, `Rescoped`, and C-Q5 `SetAltered`. **Nothing was renumbered; C-Q8 and C-Q9 were added.** |
| **5** | **R-1's consequences contradict each other; D1/D2's conditions on R-1 and R-2 are stated inconsistently; the D11 vs L-16/L-17 convention is annotated, not repaired.** (With the skeptic's findings of the same day.) | **R-1 is restated in its honest form:** under A7 §A7.10 as written, **D1 and D2 are COMPLEMENTARY today**, because each consumer transcribes the check and its own query survives severing the producer (`base_sp2.out:397`, `base_sp7.out:540`); they become capstone-internal joins **only if** the capstone's fixture composes the families' checks into one verifier — the capstone's design choice, ENUM §3 — in which case `m4` and `s4` are the capstone's own companions (C-C2, C-C4). The register's **default reading is Reading A**, stated as such in §2's preamble, and **the author decides**. **Every sentence using D5 as R-1 evidence is removed**, and so is *"Under Reading A the matrix loses D1, D2 and D5"*; the one retained sentence about D5 says R-1 does **not** change it. The one non-circular item — S-P7's own *"the check's security is consumed from S-P1"* (`s-p7:580-582`) — is put to the author as a statement, not a run. **R-2** is a joint entry with its combined-removal companion; **D10's producer defect is independent of R-2 and stays**. **R-3** keeps formulations W and N, with W consuming L-16/L-17. **One table, "Combined consequences",** now gives the **eight** R-1 × R-2 × R-3 outcomes as rows with every matrix row's status under each. **§2 is split three ways** — 2(a) the matrix, 2(b) held out by R-1, 2(c) conditional on R-3 — and **L-13, L-16 and L-17 move together into 2(c)** as D11, D12, D13, which retires the two-conventions defect. **Every count in the file is restated for the default reading** and agrees with the table. |
| **6** | **E18: the "exactly" qualification at `RESULTS-K6.md:47` conflicts with the summary at `:53`.** | **Outside this file's scope and not edited here.** `formal/tla/k6-2026-09-14/` is not this register; the ledger's E18 position is unchanged and still withholds sign-off. Recorded so the disposition is not lost. |

### Edits from the skeptic log, applied in the same pass

| Skeptic finding | Where it landed |
|---|---|
| **R-1's remaining argument is circular** (with D5 withdrawn, Reading B rested on D1/D2, whose classification Reading B decides) | §5, R-1: the rows are no longer offered as corroboration, the circularity is stated, and the only non-circular item is named as a family's statement about itself |
| **A7 §A7.10's antecedent is not established for D1/D2** — severing the producer leaves the consumer green (`base_sp2.out:397`, `base_sp7.out:540`) | L-01's S-P2 and S-P7 consumer rows are re-decided **COMPLEMENTARY today**; D1 and D2 move to §2(b); the matrix drops from 11 rows to 8 |
| **The D11 convention** — a complementary entry inside a table declared "CROSS-MODEL entries only", while equally conditional L-16/L-17 sat outside it | §2(c) created; D11, D12, D13 written out there in full; L-13's consistency note marked **REPAIRED** with the repair described |

### Scratch runs, 2026-09-15 (round 3)

Four new files in `formal/suite/ledger-tests-2026-09-14/`, each a copy
of a committed model (or of an earlier scratch copy) with a header
naming what it copies and what it mutates. All `rc=0`.

| File | Copy of | Mutation / addition | Result (`.out` line) |
|---|---|---|---|
| `d6a_sp1_q8_base.pv/.out` | `ledger-tests-2026-09-14/d5c_sp1_sigjudge.pv` (itself an unmutated copy of `s-p1/proverif/sp1_q2_degraded_compromised.pv` plus the C-Q7 judge) | **adds** the C-Q8 three-place judge: `event SigBytesUnbound(pkey, bitstring, bitstring)` over *(accepting key, signature term, presented framed bytes)*; verifier and every registered query unmutated | **C-Q7 `SigTransplanted` `is true` (`:244`)**, **C-Q8 `SigBytesUnbound` `is true` (`:250`)**, Q2(i) `is true` (`:258`), witness reachable (`:435`), Q2(ii) `is false` (`:586`) as registered. *Both candidate producers are green on the committed verifier* |
| `d6b_sp1_q8_samekey_unbound.pv/.out` | `d6a_sp1_q8_base.pv` | **same-key byte unbinding**: `let (=BYTES, =fb) = checksign(sg, kX)` becomes `let (=BYTES, fbS: bitstring) = checksign(sg, kX) in let framed(otS, algS, idS, =fp(kX), mhS, cvS, plS) = fbS in` — the signature must verify under `kX` over *some* frame naming `fp(kX)`, not over the presented bytes. Every other check retained | **C-Q7 stays `is true` (`:246`)** while **C-Q8 `is false` (`:427`)** and **Q2(i) `is false` (`:593`)**; witness reachable (`:773`). *The reviewer's finding-1 diagnostic, reproduced: C-Q7 is blind to this, C-Q8 is not. **This is the whole of the D6 argument**: the relation is falsifiable, C-Q7 does not range over it, and C-Q8 does* |
| `d10a_sp2_q9_base.pv/.out` | `s-p2/proverif/sp2_q2_degraded_compromised.pv`, verifier and every registered query **unmutated** | **adds** two judges: S-P3's `PossJudge` shape (`PossessionTransplanted`, keys only) and the C-Q9 judge `event PossessionUnbound(pkey, bitstring, bitstring)` over *(accepting key, accepted manifest, accepted possession proof)*, fed from every acceptance point | all five S-P2 safety queries `is true` (`:457, :464, :471, :478, :1097`), **`PossessionTransplanted` `is true` (`:1104`)**, **C-Q9 `is true` (`:1111`)**, both `HonestComplete` reachable (`:643`, `:861`), `HonestAccepted` reachable (`:1090`). *Both candidate producers green on the committed verifier* |
| `d10b_sp2_q9_manifest_unbound.pv/.out` | `d10a_sp2_q9_base.pv` | **both manifest-binding protections removed together**: possession made fingerprint-only (honest signer emits `sign((POSS, fp(pk(sk))), sk)`; each slot checks `let (=POSS, =fp(kX)) = checksign(ppfX, kX)`) **and** the frames' `mh = h(t)` guards dropped. Seven-field frames, per-slot `=fp(kX)` pins, tuple fingerprint matches and the three §A5.4 content guards all retained | **`PossessionTransplanted` stays `is true` (`:1297`)** while **`SetAltered` `is false` (`:673`)** and **C-Q9 `is false` (`:1462`)**; `Stripped` (`:454`), `SignerForged` (`:464`), `Reattributed` (`:683`), `Spliced` (`:1287`) still true; both `HonestComplete` (`:851`, `:1072`) and `HonestAccepted` (`:1277`) reachable. *The reviewer's finding-2 diagnostic, reproduced: the named theorem survives the mutation that reds the consumer; C-Q9 does not* |

Read together, the four runs are findings 1 and 2 in full: for each of
D6 and D10, the relation the consumer needs is **falsifiable**, the
named producer **survives** its falsification, and a query that
**does** range over it is green on the committed verifier. No new claim
is made about any registered query; no family file records these runs;
they discharge nothing.

### Hostile re-read of the whole document (2026-09-15, round 3)

Every producer cell in the file was re-read against the question *does
a query exist that ranges over the term this consumer consumes?*, and
every count against the "Combined consequences" table. Results:

- **Producer claims backed by a query that ranges over the consumed
  term:** D3, D4 (S-P3 Q1(ii), over the authority tuple and the
  accepted key), D7 (S-P2 Q2 + Q6, over the signer set and the frames),
  D8 (S-P7 Q2/Q1, over `objType`), D9 (first-link Q4/Q6, over the
  evidence pair), D11/D12/D13 (S-P7 Q2/Q5 and S-STANDING Q1, over the
  attributed identity, the TLR and the entitled key — producers only;
  their **consumers** do not exist).
- **Producer claims withdrawn to "to be registered in the capstone":**
  D5 (C-Q7), D6 (**C-Q8**, this round), D10 (**C-Q9**, this round).
  No near-miss theorem is named for any of them.
- **Counts:** the matrix is 8 rows; firm 5; provisional-on-producer 3;
  provisional-on-R-2 1; producer exists and is green 5 of 8; NOT YET
  SHOWN 5; held out by R-1 2; conditional on R-3 3. Each agrees with
  outcome 1 of the combined-consequences table, and §2's counts table,
  §5's table and this list were compared cell by cell.

  > **[Superseded by the round-4 repair, 2026-09-15.]** These counts
  > were correct against the file as this round-3 pass left it and are
  > kept as written per amend-don't-rewrite. They are **not** the
  > file's current counts. Round 4 (finding 2) moves **D11** from
  > §2(c) into the matrix, because C-Q1's link 6b consumes L-13's scope
  > relation unconditionally: the matrix is now **9 rows**, firm **6**,
  > provisional-on-producer **3**, provisional-on-R-2 **1**, producer
  > green **6 of 9**, red-on-exactly **3**, NOT YET SHOWN **6**, held
  > out by R-1 **2**, conditional on R-3 **2**. See §2's counts table
  > and §5's "Combined consequences".
- **Marked NOT YET SHOWN and left there:** D4, D6, D7, D8, D9 in 2(a);
  D11, D12, D13 in 2(c); C-C1's set (b). In every case the consumer is
  the capstone and its query does not exist.
- **Not asserted anywhere in this file:** that any join is discharged;
  that C-Q1, C-Q6, C-Q7, C-Q8 or C-Q9 exists; that any companion's
  family-local failed-query set is exhaustive for the composed fixture;
  that the `REFUSAL` domain is checked; or that E18 is signed off.
- **Known limit of this pass, recorded rather than hidden.** The
  register applies R-1's Reading A to D1 and D2 because the skeptic
  established the rule's antecedent is unmet there. **The same
  structural argument reaches D10**: S-P2 transcribes S-P3's possession
  check, and severing S-P3 leaves `SetAltered` green. D10 is kept in
  2(a) because, after finding 2, its producer is **C-Q9 — a capstone
  query in the same fixture as the consumer**, so the transcription
  question does not arise for it. If the author reads R-1 more widely
  than this register does, D10 belongs in 2(b) with D1 and D2, and the
  matrix is 7 rows. **This is flagged, not decided.**

**One item outside this file, for the owner**, carried forward from the
skeptic log and still true: `formal/BAND0-EXIT.md` E5's description of
this register is stale — it reads *"the capstone's minimum query list
C-Q1–C-Q4"*, while §6 now registers C-Q1(strict/degraded), C-Q2, C-Q3,
C-Q4, C-Q5, C-Q5w, C-Q6, C-Q7, **C-Q8**, **C-Q9**, C-N1 and nine
required retained queries, and its kind tallies predate every repair
since 2026-09-14. Not edited here; this pass's scope is this file and
the ledger-tests README.

---

## Repairs after the 2026-09-15 Codex round 4

**Source:** `docs/reviews/2026-09-15-codex-full-review-ledger-round4.md`
(OpenAI Codex CLI, `gpt-6-astra`, non-author; run non-interactively by
the owner instance against the whole file after the fourth repair; four
findings, all accepted). The reviewer would not approve the register as
the capstone plan. **All four findings are defects in the proposed
proof contract — C-Q1 and C-Q8 — not in the register's entries, its
producer–consumer determinations or the construction**; the reviewer
re-checked every matrix row, every companion and every count and found
the rest internally consistent, and recorded in terms that these are
*"not counterexamples to the unmutated construction"*.

This file is an unfrozen PROPOSED draft, so the repairs are made in
place and listed below. **No repository file other than this one and
the ledger-tests README was edited, and no repository model was run.**
The seven verification runs were made on **copies** in
`formal/suite/ledger-tests-2026-09-14/`
(`proverif -lib formal/suite/lib/tessera_theory.pvl`, ProVerif 2.05,
each `rc=0`, each a few seconds); they are unregistered
ledger-verification probes — evidence about the checking arrangement,
never about a registered query — and no family file records them.

**The finding behind the findings, this round.** Rounds 1–3 kept
finding *near-miss producers*. Round 4 finds the same shape one level
up, in the **queries themselves**: a contract conjunct written so that
it quantifies over less than the relation it is supposed to establish —
C-Q8 over honest-released signature terms instead of every accepted
triple; C-Q1's link 1 over honest publication instead of
evidence-to-this-acceptance; its link 2 over reported slots instead of
required slots; its link 6 over one property while claiming two. **The
rule this repair adopts:** a contract conjunct names *the set it
quantifies over* and *the failure mode it must catch*, and a companion
is registered for every conjunct, including conjuncts whose producer is
the capstone's own verifier.

### Edits by finding

| # | Finding | Repair |
|---|---|---|
| **1** | **C-Q8 quantifies over honest-released signature terms only, so a same-key unbinding of non-`OT_ATTEST` frames escapes it.** C-Q1 requires `checksign(sg, kX) = (BYTES, fb)` for *every* acceptance, including degraded acceptance; attacker-created signatures were outside C-Q8's observation. | **C-Q8 is rewritten** (§6) as a **structural judge over every accepted `(accepting key, signature term, presented framed bytes)` triple, including failed verification**: the verifier reports the triple at every acceptance point whoever made `sg`, and the judge fires unless `checksign(sg, kX)` is exactly `(BYTES, fb)`. The honest-issuer private release is removed; **the honest-origin/transplant claim stays C-Q7's** and the two are registered as separate queries with separate companions. The withdrawn round-3 wiring is kept in the row, and in L-06's R-bytes rows, marked as the thing the query must **not** be. C-Q8's cell gains a fixture, a four-case compromise list, an expected outcome and named witnesses. **C-C7 is re-specified against the rewritten query** and now carries **two configurations**: (i) the same-key byte unbinding and (ii) the reviewer's **type-conditional** escape. Runs: `d6c`, `d6d`, `d6e` below. The "must not do" list gains *"build C-Q8 in its round-3, honest-filtered form"*. |
| **2** | **C-Q1 link 6 conflates object type with innermost-issuer scope; only `TypeConfused` is named as producer.** | **Link 6 splits into 6a (object type, producer S-P7 Q2/Q1 `TypeConfused`, D8) and 6b (innermost-issuer scope, producer S-P7 Q2/Q5 `Rescoped`/`RescopedD1`/`RescopedD2`, D11)**, with S-P7's own Q6b companion cited as the separation: `TypeConfused` stays `is true` (`sp7_q6b_companion_key_outermost.out:489`) while `Rescoped` goes `is false` (`:769`) and both honest witnesses stay reachable (`:1317`, `:1508`). **The routing is then fixed.** C-Q1 consumes scope **unconditionally** under every formulation, so L-13's consumption never depended on R-3: **D11 moves out of §2(c) into the cross-model matrix §2(a)**, L-13's Kind becomes CROSS-MODEL, and **R-3 is restated as deciding only the standing conjuncts** — L-16/L-17, rows D12/D13. §2(c) is renamed and now holds **two** entries (empty under formulation N and under the degenerate case). **Every count is restated:** matrix **9**, firm **6**, provisional-on-producer 3, provisional-on-R-2 1, producer green **6 of 9**, red-on-exactly 3, NOT YET SHOWN **6**, companion-on-producer's-own-query **5**, held out by R-1 2, conditional on R-3 **2**. **The combined-consequences table is rewritten** with D11 in the firm base and a new §2(c)-entries column: outcomes 1–2 → 9 rows, 3–4 → 8, 5–6 → 11, 7–8 → 8. The round-3 counts in the earlier repair sections are left as written and given a superseding note. |
| **3** | **C-Q1 drops accepted-evidence binding in degraded mode.** `AuthorityEvidence` was declared but `LayerAccepted` carried neither the evidence term nor a reference tying that validation to this acceptance; link 1 asked only whether an honest authority published `t`, and degraded mode dropped the link entire. | **`LayerAccepted` gains the accepted evidence term** (or a reference naming the `AuthorityEvidence` report this acceptance consumed). **Link 1 splits into 1a and 1b.** **1a — evidence → this acceptance:** `checksign(ev, kCh) = (STMT_DIGEST, h(t))` (or `(STMT_DIRECT, t)`, D-1) for the accepted `t`, **including the case where `ev` does not verify at all**, asserted in **both** modes; a declared-but-unconsumed `AuthorityEvidence` event does not close it. **1b — authority → tuple:** the honest-publication conclusion, **and only this** is dropped in degraded-compromised mode, per A3 §A3.2's fewer-but-never-zero evidence (`docs/phase-0-prereg-amendment-3.md:115-120`, `:142-150`). The strict/degraded table is rewritten accordingly. **C-C10 is registered** as 1a's companion, with the note that C-C1 (both channel keys public) breaks 1b and leaves 1a standing. Runs: `cq1a`, `cq1b` below. |
| **4** | **C-Q1's per-slot contract does not express required-set completeness within one acceptance.** The correspondence quantified over observed `LayerAccepted` reports and checked each reported slot against the manifest; it never required a report for *every* required slot, and the event carried nothing tying two slots to the same acceptance. | **`LayerAccepted` gains an acceptance identifier `aid`** (the aggregate package term serves equally; whichever is chosen is written into the query text before predictions freeze), every slot report of one acceptance carries the same `aid`, and a new event **`AcceptanceComplete(aid, lyr, t)`** is emitted once per acceptance after the slot reports. **Link 2 splits into 2a (per-slot membership) and 2b (required-set completeness)**, 2b written as one correspondence conjunct per required-set shape, demanding a `LayerAccepted` record for **every** required slot **grouped under the same `aid`**. **C-C9 is registered** as 2b's companion and as **D7's re-specified companion**, so D7's severing now falsifies C-Q1's completeness conjunct and not only `Stripped`; S-P2's own Q3/Q4/Q6-C are retagged as family-local contrasts. Runs: `cq1c`, `cq1d` below. |

### Scratch runs, 2026-09-15 (round 4)

Seven new files in `formal/suite/ledger-tests-2026-09-14/`, each a copy
of a committed model (or of an earlier scratch copy) with a header
naming what it copies and what it mutates. All `rc=0`.

| File | Copy of | Mutation / addition | Result (`.out` line) |
|---|---|---|---|
| `d6c_sp1_q8_judge_all.pv/.out` | `ledger-tests-2026-09-14/d6a_sp1_q8_base.pv` (itself an unmutated copy of the committed `s-p1/proverif/sp1_q2_degraded_compromised.pv` plus the C-Q7 and round-3 C-Q8 judges) | **adds** the **rewritten C-Q8** — a structural judge over *every* accepted `(key, signature, presented frame)` triple, including failed verification, with no honest-signature filter; verifier and every registered query unmutated | C-Q7 `is true` (`:272`), round-3 C-Q8 `is true` (`:278`), **rewritten C-Q8 `is true` (`:284`)**, Q2(i) `is true` (`:292`), witness reachable (`:469`), Q2(ii) `is false` (`:620`) as registered. *The rewritten judge is green on the committed verifier* |
| `d6d_sp1_q8_type_conditional_unbound.pv/.out` | `d6c_sp1_q8_judge_all.pv` | **the reviewer's round-4 escape:** byte equality between the signed and the presented frame required **only** when the signed frame's `objType` is `OT_ATTEST`, waived for every other signed frame type. Every other check retained; every honest signature in this fixture is over an `OT_ATTEST` frame | **round-3 honest-filtered C-Q8 stays `is true` (`:315`)** while **the rewritten C-Q8 is `is false` (`:507`)**; C-Q7 `is true` (`:308`), honest-key authorship `is true` (`:515`), witness reachable (`:692`), Q2(ii) `is false` (`:876`). ***This is the whole of finding 1:*** *the exact byte relation fails, the round-3 form does not see it, the rewritten form does, and the honest witness survives* |
| `d6e_sp1_q8all_samekey_unbound.pv/.out` | `d6c_sp1_q8_judge_all.pv` | **C-C7 configuration (i)**, the same-key byte unbinding `d6b` makes: the signature must verify under `kX` over *some* frame naming `fp(kX)`, not over the presented bytes | **rewritten C-Q8 `is false` (`:643`)**, round-3 form `is false` (`:455`), Q2(i) `is false` (`:809`), **C-Q7 stays `is true` (`:274`)**, witness reachable (`:989`). *C-C7 re-specified against the rewritten query: it still falsifies it, and still leaves C-Q7 green* |
| `cq1a_sp1_evidence_base.pv/.out` | `d6c_sp1_q8_judge_all.pv`, verifier and every registered query **unmutated** | **adds** C-Q1's **link-1a** evidence-binding conjunct: the acceptance report carries the accepted evidence term and a judge requires `checksign(ev, pkCh) = (STMT_DIGEST, h(t))` for the accepted `t`, including non-verification. **Degraded mode, sole channel compromised** | C-Q7 (`:304`), round-3 C-Q8 (`:310`), rewritten C-Q8 (`:316`), **link 1a (`:322`)** and Q2(i) (`:330`) all `is true`; witness reachable (`:507`); Q2(ii) `is false` (`:658`). *The evidence conjunct is feasible and green on the committed degraded verifier* |
| `cq1b_sp1_evidence_unchecked.pv/.out` | `cq1a_sp1_evidence_base.pv` | **only** the degraded verifier's evidence check removed — `let (=STMT_DIGEST, =h(t)) = checksign(ev, pkS) in` deleted. Tuple fingerprint, possession over the manifest, the attestation signature over the presented bytes, the in-bytes P3 binding and `mh = h(t)` all retained | **link 1a `is false` (`:466`)** while **C-Q7 (`:301`), the round-3 C-Q8 (`:307`), the rewritten C-Q8 (`:313`) and honest-key authorship (`:474`) all stay `is true`** and the witness stays reachable (`:638`); Q2(ii) `is false` (`:776`) as registered and as in the baseline. ***This is the whole of finding 3:*** *evidence binding is a separate conjunct, it is falsifiable, and dropping it disturbs nothing else — so the degraded form must carry it* |
| `cq1c_sp2_slots_base.pv/.out` | `ledger-tests-2026-09-14/d10a_sp2_q9_base.pv` (itself an unmutated copy of the committed `s-p2/proverif/sp2_q2_degraded_compromised.pv` plus the `PossJudge` and C-Q9 judges) | **adds** C-Q1's **link-2b** completeness conjunct: a fresh **acceptance identifier** per acceptance, a slot record per signer slot under that identifier, `AcceptanceComplete(aid, t)` after them, and three correspondence queries demanding a record for every required slot of the accepted manifest; verifier and every registered query unmutated | `Stripped` (`:471`), `SignerForged` (`:478`), `SetAltered` (`:485`), `Reattributed` (`:492`), `Spliced` (`:1133`), `PossessionTransplanted` (`:1140`), C-Q9 (`:1147`) all `is true`; **all three link-2b conjuncts `is true`** — one-signer (`:1161`), two-signer slot A (`:1175`), two-signer slot B (`:1189`); both `HonestComplete` reachable (`:663`, `:889`), `HonestAccepted` reachable (`:1126`) |
| `cq1d_sp2_slots_missing.pv/.out` | `cq1c_sp2_slots_base.pv` | **the one-signer branch's required-set requirement dropped**: `let authTuple(id, kfprA, =signers0, alg, ver) = t in` becomes `let authTuple(id, kfprA, ss, alg, ver) = t in`. Every per-slot check retained — each reported slot still belongs to the manifest and still matches its key | **link-2b slot-B conjunct `is false` (`:1519`)** and `Stripped` `is false` (`:643`), while **the per-slot conjuncts survive** — link-2b one-signer (`:1333`) and slot A (`:1353`) stay `is true`, as do `SignerForged` (`:650`), `SetAltered` (`:657`), `Reattributed` (`:664`), **`Spliced` (`:1305`)**, `PossessionTransplanted` (`:1312`) and **C-Q9 (`:1319`)**; both `HonestComplete` (`:835`, `:1061`) and `HonestAccepted` (`:1298`) reachable. ***This is the whole of finding 4:*** *every reported slot can belong to the manifest and match its key while a required slot has no report at all* |

Read together, the seven runs are the four findings in full. `d6c`/`d6d`
show a quantifier gap in a query that was green: the relation fails, the
old judge does not see it, the rewritten judge does. `d6e` re-specifies
C-C7 against the rewritten judge. `cq1a`/`cq1b` and `cq1c`/`cq1d` show
that C-Q1's evidence-binding and completeness conjuncts are each
**separately falsifiable** and each **undetected by the conjuncts that
were written**. No new claim is made about any registered query; no
family file records these runs; they discharge nothing.

### §6 re-read as a builder (2026-09-15, round 4)

After the four repairs, §6 was re-read against the question *could
someone build this without asking a question the file does not answer?*

- **Every capstone query** — C-Q1(strict/degraded), C-Q2, C-Q3, C-Q4,
  C-Q5, C-Q5w, C-Q6, C-Q7, C-Q8, C-Q9, C-N1 — carries an **event
  signature**, a **fixture**, a **compromise-case list**, an **expected
  outcome** and **named witnesses**. C-Q8's cell gained all five this
  round; C-Q1's fixture and four compromise cases are §6(4) and are
  inherited by C-Q8, C-Q9 and the retained checks; C-Q5w *is* the
  witness clause for C-Q5; C-N1 is the per-fixture witness requirement
  every other query's witness clause cites.
- **Every companion** — C-C1…C-C10 — carries its **three sets**
  (expected failed-query set, guarantees that must stay green,
  witnesses that must stay reachable), each verified against a cited
  `.out` line, and each is tagged **family-local** with the standing
  instruction to **re-specify against the capstone's own query names
  once C-Q1…C-Q9 exist, before predictions freeze, as a registered
  step** (round 3, finding 3 — unchanged and reaffirmed).
- **Three conjuncts now have companions that did not:** C-Q1's link 1a
  (**C-C10**), link 2b (**C-C9**), and C-Q8 in its rewritten form
  (**C-C7**, two configurations).
- **Still unanswered by design, and said so:** links 3 and 4 have **no
  producer** (C-Q9, C-Q8 must be registered first); link 1a names no
  producer at all and claims none, being structural in the capstone's
  own verifier; C-Q6's formulation is R-3's; and `ChainBroken`,
  `AcceptanceComplete`, C-Q8's and C-Q9's events are declared in **no
  committed model**, so no companion's set for them can be shown before
  the capstone exists.

**Not asserted anywhere in this file:** that any join is discharged;
that C-Q1, C-Q6, C-Q7, C-Q8 or C-Q9 exists; that any companion's
family-local failed-query set is exhaustive for the composed fixture;
that the `REFUSAL` domain is checked; or that E18 is signed off.

**Carried forward, still true, still outside this file's scope:**
`formal/BAND0-EXIT.md` E5's description of this register is stale — it
reads *"the capstone's minimum query list C-Q1–C-Q4"*, while §6 now
registers C-Q1(strict/degraded), C-Q2, C-Q3, C-Q4, C-Q5, C-Q5w, C-Q6,
C-Q7, C-Q8, C-Q9, C-N1, nine required retained queries and ten
companions C-C1–C-C10; its kind tallies predate every repair since
2026-09-14. Not edited here.

---

## The author's ruling (2026-09-15) — what it changed in this file

**Provenance label: RULED (author)**, per
`formal/spike/first-link/DECISION.md`. The author decided in session, in
his own words; nothing recorded here is a clerk's reading of a
discussion. The two ruling sentences are quoted verbatim at the head of
§5 and in the file's header block, and are not paraphrased anywhere.

| Fork | Ruled | Effect in this file |
|---|---|---|
| **R-1** | **Reading B — composed** | L-01 → S-P2 and L-01 → S-P7 are CROSS-MODEL. **D1 and D2 move from §2(b) into the §2(a) matrix**, firm, with `m4`/`s4` registered as the capstone's own companions **C-C2** and **C-C4**. **§2(b) is vacated** (its preamble kept as the record of why the rows were once held out) |
| **R-2** | **yes** | A jointly-sufficient pin is a dependency. **D10 is a matrix row**; the `prov(R-2)` tag is retired throughout; C-C3 is no longer "provisional, R-2". **D10's producer defect is untouched** — C-Q9 must still be registered |
| **R-3** | **formulation W** | The composition query concludes in a **standing verdict**. L-16 and L-17 are CROSS-MODEL; **D12 and D13 are rows of §2(c)**, both NOT YET SHOWN. **C-Q6 is written in formulation W** in §6 |

**The instrument, restated.** This file's **default reading** is now
outcome 5, stated in the header, in §2's preamble, in §2's counts, at
the head of §5, in the combined-consequences table's row 5, and in §6's
opening. The capstone's `PREDICTIONS.md` is drafted from §6 under this
reading. **The commit is the author's**; the file remains PROPOSED and
**discharges nothing**.

**The ruled counts.** Matrix §2(a): **11 rows** (D1–D11) — **8 firm**
(D1, D2, D3, D4, D7, D8, D9, D11) and **3 `prov(P)`** (D5 → C-Q7,
D6 → C-Q8, D10 → C-Q9). Producer exists and is green: **8 of 11**.
NOT YET SHOWN within the matrix: **6** (D4, D6, D7, D8, D9, D11).
§2(b): **0 — vacated**. §2(c): **2 rows** (D12, D13), both NOT YET
SHOWN, both outside the matrix count.

**The author's carried concern is recorded and not dissolved:** *"the
real burden for testing these claims will fall on the adjudicator."*
Kept at the head of §5 in his words.

**Vocabulary.** "Producer" and "consumer" name **models**, never
parties — stated once at the top of the file, at the author's
instruction that the word be given its abstract reading.

---

## Corrections after the author's ruling (2026-09-15)

Three bounded corrections carried forward by the **non-author
reviewer** (Codex, gpt-6-astra) on 2026-09-15 and **accepted by the
owner instance**. Each is a correction of *this file's* proof contract.
**None of them touches the author's ruling, and none touches a sentence
of the author's.** They were applied after the ruling because they are
contract defects the ruling neither creates nor cures.

### (a) The authorship gloss on C-Q8's predicate — L-06 and D6

**The defect.** L-06's R-bytes row and the D6 row both read the
relation as *"the signature accepted over `fb` under `kX` **was produced
by `kX`'s holder** over exactly `fb`"*. That **overstates what C-Q8's
predicate establishes.** The rewritten C-Q8 (round 4) is a *structural*
judge: it checks that the accepted signature **verifies under the
accepted key over exactly the presented bytes** —
`checksign(sg, kX) = (BYTES, fb)` — including the case where it does not
verify at all. It does not, and cannot, say who produced `sg`.

**Why the model forbids the stronger reading.** The library's signature
destructor has a second rewrite rule
(`formal/suite/lib/tessera_theory.pvl:110-115`, read for this
correction):

> `fun dsks(bitstring, bitstring): skey.`
> `fun checksign(bitstring, pkey): bitstring`
> `  reduc forall m: bitstring, k: skey; checksign(sign(m, k), pk(k)) = m`
> `  otherwise forall m: bitstring, k: skey, r: bitstring;`
> `          checksign(sign(m, k), pk(dsks(sign(m, k), r))) = m.`

This is the registered A1.3 item 3 / D-4 capability: from one seen
signature the adversary derives a key it holds under which that same
signature verifies to the same message. **A signature may therefore
verify under an alternative key**, and "verifies under the accepted key"
does not entail "was produced by that key's holder".

**The repair.** The authorship gloss is replaced with the exact-bytes
statement in all four live places: L-06's *"Two relations, not one"* row,
L-06's *"Producer for R-bytes (D6)"* cell, L-06's capstone consumer row,
and the **D6** row of §2(a). **Nothing else changes.** In particular:

- **Authorship stays S-P1's separate obligation** — Q2(i),
  `AcceptedUnderHonestKey(k, fb) ⟹ IssuerSigned(k, fb)`, quantified over
  **honest** keys, `sp1_q2_*.out:173`. It is not merged into C-Q8 and is
  not weakened.
- **Anti-transplant stays C-Q7's separate obligation** — the
  signature-**term** judge, registered unreachable, whose companion is
  C-C6. It is not merged into C-Q8 either; round 4 already ruled the two
  queries separate and that stands.
- No count moves. D6 was `prov(P)` on C-Q8 before the correction and is
  `prov(P)` on C-Q8 after it.

*Left as written:* the round-3 finding-1 row of the review log below,
which quotes the old gloss. It is a record of what was repaired that
round, not a live statement of the contract.

### (b) C-Q1 link 1b — a judge cannot observe a non-event

**The defect.** Link 1b was written as a conjunct the judge *tests*:
*"the accepted `t` is the tuple an uncompromised authority channel
**published**"*, with `ChainBroken` fired when it fails. **A judge
inside the model cannot observe that a publication event never
occurred.** It sees only what the acceptance carried. The link as
written asked for a negative observation that no process can make, and
C-C1's expected failure was specified in the same impossible terms
(*"`ChainBroken` at link 1b, reachable"*).

**The repair.** Link 1b is expressed as a **correspondence** — the shape
ProVerif actually has for provenance, and the shape S-P3 Q1(ii) (its
named producer) already uses:

> `event(LayerAccepted(aid, lyr, t, ev, slot, kX, ppf, sg, fb))`
> `  ==> (event(AuthorityPublishedDNS(t)) || event(AuthorityPublishedRepo(t)))`

in the library's own event names (`lib/tessera_theory.pvl:190-191`),
quantified over every acceptance the judge observes, registered
`is true`, **strict form only**. Link 1b is therefore **not** among
`ChainBroken`'s conjuncts — it joins link 2b as a correspondence — and
§6(2) and §6(5) say so.

**The companion re-specified.** **C-C1**'s conjunct (b) no longer reads
*"`ChainBroken` at link 1b, reachable"*. What C-C1 must expose is **the
link-1b correspondence going `is false`**: with both channel keys
public, the adversary produces accepted evidence for a tuple **no honest
channel process ever published**, so an acceptance exists with no
antecedent publication event. It is still **NOT YET SHOWN** — C-Q1
exists in no model — and C-C1's conjunct (a), `Accept ⟹ IssuerSigned`
red at `s6_bothchannels.out:361`, is unchanged. Link **1a** and its
companion **C-C10** are untouched: 1a is a structural conjunct of the
capstone's own verifier, asserted in both modes, and this correction
does not reach it.

### (c) The acceptance identifier is not the aggregate package term

**The defect.** The round-4 event contract offered two things as equally
good acceptance identifiers: *"a fresh name minted once per completed
acceptance; **the aggregate package term serves equally**, and whichever
is chosen must be written into the query text before predictions
freeze."* **The aggregate package term is not an acceptance
identifier.** Replaying the same package gives **distinct acceptance
executions the same term**, so slot reports from *different* executions
would group under one `aid` and a link-2b completeness conjunct could be
satisfied without any single acceptance having checked every required
slot. That is precisely the hole link 2b was added to close (round 4,
finding 4).

**The repair.** `LayerAccepted`'s first argument is **a fresh
`new aid: bitstring`, minted once per completed acceptance, and nothing
else.** *"Serve equally"* is withdrawn, and with it the instruction to
choose between the two before predictions freeze — there is nothing to
choose. **Completeness means every required slot was checked in THIS
execution**, and only a per-acceptance fresh name expresses that.
`AcceptanceComplete(aid, lyr, t)` carries the same `aid`, as before.

*Unchanged:* link 2b's correspondence text, C-C9 (its companion) and
the `cq1c`/`cq1d` runs behind it — those fixtures already mint a fresh
per-acceptance name.

### What these three corrections do not do

They add no row, remove no row, and move no count. They change **no**
classification, and therefore nothing the author ruled. They register
nothing: C-Q1, C-Q8 and C-C1 still do not exist, and the register still
claims no discharge. **No sentence of the author's is altered anywhere
in this file.**
