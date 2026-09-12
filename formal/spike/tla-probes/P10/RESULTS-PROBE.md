# P10 manifest-authority TLA+ probe — predictions vs. observed

**STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not
adopted; the commit is the author's.**

**PROBE — NON-DISCHARGING.** Under Amendment 4 §A4.1 and the design-probe
tier (`docs/reviews/2026-08-29-design-probe-ruling.md`): *green is not
evidence* and is cited by no tracker row; *red or unrepresentable is a
finding to disposition before exit.* Nothing here changes any row of
`formal/PROPERTIES.md`. Questions and predictions were frozen in
`PROBE.md` before any model existed (collaborator's working order; see
PROBE.md "Freeze" for what that does and does not attest).

Run 2026-09-06, TLC (tla2tools.jar, OpenJDK 21.0.12), from
`formal/spike/tla-probes/P10/`, by `./run-probe.sh`, which reproduces
every `.out` from the committed `.tla`/`.cfg` files. P4's module was
instantiated from the tree, not copied: every run's log shows `Parsing
file /home/tony/projects/tessera/formal/tla/P4_VerifierStates.tla`. Every
TLC run terminated in ≤ 2 s against the 300 s box; no timeouts. State
space of every module: 62,448 states generated, 43,248 distinct, depth 4.

## Three recuts (encoding and tooling, not property), before any result

1. **`"absent"` as a string.** TLC refuses to compare a record with a
   non-record (`Attempted to check equality of record … with non-record
   "absent"`). Absent evidence is now one canonical record with
   `present = FALSE`. Nothing in the questions changed.
2. **`>=` needs `Naturals`.** `EXTENDS FiniteSets, Naturals`.
3. **`-continue` does not observe the whole red set — PROBE.md Q6's
   method claim was wrong.** TLC checks a state's invariants in cfg
   order and reports only the *first* one violated in that state, even
   under `-continue`; a witness or companion invariant that is
   co-violated with an earlier-listed one is never printed. The first
   `-continue` sanity run reported exactly the four `VerdictNever*`
   witnesses and none of the other twelve — all of which fire when run
   alone. `run-probe.sh` therefore runs **one TLC run per invariant**
   for the sanity witnesses and the companions, and the `.out` files
   are the concatenation of each run's evidentiary core. Recorded as a
   prediction/method miss against Q6's last paragraph, and as a caution
   for the tree: the same suppression applies to any multi-invariant
   `-continue` run, including the existing `_Sanity` runs under
   `formal/tla/` when several witnesses are satisfiable by one state
   (Codex P4 review item 4 named half of this; the per-state half is
   new). PROBE.md carries a dated note; its frozen text is unchanged.

## Predictions vs. observed

| Q | Predicted (frozen) | Observed | Outcome |
|---|---|---|---|
| Q1 headline | `StrictNeedsAuthorizedKey` green (p≈0.85) | **green.** Also green: `Partition`, `StrictMeansBothAgree`, `NeverZero`, `UnavailabilityIsNotWaiver`, `PossessionNeverAuthority`, `LaterCaptureStrictUnreachable`, `TypeOK`. | as predicted — **not evidence** (A4.1) |
| Q2 naming | `DegradedNamesWaived`, `NeverSilent` green by construction (p≈0.9); the six-valued "why" lattice is the content | **green;** all six `WhyNever_<o>` witnesses fire — every observation value appears in some `VALID_DEGRADED` record | as predicted; Q2 routed (finding R2 below) |
| Q3 conflict | correct model reaches `VALID_DEGRADED` with a waived `names_other_key` (p≈0.9); `_A32Reading` green incl. `DegradedWaivedFailUnreachable` as an invariant (p≈0.8) | **both as predicted.** `WhyNever_names_other_key` and `DegradedWaivedFailUnreachable` violated in the correct model; `_A32Reading` green on all eleven | as predicted; **finding R1** |
| Q4 later capture | unreachable in correct (p≈0.85); reachable in `_BrokenAnchorIgnored` (p≈0.9) | **as predicted.** `LaterCaptureStrictUnreachable` green in the correct model, violated in the companion with `compIssue = {}`, `compLater = {dns, repo}`, both evidences `anchor = "late"`, `mkey = kA`, `VALID_STRICT` | as predicted |
| Q5 never zero | green, and load-bearing only through `waived ⊊ Channels` (p≈0.95 that relaxing it reddens `NeverZero`) | **green; relaxation observed** (scratch, not committed): with `waived ∈ SUBSET Channels`, `NeverZero`, `UnavailabilityIsNotWaiver`, and `PossessionNeverAuthority` all go red on `waived = {dns, repo}`, verdict `VALID_DEGRADED` resting on the self-signature alone; `StrictNeedsAuthorizedKey` and `DegradedNamesWaived` stay green | as predicted; **observation O1** |
| Q6 companions | see below | see below | two branches taken, one miss |
| Q7 witnesses | all fire (p≈0.9) | **all sixteen fire** (once run one per TLC run; recut 3) | as predicted |
| Q8 join | `INSTANCE` works (p≈0.85) | **works.** `P4 == INSTANCE P4_VerifierStates WITH Checks <- Checks, NonWaivable <- {"poss"}, status <- status, waived <- waived`; verdict is `P4!Verdict` | as predicted |

**Companions (Q6), red set certified per invariant:**

| Companion (mutation, exact diff from the correct module) | Predicted red | Observed red | Note |
|---|---|---|---|
| `_BrokenSilent` — `RecordHere == NoRecord` | {`DegradedNamesWaived`, `NeverSilent`} | **{`DegradedNamesWaived`, `NeverSilent`}** | as predicted |
| `_BrokenSelfCounted` — `VALID_STRICT` if `waived = {}` and ≥ 2 of {dns pass, repo pass, self-sig pass} | {`StrictNeedsAuthorizedKey`, `StrictMeansBothAgree`}; p≈0.1 `NeverSilent` joins | **{`StrictNeedsAuthorizedKey`, `StrictMeansBothAgree`, `NeverSilent`}** | the declared 0.1 branch: `dns` absent, `repo` + self → strict, absent `dns` unnamed |
| `_BrokenAnchorIgnored` — the `anchor = "late"` branch removed from `Observe` | {`StrictNeedsAuthorizedKey`, `StrictMeansBothAgree`} + `LaterCaptureStrictUnreachable` | **{`StrictNeedsAuthorizedKey`, `LaterCaptureStrictUnreachable`}**; `StrictMeansBothAgree` **green** | **prediction miss** — see O2 |
| `_BrokenAnyOne` — `VALID_STRICT` if `waived = {}`, possession passes, and either channel passes | {`StrictNeedsAuthorizedKey`, `StrictMeansBothAgree`, `NeverSilent`} | **exactly that set** | as predicted |

In every companion `TypeOK`, `Partition`, `NeverZero`,
`UnavailabilityIsNotWaiver`, `PossessionNeverAuthority`, and
`DegradedNamesWaived` (except `_BrokenSilent`) held on every state.

**Outcome classification (declared vocabulary): outcome 1 — shape
confirmed, one specification finding (R1), with one routed
specification question (R2).** No red on the correct model.

## The traces that matter (from the committed `.out` files)

- **The A1.5 boundary, exhibited not hidden** (`_Sanity.out`,
  `StrictNonAuthorizedUnreachable`): `VALID_STRICT` with `mkey = kA`
  requires `compIssue = {dns, repo}` — both channels adversary-
  controlled *at issue time*, both evidences `names = kA`, `valid`,
  `consistent`. That is A1.3 item 7's misissuance boundary and A1.5's
  "tampering with both external channels, at or before issue time,
  consistently", as a TLC state.
- **The registered waiver cost** (`DegradedNonAuthorizedUnreachable`):
  `compIssue = {dns}`, `waived = {repo}`, `repo` absent, `dns` names
  `kA` → `VALID_DEGRADED` for `kA` with `record = [policy |-> {repo},
  why |-> [repo |-> "absent"]]`. First-link Q5b and the S-P3 F8 ruling,
  concretely: the verdict says it is degraded and says what was not
  there.
- **The Q3 conflict state** (`WhyNever_names_other_key`): `compIssue =
  {dns}`, `dns` names `kA`, `repo` names `kH`, `mkey = kH`, `waived =
  {dns}` → `VALID_DEGRADED` for the honest key with `why = [dns |->
  "names_other_key"]`. The mirror (waive the honest channel, accept
  `kA`) is the same lattice class. Under `_A32Reading` this state is
  `INVALID`.
- **The 2106 attack, in the companion only**
  (`_BrokenAnchorIgnored.out`, `LaterCaptureStrictUnreachable`):
  `compIssue = {}`, `compLater = {dns, repo}`, both evidences `names =
  kA`, `valid`, `anchor = "late"`, `mkey = kA` → `VALID_STRICT`. In the
  correct model the same bundle is `INVALID` (both required checks
  fail on the anchor).

## Findings and observations

**R1 — Two registered readings of one bundle state (route for
disposition before exit).** A `VALID_DEGRADED` verdict coexisting with
a *waived* channel evidence whose check would have **failed** —
present, validating, consistently anchored, naming a different key —
is reachable under the P4 join (P4's `ExactDegraded`: waived checks are
not consulted; A4.2 ratified P4 as modelled) and is `INVALID` under
A3 §A3.2 item 2's second sentence read literally (*"Evidence that is
present and whose validation is performed but fails yields
INVALID"*). Both modules pass every invariant this probe declares; the
difference is the classification of exactly the set {`VALID_DEGRADED`
∧ ∃ waived channel with status `fail`}, which `DegradedWaivedFailUnreachable`
witnesses (violated in the correct model, holds in `_A32Reading`).
A3.2 item 5 (*"no change to P4's partition … P4 remains correct but
incomplete by abstraction"*) leans toward the P4 reading, under which
the conflict is the registered waiver cost handed to the adjudicator
with `names_other_key` in the record (A4.6). The other reading makes
the verifier refuse rather than report. **This is not decided here.**
It is the kind of item A4.1 says a probe may surface: not a red, an
ambiguity in registered text that a concrete instance makes visible.
One sentence from the author settles it either way; the amendment
would be a precision repair in the A4.2 style.

**R2 — What "why" must contain (route; specification gap, not a
defect).** P10 requires the degraded verdict to name *"which authority
evidence was waived and why"*; A1.2.1's recording sentence names *"the
precise waived check set and the policy that authorized the waiver."*
These are two different "whys": the policy that permitted the waiver
versus what the verifier observed about the waived evidence. The probe
records both, and the observation needs six values (`absent`,
`unperformable`, `invalid`, `anchor_late`, `names_other_key`,
`would_pass`), not P4's three statuses — all six are reachable in
records. Under A4.6 (*"hand the adjudicator the evidence of what could
and could not be excluded"*) the observation is the load-bearing half:
an adjudicator told only "repo waived by policy P" cannot distinguish
a lapsed registrar from a conflicting publication. No registered text
requires the observation to be recorded, and P4's model carries no
record at all (Codex P4 review item 3: recording is an H1a/Band 1
artifact). Consequence if adopted: the verifier must **evaluate**
waived checks it does not **require** — P9-compatible (same inputs),
but a different verifier shape from "skip what is waived", and a
record-format obligation for H1a. Nothing changes until the author
says which "why" P10 means.

**O1 — The never-zero floor is a P10-instance constraint P4's generic
model does not have.** P4's `Init` admits `waived = Waivable` (waive
the whole waivable class); A3.2 item 1 tightens P10's instance to
*fewer, never zero*. The probe encodes the tightening in `Init` and
the scratch relaxation shows it is load-bearing for three invariants
at once: without it a `VALID_DEGRADED` verdict can rest on the
self-signature alone — precisely the circularity A1.5 rejects. The
headline (`StrictNeedsAuthorizedKey`) does not depend on it. For the
reading aid: A1.2.1's own words ("fewer than all") admit zero; A3.2
item 1 is where zero is excluded; a verifier built from A1.2.1 alone
would be wrong. Already registered; observed here.

**O2 — Companion prediction miss, a probe-construction lesson.**
`_BrokenAnchorIgnored` did not redden `StrictMeansBothAgree` because
that invariant is written in terms of the verifier's own `Observe`,
which the mutation also blinds: the invariant cannot see what the
verifier cannot see. `StrictNeedsAuthorizedKey`, written in ground
truth (`mkey`, `compIssue`), caught it. Rule for the tree: an
invariant meant to catch a verifier defect must be stated over the
world's state, never over the verifier's derived view. Not a defect in
any registered text.

**O3 — Possession's lattice class is implied, not stated.** A1.2.1's
non-waivable enumeration (five categories) does not list proof of
possession; the waivable list (three, exhaustive) does not either; it
is non-waivable by exclusion, and A3.2 item 3 makes it chain-internal.
The probe treats it as non-waivable and says so in its header. Reading-
aid material; no text needs to change.

**O4 — What the state machine added over P4, in one line each.** Time:
a channel captured after the window cannot back-date its evidence
(`I2`), and that is the whole difference between the boundary trace
and the 2106 trace. Derivation: P4's three statuses are computed from
six observations of two archived evidences and one asserted key.
Policy-before-bundle: `waived` is fixed in `Init` (P9 by
construction). Record: P4 has none.

## The P4 join, as run

Producer `formal/tla/P4_VerifierStates.tla` (`3c1cfff`), consumed by
`INSTANCE` with the shared term `status = [c ∈ {dns, repo, poss} ↦
pass | fail | unperformable]`; `NonWaivable = {poss}`. The probe
re-proves none of P4's eleven invariants; it checks `Partition` over
`P4!Verdicts` as a type witness only. Every reachable status/waiver
pair here is inside P4's `Init` enumeration (P4 admits all of
`SUBSET Waivable`; this probe admits a strict subset), so P4's checked
results cover every verdict computed here. The A4.2 precedence is
inherited unchanged: a required channel failing on `names_other_key`
beats a required channel `absent`.

## Boundaries of this evidence

n = 2 channels by A1.5; one asserted key; possession as a boolean;
`late` as a boolean abstraction of the A2.1 predicate; no bytes, no
signatures, no key binding, no wrapper layers, no DNSSEC/git internals,
no trust-anchor store contents. `I1`–`I4` are consumed idealizations
(symbolic leg, P5 leg, A1.3 item 3, P9), not results. Every green here
is about the checked abstraction under those idealizations and, per
A4.1, is not evidence for any tracker row. What the probe is *for* is
R1 and R2, which do not depend on any green.

## Files

`PROBE.md` (frozen declaration; dated post-run note appended);
`P10_ManifestAuthority.tla/.cfg/.out` (correct; single run);
`P10_ManifestAuthority_Sanity.cfg/.out` (sixteen witnesses, one run
each); `P10_ManifestAuthority_A32Reading.tla/.cfg/.out` (reading
variant; single run); `P10_ManifestAuthority_Broken{Silent,SelfCounted,
AnchorIgnored,AnyOne}.tla/.cfg/.out` (one run per invariant);
`make-companions.py` (generates the five variants from the correct
module by exact substitution; `diff` shows header plus one mutation);
`run-probe.sh` (reproduces every `.out`). The Q5 relaxation was a
scratch run and is not committed; it reproduces by replacing `Init`'s
`waived` conjunct with `waived \in SUBSET Channels`.

## Review log

- 2026-09-06 — PROBE.md written; modules built; run 1 failed on recuts
  1–2 (tooling); run 2 green/red as tabulated but with the sanity and
  companion runs under `-continue`, which suppressed twelve witnesses
  (recut 3); `run-probe.sh` written; run 3 is the committed evidence.
  Collaborator throughout; no author read; no cross-family review
  (none is owed: probe tier, non-discharging). R1 and R2 are routed to
  the author; O1–O4 are recorded for the reading aids.

## Addendum — 2026-09-06, same day, later (second collaborator pass; amend-don't-rewrite; the text above is unchanged)

**STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not
adopted; the commit is the author's. PROBE — NON-DISCHARGING.**

A second collaborator instance, dispatched under Amendment 4 §A4.1 to
build this probe, found the directory complete and verified it instead
(PROBE.md post-run note 2 registers what it intended to do, and the one
new prediction, before the re-run). What it found:

**Verification (before any edit).** Recut 3's claim reproduces: one
`-continue` run of `_Sanity.cfg` reports only `VerdictNeverStrict` (20
states), `VerdictNeverDegraded` (480), `VerdictNeverInvalid` (15,436),
`VerdictNeverUnverifiable` (3,264) — the other twelve witnesses are
co-violated with one of those in every state and are never printed.
Every red set in the companion table above matches the per-invariant
`.out` sections. The boundary trace and the Q3 conflict trace read as
tabulated.

**C1 — Citation correction: which P4 text the join used.** "P4's module
was instantiated from the tree … (`3c1cfff`)" above is right about the
semantics and wrong about the file identity. The parsed file was the
working tree's `formal/tla/P4_VerifierStates.tla`, which at run time
differed from `3c1cfff` by 37 *uncommitted, comment-only* insertions
(the 2026-09-06 CORRECTION header entered after the Codex TLA review);
`git diff` shows no non-comment line changed, so `VerdictFor`,
`Verdicts`, and everything the `INSTANCE` uses are `3c1cfff`'s text.
From run 4 on, every `.out` begins with a `### P4 join source:` line
giving the sha256 prefix of the P4 file joined, the `HEAD` the run was
made under, and `clean` / `modified-uncommitted` for that file. Run 4:
`sha256=9f5c551641f6627f HEAD=5dfd82b working-tree=modified-uncommitted`.
When the author commits the P4 header correction, the sha256 will
change and the `.out` files should be regenerated once so the line
reads `clean`; nothing else will move.

