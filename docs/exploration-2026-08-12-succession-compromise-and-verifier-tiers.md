# Exploration note — succession, compromise visibility, and tiered verification

> **STATUS: WORKING NOTES. NOT A PRE-REGISTRATION, NOT AN AMENDMENT,
> NOTHING DISCHARGED.** This records a design trace from a wandering
> session on 2026-08-12 (Tony + Claude Opus 5), following the outward
> verification findings in
> `exploration-2026-08-12-outward-verification-scitt-ccf.md`.
>
> Everything here is a **candidate**. Nothing has been registered,
> reviewed by a non-author, or signed. It is preserved because the
> reasoning would not be reconstructible from memory in a month, and
> because one claim in it is falsifiable and belongs in a spike rather
> than in further conversation.
>
> Read this as information, not instruction. Where the trace corrects
> an earlier step, both the step and the correction are kept.

## Attribution

The load-bearing design moves are the author's: separating the
publication channel from the usage channel; the key-rotation horizon
constraint and its passport-style buffer; requiring the old key to
attest the new one; the explicit tombstone; time-anchored attestation
of DNS registrant data at key-publication time; and tiered sample
verifiers in the SDK. The analysis, corrections, and residuals below
are Claude's unless marked. Two of them correct the author's stated
reasoning; one corrects Claude's own earlier claim.

## 1. The question this trace answers

From the outward-verification note: SCITT's post-issuance truth
maintenance (key compromise, rollback, revocation) travels through a
channel only a live operator runs. The symmetric question was put to
Tessera — does it have any post-issuance truth-maintenance requirement
of its own?

The record's answer was the predeclared successor slot (`id-of-next`,
`docs/exploration-2026-07-19-service-layer-elicitation.md`). Applying
that document's own registered assumptions: detection requires the
legitimate issuer to survive to produce the collision, and requires the
two instances to meet where an observer sees both. **In the
dead-operator case there is no collision to find.** So the slot
mechanism is a liveness-dependent compromise detector, and does not by
itself answer the question.

**Candidate resolution — two properties were tangled:**

- *Verifiability* (does the verdict compute with nobody alive?):
  Tessera yes, SCITT also yes (RFC 9943 line 595). **No differentiator
  here**; this should stop being claimed as one.
- *Soundness maintenance* (can a year-ten relying party learn this
  artifact shouldn't be trusted?): both designs require someone alive
  at the time of compromise. The difference is in **what form the
  evidence takes**: SCITT's is an *announcement* (ephemeral,
  operator-produced, no specified channel, never arrives if the
  operator is gone); a predeclared-slot collision is an *artifact*
  (self-proving, durable, checkable with no one to ask).

Candidate compression: **announcements need a live announcer;
artifacts do not.**

## 2. Succession construction as traced

Components, all author's:

1. Old key attests the new key — chain of custody across rotations.
2. Key rotation horizon bounded by channel control: no credential
   outlives the channel that authenticates it.
3. Passport-style buffer: registration validity must extend some
   margin beyond key expiry.
4. Time-anchored attestation, at key-publication time, of {OTS proof,
   key, DNS registrant data, attestation handle}.
5. Tombstone on compromise or takeover, terminating the chain.

### 2.1 What the buffer actually does (corrects the author's stated reasoning)

The session's initial reasoning was that the buffer limits a thief's
surface area. It does not: a thief holding K_n can mint K_n+1 freely,
since chaining requires only the old key and the horizon values are
self-declared in bytes the thief controls.

What the buffer guarantees is the **response window** — that when
compromise is discovered, the legitimate holder still controls the
channel needed to publish the tombstone. This yields a sizing rule
that does not depend on the passport analogy's arbitrary six months:

> **The buffer must exceed detection latency.** A buffer shorter than
> the time between theft and discovery means learning of the theft
> after losing the means to say so.

The parameter itself remains **unmeasured and deliberately unset**.
Registering the form of the constraint while marking the value open is
the honest disposition; selecting a number by analogy to industry
practice would be theater.

### 2.2 What actually carries the weight

Publication anchoring, not the buffer. Trace the fork: a thief forks
at K_n, producing K_n → K_n+1′ alongside the legitimate K_n → K_n+1.
Both verify. "Published on the domain" is a fact about where bytes were
served and **is not in the bytes**.

