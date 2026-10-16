# Non-author adversarial review: hybrid registration supplement

Reviewer: Codex. Date: 2026-10-14. Status: review of an unregistered draft; no adoption or discharge is asserted. Owner decisions in `DECISIONS.md` are treated as decisions, not evidence of execution. Only this review file was edited.

**Verdict: not ready to register.** The genuine V1-frame KMS capture remains incomplete, as the draft honestly reports. The selected slot-2 capture establishes HSM/signature compatibility but does not establish the deployed policy-signer path required by A9.6. The core rule-R encoding, external-μ equivalence, fingerprint definition and bounded P3 symbolic results withstand this review. Resolve the findings below before describing the pass-condition evidence as completed.

## Findings and exact fixes

### HS-01 — High: the real KMS V1-frame pass condition is still unmet

**Locations:** supplement §§8, 10.3, 11.4; A9.6 pass condition; `hybrid-golden.json` SIG-H5/SIG-H6; `spike_v1_hybrid.py`.

The real signatures are over 2123- and 6075-byte messages bearing `tessera-v1/receipt`, outside T. A and B correctly verify them as arbitrary pure ML-DSA messages; that does not turn those messages into `Frm(attest)`. R-H1/R-H2 and P-H1 use the public illustrative key. The prepared re-capture has not supplied the missing real-key evidence. This is an acknowledged completion blocker, not a discovered cryptographic failure. Owner decision 1 closes the proposed option of treating V1-shaped messages as sufficient.

**Exact fix:** retain §10.3 as incomplete until the re-capture actually runs. Archive the genuine manifest, both attestation pairs, exact signatures and keys, the large frame's length and issuer-computed μ, capture hash, tool versions, and offline A/B verification output. Both frame decoders must accept the large signed frame as `attest`, and both verifiers must verify its exact KMS signature over that frame. Update §10.3 and the evidence hashes from that saved run, before 21 Oct. Do not re-frame SIG-H5/H6. Incorporate the new evidence into the frozen vector object as owner decision 6 requires. No cloud signing was performed in this review.

### HS-02 — High: “as deployed” is not established by a direct GCP HSM capture

**Locations:** supplement §10.4 (“Met”), §11.5; A9.6 “Policy signer” and “Deadline”; `prototype/spike-pq/spike_gcp.py:49–55`; `spike_v1_hybrid.py:gcp_rule_o`.

The selected GCP custody is consistent with A9.6, and SIG-H7 is a genuine verifying rule-O signature. But the capture calls `gcloud kms asymmetric-sign` directly from the instrument. The prepared re-capture does the same. Neither artifact exercises the queue-pulling policy signer, its complete-frame validation, its own-clock declared-time refusal, or the boundary preventing the issuing AWS account from invoking the GCP key directly. Changing the frame tag or pair id will not supply that missing evidence. This finding does not assert that deployment is absent elsewhere; the reviewed evidence does not identify it.

**Exact fix:** change §10.4 to “HSM custody and offline rule-O compatibility met; deployed-slot path not yet evidenced.” For completion, identify the dated deployment/access-policy record and capture a signature through the selected external policy signer, with an accepted valid frame and a refusal for a declared time outside ε. Name the signer version, clock policy, queue path, key version and access boundary in the evidence record. Reuse already completed deployment evidence if it exists, with exact references; otherwise complete it by 21 Oct. Keep the offline rule-O checks. These are the existing A9.6 boundary and deadline, not an added independence-of-control claim.

### HS-03 — Medium: fixed rejection vectors omit mode/context and several hint-decoding obligations

**Locations:** supplement §§1–2, 8; `gen.py:1894–1950`; `check.py:mldsa65_ok`; `hybrid-reject.json`.

The 53 cases cover the principal length, slot, key, signature, possession and anchor failures. They do not contain a valid signature made with nonempty context, HashML-DSA, or μ computed without the pure prefix. XM-05 tests treating μ as the verifier's message; it does not test those different issuer-side domain computations. The fixed hint cases exercise ordering, but not a cumulative count above 55, decreasing counts, duplicate indices, or nonzero unused hint padding. Random signature mutations are useful agreement evidence but cannot ensure each named validation check is necessary: a changed commitment can mask a missing check.