**O1, committed.** The Q5 relaxation is no longer scratch:
`P10_ManifestAuthority_A121Literal.tla/.cfg/.out` (generated by
`make-companions.py`, one substitution: `waived \in SUBSET Channels`;
A1.2.1's "fewer than all" without A3.2 item 1) was run one invariant
per TLC run. **Prediction (PROBE.md post-run note 2, registered before
the run): red on exactly {`NeverZero`, `UnavailabilityIsNotWaiver`,
`PossessionNeverAuthority`}, green on the other seven. Observed: exactly
that.** All three reds exhibit the same state: `waived = {dns, repo}`,
both evidences absent, `mkey = kH`, `poss = pass`, verdict
`VALID_DEGRADED`, `record = [policy |-> {dns, repo}, why |-> [dns |->
"absent", repo |-> "absent"]]` — a valid verdict resting on the
self-signature alone, the circularity A1.5 rejects, reached under
A1.2.1's own words. `StrictNeedsAuthorizedKey` and `DegradedNamesWaived`
stay green, as O1 said. State space 83,264 generated / 57,664 distinct
(the extra policy `{dns, repo}`), depth 4, ≤ 2 s per run. As
predicted; not evidence (A4.1); it makes O1 reproducible from the
committed files rather than from a sentence.

**O5 — The record carries one reason per waived channel, in a fixed
order (probe-encoding boundary of R2).** `Observe` returns the first
failing check in the order absent → unperformable → invalid →
anchor_late → names_other_key. A waived evidence that is late-anchored
*and* names another key is recorded as `anchor_late` only. R2's
"six-valued observation" is therefore a lower bound on what an
adjudicator under A4.6 would need; a record format that lists every
failed check per channel is the natural form, and the probe's does
not. This is a fact about the probe's encoding, not about any
registered text; it belongs with R2 when the author decides which "why"
P10 means.

**O6 — Honest evidence is never late here.** `HonestEv` produces only
`anchor = "consistent"`, so every `anchor_late` trace involves adversary
control of that channel. An honest publication whose anchor confirmed
late (the A2.4 situation, P5c's leg) would be classified identically
(`fail`) and is excluded from the fixture only to keep `I2`'s reading
clean. Availability, not safety; no question in PROBE.md depends on it.
Boundary, recorded.

**Labelling.** The `.cfg` files and `.out` headers now carry the STATUS
line; the `.tla` text is unchanged (the correct module byte-for-byte;
the companions regenerated from it by the same substitutions).

**Run 3 → run 4 diff (modulo tmp paths, timestamps, seeds, pids).** No
verdict, red set, or witness result changed. State-count lines differ
in violation runs (BFS with four workers stops nondeterministically
after the first violation); one witness (`VerdictNeverInvalid`) exhibits
a different state (`compLater = {}` for run 3's `{"dns"}`), equivalent
for that witness. Run 3's outputs are not archived (they reproduce from
the same `.tla`/`.cfg`; the only intended differences are the two
header lines).

### Review log (continued)

- 2026-09-06, later — second collaborator instance: verified recut 3's
  TLC claim and every tabulated red set; corrected the P4 citation
  (C1) and added the join-source provenance line to every `.out`;
  committed the O1 relaxation as `_A121Literal` with its prediction
  registered first (landed); recorded O5 (single-reason record) and O6
  (no honest-late evidence) as probe-encoding boundaries; labelled the
  `.cfg`/`.out` files; run 4 is the current evidence. No author read;
  no cross-family review (none owed at probe tier). R1 and R2 remain
  routed to the author, undecided here. C1 changes no result.

## Addendum 2 — 2026-09-06, same day, later still (third collaborator pass, applying a skeptic's verified findings; amend-don't-rewrite; every line above is unchanged)

**STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not
adopted; the commit is the author's. PROBE — NON-DISCHARGING.**

A skeptic (cross-family is not asserted; the review was dispatched by
the orchestrating session) read this directory against PROBE.md's
frozen text, the P4 module and A3.2, re-ran the models in scratch, and
returned three defects and five nits. All three defects and all five
nits are applied below; the predictions the fixes needed were
registered first in PROBE.md post-run note 3, and the re-run is
**run 5**. Nothing here is evidence for any tracker row (A4.1).

**Standing caveat for this file's header (skeptic's nit).** The header
above and PROBE.md's Tier paragraph cite Amendment 4 §A4.1 as the
commission and §A4.2 as "ratified". `docs/phase-0-prereg-amendment-4.md`'s
own status line reads "DRAFT — adopted in session, not yet signed …
becomes in force on the author's signing commit and OpenTimestamps
stamp". **Amendment 4's own status line governs whether §A4.1/§A4.2 are
in force.** The P4 module header carries this caveat; this directory did
not until now.

### C2 — Three invariants checked without a frozen prediction (divergence, unrecorded until now)

`LaterCaptureStrictUnreachable`, `PossessionNeverAuthority` and `TypeOK`
appear nowhere in PROBE.md's frozen text (the first operationalizes
Q4's prose, which names no invariant; the second has no frozen
question; the third is a type witness). All three were added at build
time and are checked on the correct model and every companion. PROBE.md's
Freeze paragraph required this to be recorded as a divergence; post-run
notes 1 and 2 did not. Consequences for the tables above:

