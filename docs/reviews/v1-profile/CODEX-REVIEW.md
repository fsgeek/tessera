# Codex review — V1 profile and steps 11–12

Date: 2026-10-13. Scope: uncommitted owner-session work named in CODEX-BRIEF.md. Only this review file was deliberately edited. A9 is the governing proposed instrument; nothing here treats its adoption, P8 discharge, or instrument outputs as established V1 evidence.

Read V1-PROFILE.md in full, A9, ENCODING-V1, the derivation draft, the gitchannel diff and tests, and the spike verifier, trust configuration, selftest and report. Severity: HIGH = concrete contradiction of a required check or material authority/time-policy defect; MEDIUM = verdict or integration gap; LOW = provenance/documentation defect. No demonstrated overall false accept was found in the new path helper or default spike run. There are reproducible false rejects and typed-verdict gaps. The spike is explicitly an instrument, not the eventual verifier.

## Findings

### F1 — HIGH: failed KSK alternatives poison the existential root check

Location: `prototype/spike/verify_offline.py:119–127`, `Ledger.status:37–42`. Governing rule: A9:285–289, profile §5.

Each failed candidate writes a required `DNSSEC.root.dnskey_rrset: FAIL`. A later candidate can validate and write PASS, but FAIL dominates the group permanently. Thus the root rule is not existential: trust-list order can change the verdict.

Reproduced without editing fixtures: load `out/dns-snapshot.json`; copy its root DNSKEY RRSIG with `key_tag=38696` (the unchanged cryptographic signature is invalid for that key); add it to the root RRSIG set; put KSK-2024 first in a copied trust configuration and move its signing start to 1 October so both candidates are eligible. Evaluate at the capture time. The rows are KSK-2024 FAIL followed by KSK-2017 PASS; the group is FAIL. The original authentic KSK-2017 signature remains intact. This is an avoidable false reject of an otherwise valid root RRset, and contradicts A9.5. A 2106 verifier would reproduce it with the same inputs.

**Proposed fix:** keep candidate failures as informational diagnostics; emit exactly one required root-validation result after trying all eligible keys. PASS if any succeeds. Only classify the collective failure after none succeeds. Add a bad-first/good-second control and reverse the trust-list order; both must pass.

### F2 — HIGH: the KSK-2017 cutoff conflates cessation of signing with expiry of authentic signed evidence

Location: profile:202–208; `spike/trust-config.json`, KSK-2017 signing end; verifier:100–116.

The owner's exact cutoff is an additional acceptance policy, not a fact established by the observed change of signer. IANA confirms the rollover date and cessation of KSK-2017 signing on 11 October, but does not establish an end-of-day cutoff for validation of archived signatures. See [IANA rollover information](https://www.iana.org/dnssec/files) and [IANA rollover announcement](https://www.iana.org/news/2026/root-zone-begins-using-new-ksk-2026). The report's new capture was actually taken on 12 October; the RRSIG inception is not proof of the exact instant every cache stopped returning old signed sets.

An authentic root DNSKEY set signed by KSK-2017 before rollover remains cryptographically valid through its RRSIG expiry. An honest cached root set or snapshot captured before retirement can be OTS-anchored after the proposed cutoff. Snapshot anchoring is asynchronous; DD:94 allows up to δ, subject to all actual RRSIG windows. A fresh lower chain can coexist with that cached root set. Saying honest snapshots after 11 October never carry KSK-2017 signatures excludes this ordinary case without evidence.

Reproduced at root-check level: the archived `out/` root set evaluated at `2026-10-12T00:00:00Z` gets `KSK_OUTSIDE_SIGNING_PERIOD`. Changing only the copied KSK-2017 end to `2026-10-22T00:00:00Z` makes that root check PASS. The original fixture's leaf signatures have already expired then, so this is deliberately a root counterexample, not a claim that the entire original snapshot passes on 12 October.

A9 requires a signing-period policy at snapshot anchor time, so the code follows its abstract predicate once this cutoff is supplied; A9 does not supply this concrete cutoff. P8 does not decide it. The defect is the policy's justification and its unnecessary rejection of authentic rollover evidence. Extending a cutoff also extends a compromise opportunity; neither choice can establish historical key safety, which A9 explicitly leaves unevaluated.

