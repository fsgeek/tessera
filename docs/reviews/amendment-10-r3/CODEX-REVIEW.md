# Non-author review: Amendment 10 custody timing and custody draft, second pass

2026-10-17. **Result: the timing move is sound in principle; revise the documents before treating the custody procedure as ready.** Release independence must exist before the first production release is authorized and offered to relying parties. It need not already exist when the specification is frozen. This is a real change to the recorded freeze prerequisites, however, and authenticated bootstrap remains essential.

One HIGH remains from C01/C05: the procedure does not explicitly bind the independently built verifier to the contents of the archive it approves and signs. There is no additional, distinct new HIGH in this pass. The TEST-key rule provides a useful production authentication boundary, but its absolute statements about what users can receive or mistake for real exceed that boundary.

## Scope and evidence

Reviewed the current working-tree A10, especially the plain custody summary, A10.4.1–A10.4.2 and rows 32–36; the complete custody draft; the original C01–C09 review and its disposition; A9.2/A9.5/A9.6; V1-PROFILE §3.5, §5, §14.2 and §15.8; operations runbook §6; V1-SCHEDULE; and STE-STYLE. Checked the preceding A10 review/disposition for the earlier gate and the decision memo's corresponding provisions. A9.5's release-authority wording was also checked at signing commit `2ad3489`.

Repository HEAD: `7d7f94d797048f96df9a2b129962a5604439f4ae`. The reviewed A10 and custody draft are untracked proposed documents, not a committed revision pair. There is no tracked A10 diff from which to establish the concurrent edit; this review addresses the current bytes against the preceding review record.

| Artifact | Reviewed SHA-256 |
|---|---|
| `docs/phase-0-prereg-amendment-10.md` | `d3f47fd8c418b138b75360ea381113cedb5f34692a79316edf8ebde15933ed0e` |
| `docs/V1-RELEASE-KEY-CUSTODY-DRAFT.md` | `2384e4ef298302b02d8ed2f12dfe4b0a3fee0c5762b8219936c98ca654c56895` |
| `docs/reviews/custody/CODEX-REVIEW.md` | `6429a78c7d94ee8508315f4f3532e2cf98b0792d7666c7e4646e80e2625def76` |
| `docs/reviews/custody/DISPOSITION.md` | `7d22b396ef343ef4761f9f73802ec664abd3d149931d8ced313292abe79271a7` |

Locations below refer to these working-tree documents. “A10” means the amendment; “draft” means the custody draft. APPLIED means that the requested procedural correction is present. It does not mean that author choices are settled, hardware is configured, or independence has been demonstrated. WITH DEFECT means a correction is present but has the specific remaining defect described here. No finding is wholly NOT APPLIED.

## 1. Answers about the amendment

### Moving the gate

**Sound as a proposed gate change, subject to the retained prerequisites.** A9.5 :326–332 requires authenticated releases and an access boundary that the operational credentials cannot use. It does not date implementation of that boundary to 30 October. The protection is consumed when someone authenticates a production verifier and relies on its trust configuration. A10.4.1 :461–478 likewise scopes its added protection to authentic, trustworthy releases; it does not assert that such a release already exists at freeze.

A9.2 :205–210's formal/encoding exit items do not require the production release key or signing environment. They must still pass on their registered terms. Instrument TEST provisioning can support specification and conformance work; it cannot demonstrate the real release authority's implemented independence. Moving custody implementation does not move the formal exit, authorize early service code, or turn instrument results into production evidence.

There **are existing documentary freeze prerequisites** affected by the move: profile §14.2 item 1 requires the named key and demonstrated boundary before 30 October; §5 puts its fingerprint in the freeze record; runbook §6 :115, :134–145 places custody, bootstrap tracking and a required refusal test at freeze. These are not a cryptographic reason to reject the move. They require an explicit, author-ratified change of timing. A10 :525–528 acknowledges the profile fingerprint/deadline change rather than pretending it was already permitted.

At freeze, retain the release artifact/signature/preimage and trust-hash binding, verification format and dependency pinning required by profile §14.2 item 2. Also resolve the bootstrap/normal-rotation/bounded-recovery **rules** that item 2 already requires. Later ceremony and rehearsal supply their actual key, equipment and observed results. The adopted text and subsequent profile/runbook update should distinguish these registered rules from their later execution, and distinguish a pre-freeze TEST refusal vector from the later deployed-boundary rehearsal. A general postponement of item 1 must not silently postpone item 2's overlapping requirements.

