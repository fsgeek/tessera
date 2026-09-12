# S-STANDING reading aids — cast, checks, and plain-language claim for all seven models

**STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not
adopted; the commit is the author's.** This is *testimony* under
`formal/suite/ENUMERATION.md` amendment note 5 item 2: reading aids for
non-expert readers, reviewed by the lower-ceiling reader probe (**not
yet run** for these models), **not a gate for exit**. Nothing here
changes a query, a result, a header, or a `.pv` file. Every statement
about a model cites `file:line` (the committed `.pv`, header included);
every LOAD-BEARING / CARRIED label cites the result that established it
— a companion's red, or an ablation probe under
`proverif/ablations/` (`RESULTS.md` "Ablation probes") — never an
assumption. Form: `formal/spike/first-link/READING-AID-Q3.md` (typing
note, cast with build/consume, checks table, claim / adversary /
boundary in plain language) and `formal/suite/s-p3/READING-AIDS.md`.

Files this document reads (all under `formal/suite/s-standing/proverif/`;
results in the sibling `.out` files; `run1/` and `ablations/` cited
where named):

| Short name | File | Kind |
|---|---|---|
| Q1d | `ss_q1_strict_dns_compromised.pv` | correct, strict, DNS key leaked — **the primary fixture** |
| Q1r | `ss_q1_strict_repo_compromised.pv` | correct, strict, repository key leaked |
| Q1deg | `ss_q1d_degraded_compromised.pv` | correct, degraded, sole channel leaked — **the registered cost** |
| Q2 | `ss_q2_companionA_identity_declared.pv` | broken companion A (identity declared; wrapper transplant) |
| Q3 | `ss_q3_companionB_entitled_via_envelope.pv` | broken companion B (entitled key only via envelope) |
| Q4 | `ss_q4_companionC_terminal_unchecked.pv` | broken companion C (terminal disposition unchecked) |
| Q5 | `ss_q5_companionD_reason_collapsed.pv` | broken companion D (reason codes collapsed; B9) |

Library: `formal/suite/lib/tessera_theory.pvl` (cited as `lib:N`).
Property text: A3.7.1, `docs/phase-0-prereg-amendment-3.md` §A3.7 item 1
(quoted in `PREDICTIONS.md` "Target"); adversary A1.3,
`docs/phase-0-prereg-amendment-1.md` lines 331–347; the degraded-mode
principle, `docs/phase-0-prereg-amendment-4.md` §A4.6 lines 152–167.

---

## 0. Typing note (once, for every model)

- **Every message is a `bitstring`.** Keys are typed `skey`/`pkey` and
  the network `channel`; everything else — a manifest, a core, a
  lineage, a TLR, a report verdict, a reason code — is a `bitstring`.
  **Shape lives in construction and pattern matches, never in
  declarations.** A lineage is a lineage because it was built with
  `lineage2(entry(…), entry(…))` (Q1d:125–126) and is later taken apart
  by the destructor `lookup2` (Q1d:269–273); nothing in a `fun` or
  `const` line says "this is a lineage".
- **`=x` in a pattern means "must equal the value already bound to
  x"; a bare name means "read this and bind it".** So
  `let (=TLR, (lin, terminal, declT)) = checksign(tlrSig, kT)`
  (Q1d:319) checks the tag and reads three fields.
- **`let pat = M in P else Q`**: if the pattern or destructor fails,
  run `Q`. This is how the verifier *reports* a rejection instead of
  silently stopping — every `else` in the standing path is a named
  report (Q1d:325–332).
- **`[data]` constructors** (`attemptCore`, `wrapCore`, `entry`,
  `lineage2`, `TERM_SHIPPED`, `withTLR`, `anchorProof`, `framed`,
  `authTuple`) are transparent: the adversary builds and dismantles
  them. `sign`, `h`, `fp` are not; they are built from inputs and
  never inverted except by `checksign` (`lib:111–115`).
- **`const X: bitstring.`** is a public name with no structure. The
  verdicts and reason codes are constants (Q1d:139–153): the model can
  compare them, and a companion can make two of them one (Q5).
- **A process macro** `let StandingDecide(...) = ...` (Q1d:277) is
  inlined where it is called (Q1d:324); its parameters are the values
  in scope at the call.
- **`!P`** is unboundedly many copies. Every honest role, both
  verifier paths and both judges are replicated (Q1d:376–381).
- **Two idealizations carry the whole result** and live in the
  library, not in any model: `fp` injective (`lib:117–128`) and `h`
  injective (`lib:130–142`). The plan said in advance, and F1 confirms,
  that **the transplant result's entire load is `h`**.

## 0.1 Shared cast — library terms every model uses

| Name | What it is in the design (plain words) | Declared (lib) | Used in the models |
|---|---|---|---|
| `c` | the public network; everything the adversary sees and can inject | 88 | every `in(c, …)`/`out(c, …)` |
| `skey`, `pkey`, `pk` | private key, public key, the map between them | 106–108 | every key |
| `sign`, `checksign` | deterministic signature with message recovery | 109, 111–115 | authority evidence, possession, attestation, **the TLR** |
| `dsks(s, r)` | the A1.3 item 3 capability (D-4): a held key whose public key verifies one seen signature | 110, 114–115 | never in an honest process; available to the adversary; appears in no derivation of this ladder |
| `fp(pk)` | key fingerprint; **idealized injective** | 128 | manifests; the entitled-key checks |
| `h(x)` | hash; **idealized injective** | 142 | evidence digests; **the derived attempt identity `h(core)`**; the anchor proof |
| `STMT_DIGEST`, `POSS`, `BYTES` | tags: authority evidence (digest form), manifest self-signature, attestation bytes | 150–152 | channels, issuers, envelope path |
| `TLR` | **tag: "this is a terminal lineage record"** (D-6; Amendment 4 §A4.5; ruling A6) | 154 | inside every TLR signature; checked by the standing path |
| `REFUSAL`, `STMT_DIRECT`, `OT_*` other than `OT_ATTEST` | declared in the library, **used by no S-STANDING model** | 149, 155, 162–168 | — |
| `OT_ATTEST` | object-type constant carried in the frame (D-5) | 161 | issuers' frames, unchecked (P7's business) |
| `authTuple(id, kfp, sset, alg, ver)` | **the key statement = the manifest**: issuer identity, key fingerprint, signer-set, algorithm, version | 175 | `m`, `m2`; the tuple every path evidences and destructures |
| `issuerId`, `ssetH`, `algH`, `verH` | honest fixture values, public | 180–183 | `m`, `m2`, frames |
| `fbH` | the spike's honest-bytes fixture | 184 | **used by no S-STANDING model** (judge locals named apart) |
| `AuthorityPublishedDNS/Repo`, `IssuerPossession`, `IssuerSigned` | library events | 190–193 | fired by channels/issuers, **never queried here** |
| `Accept(evD, evR, t, k, fb)` | strict envelope acceptance | 194 | fired by the envelope path (Q1d:349), **never queried here** |

## 0.2 The two judges (shared by all seven)

