# Band 0 exit — the finite list

> **STATUS: PROPOSED — 2026-09-13 — drafted by the AI collaborator (Claude,
> Fable 5.1, owner instance for sequencing and mechanics); not adopted; the
> commit is the author's.** This file enumerates every condition the signed
> record places on Band 0 exit, with its source, its state in the tree today,
> and what remains. It registers nothing and discharges nothing: the
> authoritative texts are the pre-registration and its amendments, and if
> this file and an amendment disagree, the amendment wins and the
> disagreement is a defect here. Status values are copied from
> `formal/PROPERTIES.md` (TRK), which wins over this file too. Readings the
> clerk had to take to make the list finite are collected in §5 so they can
> be vetoed in one place. Amend-don't-rewrite applies from this file's first
> commit.

**Why this file exists.** The author has been pushing to close Band 0 since
early September and said on 2026-09-13 that the obstacles do not seem to
be going away. The record contained the exit conditions but not in one
place; the same session's owner instance found them across `phase-0-prereg.md`
§8, Amendment 1 §A1.4/§A1.7, Amendment 3 §A3.1/§A3.3/§A3.6/§A3.7/§A3.9,
Amendment 4 §A4.4, the first-link spike's panel criteria, the TRK's
cross-cutting boxes, and the first-link residual's corrected closing
condition. A push needs a target. This is the target, and it is meant to
shrink, not grow.

## 1. The gate as registered

`docs/phase-0-prereg.md` §8, three clauses, each since read by amendment:

- **Clause 1 — the machine-checked model exists and the proof holds.**
  Tools per property are fixed by A1 §A1.4 as amended (A4 §A4.1 for P9/P10,
  A6 §A6.1 for P7). The *composition* is machine-checked only by the capstone
  (A3 §A3.3, quoted in TRK): every ledgered cross-model assumption discharged
  by a producer query with a severing companion; Layer 2 exposed and
  unclaimed.
- **Clause 2 — the agreement gate has passed.** A1 §A1.7 hardens it to a
  falsification task by non-author models, plus model-derived conformance
  vectors. A4 §A4.4 and the author's 2026-09-06 scope ruling (recorded in
  `formal/spike/first-link/DECISION.md`, the residual's correction block)
  fix how the author's half is performed: from each model's plain-language
  statement and the cross-family comparator, never from the tool text cold.
  TRK's `discharged` status is this clause per row.
- **Clause 3 — the informal written proof is in the repository.** A4 §A4.4:
  the account *is* the collection of each checked model's plain-language
  statement of claim, adversary, and boundary, carried as a reading aid. Its
  sufficiency for non-expert readers is reviewed, not gated. A1 §A1.4
  separately requires that the written proof include the TLA+ ↔ symbolic
  **correspondence mapping**; A4.4 does not remove that sentence.

Exit is the act of §8's last paragraph: an explicit, dated, signed author
commit declaring the build runway open for Phase 1a.

## 2. The list

Status key: **done** (artifact exists and no registered step remains),
**partial** (artifact exists; a named step remains), **not begun**.
"Author act" marks steps only the author can perform.

