# Reading aid — P5P6_TemporalRevocation (temporal soundness and revocation, verifier side), Part A

**STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not adopted; the commit is the author's.**

*Repairs 2026-09-06 (skeptic findings on the TLA+ aids; applied by the AI
collaborator, PROPOSED):* "committed `.out`/red runs/sanity `.out`" wording
corrected to regenerated, uncommitted working-tree files; Part B stated
as not yet dispatched; "ratified 72 h / 24 h" reworded to the registered
maxima pending ratification at Band 0 exit (`amendment-1.md:182`); checks
row 5 no longer claims `_BrokenConf` certifies `ReceiptIndependence`;
`DeltaMax` cast cites and `_Sanity.out` count-line cites corrected. No
module, cfg or `.out` changed.

Testimony under `formal/suite/ENUMERATION.md` amendment note 5 item 2
(lines 297–312): a reading aid for non-expert readers, reviewed by the
lower-ceiling reader probe, **not a gate for exit**, never a verdict on
the proof. Nothing here changes a module, a cfg, or a `.out`.

**Model.** `formal/tla/P5P6_TemporalRevocation.tla` with
`P5P6_TemporalRevocation.cfg` (main, seven invariants),
`_Sanity.cfg` (four vacuity witnesses, `-continue`); companions
`_Broken.tla` (point-evaluated authorisation), `_BrokenConf.tla`
(pre-Amendment-2 verifier), `_BrokenTol.tla` (receipt enlarges
tolerances), `_BrokenTolStrict.tla` (receipt narrows tolerances), each
with its cfg; isolation cfgs `_BrokenConf_Green.cfg` and
`_BrokenTolStrict_Green.cfg` (added 2026-09-06). Line numbers are from
the **current** working-tree text after the fixes logged in
`formal/tla/falsification-2026-09-06/FIXES-2026-09-06.md`; every
`.out` in this family was regenerated against it (FIXES log 26,
254–261). All `.out`, `_Green`
cfg/out pairs and archived runs cited below are uncommitted working-tree
files (`git status` 2026-09-06; the commit is the author's); "regenerated" below means "as regenerated in the
working tree".

**Provenance of the parts.** Part A (this file) is by the AI
collaborator (Claude, Fable 5.1). Part B — the blind explanation by a
non-author model of a different family — is to be dispatched separately
and has not been dispatched as of 2026-09-06; it is not in this file;
disagreements are to be recorded at the top of this file, as `READING-AID-Q3.md` does. Probe result: run 2026-09-06, next paragraph (this sentence corrected in place 2026-09-06; the file is an uncommitted draft).

**Probe result (2026-09-06, `falsification-2026-09-06/P5P6/PROBE-haiku-2026-09-06.md`; PROPOSED, AI collaborator).**
A Haiku reader given the stripped module named `StrictAccept` and the
`signed <= anchor` line correctly but supplied as the registered
sentence "revoked material is never accepted" — which inverts Amendment
1 `:212` as written by §A4.3: material from a key revoked after both
`anchor_time` and `declared_issue_time` IS accepted; what is never
accepted is bytes **signed at or after** revocation (166–167). It also
fused the verifier's policy window with the global maxima (the item-8
distinction, checks rows 3 and 5), named no finite instance, and left
item 11 off its boundary list. Given this aid it got the registered
sentence, the 4,302,592-state instance, the item-8 division of labour,
the conditional-on-`signed <= anchor` reading (Plain-language statement, *Claim*) and item 11's
consequence right; three boundaries right. The aid did work, on the
claim and the boundary; the stripped reader's adversary was already
right, and its input evidently retained the module's comments (it
cites "Layer 2", the 2026-07-21 bridge, "lifecycle deferred"), so the
condition-1 baseline is weaker than a true comment-stripped one — the
next probe should archive the exact condition-1 input. Two sentences
the aided reader still wanted, added here for the reader in a hurry:
**the enumeration supplies `signed` too — every signing time from 0 to
`anchor` (109) — not only what the issuer writes into the receipt;**
and **no parameter-independence argument for this instance exists
anywhere in the record** (Finite instance, last sentence; Part B, last bullet of "What this result does not show"), not only in this aid —
the bridge (`P5cP5P6_Bridge.tla`) is a different check, not a
parameterisation of this one.