- The companion table's `_BrokenAnchorIgnored` **"Predicted red" cell
  is wrong as attributed.** It reads "{`StrictNeedsAuthorizedKey`,
  `StrictMeansBothAgree`} + `LaterCaptureStrictUnreachable`". PROBE.md
  Q6 actually says: {`StrictNeedsAuthorizedKey`} with a trace at
  `compIssue = {}`, `compLater = {dns, repo}` (p ≈ 0.8), the later-
  capture trace otherwise "exhibited by a dedicated witness", and
  "`StrictMeansBothAgree` joins … (p ≈ 0.85)". Corrected row:

  | Companion | Predicted red (PROBE.md Q6, as frozen) | Observed red | Note |
  |---|---|---|---|
  | `_BrokenAnchorIgnored` | {`StrictNeedsAuthorizedKey`}; `StrictMeansBothAgree` joins (p≈0.85) | {`StrictNeedsAuthorizedKey`, `LaterCaptureStrictUnreachable`}; `StrictMeansBothAgree` green | `StrictMeansBothAgree` miss stands (O2); the `LaterCaptureStrictUnreachable` red is **observed but unpredicted** — it is the "dedicated witness" Q6 anticipated, added at build time, and it happened to fire on the first-reported trace |

- The Q1 row's "Also green: … `PossessionNeverAuthority`,
  `LaterCaptureStrictUnreachable`, `TypeOK`" and the sentence "In every
  companion `TypeOK`, … `PossessionNeverAuthority` … held" report
  **unpredicted greens** — under A4.1 not evidence in any case, but a
  reader should not take them for confirmed predictions. The
  `_A121Literal` prediction in PROBE.md post-run note 2 item 3 *does*
  name `PossessionNeverAuthority` and was registered before its run;
  that one stands as a prediction.
