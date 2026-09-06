## 1. Correspondence audit

All findings are from reading the supplied files, **not re-running TLC**. Citations to `.out` files use their numbered “final 40 lines.” For compact citations, `M` means `P5P6_TemporalRevocation.tla`; `R` means `REGISTERED-P5-P6.txt`; other filenames are written explicitly.

The main configuration checks seven state invariants. It checks no temporal property, and the sole transition preserves every variable. Thus the checked behavior is enumeration of fixed assignments, not an issuance or adversarial execution protocol. (`P5P6_TemporalRevocation.cfg:7–17`; `M:74–86`)

- **`ForgeryRejected`** corresponds to the attack described as “a key revoked inside the δ window could sign *after* revocation while declaring a time just before it,” and its remedy, “no revocation effective at or before anchor_time.” (`R:45–52`)
  The formula rejects every assignment with `revoked <= signed`, including equality and cases outside that particular backdating scenario. Its proof depends entirely on the initialization constraint `signed <= anchor` and acceptance requiring `revoked > anchor`. It does not establish the anchor constraint, signature authenticity, or that revocation is authentic. It addresses post-revocation signing, not forgery generally. (`M:24–25,74–79,116–136`)

- **`WindowRespected`** corresponds exactly, algebraically, to the registered scalar inequalities “declared_issue_time − ε ≤ anchor_time ≤ declared_issue_time + δ,” extended by “confirmed_at ≤ declared_issue_time + δ.” (`R:6`; `A2.1-A2.2.txt:143–147`)
  It expresses a necessary condition on acceptance, using the selected verifier policy. It does not establish that `confirmedAt` actually comes from the designated block, that depth exists, or that headers are authentic. The inequalities are already acceptance conjuncts, so this checks their preservation in the assembled predicate. (`M:104–123,141–144`; `A2.1-A2.2.txt:159–167`)

- **`VerifierOwnsTolerances`** claims correspondence to “δ and ε belong to the verifier, not the receipt” and “no degraded policy may enlarge δ or ε beyond the strict maxima.” (`R:15–23`)
  Its actual quantity is the accepted timestamp gap versus **global maxima**, not versus the verifier’s chosen tolerances. Receipt-driven enlargement from policy δ = 0 to effective δ = 1 can satisfy this invariant when `DeltaMax = 3`. Ownership therefore does not follow from this formula alone. There is also no degraded policy or waiver state. (`M:151–155`; `P5P6_TemporalRevocation.cfg:2–5`)
  The constants stand in for the registered magnitudes; the check does not validate 72/24 hours or their ratification. (`M:21–23`; `R:19–24`)

- **`AbandonedArtifactRejected`** corresponds to “The **chain-late subclass** … (`confirmed_at > declared + δ`) is **rejected outright**.” (`A2.1-A2.2.txt:151–158`)
  Its antecedent additionally requires an in-window anchor, making the standalone invariant narrower than rejection of every chain-late artifact. The actual acceptance predicate rejects all chain-late assignments regardless of anchor position. No abandonment, issuance attempt, shipping, or standing is represented; the formula recognizes a timestamp pattern. (`M:104–107,164–168`)
  Its δ is the verifier’s policy, so lateness under a stricter verifier need not imply abandonment under the issuance policy. The amendment expressly allows this disagreement. (`M:80–81,165–167`; `A2.1-A2.2.txt:23–28`)

- **`ReceiptIndependence`** corresponds to “it may not choose its own temporal tolerances.” (`R:15–18`)
  It requires verdict equality under every bounded pair of receipt-tolerance arguments, capturing both enlargement and narrowing. It does not quantify over receipt bytes, policy-version selection, or other receipt-controlled inputs. (`M:178–180`; `R:15–17`)
  Independence is stronger than merely forbidding receipt-induced enlargement, but it is **not logically stronger than the maxima invariant without additional assumptions**: a predicate ignoring receipt arguments could still accept outside the maxima. The comment’s “strictly stronger” wording needs that qualification. (`M:151–155,170–180`)

- **`AuthorizedAtDeclared`** corresponds to “key_authorized(declared_issue_time).” (`R:51`)
  The formula substitutes `declared < revoked`. This is equivalent only under an additional interpretation that the key is otherwise authorized throughout all modeled pre-revocation times. There is no activation time, authorization grant, scope, manifest entry, or key identity. Terminal revocation alone does not establish initial authorization. (`M:43–45,67–83,184–185`; `R:58–66`)

