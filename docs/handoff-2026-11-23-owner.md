# Owner handoff, 2026-11-23 (Claude Opus 5.5, steward from 2026-11-19)

Start here, then `recall()` in qhaway. The repository and memory are the record; where this note disagrees, they win.
Supersedes `docs/handoff-2026-11-17-owner.md` for current state (its "how to work here" section still applies).

## First thing, Thursday 2026-11-26 (rehearsal day)
The author's sitting is today: read the diff on the Pangolin (~75 min), then the TEST rehearsal (~90 min).
Before he starts, the steward (about 30 min):
1. Run `scripts/ots-upgrade.sh`.
2. Follow `docs/releases/v1-1/REFRESH.md`: anchor heights of every COMPLETE receipt (DynamoDB `lstate = COMPLETE`;
   heights from each receipt's `layers[0].headers`), add pins, rebuild twice, regenerate the diff, update both sheets.
3. Re-verify every receipt under the new trust file as in `docs/releases/v1-1/evidence/candidate-4-all-receipts.md`
   (script pattern: a TEST wrapper around the exact trust file; fetch receipts read-only by digest name).
4. Commit, push (the sheets clone a commit from GitHub), then give the author the printable
   `docs/ceremony/release-REHEARSAL-SHEET.md` and a short list of what to bring (Pangolin, never-NUC sticks, paper
   ceremony record; YubiKey B is not needed for the rehearsal).
Still open with the author: the baseline decision (recommend: accept time-rooted `b134cdf` plus his diff reading);
the later pin cadence (proposed: with the January and February sittings); a second fingerprint channel and the
off-site copy of YubiKey B (needed before production, 27-30 Nov); "go" for the live detection tests.

## Done this tenure
- **Amendment 12 signed** by the author, 2026-11-22 (`144b9f6`, final text r6), with his statement in the commit
  message. A termination deadline as *conditional abandonment* (each invocation reading at or after L_term attempts only
  refusal; no termination time promised) and sequential successor windows (drain, then replace; acceptance fence; gap
  "normally of more than nine days"). A12.3-A12.5 deferred, not registered. Reviews: `docs/reviews/amendment-12/`.
  Its duties before the deadline is enabled: the cut in code, the TLA+ model with broken companions, D10 at L_term + 1 h.
- **Content-addressed receipts deployed** (a deployed defect: a fixed overwritable key). 7 pre-existing receipts
  migrated; live 303 to the digest key verified. `service/issuer/DEPLOY-RUN.md` 2026-11-22.
- **Detection, deployed and running** (`service/detect/infra/`, `service/watcher/`; contract
  `docs/V1-DETECTION-CONTRACT.md`, sections "D1-D4 as built" and "Deployed"):
  - G1 structured issuer logs (`service/issuer/LOGGING.md`).
  - Alarm topic `tessera-v1-alarms` -> `aws-tessera@wamason.com` (a distribution list to the author's Microsoft 365
    mailbox; the steward may read alarm mail there, read-only, to measure arrival).
  - D7 EventBridge tampering rules (readable one-line bodies), D10 Lambda errors and a $10 budget.
  - The watcher (Arariwa): D5, D6 slot 1, D7 IAM (via the trail; the org SCP closes us-east-1), D8, D9 heartbeat,
    trace records (Object Lock, 400 days). First real run re-verified all 8 receipts.
  - D1-D4 access-log alarms with an API-metric backstop; patterns tested against real and synthetic lines.
- **Release-key fingerprint channel:** the author's ORCID record (0000-0002-0651-5019), verified three ways.
  `docs/V1-RELEASE-KEY-CUSTODY-DRAFT.md`.

## In progress
- **Gate item 3, live detection tests**, written by Gemini 4 Neon (`agy --model gemini-4-neon-high`, always named
  explicitly; agy also offers Claude models) from `docs/reviews/detection-tests/BRIEF-gemini.md` r5, AWS-isolated
  (`AWS_CONFIG_FILE=/dev/null AWS_SHARED_CREDENTIALS_FILE=/dev/null AWS_PROFILE=no-such-profile`). Codex review ->
  Gemini fixes -> Codex safety confirmation (partials) -> a steward capability-removal pass (production-topic
  subscription and all IAM mutations removed; API bound to `p4e0222jof`). **Not yet run.** The live run needs the
  author's explicit go-ahead and session, and his answers on the opt-ins (quota exhaustion, throwaway CloudTrail
  trail). About 28+ of ~68 rows are NOT COVERED against production (watcher detections, GCP, D10); they keep the gate
  open and need a staging replay.

## Next, toward 4 Dec (`docs/V1-SCHEDULE.md` "What ship means")
Proposed to the author 2026-11-23 (answer pending): switch effort to the remaining ship items and publish the gate's
status honestly. 1) Verifier release candidate + per-release procedure cut to essentials + one-page sheet; rehearsal
sitting ~25-27 Nov; production release with YubiKey B ~28 Nov-1 Dec (ORCID check against paper on the sheet).
2) Service page on wamason.com (claim, V1-CONTRACT §3 limits incl. dual capture, how to call, how to verify alone).
3) The two 4 Dec tests: relying-party (a model family new to Tessera) and dead-service (clean Azure VM, AWS off).
Also: slot-2 (GCP) reconciliation for D6; notice to Yanantin of the window end (issuance stops ~2027-01-23 unless a
successor is prepared by ~2027-01-09); the deferred A12 sections in a later amendment; signer log redaction (next
signer release).

## Lessons this tenure (in qhaway)
- Promise behaviour and safety, never real-time or quantitative bounds the system cannot enforce (A12's six rounds;
  a best-effort API quota is not a ceiling).
- Review fixes that add mechanism do not converge; brief fixes as "smallest change, prefer removing capability", and
  pre-register the exit before round one. Live tests by another family are the real check.
- Do not name work as "next" without starting it in the same turn.
- Run `scripts/ots-upgrade.sh` at session start and before handoff (the author had been doing it by hand).
- Deploys generate 20+ alarm emails; warn the author first.
