| Exit row | Companion / query / slice | Verdict | What this trace establishes |
|---|---|---|---|
| D10 | C-C3 C-Q5 `SetAltered`, depth0.cone | **Registered mechanism** | The consumer accepts an altered manifest using an honest key's reusable fingerprint-only possession proof. Both protections are severed. |
| D10 | C-C8 C-Q5 `SetAltered`, depth0.cone | **Registered mechanism** | The same consumer failure, not merely C-Q9's structural red. |
| D2 | C-C4 C-Q4 `Rescoped`, depth1.cone | **Registered mechanism** | Existing honest inner bytes are re-signed and attributed to an attacker key at L1. |
| D2 | C-C4 link 6b, depth1.cone | **Different but valid attack within case (d)** | An entirely attacker-made inner frame has a fingerprint inconsistent with the accepting key. No honest-byte reattribution occurs in this trace. |
| D6 | C-C7(i) C-Q8, depth0.cone | **Registered mechanism** | Same-key signature verification succeeds over different bytes; matches the structural family attack. |
| D6 | C-C7(i) link 4, depth0.cone | **Registered mechanism** | The same accepted triple breaks the consuming linkage check. |
| D6 | C-C7(i) `AcceptedUnderHonestKey ==> IssuerSigned`, depth0 | **Registered mechanism** | An honest wrapper signature authenticates attacker-built attestation bytes under that same honest key. |
| D6 | C-C7(ii) C-Q8, depth0.cone | **Registered mechanism** | Attacker-signed non-attestation bytes trigger the registered type-conditional waiver. |
| D6 | C-C7(ii) link 4, depth0.cone | **Registered mechanism** | The same waiver breaks the consuming linkage check. |
| D7 membership | C-C17 link 2a, depth0.cone | **Registered mechanism** | Slot B is satisfied by a key its manifest does not name; matches the structural family trace. |
| D7 membership | C-C17 `SignerForged`, depth0 | **Registered mechanism** | The genuine M2 slot B is satisfied by an attacker key, with genuine slot-A material. |
| D1 | C-C2 link 5, depth0.cone | **Different but valid attack within case (d)** | Both fingerprint and hash are wrong in attacker-made frames. This is not the cited honest-frame reattribution attack. |

Reviewed 2026-10-06 against live files at HEAD `77c92a5ec1fa5f8fe03d7c56ae293af91f8e6da6`. **No artifact among these twelve reconstructed reds. D10 really does have consumer-failure evidence.** The two “different” verdicts deliberately distinguish structural counterexamples from the cited family attacks on existing honest bytes. They still exploit the registered mutations and falsify the registered set-(1) links. They do not independently demonstrate the honest-provenance attacks.

