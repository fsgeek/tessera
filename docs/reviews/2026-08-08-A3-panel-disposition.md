# A3 panel disposition record — 2026-08-08

Status: DRAFT (clerk-compiled; author adoption required)
Compiled by: Claude (warm to the 2026-08-07/08 sessions; clerk, not panelist)
Panel target: Amendment 3 as ratified at commit `c54d70d`

## Panel composition and method

Four reviewers, model-diverse and input-cold to the 2026-08-07 and
2026-08-08 authoring sessions, per §A3.11: DeepSeek, Gemini, Grok,
Kimi. Each received an identical prompt from the author together with
the original pre-registration and all three amendments:

> We are working on a design for an attestation service and have just
> completed the third amendment to the original preregistration. One
> of the requirements for approving the third amendment is to ensure
> we have cold reads of it. Would you be willing to read it and let me
> know if you see any fatal errors in the design? If there are no
> fatal errors, I'm open to suggestions on how to strengthen the
> design.

Review artifacts: `2026-08-08-A3-{deepseek,gemini,grok,kimi}-review.md`
in this directory.

## Headline, scoped

All four reviewers found **no fatal errors** and no triggering of the
A1.1 falsifier. Scope of that headline: this is a coherence and
design read of the registered prose by four cold models — not formal
verification (no model was run), not a human security audit, and the
shared no-fatal/strengthen structure of all four outputs mirrors the
shared prompt. The evidential weight sits in the specific findings,
several of which converge from independent directions.

Predeclared discipline applied (§A3.11): genuinely new issues in
scope; re-litigation of adopted dispositions is not.

## Dispositions

### 1. Killed by source (finder defects — recorded per the
falsification discipline; a reviewer's finding is not acted on until
the source agrees)

- **DeepSeek 3 (partial):** claims the spike's timebox is
  "unspecified in the amendment." Refuted: §A3.3 registers a
  per-query timebox declared before running with three named
  outcomes, and §A3.9 repeats it ("three-outcome timebox,
  predictions-first"). The surviving remainder of the finding
  (execution risk that equivalence queries blow up) is real and
  already the spike's declared purpose.
- **DeepSeek suggestion 1:** predictions registered before running is
  already in §A3.3 ("predictions registered before running"). The
  increment — numeric probabilities rather than qualitative
  predictions — is carried to the spike pre-registration as optional.
- **Kimi 4 (downgraded, then applied as clarification):** claims
  standing's waivability is unstated. The design already answers
  structurally — standing never enters the P4 verdict, so it is not
  in the waiver lattice — but a careful cold reader asking the
  question is itself evidence the text under-communicated. Disposed
  as a pre-sign clarification (below), not a defect.

### 2. Pre-sign repairs applied to the A3 draft (text-level; in the
working tree pending author sign-off)

- §A3.4 Designated Community declaration: reconstructability claim
  explicitly scoped to survivability claim 1 (Grok minor note).
- §A3.7.1: panel-driven clarification added — standing is reported,
  never waived; relying-party acceptance of `ABSENT`/`UNVERIFIABLE`
  standing is a recorded policy decision outside the verdict
  (Kimi 4, downgraded).
- §A3.10 category-(b) register: per-item status made explicit
  (ratified at `c54d70d`; no panel objection) (Grok minor note).
- §A3.11 author note: carried into the signed document unchanged
  (DeepSeek suggestion 5 — no edit required; recorded here so the
  disposition is visible).

### 3. Registered into the first-link mechanism-spike
pre-registration (see `formal/spike/FIRST-LINK-SPIKE.md`, DRAFT)

Convergent cluster — three reviewers independently pressured the same
joint: the spike's exit criteria are the load-bearing softness.

- **Kimi 3:** the spike must produce a formal **authority-relevance
  map** (which manifest fields are authority-relevant), else the
  two-worlds broken companion tests the implementation, not the
  property.
- **Grok medium-term 1:** the broken companion must genuinely
  exercise the first-link invariant (two authority-distinct manifests
  sharing evidence; consuming linkage query fails), and spike failure
  to produce such a companion is an **amendment trigger**, not a soft
  "mechanism still open."
- **DeepSeek suggestion 4:** the A1.3 "any subset of authority
  channels but not all" adversary capability is explicitly connected
  to the floor's proof obligation in the capstone ledger.
