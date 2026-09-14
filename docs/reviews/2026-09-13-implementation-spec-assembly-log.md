# Implementation specification: 2026-09-13 assembly log

> **STATUS: PROPOSED. Working record only.** This is the clerk's record of the
> 2026-09-13 assembly of `docs/implementation-spec.md`, band-1 docket item 31.
> It registers nothing, adopts nothing, resolves no contradiction and moves no
> tracker row. Nothing in it is an author act; the commit is the author's.

## What this is

`docs/implementation-spec.md` was assembled on 2026-09-13 from six
skeptic-reviewed section drafts held outside the repository as working papers.
This log keeps the working material the specification itself does not carry:
the pipeline that produced it, the counts, the mapping from each draft's local
open-item and contradiction labels to the register IDs the specification now
uses, and the drafters' and skeptics' own end-of-section lists and logs,
verbatim.

## The pipeline as run

| Stage | Agents | Model | Output |
|---|---|---|---|
| Extraction | 6 | Claude Opus 5 | 759 extraction cards with file:line citations, over the pre-registration, Amendments 1 to 6, the two spike decision records, the suite enumeration and routed dispositions, the shared ProVerif library, the five suite families, the TLA+ modules and reading aids, the tracker, the coverage map, the Band 0 exit list, the band-1 docket, and the 2026-07-28 identity-boundary ruling |
| Section drafting | 6 | Claude Opus 5 | `S0`, `S1-S2`, `S3`, `S4-S8`, `S5-S9`, `S6-S7`, `S10`, `S11-S12` |
| Skepticism | 3 | Claude Opus 5 | five logs, one per drafted file that carried requirements; the §1 to §3 pair is one skeptic's (both section heads carry the same Amendment 3 caveat) |
| Integration | 1 | Claude Opus 5 (1M context) | `docs/implementation-spec.md`, this log |

The extraction cards are working papers and are not part of the record.
Section §0's status block names Fable 5.1 as the assembler; that block was
carried verbatim from the drafter, while the integration pass named above ran
on Claude Opus 5 (1M context). The author may want that line corrected.

## Counts

| Measure | Value |
|---|---|
| Lines in the specification | 2765 |
| Requirements (`R-` identifiers, all unique) | 455 |
| Sections carrying requirements | §1 to §9 |
| Distinct file paths cited in provenance tags | 38 |

| Section | Requirements |
|---|---|
| §1 What Tessera attests, and what it does not | 26 |
| §2 Actors, channels, trust configuration, adversary | 49 |
| §3 Objects and formats | 67 |
| §4 Issuance protocol | 106 |
| §5 Verification procedure | 62 |
| §6 Standing assessment | 54 |
| §7 Survivability, custody, tending, agility, renewal | 65 |
| §8 Parameters and constants | 8 |
| §9 Invariants and failure behaviour | 18 |
| **Total** | **455** |

Provenance-kind counts are tag occurrences inside requirement paragraphs, not
requirements: a requirement carrying `[REGISTERED …] [MODELLED …] [OPEN …]`
contributes to three rows.

