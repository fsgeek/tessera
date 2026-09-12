# S-P1 reading aids — cast, checks, and plain-language claim for all five models

> **STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator;
> not adopted; the commit is the author's.** This is *testimony* under
> `formal/suite/ENUMERATION.md` amendment note 5 item 2 (lines
> 297–312): reading aids for non-expert readers, reviewed by the
> lower-ceiling reader probe (not yet run for S-P1), **not a gate for
> exit**. Nothing here changes a query, a result, a header, or a `.pv`
> file. Every statement about a model cites `file:line`; every
> LOAD-BEARING / CARRIED label cites the S-P1 probe or companion that
> established it (`RESULTS.md`, "Load-bearing / carried, from
> ablation", and findings F2–F6), a mutant from the cross-family
> review's single-removal matrix (2026-09-06, reproduced by the
> collaborator), or — where a row is marked *inferred* — S-P3 F1/F7,
> which that row says (§1b's domain-tag sentence is the one remaining
> inferred label; §2b rows 179–182 were inferred until the review
> ablated them). *(Sentence amended 2026-09-06, skeptic pass 2; it
> previously ended "— from S-P1's own runs, not assumed from S-P3's",
> which the inferred rows contradicted. Amended again 2026-09-06 when
> the cross-family review supplied ablations for the §2b rows.)* Form
> follows `formal/spike/first-link/READING-AID-Q3.md`
> and `formal/suite/s-p3/READING-AIDS.md`.

Files this document reads (all under `formal/suite/s-p1/proverif/`;
results in the sibling `.out` files, ladder run 7 — byte-identical to
run 2, whose line numbers this document cites):

| Short name | File | Kind |
|---|---|---|
| Q1d | `sp1_q1_strict_dns_compromised.pv` | correct, strict, DNS key leaked |
| Q1r | `sp1_q1_strict_repo_compromised.pv` | correct, strict, repo key leaked |
| Q2 | `sp1_q2_degraded_compromised.pv` | correct, degraded, sole channel leaked — **the P1 [model] binding claim** |
| Q3 | `sp1_q3_companionA_sig_unbound.pv` | broken companion A (signature not bound to presented bytes) |
| Q4 | `sp1_q4_companionB_frame_unsigned.pv` | broken companion B (frame fields outside the signature) |

Library: `formal/suite/lib/tessera_theory.pvl` (cited as `lib:N`).
Property text: `docs/phase-0-prereg-amendment-1.md` P1 at lines
116–119; operative form `docs/phase-0-prereg-amendment-3.md` §A3.1
items 1–2 (lines 68–83); adversary A1.3 at lines 331–347 of
Amendment 1. Predictions: `formal/suite/s-p1/PREDICTIONS.md` (frozen
`5188e7a`).

---

## 0. Typing note (once, for every model)

- **Messages are `bitstring`; keys are not.** Secret keys are `skey`,
  public keys `pkey` (`lib:95–97`), the network is `channel`
  (`lib:77`). A manifest, a frame, channel evidence, a possession
  proof and an attestation signature are all `bitstring`. **Shape
  lives in construction and pattern matches, never in declarations.**
  A frame is a frame because it was built with `framed(...)`
  (Q2:193) and is later taken apart with the pattern
  `let framed(ot, =alg, =id, =fp(kX), mh, cv, pl) = fb in` (Q2:179).
- **`: bitstring` on a pattern variable carries no information**
  (Q2:169–170). Read those as names. ProVerif's default does not
  enforce `pkey` against the adversary: what constrains the accepted
  key is the *checks*, never the annotation `kX: pkey`.
- **`=x` in a pattern means "must equal the value already bound to
  x"; a bare name means "read this and bind it".** So
  `let (=BYTES, =fb) = checksign(sg, kX)` (Q2:177) is a check —
  the signature must verify under `kX` **to exactly the presented
  `fb`** — while `let (=BYTES, fbSigned: bitstring) = checksign(sg,
  kX)` (Q3:79) is a read: it verifies a signature over *something* and
  never compares it to `fb`. That one-token difference is the whole
  of companion A.
- **`[data]` on a constructor** (`framed`, `authTuple`) means
  transparent: anyone can build one from parts and take one apart.
  `sign`, `h`, `fp` are not `[data]`.
- **`!P` is unboundedly many copies of P.** Every honest role, the
  verifier and both judges are replicated (Q2:218–222).
- **`event E(...); ...` records a milestone for the queries; it is not
  a message.** `query A ==> B` asks: in every execution, does each
  occurrence of `A` have an earlier `B` with the same arguments? `is
  true` = proved for all executions; `is false` = a counterexample
  trace was found. `query event(E)` alone asks whether `E` is
  reachable; the answer prints as `RESULT not event(E) is false`
  (reachable) — the double negative is ProVerif's, and it is the
  *wanted* answer for the N1 witness.
- **Two idealizations declared in the library, not in any model:**
  `fp` injective (`lib:117`, header 106–116) and `h` injective
  (`lib:131`, header 119–130). **A third carries this model's whole
  result:** `checksign` (`lib:100–104`) returns the signed message
  only under the signer's public key (or a DSKS-derived key that
  verifies that one signature, `lib:99`, D-4) — signature
  unforgeability, Dolev–Yao. RESULTS F2 (probes p6, p7) locates the
  entire load of the S-P1 headline on this rule.

