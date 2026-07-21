# Clock-precedence ruling — the round-2 sign-blocker, resolved

**Date:** 2026-07-21. **Ruling author:** Tony Mason. **Consultation:**
Codex (GPT-5.6, two rounds, verbatim below); slack-parameter analysis
(Claude; `formal/tla/P5cP5P6_BridgeSlack{,_Latch}.tla`,
predictions-first record in
`2026-07-21-claude-predictions-slack-bench.md`).

## The ruling

Of the three options routed in round 2 (wall wins / chain wins /
two-clock with explicit precedence), the author adopts **separate clock
roles with operational slack and no hard lag assumption** — Codex's
recommendation, with Claude's concurrence on the record:

1. **Chain time governs evidence.** The three-conjunct temporal
   predicate (A2.2) is evaluated identically by issuer and verifier on
   the designated blocks' timestamps.
2. **Wall time governs the attempt lifecycle.** The service waits
   through `declared + δ + S` before treating an attempt as expired;
   refusal (A2.3) is wall-governed. S is an operational slack constant
   joining δ, ε, k, N for Band 0 exit ratification (working default
   S = 24 h — proposed by the assistant, flagged for author
   ratification, sized to the observation path rather than timestamp
   skew alone).
3. **No global backward-lag bound L is registered.** Bitcoin consensus
   provides none (median-time-past + two-hour future rule bound the
   forward direction only), and the observation instant B absorbs the
   entire operational path — network, stores, polling, outages, clock
   error. A Phase 0 registration of L would assert a property of a
   stack that does not yet exist.
4. **The opportunity guarantee is conditional on the observable
   antecedent:** if B − C ≤ S for an attempt whose predicate holds, the
   attempt has a live shipping opportunity at eligibility. B and C are
   both observable, so a violated antecedent is a detectable
   operating-envelope event, not a silently failed assumption.
5. **Lag-exceeded artifacts lose protocol standing, not cryptographic
   validity.** A chain-valid artifact of a refused attempt remains
   verifiable and evidentially admissible; it carries no standing
   (A2.4). Enforcing that distinction against later publication is
   Amendment 3's lineage/equivocation obligation.
6. **Eligibility timeliness is latched at B.** A timely-eligible
   attempt cannot be expired by later packaging/scheduling delay;
   eligible/finalizing, shipped, and expired/refused are mutually
   exclusive protocol states — a construction obligation on the
   implementation (stage-one / A3), not a reason to hold A2 open.
7. **An SLA-style hard L may enter a deployment profile later** — with
   monitoring and an explicit violation outcome — never the Phase 0
   assumption set.

## Author confirmations recorded (closing the round-2 gap)

The two round-1 author-reserved items, confirmed by the author in the
2026-07-21 session and recorded here because the round-2 archive still
read "awaiting confirmation":

- **A2.4 standing narrowing — CONFIRMED** as folded (no validity, no
  priority, no claimed anchor identity; evidentiary use preserved).
- **Double-SHA-256 decline — CONFIRMED** (chain-agnostic txid wording
  declined while Bitcoin/OTS remains the registered construction; all
  three reviewers endorsed the decline).

## Downstream repairs executed with this ruling (same commit)

- A2.1: boundary-tie sentence replaced by per-clock boundary
  registration; clock-roles ruling block added (S, conditional
  guarantee, latch obligation, standing rule, deployment-profile
  deferral).
- A2.3: expiry clock named (wall), lifecycle envelope δ + S, nominal
  budget restated as N × (δ + S); S added to the Band 0 exit
  ratification list.
- A2.0: two-receipts closure claim withdrawn with a dated correction;
  re-registered as an Amendment 3 obligation.
- A2.5: clock-roles analysis artifacts registered; bridge's
  absence-of-lifecycle-guard registered.
- A2.6: change summary extended (rules / withdraws).
- `P5c_IssuanceProtocol.tla` header: single clock re-read as the wall
  clock (S = 0 instance); fused-guard coincidence scoped.
- `P5cP5P6_Bridge.tla` header: RULING block registering the absence of
  a lifecycle guard (chain-evidence seam only).

## Round-3 scope (predeclared, per the bench contract)

Round 3 verifies **discharge of the clock blocker and its consequential
stale text only** — the narrow blocker filter. A genuinely new issue may
still be reported, but re-litigating settled dispositions or opening a
fresh unrestricted falsification round is out of scope. After bounded
verification: sign, commit, anchor.

## Assistant's dispositions on the second consultation

