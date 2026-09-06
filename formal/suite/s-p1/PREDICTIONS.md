# S-P1 — integrity (headline, operative form): query plan and registered predictions

**Status: PROPOSED — clerk-drafted by the AI collaborator 2026-09-06;
not adopted; the commit is the author's. No model exists and nothing
has been run.** Per `formal/suite/ENUMERATION.md` §5, predictions are
registered and frozen — by the author's signing commit — before any
S-P1 model is run. The author's cold read of this file precedes that
commit. Post-freeze changes are prediction divergences (spike rule),
never refinements. Amend-don't-rewrite applies from first commit.

Governed by: `ENUMERATION.md` §1–§2, §5 (discipline), §6 (sequencing:
S-P1 second, after S-P3); Amendment 1 P1 as registered (§A1.2) and
A1.3 (adversary); Amendment 3 §A3.1 items 1–2 (P1's symbolic
statement; the operative headline) and §A3.3 (ledger conservation
fields; three-outcome timebox discipline); `ENUMERATION.md` "Author
dispositions — 2026-08-29", Question 2 (scope of the symbolic leg);
`formal/suite/s-p3/RESULTS.md` "Suite rules from S-P3" and finding F7
(the consumer obligation handed to S-P1). Library:
`formal/suite/lib/tessera_theory.pvl` (PROPOSED); no library term is
redeclared by any S-P1 model.

## Target

P1 as registered (Amendment 1 §A1.2, verbatim):

> **P1 — Integrity (the headline claim).** There is no reachable state
> in which the verifier returns `VALID_STRICT` or `VALID_DEGRADED` for
> a package whose canonical bytes differ from bytes signed at issue
> time. **[model]**

Its operative form (Amendment 3 §A3.1 item 2, the Sol finding 1
repair): alteration is trivial; *surviving verification over altered
bytes is what is hard* — **no transition leads to an accepted receipt
over altered bytes.** Its symbolic statement (§A3.1 item 1):
**existential issuance-event authenticity, a non-injective
correspondence**, with replay and context scoped to caller policy.

**Scope of this leg — quoting the dated ruling.** `ENUMERATION.md`,
"Author dispositions — 2026-08-29", Question 2, RULED (author):
*"it is acceptable, so long as at least one leg covers every claim …
in cases where they overlap both must support the claim."*
Consequence recorded there: *S-P1's symbolic leg proves the binding
half ("no acceptance over altered bytes"); P4's TLA+ model owns the
verdict partition.* This plan follows that split exactly:

- **Here (symbolic):** an acceptance event over framed bytes `fb`
  under key `k` occurs only if `fb` is exactly what `k`'s holder signed
  at an issuance event. No verdict vocabulary appears in any S-P1
  model; the symbolic `Accept` is the event P4's model classifies.
- **Not here (P4, TLA+):** that every path stopping short of `Accept`
  lands in `INVALID` or `UNVERIFIABLE`, never in a valid verdict
  (`formal/tla/P4_VerifierStates.tla`, invariants `Partition`,
  `NoSilentPromotion`, `ExactInvalid`, `ExactUnverifiable`,
  `ValidNeedsNonWaivablePass` — the module header's "P1-facing
  corollary" — and `StrictMeansEverything`; the same set is to be
  carried in `formal/COVERAGE-MAP.md` row 1, PROPOSED 2026-09-06,
  untracked, which currently names the first four). The join between
  the two is a cross-formalism ledger entry (below), never marked
  symbolically discharged (ENUMERATION §4).

**The consumer obligation from S-P3 (RESULTS.md F7).** S-P3 found that
its re-attribution queries never exercise the attestation-signature
check; what exercises it is an *authorship correspondence* — accepted
under an honest key ⇒ that key signed those bytes — and F7 hands that
to S-P1 as its integrity claim. This plan makes it S-P1's headline
query (Q1(ii)/Q2(i)); it is not a separate lemma.

## The claim in symbolic form (registered here, before any run)

