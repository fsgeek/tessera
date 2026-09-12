# S-P2 reading aids — cast, checks, and plain-language claim for all eight models

> **STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator;
> not adopted; the commit is the author's.** This is *testimony* under
> `formal/suite/ENUMERATION.md` amendment note 5 item 2: reading aids
> for non-expert readers, reviewed by the lower-ceiling reader probe
> (not yet run for S-P2), **not a gate for exit**. Nothing here changes
> a query, a result, a header, or a `.pv` file. Every statement about a
> model cites `file:line`; every LOAD-BEARING / CARRIED label cites the
> S-P2 run that established it (`RESULTS.md` findings F2–F6, the F1
> correction note, and the diagnostics d1–d11), never an assumption
> carried from S-P3 — where an S-P3 result is the only source, the row
> says "inferred from S-P3, not ablated here". Q1d/Q1r line citations
> below are to the files as corrected 2026-09-06 (the header gained ten
> lines; bodies unchanged). Q1d, Q1r and Q2 were corrected again the
> same day after the cross-family falsification review, and a CORRECTION
> RECORD was appended **after** the process in each. Q1d was narrowed
> **within its existing line count**, so every `file:line` citation into
> it is unchanged. Q2's header is the same total length, but its
> sub-blocks shifted by one to two lines: the claim block 14–26 is now
> 14–27, "This model does not prove" 27–37 is now 28–38, "Carried …"
> 46–50 is now 48–50, and the Fixture (N2) note now begins at 62 — the
> two §1d citations below and the §9 note on the header's load-bearing
> block are corrected to the new ranges; every citation into Q2's
> **body** (72 onward) is unchanged, as are §1b's check table and §1c's
> `.out` lines. Q1r's header is also the same total length and also not
> line-for-line: its first block gained a line (16–22 → 16–23) and its
> load-bearing block lost one (24–45 → 25–45), so "the verification
> profile)." moved from 23 to 24 and the load-bearing block now runs
> 25–34, with the CORRECTION beginning at 35; this document carries no
> Q1r header line citation. All three were re-run and their `.out`
> files are byte-identical (`proverif/ladder.log`). The boundaries that
> review adds are in §1d.
>
> *(CORRECTION 2026-09-06, second pass: the paragraph above originally
> claimed all three headers were narrowed within their existing line
> count "so every `file:line` citation in this document is unchanged".
> That was false for Q2 and imprecise for Q1r; verified by diffing the
> three files against
> `proverif/falsification-2026-09-06/scratch/baseline_sp2_*.pv`.
> `RESULTS.md`'s review log carries the same correction.)*

Files this document reads (all under `formal/suite/s-p2/proverif/`;
results in the sibling `.out` files; diagnostics under `diagnostics/`):

| Short name | File | Kind |
|---|---|---|
| Q1d | `sp2_q1_strict_dns_compromised.pv` | correct, strict, DNS key leaked |
| Q1r | `sp2_q1_strict_repo_compromised.pv` | correct, strict, repo key leaked |
| Q2 | `sp2_q2_degraded_compromised.pv` | correct, degraded, sole channel leaked — **the P2 claim** |
| Q3 | `sp2_q3_companion_cardinality_ignored.pv` | broken companion: set cardinality ignored |
| Q4 | `sp2_q4_companion_slot_unbound.pv` | broken companion: slot B not bound to the named fingerprint |
| C1 | `sp2_q5_c1_fponly_frame_mh.pv` | note 2's companion as literally specified (green as registered, F4) |
| C2 | `sp2_q5_c2_fponly_frame_nomh.pv` | the red companion: both set-pins removed |
| C3 | `sp2_q5_c3_manifestposs_frame_nomh.pv` | green isolation: possession-over-manifest alone |

Library: `formal/suite/lib/tessera_theory.pvl` (cited as `lib:N`).
Property text: `docs/phase-0-prereg-amendment-1.md` P2 at lines
121–128; adversary A1.3 at lines 331–355 (item 2, "strip, reorder, or
duplicate", line 337); the waivable-subset clause at lines 319–321.
Required-set grammar: `formal/spike/first-link/DECISION.md` 364–431.

---

## 0. Typing note (once, for every model)

- **All tuples are `bitstring`.** ProVerif has no record types; a
  manifest, a frame, a channel evidence, a possession proof, a
  signature, and the "verified keys" summary are all `bitstring`.
  **Shape lives in construction and pattern matches, never in
  declarations.** A manifest is a manifest because it was built with
  `authTuple(...)` (`lib:164`; Q2 237–238) and later matched with
  `let authTuple(id, kfprA, =signers0, alg, ver) = t in` (Q2 163).
- **The signer set is a shape, not a list.** `signers0` (a constant,
  Q2 82) means "no additional signer"; `signers1(fpB)` (Q2 83) means
  "one additional signer, fingerprint `fpB`". The required set of a
  manifest is `{kfp} ∪ sset` — the tuple's second field plus whatever
  the third field names. There is no `signers2`: the bound is two
  signers, and that bound is a stated boundary of every result.
- **`verified1(kA)` / `verified2(kA, kB)`** (Q2 85–86) are the
  verifier's own report of *which keys it verified signatures under*.
  They exist only so a judge can compare that report with the set the
  manifest names.
- **`=x` in a pattern means "must equal x"; a bare name means "read
  this".** `let framed(ota, =alg, =id, =fp(kA), mha, cva, pla) = fa`
  (Q2 167) checks three fields and reads four. `let authTuple(id,
  kfprA, =signers0, alg, ver) = t` (Q2 163) *checks* that the signed
  set names no additional signer; Q3's `let authTuple(id, kfprA, ss,
  alg, ver) = t` (Q3 128) merely *reads* it — that one character
  class is the whole difference between the correct model and the
  stripping companion.
- **`[data]` constructors** (`framed`, `framedNoMh`, `authTuple`,
  `signers1`, `verified1/2`) are transparent: the adversary builds and
  takes them apart. `sign`, `h`, `fp` are not (`lib:97–131`).
- **`!P`** is unboundedly many copies of `P`. **`free x [private]`**
  is a value the adversary does not know — here the three honest
  signer keys (Q2 89–91), private so the registered queries can name
  the fixture manifests literally (Q2 126–129).
- **Two idealizations carry results here, and are declared in the
  library, not the models:** `fp` injective (`lib:107–117`) and `h`
  injective (`lib:120–131`). A third — signature unforgeability, the
  Dolev–Yao rule at `lib:100–104` — carries exactly one thing in this
  ladder (possession over the manifest, C3), and the DSKS extension
  `dsks` (`lib:99`, 103–104) appears in **no** S-P2 derivation.

## 0.1 Shared cast — the library terms every model uses

| Name | What it is in the design (plain words) | Declared (lib) | Used in the models |
|---|---|---|---|
| `c` | the public network; the adversary sees and injects everything on it | 77 | every `in(c, …)`/`out(c, …)` |
| `skey`, `pkey`, `pk` | private key, public key, the map between them | 95–97 | every key |
| `sign(m, k)`, `checksign(s, pk)` | deterministic signature with message recovery | 98, 100–104 | evidence, possession, attestation checks |
| `dsks(s, r)` | the A1.3 item 3 capability: a fresh held key that verifies one seen signature | 99, 103–104 | adversary only; **appears in no S-P2 derivation** (RESULTS F4, F5) |
| `fp(pk)` | key fingerprint, idealized injective | 117 | manifests, frames, slot checks, judges |
| `h(x)` | hash, idealized injective | 131 | evidence digest and the frame's manifest hash |
| `STMT_DIGEST`, `POSS`, `BYTES` | domain tags: authority evidence (digest form), manifest self-signature, attestation over framed bytes | 139–141 | Q2 136, 149, 155, 161, 165–166 |
| `OT_ATTEST` | object type "base attestation" (D-5) | 150 | the honest frame's first field, Q2 152 |
| `authTuple(id, kfp, sset, alg, ver)` | **the manifest as modeled** — issuer identity, first required signer's fingerprint, remaining required signers, algorithm, version | 164 | `m1`, `m2` (Q2 237–238); matched at Q2 163, 181, 204 |
| `issuerId`, `algH`, `verH` | public honest fixture values | 169, 171–172 | `m1`, `m2`, frames |
| `ssetH`, `fbH`, `STMT_DIRECT`, `TLR`, `REFUSAL`, other `OT_*` | library terms **used by no S-P2 model** | 138, 143–157, 170, 173 | — |
| `AuthorityPublishedDNS/Repo`, `IssuerPossession`, `IssuerSigned` | library events, fired and **never queried** here | 179–182 | Q2 135, 148, 153 |
| `Accept(evD, evR, t, k, fb)` | strict two-channel acceptance | 183 | Q1d/Q1r n = 1 branch only (Q1d 148) |

## 0.2 The judge idiom (shared by all eight)

Registered in `PREDICTIONS.md` 237–282 before any run. Honest parties
report on private channels the adversary cannot see; the verifier
reports what it accepted; a judge pairs the two and fires an event.
Four judges, three of them S-P2's and one S-P3's carried verbatim:

- **Registrar → `honestSetCh`** (Q2 139–140): "this manifest is
  honest". **Signer → `honestKeyCh`** (Q2 150): "this key belongs to
  this one manifest". **Signer → `honestCh`** (Q2 154): "this key
  framed these bytes" (S-P3's report).
- **Verifier → `setCh`** (Q2 170, 193): "I accepted tuple `t` having
  verified these keys". **Verifier → `slotCh`** (Q2 171, 194): one
  report per slot, "for tuple `t`, the slot the set names as `fpS` was
  satisfied by key `kUsed`". **Verifier → `acceptCh`** (Q2 172, 195):
  S-P3's report.
- **SetJudge** (Q2 201–214): honest manifest + acceptance of the same
  tuple. Fires `HonestComplete` only when the verified keys match the
  named set fingerprint by fingerprint (207, 214) — the N1 witness, one
  per set size, required reachable; fires `Stripped` when a two-signer
  manifest was accepted with one verified key (209–210).
- **MemberJudge** (Q2 220–226): honest (key, manifest) + slot report.
  Same tuple, this key's slot, another key used → `SignerForged`
  (224). Different tuple, this honest key used → `SetAltered` (226).
- **Judge** (Q2 229–233, S-P3 verbatim): honest bytes accepted under
  their own key → `HonestAccepted`; under another → `Reattributed`.

Two things to hold onto: (1) every judge compares **keys and
manifests**, never who authored the bytes — remove the attestation
signature check entirely and no judge notices (RESULTS F6, d4); (2)
the judges are keyed on honest manifests and honest keys, so a
manifest the adversary wrote for keys it holds, accepted with all its
own signers present, fires nothing — impersonation, out of scope by
registration (`PREDICTIONS.md` 279–282; A4 §A4.6).

---

## 1. Q2 — `sp2_q2_degraded_compromised.pv` (the P2 claim)

The other seven are this file with named differences, so it is read
first and in full.

### 1a. Cast

| Name | What it is in the design | Built | Consumed |
|---|---|---|---|
| `skS` | the **sole** authority channel's signing key — **leaked** | 236 | 136 (signs evidence); **242 `out(c, skS)`**; 243, 247 |
| `skA1` | M1's only required signer's key (private) | 89 | 237 (fingerprint into M1); 239 (public key published); 245 |
| `skA2`, `skB2` | M2's two required signers' keys (private) | 90–91 | 238; 239; 246 |
| `m1` | **the one-signer manifest**: `authTuple(issuerId, fp(pk(skA1)), signers0, algH, verH)` | 237 | 240 (published); 243 (channel signs it); 244 (registered honest); 245 → 149 (self-signed), 152 (hashed into the frame) |
| `m2` | **the two-signer manifest**: `authTuple(issuerId2, fp(pk(skA2)), signers1(fp(pk(skB2))), algH, verH)` | 238 | 240; 243; 244; 246 → 149, 152 |
| `signers0`, `signers1(fp)` | the set shape: no / one additional signer | 82–83 | 163, 181 (verifier demands the shape); 205, 212 (judge reads it); 237–238 |
| `verified1(k)`, `verified2(kA, kB)` | the verifier's report of which keys it verified under | 85–86 | built 170, 193; read 206, 209, 213 |
| `payload` | **the thing attested**; adversary-chosen | read 147 | 152 |
| `framed(...)` | the P3 field list as a transparent 7-tuple, copied verbatim from S-P3 | 76 | built 152; matched 167, 190 |
| `fb` (signer) | the framed bytes | 152 | 153, 154 (report), 155 (signed) |
| `ppf` | possession proof, **the manifest self-signature** `sign((POSS, m), sk)` (D-3) | 149 | 151 (published); checked 165, 184–185 |
| `ev` | the sole channel's evidence `sign((STMT_DIGEST, h(t)), skS)` | 136 | read 159, 176; checked 161, 179 |
| `canonVerH`, `issuerId2` | fixture values | 78–79 | 152; 238, 246 |
| `t` | the manifest the package *presents* | read 159, 176 | 161/179 (evidence over `h(t)`), 163/181 (shape), 165/184–185 (possession over `t`), 168/189/191 (frame hash), reports |
| `id`, `kfprA`, `kfprB`, `alg`, `ver` | fields of `t` | 163, 181 | `kfprA` 164/182, 171/194; `kfprB` 183, 194; `id` 167/188/190, 172/195; `alg` 167/188/190; **`ver` never used** |
| `kA`, `kB` | the keys the package presents for slot A / slot B | read 160, 177 | slot match 164/182–183; possession 165/184–185; signature 166/186–187; frame 167/188/190; reports |
| `ota`, `otb`, `mha`, `mhb`, `cva`, `cvb`, `pla`, `plb` | frame fields read at the verifier | 167, 188, 190 | `mha`/`mhb` 168/189/191; **`ota`, `otb`, `cva`, `cvb`, `pla`, `plb` never used** |
| `honestSetCh`, `honestKeyCh`, `setCh`, `slotCh`, `honestCh`, `acceptCh` | private judge channels (§0.2) | 94–99 | out 140/150/170,193/171,194/154/172,195; in 202/221/203/222/230/231 |
| `Stripped`, `SignerForged`, `SetAltered` | the three P2 threats (§0.2) | 101–103 | fired 210, 224, 226; queried 114–121 |
| `HonestComplete`, `HonestAccepted` | the N1 witnesses | 104, 106 | fired 207/214, 232; queried 126–129, 131–132 |
| `Reattributed` | S-P3's threat, carried | 105 | fired 233; queried 123–124 |
| `Accept1S`, `Accept2S` | acceptance, one per branch (not queried; the witnesses are judge-emitted) | 107–110 | fired 169, 192 |
| `AuthorityS`, `Registrar`, `Signer`, `Verifier1S`, `Verifier2S`, `SetJudge`, `MemberJudge`, `Judge` | the roles | 134–136, 139–140, 146–155, 158–172, 175–195, 201–214, 220–226, 229–233 | 243–248 |

### 1b. The verifier's checks — n = 1 branch (158–172) and n = 2 branch (175–195)

Status column sources: **Q3** (`Stripped` red when the sset pattern is
removed), **Q4** and **d6** (`SignerForged` red when a slot match is
removed), **C1/C2/C3** (the two set-pins), **d2/d3/d4** (removed with
no change), RESULTS F2–F6. Strict-mode sources (§2, added 2026-09-06):
**d7** (strict + Q3 mutation, `Stripped` red), **d8** (strict + Q4
mutation, `SignerForged` red), **d9** (strict + C2 mutation,
`SetAltered` green), **d10** (strict, frame `=fp` unbound, slot match
kept, green), **d11** (d10 with the slot matches removed,
`Reattributed` and `SignerForged` red); RESULTS F1 correction note.

| Line (n=1 / n=2) | Check | Plain meaning | Status |
|---|---|---|---|
| 161 / 179 | `let (=STMT_DIGEST, =h(t)) = checksign(ev, pkS)` | the sole authority evidence endorses exactly this manifest | **CARRIED — inert by construction** (d2: removed, every result identical; the channel key is public at 242) |
| 163 / 181 | `let authTuple(id, kfprA, =signers0, …) = t` / `… signers1(kfprB) …` | the **signed** tuple's set must have exactly the shape this branch handles; the second slot's fingerprint is read from the signed set, never from the package | **LOAD-BEARING for `Stripped`** (Q3: pattern → variable, red; F2) |
| 164 / 182 | `if fp(kA) = kfprA` | slot A's key is the one the set names | **LOAD-BEARING for `SignerForged`** (d6: removed, red at slot A; F5) |
| — / 183 | `if fp(kB) = kfprB` | slot B's key is the one the set names | **LOAD-BEARING for `SignerForged`** (Q4: removed, red; F5). Also the check that closes *duplicate* (same honest key in both slots) — by inspection, not by a run (F8a) |
| 165 / 184–185 | `let (=POSS, =t) = checksign(ppfX, kX)` | each presented key has self-signed *this* manifest | **LOAD-BEARING for `SetAltered`, redundantly with 168/189/191** (C3: alone, green; C1: absent with the hash kept, green; C2: both absent, red; F4) |
| 166 / 186–187 | `let (=BYTES, =fX) = checksign(sgX, kX)` | each presented key signed exactly its presented framed bytes | **CARRIED — unexercised by every S-P2 judge** (d4: removed on both slots, every result identical; authorship is S-P1's; F6) |
| 167 / 188, 190 | `let framed(ot, =alg, =id, =fp(kX), mh, cv, pl) = fX` | the signed bytes name this algorithm, identity and fingerprint | `=fp(kX)`: **LOAD-BEARING for `Reattributed` JOINTLY with the slot match (164 / 182–183)** — *corrected 2026-09-06, cross-family review items 4 and 17*: its own single removal is green in Q1d, Q1r and Q2 (d10; matrix `falsification-2026-09-06/scratch/dependencies.tsv:18,42,46` for Q1d and `:107,128,132` for Q2), and only both gone is red (d11); it carries `Reattributed` alone where the manifest hash is absent (C3's fingerprint ablations, `tsv:147,167,170`, red). Read as *individually necessary* the old label overstated (d6 and Q4 leave it unreachable with the slot match gone; F5). `=alg`, `=id`: **CARRIED** (d3: unbound, every result identical; F6). `ot`, `cv`, `pl`: read, never checked (Q4's trace has them adversary-chosen, F5) |
| 168 / 189, 191 | `if mh = h(t)` | the signed bytes commit to this manifest | **LOAD-BEARING for `SetAltered`, redundantly with 165/184–185** (C1: alone, green; C3: absent with possession kept, green; C2: both absent, red; F4) |
| 169 / 192 | `event Accept1S / Accept2S` | acceptance | not queried; the N1 witnesses are judge-emitted |
| 170–172 / 193–195 | parallel reports | S-P3 recut-1 idiom | encoding |

### 1c. Results (`.out`)

| Query | `.out` line | Result | Meaning |
|---|---|---|---|
| `Stripped` | 354 | unreachable | no honest manifest accepted with fewer signers than it names |
| `SignerForged` | 360 | unreachable | no slot the set assigns to an honest signer satisfied by another key |
| `SetAltered` | 366 | unreachable | no honest key accepted as a signer of a manifest it never signed — **under the fixture rule one key, one manifest** (cross-family review item 13): the judge compares the accepted manifest with the one honest record for that key, so it reads as “never signed” only because each honest key signs exactly one manifest here |
| `Reattributed` | 372 | unreachable | S-P3's binding not weakened |
| `HonestComplete(M1, verified1(k1))` | 536 | **reachable** | the one-signer honest flow is accepted (trace 378–535) |
| `HonestComplete(M2, verified2(k1, k2))` | 756 | **reachable** | the two-signer honest flow is accepted, both keys their own (trace 542–755) |
| `HonestAccepted` | 987 | reachable | the carried S-P3 judge is live |

### 1d. Claim, adversary, boundary (plain language)

**Claim (header 14–27; RESULTS F1).** A relying party who runs these
checks, with only one authority channel available and that channel in
the adversary's hands, will never accept a package for an honest
two-signer manifest that carries only one of its signatures; will never
accept, in a slot the signed manifest assigns to an honest signer, a
signature by any other key; and will never accept an honest signer's
key as vouching for a manifest that signer never self-signed — so a
sole-channel adversary cannot shrink the required set around an honest
key. That third sentence holds **under the fixture rule one key, one
manifest** (cross-family review item 13): the `SetAltered` judge reports
difference from the one honest (key, manifest) record it holds, so read
without that rule it says “different from this record”, not “never
signed” — the judge is instrumentation, not a verifier check, and no
verifier line depends on it. "Issued with one" (M1) and "issued with two" (M2) are both
accepted when complete, and are told apart because the set is read from
the signed manifest, not from what the package presents. For sets of at
most two signers.

**Adversary (A1.3 331–355; fixture 239–242).** Sees everything on `c`;
holds the only authority key (242) and so can make the channel endorse
any manifest; chooses every payload the honest signers sign (147);
builds manifests, set shapes and frames freely (`[data]`); has the
DSKS capability (`lib:99–104`) and every key it uses. Does **not** hold
`skA1`, `skA2`, `skB2`.

**Why the attacks fail.** *Stripping:* the n = 1 branch demands
`signers0` in the signed tuple (163); M2's tuple has `signers1(…)`, so
A2's honest sub-package is refused there, and the n = 2 branch demands a
second signature under the key M2 names (181–187). *Substitution:* the
slot match (164, 182–183) forces `kX` to the named key (`fp`
injective), and the frame's `=fp(kX)` (167, 188, 190) does the same for
the bytes. *Set-shrinking:* a shrunk tuple `M2'` hashes differently from
M2 (`h` injective), so A2's honest frame fails 168; and A2 never
self-signed `M2'`, so 165 fails too — either alone suffices (F4).
*Re-attribution:* the frame's own fingerprint (S-P3 F5). What did
**not** matter: the evidence check (161/179), the identity and
algorithm conjuncts, and the attestation-signature check itself (F6).

**Boundary (header 28–38; RESULTS "What S-P2 does not discharge").**
Sets larger than two; ordering, uniqueness and bounds of the set
encoding (P8); the `INVALID` verdict (P4's model, cross-formalism); the
`VALID_DEGRADED` waiver of a subset (not modeled); impersonation with
the adversary's own key, own manifest, own bytes (reachable, the
registered cost, A4 §A4.6); authorship — a fabricated signature under
the honest *named* key passes every judge here (F6; S-P1); the
verification profile. `fp` and `h` are collision-free by fiat.

**Boundaries the cross-family falsification review adds (2026-09-06;
`docs/reviews/2026-09-06-codex-suite-falsification-s-p1-s-p2-s-p7-s-standing.md`,
item numbers as in its "Consolidated findings" section; the reviewer's
fixtures and matrix are archived under
`proverif/falsification-2026-09-06/`).** These are boundary statements,
not new results; no query, result or `.pv` body changed.

- **Item 1 — signature-set operations at n ≤ 2 only.** A1.3 item 2's
  strip / reorder / duplicate are representable here only inside the
  bounded family `signers0` / `signers1(fp)`, one verifier branch per
  arity; the signer *set* is S-P2's subject (S-P1, S-P7 and S-STANDING
  have one signature slot each and cannot express it at all). The
  reorder run (`scratch/a_reordered_keys.pv`, unreachable) swaps
  positional package slots; it says nothing about equivalence of
  reordered set *encodings*.
