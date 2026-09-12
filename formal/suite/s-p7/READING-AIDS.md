# S-P7 reading aids — cast, checks, and plain-language claim for all twelve models

> **STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not
> adopted; the commit is the author's.** This is *testimony* under
> `formal/suite/ENUMERATION.md` amendment note 5 item 2 (lines 297–312):
> reading aids for non-expert readers, reviewed by the lower-ceiling
> reader probe, **not a gate for exit**. Nothing here changes a query, a
> result, a header, or a `.pv` file. Every statement about a model cites
> `file:line`; every LOAD-BEARING / CARRIED label comes from **this
> ladder's own ablations** (`RESULTS.md`, "Ablations" table and F2–F5;
> `proverif/ablations/ablations.log`), never from the registered plan's
> prediction — where the two differ, the ablation wins and the
> difference is recorded (`RESULTS.md` divergence 4). Form follows
> `formal/spike/first-link/READING-AID-Q3.md` and `s-p3/READING-AIDS.md`.
> *Amended 2026-09-06, PROPOSED:* since the cross-family falsification
> review (Codex, `docs/reviews/2026-09-06-codex-suite-falsification-s-p1-s-p2-s-p7-s-standing.md`;
> its scratch under `proverif/falsification-2026-09-06/`) every
> LOAD-BEARING label here is read **jointly** unless a single removal is
> named red — the reviewer's 198-mutant matrix
> (`scratch/guard_groups.tsv`) agrees with the ablations wherever they
> overlap and adds Q1, Q4c and Q5 columns; where a label below said
> LOAD-BEARING singly for a check whose single removal is green, the
> dated corrections in §1b, §2 and §4 apply (review items 4, 5, 19, 20).
> The seven header edits those items required are comment-only and
> line-count neutral, so every `file:line` here stands (`RESULTS.md`
> review log, 2026-09-06 cross-family entry).

Files this document reads (all under `formal/suite/s-p7/proverif/`;
results in the sibling `.out` files):

| Short | File | Kind |
|---|---|---|
| Q1d | `sp7_q1_strict_dns_compromised.pv` | correct, strict, DNS key leaked |
| Q1r | `sp7_q1_strict_repo_compromised.pv` | correct, strict, repo key leaked |
| Q2 | `sp7_q2_degraded_compromised.pv` | correct, degraded, sole channel leaked — **the C2 claim; the template** |
| Q3 | `sp7_q3_companion_type_unchecked.pv` | broken companion (C1) |
| Q4t | `sp7_q4_companion_reserialize_twoversion.pv` | broken companion (C3), two versions, strict |
| Q4i | `sp7_q4_companion_reserialize_isolation.pv` | Q4t's isolation config, one version |
| Q4c | `sp7_q4_control_opaque_twoversion.pv` | added control (unregistered): correct wrapper, two versions |
| Q4p | `sp7_q4_probe_degraded_twoversion.pv` | probe (unregistered): Q4t's mutation in degraded mode |
| Q5 | `sp7_q5_depth2_correct.pv` | correct, degraded, depths 1 and 2 |
| Q5c | `sp7_q5c_companion_one_level_in.pv` | broken companion (depth) |
| Q6a | `sp7_q6a_companion_identity_outermost.pv` | broken companion (C2, identity) |
| Q6b | `sp7_q6b_companion_key_outermost.pv` | broken companion (C2, key and authority) |

Library: `formal/suite/lib/tessera_theory.pvl` (cited as `lib:N`).
Property text: P7, Amendment 1 §A1.2, quoted in `PREDICTIONS.md` 36–48;
adversary A1.3; the suite's sharpening, `ENUMERATION.md` 90–100.

---

## 0. Typing note (once, for every model)

- **Every message is a `bitstring`.** Keys are typed (`skey`, `pkey`,
  `lib:95–96`) and the network is a `channel` (`lib:77`); everything
  else — a manifest, a frame, a wrapper, a signature, a hash, a
  fingerprint, an object-type tag, a canonicalization version, a
  judge's context — is `bitstring`. **Shape lives in construction and
  pattern matches, never in declarations.** A frame is a frame because
  it was built with `framed(...)` (Q2:129) and is later taken apart with
  `let framed(=OT_ATTEST, =algI, =idI, =fp(kI), mhI, cvI, plI) = fbI in`
  (Q2:253); a wrapper's payload is a wrapper's payload because it was
  built with `wrap(...)` (Q2:131, 222) and matched at Q2:279.
- **`=x` in a pattern means "must equal x"; a bare name means "read it".**
  Q2:253 checks four things (`OT_ATTEST`, `algI`, `idI`, `fp(kI)`) and
  reads three (`mhI`, `cvI`, `plI`). Q2:279 checks `OT_WRAPPER`, `algW`,
  `idW`, `fp(kW)` and reads `mhW`, `cvW`, and the three parts of
  `wrap(cvIw, (fbI, sgI))`. This one distinction is most of what a
  reader needs.
- **`[data]` constructors are transparent** (`framed`, `wrap`, `wctx`,
  `authTuple`, and in the Q4 family `canon`): the adversary builds and
  decomposes them freely. `sign`, `h`, `fp` are not; `checksign`
  (`lib:100–104`) is the only way to open a signature, and it recovers
  the message (so every honest signed message is public).
- **`!P` is unboundedly many copies.** Every honest role, every
  verifier, every judge is replicated.
- **The judges are private-channel processes** (Q2:145–152, `[private]`):
  the adversary neither sees nor forges their reports. Report outputs
  are always in *parallel* with the continuation (`( out(..) | out(..) )`,
  Q2:208–212, 256–259) — the S-P3 recut-1 rule.
- **A process macro with parameters** (`let InnerCheck(...) =`, Q2:246)
  is expanded where it is invoked (Q2:264, 283). "One process invoked
  from both paths" means the same text, not a shared running instance.
- **Two idealizations carry the results** and are declared in the
  library, not in any model: `fp` injective (`lib:107–117`) and `h`
  injective (`lib:119–131`). F2 locates the whole load of the C2
  results' key half on `fp`, and the identity half on any one of the
  frame's `=idI`, `h` (the manifest hash) or possession (a17, a18).

## 0.1 Shared cast — the library terms every model uses