The independently retained freeze baseline also remains necessary. In particular, A10 :457–459 and row 32 still require the single service-key tuple to be authorized at freeze. That authorization can be preserved without an existing production release key, then checked and bound into the first release. The new gate does not authorize selecting a different tuple later from possibly captured channel assertions. The freeze's trust values, catalog and specification-source hashes remain the baseline, not inputs that the November NUC may redefine. The first verifier-code baseline is established independently when that code exists; the move does not require service code before its registered exit gate.

A10 :511–512 correctly requires the environment, rehearsal, reviewed procedure and established independence before the first public release; 20 November is a target for this work. The gate must pass **before the first production signature authorizes a release for relying-party use**, not merely after signing and immediately before upload. A rehearsal uses throwaway keys. Nothing here establishes that the November schedule will be met.

### TEST releases and row 36

**The key exclusion works for production authentication, under authenticated bootstrap.** A signature made only with the TEST key cannot authenticate as a production release when the authentication step requires the independently authenticated production key and never accepts the TEST root. The explicit prohibitions on promoting the TEST key through the freeze record, user documentation or a production key transition are useful. They address accidental promotion, not just different key names.

But A10 :515–516, plain :131–139 and row 36 go further: “no pre-gate release can reach a relying party as a real release.” A person can receive a public TEST executable, skip authentication, or be given an attacker-substituted initial key. The rule does not prevent that. The first-public-release definition at :506–507 concerns production-signed releases offered to relying parties; it does not itself prohibit all public TEST artifacts. Thus :524's “nothing is public before the gate” is also not established by that definition. This is the same authenticated-acquisition boundary already acknowledged by C07 and the targeted-distribution residual, not a demand for a new public log. See R3-02.

Profile §3.5 :316–325 explicitly binds no production release and lets the instrument harness supply a TEST key through the environment. It is consistent with keeping TEST authority separate; it supplies no evidence that the eventual production authentication path excludes TEST provisioning. That exclusion needs a production-path negative check before release.

### Fingerprint at first bootstrap publication

**Compatible with A9.5 and technically sound, but a change to the current profile.** Profile §5 :399–400 and runbook :134–136 currently require the fingerprint in the freeze record. Recording it later is not literal compliance with those sentences. A10 :525–528 openly proposes replacing that timing after the author's ruling. A9.5 requires the actual key and access boundary in a dated custody record; it does not require the key to predate specification freeze.

There is no need to mutate frozen specification bytes or recompute their identity merely because the key is generated later. Profile §14.2 item 7 and §15.8 already place actual hashes in an external release/freeze record. Use a dated first-release bootstrap/custody record that names the production fingerprint, frozen baseline/catalog and exact approved release, with its reviewed procedure and rehearsal. Preserve the original freeze record; link the later record rather than retrospectively claiming that the fingerprint was present on 30 October. Authenticate first acquisition through the independent path required by C07. A fingerprint posted beside its own unauthenticated key is insufficient.

The draft's bootstrap step still demands checking the fingerprint in the freeze record (:236–237). That is an unreconciled instruction under the proposed timing, not evidence that the move is unsound. See R3-03.

### The author's words

**A10 uses the quotation within its accepted scope.** Plain :140 ties it to the author's time in November; :522–523 expressly limits acceptance to risk (4) and denies that it is a ruling on A10.4.2. The heading, opening status and :657–660 keep the gate recommendation pending. No author ruling is established by this quotation.

The separate custody disposition's C08 calls the moved gate an “author fact.” That attribution is stronger than the A10 record reviewed here. Correct that attribution when reconciling the stale draft note; neither the quotation nor this review supplies the author's pending ruling. See R3-04.

## 2. Remaining findings and exact corrections

### R3-01 — HIGH, retained C01/C05: the checked build is not explicitly the archive that gets signed

**Locations:** draft :251–278, :282–294; A10 :500–502.

The revision adds independent source/trust review, the independent authorization record, a pinned checker and a clean build. These substantially address the original authorization attack. However, the NUC first prepares a release archive (:253–255). Later, the author builds source and checks **the built verifier** (:275–276), then records **the archive** hash (:277) and signs that archive. No step requires replacing the NUC archive with an archive assembled from that build, or establishing byte correspondence between the built verifier and the executable actually in the archive.

The residual attack is concrete at the procedural level: the NUC supplies benign source S and archive M containing a modified verifier. The reviewer approves S, builds verifier V and checks V's correct trust/catalog binding, then approves SHA-256(M) and signs M. A hash match and a valid signature over M do not establish that M contains V. This is an omitted required check, not an observed exploit or a claim that the author would necessarily follow this interpretation.

