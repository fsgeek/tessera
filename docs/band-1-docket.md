# Band 1 / build-phase docket

Status: parking record (clerk-compiled 2026-08-08 from the A3
four-model panel; see `docs/reviews/2026-08-08-A3-panel-disposition.md`).
Nothing here is registered; the purpose is that nothing silently
drops. Items graduate by being registered (amendment or Band 1
specification) or disposed with reasons.

## Issuance / operational

1. **Local-GPG signing path under automation** (Gemini A). The
   dual-signature construction requires the firewalled local key
   during automated issuance. Specify the execution model: how the
   service edge invokes the local signer without an internet-facing
   surface on the workstation, and what happens to the attempt loop
   (N=3, A2.3) when the local signer is unreachable — a transient
   partition must not manufacture a false `REFUSED` terminal state.
2. **Refusal-residual bounding** (Grok immediate 3; DeepSeek 6).
   Declared maximum delivery/publication latency T, after which the
   residual is accepted and marked (`DELIVERY_EXPIRED` /
   `PUBLICATION_EXPIRED`); and the precomputed-commitment variant
   (commitment value computed pre-issuance, revealed on refusal) that
   moves the publishing moment earlier. Both touch A3.7.2's
   registered decomposition — if adopted, by amendment, not silently.
3. **OTS congestion behavior** (Gemini strengthening 2, operational
   half). Fee-bumping / aggregator-delay behavior relative to the
   adopted S = 24h working default. S itself is A2.1-adopted;
   revision is by A2.1's own declared terms.

## Verifier / bundle format

4. **Numeric-precision rejection at ingestion** (Gemini C). Schema
   validation rejects raw JSON numerics exceeding IEEE 754 exact
   range before canonicalization; string-encoding is enforced at the
   boundary, not assumed of clients. Good catch; cheap; belongs in
   the Band 1 ingestion spec and conformance vectors.
5. **Fixed-width envelope encodings** (Gemini strengthening 3).
   Explicit binary widths/endianness for `payload_length` and
   `canonicalization_version` in the P8 framing envelope, for
   cross-language byte determinism.
6. **SPV header segment in bundle** (Gemini strengthening 1). Embed
   the k-header segment in `authority_evidence` so the standalone
   verifier needs no header database.
7. **Header authentication pinning** (Grok medium-term 2; carried
   A2.1 residual). Verifier policy pins checkpoint hashes or a
   minimum cumulative-work threshold, travelling with the trust
   configuration; absence of a pin is an explicit `UNVERIFIABLE`
   case. Touches registered verdict semantics — register before
   build.
8. **Historical trust-anchor store as standalone object** (Gemini B,
   surviving half). Versioned, decoupled from the verifier binary,
   exportable. (The declined half — degrading unknown roots to the
   repo anchor — stays declined; see disposition record §6.)
9. **Bundle-size budget for embedded specifications** (Kimi 5).
   Declared per-bundle byte budget; above it, content-addressed
   reference plus published store.
10. **Embedded verification spec executable-in-principle** (Grok
    immediate 1). Formal fragment or pure-function reference
    implementation in a frozen-semantics language, not prose+vectors
    alone. Interacts with the §A3.4 Designated Community claim — may
    warrant registration rather than quiet build-phase adoption.
28. **Degraded-verdict record format** (Amendment 5 §A5.3). For each
    waived check, the record states both the policy that authorized
    the waiver and the verifier's observation of the waived evidence —
    at least six values: absent, unperformable, invalid, anchor-late,
    names-other-key, would-pass. H1a obligation.
29. **Three verifier checks pending their symbolic legs** (Amendment 5
    §A5.4–§A5.6). Multi-signer common content — the six non-fingerprint
    frame fields equal across signer slots, three already carried by
    the shared manifest tuple, three new; the wrapper's recorded inner
    canonicalization version checked against the inner frame's own; the
    standing path pins the presented authority tuple to the tuple
    embedded in the core. H1a reference-verifier obligations, entered
    once their symbolic legs run.

