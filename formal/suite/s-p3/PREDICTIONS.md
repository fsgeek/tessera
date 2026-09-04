# S-P3 — key binding (anti-DSKS): query plan and registered predictions

**Status: PROPOSED — drafted by the AI collaborator 2026-09-04; not
frozen; no model exists and nothing has been run.** Per
`formal/suite/ENUMERATION.md` §5, predictions are registered and
frozen — by the author's signing commit — before any S-P3 model is
run. The author's cold read of this file precedes that commit.
Post-freeze changes are prediction divergences (spike rule), never
refinements.

Governed by: `ENUMERATION.md` §1–§2, §5 (discipline), §6 (sequencing:
S-P3 first); Amendment 1 §A1.3 item 3 (the DSKS capability) and P3 as
registered there; A3 §A3.3 (ledger conservation fields; three-outcome
timebox discipline); `ENUMERATION.md` amendment note 1 item 2 (the
four things S-P3 owes) and note 2 (possession over the manifest).
Library: `formal/suite/lib/tessera_theory.pvl` (PROPOSED), whose
divergence record D-3 (possession over manifest) and D-4 (DSKS
expressible) exist for this model.

## Target

P3 as registered (Amendment 1, verbatim in its operative sentences):

> Acceptance binds each signature to the issuer identity committed in
> the signed bytes. The adversary model (A1.3) explicitly includes
> key-substitution attacks (DSKS / exclusive-ownership failures:
> constructing a different keypair under which an existing
> message–signature pair verifies, then re-presenting the package
> under a substituted manifest). […] Discharge is split: the binding
> of identity into signed bytes — the signed bytes include, at
> minimum: domain-separation tag, object type, algorithm identifier,
> issuer identity, key fingerprint, manifest hash, and
> canonicalization version — is **[model]**; the implementation's
> verification profile is **[assumption]**.

S-P3 is the **[model]** half only. It does not touch the verification
profile, which is Layer 2 and H1a evidence.

