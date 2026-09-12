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