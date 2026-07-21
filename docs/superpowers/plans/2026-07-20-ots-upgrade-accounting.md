# OTS Upgrade Accounting Repair Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `scripts/ots-upgrade.sh` count only proofs whose bytes change and prevent its bookkeeping commit from capturing unrelated staged work.

**Architecture:** Keep the existing standalone Bash workflow and OTS client resolution. Add before/after SHA-256 comparison and an exact changed-path array, then commit only those proof and backup paths. Exercise the script through an isolated temporary Git repository and deterministic fake OTS executable.

**Tech Stack:** Bash, Git, `sha256sum`, OpenTimestamps CLI interface simulated by a shell fake

## Global Constraints

- Modify only `scripts/ots-upgrade.sh` and create `tests/test_ots_upgrade.sh`.
- Preserve `.ots.bak` files generated for proofs changed by OpenTimestamps.
- Do not modify sibling projects or existing timestamp history.
- Do not stage, commit, or alter concurrent P5c work or reconnect scratch files.
- The script must not push.
- The regression test must operate only in a temporary Git repository.

---

## File Map

- `scripts/ots-upgrade.sh`: classify OTS outcomes by byte change, collect exact changed paths, and create an isolated bookkeeping commit.
- `tests/test_ots_upgrade.sh`: deterministic end-to-end shell regression test using a temporary repository and fake OTS client.

### Task 1: Reproduce and Repair Upgrade Accounting

**Files:**
- Create: `tests/test_ots_upgrade.sh`
- Modify: `scripts/ots-upgrade.sh:23-39`

**Interfaces:**
- Consumes: an executable OTS client supporting `ots upgrade <proof>` with the existing exit-code behavior.
- Produces: output classifications `upgraded`, `already complete`, and `pending`; an optional path-isolated commit named `ots: upgrade N timestamp(s)`.

- [ ] **Step 1: Write the failing end-to-end regression test**

Create `tests/test_ots_upgrade.sh` with this content:

```bash
#!/bin/bash
set -euo pipefail

SOURCE_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
SCRIPT="$SOURCE_ROOT/scripts/ots-upgrade.sh"
TEST_ROOT=$(mktemp -d)
trap 'rm -rf "$TEST_ROOT"' EXIT

fail() {
    echo "FAIL: $*" >&2
    exit 1
}

assert_contains() {
    local haystack=$1
    local needle=$2
    [[ "$haystack" == *"$needle"* ]] || fail "expected output to contain: $needle"
}

cd "$TEST_ROOT"
git init -q
git config user.name "OTS Test"
git config user.email "ots-test@example.invalid"
git config commit.gpgsign false

mkdir -p .venv/bin timestamps
cat > .venv/bin/ots <<'FAKE_OTS'
#!/bin/bash
set -e

if [ "$1" != "upgrade" ]; then
    echo "unsupported fake OTS command: $1" >&2
    exit 2
fi

proof=$2
case "$(cat "$proof")" in
    complete)
        echo "Success! Timestamp complete"
        ;;
    ready)
        cp "$proof" "$proof.bak"
        printf 'complete' > "$proof"
        echo "Success! Timestamp complete"
        ;;
    pending)
        echo "Calendar proof is not ready" >&2
        exit 1
        ;;
    *)
        echo "unexpected proof fixture" >&2
        exit 2
        ;;
esac
FAKE_OTS
chmod +x .venv/bin/ots

printf 'fixture repository\n' > README.md
printf 'complete' > timestamps/complete.ots
printf 'ready' > timestamps/ready.ots
printf 'pending' > timestamps/pending.ots
git add README.md timestamps
git commit -qm "test: initial fixtures"

printf 'must remain outside the OTS commit\n' > unrelated.txt
git add unrelated.txt

output=$("$SCRIPT")

assert_contains "$output" "already complete: timestamps/complete.ots"
assert_contains "$output" "upgraded: timestamps/ready.ots"
assert_contains "$output" "pending:  timestamps/pending.ots"

subject=$(git log -1 --format=%s)
[ "$subject" = "ots: upgrade 1 timestamp(s)" ] || \
    fail "expected one-upgrade subject, got: $subject"

changed=$(git diff-tree --no-commit-id --name-only -r HEAD | sort)
expected=$(printf '%s\n' \
    timestamps/ready.ots \
    timestamps/ready.ots.bak | sort)
[ "$changed" = "$expected" ] || \
    fail "unexpected paths in upgrade commit: $changed"

staged=$(git diff --cached --name-only)
[ "$staged" = "unrelated.txt" ] || \
    fail "unrelated staged content was not preserved: $staged"

head_before=$(git rev-parse HEAD)
second_output=$("$SCRIPT")
head_after=$(git rev-parse HEAD)

[ "$head_before" = "$head_after" ] || \
    fail "a no-change run created a commit"
assert_contains "$second_output" "No timestamps ready to upgrade yet."

echo "PASS: OTS upgrade accounting and commit isolation"
```

