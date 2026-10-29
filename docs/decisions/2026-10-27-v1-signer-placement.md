# Where V1's signers and services run (2026-10-27)

> **Status: OWNER DECISION**, by the owner instance (Claude Opus 5.5), 2026-10-27. It closes the "signer split"
> item that the 2026-10-26 handoff left open as an author question. It changes no guarantee in `docs/V1-CONTRACT.md`. *(Corrected 2026-10-28: it first said it changed no
> registered sentence. It changes K-R's enforcement wording in `formal/p8/HYBRID-SUPPLEMENT.md` (who computes `μ`,
> who may `kms:Sign`); that is Amendment 11 §A11.5 item 5, for the author.)* Contestable by the author at any time.

## Why this is the owner's call

On 2026-10-24 the author agreed to put the AWS-slot caller in an Azure VM and the GCP-slot caller on Linode. On
2026-10-26 the previous owner withdrew the reason it had given for that: a signer outside the issuing account still
signs whatever the issuer sends it, so the split does not stop a captured issuer from getting signatures. Asked
today what he wanted Azure and Linode for, the author said: *"I'd suggested them as places for the service. We have
the linode instance, and I have a budget ($70/mo) via my MSDN subscription for Azure."* They were offered as
resources, not as a requirement. Choosing among resources is owner work.

## Decision

1. **Slot 2 (GCP HSM, P-256) stays as it is**: the existing GCP policy signer, its own policy and its own logs.
2. **The KMS slot (ML-DSA-65) is signed by a policy signer in the issuing AWS account**, under its own IAM role. That
   role is the only principal granted `kms:Sign` on the key. The issuer roles keep no KMS permissions (already true,
   `service/issuer/infra/main.tf:181`, checked by `tests/test_infra.py`). The signer reads frames from the existing
   per-slot SQS queue and applies the same policy as slot 2.
3. **CloudTrail**, with all management events, read and write, including KMS (`kms:Sign` is a management read event
   in CloudTrail, not a data event; corrected the same day by the signer build), writes to an S3 bucket with Object
   Lock in compliance mode. A captor can stop the trail from then on, but cannot delete what is already logged, and stopping the trail
   is itself logged. This supports the AJ7 capture-notice recommendation. It adds no claim: V1 still promises no
   detection.
4. **No Azure or Linode in any signing path in V1.** Linode keeps serving wamason.com and never holds a signing role.
   Azure is used for the **dead-service test** (4 Dec). A clean VM outside AWS verifies receipts with the Tessera
   endpoint switched off. This uses the author's MSDN credit for the one V1 test that benefits from being off AWS.
5. **A separate AWS signing account** (the previous owner's recommendation) is recorded as a **V2 candidate**, next to
   the disjoint-authorities design (A9.3). Moving the KMS signer to another account later means redeploying
   `service/signer-kms/infra` there with cross-account access to the queues and frames. That is a deployment change,
   not a redesign. (Corrected the same day: this first said it was a change of one variable.)

## Checks run on this decision

- **Who can ask for a signature?** For the KMS slot: whatever can write to its SQS request queue (the issuer
  roles), and any principal with IAM administration in the account, which can rewrite the key policy (`PutKeyPolicy`, held by the account root) to grant itself `kms:Sign`; an ordinary IAM grant cannot override the key policy's explicit Deny (corrected after the signer review, Q1). The full list of narrower routes, such as direct Lambda invocation and `iam:PassRole`, is in the signer READMEs and is checked at deployment (`service/issuer/DEPLOY.md` step 8). The same
  holds for slot 2 through its queue. This is C3 as already registered: *capturing the issuing AWS account means
  both slots can sign.* Nothing in this decision weakens or strengthens that.
- **Both authority channels captured:** unchanged. G10 protects honest receipts, and new receipts under the
  attacker's own keys pass (`docs/V1-CONTRACT.md` §2, §4).
- **Simplest alternative considered:** a single account, with no separate signer role and the issuer holding
  `kms:Sign`. Rejected: the design already separates the issuer from the signer (IS-03/IS-09), and undoing that
  would cost code changes for no saving.

## What the separate account would have bought, and why V1 does without it

It would put a policy and its logs out of reach of an admin of the issuing account. That gives policy the captor
can't override, and logs it can't erase. Object Lock gives the second within one account. The first needs a second
controller, and V1 already states that one controller holds both keys (`docs/V1-CONTRACT.md` §3). The yardstick is
the author's: *"build something that works, with known limitations"* (2026-10-24).
