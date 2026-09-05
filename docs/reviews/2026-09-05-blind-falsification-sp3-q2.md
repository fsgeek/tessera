# Blind falsification reviews: S-P3.Q2 (two non-author models)

Agreement-gate falsification reviews (`formal/PROPERTIES.md` line 121
class; ENUMERATION §5) on `formal/suite/s-p3/proverif/sp3_q2_degraded_compromised.pv`,
dispatched by the AI collaborator on 2026-09-05 (UTC) with the author's
standing choice to continue, before the author's own read. Both
reviewers were jailed to four files — the Q2 model (recut-2 text), the
shared library, P3's registered text (Amendment 1 lines 130–152), and
A1.3 (lines 330–346) — with no repository, history, or documentation
access, and instructed to falsify: audit the correspondence between the
verifier and P3's sentence, attempt attacks without weakening the
verifier, remove one check at a time, and give a verdict on the header's
honesty. Their mutation and attack files are archived under
`formal/suite/s-p3/proverif/run2/falsification/`.

## Reproducibility record

- **Reviewer 1:** Claude Opus 5 (`opus`), via the collaborator's Agent
  tool, fresh context. Work dir archived as `run2/falsification/reviewer1-opus/`
  (31 files: 13 single/paired check removals M1–M13, 3 fixture attacks,
  5 alternative signature/fingerprint theories, 1 observer probe).
- **Reviewer 2:** Claude Sonnet 5 (`sonnet`), same dispatch, in parallel,
  separate work dir `run2/falsification/reviewer2-sonnet/` (14 files:
  7 single removals, 3 pairs, 1 fixture attack, 1 observer probe).
- **Baseline both reproduced:** `Reattributed` unreachable,
  `PossessionTransplanted` unreachable, `AcceptS` reachable.
- **Model text reviewed:** recut 2 (asynchronous reports, before recut 3).
  Recut 3 (below) changed no result.

## Consolidated findings and collaborator dispositions

Numbered across both reviews; R1 = Opus, R2 = Sonnet. Each disposition
was checked against the model or by re-running before being written.

1. **The authority-evidence check is inert in this fixture** (R1 M1, R2
   M1: removing it changes nothing). The sole channel's key is published,
   so the adversary forges evidence for any tuple with or without the
   check. **Accepted.** The compromised channel is the adversary's
   *maximal condition* — it makes the claim strongest — not something the
   verifier's checks defend against here. Q2's header now says so.
   R1's further note: A1.3 item 6 licenses a *proper* subset of channels;
   compromising the sole channel exceeds it, in the conservative
   direction. Accepted as a note.

2. **The results do not depend on signature security.** R1 replaced the
   library's signature theory with total exclusive-ownership failure
   (`checksign(sign(m,k), kk) = m` for any `kk`) and both queries still
   held; `dsks` appears nowhere in the baseline derivation. **Accepted
   as fact; the characterisation "vacuous" is rejected.** A property
   that holds under a strictly stronger adversary is a strictly stronger
   result, not a vacuous one. What is true and now stated: the two
   queries are carried entirely by fingerprint injectivity (and,
   redundantly, hash injectivity); the honest sentence for the header is
   *under a perfect fingerprint, key substitution cannot move an
   acceptance of honest bytes to another key*. DSKS bites the moment the
   tuple-fingerprint check is removed (R1 M2, R2 M2 — trace through
   `dsks`), which is F4 of `RESULTS.md` restated with the load located.

3. **Fingerprint injectivity carries the whole load** (R1 A7/A8: under
   two fingerprint-collision theories one or both queries become
   reachable). **Accepted.** Already the library's declared Layer 2
   residual and ledger entry 1's residual; now the *first* sentence of
   Q2's header rather than a citation. R1's equational encodings of the
   same idea did not terminate; the destructor forms did. Recorded.

4. **Five of P3's seven fields are unexercised by these two queries**
   (R1 M6b/M6c/M7/M9/M12, R2 G/ot/cv): issuer identity, algorithm
   identifier, object type, canonicalization version, and the domain
   tag can be unbound or removed without changing either result; only
   key fingerprint and (redundantly) manifest hash are load-bearing.
   **Accepted.** This sharpens `RESULTS.md` F3. P3's text requires the
   fields be *included*; the model includes them; their *checks* are
   owed to other properties (object type → P7; canonicalization version
   and algorithm profile → P8/H1a; algorithm identifier → the A3 §1
   identifier-binding invariant; identity → see item 6). The Q2 header
   now lists them as included-and-unexercised. R2's note that the
   domain tag is realised as the outer signature tag rather than a frame
   field: accepted as a reading aid.

5. **The attestation-signature check is unexercised by these queries**
   (R1 M4, R2 E). With the frame's fingerprint field forcing `kX` to the
   signer's key whenever `fb` equals the honest bytes, whether `sg`
   verifies is irrelevant to re-attribution. **Accepted.** The check is
   exercised by an *authorship* correspondence (accepted under an honest
   key ⇒ that key signed those bytes), which is S-P1's integrity claim,
   and in strict mode by Q1's first-link correspondence
   (`IssuerSigned(k, fb)` in its conclusion). Carried to S-P1 as a
   consumer obligation in `RESULTS.md`; not added to S-P3's registered
   queries post hoc.

6. **The failure predicate is key-based; P3's sentence is identity-based.**
   R1's observer probe shows `IdentityUsurped` reachable: an adversary
   key accepted under honest issuer 2's identity, with adversary-authored
   bytes carrying that identity. R1 reads this as P3's headline sentence
   being false in the fixture. **Accepted as an observation; the reading
   is rejected, with reasoning.** P3 binds each signature to the identity
   *committed in the signed bytes*; in the usurpation trace the accepted
   key's fingerprint and the identity in the bytes agree with the
   manifest the (compromised) channel vouches for — the binding holds.
   What is wrong is that the identity→key *authority* is forged, which is
   P10 / the first link, and in degraded mode with the sole channel
   compromised that is the registered waiver cost (first-link RESULTS
   Q5b; ENUMERATION note 2). P3's registered threat is re-attribution of
   an *existing* signature; usurpation with a fresh signature is
   impersonation. **What R1 did correct:** the header's phrase
   "impersonation with the adversary's own key over its own bytes"
   understated the event — the bytes claim the honest issuer's identity.
   Reworded in Q2's header and `RESULTS.md`. If the author reads P3's
   sentence the other way, that is a ruling on P3's scope, not a model
   defect; flagged.