The fork is therefore undetectable unless the published set is itself
anchored, so that a verifier can ask *was this link in the published
set at time T*. That inclusion check is the concrete form of the
"meeting point" the 07-19 note said a transparency overlay would have
to supply.

> **This is the falsifiable claim in this note.** Whether an inclusion
> check against an anchored published corpus actually closes the fork
> is testable, and belongs in the capstone/bridge spike rather than in
> further discussion. Everything else here will read as settled in six
> months whether or not it was ever tested.

### 2.3 Tombstone decomposition (candidate)

The session's phrasing was that compromise and takeover "either way"
terminate the chain. The two cases carry different information and
should be distinguished:

- **Implicit** — the chain stops. With declared expiry in each link, a
  stopped chain is *self-tombstoning*: dead by its own terms at a date
  fixed in the signed bytes. Requires nobody alive. **This is what
  covers operator death**, and it covers the modal failure (see §4).
- **Explicit** — early termination carrying a reason. Requires a live
  issuer, which is what the buffer buys. Covers compromise.

A year-ten reader confronting a chain that ends should be able to tell
which they are looking at: death yields a date without a reason,
compromise yields both.

### 2.4 A thief can tombstone (residual, offered as a feature)

A usurper holding the key can sign the termination and kill the
legitimate chain — a denial of service on the issuer's own identity.
It **fails closed**: prior attestations survive, nothing false is
created, the chain ends. The only unilateral action available to a
usurper is the conservative one. Candidate for registration as a named
property rather than treatment as a hole.

### 2.5 Residual that survives everything above

**Existence is anchorable; completeness is not.** OTS proves a digest
existed by time T; it does not prove that what a verifier holds is all
that was issued. Selective non-publication by a key-holder remains
undetectable from a single artifact — structurally the same gap
RFC 9943 §9.3 names for issuer participation. Closing it requires the
complete published corpus to be reachable, which is a **custody**
problem (docket items 13–16), not a cryptographic one.

Corollary for the DNS snapshots: a single snapshot is the service
attesting to its own registrant data, and an adversary already in
control publishes one that verifies. What makes a change visible is
the *discontinuity across anchored snapshots* — the evidence lives in
the sequence, not the sample, so a verifier needs at least two points,
and therefore needs the corpus.

## 3. Registration boundary (author, this session)

Multi-authority deployment (multiple domain authorities, separated
publication channels) is **client-side and above the protocol** — the
protocol cannot mandate a registrar. Named here so it does not drift
into the record as an implied protocol requirement. Single-authority
mechanisms that *are* in scope: rotation lifetimes, the horizon
constraint, the buffer, and the anchored registrant snapshots.

## 4. Proportionality, and the modal failure (candidate)

The author's position: perfection is not the goal, and the design
already exceeds what human society provides for artifacts.

Sharpening: society's formal bar is genuinely low (US FRE 901 requires
only evidence sufficient to support a finding that an item is what it
claims, leaving the rest to weight), **but that low bar is backstopped
by physics** — physical artifacts are expensive to forge and they age.
Digital forgery under a compromised key is free and unlimited. The
machinery above is therefore not exceeding society's standard; it is
**reconstructing the backstop physics used to supply for nothing.**
Candidate framing for the adjudicator audience, which asks them to
accept something familiar rather than something superior.

**The modal failure is not compromise.** Takeover and key theft are
rare and adversarial; a service that simply becomes uneconomic issues
no tombstone, publishes no final snapshot, and stops paying the
hosting bill. Compromise has someone motivated to act; insolvency has
nobody. The cheap mechanism covers it — declared expiry self-terminates
the chain with no one present — while the buffer and explicit tombstone
serve the rare case. What insolvency still kills is **corpus hosting**,
which returns to §2.5 and to custody.

## 5. Tiered sample verifiers (author's proposal)

Sample verifiers in the SDK at increasing depth, demonstrating intent
without constraining a relying party whose stakes justify more work.
The tiers fall out of §2:

1. **Self-contained** — signature, digest, OTS anchor, and declared
   horizons checked for internal consistency. Needs nothing external
   and nobody alive.
