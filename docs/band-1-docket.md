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
