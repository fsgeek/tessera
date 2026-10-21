# The 30 Oct V1 exit: item by item

> **Status: OWNER WORKING NOTE, 2026-10-19** (Claude Opus 5.5, owner instance). Read-only survey. It changes no
> registered sentence. If it disagrees with A9 or A10, they win. Every effort figure is **my estimate**, not a
> measurement. Every state was checked against the file named, not against another tracker.

**Sources.**
- The gate: `docs/phase-0-prereg-amendment-9.md` §A9.2, lines 193–225 ("A9" below). Signed at `2ad3489`.
- Its amendment: `docs/phase-0-prereg-amendment-10.md` ("A10"), signed at `9ade764`. Only one A10.7 row touches
  A9.2: **row 33** (A10:769), which changes the cut order (A9:211-213). Rows 34–36 move the release-custody gate
  to the first public verifier release, but they keep two things on 30 Oct: the release format and the custody
  procedure's required contents (A10:637-641). Those are freeze items, not A9.2 items. They are listed in §3.
- Property tracker: `formal/PROPERTIES.md`. `formal/BAND0-EXIT.md` (2026-09-13) predates A9 and is not used for
  states here.

**The instrument rule** (A9:198-200): instrument code "lives under `prototype/` or `formal/spike*/` … An
instrument's outputs … never stand as evidence for a C-row, and nothing an instrument produces discharges an
obligation." So the e2e run (`prototype/e2e/`, `receipts/real-1`, `FINDINGS.md`) and the conformance suite
(`prototype/conformance/`) can only **inform** an item below. `formal/p8/vectors/` is not under `prototype/` or
`formal/spike*/`, so it is not instrument code. The conformance cases (RES §L) become part of the frozen vectors
object at the freeze (`docs/V1-PROFILE.md:1567-1568`). After that they are spec parts, not instrument output.

## 1. Summary

| # | Item (A9:205-210) | State | Remaining (my estimate) |
|---|---|---|---|
| 1 | P1 `checked` | DONE | 0 |
| 2 | P2 `checked` | DONE | 0 |
| 3 | P3 [model] `checked` | DONE | 0 |
| 4 | P4 `checked` | DONE | 0 |
| 5 | P5 `checked` | DONE | 0 |
| 6 | P5c `checked` | DONE | 0 |
| 7 | P10 `checked` | DONE | 0 |
| 8 | P7 type-separation half `checked` | DONE | 0 |
| 9 | P8 prose proof plus golden and rejection vectors for `A_sig`, with a time-boxed falsification attempt | PARTIAL | 3–3.5 d |
| 10 | P9 as a contract inspection | NOT BEGUN | 0.75 d |
| 11 | E6a with companions | NOT BEGUN | 1.5–2 d |
| 12 | The 129 strict correct-form rows | DONE | 0 |
| 13 | Statements M2 and M5 | DONE | 0.25 d (M5 gains the A10 classifier) |
| 14 | E18 with its time-boxed sign-off | PARTIAL | 0.5 d |
| 15 | The one-page E8/E7/E11 sheet | NOT BEGUN | 1.5 d |
| 16 | The E12 page | PARTIAL | 0.75 d |
| 17 | Anchored-versus-unanchored-signature negative control | DONE | 0 |
| 18 | `ISSUANCE_WINDOW` and `DNS_WINDOW_LENGTH` vectors | DONE | 0 |
| 19 | Root-KSK rollover control | PARTIAL | 0 extra (it enters at the freeze assembly, §3) |
| 20 | Signer branch recorded | DONE | 0.1 d (stale profile lines) |
| — | E9 packet and the author's read (A9:222) | NOT BEGUN | 1 d owner, under 1 h author |

**Counts: 13 DONE, 4 PARTIAL, 3 NOT BEGUN** (20 items; the E9 read is counted in §4, not here).
**A9.2 items remaining: about 9–11 agent-days**, and most of it can run in parallel. The freeze work in §3 is
larger, about 8–9 agent-days, and it decides the date.

## 2. Each item

### 1–8. P1, P2, P3 [model], P4, P5, P5c, P10, P7 type-separation half

