# Codex non-author review of the capstone registration, fourth round (2026-09-17)

Reviewer: OpenAI Codex CLI (`gpt-6-astra`), run non-interactively by the
owner instance on 2026-09-17 (18:00–18:06 UTC) against the whole of
`formal/suite/capstone/PREDICTIONS.md` after the round-three repairs,
with the three earlier records as its starting point; scratch
diagnostics on family-model copies under `/tmp/tessera-capstone-r4/`.
**The reviewer found the registration not ready to freeze**, on two
supported defects — its own words: *"I found two supported defects, not
a third to manufacture. The repaired structural join passes the
requested independence and substitution controls."* Every factual claim
below was checked against the tree before disposition, and every run
the reviewer cites was reproduced on our tree
(`formal/suite/ledger-tests-2026-09-14/cap12a`–`cap12g`, eighth batch of
that directory's README) at the reviewer's own `.out` line numbers. No
capstone model exists; nothing in the repository was run. The reviewer
confirms all fourteen accepted findings of rounds one to three repaired
(R1.4 and R3.2 reopened only by finding 1 here), the three ledger
corrections honoured, and the two contestable fixture choices explicit.

## Dispositions (owner instance, 2026-09-17)

Both are **clerk dispositions** of the owner instance; neither fixes a
fixture meaning.

1. **Conjunct 3 compares the key only; the inherited scope relation
   covers key and issuer identity.** ACCEPTED. S-P7's `Rescoped` fires
   on `(kIrep, idIrep) ≠ (kH, idH)` (`s-p7/PREDICTIONS.md:226-237`), and
   its Q6a companion is exactly the identity-only case: verification
   under `kI` retained, the wrapper's identity reported
   (`sp7_q6a_companion_identity_outermost.pv:189-200`). Reproduced:
   on the structural-join copy, changing **only the reported issuer
   identity** leaves all three C-Q6 conjuncts green
   (`cap12e_ss_q1_join_scope_identity.out:542`, `:570`) while an
   identity judge fires (`:945`), substitution excluded (`:563`) and
   honest standing reachable (`:1718`); on a copy of the committed Q6a
   companion, a key-only scope judge stays green
   (`cap12f_sp7_q6a_keyjudge.out:1339`) while the committed `Rescoped`
   is red (`:818`) and the honest wrapped witness reachable (`:1130`).
   **Repair:** the standing path's report carries the innermost issuer
   identity it extracted itself — `(aid, lyr, kX, id)`, `id` from its
   own `authTuple(id, kfpr, …)` — and the judge fires
   `ScopeMisreported(aid, lyr, kX, id, kA, idA)` when
   `(kA, idA) ≠ (kX, id)`, the pair form S-P7's judge uses; unreachable
   in (a), (b), (d). The identity-only demonstration is registered as
   a **third, isolation configuration of C-C15** — S-P7 Q6a transcribed,
   *identity from the outermost, key retained* — whose set (1) is
   conjunct 3, C-Q4's `Rescoped` (descended, committed
   `sp7_q6a…out:516`, `:806`) and link 6b at `L1`; set (2) everything
   else including conjunct 3's **key** half, so the run shows the
   identity comparison is what fires; set (3) the honest wrapped
   witnesses. C-C15's existing note that Q6a is "the isolation
   contrast" becomes this configuration. The companion count stays
   sixteen; no timeboxed entry is added.

2. **C-C11's terminal-unchecked alternate makes a universally required
   witness unreachable.** ACCEPTED. S-STANDING Q4 replaces the terminal
   decision with unconditional `ESTABLISHED` after lineage membership
   (`ss_q4_companionC_terminal_unchecked.pv:231-237`), so the S4 witness
   `(ABSENT, ISSUANCE_REFUSED)` — and the S2 witness `(ABSENT,
   SUPERSEDED)` — cannot fire: the branches no longer exist. The family
   already records this as a consequence of the mutation
   (`s-standing/RESULTS.md`, Q4 row: *"S2 and S4 witnesses unreachable …
   consequence of the mutation, the branches no longer exist"*;
   `ss_q4…out:1708`, `:1838`). Reproduced on the structural join with
   the paired judge: standing correspondences red
   (`cap12g_ss_q1_join_terminal_unchecked.out:810`, `:1136`), S2 and S4
   unreachable (`:3217`, `:3413`), honest standing and the agreement
   witness reachable (`:2873`, `:1542`). But C-Q6 lists the S4 witness
   among its required witnesses and C-N1 says *"a run in which any
   registered witness is unreachable is a broken fixture"*, so a
   faithful transcription of the alternate would be classified as a
   broken fixture. **Repair:** the witnesses are split into two kinds —
   **honest-flow witnesses** (`HonestStandingEstablished`,
   `HonestWrappedStandingAgreed`, `HonestWrappedAccepted`,
   `HonestAccepted`, both `HonestComplete`, `HonestChain`), which must
   survive every companion, and **vocabulary witnesses** (the S1–S4 and
   MISMATCH report-shape witnesses), reachable in every correct-form run
   and whose disappearance under a **named** companion is a registered
   consequence, never a broken fixture. C-N1's rule gains that
   exception, quoted and dated; C-C11's row records S2 and S4
   unreachable under its Q4 alternate, descended from the committed run
   and `cap12g`; C-Q6's witness list marks the S4 witness as a
   vocabulary witness.

