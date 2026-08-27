# First-link spike — read-and-challenge annotation (ProVerif)

**Status: author-side, NON-DISCHARGING. Not a review. PROPOSED where it
recommends anything.** Written 2026-08-27 by the AI collaborator
(Claude) at the author's request, after he named the gap this file
exists for: the first-link decision (`459aff0`) rests on ProVerif
results, the credibility line requires every load-bearing decision to
be defensible by the author without the AI in the room, and the author
has said on the record he is not yet a ProVerif reader. He has also
said he will not block the project on that; this file is how the gap
gets narrower instead of merely acknowledged.

This is a *teaching artifact*, not a verification artifact. It was
produced with AI assistance against models written with AI assistance
— the correlated-blind-spot configuration A1.7's non-author gate exists
to defeat. Nothing here discharges anything, changes any status in
`PROPERTIES.md`, or counts as review. If a claim here and a model
disagree, that is a question to investigate, not a verdict.

Its one purpose, following `formal/tla/P5c_IssuanceProtocol.READ-AND-CHALLENGE.md`:
to show the *shape* of the questions a skeptic asks of these
particular files, so the read-and-challenge muscle is yours. The
questions are the product. The answers are yours to reach. Where this
file records an answer it reached itself, it says so and tells you how
to check it in under five minutes.

The question it is keyed to throughout: **what would have to be wrong
in `proverif/*.pv` for `459aff0` to be a bad decision, and how would
you see it?**

---

## 0. Reading keys — the minimum needed to contest these files

You know TLA+. ProVerif is a different animal: not a state machine you
enumerate but a set of processes an unbounded adversary interleaves,
with the adversary's knowledge computed as a closure. Twelve keys,
each pinned to a line in the spike so you can check the key against the
file rather than trust it.

1. **`free c: channel.`** — a public channel. Everything `out(c, …)`
   goes into the adversary's knowledge; every `in(c, …)` can receive
   anything the adversary can build. The verifier's entire input bundle
   (`q3_mechanism_dns_compromised.pv:90–91`) arrives this way: the
   adversary assembles it. That is the right adversary for a binding
   question — nothing is trusted because it "came from" somewhere.

2. **`free accCh: channel [private].`** — invisible to the adversary.
   Used only to feed accepted records to the two-worlds judge
   (`q4_attack_dns_compromised.pv:35, 85, 87–91`). The judge is not part
   of the protocol; it is the property, written as a process.

3. **`new skD: skey;`** — a fresh secret. The adversary does not know it
   unless something outputs it. `out(c, skD)` on line 109 of the q3 DNS
   variant is the *entire* compromise model: the key is public from the
   start, forever, and the verifier keeps trusting `pk(skD)`.

4. **`!P`** — unboundedly many copies of `P`. Every honest role is
   replicated. There is no session bound; a "true" result is for
   unbounded sessions.

5. **`fun` / `reduc`** — the term algebra. `fun sign(bitstring, skey):
   bitstring.` is a free constructor; the only thing you can do with a
   signature is `checksign(sign(m, k), pk(k)) = m` (line 41). Read what
   that equation *cannot* express: a signature that verifies under two
   different keys (DSKS); two byte-distinct signatures on the same
   message (randomized schemes); a signature verifying under a key that
   is not `pk` of its signer. Every one of those is excluded by the
   algebra, not by the design.

6. **Free constructors are injective.** `fun h(bitstring): bitstring.`
   and `fun fp(pkey): bitstring.` have no equations, so `h(t) = h(t′)`
   iff `t = t′`, and likewise for `fp`. You found this for `h` (author
   finding 3, DECISION.md §"Binding-form disposition"). Hold the thought
   for §A1: it applies to `fp` identically.

7. **`event Name(args).`** — a marker with no protocol effect. Events
   are what queries talk about. The five kinds are declared at
   q3:55–59.