- **`HonestCostIsExactlyTheWindow`** corresponds to “it can fail honest receipts whose key was revoked between declaration and anchor confirmation.” (`R:68–73`)
  The formula says that temporally passing, pre-revocation-signed, declaration-authorized but rejected assignments have `revoked <= anchor`. The declaration authorization premise supplies the other endpoint, yielding `(declared, anchor]`. This is a one-way implication, though the converse follows from the acceptance definition under the same premises. (`M:116–123,192–197`)
  “Honest” means only the specified scalar premises; it does not include successful issuance or authenticated evidence. “Everything else honest is accepted” in the comment omits the formula’s declaration-authorization restriction. Also, `anchor` is the inclusion block timestamp, while `confirmedAt` is the k-th-confirmation timestamp: the formula does **not** measure cost through confirmation or wall-clock burial. (`M:33–42,187–197`)

The companion configurations check variants of these same invariants; their acceptance definitions change the correspondence as detailed in section 4. (`P5P6_TemporalRevocation_Broken.cfg:10–11`; `P5P6_TemporalRevocation_BrokenTol.cfg:10–11`; `P5P6_TemporalRevocation_BrokenTolStrict.cfg:13–17`; `P5P6_TemporalRevocation_BrokenConf.cfg:15–18`)

The sanity configuration checks four negated witness predicates, not registered safety obligations. Their registered connections and observed failures are addressed below. (`P5P6_TemporalRevocation_Sanity.cfg:1–7,17–21`; `M:199–214`)

**Registered clauses with no corresponding formula in this file set:**

- Receipt policy-version and observed-delay recording; degraded-policy handling; non-waivability; actual tolerance magnitudes and ratification. Only bounded strict-path arithmetic appears. (`R:15–26`; `M:60–83,104–123`)
- Depth k, inclusion/confirmation-height arithmetic, reorgs, shipping only after confirmation, discarding, and re-issuance. `confirmedAt` is an unconstrained input, not computed from a chain. (`R:28–39`; `A2.1-A2.2.txt:3–8,131–137`; `M:74–86`)
- Issuer/verifier comparison on the same observations and issuance policy; slack, observation lag, live opportunity, latch priority, expiry, mutual exclusion, and protocol standing. (`A2.1-A2.2.txt:14–28,29–85,91–101`; `M:67–86,104–123`)
- Header availability, authentication, canonical-chain selection, work validation, store identity, conflict resolution, and the `INVALID`/`UNVERIFIABLE` partition. The model has only a Boolean acceptance predicate over supplied scalars. (`A2.1-A2.2.txt:159–171`; `M:67–68,104–123`)
- Lifecycle enforcement, new fingerprints and manifest entries after re-keying, and explicit verdict stability across revocation updates. One fixed cutoff substitutes for lifecycle behavior. (`R:54–66`; `M:43–45,79,85–86`)
- The adversary’s byte alteration, signature-set manipulation, key substitution/DSKS, replay/type reframing, crafted manifests/anchors, and channel compromise have no corresponding actions or object representations. (`A1.3.txt:5–16`; `M:67–86`)

## 2. Vacuity

The four expected reachable predicates are:

| Witness predicate | Evidence that its negation went red |
|---|---|
| `StrictAccept /\ confirmedAt < anchor` | 267,932 reported violations of `NonMonotonicAcceptUnreachable`. (`M:203–204`; `P5P6_TemporalRevocation_Sanity.out:15`) |
| `StrictAccept` | 441,098 reported violations of `AcceptanceUnreachable`. (`M:205`; `P5P6_TemporalRevocation_Sanity.out:12`) |
| In-window anchor with `confirmedAt > declared + polDelta` | 267,736 reported violations of `LateBurialCaseUnreachable`. (`M:206–209`; `P5P6_TemporalRevocation_Sanity.out:14`) |
| `TemporalOK /\ signed < revoked /\ revoked > declared /\ ~StrictAccept` | 101,528 reported violations of `HonestCostCaseUnreachable`. (`M:210–214`; `P5P6_TemporalRevocation_Sanity.out:13`) |

These counts confirm that the **provided summary reports** all four witnesses firing. Individual assignments were elided, so their contents cannot be inspected in this output. The file reports a completed depth-one enumeration with zero queued states. (`P5P6_TemporalRevocation_Sanity.out:10–23`)

Acceptance witnesses cover the antecedents of `WindowRespected`, `VerifierOwnsTolerances`, and `AuthorizedAtDeclared`; the other predicates cover the abandonment and honest-cost antecedents. `ReceiptIndependence` has no implication antecedent, and its argument domains are nonempty. (`M:141–155,164–185,192–214`; `P5P6_TemporalRevocation.cfg:5`)

