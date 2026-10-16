# Codex brief: full review of Amendment 9 (draft, unsigned)

Repo: /home/tony/projects/tessera. Review docs/phase-0-prereg-amendment-9.md IN FULL — every section, every row of
the changed-sentence table. Not a subset. The author (Tony Mason) signs it only after this review and a skeptic
read; his read must be short, so this review must be complete.

Sources to check it against: docs/V1-DERIVATION-DRAFT.md; docs/V1-SCHEDULE.md; docs/phase-0-prereg.md and
amendments 1-8; docs/implementation-spec.md; formal/p8/ENCODING-V1.md and PROOF.md (revised 2026-10-12);
docs/reviews/anchor-signatures/; prototype/spike/SPIKE-REPORT.md; prototype/spike-pq/REPORT.md.

Check:
1. Fidelity: does it implement exactly the decisions it names (author decisions A/B/C of 2026-10-10 with his quoted
   words; the owner decisions of 2026-10-12) — no more, no less? Is any owner decision given the grammar of an
   author ruling, or vice versa?
2. Completeness: verify every changed-sentence row against the cited file:line (quote mismatches). Find registered
   sentences the amendment changes in effect but does not list. Nothing may be dropped quietly.
3. Soundness: is the V1 claim (C1-C7) true given the checked evidence and the stated non-claims? Narrow-the-claim
   first: prefer WORDING over new MECHANISM. Check the two conditional product guarantees, the issuance-window rule
   (including chain-time skew and the 96 h retirement margin vs δ), the signature-inclusive anchor, the
   existential root-KSK rule, the conditional hybrid signer profile and its fallback, the code rule replacing
   "Before any code", and the closure rule.
4. Internal consistency and consistency with ENCODING-V1/PROOF as revised.
5. Readability for the author: does it open with the claim, adversary and boundaries in ordinary language?

Write numbered findings to docs/reviews/amendment-9/CODEX-REVIEW.md, each with severity, evidence (file:line), and a
recommended disposition (WORDING / MECHANISM / OMIT / REJECT). Do not edit any other file. Do not commit.
