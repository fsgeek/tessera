# Review: service-layer elicitation notes (2026-07-19), Codex

Review artifact under the A1.7 falsification discipline, applied to working
notes (the `exploration-2026-07-18` precedent: reviews of non-registered
exploration documents are archived and their corrections folded in-place with
the originals preserved).

## Reproducibility record

- **Reviewer:** Codex (OpenAI), dispatched directly by the author (Tony
  Mason). Model per the author's Codex configuration observed 2026-07-19:
  `gpt-5.6-sol`, reasoning high, codex-cli 0.144.6. **Gap:** the author's
  exact prompt was not captured in this session; recorded as a known hole in
  this record rather than reconstructed.
- **Reviewed input:** `docs/exploration-2026-07-19-service-layer-elicitation.md`
  at content commit `a54137c`.
- **Prior-transcript visibility:** yes — the reviewer had repo access
  (cites file line numbers and the earlier 07-18 review artifacts).
- **Prediction pre-registration:** the AI collaborator's predictions of this
  review's findings were committed and anchored *before* the review returned
  (`docs/reviews/2026-07-19-claude-predictions-for-codex-elicitation-review.md`,
  commit `eecd197`). Scoring appended to that file.
- **Reviewer-reported worktree state:** no files changed; clean.

## Verbatim review