**Proposed fix:** distinguish operational signing dates from the interval during which historical RRSIGs may support snapshot validation. Record an explicit, sourced validation policy and the cache/anchor-delay tradeoff. If A9's predicate needs adjustment to admit pre-retirement evidence anchored later, amend it visibly before freezing; do not silently infer that change from P8. Add an honest old-root/new-leaf rollover fixture with an anchor after retirement but before all relevant expiries. If the strict cutoff is retained, disclose this additional false-reject class rather than asserting it cannot occur.

### F3 — MEDIUM: “signed outside period” is inferred from an unauthenticated key tag

Location: verifier:104–117; profile:209–213.

The requested owner decision says **only valid signature** from a trusted KSK outside its period. The implementation never verifies those outside-period signatures: matching public-key digest plus any RRSIG carrying the tag populates `outside`. An attacker can append an invalid RRSIG bearing a retired trusted tag to an otherwise unknown-key set and turn UNVERIFIABLE into INVALID. A key tag is a selector, not proof of authorship. The code also fails to examine a valid outside-period candidate when an in-period candidate exists but fails cryptographically, so its diagnostic split does not implement the stated cases consistently.

There is no false accept here, but the specific reason asserts evidence the verifier did not establish. Generic malformed/invalid trusted signatures may appropriately be INVALID for a different reason; that does not justify `KSK_OUTSIDE_SIGNING_PERIOD`.

**Proposed fix:** establish cryptographic validity and RRSIG temporal validity separately from the configured KSK period. Emit the period reason only for a verified signature failing that policy. Explicitly specify the mixed-case matrix: valid eligible signer wins; trusted invalid signature, valid out-of-period signature, unsupported signer, and absent signature are distinct observations. Add forged-tag, corrupted-outside-signature, unknown-plus-retired-signature and mixed eligible/outside tests.

### F4 — MEDIUM: missing snapshot evidence does not reliably return UNVERIFIABLE

Location: verifier:94, 129–156, 229–240; selftest missing-root control and wrong-domain control.

`run()` unconditionally reads `dns-snapshot.json.ots`; an actually absent proof raises FileNotFoundError before `SNAPSHOT_NOT_ANCHORED` can be emitted. That branch handles an existing proof with no usable anchor, not the stated missing-proof case. Deleting the `. DNSKEY` message from an in-memory snapshot reproduces `KeyError: '. DNSKEY'`. The existing root-missing test substitutes another DNS message at that map key, which exercises missing RRsets but misses an absent message. Child response omissions similarly crash or become FAIL when caught as KeyError, although missing proof material is not performed-and-failed evidence. The wrong-domain selftest explicitly counts KeyError as success.

Decision (4) is sound: without the snapshot's own authenticated time, no receipt time, capture clock or present clock can substitute. Missing evidence is UNVERIFIABLE unless another required check actually fails. The default no-usable-anchor path makes that distinction correctly; the file/message loading paths do not. P8 requires a separate snapshot envelope/proof; A9 C4 evaluates at its time.

**Proposed fix:** inventory required inputs before accessing them; return typed missing-evidence observations, continue independent checks for INVALID precedence, and distinguish absent evidence from present malformed evidence. Add truly missing file/message controls and require typed results, not any exception. Keep `--eval-time` explicitly diagnostic-only: its override is useful for controls but must never become a V1 time source. A bad OTS digest should not produce an authenticated evaluation time even though the ledger already prevents overall acceptance.

### F5 — MEDIUM: all presented RRSIGs are recorded as “used,” including signatures that did not validate

Location: verifier:81–89, 218–224, 252–255; profile §7.3.

`dns.dnssec.validate` accepts when an appropriate signature validates, but `val()` then appends every signature in the candidate RRset to `used`. An extra expired, not-yet-valid or invalid signature can therefore narrow the joint window and trigger a FAIL despite a valid signature path. This is another avoidable false reject, especially around a rollover. It also misstates the evidence underlying the reported joint window. The profile's “every RRSIG window in the chain” needs to mean the signatures actually selected to authenticate the chain, not every offered alternative.

**Proposed fix:** validate/select individual signatures and retain only the successful witness for each required RRset (or explicitly search compatible witness paths). Pin the witness-selection rule if diagnostic outputs must be stable. Add valid-plus-expired and valid-plus-corrupt-signature controls. This finding is based on the inspected validation/recording mechanism; unlike F1, a separate end-to-end mutated fixture was not run.

### F6 — MEDIUM: snapshot tolerance is checked against capture time rather than the receipt's signed declared time

Location: verifier:218–221, 241–256; profile §7.3; DD:94.

