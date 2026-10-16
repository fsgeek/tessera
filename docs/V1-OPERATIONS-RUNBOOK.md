# V1 operations runbook

> **STATUS: DRAFT, 2026-10-12. Not registered.** Owner instance (Claude Opus 5.5). This file receives what the
> Amendment 9 review disposition (`docs/reviews/amendment-9/DISPOSITION.md`, Skeptic 2/10/12, 6, 11, 15; Codex 2, 8)
> moved out of the instrument. Nothing here is a verifier rule or a registered parameter, and changing it needs no
> amendment. Where it touches a registered invariant, the invariant is in `docs/phase-0-prereg-amendment-9.md` (A9.6)
> and this file only implements it. Revised 2026-10-13: slot-2 custody wording reconciled with A9.6 using the exact
> replacements of `docs/reviews/a9-custody/CODEX-REVIEW.md` finding 3 (owner disposition 2026-10-13).
> Revised 2026-10-14: §5 (issuer chain-order duty) and §6 (release key, custody OPEN) added from the owner-disposed
> spec-sufficiency resolutions (`docs/reviews/spec-sufficiency/RESOLUTIONS-DRAFT.md`, G02 and G08; A9 C4 and A9.5).
> Revised again 2026-10-14 after `docs/reviews/v1-profile-r2/CODEX-REVIEW.md` (owner disposition
> `docs/reviews/v1-profile-r2/DISPOSITION.md`): the 21 Oct hybrid custody deadline (§1), pre-ship proof and snapshot
> checks for the profile's fail-closed completions (§5), and release-key bootstrap/rotation/recovery tracking (§6).
> Changes are tagged `[OWNER 2026-10-14, r2-Fxx]`.

## 1. Hardware

- **If token custody is selected: YubiKey 1, the gpg signing token.** Holds the `gpg` slot's P-256 key, generated on the token, non-exportable.
  PIN required; touch **off** for signing (the queue-fed signer runs unattended). It stops key export, not misuse:
  whoever controls the queue has signing capability (A9 C3).
- **YubiKey 2: the offline repository root.** Touch and PIN required. Generated on an **air-gapped machine**, with an
  **encrypted offline backup** held separately. The generation and signing ceremony is written down and rehearsed
  before first use. Its acts are limited to key publication and rotation commits and the end-of-issuance statement
  (§4).
- **Loss of the selected slot-2 token.** Issuance stops. Loss cannot be told apart from theft, so the current window is treated as
  compromised until its not-after: a published window cannot be shortened (A9.6). Issuance resumes only under a new
  key, which needs a registered rotation mechanism (A9.6), or not at all.
- **Loss of YubiKey 2.** Restore the root from the encrypted offline backup, by the written ceremony. If the backup
  is also lost, no new key assertion can be signed by the key in the verifiers' trust configuration: that needs a
  new verifier release, and every relying party must update. Existing receipts are unaffected.

- **If slot-2 custody is a token (A9.6, chosen before 30 Oct), YubiKey 1 is in every receipt's signing path.** Issuance
  throughput and availability are those of one USB token on the author's host: if that host, its power or its
  network is down, issuance stops. This follows from prereg §3 C (a local signer in a failure domain independent of
  AWS) made physical by the author's hardware requirement. It would be acceptable for V1 (one domain, about a dozen
  test receipts). It contradicts the product thesis ("cheap, easy") at any real volume.
  - *Measure before the 30 Oct freeze:* sustained signatures per second on the real token, using a throwaway key
    and resetting the applet afterwards. Until measured, any throughput figure is a prediction.
  - **Alternative V1 custody (A9.6):** an HSM-generated non-exportable P-256 key at a non-AWS provider, used through the external queue-pulling policy signer. The dated profile choice records the provider, key version, policy boundary, OpenPGP adapter and immutable public-key packet. Its authority is evidenced through the same DNSSEC and signed, anchored git key-publication record.
  - **Deadline (A9.6) [OWNER 2026-10-14, r2-F17].** For the hybrid, the final custody implementation must have
    completed the deployed-slot pass-condition evidence by **21 Oct**. Selection may be deferred to before 30 Oct only
    among custody implementations that each met that deadline; otherwise the registered fallback is taken
    (V1-PROFILE §14.2 item 5).