> This is genuine forward progress. The note correctly restores the missing
> distinction: the claim graph may be concurrent while an issuer's control
> lineage can be linear. It also states the two assumptions that make
> split-brain detection conditional instead of magical.
>
> I would not register the mechanism yet. Three points need resolution first:
>
> 1. A public id-of-next may provide no security property beyond
>    (issuer, sequence, previous_hash).
> 2. The secret-seeded refinement is not verifier-enforceable as currently
>    described.
> 3. "Each signed package" implies a globally linear issuance stream per
>    issuer, which may be an unintended concurrency constraint.
>
> ## What has been earned
>
> The layer correction at
> docs/exploration-2026-07-19-service-layer-elicitation.md:40 is right. The
> earlier review established that a DAG alone has no unique equivocation
> position; the recovered design supplies one. Two different signed objects
> occupying an explicitly exclusive slot are indeed portable evidence of
> equivocation.
>
> The note is also admirably precise about its conditionality:
>
> - the legitimate issuer must continue publishing;
> - conflicting versions must reach a common observer.
>
> Those conditions at
> docs/exploration-2026-07-19-service-layer-elicitation.md:47 align with
> current key-transparency thinking: local proof verification alone is
> insufficient to expose a split view; detection requires monitoring, trusted
> auditors, anonymous comparison, or sufficiently connected gossip. IETF Key
> Transparency architecture
> (https://datatracker.ietf.org/doc/draft-ietf-keytrans-architecture/)
>
> The distinction between key succession and ordinary issuance is also
> productive. KERI pre-rotation really does commit to the next key
> configuration, require the subsequent rotation to reveal the committed
> keys, and require those keys to authorize the rotation. Official KERI
> next-key commitment description
> (https://identity.foundation/keri/kids/kid0005.html) The KERI paper
> separately distinguishes direct verifiable key-event logs from witnessed
> infrastructure and duplicity detection. KERI design paper
> (https://arxiv.org/pdf/1907.02143)
>
> Finally, keeping this as a sibling registration rather than expanding
> Band 0 is the right disposition.
>
> ## Where id-of-next is currently overcredited
>
> The earlier correction derived the need for a unique position, not
> specifically a forward UUID. These two constructions appear equivalent for
> the split-brain property:
>
> Forward slot:
> N.next_id = U
> S.id must equal U
>
> Sequence slot:
> S.issuer = N.issuer
> S.sequence = N.sequence + 1
> S.previous_hash = hash(N)
>
> Both make two distinct successors evidence of equivocation. Both reject an
> off-lineage successor. Both fail under silent usurpation. Both require
> conflicting versions to meet.
>
> So id-of-next is one implementation of the necessary unique position, but
> it has not yet shown why it is preferable to the simpler
> sequence-plus-parent rule. Its possible distinctive benefits might be:
>
> - reserving a registry location before the successor exists;
> - unlinkability until publication, if designed carefully;
> - supporting sparse or sharded issuer lanes;
> - serving as a commitment to some separately generated succession
>   credential.
>
> If none of those is required, the UUID is extra state without extra
> security.
>
> I would also avoid calling it a fencing token. A fencing token works
> because the protected resource remembers the greatest accepted generation
> and rejects stale actors. Here, the UUID creates an exclusive evidentiary
> slot, but it does not fence a thief out. "Forward slot commitment" or
> "predeclared successor slot" is more exact.
>
> ## The secret-seeded refinement has a hole
>
> The claim at docs/exploration-2026-07-19-service-layer-elicitation.md:66
> does not yet follow from the mechanism.
>
> Suppose N publicly declares slot U1. The thief knows U1, occupies it with
> forged successor S1, and signs S1 using the stolen signing key. Unless a
> verifier can check some additional constraint, the thief can simply place
> an attacker-chosen U2 in S1.next_id. The verifier cannot know that U2 was
> not derived from the legitimate issuer's secret seed.
>
> A secret matters only when its use is publicly verifiable. For example:
>
> N contains commitment C1 = H(secret1, context)
> S1 reveals secret1 satisfying C1
> S1 contains commitment C2 = H(secret2, context)
>
> But after secret1 is revealed, a thief holding the signing key may be able
> to construct an alternate S1. The clean repair is to have the revealed
> secret authorize a simultaneous key rotation, so the compromised current
> signing key is no longer sufficient. That is the structural advantage of
> KERI-style pre-rotation: the separate succession credential is a
> precommitted, unexposed signing key, not merely a hidden identifier.
>
> A VRF or a commitment chain could make secret-derived slots verifiable,
> but either becomes another key/credential protocol. It should be evaluated
> explicitly against simply adopting pre-rotation.
>
> Similarly, the public-deterministic variant protects every future slot
> only if the entire schedule is bound by an earlier uncompromised event or
> independently derivable under fixed rules. If each successor is allowed to
> choose its successor slot, a thief controls the schedule after occupying
> the first slot.
>
> My recommendation is therefore:
>
> - Use sequence plus previous-event hash to define the ordinary exclusive
>   position.
> - Use KERI-style precommitted keys for actual succession authority.
> - Add a separate opaque slot identifier only if it supplies a demonstrated
>   privacy, registry, or sharding property.
>
> ## The concurrency question is missing
>
> The opening says "each signed package" declares its successor. That gives
> each issuer one globally serialized issuance stream.
>
> This may be intended, but it has consequences:
>
> - only one worker may finalize the next package at a time;
> - concurrent issuances require coordination around the chain head;
> - a stalled issuance can obstruct later issuance;
> - partitioned issuer infrastructure naturally produces equivocation;
> - restoring from backup risks reusing a slot;
> - high-volume issuers may need lanes or sequence-range allocation.
>
> The earlier claim graph permits concurrent children. The recovered issuer
> thread removes that concurrency per issuer. That is a valid trade, but it
> needs to be explicit.
>
> The cleaner split may be:
>
> - Control plane: one linear key-event lineage per issuer.
> - Claim plane: concurrent attestations bound to a particular issuer-key
>   epoch.
> - Optional issuance-transparency plane: ordered or sharded registry
>   positions when completeness of all issuer output matters.
>
> If every ordinary attestation must be in the linear thread to expose
> stolen-key issuance, say so and accept the serialization cost. If only key
> events are linear, the system detects unauthorized succession but does not
> detect arbitrary claims produced by a stolen currently authorized key.
> That distinction belongs in the guarantee statement.
>
> ## Collision evidence requires registry behavior
>
> A transparency overlay must do more than enforce uniqueness.
>
> If it accepts the thief's first insertion and silently rejects the
> legitimate issuer's duplicate UUID, the registry has prevented two live
> values but has also destroyed the public evidence of equivocation. To
> support the note's property, it must retain evidence of both valid
> conflicting submissions—or issue a signed rejection receipt that commits
> to the rejected object.
>
> The overlay needs at least:
>
> - a lookup key such as (issuer, epoch, sequence/slot);
> - an append-only record of every syntactically valid submission attempt;
> - an inclusion promise or receipt;
> - consistency/checkpoint proofs;
> - explicit behavior for conflicting occupancy;
> - monitors that query or receive collision events;
> - a bound on checkpoint, witness, and detection delay;
> - retention sufficient to preserve both sides of a conflict.
>
> This makes "meeting point" a protocol rather than a metaphor.
>
> ## The doppelganger exclusion is honest but renames the guarantee
>
> The exclusion at docs/exploration-2026-07-19-service-layer-elicitation.md:84
> is acceptable as an initial profile, but then row 2 does not establish
> "issuer continuity" against takeover. It establishes something narrower:
>
> > Lineage conformance and split-brain evidence, conditional on continued
> > honest publication and observer convergence.
>
> That is still useful. But silent usurpation is close to the original
> motivating adversary, so excluding it should be visually prominent, not
> merely residual prose.
>
> A relatively cheap partial mitigation exists: short-lived online
> issuance-key epochs combined with precommitted offline rotation keys. If
> the issuer dies or is silenced, a thief with only the current online key
> can impersonate within the current epoch but cannot extend authority
> indefinitely. This does not solve doppelganger attack, but it bounds its
> duration and damage without requiring synchronous witnesses on every
> attestation.
>
> The profile ladder could be:
>
> - C0: wrong-slot continuations rejected offline.
> - C1: split-brain equivocation becomes provable when versions meet.
> - C2: current-key compromise recoverable through precommitted rotation
>   keys.
> - C3: current-key compromise bounded by epoch/key expiration.
> - C4: silent usurpation resisted through witnesses or threshold control.
>
> That is clearer than treating the excluded case as an all-or-nothing
> future band.
>
> ## The authority section needs temporal semantics
>
> The registered design correctly archives DNSSEC and repository evidence
> inside the bundle. But this sentence is misleading:
>
> > "DNS and repositories are discovery mechanisms, not verification
> > mechanisms."
>
> The live endpoints are not verification dependencies. Their authenticated
> historical statements absolutely are verification inputs and authority
> roots. I would say:
>
> > Live channel availability is not required for verification; archived
> > authenticated channel evidence remains part of the authority basis.
>
> For key succession, "channels disagreeing at one instant" is also
> underspecified. DNS publication, repository commits, OTS anchoring, and
> Bitcoin confirmation do not share an instant. A key event needs an
> activation rule such as:
>
> > A transition becomes VALID_STRICT only after the bundle contains
> > matching, independently valid publications of the exact event digest
> > from every required authority channel, each anchored within the
> > transition window.
>
> Then distinguish:
>
> - evidence present and contradictory → INVALID;
> - required historical evidence unavailable → UNVERIFIABLE;
> - both channels agree but lineage rule fails → INVALID;
> - both channels and lineage agree → eligible for VALID_STRICT;
> - old and new authority overlap during staging → explicit transition
>   state.
>
> Revocation particularly needs attention: if one authority channel is
> unavailable, does the old key remain authorized, does the new event remain
> unverifiable, or does issuance halt? That is a safety-versus-availability
> decision, not just a verifier classification.
>
> The note correctly carries forward correlated control. Both channels have
> different failure modes but the same human administrative root; they
> should not be described as independent against coercion or total
> operational compromise.
>
> ## KERI reference hygiene
>
> The official KERI material supports the structural comparison, but
> vlei.wiki identifies its rotation page as AI-generated and warns that it
> may contain hallucinations. It is useful explanatory material, not
> authority. I would either remove it from the prior-art evidence list or
> label it explicitly as a secondary orientation source.
>
> The official KERI page and design paper are enough for the current claim.
> They should still be treated as prior art, not as an externally proven
> security result.
>
> ## Registration structure
>
> The assistant recommendation is close, with two changes.
>
> First, "one reviewed artifact" need not mean one file. A signed
> registration manifest can bind several row documents and a seam/handoff
> matrix atomically. That gives local readability without allowing
> composition obligations to disappear.
>
> Second, an adversary model cannot be reviewed meaningfully without knowing
> the protected assets and intended guarantees. Stage one should therefore
> contain:
>
> - assets and security objectives;
> - actors, trust roots, and trust boundaries;
> - adversary capabilities and exclusions;
> - provisional guarantee profiles;
> - row handoffs;
> - explicitly unclaimed properties.
>
> For organization, I would use a matrix rather than choose one axis:
>
> - rows: receipt, continuity, transparency, claim graph, process
>   assurance, survivability;
> - columns: attacker capabilities or guarantee profiles;
> - cells: mechanism, assumption, handoff, residual risk.
>
> Cost estimates remain metadata. A guarantee lattice can be derived later
> if the profiles genuinely form one.
>
> ## Recommended next elicitation exercise
>
> Before choosing public-deterministic versus secret-seeded slots, compare
> four mechanisms against four traces:
>
> | Mechanism | Wrong slot | Correct slot + issuer live | Correct slot + issuer silent | Recovery after key theft |
> |---|---|---|---|---|
> | Sequence + previous hash | Rejects | Equivocation | Accepts thief | None |
> | Public next UUID | Rejects | Equivocation | Accepts thief | None |
> | Verifiable secret commitment | Rejects | Depends on reveal race | May block thief | Loss/recovery problem |
> | Precommitted next key | Rejects invalid rotation | Duplicity detectable | Current claims still forgeable; rotation constrained | Legitimate rotation possible |
>
> If the first two rows remain identical, omit the UUID unless it supplies
> a separate operational property. If secret succession is wanted, specify
> the verification equation before choosing the primitive.
>
> My disposition: preserve this note—it has recovered valuable architecture
> and accurately narrowed the split-brain claim. Add concurrency semantics,
> correct the secret-seed claim, weaken the fencing-token analogy, and state
> the first continuity profile as conditional split-brain evidence rather
> than takeover resistance. After those changes, the material is mature
> enough to begin the stage-one service-layer registration, though not yet
> to freeze its mechanisms.
>
> No files were changed; the worktree remains clean.

## Verbatim follow-up exchange (author question, reviewer response)

**Author:** "Reading this analysis, I have a sense that we are near the edge
of current knowledge and practice."

**Reviewer:**

> Yes—but asymmetrically.
>
> Several individual components are established practice:
>
> - signed, content-addressed receipts;
> - append-only Merkle logs and consistency proofs;
> - key pre-rotation and witnessed key-event histories;
> - offline verification;
> - replicated content storage;
> - marketplace conflict and disclosure controls.
>
> The frontier appears in their composition. Tessera is asking whether these
> can coexist while preserving all of the following:
>
> - verification without a live operator;
> - issuer continuity after key compromise;
> - detectability without universal observation;
> - concurrency without an authoritative global order;
> - evidence availability without central ownership;
> - useful completeness claims in a permissionless graph;
> - independence in a beneficiary-funded expert market;
> - cryptographic migration across decades.
>
> There is no standard architecture that simply supplies that bundle. CT,
> KERI, SCITT, Bitcoin, and marketplace governance each solve a different
> projection of it. Their seams are precisely where Tessera keeps finding
> trouble.
>
> I see three kinds of edge:
>
> 1. Engineering edge: known mechanisms combined in an uncommon way.
>    Key-event lineage plus portable attestations plus plural transparency
>    overlays belongs here. Difficult, but approachable through explicit
>    interfaces and refinement properties.
>
> 2. Research edge: guarantees whose achievable bounds remain unsettled.
>    Fork detection under partial observation, durable decentralized
>    availability, and post-compromise continuity without standing
>    infrastructure belong here.
>
> 3. Epistemic or institutional edge: problems cryptography cannot close.
>    Opinion shopping, expert independence, scope laundering, and
>    completeness of all relevant evidence belong here. These require
>    governance and incentives; some admit only bounded, contextual claims.
>
> The danger would be interpreting proximity to the frontier as permission
> to invent mechanisms confidently. The opportunity is almost the opposite:
> Tessera can contribute by drawing unusually honest borders around what
> each mechanism proves, what assumptions connect them, and where no proof
> is presently possible.
>
> That may be the project's most distinctive contribution. It need not solve
> the whole frontier to matter. A carefully named result such as—
>
> > Under continued honest publication, checkpoint convergence, and
> > retained conflicting submissions, two valid occupants of an exclusive
> > issuer slot yield portable evidence of equivocation.
>
> —is modest beside "takeover-resistant unowned commons," but it is
> defensible, reusable, and capable of being built upon.
>
> I also think your wandering has been productive here. The difficulty has
> not primarily come from aimlessness; it has come from repeatedly reaching
> boundaries hidden inside ordinary words: continuity, independence,
> complete, survives, detectable. Wandering exposed that those words
> contained multiple incompatible guarantees. The discipline now is to
> preserve the discoveries without obligating this one project to conquer
> every territory they revealed.

## Disposition (author + AI collaborator, 2026-07-19)

Codex's own disposition accepted as drafted: preserve the note; fold
corrections in-place with originals preserved (done — see the CORRECTED /
SHARPENED blocks added to
`docs/exploration-2026-07-19-service-layer-elicitation.md`); do NOT freeze
mechanisms; the four-trace mechanism comparison is the next elicitation
exercise before any slot primitive is chosen. Specific dispositions:

1. **id-of-next overcredited (redundancy vs. sequence+previous-hash):**
   ACCEPT. Recorded as an open comparison, not a chosen mechanism. The
   UUID's four candidate distinctive benefits recorded; if none is required,
   it is extra state.
2. **Secret-seed hole:** ACCEPT. The claim as written was wrong (predicted
   as such — prediction 2). Corrected in place; VRF/commitment-chain vs.
   pre-rotation is an explicit future evaluation.
3. **Concurrency semantics missing:** ACCEPT. Control-plane / claim-plane /
   optional issuance-transparency-plane split recorded; the guarantee
   distinction (linear key events only ⇒ stolen-key ordinary claims not
   detected) recorded for the guarantee statement.
4. **Registry conflict behavior:** ACCEPT. "Meeting point" upgraded from
   metaphor to protocol requirement list; evidence-preserving conflict
   handling (both sides retained or signed rejection receipts) recorded.
5. **Guarantee renaming + C0–C4 ladder:** ACCEPT. Row-2 initial profile
   restated as conditional split-brain evidence; ladder recorded; epoch-
   bounding mitigation recorded as candidate C3.
6. **Temporal semantics of authority:** ACCEPT (predicted in direction —
   prediction 1). Corrected sentence adopted; activation-rule sketch and
   verdict classification recorded; revocation-under-channel-unavailability
   flagged as a safety-vs-availability decision for the author.
7. **KERI reference hygiene (vlei.wiki AI-generated):** ACCEPT. Demoted to
   secondary orientation source.
8. **Registration structure (manifest-bound multi-file; stage-one
   contents; matrix organization):** ACCEPT as the revised recommendation,
   pending author ratification of the structure decision.

Prediction calibration: scored in
`docs/reviews/2026-07-19-claude-predictions-for-codex-elicitation-review.md`
(addendum). Headline: the predictions caught the author-side *prose*
overclaims (predictions 1, 2, 5) and missed the review's most serious
*design-level* findings (redundancy, concurrency, evidence-destroying
registry) — the assistant predicts its rhetoric's flaws, not its design's
blind spots. That asymmetry is itself the strongest argument on record for
the non-author gate.
