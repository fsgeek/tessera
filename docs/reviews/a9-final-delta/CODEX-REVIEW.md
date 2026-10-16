# Codex review — A9 final owner delta

2026-10-13. **Artifact: PROPOSED, unsigned A9; author read/sign next.** Reviewed A9 in full, the preserved pre-revision text and `delta.diff`, both custody/profile CODEX reviews and dispositions, V1–V2 compatibility analysis, ENCODING-V1's governing signature, DNS/window and git sections, and the earlier registered sentences identified below. Current profile wording was checked for reconciliation. Only this review file was edited.

**Verdict: resolve the six findings below before signing.** The custody enforcement and deadline repairs faithfully implement their source findings. The new root rule correctly makes candidate failures informational and acceptance existential. The reliance-period extension is a defensible acceptance policy, but its security tradeoff is not yet stated honestly. Verdict stability is substantially improved but remains underspecified at and after an algorithm cutoff and lacks its required A9.7 row. No implementation conformance, deployed custody, rotation model result or P8 discharge is established by this review.

Severity: **HIGH** = misleading security boundary; **MEDIUM** = normative ambiguity, missing amendment registration or freeze/evidence inconsistency; **LOW** = editorial clarification. Locations below refer to the inspected A9, not the historical line numbers used by its source reviews.

## F1 — HIGH: reliance limits acceptance in chain time, not the signing date or a finite UTC forgery exposure

**Location:** A9:296–303; A9.4:258–263; opening adversary/boundaries; source profile F2 and disposition.

Extending reliance beyond signing retirement admits authentic cached root signatures, as intended. It also admits a *newly forged* root DNSKEY signature made with a stolen retired KSK during that extension, provided its presented RRSIG validity covers the snapshot's anchored time and the rest of the required evidence succeeds. Signed inception/expiration values cannot prove the private key signed before retirement: a thief chooses those values. “Evidence it signed while signing stays usable for that long and no longer” implies that provenance was checked when the predicate checks only the anchored time, signature and configured eligibility. This is an authority-channel limitation, not a demonstrated full V1 receipt forgery; both authority channels and the attestation signatures remain required.

The extension bounds eligible **snapshot chain time** by signing-end plus the configured maximum lifetime. A9 already discloses that A2.1 gives no finite backward-skew bound for T; the same issue must not disappear for the snapshot anchor. Thus there is no established finite UTC exposure bound. Historical KSK safety remains assumed, not evaluated. Moreover, a maximum observed in archived captures is a policy value, not proof of the maximum over all signatures the root ever issued. The source disposition is candid about using observed windows; A9's universal “maximum ... it made” is stronger.

**Exact proposed fix:** replace the reliance-period definition/explanation at :297–300 with:

> Each KSK entry records signing-start, signing-end and a sourced reliance lifetime L, with the reliance interval [signing-start, signing-end + L]. L is the registered acceptance-policy value derived from the cited root DNSKEY RRSIG validity evidence; a largest observed lifetime is labelled observed, not asserted to be a proven global maximum. A candidate must also satisfy cryptographic validation and the selected RRSIG's inception/expiration checks at the snapshot's own verified anchored time. This extension permits authentic pre-retirement evidence anchored later; it does not establish that signing occurred before retirement. A thief of a retired KSK can manufacture eligible root evidence during the extension. Exposure is bounded by the reliance endpoint in snapshot chain time, not by a finite UTC duration under A2.1. Historical authority-key safety and the continuing anchor/history assumptions remain necessary and are not evaluated by V1.

Retain the following existential/order-independent sentences. Record concrete sourced L and interval endpoint conventions in the pre-freeze trust configuration. If the intent instead is to prove pre-retirement signing, that requires a pre-retirement commitment to the exact signature; the current predicate does not do so.

## F2 — MEDIUM: algorithm cutoff rule has an undefined branch and changes A3 without an A9.7 row

**Location:** A9:265–277 and A9.7; A3:503–508; source compatibility §2.4.

The delta contains the requested phrases “per-algorithm cutoff compared with T” and “reported separately”. It preserves the same-input contract and the C7 missing-capture companion. But it says only that T *before* a cutoff preserves the V1 verdict. At equality or after it, it is unclear whether the V1 verdict changes, despite the next sentence saying historical-security results never replace that verdict. Authentication of the cutoff is stated in the historical-security paragraph but omitted from the new policy rule. Key-theft cutoffs must remain separate too. A cutoff is not a demonstration that security held earlier, especially with A2.1 uncertainty.

