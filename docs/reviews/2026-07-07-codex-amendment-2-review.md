# Review: Phase 0 Pre-Registration Amendment 2 draft, Codex

Review artifact under the Amendment 1 §A1.7 falsification discipline.
Reviewer: Codex (OpenAI), acting as a non-author reviewer. Original review
date: 2026-07-07. The completed review was recovered on 2026-07-19 after its
artifact failed to land in `docs/reviews/`.

## Reproducibility and recovery record

- **Original reviewed commit:** `4e8bc78e0220cb581421f7340654d3cfba17c5b2`.
- **Recovered input request:** “Falsification-style review (A1.7 discipline)
  of Tessera's Amendment 2 draft and the new TLA+ model work at commit
  4e8bc78.”
- **Recovered source:** the completed local Codex transcript dated
  2026-07-07, session
  `019f3db3-c778-7310-85cc-78cb69bb500b`. The transcript does not embed the
  scheduler identifier `task-mray2hm5-ob8gqq`; its identity with that task is
  therefore inferred from the date and matching review request. This is the
  only unresolved recovery ambiguity.
- **Current-commit validation:** current commit
  `d4b23a40e6c3055e62bd1954ad0a02c2563781da` has the same Amendment 2 draft
  blob as `4e8bc78`:
  `d02046e2736c3584825d6ea1fa29675abf1cbc16`. The recovered review therefore
  addresses the exact current draft text, not merely an earlier revision.
- **Validation scope:** the review inspected the committed draft, models, and
  existing TLC evidence. It did not rerun TLC.

## Current status of the recovered findings

All three findings remain applicable at the current commit:

1. **High — explicit refusal is prose/commentary, not modeled state.**
   Amendment 2 requires an “explicit, reported refusal” as a first-class
   protocol outcome (`docs/phase-0-prereg-amendment-2.md`, lines 136–154).
   `formal/tla/P5c_IssuanceProtocol.tla` still has no refusal variable or
   transition: its variables are listed at lines 67–78, `Reissue` is enabled
   only while `attempts < MaxAttempts` at lines 124–131, and `Next` contains
   only `Tick`, `Anchor`, `Reorg`, `Ship`, and `Reissue` at line 133. The
   header's statement that exhaustion means explicit refusal (lines 43–48)
   is a comment, not state-machine semantics.
2. **Medium — the claimed exact issuer/verifier predicate correspondence is
   only an abstraction-level assertion.** The draft claims an identical
   predicate on an identical chain-visible observable and “exact
   correspondence” (`docs/phase-0-prereg-amendment-2.md`, lines 59–86), while
   P5c `Ship` checks `now <= declared + Delta`
   (`formal/tla/P5c_IssuanceProtocol.tla`, lines 113–122) under a single-clock
   abstraction (lines 17–26). Current `formal/PROPERTIES.md`, lines 40–50,
   independently records that P5c and P5P6 model the quantity incompatibly,
   that the join is asserted rather than checked, and that a bridge model
   remains an open obligation.
3. **Medium — A2.4's normative commitments lack an explicit discharge path.**
   The draft makes anchor standing and declared-time confinement normative
   commitments (`docs/phase-0-prereg-amendment-2.md`, lines 158–183) and lists
   them among the obligations added by Amendment 2 (lines 204–213), but A2.5
   enumerates only the verifier family, P5c, and conformance-vector model
   obligations (lines 187–200). Current `formal/PROPERTIES.md` adds P5c, the
   A2.2 conjunct, and its vector cases, but contains no A2.4-specific tracker
   entry. Whether A2.4 is to be modeled or discharged as policy remains
   unspecified.

The High finding should be resolved before the draft is signed. The two
Medium findings require either a concrete obligation/discharge artifact or
text that accurately limits what is being claimed.

## Full recovered review text (verbatim)

Reviewed `4e8bc78`; `HEAD` only adds the stamp commit, and the reviewed files are unchanged after it.

**Findings**

- **High:** A2.3’s “explicit, reported refusal” is not modeled. The draft makes refusal a first-class protocol outcome in `docs/phase-0-prereg-amendment-2.md:144`, but `P5c_IssuanceProtocol` has no `refused` state/action in its variables or transitions. `Reissue` simply stops at `attempts < MaxAttempts`, while terminal failure is described as bounded deadlock in `formal/tla/P5c_IssuanceProtocol.tla:126` and line 135. This is exactly the A1.7 case: prose implies a property the model fails to state.

