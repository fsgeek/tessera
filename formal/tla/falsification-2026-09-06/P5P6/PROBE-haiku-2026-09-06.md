# Lower-ceiling reader probe — P5P6 reading aid (2026-09-06)

**STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not
adopted; the commit is the author's.**

Per `formal/suite/ENUMERATION.md` amendment note 5 item 2 (lines
297–312), in the form of
`formal/spike/first-link/proverif/reading-aid-q3/PROBE-haiku-2026-09-06.md`.
Reader: Claude Haiku 4.5, two fresh contexts; condition 1 given the
stripped `P5P6_TemporalRevocation.tla` only, condition 2 given
`formal/tla/READING-AID-P5P6.md` (Parts A and B) plus the module. Same
three questions both times: the claim (the quantity judged and the
registered sentence it supports), the adversary (and the load-bearing
initialization line), three boundaries. Graded by the AI collaborator
against `READING-AID-P5P6.md` and the review record
`docs/reviews/2026-09-06-codex-tla-falsification-p4-p5p6-p5c.md`
(items 8–14, lines 105–145; reviewer output lines 308–454). Module
line numbers are the current working-tree text. **Aid line numbers**
(both the reader's and the grader's) are the aid as the reader saw it,
before the 26-line Probe result paragraph was inserted after its
provenance block on 2026-09-06; add 26 to locate them in the current
file.

## Condition 1 — stripped module only

- Claim: **partial.** Quantity right (`StrictAccept`, line 154).
  Content right for two of the seven invariants — bytes signed at or
  after revocation are never accepted (`ForgeryRejected`, 166–167),
  acceptance stays inside the verifier's window whatever tolerances the
  receipt declares (`WindowRespected`, `VerifierOwnsTolerances`,
  172–186) — but it fused the policy window and the global maxima into
  one sentence ("the verifier's chosen temporal window, bounded by the
  global maxima"), which is exactly the distinction item 8 draws
  (record 105–111; header correction 37–44): `VerifierOwnsTolerances`
  compares against `DeltaMax`/`EpsilonMax`, not the chosen policy, and
  policy ownership is `ReceiptIndependence`'s. It named enlargement
  only ("adversarially-inflated tolerances"); narrowing, the
  `_BrokenTolStrict` defect that only `ReceiptIndependence` sees (aid
  checks row 5), is absent from the claim and reappears only as its
  closing question. The confirmation-timing conjunct
  (`AbandonedArtifactRejected`, 195–199) and the honest-cost bound
  (240–245) are not in the claim. **One error:** the "registered
  sentence" it supplied — "P6 security — revoked material is never
  accepted" — is not registered text (the reader had none) and, read
  as written, contradicts the registered rule: material from a key
  revoked after both `anchor_time` and `declared_issue_time` IS
  accepted (Amendment 1 `:212`, as written by §A4.3
  `amendment-4.md:107–119`; `AuthorizedThroughWindow` 147–149). The
  invariant rejects bytes *signed at or after* revocation, not
  "revoked material". No finite-instance bound was named (no state
  count, no constants).
- Adversary: **partial.** Right on `declared`, `rcptDelta`, `rcptEps`
  (with `RcptTolMax > DeltaMax`, 94) and `revoked`; right on the
  load-bearing initialization line `signed <= anchor` (109) and on the
  proof shape it carries (`revoked <= signed` forces `revoked <=
  anchor`, which `AuthorizedThroughWindow` rejects; comment 163–165;
  item 11). Omitted `signed` itself and `anchor` and `confirmedAt` from
  what the enumeration supplies — the aid's adversary "signs at any
  time not after the anchor" (aid 243–245), and the
  `confirmedAt`-unconstrained-relative-to-`anchor` fact (108; A2.1
  non-monotonic timestamps) is the module's one deliberate
  non-assumption. Cannot-represent list (signature verification
  abstracted as passing, header 54–56; no activation time, item 13)
  right but short: no header authentication, no depth-k derivation,
  no verdict partition (item 14), no transitions (reviewer 375) were
  not named.
- Boundary: **partial.** (2) integer times check the logic, not the
  72 h / 24 h magnitudes — right (header 52–54; aid 180–181). (3) the
  correspondence with P5c's `Ship` is the bridge's
  (`P5cP5P6_Bridge.tla`, 2026-07-21), not this module's — right (item
  12; header correction 26–36). (1) "not that an implementation relying
  on receipt-declared tolerances is safe" — not wrong, but not a
  boundary of this result: it is the `_BrokenTol` / `_BrokenTolStrict`
  companions' subject, which the model does address. **Missed the
  record's central boundary:** item 11 — `signed <= anchor` is imposed
  at `Init`, not checked; backward header skew can violate it, and the
  attack that exploits it is excluded at initialization rather than
  rejected (reviewer 387, 454; aid 196–203). The reader named the
  assumption under "adversary" and did not carry it into the boundary
  list. No inversion.