- **Item 2 — byte-encoding attacks are unrepresentable.** Non-canonical
  encodings of the same abstract required set, hash-input ambiguity and
  cross-kind parse confusion have no expression: term equality stands
  in for byte equality, and distinct constructors never confuse
  (`lib:119–131`). This is a **coverage failure, not an unreachable
  attack** — rejecting them has no established RESULT here. Already
  registered: P8's injectivity obligation and the library's `h` / `fp`
  idealization (Layer 2 residual; consumed ledger entry 3).
- **Item 3 — no verdict values, waiver records or policy inputs.** A
  failed check stops a process; nothing here establishes that a
  stripped package yields `INVALID` rather than some other non-valid
  outcome, and no waiver record or waiver-membership check exists.
  Assigned: P4's partition and the `Accept` ↔ P4 cross-formalism join
  (author ruling 2026-08-29; coverage map; consumed ledger entry 4).
- **Item 6 — the witnesses are existential.** Both `HonestComplete`
  witnesses and `HonestAccepted` are reachable with concrete traces
  (§1c), but reachability for one honest key on one branch does not
  establish it per branch or per key. N1 is a **vacuity guard, not
  coverage**.
- **Item 14 — the attestation-signature check is inert for all four
  registered queries**, not only for their authorship content: single
  removal of the check, its `BYTES` tag, or its signature-to-frame
  equality (166 / 186–187; `tsv:102–104,120–125` — the review cites
  `:102–104,122–127`; the attestation rows for the n = 2 branch are in
  fact `:120–125`, since 126–127 are the frame `alg`/`id` ablations,
  item 4's separate row) leaves every result
  identical, as d4 already showed. The judges compare keys, manifests
  and frames and never establish who signed the bytes, so the check is
  **carried for S-P1's** correspondence (S-P3 F7; S-P1's ledger).