**Exact correction:** after the build, require the independent environment to assemble the final archive from that reviewed build and the approved trust file. Check the contents and compiled trust/catalog binding of the verifier **as packaged in that final archive**. Reject extra or substituted executable content. Compute the approved archive hash only after that assembly/check, and transfer that exact archive for signing. If retaining a NUC-built archive instead, require an independent byte comparison establishing that its executable and other release contents are exactly the approved build/package before approval. Merely finding the expected hashes somewhere in an executable is not that comparison.

Use the same archive identity through approval, signing, verification and publication. Add a rehearsal case with benign reviewed source and a malicious executable in an otherwise plausible candidate archive; it must be rejected or discarded and rebuilt before signing. This closes the remaining part of the original C01 attack and C05's actual-distributed-verifier requirement. It does not require reproducible builds if the independent build itself supplies the shipped archive.

### R3-02 — MEDIUM: TEST-key exclusion is stated as an unconditional user/distribution guarantee

**Locations:** A10 :131–139, :513–516, :520–524 and row 36 (:626); draft :13–14 and §11.

Keep the separate TEST key and every prohibition on promoting it into production authority. Replace the absolute conclusion consistently in the technical rule, table and plain summary with a scoped statement, for example:

> A pre-gate TEST signature cannot authenticate a production release. Production authentication must use the independently authenticated production release key and must reject TEST authority, including TEST provisioning overrides. This does not protect a user who skips authentication or acquires a substituted initial key.

For plain text:

> Each early release uses a separate test release key. Production checks never accept this key. Users must authenticate the production release key before they rely on a release.

Replace the unqualified “nothing is public”/“no risk” mitigation with the actual restriction on offering pre-gate artifacts for production reliance. If the owner intends an additional ban on public TEST distribution, state that rule explicitly; it does not follow from the current definition.

Require a rehearsal in which an otherwise correct archive has only a TEST signature. The production acquisition/verification procedure must refuse it, including an attempt to supply the TEST key via the test interface. Missing or substituted bootstrap authority must not be accepted as production merely because a signature verifies. Test signatures remain useful test evidence. This correction does not change any receipt verdict rule.

### R3-03 — MEDIUM, C07: bootstrap still requires a fingerprint in a record that predates the key

**Locations:** draft :232–247; A10 :525–528; profile :399–400; runbook :134–136.

The independent recomputation, paper comparison, independent first-acquisition path and retained public artifacts are applied. The draft nevertheless tells the author to inspect the actual fingerprint in the freeze record. A10 now permits the production key not to exist then. Following both instructions would require an unmentioned later addition or leave the ceremony apparently failed.

**Exact correction:** make the draft's step 3 inspect the dated first-production-release bootstrap record, verifier documentation and relying-party text. Require that later record to identify the original freeze baseline and actual production key, and require comparison with the ceremony reference. Preserve the original freeze record. After the author rules, reconcile profile §5, §14.2 items 1–2 and runbook §6 with the same registration/execution split described above. Do not edit those other files as part of this review.

### R3-04 — LOW, C08: the draft's concurrent-edit note is stale

**Locations:** draft :9–10; custody disposition C08 (:12).

A10.4.2 now says the gate is before the first public verifier release. The draft's instruction saying A10 still says “before the freeze” is stale. It must not be used as an outstanding demand to amend an already revised sentence or as evidence that A10 retained the old gate.

Replace the annotation with a note that the revised A10 proposes this timing and still awaits the author's ruling. In the disposition, replace “author fact” with “owner proposal; risk (4) accepted by the author; gate ruling pending.” Keep the historical record of the concurrent mismatch visible as a dated correction if desired. No additional author acceptance can be inferred from the available quotation.

### R3-05 — LOW, C09: substantial style repair, with remaining defined-term and sentence-limit defects

**Locations:** draft :26–30, :267–270, :331–333.

ECDSA is used without explanation; USB first appears in the YubiKey definition before its explanation. The mandatory checker sentence at :267–268 has 28 whitespace-separated words excluding its list number, exceeding STE-STYLE's 20-word instruction limit. The rehearsal-record sentence at :331–333 also exceeds either sentence limit. These are bounded style defects; they do not remove the security improvements.

Explain ECDSA at first use and explain USB before or within its first use. Split the checker instruction into short rules for immutable fields/pins, horizon/version/hash linkage and permitted endpoint closure; preserve the profile's allowed null-to-end transition. Put rehearsal-record fields in a short list. Keep the corrected definitions, end references, mandatory wording and the conditional status of a later service window. No new release-count promise is needed.

## 3. C01–C09 second-pass disposition

