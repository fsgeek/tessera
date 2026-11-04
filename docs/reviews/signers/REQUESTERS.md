# Who can cause a signature (DEPLOY.md step 8, SG-04) — owner, 2026-11-02

Enumerated against the live accounts after steps 5–7. Method: the live KMS key policy, the IAM inline and attached
policies of every role in account 477139661040 (there are no IAM users), queue listing, the GCP key and project
IAM. `iam simulate-principal-policy` is **unusable** here: the account is an Organizations member and the simulator
returns `explicitDeny` with `AllowedByOrganizations: false` for every request, including ones the role plainly allows.
So this is a policy reading, not a simulation, and should be confirmed by a reviewer.

## The account's place in AWS Organizations

- 477139661040 (Tessera) is a **member account** of organization `o-iljslwvgd9`. The management account is
  **871341458535**, email `aws-tessera@wamason.com`, the author's login. SCPs are enabled.
- The author's session is `AccountFullAccessRole` (AdministratorAccess), assumed via `account-access.amazonaws.com`.
- The management account can also assume `AWSManagedAccountManagementAccessRole` (via
  `aws-role-management.amazonaws.com`), whose policy can create roles, attach policies and update trust policies: a
  full privilege path. And `AWSManagedAdvancedFeaturesActivationRole` (via `account.amazonaws.com`).
- **So the author's administrator identity is the management account 871341458535 and whoever holds its
  credentials.** Everything below that says "admin" means that.

## kms slot (AWS KMS key `2c9ba2cf-…`, ML-DSA-65)

| Capability | Who | Basis |
|---|---|---|
| `kms:Sign` | `tessera-v1-signer-kms-role` only | Live key policy: SignerRoleOnly + DenySignToEveryoneElse. Negative test: the admin session was refused with an explicit deny (DEPLOY-RUN 2026-11-02). |
| Send work to the signer (`sqs:SendMessage` on `tessera-v1-issuer-kms-requests`) | `tessera-v1-issuer-poller` (by design); admin | Poller inline policy; AdministratorAccess. |
| Change the signer (`lambda:UpdateFunctionCode`, `iam:PassRole` on the signer role, change the role) | admin | AdministratorAccess; management roles. |
| `kms:PutKeyPolicy` | the account root principal, i.e. any account administrator | Key policy KeyAdministrationWithoutSign. A management event, recorded by the Object-Locked trail. |

## gpg slot (GCP KMS `slot2-v1`, HSM P-256)

| Capability | Who | Basis |
|---|---|---|
| `cloudkms.cryptoKeyVersions.useToSign` on `slot2-v1` | `tessera-signer-gpg@tessera-slot2` only (key IAM) | `gcloud kms keys get-iam-policy slot2-v1`: signer + publicKeyViewer, that SA only. |
| Send work (`sqs:SendMessage` on `tessera-v1-issuer-gpg-requests`) | `tessera-v1-issuer-poller`; admin | As above. The signer's AWS path is federated: Google ID token → `tessera-v1-signer-gpg-federated` → `tessera-v1-issuer-signer-gpg` (receive requests, send responses, read `frames/*` only). |
| Run, update or override the job; act as or mint tokens for the runtime SA; change key IAM | GCP project owner `wamason@gmail.com` (the only human principal) | Project IAM: `roles/owner` is that user alone; the rest are Google service agents and `slot2-builder` (log writer only). |

## Outside the V1 path, still present

- `tessera-slot2-signer-sqs` (AWS role, 2026-10-14 prototype): assumable only by the disabled prototype SA
  (uniqueId 100451337620005518976); reaches only `tessera-slot2-requests/-responses`, which feed nothing. Cannot
  cause a V1 signature. Delete with the prototype queues and the spike keys (HYBRID-SUPPLEMENT §11 item 6).
- Spike keys `alias/tessera-pq-spike` and `slot2-spike`: retire-instrument removed the prototype's signing access to
  `slot2-spike`; deletion follows the supplement's conditions.

## Result against the gate

Beyond the issuer (poller), the two signers and the author's administrator identity, **no principal can cause a
signature**. The gate passes, with two notes that belong in the V1 contract's limits, not in a fix:
1. The administrator identity is two credentials in two clouds: the AWS management account (871341458535) and the
   GCP owner `wamason@gmail.com`. Capturing either one gives control of that one slot's signer. Capturing both gives
   control of both. This is C3, already disclosed.
2. AWS Organizations adds the management account's role-management path, which is not visible from the member
   account's own IAM. The CloudTrail trail records its effects in this account.
