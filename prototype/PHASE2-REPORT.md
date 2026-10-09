# Phase 2 report: the consumers (throwaway prototype)

*2026-10-06. Built by a Claude Opus 5.5 agent on top of the phase-1 issuer and verifier. This is
THROWAWAY code, not service code. Nothing is staged or committed. To reproduce, run `cd prototype && uv run pytest -q` (50 tests pass: the
25 from phase 1 and 25 new ones) and `uv run python run_phase2.py`. Code: `consumers/` (`submitter.py`,
`relying_party.py`, `examiner.py`, `scenarios.py`, `log.py`). Tests: `tests/test_phase2.py`. Spec
citations are to `docs/implementation-spec.md`.*

## Outcome

**Submitter.** It gets a receipt it can store and hand on as one JSON file without understanding it.
What the receipt attests is narrower than the submitter wants:
- It attests a JSON statement the submitter wrote, holding the tarball's digest. It does not attest the
  tarball.
- Nothing in it says who submitted. The organisation's name is an unchecked claim inside the payload.

Problems with the receipt as the submitter receives it:
- It is incomplete when it ships. The standing evidence (the TLR) can only exist about an hour later,
  and the spec names no way for it to reach the holder.
- Even its own self-check says `UNVERIFIABLE` until the submitter gets a newer verifier release. The
  release it already had does not know the blocks that bury its anchor.
- Reading back *what* was attested means decoding frame bytes. The verifier's report does not return
  the content.

**Relying party, today.** Ten bundles were run under strict and degraded policies, 20 runs in all.
Two integrators read the output:
- A non-expert reads the headline verdict and checks the digest. It made **6 unsafe accepts**.
- A careful integrator reads every field. It made **5 unsafe accepts and 5 false rejects**.

The honest receipt and the C-C2 attack are handled correctly by both. The unsafe accepts have four
causes, and only one of them is about vocabulary:
1. **Revocation.** A key revoked inside (declared, anchor] verifies `VALID_STRICT` / `ESTABLISHED`. No
   input carries revocation, and the report lists the revocation check as *passed*.
2. **Impostors.** Someone else submitted "Acme Corp" with an evil tarball through the honest service, and
   the result was `VALID_STRICT` / `ESTABLISHED`. This is correct by the spec, which attests bytes, not
   submitters.
3. **C-C5.** In degraded mode the report's first entry says `VALID_DEGRADED` and the second says
   `INVALID`. Nothing says which layer answers the integrator's question.
4. **A leaked channel key.** An attacker running its own copy of the issuer with the leaked dns key
   produces the *identical* report to an honest receipt that lost its repo evidence. This is a
   registered cost of degraded mode.

**2106 examiner.** It cannot honestly reach a verdict.
- As built, five required steps are blocked:
  - the embedded spec is a stub;
  - for a two-frame receipt, nothing defines what was anchored (K-2);
  - the anchor proof format is neither embedded nor named;
  - the bundle carries no k, δ or ε;
  - nothing carries revocation.

  Its honest output is `UNVERIFIABLE`.
- Handing it every rule a complete spec would state still leaves one required step blocked: revocation.
- It cannot rule out a contradictory TLR, because R-5.10 excludes the log that could.
- It has to trust an archived store whose identity the bundle never names.
- A bundle whose key was revoked inside the window gives it exactly the same ledger as an honest one.

## 1. Submitter (`consumers/submitter.py`)

**What it must supply.**
- **Only I-JSON** (R-4.1, R-4.2). The tarball cannot be submitted. The submitter pre-hashes it, chooses
  the hash itself, and submits a digest statement. Tessera attests that statement's bytes and nothing
  about the referent (R-1.2, R-1.4 "the external thing named by the payload is authentic").
- **A real SBOM was refused inline.** A CycloneDX SBOM with a CVSS score of `9.8` came back
  `P8_NUMBER_NOT_DOUBLE`, because 9.8 is not exactly a double. This depends on GUESS G-03 (the literal
  reading of R-3.4). The submitter cannot know which reading a real service uses. A digest-only
  statement with string values (R-4.3) is accepted.
- **No identity.** The submitter has no identity anywhere in the protocol. §2.1's actors are issuer,
  verifier, adjudicator and custodian. `"org": "Acme Corp"` is a payload claim the issuer signs
  unchecked (R-1.1, R-5.58).
- **No parameters.** §4.1 "consumes … the requested issuance parameters" but never lists them. The
  submitter cannot request a binding-form set or a policy, or declare itself custodian (R-4.63). The
  Representation Information companion (R-3.52), the natural home for the statement schema, has no
  issuance input.

