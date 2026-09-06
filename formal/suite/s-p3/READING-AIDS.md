# S-P3 reading aids — cast, checks, and plain-language claim for all eight models

> **STATUS: PROPOSED — 2026-09-06; clerk-drafted by the AI collaborator;
> not adopted; the commit is the author's.** This is *testimony* under
> `formal/suite/ENUMERATION.md` amendment note 5 item 2 (lines 297–312):
> reading aids for non-expert readers, reviewed by the lower-ceiling
> reader probe, **not a gate for exit**. Nothing here changes a query, a
> result, a header, or a `.pv` file. Every statement about a model cites
> `file:line`; every statement about which check carries which result
> cites `RESULTS.md` F1–F8 (lines 77–199) or the dependency statement
> (lines 194–199) — the source of truth for LOAD-BEARING vs CARRIED is
> F7 (lines 149–162). Where the aid noticed something in a model's
> *comments* that reads wrong, it is recorded in §9 as an observation
> about the testimony, never as a verdict on the proof, and not changed.
>
> Form follows the Codex review's walk-through
> (`docs/reviews/2026-09-04-codex-sp3-q2-review.md` lines 43–66): a
> checks table, a short "why the attack fails" (or, for
> companions, "why it succeeds") paragraph, and the boundaries.

Files this document reads (all under `formal/suite/s-p3/proverif/`,
run 3 = recut 3, results in the sibling `.out` files; `run2/` not read):

| Short name | File | Kind |
|---|---|---|
| Q1d | `sp3_q1_strict_dns_compromised.pv` | correct, strict, DNS key leaked |
| Q1r | `sp3_q1_strict_repo_compromised.pv` | correct, strict, repo key leaked |
| Q2 | `sp3_q2_degraded_compromised.pv` | correct, degraded, sole channel leaked — **the P3 claim** |
| Q3 | `sp3_q3_companionA_frame_unbound.pv` | broken companion A |
| Q4 | `sp3_q4_companionB_possession_unnamed.pv` | broken companion B |
| Q5c | `sp3_q5_multikey_correct.pv` | correct, two signers |
| Q5n | `sp3_q5_multikey_companion_noFpB.pv` | registered companion (could not go red, F3) |
| Q5u | `sp3_q5_multikey_companion2_unboundB.pv` | added companion (red on B only) |

Library: `formal/suite/lib/tessera_theory.pvl` (cited as `lib:N`).
Property text: `docs/phase-0-prereg-amendment-1.md` P3 at lines 130–151;
adversary A1.3 at lines 331–347.

---

## 0. Typing note (once, for every model)

- **All tuples are `bitstring`.** ProVerif has no record or struct
  types; a manifest, a frame, a piece of channel evidence, a possession
  proof and an attestation signature are all `bitstring` values. **Shape
  lives in construction and pattern matches, never in declarations.**
  A manifest is a manifest because it was built with `authTuple(...)`
  (`lib:128`) and is later taken apart with the pattern
  `let authTuple(id, kfpr, ss, alg, ver) = t in`; nothing in a `free` or
  `fun` line says "this is a manifest".
- **The `: bitstring` annotations on pattern variables carry no
  information.** `in(c, (t: bitstring, ev: bitstring, ...))` says only
  that these are bitstrings — which everything already is. Read them as
  names, not as types.
- **`pkey` / `skey` are declared types (`lib:75–76`) but ProVerif's
  default does not enforce types against the adversary.** The adversary
  may present any term where a `pkey` is expected. What actually
  constrains the accepted key is the *checks* (fingerprint match,
  signature verification), never the type annotation on `kX: pkey`.
- **`=x` in a pattern means "must equal the value already bound to x";
  a bare name means "read this and bind it".** So
  `let framed(ot, =alg, =id, =fp(kX), mh, cv, pl) = fb in` checks three
  fields and merely reads four. This one distinction is most of what a
  reader needs to tell a check from a read.
- **`[data]` on a constructor** (`framed`, `authTuple`) means it is
  transparent: the adversary can build one from parts and take one
  apart. `sign`, `h`, `fp` are *not* `[data]`: they can be built by
  anyone who has the inputs but never inverted, except by the
  `checksign` rules (`lib:80–84`).
- **`!P` means unboundedly many copies of P.** Every honest role and
  the verifier are replicated; there are unboundedly many sessions.
- **Two idealizations carry the whole result** and are declared in the
  library, not in any model: `fp` is injective (`lib:87–97`) and `h` is
  injective (`lib:99–111`). F5 (RESULTS 128–140) locates the entire
  load of the S-P3 results on the `fp` idealization.

## 0.1 Shared cast — the library terms every model uses

| Name | What it is in the design (plain words) | Declared (lib) | Used in the models |
|---|---|---|---|
| `c` | the public network; everything the adversary sees and can inject | 57 | every `in(c, …)`/`out(c, …)` |
| `skey`, `pkey`, `pk` | private key, public key, and the map from one to the other | 75–77 | every key |
| `sign(m, k)`, `checksign(s, pk)` | deterministic signature with message recovery: `checksign` returns the signed message if `s` verifies under `pk` | 78, 80–84 | every evidence/possession/attestation check |
| `dsks(s, r)` | **the A1.3 item 3 capability (D-4):** from one seen signature `s` and a fresh `r`, a private key the adversary *holds* whose public key verifies `s` to the same message. Grants nothing else (`lib:60–74`) | 79, 83–84 | never in an honest process; only via the adversary. Appears in a derivation only in Q4 (`.out:238–247`) |
| `fp(pk)` | key fingerprint; **idealized injective** | 97 | manifests, frame field, verifier check |
| `h(x)` | hash; **idealized injective** | 111 | manifest hash in evidence and frame |
| `STMT_DIGEST` | tag: "this is authority evidence in digest form" (transcription binding, the selected first-link form) | 119 | channel evidence |
| `POSS` | tag: "this is a manifest self-signature (proof of possession)" | 120 | possession proof |
| `BYTES` | tag: "this is the attestation signature over framed bytes" | 121 | attestation signature |
| `STMT_DIRECT` | tag for the direct binding form | 118 | **declared in the library, used by no S-P3 model** |
| `authTuple(id, kfp, sset, alg, ver)` | **the key statement — the map-v1 authority tuple = the manifest as this suite models it:** issuer identity, key fingerprint, signer-set, algorithm id, statement version | 128 | `m`, `m2` in every model |
| `issuerId`, `ssetH`, `algH`, `verH` | the honest issuer's identity, signer-set, algorithm, version — public fixture values | 133–136 | `m` in every model |
| `fbH` | the spike's honest framed bytes fixture | 137 | **used by no S-P3 model** (was shadowed by judge locals before recut 3; RESULTS 64–73) |
| `AuthorityPublishedDNS(t)`, `AuthorityPublishedRepo(t)` | "the DNS / repository authority channel published manifest `t`" | 143–144 | fired by channel processes; queried only in Q1d/Q1r |
| `IssuerPossession(k)` | "the honest issuer demonstrated possession of `k`" | 145 | fired in every issuer; queried only in Q1d/Q1r |
| `IssuerSigned(k, fb)` | "the honest issuer signed framed bytes `fb` under `k`" | 146 | fired in every issuer; queried only in Q1d/Q1r |
| `Accept(evD, evR, t, k, fb)` | strict-mode acceptance (two evidences, tuple, accepted key, bytes) | 147 | Q1d/Q1r only; Q2–Q4 declare `AcceptS`, Q5 declares `Accept2` |

