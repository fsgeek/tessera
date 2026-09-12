# S-STANDING — the terminal lineage record under A1.3: results

**STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not
adopted; the commit is the author's.** Predictions were frozen at
`5188e7a` (`PREDICTIONS.md`, with the three dated rulings A6/A7/A8
entered at its end and dispositions B8/B9 of
`formal/suite/ROUTED-2026-09-06.md`) before any model existed. This
file records predictions against observed outcomes in the registered
three-outcome vocabulary (violation / timeout / termination), the one
encoding recut and why, seven findings, and the A3.3 ledger entries
S-STANDING offers the suite — offered, not entered. Falsification
review: **NOT RUN**. Author read: **pending**. Nothing here is
ratified; nothing here discharges criterion 4's second condition until
the cross-family falsification review (ENUMERATION note 5 item 1) and
the author's read have happened.

Tooling: ProVerif 2.05, `-lib formal/suite/lib/tessera_theory.pvl`
(with D-5/D-6 entered 2026-09-06). Models and outputs:
`formal/suite/s-standing/proverif/` (`run_ladder.sh`, `ladder.log`).
Pre-recut development encoding archived under `proverif/run1/`;
scratch ablation probes under `proverif/ablations/`. Every registered
run terminated in ≤ 1 s against boxes of 15–30 min.

## Ladder outcomes (predictions vs observed)

