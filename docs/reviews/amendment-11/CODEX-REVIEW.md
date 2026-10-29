The amendment is a defensible repair in principle, but **not ready to sign as written**. I found no demonstrated failed P3 result being relabelled as a pass. However, the draft leaves room to weaken discharge requirements and understates the retrospective change to slot-2 qualification.

I reviewed the working-tree draft against the registered sources, `270ca49`’s custody record, signer code, and review records. The profile run returned **1,191 passed, 1 skipped**; the skipped check binds the evidence to an actual deployed package. No repository edits or git writes were made.

1. **A11-01 — High: the replacement floor needs explicit discharge prerequisites.**  
   **Location:** [A11:32](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:32), especially lines 35–37 and the replacement table at line 63.

   **Scenario:** A reviewer treats the passing floor as sufficient to discharge P3 despite an unverified deployed artifact or a recorded, unresolved defect. The current wording requires disagreements to be *recorded* as policy or defect, but does not state which defects prevent discharge. The deployed-package check can skip at [test_p3_profile.py:151](/home/tony/projects/tessera/formal/p3-verification-profile/test_p3_profile.py:151).

   A1 required an implementation verification profile: exact library/version, encodings, key-validation behaviour, equation behaviour, and negative vectors, recorded as H1a evidence. The supplied evidence substantially covers those obligations. Replacing their explicit enumeration with “owner-enumerated vectors” makes preservation depend on the current directory’s contents.

   **Fix:** Retain the applicable original fields explicitly; register the algorithm-specific substitutions; bind the baseline evidence to immutable files or a manifest; require deployed-build identity before implementation discharge; and state that unresolved defects affecting the required behaviour block discharge. Distinguish adoption of this discharge criterion from discharge itself.

2. **A11-02 — High: the custody change is a retrospective exception, and “the hybrid itself is not in question” is too absolute.**  
   **Location:** [A11:86](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:86).

   **Scenario:** Historical success of the hybrid spike is used to authorize a replacement implementation that did not satisfy the deadline. [A9:389](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:389) expressly requires deadline qualification of the final custody implementation and otherwise invokes the fallback. The frozen profile independently retains the selected, deadline-qualified implementation at `270ca49:docs/V1-PROFILE.md:1023–1026`.

   The October 14 evidence remains historical evidence; changing implementations does not erase it. But that does not automatically qualify the replacement.

   **Fix:** Say explicitly that the proposed ruling relaxes the implementation/deadline restriction after the deadline and after candidate code exists. Preserve the historical qualification while authorizing a named replacement subject to new evidence. Explain that retaining the hybrid with that replacement depends on this ruling.

   Also avoid equating every source port with a new custody selection: the E9 record already permits source porting with production evidence at [AUTHOR-RULINGS.md:119](/home/tony/projects/tessera/docs/reviews/e9-packet/AUTHOR-RULINGS.md:119). Explain why this candidate exceeds that permission.

3. **A11-03 — High: the sweep missed the spike-key deletion commitment.**  
   **Location:** [A11:75](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:75), [SWEEP:14](/home/tony/projects/tessera/docs/reviews/stale-dependencies/SWEEP-2026-10-28.md:14).

   **Scenario:** Production reuses keys whose registered disposition was deletion. [HYBRID-SUPPLEMENT.md:524](/home/tony/projects/tessera/formal/p8/HYBRID-SUPPLEMENT.md:524) says both spike keys are deleted after recapture verifies and review clears. [DEPLOY.md:18](/home/tony/projects/tessera/service/issuer/DEPLOY.md:18) instead proposes reusing both TEST keys. The signer disposition calls that an owner decision at [DISPOSITION.md:18](/home/tony/projects/tessera/docs/reviews/signers/DISPOSITION.md:18).

   **Fix:** Add this dependency to the sweep. Either use replacement production keys or obtain an explicit author ruling changing the deletion commitment, with the prior-use limitation stated. Conditions (i)–(iii) about the implementation do not resolve key reuse.

4. **A11-04 — High: conditions (i)–(iii) do not expressly preserve the entire registered enforcement boundary.**  
   **Location:** [A11:90](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:90).

   **Scenario:** Deployment satisfies the abbreviated property list while the issuing account can alter the signer’s policy or clock, impersonate its runtime identity, or reach another signing path. [A9:382](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:382) requires complete-frame validation and denies the issuing account those capabilities. “Sole `roles/cloudkms.signer`” is insufficient to establish that boundary.

   DEPLOY steps 7–8 appropriately address retirement and requesters, but do not themselves specify verification of every claimed property—frame validation, image identity, clock policy, and negative controls.

   **Fix:** Require preservation of **all A9.6 custody and policy requirements**, plus the frozen record’s properties. Define the re-earned evidence: deployed positive signature verification, malformed/tag/algorithm/fingerprint/time refusals, requester and administrative-access review, retirement of alternative paths, and identification of the tested image and configuration.

   The prototype-cost description is otherwise supported: [main.py:185](/home/tony/projects/tessera/prototype/policy-signer/signer/main.py:185) accepts only inline requests; it has no `sign_by` or window stop. IS-09 documents the oversized-message failure at [CODEX-REVIEW.md:35](/home/tony/projects/tessera/docs/reviews/issuer/CODEX-REVIEW.md:35). These are costs of retaining its behaviour, not proof that literal deployment from `prototype/` is mandatory.