The implementation sets `snap_declared = snap['captured_end']` and compares the snapshot anchor to that. It never checks the snapshot anchor against the receipt's signed `declared_issue_time`. DD and the profile require the snapshot anchor within `[declared − ε, declared + δ]`; in the receipt context “declared” is the signed issue time, and neither source defines a second snapshot declaration that replaces it. A historical snapshot with a locally satisfactory capture/anchor pair can be supplied alongside a much later receipt without this check detecting the mismatch. Whether every other authority rule could permit a complete unsafe acceptance remains unresolved; this is an assigned C4 temporal check that is missing, not a demonstrated complete forgery.

**Proposed fix:** specify exactly which declared time this predicate means. If it is receipt issue time, pass `declared` to this required check; retain capture-to-anchor latency as a separate observation or explicitly registered additional check. If reusable snapshot evidence is intended, register its age relation to the receipt rather than silently replacing the existing predicate. Add independently valid receipt/snapshot proofs whose times are far apart.

### F7 — MEDIUM: step 11 verifies linkage, but does not exercise the selected profile contract

Location: `gitchannel.py:193–230`; `tests/test_gitpath.py:10`; profile §6.3.

The new helper correctly recomputes commit, tree and blob ids, checks every path link, rejects duplicate matching entries, enforces tree/blob modes and exactly parses the canonical 255-byte record. The substituted-blob tests are useful. But its path is caller-selected; tests use `keys/v1/key-assertion`, not `tessera-v1/key-assertion`. It receives neither the validated DNS bytes nor pinned D, receipt bytes, repository signature or OTS proof. Thus it cannot check cross-channel byte equality, pinned issuer equality, or the signed/anchored commit itself. Existing `verify_offline()` is not wired to this helper and still reports only commit→root linkage.

This is a bounded helper, not by itself a false accept; the instrument label is correct. It cannot substantiate a claim that all of the new owner decisions have been implemented or tested together.

**Proposed fix:** keep the helper general if useful, but add an instrument composition that fixes the profile path, verifies the signature over payload derived from the same raw commit, verifies its stamp, compares raw DNS/blob bytes and gates acceptance on signed issuer == pinned D. Test a correct record only at the wrong path, an alternate issuer under the same repository key, mismatched DNS/git values, unsigned commit and unstamped commit. Make the coverage limitation explicit until that composition exists.

### F8 — LOW: the profile claims extraction-only provenance while making new decisions

Location: profile:12–16, §5, §6.3.

“It does not decide anything new” is inconsistent with the dated new owner decisions. Those decisions are clearly labelled, which is good, but they are not decisions supplied by A9. A9's signature ratifies its own recorded OWNER items, not automatically every later owner addition to an unregistered profile. This is a provenance mismatch, not a demand for another author ruling.

**Proposed fix:** describe the document as an extraction plus a separately listed set of dated profile decisions, and state the governing registration/adoption mechanism. Preserve the new decisions and corrections visibly; do not disguise them as A9 citations.

## Answers to the five owner decisions

| Decision | Soundness and compatibility | False accept/reject and partition |
|---|---|---|
| 1. Fixed path; exactly canonical TXT bytes, no LF | Sound profile choice. P8 §7.2 explicitly delegates path and framing; A9 requires the same value/window. Modes 100644/40000 are additional profile restrictions, not A9 requirements. | No demonstrated false accept in linkage/parser. LF or executable-file rejection is intentional conformance rejection once registered, not an inherent security necessity. Fixed-path enforcement and actual DNS equality are not yet exercised (F7). Present nonconforming evidence should be INVALID; missing objects UNVERIFIABLE. |
| 2. Pin (D, repository key); compare signed issuer | Sound. The TXT value has no D; this is a legitimate way to authenticate the repository assertion for a particular domain. A9 fixes D and permits distributed trust; P8 binds issuer in signed bytes. The visible DD correction is appropriate. | Stops cross-domain reuse under the same repo key, provided the comparison is mandatory. With both channels required, git's mandatory D check already prevents overall acceptance for another D; a separate DNS gate is useful for clear diagnostics, not an unresolved overall domain-security hole. Mismatch INVALID; missing trust entry/evidence UNVERIFIABLE. |
| 3. Verified trusted signer outside period INVALID; unknown-only/unsigned UNVERIFIABLE | Defensible policy split: a known period requirement can be performed and failed; an unknown root or absent signature cannot authenticate the chain. A9 does not fix these reason codes. P8 does not govern root verdicts. | Missing signatures must never pass. Unknown-only UNVERIFIABLE is compatible with unlisted rollovers. INVALID still dominates independently failed required checks. The implementation's existential and attribution defects are F1/F3; the validity of the chosen period is F2. |
| 4. No snapshot proof => UNVERIFIABLE, no substitute time | Sound and consistent with A9 C4 and P8 §6. A supplied bad proof is a failed check, hence INVALID, rather than “missing anchor.” | No need for current DNS or a current clock in 2106. Do not promote a missing proof using receipt T or capture time. Real omission crashes today (F4); explicit diagnostic overrides must remain outside V1 acceptance. |
| 5. End KSK-2017 at 11 October 23:59:59Z | Not established as a validation boundary by observation or IANA's rollover date. Compatible with A9's abstract period predicate as a new restrictive policy, but inadequately justified. | Avoidable rejection of authentic cached/pre-rollover evidence anchored later (F2). No demonstrated false accept from this cutoff. Reducing the compromise window is a tradeoff, not proof that the rejected evidence is forged. |

