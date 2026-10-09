#!/usr/bin/env python3
"""Development helper (scratch): injects the generated tables into RESULTS.md at
   its <!--RESULTS-TABLES--> marker.  Transcription only.

   SUPERSEDED 2026-10-01 (capstone builder): this script and mkresults.py/summarize.py produced the
   ladder-1 interim tables and are kept unedited below this note as that record.  Do NOT run it
   against the current RESULTS.md: the markers it writes were replaced, its needles miss the C-C15
   files (variable renumbering under recut R-6), and its EXPECTED ignores the Cases cells.  Ladder 2
   is assembled by dev/assemble_l2.py, which says why in its header."""
import sys as _s; _s.exit("superseded 2026-10-01: use dev/assemble_l2.py")
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.abspath(os.path.join(HERE, "..", "..", "RESULTS.md"))
r = subprocess.run([sys.executable, os.path.join(HERE, "mkresults.py")],
                   capture_output=True, text=True)
tables = r.stdout
sys.stderr.write(r.stderr)
body = ("## 1. Every registered query, by case\n\n"
        "Registered prediction as PREDICTIONS.md states it, with its line; observed as the `.out`\n"
        "line and ProVerif's verdict; outcome in the registered three-outcome vocabulary\n"
        "(violation / timeout / termination) and which registered branch fired.  A cell reading\n"
        "*not run* is a run that has not landed; a cell reading *not declared in this case* is a\n"
        "query the registration does not state for that case.\n\n")
parts = tables.split("\n| Companion / configuration |")
q = parts[0]
rest = parts[1] if len(parts) > 1 else ""
comp, matrix = (rest.split("\n| Row |") + [""])[:2]
out = body + q
if rest:
    out += ("\n\n## 2. Every companion, by case\n\n"
            "Set (1) is the registered expected failed set, in this model's query keys.  "
            "*red as required* = every registered member fired; *did not go red* = one did not; "
            "*control green as required* = the configuration is an isolation control whose "
            "registered outcome is all green.\n\n| Companion / configuration |" + comp)
if matrix:
    out += ("\n\n## 3. The discharge matrix, as run\n\n"
            "D1-D11 are §2(a)'s eleven cross-model rows; D12 and D13 are §2(c)'s standing-verdict "
            "rows, outside the matrix and outside its count.  **Nothing below is discharged by this "
            "file**: the commit is the author's and the non-author cross-family review is still "
            "owed.\n\n| Row |" + matrix)
s = open(RES).read()
A, B = "<!--RESULTS-TABLES-->", "<!--END-RESULTS-TABLES-->"
i, j = s.index(A), s.index(B)
s = s[:i] + A + "\n" + out + "\n" + s[j:]

# the not-run list
import glob
logged = set()
for ln in open(os.path.join(HERE, "..", "ladder.log")):
    if " rc=" in ln:
        logged.add(ln.split()[0])
allf = sorted(set(os.path.basename(f)[:-3] for f in
              glob.glob(os.path.join(HERE, "..", "cap*.pv")) +
              glob.glob(os.path.join(HERE, "..", "capstone*.pv"))))
done = [f for f in allf if f in logged]
todo = [f for f in allf if f not in logged]
nl = ("**Landed (%d of %d):** %s\n\n**Outstanding (%d of %d), marked *not run* in every table above:** %s"
      % (len(done), len(allf), ", ".join("`%s`" % f for f in done) or "none",
         len(todo), len(allf), ", ".join("`%s`" % f for f in todo) or "none"))
C, D = "<!--NOTRUNLIST-->", "<!--END-NOTRUNLIST-->"
i2, j2 = s.index(C), s.index(D)
s = s[:i2] + C + "\n" + nl + "\n" + s[j2:]

# the whole-ladder ceiling accounting (§3: at most 4 x 1185 = 4740 min)
tot = 0; landed = 0; killed = 0; kseconds = 0
for ln in open(os.path.join(HERE, "..", "ladder.log")):
    if ln.startswith("#") or " rc=" not in ln:
        continue
    d = dict(x.split("=", 1) for x in ln.split()[1:] if "=" in x)
    sec = int(d.get("seconds", "0"))
    tot += sec
    if d.get("rc") in ("137", "143"):
        killed += 1; kseconds += sec
    else:
        landed += 1
CEIL = 4740 * 60
verdict = ("**within the ceiling**" if tot <= CEIL else
           "**EXCEEDS THE CEILING by %d s (%.1f min)**" % (tot - CEIL, (tot - CEIL) / 60.0))
cl = ("**Accounted so far: %d s of solver time against the %d s (4740 min) ceiling -- %.2f%%, %s.** "
      "Of that, %d s over %d run(s) that LANDED and %d s over %d run(s) that were KILLED and produce "
      "no result (their rc=137/143 lines stay in ladder.log as history and each file is rerun)."
      % (tot, CEIL, 100.0 * tot / CEIL, verdict, tot - kseconds, landed, kseconds, killed))
E, F = "<!--CEILING-->", "<!--END-CEILING-->"
i3, j3 = s.index(E), s.index(F)
s = s[:i3] + E + "\n" + cl + "\n" + s[j3:]
open(RES, "w").write(s)
print("RESULTS.md tables written")