**What it gets back.**
- **A shipped bundle about 60 min after submission** (k = 6 on the stub chain).
- **The TLR, about 60 min later still.** This is R-4.88(iv), "late by construction". R-4.91 says the TLR is
  "carried, not maintained" and that "everything the standing report needs is in the bundle". But:
  - nothing says how the TLR reaches the holder;
  - there is no delivery state machine like the refusal record's (R-4.63);
  - the holder must splice it in under a member name it can only learn from the implementation
    (G-26).
- **An unclear upgrade duty.** R-4.88(ii) speaks of bundles that ship with a pending proof the holder
  must upgrade. R-2.2 says a receipt never ships shallow. The submitter cannot tell which to expect.
- **A self-check that fails until it upgrades its verifier.** The verifier release the submitter held
  before submitting says `UNVERIFIABLE` (V37/V38 `HEADER_NOT_IN_TRUST_STORE`), because the burying blocks
  postdate its header store. With a refreshed release it says `VALID_STRICT` / `ABSENT` at ship, and
  `VALID_STRICT` / `ESTABLISHED` once the TLR is added.
  - This rests on the prototype's store-pin reading of header authentication (G-31). V38 is "not
    specified" (O-22).
- **A statement it cannot find without internals.** The digest of its own statement file appears
  nowhere in the receipt as text. The statement sits only inside base64 frames, and what is signed is
  its JCS-canonical form, not the bytes it sent (R-4.8). Finding "what was attested" requires the frame
  layout and payload schema (G-01, G-15). R-5.44 does not require the report to return the content.
- **On refusal it gets only a stub** (G-49, R-4.61/R-4.62 not built). It holds nothing to show an
  auditor. The spec does not say whether discarded attempt bundles ever reach the submitter.

**Can it store and hand on the receipt?** Yes: the bundle is one JSON object that survives a round
trip. But a relying party needs the submitter's statement schema to connect the receipt to the tarball,
and no part of the bundle carries or types that schema.

## 2. Relying party, today (`consumers/relying_party.py`)

**What it has.**
- The downloaded tarball and SBOM, and the bundle.
- The reference verifier.
- A trust configuration with exactly R-5.8's members, fetched at evaluation time (fresh header store).
  It has no revocation member, because R-5.8 lists none.
- A declared policy: strict, or degraded with `repo` waived.

**The two integrators.** Their rules are written down in the module docstring, because the spec leaves
the rule to relying-party policy (R-1.16, R-5.42, R-5.56):
- **Non-expert:** first per-layer entry is `VALID_*`, and the tarball digest is in an attested
  statement.
- **Careful:** every layer `VALID_*`; innermost issuer id = `wamason.com`; innermost standing
  `ESTABLISHED`; no waived evidence observed `invalid` or `names-other-key`; digest in the innermost
  statement.

| Case | Policy | Verdict per layer / standing | Non-expert | Careful | Safe decision |
|---|---|---|---|---|---|
| a honest, complete | strict | `VALID_STRICT` / `ESTABLISHED` | correct | correct | accept |
| g honest, as shipped (no TLR yet) | strict | `VALID_STRICT` / `ABSENT` (S3) | correct | false reject | accept |
| b C-C2 reattribution | strict / degraded | `INVALID` (V17, V18 on A and B) | correct | correct | reject |
| c C-C5 transplant, evil tarball | strict | `UNVERIFIABLE`; `INVALID` | correct | correct | reject |
| c C-C5 transplant, evil tarball | degraded | **`VALID_DEGRADED`; `INVALID`** (V19[A]) | **UNSAFE ACCEPT** | correct | reject |
| d1 honest, repo waived, present | degraded | `VALID_DEGRADED` / `ESTABLISHED`, repo `would-pass` | correct | correct | accept |
| d2 honest, repo evidence lost | strict | `UNVERIFIABLE` / standing `None` | false reject | false reject | accept |
| d2 honest, repo evidence lost | degraded | `VALID_DEGRADED` / `ESTABLISHED`, repo `absent` | correct | correct | accept |
| d3 clone issuer, leaked dns key, own TLR | degraded | **same as d2** | **UNSAFE ACCEPT** | **UNSAFE ACCEPT** | reject |
| e honest, key revoked in (declared, anchor] | strict / degraded | **`VALID_STRICT`** / `ESTABLISHED` | **UNSAFE ACCEPT** | **UNSAFE ACCEPT** | reject (R-5.21: `INVALID`) |
| f impostor through the honest service | strict / degraded | **`VALID_STRICT`** / `ESTABLISHED` | **UNSAFE ACCEPT** | **UNSAFE ACCEPT** | reject |
| h honest custodial renewal wrapper | strict / degraded | `VALID_STRICT`; `VALID_STRICT`, no standing for either layer | correct | false reject | accept |

