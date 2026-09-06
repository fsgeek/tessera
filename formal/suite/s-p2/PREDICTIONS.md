# S-P2 — signature-set completeness (anti-stripping): query plan and registered predictions

**Status: PROPOSED — clerk-drafted by the AI collaborator 2026-09-06;
not adopted; the commit is the author's. Not frozen; no model exists
and nothing has been run.** Per `formal/suite/ENUMERATION.md` §5,
predictions are registered and frozen — by the author's signing commit
— before any S-P2 model is run. The author's cold read of this file
precedes that commit. Post-freeze changes are prediction divergences
(spike rule), never refinements.

Governed by: `ENUMERATION.md` §1–§2, §5 (discipline), §6 (sequencing:
S-P2 after S-P3 and S-P1; this draft is written after S-P3 only, on
the author's read of S-P3 (agreement gate passed 2026-09-05, entered
`dae1c65` together with recut 3, F5–F8, and the "Suite rules from
S-P3"; the F8 ruling entered `a8415eb`, 2026-09-06; the earlier
`71c2887` of 2026-09-04 is the author's acceptance of the
Codex-corrected Q2 record and predates every S-P3 fact this draft
consumes) — whether S-P2 may run before S-P1 is a sequencing
question, see the end of this file); Amendment 1 §A1.3 item 2 (strip, reorder,
duplicate) and P2 as registered there; §A1.2.1 (the waiver lattice:
"accepting a subset of the issue-time signature set (P2)" is a
*waivable* check); A3 §A3.2 item 3 (possession is chain-internal; an
existential self-signature by another key in a multi-key manifest does
not close the chain) and §A3.3 (ledger conservation fields;
three-outcome timebox discipline); `ENUMERATION.md` amendment note 2
(the mandatory degraded-mode signer-stripping companion), note 3 (N1
reachability witness; N2 two honest values per bound axis), note 5
(cross-family falsification as the gate; reading aids as reviewed
testimony); `formal/suite/s-p3/RESULTS.md` "Suite rules from S-P3".
Library: `formal/suite/lib/tessera_theory.pvl` (PROPOSED), D-2
(`authTuple` with a signer-set field), D-3 (possession over the
manifest), D-4 (DSKS expressible).

## Target

P2 as registered (Amendment 1, verbatim):

> The canonical signed bytes commit to the required-signer manifest. A
> package presenting fewer signatures than its manifest requires
> yields `INVALID` — never `VALID_STRICT`, and `VALID_DEGRADED` only
> under an explicit, recorded policy within the waivable set of
> A1.2.1. Consequence: "issued with one signature" and "issued with
> two, one stripped" are distinguishable by construction, because the
> expected set is inside what every signature signs. **[model]**

The required-set grammar this model applies to signers is the
first-link ruling — **ADOPTED 2026-08-13 (author)**,
`formal/spike/first-link/DECISION.md` §"Verifier boundary — the
required-set ruling" — written there for binding-form identifiers and
carried to signers by `ENUMERATION.md` §2's S-P2 entry ("the
DECISION.md required-set grammar, applied to signers"). Its operative
clauses for this model: a signed, nonempty required set; every member
must validate, partial success is not success; a missing, duplicate,
or substituted member makes the artifact `INVALID`; P8 defines the
set's canonical encoding, ordering, uniqueness, and bounds; and
"because the required set is itself signed, removing a member changes
the signed envelope rather than silently weakening it."

S-P2 is the symbolic leg of P2's **[model]** discharge. `PROPERTIES.md`
assigns P2 "TLA+ and ProVerif"; the verdict words in P2's sentence
(`INVALID`, `VALID_STRICT`, `VALID_DEGRADED`) are P4's partition and
stay in the TLA+ leg. In the symbolic leg, as in the spike and S-P3,
**rejection is non-acceptance**; the claim this model carries is:

> *No acceptance of a package for a manifest whose signed required
> set names a signer whose signature over the exact framed bytes the
> package does not carry; and no acceptance under an honest signer's
> key of a manifest that signer never signed.*

The first clause is anti-stripping (A1.3 item 2). The second is the
set-shrinking surface `ENUMERATION.md` note 2 named: the adversary
does not remove a *signature* from the package, it removes a *signer*
from the set around the honest key, so that the stripped package
looks complete. Both are P2's subject; the second is where degraded
mode bites.

## How the signer set is represented (the S-P3 gap, closed here)