- `make-companions.py`'s `_BrokenAnchorIgnored` banner carried the same
  misattribution; corrected (comment text only, no mutation changed;
  the regenerated module's body diff from the correct module is still
  exactly the one marked line).

### C3 — The divergence set in Q3 and R1 is larger than "exactly {VALID_DEGRADED ∧ ∃ waived fail}"

PROBE.md Q3 (frozen) and R1 above both say the two readings "differ on
exactly the set {`VALID_DEGRADED` ∧ ∃ waived channel with status
`fail`}". False. `_A32Reading` returns `INVALID` whenever *any* channel
has status `fail`, waived or not; P4's `VerdictFor` returns
`UNVERIFIABLE` when no *required* check fails and some required check
is unperformable — so a bundle with a waived channel failing and the
required channel unperformable is `UNVERIFIABLE` under the P4 join and
`INVALID` under the literal reading. Both readings agree on `INVALID`
(a required fail is `INVALID` either way) and `VALID_STRICT` has no
waived channel. **The set on which the readings differ is {verdict ∈
{`VALID_DEGRADED`, `UNVERIFIABLE`} ∧ ∃ waived channel with status
`fail`}**; the `UNVERIFIABLE` half maps to `INVALID` — fail-closed to
fail-closed, so the safety story is unchanged, but the routed question
R1 misstated what the author is asked to rule on.