Paths below are relative to `formal/suite/capstone/proverif/dev/slice_probe/`, unless qualified. `PREDICTIONS` means `formal/suite/capstone/PREDICTIONS.md`; `family/` means `formal/suite/ledger-tests-2026-09-14/`. All slice trace line numbers refer to the original **out/** files, including their exploratory banner. Each named `.out` has the same-stem `.pv` in `gen_ext/`, except C-C2 link 5 in `gen/`. These are mechanism verdicts, not a change to registration/discharge status or a review of the unrequested retained sets, isolation runs, or witnesses.

### D10 — C-C3 C-Q5

File: `out/cap_cc03_d__depth0.cone__cq5.out`.

- Lines **777–787** disclose the sole authority key and release skB2's fingerprint-only possession proof plus an honest frame/signature for its assigned two-signer manifest M2.
- Line **799** reuses that exact frame/signature and proof, but supplies a forged one-signer manifest naming skB2 alone, with attacker-chosen version `a_6`.
- Lines **805–815** accept that altered manifest at L0; the accepted frame still hashes M2, and the accepted possession proof still recovers `(POSS, fp(pk(skB2)))` rather than `(POSS, accepted_manifest)`.
- Lines **819–827** join the genuine `(pk(skB2), M2)` member report to this same accepted slot and fire `SetAltered`. No key reuse across honest manifests or DSKS step explains the red.

**Registered mechanism.** PREDICTIONS **1772**, MUTATES and case-(d) set (1), names the combined removal of the frame hash pin and possession-over-manifest. Its cited family output is actually under `formal/suite/s-p2/proverif/sp2_q5_c2_fponly_frame_nomh.out`: **523–535** likewise moves honest skB2 from its two-signer manifest to a forged one-signer tuple. The family uses `framedNoMh`; the capstone keeps the seventh field but does not check it. That preserves the mechanism.

**The producer/consumer answer is yes, with the registered qualification.** C-Q9's exact possession relation fails on the *same accepted material* that reaches C-Q5. Restoring its `(POSS, t)` check rejects this fingerprint-only proof; restoring `mh = h(t)` rejects this frame. C-Q9 unbinding **alone** is not enough to establish C-Q5 failure. Both routes must be removed, as registered. The source checks and consumer are `../../cap_cc03_d.pv:609–618,1011–1017`; the one-key/one-manifest restriction is PREDICTIONS **643–658**.

**Slice loss:** removes PossJudge, honest authorities, standing, wrappers and unrelated judges/producers; retains skB2's Attester, member reports, Front, AttestStage and MemberJudge. Removing PossJudge deletes an observer, not the possession check or its evidence. The leak and both severed checks are unchanged. Nothing this attack needs is removed.

### D10 — C-C8 C-Q5

File: `out/cap_cc08_d__depth0.cone__cq5.out`.

- Lines **777–787** supply the compromised authority key and genuine skB2 proof/frame material tied to M2.
- Line **799** packages that material with a new one-signer tuple naming skB2 and forged authority evidence for that changed tuple.
- Lines **809–815** accept the new tuple despite the frame's old manifest hash and the possession proof's fingerprint-only message.
- Lines **819–827** compare the accepted tuple with skB2's M2 membership and reconstruct `SetAltered`; this is the consumer's own failure.

**Registered mechanism.** PREDICTIONS **1777** explicitly separates (α) set integrity, requiring both removals, from (β) possession-message correctness, falsified by fingerprint-only possession alone. `family/d10b_sp2_q9_manifest_unbound.out:637–673`, especially **661–669**, is this same changed-tuple replay. The two capstone C-Q5 traces are identical in their substantive attack. They do not constitute two independent mechanisms.

**Slice loss:** identical relevant retained/deleted components to C-C3 above. No needed component is lost. Again, the absent C-Q9 judge is immaterial: its failed relation is visible directly in the accepted proof. This verdict does not substitute for C-C8's registered isolation requirements.

### D2 — C-C4 C-Q4 Rescoped

File: `out/cap_cc04_d__depth1.cone__cq4r.out`.

- Lines **1347–1357** leak the authority key and release an honest skB2 attestation whose frame names skB2 and hashes M2.
- Line **1359** re-signs those unchanged inner bytes under attacker key `a_7`, gives that key a new evidenced inner manifest and possession proof, and encloses the pair in an attacker-signed wrapper under `a_4`.
- Lines **1369–1385** accept the valid outer wrapper at L0, descend with `wctx` to L1, and accept the honest inner bytes under `pk(a_7)` despite their old fingerprint/hash.
- Lines **1393–1403** compare the L1 attribution with the honest-inner report and fire `Rescoped`. The issuer ID stays `issuerId2`; the **key**, not the ID, is changed. No DSKS is used.

**Registered mechanism.** PREDICTIONS **1773** removes both inner key and hash binding while retaining possession and signature-byte verification. `family/s4_innerfp_mh.out:826–864` re-signs honest inner bytes under `a_6` and accepts them under that key inside a wrapper. That family obtains its wrapper from honest skW2; the slice builds its own under an attacker key. The inner attack is the same. Source: `../../cap_cc04_d.pv:614–618`.

**Slice loss:** removes honest Wrapper producers and L1→L2 processing, but keeps the honest inner producer and L0→L1 WrapStage. It removes a producer used in the literal family transcript, not a requirement of the registered attack: case (d)'s leaked authority key permits the replacement outer key. No depth-2 behavior is needed.

### D2 — C-C4 link 6b

File: `out/cap_cc04_d__depth1.cone__link6b.out`.

- Lines **1319–1321** leak the authority key and construct the entire bundle: outer key `a_2`, inner key `a_11`, and an inner frame whose fingerprint field is arbitrary name `a_8`.
- Lines **1331–1341** accept the correctly bound outer wrapper and forward its inner pair to L1.
- Lines **1347–1355** accept the inner frame under `pk(a_11)` and report `(pk(a_11), a_7)`. The frame has the same ID `a_7`, but `a_8` is not `fp(pk(a_11))`.
- Lines **1357–1363** send precisely that accepted frame/report to Link6bJudge and fire `ChainBroken(L1, LINK_6B)`.

**Different but valid attack within case (d).** PREDICTIONS **1773** registers this structural link red, but its `family/s4_innerfp_mh.out:826–864` witness reattributes existing honest inner bytes. This trace uses no honest signing at all. It directly witnesses the registered *inner fingerprint mismatch*, not outer attribution leaking inward, missing reports, or a failed cross-path join. Link6bJudge checks the L1 envelope report against the frame at `../../cap_cc04_d.pv:973–979`; the arbitrary hash is also unbound but is not what link 6b tests.

**Slice loss:** removes the family transcript's honest wrapper signer and ScopeJudge; keeps Attester (unused here), the actual L0→L1 path and Link6bJudge. Nothing needed for this structural witness is lost. The separate Rescoped trace above supplies the honest-byte mechanism evidence.

### D6 — C-C7(i) C-Q8

File: `out/cap_cc07i_d__depth0.cone__cq8.out`.

- Lines **770–772** forge authority evidence for attacker key `a_2`, supply correct manifest possession, and sign a different frame under `a_2`.
- The signed frame's fingerprint is correctly `fp(pk(a_2))`, but its other fields differ from the presented `OT_ATTEST` frame (**772–782**).
- Lines **782–792** accept the presented frame and pass the actual `(key, signature, presented bytes)` triple to BytesJudge.
- Lines **794–798** reconstruct `SigBytesUnbound`: successful same-key verification does not bind the presented bytes.

**Registered mechanism.** PREDICTIONS **1776**, configuration (i), demands verification of some frame naming the accepting key and waives byte equality. The cited structural family trace `family/d6e_sp1_q8all_samekey_unbound.out:631–643` is likewise entirely attacker-made. Its event is called `SigBytesUnboundAll`; the capstone's `SigBytesUnbound` is the **unfiltered structural** judge, not the similarly named family honest-filtered judge (`../../cap_cc07i_d.pv:949–955`). No honest signature or DSKS is needed.

**Slice loss:** removes honest wrapper/other producers and unrelated observers, but none is needed for this attacker-key structural attack. The retained Attester is unused. This trace alone says nothing about honest-key authorship.

### D6 — C-C7(i) link 4

File: `out/cap_cc07i_d__depth0.cone__link4.out`.

- Line **772** presents the same-key, different-byte construction just described, with correct possession over the presented manifest.
- Lines **782–790** accept the `OT_ATTEST` frame even though the supplied signature covers a different frame naming the same key.
- Lines **792–796** deliver the accepted triple to BytesJudge, which emits both `SigBytesUnbound` and `ChainBroken(L0, LINK_4)`.
- Lines **799–800** confirm a reconstructed attack on link 4, not just a derivation.

**Registered mechanism.** PREDICTIONS **1776** registers link 4 beside structural C-Q8; `family/d6e_sp1_q8all_samekey_unbound.out:633–643` descends the byte relation, though it declares no `ChainBroken`. This trace supplies the actual capstone consuming-link event. The two reds are the same failure observed by the same judge, not independent attacks.

**Slice loss:** as for C-Q8 above; no needed producer or check is removed by slicing.

### D6 — C-C7(i) honest-key authorship

File: `out/cap_cc07i_d__depth0__auhk.out`.

- Lines **2092–2100** obtain a genuine wrapper signature and possession proof from honest **skW**, over its own MW manifest.
- Line **2108** pairs that wrapper signature with attacker-built `OT_ATTEST` bytes naming the same skW and MW; authority evidence is forged using the leak at **2090**.
- Lines **2118–2124** accept the new attestation under skW: the signed wrapper frame names skW, satisfying the weakened check, but is not the presented attestation.
- Lines **2128–2136** recognize skW as honest and fire `AcceptedUnderHonestKey`; no `IssuerSigned(skW, presented_attestation)` preceded it. The observed signing at **2098** was of wrapper bytes.

**Registered mechanism, with a different honest signature source.** PREDICTIONS **1776** registers this correspondence red for (i). `family/d6e_sp1_q8all_samekey_unbound.out:793–809` and `family/cap7d_sp1_q8_samekey_unbound_wrapper_signer.out:831–847` reuse an honest attestation signature with changed presented bytes. Here the signature is from the separate honest wrapper key skW, not the issuer's same-key wrapper skI. Configuration (i) permits either signed type; the same-key fingerprint test passes and exact bytes remain unbound (`../../cap_cc07i_d.pv:619–620`). This is not evidence for a stolen key or for configuration (ii)'s conditional branch.

**Slice loss:** depth0 deletes only the four WrapStage/SUnwrap calls. **Wrapper signing remains present**, as do every honest signer and `IssuerSigned` event site. No missing producer manufactures the correspondence failure. A wrapper *signature* is used as material at L0; no wrapper *verification/descent* is needed. The green depth0.cone authorship run removed the useful Wrapper producer and cannot refute this red.

### D6 — C-C7(ii) C-Q8

File: `out/cap_cc07ii_d__depth0.cone__cq8.out`.

- Lines **912–914** use the leaked authority key to evidence attacker key `a_3`, supply correct manifest possession, and sign a frame of fresh type `a_7`.
- The presented frame is `OT_ATTEST`; the signature instead covers the different frame with type `a_7`, which is not `OT_ATTEST` (**914–924**).
- Lines **924–934** accept and report that mismatched triple: the signed type takes the waiver branch, despite the presented type being attestation.
- Lines **936–940** reconstruct `SigBytesUnbound`. All signing material here is attacker-made; no honest-wrapper signature or DSKS step is used.

**Registered mechanism.** PREDICTIONS **1776** cites `family/d6d_sp1_q8_type_conditional_unbound.out:495–507`; it has the same attacker-key/non-attestation construction. The composed family output `family/cap7b_sp1_q8_wrapper_signer_type_conditional.out:892–904` also uses it for its structural C-Q8. The guard is `sbA = fbA || sigFrameOt(sbA) <> OT_ATTEST` (`../../cap_cc07ii_d.pv:633–634`), applied to the **signed** frame.

**Slice loss:** removes honest Wrapper producers, including the source needed for the *additional* honest-filtered/authorship attack in `cap7b:1056–1072`. It removes nothing this structural family attack needs. Do not promote this result into evidence for those additional registered reds or the honest-filtered C-Q8 result.

### D6 — C-C7(ii) link 4

File: `out/cap_cc07ii_d__depth0.cone__link4.out`.

- Line **914** supplies the same attacker-key signature over a non-attestation frame beside different presented attestation bytes.
- Lines **924–932** show acceptance under the type-conditional waiver with manifest possession intact.
- Lines **934–938** send the exact accepted triple to BytesJudge and emit both byte-unbinding and `ChainBroken(L0, LINK_4)`.
- Lines **941–942** confirm the reconstructed link-4 counterexample.

**Registered mechanism.** Same registration and structural family comparisons as C-Q8 above: `d6d:495–507` and `cap7b:892–904`. It witnesses the consuming byte-binding link, not merely failed authorship for an adversary-enrolled key.

**Slice loss:** identical to C-Q8 above; no dependency of this attack is removed, but the separate honest-wrapper mechanism is unavailable in this cone.

### D7 membership — C-C17 link 2a

File: `out/cap_cc17_d__depth0.cone__link2a.out`.

- Lines **740–742** disclose the authority key and forge a two-slot manifest: slot A names `fp(pk(a_2))`, while slot B names arbitrary fingerprint term `a_3`.
- Line **742** nevertheless supplies slot B under `pk(a_7)`, with that key's valid frame signature and possession over the exact manifest; both frames retain correct key pins, hashes and common content.
- Lines **752–760** accept both slots and report completeness, even though slot B's named fingerprint `a_3` differs from its actual accepting key's fingerprint.
- Lines **768–774** pass that named-slot/actual-key mismatch to Link2aJudge and reconstruct `ChainBroken(L0, LINK_2A)`.

**Registered mechanism.** PREDICTIONS **2666** registers removal of slot B's membership equality, not removal of a required-slot read. Its cited structural family trace `family/cap13b_sp2_membership_unbound.out:1954–1972` is already the same entirely attacker-made construction (`SlotKeyWrong`). Both required slots are reported satisfied; this is membership failure, not C-C9's completeness failure. Source: `../../cap_cc17_d.pv:643–657`.

**Slice loss:** removes all honest signing producers and member reports. The cited structural family attack needs none of them; Front, AttestStage and Link2aJudge suffice. This trace by itself does not impersonate an honest member; the next one does.

### D7 membership — C-C17 SignerForged

File: `out/cap_cc17_d__depth0__sf.out`.

- Lines **2141–2153** release genuine slot-A material under skI for M2 through ShipIssuer, including its frame signature and possession proof.
- Line **2179** retains M2, uses that genuine material for slot A, and fills the slot naming skB2 with attacker key `a_7`, signing its own correctly pinned frame and possession over M2.
- Lines **2189–2197** accept both slots and complete M2; slot B's report explicitly pairs `fp(pk(skB2))` with actual key `pk(a_7)`.
- Lines **2205–2213** pair that report with skB2's genuine M2 membership and fire `SignerForged`. No DSKS, changed set, missing slot, or forged signature under skB2 is involved.

**Registered mechanism.** PREDICTIONS **2666** and `family/cap13b_sp2_membership_unbound.out:710–730` show the same M2 membership substitution: honest slot-A material, attacker-held key in the skB2 slot, all other checks retained. ShipIssuer replaces the family's simpler slot-A signing process without changing the attacked membership relation.

**Slice loss:** depth0 deletes only wrapper descent, retaining ShipIssuer and the member reports this trace needs. The depth0.cone `SignerForged` green is not contrary evidence: that cone deleted ShipIssuer/RefuseIssuer and could not supply this M2 slot-A material. Nothing required is missing from the reviewed depth0 red.

### D1 — C-C2 link 5

File: `out/cap_cc02_d__depth0.cone__link5.out` (the cone representative; other link-5 slice depths are not separately classified here).

- Lines **755–757** leak the authority key and construct a wholly attacker-made two-signer bundle under keys `a_6` and `a_9`, with correct manifest possession and byte signatures.
- The first frame carries arbitrary fingerprint `a_2` and hash `a_3`, although its actual accepting key is `pk(a_6)` and the manifest names that key (**757–767**).
- Lines **767–775** accept both frames and complete the manifest; both the first frame's fingerprint and hash mismatch their required values.
- Lines **783–789** report the first frame to Link5Judge and reconstruct `ChainBroken(L0, LINK_5)`. No honest signer runs anywhere in this trace.

**Different but valid attack within case (d).** PREDICTIONS **1771** registers the multi-signer pin/hash removal and link 5's frame-to-key half. Its cited `family/m4_framepin_mh.out:604–620` instead re-signs existing honest skB2 bytes under an attacker key and fires `Reattributed`. This cone witness is structural malformation accepted through those same omissions. It is not evidence of honest-frame reattribution.

**The conjunct question is resolved for this trace.** Link5Judge combines fingerprint and hash at `../../cap_cc02_d.pv:948–951`; the boolean red alone is ambiguous, but the reconstructed terms are not: `a_2 ≠ fp(pk(a_6))` **and** `a_3 ≠ h(accepted_manifest)`. Thus it really breaks the registered fingerprint half, not just the hash half. It does **not** establish that removing the pin alone suffices for the family attack. The previous C-Q3-A review supplies the separate honest-byte evidence.

**Slice loss:** deletes every honest producer, including the Attester needed for the literal family reattribution trace, and retains only Front, AttestStage and Link5Judge. That is why this output must not be described as a replay of the family attack. It does not create the structural mismatch or delete a check; no removed component is needed for this valid structural counterexample.

### Verification and limits

`codex2/audit.py` checked all twelve current source/slice pairs: exact regeneration, unchanged pre-composition text except query deletion, and unchanged replicated final components retained in source order. Results, input hashes, HEAD and binary/library hashes are in `codex2/audit.txt:1–19`. This is a narrow freshness check alongside the previous deletion-soundness review, not a new claim that the regex slicer is generally safe.

I independently reran C-C2 link 5, C-C7(i) honest-key authorship, and C-C3 C-Q5 to resolve the conjunct, producer-deletion and D10-consumer questions. Each used `timeout 1800 /home/tony/.local/bin/proverif -lib ../../../../lib/tessera_theory.pvl FILE`, matching run.sh's library path. All exited 0 with reconstructed `is false`, in 7.20, 3.60 and 1.48 seconds respectively. Commands and results are in `codex2/reruns.jsonl:1–3`; full outputs are beside this review. Every rerun is byte-identical to its saved output after removing the saved one-line exploratory banner (`codex2/audit.txt:13–16`). The raw `identical_to_saved=false` log fields reflect that banner, not a trace difference.

For the reviewed red executions, restoring deleted components and leaving them unscheduled preserves the same finite event prefix. No “absence of a producer” argument is needed for any reachability red; the authorship red retains all honest signing producers anyway. **None of these twelve traces uses DSKS.** The structural results do not automatically supply the separately registered honest-filtered queries, all retained greens, isolation controls, or Band 0 discharge. Writes were confined to `codex2/`; no VM access, staging or commits.