The table shows one row per distinct outcome. The full matrix (20 runs) is in `run_phase2.py` and is
pinned by `test_relying_party_matrix`.

**What worked.**
- C-C2 is `INVALID` under both policies, and the failed checks name the binding (R-5.35, V17, V18).
- Strict policy turns every leaked-channel case (c, d3) into `UNVERIFIABLE`. A relying party that never
  degrades is never fooled by them. The price is false rejects of honest receipts that lost one evidence
  (d2).

**What broke or confused.**
1. **C-C5 (c).** Per-layer reporting (R-5.42) places the attacker's own `VALID_DEGRADED` wrapper first.
   The spec forbids an aggregate (R-5.47) and gives no composition rule (R-7.49 is a candidate only). The
   non-expert's rule accepts the evil tarball. The careful rule rejects it, but the same rule rejects the
   honest renewal wrapper (h): no layer of a wrapped bundle reports standing (R-6.44 routes it to S-P7).
   No rule found here gets both c and h right while also demanding standing.
2. **A leaked key looks like a lost evidence (d2 = d3).** An honest receipt whose repo evidence was lost,
   and an attacker's receipt minted under Tessera's issuer id with the leaked dns key and its own TLR,
   give the same verdict, standing, observations, failed list and unperformable list. Only the issuer
   key fingerprint differs, and R-5.8's trust configuration holds no issuer key to compare it with.
   - This is the registered cost (R-1.11, R-5.31, R-6.43).
   - The relying-party consequence is that the `absent` observation is uninformative: the same
     observation fits both cases.
3. **Revocation (e).** The bundle bytes are identical to (a). The revocation is a fact in the world that
   no input carries (R-5.4, R-5.8; G-27).
   - What the relying party can learn: the window that matters, (declared, anchor] = (T0, T0 + 600 s),
     and the two key fingerprints. Nothing else.
   - What the verifier reports: `REV[A]` and `REV[B]` as `pass`. A required check reported as passed
     without being performed is the misreport R-5.33 forbids.
   - The other reading of the same spec makes the check unperformable, and then *every* bundle ever
     issued is `UNVERIFIABLE`.
   - With the prototype's out-of-band extension (G-27) the result is `INVALID` on `REV[B]`.
   - As adjudicator the relying party may use anything (R-1.22), but no revocation publication, format
     or authenticated effective time is defined (R-5.24), so there is nothing to fetch.
4. **The impostor (f)** is the cleanest case. Someone other than Acme submits a statement naming "Acme
   Corp" through the honest service and gets `VALID_STRICT` / `ESTABLISHED`. It is correct by R-1.1 and
   R-1.4, and fatal to an integrator whose question is "is this Acme's release". §3.4 marks issuer
   identity "bound, not validated". No input tells the relying party which issuer or submitter to
   expect.
5. **A fresh honest receipt (g)** reports `ABSENT` / `NO_TERMINAL_DISPOSITION_EVIDENCE`. That is the
   same code an abandoned artifact presented alone gets (S3, R-6.30). A relying party cannot tell "too
   early" from "abandoned".
6. **Strict, evidence lost (d2).** Standing comes back with value `None`. The model emits no standing
   report when the authority step cannot proceed (R-6.24 step 1; G-34), so the output has a hole the
   vocabulary (R-5.46) does not name.

## 3. The 2106 examiner (`consumers/examiner.py`)

**What it holds.** The bundle; an archived store holding channel keys by validity period (R-5.8) plus
header hashes (R-2.19); and the bundle's embedded objects. No live service, DNS, repository or log
(R-5.10).

**No Tessera code.** The module imports nothing from `tessera_proto` at top level, and a test pins
this. Only the two experimenter-side helpers that build its inputs import it. It reconstructs what it
can and records the source of every rule.

**Run 1, the bundle as built: `UNVERIFIABLE`.** Five required steps are blocked:
- **The procedure.** The embedded spec is 180 bytes of prose. Even the full 2026 spec leaves O-01 and
  O-79 open (R-7.4, R-7.9).
