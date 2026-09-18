# Codex reviews of the author's freeze read, `formal/suite/capstone/READ-FREEZE-2026-09-17.md` (2026-09-17, two reads)

Two non-author reads of the **handoff note**, not of the registration.
Neither reopened `PREDICTIONS.md`; both are archived here so the record
shows what the author's one read had been through before he spent it.
Entered 2026-09-18 by the owner instance (successor), from the author's
pasted text (read 1) and the owner-run output (read 2); the prior owner
instance applied both sets of repairs but did not archive the reads.

## Read 1 — dispatched by the author, 2026-09-17 ~23:05 UTC

Reviewer: OpenAI Codex CLI (`gpt-6-astra`), interactive session run by
the author against the **first draft** of the note (the draft is not
preserved; the rewrite that answered it is the note as it stands).
Read-only; no models run. **Four findings, all accepted; three smaller
corrections, all accepted.** The note was rewritten the same evening:
it now opens with the experiment in ordinary language; the choice
inventory is six (two settled, four contestable) and reconciled with §8;
the enrolment reading is presented as a measurement limit; decisions
precede the commit; the staging is an explicit `git add`, not `-A`.

### Disposition (owner instance, 2026-09-17)

All accepted. Nothing routed; nothing in the registration changed.

### Review — verbatim

I would revise this handoff before spending your first read on it. I found problems in how it presents the approval, rather than a newly demonstrated defect in the capstone design. This was a read-only review against the registration, ledger, governing amendment, and cited reviews; I did not rerun models.

Four findings matter.

1. Its "four choices" are not the same four choices in the section it sends you to.

   The handoff's list (formal/suite/capstone/READ-FREEZE-2026-09-17.md:69) names same-key wrapping, adversary enrollment, paired evidence, and reporting presented terms.

   But the registration's numbered list (formal/suite/capstone/PREDICTIONS.md:1958) names the standing/wrapper join, the one-key/one-manifest fixture, same-key wrapping, and adversary enrollment. Across those lists there are six distinct choices.

   The omitted explanations are consequential. In particular, the signer/manifest test supports its stated interpretation only when each honest key signs exactly one manifest. The registration explicitly explains that reusing a key across manifests can make that test fail without changing the verifier.

   Repair: reconcile the inventories and explain those two choices briefly. This need not create two new approval gates; it must make clear which choices you are accepting, which were already settled, and what limits follow.

2. The adversary summary makes a measurement limitation sound like a security failure being excluded.

   The handoff says (formal/suite/capstone/READ-FREEZE-2026-09-17.md:83) that legitimate enrollment of an adversary's key "falsifies the strict baseline with no verifier change."

   The source paragraph (formal/suite/capstone/PREDICTIONS.md:77) supplies the essential missing explanation: a genuinely enrolled key is an issuer to the verifier, but the model's IssuerSigned event is emitted only by its honest issuer processes. The broader authorship assertion therefore fails; the honest-key assertion remains intact. The paragraph explicitly calls this not a defect of the design.

   Repair: carry that explanation into the handoff. Otherwise, you could reasonably read this as "we excluded an attacker because allowing it broke our security claim."

3. The instructions permit giving a decision too late to incorporate it into the freeze.

   The REFUSAL section (formal/suite/capstone/READ-FREEZE-2026-09-17.md:54) says option (i) requires a new query and companion before freezing, then invites you to give your answer "in the commit message." But that very commit freezes the registration.

   Likewise, "confirm or overrule … at the freeze" needs to distinguish communicating an objection from incorporating its consequences.

   Repair: state the sequence plainly: your decisions first; affected registration text and predictions updated; applicable review prerequisites satisfied for that version; then your freeze commit. Existing approval concerns the version reviewed, not an unwritten REFUSAL addition.

4. It does not first explain, in ordinary language, what this experiment is supposed to establish.

   It opens with commit mechanics and review history, then directs you into technical passages. The distinction between registration readiness and demonstrated composition is correctly retained, but there is no short account of the claim, adversary, and boundaries to orient your judgment.

   Something like this would help:

   > The capstone tests whether the separately examined checks still support their claims when combined in one verifier. Deliberately broken variants test whether removing a required connection exposes the expected failure. Success would support the registered symbolic composition within its stated limits; concrete encoding, implementation fidelity, and connections to the TLA+ models remain separate obligations.

   Follow that with the consequential limits—including the one-key/one-manifest fixture—and then present your decisions. This is an editorial repair, not a demand that you learn ProVerif.

There are smaller corrections too: the archive description stops at batch sixteen/cap25, although batch seventeen/cap26 exists; "the event table" begins after its assigned passage ends; and git add -A stages everything rather than an explicitly checked freeze package.

Your "2.4 googol words" estimate is modestly high: the guide is about 1,085 words, and its required excerpts another 2,358. The problem is less their length than the repeated history and the work you must do to translate them into decisions.

My recommendation is a bounded rewrite of the author handoff, with the choice inventory reconciled against the registration. I am not recommending another unrestricted review cycle. The current handoff asks you to supply clarity that it should provide.

## Read 2 — run by the owner instance, 2026-09-17 23:55–23:57 UTC

