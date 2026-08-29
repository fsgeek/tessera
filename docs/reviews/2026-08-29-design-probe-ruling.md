# Author clarification: the scope of "before any code," and the design-probe tier

**Status: clerk-drafted 2026-08-29 from the author's words in session;
becomes RULED (author) on the author's signing commit.** Until that
commit this file records a statement the author made and the
consequences the clerk drew from it; the consequences are PROPOSED.

## What prompted this

The pre-registration says (`docs/phase-0-prereg.md`, Band 0):

> Before any code, the central guarantee is established by a
> machine-checked formal model and proof.

and that Phase 1a opens only on "an explicit, dated, signed commit
declaring the build runway open."

On 2026-08-29 two AI collaborators independently read that sentence at
its broadest — no executable code of any kind before Band 0 exit — and
on that reading diagnosed a sequencing defect: the standing-evidence
construction (A3 §A3.7.1; panel criterion 4 in `FIRST-LINK-SPIKE.md`)
had reduced to a question that abstraction could no longer answer
responsibly ("what does a verifier holding an abandoned attempt
actually lack?"), while the record appeared to forbid the one
instrument that could — a small executable fixture. Codex recommended
an amendment permitting a bounded executable probe; Claude concurred.
Both were reading the text without its author.

## The author's clarification (verbatim, 2026-08-29)

> As for the "before any code" the intent was "before any code
> intended for use in the Tessera service". The idea was that we
> wanted to do our homework first — robust design — but sometimes to
> do that we need to build pieces that aren't part of the final
> construction. I certainly never had any intention of an
> interpretation so broad and illogical.

**RULED (author) on signing:** "before any code" in the
pre-registration means *before any code intended for use in the
Tessera service*. Executable pieces built to do the design homework
and not intended for the final construction were never prohibited.

This is a clarification of the author's own signed intent, not a
weakening of any obligation; it therefore does not require an
amendment under A1.1. It is recorded so that no future reader —
human or model — repeats the broad reading.

## The design-probe tier (PROPOSED consequences, clerk-drafted)

To keep the clarification from becoming a loophole, an executable
design probe under it is bounded the way the record already bounds
its formal probes (`formal/spike/floor-structure/PROBE.md` precedent):

1. **Declared before it is built.** Purpose, fixture, questions,
   predictions, named outcomes, and timebox are written and committed
   before any probe code exists. The committing order is the freeze.
2. **Non-production.** No line of probe code is intended for, or may
   be carried into, the Tessera service. If a construction the probe
   informs is later selected, its Phase 1a implementation is written
   from the *decision*, under H1a evidence rules, not from the probe.
3. **Non-conformance-claiming.** A probe is not evidence that any
   implementation conforms to any model. It is not H1a, not the
   LocalStack slice, not a vertical slice.
4. **Non-discharging.** Probe outcomes are evidence about the *shape*
   of a construction — what a verifier lacks, what a record must bind,
   what breaks under mutation — never about any registered property.
   Nothing in `PROPERTIES.md` changes status because of a probe.
5. **Labeled as such**, in its directory name, its declaration, and
   its results file, so that nothing it produces can be mistaken for
   registered evidence.
6. **Feeds a decision, does not make one.** A probe's findings are
   routed to a mechanism decision under the DECISION.md pattern
   (criteria before evidence, scoring on record); the author decides.

**What is unchanged:** every Band 0 proof obligation; the Phase 1a
runway commit; panel criterion 4 (the chosen standing mechanism is
modeled in the symbolic suite before Band 0 exit); the H1a and H1b
evidence obligations.

## First probe under this tier

`formal/spike/standing-probe/PROBE.md` — declared the same day, to
inform the §A3.7.1 construction choice. Its construction waits for
the author's signing commit on this file.

## Provenance

Author's words: verbatim from session, 2026-08-29. Tier constraints:
clerk-drafted (Claude), drawing on the floor-structure probe
precedent and on Codex's 2026-08-29 recommendation ("freeze its
questions before running it, label every result non-discharging").
The broad reading that made this clarification necessary was the
collaborators', recorded as such.