- **Signer isolation (OWNER DECISION 2026-10-13, prompted by the author's three-cloud proposal).** Each signer runs
  inside its own provider's private network with no inbound path. It pulls requests from a queue and pushes
  signatures back. Each key accepts use only from inside that network: in AWS, a KMS key-policy condition on the VPC
  endpoint; in GCP, a VPC Service Controls perimeter around Cloud KMS. Stolen credentials alone then cannot sign.
  There is no cross-cloud private network, because it would be a shared component coupling the two failure domains.
  *V2 note (not registered):* the public API moves to a third provider (Azure), so capture of one signer's cloud
  yields one slot, not two. Capture of the API layer still yields both, until there is separation of control.
- **Monoculture check (open, before 30 Oct).** Heterogeneous layers are defeated when the components underneath turn
  out to be identical (the author's procurement observation). Before choosing slot-2 custody, record which HSM
  vendor and certification sits under AWS KMS and under GCP Cloud HSM. If both slots rest on the same HSM product,
  their failure domains are less independent than the design assumes. *Not yet checked; treat any statement about
  it as a prediction.*

## 2. Operating numbers

- **Window length:** fixed when the key-publication record is published; at most 90 days (A9 invariant,
  `DNS_WINDOW_LENGTH`).
- **Retirement margin: 96 h = δ + 24 h.** The issuer stops signing 96 h before `issuance-not-after`. This is an
  owner-selected operating reserve, not a proved signing-to-anchor bound: δ is a declared-time-to-chain-time
  tolerance, and A2.1 gives no finite backward-skew bound (Codex finding 2). Safety does not depend on it: an attempt
  whose T would exceed not-after is not shipped (A9.6), whatever the margin.
- **Rotation plan.** Before the stop point of the single 90-day window, record one of: a rotation mechanism
  registered by amendment (multiple records or per-key owner names), or the end of issuance (§4).

## 3. Slot-2 declared-time check

The `gpg`-slot signer compares each frame's `declared_issue_time` with its own clock and refuses to sign if the
difference exceeds ε (24 h, A9.2). This limits an AWS-side takeover to minting at the current time (A9.6); it
does not stop it. A clock fault on the signer host shows up as refusals, which fail safe. For HSM custody, the external policy signer enforces this check before submitting the OpenPGP digest; AWS has no direct key-use permission.

## 4. Exit procedure

When V1 stops issuing:
1. **Disable issuance:** stop the API and the queue consumer; the issuer signs nothing more.
2. **Initiate key destruction:** schedule KMS key deletion; initiate destruction of the selected slot-2 key (token applet reset, or the non-AWS provider's key-version destruction procedure). Scheduling a KMS
   deletion starts a waiting period; it is not destruction.
3. **Record completion** of destruction as an operational fact, with the date, once the KMS deletion has completed
   and the selected slot-2 key's destruction has completed. If a token is lost, record that instead (§1).
4. **Publish an end-of-issuance statement** as a git commit signed by the repository root (YubiKey 2), OTS-stamped on
   its signed commit id.

Verification of existing receipts needs no private key. No V1 verifier rule consults the statement; it is evidence
for a later examiner. After the exit, the window's not-after, not the statement, is what bounds minting (A9.6
guarantee 2, in chain time).

## 5. Issuance gate: chain-order pre-commitment (A9 C4; OWNER 2026-10-14, G02)

**Issuer duty.** Do not issue in a window until the key-assertion commit's stamp has k = 6 confirmations and the
receipt will anchor at a higher height (chain-order pre-commitment, A9 C4).

- Before the first receipt of a window: obtain the key-assertion commit's upgraded OTS proof, validate it offline
  under the V1 rules (qualifying attestation at height h_git, headers h_git … h_git + 5 present and pinned), and
  record h_git and T_git.
- The verifier requires `h_git + 5 < h_receipt` (`INVALID / GIT_NOT_PRECOMMITTED`). A receipt whose stamp is
  submitted after the issuer has observed block h_git + 5 is mined above it, so the wait satisfies the rule. No
  clock comparison with `declared_issue_time` is made (owner, 2026-10-14).
- The issuer still checks both rules on each receipt's own evidence before shipping (a receipt ships only when
  complete, A9.1). A receipt that fails either is not shipped; it is re-stamped or abandoned.
- **Pre-ship checks for the profile's fail-closed completions** [OWNER 2026-10-14, r2-F07, r2-F08, r2-F09,
  r2-F10]. Before shipping, also check on the receipt's own evidence: the selected path of each of the three proofs
  (receipt, snapshot, git) has the transaction-shape subset and the conventional merkle suffix (V1-PROFILE §15.2;
  the git proof is checked once per window, when h_git is recorded); the snapshot body has no RRSIG with fewer
  Labels than its owner (§15.3); every OpenPGP signature (both slots, possession, the repository commit) carries
  type-16/type-33 subpackets only in the shapes V1-PROFILE §8 allows. A failure means re-stamp, re-capture or
  re-sign before shipping, never ship. All 352 Bitcoin paths in the repository's 129 proofs pass the proof checks
  (owner check 2026-10-14).