- **Medium:** The “one predicate, both sides” claim is stronger than the issuer model supports. A2.1 defines `confirmed_at` as a chain-visible block timestamp in `docs/phase-0-prereg-amendment-2.md:66`, while P5c `Ship` still checks `now <= declared + Delta` in `formal/tla/P5c_IssuanceProtocol.tla:117`. The header admits this works only under the single-clock abstraction in line 23. That may be acceptable, but then the draft/model should say the correspondence is by abstraction, not “exact by construction.”

- **Medium:** A2.4 adds normative obligations that are not tracked as model/review obligations. The draft adds anchor-standing and declared-time confinement rules in `docs/phase-0-prereg-amendment-2.md:160`, and A2.6 says these are added obligations in line 206. But A2.5 and `formal/PROPERTIES.md` track only P5/P5c/A2.2/conformance-vector work; see `formal/PROPERTIES.md:46`. Either add explicit tracker entries or state they are out-of-model policy commitments with their own discharge path.

No blocking issue found with the `4e8bc78` cleanup itself: ignoring TLC scratch state and replacing the massive sanity output with a marked summary is consistent with the commit message. I did not rerun TLC; I reviewed the committed models and existing TLC artifacts.

---

## Independent recovery verification (Claude, main session, 2026-07-19)

Checked before committing this artifact, against the recovery claims above:

- **Session file exists:**
  `~/.codex/sessions/2026/07/07/rollout-2026-07-07T10-50-20-019f3db3-c778-7310-85cc-78cb69bb500b.jsonl`,
  mtime 2026-07-07 10:53:23 −0700, 340,261 bytes (run 10:50→10:53).
- **Verbatim text present in transcript:** distinctive phrases matched —
  "bounded deadlock" ×3, "one predicate, both sides" ×4,
  "Falsification-style review" ×2.
- **Stated ambiguity confirmed:** `task-mray2hm5-ob8gqq` does not appear in
  the transcript; identity with that scheduler task rests on date + matching
  request text only.
- **Reviewer model (from transcript):** `gpt-5.5`. The 2026-07-19
  recovery/validation pass ran separately under `gpt-5.6-sol`
  (codex-cli 0.144.6); the review findings are the 2026-07-07 gpt-5.5 output.
- **Blob check reproduced:** `docs/phase-0-prereg-amendment-2.md` is blob
  `d02046e2736c3584825d6ea1fa29675abf1cbc16` at both `4e8bc78` and current
  HEAD (`d4b23a4`).
- **Prior-transcript visibility:** yes — the reviewer had repo access
  including the committed A1 review artifacts in `docs/reviews/`.

## Disposition (DRAFT — AI collaborator, 2026-07-19; pending author sign-off)

1. **High (refusal unmodeled): ACCEPT.** Independently corroborates Q7 of
   `formal/tla/P5c_IssuanceProtocol.READ-AND-CHALLENGE.md` (silent stall on
   attempt N is a fail-open). Work item: explicit `refused` terminal state
   and `Refuse` action in P5c, an invariant that attempt exhaustion reaches a
   *reported* refusal rather than deadlock, and a broken companion
   (silent-stall) that must go red. This grows the model to match registered
   prose — no amendment required (A1.1 gates weakenings) — and per the
   review's recommendation should land before the author signs A2.
2. **Medium (correspondence is by abstraction): ACCEPT.** Convergent with
   the TLA+↔TLA+ bridge obligation independently itemized in
   `formal/PROPERTIES.md` on 2026-07-19. The wording correction ("by
   abstraction, not exact by construction") goes to Amendment 3 per the
   break-the-chain decision; A2 stands as drafted.
3. **Medium (A2.4 lacks a discharge path): ACCEPT the gap; discharge-path
   choice routed to the author** — model obligation vs. explicit out-of-model
   policy commitment. AI recommendation on record: split it — anchor-standing
   (txid binding) as a model/conformance-vector obligation; declared-time
   confinement (existed-by, never priority) as a policy statement plus a
   verifier conformance vector; both itemized in Amendment 3.
