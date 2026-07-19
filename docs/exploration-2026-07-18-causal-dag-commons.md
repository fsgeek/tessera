# Exploration notes — the causal-DAG commons and the beneficiary adversary

> **STATUS: WORKING NOTES. NOT A PRE-REGISTRATION, NOT AN AMENDMENT, NOTHING
> DISCHARGED.** This document captures a single session of architecture
> exploration (2026-07-18, Tony + Claude Opus 4.8). It exists so the reasoning
> is preserved rather than left to memory — after a session where the recurring
> finding was *the designed system had outrun the registered one*, leaving this
> in anyone's head would repeat that exact failure a fourth time.
>
> Everything here is a **candidate**. Some of it contradicts the current
> registered Band 0. None of it has been modeled, checked, reviewed, or signed.
> Do not cite it as a commitment. Its purpose is to give a well-posed starting
> point to whoever picks this up next — a future instance, another model, or
> Tony cold in three weeks — and to hand external reviewers a *stable* target
> instead of a re-narrated one.
>
> If any of this is ever to become real, the path is: adversary model →
> properties → formal discharge → non-author falsification → signed, anchored
> amendment. This document is upstream of all of that.
>
> **REVISED 2026-07-19 after non-author review (Codex / GPT-5.6).** Several
> claims in the 07-18 draft were **wrong**, not merely loose. They are corrected
> in place with `CORRECTED` / `SHARPENED` blocks that state the original claim,
> why it failed, and what replaces it — originals preserved rather than quietly
> deleted, so the error record stays legible. The most serious:
>
> 1. **A DAG does not make key takeover detectable** (§5) — a stolen key need
>    not fork; takeover ≠ equivocation; the Certificate Transparency analogy was
>    structurally wrong.
> 2. **"The client never sees the service layer"** (§1) — incoherent; the layer
>    can only help if portable proofs reach the client.
> 3. **"Universal detectability"** (§2) — overclaim; detectability is *bounded*
>    by observer/retention/non-collusion assumptions.
> 4. **Completeness-by-convention** (§6) — a root of "what I found" is not a
>    completeness proof.
> 5. **First-to-file** (§7 q6) — a misreading of A2.4, which *forbids* it.
> 6. **"Sound"** (§0) — Band 0 is *well-scoped*, not sound; most properties are
>    still `open`.
>
> New §8b carries the layer decomposition and disposition. The corrections were
> found by an **external** reviewer, which is the standing argument for the
> non-author gate: the same assistant that helped write these claims did not
> catch them.

---

## 0. How we got here (the through-line)

The session began as a git-push problem (branch protection on `phase-0-prereg`)
and became an architecture re-examination. The connective tissue was a single
finding that recurred **four times**, each time surfaced by Tony's systems
memory pointing at something the *registered record* under-specified:

1. **The P5c↔P5P6 seam.** The two temporal TLA+ models agree in prose
   (`confirmedAt := timestamp(block h+k−1)`) but model the underlying quantity
   incompatibly — P5c as an operational `depth` state variable, P5P6 as a free
   integer. The correspondence is asserted, not mechanically checked. Codex
   confirmed the *narrow* gap (the alarming "burial delay vanishes" trace does
   NOT reproduce — 384 states, invariant holds; Claude's initial framing was
   wrong and the falsification gate correctly killed it). What survives: an
   undischarged TLA+↔TLA+ correspondence obligation, and it was previously
   raised (Antigravity 2026-07-03) but itemized only as TLA+↔*symbolic*.

2. **Length / P8 as unmodeled root-of-trust.** Length is bound into canonical
   bytes (pre-reg line 376) and survives as a real forgery confound — but P8
   (canonicalization injectivity + framing), the property that makes length
   *mean* anything, is the one tracker entry with no tool, `[proof]` only,
   status `open`. Every symbolic proof's "over *these* bytes" premise rests on
   P8, which is prose. Of all open properties, P8's absence propagates furthest.