Let `fb` be the framed bytes (the P3 field list as a transparent
constructor, exactly as in S-P3: `framed(objType, alg, issuerId, kfp,
mh, canonVer, payload)` under the `BYTES` tag). The honest issuer
emits the library event `IssuerSigned(pk(skI), fb)` immediately before
releasing `sign((BYTES, fb), skI)`. The verifier's acceptance is the
event over `(…, kX, fb)`.

**Headline query (both modes):**

> `AcceptedUnderHonestKey(k, fb) ⟹ IssuerSigned(k, fb)`

— a non-injective correspondence: *if bytes `fb` are accepted under
an honest key `k`, then `k`'s holder signed exactly `fb` at an
issuance event.* The contrapositive is P1's operative form: bytes
differing from what `k` signed ("altered bytes") are never accepted
under `k`.

Three deliberate choices, each with its reason:

1. **Non-injective, by registration.** §A3.1 item 1 registers P1's
   symbolic statement as non-injective: replay of a genuinely issued
   package preserves identity and P1 permits it. No injective
   (`inj-event`) form is queried. A reviewer who proposes one is
   proposing a change to §A3.1, not to this model.
2. **Restricted to honest keys — a mechanization device, not a scope
   cut.** ProVerif events are emitted only by modeled honest
   processes. For a key the adversary holds, the unrestricted form
   conflates two claims that are not P1's: that the accepted key is
   an honest issuer's (*authority* — P10 / the first link), and that
   honest bytes are never accepted under a DSKS-derived key
   (*re-attribution* — S-P3's `Reattributed`; the library's D-4 rule,
   `checksign(sign(m, k), pk(dsks(sign(m, k), r))) = m`, lets the
   adversary hold a key under which an honest signature verifies
   without ever signing under it, so "the accepted bytes are what
   that key signed" is *not* a tautology for derived keys). Neither
   excluded trace violates P1's letter: bytes accepted under an
   adversary-signed or DSKS-derived key are still bytes signed at an
   issuance event. The restriction therefore excludes no
   P1-violating trace; it excludes P10's and P3's, and keeps P1's
   query about P1. The unrestricted form is
   nonetheless run in both modes as a contrast (Q1(i) holds in strict
   mode; Q2(ii) is registered red in degraded-compromised mode), so
   the record shows precisely which claim the restriction excludes.
3. **"Altered" is term inequality.** In the model, bytes differ from
   signed bytes iff the framed terms differ. P1's "canonical bytes"
   are P8's: two byte strings canonicalizing to one input are one term
   here. That is a Layer 2 residual until P8's proof exists (ledger,
   below) — cited, never absorbed.

The honest-key restriction is realized by a judge (encoding below),
so that the headline query and the N1 honest-flow witness come from
the same judge mechanism (two judge processes reading the same
private channels), per the suite rule carried from S-P3 recut 3.

## Abstractions this plan fixes (and their residuals)

- **Framed bytes** — `framed(…)` as in S-P3, so the ledger's shared
  term is literally shared. **Residual:** frame layout and encoding
  are P8's; `framed(…)` is "these fields are inside the signed
  bytes," not a layout claim.
- **Single signer per package.** `sset` is the honest singleton. The
  multi-signer case (each required signature covering the exact bytes;
  the required set itself signed) is S-P2's, not S-P1's; S-P1
  establishes the per-signature fact S-P2 extends to the set.
- **Manifest** — the map-v1 `authTuple` for n = 1, honestly published;
  `mh = h(manifest)` inherits h's idealization (library header).
- **Possession** — over the manifest (library D-3). Unexercised by
  S-P1's queries (expected; see the header text below) and carried so
  the verifier is the same verifier S-P3 checked, not a subset of it.
- **Fingerprint match** — key equality under `fp` injectivity
  (library header). S-P1 does not re-prove key binding; S-P3 covers
  that axis and the two compose at the capstone (ledger entry 1,
  complementary — not consumed).
- **Signatures** — Dolev–Yao unforgeable, deterministic, with the D-4
  DSKS rule. **Unlike S-P3 (its F5), S-P1's result is expected to
  rest on signature unforgeability**: remove `checksign`'s
  unforgeability and the headline goes red. This is stated so the
  header can name it as the load-bearing assumption rather than
  discovering it in review.