3. **Conjunct 3's independence controls, recorded as its descent.** The
   reviewer's four paired-judge runs are archived so the file can cite
   them instead of asserting: correct checks — scope mismatch,
   unentitled standing and substitution all unreachable
   (`cap12a_ss_q1_join_correct.out:570`, `:998`, `:563`); C-C12 —
   unentitled **reachable** (`cap12b…out:1762`), scope unreachable
   (`:813`); key-scope mutation — scope **reachable** (`cap12c…out:947`),
   unentitled unreachable (`:1378`); both — both reachable
   (`cap12d…out:1192`, `:2140`); the agreement witness reachable in all
   four (`:958`, `:1204`, `:1334`, `:1581`). Both paths emit
   independently; only the judge waits.

4. **The REFUSAL fork stands** as the one routed item, unresolved here;
   the reviewer names it, correctly, as owed before the freeze commit.
   The two contestable choices stand.

**Loop.** One repair pass (Opus, briefed from these dispositions), then
a fifth owner-run full Codex pass. Round four's two findings are both
on round three's new conjunct and on a witness rule that conjunct's
mutation-set exposed; nothing outside the repaired text was found.

## Codex review — verbatim

## 1. Query strength and discharge

Repository files were read only. New diagnostics used family-model copies under `/tmp/tessera-capstone-r4/`, with a copied theory library. No capstone model was built.

Below, **P** means `formal/suite/capstone/PREDICTIONS.md`; **T** means `/tmp/tessera-capstone-r4`.

**1. C-Q6’s scope-agreement conjunct misses identity-only re-scoping.**

The envelope report carries `(aid, lyr, kA, idA)`, but the judge tests only `kA ≠ kX`. It never compares `idA` with the innermost issuer identity. Nevertheless, D11’s conditional discharge names this conjunct as its scope consumer. (`P:883–900`, `P:1250`.)

The inherited scope relation covers **both key and issuer identity**. S-P7’s Q6a demonstrates the missing case: it retains verification under `kI` but reports the wrapper’s `idW`. (`formal/suite/s-p7/PREDICTIONS.md:226–237`; `formal/suite/s-p7/proverif/sp7_q6a_companion_identity_outermost.pv:189–200`.)

Two diagnostics confirm the gap:

- On the structural-join copy, changing only the reported issuer identity leaves **all three C-Q6 conjuncts green**, while `ScopeIdentityWrong` becomes reachable. Substitution remains excluded and honest standing remains reachable. (`T/scope_id.pv:337–364`; `T/scope_id.out:542`, `:570`, `:945`, `:1368`, `:1718`.)
- On a copy of the actual Q6a companion, adding a key-only scope judge leaves that judge **green**, while the existing full `Rescoped` query is **red**, with its honest wrapped witness reachable. (`T/q6a_keyjudge.out:1339`, `:818`, `:1130`.)

**Required repair:** register agreement on the attributed issuer identity as well as the key, with an identity-only mutation demonstrating the added comparison. Link 6b can detect this defect elsewhere; that does not establish C-Q6’s claimed consumption.

## 2. Companion consistency

**2. C-C11’s terminal-unchecked alternative necessarily kills a witness the registration universally requires.**

C-Q6 requires the S4 witness `(ABSENT, ISSUANCE_REFUSED)`. C-N1 says an unreachable registered witness makes a run a broken fixture. Yet C-C11 permits S-STANDING Q4’s terminal-unchecked mutation without recording an exception to that rule. (`P:987–993`, `P:1053–1059`, `P:1171`.)

Q4 replaces the terminal decision with unconditional `ESTABLISHED` after lineage membership. Its committed S4 witness is therefore **unreachable**, while honest standing remains reachable. (`formal/suite/s-standing/proverif/ss_q4_companionC_terminal_unchecked.pv:231–237`; corresponding `.out:1838`, `:1425`.)

The same result holds after adding the structural join and paired scope judge: standing correspondence **false**, S4 **unreachable**, honest standing and scope-agreement witnesses **reachable**. (`T/terminal_unchecked.out:810`, `:3413`, `:2873`, `:1542`.)

**Required repair:** explicitly register S4’s disappearance as a consequence of this alternative, and distinguish vocabulary witnesses from the honest-flow witnesses that must survive. Otherwise a faithful transcription is classified as a broken fixture.