| # | Condition | Source | State in tree (2026-09-13) | What remains |
|---|-----------|--------|----------------------------|--------------|
| E1 | Per-property models checked: P1–P7, P10 | A1 §A1.2/§A1.4; TRK | **done** — all eight rows `checked` | nothing for `checked`; see E9 for `discharged` |
| E2 | Standing-evidence model in the suite under A1.3 (panel criterion 4, condition 2) | `FIRST-LINK-SPIKE.md` panel criteria item 4; ENUM note 4; TRK row SC | **partial** — seven models + SS.Q6 run; cross-family reviews run 2026-09-06 and 2026-09-12; author's C5 read YES 2026-09-12; row `open` | owner assesses the row's recorded prerequisites and proposes `checked` (assessment owed, this week); then E9 as for every row |
| E3 | P8 framing proof (injectivity over the accepted domain, boundary-unambiguous frame) | A1 §A1.2 P8 **[proof]**; §A1.4 (Lean4 or rigorous prose); A3 §A3.6.1 (identifier encoding fixed by the proof and golden vectors before exit) | **not begun** — TRK `open`, artifact "—" | (a) criteria-before-evidence decision on the proof's form, DECISION.md pattern, routed to the author; (b) the proof; (c) the golden vectors that fix the frame layout and the identifier encoding (§5 reading b); (d) non-author falsification review; (e) author's plain-language read |
| E4 | P9 statelessness | A1 §A1.2 P9; A4 §A4.1 (**[inspection+vector]**) | **partial** — inputs enumerated (`formal/spike/standing-probe/RESULTS-PROBE.md` Q6); TLA+ probe non-discharging; two-machine vector owed | the inspection artifact written against the enumeration and the P4 module headers (which assume P9); the two-machine vector is specified at Band 0 and *run* at H1a (§5 reading b); author read of the inspection |
| E5 | Capstone composition context with discharge matrix | A3 §A3.3 (verbatim gate); ENUM §3; TRK cross-cutting box 2 | **not begun** — `formal/suite/capstone.pv` absent; every family's ledger entries are "offered, not entered" | (a) enter the ledger entries (five families) with the A3.3 conservation fields; (b) build the capstone transcribing the library; (c) discharge matrix (consumer entry → producer query → severing companion → expected red), every cross-model row green/red as registered; (d) predictions frozen before the run; (e) non-author falsification review; (f) author read |
| E6 | Two registered model obligations with no TRK row | A3 §A3.6.2 item 3 (unknown-algorithm P4 transition + fail-open companion); A3 §A3.9 (§A3.7.2 extended atomic-entry invariant + two companions); COVERAGE-MAP rows 4, 6, 15 flag both | **not begun** — neither modelled, neither tracked | TRK rows added `open` (record fact, PROPOSED); P4 gains the `UNVERIFIABLE`-on-unsupported-identifier transition and a fail-open companion; P5c gains the extended atomic-entry invariant (`REFUSED` ⇒ record + commitment + delivery `PENDING` + publication `PENDING`) with the primary companion (latch while postponing one creation) and the second (`DELIVERY_FAILED` re-entering issuance or decrementing the bound); both red; reading aids updated; review; author read |
| E7 | Prose mapping for every symbolic lemma | A1 §A1.4; TRK box 4 | **partial** — claim blocks and `READING-AIDS.md` exist for all five families; TRK box unchecked | owner verifies each registered query has a mapping sentence naming its A1.2 property; ticks the box or lists the gaps |
| E8 | Cross-model correspondence mapping (TLA+ ↔ symbolic) in the written proof | A1 §A1.4; TRK box 5 | **not begun** — ENUM §4 names the joins; COVERAGE-MAP names the legs | one document mapping each TLA+ transition/invariant to the symbolic rules/events it corresponds to (the `Accept` ↔ P4 partition join for P1/P2; P5/P6 anchor validity as a Layer 2 entry; refusal latch → S-P7/S-STANDING); non-author review; author read |
| E9 | Agreement gate per row: falsification review run **and** the author's plain-language read and adjudication recorded | prereg §8 clause 2; A1 §A1.7; A4 §A4.4; TRK status ladder | **partial** — reviews run: S-P3 (blind, 2026-09-05, author read same day); TLA+ P4/P5/P5c/P6 (2026-09-06); S-P1/S-P2/S-P7/S-STANDING (2026-09-06, 2026-09-12). Author has read S-P3's only. Reading aids exist for all eight modules | one batched read, assembled like `READ-C5-2026-09-12.md`: per family, the review's surviving findings and the plain-language statement, one question each; the author's adjudications entered; rows move to `discharged`. Reviews for E3, E5, E6, E8 once those exist. **Author act** |
| E10 | Model-derived conformance vectors extracted from checked traces | A1 §A1.7 item 2; TRK boxes 6 and 8 (A2.2 cases); docket 30, 32 | **not begun** | vectors extracted at Band 0 from the checked traces (late burial → `INVALID`; headers missing → `UNVERIFIABLE`; the P9 two-machine case; the P7 verdict-independence case; A3.9's refuse-to-ship issuance case); the concretizer reviewed under non-author discipline; *running* them is H1a (§5 reading b) |
| E11 | Informal written proof in the repository | prereg §8 clause 3; A4 §A4.4 | **partial** — the reading aids are the account by A4.4; no single index binds them, and E8 is still owed inside it | one index page listing every model's plain-language statement (claim, adversary, boundary) with links, plus E8; the lower-ceiling reader probe and blind reverse-translation are review, not gate |
| E12 | Relying-party story page | A3 §A3.1 item 4 (registered exit artifact) | **not begun** — not in `docs/` | one page opening with the can/does-not-establish list verbatim from the 2026-07-28 ruling; written inside the implementation specification (docket 31) and also published stand-alone; author read |
| E13 | Coverage map with open cells visible | A3 §A3.1 item 3 | **done** — `formal/COVERAGE-MAP.md`, committed by the author, PROPOSED status retained | refresh its status column when rows move (a defect in the map if it lags TRK) |
| E14 | Parameter ratification: δ = 72h, ε = 24h, k = 6, N = 3 (working defaults) | A1 §A1.2 P5, §A1.6; A2 §A2.1/§A2.3; TRK box 9 | **not begun** — sizing evidence exists (A2's δ argument; bridge slack analysis) | one dated ruling in an amendment or the exit commit's record. **Author act** |
| E15 | First-link residual: closing condition per its 2026-09-06 correction | `first-link/DECISION.md` residual block | **partial** — condition restated: for each symbolic result the decision rests on, the author states claim, adversary and boundary with the record open, and a non-author model checks the statement | those statements exist for S-P3 (2026-09-05 read) and the first-link spike's Q1/Q3/Q4 only partly; the E9 batched read produces the rest. Not an exit blocker by its own terms ("accepted, not waived"), but E9 closes it as a by-product |
| E16 | Implementation specification (the current contract) | docket item 31 — **collaborator-proposed** exit companion, not registered | **partial** — first draft `docs/implementation-spec.md` (2026-09-13; 455 requirements; §11 register, §12 routed contradictions; assembly log in `docs/reviews/`); Codex non-author review run and dispositioned 2026-09-13 (`docs/reviews/2026-09-13-codex-review-implementation-spec.md`, six repairs applied); author read owed: §12 open table and §1.5 | written from the adopted artifacts; contradictions routed, never resolved by the writer; contains E12. Sequenced first because it is the cheapest test of whether the record composes |
| E18 | Confirmation-depth evidence at the registered parameter (Amendment 7 §A7.8, author ruling 2026-09-14): either (a) P5c, P5P6 and bridge re-run at `DepthK = 5` with bounds sized so every registered witness fires, or (b) a non-author-reviewed argument that every checked invariant is independent of `DepthK` above the witnesses' minimum | A7 §A7.8; `formal/tla/READING-AID-P5c.md:226-231` | **not begun** — checked configurations use `DepthK = 2` | owner tries (a) first; falls back to (b) if the state space does not close; result recorded in the family's reading aid and here |
| E17 | The exit act | prereg §8 last paragraph | — | a dated, signed author commit declaring the Phase 1a runway open, after E1–E15 are green and E16 exists. **Author act** |

## 3. Explicitly not on the list

- **The integrated adversarial lifecycle model** (A3 §A3.9, Kimi 2) — gates the H1a freeze, not Band 0 (A3 line ~796: "deliberately NOT a Band 0 exit" obligation).
- **Running the H1a vectors against an implementation** — Band 1; Band 0 extracts and reviews them (E10).
- **The P3 [assumption] half** (verification profile) — H1a evidence by A1 §A1.2; P3 reaches `discharged` on its [model] half read (E9) with the [assumption] half named open.
- **Tending-policy skeleton** (docket 15) — not registered for exit; the docket itself says making it one is a registration change.
- **Higher-assurance signing, hardware tokens, independent human formal review** — deferred by the pre-registration (§4.2, §8) and gated on reliance or revenue.
- **Band 1 docket items** other than 30–32's vector *specifications*.
- **Any weakening of a property** — needs a signed amendment (A1 §A1.1), and none is proposed here.

## 4. Two findings this list surfaced

1. **E6 — two registered model obligations were never entered on the tracker.** A3 §A3.9 says its obligations are "tracked in `formal/PROPERTIES.md` upon adoption"; A3 was adopted 2026-08-09 and neither the unknown-algorithm P4 transition nor the §A3.7.2 extended atomic-entry invariant has a row. The coverage map flagged both on 2026-09-06 (rows 4, 6, 15) as "no TRK line" and nothing followed. Both are small TLA+ additions to modules that already exist. Proposed disposition: add both to TRK as `open` rows now (record fact; PROPOSED) and build them after the capstone.
2. **E9 is the long pole and it is the author's.** Seven review records are unread. The record's own discipline (`never-ask-for-an-unnamed-cold-read`, 2026-09-04 travelog) means the owner assembles one file per sitting with file, lines, question and length stated. The first such file is owed once E3, E5, E6 and E8 exist so the sitting happens once, unless the author prefers two sittings.

## 5. Clerk readings taken to make the list finite (contestable; veto here)

- **(a) `discharged` is the exit status for every row.** §8 clause 2 says the agreement gate has passed; TRK defines `discharged` as tool passes plus agreement-gate falsification review passed; A4.4 says the author's half is the plain-language read. Therefore every row on the tracker, including SC and the two E6 rows, must reach `discharged` for exit, not `checked`. If the author reads §8 as satisfied by `checked` plus one aggregate read, E9 shrinks to one sitting and this reading is withdrawn.
- **(b) Vectors are specified and reviewed at Band 0, run at H1a.** A1 §A1.2 P8 puts the golden vectors and rejection suite at "H1a obligations" and the frame layout "before the Band 1 freeze"; A3 §A3.6.1 says the identifier encoding is fixed "by P8's framing proof and golden vectors before Band 0 exit". Read together: the proof and the vectors that *fix* the layout and encoding exist at exit (they are part of the proof's statement of its domain); executing the suites against code is H1a. The A1.7 model-derived vectors follow the same split.
- **(c) "Offered, not entered" ledger entries do not satisfy A3.3.** The gate text says every ledgered cross-model assumption is discharged; an offered entry is not ledgered. Entering them is the first capstone step (E5a) and is collaborator work with author read of the resulting matrix.
- **(d) Reading aids are the written proof (A4.4), but the correspondence mapping is still owed (A1.4).** A4.4 restates clause 3 without mentioning §A1.4's mapping sentence; amend-don't-rewrite means the sentence stands. E8 is therefore on the list. If the author rules that A4.4 subsumed it, E8 is withdrawn.
- **(e) The relying-party story is one page, published stand-alone.** A3 §A3.1.4 says "one page". Writing it inside the specification and then extracting the page keeps both honest; the specification is not a substitute for the registered artifact.

## 6. Sequencing (owner's call; the author may veto)

1. E16 implementation specification (contains E12) — first, because writing it tests composition and produces the contradiction list the capstone needs.
2. E5a ledger entries entered, then E5b–d capstone built and run under frozen predictions.
3. E3a P8 criteria and form decision (routed), then E3b–c proof and vectors.
4. E6 the two TLA+ additions.
5. E10 vector extraction; E8 correspondence mapping; E11 index page; E7 check.
6. Non-author reviews of 2–5 as each lands (Codex, flat rate; run when needed).
7. E9 one batched author sitting; E14 parameter ruling; E2 row assessment folded in.
8. E17 exit commit.

Model allocation for dispatched work, per the author's 2026-09-11 rule: Opus for builders, skeptics and repairs; Sonnet for clerical extraction and citation checks; Haiku for probes. Each dispatch names its model in the record.

## 7. Routed to the author

2026-09-14: the eleven §12 items were ruled; instrument Amendment 7 (PROPOSED). Nothing blocks today. Two items will be routed when ready: the P8 form decision (E3a, with criteria first) and the E9 sitting. The §5 readings stand unless vetoed; the E6 tracker rows are added as PROPOSED record facts in the same tree change as this file.
