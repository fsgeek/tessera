# Codex non-author review of the capstone registration, tenth round (2026-09-17)

Reviewer: OpenAI Codex CLI (`gpt-6-astra`), run non-interactively by the
owner instance on 2026-09-17 (20:06–20:21 UTC) against the whole of
`formal/suite/capstone/PREDICTIONS.md` after the round-nine repairs;
scratch diagnostics on family-model copies under
`/tmp/tessera-capstone-r10/`. **The reviewer found the registration not
ready to freeze**, on two findings — both consequences of the
round-nine report contract making failures observable that the
companion predictions had not caught up with — and confirms all
thirty-one earlier accepted findings present, the round-nine repairs
correctly cited, and (by a mechanical check) all 157 fully named
`cap*.out:line` anchors in the file resolving to `RESULT` lines. Every
run the reviewer cites was reproduced on our tree
(`formal/suite/ledger-tests-2026-09-14/cap23a`–`cap23h`, fourteenth
batch of that directory's README) at the reviewer's own `.out` line
numbers. No capstone model exists; nothing in the repository was run.

## Dispositions (owner instance, 2026-09-17)

Both are **clerk dispositions** of the owner instance; neither touches
a contestable choice.

1. **C-C15(i) retains guarantees that fail under the report
   contract.** ACCEPTED. The round-nine repair moved C-Q9 and link 3 to
   descended red and said "every other member of it stands unchanged".
   But the mutation checks the **outer** tuple, evidence and
   possession, then verifies the inner signature under `kW` and never
   examines the presented inner tuple or evidence; under the contract
   the inner acceptance reports those presented terms, and every
   relation over them is exposed. Reproduced with structural observers
   on the reported inner terms, restricted to well-formed tuples:
   baseline all green (`cap23b_sp7_strict_base_observers_tuple.out:1329`–`:1385`);
   on C-C15(i) in both channel variants, **link 1b** (prior authority
   publication of the inner tuple, `cap23d…out:1735`; `cap23f:1735`),
   **link 5**'s `mh` half (`:2017`), **link 2a**'s primary-slot relation
   (`:2297`), **link 1a** (`:2573`) and **C-Q5**'s relation (`:2883`) are
   all **red**, with the four S-P7 queries green (`:686`–`:716`) and both
   witnesses reachable (`:992`, `:1199`). The route: an honest same-key
   wrapper with its valid inner signature, bytes and outer credentials
   retained, the presented inner tuple and evidence replaced — no
   authorized adversary key, neither contestable choice reversed.
   **Repair:** C-C15(i)'s strict lists: **descended red** gains links
   1a, 1b, 2a, 5 (`mh` half) and C-Q5 beside C-Q9 and link 3 (cases
   (a) and (b), `cap23d`/`cap23f`); **predicted green** keeps C-Q7,
   C-Q8, link 4 (byte binding retained), link 2b, 6a, `Stripped`,
   `SignerForged`, `Spliced`, `VersionLied`, each with its basis; the
   sentence "every other member of it stands unchanged" is withdrawn,
   quoted. The degraded set (1) of configuration (i) gains the same
   five as **predicted red** under the contract (no degraded copy
   carries the observers); the family's Q6b row is not edited.

2. **C-C13(ii) assigns link 6a's red to layers whose type check is
   intact.** ACCEPTED. Ablation a10 relaxes only the **outer**
   `=OT_WRAPPER` guard and keeps `=OT_ATTEST` inside `InnerCheck`
   (`s-p7/proverif/ablations/a10_no_wrapper_type.pv:129-166`); the cell
   predicted `ChainBroken(lyr, LINK_6A)` "at `L1` and `L2`". Reproduced
   with separate inner and outer type observers: baseline both green
   (`cap23g_sp7_strict_type_base.out:1111`, `:1124`); under a10 the
   **inner** relation stays **green** (`cap23h…out:1313`) while the
   **outer** is **red** (`:1520`), `TypeConfused` red in aggregate
   (`:749`), witnesses reachable (`:1100`, `:1298`). **Repair:** C-C13(ii)
   states, per depth, which wrapper layer's guard is removed and assigns
   link 6a's red to **that layer only** — the wrapper layer, never the
   innermost attestation layer, whose `=OT_ATTEST` guard the
   configuration retains; the "at `L1` and `L2`" phrase is withdrawn,
   quoted, and the layer indexing is stated against (E4)'s convention
   (innermost = `L2` at depth 2). If a red at the innermost layer is
   wanted, that is configuration (i), not (ii). `TypeConfused`'s
   aggregate red stays descended.

3. **The REFUSAL fork stands**, unresolved, owed at the freeze commit;
   the four contestable choices stand and the reviewer confirms finding
   1 operates within them.

**Loop.** One repair pass (Opus), then an eleventh owner-run full Codex
pass.

## Codex review — verbatim

## 1. Query adequacy

No additional defect established in the query forms themselves. The new report contract makes previously hidden failures observable; the companion predictions have not fully caught up.

All new probes used ProVerif 2.05 on family-model copies under `/tmp/tessera-capstone-r10/`, with unchanged verifier checks and added observers. All terminated successfully. No repository file was changed and no capstone model was built.

## 2. Companion outcomes

**1. C-C15(i) retains several guarantees that fail under the newly fixed report contract.**

The strict cell removes C-Q9 and link 3 from its green list but explicitly says “every other member of it stands unchanged.” That still includes links 1a, 1b, 2a, 5 and C-Q5. Yet this mutation checks the outer authority tuple and possession proof, then accepts the inner signature under `kW` without checking the presented inner tuple or evidence. Reporting those inner terms exposes more than possession unbinding. (`formal/suite/capstone/PREDICTIONS.md:2173`; `formal/suite/ledger-tests-2026-09-14/cap22e_sp7_strict_q6b_q9_inner.pv:231–251`.)

**Constructed route:** obtain an honest same-key wrapper and its valid inner signature; retain their bytes, signatures and outer credentials; replace the presented inner tuple and evidence. The mutant still accepts. This needs neither an adversary-authorized wrapper key nor a reversal of either contestable fixture choice.

Added observers on the strict baseline and C-C15(i) give:

| Observed relation | Baseline | C-C15(i), DNS compromised | Repository compromised |
|---|---|---|---|
| Inner tuple has prior authority publication — link 1b | Green | Red | Red |
| Inner frame’s `mh = h(tI)` — link 5 | Green | Red | Red |
| Primary tuple fingerprint matches accepting key — link 2a’s primary-slot relation | Green | Red | Red |
| Presented inner evidence verifies over `tI` — link 1a | Green | Red | Red |
| Honest accepting key reports its sole signed manifest — C-Q5’s relation | Green | Red | Red |

These results persist with reports restricted to well-formed `authTuple` terms. Baseline results: `/tmp/tessera-capstone-r10/base_tuple.out:1329–1385`. Mutant results: `/tmp/tessera-capstone-r10/q6b_tuple.out:1735,2017,2297,2573,2883`; repository variant: `/tmp/tessera-capstone-r10/q6b_repo_tuple.out:1735,2017,2297,2573,2883`. Both honest witnesses remain reachable (`q6b_tuple.out:992,1199`).

The tested relations are the registered ones at `formal/suite/capstone/PREDICTIONS.md:321–326,350–370,468–475,617–639`. These are family-copy projections, not capstone results.

**Required repair:** revise C-C15(i)’s retained and failed sets across the affected cases. The report-contract repair cannot stop at C-Q9/link 3; preservation of byte binding supplies no basis for preserving the unexamined tuple relations.

**2. C-C13(ii) predicts the type failure at layers whose type check remains intact.**

C-C13(ii) removes the **outer** `=OT_WRAPPER` equality but predicts link 6a red “at `L1` and `L2`.” The registration separately identifies the depth-two innermost layer as `L2`, and requires each layer to report its own presented bytes. An outer-frame type violation cannot therefore be reported as the innermost layer’s violation. (`formal/suite/capstone/PREDICTIONS.md:2171,842–843,201–209`.)

The cited a10 transcription preserves `=OT_ATTEST` inside `InnerCheck`, while relaxing only the outer wrapper guard. (`formal/suite/s-p7/proverif/ablations/a10_no_wrapper_type.pv:129–166`.)

Separate structural observers confirm the distinction:

- Correct baseline: inner and outer type relations green (`/tmp/tessera-capstone-r10/type_base.out:1111,1124`).
- a10 mutation: **inner relation green, outer relation red**, while both honest witnesses remain reachable (`/tmp/tessera-capstone-r10/type_outer.out:1313,1520,1100,1298`).

**Required repair:** specify which wrapper-layer guard is removed at each depth and assign link 6a’s expected red to that layer. If an innermost-layer red is required, it needs a different mutation. The aggregate `TypeConfused` result does not establish the stated per-layer failed set.

## 3. Prediction bases and diagnostic citations

Finding 1 contradicts retained predictions; finding 2 shows that an aggregate family result does not support the registered layer assignment. I established no separate numerical-probability defect.

The round-nine repairs cite the recorded results correctly: C-C15(i)’s presented-inner C-Q9 reds and rejected outer-report green; C-C8’s strict manifest-hash greens and degraded red; and C-C6’s five declared green queries, with unqueried guarantees remaining predictions. (`formal/suite/capstone/PREDICTIONS.md:3213–3216,3231–3240`; `formal/suite/ledger-tests-2026-09-14/README.md:416–425`.)

The two C-C7(i) C-Q8 citations are exchanged as requested (`formal/suite/capstone/PREDICTIONS.md:1571,3215`). A mechanical check also confirmed that all **157 explicit, fully named `cap*.out:line` anchors** resolve to `RESULT` lines. That check alone does not validate abbreviated citations or the surrounding interpretation.

## 4. Buildability and the requested report-contract audit

| Companion | Report terms specified? | Audit result |
|---|---|---|
| C-C4 | Yes: presented inner terms under `kI` | Possession checks still examine those terms; no additional report-induced outcome change established. |
| C-C15(ii) | Yes: innermost terms under verified `kI`; attribution separately names the middle layer | The distinction preserves the structural reports while exposing the scope mutation. |
| C-C15(iii) | Yes: innermost terms under `kI`; attribution identity becomes `idW` | No additional report-induced outcome change established. |
| C-C13 | Yes: each layer’s presented terms under its accepting key | Term reporting is specified, but finding 2 leaves the required layer-specific outcome inconsistent. |

Sources: `formal/suite/capstone/PREDICTIONS.md:1568,2171,2173`.

Beyond finding 2, I established no additional missing fixture or ordering requirement.

## 5. Routed and contestable choices

The **REFUSAL fork is genuine and remains unresolved**. Both options and costs are explicit: introduce the honest REFUSAL signer and corresponding query/companion, bringing that symbolic fixture forward; or leave the domain unexercised and relinquish the proposed tag-separation demonstration. The file expressly reserves the decision to the author before the commit. (`formal/suite/capstone/PREDICTIONS.md:1794–1822`.)

Same-key wrapping and compromised-channel-only enrolment remain explicit, contestable choices; neither is reversed here (`formal/suite/capstone/PREDICTIONS.md:65,67`). Finding 1 operates within both choices. I established no additional hidden policy fork.

## 6. Earlier accepted findings and carried-forward corrections

The three ledger corrections remain honoured: structural C-Q8 without an honest-origin filter; publication provenance as a correspondence; and fresh intake identity with layer-preserving acceptance grouping. (`formal/suite/capstone/PREDICTIONS.md:350–356,394–423,140–162`; C-Q8’s registered contract in §3.)

The **31 accepted findings across rounds 1–9** have their specified repairs present, including the independent standing path, immutable join, identity-and-key scope comparison, terminal-unchecked witness exception, membership companion, per-case outcomes, and separation of descended results from predictions. Their repair mappings are recorded at `formal/suite/capstone/PREDICTIONS.md:2374–2379,2439–2442,2525–2528,2616–2617,2709–2710,2818–2823,2940–2941,3076–3077,3213–3215`. **Round 9’s report-contract repair is present but its consequences are incomplete**, as finding 1 demonstrates; the consequential C-C13 audit also misses finding 2.

**This registration is not ready to freeze. The author should see first: finding 1, C-C15(i)’s additional tuple/evidence failures; finding 2, C-C13(ii)’s incorrect layer-specific failed set; and the already-routed REFUSAL decision. Those are two new defects and one existing author decision—not three invented defects.**