- **Item 15 — object type is carried, never exercised.** The reviewer's
  `a_wrapper_replay` adds an honest `OT_WRAPPER`-signing producer over
  the shared frame and presents its output to this verifier: it is
  accepted, with all four registered queries green
  (`scratch/a_wrapper_replay.pv`; RESULT line at `.out:588`, quoted in
  `CODEX-REVIEW.md` — the reviewer's `.out` files are regenerable, not
  archived, per `ARCHIVE-NOTE.md`). S-P7's type judge owns this;
  §1e already lists `ota` / `otb` as read and never used.
- **Item 16 — a semantically empty required set is unrepresentable.**
  The grammar has no n = 0 shape (`signers0` *is* one signer), so
  rejection of an empty required set has no established RESULT here.
  Already registered: A3 §A3.2 item 1's never-zero floor (also P10
  probe O1), and "What S-P2 does not discharge" in `RESULTS.md`.

### 1e. Read and never used

`ver` (163, 181); `ota`, `otb`, `cva`, `cvb`, `pla`, `plb` (167, 188,
190); the S-P3 judge's `id` (231); the SetJudge's `idJ`, `algJ`, `verJ`
(204) and `kA`/`kB` inside the `Stripped` arm (209). Library events
fired and never queried (135, 148, 153). Library terms unused: §0.1.