- **Chosen-message issuers.** The adversary supplies each honest
  issuer's payload (S-P3 fixture). Consequence: S-P1 binds the *exact
  bytes*, not the payload's origin or truth — an issuer that will sign
  anything is the right fixture for a property that claims nothing
  about what was signed (§A3.1: meaning, truth and intended use are
  outside the attestation).
- **Rejection is non-acceptance** (spike idiom); the verdict partition
  is P4's (scope ruling above).

## Adversary and modes

A1.3 throughout: item 1 (alter any bytes after issue) is the
capability under test; items 2–6 are present, not defended against
here except as the verifier's other checks incidentally block them.
Possession is free to the adversary (P10). Two evidence modes, run
separately — P1's text names both verdicts, so both are registered:

- **Strict** — two authority channels, both required, one compromised
  (its signing key public); both channel variants run (spike
  convention: a generic single channel is not accepted as
  representing both).
- **Degraded** — one authority channel, sole evidence (A3.2
  `VALID_DEGRADED` never-zero), **that channel compromised**. The
  hard case: the adversary vouches for any key it likes, and the only
  thing standing between an honest key and altered bytes is the
  attestation-signature check over the exact frame.

**Omitted, with reason:** degraded mode with an *honest* sole channel.
Dolev–Yao attacker knowledge is monotone — publishing `skS` only
enlarges the reachable set — so a headline query unreachable in the
compromised variant is unreachable in the honest one. The honest
variant is therefore not registered; if the compromised variant
times out, the honest variant becomes the first ablation step
(ablation rule, below), not a substitute result.

**Relying-party consequence this leg sharpens** (in the terms fixed by
S-P3 F2/F8 and the ruling quoted there): in degraded mode with the
sole channel compromised, fresh bytes signed by the adversary under
its own key remain acceptable — the registered waiver cost. What S-P1
adds is that this cost is *bounded to the adversary's own key*: an
honest issuer's key can never be made to vouch for bytes it did not
sign, altered or fresh, however the channel is compromised.

## The judge (encoding registered here, before any run)

Suite rules from S-P3 applied without exception: report outputs to
private-channel judges are **parallel** with their continuations
(recut 1); the N1 witness is honest-flow acceptance **emitted by the
judge** (recut 3); judge locals never shadow library names; each
model's header names which checks are load-bearing.

- The main process outputs each honest issuer key once on a private
  channel `honestKeyCh` (replicated, so the judge may consume it for
  every acceptance).
- The issuer reports `(pk(skI), fb)` on private `honestCh` for each
  `fb` it signs (in parallel with the public output).
- The verifier reports `(kX, fb)` on private `acceptCh` for each
  acceptance (in parallel with its continuation).
- **Judge H (headline):** `in(honestKeyCh, kH); in(acceptCh, (=kH,
  fbAcc)); event AcceptedUnderHonestKey(kH, fbAcc)`. The registered
  query is the correspondence `AcceptedUnderHonestKey(k, fb) ⟹
  IssuerSigned(k, fb)`. The judge cannot observe "was not signed";
  the correspondence is what states it.
- **Judge N1 (witness):** `in(honestCh, (kH, fbHon)); in(acceptCh,
  (=kH, =fbHon)); event HonestAccepted(kH, fbHon)`. Must be
  **reachable** in every model, companions included — a companion
  whose honest flow is dead is not evidence that its red means
  anything.
- The unrestricted contrast is the plain correspondence on the
  acceptance event: `Accept(…, kX, fb) ⟹ IssuerSigned(kX, fb)` (strict,
  library 5-ary `Accept`) / `AcceptS(ev, t, kX, fb) ⟹ IssuerSigned(kX,
  fb)` (degraded, model-local 4-ary `AcceptS`, spike Q5 shape).

Deliberate scope of judge H: it is keyed on honest *keys*, not honest
*bytes*. It is therefore blind to re-attribution (honest bytes
accepted under an adversary key) by construction — that is S-P3's
subject; no S-P1 query depends on it, so S-P1 does not re-prove it
and does not consume it (ledger entry 1, complementary).

