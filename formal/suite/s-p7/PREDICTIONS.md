# S-P7 — wrapper / object-type soundness: query plan and registered predictions

**Status: PROPOSED — clerk-drafted 2026-09-06 by the AI collaborator;
not adopted; the commit is the author's. No model exists and nothing
has been run.** Per `formal/suite/ENUMERATION.md` §5, predictions are
registered and frozen — by the author's signing commit — before any
S-P7 model is run. Post-freeze changes are prediction divergences
(spike rule), never refinements. Amend-don't-rewrite applies from this
file's first commit.

Governed by: `ENUMERATION.md` §2 (S-P7 entry), §4 (cross-formalism
joins), §5 (discipline), amendment note 1 item 1 (cross-form control
proposed struck from S-P7, ratification pending — see "Deliberately
not registered" below), note 3
(N1 reachability witness; N2 two honest values per bound axis), note
4 (S-STANDING owns the standing-evidence construction); Amendment 1
§A1.2 P7 as registered and §A1.3 item 4 ("re-frame objects across the
P7 type boundaries"); A3 §A3.1 item 3 (coverage map: type/wrapper →
P7), §A3.7.1 (standing invariant: evidence binds *issuance
identity*), §A3.9 (Kimi-2 integrated lifecycle model — NOT this
model; see boundary below); the original pre-registration's "What
the wrapper attests" (`docs/phase-0-prereg.md`, the paragraph
beginning at line 357). Suite rules carried from S-P3
(`formal/suite/s-p3/RESULTS.md`, "Suite rules from S-P3"): judge
report outputs parallel with continuations; N1 witness is honest-flow
acceptance emitted by the judge, never bare acceptance; judge locals
never shadow library names; each model header names which checks are
load-bearing. Library: `formal/suite/lib/tessera_theory.pvl`
(PROPOSED); a model may not redeclare a library term.

## Target

P7 as registered (Amendment 1 §A1.2, verbatim in its operative
sentences):

> Every signed object carries a domain-separation type tag *inside
> the signed bytes*, drawn from the enumerated set: base attestation,
> wrapper, issuer-key manifest, authority evidence, conformance
> vector, review-recency attestation (§4.7). No trace exists in which
> an object of one type is accepted as another (no cross-type
> confusion). A wrapper commits to the inner package's **exact bytes,
> embedded as an opaque byte string** […] — never as parsed JSON.
> Outer canonicalization must be structurally unable to re-serialize,
> re-escape, or otherwise touch the inner byte stream […]. The
> wrapper records both inner and outer canonicalization versions.
> Wrapping never alters the inner package's independently-computed
> verdict — the wrapper attests the inner *bytes*, never the inner
> *verification result* […]. **[model]**

and the suite's sharpening of it, `ENUMERATION.md` §2:

> Wrapping does not re-scope identity or authority: standing binds to
> innermost issuance identity; a wrapper cannot re-scope it.

Three claims fall out, and this plan's queries are organized by them:

- **C1 — type soundness.** A *framed* object signed as one enumerated
  type is never accepted as another. (S-P3 finding F7 placed the
  *check* of the object-type field here: S-P3 binds the field and does
  not check it.) Scope limit, stated up front: the manifest
  (`authTuple`), possession proof (`POSS`), and authority evidence
  (`STMT_*`) are distinct library constructors with no object-type
  field; confusion between those kinds and framed objects is
  unrepresentable in ProVerif for the reason ENUMERATION note 1 item 1
  gives for the cross-form control (guide M5), so C1 is exercised here
  only among framed kinds. Recorded as an open coverage-map cell under
  "Deliberately not registered".
- **C2 — scope soundness.** A wrapped presentation attributes the
  inner artifact's issuance identity and key to the *innermost*
  frame's committed `(issuerId, kfp)`, never to any wrapper's. This is
  the targeted piece of the Kimi-2 transplant: a wrapper cannot lend
  its own identity or authority to the artifact it encloses, nor
  borrow the enclosed artifact's for itself.