## 0.1 Shared cast — the library terms every model uses

| Name | What it is in the design (plain words) | Declared (lib) | Used in the models |
|---|---|---|---|
| `c` | the public network; everything the adversary sees and can inject | 77 | every `in(c, …)` / `out(c, …)` |
| `skey`, `pkey`, `pk` | private key, public key, and the map from one to the other | 95–97 | every key |
| `sign(m, k)`, `checksign(s, pk)` | deterministic signature with message recovery: `checksign` returns the signed message if `s` verifies under `pk`, else the process stops (= reject) | 98, 100–104 | every evidence / possession / attestation check |
| `dsks(s, r)` | the A1.3 item 3 capability (D-4): a private key the adversary holds whose public key verifies the one seen signature `s` | 99, 103–104 | never in an honest process; available to the adversary; appears in no S-P1 derivation (the reds are reached without it) |
| `fp(pk)` | key fingerprint; idealized injective | 117 | manifests, frame field, verifier check |
| `h(x)` | hash; idealized injective | 131 | manifest hash in evidence and frame |
| `STMT_DIGEST`, `POSS`, `BYTES` | domain tags: authority evidence (digest form), manifest self-signature (possession), attestation signature over framed bytes | 139–141 | inside every signature |
| `OT_ATTEST` | object-type constant "base attestation" (D-5) — the frame's first field, honest side | 150 | Q2:193 and the same line in each model |
| `authTuple(id, kfp, sset, alg, ver)` | **the key statement = the manifest as this suite models it:** issuer identity, key fingerprint, signer-set, algorithm id, statement version | 164 | `m`, `m2` in every model |
| `issuerId`, `ssetH`, `algH`, `verH` | honest fixture values (public) | 169–172 | `m` in every model |
| `IssuerSigned(k, fb)` | **the issuance event:** "the honest issuer holding `k` signed framed bytes `fb`" — the right-hand side of every S-P1 correspondence | 182 | fired Q2:194; queried Q2:145, 164 |
| `IssuerPossession(k)`, `AuthorityPublishedDNS/Repo(t)` | fired for uniformity with S-P3; **queried by no S-P1 model** | 179–181 | Q2:190, 152 |
| `Accept(evD, evR, t, k, fb)` | strict-mode acceptance (two evidences, tuple, accepted key, bytes) | 183 | Q1d/Q1r only (Q1d:188); Q2–Q4 declare the 4-ary `AcceptS` |

## 0.2 The judge idiom (shared by all five) — registered before any run

`PREDICTIONS.md` "The judge" (lines 192–226). Three private channels
the adversary cannot see (Q2:133–135):

- `honestKeyCh` — the main process publishes each honest issuer's
  public key on it, replicated (Q2:218), so the judge may consume it
  for every acceptance;
- `honestCh` — the issuer reports `(its key, the bytes it framed)`
  for every signature it makes (Q2:195), in parallel with the public
  release (S-P3 recut 1);
- `acceptCh` — the verifier reports `(accepted key, accepted bytes)`
  on every acceptance (Q2:182).

**Judge H** (Q2:199–202): takes an honest key `kH`, then an
acceptance under *that* key, and fires `AcceptedUnderHonestKey(kH,
fbAcc)`. It knows nothing about what was signed; the **query**
(Q2:144–145) supplies that: every `AcceptedUnderHonestKey(k, fb)` must
have an earlier `IssuerSigned(k, fb)` — same key, same bytes. Read the
query as: *bytes accepted under an honest key are bytes that key's
holder signed.* Its contrapositive is P1's operative form: bytes
differing from what the honest key signed are never accepted under it.

**Judge N1** (Q2:205–208): takes an honest `(key, bytes)` report and
an acceptance of *those* bytes under *that* key, and fires
`HonestAccepted`. Its query (Q2:148–149) asks only that this be
**reachable**: the honest flow gets through. A model where it is not
reachable proves its correspondences vacuously; every S-P1 model,
companions included, reports it reachable.

A third thing about N1, recorded 2026-09-06 (cross-family review
item 6). **N1 is a vacuity guard, not coverage.** Every S-P1 model's
witness is reachable, and the committed outputs carry a reconstructed
trace for each; but the query is existential, and every committed
witness trace uses `skI2`. Reachability rules out a model in which
nothing is ever accepted; it does not show that each branch, each
honest key, or each payload shape is live. The reviewer verified this
in all four families and it is recorded as a suite-wide reading rule;
the rule's home is `ENUMERATION.md`, which is outside this directory
and is not amended here.

Two things a reader should hold onto. (1) Judge H is keyed on honest
*keys*. Honest bytes accepted under an *adversary* key never reach it
— that is S-P3's `Reattributed`, the complementary axis (RESULTS ledger
entry 1). (2) The correspondence is non-injective: two acceptances may
share one issuance (replay), and P1 permits that (§A3.1 item 1).

---

## 1. Q2 — `sp1_q2_degraded_compromised.pv` (the P1 [model] binding claim)

Taken first because Q1, Q3 and Q4 are read as differences from it.

### 1a. Cast