Reviewer scratch probes confirmed that A and B reject nonempty-context, HashML-DSA/SHA-256, omitted-prefix and nonzero-padding signatures while their exact-length codecs accept them. Thus this is a coverage gap, not an observed acceptance bug. XHR-12 is particularly good: it remains cryptographically consistent when only the norm check is disabled; XHR-05 alone would not establish that sensitivity.

**Exact fix:** add fixed receipt and manifest-possession cases made from the same key/message with the wrong context or mode, and a μ computed without `00 00`; rebuild each anchor so the expected receipt failure is `SIG_INVALID`, not anchor mismatch. Possession failure is `POSSESSION_INVALID`. Add independent hint-decoding cases for the conditions above, all 3309 bytes and codec-valid. For duplicate/order/padding mutations of a valid signature, demonstrate acceptance when only that decoding gate is disabled; retain explicit decoder-failure checks for invalid cumulative counts. Preserve the byte-blind codec choice and update counts/hashes/agreement output. Do not add a codec `sigDecode` gate.

### HS-04 — Medium: the vectors do not establish the catalog/registry/M5 routing claims

**Locations:** supplement §§1, 5, 8; `gen.py:538–539, 592–602`; `check.py:receipt, possession`; V1-PROFILE §1 (`r2-F01`, branch-before-registration), §6.4 M5.

Both evidence implementations hard-code both ids in their candidate codec registries and use registry membership as the condition for signature verification. They have no selected catalog id or registration-state input. Consequently they verify the classical id even in a hypothetical hybrid installation, and they recognize the draft hybrid id even before registration. This is legitimate candidate-profile testing, but it cannot validate the supplement's claim that the unselected classical branch is policy-unsupported, or the profile's pre-registration opaque routing. XHR-09 only establishes the wholly unknown-id case. There is no newly discovered textual contradiction in the current profile: r2-F01 already resolves the earlier fork.

**Exact fix:** label A/B results explicitly as candidate codec/cryptographic-profile evidence. Reference separate profile-conformance results with these cases: (a) before registration, hybrid id absent, nonempty opaque signatures accepted by the codec, semantics skipped, `ALG_UNKNOWN`; (b) after hybrid registration/selection, classical id still rule O, codec-valid input contributes `ALG_UNKNOWN` and skips key/signature/possession semantics; (c) codec-invalid classical signatures still produce INVALID; (d) wholly unknown consistent ids use opaque with `ALG_UNKNOWN`; (e) unequal frame/manifest alg values still fail receipt consistency independently of support. M5 must not add `SCHEMA` solely for an unsupported well-formed alg. Do not alter the shared pair id or the r2-F01 routing rule.

### HS-05 — Low: remove stale discretionary edits and synchronize decided issuer policy

**Locations:** supplement opening status, §§1, 7, 11.3/6; owner decisions 5–6.

A9.6 expressly requires slot key/fingerprint encodings and slot-appropriate key-use assumptions in its full-byte-profile pass condition, and expressly says baseline plus supplement governs. Keeping the ML-DSA SPKI definition and K-R in the supplement is therefore within the authorized branch completion; it need not amend E§3.3 or PROOF (K). The SHA-256/SPKI fingerprint scheme itself is unchanged. However §7 still offers consequential edits to E§8 and PROOF §6, and §11 still offers edits to E§3.3 and PROOF (K), outside the one baseline edit authorized here. DECISIONS.md has already selected leaving these definitions in the supplement. Likewise §1 still proposes RAW for small frames after the owner selected always EXTERNAL_MU.