- Confidence: **high** — on an answer with a wrong claim sentence.
  Asked: does `\A rd \in 0..RcptTolMax` trap a narrowing bug when no
  narrowing function appears in the code? Yes: in the correct module
  `rd`, `re` are ignored (135–138), so the biconditional (219–221) is
  trivially true; `_BrokenTolStrict` routes them through `Min` (its
  lines 50, 54–57), so verdicts differ across `rd` values and the
  invariant goes red on `polDelta 1, rcptDelta 0, confirmedAt 1`
  (`_BrokenTolStrict.out:35–44`; aid checks row 5). The question
  shows the reader had not seen the companion.
- Note on the input: the answer cites "Layer 2" (comment 64–67, 109),
  "lifecycle deferred" (231), "the P5c bridge model (2026-07-21)"
  (29–30) and "72h/24h" (53). A fully comment-stripped module carries
  none of these; the condition-1 copy evidently retained the comments,
  or the reader inferred them. As with the P4 probe, the exact
  condition-1 input was not archived beside this file; the next probe
  should archive it, as the Q3 probe archived `q3_dns_stripped.pv`.
  This weakens the condition-1 baseline: a reader given the comments
  is already reading half the aid.

## Condition 2 — reading aid (`READING-AID-P5P6.md`) + module

- Claim: **right.** `StrictAccept` right; **4,302,592 distinct states**
  right (`P5P6_TemporalRevocation.out:47`; aid 170); the three-part
  content (signed before revocation, inside the verifier's own
  three-part window, independent of receipt tolerances) matches the
  aid's Claim (229–237) and Part B's (342); registered sentence P6 "no
  revocation effective at or before `anchor_time`" (Amendment 1
  `:209–210`) for `ForgeryRejected` 166–167 — right (aid checks row 1;
  Part B row 332). Finite instance right (times `0..6`, `signed \in
  0..anchor`, `DeltaMax = 3`, `EpsilonMax = 1`; cfg 2–5; Part B 344);
  did not name `RcptTolMax = 6`. "The central theorem is conditional
  on `signed <= anchor` (109), named but not checked here" — right,
  verbatim the aid's strongest defensible reading (240–241).
- Adversary: **right.** `declared`, `rcptDelta`/`rcptEps`,
  `confirmedAt` (unconstrained relative to `anchor`, 108), `revoked`
  (`0..MaxTime` or `NoRev`) right; load-bearing line `signed <= anchor`
  at `Init` (64–67, 109) right, with the correct consequence — without
  it a key revoked before the anchor could sign after revocation and
  declare a time just before (item 11; aid 196–203; reviewer 387).
  Cannot represent: activation time (item 13), signature verification
  (header 54–56), header authentication (item 14), issuer shipping and
  lifecycle transitions (item 12; reviewer 375), depth derivation
  (`confirmedAt` supplied, 108; item 14) — all right. Same omission as
  condition 1: `signed` is not listed among what the enumeration
  supplies, though the aid's adversary paragraph says "signs at any
  time not after the anchor" (243–245).
- Boundary: **three right** — cryptographic proof and header
  authentication (item 14; aid 215–219; Part B 367); exact signing-time
  recovery, tolerated backdating, wall-clock deadline (Part B 369;
  reviewer 333); 72 h / 24 h magnitudes and the absence of a
  parameter-independence theorem (header 52–54; aid 180–181; Part B
  372). Item 11 was carried under "adversary" with its consequence
  stated, so the central boundary is present in the answer, though not
  in the boundary list.
- Confidence: high. Relied on the Checks table (aid 136–145) and
  Boundaries (191–225); found no contradiction between the module and
  the aid, and did not report one between Parts A and B (none is
  recorded at the top of the aid). Asked: does any
  parameter-independence result exist elsewhere, since the aid
  disclaims one (181)? Answer: no — the record contains none for this
  instance (aid 180–181; Part B 372: "No all-bounds theorem"); the
  bridge model (`P5cP5P6_Bridge.tla`) is a different check, not a
  parameterisation of this one. That is a fact the aid states and a
  gap it does not close.

## Reading