- **Kimi 1 + Grok 3 (standing):** the chosen standing-evidence
  mechanism is modeled in the symbolic suite before Band 0 exit; the
  design-space tension between abandoned-artifact-alone testability
  and A2.4's exactly-one-shipped-anchor rule is named as a spike
  question that the mechanism choice must resolve explicitly.
- **DeepSeek suggestion 3:** dead-project/standing tests record
  whether the abandoned artifact was presented with or without
  lineage context; the alone-case is the hard case.

### 4. Routed to the author (the one genuinely open decision from the
panel's content)

- **Kimi 2 — integrated adversarial lifecycle model.** One model in
  which the adversary drives issuance → wrapping → supersession →
  refusal → verification → tending, including a broken companion
  where a wrapper transplants standing from a valid inner artifact
  onto a forged outer artifact. No other reviewer saw this; the clerk
  assesses it as the panel's strongest single finding. Adopting it
  **expands the H0/Band 0 exit obligations** (cost: one additional
  model plus companions), which is an author decision, not a clerk
  disposition. Clerk recommendation: adopt as a Band 0 exit
  obligation; it is the composition check the capstone linkage query
  only approximates.

### 5. Docketed for Band 1 / build phase (see
`docs/band-1-docket.md`; out of A3's registration scope, parked with
attribution so nothing silently drops)

Gemini A (Lambda/local-GPG dual-signing execution model), Gemini C
(numeric-precision rejection at ingestion), Gemini strengthening 1
(SPV header segment in bundle), Gemini strengthening 3 (fixed-width
envelope encodings), DeepSeek 6 + Grok immediate 3 (refusal-residual:
precomputed commitment; declared maximum delivery/publication latency
T), DeepSeek suggestion 2 (tending visibility deadlines), Grok
medium-term 2 (header checkpoint/cumulative-work pinning — carried
A2.1 residual), Grok structural 1 (attested renewal-window
parameter), Grok structural 2 + Kimi 6 (renderer conformance vectors;
whether the signed report becomes the only relayable form), Kimi 5
(bundle-size budget for embedded specifications), Kimi 7 (minimal
tending-policy skeleton sized to the demonstration horizon), Grok
immediate 1 (embedded verification spec executable-in-principle —
interacts with the Designated Community claim; docketed with a note
that it may warrant registration rather than build-phase disposal).

### 6. Declined, with reasons on record

- **Gemini B (second half):** degrading an unknown DNSSEC root anchor
  to the repo anchor instead of `UNVERIFIABLE` would weaken a
  registered verdict boundary — precisely what the A1.1 falsifier
  exists to prevent. Declined. The first half (historical trust-anchor
  store versioned, decoupled, exportable) is consistent with A1.5 and
  docketed for Band 1.
- **Gemini strengthening 2:** re-sizing S and linking it to
  fee-bumping policy re-litigates A2.1's adopted working default
  (S = 24h, declared revisable by its own terms). Declined as an A3
  item; the operational half is noted in the Band 1 docket.

### 7. Undischarged panel-scope item — blocks signature

§A3.11 placed the **A3.7.3 bridge-finding disposition** (its pending
non-author review: confirm the prose repair matches what the bridge
model already checks) in panel scope. The dispatch prompt did not
include it, so no panelist discharged it; DeepSeek (8) and Grok
(minor 1) independently flagged it as still pending. Resolution: a
targeted follow-up to one cold reviewer with the repair text and the
bridge model artifacts. **Roster is the author's decision.** Until
discharged, A3 is not signable under its own predeclared plan.

## Addendum round — the A3.7.3 targeted dispatch (2026-08-08/09)

The author sent all four panelists a follow-up naming the undischarged
scope item (§7 above); responses are recorded under `# Addendum` in
each review file. Gemini's prompt context differed slightly (prior
unrelated questions in that thread).

**Discharge status.** Grok and Kimi performed the disposition review:
Grok validated outright with explicit residual checks (A2.2, clock
roles, A2.3 interaction, P9, A1.4 correspondence); Kimi validated with
tightenings. DeepSeek and Gemini did not perform the review — each
described a protocol for performing it (useful; folded below).