| Name | What it is in the design (plain words) | Declared (lib) | Used in the models |
|---|---|---|---|
| `c` | the public network; the adversary owns it | 77 | every `in(c,…)`/`out(c,…)` |
| `skey`, `pkey`, `pk` | private key, public key, the map between them | 95–97 | every key |
| `sign`, `checksign` | deterministic signature with message recovery | 98, 100–104 | every check |
| `dsks(s, r)` | **A1.3 item 3 (D-4):** from one seen signature, a private key the adversary holds whose public key verifies it | 99, 103–104 | appears in a derivation only in Q6b (`InnerSigTransplanted`, `.out` 778) |
| `fp(pk)` | key fingerprint, **idealized injective** | 117 | manifests, frame field, slot checks |
| `h(x)` | hash, **idealized injective** | 131 | manifest hash in evidence and frame |
| `STMT_DIGEST` | tag: authority evidence, digest form | 139 | channel evidence |
| `POSS`, `BYTES` | tags: manifest self-signature; signature over framed bytes | 140–141 | possession proofs; attestation and wrapper signatures |
| `STMT_DIRECT`, `TLR`, `REFUSAL` | tags for the direct form and the two Amendment-4 kinds | 138, 143–144 | **declared in the library, used by no S-P7 model** |
| `OT_ATTEST`, `OT_WRAPPER`, `OT_REVIEWREC` | **object-type constants (D-5)** — the three exercised | 150, 151, 155 | frames; every type check |
| `OT_MANIFEST`, `OT_AUTHEVID`, `OT_CONFVEC`, `OT_TLR`, `OT_REFUSAL` | the five declared, unexercised types | 152–154, 156–157 | **no S-P7 model** |
| `authTuple(id, kfp, sset, alg, ver)` | **the key statement — the manifest as the suite models it** | 164 | `mI1`, `mI2`, `mW1`, `mW2` (Q2:311–314) |
| `issuerId`, `ssetH`, `algH`, `verH` | honest fixture values; `issuerId` is **inner issuer I1's identity** here | 169–172 | Q2:311, 321 |
| `fbH` | the spike's honest-bytes fixture | 173 | **used by no S-P7 model** (judge locals are `fbHon`, `fbT`) |
| `AuthorityPublishedDNS/Repo`, `IssuerPossession`, `IssuerSigned`, `Accept` | library events | 179–183 | fired (Q2:194, 202, 207, 220, 235); **queried by no S-P7 model**; `Accept` unused |

## 0.2 The judge idiom (shared by all twelve)

Registered in `PREDICTIONS.md` 216–261 before any run. Four judges, each
pairing an honest report with a verifier report **for the same bytes**
(the `=fbHon` / `=fbT` / `=sgH` pattern):

- **Type judge** (Q2:286–289). Honest signer reports `(objType, bytes)`
  for everything it signs (Q2:208, 224, 237); a verifier reports
  `(objType it accepted the bytes AS, bytes)` (Q2:256, 282). Different
  types, same bytes → `TypeConfused(signed, accepted, bytes)`.
- **Base judge, S-P3's transcribed** (Q2:292–296). Attester reports
  `(key, bytes)` (Q2:209); `InnerCheck` reports `(ctx, key, id, bytes)`
  on *both* paths (Q2:257). Key differs → `Reattributed`; key equal
  **and the context is `BASE`** → `HonestAccepted`, the base-path N1
  witness.
- **Scope judge** (Q2:298–302). Attester reports `(key, id, bytes)`
  (Q2:210); `InnerCheck` reports `(ctx, attributed key, attributed id,
  bytes)` (Q2:258). The judge matches **only wrapped contexts**
  (`wctx(kW, idW, fbW)` in the pattern, Q2:300). Pair equal →
  `HonestWrappedAccepted(kH, bytes, kW)`, the wrapped-path N1 witness;
  else `Rescoped(kIrep, idIrep, kH, idH, bytes)`.
- **Signature judge** (Q2:304–307). Attester reports `(key, signature
  term)` (Q2:211); `InnerCheck` reports `(ctx, attributed key, the
  signature term it verified)` (Q2:259), wrapped contexts only. Same
  term, different key → `InnerSigTransplanted(kIrep, term)`.

Three consequences to hold onto: (1) the scope judge compares the
*attributed pair*, so it is red on identity alone (Q6a) or key alone;
(2) the signature judge is keyed on the *term* and so tells the DSKS
route (honest term under a derived key, Q6b `.out` 778) from the
re-sign route (adversary's own term over public honest bytes, Q6b
`.out` 498) — the bytes-keyed scope judge cannot; (3) all four are keyed
on exact honest bytes/terms and say nothing about bytes the adversary
signed itself (impersonation, out of scope by the 2026-09-05 ruling).

---

## 1. Q2 — `sp7_q2_degraded_compromised.pv` (the C2 claim; the template)

### 1a. Cast