**The entitled-key judge** (Q1d:354–360; plan §"The judge and the
correspondence" item 2). The standing path reports `(key, evidenced
tuple, derived identity)` on the private channel `estCh` when it says
`ESTABLISHED` (Q1d:287); the honest issuer reports `(its key, the
identity it shipped)` on `designCh` *before* releasing its TLR
(Q1d:241). The judge destructures the tuple and fires
`StandingUnentitled(kX, t)` if the key's fingerprint is not the one the
tuple names (Q1d:357), else waits for a matching honest designation and
fires `HonestStandingEstablished(kX, aid)` — the N1 witness (Q1d:359–360).
Judge locals are `idJ, kfprJ, ssJ, algJ, verJ` so nothing shadows the
library's names.

**The reason judge** (Q1d:363–366; disposition B9). Every no-standing
branch of the standing path also reports `(which branch, which code)` on
`reasonCh` (Q1d:280, 293, 311). The judge reads two reports with the
same code and fires `ReasonCollapsed(p1, p2, r)` if they came from
different branches. Unreachable when S2/S3/S4 use three codes;
reachable in Q5, where S2 and S3 share one.

**Two consequences to hold onto:** (1) the correspondence queries are
about `Established`/`Designated` events keyed on the *derived identity*
`h(core)` — a label, an ordinal, or a wrapper's inner identity never
enters them; (2) `StandingReport(...)` events are vocabulary-liveness
witnesses only: they show a branch is reachable, and in degraded mode
the S1 witness is satisfied by the adversary's own key (Q1deg
`.out:1094`, restated at 1096), which is why the N1 witness is the judge's and not any
of them.

## 0.3 What these seven models cannot see (cross-family falsification review, 2026-09-06)

Added 2026-09-06 after the agreement-gate review
(`docs/reviews/2026-09-06-codex-suite-falsification-s-p1-s-p2-s-p7-s-standing.md`;
reviewer's scratch archived under
`proverif/falsification-2026-09-06/`). Item numbers are that record's
consolidated list. None of these changes a result; each is a boundary
the aids must state so a reader does not read more out of a green
RESULT line than is in it.

1. **Signature-set operations are unrepresentable here (item 1).**
   Every object in these models carries exactly one signature slot;
   `ss` inside the tuple is destructured and never interpreted.
   Stripping, reordering or duplicating signatures — A1.3 item 2 — has
   no representation, so no green line here says anything about it.
   That surface belongs to S-P2.
2. **Byte-encoding attacks are unrepresentable here (item 2).** Term
   equality stands in for byte equality; distinct constructors never
   confuse. Non-canonical encodings, hash-input ambiguity and
   cross-kind parse confusion therefore cannot be tried. The reviewer's
   wording is adopted: this is **a coverage failure, not an unreachable
   attack**. It is registered — P8's injectivity obligation and the
   library's `h`/`fp` idealization (Layer 2).
3. **There are no verdict values, waiver records or policy inputs in
   any of these models (item 3).** `Accept`/`AcceptS` are emitted and
   never queried. Everything about what a verifier *reports* as a
   verdict is P4's partition and the `Accept` ↔ P4 cross-formalism
   join (author ruling 2026-08-29; coverage map).
4. **"Inert" is a fixture-and-query observation, never permission to
   remove a check (item 4).** The `CARRIED, inert` labels in §1b and
   §3b each mean "removing this one check alone changed no registered
   RESULT line in this fixture". They do not license removing two
   together, and inertness flips under composition — see item 27
   below. Where a check the old headers called load-bearing turns out
   green on single removal, §1b now says "jointly with …".
5. **The N1 witness is existential (item 6).** It is reachable with a
   trace in all seven models, but reachability for one honest key is
   not reachability per branch or per key. N1 is a vacuity guard —
   proof that the honest flow is not dead — not coverage.
6. **The unrestricted correspondence (i) is fixture-bound (item 24).**
   It holds in §1 and §2 because every honestly evidenced tuple in the
   fixture names an honest key. The reviewer built an honestly
   *enrolled* adversary-owned issuer — its own identity, its own key,
   its own tuple evidenced by both honest channels — and (i) goes
   false while both per-honest-key sentences (ii) and the entitled-key
   sentence (iii) stay true. An honestly registered issuer *is* an
   issuer; (ii) is the claim. Same pattern as S-P3 and S-P1.
7. **`kT = kX` is a fixture shape, not a requirement (item 28).** No
   registered text asks that the key the artifact presents equal the
   key the TLR was signed under. It is the standing probe's `tlr.pub =
   core.pub` shape, kept so that Q3's registered mutation is a removal
   from the correct form rather than a substitution (§8 item 3).
8. **The TLR domain tag's work is invisible to this family (item
   27).** Removing it changes nothing here, because no honest signer in
   any of these fixtures emits another tag over a TLR-shaped body. Add
   one honest `REFUSAL`-tagged signer over such a body — the
   reviewer's composition fixture — and removing only the tag check
   turns the strict correspondence red. Recorded on the library's D-6
   entry; carried, never removable on single-removal evidence.
9. **Four things this family was never asked to model (item 29), each
   assigned:** the combined report — standing alongside the P4 verdict
   for *one* request — is the capstone's; policy non-rewriting is
   P4's; relying-party recording is the relying-party story's;
   temporal replay against the anchor is the A2.1 bridge's (ledger
   C-2). And A3 §A3.7's adjacent obligations — retention, verified
   handoff, delivery expiry, disclosure and minimization — were never
   this family's target: nothing here bears on them either way.

One design question the review raised is **routed and unruled** (C10,
item 23); it is stated in `RESULTS.md` and nothing in this aid or in
any model has been changed for it.

---

## 1. Q1d — `ss_q1_strict_dns_compromised.pv` (correct, strict, DNS leaked)

### 1a. Cast

| Name | What it is in the design | Built | Consumed |
|---|---|---|---|
| `skD`, `skR` | DNS / repository channel signing keys; **`skD` leaked** at 375 | 369 | 210–216 (sign evidence); 380 (verifier public keys) |
| `skH1`, `skH2` | the two honest issuers' keys — **private free names** so queries can write `pk(skH1)` (180–183) | 113–114 | 370–371 (fingerprints into manifests); 372 (public keys published); 378–379 (roles) |
| `m`, `m2` | **the key statement (manifest)** for each honest issuer: `authTuple(issuerId, fp(pk(skH1)), ssetH, algH, verH)` and its twin | 370–371 | 373 (published); 376–377 (both channels sign each); 378–379 (issuers) |
| `p1`, `p2` | the two attempts' payloads, **adversary-chosen** | read 222 / 246 | 226, 231 (inside frames) |
| `decl1`, `decl2`, `declT` | declared times of attempt 1, attempt 2, and the terminal disposition — fresh names (A2.4: re-declaration moves time forward, so honest cores never coincide) | 223 / 247 | 228, 233 (cores); 239–240, 260–261 (TLR body) |
| `ppf` | possession proof = manifest self-signature `sign((POSS, m), skI)` (D-3) | 225 / 249 | 228, 233 (in the cores); envelope check 345 |
| `framed(...)` | S-P3's seven-field frame, copied verbatim (`OT_ATTEST`, alg, id, fp, `h(m)`, canonVer, payload) | 108 | built 226/231; matched 347 |
| `fb1`, `fb2`, `sg1`, `sg2` | framed bytes and attestation signatures of the two attempts | 226–227, 231–232 | cores 228/233; published 230/235; envelope 346 |
| `attemptCore(t, ppf, sg, decl)` | **the signed core of one attempt** — what identity is derived from | 117 | built 228, 233 (and 252, 257); published 230, 235; **hashed at 236–237**; destructured only by the envelope 344 |
| `aid1`, `aid2` = `h(core)` | **the derived identities** of the two attempts | 236–237 | 238 (`Designated`), 239 (lineage), 240 (terminal), 241 (judge) |
| `wrapCore(inner, outer)` | a wrapper-shaped outer artifact (ruling A7); **no honest process builds one**; adversary vocabulary | 121 | nowhere honest; available at every `in(c, …)` |
| `entry(aid, disp)`, `lineage2(e1, e2)` | one lineage entry; a lineage of exactly two | 125–126 | 239, 260 (built); 269–273 (destructured by `lookup2`) |
| `DISP_ABANDONED`, `DISP_SHIPPED` | per-entry dispositions | 127–128 | 239, 260; checked 284 |
| `TERM_SHIPPED(aid)`, `TERM_REFUSED` | terminal disposition: "SHIPPED <attempt>" / "REFUSED" | 129–130 | 240, 261 (built); 278, 282 (checked) |
| `body` = `(lineage, terminal, declT)` | the TLR body | 239–240 / 260–261 | signed at 242 / 262 under the library tag `TLR` |
| `sign((TLR, body), skI)` | **the terminal lineage record** — the standing evidence | 242 / 262 | read from the bundle 313; verified 319 |
| `noTLR`, `withTLR(kT, tlrSig, ap)` | standing evidence as carried in a bundle: absent, or (claimed TLR key, TLR, anchor proof) | 133–134 | 309 (absent → S3); 313 (present) |
| `anchorProof(h(tlr))` | anchoring as a **public oracle** (A1.3 item 5): any term over `h(TLR)`; time not represented | 136 | checked 321 (carried, inert — abl2) |
| `ESTABLISHED`, `ABSENT`, `UNVERIFIABLE` | the A3.7.1 verdicts | 139–141 | every `StandingReport` |
| `TERMINAL_DISPOSITION_SHOWN`, `SUPERSEDED`, `NO_TERMINAL_DISPOSITION_EVIDENCE`, `ISSUANCE_REFUSED` | S1–S4 reason codes (first-link `DECISION.md` exit condition 3 as amended) | 142–145 | 286, 292, 310, 279 |
| `STANDING_EVIDENCE_MALFORMED`, `…_TEMPORAL_MISMATCH` | SC-3's two outcomes | 146–147 | 290/295, 328 |
| `STANDING_EVIDENCE_MISMATCH`, `…_SIGNATURE_INVALID` | probe-recorded codes (vocabulary completeness) | 148–149 | 326, 330/332 |
| `PATH_S2/S3/S4` | which branch emitted a no-standing code (for the reason judge) | 151–153 | 280, 293, 311 |
| `designCh`, `estCh`, `reasonCh` | private judge channels | 156–158 | 241 / 287 / 280, 293, 311; judges 355, 359, 364–365 |
| `Designated(k, aid)` | "the issuer holding `k` designated derived identity `aid` as shipped" — fired **before** the TLR leaves | 160 | 238; right-hand side of (i)/(ii) 176–183 |
| `Established(k, t, aid)` | "the standing path reported ESTABLISHED against `k`, tuple `t`, identity `aid`" | 162 | 285; left-hand side of (i)/(ii) |
| `StandingReport(v, r, k, t, aid)` | the report, for vocabulary witnesses | 164 | every branch 279–332; queries 194–203 |
| `StandingUnentitled`, `HonestStandingEstablished`, `ReasonCollapsed` | judge events (§0.2) | 166–170 | 357, 360, 366; queries 186–191, 206–207 |
| `lookup2(aid, lin)` | model-local destructor: the disposition recorded for `aid` in a two-entry lineage; fails if absent | 269–273 | 323 |
| `t`, `evD`, `evR`, `kX`, `core`, `fb`, `se` | **the bundle** as the presenter hands it over (tuple, two evidences, artifact key, core, framed bytes, standing evidence) | read 301–302 (and 338–339) | standing path 304–332; envelope 340–349 |
| `id`, `kfpr`, `ss`, `alg`, `ver` | fields of `t` | 306 / 342 | `kfpr` 315 / 343; `alg`, `id` 347; **`ss`, `ver` never used** |
| `kT`, `tlrSig`, `ap` | the TLR's claimed key, the TLR, its anchor proof | 313 | 315, 317, 319, 321 |
| `lin`, `terminal`, `declT` | the TLR body's fields | 319 | 323; 278–282; **`declT` never used** (its content is ledger C-2) |
| `d`, `shippedId` | the looked-up disposition; the identity the terminal names | 323; 282 | 284; 283 |
| `AuthorityDNS`, `AuthorityRepo` | the two channels: fire the library event, emit evidence | 210–216 | 376–377 (each channel publishes **both** honest manifests) |
| `ShipIssuer` | honest issuer, lineage shape "a1 abandoned, a2 shipped" | 221–242 | 378–379 (**both keys**) |
| `RefuseIssuer` | honest issuer, lineage shape "both abandoned, REFUSED"; fires no `Designated` | 245–262 | 378–379 (**both keys**) |
| `StandingDecide` | the terminal decision once `aid` is found in the lineage | 277–295 | called 324 |
| `StandingPath` | **the standing verifier** | 300–332 | 380 |
| `EnvelopePath` | the P4 verifier (S-P3's strict verifier verbatim), same bundle, separate process | 337–349 | 380 |
| `Judge`, `ReasonJudge` | §0.2 | 354–366 | 381 |

### 1b. The standing path's checks (lines 300–332, with `StandingDecide` 277–295)

Provenance of the labels: companions Q2/Q3/Q4 and the six ablation
probes (`RESULTS.md` "Ablation probes", run on this file), and — since
2026-09-06 — the cross-family reviewer's single-removal matrix
(`proverif/falsification-2026-09-06/scratch/dependency-index.txt`).
"Inert" means every one of the eleven results was unchanged when that
one check was removed **by itself, in this fixture** (§0.3 item 4): it
is not permission to remove two together, and it can flip under
composition. *(Reworded 2026-09-06, cross-family falsification review
items 4 and 25; the sentence replaced said the companions "each
remove one check and go red on a named query", which is true of Q2 and
Q3 and not of Q4 — Q4 removes two checks and rearranges the fixture.)*

| Line | Check | Plain meaning | Status |
|---|---|---|---|
| 304 | `let (=STMT_DIGEST, =h(t)) = checksign(evD, pkD)` | DNS evidence is a DNS-key signature over the digest of the presented tuple | **CARRIED, inert** (abl4): the DNS key is public (375), so this evidence exists for any `t` |
| 305 | `let (=STMT_DIGEST, =h(t)) = checksign(evR, pkR)` | same, for the honest repository channel | **LOAD-BEARING for (i)** (abl5: removing it makes (i) false — the adversary's own tuple becomes "evidenced" and its own key entitled to it); `h` injective pins `t` to `m` or `m2` |
| 306 | `let authTuple(id, kfpr, ss, alg, ver) = t` | read the tuple's fields | structural |
| 308 | `let aid = h(core)` | **the identity is computed from the core the verifier holds** — never read from the bundle | **LOAD-BEARING for (i)/(ii)** (Q2: replacing it by a presented label makes both false, two trace shapes) |
| 309–311 | `if se = noTLR then … NO_TERMINAL_DISPOSITION_EVIDENCE` | no standing evidence → S3 | the S3 branch; witness `.out:1472` |
| 313 | `let withTLR(kT, tlrSig, ap) = se` | unpack the standing evidence | structural |
| 315 | `if fp(kT) = kfpr` | **the TLR's key is the key the evidenced tuple names — inside the standing path** | **LOAD-BEARING for (iii)** (Q3: removing it makes `StandingUnentitled` reachable); else branch 332 reports `SIGNATURE_INVALID` |
| 317 | `if kT = kX` | the TLR key equals the key the artifact presents (probe fixture shape) | **CARRIED, inert** (abl1; reviewer matrix 12) — and required by **no registered text** (§0.3 item 7) |
| 319 | `let (=TLR, (lin, terminal, declT)) = checksign(tlrSig, kT)` | the TLR verifies under that key and carries the `TLR` tag | **LOAD-BEARING for (i)/(ii)** (abl6: reading the body unsigned makes both false); else 330. The **key** binding is what carries it here; the **tag** alone is inert in this fixture and load-bearing under composition (§0.3 item 8; reviewer matrix 14) |
| 321 | `let anchorProof(=h(tlrSig)) = ap` | the anchor proof presented is over the TLR presented | **CARRIED, inert** (abl2); the temporal content is ledger C-2; else 328 emits the code for vocabulary |
| 323 | `let d = lookup2(aid, lin)` | the derived identity is in the lineage (with disposition `d`) | **LOAD-BEARING for (i)/(ii)** jointly with 308 (the lookup is where a foreign identity is rejected); else 326 `STANDING_EVIDENCE_MISMATCH` — G1's correct-side polarity, witness `.out:1927` |
| 278–280 | `if terminal = TERM_REFUSED` → `ISSUANCE_REFUSED` | refused lineage → S4 | the S4 branch; witness `.out:1752` |
| 282–283 | `let TERM_SHIPPED(shippedId) = terminal` … `if shippedId = aid` | the terminal designates **this** identity | **LOAD-BEARING JOINTLY with 284**, and **singly for the S2 vocabulary** (SC-3): removing this predicate alone, keeping `d = DISP_SHIPPED`, leaves (i)–(iii) green and loses the S2 witness (reviewer matrix 19); removing the whole terminal predicate, the 278–280 refused branch included, loses S2 and S4 (matrix 20), and removing that branch alone loses S4 (matrix 22); Q4 removes *both* and rearranges the fixture, so its red is the joint removal's. The `else` at 292 is S2 `SUPERSEDED`, witness `.out:1347`. *(Narrowed 2026-09-06, review item 25; read "LOAD-BEARING for (i)/(ii) (Q4: ignoring the terminal makes both false, two shapes)".)* |
| 284 | `if d = DISP_SHIPPED` | well-formedness: the entry for the designated identity reads shipped | **CARRIED, inert singly** (abl3; reviewer matrix 21), **load-bearing jointly with 282–283** (Q4 removes both); the F1 shape needs an honest issuer to sign a malformed TLR; vector obligation |
| 285–287 | `event Established; event StandingReport(ESTABLISHED, …); out(estCh, …)` | the report, and the judge's input | the events the queries are about |

**The envelope path (337–349)** is S-P3's strict verifier line for line
(evidence 340–341; `fp(kX) = kfpr` 343; possession over the manifest
345; attestation signature 346; frame binding 347; manifest hash 348;
`Accept` 349) reading the core's fields at 344. It is **CARRIED whole**:
no query here mentions `Accept`; its labels are S-P3's (`s-p3/READING-AIDS.md`
§1b). It exists so that orthogonality is structural (F3).

### 1c. Results (`ss_q1_strict_dns_compromised.out`)

| Query | `.out` line | Result | Meaning |
|---|---|---|---|
| (i) `Established(kX,t,aid) ==> Designated(kX,aid)` | 457 | **true** | every ESTABLISHED, under any key, was preceded by that key's holder designating that derived identity |
| (ii) same with `pk(skH1)` / `pk(skH2)` | 467 / 477 | true / true | the sentence per honest issuer |
| (iii) `StandingUnentitled` | 484 | unreachable | no ESTABLISHED against a key the evidenced tuple does not name |
| (iv) N1 `HonestStandingEstablished` | 781 | **reachable** | the honest flow reaches ESTABLISHED and the judge confirms the designation (trace 486–780: `Designated` 763, bundle in 767, `Established` 769, judge 773–777) |
| S1 witness | 1065 | reachable | shipped attempt with its TLR |
| S2 witness | 1347 | reachable | the abandoned attempt (`decl1`) of a shipped lineage with its TLR |
| S3 witness | 1472 | reachable | any artifact, `noTLR` |
| S4 witness | 1752 | reachable | an attempt of a refused lineage with its TLR |
| MISMATCH witness | 1927 | reachable | an adversary-built core `a_4` with an honest TLR — the transplant, *rejected* |
| B9 `ReasonCollapsed` | 1934 | unreachable | S2/S3/S4 emit three distinct codes |

### 1d. Claim, adversary, boundary (plain language)

**Claim (header 20–32; F1).** A relying party who runs the standing
path will say "this artifact has standing" only for an artifact whose
own bytes — hashed by the verifier, never labelled by anyone — appear in
a lineage record that the entitled issuer signed, with that record's
terminal line naming exactly that artifact as the one shipped. It will
never say so against a key the authority statement does not name. And
the honest case does reach "standing" (N1). This is A3.7.1's three
bindings — issuance identity, attempt lineage, terminal disposition —
under one signature, checked against a compromised authority channel.

**Adversary (A1.3; fixture 368–375).** Sees everything on `c`; holds
the DNS channel's private key (375) and can publish any tuple through
DNS; chooses every payload the honest issuers sign (222, 246); builds
cores, wrappers, lineages, TLR-shaped objects, anchor proofs and bundles
freely (`[data]`); anchors anything; has DSKS (`lib:110`); holds every
key it uses. Does **not** hold `skR`, `skH1`, `skH2`.

**Why the attack fails.** The honest repository channel signs only
`h(m)` and `h(m2)` (377), so the tuple the standing path is shown is an
honest one (305, `h` injective) and names an honest fingerprint; 315
forces the TLR key to be that honest key (`fp` injective); 319 then
accepts only a TLR that honest key signed — and the honest issuers sign
lineages naming only `h` of their own cores (239–240, 260–261). The
presented core must hash to one of those (323, `h` injective), so the
presented core *is* an honest core; the terminal must name it (282–283);
and the issuer fired `Designated` for exactly that identity before
releasing the TLR (238, 241–242). A wrapper around an honest core, a
core with one field changed, a core from another lineage: each has a
different `h` and stops at 323 (`STANDING_EVIDENCE_MISMATCH`). Note
what did *not* matter: the DNS evidence (abl4), the `kT = kX` check
(abl1), the anchor check (abl2), the well-formedness check (abl3).

**Boundary (header 33–43; `RESULTS.md` "What S-STANDING does not
discharge").** Not the degraded case (Q1deg). Nothing temporal — the
anchor is a public oracle and time is absent (C-2). Nothing about a
second TLR under the same key (G4). Nothing about malformed evidence
beyond emitting a code (vector). Nothing about the implementation's
reason codes (vector, F6). Nothing about which identity a *wrapped
bundle's* standing should be computed against (S-P7, C-4): this model
reports on the artifact presented. Nothing about the core's byte
layout (P8, C-3). Nothing about the P4 verdict. Two-entry lineages
only. `fp` and `h` are collision-free by fiat: **the transplant result
is a statement about a perfect hash.** And, added 2026-09-06 from the
cross-family falsification review: nothing about signature-set
operations, byte encodings or verdict values, which are unrepresentable
here (§0.3 items 1–3); nothing about the unrestricted sentence beyond
this fixture — an honestly enrolled adversary-owned issuer falsifies it
while (ii) and (iii) hold, and (ii) is the claim (§0.3 item 6, review
item 24); nothing about the combined standing-plus-verdict report for
one request, policy non-rewriting, relying-party recording, or temporal
replay against the anchor (§0.3 item 9, review item 29).

### 1e. Read and never used (Q1d)

`ss`, `ver` (306, 342); `declT` (319); `ot`, `cv`, `pl` (347); `id` at
the envelope 347 is checked, at the judge `idJ` is read only (356).
Library: `STMT_DIRECT`, `REFUSAL`, `fbH`, `OT_*` other than
`OT_ATTEST`; the events `AuthorityPublishedDNS/Repo`, `IssuerPossession`,
`IssuerSigned`, `Accept` are fired and never queried.

---

## 2. Q1r — `ss_q1_strict_repo_compromised.pv` (correct, strict, repository leaked)

Line for line the same file as Q1d with two extra header lines (the
body is shifted by +2: standing path 302–334, envelope 339–351, judges
356–368, process 370–383) and one changed action: **377 `out(c, skR)`**
— the repository key is leaked and the DNS key stays honest. Every table
in §1 applies with the substitutions:

- §1a: `skR` is the leaked key; `skD` honest.
- §1b: line 306 (DNS evidence, Q1r numbering) is the **LOAD-BEARING**
  channel check and 307 (repository) the inert one — by the same
  reasoning as abl4/abl5, which were run on Q1d, not on this file
  (inferred, not ablated, exactly as `s-p3/READING-AIDS.md` §2 says of
  its repo variant).
- §1c: results identical, same `.out` line numbers (457, 467, 477,
  484, 781, 1065, 1347, 1472, 1752, 1927, 1934).

**Claim / adversary / boundary:** as §1d with "DNS" and "repository"
exchanged. The point of running both (plan, §"Adversary and modes": "a
generic single channel is not accepted as representing both") is that
neither channel's honesty is assumed by name.

---

## 3. Q1deg — `ss_q1d_degraded_compromised.pv` (correct, degraded, sole channel leaked)

### 3a. Cast — differences from Q1d

The declarations (80–142), queries (148–179), issuers (192–233),
`lookup2` (240–244), `StandingDecide` (248–266), judges (323–335) are
Q1d's with shifted lines. What changes:

| Name | What it is | Built | Consumed |
|---|---|---|---|
| `skS` | the **sole** authority channel's signing key — **leaked** at 344 | 338 | 182–184 (signs evidence); 348 (verifier key) |
| `AuthorityS` | the sole channel (fires the library's `AuthorityPublishedDNS`, as S-P3 Q2 did) | 182–184 | 345 (publishes both honest manifests) |
| `ev` | the sole evidence, in place of `evD`, `evR` | read 272 / 308 | 275 / 310 |
| `AcceptS(ev, t, kX, fb)` | model-local **degraded** acceptance (spike Q5 / S-P3 Q2 shape) — the degraded-shape event; whether the verdict is *marked* degraded is P4's (§3d) | 187 | emitted 318; never queried; not shown reachable in the `.out` |
| `StandingPath(pkS)`, `EnvelopePath(pkS)` | single-evidence paths | 271–302, 307–318 | 348 |

Fixture as Q1d: two honest issuers, both shapes each (346–347).

### 3b. The standing path's checks (271–302) — difference from Q1d

Only the evidence check differs: 275 `checksign(ev, pkS)` — **inert by
construction** (the key is public at 344; S-P3 F6: "the adversary's
condition, not something the checks defend against"). Consequence: the
evidenced tuple is whatever the adversary signs, so 285 (`fp(kT) =
kfpr`) now pins the TLR key to *the presented tuple's* key, not to an
honest one. Every other label in §1b stands (the companions and
ablations were run in strict mode; the mechanism at 278–302 is
identical).

### 3c. Results (`ss_q1d_degraded_compromised.out`)

| Query | `.out` line | Result | Meaning |
|---|---|---|---|
| (i) unrestricted | **589** | **false — trace found** | 581: `skS` leaked; 583: the bundle — the adversary's own tuple `authTuple(a_1, fp(pk(a_2)), …)` with evidence signed by `skS`, key `pk(a_2)`, core `a_6`, TLR `sign((TLR, (lineage2(…, entry(h(a_6), DISP_SHIPPED)), TERM_SHIPPED(h(a_6)), …)), a_2)`; 587: `Established(pk(a_2), …, h(a_6))` with no `Designated` |
| (ii) `pk(skH1)` / `pk(skH2)` | 598 / 607 | **true** | no honest issuer's standing is usurped |
| (iii) `StandingUnentitled` | 613 | unreachable | the adversary must bring its *own* tuple; against an honest tuple its key is rejected at 262 |
| N1 | 917 | reachable | honest flow intact |
| S1 witness | 1098 | reachable — **by the adversary's own key** (`pk(a_2)`) | why the N1 witness is the judge's |
| S2, S3, S4, MISMATCH | 1280, 1388, 1566, 1719 | reachable | vocabulary live |
| B9 | 1725 | unreachable | |

### 3d. Claim, adversary, boundary

**Claim (header 15–20; F2, ledger P-3).** With the only authority
channel in the adversary's hands, a relying party running these checks
still never reports standing *under an honest issuer's key* for an
artifact that issuer did not designate, and never reports it against a
key the presented statement does not name. What it cannot do is tell an
honest statement from the adversary's: the adversary publishes its own
statement through the compromised channel, ships its own artifact, signs
its own lineage record, and is reported as having standing for it.

**The registered ruling this rests on** — Amendment 4 §A4.6, RULED
(author), 2026-09-06, `docs/phase-0-prereg-amendment-4.md` lines
152–167, entered in `PREDICTIONS.md` routed item 4 as ROUTED A8:

> In degraded mode — any verdict other than `VALID_STRICT`, including
> the sole-channel-compromised case — the verifier's job is to hand the
> adjudicator the evidence of what could and could not be excluded,
> marked as degraded per §A1.2.1's explicit-policy logic. Tessera does
> not decide whether the adjudicator should trust the attestation and
> must not try to. A correspondence that holds in strict mode and fails
> in degraded mode is therefore a registered **cost** of degradation,
> to be stated in the relying-party story, never a defect of the
> construction — provided the verdict says it is degraded.

Whether the verdict is marked degraded is P4's obligation (§A1.2.1
explicit-policy logic; cross-formalism, carried here and not checked):
this model's envelope path fires the degraded-shape event `AcceptS`
(318), which is neither queried nor shown reachable in the `.out` (the
name appears only in the process listing, `.out:189`, `395`). §A4.6's
proviso is therefore assumed to be met by P4, not shown here; the cost
is the adjudicator's to weigh. *(Reworded 2026-09-06 after the skeptic
review, finding 2; the sentence it replaces read "The envelope path
here reports `AcceptS` (295), the degraded shape; the verdict says
degraded".)*

**Adversary.** As §1d plus: holds the *only* authority key (344) — a
fixture strictly stronger than A1.3 item 6's "proper subset" (S-P3 F6).
Still does not hold `skH1`, `skH2`.

**Boundary.** Everything in §1d, and: the unrestricted sentence (i) is
**not** proved here and is not claimed; what this model proves is the
*shape* of the cost (its own key over its own objects, F2) and what
survives it ((ii), (iii)). The cross-family review's item 24 lands here
as confirmation rather than as news: in strict mode (i) is fixture-bound
and an honestly enrolled adversary-owned issuer falsifies it; in
degraded mode the compromised channel lets the adversary enrol itself,
which is the same failure reached by a cheaper route. *(Added
2026-09-06.)*

### 3e. Read and never used (Q1deg)

As §1e; `AcceptS` is emitted at 318, never queried, and not shown reachable in the `.out` (§3d).

---

## 4. Q2 — `ss_q2_companionA_identity_declared.pv` (companion A: identity declared; wrapper transplant)

### 4a. Cast — differences from Q1d

| Name | What it is | Built | Consumed |
|---|---|---|---|
| `LBL1`, `LBL2` | **MUTATION 1:** per-lineage labels (the probe's ordinal binding); public constants; every lineage of every issuer uses the same two | 103–104 | lineages 223–224, 245–246; terminal `TERM_SHIPPED(LBL2)` 224 |
| `lbl` | **MUTATION 2:** the label the *presenter* claims for the artifact — an adversary-writable bundle field | read 290 / 327 | looked up 311; compared 268 |
| `EstablishedWrapped(k, t, aid)` | **A7:** fired in addition to `Established` when the presented core is `wrapCore(…)` | 140 | 274–275; query 156–157 |
| `StandingDecide(kT, t, aid, core, lbl, d, terminal)` | two extra parameters | 262 | called 312 |

Unchanged: `Designated` still carries the **derived** `h(core2)` (221);
`Established` still carries the derived `h(core)` of the presented
artifact (270, via 296). That is what makes the label a transplant
surface rather than a renaming: the identities in the correspondence
are the artifacts', the lookup is by a name anyone can write.

### 4b. The standing path — difference from Q1d

| Line | Change | Effect |
|---|---|---|
| 311 | `let d = lookup2(lbl, lin)` (was `lookup2(aid, lin)`) | the lineage is searched for the *claimed* label; the derived identity plays no part in the lookup |
| 268 | `if shippedId = lbl` (was `= aid`) | the terminal is compared to the label |
| 272–275 | `( out(estCh, …) \| let wrapCore(inner, outer) = core in event EstablishedWrapped(…) )` | the second trace's event, fired for wrapper-shaped cores |

Everything else — evidence 292–293, `fp(kT) = kfpr` 303, `kT = kX`
305, the TLR signature 307, the anchor 309, `TERM_REFUSED` 263, `d =
DISP_SHIPPED` 269 — is Q1d's.

### 4c. Results (`ss_q2_companionA_identity_declared.out`)

| Query | `.out` line | Result | The trace |
|---|---|---|---|
| (i) | **630** | **false** | 624: honest tuple `m2` with honest evidence, key `pk(skH2)`, an **adversary core `a_4`**, `withTLR(pk(skH2), <honest TLR of skH2>, …)`, and `lbl = LBL2`; 626 (restated 628): `Established(pk(skH2), m2, h(a_4))` — an identity nobody designated |
| (ii) `pk(skH1)` / `pk(skH2)` | **808** / **986** | **false** / **false** | same shape under each honest key |
| A7 `EstablishedWrapped ==> Designated` | **1176** | **false** | 1166: the core is **`wrapCore(a_4, a_5)`** — a wrapper-shaped outer artifact — with `LBL2` and the honest TLR; 1172 (restated 1174): `EstablishedWrapped(pk(skH2), m2, h(wrapCore(a_4, a_5)))` |
| (iii) `StandingUnentitled` | 1182 | unreachable | the key is honest throughout — as the plan required |
| N1 | 1514 | reachable | the honest flow still works (honest core, `LBL2`) |
| S1–S4, MISMATCH witnesses | 1692, 1868, 1996, 2170, 2346 | reachable | |
| B9 | 2352 | unreachable | |
| **post-freeze, UNREGISTERED:** `EstablishedWrapped(k,t,h(wrapCore(inner,outer))) && Designated(k,h(inner))` | **2685** | **reachable** | the literal A7 transplant: 2684 is the trace — `inner` = the core `skH2` fired `Designated` for, `outer` = adversary-chosen `a_12`, `skH2`'s honest TLR as standing evidence, `lbl = LBL2`. Added 2026-09-06 under review item 26; **not a registered prediction** — see `RESULTS.md` "Post-freeze additions (unregistered)" |

### 4d. Why the attack succeeds, and its boundary

The honest TLR of `skH2` says "the attempt labelled `LBL2` shipped". The
adversary hands over *any* core — its own, or a wrapper around the
honest shipped core — and writes `LBL2` in the label field. The
standing path checks everything about the TLR correctly (right key,
right signature) and then asks the lineage about the label, not about
the artifact. `ESTABLISHED` follows for an artifact the issuer never
saw. This is the standing probe's Q3 ordinal-binding result
(`RESULTS-PROBE.md` "What the TLR had to be" item 1: "The ordinal
variant is not a weaker binding; it is no binding") mechanized under
A1.3, with the wrapper shape A3.9 names exhibited (ruling A7).

*(Narrowed 2026-09-06, cross-family falsification review item 26.)* The
registered A7 query `EstablishedWrapped ==> Designated` constrains only
that the presented core **is a wrapper**; neither it nor the event binds
the wrapper's inner value to anything, and its committed trace
(`.out:1166–1176`) uses arbitrary `a_4` and `a_5`. So that trace alone
shows a transplant onto a *wrapper-shaped* core, not a wrapper around
the honest shipped core. The literal A7 transplant is exhibited by the
**unregistered post-freeze companion query** added at
`ss_q2_companionA_identity_declared.pv:189–190` and recorded in
`RESULTS.md` under "Post-freeze additions (unregistered)": it requires
one trace in which the wrapper's inner value is a core the honest
issuer designated as shipped, and it is reachable
(`.out:2685`, trace `.out:2684`) with `inner` = `skH2`'s shipped core
and `outer` = an adversary-chosen value.

**Boundary:** evidence only against Q1d; it discharges nothing; the
re-scoping question for wrapped bundles remains S-P7's (F5).

### 4e. Read and never used

As §1e, plus `inner`, `outer` (274): bound, never used — the event
needs only that the core *is* a wrapper.

---

## 5. Q3 — `ss_q3_companionB_entitled_via_envelope.pv` (companion B: entitled key via envelope only)

### 5a. Cast — differences from Q1d

None in the declarations (54–116), queries (122–152), issuers
(167–208), judges (299–311), fixture (313–326). The mutation is one
removed check in the standing path.

### 5b. The standing path — difference from Q1d

| Line | Q1d had | Q3 has | Effect |
|---|---|---|---|
| 260–263 | `if fp(kT) = kfpr then ( if kT = kX then …` (Q1d:315–317) | `( if kT = kX then …` — **no fingerprint comparison** | the standing path accepts a TLR under any key that equals the artifact's presented key; whether that key is the one the evidenced tuple names is left to the envelope path (288, unchanged) |

Everything else is Q1d's: evidence 250–251; derived identity 254; TLR
signature 265; anchor 267; lookup 269; terminal 224–229.

### 5c. Results (`ss_q3_companionB_entitled_via_envelope.out`)

| Query | `.out` line | Result | The trace |
|---|---|---|---|
| (iii) `StandingUnentitled` | **860** | **reachable — the discriminating red** | 848: **honest** tuple `m2` with honest evidence from both channels; key `pk(a_2)` (adversary's); core `a_3` (adversary's); TLR under `a_2` naming `h(a_3)` shipped; 850: `Established(pk(a_2), m2, h(a_3))`; 856: the judge sees `fp(pk(a_2)) ≠ fp(pk(skH2))` and fires |
| (i) | 628 | false | the same adversary-key shape as Q1deg — predicted; not the discriminator |
| (ii) | 642 / 656 | **true** | no honest key involved |
| N1 | 1157 | reachable | |
| witnesses | 1357, 1558, 1686, 1883, 2055 | reachable | |
| B9 | 2062 | unreachable | |

### 5d. Why the attack succeeds, and its boundary

The blind re-scoring's conformance note (ENUMERATION note 4 item 2): a
bundle whose envelope fails `KEY_FINGERPRINT_MISMATCH` must not receive
a standing report computed against an unentitled key. Here the envelope
*would* fail (288: `fp(pk(a_2)) ≠ kfpr` of `m2`) — but the standing path
is a separate process on the same bundle and, without its own
fingerprint check, computes `ESTABLISHED` against `pk(a_2)` anyway. In
the correct form the same bundle is reported
`UNVERIFIABLE`/`STANDING_EVIDENCE_SIGNATURE_INVALID` — by inspection of
Q1d:315 and 331–332, not a queried witness; only (iii)'s
unreachability is in the `.out`. The plan's p≈0.2
worry — that a sequential verifier would let the envelope's check
shadow the missing one, making the companion unable to fail — did not
materialize because the two paths are parallel (F3). **What
distinguishes Q3's red from Q1deg's:** in Q3 the tuple is honest and
the key is not entitled to it (the judge fires); in Q1deg the tuple is
the adversary's own (the judge is silent). **Boundary:** evidence only
against Q1d.

### 5e. Read and never used

As §1e.

---

## 6. Q4 — `ss_q4_companionC_terminal_unchecked.pv` (companion C: terminal disposition unchecked)

### 6a. Cast — differences from Q1d

| Name | Change | Lines |
|---|---|---|
| `StandingDecide` | **MUTATION 1:** collapsed to the S1 branch — `Established`, the S1 report, `out(estCh, …)`; `d` and `terminal` are received and never read | 231–237 |
| fixture | **MUTATION 2 (registered fixture exception):** `skH1` runs only `ShipIssuer`, `skH2` only `RefuseIssuer` — one lineage shape per key, so one trace per query shows one shape each; both terminal values remain in the fixture | 320–322 |

### 6b. The standing path — difference from Q1d

Lines 242–274 are Q1d's 300–332 (evidence 246–247; derived identity
250; `fp(kT) = kfpr` 257; `kT = kX` 259; TLR 261; anchor 263; lookup
265). The difference is entirely at 234–237: membership in the lineage
is enough; `TERM_REFUSED`, `TERM_SHIPPED(=aid)` and the well-formedness
check are gone. Consequence (not a result): the S2 and S4 branches do
not exist, so their witnesses are unreachable and `reasonCh` carries
only S3 reports.

### 6c. Results (`ss_q4_companionC_terminal_unchecked.out`)

| Query | `.out` line | Result | The trace |
|---|---|---|---|
| (ii) `pk(skH1)` | **849** | **false** — shape 1 | 843: the bundle presents the core with **`decl1`** — the *abandoned* attempt of `skH1`'s shipped lineage — with that lineage's TLR; 845: `Established(pk(skH1), m, h(attemptCore(…, decl1)))`; `Designated` (at `.out:839`) was for the `decl2` core. **S2 reported as established.** |
| (ii) `pk(skH2)` | **1123** | **false** — shape 2 | 1115: `skH2`'s TLR with `TERM_REFUSED` published; 1117: an attempt of that lineage presented with it; 1119: `Established(pk(skH2), m2, …)`; `skH2` fires no `Designated` at all. **S4 reported as established.** |
| (i) | 576 | false | either shape |
| (iii) | 1129 | unreachable | keys honest throughout |
| N1 | 1425 | reachable | |
| S1, S3, MISMATCH witnesses | 1701, 1831, 2009 | reachable | |
| S2, S4 witnesses | 1708, 1838 | **unreachable** (consequence of the mutation) | |
| B9 | 2015 | unreachable (trivially) | |

### 6d. Why the attack succeeds, and its boundary

A3.7.1's third binding — terminal disposition — is what separates "this
attempt is in the lineage" from "this attempt is the one that shipped".
Without it, every attempt the issuer ever made and abandoned (S2), and
every attempt of a lineage the issuer refused (S4), reads as having
standing. The two shapes are distinct traces because the fixture puts
one shape under each key; S4 is not S2 under another name (F4).

*(Narrowed 2026-09-06, cross-family falsification review item 25.)*
Read the red as the **joint** removal's, not the terminal check's
alone. This companion's `StandingDecide` reads neither `terminal` nor
`d`, and its fixture is rearranged besides. The reviewer removed the
terminal predicate *by itself*, keeping `d = DISP_SHIPPED`: (i)–(iii)
stayed green and only the S2 and S4 vocabulary witnesses disappeared
(matrix 19, 20). So the terminal check is load-bearing **singly for the
S2/S4 vocabulary** — which is exactly what SC-3 registers — and
load-bearing for safety only **jointly** with the per-entry check.

**Boundary:** evidence only against Q1d; the registered fixture
exception means this companion matches the correct form only up to the
rearrangement (plan, SS.Q4).

### 6e. Read and never used

As §1e, plus `d`, `terminal` (234): received, never read — the point of
the mutation.

---

## 7. Q5 — `ss_q5_companionD_reason_collapsed.pv` (companion D: reason codes collapsed; B9)

### 7a. Cast — differences from Q1d

| Name | Change | Lines |
|---|---|---|
| `NO_STANDING` | **MUTATION:** one code for S2 and S3 (the standing probe's Q4 collapsed verifier) | 94–95 |
| S2 branch | reports and emits `NO_STANDING` instead of `SUPERSEDED` | 237–238 |
| S3 branch | reports and emits `NO_STANDING` instead of `NO_TERMINAL_DISPOSITION_EVIDENCE` | 255–256 |
| S2/S3 witnesses | restated over `NO_STANDING` (one query for both) | 143–144 |
| B9 query | same query as Q1d, now **required reachable** | 151–152 |

`SUPERSEDED` and `NO_TERMINAL_DISPOSITION_EVIDENCE` stay declared
(87–88) and are emitted by nothing.

### 7b. The standing path — difference from Q1d

None in any check (245–277 are Q1d's 300–332); only the constants the
two branches report changed.

### 7c. Results (`ss_q5_companionD_reason_collapsed.out`)

| Query | `.out` line | Result | The trace |
|---|---|---|---|
| B9 `ReasonCollapsed` | **1965** | **reachable — red by construction** | 1951: an S3 report (`noTLR`) `NO_STANDING`; 1955: an S2 report (the `decl1` attempt with its TLR) `NO_STANDING`; 1957, 1959: both reach the reason judge; 1961: `ReasonCollapsed(PATH_S2, PATH_S3, NO_STANDING)` |
| (i), (ii), (iii), N1 | 457, 467, 477, 484, 781 | as Q1d | the mutation touches no check |
| S1, `NO_STANDING`, S4, MISMATCH witnesses | 1065, 1190, 1470, 1645 | reachable | |

### 7d. What this shows, and its boundary

Exactly what disposition B9 said it would (`ROUTED-2026-09-06.md` §B:
"predicted red-by-construction and recorded as such, *and* the vector
obligation stands"): the judge that is green in Q1d can go red, so that
green is not a companion-that-cannot-fail. The red is evidence about
two constants having been made one — not about the mechanism, and not
about any implementation. The discrimination check that matters (the
reference verifier's S2/S3/S4 outputs pairwise distinct; a collapsing
verifier failing) is the H1a/P8 S-series vector obligation, unchanged
(F6).

### 7e. Read and never used

As §1e, plus `SUPERSEDED`, `NO_TERMINAL_DISPOSITION_EVIDENCE` (87–88).

---

## 8. Observations about the testimony (comments and names), not the proofs

Recorded so a reviewer of the aids can weigh them; none changes a
result, and none was "fixed" here.

1. **`Designated` is fired for the derived identity in every model,
   including Q2.** A reader of Q2 alone might expect the label-bound
   issuer to designate the label. It does not, on purpose (§4a); the
   Q2 header says so (Q2:20–23). If the reader probe misreads this, the
   header line is the place to strengthen.
2. **The S1 witness in degraded mode is satisfied by the adversary
   (Q1deg `.out:1094`, restated 1096).** The header does not point at this line; §3c
   does. It is the concrete reason N1 is the judge's event, and a
   non-expert reading the witness list alone could take "S1 reachable"
   for "the honest flow works".
3. **`kT = kX` (Q1d:317) is labelled carried in the header (Q1d:81–83)
   and confirmed inert (abl1).** A reader may ask why it is there at
   all: it is the probe fixture's `tlr.pub == core.pub` shape, kept so
   Q3's registered mutation ("checks that the TLR's signing key equals
   the key the artifact presents … but does not compare that key's
   fingerprint") is a *removal* from the correct form and not a
   substitution.
4. **`declT` (Q1d:319) is read and never used.** Its content — the
   A2.1 predicate against the TLR's own anchor (SC-1) — is ledger C-2
   and cannot be expressed here. The name is kept so the TLR body has
   the shape the record fixed.
5. **The `AuthorityPublishedDNS` event is fired by the degraded sole
   channel (Q1deg:183)**, as in S-P3 Q2; the name is the library's
   two-branch vocabulary, not a claim that the sole channel is DNS.

## 9. Probe status

The lower-ceiling reader probe (note 5 item 2; the first-link Q3
precedent, `formal/spike/first-link/proverif/reading-aid-q3/PROBE-haiku-2026-09-06.md`)
has **not been run** for these models. Its inputs, when run, are the
comment-stripped `.pv` files, their RESULT lines, A3.7.1's text, A1.3,
and this document; the question is the standard one — claim,
adversary, boundary, stated twice. A failed probe is a defect in this
aid, never a verdict on the proofs, and does not block exit.

## Review log

- 2026-09-06 — drafted by the AI collaborator from the committed `.pv`
  and `.out` files, the ablation probes, and `RESULTS.md`; every
  LOAD-BEARING / CARRIED label traced to a companion red or an ablation
  no-change. No reader probe; no cross-family review; no author read.
- 2026-09-06 — second agent session (after a usage-limit interruption
  of the first; see `RESULTS.md` review log): every `file:line`
  citation in §§0–7 spot-checked against the `.pv` files (Q1d 204–210,
  272–291, 336–349; Q1r 345; Q1deg 252, 262, 295, 321; Q2 92–93, 248,
  252–255, 291; Q3 260–263, 288; Q4 219–225, 308–310; Q5 87–88, 94–95,
  143–144, 151–152, 237–238, 255–256) and every `.out` citation against
  the outputs (Q1d N1 trace 761–781; Q1deg 581–589 and 1096; Q2
  1166–1176; Q3 848–860; Q4 839–849 and 1113–1123; Q5 1951–1965): all
  as written. One `.pv` comment line was added to the Q5 header
  (`RESULTS.md` review log) without changing its line count, so §7's
  citations stand. No reader probe, no cross-family review, no author
  read.
- 2026-09-06 — **skeptic review applied** (see `RESULTS.md` review log,
  same date, for the full list). Here: §0.1 lib range `150–157` →
  `151–157` (150 is `OT_ATTEST`, used); §0.2 and §8 item 2 Q1deg
  `.out:1096` → `1094` (the event; 1096 is the "is executed"
  restatement); §4c Q2 `.out` `628` → `626` and `1174` → `1172` (same
  distinction); §3a's `AcceptS` row, §3d and §3e no longer say "the
  verdict says degraded" — `AcceptS` is unqueried and not shown
  reachable, and marking the verdict degraded is P4's obligation,
  assumed here; §5d marks the correct form's
  `UNVERIFIABLE`/`STANDING_EVIDENCE_SIGNATURE_INVALID` report as read
  from the code (Q1d:283, 299–300), not a queried witness. The `.pv`
  header edits recorded in `RESULTS.md` changed no file's line count,
  so every `file:line` citation in §§0–7 stands as written; the
  re-run `.out` files are byte-identical, so every `.out` citation
  stands. No reader probe, no cross-family review, no author read.
- 2026-09-06 — **cross-family falsification review applied** (see
  `RESULTS.md` review log, same date, for the full list and for what
  was *not* applied). Here, in the order a reader can check them:
  (a) new **§0.3**, "What these seven models cannot see", carrying the
  review's boundary items 1–4, 6, 24, 27, 28 and 29 as numbered
  sentences — the routed item 23 is deliberately **not** among them and
  nothing in this aid changed for it; (b) §1b's provenance paragraph
  reworded (items 4, 25) — "inert" now says explicitly that it is a
  single-removal observation in this fixture; (c) §1b rows 282–283 and
  284 re-partitioned to "load-bearing jointly", with the terminal check
  load-bearing singly only for the S2/S4 vocabulary (item 25), row 317
  marked as required by no registered text (item 28), and row 319
  splitting the key binding from the tag (item 27); (d) §1d and §3d
  boundary paragraphs extended (items 1–3, 24, 29); (e) §4c gains a row
  for the **unregistered post-freeze** companion query at `.out:2685`
  and §4d narrows the wrapper claim to what the registered A7 trace
  shows, pointing at that companion for the literal transplant (item
  26); (f) §6d reads Q4's red as the joint removal's (item 25).
  **Citations.** The review's header corrections lengthened five `.pv`
  files and the library, which moved every body line and so invalidated
  every `file:line` citation in §§0–8. Offsets were established by
  diffing each model against the reviewer's archived pre-edit mutants
  (`proverif/falsification-2026-09-06/scratch/m_dns_anchor.pv`,
  `m_repo_anchor.pv`, `m_deg_anchor.pv` — the body diff is the single
  mutated line in each, so the bodies are unchanged): **Q1d +32, Q1r
  +32, Q1deg +23, Q4 +12, Q2 +11 before its added query and +20 after
  it, Q3 and Q5 unchanged, `lib` +11.** Every `.pv` and `lib` citation
  in §§0–8 was remapped and spot-checked line by line against the
  files. `.out` citations did not move (ProVerif does not echo
  comments; all seven `.out` files are byte-identical to a fresh run)
  and were left alone. The two earlier entries of this log keep their
  original numbers: they record what was checked against the text of
  the day, and renumbering them would falsify that record. No reader
  probe; no author read.

---

## Post-freeze addendum 1 — results, 2026-09-12: SS.Q6 and SS.Q6-C

**STATUS: PROPOSED — 2026-09-12 — the AI collaborator's; not adopted.**
APPENDED, in this file's style; §§0–9 above are unchanged. Line numbers
in §§0–8 refer to the **pre-addendum** `.pv` text and were not fixed;
`RESULTS.md` §A1.8 carries the shift table. Everything below cites the
**post-addendum** text. Registered in `PREDICTIONS.md`, "Post-freeze
addendum 1 — 2026-09-12" (Amendment 5 §A5.6, ADOPTED (author); ROUTED
C10). Full results: `RESULTS.md` §"Post-freeze addendum 1 — results".

### 10. The question §A5.6 asks

The standing path has always bound the **key**: the TLR key must be the
key the evidenced authority tuple names (`fp(kT) = kfpr`, §1b). It never
bound the **tuple**. So a core issued under identity A, with A's honest
terminal lineage record, could be presented under a second honest tuple
naming the same key as identity B, and the standing path — which derives
`aid = h(core)` from the core it holds but reads the tuple from the
presenter — would report `ESTABLISHED` against B. The envelope path
already pins the tuple (`let attemptCore(=t, …) = core`, §1b's
`EnvelopePath`); `ENUMERATION.md` note 4 item 2 says the standing path
may rely on nothing the envelope path established, so it must do the
same check itself.

### 10a. Cast — differences from §1

Three additions to all three correct models and to the new companion.
Nothing is removed and no existing query changes.

| New name | Where (DNS `.pv`) | What it is |
|---|---|---|
| `issuerIdAlias` | 144 | a public free name: the alias identity |
| `mAlias = authTuple(issuerIdAlias, fp(pk(skH1)), ssetH, algH, verH)` | 446 | the **alias tuple** — H1's key, a different identity. Evidenced by **both** authority channels exactly as `m` is (451–452), and published (448). **No issuer runs under it**: H1 signs its TLR under `m` only, so the alias has an enrolment but no lineage |
| `aliasCh` | 197 | a fourth private report channel. `estCh` carries `(kX, t, aid)` and **not** the core, and `Established` is an event no judge can read — so the alias judge needed a channel of its own |
| `event Aliased(pkey, bitstring, bitstring, bitstring)` | 212 | key, presented tuple, the core's embedded tuple, derived identity |
| `AliasJudge` | 434–437 (companion 351–354) | reads `aliasCh`, destructures the core, fires when the two tuples differ. **Instrumentation, not a verifier check** — it observes the report, it does not gate it. Emits nothing when the core is not an `attemptCore` (the `let` has no `else`) |

`estCh`, `reasonCh`, `designCh`, `Judge` and `ReasonJudge` are
untouched, which is why §1's (iii) and B9 cannot move on the judges'
account.

### 10b. The standing path's one new check (DNS `.pv:373–387`)

| Line | What | Effect |
|---|---|---|
| 382 | `let attemptCore(=t, ppfS, sgS, declS) = core in` — **the tuple pin**, no `else` | the presented tuple must be the tuple inside the core the identity is derived from |
| 335–338 | `( out(estCh, (kT, t, aid)) \| out(aliasCh, (kT, t, core, aid)) )` | the alias report is emitted **in parallel** with the existing `estCh` report, so neither blocks the other (the S-P3 recut-1 idiom); `StandingDecide` gained a `core` parameter (325) to carry it |

**Where the pin sits, and why it matters.** After `se = noTLR` (S3),
after `withTLR` destructuring, after `fp(kT) = kfpr` (the entitled-key
test), after `kT = kX`, after the TLR signature check, after the anchor
proof — and **immediately before** `let d = lookup2(aid, lin)` (384).
Every `ABSENT` and `UNVERIFIABLE` reason code is therefore decided
*before* the pin, so no reason-code branch acquires a new precondition
and the five vocabulary witnesses keep the traces they had. Had the pin
gone earlier — say, next to the evidence checks — S3, the two
`SIGNATURE_INVALID` branches and `TEMPORAL_MISMATCH` would all have
become unreachable for a malformed core, and B9's `PATH_S3` emission
with them.

**What the pin removes.** Because it has no `else`, a presented core
that is not an `attemptCore` over `t` now produces **no report at all**.
That deletes the A7 wrapper-shaped core (`wrapCore`, §4) from the
**correct** model's standing path: it used to arrive as
`ABSENT / STANDING_EVIDENCE_MISMATCH`, and now arrives as silence. No
registered witness needed that route (see 10d), and §4's companion —
where the A7 transplant is registered and exercised — is untouched, its
`.out` byte-identical.

### 10c. SS.Q6 — results in the three correct models

| Query | DNS `.out` | repo `.out` | deg `.out` | Result |
|---|---|---|---|---|
| `Aliased` | **2007** | **2007** | **1821** | **unreachable** — `RESULT not event(Aliased(kX_3,t_3,tc,aid_2)) is true.` |
| (i), (ii)×2, (iii), N1, five witnesses, B9 | see `RESULTS.md` §A1.6, §A1.8 | | | **every RESULT line text-identical to the archived pre-addendum `.out`** |

Registered prediction: unreachable, terminating, SS.Q1 lines unchanged
(p≈0.75). That is what happened, in all three, in 0–1 s against a
30-minute box. The alias fixture did not move any SS.Q1 result — the
registered p≈0.10 divergence branch did not fire.

### 10d. What the pin did to the MISMATCH witness (the interesting part)

`ABSENT / STANDING_EVIDENCE_MISMATCH` is still reachable, but by a
different route, and the addendum predicted the route at registration.

| | Pre-addendum | Post-addendum |
|---|---|---|
| the core in the bundle | `a_4` — an **opaque adversary term**, any bitstring at all (`pre-addendum-…/ss_q1_strict_dns_compromised.out:1921`) | `attemptCore(authTuple(issuerId2, fp(pk(skH2)), ssetH, algH, verH), a_4, a_5, a_6)` — a **well-formed core carrying the presented tuple**, with adversary-chosen possession proof, attestation signature and declared time (`.out:1987`) |
| the report | `…, h(a_4)` (`.out:1923`) | `…, h(attemptCore(…))` (`.out:1989`) |
| RESULT | `is false` (reachable) at 1927 | `is false` (reachable) at 1993 |

The witness survives because `attemptCore` is a public `[data]`
constructor: the adversary can build one over the honest tuple whose
derived identity is in no lineage. The pin narrows *how* a mismatch can
be presented; it does not remove the vocabulary.

### 11. Q6-C — `ss_q6_companion_alias_unchecked.pv` (companion E: the tuple pin absent)

### 11a. Cast — differences from §10

None. Same declarations, same queries, same fixture including `mAlias`,
same judges, same envelope path. Built from the **strict
DNS-compromised** variant (the registered base) by removing exactly one
check: a body diff against the amended DNS model is **one hunk**, the
pin block.

### 11b. The standing path — difference from §10

| Line | §10 has | Q6-C has | Effect |
|---|---|---|---|
| 293–304 | `let attemptCore(=t, ppfS, sgS, declS) = core in ( let d = lookup2(aid, lin) in …` (DNS 373–387) | **no pin** — straight to `let d = lookup2(aid, lin) in …` (301) | the standing path binds the **key** to the presented tuple and never the presented tuple to the core's embedded one |

Everything else is §10's text: evidence 275–276, entitled key 286,
`kT = kX` 288, TLR signature 290, anchor 292, terminal decision
(`StandingDecide`) 245–266.

### 11c. Results (`ss_q6_companion_alias_unchecked.out`)

| Query | `.out` line | Result | The trace |
|---|---|---|---|
| `Aliased` | **2308** | **reachable — the discriminating red** | 2292: H1's honest `ShipIssuer` designates `h(core)` where `core = attemptCore(m, …)`; 2294: H1 releases its honest TLR under `skH1`, terminal `TERM_SHIPPED(h(core))`; 2296: the bundle presents **`mAlias`** with **honest** DNS and repo evidence (`skD_4`, `skR_4`), key `pk(skH1)`, **H1's core under `m`**, H1's honest TLR; 2298: `Established(pk(skH1), mAlias, h(core))`; 2302: `out(aliasCh, …)` carries the core; 2304: the judge sees `mAlias ≠ m` inside the core and fires |
| (i) unrestricted | 505 | **true** | no adversary key is needed or used |
| (ii) `pk(skH1)` / `pk(skH2)` | 519 / 530 | **true** | see 11d |
| (iii) `StandingUnentitled` | 537 | unreachable | `mAlias` names H1's own key: `fp(pk(skH1)) = kfpr` holds, so the entitled-key judge is silent |
| N1 | 836 | reachable | |
| five witnesses | 1123, 1408, 1536, 1819, 1997 | reachable | |
| B9 | 2004 | unreachable | no reason-code branch is touched |

Red on **exactly one** query, as registered. Predicted p≈0.80 for
"reachable with that shape"; the trace matches the registered shape
element for element (`RESULTS.md` §A1.5), so the p≈0.10 recut branch and
the p≈0.05 "companion cannot fail" branch did not fire.

### 11d. Why the attack succeeds, and its boundary

Nothing in this trace is dishonest except the *pairing*. The key is
honest. The core is honest. The TLR is honest. Both authority channels
published `mAlias` honestly — the alias is a real enrolment, not a
forgery; that is the point of §A5.6, which is about an issuer holding
two identities on one key, not about an attacker. What the adversary
supplies is only the **bundle**: it hands the verifier H1's core from
lineage A together with H1's tuple for identity B, and the unpinned
standing path reports `ESTABLISHED` against B for an artifact B never
issued.

**Why the per-honest-key correspondence still holds** (519, 530), and
why that is the companion's point rather than its weakness: the
correspondence asks whether the key against which `ESTABLISHED` was
computed designated that identity. It did — `pk(skH1)` signed a TLR
whose terminal disposition names `h(core)`. The correspondence is
key-level and cannot see which *tuple* the report was computed against.
That is exactly why §A5.6 needed a **new** query (`Aliased`, tuple-level)
rather than a new trace of an existing one; a family that only ever
asked the key-level question would never have found this.

**What distinguishes this red from §5's (Q3):** in Q3 the tuple is
honest and the **key** is not entitled to it, so `StandingUnentitled`
fires; here the key *is* entitled to the tuple and it is the
**identity** that is wrong, so `StandingUnentitled` is silent (537) and
only `Aliased` fires. Two different failures, two different judges.

**Boundary:** evidence only against the amended correct model, and only
that the pin is load-bearing for `Aliased`. It says nothing about
whether an issuer holding two identities on one key should keep one
terminal lineage record or two — §A5.6 explicitly leaves that open, and
a single TLR under that key may still name cores from both.

### 11e. Read and never used

As §1e, plus: the alias judge reads the core off `aliasCh` and never
acts on it — no report depends on `Aliased`. In all four models
`ppfS`/`sgS`/`declS` (the pin's other three fields) and
`ppfA`/`sgA`/`declA` (the judge's) are bound and never used; only the
tuple field is compared.

### 12. Probe status (addendum)

Unchanged from §9: no lower-ceiling reader probe has been run, now for
eight models rather than seven. No cross-family falsification review of
the pin, the alias fixture, `AliasJudge` or the companion — the archived
2026-09-06 Codex review predates them and its single-removal matrix does
not cover the pin. No author read.

### Review log (addendum)

- 2026-09-12 — §§10–12 drafted by the AI collaborator from the amended
  `.pv` files and the fresh `.out` files, after the whole-ladder re-run.
  Every `.pv` citation here was read from `grep -n` over the
  post-addendum files; every `.out` citation from `grep -n`/`awk` over
  the fresh outputs; the pre-addendum `.out` citations in §10d from
  `proverif/pre-addendum-2026-09-12/`. §§0–9 were **not** renumbered:
  they record what was checked against the text of their day, and the
  shift table in `RESULTS.md` §A1.8 is how a reader follows them
  forward. No reader probe; no cross-family review; no author read.

## Cross-family review 2026-09-12 — dispositions applied

Amend-don't-rewrite: the sentences corrected below are left as written
above; this section is the correction of record. Full dispositions and
evidence are in `RESULTS.md`, "Cross-family review 2026-09-12 —
dispositions applied"; the review itself is
`docs/reviews/2026-09-12-codex-falsification-amendment-5-checks.md`.

**1 — line 891.** It reads:

> *before* the pin, so no reason-code branch acquires a new
> precondition

That rationale is false as written. Correct text: **the aggregate
vocabulary witnesses (S1–S4 and `STANDING_EVIDENCE_MISMATCH`,
quantified over free variables) acquire no new precondition and all
stay reachable; but for an ALIAS presentation the lineage-derived
reports `SUPERSEDED`, `ISSUANCE_REFUSED` and
`STANDING_EVIDENCE_MISMATCH` do acquire the pin as a precondition** —
`falsification-2026-09-12/scratch/alias_reasons_correct.out:2015,2023`
(unreachable) against `alias_reasons_companion.out:2604,2898`
(reachable). A checked consequence of the registered placement, not a
defect.

**2 — line 899.** It reads:

> that is not an `attemptCore` over `t` now produces **no report at
> all**.

Falsified by
`falsification-2026-09-12/scratch/wrap_routes.out:1944`, where the
`noTLR` branch still reports over a `wrapCore` core. Correct text:
**produces no lineage-derived report (no mismatch, supersession or
refusal report); the no-TLR report is unaffected.**

**3 — line citations still resolve.** The three correct models' header
and pin-comment repairs of 2026-09-12 are comment-only and same line
count, and each model's `.out` is byte-identical after them
(`proverif/ladder.log`, last three lines), so every `.pv` line number
in §§0–10 of this file still resolves.