## Fixture statement (ENUMERATION note 3, N1/N2)

Every S-P1 model carries: **two honest issuers** (`skI`, `skI2`), each
with its own honestly published manifest, each replicated with
adversary-chosen payloads — so both axes the headline query binds
(`k`, `fb`) carry at least two honest values, and "with the same `fb`"
has content beyond a one-element set; **a reachability query on
`HonestAccepted`** (N1, judge-emitted), expected `not event(…) is
false`; the strict models additionally carry two authority channels
with two honest tuples each. Recorded in the plan this time, so no
later RESULTS entry has to call it an omission.

## "This model proves / does not prove" — registered header text

To be carried verbatim (adjusted per variant) in each correct model's
header, with the load-bearing statement required by S-P3 F7:

> **This model proves:** in [strict mode with one of two required
> authority channels compromised | degraded mode with the sole
> authority channel compromised], under an adversary that can alter
> any bytes after issue, holds every key it uses, and has the A1.3
> item 3 (DSKS) capability, framed bytes accepted under an honest
> issuer's key are exactly the bytes that issuer signed at an
> issuance event — the [model] binding half of P1 in its §A3.1
> operative form, as a non-injective correspondence.
> **This model does not prove:** the verdict partition (P4, TLA+);
> that acceptance is fresh or context-bound (replay is permitted,
> §A3.1 item 1); that the accepted key is an honest issuer's (P10 /
> the first link — in degraded-compromised mode it is not, and the
> unrestricted contrast query is registered red); re-attribution of
> honest bytes to another key (S-P3, complementary — composed at the
> capstone, not consumed here); the multi-signer set
> (S-P2); canonicalization or the frame's byte layout (P8); wrapper
> soundness (P7); anything temporal (P5/P6); the verification
> profile (H1a).
> **Load-bearing for these queries:** the attestation-signature check
> `let (=BYTES, =fb) = checksign(sg, kX)` binding the *presented*
> bytes to the *signed* bytes, resting on signature unforgeability
> (library, Dolev–Yao). **Carried, not exercised here:** the
> fingerprint match and manifest-hash check (S-P3), possession over
> the manifest (A1.5/P10, S-P3 entry 2), the authority-evidence check
> (inert in degraded-compromised mode by construction, S-P3 F6),
> object type (P7); canonicalization version and algorithm profile
> (P8/H1a); algorithm identifier (A3 identifier-binding invariant,
> per F7); issuer identity (F8 and its 2026-09-05 ruling).

Per ENUMERATION amendment note 5 item 2, each model also carries the
reading aids (typing convention, cast list, plain-language claim /
adversary / boundary) as reviewed testimony, not a gate.

## Query ladder, timeboxes, predictions

Outcome vocabulary is the registered three: **violation**
(counterexample trace), **timeout** (mechanism failure — evidence
about the tool or encoding, never about the property),
**termination** (evidence for the checked abstraction only).
Timeboxes are per run; each channel/mode variant gets the full box.
S-P3's ladder terminated in ≤ 1 s against 15–30 min boxes; the boxes
here keep parity with S-P3 rather than shrinking on that evidence.

Proposed files: `sp1_q1_strict_dns_compromised.pv`,
`sp1_q1_strict_repo_compromised.pv`, `sp1_q2_degraded_compromised.pv`,
`sp1_q3_companionA_sig_unbound.pv`,
`sp1_q4_companionB_frame_unsigned.pv`.

**S-P1.Q1 — correct model, strict mode: the binding half where
authority also holds.** Both channels required, one compromised (both
variants). Queries: (i) unrestricted `Accept ⟹ IssuerSigned` — the
spike's "accepted key signs the exact framed bytes" link, transcribed
to the suite library and the structured frame; (ii) the headline
`AcceptedUnderHonestKey ⟹ IssuerSigned`; (iii) N1 `HonestAccepted`
reachable.
- Timebox: 15 minutes per variant.
- Prediction: all three as stated, both variants. (p ≈ 0.75; p ≈ 0.15
  violation — most likely a judge or frame encoding defect needing one
  recut, disposition by trace inspection; p ≈ 0.10 timeout.) A
  violation of (i) that survives trace inspection would contradict
  S-P3 Q1(ii) and the spike's Q1 over the same theory, and is
  therefore to be treated first as a transcription defect.

