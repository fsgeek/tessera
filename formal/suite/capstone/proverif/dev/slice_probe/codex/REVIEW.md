**Verdict: sound with conditions. The audited slices preserve RED results, and the three independently rerun reds are real symbolic attacks.** No counterexample to trace inclusion was found in the current sources or library. C-C2 C-Q3 A and C-C5 InnerSigTransplanted instantiate their registered case-(d) failure mechanisms. This is not approval to count exploratory runs as registered discharge, and not a validation of arbitrary future inputs to this regex slicer.

Review: Codex, 2026-10-05, independent of the Claude builder. Scope: deletion soundness, saved-artifact integrity, four reruns, and two registration/trace comparisons. Paths below are relative to `formal/suite/capstone/proverif/dev/slice_probe/` unless stated otherwise. Source/binary SHA-256 values and repository HEAD are in `codex/provenance.txt:1-34`. Writes were confined to `codex/`; no VM access, staging, or commits.

1. **The current 93 artifacts satisfy the deletion contract. Severity: informational; changes any red: no.**

   Read `slice.py`, including query replacement at lines 114-127 and process filtering/reassembly at 129-137. Queries are replaced with comments; the final parallel block is reformatted and components removed. Generated banners are also added (150-153). Thus “only deletes” is semantically accurate, not literally a byte-diff description. No process body, declaration, destructor, setting, or fixture-prefix statement is changed in the saved artifacts.

   I ran `python3 slice.py --identity SOURCE` for **all 25** matching source files (24 `cap_cc*_d.pv` plus `capstone_d.pv`): all OK (`codex/audit.txt:1-25`). I also checked that text-mode reading does not normalize any source bytes here. `python3 codex/audit.py` regenerated all **48 gen + 45 gen_ext** files, including their banners, byte-identically. Its separate component check establishes that each retained component is an unchanged, ordered member of the source's final composition, and that every source component there is replicated. Output: `codex/audit.txt:104-197`, ending `ALL PASSED 25 sources; 93 slices expected`.

   A second check, `python3 codex/exact-prefix.py`, compares the original prefix after replacing only absent query declarations, byte for byte, against each generated file. Output `codex/exact-prefix.txt:94`: `TOTAL 93; every byte outside query removals and final parallel block preserved`. This includes the complete process definitions and main fixture prefix, not just selected lines.

   Six manually inspected diffs, with their load-bearing process hunks:

   | Diff | Evidence and observation |
   |---|---|
   | `diffs/cap_cc02_d__depth0.cone__cq3a.diff:162-188` | Keeps Attester, Front, AttestStage, SP3Judge; deletes whole components. |
   | `diffs/cap_cc02_d__depth0__cq3a.diff:162-228` | All honest producers retained; only both WrapStage and both SUnwrap calls deleted; other changes are layout. |
   | `diffs/cap_cc05_d__depth1.cone__cq4s.diff:162-190` | Retains L0-to-L1 WrapStage/SUnwrap, Attester, Front, AttestStage, SigJudge. |
   | `diffs/cap_cc04_d__depth1.cone__link6b.diff:160-188` | Same depth boundary, Link6bJudge retained; no wrapper body edited. |
   | `diffs/cap_cc17_d__depth0__sf.diff:164-230` | Honest producers/member reports retained; only four wrapper-stage calls removed. |
   | `diffs/capstone_d__depth0.attOnly__a46.diff:161-222` | Removes the named honest-producer families and four wrapper-stage calls, without changing their definitions. |

   In each, preceding substantive hunks delete query declarations only. I additionally recomputed all 91 saved diffs using `diff SOURCE GENERATED`, excluding the saved diff's exploratory banner: all match (`codex/diff-audit.txt:1-92`). There are 93 generated paths; two filenames occur in both gen and gen_ext.

