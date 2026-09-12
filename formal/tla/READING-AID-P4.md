# Reading aid — P4_VerifierStates (fail-closed verifier state logic), Part A

**STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not adopted; the commit is the author's.**

*Repairs 2026-09-06 (skeptic findings on the TLA+ aids; applied by the AI
collaborator, PROPOSED):* "committed `.out`/result" wording corrected to
regenerated, uncommitted working-tree files (Model paragraph, vacuity
paragraph); Part B stated as not yet dispatched; Amendment 1 line cites
in checks rows 2–3 corrected to `:312–314` / `:314–317`; the `_Green`
cfg-vs-out witness (`c1` predicted, `c2` reported) explained. No
module, cfg or `.out` changed.

Testimony under `formal/suite/ENUMERATION.md` amendment note 5 item 2
(lines 297–312): a reading aid for non-expert readers, reviewed by the
lower-ceiling reader probe, **not a gate for exit**, never a verdict on
the proof. Nothing here changes a module, a cfg, or a `.out`.

**Model.** `formal/tla/P4_VerifierStates.tla` with `P4_VerifierStates.cfg`
(main, eleven invariants), `P4_VerifierStates_Sanity.cfg` (four vacuity
witnesses, run with `-continue`); companion
`P4_VerifierStates_Broken.tla` with `_Broken.cfg`, `_Broken_Green.cfg`
and `_Broken_Green2.cfg` (the last two added 2026-09-06). Line numbers
below are from the **current** working-tree text, after the fixes logged
in `formal/tla/falsification-2026-09-06/FIXES-2026-09-06.md`; every
`.out` in this family was regenerated against that text (FIXES log lines
26, 254–259). All `.out`, `_Green`
cfg/out pairs and archived runs cited below are uncommitted working-tree
files (`git status` 2026-09-06; the commit is the author's); "regenerated" below means "as regenerated in the
working tree".

**Provenance of the parts.** Part A (this file) is by the AI
collaborator (Claude, Fable 5.1), who knows what the names were meant to
stand for. Part B — the blind explanation by a non-author model of a
different family, given only the comment-stripped module, the cfgs, the
RESULT lines, and the registered text — is to be dispatched separately
and has not been dispatched as of 2026-09-06; it is not in this file;
where it disagrees with Part A, the disagreement is to be recorded at the top of this file, as `READING-AID-Q3.md` does. Probe
result: run 2026-09-06, twice; see the two paragraphs below (this sentence corrected in place 2026-09-06; the file is an uncommitted draft).

**Probe result (2026-09-06, `falsification-2026-09-06/P4/PROBE-haiku-2026-09-06.md`; PROPOSED, produced by the AI collaborator).**
A Haiku reader given only the stripped module got the four-branch
classification and all three boundaries right but bounded the claim to
no instance (never named the five-check configuration or the 1944
states), named the §A4.2-qualified unperformability sentence as the
sentence supported rather than Amendment 1 `:152–153`, attributed the
"required" qualifier to "the 2026-09-06 correction" rather than to
Amendment 4 §A4.2, and read `Init`'s `waived \in SUBSET Waivable` (line
79) as what keeps "the verdict logic" from collapsing. Given this aid it
got the instance and count, the registered sentence, the §A4.2
provenance, and the `Init` line right (reviewer 259). The aid did work;
it did not correct an inversion, because there was none. The one thing
the aided reader still asked is *why* exclusion-not-rejection matters,
which this aid states but does not explain. So, for the reader in a
hurry: **`Monotonicity`'s and `NoSilentPromotion`'s "under EVERY
policy" ranges over legal policies only. A policy that names a
non-waivable check is never in the enumeration, so what the verifier
does when handed one — reject it, normalise it, or obey it — is not
checked by this module (reviewer 219, 259).** No module, cfg or `.out`
changed.

**Probe result, run 2 (2026-09-06, same file, "Run 2" section; PROPOSED,
produced by the AI collaborator).** A second pair of fresh Haiku
contexts, the aided one reading this file with the paragraph above in
place. Stripped: four-branch classification and three boundaries right,
but no instance bound, no registered sentence named (it asked what
"registered sentence" means), the quantity called a verdict "over a
bundle" (none is represented), and the load-bearing line given as
`ASSUME NonWaivable \subseteq Checks` (line 64) rather than `Init`'s
`waived \in SUBSET Waivable` (79) — with the gloss that the logic
"depend[s] entirely on non-waivable checks", conflating non-waivable
with required (`VerdictFor` ranges over `Checks \ W`, 94–103; a
required waivable failure is `INVALID` too, 164–165). Aided: instance,
1944 count, Amendment 1 `:152–153`, line 79 with the
exclusion-not-rejection consequence, and three boundaries (mapping
unchecked; verdict derived not stored; illegal policy excluded not
validated) all right; one leftover gloss ("collapsing to vacuous
implication-checking") without operative effect. It reported the bold
sentence above as answering the why-question the run-1 aided reader
asked. The aid did work; nothing aided was wrong. No module, cfg or
`.out` changed.

**Registered text read against.** Amendment 1 P4
(`docs/phase-0-prereg-amendment-1.md:152–157`) and §A1.2.1 (`:304–327`);
Amendment 4 §A4.2 (`docs/phase-0-prereg-amendment-4.md:84–105`) — whose
own status line (`:3`) still reads "adopted in session, not yet signed"
while the file is committed at `5188e7a` and OTS-stamped at `5dfd82b`;
which governs is recorded as the author's call (module header 46–51;
FIXES log 142–151). Review record:
`docs/reviews/2026-09-06-codex-tla-falsification-p4-p5p6-p5c.md`, items
1–7 (lines 54–101) and the verbatim reviewer output for P4 (lines
210–307). Item numbers below are that record's.

---

## Typing / idiom note (TLA+ and TLC as used in this family)

