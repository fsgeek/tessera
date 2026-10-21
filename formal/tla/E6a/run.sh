#!/bin/bash
# E6a run harness (STATUS: PROPOSED, 2026-10-19, AI collaborator).
# Re-runnable: regenerates runs/ from the committed modules and cfgs.
# TLC: ~/.local/lib/tla2tools.jar (2026.07.31), -workers 1 (deterministic
# first violation). P4_VerifierStates.tla is found through TLA-Library and is
# not copied or edited.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
TLA_DIR="$(cd "$HERE/.." && pwd)"
JAR="${TLA2TOOLS:-$HOME/.local/lib/tla2tools.jar}"
META="$(mktemp -d "${TMPDIR:-/tmp}/e6a-meta.XXXXXX")"
RUNS="$HERE/runs"
mkdir -p "$RUNS/main" "$RUNS/sanity" "$RUNS/broken" "$RUNS/matrix" "$RUNS/p4-rerun" "$RUNS/cfg"
cd "$HERE" || exit 1

tlc() { # tlc <out> <cfg> <module> [extra...]
  local out=$1 cfg=$2 mod=$3; shift 3
  java -XX:+UseParallelGC -DTLA-Library="$TLA_DIR" -cp "$JAR" tlc2.TLC \
    -workers 1 -noGenerateSpecTE -metadir "$(mktemp -d "$META/m.XXXXXX")" "$@" \
    -config "$cfg" "$mod.tla" > "$out" 2>&1
}
summ() { # one line: result | invariant | distinct states
  local f=$1 r inv st
  # Violations are checked first: under -continue TLC also prints "No error has been found".
  if grep -q "Invariant .* is violated" "$f"; then r=RED
    inv=$(grep -o "Invariant [A-Za-z0-9_]* is violated" "$f" | awk '{print $2}' | sort -u | paste -sd, -)
  elif grep -q "Model checking completed. No error has been found." "$f"; then r=GREEN; inv=-
  else r=ERROR; inv=-; fi
  st=$(grep -o "[0-9]* distinct states" "$f" | tail -1)
  echo "$r|$inv|${st:-n/a}"
}

INVS=$(awk '/^INVARIANTS/{f=1;next} f&&NF{print $1}' E6a_V1.cfg)
WITS="NeverInStrict NeverInDegraded NeverInInvalid NeverOutOfProfile NeverAlgUnknown NeverUnknownOpaqueBadSig NeverMixedFailedUnknown NeverUnknownEmptySig NeverMissingSignature NeverMemberMissing NeverMissingEvPlusUnknown NeverDefectPlusMissingEv NeverWaivedAbsentDegraded"
BROKEN="E6a_Broken_FailOpen E6a_Broken_MalformedAsUnknown E6a_Broken_MissingSigAsEvidence E6a_Broken_MissingEvidenceAsFail E6a_Broken_UnknownDominates E6a_Broken_UnknownAsOutOfProfile E6a_Broken_DispatchFallthrough"

mkcfg() { # mkcfg <out> <inst V1|General> <invariant...>
  local out=$1 inst=$2; shift 2
  { awk '/^CONSTANTS/{f=1} /^INVARIANTS/{exit} f' "E6a_$inst.cfg"; echo "INVARIANTS"
    for i in "$@"; do echo "  $i"; done; } > "$out"
}

SUMMARY="$RUNS/SUMMARY.tsv"
echo -e "run\tmodule\tinstance\tinvariants\tresult\tred_on\tstates" > "$SUMMARY"
rec() { local s; s=$(summ "$5" | tr "|" "\t"); printf "%s\t%s\t%s\t%s\t%s\n" "$1" "$2" "$3" "$4" "$s" >> "$SUMMARY"; }

for inst in V1 General; do
  # 1. Main: correct module, all invariants. Must be GREEN.
  tlc "$RUNS/main/E6a_AlgVerdict_$inst.out" "E6a_$inst.cfg" E6a_AlgVerdict
  rec main E6a_AlgVerdict "$inst" ALL "$RUNS/main/E6a_AlgVerdict_$inst.out"
  # 2. Sanity witnesses, one run each. Healthy = RED (reachable).
  for w in $WITS; do
    mkcfg "$RUNS/cfg/sanity_${w}_$inst.cfg" "$inst" "$w"
    tlc "$RUNS/sanity/${w}_$inst.out" "$RUNS/cfg/sanity_${w}_$inst.cfg" E6a_AlgVerdict
    rec sanity E6a_AlgVerdict "$inst" "$w" "$RUNS/sanity/${w}_$inst.out"
  done
  # 3. Broken companions: all-invariants run (first violation), then one run
  #    per invariant (the exact red/green matrix).
  for b in $BROKEN; do
    tlc "$RUNS/broken/${b}_$inst.out" "E6a_$inst.cfg" "$b"
    rec broken-all "$b" "$inst" ALL "$RUNS/broken/${b}_$inst.out"
    log="$RUNS/matrix/${b}_$inst.log"; : > "$log"
    for i in $INVS; do
      mkcfg "$META/c_${b}_${i}_$inst.cfg" "$inst" "$i"
      tlc "$META/o.out" "$META/c_${b}_${i}_$inst.cfg" "$b"
      { echo "===== $b / $inst / $i"; cat "$META/o.out"; } >> "$log"
      rec matrix "$b" "$inst" "$i" "$META/o.out"
    done
  done
done

# 4. P4 regression: the committed P4 cfgs, unchanged, re-run into runs/p4-rerun.
cd "$TLA_DIR" || exit 1
tlc "$RUNS/p4-rerun/P4_VerifierStates.out" P4_VerifierStates.cfg P4_VerifierStates
rec p4-rerun P4_VerifierStates - main "$RUNS/p4-rerun/P4_VerifierStates.out"
tlc "$RUNS/p4-rerun/P4_VerifierStates_Sanity.out" P4_VerifierStates_Sanity.cfg P4_VerifierStates -continue
rec p4-rerun P4_VerifierStates - sanity "$RUNS/p4-rerun/P4_VerifierStates_Sanity.out"
for c in P4_VerifierStates_Broken P4_VerifierStates_Broken_Green P4_VerifierStates_Broken_Green2; do
  tlc "$RUNS/p4-rerun/$c.out" "$c.cfg" P4_VerifierStates_Broken
  rec p4-rerun P4_VerifierStates_Broken - "$c" "$RUNS/p4-rerun/$c.out"
done
echo "done: $SUMMARY (metadirs left in $META)"