## 3. Prediction bases and requested controls

The cited cap5a–cap8b and cap9–cap11c result polarities match the tree and the sixth/seventh-batch records. The corrected honest-key-authorship basis also matches cap7b. These remain family-copy diagnostics, not capstone discharge. (`P:1954–1962`, `P:2042–2046`, `P:1071`; `formal/suite/ledger-tests-2026-09-14/README.md:159–168`, `:200–204`.)

The requested **actual paired-report judge** works without reintroducing path dependency:

| Diagnostic | Scope mismatch | Unentitled standing | A/B substitution |
|---|---|---|---|
| Correct checks | Unreachable | Unreachable | Unreachable |
| C-C12 | Unreachable | **Reachable** | Unreachable |
| Key-scope mutation | **Reachable** | Unreachable | Unreachable |
| Both mutations | **Reachable** | **Reachable** | Unreachable |

Evidence: `T/correct.out:563–577`, `:998`; `T/cc12.out:805–813`, `:1762`; `T/scope_key_live.out:570`, `:947`, `:1378`; `T/cc12_scope_key_live.out:814`, `:1192`, `:2140`. The agreement witness remains reachable in all four (`:958`, `:1204`, `:1334`, `:1581`, respectively).

Both paths emit independently; only the judge waits for the matching `(aid, lyr)` reports. These are bounded depth-1 structural diagnostics, not reproductions of the complete C-C15 configurations.

## 4. Builder-ready contracts and fixture choices

The two contestable choices are explicit: same-key wrapping is required, and adversary enrollment means compromised-channel evidence only, separately for each case. Their alternatives and consequences are stated. I do not reverse either choice. (`P:65–67`, `P:1432–1454`.)

C-C7(ii)’s expanded failed set, C-C6/C-C7(i)’s recorded controls, and C-C15(i)’s corrected transplant losses are carried into their three-set specifications. I found no further demonstrated contradiction attributable to those choices. (`P:1141–1142`, `P:1731`.)

Findings **1–2** still require registration changes: the identity observed by the scope consumer, and the witness exception for C-C11’s alternative.

## 5. Routed and hidden choices

The **REFUSAL fork remains genuine**. Both options and costs are stated: exercise the foreign signing domain and add its test, or retain declared-and-unexercised status and leave that test unavailable. The freeze statement requires its resolution before the author’s commit. I leave it unresolved. (`P:1353–1380`; `formal/suite/lib/tessera_theory.pvl:66–76`.)

Neither finding should be silently settled as an encoding choice.

## 6. Accepted findings and carried-forward corrections

| Accepted finding | Verification |
|---|---|
| R1.1: D7 common-content consumer | Repaired: link 5 and C-C16. `P:374–382`, `P:1246`. |
| R1.2: C-C8 isolation contradiction | Repaired: possession-message and set-integrity obligations separated. `P:1770–1799`. |
| R1.3: C-C15 retained key-binding guarantees | Repaired. `P:1731`. |
| R1.4: C-Q6 composition join | Structural binding works; scope coverage remains incomplete under finding 1. `P:640–651`, `P:763–785`. |
| R1.5: one-key/one-manifest restriction | Repaired explicitly. `P:66`, `P:477–510`. |
| R1.6: every other choice determined | Withdrawn; choices exposed. `P:1390–1454`. |
| R2.1: E1 shadows C-C12 | Repaired and independently tested above. `P:640–725`. |
| R2.2: C-C15(i) retains C-Q7 | Repaired. `P:1731`. |
| R2.3: same-key wrapping unspecified | Explicit contestable choice; consequences recorded. `P:67`, `P:1141–1142`. |
| R2.4: enrollment unspecified | Explicit per-case contestable choice. `P:65`. |
| R3.1: projection loses layer | Repaired: `(aid, lyr)` and layer-preserving projection. `P:140–162`, `P:286–319`. |
| R3.2: no standing scope consumer | Key-scope consumer added and severable; identity component still missing—finding 1. `P:883–908`. |
| R3.3: mapping restores fingerprint precondition | Repaired; immutable terms separated from checks; C-C12 retains `kT = kX`. `P:703–714`, `P:754–769`. |
| R3.4: unsupported authorship generalization | Repaired against the recorded results. `P:1071`. |

All three ledger corrections are honoured: structural exact-byte verification without authorship overclaim, publication provenance as a correspondence, and fresh per-acceptance grouping now represented by `(aid, lyr)`. (`P:1018–1028`, `P:259–273`, `P:140–179`.)

**This registration is not ready to freeze. The author should see first: finding 1, the identity-only scope escape; finding 2, the terminal-unchecked alternative’s contradictory witness requirement; and the still-unresolved REFUSAL decision required before freezing. I found two supported defects, not a third to manufacture. The repaired structural join passes the requested independence and substitution controls.**