- **Means.** Each property's model passes its tool, with its broken companions red as registered.
- **State: DONE (`checked`).** `formal/PROPERTIES.md:35` (P1), `:36` (P2), `:37` (P3, "[model] half; [assumption]
  half open"), `:38` (P4), `:39` (P5), `:40` (P5c), `:45` (P10), `:42` (P7). Files exist: `formal/suite/s-p1/`,
  `s-p2/`, `s-p3/`, `s-p7/RESULTS.md`; `formal/tla/P4_VerifierStates.out`, `P5c_IssuanceProtocol.out` and
  `P5P6_TemporalRevocation.out` each end "Model checking completed. No error has been found." (checked today);
  `formal/spike/first-link/` for P10.
- **P7.** A9.7 row 26 (A9:490): "The wrapper half and its H1a vector move to Wrapping and renewal (A9.3); P7's
  type-separation half stays on the 30 Oct gate". S-P7 Q1/Q2 and Q7 are the checked part (`PROPERTIES.md:42`).
- **Remaining.** None for "checked". The author accepts or rejects each row in E9 (§4).
- **Note for E9.** `prototype/e2e/FINDINGS.md` E-02 says "P5c models issuance as sign-then-stamp, with no state for
  a signature that is made but never shipped." Under the closure rule (A9:219-222) this gates V1 only if it is a
  counterexample to C1–C7. The owner's reading (CLARIFY, `docs/V1-CONTRACT.md` §3) is that it is not. Put it in
  the P5c row so the author sees it.
- **Author act.** None beyond E9.
- **Instrument material.** The differential run (342/342 AGREE, `prototype/differential/results-run5.json`) and
  mutation testing (`prototype/mutation/REPORT.md`) could inform; they discharge nothing.

### 9. P8: prose proof plus golden and rejection vectors for `A_sig`, time-boxed falsification

- **Means.** A written proof that the V1 encoding (both frames and the `A_sig` anchor preimage) is unambiguous,
  backed by vectors, and an adversary tried to break it within a fixed time and failed.
- **State: PARTIAL.**
  - Proof: `formal/p8/PROOF.md` (531 lines). Its header still reads "STATUS: DRAFT … It is waiting for its
    time-boxed falsification pass" (`PROOF.md:3-6`).
  - Vectors: `formal/p8/vectors/golden.json`, `reject.json`, and the hybrid pair. `A_sig` is covered by A-01, A-02,
    SIG-01, SIG-02, XA-01 to XA-32 and XR-06 to XR-15 (`PROOF.md:438-445`).
  - Run today: `check.py` gives "golden 71/71 round-trip; rejection 173/173 … negative controls 5/5" and, for the
    hybrid, "golden 35/35; rejection 63/63 … negative controls 1/1".
  - Falsification attempt: **not run.** I found no review of P8 itself. The 2026-10-12 anchor review
    (`docs/reviews/anchor-signatures/CODEX-REVIEW.md` finding 10) reviewed the anchor design, not the proof.
- **Remaining.**
  1. ENCODING-V1 and PROOF wording edits, profile §14.2 item 9 (`docs/V1-PROFILE.md:1201-1207`): 0.5 d. Do these
     first, so the falsification attacks the text that will be frozen.
  2. The falsification attempt (Codex, non-author), time-boxed: 2 d.
  3. One repair day if it finds a counterexample: 0–1 d.
  4. A plain-language statement of P8 for the E9 packet: 0.25 d.
- **Author act.** None in A9.2 beyond E9. ("P8 by prose proof … surviving a time-boxed falsification attempt",
  A9:206-207, names no author step.)
- **Instrument material, could inform.** Mutation testing (253,363 mutants, 0 false accepts,
  `prototype/mutation/REPORT.md`); hybrid fuzz (90,400 cases, `formal/p8/HYBRID-REGISTRATION-RECORD.md` item 5);
  e2e E-03 hand controls (seven `a_sig` flips all INVALID, `prototype/e2e/FINDINGS.md`). These are good seeds for
  the falsifier. They are not the falsification.

### 10. P9 as a contract inspection

- **Means.** A written check that the verifier's declared inputs are only the bundle, the published verifier and
  its trust configuration, so the verdict cannot depend on anything Tessera runs.
- **State: NOT BEGUN.** `formal/PROPERTIES.md:44` is `open`: "inputs enumerated … two-machine vector owed (H1a)".
  No inspection file exists. The probe input list is in `formal/spike/tla-probes/P9/RESULTS-PROBE.md` (Q6 at :102).
- **Remaining.** One page that walks the profile's declared inputs (`docs/V1-PROFILE.md` §2.2 "What the bundle
  never supplies", §5 trust configuration, §9 dependency manifest, §3.5 CLI) against C6 (A9:145): 0.5 d. A short
  Codex check: 0.25 d. The code inspection is after exit (A9:214).
- **Author act.** None beyond E9.
- **Instrument material, could inform.** `prototype/indep-verifier/` runs offline; the e2e verdict came from a
  TEST-provisioned release with no network (`FINDINGS.md` E-03). That is code, so it belongs to the 20 Nov code
  inspection, not to the contract inspection.

### 11. E6a with companions

- **Means.** The P4 model gains the transition "a well-formed but unsupported algorithm id gives `UNVERIFIABLE`",
  and a broken companion that fails open past it must go red (A3 §A3.6.2 item 3).
- **State: NOT BEGUN.** The tracker row "A3.6.2 Unknown-algorithm verdict transition" is `open`, "—"
  (`formal/PROPERTIES.md:47`). No TLA+ file in `formal/tla/` mentions an unknown algorithm or out-of-profile
  input (grep, today).
- **Remaining.** P4 transition plus the fail-open companion, and the companions the derivation names: a mixed
  failed/unperformable case and missing-signature versus missing-evidence (`docs/V1-DERIVATION-DRAFT.md:114`):
  1–1.5 d. Codex falsification pass, time-boxed: 0.5 d.
- **Author act.** None beyond E9.
- **Instrument material, could inform.** Conformance cases with the expected verdicts: 12 `ALG_UNKNOWN` (ALG-01,
  HY-*), 11 `OUT_OF_PROFILE` (L-01 to L-04 …), 5 `MEMBER_MISSING` (L-09, L-10 …), all AGREE in run 5. They show
  what the model's red and green cases should be.

### 12. The 129 strict correct-form rows

- **Means.** In the capstone, every registered query for strict cases (a), (b) and (c) came out as registered.
- **State: DONE.** `formal/suite/capstone/RESULTS.md` §1 (lines 165–357): 47 rows (a), 47 (b), 35 (c), all "as
  registered" (counted today), and `RESULTS.md:9`: "Every strict file — cases (a), (b) and (c) — landed."
- **Remaining.** None. The capstone's three routed questions were deferred by the author on 2026-10-07
  (`READ-CAPSTONE-2026-10-06.md:6-11`). They concern the degraded wave and companions, not these rows. The
  derivation states that V1 cites none of the ten divergent companions or the withheld C-C15(i) C-Q6 results
  (`docs/V1-DERIVATION-DRAFT.md:93`).
- **Author act.** None beyond E9.
- **Instrument material.** Not needed.

### 13. Statements M2 and M5

- **Means.** M2: the authority evidence is for the issuer's own domain on both channels. M5: every field of the
  manifest tuple is fixed by an authenticated source.
- **State: DONE.** Text at `docs/V1-PROFILE.md:727-731` (M2) and `:741-750` (M5), both "[OWNER 2026-10-14]".
  M2 already uses the A10.6 owner name `_tessera-v1.<D>`.
- **Remaining.** A10 row 27 (A10:763) adds the service-key classifier, and the memo places it after M5 (memo item 4). Add one
  cross-reference when the listing lands: 0.25 d, counted in §3.
- **Author act.** None beyond E9.
- **Instrument material, could inform.** Cases b and d3 fixtures (`V1-PROFILE.md` §11) and `DNS_KEY_MISMATCH`
  cases.

### 14. E18 with its time-boxed sign-off

- **Means.** The issuance and bridge models are re-run at the registered k = 6, and a non-author reviewer signs
  off within a fixed time.
- **State: PARTIAL.** Runs done: `formal/tla/k6-2026-09-14/RESULTS-K6.md` §4. Sign-off not done: "Codex confirmed
  … and stated it is not an E18 sign-off … a full pass is owed" (`RESULTS-K6.md:151-157`;
  `docs/reviews/2026-09-14-codex-review-ledger-and-k6.md:18, :54`).