- **C3 — commitment soundness.** The wrapper commits to the inner
  bytes as an opaque term; the inner artifact's acceptance inside the
  wrapped presentation is exactly its standalone acceptance, for any
  pair of inner/outer canonicalization versions. (The mechanized
  form of Antigravity's P7 finding, `docs/reviews/2026-07-03-antigravity-amendment-1-review.md`
  finding 1 — "Outer canonicalization re-serializes nested JSON,
  altering inner bytes" — whose *hash-only* alternative fix was
  rejected at incorporation because P9's self-containment requires
  the inner bytes to travel inside the bundle.) C3 is encoded **by
  construction** in this plan (one inner-check process invoked in
  both paths, below) and is not stated by any registered query; what
  the ladder supplies for it is a witness/control pair (Q1/Q2's
  `HonestWrappedAccepted` reachable; Q4's red/green). See ledger
  entry 3 for what that does and does not license.

`PROPERTIES.md` assigns P7 "TLA+ and ProVerif". S-P7 is the symbolic
leg. Under the author's 2026-08-29 ruling on ENUMERATION question 2
(`ENUMERATION.md`, "Author dispositions", Question 2 — RULED:
narrowing is acceptable "so long as at least one leg covers every
claim"), this plan states which of P7's sentences the symbolic leg
covers (C1–C3) and names the residue at the end. It does not claim
the TLA+ leg.

## Boundary with S-STANDING (drafted reading; see routed question 1)

ENUMERATION's author disposition of 2026-08-29 and amendment note 4
place the standing-evidence construction (terminal lineage record)
and its Kimi-2 transplant companion — "standing evidence moved from a
valid inner artifact onto a forged outer one → red" — in
**S-STANDING**. ENUMERATION §2 places "the *targeted* piece" of the
transplant threat in S-P7. This plan reads the seam as follows:

- S-P7 models **no standing evidence object**. Its subject is the
  *identity relation* a wrapped presentation establishes: which
  `(issuerId, kfp)` the verifier attributes to the inner artifact.
- S-STANDING consumes that relation (its entitled-key check inside
  the standing path, note 4 item 2, needs to know *whose* artifact
  it is assessing) and models the evidence object and its transplant.
- Consequently the §4 cross-formalism join "refusal/standing state
  (producer: P5c refusal latch) consumed by S-P7's standing claims"
  is, under this reading, consumed by S-STANDING, not S-P7. S-P7 as
  drafted consumes no TLA+ join; that is recorded in the ledger
  interface below so the capstone does not look for one here.

If the author reads ENUMERATION §2's sentence as requiring S-P7 to
model standing evidence itself, that changes this plan's scope and
must precede the freeze. **ROUTED TO AUTHOR** (question 1 below).

## Abstractions this plan fixes (and their residuals)

- **Object types are constants.** Six model-visible constants, one
  per enumerated P7 type: `OT_ATTEST`, `OT_WRAPPER`, `OT_MANIFEST`,
  `OT_AUTHEVID`, `OT_CONFVEC`, `OT_REVIEWREC`. Proposed as library
  divergence record **D-5** (the library currently carries no object
  type; S-P3 declared a model-local `objTypeH`) so S-P1/S-P2 and the
  capstone share the names; if D-5 is not entered before S-P7 runs,
  the constants are declared model-locally and the ledger notes the
  term is not yet shared. Only `OT_ATTEST` and `OT_WRAPPER` (and, for
  N2 on the type axis, `OT_REVIEWREC`) are *exercised*; the other
  three are declared so the enumeration is the registered one, and
  are unexercised — stated in every header. **Residual:** that the
  implementation's type-tag bytes are these six and no others is a
  P8 golden-vector / H1a fact.
- **Frame.** S-P3's `framed(objType, alg, issuerId, kfp, mh,
  canonVer, payload)` under `BYTES`, declared model-locally with the
  identical shape so the ledger's shared term "framed bytes" is the
  same term in both models. A base attestation is
  `framed(OT_ATTEST, …)`. **Residual:** frame layout is P8's (S-P3
  residual, carried).
- **Wrapper.** A wrapper is itself a framed object,
  `framed(OT_WRAPPER, algW, idW, fp(kW), h(mW), cvOuter, wrap(cvInner,
  innerBlob))`, signed under `BYTES` by the wrapper issuer's key, where
  `innerBlob` is the **inner bytes and inner signature as terms** —
  the opaque embedding is the term itself. `wrap` is a transparent
  `[data]` constructor recording the inner canonicalization version
  beside the blob (P7: "records both inner and outer canonicalization
  versions"). The wrapper issuer has its own manifest, authority
  evidence, and possession proof, exactly as an S-P3 issuer.
  **Residual:** that a concrete base64-of-framed-bytes embedding is
  in fact structurally opaque under the outer JCS pass is P8/H1a —
  the symbolic model makes opacity true by construction and cannot
  test it; what it *can* test is the companion where the embedding is
  not opaque (Q4).
- **Re-serialization** is a destructor `reserialize(v, canon(v0, x))
  = canon(v, x)`: applying outer version `v` to bytes canonical under
  `v0` yields bytes canonical under `v`, identical to the input iff
  `v = v0`. Inner bytes in Q4 are `canon(cvInner, framed(…))`. This is
  the minimum theory under which Antigravity's finding is
  expressible; nothing about *what* changes between versions is
  modeled. **Residual:** canonicalization semantics are P8's.
- **Verifier for a wrapped presentation** checks the outer object as a
  base verifier would (outer authority, possession, signature, frame,
  `objType = OT_WRAPPER`), then unwraps and checks the inner object
  **independently and completely** — inner authority evidence
  against the inner manifest, inner possession, inner signature over
  the inner bytes under the inner frame's key, `objType = OT_ATTEST`
  — and emits an acceptance event carrying **both** `(kW, idW)` and
  `(kI, idI)` where `(kI, idI)` are read from the *inner* frame and
  verified there. "Wrapping never alters the independently-computed
  verdict" is encoded as: the inner check in the wrapped path is the
  same process as the standalone base verifier (a single `let`
  process, invoked in both paths), never a check of a wrapper-carried
  claim about the inner. **Residual:** verdict partition (which
  non-acceptance is `INVALID` versus `UNVERIFIABLE`) is P4's;
  rejection is non-acceptance (spike idiom).
- **Nesting.** Depth 1 (wrapper over attestation) and depth 2
  (wrapper over wrapper over attestation). "Innermost" has content
  only at depth ≥ 2; depth 2 is therefore the N2 second value on the
  depth axis and is where the timeout risk concentrates. Depth is
  bounded at 2 in the model; the design bounds it by cost, not by
  protocol, and the model claims nothing beyond 2 (the n = 2
  enumeration-does-not-generalize discipline, ENUMERATION §3).
- **Signatures deterministic; `h`, `fp` idealized** — library header;
  every S-P7 ledger entry cites them (S-P3 residuals carried).

## Adversary and modes

A1.3 throughout, with item 3 expressible (library D-4), possession
free (P10), and item 4 in force — replay and *re-framing across the
P7 type boundaries*, which is the capability C1 and C2 are about.

- **Strict** — two authority channels required, one compromised (both
  channel variants run). In strict mode the adversary cannot obtain
  authority for a wrapper key of its own; C2's threat is then confined
  to re-framing honest objects.
- **Degraded** — sole channel, compromised (A3.2 `VALID_DEGRADED`
  never-zero; S-P3 Q2 fixture). Here the adversary holds a wrapper
  identity `idA` with key `kA`, self-signed manifest, and channel
  evidence it minted itself: a fully "authorized" wrapper issuer. This
  is C2's hard case — the adversary is a *legitimate-looking
  wrapper*, and the question is whether wrapping honest bytes under
  its authority lets it claim them, or lets a forged inner artifact
  borrow an honest wrapper's standing. Per S-P3 finding F6, the
  compromised sole channel is the adversary's condition, not
  something the checks defend against; per the 2026-09-05 author
  ruling under F8 (`formal/suite/s-p3/RESULTS.md`, block quote
  following F8), impersonation with the adversary's own key over its
  own bytes in degraded mode is the verifier's cost and is out of
  scope here too.

## The judges (encoding registered here, before any run)

Private-channel judges, spike Q4 pattern; report outputs parallel
with continuations (S-P3 recut 1).

- **Type judge.** Each honest signer reports `(objType, fb)` for every
  framed object it signs. The base verifier reports `fb` on accepting
  an object *as* `OT_ATTEST`; the wrapped-path verifier reports the
  outer `fb` accepted *as* `OT_WRAPPER`. `TypeConfused(otSigned,
  otAccepted, fb)` fires on an honest report and an acceptance of the
  same `fb` with `otSigned ≠ otAccepted`. Registered query:
  unreachable.
- **Scope judge.** Each honest inner issuer reports `(pk(skI), idI,
  fbI)`. The wrapped-path verifier reports `(kIrep, idIrep, fbI)` — the
  key and identity it *attributes to the inner artifact* — on every
  acceptance. `Rescoped(kIrep, idIrep, kH, idH, fbI)` fires on an
  honest report and an acceptance of the same `fbI` with `(kIrep,
  idIrep) ≠ (kH, idH)`. When they are equal the judge instead emits
  `HonestWrappedAccepted(kH, fbI, kW)` — the **N1 witness**, honest
  inner bytes accepted inside a wrapper with the inner attributed to
  its signer (honest-flow, per suite rule; a bare wrapped-acceptance
  witness is satisfiable by the adversary wrapping its own bytes).
  Registered queries: `Rescoped` unreachable; `HonestWrappedAccepted`
  reachable.
- **Inner-signature transplant judge** (added 2026-09-06 after
  skeptic review; the wrapped form of S-P3's `PossessionTransplanted`).
  Each honest inner issuer's report additionally carries the honest
  signature term `sigI` it produced over `fbI`. The wrapped-path
  verifier reports, beside the attributed pair, the inner signature
  term it *presented and verified*. `InnerSigTransplanted(kIrep,
  sigI)` fires on an honest report and a wrapped-path acceptance that
  verified the honest issuer's exact `sigI` term under `kIrep ≠ kH`.
  This judge is keyed on the signature **term**, not on the bytes,
  which is what lets it distinguish the DSKS route (honest `sigI`
  re-verified under a derived key) from the re-sign route (adversary
  signs the public honest bytes under its own key — S-P3 F2 pattern),
  which the bytes-keyed `Rescoped` cannot. Registered query:
  unreachable in the correct models (Q1, Q2, Q5); required red in
  Q6b.
- **Base honest-flow witness.** `HonestAccepted(k, fb)` from a base
  judge as in S-P3 (reachable), so the base verifier is known to
  accept something before it is reused inside the wrapped path.

Deliberate scope of the judges: keyed on exact honest bytes (S-P3's
scope). The scope judge compares the *attributed* pair; it says
nothing about which key signed the wrapper — the wrapper's own
authorship is S-P3's relation applied to the outer object, consumed
not re-proved.

## Query ladder, timeboxes, predictions

Outcome vocabulary is the registered three: **violation**
(counterexample trace), **timeout** (mechanism failure — evidence
about the tool or encoding, never about the property), **termination**
(evidence for the checked abstraction only). Timeboxes are per run;
each channel/mode variant gets the full box.

**S-P7.Q1 — correct model, strict mode, depth 1: sanity and linkage.**
Both channels required, one compromised (both variants). Queries: (i)
`TypeConfused` unreachable; (ii) `Rescoped` unreachable; (iii)
`HonestWrappedAccepted` and `HonestAccepted` reachable; (iv) S-P3's
`Reattributed` judge, transcribed, still unreachable for the inner
object inside the wrapped path (nothing in S-P7 may weaken what S-P3
established); (v) `InnerSigTransplanted` unreachable.
- Timebox: 15 minutes per variant.
- Prediction: all hold, both variants. (p ≈ 0.6; p ≈ 0.25 an encoding
  recut — most likely the two-path verifier sharing one inner-check
  process, or the wrap constructor's pattern in the unwrapping `let`;
  p ≈ 0.15 timeout — the wrapped verifier is roughly twice S-P3's
  Q2 process.)

**S-P7.Q2 — correct model, degraded mode, sole channel compromised,
adversary-held wrapper identity, depth 1: the C2 claim.** Queries:
`Rescoped` unreachable; `TypeConfused` unreachable;
`InnerSigTransplanted` unreachable; `HonestWrappedAccepted` reachable.
- Timebox: 30 minutes.
- Prediction: unreachable, terminating. (p ≈ 0.6; **p ≈ 0.15 a real
  re-scoping surfaces** — the outcome that earns the model its keep:
  it would mean that reading identity from the innermost frame is not
  sufficient when the wrapper's authority is adversary-controlled, an
  amendment trigger for P7/A3.7.1 wording, not a recut; p ≈ 0.25
  timeout.) Q2 carries the ladder's highest genuine uncertainty
  after Q5.

**S-P7.Q3 — broken companion (C1): object-type field unchecked.**
Mutation: the base verifier accepts any `framed(ot, …)` without
`ot = OT_ATTEST`. Fixture: each honest key signs objects of at least
two types (an issuer that both attests and wraps; the second honest
key also signs an `OT_REVIEWREC` object) — N2 on the type axis, and
the reason the companion has something to confuse. Degraded mode.
Required result: `TypeConfused` **reachable** — an honest wrapper
object (or review-recency object) re-framed by the adversary and
accepted as a base attestation.
- Timebox: 15 minutes.
- Prediction: violation found, trace readable, no DSKS needed. (p ≈
  0.75; p ≈ 0.15 the companion cannot go red because some other
  check — most plausibly the manifest-hash or payload shape —
  already discriminates the types, which would be an F3-type finding
  (a redundant field) and a ledger line, not a shrug; p ≈ 0.1
  timeout.) Per the Grok panel criterion: if no type-confusion
  companion can be made to go red at all, the theory does not express
  A1.3 item 4 and that is an amendment trigger.

**S-P7.Q4 — broken companion (C3): non-opaque embedding
(Antigravity's re-serialization).** Mutation: the wrapper commits to
`reserialize(cvOuter, innerBytes)` instead of `innerBytes` — the
nested-JSON embedding, in which the outer canonicalization pass
touches the inner stream. Fixture: **two honest canonicalization
versions** `cvA ≠ cvB` (N2 on the version axis), inner objects
canonical under `cvA`, honest wrappers under `cvB` — **the two-version
run carries only differing pairings** (a matching pairing would let
the honest inner signature verify over the carried bytes and make the
required red impossible by construction; the matching pairing is
supplied by the isolation config below, not by this run — exception
to the global fixture statement, recorded there). Required result:
`HonestWrappedAccepted` **unreachable** — the honest inner signature
no longer verifies over the bytes the wrapper carries; wrapping has
altered the inner verdict. Because this red is an *unreachability*,
it carries the vacuity tell by construction, and so the companion
MUST be run with an **isolation config**: the same mutated model with
`cvOuter = cvInner` (single version), in which `HonestWrappedAccepted`
must be **reachable**. Red in the two-version run *and* green in the
isolation run is the required pattern; red in both is a model defect,
not a finding.
- Timebox: 15 minutes each (two-version, isolation).
- Prediction: red/green as required. (p ≈ 0.6; p ≈ 0.3 the
  `reserialize` destructor needs one encoding recut to fire in
  ProVerif's resolution — it is the only new equational rule in this
  ladder — recorded as a tool finding; p ≈ 0.1 timeout.)

**S-P7.Q5 — correct model, depth 2, degraded mode: "innermost" has
content.** Adversary wrapper `idA` wraps an honest wrapper `idW1` that
wraps an honest attestation `idI1`; also honest `idW2` over the same.
Queries: `Rescoped` unreachable at depth 2 (attributed pair is
`(kI1, idI1)`, never `(kW1, idW1)` and never `(kA, idA)`);
`InnerSigTransplanted` unreachable;
`HonestWrappedAccepted` reachable at depth 2; `TypeConfused`
unreachable (a depth-1 wrapper accepted as a base attestation inside
a depth-2 presentation is the cross-level confusion this fixture can
exhibit). Companion **Q5c**: the verifier attributes the inner
artifact to the frame *one level in* (correct at depth 1, wrong at
depth 2) — red on `Rescoped` at depth 2 only; the same mutation at
depth 1 must stay green (the "inner" ≠ "innermost" distinction is
exactly what the companion isolates).
- Timebox: 45 minutes per model (correct and companion) — the
  largest process in the suite so far.
- Prediction: correct model holds; companion red at depth 2, green at
  depth 1. (p ≈ 0.45; p ≈ 0.2 encoding defect in the recursive unwrap
  — ProVerif has no recursion, so depth 2 is a second hand-written
  verifier path and the two may drift; p ≈ 0.35 timeout, concentrated
  here.)

**S-P7.Q6 — broken companions (C2), degraded mode, depth 1: the
transplant, targeted.** Two mutations, run separately:
- **Q6a — identity from the outermost frame.** The wrapped-path
  verifier checks the inner signature under the inner frame's key
  but reports the *wrapper's* `idW` as the inner artifact's issuance
  identity. Required result: `Rescoped` **reachable** without DSKS —
  the adversary's authorized wrapper `idA` encloses honest bytes and
  the acceptance attributes them to `idA`. Timebox 15 minutes.
  Prediction: red. (p ≈ 0.8; p ≈ 0.1 the mutation needs a recut
  because the judge's tuple comparison does not fire on identity
  alone; p ≈ 0.1 timeout.) The mutation misattributes on *every*
  wrapped acceptance, including the honest `idW1`-over-`idI1` flow,
  so the exhibited trace may be honest-wrapper-only (no adversary
  step); red on `Rescoped` is the requirement, the mechanism
  narrative above is not, and an honest-only trace is not a miss.
- **Q6b — key and authority from the outermost frame.** The
  wrapped-path verifier takes the inner artifact's key from the
  wrapper's manifest and checks the inner signature under it (and,
  necessarily, no longer matches the inner frame's `kfp` against that
  key — otherwise nothing fires, S-P3 Q4's recut risk). Two
  registered reds, one per route, because the bytes-keyed `Rescoped`
  cannot tell the routes apart (skeptic finding, 2026-09-06):
  - `Rescoped` **reachable** — expected trace is the **re-sign
    route, no DSKS**: honest bytes `fbI` are public (library
    `checksign` has message recovery), so the adversary signs
    `(BYTES, fbI)` under its own wrapper key `kA`, which its manifest
    names; the acceptance attributes `fbI` to `(kA, idA)`. This is
    S-P3's F2 pattern in wrapped form and is the *primary* expected
    outcome for this query.
  - `InnerSigTransplanted` **reachable** — the honest issuer's exact
    `sigI` term verified under `pk(dsks(sigI, r))`, a key the
    adversary derives and registers as its wrapper key through the
    compromised channel. This is the wrapped form of S-P3's Q4
    mechanism and is the red that **requires the DSKS capability**;
    it is the registered red for ledger entry 2's "key/authority"
    severing, not `Rescoped`.
  Timebox 15 minutes (one run, both queries). Prediction: both red.
  (p ≈ 0.6 both red as described, the `InnerSigTransplanted`
  derivation passing through `dsks`; p ≈ 0.25 `Rescoped` red but
  `InnerSigTransplanted` not — most plausibly because the mutation
  still pins the key somewhere the draft has not noticed, an
  F3-type "which check is load-bearing" finding and a ledger line; p
  ≈ 0.05 the reverse; p ≈ 0.1 timeout.)

**Ablation rule (on any timeout):** first drop depth 2 (Q5 → Q2
shape); then drop the second wrapper issuer; then drop the unexercised
object-type constants; then drop frame fields from the payload end
toward the binding fields (S-P3's rule). Record the break point; a
timed-out query's ledger entry says "mechanism failure at depth d /
n issuers," never a property claim.

**Ordering rule:** Q1 before Q2; Q2 before Q3, Q4, Q6 (a companion is
evidence only against a matching correct form); Q5 and Q5c last.
Strict-mode channel variants both run for Q1; degraded mode is
single-variant by construction.

## Fixture statement (N2, per query)

Every model carries: **two honest inner issuers** (`idI1`, `idI2`,
own keys and manifests, both manifests honestly published); **two
honest wrapper issuers** (`idW1`, `idW2`, likewise); **adversary-chosen
payloads** (chosen-message issuers, S-P3 convention); **two honest
canonicalization versions** (`cvA`, `cvB`) with at least one honest
inner/outer pairing that differs and one that matches — **exception:
Q4's two-version run carries only differing pairings** (inner `cvA`,
wrapper `cvB`); the matching pairing is supplied by Q4's isolation
config, not by the two-version model, since a matching pairing in that
model would make its required red unreachable by construction; **at
least two
object types signed by the same honest key** (Q3's fixture, carried
into every model so the type judge has content everywhere); **two
nesting depths** (Q5 only: 1 and 2; elsewhere depth 1, with the depth
axis therefore *not* bound by those queries and their headers saying
so). In degraded mode the adversary additionally holds the wrapper
identity `idA` with channel evidence it minted.

## Header text (registered before the model exists; each model's
header is this text narrowed to what its queries discharge)

**Q2 (the claim model):** *This model proves: in degraded mode with
the sole authority channel compromised and the adversary holding an
authorized wrapper identity, a wrapped presentation of an honest
attestation is never accepted with the inner artifact attributed to
any identity or key other than the inner frame's committed
`(issuerId, kfp)` (C2), and no framed object signed as one enumerated
type is accepted as another (C1) — under a perfect fingerprint and
hash, deterministic signatures, at nesting depth 1. Load-bearing for
these queries: the inner frame's `(issuerId, kfp)` read and the
`fp(kI) = kfp` match in the wrapped path (for `Rescoped` and
`InnerSigTransplanted` — the attributed key is pinned to the frame's
`kfp` by `fp` injectivity, S-P3 F5); the `objType` equality in each
verifier (for `TypeConfused`). Carried, not load-bearing: the inner
signature check (both levels) — unexercised by re-scoping for the
same reason S-P3 F5/F7 give for re-attribution, exercised by S-P1's
authorship correspondence and by Q1(iv), consumed from S-P3 entry 1;
outer authority evidence (inert, sole channel key public — S-P3 F6);
outer possession; the canonicalization version fields (bound, checked
only for presence). This model does not prove: that a concrete opaque
embedding is structurally opaque (P8/H1a); anything at depth ≥ 2
(Q5); anything about standing evidence or its transplant
(S-STANDING); the P4 verdict partition; that the three unexercised
object types are distinguishable in bytes (P8 vectors); type
confusion involving the manifest, authority-evidence, or possession
objects, which are distinct library constructors with no object-type
field — unrepresentable here (note 1 item 1 / M5 pattern), byte-level,
P8 vectors; impersonation with the adversary's own key over its own
bytes (reachable, verifier's cost per the 2026-09-05 ruling).*

Q1's header adds the strict-mode fixture and the S-P3 correspondence
carried; Q5's replaces "depth 1" with "depths 1 and 2"; companions'
headers state the mutation and the query they are required to turn
red, and nothing else.

## What S-P7 produces, and for whom (ledger interface, A3.3 fields)

Producer entries this model will supply, each with consumer, shared
term, adversary at the join, and residual:

1. **Type-soundness relation** (producer: Q2/Q1, `TypeConfused`
   unreachable). Consumers: S-P1 (integrity over bytes of *this*
   type), S-P2 (a signature set over a manifest is not a signature
   set over an attestation), the capstone's per-layer linkage (each
   join crosses a typed object). Shared term: `objType` in the frame.
   Severing companion: Q3. Residuals: P8 type-tag bytes; `h`, `fp`
   idealization; deterministic signatures.
2. **Scope relation** (producer: Q2 and Q5, `Rescoped` unreachable).
   Consumer: **S-STANDING** — the entitled-key check inside the
   standing path (note 4 item 2) takes the artifact's `(issuerId,
   kfp)` from this relation, not from any wrapper; and the A3.7.1
   invariant's "issuance identity" is, for a wrapped artifact, the
   innermost frame's. Shared terms: attributed key, attributed
   identity, inner framed bytes. Adversary at the join: A1.3 with
   DSKS, sole channel compromised, adversary-authorized wrapper.
   Severing companions: Q6a (identity, red on `Rescoped`), Q6b
   (key/authority, red on `InnerSigTransplanted` via `dsks`; its
   `Rescoped` red is by the non-DSKS re-sign route), Q5c (depth).
   Residuals: as entry 1, plus depth bounded at 2.
3. **Commitment relation — by construction, not a producer.** No
   query in this ladder states C3; it is encoded by the single
   inner-check process invoked in both paths (Abstractions, "Verifier
   for a wrapped presentation"), and `HonestWrappedAccepted` reachable
   is a witness, not a correspondence. Under PROPERTIES.md / A3.3 a
   ledgered cross-model assumption is discharged only by a
   machine-checked producer query; **S-P1 may not consume this entry
   as discharged**, and it is not offered to S-P1 as a producer. What
   the ladder supplies: Q1/Q2's witness together with Q4's red/green
   control — evidence that the checking arrangement detects
   re-serialization, on the terms S-P3's RESULTS gives for companions
   ("they discharge nothing of the property"). The relying-party
   sentence "wrapping cannot break an honest inner package" rests on
   the by-construction encoding plus this control, and must say so.
   Shared term: inner framed bytes. Residual: opacity of the concrete
   embedding (P8/H1a) — the largest Layer 2 residual in this model and
   the one Antigravity's finding is actually about. If a registered C3
   correspondence is wanted, it must be added before the freeze; none
   is proposed here.

Consumed from elsewhere (assumes-from-elsewhere entries S-P7 will
carry): S-P3 ledger entry 1 (key binding — the wrapper's and the
inner's authorship are each S-P3's relation; S-P7 transcribes the
checks but its queries do not exercise them, F7 discipline) and entry
2 (possession over manifest, both levels). **Cross-formalism joins:
none consumed** under the boundary reading above; if question 1
resolves the other way, the §4 refusal-latch join enters here and is
never marked symbolically discharged.

## Deliberately not registered (recorded so the suite is not later blamed)

- **Cross-form substitution negative control — not registered here
  (proposed struck, `ENUMERATION.md` amendment note 1 item 1; within
  the working scope provisionally ADOPTED by the author 2026-08-29,
  ENUMERATION Question 1, which ratifies nothing in §1–§6;
  ratification pending).** Per note 1 item 1: a `STMT_DIGEST` binding
  read as `STMT_DIRECT` cannot go red in ProVerif because `h(t)` and
  the five-tuple are distinct constructors regardless of tag (guide
  appendix M5) — the companion-that-could-not-fail pattern. It is a
  byte-level control and a **P8 golden-vector obligation**;
  `formal/spike/first-link/DECISION.md`'s routing ("P7/P8", lines
  361 and 913) is left intact with the P8 half now operative. Not
  registered here; not a query; no prediction attaches to it.
- **Standing tests S1–S4 with reason codes** — conformance-vector
  obligations (H1a/P8 track), ENUMERATION §2 and Question 3 (S1–S3);
  S4 (`ISSUANCE_REFUSED`) per note 4 item 1 (criterion 4 stands as
  signed; the *mechanism* model is S-STANDING). Not S-P7 queries.
- **The standing-evidence transplant itself** (A3.9's named companion)
  — S-STANDING, per the 2026-08-29 disposition and note 4. S-P7's
  Q6 is the identity/authority piece only.
- **The integrated adversarial lifecycle model** (A3.9, Kimi-2) —
  separate obligation gating the H1a freeze, not this suite.
- **P7's TLA+ leg** — the "independently-computed verdict" sentence
  as a verdict-partition claim (that a wrapped presentation whose
  inner check fails lands in `INVALID`/`UNVERIFIABLE`, never a valid
  state) is P4-shaped and is not covered by S-P7; recorded as an open
  cell for the claim-level coverage map (Question 2 ruling), not an
  author question.
- **C1 across non-framed kinds — open coverage-map cell.** P7's
  enumeration lists six types; in this model only framed objects
  carry an `OT_*` field. The manifest (`authTuple`), possession proof
  (`POSS`), and authority evidence (`STMT_DIRECT`/`STMT_DIGEST`) are
  distinct library constructors, and a symbolic companion confusing
  one of them with a framed object is green by constructor, not by
  the type tag — the note 1 item 1 / M5 pattern. C1 is therefore
  exercised here among framed kinds only; confusion involving the
  non-framed kinds is byte-level and a **P8 golden-vector
  obligation**. Recorded as an open cell beside the TLA+ leg entry
  above so the Question 2 ruling's "every claim names at least one
  leg" can be checked against it; not an author question.

## What this plan does not claim

- Opacity of any concrete embedding; canonicalization semantics; what
  bytes distinguish the six types — P8/H1a.
- Anything at nesting depth > 2.
- Anything about the three unexercised object types (`OT_MANIFEST`,
  `OT_AUTHEVID`, `OT_CONFVEC`) beyond their declaration.
- Standing, lineage, terminal disposition, or the TLR — S-STANDING.
- Authorship of the wrapper or of the inner object as a *proved*
  relation here — consumed from S-P3.
- Impersonation with the adversary's own key over its own bytes, at
  either level — reachable, out of scope (2026-09-05 ruling under
  S-P3 F8).

## Questions only the author can answer

1. **ROUTED TO AUTHOR — the S-P7 / S-STANDING seam.** Does ENUMERATION
   §2's "standing binds to innermost issuance identity" require S-P7
   to model a standing-evidence object, or only the identity relation
   S-STANDING consumes (this plan's reading)? Under the first reading
   the §4 refusal-latch join enters S-P7 and Q6 becomes the A3.9
   transplant proper; under the second, S-P7 is as drafted. Read
   request, per the standing rule: this file, sections "Target" and
   "Boundary with S-STANDING" (about 60 lines), one question — which
   reading. Nothing else in this file needs a read before the freeze
   beyond the freeze itself.

   > **ADOPTED (author), 2026-09-06** (`formal/suite/ROUTED-2026-09-06.md` A7): the second reading. S-STANDING carries the transplant with a minimal wrapper-shaped outer artifact; S-P7 stays as drafted; the capstone composes both.
2. **ROUTED TO AUTHOR (lighter; can be answered at the freeze
   commit).** Whether library divergence D-5 (object-type constants
   in `tessera_theory.pvl`) may be entered by the collaborator on the
   same terms as D-1–D-4 (collaborator-drafted, PROPOSED, recorded),
   or whether a change to the shared library after S-P3's results
   were entered wants an author signature of its own.

> *Disposition (clerk), 2026-09-06 — settled from the record, not routed; listed for veto in `formal/suite/ROUTED-2026-09-06.md` §B.* Same terms as D-1–D-4 (collaborator-drafted, PROPOSED, recorded), entered as D-6 at model-build time; the library change rides in the author's freeze commit. (B7)

## Review log

- 2026-09-06 — drafted by the AI collaborator from ENUMERATION (all
  notes and dispositions), S-P3's PREDICTIONS and RESULTS (template
  and suite rules), the library, P7/A1.3 as registered, A3 §A3.7 and
  §A3.9, the spike DECISION.md's P7/P8 routing and standing
  conditions, and Antigravity's finding 1. No model written, nothing
  run, no scratch runs. No author read yet.
- 2026-09-06 — skeptic review (same day, pre-freeze; the file is
  uncommitted so these are draft corrections, not divergences). Seven
  defects and three nits applied: Q4's two-version fixture exempted
  from the matching-pairing requirement; the Q2 header's load-bearing
  list corrected to the `kfp` read and `fp` match (the inner signature
  check moved to "carried", per S-P3 F5/F7); Q6b split into a
  non-DSKS `Rescoped` red and a new signature-term-keyed
  `InnerSigTransplanted` red that is the DSKS-requiring one (judge
  added; unreachable registered in Q1/Q2/Q5); ledger entry 3 relabelled
  by-construction, not a producer, S-P1 not a consumer; "STRUCK"
  replaced with the record's own grammar; unexercised-type count
  corrected to three; C1 narrowed to framed kinds with the non-framed
  cell recorded as open; P7 elision marked; S1–S3/S4 citation split;
  Q6a's honest-only trace shape admitted. Still no model, no run, no
  author read.