| Name | What it is in the design | Built | Consumed |
|---|---|---|---|
| `skS` | the **sole** authority channel's signing key — **leaked** | 211 | 153 (signs evidence); **217 `out(c, skS)`**; 219, 221 |
| `skI`, `skI2` | the two honest issuers' keys | 211 | 212/213 (fingerprinted into manifests), 214, 218 (published to judge H), 220 |
| `m`, `m2` | the two honest manifests, `authTuple(issuerId, fp(pk(skI)), ssetH, algH, verH)` and its twin | 212, 213 | 215 (published), 219 (channel signs each), 220 → 191 (self-signed), 193 (hashed into frame) |
| `payload` | **the thing attested**; adversary-chosen | read 189 | 193 |
| `framed(…)` | the P3 field list as a transparent 7-tuple: object type, algorithm, issuer id, key fingerprint, manifest hash, canonicalization version, payload | 127 | built 193; matched 179 |
| `fb` (issuer) | **the framed bytes** the issuer signs | 193 | 194 (`IssuerSigned`), 195 (report), 196 (signed) |
| `sg` | attestation signature `sign((BYTES, fb), skI)` | 196 | read 170; checked 177 |
| `ppf` | possession proof `sign((POSS, m), skI)` — manifest self-signature | 191 | 192 (published); read 170; checked 175 |
| `ev` | the sole authority evidence `sign((STMT_DIGEST, h(t)), skS)` | 153 | read 169; checked 171; 181 |
| `canonVerH`, `issuerId2` | fixture values (model-local) | 129, 130 | 193; 213/220 |
| `t` | the presented manifest | read 169 | 171, 172, 175, 180, 181 |
| `id`, `kfpr`, `ss`, `alg`, `ver` | fields of `t` | 172 | `kfpr` 173; `id`, `alg` 179; **`ss`, `ver` never used** |
| `kX` | the presented key | read 170 | 173, 175, 177, 179, 181, 182 |
| `fb` (verifier) | **the presented bytes** | read 170 | 177 (must equal what `sg` signs), 179 (taken apart), 181, 182 |
| `ot`, `mh`, `cv`, `pl` | frame fields read at 179 | 179 | `mh` 180; **`ot`, `cv`, `pl` never used** |
| `honestKeyCh`, `honestCh`, `acceptCh` | judge channels, §0.2 | 133–135 | out 218 / 195 / 182; in 200 / 206 / 201, 207 |
| `AcceptedUnderHonestKey`, `HonestAccepted` | judge events, §0.2 | 136, 138 | fired 202, 208; queried 144–145, 148–149 |
| `AcceptS(ev, t, kX, fb)` | model-local degraded acceptance: evidence, tuple, key, bytes | 158 | fired 181; queried 163–164 (the unrestricted contrast) |
| `AuthorityS`, `Issuer`, `VerifierS`, `JudgeH`, `JudgeN1` | roles | 151–153, 188–196, 168–182, 199–202, 205–208 | 219–222 |

### 1b. The verifier's checks (lines 168–182) — status from S-P1's own probes