7. **The N1 vacuity witness was satisfiable by impersonation alone**
   (both reviewers: the printed `AcceptS` trace runs no honest issuer).
   **Accepted; fixed in recut 3.** Every S-P3 model now emits
   `HonestAccepted(k, fb)` from the judge when the accepted key *is* the
   signer's, and queries its reachability: reachable in all eight models.
   Suite rule added to `RESULTS.md`: the N1 witness is honest-flow
   acceptance, never bare acceptance.

8. **Possession-not-transplanted is an A1.5/P10 result reported under a
   P3 heading** (R1: the two load-bearing checks for it, tuple-fingerprint
   and possession-over-manifest, are P10 obligations carried in by
   library divergence D-3). **Accepted.** Ledger entry 2 in `RESULTS.md`
   is relabelled as P10-carried-in-S-P3, per ENUMERATION §2's "producer
   for the fingerprint relation" scope (note 1 item 2), which is wider
   than P3's registered text.

9. **Redundancy and necessity matrix** (both reviewers, consistent):
   frame-fingerprint alone suffices for re-attribution; tuple-fingerprint
   plus manifest-hash together compensate for its absence, and neither
   alone does; tuple-fingerprint and possession-over-manifest are jointly
   necessary and individually insufficient for the possession result.
   **Accepted** and recorded as the ledger's dependency statement.

10. **`fbH` rebound warning** (R1): the judges' local shadowed the
    library's fixture value. **Accepted; fixed in recut 3** (renamed
    `fbHon`); no warnings in any output.

11. **A1.3 item 2 (signature set) is unrepresentable in the fixed-arity
    slots** (both). **Accepted** as S-P2 scope, where the signer set is
    the subject.

12. **Fixture attacks that did not break the model** (R1 A1–A6, R2
    attempt 1): multi-signature DSKS, public-key-derived substitution,
    adversary-chosen manifests at the issuer, a cross-bound manifest
    tying issuer 1's key to issuer 2's identity, three issuers with two
    channels and two verifiers, a colliding issuer-identity string. All
    unreachable. Recorded as the breadth of the negative result.

**Net effect:** no query, prediction, or verdict changed. The header
claims were narrowed to what the queries discharge; one witness was
made honest; one warning was removed; two scope labels were corrected.
The reviewers found the model's *self-description* overstated and its
*results* sound, which is the outcome the gate exists to produce.

## Reviewer 1 (Opus) — verbatim

# Adversarial review — `sp3_q2_degraded_compromised.pv` against P3 / A1.3

Baseline reproduced (ProVerif 2.05, 0.03 s):

```
RESULT not event(Reattributed(kX,kH,fb)) is true.
RESULT not event(PossessionTransplanted(kX,p)) is true.
RESULT not event(AcceptS(ev,t,k,fb)) is false.
```

---

## 1. CORRESPONDENCE AUDIT

The verifier performs seven checks. Numbering them C1–C7:

| # | Line | What it is |
|---|---|---|
| C1 | `let (=STMT_DIGEST, =h(t)) = checksign(ev, pkS) in` | authority evidence over the manifest |
| C2 | `let authTuple(id, kfpr, ss, alg, ver) = t in` | tuple parse |
| C3 | `if fp(kX) = kfpr then` | presented key vs. manifest fingerprint |
| C4 | `let (=POSS, =t) = checksign(ppf, kX) in` | possession over the manifest (D-3) |
| C5 | `let (=BYTES, =fb) = checksign(sg, kX) in` | attestation signature over framed bytes |
| C6 | `let framed(ot, =alg, =id, =fp(kX), mh, cv, pl) = fb in` | in-bytes binding |
| C7 | `if mh = h(t) then` | manifest-hash linkage |

### (a) Checks the verifier performs that P3 does not license

- **C3 and C4 are not P3 checks.** P3's [model] half is exactly *"the binding of identity into signed bytes"*. C3 compares the key against the **manifest**, and C4 demands a **possession self-signature** — these are P10 / A1.5-item-3 obligations carried in by D-3, not the in-bytes binding. This matters because **C3 is the sole reason `PossessionTransplanted` is unreachable** (mutation M2 below). So the *second* of the two headline claims — *"nor an honest possession proof to be accepted for another key"* — is discharged entirely by a non-P3 check. It is a P10 result reported under a P3 heading.
- **C1 is licensed by nothing in this fixture** — see (c); it is inert by construction.

### (b) P3 requirements the verifier does not check

P3 field list: *"domain-separation tag, object type (per P7's enumeration), algorithm identifier, issuer identity, key fingerprint, manifest hash, and canonicalization version"*.