**Probe result, run 2 (2026-09-06, same file, "Run 2" section; PROPOSED, AI collaborator).**
A second Haiku pair, the aided reader reading this file at its current
line numbers. The stripped reader kept the item-8 distinction this
time but gave four invariants for the cfg's seven (no
`ReceiptIndependence`, `AbandonedArtifactRejected`,
`HonestCostIsExactlyTheWindow` in the claim), named no instance and no
registered sentence, and its relying-party revocation clause ("no
revocation before both declared and the anchor") fails the §A4.3 case
(item 10) that `AuthorizedThroughWindow` (147–149) handles; item 11
was again off its boundary list, present only as its closing
question. The aided reader gave the seven-invariant content, the
4,302,592-state instance, item 11 with its consequence, and three
boundaries right (items 13, 14; Part B 395) — the aid did work on the
claim and the boundary and did not discriminate on the adversary,
where both readers had line 109 and the stripped input again carried
the comments (still not archived). Two errors in the aided answer are
this aid's to fix, neither applied here: **(a)** it wrote "revoked
*strictly* between declaration and anchor" for the honest cost; the
interval is `(declared, anchor]` (comment 235–239; checks row 7), and
the *Claim* below says "between declaration and anchor" without the
bracket — the sentence should carry it; **(b)** it again omitted
`signed` from what the enumeration supplies, and attributed the
`Init` constraint to `declared`/`anchor`/`confirmedAt` instead — the
bold sentence in the paragraph above was not where the reader looked
(Cast, Boundaries, Part B), so it belongs in the `signed` cast row
and the *Adversary* paragraph, not only here. It also called
the *Claim* paragraph "registered"; it is the collaborator's
statement, and the registered sentences are the checks table's third
column.

**Registered text read against.** Amendment 1 P5
(`docs/phase-0-prereg-amendment-1.md:159–197`), P6 (`:199–230`), A1.6
(`:477–510`); Amendment 2 §A2.1 (`docs/phase-0-prereg-amendment-2.md:78–217`)
and §A2.2 (`:218–250`); Amendment 4 §A4.3
(`docs/phase-0-prereg-amendment-4.md:107–119`; status caveat as in the
P4 aid). Review record:
`docs/reviews/2026-09-06-codex-tla-falsification-p4-p5p6-p5c.md`, items
8–14 (lines 105–145) and the verbatim reviewer output for P5P6 (lines
308–454). Item numbers below are that record's.

---

## Typing / idiom note

- **A state is an assignment to the nine `VARIABLES`** (98–99). `Init`
  (105–114) admits every combination of small integers the constants
  permit, with one constraint: `signed \in 0..anchor` (109). `Next`
  (116–117) is `UNCHANGED`. So, like P4, this is a **truth-table
  model**: TLC enumerates every initial state and checks the invariants
  on each; violations are reported "by the initial state" with no trace.
  The narrative actions the comments describe — sign, revoke, anchor,
  confirm — are **not transitions**; only their end-state scalars are
  representable (reviewer 375).
- **The one constraint is the assumption.** `signed <= anchor` is A1.6's
  "the anchor is an upper bound on creation time" (`amendment-1.md:485–490`),
  imposed at `Init`, not checked by a verifier (reading guide 64–67).
  Everything `ForgeryRejected` proves rests on it (comment 163–165;
  item 11).
- **Observable vs. hidden.** `signed` exists so an invariant can
  quantify over what the verifier cannot see (61–63); the verifier's
  predicate `StrictAccept` (154) mentions `declared`, `anchor`,
  `confirmedAt`, `revoked`, `polDelta`, `polEps` only (86–87).
- **Time is small integers**; `DeltaMax`, `EpsilonMax` are scaled-down
  stand-ins for the registered 72 h / 24 h strict maxima (to be ratified
  or revised at Band 0 exit, `amendment-1.md:182`; the module header at
  53 says "ratified") — the model checks the *logic* of the window, not
  the magnitudes (52–54). `NoRev = MaxTime + 1`
  (96) is the sentinel "never revoked".
- **Parameterised predicates.** `TemporalOKWith(rd, re)` (135–138) takes
  the receipt-declared tolerances as arguments it deliberately ignores
  (133–134); `ReceiptIndependence` (219–221) then quantifies over all
  argument values and pins the ignoring. The `_BrokenTol` /
  `_BrokenTolStrict` companions route `rd`, `re` into the window via
  `Max` / `Min` (their lines 53, 58–61 / 50, 54–57).
- **Invariant, sanity witness, `_Broken`, `_Green`** — as in the P4 aid:
  an invariant must hold in every state; a witness (`XUnreachable ==
  ~(...)`, 251–262) is deliberately false and its **violation is the
  healthy result**; a companion goes red on a named invariant and
  discharges nothing of the property; a `_Green` cfg re-runs the
  companion with the red invariant removed to establish isolation among
  the checked set (item 4). TLC stops at its first violation, so the
  regenerated red runs (working tree, uncommitted as of 2026-09-06)
  "certified neither [other invariant] on its own"
  until the `_Green` runs (`_BrokenConf_Green.cfg` 6–7).
- **`_Sanity` ordering.** TLC reports only the first failing invariant
  per state; the cfg lists the most specific witness first so the broad
  one cannot mask it (Sanity cfg 5–7). The regenerated sanity `.out` (working
  tree, uncommitted) is elided through
  `falsification-2026-09-06/filter-tlc-initial-state.awk`
  (first violation per witness kept; counts in the file's note,
  `_Sanity.out:65–75`, counts at 71–74).

## Cast

Line numbers are `P5P6_TemporalRevocation.tla` unless a file is named.

| Name | What it is in the design (plain words) | Defined | Used |
|---|---|---|---|
| `MaxTime` | horizon of abstract time | 91; cfg 2 | 96, 106–110 |
| `DeltaMax` | stand-in for the strict δ maximum (72 h, `amendment-1.md:177–178`); the verifier may choose stricter, never larger (`:180–181`) | 91; cfg 3 | 94, 111, 184, 186 |
| `EpsilonMax` | stand-in for the strict ε maximum (24 h) | 91; cfg 4 | 112, 185 |
| `RcptTolMax` | bound on what a receipt may *declare*; `ASSUME RcptTolMax > DeltaMax` so receipts CAN overclaim (94) | 91; cfg 5 | 113–114, 220 |
| `NoRev` | "never revoked" sentinel, sorts after all times | 96 | 110 |
| `declared` | `declared_issue_time`: what the issuer claims — adversarial, unconstrained (reading guide 59–60) | 98; 106 | 136–138, 148, 173–175, 184–186, 196–198, 233, 243 |
| `signed` | the actual signing moment — **not observable by the verifier**; exists so `ForgeryRejected` can quantify over it (61–63) | 98; 109 | 167, 242 |
| `anchor` | `anchor_time`: Bitcoin block time of the OTS anchor; bytes existed not-after it (A1.6, 64–67) | 98; 107 | 109, 136–137, 149, 173–174, 184–185, 196–197, 245 |
| `confirmedAt` | timestamp of the block granting the k-th confirmation, height h+k−1 (`amendment-2.md:85`); chain-visible; **unconstrained relative to `anchor`** because block timestamps are non-monotonic (68–73; `amendment-2.md:186`) | 98; 108 | 138, 175, 186, 198, 252, 257 |
| `revoked` | the key's revocation time, or `NoRev`; one number suffices because the lifecycle is monotonic — revocation is terminal (74–76; `amendment-1.md:216–224`) | 98; 110 | 148–149, 167, 233, 242–243, 245 |
| `polDelta`, `polEps` | the **verifier's** chosen tolerances, bounded by the maxima (77–79; `amendment-1.md:173–183`) | 99; 111–112 | 136–138, 173–175, 196–198 |
| `rcptDelta`, `rcptEps` | tolerances **declared by the receipt** — adversarial; the verifier must ignore them; present so the invariants can check that acceptance never depends on them (80–85) | 99; 113–114 | 140, 154 (as ignored arguments) |
| `Init` | every combination the universe permits, under the anchor assumption | 105–114 | cfg 7 |
| `Next` | stutter | 116–117 | cfg 8 |
| `TemporalOKWith(rd, re)` | the three A2.2 conjuncts (`amendment-2.md:220–224`) on the verifier's own tolerances: `declared − polEps ≤ anchor ≤ declared + polDelta`, and `confirmedAt ≤ declared + polDelta` | 135–138 | 140, 152 |
| `TemporalOK` | the same at the state's receipt fields (ignored) | 140 | 241, 259 |
| `AuthorizedThroughWindow` | P6's rule: authorised at `declared` (`revoked > declared`) AND no revocation at or before `anchor` (`revoked > anchor`) (`amendment-1.md:209–210`); both conjuncts needed because with ε > 0 the anchor may precede `declared` (145–146) | 147–149 | 152 |
| `StrictAcceptWith(rd, re)` | the temporal/authorisation face of `VALID_STRICT` | 152 | 154, 221 |
| `StrictAccept` | the verifier's verdict projection in this module | 154 | 167, 173, 183, 199, 221, 233, 244, 252–253, 262 |
| `ForgeryRejected` … `HonestCostIsExactlyTheWindow` | the seven invariants (checks table) | 166–167, 172–175, 182–186, 195–199, 219–221, 232–233, 240–245 | cfg 11–17 |
| `NonMonotonicAcceptUnreachable`, `AcceptanceUnreachable`, `LateBurialCaseUnreachable`, `HonestCostCaseUnreachable` | vacuity witnesses | 251–262 | Sanity cfg 18–21 |
| `_Broken.AuthorizedPointOnly` | P6 as it stood after review round 1: authorisation at `declared` only | `_Broken.tla` 50 | 52, 55–56 |
| `_BrokenConf.TemporalOKWith` | the pre-Amendment-2 verifier: no confirmation-timing conjunct | `_BrokenConf.tla` 56–58 | 64–83 |
| `_BrokenTol.Max`, `TemporalOKWith` | verifier honours the LARGER of its own and the receipt's tolerance | `_BrokenTol.tla` 53, 58–61 | 67–76 |
| `_BrokenTolStrict.Min`, `TemporalOKWith` | verifier honours the SMALLER — issuer-selected verdicts | `_BrokenTolStrict.tla` 50, 54–57 | 63–87 |

## Checks table

| # | Invariant (lines) | Registered sentence it discharges | What the review found it does NOT discharge | Companion behaviour |
|---|---|---|---|---|
| 1 | `ForgeryRejected` (166–167) | P6: the round-2 attack — "a key revoked inside the δ window could sign *after* revocation while declaring a time just before it" — defeated by "no revocation effective at or before `anchor_time`" (`amendment-1.md:203–210`). Bytes signed at or after revocation are never strict-accepted, under every policy, though the verifier cannot see `signed` (comment 160–165). **Load-bearing** for P6's security theorem. | Its proof depends entirely on `signed <= anchor` at `Init` and `revoked > anchor` in acceptance; it does not establish the anchor constraint, signature authenticity, or that revocation is authentic; it addresses post-revocation signing, not forgery generally (reviewer 317). **Item 11 (Boundary):** backward header skew can violate `signed <= anchor` — the relevant attack (reviewer 387) is excluded at initialisation, not rejected (454). No dedicated sanity witness; antecedent satisfiable by reading (369). | **RED in `_Broken`** — `declared 0, signed 1, anchor 1, revoked 1, confirmedAt 0, polDelta 1`: point-only authorisation accepts `1 > 0` (`_Broken.out:38–47`). Green in `_BrokenConf_Green` and `_BrokenTolStrict_Green`. |
| 2 | `WindowRespected` (172–175) | P5's two-sided inequality `declared − ε ≤ anchor ≤ declared + δ` (`amendment-1.md:159–171`) plus A2.2's `confirmed_at ≤ declared + δ` (`amendment-2.md:224`), on the verifier's own policy. | A necessary condition already inside the acceptance predicate, so it checks preservation in the assembled predicate; does not establish that `confirmedAt` comes from the designated block, that depth exists, or that headers are authentic (reviewer 320; item 14). | Green in `_BrokenTolStrict_Green` (narrowed acceptance stays inside the policy). |
| 3 | `VerifierOwnsTolerances` (182–186) | "δ and ε belong to the verifier, not the receipt"; "no degraded policy may enlarge δ or ε beyond the strict maxima" (`amendment-1.md:173–183`). | **Item 8 (Accepted as fact):** compares the accepted gaps against the GLOBAL maxima, not the verifier's chosen policy — a receipt enlarging δ from 0 to an effective 1 under `DeltaMax = 3` passes it (header 37–44; reviewer 323). Ownership in the policy sense is carried by `ReceiptIndependence`. Does not validate 72/24 h or their ratification (324). No degraded policy or waiver state exists (323). | **RED in `_BrokenTol`** — `rcptDelta 4, confirmedAt 4, polDelta 0, anchor = declared = 0`; the red conjunct is `confirmedAt − declared ≤ DeltaMax` (`_BrokenTol.out:37–46`; item 9 corrected the header's witness quantity, `_BrokenTol.tla` 17–25). Green in `_BrokenTolStrict_Green`. |
| 4 | `AbandonedArtifactRejected` (195–199) | A2.2: "the **chain-late subclass** of the A2.0 abandoned-anchor artifact (`confirmed_at > declared + δ`) is rejected outright" (`amendment-2.md:228–231`); the A2.0 correction made mechanical (comment 188–194). | Antecedent additionally requires an in-window anchor, so the standalone invariant is narrower than rejecting every chain-late artifact; no abandonment, attempt, shipping, or standing is represented — it recognises a timestamp pattern (reviewer 327). Under a stricter verifier δ, lateness need not imply abandonment under the issuance policy (328; `amendment-2.md:96–103`). | **RED in `_BrokenConf`** — `anchor = declared = 0, confirmedAt 1, polDelta 0` (`_BrokenConf.out:35–44`); `_BrokenConf_Green` **green** on `ForgeryRejected`, `ReceiptIndependence` (`_BrokenConf_Green.out:47`, 4,302,592 states) — the artifact is no forgery and touches no receipt tolerance. |
| 5 | `ReceiptIndependence` (219–221) | "it may not choose its own temporal tolerances — a receipt-controlled tolerance would let a malicious issuer write an enormous window into the signed bytes" (`amendment-1.md:173–178`), taken literally: the verdict is identical under every receipt-declared pair. **Load-bearing** for receipt influence, enlargement and narrowing alike. | **Item 8:** not logically stronger than `VerifierOwnsTolerances` — a predicate ignoring its receipt arguments could still accept outside the maxima (correction 209–218). Does not quantify over receipt bytes, policy-version selection, or other receipt-controlled inputs (reviewer 331). | **RED in `_BrokenTolStrict`** — `polDelta 1, rcptDelta 0, confirmedAt 1`: narrowed rejects, unnarrowed accepts (`_BrokenTolStrict.out:35–44`); `_BrokenTolStrict_Green` **green** on the three safety invariants (`_Green.out:47`) — only this invariant sees narrowing. Not certified by `_BrokenConf` (stopped at its first violation, item 4); **green** in `_BrokenConf_Green` (`_BrokenConf_Green.out:47`). |
| 6 | `AuthorizedAtDeclared` (232–233) | `key_authorized(declared_issue_time)` (`amendment-1.md:209`), standing alone; and, per §A4.3, the case where the anchor precedes `declared` and a revocation between them invalidates (`amendment-4.md:107–119`; note 225–231; item 10 ROUTED → §A4.3). | **Item 13 (Boundary):** `declared < revoked` stands in for `key_authorized(declared)`; no activation time, grant, scope, manifest entry, or key identity — terminal revocation alone does not establish initial authorisation (reviewer 335; attack 6, 392). | No dedicated companion; green in the correct run. |
| 7 | `HonestCostIsExactlyTheWindow` (240–245) | P6's fail-closed cost: "it can fail honest receipts whose key was revoked between declaration and anchor confirmation — the correct fail-closed outcome" (`amendment-1.md:226–230`); made exact: the only honest receipts sacrificed are those revoked in `(declared, anchor]` (comment 235–239). | "Honest" means only the scalar premises, not successful issuance or authenticated evidence; the comment's "everything else honest is accepted" omits the declaration-authorisation restriction; `anchor` is the inclusion-block timestamp, so the formula does not measure cost through confirmation (reviewer 339). | No dedicated companion. |

