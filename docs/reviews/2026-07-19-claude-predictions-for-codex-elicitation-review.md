# Pre-registered predictions: Codex review of the 2026-07-19 elicitation notes

Author-side artifact (Claude Fable 5, 2026-07-19), committed **before** the
Codex review of `docs/exploration-2026-07-19-service-layer-elicitation.md`
returned. Purpose: calibration test per the A1 precedent of recording the
AI collaborator's predictions of what an external reviewer will find. To be
compared against the actual review at disposition time. Non-discharging.

Predictions, in descending order of confidence that the reviewer flags it:

1. **The "dissolves the fork" claim (§3) is an overclaim** — the lyrical-tell
   case. Archived plural evidence proves authority *at issue time*; but
   revocation and succession are inherently about *later* information
   reaching verifiers, and no archive inside an old bundle can carry news
   that postdates it. The offline-verification vs. revocation-freshness
   tension (already named in the 07-18 corrections as a real trade) is
   papered over by the word "dissolves." Expected correction: the fork is
   *reframed*, not dissolved; a freshness/countersignature mechanism or an
   explicit staleness policy is a missing component.

2. **The secret-seeded slot variant (§1) is underspecified to the point of
   possible vacuity.** If slot validity is defined only by "matches the
   pre-declared next-ID in the previous node," then after the thief occupies
   the one pre-declared slot, they pre-declare their own successor — and
   nothing in the doc says how a verifier distinguishes seeded-valid slots
   from thief-declared slots without the issuer revealing the seed or a
   commitment to it being registered somewhere. The claimed "cannot even
   name valid slots after it" does not follow as written.

3. **"Provable equivocation" (§1) elides detection vs. adjudication and
   recovery.** Two instances of one (issuer, UUID) prove duplicity of the
   key, not which continuation is legitimate, and the doc says nothing about
   how a lineage *continues* after a detected collision (re-anchor? channel
   re-key event? terminal?). Expected flag: detection without a registered
   recovery rule is an incomplete property.

4. **Staged signing (§4) reintroduces the A2 contradiction pattern between
   stages.** A signed adversary model with unsigned derived properties
   creates a window where downstream artifacts can reference stage-2 content
   as if in force — the exact draft-vs-ratified drift that required the
   break-the-chain decision. Expected correction: an explicit rule for what
   may cite stage-2 material before its signature.

5. **The KERI "strictly stronger" comparison (§1) is loose.** It compares
   different event types (key rotation vs. issuance continuation) and omits
   KERI's witness-receipt infrastructure, which is doing load-bearing work
   in KERI's guarantees. The integration claim (pre-rotation + UUID slots +
   overlay) is asserted, not designed.

Calibration note: if the review's most serious finding is something absent
from this list, that miss is itself the interesting datum and should be
recorded in the disposition.

---

## Scoring addendum (2026-07-19, after the review returned)

Review: `docs/reviews/2026-07-19-codex-service-layer-elicitation-review.md`.

- **Prediction 1 (temporal semantics / "dissolves the fork" overclaim): HIT.**
  The review's "authority section needs temporal semantics" — the misleading
  discovery/verification sentence, activation windows, revocation as a
  safety-vs-availability decision. The review went further than predicted
  (activation rule, verdict classification table).
- **Prediction 2 (secret-seed not verifier-enforceable): DIRECT HIT.** Same
  mechanism predicted (thief supplies own successor slot); the review added
  the structural repair (reveal must authorize rotation → pre-rotation).
- **Prediction 3 (detection vs. adjudication/recovery): PARTIAL.** Recovery
  appears as a column of the review's mechanism table and in the C-ladder,
  but the review's sharper adjacent finding (registry uniqueness can
  *destroy* equivocation evidence) was not predicted.
- **Prediction 4 (inter-stage drift in staged signing): NOT RAISED.** Not
  confirmed, not refuted. Remains a live concern for the structure decision.
- **Prediction 5 (KERI comparison loose): PARTIAL HIT.** The review kept the
  comparison as productive but demoted the fencing-token analogy and flagged
  the vlei.wiki citation as AI-generated (reference hygiene) — adjacent to,
  but not identical with, the predicted witness-infrastructure objection.

**Unpredicted serious findings (the calibration datum):**

1. id-of-next may be redundant with sequence+previous-hash — the review's
   headline. Not predicted at all.
2. The per-issuer serialization / concurrency constraint and the
   control-plane vs. claim-plane split. Not predicted.
3. Evidence-destroying registry behavior (uniqueness enforcement without
   retention destroys the collision proof). Not predicted.
4. The guarantee renaming (row 2 = conditional split-brain evidence, not
   takeover resistance) and the C0–C4 profile ladder. Not predicted.

**Pattern, recorded for future calibration:** the assistant's predictions
caught its own *prose-level* overclaims — places where it wrote a stronger
sentence than the mechanism supported — and missed every *design-level*
finding that required comparing the mechanism against a simpler alternative
or tracing an operational consequence. The assistant predicts its rhetoric's
flaws, not its design's blind spots. This asymmetry is a direct, worked
argument for the non-author gate and should temper any future confidence
the assistant expresses about design-space completeness — including lists
it has already enriched once under pushback.