- This is chain order, not UTC (A2.1). It does not establish that the assertion was published before issue.

## 6. Release key (A9.5 trust-configuration authority; OWNER 2026-10-14, G08)

**Custody: OPEN.** Not chosen. Due before the 30 Oct freeze.

- **What it does.** Signs each verifier release. Each release compiles in the SHA-256 of exactly one trust
  configuration and the frozen spec catalog; the verifier refuses any other configuration
  (`TRUST_CONFIG_UNAUTHENTICATED`, no verdict). The trust configuration itself carries no signature.
- **Independence requirement.** The release key must be unusable by the DNS credential, the repository root
  (YubiKey 2), the issuing AWS account, and any service those can invoke. Key inequality is not enough: the dated
  custody record must name the key, its holder and its access boundary, and show that capture of any
  authority-channel credential grants no ability to sign a release, authorize a configuration hash, or replace the
  compiled trust root. CI is not the authenticity check.
- **Not YubiKey 2.** The repository root signs key assertions; if it also authorized releases, capture of one
  channel credential would let an attacker distribute a configuration trusting their own keys and pins, collapsing
  n = 2.
- **Candidates, not decided:** a third hardware token, generated air-gapped with an encrypted offline backup and a
  written ceremony like YubiKey 2's; or an HSM key at a provider that holds none of the channel credentials. YubiKey 2
  itself is not yet in hand.
- **Before each release:** run the release checker (G09 invariants: immutable entries and pins, nondecreasing
  `as_of`, version + 1, `previous_sha256` chain, non-retroactive closing of open ends), then sign. Close a KSK's open
  end before `as_of` passes IANA's announced retirement.
- **Bootstrap and rotation.** Publish the release public key with the verifier documentation and relying-party
  text, and record its fingerprint in the freeze record. A new release key is introduced only by a release signed
  with the current one. The procedure is OPEN with custody.
- **Loss or compromise.** Compromise is distribution compromise, a stated A9 boundary: a malicious release could
  trust attacker keys and pins and so accept forged evidence. Existing receipts stay verifiable under genuine
  releases, and relying parties must obtain a release under a new key by some authenticated path. Loss stops new
  releases (configuration updates, new pins) until a recovery path exists. Both procedures are OPEN with custody.
- **Required test before freeze:** a captured repository signer, a captured DNS credential and the issuing AWS
  account each try to authorize a configuration; the verifier refuses all three.
- **Tracked as freeze items** [OWNER 2026-10-14, r2-F17]. Bootstrap, rotation and bounded loss/compromise recovery
  for the release key, and the exact signed release preimage and verification format, are named items of
  V1-PROFILE §14.2 (items 1 and 2). They stay operations; none becomes a bundle-verifier rule.