- **The receipt-to-anchor binding.** A two-frame receipt has no defined "its canonical bytes" (R-3.42,
  K-2). Obvious constructions were tried and none matched.
- **The anchor proof path.** The OpenTimestamps and Bitcoin formats are neither embedded nor named
  (R-3.51, R-7.7).
- **The temporal predicate.** The bundle carries a policy-version label and an observed delay, not k, δ
  or ε (R-2.20, §8).
- **Revocation** (R-5.21).

Reconstructed by inspection or trial, plausible but not given:
- the frame layout (byte-identical rebuild);
- the fingerprint function (one of four candidates matched);
- the manifest hash;
- the possession message (by guessing a type tag never seen in the bundle);
- the header-hash rule;
- the entitled key.

**Run 2, every rule a complete spec would state handed over: still `UNVERIFIABLE`.** Those rules are
the frame layout, encoding map, fingerprint, manifest hash, possession message, receipt digest, proof
format, header hash, k/δ/ε and the attempt-core rule. One required step stays blocked: revocation.
- If the examiner trusts its reconstructions and assumes no revocation, it reaches `VALID_STRICT`.
- The revoked-in-window bundle yields exactly the same ledger (`test_examiner_with_complete_spec_still_lacks_revocation`).
- "No contradictory TLR exists" stays undecidable: the only witness is a log, and R-5.10 excludes it
  (R-5.59, R-7.23).

**What it has to trust.**
- **The archived store.** It decides every channel and header check, and the bundle names no store
  identity, digest or version (R-5.8, R-2.18; R-7.12 is a candidate).
- **The issuer's declared time.** The stub authority evidence carries no time of its own, so the
  examiner picks the store's key "by validity period" using the issuer's own declared time. R-5.4
  requires "time-anchored" evidence; the stub omits it.
- **Its reconstructions.**
- **SHA-256 and Ed25519**, still sound or renewed by a custodian (R-7.1 claim 3).
- **The issuer's honesty** about misissuance and equivocation (R-5.58, R-5.59).

**Chicken and egg.** The governing spec's identifier sits inside the signed payload (R-3.50). The
examiner has to parse the frame before it can learn which procedure governs parsing it.

**What the bundle would need to carry that it does not.**
- *The spec does not require it either (design gaps):*
  - revocation facts with authenticated effective times, or a statement that none exist (G-27);
  - the identity and digest of the trust-anchor and header store the verdict depends on;
  - (inherent) evidence about contradictory TLRs.
- *The spec requires it; the prototype omits it:*
  - a real embedded spec and conformance vectors (R-3.50, R-3.53);
  - a complete dependency manifest (R-3.51). Missing are SHA-256, JSON, base64, OpenTimestamps,
    Bitcoin header and proof-of-work rules, DNSSEC, and the git object format with OpenPGP;
  - time-anchored authority evidence (R-5.4).
- *The spec has not yet fixed it (open obligations the embedded spec would carry once fixed):*
  - the frame layout (O-01) and encoding map (O-79);
  - the fingerprint function (G-10);
  - the two-frame anchor digest (K-2);
  - the attempt-core rule (MODELLED only).

**What the stubbed anchor hides.**
- **Header authentication.** In the stub, "authenticated" means "listed in the store". A real
  examiner needs Bitcoin's header format, proof-of-work and difficulty rules, and a checkpoint, and must
  decide which chain is canonical (V38 not specified, O-22). A store frozen before issuance cannot pin
  later blocks. This is the same effect that made the submitter's self-check `UNVERIFIABLE`.
- **Block time.** Stub blocks carry exactly the chosen time. Real header timestamps are miner-set, can
  run about 2 h fast and need not increase, yet V33–V35 compare them with the declared time to the
  second.
- **Proof format.** The stub txid is a hash of the digest, and the merkle path uses private prefixes.
  Real OTS proofs are operation chains into a real transaction, and txid-to-transaction needs chain
  data (R-4.75).
- **Authority evidence.** One Ed25519 key per channel stands in for:
  - a DNSSEC chain: the 2026 root KSK, DS/DNSKEY links, and RRSIG windows evaluated at an authenticated
    time;
  - an anchored git publication with its own signing key and OTS proof.
- **Hash survival.** Everything bottoms out in SHA-256. The stub cannot show the never-renewed bundle
  after SHA-256 weakens.

## Evidence for PREDICTIONS.md items 5 and 6 (the owner scores)

**5. "A relying party finds the verdict vocabulary confusing or insufficient in at least one realistic
case."**

