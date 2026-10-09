# TRIAGE of the throwaway prototype's findings (2026-10-07)

*Owner-instance triage (Claude Opus 5.5) of `GUESSES.md`, `PHASE1-REPORT.md`, `PHASE2-REPORT.md` and
the scored `PREDICTIONS.md`. Reference texts: `docs/implementation-spec.md` (cited "spec l.N"),
`formal/PROPERTIES.md`, `formal/suite/capstone/PREDICTIONS.md` ("CAP l.N"), `formal/suite/LEDGER.md`,
`formal/BAND0-EXIT.md`. THROWAWAY directory; nothing here registers, rules or discharges anything.
Where a point below goes beyond what the prototype tested, it says "(triage analysis)".*

## 0. Is the model modelling the right thing? The WRONG list

**No finding is WRONG in the sense of this file: the prototype shows no model claim or checked property to
be false.** The evidence:

- **Positive evidence.** Both symbolic attack traces replay with real Ed25519 signatures. The verifier
  built from spec §5 rejects them on the checks the model names: C-C2 on V17/V18, C-C5 on V19 alone. The
  mutants that remove exactly those checks accept (PHASE1-REPORT l.13-20, l.92-98). The registered
  degraded cost (case (d), `AcceptS ⟹ IssuerSigned` red, CAP l.91) shows up concretely as d2 = d3
  (PHASE2 l.149-157). S-P7's model also accepts an outer layer independently of its inner check
  (`AcceptOuter` precedes `InnerCheck`, `s-p7/proverif/sp7_q2_degraded_compromised.pv:328-333`), which
  matches the prototype's `VALID_DEGRADED` outer layer beside an `INVALID` inner one.
- **The one result that looks like a violation is the prototype's own.** In case (e) a key revoked
  inside (declared, anchor] verified `VALID_STRICT`, which contradicts P6. The cause is
  `tessera_proto/verifier.py:315-317`, which maps "no revocation entry" to `PASS`. That is a misreport
  under R-5.33 (spec l.1384), not a counterexample to P6 (see §6).
- **What the prototype finds instead is 21 MISSING items.** In each, a model claim holds only under a
  condition that neither the model nor the spec states, or the design needs a fact that no model
  carries. Six bear on the capstone (§3). The deepest are:
  - G-17: the required binding-form set;
  - G-21: authority-channel scope;
  - G-27: revocation has no carrier.
- **How strong the "none WRONG" evidence is depends on the area.**
  - Where the prototype stubbed *exactly as the model abstracts*, it could not have found a WRONG: the
    authority channels are one Ed25519 key each (G-21), the anchor is a hash chain (G-20), and KMS and
    GPG are both Ed25519 (G-12, G-13).
  - The G-21 and P1-1 entries below are places where a real primitive *could* contradict a model claim.
    The prototype did not exercise any of them.
  - The prototype was built by the same model family that drafted the spec.

## 1. The triage rule

1. **Kind**:
   - IMPL: the spec leaves an implementation detail open.
   - ASSUMPTION: something is relied on that nothing establishes.
   - STANDARD: an unstated choice, or a mismatch, relative to a named external standard.
   - GUARANTEE: a modelled guarantee fails, or holds only under a hidden condition.
2. **Capstone?**
   - YES: it changes what `capstone.pv` must express, or what one of its queries means.
   - OTHER-MODEL: it bears on P4, P5, P5c, P6, P8, P9 or P10, named.
   - NO-DEFER: it can be settled in code without moving any model claim. "Nice to model" counts here.
3. **Model status**:
   - WRONG: a model claim is shown false.
   - MISSING: the model does not claim it, and the design's claims need it.
   - DEFER: implementation only.
4. **Severity** is for the author: HIGH, MED or LOW.
5. **Merges.** Duplicates are merged into one row, and the merged ids are listed in the row:
   - K-2 into G-19; K-4 into G-17; K-5 into G-14; K-6 into G-29; K-7 into G-42;
   - K-3's OpenPGP half into G-13, while its algorithm-equality half is K-3a;
   - G-52 into G-31; G-53 into P2-1; G-54 into P2-9.

