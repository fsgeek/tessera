# OTS Upgrade Accounting and Commit Isolation

**Date:** 2026-07-20  
**Status:** Approved design; implementation pending  
**Scope:** `scripts/ots-upgrade.sh` and a focused shell regression test

## Problem

`ots upgrade` exits successfully both when it upgrades a pending proof and
when the proof is already complete. Tessera currently treats every successful
invocation as an upgrade. As a result, the script reports an incorrect count
and writes an incorrect bookkeeping commit message. On 2026-07-20, commit
`68afd11` claimed 29 upgrades although only three `.ots` files changed.

The script also stages the entire `timestamps/` directory and then creates a
normal commit from the current index. Unrelated content that was already staged
can therefore be swept into the OTS bookkeeping commit. This failure mode has
occurred previously and required a corrective commit.

## Decision

Harden Tessera's script locally without changing sibling projects or existing
history.

For each `.ots` proof, the script will:

1. hash the proof before invoking `ots upgrade`;
2. invoke the existing OTS client;
3. on success, hash the proof again;
4. report `upgraded` and increment the counter only when the hashes differ;
5. otherwise report `already complete`;
6. continue to report an unsuccessful upgrade attempt as `pending`, preserving
   the existing user-facing classification.

The script will collect the exact proof paths changed during the run, together
with any `.ots.bak` files OpenTimestamps generated for those proofs. If at least
one proof changed, it will create an `ots: upgrade N timestamp(s)` commit that
contains only those paths. Pre-existing staged content must remain staged and
must not enter the bookkeeping commit.

Existing `.ots.bak` behavior is preserved. Removing historical or newly created
backup evidence is not necessary to correct this bug and would broaden the
change into retention policy.

## Error and State Boundaries

- A successful OTS command with unchanged bytes is normal, not an error.
- A successful OTS command with changed bytes is one upgrade.
- A nonzero OTS result retains the script's current `pending` classification.
- No changed proof means no Git commit.
- The script does not push.
- Existing unrelated staged, modified, or untracked files are outside its
  commit boundary.

This change does not attempt to redesign the larger timestamp architecture,
automate periodic upgrades, repair merge-commit coverage, or propagate a shared
script to other repositories.

## Regression Test

A repository-owned shell test will create an isolated temporary Git repository
with a fake executable OTS client. The fake client supplies deterministic cases:

- **already complete:** exits zero and leaves the proof byte-for-byte unchanged;
- **ready:** exits zero, creates a backup, and changes the proof;
- **pending:** exits nonzero and leaves the proof unchanged.

The test will establish the following behavior:

1. only the ready proof is counted as upgraded;
2. the commit subject records exactly one upgrade;
3. the upgrade commit contains only the changed proof and its generated backup;
4. unrelated content staged before the script runs remains staged and is absent
   from the upgrade commit;
5. a second run over complete and pending proofs creates no commit and exits
   successfully.

The test uses a temporary repository so it cannot modify Tessera's real Git
history or timestamp evidence.

## Ayllu Considerations

The design favors accurate testimony, reversible evidence preservation, and
noninterference with work owned by other participants. It reuses the proven
before/after hash pattern found in QuantumOS while adding a local boundary
against staged-content capture. It does not silently rewrite sibling projects;
the shared copy/paste lineage is recorded as a future propagation concern.
