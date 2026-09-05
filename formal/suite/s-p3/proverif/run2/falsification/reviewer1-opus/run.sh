#!/bin/bash
cd /tmp/claude-1000/-home-tony-projects-tessera/782e9de4-378f-442a-9956-988f38b4517c/scratchpad/falsify/work
LIB=${2:-tessera_theory.pvl}
echo "### $1  (lib=$LIB)"
/home/tony/.local/bin/proverif -lib "$LIB" "$1" 2>&1 | grep -E '^(RESULT|Query |Error|.*error)' | sed 's/^/    /'
