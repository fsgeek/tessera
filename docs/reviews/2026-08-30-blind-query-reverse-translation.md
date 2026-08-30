# Blind reverse-translation of the first-link ProVerif models

**Status: non-author review artifact, 2026-08-30. Non-discharging.**
Method proposed the same day by a blind project-level reviewer (a
Claude instance outside this harness): *a model that sees only the
ProVerif code, no prose, writes back the English claim it believes
each query proves; diff that against the registered invariant;
divergence is a finding either way.* This closes the unaudited link
the reviewer named — English invariant → query encoding → green
result — from a direction the author's own read cannot supply, and
does so without the author.

## Method and blindness

- **Input:** the seven distinct first-link models
  (`q1_chain_dns_compromised`, `q2_broken_dns_compromised`,
  `q3_mechanism_dns_compromised`, `q4_attack_dns_compromised`,
  `q5_single_dns_compromised`, `q6_single_dns_compromised`,
  `q7_asym_dnsweak`), with **every comment stripped** and the files
  renamed `model_1.pv` … `model_7.pv`. The repository-compromise
  mirrors and the honest single-evidence variants were not supplied;
  they differ from these only by which key is leaked or none.
- **Reader:** a fresh agent on Claude Opus — a different model from
  the clerk that wrote the models' prose — instructed to read only
  those seven files, not to search or open anything else on the
  machine, and not to infer purpose beyond what the code forces.
  **Blindness was by instruction, not enforcement**; the agent's
  transcript reports seven tool uses, all reads of the supplied files.
- **Output:** per model, the setup in plain English, the claim each
  query proves if "true," what it does not say, which verifier checks
  are load-bearing, and oddities; then a cross-model synthesis. The
  full output is Appendix A, verbatim.
- **Diff:** performed by the clerk (Claude, this harness) against the
  registered claims — A3 §A3.2 chain, §A3.2.1 boundary invariant,
  the 2026-08-09 recut (RESULTS.md finding 1), the 2026-08-12 author
  review, DECISION.md — and against this session's guide findings.

## Diff against the registered claims

| Model | Registered claim (record) | Blind reading (Appendix A) | Diff |
|---|---|---|---|
| Q1 chain | Accept ⇒ at least one **uncompromised** channel published this exact tuple ∧ possession(k) ∧ signed(k, fb) (recut, RESULTS.md finding 1) | "at least one of the two authorities had published about that same record `t` … even though the adversary holds the DNS key"; notes the DNS half "carries zero information" so the property is carried by the honest channel | **Agrees.** The blind reader states the recut's content — the disjunction is really "the honest one" — without having seen the recut. |
| Q2 broken | Binding issuer identity only permits a two-worlds witness on a map-v1 field (RESULTS.md Q2 instantiation: key fingerprint) | Both queries fail; the attack "needs no forgery and no compromised key at all"; the differing field is any field the statement does not cover | **Agrees**, and restates RESULTS.md finding 2 (compromise not needed) independently. |
| Q3 mechanism | Same correspondence as Q1 with `h(t)`; `h` injective is a Layer 2 residual (ledger 1); author finding 3: Q3 proves nothing Q1 does not | "`=h(t)` is exactly equivalent to `=t`… models 3 and 1 are the same model… the check is vacuous — the algebra assumed the answer" | **Agrees**, and is author finding 3 verbatim in substance. |
| Q4 attack | `TwoWorldsBroken` unreachable with the mechanism intact (criterion 0, leg 1) | Unreachable; "it is a 'there is only one record' property" — the judge never exercises the interesting case because only `tH` exists | **Agrees on the result; adds a scope qualification** (new finding N2). |
| Q5b degraded, compromised | Registered red: no provenance survives when the sole channel is compromised | All three conjuncts fail at once; "the verifier accepts a record about a key the honest issuer never held, carrying a payload the honest issuer never signed" | **Agrees**, and matches the guide's B5 ("the waiver cost is total"). |
| Q6b single two-worlds | Unreachable even under compromise of the accepted channel; unconditional (ledger addendum 6) | Unreachable; "key compromise… lets the adversary mint a statement for any record, but each minted statement is bound to exactly one record" | **Agrees**, including the unconditional character. |
| Q7 contrast | Single reachable, Pair unreachable; the pair-judge blind spot mechanized | Exactly that contrast; "the variable that matters is what the statement covers, not how many statements there are" | **Agrees**, and adds that `VerifierP`'s DNS check is load-bearing for nothing (new finding N3). |

**No divergence.** Every "true" and every "false" the blind reader
predicted from the code alone matches the committed `.out` files, and
every English sentence it wrote for a green result is the registered
claim or narrower. The registered prose does not overclaim relative to
the code on any of the seven.

## Independent corroboration of this session's findings

- **The possession check is redundant in every correct model.**
  Appendix A, model 1 §4 and the synthesis: "the proof-of-possession
  check is load-bearing for nothing in any of the seven (in models 1
  and 3 it is strictly redundant given the ordering of `event
  IssuerPossession` before `event IssuerSigned`)." This is the guide's
  headline (M1), reached by reading rather than by mutation, by a
  different model, blind. The guide's *correction* — that the spike
  under-encoded possession relative to A1.5 item 3 — is not something
  the code alone could show, and the blind reader did not reach it;
  that is the expected limit of the method.
- **`h(t)` ≡ `t`** — author finding 3, reached blind.
- **`label`, `ss`, `alg`, `ver` carried and never compared** — author
  finding "bound but not semantically validated," reached blind.