This restriction also narrows A3 §A3.6.2's registered `INVALID` case, “an identifier prohibited by applicable policy”. A9's table has no replacement for that sentence. Row 25 concerns hybrid deployment; row 28 concerns waivers. Neither registers this change. A9 explicitly says the P4 partition is unchanged, so the scope of this narrowing must be explained.

**Exact proposed fix:** replace :271–274 with:

> Later algorithm policy enters the separate historical-security assessment only as an authenticated per-algorithm cutoff compared with T, with A2.1's chain-time uncertainty; authenticated per-key theft cutoffs are assessed separately there as well. It never overwrites the V1 verdict or its six stable fields, whether T is before, equal to or after a cutoff. A receipt whose T precedes an algorithm's cutoff keeps its V1 verdict; that comparison alone does not establish historical safety. Later revocation, standing, renewal and historical-security results are reported separately, together with later adverse evidence. The V1 verdict continues to apply the algorithm policy registered for its governing V1 specification, including its original malformed, unsupported and prohibited-identifier cases.

Keep the existing same-input contract, non-repudiation disclaimer and C7 evidence clause verbatim. Add A9.7 row 29:

| 29 | “an identifier prohibited by applicable policy” | `phase-0-prereg-amendment-3.md:503-508` | A9.4: V1's registered algorithm policy determines its verdict; later algorithm prohibition/cutoff results belong to a separate assessment and cannot overwrite that verdict | R |

Update the table count and “Named and not changed” P4 sentence to: `the P4 check-result partition (later algorithm-policy effects are narrowed by row 29)`. This preserves a historical V1 verification result while allowing a relying party to reject a transaction on the separate adverse assessment. It does not promise continuing cryptographic truth after a break.

## F3 — MEDIUM: provider-neutral custody conflicts with the retained registered “local GPG” placement

**Location:** A9:341–360; A9.7 row 15 and “Named and not changed”; original prereg:292–294. Source custody F3/disposition.

The policy signer, credential boundary, dedicated use, hybrid deadline and limited independence text faithfully implement custody F1/F2/F4. C3 still honestly allows queue-based misuse of both slots by an AWS takeover; external policy prevents bypassing the clock check, not adversarial current-time issuance. No new independent approval or control is claimed.

However, row 15 explicitly says “The ‘local GPG’ placement is kept”, and the later inventory calls that placement unchanged. A9.6 now permits an HSM and policy signer at another cloud provider. That replaces the earlier registered placement, even though the fingerprint scheme and rule O stay unchanged. A first-time reader encounters two incompatible deployment requirements.

**Exact proposed fix:** replace the row-15 sentence `The "local GPG" placement is kept.` with:

> The registered local-GPG placement is replaced for V1 by A9.6's slot-2 custody alternatives, both through the external policy signer; rule O and the gpg fingerprint scheme are retained.

Delete `the "local GPG" placement (phase-0-prereg.md:292-294)` from “Named and not changed”. Row 15 already cites that source range, so no extra row is necessary.

**Unfinished source reconciliation:** ENCODING-V1:441 still says `rule O (P-256, hardware token; owner decision 2026-10-12 replaced SLH-DSA)`, despite custody disposition saying this repair was delegated. The exact source-review replacement remains appropriate: `rule O (OpenPGP P-256; slot-2 custody per A9.6; owner decision 2026-10-12 replaced SLH-DSA)`. A9 binds this file at signing, so delegation is not evidence that the reconciliation is done. This is a prose custody correction, not a signature-byte or vector change.

## F4 — MEDIUM: repository-key period borrows an ambiguous KSK rule; append-only updates do not by themselves preserve every verdict

**Location:** A9:304–308 and :269–271; compatibility §2.1/§2.5.

The repository key has a *signing period*, while the “same existential rule as the KSKs” now tests a *reliance period*. A repository signature has no DNSKEY RRSIG lifetime from which to derive L. The governing evaluation time is also unstated here. The source recommendation specifies the commit's anchored time, not receipt T or snapshot time.