Fix, run 5: witness `UnverifiableWaivedFailUnreachable == ~(V /\
verdict = "UNVERIFIABLE" /\ \E ch \in waived : ChanStatus(ch) =
"fail")` added to the correct module (dated comment at the operator),
to `_Sanity.cfg` and to `_A32Reading.cfg`. **Prediction (PROBE.md
post-run note 3 item 2): violated in the correct model, holds in
`_A32Reading` (p ≈ 0.95 each). Observed: exactly that.** The correct
model's trace (`_Sanity.out`, section `UnverifiableWaivedFailUnreachable`):
`compIssue = {}`, `compLater = {}`, `waived = {repo}`, `dns` absent,
`repo` honest (`names = kH`, `valid`, `consistent`), `mkey = kA`,
`poss = pass` → `UNVERIFIABLE` with `record = NoRecord` (the waived
`repo` observes `names_other_key` against the asserted `kA`; the
required `dns` is unperformable). Under `_A32Reading` the same bundle
is `INVALID` (`_A32Reading.out`: green on all twelve invariants, the
new one included; `_A32Reading_Sanity.out`: `UnverifiableWaivedFailUnreachable`
holds).

### R1, amended — the divergence set has three members per waived channel, and the trace on record is the one R1 did not narrate

R1 above narrates the divergence as the `names_other_key` "conflict
case" — a waived evidence that is present, validating, consistently
anchored and names a different key. That is one of three members.
`ChanStatus(ch) = "fail"` holds for three observations: `invalid`,
`anchor_late`, `names_other_key`. And the trace TLC put on record for
`DegradedWaivedFailUnreachable` (`_Sanity.out`, run 4 and run 5 alike)
is the **`invalid`** member: `compIssue = {}`, `compLater = {}`, `waived
= {repo}`, `dns` honest and `would_pass`, `repo` honest with `sig =
invalid`, `mkey = kH`, verdict `VALID_DEGRADED`, `record = [policy |->
{repo}, why |-> [repo |-> "invalid"]]`. No channel is adversary-
controlled at any time; the adversary merely altered the bytes of the
waived evidence in the bundle (A1.3 item 1). Under the A3.2-literal
reading (`_A32Reading`) that state is `INVALID`.