8. **`query … event(A) ==> event(B) && event(C).`** — a
   *correspondence*: every execution of `A` was preceded by `B` and `C`
   with the shared variables bound to the same terms. It is
   **non-injective**: one `B` can justify unboundedly many `A`s. Replay
   is not caught by this form. Whether that matters here is §B1.

9. **`query … event(X).`** — a *reachability* query. **ProVerif answers
   it inverted:** the output line reads `RESULT not event(X) is true`
   when `X` is **unreachable** (the safe answer for an attack
   objective) and `RESULT not event(X) is false` when `X` **is
   reachable**. In this spike the same output shape is green for Q4/Q6
   and the *required red* for Q2/Q7/Q8. Do not read a `.out` file
   without this key in hand.

10. **`let (=STMT, =h(t)) = checksign(evD, pkD) in …`** — pattern match
    with `=x` meaning "must equal the value already bound to `x`." On
    mismatch the process silently stops. That silence is the
    non-acceptance idiom: rejection is *not reaching* `event Accept`.
    There is no `INVALID`/`UNVERIFIABLE` here; the verdict partition is
    TLA+ territory (PREDICTIONS.md §Tooling). Keep that in mind for
    §C2.

11. **Anatomy of a `.out` file.** After the process dump, each query
    gets a block. Lines beginning `goal reachable:` are *derivations of
    the hypotheses* — they appear for **true** results too
    (`q1_chain_dns_compromised.out:87` shows the honest derivation
    behind a green result). An **attack** is marked by the literal line
    `A trace has been found.` followed by `RESULT … is false`
    (`q2_broken_dns_compromised.out:242–243`; `…_run1.out:211–212`).
    `attacker(x)` in a goal line means "the adversary knows `x`." The
    `Verification summary` block at the end repeats every RESULT.

12. **What "true" and "false" are worth.** ProVerif over-approximates
    the adversary (Horn-clause abstraction). So `is true` is *sound* —
    no attack exists in the symbolic model, unbounded sessions — while
    `is false` is accompanied by a reconstructed trace, which in this
    spike ProVerif always produced (no `cannot be proved` outcome
    appears anywhere in `proverif/*.out`; that third outcome is the
    "timeout/mechanism failure" branch of the registered vocabulary and
    it never fired).

**First exercise (thirty minutes, no tool).** There are 20 `.out` files
and 24 `RESULT` lines. Using keys 9 and 11 only — not RESULTS.md —
classify every line as *green-as-designed*, *red-as-required*, or
*red-unexpected*, and for each red find its `A trace has been found.`
Then compare with the tables in RESULTS.md. Any disagreement is a
finding (about you, the file, or RESULTS.md — all three are worth
knowing).

---

## The four places a symbolic model can be wrong

The P5c guide's three, plus one that symbolic tools add:

1. **The abstraction lies** — the model omits something whose omission
   is load-bearing.
2. **The property is too weak** — the query passes but does not say
   what the English says.
3. **The seam is unguarded** — this artifact proves its half, another
   proves the other half, and the join is asserted.
4. **The algebra is too kind** — the equational theory erases a
   distinction the design relies on, so a query is green because the
   attack is *unrepresentable*, not because it is prevented. This is
   category 1 wearing a mathematician's coat, and it is the one you
   are least equipped to see from the prose, because the prose never
   mentions it.

For every question below: which of the four is it, and do you believe
the model's answer?

---

## A. Does the abstraction lie?