- **A state is an assignment of one value to every `VARIABLE`.** Here
  the variables are `status` and `waived` (line 72). Nothing else is in
  a state. The verdict is *derived* from them by an operator (105), not
  stored (header correction 38–39) — so "the verifier emitted the wrong
  verdict" is not a state this model can be in (reviewer 298).
- **`Init` says which states are initial; `Next` says how states
  change.** `Init` (77–79) admits every function from checks to statuses
  and every legal waiver set. `Next` (81) is `UNCHANGED`: nothing ever
  changes. TLC therefore enumerates every initial state and evaluates
  each invariant on each one. This is a **truth-table model**; the
  header calls the state machine "degenerate" (11–13). TLC reports a
  violation "by the initial state" with no trace (FIXES log 113–114).
- **An invariant is a predicate TLC requires to be true in every
  reachable state.** Green means no state of the *configured instance*
  falsifies it (reviewer 293). It is not a proof for other instances.
- **`CONSTANTS`** (62) are fixed by the cfg (main cfg 2–3). `c1..c5` are
  TLC *model values*: uninterpreted names, distinct from one another and
  nothing more.
- **Set idioms.** `[Checks -> Statuses]` (78) is the set of all functions
  from checks to statuses; `SUBSET Waivable` (79) is the powerset;
  `status[c]` reads one check's outcome; `Checks \ W` (94) is set
  difference; `\E` / `\A` are "there exists" / "for all".
- **`VerdictFor(W)` is parameterised by a waiver set** (96–103) so that
  `Monotonicity` and `NoSilentPromotion` can say `\A W \in SUBSET
  Waivable` — "under EVERY legal policy for this one status assignment"
  (comment 84–86). `Verdict` (105) is the same function at the state's
  own `waived`.
- **`=>` is implication; `<=>` is if-and-only-if.** The seven one-way
  invariants (113–150) would all pass an over-conservative verdict
  function (everything `INVALID`); the four `Exact*` formulas (164–175)
  pin both directions (comment 153–158).
- **A sanity witness is a deliberately false assertion.** `VerdictNeverX
  == Verdict # "X"` (185–188). The `_Sanity` cfg is run with `-continue`
  so TLC keeps going after a violation; **a violation is the healthy
  result** — it exhibits a reachable state carrying that verdict, so the
  implication-shaped invariants are not true merely because their
  antecedents never occur (comment 178–183; Sanity cfg 1–4). TLC reports
  only the first failing invariant per state, so per-witness counts are
  first-violation-per-state (FIXES log 52).
- **A `_Broken` companion** is the same enumeration with a deliberate
  defect — here a `VerdictFor` with no unperformable branch, the classic
  fail-open bug (`_Broken.tla` 36–43). It must go **red** on a named
  invariant. It discharges nothing about P4; it shows that the checking
  arrangement can detect the intended failure (`formal/suite/s-p3/RESULTS.md`,
  "On companions"). TLC stops at the first violation it meets, so a red
  run certifies nothing about the other configured invariants (item 4).
- **A `_Green` isolation cfg** re-runs the broken module with the red
  invariant removed. Green isolates the break to that invariant among
  the checked set; red means the defect turns more than one formula red
  and the run names which (`_Broken_Green.cfg` 1–8). For P4 the `_Green`
  went red on the invariant predicted in its cfg (9–12) — the cfg's
  prediction named `c1` unperformable; TLC reported `c2` first
  (`_Broken_Green.out:32–38`): the invariant prediction held, the
  specific state is scheduling-dependent — and `_Green2` removed the
  whole implicated set (`_Broken_Green2.cfg` 1–14; FIXES log row F1).

## Cast

Line numbers are `P4_VerifierStates.tla` unless a file is named.

