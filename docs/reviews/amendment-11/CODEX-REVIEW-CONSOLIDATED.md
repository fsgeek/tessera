**Verdict: not ready for the author’s ruling and signature; fix the dependency omissions and lifecycle contradiction, then confirm the repairs.**

Reviewed the live **282-line** draft, all 15 change-table rows, the scorecard, all 28 disposition records and the prior confirmations. No repository edits or git writes were made. I did not read `levadura_salvaje/predictions/`.

### Findings

**A11X-01 — High: the K-R row still leaves a frozen normative duplicate unchanged.**

Location: [A11:126](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:126).

Row 12 changes ENCODING-V1:557–559 but misses the same rule in [HYBRID-SUPPLEMENT:274–276](/home/tony/projects/tessera/formal/p8/HYBRID-SUPPLEMENT.md:274):

> The issuer obtains `S_kms` … from KMS … sending

That is inside §7’s **exact replacement block**, not merely a record of an experimental capture. Under A11’s component-specific meaning of “issuer,” it retains precisely the actor assignment row 12 replaces. This repeats the dependency defect A11.4 addresses.

**Fix:** add supplement:274–276 to row 12, replacing the actor consistently while retaining the formula and verifier behavior. Explicitly classify the historical “issuer-computed μ” capture descriptions as historical and still fitting.

**A11X-02 — High: the E9-cut row misses A10’s plain-language protection claims.**

Location: [A11:122](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:122).

Row 8 accounts for the adoption, mechanism section and change-table rows, but leaves these registered restatements outside its source inventory:

- [A10:106–124](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-10.md:106): the verifier rejects unlisted keys; the mechanism stops scoped users accepting attacker receipts; holders preserve listing evidence.
- [A10:213–226](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-10.md:213): the listing adds checks, reason codes, issuer duties and protection.
- [A10:432](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-10.md:432): row 26 replaces the boundary sentence under option (e).

These remain misleading descriptions of the narrowed option (e). In particular, the plain-language rejection promise conflicts with V1-CONTRACT:37 and :72: captor-key receipts pass after both authority channels are captured.

**Fix:** extend row 8 with explicit dispositions for these passages. Preserve the dated adoption history and author quotations; supersede the passages describing the listing as a current V1 mechanism. State that no listing rejection, precommitment or preservation duty remains in V1. Keep release-key independence separate.

**A11X-03 — High: A11 introduces an impermissible latch override.**

Location: [A11:268–269](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:268).

The phrase “a latch that expiry can override only by re-observing the chain evidence” permits expiry of a latched attempt. [A2:153–160](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:153) expressly forbids that: expiry applies only to attempts without timely-latched eligibility.

The cited owner design agrees with A2: [design:49–56](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:49) first requires finding the attempt **not latched**, then requires re-observation and a conditional write.

**Fix:** replace the phrase with:

> a latch that excludes expiry; expiry of an unlatched attempt requires re-observing the chain evidence and an atomic check that no latch intervened

No registered relaxation is needed.

**A11X-04 — Medium: the fingerprint correction misses PROOF’s second “no check reads it” statement.**

Location: [A11:124](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:124).

Row 10 correctly repairs PROOF:134–135, but [PROOF:485](/home/tony/projects/tessera/formal/p8/PROOF.md:485) still says:

> No check reads it, and B never computes it.

The profile structurally checks the fingerprint bytes, including cross-field consistency. The historical implementation-B statement can remain if accurate; the unqualified “No check” needs its scope stated. Otherwise the consolidated repair leaves the same contradiction elsewhere in the frozen proof.

**Fix:** add :485 to row 10, distinguishing V1 structural validation from SHA-1 security reliance and from the recorded vector-checker behavior.

**A11X-05 — Low: row 12’s “unchanged assumption” locator contradicts its own edit.**

Location: [A11:126](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:126).

“The (K-R) assumption itself (:151–152, :156) is unchanged” includes the beginning of the very sentence whose actor changes; :156 is blank. The no-other-context/protocol restriction is at :157.

**Fix:** say that the **allowed-message, pure-mode, empty-context and exclusive-key-use restrictions** remain unchanged, citing :151–153 and :157, while the enforcement actor changes. Avoid declaring the source wording unchanged.

### Change-table audit

“Checked” below means the quoted source words match after Markdown/line-wrap normalization; explicit ellipses are omissions, not complete quotations.

