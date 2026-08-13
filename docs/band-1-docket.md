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

## Surfaces / conformance

11. **Renderer conformance vectors** (Kimi 6). Structured outputs a
    conforming renderer must display in full; malformed renderings
    (stripped scope, collapsed dimensions) must fail a mechanical CI
    check — the rendering red-bar made testable.
12. **Signed report as the only relayable form?** (Grok structural
    2). Whether Tessera-controlled surfaces may emit only the
    attested report (A3.8) when a result will be relayed. Policy
    decision; register if adopted.

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