**Exact fix:** state that registration edits only E§5.2, with the branch-specific key definition and K-R carried by the supplement. Remove the optional additional baseline edits from the registration instructions; explain obsolete baseline “no vectors yet” statements as superseded for this branch by the supplement's evidence, without editing them under this authorization. Mark decisions 5–6 resolved and state always EXTERNAL_MU for attestation and possession. RAW captures may remain comparative evidence, clearly distinguished from the selected issuer path. The prepared instrument's RAW small/possession calls must not be described as testing that selected one-path issuer policy.

### HS-06 — Low: pin the published key-encoding source and distinguish specification hashes

**Locations:** supplement §§3, 9, 11.8.

The OID, absent parameters and exact DER prefix are correct, but §3 cites an unnamed future published RFC although RFC 9881 already exists. §9's implementation-spec hash is an identifiable design-reference hash; it must not be confused with the frozen multipart verification-spec object hashed in `common.spec`. The current ambiguity is disclosed, not concealed, but a dated registration should resolve it.

**Exact fix:** cite RFC 9881 §§2/4 for the OID/SPKI and Appendix D for external μ. Label the §9 implementation-spec entry “design reference”; name the exact baseline object intended by A9.6's specification hash, and separately identify the frozen verification-spec object's hash at freeze. Name the final supplement and edited E§5.2 artifact versions in the registration record. Do not silently substitute one specification object for another.

## Load-bearing checks that passed

**Rule R and external μ.** ML-DSA-65 uses 48 commitment bytes + 3200 z bytes + 61 hint bytes = 3309. The codec accepted exactly-length strings unchanged, including internally invalid ones. Length 0, 1/3308, and 3310/65536 produced respectively `SIG_EMPTY`, `SIG_FORMAT`, and `LENGTH_CAP` in both implementations. A physically incomplete enclosing anchor still has the ordinary `TRUNCATED` check; the draft's 3308/3310 examples concern present slots with those declared lengths.

Let `pk` be the **raw 1952-byte key**, not SPKI DER; `tr = SHAKE256(pk,64)`; `M' = 00 || 00 || F`; `μ = SHAKE256(tr || M',64)`. Standard pure signing supplies precisely this μ to its internal signing computation. EXTERNAL_MU supplies it directly. For the same key and signing randomness, those paths yield the same signature; hedged calls with different randomness need not yield identical bytes. Verification recomputes μ from F. SIG-H3 pins deterministic equality in A; B independently verifies it and recomputes μ. SIG-H6 demonstrates actual KMS interoperability, subject to HS-01's frame-domain limit. [FIPS 204, Algorithms 2/3/7/8](https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.204.pdf), [AWS offline operations](https://docs.aws.amazon.com/kms/latest/developerguide/offline-operations.html), [RFC 9881 Appendix D](https://www.rfc-editor.org/rfc/rfc9881.html#appendix-D).

