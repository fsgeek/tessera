# Lower-ceiling reader probe — P4 reading aid (2026-09-06)

**STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not
adopted; the commit is the author's.**

Per `formal/suite/ENUMERATION.md` amendment note 5 item 2, in the form
of `formal/spike/first-link/proverif/reading-aid-q3/PROBE-haiku-2026-09-06.md`.
Reader: Claude Haiku 4.5, two fresh contexts; condition 1 given the
comment-stripped `P4_VerifierStates.tla` only, condition 2 given
`formal/tla/READING-AID-P4.md` (Parts A and B) plus the module. Same
three questions both times: the claim (the quantity judged and the
registered sentence it supports), the adversary (and the load-bearing
initialization line), three boundaries. Graded by the AI collaborator
against `READING-AID-P4.md` and the review record
`docs/reviews/2026-09-06-codex-tla-falsification-p4-p5p6-p5c.md`
(items 1–7, lines 54–101; reviewer output lines 210–307). Line numbers
into `READING-AID-P4.md` below, and in the condition-2 answer, are
those of the aid **as the reader saw it**, before the Probe result
paragraph was inserted after the provenance block (which moved every
later line down by 21: Boundaries 199→220, Plain-language 228→249, Part
B "does not show" 345→366).

## Condition 1 — comment-stripped module only