---

## 2. Q1d — `sp2_q1_strict_dns_compromised.pv` (strict, DNS key leaked)

Q2 with two authority channels. Differences: `AuthorityDNS` /
`AuthorityRepo` (107–113), each firing its library event and signing
`h(t)`; both evidences checked in each branch (Verifier1 139–140,
Verifier2 159–160); the n = 1 branch fires the library's `Accept`
(148), the n = 2 branch a model-local `Accept2` (82, 173); `skD`,
`skR` created at 217, **`skD` leaked at 223**; both channels publish
both manifests (224–225). Every other line is Q2's, shifted: queries
87–105; Registrar 116–117; Signer 123–132; Verifier1 135–152; Verifier2
154–180; SetJudge 182–195; MemberJudge 201–207; Judge 210–214. (The
header, lines 24–39, was corrected 2026-09-06; see the last paragraph.)

**Checks.** As §1b with these additions: 140 / 160 (honest repository
evidence) pins `t` to an honestly published manifest before the set is
inspected. What that pin closes was **ablated in strict mode on
2026-09-06** (d7–d11, Q1d as base; `RESULTS.md` F1 correction note):
it closes `SetAltered` on its own (d9: both set-pins removed, green);
it does **not** close `Stripped` or `SignerForged` (d7/d8: the Q3/Q4
mutations, red, no `dsks` step) — those packages present the honest
tuple M2, which this very check endorses; it closes `Reattributed`
only through the slot match `fp(kX) = kfprX` against the pinned
tuple's `kfpr` (d10: frame `=fp` unbound, green; d11: slot matches
removed too, red). 139 / 159 (the leaked DNS key's evidence) is inert
by the same reasoning as Q2's 161/179. So every LOAD-BEARING label in
§1b for `Stripped` and `SignerForged` holds unchanged in strict mode
(d7/d8 are the strict re-severings); for `SetAltered` the two set-pins
are redundant with the channel pin here (d9); for `Reattributed` the
frame's `=fp` is redundant with the slot match here (d10). The
repo-leaked variant (§3) was not re-ablated.

**Results.** `.out` 386, 392, 398, 404 unreachable; 580, 812 reachable
(N1 ×2); 1055 reachable. Re-run 2026-09-06 after the header correction:
byte-identical.

**Claim / adversary / boundary.** As §1d, with: two channels required
and the DNS one fully compromised; the honest repository channel signs
only `h(m1)` and `h(m2)` (225), so the presented manifest is one of the
two honest ones; the channel therefore closes set-shrinking
(`SetAltered`) on its own, and re-attribution together with the slot
match, but stripping and slot substitution present the honest manifest
and are stopped only by the same sset pattern and slot match as in Q2
(strict ablations d7/d8). Not the degraded case; that is Q2.

**Header correction (2026-09-06).** The original header (lines 24–29)
said the pin closed `Stripped`/`SetAltered` "by the channel alone" —
false for `Stripped`, as d7 shows; the skeptic review caught it and the
header now says what d7–d11 show. Comment-only change; the model body
is unchanged and the `.out` is byte-identical.

**Second header correction (2026-09-06, cross-family review items 2, 4,
5, 13, 15, 17).** Same day, after the falsification review: the two
set-pins and the frame's fingerprint, listed as load-bearing, now read
**jointly** load-bearing, because each single removal is green
(`tsv:19,43,47` and `10,28,31` for the pins, `18,42,46` for the
fingerprint); the honest channel's own evidence check (140 / 160) is
**individually inert** for these queries (`tsv:5–7,23–25`, all green)
and is recorded as defence in depth — sufficient for `SetAltered` alone
(d9), necessary for nothing while the set-pins stand, which is the
shape item 5 records in S-P1 and S-P7; "no set-shrinking around an
honest key" is read under Q2's one-key/one-manifest qualifier (item 13);
object type stays carried (item 15) and byte-encoding attacks stay
unrepresentable (item 2). Comment-only again: the header was narrowed
within its existing line count and the record appended after the
process, so the line citations above are unchanged, and the re-run
`.out` is byte-identical (`ladder.log`).

## 3. Q1r — `sp2_q1_strict_repo_compromised.pv`

Line for line Q1d except the header's variant name and lines 222–223:
`out(c, skR)` — the **repository** key is leaked and DNS is honest.
Exchange "DNS" and "repository" throughout §2; the honest evidence
check is then 139 / 159. The strict ablations d7–d11 use Q1d as base
and were not repeated on this variant. Results identical: 386, 392, 398, 404
unreachable; 580, 812, 1055 reachable. Running both variants is the
spike rule that a generic single channel does not represent both
(`PREDICTIONS.md` 172–174).

---

## 4. Q3 — `sp2_q3_companion_cardinality_ignored.pv` (broken: cardinality ignored)

**The one changed line.** Q2's 163 `let authTuple(id, kfprA,
=signers0, alg, ver) = t` becomes Q3's 128 `let authTuple(id, kfprA,
ss, alg, ver) = t` — the set is read into `ss` and never looked at
(comment 125–127). This is S-P3 Q2's verifier line 102, character for
character. The n = 2 branch (140–163) is unchanged. Everything else:
queries 77–95; AuthorityS 97–99; Registrar 102–103; Signer 109–118;
Verifier1S 121–138; SetJudge 166–179; MemberJudge 185–191; Judge
194–198; process 200–213, leak 207.

**Results (`.out`).** `Stripped` **reachable** at 520 (derivation 354–
468, trace 472–519); `SignerForged` 526, `SetAltered` 532,
`Reattributed` 538 unreachable; `HonestComplete` ×2 reachable 702,
922; `HonestAccepted` 1153.

**Why it succeeds (trace, `.out` 472–519).** The adversary feeds A2 a
payload (in copy `a_3`), collects A2's honest possession over M2 and
honest signature over A2's honest frame, and hands the n = 1 branch
M2's own tuple, the channel's evidence for M2, `pk(skA2)`, and A2's
proof, signature and frame. Every retained check passes — these are
honest values for M2 — and the branch, no longer asking whether M2
names a second signer, reports `verified1(pk(skA2))` for M2. The
SetJudge pairs that with the registrar's M2 and fires `Stripped` (Q3
175). **No cryptographic step**: nothing forged, no `dsks`; the
leaked key is not needed (the honest channel emits the same evidence).
This is A1.3 item 2's "strip" exactly, and P2's "issued with two, one
stripped" being mistaken for "issued with one".

**Why only `Stripped` goes red.** Slot match, possession over the
manifest, manifest hash and the frame's fingerprint are all retained,
so no key is substituted (`SignerForged`), no tuple is altered
(`SetAltered`), and no bytes move to another key (`Reattributed`).

**Boundary.** Proves nothing about P2; evidence that the checking
arrangement detects stripping, and the record that S-P3's verifier
shape does not (F2).

---

## 5. Q4 — `sp2_q4_companion_slot_unbound.pv` (broken: slot B unbound)

**The one removed line.** Q2's 183 `if fp(kB) = kfprB then` is gone
from the n = 2 branch (comment 145–147); the possession check under
`kB` (149), the signature check (151) and the frame's `=fp(kB)` (154)
stay. Everything else as Q2: queries 76–94; Verifier1S 120–135;
Verifier2S 137–162; SetJudge 165–178; MemberJudge 184–190; Judge
193–197; process 199–212, leak 206.

**Results.** `SignerForged` **reachable** at 601 (derivation 360–539,
trace 543–600); `Stripped` 353, `SetAltered` 608, `Reattributed` 615
unreachable; witnesses 780, 1001, 1233 reachable.

**Why it succeeds (trace 543–600).** The adversary presents M2 with
A2's honest material in slot A and, in slot B, **its own key `pk(k)`**,
its own self-signature over M2 under `k`, and its own frame
`framed(otb_1, algH, issuerId2, fp(pk(k)), h(M2), cvb_1, plb_1)`
signed by `k` — object type and canonicalization version chosen freely
(`otb_1`, `cvb_1`). Without the slot match nothing compares `fp(pk(k))`
with the fingerprint M2 names for slot B; the slot report says "M2's
B-slot, named `fp(pk(skB2))`, satisfied by `pk(k)`", and the
MemberJudge fires (188). **No `dsks` step**: the derived-key route over
B2's honest frame is closed by the retained `=fp(kB)` at 154, as the
plan traced — a derived key has a different fingerprint.

**Why only `SignerForged` goes red.** The arity is still read from the
signed set (`Stripped`); the hash and possession pins hold
(`SetAltered`); the frame's own fingerprint holds (`Reattributed`).

**Boundary.** Proves nothing about P2; shows the per-slot fingerprint
match is what membership rests on. The same removal at slot A behaves
identically (d6). A fabricated signature accepted under the *honest*
named key would pass this judge (`kUsed = kH`): authorship, S-P1 (F6).

---

## 6. Q5-C1 — `sp2_q5_c1_fponly_frame_mh.pv` (note 2's companion as literally specified — green)

**Two changed lines, one kept.** Signers produce fingerprint-only
possession `sign((POSS, fp(pk(sk))), sk)` (112, the spike's encoding,
library D-3's named broken form); verifiers check possession over the
fingerprint only (128; 147–148). The frame still carries the manifest
hash and the verifier still checks it (130–131; 151–154). Layout:
Verifier1S 121–136; Verifier2S 138–162; judges 164–196; leak 205.

**Results.** All four unreachable (354, 360, 366, 372); witnesses
reachable (536, 756, 987). **Green as registered** (`PREDICTIONS.md`
395–407): a companion that cannot fail.

**Why the attack fails here.** A2's honest frame carries `h(M2)`; the
shrunk tuple presented to the n = 1 branch is not M2, so `mha = h(t)`
at 131 fails (`h` injective). The possession encoding never gets to
matter. This is the S-P3 F3 redundancy seen from P2's side: two
independent pins, and note 2 — drafted before the frame carried a
manifest hash — removed only one.

**Boundary.** Green here is evidence about the checking arrangement's
redundancy, not about P2 (RESULTS F4; `ENUMERATION.md` note 6 item 2).

## 7. Q5-C2 — `sp2_q5_c2_fponly_frame_nomh.pv` (the red companion)

**C1 plus the hash removed.** The frame is `framedNoMh(objType, alg,
issuerId, kfp, canonVer, payload)` (44–45; built 120); the verifiers
match it with no hash check (135; 155–156) and still check `=alg`,
`=id`, `=fp(kX)`. Possession is fingerprint-only as in C1 (117; 133;
151–152). Layout: Verifier1S 126–141; Verifier2S 142–165; judges
166–198; leak 207.

**Results.** `SetAltered` **reachable** at 535 (derivation 363–473,
trace 477–534); `Stripped` 349, `SignerForged` 356, `Reattributed`
542 unreachable; witnesses 706, 925, 1100 reachable.

**Why it succeeds (trace 477–534).** The adversary writes a new tuple
`authTuple(issuerId2, fp(pk(skB2)), signers0, algH, a_6)` — **B2 alone,
A2 dropped, the version replaced** — signs its digest with the leaked
channel key, and hands the n = 1 branch that tuple, that evidence,
`pk(skB2)`, B2's honest fingerprint-only possession (which says nothing
about any tuple), B2's honest signature and B2's honest hash-free frame.
Every check passes: the slot names `fp(pk(skB2))`; the possession
verifies under `pk(skB2)` and names its fingerprint; the frame names
`algH`, `issuerId2`, `fp(pk(skB2))`. The slot report says "this new
tuple, satisfied by `pk(skB2)`"; the MemberJudge pairs it with B2's
honest report "(pk(skB2), M2)", sees a different tuple, and fires
(191). This is the guide's M7a mechanized, and the exhibited instance
is a **different member and an extra altered field** from the plan's
named one (F3); the plan's instance is reachable too (d5).

**Why only `SetAltered` goes red.** The forged tuple is not an honest
manifest, so the SetJudge never pairs it (`Stripped`); the slot match
stands (`SignerForged`); the frame still names `fp(kX)`
(`Reattributed`).

**Boundary.** Proves nothing about P2; exhibits the relying-party cost
of the spike's possession encoding without the frame's hash: a
sole-channel adversary can alter the signer set and the version around
an honest key. Algorithm and identity are *still* pinned here by the
frame's `=alg`, `=id` (F3).

## 8. Q5-C3 — `sp2_q5_c3_manifestposs_frame_nomh.pv` (green isolation)

**Hash removed, possession over the manifest kept.** `framedNoMh`
(41–42; built 117; matched 132, 152–153) with possession
`sign((POSS, m), sk)` (114) checked over the presented tuple (130;
148–149). Layout: Verifier1S 123–138; Verifier2S 139–162; judges
163–195; leak 204.

**Results.** All four unreachable (349, 356, 363, 370); witnesses
reachable (534, 753, 983). Green as registered.

**Why the attack fails here.** The C2 package needs B2's (or A2's)
signature over `(POSS, M2'')` for a tuple the honest key never saw;
the honest signers self-sign only their own manifest (114 with `m`
bound at 199–200), and `dsks` derives keys for signatures already
seen, never new signatures (`lib:100–104`). So 130 fails for every
shrunk tuple, hash or no hash. This is the guide's M7b: possession over
the manifest is individually sufficient against set-shrinking.

**Boundary.** An isolation configuration, not the P2 model; together
with C1 and C2 it is the dependency statement in RESULTS F4. The
result here rests on signature unforgeability (Layer 2), where C1's
rests on `h` injectivity.

---

## 9. Observations about the testimony (not verdicts on the proofs)

- Q2's header (lines 38–45 as written, now 39–47) predicted its
  load-bearing checks before the companions ran; the companions and
  d2–d6 confirmed every assignment. *(CORRECTION 2026-09-06,
  cross-family review, second pass: this bullet used to end "the
  header's phrase 'confirmed or corrected in RESULTS.md' is now
  'confirmed' (F2–F6); the header text was not edited." The header text
  **was** edited later the same day — the phrase now reads "confirmed:
  RESULTS.md F2–F6; cross-family single-removal matrix, see footer",
  and item 4 changed "each individually" to **JOINTLY**. The block also
  moved from 38–45 to 39–47.)*
- Q2's header says the version field is unexercised only by
  implication ("the S-P3 F7 fields"); RESULTS F3 makes it explicit that
  `ver` is not a frame field and is alterable in C2. A reader of the
  code sees this at Q2 163 (`ver` read, never used) and C2 `.out` 363
  (`ver_2` adversary-chosen).
- The C2 header (lines 15–22) narrates the attack with A2 kept, as the
  plan did; the tool exhibited B2 kept. Both are reachable (d5). The
  header was left as written; F3 is the correction of record.
- The unregistered `HonestAccepted` query (Q2 130–132) is labelled in
  the file as "not registered"; RESULTS "Prediction divergences" item 2
  says why it is there.
- The Q1 headers (both variants) originally asserted a mechanism no run
  had tested and one run refutes ("Stripped/SetAltered are closed by the
  channel alone"). A header is testimony too, and this one was wrong in
  the direction that matters to a relying party (it made strict mode
  sound as if it needed less of the verifier than it does). Corrected
  2026-09-06 from d7–d11; the .pv change is comment-only. The general
  lesson is the one S-P3 F7 already states — a header names what its
  queries discharge, and a mechanism claim needs its ablation.

---

## 10. Post-freeze addendum 1 — Q6 and Q6-C (common attested content), 2026-09-12

> **STATUS: PROPOSED — 2026-09-12 — produced by the AI collaborator;
> not adopted; the commit is the author's.** Appended, not edited in:
> no sentence above this line is changed. This section reads the
> post-freeze addendum registered at the end of `PREDICTIONS.md`
> (Amendment 5 §A5.4; ROUTED C8, ADOPTED (author) reading (a)) and the
> run recorded in `RESULTS.md`, "Post-freeze addendum 1 — results,
> 2026-09-12".
>
> **Line citations above are now stale for Q2 and must be shifted.**
> Unlike the 2026-09-06 corrections, this one changed the Q2 model's
> **body**, so its `.pv` grew from 291 to 342 lines and its `.out` line
> numbers moved. Q2 `.pv` header citations into 14–50 (§1d's Claim
> 14–27 and Boundary 28–38, §9's load-bearing 39–47) are **unchanged**
> — the addendum block was placed after line 50, at 51–70. Every Q2
> **body** citation in §1a, §1b, §0.2 and §1e shifts: +20 for old lines
> 51–132, +33 for 133–191, +39 for 192–195, +40 for 196–233, +51 for
> 234–291. §1c's `.out` lines shift too: 354→378, 360→384, 366→390,
> 372→397, 536→561, 756→778, 987→1007. The full table, segment by
> segment, is in `RESULTS.md`'s addendum section under "Line-shift
> table"; the old citations are **not** corrected in place. The seven
> other models' `.pv` and `.out` files are untouched and byte-identical,
> so every citation into Q1d, Q1r, Q3, Q4, C1, C2 and C3 still resolves
> as written.

| Short name | File | Kind |
|---|---|---|
| Q6 | `sp2_q2_degraded_compromised.pv` (amended in place) | correct, degraded, sole channel leaked — **the P2 claim, now including common attested content** |
| Q6-C | `sp2_q6_companion_content_unchecked.pv` | broken companion: the three common-content equalities removed (the verifier as it stood) |

### 10a. What was added, in one paragraph

Two honest signers of one manifest each sign their **own** frame — each
frame carries that signer's own key fingerprint, so the two frames can
never be byte-equal (that is the "framing fork" Amendment 5 §A5.4
settles, reading (a)). Six of the seven frame fields are supposed to be
the same in both: object type, algorithm, identity, manifest hash,
canonicalization version, payload. Three of those six were already
pinned, because both frames are matched against the *same* shared
tuple — `=alg` and `=id` come from `t`, and `mh = h(t)` is checked for
each frame. The other three were only *read*, never compared: `ota`
vs `otb`, `cva` vs `cvb`, `pla` vs `plb`. So A2 could attest to one
payload and B2 to another, under one manifest, and the verifier
accepted. The addendum adds the three missing comparisons, plus one
piece of **instrumentation** that lets a judge see the failure at all.

### 10b. Cast — the three new names (added to §1a)

Line numbers are Q6's (`sp2_q2_degraded_compromised.pv` as amended);
Q6-C's are given in parentheses where they differ.

| Name | What it is in the design | Built | Consumed |
|---|---|---|---|
| `contentCh` | a **private** judge channel (§0.2), the only report that carries **both** frames of **one** acceptance — needed because `acceptCh` delivers `(kA, id, fa)` and `(kB, id, fb)` as two separate messages, so a judge pairing two `acceptCh` messages could pair frames from two *different* acceptances and fire on a difference that no single acceptance ever contained | 157 (105) | out 235 (180), at the single `Accept2S` point and in parallel with the other reports (the S-P3 recut-1 idiom); in 280 (225) |
| `Spliced` | the new threat: **one** acceptance whose two frames attest different content | 160 (108) | fired 284 (229); queried 164–165 (112–113) |
| `ContentJudge` | the judge: reads the one two-frame report, destructures both frames, fires `Spliced` when object type, canonicalization version or payload differs between them; emits nothing otherwise. **Instrumentation on the acceptance report, not a verifier check** — no verifier line depends on it, exactly as `MemberJudge`'s `SetAltered` is instrumentation (§1d, cross-family review item 13) | 275–284 (220–229) | 299 (244) |

`Verifier1S`, `setCh`, `slotCh`, `acceptCh`, `SetJudge`, `MemberJudge`,
the carried S-P3 `Judge`, the fixture, the library and every
pre-existing query are **untouched**; the judge locals are `…J`-suffixed
so they shadow no library name (the S-P3 rule).

### 10c. The three new checks (added to §1b, n = 2 branch only)

Status column source: **Q6-C** (all three removed at once → `Spliced`
red) and **d12** (Q6-C plus the registered instance named literally →
that instance reachable); `RESULTS.md` addendum section, F9. They sit
after both frames are destructured (221, 223) and after both
manifest-hash checks pass (222, 224), so every field they compare has
already been shown to belong to a frame signed by the key the signed
set names for that slot.

| Line (n=1 / n=2) | Check | Plain meaning | Status |
|---|---|---|---|
| — / 228 | `if ota = otb` | both signers framed the same **kind of object** | **LOAD-BEARING for `Spliced`, jointly with 229 and 230** (Q6-C: all three absent, red; Q6: present, green). Not separately ablated: the three are registered and severed as one group |
| — / 229 | `if cva = cvb` | both signers used the same **canonicalization version** | as above |
| — / 230 | `if pla = plb` | both signers attested to the same **payload** — the field the exhibited attack moves | as above |
| — / 235 | `out(contentCh, (t, fa, fb))` | the one report that carries both frames | encoding (S-P3 recut-1 idiom), not a check |

Note what the three do **not** do, and why §1b's "`ot`, `cv`, `pl`:
read, never checked" row (167 / 188, 190 in the old numbering; 221 /
223 in the new) is still true as written for the n = 1 branch and for
each frame *individually*: nothing compares a frame's object type,
canonicalization version or payload against any **externally fixed**
value. Q4's trace still has them adversary-chosen; what the addendum
adds is only that the two slots must choose the **same** ones. Object
type against a *required* type is still S-P7's check (cross-family
review item 15), and the byte-level encoding and ordering of these now-
equal fields is still P8's (`RESULTS.md` addendum, Ledger).

### 10d. Results (`.out`)

| Query | Q6 `.out` line | Q6 result | Q6-C `.out` line | Q6-C result |
|---|---|---|---|---|
| `Stripped` | 378 | unreachable | 372 | unreachable |
| `SignerForged` | 384 | unreachable | 379 | unreachable |
| `SetAltered` | 390 | unreachable | 386 | unreachable |
| `Reattributed` | 397 | unreachable | 393 | unreachable |
| `HonestComplete(M1, verified1(k1))` | 561 | **reachable** | 558 | **reachable** |
| `HonestComplete(M2, verified2(k1, k2))` | 778 | **reachable** | 779 | **reachable** |
| `HonestAccepted` | 1007 | reachable | 1011 | reachable |
| **`Spliced`** | **1013** | **unreachable** | **1213** | **reachable** (trace 1187–1211) |

The companion is red on **exactly** `Spliced` and green on everything
else, which is what the addendum required; the amended correct model
reproduces all seven of Q2's results unchanged in text (`RESULTS.md`
addendum, "The eight-model comparison").

### 10e. Claim and boundary (plain language)

**Claim added (Q6 header 51–70).** A relying party who runs these
checks, in degraded mode with the sole authority channel in the
adversary's hands, will not accept a two-signer package in which the
two signers attested to **different content**: the two frames must
agree on object type, canonicalization version and payload, and each
still carries its own key's fingerprint. "All required signers signed
the same thing, each in its own wrapper" is now something the model
shows, not something the plan assumed.

**What Q6-C shows, and the one thing to hold onto about its trace.**
Without the three equalities, a two-signer acceptance can carry two
different payloads and nothing else in the model notices — not
`Stripped` (the set is complete), not `SignerForged` (each slot's key
is the one the signed set names), not `SetAltered` (each signer
self-signed this very manifest), not `Reattributed` (each frame binds
its own signer's fingerprint). Every existing check passes and the
content is still spliced. The trace ProVerif *exhibited* is the
cheapest one — the adversary's own manifest with two of its own keys,
which is the registered degraded-mode impersonation cost (A4 §A4.6)
happening to carry the splice — **not** the honest-A2-and-B2 shape the
plan named. That the honest shape is also reachable had to be checked
separately, and was: unregistered diagnostic
`diagnostics/d12_q6c_registered_witness.pv` names it literally and finds
it (`.out` 1428; trace 1362–1426 — honest A2 takes one payload, honest
B2 takes a different one, both under `m2`, one tuple, `Accept2S`,
`Spliced`). The same thing happened to C2 (F3), and it is worth a
reader's attention: **an exhibited trace is one witness, not the
boundary of the attack surface.**

**Boundary.** Nothing here is about the encoding or ordering of the
now-equal fields (P8): `ota = otb` is *term* equality standing in for
byte equality, under the same idealization as `h` and `fp` (§0.1,
`RESULTS.md` Consumed entry 3). Nothing here is about required sets of
more than two — the equalities live only in the n = 2 branch, because
there is no second slot to compare against in the n = 1 branch. And
`ContentJudge` is instrumentation: it reports on what the verifier
accepted and changes nothing the verifier does.
