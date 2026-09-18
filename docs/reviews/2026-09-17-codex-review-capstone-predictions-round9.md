# Codex non-author review of the capstone registration, ninth round (2026-09-17)

Reviewer: OpenAI Codex CLI (`gpt-6-astra`), run non-interactively by the
owner instance on 2026-09-17 (19:46–19:56 UTC) against the whole of
`formal/suite/capstone/PREDICTIONS.md` after the round-eight repairs,
with one explicit test requested (C-C6); scratch diagnostics on
family-model copies under `/tmp/tessera-capstone-r9/`. **The reviewer
found the registration not ready to freeze**, on three findings — one
builder-choice gap in the report contract, one contradicted prediction,
one swapped citation — and confirms the round-eight label retirement
holds, that no whole configuration is still called a descended green
control, and that all twenty-eight earlier accepted findings are
present. Every run the reviewer cites was reproduced on our tree
(`formal/suite/ledger-tests-2026-09-14/cap22a`–`cap22j`, thirteenth
batch of that directory's README) at the reviewer's own `.out` line
numbers. No capstone model exists; nothing in the repository was run.

## Dispositions (owner instance, 2026-09-17)

All are **clerk dispositions** of the owner instance. Disposition 1
fixes a contract term and is marked **contestable**.

1. **Under a companion, which terms an inner acceptance reports is a
   choice that changes C-Q9's result.** ACCEPTED, and the term fixed.
   C-C15(i)'s strict transcription checks the outer possession proof
   and then verifies the inner signature under `kW`; it never checks the
   presented inner `tI` or `ppfI`. What the inner acceptance then
   **reports** to the judges was unspecified. Reproduced: with the
   C-Q9 judge added and the inner acceptance reporting the **presented
   inner** `(kW, tI, ppfI)`, C-Q9 is **red** in both channel variants
   (`cap22e_sp7_strict_q6b_q9_inner.out:1334`; `cap22f_…_repo.out:1334`)
   while the four S-P7 queries stay green and the witnesses reachable
   (`:569`–`:596`, `:871`, `:1075`); reporting the **checked outer**
   `(kW, tW, ppfW)` instead makes it **green** (`cap22g_…_outer.out:1084`);
   the unchanged strict baseline with its checked inner terms is green
   (`cap22d_sp7_strict_base_q9.out:1186`). **The term, contestable:**
   under every companion, `LayerAccepted` and every judge report at a
   layer carry **the terms that layer's acceptance was about** — the
   presented `(t, ppf, sg, fb)` of that layer under the key the
   (mutated) verifier verified against — and **never** terms checked at
   another layer. This is already what the immutable join requires
   (`t = tI`, `ppf = ppfI`, §3 C-Q6 (3)); it is now stated in §1.3 as
   the report contract so a builder cannot make a companion's failure
   invisible by reporting what it did check. **Consequence for
   C-C15(i):** C-Q9 and link 3 move from *predicted green* to
   **descended red** in (a) and (b); the outer-report reading is
   recorded as the rejected alternative with `cap22g` as its evidence.
   The repair step checks every other companion that changes the key
   or layer an inner term is verified against (C-C4, C-C15(ii), (iii))
   for the same dependence and states the reported terms explicitly.

2. **C-C8's strict manifest-hash prediction is contradicted by a direct
   judge.** ACCEPTED. The round-eight cell predicted link 5's `mh` half
   red in strict "descended by `cap18c`'s C-Q9 judge"; C-Q9 tests the
   possession message, not the frame's manifest hash. Reproduced: a
   judge firing on `mh ≠ h(t)` for each accepted slot is **green** on
   the strict C-C8 mutant in both variants
   (`cap22h_sp2_strict_cc8_mh.out:1478`; `cap22i_…_repo.out:1477`) while
   C-Q9 stays red (`:1466`, `:1465`) and the witnesses reachable; on the
   degraded source it is **red** (`cap22j_sp2_degraded_cc8_mh.out:1665`,
   with `SetAltered` red `:701` and C-Q9 red `:1499`). **Repair:**
   C-C8's strict cell lists link 5's `mh` half as **descended green**
   (the honest channel's tuple pin keeps `mh = h(t)` even with the
   guard dropped), link 3 and C-Q9 descended red, C-Q5 descended green;
   the claimed C-Q9 basis is withdrawn, quoted; the (β)-only strict
   split is stated as what the runs show.

3. **C-C7(i)'s two C-Q8 citations are swapped.** ACCEPTED. In
   `cap17b_sp1_strict_cc7i.out`, `:533` is `SigBytesUnbound` (the
   round-3, honest-filtered form) and `:709` is `SigBytesUnboundAll`
   (the structural form); both red. The cell's attributions are
   exchanged. Same polarity, corrected attribution.

4. **C-C6, the requested test.** Recorded. With C-C6's conditional
   unbinding on the strict S-P7 copy with the wrapped byte-binding
   judge and same-key wrapping retained, **every declared query is
   green and both witnesses reachable** in both variants
   (`cap22b_sp7_strict_cc6.out:692`–`:812`, `:1161`, `:1386`;
   `cap22c_…_repo.out:693`–`:817`, `:1167`, `:1393`; baseline
   `cap22a:594`–`:658`). The same-key wrapper frame names the verifying
   key's fingerprint, so C-C6's waiver demands byte equality on that
   route and C-C5's strict failure does not reproduce. **Repair:** C-C6's
   strict cell: descended green on the five declared queries and two
   witnesses; C-Q7 and the linkage conjuncts predicted green; a
   **predicted** green control at the configuration level; "predicts
   neither colour" withdrawn, quoted.

5. **The REFUSAL fork stands**, unresolved, owed at the freeze commit;
   the three earlier contestable choices stand and a fourth (the report
   contract of disposition 1) joins them.

**Loop.** One repair pass (Opus), then a tenth owner-run full Codex
pass.

## Codex review — verbatim

## 1. Query strength and event contracts

**1. C-C15(i)’s predicted C-Q9 green depends on an unspecified choice of inner-report arguments.**

The strict cell predicts C-Q9 and link 3 green. Its cited model checks the **outer** possession proof, then accepts the inner signature under `kW`; it never checks the presented `tI` or `ppfI`. The general event contract names the “accepted” tuple and proof without specifying their replacement in this companion. (`formal/suite/capstone/PREDICTIONS.md:168`, `:2131`; `formal/suite/ledger-tests-2026-09-14/cap14b_sp7_q1_strict_q6b.pv:215–234`.)

I added the structural C-Q9 judge, including verification failure, without changing verifier checks:

| Report at inner acceptance | DNS compromised | Repository compromised |
|---|---|---|
| `(kW,tI,ppfI)` — presented inner tuple/proof | Red | Red |
| `(kW,tW,ppfW)` — checked outer tuple/proof | Green | Not run |

The unchanged strict baseline with its checked inner terms is green. The red trace accepts an honest wrapper and inner signature while the attacker supplies arbitrary inner tuple/proof values. (`/tmp/tessera-capstone-r9/cap14a_sp7_q1_strict_base_q9.out:1186`; `/tmp/tessera-capstone-r9/cap14b_sp7_q1_strict_q6b_q9.out:1327–1334`; `/tmp/tessera-capstone-r9/cc15_inner_projection_repo.out:1334`; `/tmp/tessera-capstone-r9/cc15_outer_projection.out:1084`.)

**Required repair:** specify C-C15(i)’s inner `LayerAccepted` tuple, evidence, slot and possession-proof arguments, and reconcile that mapping with the immutable inner-term join. Retaining byte binding establishes neither this possession relation nor that mapping. This is a consequential builder choice, not an unconditional counterexample to every possible transcription. (`formal/suite/capstone/PREDICTIONS.md:866–881`, `:1260–1267`.)

## 2. Companion outcomes and witnesses

**2. C-C8’s strict manifest-hash prediction is contradicted by a direct judge on its cited shape.**

The latest Cases cell predicts **both link 3 and link 5’s `mh` half red**, claiming their relation descends from cap18c’s C-Q9 judge. C-Q9 tests the possession message; it does not test the frame’s manifest hash. (`formal/suite/capstone/PREDICTIONS.md:1530`.)

On copies of cap18c, I reported each accepted slot’s `(t,frame)` and tested exactly `mh ≠ h(t)`:

| C-C8 projection | C-Q9 | Wrong frame manifest hash |
|---|---|---|
| Strict, DNS compromised | Red | **Green** |
| Strict, repository compromised | Red | **Green** |
| Degraded source, control | Red | **Red** |

All existing honest witnesses remained reachable. The added judge is at `/tmp/tessera-capstone-r9/cap18c_sp2_strict_cc8_mh.pv:371–374`; results are at its `.out:1466–1478`, `/tmp/tessera-capstone-r9/cc8_mh_repo.out:1465–1477`, and `/tmp/tessera-capstone-r9/d10b_sp2_q9_manifest_unbound_mh.out:1499–1665`.

**Required repair:** separate the strict possession failure from the manifest-hash prediction and withdraw the claimed C-Q9 basis for the latter. These are family-projection results, not a completed capstone proof.

**Requested C-C6 experiment.** I applied its conditional unbinding to cap21b’s strict wrapped-byte-judge shape, preserving same-key wrapping and changing only the leaked channel between variants.

| Declared query or witness | DNS compromised | Repository compromised |
|---|---|---|
| `BytesUnbound` — wrapped C-Q8 relation | Green | Green |
| `TypeConfused` | Green | Green |
| `Rescoped` | Green | Green |
| `InnerSigTransplanted` | Green | Green |
| `Reattributed` | Green | Green |
| `HonestWrappedAccepted` | Reachable | Reachable |
| `HonestAccepted` | Reachable | Reachable |

Results: `/tmp/tessera-capstone-r9/cc6_dns.out:692–1386` and `/tmp/tessera-capstone-r9/cc6_repo.out:693–1393`. The same-key wrapper frame names the verifying key’s fingerprint, so this route requires byte equality. It does **not** reproduce C-C5’s strict failure. Generic C-Q7 and the full capstone linkage query are undeclared in these copies; no whole-configuration green conclusion follows. This answers the open question at `formal/suite/capstone/PREDICTIONS.md:1528`.

## 3. Prediction bases and descent audit

**3. C-C7(i)’s strict cell reverses its two C-Q8 citations.**

It labels cap17b `:533` structural and `:709` honest-filtered. The output has `SigBytesUnbound` at `:533` and `SigBytesUnboundAll` at `:709`. Both are red, so this changes attribution, not polarity. (`formal/suite/capstone/PREDICTIONS.md:1529`; `formal/suite/ledger-tests-2026-09-14/cap17b_sp1_strict_cc7i.out:533`, `:709`.)

The retirement otherwise holds in the operative Cases entries: I found no surviving assertion that a whole configuration is a **descended green control**, and no additional per-query descent to a copy lacking that query. Explicitly withdrawn quotations are not operative predictions. (`formal/suite/capstone/PREDICTIONS.md:1484–1519`, `:3036`.)

Finding 1 identifies a predicted green contradicted under the presented-inner reporting interpretation. Finding 2 identifies an unsupported, contradicted red prediction. I found no additional supported probability defect.

## 4. Builder completeness

Finding 1 is the remaining demonstrated builder gap: a clerk can select report arguments that change C-Q9’s result without changing verifier behavior.

The same-key wrapping and compromised-channel-only enrollment choices remain explicit. I do not reverse either choice; the C-C6 result above is a consequence of them. (`formal/suite/capstone/PREDICTIONS.md:65–67`.)

## 5. Routed fork

The `REFUSAL` fork is genuine and states both options and costs: add the honest tagged signer and amend the query/companion registration, or leave the domain unexercised and accept the resulting coverage limit. I leave that decision to the author. (`formal/suite/capstone/PREDICTIONS.md:1759–1780`.)

Finding 1 exposes a separate reporting choice that should not remain with the builder.

## 6. Earlier accepted findings and ledger corrections

I checked all eight disposition records against the current operative text. All **28 accepted repairs are present**; that does not validate the newly expanded prediction lists.

| Repairs | Current repair anchors |
|---|---|
| Round 1: six | D7/common content and C-C16; C-C8 isolation; C-C15 retained set; standing join; one-key/one-manifest; withdrawal of builder completeness (`PREDICTIONS.md:582–615`, `:866–881`, `:1808–1854`, `:2131`, `:2174–2175`, `:2237`) |
| Round 2: four | Independent intake/standing emission, C-C15 C-Q7, wrapper-signature consequences, structural judges (`PREDICTIONS.md:115–162`, `:744–837`, `:1237–1272`, `:1529`, `:2131`) |
| Round 3: four | Layer-indexed completeness, scope agreement, immutable join, diagnostic basis (`PREDICTIONS.md:351–396`, `:866–881`, `:995–1016`, `:1097–1137`) |
| Round 4: two | Identity as well as key agreement; repaired witness/join checks (`PREDICTIONS.md:995–1016`, `:1097–1137`, `:2131`) |
| Round 5: two | Vocabulary-only witness exception and per-case outcomes (`PREDICTIONS.md:1283–1349`, `:1523–1532`, `:1558–1559`, `:2129–2131`) |
| Round 6: six | Envelope-report link 6b; corrected mixed cases, compromise assignments and repository descents (`PREDICTIONS.md:473–513`, `:1529–1530`, `:1558`, `:2131`) |
| Round 7: two | C-C3’s C-Q9 failure; strict evidence pair and C-C10 isolation (`PREDICTIONS.md:176–199`, `:267–306`, `:1525`, `:1532`) |
| Round 8: two | Mixed C-C5 and retirement of whole-configuration descent (`PREDICTIONS.md:1484–1519`, `:1527`, `:3036`) |

Here `PREDICTIONS.md` denotes `formal/suite/capstone/PREDICTIONS.md`. The three ledger corrections remain honoured: unrestricted exact-byte checking, publication provenance as correspondence, and fresh presentation identity with layer-specific completion. (`formal/suite/capstone/PREDICTIONS.md:115–162`, `:308–323`, `:1237–1256`.)

**This registration is not ready to freeze. The author should see first finding 1, the result-changing C-C15(i) reporting choice; finding 2, the contradicted C-C8 strict manifest-hash prediction; and finding 3, the reversed C-Q8 provenance citations. The existing REFUSAL decision also remains outstanding. The requested C-C6 projection is green on every declared safety query in both strict variants, with live witnesses. No repository file was changed.**