S-P3's blind falsification review (`docs/reviews/2026-09-05-blind-
falsification-sp3-q2.md`) found A1.3 item 2 "structurally
unrepresentable: there is one signature per slot, never a set"
(Reviewer 1, line 197), and the S-P3 verifier's `ss` field "bound and
discarded" (Reviewer 2 minor list, line 304). The consolidated
disposition (item 11, both reviewers, lines 139–141) was "Accepted as
S-P2 scope, where the signer set is the subject." This section is
that scope.

- **The required set is `{kfp} ∪ sset`**, read from the map-v1
  authority tuple `authTuple(issuerId, kfp, sset, alg, ver)` (library
  D-2): `kfp` is the first required signer's fingerprint; `sset` is
  the remaining required signers. This follows S-P3 Q5's convention
  (B's fingerprint in the `sset` field) so that S-P3's ledger entries
  and S-P2's share the `authTuple` constructor and its `sset` field.
  S-P2 wraps that field in the `signers0/signers1` family below, so
  the S-P3 Q5 tuple `authTuple(issuerId, fp(pk(skA)), fp(pk(skB)),
  algH, verH)` (`sp3_q5_multikey_correct.pv` line 145) *corresponds
  to*, but is not term-equal to, an S-P2 n = 2 tuple. Consequence: the required
  set is **nonempty by construction** in map v1 — the grammar's
  "empty required set → `INVALID`" case is unrepresentable here and
  is a P8 vector obligation, recorded so it is not later blamed on
  this model.
- **`sset` is a bounded family of transparent constructors**, declared
  model-locally (library terms are not redeclared): `signers0` (no
  additional signer; n = 1) and `signers1(fp)` (one additional signer;
  n = 2), both `[data]`. The bound is **n ≤ 2 required signers**. This
  is not a list: ProVerif processes do not recurse, so the verifier's
  "validate every member" is an unrolled case per arity, one verifier
  branch per set size, in parallel. The adversary chooses which branch
  it feeds.
- **What is representable at this bound.** *Strip*: present one
  signature for a manifest whose set has two — the subject of Q3.
  *Substitute a member*: satisfy a required slot with a key the set
  does not name — Q4 ("forge one," in ENUMERATION §2's words).
  *Duplicate*: present one honest signature in both slots — covered by
  the same slot-fingerprint check as Q4 (the two named fingerprints
  are distinct), so it carries no separate companion; the header must
  say that duplicate and substitute share a load-bearing check.
  *Shrink the set around the honest key* (note 2): Q5.
- **What is not representable, and where it goes.** *Reorder* (A1.3
  item 2's third verb): a set is order-independent, but the model's
  set is positional. Whether a reordered presentation is the same set
  is P8's canonical-ordering obligation (the ruling assigns
  "ordering" to P8); the model assumes canonical order and cannot
  test it. *Bounds and uniqueness* beyond n = 2: P8. These are Layer 2
  here, consumed in the ledger below — the "consumes P8's
  canonical-encoding assumption" line ENUMERATION §2 forecast.
- **"The set is inside what every signature signs"** is realized two
  ways in this design, and the model keeps both because S-P3 F3
  showed they are separately load-bearing across two hardness
  assumptions: (i) each attestation frame carries the manifest hash
  `mh = h(manifest)`, and the manifest carries the set (h idealization,
  library); (ii) each required key's possession proof is its
  self-signature *over the manifest* (D-3), so a manifest naming a set
  that a named key never signed has no valid possession proof under
  that key. Q5's configurations separate them.

## Abstractions this plan fixes (and their residuals)

- **Frame.** `framed(objType, alg, issuerId, kfp, mh, canonVer,
  payload)` under `BYTES` — the S-P3 constructor, declared model-
  locally with the same name, arity, and field order so the ledger's
  shared term is literal. **Residual:** frame layout and encoding are
  P8's. (Whether `framed` should be promoted into the library as a
  recorded divergence D-5, so that S-P1/S-P2/S-P3 share it by
  construction rather than by copy, is routed to the author at the end
  of this file; nothing in this plan depends on the answer.)
- **Each required signer's frame binds its own fingerprint and the
  shared manifest hash** (S-P3 Q5 shape). Consumed from S-P3 ledger
  entry 1 (key-binding relation), not re-proved.
- **Possession** is `sign((POSS, manifest), sk)` for every required
  key (D-3; A3.2 item 3: chain-internal, per key). Fingerprint-only
  possession is a broken companion by definition (library D-3) — it
  is Q5's companion.
- **A package** is the tuple the verifier reads: `(t, evidence, keys,
  possession proofs, signatures, framed bytes)` with one key/proof/
  signature/bytes per slot — the fixed-arity shape S-P3 used, now with
  the arity dictated by the *signed* tuple's `sset` pattern, not by
  what the package presents. That dictation is the load-bearing check
  for Q3, and the check S-P3's verifier omitted.
- **Signatures are deterministic** (library); the judges equate more
  evidence than a byte-level judge; unreachability is conservative
  (guide A2, S-P3 plan). **Rejection is non-acceptance**; verdicts are
  P4's.
- **Fingerprint match is key equality** (library `fp` idealization);
  every ledger entry cites it.

## Adversary and modes

A1.3 throughout: item 2 now representable at n ≤ 2 (above); item 3
expressible (D-4); possession free (P10). Two modes, as in S-P3:

- **Strict** — two authority channels, both required, one compromised
  (both channel variants, per the spike rule that one generic channel
  does not represent both).
- **Degraded** — one authority channel, compromised (sole channel key
  public). S-P3 F6 applies: this fixture is strictly stronger than
  A1.3 item 6 in the conservative direction; the authority-evidence
  check is inert by construction and the header must say so.

Stripping proper (Q3) does not touch the manifest, so channel mode is
not expected to matter to it; it is run in degraded mode because that
is the stronger fixture. Set-shrinking (Q5) is a degraded-mode attack
by nature — in strict mode the uncompromised channel pins the tuple
and the surface is closed before the set is inspected — so Q5 runs in
degraded mode only, which is note 2's fixture exactly.

The relying-party consequence this model is meant to sharpen (guide
"What this means, stated carefully"): under the design's possession
encoding, a sole-channel adversary "can still substitute its own key
… but cannot alter the signer set, algorithm, or version around the
honest key." Impersonation with the adversary's own key over its own
bytes in degraded mode remains reachable, is the registered waiver
cost — **RULED (author), 2026-09-05**, entered under S-P3 F8 in
`formal/suite/s-p3/RESULTS.md` — and is not P2's subject.

## Fixture (N2) and honest-flow witness (N1)

Registered here so that the S-P3 plan omission (RESULTS.md, "N1/N2
… neither was spelled out in the frozen plan") is not repeated.

- **Two honest manifests with different required-set sizes.**
  `M1 = authTuple(issuerId, fp(pk(skA1)), signers0, algH, verH)` —
  one required signer; `M2 = authTuple(issuerId2, fp(pk(skA2)),
  signers1(fp(pk(skB2))), algH, verH)` — two. Both honestly published
  on every channel of the mode. This gives two honest values on the
  set-size axis, the manifest axis, and the issuer-identity axis, and
  three honest signing keys. P2's "issued with one" / "issued with
  two, one stripped" distinction is therefore a *fixture fact* the
  verifier must respect: it must accept M1's single-signature package
  and reject M2's.
- **Every honest signer signs adversary-chosen payloads** (chosen-
  message signers, S-P3 convention). Each honest signer's key is bound
  to exactly one manifest; it signs possession over that manifest
  only.
- **All public keys public; the compromised channel's signing key
  public** in the mode that compromises it. DSKS available (library).
- **N1 witnesses, judge-emitted (S-P3 recut 3 rule — never bare
  acceptance).** `HonestComplete(m, verified)` fires only when an
  acceptance of honest manifest `m` verified exactly the signers `m`
  names, each under its own key — the judge compares the verified
  keys against the fingerprints the set names (encoding in "The
  judges" below); arity agreement alone does not emit it, because
  an arity-only witness is satisfiable by impersonation (the bare
  witness recut 3 replaced). It must be **reachable for M1 and for
  M2 separately** — two registered reachability queries, one per
  set size:

      query k1: pkey; event(HonestComplete(M1, verified1(k1))).
      query k1: pkey, k2: pkey;
        event(HonestComplete(M2, verified2(k1, k2))).

  each expected `not event(…) is false` (reachable), with `M1` and
  `M2` the fixture terms above. A model in which only the n = 1
  witness is reachable has a dead two-signer branch and satisfies Q2
  vacuously; that is a red bar.

## The judges (encoding registered here, before any run)

Private-channel judges, spike Q4 / S-P3 pattern; report outputs in
parallel with their continuations (S-P3 recut 1 rule); locals named
to avoid the library's `issuerId`, `ssetH`, `algH`, `verH`, `fbH`
(recut 3 rule).

- **Honest reports.** A registrar process reports each honest
  manifest `m` once on `honestSetCh`. Each honest signer reports
  `(pk(sk), m)` once on `honestKeyCh` — its key and the one manifest
  it belongs to — and `(pk(sk), fb)` per signed frame on `honestChX`
  as in S-P3.
- **Verifier reports.** On acceptance, the verifier reports `(t,
  verified)` on `setCh`, where `verified` is `verified1(kA)` or
  `verified2(kA, kB)` — the keys it actually verified signatures
  under; and, per slot, `(t, slotFp, kUsed)` on `slotCh` — the
  fingerprint the signed set names for that slot and the key that
  satisfied it.
- **`Stripped(t, verified)`** — SetJudge: honest `m` from
  `honestSetCh`; `(=m, verified)` from `setCh`; if `m`'s `sset` is
  `signers1(_)` and `verified` is `verified1(_)`, fire. Registered
  query: `Stripped` unreachable.
- **`HonestComplete(m, verified)`** — SetJudge, witness arm: emitted
  only when `verified` matches the set `m` names, key by key: for
  `m = authTuple(_, fpA, signers0, _, _)` require `verified =
  verified1(kA)` with `fp(kA) = fpA`; for `m = authTuple(_, fpA,
  signers1(fpB), _, _)` require `verified = verified2(kA, kB)` with
  `fp(kA) = fpA` and `fp(kB) = fpB` (equivalently, key equality
  against the `honestKeyCh` reports; the fingerprint form is chosen
  so the witness cites the same `fp` idealization as the checks it
  witnesses). Arity agreement without the fingerprint match emits
  nothing. Registered queries: the two reachability queries stated
  under "Fixture (N2) and honest-flow witness (N1)".
- **`SignerForged(t, kUsed)`** — MemberJudge: `(kH, m)` from
  `honestKeyCh`; `(=m, =fp(kH), kUsed)` from `slotCh`; if `kUsed ≠
  kH`, fire. "A slot the signed set assigns to an honest signer was
  satisfied by another key." Registered query: unreachable.
- **`SetAltered(kH, m, t)`** — MemberJudge, second arm: `(kH, m)` from
  `honestKeyCh`; `(t, _, =kH)` from `slotCh` with `t ≠ m`; fire.
  "An honest key was accepted as a signer of a manifest it never
  signed" — the set-shrinking event. Registered query: unreachable.

Deliberate scope: the judges are keyed on honest manifests and honest
keys. They say nothing about a manifest the adversary authored under
keys it holds, accepted with all *its* signers present — that is
impersonation, out of scope above.

## Query ladder, timeboxes, predictions

Outcome vocabulary is the registered three: **violation**
(counterexample trace), **timeout** (mechanism failure — evidence about
the tool or encoding, never about the property), **termination**
(evidence for the checked abstraction only). Timeboxes are per run;
each variant gets the full box. S-P3's eight runs each terminated in
≤ 1 s against 15–30 min boxes; the boxes below are kept at that scale
because S-P2's two-branch verifier and two-arity fixture are the
largest processes the suite has yet run, not because a long run is
expected.

**S-P2.Q1 — correct model, strict mode: sanity and linkage.** Both
channels required, one compromised (both variants). Queries:
`Stripped`, `SignerForged`, `SetAltered` unreachable; `HonestComplete`
reachable for M1 and for M2; S-P3's `Reattributed` unreachable
(nothing in S-P2 may weaken S-P3's binding; the judge is carried
verbatim as a consumer check).
- Timebox: 15 minutes per variant.
- Prediction: all hold, both variants. (p ≈ 0.65 termination as
  predicted; p ≈ 0.10 violation — a genuine trace on one of the three
  judges in strict mode, which would mean the uncompromised channel's
  tuple pin is not doing what S-P3 Q1 showed it does, an amendment
  trigger; p ≈ 0.15 termination-after-recut — the most likely defect
  is the two-branch verifier or the arity-typed judge failing to
  reconstruct a trace for the n = 2 witness, the S-P3 recut-1 class,
  classified under termination as S-P3 RESULTS did; p ≈ 0.10
  timeout.)

**S-P2.Q2 — correct model, degraded mode, sole channel compromised:
the P2 claim.** Queries as Q1.
- Timebox: 30 minutes.
- Prediction: all unreachable, witnesses reachable, terminating.
  (p ≈ 0.65; **p ≈ 0.15 a real violation surfaces** — most plausibly
  `SetAltered` via a route this plan has not traced, which would mean
  the design's two set-pins are not sufficient under DSKS with the
  sole channel compromised: an amendment trigger, not a recut;
  p ≈ 0.20 timeout, concentrated here.) Q2 carries the ladder's
  genuine uncertainty.

**S-P2.Q3 — broken companion: verifier ignores the signed set's
cardinality.** Mutation: the verifier binds the tuple's `sset` field
as a variable and never inspects it — the S-P3 Q2 verifier's exact
shape (`let authTuple(id, kfpr, ss, alg, ver) = t in …`, `ss`
discarded) — and accepts a single-signature package for any tuple.
Degraded mode. Required result: `Stripped` **reachable** — M2 (two
required signers) accepted with A2's honest signature alone.
- Timebox: 15 minutes.
- Prediction: violation found, trace readable, no cryptographic step
  in the trace (the package is an honest sub-package; nothing is
  forged). (p ≈ 0.75 violation; p ≈ 0.10 termination-after-recut —
  the judge pairing on `=m` fails to reconstruct, recut-1 class;
  p ≈ 0.10 **termination — companion green, cannot fail** — some
  other retained check blocks the single-signature package for M2
  without inspecting `sset`, the S-P3 F3 pattern; disposition: record
  the miss, locate the blocking check, and add a companion that
  removes it, as S-P3 did; p ≈ 0.05 timeout.) This companion also
  documents that S-P3's verifiers, correct for P3,
  are P2-broken — which is what "each model proves only its
  property" should look like in the record.

**S-P2.Q4 — broken companion: slot not bound to the named
fingerprint.** Mutation: the verifier drops `fp(kB) = kfprB` for the
second slot (keeps the signature check and the frame's own
`=fp(kB)`). Degraded mode. Required result: `SignerForged`
**reachable** — the adversary satisfies B2's slot with a key it holds
over bytes it framed.
- Timebox: 15 minutes.
- Prediction: violation found. (p ≈ 0.75; p ≈ 0.15 the path is
  blocked by another check and needs a recut — the candidate is the
  frame's `=id` conjunct if the adversary must reuse `issuerId2`,
  which it can, so this is judged unlikely; p ≈ 0.10 timeout.) The
  predicted trace is the **adversary's own key over its own frame**:
  `kUsed = pk(skX)` with `skX` adversary-held, over
  `framed(objType, alg, issuerId2, fp(pk(skX)), h(M2), canonVer, p)`
  signed by `skX`. A `dsks`-derived key over B2's *honest* frame is
  **closed** by the check the mutation retains: B2's honest frame
  carries `fp(pk(skB2))`, a derived key `kB'` has `fp(kB') ≠
  fp(pk(skB2))` (`fp` injective, library), so the retained `=fp(kB)`
  pattern fails — S-P3's dependency statement ("the frame's
  fingerprint field alone suffices against re-attribution", F5) seen
  from P2's side. If the trace nevertheless shows a `dsks` step, that
  is a finding about the retained check, recorded as such.
  Prediction about the correct form (Q2): under the S-P3 F5 mutation
  (any key verifies any signature) the S-P2 judges **as encoded
  remain unreachable**, exactly as S-P3's did. `SignerForged` fires
  only on `kUsed ≠ kH`, and a fabricated signature accepted under the
  honest named key has `kUsed = pk(skB2) = kH`; `Stripped` sees a
  matching arity; `SetAltered` sees `t = m`. A fabricated signature
  accepted under the honest named key is an *authorship* failure,
  which S-P3 F7 assigns to S-P1's integrity correspondence, and S-P2
  carries no authorship judge. So Q4's correct form, like S-P3's,
  rests on the `fp` idealization and not on signature
  unforgeability; the header says so below. (The unforgeability
  dependence in this ladder belongs to Q5-C3 — possession over the
  manifest — and to consumed ledger entry 2, where it is cited.)

**S-P2.Q5 — the mandatory companion (ENUMERATION note 2): set-
shrinking around the honest key.** Attack: degraded mode, sole channel
compromised; the adversary crafts `M2' = authTuple(issuerId2,
fp(pk(skA2)), signers0, algH, verH)` — B2 removed — forges channel
evidence for `M2'` with the leaked channel key, and presents A2's
honest possession proof, honest signature, and honest frame through
the n = 1 branch. Registered event: `SetAltered(pk(skA2), M2, M2')`.
Three configurations, each its own model file:

