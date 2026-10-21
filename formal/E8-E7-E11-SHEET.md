# E8 / E7 / E11 sheet for the V1 exit (`tessera-v1-strict`)

> **OWNER DRAFT 2026-10-19, revised after Codex review (docs/reviews/exit-pages/).** (Claude Opus 5.5, owner instance.) The "one-page
> E8/E7/E11 sheet" of A9.2 (`docs/phase-0-prereg-amendment-9.md:208`); item definitions at
> `formal/BAND0-EXIT.md:67-68, :71`; V1 scope "V1 queries only" and E8 as "C3 × C5"
> (`docs/V1-DERIVATION-DRAFT.md:131-132, :135`). It maps; it discharges nothing and changes no status. Paths are
> relative to `formal/` unless they start with `docs/`. `formal/p8/PROOF.md` is cited at commit `8ea8bfa` (its
> working copy is being edited today). The reading-aid line ranges were collected by a delegated read on
> 2026-10-19 and spot-checked by the owner; the reviewer must check them.

**V1 scope.** Strict only, one layer, no wrappers, no standing (`docs/phase-0-prereg-amendment-9.md:61, :161`).
A query is V1-relevant if it runs the strict verifier (leaks `skD` or `skR`, not `skS`) and concerns C1–C7.

## E8 — joins between the TLA+ and ProVerif models

ProVerif cannot consume a TLA+ result; every join is a ledger entry carried in prose and "never" marked
symbolically discharged (`suite/ENUMERATION.md:137-147`; `suite/LEDGER.md:919-937`). The capstone does not
discharge any of them (`suite/capstone/PREDICTIONS.md:1974-1981`).

| Join (ledger id) | Shared term | TLA+ producer | ProVerif consumer | V1? | Checked by |
|---|---|---|---|---|---|
| **L-05** | `Accept`/`AcceptS` ↔ P4's verdict partition | `tla/P4_VerifierStates.tla`: `Partition` :113, `NoSilentPromotion` :124, `ExactInvalid` :164, `ExactUnverifiable` :167 | S-P1 (`suite/s-p1/RESULTS.md:384-403`), S-P2 (`suite/s-p2/RESULTS.md:275-283`) | **Yes** (C1–C3 acceptance → C7 verdict) | **Nothing.** Prose only; "agreement unchecked" (`suite/LEDGER.md:927`; `COVERAGE-MAP.md:43`) |
| **L-19** | "anchor valid" (A2.1 predicate) | `tla/P5c_IssuanceProtocol.tla` `ShippedIsSound`, `ExpiredCannotShip`; bridge `PinAgreement`, `ShippedDesignatedAgree`, `LateBurialRejected` (`suite/LEDGER.md:929`) | S-STANDING C-2 only (`suite/s-standing/RESULTS.md:495-498`) | **No consumer in V1** (standing omitted) | Nothing; consumer check inert |
| **L-21** | refusal latch → terminal disposition | `tla/P5c_IssuanceProtocol.tla` `RefusedOnlyWhenExhausted`, `RefusalLatched`; extended invariant not built | S-STANDING C-5 | No (standing) | Producer incomplete (`suite/LEDGER.md:930`) |
| P9 premise | "the verdict is a pure function" | assumed in `tla/P4_VerifierStates.tla:7` and `tla/P5cP5P6_Bridge.tla:70` | none | Yes (C6) | Not a model; the textual basis is `formal/P9-CONTRACT-INSPECTION.md` (owner draft) |
| Negative records | S-P3, S-P2 and S-P7 consume no temporal join | — | L-03, L-11, L-15 (`suite/LEDGER.md:931-933`) | — | Recorded |

**L-05 correspondence, in prose (XP-06).** L-05 maps strict `Accept` to P4 with no waivers and every required check passed. Failed checks map to INVALID. Unperformable checks without failures map to UNVERIFIABLE. ProVerif's silent stopping does not itself establish that distinction. This is a prose correspondence, not a proof of composition (A1 §A1.4, `docs/phase-0-prereg-amendment-1.md:397-406`; `suite/LEDGER.md:935-937`).

TLA+ ↔ TLA+ (not cross-formalism): P5c and P5P6 agree through the bridge, checked (`PROPERTIES.md:101-103`;
`COVERAGE-MAP.md:27`).