- **Remaining.** A full Codex pass on `formal/tla/k6-2026-09-14/`, time-boxed: 0.5 d.
- **Author act.** None in A9.2 beyond E9. (A7.8 asks for "a non-author model" review; it names no author step.)
- **Instrument material, could inform.** e2e E-03: h_git = 972177, h_receipt = 972187, k = 6 met on mainnet once.

### 15. The one-page E8/E7/E11 sheet

- **Means.** One page that names each join between the TLA+ and ProVerif models (E8), confirms each V1 query has a
  sentence naming its property (E7), and indexes the plain-language statements (E11), stating the composition
  that is not proved.
- **State: NOT BEGUN.** No such file in `docs/` or `formal/` (grep, today). Inputs exist: `formal/COVERAGE-MAP.md`,
  `formal/suite/ENUMERATION.md` §4, `formal/suite/s-p3/READING-AIDS.md`, `formal/tla/READING-AID-P4.md`,
  `-P5P6.md`, `-P5c.md`.
- **Remaining.** Draft: 1 d. Codex check: 0.5 d.
- **Author act.** None beyond E9.
- **Instrument material.** Not applicable.

### 16. The E12 page

- **Means.** One page for a person holding a receipt and a verdict: the decisions they may and may not make. It
  opens with the can/does-not-establish list "recorded verbatim in the 2026-07-28 ruling doc"
  (`docs/phase-0-prereg-amendment-3.md:89-95`).