**Key encoding, fingerprint and K-R.** The exact 1974-byte SPKI and absent parameters agree with [RFC 9881 §§2/4](https://www.rfc-editor.org/rfc/rfc9881.html#section-4). Every raw public-key bit pattern has representable ρ/t1 fields. Strict encoding precedes fingerprint matching. The existing SHA-256/SPKI fingerprint is retained, including the algorithm OID in its input. K-R explicitly says the HSM cannot validate the frame and does not see it under external μ. IAM exclusivity alone does not constrain what an authorized caller hashes; the assumption depends on dedicated-key issuer code and its access boundary. The draft is honest about that enforcement. It supplies neither HSM-enforced tagging nor a custody proof. FIPS mode separation is not an enforcement mechanism for arbitrary external μ.

**P3 attack surface and companions.** The adversary gets the sole authority signing key, public manifests and honest signatures, arbitrary payload inputs, attacker-generated keys, and independent DSKS constructors for both signature families. Honest slot secret keys are not leaked. Injective symbolic `fp`/`h`, deterministic abstract signatures and family separation are assumptions, not concrete cryptographic results. H1 does not enforce equality of both payload/type/canonicalization fields and does not prove R-3.12; the separate byte checks do that work.

| Model | Rerun result: unreachable violations / reachable witnesses | Trace interpretation |
|---|---|---|
| H1 | A, B, possession unreachable; HonestAccepted, Accept2 reachable | Correct under the stated symbolic boundary. |
| H2 | Only possession reachable | Honest `skA2` possession signature is reused under `pk(dsksR(signature,r))`; attacker names that key in a fresh tuple and signs fresh attestation bytes. Naming the accepted tuple in the possession check prevents this in H1. `.out:335–576`. |
| H3 | Only A reattribution reachable | Attacker signs identical `framedU` bytes under its own key after honest A signs them; omitted identity/fingerprint/manifest permits collision. No reuse of the honest signature or DSKS is required, exactly as predicted. `.out:478–535`. |
| H4 | No safety violation; HonestAccepted unreachable; Accept2 reachable | Rule O cannot consume honest rule-R possession/signatures. Attacker-owned keys can make entirely rule-O tuples under the compromised authority. “Fails closed” is limited to honest hybrid flow/these safety queries, not rejection of every tuple. `.out:334, 470–539`. |

The shared HonestAccepted event's saved H1 witness is slot B, not a witness that both honest signatures participate together. A scratch query emitted **only by JudgeA** also proved reachable while all three safety queries stayed unreachable. This addresses slot-A vacuity for this review; it is not registered evidence. Optional exact evidence improvement: add distinct slot-A/slot-B honest witnesses to future registered model headers/results. H2/H3/H4 count for their stated properties; H3 is not evidence of a DSKS transplant and H4 is not a red safety companion. Header assertions that predictions predated the first runs were read; this review did not independently reconstruct their historical timestamps.

**R-3.12/M5.** One pair id in both frames and the manifest is sound. Slot position selects the scheme. Fingerprint prefixes remain disjoint. XHR-08 rejects the M9 mixed-id shape. M5 derives fingerprints from both authenticated channels and alg from the frozen catalog; it does not require both slots to use the same signature family. HS-04 concerns evidence coverage of that routing, not a reason to change the construction.

## Reproduced evidence and limits

Python 3.14.6; ProVerif 2.05; rfc8785 0.1.4. Read the requested supplement, A9.6, E§3.3/§5, PROOF (K)/Lemma 7a and relevant proof boundaries, both hybrid implementations and vector sets, model headers/bodies/results and companion traces, owner decisions, current profile routing/M5, and the capture instruments used to assess completion.

- A regenerated in a temporary copy, using the saved real captures: all self-checks passed; all four baseline/hybrid JSON files reproduced byte-for-byte. No source/vector file was regenerated in the repository.
- B: baseline 71/71 golden, 173/173 rejection, 5/5 controls; hybrid 20/20 golden, 53/53 rejection, 1/1 control.
- Full differential fuzz: 90,400 cases, zero disagreements (60,000 baseline plus 30,400 hybrid). Hybrid histograms matched the draft: 2422 accepted anchors, SPKI outcomes 9400 `KEY_FORMAT` / 596 `KEY_MISMATCH` / 4 OK, and signature outcomes 360 false / 40 true. These are seeded agreement results, not exhaustive correctness evidence.
- All four ProVerif models reran with the existing theory library; every query polarity matched the saved outputs and header predictions. Rerun output was not written over the saved results.
- The recorded E, PROOF, implementation-spec and hybrid-vector hashes matched the reviewed bytes.
- Source inspection confirms no A/B import of each other or common local codec/ML-DSA implementation. A uses butterfly NTT and integer packing; B uses direct root evaluation/interpolation and a bit cursor. A checks an SPKI prefix/length; B parses DER fields. Shared Python/hashlib primitives and the single original author instance remain correlated dependencies. “No shared code” means no shared local implementation, not independent authors or independent cryptographic backends.

The draft's hand-run external-library and planted-defect claims were not all rerun here. None of these checks establishes real ML-DSA/ECDSA security, historical key honesty, policy-signer deployment, full bundle validity, or capstone discharge. Registration remains conditional on the existing A9.6 deadline and completion evidence.