5. **A11-05 — Medium: distinguish stable specification semantics from preserving buggy implementation outputs.**  
   **Location:** [A11:28](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:28), [A11:54](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:54).

   **Scenario:** A later vector exposes an implementation that accepts an originally prohibited malformed signature. “New findings never rewrite a V1 verdict” could be read as requiring preservation of that false acceptance.

   A9.4 preserves the governing specification and expressly retains its original malformed, unsupported, and prohibited cases at [A9:278](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:278). A new algorithm-security assessment belongs beside the verdict; an implementation-conformance defect needs separate treatment.

   **Fix:** Distinguish later security-policy findings from failures to implement the existing specification. Do not silently change policy or preserve erroneous outputs as normative V1 behaviour. Record affected releases and explain corrections explicitly.

   The symbolic proofs themselves remain unchanged. Passing this floor supplies bounded implementation evidence; it does not establish general preservation of every model assumption.

6. **A11-06 — Low: 21 cases are not exercised at library level.**  
   **Location:** [A11:48](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:48).

   **Scenario:** Readers understand all 240 unroutable ECDSA cases to have been tested against the backend. In fact, the 219 DER cases reach library verification, while the 21 wrong-length P1363 cases return `NOT_ROUTED` before verification at [test_wycheproof.py:177](/home/tony/projects/tessera/formal/p3-verification-profile/test_wycheproof.py:177).

   **Fix:** State the split: 219 library-tested DER cases; 21 P1363 cases outside both interfaces. The claimed zero disagreements remains correct within the stated routing.

7. **A11-07 — Medium: disclosure identifies the P3 outcome, but not all outcome-informed changes.**  
   **Location:** [A11:7](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:7), [A11:19](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:19).

   **Scenario:** A reader sees an amendment strengthening an inadequate checklist, without seeing that it also permits late qualification of an already-built signer.

   Furthermore, only the curve-specific fields lack an ML-DSA referent. The whole checklist is not “met vacuously”: exact library/version, encodings, key validation, and negative vectors still apply.

   **Fix:** Disclose each retrospective change separately, identifying what was known and which previous condition changes. Replace the blanket vacuity claim. Remove the stale “Sections marked PENDING” sentence: no such sections remain, and the run and sweep already exist.

**H3:** Non-amendment is the correct disposition. [The original:232](/home/tony/projects/tessera/docs/phase-0-prereg.md:232) states system costs; its AWS examples do not restrict measurement to AWS. Including every provider preserves the existing scope and needs no new hypothesis. The draft should say “AWS-based examples,” rather than implying an explicit AWS-only exclusion.

Record a measurement protocol before measurement: include retained locked storage and other residual resources, identify the demonstration/idle periods, and report all three components separately. An operated minute-by-minute signer/poller outside demonstrations conflicts with the registered idle-compute condition; accepting that falsification is appropriate. Do not redefine the whole operating window as a demonstration to avoid it.

**Citation check:** The explicit amendment locators to A1:144–148, A9:267–283 and :381–392, A10:675, preregistration:232–248, PROPERTIES:37, and FREEZE-RECORD:81 land on the intended material. The A10 row-25 correction is supported by the author’s explicit CUT; no schedule-slip trigger is needed. Improvements still needed:

- Pin the normative custody citation to `270ca49` and its exact range.
- Replace bare “S1” with [V1-SERVICE-RESOLUTIONS.md:20](/home/tony/projects/tessera/docs/V1-SERVICE-RESOLUTIONS.md:20), identifying it as a stamped **owner operational resolution**, rather than implying it is an original registered requirement.
- The frozen profile’s reference to supplement “§9 item 6” is stale: the deletion sentence is now **§11 item 6**, lines 524–526. Preserve the frozen bytes and supply a corrected locator.

**Owner prechecks:**

| Check | Result | Evidence |
|---|---|---|
| Capture row | **PASS** | [A11:28](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:28) and [A11:90](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:90) claim bounded verification/custody behaviour, without promising rejection of fresh attacker-key receipts or capture visibility. |
| Trigger clause | **FAIL** | [A11:89](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:89) treats historical qualification as settling the hybrid question without resolving the replacement’s deadline condition. A11-02. |
| Requester | **PASS** | [A11:91](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:91) names the request path and incorporates DEPLOY’s requester gate. Completeness still requires A11-04. |
| Binding text | **FAIL** | [A11:99](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:99) uses the owner’s S1 resolution as an unexplained binding yardstick. Identify its authority level; stamping alone does not make it a signed amendment or author ruling. |

**Verdict: Not ready for the author’s signature; resolve A11-01 through A11-07 first.**