**Vacuity witnesses** (251–262). All four fire — 441,098
(`AcceptanceUnreachable`), 101,528 (`HonestCostCaseUnreachable`),
267,736 (`LateBurialCaseUnreachable`), 267,932
(`NonMonotonicAcceptUnreachable`); 1,078,290 repeats elided
(`_Sanity.out:65–75`, counts at 71–74; FIXES log 214–218). No registered sentence claims
reachability (reviewer 343). Acceptance witnesses cover the antecedents
of `WindowRespected`, `VerifierOwnsTolerances`, `AuthorizedAtDeclared`;
`ReceiptIndependence` has no antecedent (367). The witnesses establish
scalar-case coverage, not reachability of any operational event (371).

**Registered clauses with no formula in this module** (reviewer 347–352):
receipt policy-version and observed-delay recording; degraded-policy
handling, non-waivability, actual magnitudes and ratification; depth k,
height arithmetic, reorgs, shipping, discarding, re-issuance
(`confirmedAt` is an unconstrained input, not computed from a chain);
issuer/verifier comparison, slack, observation lag, latch, expiry,
standing; header availability/authentication, canonical-chain
selection, and the `INVALID`/`UNVERIFIABLE` partition; lifecycle
enforcement; every A1.3 action.

## Finite instance

`MaxTime = 6`, `DeltaMax = 3`, `EpsilonMax = 1`, `RcptTolMax = 6`
(cfg 2–5); `NoRev = 7`. **4,302,592 distinct states**, green on all
seven, 2 min 32 s (`P5P6_TemporalRevocation.out:46–47, 52, 55`). The
constants are scaled-down stand-ins for 72 h / 24 h (header 52–54); the
"unconstrained" declared time and "possibly enormous" receipt
tolerances of the comments are in fact bounded to `0..6` (reviewer 441).