- **State: PARTIAL.** Material exists but not the page:
  - `docs/V1-CONTRACT.md` §2–§3 (guarantees G1–G11 and "Not guaranteed"), owner draft, Codex-reviewed 2026-10-19;
  - the scenario mapping, `docs/V1-PROFILE.md` §11;
  - `docs/implementation-spec.md` §1.5 (pre-A9 draft).
- **Remaining.** Write the V1 page: open with the verbatim list, then the A9.1 rows in relying-party terms, with
  the A10 narrowings (chain time, not UTC; window as two comparisons). Use the plain style
  (`docs/plain/STE-STYLE.md`): 0.5 d. Codex check: 0.25 d. The acceptance test is 4 Dec, not 30 Oct.
- **Author act.** None beyond E9.
- **Instrument material, could inform.** e2e E-03's negative controls are good worked examples for the page.

### 17. Anchored-versus-unanchored-signature negative control

- **Means.** A valid signature over the right frame that is not the one committed in `A_sig` must fail.
- **State: DONE.** `formal/p8/PROOF.md:444` ("XR-10 to XR-14: a valid signature that is not the committed one
  fails the anchor check"); `check.py` "negative controls 5/5" and hybrid "1/1" (run today). GnuPG reported "Good
  signature" for all five (`PROOF.md:471-475`).
- **Remaining.** None.
- **Instrument material, could inform.** L-88 `RECEIPT_ANCHOR_MISMATCH`; e2e E-02's real orphan ML-DSA signature
  is a natural real-world instance of this control.

### 18. `ISSUANCE_WINDOW` and `DNS_WINDOW_LENGTH` vectors

- **Means.** Vectors at the window edges, and for a key-publication record whose window exceeds 90 days.
- **State: DONE.** `formal/p8/PROOF.md:449`: W-01, W-02, XW-01 to XW-03 (`ISSUANCE_WINDOW`); XD-32, XD-33
  (`DNS_WINDOW_LENGTH`); DNS-02 (exactly 90 days). All pass `check.py` (run today).
- **Remaining.** None. They are frozen with the vectors object (§3).
- **Instrument material, could inform.** Conformance W-02, L-34, AGG-f (`ISSUANCE_WINDOW`) and DNS-wlen.

### 19. Root-KSK rollover control

- **Means.** A DNSSEC snapshot taken while one trusted root KSK is published but not signing must pass (A9:341-342).
- **State: PARTIAL.** The case exists only under `prototype/`: L-60 "Rollover control: KSK-A published but not
  signing → `VALID_STRICT / OK`" (`prototype/conformance/REPORT.md:516`), AGREE in run 5. As instrument output it
  does not count yet. It counts once the RES §L cases enter the frozen vectors object (`V1-PROFILE.md:1567-1568`).
- **Remaining.** No separate work: it lands with the freeze assembly (§3).
- **Instrument material, could inform.** `prototype/spike/SPIKE-REPORT.md:78-81` (the real KSK-2024 re-capture);
  e2e real-1 validated under the real KSK-2024 on 2026-10-19 (`FINDINGS.md` E-03).

### 20. Signer branch recorded

- **Means.** The owner records, dated, which signer branch was taken, in ENCODING-V1 §5.2 and in the profile.
- **State: DONE.** `formal/p8/HYBRID-REGISTRATION-RECORD.md:1-5` ("REGISTERED 2026-10-16 … Branch taken:
  HYBRID"); `formal/p8/ENCODING-V1.md:485`; `docs/V1-PROFILE.md:900-902`.
- **Remaining.** Stale text: `docs/V1-PROFILE.md:146-148` still says "`OPEN (other):` not yet taken", and §14.2
  item 4 (`:1165`) still lists the branch as open. 0.1 d.
- **Author act.** None ("needs no further amendment and no further author approval", A9.6).

## 3. Freeze work that shares the 30 Oct date (not A9.2 items)

These are not in A9.2's list, but the frozen spec and vectors objects carry items 9, 18 and 19, and A10 puts
these on 30 Oct. Estimates are mine, from `docs/decisions/2026-10-17-utc-bound-and-capture-visibility.md:350-355`
and `docs/V1-E2E-GAP.md`.

| Work | Source | State | Estimate |
|---|---|---|---|
| Service-key listing (A10.4.1) in profile, both verifiers, vectors | A10 rows 25–31, 37–39 | NOT BEGUN: `service_keys` and `utc_assessment` appear 0 times in `V1-PROFILE.md` and in no verifier code | 3.5–4 d |
| `utc_assessment` (A10.1.1) | A10 rows 20–22 | NOT BEGUN | 0.75 d |
| Release format frozen | A10:639-641 | OPEN (`V1-PROFILE.md` §14.2 item 2) | 1 d |
| Trust-configuration values, KSK sources, KSK-2017 start | §14.2 item 3 | OPEN | 1 d |
| Freeze assembly, spec/vectors/catalog hashes, locator refresh | §14.2 items 7–8, 15 | OPEN; `prototype/e2e/freeze.py` is a TEST assembler that could inform | 1.5–2 d |

**Freeze total: about 8–9 agent-days.**

## 4. The author's read (E9)

**The registered text.** A9:222: "The author's E9 read is accept or reject per row." This is the only author act
A9.2 names for the exit. Two more are nearby but not in the exit list:
- A9:201: "The author commits `prototype/spike*`." Already done: 42 tracked files under `prototype/spike` and
  `prototype/spike-pq`, none modified (`git ls-files`, `git status`, today).
- A9:218: the exit "opens Phase 1a for V1-profile code only, still by an explicit, dated, signed opening commit".
  The text says "signed", not who signs; in the house form it is the author's commit. About 10 minutes.

**Size if done naively.** The unread falsification reviews alone are about 1,900 lines
(`docs/reviews/2026-09-06-codex-tla-falsification-p4-p5p6-p5c.md` 582,
`…-codex-suite-falsification-s-p1-s-p2-s-p7-s-standing.md` 934, `2026-09-12-…-amendment-5-checks.md` 311,
`2026-09-14-…-k6.md` 54). Add `PROOF.md` (531) and the new reviews for P8, E6a, E18 and the E8 sheet. That is
several sittings.

**Proposal: one packet, about 20 rows, under 45 minutes.**
1. One file, `docs/READ-E9-V1.md`, built like `formal/suite/READ-C5-2026-09-12.md`. One row per exit item 1–20.
   Each row has: the claim in two or three plain sentences; one evidence pointer; the findings that **gate** under
   the closure rule (A9:219-221), each quoted; a count of the non-gating findings, already filed to the A9.3
   register by the owner; and an ACCEPT / REJECT box.
2. The closure rule does the filtering. A finding gates only if it is "a concrete counterexample to C1–C7" or shows
   a C-row "lacks the evidence assigned to it". The owner sorts every surviving finding before the packet. The
   author reads only the gating ones. I expect few or none.
3. Rows he already read are marked so: the C5 claim-block reads of 2026-09-12 (P1, P2, S-STANDING, P7) and the
   S-P3 read of 2026-09-05. Those rows ask only "anything since?".
4. Evidence-only rows (12, 17, 18, 19, 20) are one line each: the count and the file.
5. Size target: about 2,000–2,500 words, about 5 pages. About 30–45 minutes, including the P8 plain-language
   statement and the E12 page, which are already one page each.
6. The request names the file, the rows, the question ("accept or reject per row") and the length, as the
   standing rule asks.

## 5. Total, critical path, and the cut order

**Total remaining (my estimates).** A9.2 items: about 9–11 agent-days. Freeze work (§3): about 8–9 agent-days.
E9 packet: 1 d. Author: under 1 hour for E9, plus about 10 minutes for the opening commit. There are 10 working
days from Mon 19 Oct to Fri 30 Oct (11 calendar days to the gate). Three parallel tracks fit. One track does not.

**Critical path.** The A10 listing work is the longest chain, because the spec hash and vectors depend on it and
the freeze depends on both.

| Dates | Track A, freeze (critical) | Track B, P8 | Track C, models and pages |
|---|---|---|---|
| 19–20 Oct | Listing and `utc_assessment` in the profile | ENC/PROOF edits (14.2 item 9); start the falsification | E6a model and companions |
| 21–22 Oct | Listing in both verifiers; vectors | Falsification (time-box ends 22 Oct) | E6a Codex pass; E18 Codex pass; P9 inspection |
| 23 Oct | Release format; trust values | Repair day, if needed | E8/E7/E11 sheet |
| 26 Oct | Freeze assembly; locator refresh | P8 plain statement | E12 page; Codex checks on sheet and page |
| 27 Oct | Independent byte-agreement check | — | **E9 packet** (needs every row) |
| 28 Oct | — | — | **Author's E9 read** (under 1 h) |
| 29–30 Oct | Freeze record; one day of slack | — | Signed opening commit |

The path: listing in profile (19–20) → verifiers and vectors (21–22) → release format and trust values (23) →
freeze assembly (26–27) → E9 packet (27) → author read (28) → freeze record and opening commit (29–30). Slack:
about one working day. A P8 counterexample that needs more than one repair day also lands on the path.

**The cut order, as registered.** A9:211-213: "If the 30 Oct exit slips, the first item cut is the PQ hybrid (the
registered fallback is then taken), and nothing else is on the list: the signature-inclusive anchor `A_sig`, the
root-KSK rule and the git stamp target (D-16) are required."

As amended by A10 row 33 (A10:769), "and nothing else is on the list" becomes: "the second item cut is the
service-key listing (A10.4.1). If it is cut while A9.5's independent release boundary is established, A10.4
option (a) applies and the absence of new-key protection is stated. Cutting it does not cure a failure of
release-key independence (A10.4.2). The rest stays required."

**What the cuts buy now (my reading).** The hybrid is already registered and its evidence is complete
(`HYBRID-REGISTRATION-RECORD.md`). Cutting it now saves almost nothing. The listing is the real lever: cutting it
removes about 3.5–4 days from track A and roughly halves the critical path. If 30 Oct slips by more than a week,
the slip rule (`docs/V1-SCHEDULE.md:30-31`) brings the author one choice: cut scope or stop.

---

## Status at end of 2026-10-19 (owner)

| Item | Now | Evidence |
|---|---|---|
| P8 time-boxed falsification | **Survived with gaps; all 7 repaired** (NARROW-CLAIM of Lemma 9; no codec rule, code or vector changed) | `docs/reviews/p8-falsification/`, `prototype/p8-falsify/REPORT.md` |
| E18 sign-off | **SIGN-OFF: YES** (A7.8 option (a)); E18-02 open, non-blocking | `docs/reviews/e18-signoff/` |
| E6a with companions | **Checked** (495 TLC runs; 7 companions red as predicted); review survived, mapping corrected | `formal/tla/E6a/`, `docs/reviews/e6a/` |
| P9 contract inspection | Drafted and Codex-reviewed; findings applied | `formal/P9-CONTRACT-INSPECTION.md`, `docs/reviews/exit-pages/` |
| E8/E7/E11 sheet | Drafted and Codex-reviewed; findings applied. The capstone statement in E11 is interim | `formal/E8-E7-E11-SHEET.md` |
| E12 page | Drafted and Codex-reviewed; findings applied | `docs/V1-RELYING-PARTY.md` |
| A10.4.1 listing | **Cut** under A10 row 33 | `docs/decisions/2026-10-19-listing-cut.md` |
| A10.1.1 `utc_assessment` | Built: profile §7.4, verifier, UTC-01..10; differential 352/352 | `prototype/differential/results-run6.json` |
| Levadura contradictions | 17 disposed (9 fixed, 2 already fixed, 6 reconciled) | `docs/reviews/levadura-contradictions/` |

**Still open for 30 Oct:** root-KSK rollover control into the frozen vectors object; release format; trust-configuration
values (KSK sources, KSK-2017 start date); Δ and m into the catalog (profile §13 note 15); freeze assembly; the E9
packet for the author's one read (about 30–45 minutes, planned 28 Oct); the freeze record and the signed opening commit.