Evidence for:
- **Vocabulary proper.**
  - S3 gives one code to a fresh honest receipt and to an abandoned artifact presented alone (g).
  - In strict mode with lost evidence, standing has no value at all (d2; R-6.24 step 1, G-34).
  - `absent` is reported identically for lost honest evidence and for a leaked-key clone (d2 = d3).
    That is registered as a cost (R-1.11), but it leaves the observation unable to inform the
    decision.
- **Composition.** C-C5 yields `VALID_DEGRADED` beside `INVALID`. Six of the non-expert's 20 runs are
  unsafe accepts, one of them caused by reading the first layer.

Evidence that tempers it: most unsafe accepts are *not* vocabulary failures.
- Revocation (e) is an input gap; the verifier reports a check that never ran as passed.
- The impostor (f) is the identity boundary working as specified.
- In strict mode with a never-degrade policy, only e and f fool the careful integrator.

Whether that counts depends on how narrowly "vocabulary" is read.

**6. "The 2106 examiner, with no service alive, needs something the bundle does not carry."**

Evidence for: with a complete spec handed over, the examiner still lacks two things the spec does not
require the bundle to carry:
- revocation facts (G-27). This one blocks a required check;
- the identity of the archived store it must trust.

It also cannot decide equivocation without a log, which R-5.10 excludes.

Caveats:
- With the bundle as built, many more blockers are prototype omissions (stub spec, short dependency
  manifest, untimed evidence) or open spec obligations (O-01, O-79, K-2). They are not design gaps.
- The stub anchor makes run 2 look easier than reality: real header authentication and OTS are hidden.

## Design questions for the author (ranked)

1. **Where do revocation facts come from?** R-5.21 needs revocation facts and their effective times,
   but no bundle member (R-5.4) or trust-configuration member (R-5.8) carries them and R-5.10 forbids
   fetching them. Where do they come from? Until then, is the check *unperformable* (every bundle
   `UNVERIFIABLE`) or *vacuously passed* (revoked keys verify)? [§5.2(i) R-5.21; R-5.4; R-5.8; R-5.10]
2. **Who is the issuer for a release an organisation submits?** One of two readings must hold, and in
   neither does any input tell the relying party whom to expect:
   - (a) A single Tessera service signs anyone's statements. Then the submitter is never attested, and
     an impostor gets `VALID_STRICT` / `ESTABLISHED`.
   - (b) Each organisation runs its own issuer. Then the relying party must check an issuer id that
     §3.4 calls "bound, not validated".

   [§2.1; R-1.1/R-1.4; §3.4 table; R-2.13; R-5.8]
3. **How should a relying party combine per-layer verdicts?** What should it do when they disagree
   (C-C5: `VALID_DEGRADED` over `INVALID`) or when wrapped layers carry no standing? R-5.42 and R-5.47
   forbid an aggregate, and the only composition rule is a candidate. [R-5.42; R-6.44; R-7.49 (docket 19)]
4. **How does the TLR reach the holder?** Also:
   - what does a holder of a fresh receipt see meanwhile, given that S3 conflates "too early" with
     "abandoned"?
   - what happens to an already-shipped receipt when the second anchoring fails? R-4.88(i) hands that
     failure to refusal machinery after shipping.

   [R-4.88; R-4.91; R-6.30; R-4.63]
5. **Should the bundle bind the archived store?** Should it bind the identity and digest of the
   trust-anchor and header store its verdict depends on? And how does a store distributed before
   issuance authenticate the later blocks that bury the anchor?
   [R-5.8; R-2.18; R-2.19; V38 / O-22; R-7.12 (docket 8)]

## Phase-2 guesses and changes (for GUESSES.md bookkeeping)

- **G-51.** The TLR reaches the holder as a separate message after ship; the shipped bundle carries
  no `standing` (`submitter.deliveries_from`).
- **G-52.** The relying party's trust configuration is fetched at evaluation time. The submitter's
  pre-submission copy is stale, which demonstrates the effect of G-31.
- **G-53.** The two integrator rules are mine. The spec gives none.
- **G-54.** The examiner's archived store has the shape `{channel_keys{name: {pub, valid_from, valid_to}},
  header_hashes}`. Its validity periods are invented.
- **Phase-1 code changed in one place.** `attacks.replay_cc05` gained optional `inner_content` and
  `outer_content` arguments, so C-C5 can carry an evil release statement. The defaults are unchanged
  and the phase-1 tests pass unchanged.