**k does not appear in this module.** `confirmedAt` is a free integer
in `0..MaxTime` (108), not derived from a height h and depth k (reviewer
348, 438); the depth arithmetic and the `DepthK = k − 1` pin are the
bridge's (`P5cP5P6_Bridge.tla`; item 14; `formal/PROPERTIES.md:90–131`).
The record contains no parameter-independence argument for this
instance; this aid supplies none.

Runs in the current record (FIXES log 54–57, 115–121): main **green**;
`_Broken` **red** `ForgeryRejected`; `_BrokenConf` **red**
`AbandonedArtifactRejected`; `_BrokenTol` **red** `VerifierOwnsTolerances`;
`_BrokenTolStrict` **red** `ReceiptIndependence`; `_BrokenConf_Green`
and `_BrokenTolStrict_Green` **green** (4,302,592 states each).
`_Broken.cfg` and `_BrokenTol.cfg` configure one invariant each, so
their item-4 `_Green` set is empty (FIXES log 49, 128–132).

## Boundaries

From the review's **Boundary** / **Covered elsewhere** dispositions and
the header correction:

- **Item 11 — the load-bearing assumption.** `signed <= anchor` (109) is
  A1.6's upper-bound semantics (`amendment-1.md:485–490`), imposed at
  `Init`. Backward header skew can violate it; the residual is A2.1's
  timestamp-skew residual (`amendment-2.md:186–196`; A1.6 `:500–505`,
  skew "absorbed into δ and ε"), carried in the first-link decision as
  "δ plus A2.1's skew residuals" (`formal/spike/first-link/DECISION.md:553–563`).
  The module names the assumption (64–67) and this aid cites the
  residual.
- **Item 12 — the join with P5c's `Ship`.** The header's "exact by
  construction" (17–19) predates the bridge; the correspondence was
  asserted, not checked, until `P5cP5P6_Bridge.tla` checked it as
  `ShippedDesignatedAgree` with `_BrokenAnchorSubst` red (header
  correction 26–36; `formal/PROPERTIES.md:90–131`). Under P5c's fused
  clock the guards merely coincide.
- **Item 13 — no key lifecycle.** `declared < revoked` stands in for
  `key_authorized(declared)`; no activation time (note 229–231). The
  binding-form lifecycle is deferred (`docs/band-1-docket.md:179`, item
  18); issuer signing-key lifetime and rotation is a candidate not yet
  registered (`:344`, item 26).
- **Item 14 — assigned elsewhere.** Header availability and
  authentication → A2.2's H1a evidence obligation
  (`amendment-2.md:236–244`); depth-k derivation → the bridge; the
  `INVALID`/`UNVERIFIABLE` partition → P4 (this module has a Boolean
  acceptance that merges rejection reasons, reviewer 440).
- **Item 10** was ROUTED and is now §A4.3 (header 45–50).
- Signature checks are abstracted as passing — that face belongs to the
  ProVerif models and P4 (header 54–56); no receipt byte binding
  connects the scalars to signed artifacts (reviewer 442).
- Verification time is absent; `_BrokenTolStrict`'s "parties checking
  promptly" is unmodelled (reviewer 412).

## Plain-language statement (collaborator; cited; Part B pending)

*Claim.* For every assignment of declared time, signing time, anchor
time, k-th-confirmation time, revocation time, and tolerances in the
configured instance: a receipt strict-accepted by the verifier's
temporal/authorisation predicate was signed before its key was revoked
(given that the anchor bounds signing from above); sits inside the
verifier's own window on all three A2.2 conjuncts; is accepted
identically whatever tolerances the receipt itself declares; and the
only honest receipts the rule sacrifices are those revoked between
declaration and anchor. Seven formulas, green over 4,302,592 states
(`out:47`). The review's strongest defensible reading (reviewer 446,
454): no invariant error across those fixed assignments in one bounded
configuration; the central theorem is conditional on `signed <= anchor`,
named but not checked here.

*Adversary.* A forger or malicious issuer who declares any time, signs
at any time not after the anchor, and writes any tolerances into the
receipt (reading guide 59–60, 80–85); no bytes, keys, or actions.

*Boundary.* Anchor semantics and skew (item 11), the join with issuance
(item 12), key lifecycle (item 13), header provenance and the verdict
partition (item 14) are elsewhere; this module checks the *logic* of the
window, not its magnitudes (52–54).

---

# Part B — blind explanation (Codex CLI 0.153.3, model gpt-6-astra, 2026-09-06, verbatim)

> Written by a non-author model of a different family, jailed to the current modules, configurations, trimmed committed TLC outputs, the registered text, and Amendment 4 — no repository, results, or review access. Its English is evidence of what the modules *say*. Where it disagrees with Part A, the disagreement is a finding to disposition, not a defect to hide. Dispatch prompt archived at `formal/tla/falsification-2026-09-06/P5P6/PART-B-PROMPT.md`.

