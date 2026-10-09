**Verdict: freeze after listed fixes.** Findings 1–5 require changes before freeze. The deletion-only slicing argument and the A8.4 query are defensible; the present rules can nevertheless count evidence outside a registered layer restriction, skip a necessary fallback, and accept vacuous companion greens. This is one pre-freeze review, not discharge or confirmation of the predicted runtime results.

Evidence paths below are repository-relative; `S` abbreviates `formal/suite/capstone/SLICE-PREREG-2026-10-09.md`, `P` abbreviates `formal/suite/capstone/PREDICTIONS.md`, and `V` abbreviates `formal/suite/capstone/proverif/`.

1. **HIGH — Item (L) broadens registered wrapped-inner members to base acceptances.**

   Evidence: `S:61-63` says “A red at any layer of AttestStage counts.” But `P:1773` registers C-C4 link 5's frame-to-key half “at the inner layer,” in a row descending a degraded **depth-1** S-P7 model. `P:1774` registers C-C5 C-Q8 and link 4 “at the inner layer”; its Cases cell explicitly says the structural judge is “restricted to wrapped inner acceptances.” `P:120` distinguishes `InnerCheck` for `lyr ≠ L0`; `P:3490-3492` distinguishes the unrestricted judge from the wrapped-inner baseline and mutation. The builder's comment in `V/capstone.pv:580-585` that one implementation process is shared by L0 and wrapped innermost layers does not amend these registered scopes.

   Rows 12, 14 and 15 (`S:115-118`) have depth0.cone fallbacks. These delete wrapper descent altogether, so an L0 failure cannot demonstrate their registered wrapped-inner member. Even depth1 permits L0 failures. Such failures transfer to the full file's **unrestricted query**, but not to its registered **wrapped-inner claim**. Sharing code proves the mutation is exercised; it does not prove the required consumer is exercised.

   **Exact fix:** replace (L) with: “For rows 12, 14 and 15, count only a reconstructed trace whose violating accepted frame is an OT_ATTEST frame at L1 or L2 reached through wrapper descent in that intake. An L0 violation is recorded as an additional uncounted mutation consequence.” Remove the depth0.cone fallbacks for these rows; preregister depth1.cone alternatives and their hashes, or state that no further fallback exists. Keep queries and process bodies unchanged. If the author wants L0 to satisfy these members, that needs an explicit amendment to their registered scope, not this interpretive note.

2. **MEDIUM — The fallback trigger uses query polarity instead of the counting predicate.**

   Evidence: `S:93-95` runs the fallback “only if the primary is not red.” Yet `S:57-60` and `S:266-268` correctly refuse to count a link-5 red when its required half is not visible. `V/cap_cc02_d.pv:948-951` conflates key-fingerprint and manifest-hash mismatch in one failure branch. A primary can therefore report false with a trace for the wrong half, suppress the fallback, and leave the registered member not shown even though the fallback might show it. The same issue applies to the layer qualification in finding 1.

   **Exact fix:** say “Run the fallback unless the primary has rc=0, a reconstructed false result for the kept query, and a trace satisfying every row-specific counting condition.” Evaluate T/H/L on the **same violating accepted frame** responsible for the queried failure. A wrong-half or wrong-layer trace remains an uncounted full-file red. Do not treat it as satisfying the row or as a reason to skip the registered fallback.

3. **HIGH — Companion A8.4 vacuity witnesses are predicted, then explicitly not read.**

   Evidence: `S:182-183` says A8.4w “must be REACHABLE”; `S:206-209` predicts it reachable in every C-C15 file. `S:228` then says witness results in those files “are recorded and not read.” `S:280-283` defines a vacuity response only for correct-form files. This leaves C-C15(i) strict greens and (ii)/(iii) greens acceptable even if their joined premise never occurs.

   The witness is adequate **when enforced**: `V/dev/prereg_scratch/derive_a84.py:17-23` asks for the exact safety premise with equal keys. Its reachability is stronger than simple premise reachability, so a reconstructed witness proves the safety query is not wholly vacuous. Its unreachability does not itself prove the general premise unreachable (unequal-key instances could exist).

   **Exact fix:** remove “and not read.” For **every green-predicted A8.4 file**, require a reconstructed A8.4w reachability result (`not (premise-with-equal-keys) is false`, with its own trace). If it is proved unreachable, report the witness prediction as falsified and withhold the non-vacuous green pending diagnosis; if inconclusive, report non-vacuity not shown. A C-Q6k reconstructed red already witnesses its own premise, but does not satisfy the separate equal-key witness prediction. Require query-specific traces: one file-level `traceFound` flag cannot distinguish the two queries.