- [ ] **Step 2: Run the test and verify the existing script fails**

Run:

```bash
bash tests/test_ots_upgrade.sh
```

Expected: nonzero exit with a message like:

```text
FAIL: expected output to contain: already complete: timestamps/complete.ots
```

The existing script calls the unchanged proof `upgraded` and counts it.

- [ ] **Step 3: Implement byte-change accounting and exact-path commit isolation**

Replace the loop and commit block in `scripts/ots-upgrade.sh` with:

```bash
upgraded=0
changed_paths=()
for f in timestamps/*.ots; do
    [ -f "$f" ] || continue
    original_hash=$(sha256sum "$f" | cut -d' ' -f1)
    if "${OTS[@]}" upgrade "$f" 2>/dev/null; then
        upgraded_hash=$(sha256sum "$f" | cut -d' ' -f1)
        if [ "$original_hash" != "$upgraded_hash" ]; then
            echo "upgraded: $f"
            upgraded=$((upgraded + 1))
            changed_paths+=("$f")
            if [ -f "$f.bak" ]; then
                changed_paths+=("$f.bak")
            fi
        else
            echo "already complete: $f"
        fi
    else
        echo "pending:  $f"
    fi
done

if [ "$upgraded" -gt 0 ]; then
    git add -- "${changed_paths[@]}"
    git commit --only --no-verify \
        -m "ots: upgrade $upgraded timestamp(s)" -- "${changed_paths[@]}"
else
    echo "No timestamps ready to upgrade yet."
fi
```

- [ ] **Step 4: Run the focused regression test and verify it passes**

Run:

```bash
bash tests/test_ots_upgrade.sh
```

Expected:

```text
PASS: OTS upgrade accounting and commit isolation
```

- [ ] **Step 5: Run static and repository-safety checks**

Run:

```bash
bash -n scripts/ots-upgrade.sh tests/test_ots_upgrade.sh
git diff --check -- scripts/ots-upgrade.sh tests/test_ots_upgrade.sh
git diff --cached --name-only
```

Expected: both Bash files parse, no whitespace errors, and no unrelated path is staged.

- [ ] **Step 6: Commit only the implementation and test**

Run:

```bash
git add -- scripts/ots-upgrade.sh tests/test_ots_upgrade.sh
git commit --only -m "fix: count only changed OTS proofs" -- \
    scripts/ots-upgrade.sh tests/test_ots_upgrade.sh
```

Expected: one signed implementation commit followed by the repository's automatic OTS bookkeeping commit. Concurrent formal work and reconnect scripts remain outside both commits.

- [ ] **Step 7: Verify the committed result from a clean temporary fixture**

Run:

```bash
bash tests/test_ots_upgrade.sh
git show --stat --oneline HEAD~1
git status --short
```

Expected: the regression test passes; the implementation commit contains only the script and test; pre-existing concurrent work remains present but unstaged.