| Finding | Result | Evidence and remaining boundary |
|---|---|---|
| **C01 — HIGH** | **WITH DEFECT** | Draft §9 :260–280 adds the independent baseline, source/trust review, checker, independent service-key authorization, build and exact-hash approval. The archive-to-build correspondence is still missing: R3-01. First-baseline construction, checker identity and independent fingerprint sources remain explicit author choices, not completed controls. |
| **C02 — HIGH** | **APPLIED** | §4–5 specifies separation, independent image verification, fresh live boot, no internal disks/swap/network/autorun, no candidate execution in the signing session, separate media roles, no NUC-written inbound medium, disconnection before unlock, output-only return and shutdown. Hostile peripheral firmware remains an explicit assumption. Signing hardware, image/device and crossing method must be selected and reviewed before rehearsal; no deployed boundary is established here. |
| **C03 — MEDIUM** | **APPLIED** | §6 and §8 require volatile keyrings, an inventory by mode, separate encrypted media, independent secret generation, protected prompts, a separate restore and verified signature for each backup and primary, shutdown/residue discipline and no hardware claims for file mode. Encryption settings and passphrase method remain choices to resolve before the ceremony. Inventory retained offline recovery material as well; never publish it as routine ceremony evidence. |
| **C04 — MEDIUM** | **APPLIED** | §7 specifies `always` signature-PIN policy and `fixed` touch, separate token roles, changed defaults/reset-code choice, read-back, second-request/PIN and missing-touch checks, agent-cache observation and immediate disconnection. The rehearsal table also requires refusal without fresh PIN verification. The commands/policy names match current Yubico documentation; actual device compatibility and behavior are untested. |
| **C05 — MEDIUM** | **WITH DEFECT** | §3 unambiguously chooses archive-byte detached OpenPGP signatures, ECDSA P-256/SHA-256 and no separate trust-file signature. §9 requires same-byte verification and a changed-byte failure. But checking a separately built verifier does not establish the binding in the archive actually signed and distributed: R3-01. Filename/version convention, exact tools/dependencies and tested commands also remain author-selected freeze work. |
| **C06 — MEDIUM** | **APPLIED** | §10 covers loss/theft/exposure stop events, uncertain theft, no automatic same-key restoration, ordinary authenticated rotation, independent compromise recovery or an explicit no-assured-recovery stop, and preservation of genuine old releases without remote-revocation promises. The recovery-path/no-path choice and restart confirmer are still unresolved; until resolved there is no authorized restart on uncertain recovery. |
| **C07 — MEDIUM** | **WITH DEFECT** | §8 adds independent fingerprint computation, actual-publication checks, retained approved artifacts and an independent first-acquisition method/assumption. The freeze-record instruction conflicts with the new key-publication timing: R3-03. The concrete authenticated first-acquisition method remains a prerequisite, not something two matching web copies supply. |
| **C08 — MEDIUM** | **WITH DEFECT** | §1 and §11 correctly keep the gate open and require selections, a dated evidence record, all eight original cases, branch-specific rehearsal and failure gating. The stale A10 annotation and the disposition's “author fact” attribution require R3-04. Add R3-01/R3-02's distinguishing cases. No rehearsal result or gate closure was inspected. |
| **C09 — LOW** | **WITH DEFECT** | §2 definitions, proposed local terms, end references and short steps substantially implement the repair. The future-window sentence retains separate rotation registration, and the service-key list remains conditional. First-use explanations and oversized instructions remain: R3-05. |

The YubiKey policy check above uses the manufacturer's [OpenPGP command documentation](https://docs.yubico.com/software/yubikey/tools/ykman/OpenPGP_Commands.html): `always` is a signature-PIN policy; `fixed` requires touch without caching and cannot be disabled without deleting the private key. This is documentation evidence, not a configured-device test. Neither policy proves that the human intended the signed archive.

## 4. Review limits and next state

The amendment's timing proposal preserves the central security boundary if adopted and implemented as described. The author's pending decisions remain pending. The quotation accepts risk (4) only. A10's rows 34–35 preserve independence under every capture-scope option and preserve the author-visible fallback; cutting the service-key listing still cannot cure a failed release boundary. Row 36 needs the scoped authentication conclusion and production-path check above.

Resolve the retained archive/build HIGH, align bootstrap and stale timing text, qualify the TEST guarantee and complete the selected procedure/rehearsal before claiming independence. Format and verification choices still belong at freeze. A later operational discovery requiring a different frozen format needs a visible amendment; the timing change cannot guarantee that no such discovery occurs.

No physical device, configured signing environment, backup, credential check, bootstrap delivery or rehearsal evidence was inspected. No release/key was generated, signed or restored; no implementation or formal/conformance suite was executed. The attack walkthroughs identify permitted readings of the procedure, not executed exploits. Only this review file was written; no amendment, disposition, profile, runbook or custody draft was edited.