Received-with-verification, not performed agreement: the reframed
conditional theorem is the registered two-line argument with the
assumption relocated to an observable antecedent (verified equivalent);
the observation-path definition of B strengthens the case against hard
L beyond the assistant's own correction (adopted); the latch
mutual-exclusion states are a construction obligation (adopted,
registered in A2.1/A2.3); the bench-soundness assessment matches the
predictions file's own scoring including its recorded miss (concur).

---

## Verbatim: Codex consultation 1 (bench contract, received post-run)

> Claude's sequence is sound and remains inside the single substantive
> blocker. I would give step 1 the go-ahead, but with a written bench
> contract so it cannot grow into another exploratory branch.
> [Three constraints: (1) define the compared times precisely —
> C = confirmed_at, B = wall observation of the designated block,
> L = max backward lag, S = slack; the lifecycle decision must use or
> atomically latch B, not Ship's execution time, else the scheduler
> manufactures expiry (modeling artifact, not the clock question).
> (2) Do not call L a consensus timestamp-lag bound: Bitcoin gives
> median-time-past plus the two-hour future rule, not a symmetric
> finite bound; L is an environment/threat-model/operational-policy
> assumption, else the model dissolves the divergence by assuming away
> the difficult half. The honest conditional result: "Under a declared
> maximum backward timestamp-lag assumption L, slack S ≥ L makes every
> chain-timely attempt operationally timely at eligibility."
> (3) Predeclare stopping outcomes: viable-with-defensible-L /
> assumption-unwilling-to-register means slack has not solved it /
> failure-inspect-scheduling-then-rule; "empty exactly when S ≥ L" is
> a general result only with an argument beyond parameter instances.
> Provisional architectural preference: separate roles with explicit
> precedence — chain time governs the stateless verifier predicate,
> wall time governs waiting-before-refusal, refusal removes standing
> not cryptographic validity, enforcement via A3 lineage. Accepts that
> A2.2 + A2.4 alone do not prevent two verifiable receipts; the A2.0
> closure sentence should be withdrawn or deferred, not rescued by
> rhetoric. Step 5 explicitly bounded: verify blocker discharge, not a
> fresh unrestricted round.]

## Verbatim: Codex consultation 2 (the clock question)

> Claude has addressed my concrete model concerns. The slack result is
> now honestly conditional, and the latch variant removes the
> scheduler artifact. My remaining insight is that the choice is not
> actually binary.
> I would not register a global finite L as a foundational Layer 2
> assumption in A2. I would retain the theorem, retain S as an
> operational parameter, and state the guarantee conditionally on the
> observed lag.
> [Why: L is structurally registrable but is an environmental
> availability assumption, not computational or consensus-derived; its
> failure does not break cryptographic safety, only late eligibility;
> B and C are comparable, so the violation is observable — an
> observable operating-envelope violation is better modeled as an
> explicit branch than assumed never to occur.
> Choices: register hard L (valid but brittle) / slack S without
> assuming L, late chain-valid artifacts receive no standing
> (preference) / chain time controls termination (undermines
> bounded refusal).
> The middle option preserves the experiment's value: "If B − C ≤ S,
> every chain-valid attempt has a timely shipping opportunity. If
> B − C > S, the service may refuse; the artifact can remain
> cryptographically valid but lacks protocol standing." A theorem with
> an observable antecedent, not an assumption nature must satisfy.
> Two details: (1) define B operationally — service observation time
> includes backward skew, network/store delay, polling, outage
> recovery, wall-clock error; an objective network-arrival B may not
> be implementably observable. (2) Latch semantics creates a real
> commitment: eligible/finalizing, shipped, expired/refused must be
> mutually exclusive; the implementation contract must prohibit
> refusing an attempt whose timely eligibility latched — a downstream
> construction obligation, not a reason to keep A2 open.
> Bench soundness: opportunity vs outcome distinguished; S = L passes;
> S < L has a targeted counterexample; cutoff exercised; the general
> iff correctly identified as argument plus bounded checking.
> Recommendation: (1) separate clock roles; (2) finite slack S as
> operational grace; (3) no global finite backward-lag assertion;
> (4) register the conditional opportunity guarantee B − C ≤ S;
> (5) lag-exceeded artifacts get no standing while acknowledging
> cryptographic validity; (6) A3's lineage/standing mechanism enforces
> the distinction; (7) an SLA-style L belongs in a deployment profile
> with monitoring and an explicit violation outcome, not Phase 0.
> This resolves the clock blocker without assuming away its difficult
> half, and does not require another exploratory round.]
