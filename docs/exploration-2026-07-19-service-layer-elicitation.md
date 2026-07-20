# Exploration notes — service-layer elicitation (issuer continuity, succession, registration structure)

> **STATUS: WORKING NOTES. NOT A PRE-REGISTRATION, NOT AN AMENDMENT, NOTHING
> DISCHARGED.** Session of 2026-07-19 (Tony + Claude Fable 5). Companion to
> `exploration-2026-07-18-causal-dag-commons.md`; same rules: everything here
> is a candidate, decisions marked as such are the author's, and the path to
> reality is adversary model → properties → formal discharge → non-author
> falsification → signed registration.
>
> Purpose: capture the service-layer design elicited from the author's memory
> before it evaporates again. The prior version of this design survived only
> in the author's head after the AI conversation that developed it was lost —
> this document exists so that failure mode is not repeated a second time.
>
> **REVISED 2026-07-19 after non-author review (Codex, dispatched by the
> author; archived verbatim with disposition in
> `docs/reviews/2026-07-19-codex-service-layer-elicitation-review.md`).**
> Corrections folded in place with `CORRECTED` / `SHARPENED` blocks;
> originals preserved. The most serious, none of which the assistant
> predicted (calibration scored in
> `docs/reviews/2026-07-19-claude-predictions-for-codex-elicitation-review.md`):
>
> 1. **id-of-next may be redundant** — a sequence+previous-hash rule appears
>    to give the identical split-brain property; the UUID must earn its keep
>    on separate operational grounds or be dropped (§1).
> 2. **The secret-seeded variant was wrong as written** — not
>    verifier-enforceable (§1; predicted by the assistant's pre-registered
>    prediction 2).
> 3. **Concurrency semantics were missing** — "each signed package"
>    silently serialized all issuance per issuer (§1c).
> 4. **A uniqueness-enforcing registry can destroy the very equivocation
>    evidence the mechanism exists to create** (§1b).
> 5. **The row-2 guarantee is renamed**: conditional split-brain evidence,
>    not takeover resistance (§2).
>
> Verdict carried forward: mature enough to begin stage-one registration;
> NOT mature enough to freeze mechanisms. Next elicitation exercise: the
> four-mechanism × four-trace comparison (§5).

## 1. The id-of-next design, recovered (row 2: issuer continuity)

The author's original design: each signed package pre-declares a UUID — "the
next identifier I'll use" — as a pre-registration of the successor slot.