## 0.2 The judge idiom (shared by all eight)

Registered in `PREDICTIONS.md` lines 128–143 before any run. The
honest issuer reports `(its key, the bytes it framed)` on a private
channel that the adversary cannot see; the verifier reports
`(accepted key, identity, accepted bytes)` on another. A **Judge**
process pairs an honest report and an acceptance for the *same bytes*
(the `=fbHon` pattern) and fires:

- `HonestAccepted(kX, fb)` when the accepted key *is* the signer's — the
  N1 honest-flow witness, which must be **reachable** (recut 3, RESULTS
  64–73; suite rule, RESULTS 277–283);
- `Reattributed(kX, kH, fb)` when it is not — the P3 threat, which must
  be **unreachable** in correct models.

A **PossJudge** does the same for possession proofs: honest
`(key, proof)` versus accepted `(key, proof presented)`, firing
`PossessionTransplanted(kX, p)` on a key mismatch over the same proof
term.

Two consequences a reader should hold onto: (1) the judge compares
**keys**, not identities — the `id` it receives is bound and never
used, which is F8 (RESULTS 164–174) and the author's ruling of
2026-09-05 (RESULTS 176–192, quoted in §3d below); (2) the judge is
keyed on the *exact* honest bytes, so it says nothing about bytes the
adversary signed itself (impersonation), `PREDICTIONS.md` 141–143.

---

## 1. Q1d — `sp3_q1_strict_dns_compromised.pv`

### 1a. Cast

| Name | What it is in the design | Built | Consumed |
|---|---|---|---|
| `skD` | DNS authority channel's signing key — **leaked in this variant** | 156 | 104 (signs evidence), **162 `out(c, skD)`**, 159, 166 |
| `skR` | repository channel's signing key — honest here | 156 | 108, 159, 166 |
| `skI`, `skI2` | the two honest issuers' signing keys (N2: two honest values on the issuer axis) | 156 | 157/158 (fingerprint into manifest), 159 (public keys published), 165 |
| `m`, `m2` | **the key statement (manifest):** `authTuple(issuerId, fp(pk(skI)), ssetH, algH, verH)` and its twin for issuer 2 | 157, 158 | 160 (published), 163–164 (both channels sign each), 165 → 116 (self-signed as possession), 119 (hashed into the frame) |
| `payload` | **the thing attested:** content the issuer signs over; adversary-chosen (chosen-message issuer) | read 114 | 119 (inside the frame) |
| `framed(...)` | model-local constructor: the P3 field list as a transparent 7-tuple (objType, alg, issuerId, kfp, manifestHash, canonVer, payload) | 62 | built 119; matched 138 |
| `fb` (issuer) | the framed bytes — the signed object of the attestation | 119 | 120 (event), 121 (report to judge), 122 (signed) |
| `sg` | the attestation signature `sign((BYTES, fb), skI)` | 122 | read 126; checked 136 |
| `ppf` | the possession proof — the **manifest self-signature** `sign((POSS, m), skI)` (D-3; A1.5 item 3) | 116 | 117 (report), 118 (published), read 126; checked 134; 141 (report) |
| `evD`, `evR` | authority evidence, one per channel: `sign((STMT_DIGEST, h(t)), skCh)` | 104, 108 | read 125; checked 128, 129; carried in `Accept` 140 |
| `objTypeH`, `canonVerH` | honest object type and canonicalization version; public | 64, 65 | 119 |
| `issuerId2` | second honest issuer's identity | 66 | 158, 165 |
| `t` | verifier's local: the manifest the package *presents* | read 125 | 128, 129 (evidence must be over `h(t)`), 130 (destructured), 134 (possession must be over `t`), 139, 140 |
| `id`, `kfpr`, `ss`, `alg`, `ver` | fields of `t` | 130 | `kfpr` 132; `id` 138, 141; `alg` 138; **`ss`, `ver` never used** |
| `kX` | verifier's local: the key the package presents as signer | read 126 | 132, 134, 136, 138, 140, 141 |
| `ot`, `mh`, `cv`, `pl` | frame fields read at the verifier | 138 | `mh` 139; **`ot`, `cv`, `pl` never used** |
| `honestCh`, `acceptCh`, `honestPossCh`, `possCh` | private judge channels (issuer→judge bytes; verifier→judge acceptance; issuer→judge possession; verifier→judge possession) | 69–72 | out 121 / 141 / 117 / 141; in 144 / 145 / 150 / 151 |
| `Reattributed(kX, kH, fb)` | "honest bytes accepted under a key other than their signer's" | 73 | fired 147; queried 81–82 |
| `PossessionTransplanted(kX, p)` | "an honest self-signature accepted as possession for another key" | 75 | fired 153; queried 85–86 |
| `HonestAccepted(k, fb)` | N1 witness: honest bytes accepted under their own key | 76 | fired 146; queried 88–89 |
| `Accept(evD, evR, t, kX, fb)` | strict acceptance (library) | lib:147 | fired 140; queried 92–96 (correspondence), 99–100 (reachability) |
| `Judge`, `PossJudge` | the two judges (§0.2) | 143–147, 149–153 | 167 |
| `AuthorityDNS`, `AuthorityRepo` | the two channels: fire the publication event, then emit evidence | 102–104, 106–108 | 163–164 (each channel publishes **both** honest manifests) |
| `Issuer` | honest issuer: takes a payload, proves possession over its manifest, frames and signs | 113–122 | 165 |
| `Verifier` | strict verifier | 124–141 | 166 |

### 1b. The verifier's checks (lines 124–141)

Caveat on provenance: F7's ablations were run on **Q2** (RESULTS
149–162; review record `docs/reviews/2026-09-05-blind-falsification-sp3-q2.md`).
Q1's lines 130–139 are Q2's 102–109 line for line in code (Q1 adds
comment lines at 131 and 135), so F7's assignments are carried to them
here; for the two channel checks,
which Q2 does not have, F1 (RESULTS 77–85) is the source.