| Row | Assessment |
|---|---|
| 1 | Checked. Appropriate V1 narrowing; correctly distinguishes non-exportability from misuse. |
| 2 | Checked. Extends A9’s existing narrowing to the §6 restatement. |
| 3 | **Was is a paraphrase**, not an exact quotation. Proposed fields, floor and discharge conditions are adequately identified. Label it “paraphrase” for precision. |
| 4 | Mixed paraphrase/exact excerpt. Four locations checked; V1 ratification and non-V1 preservation are correct. |
| 5 | Checked. Correctly removes issue-time authority/publication implications. |
| 6 | Checked. Correct signature-inclusive target; retains the surrounding identity-handle rule. |
| 7 | Mixed paraphrase/exact excerpt. All three custody/deadline locations are represented; replacement remains pending. |
| 8 | Mixed paraphrase/exact excerpts. Correct substantive cut and row-33 treatment; **incomplete dependencies, A11X-02**. |
| 9 | Checked. Correct once row 8’s cut is registered. |
| 10 | Checked. Correct replacement; **missed restatement, A11X-04**. |
| 11 | Source wording checked. Replacement correctly separates classical and pair identifiers. Inner quotation marks differ typographically. |
| 12 | Quoted excerpts checked. Actor replacement is bounded; **A11X-01 and A11X-05 remain**. |
| 13 | Checked. Correctly distinguishes genuine-frame captures from spike-tag captures; does not turn SIG-H5 into conforming production evidence. |
| 14 | Checked. Correct hybrid fixture description and reason precedence; preserves A9’s INVALID outcome. |
| 15 | Checked. Correct locator-only repair. |

Apart from the identified omissions, I found no additional sentence silently changed by these rows. The table should explicitly label its paraphrases rather than imply every Was cell is an exact quote.

### Completeness, clarifications and author choice

All **28 disposition IDs appear in A11**. That includes the explicitly unconfirmed c145; no confirmed or partial disposition lacks a corresponding row, clarification, draft correction or owner repair.

The owner repairs are **listed, not completed**. Live S4 still contains the 24-hour FAILED rule; DEPLOY steps 6–7 remain unconditional; PROPERTIES still omits S; S7 still attributes per-receipt cost to H3. A11.7 largely acknowledges their pending status. These should not be reported as implemented repairs.

All three A11.6 readings are acceptable:

- Item 1 preserves rule O and interprets its rationale for the hybrid.
- Item 2 reconciles statement identity with exact receipt identity using ENC’s existing qualification.
- Item 3 applies OpenPGP duties to the OpenPGP signers actually in use, preserving rule R for kms.

Neither custody option offers production use of prototype code. Option 1 accurately identifies the retrospective deadline relaxation and requires evidence on service bytes. Option 2 accurately retains classical fallback custody, has no hybrid custody deadline and requires freeze reconciliation. PQ is correctly described as the author’s preference rather than a C-row requirement. The owner recommendation is visibly separate from the pending author decision.

The outcome disclosures are materially adequate: they expose the late checklist repair, retrospective custody relaxation, prior K-R misstatement and withdrawn spike-key reuse. Row 13 preserves the historical capture defect, and row 14 preserves the registered verdict. I found no undisclosed conversion of a failed historical result into a pass. Preserve that distinction when regenerating the fixture.

### §A11.2 verification

**PASS.** Compared with the amendment text embedded in `codex-confirm-4.log`, only the owner-harness count/coverage paragraph changed; the requirements and limitations are unchanged.

All **15 manifest entries verify**. The manifest hash matches A11:70 exactly:

```text
844cb7ff8df59f047d2ea48536ddb30bad5b3e93684acbce6a4dad1241aee42d
```

The live profile also matches frozen commit `270ca49`. I did not rerun the test suite or establish deployment evidence; manifest verification does not discharge P3.

### Owner prechecks

| Check | Result | Evidence |
|---|---|---|
| Capture row | **FAIL** | [A11:122](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:122) leaves A10:106–124’s rejection promises undisposed. A11X-02. A11’s direct fixture claim at :128 appropriately assumes honest DNS. |
| Trigger clause | **FAIL** | [A11:269](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:269) permits expiry despite a latch; A2’s expiry trigger requires no timely latch. A11X-03. |
| Requester | **PASS** | [A11:180](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:180), :188–189 and :224–231 address queue access, principals able to cause signing, direct key permission and administrative bypass. No claim rests solely on key storage. |
| Binding text | **FAIL** | [A11:269](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:269) describes an owner construction that contradicts registered A2 latch protection. The cited owner design itself correctly forbids that construction. |

