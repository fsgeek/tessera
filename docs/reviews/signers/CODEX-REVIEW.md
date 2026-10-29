Found **five defects or deployment gaps**. All requested suites pass: **KMS 48, GCP 115, issuer 121**. Additional local fault probes reproduced the timing and requester issues below. I made no repository or Git writes; test temporary files went under a fresh `/tmp/tessera-review-GuT6sZua`. No cloud commands, Terraform plan, or apply ran. Live IAM state remains unverified.

1. **SG-01 — Medium: GCP releases signatures after the deadline and skips deadline checks for cached duplicates.**  
   [signer.py:166](/home/tony/projects/tessera/service/signer-gcp/tessera_signer/signer.py:166)

   Two reproduced traces:

   - Start with one second remaining before `sign_by`; advance the clock two seconds inside `sign_digest()`. The signer returns **SIGNED**, with a valid signature, after the deadline.
   - Sign once, advance past `sign_by`, then submit the same request ID and frame. The cache returns **SIGNED** without checking either deadline. This makes the README’s unconditional late-request refusal statement false.

   **Fix:** check deadlines before both fresh and cached responses, and again after signing/self-verification. Document that withholding a late signature cannot prevent an HSM from having produced it. This affects the service stop policy; it does not independently invalidate G1–G10.

2. **SG-02 — Medium: GCP checks declared time against a clock read before fetching the frame.**  
   [signer.py:154](/home/tony/projects/tessera/service/signer-gcp/tessera_signer/signer.py:154), [policy.py:123](/home/tony/projects/tessera/service/signer-gcp/tessera_signer/policy.py:123)

   Reproduction: declare exactly `clock − 86400`; delay S3 retrieval by 60 seconds. The signer returns **SIGNED** even though the declared time is now **86460 seconds** old. The fresh clock before the HSM call checks only the stop.

   **Fix:** fetch and decode first, then evaluate ε and both deadlines using a fresh clock immediately before requesting the signature. Correct [README.md:40](/home/tony/projects/tessera/service/signer-gcp/README.md:40): a clock fault does not universally “fail safe” for ε—an adversarial declaration can track the faulty clock.

3. **SG-03 — High: prototype retirement can report success while leaving the old signing path operational.**  
   [deploy.sh:164](/home/tony/projects/tessera/service/signer-gcp/deploy.sh:164)

   Scheduler deletion, job deletion, and both key-grant removals suppress **every error** with `|| true`. Permission failures or transient failures can therefore leave `slot2-signer` consuming `tessera-slot2-requests` with the production-reused key. The final IAM read does not assert that retirement succeeded.

   That older signer has neither the new `sign_by` contract nor the configured signing stop. Its queue writers retain another signing route.

   **Fix:** tolerate only confirmed absence; fail on other errors. Before enabling production issuance, verify the old job/scheduler are absent and its service account cannot sign, including inherited grants. Move this verified gate ahead of production activation.

