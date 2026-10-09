EXPLORATORY PROBE 2026-10-04 — non-discharging; not part of any registration

# FIDELITY: `cap_cc02_d.pv` (ProVerif) mapped to `cap_cc02_d.spthy` (Tamarin)

Source: `formal/suite/capstone/proverif/cap_cc02_d.pv` (working-tree blob, 1155 lines; the
ladder-3 form with BF-5/BF-6) plus `formal/suite/lib/tessera_theory.pvl`. The correct form,
`capstone_d.pv`, is the same Tamarin file run with `-D=CORRECT`. The two forms differ only in
`AttestTwo_*` and `WrapTwo_*`, and only in the mutation: the frame's `=fp(k_)` pin and
`mh = h(t)`, on both slots (`diff capstone_d.pv cap_cc02_d.pv`).

This is a hand transcription by one AI agent, done in one sitting. Nobody else has reviewed it.
Fidelity is the main risk; the ranked concerns are at the end.

## Encoding conventions (applied everywhere)

| ProVerif | Tamarin | Faithful? |
|---|---|---|
| `checksign` reduc + D-4 `otherwise` (dsks) | two equations: `checksign(sign(m,k),pk(k))=m`; `checksign(sign(m,k),pk(dsks(sign(m,k),r)))=m` | **Exact** as a rewrite system. The two left-hand sides do not unify (occurs check), so the `otherwise` priority is vacuous. Subterm-convergent; accepted by Tamarin. |
| `pk`, `sign`, `dsks`, `fp`, `h` (free constructors) | free function symbols (public) | Exact. |
| `[data]` constructors: `framed`, `authTuple`, `signers1`, `verified1/2`, `wrap`, `wctx`, `attemptCore`, `entry`, `lineage2`, `TERM_SHIPPED`, `withTLR`, `anchorProof`, `authTuple` | tagged tuples `<'tag', ...>` via `macros:` | **Approximation (A1).** Transparent to the adversary, as `[data]` is. But ProVerif tuples are arity-typed and Tamarin pairs are right-nested, so a k-field pattern also matches a longer tuple, with the tail collapsed into the last field. This only adds adversary behaviours (over-approximation), and only for malformed bundles. |
| ProVerif tuples `(a,b,c)` | Tamarin `<a,b,c>` | Same caveat as A1. |
| types (`pkey`, `skey`, `bitstring`) | untyped | **Approximation (A2).** Over-approximation: the adversary may send any term where a `pkey` is expected. ProVerif's attack search is also effectively untyped here, but this was not checked. |
| `free x: bitstring` / `const X` (public) | public constants `'x'` | Exact. |
| `free skI ... [private]` and the top-level `new skS; new skAdv` | fresh names in a single `Init` rule, restricted to fire once (`Once`) | Exact for reachability. |
| private channel `out(ch, m)` / `in(ch, x)` | persistent fact `!Ch(m)`, read without consumption | **Approximation (A3).** This is ProVerif's own Horn-clause abstraction, not the applied-pi semantics. A message on a private channel can be read any number of times, and two readers can both consume the one `out(stageCh, ...)` of a `Front`. It over-approximates, so an attack found here could in principle need a message to be read twice. The trace has to be checked for that (see REPORT.md). |
| `let pat = checksign(x,k) in P`, **in a stage** (the verifier's POSS/BYTES checks) | **two rules per check**: `_H` matches `x = sign(pat, sk)`, `k = pk(sk)`; `_D` matches `x = sign(pat, k0)`, `k = pk(dsks(sign(pat,k0), r))` (A13) | Exact: these are the two rewrite rules of `checksign`, and `checksign(x,k) = pat` holds iff one of them applies. |
| `let pat = checksign(x,k) in P`, check 1 (authority evidence under `pk(skS)`) | premise pattern `ev = sign(<'STMT_DIGEST', h(t)>, skS)` | Exact (the dsks case cannot unify with the fresh `skS`). |
| `let (=TLR, ...) = checksign(tlrSig, kT)` (standing path) | `Standing_tagOK` / `_dsks`, the same two cases | Exact. |
| `... else Q` of a destructor or pattern | action `Neq(...)` with restriction `Neq` | Exact when the negated pattern is ground in the rule's variables. Where it has wildcards, Tamarin's guarded fragment cannot say "matches no instance". Those places are listed as A7–A10. |
| `if a = b then P` | the same variable in the premise pattern | Exact. |
| `if a <> b then P` | `Neq(a, b)` | Exact. |
| replication `!P` | MSR rules fire unboundedly | Exact. |
| `new n` inside a process | `Fr(~n)` | Exact. |
| `event E(...)` | action `E(...)` | Exact, but see A4 on where events sit relative to checks. |
| ProVerif's per-process sequential `in`s (judges reading two channels) | one rule with both facts in the premise | Exact under A3. |

## Processes

| ProVerif construct (.pv lines) | Tamarin rule(s) | Notes |
|---|---|---|
| `process` (fixture, :1100-1155) | `Init` | It emits every `!out(honestKeyCh/MemberCh/SetCh, ...)` as a persistent fact, and every replicated honest-process instance as an instance fact (`!ShipI`, `!RefI`, `!AttI`, `!ForI`, `!WrapI`). `out(c, skS)` is the case-(d) delta. `out(c, skAdv)` and `out(c, MA)` are in. |
| `AuthorityS(skS, t)` ×3 | `AuthorityS` with `!AuthTask(M1/M2/MW)` | Exact. |
| `Attester(skB2, issuerId2, M2, cvA)` | `Attester` | Exact. |
| `ShipIssuer` ×2, `RefuseIssuer` ×2 | `ShipIssuer`, `RefuseIssuer` | Exact. Each is one atomic rule (ProVerif interleaves its outputs; there are no inputs mid-process, so the reachable knowledge is the same). |
| `Wrapper` ×3 | `Wrapper` | Exact. |
| `ForeignIssuer(skI)` | `ForeignIssuer` | Exact. |
| `Front` | `Front` | Exact under A3. One `In` of the 26-field bundle, plus a fresh `~aid`. |
| `AttestStage(pk(skS))` | `AttestCheck1_L{0,1,2}` (check 1, `AuthorityEvidence`, `authTuple` parse; one copy per layer, A11) → `AttestOne_parse` / `AttestTwo_parse_{correct,mutated}` → one step per signature check (`A1_chk*`, `A2_chk*`, each `_H`/`_D`) → `AttestOne_accept` / `AttestTwo_accept` | **A4b:** a branch is a parse rule (every pin, equality and type check as a premise pattern), then the signature checks in the .pv's order, then an accept rule that carries every event and output. Intermediate facts are internal, and no event or output sits between the checks in the .pv. **A4:** check 1 and the parse are a separate step, so `AuthorityEvidence` fires even when the branch later fails, as in the .pv. Within a branch, all checks and all events are one atomic rule. The .pv emits events only after every check passes, so this is exact. Check 1's `checksign(ev, pk(skS))` is written as the premise pattern `ev = sign(<'STMT_DIGEST', h(t)>, skS)`. That is exact, because `pk(skS) = pk(dsks(..))` has no unifier (`skS` is a fresh name). |
| two-signer `AttestStage` branch, **MUTATED** (:640-690 of cap_cc02_d.pv) | `AttestTwo_mutated`: frame fields `kfpxA`, `mhA`, `kfpxB`, `mhB` free | Mirrors the diff exactly. |
| two-signer `AttestStage`, correct (capstone_d.pv) | `AttestTwo_correct`: `fp(kA)`, `h(t)`, `fp(kB)`, `h(t)` pinned | Exact. |
| `WrapStage(pk(skS), L0, L1)` and `(L1, L2)` | **unrolled (A11)**: `WrapCheck1_01`, `WrapOne_*_01`, `WrapTwo_*_01`, `W1_*_01`, `W2_*_01` and the same with `_12`. Hand-down: `!StageL1(aid,'L1', wctx(kA,id,fbA), ...)` and `!StageL2(...)` | Exact. The .pv instantiates `WrapStage` exactly twice, so per-layer facts (`!StageL0/L1/L2`, `!SStageL0/L1/L2`) are the same system. The version check (`=cvIw` in `fbIA`) is a premise pattern in the parse rule. In the .pv it comes after the signature checks, with nothing observable between. |
| `SUnwrap` ×2 | `SUnwrap_01`, `SUnwrap_12` | Exact (pattern; unrolled, A11). |
| `StandingPath` (BF-5 innermost selection) | `StandingPathIn_L{0,1,2}` | **A7 (approximated):** "fbI does not match `framed(OT_WRAPPER,…,wrap(_, 4-tuple))`" is tested as `Neq(<fst, fst∘snd, fst∘snd^7>(fbI), <'framed','OT_WRAPPER','wrap'>)`, i.e. on the three tags, not on the inner tuple's arity. A malformed wrapper with a short inner blob is treated as "not innermost" here and as "innermost" in the .pv. This is standing path only. |
| TLR destructor in `StandingPath` | `Standing_tagOK`, `Standing_tagOK_dsks` (success, both reduction cases written out) and `Standing_tagBad` (else) | **A8:** the else branch is tested on the tag only (`Neq(fst(checksign(..)), 'TLR')`). A TLR-tagged message whose body is not a triple gets no `SIGNATURE_INVALID` report here. Standing vocabulary only. |
| `lookup2` (reduc with `otherwise`) | `Standing_lookup1/2/Miss` | **A9:** a lineage that is not `lineage2(entry, entry)` gets no `MISMATCH` report. Standing vocabulary only. |
| `StandingDecide` | `Decide_*` | **A10:** "terminal neither `TERM_REFUSED` nor `TERM_SHIPPED(_)`" is tested on the tag. `EstablishedWrapped` is split into its own rule guarded by `Neq(lyr, 'L0')`, which is exact. |
| `ReasonSink` | omitted (`!ReasonCh` has no reader) | It emits nothing, so the omission is harmless. |

## Judges

| ProVerif judge | Tamarin rule(s) | Notes |
|---|---|---|
| `Link1aJudge(pk(skS))` | `Link1aJudge` | Both destructor elses become two `Neq`s on ground terms. Exact. |
| `Link2aJudge` | `Link2aJudge_fp / _notB / _s0` | Exact *given the producers*. The `else` of the `authTuple` and `signers1` parses is replaced by the only shapes a stage ever sends (`signers0` or `signers1(_)`). |
| `PossJudge` (link 3 + C-Q9) | `PossJudge` | Exact. |
| `BytesJudge` (link 4 + C-Q8) | `BytesJudge` | Exact. |
| **`Link5Judge`** (link 5 frame-to-key) | **`Link5Judge_kfp`, `Link5Judge_mh`** | Exact *given the producers*. Every `!Link5` producer has already parsed `fb` as `framed(...)`, so the .pv's `else` is exactly "kfp ≠ fp(kX) or mh ≠ h(t)". Each rule also emits an instrumentation event (`Link5FrameToKey` / `Link5ManifestHash`) that the .pv does not have. They are used only to say which half fired. |
| `Link5cJudge` (link 5 cross-slot) | `Link5cJudge_ot/_cv/_pl` | Exact. They emit the same `ChainBroken(l, LINK_5)` as the .pv. |
| `Link6aJudge`, `Link6bJudge` | `Link6aJudge`, `Link6bJudge_k/_id` | Exact given the producers (`fb` always framed). |
| `JudgeH` | `JudgeH` | Exact. |
| **`SP3Judge`** (C-Q3) | **`SP3Judge_honest / _reA / _reB`** | Exact: `kX = kH` with `ctx = BASE` gives `HonestAccepted`. `kX ≠ kH` gives `ReattributedA` if role = `SLOT_A`, `ReattributedB` otherwise. |
| `SetJudge` | `SetJudge_complete2 / _stripped / _complete1` | Exact. |
| `MemberJudge` | `MemberJudge_forged / _altered` | Exact. |
| `ContentJudge` | `ContentJudge_ot/_cv/_pl` | Exact. |
| `TypeJudge`, `ScopeJudge`, `SigJudge`, `GenericSigJudge`, `VersionJudge`, `ChainWitnessJudge` | same names | Exact. |
| `StandingJudge`, `ScopeAgreementJudge` (+ 2 observers), `TagJudge` | same names | Exact (the `if (ka,ia) <> (k,idS)` is a pair `Neq`). |

## Queries

| ProVerif query | Tamarin lemma | Run? |
|---|---|---|
| `query l; event(ChainBroken(l, LINK_1A))` (the query ProVerif stalled on) | `Link1a` | yes |
| `event(ReattributedA(...))`, `event(ReattributedB(...))` (C-Q3, **set (1)**) | `CQ3_ReattributedA`, `CQ3_ReattributedB` | yes |
| `event(ChainBroken(l, LINK_5))` (link 5, **set (1)** frame-to-key half) | `Link5` (+ `Link5_frameToKey_only`, instrumentation) | yes |
| `AcceptS ==> IssuerSigned` (registered red in (d), the A4.6 cost) | `A46_AcceptS_IssuerSigned` (sanity anchor; the .pv's correspondence carries no explicit `j < i`, and Tamarin's form adds it — immaterial for a red) | yes |
| C-N1 witnesses `HonestAccepted`, `HonestChain(L0/L1)`, `HonestComplete(..verified2..)` | `W_*` (exists-trace) | yes |
| every other query of the .pv (links 2a, 2b ×3, 3, 4, 6a, 6b; C-Q4, C-Q5, C-Q5w, C-Q6 ×4, C-Q7, C-Q8, C-Q9, C-Q10; the retained queries; the other witnesses) | **not written** | The events are all emitted, so each is a one-line lemma to add. They were left out to keep the probe on set (1). |

## Ranked fidelity concerns

1. **This is an unreviewed hand transcription (the largest risk).** About 600 lines of MSR were written in one sitting from a 1155-line .pv. No second reader has checked it, and there is no mechanical cross-check (for example SAPIC+ export to ProVerif, then diff). A transcription slip in a stage rule could create or hide the attack. The partial mitigations: the `-D=CORRECT` contrast (the same file must *not* produce the attack), and the witnesses (honest flows are reachable).
2. **A3, private channels as persistent facts.** This matches ProVerif's clause abstraction, not its process semantics. An attack here has to be checked by hand to see that it does not read a one-shot private message twice, which REPORT.md does for the attack found. A verified result is unaffected, since this is an over-approximation.
3. **A1/A2, tuples and types.** The tuples are untyped and right-nested. Both are over-approximations, so neither can hide an attack. They could in principle manufacture one; the attack trace has to be read to rule that out.
4. **A7–A10.** Standing-path else branches are approximated on tags. Nothing in C-C2's set (1) or link 1a reads a standing-path fact or event, and the standing path emits no `Out` (adversary knowledge). So these approximations cannot affect the lemmas run here. They would matter for C-Q6-family companions.
5. **Event placement (A4).** Each acceptance branch is one atomic rule. This is exact for these queries, since events come after all checks in the .pv. Queries that order events relative to one another inside one acceptance (none here) would need finer rules.

## Encoding revisions made during the probe (each a solver-performance change; semantics argued equal)

| Rev | Change | Why | Semantic argument |
|---|---|---|---|
| v1 → v2 | One rule per acceptance branch (with 4 `Eq(checksign..)` actions) split into parse, one step per check, then accept (A4b) | v1's two-signer rules have 2^4 rule variants each, and three runs ran out of memory at 6–8 GB | Internal intermediate facts. Events and outputs are only in the accept rule, as in the .pv. |
| v2 → v3 | One `!Stage` / `!SStage` fact with a recursive hand-down, unrolled per layer (A11) | Tamarin's source precomputation hit a Haskell `<<loop>>` (single-threaded) or unbounded memory (`-N3`) on the recursion | The .pv bounds depth at 2 by instantiating `WrapStage` twice. The unrolled system has the same reachable states. |
| v3 → v5 | `Eq(checksign(sig,k), msg)` replaced by explicit `_H` / `_D` rules (A13) | Depth-first search took the dsks variant first and diverged | The two rules are exactly the two rewrite rules of `checksign`. (v4, "verification as an adversary-derived fact", was tried in scratch and was worse: 18.7 GB at 485 s. It was discarded.) |

## Slices and guided slices (`slice.py`)

`slice.py` only **deletes whole rules**. Deleting rules only removes behaviours, so:

* **an attack (trace) found in any slice is a trace of the full model** (`cap_cc02_d.spthy`);
* **a `verified` in a slice is NOT a result for the full model.** It says only that no attack
  exists among the slice's behaviours.

| Slice | Deletes | Use |
|---|---|---|
| `depth0` | every `WrapStage` rule, `AttestCheck1_L1/L2`, `SUnwrap_*`, `StandingPathIn_L1/L2` (no wrapped layers are accepted) | Falsification. The correct-form `verified`s here are depth-0 statements only. |
| `depth1` | the (L1, L2) wrapper layer | Falsification. |
| `depth2` | nothing (= the full model) | — |
| `+noD` | every `_D` (dsks) reduction at stage checks | Falsification only. A **guided under-approximation**. |
| `+bytesD` | the `_D` reductions of the POSS checks | Falsification only. |
| `+attOnly` | as `bytesD`, plus the honest processes `ShipIssuer`, `RefuseIssuer`, `ForeignIssuer`, `Wrapper` | Falsification only. This is the strongest guidance. The C-Q3 trace uses only `Attester`, `AuthorityS` and `Init` among the honest rules. |

**Fidelity concern raised by the guidance itself.** Tamarin found the C-C2 reds only after
rules were deleted by hand, so a human chose where to look. The traces are valid traces of
the full model, but **"Tamarin found it unaided in the composed model" is not established.**