**S-P1.Q2 — correct model, degraded mode, sole channel compromised:
the P1 binding claim in the hard case.** Queries: (i) headline
`AcceptedUnderHonestKey ⟹ IssuerSigned` — **the registered P1 [model]
claim for this leg**; (ii) unrestricted `AcceptS ⟹ IssuerSigned` —
**registered red**: reachable via impersonation with the adversary's
own key (the Q5b lineage; S-P3 F2), the degraded-mode cost handed to
the verifier by the ruling recorded at `s-p3/RESULTS.md` F8, *RULED
(author), 2026-09-05*; (iii) N1 reachable.
- Timebox: 30 minutes.
- Prediction (i): unreachable, terminating. (p ≈ 0.70; **p ≈ 0.10 a
  real violation** — an honest key made to vouch for bytes it never
  signed with every check present: an amendment trigger on the
  verifier specification, not a recut; p ≈ 0.20 timeout — the
  correspondence over a seven-field frame with two chosen-message
  issuers is the widest term space in the ladder.)
- Prediction (ii): **violation, as registered** (p ≈ 0.85; p ≈ 0.10
  unexpectedly unreachable — which would mean the impersonation path
  is missing from the fixture, a *model* defect to be fixed before (i)
  is believed; p ≈ 0.05 timeout).

**S-P1.Q3 — broken companion A: signature not bound to the presented
bytes (the required bytes-substitution companion).** Mutation, in the
Q2 form: the verifier checks that `sg` verifies under `kX` to
`(BYTES, fbSigned)` for *some* `fbSigned` but does not require
`fbSigned = fb` — it verifies a signature and returns the presented
bytes (the detached-signature integrity bug, made explicit). All
other checks unchanged. Required result: headline (i) **red** — the
adversary takes an honest `sign((BYTES, fb), skI)` and presents `fb'`
with the same frame fields and a different payload; `HonestAccepted`
must remain **reachable** in the same model.
- Timebox: 15 minutes.
- Prediction: violation found, trace readable, `fb' ≠ fb` visible in
  the trace. (p ≈ 0.80; p ≈ 0.10 the companion cannot be made to go
  red — under the Grok panel criterion an amendment trigger, since it
  would mean the theory cannot express the alteration threat, not a
  shrug; p ≈ 0.10 timeout.) Trace-inspection rule: a trace in which
  the issuer was simply *asked* to sign `fb'` is not a violation (the
  correspondence would be satisfied); the recorded red must show
  `fb'` absent from every `IssuerSigned`.