## 2. Summary

Rows: G-01 to G-50, G-03b and G-10b (52), K-1, K-3a, G-51, P2-1 to P2-14 (phase-2 findings with no
G-number) and P1-1 to P1-2 (phase-1 prediction observations), **71 in total**. The brief's "52 entries
incl. 7 contradictions" is 52 G-rows *plus* K-1 to K-7.

| Kind \ Capstone? | YES | OTHER-MODEL | NO-DEFER | Total |
|---|---|---|---|---|
| IMPL | 0 | 13 | 31 | 44 |
| ASSUMPTION | 4 | 7 | 3 | 14 |
| STANDARD | 1 | 5 | 3 | 9 |
| GUARANTEE | 1 | 0 | 3 | 4 |
| **Total** | **6** | **25** | **40** | **71** |

- Model status: **WRONG 0, MISSING 21, DEFER 50**.
- Severity: HIGH 5, MED 25, LOW 41.
- The six YES rows are five items: G-14 and G-22 form one item.

## 3. Capstone YES, ranked

**1. G-17 (+K-4): who sets the required binding-form set.** ASSUMPTION · MISSING · **HIGH**.

- *What the capstone assumes.* Its strict and degraded forms fix in the verifier which channels are
  required (CAP l.84-91).
- *What the spec says.* R-3.37 / V21 (spec l.635, l.1300) has the verifier read a *signed* required set
  from the envelope. The §3.4 table (l.585) puts that set in the manifest, which is outside map-v1 and
  outside `mh = h(t)` (K-4). No family carries the set (O-73, spec l.2166).
- *The attack (triage analysis).* If the set is read from the bundle, an adversary-enrolled key signs its
  own set `{repo}`. In case (b) it then reaches strict acceptance with the one leaked channel. This
  happens even if the set is signed, and link 1b with `Accept ⟹ IssuerSigned` would go red.
- *What the capstone needs.* Either:
  - a registered sentence, with a matching spec rule, that strict's required forms come from verifier
    policy and that V21 is only a well-formedness check; or
  - the set modelled inside `t` or the frame, plus a companion that lets the bundle choose the set,
    which should red link 1b in (a)/(b).

**2. G-21 (+P2-3, the issuer-identity question): authority-channel scope.** GUARANTEE · MISSING ·
**HIGH**. This is triage analysis built on the prototype's stub, and the prototype did not test it.

- *What the model assumes.* An authority channel is one key, `pkD` or `pkR`, held only by the issuer's
  channel.
- *What the spec says.* R-4.26 (l.949) names the `wamason.com` zone. R-5.8 (l.1217) puts *DNS root keys*
  in the trust-anchor store, and a DNSSEC chain to the root validates any zone. No check (V20, V22, V23)
  ties the evidence's owner name or repository to the issuer: R-3.36 says `issuerId` is "bound, not
  validated".
- *The consequence.* If the verifier validates DNSSEC from the root and pins no owner name, any domain
  holder is an "uncompromised channel". Case (b) then yields strict acceptance for an adversary key with
  no verifier mutation, and link 1b's meaning ("an uncompromised channel published this tuple") silently
  depends on name scoping.
- *What the capstone needs.* A registration sentence that a channel key denotes the issuer's
  trust-configuration-pinned zone and repository, with a matching spec check (owner name = pinned name,
  or = `issuerId`). Alternatively, evidence modelled as `(STMT_DIGEST, zone, h(t))` under a
  root-certified zone key, with a companion that drops the zone pin.
- *The other half of the identity question is by design.* The impostor submitting through the honest
  service (P2-3) is R-1.1/R-1.4 working as written, and it is NO-DEFER.

**3. G-14 + G-22 (+K-5): the "manifest = authority tuple" abstraction.** ASSUMPTION · MISSING · MED.

- *The gap.* R-3.38 (l.641) says possession covers the "manifest", while the model and V24 cover `t`.
  R-3.31 (l.589) makes the manifest keys + evidences + its own anchor. The prototype stayed sound only
  by keeping `mh = h(t)` and pushing every other member into the attestation's signed bytes or into a
  fingerprint comparison (PHASE1 l.88-90). The spec does not state that rule.