| Provenance kind | Tag occurrences |
|---|---|
| REGISTERED | 273 |
| RULED | 98 |
| DECIDED | 10 |
| ADOPTED | 2 |
| MODELLED | 66 |
| PROPOSED | 19 |
| DOCKET | 35 |
| DEFERRED | 2 |
| OPEN | 50 |
| CONTRADICTION | 20 |
| SETTLED | 3 |
| SCOPED-OUT (not in §0's declared tag set) | 1 |
| Suite obligation (not in §0's declared tag set) | 1 |
| **Total** | **580** |

Two tag words appear in the drafts that §0's tag table does not declare:
`SCOPED-OUT` (R-4.50) and `Suite obligation` (R-3.63). Both were left as the
drafters wrote them. The §4/§8 skeptic made the same observation about
`[DECIDED …]`, which §0 does declare.

## Local label to register ID mapping

90 local labels appear in the five drafts' end lists. 88 were mapped to a
register entry; 2 were deliberately not mapped, because the §6/§7 skeptic had
already rewritten them as not contradictions. 10 register entries were added
during integration to carry local items that had no entry: nine in §11 (O-69 to
O-77) and one in §12 (C-15).

| Draft | Local | Register | Subject and any per-occurrence split |
|---|---|---|---|
| §1–§2 | O-A1 | O-66 | relying-party story as a Band 0 exit artifact |
| §1–§2 | O-A2 | O-69 (added) | authority-channel count n-ary versus n = 2 |
| §1–§2 | O-A3 | O-44 | ratification of the parameters at Band 0 exit |
| §1–§2 | O-A4 | O-06 | degraded-verdict record format |
| §1–§2 | O-A5 | O-19 | issuer key lifetime and rotation |
| §1–§2 | C-A1 | C-06 | declared-time ordering versus the adjudicator boundary (end list only) |
| §1–§2 | C-A2 | C-07 | `UNVERIFIABLE` for exactly one case (end list only) |
| §1–§2 | C-A3 | C-05 | anchor lateness as a waived observation |
| §1–§2 | C-A4 | S-02 (settled) | Amendment 3 ADOPTED versus DRAFT; the two section-head caveats it carried are replaced by the §0.1 cross-reference |
| §1–§2 | C-A5 | C-08 | what the issuer evaluates at ship |
| §3 | O-B1 | O-01 | exact binary frame layout |
| §3 | O-B2 | O-03 | algorithm-identifier encoding |
| §3 | O-B3 | O-10 | forward-link / successor slot |
| §3 | O-B4 | O-06 | degraded-verdict record format |
| §3 | O-B5 | O-07 | commitment construction; the handoff half of the local statement is O-18 |
| §3 | O-B6 | O-36 | one TLR per key or per identity (end list only) |
| §3 | O-B7 | O-70 (added) | package completeness / self-containment |
| §3 | O-B8 | O-22; O-09 + O-22; O-08 + O-42 | composite: header authentication at R-3.47; SPV segment and pinning at R-3.48; byte budget and custody of referenced bytes at R-3.56 |
| §3 | O-B9 | O-30; O-30 to O-34 | renewal-chain objects: O-30 in the §3.3 table row, the full range at R-3.30 |
| §3 | O-B10 | O-02 | numeric rejection at ingestion |
| §3 | C-B1 | C-15 (added) | four-field frame versus the multi-signer frame's field list |
| §3 | C-B2 | C-03 | where the length is bound |
| §3 | C-B3 | C-04 | keys or references versus self-containment |
| §3 | C-B4 | C-10 | two standing output vocabularies |
| §3 | C-B5 | S-04 (settled) | what §A5.6 leaves undecided about two identities on one key (end list only) |
| §4/§8 | O-C1 | O-18 | refusal-record handoff mechanism |
| §4/§8 | O-C2 | O-48; O-15 + O-48 | retention horizon: O-48 at R-4.70, both at the §8 T row |
| §4/§8 | O-C3 | O-07 | commitment construction |
| §4/§8 | O-C4 | O-18 | refusal reporting surface |
| §4/§8 | O-C5 | O-36 | one TLR per key or per identity |
| §4/§8 | O-C6 | O-01; O-03 | composite: frame layout at R-4.9 and the §8 canonicalization row; identifier encoding at R-4.12 |
| §4/§8 | O-C7 | O-10 | forward-link / successor slot |
| §4/§8 | O-C8 | O-45 | review-staleness threshold |
| §4/§8 | O-C9 | O-47 | tending cadence |
| §4/§8 | O-C10 | O-08 | bundle-size budget |
| §4/§8 | O-C11 | O-02 | numeric-precision rejection at ingestion |
| §4/§8 | O-C12 | O-14 | local-GPG signing path under automation |
| §4/§8 | O-C13 | O-19 | issuer key lifetime and rotation |
| §4/§8 | O-C14 | O-71 (added) | extended atomic-entry refusal invariant, unmodelled (end list only) |
| §4/§8 | C-C1 | C-08 | what the issuer evaluates at ship |
| §4/§8 | C-C2 | C-13 | which k the P5c family checks |
| §4/§8 | C-C3 | S-12 (settled) | `ExpiredCannotShip` versus the latched expiry rule |
| §4/§8 | C-C4 | S-10 (settled) | status of the P5c to P5P6 correspondence |
| §4/§8 | C-C5 | C-10 | standing report output vocabulary |
| §4/§8 | C-C6 | C-04 | manifest key references |
| §5/§9 | O-D1 | O-45 | review-staleness threshold |
| §5/§9 | O-D2 | O-44; O-01 | O-44 at V36 (parameters). At V2 the local tag's subject is the frame layout, that is the local list's O-D7, so V2 was mapped to O-01 |
| §5/§9 | O-D3 | O-06 | degraded-verdict record format |
| §5/§9 | O-D4 | O-22 | header authentication rules |
| §5/§9 | O-D5 | O-03 | algorithm-identifier encoding |
| §5/§9 | O-D6 | O-05 | the §A5.4 framing fork, reading (a) versus (b) |
| §5/§9 | O-D7 | O-01 | exact binary frame layout (end list only) |
| §5/§9 | O-D8 | O-36 | one TLR per key or per identity (end list only) |
| §5/§9 | O-D9 | O-72 (added) | log-versus-verdict boundary has no registered text |
| §5/§9 | O-D10 | O-71 (added) | two registered model obligations unmodelled |
| §5/§9 | O-D11 | O-73 (added) | binding-form required set unmodelled; lifecycle half is O-20 |
| §5/§9 | O-D12 | O-42 | custody of externally-referenced inputs (end list only) |
| §5/§9 | O-D13 | O-70 (added) | package completeness (end list only) |
| §5/§9 | C-D1 | C-05 | anchor lateness as a waived observation |
| §5/§9 | C-D2 | C-07 | `UNVERIFIABLE` for exactly one case |
| §5/§9 | C-D3 | C-10 | two standing output vocabularies |
| §5/§9 | C-D4 | C-02 | revocation after issue |
| §5/§9 | C-D5 | C-03 | where the length is bound |
| §5/§9 | C-D6 | C-04 | keys or references versus P9 self-containment |
| §5/§9 | C-D7 | C-12 | `ot` and `cv` as checks or carried fields |
| §5/§9 | C-D8 | C-06 | downstream ordering versus the adjudicator boundary |
| §5/§9 | C-D9 | S-05 (settled) | what a non-`attemptCore` presentation produces after the pin |
| §5/§9 | C-D10 | S-09 (settled) | COVERAGE-MAP row 1 versus S-P1's record |
| §5/§9 | C-D11 | S-12 (settled) | `ExpiredCannotShip` versus the latched expiry rule |
| §6/§7 | O-E1 | O-36 | one TLR per key or per identity |
| §6/§7 | O-E2 | O-74 (added) | the standing path's `if kT = kX` check |
| §6/§7 | O-E3 | O-75 (added) | two standing reason codes with no registered home |
| §6/§7 | O-E4 | O-76 (added) | lineage arity other than two |
| §6/§7 | O-E5 | O-77 (added) | TLR anchor temporal validity, cross-formalism |
| §6/§7 | O-E6 | O-18 | refusal-record handoff mechanism |
| §6/§7 | O-E7 | O-42 | custody of externally referenced inputs |
| §6/§7 | O-E8 | O-47 | tending cadence |
| §6/§7 | O-E9 | O-37 | tending triggers, clock, monitoring surface, succession |
| §6/§7 | O-E10 | O-03 | algorithm-identifier encoding |
| §6/§7 | O-E11 | O-13 | hybrid classical plus PQ dual signing |
| §6/§7 | O-E12 | O-19 | issuer key lifetime and rotation |
| §6/§7 | O-E13 | O-30 | verdict composition along a renewal chain |
| §6/§7 | O-E14 | O-48 | retention horizon and minimization policy |
| §6/§7 | O-E15 | O-07 | commitment construction |
| §6/§7 | O-E16 | O-18 | refusal reporting surface |
| §6/§7 | C-E1 | C-10 | two standing output vocabularies |
| §6/§7 | C-E2 | C-07 | `UNVERIFIABLE` for exactly one case |
| §6/§7 | C-E3 | none, by design | the skeptic rewrote it as not a contradiction; no §12 entry created, body left as written |
| §6/§7 | C-E4 | none, by design | same |
| §6/§7 | C-E5 | S-13 (settled) | the standing decision's own status |

## Register entries added at integration

Nine §11 entries and one §12 entry were added, each carrying the local list's
own one-line statement and citations. The §11 preamble's area counts were
updated from 66 entries to 75 (Verification 14 to 18, Standing 1 to 5,
Process-exit 17 to 18) and the §12 preamble from twenty-six conflicts to
twenty-seven. No existing entry was edited.

| New ID | Area | Carries |
|---|---|---|
| O-69 | Verification | O-A2: the authority-channel count is n-ary as ruled, every rule in the record is written at n = 2 |
| O-70 | Verification | O-B7 and O-D13: package completeness and self-containment |
| O-71 | Process-exit | O-C14 and O-D10: two registered Band 0 model obligations unmodelled |
| O-72 | Verification | O-D9: the log-versus-verdict boundary has no registered text |
| O-73 | Verification | O-D11: the binding-form required set is unmodelled by any suite family |
| O-74 | Standing | O-E2: whether the standing path's `if kT = kX` check is a conformance requirement |
| O-75 | Standing | O-E3: two standing reason codes with no registered home |
| O-76 | Standing | O-E4: standing behaviour for lineages of other than two attempts |
| O-77 | Standing | O-E5: the TLR anchor's temporal validity, owed cross-formalism to the bridge |
| C-15 | §12 open | C-B1: four fields in the P8 frame versus the multi-signer frame's field list. Cross-referenced to O-05, which asks a different question of the same passage |

## Judgement calls the author may want to overturn

1. **C-B1 became a new §12 entry rather than a pointer to O-05.** The register
   already carries the (a)/(b) multi-signer framing fork as an open decision,
   O-05. The §3 skeptic raised a narrower and different point: P8 registers four
   frame fields and A5 §A5.4 describes seven while saying P8's frame is
   unchanged. It was entered as C-15 with a cross-reference rather than folded
   into O-05, so the skeptic's finding is not lost. If the author reads the two
   as one question, C-15 is withdrawn and R-3.12's tag becomes `[OPEN — §11 O-05]`.
2. **O-A1 was mapped to O-66.** O-66 is the reading-to-veto on whether the
   relying-party story must be published stand-alone as well as written into the
   specification. O-A1 says the artifact does not exist at all. They are the same
   artifact and the same Band 0 exit obligation (E12), so no entry was added.
3. **V2's tag was mapped by subject, not by label.** The §5 draft tagged V2
   (frame reconstruction, exact binary layout unfixed) `[OPEN — see §11 O-D2]`,
   the parameters item; its subject is the local list's O-D7. It was mapped to
   O-01, the frame layout.
4. **Composite local labels were split per occurrence.** O-B8, O-B9, O-C2, O-C6
   and O-D2 each covered more than one register entry; the mapping table above
   records which entry each occurrence took.
5. **Appendix A and Appendix B titles** carry the em dash the assembly brief
   specified for them, unlike the numbered section heads.

## Skeptic logs, verbatim

Five logs from three skeptics, copied without change under the sections they
cover.

### Skeptic log, §1 and §2 (`S1-S2.md`)

- **§1 head** — added a provenance caveat that every `[REGISTERED A3 …]` tag in this section rests on C-A4. Checked amendment-3.md:1 ("Amendment 3 — ADOPTED (2026-08-08)") against :3 ("**Status: DRAFT — not signed, not in force.**"); §1's whole identity boundary is A3 text, so tagging it REGISTERED silently picks one side of C-A4.
- **R-1.6** — citation `sp1_q2_degraded_compromised.pv:166-180` → `:163-164` (the correspondence query) plus `:168-181` (the verifier). Checked :166-180: it is the `VerifierS` process; the non-injective correspondence `event(AcceptS(...)) ==> event(IssuerSigned(...))` is at :164.
- **R-1.13** — downgraded "No API or UI may relay envelope validity as content validity" to the source's own wording. Checked amendment-3.md:679-684: the source says "nothing previously registered prevented a future API or UI from relaying…" (a description of a gap); only "Nor may the system collapse…" is normative. Citation narrowed :677-684 → :679-684.
- **R-1.15** — `[RULED A3 §A3.8]` → `[REGISTERED …]` with a pointer to the `[AUTHOR DECISION — ratified -- 2026-08-08]` block. Checked amendment-3.md:686-689: plain amendment text, no ruling marker; the marker is at :722.
- **R-1.16** — citation `:546-549` → `:542-548`. Checked: :549 is blank and :546 starts mid-sentence; the "reported separately, never collapsed" material is :542-548.
- **R-1.17** — `[RULED (panel-driven clarification) …]` → `[REGISTERED … [PANEL-DRIVEN CLARIFICATION — 2026-08-08]]`. Checked amendment-3.md:550: the marker is a panel clarification inside an amendment, not an `[AUTHOR DECISION]` / "ADOPTED (author)" label.
- **R-1.21** — citation `docs/band-1-docket.md:517-527` → `:517-521`; the file ends at line 526. Quote corrected to the source's lowercase "if the verifier requires anything…" (docket:519-520).
- **R-1.22** — citation `:517-527` → `:521-525`. Checked: the adjudicator sentence and its quote are at :521-525.
- **R-1.23** — citation `:526-527` → `:525`; :526 is blank, :527 does not exist. Noted the docket says "an enumeration API" where A4 §A4.6 says "An enumeration or observability API".
- **R-1.24** — citation `:524-526` → `:524`. Checked: "The relying-party story defines both terms" is on :524.
- **R-1.26** — citation `:738-739` → `:736-737`. Checked: the human-facing-twin sentence is at :736-737; :738-739 are blank and a rule.
- **§1.5 "What a bundle presented alone gives you"** — the three-part `VALID_STRICT` gloss was cited to amendment-3.md:677-684, which does not contain it. Checked :677-684 (envelope soundness only); re-cited to A1 P1 :116-119, A1 §A1.5 :444-448, and P5 with A2 §A2.2 :220-224, and flagged in-line that the gloss goes beyond the can/does-not-establish list, which says only "This valid package reconstructs the same framed bytes recorded at issuance."
- **§1.5 "What `UNVERIFIABLE` means"** — "standing evidence whose own anchor does not check out" had no supporting citation among the four given (checked all four); added `STANDING_EVIDENCE_TEMPORAL_MISMATCH`, first-link/DECISION.md:844-847.
- **R-2.2** — section label `A2 §A2.2` → `A2 §A2.1 "The rule"` for `:87-89`. Checked amendment-2.md:78-89: those lines are §A2.1, not §A2.2.
- **R-2.3** — `RULED (panel repair)` → `REGISTERED … [PANEL-DRIVEN REPAIR — 2026-08-08]`. Checked amendment-3.md:665: the marker is a panel repair inside the amendment, not an author ruling.
- **R-2.7** — `RULED A3 §A3.5` → `REGISTERED A3 §A3.5`. Checked amendment-3.md:384-394: plain amendment text; the nearest `[AUTHOR DECISION]` is at :424 and covers a different question.
- **R-2.12** — citation `A1 P10 :292-297` → `:290-291`. Checked: :292-294 is the proper-subset property; the sentence "`VALID_STRICT` requires **all** external authority evidences to validate, plus proof-of-possession" is at :290-291.
- **R-2.13, R-2.14** — provenance qualified: both sit inside band-1 docket item 26, whose own heading reads "candidate; not registered anywhere in the record" (docket:385-386), and neither passage carries a RULED/ADOPTED label (contrast item 27's explicit "*Vocabulary, RULED (author)*" at :517).
- **R-2.17** — citation `standing-probe/DECISION.md:72-74` → `:71-72`. Checked: :71-72 is G2 ("Zero inputs beyond the bundle and the trust configuration"); :73-74 is G3, a different criterion.
- **R-2.25** — split the prereg label: `:327-337` is §3.1's verifier-state list (it cross-references §4.6), `:555-562` is §4.6 itself.
- **R-2.31** — cross-reference `[CONTRADICTION — C-A2]` → `C-A3`. Checked C-A2 (the count of `UNVERIFIABLE` cases) has no bearing on waived-but-failing evidence; C-A3 (anchor-late as a waived observation vs non-waivable temporal consistency) is the contradiction this requirement sits inside.
- **R-2.32** — quotation corrected. Checked amendment-4.md:100-103: A4 quotes P4's *old* sentence in full and writes the replacement only as an ellipsis, "A **required** check that cannot be performed…". The draft's full quoted replacement sentence does not appear in the record.
- **R-2.34** — added the line number for `NoSilentPromotion` (P4_VerifierStates.tla:124).
- **R-2.41** — "Item 6's 'never all'" replaced with item 6's actual words, "Control any proper subset of the external manifest-authority channels", noting "never all" is the record's shorthand. Checked amendment-1.md:345-346: the phrase "never all" is not in A1.3.
- **R-2.49** — tightened to the source's falsification condition. Checked amendment-1.md:79-90: H0 is falsified if a property "cannot be discharged without" excluding a capability; excluding a capability is not by itself the falsifier, and the draft's wording would be wrong under that reading.
- **O-A5** — citation `docs/band-1-docket.md:432-435` → `:429-433`. Checked: the rotation-moment threat sentence runs :429-433; :434-435 begins the author's separate reason.

### Skeptic log, §3 (`S3.md`)

- **§3 head** — added a provenance caveat that every `[REGISTERED A3 …]` tag in this section rests on C-A4. Checked amendment-3.md:1 ("ADOPTED (2026-08-08)") against :3 ("**Status: DRAFT — not signed, not in force.**").
- **R-3.12** — citation `A5 §A5.4 :178-190` → `:165-190`, with the (a)/(b) fork located at :165-179 and the six-field sentence at :179-183; the cited range did not contain the definition of reading (b) the requirement relies on. Label made explicit: A5 §A5.4's heading is "ADOPTED (author)".
- **R-3.24** — `[RULED (author) 2026-09-04]` → `[MODELLED standing-probe G0]`. Checked standing-probe/DECISION.md:61-66: the passage is a scoring entry, "G0 — pass (evidential)", and closes "the probe is a stub fixture; this is design evidence, not conformance." The author's act at :378-384 selects the mechanism, not this behaviour; the requirement now says "As probed".
- **R-3.26** — `[RULED (author) A3 §A3.5]` → `[REGISTERED A3 §A3.5]`. Checked amendment-3.md:384-402: plain amendment text with no `[AUTHOR DECISION]` marker.
- **R-3.27** — `[RULED (author) A3 §A3.8]` → `[REGISTERED …]` plus a pointer to the `[AUTHOR DECISION — ratified -- 2026-08-08]` at :722-734, which is what actually rules the "unsigned" choice. Checked amendment-3.md:686-704.
- **R-3.34** — `[RULED (author) 2026-08-12/13]` → `[DECIDED …]`. Checked first-link/DECISION.md:145: the transcription-binding text sits under the heading "Proposed decision" and carries none of the document's own per-statement labels, whose discipline at :140 reads "Absence of a label means unlabelled draft prose, not implicit adoption." The document status DECIDED at :1-9 is what carries the selection.
- **R-3.35** — same correction. Checked first-link/DECISION.md:353-362: "Selected: authenticated, domain-separated forms" and "Map v1 ruling" are unlabelled; only the enabling observation at :338-344 is attributed to the author. Citation narrowed `:344-363` → `:353-362`.
- **R-3.37** — kept RULED but recorded the source's own label. Checked first-link/DECISION.md:366-372: "ADOPTED 2026-08-13 (author) … Labelled ADOPTED rather than RULED because the reasoning originated in the cross-review."
- **R-3.44** — section label corrected: `A1 §A1.6 :111-114` is in fact §A1.2's temporal-vocabulary paragraph; A1.6's own vocabulary is :482-491. Both now cited.
- **R-3.47** — split the A2 labels: `:236-244` is §A2.2's evidence obligation; `:197-206` (candidate chain segment, header provenance) is §A2.1's header-provenance residual, not §A2.2.
- **R-3.49** — reworded to the source and re-cited `:56-81` → `:56-58, 65-69`. Checked AMENDMENTS-2026-08-31.md:65-68: cost (ii) says "Where the bundle ships before chain confirmation"; the draft's "before its TLR's anchor confirms" narrows a condition the record leaves general.
- **R-3.56** — `[RULED consequence]` → the source's own characterisation. Checked first-link/DECISION.md:261-266: criterion 4 is "PASS, WEAKLY (not query-discharged) … Recorded honestly as a construction-level judgment", not a ruling.
- **R-3.57** — citation `docs/band-1-docket.md:483-526` → `:483-516`; the file ends at 526 and :517-525 is the separate vocabulary ruling belonging to R-1.21–R-1.24.
- **R-3.61** — added the registered source for the standing triple: A3 §A3.7.1, amendment-3.md:542-546 ("The base result reports at least `ESTABLISHED`, `ABSENT`, or `UNVERIFIABLE`"). The draft attributed the triple only to the spike texts; it is registered amendment text.
- **R-3.63** — `[RULED suite obligation]` → suite obligation, not an author ruling. Checked ENUMERATION.md:502-509: it is a note "carried from the blind re-scoring", with no ruling label.
- **C-B4** — sharpened with the same A3 §A3.7.1 citation: the conflict is registered-against-registered, not spike-against-amendment. No side chosen.

### Skeptic log, §4 and §8 (`S4-S8.md`)

- **R-4.36** — provenance kind changed `RULED` → `REGISTERED`; the source marker is `[PANEL-DRIVEN REPAIR — 2026-08-08, from the Kimi addendum, clerk-verified against the model]`, which is not an author-decision marker (the draft already tagged the same repair REGISTERED at R-4.40). Range tightened 665-675 → 665-673 (674 blank, 675 is `---`). The competing §A3.9 line is now stated inline rather than only cross-referenced, so the requirement does not read as a resolution. Checked docs/phase-0-prereg-amendment-3.md:654-675, :832.
- **C-C1** — citation `:833` → `:832`; the sentence "A2.1 prose repair (issuer ships on full `VALID_STRICT`)." is at 832; 833 is blank. Also 665-675 → 665-673. Checked docs/phase-0-prereg-amendment-3.md:825-834.
- **R-4.30** — citation `153-159` (the direct-form sentence begins at 153, not 154) and `353-357` (the `STMT_DIRECT`/`STMT_DIGEST` construction is at 353-354; 344-352 is the D1 sub-ruling, unrelated). Checked formal/spike/first-link/DECISION.md:150-160, :344-363.
- **R-4.83, R-4.84, R-4.92** — provenance kind changed `DECIDED` → `PROPOSED (probe scoring draft)`; the cited gate lines sit under `DECISION.md`'s deliberately retained header "Status: PROPOSED — scoring draft, nothing decided." What the author adopted is sub-ruling 5, not the gate scoring. Checked formal/spike/standing-probe/DECISION.md:28-41, :61-82.
- **R-4.83** — added the source's own boundary ("the probe is a stub fixture; this is design evidence, not conformance") and scoped the subject to the probe's TLR; the draft generalized a fixture observation into a property of the TLR. Checked formal/spike/standing-probe/DECISION.md:61-66.
- **R-4.91** — attribution corrected: the quoted "carried, not maintained; the service's duty is punctual, not custodial" is the collaborator's record of an in-session resolution inside a `[2026-08-31 Collaborator note …]` bracket; the author's own quoted words there are "Item 5 adopted." Checked formal/spike/standing-probe/DECISION.md:378-398.
- **R-4.96** — citation corrected: `:185-195` is the scorer's composition observation, labelled "an input to the rule-3 fork, not a selection", and the fuller phrasing at `:313-321` sits under "RECOMMENDED (not adopted, and carrying the scorer's non-blindness)"; the adopted wording is sub-ruling 5's at `:378-384`. Checked formal/spike/standing-probe/DECISION.md:185-195, :313-321, :378-398.
- **§4.10 table row 2** — citation `166-168` → `34-45`; 166-168 is the `VARIABLES` block, while the clock-roles sentence ("this module's single clock READS AS THE WALL CLOCK … the S = 0 instance") is at 34-45. Checked formal/tla/P5c_IssuanceProtocol.tla:34-45, :160-180.

**Checked and left unchanged (traps).** (a) §4's ship guard quotes A3 §A3.7.3's panel repair byte-exactly and does not say the issuer re-runs full `VALID_STRICT` at ship — verified against docs/phase-0-prereg-amendment-3.md:665-673. (b) R-4.38/R-4.39/R-4.42 carry the A2 §A2.1 chain-time form with `confirmed_at := timestamp(block at height h + k − 1)` and the pin `DepthK = k − 1` — verified against docs/phase-0-prereg-amendment-2.md:80-89, :208-214. (c) The k contradiction is stated at C-C2 and in the §8 k row, not resolved — verified against formal/tla/P5c_IssuanceProtocol.tla:26-29, formal/tla/P5c_IssuanceProtocol.cfg:15-19, formal/tla/P5cP5P6_Bridge.cfg:1-14, formal/PROPERTIES.md:167-168. (d) The standing-vocabulary contradiction is stated at C-C5 and flagged on R-4.90, not resolved. (e) SC-1/SC-2/SC-3/D1 (R-4.85–R-4.89, R-4.94) match the adopted wording in formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:22-81, :96-116, :159-206 and formal/spike/first-link/DECISION.md:834-847; no commit is named in these requirements, so none was inserted (the author's adopting commit is `fbf6387`, 2026-09-04). All TLA+ line citations (R-4.43, R-4.44, R-4.50, R-4.56–R-4.58, R-4.79, R-4.80, and §4.10 rows 3-14) were opened and support their statements.

**Observation, not edited.** The tag `[DECIDED …]` is not in the tag set the document declares. It is used consistently for author-entered spike decision records (first-link `DECISION.md`, entered by the author at `459aff0`), so it was left alone rather than mass-rewritten; only the uses that pointed at *scoring-draft* text were retagged.

### Skeptic log, §5 and §9 (`S5-S9.md`)

- R-5.8 — split the citation and named what a1:459-469 does not carry (authority-channel public keys, `k`); added a1:173-184 for δ/ε. Those lines register only the archived historical trust-anchor store. Checked docs/phase-0-prereg-amendment-1.md:459-469, :173-184.
- R-5.10 — added the two missing citations (a1:173-177 for receipt tolerance; a4:181-182 for the log) and marked "verifier-local history of prior evaluations" as having no registered prohibition sentence; A5 §A5.1's lines describe probe verifiers, they do not prohibit. The MUST NOT is left standing only over the items with normative source wording. Checked docs/phase-0-prereg-amendment-5.md:65-91, docs/phase-0-prereg-amendment-4.md:176-182.
- R-5.12 — dropped "refusal-reporting state": neither a3:418-419 nor a3:700-702 mentions it. Checked docs/phase-0-prereg-amendment-3.md:415-419, :700-704.
- Bundle table, attempt-core row — a3:531-535 registers only "issuance identity, attempt lineage, and terminal disposition"; the `attemptCore` composition and `aid = h(core)` are model constructs, retagged MODELLED. Checked docs/phase-0-prereg-amendment-3.md:529-535, ss_q1d:328-329, :352.
- Stage table (b) — "Yes" (registered order) replaced: A5 §A5.5 registers the check and the rejection, not its position; the before-`InnerCheck` placement is modelled only. Checked docs/phase-0-prereg-amendment-5.md:192-200, sp7_q2:326-334.
- Stage table (e), (f) — prefixed "Not registered … Modelled:"; both rows stated model behaviour inside a column asking whether the order is registered. Checked sp2_q2:195-196, 213-214.
- Stage table (g) — corrected: the attestation-signature check is the last `checksign`, not stage (d)'s last step; the frame destructure and manifest-hash equality follow it, as row (d) itself lists. Checked sp3_q2:106-109.
- Stage table (i) — "so it follows (h)" marked an unregistered inference of this document. Checked docs/phase-0-prereg-amendment-1.md:199-233.
- V20 — predicate corrected to the model's own spelling `checksign(ev, pkS)`; `pkCh` appears in no model. Checked sp3_q2:101, sp1_q2:171, ss_q1_strict_dns_compromised.pv:355-356.
- V21, R-5.18, R-5.27, and the two binding-form fail-closed rows — provenance downgraded from RULED (author) to ADOPTED (author): the source expressly declines the RULED label. Checked formal/spike/first-link/DECISION.md:366-372.
- V23 — disambiguated the strict-model citation to ss_q1_strict_dns_compromised.pv:355-356; two strict files exist with different line numbers. Checked both files.
- V25 — [RULED C7] retagged PROPOSED: ROUTED records C6/C7 as "settled by the collaborator, listed for veto". Checked formal/suite/ROUTED-2026-09-06.md:313-322.
- V32 and the §9.3 P1-headline row — citation corrected from sp1_q2:198-202 (the JudgeH process) to :141-145 (the query that states the correspondence). Checked formal/suite/s-p1/proverif/sp1_q2_degraded_compromised.pv:141-145, 198-202.
- V40 — added the citation that actually forbids the bare "within δ" phrase. Checked standing-probe/AMENDMENTS-2026-08-31.md:228-234.
- R-5.21 — added the C-D4 pointer; the row stated P6's outcome with no marker while prereg §4.4 states the opposite for the same input. Checked docs/phase-0-prereg.md:537-546.
- R-5.44 — citation corrected to a3:689-700; the Representation-Information bullet is at :700, outside the cited range. Checked docs/phase-0-prereg-amendment-3.md:686-704.
- R-5.46 — the modelled event quote was a gloss, not the declaration; replaced with the byte-exact declaration plus its comment. Checked ss_q1d:175-176.
- R-5.60 — citation corrected from a3:738-739 (blank line and a heading) to :736-737. Checked docs/phase-0-prereg-amendment-3.md:736-739.
- R-5.32, R-5.54 — A4 §A4.6 ranges corrected to start at :156; :153-155 is A4.5's tail. Checked docs/phase-0-prereg-amendment-4.md:144-182.
- Output table — section label corrected: the four-state list is prereg §3.1 at p0:327-337, not §4.6 (which is at p0:555-562). The `VALID_STRICT` row's "every check passed, not only the required ones" split out as modelled-only, per the falsification finding that no registered sentence defines strict that way. Checked docs/phase-0-prereg.md:327-337, :555-562; P4_VerifierStates.tla:135-138, :170-172.
- Per-layer result table, `protocol_standing` — added the C-D3 marker; the row named one of the two unreconciled vocabularies as if it were the only one. Checked docs/phase-0-prereg-amendment-3.md:541-557 against first-link/DECISION.md:790-847.
- §5.5 coverage, "P3 fields carried but unexercised" — corrected to F7's own five fields and F7's own onward assignment (identity → F8, not P7/P8/A3.6.1). Checked formal/suite/s-p3/RESULTS.md:149-158.
- §5.5 coverage, P9 row — stray "`;`" in the modelled-in cell replaced with "none". Checked formal/COVERAGE-MAP.md:32.
- R-9.14 — added the missing provenance tag and excluded DOCKET rows from "required behaviour"; the fail-closed table contains a DOCKET 17 candidate row. Checked docs/phase-0-prereg-amendment-3.md:161-164, :703-704; docs/band-1-docket.md:133-140.
- §9.2, splicing row — "(six non-fingerprint fields unequal)" would acquit a bundle in which exactly one field differs, which is the case A5 §A5.4 registers as failing; reworded to "any one of the six", fields enumerated, and the (a)/(b) fork pointer added. Checked docs/phase-0-prereg-amendment-5.md:173-190; sp2_q2:225-230, :275-284.
- §9.2, waived-evidence row — added the C-D1 marker; the row recorded `anchor-late` as an observation without noting the conflict with A2 §A2.2's non-waivability. Checked docs/phase-0-prereg-amendment-5.md:145-154; docs/phase-0-prereg-amendment-2.md:245-248.
- R-9.15 — [RULED C6] retagged PROPOSED, same reason as C7. Checked formal/suite/ROUTED-2026-09-06.md:313-318.
- C-D2 — the enumeration was incomplete; added the three further registered `UNVERIFIABLE` assignments (headers unavailable, the binding-form cases, `STANDING_EVIDENCE_TEMPORAL_MISMATCH`). Checked docs/phase-0-prereg-amendment-2.md:245-248; first-link/DECISION.md:376-378; standing-probe/AMENDMENTS-2026-08-31.md:44-47.
- O-D3 — a5:153-155 corrected to :152-153 (the H1a-obligation sentence); docket range corrected to :62-66. Checked docs/phase-0-prereg-amendment-5.md:150-155; docs/band-1-docket.md:62-66.
- O-D4, R-5.41 — docket ranges corrected (item 7 is at :44-49; item 28 at :62-66). Checked docs/band-1-docket.md:44-49, :62-66.

Verified and left unchanged (sampled, byte-exact against source): R-5.1–R-5.7, R-5.9, R-5.11, R-5.13–R-5.20, R-5.22–R-5.31, R-5.33–R-5.39, R-5.42–R-5.43, R-5.45, R-5.47–R-5.59, R-5.61–R-5.62; R-9.1–R-9.13, R-9.16–R-9.18; V1–V19, V22, V24, V26–V39; every §9.3 invariant line range; the reason-code table; the boundary table; O-D1, O-D2, O-D5–O-D13; C-D1, C-D3–C-D11.

### Skeptic log, §6 and §7 (`S6-S7.md`)

**Contradictions that were not contradictions.**

- **C-E3** — rewritten. The draft presented the frozen-plan sentence versus §A5.6 as unreconciled. The record reconciles it explicitly: "the frozen plan and the signed amendment diverge there and the amendment governs", and RESULTS.md repeats it at :1318-1333 ("its registered sentence stands on the record as written and is wrong"). Entry now records the divergence *and* the governing text. Consequential: leaving it as an open contradiction would have made an implementer treat a superseded sentence as live. Checked formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:74-80; formal/suite/s-standing/RESULTS.md:1185-1199, :1318-1333.
- **C-E4** — rewritten for the same reason. RESULTS.md corrects its own :1203-1207 at :1335-1348 ("**5 — "produces no report at all" is overbroad**"), with the verifying output cited. Checked formal/suite/s-standing/RESULTS.md:1203-1207, :1335-1348.
- **C-E5** — rewritten. `DECISION.md` states why both labels stand ("The registered PROPOSED header is retained below, per amend-don't-rewrite"), so they are not mutually exclusive. The genuinely stale item is "author commit pending": `git show fbf6387` (2026-09-04) contains `formal/spike/standing-probe/DECISION.md` and `AMENDMENTS-2026-08-31.md`. Checked formal/spike/standing-probe/DECISION.md:3-26, :28-41; commit `fbf6387`.
- **R-6.42, R-6.26** — the `[CONTRADICTION]` markers pointing at C-E3 and C-E4 were removed accordingly (the C-E4 marker was replaced by the corrected statement inside R-6.26).

**Provenance kinds.**

- **R-6.4** — `RULED (panel-driven clarification)` → `REGISTERED`; the source marker is `[PANEL-DRIVEN CLARIFICATION — 2026-08-08, from the Kimi cold read]`, which is not an author-decision marker. Checked docs/phase-0-prereg-amendment-3.md:550-557.
- **R-6.9, R-6.10, R-6.11, R-6.22a, R-6.36, R-6.38, R-6.39** — `DECIDED`/`REJECTED` → `PROPOSED (probe scoring draft)`; all cite gate/criteria lines under `DECISION.md`'s retained "Status: PROPOSED — scoring draft, nothing decided." header. Checked formal/spike/standing-probe/DECISION.md:28-41.
- **R-6.25** — `RULED (carry note …)` → `PROPOSED`; the source is headed "Carry note (drafter, not an amendment)" and the `ENUMERATION.md` note carrying it is headed "Amendment note 4 — 2026-09-04 (clerk; PROPOSED; …)". The MUST wording is quoted as the drafter's, not upgraded to an author obligation. Consequential: this is the entitled-key-inside-the-standing-path obligation the S-STANDING model was built to satisfy. Checked formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:210-219; formal/suite/ENUMERATION.md:486, :502-509.
- **R-6.36b** — `RULED (clerk disposition, no veto stated)` → `PROPOSED (clerk disposition B9)`; a clerk disposition is not an author ruling. Checked formal/suite/ROUTED-2026-09-06.md:158-161.
- **R-6.42, R-6.43** — `REGISTERED` → `RULED`; §A5.6 is headed "ADOPTED (author)" and §A4.6 "RULED (author)". R-6.43's range narrowed 152-167 → 156-167 (152-154 is §A4.5's tail). Checked docs/phase-0-prereg-amendment-5.md:202-219; docs/phase-0-prereg-amendment-4.md:152-167.
- **R-7.26** — `RULED (author) 2026-08-08` → `REGISTERED`; there is no author-decision marker on the four-outcome passage, and the nearest `[AUTHOR DECISION — ratified -- 2026-08-08]` block begins at :424 and governs R-7.31/R-7.32, not this. Checked docs/phase-0-prereg-amendment-3.md:380-397, :424-452.
- **R-7.41** — the invented tag `PROVISIONAL` replaced with `REGISTERED prereg §4`, matching R-7.46's tag for the same passage. Checked docs/phase-0-prereg.md:339-345.
- **R-6.8** — the author's adopting commit `fbf6387` added, since the cited lines read "author commit pending". Checked formal/spike/standing-probe/DECISION.md:3-26.

**Quotations.**

- **R-6.20** — the quoted sentence was stitched from two sources and matched neither byte-for-byte. Replaced with the band-1 docket's exact ruling wording plus, separately attributed, the `DECISION.md` wording. Checked docs/band-1-docket.md:355-383; formal/spike/standing-probe/DECISION.md:368-377.
- **R-6.22** — the quoted phrase is verbatim but sits under "**RECOMMENDED (not adopted, and carrying the scorer's non-blindness)**", and the composition sentence under "an input to the rule-3 fork, not a selection". Both now attributed as the scorer's; the adopted wording (sub-ruling 5) is given first. Checked formal/spike/standing-probe/DECISION.md:185-195, :313-321, :378-384.
- **R-6.30** — S3 row: comma → em dash, as the registered table has it. Checked formal/spike/first-link/DECISION.md:801.
- **R-6.31** — truncated quote completed ("… in exactly the way the panel criterion warned about."). Checked formal/spike/first-link/DECISION.md:804-806.
- **R-6.9** — subject scoped to "the probe's TLR" and the source's own boundary added ("the probe is a stub fixture; this is design evidence, not conformance"). Checked formal/spike/standing-probe/DECISION.md:61-66.
- **R-6.12** — attribution corrected: the quoted custody sentence is the collaborator's record of an in-session resolution; the author's own quoted words there are "Item 5 adopted." Checked formal/spike/standing-probe/DECISION.md:378-398.
- **R-6.37** — the quoted "evidence about the model's constants … and about nothing else" is in RESULTS.md:274-280, not in the cited `.pv` lines; the citation now names it. Checked formal/suite/s-standing/RESULTS.md:268-280.

**Statements corrected against the source.**

- **R-6.26** — the "consequence recorded at registration" as the draft stated it is the pre-correction wording, falsified on 2026-09-12. Replaced with the corrected form: aggregate witnesses S1-S4 and `STANDING_EVIDENCE_MISMATCH` stay reachable; only the lineage-derived reports acquire the pin as a precondition, and only for alias presentations; a non-`attemptCore` core yields no lineage-derived report while the no-TLR report is unaffected. Checked formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:343-352; formal/suite/s-standing/RESULTS.md:1335-1370.
- **R-6.24** — the "steps, in order" table skipped the `let withTLR(kT, tlrSig, ap) = se` destructuring, which has no else branch; off the happy path, standing evidence that is neither `noTLR` nor a `withTLR` term produces no report at all rather than any of the tabled reason codes. Added as a sentence; citation range extended `:322-357` → `:322-363` so the `SIGNATURE_INVALID` and `TEMPORAL_MISMATCH` else-branches at :358-363 fall inside it. Checked formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:322-363.

**Citations repaired (lines did not support the statement; correct lines were nearby).**

- **R-7.10** 48-51 → 54-56 (docket item 9); **R-7.11** 52-60 → 57-61 (item 10); **R-7.12** 46-51 → 50-53 (item 8); **R-7.20** 170-186 → 163-173 (the constraint sentences begin at 163); **R-7.23** 341-355 → 336-347 (24(b) begins at 336; 348-353 is 24(c)); **R-7.25** 518-526 → 517-526 (the "RULED (author)" marker is at 517); **R-7.34** 117-138 → 117-132 (133+ is item 17); **R-7.48** 243-258 → 269-282 (item 20); **R-7.49** and **O-E13** 216-242 → 245-267 (item 19); **R-7.50** 259-269 → 284-292 (item 21); **R-7.51** 270-302 → 294-302 (item 22). The docket citations for items 19-22 were displaced by ~25 lines throughout. Checked docs/band-1-docket.md:46-61, :117-208, :245-302, :326-355, :429-526.
- **R-6.3** 546-549 → 545-548; **R-7.30** :700-702 → :702-704; **R-6.20** docket 356-385 → 355-383. Checked docs/phase-0-prereg-amendment-3.md:545-548, :699-711.

**Checked and left unchanged (traps).** (b) R-6.14 carries SC-1's A2.1 chain-time form byte-exactly, including `confirmed_at := timestamp(block at height h + k − 1)`, `confirmed_at ≤ declared_terminal_time + δ` and the ε lower-bound conjunct — verified against formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:30-54. (d) The two-vocabulary contradiction is stated at R-6.35 and C-E1 and left unresolved. (e) SC-1/SC-2/SC-3/D1 (R-6.13–R-6.18, R-6.20) match the adopted wording. (f) Docket 26: both author quotes (R-7.43's "key lifetime becomes a safeguard…" and R-7.44's "By staggering rotation periods…") are byte-exact against docs/band-1-docket.md:389-391 and :436-438, the two candidate rules are marked "neither agreed", and the collaborator's objections appear only as recorded objections in R-7.44a/R-7.44b, never as rules.

## Per-section open-item and contradiction lists, verbatim

These are the drafts' own end-of-section lists, using the local labels.
The specification drops them; the mapping table above is the bridge.

### End lists, §1 and §2 (`S1-S2.md`)

### Open items raised in §1–§2

**O-A1** — The relying-party story is a required Band 0 exit artifact and does not exist in the repository; §1.5 above is draft text, and its anchor-robustness paragraph rests on record text marked candidate. [REGISTERED A3 §A3.1 item 4, docs/phase-0-prereg-amendment-3.md:89-96; docket item 24(c) candidate, docs/band-1-docket.md:348-353]

**O-A2** — The authority-channel count is n-ary as ruled, but every model, ledger entry and evidence-set rule in the record is written at n = 2; no rule states how the strict "all external evidences" requirement, the waiver lattice, or the "never all" enumeration behave for n > 2. [RULED (author) 2026-09-06, docs/band-1-docket.md:465-468; docs/phase-0-prereg-amendment-1.md:283-297, 344-346]

**O-A3** — δ, ε, k, N and S remain to be ratified or revised on the record at Band 0 exit; the values 72 h, 24 h, 6, 3 and 24 h are working strict defaults. [PROVISIONAL, docs/phase-0-prereg-amendment-1.md:180-190; docs/phase-0-prereg-amendment-2.md:270-274, 372-375]

**O-A4** — The degraded-verdict record format is an H1a obligation entered on the band-1 docket; only the required content is registered, not the format. [REGISTERED deferral A5 §A5.3, docs/phase-0-prereg-amendment-5.md:153-155; docs/band-1-docket.md:62]

**O-A5** — Issuer signing-key lifetime, rotation cadence, verifier behaviour at the window boundary, and the rotation-moment threat are candidates on the band-1 docket, not registered anywhere in the record; the author deferred key-rotation policy from the 2026-09-06 round. [PROPOSED — docket item 26, docs/band-1-docket.md:385-400, 429-433; deferral noted at docs/band-1-docket.md:505-507]

### Contradictions raised in §1–§2

**C-A1** — A2 §A2.4 registers that no verifier policy and no downstream marketplace rule may order competing receipts by declared time; A4 §A4.6 registers that the adjudicator decides trust using the verdict and anything else available and that Tessera must not decide for it. Neither cites the other; whether an implementation must refuse to serve declared-time ordering or merely not perform it is unstated. [docs/phase-0-prereg-amendment-2.md:327-333; docs/phase-0-prereg-amendment-4.md:159-182]

**C-A2** — A3 §A3.6.2 registers "`UNVERIFIABLE` for exactly one case — a well-formed, correctly bound, but unsupported algorithm identifier", while the same amendment and A2 assign `UNVERIFIABLE` to at least three further cases (all authority evidence for a layer unavailable; unavailable issuance-profile dependency interpretation; missing block headers), and protocol standing reports `UNVERIFIABLE` as a dimension value. [docs/phase-0-prereg-amendment-3.md:503-505 vs :146-149, :353-356, :541-546; docs/phase-0-prereg-amendment-2.md:245-248]

**C-A3** — A2 §A2.2 registers temporal-anchor consistency as non-waivable with the new conjunct part of it (performed-and-failed → `INVALID`); A5 §A5.3 registers `anchor-late` as one of six observation values recorded for a *waived* check whose condition never determines the verdict, and A5 §A5.2 lists a late anchor among failures a waived channel evidence may exhibit while `VALID_DEGRADED` stands. The two may be scoped to different anchors; the registered text does not say so. [docs/phase-0-prereg-amendment-2.md:245-248; docs/phase-0-prereg-amendment-5.md:96-100, 145-150]

**C-A4** — Amendment 3's title line declares "Amendment 3 — ADOPTED (2026-08-08)"; the immediately following status block declares "**Status: DRAFT — not signed, not in force.**" and conditions force on cold read, non-author panel review, signature, commit and OTS stamp. Both stand unamended, and A3 §A3.1 is the source of §1's identity boundary. [docs/phase-0-prereg-amendment-3.md:1 vs :3-20]

**C-A5** — A3 §A3.7.3's panel repair states the issuer's ship guard is the three-conjunct temporal predicate plus burial depth and that the issuer "does not re-run envelope verification (P1–P3) at ship", explicitly rejecting the phrase "the full `VALID_STRICT` predicate"; the §A3.9 obligations summary in the same document lists "A2.1 prose repair (issuer ships on full `VALID_STRICT`)." [docs/phase-0-prereg-amendment-3.md:665-675 vs :833]

---

### End lists, §3 (`S3.md`)

### Open items raised in §3

- **O-B1 — Exact binary frame layout.** Layout, field widths and endianness unfixed; to be fixed with golden vectors before the Band 1 freeze. [docs/phase-0-prereg-amendment-1.md:262-264; docs/band-1-docket.md:37-40]
- **O-B2 — Algorithm-identifier encoding.** Location pinned inside the canonical payload; exact encoding left to P8's framing proof and golden vectors before Band 0 exit. [docs/phase-0-prereg-amendment-3.md:491-502; formal/COVERAGE-MAP.md:31]
- **O-B3 — Forward-link / successor-slot mechanism.** Location ruled and registration scheduled before format freeze; the mechanism itself is not frozen and may be substituted. [formal/spike/standing-probe/DECISION.md:368-377; docs/band-1-docket.md:355-384]
- **O-B4 — Degraded-verdict record format.** The six observation values are registered; the record format is an undecided H1a obligation. [docs/phase-0-prereg-amendment-5.md:153-155; docs/band-1-docket.md:62-66]
- **O-B5 — Refusal-record handoff and commitment construction.** "The handoff mechanism remains open"; the commitment text states resistance requirements and names no construction. [docs/phase-0-prereg-amendment-3.md:596-597; docs/phase-0-prereg-amendment-3.md:648-653]
- **O-B6 — One TLR per key or per identity.** Explicitly not decided; a single TLR under one key may still name cores from both identities. [docs/phase-0-prereg-amendment-5.md:214-219; formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:78-80]
- **O-B7 — Package completeness / self-containment.** P7's "inner bytes travel inside the bundle" is exercised for inner bytes and signature only; inner manifest, evidence and possession are presenter-supplied in the S-P7 models. [formal/COVERAGE-MAP.md:55; formal/suite/s-p7/proverif/sp7_q2_degraded_compromised.pv:316-318]
- **O-B8 — Header material, size budget, custody of referenced bytes.** SPV header segment, header-authentication pinning, per-bundle byte budget, and what must remain obtainable behind a reference are all unregistered. [docs/band-1-docket.md:41-56; docs/band-1-docket.md:133-206]
- **O-B9 — Renewal-chain objects.** Verdict composition along a renewal chain, cumulative-only renewal, wrapper-lineage completeness and per-epoch anchor independence are candidates only. [docs/band-1-docket.md:245-320; docs/phase-0-prereg-amendment-3.md:273-278]
- **O-B10 — Numeric rejection at ingestion.** Rejecting out-of-range JSON numerics before canonicalization is a docket candidate, not a registered requirement. [docs/band-1-docket.md:32-36; docs/phase-0-prereg.md:502-506]

### Contradictions raised in §3

- **C-B1 — Four-field frame versus seven-field signer frame.** P8 registers `type_tag || canonicalization_version || payload_length || payload`; A5 §A5.4 describes every required signer's frame as carrying object type, algorithm, identity, manifest hash, canonicalization version, payload and key fingerprint (the as-modelled `framed` shape) while stating P3's field list and P8's frame are unchanged. [docs/phase-0-prereg-amendment-1.md:255-264; docs/phase-0-prereg-amendment-5.md:178-190]
- **C-B2 — Where the length is bound.** §4.3 requires length bound into the canonical bytes "not a side field"; P8 places `payload_length` in an envelope around the JCS payload because JCS carries no length header. [docs/phase-0-prereg.md:486-494; docs/phase-0-prereg-amendment-1.md:255-264]
- **C-B3 — "Keys or references" versus self-containment.** §4.4 permits the manifest to carry issuer public keys "or references"; P9 and A1.5 require the verdict to be a pure function of the bundle with evidence archived, never live availability. [docs/phase-0-prereg.md:527-535; docs/phase-0-prereg-amendment-1.md:278-281, :430-438]
- **C-B4 — Two standing output vocabularies.** The registered S-series table states "standing" / "no standing" plus four reason codes; the standing-probe and SC-3 texts state `ESTABLISHED` / `ABSENT` / `UNVERIFIABLE`. Neither maps one onto the other, and the report schema depends on which governs. The `ESTABLISHED` / `ABSENT` / `UNVERIFIABLE` triple is also registered amendment text (A3 §A3.7.1), so this is registered-against-registered, not spike-against-amendment. [formal/spike/first-link/DECISION.md:790-847; formal/spike/standing-probe/DECISION.md:61-141; docs/phase-0-prereg-amendment-3.md:542-546]
- **C-B5 — What §A5.6 leaves undecided about two identities on one key.** The model's claim block says it does not decide whether such an issuer keeps one TLR or two; the same family's RESULTS quotes the registered wording as "beyond their having separate lineages". [formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:78-80; formal/suite/s-standing/RESULTS.md:1197-1199]

### End lists, §4 and §8 (`S4-S8.md`)

### Open items raised in §4/§8

- **O-C1 — Refusal-record handoff mechanism.** "The handoff mechanism remains open." [docs/phase-0-prereg-amendment-3.md:596-597; R-4.69]
- **O-C2 — Retention horizon T and minimization policy.** Declared bounded horizon with no value; the docketed candidate adds a declared maximum delivery/publication latency. [docs/phase-0-prereg-amendment-3.md:583-592; docs/band-1-docket.md:18-24]
- **O-C3 — The commitment construction.** Only a resistance requirement and the non-claims are registered; no construction is named. [docs/phase-0-prereg-amendment-3.md:648-653; R-4.103, R-4.104]
- **O-C4 — Refusal reporting surface.** Observer roles are registered; the reporting surface is not frozen. [docs/phase-0-prereg-amendment-3.md:614-617; R-4.72]
- **O-C5 — One terminal lineage record per key, or per identity.** Explicitly not decided. [docs/phase-0-prereg-amendment-5.md:214-219; R-4.93]
- **O-C6 — Frame binary layout and algorithm-identifier encoding.** Both fixed with golden vectors before the Band 1 freeze; unfixed in the record. [docs/phase-0-prereg-amendment-1.md:262-264; docs/phase-0-prereg-amendment-3.md:491-502]
- **O-C7 — Forward-link / successor slot mechanism.** Registration scheduled before format freeze; the mechanism is not frozen and may be substituted. [docs/band-1-docket.md:355-384; formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:182-206]
- **O-C8 — Review-staleness threshold.** Required as a failing invariant "past a declared threshold"; no value is given. [docs/phase-0-prereg.md:564-572; docs/phase-0-prereg.md:595-598]
- **O-C9 — Tending cadence.** Lives in each custodial policy; no global duration is frozen. [docs/phase-0-prereg-amendment-3.md:447-452; docs/phase-0-prereg-amendment-3.md:419-423]
- **O-C10 — Bundle-size budget.** Candidate only; interacts with first-link criterion 4 and with custody of the committed representation (docket 17). [docs/band-1-docket.md:54-56; formal/spike/first-link/DECISION.md:261-275]
- **O-C11 — Numeric-precision rejection at ingestion.** Candidate for the Band 1 ingestion spec; not registered. [docs/band-1-docket.md:32-36; docs/phase-0-prereg-amendment-1.md:264-273]
- **O-C12 — Local-GPG signing path under automation.** Execution model and attempt-loop behaviour on signer unreachability unspecified. [docs/band-1-docket.md:11-17; docs/phase-0-prereg-amendment-2.md:252-262]
- **O-C13 — Issuer signing-key lifetime and rotation policy.** No declared maximum validity window, no rotation cadence, no boundary behaviour registered. [docs/band-1-docket.md:385-400; docs/phase-0-prereg.md:454-469]
- **O-C14 — Extended atomic-entry refusal invariant, unmodelled.** Registered as a Band 0 model obligation; tracker row `open`, artifact "—". [docs/phase-0-prereg-amendment-3.md:814-831; formal/PROPERTIES.md:48, 260]

### Contradictions raised in §4/§8

- **C-C1 — What predicate the issuer evaluates at ship.** §A3.7.3's panel repair scopes the Ship guard to the three-conjunct temporal predicate plus burial depth and states the issuer "does not re-run envelope verification (P1–P3) at ship"; the §A3.9 obligations summary lists "A2.1 prose repair (issuer ships on full `VALID_STRICT`)". [docs/phase-0-prereg-amendment-3.md:665-673; docs/phase-0-prereg-amendment-3.md:832]
- **C-C2 — Which k the P5c family checks.** The P5c header registers k = 6 hence `DepthK = 5`, and the tracker's ratification line carries k = 6; the P5c cfg sets `DepthK = 2` (k = 3) and the bridge cfg sets `KConf = 3`, `DepthK = 2`, with `PinAgreement` checking only `DepthK = KConf − 1`. [formal/tla/P5c_IssuanceProtocol.tla:26-29 and formal/tla/P5c_IssuanceProtocol.cfg:15-19; formal/tla/P5cP5P6_Bridge.cfg:1-14 and formal/PROPERTIES.md:167-168]
- **C-C3 — Whether `ExpiredCannotShip` is the registered expiry rule.** P5c makes every unshipped attempt past its window unable to ship; the registered lifecycle latches eligibility so expiry applies only strictly after the boundary and only to attempts with no timely-latched eligibility. [formal/tla/P5c_IssuanceProtocol.tla:305-310, 34-45; docs/phase-0-prereg-amendment-2.md:150-160]
- **C-C4 — Status of the P5c↔P5P6 correspondence.** The P5P6 header calls the correspondence "exact by construction, not by argument"; the same file's 2026-09-06 correction and the tracker state it was "asserted in comments and checked nowhere" until the bridge. [formal/tla/P5P6_TemporalRevocation.tla:14-19, 26-36; formal/PROPERTIES.md:101-104]
- **C-C5 — The standing report's output vocabulary.** The registered S-series table states the verdict as "standing"/"no standing" with reason codes; the standing-probe scoring and SC-3 state outcomes as `ESTABLISHED` / `ABSENT` / `UNVERIFIABLE`. Neither document maps one vocabulary onto the other. [formal/spike/first-link/DECISION.md:797-801, 838-847; formal/spike/standing-probe/DECISION.md:61-71, 116-141]
- **C-C6 — Whether the manifest may carry key *references*.** prereg §4.4 permits the issuer-key manifest to carry "the issuer public keys (**or references**)"; P9 requires the verdict to be "a pure function of the bundle" with no live network dependency, and A1.5 requires both authority evidences archived in the bundle, "never live repository availability". A1 never withdraws "or references". [docs/phase-0-prereg.md:527-535; docs/phase-0-prereg-amendment-1.md:278-281, 430-438]

---

### End lists, §5 and §9 (`S5-S9.md`)

### Open items raised in §5/§9

- **O-D1 — Review-staleness threshold undeclared.** §4.7 and the §5 done-line make staleness past "a declared threshold" a failing invariant; no value is given. [docs/phase-0-prereg.md:564-572; docs/phase-0-prereg.md:595-598]
- **O-D2 — δ, ε, k, N, S unratified; the models check a different k.** Working defaults δ = 72 h, ε = 24 h, k = 6, N = 3, S = 24 h are ratified or revised at Band 0 exit; the P5c and bridge cfgs instantiate k = 3 with no parameter-independence argument. [docs/phase-0-prereg-amendment-1.md:177-190; docs/phase-0-prereg-amendment-2.md:270-274; formal/tla/P5c_IssuanceProtocol.cfg:15-19]
- **O-D3 — Degraded-verdict record format.** Registered as an H1a obligation on the band-1 docket; no format exists. [docs/phase-0-prereg-amendment-5.md:152-153; docs/band-1-docket.md:62-66]
- **O-D4 — Header authentication rules deferred.** Proof-of-work validity, cumulative-work or checkpoint anchoring, store identity pinned in policy, and bundle/store conflict rules are named and their specification deferred. [docs/phase-0-prereg-amendment-2.md:197-206; docs/band-1-docket.md:44-49]
- **O-D5 — Exact algorithm-identifier encoding unfixed.** The location is pinned inside the canonical payload; the encoding waits on P8's framing proof and golden vectors. [docs/phase-0-prereg-amendment-3.md:491-502; formal/COVERAGE-MAP.md row 15]
- **O-D6 — The §A5.4 framing fork, reading (a) vs (b).** If the author meant one shared frame, P3's field list and P8's frame change and the S-P2 addendum is withdrawn. [docs/phase-0-prereg-amendment-5.md:166-182; formal/suite/ROUTED-2026-09-06.md:470-479]
- **O-D7 — The exact binary frame layout is not fixed.** Registered as an obligation to be discharged with golden vectors before the Band 1 freeze. [docs/phase-0-prereg-amendment-1.md:262-264; formal/COVERAGE-MAP.md row 9]
- **O-D8 — One terminal lineage record per key, or per identity.** Explicitly not decided; a single TLR under one key may still name cores from both identities. [docs/phase-0-prereg-amendment-5.md:214-219; formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:78-80]
- **O-D9 — The log-versus-verdict boundary has no registered text.** COVERAGE-MAP row 14 is a clerk's reading, PROPOSED, with no tool leg. [formal/COVERAGE-MAP.md row 14; docs/band-1-docket.md:520-530]
- **O-D10 — Two registered model obligations are unmodelled.** The unknown-algorithm P4-partition transition with its fail-open companion, and the extended atomic-entry refusal invariant with its two companions. [formal/PROPERTIES.md:47-48; formal/PROPERTIES.md:260]
- **O-D11 — The binding-form required set is unmodelled and its lifecycle deferred.** No suite verifier carries a required-set-of-forms input; form lifecycle, registry epoch and the reference-verifier obligation are deferred with nothing implemented. [formal/spike/first-link/DECISION.md:366-405; formal/spike/first-link/DECISION.md:436-461]
- **O-D12 — Custody of externally-referenced verification inputs has no owner.** Retention, replication, discovery and retrieval-testing responsibility for bytes a verifier must fetch from outside the envelope is unassigned. [docs/band-1-docket.md:133-145; formal/spike/first-link/DECISION.md:261-275]
- **O-D13 — Package completeness is an open coverage cell.** P7's "the inner bytes must travel inside the bundle" is exercised for bytes and signature only; the inner manifest, evidence and possession proof are presenter-supplied. [formal/COVERAGE-MAP.md amendment note 1; formal/suite/s-p7/RESULTS.md:646-654]

### Contradictions raised in §5/§9

- **C-D1 — Is anchor lateness ever a waivable observation?** A2 registers temporal-anchor consistency as non-waivable with the P4 partition inside it; A5 §A5.3 lists `anchor-late` among the six observations recorded for a waived check whose condition never determines the verdict. [docs/phase-0-prereg-amendment-2.md:245-248; docs/phase-0-prereg-amendment-5.md:96-100, :145-150]
- **C-D2 — "`UNVERIFIABLE` for exactly one case" versus three further assignments.** §A3.6.2 registers the algorithm-identifier case as the only one; the same amendment assigns `UNVERIFIABLE` to an entirely-unavailable authority-evidence set, to an unavailable issuance-profile dependency, and as a protocol-standing dimension value. [docs/phase-0-prereg-amendment-3.md:503-505; docs/phase-0-prereg-amendment-3.md:146-149, :353-356, :541-546]. Three further registered `UNVERIFIABLE` assignments outside that amendment are also unreconciled with the "exactly one case" wording: headers unavailable (A2 §A2.2, docs/phase-0-prereg-amendment-2.md:245-248); the binding-form required set's unknown and known-but-unsupported cases (first-link/DECISION.md:376-378); and `STANDING_EVIDENCE_TEMPORAL_MISMATCH` (standing-probe/AMENDMENTS-2026-08-31.md:44-47)
- **C-D3 — Two unmapped standing output vocabularies.** The S-series table reports standing / no standing with reason codes; the standing-probe and SC-3 texts report `ESTABLISHED` / `ABSENT` / `UNVERIFIABLE`. Neither document maps one onto the other. [formal/spike/first-link/DECISION.md:790-847; formal/spike/standing-probe/DECISION.md:61-141]
- **C-D4 — Revocation after issue.** Prereg §4.4 says a key revoked after issue leaves the attestation `VALID_STRICT`; P6 as amended yields `INVALID` for a revocation between `declared_issue_time` and `anchor_time`. [docs/phase-0-prereg.md:537-546; docs/phase-0-prereg-amendment-1.md:199-233]
- **C-D5 — Where length is bound.** §4.3 requires length bound into the canonical bytes and not a side field; P8 places `payload_length` in the frame around the JCS payload. [docs/phase-0-prereg.md:486-494; docs/phase-0-prereg-amendment-1.md:255-264]
- **C-D6 — Keys "or references" versus P9 self-containment.** §4.4 permits the manifest to carry references; P9 and A1.5 require the verdict to be a pure function of the bundle with the evidence archived, never live availability. [docs/phase-0-prereg.md:527-535; docs/phase-0-prereg-amendment-1.md:278-281, :430-438]
- **C-D7 — Are `ot` and `cv` checks or carried fields?** The S-P3 model headers state they are included in the signed bytes but unexercised; the reading aid's verifier-check tables label them CARRIED inside a column of check statuses. [formal/suite/s-p3/proverif/sp3_q2_degraded_compromised.pv:53-55; formal/suite/s-p3/READING-AIDS.md:177, :302]
- **C-D8 — Prohibiting downstream ordering versus not deciding for the adjudicator.** A2 §A2.4 forbids any downstream marketplace rule from ordering receipts by declared time; A4 §A4.6 registers that Tessera does not decide what the adjudicator should do. [docs/phase-0-prereg-amendment-2.md:327-333; docs/phase-0-prereg-amendment-4.md:159-182]
- **C-D9 — What a non-`attemptCore` presentation produces after the §A5.6 pin.** The model's claim block says no lineage-derived report and the no-TLR report unaffected; RESULTS.md says no report at all. [formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:88-91; formal/suite/s-standing/RESULTS.md:1203-1207]
- **C-D10 — COVERAGE-MAP row 1 versus S-P1's record.** Row 1 states the symbolic leg is "none — S-P1 enumerated, not built" and that S-P1 consumes S-P3's key binding; S-P1's RESULTS records five models built and run and the relation as complementary, not consumed. The row text is unchanged. [formal/COVERAGE-MAP.md:23; formal/suite/s-p1/RESULTS.md:536-556]
- **C-D11 — Is `ExpiredCannotShip` the registered expiry rule?** The invariant makes every unshipped attempt past its window unable to ship; the registered lifecycle latches eligibility, so expiry applies only strictly after the boundary and only to attempts with no timely-latched eligibility. [formal/tla/P5c_IssuanceProtocol.tla:305-310; docs/phase-0-prereg-amendment-2.md:150-160]

---

### End lists, §6 and §7 (`S6-S7.md`)

### §11 Open items raised in §6/§7

- **O-E1** One terminal lineage record per key, or per identity, is not decided. [docs/phase-0-prereg-amendment-5.md:214-219; formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:78-80]
- **O-E2** The standing path's `if kT = kX` check (TLR key equals presented key) is "a fixture-shape restriction no registered text requires"; whether it is a conformance requirement is unstated. [formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:51-52; :337-338]
- **O-E3** `STANDING_EVIDENCE_MISMATCH` and `STANDING_EVIDENCE_SIGNATURE_INVALID` have no registered home comparable to SC-3's registration of the other two codes. [formal/spike/standing-probe/DECISION.md:61-71, :119; formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:144-155]
- **O-E4** Standing behaviour for lineages of other than two attempts is neither modelled nor registered. [formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:130-136; formal/suite/s-standing/RESULTS.md:540-556]
- **O-E5** The TLR anchor's temporal validity (SC-1) is a cross-formalism consumed obligation owed to the bridge and "must never be marked discharged" by the symbolic standing family. [formal/suite/s-standing/RESULTS.md:484-536; formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:22-47]
- **O-E6** The refusal-record handoff mechanism "remains open." [docs/phase-0-prereg-amendment-3.md:592-597; :583-589]
- **O-E7** Custody of externally referenced verification inputs: what must remain obtainable, who retains it, how a verifier discovers it, how retrieval is tested. [docs/band-1-docket.md:139-186; formal/spike/first-link/DECISION.md:916-920]
- **O-E8** Tending cadence is a per-policy parameter; no global duration is frozen. [docs/phase-0-prereg-amendment-3.md:447-452; :424-437]
- **O-E9** Exact trigger expressions, clock, monitoring surface and succession mechanism for tending remain design obligations. [docs/phase-0-prereg-amendment-3.md:419-423; docs/band-1-docket.md:117-138]
- **O-E10** The exact encoding of the algorithm identifier inside the canonical payload is not frozen; P8's framing proof and golden vectors must fix it before Band 0 exit. [docs/phase-0-prereg-amendment-3.md:491-502; :878-885]
- **O-E11** Hybrid classical plus PQ dual signing is deferred to a deployment profile or later amendment. [docs/phase-0-prereg-amendment-3.md:480-483; docs/phase-0-prereg.md:339-345]
- **O-E12** Issuer signing-key lifetime, rotation cadence and verifier behaviour at the window boundary are registered nowhere; two candidate rules are recorded, neither agreed. [docs/band-1-docket.md:386-410; :405-465]
- **O-E13** Verdict composition along a renewal chain (per-link epochs, meaning of one `UNVERIFIABLE` link, where standing sits) is not registered. [docs/band-1-docket.md:245-267; docs/phase-0-prereg-amendment-3.md:158-164]
- **O-E14** The retention horizon for the refusal record and the post-terminal minimization policy are declared per deployment, not fixed. [docs/phase-0-prereg-amendment-3.md:583-592; :642-648]
- **O-E15** The commitment construction for the refusal record is not named; only its resistance requirement and its non-claims are registered. [docs/phase-0-prereg-amendment-3.md:648-653]
- **O-E16** The refusal reporting surface is not frozen; only observer roles are registered. [docs/phase-0-prereg-amendment-3.md:614-621; :639-642]

### §12 Contradictions raised in §6/§7

- **C-E1** Two unreconciled vocabularies for the same standing report: "standing" / "no standing" plus reason codes, versus `ESTABLISHED` / `ABSENT` / `UNVERIFIABLE`; neither document maps one onto the other. [formal/spike/first-link/DECISION.md:798-801, :826, :838-847 vs formal/spike/standing-probe/DECISION.md:61-71, :138-141 and docs/phase-0-prereg-amendment-3.md:541-546]
- **C-E2** §A3.6.2 registers "`UNVERIFIABLE` for exactly one case", while §A3.4 assigns `UNVERIFIABLE` to an unavailable issuance-profile dependency "for the affected check", §A3.2.2 to a layer whose external authority evidence is entirely unavailable, and §A3.7.1 lists it as a standing-dimension value. [docs/phase-0-prereg-amendment-3.md:503-505 vs :353-356, :146-149, :541-546]
- **C-E3 — recorded and resolved in the record; not an open conflict.** The frozen `PREDICTIONS.md` sentence quoted at RESULTS.md:1197-1199 ("beyond their having separate lineages") diverges from signed Amendment 5 §A5.6, and the record says which governs: "the frozen plan and the signed amendment diverge there and the amendment governs", repeated at RESULTS.md:1318-1333 ("`PREDICTIONS.md` is frozen and was not edited; its registered sentence stands on the record as written and is wrong"). Noted only because the superseded sentence is still on the page. [formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:78-80; formal/suite/s-standing/RESULTS.md:1197-1199, corrected at :1318-1333]
- **C-E4 — recorded and resolved in the record; not an open conflict.** RESULTS.md:1203-1207 still carries the pre-correction wording ("no report at all"), and the same file corrects it at :1335-1348: "**5 — "produces no report at all" is overbroad**", the right statement being that such a presentation "produces no lineage-derived report (no mismatch, supersession or refusal report); the no-TLR report is unaffected." The claim block carries the corrected form. Noted only because the superseded sentence is still on the page. [formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:88-91; formal/suite/s-standing/RESULTS.md:1203-1207, corrected at :1335-1348]
- **C-E5 — two status labels, with the record's own reconciliation stated.** The standing-probe decision record retains "**Status: PROPOSED — scoring draft, nothing decided.**" beside the correction notes recording entry (2026-09-04), and gives the reason: "The registered PROPOSED header is retained below, per amend-don't-rewrite." The gate scoring under that header therefore remains scoring-draft provenance (see R-6.9–R-6.11, R-6.38, R-6.39), while sub-ruling 5 is ADOPTED. What is stale rather than contradictory is the twice-repeated "author commit pending": the author committed `DECISION.md` and `AMENDMENTS-2026-08-31.md` at `fbf6387` (2026-09-04, "Another round: mostly decisions, a few small clarifications.  Ratified and time to move forward."). [formal/spike/standing-probe/DECISION.md:3-13, :12-13, :15-26, :28-41; commit `fbf6387`]

---

Non-author review: pending (Codex); author read: pending.

**Post-assembly correction (owner instance, 2026-09-13).** C-01, C-02 and C-14 were moved from the open table to the settled table as S-14, S-15, S-16: C-01 is answered by A1 §A1.4 (a signed amendment revising the original's tool sentence), C-02 by A1 P6 as clarified by A4 §A4.3, C-14 by the three reading-aid files in `formal/tla/`. Open contradictions: 11 (C-03 to C-08, C-10 to C-13, C-15). Settled: 16. A tracker note about the reading aids was appended to `formal/PROPERTIES.md`. The §0 status block now names the Opus 5 agents the owner instance directed.

---

## Repairs after the Codex review (2026-09-13)

Six repairs, one per ACCEPTED disposition in
`docs/reviews/2026-09-13-codex-review-implementation-spec.md`. The spec is an
unfrozen PROPOSED draft, so every repair is an in-place amendment; no model,
amendment, tracker row or prediction file changed. Every cited line was opened
before the edit. Requirement count before: 455 (`grep -c '^\*\*R-'`); after: 456
(one new requirement, R-6.24a; nothing renumbered). No local labels (`O-[A-E]n`,
`C-[A-E]n`) were introduced.

| Finding | IDs touched | What changed | Lines checked |
|---|---|---|---|
| 1.1 | V7 (§5.2 stage (a)); R-5.25 (see 4.1) | Retagged `[DOCKET 17 — candidate, not a member of the check map]`; the source's confinement carried verbatim ("Retrieval failure yields `UNVERIFIABLE` with a reason code distinguishing *not retrieved* from other unverifiable causes, and per item 16 must not contaminate the base verdict"); the row now states V7 is not in `Checks`, never enters the R-5.25 aggregation, and names no alternative result destination | `docs/band-1-docket.md:163-171` (confinement sentence at :168-171), :133-145 |
| 1.2 | V1 (§5.2 stage (a)); new §11 **O-78** | Predicate restated as the source's: an unknown canonicalization version is rejected → `INVALID`. The recognized-but-unimplemented case is given no verdict and is entered as O-78 at the end of the Verification area, with V1's registered-vs-modelled cell tagged `[OPEN — §11 O-78]`. §11's preamble and the open-entry count (75→76, Verification 18→19) updated | `docs/phase-0-prereg-amendment-1.md:264-275` (rejection list at :267-273) |
| 1.3 / 4.2 / 5.5 | §6.3 lead; new **R-6.24a**; §5.5 coverage row; §10.2 H1a row | §6.3's lead now says "The procedure as S-STANDING models it" and that R-6.24's steps are the model's. R-6.24a states the registered SC-3 internal-consistency rule as its own requirement, evaluated before the model's step 11, covering both shapes the model treats ordinarily. A registered-vs-modelled note records that `StandingDecide` returns refusal and supersession without inspecting `d`, so the model is narrower than SC-3, and that the family's own record assigns malformed handling beyond emitting the code to the vector track. One coverage row added to §5.5, one H1a vector row to §10.2 | `formal/spike/first-link/DECISION.md:834-843` (MALFORMED bullet at :838-843); adopted text `formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:146-151`; `formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:296-317`; `formal/suite/s-standing/RESULTS.md:540-556`, the vector-track sentence at :547-549 |
| 2.1 | R-3.61 (§3.7); four rows of §5.3's reason-code table | `STANDING_EVIDENCE_MISMATCH` and `STANDING_EVIDENCE_SIGNATURE_INVALID` retagged probe-observed `[MODELLED standing probe, formal/spike/standing-probe/DECISION.md:116-129]` with `[OPEN — §11 O-75]`; `STANDING_EVIDENCE_MALFORMED` and `STANDING_EVIDENCE_TEMPORAL_MISMATCH` keep RULED (SC-3). The §5.3 table now says the same in its source column | `formal/spike/standing-probe/DECISION.md:110-135` (R3 finding at :116-129); `formal/spike/first-link/DECISION.md:834-847` |
| 3.1 | new **V33a** (§5.2 stage (h)); two rows of §5.1's field-to-check map; §5.5 coverage row | V33a: the shipped anchor proof is evaluated over this receipt's canonical bytes and over no other, and the block its merkle path authenticates is the block used for V33–V36's depth and timestamp comparisons; failure → `INVALID`. Modelled nowhere — the TLA+ module abstracts proof and signature validity. §5.1's OTS-proof row now names V33a, and a row for the merkle path and its authenticated block was added; §5.5 carries the coverage cell. Existing V-numbers unchanged | `docs/phase-0-prereg-amendment-2.md:299-322` (the two quoted clauses at :307-308 and :319-320); `formal/tla/P5P6_TemporalRevocation.tla:52-56` |
| 4.1 | R-5.25; V27 and V40 rows (§5.2) | R-5.25 gains an explicit membership sentence: `Checks` holds the envelope checks of stages (a)–(i) only; V27 and V40 are standing checks feeding the §6 report and never the envelope verdict; V7 is a docket candidate outside the map. Tagged `[REGISTERED A3 §A3.7.1, docs/phase-0-prereg-amendment-3.md:542-557]`, with the P4 tag qualified (the ladder does not fix the set's membership) and the S-STANDING path separation cited. V27's and V40's registered-vs-modelled cells now open "Standing row; not in `Checks` (R-5.25)" | `docs/phase-0-prereg-amendment-3.md:538-560`; `formal/tla/P4_VerifierStates.tla:94-105`; `formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:322-379` |

Appendix A: one row added for R-6.24a in document order; the §6 count moved
54→55 and the total 455→456. Nothing renumbered. The provenance-kind occurrence
table below the counts was generated over §1–§9 by a method this pass did not
reproduce, and was left as generated.

Finding 5.1–5.4 (traces) needed no action, per its disposition.

---

## Amendment 7 rulings applied (2026-09-14)

Source of truth: `docs/phase-0-prereg-amendment-7.md` (read in full first), the
instrument for the author's 2026-09-14 rulings on the eleven open items of
`docs/implementation-spec.md` §12. A7 is PROPOSED and becomes in force on the
author's first commit containing it, so every tag this pass wrote reads
`[RULED (author) 2026-09-14; instrument A7 §A7.n, PROPOSED]`. The spec is an
unfrozen PROPOSED draft, so every edit is an in-place amendment; no amendment,
model, tracker row, reading aid, coverage map, docket or exit list was edited by
this pass (A7 §A7.8's E18 and §A7.9's docket item 33 already stand in
`formal/BAND0-EXIT.md` and `docs/band-1-docket.md`; §A7.10's COVERAGE-MAP and
S-P3 reading-aid corrections are recorded here as record facts, not made here).
Every cited line was opened before the edit. Nothing in this pass resolves a
contradiction on the specification's own authority.

**§12.** The eleven entries (C-03 to C-08, C-10 to C-13, C-15) moved out of
"Open, author ruling needed" into a new subsection **"Ruled 2026-09-14,
instrument Amendment 7 (PROPOSED)"**, placed before the settled table. Each
keeps its two passages, its implementer note and its Governs line, and gains:
`**Status**: RULED (author) 2026-09-14 — instrument Amendment 7 §A7.n (PROPOSED;
in force on the author's commit).`, `**Ruling**: "<the author's verbatim words>"`,
an `**Instrument**` line, and — for C-05 (§A7.3 "still not non-waivable" read as
"still non-waivable") and C-08 (§A7.6 "burial death" read as "burial depth") — a
`**Reading marked for correction**` line. Sentences the open entries carried
beyond the status ("no later dated note reconciles the two", "interacts with
O-44", and so on) are kept as record notes. "Open, author ruling needed" now
holds one line: no entry remains open as of 2026-09-14, and IDs are not reused.
C-07's "Implementer" paragraph is corrected per A7 §A7.5 — scoping A to
algorithm-identifier handling does *not* leave `:146-149` and `:353-356` in
conflict; they are independent unperformable checks — with the correction dated
and attributed to the non-author reviewer's finding. §12's preamble now reads
eleven ruled, sixteen settled, none open.

**Body consequences**, one row per item:

| Item | Sections edited | IDs touched | What changed |
|---|---|---|---|
| C-03 (§A7.1) | §3.1, §3.2, §9.1 | new prose in §3.1 and §3.2; R-9.4 marker | Canonical payload bytes and signed frame defined as two byte strings where the frame is introduced; the original §4.3 length sentence cited as superseded by A1 P8 and read as "bound into the signed bytes"; golden vectors owed for both separately |
| C-04 (§A7.2) | §3.4, §4.4, §5.1 | new **R-3.31a**; R-3.31, R-4.24, R-5.13 | References permitted when resolvable from the bundle or from declared trusted inputs (§2.3), never a live lookup; unresolvable → the needing check is unperformable (`UNVERIFIABLE`); A1 §A1.5's "archived in the bundle" unchanged. R-5.13 restated |
| C-05 (§A7.3) | §2.4, §5.3, §9.2 | new **R-2.31a**; R-2.31, R-2.36, R-5.40 | The receipt's own anchor conjuncts are non-waivable (`INVALID` when failed); `anchor-late` is an observation against a waived redundant authority evidence's own anchor. A7's reading marked for correction carried once, in §2.4 |
| C-06 (§A7.4) | §1.3, §4.7, §5.4 | new **R-1.10a**; R-4.78, R-5.62 | A2 §A2.4's ordering prohibition binds Tessera's own surfaces, policies and claims; adjudicators reason for themselves; not a service-refusal requirement. A7's narrowing of the bearer recorded as such |
| C-07 (§A7.5) | §5.2 stage (c), §5.3, §7.1, §7.4 | V14; the `UNVERIFIABLE` row of §5.3's verdict table; R-7.7a, R-7.38 | "Exactly one case" bounds the algorithm-identifier check only; every other required check is independently unperformable; the standing dimension's value is not a P4 verdict |
| C-08 (§A7.6) | §2.1, §4.4, §4.7, §4.10 | new **R-4.77a**; R-2.3, R-4.36; a ruling note on §4.10 row 3 | The §A3.7.3 repair governs: three temporal conjuncts plus burial depth `DepthK = k − 1`, no envelope re-verification at ship; the §A3.9 summary line is superseded, not edited |
| C-10 (§A7.7) | §3.7, §5.3, §6.4 | new **R-3.60a**; R-3.60, R-3.61, R-5.52, R-6.35, the `protocol_standing` row and the reason-code table | One vocabulary `ESTABLISHED` / `ABSENT` / `UNVERIFIABLE`, with A7 §A7.7's mapping table copied verbatim in §3.7 and §6.4; S-series names readable as aliases; `STANDING_EVIDENCE_MISMATCH` and `STANDING_EVIDENCE_SIGNATURE_INVALID` stay `[OPEN — §11 O-75]` |
| C-11 (§A7.10) | §5.5 | ruling note after the coverage table | S-P1 and S-P3 key binding are complementary, no cross-model entry; the rule "an entry exists only where severing the producer would falsify the consumer's query"; S-P2 and S-P7 determine their own (E5a); recorded in COVERAGE-MAP by an appended note |
| C-12 (§A7.10) | §5.2 stage (d) | V17 | `ot` and `cv` are bound, not checked at this layer; validation obligations are P7's and P8/H1a's; the two S-P3 reading-aid rows are corrected in place in that file, no model edited |
| C-13 (§A7.8) | §8, §10.1, §4.10 | new **R-8.9**; the k row; §4.10 row 12 | k = 6 preserved; the checked `DepthK = 2` is evidence for the abstraction, not the parameter; obligation **E18** named and added to §10.1 (E1–E17 → E1–E18) |
| C-15 (§A7.9) | §3.2, §10.2, §11 | new **R-3.12a**; R-3.12; O-01 | Four-field envelope and seven bindings both stand, joined by an encoding map settled pre-freeze (docket 33); the map added to §10.2's pre-freeze list and to §11 as **O-79**; O-01 now waits on O-79 |

**New O-numbers.** One: **O-79** (Format, end of the area) — the encoding map
joining P8's four-field signed frame to A5 §A5.4's seven signer-specific
bindings, deadline `pre-freeze`, citing A7 §A7.9 and band-1 docket item 33.
O-01 gains a note that it now waits on O-79. §11's preamble and counts updated
(76 → 77 entries, Format 13 → 14); a duplicated, stale count line left by an
earlier pass was removed in the same edit.

**§0.1** gains a row: "Amendment 7 — PROPOSED 2026-09-14; in force on the
author's first commit containing it."

**§1.5, the relying-party story** — five drafting repairs recommended by the
non-author reviewer on 2026-09-14 and adopted by the owner instance. They are
drafting corrections toward the record, not decisions; every cited line was
opened before writing. (i) The "What the anchor rests on" candidate paragraph is
removed: the hash-failure survivability claim is docket-24 candidate text, not
registered. Its registered second sentence survives as "What the anchor bounds"
(`docs/phase-0-prereg-amendment-1.md:477-491`). (ii) Envelope `UNVERIFIABLE` and
standing `UNVERIFIABLE` are separated into two sentences, and "a key you do not
hold" is now "a required public key unavailable to the verifier". (iii) A new
paragraph "What `INVALID` means" — a required check was performed and failed,
distinct from a check that could not be performed — cites A1 §A1.2 P4
(`docs/phase-0-prereg-amendment-1.md:152-158`) and the original §4.6
(`docs/phase-0-prereg.md:555-562`). (iv) "Standing evidence is what tells you
which" is qualified: it establishes the designation the presented evidence
supports and does not establish that no contradictory terminal record exists,
citing the equivocation boundary (`formal/suite/s-standing/RESULTS.md:540-546`,
"What S-STANDING does not discharge", first bullet). (v) The "in 2106 Tessera
will not exist in its current form" sentence is replaced by "verification must
not depend on Tessera still existing", cited to the original §4.4 ("An
attestation must verify with the service **dead**",
`docs/phase-0-prereg.md:519-525`). The section's standfirst now records that no
candidate sentence remains in it. §1.5 stays about one page.

**Counts and checks.** Requirements before 456, after **463**: seven added —
R-1.10a, R-2.31a, R-3.12a, R-3.31a, R-3.60a, R-4.77a, R-8.9 — and nothing
renumbered. Appendix A gains one row for each in document order; the four rows
whose provenance tags changed (R-4.78, R-5.13, R-5.52, R-6.35) were updated to
match the body verbatim; the §1, §2, §3, §4 and §8 counts and the total were
moved. `grep -c 'OPEN - author ruling needed'` = 0. No local labels
(`O-[A-E]\d`, `C-[A-E]\d`) = 0. Every `R-` ID unique, and the body's 463 IDs and
Appendix A's 463 rows are the same set. Eighteen `[CONTRADICTION — §12 C-n]`
markers became `[RULED — §12 C-n, A7 §A7.m]` across §1–§9 and Appendix A; the
two remaining CONTRADICTION markers are C-02's, which is settled as S-15 and out
of this pass's scope. The provenance-kind occurrence table under Appendix A's
counts was generated by a method neither the 2026-09-13 repair pass nor this one
reproduced; it carries a dated note saying which two rows are now stale rather
than a regenerated number.

**Nothing in A7 was left unapplied.** The two words A7 marks for the author's
confirmation (§A7.3, §A7.6) are carried into §12 and, for C-05, into §2.4, with
A7's own withdrawal condition stated.