- **`objType` is never checked.** C6 binds it to a fresh variable `ot` and discards it. A1.3 item 4 explicitly grants *"re-frame objects across the P7 type boundaries"*; the model has no way to express or detect that.
- **`canonVer` is never checked.** C6 binds `cv` and discards it.
- Proof these two are decorative: **M7** deletes both fields from `framed` outright (5-ary constructor, issuer and verifier updated) and **every query result is byte-identical to baseline**. P3 says the signed bytes *include* those fields; the model includes them as unread padding.
- **Domain separation is present but unexercised.** **M12** collapses `POSS` and `BYTES` to a single tag — no result changes. P3 field #1 does no work in either query.
- **`ss` (signer-set) and `ver` are bound and discarded.** A1.3 item 2 (*"Strip, reorder, or duplicate signatures within the signature set"*) is structurally unrepresentable: there is one signature per slot, never a set.
- **The failure predicate is key-based, but P3's sentence is identity-based.** P3 opens: *"Acceptance binds each signature to the **issuer identity** committed in the signed bytes."* `Judge` receives the accepted identity and throws it away:
  ```
  in(acceptCh, (kX: pkey, id: bitstring, =fbH));
  if kX = kH then 0
  else event Reattributed(kX, kH, fbH).
  ```
  `id` is dead. The model tests key re-attribution, not identity binding. This is not cosmetic: **probe1** adds an observer (pure addition, no verifier weakening) and shows

  ```
  RESULT not event(IdentityUsurped(kX,kH,id,fb)) is false.
  event IdentityUsurped(pk(a_2), pk(skI2_1), issuerId2,
      framed(a_6, a_4, issuerId2, fp(pk(a_2)), h(authTuple(issuerId2,fp(pk(a_2)),…)), a_7, a_8))
  ```
  i.e. an **adversary key accepted under honest issuer 2's registered identity `issuerId2`**, with adversary-chosen objType, alg, canonVer and payload. The header calls this *"impersonation with the adversary's own key over its own bytes"* — that phrasing is wrong. The bytes carry a **victim's identity**, not the adversary's. P3's headline sentence is *false* in this fixture, and the registered queries are structurally blind to it.

### (c) Where the abstraction makes a query true for an unrelated reason