**S-P1.Q4 — broken companion B: frame fields outside the signature.**
Mutation, in the Q2 form: the issuer signs the *payload* alone
(`sign((BYTES, payload), skI)`); the verifier reconstructs `fb` from
presented frame fields and the verified payload, checking the frame
fields against the manifest as before. Required result: headline (i)
**red** — the adversary alters an unsigned frame field the verifier
does not pin to the manifest (canonicalization version or object type,
which S-P3 F7 found bound-but-unchecked) while the payload signature
still verifies; `HonestAccepted` reachable.
- Timebox: 15 minutes.
- Prediction: violation found. (p ≈ 0.80; **p ≈ 0.10 a companion that
  could not fail** — only if S-P1's verifier diverges from the S-P3
  verifier this plan says it reuses: in that verifier
  (`sp3_q2_degraded_compromised.pv` line 108, `let framed(ot, =alg,
  =id, =fp(kX), mh, cv, pl) = fb`) `ot` and `cv` are unpinned, and
  F7 records both as unbound-or-removable without effect, so the
  cited record already rules out "the manifest checks pin every frame
  field" for the reused verifier; should it happen anyway the
  companion is green for a reason unrelated to P1 (S-P3 F3's pattern),
  the recorded disposition is "which frame fields the manifest pins,"
  a ledger line for P7/P8, and the companion is recut to alter a
  field the manifest does not carry; p ≈ 0.10 timeout.) This companion is
  registered in S-P1 because §A3.1 attests the identity of the
  *framed* bytes; it is contestable that its home is P8's framing
  obligation instead, and the clerk records that as a judgment, not a
  ruling.

**Ablation rule (on any timeout):** first, the degraded honest-channel
variant (removes the public `skS`); then drop frame fields from the
payload end toward the binding fields; then reduce to one honest
issuer, recording the loss of N2; re-run and record the break point.
A timed-out query's ledger entry records "mechanism failure at N
fields/issuers," never a property claim.

**Ordering rule:** Q1 (both variants) before Q2; Q2 before Q3 and Q4
(a companion is evidence only against a matching correct form); Q3
before Q4. Companions run in the degraded-compromised form only. No
strict-form bytes-substitution companion exists in the tree: the
strict companion on record (the spike's Q2, `formal/spike/first-link/
RESULTS.md` ledger entry 2, "evidence binds issuer identity only")
severs the first link, not the signature-to-bytes binding, and S-P3's
Q3 is a degraded-mode model (`sp3_q3_companionA_frame_unbound.pv`
line 3), not a strict one. Companions are registered in
degraded-compromised form only on the clerk's judgment that the
attestation-signature check is the same conjunct in both verifiers
(S-P3 precedent: Q3/Q4 degraded-only) — contestable; the alternative
is a strict variant of Q3 with its own timebox and probabilities,
which the author may require at cold read.

## What S-P1 consumes, and from whom (ledger interface, A3.3 fields)

Consumer entries this model will carry, each with producer, shared
term, adversary at the join, severing companion, and residual:

1. **Key binding — complementary to S-P3's ledger entry 1, not
   consumed** (S-P3 producer: `sp3_q2_degraded_compromised.pv`,
   `Reattributed` unreachable). S-P3 covers the bytes axis (honest
   bytes → the signer's key); S-P1 covers the key axis (honest key →
   the bytes that key signed). The headline `AcceptedUnderHonestKey(k,
   fb) ⟹ IssuerSigned(k, fb)` binds the same `k` on both sides, so no
   S-P1 query has a gap that S-P3's fact fills: judge H is keyed on
   honest keys and is blind to honest bytes accepted under an
   adversary key by construction, and no S-P1 query goes red when
   S-P3's link is severed (under S-P3 Q3's mutation the adversary's
   accepted key is its own and S-P1's headline is expected to stay
   green). **This is therefore not an A3.3 cross-model entry**: it
   has no severing companion that fails an S-P1 query, and none is
   claimed. The two facts are composed at the capstone, which must
   carry both queries, since neither alone sees the whole (key, bytes)
   pair. Shared terms: accepted key, framed bytes (the same `framed(…)`
   constructor). Adversary at the join: A1.3 with D-4, sole channel
   compromised. Residual Layer 2: `fp` collision resistance and what
   is fingerprinted (P8); `h` idealization for the manifest hash.
   *Skeptic pass 2026-09-06: this entry was first drafted in A3.3
   cross-model form with S-P3 Q3 as its severing companion; the
   skeptic observed that the recorded expected-failing query belonged
   to S-P3, not S-P1, and the entry was re-labelled. ENUMERATION §2's
   "consumes key-binding from S-P3" and `formal/COVERAGE-MAP.md` row 1
   "Consumes SP3 ledger entry 1" are not borne out by the drafted
   queries — ROUTED item 2.*
2. **First link (strict mode only) — consumed from the spike
   (`formal/spike/first-link/`, ledger entry 1) as re-established by
   S-P3 Q1(ii).** Assumed fact: strict acceptance implies an
   uncompromised channel published the accepted tuple (A1.3 "never
   all", n = 2 enumerated, not generalized). Used by Q1(i) only; Q2
   consumes nothing from it (the sole channel key is public, S-P3
   F6). Residual: as recorded there.
3. **Cross-formalism join — `Accept` ↔ P4 verdict partition (not
   symbolically dischargeable).** Assumed fact: every symbolic path
   that stops short of the acceptance event lands in `INVALID` or
   `UNVERIFIABLE` in P4's model, never in a valid verdict; and
   `Accept` in strict / `AcceptS` in degraded mode correspond to
   `VALID_STRICT` / `VALID_DEGRADED` respectively, the latter only
   under an explicit recorded waiver (`DegradedNeedsExplicitWaiver`).
   Producer: `formal/tla/P4_VerifierStates.tla`, invariants named in
   the Target section. Shared term: the acceptance predicate ("every
   required check passes"). Carried in the written proof and the
   coverage map (`formal/COVERAGE-MAP.md`, PROPOSED 2026-09-06,
   untracked, row 1; bytes → P1, Amendment 3 §A3.1 item 3); **never
   marked discharged by any symbolic query** (ENUMERATION §4 — the
   checkmark-relay defect is a red-bar condition).

S-P1 consumes nothing from S-P7: object type is an opaque frame field
here (Q4 alters it without interpreting it); S-P7's producer entries
naming S-P1 as a consumer (`formal/suite/s-p7/PREDICTIONS.md`,
PROPOSED, same day) are S-P7's claim, not carried here. If library
divergence D-5 (object-type constants) proposed there is entered
before S-P1 runs, Q4's altered field becomes a library constant
rather than S-P3's model-local `objTypeH`; the query is unchanged.

Producer entries this model will supply:

4. **Integrity / authorship correspondence (producer: Q2(i),
   `AcceptedUnderHonestKey ⟹ IssuerSigned`).** Consumers: S-P2 (each
   accepted signature covers the exact framed bytes; S-P2 extends the
   fact to every required signer and to the signed required set);
   S-P7 (a wrapper's commitment to the inner package's exact bytes
   presupposes "accepted bytes = signed bytes" for the inner
   signature); the capstone's last link ("accepted signature verifying
   under that key → the exact framed bytes", §A3.2 chain); the
   relying-party story's can-establish line ("this valid package
   reconstructs the same framed bytes recorded at issuance"). Shared
   terms: accepted key, framed bytes. Adversary at the join: A1.3
   items 1–6 with D-4, sole channel compromised. Severing companion:
   Q3 (signature unbound from presented bytes) → headline red.
   Residual Layer 2: signature unforgeability (Dolev–Yao; the
   verification profile is P3's [assumption] half, H1a);
   deterministic signatures (judge equates more than a byte-level
   judge — conservative); **canonical encoding — P8's injectivity
   obligation** (term equality stands in for canonical-byte equality
   until P8's proof exists; then this entry cites the proof, never
   silently absorbs it); `h` idealization; frame layout (P8);
   implementation fidelity.

Layer 2 residuals exposed by this model, collected: concrete hash
collision resistance (manifest hash); canonical encoding / framing
injectivity (P8, pre-proof); fingerprint collision resistance (via
entry 1); signature unforgeability and the verification profile
(H1a); implementation fidelity. Enumerated, exposed, unclaimed.

## What this plan does not claim

- The verdict partition, or anything about `INVALID` /
  `UNVERIFIABLE` — P4 (scope ruling quoted above).
- Freshness, uniqueness, or context of an acceptance — replay is
  permitted (§A3.1 item 1); the correspondence is non-injective by
  registration.
- That the accepted key belongs to an honest issuer in
  degraded-compromised mode — reachable by construction, registered
  red in Q2(ii), the waiver cost handed to the verifier (ruling
  location in Q2).
- Re-attribution of honest bytes to another key — S-P3's;
  complementary, composed at the capstone, not consumed here.
- Multi-signer completeness — S-P2's.
- That `framed(…)` is the P8 frame, or anything about canonical byte
  layout or encoding ambiguity — P8's.
- Cross-type confusion or wrapper re-serialization — P7's.
- Semantic validity, truth, or authority of anything in the bytes —
  outside the attestation (§A3.1).
- Any temporal claim — P5/P6.

## ROUTED TO AUTHOR

1. **What moves P1's tracker row.** `formal/PROPERTIES.md` lists P1's
   tool as "TLA+ and ProVerif" with one status cell. Under the
   2026-08-29 ruling the claim has two legs and a join. Does `checked`
   for P1 require (a) S-P1's correct models green with companions red,
   plus (b) P4's model as already `checked`, plus (c) the `Accept` ↔
   P4 join carried in the coverage map (`formal/COVERAGE-MAP.md`,
   PROPOSED 2026-09-06, untracked, whose draft row 1 already names
   the join) — or does the row wait for the capstone, where §A3.3
   says cross-model links are discharged? The clerk's reading is
   (a)+(b)+(c) with the row's artifact cell naming both models and
   the map; the row is the author's to move.

> *Disposition (clerk), 2026-09-06 — settled from the record, not routed; listed for veto in `formal/suite/ROUTED-2026-09-06.md` §B.* By the tracker's status definitions (`checked` = tool passes) and the 2026-08-29 Question 2 ruling (every claim ≥ one leg; overlapping legs must agree), P1 is `checked` when (a)+(b) hold and (c) is written; `discharged` adds the cross-family review and the author's read. The capstone discharges ledger links, not tracker rows. The row move itself remains the author's commit. (B2)
2. **Two records say S-P1 consumes S-P3's key binding; the drafted
   queries do not.** `ENUMERATION.md` §2 ("Expected ledger: consumes
   key-binding from S-P3") and `formal/COVERAGE-MAP.md` row 1
   ("Consumes SP3 ledger entry 1") both name a consumption that ledger
   entry 1 above records as complementary, not consumed (no S-P1
   query fails when the link is severed). Both need an amendment note
   if this plan's reading stands; alternatively the author may require
   an S-P1 query that actually consumes the link (a bytes-keyed judge,
   which is S-P3's `Reattributed` restated, with S-P3 Q3 as the
   companion that reddens it). Clerk's judgment: the former — a
   restated query proves nothing S-P3 has not.

> *Disposition (clerk), 2026-09-06 — settled from the record, not routed; listed for veto in `formal/suite/ROUTED-2026-09-06.md` §B.* The former. ENUMERATION gains amendment note 6 (PROPOSED) recording S-P1/S-P3 as complementary axes composed at the capstone; coverage-map row 1 is corrected to match. (B3)

## Review log

- 2026-09-06 — drafted by the AI collaborator from ENUMERATION.md
  (with notes 1–5 and the 2026-08-29 dispositions), S-P3's
  PREDICTIONS.md and RESULTS.md (suite rules; F7), the shared library,
  Amendment 1 P1–P10 and A1.3, and Amendment 3 §A3.1–§A3.3. No S-P1
  model has been written or run; no scratch run was made. The
  headline query's shape (honest-key-restricted correspondence via a
  private-channel judge) is registered here untested, and the
  Q1/Q2/Q3 probabilities lean on S-P3's identical fixture having
  terminated in seconds.
- 2026-09-06 — skeptic pass (AI reviewer, findings verified against
  sources by the AI collaborator; corrected in place before first
  commit). Three defects: the ordering rule mis-cited S-P3 Q3 (a
  degraded model) and the spike's Q2 (a first-link companion) as
  strict-form bytes-substitution evidence — no such companion exists,
  now stated with the clerk's degraded-only judgment marked
  contestable; consumer ledger entry 1 was in A3.3 cross-model form
  while its recorded expected-failing query belonged to S-P3 —
  re-labelled complementary, ROUTED item 2 added; choice 2's
  "Dolev–Yao tautology" parenthetical was false under the library's
  D-4 rule for adversary-held derived keys — replaced. Nits applied:
  F7's carried-field assignments restated as F7 gives them; Q4's
  "could not fail" hedge reduced to the verifier-divergence case with
  `sp3_q2` line 108 cited; P4 invariant set aligned with the coverage
  map and the map cited by path and status; the S-P7 non-consumption
  stated; line 112's "one place" corrected to "the same judge
  mechanism". No query, timebox, or outcome vocabulary changed; Q4's
  probabilities moved (0.65/0.25/0.10 → 0.80/0.10/0.10) before
  freeze, which is a draft revision, not a divergence.