4. **MEDIUM — The named audit and runner do not yet enforce the registered workflow.**

   Evidence: `S:70-78` requires auditing counted outputs in `proverif/slice/gen/`, and `S:257-261` names the pilot runner with only banner/library edits. However, `V/dev/slice_probe/codex/audit.py:3-5,40-42` hardcodes pilot sources and pilot `gen`/`gen_ext`; its construct scan at `:34-39` prints hits without failing. `V/dev/slice_probe/codex/exact-prefix.py:3-5,15` scans working-directory `gen`/`gen_ext` and prints a fixed total even if no files were checked. The pilot runner (`V/dev/slice_probe/run.sh:9-19`) logs hashes after runs but has no expected-manifest comparison, control gate, or batch-stop logic. Removing its banner and changing LIB cannot implement the stop promises of `S:261,274-277`.

   **Exact fix:** specify an executable audit/batch procedure with explicit counted source/output roots and the frozen expected manifest. Require nonzero checked counts matching that manifest; fail on prohibited constructs, unexpected set lines, altered prefix/components/query, and blob mismatches. Check blobs **before** execution as well as afterward. Run/read controls and close that gate before primaries; stop on a control red or provenance mismatch, with no subsequent results counted. Record the audit/runner hashes and validation before the first counted run. This can be a supervising script or an explicit mandatory manual procedure; the existing pilot script alone does not enforce it. No counted ProVerif run is needed to validate these mechanics.

5. **MEDIUM — Failure of all slice members must not automatically adopt A8.3's rejected family-only alternative.**

   Evidence: `S:269-271` automatically falls back to family evidence and says A3.3 is narrowed. The governing ruling (`docs/phase-0-prereg-amendment-8.md:72-79`) expressly calls family-evidence-only a **rejected alternative** because it narrows A3.3. Its adopted allowance at `:62-70` permits slice reds; it does not authorize a new discharge rule when none land.

   **Exact fix:** replace that branch with: “If no registered set-(1) member is shown, composed degraded severing evidence remains withheld. Report the existing family evidence separately and route any proposed narrowing of A3.3 to the author for an explicit amendment.” Partial results must likewise list shown and unshown members without implying complete companion discharge. This preserves failure visibility without changing the finish line automatically.

6. **INFORMATIONAL — Membership inventory otherwise passes; exclusions are stated.**

   Evidence: compare `S:104-136` against the failed-set and Cases cells at `P:1771-1777,2547,2666`:

   | Companion | Counted rows | Registered case-(d) members represented |
   |---|---|---|
   | C-C2 | 1–3 | C-Q3 A/B; link 5 key half |
   | C-C3 | 4–6 | C-Q5; C-Q9; link 3 |
   | C-C4 | 7–12 | Rescoped; InnerSigTransplanted; C-Q3 A/B; link 6b; link 5 key half, subject to finding 1 |
   | C-C5 | 13–15 | InnerSigTransplanted; C-Q8; link 4, subject to finding 1 |
   | C-C6 | 16–19 | C-Q7; InnerSigTransplanted; predicted-also C-Q8/link 4 |
   | C-C7(i) | 20–22 | C-Q8; link 4; honest-key authorship |
   | C-C7(ii) | 23–26 | Structural C-Q8; link 4; composed C-Q7; honest-key authorship |
   | C-C8 | 27–30 | C-Q9; C-Q5; link 3; link 5 hash half |
   | C-C8-ii | 31 | By-construction C-Q9 red, not its required green/isolation outcome |
   | C-C17 | 32–33 | Link 2a; SignerForged |

   The absent C-C7(ii) honest-filtered C-Q8 and C-C17 PossessionTransplanted are expressly listed as unavailable queries (`S:138-140`). The latter is a real registered set-(1) residual, not proof that the consequence is absent. Strict-only authorship additions under A8.2 are correctly excluded from (d). C-C8-i and the isolation greens are explicitly carried on family evidence under A8.3 (`S:233-236`); row 31 cannot establish isolation. No extra unregistered query member was found. **Fix:** none beyond finding 1; preserve the named missing-member residuals in the final read.

7. **INFORMATIONAL — Trace inclusion is sound for these deletion-only safety slices, conditional on the audit.**

   Evidence: governing `docs/phase-0-prereg-amendment-8.md:63-66,81-82`; `S:33-39,66-78`; `V/dev/slice_probe/slice.py:79-94,114-138`. The slicer filters whole final parallel components, preserves kept query text, and leaves the fixture prefix and bodies intact. The actual ten companion source blocks are replicated calls; no prohibited construct was found in an independent comment-stripped scan of those sources. A finite slice attack can be scheduled in the full process while the additional replicated components remain inactive. For authorship correspondences, those inactive components need not emit extra IssuerSigned events before the violating acceptance. Ordinary local destructor-failure branches are unchanged; table absence tests and global constraints would defeat this reasoning, hence the stated exclusions matter.

   I reproduced all 104 existing scratch slice bodies in memory; all matched slice.py. All 66 counted primary/fallback hash prefixes matched the table. Both registered derivation-script SHA256 values matched. No counted slice was executed. **Fix:** none to the mathematical rule. Implement finding 4, and keep full-query transfer distinct from the scoped membership failure in finding 1. The rule is format-specific, not a safe arbitrary ProVerif parser.

