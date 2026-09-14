# Codex non-author review of the implementation specification, first draft (2026-09-13)

Reviewer: OpenAI Codex CLI, model `gpt-6-astra`, run non-interactively from the
owner instance's shell with the repository readable (`codex exec`, prompt
archived at the end of this file). Subject: `docs/implementation-spec.md` as
of the 2026-09-13 assembly, after the three skeptic passes and the owner's
post-assembly moves (C-01/C-02/C-14 to settled). The reviewer's task was
adversarial: misstated contract, silent resolution, omission, procedure
against the models, off-happy-path traces. Every factual claim below was
checked against the tree before disposition.

## Dispositions (owner instance, 2026-09-13)

Repairs are applied to `docs/implementation-spec.md` in place (it is an
unfrozen PROPOSED draft; amend-don't-rewrite binds from its first commit)
and logged in `docs/reviews/2026-09-13-implementation-spec-assembly-log.md`.
No model, amendment, tracker row or prediction file changes on this review.

1. **1.1 — V7 imports a docket candidate into the operative table and drops its confinement.** ACCEPTED. V7 is retagged as a docket candidate outside the check map; the source's confinement ("must not contaminate the base verdict", `docs/band-1-docket.md:163-171`) is carried verbatim; the check-map definition (R-5.25) gains an explicit membership statement (see 4.1).
2. **1.2 — V1 says "supported" where the source says "unknown".** ACCEPTED. Predicate restated as the source's: unknown canonicalization version → `INVALID`. The recognized-but-unimplemented case is not registered and is entered in §11 as an open item, not given a verdict.
3. **1.3 / 4.2 / 5.5 — §6.3 presents the S-STANDING model's narrower consistency handling as "the registered procedure"; SC-3 registers `UNVERIFIABLE / STANDING_EVIDENCE_MALFORMED` for internally inconsistent evidence.** ACCEPTED. §6.3 is relabelled as the procedure *as modelled*; the registered SC-3 internal-consistency rule is stated as a check preceding the model's step 11, tagged REGISTERED (`formal/spike/first-link/DECISION.md:834-843`); the gap is recorded in §6.3's registered-vs-modelled column and in §5.5 coverage. The record already assigns malformed-evidence handling "beyond emitting the code" to the vector track (`formal/suite/s-standing/RESULTS.md`, "What S-STANDING does not discharge"), so this is a model-coverage fact, not a contradiction; the H1a standing vector for internal inconsistency is added to §10.2.
4. **2.1 — R-3.61 promotes two probe-observed codes to RULED.** ACCEPTED. `STANDING_EVIDENCE_MISMATCH` and `STANDING_EVIDENCE_SIGNATURE_INVALID` retagged as probe-observed / MODELLED with `[OPEN — §11 O-75]`; `STANDING_EVIDENCE_MALFORMED` and `STANDING_EVIDENCE_TEMPORAL_MISMATCH` keep RULED (SC-3).
5. **3.1 — the procedure omits the receipt-to-anchor binding check.** ACCEPTED. A temporal-stage row is added: the shipped OTS proof is evaluated over the receipt's canonical bytes and its authenticated block is the block used for the depth and timestamp comparisons (`docs/phase-0-prereg-amendment-2.md:299-320`); modelled nowhere (the TLA+ modules abstract the binding; noted as a coverage cell).
6. **4.1 — V27 and V40 are not excluded from the envelope check map.** ACCEPTED. R-5.25's check map now states its membership: the standing rows (V27, V40) and the docket row (V7) are not members; standing rows feed the §6 report only; the envelope verdict never depends on standing evidence (`docs/phase-0-prereg-amendment-3.md:542-557`).
7. **5.1–5.4 traces — record agrees.** No action; recorded as evidence that the multi-signer, lying-wrapper, unsupported-identifier and boundary-anchor paths are stated as registered.

**Method.** Every cited line was opened before disposition. Nothing was committed by the owner instance; the commit is the author's.

## Codex review — verbatim

# 1. Misstated contract

### 1.1 V7 imports an external-retrieval failure into the base-verdict procedure while dropping its source’s confinement

**Spec:** V7 assigns `UNVERIFIABLE` when a check “cannot obtain its input,” within the procedure that assigns the envelope verdict. (`docs/implementation-spec.md:1146–1148,1179–1179`)

**Source:** “Retrieval failure yields `UNVERIFIABLE` with a reason code distinguishing *not retrieved* from other unverifiable causes, and per item 16 **must not contaminate the base verdict**.” (`docs/band-1-docket.md:163–171`)

**Delta:** V7 omits the confinement and places a docket candidate in the operative decision table. An implementer folding V7 into R-5.25’s check map would downgrade the base verdict for a retrieval failure that the cited passage expressly confines outside it. The candidate tag does not specify an alternative result destination. (`docs/implementation-spec.md:1282–1286`)

### 1.2 V1 substitutes “supported” for “known”

**Spec:** “Canonicalization version known”; predicate `version ∈ verifier's supported set`; failure → `INVALID`. (`docs/implementation-spec.md:1173–1173`)

**Source:** The mandatory rejection list names “unknown canonicalization versions.” (`docs/phase-0-prereg-amendment-1.md:267–273`)

**Delta:** The predicate rejects a version the verifier recognizes but does not implement. The cited source does not equate those cases or register that additional `INVALID` transition. An implementer would classify recognized-but-unsupported canonicalization as malformed by implementing the stated predicate. This finding does not prescribe the missing case’s verdict.

### 1.3 R-6.24 narrows SC-3’s internal-consistency rule to one affirmative-standing branch

**Spec:** Step 11 sends `TERM_REFUSED` directly to `ABSENT / ISSUANCE_REFUSED`, and a shipped identity different from the presented identity to `ABSENT / SUPERSEDED`. Step 12 checks `d = DISP_SHIPPED` only for the designated shipped identity. (`docs/implementation-spec.md:1527–1529`)

**Source:** “Internally inconsistent standing evidence (e.g., a terminal disposition contradicting the lineage’s own entry for that attempt …) yields `UNVERIFIABLE`” with `STANDING_EVIDENCE_MALFORMED`. (`formal/spike/first-link/DECISION.md:834–843`)

**Delta:** A signed TLR declaring `TERM_REFUSED` while marking the presented attempt `DISP_SHIPPED` receives ordinary refusal treatment in the procedure. Likewise, an entry marked shipped while another identity is terminally designated receives ordinary supersession treatment. Both contradict the broader registered consistency rule.

An implementer would report a definite terminal disposition where the record requires an inability to establish standing because the evidence contradicts itself. R-6.18 preserves the broader requirement, so the draft itself gives incompatible instructions. (`docs/implementation-spec.md:1489–1494`)

# 2. Silent resolution or promotion

### 2.1 R-3.61 promotes two probe-observed reason codes to author-ruled status

**Spec:** R-3.61 labels all four listed standing-error codes “RULED (author) 2026-09-04,” including `STANDING_EVIDENCE_MISMATCH` and `STANDING_EVIDENCE_SIGNATURE_INVALID`. (`docs/implementation-spec.md:767–771`)

**Source:** Its cited scoring passage calls these “Distinct defined outcomes **observed**,” labels the finding “pass with remediation (evidential),” and routes additions for registration. The dated SC-3 amendment registers the malformed and temporal-mismatch outcomes. (`formal/spike/standing-probe/DECISION.md:116–129`; `formal/spike/first-link/DECISION.md:834–847`)

**Delta:** Observed probe behavior becomes a registered output-schema obligation. The draft later explicitly acknowledges that the first two codes lack equivalent registration and leaves them open as O-75. An implementer following §3 would freeze a schema that §6 says remains unregistered. (`docs/implementation-spec.md:1572–1572`)

# 3. Omission

### 3.1 The executable verification checklist omits the receipt-anchor proof’s binding check

The registered requirement is to evaluate **the shipped proof over the receipt’s canonical bytes**; the OTS Merkle path binds those bytes to the block independently of the txid handle. (`docs/phase-0-prereg-amendment-2.md:299–320`)

The draft carries that obligation descriptively in R-3.42, but its field-to-check map sends the OTS proof exclusively to V33–V36. Those rows compare timestamps and designate confirmation depth; none verifies the proof’s commitment to the presented framed bytes or connects its authenticated block to the block used for those comparisons. V38 authenticates headers, which does not supply the missing receipt-to-block binding. (`docs/implementation-spec.md:634–638,1117–1119,1259–1264`)

This is a **procedural omission**, not an assertion that the obligation is absent from every paragraph. It belongs in §5.2’s temporal checks. An implementer translating the advertised checklist literally could accept a valid signature over one receipt together with another receipt’s genuine, in-window anchor evidence.

# 4. The procedure against the models

### 4.1 V27 and V40 lack an explicit exclusion from the envelope check map

V27 is the standing-core tuple pin; V40 is the TLR’s temporal check. Both appear in §5.2’s procedure, whose introductory rule assigns exactly one verdict and whose final rule computes it from `Checks \ waived`. V40’s failure cell says `UNVERIFIABLE / STANDING_EVIDENCE_TEMPORAL_MISMATCH`. No check-map definition there excludes these standing rows. (`docs/implementation-spec.md:1146–1148,1223–1223,1266–1266,1284–1286`)

The model separates `StandingPath` and `EnvelopePath`: the latter neither consumes standing evidence for acceptance nor performs the tuple pin as a standing prerequisite. The model explicitly calls their orthogonality structural. (`formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:322–363,365–379`)

P4’s ladder simply aggregates whatever belongs to `Checks`; it does not establish the correct membership of that set. (`formal/tla/P4_VerifierStates.tla:62–79,94–105`)

Consequently, a literal V1–V40 aggregation makes a late TLR downgrade an otherwise valid envelope. The registered contract instead requires the unchanged envelope verdict beside a separate standing result. The draft states that separation elsewhere, making this an internal procedural ambiguity rather than evidence that it consistently adopts the wrong outcome. (`docs/phase-0-prereg-amendment-3.md:542–557`; `docs/implementation-spec.md:1447–1451`)

### 4.2 The narrowed consistency check is copied faithfully from the model, but is not the full registered procedure

Finding **1.3** is not a transcription error: `StandingDecide` really returns refusal without inspecting `d`, and supersession without inspecting `d`; only the terminally designated identity reaches the `DISP_SHIPPED` check. (`formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:296–317`)

The defect is presenting that narrower implementation as “The registered procedure” without routing its difference from SC-3. (`docs/implementation-spec.md:1508–1510`) Model fidelity does not establish contract fidelity here.

For the other named models, the material predicates examined are transcribed faithfully: S-P2’s three additional common-content equalities, S-P3’s fingerprint/possession/signature/frame/manifest bindings, S-P7’s recorded-inner-version pin, and P4’s failure-before-unperformable precedence. (`docs/implementation-spec.md:1207–1220,1244–1247,1191–1191,1284–1286`; `formal/suite/s-p2/proverif/sp2_q2_degraded_compromised.pv:212–230`; `formal/suite/s-p3/proverif/sp3_q2_degraded_compromised.pv:101–109`; `formal/suite/s-p7/proverif/sp7_q2_degraded_compromised.pv:319–334`; `formal/tla/P4_VerifierStates.tla:94–103`)

# 5. Off-happy-path traces

Unless specified otherwise, all unrelated required checks pass, the waiver set is empty, authority evidence is valid, and no TLR is supplied. “Standing absent” below follows the draft’s §6.3 model vocabulary; it does not resolve C-10.

### 5.1 Two required signers, different payloads, individually valid signatures

Both signer frames pass their individual bindings. V30 fails payload equality; R-5.25 returns `INVALID`. The independent no-TLR branch reports `ABSENT / NO_TERMINAL_DISPOSITION_EVIDENCE`.

**Record agrees:** A5 requires all six non-fingerprint fields to agree, and the model explicitly tests payload equality before acceptance. (`docs/implementation-spec.md:1245–1247,1284–1286,1521–1521`; `docs/phase-0-prereg-amendment-5.md:179–190`; `formal/suite/s-p2/proverif/sp2_q2_degraded_compromised.pv:219–231`)

### 5.2 Valid inner package; wrapper records the wrong inner canonicalization version

V10 fails: outer verdict `INVALID`. The independently evaluated inner package remains `VALID_STRICT`. Neither layer gains standing without its standing evidence.

**Record agrees:** A5 registers rejection of the lying record, while P7 preserves the inner package’s independent verdict. (`docs/implementation-spec.md:1191–1192,1333–1333`; `docs/phase-0-prereg-amendment-5.md:192–200`; `docs/phase-0-prereg-amendment-1.md:248–253`)

### 5.3 Well-formed, correctly bound, unsupported algorithm identifier

V14 makes the required algorithm check unperformable. With no definite failure elsewhere, R-5.25 returns `UNVERIFIABLE`. The independently evaluated no-TLR branch reports standing absent.

**Record agrees:** This is precisely A3’s registered unsupported-algorithm case. (`docs/implementation-spec.md:1200–1201,1284–1286,1521–1521`; `docs/phase-0-prereg-amendment-3.md:503–518`)

### 5.4 Confirmation timestamp equals `declared_issue_time + δ`

V35 passes equality. With the anchor lower and upper bounds, burial, authentication, and remaining checks satisfied, the result is `VALID_STRICT`; standing is absent without a TLR.

**Record agrees:** The registered confirmation bound is inclusive, `confirmed_at ≤ declared_issue_time + δ`. This concerns the designated block timestamp, not wall-clock arrival. (`docs/implementation-spec.md:1259–1264,1284–1286`; `docs/phase-0-prereg-amendment-2.md:190–196,218–248`)

### 5.5 Valid envelope; authenticated, timely TLR says `TERM_REFUSED` but its entry says `DISP_SHIPPED`

Standing steps 1–10 pass. Step 11 immediately returns `ABSENT / ISSUANCE_REFUSED`; step 12 is bypassed. The envelope remains `VALID_STRICT`.

**Record disagrees with the standing report:** SC-3 requires `UNVERIFIABLE / STANDING_EVIDENCE_MALFORMED` for this internal contradiction. The envelope remains unchanged under either reading. (`docs/implementation-spec.md:1518–1529`; `formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:296–305`; `formal/spike/first-link/DECISION.md:838–843`; `docs/phase-0-prereg-amendment-3.md:542–546`)

**Verdict:** This draft is not yet a faithful executable statement of the current contract. The author should first see **1.3**, where the standing procedure understates registered malformed-evidence handling; **4.1**, where standing checks can enter the envelope-verdict aggregation; and **3.1**, where the temporal checklist lacks the receipt-to-anchor cryptographic binding check. These affect what an implementation accepts or reports, despite correct statements elsewhere in the draft.


## Prompt — verbatim

    You are a non-author falsification reviewer for the Tessera project. Working directory: /home/tony/projects/tessera (read-only; do not edit anything; write your report only to the -o output).
    
    Subject: docs/implementation-spec.md (first draft, 2026-09-13, ~2,760 lines), band-1 docket item 31: the current contract derived from the adopted artifacts, every requirement tagged with the amendment, ruling or model that justifies it; unresolved decisions in §11; contradictions routed to the author in §12, never resolved by the writer. Its assembly log is docs/reviews/2026-09-13-implementation-spec-assembly-log.md. The signed sources are docs/phase-0-prereg.md and docs/phase-0-prereg-amendment-1.md … -6.md; decisions in formal/spike/first-link/DECISION.md and formal/spike/standing-probe/; models under formal/tla/ and formal/suite/ (each family's .pv claim blocks and RESULTS.md); tracker formal/PROPERTIES.md; coverage formal/COVERAGE-MAP.md; docket docs/band-1-docket.md.
    
    Your task is adversarial. Hunt for the following, in priority order, and report only what you can cite:
    
    1. MISSTATED CONTRACT. Any requirement (R-n.m) or decision-procedure row (V1–V40 in §5.2) whose tagged source does not say what the requirement says, or says it more narrowly or more broadly. Open the cited lines. Give: ID, the spec's sentence, the source's sentence, the delta, and what an implementer would build wrongly. Concentrate on §3 (objects and formats), §4 (issuance), §5 (verification) and §6 (standing) — those are what gets built.
    
    2. SILENT RESOLUTION. Any place the spec picks one side of a conflict that the record leaves open (compare against §12's open list C-01…C-15, and against your own reading of the amendments), or presents a PROPOSED, DOCKET, or MODELLED-only item with the grammar of a registered requirement.
    
    3. OMISSION. Registered verifier or issuer obligations, fields, reason codes, verdict transitions, or invariants in the signed texts that an implementer needs and the spec does not carry. Name the source lines and the section of the spec where it belongs.
    
    4. THE PROCEDURE AGAINST THE MODELS. Take §5.2's ordered checks and the standing procedure in §6.3 and compare them with the verifier processes in formal/suite/s-p2/proverif/sp2_q2_degraded_compromised.pv, formal/suite/s-p3/proverif/sp3_q2_degraded_compromised.pv, formal/suite/s-p7/proverif/sp7_q2_degraded_compromised.pv, formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv and the P4 ladder in formal/tla/P4_VerifierStates.tla. Report any check the models perform that the spec omits, any check the spec states that no model or registered text contains, and any predicate the spec transcribes inexactly.
    
    5. OFF-HAPPY-PATH. For five inputs of your choosing (e.g. a multi-signer bundle with one non-fingerprint frame field differing; a wrapper whose recorded inner canonicalization version lies; a well-formed unsupported algorithm identifier; an anchor confirmed exactly at declared+δ; a TLR presented without lineage context), trace the verdict and standing report the spec would produce and state whether the record agrees.
    
    Do NOT report: style, length, history, or anything about the process. Do not propose resolutions to §12 items; you may say a contradiction is real or is settled by a later text you cite.
    
    Output format: a markdown report with sections 1–5 above, each finding numbered (e.g. 1.3), each with citations as file:line ranges. End with a one-paragraph verdict: is this draft a faithful statement of the current contract, and what are the three findings the author must see first. Aim for the findings that matter; a short report of real defects beats a long one of nits.
