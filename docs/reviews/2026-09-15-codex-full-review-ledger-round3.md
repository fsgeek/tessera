# Codex non-author full review of the ledger register, third round (2026-09-15)

Reviewer: OpenAI Codex CLI (`gpt-6-astra`), run non-interactively by the
owner instance (`codex exec`, repository readable, scratch diagnostics
under `/tmp/tessera-ledger-fourth-1qpc5wh4/`), against the whole of
`formal/suite/LEDGER.md` after the third repair and the 2026-09-15
skeptic read. The reviewer would not yet approve the register as the
capstone plan. Every factual claim below was checked against the tree
before disposition.

## Dispositions (owner instance, 2026-09-15)

1. **C-Q7 does not establish D6's exact signature/bytes relation.** ACCEPTED. Binding a signature to the presented bytes and preventing an honest signature term's acceptance under another key are different properties; C-Q7 observes `(acceptedKey, signature)` only and cannot see different bytes under the same key (Codex's same-key-unbinding diagnostic: C-Q7 holds, authorship fails). Repair: D6's producer is "to be registered in the capstone" with the exact three-place relation (key, signature term, presented framed bytes) stated; C-Q7 keeps D5's transplant scope only.
2. **D10's named producer, `PossessionTransplanted`, does not establish possession over the accepted manifest.** ACCEPTED. S-P3's judge compares the proof term's original and accepted keys and never mentions the accepted manifest; Codex removed both manifest-binding protections in an S-P2 copy and `SetAltered` went red while that theorem held. Repair: D10's producer is "to be registered in the capstone" with a possession-over-the-accepted-manifest relation; independent of R-2.
3. **Companion failed-query sets are family-local, presented as exhaustive for the capstone.** ACCEPTED. §6's "any red outside the listed set is a broken fixture" is withdrawn for the composed fixture; expected sets are to be specified against the capstone's actual query names once the composed queries are defined; C-C1 must name D4's linkage failure explicitly.
4. **C-Q1 is not builder-ready; required retained queries are unlisted.** ACCEPTED. C-Q1 is rewritten as a query contract: event signatures, the correspondence tying evidence, manifest, possession proof, signature term, presented frame, signer slot and layer; strict vs degraded split with the honest-channel requirement stated per conclusion; and the retained checks (`Accept ⇒ IssuerSigned`, `Stripped`, `SignerForged`, `Spliced`, `TypeConfused`, `VersionLied`, honest-key authorship) listed as required queries.
5. **R-1's consequences contradict each other; D1/D2's conditions on R-1 and R-2 are stated inconsistently; the D11 vs L-16/L-17 convention is annotated, not repaired.** ACCEPTED, together with the skeptic's three findings of the same day (R-1's argument circular once D5 was withdrawn; A7 §A7.10's antecedent not established for D1/D2 because severing the producer leaves the consumer green; D11 convention). Repair: R-1 is restated in its honest form — under A7 §A7.10 as written, D1 and D2 are COMPLEMENTARY today (the consumer transcribes the check and its own query survives severing the producer), and they become capstone-internal joins only if the capstone's fixture composes the families' checks into one verifier; the combined consequences of R-1 × R-2 × R-3 are written as one table; L-13, L-16 and L-17 move together to a "conditional on R-3" sub-table so no complementary entry sits in the cross-model matrix.
6. **E18 record: the "exactly" qualification at `RESULTS-K6.md:47` conflicts with the summary at `:53`.** ACCEPTED; the summary sentence is corrected the same day.

**Method.** All cited lines opened. No committed model, amendment, tracker row or prediction file changes. The register's next state is the fourth repair; the author's confirm/overrule of R-1, R-2, R-3 waits for it.

## Codex review — verbatim

# 1. Producer–consumer determinations

Reviewed the whole register and both archived reviews. Repository files were unchanged. New paired diagnostics ran on copies under `/tmp/tessera-ledger-fourth-1qpc5wh4/`.

**1. C-Q7 does not establish D6’s signature-to-presented-bytes relation.**

L-06 calls two properties “equivalent”: binding a signature to the presented bytes, and preventing an honest signature term from being accepted under another key. They are not equivalent. C-Q7 observes only `(acceptedKey, signature)`, so it cannot detect presenting different bytes under the **same** key. Nevertheless, D6 names it as the producer of the chain’s exact-bytes link. (`formal/suite/LEDGER.md:262`, `:265`, `:574`, `:869`.)

I replaced the signature’s presented-byte equality with a check that its **signed** frame names the verification key, retaining the other checks:

| Diagnostic | C-Q7 transplant unreachable | Honest-key authorship | Honest acceptance |
|---|---|---|---|
| Baseline | Holds | Holds | Reachable |
| Same-key byte unbinding | Holds | **Fails** | Reachable |

Evidence: `/tmp/tessera-ledger-fourth-1qpc5wh4/base.out:203`, `:210`, `:386`; `same_key_unbound.pv:200`; `same_key_unbound.out:207`, `:372`, `:551`.

C-Q7 matches D5’s signature/key-transplant objective, subject to the composed fixture. It does **not** supply D6. Register an exact signature/key/presented-bytes relation for D6 and test that relation separately.

**2. D10 repeats the insufficient-producer defect: `PossessionTransplanted` does not establish possession over the accepted manifest.**

D10 names S-P3’s `PossessionTransplanted` unreachability as producer for S-P2’s `SetAltered`. But S-P3’s judge compares the proof term’s original and accepted **keys**; neither its report nor its test contains the accepted manifest. (`formal/suite/LEDGER.md:190`, `:191`, `:578`; `formal/suite/s-p3/proverif/sp3_q2_degraded_compromised.pv:137`.)

I added that judge to an unchanged S-P2 copy, then applied fingerprint-only possession and removed manifest-hash comparisons, retaining the seven-field frames and content guards:

| Diagnostic | Possession transplant unreachable | `SetAltered` unreachable |
|---|---|---|
| Instrumented baseline | Holds | Holds |
| Both manifest-binding protections removed | **Holds** | **Fails** |

All four other S-P2 safety queries remain green; both `HonestComplete` witnesses and `HonestAccepted` remain reachable. Evidence: `/tmp/tessera-ledger-fourth-1qpc5wh4/poss_base.out:433`, `:1066`; `poss_unbound.pv:167`, `:191`, `:207`; `poss_unbound.out:415`, `:424`, `:632`, `:641`, `:808`, `:1028`, `:1232`, `:1241`, `:1250`.

The consumer failure is real, but the named producer theorem survives it. D10 needs a producer query covering the accepted **manifest**, independently of the author’s R-2 decision.

### Every matrix row

“Shown” below means the cited consumer mutation, not capstone discharge.

| Row | Producer fact → consumer query | Does severing falsify the consumer? |
|---|---|---|
| D1 | Honest-byte/key binding → S-P2 `Reattributed` | **Shown**, complete two-removal mutation; classification remains conditional on R-1/R-2. `formal/suite/ledger-tests-2026-09-14/m4_framepin_mh.out:620`. |
| D2 | Same binding → S-P7 `Rescoped`, key half | **Shown**, complete inner mutation; R-1/R-2 remain. `formal/suite/ledger-tests-2026-09-14/s4_innerfp_mh.out:864`. |
| D3 | Strict authority/possession/signing correspondence → `Accept ⇒ IssuerSigned` | **Shown**, both channels compromised; honest-key correspondence survives. `formal/suite/ledger-tests-2026-09-14/s6_bothchannels.out:361`, `:368`. |
| D4 | D3’s producer → capstone first link | **Unestablished**: consumer absent. `formal/suite/LEDGER.md:572`. |
| D5 | Proposed signature-term/key binding → `InnerSigTransplanted` | Consumer red **shown**; proposed producer has matching transplant scope, but composed transfer remains unbuilt. `formal/suite/LEDGER.md:573`; `formal/suite/ledger-tests-2026-09-14/d5b_sp7_condunbind.out:1037`. |
| D6 | Proposed C-Q7 → exact signature/bytes link | **Insufficient producer**, finding 1; consumer absent. |
| D7 | Cardinality, membership, common content → per-signer linkage | **Unestablished**: existing reds concern producer-family queries, not the absent consumer. `formal/suite/LEDGER.md:575`. |
| D8 | Type soundness → per-layer linkage | **Unestablished** for the same reason. `formal/suite/LEDGER.md:576`. |
| D9 | Evidence/tuple uniqueness → capstone boundary judge | **Unestablished**: spike companions are red; capstone consumer absent. Pair-only scope is explicit. `formal/suite/LEDGER.md:577`. |
| D10 | Proof-term/key non-transplant → `SetAltered` | **Insufficient producer**, finding 2; manifest-binding removal makes the consumer red while that theorem holds. |
| D11 | Inner attribution/scope → wrapped-standing linkage | **Unestablished**: consumer formulation and composition await R-3. `formal/suite/LEDGER.md:579`. |

# 2. Companions

**3. The repaired failed-query sets describe isolated family runs, but are presented as exhaustive capstone sets.**

C-C1 serves **D3 and D4**, yet specifies `Accept ⇒ IssuerSigned` **only** as its failed set. D4 separately requires the capstone linkage query to fail. Section 6 says any red outside the listed set is a broken fixture. Thus the required D4 failure is either omitted or implicitly identified with another query without specifying that identification. (`formal/suite/LEDGER.md:572`, `:865`, `:882`, `:897`.)

Specify the expected sets against the actual capstone query names after defining the composed queries. Family-local outputs cannot establish an exhaustive result set for the enlarged fixture.

The cited local polarities otherwise match: C-C2 uses the two-removal mutation; C-C4 records all three failures; C-C6 distinguishes its mutation-induced failures from the pre-existing degraded-mode cost. C-C3’s added `Spliced` guarantee also survived the new diagnostic above. (`formal/suite/LEDGER.md:898`–`:902`; `/tmp/tessera-ledger-fourth-1qpc5wh4/poss_unbound.out:1241`.) C-C3’s remaining problem is its producer attribution, finding 2.

# 3. Builder-ready queries

**4. C-Q1 does not yet specify the query needed to decide several matrix rows.**

Its single sentence serves D4, D6, D7 and D8, but supplies no event signature or explicit correspondence tying together the evidence, manifest, possession proof, signature term, presented frame, signer slot and layer. These are precisely the distinctions on which findings 1 and 2 turn. (`formal/suite/LEDGER.md:865`; `docs/phase-0-prereg-amendment-3.md:115`–`:120`.)

The strict/degraded split also needs an explicit query contract. The register requires strict first-link provenance through D4 while several fixtures use a compromised sole channel; unrestricted authorship already fails in the latter baseline. A builder must know which conclusions are structural binding requirements and which require an honest authority channel. (`formal/suite/LEDGER.md:232`, `:267`, `:374`; `formal/suite/ledger-tests-2026-09-14/d5c_sp1_sigjudge.out:536`.)

Finally, the minimum query table never explicitly lists **D3’s own** `Accept ⇒ IssuerSigned` query, although C-C1 must falsify it. It also does not explicitly register several mandatory retained checks—`Stripped`, `SignerForged`, `Spliced`, `TypeConfused`, `VersionLied`, and honest-key authorship. Their appearance in companion requirements makes them required queries, not optional additions. (`formal/suite/LEDGER.md:863`–`:873`, `:897`–`:902`.)

Write the correspondences, fixtures, compromise cases, shared arguments and expected outcomes before approving the build plan.

# 4. Consistency and routed consequences

**5. R-1’s consequences still contradict each other and the matrix counts.**

R-1 first says Reading A removes **D1, D2 and D5**. It then says R-1 does **not** change D5’s state. Both instructions remain operative. (`formal/suite/LEDGER.md:724`–`:726`, `:739`–`:740`.)

Likewise, the consumer determinations explicitly condition D1/D2 on R-1 Reading B, but the matrix’s consequence paragraph says R-2 “yes” makes them firm without requiring that R-1 outcome. (`formal/suite/LEDGER.md:138`, `:139`, `:609`–`:612`.)

R-3 clearly distinguishes W’s additional standing dependencies from N’s narrower attribution claim. However, the register itself identifies the unresolved convention: complementary L-13 already occupies provisional D11, while equally conditional L-16/L-17 remain outside the matrix. That annotation identifies an unrepaired inconsistency; it does not repair it. (`formal/suite/LEDGER.md:424`, `:799`–`:829`.)

I do not resolve any fork. State their **combined** consequences consistently before treating the counts as decision-ready. The basic LAYER-2(a)/(b) repair is present: internal encoding and atomic-entry obligations now name E3/E6 rather than remaining assumptions forever. (`formal/suite/LEDGER.md:630`–`:670`.)

# 5. Previous accepted findings

| Accepted finding | Current verification |
|---|---|
| First review: single fingerprint-removal claim | **Repaired.** Single removal remains green; C-C2 requires the minimal successful pair. `formal/suite/LEDGER.md:158`, `:161`, `:898`. |
| Both reviews: D5’s insufficient authorship producer | **Partly repaired.** Old attribution withdrawn, D5 provisional, C-C5 appropriately limited. The replacement is incorrectly extended to D6: finding 1. `formal/suite/LEDGER.md:264`–`:276`. |
| First review: redundancy plus `SetAltered`/witness registration | **Repaired as requested.** C-Q5/C-Q5w and isolation evidence are present. D10 has the additional producer defect above. `formal/suite/LEDGER.md:870`, `:871`, `:899`. |
| First review: wrapper-existence claim | **Repaired.** The missing obligation is identified as composition. `formal/suite/LEDGER.md:424`. |
| Second review: signing-domain whitelist | **Substantively repaired.** TLR and REFUSAL are included and modeled-domain separation is required. `formal/suite/LEDGER.md:319`–`:339`. |
| Second review: common-content producer | **Repaired.** `Spliced`, the shared-field mapping and separate authorship obligation are explicit. `formal/suite/LEDGER.md:370`, `:371`, `:575`. |
| Second review: propagated routing consequences | **Partly repaired.** R-2 provisional status and W/N consequences are present; finding 5 remains. |
| Second review: companion result sets | **Repaired against local evidence.** Capstone-wide completeness remains unresolved, finding 3. |
| Second review: “Layer 2 forever” | **Repaired for the named internal obligations.** `formal/suite/LEDGER.md:657`–`:677`. |

The first review’s E18 findings concern artifacts outside this register. The bounded-instance qualification is present in `formal/tla/k6-2026-09-14/RESULTS-K6.md:133`. I cannot confirm the claimed complete repair of “exactly”: its local qualification at `:47` still conflicts with the summary at `:53`. This remains outside the ledger approval; the ledger correctly withholds E18 sign-off at `formal/suite/LEDGER.md:1028`.

**I would not yet approve this register as the capstone plan. The author should see first: (1) C-Q7 can remain green while D6’s exact-byte relation fails; (2) D10’s named possession theorem can remain green while `SetAltered` fails; and (3) C-Q1 and the companion result sets still need an explicit, consistent contract for the composed fixture. These are plan defects, not counterexamples to the unmutated Tessera construction.**