**`ForgeryRejected` has no dedicated sanity witness.** Its antecedent is nevertheless satisfiable directly in `Init`: set `declared=signed=anchor=confirmedAt=revoked=0` and both policy tolerances to zero. This is a reading-derived witness, not an individually printed main-run state. (`M:74–83,135–136`)

No checked implication has an antecedent that reading shows to be unreachable. There are no action guards to become enabled: `Next` only stutters. This means the witnesses establish scalar-case coverage, not the reachability of operational eligibility, shipping, revocation, or attack actions. (`M:85–86,135–214`)

## 3. Attack attempts

Tuple notation below is `(declared, signed, anchor, confirmedAt, revoked; polDelta, polEps; rcptDelta, rcptEps)`. Every representable model trace is `Init(tuple) → Next(tuple) → …`; the narrative actions are not transitions in this model. (`M:67–86`)

1. **Revoke, then sign while claiming an earlier date.** Narrative: declare 0 → revoke at 1 → sign at 1 → anchor at 1, with confirmation timestamp 1. Use `(0,1,1,1,1;1,0;0,0)`.
   **Representable as a fixed assignment.** All temporal conjuncts pass; `revoked > anchor` rejects because `1 > 1` is false. The actual revoke/sign sequence is unrepresentable. (`M:74–86,104–118`)

2. **Enlarge the receipt’s tolerance.** Declare/sign/anchor at 0 → obtain confirmation timestamp 4 → claim receipt δ = 4. Use `(0,0,0,4,7;0,0;4,0)`.
   **Representable as a fixed assignment.** Receipt δ is ignored; `confirmedAt <= declared + polDelta` rejects `4 <= 0`. This is also the shape of the printed enlargement counterexample, with revocation set to 1 there. (`M:65,74–83,104–107`; `P5P6_TemporalRevocation_BrokenTol.out:26–35`)

3. **Publish a chain-late, never-shipped receipt.** Declare/sign/anchor at 0 → confirmation timestamp 1 → publish after discarding. Use `(0,0,0,1,1;0,0;0,0)`.
   **Timestamp assignment representable; discarding and publication UNREPRESENTABLE.** The third temporal conjunct rejects. This is the exact scalar assignment printed for the missing-confirmation companion. (`M:67–86,104–107`; `P5P6_TemporalRevocation_BrokenConf.out:24–33`)

4. **Exploit backward header time to hide post-revocation signing.** Declare 1 → revoke at wall time 2 → sign at wall time 3 → later mine headers timestamped 1. Desired tuple: `(1,3,1,1,2;0,0;0,0)`.
   **UNREPRESENTABLE:** `signed <= anchor` excludes it before verification, although the acceptance conjuncts would all pass on these scalars. The amendment acknowledges backward-skewed header timestamps; it does not establish this module’s cross-clock signing bound. Thus the signing theorem is conditional on the named anchor assumption, not a check of its applicability to actual signing time. (`M:30–42,78,104–118`; `A2.1-A2.2.txt:113–119`)

5. **Present a privately mined or unauthenticated in-window header segment.** Sign at 1 → fabricate/select header timestamps 1 → submit `(1,1,1,1,7;0,0;0,0)`.
   **The malicious provenance is UNREPRESENTABLE; its timestamp projection is accepted.** There is no provenance variable or rejecting conjunct. This is precisely the kind of false acceptance the amendment identifies for naive stateless evaluation. (`M:65,67–83,104–123`; `A2.1-A2.2.txt:120–129,159–167`)

6. **Sign before the key becomes authorized.** Sign/declare at 1 → anchor at 2 → grant authorization only at 3; no revocation. Projection: `(1,1,2,2,7;1,0;0,0)`.
   **The authorization grant and pre-grant status are UNREPRESENTABLE; the projection is accepted.** `revoked > declared` supplies no test of whether authorization had begun. This exposes the additional assumption required to equate it with `key_authorized(declared_issue_time)`. (`R:51`; `M:65,67–83,104–123`)

7. **Supply an anchor that has not reached k confirmations.** Declare/sign/include at 1 → present only the inclusion header while assigning `confirmedAt=1`. Projection: `(1,1,1,1,7;0,0;0,0)`.
   **Shallow depth and missing designated evidence are UNREPRESENTABLE; the projection is accepted.** No height, depth, header sequence, or evidence-availability conjunct rejects it. (`R:28–35`; `A2.1-A2.2.txt:159–171`; `M:67–83,104–123`)

