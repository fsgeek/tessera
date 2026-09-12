from pathlib import Path
import re
head='''## 1. Correspondence audit

**The largest gap is unrepresentable signature-set and byte-encoding attacks, not a recovered counterexample to the closed correct models.** Each verifier accepts one `sg`; `ss` is uninterpreted, and canonical bytes are a free `framed` term. A1.3 expressly permits signature-set operations and arbitrary byte alteration. (`A1.3-adversary.txt:5–12`; `proverif/sp1_q2_degraded_compromised.pv:110–121`; `tessera_theory.pvl:119–131`.)

Citation abbreviations below expand to these exact files; `.out` replaces `.pv` when specified:

- **D** = `proverif/sp1_q1_strict_dns_compromised.pv`.
- **R** = `proverif/sp1_q1_strict_repo_compromised.pv`.
- **G** = `proverif/sp1_q2_degraded_compromised.pv`.
- **A** = `proverif/sp1_q3_companionA_sig_unbound.pv`.
- **B** = `proverif/sp1_q4_companionB_frame_unsigned.pv`.

**Licensing standard.** The property says: “There is no reachable state in which the verifier returns `VALID_STRICT` or `VALID_DEGRADED` for a package whose canonical bytes differ from bytes signed at issue time.” It also says Tessera attests “the identity of the framed bytes presented at an issuance event” and registers “existential issuance-event authenticity.” These license byte binding and a non-injective issuance correspondence, not a particular authority/manifest algorithm. (`REGISTERED-PROPERTY.txt:1–4,8–13,15–21`.)

The following is the complete accepting-path check inventory for **each** correct verifier. “Added” means an implementation condition not prescribed by the supplied property/adversary text; it does not mean forbidden. The frozen plan explicitly chooses several such conditions, as noted below. (`REGISTERED-PROPERTY.txt:1–27`; `A1.3-adversary.txt:1–16`; `PREDICTIONS-frozen.md:124–174`.)

| Check, including structural matches | D | R | G | License |
|---|---|---|---|---|
| Typed input: seven fields strict, six degraded; one `pkey`, one attestation signature | D:110–111 | R:110–111 | G:110–111 | Added wire/typing abstraction; singleton scope chosen in frozen plan:130–133. |
| DNS/sole evidence signature verifies under configured authority key; recovered pair has `STMT_DIGEST` and exactly `h(t)` | D:113 | R:113 | G:112 | Added concrete mechanism; channel threat is A1.3:15–16; digest form chosen in frozen plan:134–135,166–174. |
| Repository evidence: same three conditions, independently checked | D:114 | R:114 | — | Added; two-channel strict mechanism chosen in frozen plan:166–169. |
| `t` decomposes as five-field `authTuple(id,kfpr,ss,alg,ver)` | D:115 | R:115 | G:113 | Added manifest schema; frozen plan:134–135. |
| Presented key fingerprint equals manifest `kfpr` | D:116 | R:116 | G:114 | Added key binding; frozen plan:139–142. |
| Possession signature verifies under `kX`; recovered pair has `POSS` and exactly `t` | D:117 | R:117 | G:116 | Added proof-of-possession mechanism; frozen plan:136–138; library:37–45. |
| Attestation signature verifies under `kX`; recovered pair has `BYTES` and exactly presented `fb` | D:119 | R:119 | G:118 | Exact-byte binding implements property:1–3,8–10,20–21; tag/key-specific construction is an added realization. |
| `fb` decomposes as seven-field `framed`; frame algorithm equals manifest `alg` | D:120 | R:120 | G:120 | Added schema and identifier consistency, not algorithm suitability. |
| Frame issuer identity equals manifest `id` | D:120 | R:120 | G:120 | Added identifier consistency, not independently authenticated identity. |
| Frame fingerprint equals `fp(kX)` | D:120 | R:120 | G:120 | Added in-frame key binding. |
| Frame manifest hash equals `h(t)` | D:121 | R:121 | G:121 | Added in-frame manifest binding. |

In that table, “property” means `REGISTERED-PROPERTY.txt`, “A1.3” means `A1.3-adversary.txt`, “frozen plan” means `PREDICTIONS-frozen.md`, and “library” means `tessera_theory.pvl`. The frame construction is fixed by the frozen plan:70–75,126–142; none of its individual identifier comparisons is specified by the supplied property:1–27.

**Judge filters are not verifier checks.** H matches acceptance to a privately enumerated honest key; N1 matches both key and bytes to an issuance report. They do not constrain public acceptance. D/R enumerate two keys; G does likewise. (`D:125–148`; `R:125–148`; `G:140–163`.)

**Registered requirements without a corresponding check/discharge:**

- **Both valid verdicts:** no verdict variable, failure classification, or waiver check exists; only `Accept`/`AcceptS`. The frozen plan explicitly defers the join, but nothing supplied discharges it. (`REGISTERED-PROPERTY.txt:1–3`; `D:109–123`; `R:109–123`; `G:109–123`; `PREDICTIONS-frozen.md:46–59,435–447`.)
- **Canonical-byte identity:** no serialization, parsing-to-canonical-bytes function, or injectivity obligation is checked. Term equality is the substitution. (`REGISTERED-PROPERTY.txt:3,8–10`; `G:68–69,118–121`; `PREDICTIONS-frozen.md:113–117`; `tessera_theory.pvl:119–131`.)
- **All accepted packages:** G's proved correspondence excludes adversary-held keys, while its unrestricted query fails. The frozen plan argues these excluded cases do not violate P1; that argument is not an all-keys issuance-event theorem in this family. Self-signing alone explains the red query and is not evidence of changed unsigned bytes. (`REGISTERED-PROPERTY.txt:1–3,20–21`; `G:85–105,140–143`; `G.out:173,499`; `PREDICTIONS-frozen.md:94–112`.)
- **Signature-set operations:** “Strip, reorder, or duplicate signatures within the signature set” has no set representation or membership/completeness check. `ss` and `ver` are only destructured; one `sg` is verified. The P2 excerpt itself stops at “The canonical”, so a full P2 obligation cannot be reconstructed. (`A1.3-adversary.txt:7`; `REGISTERED-PROPERTY.txt:6`; `D:110–121`; `R:110–121`; `G:110–121`.)
- **Wrappers, receipts, re-framing, and anchoring:** no wrapper/receipt parser, anchor process, or interpretation of object type is present; arbitrary payload terms are not an encoding of those protocols. (`A1.3-adversary.txt:5–14`; `G:109–137`; `PREDICTIONS-frozen.md:450–456,492–502`.)
- **Channel subsets generally:** D/R cover either single compromise of two keys, not arbitrary channel counts. G publishes its only authority key, a stronger exposure than a proper subset of a one-channel universe; the unmodeled unavailable honest channel/waiver must not be inferred. (`A1.3-adversary.txt:15–16`; `D:136–147`; `R:136–147`; `G:152–162`; `PREDICTIONS-frozen.md:166–182`.)

Replay prevention and semantic truth are **not missing requirements**: “Re-presenting a genuinely issued package preserves identity; P1 permits it”; meaning and truth are outside the attestation. Object-type/profile validation is also not required by this supplied P1 text, although headers misleadingly call those carried checks. (`REGISTERED-PROPERTY.txt:11–21`; `D:42–47`; `R:42–47`; `G:40–46`.)

## 2. Attacks

**UNREPRESENTABLE:** stripping/reordering/duplicating a genuine multi-signature package, or changing concrete encodings while preserving a symbolic frame, cannot be tested against these unchanged verifiers. Encoding signatures as a tuple inside `sg` merely makes `checksign` fail; encoding them inside payload never checks set semantics. This is a coverage failure, not an unreachable attack. (`A1.3-adversary.txt:5–12`; `G:110–121`; `tessera_theory.pvl:98–104`; `PREDICTIONS-frozen.md:113–133`.)

All attack fixtures keep G's verifier byte-for-byte unchanged; the generator asserts this. A1–A4 use three honest parties and fixed honest payloads, so the target altered payload was never requested from those parties. Target reports run in parallel with protocol processes. (`scratch/build_attacks.py:72–78`; `scratch/a1_payload_tamper.pv:152–195`.) A1–A4 and cross-mode replay exercise A1.3:5–12; the foreign-type fixture adds a legitimate signed object to exercise that replay boundary. G's exposed sole evidence key is retained (`scratch/a4_dsks_resign.pv:177–195`).

| Attempt and concrete target | Outcome and exact RESULT |
|---|---|
| **A1 payload substitution:** replace `goodPayload` with `alteredPayload`, retain honest key and binding fields; adversary has the original signature. (`scratch/a1_payload_tamper.pv:181–195`.) | **Unreachable:** `RESULT not event(Attack) is true.` (`scratch/a1_payload_tamper.out:582`.) |
| **A2 extra-party swap:** present first issuer's frame under the third honest issuer's key. (`scratch/a2_party_swap.pv:177–195`.) | **Unreachable:** `RESULT not event(Attack) is true.` (`scratch/a2_party_swap.out:583`.) |
| **A3 DSKS replay:** derive `dsks(observed,dsksSalt)` after the first honest signature; try that key with the original frame. The library permits signature verification, but the frame's fingerprint cannot equal the derived key's fingerprint. (`scratch/a3_dsks_replay.pv:181–188`; `G:120`; `tessera_theory.pvl:99–117`.) | **Unreachable:** `RESULT not event(Attack) is true.` (`scratch/a3_dsks_replay.out:585`.) |
| **A4 DSKS re-signing:** use the held derived key to sign an altered payload in a new consistent frame, with an attacker-chosen signer-set term and forged sole-channel evidence. This changes the key and signs the new bytes; it does not break honest-key P1. (`scratch/a4_dsks_resign.pv:181–195`.) | **Reachable:** `RESULT not event(Attack) is false.` Trace found at :782; headline remains true at :242. (`scratch/a4_dsks_resign.out:242,782–783`.) |
| **A6 foreign type/version:** add honest issuance of `OT_WRAPPER` with `badVersion`, then present it to unchanged G. The verifier accepts without interpreting either field; this is unchanged signed-byte replay, not a P1 counterexample. (`scratch/a6_foreign_type.pv:153–160,188–195`; `G:120`.) | **Reachable:** `RESULT not event(Attack) is false.` (`scratch/a6_foreign_type.out:746–747`.) |
| **A7 cross-model replay:** copy Q1's issuer body, sharing its terms/key with G, and submit its signed frame to the degraded verifier. No mode/context appears in the signed frame. (`scratch/a7_cross_mode.pv:161–170,189–205`; `D:98–106`.) | **Reachable:** `RESULT not event(Attack) is false.` Permitted replay, not P1 failure. (`scratch/a7_cross_mode.out:746–747`; `REGISTERED-PROPERTY.txt:15–21`.) |

**Conditional composition break (A8):** add B's payload-only signing endpoint under the same honest key. Ask it to sign a complete attacker-chosen inner frame as its payload; replay that signature to the correct G verifier. B emits `IssuerSigned` for the outer frame, G accepts the inner frame, and no matching issuance event exists. (`scratch/a8_cross_broken_endpoint.pv:161–169,198–206`; `scratch/a8_cross_broken_endpoint.out:919–948`.)

`RESULT event(AcceptedUnderHonestKey(k,fb_5)) ==> event(IssuerSigned(k,fb_5)) is false.` (`scratch/a8_cross_broken_endpoint.out:428`.)
`RESULT not event(Attack) is false.` (`scratch/a8_cross_broken_endpoint.out:948`.)

This falsifies unrestricted composition of the correspondence, **not the original correct fixture under A1.3**: the added endpoint is explicitly broken. The accepted inner bytes really do have a valid honest-key signature; the mismatch is with the endpoint's issuance-event record. Same-key cross-protocol signing behavior is therefore a required composition assumption. (`B:18–28`; `scratch/a8_cross_broken_endpoint.pv:161–169`; `scratch/a8_cross_broken_endpoint.out:925–935`.)

**Unresolved attempt A5:** the judge demanding two identical acceptance reports returned `RESULT not event(Attack) cannot be proved.` Explicit verifier copies and an injectivity diagnostic did not reconstruct a trace either. This is **inconclusive**, not reachable or unreachable; the diagnostic is not a registered freshness requirement. (`scratch/a5_repeat_replay_uncertain.out:688–689`; `scratch/a5_repeat_replay.out:736–737`; `scratch/a5_injective_diagnostic.out:800–802,1249–1250`; `REGISTERED-PROPERTY.txt:15–21`.)

**Review correction:** initial attack harnesses put a private target output before starting its receiver, blocking execution; their `cannot be proved` results are retained under `scratch/initial/` and are not attack evidence. The corrected fixtures place this output in parallel. (`scratch/initial/a4_dsks_resign.pv:188–195`; `scratch/initial/a4_dsks_resign.out:819`; `scratch/a4_dsks_resign.pv:188–195`.)

## 3. Mutations

Each mutant starts from its original correct model and removes/unbinds one check, never another mutant. Whole signature/evidence removals are distinguished from their individual key, tag, and message equalities. `tuple_binding` replaces the manifest pattern with attacker-supplied fields; `frame_binding` removes the whole compound frame pattern, retaining an independently supplied `mh` for the later hash check. These last two are compound-pattern ablations, not single-field ablations. (`scratch/build_mutants.py:4–35`; `scratch/m_D_poss_key.pv:118–119`.)

Matrix entries are **H/U/N**: honest-key correspondence / unrestricted correspondence / honest witness. **T** = correspondence true; **F** = correspondence false with attack; **r** = witness reachable (`not event(...) is false`). Citations span all three RESULT lines in each output. Query definitions: `D:78–88`; `R:78–88`; `G:85–105`. Mutant filenames are the cited output filename with `.pv` substituted.

| Removed/unbound check | D: H/U/N | R: H/U/N | G: H/U/N |
|---|---|---|---|
'''
rows=['evD','evD_tag','evD_digest','evD_key','evR','evR_tag','evR_digest','evR_key','ev','ev_tag','ev_digest','ev_key','tuple_binding','fp','possession','poss_tag','poss_manifest','poss_key','signature','sig_tag','sig_bytes','sig_key','frame_binding','frame_alg','frame_id','frame_fp','manifest_hash']
lines=[]
for row in rows:
 cells=[]
 for mode in 'DRG':
  p=Path(f'scratch/m_{mode}_{row}.out')
  if not p.exists(): cells.append('—');continue
  results=[(i,s) for i,s in enumerate(p.read_text().splitlines(),1) if s.startswith('RESULT')]
  assert len(results)==3
  assert all('cannot' not in s for _,s in results)
  def truth(term):
   n,s=next((n,s) for n,s in results if term in s)
   return ('T' if s.endswith('is true.') else 'F')
  H=truth('event(AcceptedUnderHonestKey(')
  U=truth('event(AcceptS(' if mode=='G' else 'event(Accept(')
  assert truth('event(HonestAccepted(')=='F'
  cells.append(f'**{H}/{U}/r** (`{p}:{results[0][0]}–{results[-1][0]}`)')
 lines.append('| `'+row+'` | '+' | '.join(cells)+' |')
