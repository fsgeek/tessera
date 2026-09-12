# S-STANDING — the terminal lineage record under A1.3: query plan and registered predictions

**Status: PROPOSED — clerk-drafted by the AI collaborator 2026-09-06;
not adopted; the commit is the author's. Not frozen; no model exists
and nothing has been run.** Per `formal/suite/ENUMERATION.md` §5,
predictions are registered and frozen — by the author's signing
commit — before any S-STANDING model is run. The author's cold read
of this file precedes that commit. Post-freeze changes are prediction
divergences (spike rule), never refinements. Amend-don't-rewrite
applies from the first commit.

Governed by: `ENUMERATION.md` §2 fifth slot (author dispositions,
2026-08-29, consequences paragraph) and amendment note 4 (2026-09-04);
§5 discipline with note 3 (N1 reachability witness; two honest values
per bound axis) and note 5 (cross-family falsification as the gate;
reading aids as reviewed testimony); the S-P3 suite rules carried in
`formal/suite/s-p3/RESULTS.md` (judge report outputs parallel with
continuations; N1 witness is honest-flow acceptance emitted by the
judge; judge locals never shadow library names; the header names which
checks are load-bearing). Construction: the terminal lineage record —
**ADOPTED (author, 2026-08-31; entered 2026-09-04)**,
`formal/spike/standing-probe/DECISION.md` sub-ruling 5 — as amended by
SC-1 (anchored TLR; `DECISION-CRITERIA.md` §1 dated amendment), SC-2
(one signing act; `DECISION.md` R2), SC-3 (S4 row and two outcomes;
`formal/spike/first-link/DECISION.md` exit condition 3, dated
amendment 2026-09-04), and the blind re-scoring's conformance note
(`docs/reviews/2026-08-31-blind-standing-scoring.md`, carried as
ENUMERATION note 4 item 2). Library:
`formal/suite/lib/tessera_theory.pvl` (PROPOSED); this model adds
only its own process structure, events, and queries and redeclares
nothing.

Criterion 4's first condition (author selection of the construction)
is satisfied by the entered decision (ENUMERATION note 4); this file
plans the model its second condition requires (a model in this suite
under the A1.3 adversary, before Band 0 exit). Nothing here discharges
anything.

## Target

The A3.7.1 invariant as registered (`docs/phase-0-prereg-amendment-3.md`
§A3.7 item 1, verbatim):

> Cryptographic validity alone confers no protocol standing. Any
> artifact claiming standing must present verifiable standing
> evidence binding its issuance identity, attempt lineage, and
> terminal disposition. Missing standing evidence leaves the artifact
> evidentially admissible but without protocol standing.

with the registered reporting form (same section): standing is an
orthogonal assessment dimension, never a fifth P4 state; the base
result reports at least `ESTABLISHED`, `ABSENT`, or `UNVERIFIABLE`
with reasons, alongside the unchanged P4 verdict; standing is reported,
never waived.