8. **Revoke after the anchor but before a post-dated declaration.** Anchor/sign at 0 → revoke at 1 → declared time 1. Use `(1,0,0,0,1;0,1;0,0)`.
   **Representable and rejected by `revoked > declared`; `revoked > anchor` passes.** This exposes a qualification missing from the registered sentence “Revocation effective *after* `anchor_time` does not retroactively change the verdict”: when the anchor precedes declaration, a later revocation can still invalidate authorization at declaration. The explicit registered two-conjunct rule agrees with the model; that unqualified sentence does not. (`R:51–56`; `M:104–118`)

## 4. Companions

- **`Broken`: observed red set `{ForgeryRejected}`**, exactly the singleton configured and predicted. The printed assignment has declaration 0, signing/revocation/anchor 1, confirmation timestamp 0, and policy δ = 1. Temporal checks pass; point-only authorization accepts `1 > 0`, exposing the omitted anchor authorization check. (`P5P6_TemporalRevocation_Broken.cfg:10–11`; `P5P6_TemporalRevocation_Broken.tla:3–15,43–56`; `P5P6_TemporalRevocation_Broken.out:27–36`)
  It demonstrably could fail. Its counterexample permits non-monotonic timestamps, but the defect does not depend on that: setting `confirmedAt=1` preserves acceptance and the violation under the written formulas. (`P5P6_TemporalRevocation_Broken.tla:29–38,43–56`)

- **`BrokenTol`: observed red set `{VerifierOwnsTolerances}`**, exactly the configured and predicted invariant. The witness enlarges confirmation allowance to 4 while policy δ is 0 and the configured maximum is 3. (`P5P6_TemporalRevocation_BrokenTol.cfg:2–11`; `P5P6_TemporalRevocation_BrokenTol.out:26–35`)
  The header predicts an excessive **anchor-to-declared** gap; the printed gap is zero. The red conjunct is instead `confirmedAt - declared <= DeltaMax`. The general enlargement defect is exhibited, but the stated witness quantity is wrong. (`P5P6_TemporalRevocation_BrokenTol.tla:10–13,48–51,62–66`)
  This companion could fail and did. However, enlargement that stays below global maxima cannot fail this invariant merely for exceeding the selected policy; that is a limitation of its catcher. (`P5P6_TemporalRevocation_BrokenTol.tla:62–66`)

- **`BrokenTolStrict`: observed red set `{ReceiptIndependence}`**, matching the named expected failure. The run stops at an initial-state violation, so the output does **not** establish exhaustive green results for the three other configured invariants. (`P5P6_TemporalRevocation_BrokenTolStrict.cfg:1–3,13–17`; `P5P6_TemporalRevocation_BrokenTolStrict.out:24–35`)
  Reading explains the failure: with `confirmedAt=1`, declaration/anchor 0, policy δ = 1 and receipt δ = 0, the current verdict rejects; substituting receipt δ = 1 accepts. The unchanged revocation rule and `Min` bounds also explain algebraically why the three safety invariants cannot detect this narrowing defect. (`P5P6_TemporalRevocation_BrokenTolStrict.out:25–33`; `P5P6_TemporalRevocation_BrokenTolStrict.tla:50–87`)
  Its claimed distinction between parties “checking promptly” and others is unmodeled: verification time is absent and the anchor-to-declared gap is fixed. (`P5P6_TemporalRevocation_BrokenTolStrict.tla:8–13,33–48`)

- **`BrokenConf`: observed red set `{AbandonedArtifactRejected}`**, matching the named expected failure. The initial-state witness has anchor/declaration 0, confirmation timestamp 1, policy δ = 0, and revocation 1. Omitting the confirmation conjunct makes it accepted. (`P5P6_TemporalRevocation_BrokenConf.cfg:1–5,15–18`; `P5P6_TemporalRevocation_BrokenConf.out:24–33`; `P5P6_TemporalRevocation_BrokenConf.tla:56–83`)
  The stopped output does **not** establish exhaustive green results for `ForgeryRejected` and `ReceiptIndependence`. Reading supports them: signing remains bounded by anchor, authorization still checks anchor, and receipt arguments remain unused. Neither can detect the missing confirmation conjunct. (`P5P6_TemporalRevocation_BrokenConf.out:24–35`; `P5P6_TemporalRevocation_BrokenConf.tla:40–75`)
  “Only” this invariant fails is relative to the selected suite: the header itself acknowledges that the main `WindowRespected` and `VerifierOwnsTolerances` would also detect confirmation violations on suitable assignments. (`P5P6_TemporalRevocation_BrokenConf.tla:15–24`)

None of the four companions was prevented from failing by an unrelated restriction: each supplied output contains its targeted failure. The multi-invariant companion runs establish the reported first failure, not an exhaustive classification of every configured invariant. (`P5P6_TemporalRevocation_Broken.out:27–38`; `P5P6_TemporalRevocation_BrokenTol.out:26–37`; `P5P6_TemporalRevocation_BrokenTolStrict.out:24–35`; `P5P6_TemporalRevocation_BrokenConf.out:24–35`)

