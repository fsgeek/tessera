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