- Claim: **partial.** The four-branch classification is right (required
  fail → `INVALID`; required unperformable → `UNVERIFIABLE`; all
  required pass → `VALID_STRICT` with no waivers, `VALID_DEGRADED` with
  a nonempty waiver set). Two errors of scope: it said "all outcomes
  under all policies" with **no finite-instance bound** — never named
  the configured instance (five checks, two non-waivable) or the 1944
  states (`P4_VerifierStates.out:34, 39`; reviewer 293: "exhaustive
  within that instance, not a demonstrated result for arbitrary set
  sizes"), and "all policies" is legal policies only (`Init` line 79).
  The registered sentence it named — "A REQUIRED check that cannot be
  performed yields `UNVERIFIABLE`" — is the §A4.2-qualified sentence
  that `NoSilentPromotion` and `ExactUnverifiable` check (aid checks
  table rows 3, 9), not the sentence its own claim paraphrases
  (Amendment 1 `:152–153`, "The verifier's four states partition all
  outcomes", row 1); and it attributed the qualifier to "the 2026-09-06
  correction" rather than to Amendment 4 §A4.2
  (`docs/phase-0-prereg-amendment-4.md:96–105`), where the author wrote
  it.
- Adversary: **partial.** Right that the adversary is any status
  assignment in `[Checks -> Statuses]` and any waiver set in
  `SUBSET Waivable` (reviewer 297), and right that `waived \in SUBSET
  Waivable` (line 79) is the load-bearing initialization line (reviewer
  259; Part B "legal-policy initialization", aid line 333). Wrong gloss
  on why it bears load: it said that without it "the verdict logic
  would collapse". What the record says is the opposite direction — the
  line **excludes** policies naming a non-waivable check from the
  enumeration, so the verifier's rejection or normalisation of such a
  policy is never tested (reviewer 219, 259; aid checks table row 2).
  Cannot-represent list (concrete mapping, bundle, keys, replay, A1.3
  actions) right (items 3, 7).
- Boundary: **three right** — concrete-check correctness and the
  soundness of the `c1..c5` categorisation (item 3; reviewer 237, 296);
  checks executing correctly or resisting bypass (reviewer 221, 294);
  recorded waiver set vs. authorising policy vs. set used at verdict
  time (item 3; reviewer 236, 298). No inversion.
- Confidence: medium. Asked whether the eleven formulas run as one TLC
  check or split into vacuity/safety runs (aid Model paragraph: main
  cfg eleven invariants; `_Sanity` cfg four witnesses with `-continue`),
  and whether the 2026-09-06 correction changed what a clean run
  certifies (aid line 16, header 22–58: no module, cfg or `.out`
  changed; the header was narrowed).
- Note on the input: the answer cites "the 2026-09-06 correction" and
  "the eleven formulas in `P4_VerifierStates.cfg`". A fully
  comment-stripped module carries neither; either the condition-1 copy
  retained the header correction (lines 22–58) and the cfg, or the
  reader inferred them. The probe record does not say which; the next
  probe should archive the exact condition-1 input beside this file, as
  the Q3 probe archived `q3_dns_stripped.pv`.

## Condition 2 — reading aid (`READING-AID-P4.md`) + module

- Claim: **right.** Four-branch classification right; "every legal
  policy within the configured instance" right; **1944 = 3^5 × 2^3**
  right (aid Finite instance, `out:34, 39`); registered sentence
  Amendment 1 `:152–153` "The verifier's four states partition all
  outcomes" right (aid checks table row 1). Quantity named as "the
  verdict function returns exactly one of the four P4 states", which is
  `Partition` alone; the answer then states the other branches, so the
  eleven-formula content is present.
- Adversary: **right.** Any status assignment plus any subset of the
  three waivable checks; load-bearing line named as legal-policy
  initialization with the correct consequence — `Init` excludes
  policies naming non-waivable checks, so no rejection path is tested
  (reviewer 259; aid cast `waived` row, checks table row 2). Cannot
  represent: recording and authorisation of waivers (item 3; reviewer
  236).
- Boundary: **three right** — no concrete check implementations and no
  checked `c1..c5` mapping (item 3; Part B 347); no audit or policy
  validation, illegal waivers excluded not rejected, computed-vs-stored
  verdict mismatch inexpressible (item 3; reviewer 298; Part B 348);
  no attacker, replay, network, changing-policy trace, or
  arbitrary-size theorem (item 7; reviewer 293; Part B 349).
- Confidence: high. Relied on the Plain-language statement (aid
  228–248) and the two Boundaries sections (Part A 199–226; Part B
  345–351); found no contradiction between parts. Correctly reported
  the Amendment 4 §A4.2 status-line caveat as the author's call, not
  as a defect. Asked: *why* does excluding illegal waivers in `Init`
  rather than rejecting them matter to the registered sentence? The
  aid states the fact (checks table row 2) but does not answer the why;
  the Probe result paragraph in `READING-AID-P4.md` now does.

## Reading

The aid did work, less dramatically than for Q3: the stripped reader
made no inversion, but bounded the claim to no instance, named a
secondary registered sentence and misattributed its provenance, and
read the load-bearing `Init` line backwards (as protecting the logic
rather than as leaving hostile policy input untested); the aided
reader got the instance and count, the load-bearing sentence, the
§A4.2 provenance, and the `Init` reading right. The one thing the aided
reader still wanted is an explanation the aid did not give — why
exclusion-not-rejection matters — and that is a sentence to add, not a
defect in what the aid says. The probe does not say the aid is
sufficient for the author; that is the author's read.

---

# Run 2 (2026-09-06, after the run-1 Probe result paragraph was added to the aid)

**STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not
adopted; the commit is the author's.** Appended, not rewritten: run 1
above is the record of its own answers; the answers graded here are a
second pair from two fresh Haiku 4.5 contexts, same two conditions,
same three questions. The condition-2 reader saw `READING-AID-P4.md`
**with** the run-1 Probe result paragraph (lines 40–59) in place — its
citations to aid lines 132–155 (Cast), 157–177 (Checks table),
220–248 (Boundaries) and 54–58 (the bold exclusion-not-rejection
sentence) are those numbers, i.e. the numbering **before** the run-2
paragraph was inserted after line 59 (which moved every later line
down by 21: Cast 132→153, Checks table 157→178, Boundaries 220→241). Same grading sources as run 1:
`READING-AID-P4.md` and the review record items 1–7 (lines 54–101),
reviewer output lines 210–307.

## Condition 1 — comment-stripped module only

- Claim: **partial.** Four-branch classification right, including the
  FAIL-over-UNPERFORMABLE order ("fail-closed order"; §A4.2
  precedence, `amendment-4.md:86–94`) and "every **legal** waiver
  policy" (an improvement on run 1, which said "all policies"). Three
  errors. (a) **No finite-instance bound**: never named the five-check /
  two-non-waivable configuration or the 1944 states
  (`P4_VerifierStates.out:34, 39`; reviewer 293). (b) **No registered
  sentence**: cited "Amendment 1 §A1.2 (P4) and §A1.2.1" as a block and
  asked what "registered sentence" means — it could not connect the
  run to "The verifier's four states partition all outcomes"
  (Amendment 1 `:152–153`; aid checks table row 1) or to any other
  sentence. (c) The quantity judged was called "the verifier's verdict
  logic **over a bundle**"; no bundle is represented — the quantity is
  the derived `Verdict` (line 105) over a status/waiver assignment
  (reviewer 218; Part B cast preamble, aid 288). "Explicit waivers" for
  `VALID_DEGRADED` imports a word the model does not carry: the state
  holds a nonempty waiver set, not an explicitness or a record
  (reviewer 223).
- Adversary: **wrong on the load-bearing line, right on the range.**
  Right that the adversary chooses any status assignment and any legal
  waiver set (reviewer 297), and right on cannot-represent (the
  `c1..c5` mapping; item 3). The load-bearing line it named is
  `ASSUME NonWaivable \subseteq Checks` (line 64) — an `ASSUME`, not an
  `Init` conjunct — instead of `waived \in SUBSET Waivable` (line 79),
  which reviewer 259 and Part B ("legal-policy initialization", aid
  354) identify. Its gloss compounds the miss: it said the
  fail-closed logic "depend[s] entirely on non-waivable checks forcing
  INVALID or UNVERIFIABLE". `VerdictFor` (96–103) ranges over
  **required** checks, `Checks \ W` (94), not over `NonWaivable`: a
  required *waivable* check that fails is `INVALID` too
  (`ExactInvalid`, 164–165), and `NonWaivable` appears only in the three
  §A1.2.1 invariants (118, 125, 133). It conflated "non-waivable" with
  "required".
- Boundary: **three right** — check outcomes are arbitrary inputs, not
  cryptographic results (reviewer 294; item 3); no implementation
  conformance follows (reviewer 305; Part B 370); waiver policies are
  not shown authorised or recorded (item 3; reviewer 236). No
  inversion.
- Confidence: medium. Asked what "registered sentence" means.
- Note on the input, as in run 1: "over a bundle" and "Amendment 1
  §A1.2 (P4) and §A1.2.1 (the waiver lattice)" are the module header's
  own phrases (lines 3–4, 7). Either the condition-1 copy retained
  those header lines, or the question supplied the amendment name. The
  exact condition-1 input was again not archived beside this file; it
  should be, as `q3_dns_stripped.pv` was for Q3.

## Condition 2 — reading aid (`READING-AID-P4.md`, Parts A and B) + module

- Claim: **right.** 1944 exhaustively enumerated states; eleven
  formulas; "five abstract checks, two non-waivable" (aid Finite
  instance, 196–202); registered sentence Amendment 1 `:152–153` "The
  verifier's four states partition all outcomes" (checks table row 1);
  four branches with the correct conditions, including "all-required-
  pass-with-nonempty-waiver → VALID_DEGRADED" (`ExactDegraded`,
  174–175). The sentence named is `Partition`'s; the other ten formulas'
  content is stated in the branch list.
- Adversary: **right; one unsupported gloss.** Any status assignment
  plus any subset of the three waivable checks; load-bearing line
  `waived ∈ SUBSET Waivable` (line 79), with the right consequence —
  illegal policies never enter the state space, so no rejection path
  exists to test (reviewer 259; aid cast `waived` row, checks table row
  2); cannot represent what the verifier does with an illegal policy
  (reject, normalise, mishandle). The gloss "preventing the verdict
  logic from collapsing to vacuous implication-checking" is the run-1
  stripped reader's phrase and has no support in the record — the
  line's effect is exclusion, and the invariants do not become vacuous
  under illegal policies, they are simply never evaluated on them.
  The reader's operative statement in the same sentence is the correct
  one; the gloss is a leftover, not a misreading of the consequence.
- Boundary: **three right** — `c1..c5` mapping is a reading, not a
  checked correspondence (aid cast row, 143; reviewer 237); the verdict
  is derived, never stored or transmitted (module header correction
  38–39; reviewer 298); illegal policies are excluded by `Init`, not
  validated at runtime (module comment 74–76; reviewer 259). These are
  three *different* boundaries from condition 1's three; both sets are
  in the record.
- Confidence: high. Relied on the Cast table (132–155), the Checks
  table (157–177) and the Boundaries section (220–248); found nothing
  contradicting the module. The question it most wanted answered —
  *why* exclusion-not-rejection matters — it reported as answered by
  the aid's lines 54–58, which is the bold sentence the run-1 result
  added. The run-1 gap is closed.

## Reading (run 2)

The aid did work. The stripped reader named the wrong load-bearing
line (the `ASSUME`, not the `Init` conjunct), conflated non-waivable
with required, bounded the claim to no instance, and could not name a
registered sentence; the aided reader got the line, the instance, the
count, the sentence and three boundaries right, and its one slip is a
gloss without operative consequence. No aided error is a defect to fix
in the aid. Two runs now agree on the stripped reader's instance-bound
and load-bearing-line failures and on the aided reader's recovery of
both; the second run additionally confirms that the sentence added
after run 1 answers the question the run-1 aided reader asked. Neither
run is the author's read; the probe does not say the aid is sufficient
for the author.
