# Exploration note — the per-channel correspondence lemma and the survivor requirement

> **STATUS: WORKING NOTES. NOT A PRE-REGISTRATION, NOT AN AMENDMENT,
> NOTHING DISCHARGED.** This document captures design content that
> surfaced during the author's cold read of the first-link spike's
> correct models (2026-08-09, Tony + Claude Fable 5, same session as
> the floor-structure viability probe). It exists so the reasoning is
> preserved on the record rather than left to memory or a session
> transcript.
>
> Everything here is a **candidate**. One supporting run was informal
> (scratchpad, unregistered — flagged below). Nothing here has been
> registered, reviewed by a non-author, or signed. Do not cite it as
> a commitment. If any of this is to become real, the path is:
> Addendum-2 registration (frozen before runs) → runs → DECISION.md
> design content → the written proof — with non-author review at the
> registration step.

## Provenance

During the cold read of `q1_chain_dns_compromised.pv`, the author
asked whether the recut disjunctive conclusion could be strengthened
per-variant (`Accept ⟹ AuthorityPublishedRepo(t)` in the
DNS-compromised variant). An informal scratchpad run (ProVerif 2.05,
model unmodified except the query, NOT in the repository, NOT
registered) found the specialized query **true**. The author then
constructed the strict-mode asymmetric-compromise attack (Q7's
bindings, repository key leaked, weak DNS as sole honest survivor)
and identified the requirement lurking under A1.3. The dialogue that
followed produced the claims below.

## The stronger claim (candidate lemma)

**Per-channel correspondence:** for every authority channel whose
evidence is consumed by an acceptance and whose signing key is
uncompromised, that channel published the exact accepted authority
tuple.

Universal over consumed-and-honest channels; conjunctive, not
disjunctive. The registered Q1 conclusion — "at least one
uncompromised channel published this exact tuple" — is the corollary
obtained by adding A1.3's nonemptiness guarantee. The lemma tier may
quantify over ground truth (which key leaked) that no relying party
has; the relying-party claim stays disjunctive and is *derived*, not
weakened by the derivation. (The privileged-knowledge objection that
correctly keeps the registered query disjunctive applies to the
relying-party claim, not to the lemma tier — this distinction is why
the recut's refusal of the specialized conclusion and this lemma are
both right.)

## Consequences, stated as reframes of existing results

1. **A1.3 is demoted from source of the guarantee to counting
   assumption.** Correspondence is manufactured per channel by that
   channel's strong first-link binding, independently. "Never all"
   contributes exactly one thing: the honest consumed subset is
   nonempty, so the conjunction has at least one contentful
   conjunct. Redundancy buys nonemptiness — nothing else.
2. **The two registered failure modes become one failure.** Q5b (the
   degraded-mode waiver cost: sole accepted channel compromised) and
   the candidate NC1 below (strict mode, weakly bound survivor) are
   the same event — an *empty effective conjunction* — reached by
   two routes: honesty removes conjuncts, weak binding makes
   conjuncts vacuous.
3. **The boundary invariant is orthogonal and untouched.** Per
   object, unconditional (Q6, both compromise states). Provenance is
   the conditional half; this note is entirely about the conditional
   half.
4. **The relying-party story gains its derivation:** each strongly
   bound channel is an independent provenance root; the relying
   party holds the conjunction over whichever are honest; it cannot
   know which those are; A1.3 — or the recorded waiver accepted in
   its place — prices how many there are at minimum.

## The survivor requirement (the necessity direction)

Author's formulation, 2026-08-09, verbatim:

> It is not enough that some authority remains uncompromised; every
> authority that may become the last honest survivor must itself
> strongly bind the complete authority statement.

The "may become the last honest survivor" qualifier is substantive
scoping, not rhetoric: under A1.3 any channel may be the last
survivor by compromise, and under the A3.2 waiver lattice a waivable
channel may be the sole *accepted* channel by waiver — survivor by
construction. The requirement therefore binds every member of the
A1.5 evidence set that can ever be accepted, strict or degraded, and
would not bind a hypothetical advisory channel excluded from the
floor.

Attack sketch establishing necessity (constructed by the author
during the cold read; not yet mechanized): Q7's configuration (DNS
binds issuer identity only, repository binds h(t)), repository key
leaked. Honest DNS evidence authenticates only issuerId, so it
supports any tuple sharing that identity; the adversary forges
repository evidence for a self-keyed tuple tX and self-signs
possession and bytes. The strict verifier accepts tX; no honest
authority published tX; A1.3 holds throughout (DNS honest). The
weakly bound survivor contributed a vacuous conjunct.

## Relation to registered text

The lemma's universality requirement is arguably already present in
A3.2.1's boundary invariant ("external authority evidence must
unambiguously bind the exact authority statement"). What is new
here: (a) the *dependency* between A1.3 and universal A3.2.1 —
never-all is insufficient without it — which the record nowhere
states; (b) the necessity proof by attack; (c) the lemma-tier
reframe under which the registered disjunction is a corollary.

**Open interpretive fork (author ruling required at registration
time):** whether A3.2.1 quantifies over *deployed evidence formats
at design time* (every channel's format must bind fully, because any
channel may become the survivor) or only over *evidence actually
consumed at verification time*. The survivor requirement resolves
toward design-time universal. If the author judges A3.2.1's adopted
text already unambiguous on this, decision-document tier suffices;
if a future reader could honestly read it the other way, this is a
one-paragraph interpretive ruling under amendment discipline.

## Candidate mechanization (for Addendum-2, if registered)

- **Lemma instances:** per variant, the specialized per-honest-
  channel queries (the informal scratchpad run is the DNS-
  compromised/repo-conjunct instance; it must be re-run under
  registration to count). Predictions: holds, all instances, for
  intact-binding models.
- **NC1 / NC2 (negative controls, companion tier):** asymmetric
  bindings, strong channel compromised, strict acceptance, Q1-style
  events and chain-correspondence query added. Expected VIOLATION —
  the survivor requirement's necessity, mechanical.
- **Flip-side contrasts:** same configurations, weak channel
  compromised instead. Expected HOLDS — same compromise count,
  outcome flips on the survivor's binding strength alone. The
  controlled contrast in the Q7/Q8 idiom.
- **Boundary persistence prediction:** TwoWorldsPair (and single-
  object judges where present) stay UNREACHABLE in all new models —
  provenance dies, the boundary invariant does not; preserves the
  addendum's unconditional-vs-honesty-bought split.

All companion-tier or lemma-tier: nothing here discharges an A1.2
property; the negative controls exist to make a design rationale
mechanical.

## What this does not do

Does not invalidate any registered result: Q1's disjunction stands
as corollary; Q5a is the degraded lemma instance; Q5b's red keeps
its registered meaning; Q6 and the boundary invariant are untouched;
the 10/10 addendum-1 record is unaffected. This note is a
strengthening candidate and a dependency made explicit — upstream of
all discipline, per the status banner.
