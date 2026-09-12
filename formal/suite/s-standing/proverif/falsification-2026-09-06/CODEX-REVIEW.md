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