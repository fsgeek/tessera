# Codex non-author review of the ledger register draft and the k = 6 runs (2026-09-14)

Reviewer: OpenAI Codex CLI (`gpt-6-astra`), run by the author in his own
session on 2026-09-14 against `formal/suite/LEDGER.md` (first draft,
uncommitted) and `formal/tla/k6-2026-09-14/` (uncommitted); the author
pasted the reviewer's answer to the owner instance. The reviewer's
recommendation was **not to confirm the ledger as written**. Every
factual claim below was checked against the tree before disposition.

## Dispositions (owner instance, 2026-09-14)

1. **R-1 evidence — the S-P2 severing test is wrong.** ACCEPTED. The reviewer removed the frame-fingerprint comparisons from every signer slot of `sp2_q2_degraded_compromised.pv` and `Reattributed` stayed unreachable with honest acceptance reachable: the manifest-hash and manifest-key checks preserve the binding. This is S-P3's own finding F3 ("the tuple fingerprint match and the manifest-hash check together compensate for its absence") applied to S-P2, which the register overlooked. L-01's S-P2 determination and companion C-C2 are repaired: a severing mutation must remove the complete binding relation (the frame's fingerprint pin, the manifest-hash equality and the tuple fingerprint match), and the register now records what each single removal does. The principle the reviewer endorses stands: transcription alone does not settle R-1.
2. **D5 — a DSKS transplant under another key does not falsify P1's authorship-under-an-honest-key claim.** ACCEPTED. "Removing a signature check and permitting key substitution are different failures." D5 is rewritten to name the producer fact it severs and a companion whose red is on the consumer's own query for that fact, or is demoted to complementary if no such companion exists.
3. **R-2 — represent the redundant protection explicitly; register `SetAltered` and its honest-flow witness in §6.** ACCEPTED. Companion C-C3 must falsify `SetAltered`, which the §6 query list omitted; both are added.
4. **R-3 — yes, but "S-STANDING's fixture contains no wrapper" is inaccurate.** ACCEPTED. S-STANDING declares `wrapCore` and its companion exercises a wrapper-shaped transplant; the gap is the composition of S-P7's wrapper processing with S-STANDING's assessment. Wording corrected in L-13 and R-3.
5. **E18 qualification (a) — bounded instances, not arbitrary skew or a parameter-general theorem; reducing skew reduces the modelled behaviours.** ACCEPTED; sentence added to `RESULTS-K6.md` §3 and §4.
6. **E18 qualification (b) — the P5c `_Broken` run stops at its first violation and does not establish "exactly".** ACCEPTED. A remaining-invariants run (`P5c_IssuanceProtocol_Broken_Green_k6.*`: the five other invariants plus `RefusalLatched`) was added the same day; the result is recorded in `RESULTS-K6.md` §1. The bridge companions already had per-invariant red runs plus full-space green runs on the rest.
7. **Not an E18 sign-off.** Recorded as such; E18's row in `BAND0-EXIT.md` reads "non-author review owed" until a full pass runs.

## Codex review — verbatim (as pasted by the author)

> This is progress toward exit, but I would not confirm the ledger as written yet. I found a concrete error in the proposed severing test, and a second dependency that needs a better argument.
>
> R-1: transcription alone should not decide the classification—but its supporting evidence needs repair.
>
> The ledger says removing S-P2's frame-fingerprint check makes its Reattributed query fail. I tested that against the current model:
>
> - Baseline: re-attribution unreachable.
> - Frame-fingerprint comparisons removed from all signer slots: still unreachable, with honest acceptance still reachable.
>
> The manifest-hash and manifest-key checks preserve the binding. "This check alone suffices" does not imply "removing this check breaks protection."
>
> Consequently, L-01's S-P2 determination and proposed companion C-C2 are incorrect as stated. The capstone needs a mutation that actually severs the complete binding relation. Fresh test evidence (/tmp/tessera-ledger-review-msmxxnlu)
>
> There is another issue in D5: a DSKS transplant accepted under another key does not, by itself, falsify P1's authorship under an honest key claim. Removing a signature check and permitting key substitution are different failures. The ledger needs to demonstrate that its companion severs the named producer fact, not merely that some consumer query turns red.
>
> R-2: I support explicitly representing the redundant protection.
>
> Record the two alternative routes, verify that either survives removal of the other, and require the combined removal to expose the attack. That accurately represents the design.
>
> But the current query list omits SetAltered, although companion C-C3 is required to falsify it. If R-2 is adopted, section 6 must explicitly register that consumer query and the corresponding honest-flow witness.
>
> R-3: yes, I recommend the wrapped-standing linkage query.
>
> That is a meaningful composition obligation. However, "S-STANDING's fixture contains no wrapper" is inaccurate: it declares wrapCore, and its companion exercises a wrapper-shaped transplant. The actual gap is composition of S-P7's wrapper processing with S-STANDING's standing assessment, which the existing wrapper-shaped term does not establish.
>
> For E18, the saved bridge output confirms the reported completed search: 86,849,955 distinct states, zero queued, no error at the smaller skew. The report appropriately labels the larger-skew search incomplete.
>
> I would retain two qualifications:
>
> - This establishes results for the specified bounded instances, not arbitrary timestamp skew or a parameter-general theorem. Reducing skew is a real reduction in modeled behaviors, even though the witnesses remain reachable.
> - The issuance report claims the broken companion fails on exactly its registered invariant. Its saved run stops at the first violation; that alone establishes the named failure, not that all other invariants hold. The directory has a separate remaining-invariants run for BrokenSilent, but I did not find the equivalent for Broken.
>
> My recommendation is therefore: endorse the intended R-2 and R-3 work, and the principle that transcription alone does not settle R-1; repair the dependency claims and query list before freezing the capstone plan. I have not performed a full independent audit of the depth-six runs, so this is not yet my E18 sign-off.