3. **The linkage / split-brain design.** Tony recalled a signed package with
   `hash-of-prior` (backward) and `id-of-next` (forward preallocation, a
   split-brain / mimic-takeover defense). Repo search: the *backward*
   hash-chain exists as inherited Willay implementation ("ledger hash-chain
   logic", DynamoDB "chain head") but is **absent from the registered
   signed-bytes definition and from every formal model**; the *forward*
   preallocation exists **only in Tony's head** — zero hits anywhere.

4. **The threat model itself.** A1.3's adversary is entirely *single-attestation*
   and *outsider* (forge/strip/substitute/replay/backdate one attestation,
   cannot break primitives). It has **no** chain-continuity, equivocation,
   history-rewrite, or takeover adversary. The registered threat model is for a
   *client-layer attestation*; the design in Tony's head is a *service-layer
   ledger*. Same system, two threat surfaces, only the near one registered.

**The synthesis:** the registered Band 0 is a **well-scoped** pre-registration of
a *single-attestation client guarantee*. The system actually being designed is a
two-layer thing whose service layer has an unwritten (and stronger) threat
model. That reframing is what the rest of these notes build on.

> **CORRECTED 2026-07-19 (Codex review).** The original said Band 0 was
> "correct, near-complete" and elsewhere that "the registered layer is sound."
> **Not earned.** Most of P1–P10 remain `open` in `formal/PROPERTIES.md`. The
> registered layer is *well-scoped*, not *sound*. (This was a regression: the
> session had earlier stated this correctly — "method demonstrated, not result
> verified" — and the note then used the looser word.)

---

## 1. The two-layer reframing (Tony's, and it holds)

- **Client layer (the handle).** A client gets a handle and verifies ONE
  attestation, standalone, with no infrastructure and no trust in
  Tessera-the-operator. The registered pre-registration (P1–P10, temporal
  models) is sound *for this layer*.
- **Service layer (the commons).** The integrity of the *issuing lineage* —
  that the entity issuing attestations is genuine and has not been co-opted,
  forked, or rewritten. This is where the unwritten threat model lives.

> **CORRECTED 2026-07-19 (Codex review).** The original read: "The client never
> sees the service layer. The service layer is what makes the client's handle
> trustworthy over time and against a service-level adversary." **That is
> incoherent as stated** — if the client receives no checkpoint, witness proof,
> or key-history proof, the service layer *cannot* strengthen the client's
> verdict. It may protect operations, but it does not make a standalone handle
> trustworthy against service takeover. Offline verification and
> takeover-resistance trade against each other; the original wished that away.
>
> **Accurate statement:** *basic verification needs no live Tessera
> infrastructure; stronger continuity profiles consume portable service-layer
> proofs embedded in the bundle.* This preserves offline verification while
> making the trust dependency visible.

## 2. The service-layer adversary (the unwritten threat model)

Tony's calibration: **mid-capability nation-state, goal = drive attack cost
above the value of the attack** ("not worth the hassle" is a design target, not
a hand-wave — every defense should carry a *current-dollar* cost figure; note
CURRENT, because PQ resets the figure). Capabilities beyond A1.3:

1. **Key compromise (not just substitution).** The signing key is *taken*. A1.3
   explicitly excludes breaking primitives; a compromised key IS the primitive
   in enemy hands.
2. **MITM** — active, online, interactive. A1.3 is essentially an offline
   forgery model.
3. **PQ retroactive history-rewrite.** When a CRQC exists, every classical
   signature in history becomes forgeable *retroactively*. This is why the
   "upgrade the signatures" mechanism exists — it is the defense against
   retroactive primitive-break, and it maps exactly onto the **time-indexed
   validity** principle (below).
4. **Operator death.** If Tessera is gone: who can still verify, and who can
   still attack? Integrity that rests on Tessera's servers dies with Tessera.
   Bitcoin-anchoring is the survivability substrate — *if* the design can be
   reconstructed from what's anchored, not from a Tessera database.

**Design posture (idea 11, generalized).** Assume EVERY party — issuer,
operator, expert, AND beneficiary — is a potential adversary. Design so each
one's misbehavior is *detectable* rather than *prevented*. Assume-compromise is
not an edge case, it is the center.

> **CORRECTED 2026-07-19 (Codex review).** The original named this posture
> "trust-minimized via **universal** detectability." **Overclaim.**
> Detectability always has coverage assumptions: a censored node seen by nobody
> leaves no mark; a stolen key making one plausible statement never equivocates;
> an opinion commissioned outside the marketplace leaves no protocol trace;
> availability failure can erase the very evidence needed to show misconduct.
>
> **Corrected posture:** *trust minimization through **bounded** detectability
> under explicit observer, retention, and non-collusion assumptions.* Less
> lyrical, and it can become a theorem — which is the point. Preferring the
> quotable phrasing was exactly the temptation this project exists to resist.

## 3. Time-indexed validity (resolved this session)

Apparent conflict: "once a decision is visible it cannot change" (Tony's
distributed-systems invariant) vs. "delta belongs to the verifier" (A1.2, a
verifier may apply stricter standards). **Resolution (Tony's):** a decision is
valid *at its evaluation time under the standard then in force*. Immutability
attaches to the **(receipt, time, standard) verdict**, not to the receipt. A
verifier applying a later, stricter standard (e.g. post-PQ) reaching
"invalid-now" is **not** revoking the earlier valid-at-t verdict — it is a new
verdict at t'. Both are true. The PQ-signature-upgrade path is the concrete
mechanism: accept the PQ-signed amendment, judge the pre-PQ signatures
inadequate *now*, without rewriting the past.

Consequence: A2.1's *unconditional* "no honestly-shipped receipt can fail the
confirmation conjunct" is an **overclaim**; the true guarantee is issuance-time-
indexed. This is a wording correction, not a model defect. (`polDelta` stricter
than `Delta` is therefore *correct behavior*, not the defect Codex flagged.)

> **REFINED 2026-07-19 (Codex review).** Time alone is not a sufficient index.
> Two verifiers *at the same instant* may hold different policies, evidence
> snapshots, and trust stores. The stable relation is closer to:
>
> ```
> Verdict(bundle_hash, policy_id, evidence_snapshot_hash, evaluated_at)
> ```
>
> And the claim should be *"both verdicts are authentic and correct under their
> recorded contexts,"* not the unqualified "both are true."

## 4. `confirmedAt` must be verifier-derived (causally forced)

Not a design choice — a causal necessity. The OTS proof and txid **postdate**
the signed bytes (the anchor is computed over those bytes; they exist only
after). So `confirmed_at` **cannot** be a trusted receipt field; it must be
DERIVED by the verifier: `txid → inclusion block h → header chain → block
h+k−1 → its timestamp`. A deriving verifier is also a **differential oracle
against the issuer's own implementation** — it catches implementation errors,
not just logic errors (Tony's point, stronger than the original framing).

Asymmetry worth recording: the signed payload has a multi-key, length-bound,
injective-canonicalization defense stack. `confirmedAt` has **none of that** —
it is outside the signature by causal necessity, defended *only* by the
derivation path. So the derivation-conformance tests (wrong block height,
off-by-one h+k−2/h+k, disconnected headers, non-monotonic timestamps,
receipt-supplied value, unavailable-vs-invalid) are not defense-in-depth for
`confirmedAt` — they are its *entire* defense.

## 5. The architecture candidate — a causal-DAG commons + a market over it

The keystone move (idea 9, Tony's sharpening): **attestation needs causal
consistency, not linear ordering.** Linear order across an asymmetric network is
a consensus problem — slow, quorum-dependent, and *impossible to provide
honestly* once no single party owns the log. And it is an overclaim anyway:
Bitcoin gives total order only at block granularity; sub-block ordering is not
attested. **Attestation is an existence + integrity claim, not an ordering
claim.** First-to-file is explicitly NOT claimed — "let the patent office be the
oracle" (Tony). (Cf. Tony's paper *Legible Consensus: Topology-Aware Quorum
Geometry for Asymmetric Networks* on the cost of linear ordering.)

Therefore the structure is a **Bitcoin-anchored, client-held causal Merkle-DAG**,
not a chain:

- A **node** = signed bytes of one attestation: `canonical(payload_hash,
  length, type_tag, issuer_identity, key_fingerprint, manifest_hash,
  causal_parents (set of predecessor node-hashes — the DAG edges),
  declared_issue_time)` + signature(s) + (alongside, NOT signed) ots_proof,
  txid.
- **No `id-of-next`.** Forward preallocation assumed linear succession; a DAG
  has many concurrent children, so "the next" is undefined.

  > **CORRECTED 2026-07-19 (Codex review). The original claim here was FALSE
  > and it was this note's worst error.** It read: the takeover-detection
  > property "relocates" to equivocation-visibility, because a compromised key
  > forking causal history produces two nodes at the same causal position — so
  > takeover-detection and compromise-detection are "the same mechanism," "this
  > is how Certificate Transparency detects a bad log."
  >
  > **Why it is wrong.** An attacker with a stolen key *need not fork
  > anything*. They publish ONE plausible continuation. No conflicting sibling,
  > no topological anomaly, nothing to detect. In a DAG, two children of one
  > parent are ordinary concurrency unless the protocol defines a unique causal
  > position (e.g. `(issuer, epoch, sequence)`) at which only one event is
  > permitted. Topology cannot distinguish a malicious continuation from a
  > legitimate one.
  >
  > **Takeover detection ≠ equivocation detection.** They are distinct
  > properties. Detecting key takeover requires an *independent authority
  > source*: recovery keys, witness cosigning, threshold control, device
  > continuity, delayed activation, or an externally monitored key-event
  > policy. Parent hashes provide none of these.
  >
  > **The CT analogy was also wrong.** CT is an *ordered append-only Merkle
  > tree* with signed tree heads, inclusion proofs and consistency proofs, plus
  > explicit observer/gossip assumptions — not a causal DAG. CT does not detect
  > malicious leaf-signing keys topologically. (RFC 9162
  > <https://www.rfc-editor.org/rfc/rfc9162.html>; IETF Key Transparency
  > architecture
  > <https://datatracker.ietf.org/doc/draft-ietf-keytrans-architecture/>.)
  > The error was reaching for a familiar precedent to buttress a claim without
  > checking that the precedent had the structure being attributed to it.
  >
  > **What replaces it:** a DAG of claims **plus one or more ordered
  > transparency overlays**. The DAG is a claim-data model; continuity and
  > non-equivocation are separate layers with separate mechanisms.

- **On "unowned."** *Original claim: people trust the commons because nobody
  owns it — "a feature, not a cost."* **Corrected:** absence of an owner is not
  itself a trust property. No owner also means nobody necessarily owes
  persistence, moderation, repair, or funding. Trust should come from
  verifiability, plural custody, transparent governance, and easy exit — not
  from ownership's absence alone.

### The market (corrected — market ≠ expert opinion)

- An **expert opinion is a node IN the commons** — an attestation whose payload
  is "I, <expert>, verified <property> of <parent_node>," causally linked,
  anchored, gossiped. Recursion: the evidentiary package is a *subgraph*.
  (Worked example: HotCRP-with-attestations where a paper signs its reference
  set; each reference is itself an attestation; a citation-checker like
  Russinovich's `refchecker`
  <https://github.com/markrussinovich/refchecker> attaches an opinion node;
  a reviewer sign-off attaches another.)
- The **marketplace is NOT in the DAG.** It is a directory + integration layer:
  how a workflow *finds* an acceptable expert and *invokes* them conveniently.
  Customers pay the *expert* for the opinion; the marketplace monetizes
  *discovery/convenience* (app-store-over-the-commons, not the apps).
- **Eating the base-layer business model is the point.** The commons is a free,
  unowned substrate; a competitive expert-market can only exist *because* the
  substrate is unowned. You run one instance of that market. (Willay heritage:
  "survivability without our service is an objective." The irony recorded by
  Tony: building the truly-decoupled layer is *why* people use it — "nobody owns
  it.")

## 6. The beneficiary adversary (the session's sharpest discovery)

Shifting cost to the beneficiary (they pay for strengthening) creates an
adversary class **inside the trust boundary**: the *subject/beneficiary of the
attestation attacking the content of the package*.

> **CORRECTED 2026-07-19 (Codex review).** The original said A1.3 "entirely
> misses" this. **Not accurate.** A1.3 (`phase-0-prereg-amendment-1.md:347`)
> already names an adversary using *legitimate issuance credentials* and
> deliberately places that behavior **outside** the cryptographic construction.
> The boundary was drawn on purpose. What this exploration actually showed is
> that the **marketplace makes that boundary load-bearing at the product
> layer**, so it now needs its own formal product-layer treatment — not that it
> was overlooked.

Distinct attacks:

1. **Opinion shopping / expert laundering.** Pay experts until one is favorable;
   attach only that one. Every node is *valid*; the subgraph is a lie **by
   omission**. (The pay-your-own-auditor capture problem, cryptographically
   reborn.) The commons's integrity guarantees are useless here — nothing was
   forged, evidence was *selected*.
2. **Sybil experts.** The beneficiary *is* the "independent" expert.
   Manifest-authority proves key *possession*, not opinion *independence*.
3. **Fabricated-parent / narrow-truth gap.** Attest a fabricated artifact, then
   attach genuine expert opinions that check the *wrong narrow thing* (format
   valid ≠ cited work exists / says what's claimed).

**Why this is structurally hard:** it is the DUAL of equivocation.
- Equivocation = "did anyone show *different* histories?" → defended by
  gossip + consistency (make the full DAG visible).
- Beneficiary curation = "did the beneficiary show an *incomplete* history?" →
  needs **completeness / non-omission proofs**, a much harder and less-solved
  problem. And the very decentralization that defeats the *operator-takeover*
  adversary **empowers** the *beneficiary-curation* adversary: with no owner,
  nothing authoritatively says "here is the COMPLETE set of opinions about X."

**Candidate defenses (economic/structural, fitting cost-driving — none
discharged):**
- **Scoped completeness (CORRECTED).** *Original: an expert attests "I searched
  the commons for all attestations about `payload_hash` as of block h; here is
  the Merkle root of what I found," and omission becomes detectable by re-running
  the search.* **A Merkle root of "what I found" proves what the searcher
  committed to — not that the search was complete.** Re-running proves an
  omission only if all of these were fixed beforehand: the registries searched;
  authenticated checkpoints for each; the query specification and software
  version; the subject-identity rule; the cutoff; inclusion/non-inclusion
  semantics; and availability of the relevant registry history. A defensible
  node reads:

  > *I searched registries R1…Rn at signed checkpoints C1…Cn, using query
  > specification Q and software version V, through cutoff H, producing
  > result-set root M.*

  That yields **scoped, falsifiable completeness**. It cannot prove no relevant
  opinion exists outside those registries, and must not claim to.

  **Product hazard (Codex):** "all claims about X" invites spam, adversarial
  accusations, and cheap Sybil noise. The property actually wanted is usually
  **completeness of a declared review process or commission**, not completeness
  of the permissionless universe.

- **Attested reputation — necessary, not sufficient (CORRECTED).** Reputation
  helps estimate *quality*; it does **not** establish *independence*, since a
  Sybil can manufacture activity. Independence depends on external identity and
  relationship evidence.

- **Mandatory disclosure is a MARKETPLACE (governance) property, not a commons
  property.** To prevent shopping, the commission must be recorded *before* the
  expert begins, and *every terminal outcome* must produce a record: completed,
  declined, conflicted, abandoned, disputed. Even then Tessera can guarantee
  only completeness of **Tessera-mediated** commissions. Useful controls:
  relying-party or randomized expert assignment; outcome-independent payment;
  precommitted panel size and selection method; all commissioned outcomes
  recorded; conflict / payment / employer / beneficial-ownership disclosure;
  privacy-preserving status publication when the report itself cannot be public.

---

## 7. OPEN QUESTIONS (the register — roughly in dependency order)

The predicted fractal: drilling into any one of these is expected to spawn more.
That prediction is itself a reason these are captured rather than chased now.

1. **Completeness proofs in a permissionless DAG.** *The crux.* Prove "no
   relevant node was hidden" when anyone can attest anything about anything and
   no party owns the complete set. Suspected to be genuinely hard, possibly with
   an impossibility result at the edge (cf. proof-of-non-existence). The
   completeness-by-convention idea (§6) bounds it to "complete *as of block h,
   per this searcher*" — is that bound strong enough to be useful, and what does
   it cost the searcher?
2. **Equivocation-detection coverage.** How much of the DAG must a client hold
   to make forks visible? Can a fork hide in a region nobody watches? (This is
   the CT gossip-coverage problem; unsolved at the edges there too.)
3. **Operator-independent retrieval + gossip.** The experiment in §5 showed
   single-node *integrity* verification closes WITHOUT Tessera (signatures via
   DNSSEC/cache, `confirmedAt` via Bitcoin). But **parent-fetch and
   fork-gossip** currently depend on Tessera's DynamoDB "chain head." *This* —
   decoupling availability + gossip from the operator — is the real content of
   the survivability band, NOT stronger crypto.

   > **CORRECTED 2026-07-19 (Codex review).** The original floated IPFS as an
   > answer. **Bitcoin anchors commitments; it does not store the DAG** — and
   > IPFS does not persist content without pinning and *someone bearing
   > retention cost* (<https://docs.ipfs.tech/concepts/persistence/>). Content
   > addressing is useful *transport*, not survivability. A survivability
   > profile must require: self-contained export bundles; multiple independent
   > mirrors/custodians; anchored inventory/checkpoint roots; explicit retention
   > periods; **periodic retrieval drills**; and enough replication that
   > Tessera's disappearance is an *exercised scenario*, not an architectural
   > hope.

4. **The PQ-migration mechanism, concretely.** §3 gives the principle
   (context-indexed validity).

   > **SHARPENED 2026-07-19 (Codex review).** A PQ wrapper **cannot repair a
   > classical signature after that signature becomes forgeable.** *Before* such
   > a break it can make a new PQ-authenticated statement committing to the
   > exact old bytes and their pre-existing anchor — protecting the wrapper's
   > statement under new trust roots. It does **not** retroactively strengthen
   > every authority channel in the old package. Migration must therefore cover:
   > receipt signatures; manifest/identity authority; wrapper signatures;
   > transparency checkpoints and witnesses; canonicalization and hash agility;
   > and **archived verification software and policy**. NIST has already
   > standardized ML-DSA and SLH-DSA and advises beginning migration now rather
   > than awaiting a CRQC
   > (<https://www.nist.gov/cybersecurity-and-privacy/what-post-quantum-cryptography>).

7. **Attacker-cost expression (REPLACES dollar-denomination).** The session's
   "current-dollar cost per defense" framing is **false precision** — attacker
   cost depends on access, target value, zero-days, coercion, jurisdiction,
   duration, and whether discovery matters. Use **named attack paths with
   coarse, dated, sensitivity-tested bands**, e.g.: steal one online signing
   credential; compromise issuer *plus* one witness; partition all observers for
   30 days; suppress all replicas; forge after a specified primitive failure.
   The security property should state **what must be compromised
   concurrently**. Dollar estimates belong in an economic appendix, not in the
   property.
5. **Band organization (deferred, not collapsed).** Options surfaced:
   adversary-indexed bands (each band prices out one more capability);
   guarantee-lattice with bands as antichains/cuts; cost-denominated bands
   ($10^k). NOT resolved into close-Band-0-vs-expand-Band-0 — that was flagged
   as premature collapse. Whatever is chosen, the current registered Band 0 is
   *correct as the client-layer attestation* and its status contradictions
   (below) are Band-0-scoped cleanups.
6. ~~**First-to-file confirmed dropped?**~~ **CLOSED 2026-07-19 — THIS WAS MY
   ERROR, not an open question.** A2.4 (`phase-0-prereg-amendment-2.md:174`)
   does not *have* first-to-file; it **explicitly forbids** it: *"No verifier
   policy, and no downstream marketplace rule, may order competing receipts by
   declared time."* I read the fragment "order competing receipts by declared
   time" and inverted the sentence's meaning by not quoting it in full. Nothing
   to reconcile — the registered position already matches §5. Retained here as a
   worked example of why partial quotation is dangerous in this project.

## 8. Band-0 housekeeping surfaced this session (independent of the above)

These are real, small, and do NOT depend on any of the architecture speculation:

- **A2 status contradiction.** `docs/phase-0-prereg-amendment-2.md:1` says
  "DRAFT, not signed, not in force"; `P5c_IssuanceProtocol.tla:17` and
  `PROPERTIES.md:51` say A2.1 "ratified 2026-07-07". The authoritative doc says
  not-in-force; two downstream artifacts assert ratified. **Decision (Tony):
  break the chain — A2 stands as drafted, the seam finding + dispositions go in
  a NEW A3 that is honest about the sequence. No incorporate-before-sign** (that
  would be a non-atomic amendment to a draft already referenced as ratified —
  2PC changing its vote after others acted on the prepare).
- **P5c↔P5P6 correspondence** (finding #1) should become a *distinct* tracker
  obligation (TLA+↔TLA+), separate from the existing TLA+↔symbolic line; plus
  latch `confirmedAt` explicitly in P5c at `depth = DepthK` (fixes the
  "identical predicate" overclaim AND makes the derivation explicit — one change,
  two defects), with a broken-bridge companion that substitutes `anchorAt` and
  must fail.
- **P8 priority.** Reframe P8 in the tracker from a deferrable formalization
  chore to *the root-of-trust that P2/P5/P6's symbolic proofs consume*. If
  outsourced human review (the "when finances improve" option) happens, P8 and
  the `confirmedAt` derivation-conformance are where it should concentrate — not
  the already-`checked` temporal models.

## 8b. The layer decomposition (Codex, 2026-07-19) — the structural correction

The note's central structural failure was **not naming which layer owns which
property**, so the DAG was implicitly asked to provide guarantees belonging
elsewhere. Silence read as claim. This table fixes it:

| Layer | Actual guarantee | Likely mechanism |
|---|---|---|
| **Portable receipt** | These exact bytes were signed and anchored under this policy | Existing P1–P10 work |
| **Issuer continuity** | This key event belongs to the issuer's accepted lineage | Per-issuer key-event log, epochs, recovery/witness rules |
| **Transparency** | Named observers can detect inconsistent or omitted registry behavior | Append-only registries, checkpoints, consistency proofs, witnesses |
| **Claim graph** | These claims refer to these artifacts and prior claims | Content-addressed DAG |
| **Process assurance** | The review was independently commissioned and unfavorable results were not suppressed | Marketplace workflow, precommitments, assignment and disclosure rules |
| **Survivability** | Evidence remains obtainable after Tessera disappears | Portable bundles, plural custodians/mirrors, retention obligations, retrieval audits |

**The DAG belongs in row four — and only row four.** Several passages in the
original note asked it to provide properties from the other five. It is a useful
**claim-data model**, not yet a security architecture.

### Recommended disposition (Codex, endorsed)

1. **Keep Band 0 narrow — do NOT expand it to absorb the commons.** Finish the
   registered standalone-receipt guarantee: P8, the open P1–P10 obligations, the
   derived-`confirmedAt` conformance cases, and the P5c↔P5P6 bridge.

   > **Note on the bridge (Codex correction to §8's repair).** Merely *latching*
   > `confirmedAt` under P5c's single clock would make the correspondence **true
   > by construction without testing the real seam.** The bridge must model
   > block timestamps *separately* and derive `confirmedAt` from headers.

2. **Register the survivability/transparency program separately**, with its own
   adversary model and properties: key continuity, fork detection *with coverage
   assumptions*, registry consistency, data availability, recovery, algorithm
   migration. Cf. IETF SCITT's separation of portable signed statements from
   append-only transparency services
   (<https://datatracker.ietf.org/doc/html/draft-ietf-scitt-architecture-09>).

3. **Retain the DAG as the claim model** — "portable claim graph" / "federated
   evidence graph." Overlay named transparency registries and witnesses where
   stronger guarantees are needed. **Do not call the graph complete,
   consensus-bearing, or takeover-detecting.**

4. **Treat marketplace assurance as governance**: commission precommitment,
   assignment, conflict disclosure, terminal-outcome recording.

> Codex's summary, which is the honest account of this note's contribution:
> *"The exploration did not invalidate Tessera's foundation. It revealed that
> the project had begun silently asking the foundation to support a cathedral.
> The right response is neither to discard the foundation nor to enlarge it
> indefinitely — it is to name the additional structures, give each its own load
> claims, and refuse to call adjacency a proof."*

## 9. Meta-observations (method, not content)

- **Fusion, repeatedly.** Three times this session the answer was not in the
  option list but a *weave* of it (the tail-sample's value was #10+#11+#15
  pointing at one attractor — operator-independence — from different angles, not
  any single idea being right). When low-temperature samples converge from
  independent directions, the attractor is load-bearing. Reusable move.
- **The falsification gate worked on the assistant — twice, and the second time
  was worse.** Round 1: Claude's alarming `confirmedAt` claim was wrong; Codex's
  384-state check killed it; the narrow real gap survived. Round 2: Codex's
  review of *this note* found six wrong claims (header), including a false
  security property (DAG ⇒ takeover detection) propped up by a **misapplied
  Certificate Transparency analogy**. The failure mode in both rounds was the
  same: reaching for a plausible mechanism or precedent and asserting it fits,
  without checking the structure being attributed to it. An AI-authored critique
  of AI-assisted work is precisely the correlated-blind-spot case A1.7 exists
  for. **The standing argument for outsourced review now has two worked
  examples, both against the assistant.**
- **Preferring the quotable phrase is a detectable failure signal.** "Universal
  detectability," "the same mechanism," "a feature not a cost" — each was
  lyrical and each was an overclaim. In this project, a phrase that resists
  becoming a theorem should be treated as suspect on that basis alone.
- **"The method as the product" (idea 16) kept recurring unbidden.** Either a
  Claude bias or a real signal that the anchored-falsification-band discipline is
  the most-demonstrated artifact here. Flagged for skepticism *and* attention;
  candidate for an eventual written case study.