## Surfaces / conformance

11. **Renderer conformance vectors** (Kimi 6). Structured outputs a
    conforming renderer must display in full; malformed renderings
    (stripped scope, collapsed dimensions) must fail a mechanical CI
    check — the rendering red-bar made testable.
12. **Signed report as the only relayable form?** (Grok structural
    2). Whether Tessera-controlled surfaces may emit only the
    attested report (A3.8) when a result will be relayed. Policy
    decision; register if adopted.
30. **P9 conformance vector cases** (Amendment 5 §A5.1). The H1a
    vector carries the expected verdict determined by bundle and
    declared policy, with each machine's verdict compared to it; one
    case presents the same bundle twice on one machine; one case has
    the optional service reachable and contradicting the bundle. H1a
    obligation.

32. **P7 verdict-independence vector** (Amendment 6 §A6.1). A wrapped
    bundle's inner verdict equals the same inner bundle's standalone
    verdict, under each of the four P4 verdict values; a re-serializing
    wrapper is the red bar. H1a obligation.

31. **Implementation specification — the current contract, derived from
    the adopted artifacts** (proposed 2026-09-12 by the AI collaborator,
    after a Codex assessment the author shared the same day; the author's
    words: *"when an implementation plan is needed, the travelog of how
    we got there is not of interest until some flaw is discovered, or
    there is some need to enhance or amend functionality"*). One
    document stating, per verifier behaviour, what it consumes, what it
    checks, what it reports, and what it leaves to the adjudicator;
    interfaces, invariants, failure behaviour, and outstanding
    obligations; unresolved decisions visibly marked; every requirement
    linked to the amendment, ruling or model that justifies it. Any
    contradiction found while consolidating is returned as a routed
    question, never resolved by the writer. Wider than the A3 §A3.1.4
    relying-party story (which it contains). Sequenced as a Band 0 exit
    companion, not a Band 1 item: writing it is the cheapest test of
    whether the record composes. Not yet begun.

## Tending / custody

13. **Tending visibility deadlines** (DeepSeek suggestion 2).
    `ACTION_DUE`/`FAILED` carry observable deadlines; visibility
    boundary stated explicitly (current custodial record holders see
    staleness; old-bundle holders do not, by design).
14. **Attested renewal-window parameter** (Grok structural 1). The
    renewal window itself attested and visible in the tending record,
    so a custodian cannot claim the trigger never fired.
15. **Minimal tending-policy skeleton for the demonstration** (Kimi
    7). Even a declared `NO_ACTION_REQUIRED` policy sized to the PoC
    horizon, so the machinery is concrete and testable at Band 0
    exit. (If required *at Band 0 exit*, this is a registration
    change — flag for the author rather than adopting here.)
16. **Old-bundle stability without custodial records** (DeepSeek 5).
    Dead-project demonstration explicitly tests that an old bundle's
    `VALID_STRICT` is unaffected when custodial records are
    unavailable and the tending check reports `UNVERIFIABLE`.
17. **Custody of externally-referenced verification inputs**
    (added 2026-08-13 from the first-link DECISION.md cross-review;
    raised as "remains obtainable" doing unowned work). Items 13–16
    cover tending visibility, renewal parameters, minimal policy, and
    old-bundle behaviour. **None of them assigns retention,
    replication, discovery, or retrieval-testing responsibility for
    bytes a verifier must fetch from outside the envelope.** Citing
    13–16 for this would conceal the gap rather than close it.

    *Subjects — at least three, and the list is open:*
    (a) the exact referenced representation, wherever item 9's size
    budget pushes transcribed authority content behind a
    content-addressed reference (criterion 4 of the first-link
    decision depends on it);
    (b) **conditional on item 18 being activated** — the versioned
    historical trust/registry store of item 8, against which
    issuance-time binding-form validity *would* be judged; without it
    a future verifier could not distinguish *illegal when issued* from
    *retired later*. No such judgment exists while item 18 is
    deferred;
    (c) **conditional on item 18 being activated** — the specification
    and conformance vectors of **retired** binding forms, which the
    deferred lifecycle plan *would* require be preserved for
    previously issued envelopes. Nothing is retired while item 18 is
    deferred, so this subject is presently empty.

    *Questions this item must answer before any Band 1 freeze:* what
    exactly must remain obtainable; who is expected to retain it;
    how a verifier discovers it; and how retrieval is tested.

    *Constraints already implied by the record, not free choices:*
    the answer cannot be "Tessera, in perpetuity" — that is the
    dependency the project exists to refuse. Discovery should rest on
    intrinsic identity (content addressing) with location as a
    revocable hint, since locators rot on exactly the schedule the
    threat model cares about. Retrieval failure yields `UNVERIFIABLE`
    with a reason code distinguishing *not retrieved* from other
    unverifiable causes, and per item 16 must not contaminate the base
    verdict.

    *No availability promise is made or implied.* The tiered verifier
    ladder bounds the blast radius without claiming anything about
    perpetuity — but **an earlier draft of this item contradicted
    itself** (cross-review finding, 2026-08-13) by making subject (b)
    required for binding-form validity while also asserting that a
    self-contained-tier verdict is unaffected by custody loss. Both
    cannot hold. The unresolved fork, stated rather than papered over:

    - **(A) The bundle carries its own authenticated registry entry**
      (or an inclusion proof against the registry) sufficient for the
      self-contained check. Preserves the strong self-contained-tier
      claim; costs bundle bytes, which is item 9's tension again.
    - **(B) The self-contained tier does not judge issuance-time
      binding-form validity**, and that check moves to the corpus
      tier. Keeps bundles small; narrows what a self-contained verdict
      asserts, and that narrowing must then be visible in the verdict
      rather than implied.

    Neither has been selected. Whichever is chosen, subjects (a) and
    (c) still depend on custody, so this item does not disappear under
    either branch.

    *Provenance:* this is the custody half of the 2026-08-12 finding
    that **existence is anchorable and availability is not**
    (`docs/exploration-2026-08-12-succession-compromise-and-verifier-tiers.md`
    §2.5). Anchoring cannot close it; only custody can.

    *Scope reduced 2026-08-13 by item 18's deferral.* With **no form
    lifecycle or issuance-state distinction implemented**, subject (b)
    has nothing to judge and subject (c) is empty. **Only subject (a)
    is live**, and only where item 9's size budget actually pushes
    content behind a reference. The A/B fork above is moot on the same
    grounds and revives only with item 18. (Note the wording: both
    direct and digest remain *permitted protocol forms* under the
    adopted decision — the deferral removes the lifecycle's
    issuable/retired classification, not the permission.)

    *Leading candidate if this is ever taken up (candidate, not
    adopted):* bind form legitimacy to the **key chain** rather than to
    a global registry. The chain must be preserved for any verification
    at all, so policy riding in a key's attestation is free custody;
    policy change becomes key rotation, emergency retirement becomes a
    tombstone, both already-required mechanisms. This splits the
    tangled notion of "registry" into *legitimacy* (per-key, free) and
    *semantics* (global, but specification rather than per-artifact
    state — i.e. subject (c)), which is what dissolves subject (b).

18. **Binding-form lifecycle and reference-verifier obligation**
    (DEFERRED 2026-08-13 by author ruling; plan drafted in
    `formal/spike/first-link/DECISION.md` §"Form lifecycle and the
    reference-verifier obligation"). Three-state lifecycle, issuance-
    time registry epoch, append-only shared-layer verifier support, CI
    gating before a form becomes issuable, and the named δ-width
    rollback residual. **Nothing is implemented.** Inert until a second
    binding form becomes issuable, which is separately gated on the
    P7/P8 cross-form substitution negative control. Deferral was
    checked to be free, not merely cheap: no envelope field is required
    under any live candidate, so no irreversible decision is being
    postponed.

    *Governing principle, stated by the author on this ruling and
    general beyond it:* **plans are cheap and implementations are not.**
    Every complication added now increases the complexity of the
    baseline service; keeping a plan on record for a future feature is
    the architect's job, but implementing it early requires a
    demonstrated reason. Absent that reason, the disposition is
    "registered plan, no implementation." Successors applying this
    should confirm the deferral is genuinely free — that nothing
    irreversible (an envelope field, a frozen format) is being
    postponed — because that check is what separates this principle
    from procrastination.

19. **Verdict composition along a renewal chain** (candidate, 2026-08-30;
    surfaced in the author's design walk with a Claude Desktop
    instance, clerk-entered). Over a long horizon, renewal wraps
    (A3.4: RFC 4998-style; A3.5: each tending record references the
    renewal artifact, its predecessor, and a predecessor-link result),
    so a far-future verification is a walk down a chain of wrappers,
    each link judged under the standard of its own epoch. The record
    already forbids an aggregate checkmark (A3.8) and requires per-layer
    evaluation of wrapped artifacts (A3.2 item 4) — but both were
    framed for layers inside one bundle at one time, and the S-series
    and P4 were framed for single artifacts. **Not registered:** (a)
    that a renewal chain is the A3.2 item 4 per-layer case extended in
    time, evaluated link by link under each link's epoch — which
    depends on the registry-epoch material deferred under item 18; (b)
    what one `UNVERIFIABLE` link means for the links beneath it, given
    that a relying party's trust is rooted at the newest signer it can
    verify — the honest candidate rule, consistent with A3.8, is
    *report per link, never propagate as `INVALID`, and state which
    links the verifier could reach from its trust root*; (c) where
    standing sits on a chain: the innermost issuance identity (A3.9's
    transplant companion already says a wrapper cannot re-scope it).
    Cheap to specify now; expensive to discover at year ten. Disposition
    is the author's; nothing here is adopted.

20. **Renewal is always cumulative — state it** (candidate, 2026-08-30;
    author's design walk with a Claude Desktop instance, checked
    against the record by the clerk). RFC 4998 has two renewal modes:
    simple timestamp renewal covers only the previous timestamp;
    hash-tree renewal re-commits the data and all accumulated evidence.
    Original §4 already builds the cumulative form — "a superseding
    attestation wraps the original package … the inner attestation's
    bytes, signatures, and OTS proof are immutable; the wrapper is a
    new layer with its own time-anchor" — so wrapper N commits to
    package N−1 including its evidence, by construction. What is not
    stated: that simple renewal is excluded, and that the reason is the
    one the walk found — cumulative wrapping stops the hash-transition
    case being special and stops a broken middle link severing the
    chain. One registered sentence; no mechanism change.

21. **Completeness rule for wrapper lineage** (candidate, 2026-08-30,
    same source). A wrap commits to the *full known lineage* of prior
    wrappers, unfavorable members included, so that pruning by omission
    becomes discoverable evidence rather than silent loss. Not
    registered anywhere. Wrapper-level equivocation — two wraps of the
    same package by one key, each claiming completeness — is the A2
    residue one level up and should be named with the standing
    decision's G4 treatment (boundary stated, closure not claimed),
    never as a closure.

22. **Independence of testimony comes from anchors, not custody**
    (candidate, 2026-08-30, same source). Original §4 gives each
    wrapper "its own time-anchor"; what is not stated is the
    epistemic claim that follows — cumulative depth from one custody
    line is one thread that merely looks dense, and each epoch's
    wrapper is independent testimony *only* through its own
    contemporaneous anchor. A 2106 examiner's forgery-cost estimate
    rests on the anchors, not on the wrap count. One sentence, near
    A3.4 claim 3.

23. **Per-prior verdict snapshots — registered AGAINST, in the renewal
    wrapper; provided for, elsewhere** (2026-08-30; a correction the
    clerk owes the author's design walk). The walk proposed that each
    wrap carry a snapshot of the prior links' verdicts, yielding a
    court-legible density report as a byproduct. Original §4 rules the
    renewal wrapper out for that role, by author decision: it "commits
    to the inner package's bytes, not to the inner receipt's
    verification result at wrap time … because that would be a form of
    re-evaluation." The role exists, but as A3.8's **optional signed
    verification report** — "a distinct typed wrapper" whose bounded
    claim is that an identified evaluator assessed an identified bundle
    under an identified environment and obtained the enclosed result.
    So the density report the walk wants is buildable, from A3.8 report
    wrappers interleaved with A3.4 renewal wrappers, and must not be
    folded into the renewal wrapper itself. Disposition: no change to
    the record; the correction is to the conversation.

24. **Correlated versus uncorrelated custody; what anchoring standing
    evidence does and does not buy** (candidate, 2026-08-30; the
    author's observation that recomputing the 2026 chain, however
    cheap in 2106, produces a *different* chain inconsistent with every
    other surviving reference; sharpened by a Kimi review the same day;
    entered by the AI collaborator with two corrections). (a) An
    anchor's evidentiary value is the number of independent surviving
    references it must remain consistent with, not the work to
    recompute it — a **correlated** custody subject the world maintains
    for its own reasons, as against an **uncorrelated** one (a
    project-specific log) that only this project's relying parties
    have reason to keep. This is a legitimate reading of
    DECISION-CRITERIA.md C2 *as registered* ("does the construction
    create a new custody subject?") and may be cited in scoring under
    that question; it is **not** entered into the criteria, which are
    frozen at `74ee46e` and whose scorer is non-blind. (b) Anchoring
    standing evidence bounds *when* each record was made — the G4
    temporal clause — and so defeats backdated equivocation by a
    post-mortem key holder. It does **not** make a contemporaneous
    second record *discoverable*: an OTS anchor is a hash in a Merkle
    tree, and finding "every record for lineage X" from the chain
    requires an index the chain does not provide. Kimi's claim that
    two differently-anchored records "leave a trace a future examiner
    can discover" overstates this; the trace exists and is not
    findable without an index, which is the transparency witness
    again. The honest split: the anchor narrows *when*; only a log
    narrows *whether*; and the log is the uncorrelated subject of (a).
    (c) For the relying-party story: the anchor's robustness over 80
    years rests on the global irreversibility of a reference graph
    maintained by others, not on Tessera or any single party; if the
    hash function falls, the reference structure still constrains a
    forger to consistency with every surviving copy — detectability by
    global state, not by local cryptography.

25. **Forward-link / predeclared successor slot — registration
    scheduled** (entered 2026-09-04 by the AI collaborator from the
    author's D1 ruling, `formal/spike/standing-probe/DECISION.md`
    sub-ruling 4; drafting record
    `formal/spike/standing-probe/AMENDMENTS-2026-08-31.md`). Row 2 of
    the 07-19 service-layer note ("predeclared successor slot") WILL
    be registered; the mechanism is not frozen and may be substituted
    under the author's criterion that key compromise be made legible
    (any fork leads back to the point of compromise). Relation to the
    selected standing mechanism: the terminal lineage record chains
    attempts within one issuance, backward; the slot chains issuances
    across the service's life, forward. **Location RULED (author,
    2026-09-04):** inside the canonical payload under P3's
    obligations, per the A3 §1 precedent, leaving P8's four-field
    frame unchanged. **Schedule:** registration, including the 07-19
    note's four-mechanism × four-trace comparison, completes before
    format freeze; P8's golden vectors gain a slot-bearing vector at
    registration. Not gated on, and does not gate, the S-STANDING
    model. This is the only docket item besides 17 with a pre-freeze
    deadline.
    *Author clarification, 2026-09-04 (in session, recorded by the AI
    collaborator):* the travelog entry of the same date says the
    forward identifier is "not tied to the signature over Attestation
    N"; asked whether that meant *not derived from* N's signature or
    *not covered by* it, the author ruled: "the forward identifier has
    to be inside the signed package — otherwise, it isn't tied to the
    attestation." So: an independent identifier (not a back-hash),
    carried inside N's signed bytes — consistent with the payload
    location ruled above.

26. **Issuer signing-key lifetime and rotation policy — candidate;
    not registered anywhere in the record** (entered 2026-09-05 by the
    AI collaborator from the author's walk-through of
    `formal/spike/first-link/proverif/q3_mechanism_dns_compromised.pv`).
    The author's concern, in his words: *"key lifetime becomes a
    safeguard against someone surreptitiously taking over the service
    and pretending to be Tessera."* Facts established from the tree
    the same day: every symbolic model leaks channel keys only and
    never the issuer key, so an adversary holding the issuer key is
    indistinguishable from the issuer in every model; the mechanism
    that would make a bounded key lifetime bite is the temporal anchor
    plus the P5/P6 validity-at-anchored-time logic (TLA+); "lifecycle"
    in the record means binding-form lifecycle (item 18) and
    "rotation" in A3.5 means challenge-vector rotation. No declared
    maximum validity window for the issuer key, no rotation cadence,
    and no verifier behaviour at the window boundary is registered.
    Relation to item 25: the forward-link slot makes a fork legible
    after the fact; a lifetime policy bounds the window in which a
    stolen or inherited key can issue at all. Candidate for
    registration before format freeze if the window or boundary
    behaviour affects the bundle's fields; otherwise Band 1 policy.
    *Author addition, 2026-09-06 (in session, recorded by the AI
    collaborator):* rotation must be designed, not only lifetime. His
    words: *"we might want to insist that keys can only be replaced
    within some time band of expiration and then require the
    expiration bands not overlap between the authorities."* So two
    candidate rules: (i) a replacement key is accepted only inside a
    declared band before the current key's expiry; (ii) the authority
    channels' expiry bands are staggered so that no instant has more
    than one channel in rotation, which keeps A1.3 item 6's
    "proper subset" condition true across a rotation — that rationale
    is the collaborator's reconstruction, not the author's stated
    reason. Unexplored; interacts with the first link (which manifest
    a rotated channel key endorses) and with P5/P6's
    validity-at-anchored-time logic.
    *Collaborator objections, same day, so the rules are not read as
    agreed:* (i) forbids emergency retirement after a discovered
    compromise, and any exception path is the attack surface again;
    the defensible form is weaker — an out-of-band rotation is a
    detection signal a verifier treats as degradation. (ii) helps only
    if the stable channel vouches for the rotating one (a
    cross-endorsement mechanism not yet decided); under per-channel
    chaining a thief of the old key rotates alone regardless; and
    DNSSEC rollover timing is partly the registrar's and parent zone's,
    so the band may be unenforceable for that channel. What stands
    without objection: rotation is the moment a channel's trust root
    is replaced and therefore the most attractive moment for a holder
    of a stolen key; that threat is absent from A1.3 and should be
    registered.
    *Author's reason, 2026-09-06, in his words (supplied after the
    objections):* *"The presumption with authority keys is that they
    are different channels, with separate governance. By staggering
    rotation periods it makes it more difficult for a single entity to
    compromise them in a way that is not detectable. Governments could
    likely do it, but then that could turn into a choice of domains to
    use … pick the US, China, and Brazil, for example — anything that
    requires all three to agree is socio-politically resistant to
    compromise."* *Collaborator revision of objection (ii), same day:*
    the objection was too strong. The strict verifier's requirement
    that both channels endorse the same manifest is already the
    cross-check; staggering then forces an attacker to hold one
    channel from its window until the other's, during which the
    channels disagree and strict verification fails visibly. The
    condition the argument needs is narrower than a new endorsement
    mechanism: **channel-key rotation must itself be a visible,
    endorsed object** (a rotation of A recorded in the manifest
    lineage and endorsed by B), and verifiers must check key history,
    not only the current key. A quiet DNSSEC rollover B never sees
    gives staggering nothing to work with. Two facts for the
    governance premise: (1) the current channels — a `.com` zone
    (Verisign, US) and a GitHub repository (US) — are organisationally
    distinct but under one jurisdiction, so the multi-government
    property the author describes is not held by the present channel
    choice; achieving it is a channel-selection policy (a `.br` or
    `.cn` zone, a non-US forge) exposed in the verifier's trust
    configuration, and it extends item 24's correlated-custody
    argument from anchors to authority channels. (2) The temporal
    anchor is what makes governance diversity hold over 80 years:
    later collusion cannot backdate, so the resistance need only be
    true at issuance.
    *Author, 2026-09-06, same session:* the channels are generalised —
    "DNS" means any domain, "repository" means any public repository
    source; multiple authority-key services are permitted (A1.3 item 6
    is already n-ary; the models are the n = 2 instance and say so).
    Carried caveats: channel count is not strength — an inert check
    adds nothing (spike Q7/Q8) — and each added channel raises the
    frequency of degraded verdicts. The author names the attestation
    company itself as the weak spot, since it holds the accounts on
    every channel plus the issuer key: correlated custody at the
    account layer. His qualifier, "change of control for companies is
    generally visible," holds for legal change of control (defended by
    the anchor: no backdating) and not for compromise of control
    (credential theft, insider), which no model here distinguishes
    from Tessera; only equivocation visibility (item 25) and a public
    log (the transparency witness, set aside 2026-08-31; item 24(b))
    address it. Recorded as reopening the case for a log, not as a
    mechanism decision.

27. **Third-party log buildability — a format-freeze constraint**
    (candidate, 2026-09-06; entered by the AI collaborator from the
    author's words in session). The author: *"nothing says we cannot
    add a separate log outside Tessera; what it suggests is that we
    need to have a mechanism to permit someone to build such a log if
    they decide it has value to do so … the design is a floor, not a
    ceiling."* This dissolves the item 24 / 2026-08-31 objection to a
    transparency witness: the objection was to Tessera as the custody
    subject that must survive to keep a log, not to logs. A log kept by
    a party who has decided it is worth keeping is a correlated subject.
    What buildability already has: stateless verification (P9), the
    forward identifier in the payload (item 25) making forks visible to
    any holder of both successors, the canonical format (P8), and the
    anchor bounding when each entry was made. What it lacks: a
    registered statement that third-party logs are an intended
    consumer, so that the format freeze preserves the fields a log
    builder needs — issuer identity, the forward identifier, anchor
    evidence, and a stable indexing key — even where no relying party
    needs them. Pre-freeze, alongside items 17 and 25. Relation to
    outward work: SCITT separates issuers from transparency services
    (`docs/exploration-2026-08-12-outward-verification-scitt-ccf.md`);
    under this item Tessera is an issuer whose artifacts are loggable
    by a transparency service it never heard of. Key-rotation policy
    (item 26) is explicitly deferred from the current round by the
    author, same session.
    *Correction, same day (collaborator):* no field is known to be
    missing. The four named are present or scheduled (identity and
    manifest hash in the signed frame; forward identifier in the
    payload per item 25; anchor evidence in the bundle; the
    attestation's own digest as index key). Item 27 is a
    **preservation** constraint at freeze, not an addition. Scope:
    what is loggable is what is presented — attestations are delivered
    to requesters, not published — so a third-party log's coverage is
    whatever the world shows it (item 24(b)).
    *Vocabulary, RULED (author) 2026-09-06 in substance:* the
    **verifier** is P9's pure function — bundle plus declared policy
    in, verdict out; *"if the verifier requires anything from an
    optional service, it is fundamentally broken."* The
    **adjudicator** (the relying party) decides trust using the
    verdict plus anything else, including any log anyone built, and
    *"is not prohibited from using that log as part of its own
    verification."* The relying-party story defines both terms; an
    enumeration API may feed a log and may never feed a verdict.