| Query | Registered prediction (`PREDICTIONS.md`) | Observed (ladder run, `ladder.log`) | Outcome; registered branch that fired |
|---|---|---|---|
| **SS.Q1 strict, DNS compromised** — `ss_q1_strict_dns_compromised` | all hold (p≈0.5 as-registered; 0.25 encoding recut; 0.05 real violation; 0.2 timeout); box 30 min | (i) `Established ==> Designated` **true** (`.out:457`); (ii) true for `pk(skH1)`, `pk(skH2)` (`.out:467`, `477`); (iii) `StandingUnentitled` unreachable (`.out:484`); (iv) `HonestStandingEstablished` **reachable** (`.out:781`); five witnesses reachable — S1 `1065`, S2 `1347`, S3 `1472`, S4 `1752`, MISMATCH `1927`; B9 `ReasonCollapsed` unreachable (`.out:1934`); 1 s | **termination, as predicted** — the "all hold, as-registered" branch (p≈0.5). One development-time encoding recut preceded the ladder (see Recuts); it changed no result |
| **SS.Q1 strict, repo compromised** — `ss_q1_strict_repo_compromised` | same | identical results, same `.out` line numbers; 0 s | **termination, as predicted** |
| **SS.Q1d degraded, sole channel compromised** — `ss_q1d_degraded_compromised` | (i) **fails** by an adversary-key trace (p≈0.7); (ii), (iii) hold; (iv) reachable; p≈0.15 (i) unexpectedly holds; p≈0.15 timeout; box 30 min | (i) **false**, trace found (`.out:589`; trace `.out:581–587`: the adversary's own tuple `authTuple(a_1, fp(pk(a_2)), …)` signed with the leaked `skS`, its own core `a_6`, its own TLR under `a_2`); (ii) true (`.out:598`, `607`); (iii) unreachable (`.out:613`); (iv) reachable (`.out:917`); witnesses reachable (`1098`, `1280`, `1388`, `1566`, `1719`); B9 unreachable (`1725`); 1 s | **violation of (i), as predicted** — the registered degraded-mode cost branch (p≈0.7), now a checked fact (F2) |
| **SS.Q2 companion A: identity declared** — `ss_q2_companionA_identity_declared` (+ A7 wrapper trace) | (i), (ii) **violated**, trace readable (p≈0.75; 0.15 recut; 0.1 timeout); `StandingUnentitled` unreachable; box 15 min | (i) **false** (`.out:630`), (ii) **false** for both honest keys (`.out:808`, `986`); A7 wrapper correspondence `EstablishedWrapped ==> Designated` **false** (`.out:1176`, trace `.out:1166–1174`: core `wrapCore(a_4, a_5)`, label `LBL2`, honest TLR of `skH2`); `StandingUnentitled` unreachable (`.out:1182`); N1 and five witnesses reachable; B9 unreachable; 0 s | **red as required**, on exactly the named queries, no recut; two transplant trace shapes exhibited (F5) |
| **SS.Q3 companion B: entitled key via envelope only** — `ss_q3_companionB_entitled_via_envelope` | `StandingUnentitled` **reachable**; (i) violated by the Q1d shape; (ii) true (p≈0.7; 0.2 companion cannot fail; 0.1 timeout); box 15 min | `StandingUnentitled` **reachable** (`.out:860`; trace `.out:848–856`: adversary key `pk(a_2)`, adversary core `a_3`, adversary TLR under `a_2`, **honest** evidenced tuple `m2`); (i) false (`.out:628`); (ii) true (`.out:642`, `656`); N1, witnesses reachable; B9 unreachable; 1 s | **red as required** on exactly the named query; the p≈0.2 "cannot fail" branch did not fire (F3) |
| **SS.Q4 companion C: terminal unchecked** — `ss_q4_companionC_terminal_unchecked` | correspondences **violated** by two trace shapes (S2 as established; S4 as established) (p≈0.8; 0.1 recut; 0.1 timeout); fixture exception registered; box 15 min | (i) false (`.out:576`); (ii) for `pk(skH1)` false, trace = the **abandoned** attempt (`decl1`) of the shipped lineage (`.out:843–849`); (ii) for `pk(skH2)` false, trace = an attempt of the **refused** lineage (`.out:1115–1123`); `StandingUnentitled` unreachable (`1129`); N1 reachable (`1425`); S2 and S4 witnesses **unreachable** (`1708`, `1838` — consequence of the mutation, the branches no longer exist); S1, S3, MISMATCH reachable; B9 unreachable; 0 s | **red as required**, both shapes, no recut (F4) |
| **SS.Q5 companion D: reason codes collapsed** (B9; not in the frozen ladder) — `ss_q5_companionD_reason_collapsed` | red-by-construction (p≈0.95 violation; 0.05 encoding) per routed item 5 as dispositioned by B9; box: the companion box, 15 min (none registered for this item) | `ReasonCollapsed` **reachable** (`.out:1965`; trace `.out:1951–1961`: `PATH_S2` and `PATH_S3` both emit `NO_STANDING`, the judge pairs them); every other query as in Q1 (the S2/S3 witnesses restated over `NO_STANDING`, reachable at `.out:1190`); 1 s | **red by construction, as registered** (F6) |

N1/N2 (ENUMERATION note 3): every model carries the judge-emitted
honest-flow witness `HonestStandingEstablished` (reachable in all
seven) and two honest issuers, each with its own tuple, each running
both lineage shapes (Q4's registered exception aside), with
adversary-chosen payloads; every axis a query binds has two honest
values (keys, tuples, lineage shapes, terminal dispositions, ≥ 4
honest attempt identities). All of this was spelled out in the frozen
plan (`PREDICTIONS.md` §"Fixture") and built as written.

## Prediction divergences

**None.** No registered query, companion, fixture, or timebox was
changed. Four entries belong under this heading anyway, because a
reader comparing the frozen plan to the models will see them; each is
recorded with its authority so it is not mistaken for a refinement:

1. **The TLR tag is the library's `TLR` (D-6), not model-local.** The
   plan's "Abstractions" bullet says "under a model-local
   domain-separation constant `TLR`". Ruling A6 (`PREDICTIONS.md`,
   routed item 1, dated note: *"ADOPTED (author), 2026-09-06 (ROUTED
   A6): Amendment 4 §A4.5 adds the terminal lineage record and the
   portable refusal record to P7's enumerated set. Until signed, the
   tag stays model-local as this plan says; on signature it enters the
   library as a recorded divergence."*) — Amendment 4 was committed by
   the author at `5188e7a` and OTS-stamped at `5dfd82b`; its status
   line (`docs/phase-0-prereg-amendment-4.md` lines 3–4) still reads
   "DRAFT — adopted in session, not yet signed" and carries no dated
   signing note; **this record reads the author's commit as the signing
   act**, and D-6 entered the library the same day on that reading. On
   that reading the plan's model-local branch no longer applies; every
   model uses the library constant and redeclares nothing, and this is
   a registered ruling executed, not a divergence. If the reading is
   wrong, every model's use of the library tag *is* a divergence from
   the frozen plan (ROUTED TO AUTHOR, item 1). *(Amended 2026-09-06
   after the skeptic review, finding 3; the sentence it replaces read
   "Amendment 4 was signed at `5188e7a` and D-6 entered the library the
   same day."; nothing else in this entry changed.)*
2. **Q2 carries a wrapper-shaped outer artifact and a second trace**
   (ruling A7, `PREDICTIONS.md` routed item 3, dated note). Built as:
   `wrapCore(inner, outer)` (declared, `[data]`), an extra event
   `EstablishedWrapped` fired in addition to `Established` when the
   presented core is wrapper-shaped, and one extra correspondence
   query. **Encoding choice beyond A7's literal wording:** `wrapCore`
   is declared in *every* model of the ladder, not only in Q2, so that
   (a) Q2 differs from the correct form only by its mutation and (b)
   the correct form's (i) is proved with wrapper-shaped outer
   artifacts available to the adversary. No honest process builds
   one. No prediction changed (A7's own statement).
3. **Q1 gains the B9 discrimination query and the ladder gains Q5.**
   Disposition B9 (`PREDICTIONS.md` routed item 5, dated clerk
   disposition; `ROUTED-2026-09-06.md` §B, "no veto stated"): *"Q1
   gains the collapsing companion, registered red-by-construction (p ≈
   0.95 violation, p ≈ 0.05 encoding), and the vector obligation
   stands."* The companion needs a query to be red on; that query
   (`ReasonCollapsed`, a private-channel reason judge pairing two
   distinct no-standing branches that emit one code) is therefore
   carried in every model and is green everywhere but Q5. It is not
   among Q1's four registered queries (i)–(iv); it is an addition under
   the disposition, not a divergence of registered text. Its box (15
   min) is the companion box, assigned by the collaborator because
   none was registered.
4. **Q1's "encoding recut" sub-bucket did not fire, but an encoding
   change did happen** — before the ladder, in development, without
   changing a result. Recorded under Recuts so the p≈0.25 branch is not
   read as "nothing happened".

## Recuts (encoding, not property)

**Recut 1 — lineage lookup as a destructor; reserved identifier
renamed (all models, before the ladder run).** The first complete
development run of Q1 (DNS) used an inline case split over the
two-entry lineage — `let lineage2(entry(a1, d1), entry(a2, d2)) = lin
in if aid = a1 then … else if aid = a2 then … else MISMATCH` — with
`StandingDecide` expanded twice, and a local named `sid`. Every RESULT
line was as registered; ProVerif emitted one warning, `identifier sid
rebound` (`sid` is ProVerif's reserved session-identifier name). The
recut replaces the split with a model-local destructor
`lookup2(aid, lin)` (the disposition recorded for `aid`, failing to the
`else` branch when `aid` is in neither entry) and renames the local
`shippedId`. Results identical; no warnings remain (S-P3 recut-3 rule).
Pre-recut encoding and output archived under `proverif/run1/` with a
README. This is the "case split the two-entry structure needs" the
plan predicted under SS.Q1's encoding sub-bucket, met at development
time rather than as a failed run.

No recut was needed for the judge-report idiom: every report output to
a private channel is either the last action of its branch or placed in
parallel with its continuation (S-P3 recut 1), and no query returned
"cannot be proved".

## Ablation probes (scratch, unregistered; `proverif/ablations/`)

Run by the collaborator after the ladder, on the DNS-compromised
correct form, one removal each, to make the header's LOAD-BEARING /
CARRIED labels results rather than predictions (S-P3 F7 pattern). These
are not registered queries and discharge nothing; they are archived so
the falsification reviewer starts from them rather than repeating them.

| Probe | Removed | Result | Label confirmed |
|---|---|---|---|
| `abl1_no_kT_eq_kX` | `if kT = kX` (TLR key equals the artifact's presented key) | all eleven results unchanged | **CARRIED** (inert) — as predicted |
| `abl2_no_anchor_check` | `let anchorProof(=h(tlrSig)) = ap` | unchanged | **CARRIED** (inert) — as predicted; content is ledger C-2 |
| `abl3_no_wellformedness` | `if d = DISP_SHIPPED` under `TERM_SHIPPED(aid)` | unchanged | **CARRIED** (inert) — as predicted; S-series vector obligation |
| `abl4_no_dns_evidence` | the compromised channel's evidence check | unchanged | **CARRIED** (inert) — the key is public; S-P3 F6 |
| `abl5_no_repo_evidence` | the honest channel's evidence check | (i) **false**; (ii), (iii) still true | **LOAD-BEARING for (i)** — with no honest evidence the adversary's own tuple is "evidenced" and its own key is entitled to it: the Q1d shape, reproduced in strict mode by removing the honest channel |
| `abl6_no_tlr_signature` | TLR signature verification (body read unsigned) | (i) **false**, (ii) **false** for both honest keys | **LOAD-BEARING for (i) and (ii)** — an unsigned lineage naming an adversary core, presented under the honest entitled key |

With the three companions (Q3: `fp(kT) = kfpr` inside the standing
path; Q2: derived identity; Q4: terminal disposition), every check the
header calls load-bearing has an exhibited red, and every check it
calls carried has an exhibited no-change.

## Findings

**F1 — The construction holds as registered, in strict mode, on the
first complete run, both variants.** With either authority channel
fully compromised, an `ESTABLISHED` standing report computed against a
key implies that the issuer holding that key signed one TLR whose
lineage contains the presented artifact's *verifier-derived* identity
`h(core)` and whose terminal designates it (Q1 (i), (ii)); no
`ESTABLISHED` is computed against a key the evidenced tuple does not
name (Q1 (iii)); and the honest flow reaches `ESTABLISHED` through the
judge (N1). What carries it, by the ablations and companions: the
honest channel pins the evidenced tuple (abl5); the tuple's fingerprint
pins the TLR key inside the standing path (Q3); the TLR signature pins
the lineage to that key (abl6); the derived identity pins the artifact
to a lineage entry (Q2); the terminal check and the per-entry
disposition check together pin "shipped" to that entry (Q4). *(Narrowed
2026-09-06, cross-family falsification review item 25: Q4 removes the
terminal predicate AND the per-entry check together and rearranges the
fixture, so its red cannot be attributed to the terminal check alone;
the reviewer's single-removal matrix shows that removing the terminal
predicate while keeping `d = DISP_SHIPPED` leaves (i)-(iii) green and
loses only the S2/S4 vocabulary witnesses, which is what SC-3
registers. The sentence replaced read "the terminal check pins
'shipped' to that entry (Q4)".)* Under a perfect `fp` and a perfect `h` (library header) —
**the transplant result's entire load is `h` injective** (plan,
"Abstractions"), as the plan said in advance so no reader mistakes it
for a signature result. The p≈0.05 "real violation" branch (the TLR as
adopted does not bind what A3.7.1 says) did not fire.

**F2 — The degraded-mode cost is now a checked fact, and the record can
say mechanically which claims survive it.** In Q1d the unrestricted
sentence (i) fails by exactly the predicted trace: the adversary signs
its own tuple with the leaked sole-channel key, presents its own
artifact and its own TLR under its own key, and the standing path
reports `ESTABLISHED` for an identity no honest issuer designated
(`.out:581–589`). The per-honest-key sentences (ii) and the
entitled-key sentence (iii) hold: an honest issuer's standing is not
usurped, and the adversary must bring its *own* tuple — it cannot
establish standing against the honest tuple. Amendment 4 §A4.6 (RULED,
author, 2026-09-06; `docs/phase-0-prereg-amendment-4.md` lines
152–167), quoted: *"A correspondence that holds in strict mode and
fails in degraded mode is therefore a registered **cost** of
degradation, to be stated in the relying-party story, never a defect of
the construction — provided the verdict says it is degraded."* Whether
the verdict is marked degraded is P4's obligation (§A1.2.1
explicit-policy logic; cross-formalism, carried here and not checked):
this model's envelope path fires the degraded-shape event `AcceptS`
(`ss_q1d_degraded_compromised.pv:318`), which is neither queried nor
shown reachable in the `.out` (the string appears only in the process
listing). §A4.6's proviso is therefore assumed to be met by P4, not
shown here. *(Reworded 2026-09-06 after the skeptic review, finding 2;
the two sentences replaced read "The envelope path in Q1d reports the
degraded acceptance shape (`AcceptS`), so the verdict says degraded.")*
Consequence for the relying-party story:
in degraded mode a standing report of `ESTABLISHED` says "the key this
bundle's evidence names designated this artifact"; whether that key is
the issuer's is what the sole compromised channel could not exclude,
and the adjudicator is handed that. This is Q5b's waiver cost
(first-link spike) and S-P3 F8's impersonation, met a third time at the
standing layer, and it is the same shape each time: the adversary's own
key over its own objects, never the honest key over anything.

**F3 — Companion B's discriminator is the judge, and the orthogonality
abstraction held.** Q3 and Q1d both violate (i) by the adversary-key
shape; what separates them is `StandingUnentitled`: in Q3 the evidenced
tuple is the honest `m2` and the key is not the one it names
(`.out:848–856`), so the judge fires; in Q1d the tuple is the
adversary's own, so it does not. This is exactly the split the
pre-freeze skeptic review wrote into the plan (review log entry 2). The
p≈0.2 branch — "the companion cannot fail because the envelope's
fingerprint check shadows the missing one" — did not fire, because the
envelope path and the standing path are separate processes on the same
bundle input, run in parallel: the structural orthogonality the plan
registered is what let the companion go red. The blind re-scoring's
conformance note (ENUMERATION note 4 item 2) is thereby a checked shape
in this suite: a bundle whose envelope would fail
`KEY_FINGERPRINT_MISMATCH` receives, from the correct standing path, an
`UNVERIFIABLE`/`STANDING_EVIDENCE_SIGNATURE_INVALID` report (by
inspection of `ss_q1_strict_dns_compromised.pv:315, 331–332`; not a
queried witness — only (iii)'s unreachability is in the `.out`), never
an `ESTABLISHED` against the unentitled key.

**F4 — S4 is not S2 under another name; the third binding is
load-bearing on both lineage shapes.** Q4 exhibits the two registered
trace shapes with one trace per query: under `pk(skH1)` the
**abandoned** attempt of the shipped lineage (its core carries
`decl1`) is reported `ESTABLISHED` (`.out:845`); under `pk(skH2)` an
attempt of the **refused** lineage — whose TLR's terminal is
`TERM_REFUSED` and which fires no `Designated` at all — is reported
`ESTABLISHED` (`.out:1119`). The registered fixture exception (one
lineage shape per honest key in this companion) was used as written;
the alternative the plan named (per-shape judge events, S-P3 recut-2
pattern) was not needed.

**F5 — The wrapper transplant is exhibited literally (A7), and the
correct form rejects it by the same mechanism as any other transplant.**
Q2's second trace presents `wrapCore(a_4, a_5)` — an adversary-built
outer artifact around an *arbitrary* inner value — with the shipped
attempt's label `LBL2` and the honest TLR of `skH2`; the label-bound
standing path reports `ESTABLISHED` for `h(wrapCore(a_4, a_5))`, an
identity nobody designated (`.out:1166–1176`). *(Narrowed 2026-09-06,
cross-family falsification review item 26: the registered A7 query
binds only the wrapper SHAPE, and its committed trace uses arbitrary
inner and outer values, so this trace alone does not show a wrapper
around the honest shipped core. The literal transplant is now
exhibited by an unregistered post-freeze companion query — see
"Post-freeze additions (unregistered)" below — whose trace has
`inner` = the very core `skH2` designated as shipped.)* In the correct form the same
presentation reaches `STANDING_EVIDENCE_MISMATCH` by `h` injectivity —
an inference from `h` injective and `[data] wrapCore`, not an exhibited
trace: the queried MISMATCH witness (Q1 `.out:1927`) carries an
adversary core `a_4`, not a wrapper. The inference: the lineage names
`h(core2)`, and `h(wrapCore(core2, x)) ≠ h(core2)` under `h` injective
— the derived identity is the only identity, and a wrapper has a
different one. **Boundary, stated exactly:** this is the
*identity-binding* half of the transplant. Which identity a *wrapped
bundle's* standing report should be computed against — the innermost
issuance identity, per P7 — is not decided here; the model treats the
outer artifact as the presented artifact and reports on it. That
re-scoping half is S-P7's (ledger C-4), as the plan and ruling A7 both
say.

**F6 — The reason-code collapse is red by construction, and the record
says so.** Q5's `ReasonCollapsed(PATH_S2, PATH_S3, NO_STANDING)` fires
because two constants were made one; the trace (`.out:1951–1961`) is a
superseded-attempt report and a no-evidence report meeting at the
reason judge. This is evidence about the model's constants — that the
discrimination judge carried in Q1 *can* fail, so Q1's green on it is
not a companion-that-cannot-fail — and about nothing else. The
implementation-level check (S2/S3/S4 pairwise distinct on the reference
verifier's output; a collapsing verifier failing it) is the H1a/P8
S-series vector obligation, unchanged (plan, Vector obligations item 1;
disposition B9's "and the vector obligation stands").

**F7 — The header's load-bearing / carried partition is now a result,
not a prediction, and the carried set is exactly what the plan
predicted inert.** Ablation table above. Two observations a reviewer
should weigh: (a) the anchor-proof binding is inert *because time is not
represented* — the temporal content of SC-1 is entirely ledger C-2 and
no symbolic result here touches it; (b) the well-formedness check is
inert *because no honest issuer signs a malformed TLR and the adversary
holds no honest key* — the probe's F1 shape (`TERM_SHIPPED(a1)` over an
entry reading `DISP_ABANDONED`) needs an honest-but-defective issuer,
which the A1.3 adversary is not; it is a conformance vector
(`STANDING_EVIDENCE_MALFORMED`), and this model's emitting the code only
keeps the vocabulary complete. The envelope path is carried whole and
never queried; its `Accept`/`AcceptS` events are emitted by its code but
are neither queried nor shown reachable in any `.out`, and no result
here depends on them (F2).

## Cross-family falsification review (2026-09-06) — dispositions applied

The agreement-gate review required by `formal/suite/ENUMERATION.md`
amendment note 5 item 1 ran on 2026-09-06 (OpenAI Codex CLI 0.153.3,
`gpt-6-astra`, sandbox bypassed so the reviewer could run ProVerif on
its own mutants; 101 scratch models for this family). Record:
`docs/reviews/2026-09-06-codex-suite-falsification-s-p1-s-p2-s-p7-s-standing.md`
— consolidated findings and collaborator dispositions, items 1–29; the
verbatim S-STANDING review is in that file and the reviewer's `.pv`
files, prompt and index files are archived under
`proverif/falsification-2026-09-06/`. **No registered query,
prediction or verdict changes.** The reviewer re-ran every committed
model and reproduced every committed RESULT line before mutating.
Dispositions are the AI collaborator's and carry no authority until the
author reads them. What was applied here (item numbers are the
consolidated list's):

- **Items 1–3 (Boundary).** Signature-set operations (A1.3 item 2),
  byte-encoding attacks, and verdict/waiver/policy values are
  UNREPRESENTABLE in this family; each is assigned elsewhere (S-P2, P8
  and the library's `h`/`fp` idealization, P4). Stated in the corrected
  `.pv` headers of Q1 (both variants) and Q1d, and in
  `READING-AIDS.md` §0.3. The reviewer's phrase for the byte-encoding
  cell — "a coverage failure, not an unreachable attack" — is adopted
  verbatim.
- **Item 4 (Accepted).** "Inert" is a fixture/query observation, never
  permission to remove a check: single removals do not license joint
  removal, and inertness flips under composition (item 27). Every
  header sentence naming a check whose single removal is green was
  reworded to "load-bearing jointly with …" or moved to "carried",
  citing the reviewer's single-removal matrix
  (`proverif/falsification-2026-09-06/scratch/dependency-index.txt`).
- **Item 6 (Recorded).** The N1 witness is existential: reachable with
  a trace in all seven models, but reachability for one honest key is
  not reachability per branch or per key. N1 is a vacuity guard, not
  coverage.
- **Item 24 (Boundary, expected).** An honestly ENROLLED
  adversary-owned issuer (reviewer fixture `a_own_registered_key`: its
  own tuple evidenced by both channels) falsifies the *unrestricted*
  correspondence (i) while both per-honest-key correspondences (ii) and
  the entitled-key sentence (iii) hold. An honestly registered issuer
  *is* an issuer; (ii) is the claim and (i) is what this fixture adds.
  Stated in the Q1 D/R headers. This is the S-P3/S-P1 pattern, not a
  defect.
- **Item 25 (Accepted).** Terminal-disposition checks are
  safety-inert: removing the terminal predicate while keeping the
  per-entry `d = DISP_SHIPPED` check leaves (i)–(iii) green and loses
  only the S2/S4 vocabulary witnesses. Q4's "LOAD-BEARING for the red:
  the removed terminal check" was a causal overclaim — the mutant
  removes both checks and rearranges the fixture. D/R/G/Q4 headers, F1
  above, and `READING-AIDS.md` §1b/§6d reworded; the terminal check is
  load-bearing singly for the S2/S4 *vocabulary*, which is what SC-3
  registers.
- **Item 26 (Accepted).** Q2's wrapper sentence was narrowed to what
  its committed trace shows, and an unregistered post-freeze companion
  query was added so the literal A7 transplant is exhibited rather than
  inferred. See the next section.
- **Item 27 (Recorded).** The TLR domain tag is inert in this family's
  fixture and load-bearing under composition: with an honest
  REFUSAL-tagged signer over a TLR-shaped body added (reviewer fixture
  `a_foreign_tag`), removing only the tag check turns the strict
  correspondence red. Recorded as a dated note on the D-6 entry in
  `formal/suite/lib/tessera_theory.pvl` (comment only). Because the
  library text changed, the eight S-P3 models were re-run against it
  into a scratch path and their RESULT lines diffed: **all eight
  identical, no warnings** (no S-P3 `.out` was touched).
- **Item 28 (Recorded).** `kT = kX` — the presented key equals the TLR
  key — is required by no registered text; it is a fixture-shape
  restriction inherited from the standing probe (`tlr.pub =
  core.pub`), kept so Q3's registered mutation is a *removal* from the
  correct form. Said in the D/R/G headers and `READING-AIDS.md` §1b.
- **Item 29 (Boundary).** Unrepresentable here and assigned elsewhere:
  the combined report (standing alongside the P4 verdict for one
  request) — the capstone; policy non-rewriting — P4; relying-party
  recording — the relying-party story; temporal replay against the
  anchor — the A2.1 bridge (ledger C-2). A3 §A3.7's adjacent
  obligations (retention, verified handoff, delivery expiry,
  disclosure/minimization) were never this family's target and are
  listed as such in `READING-AIDS.md` §0.3.

**Pending author ruling (ROUTED C10) — item 23, alias replay.** The
reviewer's `a_alias_replay` fixture is reachable with all registered
queries green: a core issued under identity A, with its honest TLR, is
accepted for standing under a second honestly published tuple naming
the same key with identity B, because the standing path binds the key
to the *presented* tuple and never binds that tuple to the core's
*embedded* tuple (the envelope path does). **Nothing has been applied
for this item.** If the author rules yes, the standing path would gain
a check of the presented tuple against the core's embedded tuple —
ENUMERATION note 4 item 2's principle (no reliance on the envelope)
applied to the tuple as it already is to the key — with an alias
companion, recorded as a post-freeze query addition; if the author
rules no, standing is per key and not per identity, and the
relying-party story must say that an issuer with two identities on one
key has one standing lineage. See
`formal/suite/ROUTED-2026-09-06.md` §C item C10.

## Post-freeze additions (unregistered)

One query was added after the plan froze at `5188e7a`. It is **not** a
registered prediction and is recorded here as an addition, in the S-P3
precedent (an added companion recorded as such).

1. **Q2 — the literal A7 wrapper transplant, bound to the honest
   shipped core** (`ss_q2_companionA_identity_declared.pv:189–190`;
   added under cross-family falsification review item 26). The
   registered A7 query `EstablishedWrapped ==> Designated` constrains
   only the wrapper *shape*, and its committed trace
   (`.out:1166–1176`) uses arbitrary inner and outer values. The added
   query requires a single trace in which the wrapper's inner value is
   a core the honest issuer designated as shipped:

   ```
   query k: pkey, t: bitstring, inner: bitstring, outer: bitstring;
     event(EstablishedWrapped(k, t, h(wrapCore(inner, outer))))
       && event(Designated(k, h(inner))).
   ```

   Required REACHABLE. Observed, `ss_q2_companionA_identity_declared.out:2685`:

   ```
   RESULT not (event(EstablishedWrapped(k,t_3,h(wrapCore(inner_1,outer_1)))) && event(Designated(k,h(inner_1)))) is false.
   ```

   The trace (derivation `.out:2362`, trace `.out:2684`) has `inner` =
   `attemptCore(m2, sign((POSS,m2),skH2), sign((BYTES,…),skH2), decl2)`
   — the very core `skH2` fired `Designated` for — `outer` = an
   adversary-chosen `a_12`, the honest TLR of `skH2` as standing
   evidence, and `lbl = LBL2`. It is evidence **only against the
   label-bound companion** and discharges nothing of the property; the
   correct form rejects the same presentation at the lineage lookup by
   `h` injectivity (F5). The other twelve RESULT lines of Q2 are
   unchanged by the addition (re-run and diffed).

## Ledger entries (A3.3 conservation fields) — offered, not entered

1. **P-1 — Standing relation (producer: Q1 (i)/(ii), both variants,
   `Established ==> Designated` true; N1 reachable).** Assumed fact for
   consumers: an `ESTABLISHED` standing report computed against an
   honest entitled key `kH` for an artifact with derived identity
   `aid` implies the issuer holding `kH` signed one TLR whose lineage
   contains `aid` and whose terminal designates `aid`. Consumers: the
   A3.8 base assessment's `protocol_standing` dimension; the
   relying-party story ("what a bundle presented alone establishes");
   the integrated adversarial lifecycle model (A3.9, pre-H1a-freeze),
   which must reproduce this at the seam with wrapping; S-P7's
   innermost-identity claim. Shared terms: entitled key, derived
   identity `h(core)`, TLR. Adversary at the join: A1.3 with DSKS
   expressible (D-4), one of two channels compromised (both variants),
   possession free. Severing companions: Q2 (identity declared) →
   (i)/(ii) red; Q4 (terminal unchecked) → (i)/(ii) red; ablation abl6
   (TLR unsigned) → red. Residual Layer 2: `h` injectivity — **the
   whole load of the transplant result**; `fp` injectivity; P8's "what
   bytes are the core" and their canonical encoding (C-3); deterministic
   signatures (conservative for the judge); lineages of exactly two
   entries (n = 2 does not generalize).
2. **P-2 — Entitled key inside the standing path (producer: Q1 (iii),
   `StandingUnentitled` unreachable, both variants and Q1d).** Assumed
   fact: `Established(kX, t, aid)` implies `fp(kX) = kfpr(t)` for the
   evidenced `t`. Consumer: the H1a conformance profile (the blind
   re-scoring's note, ENUMERATION note 4 item 2, becomes a checked
   shape). Severing companion: Q3 → `StandingUnentitled` red. Residual:
   `fp` idealization (library header); S-P3 ledger entry 1 for what
   "the evidenced tuple names the key" rests on. Shared terms: the
   accepted standing key `kX`; the evidenced tuple `t` (its `kfpr`
   field). Adversary at the join: A1.3, one of two channels compromised
   (both strict variants) and, for Q1d, the sole channel compromised;
   DSKS expressible (D-4); possession free. *(Fields added 2026-09-06,
   skeptic review finding 1 — A3.3 conservation form.)*
3. **P-3 (degraded; a boundary, not a guarantee) — what survives the
   sole compromised channel (producer: Q1d (ii), (iii)).** Assumed
   fact: in degraded mode with the sole channel compromised, no
   `ESTABLISHED` is computed against an honest key for an identity that
   key's holder did not designate, and none against a key the presented
   tuple does not name; the unrestricted sentence does **not** hold
   (Q1d (i) red) and is the A4.6 cost. Consumer: the relying-party
   story's degraded-mode paragraph. No severing companion is owed for a
   cost. Residual: as P-1. Shared terms: honest entitled key; presented
   tuple; derived identity `h(core)`. Adversary at the join: A1.3 with
   the *sole* authority channel compromised — a fixture strictly
   stronger than item 6's "proper subset" (S-P3 F6); DSKS expressible;
   possession free. *(Fields added 2026-09-06, finding 1.)*

**Consumer entries (assumes-from-elsewhere):**

- **C-1 — Key-binding relation** from S-P3 ledger entry 1 (producer
  S-P3 Q2, `Reattributed` unreachable; severing companion S-P3 Q3).
  Assumed here: the artifact's bytes belong to the key the evidenced
  tuple names; the envelope path carries S-P3's checks verbatim and
  this model does not re-prove them. Shared term: the key the evidenced
  tuple names, and the artifact's framed bytes. Adversary at the join:
  as S-P3 Q2 (sole channel compromised, DSKS expressible, possession
  free). Residual Layer 2: S-P3 entry 1's list — `fp` collision
  resistance and what a fingerprint hashes (P8); `h` idealization for
  the manifest hash; deterministic signatures; frame layout (P8); the
  verification profile (P3's [assumption] half, H1a). *(Fields added
  2026-09-06, finding 1.)*
- **C-2 — TLR anchor temporal validity (cross-formalism; never
  symbolically discharged).** Producer: the A2.1 predicate as modeled
  in the P5c bridge family, applied per SC-1 to the TLR's own anchor
  against `declTerminal`. Shared term: "anchor valid". Assumed here: a
  TLR reported `ESTABLISHED` passed that predicate. The symbolic model
  represents no time; its anchor-proof check is inert (abl2) and its
  `STANDING_EVIDENCE_TEMPORAL_MISMATCH` code is vocabulary only.
  Whether SC-1 needs its own TLA+ instance is the coverage map's open
  cell (row 13; disposition B8). **Must never be marked discharged by
  anything in this directory** (ENUMERATION §4 red-bar; Sol finding
  2). Adversary at the join: A1.3 item 5 (the adversary anchors
  anything; anchoring proves existence at a time, not authority); time
  is not represented here. *(Field added 2026-09-06, finding 1.)*
- **C-3 — Canonicalization injectivity and the core's byte
  composition** (P8). Assumed here: two distinct attempts have distinct
  cores and the verifier reconstructs the core bytes exactly;
  `attemptCore(t, ppf, sg, decl)` is a perfectly parsed 4-tuple, not a
  byte format. Shared term: the core bytes and their digest `h(core)`.
  Adversary at the join: A1.3 item 1 (alters any bytes after issue).
  Residual: Layer 2 — unclaimed (canonical encoding and the core's byte
  composition; P8). *(Fields added 2026-09-06, finding 1.)*
- **C-4 — Type soundness of the TLR object and of wrappers** (P7 /
  S-P7; Amendment 4 §A4.5). Assumed here: a TLR is never accepted as
  another object type (the library's `TLR` tag is checked, `OT_TLR` is
  declared but not exercised); a wrapped bundle's standing is evaluated
  against the innermost issuance identity (F5 boundary). This model
  exhibits the identity-binding half; the re-scoping half is S-P7's.
  Shared term: the `TLR` domain-separation tag and the object type
  (`OT_TLR`, declared and unexercised). Adversary at the join: A1.3
  item 4 (re-frames objects across the P7 type boundaries). Residual:
  Layer 2 — unclaimed until S-P7. *(Fields added 2026-09-06, finding
  1.)*
- **C-5 — SC-2's one-signing-act commitment** (`DECISION.md` R2).
  Assumed here: the TLR's terminal disposition *is* the disposition
  fact the A3.7.2 refusal record also projects. Not modeled; the A3.9
  refusal-decomposition obligation (TLA+). Shared term: the terminal
  disposition. Adversary at the join: none symbolic (a specification
  commitment, not an attack surface here). Residual: Layer 2 —
  unclaimed until the A3.9 TLA+ obligation. *(Fields added 2026-09-06,
  finding 1.)*

The discharge matrix (consumer entry → producer query → severing
companion → expected red) is written when the capstone exists
(ENUMERATION §3's own rule).

## What S-STANDING does not discharge

- Equivocation by the entitled key (G4; probe F3): two TLRs under one
  key are each valid here; the fixture even replicates both lineage
  shapes under each key, and (i) still holds because `Designated` is
  per identity. Confined, not closed, exactly as the construction's
  boundary states.
- Anything temporal (C-2). Anything about malformed standing evidence
  beyond emitting the code (vector). Anything about the implementation's
  reason codes (vector; F6). P7's re-scoping question (C-4). P8's byte
  questions (C-3). TLR/refusal-record consistency (C-5). Lineages of
  other than two attempts. The envelope (P4) verdict, carried and not
  queried. In degraded mode, the unrestricted sentence (F2).
- Whether the degraded verdict is *marked* degraded (§A4.6's proviso).
  That is P4's obligation (§A1.2.1 explicit-policy logic;
  cross-formalism, carried here and not checked): this model's envelope
  path fires the degraded-shape event `AcceptS`, which is neither
  queried nor shown reachable in the `.out`; §A4.6's proviso is assumed
  to be met by P4, not shown here. If a reachability witness for
  `AcceptS` is wanted, it is a registered addition for a later run, not
  a recut of this one. *(Added 2026-09-06, skeptic review finding 2.)*
- Unrepresentable in this family, and assigned elsewhere
  (cross-family falsification review items 1–3, 29): signature-set
  operations — stripping, duplication, reordering (A1.3 item 2; one
  signature slot per object here; S-P2's subject); byte-encoding
  attacks — non-canonical encodings, hash-input ambiguity, cross-kind
  parse confusion (term equality stands in for byte equality; P8's
  injectivity obligation and the library's `h`/`fp` idealization; a
  coverage failure, not an unreachable attack); verdict values, waiver
  records and policy inputs (P4); the combined report joining standing
  and the P4 verdict for one request (the capstone); policy
  non-rewriting (P4); relying-party recording (the relying-party
  story); temporal replay against the anchor (the A2.1 bridge, C-2).
  A3 §A3.7's adjacent obligations — retention, verified handoff,
  delivery expiry, disclosure/minimization — were never this family's
  target. *(Added 2026-09-06, cross-family falsification review.)*
- The *unrestricted* correspondence (i) beyond this fixture
  (cross-family falsification review item 24): (i) holds here because
  every honestly evidenced tuple in the fixture names an honest key. An
  honestly enrolled adversary-owned issuer falsifies it while (ii) and
  (iii) hold. The per-honest-key form (ii) is the claim.
  *(Added 2026-09-06.)*
- Criterion 4's second condition — "a model in this suite under the
  A1.3 adversary, before Band 0 exit" — is **not** claimed satisfied by
  this file. The model exists and its tool passes are as registered;
  the cross-family falsification review (the gate, ENUMERATION note 5
  item 1) **has now run** (2026-09-06; see the section above) and its
  results survived it, but the author has not read the correct models
  or the narrowed headers. *(Updated 2026-09-06.)*

## Status toward discharge

Tool passes: **yes** — both correct strict variants green on every
registered query; Q1d green on (ii)/(iii)/(iv) and red on (i) as
registered; all four companions red on exactly their named queries and
green on the rest (table above; the Q4 witness unreachabilities and the
Q5 witness restatement are consequences of the mutations, stated in
each header). Every run ≤ 1 s. No warnings.
Falsification review (cross-family, the gate): **RUN 2026-09-06**
(Codex, `gpt-6-astra`; record
`docs/reviews/2026-09-06-codex-suite-falsification-s-p1-s-p2-s-p7-s-standing.md`).
Outcome: the *results* survived — every committed RESULT line was
reproduced before mutating and no registered query, prediction or
verdict changed; the *self-description* did not — roughly a dozen
header and results sentences were narrowed (items 1–6, 24–29 above).
One design question is routed and unruled (C10, item 23).
*(Updated 2026-09-06.)*
Author read of the correct models and of the narrowed headers:
**pending** (ROUTED C5).
`checked` for the standing invariant therefore still waits on the
author. *(Added 2026-09-06.)*
Reading aids (note 5 item 2, testimony, not gating):
`READING-AIDS.md`, drafted; lower-ceiling reader probe **not run**.
Recommendation (collaborator): the cross-family falsification review
recommended above was dispatched and has run (2026-09-06); nothing in
`formal/PROPERTIES.md` moves on this file. *(Updated 2026-09-06; the
sentence replaced read "dispatch the cross-family falsification review
on `ss_q1_strict_dns_compromised.pv` and
`ss_q1d_degraded_compromised.pv` with the library, the plan, A3.7.1's
text, A1.3, and the ablation directory".)*

## ROUTED TO AUTHOR

One item is routed *(added 2026-09-06 after the skeptic review, finding
3; the paragraph as first drafted read "Nothing in this run produced a
genuine fork")*:

1. **Confirm that `5188e7a` is Amendment 4's signing commit.** The
   amendment's status line (`docs/phase-0-prereg-amendment-4.md` lines
   3–4) still reads "DRAFT — adopted in session, not yet signed" and the
   document carries no dated signing note; a dated note there is the
   author's to add. This record and the library's D-6 entry read the
   author's commit plus its OTS stamp (`5dfd82b`) as the signing act.
   Ruling A6 makes the TLR tag's location depend on signature, so the
   reading is load-bearing: if `5188e7a` is not the signing commit,
   every S-STANDING model's use of the library `TLR`/D-6 tag is a
   divergence from the frozen plan and the tag must be recut
   model-local per A6 (seven models, six ablations and `run1/`, with a
   full re-run).

The three rulings the plan carried (A6, A7, A8) were otherwise executed
as entered; the two dispositions (B8, B9) were followed as listed for
veto. Items a reader may expect to see routed, and why they are not:

- *Whether Q5's box is registered.* Assigned the companion box by the
  collaborator; the run took 1 s; a box ruling would change nothing.
- *`wrapCore` in every model rather than Q2 only* (divergence entry 2).
  An encoding choice within A7's "minimal constructor"; recorded, not
  routed.

## Review log

- 2026-09-06 — models built from the frozen plan by the AI
  collaborator; one development-time recut (lookup destructor,
  reserved-identifier rename; results unchanged; pre-recut archived
  `proverif/run1/`); registered ladder run once, all seven outcomes on
  their predicted branches; six scratch ablation probes run after the
  ladder (`proverif/ablations/`); this file and `READING-AIDS.md`
  drafted. No non-author replication, no falsification review, no
  author read.
- 2026-09-06 — **build completed in two agent sessions.** The first
  session built the seven models, ran the ladder and the ablations, and
  drafted this file and `READING-AIDS.md`, then was cut off by a usage
  limit before returning its summary. The second session (same day, AI
  collaborator) did not rebuild: it inventoried the directory; re-ran
  all seven ladder models, the six ablation probes and the `run1/`
  archive against the library with `-lib`, into scratch, and compared
  `RESULT` lines to the committed-candidate `.out` files — **every line
  identical, no warnings** (the `run1/` output reproduces its one
  recorded `identifier sid rebound` warning); no `.out` was overwritten
  and no recut was needed. Spot-checked every `file:line` citation in
  `READING-AIDS.md` §§0–7 and the trace citations in this file's ladder
  table against the `.pv`/`.out` files: all as cited. Checked the frozen
  plan's registered items against the directory — SS.Q1 both variants,
  SS.Q1d, SS.Q2 with the A7 wrapper constructor and second trace, SS.Q3
  (entitled key inside the standing path; envelope-only companion red),
  SS.Q4 (terminal disposition), the B9 collapsing companion (Q5), the N1
  judge-emitted witness in all seven, the five vocabulary witnesses,
  the A6 library `TLR` tag with no redeclaration, the A8 §A4.6 quotation
  — **no registered item is without a model**; no new divergence to
  record. One completion: the Q5 header lacked the "LOAD-BEARING /
  carried" line the suite's header form requires; one comment line was
  added in place of a blank comment line (line count unchanged, no
  citation shifted), and Q5 was re-run: `.out` byte-identical. Facts a
  reader should hold: `PREDICTIONS.md` is unchanged from `5188e7a`
  (`git diff` empty); the library's D-5/D-6 entries were **uncommitted**
  in the working tree at the time of both sessions' runs, so every
  `.out` here is evidence against that working-tree library and the
  author's commit of the library is what makes them reproducible from
  history. Still no non-author replication, no falsification review, no
  author read.
- 2026-09-06 — **skeptic review of S-STANDING applied** (findings
  returned as verified; applied by the AI collaborator, STATUS:
  PROPOSED). Three defects and three nits. (1) Ledger entries P-2, P-3,
  C-1–C-5 lacked A3.3 conservation fields (`docs/phase-0-prereg-
  amendment-3.md` lines 232–236: shared term, adversary at the join,
  residual / "Layer 2 — unclaimed"); the fields were **added as
  labelled sentences** at the end of each entry, nothing removed. (2)
  F2, the Q1d header and `READING-AIDS.md` §3d asserted "the verdict
  says degraded" on the strength of an event (`AcceptS`) that no query
  mentions and no trace exhibits; reworded in all three places to
  "P4's obligation, carried and not checked; assumed, not shown", and
  a bullet added under "What S-STANDING does not discharge". No model
  was recut; an `AcceptS` reachability witness, if wanted, is a
  registered addition for a later run. (3) Divergence entry 1 said
  "Amendment 4 was signed at `5188e7a`"; the amendment's own status
  line still reads "DRAFT — not yet signed" with no dated signing
  note, so the entry now states the basis (author's commit + OTS stamp,
  read as the signing act) and ROUTED TO AUTHOR gains item 1. (4)
  Author-decision grammar in `.pv` headers (Q1 both variants, `run1/`,
  `ablations/abl1–6`, Q2, Q1d) carried no file citation for the ruling;
  citations added **as comment-only edits with every file's line count
  unchanged** (the blank comment line following each edited block was
  consumed, the Q5 precedent), so no `READING-AIDS.md` `file:line`
  citation shifted. All fourteen models were then re-run with `-lib`
  under the registered boxes (`run_ladder.sh` → `ladder.log`;
  `ablations/ablations.log`; `run1/` from its own directory): **every
  `.out` byte-identical to the pre-edit output** (`cmp`), `run1/`
  reproducing only its recorded `sid` warning; the `.out` files and the
  two logs were refreshed in place (the logs differ only in the 0/1 s
  timings). Not a recut: no query, process, or result changed. (5) F3
  and F5 presented code inferences as checked results; each now says
  "by inspection" / "by `h` injectivity" and names what the queried
  witness actually exhibits (Q1 `.out:1927`: core `a_4`). (6) Citation
  imprecisions in `READING-AIDS.md` (lib `150–157` → `151–157`; Q2
  `.out` `628` → `626`, `1174` → `1172`; Q1deg `.out` `1096` → `1094`,
  restatement lines noted) corrected. Not applied: the nit's pointer at
  `READING-AIDS.md` §4d line 439 — that line carries a boundary
  statement, not a claim about an unexhibited trace; nothing to mark.
  Still no non-author replication, no cross-family falsification
  review, no author read.
- 2026-09-06 — **cross-family falsification review applied** (the
  agreement gate, ENUMERATION note 5 item 1; reviewer OpenAI Codex CLI
  0.153.3, `gpt-6-astra`, 101 scratch models for this family; record
  `docs/reviews/2026-09-06-codex-suite-falsification-s-p1-s-p2-s-p7-s-standing.md`,
  scratch archived `proverif/falsification-2026-09-06/`). Applied by
  the AI collaborator, STATUS: PROPOSED; dispositions carry no
  authority until the author reads them. **The work was done in two
  agent sessions: the first was cut off by a usage limit part-way
  through and the second inventoried the directory before touching
  anything and applied only what was missing.** The complete list of
  changes, in the order a reader can check them:
  1. *`.pv` header corrections (first session).* Q1 DNS and Q1 repo
     each gained a dated `CORRECTION 2026-09-06 (cross-family review
     item 24)` block (the unrestricted sentence (i) is fixture-bound)
     and a `(items 1-3)` block (signature sets, byte encodings,
     verdicts unrepresentable), and their LOAD-BEARING / CARRIED lists
     were rewritten in place against the reviewer's single-removal
     matrix (items 4, 25, 27, 28), each rewrite naming the sentence it
     narrowed. Q1d gained the same items 1–3 block and the same
     rewritten list. Q4 gained an item 25 block and its two overclaiming
     lines were narrowed in place. Q2 gained an item 26 block. Q3 and
     Q5 were not edited.
  2. *One post-freeze UNREGISTERED query (first session)*, added to Q2
     under item 26 and recorded above under "Post-freeze additions
     (unregistered)" with its RESULT line — never as a registered
     prediction.
  3. *Library (first session).* A dated note was added to the D-6
     entry of `formal/suite/lib/tessera_theory.pvl` under item 27
     (the TLR tag is inert in every single-family fixture and
     load-bearing under composition). Comment only; no declaration
     changed.
  4. *Runs (first session, re-verified by the second).* All seven
     models were re-run with `-lib` under the registered boxes
     (`run_ladder.sh` → `ladder.log`) after the edits. The second
     session re-ran all seven again into a scratch path and compared:
     **every committed `.out` is byte-identical to a fresh run, no
     warnings**, so every `.out` in this directory is current for the
     `.pv` text beside it. Q2's twelve pre-existing RESULT lines are
     unchanged by the added query; the added query's RESULT line is the
     thirteenth, quoted above. The six ablation probes and `run1/` were
     not edited and were not re-run.
  5. *S-P3 re-verification (second session, item 27's obligation).*
     Because the shared library's text changed, the eight S-P3 models
     were re-run with `-lib` into a scratch path and their RESULT lines
     diffed against the committed `.out` files: **all eight identical,
     no warnings.** No file in `formal/suite/s-p3/` was written.
  6. *This file (second session).* F1's load-bearing list narrowed
     (item 25) and F5's wrapper sentence narrowed (item 26), each
     quoting what it replaced; two stale `.pv:` citations repaired
     (item 7 below); new sections "Cross-family falsification review
     (2026-09-06) — dispositions applied", carrying items 1–6 and
     24–29 and the **Pending author ruling (ROUTED C10)** line for item
     23, and "Post-freeze additions (unregistered)"; three bullets
     added to "What S-STANDING does not discharge" (items 1–3, 24, 29);
     "Status toward discharge" updated — the gate has now run.
     **Item 23 (ROUTED C10, alias replay) was NOT applied**: no query,
     process or header changed for it, and the pending line states only
     what would change under either ruling.
  7. *Citation repair (second session), `READING-AIDS.md` and this
     file.* The first session's header blocks lengthened five `.pv`
     files, which shifted every body line and so **invalidated every
     `file:line` citation in `READING-AIDS.md`** — the convention this
     family had kept until then (skeptic-review entry item 4: comment
     edits consume a blank comment line so no citation moves) was
     broken. The offsets were established by diffing each model against
     the reviewer's archived mutants, which carry the pre-edit text
     (`proverif/falsification-2026-09-06/scratch/m_dns_anchor.pv`,
     `m_repo_anchor.pv`, `m_deg_anchor.pv`; the body diff in each case
     is the single mutated line, so the bodies are unchanged): Q1 DNS
     +32, Q1 repo +32, Q1d +23, Q4 +12, Q2 +11 before its added query
     and +20 after it, Q3 and Q5 unchanged. The library's D-6 note
     shifted its own declarations by +11. Every `.pv` and `lib`
     citation in `READING-AIDS.md` §§0–8 and the two in this file were
     remapped by those offsets and spot-checked against the files
     line by line. `.out` line numbers did not move (ProVerif does not
     echo comments) and were left alone; the added Q2 query appends
     after every existing `.out` citation. **The historical review-log
     entries in both files were left as written** — they record what
     was checked against the then-current text, and rewriting their
     numbers would falsify that record.
  8. *Count and witness-scope repair (third session, skeptic review of
     the second session's application), `READING-AIDS.md` and this
     file.* Two arithmetic/scope errors inside sentences that record a
     verification were corrected; no `.pv` text changed, so nothing was
     re-run and no `.out` moved.
     (a) **Q2's RESULT-line count.** `ss_q2_companionA_identity_declared.out`
     carries **thirteen** RESULT lines — twelve pre-existing (`.out`
     630, 808, 986, 1176, 1182, 1514, 1692, 1868, 1996, 2170, 2346,
     2352; the registered A7 query at 1176 was the one missed) plus the
     post-freeze addition at 2685. F5's closing sentence read "The other
     eleven RESULT lines of Q2 are unchanged by the addition" and item 4
     above read "Q2's eleven pre-existing RESULT lines are unchanged by
     the added query; the added query's RESULT line is the twelfth";
     both now read twelve and thirteenth. The verification they record
     is unaffected — the committed `.out` is still byte-identical to a
     fresh run — only the count was wrong.
     (b) **§1b row `282–283`, single-removal scope.** The row read
     "**singly for the S2/S4 vocabulary** (SC-3) … loses the S2 and S4
     witnesses (reviewer matrix 19, 20)", which claims more
     witness-dependence than the matrix supports — the same class of
     over-claim item 25 exists to narrow. Reviewer matrix line 19
     (`terminal_identity`) *is* the removal of exactly that row's check
     (the body diff against the committed model is the single line
     `if shippedId = aid` → `if true`) and its vector is `TTTTFFTFFFT`:
     slot 7 (S2, `ABSENT`/`SUPERSEDED`) is true, the witness lost, but
     slot 9 (S4, `ABSENT`/`ISSUANCE_REFUSED`) is still false, the
     witness reachable. Matrix 20 (`terminal_predicate`) loses both, but
     that mutant removes **all** terminal decisions including the
     `TERM_REFUSED` branch, which §1b carries as the separate row
     278–280; the S4-only loss is matrix 22 (`refused_branch`,
     `TTTTFFFFTFT`). The row now reads "singly for the S2 vocabulary …
     loses the S2 witness (reviewer matrix 19)" and names matrix 20 and
     22 for the two wider removals. Vectors read from
     `proverif/falsification-2026-09-06/scratch/dependency-index.txt`
     lines 19, 20, 22. **The `D`/`R` headers were left alone**
     (`ss_q1_strict_dns_compromised.pv:75`,
     `ss_q1_strict_repo_compromised.pv:77`): they cite both matrix rows
     without the word "alone", which is defensible as written, and
     editing a `.pv` would oblige a re-run and `.out` refresh for a
     comment.
  9. *Cross-family defect found, not repaired here.* Item 27's dated
     note (entry 3 above) added **11 comment lines** to the library's
     D-6 entry, so every declaration below it moved +11 — entry 7
     remapped this family's `lib:` citations but flagged the siblings'
     as unchecked. They are stale: `s-p1/READING-AIDS.md`,
     `s-p2/READING-AIDS.md` and `s-p7/READING-AIDS.md` each cite the
     pre-note numbers (e.g. s-p1:82 `checksign` at `lib:100–104`, now
     111–115; s-p1:80 `fp` at `lib:117`, now 128). Those are not
     S-STANDING files and were **not** edited from here; the remap
     (+11, with post-note anchors `sign` 109, `dsks` 110, `checksign`
     111–115, `fp` block 118–128, `h` block 130–142, `STMT_DIRECT` 149,
     `TLR` 154, `OT_ATTEST` 161, `authTuple` 175, `Accept` 194) is
     reported to those families. S-P3's `lib:` citations are stale by a
     different and larger amount, from the earlier uncommitted D-5/D-6
     declarations rather than from this note.
  Not applied, with reasons: item 23 (ROUTED C10 — the author has not
  ruled; pending line only, as above); items 5 and 7–22 (other
  families, or not applicable to S-STANDING). `PREDICTIONS.md` is
  FROZEN and was not touched (`git diff` empty against `5188e7a`).
  Still no author read; `checked` for the standing invariant waits on
  it (ROUTED C5).
