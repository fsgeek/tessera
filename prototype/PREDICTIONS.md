# What I expect the prototype to show — written before any code (2026-10-06)

*Owner instance (Claude Opus 5.5). These are priors, not a registration. They exist so the prototype can
prove me wrong. Each is scored when the phase it belongs to ends: right, wrong, or could not tell.*

1. **The spec is underdetermined in at least five places** a builder must guess to get running code (byte
   encodings, identifier formats, field order), mostly inside P8's territory. *(phase 1)*
2. **The manifest-versus-authority-tuple abstraction forces a design choice the model never made.** The
   model treats the signed manifest, its hash and the authority tuple as one object. A real manifest with
   more fields will need a stated rule for what is bound to what. *(phase 1)*
3. **A verifier built straight from spec §5 rejects the C-C2 reattribution and C-C5 transplant traces**,
   replayed with real signatures. If it accepts either one, the spec and the model have drifted apart. That
   is the most important outcome this prototype can have. *(phase 1)*
4. **Replaying a symbolic trace concretely will need at least one non-obvious translation.** The adversary
   functions with no real counterpart (`dsks` above all) will have to be emulated, or the trace will not be
   replayable at all. *(phase 1)*
5. **A relying party finds the verdict vocabulary (VALID / INVALID / UNVERIFIABLE, plus standing)
   confusing or insufficient in at least one realistic case.** *(phase 2)*
6. **The 2106 examiner, with no service alive, needs something the bundle does not carry.** This is my
   weakest prior: a guess at where the design is thinnest, not a reasoned prediction. *(phase 2)*

## Phase 1 scoring (owner instance, 2026-10-06, from PHASE1-REPORT.md and GUESSES.md; tests: 25 passed)

1. **Half right.** The count was right: 50 guesses and 7 internal contradictions or tensions. The location
   was wrong: only 18 of 52 entries are byte or encoding guesses, so most of the gaps are *not* P8's. The
   biggest is G-27: R-5.21 requires a revocation check, but no bundle member and no trust-configuration
   member (R-5.8) carries revocation facts, and R-5.10 forbids live lookups. In the TLA+ model `revoked` is a
   given state variable with no carrier. P6 is `checked` in a model that never had to say where revocation
   facts come from. (I confirmed R-5.8's list myself.)
2. **Right.** The binding-form set had to be moved into the attestation's signed bytes before anything
   covered it. The manifest hash and the possession signature cover the authority tuple only.
3. **Right.** The correct verifier rejects both attacks; the mutated one accepts both. C-C5 needs an
   emulated DSKS hook to exist at all.
4. **Right, and with one surprise in the defenders' favour.** The honest frame's signed declared time limits
   C-C2 to about 72 h even against the broken verifier, a defence the untimed model does not see.

## Phase 2 scoring (owner instance, 2026-10-06, from PHASE2-REPORT.md; tests: 50 passed)

5. **Right.** A plausible non-expert integrator rule accepted unsafely 6 times out of 20 runs; a careful rule
   accepted unsafely 5 times and falsely rejected 5 honest receipts. The sharpest cases:
   - C-C5's `VALID_DEGRADED` outer layer beside an `INVALID` inner one, with no combining rule;
   - degraded mode, where an honest receipt that lost its repository evidence and an attacker's receipt
     made with the leaked key give identical reports.
   The "impostor gets VALID_STRICT" case is **by design** (R-1.1, R-1.4: Tessera does not establish "this
   was the package the relying party expected"), but it shows how easily that boundary is misread.
6. **Right, more strongly than I expected.** With the bundle as built, the 2106 examiner's honest answer is
   UNVERIFIABLE. Even with a complete rulebook it cannot see revocation (G-27), must trust an archived
   trust-anchor store the bundle never names, and cannot rule out a contradictory standing record without a
   third-party log, which R-5.10 forbids.
