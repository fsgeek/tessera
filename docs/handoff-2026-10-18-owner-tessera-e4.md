# Handoff from the owner instance tessera-e4 (Claude Opus 5.5), 2026-10-18

For the next owner instance. Read this first, then `recall()` in qhaway. The repository and the memory store are the
record; if this note disagrees with them, they win.

## Where V1 stands

- **A9 is SIGNED** (`2ad3489`, 2026-10-16). It defines the V1 claim, profile and gate.
- **The hybrid branch is REGISTERED** (2026-10-16, A9.6): pair `KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256`
  - Slot kms: AWS KMS ML-DSA-65, account 477139661040, us-east-2.
  - Slot gpg: GCP Cloud KMS HSM P-256, project tessera-slot2, us-east1. It is reached only through the policy signer
    (Cloud Run job `slot2-signer`; the scheduler is PAUSED).
  - Records: `formal/p8/HYBRID-SUPPLEMENT.md` and `formal/p8/HYBRID-REGISTRATION-RECORD.md`.
- **A10 is PROPOSED** (`docs/phase-0-prereg-amendment-10.md`, 36 rows). It is waiting for **Tony's three rulings in
  his own words**:
  1. the conditional UTC assessment under A-UTC;
  2. A04 option (e), the service-key listing (protection against key substitution);
  3. the release-custody gate at the first public verifier release.

  Owner and Codex recommend adopting all three. Tony relays Codex advice without comment **on purpose**. That relay
  is not his ruling. When he rules: enter his words verbatim as AUTHOR DECISIONs, check each one against the text,
  then give him the A10 signing commit. Commit 1 (everything else) is listed in the last chat message of tessera-e4.
- **Evidence:** the independent verifier (Codex, `prototype/indep-verifier`) and the conformance suite
  (`prototype/conformance`, 342 cases) agree on 342/342 (`prototype/differential/results-run5.json`). Mutation
  testing: 253,363 mutants, 0 false accepts (`prototype/mutation/REPORT.md`).
- **Plain-language work** (at Tony's request, ASD-STE100-inspired): `docs/plain/STE-STYLE.md` and
  `docs/plain/A9-PLAIN-PILOT.md`. After A10 is signed, write ONE current V1 service description in that style
  (Codex point 5). The 4 Dec relying-party documentation is the main STE deliverable.

## Before the 30 Oct freeze (owner work)

- After the A10 rulings: implement the service-key listing and the `utc_assessment` wrapper in the profile and both
  verifiers, and add conformance cases (the memo estimates 4–5 days). Reconcile profile §5, §14.2 items 1–2 and
  runbook §6 with the bootstrap-record split.
- Freeze the release FORMAT: archive, signature format, trust-file hash binding.
- The trust-configuration values: KSK sources archived; KSK-2017 start date sourced.
- The frozen spec object and catalog; re-cite the stale profile line numbers in about 281 conformance cases.
- Dependency manifest: pinned editions; libraries unfit as references (python-opentimestamps rejects depth-256
  proofs; dilithium-py accepts duplicate hint indices); SHA-1DC pinned (`prototype/vendor/SHA1DC-PIN.md`).
- HSM monoculture check: GCP attests Marvell/Cavium. Find out what is under AWS KMS.

## Before the first public verifier release (Nov, gate)

- Custody procedure `docs/V1-RELEASE-KEY-CUSTODY-DRAFT.md`, reviewed twice. Still open:
  - R3-01 HIGH: bind the reviewed build to the signed archive;
  - R3-03: bootstrap step 3;
  - R3-04/05: stale note and style;
  - the owner-level "(Author: …)" choices.
- Tony's machine is the System76 laptop: live-boot signing, review VM with snapshots, no SSH path from the NUC.
  YubiKey 5s arrive 2026-10-20. Rehearse with a throwaway key, including the TEST-signature refusal case.

## Waiting on others

- **Levadura:** contradiction search request (`docs/requests/2026-10-16-…`).
- **Authority project:** reply written (`docs/requests/2026-10-18-…`), for Tony to carry.

## Working lessons from this instance (also in qhaway)

- Backgrounded `codex exec` needs `< /dev/null` and should be launched as a tracked task, with `-c
  model_reasoning_effort=high` for reviews. Codex runs as gpt-6.1-sol. Check the log header.
- Check for concurrent sessions at startup (ListAgents, `ps`, the PID-to-transcript map) before acting on unexplained
  tree changes.
- A claim with no run behind it is a prediction; label it (the lesson of Tukuq's stone, "Round Two of Eighteen").
- Document-only review rounds converge slowly. Construction finds holes faster: spike, differential, mutation,
  plain-language rendering. The plain-language rendering found an A9 overclaim that 18 review rounds missed.
- Amendments grow under review (A10 went from short to 32 pages). Give Tony a plain summary to read, and keep the
  record for reviewers.
