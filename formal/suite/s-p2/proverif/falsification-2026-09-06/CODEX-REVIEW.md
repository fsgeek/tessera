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