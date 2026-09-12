# Lower-ceiling reader probe — P5c reading aid (2026-09-06)

**STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not adopted; the commit is the author's.**

Per `formal/suite/ENUMERATION.md` amendment note 5 item 2 (lines
297–312). Reader: Claude Haiku 4.5, two fresh contexts; condition 1 given
the module only, condition 2 given `formal/tla/READING-AID-P5c.md` (Parts
A and B) plus the module. Same three questions both times: the claim
(the quantity judged and the registered sentence), the adversary/
abstraction (and the load-bearing initialization assumption), three
boundaries. Graded against the aid and the review record
`docs/reviews/2026-09-06-codex-tla-falsification-p4-p5p6-p5c.md` items
15–21 (lines 149–183) and the verbatim P5c reviewer output (lines
455–581). Line numbers are the current working-tree
`P5c_IssuanceProtocol.tla`.

**Two runs are recorded here** (both 2026-09-06; run 2 added by the AI
collaborator, PROPOSED). Run 2 was a second pair of fresh contexts,
dispatched after run 1's probe paragraph had been appended to the aid,
so run 2's condition 2 saw the aid *with* that paragraph (its answer
cites aid lines 61–62). Run 1 is left as written; run 2 follows it.

**Caveat on the baseline.** The condition-1 answer cites "header lines
54–60", "line 248–258" (the boundary-race comment), "Layer 2 assumption
A1.6" and "Amendment 3" — text that exists only in the module's
comments. So condition 1 here was not comment-stripped in the Q3 sense
(no stripped `.tla` is archived beside this file); the P5c header is
itself a strong reading aid (lines 47–101 name the refusal split, the
liveness residuals and the permanence assumption). The probe therefore
measures the aid over the *commented* module, a stronger baseline than
Q3's.

# Run 1

## Condition 1 — module only

- Claim: **partial.** Named the shipping half only — "a shipped
  receipt's anchor remains buried at minimum confirmation depth k
  within the declared issuance window", discharged by `ShippedIsSound`
  and `NoShippedOrphan`. **Missed the refusal half entirely** (atomic
  entry `NoSilentDeadlock`, `RefusedOnlyWhenExhausted`,
  `RefusalLatched`), which the header calls "What IS claimed" (69–76)
  and the aid's checks table rows 4–6 mark load-bearing for the A2.3
  model note. The registered sentence was paraphrased, not the
  `amendment-1.md:186–189` text; "remains buried" is right in substance
  (`NoShippedOrphan`, `Reorg` guard 237). Did not quantify the instance
  (2190 states; k = 3).
- Adversary: **right.** Scheduler nondeterminism over `Tick`, `Anchor`,
  `Reorg`, `Ship`, `Reissue`; A1.6 permanence as a `Reorg` precondition
  (237; comment 231–235), matching item 21; Bitcoin timestamp skew as
  unrepresentable (header 79–82). One category slip: asked for an
  *initialization* assumption, it answered with the `Reorg` action
  precondition and said so itself.
- Boundary: **right (3/3).** Liveness unclaimed (header 62–69);
  the deadline-instant race at `now = declared + Delta` where `Ship`
  (263) and the refusing `Tick` (204) are both enabled (comment
  248–259) — correct, though not routed to the latch module (item 16);
  refusal is a Boolean, durability/retrieval/reporting are Amendment 3
  obligations (header 55–61). Did not name k = 3 vs k = 6 (item 20).
- Confidence: high.

## Condition 2 — reading aid (Parts A and B) + module (run 1)

- Claim: **right.** Both halves — shipped receipts in-window, buried,
  not orphanable by the permitted shallow reorgs; final expiry without
  shipping atomically enters a refusal that persists — six invariants
  and one action property, 2190 distinct states, instance k = 3, δ = 3,
  N = 3, `MaxTime` 14; quoted the registered sentence
  (`amendment-1.md:186–189`) correctly; named the quantity judged as
  the issuance outcome (shipped or refused), which is Part B's "thing
  being judged" (line 300).