| Line | Check | Plain meaning | Status |
|---|---|---|---|
| 128 | `let (=STMT_DIGEST, =h(t)) = checksign(evD, pkD)` | the DNS evidence is a DNS-key signature over exactly the digest of the presented manifest | **Inert — inferred, not ablated** (no Q1 ablation is in the record): the channel key is public at 162, so the adversary produces this evidence for any `t`; F6/M1 (RESULTS 142–147; falsification record M1) is the Q2 result, carried here by the same reasoning |
| 129 | `let (=STMT_DIGEST, =h(t)) = checksign(evR, pkR)` | same, for the honest repository channel | **LOAD-BEARING for Q1** — F1: "strict mode (Q1) is carried by the cross-channel fingerprint agreement before the frame is even inspected." The honest channel only ever signs `h(m)` and `h(m2)` (164), so `t` is pinned to an honestly published manifest |
| 130 | `let authTuple(id, kfpr, ss, alg, ver) = t` | read the manifest's fields | structural (a read, not a check) |
| 132 | `if fp(kX) = kfpr` | the presented key is the one the manifest names | **LOAD-BEARING for `PossessionTransplanted`** (jointly with 134 — dependency statement; falsification record M2, M3 on Q2's identical line 103); **for `Reattributed` only via the redundant route with 139** (M10; dependency statement: the frame's `=fp(kX)` at 138 alone suffices). F5's "whole load is `fp` injectivity" is about the idealization both routes rest on, not about this line carrying the P3 claim by itself |
| 134 | `let (=POSS, =t) = checksign(ppf, kX)` | the presented key has self-signed *this* manifest (possession over the manifest, D-3) | **LOAD-BEARING** for `PossessionTransplanted` (dependency statement); the result it protects is an A1.5/P10 result **CARRIED** in S-P3, not a P3 result (header 54–55; RESULTS ledger entry 2, 217–227) |
| 136 | `let (=BYTES, =fb) = checksign(sg, kX)` | the presented key signed exactly the presented framed bytes | **LOAD-BEARING for the first-link correspondence** (92–96, `IssuerSigned(k, fb)` conjunct) — F7: "Q1's strict-mode first-link correspondence exercises it already"; for `Reattributed` it is **unexercised** (F7), and the authorship claim it supports is **CARRIED to S-P1** |
| 138 | `let framed(ot, =alg, =id, =fp(kX), mh, cv, pl) = fb` | the signed bytes name the same algorithm, identity and key fingerprint the manifest does; object type, hash, version, payload are read | `=fp(kX)`: **LOAD-BEARING** (F7). `=alg`, `=id`: **CARRIED** (F7: algorithm → A3 §1 identifier-binding invariant; identity → F8). `ot`, `cv`: **CARRIED** unchecked (F7: object type → P7; canonicalization version → P8/H1a) |
| 139 | `if mh = h(t)` | the signed bytes commit to this manifest | **LOAD-BEARING, redundantly with `=fp(kX)`** (F3, RESULTS 100–113; F7) |
| 140 | `event Accept(...)` | acceptance | the event the correspondence and N1 queries are about |
| 141 | `( out(possCh, …) \| out(acceptCh, …) )` | report to the judges, **in parallel** with nothing else (recut 1) | encoding rule, RESULTS 40–56 |

Domain tags `STMT_DIGEST`/`POSS`/`BYTES` are present in 128/129/134/136:
**CARRIED** — F7 lists the domain tag among the five unexercised fields.

### 1c. Results (`.out`)

| Query | Line in `.out` | Result | Meaning |
|---|---|---|---|
| `Reattributed` | 223 | unreachable (`is true`) | no honest bytes accepted under another key |
| `PossessionTransplanted` | 228 | unreachable | no honest self-signature accepted for another key |
| `HonestAccepted` | 416 | **reachable** (`is false`) | N1: the honest flow does get accepted (trace at 233: adversary picks a payload, issuer 2 frames and signs, verifier accepts under `pk(skI2)`) |
| first-link correspondence | 424 | true | every acceptance was preceded by an honest publication of `t`, possession of `k`, and `k` signing `fb` |
| `Accept` reachable | 587 | reachable | the bare acceptance witness (kept alongside the honest one) |

### 1d. Claim, adversary, boundary (plain language)

**Claim (header 10–16, F1).** With two authority channels both
required and one of them (DNS) fully compromised, a relying party who
runs these checks will never accept an honest issuer's signed bytes as
if they were signed by some other key, and will never accept an honest
issuer's manifest self-signature as proof that some *other* key owns
that manifest — even against an adversary who can manufacture, after
the fact, a key that verifies any one signature it has seen. The
spike's first-link result (acceptance implies honest publication,
possession and signing) still holds with the structured frame.

**Adversary (A1.3, prereg 331–347; header 10–12; fixture 159–162).**
Sees everything on `c`; holds the DNS channel's private key (162) and
so can publish any manifest through DNS; can choose every payload the
honest issuers sign (114); can build manifests and frames freely
(`[data]`); has the DSKS capability (`lib:79–84`); holds every key it
uses. Does **not** hold `skR`, `skI`, `skI2`.

**Why the attack fails (Q1 form).** The honest repository channel signs
only `h(m)` and `h(m2)` (164), so the manifest the verifier is shown
must be one of the two honest ones (129, `h` injective). That manifest
names an honest fingerprint, so 132 forces the presented key to be the
honest key (`fp` injective). A DSKS-derived key has a different
fingerprint and is rejected at 132 before the possession or attestation
signature is examined — which is what F1 means by "carried by the cross-channel fingerprint
agreement before the frame is even inspected".

**Boundary (header 17–20; RESULTS 256–275).** Not the degraded case
(that is Q2). Nothing about the verification profile (library,
encodings, low-order points — P3's [assumption] half, H1a). Nothing
about the frame's byte layout (P8): `framed(...)` is a perfectly
parsed 7-tuple, not a byte format. Nothing about whether an issuer
identity is *valid*. Nothing about bytes the adversary signed itself
(impersonation). Both `fp` and `h` are collision-free by fiat
(`lib:87–111`): the result is a statement about a perfect fingerprint
(F5). Object type and canonicalization version are bound but not
checked for support (RESULTS 266–271).

### 1e. Read and never used (Q1d)

`ss`, `ver` (130); `ot`, `cv`, `pl` (138); the judge's `id` (145 —
F8). `STMT_DIRECT`, `fbH` from the library. Everything else declared
in this file is consumed.

---

## 2. Q1r — `sp3_q1_strict_repo_compromised.pv`

Line for line the same file as Q1d except line 3 (variant name), line
35 (run command), and lines 161–162: `out(c, skR)` — the **repository**
key is leaked and the DNS key stays honest. Every table in §1 applies
with these substitutions:

- In §1a, `skR` is the leaked key (162) and `skD` the honest one.
- In §1b, line 128 (DNS evidence) is the **LOAD-BEARING** channel
  check per F1, and line 129 (repository evidence) is the inert one
  (inferred, not ablated, as in §1b row 128).
- §1c results are identical: `.out` 223 (Reattributed unreachable),
  228 (PossessionTransplanted unreachable), 416 (HonestAccepted
  reachable), 424 (correspondence true), 587 (Accept reachable).

