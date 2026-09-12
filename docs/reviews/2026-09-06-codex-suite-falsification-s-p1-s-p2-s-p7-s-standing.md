# Cross-family falsification reviews: S-P1, S-P2, S-P7, S-STANDING (Codex, gpt-6-astra)

The agreement-gate falsification review required by `formal/suite/ENUMERATION.md`
amendment note 5 item 1 (cross-family first) for the four suite models
built on 2026-09-06 from their frozen plans (`5188e7a`). Dispatched by
the AI collaborator the same evening under the author's standing
instruction that Codex runs when needed. Nothing here changes a query,
a prediction, or a property status. Dispositions are the collaborator's
and carry no authority until the author reads them; three items are
routed (`formal/suite/ROUTED-2026-09-06.md` C8–C10).

## Reproducibility record

- **Reviewer:** OpenAI Codex CLI 0.153.3, model `gpt-6-astra`
  (verified per run), four parallel runs, one per model family, with
  Codex's own sandbox bypassed so it could **run ProVerif on its own
  mutants and attack fixtures**. Jailing was by directory content:
  each run saw only that family's `.pv`/`.out` files, the shared
  library, the registered property text (Amendment 1; Amendment 3
  §A3.1 for P1's operative form and §A3.7 for standing), §A1.3, and
  the frozen plan (instructed to read it last).
- **Scale:** the reviewer ran 83 (S-P1), 256 (S-P2), 301 (S-P7) and
  101 (S-STANDING) scratch models — single-check mutants, attack
  fixtures, and audits — and built dependency matrices from them.
  Archived per family under
  `formal/suite/<family>/proverif/falsification-2026-09-06/`: the
  review, the prompt, the reviewer's `.pv` files and index/generator
  files. The reviewer's `.out` files (regenerable) were not archived;
  every RESULT line the review relies on is quoted in it.
- **Baselines:** in every family the reviewer re-ran the committed
  models and reproduced every committed RESULT line before mutating.
- **Not in the jails, material to several "uncovered" findings:** the
  sibling families. Several attack surfaces the reviewer calls
  unrepresentable in one family are the subject of another (signature
  sets → S-P2; byte encodings → P8; verdicts → P4; wrappers → S-P7).
  Dispositions say so; that is the coverage map's job, not a defect.

## Consolidated findings and collaborator dispositions

Labels as in the TLA+ record: **Accepted** (header/comment/results
text fix, collaborator work, no query changes); **Boundary** (true;
assigned to another leg or an existing Layer 2 residual; the reading
aid must say it); **Recorded** (a fact worth keeping, no action);
**ROUTED** (needs an author act).

### Common to all four families

1. **Signature-set operations (A1.3 item 2) are unrepresentable in
   S-P1, S-P7 and S-STANDING** — one signature slot each. **Boundary:**
   the signer set is S-P2's subject; S-P2 represents it at n ≤ 2
   (finding 12 below). Each family's reading aid names it.
2. **Byte-encoding attacks (non-canonical encodings, hash-input
   ambiguity, cross-kind parse confusion) are unrepresentable
   everywhere** — term equality stands in for byte equality; distinct
   constructors never confuse. **Boundary, already registered:** P8's
   injectivity obligation and the library's `h`/`fp` idealization
   (Layer 2). The reviewer's phrase "coverage failure, not an
   unreachable attack" is adopted into every family's header.
3. **No verdict values, waiver records, or policy inputs anywhere.**
   **Boundary, assigned:** P4's partition and the `Accept` ↔ P4
   cross-formalism join (author ruling 2026-08-29; coverage map).
4. **"Inert" checks.** In every family most verifier checks are inert
   *for the registered queries* — removing one changes no verdict —
   because the fixtures give each relation two routes, and because
   several checks exist for other properties' queries. The reviewer
   is careful and right that inert ≠ removable: single removals do not
   license joint removal, and inertness flips under composition
   (finding 22). **Accepted:** every "Load-bearing for these queries"
   header that names a check whose single removal is green is
   reworded to "load-bearing jointly with …" or moved to "carried",
   citing the reviewer's matrix line.
5. **The strict-mode honest-channel evidence check is individually
   inert in S-P1 and S-P7** (the manifest-hash and fingerprint pins
   carry the relation on their own). **Accepted** as a header
   correction; **Recorded** as defence in depth, the same shape as S-P3
   F5.
6. **Witnesses are existential.** Every N1 witness is reachable with a
   trace (all four families, all committed outputs), but reachability
   for one honest key does not establish it per branch or per key.
   **Recorded** in the suite rules: N1 is a vacuity guard, not
   coverage.

### S-P1

7. **Header lists "object type (P7); canonicalization version and
   algorithm profile (P8/H1a)" under "carried checks", but there are no
   such checks** — `ot` and `cv` are bound and never compared (the
   reviewer's A6 replays a wrapper-typed frame into the attestation
   verifier and it is accepted). **Accepted:** reworded as *signed
   fields carried as obligations for P7/P8*, not checks; S-P3's headers
   have the same wording and get the same fix.
8. **Composition break A8: a second honest signing endpoint under the
   same key that signs a payload-only message lets an attacker-chosen
   frame be accepted with no matching issuance event.** The reviewer
   is explicit that the added endpoint is *broken by construction* and
   that the original fixture is not falsified. **Recorded as a named
   assumption, entered in the ledger:** *key-use discipline* — an
   issuer key signs only framed objects under their domain tag, never
   raw payloads; this is the domain-separation design (P7) stated as
   an obligation on issuer code, and an H1a red-bar vector (an endpoint
   that signs unframed bytes must be rejected by the reference
   issuer). Not a query change.
9. **The frozen plan's sentence "A1.3 items 2–6 are present" overstates**
   (items 2 and 5, signature sets and anchoring, are absent). The plan
   is frozen; **Accepted** as a divergence entry in RESULTS.md, not an
   edit to the plan.
10. **Strict headers omit the manifest-destructuring dependency; the
    fingerprint dependency is now empirically red rather than
    inferred.** **Accepted**, header addendum citing the matrix.
11. **A5 (injective replay judge) returned "cannot be proved".**
    **Recorded:** inconclusive; injectivity is not a registered
    requirement (A3 §A3.1 registers the non-injective form).

### S-P2

12. **Two honest signers under one manifest can sign *different*
    framed payloads and the verifier accepts** (reviewer's
    `a_mixed_payload`, reachable, all four registered queries green).
    P2's registered text does not say the signers sign a *common*
    content; the frozen plan's exported sentence "a signature over the
    exact framed bytes from every signer" assumes it. **ROUTED (C8).**
    Recommendation: yes, P2 means one framed byte string signed by
    every required signer — the verifier gains an equality across
    signer slots and a companion that splices; a post-freeze query
    addition recorded as such. *On no:* the plan's sentence is
    corrected and the relying-party story says a multi-signer
    attestation is a set of per-signer attestations of possibly
    different bytes.
13. **`SetAltered` misfires on legitimate key reuse across manifests**
    (`a_key_reuse`): the fixture rule "one key, one manifest" is
    essential to reading the judge as "never signed". **Accepted:**
    the G header gains that qualifier; the judge is instrumentation,
    not a verifier check, and the reviewer says so.
14. **Attestation-signature checks are inert for S-P2's queries** —
    the judges inspect keys, manifests and frames without establishing
    signature issuance. **Boundary, assigned:** authorship is S-P1's
    correspondence (S-P3 F7, S-P1 ledger entry 4); the S-P2 header
    says the signature checks are carried for S-P1.
15. **Wrapper replay accepted** (`a_wrapper_replay`): object type is
    carried, not exercised. **Boundary:** S-P7's type judge; the
    S-P2 header already says so.
16. **An empty required set is unrepresentable in the grammar.**
    **Boundary, already registered:** A3 §A3.2 item 1's never-zero
    floor (also P10 probe O1).
17. **"the frame's fingerprint (Reattributed)" named load-bearing;
    its single removal is green in D/R/G** (the manifest-hash pin
    carries it; C3 without the hash shows it active). **Accepted** per
    finding 4.

### S-P7

18. **The wrapper's recorded inner canonicalization version is never
    checked against the inner frame's version** (`attack_version_lie`,
    reachable; the observer fires). P7 says the wrapper "records both
    inner and outer canonicalization versions"; nothing registered says
    the record must be *true*. **ROUTED (C9).** Recommendation: add
    the equality (recorded inner version = inner frame's version) as a
    verifier check with a lying-wrapper companion; a post-freeze query
    addition. *On no:* the record is informational and the reading aid
    says a wrapper's version record is unverified.
19. **Q2 header "the honest inner signature term is never *verified*
    under a key other than its signer's" is literally false** — the
    primitive verifies under a DSKS-derived key before the frame check
    rejects (`attack_dsks_checked`). **Accepted:** "never *accepted*".
20. **Q4 control header "exactly its standalone acceptance" exceeds
    the existential witnesses; Q6a "on EVERY wrapped acceptance"
    overstates.** **Accepted**, both narrowed.
21. **Self-containment: the embedded pair carries inner bytes and
    signature, but the inner manifest, evidence and possession are
    presenter-supplied outside it; no package-completeness query.**
    **Boundary, recorded as an open coverage cell** (P7 "the inner
    bytes must travel inside the bundle" / P9 self-containment) —
    bundle completeness is a P8/H1a format obligation, not a
    symbolic one.
22. **Q6b: restoring the omitted `Reattributed` query makes it red
    too.** **Recorded**; the companion's header lists the omission.

### S-STANDING

23. **Alias replay: a core issued under identity A, with its honest
    TLR, is accepted for standing under a second honestly published
    tuple naming the same key with identity B** (`a_alias_replay`,
    reachable, all registered queries green). The standing path binds
    the key to the *presented* tuple and never binds that tuple to the
    core's *embedded* tuple; the envelope path does. **ROUTED (C10).**
    Recommendation: the standing path checks the presented tuple
    against the core's embedded tuple — note 4 item 2's principle
    (no reliance on the envelope) applied to the tuple as it already
    is to the key — with an alias companion; post-freeze query
    addition. *On no:* standing is per key, not per identity, and the
    relying-party story must say an issuer with two identities on one
    key has one standing lineage.
24. **An honestly enrolled adversary-owned issuer falsifies the
    *unrestricted* event correspondence while both honest-key
    correspondences hold** (`a_own_registered_key`). **Boundary,
    expected:** an honestly registered issuer *is* an issuer; the
    unrestricted form is fixture-bound and the per-honest-key form is
    the claim (the S-P3/S-P1 pattern). The D/R headers say so.
25. **Terminal-disposition checks are safety-inert** (only the
    vocabulary witnesses depend on them); Q4's "LOAD-BEARING for the
    red: the removed terminal check" is a causal overclaim (the mutant
    also removes the per-entry check and changes fixtures).
    **Accepted:** D/R/G/Q4 headers reworded; the terminal check is
    load-bearing for the S2/S4 *vocabulary*, which is what SC-3
    registers.
26. **Q2's wrapper trace does not bind the inner value to the honest
    shipped core** — the exhibited transplant is onto a wrapper-shaped
    core with arbitrary contents. **Accepted:** the header narrows to
    what the trace shows; a stronger companion query binding the
    inner value to the honest core is added as an unregistered
    addition (S-P3 precedent) so the A7 ruling's literal transplant is
    exhibited, not inferred.
27. **The TLR domain tag is inert in the original fixture and
    load-bearing under composition** (`a_foreign_tag` + tag removal:
    red). **Recorded** in the library header (D-6): the tag's work is
    cross-protocol, invisible to any single-family model.
28. **`kT = kX` (presented key equals TLR key) is not required by any
    registered text.** **Recorded**; header says it is a fixture-shape
    restriction.
29. **Unrepresentable:** the combined report (standing alongside the
    P4 verdict for one request), policy non-rewriting, relying-party
    recording, temporal replay against the anchor. **Boundary,
    assigned:** the capstone (one request, both paths), P4, the
    relying-party story, and the A2.1 bridge respectively; A3 §A3.7's
    adjacent obligations (retention, handoff, delivery expiry,
    disclosure) were never this family's target and are listed as
    such in its reading aid.

## Net effect

No registered query, prediction, or verdict changes. Three design
questions surfaced by reachable attacks are routed (C8 common content
across signers; C9 verified version record; C10 tuple-to-core binding
in the standing path), each recommended as a small post-freeze check
with a companion. One named assumption enters the ledger (key-use
discipline). Roughly a dozen header sentences are narrowed. Under
ENUMERATION note 5 item 1, each family's *results* have now survived
cross-family scrutiny; each family's *self-description* did not, which
is the pattern S-P3 set and the outcome the gate exists to produce.
`checked` for P1, P2, P7 and the standing invariant waits on the
author's read of the narrowed headers (ROUTED C5).

---

## Reviewer output — verbatim

### Reviewer output — S-P1 (`model: gpt-6-astra`; scratch archived under `formal/suite/s-p1/proverif/falsification-2026-09-06/`)

## 1. Correspondence audit

**The largest gap is unrepresentable signature-set and byte-encoding attacks.** Each verifier accepts one `sg`; `ss` is uninterpreted, and canonical bytes are represented by a free `framed` constructor. A1.3 expressly permits signature-set operations and arbitrary byte alteration. (`A1.3-adversary.txt:5–12`; `proverif/sp1_q2_degraded_compromised.pv:110–121`; `tessera_theory.pvl:119–131`.)

Citation abbreviations expand to these exact files; `.out` replaces `.pv` when specified:

- **D** = `proverif/sp1_q1_strict_dns_compromised.pv`.
- **R** = `proverif/sp1_q1_strict_repo_compromised.pv`.
- **G** = `proverif/sp1_q2_degraded_compromised.pv`.
- **A** = `proverif/sp1_q3_companionA_sig_unbound.pv`.
- **B** = `proverif/sp1_q4_companionB_frame_unsigned.pv`.

**Licensing standard.** The property says: “There is no reachable state in which the verifier returns `VALID_STRICT` or `VALID_DEGRADED` for a package whose canonical bytes differ from bytes signed at issue time.” It also registers “existential issuance-event authenticity.” These license exact-byte binding and a non-injective issuance correspondence, without prescribing a particular authority/manifest algorithm. (`REGISTERED-PROPERTY.txt:1–4,15–21`.)

The following inventories every accepting-path check in **each** correct verifier. “Added” means not prescribed by the supplied property/adversary text, not forbidden. The frozen plan explicitly selects several such mechanisms. (`REGISTERED-PROPERTY.txt:1–27`; `A1.3-adversary.txt:1–16`; `PREDICTIONS-frozen.md:124–174`.)

| Check, including structural matches | D | R | G | License |
|---|---|---|---|---|
| Typed input: seven fields strict, six degraded; one `pkey`, one attestation signature | D:110–111 | R:110–111 | G:110–111 | Added wire/typing abstraction; singleton scope selected in `PREDICTIONS-frozen.md:130–133`. |
| DNS/sole evidence verifies under configured authority key; recovered pair contains `STMT_DIGEST` and exactly `h(t)` | D:113 | R:113 | G:112 | Added mechanism; channel threat licensed by `A1.3-adversary.txt:15–16`. |
| Repository evidence: same three conditions, independently checked | D:114 | R:114 | — | Added strict mechanism; selected in `PREDICTIONS-frozen.md:166–169`. |
| `t` decomposes as `authTuple(id,kfpr,ss,alg,ver)` | D:115 | R:115 | G:113 | Added manifest schema; `PREDICTIONS-frozen.md:134–135`. |
| Presented key fingerprint equals manifest `kfpr` | D:116 | R:116 | G:114 | Added key binding; `PREDICTIONS-frozen.md:139–142`. |
| Possession signature verifies under `kX`; recovered pair contains `POSS` and exactly `t` | D:117 | R:117 | G:116 | Added possession mechanism; `PREDICTIONS-frozen.md:136–138`; `tessera_theory.pvl:37–45`. |
| Attestation signature verifies under `kX`; recovered pair contains `BYTES` and exactly presented `fb` | D:119 | R:119 | G:118 | Exact-byte binding implements `REGISTERED-PROPERTY.txt:1–3,8–10,20–21`; tag/key-specific construction is an added realization. |
| `fb` decomposes as seven-field `framed`; frame algorithm equals manifest `alg` | D:120 | R:120 | G:120 | Added schema and identifier consistency, not algorithm suitability. |
| Frame issuer identity equals manifest `id` | D:120 | R:120 | G:120 | Added identifier consistency, not independently authenticated identity. |
| Frame fingerprint equals `fp(kX)` | D:120 | R:120 | G:120 | Added in-frame key binding. |
| Frame manifest hash equals `h(t)` | D:121 | R:121 | G:121 | Added in-frame manifest binding. |

The frame construction is selected in `PREDICTIONS-frozen.md:70–75,126–142`; none of its individual identifier comparisons is prescribed by `REGISTERED-PROPERTY.txt:1–27`.

**Judge filters are not verifier checks.** H matches acceptance to a privately enumerated honest key; N1 matches key and bytes to an issuance report. Neither restricts public acceptance. Each correct model enumerates two honest keys. (`D:125–148`; `R:125–148`; `G:140–163`.)

**Registered requirements without a corresponding check/discharge:**

- **Both valid verdicts:** no verdict variable, failure classification, or waiver check exists; only `Accept`/`AcceptS`. The frozen plan defers the join, but the supplied models do not discharge it. (`REGISTERED-PROPERTY.txt:1–3`; `D:109–123`; `R:109–123`; `G:109–123`; `PREDICTIONS-frozen.md:46–59,435–448`.)
- **Canonical-byte identity:** no serialization or canonicalization function, or encoding-injectivity obligation, is checked. Term equality substitutes for byte equality. (`REGISTERED-PROPERTY.txt:3,8–10`; `G:68–69,118–121`; `PREDICTIONS-frozen.md:113–117`; `tessera_theory.pvl:119–131`.)
- **All accepted packages:** G’s proved correspondence excludes adversary-held keys; its unrestricted query fails. The frozen plan argues the excluded cases do not violate P1, but this is not an all-keys issuance-event theorem. Self-signing explains the red query without demonstrating acceptance of unsigned altered bytes. (`REGISTERED-PROPERTY.txt:1–3,20–21`; `G:85–105,140–143`; `G.out:173,499`; `PREDICTIONS-frozen.md:94–112`.)
- **Signature-set operations:** “Strip, reorder, or duplicate signatures within the signature set” has no set representation or membership/completeness check. `ss` and `ver` are only destructured; one `sg` is verified. The P2 excerpt stops at “The canonical”, preventing reconstruction of its complete obligation. (`A1.3-adversary.txt:7`; `REGISTERED-PROPERTY.txt:6`; `D:110–121`; `R:110–121`; `G:110–121`.)
- **Wrappers, receipts, re-framing, anchoring:** no wrapper/receipt parser, anchor process, or interpretation of object type exists. Arbitrary payload terms do not encode those protocols. (`A1.3-adversary.txt:5–14`; `G:109–137`; `PREDICTIONS-frozen.md:450–456,492–502`.)
- **Channel subsets generally:** D/R cover either single compromise of two keys, not arbitrary channel counts. G exposes its only authority key—a stronger exposure than a proper subset of a one-channel universe. An unavailable honest channel or waiver is not represented. (`A1.3-adversary.txt:15–16`; `D:136–147`; `R:136–147`; `G:152–162`; `PREDICTIONS-frozen.md:166–182`.)

Replay prevention and semantic truth are **not missing requirements**: “Re-presenting a genuinely issued package preserves identity; P1 permits it”; meaning and truth are outside the attestation. Object-type/profile validation is also not required by this supplied P1 text, although the headers call those carried checks. (`REGISTERED-PROPERTY.txt:11–21`; `D:42–47`; `R:42–47`; `G:40–46`.)

## 2. Attacks

**UNREPRESENTABLE:** stripping/reordering/duplicating a genuine multi-signature package, or changing concrete encodings while preserving a symbolic frame, cannot be tested against these unchanged verifiers. Encoding signatures as a tuple inside `sg` merely makes `checksign` fail; placing them inside payload never checks set semantics. This is a coverage failure, not an unreachable attack. (`A1.3-adversary.txt:5–12`; `G:110–121`; `tessera_theory.pvl:98–104`; `PREDICTIONS-frozen.md:113–133`.)

All attack fixtures preserve G’s verifier byte-for-byte; the generator asserts this. A1–A4 use three honest parties and fixed honest payloads, so those parties never sign the target altered payload. Target reports run in parallel with protocol processes. (`scratch/build_attacks.py:72–78`; `scratch/a1_payload_tamper.pv:152–195`.)

| Attempt and concrete target | Outcome and exact RESULT |
|---|---|
| **A1 payload substitution:** replace `goodPayload` with `alteredPayload`, retaining honest key and binding fields; the original signature is available. (`scratch/a1_payload_tamper.pv:181–195`.) | **Unreachable:** `RESULT not event(Attack) is true.` (`scratch/a1_payload_tamper.out:582`.) |
| **A2 extra-party swap:** present the first issuer’s frame under the third honest issuer’s key. (`scratch/a2_party_swap.pv:177–195`.) | **Unreachable:** `RESULT not event(Attack) is true.` (`scratch/a2_party_swap.out:583`.) |
| **A3 DSKS replay:** derive `dsks(observed,dsksSalt)` after an honest signature; try that key with the original frame. Signature verification is possible, but the frame fingerprint cannot equal the derived key’s fingerprint. (`scratch/a3_dsks_replay.pv:181–188`; `G:120`; `tessera_theory.pvl:99–117`.) | **Unreachable:** `RESULT not event(Attack) is true.` (`scratch/a3_dsks_replay.out:585`.) |
| **A4 DSKS re-signing:** sign an altered payload using the held derived key, a consistent new frame, attacker-chosen signer-set term, and forged sole-channel evidence. This changes the key and signs the new bytes; it does not break honest-key P1. (`scratch/a4_dsks_resign.pv:181–195`.) | **Reachable:** `RESULT not event(Attack) is false.` A trace is found; the headline remains true. (`scratch/a4_dsks_resign.out:242,782–783`.) |
| **A6 foreign type/version:** add honest issuance of `OT_WRAPPER` with `badVersion`, then present it to unchanged G. Both fields are accepted without interpretation. This is unchanged signed-byte replay, not a P1 counterexample. (`scratch/a6_foreign_type.pv:153–160,188–195`; `G:120`.) | **Reachable:** `RESULT not event(Attack) is false.` (`scratch/a6_foreign_type.out:746–747`.) |
| **A7 cross-model replay:** copy Q1’s issuer body, sharing its terms/key with G, and submit its signed frame to the degraded verifier. No mode/context appears in the frame. (`scratch/a7_cross_mode.pv:161–170,189–205`; `D:98–106`.) | **Reachable:** `RESULT not event(Attack) is false.` Permitted replay, not P1 failure. (`scratch/a7_cross_mode.out:746–747`; `REGISTERED-PROPERTY.txt:15–21`.) |

A1–A4 exercise alteration, substitution and self-signing capabilities in `A1.3-adversary.txt:5–10`; A6/A7 exercise the replay boundary in `A1.3-adversary.txt:11–12`. All retain G’s registered exposed evidence key. (`scratch/a4_dsks_resign.pv:185–195`.)

**Conditional composition break (A8):** add B’s payload-only signing endpoint under the same honest key. Ask it to sign a complete attacker-chosen inner frame as payload; replay that signature to correct G. B emits `IssuerSigned` for the outer frame, while G accepts the inner frame without a matching issuance event. (`scratch/a8_cross_broken_endpoint.pv:161–169,198–206`; `scratch/a8_cross_broken_endpoint.out:919–948`.)

`RESULT event(AcceptedUnderHonestKey(k,fb_5)) ==> event(IssuerSigned(k,fb_5)) is false.` (`scratch/a8_cross_broken_endpoint.out:428`.)

`RESULT not event(Attack) is false.` (`scratch/a8_cross_broken_endpoint.out:948`.)

This falsifies unrestricted composition of the correspondence, **not the original correct fixture under A1.3**: the added endpoint is explicitly broken. The accepted inner bytes have a valid honest-key signature; the mismatch concerns the endpoint’s issuance record. Same-key cross-protocol signing behavior therefore needs an explicit composition assumption. (`B:18–28`; `scratch/a8_cross_broken_endpoint.pv:161–169`; `scratch/a8_cross_broken_endpoint.out:925–935`.)

**Unresolved A5:** a judge demanding two identical acceptance reports returned `RESULT not event(Attack) cannot be proved.` Explicit verifier copies and an injectivity diagnostic also failed to reconstruct a trace. This is **inconclusive**, not reachable or unreachable; injectivity is not a registered freshness requirement. (`scratch/a5_repeat_replay_uncertain.out:688–689`; `scratch/a5_repeat_replay.out:736–737`; `scratch/a5_injective_diagnostic.out:800–802,1249–1250`; `REGISTERED-PROPERTY.txt:15–21`.)

**Review correction:** initial attack harnesses put a private target output before starting its receiver, blocking execution. Their inconclusive outputs remain under `scratch/initial/` and are not attack evidence. Corrected fixtures place that output in parallel. (`scratch/initial/a4_dsks_resign.pv:188–195`; `scratch/initial/a4_dsks_resign.out:819`; `scratch/a4_dsks_resign.pv:188–195`.)

## 3. Mutations

Each mutant starts from its original correct model and removes/unbinds one check. Whole signature/evidence removals are distinguished from individual key, tag and message equalities. `tuple_binding` replaces the manifest pattern with attacker-supplied fields. `frame_binding` removes the compound frame pattern, retaining independently supplied `mh` for the later hash check. Those two are compound-pattern ablations, not single-field ablations. (`scratch/build_mutants.py:4–35`; `scratch/m_D_poss_key.pv:118–119`.)

Entries are **H/U/N**: honest-key correspondence / unrestricted correspondence / honest witness. **T** = correspondence true; **F** = correspondence false; **r** = witness reachable. Citations span the three RESULT lines. Mutant filenames are the cited output filename with `.pv` substituted. Query definitions: `D:78–88`; `R:78–88`; `G:85–105`.

| Removed/unbound check | D: H/U/N | R: H/U/N | G: H/U/N |
|---|---|---|---|
| `evD` | **T/T/r** (`scratch/m_D_evD.out:198–380`) | **T/F/r** (`scratch/m_R_evD.out:349–540`) | — |
| `evD_tag` | **T/T/r** (`scratch/m_D_evD_tag.out:201–396`) | **T/T/r** (`scratch/m_R_evD_tag.out:201–396`) | — |
| `evD_digest` | **T/T/r** (`scratch/m_D_evD_digest.out:201–399`) | **T/F/r** (`scratch/m_R_evD_digest.out:357–552`) | — |
| `evD_key` | **T/T/r** (`scratch/m_D_evD_key.out:205–390`) | **T/F/r** (`scratch/m_R_evD_key.out:366–567`) | — |
| `evR` | **T/F/r** (`scratch/m_D_evR.out:349–540`) | **T/T/r** (`scratch/m_R_evR.out:198–380`) | — |
| `evR_tag` | **T/T/r** (`scratch/m_D_evR_tag.out:201–396`) | **T/T/r** (`scratch/m_R_evR_tag.out:201–396`) | — |
| `evR_digest` | **T/F/r** (`scratch/m_D_evR_digest.out:357–552`) | **T/T/r** (`scratch/m_R_evR_digest.out:201–399`) | — |
| `evR_key` | **T/F/r** (`scratch/m_D_evR_key.out:366–567`) | **T/T/r** (`scratch/m_R_evR_key.out:205–390`) | — |
| `ev` | — | — | **T/F/r** (`scratch/m_G_ev.out:170–470`) |
| `ev_tag` | — | — | **T/F/r** (`scratch/m_G_ev_tag.out:173–499`) |
| `ev_digest` | — | — | **T/F/r** (`scratch/m_G_ev_digest.out:173–505`) |
| `ev_key` | — | — | **T/F/r** (`scratch/m_G_ev_key.out:174–515`) |
| `tuple_binding` | **T/F/r** (`scratch/m_D_tuple_binding.out:387–601`) | **T/F/r** (`scratch/m_R_tuple_binding.out:387–601`) | **T/F/r** (`scratch/m_G_tuple_binding.out:173–523`) |
| `fp` | **T/F/r** (`scratch/m_D_fp.out:362–559`) | **T/F/r** (`scratch/m_R_fp.out:362–559`) | **T/F/r** (`scratch/m_G_fp.out:171–500`) |
| `possession` | **T/T/r** (`scratch/m_D_possession.out:199–380`) | **T/T/r** (`scratch/m_R_possession.out:199–380`) | **T/F/r** (`scratch/m_G_possession.out:171–473`) |
| `poss_tag` | **T/T/r** (`scratch/m_D_poss_tag.out:201–396`) | **T/T/r** (`scratch/m_R_poss_tag.out:201–396`) | **T/F/r** (`scratch/m_G_poss_tag.out:173–499`) |
| `poss_manifest` | **T/T/r** (`scratch/m_D_poss_manifest.out:201–396`) | **T/T/r** (`scratch/m_R_poss_manifest.out:201–396`) | **T/F/r** (`scratch/m_G_poss_manifest.out:173–502`) |
| `poss_key` | **T/T/r** (`scratch/m_D_poss_key.out:203–401`) | **T/T/r** (`scratch/m_R_poss_key.out:204–402`) | **T/F/r** (`scratch/m_G_poss_key.out:175–514`) |
| `signature` | **F/F/r** (`scratch/m_D_signature.out:340–679`) | **F/F/r** (`scratch/m_R_signature.out:340–679`) | **F/F/r** (`scratch/m_G_signature.out:314–619`) |
| `sig_tag` | **T/T/r** (`scratch/m_D_sig_tag.out:201–396`) | **T/T/r** (`scratch/m_R_sig_tag.out:201–396`) | **T/F/r** (`scratch/m_G_sig_tag.out:173–499`) |
| `sig_bytes` | **F/F/r** (`scratch/m_D_sig_bytes.out:357–725`) | **F/F/r** (`scratch/m_R_sig_bytes.out:357–725`) | **F/F/r** (`scratch/m_G_sig_bytes.out:331–663`) |
| `sig_key` | **F/F/r** (`scratch/m_D_sig_key.out:365–738`) | **F/F/r** (`scratch/m_R_sig_key.out:365–738`) | **F/F/r** (`scratch/m_G_sig_key.out:338–677`) |
| `frame_binding` | **T/T/r** (`scratch/m_D_frame_binding.out:202–400`) | **T/T/r** (`scratch/m_R_frame_binding.out:202–400`) | **T/F/r** (`scratch/m_G_frame_binding.out:173–489`) |
| `frame_alg` | **T/T/r** (`scratch/m_D_frame_alg.out:201–396`) | **T/T/r** (`scratch/m_R_frame_alg.out:201–396`) | **T/F/r** (`scratch/m_G_frame_alg.out:173–502`) |
| `frame_id` | **T/T/r** (`scratch/m_D_frame_id.out:201–396`) | **T/T/r** (`scratch/m_R_frame_id.out:201–396`) | **T/F/r** (`scratch/m_G_frame_id.out:173–502`) |
| `frame_fp` | **T/T/r** (`scratch/m_D_frame_fp.out:201–396`) | **T/T/r** (`scratch/m_R_frame_fp.out:201–396`) | **T/F/r** (`scratch/m_G_frame_fp.out:173–502`) |
| `manifest_hash` | **T/T/r** (`scratch/m_D_manifest_hash.out:199–394`) | **T/T/r** (`scratch/m_R_manifest_hash.out:199–394`) | **T/F/r** (`scratch/m_G_manifest_hash.out:171–500`) |

**Inert for all three registered queries:** in D/R, compromised evidence and its key/tag/digest equalities; honest-evidence tag alone; possession and its equalities; signature tag alone; frame binding/individual fields; manifest hash. In G, everything tested except whole attestation verification and its byte/key equalities is inert. “Inert” means unchanged query outcomes, not unchanged acceptance behavior; G’s unrestricted query was already false. (Matrix; baselines `D.out:201–396`; `R.out:201–396`; `G.out:173–499`.)

**Why:** under an honest accepted key, signature-byte/key binding forces a signature released by an issuance process. Other signatures under honest issuer keys cover `POSS` and `authTuple`, so removing `BYTES` cannot supply a signature over a `framed` message. Honest authority keys sign only `STMT_DIGEST`, making its tag separately inert. Unrestricted strict acceptance additionally depends on honest-authority key/digest binding, tuple binding and the manifest fingerprint to exclude attacker-held keys. (`D:90–121,136–147`; `R:90–121,136–147`; `G:129–137`; `tessera_theory.pvl:98–104`; matrix.)

The strict headers omit the manifest-destructuring dependency. Their fingerprint dependency is now empirically red rather than merely inferred. Single-removal experiments do not establish that several inert checks can safely be removed together. (`D:34–47`; `R:34–47`; `scratch/m_D_fp.out:362`; `scratch/m_R_fp.out:362`; `scratch/m_D_tuple_binding.out:387`; `scratch/m_R_tuple_binding.out:387`.)

## 4. Vacuity

The committed outputs contain a derivation **and a reconstructed trace** for every declared N1 witness. Each has the exact result `RESULT not event(HonestAccepted(k,fb_3)) is false.` (`D:86–88`; `R:86–88`; `G:88–90`; `A:56–58`; `B:53–55`.)

| Model | Derivation starts | Witness trace/event | RESULT |
|---|---|---|---|
| D | D.out:215 | D.out:392–395 | D.out:396 |
| R | R.out:215 | R.out:392–395 | R.out:396 |
| G | G.out:180 | G.out:345–348 | G.out:349 |
| A | A.out:338 | A.out:506–509 | A.out:510 |
| B | B.out:335 | B.out:500–503 | B.out:504 |

**Companion selectivity:** A and B each change the named honest-key correspondence from G’s true to false. Their unrestricted query was already false in G; N1 stays reachable. Thus exactly one correspondence changes relative to G, but each companion has **two false correspondences**, not one. (`G.out:173,349,499`; `A.out:331,510,663`; `B.out:328,504,654`; `A:18–34,66–68`; `B:15–31,63–65`.)

A’s trace records an honest frame with payload `a_2`, then accepts a different frame with type `a_4`, version `a_5` and payload `a_6`. It is not a request to sign the accepted frame. B preserves payload `a_2` but changes type/version; its issuance event reports the intended frame while its signature covers payload only. (`A.out:315–331`; `B.out:312–328`; `B:18–23`.)

N1 is existential, not coverage of every issuer or payload: all committed witness traces use `skI2`. Reachability excludes total deadness but does not establish branch-by-branch non-vacuity. (`D:87–88`; `R:87–88`; `G:89–90`; `D.out:392`; `R.out:392`; `G.out:345`; `A.out:506`; `B.out:500`.)

## 5. Verdict on each header’s honesty

- **D:** its core “This model proves” statement matches the two proved symbolic correspondences within the fixed producer fixture. It does not discharge unrestricted canonical-byte P1; its scope exclusions acknowledge verdicts, multi-signers and encoding. (`D:16–33`; `D.out:201–208`; `REGISTERED-PROPERTY.txt:1–3`.)
- **R:** same verdict, supported independently by its committed results and mutations. The load-bearing authority role reverses correctly. (`R:16–41`; `R.out:201–208`; `scratch/m_R_evD.out:349`; `scratch/m_R_evR.out:198`.)
- **G:** “framed bytes accepted under an honest issuer’s key are exactly the bytes that issuer signed at an issuance event” accurately states its conditional query. Calling this “the [model] binding half of P1” must retain the honest-key, term-equality and closed-producer qualifications; the all-keys contrast is false and composition A8 fails. (`G:18–33`; `G.out:173,499`; `scratch/a8_cross_broken_endpoint.out:428`; `PREDICTIONS-frozen.md:94–117`.)
- **A:** “This model exists to go RED on the headline” and “It discharges nothing” match the outputs. Its corrected field description matches the trace; the earlier payload-only description remains as a visible correction note. (`A:18–34,119–135`; `A.out:315–331`.)
- **B:** “It discharges nothing. It proves nothing about P1” is consistent with this deliberately broken producer/verifier pair. `IssuerSigned` describes intended framing, not the actual payload-only signature message; the red result concerns that explicit mutation. (`B:15–31,85–93`; `B.out:312–328`.)

**Verbatim inventory overclaims:** D/R list “object type (P7); canonicalization version and algorithm profile (P8/H1a)” under “Carried checks”; G similarly lists “object type (P7); canonicalization version and algorithm profile (P8/H1a)”. There are no such validation checks: `ot`/`cv` are unconstrained, and `alg` is merely compared with the manifest identifier. These are signed fields or external obligations, not carried validation checks. (`D:42–47,120`; `R:42–47,120`; `G:40–46,120`; `scratch/a6_foreign_type.out:747`.)

**Verbatim adversary overclaim in the frozen plan:** “items 2–6 are present” is false for signature-set operations and anchoring, and overstates semantic cross-type/context coverage. Those attacks lack corresponding state or parsers here. The headers’ narrower DSKS claim is supported by the library and A3/A4 probes; it does not repair these omissions. (`PREDICTIONS-frozen.md:160–162`; `A1.3-adversary.txt:7–16`; `G:109–137`; `tessera_theory.pvl:99–104`; `scratch/a3_dsks_replay.out:585`; `scratch/a4_dsks_resign.out:783`.)
### Reviewer output — S-P2 (`model: gpt-6-astra`; scratch archived under `formal/suite/s-p2/proverif/falsification-2026-09-06/`)

## 1. Correspondence audit

**The models do not discharge all of P2.** The unchanged strict verifier accepts signatures over different payloads without triggering any original safety query. The `SetAltered` judge also misclassifies legitimate reuse of a key across manifests. (`scratch/a_mixed_payload.out:603–635`; `scratch/a_key_reuse.out:642–654`)

File aliases below refer to `proverif/`:

| Alias | Filename stem |
|---|---|
| D | `sp2_q1_strict_dns_compromised` |
| R | `sp2_q1_strict_repo_compromised` |
| G | `sp2_q2_degraded_compromised` |
| Q3 | `sp2_q3_companion_cardinality_ignored` |
| Q4 | `sp2_q4_companion_slot_unbound` |
| C1 | `sp2_q5_c1_fponly_frame_mh` |
| C2 | `sp2_q5_c2_fponly_frame_nomh` |
| C3 | `sp2_q5_c3_manifestposs_frame_nomh` |

Thus `G.pv:163` means `proverif/sp2_q2_degraded_compromised.pv:163`.

The supplied registration says:

> “The canonical signed bytes commit to the required-signer manifest.” (`REGISTERED-PROPERTY.txt:1–2`)

> “A package presenting fewer signatures than its manifest requires yields `INVALID` — never `VALID_STRICT`, and `VALID_DEGRADED` only under an explicit, recorded policy within the waivable set of A1.2.1.” (`REGISTERED-PROPERTY.txt:2–5`)

> “Consequence: "issued with one signature" and "issued with two, one stripped" are distinguishable by construction, because the expected set is inside what every signature signs.” (`REGISTERED-PROPERTY.txt:5–8`)

The supplied P3 text ends at “Acceptance binds each”; its missing continuation cannot license additional requirements. (`REGISTERED-PROPERTY.txt:10`)

Every verifier check is catalogued below. “Licensed” means implementing supplied P2 text, not that P2 mandates this particular encoding. D and R have identical verifier lines; C3 is included because its header makes a positive sufficiency claim. (`D.pv:134–176`; `R.pv:134–176`; `G.pv:157–195`; `C3.pv:122–157`)

| Check, including implicit pattern checks | D/R `.pv` lines | G `.pv` lines | C3 `.pv` lines | License / limitation |
|---|---|---|---|---|
| Fixed input tuple arity; typed keys and byte fields | 136–137,155–157 | 159–160,176–178 | 124–125,140–142 | Representation choice; P2 specifies no wire grammar. |
| Authority signature verification | 139–140,159–160 | 161,179 | 126,143 | Additional authority mechanism, not prescribed by supplied P2. |
| Authority message pair, `STMT_DIGEST` tag, exact `h(t)` | same | same | same | Additional authority binding; not itself the required-signer signature commitment. |
| Five-field `authTuple`; `signers0` for one slot, `signers1(kfprB)` for two | 142,162 | 163,181 | 128,145 | Implements required cardinality from manifest; positional grammar and bound are assumptions. |
| Each supplied key fingerprint equals its manifest slot | 143,163–164 | 164,182–183 | 129,146–147 | Implements required **signer** membership; assumes ideal fingerprints. |
| Each possession signature verifies under its slot key | 144,165–166 | 165,184–185 | 130,148–149 | Additional proof object; P2 does not require separate possession signatures. |
| Possession message pair, `POSS` tag, exact manifest `t` | same | same | same | Additional manifest commitment; does not alone place the manifest inside attestation signed bytes. |
| Each attestation signature verifies under its slot key | 145,167–168 | 166,186–187 | 131,150–151 | Licensed by “signatures” and “what every signature signs.” |
| Attestation message pair, `BYTES` tag, exact presented frame | same | same | same | Exact message binding implements P2; particular tag is additional. |
| Frame constructor and arity | 146,169,171 | 167,188,190 | 132,152–153 | Representation assumption; C3 has six fields instead of seven. |
| Frame algorithm equals manifest algorithm | same | same | same | Additional consistency check, absent from supplied P2; no allowed-algorithm check. |
| Frame issuer equals manifest issuer | same | same | same | Additional consistency check, absent from supplied P2. |
| Frame fingerprint equals verifying-key fingerprint | same | same | same | Supports key binding; duplicate binding in this precise location is not mandated by P2. |
| Frame manifest hash equals `h(t)` | 147,170,172 | 168,189,191 | **Absent** | Direct signed-byte commitment, conditional on ideal hashing and encoding. |

The licensing comparator is `REGISTERED-PROPERTY.txt:1–8`. A1.3 permits channel compromise but does not prescribe an authority verifier. Fingerprint equality is ideal key equality; `h` has neither collisions nor byte-encoding structure. (`A1.3-adversary.txt:15–16`; `tessera_theory.pvl:106–131`)

Registered requirements lacking a check or complete query:

- **Canonical signed bytes:** no canonicalization validation; `cva/cvb` are merely bound. Noncanonical encodings and hash-input ambiguity are absent from the algebra. (`REGISTERED-PROPERTY.txt:1–2`; `G.pv:167–191`; `tessera_theory.pvl:119–131`)
- **Required verdict and recorded waiver:** no verdict events, policy input, waiver record, or waiver-membership check. Failure stops a process; no query establishes `INVALID` rather than another outcome. (`REGISTERED-PROPERTY.txt:2–5`; `G.pv:107–132,158–195`; `D.pv:81–105,135–176`)
- **General signature-set completeness:** only one/two-slot acceptance exists. `Stripped` specifically detects a registered two-slot manifest accepted through `verified1`; it does not count arbitrary signature collections. (`REGISTERED-PROPERTY.txt:2–8`; `G.pv:81–86,201–214,237–248`)
- **Commitment inside every attestation signature:** D/R/G check this syntactically, but no query establishes an acceptance-to-issuance correspondence for those bytes. C3 omits the frame commitment entirely while preserving `SetAltered`. (`REGISTERED-PROPERTY.txt:1–2,7–8`; `G.pv:114–132`; `C3.pv:117–119,130–132,148–153`)
- **Common content across signer slots:** payloads, canonicalization versions and object types are not compared. P2 does not expressly define that relation; the frozen plan’s stronger “exact framed bytes from every signer” claim requires qualification and fails if interpreted as common attestation content. (`G.pv:176–195`; `PREDICTIONS-frozen.md:537–546`; `scratch/a_mixed_payload.out:603–611`)

The safety queries are bad-event reachability queries, not issuance correspondences. `SignerForged` observes wrong-key use against a matching honest record; `SetAltered` means “different from this record’s manifest,” not “never signed”; `Reattributed` compares identical honest and accepted frames. Authorship is expressly excluded. (`G.pv:114–124,220–233,35–37`)

## 2. Attacks

All seven fixtures preserve D’s verifier checks and authority setup: DNS compromised, repository honest. Additional `Attack` events observe acceptance without gating it. The adversary supplies packages through the existing public inputs. Each `.pv` and matching `.out` remains under `scratch/`. (`D.pv:135–176,216–230`; `scratch/check.py:17–24`; `A1.3-adversary.txt:5–16`)

| Concrete attempt | Fixture | Outcome and exact RESULT |
|---|---|---|
| **Splice payloads:** combine A2’s signature for X and B2’s for Y, X ≠ Y, both under M2, with possession proofs and honest repository evidence. | `scratch/a_mixed_payload.pv:177`; acceptance derivation at `.out:603–610` | **Reachable:** `RESULT not event(Attack) is false.` (`scratch/a_mixed_payload.out:611`) |
| **Duplicate a signature:** put the identical key/signature into both M2 positions. | `scratch/a_duplicate_signature.pv:177` | **Unreachable:** `RESULT not event(Attack) is true.` (`scratch/a_duplicate_signature.out:392`) |
| **Reorder presentations:** put B2 first and A2 second, retaining the manifest. | `scratch/a_reordered_keys.pv:177` | **Unreachable:** `RESULT not event(Attack) is true.` (`scratch/a_reordered_keys.out:392`) |
| **DSKS substitution:** derive `dsks(sB,fbH)` from B2’s honest signature on a public payload; try its public key in slot B. | `scratch/a_dsks.pv:177`; capability at `tessera_theory.pvl:99–104` | **Unreachable:** `RESULT not event(Attack) is true.` (`scratch/a_dsks.out:392`) |
| **Shrink M2:** change its required set to `signers0`, retain A2’s key, replay honest material and forge DNS evidence. | `scratch/a_shrink.pv:152` | **Unreachable:** `RESULT not event(Attack) is true.` (`scratch/a_shrink.out:392`) |
| **Reuse an honest key:** add honestly published M3 with a different version; A1 signs both M1 and M3; replay valid M1 material. | `scratch/a_key_reuse.pv:221–227` | **Reachable judge alarm:** `RESULT not event(SetAltered(kH_2,m,t_2)) is false.` (`scratch/a_key_reuse.out:654`) |
| **Cross-type replay:** add an honest wrapper-signing producer using the shared frame and `OT_WRAPPER`; present its output to the attestation verifier. | `scratch/a_wrapper_replay.pv:137–146,163,242` | **Reachable:** `RESULT not event(Attack) is false.` (`scratch/a_wrapper_replay.out:588`) |

Mixed-payload and wrapper acceptance leave all four original safety queries green. These are accepted packages outside what the judges observe, not counterexamples to their literal unreachability results. Object type is explicitly carried rather than exercised. (`scratch/a_mixed_payload.out:617–635`; `scratch/a_wrapper_replay.out:594–612`; `G.pv:46–50`)

Key reuse is a **false positive, not forgery**. The accepted M1 was honestly signed. `MemberJudge` pairs acceptance with A1’s M3 report and fires because M1 ≠ M3. The fixture restriction “one key, one manifest” is essential to interpreting this event as “never signed.” (`scratch/a_key_reuse.out:638–654`; `G.pv:142–145,220–226`)

**UNREPRESENTABLE — the most important coverage boundary:** two distinct noncanonical byte encodings of the same abstract required set cannot be expressed. There are no raw manifest encodings or canonicalization operations. A semantic empty required set likewise has no representation in the accepted grammar. Rejection of these attacks has **no established RESULT**. Predictions acknowledge the exclusions, but that does not discharge “canonical signed bytes.” (`tessera_theory.pvl:119–131,159–164`; `G.pv:81–86,163,181`; `PREDICTIONS-frozen.md:95–109,119–126,593–595`; `REGISTERED-PROPERTY.txt:1–2`)

The reorder run tests swapping positional package slots, not equivalence of reordered set encodings. The wrapper run tests an added producer, not composition with an unavailable S-P7 model. (`scratch/a_reordered_keys.pv:177`; `scratch/a_wrapper_replay.pv:137–146`; `PREDICTIONS-frozen.md:119–126`)

## 3. Mutations

I ran **169 independent single-check mutants**: D 46, R 46, G 40, C3 37. Each changes one source occurrence, preserving producers and judges. Every corrected run terminates with seven RESULT lines; both `HonestComplete` witnesses and `HonestAccepted` remain reachable. The complete per-run matrix includes every output location. (`scratch/dependencies.tsv:2–170`; `scratch/check.py:25–29`)

**S/F/A/K** below mean unreachability of `Stripped`, `SignerForged`, `SetAltered`, and `Reattributed`. “All” means all four survive. Every listed source line denotes a separate run; D/R denotes independent runs in both models. Files are `scratch/m_<model>_<source-line>_<operation>.pv`, with matching `.out`. (`scratch/build.py:4–32`; `scratch/dependencies.tsv:1–170`)

| Single removal/unbinding | D/R source lines → surviving queries | G source lines → surviving queries | C3 source lines → surviving queries |
|---|---|---|---|
| `arity`: unbind `=signers0` | 142 → F,A,K | 163 → F,A,K | 128 → F,A,K |
| `drop`: slot fingerprint equality | 143,163,164 → S,A,K | 164,182,183 → S,A,K | 129,146,147 → S,A,K |
| `drop`: entire authority check | 139,140,159,160 → All | 161,179 → All | 126,143 → All |
| `tag`: authority `STMT_DIGEST` | 139,140,159,160 → All | 161,179 → All | 126,143 → All |
| `binding`: authority digest | 139,140,159,160 → All | 161,179 → All | 126,143 → All |
| `drop`: entire possession check | 144,165,166 → All | 165,184,185 → All | 130,148,149 → S,F,K |
| `tag`: possession `POSS` | 144,165,166 → All | 165,184,185 → All | 130,148,149 → All |
| `binding`: possession manifest | 144,165,166 → All | 165,184,185 → All | 130,148,149 → S,F,K |
| `drop`: entire attestation check | 145,167,168 → All | 166,186,187 → All | 131,150,151 → All |
| `tag`: attestation `BYTES` | 145,167,168 → All | 166,186,187 → All | 131,150,151 → All |
| `binding`: signature-to-frame equality | 145,167,168 → All | 166,186,187 → All | 131,150,151 → All |
| `alg`: frame algorithm equality | 146,169,171 → All | 167,188,190 → All | 132,152,153 → All |
| `id`: frame issuer equality | 146,169,171 → All | 167,188,190 → All | 132,152,153 → All |
| `fp`: frame fingerprint equality | 146,169,171 → All | 167,188,190 → All | 132,152,153 → S,F,A |
| `drop`: frame manifest-hash equality | 147,170,172 → All | 168,189,191 → All | Absent |

Evidence for every matrix cell: D `scratch/dependencies.tsv:2–47`; R `:48–93`; G `:94–133`; C3 `:134–170`. Each row identifies all seven RESULT locations. Representative red results: `scratch/m_D_142_arity.out:564`; `scratch/m_G_183_drop.out:601`; `scratch/m_C3_130_binding.out:535`; `scratch/m_C3_132_fp.out:545`.

**Inert** means unchanged query outcomes under one removal, not unchanged acceptance behavior:

- **Authority checks are inert for these queries.** Compromised evidence is forgeable; removing an honest channel check leaves other signature/set constraints. This is query-relative redundancy, not evidence that authority is unnecessary. (`scratch/dependencies.tsv:2–7,19–24,94–96`; `D.pv:139–147,159–172,223`)
- **Possession and frame-hash checks are individually inert in D/R/G.** Each retains a manifest commitment when the other is removed. C3 exposes possession as active after omitting the frame commitment. (`scratch/dependencies.tsv:99–102,108,116–121,134–170`; `C1.out:366`; `C2.out:535`; `C3.out:363`)
- **All attestation-signature checks, tags and signature/frame equalities are inert.** Judges inspect reported keys, manifests and frames without establishing signature issuance; possession still constrains honest-key use. This is a measurement gap for “signatures,” although the original verifier checks them. (`G.pv:165–172,184–195,201–233`; `scratch/dependencies.tsv:102–104,122–127`)
- **Frame algorithm and issuer equalities are inert.** Object type and canonicalization version have no equality checks to remove. (`scratch/dependencies.tsv:105–107,128–132,165–170`; `G.pv:167–191`)
- **Frame fingerprint equality is inert in D/R/G.** The retained signed manifest hash and slot match pin the key when replaying identical honest bytes. C3 lacks that hash, and its fingerprint ablations expose reattribution. (`scratch/m_G_190_fp.out:372`; `scratch/m_C3_153_fp.out:598`; `G.pv:181–191`)

Structural input typing and binding constructor destructors were retained. This is **not** an ablation of the wire grammar or n=2 destructor: removing those requires specifying how their bound variables are supplied. No matrix result claims those structural assumptions were independently tested. (`scratch/build.py:10–32`; `G.pv:159–163,176–181`)

Initial tag/message-unbinding variants failed parsing because new tuple variables lacked explicit types. They remain as `*.initial.pv` and `*.initial.out`; they have no security result. Corrected versions use typed variables. (`scratch/m_D_139_tag.initial.out:1–2`; `scratch/m_D_139_tag.pv:139`; `scratch/m_D_139_binding.pv:139`)

## 4. Vacuity

All eight committed outputs contain reachable witnesses with concrete traces. Each witness RESULT below is immediately preceded by `A trace has been found.` Independent baseline reruns reproduce every committed RESULT line. (`scratch/baselines.tsv:1–9`)

| Committed `.out` | Safety results S,F,A,K and lines | M1 trace/result | M2 trace/result | HonestAccepted trace/result |
|---|---|---|---|---|
| D | T,T,T,T: 386,392,398,404 | 579–580 | 811–812 | 1054–1055 |
| R | T,T,T,T: 386,392,398,404 | 579–580 | 811–812 | 1054–1055 |
| G | T,T,T,T: 354,360,366,372 | 535–536 | 755–756 | 986–987 |
| Q3 | **F**,T,T,T: 520,526,532,538 | 701–702 | 921–922 | 1152–1153 |
| Q4 | T,**F**,T,T: 353,601,608,615 | 779–780 | 1000–1001 | 1232–1233 |
| C1 | T,T,T,T: 354,360,366,372 | 535–536 | 755–756 | 986–987 |
| C2 | T,T,**F**,T: 349,356,535,542 | 705–706 | 924–925 | 1099–1100 |
| C3 | T,T,T,T: 349,356,363,370 | 533–534 | 752–753 | 982–983 |

T/F are ProVerif truth values for **non-reachability**; all witness results are F. Q3, Q4 and C2 go red on exactly their named safety query, with traces. C1 and C3 are intentionally green configurations, not missing red companions. (`Q3.pv:20–25`; `Q3.out:519–538`; `Q4.pv:20–24`; `Q4.out:600–615`; `C1.pv:23–29`; `C2.pv:27–30`; `C2.out:534–542`; `C3.pv:21–31`)

Witness reachability does not establish content agreement: `HonestComplete` checks manifest and key fingerprints only. It coexists with mixed-payload acceptance. (`G.pv:201–214`; `scratch/a_mixed_payload.out:611,811,1045`)

## 5. Verdict on each header’s honesty

| Header | Verdict |
|---|---|
| **D** | The bounded four-query result is reproduced. “no set-shrinking around an honest key” needs the one-key/one-manifest qualification; it is not a general signing-history correspondence. Naming “the frame’s fingerprint (Reattributed)” as load-bearing overstates individual necessity: its isolated removals remain green. (`D.pv:15–35,119–121`; `D.out:386–404`; `scratch/dependencies.tsv:17,42,46`; `scratch/a_key_reuse.out:654`) |
| **R** | Same bounded result and qualification, independently rerun. Its matching “the frame’s fingerprint (Reattributed)” dependency wording is too strong if read as individually necessary. (`R.pv:15–35,119–121`; `R.out:386–404`; `scratch/dependencies.tsv:63,88,92`) |
| **G** | Fixed-fixture unreachability holds. “no honest key is accepted as a signer of a manifest it never signed” is **not what the judge expresses generally**: it detects difference from one selected record. The fixture qualification is essential. Excluded verdicts, canonical encoding, waiver and authorship materially limit P2 discharge. (`G.pv:20–21,27–37,61–66,220–226`; `G.out:354–372`; `scratch/a_key_reuse.out:644–654`) |
| **Q3** | “It must go red on Stripped ONLY” matches the trace and remaining safety results. No identified overclaim in that bounded companion result. (`Q3.pv:14–28`; `Q3.out:519–538`) |
| **Q4** | “go red on SignerForged ONLY” matches. The unchanged strict fixture blocks duplicate presentation, consistent with its distinct-slot-key explanation; this does not establish canonical-set uniqueness. (`Q4.pv:20–28`; `Q4.out:353–615`; `scratch/a_duplicate_signature.out:392`; `PREDICTIONS-frozen.md:114–126`) |
| **C1** | “This model proves: nothing about P2” and its green redundancy result match. It is not an effective red companion by itself, as stated. (`C1.pv:23–30`; `C1.out:354–372`) |
| **C2** | “It must go red on SetAltered ONLY” matches. Its shrink result is fixture-bound; a general “never signed” interpretation inherits the judge defect. (`C2.pv:23–35`; `C2.out:349–542`; `G.pv:220–226`) |
| **C3** | “possession over the manifest is INDIVIDUALLY sufficient against set-shrinking” is supported **with the remaining verifier and fixture retained**. It does not establish the expected set inside every attestation signature; the header explicitly calls this an isolation configuration. (`C3.pv:21–31,117–119,130–153`; `C3.out:363`; `REGISTERED-PROPERTY.txt:7–8`) |

The strongest unsupported exported wording is the frozen plan’s:

> “acceptance for manifest `m` implies a signature over the exact framed bytes from every signer `m`’s signed set names” (`PREDICTIONS-frozen.md:537–540`)

The slots sign distinct frames and can sign distinct payloads. Every individual attestation-check removal also preserves the registered queries. A defensible exported statement must specify **per-slot frames**, identify any common-content relation separately, and retain the signature-verification dependency rather than treating the two judge queries as sufficient evidence for it. (`G.pv:176–195`; `scratch/a_mixed_payload.out:603–635`; `scratch/dependencies.tsv:102–104,122–127`)
### Reviewer output — S-P7 (`model: gpt-6-astra`; scratch archived under `formal/suite/s-p7/proverif/falsification-2026-09-06/`)

## 1. Correspondence audit

**The queries do not discharge P7 as a whole.** The largest gaps are unrepresentable cross-kind byte confusion, signature-set manipulation, and verdict preservation. An unchanged strict verifier accepts a false inner-version record. Q2 can successfully check an honest signature under a substituted key before rejecting the frame. (`proverif/sp7_q2_degraded_compromised.pv:64-79,246-259`; `scratch/attack_version_lie.out:809`; `scratch/attack_dsks_checked.out:864`.)

Notation: Q1D/Q1R are the DNS/repository-compromised strict models; Q2 is degraded; Q4O is the opaque two-version control; Q5 is depth two. I = shared inner check, W = depth-one wrapper, O/M = depth-two outer/middle wrapper. These are implemented paths, not arbitrary recursion. (`proverif/sp7_q1_strict_dns_compromised.pv:177-216`; `proverif/sp7_q1_strict_repo_compromised.pv:177-216`; `proverif/sp7_q2_degraded_compromised.pv:246-283`; `proverif/sp7_q4_control_opaque_twoversion.pv:151-190`; `proverif/sp7_q5_depth2_correct.pv:177-242`.)

**Complete check inventory.** Every role below executes the catalog following the table. I expects `OT_ATTEST`; wrapper roles expect `OT_WRAPPER`. The base path supplies I with standalone inputs; wrapped paths extract its bytes/signature from the embedded pair. Q4O additionally requires `canon(cvc,framed(...))` for I. (`proverif/sp7_q2_degraded_compromised.pv:262-283`; `proverif/sp7_q4_control_opaque_twoversion.pv:159`; `proverif/sp7_q5_depth2_correct.pv:192-242`.)

| Model | Every verifier role and check location |
|---|---|
| Q1D | I: `proverif/sp7_q1_strict_dns_compromised.pv:179-186`; W: `:206-213`; two evidence checks per role. |
| Q1R | I: `proverif/sp7_q1_strict_repo_compromised.pv:179-186`; W: `:206-213`; two evidence checks per role. |
| Q2 | I: `proverif/sp7_q2_degraded_compromised.pv:248-254`; W: `:274-280`; one evidence check per role. |
| Q4O | I: `proverif/sp7_q4_control_opaque_twoversion.pv:153-160`; W: `:180-187`; two evidence checks per role, plus I’s `canon` shape. |
| Q5 | I: `proverif/sp7_q5_depth2_correct.pv:179-185`; W: `:205-211`; O: `:224-230`; M: `:233-239`; one evidence check per role. |

The catalog applies separately at every cited role:

| Check performed | License in the supplied registered text |
|---|---|
| Presentation tuple arity and argument sorts; five-field `authTuple` decomposition | Encoding choices, not P7-specified formats. The frozen plan selects this abstraction. (`PREDICTIONS-frozen.md:137-151,164-178`.) |
| Evidence signature verifies under designated channel key; recovered tag equals `STMT_DIGEST`; digest equals `h(t)` | Extra authority premises, absent from P7’s operative sentences. Selected by the plan’s “outer authority” and “inner authority evidence against the inner manifest.” (`REGISTERED-PROPERTY.txt:1-19`; `PREDICTIONS-frozen.md:164-169`.) |
| Manifest slot satisfies `fp(k) = kfpr` | Extra key-binding premise. P7 does not prescribe this slot test. (`REGISTERED-PROPERTY.txt:1-19`; `PREDICTIONS-frozen.md:168-172`.) |
| Possession signature verifies under `k`; tag equals `POSS`; recovered manifest equals `t` | Extra possession premise, selected by “outer … possession” and “inner possession,” not prescribed by P7. (`REGISTERED-PROPERTY.txt:1-19`; `PREDICTIONS-frozen.md:164-169`.) |
| Object signature verifies under `k`; tag equals `BYTES`; recovered object equals complete presented `fb` | Supports “inside the signed bytes” and exact-byte commitment; the particular envelope is an encoding choice. (`REGISTERED-PROPERTY.txt:1-8`; `PREDICTIONS-frozen.md:137-147`.) |
| Seven-field frame shape; type equals expected role type | Directly supports “No trace exists in which an object of one type is accepted as another,” restricted to implemented acceptance roles. (`REGISTERED-PROPERTY.txt:5-6`; `PREDICTIONS-frozen.md:57-67`.) |
| Frame algorithm equals manifest algorithm; frame identity equals manifest identity; frame fingerprint equals `fp(k)`; frame manifest hash equals `h(t)` | Additional binding premises, not checks named by P7. Identity/key binding implements the plan’s C2. Algorithm equality is not an algorithm-support check. (`REGISTERED-PROPERTY.txt:1-19`; `PREDICTIONS-frozen.md:68-73,137-142,164-172`.) |
| Wrapper payload decomposes as `wrap(cvInner,(innerBytes,innerSig))`; embedded pair feeds next check | Supports embedding and rejection of hash-only commitment at term level. It does not test concrete serialization. (`REGISTERED-PROPERTY.txt:6-14`; `PREDICTIONS-frozen.md:143-156`.) |
| Version fields are bound by pattern presence; Q4O additionally decomposes `canon(cvc,...)` | Implements only presence. No equality connects recorded inner version to inner frame version, or Q4O’s `cvc` to its frame version. (`REGISTERED-PROPERTY.txt:14-15`; `proverif/sp7_q2_degraded_compromised.pv:253,279`; `proverif/sp7_q4_control_opaque_twoversion.pv:159,186`.) |

These extra premises are **not prohibited**, but P7 alone does not license treating them as its complete verifier specification. The frozen plan specifies them without closing these property gaps. (`REGISTERED-PROPERTY.txt:1-19`; `PREDICTIONS-frozen.md:164-178,503-521`.)

**Registered requirements without a complete check/query:**

- “Every signed object carries a domain-separation type tag inside the signed bytes, drawn from the enumerated set: base attestation, wrapper, issuer-key manifest, authority evidence, conformance vector, review-recency attestation (§4.7).” Only attestation/wrapper/review frames are exercised. Actual possession and authority signatures use `POSS`/`STMT_DIGEST` outside the framed-type judge; conformance-vector verification is absent. (`REGISTERED-PROPERTY.txt:1-5`; `proverif/sp7_q2_degraded_compromised.pv:193-238,286-289,320-325`.)
- “No trace exists in which an object of one type is accepted as another (no cross-type confusion).” No judge covers actual non-framed kinds, adversary-only signing provenance, or acceptance as manifest/evidence/vector/review. The judge requires an honest report of the **identical framed term**; altered/re-signed terms fall outside that comparison. (`REGISTERED-PROPERTY.txt:5-6`; `proverif/sp7_q2_degraded_compromised.pv:208-211,237,286-289`; `PREDICTIONS-frozen.md:561-570`.)
- “A wrapper commits to the inner package’s exact bytes, embedded as an opaque byte string … — never as parsed JSON.” “Outer canonicalization must be structurally unable to re-serialize, re-escape, or otherwise touch the inner byte stream ….” No correct-model query tests serialization, escaping, or OTS preservation. `wrap` preserves terms by construction; Q4’s rewrite is stipulated. (`REGISTERED-PROPERTY.txt:6-12`; `proverif/sp7_q2_degraded_compromised.pv:64-68,98-103,129-132`; `proverif/sp7_q4_companion_reserialize_twoversion.pv:61-66`.)
- “Hash-only commitment is rejected: the inner bytes must travel inside the bundle, or P9’s self-containment fails.” The embedded pair contains bytes/signature, but inner manifest, evidence and possession remain presenter-supplied outside it. No package-completeness query checks their inclusion. Rejecting the hash-only attack below does not establish full self-containment. (`REGISTERED-PROPERTY.txt:13-14`; `proverif/sp7_q2_degraded_compromised.pv:272-283`; `scratch/attack_hash_only_fixed.out:590`.)
- “The wrapper records both inner and outer canonicalization versions.” No check establishes that the recorded values are true; a mismatch reaches acceptance. (`REGISTERED-PROPERTY.txt:14-15`; `scratch/attack_version_lie.pv:244-248`; `scratch/attack_version_lie.out:799-809`.)
- “Wrapping never alters the inner package’s independently-computed verdict — the wrapper attests the inner bytes, never the inner verification result (preserving §3.1’s distinction exactly).” There is no paired-verdict query, verdict partition, or universal base/wrapped correspondence. Reusing I establishes the same predicate only after outer checks pass and with the same supplied inner inputs. Existential witnesses do not establish preservation. (`REGISTERED-PROPERTY.txt:15-19`; `proverif/sp7_q2_degraded_compromised.pv:171-188,262-283`; `PREDICTIONS-frozen.md:503-521,555-560`.)
- P7 gives no depth-two exemption. Deeper verification and A1.3’s signature-set stripping/reordering/duplication have no corresponding structure or checks: each layer has one signature, and Q5 has two handwritten wrapper levels. (`REGISTERED-PROPERTY.txt:1-19`; `A1.3-adversary.txt:7`; `proverif/sp7_q5_depth2_correct.pv:220-242`.)

## 2. Attacks

The first five experiments retain every strict verifier check and use one compromised channel. They change fixtures, add observers, or supply adversarial inputs. The original checks are at `proverif/sp7_q1_strict_dns_compromised.pv:179-216`, and the leaked key at `:253`. A1.3 permits alteration, replay, chosen keys/manifests and proper-subset channel compromise. (`A1.3-adversary.txt:5-16`.)

1. **False inner canonicalization-version record — reachable.** Supply an honest wrapper with arbitrary `cvInner` while embedding an honest `cvA` attestation. Both objects pass. The observer compares the recorded version with the accepted inner frame’s version. (`scratch/attack_version_lie.pv:244-248`; concrete trace: `scratch/attack_version_lie.out:787-805`.)
   `RESULT not event(BadVersion) is false.` (`scratch/attack_version_lie.out:809`.) This defeats truthful version recording, not an existing registered query.
2. **Additional honest signed types replayed into attestation/wrapper roles — unreachable.** Extend I2 with framed `OT_MANIFEST`, `OT_AUTHEVID`, `OT_CONFVEC`, `OT_TLR` and `OT_REFUSAL` signers under its existing certified key. This tests additional framed fixtures, not actual `authTuple`/evidence encodings. (`scratch/attack_extra_types.pv:263-267`.)
   `RESULT not event(TypeConfused(otS_1,otA_1,fb)) is true.` (`scratch/attack_extra_types.out:730`.)
3. **Same honest key, additional issuance identity — unreachable re-scoping.** Publish another honest manifest for I1’s key with `aliasId`; add its honest attester and allow mixing/replay of both manifests, signatures and identities. (`scratch/attack_alias_issuer.pv:263-265`.)
   `RESULT not event(Rescoped(kX_1,idX_1,kH_3,idH_1,fb)) is true.` (`scratch/attack_alias_issuer.out:658`.)
4. **Cross-model Q4-to-Q1 replay — unreachable acceptance.** Add a Q4-shaped `canon(cvA,framed(...))` signer sharing Q1’s honest key and manifest. Q1 rejects that shape. This is a representation incompatibility, not a security result for a common byte parser. (`scratch/attack_cross_model.pv:245-253`; `proverif/sp7_q1_strict_dns_compromised.pv:185`; `proverif/sp7_q4_control_opaque_twoversion.pv:110,159`.)
   `RESULT not event(CrossAccepted) is true.` (`scratch/attack_cross_model.out:606`.)
5. **Hash-only replacement with original signature — unreachable inner acceptance.** Recover an honest signed frame, submit `(cvA,h(bytes),seenSignature)` to an honest wrapper, and watch for acceptance of the hash as the inner object. (`scratch/attack_hash_only_fixed.pv:245-252`.)
   `RESULT not event(HashOnlyAccepted) is true.` (`scratch/attack_hash_only_fixed.out:590`.)

Two additional experiments use Q2’s selected degraded compromise. The isolated model does not describe a larger channel universe or availability transition, so identifying its compromised **sole** channel with A1.3’s **proper subset** requires an external premise. The five strict experiments do not require it. (`A1.3-adversary.txt:15-16`; `proverif/sp7_q2_degraded_compromised.pv:317-319`; `PREDICTIONS-frozen.md:195-200`.)

6. **Post-signature DSKS substitution — unreachable completed transplant.** Derive `dsks(seen,salt)`, make a manifest/possession/evidence for that key, wrap unchanged honest bytes/signature, and present the derived key as the inner key. (`scratch/attack_dsks.pv:311-322`; `tessera_theory.pvl:99-104`.)
   `RESULT not event(AttackSent) is false.` (`scratch/attack_dsks.out:606`.)
   `RESULT not event(InnerSigTransplanted(kX_1,s)) is true.` (`scratch/attack_dsks.out:651`.)
7. **Same DSKS attack against “never verified” wording — reachable.** Add only a private, parallel observation immediately after successful inner `checksign`; retain all subsequent frame/hash checks. Pair that observation with the honest signature report. (`scratch/attack_dsks_checked.pv:253-265,328-331`.)
   `RESULT not event(WrongKeyVerified) is false.` (`scratch/attack_dsks_checked.out:864`.)
   `RESULT not event(InnerSigTransplanted(kX_1,s)) is true.` (`scratch/attack_dsks_checked.out:1031`.) The primitive verifies under the substituted key; the complete verifier rejects before acceptance.

**Most important: UNREPRESENTABLE attacks.** No fixture can make one byte string parse both as non-framed authority/possession material and as a frame in this algebra. Distinct constructors decide that before the type guard; more `OT_*` signers do not repair it. There is also no signature set to reorder/duplicate, concrete outer canonicalizer to attack, or verdict value to transplant. These are missing attack surfaces, not unreachable attacks established by `RESULT` lines. (`A1.3-adversary.txt:5-12`; `tessera_theory.pvl:98-104,138-164`; `proverif/sp7_q2_degraded_compromised.pv:129-132,193-238,246-283`; `PREDICTIONS-frozen.md:503-521,561-570`.)

## 3. Mutations

**198 completed single-check mutants: 180 inert, 18 changed outcomes.** Five baseline reruns match committed results. The complete dependency matrix records every mutant, original check location, every query’s truth value, and raw output locations in `scratch/dependencies.tsv:1-199`; grouped results are in `scratch/guard_groups.tsv:2-16`; baseline verification is in `scratch/verification.txt:1-7`.

Each experiment removes one whole guard or unbinds one equality. Structural constructors, tuple arities and presence-only fields remain fixed: this is a guard dependency matrix, not an ablation of the term algebra. Exact edits are recorded by the generator. (`scratch/mutate.py:12-39`; `scratch/mutations.json:1-20`.)

Cell positions are **I/W**, or **I/W/O/M** for Q5. `–` means every query retains its baseline outcome; `T` means only TypeConfused becomes reachable; `S` means only InnerSigTransplanted becomes reachable. **All scope queries, Reattributed where queried, and every honest witness survive every removal.** Q4O does not query Reattributed. Evidence rows cover each channel separately. (`scratch/dependencies.tsv:1-199`; `proverif/sp7_q4_control_opaque_twoversion.pv:75-92`.)

| Single removed/unbound guard | Q1D | Q1R | Q2 | Q4O | Q5 | Evidence |
|---|---|---|---|---|---|---|
| Entire evidence check | –/– | –/– | –/– | –/– | –/–/–/– | `scratch/guard_groups.tsv:2` |
| Evidence `STMT_DIGEST` equality | –/– | –/– | –/– | –/– | –/–/–/– | `scratch/guard_groups.tsv:3` |
| Evidence digest equality | –/– | –/– | –/– | –/– | –/–/–/– | `scratch/guard_groups.tsv:4` |
| Manifest fingerprint slot | –/– | –/– | –/– | –/– | –/–/–/– | `scratch/guard_groups.tsv:5` |
| Entire possession check | –/– | –/– | –/– | –/– | –/–/–/– | `scratch/guard_groups.tsv:6` |
| Possession `POSS` equality | –/– | –/– | –/– | –/– | –/–/–/– | `scratch/guard_groups.tsv:7` |
| Possession manifest equality | –/– | –/– | –/– | –/– | –/–/–/– | `scratch/guard_groups.tsv:8` |
| Entire object signature check | S/– | S/– | S/– | S/– | S/–/–/– | `scratch/guard_groups.tsv:9` |
| Object signature `BYTES` equality | –/– | –/– | –/– | –/– | –/–/–/– | `scratch/guard_groups.tsv:10` |
| Object signature bytes equality | –/– | –/– | S/– | –/– | S/–/–/– | `scratch/guard_groups.tsv:11` |
| Frame type equality | T/T | T/T | T/T | –/T | T/T/T/T | `scratch/guard_groups.tsv:12` |
| Frame algorithm equality | –/– | –/– | –/– | –/– | –/–/–/– | `scratch/guard_groups.tsv:13` |
| Frame identity equality | –/– | –/– | –/– | –/– | –/–/–/– | `scratch/guard_groups.tsv:14` |
| Frame fingerprint equality | –/– | –/– | –/– | –/– | –/–/–/– | `scratch/guard_groups.tsv:15` |
| Frame manifest-hash equality | –/– | –/– | –/– | –/– | –/–/–/– | `scratch/guard_groups.tsv:16` |

Why checks are inert **for these queries**:

- Key/identity checks have redundant routes: frame fingerprint binds the key directly; frame hash plus manifest slot also binds it. Frame identity, manifest hash and possession under the pinned honest key constrain identity in the fixed fixture. Removing one preserves alternatives; this does not justify removing them together. (`proverif/sp7_q2_degraded_compromised.pv:248-254,311-314`; `scratch/guard_groups.tsv:5-8,14-16`.)
- Compromised evidence checks cannot exclude attacker-made evidence. Even the **honest** strict-channel check is individually inert: remaining bindings protect the measured relations. Honest repository removal leaves S true in Q1D; honest DNS removal does likewise in Q1R. This contradicts an individual-necessity reading of Q1’s load-bearing list. (`scratch/q1d_I_evRI_evidence.out:580`; `scratch/q1r_I_evDI_evidence.out:580`; `proverif/sp7_q1_strict_dns_compromised.pv:28-38`; `scratch/guard_groups.tsv:2-4`.)
- Wrapper signature/binding checks do not discharge an outer-authorship query here. Scope judges compare accepted inner bytes with honest inner reports; type guards still constrain wrapper type. Algorithm correctness is not queried. (`proverif/sp7_q2_degraded_compromised.pv:171-188,286-307`; `scratch/guard_groups.tsv:9,13-16`.)
- Unbinding tag equalities retains constructor/payload distinctions between manifests, frames and digests. Green tag mutants do not demonstrate safe byte-level tag omission. (`tessera_theory.pvl:131,164`; `proverif/sp7_q2_degraded_compromised.pv:129,248-253`; `scratch/guard_groups.tsv:3,7,10`.)
- **Q4O’s inner type equality is inert:** only its honest attester emits `canon(...,framed(...))`; wrappers and review records remain bare frames. The `canon` shape already discriminates these fixtures. `RESULT not event(TypeConfused(otS_1,otA_1,fb)) is true.` (`proverif/sp7_q4_control_opaque_twoversion.pv:110,127,140,159`; `scratch/q4o_I_type.out:560`.)
- Removing the inner signature check makes S report an **unverified supplied signature** beside other bytes. Its red is a reporting dependency, not a cryptographic forgery. Unbinding only byte equality also makes S red in Q2/Q5; strict fixtures keep it green. (`proverif/sp7_q2_degraded_compromised.pv:252-259,304-307`; `scratch/q2_I_sig_bytes_typed.out:876`; `scratch/q1d_I_sig_bytes_typed.out:615`; `scratch/guard_groups.tsv:9,11`.)

Failed syntax attempts remain beside corrected `_typed`/`_fixed` files and outputs; they are excluded from semantic results. For example, `scratch/q2_I_sig_bytes.out:1-2` records a missing type annotation; `scratch/q2_I_sig_bytes_typed.out:514-1423` contains the completed run.

## 4. Vacuity

Every **intended reachable** committed witness has a derivation and a found trace. Entries below give `derivation-start → RESULT-line`; immediately preceding each reachable result is “A trace has been found.” B = HonestAccepted; W = HonestWrappedAccepted. **Q4 two-version W is intentionally unreachable**, so the literal assertion that every witness is reachable is false. (`scratch/committed_audit.tsv:1-69`.)

| Committed output | B | W / W1 | W2 |
|---|---|---|---|
| `proverif/sp7_q1_strict_dns_compromised.out` | `:951→1144` | `:618→935` | — |
| `proverif/sp7_q1_strict_repo_compromised.out` | `:951→1144` | `:618→935` | — |
| `proverif/sp7_q2_degraded_compromised.out` | `:861→1042` | `:559→846` | — |
| `proverif/sp7_q3_companion_type_unchecked.out` | `:1086→1267` | `:780→1067` | — |
| `proverif/sp7_q4_companion_reserialize_twoversion.out` | `:619→817` | **unreachable `:604`** | — |
| `proverif/sp7_q4_companion_reserialize_isolation.out` | `:949→1147` | `:610→933` | — |
| `proverif/sp7_q4_control_opaque_twoversion.out` | `:942→1140` | `:604→926` | — |
| `proverif/sp7_q4_probe_degraded_twoversion.out` | `:854→1040` | `:548→840` | — |
| `proverif/sp7_q5_depth2_correct.out` | `:1613→1794` | `:846→1133` | `:1173→1573` |
| `proverif/sp7_q5c_companion_one_level_in.out` | `:1916→2097` | `:1209→1496` | `:1537→1876` |
| `proverif/sp7_q6a_companion_identity_outermost.out` | `:1133→1314` | `:834→1118` | — |
| `proverif/sp7_q6b_companion_key_outermost.out` | `:1327→1508` | `:1069→1317` | — |

Companions have their named failures **among the queries actually committed**:

| Companion | Header requirement | Committed failure; other queried safety events remain unreachable |
|---|---|---|
| Q3 | TypeConfused reachable (`proverif/sp7_q3_companion_type_unchecked.pv:19-24`) | `proverif/sp7_q3_companion_type_unchecked.out:727,744,761` |
| Q4 two-version | W unreachable; isolation W reachable (`proverif/sp7_q4_companion_reserialize_twoversion.pv:39-46`) | `proverif/sp7_q4_companion_reserialize_twoversion.out:565-604`; isolation `proverif/sp7_q4_companion_reserialize_isolation.out:933` |
| Q5c | R2 reachable, R1 unreachable (`proverif/sp7_q5c_companion_one_level_in.pv:22-28`) | `proverif/sp7_q5c_companion_one_level_in.out:652,690,1131,1169` |
| Q6a | Rescoped reachable (`proverif/sp7_q6a_companion_identity_outermost.pv:22-26`) | `proverif/sp7_q6a_companion_identity_outermost.out:503,806,819` |
| Q6b | Rescoped and S reachable (`proverif/sp7_q6b_companion_key_outermost.pv:26-30`) | `proverif/sp7_q6b_companion_key_outermost.out:489,769,1058`; explicit DSKS at `:882-883`. |

**“Exactly” cannot extend to omitted queries.** The companions deliberately omit Reattributed. Restoring only that query leaves it unreachable in Q3, both Q4 configurations, Q5c and Q6a, but **Q6b also makes it reachable**:
`RESULT not event(Reattributed(kExtra,kHonExtra,bytesExtra)) is false.`
(`proverif/sp7_q6b_companion_key_outermost.pv:89-91`; `scratch/audit_sp7_q3_companion_type_unchecked.out:778`; `scratch/audit_sp7_q4_companion_reserialize_isolation.out:608`; `scratch/audit_sp7_q4_companion_reserialize_twoversion.out:604`; `scratch/audit_sp7_q5c_companion_one_level_in.out:1207`; `scratch/audit_sp7_q6a_companion_identity_outermost.out:832`; `scratch/audit_sp7_q6b_companion_key_outermost.out:1338`.)

Witnesses are existential, not acceptance guarantees for every honest issuer/version pairing. Q6a/Q5c explicitly retain a same-issuer route despite their bad attribution rule. (`proverif/sp7_q2_degraded_compromised.pv:183-188`; `proverif/sp7_q6a_companion_identity_outermost.pv:24-25`; `proverif/sp7_q5c_companion_one_level_in.pv:25-27`.)

## 5. Verdict on each header’s honesty

| Header | Verdict and verbatim wording requiring attention |
|---|---|
| Q1D | Bounded query claims match committed outcomes, but **“Load-bearing for these queries: the honest channel’s evidence check”** overstates individual necessity: removal changes none of these queries. (`proverif/sp7_q1_strict_dns_compromised.pv:14-38`; `scratch/q1d_I_evRI_evidence.out:554-1125`.) |
| Q1R | Same verdict for **“Load-bearing for these queries: the honest channel’s evidence check”**, independently tested with DNS as the honest channel. (`proverif/sp7_q1_strict_repo_compromised.pv:14-38`; `scratch/q1r_I_evDI_evidence.out:554-1125`.) |
| Q2 | **Literal overclaim:** “the honest inner signature term is never verified under a key other than its signer’s inside a wrapped presentation.” It verifies under a DSKS key before rejection. The claim must concern an **accepted** presentation. The narrower acceptance queries survive. Version and non-framed-type exclusions are explicit, so the version attack exposes a P7 gap rather than a concealed version-consistency claim. (`proverif/sp7_q2_degraded_compromised.pv:20-23,60-79`; `scratch/attack_dsks_checked.out:864,1031`.) |
| Q4O | **“the honest inner acceptance inside the wrapper is exactly its standalone acceptance”** exceeds its existential witnesses. The shared-check argument is conditional on reaching I with identical inputs. The header separately says “Proves nothing”; no relational query discharges the quoted equality. (`proverif/sp7_q4_control_opaque_twoversion.pv:10-19,75-92,167-190`.) |
| Q5 | **“This model proves: everything the Q2 header states”** inherits Q2’s overbroad “never verified” wording. Actual depth-one/depth-two acceptance queries hold; “nothing is claimed beyond 2” limits depth. Inherited load-bearing reasoning does not establish individual necessity. (`proverif/sp7_q5_depth2_correct.pv:14-38,179-190`; `proverif/sp7_q5_depth2_correct.out:654-806`; `scratch/guard_groups.tsv:2-16`.) |
| Q3 | “This model proves nothing; it shows the type judge can detect the failure it is for” is supported for the implemented framed-type mutation. It establishes no non-framed coverage. (`proverif/sp7_q3_companion_type_unchecked.pv:16-24`; `proverif/sp7_q3_companion_type_unchecked.out:727`.) |
| Q4 two-version | Named witness failure and isolation requirement are met. **“wrapping has altered the inner verdict”** must retain the symbolic, non-acceptance interpretation: no verdict-valued query exists. “This model proves nothing” excludes property discharge. (`proverif/sp7_q4_companion_reserialize_twoversion.pv:21-46`; `proverif/sp7_q4_companion_reserialize_twoversion.out:604,817`.) |
| Q4 isolation | Stated reachable control and “This model proves nothing” match results. Arbitrary canonicalization semantics remain untested. (`proverif/sp7_q4_companion_reserialize_isolation.pv:21-40`; `proverif/sp7_q4_companion_reserialize_isolation.out:933,1147`.) |
| Q4 degraded probe | Limited fixture-interaction claim matches reachable W; it explicitly offers no property evidence. (`proverif/sp7_q4_probe_degraded_twoversion.pv:5-14`; `proverif/sp7_q4_probe_degraded_twoversion.out:840`.) |
| Q5c | Named depth-specific failure and surviving witnesses match; “model proves nothing” limits the claim. (`proverif/sp7_q5c_companion_one_level_in.pv:12-28`; `proverif/sp7_q5c_companion_one_level_in.out:690,1131,1496,1876`.) |
| Q6a | **Overclaim:** “the mutation misattributes on EVERY wrapped acceptance.” Its later same-issuer exception and reachable honest witness refute “EVERY.” Required Rescoped red is present. (`proverif/sp7_q6a_companion_identity_outermost.pv:11-12,22-26`; `proverif/sp7_q6a_companion_identity_outermost.out:806,1118`.) |
| Q6b | Two named reds and “This model proves nothing” match. They are not its only broken relation: restored Reattributed is also red. Explicit omission makes this a diagnostic limitation, not evidence that other relations survive. (`proverif/sp7_q6b_companion_key_outermost.pv:26-30,89-91`; `scratch/audit_sp7_q6b_companion_key_outermost.out:1338`.) |
### Reviewer output — S-STANDING (`model: gpt-6-astra`; scratch archived under `formal/suite/s-standing/proverif/falsification-2026-09-06/`)

## 1. Correspondence audit

**The safety results depend on the issuer fixtures more heavily than the load-bearing annotations acknowledge.** Removing all terminal decisions while retaining the per-entry disposition check preserves every safety result in all three correct models. Adding an honestly evidenced adversary-owned key breaks the strict unrestricted correspondence without breaking either honest-key correspondence. (`scratch/dependency-index.txt:20`; `scratch/a_own_registered_key.out:658–684`)

Citation abbreviations below resolve to these exact files; `.out` denotes the corresponding committed output.

| Reference | File |
|---|---|
| D.pv | `proverif/ss_q1_strict_dns_compromised.pv` |
| R.pv | `proverif/ss_q1_strict_repo_compromised.pv` |
| G.pv | `proverif/ss_q1d_degraded_compromised.pv` |
| Q2.pv | `proverif/ss_q2_companionA_identity_declared.pv` |
| Q3.pv | `proverif/ss_q3_companionB_entitled_via_envelope.pv` |
| Q4.pv | `proverif/ss_q4_companionC_terminal_unchecked.pv` |
| Q5.pv | `proverif/ss_q5_companionD_reason_collapsed.pv` |
| P | `REGISTERED-PROPERTY.txt` |
| A | `A1.3-adversary.txt` |
| F | `PREDICTIONS-frozen.md` |

The governing sentence is: **“Any artifact claiming standing must present verifiable standing evidence binding its issuance identity, attempt lineage, and terminal disposition.”** This licenses the binding obligations; it does not itself specify a hash, fingerprint, TLR encoding, channel threshold, or anchor format. Those construction choices appear in the predictions. (`P:14–16`; `F:56–73`)

Every verifier check is inventoried below. “Construction” means an implementation of the broad registered obligation, additionally specified in F; it does not mean that the exact check occurs in P.

| Check or structural gate | D.pv | R.pv | G.pv | Registration correspondence |
|---|---:|---:|---:|---|
| Typed bundle shape; public-key field type | 269–270 | 271–272 | 249–250 | Encoding scaffolding; exact shape not specified by P:13–17. |
| Authority signature under each configured channel key; `STMT_DIGEST` tag; exact `h(t)` | 272–273 | 274–275 | 252 | Construction of evidenced entitlement, F:145–151,197–205; exact threshold not in P. |
| Five-field `authTuple` decomposition | 274 | 276 | 253 | Construction, F:145–147. No independent acceptance test of `ss`, `alg`, or `ver` here. |
| Verifier derives identity as `h(core)` | 276 | 278 | 255 | Implements identity binding, P:14–16; digest choice specified by F:113–125. |
| `se = noTLR` | 277–279 | 279–281 | 256–258 | Directly implements missing-evidence outcome, P:16–17. |
| `withTLR(kT,tlrSig,ap)` decomposition | 281 | 283 | 260 | Construction-specific evidence representation, F:58–64. |
| `fp(kT) = kfpr` | 283 | 285 | 262 | Entitlement construction, F:62–73; not an explicit fingerprint requirement in P. |
| `kT = kX` | 285 | 287 | 264 | Additional fixture-shape restriction; neither P:13–17 nor F:66–73 requires this separate presented-key equality. |
| Signature verification under `kT`; `TLR` tag; three-field body decomposition | 287 | 289 | 266 | Implements verifiable joint binding; exact encoding is construction-specific, P:14–16; F:139–144. |
| `anchorProof(h(tlrSig))` shape and digest equality | 289 | 291 | 268 | Anchored construction, F:64,169–175; P:13–17 does not mandate this particular mechanism. |
| Two-entry lineage decomposition and identity lookup; first matching entry wins | 237–241,291 | 239–243,293 | 217–221,270 | Implements lineage membership, P:15–16. Two entries and duplicate precedence are encoding restrictions, F:127–138. |
| `terminal = TERM_REFUSED` | 246–248 | 248–250 | 226–228 | Terminal interpretation; exact refusal code is construction vocabulary, F:152–164. |
| `TERM_SHIPPED(shippedId)` decomposition | 250 | 252 | 230 | Construction of terminal disposition, P:15–16; F:129–130. |
| `shippedId = aid` | 251 | 253 | 231 | Implements identity-to-terminal binding, P:14–16. |
| `d = DISP_SHIPPED` | 252 | 254 | 232 | Additional consistency check on the selected entry; construction-specific, F:95–104. |
| Envelope: typed bundle, authority signatures/tags/digests, tuple decomposition | 306–310 | 308–312 | 285–288 | P:24–30 requires an unchanged parallel verdict; these particular envelope checks are not specified in the supplied property text. |
| Envelope: fingerprint equality; `attemptCore` shape and embedded tuple equality | 311–312 | 313–314 | 289–290 | Same limitation: carried envelope checks, not discharged here. |
| Envelope: possession signature/key/tag/tuple; bytes signature/key/tag/`fb` | 313–314 | 315–316 | 291–292 | Same limitation. |
| Envelope: seven-field frame; algorithm, issuer, fingerprint equalities; manifest digest equality | 315–316 | 317–318 | 293–294 | Same limitation. `ot` and `cv` are extracted without validation. |

The judges are instrumentation, not verifier defenses: entitlement compares the reported key against the reported tuple; N1 additionally joins a designation; reason discrimination joins two different branch labels carrying one code. (`D.pv:322–334`; `R.pv:324–336`; `G.pv:300–312`)

**Requirements without a corresponding complete check/query:**

- **“Cryptographic validity alone confers no protocol standing.”** The standing path requires its own evidence, but there is no query relating envelope acceptance, missing evidence, and the standing report for one invocation. (`P:13`; `D.pv:143–175,268–317`)
- **“Missing standing evidence leaves the artifact evidentially admissible but without protocol standing.”** The sentinel branch implements `ABSENT`; its query proves only existential reachability. Evidential admissibility is not modeled, and reports omit the submitted `se`, preventing a direct missing-evidence correspondence with the current event signature. (`P:16–17`; `D.pv:132–133,166–167,277–279`)
- **“The base result reports at least `ESTABLISHED`, `ABSENT`, or `UNVERIFIABLE`, with evidence and reasons, alongside the unchanged P4 envelope verdict.”** There is no combined result, evidence-carrying report, total-reporting query, or `UNVERIFIABLE` witness. Several failed parses terminate silently. The two paths independently receive public-channel inputs; they are not joined to one request. (`P:25–27`; `D.pv:132–133,161–175,269–274,281–300,305–317,348`)
- **“No verifier policy, strict or degraded, rewrites the reported standing value.”** There is no policy input, waiver operation, or cross-mode correspondence. Separate processes establish independence from envelope acceptance, not this universal policy property. (`P:34–35`; `D.pv:348`; `G.pv:325`)
- **“A relying-party policy may accept an artifact whose standing is `ABSENT` or `UNVERIFIABLE`, but that acceptance is the policy's own recorded decision outside the verdict…”** No relying-party decision or recording mechanism exists. (`P:35–39`; `D.pv:128–175,336–349`)
- The requirement that the mechanism be testable on an abandoned artifact presented alone **is represented**: the standing input contains one core, and S2 is reachable without requiring a competing artifact as verifier input. This is an existential test, not universal reporting correctness. (`P:19–22`; `D.pv:269–270`; `D.out:1078–1347`)
- The full **identity/lineage/terminal evidence relation is not the query relation**: `Designated(k,aid)` contains neither tuple, lineage, terminal value, nor presented signature. Its interpretation as “signed one TLR” depends on the subsequent honest-process construction and release. (`P:14–16`; `D.pv:128–145,204–210`; `F:245–260`)

The supplied text also contains adjacent obligations outside this family’s declared target. None is discharged here: refusal latching and durable local record creation; retention and verified handoff; delivery failure/expiry reporting; separate acknowledged publication and channel assumptions; observer visibility; the authority-death residual; disclosure/minimization and commitment privacy; and the full shipping-time temporal predicate. The corresponding registered passages are `P:51–63,65–79,81–103,105–119,121–135,139–155`; the complete model state and query inventory is `D.pv:128–175,189–230,336–349`.

## 2. Attacks

All six attack files retain **byte-identical `StandingDecide`, `StandingPath`, and `EnvelopePath` definitions** from D. Every run has its paired `.out`. These checks are recorded in `scratch/run-audit.txt:1–7`.

**1. Wrapper transplant — UNREACHABLE.** Reuse honest evidence and TLR while replacing the presented core by `wrapCore(inner,outer)`. Both wrapper arguments are adversary-chosen. This exercises alteration/reframing under A:5–6,11–12. (`scratch/a_wrapper.pv:179`)

```text
RESULT not event(Established(k,t_3,h(wrapCore(x,y)))) is true.
```

Source: `scratch/a_wrapper.out:1941`. The result is bounded by the fixture: no honest issuer produces a wrapper core. (`D.pv:87–89,189–230`)

**2. DSKS substitution — UNREACHABLE.** After seeing signature `s`, choose `r` and substitute `pk(dsks(s,r))` as the standing key. The query permits any signature and randomness; the library grants signature reuse under that derived key. (`A:8–10`; `tessera_theory.pvl:99–104`; `scratch/a_dsks.pv:179`)

```text
RESULT not event(Established(pk(dsks(s,r)),t_3,a)) is true.
```

Source: `scratch/a_dsks.out:1941`. The honest authority channel publishes only fingerprints of `skH1` and `skH2`; this blocks entitlement of the derived key before its signature capability can establish standing. (`D.pv:283,338–345`)

**3. Same-key, different-identity context replay — REACHABLE; all original safety queries survive.** Add an honestly published tuple naming `issuerId2` but the existing `skH1` key. Replay a core issued under `issuerId`, with its original TLR, under this second tuple. No additional authority compromise is introduced. (`A:11–12`; `scratch/a_alias_replay.pv:179,352`)

```text
RESULT not event(Established(pk(skH1[]),authTuple(issuerId2[],fp(pk(skH1[])),ssetH[],algH[],verH[]),h(attemptCore(authTuple(issuerId[],fp(pk(skH1[])),ssetH[],algH[],verH[]),p,s,d_1)))) is false.
```

Source: `scratch/a_alias_replay.out:2260`; original safety results: `484–514`. The standing path binds the key to the presented tuple but never binds that tuple to the core’s embedded tuple. This exposes a composition boundary; it does not contradict the narrow key-and-core designation correspondence. (`D.pv:274–292,312`)

**4. Honestly registered adversary-owned issuer — REACHABLE; unrestricted strict correspondence fails.** Add a public adversary key and honest authority publications for that key’s own identity. The adversary signs a lineage and terminal designation for its chosen core. This uses self-signing and manifest construction, without corrupting the honest repository channel. (`A:8–10,13–16`; `scratch/a_own_registered_key.pv:142–143,180,353`)

```text
RESULT event(Established(kX_3,t_5,aid_2)) ==> event(Designated(kX_3,aid_2)) is false.
RESULT not event(Established(pk(skA[]),authTuple(attackerId[],fp(pk(skA[])),ssetH[],algH[],verH[]),a)) is false.
```

Sources: `scratch/a_own_registered_key.out:658,2051`. Both honest-key correspondences and entitlement remain true at `668–684`.

This is a **counterexample to generalizing the event correspondence**, not proof that the adversary’s self-signed evidence lacks the three bindings. The event exists only in modeled honest issuer code. The original strict fixture cannot represent an honestly enrolled adversary-owned issuer. (`D.pv:206,338–347`; `F:250–260`)

**5. Cross-protocol tag replay — UNREACHABLE.** Add an honest foreign signing role that signs an adversary-chosen core’s TLR-shaped body under `REFUSAL`, using `skH1`. Attempt to present it as standing evidence for `fbH`. This is an explicit composition stress fixture, not a claim about any unavailable model family. (`A:11–12`; `scratch/a_foreign_tag.pv:178,339–342,357`)

```text
RESULT not event(Established(pk(skH1[]),t_3,h(fbH[]))) is true.
```

Source: `scratch/a_foreign_tag.out:1953`. Removing only the TLR tag check in this extended fixture reverses the result; see §3.

**6. Omit the TLR — ABSENT reachable; successful standing bypass not found.** Present an honest-core-shaped artifact with the `noTLR` sentinel. This is the omission control under A:5–6. (`scratch/a_omit_tlr.pv:179`; `D.pv:277–279`)

```text
RESULT not event(StandingReport(ABSENT,NO_TERMINAL_DISPOSITION_EVIDENCE,pk(skH1[]),authTuple(issuerId[],fp(pk(skH1[])),ssetH[],algH[],verH[]),h(attemptCore(authTuple(issuerId[],fp(pk(skH1[])),ssetH[],algH[],verH[]),p,s,d_1)))) is false.
```

Source: `scratch/a_omit_tlr.out:2069`. This establishes the exercised rejection outcome, not a universal missing-evidence theorem.

**UNREPRESENTABLE attacks are the principal scope finding:**

- **Signature-set stripping, duplication, and reordering:** there is one attestation-signature slot, no signature-set verifier, and no signer-set policy evaluation. Putting a tuple into that slot merely produces a failed signature parse. A:7’s operational threat is not modeled. (`D.pv:85,194–201,274,312–315`)
- **Temporal replay against anchor time:** `anchorProof` has only a digest; declared times are fresh uninterpreted names. No ordering, clock, or burial depth exists to attack. This is explicitly excluded, not an unreachable attack result. (`D.pv:35–36,103–104,191,289`; `P:139–155`; `F:169–175`)
- **Suppression or misassociation of the required complete report:** reports have no request identifier or submitted-evidence field, and there is no completion event. The current queries cannot express “this submitted bundle received no report” or join its standing and envelope results. (`P:25–27`; `D.pv:132–133,269–270,305–317`)
- **Actual cross-family replay:** no other family’s process is supplied. Attack 5 supplies a bounded extra role; it cannot discharge composition with absent implementations. (`scratch/a_foreign_tag.pv:339–342`)

## 3. Mutations

All registered queries were retained. The complete dependency matrix, including **every individual RESULT line reference**, is `scratch/dependency-index.txt:1–35`; exact source changes are in `scratch/mutations.diff:1` onward.

Notation: **U** = unrestricted correspondence; **H1/H2** = honest-key correspondences; **E** = unentitled standing unreachable; **R** = reason collapse unreachable. Baseline D/R satisfy all five; G already fails U. **“Same” means all baseline truth values survive.** N1 remains reachable in every listed mutant. (`scratch/committed-index.txt:1–33`; `scratch/dependency-index.txt:1–35`)

| Single removal/unbinding | D safety | R safety | G safety | Vocabulary change | Matrix evidence |
|---|---|---|---|---|---|
| DNS evidence check | Same | U fails | — | None | `scratch/dependency-index.txt:2` |
| Repository evidence check | U fails | Same | — | None | `…:3` |
| Sole-channel evidence check | — | — | Same | None | `…:4` |
| Authority digest equality, each channel separately | U fails only when honest channel unbound | Same rule | Same | None | `…:5–7` |
| Authority tag equality, each channel separately | Same | Same | Same | None | `…:8–10` |
| Standing entitlement fingerprint | U,E fail | U,E fail | E fails | None | `…:11` |
| Presented-key equality `kT=kX` | Same | Same | Same | None | `…:12` |
| TLR verification key bound to `kT` | U,H1,H2 fail | U,H1,H2 fail | H1,H2 fail | None | `…:13` |
| TLR domain tag | Same | Same | Same | None | `…:14` |
| Anchor-proof check | Same | Same | Same | None | `…:15` |
| Identity argument of lookup; attacker supplies lookup identity | Same | Same | Same | None | `…:16` |
| Entire lookup bypassed, supplying `DISP_SHIPPED` | Same | Same | Same | Mismatch witness disappears | `…:17` |
| Derived verification identity; accepted-event identity remains actual `h(core)` | U,H1,H2 fail | U,H1,H2 fail | H1,H2 fail | None | `…:18` |
| Terminal identity equality | Same | Same | Same | S2 disappears | `…:19` |
| Entire terminal predicate; per-entry check retained | Same | Same | Same | S2,S4 disappear | `…:20` |
| Per-entry `DISP_SHIPPED` check | Same | Same | Same | None | `…:21` |
| Refused-terminal branch | Same | Same | Same | S4 disappears | `…:22` |
| Missing-evidence branch | Same | Same | Same | S3 disappears | `…:23` |
| Each envelope authority check separately | Same | Same | Same | None | `…:24–26` |
| Envelope fingerprint | Same | Same | Same | None | `…:27` |
| Envelope embedded tuple equality | Same | Same | Same | None | `…:28` |
| Envelope possession verification | Same | Same | Same | None | `…:29` |
| Envelope bytes verification | Same | Same | Same | None | `…:30` |
| Each envelope frame equality: algorithm, issuer, fingerprint | Same | Same | Same | None | `…:31–33` |
| Envelope manifest digest | Same | Same | Same | None | `…:34` |
| Entire envelope process | Same | Same | Same | None | `…:35` |

Here `…:n` means `scratch/dependency-index.txt:n`. Each grouped row represents separate runs, not a combined mutation.

**Inert against the complete registered query set:** compromised-channel evidence/digest checks; authority tags; presented-key equality; TLR tag in the original fixture; anchor binding; lookup-identity binding; per-entry disposition; and every tested envelope check. (`scratch/dependency-index.txt:2–16,21,24–35`)

Their reasons differ:

- Compromised-channel checks add no restriction because the adversary has the signing key. (`D.pv:343`; `R.pv:345`; `G.pv:321`)
- Entitlement and the signature check constrain establishment independently of `kX`; the queried accepted key is `kT`. (`D.pv:253–255,283–287`)
- Anyone can construct the anchor term. (`D.pv:103–104`)
- Terminal designation and the fixed honest TLR shapes make lookup-identity and per-entry checks redundant for these queries. (`D.pv:204–210,228–229,250–252`; `scratch/dependency-index.txt:16,21`)
- Original honest signers emit no alternative-tag signature with a compatible TLR body. This fixture restriction hides domain-separation dependence. (`D.pv:193–210,217–230`)
- Envelope acceptance is unqueried and never gates standing. (`D.pv:143–175,305–317,348`)

**Terminal comparison is safety-inert, not wholly inert:** removing it destroys S2 reachability. Removing the full terminal predicate while preserving the entry check still leaves U/H1/H2 true in strict mode. Companion C removes both protections. Its red cannot isolate terminal checking as the safety dependency. (`scratch/m_dns_terminal_predicate.out:426–450,1037,1169`; `Q4.pv:219–225`)

**Composition changes inertness.** In attack 5’s fixture, unbinding only `TLR` makes U and H1 false; H2, E, R and the witnesses survive. The targeted replay becomes:

```text
RESULT not event(Established(pk(skH1[]),t_3,h(fbH[]))) is false.
```

Sources: `scratch/m_foreign_tlr_tag.out:595–751,2201,2340`. Thus “inert” here is a fixture/query observation, not permission to remove a check.

Eight initial parsing failures lacked types on new pattern variables; those exact `.pv/.out` pairs remain as `*_parsefail`. Corrected runs are separate retained files. They are not proof results. (`scratch/m_dns_tlr_tag_parsefail.out:1–2`; `scratch/m_dns_authority_digestR_parsefail.out:1–2`; `scratch/run-audit.txt:7`)

## 4. Vacuity

**Every committed N1 witness is reachable with a derivation and reconstructed trace.** These are existential witnesses; they do not independently establish reachability for each honest key or every branch. (`D.pv:157–159`; `G.pv:138–140`)

| Output | Derivation starts | Trace found | N1 RESULT |
|---|---:|---:|---:|
| D.out | 495 | 780 | 781: `not event(HonestStandingEstablished(...)) is false` |
| R.out | 495 | 780 | 781: same |
| G.out | 623 | 916 | 917: same |
| Q2.out | 1192 | 1513 | 1514: same |
| Q3.out | 871 | 1156 | 1157: same |
| Q4.out | 1139 | 1424 | 1425: same |
| Q5.out | 495 | 780 | 781: same |

All five vocabulary witnesses in D/R/G/Q2/Q3 have derivations and traces. Q4 intentionally loses S2/S4; Q5 replaces two distinct vocabulary queries with one collapsed-code query. Therefore “every vocabulary witness is reachable in every companion” would be false. (`scratch/committed-index.txt:6–10,17–21,28–32,40–44,51–55,62–66,73–76`; `Q4.pv:19–21`; `Q5.pv:15–20`)

| Companion | Actual safety failures | Other outcomes | Matches named query polarities? |
|---|---|---|---|
| Q2 | U,H1,H2 and wrapper correspondence | E,R hold; N1 and five vocabulary witnesses reachable | Yes: `Q2.pv:16–29`; `Q2.out:630,808,986,1176,1182,2352`. |
| Q3 | U and E | H1,H2,R hold; all witnesses reachable | Yes: `Q3.pv:19–25`; `Q3.out:628,642,656,860,2062`. |
| Q4 | U,H1,H2 | E,R hold; S2/S4 unreachable as announced | Yes, including announced witness losses: `Q4.pv:19–27`; `Q4.out:576,849,1123,1129,1708,1838,2015`. |
| Q5 | R only | Correspondences and E hold; revised witnesses reachable | Yes: `Q5.pv:22–29`; `Q5.out:457–484,1965`. |

The matching query polarities do not validate every claimed trace interpretation. In particular, Q2’s wrapper trace contains `wrapCore(a_4,a_5)`, with no binding of `a_4` to the honest shipped core. (`Q2.out:1166–1176`)

## 5. Verdict on each header’s honesty

**D — conditional fixture theorem; load-bearing annotation overstates independence.** The “This model proves” statement is supported when read together with its fixed honest-issuer fixture and stated idealizations. It is not the full registered reporting theorem. The wording **“aid := h(core) computed by the verifier and looked up in the lineage (Q2); terminal = TERM_SHIPPED(aid) (Q4)”** labels a package as load-bearing although lookup-identity unbinding changes no query, and terminal removal does not break safety. (`D.pv:20–55,62–65`; `scratch/dependency-index.txt:16,18–20`)

The phrase **“under the A1.3 adversary”** needs the additional signature-set and composition limitations stated in §2. An honestly enrolled adversary-owned key already falsifies the unrestricted event correspondence; this should not be reported as failure of the prose’s three evidence bindings. (`D.pv:20–30`; `A:7–12`; `scratch/a_own_registered_key.out:658–684`)

**R — same verdict, independently tested.** Its theorem has the same fixture limitation, and its corresponding load-bearing annotation has the same redundancy problem. The honest channel’s evidence/digest binding matters; the compromised repository check does not. (`R.pv:22–57,64–67`; `scratch/dependency-index.txt:2–6,16–20`)

**G — narrow proof claim supported; broader interpretation remains conditional.** **“for EACH HONEST KEY the A3.7.1 correspondence still holds”** matches the two results, and the header explicitly excludes U and admits that degraded verdict labeling is unqueried. It does not establish complete A3.7.1 reporting or the labeling proviso. Its load-bearing terminal annotation has the same safety redundancy. (`G.pv:15–39`; `G.out:589–613`; `scratch/dependency-index.txt:19–20`)

**Q2 — overclaim in the claimed wrapper trace.** Verbatim: **“a wrapper-shaped outer artifact around the honest shipped core.”** The event only checks wrapper shape; neither query nor emitted event binds its inner value to an honest designation. The committed trace uses arbitrary inner and outer values. The weaker claim—transplant onto a wrapper-shaped core—is discharged. (`Q2.pv:34–39,143–146,253–261`; `Q2.out:1166–1176`)

**Q3 — claimed detection supported.** **“the envelope's fingerprint check cannot shadow the standing path's missing one”** matches the independent processes and reachable unentitled-standing judge. The header’s prose mentions `KEY_FINGERPRINT_MISMATCH`, but no such report is emitted: the envelope stops at a failed guard. (`Q3.pv:19–35`; `Q3.out:860`; `D.pv:311–317`)

**Q4 — causal overclaim.** Verbatim: **“LOAD-BEARING for the red: the removed terminal check. Else as Q1.”** The mutant ignores both `d` and `terminal` and changes issuer fixtures. Removing terminal decisions alone while preserving `d` does not produce its safety red. The “This model proves” sentence therefore needs to name the combined removal, rather than attribute detection specifically to an unchecked terminal disposition. (`Q4.pv:9–18,31–35,219–225`; `scratch/dependency-index.txt:20`)

**Q5 — claimed scope supported.** **“the ReasonCollapsed judge carried in Q1 can fail”** is exactly what its red establishes. Its explicit restriction to model constants is necessary: it proves neither implementation discrimination nor complete reporting. (`Q5.pv:25–35`; `Q5.out:1964–1965`)