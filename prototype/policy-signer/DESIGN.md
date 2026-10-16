# Slot-2 policy signer: spike deployment design (OWNER DECISIONS 2026-10-14)

Instrument code under A9.2 (it lives in `prototype/`). It exists to produce A9.6's "deployed-slot" evidence before
21 Oct (Codex HS-02). It becomes the V1 issuer's design input; it is not service code.

**What A9.6 requires.** A queue-pulling policy signer outside the issuing AWS account validates the complete V1
frame and enforces the declared-time check against its own clock (ε = 24 h, A9.2) before requesting a signature. The
issuing AWS account can enqueue frames but cannot invoke the slot-2 key directly, change the signer's policy or
clock, or obtain its key-use credentials. The slot-2 key is dedicated to V1 tagged type-0x00 documents
(attestation and manifest-possession).

**Decisions.**
1. **Queues are in AWS** (us-east-2): SQS `tessera-slot2-requests` and `tessera-slot2-responses`. The issuer
   enqueues requests and reads responses. Queue content is untrusted input to the signer.
2. **The signer runs in GCP** (project `tessera-slot2`, us-east1) as a Cloud Run job on a Cloud Scheduler trigger
   (every minute). Its service account is `slot2-signer@tessera-slot2.iam.gserviceaccount.com`, with
   `roles/cloudkms.signer` and `roles/cloudkms.publicKeyViewer` on key `slot2-spike` only: no project-level roles,
   no other keys.
3. **No static credentials cross the boundary.** The signer reaches SQS by assuming an AWS IAM role through web
   identity federation (Google-issued OIDC token for the service account, `accounts.google.com` as provider, trust
   condition on the service account's unique ID). The role allows only `sqs:ReceiveMessage`,
   `sqs:DeleteMessage`, `sqs:ChangeMessageVisibility` on the request queue and `sqs:SendMessage` on the response
   queue. The AWS account holds **no** GCP credential of any kind.
4. **Validation before signing.** The signer vendors the P8 reference decoder (gen.py's decode path) and checks:
   - the frame decodes under tag `tessera-v1/attest` or `tessera-v1/manifest`, within schema;
   - for attest, `common.alg` is the registered id and `signer.key_fp` equals this key's `gpg-sha256` fingerprint;
   - `declared_issue_time` is within ε of the signer's own clock (Cloud Run's system clock, which Google
     synchronizes).

   On any failure it sends a signed-nothing refusal response with a reason, and logs it.
5. **Output** is a rule-O packet built exactly as in `spike_gcp.py` (one v4 type-0x00 OpenPGP packet), returned on the
   response queue with the request id.
6. **Evidence to capture** (record in `prototype/policy-signer/EVIDENCE.md`):
   - (a) a valid frame enqueued and signed, with the signature verified offline in both P8 codecs;
   - (b) a frame with declared time 25 h in the past, refused;
   - (c) a wrong-tag or wrong-key_fp frame, refused;
   - (d) a demonstration that the AWS role used by the issuer (the tessera SSO role) has no path to the GCP key: no GCP
     credential exists in AWS, and the GCP key's IAM policy lists only the signer service account;
   - (e) the exact signer version (image digest), key version, IAM policies and queue ARNs;
   - (f) every cloud resource created, in a manifest, so it can be torn down.
7. **Limits stated, not hidden.** A takeover of the AWS account can still enqueue any valid frame at the current
   time, and it will be signed. That is C3 and is accepted. The issuer must not be able to call the GCP key directly.
   A takeover of the GCP project defeats slot 2 alone.