- **Q5-C1 — note 2's companion as literally specified:** possession
  is fingerprint-only, `sign((POSS, fp(pk(sk))), sk)` (the spike's
  encoding, library D-3's named broken form); **the frame is
  unchanged** (carries `mh`). Note 2 requires this to go red.
  - Timebox: 20 minutes.
  - **Prediction: `SetAltered` UNREACHABLE — a companion that cannot
    fail.** (p ≈ 0.65; p ≈ 0.25 reachable as note 2 requires — which
    would mean this plan's trace of the frame check is wrong and is
    itself worth a finding; p ≈ 0.10 timeout.) Reason, traced before
    any run: A2's honest frame carries `mh = h(M2)`; the verifier
    checks `mh = h(t)` against the presented `M2'`; `h` is injective
    (library), so the frame blocks the shrink regardless of the
    possession encoding. Note 2 was drafted 2026-08-27 against the
    spike's opaque-bytes frame (guide M7a's base model), before S-P3
    gave the frame a manifest hash (2026-09-04). This is the S-P3 F3
    redundancy, seen from P2's side. Registering the green prediction
    here, rather than discovering it as a miss, is the reason C2 and
    C3 exist.
- **Q5-C2 — the companion that isolates the encoding note 2
  names:** fingerprint-only possession **and** a frame without the
  manifest hash (`framedNoMh(objType, alg, issuerId, kfp, canonVer,
  payload)`, model-local; the S-P3 F7 unexercised fields retained).
  Required result: `SetAltered` **reachable** — this is guide M7a,
  mechanized in the suite.
  - Timebox: 20 minutes.
  - Prediction: violation found, trace = forge evidence with leaked
    channel key, replay honest possession and signature. (p ≈ 0.70
    violation; p ≈ 0.10 termination-after-recut; p ≈ 0.10
    **termination — companion green, cannot fail** — a retained check
    this plan has not traced (the candidate is the n = 1 branch's
    own slot fingerprint match, which the shrunk `M2'` satisfies, so
    judged unlikely) blocks the shrink even with both set-pins
    removed; disposition: record the miss, locate the check, add a
    companion removing it (S-P3 F3 pattern), and treat guide M7a as
    not reproduced in the suite until that companion is red;
    p ≈ 0.10 timeout.)