**A1. You already found one. Here is its twin.** Your finding 3 —
`h` is free, so Q3 proves nothing Q1 does not — is the canonical
category-4 catch, and DECISION.md records it and the ledger cites the
Layer 2 residual (concrete digest collision resistance). Now look at
`fp`. Same declaration shape (q3:42), same injectivity, and the
verifier's only semantic check on the accepted key is `if fp(kX) = kfpr
then` (q3:98). In the model that line is equivalent to `kX = the key
whose fingerprint the channel published`. In the implementation it is
"the fingerprint bytes match," which depends on the fingerprint
function's collision resistance and on what a *fingerprint* is (full
hash? truncated? which encoding of the key?). **Ask:** where is the
fingerprint's Layer 2 residual recorded? RESULTS.md ledger entry 1
names only `h`. ENUMERATION.md §1 says `h` carries its idealization
"stated in the header" and says nothing of `fp`. Either the omission is
harmless because fingerprints are covered by a P3/P8 obligation
elsewhere — find it — or the ledger is missing a line. Decide which.

**A2. Read the signature equation for what it excludes.** Key 5. The
algebra makes DSKS — an adversary constructing a key under which
someone else's signature verifies — *unrepresentable*. That is
precisely P3's threat, and ENUMERATION.md says S-P3 is the producer of
the key-binding relation these models "consumed." **Ask:** is that
sentence honest about direction? These models did not *consume* a key
binding proved elsewhere; they consumed an *algebra* in which the
attack cannot be written. Consuming an algebra is not a ledger entry
against a producer query; it is a category-4 residual until S-P3 adds
DSKS to the theory (which ProVerif can do, with an explicit
`reduc`-level model of key substitution — but that is S-P3's design
problem, and the spike's headers should not imply it is already
solved). Second thing the equation excludes: randomized signatures.
The judge (q4:87–91) matches evidence by *term equality*; with
deterministic `sign`, "same evidence" means "same message under same
key." Real ECDSA evidence is per-signature bytes. **Ask:** which way
does that cut? (Work it out: the model's judge equates *more* things
than a byte-level judge would, so an unreachable result in the model
is unreachable for the stricter real judge too. Conservative. But say
it out loud rather than assume it.)

**A3. Count the signers.** Map v1 (PREDICTIONS.md §Authority-relevance
map) lists "signing-key fingerprints (each member of the required-
signer set)" and "algorithm identifiers for each required signature" —
both plural. The tuple `tH = (issuerId, fp(pk(skI)), ssetH, algH, verH)`
(q3:106) carries **one** fingerprint, **one** algorithm, and an opaque
free term `ssetH` for the set, which no process ever inspects. This is
map v1 instantiated at n = 1 signer. **Ask:** is that in any header's
"does not prove" list? (It is not.) Is it a map *change* that triggers
the divergence rule? (No — the map is unchanged; the model is a narrow
instance of it.) Is it recorded anywhere? (Not that this file could
find.) It is load-bearing for nothing in the *first link* — a second
signer's fingerprint would live inside `ss` and be bound by the same
digest — but it means the spike says nothing about P2's per-member
binding, which is S-P2's job. Also: **one issuer.** Every honest
channel signs exactly one tuple, ever. Real channels sign many
statements for many issuers. Exercise M4 in the appendix adds a second
honest issuer to check that the binding still holds when the honest
channel keys are reused; the result is green, but you should run it
because the *reasoning* for why Q1/Q3 hold (see B2) quietly uses "the
honest channel signs only `tH`," and you want to see that assumption
fall away and the property survive.

**A4. Where is the honest baseline for Q1–Q4?** RESULTS.md ledger
entry 1 (as corrected 2026-08-12) and DECISION.md criterion 3 both say
the proper subsets `{}`, `{DNS}`, `{repo}` are "exhaustive by
enumeration." List `proverif/`: there is no `q1_chain_honest.pv`. The
`{}` case was never *run* for the strict ladder (only Q5/Q6 have
`_honest` variants). **Ask:** why is that acceptable? The answer is a
one-line monotonicity argument — the adversary with less initial
knowledge and the same honest processes can derive strictly less, so a
correspondence that holds under `{DNS}` holds under `{}` — and it is
*sound*. But it is an argument, not a run, and the record says
"enumeration." Decide whether a sentence belongs in the ledger. Then
ask the sharper follow-up: the compromise is **static** (key public
before any honest process runs), **permanent** (no rotation, no
revocation; the verifier trusts `pk(skD)` forever). Worst case for a
binding question — good. But "compromised, then revoked, then a
verifier holding the old trust anchor" is unrepresentable here; that
is P6's TLA+ territory and the seam between them is §C2's kin.

**A5. The model starts at the tuple.** The verifier receives `t`
already parsed (q3:90). No manifest object exists; "manifest" is `(t,
label)` and `label` is ignored by construction (q1:115–116 comment).
Everything between bytes-on-the-wire and a five-tuple — parsing,
canonical encoding, field ordering, what counts as "the same" field —
is P8's, and the spike is explicit that encoding is a residual.
**Ask:** does the "does not prove" list in each header say *where the
model's input begins*? A future reader who thinks the first link starts
at the DNS record will over-read every green result by one whole
layer.

---

## B. Is the property too weak?

**B1. Non-injective.** Key 8. One `AuthorityPublishedRepo(tH)` event
licenses every acceptance of `tH` forever. **Ask:** is there any
first-link claim that needs freshness? Work through map v1: the
authority statement is per-issuer-key (identity, fingerprint, signer
set, algorithm, version) — not per-attestation. Evidence *should* be
reusable across every attestation that key ever makes. Non-injectivity
is the right choice. But notice you had to go to the map to know that;
nothing in the `.pv` says "this evidence is long-lived by design." See
B3 for the same fact from the other side.

**B2. Trace why `t′ ≠ tH` cannot be accepted.** This is the exercise
that turns the disjunction you flagged (finding 1) from a wording
complaint into understanding. In the DNS-compromised variant the
adversary can produce `sign((STMT, h(anything)), skD)` at will. For
`Accept(…, t′, …)` it also needs `sign((STMT, h(t′)), skR)` (q3:95).
Only `!AuthorityRepo(skR, tH)` uses `skR`, and it signs only `h(tH)`;
`h` is injective; so `t′ = tH`. **That is the whole proof**, and every
step is visible in the file. Now notice what it leaned on: (i) `h`
injective (category 4, ledgered); (ii) `skR` used for exactly one
message (A3 — exercise M4 removes this and the property survives, for
the right reason: each honest signature still pins its own tuple);
(iii) the query binds the *same* `t` in `Accept` and in
`AuthorityPublished*` — remove that shared variable and the query
proves nothing. **Ask:** can you write the same three-step argument for
the repo-compromised variant without looking? If you can, you can
defend Q3 cold. If you cannot, the gap is exactly the size of the
argument, which is small.

**B3. What the judge does not see.** `Judge` (q4:87–91) compares two
accepted records `(evD, evR, t)`. It never sees `label`, `kX`, or `fb`.
Two acceptances with the same evidence pair and the same `t` but
different framed bytes `fb ≠ fb′` are *not* a two-worlds violation.
**Ask:** is that the design? By map v1, yes — the evidence binds the
*authority statement*, and the bytes are bound one link later by the
issuer's own `sign((BYTES, fb), skI)`. But if anywhere in your head the
DNS record or the repository publication was supposed to commit to a
*specific attestation*, this model is of a different design than the
one in your head, and every green result is about the wrong thing.
Settle it in one sentence in the relying-party story: *authority
evidence is per-key and long-lived; it vouches for who may sign, never
for what was signed.*

**B4. Which verifier lines have a negative control?** The spike's
companions (Q2, Q7, Q8) all weaken the same thing: the first-link
binding. That was the spike's scope, and it was right. But the verifier
has five checks (q3:94, 95, 98, 99, 100) and only the first two have
ever been shown to matter. A green model with an unexercised check is
indistinguishable from a green model with a dead check. Three
five-minute mutations, predictions registered in this file before they
were run, results in the appendix:

- **M2 — delete the fingerprint check (q3:98).** Prediction: **red**.
  The adversary presents its own key with the channel-pinned tuple;
  `IssuerPossession(pk(k_att))` never fired. *Observed: red, exactly
  that trace.* The fingerprint check is load-bearing.
- **M3 — collapse `POSS` and `BYTES` into one tag.** Prediction:
  **red**, with a specific trace: the adversary replays the honest
  possession proof `sign((TAG, fp(pk(skI))), skI)` *as the bytes
  signature*, and the verifier accepts an attestation whose framed bytes
  are the issuer's own fingerprint. *Observed: red, exactly that trace
  — `Accept(…, pk(skI), fp(pk(skI)))`, with `IssuerSigned` absent from
  the hypotheses.* Domain separation is load-bearing, and now you have
  seen *what it prevents* rather than been told.
- **M1 — delete the possession check (q3:99).** Prediction: **still
  green.** *Observed: green.* This is the headline; see below.

**B5. Read Q5b's red for what it actually says.** The registered
"waiver cost" is described in prose as "no provenance guarantee
survives." Open `q5_single_dns_compromised.out` and find the goal line:
`attacker(id_1) && attacker(ss_1) && attacker(alg_1) && attacker(ver_1)
&& attacker(k) && attacker(fb_2) -> event(AcceptS(…))`. Every field is
adversary-chosen — **including `issuerId`**. In degraded mode with the
sole channel compromised, the adversary can attest *anything* under
*anyone's* name. **Ask:** does the relying-party story say it that
starkly, or does "no provenance guarantee" let a reader imagine a
slightly-wrong statement rather than total impersonation? The `.out`
is blunter than the prose. Prefer the `.out`.

---

## C. Is the seam unguarded?

**C1. Map v1 ↔ the tuple.** See A3. The map is prose; the tuple is a
term; the correspondence between them (five fields, one signer) is
asserted by a comment (q1:31–34), not checked by anything. Not a
divergence. Possibly a ledger line. Your call.

**C2. `Accept` ↔ P4's verdict partition.** Key 10. The strict
`Verifier` corresponds to a `VALID_STRICT` entry and `VerifierS` to
`VALID_DEGRADED`; neither name appears in any `.pv`. ENUMERATION.md §4
lists the TLA+↔symbolic joins to carry as ledger entries: temporal
validity and refusal/standing. **Ask:** is the verdict-partition join
on that list? (It is not.) It is the join that makes "rejection is
non-acceptance" honest — someone must show that every path that stops
short of `event Accept` in the symbolic model lands in `INVALID` or
`UNVERIFIABLE`, never in a valid verdict, in P4's model. That is a
cross-formalism entry and, per §4's own rule, must never be marked
symbolically discharged.

**C3. `STMT` ↔ `STMT_DIRECT`/`STMT_DIGEST`.** DECISION.md rules that
both forms are legal, distinguished by tag, and says the spike's single
tag is "not a defect in the spike" because each model implements one
form. Agreed. It then routes a **cross-form substitution negative
control** to P7/P8, and ENUMERATION.md §2 places that control under
S-P7 as a ProVerif companion: "a `STMT_DIGEST` binding read as
`STMT_DIRECT` must fail." **Ask:** can such a companion go red in this
algebra? Exercise M5 builds it with the *shared* tag — repository
publishes `sign((STMT, h(t)), skR)`, verifier reads repository evidence
in direct form `let (=STMT, =t) = …` — and asks whether *any*
acceptance is reachable. Prediction: **unreachable**, because `h(t)`
and a five-tuple are distinct constructors and no pattern confuses
them. *Observed: `RESULT not event(Accept(…)) is true`.* The control is
green **without** distinct tags, so distinct tags are not what the
symbolic model is checking; a symbolic companion for this control
cannot fail, which is the "toy spike that could not fail" pattern by
another route. The cross-form control is a *byte-level* property and
belongs to P8's golden vectors, not to S-P7's ProVerif companions.
This file recommends (PROPOSED) that ENUMERATION.md be amended
accordingly; see the note appended there.

**C4. The registration step is not modeled.** `AuthorityDNS(skD, t)`
and `AuthorityRepo(skR, t)` take `t` — including the fingerprint — as
given. Nothing models *how the channel came to publish that
fingerprint*: whether it demanded proof of possession first, whether an
adversary can register a key it does not hold. In reality that is the
step where proof of possession does its work. It is also the step the
next section is about.

---

## THE HEADLINE: the possession link is discharged by the issuer's honesty, not by the verifier's check

Author-side, non-discharging, and — unlike the P5c guide's headline —
this one was *checked* before being written, because it was cheap to
check. Go falsify it anyway.

**The claim.** In every correct model of the spike, the verifier's
possession check

```
let (=POSS, =fp(kX)) = checksign(ppf, kX) in     (* q3:99 *)
```

rejects nothing that would otherwise be accepted. The correspondence's
`IssuerPossession(k)` conjunct is satisfied whether or not that line
exists.

**The evidence.** Mutation M1 deletes q3:99 and re-runs the Q3
correspondence in the DNS-compromised variant. Result: `is true`, same
hypothesis derivation as the unmutated model (appendix). The check
is not load-bearing for the query.

**Why, in three lines you can verify in the file.** (i) The fingerprint
check (q3:98) plus channel pinning (B2) force `kX = pk(skI)`. (ii) Only
`skI` can produce `sign((BYTES, fb), skI)` (q3:100), and only the
honest `Issuer` process holds `skI`. (iii) That process (q3:83–87)
fires `IssuerPossession(pk(skI))` unconditionally, *before* it signs
anything. So by the time any acceptance is possible, the possession
event has already happened — for reasons that have nothing to do with
whether the verifier looked.

**What it means.** The header of every chain model says the accepted
key "proves possession." What the *query* establishes is weaker: "the
honest issuer, which is the only party that could have signed, also
emitted a possession claim." The verifier's check is redundant in the
model because the model has no path on which a key's fingerprint gets
published without that key's holder being the honest issuer. That path
is **registration** (C4), and it is exactly where A3.2 item 3
("proof of possession is chain-internal … an existential self-signature
by another key in a multi-key manifest does not close the chain") is
pointed. Neither registration nor the multi-key manifest is in the
spike.

**What it does *not* mean.** It does not touch criterion 0, which is
about binding, and it does not touch the selection of transcription
binding. `459aff0` stands. What it touches is the *wording* — the same
class as remediation item 2 ("bound but not semantically validated"):
the spike proves the *statement's* uniqueness and the *signature's*
binding to that statement's key; it does not demonstrate that the
possession check does any work. That demonstration is owed by S-P3.

**What S-P3 must therefore do (PROPOSED, routed to the author):**

1. Model registration: an authority channel publishes `fp(k)` **only
   on receipt of** `sign((POSS, fp(k)), k)`, and the adversary tries to
   register an honest public key it does not hold.
2. Carry a companion in which registration does *not* demand
   possession — that companion must go red on a key-substitution
   query, and the correct model must stay green *because of* the check,
   which you verify by mutation exactly as M1 did here.
3. Add the DSKS-capable algebra (A2) so the attack is representable at
   all.
4. Carry the multi-key manifest case from A3.2 item 3.

ENUMERATION.md already names S-P3 as "the suite's producer for the
fingerprint relation the spike's models consumed." This section makes
precise *what* was consumed (an algebra plus issuer honesty) and what a
producer must look like to be worth the name.

**Work-through for you (ten minutes, one tool run):**

1. Copy `q3_mechanism_dns_compromised.pv` somewhere outside the repo.
   Delete line 99. Run `proverif` on it. Predict the RESULT line before
   you look.
2. Now restore line 99 and instead delete lines 84–85 (the possession
   event and its `out`) from `Issuer`, leaving the verifier's check in
   place. Predict again. (The check now cannot be satisfied by anyone —
   what does the correspondence say about an acceptance that can never
   happen? Key 8: a correspondence over an unreachable event is
   vacuously true. That is a *second* way a green possession conjunct
   can mean nothing, and you have now seen both. Appendix M1b: the
   RESULT is `is true` with **no** `goal reachable` line at all — the
   tell for vacuity is the *absence* of a derivation, and you will only
   notice it if you know to look.)
3. Write one sentence, in your words, stating what the spike proves
   about possession. If it is shorter than the header's sentence, the
   header overclaims.

I could settle the mechanical question, and did. I could not settle
whether the *design* intends the verifier's possession check to defend
against something the model omits, and you should not let me: that is
an author question about what the check is *for*, and the answer
decides S-P3's shape.

---

## Correction to the headline — same day, after the author asked what the check is *for*

The headline above is mechanically right and its diagnosis is
incomplete. It says the possession check is "not a design bug" and
points at registration and multi-key manifests as the places
possession earns its keep. It missed the function the record actually
assigns to the check, because I reasoned from the spike's encoding
instead of from the registered text. Original headline left as written.

**What the record says.** A1 §A1.5 item 3 and P10: proof of possession
is the **manifest self-signature** — the issuer keys sign the *manifest
bytes*. Two stated functions: the asserted keys "were demonstrably
held," **and** the self-signature "binds the manifest bytes to the
asserted keys." The A3.2 chain carries it as "proof of possession by
that same key."

**What the spike encoded.** `sign((POSS, fp(pk(skI))), skI)` — a
signature over the key's own *fingerprint*, not over the manifest. That
keeps the first function and drops the second. With that encoding, the
verifier's check is redundant with the fingerprint check plus the
bytes signature (the mechanical fact M1 exhibits). With the *design's*
encoding it is not.

**The test (appendix M7a/M7b).** Degraded mode, sole channel
compromised — the Q5b setting. Ask whether the adversary can get a
tuple accepted that carries the **honest** key's fingerprint but an
**altered signer set**. With the spike's fingerprint-only proof:
**reachable** — forge the channel evidence with the leaked key, replay
the honest possession proof (it says nothing about the tuple), replay
the honest bytes signature. With possession over the manifest as A1
specifies: **unreachable** — the adversary cannot produce the honest
key's signature over a tuple the honest key never signed.

**What this means, stated carefully.**

- The check is **not theater in the design**. Its job is to make the
  issuer a *second pin* on the authority statement, independent of the
  channels: a sole-channel adversary can still substitute its *own* key
  (possession is free to the adversary — A1.3, P10), but cannot alter
  the signer set, algorithm, or version *around the honest key*. That
  is exactly the P2-stripping surface in degraded mode, and it is
  closed by the issuer's signature, not by the channels.
- The spike **under-encoded** it, and the under-encoding is what made
  M1 green. Not a defect in any spike result — every registered query
  is about binding and two-worlds, and none of them depend on this —
  but the Q5b "waiver cost" as narrated ("no provenance guarantee
  survives") is the cost of the *spike's* encoding. Under the
  *design's* encoding the cost is narrower: the adversary can
  impersonate with its own key, not tamper with the honest one. The
  relying-party story should state the narrower cost, and should say
  which encoding it is stating it for.
- ENUMERATION.md §1 defines the shared theory library as extracted
  from the spike, with divergence a defect unless recorded. **This
  divergence must be recorded**, or S-P1/S-P2/S-P7 inherit the weak
  possession object and the multi-signer stripping surface stays open
  in the suite. See ENUMERATION.md amendment note 2.
- The multi-key case (A3.2 item 3: "an existential self-signature by
  another key in a multi-key manifest does not close the chain") is
  the same function seen from the other side: each key in the set
  signs the manifest, so removing one from the set invalidates the
  others' self-signatures over it. Fingerprint-only possession cannot
  express that at all.

**What it does to `459aff0`.** Nothing. Criterion 0 is about the
binding form, and neither encoding of possession touches it. What it
touches is the suite's theory library and one sentence of the
relying-party story.

**The lesson for you, which is the point of this file.** I called the
check unexercised and reached for "registration" as the missing piece
because that is the textbook role of proof-of-possession. Your record
had assigned it a different, specific job, in a sentence eleven weeks
old, and the model's encoding had quietly dropped that job. You asked
"what is it for?" and the answer was in A1, not in ProVerif. The
skill this file is trying to teach is not reading ProVerif. It is
noticing when the model's version of an object is thinner than the
record's version, and asking which one the green result is about.

---

## How to use this

Pick one. If you have ten minutes and the tool, do the headline's
work-through — the counterintuitive prediction is the fastest way to
learn what a correspondence checks and what it merely records. If you
have thirty minutes and no tool, do the §0 exercise: 24 RESULT lines,
classify them cold, compare with RESULTS.md. If you have an hour, do B2
until you can write the three-step argument for both variants without
the file open — that is what "defend it cold" means for Q3, and it is
smaller than it looks.

Then the questions this file did not think to ask are the ones that
matter, and those are yours.

If anything here points at a real gap, the fix is on the record —
a ledger line, an ENUMERATION amendment, or a signed amendment — never
an in-place edit to a model whose `.out` is committed evidence.

---

## Appendix — mutation exercises (guide author's runs, not record evidence)

All mutations are of `q3_mechanism_dns_compromised.pv` (the decided
mechanism, in the variant where the adversary holds the DNS key). Run
2026-08-27, ProVerif 2.05, in a scratch directory; the mutant files and
outputs are **not committed** and are not evidence in the record. If
any of these becomes load-bearing, it re-runs under registration with
predictions frozen first. Predictions below were written in this file
before the runs.

| # | Mutation | Predicted | Observed | What it teaches |
|---|----------|-----------|----------|-----------------|
| M1 | delete the possession check (line 99) | **green** | green — same hypotheses as unmutated | possession conjunct is discharged by issuer honesty, not the check (HEADLINE) |
| M1b | delete the issuer's possession event and `out` (lines 84–85), keep the check | green, vacuously | green — **zero** `goal reachable` lines | a correspondence over an unreachable `Accept` is true with no derivation; absence of a goal line is the vacuity tell |
| M2 | delete the fingerprint check (line 98) | red | red — `Accept(…, pk(k), fb)` with `attacker(k)`; no possession/signed events | fingerprint check is load-bearing |
| M3 | collapse `POSS`/`BYTES` to one tag | red, via possession-proof replayed as bytes signature | red — `Accept(…, pk(skI), fp(pk(skI)))`, `IssuerSigned` absent | domain separation is load-bearing; you see the attack it prevents |
| M4 | add a second honest issuer `skI2`/`tH2` on the same channel keys | green | green — two derivations, one per issuer | binding holds with channel keys reused; B2's "signs only `tH`" was a convenience, not a dependency |
| M5 | repo publishes digest form, verifier reads direct form, **same** `STMT` tag; query `Accept` reachability | unreachable | `not event(Accept(…)) is true` | cross-form confusion is unrepresentable in the algebra; a symbolic companion for it cannot go red (C3) |
| M7a | *(base: `q5_single_dns_compromised.pv`)* spike's fingerprint-only PoP; query: acceptance of `(issuerId, fp(honest key), ssX, algH, verH)` under the honest key | reachable | reachable — channel evidence forged with leaked `skD`, honest PoP and bytes signature replayed | sole-channel adversary alters the honest key's signer set; the check cannot object because the PoP never mentioned the tuple |
| M7b | same, PoP over the **tuple** per A1.5 item 3 (`sign((POSS, t), skI)`; verifier requires it over the presented `t`) | unreachable | `not event(AcceptS(…)) is true` | the design's possession check is load-bearing in degraded mode; the spike under-encoded it (Correction section) |

Eight for eight is not a virtue of the guide; it is the expected result
of small models with legible structure. The value is not the outcomes.
It is that you can now reproduce each one and, more usefully, invent
the next. (M7 was invented by the author's question, not by the guide
— which is how it is supposed to work.)