## Reading notes

- A **state** here is one assignment of nine values describing one receipt, its signing/chain/revocation times, and two sources of tolerances; a **behaviour** starts with an allowed assignment and repeats it forever because `Next` changes nothing. There is no running clock or issuance sequence. (`P5P6_TemporalRevocation.tla:98–117`)
- An **INVARIANT** is a Boolean requirement TLC checks in every reachable state of the configured finite instance; a completed clean run supports the listed requirements for that instance, not for arbitrary bounds or an implementation. The main configuration lists seven; its run reports 4,302,592 distinct states and an empty queue. (`P5P6_TemporalRevocation.cfg:1–17`; `P5P6_TemporalRevocation.out.trimmed:40–47`)
- This is a **truth-table model**: `Init` enumerates permitted combinations and `Next` only stutters, so all reachable states are initial states. It checks the acceptance formula across those combinations; it does not simulate mining, shipping, or later revocation events. (`P5P6_TemporalRevocation.tla:105–117`; `P5P6_TemporalRevocation.out.trimmed:40–48`)
- A **sanity/witness configuration** deliberately asserts that useful cases are unreachable. Its healthy result is a **VIOLATION**: a counterexample establishes that the case exists, preventing an implication from passing merely because its premise never occurs. Here the four cases are acceptance, chain-late burial, honest rejection, and acceptance with `confirmedAt < anchor`; all four have reported violations. (`P5P6_TemporalRevocation_Sanity.cfg:1–21`; `P5P6_TemporalRevocation.tla:251–262`; `P5P6_TemporalRevocation_Sanity.out.trimmed:4–14`)
- A **_Broken companion** deliberately changes a rule; its counterexample shows that the selected invariant detects that defect. A **_Green isolation configuration** removes the expected failing invariant and completes the remaining checks on that broken model: an early stopped red run cannot establish that the others always hold. Green therefore establishes a detector's blind spot, not correctness of the broken model. (`P5P6_TemporalRevocation_Broken.tla:48–56`; `P5P6_TemporalRevocation_BrokenConf_Green.cfg:1–19`; `P5P6_TemporalRevocation_BrokenConf_Green.out.trimmed:40–47`)
- **CONSTANTS** in the configuration fix the universe for a run: time ceiling 6, verifier tolerance ceilings 3 and 1, receipt tolerance ceiling 6. The policy and receipt tolerances remain state variables ranging within those ceilings; these integers stand in for time magnitudes rather than checking 72-hour/24-hour deployment sizing. (`P5P6_TemporalRevocation.cfg:1–5`; `P5P6_TemporalRevocation.tla:52–56,105–114`)

Stale evidence notes: the module's sanity comment says “both” despite four configured witnesses; the trimmed sanity output contains “No error” after reporting violations and documents a filtering mismatch, so its final banner alone is not a pass criterion. (`P5P6_TemporalRevocation.tla:247–262`; `P5P6_TemporalRevocation_Sanity.cfg:17–21`; `P5P6_TemporalRevocation_Sanity.out.trimmed:39–52`)

## Cast

**The thing being judged is `StrictAccept`, a derived yes/no temporal-and-revocation result for a receipt, not a stored state variable or the complete `VALID_STRICT` verdict.** `signed` is hidden ground truth used to test that result, not a verifier input. (`P5P6_TemporalRevocation.tla:61–63,86–87,135–154,166–167`)

The table covers all locally declared variables, constants, and operator names; shared names are located in the main module, with companion changes and their own locations below. (`P5P6_TemporalRevocation.tla:91–262`; `P5P6_TemporalRevocation_Broken.tla:19–56`; `P5P6_TemporalRevocation_BrokenConf.tla:30–83`; `P5P6_TemporalRevocation_BrokenTol.tla:29–76`; `P5P6_TemporalRevocation_BrokenTolStrict.tla:26–87`)