8. **INFORMATIONAL — C-Q6k observes the verified key; the C-C15(i) per-case prediction is credible and not necessarily vacuous.**

   Evidence: `V/capstone.pv:567-577` gives both paths the same intake and layer-specific material; `:618-619,657-660` emit LayerAccepted with the key used by checksign. Standing establishes only on a non-L0 structurally terminal layer (`:843-844,855-884`) and requires `kT = kX` (`:893-905`). Under C-C15(i), the wrapped verifier instead checks and emits with kEncW (`V/cap_cc15i_a.pv:712-725,763-765`; `V/cap_cc15i_d.pv:695-708,745-747`). The derivation block (`V/dev/prereg_scratch/derive_a84.py:10-16`) joins aid, layer, tuple, primary slot, and the immutable signature term. It does not substitute ScopeReported for verified-key evidence. Independent derivation checks found no non-query process changes in all 13 outputs. The concrete output block is, for example, `V/dev/prereg_scratch/a84/a84_cap_cc15i_a.pv:383-399`.

   Strict (i) has a constructive witness route: ShipIssuer(skI) releases a shipped core, possession, attestation signature and TLR; Wrapper(skI) wraps that attestation; both authority channels evidence M2 (`V/cap_cc15i_a.pv:1240-1267`, ShipIssuer outputs `:489-493`). Supply the same issuer-A frame/signature in both unchecked inner slots: AttestStageW verifies both under the same wrapper key skI. Standing uses the primary-slot skI core and TLR. Thus a joined equal-key premise can occur even though the independently keyed skW route cannot accept that issuer signature. For (ii)/(iii), verification remains under kA and a normal honest wrapped route supplies the premise.

   Strict mismatch is excluded structurally: standing authority checks pin its tuple/key to the honest issued manifests; TLR and its immutable core signature come from ShipIssuer(skI/skI2). The uncompromised outer authority channel restricts a usable wrapper key to an honest evidenced key. The algebra (`formal/suite/lib/tessera_theory.pvl:106-115`) cannot make another fixed honest key verify that signature; DSKS-derived wrapper keys lack the uncompromised evidence. In (d), choose an attacker-held inner standing key and its signed core/TLR, and use a DSKS-derived wrapper key that verifies that very same inner signature. Captured authority can evidence both tuples. The unchecked presented inner pins in AttestStageW allow kV != kS. This supports red only in (d), green in (a)/(b), as a **prediction**, not a run result.

   A8.4w demonstrates one joined instance, not non-vacuity at every depth, on every signer, or on every route. The query is about the core's primary signature; it does not assert equality to every member of a multi-signer set. Its ppf and ppfV are deliberately distinct: equating them would unnecessarily exclude mutations of the presented proof. **Fix:** enforce finding 3; no query rewrite is required for the stated primary-signature property.

9. **LOW — Controls are suitable for transfer defects, but their evidence and inconclusive outcomes need explicit limits.**

   Evidence: `S:144-155` supplies matching correct-form slices for all registered (slice, query) pairs. The two A4.6 reds are useful positive controls, but they are not tests of wrapped-inner reachability or either link-5 half. A green negative control cannot prove a companion cone still contains its attack. `S:278-279` appropriately treats a green A4.6 control as a caveat rather than a refutation. The “out-of-set reds: none can appear” sentence at `S:237` concerns query declarations only; a selected broad query can still fail outside its registered layer or half.

   **Exact fix:** state that unavailable/inconclusive negative controls leave the control gate incomplete, and define whether the batch pauses or continues with results withheld. State that A4.6 false requires its reconstructed trace, and that timeout/cannot-prove is an inconclusive positive control, distinct from a proved green. Change `S:237` to “Unqueried out-of-set failures are not measured; scoped out-of-set failures of kept queries are recorded and not counted.” Together with findings 1–5, the falsifiers then separate actual divergences, unshown evidence, vacuity, and void provenance.

Validation: only A8.4 derivatives with the main process replaced by 0 were passed to ProVerif (all 13 rc=0); their trivial greens/unreachable witnesses are parse/type evidence only. Details are in `validation.txt` alongside this review. No full derived model, counted slice, VM, staging operation or commit was run. All writes stayed in `V/dev/prereg_scratch/codex/`.