**Claim / adversary / boundary:** as §1d with "DNS" and "repository"
exchanged. The point of running both variants (PREDICTIONS 110–113:
"a generic single channel is not accepted as representing both") is
that neither channel's honesty is assumed by name; whichever survives
carries the strict-mode result.

**Read and never used:** as §1e.

---

## 3. Q2 — `sp3_q2_degraded_compromised.pv` (the P3 claim)

### 3a. Cast

| Name | What it is in the design | Built | Consumed |
|---|---|---|---|
| `skS` | the **sole** authority channel's signing key — **leaked** (degraded mode, channel compromised) | 144 | 91 (signs evidence), **150 `out(c, skS)`**, 147, 153 |
| `skI`, `skI2` | the two honest issuers' keys | 144 | 145/146, 147, 152 |
| `m`, `m2` | **the key statement (manifest):** `authTuple(issuerId, fp(pk(skI)), ssetH, algH, verH)`; twin for issuer 2 | 145, 146 | 148 (published), 151 (channel signs each), 152 → 123 (self-signed), 126 (hashed into frame) |
| `payload` | **the thing attested**; adversary-chosen | read 121 | 126 |
| `framed(...)` | the P3 field list as a transparent 7-tuple | 60 | built 126; matched 108 |
| `fb` (issuer) | the framed bytes | 126 | 127, 128 (report), 129 (signed) |
| `sg` | attestation signature `sign((BYTES, fb), skI)` | 129 | read 100; checked 106 |
| `ppf` | possession proof `sign((POSS, m), skI)` — manifest self-signature | 123 | 124 (report), 125 (published); read 100; checked 105; 111 (report) |
| `ev` | the sole authority evidence `sign((STMT_DIGEST, h(t)), skS)` | 91 | read 99; checked 101; 110 |
| `objTypeH`, `canonVerH`, `issuerId2` | fixture values | 62–64 | 126; 146/152 |
| `t` | the presented manifest | read 99 | 101, 102, 105, 109, 110 |
| `id`, `kfpr`, `ss`, `alg`, `ver` | fields of `t` | 102 | `kfpr` 103; `id` 108, 111; `alg` 108; **`ss`, `ver` never used** |
| `kX` | the presented key | read 100 | 103, 105, 106, 108, 110, 111 |
| `ot`, `mh`, `cv`, `pl` | frame fields | 108 | `mh` 109; **`ot`, `cv`, `pl` never used** |
| judge channels | as §0.2 | 67–70 | out 128 / 111 / 124 / 111; in 132 / 133 / 138 / 139 |
| `Reattributed`, `PossessionTransplanted`, `HonestAccepted` | as §0.2 | 71, 73, 74 | fired 135, 141, 134; queried 79–80, 83–84, 86–87 |
| `AcceptS(ev, t, kX, fb)` | model-local degraded acceptance: one evidence, tuple, key, bytes (spike Q5 shape) | 96 | fired 110; queried 114–115 |
| `AuthorityS` | the sole channel: fires `AuthorityPublishedDNS(t)` (library event, **never queried here**), emits evidence | 89–91 | 151 |
| `Issuer`, `VerifierS`, `Judge`, `PossJudge` | roles | 120–129, 98–111, 131–135, 137–141 | 152–154 |

### 3b. The verifier's checks (lines 98–111) — F7 is the source of truth