- *Does the abstraction hide a real gap?* Item 1 is the real gap it hides. Otherwise the abstraction is
  sound when every manifest member outside map-v1 is one of:
  - (i) self-authenticating (evidences, signatures);
  - (ii) bound through `fp` (keys, L2-b);
  - (iii) declared non-authoritative under R-3.33 (l.613).
- *What the capstone needs.* §7 should register that condition, and the spec should define R-3.38's
  "manifest" as the tuple's bytes.
- *A related fixture restriction (triage analysis).* CAP l.78's ONE KEY, ONE MANIFEST is load-bearing.
  Rotating only the GPG slot under R-5.24 (a new manifest entry) while keeping the KMS key makes one key
  sign two manifests, which falls outside the fixture.

**4. K-3a: the algorithm must be equal across signer slots.** ASSUMPTION · MISSING · MED.

- *The conflict.* R-2.1/R-4.13 (l.226, l.917) put KMS and GPG in independent custody domains. R-3.12
  (l.432) and the tuple's single `alg` forbid different algorithms per slot. A KMS ECDSA-P256 slot next
  to a GPG Ed25519 slot is unrepresentable.
- *What the capstone needs.* The author should choose before freeze:
  - one algorithm for both slots (no model change; this needs a KMS that offers the GPG slot's
    algorithm); or
  - per-slot `alg`, which changes `authTuple`'s shape and check 4 of CAP l.120, and with them D7's
    companions C-C16/C-C17.

**5. P1-1: DSKS emulation versus real ECDSA (KMS).** STANDARD (FIPS 186-5 ECDSA; SEC 1) · MISSING ·
MED. This is triage analysis.

- **Strong DSKS.** This is the library's `dsks`: an attacker-*held* key under which a seen signature
  verifies (`lib/tessera_theory.pvl:110-115`, R-2.43 l.322).
  - It is not known to be feasible for ECDSA over a *fixed named curve*.
  - It is feasible when the verifier accepts keys with explicit domain parameters: the attacker picks the
    generator (Blake-Wilson & Menezes, PKC 1999; CVE-2020-0601 "CurveBall").
  - A profile that accepts explicit parameters makes C-C5 concretely replayable with no emulated hook.
    The correct verifier still rejects it on V19. The P3 [model] half stands; the P3 [assum] half (L2-e,
    H1a) must pin named curves and put the curve id under `fp` (G-10).
- **Weak key substitution, which ECDSA always permits.** For a seen `(r, s)` and *any* message `m'`, the
  key `Q' = r⁻¹(sR − H(m')G)` verifies `(r, s)` on `m'`, with no private key.
  - This lies outside R-2.43's bound, since `dsks` gives the same message only, with a private key.
  - It cannot produce possession: one `Q'` cannot satisfy two signatures, and the attacker does not hold
    the private key. So the capstone's results carry over only through link 3 / C-Q9 (D-3).
  - That is an argument, not a model fact.
- **Malleability and randomness.** `(r, n − s)` is a second valid signature, and KMS ECDSA is
  randomized, so ECDSA violates **L2-f**, deterministic signatures (LEDGER l.880: L-01, L-06, L-12,
  L-16).
  - `attemptCore` contains `sg` (R-3.25 l.535), and cap11c shows the `=sgI` pin is load-bearing
    (CAP l.2945).
  - A mauled signature therefore changes `aid`, and standing drops to `ABSENT`. This costs availability;
    it does not produce a false `ESTABLISHED`.
- **What the capstone needs.**
  - A registration change in CAP §6: D-4 under-approximates ECDSA's other-message substitution, which
    possession closes; L2-f is false for KMS ECDSA unless the profile requires low-s and RFC 6979.
  - Optionally, one probe adding a public-only rewrite `ksub(s, m')`, to show that the queries stay
    green.