## What composition is NOT proved

1. **No model holds signatures and time together.** The ProVerif models represent no time. The temporal TLA+
   model abstracts "signature checks … as passing" (`tla/P5P6_TemporalRevocation.tla:54-56`). So no model shows that
   one receipt meets C1–C3 and C5 at once. The only joins are L-05 and L-19, both prose (table above).
2. **"The signatures existed by T" is not modelled.** The signature-inclusive anchor (`A_sig`) is an assumption
   on both sides (`docs/V1-CONTRACT.md:90`).
3. **Terms are not bytes.** In ProVerif "the same bytes" means "the same term" (`suite/s-p1/READING-AIDS.md:257-259`).
   The byte link is P8: a prose proof plus vectors, not machine-checked (`docs/phase-0-prereg-amendment-9.md:203-204`).
4. **The capstone composes ProVerif families only.** It stays open: the author deferred two routed questions on
   2026-10-07 (`suite/capstone/RESULTS.md:5`), and "Nothing below is discharged by this file"
   (`suite/capstone/RESULTS.md:627-628`).
5. **No model at all** for G6 (UTC bound), G7's window endpoints, or concrete DNSSEC and git authority
   (`docs/V1-CONTRACT.md:98-99`); none for P9 (`COVERAGE-MAP.md:32`).
6. **n = 2 is enumerated, not generalized** (`suite/s-p1/READING-AIDS.md:346-348`).

## E7 — V1-relevant queries and their A1.2 property

`PROPERTIES.md:98` (the E7 box) stays unticked; the gaps below are why. E7 requires a mapping for each symbolic lemma; explicit inherited mappings count, and the TLA+ invariant rows provide context rather than additional E7 prerequisites (A1:391-395; `BAND0-EXIT.md:67`). The "Partial" state on the TLA+ rows below is context only and is not an E7 gap.