2. **The trace embedding holds for these files, including private channels and correspondence reds. Severity: informational; changes any red: no.**

   The precise claim is about **finite execution prefixes** and unchanged queries: replay the fixture prefix, then replay each slice reduction using exactly the same retained processes and attacker recipes, with all deleted components unscheduled. Fresh names can be alpha-renamed consistently. The global declarations, public/private status, and term-reduction rules are unchanged. Hence the same event history and attacker knowledge are available in this chosen full-model execution. An additional process being *available* does not require it to execute.

   This matters for `A ==> B`: deleting a producer of B might look suspicious, but it does not create a false attack here. If the slice reaches A without an earlier matching B, the full model can reproduce that exact prefix with the extra B-producing components idle. B is still absent. The claim is not that every full-model scheduling reproduces the attack, or that maximal executions have identical behavior.

   Independent searches: raw `rg` over all 25 sources and the library is saved in `codex/raw-construct-grep.txt`; the comment-aware scan and exact else locations are in `codex/audit.py:30-39` and `codex/audit.txt:26-103`. **No executable** get, insert, table, sync, phase, restriction, axiom, lemma, nounif, not assumption, equivalence, noninterf, weaksecret, choice/diff, barrier, elimtrue, pred, or clauses construct was found. The only set directive in each model is `set selFun = Term.`; the library has none. There are real else branches, but they test terms/patterns, not missing messages or global state. For example, `../../cap_cc02_d.pv:822-844` branches on terminal and disposition terms; `:948-951` branches on a frame pattern. `lookup2`'s ordered reductions (`:816-820`) and the library's ordered signature/DSKS reductions (`../../../../lib/tessera_theory.pvl:111-115`) are untouched.

   Private-channel competition does not break this argument. Front forks outputs and replicated material reports (`../../cap_cc02_d.pv:569-578`). AttestStage and WrapStage can compete for stageCh, while StandingPath and SUnwrap can compete for sStageCh. Choose the same rendezvous as the slice and leave the competing reader idle. No input has a timeout/absence branch. Removing a receiver can block an output; it cannot turn that blockage into a new successful continuation. Judges also consume concrete reports, not evidence that another judge failed to run (`../../cap_cc05_d.pv:991-998,1048-1052`). Replication of every final component is verified; replication of every internal subprocess is neither true nor needed for this proof.

   The conditions are unchanged semantics/query, ordinary finite-trace reachability/correspondence, and successful trace reconstruction. A Horn-clause derivation or `cannot be proved` alone would not suffice. This distinction agrees with the [official ProVerif result documentation](https://bblanche.gitlabpages.inria.fr/proverif/usage.html): `false` includes a reconstructed protocol attack, whereas an unsuccessful reconstruction leaves `cannot be proved`. The installed binary identifies itself as ProVerif 2.05 (`codex/log-audit.txt:93`).

3. **Four independent executions reproduce the saved results exactly. Severity: informational; changes any red: no.**

   Each command was `timeout 1800 /home/tony/.local/bin/proverif -lib ../../../../lib/tessera_theory.pvl FILE`, from the slice_probe directory, with stdout/stderr redirected into `codex/`. This is run.sh's library path (`run.sh:6`); I did not run its output-writing harness. Commands, return codes, and elapsed seconds are recorded in `codex/reruns.jsonl:1-4`.

   | FILE | Seconds / rc | Independent output |
   |---|---|---|
   | `gen/cap_cc02_d__depth0.cone__cq3a.pv` | 30.76 / 0 | `codex/cap_cc02_d__depth0.cone__cq3a.out:958-959`: `A trace has been found.`; `RESULT not event(ReattributedA(kX_1,kH_1,fb_1)) is false.` |
   | `gen_ext/cap_cc05_d__depth1.cone__cq4s.pv` | 41.99 / 0 | `codex/cap_cc05_d__depth1.cone__cq4s.out:1375-1376`: trace found; `RESULT not event(InnerSigTransplanted(kX,s)) is false.` |
   | `gen_ext/cap_cc17_d__depth0__sf.pv` | 10.68 / 0 | `codex/cap_cc17_d__depth0__sf.out:2211-2212`: trace found; `RESULT not event(SignerForged(t_7,k_1)) is false.` |
   | `gen_ext/capstone_d__depth1.cone__cq4s.pv` | 3.30 / 0 | `codex/capstone_d__depth1.cone__cq4s.out:826`: `RESULT not event(InnerSigTransplanted(kX,s)) is true.` |

   All four complete outputs are byte-identical to their saved `out/` counterparts after removal of the builder's prepended banner (`codex/log-audit.txt:89-92`). Independently checked every runs.log input blob against the generated files, every saved RESULT against out/, and every traceFound count: **87 records, 52 false, 33 true, 2 without results** (`codex/log-audit.txt:1-88`). The two no-result records are the recorded 7200-second timeouts (`runs.log:94-95`), not reds. This verifies the other logged reds as saved reconstructed results; it does not mean I independently reran or mechanistically reviewed all 52.

4. **C-C2 C-Q3 A is the registered reattribution attack. Severity: informational; changes any red: no.**

   Registration: `../../../PREDICTIONS.md:1771`, C-C2, case (d), cites `formal/suite/ledger-tests-2026-09-14/m4_framepin_mh.out:620` and explicitly corrects the earlier claim that its trace used the honest tuple. The family trace at lines 600-616 signs an honest frame under skB2, then forges authority evidence for a changed, attacker-key tuple and re-signs the unchanged frame under that key. It uses no DSKS step.

   The independent slice trace does the same at two-signer width. `codex/cap_cc02_d__depth0.cone__cq3a.out:913` leaks skS; `:917-923` produces the honest skB2 frame/signature. At `:925`, the attack uses keys a_2 and a_5, a new manifest naming both, possession signatures over that manifest, and authority evidence signed with leaked skS. Slot A carries the honest frame's exact bytes, now signed under a_2; slot B carries compatible type/version/payload. The honest frame still names fp(pk(skB2)) and h(M2). At `:935-943`, both slots and AcceptanceComplete occur at L0; `:951-955` pairs the genuine honest report with the slot-A acceptance and fires ReattributedA(pk(a_2), pk(skB2), fbHon).

   The mutation is visible at `../../cap_cc02_d.pv:643-656`: two-signer frame key/hash checks are relaxed while signature-byte checks remain. Thus this is existing-byte reattribution through a changed evidenced tuple, not signature-term transplantation, stolen skB2, or a DSKS artifact. The family run's accepting branch is one-signer; the capstone trace is its registered two-signer adaptation, not an identical transcript.

   The report's separate link-5 qualification remains necessary (`REPORT.md:38-39`): Link5Judge combines fingerprint and hash constraints (`../../cap_cc02_d.pv:948-951`). A generic link-5 red alone does not isolate which conjunct failed. The inspected C-Q3-A trace itself has a concrete wrong-key frame attribution; that does not retroactively make the separate link-5 output a conjunct-specific result.

5. **C-C5 is the registered DSKS/byte-unbinding mechanism, with a different wrapper producer. Severity: informational; changes any red: no.**

   Registration: `../../../PREDICTIONS.md:1774`, C-C5 case (d), cites `formal/suite/ledger-tests-2026-09-14/s1_sig_unbound.out:897`; the query is defined at `../../../PREDICTIONS.md:620-629` as accepting an honest inner signature term under another key, at wrapped depth. It does not require an honest wrapper signer.

   In the independent trace, let sH be the honest skB2 signature at `codex/cap_cc05_d__depth1.cone__cq4s.out:1320`, and kD = dsks(sH,a_11). At `:1332`, the attacker constructs a **different inner frame** pinned to pk(kD) and a manifest for that key, makes its possession proof with kD, and forges the manifest evidence with leaked skS (`:1310`). The original signature sH accompanies this new frame unchanged. An attacker-held outer key a_5 signs a correctly formed wrapper containing that pair. WrapStage accepts L0 (`:1342`) and forwards it with wctx to L1 (`:1352`); AttestStage accepts the inner pair at L1 (`:1358`). The honestSigCh/sigCh rendezvous at `:1368-1370` matches exactly sH, and SigJudge fires InnerSigTransplanted(pk(kD),sH) at `:1372`.

   Why it works: the library's DSKS rule verifies sH under pk(kD) but still returns the **original** signed bytes. C-C5's `let (=BYTES, anybA) = checksign(sgA,kA)` at `../../cap_cc05_d.pv:619` accepts those bytes without equating them to the presented frame. The retained frame pin/hash and possession checks at `:614-618` instead validate the newly presented frame/manifest. This is byte unbinding, not total signature-check removal. SigJudge requires wctx and a different accepting key (`:1048-1052`), so the red really is wrapped and transplanted.

   The cited family trace uses the same construction at `s1_sig_unbound.out:873,883,887-897`, but obtains its outer wrapper from honest skW2. The slice removes honest Wrapper components and builds the outer wrapper under attacker key a_5. Both are permitted in case (d); the changed wrapper producer does not change the attacked inner relation or the severed check. Therefore: **yes, registered attack mechanism; no, not a literal replay of the family transcript**. It is also distinct from C-C5's strict-case C-Q8 attack using an honest same-key wrapper signature, which the registration discusses separately.

6. **The identity test is weak, and the slicer is not a general syntactic guarantee. Severity: low for these artifacts; changes any red: no.**

   `--identity` calls `make(src,'none','all')` (`slice.py:141-146`), which bypasses both transformation branches. Passing it proves the no-op returns the input; it exercises neither query deletion nor split_top. It cannot carry claim 1 by itself. The independent generated-file/prefix/component checks above supply the missing evidence.

   `split_top` counts parentheses without lexing comments/strings and does not validate depth balance (`:97-112`); query removal assumes a column-zero query and a line-ending period (`:125`); the process cut uses a literal marker (`:131`). A future comment containing unmatched parentheses or a pipe, or different valid formatting, can invalidate those assumptions. No such input was found in the audited final blocks. Treat source-format changes as requiring a fresh structural audit; do not promote this script to a general sound ProVerif slicer merely because identity passes. No source changes were made in this review.

7. **REPORT's “cannot give ... witnesses, or out-of-set reds” is too strong. Severity: medium, interpretation/documentation; changes any existing red: no.**

   `REPORT.md:64-65,103-106` conflates evidentiary limits with the exploration's chosen scope. The same trace inclusion transfers **any reconstructed out-of-set safety red** for an unchanged query, and **any actually reached witness event** whose producer/judge remains unchanged. Registration membership does not appear in the proof. For example, the unchanged source declares HonestChain/HonestAccepted reachability queries at `../../cap_cc02_d.pv:412-418`; a reconstructed occurrence of such an event would still be an occurrence in the full model. Slices often delete the machinery needed to reach these events, but that prevents discovery rather than making a discovered witness unsound.

   What does not transfer is unreachability/green, absence of out-of-set reds, or completeness of a companion's required results. No witness or out-of-set result is newly claimed here. The report should say these were not established by this probe, and keep registration eligibility separate. This correction strengthens the accurate evidentiary boundary without changing any observed red.