| Line | Check | Plain meaning | Status |
|---|---|---|---|
| 101 | `let (=STMT_DIGEST, =h(t)) = checksign(ev, pkS)` | the sole authority evidence endorses exactly this manifest | **Inert by construction** — F6: the channel key is public (150), so this is "the adversary's condition, not something the checks defend against"; removing it changes nothing |
| 102 | `let authTuple(id, kfpr, ss, alg, ver) = t` | read the manifest's fields | structural |
| 103 | `if fp(kX) = kfpr` | the presented key is the one the manifest names | **LOAD-BEARING for `PossessionTransplanted`** (jointly with 105 — dependency statement; falsification record M2, M3: removing 103 alone leaves `Reattributed` unreachable and makes `PossessionTransplanted` reachable); **for `Reattributed` only via the redundant route with 109** (M10; dependency statement: "the frame's fingerprint field alone suffices against re-attribution" — that is 108's `=fp(kX)`). F5's "whole load is `fp` injectivity" names the idealization both routes rest on; it does not make this line carry the P3 claim by itself |
| 105 | `let (=POSS, =t) = checksign(ppf, kX)` | the presented key self-signed *this* manifest | **LOAD-BEARING** for `PossessionTransplanted`, jointly with 103 (dependency statement); an A1.5/P10 result **CARRIED** in S-P3 (header 52–53; ledger entry 2) |
| 106 | `let (=BYTES, =fb) = checksign(sg, kX)` | the presented key signed exactly these framed bytes | **Unexercised by both Q2 queries** (F7: "The attestation-signature check itself is unexercised by re-attribution"); the authorship claim is **CARRIED to S-P1** |
| 108 | `let framed(ot, =alg, =id, =fp(kX), mh, cv, pl) = fb` | the signed bytes name this algorithm, identity and fingerprint | `=fp(kX)`: **LOAD-BEARING** (F7). `=alg`, `=id`, `ot`, `cv`: **CARRIED** (F7: alg → A3 §1; id → F8; object type → P7; canonVer → P8/H1a) |
| 109 | `if mh = h(t)` | the signed bytes commit to this manifest | **LOAD-BEARING, redundant with `=fp(kX)`** (F3, F7; dependency statement: "the tuple fingerprint match and the manifest-hash check together compensate for its absence, and neither alone does") |
| 110 | `event AcceptS(...)` | acceptance | N1 target (114–115) |
| 111 | parallel reports | recut 1 | encoding |

Domain tags: **CARRIED** (F7; falsification record M12: collapsing
`POSS` and `BYTES` to one tag changes nothing).

### 3c. Results (`.out`)

| Query | `.out` line | Result |
|---|---|---|
| `Reattributed` | 195 | unreachable — **the P3 [model] claim** |
| `PossessionTransplanted` | 200 | unreachable |
| `HonestAccepted` | 376 | reachable (trace at 205: adversary-chosen payload, issuer 2 signs, accepted under `pk(skI2)`) |
| `AcceptS` | 526 | reachable (trace at 381 — note it is an *impersonation* trace: an adversary key `k`, its own manifest, its own frame; this is why the bare witness was replaced by `HonestAccepted` in recut 3) |

### 3d. Claim, adversary, boundary

**Claim (header 10–14, narrowed at 47–55; F1; F5).** In degraded mode
— only one authority channel, and that channel is in the adversary's
hands — a relying party who runs these checks will never accept an
honest issuer's signed bytes under a key other than the one that
signed them, and will never accept an honest manifest self-signature
as possession for another key. The honest sentence for what this
discharges is F5's: *under a perfect fingerprint, key substitution
cannot move an acceptance of honest bytes to another key.*

**Adversary (A1.3; header 10–12; 147–150).** Everything in §1d plus:
it holds the *only* authority key (150), so it can make the channel
say anything. This is stronger than A1.3 item 6, which licenses a
*proper* subset of channels (F6). It holds the DSKS capability. It
still does not hold `skI` or `skI2`.

**Why the attack fails (Codex review lines 58–66, checked against 103,
108, 109).** The honest framed bytes contain `fp(pk(skI))` (126).
Line 108 demands that the fingerprint inside the bytes equal
`fp(kX)`; `fp` is injective; so `kX = pk(skI)`. Changing the embedded
fingerprint would make different bytes — no longer the existing
message–signature pair the substitution attack was trying to reuse.
Independently, 109 demands the bytes' manifest hash equal `h(t)`, `t`
names `fp(kX)` at 103, and the honest bytes hash the honest manifest;
`h` injective closes the same door a second way (F3). For possession:
the honest `ppf` verifies under any DSKS-derived key, but 103 requires
the manifest to name that key's fingerprint and 105 requires the
possession to be over *that* manifest — the honest self-signature is
over `m`, which names `fp(pk(skI))`, not the derived key (F4). Note
what did *not* matter: the signature check (106) and the channel
check (101) can both be removed and both results stand (F5, F6).

**The identity question (F8, RESULTS 164–174) and the author's ruling.**
The judge compares keys; P3's opening sentence speaks of identity. An
adversary key accepted under an honest *identity* with
adversary-authored bytes is reachable here (that is the `AcceptS`
trace at `.out:381`). The record's disposition, quoted with its
location, RESULTS 176–192:

> **RULED (author), 2026-09-05** […] The narrow reading stands: P3's
> threat is re-attribution of an existing signature; fresh-signature
> impersonation under a usurped identity, with the sole channel
> compromised, is the degraded-mode cost handed to the verifier, not a
> P3 defect. […] Consequence for the relying-party story: degraded-mode
> verdicts carry the evidence of what could not be excluded; they do
> not carry Tessera's judgment of it.

**Boundary (header 15–18; RESULTS 256–275; F5).** Impersonation with
the adversary's own key over its own bytes is reachable and out of
scope. Nothing about the verification profile, the frame's byte
layout, the practicality of DSKS against Ed25519, or the semantic
validity of identities, object types, versions, or algorithm
selection. The manifest here *is* the bare authority tuple: signing,
hashing and binding all act on one object; a richer manifest's
correspondence is P8's and map v1's. The entire result rests on `fp`
being collision-free (F5) — Layer 2; the four things the record owes
about the concrete fingerprint are assigned at RESULTS 232–254.

### 3e. Read and never used (Q2)

`ss`, `ver` (102); `ot`, `cv`, `pl` (108); the judge's `id` (133, F8).
Library events `AuthorityPublishedDNS` (fired 90), `IssuerPossession`
(122), `IssuerSigned` (127) are fired and **never queried** in this
model (no correspondence query; that is Q1's). `STMT_DIRECT`, `fbH`
from the library.

---

## 4. Q3 — `sp3_q3_companionA_frame_unbound.pv` (broken companion A)

### 4a. Cast — differences from Q2

The fixture, channels, judges, keys and manifests are Q2's with shifted
lines (keys 141; `m`, `m2` 142–143; leak 147; roles 148–151; judge
channels 66–69; events 70–73; `AcceptS` 94; `AuthorityS` 87–89;
`Issuer` 117–126; `VerifierS` 96–108; `Judge` 128–132; `PossJudge`
134–138). What changes:

| Name | What it is | Built | Consumed |
|---|---|---|---|
| `framedU(objType, alg, canonVer, payload)` | **the mutation:** framed bytes with no issuer identity, no key fingerprint, no manifest hash — the spike's opaque bytes, made explicit | 76 | built 123; matched 106 |
| `framed(...)` | the correct 7-tuple constructor | 59 | **declared and never used** in this file |
| `fb` (issuer) | `framedU(objTypeH, algH, canonVerH, payload)` | 123 | 124, 125, 126 |
| `PossessionTransplanted` | declared 72, fired 138 | — | **never queried** (queries are 81–85 and 111–112 only; PREDICTIONS 177–191 required only `Reattributed` red here) |

### 4b. The verifier's checks (lines 96–108)

| Line | Check | Status relative to Q2 |
|---|---|---|
| 99 | sole evidence over `h(t)` | present; inert (F6) |
| 100 | destructure `t` | present |
| 101 | `fp(kX) = kfpr` | present (carried unchanged from Q2:103) |
| 103 | possession over `t` under `kX` | present (Q2:105) |
| 104 | attestation signature over `fb` under `kX` | present (Q2:106) |
| 106 | `let framedU(ot, =alg, cv, pl) = fb` | **THE MUTATION:** Q2's 108 (`=id`, `=fp(kX)`) and 109 (`mh = h(t)`) are gone; only `=alg` remains |
| 107 | `event AcceptS` | present |

### 4c. Results (`.out`)

| Query | `.out` line | Result |
|---|---|---|
| `Reattributed` | 359 | **reachable — red as required** |
| `HonestAccepted` | 532 | reachable |
| `AcceptS` | 680 | reachable |

### 4d. Claim, adversary, boundary — and why the attack succeeds

**What this model is for (header 11–14).** It exists to go red on
`Reattributed`; it discharges nothing. Its value is F2's: it shows the
checking arrangement detects the intended failure, and it shows *which*
failure.

**Why the attack succeeds (F2, RESULTS 87–98; trace goal `.out:191`).**
The goal line reads: any key `k ≠ skI2` the adversary holds, and any
payload `pl` the adversary chooses, reach
`Reattributed(pk(k), pk(skI2), framedU(objTypeH, algH, canonVerH, pl))`.
Because the frame carries no identity, fingerprint, or manifest hash,
the honest issuer 2's bytes over payload `pl` (123) are *term-equal* to
the bytes the adversary frames for the same `pl` under its own key. The
adversary publishes a manifest naming `fp(pk(k))` through the channel
it controls (147), self-signs possession over it, signs the frame
under `k`; the verifier accepts `fb` under `pk(k)`; the judge pairs
that acceptance with issuer 2's honest report of the identical `fb`
and fires. **DSKS was not used** (F2). The lesson for the relying
party, in F2's words: under opaque bytes, impersonation and
re-attribution "are *the same event*; the in-bytes binding is what
separates them."

**Adversary.** As Q2 (§3d).

**Boundary.** A companion proves no property (RESULTS 290–293: it
supplies "evidence that the checking arrangement can detect the
intended failures"). This file says nothing about the correct frame.

### 4e. Read and never used (Q3)

`framed` (59); `PossessionTransplanted` (72, fired 138, unqueried);
`ss`, `ver` (100); `ot`, `cv`, `pl` (106); judge's `id` (130); library
events fired at 88, 119, 124 unqueried; `STMT_DIRECT`, `fbH`.

---

## 5. Q4 — `sp3_q4_companionB_possession_unnamed.pv` (broken companion B)

### 5a. Cast — differences from Q2

Same fixture as Q2 with lines: keys 144; `m`, `m2` 145–146; leak 150;
roles 151–154; judge channels 66–69; events 70–73; `AcceptS` 95;
`AuthorityS` 88–90; `Issuer` 120–129 (frame 126 is the **correct**
`framed(...)`); `VerifierS` 97–111; `Judge` 131–135; `PossJudge`
137–141. What changes:

| Name | What it is | Built | Consumed |
|---|---|---|---|
| `mAny` | **the mutation:** whatever manifest the presented possession proof happens to cover — read, not compared to `t` | 105 | **never used** |

### 5b. The verifier's checks (lines 97–111)

| Line | Check | Status relative to Q2 |
|---|---|---|
| 100 | sole evidence over `h(t)` | present; inert (F6) |
| 101 | destructure `t` | present |
| 102 | `fp(kX) = kfpr` | present (Q2:103) |
| 105 | `let (=POSS, mAny: bitstring) = checksign(ppf, kX)` | **THE MUTATION:** Q2:105 demanded `=t`; here the possession proof need only verify under `kX` as *some* `POSS` object |
| 106 | attestation signature | present (Q2:106) |
| 108 | frame parse with `=alg`, `=id`, `=fp(kX)` | present — **the frame binding is intact** (header 16–17) |
| 109 | `mh = h(t)` | present |
| 110 | `event AcceptS` | present |

### 5c. Results (`.out`)

| Query | `.out` line | Result |
|---|---|---|
| `Reattributed` | 195 | unreachable (frame binding intact, as the header 16–17 expected) |
| `PossessionTransplanted` | 383 | **reachable — red as required, and the only red in the ladder whose derivation uses `dsks`** (F4; `.out:238–247`) |
| `HonestAccepted` | 559 | reachable |
| `AcceptS` | 713 | reachable |

### 5d. Claim, adversary, boundary — and why the attack succeeds

**What this model is for (header 10–15).** To go red on
`PossessionTransplanted` when the verifier checks that the possession
proof verifies under `kX` but not that the manifest it covers is the
accepted one naming `kX`. It discharges nothing.

**Why the attack succeeds (F4, RESULTS 115–126; trace goal `.out:200`,
derivation 238–275).** Issuer 2's honest self-signature
`ppf2 = sign((POSS, m2), skI2)` is public (125). The adversary derives
`k' = dsks(ppf2, r)` (`.out:238`) — a private key it holds whose public
key verifies `ppf2` to `(POSS, m2)` (`lib:83–84`). It builds a manifest
`t'` naming `fp(pk(k'))` (`.out:257`), forges the channel's evidence
over `h(t')` with the leaked `skS`, frames and signs its own bytes
under `k'` with `h(t')` as the manifest hash (`.out:274`), and presents
**`ppf2`** as possession. Line 105 asks only "does `ppf` verify under
`kX` as a `POSS` object?" — yes; it never asks whether the manifest
inside is `t'`. Acceptance fires; `PossJudge` pairs `(pk(k'), ppf2)`
with the honest report `(pk(skI2), ppf2)` (124), keys differ, red.

In the correct form (Q2:105, `=t`) the same `ppf2` is rejected because
it is over `m2`, not `t'`. F4's consequence: possession must be over
the manifest **and** checked against the accepted key; the spike's
fingerprint-only possession would fail this companion's correct form
trivially. This is the concrete mechanism behind ENUMERATION note 2.

**Adversary.** As Q2 — and here the DSKS capability is what it uses.

**Boundary.** As §4d: a companion discharges nothing. `Reattributed`
staying unreachable here is a *side* observation (the frame binding
does its job even when possession is mis-checked); it is not a
registered query outcome for this companion (PREDICTIONS 193–199).

### 5e. Read and never used (Q4)

`mAny` (105); `ss`, `ver` (101); `ot`, `cv`, `pl` (108); judge's `id`
(133); library events fired at 89, 122, 127 unqueried; `STMT_DIRECT`,
`fbH`.

---

## 6. Q5c — `sp3_q5_multikey_correct.pv` (two required signers)

### 6a. Cast

| Name | What it is in the design | Built | Consumed |
|---|---|---|---|
| `skS` | sole authority channel's key — **leaked** | 143 | 77, **150**, 147, 154 |
| `skA`, `skB` | the two required signers of manifest `m`; `skA2`, `skB2` the two signers of `m2` (N2: two honest two-signer manifests) | 144 | 145/146, 147, 152–153 |
| `m`, `m2` | **the key statement:** `authTuple(issuerId, fp(pk(skA)), fp(pk(skB)), algH, verH)` — **the signer-set slot carries B's fingerprint** (header 9–11); both signers share `issuerId` | 145, 146 | 148, 151, 152–153 → 84/95 (self-signed by each), 87/98 (hashed into each frame) |
| `payload` | **the thing attested** — each signer takes its own adversary-chosen payload | read 82, 93 | 87, 98 |
| `fb` (in `SignerA`/`SignerB`) | each signer's framed bytes; **each frame binds its own signer's fingerprint** (`fp(pk(sk))`) and the shared `h(m)` | 87, 98 | 88/99 (event), 89/100 (report on **its role's** channel), 90/101 (signed) |
| `ppf` (per signer) | each signer's manifest self-signature | 84, 95 | 85/96 (report), 86/97 (published) |
| `honestChA`, `honestChB` | per-role honest report channels (recut 2, RESULTS 58–62) | 49, 50 | out 89 / 100; in 125 / 131 |
| `acceptCh`, `honestPossCh`, `possCh` | as §0.2 | 51–53 | out 121–122 / 85, 96 / 121; in 126, 132 / 137 / 138 |
| `ReattributedA`, `ReattributedB` | per-role re-attribution events — so the companion can be "red on exactly B" | 54, 55 | fired 128 / 134; queried 62–63 / 64–65 |
| `PossessionTransplanted`, `HonestAccepted` | as §0.2 | 56, 57 | fired 140 / 127, 133; queried 66–67 / 69–70 |
| `Accept2(ev, t, kA, kB, fa, fb)` | two-signer acceptance | 59 | fired 120; queried 72–73 |
| `t`, `id`, `kfprA`, `kfprB`, `alg`, `ver` | presented manifest and its fields — `kfprB` is the signer-set slot read as B's fingerprint | read 104; 109 | `kfprA` 110, `kfprB` 111, `id` 116/118/122, `alg` 116/118; **`ver` never used** |
| `kA`, `kB`, `ppfA`, `ppfB`, `sgA`, `sgB`, `fa`, `fb` | the two presented keys, possessions, signatures, frames | read 105–106 | 110–119 |
| `ota`, `mha`, `cva`, `pla`, `otb`, `mhb`, `cvb`, `plb` | frame fields | 116, 118 | `mha` 117, `mhb` 119; **the other six never used** |
| `JudgeA`, `JudgeB`, `PossJudge` | one judge per role | 124–128, 130–134, 136–140 | 155 |

### 6b. The verifier's checks (lines 103–122)

F7's ablations were run on Q2; F3 (RESULTS 100–113) was established on
Q5's registered companion and is the source for the multi-key rows.

| Line | Check | Plain meaning | Status |
|---|---|---|---|
| 107 | sole evidence over `h(t)` | channel endorses this manifest | inert (F6; key public at 150) |
| 109 | `let authTuple(id, kfprA, kfprB, alg, ver) = t` | read fields; the signer-set slot is B's fingerprint | structural |
| 110 | `fp(kA) = kfprA` | A's presented key is the one the manifest names first | **LOAD-BEARING for `PossessionTransplanted`** (jointly with 112 — Q2's dependency statement, carried; no Q5c ablation is in the record); **for `ReattributedA` only via the redundant route with 117**, since 116 still carries `=fp(kA)` (Q2 M10, carried) |
| 111 | `fp(kB) = kfprB` | B's presented key is the one the signer-set names | **LOAD-BEARING for `PossessionTransplanted`** (jointly with 113 — carried as for 110); **for `ReattributedB` only via the redundant route with 119**, since 118 still carries `=fp(kB)`. F3's sentence "the verifier's slot check `fp(kB) = kfprB` does the rest" (RESULTS 103–104) is stated for **Q5n**, whose B frame lacks the fingerprint; there the slot check is on the only remaining route. Here it is evidence for the *redundant* route, not the primary one |
| 112, 113 | possession over `t` under `kA`, under `kB` | each key self-signed this manifest | **LOAD-BEARING** for `PossessionTransplanted` jointly with 110/111 (dependency statement); A1.5/P10 result CARRIED |
| 114, 115 | attestation signatures over `fa`, `fb` | each key signed its own frame | unexercised by re-attribution (F7); CARRIED to S-P1 |
| 116, 118 | frame parse with `=alg`, `=id`, `=fp(kA)` / `=fp(kB)` | each frame names its own signer's fingerprint | `=fp(k·)`: **LOAD-BEARING** (F7); `=alg`, `=id`, `ot·`, `cv·`: CARRIED (F7) |
| 117, 119 | `mha = h(t)`, `mhb = h(t)` | each frame commits to this manifest | **LOAD-BEARING, redundant with `=fp(k·)`** — and in Q5n this redundancy is what kept the registered companion green (F3) |
| 120 | `event Accept2` | acceptance | N1 target |
| 121–122 | four parallel reports | recut 1 | encoding |

### 6c. Results (`.out`)

| Query | `.out` line | Result |
|---|---|---|
| `ReattributedA` | 314 | unreachable |
| `ReattributedB` | 320 | unreachable |
| `PossessionTransplanted` | 326 | unreachable |
| `HonestAccepted` | 563 | reachable |
| `Accept2` | 768 | reachable |

### 6d. Claim, adversary, boundary

**Claim (header 15–18).** With two required signers on one manifest,
in degraded mode with the sole channel compromised and DSKS available,
neither signer's honest bytes can be accepted under any key but its
own, and neither signer's self-signature can be accepted as possession
for another key.

**Adversary.** As Q2 (§3d); it also chooses both payloads.

**Why the attack fails.** As §3d, once per signer: A's frame carries
`fp(pk(skA))` and 116 pins `kA` to it; B's frame carries `fp(pk(skB))`
and 118 pins `kB`. The manifest hash (117, 119) closes the same door
independently: the honest `h(m)` pins `t = m` (`h` injective), which
names both honest fingerprints, so 110 and 111 pin both keys.

**Boundary.** As §3d, plus: the multi-key manifest here is the bare
tuple with B's fingerprint in the signer-set slot (header 9–11) —
"signer-set" is one fingerprint, not a set; A1.3 item 2 (strip,
reorder, duplicate signatures) is not representable in the verifier's
fixed two slots (falsification record, minor note at line 304). This
is S-P3's two-signer *binding* claim; signer-set *completeness* is
S-P2's.

### 6e. Read and never used (Q5c)

`ver` (109); `ota`, `cva`, `pla`, `otb`, `cvb`, `plb` (116, 118);
judges' `id` (126, 132); library events fired at 76, 83/94, 88/99
unqueried; `STMT_DIRECT`, `fbH`, and the library's `ssetH` (**not used
here** — the signer-set slot holds `fp(pk(skB))` instead, 145).

---

## 7. Q5n — `sp3_q5_multikey_companion_noFpB.pv` (registered companion; could not go red)

### 7a. Cast — differences from Q5c

All lines as Q5c (same numbering from 45 on) except:

| Name | What it is | Built | Consumed |
|---|---|---|---|
| `framedNoFp(objType, alg, issuerId, manifestHash, canonVer, payload)` | **the registered mutation:** B's frame keeps identity and manifest hash but **drops its fingerprint** | 43 | built 98 (`SignerB`); matched 118 |
| `framed(...)` | the correct constructor, still used by `SignerA` | 41 | 87; matched 116 |

### 7b. The verifier's checks — difference from Q5c

| Line | Check | Status |
|---|---|---|
| 118 | `let framedNoFp(otb, =alg, =id, mhb, cvb, plb) = fb` | **THE MUTATION:** Q5c's `=fp(kB)` is gone from B's frame check |
| 119 | `mhb = h(t)` | **present — and this is why the companion stays green** (F3) |
| 111 | `fp(kB) = kfprB` | present |

### 7c. Results (`.out`)

| Query | `.out` line | Result |
|---|---|---|
| `ReattributedA` | 314 | unreachable |
| `ReattributedB` | 320 | **unreachable — the registered prediction (red on B) MISSED** (RESULTS 27, F3) |
| `PossessionTransplanted` | 326 | unreachable |
| `HonestAccepted` | 562 | reachable |
| `Accept2` | 766 | reachable |

### 7d. What this model shows, and its boundary

**Why the attack still fails (F3, RESULTS 100–113).** To accept B's
honest bytes under some `kX ≠ pk(skB)`, the verifier needs a manifest
`t` with `kfprB = fp(kX)` (111). But B's honest frame carries `h(m)`
(98), and 119 demands `mhb = h(t)`; `h` is injective, so `t = m`, whose
signer-set slot is `fp(pk(skB))`; so `kX = pk(skB)`. The manifest hash
pins the tuple, the tuple pins both fingerprints, the slot check does
the rest. This is "a companion that could not fail" (ENUMERATION note 1
item 1's pattern), recorded as a **prediction miss**, and it is the
evidence for F3's conclusion: in this abstraction the minimal
load-bearing binding is the manifest hash with the tuple fingerprint
match; the frame's identity and fingerprint fields are defense in
depth across two Layer-2 assumptions (`h` and `fp`), not additional
binding. RESULTS 252–254: no combined or quantified security level may
be derived from that.

**Boundary.** This file is evidence about the *redundancy* of the P3
field list, not about P3 holding. Q5u supplies the negative control
this companion could not (RESULTS 28; F3: "discharged by an added
companion").

### 7e. Read and never used

As §6e; `ver`, six frame fields, judges' `id`, `ssetH`, `STMT_DIRECT`,
`fbH`.

---

## 8. Q5u — `sp3_q5_multikey_companion2_unboundB.pv` (added companion; red on B only)

### 8a. Cast — differences from Q5c

Lines shift by +2 from Q5c after the extra constructor (keys 144–145;
`m`, `m2` 146–147; leak 151; roles 152–156; channels 51–55; events
56–59; `Accept2` 61; queries 64–75; `AuthorityS` 77–79; `SignerA`
83–92; `SignerB` 94–103; `VerifierS` 105–123; judges 125–141).

| Name | What it is | Built | Consumed |
|---|---|---|---|
| `framedU(objType, alg, canonVer, payload)` | **the mutation (unregistered, added 2026-09-04, RESULTS 28):** B's frame with no identity, no fingerprint, no manifest hash — Q3's mutation applied to B | 45 | built 100 (`SignerB`); matched 120 |
| `framed(...)` | correct constructor for A | 43 | 89; matched 118 |

### 8b. The verifier's checks — difference from Q5c

| Line | Check | Status |
|---|---|---|
| 118 | A's frame parse with `=fp(kA)` | present (correct) |
| 119 | `mha = h(t)` | present |
| 120 | `let framedU(otb, =alg, cvb, plb) = fb` | **THE MUTATION:** no `=id`, no `=fp(kB)`, and **no manifest-hash check for B** (Q5c's 119 has no counterpart) |
| 112, 113 | `fp(kA) = kfprA`, `fp(kB) = kfprB` | present |
| 114, 115 | possession over `t` under both keys | present |

### 8c. Results (`.out`)

| Query | `.out` line | Result |
|---|---|---|
| `ReattributedA` | 311 | unreachable — A untouched |
| `ReattributedB` | 540 | **reachable — red on exactly B, the negative control the registered companion could not supply** |
| `PossessionTransplanted` | 547 | unreachable |
| `HonestAccepted` | 782 | reachable |
| `Accept2` | 985 | reachable |

### 8d. Why the attack succeeds, and its boundary

**Trace goal (`.out:318`):** any key `k ≠ skB2` the adversary holds
and any payload `plb` reach
`ReattributedB(pk(k), pk(skB2), framedU(objTypeH, algH, canonVerH, plb))`.
The mechanism is Q3's (§4d, F2): with no binding fields, B2's honest
bytes for payload `plb` are term-equal to bytes the adversary frames
for the same `plb`; the adversary publishes a manifest whose signer-set
slot is `fp(pk(k))`, self-signs possession, signs the frame under `k`,
and the verifier accepts it in the B slot; `JudgeB` pairs it with
B2's honest report and fires. `ReattributedA` cannot fire because A's
slot still carries the full binding (118–119).

**Boundary.** A companion; discharges nothing. It shows that the
per-role judge arrangement can localize a failure to one signer, which
is what the registered prediction asked for and Q5n could not show.

### 8e. Read and never used

`ver` (111); `ota`, `cva`, `pla`, `otb`, `cvb`, `plb` (118, 120);
judges' `id` (127, 133); `ssetH`, `STMT_DIRECT`, `fbH`; library events
fired unqueried.

---

## 9. Observations about the testimony (comments), not the proofs

Recorded so the probe reviewer and the author see them; none changes a
result; none is acted on here (this document edits no `.pv` file).

1. **Q1d/Q1r headers carry the recut-3 block written for Q2.** Lines
   43–58 of both Q1 files say "the authority-evidence check is inert
   here by construction (the sole channel key is public)" and
   "unexercised by these two queries". In Q1 there are two channels and
   five queries; the leaked channel's check is inert, but the honest
   channel's check is load-bearing per F1 (§1b, line 129 / §2, line
   128). The block is accurate for Q2–Q5 and over-broad for Q1.
2. **A misplaced argument comment under `HonestAccepted`.** In Q1d/Q1r
   76–78, Q2 74–76, Q3 73–75, Q4 73–75 the second comment line
   "(* accepted key, the honest issuer's own possession proof it
   presented *)" describes `PossessionTransplanted`'s arguments
   (declared on the line above) but sits under `HonestAccepted`.
3. **Truncated header lines** in Q5n line 3 ("B's frame omits its
   finge") and Q5u line 3 ("B's frame omits all bi").
4. **`AuthorityS` fires the library's `AuthorityPublishedDNS`** (Q2:90,
   Q3:88, Q4:89, Q5c:76, Q5n:76, Q5u:78) although the degraded fixture
   is a generic sole channel; nothing queries it in these models, so
   the choice of the DNS branch is cosmetic here — but a reader should
   not infer that the sole channel "is DNS".
5. **Q3 declares `framed` and never uses it** (59), and fires
   `PossessionTransplanted` (138) without querying it. Both are
   consistent with the registered plan (PREDICTIONS 177–191 asks only
   for `Reattributed`), and both are places a non-expert may look for a
   check that is not there.

Proposed follow-up (clerk work, not a decision): fold items 1–3 into
the `.pv` comments on the author's say-so, since ENUMERATION note 5
item 2 speaks of aids the model *carries*.

## 10. Routed to the author

**ROUTED TO AUTHOR — where the aids must live for the probe to run.**
ENUMERATION note 5 item 2 (lines 297–312) says "every model *carries*
(a)–(c)" and the lower-ceiling reader probe reads "the annotated
model". This document is a sidecar beside the models, not annotation
in them. Whether a sidecar satisfies item 2 as written, or the
(a)–(c) content must be folded into each `.pv` header (making the
headers substantially longer) before the probe is dispatched, is a
ruling on the instrument, not something this draft can settle. The
probe design depends on the answer.

> *Disposition (clerk), 2026-09-06 — settled from the record, not routed; listed for veto in `formal/suite/ROUTED-2026-09-06.md` §B.* Note 5 item 2 says the aids live "in its header or a sibling `.md`"; a sidecar satisfies it. The probe reads the aid plus the comment-stripped model, as run for Q3 on 2026-09-06 (`formal/spike/first-link/proverif/reading-aid-q3/PROBE-haiku-2026-09-06.md`), and discriminated. (B1)

## Review log

- 2026-09-06 — drafted by the AI collaborator from the eight recut-3
  `.pv` files, their `.out` files, `ladder.log`, the library,
  `RESULTS.md` (F1–F8, dependency statement, suite rules),
  `PREDICTIONS.md`, ENUMERATION notes 1–5 and dispositions, P3 and
  A1.3 as registered, and the 2026-09-04 Codex walk-through. No run
  was made; no file other than this one was written. Not yet read by
  the author; not yet probed.