| Line | Check | Plain meaning | Status for the headline (i) |
|---|---|---|---|
| 171 | `let (=STMT_DIGEST, =h(t)) = checksign(ev, pkS)` | the sole authority evidence endorses exactly this manifest | **CARRIED — inert by construction:** the channel key is public (217); probe p5 removes it, headline unchanged (`probes/p5_no_authority_evidence.out:170`); S-P3 F6 |
| 172 | `let authTuple(id, kfpr, ss, alg, ver) = t` | read the manifest's fields | structural |
| 173 | `if fp(kX) = kfpr` | the presented key is the one the manifest names | **CARRIED** (S-P3's axis): probe p1 removes it, headline unchanged (`p1_no_fp_check.out:171`) |
| 175 | `let (=POSS, =t) = checksign(ppf, kX)` | the presented key self-signed *this* manifest (possession over the manifest, D-3) | **CARRIED** (A1.5/P10, S-P3 ledger 2): probe p2, headline unchanged (`p2_no_possession.out:171`). Its side effect in companion A — pinning `t` to an honest manifest — is RESULTS F4 |
| 177 | `let (=BYTES, =fb) = checksign(sg, kX)` | **the presented key signed exactly the presented bytes** | **LOAD-BEARING** — probe p6 removes it, headline **false** (`p6_no_attestation_sig.out:314`); companion Q3 weakens it to a read, headline **false** (Q3 `.out:331`); probe p7 keeps it but makes signatures forgeable, headline **false** (`p7_total_eo_failure.out:332`). RESULTS F2 |
| 179 | `let framed(ot, =alg, =id, =fp(kX), mh, cv, pl) = fb` | the signed bytes name the same algorithm, identity and key fingerprint the manifest does; object type, hash, version, payload are read | **CARRIED** (all three pattern pins): probe p4 pins nothing in the pattern, headline unchanged (`p4_frame_unpinned.out:173`); the fourth P3 in-bytes binding is line 180 / probe p3. `ot`, `cv` unchecked → P7, P8/H1a (S-P3 F7); this is the surface companion B exploits |
| 180 | `if mh = h(t)` | the signed bytes commit to this manifest | **CARRIED**: probe p3, headline unchanged (`p3_no_manifest_hash.out:171`) |
| 181 | `event AcceptS(ev, t, kX, fb)` | acceptance | the event the unrestricted query (ii) and the P4 join are about |
| 182 | `out(acceptCh, (kX, fb))` | report to the judges | encoding (S-P3 recut 1: nothing follows it, so no sequencing hazard) |

Domain tags are present in 171/175/177 and **CARRIED — inferred from
S-P3 F7; no S-P1 probe ablates a tag** (the seven probes touch only Q2
lines 171, 173, 175, 177, 179, 180 and, in p7, the library's
`checksign` reduc). In one sentence: **only line 177 defends P1's binding half; every other
check is there for another property and is left in so this is the
verifier S-P3 checked, not a subset of it.**

The cross-family review's own single-removal matrix (2026-09-06)
agrees with p1–p7 on every row of this table: on the Q2 form the
headline stays true under every single removal except the
attestation-signature check and its byte and key equalities
(`m_G_signature.out:314`, `m_G_sig_bytes.out:331`,
`m_G_sig_key.out:338`). Two cautions the reviewer is right to press
(review item 4). **Inert is not removable:** each row above records
what happens when *one* check goes, and nothing here licenses
removing several together. And **inert for these queries is not inert
for the verifier** — most of these checks exist for another
property's query, which is why they are left in.

### 1c. Results (`.out`)

| Query | Line in `.out` | Result | Meaning |
|---|---|---|---|
| (i) headline `AcceptedUnderHonestKey ⟹ IssuerSigned` | 173 | **true** | bytes accepted under an honest key were signed by that key; derivations at 171–172 carry `IssuerSigned` for both honest keys, so this is a proof over reachable acceptances |
| (iii) N1 `HonestAccepted` | 349 | **reachable** | the honest flow is accepted (trace 178–348: adversary picks a payload, issuer 2 frames and signs, verifier accepts under `pk(skI2)`) |
| (ii) unrestricted `AcceptS ⟹ IssuerSigned` | 499 | **false — registered red** | trace 354–498: the adversary's own key `k`, vouched for by the leaked channel, self-possesses and self-signs its own frame; no honest key involved (RESULTS F5) |

### 1d. Claim, adversary, boundary (plain language)

**Claim (header 18–24; RESULTS F1).** In degraded mode, with the only
authority channel fully in the adversary's hands, a relying party who
runs these checks and ends up accepting a package *under an honest
issuer's key* is holding exactly the bytes that issuer signed — not
one field altered, not a payload swapped, not a frame the issuer never
saw. What the adversary can still do is present a package under *its
own* key (query (ii), red); what it cannot do is make an honest key
vouch for anything that key did not sign.

**Adversary (A1.3, Amendment 1 lines 331–347; fixture 211–217).** Sees
everything on `c`; holds the sole channel's private key (217) and so
can publish any manifest through it; chooses every payload the honest
issuers sign (189); builds manifests and frames freely (`[data]`); has
the DSKS capability (`lib:99–104`); holds every key it uses. Does
**not** hold `skI` or `skI2`.

**Why the attack fails.** To have judge H fire, the accepted key must
be `pk(skI)` or `pk(skI2)` (200–201). To get past line 177 with that
key, `sg` must verify under it to `(BYTES, fb)` for the *presented*
`fb`; the only signatures under an honest key over a `BYTES`-tagged
message are the ones the issuer made at 196, each over a frame it
recorded at 194. So the presented `fb` is one of those frames. (The
DSKS rule gives the adversary a *different* key that verifies an
existing signature; it never makes an honest key verify a new one.)

**Boundary (header 25–33; RESULTS "What S-P1 does not discharge").**
Not the verdict (P4). Not freshness — the same issuance may be
accepted many times. Not that the accepted key is an honest issuer's —
in this mode it need not be (query (ii)). Not re-attribution of honest
bytes to another key (S-P3). Not the multi-signer set (S-P2). Not the
byte layout of `framed(…)` or canonical encoding (P8): "the same bytes"
here means "the same term", and two byte strings canonicalizing to one
term are one here. Not the object-type field's *meaning* (P7). Not
signature security in the real world: the result stands on
`checksign` being unforgeable (`lib:100–104`), which the
implementation buys from the verification profile (H1a).

**Boundary, three things that cannot even be *posed* here**
(cross-family review, 2026-09-06). *(1) Signature-set operations*
(A1.3 item 2 — strip, reorder, duplicate signatures within the set):
this verifier reads exactly one signature `sg`, and the manifest's
signer-set field `ss` is read and never used, so no set operation has
anywhere to happen. The signer set is S-P2's subject (review item 1).
*(2) Byte-encoding attacks* — non-canonical encodings, hash-input
ambiguity, cross-kind parse confusion: term equality stands in for
byte equality here and distinct constructors never confuse, so the
attack has no representation. In the reviewer's words this is "a
coverage failure, not an unreachable attack"; the obligation is P8's
injectivity proof and the library's `h`/`fp` idealization, already
registered as Layer 2 (review item 2). *(3) Verdicts, waivers and
policy inputs* do not exist in any S-P1 model: there is only `AcceptS`
and non-acceptance. The partition is P4's, joined to `AcceptS` in
prose (RESULTS ledger entry 3) and never symbolically (review item 3).

**Inconclusive, recorded** (review item 11): the reviewer's A5 asked
whether two *identical* acceptance reports are reachable — an
injectivity probe. ProVerif returned `cannot be proved`
(`a5_repeat_replay_uncertain.out:689`), which is neither reachable nor
unreachable. Injectivity is not a registered requirement (§A3.1
registers the non-injective form), and nothing in this family claims
it either way.

### 1e. Read and never used (Q2)

`ss`, `ver` (172); `ot`, `cv`, `pl` (179). `IssuerPossession` and
`AuthorityPublishedDNS` are fired (190, 152) and never queried. From
the library: `STMT_DIRECT`, `TLR`, `REFUSAL`, `fbH`, every `OT_*`
except `OT_ATTEST`, `Accept` (5-ary), `AuthorityPublishedRepo`.

---

## 2. Q1d — `sp1_q1_strict_dns_compromised.pv` (strict, DNS key leaked)

### 2a. Cast — differences from Q2

| Name | What it is | Built | Consumed |
|---|---|---|---|
| `skD`, `skR` | the DNS and repository channel keys; **`skD` leaked** (208), `skR` honest | 202 | 210–211 (each channel signs both manifests), 213 (verifier's fixed keys) |
| `evD`, `evR` | the two evidences, each `sign((STMT_DIGEST, h(t)), skCh)` | 158, 162 | read 176; checked 179, 180; 188 |
| `Accept(evD, evR, t, kX, fb)` | library 5-ary strict acceptance | `lib:183` | fired 188; queried 145–146 |
| everything else | as Q2, at lines 132–142 (declarations), 164–172 (issuer), 191–199 (judges), 201–214 (main) | | |

### 2b. The verifier's checks (lines 175–189)

| Line | Check | Status |
|---|---|---|
| 179 | DNS evidence verifies under the DNS key over exactly `h(t)` | **inert in this variant** (the DNS key is public at 208). Recorded as inferred until 2026-09-06; now ablated by the cross-family review's mutants: removing the check, its key equality or its digest equality leaves both registered correspondences true (`m_D_evD.out:198`, `m_D_evD_key.out:205`, `m_D_evD_digest.out:201`; review item 4) |
| 180 | repository evidence verifies under the honest repository key over exactly `h(t)` | **LOAD-BEARING for the unrestricted query (i)** — with 182, it pins `kX` to an honest key: the honest channel only signs `h(m)` and `h(m2)` (211), `h` is injective, so `t ∈ {m, m2}`, and 182 then forces `fp(kX)` to an honest fingerprint. Ablated by the cross-family review 2026-09-06 (review item 10), which replaces the earlier record "inferred from S-P3 F1 and the shape of (i); not ablated in S-P1": (i) is **false** on removing the check (`m_D_evR.out:349`), on removing its key equality (`m_D_evR_key.out:366`) or its digest equality (`m_D_evR_digest.out:357`), and **true** when only its domain tag is unbound (`m_D_evR_tag.out:201`) — the two equalities carry it (review item 5, defence in depth, the S-P3 F5 shape). For the headline (ii) it is CARRIED (the headline restricts to honest keys itself; `m_D_evR.out:356`, true) |
| 181 | `let authTuple(id, kfpr, ss, alg, ver) = t` | **LOAD-BEARING for (i)** — the strict headers omitted this dependency until 2026-09-06 (review item 10): replacing the manifest pattern with attacker-supplied fields makes (i) **false** (`m_D_tuple_binding.out:387`). Structural for (ii) |
| 182 | `if fp(kX) = kfpr` | **LOAD-BEARING for (i)**, jointly with 180 and 181 and now observed rather than inferred: (i) is **false** on its single removal (`m_D_fp.out:362`; review item 10). CARRIED for (ii) (probe p1 on the Q2 form) |
| 183 | possession over the manifest | CARRIED (probe p2, Q2 form); the review's single removals agree (`m_D_possession.out:199`, `m_D_poss_tag.out:201`, `m_D_poss_manifest.out:201`, `m_D_poss_key.out:203`) |
| 185 | `let (=BYTES, =fb) = checksign(sg, kX)` | **LOAD-BEARING for (i) and (ii)** (probes p6/p7 and companion Q3 on the Q2 form; the check is the same conjunct here, `PREDICTIONS.md` "Ordering rule"); confirmed on the Q1 form by the cross-family review — both correspondences **false** on removing it (`m_D_signature.out:340`) or its byte (`m_D_sig_bytes.out:357`) or key (`m_D_sig_key.out:365`) equality |
| 186, 187 | frame pins; manifest hash | CARRIED (probes p4, p3); the review's single removals leave both correspondences true here (`m_D_frame_binding.out:202`, `m_D_frame_alg.out:201`, `m_D_frame_id.out:201`, `m_D_frame_fp.out:201`, `m_D_manifest_hash.out:199`) |

### 2c. Results (`.out`)

| Query | Line | Result | Meaning |
|---|---|---|---|
| (i) `Accept ⟹ IssuerSigned` | 201 | **true** | in strict mode *every* acceptance is under a key that signed the accepted bytes — the spike's Q1 "accepted signature → exact framed bytes" link, transcribed (derivations 199–200 carry `IssuerSigned` for both honest keys) |
| (ii) headline | 208 | **true** | as Q2 |
| (iii) N1 | 396 | **reachable** | trace 213–395 |

### 2d. Claim, adversary, boundary

**Claim.** With two authority channels both required and one of them
(DNS) fully compromised, no package is accepted except under an honest
issuer's key, and then only over bytes that issuer signed. The first
half is the first link (consumed: RESULTS ledger entry 2); the second
is P1's binding half, the same as Q2's.

**Adversary.** As Q2 with `skD` in place of `skS`; does not hold
`skR`, `skI`, `skI2`.

**Why (i) holds here and not in Q2.** Line 180. The honest channel
signs only the two honest manifests, so the adversary cannot get a
manifest naming its own key past the strict verifier; in Q2 there is
no honest channel, and the adversary's own key gets through — which is
why Q2 restricts the headline to honest keys and registers (ii) red.

**Boundary.** As Q2, plus: `n = 2` channels, one leaked — not a
general-`n` result (A1.3 item 6 "any proper subset", enumerated not
generalized); the two-channel first link is *consumed* from the spike
and S-P3 Q1, not re-established (no `AuthorityPublished*` conjunct is
queried here — that is S-P3 Q1's query, `sp3_q1_*.pv:91–96`). And, as
in §1d, three things cannot be posed in this model at all: signature-set
operations (one signature slot, `ss` unused — S-P2's subject, review
item 1); byte-encoding attacks (term equality for byte equality —
P8's injectivity obligation and the library's `h`/`fp` idealization,
Layer 2, review item 2); and verdicts, waivers or policy inputs (only
`Accept` and non-acceptance — P4's partition, joined in prose, review
item 3).

### 2e. Read and never used (Q1d)

As Q2 §1e. Both `AuthorityPublished*` events are fired (157, 161) and
never queried.

---

## 3. Q1r — `sp1_q1_strict_repo_compromised.pv` (strict, repo key leaked)

Line for line the same file as Q1d except lines 5, 17, 41, 49, 70
(variant name and header wording), the mutant filenames quoted in the
CORRECTION item 10 and item 5 blocks (73, 84–88, 90–91, 95), and
207–208: `out(c, skR)` — the
**repository** key is leaked and the DNS key stays honest. Every table
in §2 applies with DNS and repository exchanged: line 179 (DNS
evidence) is the load-bearing channel check for (i) and 180 the inert
one. Results are identical: `.out:201` (i true), `:208` (ii true),
`:396` (N1 reachable). The point of running both (spike convention,
`PREDICTIONS.md` "Adversary and modes") is that neither channel's
honesty is assumed by name.

---

## 4. Q3 — `sp1_q3_companionA_sig_unbound.pv` (broken companion A)

### 4a. Cast — differences from Q2

| Name | What it is | Built | Consumed |
|---|---|---|---|
| `fbSigned` | whatever bytes `sg` actually signs — **read and never compared to `fb`** | 79 | nothing |
| everything else | Q2's declarations at 41–50, queries 53–58 and 67–68, verifier 70–83, issuer 85–93, judges 95–103, main 105–116 | | |

### 4b. The verifier's checks — difference from Q2

| Line | Q2 | Q3 | Plain meaning of the change |
|---|---|---|---|
| 79 (Q2:177) | `let (=BYTES, =fb) = checksign(sg, kX)` | `let (=BYTES, fbSigned: bitstring) = checksign(sg, kX)` | the verifier confirms that `sg` is a genuine `BYTES`-signature under `kX` — over *something* — and then goes on with the **presented** `fb`. The detached-signature integrity bug: "the signature checks out" without "…over these bytes" |

All other checks (73–76, 80–81) are Q2's, unchanged.

### 4c. Results (`.out`)

| Query | Line | Result | Meaning |
|---|---|---|---|
| headline | 331 | **false — red as required** | trace 330; derivation 171 |
| N1 | 510 | **reachable** | the companion's honest flow is alive, so its red means something |
| unrestricted (ii) | 663 | false | as in Q2 (registered red); not a discriminator |

### 4d. Claim, adversary, boundary — and why the attack succeeds

**What this model shows.** Nothing about P1. It shows that the
checking arrangement (judge H + the correspondence) *detects* the
bytes-substitution threat when the defense is removed: an honest
signature over one frame is accepted as vouching for a different
frame under the honest key.

**The attack (`.out:171`, trace 330).** The adversary hands issuer 2 a
payload `a_2`; issuer 2 signs `framed(OT_ATTEST, algH, issuerId2,
fp(pk(skI2)), h(m2), canonVerH, a_2)` and records exactly that at 91.
The adversary then presents that signature together with
`framed(a_4, algH, issuerId2, fp(pk(skI2)), h(m2), a_5, a_6)` — object
type, canonicalization version and **payload** all replaced with
values of its own. Line 79 verifies the signature (it is genuine) and
ignores what it signed; lines 80–81 pass because the four pinned
fields are untouched; the verifier accepts under `pk(skI2)`; judge H
fires; no `IssuerSigned` matches. The registered trace-inspection rule
(`PREDICTIONS.md` Q3) is met: the accepted frame appears in no
issuance event.

**What the adversary could *not* alter (RESULTS F4).** `alg`, `id`,
`fp`, `mh` — pinned at 80 to the manifest `t`, which line 76 pins to
the honest issuer's own manifest (only the honest key self-signs
`m2`). So with the signature detached, the P3 field list plus
possession-over-manifest still protects the *binding* fields; it does
not protect the payload, which is the attested thing. Defense in depth
for identity, not a mitigation of the integrity failure.

**Boundary.** A companion discharges nothing. It does not show that
the real verifier has this bug or does not; it shows the query would
see it.

### 4e. Read and never used (Q3)

As Q2, plus `fbSigned` (79) — the one deliberately unused value.

---

## 5. Q4 — `sp1_q4_companionB_frame_unsigned.pv` (broken companion B)

### 5a. Cast — differences from Q2

| Name | What it is | Built | Consumed |
|---|---|---|---|
| `sg` (issuer) | **`sign((BYTES, payload), skI)` — the payload alone**, not the frame | 93 | read 69; checked 79 |
| `fb` (issuer) | the frame the issuer *intends* and records (`IssuerSigned`, `honestCh`) — but does not sign | 90 | 91, 92 |
| `pl` (verifier) | the payload field of the presented frame, now the thing the signature is checked against | 75 | 79 |
| everything else | Q2's, at 38–47, 50–55, 64–65, 67–81, 85–93, 95–103, 105–116 | | |

### 5b. The verifier's checks — difference from Q2

| Line | Q2 | Q4 | Plain meaning of the change |
|---|---|---|---|
| 75–76 | same pattern and hash check | same, moved before the signature check | frame fields checked against the manifest as before |
| 79 (Q2:177) | `let (=BYTES, =fb) = checksign(sg, kX)` | `let (=BYTES, =pl) = checksign(sg, kX)` | the signature must cover the **payload**; the six frame fields are outside it |

### 5c. Results (`.out`)

| Query | Line | Result | Meaning |
|---|---|---|---|
| headline | 328 | **false — red as required** | trace 327; derivation 171 |
| N1 | 504 | **reachable** | honest flow alive |
| unrestricted (ii) | 654 | false | as in Q2; not a discriminator |

### 5d. Why the attack succeeds, and its boundary

**The attack (`.out:171`, trace 327).** Issuer 2 signs `(BYTES, a_2)`
and records `framed(OT_ATTEST, …, canonVerH, a_2)`. The adversary
presents `framed(a_4, algH, issuerId2, fp(pk(skI2)), h(m2), a_5, a_2)`:
the payload is the honest one, so line 79 passes; `alg`, `id`, `fp`,
`mh` are the manifest's, so 75–76 pass; **object type and
canonicalization version** — the two fields the manifest does not
carry and the verifier reads without checking (S-P3 F7) — are the
adversary's. Accepted under `pk(skI2)`; no `IssuerSigned` matches
(RESULTS F6).

**What it means.** A frame whose fields sit outside the signature is
integrity-protected only where the manifest happens to pin it. The
plan's 0.10 branch — "the manifest pins every frame field, so the
companion cannot fail" — did not fire, because the reused verifier
leaves `ot` and `cv` unpinned, as the record said it would.

**Boundary.** As Q3: discharges nothing. Whether the object-type
field's integrity is P1's to protect or P7/P8's is the contestable
placement recorded in `PREDICTIONS.md` (Q4) and left open by the run.

### 5e. Read and never used (Q4)

As Q2 §1e; `pl` is now used (79).

---

## 6. The probes (`proverif/probes/`) — not models, not registered

Seven one-line ablations of Q2, run to locate the load and label the
tables above. p1–p5 remove one carried check each (headline stays
true); p6 removes the load-bearing check (headline false); p7 runs Q2
unchanged against `lib_total_eo_failure.pvl`, a library copy in which
any public key verifies any signature (headline false — `.out:171`
shows a derivation with no `IssuerSigned` at all). None is cited as
evidence for P1; they are cited only for the LOAD-BEARING / CARRIED
labels. `probes.log` has rc and box for each.

## 7. Observations about the testimony (comments), not the proofs

- Q2's header sentence "Confirmed by the S-P1 probes … only this
  check, and the unforgeability of sign, move the headline" (lines
  37–39 when the provenance note was written; lines 41–47 now, where
  the cross-family review's single-removal matrix is added as
  independent confirmation) was written before the probes existed and
  confirmed by them afterwards; the dated provenance note at the end
  of that file says so (skeptic pass 2, 2026-09-06). The sentence is
  true; the order of events was not on the record until the note.
- Q3's header (lines 22–29) says the companion's mutation is "one
  line"; after the build fix it is one line with one added type
  annotation, and the header says so (27–29).
- Q1d/Q1r headers called the honest channel's evidence check
  load-bearing for (i) "inferred from S-P3 F1, not ablated here"
  (lines 34–41 as written). That was accurate then and is no longer
  the standing claim: the cross-family review ablated it, and the
  headers (now lines 37–46, with CORRECTION item 10 at 72–92) state
  the dependency as observed — (i) red on removing the honest evidence
  check, its key equality, its digest equality, the fingerprint match
  or the manifest destructuring, and green when only the evidence
  domain tag is unbound. §2b above carries the same narrowing with the
  mutant `.out` lines. The manifest destructuring was missing from the
  old list altogether (review item 10).
- Every `.pv` line number in the **body** of this document was
  converted on 2026-09-06, when the review's narrowings were written
  into the three correct models' headers in place: **+66** for Q1d/Q1r body lines, **+59** for
  Q2's; Q3 and Q4 were not edited and their numbers are unchanged. The
  conversion table sits in the LINE-COUNT NOTE at the end of each
  edited file. The reviewer's own `D:nn`/`R:nn`/`G:nn` citations in
  `docs/reviews/2026-09-06-codex-suite-falsification-s-p1-s-p2-s-p7-s-standing.md`
  are in the pre-review numbering and were deliberately not rewritten:
  that document is the review as received. The dated entries in the
  review log below likewise keep the numbering they were written in
  (amend-don't-rewrite): old §1b row 120 is now row 179, and old §2b
  rows 113/114/116 are now rows 179/180/182. *(Qualification added
  2026-09-06, skeptic pass 3; the bullet previously said "Every `.pv`
  line number in this document was converted", which those entries
  contradict.)*
- The unrestricted contrast (ii) is present in the companions (Q3:67–68,
  Q4:64–65) and red there; the headers do not claim it as a
  discriminator, and RESULTS says so under "Companion isolation".

## 8. Routed to the author

Nothing from the reading aids. (The one read `RESULTS.md` asks for is
named there: Q2's header and verifier against P1's sentence.) The
cross-family review of 2026-09-06 routed three design questions to the
author (`formal/suite/ROUTED-2026-09-06.md` C8–C10); **none of them is
S-P1's** — they are S-P2's common-content question, S-P7's wrapper
version record, and S-STANDING's tuple-to-core binding. S-P1's own
findings were all disposed as Accepted, Boundary or Recorded, so this
family adds nothing to the routed list.

## Review log

- 2026-09-06 — drafted by the AI collaborator from the five
  working-tree `.pv`/`.out` files (uncommitted; "committed" corrected
  2026-09-06, skeptic pass 2), the seven probe outputs, and `RESULTS.md`. No
  lower-ceiling reader probe run yet; no blind Part-B translation
  (the first-link Q3 aid's cross-family half) dispatched yet.
- 2026-09-06 — skeptic pass: §1b row 120 corrected from "all four
  pins" to "all three pattern pins" (p4 removes `=alg`, `=id`,
  `=fp(kX)`; the fourth P3 in-bytes binding is line 121 / probe p3).
  The Q3 `.pv` header correction of the same date kept its line
  count, so every Q3 line cited here (67–68, 79, 22–29) still holds;
  the dated correction note sits at the end of that file.
- 2026-09-06 — skeptic pass 2: the preamble overclaimed that every
  LOAD-BEARING / CARRIED label came from S-P1's own runs; amended to
  except the rows marked *inferred* (§1b domain tags → S-P3 F7; §2b
  rows 113/114/116 → S-P3 F1), which were already honest in place. §1b
  domain-tag sentence now says "inferred from S-P3 F7; no S-P1 probe
  ablates a tag". §7 gains the Q2 header provenance observation. The
  Q2 `.pv` gained a comment-only note at its end (line count
  preserved), so every Q2 line cited here still holds; ladder run 5
  and the probe re-run left every `.out` byte-identical
  (`RESULTS.md` review log).
- 2026-09-06 — cross-family falsification review applied (Codex,
  `gpt-6-astra`; the review is
  `docs/reviews/2026-09-06-codex-suite-falsification-s-p1-s-p2-s-p7-s-standing.md`,
  items 1–11 for this family). Changes here, none of them to a query,
  a result or a `.pv` check: §0.2 gains the item-6 record that N1 is a
  vacuity guard and not coverage; §1b gains the item-4 caution that the
  review's matrix agrees with p1–p7 and that single removals license
  neither joint removal nor "inert for the verifier"; §2b's rows
  179–183 and 186–187 are restated from *inferred* to *ablated*, a new
  row 181 records the manifest-destructuring dependency the strict
  headers had omitted, and row 180 records that only the evidence
  domain tag is inert for both queries (items 5, 10); §1d and §2d gain
  the three unposable-attack boundaries (items 1–3) and §1d the A5
  inconclusive record (item 11); §7 gains the header-line moves and the
  line-number conversion; §8 records that none of the three routed
  questions is S-P1's. Every `.pv` line citation in this document was
  converted (+66 Q1d/Q1r, +59 Q2) after the review's narrowings were
  written into those headers in place; Q3/Q4 numbers are unchanged.
  *(Read "every … citation in the body": the dated entries in this log
  keep their original numbering — mapping in §7, added 2026-09-06,
  skeptic pass 3.)*
  The mutant `.out` lines cited here were regenerated from the
  archived `.pv` files under
  `proverif/falsification-2026-09-06/scratch/` and match the review's
  quoted RESULT lines exactly (`RESULTS.md` review log). The
  lower-ceiling reader probe is still not run.
- 2026-09-06 — skeptic pass 3 (on the cross-family-review
  application). Line 25's "results in the sibling `.out` files, run 2"
  was stale — `proverif/ladder.log`'s current run is 7 — and now reads
  "ladder run 7 — byte-identical to run 2, whose line numbers this
  document cites"; the byte-identity was re-verified this pass by
  re-running all five models. §7's line-number bullet is qualified to
  the **body** of this document and gains the mapping for the numbers
  the dated entries in this log deliberately keep (old §1b row 120 is
  now row 179; old §2b rows 113/114/116 are now rows 179/180/182);
  those entries themselves are left as written. §8 is unchanged: the
  grep-able "Pending author ruling (ROUTED C8/C9/C10)" line the
  cross-family work order named was added to `RESULTS.md` under
  "Status toward discharge", recording that none of C8/C9/C10 is
  S-P1's. No `.pv`, no `.out`, no result and no `PREDICTIONS.md` text
  touched.