Keeping all keys/pins preserves old evidence availability. It does not guarantee full verdict identity under every enlarged configuration: adding a previously absent pin/key can turn UNVERIFIABLE into VALID_STRICT. Closing a previously open-ended period can also exclude inputs that were eligible before. The existing identical-input contract is sound; distinguish it from the weaker compatibility guarantee for compatible extensions. “A closed period never changes” alone leaves this update case undefined.

**Exact proposed fix:** replace :304–307 through “forever” with:

> Trust configuration entries are append-only: KSKs, header pins and repository keys are never removed, and finalized period endpoints never change. Repository trust entries name D, the key and an inclusive signing interval; the git assertion passes this trust check if some configured entry for D verifies gpgsig and its interval contains the signed commit's own verified anchored time. Repository entries have no KSK-style reliance extension. Unknown material cannot establish this required check. Append-only extensions preserve previously usable trust witnesses; newly covered evidence can improve an earlier UNVERIFIABLE result. Exact stable-field identity remains the contract for identical declared inputs. Closing an open period must not retrospectively exclude evidence previously accepted under that entry; the pre-freeze configuration records the endpoint/update convention explicitly.

Retain the rollover control after this replacement. If retrospective closure is deliberately wanted, it belongs in the separate adverse assessment and needs a visible exception to the stability promise; it is not an append-only edit in the semantic sense.

## F5 — MEDIUM: sequential replacement is structurally compatible, but the registration and evidence obligation need a precise boundary

**Location:** A9:375–385; ENCODING-V1 §7/§7.1; compatibility §2.3.

The error-code statements are correct: §7 requires one TXT RR (`DNS_RRSET`) and reconstructs exactly `_tessera-v1.<common.issuer>` (`DNS_OWNER`); §7 rejection order checks OWNER before RRSET. This assumes the alleged per-key names actually differ from that required name. Extra records elsewhere do not themselves violate this RRset check.

Sequential replacement fits the frozen **prose** verifier rules: each receipt supplies its own historical snapshot/commit, the same owner/path can contain a different pair of fingerprints, and each individual window satisfies the ≤90-day and C4 checks. There is no current-record lookup or successor relation to check. This is structural compatibility, not a tested frozen service verifier or P10/capstone result. The verifier also does not check cross-receipt non-overlap. At the shared endpoint, both inclusive windows can contain that instant; `next.not-before >= old.not-after` in the source is not literal non-overlap under ENC's inclusive rules.

A9 presently says both “no successor key under this amendment” and that sequential replacement is registered after unnamed vectors/model check. It does not name the registration record, model/property, or whether this is a 30 Oct obligation. That lets a reader confuse a permitted future mechanism with an already registered operating plan.

**Exact proposed fix:** replace :376–380 after the `DNS_WINDOW_LENGTH` parenthesis with:

> This amendment registers the first issuance window only; it does not yet authorize successor issuance. A future sequential-replacement registration may retain the frozen V1 byte/check profile: the same DNS owner and git path, new keys, and a new window with next.not-before > previous.not-after (both endpoints are inclusive). Each receipt carries its own historical snapshot and commit. Multiple TXT records at the required owner fail DNS_RRSET; a substituted per-key owner name fails DNS_OWNER. The V1 verifier checks each receipt's window, not non-overlap between receipts. Before successor issuance, the owner records a dated rotation registration naming the two-window positive/negative vectors and the model, checked property and result establishing the intended issuance invariant. This future rotation evidence is not added to the 30 Oct first-window gate. Without that registration, issuance stops at the first window's end.

If the intended decision is to register rotation *now*, replace the “first window only” policy explicitly and assign the named vectors/model obligation to 30 Oct instead. Neither policy is established by the current compatibility inference alone.

## F6 — MEDIUM: git-format policy has no evidence schema or verdict contract, and the revised trust policy still conflicts with the profile

**Location:** A9:291–295; ENCODING-V1 §7.2 and out-of-scope list; V1-PROFILE §2.1/§5; compatibility §2.9; profile disposition F2.

Accepting SHA-1 only is faithful to the source recommendation. It does not change receipt frames, A_sig, signature serialization, the canonical TXT/git blob, or an existing SHA-1 commit/stamp. No existing P8 vector needs to change just to declare that policy. A later spec-file edit naturally changes the spec hash bound into *new* receipts; that is not a change to the frame grammar or old signed bytes.