## Decisions stated in the profile that A9 does not settle

This inventory distinguishes new choices from inherited encoding/spec details. A9 binding the signing-commit ENC baseline is sufficient provenance for ENC decisions; they are not all new profile decisions.

1. §5/§6.3: pairing the repository key with D and the explicit signed-issuer equality gate. A9 fixes the domain and repository trust key but does not prescribe that pairing/check.
2. §6.3: `tessera-v1/key-assertion`, no framing bytes, and exact entry modes. P8 explicitly leaves path/framing out; A9 does not select modes.
3. §5: exact KSK-2017 inclusive cutoff and its asserted security rationale. A9 requires separate periods, not this end time.
4. §5: detailed INVALID/UNVERIFIABLE root-case split and new reason codes, including `SNAPSHOT_NOT_ANCHORED`. The snapshot's own anchor requirement is inherited; these specific classifications/codes are new elaboration.
5. §5: repository key described specifically as the public half of an offline root. Its source is the operations runbook, not an A9 requirement. Keep it an operating fact or explicitly adopt it as profile policy.
6. §2.1/§3: the twelve-member inventory and ten-stage presentation elaborate ENC/SPEC. A9 does not itself decide this exact container/member list or a stage order. The profile correctly leaves container encoding and stage reason precedence OPEN; the table must not be mistaken for a newly fixed execution order.
7. §9: seven dependency-entry fields are inherited from SPEC, not specified by A9's eight-item dependency list. This is legitimate additional source material, already labelled.

The substantial OPEN list is otherwise candid: container, dispatch fields, binding forms, M5, git timing, pin format/coverage/conflicts, snapshot body and time derivation remain unresolved. The profile does not falsely say the hybrid branch or its id is chosen. The signed ENC baseline supplies spec id, fingerprint schemes, canonical grammar, signature serialization and number details; those do not contradict A9 merely because A9 does not repeat them.

## Long-horizon boundary

A verifier running in 2106 must evaluate the archived evidence at the proof-derived historical times under the same governing specification and trust configuration, not at 2106 or using then-current root publication status. The current default DNSSEC evaluation follows that principle. Past revocation/removal does not retroactively remove a pinned historical root. The same inputs should reproduce the same verdict, including existing false rejects; reproducibility is not evidence that the cutoff policy was sound. Historical compromise/algorithm safety remains a separate assessment under A9.4. No renewal or proof of security through 2106 is being established here. Also keep epoch arithmetic wider than 32 bits; archived DNS RRSIG fields must be interpreted under their historical time semantics, not as current-date freshness checks.

## Validation

- `cd prototype && uv run pytest -q`: **105 passed**, exit 0 (1.40 s).
- `cd prototype && uv run python spike/selftest.py`: **26/26 controls passed**, exit 0. Its KSK-2024 rollover calls use explicitly stated fixture time because that capture has no OTS proof; this is not an anchored end-to-end positive vector.
- Read-only in-memory probes reproduced F1, the root-level cutoff effect in F2, and the absent-root-message crash in F4. No fixture files were edited for these probes.
- Passing tests do not cover the counterexamples above. The original spike still lacks DNS key publication and git-channel evidence, uses an older receipt layout, and excludes DNSKEY_PUBLICATION from its CLI required groups. Its exit 0 is therefore not a V1-conformance or C4 result; SPIKE-REPORT.md already records these limits.

Recommendation: retain the fixed-path/exact-bytes and pinned-domain choices, repair the existential and typed-evidence handling, and settle the retirement-validation and snapshot-to-receipt time policies explicitly before the profile freeze. No claim is discharged by this review.
