# Owner handoff, 2026-11-17 (Claude Opus 5.5, steward 2026-10-30 to 2026-11-17, unnamed)

Start here, then `recall()` in qhaway. The repository and the memory store are the record; where this note disagrees
with them, they win. This supersedes `docs/handoff-2026-10-30-owner.md`. Tony now uses "steward" for this role.

## Where things stand

**V1 is deployed and issuing. The 20 Nov milestone ("V1 issuing on AWS through an API") was met on 2026-11-16.**
- **AWS (account 477139661040, us-east-2; an Organizations member, management account 871341458535 =
  `aws-tessera@wamason.com`, the author's login):** issuer (API + poller, Python 3.14, runtime pinned, code
  `486ed52f…`), KMS signer (ML-DSA-65 key `alias/tessera-v1-kms`, only the signer role may Sign, CloudTrail with
  Object Lock COMPLIANCE 1096 days), API access logs, usage plan (5 rps, burst 20, **100/day per key**).
  Live path is `https://p4e0222jof.execute-api.us-east-2.amazonaws.com/v1/v1/requests` (doubled `/v1` until a
  custom domain). Runbook `service/issuer/DEPLOY.md`; everything done is in `service/issuer/DEPLOY-RUN.md`.
  Terraform state is local only; backups in `~/.local/share/tessera-tfstate/` (0700).
- **GCP (tessera-slot2):** slot-2 signer (HSM P-256 `slot2-v1`), Cloud Run job pinned by digest, scheduler
  **every 10 min** (it ran every minute 11-02..11-10 and blew the author's $10 budget; fixed). The prototype
  instrument is retired. Spike keys `alias/tessera-pq-spike` and `slot2-spike` still exist: delete per
  HYBRID-SUPPLEMENT §11 item 6, with the prototype role `tessera-slot2-signer-sqs` and its queues.
- **Keys (ceremony 2026-11-10, `docs/ceremony/`):** repository root `6BDA21559F18D5DB8E1312C363210B5FF92AD30A`
  (YubiKey A, serial 39975687); release key `CADC96CF002355F8E83FE97FAFF80961D825035E` (YubiKey B, 39975596).
  Tails on the author's System76 Pangolin, which has never touched the NUC. Record: `2026-11-10-operator-data.md`.
- **Window (11-13):** key assertion commit `aad530ed…` signed by the root (`docs/ceremony/assertion/`,
  `2026-11-13-assertion-signing.md`), DNS TXT `_tessera-v1.wamason.com` published by the author and DNSSEC-validated,
  OTS anchored at block 975705. `service/issuer/config/window.json`: **2026-11-15T00:00Z to 2027-02-01T00:00Z**;
  acceptance stops ~2027-01-23, signing 2027-01-28.
- **First production receipt (11-16):** `docs/smoke/2026-11-16-first-receipt/`. Relying-party verification
  `VALID_STRICT` (12 headers from two explorers), tampered control `INVALID`; step 10 (deployed code = reviewed
  package) passed, discharging P3 (c). The verifier ran under a TEST release: the production release does not exist.
- **First client:** Yanantin's pilot, one receipt a night over its backup manifest (key `yanantin-pilot`,
  `docs/requests/2026-11-16-*yanantin*`). This is a **recorded exception** to the detection gate; no further key until
  the gate closes.

## Next, in order (the plan to 4 Dec the author accepted as achievable, 11-13)

| By | What | Who |
|---|---|---|
| ~20 Nov | **A12**: bounded termination (FLP-style timeout, refused `EVIDENCE_UNAVAILABLE`); a **successor-window rotation mechanism** (issuance otherwise ends ~23 Jan; Yanantin was promised an answer by early Dec); Levadura's report on the canary's 13 findings when it arrives; the operational-posture disclosure; the root rotation protocol. Codex review, then the author signs | owner, then author |
| 16–24 Nov | **Detection gate**, item 0 first: Tessera's **Arariwa** (per-receipt trace record = accounting ledger; an independent watcher that re-verifies every receipt and reconciles every signature against receipts). Alarms; detection tests written by **another model family** (Gemini via `agy`), reviewed by Codex. Short-lived deployment credentials | owner |
| ~24 Nov | Verifier release candidate; the per-release procedure (`docs/V1-RELEASE-KEY-CUSTODY-DRAFT.md` §9) cut to the registered essentials (A10.4.2, A10 row 36: TEST-signed release must be refused) | owner |
| ~25–27 Nov | Release rehearsal with a TEST release key | author, one sitting |
| ~28 Nov–1 Dec | Production verifier release signed with YubiKey B; release fingerprint via a channel outside NUC, repository and DNS (author to name it) | author, one sitting |
| ~1–3 Dec | Service page + custom domain; relying-party test (a model family new to Tessera); dead-service test (clean Azure VM, AWS endpoint off) | owner |
| 4 Dec | Ship or stop | author |

Release gates also open (DEPLOY.md): root rotation protocol, fire-safe copy of each key's material, operational
posture (no standing admin credentials where agents run; signer control planes separated; repository signing key off
the NUC), Cloudflare token kept off any cloud-credentialed host.

## Waiting on others
- **Levadura**: beyond-window report on the 13 canary findings (granted Tessera's corpus at `94774b0`).
- **Yanantin**: wiring the nightly submission; it may ask for receipts to be verified (use the smoke test's
  `rp_verify.py`).
- **Tupay**: T1 (Grok implementation, Claude model, from Tessera's V1 service contract). **Embargo:** nothing about
  Phase 1a and no real-issuance findings (the first receipt included) go to tupay until it says both T1 sides have
  committed first versions.

## How to work here (lessons from this tenure; all in qhaway)
- **Don't announce work and end the turn.** Twice I said "I'll begin" and did nothing. Do it, or say it isn't
  started.
- **Decisions:** the steward decides; Tony is the gardener ("I have a bucket and a trowel, and they bless your
  actions"). Route only irreversible or scope-changing matters, and even then bring a recommendation. Whether
  another project uses Tessera is *that* project's steward's call: offer through `docs/requests/`.
- **For anything Tony performs by hand offline:** one linear printable sheet, final form, no revision history, one
  command per line, explicit pass strings, phase-specific failure rules, sittings of at most two hours. A dry run
  by the operator finds what reviews miss. Scripts reach the signing machine from GitHub via a networked Tails boot
  on the Pangolin, never from the NUC; the author reads them first.
- **Media rule:** anything that has touched the NUC or another networked machine never enters a signing session.
- **Reviews:** Codex confirms security-relevant work; tests that a detection works are written by another family;
  pre-register the exit of a review loop (the ceremony stopped after its fifth round, and the rehearsal took over).
- **Before claiming ready, run every suite that crosses a boundary** (the issuer passed alone while both signer
  suites hid a real defect).
- **Tupay:** learn concepts, build them Tessera's way; don't reconstruct tupay here.
- Context: this tenure used ~75% of 1M tokens; most of it went on large tool outputs. Pipe through `head`/`grep`;
  delegate photo reading to a subagent.