## 5. Scoped abstractions

**Named in comments:**

- Verifier-side scope; issuance behavior assigned elsewhere. (`M:9–19`)
- Small integer time and scaled tolerance maxima; signature checks assumed passing. (`M:21–25`)
- Adversarial declared time; actual signing time hidden from the verifier. (`M:28–32,55–56`)
- The anchor-as-signing-upper-bound assumption, imposed as a state constraint. (`M:33–36,70–78`)
- Designated confirmation timestamp supplied without ordering against anchor. (`M:37–42,72–77`)
- Terminal revocation represented by one timestamp; a sentinel for never revoked. (`M:43–45,65`)
- Verifier-selected bounded policies and adversarial receipt tolerance fields, intentionally ignored. (`M:46–54,80–83,88–103`)
- Strict temporal/authorization projection of `VALID_STRICT`. (`M:89–90,120–123`)

**Additional abstractions or restrictions not explicitly scoped as such:**

- A static truth-table model: no changing time, lifecycle actions, multiple attempts, or interacting issuer/verifier states. (`M:67–86`)
- Authorization before revocation is implicit; no grant, activation, expiry, identity, manifest, or authority-channel state exists. (`M:67–83,116–118`; `A1.3.txt:8–16`)
- Revocation and chain observations are supplied directly, with no evidence authentication, missing-data case, fork selection, or store disagreement. (`M:67–83`; `A2.1-A2.2.txt:159–171`)
- No derivation of `confirmedAt` from h and k; no constraint that it belongs to the same chain or anchor, or that sufficient blocks exist. (`M:74–78`; `A2.1-A2.2.txt:3–8`)
- Signing time is numerically ordered against header time without an explicit clock conversion or skew model, although confirmation/observation clock differences are material in the amendment. (`M:30–42,78`; `A2.1-A2.2.txt:29–43,113–119`)
- Boolean rejection merges invalidity, unverifiability, and any other rejection reason; protocol standing is absent. (`M:120–123`; `A2.1-A2.2.txt:58–62,168–171`)
- “Unconstrained” declarations and “possibly enormous” receipt tolerances are actually limited to `0..6`; policy ε is `0..1`, δ is `0..3`. No unbounded result is recorded. (`M:28–29,49–50,74–83`; `P5P6_TemporalRevocation.cfg:2–5`)
- No receipt byte binding or adversarial transformations connect the supplied scalars to signed artifacts. Assuming signatures pass does not model which fields those signatures authenticate. (`M:24–25,67–86`; `A1.3.txt:5–14`)

## 6. Verdict on the module header’s honesty

**The header overstates what this supplied check establishes.** The recorded result is no invariant error across 4,302,592 distinct fixed assignments in one bounded configuration, with the output’s stated fingerprint-collision estimates. It is not a checked cross-module correspondence or an operational adversary model. (`P5P6_TemporalRevocation.out:31–39`; `P5P6_TemporalRevocation.cfg:2–17`; `M:85–86`)

The claim that correspondence with `P5c` shipping is “exact by construction” is unsupported by any formula here. The supplied amendment explicitly distinguishes P5c’s fused-clock guard from the decoupled bridge and scopes issuer/verifier agreement to the issuance policy’s tolerances. This module contains neither comparison. (`M:15–19,67–86,104–123`; `A2.1-A2.2.txt:23–28,91–101`)

“Discharges the VERIFIER-SIDE face of P5” needs narrowing to the **scalar temporal/authorization predicate under the named and implicit assumptions**. The registered verifier-side evidence and verdict-partition obligations are absent. (`M:9–15,104–123`; `A2.1-A2.2.txt:159–171`)

The comments also overreach in calling timestamp patterns discarded-attempt artifacts, in describing honest cost through confirmation while testing the inclusion timestamp, and in suggesting any receipt-tolerance routing breaks the maxima invariant. The supplied narrowing companion directly demonstrates the last distinction. (`M:49–54,157–168,187–197`; `P5P6_TemporalRevocation_BrokenTolStrict.tla:54–87`)

The most consequential unresolved correspondence is **actual signing time ≤ anchor header timestamp**. The model names this assumption, but the supplied materials do not establish its validity against backward timestamp skew. Without it, the central post-revocation-signing implication loses its supporting order relation; the relevant attack is excluded at initialization. (`M:30–36,78,129–136`; `A2.1-A2.2.txt:113–119`)