- **Non-injective correspondence: replay outside scope** — guide B1.
- **`AuthorityPublished*` fires unconditionally** ("certifies only that
  this process exists… not that an authority evaluated and endorsed") —
  the guide's C4 (registration is not modeled), from the other side.

## New findings (not previously in the record)

**N1 — No sanity/reachability query on `Accept` exists in any model.**
"A verifier replaced by `0` would satisfy every 'true' result here."
The TLA+ side of Band 0 registers vacuity witnesses that must fire;
the ProVerif side did not. The spike's `.out` files do show `goal
reachable` derivations for the green correspondences, which is
evidence of reachability in the abstraction, and the guide's M1b
showed the *absence* of such a line as the vacuity tell — but nothing
registered required anyone to look. **Disposition (PROPOSED):** every
model in the symbolic suite carries a registered reachability query
on its acceptance event, expected `not event(Accept…) is false`
(reachable), as the ProVerif analogue of the TLA+ vacuity witness;
added to ENUMERATION.md §5 by amendment note 3. Retrofit to the
first-link models is not proposed — their `.out` files are committed
evidence and the goal lines are present — but the guide gains a
postscript pointing here.

**N2 — One honest tuple, one honest key, one honest payload.** "Every
'with the same `t`/`k`/`fb`' clause is matching values from a
one-element set." The guide's M4 added a second issuer and the
property held, but that was a scratch run, not a registered model.
Q4's unreachability in particular is carried by there being only one
acceptable record. **Disposition (PROPOSED):** suite models carry at
least two honest values on every axis the query binds (two issuers,
two payloads, two tuples on the honest channels), so agreement
clauses have content; added to ENUMERATION.md §5.

**N3 — In Q7, `VerifierP`'s DNS check pins nothing.** The "paired"
verifier's weak-bound DNS check contributes nothing to
`TwoWorldsPair`'s unreachability; the repo `h(t)` check alone carries
it. This is consistent with the contrast's purpose (the pair judge's
blind spot) and is not a defect in the registered result, but a
reader of "the pair judge stays green" should know that "pair" here
means "one strong check plus one inert one." **Disposition:** recorded
here; a sentence for the relying-party story's account of strict mode
under an asymmetric channel weakness.

**N4 — Model 7 never cross-checks its two verifiers.** The sound and
the unsound verifier run concurrently and their acceptances are never
compared. By design (the contrast is two judges), but the blind reader
is right that the set "never asks whether a broken verifier's
acceptance and a sound one's can contradict each other in the same
run." **Disposition:** noted; the integrated lifecycle model (A3 §A3.9,
Kimi-2) is where verifier-vs-verifier questions belong.

## What this artifact is and is not

It is a check that the registered English does not overclaim the
code, performed by a party that could not have been told what the
English was. It is not a check that the code encodes the *design* —
the possession under-encoding shows exactly that gap: a blind reader
of the code will faithfully report a redundant check and cannot know
that the design's object was richer than the model's. The two
directions — code → English (this artifact) and record → code (the
guide's correction) — are different audits, and Band 0 needs both.

It does not discharge anything. The prose-mapping obligation in
`PROPERTIES.md` ("every symbolic lemma carries a prose mapping to its
A1.2 property") remains open; this is evidence toward how that
obligation can be met without the relay pattern, not the meeting of
it.

## Provenance

Method: blind project-level reviewer, 2026-08-30 (Claude, other
harness). Preparation of the stripped inputs, dispatch, and this diff:
the clerk (Claude, this harness), who has read all of the record and
is therefore not blind. Reader: Claude Opus, fresh, blind by
instruction. The author has not yet read Appendix A.

---

## Appendix A — the blind reader's output, verbatim

> I read all seven files and nothing else. Write-up follows.

---

# Blind reverse-translation of seven ProVerif models

## Shared vocabulary (identical in all seven files)

Before the per-model sections, the primitives, because every model uses the same ones and the modelling choices in them drive most of my caveats.

```
fun sign(bitstring, skey): bitstring.
reduc forall m: bitstring, k: skey; checksign(sign(m, k), pk(k)) = m.
fun fp(pkey): bitstring.
fun h(bitstring): bitstring.        (models 3,4,5,6,7 only)
```

- **`sign`/`checksign`** is a signature-with-message-recovery. `checksign` is a *public* destructor and every `pk(sk)` is published, so the adversary can read the signed payload out of any signature it sees. The only way any term `s` can satisfy `checksign(s, pk(k))` is if `s` is literally `sign(m, k)`. Forgery is therefore *impossible by construction*, not merely hard.
- **`sign` is a free constructor**: `sign(m1,k1) = sign(m2,k2)` implies `m1=m2` and `k1=k2`. So one signature term cannot verify under two different public keys, cannot be mauled, and is deterministic (no randomised signatures, no two signatures on the same message).
- **`pk`, `fp`, `h` are free constructors with no equations**: they are *injective*. `fp(k1)=fp(k2)` **forces** `k1=k2`; `h(t1)=h(t2)` **forces** `t1=t2`. Fingerprint collisions and hash collisions are not merely hard in these models — they are not expressible. This is the single most important thing to hold onto when reading any "true" result below.
- **Tupling is free and injective**: `(a,b,c,d,e)` is a transparent 5-tuple the adversary can build and take apart at will.

Every model builds the same honest record:

```
let tH = (issuerId, fp(pk(skI)), ssetH, algH, verH) in
```

`issuerId`, `ssetH`, `algH`, `verH`, `fbH` are all `free` — public. `fp` is public and `pk(skI)` is published. **So the adversary can compute `tH` itself.** There is exactly one honest record value and exactly one honest payload value (`fbH`) in the entire universe of every model.

Nowhere in any of the seven files is there a secrecy query (`query attacker(...)`), and nowhere is there a sanity/reachability query on `Accept` — I come back to that at the end.

---

# Model 1 — two authorities sign the whole record; DNS signing key is handed to the adversary

## 1. Setup, in plain English

**Fresh secrets:** `new skD`, `new skR`, `new skI` — three signing keys, for a "DNS" authority, a "Repo" authority, and an "Issuer".

**Given to the adversary before anything runs:**

```
out(c, pk(skD)); out(c, pk(skR)); out(c, pk(skI));
out(c, skD);
```

All three public keys — and **`skD`, the DNS authority's private signing key**. From line 53 onward the adversary can mint any DNS statement it likes. This is deliberate: the model is asking what survives when one of the two authorities is fully compromised.

**Parties (all replicated, `!`, so unboundedly many instances):**

- `AuthorityDNS(skD, tH)` — fires `event AuthorityPublishedDNS(tH)`, then publishes `sign((STMT, tH), skD)`: a signature over the **entire record**.
- `AuthorityRepo(skR, tH)` — fires `event AuthorityPublishedRepo(tH)`, then publishes `sign((STMT, tH), skR)`: same statement, other key.
- `Issuer(skI, fbH)` — fires `event IssuerPossession(pk(skI))`, publishes `sign((POSS, fp(pk(skI))), skI)` (a self-signed proof-of-possession over its own fingerprint); then fires `event IssuerSigned(pk(skI), fbH)` and publishes `sign((BYTES, fbH), skI)` (a signature over the payload).
- `Verifier(pk(skD), pk(skR))` — reads an 8-field bundle off the public channel and runs the checks below.

**What the verifier checks, in order** (lines 40–47):

1. `let (=STMT, =t) = checksign(evD, pkD)` — *"`evD` must be the DNS authority's signature over the tag `STMT` paired with exactly the record `t` I was handed."*
2. `let (=STMT, =t) = checksign(evR, pkR)` — same, under the Repo authority's key.
3. `let (id, kfpr, ss, alg, ver) = t` — *"`t` must be a 5-tuple"*; only `kfpr` is subsequently used.
4. `if fp(kX) = kfpr` — *"the fingerprint of the presented key equals the fingerprint recorded in the record."*
5. `let (=POSS, =fp(kX)) = checksign(ppf, kX)` — *"`ppf` is a self-signature under `kX` over `(POSS, fp(kX))`"* — i.e. whoever holds `kX`'s private half asserted possession.
6. `let (=BYTES, =fb) = checksign(sg, kX)` — *"`sg` is a signature under `kX` over `(BYTES, fb)`"*.

Then `event Accept(evD, evR, t, kX, fb)` and stop.

**What this forces.** Check 2 is the pin: the Repo authority only ever emits `sign((STMT, tH), skR)`, so `t = tH`, hence `kfpr = fp(pk(skI))`, hence by injectivity of `fp` check 4 gives `kX = pk(skI)`, hence check 6 (the Issuer only signs `fbH`) gives `fb = fbH`. Every accepted bundle has `t = tH`, `kX = pk(skI)`, `fb = fbH`.

## 2. What the query claims if ProVerif says "true"

```
event(Accept(evD, evR, t, k, fb)) ==>
  ( (event(AuthorityPublishedDNS(t)) || event(AuthorityPublishedRepo(t)))
 && event(IssuerPossession(k)) && event(IssuerSigned(k, fb)) ).
```

I expect **true**, and the sentence it licenses is:

> Whenever the verifier accepts a bundle carrying record `t`, key `k` and payload `fb`, then earlier in the same run at least one of the two authorities had published about **that same record `t`**, the issuer had asserted possession of **that same key `k`**, and the issuer had signed **that same payload `fb`** — and this holds even though the adversary holds the DNS authority's private signing key.

## 3. What the claim does NOT say

1. **Nothing about freshness or replay.** The correspondence is non-injective (`==>`, not `==> inj-event`). One run of the Issuer supports unboundedly many `Accept`s. There is no nonce, no timestamp, no revocation, no ordering constraint between the two authorities' events, and no requirement that they be recent. An acceptance today is backed by a publication that may have happened arbitrarily long ago, arbitrarily many acceptances ago.
2. **"AuthorityPublished" does not mean an authority decided anything.** `event AuthorityPublishedDNS(t)` is the *first statement* of an unguarded, replicated, input-free process. The adversary can cause it to fire simply by letting the process be scheduled. It is an unconditional event; it certifies only "this process exists in the model", not "an authority evaluated and endorsed `tH`".
3. **The agreement clauses are barely tested.** There is exactly one honest record (`tH`), one honest key (`pk(skI)`), one honest payload (`fbH`) in the whole model. "With the same `t`/`k`/`fb`" is a statement about matching values drawn from a one-element set. A model where the Issuer read `fb` off the channel (`in(c, fb)`) would actually exercise the binding; this one cannot distinguish "the right payload" from "the only payload".
4. **Nothing ties `evD`/`evR` to the authorities.** They are arguments of `Accept` but appear nowhere in the conclusion. The property is silent on the provenance of the evidence blobs themselves.
5. **The disjunction is weak, and its DNS half is worthless here.** `||` means *either* authority suffices. Since `skD` is public, the DNS half of the conclusion carries zero information — the property is really carried entirely by `AuthorityPublishedRepo`. A reader seeing "two independent authorities" in the process list should not read the green result as "two independent attestations were required".
6. **The algebra makes the interesting attacks unrepresentable.** No fingerprint collision (`fp` is injective), no hash of any kind here, no signature that verifies under two keys, no key-substitution/DSKS attack, no malleability, no weak-key or same-signature-different-message case. The result "the fingerprint check pins the key" is a theorem about ProVerif's term algebra, not about SHA-256.
7. **No secrecy is claimed anywhere.** There is no query about `skI`, `fbH`, or anything else. And there is no claim that the verifier ever accepts anything at all (see §5 and the closing section).

## 4. Which verifier checks are load-bearing

| Check | Delete it? | Why |
|---|---|---|
| `let (=STMT, =t) = checksign(evD, pkD)` (line 40) | **No change.** | `skD` is published at line 53, so the adversary can satisfy this for any `t` whatsoever. It already constrains nothing; and `evD` never appears in the query's conclusion. This check is pure decoration in this model. |
| `let (=STMT, =t) = checksign(evR, pkR)` (line 41) | **Result flips to false.** | This is the *only* thing forcing `t = tH`. Delete it and the adversary supplies `t' = (anything, fp(pk(skI)), ssetH, algH, verH)`, reuses the honest `ppf`/`sg`, and `Accept(_,_,t',…)` fires while `AuthorityPublished{DNS,Repo}(t')` never fired. |
| `let (id, kfpr, ss, alg, ver) = t` (lines 42–43) | **No change — and it can never fail.** | After line 41, `t` is already forced to be `tH`, which *is* a 5-tuple. The pattern match is unfalsifiable at this point in the process. |
| `if fp(kX) = kfpr` (line 44) | **Result flips to false.** | Without it the adversary generates its own `skA`, presents `kX = pk(skA)` with self-made `ppf` and `sg`, and `Accept(…, pk(skA), fb')` fires with no `IssuerPossession(pk(skA))` anywhere. |
| `let (=POSS, =fp(kX)) = checksign(ppf, kX)` (line 45) | **No change — redundant for this query.** | The next check already requires a signature under `skI`, which forces the `Issuer` process to have run *past* line 35 (`event IssuerSigned`), which is after line 33 (`event IssuerPossession`). The possession proof buys nothing the payload signature does not already buy. I am fairly confident of this; the sequencing at lines 33–36 is what makes it so, and it would stop being true if the Issuer could sign payloads without having first emitted the possession proof. |
| `let (=BYTES, =fb) = checksign(sg, kX)` (line 46) | **Result flips to false.** | It is the only thing forcing `fb = fbH` and hence `IssuerSigned(k, fb)`. |

So: two of the six checks (the Repo evidence check and the fingerprint check) plus one (the payload signature check) carry the whole result; the DNS check, the tuple destructuring, and the proof-of-possession are inert.

## 5. Oddities

- **`label: bitstring` is bound in the input on line 38 and never mentioned again.** A field carried through the protocol and never compared to anything.
- **`id`, `ss`, `alg`, `ver` are bound on lines 42–43 and never used.** The verifier never checks that the record's identifier equals `issuerId`, nor anything about the "sset"/"alg"/"ver" fields. Only `kfpr` is read.
- **The two authorities sign byte-identical statements** (`sign((STMT, t), skD)` vs `sign((STMT, t), skR)`); the only difference is the key. There is no sense in which they attest *independently*, and no check that they agree — agreement is structural, not verified.
- **`evD` and `evR` are recorded in the `Accept` event but constrained by nothing in the query.** The first two arguments of `Accept` are inert.
- **There is no reachability query.** Nothing in the file establishes that `Accept` can ever fire. A verifier that rejected every input would satisfy this query just as "true".

---

# Model 2 — same as model 1, except the authorities sign only the record's *identifier*; plus a "two worlds" judge. Both queries fail.

## 1. Setup

Identical to model 1 (same keys, same `out(c, skD)` leak, same `tH`), with three changes:

- A private channel `free accCh: channel [private]` — the adversary cannot write to it, so only genuine verifier acceptances reach the judge.
- **The authorities now destructure `t` and sign only its first component:**
  ```
  let (id, kfpr, ss, alg, ver) = t in
  out(c, sign((STMT, id), skD)).     (and the same for skR)
  ```
  The statement covers `issuerId` and nothing else — not the key fingerprint, not `ss`, `alg`, or `ver`.
- A new party `Judge`, which reads two acceptance records off `accCh`, requires them to carry the **same** `(evD, evR)` pair, and fires `event TwoWorldsBroken(e1, e2, t1, t2)` if their records `t1`, `t2` differ.

**Verifier checks, in order** (lines 48–54): destructure `t` into five fields *first*; then `let (=STMT, =id) = checksign(evD, pkD)`; then the same under `pkR`; then `if fp(kX) = kfpr`; then the possession check; then the payload check. Then `event Accept(...)` and `out(accCh, (evD, evR, t))`.

**What this forces — almost nothing.** The evidence now pins only `id`. The adversary reuses the two honest signatures `sign((STMT, issuerId), skD/skR)` and supplies **any** record whose first field is `issuerId`.

## 2. What the queries claim

**Query 1** is verbatim model 1's correspondence. I expect **false**. The attack needs no forgery and no compromised key at all: submit `t' = (issuerId, fp(pk(skI)), ssetH, algH, X)` for any adversary-chosen `X`, with the honest `evD`, `evR`, `ppf`, `sg` and `fb = fbH`. Every check passes; `Accept(evD, evR, t', pk(skI), fbH)` fires; but `AuthorityPublishedDNS(t')` and `AuthorityPublishedRepo(t')` never fired — the authorities only ever fire with `tH`. The witnessed failure is precisely: *the accepted record is not the record any authority published.*

**Query 2**, `query …; event(TwoWorldsBroken(evD, evR, t1, t2)).` — this is a **reachability** query. ProVerif reports `not event(TwoWorldsBroken(...)) is true` if the event is unreachable (good), `is false` with an attack trace if it is reachable (bad). I expect **false**. Run the verifier twice with the same `(evD, evR)` and two records `t1 = tH`, `t2 = (issuerId, fp(pk(skI)), ssetH, algH, X)`; both are accepted, both reach the judge, `t1 ≠ t2`, the event fires. Stated as the property that *fails*:

> One and the same pair of authority statements can be presented alongside two different records and be accepted for both — the evidence does not determine what it is evidence *for*.

## 3. What the (failed) results do NOT say

Since both queries fail, the honest reading is about what the counterexamples do and don't cover:

1. **The failure is not about key compromise.** The `out(c, skD)` leak on line 66 is present but *irrelevant* to both attacks — both work with entirely honest authority keys, using only signatures the honest authorities freely published. A reader who blames the leak has misdiagnosed it; the cause is the *scope of the signed statement*.
2. **The failure is not about the issuer, the fingerprint check, or the proof of possession.** The winning trace uses the genuine `pk(skI)`, the genuine possession proof, and the genuine payload signature. Every issuer-side check passes honestly. The break is entirely on the authority side.
3. **`TwoWorldsBroken` firing does not mean the adversary learned any secret**, forged any signature, or made the verifier accept a *bad payload*. In the trace above `fb = fbH` and `kX = pk(skI)` both times. It means only that the *record* is unpinned.
4. **The judge only detects a divergence when the two acceptances carry a byte-identical `(evD, evR)` pair.** Two acceptances of different records backed by *different* evidence pairs are invisible to it. So `TwoWorldsBroken` being unreachable (in models 4/7) would be a narrower guarantee than "the verifier never accepts two contradictory records".
5. **`accCh` is `[private]`.** The judge is guaranteed to see only genuine acceptances. That is a modelling gift: it is what makes the two-worlds question meaningful rather than trivially breakable by the adversary posting whatever it likes.

## 4. Which verifier checks are load-bearing

Both queries are already false, and deleting a check can only *add* traces, so **no deletion can change either result.** The informative question is the reverse — which *addition* fixes it:

- `let (=STMT, =id) = checksign(evD, pkD)` (line 50) — inert, twice over: `skD` is public *and* `id` is a public free name.
- `let (=STMT, =id) = checksign(evR, pkR)` (line 51) — the weak link. Strengthening it to `=t` (model 1) or `=h(t)` (models 3/4) makes both queries true. As written it pins one field out of five.
- `let (id, kfpr, ss, alg, ver) = t` (lines 48–49) — now genuinely falsifiable (it constrains `t` to be a 5-tuple), unlike in model 1, but the adversary satisfies it trivially.
- `if fp(kX) = kfpr` (line 52) — constrains `kX` *relative to the adversary's own chosen `kfpr`*, so it constrains nothing absolute. It is a consistency check between two adversary-supplied values.
- possession check (line 53) and payload check (line 54) — pass honestly in the attack; irrelevant to both failures.

## 5. Oddities

- **`if fp(kX) = kfpr` has become self-referential.** Once `kfpr` comes from an unpinned, adversary-supplied `t`, the check is "the adversary's key matches the fingerprint the adversary wrote down". Under the declared algebra it reduces to: *the adversary must know some private key*. Nothing more.
- **`label` is still bound and still unused** (line 46).
- **`ss`, `alg`, `ver` are still never compared** — and here that matters, because they are exactly the fields the evidence no longer covers.
- **The judge's `if t1 = t2 then 0` branch** silently discards the common case; the event is only in the `else`. Fine, but it means the judge is a pure detector with no positive signal.
- **`event Accept` remains the query-1 subject, but in a model where query 1 is expected to fail**, the file is doing double duty: it is simultaneously the negative control for model 1's correspondence and the negative control for model 4's reachability query.

---

# Model 3 — model 1 with `h(t)` in place of `t` in the authority statements

## 1. Setup

Byte-for-byte model 1, plus `fun h(bitstring): bitstring.` (line 8), with the authorities publishing `sign((STMT, h(t)), skD)` / `sign((STMT, h(t)), skR)` (lines 29, 32) and the verifier checking

```
let (=STMT, =h(t)) = checksign(evD, pkD) in
let (=STMT, =h(t)) = checksign(evR, pkR) in
```

Same key leak (`out(c, skD)`, line 54), same `tH`, same issuer, same remaining four checks, same `Accept` event, same correspondence query.

## 2. What the query claims

Identical text to model 1's, and I expect **true**, licensing the same sentence:

> Whenever the verifier accepts a bundle carrying record `t`, key `k` and payload `fb`, then at least one authority had earlier published about that same `t`, the issuer had asserted possession of that same `k`, and the issuer had signed that same `fb`.

## 3. What the claim does NOT say

All of model 1's items 1–7 apply verbatim. Three that are sharpened here:

1. **`h` is a perfect, injective, collision-free function.** It has no equations and no inverse-leaking destructor. `h(t1) = h(t2)` *implies* `t1 = t2` in ProVerif's algebra. So the model literally cannot express a hash collision, a length-extension, a chosen-prefix attack, or a second-preimage. Any real-world argument of the form "an attacker finds a colliding record" is outside the model by construction, not ruled out by it.
2. **Consequently, `=h(t)` is exactly equivalent to `=t`.** Under the declared equations, model 3 and model 1 are the same model. The green result on model 3 is not independent evidence that hashing the record is safe; it is the same theorem, restated. If the intent of the pair (1, 3) was to check that "commit to the hash" is as good as "commit to the record", the check is vacuous — the algebra assumed the answer.
3. **`h` is also not modelled as hiding anything.** Nothing is claimed about `h` being one-way; nothing here needs it to be. `t` is public anyway (the adversary can compute `tH` from public data).

## 4. Which verifier checks are load-bearing

Exactly as model 1, with `h(t)` substituted for `t`:

| Check | Delete it? | Why |
|---|---|---|
| `let (=STMT, =h(t)) = checksign(evD, pkD)` (line 41) | No change | `skD` public (line 54); satisfiable for any `t`. |
| `let (=STMT, =h(t)) = checksign(evR, pkR)` (line 42) | **Flips to false** | Sole pin on `t`; injectivity of `h` is what turns "pins `h(t)`" into "pins `t`". |
| `let (id, kfpr, ss, alg, ver) = t` (lines 43–44) | No change, and can never fail | `t` is already `tH`. |
| `if fp(kX) = kfpr` (line 45) | **Flips to false** | Adversary substitutes its own key pair. |
| `let (=POSS, =fp(kX)) = checksign(ppf, kX)` (line 46) | No change — redundant | Line 47 already forces the Issuer past `event IssuerPossession` (line 34). |
| `let (=BYTES, =fb) = checksign(sg, kX)` (line 47) | **Flips to false** | Sole pin on `fb`. |

## 5. Oddities

- **The load-bearing step is an algebraic identity, not a cryptographic argument.** "The evidence commits to `h(t)`, therefore to `t`" is true here purely because `h` is a free constructor.
- **`label` unused; `id`, `ss`, `alg`, `ver` bound and never compared** — same as model 1.
- **The DNS branch is entirely ornamental** given line 54; the model runs two authorities and relies on one.
- **No reachability query** — again nothing establishes that `Accept` can fire.

---

# Model 4 — model 3 with all correspondence machinery deleted, and only the "two worlds" reachability question asked

## 1. Setup

Model 3, minus every `AuthorityPublished*`, `IssuerPossession`, `IssuerSigned` event and minus the correspondence query; plus `free accCh: channel [private]` and the `Judge` from model 2.

- `AuthorityDNS` is now just `out(c, sign((STMT, h(t)), skD))` — no event.
- `AuthorityRepo` likewise.
- `Issuer` publishes the possession proof and the payload signature — no events.
- `Verifier` runs the **same six checks as model 3** (lines 32–38) and then `event Accept(...)` followed by `out(accCh, (evD, evR, t))`.
- `Judge` reads two records with the same `(e1, e2)` and fires `TwoWorldsBroken` if `t1 ≠ t2`.
- `out(c, skD)` is still present (line 50): the DNS key is still leaked.

## 2. What the query claims

```
query evD, evR, t1, t2; event(TwoWorldsBroken(evD, evR, t1, t2)).
```

Reachability. **`not event(TwoWorldsBroken(...)) is true`** means: no trace anywhere reaches that event — the good outcome. `is false` would mean ProVerif found a trace and the construction is broken. I expect **true**, and the sentence is:

> No two acceptances backed by the same pair of authority statements can ever carry different records: the evidence pair determines the record uniquely, even though the adversary holds the DNS authority's signing key.

In fact something stronger is true and worth stating, because it explains *why*: `evR` must be `sign((STMT, h(t)), skR)`, the Repo authority only ever emits `sign((STMT, h(tH)), skR)`, so **every** accepted record is `tH`. The judge's `t1 ≠ t2` branch is unreachable because there is only one acceptable record in the entire model.

## 3. What the claim does NOT say

1. **It is not a "same evidence ⇒ same record" property; it is a "there is only one record" property.** The model contains a single honest `tH` and a single honest Repo statement. The judge never gets to exercise the interesting case. If the Repo authority published about two different records, the property as written would still hold (different records ⇒ different `evR` ⇒ the judge's `=e1, =e2` pattern never matches) — but that is an artifact of the pattern, not evidence of a real guarantee.
2. **The judge only compares acceptances sharing a byte-identical `(evD, evR)` pair.** Two contradictory acceptances backed by *different* evidence would be entirely invisible. "TwoWorldsBroken is unreachable" is a much narrower statement than "the verifier is consistent".
3. **Nothing is said about `kX` or `fb`.** The judge inspects only `t`. The verifier's key and payload checks contribute nothing to this result (see §4). Two acceptances could differ in key or payload without any event firing — the query would not notice.
4. **Nothing is said about who published, or when.** Every event that could have anchored the acceptance to an honest party has been *deleted* from this file. `Accept` fires but no query mentions it. There is no correspondence claim at all here.
5. **No replay/freshness content whatsoever.** Unbounded replay is not just permitted, it is the mechanism by which the judge gets two records to compare.
6. **The result again rests on injectivity of `h` and of `sign`.** A hash collision on `t` would break it and is unrepresentable.

## 4. Which verifier checks are load-bearing

This model has the most lopsided answer of the seven:

| Check | Delete it? | Why |
|---|---|---|
| `let (=STMT, =h(t)) = checksign(evD, pkD)` (line 32) | **No change.** | `skD` is public (line 50); the adversary can satisfy it for any `t` already. `evD` is unconstrained in practice. |
| `let (=STMT, =h(t)) = checksign(evR, pkR)` (line 33) | **Flips to false.** | The one and only check that pins `t`. Delete it and the adversary presents two arbitrary records with any fixed `(evD, evR)`; the judge fires immediately. |
| `let (id, kfpr, ss, alg, ver) = t` (lines 34–35) | **No change.** | `t` is already pinned to `tH` by line 33; the shape check is unfalsifiable at this point. |
| `if fp(kX) = kfpr` (line 36) | **No change.** | Constrains `kX`, which the judge never examines. |
| `let (=POSS, =fp(kX)) = checksign(ppf, kX)` (line 37) | **No change.** | Same — the judge compares only `t`. |
| `let (=BYTES, =fb) = checksign(sg, kX)` (line 38) | **No change.** | Constrains `fb`, which the judge never examines. |

**Five of the six checks are irrelevant to the query.** The entire green result is carried by line 33.

## 5. Oddities

- **`event Accept(evD, evR, t, kX, fb)` is declared (line 18), fired (line 39), and referenced by no query.** Dead instrumentation — a leftover from model 3.
- **The whole issuer side of the protocol — possession proof, fingerprint binding, payload signature — is present and load-bearing for nothing.** If the goal was to test the two-worlds property in a realistic setting, fine; if a reader takes the green result as validating those checks, they would be wrong.
- **`out(c, skD)` (line 50) does not affect the result.** The DNS key compromise is real but inert: `evD` is unpinned either way, and `t` is pinned by `evR`. This is a genuinely interesting negative finding — the two-worlds property here is robust to compromising *one* authority, but only because the *other* authority's statement covers the whole record.
- **`label` still bound, still unused** (line 30).

---

# Model 5 — single authority, and that authority's key is in the adversary's hands

## 1. Setup

`new skD; new skR; new skI`; `tH` as always; `out(c, pk(skD)); out(c, pk(skR)); out(c, pk(skI)); out(c, skD);` — **`skD` leaked again**.

- `AuthorityDNS` fires `AuthorityPublishedDNS(tH)` and publishes `sign((STMT, h(tH)), skD)`.
- `AuthorityRepo` fires `AuthorityPublishedRepo(tH)` and publishes `sign((STMT, h(tH)), skR)`.
- `Issuer` as before: possession event + `sign((POSS, fp(pk(skI))), skI)`, then signed event + `sign((BYTES, fbH), skI)`.
- **`VerifierS(pk(skD))`** — takes a *7*-field bundle (one evidence blob, not two) and checks, in order:
  1. `let (=STMT, =h(t)) = checksign(ev, pkA)` — one authority statement, under the DNS key.
  2. `let (id, kfpr, ss, alg, ver) = t` — 5-tuple shape; only `kfpr` used.
  3. `if fp(kX) = kfpr`.
  4. `let (=POSS, =fp(kX)) = checksign(ppf, kX)`.
  5. `let (=BYTES, =fb) = checksign(sg, kX)`.

  Then `event AcceptS(ev, t, kX, fb)`.
- The top-level composes `!AuthorityDNS | !AuthorityRepo | !Issuer | !VerifierS(pk(skD))`. **`AuthorityRepo` runs but nothing consumes its output** — the verifier only knows `pk(skD)`.

## 2. What the query claims

```
event(AcceptS(ev, t, k, fb)) ==>
  ( event(AuthorityPublishedDNS(t)) && event(IssuerPossession(k)) && event(IssuerSigned(k, fb)) ).
```

Note this one has **`&&`, not `||`** — it names the DNS authority specifically. I expect **false**.

The attack: the adversary holds `skD` (line 53). It picks any `t' = (x1, fp(pk(skA)), x3, x4, x5)` for a self-generated key `skA`, mints `ev' = sign((STMT, h(t')), skD)`, and supplies `ppf = sign((POSS, fp(pk(skA))), skA)`, `sg = sign((BYTES, fb'), skA)`. All five checks pass. `AcceptS(ev', t', pk(skA), fb')` fires while `AuthorityPublishedDNS(t')` never fired, `IssuerPossession(pk(skA))` never fired, and `IssuerSigned(pk(skA), fb')` never fired. **All three conjuncts fail at once.** The verifier accepts a record about a key the honest issuer never held, carrying a payload the honest issuer never signed.

Stated as the property that *fails*:

> With a single source of evidence, compromising that source's signing key lets an adversary make the verifier accept an entirely fabricated record, key, and payload.

## 3. What the failure does NOT say

1. **It does not say single-source verification is inherently unsound.** The counterexample is driven entirely by line 53, `out(c, skD)`. Remove that one line and I would expect this exact model to verify true — `ev` would pin `h(t)`, hence `t = tH`, hence `kX = pk(skI)`, hence `fb = fbH`. The model demonstrates *"one source plus one compromised key"*, not *"one source"*.
2. **It does not compare the single-source design against the two-source design under equal conditions.** Model 5 leaks `skD` and then relies only on `pk(skD)`; models 1/3 leak `skD` and rely also on `pk(skR)`. The variable changed between them is not just "one vs two authorities" — it is "the compromised authority is the only one consulted" vs "it is one of two". Model 7 is the file that isolates the content variable properly.
3. **It says nothing about `AuthorityRepo`.** That process and `event AuthorityPublishedRepo` are declared, fired, and referenced by nothing in the query and nothing in the verifier. Their presence in the file might invite a reader to think the model "has two authorities"; for the purposes of this query it does not.
4. **It says nothing about detection.** There is no judge here; the model does not claim the forgery is undetectable, only that it is accepted.
5. **The usual algebra caveats.** The adversary here does not need a hash collision or a fingerprint collision — it has a key. But if it did *not* have the key, the model would not let it try either of those routes.

## 4. Which verifier checks are load-bearing

The query is already false, so no deletion can change it. What *matters* is the reverse:

- `let (=STMT, =h(t)) = checksign(ev, pkA)` (line 41) — **the check that would be load-bearing if `skD` were secret.** As written it is vacuous: the adversary can produce a passing `ev` for any `t`. This is the entire cause of the failure.
- `let (id, kfpr, ss, alg, ver) = t` (lines 42–43) — falsifiable here (unlike models 1/3/4, since `t` is not pinned), but trivially satisfied.
- `if fp(kX) = kfpr` (line 44) — reduced to a consistency check between two adversary-chosen values, since `kfpr` comes from an unpinned `t`.
- `let (=POSS, =fp(kX)) = checksign(ppf, kX)` (line 45) — satisfied by the adversary's own self-signature.
- `let (=BYTES, =fb) = checksign(sg, kX)` (line 46) — likewise.

**Under a compromised single authority, every downstream check degrades into "the adversary must know some private key".** That is the shape of the failure: the checks are internally consistent but externally unanchored.

## 5. Oddities

- **`AuthorityRepo` and `event AuthorityPublishedRepo` are dead code** for this query — declared, fired, never consulted by either the verifier or the query. The only effect is to put `sign((STMT, h(tH)), skR)` on the wire for an adversary that has no use for it.
- **The query uses `&&` where models 1–3 used `||`.** So model 5's conclusion is strictly stronger in form even as it is trivially violated in substance; two of the three conjuncts fail for reasons unrelated to which authority is named.
- **`label` bound and unused** (line 39); `id`, `ss`, `alg`, `ver` bound and never compared (lines 42–43).
- **The `if fp(kX) = kfpr` check, which was the key-binding step in models 1/3, is here doing no binding at all** — a check that looks identical across files but whose force depends entirely on whether `t` was pinned upstream.

---

# Model 6 — model 5, stripped of correspondence, asking the "two worlds" question of a *single* piece of evidence

## 1. Setup

Model 5's shape with all events on the authority and issuer sides deleted, plus `free accS: channel [private]` and a judge.

- `AuthorityDNS` / `AuthorityRepo`: bare `out(c, sign((STMT, h(t)), sk))`, no events.
- `Issuer`: the two signatures, no events.
- `VerifierS(pk(skD))`: identical five checks to model 5 (lines 32–37), then `event AcceptS(ev, t, kX, fb)` and `out(accS, (ev, t))`.
- `JudgeS`: reads two records with the **same `e1`** and fires `TwoWorldsSingle(e1, t1, t2)` if `t1 ≠ t2`.
- `out(c, skD)` present (line 49): **the sole consulted authority's key is still leaked.**

## 2. What the query claims

```
query ev, t1, t2; event(TwoWorldsSingle(ev, t1, t2)).
```

Reachability again: `not event(...) is true` = unreachable = good; `is false` = attack found. I expect **true**, and the sentence is:

> One and the same authority statement can never be accepted alongside two different records — even when the adversary holds the authority's signing key and can mint statements at will.

The reason is worth being explicit about, because it is not the obvious one. The judge fixes `e1` across both acceptances. `checksign(e1, pk(skD))` reduces to a *unique* term; the check `=h(t)` therefore forces `h(t1) = h(t2)`; `h` is injective, so `t1 = t2`. Key compromise does not help: it lets the adversary mint a statement for **any** record it likes, but each minted statement is bound to exactly **one** record.

## 3. What the claim does NOT say

1. **It does not say the adversary cannot make the verifier accept a bogus record.** It absolutely can — that is model 5's counterexample, which lives in this same process structure. This query says only that a bogus acceptance is *self-consistent*: one evidence blob, one record. Non-repudiation of content, not authenticity.
2. **It does not say the compromised key is harmless.** A reader seeing "true" on a model that leaks `skD` might conclude single-source evidence survives compromise. It survives only *this* question.
3. **The truth of the result has nothing to do with the protocol.** It is a consequence of `h` and `sign` being injective free constructors. A real hash collision (`h(t1) = h(t2)`, `t1 ≠ t2`) would break it instantly, and the model cannot express one. Likewise a signature scheme where one signature is a valid signature on two messages. This is the model where the gap between "symbolic true" and "real-world true" is widest.
4. **The judge only fires on a shared `e1`.** Two acceptances of different records under two *different* statements — trivially available to an adversary holding `skD` — are not compared and not covered.
5. **Nothing about `kX` or `fb`.** The judge compares only records. Two acceptances differing in key or payload go unremarked.
6. **No correspondence claim at all.** All the `AuthorityPublished*` / `Issuer*` events are gone from this file; nothing here ties any acceptance to any honest action.

## 4. Which verifier checks are load-bearing

| Check | Delete it? | Why |
|---|---|---|
| `let (=STMT, =h(t)) = checksign(ev, pkA)` (line 32) | **Flips to false.** | The only link between `ev` and `t`. Delete it and the adversary submits any fixed `ev` with two different records; the judge fires. Note this check is *simultaneously* vacuous for authenticity (model 5) and load-bearing for consistency (here) — the same line, two different jobs, one of which the key leak destroys and the other of which it does not touch. |
| `let (id, kfpr, ss, alg, ver) = t` (lines 33–34) | **No change.** | Restricts `t` to 5-tuples, but the shared `ev` already forces `t1 = t2` regardless of shape. |
| `if fp(kX) = kfpr` (line 35) | **No change.** | The judge never inspects `kX`. |
| `let (=POSS, =fp(kX)) = checksign(ppf, kX)` (line 36) | **No change.** | Same. |
| `let (=BYTES, =fb) = checksign(sg, kX)` (line 37) | **No change.** | The judge never inspects `fb`. |

One of five checks carries the result.

## 5. Oddities

- **`AuthorityRepo` is dead** — its signature is emitted and never consulted, exactly as in model 5.
- **`event AcceptS` is fired (line 38) and queried by nothing.** Dead instrumentation carried over from model 5.
- **`out(c, skD)` (line 49) has no effect on the result.** The file leaks a key and then proves something the leak cannot touch. Whether that was the intent, I can't tell from the code, but a reader should not take "true, despite the leak" as "the leak is survivable" in any general sense.
- **The check `=h(t)` is, under the declared algebra, exactly `=t`** — same observation as model 3. Models 6 and a hypothetical `=t` variant are the same model.
- **`label` bound and unused** (line 30); `id`, `ss`, `alg`, `ver` bound and never compared.

---

# Model 7 — both authorities honest, but they sign *different* statements; two verifiers side by side; two judges

This is the only file with no `out(c, skD)`. It is also the only one that changes the *content* of the two authorities' statements independently.

## 1. Setup

**Fresh secrets:** `skD`, `skR`, `skI`.
**Given to the adversary:** `out(c, pk(skD)); out(c, pk(skR)); out(c, pk(skI));` — **public keys only. No private key is leaked.** All three authorities/issuers are honest.

Two private channels, `accS` and `accP`.

**Parties:**

- `AuthorityDNS(skD, tH)` — destructures `t` and publishes `sign((STMT, id), skD)`: the **weak, identifier-only** statement (model 2's form).
- `AuthorityRepo(skR, tH)` — publishes `sign((STMT, h(t)), skR)`: the **strong, whole-record** statement (model 3's form).
- `Issuer(skI, fbH)` — possession proof and payload signature, no events.
- `VerifierS(pk(skD))` — the single-source verifier. Checks: destructure `t`; `let (=STMT, =id) = checksign(ev, pkD)`; `if fp(kX) = kfpr`; possession check; payload check. Then `event AcceptS(ev, t, kX, fb)` and `out(accS, (ev, t))`.
- `VerifierP(pk(skD), pk(skR))` — the paired verifier. Checks: destructure `t`; `let (=STMT, =id) = checksign(evD, pkD)`; `let (=STMT, =h(t)) = checksign(evR, pkR)`; `if fp(kX) = kfpr`; possession check; payload check. Then `event AcceptP(evD, evR, t, kX, fb)` and `out(accP, (evD, evR, t))`.
- `JudgeS` — two records off `accS` with the same `e1`, fires `TwoWorldsSingle` if `t1 ≠ t2`.
- `JudgeP` — two records off `accP` with the same `(e1, e2)`, fires `TwoWorldsPair` if `t1 ≠ t2`.

## 2. What the queries claim

**Query 1** — `query ev, t1, t2; event(TwoWorldsSingle(ev, t1, t2)).` I expect **false** (`not event(...) is false`; ProVerif finds a trace).

The attack requires no key compromise and no forgery. The DNS authority publishes exactly one statement, `e1 = sign((STMT, issuerId), skD)`. The adversary hands `VerifierS` that same `e1` twice, with `t1 = (issuerId, fp(pk(skI)), ssetH, algH, verH)` and `t2 = (issuerId, fp(pk(skI)), ssetH, algH, X)` for any `X ≠ verH`. Both times `id = issuerId` matches, `kfpr = fp(pk(skI))` so `kX = pk(skI)` with the genuine possession proof, and `fb = fbH` with the genuine payload signature. Both accept, both reach `JudgeS`, `t1 ≠ t2`, event fires. As a failed property:

> A single identifier-scoped statement from an honest authority does not determine the record it is presented with: the same statement supports two different records, differing in every field the statement does not cover.

**Query 2** — `query evD, evR, t1, t2; event(TwoWorldsPair(evD, evR, t1, t2)).` I expect **true** (`not event(...) is true` — unreachable). The sentence:

> When acceptance additionally requires an honest authority's signature over the hash of the whole record, no two acceptances backed by the same evidence pair can ever carry different records — the evidence pair determines the record uniquely.

More precisely: `evR` must be `sign((STMT, h(t)), skR)`, `skR` is honest and only ever signs `h(tH)`, so every `AcceptP` carries `t = tH`.

## 3. What the pair of results does NOT say

1. **Query 2's truth does not come from "two signatures instead of one".** It comes entirely from the *scope* of the second statement. A `VerifierP` that required two identifier-scoped statements (model 2, exactly) fails. A `VerifierS` that required one hash-scoped statement (model 6) succeeds. The variable that matters is what the statement covers, not how many statements there are — and model 7 is the only file that separates those two variables, because it holds key compromise at zero.
2. **Nothing cross-checks the two verifiers.** `accS` and `accP` are separate channels with separate judges. `VerifierS` can accept `t2` while `VerifierP` accepts `tH` in the very same trace, and **no event fires**. The model runs a broken verifier and a sound verifier side by side and never compares their outputs. A reader might reasonably assume "the model shows the paired verifier fixes the single verifier"; it shows the paired verifier does not *itself* exhibit the flaw, not that deploying both is safe.
3. **Query 2 says nothing about authenticity.** There are no `AuthorityPublished*` or `Issuer*` events in this file at all, and no correspondence query. `AcceptP` firing is never tied to any honest party having done anything. The file establishes consistency, not provenance. (Models 1/3 establish provenance; nothing establishes both simultaneously in one file with two honest authorities.)
4. **Query 2 says nothing about `kX` or `fb`.** `JudgeP` compares only `t`.
5. **Query 2 is again narrow in its trigger.** It only fires when two acceptances share a byte-identical `(evD, evR)`. Contradictory acceptances under different evidence are outside its reach.
6. **Query 2's truth rests on `h` and `sign` being injective.** A hash collision on the record, or a signature valid on two messages, would break it; neither is expressible.
7. **Neither query says anything about replay.** Both are reachability queries; unbounded replay is not merely tolerated but is the mechanism that feeds the judges.

## 4. Which verifier checks are load-bearing

**For query 1 (already false):** no deletion can change it. The relevant observation is which check is too weak — `let (=STMT, =id) = checksign(ev, pkD)` (line 41). Replacing `=id` with `=h(t)` would make query 1 true, turning `VerifierS` into model 6's verifier. The remaining `VerifierS` checks — the 5-tuple destructure (39–40), `if fp(kX) = kfpr` (42), the possession check (43), the payload check (44) — are all satisfied honestly in the attack trace and are irrelevant to the failure.

**For query 2 (true):**

| Check in `VerifierP` | Delete it? | Why |
|---|---|---|
| `let (id, kfpr, ss, alg, ver) = t` (lines 50–51) | **No change.** | `t` is pinned to `tH` by line 53; the shape check is unfalsifiable once that fires. |
| `let (=STMT, =id) = checksign(evD, pkD)` (line 52) | **No change.** | It pins only `id`, and `id` is already determined by the pinned `t`. This check contributes nothing to query 2. I am confident here: line 53 alone forces `t = tH`. |
| `let (=STMT, =h(t)) = checksign(evR, pkR)` (line 53) | **Flips to false.** | The sole load-bearing check. Delete it and `t` is unconstrained; the adversary presents two records with a fixed `(evD, evR)` and `JudgeP` fires exactly as `JudgeS` does. |
| `if fp(kX) = kfpr` (line 54) | **No change.** | `JudgeP` never inspects `kX`. |
| `let (=POSS, =fp(kX)) = checksign(ppf, kX)` (line 55) | **No change.** | Same. |
| `let (=BYTES, =fb) = checksign(sg, kX)` (line 56) | **No change.** | `JudgeP` never inspects `fb`. |

One of six checks in `VerifierP` carries query 2. In particular, the *DNS* half of the "paired" verification is load-bearing for nothing.

## 5. Oddities

- **`VerifierP`'s DNS check is dead weight.** The model is named (by structure) as a two-source verifier, but only one source matters. `VerifierP` with line 52 deleted proves the same theorem.
- **`AcceptS` (line 45) and `AcceptP` (line 57) are fired and queried by nothing.** Both are dead instrumentation.
- **No cross-judge.** As noted, the two acceptance streams are never compared, which is the most conspicuous absence in the file given that both verifiers are present specifically to be contrasted.
- **`AuthorityDNS` here destructures `t` and discards four of five fields** (lines 28–30) — the destructure exists purely to project out `id`.
- **`label` bound and unused in both verifiers** (lines 37, 48).
- **This is the only file where no private key is published**, which makes it the only file where a failing query is unambiguously about protocol structure rather than about key compromise. That makes query 1's failure the most informative negative result in the set.

---

# Across the seven

## Which models are the same construction with one change

The seven files are three axes crossed over a single construction (two authority statements + issuer fingerprint binding + issuer possession proof + issuer payload signature):

**Axis A — what the authority statement covers.**
- `(STMT, t)` — the whole record: **model 1**.
- `(STMT, h(t))` — the hash of the whole record: **models 3, 4, 5, 6**, and model 7's Repo authority.
- `(STMT, id)` — the identifier field only: **model 2**, and model 7's DNS authority.

**Axis B — what is asked.**
- A correspondence query (`Accept ⟹ authority published ∧ issuer possessed ∧ issuer signed`): **models 1, 2, 3, 5**.
- A "two worlds" reachability query via a judge over a private channel: **models 2, 4, 6, 7**.

**Axis C — how much is compromised / how many sources are consulted.**
- Two sources consulted, one key (`skD`) leaked: **models 1, 2, 3, 4**.
- One source consulted, that source's key leaked: **models 5, 6**.
- Two sources consulted, *no* key leaked: **model 7**.

The minimal-pair relationships:

| Pair | The one change | Effect |
|---|---|---|
| **1 → 3** | `(STMT, t)` becomes `(STMT, h(t))` | **None.** Under the declared algebra `h` is injective, so `=h(t)` ≡ `=t`. These are the same model; both true. |
| **1 → 2** | authority statement narrowed from `t` to `id` | Correspondence flips **true → false**. This is the negative control for model 1: it isolates statement scope as the cause. |
| **3 → 4** | correspondence machinery deleted, judge added | Different question, same construction. Model 4 is true; it is the positive counterpart to model 2's second query. |
| **2 ↔ 4** | authority statement `id` vs `h(t)` (both with judge) | `TwoWorldsBroken` reachable vs unreachable. The cleanest minimal pair in the set. |
| **3 → 5** | verifier consults one authority instead of two, and that authority's key is the leaked one | Correspondence flips **true → false**. But two things changed at once (source count *and* which source is compromised), so this pair does not isolate a cause. |
| **5 → 6** | correspondence deleted, judge added | `TwoWorldsSingle` is unreachable even under key compromise — a single statement still binds a single record. |
| **6 ↔ 7 query 1** | statement scope `h(t)` vs `id`, key leaked vs honest | Unreachable vs reachable. Since 6 has the *weaker* trust assumption and the *stronger* result, this pair shows scope dominates compromise for the consistency question. |
| **7 query 1 ↔ 7 query 2** | inside one file, honest keys throughout: `id`-scoped vs `h(t)`-scoped evidence | Reachable vs unreachable. The only place in the set where statement scope is varied with *everything else held fixed and nothing compromised*. |

## What the set as a whole establishes

Across all seven, one theorem does all the work: **an accepted record is pinned exactly to the extent that some signature the verifier checks commits to the whole record** — with that commitment (models 1, 3, 4, 6, 7-query-2) the acceptance is bound to what an honest party published and cannot straddle two records; without it (models 2, 5, 7-query-1) an adversary makes the verifier accept a record no one endorsed, using only honestly published signatures.

## What it leaves open

Almost everything that is not term-shape: **no file contains a reachability query on `Accept`/`AcceptS`/`AcceptP`, so nothing in the set rules out a verifier that never accepts anything** — a verifier replaced by `0` would satisfy every "true" result here; **no correspondence query is injective**, so replay, freshness, ordering, expiry and revocation are entirely outside the set; **only one honest record, one honest key and one honest payload exist**, so every "with the same `t`/`k`/`fb`" clause is matching values from a one-element set; **`fp`, `h`, `pk` and `sign` are injective free constructors**, so fingerprint collisions, hash collisions, signature malleability and one-signature-two-keys are unrepresentable rather than excluded; **no secrecy query appears anywhere**; **the proof-of-possession check is load-bearing for nothing in any of the seven** (in models 1 and 3 it is strictly redundant given the ordering of `event IssuerPossession` before `event IssuerSigned`); **`label`, `ss`, `alg` and `ver` are carried through every model and compared in none of them**; and **model 7 runs a sound and an unsound verifier concurrently without ever cross-checking their outputs**, so the set never asks whether a broken verifier's acceptance and a sound one's can contradict each other in the same run.