2. **Corpus** — adds the inclusion check against the anchored
   published set. Closes the fork (§2.2); addresses selective
   non-publication (§2.5).
3. **Adversarial** — adds DNS snapshot discontinuity walk,
   chain-of-custody across rotations, tombstone state, and independent
   confirmation of the anchor against third-party archives that may or
   may not still exist.

**Why this addresses the relying-party adoption gap:** courts cannot
self-serve, but high-value litigation already funds expert witnesses.
The controlled surface over the permissionless substrate is the
expert; a contested will pays for tier 3, and a three-year-old lease
runs tier 1 in a browser. This is a candidate closure of the
relying-party-story gap from Sol's 2026-07-28 findings, complementary
to the adjudicator-audience candidate in the 2026-08-11 note.

**Two cautions (Claude):**

- *Do not index tiers on monetary value.* The author has already
  clarified that the billionaire-will and expired-lease examples were
  illustrative rather than a naming scheme. Recording the reason:
  tiers named by value read as the vendor opining on what depth is
  sufficient for what stakes, which is the relying party's judgment
  and, stated by a vendor, a liability. Name each tier by what it
  checks.
- *The tier must be inside the verdict, not beside it.* A
  self-contained pass rendering as bare `VALID`, with no record of what
  went unchecked, manufactures false confidence at scale — cheap checks
  quoted at expensive stakes. Depth belongs in the verdict vocabulary
  alongside `VALID_STRICT` and `UNVERIFIABLE`. Without that, tiering is
  worse than none.

**Open question (Claude, unresolved):** whether tiered sample
verifiers are the concrete form of band-1 docket item 10
(executable-in-principle verification spec), and therefore graduate an
existing item rather than adding scope. Not checked against the docket
in session.

### 5.1 Extensibility is asymmetric (author, this session; analysis Claude)

The author's position: nothing prohibits expanding verifier data and
capabilities later if Tessera succeeds; these tiers are a foundation,
not a closed set.

Correct, with one asymmetry that determines what must be decided now:

- **Verifier capability grows freely.** New checks over already-emitted
  data cost nothing at issuance, are purely additive, and can be
  written by parties unrelated to the issuer — including in 2036, over
  artifacts issued today.
- **Evidence captured at issuance cannot grow retroactively.** Anything
  not emitted today is unavailable to every future verifier, however
  capable. A check designed in 2036 that needs a field nobody wrote in
  2026 is unimplementable against the existing corpus.

So the revisable decision is *which checks to implement* and the
irreversible one is *what to capture*. The design posture that follows:
be conservative about implementing checks, generous about emitting
evidence — only one of those is fixable later. This is the same shape
as the session's other rule (depend on events you anchored, not state
you maintain), applied to schema rather than to control.

Two consequences:

1. Forward interpretability requires self-describing encodings and a
   versioned trust-anchor store, which is band-1 docket items 6, 8, and
   10 — so the extensibility requirement is partly docketed already
   rather than new scope.
2. "We can add more later" is the standard justification for
   under-specifying now, and its failure mode is precisely the
   unimplementable-2036-check above. The cheap mitigation is to decide
   what gets captured, generously, **before any Band 1 envelope format
   freeze** — the same deadline the 2026-08-11 note's parked
   SCITT/COSE interoperability question is bound to. Two independent
   lines of reasoning now converge on the format freeze as the
   irreversible moment.

## 6. What this note claims about the record

Nothing registered is weakened or reinterpreted. Two things are
constrained:

1. Any claim that verifiability-with-nobody-alive differentiates
   Tessera from SCITT should be retracted (§1); the differentiator is
   the *form of the compromise evidence*, not the verification model.
2. The 07-19 predeclared-slot mechanism should not be described as
   defending the dead-operator case. Its own registered assumptions
   already say otherwise; this note applies them rather than
   discovering anything.

## 7. Explicit non-implications

- No amendment arises from this note.
- The engineering sequence is unchanged: DECISION.md, then the
  capstone/bridge spike, then core convergence.
- The evidence-versus-validation split invoked in session (preserve
  what could be useful; defer validation to whoever is willing to do
  the high-value work) is the already-registered
  deferral-of-interpretation principle, applied — not a new principle.