**Structural caveat, on the record.** None of the four reviewers was
given the TLA+ sources — the dispatch provided the prereg and
amendments only. Every addendum statement that "the bridge model's
Ship action already evaluates the full predicate" is therefore relayed
from A3's own prose — a checkmark relay on exactly the item under
review. The clerk (warm; not a substitute for non-author review)
verified the determinate facts directly against the model:

- `P5cP5P6_Bridge.tla` Ship (lines 171–178): guards are burial depth,
  `declared − ε ≤ anchor_ts`, `anchor_ts ≤ declared + δ`,
  `confirmed_ts ≤ declared + δ` — the three temporal conjuncts plus
  burial. No P1–P3. The module header registers exactly this scope.
- Consequence: **Kimi addendum finding 1 is CONFIRMED.** The A3.7.3
  prose ("full `VALID_STRICT` predicate") overstated both the model
  and the obligation. Repaired in-place, marked PANEL-DRIVEN, scoped
  to the three-conjunct temporal predicate; Grok's optional clarity
  sentence folded in scoped form.
- **DeepSeek's asked-for broken companion is CONFIRMED ABSENT.** The
  committed bridge companions are `_BrokenAnchorSubst`, `_BrokenPin`,
  `_BrokenWallClock` (wall-clock guard, no chain conjunct at all —
  the divergence class, not the specific finding). A
  conjunct-3-only Ship mutation does not exist. Registered in §A3.9
  (panel-driven additions) as a cheap Band 0 companion.
- Kimi addendum 2 (issuance-path conformance vector for the
  divergence case) and 4 (PROPERTIES.md pointer at the frozen A2.1
  entry) applied as §A3.9 additions. Kimi addendum 3 (falsification-
  style review prompt) is subsumed: the specific check it prescribes
  ("no trace in which Ship fires while conjunct 2 is violated") is
  discharged for the committed model by inspection of the guard, and
  the new broken companion makes it mechanical.

**Honest status of the A3.7.3 scope item.** The *disposition* has cold
non-author review (Grok, Kimi — logic-level, confirmed sound). The
*model-prose correspondence* has warm clerk verification with line
citations (above), re-checkable by anyone in under a minute, but no
cold reviewer has seen the TLA+ itself. Whether that combination
discharges §A3.11's intent, or whether one cold reviewer should
receive the 12-line Ship action plus the repaired sentence for a
five-minute confirmation, is the author's ruling. The clerk notes the
check is now mechanical either way.

## Clerk's summary

Panel survived: no fatal errors, two finder defects killed by source,
one clarification applied, the convergent findings registered where
they bind (the spike pre-registration), build-phase items parked
visibly, two declines recorded. The addendum round discharged the
A3.7.3 disposition review (Grok, Kimi), surfaced one confirmed
precision defect in the repair sentence itself (fixed, marked), and
identified one missing broken companion (registered).

## Author rulings (2026-08-09)

1. **A3.7.3: discharged.** Cold logic review (Grok, Kimi) + clerk
   source verification with line citations + the author's direct read
   of the 12-line Ship guard. A fifth-party confirmation of a
   mechanical containment fact was assessed as ceremony, not
   evidence; the author declined it on those grounds. The distinction
   applied: disposition logic (cold-reviewable, done), prose/model
   correspondence (a reading check, done at source), model
   correctness (discharged in Band 0 rounds; evidence is the
   committed `.out` files, which speak from the repository).
2. **Kimi finding 2: registered with an H1a-freeze trigger, not a
   Band 0 exit obligation.** Method: three-best-per-side plus forced
   low-probability tail search with halving and a look-change
   stopping rule (the author's perturbation family). Both chains
   produced look-changers: (against gate placement) the model
   consumes the spike's mechanism outputs, so gating H0 on it makes
   the gate hostage to its own process; (against optionality) the
   cheap targeted-companion alternative is a checkmark relay between
   models. Synthesis registered in §A3.9: mandatory, triggered on
   spike completion, green before H1a freeze; Phase 1a opens on
   unchanged H0 terms. Notably, the procedure reversed the clerk's
   own on-record recommendation (§4 above) — recorded as evidence of
   the method, not embarrassment; the reversal is the point.

**Nothing further blocks signature.** No finding from either round
seeds an Amendment 4. Path: author signs, commits, OTS-stamps —
adoption; then the first-link mechanism spike
(`formal/spike/FIRST-LINK-SPIKE.md`); then, per registration, the
integrated lifecycle model before H1a freeze.