The construction, in the terms the record fixed (`DECISION-CRITERIA.md`
§1 TLR sketch, as amended; `RESULTS-PROBE.md` "What the TLR had to
be"): an issuer-signed object created at terminal disposition,
carrying issuance identity — **a digest of the artifact's signed core,
computed by the verifier** (G1) — the attempt lineage (attempt
identities with per-attempt dispositions), and the terminal disposition
(`SHIPPED <attempt>` or `REFUSED`); signed by the **entitled key**, the
key the evidenced authority tuple names; carried in the bundle;
anchored (SC-1), the anchor proof travelling beside it.

**The operative sentence this model tests.** A standing report of
`ESTABLISHED` for an artifact, computed against an entitled key `kH`,
implies that the issuer holding `kH` signed one terminal lineage record
whose lineage contains that artifact's *derived* identity and whose
terminal disposition designates that identity as shipped — the three
bindings of A3.7.1 under one signature (G0 story) — and no
`ESTABLISHED` report is computed against a key other than the one the
evidenced authority tuple names (note 4 item 2).

## What is symbolic here and what this model only records

ENUMERATION §2 (standing tests S1–S3 are conformance-vector
obligations, H1a/P8 artifacts) and note 4 (the model "must
additionally cover" SC-3's outcomes and S4) are read together as
follows. Each item note 4 names is assigned to exactly one of:
**symbolic query** (a ProVerif query in this model, with a prediction),
**carried check** (present in the verifier so the cast list and a
falsification reviewer can see it, predicted inert against the A1.3
adversary, not a query), **vector obligation** (H1a/P8 S-series
artifact; this file records the obligation and the reason it is not a
symbolic query), or **cross-formalism join** (A3.3 ledger entry whose
producer is a TLA+ model; never marked symbolically discharged,
ENUMERATION §4).

| Item (note 4) | Assignment | Where in this plan |
|---|---|---|
| A3.7.1 invariant (identity, lineage, disposition bound under the entitled key) | **symbolic query** | Q1(i)/(ii), companions Q2 and Q4 |
| Kimi-2 transplant (standing evidence moved from a valid inner artifact onto a forged outer one → red) | **symbolic companion** | Q2 |
| Entitled-key check *inside* the standing path; companion establishing it only via the envelope → must fail | **symbolic query + companion** | Q1(iii), Q3 |
| S4 row, `ISSUANCE_REFUSED` (refused-lineage holder presented with lineage → no standing) | **symbolic witness + covered by Q1(i)**; companion Q4 | Q1(iv), Q4 |
| `STANDING_EVIDENCE_MALFORMED` (probe F1, mandatory red vector) | **vector obligation**; well-formedness is a **carried check** | §"Carried checks", §"Vector obligations" |
| `STANDING_EVIDENCE_TEMPORAL_MISMATCH` (A2.1 predicate on the TLR's own anchor, SC-1) | **cross-formalism join** + **vector obligation**; anchor-digest binding is a **carried check** | §"Carried checks", §"Ledger interface" entry C-2 |
| Pairwise-distinct reason codes across S2/S3/S4; companion collapsing any pair → red | **vector obligation** (§2 followed over note 4 item 1 — routed item 5); the five report witnesses are **vocabulary-liveness witnesses** (not N1) that make the codes visible | Q1(iv), §"Vector obligations", routed item 5 |

The reasons for each non-symbolic assignment are given in their
sections; the short form is that each of those checks either fails only
by construction of constants (reason-code collapse) or defends against
an *honest-but-defective issuer*, which the A1.3 adversary is not
(malformed TLR), or states an arithmetic fact ProVerif cannot express
(temporal predicate). A symbolic companion for any of them would be a
companion that cannot fail for reasons unrelated to the property —
the pattern ENUMERATION note 1 item 1 struck from S-P7 and S-P3 F3 met
again. Recording them as vector obligations is the honest disposition;
the vectors themselves are not written here.

## Abstractions this plan fixes (and their residuals)

- **Attempt = signed core; identity is derived.** An attempt's core is
  a transparent constructor over the fields the probe's fixture signed
  and hashed — the evidenced tuple, the possession proof, the framed
  bytes' signature, and a declared time — `attemptCore(t, ppf, sg,
  decl)`; its identity is `h(attemptCore(...))`, recomputed by the
  verifier from the fields it holds, never read from a presented label.
  Each attempt's `decl` is a fresh name (A2.4: re-declaration on
  re-issue moves the declared time forward, so honest attempts in one
  lineage never share a core). **Residuals:** which bytes constitute
  "the signed core" and their canonical encoding are P8's (injectivity
  over the accepted domain); `h`'s idealization (library header) —
  **the correct model's transplant resistance rests entirely on `h`
  being injective**, stated now so no reader mistakes it for a
  signature result (the S-P3 F5 lesson, applied in advance).
- **Lineage has exactly two entries.** `lineage2(entry(aid1, d1),
  entry(aid2, d2))`; per-entry dispositions drawn from
  `{DISP_ABANDONED, DISP_SHIPPED}`; terminal is `TERM_SHIPPED(aid)` or
  `TERM_REFUSED` (named distinctly from the per-entry constants:
  ProVerif cannot declare a nullary constant and a unary constructor
  under one name, and the well-formedness check below needs both; the
  record's `SHIPPED <attempt>` / `REFUSED` are these). Two entries is
  the smallest structure in which "superseded" (S2) and "shipped" (S1)
  coexist and in which a refused lineage has more than one abandoned
  attempt (A2.3's bounded retry). **Residual:** nothing is claimed for
  lineages of other lengths; n = 2 does not generalize (author finding
  7 wording, ENUMERATION §3).
- **The TLR** is `sign((TLR, tlrBody), skI)` with `tlrBody =
  (lineage, terminal, declTerminal)`, under a model-local
  domain-separation constant `TLR`. The library has no such tag; see
  the routed question on P7's enumeration and the library
  (§"Routed to the author"). A TLR under any other tag or key is not a
  TLR.
- **Entitled key** = the key whose fingerprint the *evidenced*
  authority tuple names: `authTuple(id, kfpr, ss, alg, ver)` with
  `fp(kX) = kfpr`, the tuple evidenced under the mode's channel rule
  (below). The standing path evaluates this itself; it does not inherit
  it from the envelope path (note 4 item 2). Consumes S-P3 ledger entry
  1 (key-binding relation) for the meaning of "the key that signed the
  artifact's bytes"; S-STANDING does not re-prove it.
- **Standing report** is a model-local event carrying `(verdict,
  reason, kX, t, aid)` with verdicts `ESTABLISHED | ABSENT |
  UNVERIFIABLE` and the registered reason codes — S1–S4's
  (`TERMINAL_DISPOSITION_SHOWN`, `SUPERSEDED`,
  `NO_TERMINAL_DISPOSITION_EVIDENCE`, `ISSUANCE_REFUSED`; first-link
  `DECISION.md` exit condition 3 table and the SC-3 amendment) and
  SC-3's two additions (`STANDING_EVIDENCE_MALFORMED`,
  `STANDING_EVIDENCE_TEMPORAL_MISMATCH`) — plus the two probe-recorded
  codes `STANDING_EVIDENCE_MISMATCH` and
  `STANDING_EVIDENCE_SIGNATURE_INVALID` (standing-probe `DECISION.md`
  R3 "Distinct defined outcomes observed"; `RESULTS-PROBE.md` "What the
  TLR had to be" item 4), which no amendment registers and which are
  carried so the vocabulary is complete.
  It is never a P4 state; the envelope path is a separate process on
  the same bundle input, run in parallel — **the orthogonality of
  A3.7.1 is structural in the model**, which is what makes Q3's
  companion able to fail (below).
- **Anchoring is a public oracle.** A1.3 item 5: the adversary anchors
  anything; anchoring proves existence at a time, not authority. The
  TLR's anchor proof is an adversary-buildable term over `h(TLR)`; the
  verifier checks that the proof presented is over the TLR presented.
  Time is not represented. **Residual:** the whole temporal content of
  SC-1 (the A2.1 predicate against `declTerminal`) is a cross-formalism
  join (ledger C-2).
- **Signatures deterministic; rejection is non-acceptance; P4's
  verdict partition is P4's** — spike idioms, unchanged.
- **The forged "outer" artifact is any adversary-built artifact.** The
  A3.9 companion names a *wrapper* transplanting standing evidence from
  a valid inner artifact onto a forged outer one. This model realizes
  "outer" as an artifact whose derived identity differs from the
  inner's, which every adversary-built artifact does; it does **not**
  model P7 wrapper types, byte embedding, or which identity a wrapped
  bundle's standing report is computed against. ENUMERATION §2 assigns
  "standing binds to innermost issuance identity; a wrapper cannot
  re-scope it" to S-P7; the join is ledger entry C-4. Whether the
  companion must exhibit the wrapper shape literally is routed
  (§"Routed to the author").

## Adversary and modes

A1.3 throughout: alters, strips, replays, re-frames; crafts manifests,
artifacts, TLR-shaped objects and bundles freely; anchors anything;
substitutes keys with item 3 expressible (library D-4); possession is
free; controls a proper subset of authority channels (item 6).

- **Strict — primary fixture.** Two authority channels, both required
  for the entitled-key determination; **one compromised**, both
  variants run (a generic single channel is not accepted as
  representing both — spike rule). This is the registered adversary
  exactly; S-P3 F6 records that the sole-channel-compromised fixture is
  *stronger* than A1.3 item 6.
- **Degraded — one variant, Q1 only.** Sole channel, compromised. Here
  the adversary can install its own key as entitled (the first-link
  spike's Q5b waiver cost, `formal/spike/first-link/RESULTS.md`, cited
  in S-P3 RESULTS F8). The dated ruling in S-P3 RESULTS F8 (RULED,
  author, 2026-09-05) reads: fresh-signature impersonation under a
  usurped identity, with the sole channel compromised, "is the
  degraded-mode cost handed to the verifier, not a P3 defect", and its
  operative sentence is "P3's threat is re-attribution of an existing
  signature". Reading that ruling as covering the standing
  correspondence in degraded mode is the clerk's; the author's stated
  reason is general (degraded service hands evidence to the verifier)
  but the ruling's sentence is scoped to P3. Routed (item 4). Run so
  the record shows, in one model, which of S-STANDING's claims survive
  that cost and which do not.

## Fixture (N2, note 3: two honest values on every axis a query binds)

- **Two honest issuers**, `skH1`, `skH2` (declared as private free
  names so queries can name their public keys), each with its own
  authority tuple, both tuples honestly published on both channels
  (strict) / the sole channel (degraded).
- **Two lineage shapes per issuer, replicated:** `ShipIssuer` — attempt
  `a1` (abandoned), attempt `a2` (shipped), TLR terminal
  `TERM_SHIPPED(aid2)`; `RefuseIssuer` — `a1`, `a2` both abandoned, TLR
  terminal `TERM_REFUSED`. Payloads are adversary-chosen (chosen-message
  issuers, S-P3 idiom); declared times fresh.
- **Both attempts' artifacts are public** before the TLR exists
  (A2.0's premise: the abandoned artifact is a cryptographically valid
  object somebody can hold); the TLR is published at terminal
  disposition.
- **Axes bound by queries and their honest values:** keys (2),
  tuples (2), attempt identities (≥ 4 honest, 2 per lineage instance),
  terminal dispositions (2), lineage membership (member / non-member),
  reason codes (5 witnessed: four honest-flow, one transplant-rejection).

## The judge and the correspondence (encoding registered before any run)

Two encodings, one per claim, both in the spike's private-channel
judge idiom with the S-P3 recut-1 rule (report outputs in parallel
with continuations) and recut-3 rule (N1 witness is honest-flow,
emitted by the judge):

1. **The invariant, as a correspondence.** The honest issuer, at
   terminal disposition and *before* releasing the TLR, fires
   `Designated(pk(skI), aid)` for the shipped identity (nothing for a
   refused lineage). The standing path fires `Established(kX, t, aid)`
   on an `ESTABLISHED` report. Queries:
   - (i) **unrestricted:** `event(Established(kX, t, aid)) ==>
     event(Designated(kX, aid))`;
   - (ii) **per honest key:** the same with `kX` fixed to `pk(skH1)`
     and to `pk(skH2)`.
   (i) is the A3.7.1 sentence for *every* accepted standing claim; (ii)
   is the sentence for the honest issuers. In strict mode both are
   predicted to hold; in degraded mode (i) is predicted to **fail** —
   the adversary's own key, installed through the sole channel, with
   its own TLR over its own artifacts — and that failure is the
   registered cost, not a finding (on the scope of the ruling this
   rests on, see routed item 4). Stating (i) and (ii) separately is
   what lets the record say so mechanically instead of in prose.
2. **The entitled-key judge.** The standing path reports
   `(kX, t, aid)` on `ESTABLISHED` over a private channel; the judge
   destructures `t = authTuple(id, kfpr, ss, alg, ver)` and fires
   `StandingUnentitled(kX, t)` if `fp(kX) <> kfpr`, else — when a
   matching honest designation `(kX, aid)` has been reported on the
   issuer's private channel — `HonestStandingEstablished(kX, aid)`, the
   N1 witness.

Vocabulary-liveness witnesses (**not N1**; reachability only; may be
satisfied by adversary flows in degraded mode — the `(ESTABLISHED,
TERMINAL_DISPOSITION_SHOWN)` witness in Q1d is satisfiable by the
adversary's own installed key and TLR, which is exactly why the N1
witness is the judge-emitted `HonestStandingEstablished` above and not
any of these): the standing path's report event with `(ABSENT,
SUPERSEDED)`, `(ABSENT, NO_TERMINAL_DISPOSITION_EVIDENCE)`, `(ABSENT,
ISSUANCE_REFUSED)`, and `(ESTABLISHED, TERMINAL_DISPOSITION_SHOWN)`
each reachable — the S1–S4 rows exhibited in the model's own
vocabulary — and a fifth, `(ABSENT, STANDING_EVIDENCE_MISMATCH)` for an
adversary-built artifact presented with an honest TLR: the correct-side
polarity of G1's transplant test (`DECISION-CRITERIA.md` §2 G1: the
correct verifier "must report standing `ABSENT` with a mismatch reason
(the transplant is *rejected*)"), which the probe's Q3 witnessed and
which Q1's correspondence alone does not exhibit. They witness that the
verifier's paths are live; they are not the discrimination check
(§"Vector obligations").

Judge locals are named so as not to shadow library names (`fbH`,
`issuerId`, `ssetH`, `algH`, `verH`).

## Query ladder, timeboxes, predictions

Outcome vocabulary is the registered three: **violation**
(counterexample trace), **timeout** (mechanism failure — evidence
about the tool or encoding, never about the property), **termination**
(evidence for the checked abstraction only). Timeboxes are per run;
each channel/mode variant gets the full box. Calibration: every S-P3
run terminated in ≤ 1 s against 15–30 min boxes; this model's term
space is larger (two-entry lineages under `h`, two lineage shapes per
issuer, a correspondence rather than a reachability), so boxes are kept
at the S-P3 ceiling and the timeout mass is placed higher than S-P3's.

**SS.Q1 — correct model, strict mode, one channel compromised (both
variants).**
Queries: (i) unrestricted correspondence holds; (ii) per-honest-key
correspondences hold; (iii) `StandingUnentitled` unreachable;
(iv) N1: `HonestStandingEstablished` reachable, and the five
vocabulary-liveness report witnesses reachable, including `(ABSENT,
ISSUANCE_REFUSED)` for an artifact of a refused lineage presented with
its TLR (**the S4 row**) and `(ABSENT, STANDING_EVIDENCE_MISMATCH)` for
an adversary-built artifact presented with an honest TLR (G1's
correct-side polarity).
- Timebox: 30 minutes per variant.
- Prediction: all hold, both variants. (p ≈ 0.5 as-registered on the
  first complete run; the registered "violation" outcome splits into
  two sub-buckets — **p ≈ 0.25 an encoding recut** — most likely the
  lineage lookup pattern (`let entry(=aid, d) = ...` over a two-entry
  structure needs a case split), or a report witness "cannot be
  proved" of the S-P3 recut-1 kind if any report output is
  sequential; disposition by trace/derivation inspection, recorded as
  encoding, never as property — and a **real** violation of (i)/(ii)
  in strict mode — standing established for an identity nobody
  designated, under an honest key, with the adversary holding no
  honest key — which would mean the TLR as adopted does not bind what
  A3.7.1 says (p ≈ 0.05; an amendment trigger on the construction
  decision, not a recut); p ≈ 0.2 timeout, concentrated on the
  correspondence. Sums to 1.0.)

**SS.Q1d — correct model, degraded mode, sole channel compromised.**
Same queries.
- Timebox: 30 minutes.
- Prediction: (i) **fails, by an adversary-key trace** (p ≈ 0.7) —
  this is the registered degraded-mode cost (routed item 4 on the
  ruling's scope) and is predicted so the record carries it as a
  checked fact; (ii), (iii) hold; (iv)
  reachable. (p ≈ 0.15 that (i) unexpectedly holds — which would mean
  the model's adversary cannot install a key through the sole channel,
  an under-modeling of A1.3 to be repaired, not a result; p ≈ 0.15
  timeout.) Ordering: after Q1; not a gate for the companions.

**SS.Q2 — companion A: the Kimi-2 transplant (identity declared, not
derived).** Mutation: the TLR names attempts by a *label* carried in
the lineage (the probe's ordinal binding), and the standing path reads
the artifact's claimed label from the bundle instead of computing
`h(attemptCore(...))`. Strict mode, one channel compromised, **DNS
compromised** variant, matching Q1's DNS-compromised correct-form run
(the channel is not the load-bearing element here, so the second
variant is not run; if a reviewer wants both, both run in the same
box each).
Required result: correspondence (i) and (ii) **violated** — the
exhibited trace moves the honest TLR from the shipped attempt's bundle
onto an adversary-built artifact carrying the shipped attempt's label,
and the verifier reports `ESTABLISHED` for an identity the issuer never
designated. `StandingUnentitled` stays unreachable (the key is the
honest one throughout).
- Timebox: 15 minutes.
- Prediction: violation found, trace readable. (p ≈ 0.75; p ≈ 0.15
  recut — the label needs to be an adversary-writable bundle field for
  ProVerif to find the trace; p ≈ 0.1 timeout.) Grok panel criterion
  carried: if no companion can be made to go red, the theory does not
  express the threat — amendment trigger, not a shrug.

**SS.Q3 — companion B: entitled key established only via the
envelope.** Mutation: the standing path checks that the TLR's signing
key equals the key the *artifact* presents (`tlr.pub = core.pub`, the
probe fixture's shape) and verifies the TLR signature, but does not
compare that key's fingerprint against the evidenced tuple; the
envelope path keeps its `fp(kX) = kfpr` check. Strict mode, one
channel compromised, **DNS compromised** variant, matching Q1's
DNS-compromised correct-form run. Required result: `StandingUnentitled`
**reachable** — an adversary-built artifact under the adversary's own
key, with a TLR under that key, presented with an honest evidenced
tuple: the envelope path stops at `KEY_FINGERPRINT_MISMATCH` and the
standing path reports `ESTABLISHED` against an unentitled key.
Correspondence (i) is predicted **violated** by the same adversary-key
trace shape as Q1d (`Established` under `kA`, no `Designated` under
`kA` — (i) is unrestricted, and `Designated` is fired only by honest
issuers); (ii) stays **true** (no honest key is involved). What
distinguishes Q3's red from Q1d's is `StandingUnentitled`: here the
evidenced tuple is honest and the key is not entitled, so the judge
fires; in Q1d the tuple itself is the adversary's own and the judge
stays silent. (i)'s violation is therefore not Q3's discriminating
result; the judge is.
- Timebox: 15 minutes.
- Prediction: violation found. (p ≈ 0.7; **p ≈ 0.2 the companion
  cannot fail** because the model's verifier sequentializes the
  envelope path before the standing path so the envelope's fingerprint
  check shadows the missing one — that would be an encoding defect
  against the registered orthogonality abstraction, recut by putting
  the two paths in parallel, and worth a ledger line because it is
  exactly the conformance defect the blind re-scoring found in the
  probe; p ≈ 0.1 timeout.)

**SS.Q4 — companion C: terminal disposition unchecked.** Mutation: the
standing path reports `ESTABLISHED` whenever the derived identity
appears in the lineage, ignoring the terminal disposition. Strict mode,
one channel compromised, **DNS compromised** variant, matching Q1's
DNS-compromised correct-form run. Required result: correspondences **violated**
by *two* distinct trace shapes — the abandoned attempt of a shipped
lineage (S2 reported as established) and an attempt of a refused
lineage (S4 reported as established) — exhibiting that the third
binding of A3.7.1 is load-bearing and that S4 is not S2 under another
name.
- Timebox: 15 minutes.
- Prediction: violation found; ProVerif reports one trace per query,
  so the two shapes are exhibited by running (ii) once per honest key
  with the fixture arranged so `skH1` runs only `ShipIssuer` and `skH2`
  only `RefuseIssuer` in this companion. **Fixture exception, registered
  here:** that arrangement departs from the correct model's fixture
  (two shapes per issuer, replicated), so this companion matches the
  correct form only up to the rearrangement, and note 3's
  two-honest-values rule is relaxed on the terminal-disposition axis
  *per issuer* for this companion only (both terminal values remain
  present across the fixture). Reason: one trace per query. The
  alternative that keeps the fixture intact is per-shape judge events
  (`EstablishedShip`/`EstablishedRefuse`, the S-P3 recut-2 pattern);
  if a reviewer prefers it, no prediction changes. (p ≈ 0.8; p ≈ 0.1
  recut; p ≈ 0.1 timeout.)

**Ablation rule (on any timeout):** collapse the lineage to one entry,
then drop the second issuer, then drop the refused lineage shape;
re-run; record the break point. A timed-out query's ledger entry
records "mechanism failure at N entries/issuers," never a property
claim.

**Ordering rule:** Q1 (both variants) before Q1d and before every
companion (a companion is evidence only against a matching correct
form); Q2, Q3, Q4 in any order after Q1.

## Carried checks (in the verifier; predicted inert; not queries)

Per S-P3 F7, the model's header names which checks are load-bearing
for its queries. Predictions, to be confirmed or overturned by the
cross-family falsification review (note 5 item 1):

- **Load-bearing (predicted):** TLR signature under the entitled key;
  the standing path's own `fp(kTLR) = kfpr` against the evidenced tuple
  (Q3); derived identity computed by the verifier and looked up in the
  lineage (Q2); terminal disposition equal to `TERM_SHIPPED(aid)` for the
  looked-up identity (Q4); in strict mode, cross-channel tuple
  agreement (what makes "evidenced tuple" mean the honest one — S-P3
  F1's observation, consumed).
- **Carried, predicted inert against the A1.3 adversary:**
  - *Well-formedness* — `terminal = TERM_SHIPPED(aid)` requires the
    lineage's entry for `aid` to read `DISP_SHIPPED`, else the path reports
    `(UNVERIFIABLE, STANDING_EVIDENCE_MALFORMED)`. Inert because a
    malformed TLR under an honest key requires the honest issuer to
    sign one, and the fixture's issuers do not; the adversary cannot
    sign under `skH1`/`skH2`. **Prediction:** removing this check
    changes no query result. This is why it is not registered as a
    companion (a companion that cannot fail); it is a vector
    obligation (below). If a reviewer finds it load-bearing, that is a
    finding the record wants.
  - *Anchor-digest binding* — the presented anchor proof is over
    `h(TLR)` of the presented TLR, else `(UNVERIFIABLE,
    STANDING_EVIDENCE_TEMPORAL_MISMATCH)`. Inert because the anchoring
    oracle is public (A1.3 item 5) and time is not represented; the
    reason code is emitted here only so the vocabulary is complete in
    the model. **Prediction:** removing it changes no result. Its
    content is ledger C-2.
  - *Envelope path* — carried in parallel so orthogonality is
    structural; its verdict is P4's and is not queried here.

## Vector obligations this model records (H1a/P8 S-series; not symbolic)

Recorded so the suite is not later blamed for not containing them
(ENUMERATION §2's own sentence), with the reason each is a vector:

1. **S1–S4 with their registered reason codes**, pairwise distinct
   across S2/S3/S4, and a **collapsing companion for any pair → must
   fail the discrimination check** (first-link `DECISION.md` exit
   condition 3 as amended by SC-3). *Why a vector:* the discrimination
   check is a property of the verifier's output function over
   constants; a symbolic collapse companion fails only because two
   constants were made one, which is evidence about the constants, not
   about the mechanism. The five vocabulary-liveness witnesses in
   Q1(iv) make the codes visible in the model; the check is the
   probe's Q4 shape,
   re-run as conformance vectors.
2. **`STANDING_EVIDENCE_MALFORMED`** — the probe F1 shape (terminal
   `TERM_SHIPPED(a1)` while the lineage entry for `a1` reads
   `DISP_ABANDONED`),
   mandatory red vector; **a broken companion that accepts it must
   fail** (SC-3 text). *Why a vector:* an honest-but-defective issuer
   signed both halves; not an A1.3 capability (`RESULTS-PROBE.md` F1:
   "Not a security finding (the issuer signed both halves); a
   conformance finding").
3. **`STANDING_EVIDENCE_TEMPORAL_MISMATCH`** — a TLR whose anchor fails
   the A2.1 predicate against `declTerminal` under the issuance
   policy's δ and ε (SC-1). *Why a vector (and a join):* arithmetic;
   the A2.1 predicate's model is the TLA+ bridge family, and the
   verifier-side vector is the same three-conjunct test on a second
   anchored object.
4. **Orthogonality** — S3 leaves an old bundle's `VALID_STRICT`
   unaffected while standing is negative (exit condition 3's
   orthogonality condition). The model's parallel envelope path makes
   this structural but does not test the verdict; the vector does.

The S-series vectors are H1a/P8-track artifacts per ENUMERATION §2 and
the 2026-08-29 dispositions (Q3 assumption "was never the problem").
This file changes nothing about where they live.

## What S-STANDING produces, and for whom (ledger interface, A3.3 fields)

**Producer entries offered (once the model exists):**

- **P-1 — Standing relation.** `Established(kH, t, aid)` under an
  honest entitled key implies `Designated(kH, aid)`: the issuer holding
  `kH` signed one TLR whose lineage contains `aid` and whose terminal
  designates `aid`. Consumers: the A3.8 base assessment's
  `protocol_standing` dimension and the relying-party story ("what a
  bundle presented alone establishes"); the integrated adversarial
  lifecycle model (A3.9, pre-H1a-freeze), which must reproduce this at
  the seam with wrapping; S-P7's innermost-identity claim. Shared
  terms: entitled key, derived identity, TLR. Adversary at the join:
  A1.3, one channel compromised. Severing companions: Q2 (identity
  declared), Q4 (terminal unchecked). Residuals: `h` injectivity —
  **the whole load of the transplant result**; P8's "what bytes are
  the core"; deterministic signatures; two-entry lineages.
- **P-2 — Entitled key inside the standing path.** `Established(kX,
  t, aid)` implies `fp(kX) = kfpr(t)` for the evidenced `t`. Consumer:
  the H1a conformance profile (the blind re-scoring's note becomes a
  checked shape rather than a caution). Severing companion: Q3.
  Residuals: `fp` idealization (library header); S-P3 entry 1 for what
  "evidenced tuple names the key" rests on.

**Consumer entries (assumes-from-elsewhere):**

- **C-1 — Key-binding relation** from S-P3 ledger entry 1 (producer
  Q2, `Reattributed` unreachable; severing companion S-P3 Q3). What
  S-STANDING assumes: the artifact's bytes belong to the key the
  evidenced tuple names. Residual as S-P3 states it.
- **C-2 — TLR anchor temporal validity (cross-formalism; never
  symbolically discharged).** Producer: the A2.1 predicate as modeled
  in the P5c bridge family (`formal/tla/P5cP5P6_Bridge.tla` and
  successors), applied per SC-1 to a second anchored object with
  `declTerminal` in place of the declared issue time. Shared term:
  "anchor valid." What S-STANDING assumes: a TLR reported as
  `ESTABLISHED` passed that predicate; the symbolic model cannot say
  so and must not be marked as having done so (ENUMERATION §4 red-bar
  condition; Sol finding 2). See the routed question on whether the
  second anchored object needs its own TLA+ instance.
- **C-3 — Canonicalization injectivity and the core's byte
  composition** (P8, [proof] + golden vectors). What S-STANDING
  assumes: two distinct attempts have distinct cores and the verifier
  reconstructs the core bytes exactly.
- **C-4 — Type soundness of the TLR object and of wrappers** (P7 /
  S-P7). What S-STANDING assumes: a TLR is never accepted as another
  object type or vice versa, and a wrapped bundle's standing is
  evaluated against the innermost issuance identity. S-STANDING's
  transplant companion exhibits the identity-binding half; the
  re-scoping half is S-P7's.
- **C-5 — SC-2's one-signing-act commitment** (specification
  commitment, `DECISION.md` R2). What S-STANDING assumes: the TLR's
  terminal disposition *is* the disposition fact the A3.7.2 refusal
  record also projects. Not modeled here; the refusal record and its
  state machines are the A3.9 refusal-decomposition obligation (TLA+).

The discharge matrix (consumer entry → producer query → severing
companion → expected red) is written only once the models exist
(ENUMERATION §3's own rule).

## Draft header text (per-model "This model proves / does not prove")

To be carried in every S-STANDING `.pv` file, narrowed after the run to
what the queries discharged (S-P3 recut-3 discipline):

> This model proves: under the A1.3 adversary with one of two authority
> channels compromised (both variants), key substitution expressible,
> possession free, and any artifact, bundle, TLR-shaped object, or
> anchor proof freely constructible, a standing report of ESTABLISHED
> computed against an honest entitled key implies that the issuer
> holding that key signed one terminal lineage record whose lineage
> contains the presented artifact's verifier-derived identity and whose
> terminal disposition designates that identity — A3.7.1's three
> bindings under one signature — and that no ESTABLISHED report is
> computed against a key the evidenced authority tuple does not name.
> Under a perfect hash (h injective) and a perfect fingerprint (fp
> injective); the transplant result's entire load is h.
>
> This model does not prove: that no second, contradictory TLR under
> the same key exists (the G4 boundary; probe F3; A2's residue,
> confined not closed); anything temporal about the TLR's anchor
> (cross-formalism join C-2); that malformed standing evidence is
> rejected (carried check, inert here; S-series vector); that S2/S3/S4
> reason codes are pairwise distinct (vector); P7 type soundness of the
> TLR object or which identity a wrapped bundle's standing binds to
> (S-P7); the composition of the signed core or its encoding (P8);
> consistency between the TLR and the A3.7.2 refusal record (SC-2,
> A3.9 obligation); anything about lineages of other than two attempts;
> in degraded mode with the sole channel compromised, that an adversary
> cannot establish standing for its own artifacts under its own key
> (reachable; the first-link spike's Q5b waiver cost. The S-P3 F8
> ruling of 2026-09-05 says this is "not a P3 defect"; reading it as
> covering the standing correspondence is the clerk's — routed item 4).

## What this plan does not claim

- Anything about equivocation by the entitled key. The G4 sentence is
  the construction's boundary and this model inherits it verbatim.
- That the S-series vectors exist or pass; they are recorded, not
  written.
- That the TLR object type is within P7's enumerated set (it is not, as
  registered — routed).
- That the row-2 successor-slot construction (D1, docket item 25) is
  touched: it chains issuances forward; this model chains attempts
  within one issuance backward; "not gated on, and does not gate, the
  S-STANDING model" (DECISION.md D1 amendment).
- Anything the integrated lifecycle model (A3.9, pre-H1a-freeze) owes:
  this is the targeted model; the seam-containing model remains a
  separate obligation.

## Routed to the author (none block freezing this file; each is a ruling only the author can make)

1. **ROUTED TO AUTHOR — P7's enumerated type set and the TLR tag.** P7
   as registered enumerates six signed-object types (base attestation,
   wrapper, issuer-key manifest, authority evidence, conformance
   vector, review-recency attestation). The terminal lineage record is
   a seventh signed-object kind with its own domain-separation tag
   (the probe used `TLR`; this plan declares it model-local). Adding a
   type to P7's set is a property-list change under the pre-registration's
   change discipline (signed, dated amendment). Until ruled, this file
   declares the tag in the model, not in the library, and the S-P7
   plan should not assume the set is closed. (The A3.7.2 portable
   refusal record raises the same question; noted, not routed here.)

   > **ADOPTED (author), 2026-09-06** (ROUTED A6): Amendment 4 §A4.5 adds the terminal lineage record and the portable refusal record to P7's enumerated set. Until signed, the tag stays model-local as this plan says; on signature it enters the library as a recorded divergence.
2. **ROUTED TO AUTHOR — whether SC-1's "same three-conjunct test on a
   second anchored object" needs its own TLA+ instance**, or is covered
   by the existing A2.1 bridge family by the identity of the predicate.
   Under the 2026-08-29 Question 2 ruling every claim needs at least one
   tool leg; ledger C-2 currently names the existing bridge model as
   producer by that identity. If the author reads SC-1 as a distinct
   claim (two anchored objects, sequenced — price (iv)), that is a
   TLA+ obligation, not a change to this plan.

> *Disposition (clerk), 2026-09-06 — settled from the record, not routed; listed for veto in `formal/suite/ROUTED-2026-09-06.md` §B.* Recorded as an open cell in `formal/COVERAGE-MAP.md` row 13, decided when the capstone ledger is written; does not gate this file's freeze. (B8)
3. **ROUTED TO AUTHOR — literal wrapper shape in the transplant
   companion.** A3.9 names the companion as a *wrapper* transplant.
   This plan realizes the forged outer artifact as any adversary-built
   artifact and hands wrapper types and innermost-identity re-scoping
   to S-P7 (ledger C-4). If the author reads the A3.9 naming as
   requiring the wrapper shape inside S-STANDING, Q2 gains a
   wrapper-shaped constructor and a second trace, and S-P7's scope
   narrows correspondingly; no prediction above changes.

   > **ADOPTED (author), 2026-09-06** (ROUTED A7): the wrapper shape is required here. Q2 gains a minimal wrapper-shaped outer-artifact constructor and a second transplant trace; S-P7's scope is unchanged (it models the identity relation only). No prediction changes, per this item's own statement.
4. **ROUTED TO AUTHOR — scope of the S-P3 F8 ruling.** The dated
   ruling (S-P3 RESULTS F8, RULED, author, 2026-09-05) is scoped to P3:
   "P3's threat is re-attribution of an existing signature"; degraded-
   mode impersonation is "not a P3 defect". This plan predicts Q1d's
   correspondence (i) to fail and calls that failure "the registered
   cost" (§"Adversary and modes", §"The judge and the correspondence",
   Q1d, header text). Reading the P3 ruling as covering the standing
   correspondence in degraded mode is the clerk's inference; the
   author's stated reason is general (degraded service hands evidence
   to the verifier; Tessera does not decide for the relying party) but
   the ruling's sentence is not. If the author reads A3.7.1's
   unrestricted sentence as required to hold in degraded mode, Q1d's
   (i) is a predicted defect of the construction under the sole
   compromised channel, not a cost, and the header text changes.

   > **RULED (author), 2026-09-06** (ROUTED A8; registered as Amendment 4 §A4.6): the principle is general. Q1d's failure of correspondence (i) under the sole compromised channel is a registered cost of degradation, provided the verdict says degraded; the header text stands as drafted. His words: *"the adjudicator will have to make the decisions based upon the information available to them; anything else would imply some long-term service guarantees of Tessera, which I view as dishonest."*
5. **ROUTED TO AUTHOR — ENUMERATION §2 and note 4 item 1 conflict on
   the collapsing companion.** §2 (lines "Standing tests S1–S3", 2026-
   08-17) places the reason-code collapsing control at vector level
   "with P8/H1a vectors"; note 4 item 1 (2026-09-04) says the S-STANDING
   model "must additionally cover … pairwise-distinct reason codes
   across S2/S3/S4 and a companion collapsing any pair going red". This
   plan follows §2, for the reason given in Vector obligations item 1
   (a symbolic collapse companion fails only because two constants were
   made one). If the author reads note 4 as controlling, Q1 gains a
   companion collapsing two reason constants and the prediction is
   red-by-construction (recorded as such, p ≈ 0.95 violation, p ≈ 0.05
   encoding).

> *Disposition (clerk), 2026-09-06 — settled from the record, not routed; listed for veto in `formal/suite/ROUTED-2026-09-06.md` §B.* Both: note 4 (2026-09-04) is the later text and controls; Q1 gains the collapsing companion, registered red-by-construction (p ≈ 0.95 violation, p ≈ 0.05 encoding), and the vector obligation stands. (B9)

## Review log

- 2026-09-06 — clerk-drafted by the AI collaborator from the entered
  standing decision (`DECISION.md`, `AMENDMENTS-2026-08-31.md`,
  `DECISION-CRITERIA.md` §1 as amended), the probe's findings
  (`RESULTS-PROBE.md` F1–F3, Q1–Q7), the blind re-scoring's conformance
  note, the S-P3 plan and results (suite rules, F5–F8 and the
  2026-09-05 ruling), and the library. No S-STANDING model has been
  written, parse-checked, or run; nothing in this file is evidence.
  Author cold read pending; freeze is the author's commit.
- 2026-09-06 — skeptic (falsification) review of this draft applied,
  pre-freeze: Q3's correspondence-(i) prediction corrected (was
  predicted to stay true; it is violated by the Q1d adversary-key
  shape, and the discriminating query is `StandingUnentitled`); the
  F8 ruling re-quoted with its P3 qualifier and its extension to
  standing routed (item 4); the §2 / note 4 conflict on the collapsing
  companion routed (item 5); per-entry and terminal disposition
  constants renamed apart; the reason-code list split into registered
  and probe-recorded; a fifth report witness (G1's correct-side
  polarity) added; report witnesses relabelled as vocabulary-liveness,
  not N1; Q1 probabilities rebalanced to 1.0; companion channel
  variants named; Q4's fixture rearrangement registered as an
  exception; RESULTS-PROBE F1 quoted in full. Still not frozen.

---

## Post-freeze addendum 1 — 2026-09-12: standing binds to the tuple in the core (Amendment 5 §A5.6; ROUTED C10, ADOPTED (author))

**Status: PROPOSED, registered before any model change or run; the
commit is the author's.** Post-freeze addition, not a refinement: no
registered query, prediction, judge or companion above is altered; the
SS.Q1–Q5 ladder outcomes in `RESULTS.md` must be identical after the
change, and any difference is a recorded divergence. (*The status line
at the head of this file still reads "Not frozen; no model exists and
nothing has been run." That line is stale: it was committed unchanged
in `5188e7a`, this file's signing and freeze commit — the pattern the
author resolved for Amendment 4 at ROUTED C1. Retained per
amend-don't-rewrite; "post-freeze" means after `5188e7a`.*)

**What is registered.** The standing path (the verifier process that
derives `aid = h(core)` and computes the standing report) must check
that the presented authority tuple `t` equals the tuple embedded in
the core it derives the identity from: `let attemptCore(=t, …) = core`
(or the pattern equivalent) on the standing path, as the envelope path
already does. Note 4 item 2's principle — bind to what the verifier
holds, not to what the presenter names — applied to the tuple as it
is already applied to the key.

**Fixture extension (N2 on the new axis).** One honestly enrolled
**alias** tuple: `mAlias = authTuple(issuerIdAlias, fp(pk(skH1)), …)`
— the same key as `m`, a different identity — evidenced by both
channels exactly as `m` is, and published. The honest issuer H1 signs
its TLR under `m` only. No other fixture change.

**New judge (encoding registered here) — and the report channel it
needs.** The existing report channel `estCh` carries `(kX, t, aid)`
only; the core is **not** on it, and `Established` is an event, which
no judge can read. So the standing path gains **one new private report
channel**, `aliasCh`, carrying `(kX, t, core, aid)`, emitted at the
`ESTABLISHED` branch in parallel with the `estCh` report (S-P3 recut-1
idiom). `estCh`, `reasonCh`, `Judge` and `ReasonJudge` are untouched,
so SS.Q1 (iii) and (iv) cannot move on the judge's account.
`AliasJudge` reads `aliasCh`, destructures the core, and emits
`event Aliased(kX, t, tCore, aid)` when `t ≠ tCore` where
`attemptCore(tCore, …) = core`; it emits nothing when the core is not
an `attemptCore` term. Instrumentation, not a verifier check.
`HonestStandingEstablished` stays the vacuity guard.

**Where the tuple pin goes (registered).** The `let attemptCore(=t, …)
= core` pattern is placed **after** the `se = noTLR` test and the
`withTLR` / entitled-key / TLR-signature branches, immediately before
the lineage lookup, so that no `ABSENT` or `UNVERIFIABLE` reason-code
branch acquires a new precondition. The five vocabulary-liveness
witnesses and B9 therefore keep the traces they have: `SUPERSEDED`,
`NO_TERMINAL_DISPOSITION_EVIDENCE`, `ISSUANCE_REFUSED` and the
`UNVERIFIABLE` codes are all decided before the pin, and
`STANDING_EVIDENCE_MISMATCH` stays reachable through a well-formed
`attemptCore(t, …)` whose derived identity is absent from the lineage
(`attemptCore` is a public `[data]` constructor, so the adversary can
build one). What the pin does remove is the A7 wrapper-shaped core
(`wrapCore`) from the standing path of the **correct** model: such a
presentation now produces no report at all rather than a mismatch
report. No registered witness needs it, and SS.Q2's companion — which
is where the A7 wrapper transplant is registered and exercised — is
untouched.

**Query SS.Q6 (correct model, `ss_q1_strict_dns_compromised.pv`
amended in place; also applied to the repo-compromised and degraded
variants so the ladder stays uniform):** `Aliased` unreachable; SS.Q1
(i)–(iv), the five vocabulary witnesses and B9 unchanged. Prediction:
unreachable, terminating, SS.Q1 lines unchanged (0.75); the alias
fixture changes an SS.Q1 result = divergence, recorded, most plausibly
(i) since it is fixture-bound (0.10); unexpectedly reachable = defect
in the new pattern (0.05); timeout (0.10). Box 30 min.

**Companion SS.Q6-C (`ss_q6_companion_alias_unchecked.pv`): the
tuple check removed on the standing path, alias fixture present.**
`Aliased` reachable. Predicted trace shape: H1's honest core under `m`
with H1's honest TLR, presented with `mAlias` and its honest evidence;
the standing path binds `pk(skH1)` to `mAlias`, derives `aid` from the
core, finds it designated in H1's TLR, reports `ESTABLISHED` against
`mAlias`. Prediction: reachable with that shape (0.80); recut (0.10);
companion green (0.05); timeout (0.05). Box 30 min. Red on exactly
`Aliased`: `StandingUnentitled` and `ReasonCollapsed` stay
unreachable; `Established ==> Designated` per honest key still holds
in the companion (the key is honest and did designate the identity —
that is the point: the key-level correspondence cannot see the alias).

**Header change registered.** The Q1 claim block gains, under "This
model proves", that an `ESTABLISHED` report is computed only against
the authority tuple embedded in the core whose identity it designates;
under "does not prove", anything about two identities legitimately
sharing one key beyond their having separate lineages (Amendment 5
§A5.6).