- **Q5-C3 — green isolation config (spike pattern):** frame without
  the manifest hash, **possession over the manifest retained**.
  Required result: `SetAltered` **unreachable** — this is guide M7b,
  and the demonstration that possession-over-manifest is individually
  sufficient against set-shrinking, i.e., that note 2's check is
  load-bearing when the frame does not carry the set.
  - Timebox: 20 minutes.
  - Prediction: unreachable, terminating. (p ≈ 0.70; p ≈ 0.15 a
    route through `dsks` this plan did not trace — the adversary
    would need A2's signature over `(POSS, M2')`, which D-4 does not
    grant, so judged unlikely; p ≈ 0.15 timeout.)

The dependency statement Q5 is expected to support, in the S-P3
RESULTS form: *frame-carried manifest hash and possession-over-
manifest are each individually sufficient against set-shrinking and
jointly redundant; the former rests on `h` injectivity, the latter on
signature unforgeability; neither is exercised by stripping proper
(Q3), which rests on verifier logic alone.* If C1 goes red, the
statement is wrong and the finding is the trace. (The unforgeability
clause is C3's — a fabricated possession over `M2'` under A2's key —
and does not extend to Q4, whose correct form rests on `fp`
injectivity alone; see Q4.)

**Ablation rule (on any timeout):** drop the second honest manifest
(M1) first, then the DSKS-independent judge arm (`SetAltered`), then
the strict-mode second channel; re-run; record the break point as
"mechanism failure at …," never as a property claim. The set bound
n ≤ 2 cannot be ablated below the property (n = 1 has no set to
strip); a timeout at n = 2 is a tool finding about this encoding.