- **The N1 vacuity witness is itself vacuous.** `query event(AcceptS(ev,t,k,fb))` reports reachable, but the baseline trace contains **no `IssuerPossession` and no `IssuerSigned` step at all** — the accepted key is `pk(a_1)` for an adversary-chosen `a_1`, the tuple is `authTuple(a, fp(pk(a_1)), a_2, a_3, a_4)` with every field adversary-chosen. The witness does not show the honest package is acceptable; it shows the adversary can drive the verifier. The header says N1 *"is included and must report reachable"* — satisfied literally, not in substance. (A genuine witness exists: probe1's `HonestAccepted` is reachable. The model should carry that instead.)
- **The results are independent of the entire signature theory, including D-4.** Under `lib_H_totalEO.pvl`, which adds `checksign(sign(m,k), kk) = m` for **any** public key `kk` — total exclusive-ownership failure, strictly stronger than any DSKS — both queries still report `true`. The library header's boast that *"Every suite query therefore holds, if it holds, under an adversary with the registered DSKS capability"* is true here only vacuously: the query holds under **no signature security whatsoever**. `dsks(` does not appear anywhere in the baseline output.
- **`fp` injectivity carries the whole load.** Both claims collapse the moment the declared idealization is relaxed. Under `lib_C1.pvl` (adversary can mint a key it holds whose fingerprint equals a target's) `Reattributed` becomes reachable; under `lib_C2.pvl` (the DSKS-substituted key inherits the victim's fingerprint) **both** become reachable. So "accepted under any key but the signer's" really means "accepted under any key with a different fingerprint" — the gap between those is exactly the theory header's Layer 2 / P8 residual, and the model's own header does not restate it.
- **C1 is inert by construction.** `out(c, skS)` publishes the authority key, so the adversary forges `ev` for any `t`. Nothing constrains `t`. Confirmed by M1 (no change). Also note A1.3 item 6 licenses control of a **proper subset** of channels; with one channel a proper subset is empty, so this fixture is strictly stronger than A1.3 on that axis — conservative, but it means the "degraded / compromised channel" apparatus contributes zero to the result.
- **ProVerif warning, unaddressed:** `Warning: identifier fbH rebound.` The library declares `free fbH: bitstring` (a fixture value known to the adversary) and both judges shadow it as a local. Benign here (the free name is unused) but it is a live confusion hazard in a file whose whole point is byte identity.

---

## 2. ATTACK ATTEMPTS

No verifier check was weakened in any of these.

| # | Mutation | Result |
|---|---|---|
| A1 | **Multi-signature DSKS** (`lib_multidsks.pvl`): third rule `checksign(sign(m2,k), pk(dsks(sign(m,k),r))) = m2` — the substituted key verifies *every* signature by the victim, not just the one seen. Justified by A1.3 item 3 ("keypairs after seeing valid signature**s**") and by the real cofactored-Ed25519 `A' = A + T` attack that P3's [assumption] half names. | `Reattributed … is true.` `PossessionTransplanted … is true.` **No break.** Blocked at C3/C6 by `fp`. |
| A2 | **Public-key-derived substitution** (`lib_G_pubkeysub.pvl`): `ksubK(pkey, bitstring): skey` with `checksign(sign(m,k), pk(ksubK(pk(k),r))) = m` — key chosen from the victim's public key, no signature needed. | Both `true`. **No break.** |
| A3 | **Total exclusive-ownership failure** (`lib_H_totalEO.pvl`): `checksign(sign(m,k), kk) = m` for arbitrary `kk`. | Both `true`. **No break** — the decisive finding of §1(c). |
| A4 | **Adversary-chosen manifests at the issuer** (`atkD_chosen_manifest.pv`): A1.3 item 5 pushed inside — the honest issuer takes `m` from `c` and signs its possession proof and frames its bytes over it. | Both `true`. **No break.** |
| A5 | **Cross-bound fixture manifest** (`atkE_crossbound_manifest.pv`): extra published `m3 = authTuple(issuerId2, fp(pk(skI)), …)` binding issuer 1's key to issuer 2's identity, plus a third honest `Issuer(skI, issuerId2, m3)` instance and an authority publication of `m3`. | Both `true`. **No break** — and note *why*: the confusion it creates is an identity confusion, which `Reattributed` cannot see (§1(b)). |
| A6 | **Three issuers, two authority channels, two verifiers** (`atkF_two_channels_three_issuers.pv`): `skI3` under `issuerId`, uncompromised `skS2`, extra `VerifierS(pk(skS2))`. | Both `true`. **No break.** |
| A7 | **Fingerprint non-injectivity, form 1** (`lib_C1.pvl`): `fp` as a destructor with `fp(pk(kcolsk(k,r))) = fpOf(k)` — the adversary mints a key **it holds** whose fingerprint equals a target's. | `Reattributed … is **false**` (reachable). `PossessionTransplanted … is true.` |
| A8 | **Fingerprint non-injectivity, form 2** (`lib_C2.pvl`): `fp(pk(dsks(sign(m,k),r))) = fpOf(pk(k))` — the DSKS-substituted key inherits the victim's fingerprint. | **Both false** (both reachable). |

Reading: the model is robust against every capability A1.3 plausibly licenses **in the signature algebra**, and robust against every fixture enrichment I could construct. It is robust for one reason only — `fp` is a free constructor. A7/A8 are not A1.3-licensed (fingerprint collision is P8/Layer 2, and the theory header says so explicitly); I ran them to locate the load, not to claim a violation. The load is entirely there.

Two direct equational encodings of the same idea (`lib_fpcolB1.pvl`, `lib_fpcolB2.pvl`, using `equation … fp(pk(kcolS(k,r))) = fp(k)`) failed to terminate in ProVerif and were abandoned in favour of the destructor forms C1/C2. Recorded for completeness.

---

## 3. MUTATION SANITY

One check removed at a time (baseline library throughout):

| Mutant | Check removed | `Reattributed` | `PossessionTransplanted` | Verdict |
|---|---|---|---|---|
| M1 | C1 evidence | true | true | **No change — genuinely unexercised.** `skS` is public; `t` is adversary-chosen with or without it. |
| M2 | C3 `fp(kX)=kfpr` | true | **false** | Load-bearing, and the *only* thing holding possession. Attack trace uses the real DSKS rule: `PossessionTransplanted(pk(dsks(sign((POSS,authTuple(issuerId2,…)),skI2), a_4)), sign((POSS,authTuple(issuerId2,…)),skI2))`. |
| M3 | C4 possession | true | **false** | Load-bearing (trivially — `ppf` becomes unconstrained). No `dsks` in the trace. |
| M4 | C5 `checksign(sg,kX)` | true | true | **No change — the attestation signature check is unexercised.** The verifier can skip verifying the signature over the framed bytes entirely and both P3 queries still hold. |
| M5 | C7 `mh = h(t)` | true | true | No change **alone**; redundant with C6's `=fp(kX)` — see M8. |
| M6a | C6's `=fp(kX)` only | true | true | No change **alone**; redundant with C7 — see M8. |
| M6b | C6's `=id` only | true | true | **No change — unexercised.** |
| M6c | C6's `=alg` only | true | true | **No change — unexercised.** |
| M9 | C6's `=id` **and** `=alg` | true | true | Still no change. Two of P3's named fields are jointly inert. |
| M6 | C6 frame parse + C7 | **false** | true | The frame binding as a whole is load-bearing for re-attribution. |
| M7 | `objType`/`canonVer` deleted from `framed` | true | true | **No change — decorative fields.** |
| M12 | domain separation (POSS≡BYTES) | true | true | **No change — unexercised.** |

Redundancy pairs, to separate "unexercised" from "redundant":

| Mutant | Removed | `Reattributed` |
|---|---|---|
| M8 | C6-`=fp(kX)` **and** C7 | **false** |
| M10 | C6-`=fp(kX)` **and** C3 | **false** (and `PossessionTransplanted` false) |
| M11 | C5 **and** C6-`=fp(kX)` | true |

So there are exactly **two redundant routes** to the same conclusion `fp(kX) = fp(pk(skI))`: directly through the frame's `kfp` field, or through `mh = h(t)` ⇒ (h injective) `t = m` ⇒ `kfpr = fp(pk(skI))` plus C3. Both funnel through `fp` injectivity; neither touches the signature theory. The M8 attack trace uses the adversary's **own** key, `Reattributed(pk(a_2), pk(skI2_1), framed(objTypeH,algH,issuerId2,fp(pk(skI2_1)),…))` — no `dsks`.

Findings from this section:
- **C1 (authority evidence) and C5 (attestation signature verification) are genuinely unexercised** — not redundant with anything, just not needed for either query. C5 is the striking one: the model claims to be about signature binding and does not need the signature check.
- **C6's `=id` and `=alg`, `objType`, `canonVer`, and domain separation are unexercised.** Five of P3's seven named fields do no work.
- **C7 and C6's `=fp(kX)` are mutually redundant**, not unexercised.
- **C3 and C4 are load-bearing** — and both are P10 checks, not P3 checks.
- Positive: both companions **can** fail (M6/M8/M10 fire `Reattributed`; M2/M3 fire `PossessionTransplanted`). Neither judge is a could-never-fail companion.

---

## 4. VERDICT

**Not honest as written, though not fraudulent.** The results are correct; the header's characterisation of what they mean overstates on three counts.

**Could not falsify:**
- *"an adversary holding the DSKS capability and every key it derives cannot cause an honest issuer's framed bytes to be accepted under any key but the signer's"* — holds under baseline, under multi-signature DSKS, under public-key-derived substitution, under total exclusive-ownership failure, under adversary-chosen manifests at the issuer, under a cross-bound fixture manifest, and under three issuers / two channels / two verifiers.
- *"nor an honest possession proof to be accepted for another key"* — same, under all eight variants.
- *"impersonation with the adversary's own key over its own bytes is prevented (it is reachable…)"* — confirmed reachable.
- *"a reachability query on the acceptance event is included and must report reachable"* — literally true.

**Falsified or materially overstated:**

1. *"— the P3 [model] claim —"* (line 13). **Overstated.** P3's [model] half is *"the binding of identity into signed bytes … at minimum: domain-separation tag, object type, algorithm identifier, issuer identity, key fingerprint, manifest hash, and canonicalization version"*. M7, M12, M6b, M6c and M9 show that **five of those seven fields can be deleted or unbound with no effect on any query**. The model discharges the *key-fingerprint* field and (redundantly) the *manifest-hash* field. It does not discharge the other five; it merely lists them.

2. *"Acceptance binds each signature to the issuer identity committed in the signed bytes"* (P3's own opening sentence). **Falsified in this fixture.** `probe1.pv` yields `RESULT not event(IdentityUsurped(...)) is false` with the adversary's key accepted under `issuerId2`. The registered queries cannot see this because `Judge` binds `id` and discards it. The header's disclaimer — *"impersonation with the adversary's own key over its own bytes … out of scope by construction"* — misdescribes the event: the bytes carry the **honest issuer's registered identity**, chosen by the adversary.

3. *"an adversary holding the DSKS capability"* framing, and the library's *"Every suite query therefore holds, if it holds, under an adversary with the registered DSKS capability."* **Vacuous here.** `lib_H_totalEO.pvl` grants total exclusive-ownership failure and both queries still report `true`; `dsks(` appears nowhere in the baseline derivation. The result is insensitive to the D-4 divergence that is the library's stated reason for existing. Contrast M2, where removing C3 makes DSKS bite immediately — so the capability is real, it is simply neutralised by the fingerprint check alone.

4. The **N1 vacuity obligation is not met in substance**. The baseline witness trace runs no honest issuer. The honest path *is* reachable (probe1's `HonestAccepted`), but the model as written does not demonstrate that, and would report the same `is false` if the honest issuer were unable to produce an acceptable package at all.

5. **Undeclared residual.** The header defers to the theory for idealizations but never says that *both* of its claims collapse under `fp` non-injectivity (A7, A8). Given that C3 and C6-`=fp(kX)` are the only load-bearing checks, this file's entire contribution is: *"under a perfect fingerprint, key substitution cannot move an acceptance."* That should be the sentence in the header.

**Minor:** `Warning: identifier fbH rebound` — the library's `free fbH: bitstring` is shadowed in both judges; unaddressed in a file whose subject is byte identity. `ss` and `ver` bound and discarded. A1.3 item 2 (signature-set strip/reorder/duplicate) is unrepresentable in the model's fixed-arity signature slots. A1.3 item 6 licenses only a *proper subset* of channels; compromising the sole channel exceeds it (conservative direction).

---

## Reproducibility

All work under the reviewer's jail directory (archived at `run2/falsification/reviewer1-opus/`). `tessera_theory.pvl` and `base.pv` are verbatim copies of the two jail files. `run.sh` is a wrapper for `proverif -lib $LIB $FILE | grep RESULT`.

**Files created** (31 total): `run.sh`, `tessera_theory.pvl` (copy), `base.pv` (copy), `probe1.pv`, `lib_multidsks.pvl`, `lib_G_pubkeysub.pvl`, `lib_H_totalEO.pvl`, `lib_C1.pvl`, `lib_C2.pvl`, `lib_fpcolB1.pvl` (abandoned), `lib_fpcolB2.pvl` (abandoned), `lib_fpcol.pvl` (abandoned), `atkD_chosen_manifest.pv`, `atkE_crossbound_manifest.pv`, `atkF_two_channels_three_issuers.pv`, `M1_no_evidence_check.pv`, `M2_no_fp_vs_tuple.pv`, `M3_no_possession_check.pv`, `M4_no_bytes_sig_check.pv`, `M5_no_manifesthash_chk.pv`, `M6_no_frame_parse.pv`, `M6a_frame_drop_fp.pv`, `M6b_frame_drop_id.pv`, `M6c_frame_drop_alg.pv`, `M7_drop_objtype_canonver.pv`, `M8_dropfp_and_mh.pv`, `M9_drop_id_and_alg.pv`, `M10_dropfp_and_tuplefp.pv`, `M11_nobytessig_dropfp.pv`, `M12_no_domain_sep.pv`, `M13_no_domsep_no_tuplefp.pv`.

Legend below: `R` = `not event(Reattributed(...))`, `P` = `not event(PossessionTransplanted(...))`, `A` = `not event(AcceptS(...))`.

```
proverif -lib tessera_theory.pvl sp3_q2_degraded_compromised.pv     R true  | P true  | A false
proverif -lib tessera_theory.pvl base.pv                            R true  | P true  | A false
proverif -lib tessera_theory.pvl probe1.pv                          R true  | P true  | A false
                                     + not event(HonestAccepted(k,fb)) is false.
                                     + not event(IdentityUsurped(kX,kH,id,fb)) is false.
proverif -lib lib_multidsks.pvl  base.pv                            R true  | P true  | A false
proverif -lib lib_multidsks.pvl  probe1.pv                          R true  | P true  | A false
                                     + HonestAccepted false, IdentityUsurped false
proverif -lib lib_G_pubkeysub.pvl base.pv                           R true  | P true  | A false
proverif -lib lib_H_totalEO.pvl   base.pv                           R true  | P true  | A false
proverif -lib lib_C1.pvl          base.pv                           R FALSE | P true  | A false
proverif -lib lib_C2.pvl          base.pv                           R FALSE | P FALSE | A false
proverif -lib lib_fpcolB1.pvl     base.pv                           non-terminating (killed at 120s)
proverif -lib tessera_theory.pvl atkD_chosen_manifest.pv            R true  | P true  | A false
proverif -lib tessera_theory.pvl atkE_crossbound_manifest.pv        R true  | P true  | A false
proverif -lib tessera_theory.pvl atkF_two_channels_three_issuers.pv R true  | P true  | A false
proverif -lib tessera_theory.pvl M1_no_evidence_check.pv            R true  | P true  | A false
proverif -lib tessera_theory.pvl M2_no_fp_vs_tuple.pv               R true  | P FALSE | A false
proverif -lib tessera_theory.pvl M3_no_possession_check.pv          R true  | P FALSE | A false
proverif -lib tessera_theory.pvl M4_no_bytes_sig_check.pv           R true  | P true  | A false
proverif -lib tessera_theory.pvl M5_no_manifesthash_chk.pv          R true  | P true  | A false
proverif -lib tessera_theory.pvl M6_no_frame_parse.pv               R FALSE | P true  | A false
proverif -lib tessera_theory.pvl M6a_frame_drop_fp.pv               R true  | P true  | A false
proverif -lib tessera_theory.pvl M6b_frame_drop_id.pv               R true  | P true  | A false
proverif -lib tessera_theory.pvl M6c_frame_drop_alg.pv              R true  | P true  | A false
proverif -lib tessera_theory.pvl M7_drop_objtype_canonver.pv        R true  | P true  | A false
proverif -lib tessera_theory.pvl M8_dropfp_and_mh.pv                R FALSE | P true  | A false
proverif -lib tessera_theory.pvl M9_drop_id_and_alg.pv              R true  | P true  | A false
proverif -lib tessera_theory.pvl M10_dropfp_and_tuplefp.pv          R FALSE | P FALSE | A false
proverif -lib tessera_theory.pvl M11_nobytessig_dropfp.pv           R true  | P true  | A false
proverif -lib tessera_theory.pvl M12_no_domain_sep.pv               R true  | P true  | A false
proverif -lib tessera_theory.pvl M13_no_domsep_no_tuplefp.pv        R true  | P FALSE | A false
proverif -lib lib_H_totalEO.pvl  M6a_frame_drop_fp.pv               R true  | P true  | A false
```

Trace extractions (same binary, output filtered with `grep`/`awk`):
- baseline `AcceptS` witness — accepted key `pk(a_1)`, tuple `authTuple(a, fp(pk(a_1)), a_2, a_3, a_4)`, **no `IssuerPossession`/`IssuerSigned` in the trace**.
- `probe1.pv` `IdentityUsurped` — `event IdentityUsurped(pk(a_2), pk(skI2_1), issuerId2, framed(a_6,a_4,issuerId2,fp(pk(a_2)),h(authTuple(issuerId2,fp(pk(a_2)),a_3,a_4,a_5)),a_7,a_8)) at {82}`.
- `M2` `PossessionTransplanted` — `event PossessionTransplanted(pk(dsks(sign((POSS,authTuple(issuerId2,fp(pk(skI2_1)),ssetH,algH,verH)),skI2_1),a_4)), sign((POSS,authTuple(issuerId2,…)),skI2_1)) at {65}`.
- `M8` `Reattributed` — `event Reattributed(pk(a_2), pk(skI2_1), framed(objTypeH,algH,issuerId2,fp(pk(skI2_1)),h(authTuple(issuerId2,…)),canonVerH,a)) at {60}`.
- `grep -c 'dsks('` over full output: `base` = 0, `M2` = 38, `M3` = 0, `M6` = 0, `M8` = 0, `M10` = 27.
- `grep -i warning` on baseline: `Warning: identifier fbH rebound.`


## Reviewer 2 (Sonnet) — verbatim

## 1. CORRESPONDENCE AUDIT

**P3's text, sentence by sentence, against `VerifierS`:**

P3 requires the signed bytes to include, at minimum: domain-separation tag, object type, algorithm identifier, issuer identity, key fingerprint, manifest hash, canonicalization version. `framed(objType, alg, issuerId, kfp, manifestHash, canonVer, payload)` supplies 6 of these as named fields plus `payload` (not in P3's list, fine — "at minimum"); the domain-separation tag is realized as the *outer* signature tag (`BYTES`) rather than an inner `framed` field. That is a legitimate encoding (the tag is still part of what `sign` covers) but it means "domain-separation tag" is never a field inside `framed` — worth flagging since it's easy to misread the constructor as a literal 1:1 transcription of P3's list.

(a) **Checks the verifier performs that P3 does not license / does not need:** none found that exceed P3 — the checks are all sub-checks of the fields P3 names (`alg`, `id`, `kfp` cross-referenced against the tuple; `mh` against `h(t)`; `POSS`/`BYTES` domain tags). No extraneous strengthening.

(b) **P3 fields the verifier does not check:** two of P3's seven listed fields are bound in the `framed` pattern but never constrained against anything:
```
let framed(ot, =alg, =id, =fp(kX), mh, cv, pl) = fb in
```
`ot` (object type) and `cv` (canonicalization version) are captured as free variables — no equality, no membership check, nothing. P3's own text hedges "object type (per P7's enumeration)", so type-validity is plausibly P7's job, not P3's — but canonicalization version has no such hedge in P3's text and is simply unconstrained. Additionally, `ss` (signer-set) and `ver` (statement version) from the `authTuple` decomposition are bound and never used — but neither is in P3's registered field list, so that is out of scope for P3 specifically (it may matter to a different property).

Practically this is not exploitable *for the two queries in this file*: since `Reattributed`/`PossessionTransplanted` require the accepted `fb` to be bit-identical to the honestly-issued `fbH`, any tampering with `ot`/`cv` produces a different `fb` term, which fails the Judge's `=fbH` match anyway — the fields are "bound into the signed bytes" (satisfying the *letter* of P3) even without an independent cross-check. But it means the verifier does not itself demonstrate that substituting `ot`/`cv` is caught; it is caught only because the Judge processes compare against the literal honest witness. This is a correspondence gap worth ledger-citing even though it isn't a live attack.

(c) **Vacuity / idealization doing the work:**

- **The headline scenario is decorative for both negative queries.** This file's entire premise is "the SOLE authority channel compromised" (`out(c, skS)` — the authority signing key is leaked). I removed the entire authority-signature check (`let (=STMT_DIGEST,=h(t)) = checksign(ev,pkS) in`) — mutation M1 below — and **neither query's result changed**. That is because the model *already* leaks `skS` on the public channel, so the check it nominally performs was already vacuous before I touched it: the adversary holds `skS` outright and needs no cryptographic capability to forge `ev`. The file's own header markets this as "an adversary holding the DSKS capability ... cannot cause an honest issuer's framed bytes to be accepted under any key but the signer's" under channel compromise, but the compromise contributes nothing to that result — the same unreachability holds (for the identical reason) whether the channel is compromised or not, because the actual protection is downstream, in the fingerprint binding inside `framed`, which is completely independent of which manifest/evidence the adversary can forge.
- **The crux check is a "companion that could not fail" once one sees it.** `=fp(kX)` inside the `framed` pattern (line 87) forces `kX = pk(skI)` whenever `fb = fbH`, by the library's own declared idealization that `fp` is a free (injective, collision-free, no-preimage) constructor. This single equality is *independently sufficient* to discharge `Reattributed` (confirmed below); the DSKS capability the model advertises as being tested is present but structurally cannot reach past this equality for that query, because `dsks` only ever reproduces the *same* plaintext of the signature it was derived from — it never lets the adversary choose the fingerprint field embedded in someone else's already-issued bytes.
- **The `AcceptS` vacuity witness (N1) is satisfied via the out-of-scope impersonation branch, not a demonstrated honest flow.** ProVerif's printed witness trace for `AcceptS` uses a generic attacker-chosen key (`a_1`) self-signing everything from scratch — exactly the "impersonation with the adversary's own key over its own bytes," which the header explicitly disclaims as out of scope. I built an auxiliary probe (`honest_witness_probe.pv`, not part of the graded file) adding a `HonestAccept(kX,fb)` event that fires only when `kX` literally equals `pk(skI)` or `pk(skI2)`; that query also came back reachable (`RESULT ... is false`), so a genuine honest-flow acceptance is *also* derivable — the model isn't solely reliant on the impersonation branch. But note this is a probe I added, not evidence from the original file: read literally, the file's own trace output for its own N1 query documents only the impersonation witness.

## 2. ATTACK ATTEMPTS

All attempts below run against the **unweakened** verifier (baseline, all checks intact).

**Attempt 1 — issuer-identity collision.** A1.3 items 4–5 license replay/re-framing and free manifest crafting; I added a third issuer (`skI3`) whose `issuerId` string is *identical* to issuer 1's, on the theory that if identity-string collision could be exploited, `Reattributed`/`PossessionTransplanted` might fire between the two same-`id`, different-key issuers.
- Mutation: `attack1_id_collision.pv` — added `skI3`, `m3 = authTuple(issuerId, fp(pk(skI3)), ssetH, algH, verH)`, wired `!Issuer(skI3, issuerId, m3)` and `!AuthorityS(skS, m3)` into the process.
- Result:
  ```
  RESULT not event(Reattributed(kX_3,kH_2,fb_4)) is true.
  RESULT not event(PossessionTransplanted(kX_3,p_1)) is true.
  RESULT not event(AcceptS(ev_1,t_1,k,fb_4)) is false.
  ```
- Reading: no attack. This confirms the binding is via key fingerprint (`fp`), not the human-readable `id` string — the technically correct choice, and consistent with the header's own disclaimer that it does not prove "semantic validity of ids."

**Attempt 2 (analytic, confirmed by the tool's own exhaustive proof rather than a separate script) — DSKS on the possession signature vs. the attestation signature, cross-issuer, with the leaked authority key used to freely re-mint manifests.** I traced by hand every way to route a `dsks`-derived key through `VerifierS`'s six checks while keeping `fb = fbH` (required for `Reattributed`) or replaying the honest `ppf` (required for `PossessionTransplanted`), including using the leaked `skS` to mint an arbitrary manifest whose `kfpr` field is set to match the adversary's derived key. In every routing, either the `POSS` check forces `t = m` (the real manifest, because `checksign` is deterministic and DSKS only reproduces the exact original plaintext) or the `framed` pattern forces `kX = pk(skI)` directly (because `fbH`'s embedded fingerprint field is fixed at issuance). Since ProVerif's resolution is exhaustive over the declared attacker theory, and baseline already returns "true" for both queries, no attack of this shape exists *within the declared theory* — I did not find a script-level attempt that adds anything ProVerif's own search hadn't already ruled out.

**Attempt 3 — capability A1.3 grants that the theory cannot express.** A1.3 item 2 ("strip, reorder, or duplicate signatures within the signature set") has no counterpart in this model at all: there is no signature *set*, only single `ev`/`ppf`/`sg` terms, and the `ss` (signer-set) tuple field is bound and never checked (see 1b). I could not construct an attack exercising this A1.3 item because the model provides no structure to attack — this is a scope gap, not a defect I could falsify, and it may legitimately belong to a different property/model in the suite (multi-signature quorum) rather than P3.

No attack reached `Reattributed` or `PossessionTransplanted` without weakening the verifier.

## 3. MUTATION SANITY

Removed one check at a time from `VerifierS` (labels: A = tuple `fp(kX)=kfpr`; B = framed `=fp(kX)`; C = `mh=h(t)`; D = `POSS` check; E = `BYTES` check; F = authority `ev`/`t` check; G = framed `=alg`/`=id`).

| Mutation file | Check removed | Reattributed | PossessionTransplanted |
|---|---|---|---|
| baseline.pv | (none) | true (blocked) | true (blocked) |
| m1_no_authcheck.pv | F (authority sig) | true — **unchanged** | true — **unchanged** |
| m2_no_tuplefp.pv | A (tuple fp) | true — unchanged | **false — reachable** |
| m3_no_poss.pv | D (POSS check) | true — unchanged | **false — reachable** |
| m4_no_bytes.pv | E (BYTES check) | true — **unchanged** | true — **unchanged** |
| m5_no_framedfp.pv | B (framed fp) | true — unchanged (A+C compensate) | true — unchanged |
| m6_no_framedalgid.pv | G (framed alg/id) | true — **unchanged** | true — **unchanged** |
| m7_no_mhcheck.pv | C (mh=h(t)) | true — unchanged (B compensates) | true — unchanged |

To resolve which "unchanged" results are genuine redundancy vs. genuinely unexercised, I ran the compensating pairs together:

| Mutation file | Checks removed | Reattributed |
|---|---|---|
| combo_AB_removed_Conly.pv | A+B (only C left) | **false — reachable** |
| combo_AC_removed_Bonly.pv | A+C (only B left) | true — B alone sufficient |
| combo_BC_removed_Aonly.pv | B+C (only A left) | **false — reachable** |

Concrete witness for the M2 attack (PossessionTransplanted via A removed): ProVerif returns
```
event PossessionTransplanted(pk(dsks(sign((POSS,authTuple(issuerId2,fp(pk(skI2)),ssetH,algH,verH)),skI2),r)), sign((POSS,authTuple(...)),skI2))
```
— exactly the DSKS-on-possession-signature attack, blocked in baseline only by check A.

**Findings:**
- **F (authority signature check) — removal changes nothing, and is genuinely unexercised**, not merely redundant: no other check picks up its role; it simply never contributed to either negative result, consistent with 1(c) above (the compromised-channel premise is decorative here).
- **E (BYTES check) — removal changes nothing; redundant with B.** B (`framed`'s embedded fingerprint match) already forces `kX = pk(skI)` whenever `fb = fbH`, independent of whether `sg` is verified at all, so E adds no protection for these two queries (it may matter for a different property, e.g. genuine attestation/authorship, not tested here).
- **G (framed alg/id cross-check) — removal changes nothing; genuinely unexercised** by these two queries (neither depends on alg/id agreement; see 1b for why this happens to be safe anyway, since substitution changes `fb` itself).
- **B alone is independently sufficient** for `Reattributed` (combo_AC test). **A and C together compensate for B's absence, but neither A alone nor C alone suffices** (combo_AB and combo_BC both reachable) — A and C are a jointly-necessary compensating pair, not independently protective.
- **A and D are jointly necessary and individually insufficient** for `PossessionTransplanted` (removing either alone breaks it: M2, M3); B and C are irrelevant to `PossessionTransplanted` (removing either, or both, leaves it unaffected as long as A+D remain — confirmed by combo_BC_removed_Aonly, which keeps A+D and blocks it).

## 4. VERDICT

Under the theory's declared idealizations (`fp` and `h` as free, injective, collision-free constructors; `dsks` limited to reproducing the exact original plaintext under a fresh key), the file's header claim — *"an adversary holding the DSKS capability ... cannot cause an honest issuer's framed bytes to be accepted under any key but the signer's ... nor an honest possession proof to be accepted for another key"* — is **true as stated** and I could not falsify either negative query, including against a compromised-channel, two-honest-issuer, adversary-chosen-payload, adversary-chosen-manifest, id-colliding-third-issuer fixture.

What I could **not** falsify:
- `Reattributed` unreachable — held under every attack attempt and single-check removal except the two engineered to remove its actual protection (B alone, or A+C together).
- `PossessionTransplanted` unreachable — held except when A or D was individually removed.
- The header's explicit "does not prove" list (impersonation with adversary's own key/bytes; verification profile; frame byte layout; semantic id validity) — all confirmed genuinely out of scope and, where tested (id collision), genuinely unprotected in a way the header already disclaims.

What I **could** falsify / what should be corrected in the file's self-description:
- The header's framing of "degraded mode, sole channel compromised" as the operative adversarial condition being discharged is **misleading**: removing the entire authority-signature check (mutation F) changes nothing, because `skS` is unconditionally leaked on the public channel regardless of that check, and neither query's protection routes through it in any case. The property holds for reasons unrelated to channel compromise; the file doesn't actually stress-test what its own title advertises.
- The `BYTES`-signature check (E) and the framed `alg`/`id` cross-checks (G) are dead weight with respect to the two stated queries — present in the code, contributing nothing provable here. If the file's purpose is solely these two queries, that should be stated; if they exist for other suite properties, this file's header doesn't say so.
- Two of P3's seven registered signed-byte fields (`ot` object type, `cv` canonicalization version) are captured but never cross-checked by the verifier — safe only because the Judge's exact-bytes-equality requirement incidentally catches any tampering, not because the verifier itself validates them.
- The reachability witness the tool actually prints for the N1 vacuity obligation is the out-of-scope impersonation path, not a demonstrated honest-flow acceptance (I confirmed a genuine honest-flow witness exists only via an auxiliary probe outside the graded file).

## Reproducibility

All commands run from the reviewer's `r2/` jail directory (archived at `run2/falsification/reviewer2-sonnet/`) as `proverif -lib ../tessera_theory.pvl <file>.pv`.

Files created in `r2/`:
- `tessera_theory.pvl`, `baseline.pv` — unmodified copies of the two source files.
- `m1_no_authcheck.pv` … `m7_no_mhcheck.pv` — seven single-check removals (F,A,D,E,B,G,C respectively).
- `combo_AB_removed_Conly.pv`, `combo_AC_removed_Bonly.pv`, `combo_BC_removed_Aonly.pv` — three pairwise removals isolating A, B, C individually.
- `attack1_id_collision.pv` — third issuer with colliding `issuerId`, intact verifier.
- `honest_witness_probe.pv` — baseline plus an auxiliary `HonestAccept` event/query (not a verifier change) to test whether a genuine honest-flow accept is separately derivable.

RESULT lines:
```
baseline.pv:                    Reattributed=true  PossessionTransplanted=true  AcceptS(not)=false(reachable)
m1_no_authcheck.pv:              true               true                          false
m2_no_tuplefp.pv:                true               false(reachable)              false
m3_no_poss.pv:                   true               false(reachable)              false
m4_no_bytes.pv:                  true               true                          false
m5_no_framedfp.pv:               true               true                          false
m6_no_framedalgid.pv:            true               true                          false
m7_no_mhcheck.pv:                true               true                          false
combo_AB_removed_Conly.pv:       false(reachable)   false(reachable)              false
combo_AC_removed_Bonly.pv:       true               false(reachable)              false
combo_BC_removed_Aonly.pv:       false(reachable)   true                          false
attack1_id_collision.pv:         true               true                          false
honest_witness_probe.pv:         true (Reattributed), true (PossessionTransplanted), false (HonestAccept — reachable), false (AcceptS)
```
