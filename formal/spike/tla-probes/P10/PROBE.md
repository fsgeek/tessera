# P10 manifest-authority TLA+ probe — declaration

**STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not
adopted; the commit is the author's.**

**Tier: design probe, NON-DISCHARGING**, under the 2026-08-29 ruling
(`docs/reviews/2026-08-29-design-probe-ruling.md`) and commissioned by
Amendment 4 §A4.1 (`docs/phase-0-prereg-amendment-4.md`, entered at
`5188e7a`): *"the collaborator builds TLA+ models of P9 and P10 on its
own schedule; a green result is not evidence and is not cited by any
tracker row; a red result or an unrepresentable-attack finding is a
finding to be dispositioned before exit."* Header rule, restated so no
reader can miss it: **green is not evidence; red or unrepresentable is
a finding to disposition before exit.** Nothing in this directory
changes any row of `formal/PROPERTIES.md`.

**Freeze.** This file was written before any `.tla`, `.cfg`, or `.out`
existed in this directory, in the collaborator's working order. The
design-probe tier freezes by committing order; here the declaration,
the models, and the results will land in one author commit, so the
committing order cannot attest the freeze — only the collaborator's
statement does. Post-freeze changes to questions or predictions are
divergences, recorded in `RESULTS-PROBE.md`, never refinements.

## What the probe is for

P10's `[model]` half is discharged on the symbolic leg (A4.1: first-link
Q1/Q3 both channel variants, S-P3 strict-mode Q1). What that leg does
not cover is named in `formal/spike/first-link/READING-AID-Q3.md`, Part
B, "What this result does not show": *no archive or time-anchor check
is modeled*, and *it does not address P10's degraded-mode policy or
waiver explanations; failed checks have no modeled degraded acceptance
path.* A4.1 names the gap exactly: **the state logic of two archived,
time-anchored authority evidences under §A1.2.1's explicit-policy
waiver lattice — which evidence was waived, how the degraded verdict
names it, and that a manifest naming a non-authorized key never reaches
`VALID_STRICT` when any proper subset of channels is adversary-
controlled.** P4's model (`formal/tla/P4_VerifierStates.tla`, `3c1cfff`)
covers the lattice generically over abstract checks `c1..c5`; this probe
covers P10's instance of it concretely.

Registered text the probe is read against:

- Amendment 1 P10 (lines 283–300): two independent, archived,
  time-anchored authority evidences plus a self-signature that *"is not
  authority evidence and is never counted as an authority channel"*;
  `VALID_STRICT` requires all external evidences plus possession;
  missing or partially-validating evidence degrades by A1.2.1, *"naming
  which authority evidence was waived and why — never silently."*
- Amendment 1 §A1.2.1 (lines 304–330): the lattice; waivable =
  *"accepting fewer than all external manifest-authority evidences
  (P10)"*; recording = *"the precise waived check set and the policy
  that authorized the waiver."*
- Amendment 1 §A1.5: the two channels; anchoring proves existence, not
  authority; the declared residuals (correlated control; trust-anchor
  recursion — the archived historical trust-anchor store).
- Amendment 1 §A1.3 items 1, 2, 5, 6: alter bytes; strip; craft and
  anchor anything; control any proper subset of channels.
- Amendment 3 §A3.2 items 1–3, 5: *fewer, but never zero*; unavailability
  is not waiver (all unperformable → `UNVERIFIABLE`, never
  `VALID_DEGRADED`); possession is chain-internal; no change to P4's
  partition.
- Amendment 4 §A4.2 (precedence ratified: required fail beats required
  unperformable; "required" qualifier) and §A4.6 (degraded mode hands
  the adjudicator the evidence of what could and could not be excluded).

## The model (declared shape)

One TLA+ module, `P10_ManifestAuthority`, a four-step state machine —
not P4's degenerate one-state enumeration, so that companions produce
readable traces of *how* a bad verdict was reached:

1. **Init — the world and the policy.** The adversary's control is
   fixed in two sets: `compIssue ⊆ {dns, repo}`, the channels it
   controls *at issue time*, and `compLater ⊆ {dns, repo}`, the
   channels it comes to control *after the issuance window* (the
   registrar lapsed, the repository host changed hands, the author is
   gone). The verifier's policy `waived` is fixed here too — before any
   bundle exists — which is P9 by construction (a declared policy,
   never one chosen after seeing the evidence). Legal policies are
   `waived ⊊ {dns, repo}`: A3.2 item 1's *never zero*. Possession is
   not a waivable check (it is absent from A1.2.1's exhaustive waivable
   list; A3.2 item 3 makes it chain-internal).
2. **Publish — what the bundle can carry.** Each channel's archived
   evidence is one of: `"absent"` (stripped, or the channel lapsed);
   an honest record (present, names the authorized key `kH`, anchored
   consistently with the issuance window, signature `valid` /
   `invalid` (bytes altered in the bundle, A1.3 item 1) /
   `unperformable` (historical trust anchor unrecoverable, A1.5's
   recursion residual)); and, **only if the adversary controlled the
   channel at issue time**, any record at all (names any key, anchored
   consistently or late); **only if it controls the channel later**,
   a record naming any key but anchored *late* — anchoring proves
   existence at a time (A1.3 item 5, A1.6), and a channel captured
   after the window cannot back-date its evidence. This constraint is
   the probe's idealization of the symbolic leg (an honest channel's
   evidence cannot be made to validate naming another key) and of the
   P5 leg (the anchor's time is what it says); both are consumed, not
   proved.
3. **Present — the manifest.** The presenter asserts a key `mkey ∈
   {kH, kA}` and a self-signature status `poss ∈ {pass, fail}`.
   Possession is free to the adversary (A1.3 item 3): it self-signs
   with `kA`, and an honest `kH` manifest replays with its honest
   self-signature; `fail` is a tampered manifest.
4. **Verify — the P4 join.** Each channel evidence is *observed* into
   one of six values — `absent`, `unperformable`, `invalid`,
   `anchor_late`, `names_other_key`, `would_pass` — and the observation
   is classified into P4's three statuses (`absent`/`unperformable` →
   `unperformable`; `invalid`/`anchor_late`/`names_other_key` → `fail`;
   `would_pass` → `pass`). Possession is its own check, non-waivable.
   The verdict is **P4's own `VerdictFor`**, obtained by `INSTANCE
   P4_VerifierStates` with `Checks ← {dns, repo, poss}`, `NonWaivable
   ← {poss}`, `status ← the derived status map`, `waived ← waived`
   (TLC run with `-DTLA-Library=formal/tla` so the committed P4 module
   is the one instantiated, not a copy). A `VALID_DEGRADED` verdict
   carries a **record**: the policy that authorized the waiver
   (`policy = waived`) and, for each waived channel, its observation —
   the "why" of P10's sentence, encoded as *what the verifier observed
   about the evidence it was told not to require*, so the adjudicator
   receives what could and could not be excluded (A4.6).

**The P4 join, stated explicitly (ENUMERATION §4 form).** Producer:
`formal/tla/P4_VerifierStates.tla` (`3c1cfff`), operator `VerdictFor`
and its eleven checked invariants. Consumer: this probe. Shared term:
the per-check status map `[dns, repo, poss → pass | fail |
unperformable]` — P4's abstract `c1..c5` made concrete (Codex P4
review item 3: `dns`, `repo` stand in the waivable class "fewer than all
external manifest-authority evidences"; `poss` in the non-waivable
class). What the probe adds and P4 does not have: how the status map is
*derived* from two archived, time-anchored evidences and one asserted
key; the never-zero policy restriction; the record. What the probe
consumes and does not re-prove: P4's partition, monotonicity,
no-silent-promotion, and the A4.2 precedence. P4's invariants are not
re-run here; if `INSTANCE` fails mechanically the fallback is a
transcription with the join carried in prose (Q8).

**Unrepresentable here, by design (assigned elsewhere):** multi-key
manifests (S-P3 Q5, symbolic); everything below the first link —
framed bytes, signatures, key binding (S-P1, S-P3, P8); the internals
of a DNSSEC chain or a git commit signature; δ/ε arithmetic (`late` is
a boolean abstraction of the A2.1 `confirmed_at` predicate, P5c's leg);
wrapper layers and per-layer quantification (A3.2 item 4, S-P7); the
contents of the historical trust-anchor store (A1.5 residual, H1a);
correlated control of both channels at issue time (A1.3 item 7, the
misissuance boundary — representable as `compIssue = {dns, repo}` and
deliberately *outside* the property's guard, so the boundary is
exhibited, not hidden).

## Companions (declared)

Each is the correct module with one marked mutation, produced by
substitution so the diff is exactly the mutation:

- **`_BrokenSilent`** — degrades without recording: the verdict is
  P4's, the record is empty. The P10 sentence's "never silently."
- **`_BrokenSelfCounted`** — the A1.5 circularity: the self-signature
  is a third authority channel and `VALID_STRICT` requires two of three
  to validate.
- **`_BrokenAnchorIgnored`** — the verifier does not check the
  evidence's anchor time (`anchor_late` observed as `would_pass`): the
  2106 attack — both channels captured *after* the window, fresh
  evidences naming `kA`.
- **`_BrokenAnyOne`** — the "at least one" misreading the Haiku reader
  made of Q3 (`READING-AID-Q3.md`, probe result): `VALID_STRICT` when
  either channel validates.

Companion runs use TLC `-continue` piped through
`scripts/filter-tlc-output.sh`, so the **whole** red set is observed
in one run and every invariant absent from the output held on every
state. This supersedes, for this probe, the `_Green` re-run pattern
(Codex P4 review item 4): it certifies the same thing more completely.

## Sanity witnesses (declared; run with `-continue`; VIOLATED is healthy)

`VerdictNever{Strict,Degraded,Invalid,Unverifiable}` (P4's four);
`DegradedNonAuthorizedUnreachable` (the registered waiver cost, Q5b —
`VALID_DEGRADED` with `kA`); `StrictNonAuthorizedUnreachable` (the
A1.5 boundary — its trace must show `compIssue = {dns, repo}`);
`LateEvidenceUnreachable`; one `WhyNever_<o>` per observation value
(six), each requiring a `VALID_DEGRADED` record naming a waived channel
with that observation; `UnverifiableViaAbsentUnreachable`;
`InvalidViaConflictUnreachable`; `DegradedWaivedFailUnreachable` (a
`VALID_DEGRADED` verdict coexisting with a waived evidence whose check
would have *failed* — the state on which the two registered readings in
Q3 diverge).

## Questions (frozen), with predictions

Rough probabilities. "As predicted" is not a virtue; the probe earns
its keep on the branches that are not predicted, and under A4.1 only a
red or an unrepresentable finding is actionable.

**Q1 — The P10 headline as state logic.** Invariant
`StrictNeedsAuthorizedKey`: `compIssue ≠ {dns, repo}` ∧ verdict =
`VALID_STRICT` ⇒ `mkey = kH` — with *no* guard on `compLater`, so both
channels captured later is inside the claim.
- Prediction: green (p ≈ 0.85). p ≈ 0.10 a red caused by my encoding
  of absent/unperformable evidence (a recut, recorded as such, not a
  finding). p ≈ 0.05 the trace shows a path the registered text does
  not exclude — a finding to disposition.

**Q2 — Naming: what "why" has to be.** Invariant `DegradedNamesWaived`:
every `VALID_DEGRADED` record carries `policy = waived ≠ {}` and, per
waived channel, an observation equal to what the verifier saw; and
`NeverSilent`: any channel not validating under a VALID verdict is in
the record.
- Prediction: green by construction (p ≈ 0.9). The content is not the
  green; it is the *six-valued* observation lattice the record needs,
  against P4's three statuses. P10's "why" is ambiguous between (i)
  the policy that authorized the waiver (A1.2.1's recording sentence)
  and (ii) the observed state of the waived evidence; the probe
  encodes both and predicts (p ≈ 0.7) that (ii) is what an
  adjudicator under A4.6 needs and that no registered text requires
  it — a specification gap to route, not a defect. Routed either way.

**Q3 — The conflict case: a waived evidence that validates and names
a different key.** Under the P4 join (waived checks are not consulted,
`ExactDegraded`), `VALID_DEGRADED` with `record.why[ch] =
names_other_key` is reachable. Under A3.2 item 2's second sentence
read literally (*"Evidence that is present and whose validation is
performed but fails yields INVALID"*), it is `INVALID`.
- Prediction: the correct (P4-joined) model reaches it (p ≈ 0.9,
  witness `WhyNever_names_other_key` violated; `DegradedWaivedFailUnreachable`
  violated). A reading variant `_A32Reading` (any present, performed,
  failing channel evidence → `INVALID`, waived or not) passes all main
  invariants **and** `DegradedWaivedFailUnreachable` as an invariant
  (p ≈ 0.8). The two readings differ on exactly the set {`VALID_DEGRADED`
  ∧ ∃ waived channel with status `fail`}. **This is the probe's
  expected finding**: the registered text admits two verdicts for one
  bundle state, and the choice is the author's (Q5b's registered cost
  under one reading; `INVALID` with the conflict surfaced under the
  other). Not decided here.

**Q4 — Time anchoring: the later capture.** With `compIssue = {}` and
`compLater = {dns, repo}`, is `VALID_STRICT` with `kA` reachable?
- Prediction: unreachable in the correct model (p ≈ 0.85; the late
  anchor fails both channel checks → `INVALID`); reachable in
  `_BrokenAnchorIgnored` (p ≈ 0.9). This is the one thing the probe
  can show that no symbolic model in the tree touches (READING-AID-Q3
  Part B, last bullet).

**Q5 — Never zero, and unavailability is not waiver.** Invariants
`NeverZero` (`VALID_DEGRADED` ⇒ some un-waived channel passes and
names `mkey`) and `UnavailabilityIsNotWaiver` (all channel checks
unperformable ⇒ no VALID verdict).
- Prediction: green (p ≈ 0.9), and *only because* Init restricts
  policies to `waived ⊊ Channels`. A1.2.1's own words ("fewer than
  all") admit zero; A3.2 item 1 tightens it. The probe records
  (p ≈ 0.95) that the tightening is load-bearing: relaxing Init to
  `waived ⊆ Channels` would make `NeverZero` red. Observation for the
  reading aid, not a finding — the text already says it.

**Q6 — Companions.** Predicted red sets (whole set, via `-continue`):
- `_BrokenSilent`: {`DegradedNamesWaived`, `NeverSilent`} (p ≈ 0.9).
- `_BrokenSelfCounted`: {`StrictNeedsAuthorizedKey`,
  `StrictMeansBothAgree`} (p ≈ 0.85); p ≈ 0.1 `NeverSilent` joins.
- `_BrokenAnchorIgnored`: {`StrictNeedsAuthorizedKey`} with a trace at
  `compIssue = {}`, `compLater = {dns, repo}` (p ≈ 0.8); p ≈ 0.15 the
  first-reported trace uses `compIssue ≠ {}` instead (the mutation is
  reachable by an easier path and TLC reports that one first) —
  recorded, and the later-capture trace is then exhibited by a
  dedicated witness. `StrictMeansBothAgree` joins because `anchor_late`
  ≠ `would_pass` in the invariant even when the verifier no longer
  looks (p ≈ 0.85).
- `_BrokenAnyOne`: {`StrictNeedsAuthorizedKey`, `StrictMeansBothAgree`,
  `NeverSilent`} (p ≈ 0.85).
- Every companion: `Partition` and the invariants outside its red set
  hold (p ≈ 0.8; p ≈ 0.2 one companion also reddens an invariant I did
  not list — recorded as a prediction miss, not a defect).

**Q7 — Sanity witnesses.** All declared witnesses fire (p ≈ 0.9).
p ≈ 0.1 one does not — most likely a `WhyNever_<o>` whose observation
cannot coexist with `VALID_DEGRADED` in the correct model, which would
itself be a fact about the lattice worth writing down.

**Q8 — The mechanical join.** `INSTANCE P4_VerifierStates` from
`formal/tla` via `-DTLA-Library` works in TLC 2.x here (smoke-tested
on a throwaway module before this file was written: 108 states, no
error).
- Prediction: works in the real module (p ≈ 0.85); p ≈ 0.15 a
  level-checking or substitution error forces transcription, in which
  case the join is stated in prose and the transcription is diffed
  against P4's text in `RESULTS-PROBE.md`.

## Three named outcomes (declared)

1. **Shape confirmed, one specification finding.** Q1/Q4/Q5/Q6/Q7 as
   predicted; Q3's divergence exhibited. Reading: no red on the
   correct model (green is not evidence); the Q3 reading question and
   the Q2 "why" question are routed for disposition before exit.
2. **Red on the correct model.** A trace reaching `VALID_STRICT` with
   `kA` under a proper subset, or a `VALID_DEGRADED` verdict that does
   not name its waiver. Reading: a finding to disposition before exit
   (A4.1); the trace is the artifact; disposition by trace inspection
   distinguishes encoding defect from registered-text gap.
3. **Unrepresentable.** A question the model cannot pose in the
   timebox. Reading: evidence about the probe; record and stop.

## Timebox and discipline

- Construction: one working session. Each TLC run: `timeout 300`
  (five minutes); a timeout is "mechanism failure, not property
  evidence", never a property claim.
- Every result in `RESULTS-PROBE.md` is labeled `PROBE —
  NON-DISCHARGING`. No tracker row cites this directory.
- Files: `P10_ManifestAuthority.tla/.cfg/.out`, `_Sanity.cfg/.out`
  (filtered), `_A32Reading.tla/.cfg/.out`, four `_Broken*.tla/.cfg/.out`
  (filtered). Run lines are recorded in `RESULTS-PROBE.md`.
- Amend-don't-rewrite from this file's first commit.

## Provenance

Collaborator-drafted (Claude, Fable 5.1) 2026-09-06, on the commission
in Amendment 4 §A4.1 (author, 2026-09-06). The question set and the
model shape are the collaborator's; the reading of A3.2 item 2 in Q3
is the collaborator's and is presented as a question, not a ruling.

## Post-run note 1 — 2026-09-06, same day (collaborator; amend-don't-rewrite; the frozen text above is unchanged)

Three things the run showed about this declaration, recorded here so
the declaration is not read as if it had been right:

1. **Q6's method claim was wrong.** "Companion runs use TLC `-continue`
   … so the whole red set is observed in one run and every invariant
   absent from the output held on every state" — false. TLC reports
   only the first violated invariant (in cfg order) for a given state,
   `-continue` or not; co-violated witnesses and companion invariants
   are never printed. The first sanity run showed four of sixteen
   witnesses for this reason. `run-probe.sh` runs one TLC run per
   invariant for the sanity and companion configurations; the `_Green`
   pattern was not "superseded", it was under-specified in both
   directions. Recut 3 in `RESULTS-PROBE.md`.
2. **Two encoding recuts before any result** (a string compared with a
   record; `>=` without `Naturals`). Neither touched a question.
3. **One companion prediction missed** (`_BrokenAnchorIgnored` did not
   redden `StrictMeansBothAgree`, because that invariant reads the
   verifier's own observation, which the mutation blinds). Recorded as
   O2 in `RESULTS-PROBE.md`; the lesson is about how to write
   companion-catching invariants, not about P10.

Everything else ran on its predicted branch. The two items the probe
exists to produce — R1 (two registered readings of one bundle state)
and R2 (which "why" P10 means) — are in `RESULTS-PROBE.md`, routed to
the author, decided by no one here.

## Post-run note 2 — 2026-09-06, same day, later (a second collaborator pass; amend-don't-rewrite; the frozen text above is unchanged)

A second collaborator instance, dispatched to build this probe, found
the directory already complete and instead verified it. Recorded before
the re-run so that the one new prediction below is registered first:

1. **Verification of the committed claims, done before any edit.** The
   `-continue` suppression that motivated recut 3 reproduces: a single
   `-continue` run of `_Sanity.cfg` reports exactly the four
   `VerdictNever*` witnesses (20 / 480 / 15,436 / 3,264 states) and none
   of the other twelve. Every red set in `RESULTS-PROBE.md`'s companion
   table matches the per-invariant `.out` sections positionally. The
   boundary trace (`compIssue = {dns, repo}`) and the Q3 conflict trace
   (`why = [dns |-> "names_other_key"]`) read as tabulated.
2. **A citation correction.** `RESULTS-PROBE.md` says P4 was
   instantiated at `3c1cfff`. The file actually parsed was the working
   tree's `formal/tla/P4_VerifierStates.tla`, which differs from
   `3c1cfff` by 37 uncommitted comment-only insertions (the 2026-09-06
   CORRECTION header); `VerdictFor` and every operator the join uses
   are textually identical. So the *semantics* cited are right and the
   *file identity* was not recorded. `run-probe.sh` now writes, at the
   top of every `.out`, the sha256 prefix of the P4 file it joined, the
   `HEAD` it ran under, and whether that file was clean or modified.
3. **O1 made reproducible (one new prediction).** The Q5 relaxation was
   a scratch run. It is now a committed reading variant,
   `P10_ManifestAuthority_A121Literal` (Init admits `waived =
   Channels`: A1.2.1's "fewer than all" without A3.2 item 1), run one
   invariant per TLC run. **Prediction (registered here, before the
   run):** red on exactly {`NeverZero`, `UnavailabilityIsNotWaiver`,
   `PossessionNeverAuthority`}; green on the other seven, in particular
   `StrictNeedsAuthorizedKey` and `DegradedNamesWaived` (p ≈ 0.9; the
   scratch run is the only reason the estimate is that high).
4. **Labelling.** The `.cfg` files and the `.out` headers now carry the
   STATUS line every file in this directory is required to carry; they
   did not. No `.tla` text changed. All `.out` files are regenerated by
   `./run-probe.sh` (run 4); the backup of run 3's outputs was diffed
   against run 4 modulo timestamps, seeds and pids, and the diff is
   reported in `RESULTS-PROBE.md`'s review log.

## Post-run note 3 — 2026-09-06, same day, later still (third collaborator pass, applying a skeptic's verified findings; amend-don't-rewrite; the frozen text above is unchanged)

**STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not
adopted; the commit is the author's.**

A skeptic reviewed this directory and returned verified findings
(three defects, five nits, one "verified, no change"). This note
records the divergences the Freeze paragraph requires and registers,
**before the re-run (run 5)**, every new prediction the fixes need.

1. **Three invariants were added at build time, after the freeze, and
   carry no frozen prediction — a divergence the Freeze paragraph
   required to be recorded and that post-run notes 1 and 2 did not
   record.** `LaterCaptureStrictUnreachable` (operationalizes Q4's
   prose — Q4 names no invariant), `PossessionNeverAuthority` (no
   frozen question at all; it is the A1.5-item-3 / A3.2-item-3 clause
   as an invariant) and `TypeOK` appear nowhere in the frozen text
   above; all three are checked on the correct model and every
   companion. Consequence for the record: `RESULTS-PROBE.md`'s
   companion table attributes to the freeze a `_BrokenAnchorIgnored`
   prediction — "{`StrictNeedsAuthorizedKey`, `StrictMeansBothAgree`} +
   `LaterCaptureStrictUnreachable`" — that Q6 does not contain. Q6
   actually predicts {`StrictNeedsAuthorizedKey`} with
   `StrictMeansBothAgree` joining (p ≈ 0.85) and speaks only of "a
   dedicated witness" as the fallback for the later-capture trace. The
   `LaterCaptureStrictUnreachable` red on that companion is therefore
   **observed but unpredicted**; the `PossessionNeverAuthority` greens
   on the correct model and the companions are unpredicted greens (and,
   under A4.1, not evidence either way). Post-run note 2 item 3's
   `_A121Literal` prediction *was* registered before its run and names
   `PossessionNeverAuthority` legitimately — that prediction stands.
   `make-companions.py`'s `_BrokenAnchorIgnored` banner carried the
   same misattribution and is corrected (comment text only).

2. **Q3's and R1's "exactly" is false; the divergence set is larger.**
   The frozen Q3 says the two readings "differ on exactly the set
   {`VALID_DEGRADED` ∧ ∃ waived channel with status `fail`}". The
   `_A32Reading` variant returns `INVALID` whenever *any* channel has
   status `fail`, waived or not, so it also differs from the P4 join
   where P4 says `UNVERIFIABLE`: a waived channel failing while a
   required channel is unperformable. The set on which the readings
   differ is {verdict ∈ {`VALID_DEGRADED`, `UNVERIFIABLE`} ∧ ∃ waived
   channel with status `fail`} (they agree on `INVALID`, and
   `VALID_STRICT` has no waived channel). Fix: a new witness in the
   correct module, `UnverifiableWaivedFailUnreachable == ~(V /\
   verdict = "UNVERIFIABLE" /\ \E ch \in waived : ChanStatus(ch) =
   "fail")`, added to `_Sanity.cfg` and to `_A32Reading.cfg`.
   **Prediction (registered here, before run 5):** violated in the
   correct model (trace shape: `waived = {repo}`, `repo` failing,
   `dns` absent or unperformable, verdict `UNVERIFIABLE`); holds in
   `_A32Reading`. p ≈ 0.95 for both — the skeptic ran the same witness
   in scratch and reported exactly this, which is the only reason the
   estimate is that high. The frozen Q3 text is unchanged; this is its
   correction.

3. **`_A32Reading`'s green had no vacuity check.** A variant that made
   every bundle `INVALID` would also be "green on all eleven". New
   configuration `P10_ManifestAuthority_A32Reading_Sanity.cfg`, run one
   witness per TLC run, carrying the sixteen `_Sanity.cfg` witnesses.
   **Prediction (registered here, before run 5):**
   - VIOLATED (healthy; the variant is not vacuous): the four
     `VerdictNever*`; `DegradedNonAuthorizedUnreachable` (the waiver
     cost survives the literal reading: waived channel `absent`, sole
     channel names `kA`); `StrictNonAuthorizedUnreachable` (boundary,
     `compIssue = Channels`); `LateEvidenceUnreachable` (late evidence
     is observed, then classified `INVALID`); `WhyNever_absent`,
     `WhyNever_unperformable`, `WhyNever_would_pass`;
     `UnverifiableViaAbsentUnreachable`; `InvalidViaConflictUnreachable`.
   - HOLD (the literal reading removes exactly these "why" values from
     any `VALID_DEGRADED` record, because each maps to status `fail`
     and the variant refuses before recording): `WhyNever_invalid`,
     `WhyNever_anchor_late`, `WhyNever_names_other_key`; and
     `DegradedWaivedFailUnreachable`, `UnverifiableWaivedFailUnreachable`
     (already in `_A32Reading.cfg` as invariants; listed again so one
     `.out` shows the whole picture).
   p ≈ 0.85 that every line lands as listed; the most likely miss is a
   `WhyNever_<o>` I have mis-sorted.

4. **R1 narrates one member of a three-member set.** Per waived
   channel the divergence set has three members — `invalid`,
   `anchor_late`, `names_other_key` — and the committed
   `DegradedWaivedFailUnreachable` trace (`_Sanity.out`) is the
   `invalid` one at `compIssue = {}`, `compLater = {}`: an adversary
   with no channel control who altered the bytes of the waived
   evidence in the bundle (A1.3 item 1). Under the literal reading that
   state is `INVALID`. Recorded as a dated amendment to R1 in
   `RESULTS-PROBE.md`; it changes what the author is asked to rule on.

5. **Amendment 4's standing.** The Tier paragraph above cites §A4.1 as
   the commission and §A4.2 as "ratified" without the caveat the P4
   module header carries: `docs/phase-0-prereg-amendment-4.md`'s own
   status line reads "DRAFT — adopted in session, not yet signed … becomes
   in force on the author's signing commit and OpenTimestamps stamp".
   **Amendment 4's own status line governs whether §A4.1/§A4.2 are in
   force.** Nothing in this directory depends on the difference except
   the word "commissioned".

6. **The freeze is statement-attested only, and item 1 is what that
   cannot detect.** The Freeze paragraph said so; item 1 shows the
   declared invariant set drifted from the checked one without a
   divergence note, which mtimes cannot catch (this file was appended
   after the run). If the author wants an attestable freeze, the frozen
   section would be committed in a commit preceding the `.tla`/`.cfg`/
   `.out` commit rather than in the one commit this file anticipates.
   Not applied here (the commit is the author's).

7. **Run 5.** Because the correct module gains an operator (item 2),
   every companion is regenerated by `make-companions.py` and every
   `.out` by `run-probe.sh`. Run 4's `.out` files are archived under
   `run4/` so the run 4 → run 5 diff is checkable, which post-run note
   2's run 3 → run 4 claim was not (skeptic's nit). Predicted: no
   verdict, red set or witness result changes anywhere except the
   additions above.