- Adversary: **right, one misattribution.** Scheduler and chain
  (`Anchor` delay, shallow `Reorg`) right; load-bearing initialization
  assumption = `Init`'s clean start, which is Part B's answer (374) and
  is the actual initialization assumption (the permanence assumption
  C1 chose is an action precondition). Named cryptographic
  verification as unrepresentable (right; reviewer 565–566) but
  attributed its absence to **"the single-clock abstraction"** — wrong:
  the single clock is block time = wall time (header 79–82); the
  absence of bytes, signatures, keys, headers and verdicts is a
  separate, unnamed-in-module abstraction (aid Boundaries, "No
  adversary in the A1.3 sense"; Part B 388 attributes it to "these ten
  variables and five actions", not to the clock).
- Boundary: **right (3/3).** Liveness unclaimed; k = 3 checked, not
  the registered default k = 6, with no parameter-independence argument
  (item 20; aid "Finite instance"; reviewer 461); S = 0 pre-latch
  instance with the latch checked in `P5cP5P6_BridgeSlack_Latch.tla`
  (item 16). Its "what I most want explained" — that `RefusalLatched`
  proves in-model persistence, not durable storage — is the header's
  own narrowing (55–61) and Part B's stale-wording note (362).
- One further slip: "No contradictions between aid and module" — Part
  B 362 records one (cfg 32 "Durably recorded" and `.tla` 175 "durable
  refusal record" exceed the narrowed claim). Not a wrong answer to the
  three questions; a missed reading of Part B.
- Confidence: high. Relied most on Part A's "Plain-language statement"
  and "Boundaries" and Part B's "What this result does not show"
  (384–391); line references check against the file.

## Reading (run 1)

The aid did work on the **claim**: the module-only reader stated half
of it (shipping) and omitted the refusal half that the header, the aid
and the review all mark as load-bearing; the aided reader stated both
halves, quantified the instance, and quoted the registered sentence.
On the **adversary and the boundaries** the probe **did not
discriminate**: both readers were right, because the P5c header
already carries the permanence precondition, the liveness residuals,
the boundary race and the refusal narrowing — the aided reader's
boundaries were the review's item-numbered ones (k = 6, latch routing)
where the module-only reader's were the header's own, which is the
aid's expected effect but not a discrimination. The aid is **not
defective**: no aided answer was wrong where the module-only answer
was right. The one aided error (crypto absence attributed to the single
clock) is a conflation of two adjacent Boundaries bullets and is
addressed by one sentence in the aid's probe paragraph. Under
ENUMERATION note 5 item 2, a non-discriminating adversary/boundary
result calls for a weaker reader or a genuinely comment-stripped
condition 1; that is a probe-design note, not a verdict on the proof,
and the probe does not gate exit. The probe does not say the aid is
sufficient for the author; that is the author's read.

---

# Run 2 (second pair of fresh contexts, 2026-09-06)

Same reader, same three questions, graded against the same aid and
review record. **Aid line numbers in this section are those of the
file the reader saw** — `READING-AID-P5c.md` before the run-2 probe
paragraph was inserted after line 62 (Part A 1–302, Part B 304–417).
That insertion is 25 lines: add 25 to any aid line above 62 to find it
in the current working tree (e.g. Boundaries 232 → 257, Part B `Init`
paragraph 394 → 419).

**Caveat on the baseline, again.** The condition-1 answer refers to
"the correction note", "the A1.6 Layer 2 precondition", "Amendment 3"
and "the P5cP5P6_Bridge module" — text that exists only in the
module's comments (header 79–86, 55–61, 108–117). Condition 1 was
again the *commented* module, not a stripped one.

## Condition 1 — module only (run 2)

- Claim: **partial.** Named `ShippedIsSound`, `NoShippedOrphan` and —
  unlike run 1 — `NoSilentDeadlock` ("if all `MaxAttempts` attempts
  expire unshipped, the refusal state is recorded atomically", 318–319,
  Tick 203–204: right). Omitted `RefusedOnlyWhenExhausted`,
  `RefusalLatched` and `ExpiredCannotShip` (header "What IS claimed",
  69–76). Two overstatements: "permanently buried" and "secure,
  irreversible issuance completion" as the quantity judged — permanence
  beyond depth k is a `Reorg` precondition, not a result (237; comment
  231–235; item 21), and the thing judged is the current attempt's
  outcome (Part B 320). Registered sentence quoted correctly
  (`amendment-1.md:186–189`). Did not quantify the instance (no state
  count, no k = 3).
- Adversary: **right on the scheduler and the chain; wrong category on
  the initialization assumption.** Scheduler over the five actions,
  `Anchor` timing, `Reorg` capped at `reorgs < 2` (238), the
  `Tick`/`Ship` race at the deadline (248–259): right. Asked for the
  load-bearing *initialization* assumption it answered the `Reorg`
  precondition (A1.6 permanence) — the same category slip as run 1;
  `Init` (182–187) is the initialization. Its "without it,
  `ShippedIsSound` would fail" is defensible (a post-ship orphan would
  also falsify the `anchorAt # NoAnchor` conjunct, 300) but the
  invariant that names the harm, and the one `_Broken` turns red, is
  `NoShippedOrphan` (292; `_Broken.cfg`). Unrepresentable: variable
  block interval and the wall-time/chain-time gap — right (header
  79–82); "mempool fee dynamics" is half right — the *dynamics* are
  absent but their effect, delayed inclusion, is exactly `Anchor` not
  firing (comment 209–211).
- Boundary: **2 right, 1 partial.** (1) Liveness unclaimed — right
  (header 62–69). (2) Refusal durability not shown — right in
  substance (header 55–61) but **attributes the latch to
  `ShippedIsSound`**; the Boolean latch is `RefusalLatched` (337), an
  action property, and `ShippedIsSound` (298–303) says nothing about
  `refused`. (3) Verifier-side ε and the three-conjunct predicate live
  in the bridge — right (correction note 108–117; item 17). Did not
  name k = 3 vs k = 6 (item 20).
- Confidence: medium. Asked for "a concrete example of divergence"
  between `Ship`'s fused guard and the A2.1 predicate. The review
  record has one (reviewer §6, line 573): `Anchor(0); Tick×4` — the
  designated block's timestamp is 2, within δ = 3, but `now = 4`
  disables `Ship`; the fused guard is "locally stronger". The aid does
  not carry the example; see Reading.

## Condition 2 — reading aid (Parts A and B, with run 1's probe paragraph) + module (run 2)

- Claim: **partial — and narrower than condition 1.** The bolded claim
  is the shipping half only: "a shipped receipt's anchor is buried at
  the minimum confirmation depth k within δ of its declared time under
  the single-clock abstraction, and no shipped anchor is orphaned by
  the shallow reorganizations the model permits" (`ShippedIsSound`,
  `NoShippedOrphan`). The refusal half — `NoSilentDeadlock`,
  `RefusedOnlyWhenExhausted`, `RefusalLatched`, which the aid's
  plain-language statement puts *first* (aid 279–285) and Part B's
  claim states ("final expiry without shipping atomically enters a
  refusal that persists", 386) — is absent from the claim, although
  "refused" appears in the quantity judged ("the outcome of each
  issuance attempt (shipped, refused, or pending)" — right; Part B
  320). Instance quantified correctly (2190/3606, k = 3, δ = 3, N = 3);
  registered sentence quoted correctly. Condition 1 had named
  `NoSilentDeadlock`; condition 2 did not.
- Adversary: **right (3/3 sub-questions).** (a) `Anchor` deliberately
  not guarded on `~refused`, the A2.4 late-anchor case (209–224,
  225–229); (b) shallow `Reorg`; (c) postponable scheduling including
  the final `Tick` — all right. Load-bearing initialization assumption
  = `Init`'s clean start, no recovery from a prior attempt — right, and
  it is Part B's answer (394). Unrepresentable: cryptographic
  verification, "no bytes, signatures, or keys; timestamps and depth
  are abstract stand-ins" — right (reviewer 565–566), and **not
  attributed to the single clock** this time (run 1's aided slip; the
  correcting sentence was in the aid's run-1 probe paragraph, 55–60,
  which this reader saw).
- Boundary: **right (3/3), with correct citations.** Liveness unclaimed
  (header 62–69, 91–93); deep reorgs excluded by assumption A1.6, the
  broken companion showing what the rule buys given it (237; header
  85–86; item 21); no verifier-side processing — crypto, ε, the
  three-conjunct agreement — routed to the bridge and the A2.2
  obligations (aid 265–272; item 17). k = 3 vs k = 6 appears in the
  claim, not the boundary list.
- Confidence: medium. "What I most want explained": whether the
  single-clock abstraction is "truly valid, or just a useful toy" —
  the reader found the clock-roles ruling (header 34–44) and the
  correction (108–117) but wanted the connection made explicit. Same
  request as condition 1's, from the other side.
- Relied most on the aid's Boundaries (232–276) and plain-language
  statement (278–301) — which makes the omitted refusal half notable:
  the statement it relied on opens with that half.
- Reported the "durable" wording mismatch (cfg 32, module 175 vs the
  narrowed Boolean-latch claim) as a contradiction "in the aid itself
  (line 61–62)" — right in substance; the location is the run-1 probe
  paragraph reporting Part B 382, so run 1's missed reading is not
  repeated.

## Reading (run 2)

- **Claim: did not discriminate, and the aided answer was the narrower
  one.** Both readers gave a partial claim; the module-only reader
  named `NoSilentDeadlock` and the aided reader did not, although it
  reported relying on the plain-language statement whose first three
  clauses are the refusal half. This does not meet ENUMERATION's
  "aided wrong" (nothing the aided reader stated is false), but it
  reverses run 1, where the aid did work on exactly this point. Over
  two runs the claim discrimination is 1 of 2 — not robust. The aid's
  delivery of the two-halved claim is the defect to fix: the
  plain-language *Claim* paragraph runs the six invariants together in
  one sentence; a reader answering "what is the quantity judged" takes
  the shipped receipt and stops. A one-line lead — "two halves:
  shipping (rows 1–3) and refusal (rows 4–6)" — is the proposed repair.
- **Adversary: the aid did work on the initialization sub-question**,
  both runs: module-only answered an action precondition, aided
  answered `Init` (Part B 394). The rest did not discriminate (both
  right).
- **Boundary: the aid did work on precision.** Module-only attached the
  refusal latch to the wrong invariant (`ShippedIsSound` for
  `RefusalLatched`); aided named the routing by item number with
  correct line cites. Run 1 had both right, so this is 1 of 2 as well.
- **Not defective.** No aided answer was wrong where the module-only
  answer was right; run 1's one aided slip (crypto absence attributed
  to the clock) did not recur once the aid carried the correcting
  sentence.
- **Both readers asked for the same thing:** a concrete case where the
  fused guard and the A2.1 predicate diverge. The reviewer's
  `Anchor(0); Tick×4` example (record line 573) answers it in one
  line; the aid should carry it in checks row 2 or the single-clock
  bullet. Proposed, not applied here — the aid's change is the probe
  paragraph only.
- Probe design: condition 1 was again the commented module; the P5c
  header remains a strong aid on its own. A comment-stripped `.tla`
  archived beside this file is still needed for a Q3-form baseline.
  Not a verdict on the proof; does not gate exit.

