#!/bin/bash
# Upgrade pending OpenTimestamps proofs (the WHEN layer, part 2).
#
# `ots stamp` returns immediately with an INCOMPLETE proof (a commitment held
# by calendar servers). A few hours later, once the commitment is anchored in
# a Bitcoin block, `ots upgrade` rewrites the .ots file with the full proof
# path to the blockchain. Run this periodically after committing.
set -e

GIT_ROOT=$(git rev-parse --show-toplevel)
cd "$GIT_ROOT"

# Resolve ots the same way the post-commit hook does (venv first, uv fallback).
if [ -x "$GIT_ROOT/.venv/bin/ots" ]; then
    OTS=("$GIT_ROOT/.venv/bin/ots")
elif command -v uv >/dev/null 2>&1 && uv run --quiet ots --version >/dev/null 2>&1; then
    OTS=(uv run --quiet ots)
else
    echo "FATAL: ots client not found. Run: uv sync" >&2
    exit 1
fi

upgraded=0
for f in timestamps/*.ots; do
    [ -f "$f" ] || continue
    if "${OTS[@]}" upgrade "$f" 2>/dev/null; then
        echo "upgraded: $f"
        upgraded=$((upgraded + 1))
    else
        echo "pending:  $f"
    fi
done

if [ "$upgraded" -gt 0 ]; then
    git add timestamps/
    git commit --no-verify -m "ots: upgrade $upgraded timestamp(s)"
else
    echo "No timestamps ready to upgrade yet (Bitcoin anchoring takes a few hours)."
fi