The consequence R1 did not put in front of the author: **under the
literal reading, an A1.3-item-1 adversary — alter bytes, no channel
control — converts `VALID_DEGRADED` to `INVALID` on any degraded bundle
by tampering with the evidence the policy said not to require.** That
is an availability cost, not a safety cost (both verdicts are fail-
closed for the tampered evidence; the honest required channel still
validates); and the same reading turns the `UNVERIFIABLE` half of C3 to
`INVALID` on the same bytes-only move. So the R1 choice, restated with
all three members visible, is between: *(a)* the P4 join — evaluate
the waived evidence and **report** its state (`invalid` /
`anchor_late` / `names_other_key`) in the record, verdict unchanged by
it; and *(b)* the literal reading — let bundle tampering of, or
late/conflicting publication on, a non-required channel **refuse** the
bundle. The `anchor_late` member (channel captured after the window,
late-anchored evidence, waived) sits between them: adversary channel
control, but not at issue time. R1's routing is unchanged; its
statement of the set is corrected here. **Still not decided here.**

### Boundaries, one sentence added (skeptic's nit)

Q1's green follows in one step from `Producible` (`I1`, `I2`) and P4's
`ExactStrict`: `Producible(ch)` admits a present, valid, consistently
anchored evidence naming `kA` only when `ch ∈ compIssue`, and
`VALID_STRICT` needs both channels `would_pass`, so `compIssue ≠
Channels ⇒ mkey = kH` is immediate. **Q1's green checks that the
encoding is consistent; it is not a property result about P10**, and
PROBE.md's p ≈ 0.85 should be read as confidence in the encoding, not
in the design. (A4.1 already says every green here is non-evidence;
this says why this one could not have been otherwise.)