| Name | Plain design meaning | Defined at | Used at |
|---|---|---|---|
| `declared` | Issuer's claimed issue time | `P5P6_TemporalRevocation.tla:98` | `P5P6_TemporalRevocation.tla:136–138,148` |
| `signed` | Actual signing time, hidden from verifier | `P5P6_TemporalRevocation.tla:98` | `P5P6_TemporalRevocation.tla:109,167,242` |
| `anchor` | Assumed anchoring upper bound on signing time | `P5P6_TemporalRevocation.tla:98` | `P5P6_TemporalRevocation.tla:109,136–137,149` |
| `confirmedAt` | Supplied timestamp of the block granting confirmation k | `P5P6_TemporalRevocation.tla:98` | `P5P6_TemporalRevocation.tla:108,138,198` |
| `revoked` | Terminal revocation time, or never | `P5P6_TemporalRevocation.tla:98` | `P5P6_TemporalRevocation.tla:110,148–149,167` |
| `polDelta` | Verifier's allowed anchor/confirmation delay relative to declaration | `P5P6_TemporalRevocation.tla:99` | `P5P6_TemporalRevocation.tla:111,137–138` |
| `polEps` | Verifier's allowed declaration delay relative to anchor | `P5P6_TemporalRevocation.tla:99` | `P5P6_TemporalRevocation.tla:112,136` |
| `rcptDelta` | Receipt-supplied delta, adversarial | `P5P6_TemporalRevocation.tla:99` | `P5P6_TemporalRevocation.tla:113,140,154` |
| `rcptEps` | Receipt-supplied epsilon, adversarial | `P5P6_TemporalRevocation.tla:99` | `P5P6_TemporalRevocation.tla:114,140,154` |
| `MaxTime` | Largest ordinary time value | `P5P6_TemporalRevocation.tla:91`; `P5P6_TemporalRevocation.cfg:2` | `P5P6_TemporalRevocation.tla:96,106–110` |
| `DeltaMax` | Global verifier delta ceiling | `P5P6_TemporalRevocation.tla:91`; `P5P6_TemporalRevocation.cfg:3` | `P5P6_TemporalRevocation.tla:111,184,186` |
| `EpsilonMax` | Global verifier epsilon ceiling | `P5P6_TemporalRevocation.tla:91`; `P5P6_TemporalRevocation.cfg:4` | `P5P6_TemporalRevocation.tla:112,185` |
| `RcptTolMax` | Enumeration ceiling for receipt tolerance attacks | `P5P6_TemporalRevocation.tla:91`; `P5P6_TemporalRevocation.cfg:5` | `P5P6_TemporalRevocation.tla:113–114,220` |
| `NoRev` | “Never revoked,” encoded as `MaxTime + 1` | `P5P6_TemporalRevocation.tla:96` | `P5P6_TemporalRevocation.tla:110` |
| `Init` | Permitted input combinations and assumptions | `P5P6_TemporalRevocation.tla:105–114` | `P5P6_TemporalRevocation.cfg:7` |
| `Next` | Repeat the same assignment | `P5P6_TemporalRevocation.tla:116–117` | `P5P6_TemporalRevocation.cfg:8` |
| `TemporalOKWith(rd, re)` | Three time comparisons using verifier policy, ignoring receipt arguments | `P5P6_TemporalRevocation.tla:135–138` | `P5P6_TemporalRevocation.tla:140,152` |
| `TemporalOK` | Time comparisons evaluated with the state's receipt arguments | `P5P6_TemporalRevocation.tla:140` | `P5P6_TemporalRevocation.tla:241,259` |
| `AuthorizedThroughWindow` | Revocation strictly later than both declaration and anchor | `P5P6_TemporalRevocation.tla:147–149` | `P5P6_TemporalRevocation.tla:152` |
| `StrictAcceptWith(rd, re)` | Temporal and revocation result with explicit receipt arguments | `P5P6_TemporalRevocation.tla:152` | `P5P6_TemporalRevocation.tla:154,221` |
| `StrictAccept` | Result for this state's receipt arguments | `P5P6_TemporalRevocation.tla:154` | `P5P6_TemporalRevocation.tla:167,173,183,199,221,233,244` |
| `ForgeryRejected` | Post-revocation signing cannot pass | `P5P6_TemporalRevocation.tla:166–167` | `P5P6_TemporalRevocation.cfg:11` |
| `WindowRespected` | Acceptance stays inside the chosen policy | `P5P6_TemporalRevocation.tla:172–175` | `P5P6_TemporalRevocation.cfg:12` |
| `VerifierOwnsTolerances` | Acceptance stays inside global maxima | `P5P6_TemporalRevocation.tla:182–186` | `P5P6_TemporalRevocation.cfg:13` |
| `AbandonedArtifactRejected` | In-window anchor with chain-late confirmation cannot pass | `P5P6_TemporalRevocation.tla:195–199` | `P5P6_TemporalRevocation.cfg:14` |
| `ReceiptIndependence` | Changing receipt tolerances alone cannot change the result | `P5P6_TemporalRevocation.tla:219–221` | `P5P6_TemporalRevocation.cfg:15` |
| `AuthorizedAtDeclared` | Acceptance requires declaration before revocation | `P5P6_TemporalRevocation.tla:232–233` | `P5P6_TemporalRevocation.cfg:16` |
| `HonestCostIsExactlyTheWindow` | A time-consistent, pre-revocation signature authorized at declaration is rejected only if revoked by anchor | `P5P6_TemporalRevocation.tla:240–245` | `P5P6_TemporalRevocation.cfg:17` |
| `NonMonotonicAcceptUnreachable` | Deliberately denies accepted cases with confirmation timestamp before anchor | `P5P6_TemporalRevocation.tla:251–252` | `P5P6_TemporalRevocation_Sanity.cfg:18` |
| `AcceptanceUnreachable` | Deliberately denies any acceptance | `P5P6_TemporalRevocation.tla:253` | `P5P6_TemporalRevocation_Sanity.cfg:19` |
| `LateBurialCaseUnreachable` | Deliberately denies in-window anchors with late confirmation timestamps | `P5P6_TemporalRevocation.tla:254–257` | `P5P6_TemporalRevocation_Sanity.cfg:20` |
| `HonestCostCaseUnreachable` | Deliberately denies the honest-rejection premise | `P5P6_TemporalRevocation.tla:258–262` | `P5P6_TemporalRevocation_Sanity.cfg:21` |
| `AuthorizedPointOnly` | Broken revocation check at declaration alone | `P5P6_TemporalRevocation_Broken.tla:50` | `P5P6_TemporalRevocation_Broken.tla:52` |
| `Max(a, b)` | Larger tolerance, allowing receipt enlargement | `P5P6_TemporalRevocation_BrokenTol.tla:53` | `P5P6_TemporalRevocation_BrokenTol.tla:59–61` |
| `Min(a, b)` | Smaller tolerance, allowing receipt narrowing | `P5P6_TemporalRevocation_BrokenTolStrict.tla:50` | `P5P6_TemporalRevocation_BrokenTolStrict.tla:55–57` |

`rd/re` and `a/b` are local arguments, not extra state or configuration constants; `rd/re` are intentionally unused in the correct time predicate, but passed through the acceptance wrapper so receipt independence can be tested. (`P5P6_TemporalRevocation.tla:130–154,219–221`; `P5P6_TemporalRevocation_BrokenTol.tla:53`; `P5P6_TemporalRevocation_BrokenTolStrict.tla:50`)

The companions redeclare the same constants and variables and retain the same initialization/stuttering domains; the changed acceptance definitions are located here. (`P5P6_TemporalRevocation_Broken.tla:19–41`; `P5P6_TemporalRevocation_BrokenConf.tla:30–52`; `P5P6_TemporalRevocation_BrokenTol.tla:29–51`; `P5P6_TemporalRevocation_BrokenTolStrict.tla:26–48`)

| Companion definitions | Design meaning | Defined at | Used at |
|---|---|---|---|
| `_Broken`: `TemporalOK`, `StrictAccept`, `ForgeryRejected` | Correct time test, point-only revocation acceptance, forgery detector | `P5P6_TemporalRevocation_Broken.tla:43–56` | `P5P6_TemporalRevocation_Broken.tla:52–56`; `P5P6_TemporalRevocation_Broken.cfg:11` |
| `_BrokenConf`: `TemporalOKWith`, `AuthorizedThroughWindow`, `StrictAcceptWith`, `StrictAccept`, `ForgeryRejected`, `ReceiptIndependence`, `AbandonedArtifactRejected` | Omit confirmation timing; retain revocation and receipt independence; test chain-late acceptance | `P5P6_TemporalRevocation_BrokenConf.tla:56–83` | `P5P6_TemporalRevocation_BrokenConf.tla:64–83`; `P5P6_TemporalRevocation_BrokenConf.cfg:16–18` |
| `_BrokenTol`: `TemporalOKWith`, `AuthorizedThroughWindow`, `StrictAcceptWith`, `StrictAccept`, `VerifierOwnsTolerances` | Enlarge all time allowances using receipt values; retain revocation; test maxima | `P5P6_TemporalRevocation_BrokenTol.tla:58–76` | `P5P6_TemporalRevocation_BrokenTol.tla:67–76`; `P5P6_TemporalRevocation_BrokenTol.cfg:11` |
| `_BrokenTolStrict`: `TemporalOKWith`, `AuthorizedThroughWindow`, `StrictAcceptWith`, `StrictAccept`, `ForgeryRejected`, `WindowRespected`, `VerifierOwnsTolerances`, `ReceiptIndependence` | Narrow allowances using receipt values; retain revocation; test safety and independence | `P5P6_TemporalRevocation_BrokenTolStrict.tla:54–87` | `P5P6_TemporalRevocation_BrokenTolStrict.tla:63–87`; `P5P6_TemporalRevocation_BrokenTolStrict.cfg:14–17` |