But “git evidence names its object format” does not define a member name/type, missing-field behavior, unsupported-format verdict, or exact stamp bytes. ENCODING-V1 does **not** define the git evidence container. §7.2 fixes the signed-commit target and describes lowercase id plus LF as a repository convention. The field belongs in the bundle's git-evidence schema when V1-PROFILE §2.1/G-26's container/member encoding is settled, with the normative check in its git-channel section. Putting it into the closed signed common schema or the 255-byte key-publication grammar would change P8, unnecessarily.

**Exact proposed fix:** append to A9's git-format paragraph:

> The pre-freeze bundle schema (V1-PROFILE §2.1, G-26) defines the git-evidence member object_format as the string "sha1". It is an evidence descriptor, not a new signed-frame or key-publication field. A missing descriptor gives UNVERIFIABLE / GIT_OBJECT_FORMAT_MISSING; an unsupported value gives UNVERIFIABLE / GIT_OBJECT_FORMAT. The verifier recomputes the SHA-1 object ids from the raw commit/tree/blob bytes, so this descriptor cannot override their interpretation. For V1 the stamped message is exactly 40 lowercase ASCII hex digits naming the signed commit id followed by one LF byte. The schema/check specification and conformance cases are fixed before the 30 Oct profile freeze; no P8 frame or key-publication vector changes are required.

Also reconcile V1-PROFILE §5 before the freeze: it still requires a signing-period root predicate (:197–198), the withdrawn `2026-10-11T23:59:59Z` cutoff (:203–208), and the corresponding outside-signing-period reason (:209–211). **Exact replacement instruction:** replace the root predicate and period-policy paragraphs with A9.5's reliance predicate and the sourced interval definitions after F1; replace `KSK_OUTSIDE_SIGNING_PERIOD` with `KSK_OUTSIDE_RELIANCE_PERIOD` and require a verified signature before that reason, as source F3 requires. Mark this as a dated correction, preserving the old policy in the review record. Without this reconciliation a first-time reader following A9's sources finds two normative root policies. This review does not claim the delegated repair or instrument repairs were completed.

## Source fidelity and requested-check disposition

| Revision/check | Result |
|---|---|
| Custody F1 policy signer, F2 deployed-slot deadline, F4 limited independence | Faithfully incorporated; no change to C1–C7's substance, rule O or C3's single-controller adversary. F3 registration/encoding reconciliation remains F3 above. |
| Profile F1 existential/order-independent root result | Faithfully incorporated in prose; bad-first/good-second controls in both orders still need recorded evidence, not an inference from this edit. |
| Profile F2 reliance instead of retirement cutoff | Implements the disposed policy, but not its forgery/observed-maximum tradeoff; F1. Honest old-root/new-leaf after-retirement fixture remains required by the disposition. |
| Profile F3–F7 implementation findings | Not represented as solved by A9. Their accepted code/test repairs must retain their own evidence. No blanket claim that this prose delta implements the entire profile review. |
| Compatibility stability / append-only / repo periods | Direction is faithful; boundary and period precision remain F2/F4. Existing same-input contract and C7 companion remain present. C7 companion is assigned to 20 Nov, not 30 Oct. |
| Rotation | DNS_RRSET/DNS_OWNER verified against ENC; sequential compatibility is structural only, with inclusive-endpoint and registration caveats in F5. |
| Git object format | No signed-layout or P8-vector change needed; missing evidence-schema location and exact policy in F6. Host/default forecasts are attributed author statements, not independently verified facts needed for the check. |
| A9.7 coverage | New earlier-amendment algorithm-policy row required; existing row 15 must explicitly replace local placement. Revisions to unsigned A9's own earlier draft do not themselves require earlier-amendment rows. |
| 30 Oct | Custody choice and unchanged hybrid deadline fit the gate. New root/repository trust and git-format semantics must be resolved in its frozen profile/configuration; existing required rollover evidence must include the accepted controls. Future rotation is not silently added to this gate. |

No web or model/test execution was needed to establish these textual findings. External forecasts and IANA claims were treated as attributed source material, not freshly verified operational facts. No adversary counterexample here is promoted to a checked formal result. A9 remains unsigned; the author's signature and all exit/deployment evidence remain outstanding.