Reviewer: OpenAI Codex CLI (`gpt-6-astra`), `codex exec`, non-interactive,
against the **rewritten** note, asked to check every line range and word
estimate, the six-choice inventory and its limits against the
registration's words, the enrolment explanation, the decision sequence
against the freeze statement, the `git add` package against `git status
--porcelain -uall`, and the plain-language section against A3 §A3.3 and
§7. Read-only; no models run. **Five factual corrections, all mine and
all applied**: two word estimates; the archive count (99 model copies,
20.6 MB, in batches five to seventeen); the findings sequence (round
one's six were missing); the rerun-coverage claim (round twelve re-ran
87 `cap5`–`cap24` copies, round fourteen the eight `cap25`/`cap26`
copies); boundary wording ("ledgered cross-model assumption", the finite
scope stated, one-channel strict baseline vs the both-channels
companion, DSKS as a new key under which an existing signature
verifies). The inventory, enrolment explanation, sequence and staging
package were found correct.

### Disposition (owner instance, 2026-09-17)

All five applied. Nothing routed; nothing in the registration changed.

### Review — verbatim

The rewrite repairs the four original problems, but still needs a few factual corrections before the author’s read. I reviewed files and git status only; I changed nothing and ran no models.

1. **The line references are correct; two reading estimates are materially wrong.** Every registration locator in the note reaches the stated passage, including the event table ending at line 261. Counting whitespace-separated words in the specified ranges gives:

   | Reading-table entry | Note’s estimate | Actual |
   |---|---:|---:|
   | §7, 1844–1882 | 500 | 312 |
   | Freeze statement, 1885–1906 | 200 | 200 |
   | Routed items, 1907–2008 | 900 | 893 |
   | Rows 77 and 79 | 600 | 621 |
   | §1.3, 188–261 | 600 | 893 |
   | **Total** | **2,800** | **2,919** |

   Update the first and fifth estimates and use approximately 2,900 words overall. The note itself adds 1,553 words; fifteen minutes is an estimate for roughly 4,472 words, not a verified reading duration. See the [reading table](/home/tony/projects/tessera/formal/suite/capstone/READ-FREEZE-2026-09-17.md:152).

2. **The six-choice inventory and enrolment explanation now pass.** The two construction choices match [§8 items 1–2](/home/tony/projects/tessera/formal/suite/capstone/PREDICTIONS.md:1958); the four explicitly contestable choices match [rows 77–79](/home/tony/projects/tessera/formal/suite/capstone/PREDICTIONS.md:77), [the evidence-pair contract](/home/tony/projects/tessera/formal/suite/capstone/PREDICTIONS.md:188), and [the report contract](/home/tony/projects/tessera/formal/suite/capstone/PREDICTIONS.md:213). E5 lists the same four contestable choices. The one-key/one-manifest limit matches [C-Q5’s qualification](/home/tony/projects/tessera/formal/suite/capstone/PREDICTIONS.md:667). The enrolment explanation correctly distinguishes genuine issuer status from the honest-process-only `IssuerSigned` event; it no longer presents the alternative as a design failure being excluded.

3. **The decision sequence and current staging package pass.** The note explicitly requires decisions before the commit, amendment and renewed review for option (i), and renewed review for overridden choices. This agrees with the [freeze statement](/home/tony/projects/tessera/formal/suite/capstone/PREDICTIONS.md:1885). Against current `git status --porcelain -uall`, the command’s paths cover all 209 changed/untracked files: the two capstone documents, 15 review records, archive additions and README, and `BAND0-EXIT.md`. No currently changed file lies outside that package; nothing is already staged. This verifies the command against the present tree, without executing it. See the [sequence and command](/home/tony/projects/tessera/formal/suite/capstone/READ-FREEZE-2026-09-17.md:111).

4. **The archive count and review-history summary need correction.** Batches five through seventeen and `cap1`–`cap26` are correct, but that collection contains **99 model copies**, with 99 outputs totaling **20,574,856 bytes**, not about 120 copies. The whole archive contains 130 models, which is a different collection. The [note’s findings sequence](/home/tony/projects/tessera/formal/suite/capstone/READ-FREEZE-2026-09-17.md:165) also omits round 1’s six findings: it gives thirteen numbers for fourteen rounds. The registration records those six at [line 2033](/home/tony/projects/tessera/formal/suite/capstone/PREDICTIONS.md:2033). Finally, “rounds twelve and fourteen … re-ran every archived diagnostic” overstates coverage: round twelve reports 87 `cap5`–`cap24` copies, while round fourteen reports eight `cap25`/`cap26` copies. See the [archive README](/home/tony/projects/tessera/formal/suite/ledger-tests-2026-09-14/README.md:496) and [round-fourteen report](/home/tony/projects/tessera/docs/reviews/2026-09-17-codex-review-capstone-predictions-round14.md:58).

5. **The plain-language account needs tighter boundary wording.** Replace “every fact one family assumed” with “every ledgered cross-model assumption”: [A3.3](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-3.md:220) expressly leaves Layer 2 assumptions unclaimed. State the finite scope directly—two authority channels, two-attempt lineages, wrapper depth at most two, and signer sets of at most two—as [§7 requires](/home/tony/projects/tessera/formal/suite/capstone/PREDICTIONS.md:1846). The adversary summary should distinguish the one-channel strict baseline from the both-channels-compromised companion, which [the registration includes](/home/tony/projects/tessera/formal/suite/capstone/PREDICTIONS.md:88). For clarity, describe DSKS as deriving a **new key under which an existing signature verifies**; the theory explicitly excludes recovery of the original key. See [the capability definition](/home/tony/projects/tessera/formal/suite/lib/tessera_theory.pvl:91).

The note is close, but not yet fit for the author’s one read. Correct the reading estimates, archive count, findings sequence and rerun-coverage claim, and make the plain-language boundaries explicit. The choice inventory, enrolment explanation, decision-before-freeze sequence, and current staging package need no substantive repair; none of these findings requires reopening the registration.