**Mechanism (corrected from the assistant's initial mis-model):** the next-ID
is *public*, inside the current signed bytes. It is not a secrecy mechanism;
it is a *forcing* mechanism. Any continuation claiming legitimacy must occupy
the pre-declared slot:

- **Thief takes the slot** and the legitimate issuer is still publishing →
  two signed instances of one (issuer, UUID): *provable equivocation* under
  the lineage rule, not deniable concurrency.
- **Thief avoids the slot** → their validly-signed node does not occupy the
  declared successor position, and a verifier applying "the continuation of
  N is whatever bears N's declared next-ID" rejects it *as lineage* without
  detecting anything.

This is the fencing-token / generation-number move applied to issuance
lineage. Note the standing of the 07-18 doc's worst-error correction: the
Codex correction said DAG topology cannot detect takeover *unless* the
protocol defines "a unique causal position at which only one event is
permitted." id-of-next **is** that mechanism. The correction independently
derived the necessity of a design it did not know existed.

> **CORRECTED 2026-07-19 (Codex review).** Two repairs to the paragraph
> above. *(a) The fencing-token analogy is wrong* — a fencing token works
> because the protected resource remembers the greatest accepted generation
> and rejects stale actors; the UUID creates an exclusive *evidentiary*
> slot but fences nobody out. Exact term: **predeclared successor slot**
> (or "forward slot commitment"). *(b) id-of-next is overcredited* — the
> earlier correction derived the need for a unique position, not for a
> forward UUID specifically. A plain sequence rule
> (`S.issuer = N.issuer ∧ S.sequence = N.sequence+1 ∧
> S.previous_hash = hash(N)`) appears to yield the identical split-brain
> property: both make two distinct successors evidence of equivocation,
> both reject off-lineage successors, both fail under silent usurpation,
> both require the conflicting versions to meet. The UUID earns its place
> only if it demonstrably supplies a *separate* property — registry-slot
> reservation before the successor exists, unlinkability until
> publication, sparse/sharded issuer lanes, or commitment to a separately
> generated succession credential. If none is required, it is extra state
> without extra security. **Open comparison — mechanism NOT to be
> registered yet.**

**Layer placement (repairs the 07-18 drop):** the 07-18 notes discarded
id-of-next because "a DAG has many concurrent children, so 'the next' is
undefined." That conflated rows: the *claim graph* (row 4) is a DAG with
legitimate concurrency; the *issuer's continuity thread* (row 2) is linear
per issuer. id-of-next is a row-2 mechanism and was dropped from the wrong
row.

**Two assumptions that must be registered as such:**

1. **The legitimate issuer survives to produce the collision** — this
   defends the split-brain case (its original name), not silent succession.
2. **The two instances meet somewhere an observer sees both** — detection,
   not auto-discovery (author's phrasing). In an unowned commons the same
   UUID can live in disjoint gossip partitions indefinitely. Synthesis: the
   next-ID in the signed bytes is the *rule* (portable, offline-checkable,
   survives operator death); a transparency overlay (row 3) is the *meeting
   point* where slot-occupancy is recorded and collisions become
   discoverable. Each half covers the other's weakness.

**The nonce refinement (author, this session):** the attacker's
gossip-exposure compounds with each forged message only if slot names are
generated deterministically for the chain's lifetime. Two distinct variants:

- **Public-deterministic** (next slot derivable from public chain state):
  every future slot is watchable; a forged continuation collides or is
  invalid-by-rule at *every* position, not just the first.
- **Secret-seeded** (slots derived from a nonce only the issuer holds): the
  signing-key thief can occupy the one pre-declared slot but cannot *name*
  valid slots after it. The nonce becomes a succession credential distinct
  from the signing key — a second thing that must be compromised
  concurrently (the attacker-cost currency of 07-18 §7 item 7). Cost: a new
  loss-of-continuity point, folding into the succession story.

> **CORRECTED 2026-07-19 (Codex review; assistant's pre-registered
> prediction 2 called this).** The secret-seeded claim above **does not
> follow as written** — it is not verifier-enforceable. If N publicly
> declares slot U1, the thief occupies U1 with forged S1 (valid stolen-key
> signature) and writes an *attacker-chosen* U2 into `S1.next_id`; no
> verifier can know U2 was not seed-derived. A secret matters only when its
> use is publicly verifiable (commitment chain `C = H(secret, context)`
> with reveal, or a VRF) — and even then a reveal-race remains unless the
> revealed secret *authorizes a simultaneous key rotation*, so the stolen
> current key stops sufficing. That repair is precisely KERI pre-rotation's
> structural advantage: the succession credential is a precommitted,
> **unexposed signing key**, not a hidden identifier. Likewise the
> public-deterministic variant protects future slots only if the entire
> schedule is bound by an earlier uncompromised event or fixed public
> rules — if each successor chooses its successor's slot, the thief owns
> the schedule after one occupation. Any VRF/commitment-chain design must
> be evaluated *against simply adopting pre-rotation*, not assumed.

**Prior art (structure-checked this session, not assumed):** KERI
pre-rotation. Each key event pre-commits a digest of the *next* keys; a
rotation is valid only if it reveals and is signed by the pre-committed
keys; recovery from current-key compromise is rotation to the pre-committed
unexposed keys. For key events this is strictly stronger than the UUID slot
(the thief lacks the successor credential entirely). Natural row-2 design:
KERI-style pre-rotation for *key* succession + UUID slots for *issuance*
succession + transparency overlay as meeting point. Refs:
<https://identity.foundation/keri/kids/kid0005.html>,
<https://www.vlei.wiki/concept/rotation>, <https://arxiv.org/pdf/1907.02143>.

> **CORRECTED 2026-07-19 (Codex review — reference hygiene).** The
> vlei.wiki rotation page self-identifies as AI-generated and warns it may
> contain hallucinations: it is **demoted to secondary orientation
> material**, not evidence. The official KID-0005 description and the KERI
> design paper carry the claim — and even they are *prior art*, not an
> externally proven security result. (The "structure-checked" label above
> was earned for the mechanism description, not for the integration claim,
> which remains a design assertion pending the §5 comparison exercise.)

### 1b. Registry behavior at the meeting point (Codex, 2026-07-19 — new)

A transparency overlay that merely **enforces uniqueness can destroy the
evidence**: if it accepts the thief's first insertion and silently rejects
the legitimate issuer's duplicate, no public equivocation proof ever exists.
The overlay must retain both valid conflicting submissions — or issue a
signed rejection receipt committing to the rejected object. Minimum
protocol surface: a lookup key (issuer, epoch, sequence/slot); an
append-only record of every syntactically valid submission attempt;
inclusion promises/receipts; consistency and checkpoint proofs; explicit
conflicting-occupancy behavior; monitors that receive collision events;
bounds on checkpoint/witness/detection delay; retention preserving both
sides of a conflict. "Meeting point" is a **protocol, not a metaphor.**
(Aligned with IETF Key Transparency architecture on split-view detection:
<https://datatracker.ietf.org/doc/draft-ietf-keytrans-architecture/>.)

### 1c. Concurrency semantics (Codex, 2026-07-19 — new; was silently missing)

"Each signed package declares its successor" gives each issuer **one
globally serialized issuance stream**: one worker finalizes at a time;
coordination around the chain head; a stalled issuance blocks later ones;
partitioned issuer infrastructure *naturally produces equivocation*; backup
restore risks slot reuse; high-volume issuers need lanes or sequence-range
allocation. The cleaner split:

- **Control plane:** one linear key-event lineage per issuer.
- **Claim plane:** concurrent attestations bound to an issuer-key epoch.
- **Optional issuance-transparency plane:** ordered/sharded registry
  positions where completeness of issuer output matters.

**Guarantee distinction that must appear in any property statement:** if
only key events are linear, the system detects unauthorized *succession*
but does NOT detect arbitrary claims minted by a stolen currently-authorized
key. If every ordinary attestation must live in the linear thread to expose
stolen-key issuance, that serialization cost must be accepted explicitly.

## 2. Decision candidate (author, this session): the doppelganger exclusion

Silent usurpation — key stolen *and* issuer silenced/coerced/dead, thief
continues cleanly in-slot — is **explicitly excluded** from the row-2 threat
model as a declared residual risk (precedent: A1.3's insider boundary).
Solutions exist (witness cosigning, threshold control, delayed activation)
but all are standing infrastructure: a later band that prices out one more
adversary capability, not a requirement now. Author remains open to
solutions if cheap ones surface. NOT yet registered — candidate only.

> **SHARPENED 2026-07-19 (Codex review).** Excluding silent usurpation
> **renames the guarantee**, and the rename must be prominent, not
> residual prose: row 2 does not establish "issuer continuity against
> takeover" — it establishes *"lineage conformance and split-brain
> evidence, conditional on continued honest publication and observer
> convergence."* Still useful; much narrower; the excluded case is close
> to the original motivating adversary. Two additions accepted on the
> record: **(a)** a cheap partial mitigation exists — short-lived online
> issuance-key epochs + precommitted offline rotation keys bound a silent
> usurper to the current epoch (limits duration/damage without synchronous
> witnesses); **(b)** the all-or-nothing future band is replaced by a
> **profile ladder**: C0 wrong-slot continuations rejected offline; C1
> split-brain equivocation provable when versions meet; C2 current-key
> compromise recoverable via precommitted rotation keys; C3 compromise
> bounded by epoch/key expiration; C4 silent usurpation resisted via
> witnesses or threshold control.

## 3. Succession and the authority root (fork dissolved by the record)

The elicitation fork was: channel-rooted authority vs. self-certifying log
with channels as witnesses. The *registered* design (Amendment 1, authority
section) is a third thing that dissolves it: **plural archived evidence** —
two external authority evidences (DNSSEC chain snapshot for `wamason.com`;
anchored public-repository commit with OTS proof) archived *in the bundle*,
plus manifest self-signature as possession-only. "DNS and repositories are
discovery mechanisms, not verification mechanisms" — no live channel is in
the trust path; authority is the archived plural evidence at each event's
time.

Extension to succession (candidate): a key event (revocation, re-key) is
itself a published, anchored, plural-channel-evidenced statement; the
key-event log is the sequence of such archived events; id-of-next slots and
pre-rotation digests ride inside each event as the internal succession rule.
Channels disagreeing at one instant → fails VALID_STRICT. Internal lineage
disagreeing with channel evidence → a detectable, policy-classified event.

**Residual that carries forward and worsens:** correlated control. The
adversary who owns the author's operational sphere owns both revocation
channels too. Same misissuance boundary as A1.3 item 7; must be named in the
service-layer adversary model, not inherited silently.

> **CORRECTED 2026-07-19 (Codex review; assistant's pre-registered
> prediction 1 called the direction).** Two repairs to this section.
> *(a) The fork was reframed, not "dissolved," and the quoted registered
> sentence is misleading as deployed here:* live endpoints are not
> verification dependencies, but their **archived authenticated statements
> absolutely are verification inputs and authority roots**. Corrected
> statement: *"Live channel availability is not required for verification;
> archived authenticated channel evidence remains part of the authority
> basis."* *(b) "Channels disagreeing at one instant" is underspecified* —
> DNS publication, repository commits, OTS anchoring, and Bitcoin
> confirmation share no instant. A key event needs an **activation rule**,
> e.g.: a transition becomes VALID_STRICT only after the bundle contains
> matching, independently valid publications of the exact event digest
> from every required authority channel, each anchored within the
> transition window. Verdict classification: evidence present and
> contradictory → INVALID; required historical evidence unavailable →
> UNVERIFIABLE; channels agree but lineage rule fails → INVALID; channels
> and lineage agree → eligible for VALID_STRICT; old/new authority
> overlapping during staging → an explicit transition state. **Open
> author decision (safety vs. availability):** if one authority channel is
> unavailable during revocation — does the old key remain authorized, does
> the new event stay unverifiable, or does issuance halt? Also accepted:
> the two channels must never be described as independent against coercion
> or total operational compromise — different failure modes, same human
> administrative root.

## 4. Registration structure — the open decision (with the decision space)

The author challenged the assistant's three-option list (single program doc /
per-row docs / adversary-indexed bands) as possibly incomplete. Correct: the
list varied granularity while silently fixing other dimensions. The honest
decomposition:

- **Granularity:** one document; per-row documents; staged (adversary model
  first, properties second).
- **Organizing principle** (07-18 §7 q5, deferred there and still open):
  layer rows; adversary-indexed bands; guarantee lattice; cost-denominated
  bands.
- **Relation to existing registration:** new sibling registration (the
  07-18 §8b endorsed disposition) vs. amendment extending Band 0 (rejected:
  keep Band 0 narrow).
- **Timing:** register now vs. remain in working-notes mode until stable.
  (Mitigated regardless by committing captures like this one immediately.)
- **Methodology inside the document** (orthogonal): bespoke A1.3-style prose
  adversary model vs. structured methods (attack trees, STRIDE-per-element,
  SCITT role mapping) — can be combined.

Current assistant recommendation (not yet accepted): single-document *scope*
(seams between rows must live inside one reviewed artifact — every recurring
Band-0 finding was a composition failure), delivered in *stages*: register
the adversary model + row-handoff table first (short, high-quality review
cycle; properties then derive from a *reviewed* adversary model — same
ordering logic as not building the bridge model against an under-review A2);
properties follow as a second signed stage. Each row's section must state
what it hands to adjacent rows and what it assumes from them (the P5c↔P5P6
lesson applied at birth). Exit condition per stage: non-author review +
author signature — understanding is the gate; discharge is scheduled
separately.

> **REVISED 2026-07-19 (Codex review) — two amendments accepted into the
> recommendation.** *(a)* "One reviewed artifact" need not mean one file:
> a **signed registration manifest binding several row documents plus a
> seam/handoff matrix atomically** gives local readability without letting
> composition obligations escape. *(b)* An adversary model cannot be
> meaningfully reviewed without knowing the protected assets and intended
> guarantees; stage one must therefore contain: assets and security
> objectives; actors, trust roots, and trust boundaries; adversary
> capabilities and exclusions; provisional guarantee profiles; row
> handoffs; and **explicitly unclaimed properties**. Organization: a
> **matrix** (rows: receipt, continuity, transparency, claim graph,
> process assurance, survivability × columns: attacker capabilities /
> guarantee profiles; cells: mechanism, assumption, handoff, residual)
> rather than committing to one axis — cost estimates stay metadata; a
> guarantee lattice can be derived later if the profiles form one. The
> assistant's unresolved concern (its pre-registered prediction 4, not
> addressed by the review): staged signing must carry an explicit rule for
> what may cite stage-2 material before its signature, or the A2
> draft-vs-ratified drift recurs between stages.

## 5. Open questions register (this session's additions)

1. Public-deterministic vs. secret-seeded slot generation (or both, per
   epoch?). Interacts with the succession story and the attacker-cost model.
2. What exactly does the transparency overlay attest about slot occupancy,
   and under what observer/retention/non-collusion assumptions (07-18 §2
   bounded detectability)?
3. Succession legibility: full design of key-event statements (format,
   channels, anchoring) and their verifier policy classification.
4. Whether the doppelganger exclusion (§2 above) is ratified as registered
   text or narrowed by a cheap mitigation first.
5. Registration structure decision (§4 above) — routed to the author.
6. **The four-mechanism × four-trace comparison (Codex — the next
   elicitation exercise, before any slot primitive is chosen):** evaluate
   {sequence+previous-hash, public next-UUID, verifiable secret commitment,
   precommitted next key (pre-rotation)} against {wrong slot; correct slot
   with issuer live; correct slot with issuer silent; recovery after key
   theft}. Reviewer's provisional table: the first two mechanisms are
   *identical* on all four traces (rejects / equivocation / accepts thief /
   none) — if that holds, the UUID is omitted unless it supplies a separate
   operational property; secret-commitment turns on a reveal-race and a
   loss/recovery problem; pre-rotation uniquely constrains rotation and
   permits legitimate recovery while leaving current-epoch claims
   forgeable. If secret succession is wanted, the verification equation
   must be specified before choosing the primitive.
7. Safety-vs-availability rule for revocation under partial channel
   unavailability (§3 CORRECTED block) — routed to the author.
8. The frontier taxonomy from the review's follow-up exchange (engineering
   edge / research edge / epistemic-institutional edge) as a candidate
   organizing lens for which service-layer claims are *claimable* at all —
   with the reviewer's caution: proximity to the frontier is not permission
   to invent mechanisms confidently; the contribution is honest borders.

## 6. Author rulings (2026-07-20, resolved in walk-through with Claude)

> **STATUS OF EVERY RULING IN THIS SECTION: AUTHOR-ADOPTED FOR STAGE-ONE
> DRAFTING; NOT RATIFIED.** (Corrected 2026-07-20 after round-3 Codex
> review — the original text called Ruling 2 "RATIFIED," which violated
> that ruling's own citation rule while the document's banner says
> working notes. Nothing here is ratified until its hash appears in a
> signed, anchored registration manifest.) Round-3 findings folded below
> as CORRECTED blocks; review archived at
> `docs/reviews/2026-07-20-codex-rulings-review-round3.md`. Findings 6–7
> reword the author's own recorded rationale and analogy and are applied
> **pending the author's confirmation**, marked as such.

**Ruling 1 — revocation under partial authority-channel availability
(resolves open question 7).** Author's frame: Tessera's role is to make
risk *legible*, never to dictate verifier policy — the A1.2 "delta belongs
to the verifier" principle extended from time-tolerance to key state.
Resolved position (author: "a responsible position for stage one," with
room to tighten later):

1. **Verifier side — expose, never dictate.** Transition type
   (planned/reactive), verdict classification (VALID_STRICT /
   VALID_DEGRADED with exact waived evidence named / UNVERIFIABLE /
   INVALID), and evidence freshness (checkpoint age against a
   bounded-staleness policy) are *published signals* in the
   continuity-profile evidence surface. Interpretation belongs to the
   relying party per their risk tolerance.
2. **Issuer side — planned/reactive split.** Planned transitions
   pre-publish evidence and activate at pre-committed epoch boundaries: no
   halt. Reactive transitions halt issuance for the gap's duration — not
   as policy taste but by trace: the reactive trigger (observed revocation
   intent) makes the signing key *suspect*, and a suspect key cannot
   trustworthily label its own output, so there is nothing legible the
   issuer can say with it during the gap.
3. **VALID_DEGRADED is verifier-side only** — a relying-party policy
   naming the waived evidence; never an issuer-side license to issue under
   suspended lineage, and never a redefinition of strict validity.
4. **RECOVERY is an explicitly open mechanism** for stage-one drafting
   (candidates: pre-committed recovery keys; re-origination via surviving
   channels with an explicit successor-of link; terminal + new identity).
   Timeout value and its owner defined in stage one.

Codex's round-2 state machine is adopted as the *reactive* path; the
planned path is the amendment that prevents routine rotations from being
recurring self-inflicted outages.

> **CORRECTED 2026-07-20 (round-3 review, finding 1).** Four repairs to
> Ruling 1 as stated above. *(a)* VALID_STRICT/VALID_DEGRADED/
> UNVERIFIABLE/INVALID are **policy-computed judgments, not raw
> signals** — and Band 0 already uses that vocabulary for receipt
> validity, so one receipt can legitimately be VALID_STRICT under its
> issue-time context and UNVERIFIABLE under a continuity profile *at the
> same evaluation*. Stage one must separate: immutable evidence
> observations; protocol transition state (ACTIVE / PENDING / SUSPENDED /
> RECOVERY / TERMINAL); `ReceiptVerdict`; and
> `ContinuityVerdict(profile_id, evidence_snapshot_hash, evaluated_at)`.
> Relying-party discretion is bounded by the registered waiver lattice
> (A1 §304): non-waivable unperformable checks stay UNVERIFIABLE.
> *(b)* Planned-vs-reactive is **derived from trace evidence, never an
> issuer-supplied label** — otherwise a thief marks the takeover
> "planned." *(c)* If the activation boundary arrives before every
> planned publication converges, the path enters SUSPENDED — the
> unqualified "planned transitions: no halt" was a fail-open statement.
> *(d)* "Observed revocation intent" needs an exact authentication
> threshold; if one recognized-but-compromised path can suspend the key,
> that availability attack is accepted only as an explicit safety trade.
> RECOVERY may stay undesigned in stage one **only** registered as
> unclaimed with SUSPENDED → TERMINAL as the complete current behavior —
> a recovery *transition* in the machine requires designed authorization
> and entry/exit conditions, not a candidate list.

**Ruling 2 — registration structure (resolves open question 5 / §4).**
AUTHOR-ADOPTED FOR STAGE-ONE DRAFTING (label corrected from "RATIFIED" —
see §6 status note): manifest-bound multi-file staged registration per the Codex
round-2 recommendation — root manifest binding every component file by
hash with per-file normative status, the seam/handoff matrix as
first-class content, `WORKING → REGISTERED → DISCHARGED / SUPERSEDED`
lifecycle, the inter-stage citation rule (unsigned stage-two material is
non-normative candidate material; nothing downstream may call it
registered/ratified/required/discharged until its hash appears in a
signed, anchored manifest), stable identifiers allocatable in stage one
without wording import, and repairs only by new manifest version. Plus
the author-confirmed clarification: **the manifest is the sole authority
on normative status** — file banners are convenience copies; on conflict
the manifest wins and the conflict is a bug in the file ("banners can be
forgotten, text ambiguities present; it is the manifest that
determines"). Signing authority: the author, as with amendments.

Author's forward note, registered as a future evolution rather than a
stage-one requirement: manifest *structure* should tend toward making
ambiguity impossible to encode — a later manifest version could adopt a
DSL that limits or eliminates encoding ambiguity. Registered with the
author's own epistemic caveat: mathematics teaches that ambiguity and
undecidability arise regardless (Euclid's fifth postulate, the axiom of
choice, the continuum hypothesis, the halting problem) — so the DSL's
honest target is syntactic/status unambiguity by construction plus
*detection and forced explicit resolution* of semantic ambiguity, not its
impossibility.

> **CORRECTED 2026-07-20 (round-3 review, findings 2 and 7; finding-7
> wording PENDING AUTHOR CONFIRMATION).** *(a)* The single lifecycle enum
> conflated three orthogonal axes, now separated: **component role**
> (normative / informative / candidate), **registration state** (working
> / registered / superseded), **property discharge** (open / modeled /
> checked / discharged) — a registered document can hold undischarged
> obligations; a discharged registration can be superseded. *(b)*
> "Manifest wins" is an interpretation rule but insufficient for
> validation; strengthened to: *the manifest is authoritative, and any
> duplicated status metadata must agree with it — disagreement is a
> validation failure* (a conforming tool rejects the bundle). Schema
> obligations for stage one: role+state assignment (hash inclusion alone
> is insufficient), canonical manifest encoding, detached signing or
> equivalent non-self-referential construction, manifest identity, and
> authenticated supersession. *(c)* Finding 7, RESOLVED 2026-07-20 by
> synthesis after the author disputed the removal (was CH not exactly "a
> statement that can neither be proven nor refuted"?): the author and the
> reviewer were using **two different, both-legitimate senses of
> "ambiguity."** *Interpretive (sentence-level):* a statement admits
> multiple readings — the P5c "confirmed within δ" fork. CH is NOT this:
> its meaning is exact. *Referential (theory-level):* the axioms fail to
> pin down their subject — models of ZFC exist where CH holds and where
> it fails, so "the universe of sets" has multiple non-isomorphic
> referents (the set-theoretic multiverse view). The author's examples
> are this kind. *Undecidability* (halting) is a third bin, bounding what
> checking tools can promise. Three phenomena, three DSL responses:
> **eliminate interpretive ambiguity by construction; surface referential
> underdetermination and force the fork to be registered** (as
> mathematics did: ZF+CH and ZF+¬CH both studied, chosen per context —
> the amendment mechanism); **bound tooling claims** where checking is
> undecidable. The author's examples are retained, correctly filed,
> rather than removed.

**Ruling 3 — the mechanism-comparison exercise (resolves open question
6): ADOPT AND SCHEDULE.** The four-mechanism × four-trace comparison plus
Codex's two operational checks and per-mechanism record schema is adopted
as the mechanism-selection discipline for the successor-slot, scheduled
as its own design session (the author intends to force the AI
collaborators to trace failure states so they can be reasoned about
together). The shortcut — adopting the reviewer's provisional baseline
without the exercise — is REJECTED, with the author's rationale recorded
as a standing principle: *a failure on a scenario the record shows was
already hypothesized is not an honest mistake but a betrayal of the
representations made to the service's users; mistakes happen, but
declining to address a foreseen risk is a different category of wrong.*
Note the mechanism this project gives that principle: the anchored record
makes foreseen-vs-unforeseen auditable, so the distinction is enforced by
the architecture, not by memory or goodwill. Stage-one skeleton drafting
(assets, objectives, actors, exclusions — nothing mechanism-dependent)
may proceed before the exercise runs.

> **CORRECTED 2026-07-20 (round-3 review, finding 6; CONFIRMED by the
> author 2026-07-20 as "a language level clarification. Quite
> reasonable").** The
> principle as stated moralizes *accepted* residual risk: engineers
> legitimately identify risks whose mitigation would create greater cost,
> harm, or fragility, and a later occurrence of an analyzed, disclosed,
> bounded, explicitly-accepted risk is not dishonesty. Sharpened form:
> *allowing a foreseen risk to remain **without analysis, disclosure, and
> an accountable acceptance decision** is a breach of the representation
> made to users; an explicitly accepted residual risk is not an
> unanticipated failure — but neither is it concealment.* Also corrected:
> the anchored record does not *enforce* the distinction; it preserves
> the evidence that makes it auditable and supports accountability —
> which is still the substantial contribution.

**Ruling 4 — A2 review dispositions 1–2 (Band 0): ACCEPTED**, recorded at
the disposition itself in
`docs/reviews/2026-07-07-codex-amendment-2-review.md` (FLP rationale;
`Refuse` path; `_BrokenSilent` red-bar companion as the
not-manufacturing-silence evidence). P5c refusal-state work unblocked.

**Ruling 5 — A2.4 discharge paths (Band 0, resolves the review's
disposition 3): the REFINED split accepted** — after the author
conditioned acceptance on exhaustive analysis, the assistant's honest
re-enumeration found four omissions and strengthened the recommendation
(the condition working as designed; "the pressure to produce quickly
often weighs against exhaustive analysis" — author):

- **Anchor standing:** `[proof]+[vector]` obligation, distinct tracker
  line cross-referencing P8, **plus a named ProVerif lemma rider on P2**
  ("accepted ⇒ anchor-binding holds"), with the H1a mapping noted so the
  vector family and H1a's substitute-attack red-bar suite converge into
  one set of artifacts at Band 1 rather than being discharged twice.
- **Declared-time confinement:** `[policy]+[vector]` **in the
  by-construction form** — the reference verifier's output type contains
  no field from which priority can be derived (the prohibited behavior is
  inexpressible; the vector confirms the absence) — **plus a named row-5
  handoff** carrying the marketplace half of the prohibition into the
  service-layer registration, where marketplace rules actually live.
- Both registered via Amendment 3, per break-the-chain.
- Tail alternatives recorded for the future, not now: dual-anchor
  redundancy (Bitcoin + RFC 3161 TSA) noted by the author as potentially
  interesting **for a different service tier** some customers might want;
  ZK time-bracketing rejected outright.

**Follow-through commitment attached to Rulings 4–5 (author):** once
these decisions are settled, the ProVerif and TLA+ specifications must be
verified to *properly model what we claim they model* — this lands on the
existing cross-cutting obligations (per-lemma prose mapping, TLA+↔symbolic
correspondence, the TLA+↔TLA+ bridge) plus the new P2 lemma rider, and is
the standing test every new obligation must pass before its tracker
status advances.

> **CORRECTED 2026-07-20 (round-3 review, findings 3, 4, 5).** Three
> repairs to Rulings 4–5 as recorded above.
>
> *(Finding 4 — refusal semantics; FLP replacement CONFIRMED by the
> author 2026-07-20, "not wedded to language," with his gloss recorded
> because the intuition was structurally right: FLP's adversary wins by
> forever deferring the deciding message, and the real-world response is
> a finite bound accepted as a patch — `MaxAttempts` is that pattern
> applied to adversarially-deferrable anchor confirmation. The formal
> claim "avoids FLP" is what's withdrawn; the pattern kinship stands.)* A `refused` bit plus a
> separately-enabled `Refuse` action proves nothing about firing — TLA+
> needs a fairness assumption plus a liveness property (`exhausted ~>
> refused`) for that construction. Adopted construction instead: **atomic
> entry** — the final failed attempt enters `refused` in the same
> transition, making refusal a transition-level *safety* fact, keeping
> P5c safety-only with no fairness machinery. The claim is narrowed to
> *"refusal durably recorded and available for retrieval"* — "reported"
> would require modeling an outbox/delivery/acknowledgment handoff, which
> is not claimed. The FLP rationale is replaced by the clean form: *a
> bounded, explicit negative result is preferable to silent deadlock,
> while eventual successful issuance remains unclaimed* (FLP concerns
> consensus termination in fully asynchronous systems; an explicit
> bounded refusal does not "avoid" it — it relinquishes a liveness
> objective).
>
> *(Finding 3 — the "by-construction" claim was FALSE as written, and it
> was the AI collaborator's own refinement-stage strengthening.)* The
> verifier's output type cannot make downstream priority ordering
> inexpressible: the marketplace holds the input receipt containing
> `declared_issue_time` and can order receipts itself. The honest
> guarantee stack: the reference verifier emits no priority judgment; its
> API endorses no priority interpretation; marketplace policy forbids
> declared-time ordering; marketplace conformance tests exercise the
> prohibition; and **a nonconforming downstream consumer can still
> violate the rule — an explicit residual**, not a discharged
> impossibility.
>
> *(Finding 5 — the P2 rider is withdrawn as a seam-burial.)* Anchor
> standing becomes its **own property with a stable identifier**
> (allocated in A3), dependent on P7/P8, with explicit subclaims: exactly
> one designated proof/transaction pair has standing; the proof commits
> to the exact framed receipt bytes; the txid identifies the transaction
> containing that commitment; proof and txid are mutually coherent;
> discarded/unshipped anchors are ignored; substitution yields rejection
> or another valid proof of the same exact bytes. Evidence classes stay
> visibly separate: framing proof, ProVerif correspondence (which relates
> *modeled* events only — it cannot attest Bitcoin/OTS implementation
> correctness), implementation vectors, and named external assumptions.

**Status of this rulings section:** resolved but NOT final — the author
will pass this updated document through Codex for objections before the
rulings feed the pre-registration stage. Freedom to adjust remains until
then.
