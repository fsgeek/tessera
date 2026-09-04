# Standing decision — amendment texts (SC-1, SC-2, SC-3, D1)

**Status: ADOPTED (author, 2026-09-04) and ENTERED 2026-09-04** —
drafted by the AI collaborator 2026-08-31, revised by the AI
collaborator 2026-09-04 (see the revision note at the end), adopted
by the author's dated annotations below, and inserted at each named
target as dated amendments the same day; this file remains as the
drafting record. *(Header as originally registered: PROPOSED —
nothing entered.)* These are the four amendment texts
required by
`DECISION.md`'s status correction before the rule-3 selection
(terminal lineage record, ADOPTED 2026-08-31) is *entered*. Each item
names its target location; upon author adoption, the quoted text is
inserted there as a dated amendment and this file remains as the
drafting record. Provenance is labeled per item: the *branch choices*
were adopted by the author's dated annotations in `DECISION.md`
(commit `4f40021`); the *texts* below are proposed drafts of those
choices and carry no authority until adopted.

---

## Amendment 1 — SC-1: the G4 temporal boundary (anchor branch)

**Branch: ADOPTED** (author annotation, 2026-08-31: "agreed to anchor
the TLR"). **Text: ADOPTED (author, 2026-09-04).**

**Target A:** dated note appended to the TLR sketch,
`DECISION-CRITERIA.md` §1 (per §1's own amend-don't-rewrite clause).

> *Temporal boundary (dated amendment, 2026-08-31, per SC-1).* The
> TLR is anchored: at terminal disposition the issuer submits the
> TLR's digest to the anchoring channel, and the resulting anchor
> proof travels in the bundle beside the TLR. The verifier
> additionally evaluates the registered A2.1 predicate against the
> TLR's anchor, with the TLR's declared terminal-disposition time in
> the place of the declared issue time:
>
>     confirmed_at := timestamp(block at height h + k − 1)
>     confirmed_at ≤ declared_terminal_time + δ
>
> together with the A2.2 anchor-time lower-bound conjunct under ε,
> under the issuance policy's tolerances (verifier-owns-tolerances
> applies as in A2.1). This is not a new window: it is the same
> three-conjunct temporal test the attestation's own anchor passes,
> applied to a second anchored object. A TLR failing it yields
> `UNVERIFIABLE` / `STANDING_EVIDENCE_TEMPORAL_MISMATCH`
> (Amendment 3). Boundary
> stated in both halves: the anchor bounds **when** standing evidence
> could have been fabricated — to the [−ε, +δ] window about the
> declared terminal disposition, per A2.1/A2.2 — and does not narrow **whether** a second,
> contradictory TLR exists within that window (band-1 docket item
> 24's own line: anchoring narrows when, not whether). A holder of
> the entitled key after that window — including after the service's
> death — can no longer mint standing evidence that verifies.

**Target B:** the price sentences, entered beside Target A (these are
the cost record; adoption of the amendment adopts the costs as
stated):

> *Costs, stated plainly.* (i) Anchoring is a second anchoring event
> per issuance, at terminal disposition, after the shipped attempt's
> own anchor has confirmed; anchor-channel unavailability at that
> moment is an issuance failure mode of A2.3's class and must be
> treated by the refusal machinery, not absorbed silently.
> (ii) Where the bundle ships before chain confirmation, it carries a
> pending anchor proof; **the holder bears the upgrade duty** for
> their own proof (author, 2026-08-31: cost borne by the service's
> beneficiaries). An un-upgraded proof weakens only that holder's
> temporal bound, visibly. (iii) **δ is bounded below by
> anchor-confirmation latency**: the fabrication window is as wide as
> the anchoring channel is slow, and the service does not control
> that latency. [Raised by the collaborator 2026-08-31, unobjected;
> flagged for the author's explicit eyes at adoption.] (iv) **Complete
> standing evidence is late by construction**: it exists only after
> the shipped attempt's anchor confirms, terminal disposition is
> reached, and the TLR's own anchor confirms — two anchor-confirmation
> latencies in sequence, each bounded by δ, plus the lifecycle wait
> S on the refusal path. A holder asking for standing evidence
> before that point receives a pending proof (ii), not a verifiable
> one. [Added by the collaborator 2026-09-04; a consequence of (i)
> and A2.1's lifecycle, stated so the cost is visible.]

**Target C:** dated note appended to the transparency-witness sketch,
`DECISION-CRITERIA.md` §1 — sub-ruling 1 requires one sentence per
*surviving* candidate, and the witness survived:

> *Temporal boundary (dated amendment, 2026-08-31, per SC-1).* The
> signed log head bounds an entry's creation time only if the head is
> itself anchored or preserved; otherwise the head's date is
> testimony. Recorded for completeness; the witness was not selected,
> and this sentence governs only its optional never-load-bearing
> enrichment role.

---

## Amendment 2 — SC-2: the one-signing-act commitment

**Commitment: ADOPTED** (author annotation, 2026-08-31). **Text:
ADOPTED (author, 2026-09-04).**

**Target:** registered statement in `DECISION.md`, beside the R2
scoring line; cross-referenced from the A3.7.2 refusal-record
specification when that is next touched.

> *Specification commitment (dated, 2026-08-31, per SC-2).* One
> signing act at terminal disposition produces the **disposition
> fact** — (attempt identity, terminal disposition) — and both
> disposition-bearing records are projections of that one signed
> fact: the terminal lineage record adds the attempt lineage; the
> portable refusal record (A3.7.2) adds the disclosable reasons and
> the public commitment value. Whether the projections are one object
> or two remains unpreferred, per R2 as registered. Honest
> disagreement between the records is thereby structurally
> impossible; dishonest contradiction is equivocation and remains
> governed by G4's boundary, per the author's registration-day
> ruling on R2's wording.

---

## Amendment 3 — SC-3: the S-series and outcome amendments

**Amendment: ADOPTED** (author annotation, 2026-08-31: "agreed to
dated amendment to the registered S1-S3 table"). **Rows and codes:
ADOPTED (author, 2026-09-04).**

**Target:** dated amendment to `formal/spike/first-link/DECISION.md`
§"Standing test conditions (registered exit condition 3)".

> *Dated amendment, 2026-08-31 (standing decision, SC-3).* The
> registered table gains a fourth condition:
>
> | # | Form | Presented with lineage? | Standing verdict | Required reason code |
> |---|------|--------------------------|------------------|----------------------|
> | S4 | Lineage-present, lineage's terminal disposition is `REFUSED` | yes | **no standing** | `ISSUANCE_REFUSED` |
>
> (A refused-lineage attempt presented *alone* remains S3: absent
> evidence is absent evidence.) The discriminating requirement
> extends: S2, S3, and S4 all return "no standing" and MUST return
> pairwise distinct reason codes; the negative-control obligation
> extends to a companion collapsing any pair.
>
> Two defined outcomes are added to the standing report's vocabulary,
> in the first-link verifier-boundary spirit (no inference, fallback,
> or normalization):
>
> - **`STANDING_EVIDENCE_MALFORMED`** — internally inconsistent
>   standing evidence (e.g., a terminal disposition contradicting the
>   lineage's own entry for that attempt, probe finding F1) yields
>   `UNVERIFIABLE` with this reason; it never yields `ESTABLISHED`.
>   The S-series test vectors MUST include the F1 shape, and a broken
>   companion that accepts it MUST fail.
> - **`STANDING_EVIDENCE_TEMPORAL_MISMATCH`** — the TLR's anchor
>   failing the A2.1 predicate against its declared
>   terminal-disposition time (Amendment 1) yields `UNVERIFIABLE`
>   with this reason.

---

## Amendment 4 — D1: the row-2 registration, scheduled

**Registration: ADOPTED** (author annotation, 2026-08-31:
"forward-link/generation-chain construction registration is included,
specific approach … subject to specification or substitution … so
long as it addresses the key-compromise threat model … this doesn't
prevent key compromise, it makes it legible as any fork leads back to
the point of compromise"). **Schedule and relation text: ADOPTED; location RULED (author, 2026-09-04).**

**Target:** dated note in `DECISION.md` at the D1 sub-ruling; band-1
docket entry updated to carry the schedule.

> *Row-2 registration, scheduled (dated, 2026-08-31, per D1).* The
> forward-link / successor-slot construction
> (`docs/exploration-2026-07-19-service-layer-elicitation.md`,
> "predeclared successor slot") WILL be registered; the mechanism is
> not frozen and may be substituted, subject to the author's
> criterion: it must make key compromise legible — any fork leads
> back to the point of compromise. Relation to the selected
> mechanism, stated: the TLR chains **attempts within one issuance,
> backward**; the successor slot chains **issuances across the
> service's life, forward**. The split-brain visibility the author's
> C4 paragraphs describe belongs to row 2 and is not supplied by the
> TLR. Scheduling anchor: **[FORK — author ruling
> required, 2026-09-04]** the schedule depends on where the slot
> rides, which the 07-19 note leaves at "inside the current signed
> bytes" without pinning frame or payload.
>
> **(a) Slot inside the canonical payload, under P3's obligations**
> — the location A3 §1 pinned for the algorithm identifier, chosen
> there precisely because it leaves P8's four-field frame unchanged.
> Schedule: registration — including the 07-19 note's
> four-mechanism × four-trace comparison — completes **before format
> freeze**, the record's named irreversible moment; P8's golden
> vectors gain a slot-bearing vector at registration, without
> reopening the framing proof. Not gated on, and does not gate, the
> S-STANDING model.
>
> **(b) Slot as a frame field.** Then the slot is inside P8's scope
> and registration must complete **before P8's encoding is fixed**,
> which A3 §1 places before Band 0 exit; a later registration would
> reopen P8.
>
> Collaborator recommendation: **(a)**, by precedent and because (b)
> narrows Band 0 exit to serve a schedule. The 2026-08-31 draft
> stated the (a) schedule without the location ruling that makes it
> sound; that omission is the defect this revision repairs. [Author
> review 2026-09-04: concur with proposal to adopt (a).]

---

## Carry note (drafter, not an amendment)

From the blind re-scoring's conformance note
(`docs/reviews/2026-08-31-blind-standing-scoring.md`): the probe
fixture establishes the entitled-key link only via the envelope path;
a faithful implementation and the S-STANDING model MUST check the
entitled-key binding **inside** the standing path, so a bundle whose
envelope fails `KEY_FINGERPRINT_MISMATCH` cannot receive a standing
report computed against an unentitled key. Suite obligation; travels
with the S-STANDING slot in `formal/suite/ENUMERATION.md`.

---

## Revision note (collaborator, 2026-09-04, Adopted 2026-09-04)

Read cold on 2026-09-04 against the registered amendments before
adoption. Three changes, none altering an adopted branch:

1. **SC-1 (Target A) and SC-3 (temporal outcome):** "within δ" replaced
   by an explicit citation of the A2.1 predicate (`confirmed_at` at
   depth k, one-sided against the declared time, ε on the lower bound
   per A2.2). The bare phrase was the exact ambiguity Amendment 2 was
   written to close; re-introducing it in a new amendment would have
   let a conformant verifier pick a symmetric window or the block-h
   timestamp. Wording repair, not a branch change.
2. **SC-1 (Target B):** price (iv) added — complete standing evidence
   is two anchor latencies late by construction. A consequence of (i)
   and A2.1's lifecycle, previously unstated.
3. **D1:** the scheduling anchor is now a flagged fork on the slot's
   location (payload vs frame), because "before format freeze" is
   sound only under the payload location, and the location is an
   author ruling by the A3 §1 precedent. Recommendation recorded.

Provenance of the 2026-08-31 draft's two self-flagged passages is
unchanged: the δ-floor sentence (iii) and the D1 schedule were the
collaborator's reasoning then; the D1 schedule is now routed rather
than proposed.

[Author reviewed 2026-09-04: Concur with the three clarifications
and one amendment as stated in this document.]