**What "producer for the fingerprint relation" has to mean** (note 1
item 2, all four items, in this plan's terms):

- (c) *key substitution is expressible* — the library's D-4 rule: from
  one seen signature `s = sign(m, k)` and fresh `r`, the adversary
  derives `dsks(s, r)`, a private key it holds whose public key
  verifies `s` to `m`. Nothing else is granted (library header).
- (a)/(b) *registration* — in this design the object that "registers"
  a key is the **manifest**: it names the issuer identity and the
  key fingerprint(s), and possession is the manifest self-signature
  (A1.5 item 3, P10; library D-3). S-P3 models the manifest naming a
  key and the verifier demanding possession *over that manifest*
  under the named key, with an adversary attempting to have a
  manifest accepted that names a key it does not hold — including
  the DSKS route: re-using the honest self-signature under a derived
  key. The companion (Q4) omits the demand that the manifest name the
  accepted key.
- (d) *multi-key manifest* — Q5, two required signers, each
  signature binding its own signer's identity and fingerprint.

**Registration reading — ADOPTED (author, 2026-09-04, in session).**
The collaborator's reading of note 1 item 2(a)/(b) — that in this
design the manifest is the registering object and the verifier's
possession-over-manifest demand is the gate, with no channel-side
possession gate — was put to the author with an invited push-back for
a channel-side gate. The strongest case found (fails earlier on the
issuer's own unheld keys; independent of verifier correctness) does
not survive A1.3: the registered adversary holds every key it uses,
including substituted ones, so a channel gate blocks only keys nobody
holds, which already fail closed at issuance; and it would add a
signature to each archived channel format (format-freeze territory)
for no adversary gain. Author's words: "Decision made, Author
ratified." Provenance: reasoning originated with the collaborator;
labeled ADOPTED, not RULED, per the DECISION.md scheme. Channel-side
possession proofs remain relevant to succession (row 2, docket item
25), not to registration.

## Abstractions this plan fixes (and their residuals)

- **Framed bytes are structured.** The spike's framed bytes were an
  opaque free term. S-P3 needs the binding *content*, so the signed
  object is `framed(objType, alg, issuerId, kfp, mh, canonVer,
  payload)` under the `BYTES` tag — the P3 field list, as a
  transparent data constructor. **Residual:** the exact frame layout
  and encoding are P8's (its four-field frame is unchanged by this
  model; the model's constructor is an abstraction of "these fields
  are inside the signed bytes," not a layout claim).
- **Manifest = the map-v1 authority tuple** `authTuple(issuerId,
  kfp, sset, alg, ver)` for n = 1; for Q5, `sset` carries the second
  fingerprint. Non-authoritative manifest fields (labels) are ignored
  by construction (map v1) and omitted. **Residual:** manifest hash
  `mh = h(manifest)` inherits h's idealization (library).
- **Possession** is `sign((POSS, manifest), sk)` — D-3. A model
  signing `POSS` over a fingerprint alone is a broken companion by
  definition.
- **Fingerprint match** `fp(kX) = kfp` is a key-equality check in the
  model (fp injective). **Residual:** fingerprint collision
  resistance and P8's "what bytes are fingerprinted" — the library
  header's fp idealization; every S-P3 ledger entry cites it.
- **Signatures are deterministic.** The judge (below) equates
  evidence by term equality, so it equates *more* than a byte-level
  judge; unreachability in the model is conservative for the real
  judge (guide A2). Stated, not assumed.
- **Rejection is non-acceptance** (spike idiom); verdict partition is
  P4's.

## Adversary and modes

A1.3 throughout, with item 3 now expressible (D-4) and possession free
(item 3, P10). Two evidence modes, run separately:

- **Strict** — two authority channels, both required; **one
  compromised** (its signing key public); both channel variants run,
  as in the spike (a generic single channel is not accepted as
  representing both).
- **Degraded** — one authority channel (sole evidence, per A3.2
  `VALID_DEGRADED` never-zero) and **that channel compromised**. This
  is P3's hard case: strict mode's cross-channel tuple agreement
  already stops a substituted manifest (A1.3 "never all"); in
  degraded mode nothing but the in-bytes binding stands between an
  honest signature and a substituted identity. If S-P3 earns its keep
  anywhere, it is here.

The relying-party consequence the model is meant to sharpen (note 2,
last bullet): in degraded mode, impersonation *with the adversary's
own key over its own bytes* remains reachable and is not P3's
subject; **re-attribution of the honest issuer's bytes to another
key/identity** is P3's subject and must be unreachable.

## The judge (encoding registered here, before any run)

Re-attribution is mechanized as the spike's private-channel judge
(Q4 pattern, ledger entry 4): the honest issuer reports `(pk(skI),
fb)` for each object it signs on a private channel; the verifier
reports `(kX, id, fb)` for each acceptance; the judge fires
`Reattributed(kX, kH, fb)` on receiving an honest report and an
acceptance for the **same `fb`** with `kX ≠ kH`. The registered query
is unreachability of `Reattributed`. A second judge event,
`PossessionTransplanted(kX, ppf)`, fires when an acceptance under
`kX` presented a possession proof term equal to the honest issuer's
self-signature while `kX ≠ pk(skI)`.

Deliberate scope of the judge: it is keyed on the *exact* honest
bytes. It does not claim anything about bytes the adversary signed
itself (impersonation, out of scope above).

## Query ladder, timeboxes, predictions

Outcome vocabulary is the registered three: **violation**
(counterexample trace), **timeout** (mechanism failure — evidence
about the tool or encoding, never about the property), **termination**
(evidence for the checked abstraction only). Timeboxes are per run;
each channel/mode variant gets the full box.

**S-P3.Q1 — correct model, strict mode: sanity and linkage.**
Both channels required, one compromised (both variants). Queries: (i)
`Reattributed` unreachable; (ii) the spike's first-link
correspondence still holds against the structured frame and
possession-over-manifest (nothing in S-P3 may weaken what the spike
established).
- Timebox: 15 minutes per variant.
- Prediction: both queries hold, both variants. (p ≈ 0.7; p ≈ 0.15
  violation — most likely a frame/possession encoding defect
  needing one recut, disposition by trace inspection; p ≈ 0.15
  timeout — the DSKS rewrite rule and the wider frame enlarge the
  term space.)

**S-P3.Q2 — correct model, degraded mode, sole channel compromised:
the P3 claim.** The adversary controls the only authority channel and
holds the DSKS capability. Query: `Reattributed` unreachable.
- Timebox: 30 minutes.
- Prediction: unreachable, terminating. (p ≈ 0.6; **p ≈ 0.2 a real
  re-attribution surfaces** — the outcome that earns the model its
  keep: it would mean the P3 field list as registered is not
  sufficient binding under DSKS, an amendment trigger, not a recut;
  p ≈ 0.2 timeout.) Q2 carries the highest genuine uncertainty in
  this ladder.

**S-P3.Q3 — broken companion A: frame omits the binding.** Mutation:
the framed bytes carry no issuer identity and no key fingerprint
(the spike's opaque-bytes shape, made explicit). Degraded mode, sole
channel compromised. Required result: `Reattributed` **reachable** —
the adversary derives `dsks(sg, r)` from the honest attestation
signature, publishes its fingerprint through the compromised channel
in a manifest it self-signs, and the verifier accepts the honest
bytes under the derived key.
- Timebox: 15 minutes.
- Prediction: violation found, trace readable. (p ≈ 0.75; p ≈ 0.15
  the DSKS rule needs one encoding recut to fire in ProVerif's
  resolution — a tool finding, recorded as such; p ≈ 0.1 timeout.)
  Per the Grok panel criterion: if no companion can be made to go red
  at all, that is an amendment trigger (the theory does not express
  the threat), not a shrug.

**S-P3.Q4 — broken companion B: possession without naming.**
Mutation: the verifier checks that the possession proof verifies
under `kX` but not that the manifest it covers names `fp(kX)`. Degraded
mode, sole channel compromised. Required result:
`PossessionTransplanted` **reachable** — the honest self-signature,
verified under a DSKS-derived key, is accepted as that key's
possession proof.
- Timebox: 15 minutes.
- Prediction: violation found. (p ≈ 0.7; p ≈ 0.2 the mutation needs a
  recut because the correct model's other checks already block the
  path — itself a finding about which check is load-bearing, worth a
  ledger line; p ≈ 0.1 timeout.)

**S-P3.Q5 — multi-key manifest (A3.2 item 3, note 1 item 2(d)).** Two
required signers; the manifest names both fingerprints; each
signature's frame binds *its own* signer's fingerprint; possession
proofs from both keys over the manifest. Degraded mode, sole channel
compromised. Queries: `Reattributed` unreachable for either signer;
companion: the second signer's frame omits its fingerprint → red on
that signer only.
- Timebox: 30 minutes per model (correct and companion).
- Prediction: correct model holds; companion red on exactly the
  second signer. (p ≈ 0.55; p ≈ 0.2 encoding defect — the two-signer
  verifier is the largest process in the ladder; p ≈ 0.25 timeout,
  concentrated here.)

**Ablation rule (on any timeout):** drop fields from the frame from
the payload end toward the binding fields, then drop the second
signer (Q5), re-run, and record the break point. A timed-out query's
ledger entry records "mechanism failure at N fields/signers," never a
property claim.

**Ordering rule:** Q1 before Q2; Q2 before Q3 and Q4 (a companion is
evidence only against a matching correct form); Q5 last. Strict-mode
channel variants both run for Q1; degraded mode is single-variant by
construction.

## What S-P3 produces, and for whom (ledger interface, A3.3 fields)

Producer entries this model will supply, each with consumer, shared
term, adversary at the join, and residual:

1. **Key-binding relation** — `Accept(kX, id, fb)` implies `fb`'s
   committed `(id, kfp)` equals `(id, fp(kX))`, and honest bytes are
   never accepted under a key other than their signer's
   (`Reattributed` unreachable, Q2). Consumers: S-P1 (integrity over
   bytes presupposes whose bytes), S-P2 (signer-set completeness
   presupposes each signature's owner), S-P7 (standing binds to
   innermost issuance identity), and — carried forward — S-STANDING's
   entitled-key check inside the standing path (ENUMERATION note 4).
   Shared terms: accepted key, issuer identity, framed bytes.
   Adversary at the join: A1.3 with DSKS, sole channel compromised.
   Residuals: fp collision resistance (library header); h
   idealization for `mh`; deterministic signatures; frame layout
   (P8); verification profile (P3's [assumption] half, H1a).
2. **Possession binds the manifest to the named key** (Q4's correct
   form) — consumer: S-P2's degraded-mode signer-stripping companion
   (note 2), which relies on possession-over-manifest being the
   load-bearing check.

Severing companions for the discharge matrix (§3): Q3 severs entry 1;
Q4 severs entry 2. The matrix itself is written only once the models
exist (§3's own rule).

## What this plan does not claim

- Anything about the verification profile: library, encodings,
  low-order points, cofactor variant — Layer 2, H1a.
- That DSKS is *practical* against Ed25519 as deployed. The rule
  grants the capability because A1.3 registers it; the model shows
  the binding defeats it if granted, which is the stronger claim.
- The frame's byte layout (P8), or that `framed(...)` is the frame.
- Semantic validity of the issuer identity, or authority — P10 and
  the first link own those; S-P3 consumes the first link as the spike
  established it and adds nothing to it.
- Impersonation with the adversary's own key in degraded mode: out
  of scope by construction, and reachable; the relying-party story
  must say so in the terms note 2 fixed.

## Review log

- 2026-09-04 — drafted by the AI collaborator after extracting the
  library and diffing the nineteen spike models; the DSKS rule and
  possession-over-manifest were parse-checked and the spike's Q1
  correspondence re-run against the extended theory as a
  **library smoke test only** (scratchpad, not committed, not
  evidence): Q1 remains true under the DSKS-capable theory, which is
  the expected shape (DSKS derives keys for seen signatures; it does
  not forge signatures). No S-P3 model has been written or run.