The aid did work, on a narrower margin than for Q3 and about the same
as for P4: the stripped reader produced a claim sentence that inverts
the registered non-retroactivity rule ("revoked material is never
accepted"), fused the policy window with the global maxima (the item-8
distinction), bounded the claim to no instance, and left the record's
central boundary (item 11) off its boundary list; the aided reader got
the sentence, the count and constants, the item-8 division of labour,
and the conditional-on-`signed <= anchor` reading right, and named item
11's consequence. The stripped reader's adversary and load-bearing
line were already right — with the caveat that its input evidently
carried the module's comments, which is where those facts live — so
the discrimination is in the claim and the boundary, not the
adversary. Two things the aided reader still did not say, both
sentences to add rather than defects in what the aid says: that the
enumeration also supplies `signed` (the aid says it once, at 243–245,
outside the cast row); and that no parameter-independence argument
exists anywhere in the record, not only in this aid. The probe does
not say the aid is sufficient for the author; that is the author's
read.

---

## Run 2 (2026-09-06; appended, amend-don't-rewrite — run 1 above stands as graded)

**STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not
adopted; the commit is the author's.**

Second pair of fresh Haiku contexts, same two conditions, same three
questions. Condition 2's reader cites the aid at its **current** line
numbers (Cast 129–160, Boundaries 217–251, Part B "What this result
does not show" 391–399), so it read the file *with* the run-1 Probe
result paragraph (41–65) in place. **Aid line numbers in this section
are that text, before the 31-line run-2 Probe result paragraph was
inserted after it on 2026-09-06; add 31 to locate anything past aid
line 65 in the current file.**
Condition 1's input was again not archived beside this file, and the
answer again cites comment-only facts ("Layer 2: existence not-after
anchor", A2.1, "72h/24h", "re-issuance corollaries", "Ship rule (lines
11–12)"), so the baseline is once more a commented module, not a
stripped one. Grader: the AI collaborator, against
`READING-AID-P5P6.md` and record items 8–14 / reviewer 308–454.

### Condition 1 — module only

- Claim: **partial.** Quantity right (`StrictAccept` as `TemporalOK /\
  AuthorizedThroughWindow`, 135–154). Kept the item-8 distinction that
  run 1 fused — `WindowRespected` against "the verifier's chosen
  polDelta and polEps" and `VerifierOwnsTolerances` against "global
  DeltaMax/EpsilonMax" (172–186; header 37–44) — right. But it
  presented **four** invariants as the run's content; the cfg checks
  seven (cfg 11–17): `ReceiptIndependence` (219–221, load-bearing for
  receipt influence, aid checks row 5), `AbandonedArtifactRejected`
  (195–199) and `HonestCostIsExactlyTheWindow` (240–245) are absent
  from the claim (independence surfaces only under boundary 2). Said
  "strictly inside" the policy bounds; the conjuncts are `>=`/`<=`
  (136–138, 173–175). Named no finite instance — no state count, no
  constants (aid Finite instance, 195–200). Gave no registered
  sentence; its relying-party paraphrase is right on the three A2.2
  conjuncts but its revocation clause, "no revocation occurred before
  both declared and the anchor time", read literally excludes only a
  revocation before *both* — under ε > 0 the anchor may precede
  `declared`, and a revocation between them is not "before both", yet
  `AuthorizedThroughWindow` (147–149) rejects it; that is the §A4.3
  case (item 10; `amendment-4.md:107–119`). The answer's own gloss two
  sentences earlier ("revocation, if any, occurred after both declared
  and anchor") is right, so this is a slip in the sentence a relying
  party would quote, not a misreading of the predicate. Also drops the
  "at" (`revoked = anchor` rejects).
- Adversary: **right on the load-bearing line**, `signed <= anchor`
  (109) with the "Layer 2" gloss (64–67) and the consequence that
  `ForgeryRejected` collapses without it (comment 163–165; item 11).
  `declared` (106), `rcptDelta`/`rcptEps` up to `RcptTolMax > DeltaMax`
  (94, 113–114) right; `signed` and `revoked` named ("indirectly ...
  within the Init range"); `anchor` and `confirmedAt` — the latter
  unconstrained relative to `anchor` (108, 68–73) — not named. "No
  transitions, one snapshot" (116–117; reviewer 375) right. The
  cannot-represent sentence is muddled: the model's integers are a
  total order, so "abstract partial order" is wrong; the gap it
  reaches for — whether wall-clock signing precedes revocation when
  the header timestamp is skewed — is item 11's residual, which the
  answer then asks about in its closing question.
- Boundary: **partial.** (1) Issuer compliance with the Ship rule is
  not checked here — right, the header's scope boundary (9–13) and
  item 12 (bridge's). (3) No activation time (231) — right, item 13.
  (2) "does not certify the verifier's policy choices are justified"
  — not in the record; not a boundary of this result so much as a
  non-claim. **Item 11 again absent from the list** and again carried
  elsewhere — this time as the closing question ("does `signed <=
  anchor` hold empirically for Bitcoin's non-monotonic block
  timestamps (A2.1)"), which is the right assumption attributed to the
  neighbouring A2.1 fact: non-monotonic timestamps are why
  `confirmedAt` is unconstrained (68–73); the threat to `signed <=
  anchor` is backward header skew, A2.1's skew residual
  (`amendment-2.md:186–196`; aid Boundaries, item 11). Item 14 not
  named.
- Confidence: **high**, on a four-of-seven claim with no instance.

### Condition 2 — aid (Parts A and B) + module

- Claim: **right on content, two slips.** `StrictAccept` right;
  **4,302,592 states** right (`out:47`); the four-part sentence —
  signed before revocation, inside the verifier's own three-part
  window, identical under every receipt-declared pair, honest cost
  confined to the revocation-between-declaration-and-anchor case —
  is the aid's *Claim* (255–267) with the item-8 division intact.
  Slip 1: it labels that sentence "registered"; it is the
  collaborator's plain-language statement (heading 253), and the
  registered sentences are the checks table's third column
  (`amendment-1.md:159–230`, `amendment-2.md:220–231`). Slip 2:
  "revoked **strictly between** declaration and anchor" — the
  interval is `(declared, anchor]` (comment 235–239; checks row 7):
  `revoked = anchor` fails `revoked > anchor` (149) and is a
  sacrificed honest receipt. The aid's *Claim* says "between
  declaration and anchor" without the bracket, so this error is
  **aid-induced**; the fix belongs in the aid's Claim sentence.
- Adversary: **right on the load-bearing line and its consequence**
  — `signed <= anchor` (109) at `Init`, "excluded at initialization,
  not rejected by the verifier" (item 11; reviewer 454) verbatim the
  aid's Boundaries. `declared`, `anchor`, `confirmedAt`, the four
  tolerances, `revoked` right. **Omitted `signed`** from what the
  enumeration supplies for the second run running, and wrote "though
  some are constrained by the assumption" against
  `declared`/`anchor`/`confirmedAt` — none of those three is
  constrained; `signed` is (109). The run-1 paragraph's bold sentence
  ("the enumeration supplies `signed` too", aid 60–61) did not land:
  the reader says it relied on the Cast, Boundaries and Part B, and
  the sentence sits in the provenance area, not in the `signed` cast
  row (141) or the *Adversary* paragraph (269–271). Cannot-represent
  (signature verification, header 54–56) right.
- Boundary: **three right.** Anchor provenance / depth-k / confirmation
  count (item 14; aid 241–245; Part B 393); tolerated backdating and
  wall-clock timeliness (Part B 395; reviewer 333); no activation or
  revoke-then-re-authorise lifecycle (item 13; Part B 397). Item 11
  under "adversary" with its consequence, not in the list — same
  placement as run 1 and as condition 1.
- Confidence: **medium.** Relied on Cast 129–160, Boundaries 217–251,
  Part B 391–399; no contradiction found between module and aid, none
  reported between Parts A and B (none recorded). Asked: the exact
  item-8 division of labour — `VerifierOwnsTolerances` catches
  enlargement past the global ceilings, `ReceiptIndependence` catches
  enlargement and narrowing alike, complementary not hierarchical.
  That is what header 37–44, the `ReceiptIndependence` correction
  (209–218), checks rows 3 and 5 and Part B 350 say; the reader had it
  right and wanted it confirmed. One precision: in the correct module
  `rd`, `re` are ignored (135–138), so `ReceiptIndependence` is
  trivially true there; it "catches enlargement" only in a module that
  routes them in (`_BrokenTol`'s `Max`, its 53, 58–61), whose cfg does
  not list it (aid 214–215; Part B 389).

### Reading (run 2)

The aid did work, on a narrower margin than run 1: the stripped
reader improved (no inverted sentence, the item-8 distinction kept)
but still gave four invariants for seven, no instance, no registered
sentence, and a relying-party revocation clause that fails the §A4.3
case; the aided reader gave the seven-invariant content, the count,
and item 11's consequence, with three boundaries right. The adversary
did not discriminate — both readers had line 109 and its proof shape,
and both condition-1 answers so far have had the comments, so the
baseline for the adversary is the module's reading guide, not a bare
module. Two aid defects, one per run: **(a)** the *Claim* sentence's
"between declaration and anchor" produced "strictly between" — write
`(declared, anchor]`; **(b)** the `signed`-is-enumerated sentence,
added after run 1 to the provenance paragraph, was not read — it
belongs in the `signed` cast row and the *Adversary* paragraph. Both
are wording changes to Part A, PROPOSED, not applied by this probe.
The condition-1 input must be archived next time, as
`reading-aid-q3/q3_dns_stripped.pv` is; two runs have now graded
against an unarchived baseline. The probe does not say the aid is
sufficient for the author; that is the author's read.
