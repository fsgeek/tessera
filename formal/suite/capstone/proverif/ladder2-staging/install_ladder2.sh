#!/usr/bin/env bash
# Owner instance, 2026-09-24. Runs on wam-nuc AFTER the VM's last ladder-1 runs
# have logged. Steps: (1) pull the VM's final ladder-1 state over this copy;
# (2) archive ladder 1 under proverif/ladder1/; (3) install the staged ladder-2
# files; (4) push to the VM; (5) launch guard + runner there with a fresh log.
set -euo pipefail
cd "$(dirname "$0")/.."            # proverif/
VM=ubuntu24; R='~/tessera-ladder/formal/suite/capstone/proverif'
# (pgrep -c exits 1 when the count is 0, which pipefail would read as a failure; hence the || true)
[ "$(ssh -o BatchMode=yes $VM "pgrep -c -x proverif || true")" = 0 ] || { echo "VM still has proverif running; abort"; exit 1; }
[ "$(ssh -o BatchMode=yes $VM "pgrep -c -f '^bash run_ladder\.sh\$' || true")" = 0 ] || { echo "VM runner still alive; abort"; exit 1; }
# (1) VM -> here (results copy wins for ladder-1 artifacts), excluding local-only dirs
rsync -a --exclude 'dev/' --exclude 'ladder2-staging/' --exclude 'ladder1/' $VM:$R/ ./
rsync -a $VM:$R/ /home/tony/tessera-ladder-vm-backup/proverif/
# (2) archive ladder 1
mkdir -p ladder1
mv ladder.log ladder1/ ; mv *.out ladder1/ ; mv *.rss ladder1/ 2>/dev/null || true
for f in mem_guard.log mem_guard_all.log mem_guard_vm.log ladder.launch.log ladder.launch.vm.log; do [ -f "$f" ] && mv "$f" ladder1/; done
cp owner_interventions.log ladder1/owner_interventions.as-of-ladder1.log
ls *.mechfail 2>/dev/null && { echo "mechfail files present; abort"; exit 1; }
cat > ladder1/README.md <<'EOT'
# Ladder 1 — capstone.pv blob c6969b4cc2f2e30be7a7a950af7609ea75e4c700 — ARCHIVED 2026-09-24
Every run of the ladder under the original model text, on wam-nuc (31 GB) 2026-09-19/20 and on ubuntu24 (Hyper-V, dynamic 96 GB) 2026-09-20/24, exactly as logged; nothing here is edited after the archive. `ladder.log` is the record; `*.out` are the ProVerif outputs; the guard and launch logs show every scheduling intervention. Ladder 2 (the uniform recut `set selFun = Term.`, blob a9fb7da1…) runs in the parent directory with a fresh log; every file that landed here must reproduce its RESULT lines there (the cross-check RESULTS.md reports).
EOT
# (3) install ladder 2
cp ladder2-staging/capstone.pv ./capstone.pv
for f in ladder2-staging/cap*.pv; do cp "$f" ./; done
cmp ladder2-staging/derive.py derive.py
cmp ladder2-staging/run_ladder.sh run_ladder.sh
[ "$(git hash-object capstone.pv)" = a9fb7da1e4851120677b21dea4a8c98a481ad43a ] || { echo "blob mismatch"; exit 1; }
: > ladder.log
echo "# LADDER 2 $(date -u +%FT%TZ): uniform recut, capstone.pv blob $(git hash-object capstone.pv) (set selFun = Term.), every file re-derived by derive.py; ladder 1 archived in ladder1/; JOBS=3" >> ladder.log
echo "$(date -u +%FT%TZ) owner instance: ladder 1 archived to ladder1/, ladder 2 installed (blob a9fb7da1) and launched on ubuntu24 with JOBS=3" >> owner_interventions.log
# (4) here -> VM (delete VM-side files not present here, within the dir, excluding dev/)
rsync -a --delete --exclude 'dev/' --exclude 'ladder2-staging/' ./ $VM:$R/
# (5) launch
ssh -o BatchMode=yes $VM "cd $R && (setsid nohup bash mem_guard_vm.sh >/dev/null 2>&1 < /dev/null &) && (PATH=\$HOME/.local/bin:\$PATH JOBS=3 setsid nohup bash run_ladder.sh > ladder.launch.vm.log 2>&1 < /dev/null &) && sleep 30 && ps -C proverif -o args= | awk '{print \$NF}' && tail -2 ladder.log"
echo INSTALLED