4. **SG-04 — Medium: the documented requester boundary omits narrower invocation capabilities.**  
   [lambda_app.py:73](/home/tony/projects/tessera/service/signer-kms/tessera_sign_kms/lambda_app.py:73), [KMS README.md:63](/home/tony/projects/tessera/service/signer-kms/README.md:63), [GCP README.md:62](/home/tony/projects/tessera/service/signer-gcp/README.md:62)

   A principal with `lambda:InvokeFunction` can submit fabricated `Records` directly, without permission to enqueue. A local fabricated-event probe produced **SIGNED**. The signature goes to the configured response queue; obtaining its bytes additionally requires access to that response path.

   Also, `iam:PassRole` plus suitable Lambda creation/update permissions can run other code under the signing role. Neither capability requires full account administration.

   On GCP, `run.jobs.runWithOverrides` permits execution-specific environment overrides, including `SIGN_UNTIL` and queue configuration, without changing the deployed image. The ordinary scheduler’s `roles/run.invoker` grant is appropriately narrower. [Google API documentation](https://docs.cloud.google.com/run/docs/reference/rest/v2/projects.locations.jobs/run)

   **Fix:** explicitly inventory and restrict invocation, role-passing, runtime impersonation, and override permissions. Update the requester descriptions; adding an event-source field check alone cannot authenticate an otherwise authorized direct Lambda caller.

5. **SG-05 — Medium: the runtime pin is absent, and DEPLOY’s Terraform example is not executable configuration.**  
   [DEPLOY.md:21](/home/tony/projects/tessera/service/issuer/DEPLOY.md:21), [DEPLOY.md:47](/home/tony/projects/tessera/service/issuer/DEPLOY.md:47)

   The current infrastructure contains no runtime-management resource, although `package.py` describes the runtime as pinned. The suggested nested `runtime_management_config { … }` is not the provider’s resource syntax.

   A runtime update between facts collection and deployment can invalidate the recorded Unicode module digest and stop pre-ship verification. This fails closed, but blocks issuance.

   **Fix:** add `aws_lambda_runtime_management_config` with `update_runtime_on = "Manual"` and the exact `runtime_version_arn`; verify facts again after the final deployment. Pin every function that relies on that install record. [Provider documentation](https://raw.githubusercontent.com/hashicorp/terraform-provider-aws/v5.100.0/website/docs/r/lambda_runtime_management_config.html.markdown), [AWS runtime controls](https://docs.aws.amazon.com/lambda/latest/dg/runtime-management-configure-settings.html)

**Q1 — Who can cause signatures?**

- **KMS:** queue writers, direct Lambda invokers, code executing with the signer role’s credentials, principals able to pass that role into suitable Lambda code, and administrators able to change policy/code/trust.
- **GCP:** production queue writers; runtime-service-account impersonators; job/code administrators; execution-override holders; direct signing grantees; key/project IAM administrators; and, until successfully retired, writers to the prototype queue.
- **Federation:** the intended chain is Google runtime identity → federated AWS role → issuer’s per-slot signer role. The final role grants frame reads, request consumption, and response writes—not request enqueueing or direct KMS signing. Its `sub`, `aud`/`azp`, and `oaud` conditions match AWS’s documented Google mapping. [AWS federation conditions](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_iam-condition-keys.html)
- **KMS Deny:** comparing `aws:PrincipalArn` to the IAM role ARN is correct for assumed-role sessions. It does **not** accidentally deny the Lambda because its credentials are an STS session. Conversely, an ordinary IAM `kms:Sign` grant to another role cannot defeat that explicit Deny; the placement decision’s suggestion that an administrator can simply grant itself signing is incomplete. [AWS principal-ARN semantics](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html#condition-keys-principalarn)

C3 remains true. The additional concerns are narrower capabilities and the prototype route omitted from a simple “captured account” description; I did not establish that unauthorized principals currently hold them.

**Q2 — Does either signer pin the other key?**

**Neither does.**

- KMS checks manifest `key_fp`, but does not pin `sset[0]`.
- GCP checks `sset[0]`, but does not pin manifest `key_fp`.

I reproduced valid possession signatures for both mixed-pair directions.

That alone does **not** make a mixed-pair receipt acceptable. Verification binds supplied keys, manifests, attestations, possession signatures, and matching DNS/git authority evidence. With honest authority records naming the real pair, a substituted pair fails.

With both authority channels captured, a fresh attacker-controlled pair already passes under the listing-cut limit. Queue access additionally enables fresh mixed-pair receipts, but does not transplant honest signed frames or produce a stronger bypass than the stated capture cases. Pinning the pair and issuer would narrow permitted signing; it is optional policy hardening, not a missing registered G10 guarantee.

**Q3 — Can TEST material become VALID_STRICT with reused keys?**

For the **two archived receipts**, **not under the current frozen production catalog**:

| Receipt | Signed declared time | Recorded T | G7 using its supplied window |
|---|---|---|---|
| real-1 | 2026-10-19 16:37:07Z | 2026-10-19 17:49:13Z | PASS |
| real-2 | 2026-10-20 01:06:25Z | 2026-10-20 01:36:51Z | PASS |

Their authority evidence declares **2026-10-19 through 2026-10-26 23:59:59Z**. At [verify.py:289](/home/tony/projects/tessera/service/verifier/tessera_verify/verify.py:289), G7 checks only:

```text
declared_issue_time >= evidence.window_start
T                   <= evidence.window_end
```

It does **not** compare against the issuer’s current production `window.json`. A later operational window therefore does not itself reject an intact historical receipt.

The actual separating check here is the signed specification hash: both archived receipts name `b2345ae9…188983`, while the frozen catalog names `397581f7…26daf`. Running the service verifier engine with the frozen catalog and archival trust inputs returned **UNVERIFIABLE / SPEC_UNKNOWN** for both, while G7 passed.

There is **no general TEST-versus-production signing namespace**. A future TEST run using the frozen catalog, production keys, and eligible authority evidence can produce a production-valid receipt. The TEST client key in [DEPLOY.md:29](/home/tony/projects/tessera/service/issuer/DEPLOY.md:29) does not mark the receipt as TEST. Likewise, a possession signature over the identical manifest is reusable.

Production release provisioning is not yet present, so this is a verified catalog/window analysis, not a completed production CLI test. Separate production keys provide a clean signing-material boundary if that separation is wanted.

**Q4 — Is the facts bootstrap sound, and can its handler be abused?**

**The mechanism is sound, conditional on completing SG-05.**

The handler reads fixed local facts, accepts no caller-selected path or digest, writes nothing, and does not construct the issuer. Packaging checks the detector digest/path and versions; verifier startup independently checks the runtime and detector functionality. The record remains an installation diagnostic, not an authority credential.

A caller authorized to invoke the poller can request those diagnostics, but cannot use this branch to rewrite `install.json`, sign, or bypass pre-ship checks. Repeated invocations can consume concurrency, as other authorized invocations can.

Facts collection hashes the detector; it does not execute its functional checks. Consequently, successful facts collection is not proof that the packaged detector runs on Lambda. Require final-runtime startup verification.

**Q5 — What do the signing stops actually bound?**

- **Both:** with a correct clock, a fresh signing operation is submitted only when the checked integer second is **≤** both cutoffs. Equality is allowed.
- **KMS:** a second clock reading withholds a signature returned after either cutoff. It still cannot prevent KMS from having generated it, nor bound delivery time after the final check.
- **GCP:** currently has no post-call withholding and skips stop checks on cached responses—SG-01.
- **Clock faults:** a slow or rolled-back clock can permit signing after the real cutoff. Neither implementation detects that. ε is a relative check against that same clock.
- **Timeouts and failures:** a timed-out invocation does not prove the remote signer failed to sign. Redelivery can generate another signature; across GCP runs and across KMS deliveries there is no durable signature deduplication. Partial-batch responses and transient retries help recovery, but a whole Lambda timeout can redeliver already-processed records.

The issuer’s 15-minute tolerance does not strengthen these signer bounds.

**Owner prechecks**

| Check | Result | Evidence |
|---|---|---|
| Capture row | **PASS** | Placement decision explicitly permits attacker-key receipts after dual capture and promises no detection: [decision:25](/home/tony/projects/tessera/docs/decisions/2026-10-27-v1-signer-placement.md:25), [decision:42](/home/tony/projects/tessera/docs/decisions/2026-10-27-v1-signer-placement.md:42). The signer READMEs introduce no stronger dual-channel guarantee. |
| Trigger clause | **PASS** | No missed-milestone cut consequence is invoked. Placement is explicitly an owner decision, [decision:3](/home/tony/projects/tessera/docs/decisions/2026-10-27-v1-signer-placement.md:3); the hybrid branch is recorded as registered in [FREEZE-RECORD.md:25](/home/tony/projects/tessera/formal/freeze-v1/FREEZE-RECORD.md:25). |
| Requester | **FAIL** | The KMS README’s two-route account is incomplete, [README.md:63](/home/tony/projects/tessera/service/signer-kms/README.md:63); GCP omits execution overrides, [README.md:62](/home/tony/projects/tessera/service/signer-gcp/README.md:62). See SG-03/SG-04. |
| Binding text | **FAIL under the supplied strict check** | The clock decision calls the IS-03/IS-09 stop “binding,” [decision:32](/home/tony/projects/tessera/docs/decisions/2026-10-27-service-clock-tolerance.md:32), while L1 explicitly labels the 96-hour margin an operating margin, **not a registered rule**, [resolutions:42](/home/tony/projects/tessera/docs/V1-SERVICE-RESOLUTIONS.md:42). Preserve these useful controls, but distinguish owner operating requirements from frozen or author-adopted requirements. |

**Verdict: Not ready for the first AWS/GCP deployment as documented; resolve the timing paths, verify prototype retirement and requester permissions, and complete the runtime pin.**