| Query (model) | V1 claim | Property | Mapping sentence | State |
|---|---|---|---|---|
| S-P1 Q1d `sp1_q1_strict_dns_compromised.pv`, three queries (`suite/s-p1/proverif/sp1_q1_strict_dns_compromised.pv:144-154`) | C1, C2 | P1 | For Q1d and Q1r, query (i) maps to P1's existential issuance-event authenticity (C2; A3:68-74), query (ii) to honest-key byte binding (C1; "P1's binding half", `suite/s-p1/READING-AIDS.md:334-335`), and query (iii) supplies a reachability witness. | OK |
| S-P1 Q1r (repo leaked) | C1, C2 | P1 | Inherits Q1d's tables with the channels exchanged, `suite/s-p1/READING-AIDS.md:368-378`; this inherited mapping counts. | OK (inherited) |
| S-P2 Q1d, Q1r | C3 | P2 | refer to §1d, `suite/s-p2/READING-AIDS.md:382`; only Q2 is labelled "the P2 claim" (:50) | GAP |
| S-P3 Q1d, Q1r | C3, C4 binding | P3 [model] | only Q2 labelled "the P3 claim" (`suite/s-p3/READING-AIDS.md:28`) | GAP |
| S-P7 Q1d, Q1r | C1 type separation | P7 | labelled "the C2 claim" (S-P7's own numbering), `suite/s-p7/READING-AIDS.md:35`; P7 named only at :47 | GAP |
| First-link Q1 `q1_chain_*` | C4 | P10 | `PROPERTIES.md:45` only; no reading aid | GAP |
| First-link Q3 | C4 | P10 | "Correspondence to P10", `spike/first-link/READING-AID-Q3.md:184-187` | OK; possession signs tag and fingerprint, not manifest bytes (:188) |
| P4 invariants | C7 | P4 | "the four P4 states", `tla/READING-AID-P4.md:163`; check rows :188-198 cite A1 text, no P-label | Partial |
| P5P6 invariants | C5 | P5 (P6 not evaluated in V1) | `tla/READING-AID-P5P6.md:195-196, :201, :432`; rows 3–6 have no P-number | Partial |
| P5c invariants | C5 issuance | P5c | `tla/READING-AID-P5c.md:190` (row 1 only) | Partial |
| Capstone strict cases (a)–(c), C-Q1…C-Q10 | C1–C4 | P1, P2, P3, P7, P10 | Owner token scan of `suite/capstone/PREDICTIONS.md:312-1483`: property names appear in C-Q1 links 1b, 2a, 2b, 4, 5, 6a; C-Q3, C-Q5, C-Q8, C-Q9 | GAP: none in link 1a, link 3, C-Q2, C-Q7, C-Q10; a name is not yet a checked mapping sentence |

**Finding.** The two-signer and common-content queries (S-P3 Q5c, S-P2 Q6) run only in degraded models. V1 has two
required signers. Their strict form exists only in the capstone: D1 `ReattributedA/B` and D7 `Spliced`, green in
case (a) (`suite/capstone/RESULTS.md:633, :639`). Not V1: every degraded query (`skS` leaked), every S-STANDING
query, wrapper scope and standing queries (C-Q4, C-Q6, link 6b), and S-P7 Q7.

## E11 — index of plain-language statements (claim, adversary, boundary)

| Model | Claim | Adversary | Boundary |
|---|---|---|---|
| [S-P1](suite/s-p1/READING-AIDS.md) Q1d / Q1r (strict) | :331-335 | :337-338 | :346-357 |
| S-P1 Q2 (degraded) | :227-234 | :236-241 | :252-287 |
| [S-P2](suite/s-p2/READING-AIDS.md) Q2; Q1d/Q1r inherit | :233-249; :382-389 | :251-256 | :271-278 |
| S-P2 Q6 (common content) | :736-743 | sole authority channel compromised (:736-738), with the inherited capabilities at :251-256 | :765-772 |
| [S-P3](suite/s-p3/READING-AIDS.md) Q1d (strict) | :197-205 | :207-212 | :223-232 |
| S-P3 Q2; Q5c (two signers) | :321-328; :591-595 | :330-334; :597 | :367-376; :605-611 |
| [S-P7](suite/s-p7/READING-AIDS.md) Q2; Q1d/Q1r | :232-260; :365-371 | :262-267 | :281-292 |
| [S-STANDING](suite/s-standing/READING-AIDS.md) Q1d (not V1) | :303-311 | :313-318 | :335-353 |
| [First link Q3](spike/first-link/READING-AID-Q3.md) (P10) | :153-157 | :159-165 | :173-182 |
| [P4](tla/READING-AID-P4.md) | :270-290; Part B :365-369 | :284-285; :371-375 | :241-268; :387-393 |
| [P5P6](tla/READING-AID-P5P6.md) | :283-306; :396-400 | :299-301; :402-408 | :247-281; :421-428 |
| [P5c](tla/READING-AID-P5c.md) (k = 6 note :444-464) | :302-325; :409-413 | none (:318-320); :415-421 | :257-300; :429-436 |
| V1 capstone, strict evidence (XP-08; interim owner statement, Codex text) | One-acceptance linkage is tested | Attackers holding one or both authority credentials | Both-channel capture loses unrestricted service-origin assurance; no result establishes time, concrete encoding or implementation conformance |
| [P8 prose proof](p8/PROOF.md) | "What P8 says", `8ea8bfa`:33-36 | **missing** | "What is not claimed", `8ea8bfa`:416-420 |
| [P9 probe](spike/tla-probes/P9/RESULTS-PROBE.md) (non-discharging) | :319 | "None", :325 | :329 |

**Missing statements (gaps).** The capstone row above is an interim statement for the strict evidence this sheet uses. It is not the full capstone statement, which `suite/capstone/PREDICTIONS.md:2019-2023` expects and which `suite/capstone/RESULTS.md:1017` says must carry finding G2 (A4:127-135; A9:207-208). No plain statement for: `tla/P5cP5P6_Bridge.tla` and the
BridgeSlack modules (described only inside the P5c and P5P6 aids); the k = 6 runs in `tla/k6-2026-09-14/`;
first-link Q1, Q2 and Q4–Q8; the P10 TLA+ probe. P8 has no adversary statement. The E6a P4 transition was not begun at the
exit audit (`docs/V1-EXIT-30OCT.md:116-118`); `tla/E6a/` appeared during this draft and has no reading aid.
