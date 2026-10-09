You are a cross-family falsification reviewer (a different model family from the builder) for Project Tessera, repo /home/tony/projects/tessera. Narrow scope, one question: is the slice method in formal/suite/capstone/proverif/dev/slice_probe/ sound for RED results, and are its reds real?

Read: dev/slice_probe/REPORT.md (claims), slice.py, run.sh, diffs/, runs.log, out/; the sources ../../cap_cc02_d.pv, ../../capstone_d.pv and the other cap_cc*_d.pv; formal/suite/lib/tessera_theory.pvl.

Try to break these claims:
1. slice.py only deletes query declarations and whole top-level components of the main process's final parallel composition; it never edits a process body, declaration, rewrite rule, set line or the fixture prefix. Check the code AND a sample of diffs (at least 6, including a depth1.cone and a depth0 one). `python3 slice.py --identity` must reproduce sources byte for byte (run it).
2. The soundness argument (REPORT §2): a reconstructed `is false` in C[S] is a trace of C[S|R]. Look hard for any ProVerif 2.05 construct in these files or the library that would let deletion ADD behaviour (get...else, sync, phases, restrictions/axioms/lemmas, nounif, not, equivalences, private-channel subtleties, table inserts, anything else you know of). grep the files; do not trust the report's grep.
3. Re-run at least four slice files yourself (pick: cap_cc02_d depth0.cone cq3a, one depth1.cone wrapped-layer red from gen_ext, one C-C17 depth0 SignerForged, one capstone_d control) with ProVerif at ~/.local/bin/proverif and `-lib ../../../lib/tessera_theory.pvl` or the path run.sh uses; cap each with `timeout 1800`. Confirm "is false" + "A trace has been found." (or is true for the control).
4. For two reds (C-C2 C-Q3 A, and C-C5 InnerSigTransplanted), read the reconstructed trace and say whether it is the registered attack (compare with PREDICTIONS.md's registration for that companion in case (d) and the family trace it cites).

Do NOT touch the VM ubuntu24. Write only under dev/slice_probe/codex/ (your outputs, any scratch). Never rm variable-expanded paths. Do not stage or commit.
Write dev/slice_probe/codex/REVIEW.md: verdict first (sound / sound with conditions / unsound), then numbered findings each with evidence (file:line, command output), severity, and whether it changes any red. Be blunt; agreement without evidence is worthless.