### `_A32Reading` vacuity witnesses (skeptic's nit; new in run 5)

The variant's load-bearing green (`DegradedWaivedFailUnreachable` holds)
was certified with no witness that the variant still reaches
`VALID_DEGRADED` at all; a variant returning `INVALID` for every bundle
would have been "green on all eleven" too. New
`P10_ManifestAuthority_A32Reading_Sanity.cfg`, seventeen formulas, one
TLC run each, predictions registered in PROBE.md post-run note 3 item 3.

| Witness on `_A32Reading` | Predicted | Observed |
|---|---|---|
| `VerdictNeverStrict`, `VerdictNeverDegraded`, `VerdictNeverInvalid`, `VerdictNeverUnverifiable` | VIOLATED | **VIOLATED** (all four verdicts reachable) |
| `DegradedNonAuthorizedUnreachable` (waiver cost) | VIOLATED | **VIOLATED** |
| `StrictNonAuthorizedUnreachable` (A1.5 boundary) | VIOLATED | **VIOLATED** |
| `LateEvidenceUnreachable` | VIOLATED | **VIOLATED** |
| `WhyNever_absent`, `WhyNever_unperformable`, `WhyNever_would_pass` | VIOLATED | **VIOLATED** |
| `WhyNever_invalid`, `WhyNever_anchor_late`, `WhyNever_names_other_key` | HOLD | **HOLD** |
| `UnverifiableViaAbsentUnreachable`, `InvalidViaConflictUnreachable` | VIOLATED | **VIOLATED** |
| `DegradedWaivedFailUnreachable`, `UnverifiableWaivedFailUnreachable` | HOLD | **HOLD** |

