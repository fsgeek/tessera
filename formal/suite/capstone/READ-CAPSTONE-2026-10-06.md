# Capstone: what it shows, and three decisions

*Owner instance (Claude Opus 5.5), 2026-10-06. The full record is `RESULTS.md`; you do not need to read
it. About fifteen minutes of reading. Nothing below is committed; your rulings come before the commit.*

> **DEFERRED by the author, 2026-10-07 — no rulings requested now.** His words: *"I think ruling on this at
> this time is premature. I do think we should preserve the results and proposed slicing method for future
> use, but closing the capstone now is premature."* The capstone stays open until the throwaway prototype
> has been used to look for missing implementation details, unsupported assumptions, mismatches with RFCs and
> standards, and defects in the model's guarantees, with each finding sorted into *affects the capstone*
> or *deferred to implementation*. This note is kept as written for when the rulings are due.

## What the capstone establishes, in ordinary language

**Claim.** The five verified pieces of Tessera's checking logic still hold when composed into one verifier.
The five pieces are signer binding (S-P3), integrity (S-P1), signature-set completeness (S-P2), wrapper
soundness (S-P7) and standing. Composition here means one intake, three wrapper layers, two signer slots
and two issuers, against an attacker who controls the network and, depending on the case, holds some of
the keys.

**How we know the check isn't vacuous.** Every place where one piece relies on another (a "seam") has a
deliberately broken companion model, and that companion must go red. A checker that never says red proves
nothing.

**Results, ladder 3** (the corrected model; 69 files ran; no verdict changed from ladder 2):
- **Every correct-form query came out as registered (173 of 173), in all four compromise cases.** This is
  the security result.
- **56 broken companions came out as registered.** 10 have extra reds the registration did not predict.
  They are registration defects, plus one genuine finding (G2: the standing verdict depends on authority
  evidence in the same way acceptance does). None of them is a hole in the correct model.
- **11 degraded-case companions could not finish in ProVerif.** These are the ones meant to show attacks
  when the main signing key has leaked. Question 1 is about them.

**Boundaries.** This is symbolic: perfect crypto, ideal parsing (P8 is separate), and a model of the
verifier rather than the code. It cannot tell us whether the model matches the system we build. Only the
conformance vectors against real code can (A1 §A1.7).

## Decision 1: the eleven unfinished degraded companions

**New since you last saw this.** A ProVerif run on a *cut-down copy* of the same file finds the attack in
seconds to minutes. The cut-down copy has whole honest processes or wrapper layers deleted, and nothing else
changed. This is sound for reds only. Deleting processes can only remove possible executions, so an attack
found in the copy is an attack in the full model. A "safe" verdict in the copy means nothing.
- Codex reviewed the method: *sound with conditions* (`proverif/dev/slice_probe/codex/REVIEW.md`).
- Codex then read the twelve attack traces the exit rows depend on (`…/codex2/REVIEW.md`). None is an
  artifact. Ten are the registered attack. Two (C-C2 link 5 and C-C4 link 6b) are different but valid
  attacks on the same mutation. D1 and D2 also have registered-mechanism reds (C-C2's C-Q3, C-C4's
  `Rescoped`), so no row rests on those two alone. D10 now has real consumer-failure evidence.
- Every cut-down copy of the correct model stays green.

**My recommendation: option (iv).** Amend so that a red found this way, with a reconstructed attack trace,
counts for that companion's registered red set, and for nothing else. That gives the composed model's own
evidence for the rows that currently have none: D1, D2, D5, D10's consuming query, D6 and D7. Whatever the
cut-down runs cannot reach (the greens, and C-C8-i) is carried on the family evidence, as option (i) would
have done. *Where in RESULTS.md:* "ROUTED TO THE AUTHOR — the disposal of the eleven", options (i)–(iv) and
the 2026-10-06 recommendation.

## Decision 2: what time limit a companion runs under

The registration says two different things. One sentence gives each companion "the box of the query it is
predicted to red" (30–60 min). Every run actually used the per-case total, and per-query time was never
logged. **My recommendation (unchanged from 2026-10-01): amend to the per-case total (P).** Say so openly
as an exception entered after the freeze. It costs the claim that each attack shows within 30–60 minutes,
which no run measured. *Where:* "ROUTED … second question".

## Decision 3: under C-C15(i), which key does the standing check refer to?

Two sentences of the registration disagree for one mutation. **My recommendation: (A), the presented inner
key.** That is what was built, the conjunct-3 red then reads as the mutation being caught, and no exit row
moves either way. *Where:* "ROUTED … third question".

## Four clerical corrections to the registration (yes or no, as a batch)

G1 (C-C5 and C-C17 authorship reds), G4 (C-Q2 under C-C15(i)), conjunct 3 to case (d) only, and C-C10/C-C14's
unrestricted C-Q6 into set (1). Each is a red the runs show and the registration failed to list. *Where:*
"Amendment-shaped items" in RESULTS.md.

## What the throwaway prototype found (your idea, built 2026-10-06; `prototype/`)

An issuer and verifier were built from the implementation spec as written, with three consumers on top. All
tests pass (50). These are **not** decisions for this read. They are what the model could not have told us.

- **The good news.** A verifier built straight from spec §5 rejects the C-C2 and C-C5 attacks with real
  signatures, and the broken versions accept them. The spec and the model agree there.
- **Revocation has no source (the one real design hole).** R-5.21 requires "no revocation effective at or
  before `anchor_time`", but nothing a verifier may read carries revocation facts (R-5.8), and live lookups
  are forbidden (R-5.10). The TLA+ model takes `revoked` as given. A revoked-in-window bundle is byte for
  byte identical to an honest one, and the prototype reports the check as "pass". P6 is `checked`, but the
  design still owes where the facts come from. *I need a ruling on this, later and separately.*
- **Relying parties misread the verdicts.** A plausible integrator rule accepted unsafe bundles 6 times in
  20. The worst cases:
  - per-layer verdicts that disagree, with no rule for combining them;
  - degraded mode, where an honest receipt that lost evidence and an attack give identical reports;
  - an impostor's statement verifying `VALID_STRICT`. That is by design (R-1.4: Tessera does not establish
    "this was the package the relying party expected"), but easy to misread.
- **The 2106 examiner cannot reach a verdict** from the bundle as built. Its honest answer is UNVERIFIABLE:
  it is blind to revocation, depends on an archived store the bundle never names, and can't rule out a
  contradictory standing record without a log.
- **The spec fixes no byte layouts.** Two independent builds would agree on no signature, and most of the 50
  guesses are *not* in P8's territory.

Details: `prototype/PHASE1-REPORT.md`, `PHASE2-REPORT.md` (five ranked design questions at the end), and
`PREDICTIONS.md`, written before any code and scored after.

## What this does and doesn't finish

Your rulings close the capstone (exit item E5). **They do not close Band 0.** `BAND0-EXIT.md` lists 17
items. As of its 2026-09-13 snapshot several were not begun: E3 the P8 framing proof, E6, E8 the model
cross-walk, E10 the conformance vectors, E12 the relying-party page, E14. Given what we said on 2026-10-05
about bookkeeping and finishing, my next job after your rulings is to come back with a proposal for the
shortest honest path through that list: which items are real, which can be cut by amendment, and in what
order. The first thing that meets reality, the conformance vectors, should come early.

**To reply:** "1: iv / 2: P / 3: A / clerical: yes" is enough, or tell me where you disagree.