| Name | What it is in the design | Built | Consumed |
|---|---|---|---|
| `skS`, `pk(skS)` | the **sole** authority channel's key — **leaked** | 310; published 315 | 193–195 signs evidence; **319 `out(c, skS)`**; 320; 324 |
| `skI1`, `skI2` | the two honest **inner issuers'** keys (N2, issuer axis) | 310 | 311–312 fingerprints into manifests; 315 published; 321–322 |
| `skW1`, `skW2` | the two honest **wrapper issuers'** keys | 310 | 313–314; 315; 323 |
| `mI1`, `mI2`, `mW1`, `mW2` | the four honest manifests `authTuple(id, fp(pk(sk)), ssetH, algH, verH)` | 311–314 | 316 published; 320 channel signs each; possession self-signatures 203, 220, 234; hashed into frames 205, 222, 236 |
| `issuerId`, `issuerId2` | I1's and I2's identities | lib:169; 137 | 311–312, 321–322 |
| `idW1`, `idW2` | W1's and W2's identities | 138–139 | 313–314, 323 |
| `idA` | the adversary's wrapper identity — **a free name for readability only**; the adversary needs no process (it holds `skS`) | 140 | nowhere in a process; traces use their own `idX` |
| `cvA`, `cvB` | two honest canonicalization versions (N2, version axis): I1/`cvA`, I2/`cvB`, W1/`cvB`, W2/`cvA`, I1-as-wrapper/`cvB` | 141–142 | 321–323 |
| `framed(objType, alg, issuerId, kfp, mh, canonVer, payload)` | **the frame** — S-P3's seven-field constructor copied verbatim (library: "NOT promoted") | 129 | built 205, 222, 236; matched 253, 279 |
| `wrap(cvInner, (innerBytes, innerSig))` | **the opaque embedding as a term**: the inner package (bytes and signature) beside the inner canonicalization version — "records both inner and outer versions" (the outer one is the frame's `canonVer`) | 131 | built 222; matched 279 |
| `wctx(kW, idW, fbW)` / `BASE` | the verifier-path **context** handed to the judges: wrapped path / base path | 133, 135 | 264, 283; judge patterns 295, 300, 306 |
| `payload` | **the thing attested**; adversary-chosen | read 201, 231 | 205, 236 |
| `(cvIw, fbIn, sgIn)` | **the blob an honest wrapper wraps**; adversary-chosen (chosen-message wrapper) | read 218 | 222 |
| `fbI`, `sgI` (Attester) | the honest attestation bytes and signature `sign((BYTES, fbI), skI)` | 205–206 | reports 208–211; `sgI` published 212; `fbI` public by recovery |
| `fbW` (Wrapper) | the honest wrapper bytes `framed(OT_WRAPPER, algH, idW, fp(pk(skW)), h(mW), cvW, wrap(…))` | 222 | report 224; signed 225 |
| `fbO` (OtherSigner) | an honest `OT_REVIEWREC` object under I2's key — the N2 second type | 236 | report 237; signed 238 |
| `ppfI`, `ppfW`, `ppfO` | possession proofs — **manifest self-signatures** `sign((POSS, m), sk)` (D-3) | 203, 220, 234 | published 204, 221, 235; checked 251, 277 |
| `tI`, `evI`, `kI`, `ppfI`, `sgI`, `fbI` (verifier side) | what the presenter hands the base verifier: manifest, evidence, key, possession, signature, bytes | read 263 | `InnerCheck` 246–259 |
| `tW`, `evW`, `kW`, `ppfW`, `sgW`, `fbW` + `tI`, `evI`, `kI`, `ppfI` (wrapped) | the outer package, plus the inner manifest / evidence / key / possession the presenter supplies for the inner check; **the inner bytes and signature come out of the wrapper** (279), not from the presenter | read 272–273 | 274–283 |
| `idI`, `kfprI`, `ssI`, `algI`, `verI` | fields of the inner manifest | 249 | `kfprI` 250; `idI` 253, 255, 257–258; `algI` 253; **`ssI`, `verI` never used** |
| `idW`, `kfprW`, `ssW`, `algW`, `verW` | fields of the wrapper's manifest | 275 | `kfprW` 276; `idW` 279, 281, 283; `algW` 279; **`ssW`, `verW` never used** |
| `mhI`, `cvI`, `plI` / `mhW`, `cvW`, `cvIw` | frame fields read | 253 / 279 | `mhI` 254, `mhW` 280; **`cvI`, `plI`, `cvW`, `cvIw` never used** |
| the eight judge channels | as §0.2 | 145–152 | out 208–211, 224, 237, 256–259, 282; in 287–288, 293–294, 299–300, 305–306 |
| `AcceptInner(ctx, kI, idI, fbI)` | acceptance of an attestation on a path, with the attributed pair | 154 | 255 |
| `AcceptOuter(kW, idW, fbW)` | acceptance of a wrapper object | 156 | 281 |
| `TypeConfused`, `Rescoped`, `HonestWrappedAccepted`, `InnerSigTransplanted`, `Reattributed`, `HonestAccepted` | the judge events (§0.2) | 158–168 | fired 289, 302, 301, 307, 296, 295; queried 172–188 |
| `AuthorityS` | the sole channel: fires the library's DNS event (cosmetic — the channel is generic, comment 191–192) and emits `sign((STMT_DIGEST, h(t)), skS)` | 193–195 | 320 |
| `Attester`, `Wrapper`, `OtherSigner` | honest roles | 200–212, 217–225, 230–238 | 321–323 |
| `InnerCheck` | **the one inner check**, invoked from both paths | 246–259 | 264, 283 |
| `VerifierBase`, `VerifierWrapped` | the two paths | 262–264, 271–283 | 324 |

### 1b. The checks — LOAD-BEARING / CARRIED from the Q2 ablations (`RESULTS.md` table; a01–a18)

`InnerCheck` (246–259), run by both paths:

| Line | Check | Plain meaning | Status (ablation) |
|---|---|---|---|
| 248 | `let (=STMT_DIGEST, =h(tI)) = checksign(evI, pkS)` | the sole channel endorsed exactly this inner manifest | **CARRIED — inert** (a12 green; the channel key is public, 319; S-P3 F6) |
| 249 | `let authTuple(idI, kfprI, ssI, algI, verI) = tI` | read the inner manifest | structural |
| 250 | `if fp(kI) = kfprI` | the presented inner key is the one the manifest names | **CARRIED singly** (a07 green); **LOAD-BEARING jointly with 254 when 253's `=fp(kI)` is absent** (a02 green, a09 red) |
| 251 | `let (=POSS, =tI) = checksign(ppfI, kI)` | the inner key self-signed this manifest (D-3) | **CARRIED** for these queries (a08 green; S-P3 entry 2); one of the three routes pinning the *identity* (F2) |
| 252 | `let (=BYTES, =fbI) = checksign(sgI, kI)` | the inner key signed exactly these bytes | **LOAD-BEARING for `InnerSigTransplanted`** (a11 red — F3); **CARRIED for `Rescoped`/`TypeConfused`** (a11 green on both); authorship security is S-P1's / S-P3 entry 1 |
| 253 `=OT_ATTEST` | the bytes say they are an attestation | **LOAD-BEARING for `TypeConfused`** (Q3 = this removed: red) |
| 253 `=algI`, `=idI` | the bytes name the manifest's algorithm and identity | `=idI`: **CARRIED given 251 or 254** (a01, a03, a05 green; F2) but **one of the three identity routes** — with 251 and 254 also removed, `Rescoped` is red on the identity half (a18); `=algI` not ablated, carried by S-P3 F7 (A3 §1 identifier binding) |
| 253 `=fp(kI)` | **the bytes name the presented key's fingerprint** | **LOAD-BEARING JOINTLY for `Rescoped` (key half) and `InnerSigTransplanted`** (*corrected 2026-09-06, review item 4:* first labelled LOAD-BEARING without the qualifier; its single removal is green — a02, matrix row 15 — so it is load-bearing only jointly with 250 and 254) — `=fp(kI)` for the key half: alone pins the key (a17 green with 250 and 254 both removed); replaceable only by 250 **and** 254 together (a02 green; a06, a09 red); does **not** pin the identity (a18) — any one of `=idI` / `mh` / possession does that. The key half's whole load is `fp` injectivity (`lib:107–117`), S-P3 F5 one level up |
| 254 | `if mhI = h(tI)` | the bytes commit to this manifest | **CARRIED singly** (a04 green); **LOAD-BEARING jointly with 250 when `=fp(kI)` is absent** (a06 red); one of the three identity routes (a18: red when all three are gone) |
| 255 | `event AcceptInner(...)` | acceptance | the judges' input |
| 256–259 | four parallel reports | recut-1 rule | encoding |

`VerifierWrapped` (271–283), the outer checks:

| Line | Check | Plain meaning | Status |
|---|---|---|---|
| 274 | evidence over `h(tW)` | the channel endorsed the wrapper's manifest | **CARRIED — inert** (public channel key) |
| 276 | `fp(kW) = kfprW` | the wrapper key is the one its manifest names | **CARRIED** (not ablated singly; the wrapper's authorship is S-P3 entry 1, consumed) |
| 277 | possession over `tW` under `kW` | the wrapper key self-signed its manifest | **CARRIED** (S-P3 entry 2) |
| 278 | `checksign(sgW, kW) = (BYTES, fbW)` | the wrapper key signed the wrapper bytes | **CARRIED** (authorship; S-P3 entry 1) |
| 279 `=OT_WRAPPER` | the outer bytes say they are a wrapper | **LOAD-BEARING for `TypeConfused`** (a10 red: an honest attestation whose payload is a `wrap()` term is accepted as a wrapper) |
| 279 `=algW`, `=idW`, `=fp(kW)` | the wrapper bytes name their manifest's fields | **CARRIED** (a13: `=fp(kW)` read → all green) |
| 279 `wrap(cvIw, (fbI, sgI))` | **unwrap**: the inner bytes and signature are *read out of the signed wrapper*, never taken from the presenter | structural — this is C3 by construction (ledger entry 3) |
| 280 | `mhW = h(tW)` | wrapper bytes commit to the wrapper's manifest | **CARRIED** |
| 281–283 | accept outer; report `OT_WRAPPER`; run **the same `InnerCheck`** with context `wctx(kW, idW, fbW)` | the wrapper lends nothing: the inner check has no argument that came from the wrapper except the bytes and signature it committed to | the encoding of "wrapping never alters the independently-computed verdict" |

Domain tags (`STMT_DIGEST`, `POSS`, `BYTES`) and the version fields
(`cvI`, `cvW`, `cvIw`): **CARRIED** — bound, read, never compared (P8).

### 1c. Results (`sp7_q2_degraded_compromised.out`)

| Query | `.out` line | Result |
|---|---|---|
| `TypeConfused` | 505 | unreachable — **C1** |
| `Rescoped` | 518 | unreachable — **the C2 claim** |
| `InnerSigTransplanted` | 531 | unreachable |
| `Reattributed` | 544 | unreachable (S-P3 not weakened, either path) |
| `HonestWrappedAccepted` | 846 | **reachable** (trace at 557: adversary-chosen payload, I2 signs, the **adversary's own key `pk(k)`** wraps, accepted with the inner attributed to `pk(skI2)`/`issuerId2` — F7) |
| `HonestAccepted` | 1042 | reachable (trace at 859: base path, I2's bytes under `pk(skI2)`) |

### 1d. Claim, adversary, boundary (plain language)

**Claim (header 13–28; F1, F2).** Suppose the only authority channel
is in the adversary's hands, so the adversary can register any key it
likes — including keys it derives from signatures it has seen — as a
fully "authorized" wrapper issuer. Then: (i) a relying party who runs
these checks on a wrapped presentation will always attribute the
enclosed attestation to the key and identity written *inside the
attestation's own signed bytes*, never to the wrapper's — no wrapper
can claim honest work as its own, and no honest wrapper's standing can
be lent to bytes it did not sign; (ii) the honest signature inside a
wrapper is never **accepted** under some other key (*corrected
2026-09-06, review item 19:* first "never verified" — the signature
primitive itself can succeed under a key the adversary derives from the
signature, DSKS, before line 253's fingerprint pin rejects the
presentation; what the judge reports, and what this claim is about, is
acceptance); (iii) an object signed
as one kind (attestation, wrapper, review-recency) is never accepted
as another kind — where "accepted" has exactly two meanings in this
model: accepted *as an attestation* (`InnerCheck`, 246–259) or *as a
wrapper* (`VerifierWrapped`, 271–283); nothing is accepted as a
review-recency record or any other kind anywhere, so the check's
content is "never accepted as an attestation or as a wrapper under
another signed type" (skeptic review 2, 2026-09-06). The honest
sentence for (i), after ablation: *under a
perfect fingerprint, no wrapper can move the attribution of honest
inner bytes to another key or identity* — the key half's whole load is
the innermost frame's fingerprint field; the identity half needs any
one of the frame's identity field, the manifest hash, or possession
(a17, a18: with all three removed the identity is re-scopable even
though the key stays pinned).

**Adversary (A1.3; header; 315–319).** Sees everything on `c`; holds the
sole channel key (319), so it manufactures manifests, evidence and
possession for any key it holds; chooses every payload honest signers
sign (201, 231) and every blob honest wrappers wrap (218); builds and
opens frames and wrappers freely (`[data]`); has DSKS (`lib:99`). Does
not hold `skI1`, `skI2`, `skW1`, `skW2`.

**Why the attack fails (Q2 form).** To re-scope honest bytes `fbI2`,
the acceptance must report a pair other than `(pk(skI2), issuerId2)`.
The reported key `kI` must satisfy `fp(kI) = fp(pk(skI2))` at 253 — so
`kI = pk(skI2)` (`fp` injective), whatever manifest and evidence the
adversary minted for some other key. The reported identity comes from
the presented manifest `tI` (249), which must hash to the frame's `mhI`
(254) — so `tI = mI2` — and be self-signed under `kI` (251) — again
`mI2`; either alone pins `issuerId2`, and 253's `=idI` pins it a third
time. Nothing in the wrapper (`kW`, `idW`, `tW`) is an input to any of
those four lines: that is the design, made visible by 283 passing the
wrapper's data only as a *context* for the judges.

**Boundary (header 64–83; `RESULTS.md` "What S-P7 does not discharge").**
Depth 1 only (Q5 does 2). Opacity of a real embedding is *assumed* by
the term `wrap()` — Q4 is where it is *tested*. Nothing about the
verdict partition (non-acceptance is "the process stops"). Nothing about
the five unexercised types, the non-framed kinds (manifest, possession,
evidence — the open coverage cell), standing evidence (S-STANDING), or
impersonation with the adversary's own key over its own bytes (reachable,
the adjudicator's cost per §A4.6). `fp` and `h` are collision-free by
fiat. An adversary-authorized wrapper enclosing honest bytes **is
accepted** — with the inner correctly attributed and the wrapper
attributed to the adversary (F8); the model does not say what a wrapper
means, only what it cannot do.

*Boundary sentences added 2026-09-06 from the cross-family review
(Boundary items, each cited by number).* **Signature sets** (item 1):
every layer here has exactly one signature slot, so stripping,
reordering or duplicating signatures — A1.3 item 2 — cannot be
expressed; that is S-P2's subject, represented there at n ≤ 2.
**Bytes** (item 2): term equality stands in for byte equality and
distinct constructors never confuse, so non-canonical encodings,
hash-input ambiguity and cross-kind parse confusion are, in the
reviewer's phrase, *a coverage failure, not an unreachable attack* —
P8's injectivity obligation and the library's `h`/`fp` idealization
(Layer 2), already named above as "collision-free by fiat".
**Verdicts** (item 3): no verdict value, waiver record or policy input
exists in any S-P7 model; "rejected" means the process stops; the
four-state partition is P4's and the `Accept` ↔ P4 join is
cross-formalism (author ruling 2026-08-29). **Self-containment** (item
21): the wrapper's embedded pair carries the inner *bytes and
signature* only; the inner manifest, evidence and possession are handed
to the verifier by the presenter (272–273), and no query asks that they
travel inside the bundle — P7's "inner bytes must travel inside the
bundle, or P9's self-containment fails" is exercised for the bytes, not
for the package; an open coverage cell (`formal/COVERAGE-MAP.md` row 8,
amendment note), a P8/H1a format obligation. **Witnesses** (item 6):
`HonestAccepted` and `HonestWrappedAccepted` are existential — a
vacuity guard, not coverage; one reachable trace does not establish
acceptance for every honest key, wrapper or version pairing.

### 1e. Read and never used (Q2)

`ssI`, `verI` (249); `ssW`, `verW` (275); `cvI`, `plI` (253); `cvW`,
`cvIw` (279); the judge's `idX` (294; S-P3 F8); `idA` (140); `fbH`,
`STMT_DIRECT`, `TLR`, `REFUSAL`, five `OT_*` constants, `Accept` from
the library. Everything else declared in this file is consumed.

---

## 2. Q1d / Q1r — `sp7_q1_strict_{dns,repo}_compromised.pv`

Q2's body with two channels (Q1d lines are cited; Q1r is identical
except 253 `out(c, skR)`):

- **Cast differences.** `skD`, `skR` (243) replace `skS`; `AuthorityD`
  (121–123) fires `AuthorityPublishedDNS` and `AuthorityR` (124–126)
  `AuthorityPublishedRepo`; both channels sign all four manifests
  (254–255); one key is leaked (253). `InnerCheck` (177–191) and
  `VerifierWrapped` (203–216) take two channel keys and check two
  evidences per object (179–180; 206–207). The presenter hands six or
  twelve values (195; 204–205). Everything else is Q2 line for line,
  offset −68 (e.g. Q2:253 = Q1:185). (Every line number in this section
  was off by one in the first draft; corrected 2026-09-06.)
- **Checks.** As §1b with one change: the **honest channel's** evidence
  check (Q1d: 180 and 207, the repository; Q1r: 179 and 206, DNS) is
  **LOAD-BEARING JOINTLY — defence in depth, not individually necessary**
  (*corrected 2026-09-06, review item 5:* first labelled LOAD-BEARING
  without the qualifier). It pins every presented manifest, inner *and*
  outer, to one of the four honestly published ones before any frame is
  inspected (S-P3 F1), which is why in strict mode the adversary can
  obtain no wrapper authority of its own — but removing it *alone*
  changes no query: the reviewer's mutants `q1d_I_evRI_evidence`
  (repository check dropped in Q1d) and `q1r_I_evDI_evidence` (DNS check
  dropped in Q1r) leave all six RESULT lines as committed (matrix row
  2; re-run by the collaborator, identical), because the manifest-hash
  and fingerprint pins carry the relation on their own (the S-P3 F5
  shape). The leaked channel's check is inert. No S-P7 Q1 ablation is
  in the record, but the reviewer's matrix has Q1d and Q1r columns for
  every guard and agrees with the Q2 assignments; the strict fixture
  only adds a constraint.
- **Results** (both `.out` files identical): `TypeConfused` 560,
  `Rescoped` 574, `InnerSigTransplanted` 588, `Reattributed` 602
  unreachable; `HonestWrappedAccepted` reachable (935, trace 616 —
  through **honest wrapper `pk(skW2)`**, necessarily); `HonestAccepted`
  reachable (1144, trace 949).
- **Claim / adversary / boundary.** As §1d with "the sole channel is
  the adversary's" replaced by "one of two required channels is the
  adversary's, and the other only ever vouches for the four honest
  manifests". In this mode C2's threat reduces to re-framing honest
  objects, which the frame's fields defeat. The point of running both
  variants (registered) is that neither channel's honesty is assumed by
  name.
- **Read and never used:** as §1e.

---

## 3. Q3 — `sp7_q3_companion_type_unchecked.pv` (broken companion, C1)

- **Difference from Q2:** one line. `InnerCheck` 156 reads `ot` instead
  of matching `=OT_ATTEST` (Q2:253). `Reattributed` is fired (199) and
  not queried (83–85 comment). Everything else is Q2, offset −97.
- **Results:** `TypeConfused` **reachable** (727; trace 509 — see below);
  `Rescoped` 744 and `InnerSigTransplanted` 761 unreachable;
  `HonestWrappedAccepted` 1067 and `HonestAccepted` 1267 reachable.
  Route probe `ablations/p01_q3_routes.out`: `OT_WRAPPER→OT_ATTEST` and
  `OT_REVIEWREC→OT_ATTEST` reachable; `→OT_WRAPPER` routes unreachable.
- **Why the attack succeeds (trace at 509).** The adversary hands honest
  W2 any blob (`cvIw_4, fbIn_3, sgIn_3`, all adversary terms); W2 frames
  and signs it as `OT_WRAPPER` (125–128). The adversary presents that
  wrapper object to the **base** verifier with W2's public manifest,
  sole-channel evidence, W2's key, W2's public possession proof and
  W2's public signature. Lines 151–157 all pass — the manifest names
  W2's key, W2 did sign those bytes, the hash matches — and 156 no
  longer asks what kind of object it is. The type judge pairs W2's
  honest report `(OT_WRAPPER, fbW)` (127) with the base path's
  `(OT_ATTEST, fbW)` (159) and fires. No DSKS. The same key signing two
  types is not needed for this route (W2 signs only wrappers).
- **Boundary.** A companion; discharges nothing; shows the type judge can
  detect what the tag is for, and (F5) that nothing else in the checks
  would have — manifest, possession, signature and hash are all about
  *whose* bytes, not *what kind*.

---

## 4. The Q4 family — `sp7_q4_*` (C3, re-serialization)

All four are **strict-mode, DNS-leaked** bodies (Q1d's shape; divergence
1 in `RESULTS.md`) except Q4p, which is Q2's degraded shape. Added
theory (Q4t: 61–66): `canon(v, x)` `[data]` — "the bytes of structure
`x` canonical under version `v`" — and the destructor
`reserialize(v, canon(v0, x)) = canon(v, x)`: re-canonicalizing under
`v` yields bytes canonical under `v`, identical to the input iff `v =
v0`. Nothing about *what* changes is modeled.

| | Q4t (two-version) | Q4i (isolation) | Q4c (control) | Q4p (probe) |
|---|---|---|---|---|
| inner bytes | `canon(cvI, framed(...))` (137) | same (131) | same (110) | same (104) |
| wrapper | **mutated**: `fbC = reserialize(cvW, fbIn)` (154), wraps `fbC` (155) | **mutated** (148–149) | **correct**: wraps `fbIn` (127) | **mutated** (121–122) |
| `InnerCheck` unpack | `let canon(cvc, framed(=OT_ATTEST, …)) = fbI` (187) | 181 | 159 | 153 |
| versions | inner `cvA`, **every wrapper `cvB`** (258–261) | **all `cvA`** (252–255) | inner `cvA`, wrappers `cvB` (230–233) | inner `cvA`, wrappers `cvB` (221–224) |
| mode | strict, `skD` leaked (255) | strict (249) | strict (227) | **degraded**, `skS` leaked (219) |
| `HonestWrappedAccepted` | **unreachable (604) — the required red** | **reachable (933; trace 608 via honest `skW2`) — the required green** | reachable (926; 602 via `skW2`) | reachable (840; 546 via the **adversary's `pk(k)`**) |
| the other queries | 565/578/591 green; `HonestAccepted` 817 reachable | 566/580/594; 1147 | 560/574/588; 1140 | 510/522/534; 1040 |

**Why Q4t's red is the right red.** Honest I2 signs
`canon(cvA, framed(...))` (137–138). The honest wrapper re-serializes it
under `cvB` before committing (154): the wrapper now carries
`canon(cvB, framed(...))` beside I2's signature over the `cvA` bytes.
At the verifier, 186 asks I2's key to verify the signature over the
*carried* bytes and it does not; the standalone verdict (base path,
`HonestAccepted` 817) is untouched — "wrapping has altered the inner
verdict". Because this red is an unreachability, it carries the
vacuity tell: Q4i is the same file with one version everywhere, where
`reserialize` is the identity and the honest flow goes through (933).
Q4c adds what the registration did not ask: the version *mismatch*
alone, with a correct opaque wrapper, leaves the honest wrapped witness
reachable (926) — the red is the re-serialization. (*Narrowed
2026-09-06, review item 20:* Q4c's header first said the wrapped
acceptance "is exactly its standalone acceptance"; no query states that
equality — the control exhibits an existential witness, and the
shared-`InnerCheck` argument is conditional on reaching `InnerCheck`
with identical inputs.) Q4p records why the mode is strict: in
degraded mode the adversary's own wrapper embeds the honest blob
correctly (it never runs 121) and the honest-wrapper bug is
unfalsifiable (840).

**Boundary.** Companions and controls; discharge nothing. What they
license (ledger entry 3): the checking arrangement *detects*
re-serialization; that a concrete base64-of-bytes embedding is opaque
under a real JCS pass is P8/H1a, the largest residual in S-P7.

---

## 5. Q5 — `sp7_q5_depth2_correct.pv` (depths 1 and 2)

- **Cast additions.** `wctx2(kO, idO, kM, idM)` (55), the depth-2
  context: outermost and middle wrapper pairs; `AcceptMiddle` (80);
  per-depth events `RescopedD1/D2`, `HonestWrappedAcceptedD1/D2`
  (84–88; divergence 2); `VerifierWrapped2` (220–242); `ScopeJudge2`
  (263–267) and `SigJudge2` (274–277) matching `wctx2`. The depth-1
  path `VerifierWrapped` (202–214) is Q2's. Fixture as Q2 (the honest
  wrappers wrap adversary-chosen blobs, so W1-over-I1 and W2-over-W1
  and adversary-over-W1 all arise without new roles).
- **`VerifierWrapped2` checks.** Outer object as a wrapper (224–231,
  Q2:274–281 line for line, `=OT_WRAPPER` at 229) → unwrap to the middle
  bytes and signature (229) → **middle object as a wrapper again**
  (233–240: evidence 233, slot 235, possession, signature 237, frame
  with `=OT_WRAPPER` and `=fp(kM)` 238, hash 239) → unwrap to the
  innermost bytes (238) → **the same `InnerCheck`** (242) with context
  `wctx2(kO, idO, kM, idM)`. There is no recursion and no depth
  counter: "innermost" is "the first `OT_ATTEST` frame after peeling
  `OT_WRAPPER` frames", two paths deep (F9). LOAD-BEARING / CARRIED as
  §1b at each level, carried by reasoning (no Q5 ablation is in the
  record): the depth-2 attribution is pinned by the *innermost* frame's
  `=fp(kI)` inside `InnerCheck` (177–190), to which neither wrapper's
  data is an input.
- **Results** (`.out`): `TypeConfused` 654, `RescopedD1` 692,
  `RescopedD2` 730, `InnerSigTransplanted` 768, `Reattributed` 806
  unreachable; `HonestWrappedAcceptedD1` 1133 (trace 844) and
  `HonestWrappedAcceptedD2` 1573 (trace 1171: I2's bytes, honest middle
  wrapper, **adversary outermost `pk(k)`**) reachable; `HonestAccepted`
  1794. 6 seconds against a 45-minute box — the predicted timeout
  concentration did not materialize.
- **Claim / boundary.** §1d at depths 1 and 2: the acceptance of a
  wrapper-over-wrapper-over-attestation attributes the attestation to
  its own frame's pair, never the middle wrapper's, never the
  outermost's, even when the outermost is the adversary's authorized
  wrapper. Nothing beyond depth 2 (ENUMERATION §3, n = 2).

---

## 6. Q5c — `sp7_q5c_companion_one_level_in.pv` (broken companion, depth)

- **Difference from Q5:** the depth-2 path's inner check is inlined
  (229–241) and its **scope report is the middle wrapper's pair**
  `(kM, idM)` (240) instead of `(kI, idI)`; `AcceptInner` records the
  same (237). The signature is still verified under `kI` (234 in
  the inline block) and the `acceptCh`/`sigCh` reports carry `kI`
  (239, 241) — the mutation is in *attribution*. The depth-1 path
  (189–201) is Q5's unchanged: "one level in" and "innermost" coincide
  there (divergence 3). `Reattributed` fired, not queried.
- **Results:** `RescopedD2` **reachable** (1131; trace 728: I2's honest
  bytes inside an **adversary-held middle wrapper `pk(k)`**, attributed
  to `(pk(k), idX)`); `RescopedD1` **unreachable** (690) — the required
  green at depth 1; `TypeConfused` 652 and `InnerSigTransplanted` 1169
  unreachable; `HonestWrappedAcceptedD1` 1496 reachable;
  `HonestWrappedAcceptedD2` 1876 reachable **only** when the middle
  wrapper is I1 wrapping its own attestation (trace 1535, `pk(skI1)`;
  F7); `HonestAccepted` 2097.
- **Why the attack succeeds.** With the sole channel leaked the
  adversary is an authorized wrapper; it wraps I2's public attestation
  (as W1 would), and honest W2 or the adversary again wraps that. The
  depth-2 verifier checks everything correctly — I2's signature under
  I2's key, the frames, the hashes — and then reports the wrapper it
  peeled last as the author. "Inner" is not "innermost"; that gap is
  exactly one frame wide and this companion is it.
- **Boundary.** Companion; discharges nothing.

---

## 7. Q6a — `sp7_q6a_companion_identity_outermost.pv` (broken companion, C2 identity)

- **Difference from Q2:** the wrapped path's inner check is inlined
  (188–200) and its scope report is `(kI, idW, fbI)` (199) — the
  wrapper's identity with the inner's key; `AcceptInner` likewise
  (196). Every check is Q2's (189–195 = Q2:248–254); `acceptCh`/`sigCh`
  still report `kI` (198, 200). Base path unchanged (167–169).
  `Reattributed` fired, not queried.
- **Results:** `Rescoped` **reachable** (806; trace 516: I2's honest
  bytes, verified under `pk(skI2)`, attributed to identity `idX ≠
  issuerId2` — the adversary's own wrapper identity); `TypeConfused`
  503, `InnerSigTransplanted` 819 unreachable; `HonestWrappedAccepted`
  1118 reachable (trace 832 through **the adversary's wrapper `pk(k)`
  wearing identity `issuerId2`** — the adversary registers its own key
  under the honest identity string through the leaked channel
  (derivation 958–985), so `idW = issuerId2 = idH` by its choice and
  the mutated attribution happens to be right; F7. This line first said
  "I1 wrapping its own attestation"; corrected 2026-09-06 from the
  `.out`); `HonestAccepted` 1314.
- **Why it succeeds.** Nothing is forged. The verifier does every check
  right and then writes the wrong name on the result. The registration
  admitted that even an honest wrapper would trip it; the exhibited
  trace happens to be the adversary-wrapper one. (*Narrowed 2026-09-06,
  review item 20:* the header's "misattributes on EVERY wrapped
  acceptance" is now "on every wrapped acceptance whose wrapper identity
  differs from the inner signer's" — when `idW = idH` the attribution
  coincides, which is exactly the reachable witness above.)

---

## 8. Q6b — `sp7_q6b_companion_key_outermost.pv` (broken companion, C2 key and authority)

- **Difference from Q2:** the wrapped path's inner check is replaced
  (192–199): **no** inner manifest, evidence or possession is examined
  (the four inner inputs at 181–182 are read and ignored); the inner
  signature is verified **under the wrapper's key `kW`** (193); the
  inner frame's `kfp`, `id` and `mh` are read, not matched (194); the
  artifact is attributed to `(kW, idW)` (195, 198) and the signature
  report carries `kW` (199). Base path unchanged. `Reattributed` fired,
  not queried.
- **Results:** `Rescoped` **reachable** (769; trace 498) and
  `InnerSigTransplanted` **reachable** (1058; trace 778); `TypeConfused`
  489 unreachable; `HonestWrappedAccepted` 1317 reachable (trace 1067
  through **I1 wrapping its own attestation**, `kW = pk(skI1)`; F7);
  `HonestAccepted` 1508.
- **Two routes, two judges (F4).** *Re-sign route* (498–769, **no
  `dsks`**): I2's frame is public (`framed` is `[data]`; the adversary
  rebuilds it at trace step 22 from `issuerId2`, `fp(pk(skI2))`,
  `h(mI2)`, `cvB` and its own payload), the adversary signs it under
  its own `k`, registers `k` as wrapper `idX` through the leaked
  channel, wraps, and 193 verifies its own signature under its own
  key: `Rescoped(pk(k), idX, pk(skI2), issuerId2, fbI2)`. S-P3 F2 in
  wrapped form: impersonation colliding with honest bytes. *DSKS route*
  (778–1058): the adversary derives `dsks(sgI2, r)` from I2's **honest
  signature**, registers its public key as a wrapper key, wraps I2's
  bytes *with I2's own signature*, and 193 verifies that honest term
  under the derived key (`lib:103–104`); 194 no longer asks whether
  the frame's fingerprint is that key's:
  `InnerSigTransplanted(pk(dsks(sgI2, r)), sgI2)`. Only the term-keyed
  judge can tell these apart; only the second needs A1.3 item 3.
- **Boundary.** Companion; discharges nothing. It is ledger entry 2's
  severing companion for the key/authority half, and the one place in
  the S-P7 ladder where the registered DSKS capability is exercised.
  *Recorded 2026-09-06 (review item 22):* the omitted `Reattributed`
  query, restored by the reviewer, is **red here too** (`scratch/
  audit_sp7_q6b_companion_key_outermost.pv`, RESULT at the reviewer's
  line 1338; re-run by the collaborator, identical) and stays green in
  every other companion — the key half of this mutation is S-P3's
  relation broken; the omission is a diagnostic limitation, not
  evidence the other relations survive (header line 91).

---

## 9. Observations about the testimony (comments), not the proofs

None of these changes a result; none is acted on here.

1. **`AuthorityS` fires the library's DNS event** (Q2:194 and every
   degraded model) for a generic sole channel — the S-P3 aid's
   observation 4, inherited; the comment at Q2:191–192 says so.
2. **`idA` is declared and never used** (Q2:140). It is there so a
   reader has a name for the adversary's wrapper identity; the traces
   use `idX_1` instead. A non-expert may look for a process that "holds
   idA" and not find one — `RESULTS.md` divergence 5.
3. **Companions fire `Reattributed` without querying it** (Q3:199,
   Q6a:213, Q6b:212, Q5c:254). Each header says so (S-P3 Q3 pattern).
4. **The Q1 headers say "no Q1 ablation is in the record"** and carry
   Q2's assignments; likewise Q5. A reader should treat the Q1/Q5
   LOAD-BEARING labels as reasoned, not measured. *(2026-09-06: now
   also measured — the reviewer's matrix has Q1d, Q1r and Q5 columns
   for every single guard and agrees; §2 and the Q1/Q5 headers say so.)*
5. **The registered header text in `PREDICTIONS.md` (445–472) names the
   `=idI` read as load-bearing and the signature check as carried;**
   the models' headers now say the opposite on both counts, from
   ablation. `PREDICTIONS.md` is frozen and unchanged; the correction
   is recorded in `RESULTS.md` divergence 4 and F2/F3.
6. **`wrap`'s recorded inner version (`cvIw`) and the inner frame's
   `canonVer` are both read and never compared** (Q2:279, 253). P7 says
   the wrapper "records both"; whether it must also *agree* with the
   inner frame is not stated in P7 and is left to P8; the headers say
   "presence only".

## 10. Routed to the author

**None.** The probe for this aid (ENUMERATION note 5 item 2, disposition
B1: a sidecar satisfies "carries"; the probe reads this aid plus a
comment-stripped model) has not been dispatched; the Q2 section above
is the candidate for it.

## Review log

- 2026-09-06 — drafted by the AI collaborator from the twelve `.pv`
  files, their `.out` files, `ladder.log`, `ablations/ablations.log`,
  the library, `RESULTS.md` and `PREDICTIONS.md`. No run was made for
  this document; no file other than this one was written by it. Not
  yet read by the author; not yet probed; no cross-family review.
- 2026-09-06 — skeptic review (see `RESULTS.md` review log, same date):
  §7's Q6a witness description corrected from the `.out` (adversary
  `pk(k)` under `issuerId2`, not I1 self-wrap); §0, §1b rows 253/254 and
  §1d reworded for the key-half / identity-half split established by
  the added ablations a17/a18; §5 and §6 line ranges corrected (202–214,
  189–201); every Q1 citation in §2 corrected by +1. The three `.pv`
  header edits recorded in `RESULTS.md` are comment-only and line-count
  neutral, and every `.out` is byte-identical, so every other
  `file:line` and `.out` citation here is unchanged.
- 2026-09-06 — skeptic review 2 (see `RESULTS.md` review log, same
  date): §0.2's plan citation corrected (216–261; line 215 is blank);
  §1d claim (iii) narrowed to the model's two acceptance paths. The
  matching C1 header edits in Q2/Q1/Q5 are comment-only and line-count
  neutral (`RESULTS.md`, "Header recut 2"), so every `file:line`
  citation here is unchanged.
- 2026-09-06 — cross-family falsification review applied (see
  `RESULTS.md` review log, same date, for the header edits and the
  re-run record — all seven edited `.pv` files comment-only and
  line-count neutral, all twelve `.out` files byte-identical): header
  note added; §1b row 253 `=fp(kI)` relabelled LOAD-BEARING JOINTLY
  (item 4); §1d claim (ii) "never verified" → "never accepted" (item
  19); §1d gained a boundary paragraph for items 1, 2, 3, 6, 21; §2 the
  honest channel's evidence check relabelled jointly load-bearing /
  defence in depth with the reviewer's mutants named (item 5); §4 Q4c
  sentence narrowed (item 20); §7 Q6a narrowing recorded (item 20); §8
  Q6b restored-`Reattributed` red recorded (item 22); §9 item 4
  annotated. Item 18 (ROUTED C9) is not applied here — `RESULTS.md`
  carries the pending line; §9 item 6 already says the version record
  is unverified. No `file:line` citation in this document changed.

---

## Post-freeze addendum 1 — reading aid, 2026-09-12

*(APPENDED. No sentence, table row or `file:line` citation above this
line is edited. Everything above cites the Q2 model as it stood before
2026-09-12; `RESULTS.md`, "Post-freeze addendum 1 — results,
2026-09-12", carries the line-shift table that re-finds those
citations. Subject: Amendment 5 §A5.5, `PREDICTIONS.md` "Post-freeze
addendum 1" — **Q7** in `sp7_q2_degraded_compromised.pv` as amended,
and **Q7-C**, `sp7_q7_companion_version_unchecked.pv`. Style follows
§1 and §3.)*

### 11a. Cast — the four new entries (amended Q2 model)

| Name | What it is in the design | Built | Consumed |
|---|---|---|---|
| `versionCh` | a **ninth** judge channel: verifier → version judge, `(wrapper bytes, the version the wrapper RECORDED, the inner framed bytes)`. A new channel, not a second reader on `scopeCh`, so `ScopeJudge`'s pairing (§0.2) is untouched | 190 | out 333; in 365 |
| `VersionLied(fbW, cvIw, cvI)` | the judge event: this wrapper was accepted recording inner version `cvIw` over an inner frame whose own version is `cvI` | 209 | fired 367; queried 232 |
| `VersionJudge` | the ninth judge. Reads `versionCh`, re-reads the inner frame for its own `canonVer`, fires when the two differ. **Instrumentation on the acceptance report, not a verifier check** — it pairs with nothing honest, unlike `TypeJudge`/`Judge`/`ScopeJudge`/`SigJudge`, which each pair a verifier report with an honest signer's report | 364–367 | 386 |
| `otIv`, `algIv`, `idIv`, `kfpIv`, `mhIv`, `plIv` | throwaway names for the inner frame's other six fields, bound only so the seventh position can carry `=cvIw`. Never used | 330 | nowhere |

`cvIw` itself is no longer in the "never used" list of §1a's frame-field
row: read at 324 (the unwrap), matched at 330, reported at 333. `cvI`
and `cvW` are still never compared on the base path, and the inner
frame's own version is still never checked for support (P8/H1a).

### 11b. The check — one new row for `VerifierWrapped`

| Line | Check | Plain meaning | Status |
|---|---|---|---|
| **330** | `let framed(otIv, algIv, idIv, kfpIv, mhIv, =cvIw, plIv) = fbI` | **the version the wrapper wrote down for its inner object is the version that object's own frame declares** — a lying record is rejected | **LOAD-BEARING for `VersionLied`** (Q7-C = this line removed: red). Nothing else in the model compares the two; the sole route |

Where it sits, and why there: `cvIw` is bound in `VerifierWrapped` (324,
out of the `wrap()` pattern) and `cvI` inside `InnerCheck` (298).
Passing `cvIw` into `InnerCheck` would change `InnerCheck`, which the
**base** path also runs — so the equality is checked in
`VerifierWrapped` instead, by re-destructuring the `fbI` already in
scope. `InnerCheck` (285–304) and `VerifierBase` (306–309) are
byte-unchanged, and §1b's `InnerCheck` table is still exactly right
about the base path. The guard sits after `if mhW = h(tW)` (325) and
before `event AcceptOuter` (331): a mismatch is a rejection, not a
silent report. The report at 333 is emitted **after** the guard, beside
`out(typeCh, …)` (332) and the `InnerCheck` call (334) — the recut-1
rule of §0.2, unchanged.

### 11c. Results

`sp7_q2_degraded_compromised.out` — Q7 and the six carried queries:

| Query | `.out` line | Result |
|---|---|---|
| `TypeConfused` | 527 | unreachable — C1 |
| `Rescoped` | 540 | unreachable — the C2 claim |
| `InnerSigTransplanted` | 553 | unreachable |
| `Reattributed` | 566 | unreachable |
| `HonestWrappedAccepted` | 865 | reachable (trace 579) |
| `HonestAccepted` | 1061 | reachable (trace 878) |
| **`VersionLied`** | **1074** | **unreachable — the new claim** |

`sp7_q7_companion_version_unchecked.out` — `TypeConfused` 525,
`Rescoped` 538, `InnerSigTransplanted` 551, `Reattributed` 564 all
unreachable; `HonestWrappedAccepted` 866 and `HonestAccepted` 1062
reachable; **`VersionLied` reachable, 1301 (trace 1075)**. Red on
exactly `VersionLied`, as registered.

### 11d. Q7-C — why the attack succeeds (trace at 1075)

- **Difference from the amended Q2:** one guard. Line 330 is absent
  (its place holds a `MUTATION` comment, 222–227 of the companion);
  `versionCh` and `VersionJudge` are still there. Everything else is
  the amended Q2 model: offset **−104** from it through
  `if mhW = h(tW)` (amended Q2 325 = companion 221), and **−103** from
  `event AcceptOuter` (amended Q2 331 = companion 228) to the end — the
  five-line guard-plus-comment is replaced by a six-line `MUTATION`
  comment.
- **The trace.** The adversary holds `skS` (the degraded-mode
  `out(c, skS)`, 379, shown as `{19}`), so it is an authorized wrapper
  issuer for any key it likes. It picks its own `k`, builds a manifest
  `authTuple(idW_6, fp(pk(k)), …)`, mints channel evidence for it under
  `skS`, self-signs possession, frames
  `wrap(cvRec, (framed(…, cvAct, …), sgI_4))` as `OT_WRAPPER` and signs
  it with `k` — with `cvRec ≠ cvAct`. It presents the package at the
  wrapped path's input `{135}`; every outer check passes because it
  built every part consistently; `AcceptOuter` fires `{143}`, the
  report goes out on `versionCh` `{145}`, `VersionJudge` reads it
  `{183}` and fires `VersionLied` at `{186}`. No `dsks`, no forgery.
- **Whose objects are in that trace — the thing to notice.** *None* of
  them are honest. The registered trace shape was an **honest** wrapper
  (`skW1`, `skW2` or `skI1`-as-wrapper) handed an honest inner
  `(fbI, sgI)` with an adversary-chosen `cvIw ≠ cvI` — the shape that
  shows the lie is accepted *with no compromised wrapper at all*.
  ProVerif reports the cheapest witness, and the cheapest one here is
  the adversary minting the whole thing, inner object included: unlike
  `ScopeJudge` and `SigJudge`, `VersionJudge` pairs with no honest
  report, so nothing in the query forces an honest participant. Same
  situation as §7's Q6a, one step further. The registered shape is not
  refuted — it is simply not the one exhibited, and no model was built
  to exhibit it. `RESULTS.md` records it as an open cell.
- **Boundary.** A companion; discharges nothing. It shows the version
  judge fires at all, so Q7's green at `.out` 1074 is the new equality
  doing work rather than a query that could never go red. It says
  nothing about whether either version is *supported*, or whether the
  inner bytes were produced under the version claimed — that is still
  P8/H1a, exactly as §9 item 6 and the Q2 header say of the version
  fields. What is now narrowed is only this: on the wrapped path the
  recorded inner version is no longer "presence only", it must match.

### 11e. Review log (this section)

- 2026-09-12 — written by the AI collaborator from the amended `.pv`,
  the two `.out` files and `ladder.log` after the runs. Not read by the
  author; no falsification review of the amended model or the
  companion. The trace-shape gap in §11d is the first thing a reviewer
  should attack.

## Cross-family review 2026-09-12 — dispositions applied

Amend-don't-rewrite: the row corrected below is left as written above;
this section is the correction of record.

**1 — line 207, the `fp(kW) = kfprW` row.** It reads:

> **CARRIED** (not ablated singly; the wrapper's authorship is S-P3
> entry 1, consumed)

The author's ROUTED C5 read (`formal/suite/READ-C5-2026-09-12.md`,
"Author's answers", block 3) returned **NO** on that attribution: S-P3
ledger entry 1 is the **key-binding** relation, not authorship;
authorship is S-P1's, assigned there by S-P3 F7. Correct row text:
**CARRIED (not ablated singly; the wrapper's KEY BINDING is S-P3
entry 1, consumed; its AUTHORSHIP is S-P1's, per S-P3 F7)**. The
corresponding model comment, line 55 of
`proverif/sp7_q2_degraded_compromised.pv`, was repaired in place the
same day (same line count, dated `CORRECTION` marker); see the "Author
read — 2026-09-12 (ROUTED C5)" section of `RESULTS.md`.

**2 — line citations still resolve.** Three further comment-only,
same-line-count header repairs were applied to
`sp7_q2_degraded_compromised.pv` on 2026-09-12 from the cross-family
review (lines 144–145 and 154–155; see `RESULTS.md`, "Cross-family
review 2026-09-12 — dispositions applied"). No body line moved, the
`.out` is byte-identical after every one of them
(`proverif/ladder.log`), and every `.pv` line number in §§0–11 of this
file still resolves.