foot='''

**Inert for all three registered queries:** in D/R, compromised evidence (including key/tag/digest), the honest-evidence tag alone, possession and all its equalities, signature tag alone, frame binding/individual fields, and manifest hash. In G, everything except whole attestation verification and its byte/key equalities is inert. “Inert” here means unchanged query outcomes, not unchanged accepted language; G's unrestricted query was already false. (Matrix above; baselines `D.out:201–396`; `R.out:201–396`; `G.out:173–499`.)

**Why:** with an honest accepted key, the retained signature-byte/key check forces a signature released by an issuance process. In this closed fixture the other signatures under honest issuer keys are only `POSS` over `authTuple`, so dropping `BYTES` cannot supply a signature over a `framed` message. Honest authority keys sign only `STMT_DIGEST`, making that tag separately inert. For unrestricted strict acceptance, the honest authority key/digest, tuple binding and manifest fingerprint are necessary to exclude attacker-held keys. (`D:90–121,136–147`; `R:90–121,136–147`; `G:129–137`; `tessera_theory.pvl:98–104`; matrix.)

The strict fingerprint dependency is empirically red, not merely inferred. The strict headers' inventory also omits the manifest-destructuring dependency; the whole attestation check contains two separately necessary bindings (key and bytes). No single-removal experiment proves that several inert checks can safely be removed together. (`D:34–47`; `R:34–47`; `scratch/m_D_fp.out:362`; `scratch/m_R_fp.out:362`; `scratch/m_D_tuple_binding.out:387`; `scratch/m_R_tuple_binding.out:387`; matrix.)

## 4. Vacuity

The committed outputs contain a derivation **and a reconstructed trace** for each declared N1 witness. Exact witness RESULT for every row: `RESULT not event(HonestAccepted(k,fb_3)) is false.` (`D:86–88`; `R:86–88`; `G:88–90`; `A:56–58`; `B:53–55`.)

| Model | Derivation starts | Witness trace/event | RESULT |
|---|---|---|---|
| D | D.out:215 | D.out:392–395 | D.out:396 |
| R | R.out:215 | R.out:392–395 | R.out:396 |
| G | G.out:180 | G.out:345–348 | G.out:349 |
| A | A.out:338 | A.out:506–509 | A.out:510 |
| B | B.out:335 | B.out:500–503 | B.out:504 |

**Companion selectivity:** A and B each turn the named honest-key correspondence from G's true to false; their unrestricted query was already false in G, and N1 remains reachable. Thus exactly one correspondence changes relative to G, but each companion has **two false correspondences**, not one. (`G.out:173,349,499`; `A.out:331,510,663`; `B.out:328,504,654`; `A:18–34,66–68`; `B:15–31,63–65`.)

A's trace records an honest frame with payload `a_2`, then accepts a different frame with type `a_4`, version `a_5`, payload `a_6`. It is not a request to sign the accepted frame. B preserves payload `a_2` but changes type/version; its issuance event reports the intended full frame although its signature covers payload only. (`A.out:315–331`; `B.out:312–328`; `B:18–23`.)

N1 is existential, not coverage of every honest issuer or every payload: the committed witness traces use `skI2`. Reachability therefore excludes total deadness but does not establish branch-by-branch non-vacuity. (`D:87–88`; `R:87–88`; `G:89–90`; `D.out:392`; `R.out:392`; `G.out:345`; `A.out:506`; `B.out:500`.)

## 5. Verdict on each header's honesty

- **D:** the core “This model proves” statement matches the two proved symbolic correspondences within its fixed producer fixture; no counterexample to those original queries was obtained. It does not discharge unrestricted real canonical-byte P1. Its scope exclusions explicitly acknowledge verdicts, multi-signers and encoding. (`D:16–33`; `D.out:201–208`; `REGISTERED-PROPERTY.txt:1–3`.)
- **R:** same verdict, independently supported by its own committed results and mutations. The load-bearing authority role reverses correctly. (`R:16–41`; `R.out:201–208`; `scratch/m_R_evD.out:349`; `scratch/m_R_evR.out:198`.)
- **G:** “framed bytes accepted under an honest issuer's key are exactly the bytes that issuer signed at an issuance event” accurately states its conditional query. Calling this “the [model] binding half of P1” must retain the honest-key, term-equality and closed-producer qualifications; the all-keys contrast is false and composition A8 fails. (`G:18–33`; `G.out:173,499`; `scratch/a8_cross_broken_endpoint.out:428`; `PREDICTIONS-frozen.md:94–117`.)
- **A:** “This model exists to go RED on the headline” and “It discharges nothing” match the outputs. Its corrected field description matches the trace; the earlier payload-only account survives solely as a visible correction note. (`A:18–34,119–135`; `A.out:315–331`.)
- **B:** “It discharges nothing. It proves nothing about P1” is consistent with a deliberately broken producer/verifier pair. Its `IssuerSigned` event describes intended framing, not the actual payload-only signature message; its red is evidence about this explicit mutation. (`B:15–31,85–93`; `B.out:312–328`.)

**Verbatim inventory overclaims:** D/R list “object type (P7); canonicalization version and algorithm profile (P8/H1a)” under “Carried checks”; G similarly lists “object type (P7); canonicalization version and algorithm profile (P8/H1a)”. There are no such validation checks: `ot`/`cv` are unconstrained variables and `alg` is merely compared to the manifest identifier. These should be described as signed fields or external obligations, not carried checks. (`D:42–47,120`; `R:42–47,120`; `G:40–46,120`; `scratch/a6_foreign_type.out:747`.)

**Verbatim adversary overclaim in the frozen plan:** “items 2–6 are present” is false for signature-set operations and anchoring, and overstates semantic cross-type/context coverage. Those attacks have no corresponding state or parser here. The header's narrower DSKS claim is supported by the library and A3/A4 probes; it does not repair these missing capabilities. (`PREDICTIONS-frozen.md:160–162`; `A1.3-adversary.txt:7–16`; `G:109–137`; `tessera_theory.pvl:99–104`; `scratch/a3_dsks_replay.out:585`; `scratch/a4_dsks_resign.out:783`.)
'''
report=head+'\n'.join(lines)+foot
Path('REVIEW.md').write_text(report)
print('Report lines:',len(report.splitlines()))
# All executed model files retained with their matching output.
missing=[str(p) for p in Path('scratch').rglob('*.pv') if not p.with_suffix('.out').exists()]
assert not missing,missing
print('PV/output pairs:',len(list(Path('scratch').rglob('*.pv'))))
