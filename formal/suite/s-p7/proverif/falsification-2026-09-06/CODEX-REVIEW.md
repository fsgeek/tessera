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