Misleading names/comments: `VerifierOwnsTolerances` alone does not establish policy ownership, and `ReceiptIndependence` is not logically stronger than the maxima check; they are complementary. (`P5P6_TemporalRevocation.tla:37–44,209–218`)

## What each invariant checks

These are exactly the seven invariants selected by the main configuration. (`P5P6_TemporalRevocation.cfg:10–17`)

| Invariant | Plain-language claim enforced | Corresponding registered wording (quoted) | What it does NOT establish |
|---|---|---|---|
| `ForgeryRejected` | If signing is at or after revocation, this predicate rejects. (`P5P6_TemporalRevocation.tla:166–167`) | “no revocation effective at or before anchor_time” (`REGISTERED.txt:52`) | Cryptographic forgery resistance or proof of the assumed `signed <= anchor`; both lie outside this check. (`P5P6_TemporalRevocation.tla:54–56,109,160–165`) |
| `WindowRespected` | Every acceptance satisfies both anchor bounds and the confirmation upper bound under the chosen verifier tolerances. (`P5P6_TemporalRevocation.tla:172–175`) | “`VALID_STRICT` now requires all of:” followed by “declared_issue_time − ε ≤ anchor_time”, “anchor_time ≤ declared_issue_time + δ”, and “confirmed_at ≤ declared_issue_time + δ”. (`REGISTERED.txt:219–223`) | An exact signing date, elimination of within-window backdating, or wall-clock burial timeliness. (`REGISTERED.txt:8–10,42–44,189–195`) |
| `VerifierOwnsTolerances` | Accepted gaps never exceed the global ceilings. (`P5P6_TemporalRevocation.tla:182–186`) | “A verifier may choose stricter bounds; no degraded policy may enlarge δ or ε beyond the strict maxima.” (`REGISTERED.txt:22–23`) | Respect for a particular stricter policy, receipt independence, or degraded-mode behavior: this invariant uses maxima and this module has only a Boolean strict-path result. (`P5P6_TemporalRevocation.tla:37–44,151–154,182–186`) |
| `AbandonedArtifactRejected` | An anchor inside policy bounds cannot rescue confirmation timestamp beyond `declared + polDelta`. (`P5P6_TemporalRevocation.tla:195–199`) | “The **chain-late subclass** of the A2.0 abandoned-anchor artifact (`confirmed_at > declared + δ`) is **rejected outright**”. (`REGISTERED.txt:227–229`) | Rejection of every abandoned attempt: chain-valid operational abandonment needs separate standing rules. (`REGISTERED.txt:230–234`) |
| `ReceiptIndependence` | For fixed remaining inputs and verifier policy, every enumerated receipt tolerance pair gives the same verdict. (`P5P6_TemporalRevocation.tla:219–221`) | “δ and ε belong to the verifier, not the receipt.” (`REGISTERED.txt:15`) | Maxima compliance by itself, or independence from arbitrary other receipt fields; only two arguments are varied. (`P5P6_TemporalRevocation.tla:209–221`) |
| `AuthorizedAtDeclared` | Accepted declaration precedes revocation, including when declaration follows anchor. (`P5P6_TemporalRevocation.tla:225–233`) | “key_authorized(declared_issue_time)” (`REGISTERED.txt:51`); qualified non-retroactivity: “Revocation effective after both `anchor_time` and `declared_issue_time` does not retroactively change the verdict.” (`AMENDMENT-4.txt:116–118`) | Activation, authorization provenance, or a transition theorem about updating revocation: authorization here is only comparison with a terminal revocation time. (`P5P6_TemporalRevocation.tla:74–76,116–117,230–233`) |
| `HonestCostIsExactlyTheWindow` | Given temporal consistency, signing before revocation, and declaration before revocation, rejection implies revocation by anchor: the residual cost is in `(declared, anchor]`. (`P5P6_TemporalRevocation.tla:240–245`) | “it can fail honest receipts whose key was revoked between declaration and anchor confirmation”. (`REGISTERED.txt:68–70`) | Unconditional acceptance of honest receipts or a cost interval ending at `confirmedAt`; the invariant is a conditional implication ending at `anchor`. Its converse follows from the acceptance definition under the same premises, not from the implication alone. (`P5P6_TemporalRevocation.tla:147–154,240–245`) |

## The claim

For the checked finite instance, assuming signing no later than the anchor and terminal revocation, a relying party using this temporal-and-revocation predicate accepts only receipts signed before revocation, authorized at declaration and anchor, and inside its chosen three-part time window, with no verdict influence from receipt-supplied tolerances. (`P5P6_TemporalRevocation.tla:74–76,105–114,135–154,166–233`; `P5P6_TemporalRevocation.cfg:1–17`; `P5P6_TemporalRevocation.out.trimmed:40–47`)

TLC reports completion without an invariant error over 4,302,592 distinct assignments; stuttering introduces no new assignments. This is the universe with declaration/anchor/confirmation times 0–6, signing 0–anchor, revocation 0–6 or sentinel 7, verifier delta 0–3 and epsilon 0–1, and each receipt tolerance 0–6; all seven configured invariants hold in the reported search, including the conditional honest-rejection characterization. These bounds make the claim finite, not a proof for all integer times. (`P5P6_TemporalRevocation.out.trimmed:40–48`; `P5P6_TemporalRevocation.cfg:1–17`; `P5P6_TemporalRevocation.tla:96,105–117,240–245`)

## The adversary and the abstraction

There is no adversary process: enumeration supplies every allowed declaration and receipt tolerance, including backdating claims and oversized tolerances, together with every allowed signing, anchor, confirmation, and revocation combination. Verifier policy also ranges over all allowed choices, but that quantification does not grant the issuer control of policy; the acceptance formula uses the verifier's values and ignores the receipt's. (`P5P6_TemporalRevocation.tla:59–87,105–114,135–154`)

The load-bearing initialization assumptions are **anchor upper bound** (`signed <= anchor`), **bounded verifier policy** (`polDelta <= DeltaMax`, `polEps <= EpsilonMax`), and **finite input domains**; the constant assumptions require natural-number bounds and receipt delta capacity above the verifier maximum. **Terminal revocation** is built into representing lifecycle by one scalar and **pre-revocation authorization** into comparing that scalar with declaration, without any activation time. The adversary cannot violate these assumptions, replace the formula, forge a header representation, or introduce missing evidence: no such alternatives exist in the state. (`P5P6_TemporalRevocation.tla:74–76,91–117,147–154,230–231`)

Signature verification is assumed to pass; chain/revocation facts are supplied as integers rather than authenticated here. There is deliberately no `confirmedAt >= anchor` assumption, and the sanity run exhibits acceptance with confirmation timestamp 0 and anchor 1. (`P5P6_TemporalRevocation.tla:54–56,68–73,105–110`; `P5P6_TemporalRevocation_Sanity.out.trimmed:27–36`)