- **Ed25519's analogue (noted only).** The verification profile must choose cofactored or cofactorless
  verification and reject small-order keys (RFC 8032 leaves this open; Chalkias et al., "Taming the many
  EdDSAs", 2020).

## 4. OTHER-MODEL

| Id | Kind | Model | Status | Sev | What it needs |
|---|---|---|---|---|---|
| **G-27** (+PHASE2 Q1, case e) | ASSUMPTION | **P6** (TLA+ `revoked` is a given state variable with no carrier), **P9** (input enumeration) | MISSING | **HIGH** | R-5.21 (l.1358) cannot be performed: no bundle member (R-5.4) or trust-config member (R-5.8) carries revocation, and R-5.10 forbids fetching it. Options A/B/C are in §7. Under B, the carrier is a channel-signed statement, which also adds a signing domain to L-07 and a check to the capstone. |
| G-10b | ASSUMPTION | P4 (A3.6.2 unknown-algorithm transition, E6) | MISSING | MED | An algorithm-specific `fp` makes V16 unperformable for an unknown algorithm. P4's transition has to say "unperformable, not failed", or the canary (R-3.53) becomes `INVALID`. |
| G-29 (+K-6) | IMPL | P4 | MISSING | MED | A missing required evidence is `INVALID` under R-2.37 and `UNVERIFIABLE` under R-2.30 and P4. P4 abstracts check outcomes, so the partition must name this case. |
| G-19 (+K-2) | IMPL | P8 (receipt digest); P5 (V33a) | MISSING | MED | "Exactly one anchor over its canonical bytes" names no single byte string under reading (a). This blocked the examiner. |
| G-39 | ASSUMPTION | P5c / bridge | MISSING | MED | `HonestShipAccepted` assumes the issuer's ship guard and the verifier use the same δ/ε. Verifiers own δ (R-3.46), so honest receipts can fail at stricter verifiers. |
| G-50 | ASSUMPTION | P5c (L-19) | MISSING | MED | R-6.14's "issuance policy's tolerances (verifier-owns-tolerances applies)" contradicts itself. |
| G-31 (+G-52) | STANDARD (Bitcoin headers; OpenTimestamps) | P5 (V37/V38, O-22) | MISSING | MED | Header authentication is unspecified. The prototype's store-pin reading caused the submitter's `UNVERIFIABLE` (see §6). |
| P2-5 | ASSUMPTION | P5c (refusal latch, E6/L2-n) | MISSING | MED | R-4.88(i): the second anchoring can fail after the receipt has shipped. The refusal machinery is not modelled after ship. |
| P2-9 (+G-54, PHASE2 Q5) | ASSUMPTION | P9 | MISSING | MED | The verdict depends on an archived store the bundle never names. V38 already lists "store identity pinned in declared verifier policy" (l.1348), and L2-k is the registered exposure. A store frozen before issuance cannot pin later blocks. |
| P2-10 | ASSUMPTION | P10 (first link, untimed); P6 (`key_authorized(declared)`) | MISSING | MED | Authority evidence must be "time-anchored" (R-5.4), but how a DNSSEC snapshot's time is established is unstated. The examiner fell back on the issuer's declared time, which lets a leaked retired channel key backdate. |
| G-01 | IMPL | P8 (O-01, E3) | MISSING | MED | Frame layout. A second implementation would agree on no signature. |
| G-15 | IMPL | P8 (O-79) | MISSING | MED | The encoding map (R-3.12a). Check 4's common-content equality rests on it. |
| G-10 | STANDARD (RFC 9580 fingerprints) | P8 (L2-b) | MISSING | MED | The `fp` function, and whether DNS/git publish the same `fp` as OpenPGP's v4/v6 fingerprint. |
| G-49 | IMPL | P5c (A3.7.2, E6) | MISSING | LOW | The refusal record is not built. Known E6. |
| G-03 | STANDARD (RFC 8785 §3.2.2.3; RFC 7493 §2.2) | P8 (accepted domain, L2-j) | DEFER | MED | R-3.4's "exactly representable" read literally refuses `9.8` and `0.1`. A real SBOM was refused (PHASE2 l.63). |
| G-02, G-03b, G-06, G-08, G-11, G-16 | IMPL | P8 | DEFER | LOW | Byte details for E3's golden vectors. |
| G-04 | STANDARD (RFC 7493 §2.1) | P8 | DEFER | LOW | Surrogates and noncharacters. |
| G-05 | STANDARD (Unicode UAX #15; RFC 8785 does not normalize) | P8 | DEFER | LOW | "Reject non-NFC" is a choice. |
| G-07 | IMPL | P8 (L2-i) | DEFER | LOW | One tag carries both domain separation and the object type. This is sound only if every signed thing is a frame. |
| P2-11 | IMPL | P8 | DEFER | LOW | The spec id sits inside the payload, so the frame layout must be parseable independently of the spec version. |

## 5. NO-DEFER (40)

| Id | Kind | Status | Sev | Note |
|---|---|---|---|---|
| **P2-1** (+G-53, PHASE2 Q3) | ASSUMPTION | MISSING (design, not model) | **HIGH** | C-C5 gives `VALID_DEGRADED` over `INVALID`, and no rule combines layers. The model agrees with the per-layer outcome, and CAP §7 l.1994 excludes the adjudicator's decision. It belongs to E12, the relying-party story, and R-7.49. |
| **P2-3** (+PHASE2 Q2, case f) | ASSUMPTION | DEFER | **HIGH** | The impostor gets `VALID_STRICT` through the honest service: R-1.1/R-1.4 by design. The relying-party story (E12) must say no input names whom to expect. The capstone half is §3 item 2. |
| P2-2 (case d2 = d3) | GUARANTEE | DEFER | MED | A leaked channel key looks the same as lost evidence. This is the registered cost (R-1.11, R-5.31, case (d)). E12 must say `absent` is uninformative. |
| G-09 | IMPL | DEFER | MED | The two-signer `key_fp`/`sset` semantics. CAP l.78 already fixes them; the spec must import them. |
| G-13 (+K-3 OpenPGP half) | STANDARD (RFC 9580 §5.2.4: hashes data ‖ hashed-subpacket trailer) | DEFER | MED | The verification profile must define V19 over `fb ‖ trailer`. An *inline-signed* OpenPGP form would make C-C5's mutant a real bug class (G-41). |
| G-20 | STANDARD (OpenTimestamps; Bitcoin) | DEFER | MED | Stubbed. L2-m. |
| G-32 | IMPL | DEFER | MED | V4 takes the expected type from the bundle, restricted to `{ATTEST, WRAPPER}`. The spec should state the per-position type. |
| G-44 | IMPL | DEFER | MED | Wrapped standing. The capstone already has formulation W (CAP l.704-709), but the spec does not (see §6). |
| G-51 (PHASE2 Q4) | IMPL | DEFER | MED | How the TLR reaches the holder. No delivery machine exists, despite R-4.91's "carried". |
| P2-4 (case g) | IMPL | DEFER | MED | S3 gives "too early" and "abandoned" the same code. This is a reason-code fix (compare EN 319 102-1's `TRY_LATER`, §7). |
| G-42 (+K-7) | ASSUMPTION | DEFER | LOW | R-3.43 credits P7 with txid containment, which no model checks. The txid can be recomputed from the proof. |
| G-12, G-18, G-23, G-24, G-25, G-26, G-28, G-30, G-33, G-34, G-35, G-36, G-37, G-38, G-40, G-41, G-43, G-45, G-46, G-47, G-48, K-1, P2-6, P2-7, P2-8, P2-14 | IMPL | DEFER | LOW | Formats, reason codes, outputs and scoping that are already registered. Specific notes: G-24's single-signature core is harmless under L2-f (P1-1). G-37 is L-16 scoping. G-46 implements P4's legal-policy precondition. P2-6 is R-4.88(ii), probably misread (§6). |
| P2-12 | GUARANTEE | DEFER | LOW | Equivocation cannot be decided without a log. This is registered (R-5.59). |
| P2-13 | STANDARD (Bitcoin MTP and 2-hour future rule) | DEFER | LOW | Miner-set timestamps. P5 already models non-monotonic timestamps (`P5P6_TemporalRevocation.tla:71,103,251`). |
| P1-2 | GUARANTEE | DEFER | LOW | The signed declared time limits C-C2 to the δ/ε window concretely. The real system is stronger than the model here. |

## 6. Findings that misread, or partly misread, the spec

1. **Case (e)'s `VALID_STRICT` for a revoked key** (PHASE2 l.160, PHASE1 report "revocation
   inside the window (`INVALID`)"). The prototype's verifier (`verifier.py:315-317`) reports `REV` as
   `PASS` when no input exists. R-5.33 (l.1384) forbids reporting a required check as passed when it was
   not performed. The report says so itself, but then counts the result as an unsafe accept the spec
   produces. The spec gap (G-27) is real; the `VALID_STRICT` is the prototype's.
2. **"No rule gets both c and h right"** (PHASE2 l.146-148; G-44). R-6.44 (l.1705) does route wrapped
   standing to S-P7. But the author's 2026-09-15 ruling, formulation W (CAP l.704-709), reports standing
   over a wrapped presentation, bound to the innermost issuer. The spec (dated 2026-09-13) does not carry
   it. Under W, the careful rule accepts h on the innermost layer's standing and rejects c on its
   `INVALID`. The finding is a stale-spec defect, not a model gap.
3. **"The submitter's self-check is `UNVERIFIABLE` until it upgrades its verifier"** (PHASE2 l.83-90;
   G-31, G-52). R-5.4 (l.1184), the §3.5 table and V37 (l.1347) let the headers travel in the bundle.
   The failure comes from the prototype's rule that every header must equal a store pin; V38 is open
   (O-22).
4. **R-4.88(ii) versus R-2.2** (PHASE2 l.83). In context (l.1101, the SC-1 costs, where item (i) is the
   *second* anchoring), "a bundle ships before confirmation" most plausibly refers to the TLR's pending
   anchor, not the receipt's. R-2.2 is probably not contradicted. The author should confirm.
5. **Design question 5, "should the bundle bind the store?"** (PHASE2 l.323). This half-misreads the
   spec. R-5.8 deliberately ships the store with the verifier (P9), and V38 already names "store identity
   pinned in declared verifier policy". The open question is O-22, not a new design gap.
6. **K-1** is not a contradiction, as the prototype itself marks it ("apparent"). "Not validated" in
   R-3.36 means no policy check. The equality pins are binding.

## 7. Comparison with long-term-validation standards

*Sources are the standards named. Recollections I could not verify against the text here are marked
"(unverified)". Tessera's spec has no section that cites any of these.*

- **RFC 3161 (Time-Stamp Protocol).**
  - *What it does.* A trusted TSA signs a `TimeStampToken`, a CMS SignedData over a `messageImprint`
    hash, carrying `genTime` and a policy OID. It carries no revocation data itself. The token's own
    validity depends on the TSA certificate and its revocation status, checked separately.
  - *Tessera.* Tessera replaces the TSA with OpenTimestamps/Bitcoin, which needs no trusted third party.
    The price is that block time is miner-set within consensus bounds, hence δ/ε. Tessera has no
    analogue of TSA-certificate validation; header authentication (V38) plays that role and is open.
- **RFC 5126 CAdES, now ETSI EN 319 122-1/-2.**
  - *What it does.* It defines levels: BES/EPES, then -T (a signature timestamp), -C (certificate and
    revocation *references*), -X (timestamps over those references), -XL (the certificate and revocation
    *values* embedded: `certificate-values`, `revocation-values`), and -A (a renewable
    `archive-time-stamp`). EN 319 122 renames these baseline B-B / B-T / B-LT / B-LTA.
  - *Revocation.* Status (CRL/OCSP) is collected after signing, ideally after a grace period (RFC 5126's
    "grace period"; I could not confirm the clause number), and embedded so that validation needs no
    live access.
  - *Tessera.* Tessera has -T (the anchor) and the archive-renewal idea (wrapper renewal). It has no -LT
    equivalent: nothing embeds revocation status (G-27).
- **PAdES, ETSI EN 319 142.**
  - *What it does.* The same levels for PDF. The LT material lives in the Document Security Store (DSS)
    dictionary: certificates, CRLs and OCSP responses, with optional per-signature VRI entries. LTA adds
    document timestamps. Status is added incrementally after signing, by any party.
  - *Tessera.* The same gap as CAdES. PAdES's incremental augmentation is the model for how a holder
    could add status after shipping. Tessera's only post-ship additions are the TLR and wrappers.
- **ETSI EN 319 102-1 (signature validation procedures).**
  - *What it does.* It separates basic validation, validation with time (the signature timestamp as
    proof of existence, POE) and validation with long-term data. The last includes **past-signature
    validation**, which checks the chain and revocation status *at the POE time* rather than now.
  - *Outcomes.* It reports TOTAL-PASSED / TOTAL-FAILED / INDETERMINATE, with sub-indications
    such as `REVOKED_NO_POE`, `TRY_LATER` and `OUT_OF_BOUNDS_NO_POE` (from memory; check the exact list
    against the text).
  - *Tessera.* The three verdicts map almost one to one onto VALID / INVALID / UNVERIFIABLE. Tessera's
    interval rule (R-5.21, revocation compared against `anchor_time`) is a past-signature validation that
    uses the anchor as the POE. What it lacks is the revocation *data* and a "try later" sub-indication
    (P2-4).
- **RFC 4998 ERS (ASN.1) and RFC 6283 XMLERS (XML).**
  - *What they do.* An Evidence Record is a sequence of ArchiveTimeStampChains over a Merkle hash tree of
    data objects. Timestamp renewal happens before the TSA certificate or its algorithm weakens. Hash-tree
    renewal rehashes everything under a new hash algorithm. The material needed to validate each
    timestamp (certificates, CRLs) is to be stored with it before renewal (RFC 4998 §5;
    the exact placement is unverified).
  - *Tessera.* This is the closest analogue to Tessera's custodial renewal (R-7.1 claim 3, P7 wrappers).
    Tessera specifies no hash-tree renewal: everything rests on SHA-256 (PHASE2 l.262-263). It also has
    no rule for storing validation data for its own anchors and evidences at renewal time.

**What all five do that Tessera does not.** Each embeds the *status* evidence a later validator needs,
collected from live sources at augmentation time by some party, and then protected by a later
timestamp. Tessera forbids live and log sources at verification (R-5.10), but it never names an
augmentation-time collector. That is the root of G-27.

**Options for G-27, with what each requires of the models** (no recommendation):

- **(A) The verifier does not enforce revocation; the adjudicator does** (R-1.22 already lets the
  adjudicator use anything).
  - *P6 / R-5.21.* `VALID_STRICT` stops implying "not revoked in the window". That weakens a registered
    property, so it needs a signed amendment (A1 §A1.1).
  - *P6 in TLA+.* `revoked` leaves the verifier's predicate and moves to an adjudicator layer.
  - *Reporting.* `REV` is reported as "not evaluated by design" (R-5.33). The relying-party story says
    so.
  - *Other models.* The capstone and P9 are untouched.
- **(B) The bundle carries post-anchor revocation status, LTV-style.**
  - *A new statement.* Each channel signs "fp not revoked as of T" (or a revocation list), with T after
    `anchor_time`, and a later anchor proves T.
  - *Shared library.* It gains a statement form (a new signing domain in L-07 / D-1). The capstone and
    first-link gain a status check, with a severing companion.
  - *P6.* `revoked` gets a carrier and a freshness rule.
  - *P4.* It defines the verdict when status is absent (`UNVERIFIABLE`, like `REVOKED_NO_POE`).
  - *P8.* It encodes the statement.
  - *Augmentation.* The status is added after shipping, outside the signed bytes, so it must be
    self-authenticating. It is "late by construction", like the TLR, and needs a delivery path (G-51).
  - *P9.* Its inputs stay inside the bundle.
- **(C) A live or logged source.**
  - *Conflicts.* It conflicts with R-5.10 ("no live DNS … no third-party log") and with A4.6 ("a log …
    may never feed a verdict"). It breaks P9, because the verdict would depend on when the query is made.
  - *What it would take.* Amending R-5.10 and P9's inspection criterion, and modelling the verdict as a
    function of external state (P4, P9).
  - *Variant.* Confining the source to the adjudicator turns C into A.