All as predicted. Reading: the literal variant is not vacuous —
`VALID_DEGRADED`, the waiver cost and the three non-fail "why" values
survive it; what it removes is exactly the three `fail`-class "why"
values from any record, which is R1's set stated as witnesses.

### Run 3 → run 4 sentence, reworded (skeptic's nit)

"Run 3's outputs are not archived (they reproduce …)" in Addendum 1 is
**asserted by the collaborator; run 3's outputs were not retained, so
the claimed run 3 → run 4 no-change diff is not independently
verifiable.** Everything else in this directory reproduces from
committed files; that sentence does not. For run 5 the same mistake is
not repeated: run 4's `.out` files are archived unmodified under
`run4/` (with a `README.md` giving the diff recipe).

### Run 5 record

`./run-probe.sh`, 2026-09-06 19:32–19:33Z, HEAD `5dfd82b`, P4 join
source `sha256=9f5c551641f6627f working-tree=modified-uncommitted`
(unchanged from run 4). 86 TLC runs, every one "Finished in 00s" or
"01s" against the 300 s box; no timeouts. Changes to model text: the
correct module gains one operator (`UnverifiableWaivedFailUnreachable`)
and its dated comment; the six generated modules are regenerated
(`make-companions.py`; each body diff from the correct module is still
exactly one marked mutation, header aside); `_Sanity.cfg` and
`_A32Reading.cfg` gain the new formula; `_A32Reading_Sanity.cfg` is new;
`run-probe.sh` gains one `run_perinv` line. State space of the correct
model and every variant except `_A121Literal`: 62,448 generated / 43,248
distinct, depth 4 (unchanged).

**Run 4 → run 5 diff** (modulo tmp paths, timestamps, seeds, pids,
state-count lines, and the P4 join line, which is identical): the only
differences are *(i)* the new sections (`UnverifiableWaivedFailUnreachable`
in `_Sanity.out`; the whole of `_A32Reading_Sanity.out`); *(ii)* in
`_BrokenAnchorIgnored.out`, the `Publish`/`Present`/`Verify` line
numbers in trace headers shift by one because the corrected banner is
one line longer; *(iii)* a different first-reported violating state,
equivalent for the witness, in some violation runs (BFS with four
workers stops nondeterministically): `_Sanity.out` `VerdictNeverInvalid`,
`VerdictNeverUnverifiable`, `LateEvidenceUnreachable`, `WhyNever_would_pass`
and `UnverifiableViaAbsentUnreachable` show different `waived` /
`compLater` values; `_BrokenSelfCounted.out` `NeverSilent` shows
`compLater = {}` for run 4's `{"dns"}`; `_A121Literal.out`
`UnavailabilityIsNotWaiver` shows `mkey = "kA"` for run 4's `"kH"`.
**No verdict, red set, or hold/violated result changed anywhere.** The
reader can check this against `run4/`.

### Files (additions)

`P10_ManifestAuthority_A32Reading_Sanity.cfg/.out` (seventeen witnesses
on the reading variant, one run each); `run4/` (run 4's `.out` files,
unmodified, plus `README.md`). `PROBE.md` post-run note 3 registers the
divergences and the run-5 predictions.

### Review log (continued)

- 2026-09-06, later still — third collaborator instance, applying a
  skeptic's verified findings: recorded the three unfrozen invariants
  as a divergence and corrected the `_BrokenAnchorIgnored` prediction
  attribution (C2); corrected the Q3/R1 divergence set and added the
  `UnverifiableWaivedFailUnreachable` witness with its prediction
  registered first, landed (C3); amended R1 with the three-member set,
  the on-record `invalid` trace and the bytes-only availability
  consequence; added the Q1-is-definitional boundary sentence, the
  Amendment 4 status caveat, the `_A32Reading` vacuity witnesses (all
  seventeen as predicted), archived run 4, and reworded the
  unverifiable run 3 → run 4 sentence. Run 5 is the current evidence.
  No author read; the skeptic's review is the first review of this
  directory. R1 (as amended) and R2 remain routed to the author,
  undecided here.