## Why the broken companion fails

| Companion | Defect and exact detector | Committed evidence and its interpretation |
|---|---|---|
| `_Broken` | Uses `AuthorizedPointOnly`, dropping authorization through anchor; `ForgeryRejected` catches it. (`P5P6_TemporalRevocation_Broken.tla:43–56`) | Initial state: declaration 0, signing = revocation = anchor = 1, confirmation 0, verifier delta 1 and epsilon 0; its time test and declaration-only authorization pass despite signing at revocation. TLC names `ForgeryRejected`. (`P5P6_TemporalRevocation_Broken.out.trimmed:35–44`) |
| `_BrokenConf` | Drops the confirmation-timing conjunct; `AbandonedArtifactRejected` catches it. (`P5P6_TemporalRevocation_BrokenConf.tla:56–83`) | Initial state: declaration = anchor = signing = 0, confirmation 1, revocation 1, both policy tolerances 0; the broken formula accepts despite late confirmation. TLC names `AbandonedArtifactRejected`. The isolation run checks `ForgeryRejected` and `ReceiptIndependence` through all 4,302,592 states without error. (`P5P6_TemporalRevocation_BrokenConf.out.trimmed:35–44`; `P5P6_TemporalRevocation_BrokenConf_Green.cfg:17–19`; `P5P6_TemporalRevocation_BrokenConf_Green.out.trimmed:40–47`) |
| `_BrokenTol` | Uses the larger of policy and receipt tolerances; `VerifierOwnsTolerances` catches acceptance beyond a global maximum. (`P5P6_TemporalRevocation_BrokenTol.tla:53–76`) | Initial state: declaration = anchor = signing = 0, confirmation 4, revocation 1, policy delta 0, receipt delta 4; confirmation gap 4 exceeds `DeltaMax = 3`. TLC names `VerifierOwnsTolerances`. This is a confirmation-gap witness, not an anchor-gap witness. (`P5P6_TemporalRevocation_BrokenTol.out.trimmed:35–44`; `P5P6_TemporalRevocation_BrokenTol.cfg:3`) |
| `_BrokenTolStrict` | Uses the smaller tolerance; `ReceiptIndependence` catches receipt-driven rejection. (`P5P6_TemporalRevocation_BrokenTolStrict.tla:50–87`) | Initial state: declaration = anchor = signing = 0, confirmation 1, revocation 1, policy delta 1, receipt delta 0, both epsilons 0. The formula rejects; substituting argument `rd = 1, re = 0` accepts, explaining the named `ReceiptIndependence` violation. Its isolation run completes the three checks `ForgeryRejected`, `WindowRespected`, and `VerifierOwnsTolerances` without error. (`P5P6_TemporalRevocation_BrokenTolStrict.out.trimmed:35–44`; `P5P6_TemporalRevocation_BrokenTolStrict.tla:54–65,85–87`; `P5P6_TemporalRevocation_BrokenTolStrict_Green.cfg:19–22`; `P5P6_TemporalRevocation_BrokenTolStrict_Green.out.trimmed:40–47`) |

Suspicious companion prose: `_BrokenConf`'s “only” catcher is scoped to its selected checks (the main extended window/maxima checks would also fail), and `_BrokenTolStrict`'s story about “checking promptly” has no modeled verification-time input. (`P5P6_TemporalRevocation_BrokenConf.tla:15–24`; `P5P6_TemporalRevocation_BrokenTolStrict.tla:8–13,33–48`)

## What this result does not show

- No cryptographic implementation, Bitcoin/OTS upper-bound proof, canonical-header authentication, or confirmation-depth derivation is checked: signatures are abstracted as passing, signing is constrained by anchor, and confirmation is a supplied integer. Header authentication remains an explicit evidence obligation. (`P5P6_TemporalRevocation.tla:54–56,105–110`; `REGISTERED.txt:235–243`)
- No full verdict partition, missing-header behavior, or waiver/non-promotion enforcement: `StrictAccept` is Boolean. Amendment 4 §A4.2 ratifies `INVALID` when a required failure coexists with an unperformable check and qualifies the latter rule to a **required** check; this family has no states distinguishing those outcomes. (`P5P6_TemporalRevocation.tla:98–99,151–154`; `REGISTERED.txt:244–247`; `AMENDMENT-4.txt:84–105`)
- No exact signing-time recovery, elimination of tolerated backdating, or wall-clock deadline guarantee: signing can precede declaration, and `confirmedAt` is a chain-time proxy. (`P5P6_TemporalRevocation.tla:106–109`; `REGISTERED.txt:8–10,42–44,189–195`)
- No issuer progress, shipping, retry/refusal, operational abandonment, or lineage/standing proof; no issuer/verifier correspondence is checked here. The module explicitly corrects its earlier “exact by construction” claim and assigns that join to a separate bridge. (`P5P6_TemporalRevocation.tla:9–19,26–36,116–117`; `REGISTERED.txt:130–144,230–234`)
- No activation-time or revoke/re-authorize lifecycle verification; monotonic lifecycle is assumed, and authorization is reduced to revocation comparisons. (`REGISTERED.txt:58–66`; `P5P6_TemporalRevocation.tla:147–149,230–231`)
- No all-bounds theorem or independent rerun is supplied by this reading aid; the cited evidence is the committed finite run. Its state-fingerprint collision estimates are `1.0E-6` (optimistic calculation) and `1.0E-10` (based on actual fingerprints), so the report itself exposes a residual tool limitation. (`P5P6_TemporalRevocation.cfg:1–5`; `P5P6_TemporalRevocation.out.trimmed:40–47`)

## Correspondence to the registered text

The invariants support P5's two-sided window and verifier-owned tolerances, A2.2's confirmation-time comparison and chain-late rejection, and P6's revocation-only authorization and conditional honest-rejection cost; they do not touch the issuance lifecycle, full verdict partition, or header-evidence construction obligations. (`REGISTERED.txt:1–39,41–75,219–247`; `P5P6_TemporalRevocation.tla:135–245`)
Amendment 4 §A4.3 changes “after `anchor_time`” to “after both `anchor_time` and `declared_issue_time`,” matching the two revocation comparisons; §A4.2 separately ratifies failure precedence and inserts “required” into the unperformable-check sentence, changes belonging to the surrounding P4 verdict logic rather than this Boolean predicate. (`REGISTERED.txt:51–56`; `AMENDMENT-4.txt:84–119`; `P5P6_TemporalRevocation.tla:147–154,225–233`)
Stale status labels: the supplied amendment identifies itself as “DRAFT — adopted in session, not yet signed,” and the module correction says “PROPOSED, not adopted”; these conflict with the task's supplied signed-2026-09-06 status, which this aid uses without independently authenticating a signing commit or timestamp. (`AMENDMENT-4.txt:1–10`; `P5P6_TemporalRevocation.tla:21–25`)
