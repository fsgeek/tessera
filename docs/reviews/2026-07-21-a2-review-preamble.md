# A2 review rounds — dispatch preamble (paste ahead of each round)

Prepared 2026-07-21 for the pre-signature review of
`docs/phase-0-prereg-amendment-2.md` (GPT-5.6 via Codex CLI ×2 + Gemini,
per the standing multi-round adversarial practice; record the actual
model identifier from the CLI config in each round's archive —
`gpt-5.6-sol` as of this writing). Archive each round's verdict
and disposition in `docs/reviews/` as usual.

---

## Paste-ready preamble

You are performing a falsification-style non-author review of a DRAFT
amendment to a pre-registered protocol, before the author signs it.
Your goal is to find reasons it should NOT be signed as written.

**Object under review:** `docs/phase-0-prereg-amendment-2.md` (Amendment
2 / "A2"). It ratifies the strict reading of "confirmed within δ" on a
chain-visible observable, adds a verifier-side conjunct, bounds the
re-issue loop with an explicit refusal outcome, and registers
anchor-identity and declared-time-confinement rules.

**Normative context (what A2 amends — read for conflicts):**
`docs/phase-0-prereg.md` and `docs/phase-0-prereg-amendment-1.md`
(especially A1.2 property statements and A1.6 assumption layers).

**Discharging artifacts (check text↔model correspondence, not model
internals — the models have had their own review gates):**
- `formal/tla/P5c_IssuanceProtocol.tla` + cfgs/outs — A2.1 strict rule,
  A2.3 attempt bound and refusal state.
- `formal/tla/P5P6_TemporalRevocation.tla` + `_BrokenConf` — A2.2
  conjunct.
- `formal/PROPERTIES.md` — status ledger.

**Prior review record (do not rediscover; build on):**
`docs/reviews/2026-07-07-codex-amendment-2-review.md`,
`2026-07-20-codex-rulings-review-round3.md` / `-round4.md`,
`2026-07-20-codex-p5c-refusal-review.md`.

**Known deltas — settled this review cycle; do not spend the round
re-deriving them (but DO flag if the amendment text fails to honor
them):**

1. *Recorded vs. reported.* A2.3 requires a durably recorded refusal;
   reporting is deferred to Amendment 3. The model proves only that the
   abstract refusal state is entered atomically and latches — storage
   durability, retrievability, and reporting are implementation/handoff
   obligations. The A2.3 model note carries this proof-vs-contract split.
2. *Termination.* The model is safety-only, no fairness: it proves the
   conditional half (if the final crossing occurs, refusal is in its
   post-state), never that the crossing occurs. "Bounded termination" is
   contract language, an implementation obligation. Also carried in the
   A2.3 model note.
3. *Boundary tie.* At `confirmed_at = declared_issue_time + δ` the model
   permits both shipping and (on the next tick) refusal — an intentional
   race, documented in the P5c module at `Ship`.
4. *Anchor standing.* Per the round-3 rulings, anchor standing becomes
   its OWN property with a stable identifier in Amendment 3 (not a P2
   rider). A2.4 here states the standing rule as protocol text.

**Attack surface — what we want from this round, in order:**

1. **Internal consistency.** Any sentence in A2 that contradicts another
   sentence in A2, or the known deltas above (e.g., any surviving
   "reported refusal" or unconditional termination phrasing).
2. **Text↔model correspondence.** Does A2.1's registered predicate say
   exactly what P5c's `Ship` checks (including the `DepthK = k − 1`
   convention pin)? Does A2.2's conjunct say what P5P6's `confirmedAt`
   conjunct checks? Does A2.3 describe the refusal machinery that
   actually exists? A registered sentence that means more or less than
   the checked predicate is a finding.
3. **Boundary question (open, wants a ruling):** should A2.1's registered
   text acknowledge the tie at `confirmed_at = declared + δ` (both
   outcomes admissible at the boundary), or is the model-level
   documentation sufficient? Argue one way.
3a. **Ship-guard completeness (open, wants a ruling — surfaced
   2026-07-21 by the TLA+↔TLA+ bridge model,
   `formal/tla/P5cP5P6_Bridge.tla`):** A2.1's "The rule" sentence states
   only the confirmation conjunct ("issuance is complete only if
   confirmed_at ≤ declared + δ"). Under skewed, non-monotonic block
   timestamps, conjunct 3 does NOT imply conjunct 2: a forward-skewed
   anchor timestamp near the boundary yields `confirmed_at` in-window
   with `anchor_time` out-of-window, so a conjunct-3-only issuer would
   honestly ship a receipt the verifier rejects. A2.1's "by
   construction" sentence is narrowly true (it claims only the
   confirmation conjunct), but the honest-ship-never-rejected spirit
   requires the issuer to evaluate the FULL VALID_STRICT before
   shipping. Should A2.1 state that explicitly? (The bridge model's
   Ship guard does; the A2.2 "identical predicate" framing arguably
   already implies it.)
4. **A2.4 vs. Amendment 3 (open, wants a ruling):** does A2.4's
   anchor-standing text pre-empt, conflict with, or cleanly underdetermine
   the planned stand-alone anchor-standing property? Identify any wording
   that A3 would have to contradict rather than refine.
5. **Named residuals completeness.** A2.1 names adversarial timestamping
   and non-monotonic timestamps. Construct any *additional* residual the
   strict rule leaves open (e.g., interactions between the ε side and the
   new conjunct; reorg behavior at exactly depth k; header-store trust
   for the A2.2 evidence obligation).
6. **Hidden weakening.** A2.6 claims nothing is weakened and the A1.1
   falsifier is not triggered. Try to construct a reading under which any
   A2 change weakens a registered property.
7. **Parameter sanity.** N = 3, k = 6, δ = 72h, ε = 24h remain working
   defaults ratified at Band 0 exit; flag any way A2's text quietly
   depends on a specific value rather than the symbol.

**Verdict format:** per finding — defect / overclaim / open-question,
with the sentence or line quoted, and a proposed disposition. Do not
repair the document; the author rules on dispositions. State explicitly
at the end whether you would sign as written, sign with the listed
repairs, or not sign.

---

## Round log

Round 1 delivered 2026-07-21 as a three-reviewer panel (author's
substitution: Grok in place of a second GPT round): Grok — sign with
repairs; GPT-5.6 (gpt-5.6-sol) — not as written, sign with repairs;
Gemini (anti-gravity) — not as written, sign with repairs. All fifteen
merged findings dispositioned and folded same day; archive with
verbatim reviews and disposition matrix:
`2026-07-21-a2-reviews-round1-grok-gpt56-gemini.md`. Two dispositions
reserved for the author (anchor-standing narrowing wording;
double-SHA-256 declined-as-intentional).