| Name | What it is in the design (plain words) | Defined | Used |
|---|---|---|---|
| `Checks` | the abstract set of the verifier's individual checks — signature-verifies, manifest-evidence-validates, temporal-consistency, … (header 15–17) | 62; cfg 2 | 64, 66, 78, 94, 138, 172 |
| `NonWaivable` | the checks no policy may waive: §A1.2.1's non-waivable class (Amendment 1 `:309–313`) | 62; cfg 3 | 64, 66, 118, 125, 133 |
| `Waivable` | `Checks \ NonWaivable`: §A1.2.1's declared-redundancy class (`:319–323`) | 66 | 79, 119, 126, 143 |
| `Statuses` | `"pass"` performed-and-passed; `"fail"` performed-and-failed; `"unperformable"` could not be performed (§4.6's two distinct answers, `docs/phase-0-prereg.md:555–562`) | 68 | 78 |
| `Verdicts` | the four P4 states | 70 | 113 |
| `c1 … c5` | model values. Item 3's disposition assigns the reading: `c1`, `c2` stand for the non-waivable class (five registered categories, `:309–313`); `c3`–`c5` for the three waivable categories (`:319–323`). The invariants do not depend on the count (review 82–84). **This mapping is a reading, not a checked correspondence** (reviewer 237). | cfg 2–3 | — |
| `status` | the outcome of every check; chosen freely by `Init`. The "adversary" of this model is any status assignment whatever (reviewer 297) | 72; 78 | 97, 99, 118, 125, 133, 138, 149–150, 160–162, 172 |
| `waived` | the verifier's **declared policy**: the set of checks it waives; `{}` is strict (header 18–19). Only legal policies exist: a policy naming a non-waivable check is excluded by `Init`, not rejected by a check (comment 74–76; reviewer 259) | 72; 79 | 105, 143, 149–150, 160–162, 172, 175 |
| `Init` | every status assignment × every legal policy | 77–79 | cfg 5 |
| `Next` | stutter — nothing changes | 81 | cfg 6 |
| `RequiredUnder(W)` | the checks policy `W` still requires: `Checks \ W` | 94 | 97, 99, 149–150, 160–162 |
| `VerdictFor(W)` | **the verdict function**: a required check failed → `INVALID`; else a required check unperformable → `UNVERIFIABLE`; else nothing waived → `VALID_STRICT`; else `VALID_DEGRADED`. The FAIL-over-UNPERFORMABLE precedence is Amendment 4 §A4.2 "Precedence — RULED (author)" (`amendment-4.md:86–94`), cited at 90–92 | 96–103 | 105, 119, 127 |
| `Verdict` | the state's own verdict, `VerdictFor(waived)` | 105 | 113, 132, 138, 143, 148, 165, 168, 171, 175, 185–188 |
| `AnyRequiredFail`, `AnyRequiredUnperf`, `AllRequiredPass` | the three conditions the `Exact*` formulas are phrased in | 160–162 | 165, 168, 175 |
| `Partition` … `UnverifiableIsHonest` | the seven one-way invariants (checks table below) | 113, 117–119, 124–127, 131–133, 137–138, 142–143, 147–150 | cfg 9–15; `_Broken.cfg` 9–15 |
| `ExactInvalid` … `ExactDegraded` | the four two-way classification pins | 164–165, 167–168, 170–172, 174–175 | cfg 16–19 (not carried in `_Broken`, item 5) |
| `VerdictNeverStrict` … `VerdictNeverUnverifiable` | vacuity witnesses; violation is healthy | 185–188 | Sanity cfg 13–16 |
| `_Broken.VerdictFor` | the fail-open bug: an unperformable check is skipped, i.e. treated as pass | `_Broken.tla` 38–43 | `_Broken.tla` 45, 56–80 |

## Checks table

For each invariant: the registered sentence it is the checked form of
(the module's own comment plus the Amendment 1 line), what the
2026-09-06 review found it does **not** discharge, and how the fail-open
companion behaves against it. "Load-bearing for" names the sentence
whose only checked form in this module is this formula.

| # | Invariant (lines) | Registered sentence it discharges | What the review found it does NOT discharge | Companion behaviour |
|---|---|---|---|---|
| 1 | `Partition` (113) | "The verifier's four states partition all outcomes" (Amendment 1 `:152–153`; §4.6 `prereg.md:555–562`). Load-bearing for totality over the instance. | Checks membership of a derived scalar in four strings; "outcomes" are legal abstract status/policy assignments, not bundle outcomes or execution traces (reviewer 218). | Green in `_Broken_Green2` (`_Green2.out:35`; FIXES F1). |
| 2 | `Monotonicity` (117–119) | §A1.2.1 "A package failing any non-waivable check is `INVALID` under **every** policy — no degraded policy may promote it (*monotonicity*)" (`:312–314`). | Does not identify the registered non-waivable checks; never tests a policy that *attempts* to waive one — `Init` (79) excludes such policies, so rejection or normalisation of hostile policy input is untested (reviewer 219; attack 1, reviewer 259). | Green in `_Broken_Green2`. |
| 3 | `NoSilentPromotion` (124–127) | §A1.2.1 "A non-waivable check that *cannot be performed* yields `UNVERIFIABLE`, never any `VALID` state" (`:314–317`); P4's sentence as qualified by §A4.2 to "a **required** check" (header 52–58). | Not the unqualified P4 sentence (item 2, ROUTED → §A4.2); permits `INVALID` whenever its antecedent holds without itself requiring a simultaneous failure (reviewer 220). | **RED in `_Broken_Green`** — `c2 = "unperformable"`, `waived = {}`, broken function returns `VALID_STRICT` (`_Broken_Green.out:32–38`; predicted in the cfg, FIXES F1 — the cfg's prediction named `c1`; TLC reported `c2` first: the invariant prediction held, the specific state is scheduling-dependent). |
| 4 | `ValidNeedsNonWaivablePass` (131–133) | corollary of the two §A1.2.1 sentences above: any `VALID` verdict means every non-waivable check was performed and passed (comment 129–130). | A necessary-condition corollary only; does not distinguish `INVALID` from `UNVERIFIABLE`; does not establish that a check was performed correctly (reviewer 221). | Red on its own (`falsification-2026-09-06/P4/Broken_VNWP_alone`, FIXES F1); masked in `_Green` because every such state also fails `NoSilentPromotion`, listed first. |
| 5 | `StrictMeansEverything` (137–138) | `VALID_STRICT` ⇒ every check, not only the required ones, passed (comment 135–136, citing P4/§3.1). | The review found no supplied registered sentence defining strict validity as "everything passed"; the closest is the unperformable sentence (reviewer 222). Does not itself require an empty waiver set (that is `ExactStrict`). | **RED in `_Broken`** — `c5 = "unperformable"`, `waived = {}` (`_Broken.out:28–34`). |
| 6 | `DegradedNeedsExplicitWaiver` (142–143) | "`VALID_DEGRADED` arises only from an explicit, recorded policy within A1.2.1's waivable set, never as a default or a fallback" (`:155–157`). | "Explicit", "recorded", authorisation, default selection and fallback behaviour are absent — the state holds a waiver set, not a record (reviewer 223; item 3, Boundary). Nonemptiness is a formal interpretation the sentence does not state expressly (223). Cannot expose the fail-open defect (reviewer 251). | Green in `_Broken_Green2`. |
| 7 | `UnverifiableIsHonest` (147–150) | the converse of "A check that cannot be performed yields `UNVERIFIABLE`" (`:153–155`): `UNVERIFIABLE` only when some required check was unperformable and none failed. | Supplies the converse and the failure precedence; not the forward implication (reviewer 224). | **VACUOUS in `_Broken`** — the broken function never returns `UNVERIFIABLE` (`_Broken.tla` 52–53; reviewer 251; `_Green2.cfg` 12–14). |
| 8 | `ExactInvalid` (164–165) | "A required check that fails yields `INVALID`" (`:153`), strengthened to iff. | "Required" means exactly `Checks \ waived`; no other rejection cause exists to be excluded (reviewer 225). | Not carried in `_Broken` (item 5; `_Broken.tla` 48–51). |
| 9 | `ExactUnverifiable` (167–168) | the §A4.2-qualified sentence in iff form: `UNVERIFIABLE` iff no required failure and some required unperformable. | Not the literal unqualified sentence: attack 3 (`c1` unperformable, `c2` fail → `INVALID`) and attack 4 (`c5` unperformable and waived → `VALID_DEGRADED`) are representable and accepted (reviewer 263, 265) — both now written into the registered text by §A4.2 (`amendment-4.md:86–105`). | Not carried in `_Broken`. |
| 10 | `ExactStrict` (170–172) | `VALID_STRICT` iff `waived = {}` and every check passes. | The supplied registered text does not explicitly specify this biconditional (reviewer 227). | Not carried in `_Broken`. |
| 11 | `ExactDegraded` (174–175) | `VALID_DEGRADED` iff `waived # {}` and every required check passes; §A4.2 names this formula as implementing "explicit policies [may] waive declared redundancy whether or not the waived check could be performed" (`amendment-4.md:99–103`). | Omits recording and authorisation; allows waived checks any status; selects degraded when all checks passed but the waiver set is nonempty (reviewer 228, 299). | Not carried in `_Broken`. |

**Vacuity witnesses** (185–188). No registered sentence says each
verdict must be reachable (reviewer 232); their job is to guard the
implications above from vacuity. Regenerated result (working tree,
uncommitted as of 2026-09-06): all four fire, counts
1 / 63 / 1444 / 436 (first violation per state;
`P4_VerifierStates_Sanity.out`, 14,560 lines, unfiltered — FIXES log
33–36, 52). The reviewer notes (247) that `Monotonicity`'s antecedent —
a non-waivable *failure* — is not exhibited by a printed witness; it is
covered because the enumeration is exhaustive (1944 = 3^5 × 2^3).

**Registered obligations with no formula or representation** (reviewer
234–239; header correction 33–39): recording and authorisation of the
waiver (item 3); the concrete waiver-boundary mapping (item 3); "under
any trace" and default/fallback behaviour — there is no policy-selection
process, only `Init` and stutter; the literal unperformability
classification — now §A4.2.

## Finite instance

`Checks = {c1, c2, c3, c4, c5}`, `NonWaivable = {c1, c2}` (cfg 2–3).
3^5 status assignments × 2^3 legal waiver sets = **1944 distinct states**
(`P4_VerifierStates.out:34, 39`; reviewer 247). Main: green on all
eleven (`out:35`), 0 s. There is no *k* in this family; the instance is
"five abstract checks, two non-waivable" (header 32–33).

What the record says about generality: the result is exhaustive within
this instance and "not a demonstrated result for arbitrary set sizes or
the registered concrete check inventory" (reviewer 293); item 3's
disposition says the invariants do not depend on the count (review
83–84) — a reading claim, not a checked one. This aid adds no argument
of its own.

Runs in the current record (FIXES log 45–52, 115–123): main **green**
1944; `_Broken` **red** `StrictMeansEverything`; `_Broken_Green` **red**
`NoSilentPromotion` (predicted, F1); `Broken_VNWP_alone` **red**
`ValidNeedsNonWaivablePass`; `_Broken_Green2` **green** on `Partition`,
`Monotonicity`, `DegradedNeedsExplicitWaiver`, with
`UnverifiableIsHonest` vacuous. Net: the fail-open defect turns red
exactly the three formulas that speak about unperformable checks (FIXES
F1).

## Boundaries

From the review's **Boundary** dispositions and the header correction:

- **Item 3.** Recording of the waived set and the authorising policy is
  an H1a/Band 1 artifact (A3's refusal and verdict-record dispositions);
  the `c1..c5` mapping lives in this aid (cast table) and is not
  checked.
- **Item 7.** Bundles, replay, and key substitution are unrepresentable
  by design: P4 is the state logic; those are P1/P3/P7 and the symbolic
  suite. The seam is the coverage-map join **`Accept` ↔ P4 verdict
  partition** — every symbolic path that stops short of `event Accept`
  must land in `INVALID` or `UNVERIFIABLE` here, never a valid verdict
  (`ENUMERATION.md:404–416`, "Question 2 — RULED (author)", 2026-08-29;
  §4, lines 135–147: a cross-formalism join, never marked symbolically
  discharged).
- **Items 1 and 2** were ROUTED and are now Amendment 4 §A4.2 (header
  40–58), with the status-line caveat above.
- The verdict is derived, not emitted or stored: output corruption,
  stale-verdict reuse, and computed-vs-recorded mismatch are
  inexpressible (header 38–39; reviewer 298).
- Status values are unconstrained inputs, independent of evidence,
  check dependencies, or execution; `"pass"` stands in for the entire
  successful verification obligation (reviewer 294).
- Waived-check outcomes are ignored entirely (reviewer 299) —
  consistent with §A1.2.1 as read by §A4.2 (`amendment-4.md:99–101`).
- The adversary is reduced to status assignments; none of A1.3's
  capabilities has an object or an action here (reviewer 297).

## Plain-language statement (collaborator; cited; Part B pending)

*Claim.* Over every combination of five check outcomes and every legal
policy in the configured instance, the verdict function returns one of
the four P4 states; a failed required check is `INVALID`; an
unperformable required check is `UNVERIFIABLE`; `VALID_STRICT` needs
everything passed and nothing waived; `VALID_DEGRADED` needs a nonempty
legal waiver and every required check passed — eleven formulas, green
(`out:35`). The review's strongest defensible reading (reviewer 307):
the run reports no violation of eleven formulas over the configured
legal assignments; the sanity output witnesses all four verdicts; the
companion exposes one fail-open assignment — and, after the 2026-09-06
`_Green` runs, exactly three formulas detect the fail-open defect.

*Adversary.* Any status assignment plus any legal policy (reviewer 297).
No bytes, keys, or actions.

*Boundary.* What a check *is*, whether it was performed correctly, what
the waiver *records*, and every A1.3 capability live elsewhere (items 3,
7). The FAIL-over-UNPERFORMABLE precedence and the word "required" are
§A4.2's, not this module's.

---

# Part B — blind explanation (Codex CLI 0.153.3, model gpt-6-astra, 2026-09-06, verbatim)

> Written by a non-author model of a different family, jailed to the current modules, configurations, trimmed committed TLC outputs, the registered text, and Amendment 4 — no repository, results, or review access. Its English is evidence of what the modules *say*. Where it disagrees with Part A, the disagreement is a finding to disposition, not a defect to hide. Dispatch prompt archived at `formal/tla/falsification-2026-09-06/P4/PART-B-PROMPT.md`.

## Reading notes

- A **state** here is one assignment of outcomes to checks (`status`) together with one waiver set (`waived`); a **behaviour** is a sequence of states, but here it can only repeat its initial assignment forever. The verdict is calculated from that assignment, not stored as another variable. (`P4_VerifierStates.tla:72-81`, `P4_VerifierStates.tla:94-105`.)
- An `INVARIANT` is a condition TLC checks in every reachable state of the configured finite instance. The main configuration selects eleven conditions; its committed run reports completion with no error and 1,944 distinct states, not a proof for arbitrary numbers of checks. (`P4_VerifierStates.cfg:1-19`, `P4_VerifierStates.out.trimmed:38-44`.)
- This is a **truth-table model**: `Init` supplies all input combinations and `Next` only stutters (changes nothing). It checks classification for those combinations, not a verifier's execution, evaluation order, changing evidence, or recovery over time. (`P4_VerifierStates.tla:7-13`, `P4_VerifierStates.tla:77-81`, `P4_VerifierStates.tla:96-105`.)
- A **sanity/witness configuration** asserts that each verdict never occurs; a `VIOLATION` is healthy because it supplies an example of that verdict. All four appear in the committed sanity output, ruling out an empty verdict class, not every possible kind of vacuity. The final “No error” footer must be read alongside those violations and the configuration's `-continue` instruction. (`P4_VerifierStates_Sanity.cfg:1-16`, `P4_VerifierStates_Sanity.out.trimmed:1-17`, `P4_VerifierStates_Sanity.out.trimmed:93-99`.)
- A `_Broken` companion deliberately changes the classifier; a counterexample demonstrates that a selected invariant detects that defect. A `_Green` isolation configuration removes a detector and checks the remainder: its name does not promise success. Here `_Green` still fails; `_Green2` passes after three detectors are removed, with one remaining condition vacuous. (`P4_VerifierStates_Broken.tla:36-53`, `P4_VerifierStates_Broken_Green.cfg:3-12`, `P4_VerifierStates_Broken_Green.out.trimmed:35-41`, `P4_VerifierStates_Broken_Green2.cfg:5-14`, `P4_VerifierStates_Broken_Green2.out.trimmed:38-44`.)
- `CONSTANTS` fixes the check universe and its non-waivable subset for a run: five abstract names, with `c1` and `c2` non-waivable. Outcomes and legal waiver sets still range over all possibilities; these names do not identify concrete cryptographic checks. (`P4_VerifierStates.cfg:1-3`, `P4_VerifierStates.tla:66-79`, `P4_VerifierStates.tla:33-38`.)

## Cast

**The quantity being judged is `Verdict`**, the derived classification of supplied check outcomes under a supplied waiver set; no bundle is represented. Rows below cover locally declared variables, constants, and operators in both modules; a second definition/use citation identifies the broken copy. (`P4_VerifierStates.tla:33-39`, `P4_VerifierStates.tla:72-105`, `P4_VerifierStates_Broken.tla:26-45`.)

| Name | Plain design meaning | Defined at file:line | Used at file:line |
| --- | --- | --- | --- |
| `Checks` (constant) | Universe of abstract individual checks. | `P4_VerifierStates.tla:62`; `P4_VerifierStates_Broken.tla:16` | `P4_VerifierStates.tla:78,94`; `P4_VerifierStates_Broken.tla:29,34` |
| `NonWaivable` (constant) | Checks no legal policy may omit. | `P4_VerifierStates.tla:62`; `P4_VerifierStates_Broken.tla:16` | `P4_VerifierStates.tla:64-66,118`; `P4_VerifierStates_Broken.tla:18-20,59` |
| `c1`, `c2`, `c3`, `c4`, `c5` (configured model values) | Uninterpreted check identities; first two non-waivable, last three waivable; no concrete category mapping supplied. | `P4_VerifierStates.cfg:2-3`; `P4_VerifierStates_Broken.cfg:2-3` | `P4_VerifierStates.tla:66,78`; `P4_VerifierStates_Broken.tla:20,29` |
| `Waivable` | Check universe minus the mandatory core. | `P4_VerifierStates.tla:66`; `P4_VerifierStates_Broken.tla:20` | `P4_VerifierStates.tla:79,119,143`; `P4_VerifierStates_Broken.tla:30,60,75` |
| `Statuses` | Three input labels: pass, fail, unperformable. | `P4_VerifierStates.tla:68`; `P4_VerifierStates_Broken.tla:22` | `P4_VerifierStates.tla:78`; `P4_VerifierStates_Broken.tla:29` |
| `Verdicts` | Four permitted output labels: VALID_STRICT, VALID_DEGRADED, INVALID, UNVERIFIABLE. | `P4_VerifierStates.tla:70`; `P4_VerifierStates_Broken.tla:24` | `P4_VerifierStates.tla:113`; `P4_VerifierStates_Broken.tla:56` |
| `status` (variable) | Total map assigning one input label to every check. | `P4_VerifierStates.tla:72`; `P4_VerifierStates_Broken.tla:26` | `P4_VerifierStates.tla:78,97-99`; `P4_VerifierStates_Broken.tla:29,39` |
| `waived` (variable) | Policy abstracted to the set of omitted checks. | `P4_VerifierStates.tla:72`; `P4_VerifierStates_Broken.tla:26` | `P4_VerifierStates.tla:79,105`; `P4_VerifierStates_Broken.tla:30,45` |
| `Init` | Enumerate every status map paired with every legal waiver set. | `P4_VerifierStates.tla:77-79`; `P4_VerifierStates_Broken.tla:28-30` | `P4_VerifierStates.cfg:5`; `P4_VerifierStates_Broken.cfg:5` |
| `Next` | Repeat the same inputs without change. | `P4_VerifierStates.tla:81`; `P4_VerifierStates_Broken.tla:32` | `P4_VerifierStates.cfg:6`; `P4_VerifierStates_Broken.cfg:6` |
| `RequiredUnder(W)` | All checks except those waived by candidate policy `W`. | `P4_VerifierStates.tla:94`; `P4_VerifierStates_Broken.tla:34` | `P4_VerifierStates.tla:97-99,149-150`; `P4_VerifierStates_Broken.tla:39,79-80` |
| `VerdictFor(W)` | Classifier for a candidate waiver set: failure first, then unperformability, then strict/degraded success; broken copy omits unperformability. | `P4_VerifierStates.tla:96-103`; `P4_VerifierStates_Broken.tla:38-43` | `P4_VerifierStates.tla:105,119,127`; `P4_VerifierStates_Broken.tla:45,60,65` |
| `Verdict` | Classifier applied to the state's waiver set; the output being judged. | `P4_VerifierStates.tla:105`; `P4_VerifierStates_Broken.tla:45` | `P4_VerifierStates.tla:113,165-188`; `P4_VerifierStates_Broken.tla:56,68-80` |
| `Partition` | Output belongs to the four-label vocabulary. | `P4_VerifierStates.tla:113`; `P4_VerifierStates_Broken.tla:56` | `P4_VerifierStates.cfg:9`; `P4_VerifierStates_Broken.cfg:9` |
| `Monotonicity` | Non-waivable failure forces INVALID under every legal policy. | `P4_VerifierStates.tla:117-119`; `P4_VerifierStates_Broken.tla:58-60` | `P4_VerifierStates.cfg:10`; `P4_VerifierStates_Broken.cfg:10` |
| `NoSilentPromotion` | Non-waivable unperformability excludes either VALID label under every legal policy. | `P4_VerifierStates.tla:124-127`; `P4_VerifierStates_Broken.tla:62-65` | `P4_VerifierStates.cfg:11`; `P4_VerifierStates_Broken.cfg:11` |
| `ValidNeedsNonWaivablePass` | Either VALID label requires the mandatory core to pass. | `P4_VerifierStates.tla:131-133`; `P4_VerifierStates_Broken.tla:67-69` | `P4_VerifierStates.cfg:12`; `P4_VerifierStates_Broken.cfg:12` |
| `StrictMeansEverything` | Strict success implies every check passed. | `P4_VerifierStates.tla:137-138`; `P4_VerifierStates_Broken.tla:71-72` | `P4_VerifierStates.cfg:13`; `P4_VerifierStates_Broken.cfg:13` |
| `DegradedNeedsExplicitWaiver` | Degraded success requires a nonempty legal waiver set. | `P4_VerifierStates.tla:142-143`; `P4_VerifierStates_Broken.tla:74-75` | `P4_VerifierStates.cfg:14`; `P4_VerifierStates_Broken.cfg:14` |
| `UnverifiableIsHonest` | UNVERIFIABLE implies a required check is unperformable and no required check failed. | `P4_VerifierStates.tla:147-150`; `P4_VerifierStates_Broken.tla:77-80` | `P4_VerifierStates.cfg:15`; `P4_VerifierStates_Broken.cfg:15` |
| `AnyRequiredFail` | At least one currently required check failed. | `P4_VerifierStates.tla:160` | `P4_VerifierStates.tla:165,168` |
| `AnyRequiredUnperf` | At least one currently required check is unperformable. | `P4_VerifierStates.tla:161` | `P4_VerifierStates.tla:168` |
| `AllRequiredPass` | Every currently required check passed. | `P4_VerifierStates.tla:162` | `P4_VerifierStates.tla:175` |
| `ExactInvalid` | INVALID exactly when a required check failed. | `P4_VerifierStates.tla:164-165` | `P4_VerifierStates.cfg:16` |
| `ExactUnverifiable` | UNVERIFIABLE exactly when no required failure exists but required unperformability does. | `P4_VerifierStates.tla:167-168` | `P4_VerifierStates.cfg:17` |
| `ExactStrict` | VALID_STRICT exactly when nothing is waived and everything passes. | `P4_VerifierStates.tla:170-172` | `P4_VerifierStates.cfg:18` |
| `ExactDegraded` | VALID_DEGRADED exactly when something is waived and all required checks pass. | `P4_VerifierStates.tla:174-175` | `P4_VerifierStates.cfg:19` |
| `VerdictNeverStrict` | Deliberately deny the existence of strict success to obtain a witness. | `P4_VerifierStates.tla:185` | `P4_VerifierStates_Sanity.cfg:13` |
| `VerdictNeverDegraded` | Deliberately deny the existence of degraded success. | `P4_VerifierStates.tla:186` | `P4_VerifierStates_Sanity.cfg:14` |
| `VerdictNeverInvalid` | Deliberately deny the existence of INVALID. | `P4_VerifierStates.tla:187` | `P4_VerifierStates_Sanity.cfg:15` |
| `VerdictNeverUnverifiable` | Deliberately deny the existence of UNVERIFIABLE. | `P4_VerifierStates.tla:188` | `P4_VerifierStates_Sanity.cfg:16` |

`W` and `c` are local placeholders for a candidate waiver set and a check, not additional state or configured constants; `FiniteSets` is imported, but no operator specific to that library is used in either module's definitions. (`P4_VerifierStates.tla:60-188`, `P4_VerifierStates_Broken.tla:14-80`.)

## What each invariant checks

These are precisely the eleven selections in the main configuration; quoted fragments below retain the registered wording, with Amendment 4's qualification and precedence stated where needed. (`P4_VerifierStates.cfg:8-19`, `AMENDMENT-4.txt:86-105`.)

| Invariant and enforced claim | Corresponding registered sentence (quoted) | What it does not establish |
| --- | --- | --- |
| `Partition`: the derived output is one of four labels. (`P4_VerifierStates.tla:113`.) | “The verifier's four states partition all outcomes.” (`REGISTERED.txt:1-2`.) | Membership alone does not assign the right label or show every label occurs; exact classifiers and witnesses address those separately. (`P4_VerifierStates.tla:153-188`.) |
| `Monotonicity`: a failed non-waivable check means INVALID for every legal waiver set. (`P4_VerifierStates.tla:117-119`.) | “A package failing any non-waivable check is `INVALID` under **every** policy — no degraded policy may promote it”. (`REGISTERED.txt:16-18`.) | No general ordering theorem for every pair of policies; no check of policies attempting to waive the mandatory core, which initialization excludes. (`P4_VerifierStates.tla:79,117-119`.) |
| `NoSilentPromotion`: a non-waivable unperformable check excludes both VALID outputs under every legal policy. (`P4_VerifierStates.tla:124-127`.) | “A non-waivable check that *cannot be performed* yields `UNVERIFIABLE`, never any `VALID` state”. (`REGISTERED.txt:18-19`.) | Does not force UNVERIFIABLE if another required check fails; INVALID is permitted, as ratified. Nor does this formula itself cover an unwaived waivable check. (`P4_VerifierStates.tla:125-127`, `AMENDMENT-4.txt:86-94`.) |
| `ValidNeedsNonWaivablePass`: either VALID output implies every non-waivable check passed. (`P4_VerifierStates.tla:131-133`.) | “performed-and-failed → `INVALID`; unperformable → `UNVERIFIABLE`; neither is promotable.” (`REGISTERED.txt:20-21`.) | Does not validate the supplied pass labels against cryptographic evidence or require waived checks to pass. (`P4_VerifierStates.tla:33-39,78,133`.) |
| `StrictMeansEverything`: strict success implies every check passed. (`P4_VerifierStates.tla:137-138`.) | “A required check that fails yields `INVALID`.”; “A check that cannot be performed yields `UNVERIFIABLE`”. (`REGISTERED.txt:2-3`; required qualifier: `AMENDMENT-4.txt:96-105`.) | This one-way formula alone neither requires an empty waiver set nor guarantees strict success when all checks pass; `ExactStrict` adds the exact condition. (`P4_VerifierStates.tla:138,170-172`.) |
| `DegradedNeedsExplicitWaiver`: degraded success requires a nonempty subset of waivable checks. (`P4_VerifierStates.tla:142-143`.) | “`VALID_DEGRADED` arises only from an explicit, recorded policy within A1.2.1's waivable set, never as a default or a fallback.” (`REGISTERED.txt:4-5`.) | A set supplied as input is not evidence of authorization, consent, or a recorded policy; no recording artifact is modeled. (`P4_VerifierStates.tla:33-35,72-79`.) |
| `UnverifiableIsHonest`: UNVERIFIABLE requires an actual unperformable input among required checks, with no required failure. (`P4_VerifierStates.tla:147-150`.) | “A check that cannot be performed yields `UNVERIFIABLE` — never any `VALID` state, under any trace.” (`REGISTERED.txt:2-4`; qualified and ordered by `AMENDMENT-4.txt:86-105`.) | Checks only the reverse implication, and “actual” here means the supplied label, not an independently verified inability to perform a check. (`P4_VerifierStates.tla:78,148-150`.) |
| `ExactInvalid`: INVALID if and only if some required check failed. (`P4_VerifierStates.tla:160,164-165`.) | “A required check that fails yields `INVALID`.” (`REGISTERED.txt:2`.) | Does not implement the underlying checks; the reverse implication is a model classification commitment beyond this sentence's one-way wording. (`P4_VerifierStates.tla:78,153-165`.) |
| `ExactUnverifiable`: UNVERIFIABLE if and only if a required check is unperformable and none failed. (`P4_VerifierStates.tla:160-168`.) | “A check that cannot be performed yields `UNVERIFIABLE` — never any `VALID` state, under any trace.” (`REGISTERED.txt:2-4`.) | Not the unqualified original: waived unperformability need not prevent validity, and required failure takes precedence; no changing trace is explored. (`AMENDMENT-4.txt:86-105`, `P4_VerifierStates.tla:81`.) |
| `ExactStrict`: strict success if and only if the waiver set is empty and every check passed. (`P4_VerifierStates.tla:170-172`.) | “The verifier's four states partition all outcomes.”; degraded is “never as a default or a fallback.” (`REGISTERED.txt:1-5`.) | The supplied excerpt does not independently spell out this strict biconditional; this is the model's exact classification, not proof of concrete bundle validity. (`REGISTERED.txt:1-6`, `P4_VerifierStates.tla:33-39,170-172`.) |
| `ExactDegraded`: degraded success if and only if the waiver set is nonempty and every remaining check passed. (`P4_VerifierStates.tla:162,174-175`.) | “`VALID_DEGRADED` arises only from an explicit, recorded policy within A1.2.1's waivable set”; “where the remaining checks pass.” (`REGISTERED.txt:4-5,23-27`.) | No recording, concrete redundancy mapping, or requirement that a waived check failed: even all-pass inputs are degraded under a nonempty waiver set. (`P4_VerifierStates.tla:33-39,78-79,175`, `AMENDMENT-4.txt:96-103`.) |

## The claim

For the configured five-check instance and any legal waiver set, I can rely on this modeled classifier to return INVALID exactly for a required failure, otherwise UNVERIFIABLE for required unperformability, otherwise VALID_STRICT with no waivers or VALID_DEGRADED with waivers. (`P4_VerifierStates.cfg:1-3`, `P4_VerifierStates.tla:94-105,160-175`.)

The clean committed run checks all eleven configured formulas over 1,944 distinct states: three outcomes for each of five checks, times eight subsets of the three waivable checks, giving 3⁵ × 2³ = 1,944. Every state is initial and subsequent steps preserve it, so this is exhaustive finite classification coverage; the four exact formulas prevent both permissive and over-conservative misclassification. The output reports an empty queue and an optimistic fingerprint-collision estimate of 2.0E-13, rather than a deductive proof. (`P4_VerifierStates.cfg:1-19`, `P4_VerifierStates.tla:66-81,153-175`, `P4_VerifierStates.out.trimmed:38-45`.)

## The adversary and the abstraction

There is no adversary process. Interpreting unrestricted inputs adversarially, a challenger may choose any pass/fail/unperformable assignment and any subset of the three waivable checks, including combinations that real checks might not jointly produce; the model puts no cross-check constraints on those choices. It cannot alter the classifier, waive `c1` or `c2`, invent another input label, or change inputs after initialization. (`P4_VerifierStates.cfg:1-3`, `P4_VerifierStates.tla:64-105`.)

The load-bearing restrictions are **subset consistency** (`ASSUME NonWaivable` is a subset of `Checks`), **total three-valued inputs** (`Init` assigns every check a member of `Statuses`), and **legal-policy initialization** (`Init` admits only subsets of `Waivable`). The last restriction builds in non-waivability rather than testing rejection of an illegal policy; the fixed `Next` also assumes no later mutation. Treating input labels as faithful results and waiver sets as authorized policies is necessary to apply this classification to a real verifier, but those correspondences are not checked here. (`P4_VerifierStates.tla:64-81`, `P4_VerifierStates.tla:33-39`, `REGISTERED.txt:29-31`.)

## Why the broken companion fails

The single companion, `P4_VerifierStates_Broken.tla`, deletes the required-unperformable branch: absent a required failure it returns a VALID label, even when a required check cannot run. (`P4_VerifierStates_Broken.tla:36-45`.)

- The committed `_Broken` run reports **`StrictMeansEverything`** violated: nothing is waived, `c1`–`c4` pass, and `c5` is unperformable. The broken classifier therefore returns VALID_STRICT despite a required check not passing; the correct classifier would return UNVERIFIABLE. (`P4_VerifierStates_Broken.out.trimmed:31-37`, `P4_VerifierStates_Broken.tla:38-43,71-72`, `P4_VerifierStates.tla:97-103`.)
- `_Broken_Green` runs that same companion without `StrictMeansEverything`; it reports **`NoSilentPromotion`** violated with no waivers, `c2` unperformable, and all other checks passing. Thus the defect is not isolated to the first detector. (`P4_VerifierStates_Broken_Green.cfg:20-26`, `P4_VerifierStates_Broken_Green.out.trimmed:35-41`.)
- `_Broken_Green2` also removes `NoSilentPromotion` and `ValidNeedsNonWaivablePass`. The latter fails on the preceding assignment by direct evaluation, not by a separately reported TLC violation. Its four remaining invariants pass over 1,944 states; `UnverifiableIsHonest` passes vacuously because the broken classifier never returns UNVERIFIABLE. (`P4_VerifierStates_Broken.tla:38-43,67-80`, `P4_VerifierStates_Broken_Green2.cfg:5-26`, `P4_VerifierStates_Broken_Green2.out.trimmed:38-44`.)

Stale/overbroad comments: “Same invariants” means only the first seven, and `_Green2`'s “every formula” about unperformability is too broad because `UnverifiableIsHonest` remains vacuous; the nearby corrections disclose both limits. (`P4_VerifierStates_Broken.tla:47-53`, `P4_VerifierStates_Broken_Green2.cfg:4-14`.)

## What this result does not show

- No signature, canonical-byte, issuer-binding, framing, or temporal-anchor check is implemented; the five abstract identities have no supplied mapping to those registered categories. (`REGISTERED.txt:13-27`, `P4_VerifierStates.cfg:2-3`, `P4_VerifierStates.tla:33-39,78`.)
- No audit record stores the precise waived set or authorizing policy, and illegal waivers are excluded rather than rejected by a modeled validation path. (`REGISTERED.txt:29-31`, `P4_VerifierStates.tla:33-35,72-81`.)
- No attacker-driven bundle, key, replay, network, or changing-policy trace is explored, and no implementation conformance or arbitrary-size theorem follows from this finite run. (`P4_VerifierStates.tla:30-39,77-81`, `P4_VerifierStates.cfg:1-3`, `P4_VerifierStates.out.trimmed:38-44`.)
- The witness run shows each verdict can occur; the one broken classifier does not test every possible implementation defect, and it carries none of the four exact-classification invariants. (`P4_VerifierStates_Sanity.out.trimmed:1-17`, `P4_VerifierStates_Broken.tla:36-53`.)
- P4 does not establish the §A4.3 revocation rule: that section names `P5P6_TemporalRevocation.tla` and time quantities absent from this model's state. (`AMENDMENT-4.txt:107-119`, `P4_VerifierStates.tla:62-81`.)

## Correspondence to the registered text

The invariants support P4's four-way classification, required-failure rule, qualified unperformability rule, and nonempty legal-waiver requirement, together with the lattice's prohibition on promoting failed or unperformable non-waivable checks; they do not discharge the recording sentence or implement the named concrete checks. (`REGISTERED.txt:1-5,13-31`, `P4_VerifierStates.tla:113-175,33-39`.)
Amendment 4 §A4.2 adds **required** to P4's unperformability sentence and ratifies INVALID when required failure and unperformability coexist; §A4.3's separate repair adds **both anchor_time and declared_issue_time** to the post-revocation sentence for P5/P6, which P4 does not touch. (`AMENDMENT-4.txt:84-119`, `P4_VerifierStates.tla:72-105`.)
The supplied amendment retains a stale “DRAFT — adopted in session, not yet signed” header despite the task's signed-2026-09-06 provenance; this reading uses that supplied provenance and the operative §A4.2 ruling, without independently verifying a signature. (`AMENDMENT-4.txt:1-10,86-105`; the model also preserves a status caveat at `P4_VerifierStates.tla:47-51`.)
