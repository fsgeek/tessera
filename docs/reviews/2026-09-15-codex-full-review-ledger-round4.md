# Codex non-author full review of the ledger register, fourth round (2026-09-15)

Reviewer: OpenAI Codex CLI (`gpt-6-astra`), run non-interactively by the
owner instance against the whole of `formal/suite/LEDGER.md` after the
fourth repair (scratch diagnostics under
`/tmp/tessera-ledger-fifth-1vwu7d_p/`). The reviewer would not yet
approve the register as the capstone plan; its four findings concern
the proposed proof contract (C-Q1, C-Q8), not the register's entries or
the construction. Every factual claim below was checked against the
tree before disposition.

## Dispositions (owner instance, 2026-09-15)

1. **C-Q8 quantifies over honest-released signature terms only, so a same-key unbinding of non-`OT_ATTEST` frames escapes it.** ACCEPTED. The structural producer must be a judge over every accepted `(key, signature, presented bytes)` triple, including failed verification, separate from any honest-origin or transplant claim. C-Q8 is rewritten so; C-C7 is re-specified against it.
2. **C-Q1 link 6 conflates object type with innermost-issuer scope; only `TypeConfused` is named as producer.** ACCEPTED. Link 6 is split into a type obligation (producer `TypeConfused`) and a scope obligation (producer `Rescoped`, S-P7 Q6b's separation cited). Consequence for R-3: C-Q1 consumes scope unconditionally under every formulation, so L-13's consumption is no longer conditional on R-3; R-3 decides only whether the standing conjuncts (L-16/L-17) are consumed. The routed item and the combined-consequences table are corrected accordingly.
3. **C-Q1 drops accepted-evidence binding in degraded mode.** ACCEPTED. `LayerAccepted` carries the evidence term (or a reference) and C-Q1 requires evidence-to-this-acceptance binding in both modes; only the honest-publication conclusion is dropped in degraded-compromised mode, per A3 §A3.2's fewer-but-never-zero evidence.
4. **C-Q1's per-slot contract does not express required-set completeness within one acceptance.** ACCEPTED. `LayerAccepted` gains an acceptance identifier (or the aggregate package term) and C-Q1 requires a slot record for every required slot grouped under that acceptance; D7's companion is re-specified to falsify C-Q1, not only `Stripped`.

**Termination of the review loop.** Four rounds have moved the register from misclassified entries to a contract with named gaps. After this repair the three routed forks go to the author; the contract (C-Q1–C-Q9, companions C-C1–C-C8) is re-verified by a non-author pass when the capstone's `PREDICTIONS.md` is drafted and before it is frozen, which is where a contract defect would otherwise bite. E18 sign-off is separately owed.

## Codex review — verbatim

## 1. Producer–consumer determinations

Read all three archived reviews first, then the whole register and governing texts. Repository unchanged. Six diagnostic runs on copies completed under `/tmp/tessera-ledger-fifth-1vwu7d_p/`.

**1. D6’s replacement producer C-Q8 still does not establish the stated relation.**

C-Q1 requires `checksign(sg, kX) = (BYTES, fb)` for **every acceptance**, including degraded acceptance. But C-Q8 examines only signature terms previously released by an honest issuer. Attacker-created signatures are outside its observation. (`formal/suite/LEDGER.md:1077`, `:1116`, `:1137`; `formal/suite/ledger-tests-2026-09-14/d6a_sp1_q8_base.pv:255–260`.)

I retained byte equality for signatures over `OT_ATTEST`—covering every honest signature in this fixture—but permitted unbinding for other signed frame types. An independent judge checked the exact relation without the honest-signature filter.

| Diagnostic | C-Q8 holds | Exact byte relation holds | Honest acceptance |
|---|---|---|---|
| Baseline | Yes | Yes | Reachable |
| Conditional unbinding | **Yes** | **No** | Reachable |

Evidence: `/tmp/tessera-ledger-fifth-1vwu7d_p/bytes_base.out:264–278`, `:455`; `bytes_foreign_unbound.pv:217–219`; `bytes_foreign_unbound.out:268`, `:460`, `:645`.

**Repair:** make the structural producer inspect every accepted `(key, signature, presented bytes)` triple, including failed verification. Keep honest-signature origin/transplant claims separate. Merely adding the third argument did not remove the quantifier mismatch.

**2. C-Q1 assigns an identity-scope conclusion to D8’s type-soundness producer.**

Link 6 requires both correct object type and innermost-issuer attribution, but names only `TypeConfused` as its producer. Those are independent properties. (`formal/suite/LEDGER.md:1118`; D8 at `:629`.)

The existing Q6b companion already separates them:

- `TypeConfused` remains unreachable.
- `Rescoped` becomes reachable.
- Both honest witnesses remain reachable.

Evidence: `formal/suite/s-p7/proverif/sp7_q6b_companion_key_outermost.out:489`, `:769`, `:1317`, `:1508`.

**Repair:** split link 6’s type and scope obligations and name the scope producer explicitly. This also affects routing: C-Q1 already requires scope unconditionally, while L-13’s capstone consumption is presented as conditional on R-3. (`formal/suite/LEDGER.md:434`, `:969–974`.)

### Every matrix row

“Shown” means consumer failure in the cited family/copy, **not capstone discharge**.

| Row | Producer fact → consumer query | Does severing falsify the consumer? |
|---|---|---|
| D1 | Key binding → S-P2 `Reattributed` | Complete local severing: **shown**. Producer-model removal: no effect; correctly held out pending R-1/R-2. `formal/suite/LEDGER.md:651`. |
| D2 | Key binding → S-P7 `Rescoped` | Complete inner severing: **shown**. Same routing qualification. `formal/suite/LEDGER.md:652`. |
| D3 | Strict authority/possession/signing correspondence → `Accept ⇒ IssuerSigned` | **Shown** with both channels compromised. `formal/suite/ledger-tests-2026-09-14/s6_bothchannels.out:361–368`. |
| D4 | Strict authority provenance → C-Q1 first link | **Not yet shown**; consumer unbuilt. Its evidence-binding contract also needs finding 3’s repair. `formal/suite/LEDGER.md:625`. |
| D5 | Proposed signature-term/key non-transplant → `InnerSigTransplanted` | Consumer failure **shown**; C-Q7 matches transplant scope, composed transfer unbuilt. `formal/suite/LEDGER.md:626`. |
| D6 | Proposed C-Q8 → exact signature/bytes link | **Insufficient producer**, finding 1. `formal/suite/LEDGER.md:627`. |
| D7 | Completeness, membership, common content → per-signer chain | Family failures shown; **consumer failure unestablished**, and its completeness contract is missing: finding 4. `formal/suite/LEDGER.md:628`. |
| D8 | Type soundness → per-layer chain | Type failure shown locally; **does not supply added scope conjunct**, finding 2. `formal/suite/LEDGER.md:629`. |
| D9 | Evidence/tuple uniqueness → pair boundary judge | Spike failure shown; **capstone consumer unbuilt**. Pair-only limitation explicit. `formal/suite/LEDGER.md:630`. |
| D10 | Proposed possession over accepted manifest → `SetAltered` | Combined-removal failure **shown**; C-Q9 now checks the accepted manifest. R-2 and composition remain open. `formal/suite/ledger-tests-2026-09-14/d10b_sp2_q9_manifest_unbound.out:673`, `:1462`. |
| D11 | Inner attribution/scope → wrapped-standing linkage | **Not yet shown**; conditional consumer unbuilt. `formal/suite/LEDGER.md:670`. |
| D12 | Standing designation → W’s standing conjunct | **Not yet shown**; conditional consumer unbuilt. `formal/suite/LEDGER.md:671`. |
| D13 | Entitled-key match → W’s key conjunct | **Not yet shown**; conditional consumer unbuilt. `formal/suite/LEDGER.md:672`. |

## 2. Companions

No additional mismatch found between C-C1–C-C8’s **family-local** failed sets, retained guarantees, witnesses and their cited outputs. The distinction between mutation-induced failures and pre-existing degraded-mode failures is now explicit. (`formal/suite/LEDGER.md:1236–1243`.)

The previous exhaustive-capstone-set defect is repaired: enlarged-fixture expectations must be specified before predictions freeze, and C-C1 explicitly requires D4’s linkage failure. (`formal/suite/LEDGER.md:1201–1222`, `:1236`.)

However, C-C7’s successful falsification of C-Q8 does **not** establish that C-Q8 covers D6’s whole relation; finding 1 supplies a mutation it misses.

## 3. Builder-ready queries

**3. C-Q1 omits the actual accepted-evidence binding, especially in degraded mode.**

`AuthorityEvidence` is declared, but `LayerAccepted` carries neither its evidence term nor a reference tying that validation to this acceptance. Link 1 instead asks whether an honest authority published `t`; degraded mode drops that link entirely. None of links 2–6 then requires external evidence. (`formal/suite/LEDGER.md:1101–1118`, `:1136–1143`.)

That is weaker than A3.2’s chain beginning with **accepted external evidence bound to the consumed statement**, with fewer-but-never-zero evidence even under waiver. (`docs/phase-0-prereg-amendment-3.md:115–120`, `:142–150`.)

A diagnostic removed only the degraded verifier’s evidence check. An explicit evidence-binding query changed from green to red; C-Q8, exact signature/byte binding, honest-key authorship and honest acceptance retained their baseline outcomes. Evidence: `/tmp/tessera-ledger-fifth-1vwu7d_p/evidence_unchecked.pv:214–226`; `evidence_base.out:290–304`; `evidence_unchecked.out:428–442`, `:606`.

**Repair:** retain an evidence-to-this-acceptance binding requirement in both modes. Drop only the honest-publication conclusion in degraded-compromised mode. A declared but unconsumed `AuthorityEvidence` event does not close this link.

**4. C-Q1’s per-slot contract does not express D7’s required-set completeness.**

The correspondence quantifies over observed `LayerAccepted` reports and checks that each reported slot belongs to the manifest. It never requires a report for **every required slot**. Its event also lacks an acceptance identifier or aggregate package term tying two slots to the same acceptance. (`formal/suite/LEDGER.md:1102`, `:1106–1117`.)

Removing the one-signer branch’s `signers0` requirement demonstrates the distinction:

- Every reported slot still belongs to the manifest and matches its key.
- `Stripped` becomes reachable.
- `Spliced`, the other safety queries and all honest witnesses retain their expected outcomes.

Evidence: `/tmp/tessera-ledger-fifth-1vwu7d_p/slots_missing.pv:199`; `slots_base.out:407–435`; `slots_missing.out:407`, `:580–601`, `:766`, `:984`, `:1213–1220`.

**Repair:** specify acceptance of the complete required set, with all slot records grouped into that same acceptance. Registering standalone `Stripped` is useful, but does not make C-Q1 consume completeness or ensure D7’s companion falsifies C-Q1. (`formal/suite/LEDGER.md:628`, `:1180`.)

## 4. Consistency and routed consequences

The default eight-row count, five existing producers, three provisional producers, and separate held-out/conditional tables agree internally. The LAYER-2(a)/(b) repair correctly assigns internal encoding and atomic-entry obligations to E3/E6. (`formal/suite/LEDGER.md:686–698`, `:782–794`.)

R-1 and R-2 now state their combined consequences consistently without requiring this reviewer to decide them. R-3 distinguishes W, N and no composition query, but **its consequences are not yet complete because C-Q1 already consumes scope**, as finding 2 explains. (`formal/suite/LEDGER.md:997–1025`, `:1118`.)

## 5. Previous accepted findings

| Accepted finding | Verification |
|---|---|
| First review: fingerprint-only removal was insufficient | **Repaired:** minimal two-removal C-C2 and retained guarantees agree with evidence. `formal/suite/LEDGER.md:174`, `:1237`. |
| First/second reviews: D5’s authorship producer was insufficient | **Repaired for D5:** old producer withdrawn; C-Q7 scoped to transplant. D6’s replacement remains defective under finding 1. `formal/suite/LEDGER.md:280–283`. |
| First review: redundancy and missing `SetAltered`/witness | **Repaired.** `formal/suite/LEDGER.md:1079–1080`, `:1238`. |
| First review: wrapper-existence assertion | **Repaired:** missing composition distinguished from existing wrapper-shaped terms. `formal/suite/LEDGER.md:442`. |
| Second review: signing-domain whitelist | **Repaired:** TLR/REFUSAL included; modeled versus external endpoints distinguished. `formal/suite/LEDGER.md:337–365`. |
| Second review: common-content producer omitted | **Repaired:** `Spliced` and shared fields named. C-Q1 completeness remains finding 4. `formal/suite/LEDGER.md:388–389`. |
| Second/third reviews: routing and complementary-row convention | **Substantially repaired:** separate tables and combined outcomes. New unconditional scope consumption remains finding 2. `formal/suite/LEDGER.md:633–672`, `:997–1025`. |
| Second/third reviews: companion failed sets | **Repaired against local evidence**, with capstone re-specification explicitly owed. `formal/suite/LEDGER.md:1201–1243`. |
| Second review: internal obligations classified “forever” | **Repaired.** `formal/suite/LEDGER.md:774–794`. |
| Third review: C-Q7 incorrectly supplied D6 | **Old attribution repaired; replacement insufficient**, finding 1. `formal/suite/LEDGER.md:1077`. |
| Third review: key-only possession theorem supplied D10 | **Repaired:** C-Q9 checks the exact accepted manifest, including verification failure. `formal/suite/ledger-tests-2026-09-14/d10a_sp2_q9_base.pv:335–339`. |
| Third review: C-Q1 contract and retained queries missing | **Partly repaired:** retained queries are listed; contract gaps remain findings 2–4. `formal/suite/LEDGER.md:1176–1188`. |
| E18 bounded-instance and “exactly” qualifications | **Repaired in the current external record’s wording.** This is not E18 sign-off. `formal/tla/k6-2026-09-14/RESULTS-K6.md:47–56`, `:134–138`. |

**I would not yet approve this register as the capstone plan. The author should see first: (1) C-Q8 still permits D6’s exact-byte relation to fail while its producer query stays green; (2) C-Q1 drops accepted-evidence binding from the degraded chain; and (3) C-Q1 does not require every named signer within one acceptance. The type-versus-scope mismatch also needs repair before R-3’s consequences are decision-ready. These are defects in the proposed proof contract, not counterexamples to the unmutated construction.**