**Ordering rule:** Q1 before Q2; Q2 before Q3 and Q4 (a companion is
evidence only against a matching correct form); Q5 last, C1 then C2
then C3. Strict-mode channel variants both run for Q1; degraded mode
is single-variant by construction.

## Header text for the correct model (draft; narrowed after review, per S-P3 recut 3)

> *This model proves:* in degraded mode with the sole authority
> channel compromised, under an adversary that holds every key it
> uses and the DSKS capability, no package is accepted for an honest
> manifest with fewer signatures than that manifest's signed required
> set names, each required slot is satisfied only by the key the set
> names, and no honest key is accepted as a signer of a manifest it
> never signed — for required sets of at most two signers, read from
> the map-v1 tuple. *This model does not prove:* anything about
> required sets larger than two; canonical ordering, uniqueness, or
> bounds of the set encoding (P8); that a stripped package yields
> `INVALID` rather than some other non-valid verdict (P4, cross-
> formalism join); anything about the `VALID_DEGRADED` waiver of a
> signature subset (P4's lattice; see "What this plan does not
> claim"); impersonation by the adversary's own key over its own
> bytes; the verification profile. *Load-bearing checks:* Q3 — the
> verifier's required arity is read from the signed tuple's `sset`
> pattern; Q4 — slot fingerprint match (`fp` idealization; a
> fabricated signature accepted under the honest named key is an
> authorship failure carried to S-P1 per S-P3 F7, not detected here);
> Q5 — manifest hash in the frame (`h` idealization) and possession
> over the manifest (signature unforgeability), each individually.
> *Carried for other properties, not exercised here:* the
> authority-evidence check (inert in degraded mode, S-P3 F6); issuer
> identity, algorithm identifier, object type, canonicalization
> version, domain tags (S-P3 F7's five unexercised fields).

Reading aids owed per note 5 item 2 (typing convention, cast list,
plain-language claim/adversary/boundary): testimony, reviewed by the
lower-ceiling reader probe, not gating exit.

## What S-P2 consumes and produces (ledger interface, A3.3 fields)

**Consumed:**

1. **Key-binding relation** — producer S-P3 Q2 (`Reattributed`
   unreachable), `formal/suite/s-p3/RESULTS.md` ledger entry 1.
   Assumed fact used here: an accepted signature's key is the key the
   frame and tuple fingerprint name, so "the set names signer B" and
   "the signature verified under B's key" refer to one key. Shared
   terms: `framed`, `authTuple`, `fp`. Adversary at the join: A1.3
   with DSKS, sole channel compromised. S-P2 carries S-P3's
   `Reattributed` judge unchanged as the consumer-side check.
   Residual: as S-P3 entry 1 (`fp` and `h` idealizations, frame
   layout, verification profile).
2. **Possession binds the manifest to the named key** — producer
   S-P3 Q2/Q4 correct form (`PossessionTransplanted` unreachable),
   S-P3 ledger entry 2, which names "S-P2's degraded-mode signer-
   stripping companion (note 2)" as its consumer. Q5 is that
   companion. Shared terms: `POSS`, the manifest term. Residual: as
   entry 1, plus signature unforgeability (Dolev–Yao idealization).
3. **P8 canonical encoding of the required set — Layer 2, cross-
   track, never symbolically discharged.** Assumed facts: (a) the
   symbolic set `{kfp} ∪ sset` corresponds to exactly one canonical
   byte encoding, so that two byte-distinct envelopes carrying one
   abstract set (the DECISION.md hazard) are collapsed correctly by
   term equality; (b) reordering a canonically encoded set is not a
   distinct set; (c) uniqueness and bounds. Producer: P8 **[proof]**
   (open, `PROPERTIES.md` row P8). Until P8's proof exists this entry
   cites the assumption; when it exists the entry cites the proof —
   never silently absorbs it (ENUMERATION §2's S-P2 line). Shared
   term: the `sset` constructor family and its encoding. This entry is
   the reason A1.3 item 2's "reorder" has no query here.
4. **`Accept` ↔ P4 verdict partition** — cross-formalism join per the
   author's Question 2 ruling (**RULED, 2026-08-29**, `ENUMERATION.md`
   "Author dispositions"): every path in this model that stops short
   of acceptance on a stripped or substituted set must land in
   `INVALID` in P4's model (a performed-and-failed check), never in a
   valid verdict; the waived-subset case lands in `VALID_DEGRADED`
   only with a recorded policy. Producer: P4's model and fail-closed
   invariants. Shared term: the acceptance predicate. Never marked
   symbolically discharged.

**Produced (offered; entered only in RESULTS.md after the runs):**

1. **Set-completeness relation** — acceptance for manifest `m`
   implies a signature over the exact framed bytes from every signer
   `m`'s signed set names, each under that signer's own key (Q2:
   `Stripped` and `SignerForged` unreachable). Consumers: the capstone
   (A3.2 chain, per signer — "proof of possession by that same key →
   accepted signature verifying under that key → the exact framed
   bytes," quantified over the set, item 3); S-P1 (integrity over
   bytes presupposes which signatures are required over them);
   S-P7 (a wrapper's inner attestation's completeness is per layer,
   A3.2 item 4). Shared terms: `authTuple`'s `sset`, `framed`,
   accepted keys. Severing companion: Q3 for the cardinality half, Q4
   for the membership half.
2. **Set integrity around an honest key** — no honest key is accepted
   as a signer of a manifest it never signed (Q2: `SetAltered`
   unreachable). Consumer: the relying-party story's degraded-mode
   cost statement (note 2, last bullet: "tampering with the honest
   key's parameters does not" survive). Severing companion: Q5-C2.

Severing companions for the discharge matrix (ENUMERATION §3): Q3
severs produced entry 1's cardinality half; Q4 its membership half;
Q5-C2 entry 2. The matrix itself is written only once the models
exist.

## What this plan does not claim

- **The `VALID_DEGRADED` waiver of a signature subset** (A1.2.1
  waivable item; P2's second clause). Deliberately not modeled in the
  symbolic leg, for a reason stated so the author can overrule it:
  the only symbolic content of a correct waiver verifier — that the
  required set it reports against is read from the *signed* manifest,
  so the waived members are named and "issued with one" is never
  confused with "issued with two, one waived" — is exactly Q3's
  load-bearing check; a waiver companion would be Q3 with a
  different report. The rest of the clause (that a policy is
  explicit, recorded, within the lattice, and produces
  `VALID_DEGRADED` rather than `VALID_STRICT`) is P4's verdict
  partition, consumed as ledger entry 4. Under the author's Question
  2 ruling narrowing is acceptable "so long as at least one leg
  covers every claim". What P4's leg carries, from the tree:
  `formal/tla/P4_VerifierStates.tla` models checks abstractly
  (`CONSTANTS Checks, NonWaivable`, line 25) with no P2-specific
  check, and `DegradedNeedsExplicitWaiver` (lines 100–103) carries
  the recorded-waiver clause generically for every waivable check —
  so P4's leg covers "`VALID_DEGRADED` only under an explicit waiver
  within the waivable set" for the abstract check set, not for a
  named signature-subset check. Whether that generic coverage is
  accepted as covering P2's clause is **routed to the author**
  (below).
- Required sets of more than two signers; canonical ordering,
  uniqueness, bounds (P8, ledger entry 3).
- The frame's byte layout, or that `framed(...)` is the P8 frame.
- Impersonation with the adversary's own key over its own bytes in
  degraded mode (reachable; the registered waiver cost).
- Anything the DSKS capability is *practical* against; the library
  grants it because A1.3 registers it.
- The verification profile (P3's [assumption] half, H1a).
- That the empty-set and malformed-member cases of the required-set
  grammar are rejected: unrepresentable in map v1 and in the symbolic
  algebra respectively; P8 vector obligations.

## Exit gate for the model (not for this file)

Per ENUMERATION note 5 item 1: the S-P2 correct model's queries are
accepted when they survive falsification review by at least one
reviewer from a different model family than the model's author, cross-
family first. The blind reverse translation against P2's registered
sentence is the comparator. The author's cold read of the corrected
header against P2's sentence is the agreement gate, on the S-P3
pattern (2026-09-05 read, recorded in S-P3 RESULTS.md).

## Questions routed to the author (none block freezing this file; each is answerable by ruling without rework)

1. **Note 2's companion as literally specified is predicted green
   (Q5-C1).** Is the note's requirement satisfied by Q5-C2 — the same
   encoding fault with the frame's redundant set-pin removed — with C1
   recorded as the redundancy finding? Or does the author want note 2
   amended to name C2's configuration, or the frame changed for S-P2?
   This plan registers C1, C2, and C3 so that any answer leaves the
   predictions intact.

> *Disposition (clerk), 2026-09-06 — settled from the record, not routed; listed for veto in `formal/suite/ROUTED-2026-09-06.md` §B.* Satisfied by Q5-C2, with C1 recorded as the redundancy finding; note 2 is a clerk note and its text is sharpened by amendment note 6, not by the author. (B4)
2. **Waiver-mode narrowing.** Confirmation that S-P2's symbolic leg
   may leave the `VALID_DEGRADED` recorded-waiver clause of P2 to
   P4's leg (ledger entry 4), on the Question 2 precedent. P4's
   `DegradedNeedsExplicitWaiver` carries the clause generically over
   an abstract check set (see "What this plan does not claim"); the
   question is whether that generic invariant is accepted as covering
   P2's recorded-waiver clause, or whether a named signature-subset
   check must be instantiated in P4's model.

> *Disposition (clerk), 2026-09-06 — settled from the record, not routed; listed for veto in `formal/suite/ROUTED-2026-09-06.md` §B.* The symbolic leg narrows on the Question 2 precedent. P4's generic `DegradedNeedsExplicitWaiver` covers the *explicit-policy* half; the *recorded* half is an H1a artifact (the 2026-09-06 TLA+ review found recording absent from P4's model, disposition: boundary) and is an open cell in `formal/COVERAGE-MAP.md`, not a ruling. (B5)
3. **Sequencing.** ENUMERATION §6 orders S-P1 before S-P2. This draft
   exists because S-P3's record was accepted first and S-P2 is S-P3's
   named consumer; nothing here consumes S-P1. Whether S-P2 may run
   before S-P1 is the author's to say.

> *Disposition (clerk), 2026-09-06 — settled from the record, not routed; listed for veto in `formal/suite/ROUTED-2026-09-06.md` §B.* Permitted: nothing here consumes S-P1, §6 was clerk sequencing, and both are built in parallel. (B6)
4. **`framed` into the library.** Whether the seven-field frame
   constructor should be added to `tessera_theory.pvl` as a recorded
   divergence (D-5) so that S-P1/S-P2/S-P3 share it by construction.
   Library changes are the author's to sign; this plan copies the
   constructor verbatim either way.

> *Disposition (clerk), 2026-09-06 — settled from the record, not routed; listed for veto in `formal/suite/ROUTED-2026-09-06.md` §B.* Entered as recorded divergence D-5 on D-1–D-4's terms at model-build time; S-P3's committed runs are not touched. (B7)

## Review log

- 2026-09-06 — clerk-drafted by the AI collaborator from
  `ENUMERATION.md` (all notes and dispositions), the S-P3 plan and
  results, the library, P1–P10 and A1.3 texts, A1.2.1, A3.2, the
  first-link required-set ruling, and the guide's M7a/M7b section.
  No S-P2 model has been written or run; no scratch run was made. The
  Q5-C1 green prediction is a paper trace against the S-P3 verifier
  shape, not a tool result.
- 2026-09-06 — skeptic review (AI, same day, pre-freeze) returned two
  blocking and four defect findings plus three nits; all applied in
  place, the file being an unfrozen draft. Blocking: (1) the Q4
  correct-form claim that `SignerForged` depends on signature
  unforgeability contradicted the judge's own `kUsed ≠ kH` condition
  — withdrawn; Q4 now rests on the `fp` idealization and the
  authorship case is routed to S-P1 per S-P3 F7; (2) `HonestComplete`
  was emitted on arity match alone, a bare-acceptance witness in
  recut 3's sense — now emitted only on key-by-key fingerprint match,
  with both reachability queries stated in ProVerif form. Defects:
  the commit pin (`71c2887` → `dae1c65`/`a8415eb`); the Q4 `dsks`
  route (closed by the retained frame `=fp(kB)`); missing outcome
  buckets on Q1 (violation) and Q3/Q5-C2 (companion green); the
  header's carried-field list (algorithm identifier added). Nits:
  tuple-term wording, review citations, the P4 fact and routed
  question 2. No prediction was changed except by adding buckets and
  redistributing probability within a query.
