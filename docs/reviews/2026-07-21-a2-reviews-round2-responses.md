# A2 pre-signature review — round 2: re-review of the folded revision

**Date:** 2026-07-21. **Reviewers re-consulted by the author:** Gemini,
Grok, GPT-5.6 (Codex CLI). **Verdicts on the revised draft:** Gemini —
sign; Grok — sign, contingent only on the two author-reserved rulings;
GPT-5.6 — **do not sign yet: one new blocking finding** (clock
precedence), plus four small wording repairs.

## The blocking finding (GPT-5.6), verified

**Which clock expires an attempt?** A2.1 makes chain time authoritative
for shipping; P5c expires attempts and enters refusal on its fused
`now` clock; the bridge scoped retry/refusal out as "orthogonal to the
ship/verify seam." The reviewer refuted that orthogonality claim with
the bridge's own committed witness trace
(`P5cP5P6_Bridge_Sanity.out`): declared = 0, δ = 2, wall now = 3,
chain timestamps in-window — Ship legal in the bridge at a moment
P5c's fused-clock machinery would already have discarded/refused the
attempt. VERIFIED against the committed .out (session instance,
2026-07-21). The two models admit different outcomes away from the
boundary, so A2.1 shipping and A2.3 refusal are not compositionally
reconciled until the author rules on clock precedence.

**Consequent defect, also verified:** the round-1 boundary-tie sentence
registers the race at `confirmed_at = declared + δ`, but P5c's race is
keyed to `now = declared + Δ`; decoupled, these differ. The boundary
sentence must be rewritten AFTER the clock ruling, not independently —
left as-is pending the ruling.

**Session instance's addition, for the ruling's consequences:** the
divergence reopens a closure A2.0 currently claims. A2.0's
two-verifiable-receipts residue is said to be "closed by A2.2 and
A2.4" — an argument that silently depended on the fused clock's
guarantee that a discarded attempt is chain-late (A2.2 rejects it).
Under decoupled clocks with a wall-clock lifecycle, a discarded attempt
can be **chain-valid**: signed, anchored, in-window, unshipped. If a
dishonest issuer later ships it alongside the re-issued receipt, both
verify — A2.2 rejects neither, and A2.4's per-receipt anchor binding
does not deduplicate content across receipts. Closure of that residue
then rests on lineage/equivocation-evidence mechanisms (the row-2
territory) or an explicit dedup rule — an A3-scale disposition, and an
input the clock ruling should be made with.

**Disposition: ROUTED TO AUTHOR** (the reviewer's three options:
wall-clock cutoff wins / chain-time wins / two-clock rule with explicit
precedence). The bridge header's "orthogonal" claim is corrected in
place either way (done — marked CORRECTION, refuted-by-own-witness).
Post-ruling bench work, whichever way it goes: bridge `Ship` gains (or
registers the absence of) a lifecycle guard; the boundary sentence is
rewritten on the ruled clock; P5c's expiry comments are aligned.

## Small repairs (GPT-5.6 round 2), all folded

1. **Stricter ε′ unnamed** — the tolerance-scoping sentence now covers
   both tolerances (δ′ and ε′; guarantee scoped to the issuance
   policy's δ and ε).
2. **Provenance still says literal "depth k reached by"** — now
   annotated with the ratified chain-time proxy form in place.
3. **A2.0's bare "Nothing is weakened"** (also Grok's residual 1) —
   now "No A1.2 property is weakened… (stated precisely in A2.6)";
   A2.0's "same predicate" opener also scoped to "same temporal
   conjuncts under the issuance policy's tolerances."
4. **"Full VALID_STRICT" over-names the temporal test** — now "full
   three-conjunct temporal predicate (the P5 temporal test inside
   VALID_STRICT)" in A2.1 and synced in the bridge module comments.

## Reviewer self-assessments, noted for future weighting

Grok's round-2 self-calibration is on the record and matches the
round-1 archive's note: its round-1 pass was the most agreeable and
thinnest, and it now states it would weigh "more aggressive on scope
language and cross-artifact correspondence, less satisfied with
'intent recoverable.'" Gemini and Grok both explicitly endorse the
folded union, including the dispositions that overruled them. All
three reviewers endorse declining the chain-agnostic txid wording
while Bitcoin/OTS remains the registered construction (Gemini, whose
finding it was, concurs with the decline).

## Standing after round 2

Sign-blockers: (1) the clock-precedence ruling (author), with the
boundary-sentence rewrite downstream of it; (2) the two round-1
author-reserved items (A2.4 dispute-scope narrowing — folded text
awaiting confirmation; double-SHA-256 decline — awaiting confirmation).
Explicit follow-ons that signing A2 does NOT close: header
authentication specification (A2.2 obligation / H1a), refusal
reporting (A3), bridge non-author review (pending), and now the
two-receipts-residue closure under the ruled clock semantics (A3 /
row-2).

Verbatim round-2 responses follow.

---

## Verbatim: Gemini

> Thank you for sharing the updated draft and the review aggregate. I
> have reviewed the revised docs/phase-0-prereg-amendment-2.md and the
> disposition notes. Claude has successfully addressed all of my
> concerns, and the revisions haven't introduced any new issues. The
> synthesis of the three independent reviews has resulted in a much
> stronger, more precise document. [Itemized resolutions 1–6 omitted
> here for length: each marked "Addressed," matching the disposition
> matrix; item 7 (double-SHA-256): "Explicitly declined and flagged for
> you (the author)… completely sound. Unless you are specifically
> aiming for multi-chain neutrality in Phase 0, leaving this as
> double-SHA-256 is the right choice."] Overall, the incorporation of
> the other reviewers' findings (like C2's sharp catch about the
> verifier's stricter policy delta δ′ < δ) has further tightened the
> document. I have no new concerns and would be ready to sign this
> revised draft.

## Verbatim: Grok

> Short answer: Claude has addressed my three repair items well, and
> the union of the other reviewers' findings was folded in honestly. I
> have no new blocking concerns. I do have a few light residuals and
> one note of self-calibration. I would now sign with only
> author-reserved decisions, not more textual repairs from me.
> [Status table omitted for length: items 1–7 all "fixed"/"clean",
> including "GPT-5.6 was right; my 'no defect' was too soft" on A2.4.]
> What I missed (worth owning): the disposition matrix's calibration
> note is fair: my round was the most agreeable and the thinnest.
> Concretely I under-called or missed: identical predicate /
> verifier-owns-tolerances (C2)… unconditional "terminates" vs
> safety-only model note (M1)… A2.4 "dispute" breadth (C9/M4)… proxy /
> backward skew (C10), nine-day overclaim (C5), "red on exactly" (C6),
> A3-as-already-registered (C7), txid retrieval vs identity (C8) — all
> real; all repaired. That is useful information for how to weigh my
> next review: more aggressive on scope language and cross-artifact
> correspondence, less satisfied with "intent recoverable."
> Did the repairs create new concerns? No blockers. Small residuals
> only: (1) A2.0 still leads with "same predicate"… and a short
> "Nothing is weakened"… optional polish, not a signing block. (2)
> Header authentication is largely deferred… an open discharge
> obligation, not a text defect. Worth tracking in PROPERTIES.md / A3.
> (3) Author-reserved items are still open by design… both need your
> ruling, not more assistant rewrites. (4) Bridge non-author review
> still pending… Do not treat the bridge as fully discharged until
> that gate runs.
> Updated verdict: I would sign the revised draft, contingent only on
> your rulings on the two reserved items, and treating header
> authentication and A3 refusal reporting as explicit follow-ons…
> The multi-reviewer union was clearly stronger than my single pass —
> which is exactly the discipline working.

## Verbatim: GPT-5.6

> Claude addressed nearly all of my prior concerns faithfully. I would
> not reopen the txid, standing, header-provenance, nine-day,
> A3-lifecycle, or A2.6 dispositions. However, the new bridge exposed
> one substantive issue that should block signing until ruled upon.
>
> ## New blocking concern: which clock expires an attempt?
> A2.1 now makes chain time authoritative for successful issuance,
> while P5c expires attempts and enters refusal using its fused now
> clock… The bridge explicitly omits retry/refusal as supposedly
> "orthogonal"… The bridge's own sanity trace disproves that
> orthogonality: declared = 0, δ = 2, wall now = 3, anchor_time = 1,
> confirmed_at = 1, Ship succeeds… In a decoupled implementation,
> P5c's final crossing would instead have entered refusal when wall
> time advanced from 2 to 3. Thus the two models admit different
> outcomes away from confirmed_at = declared + δ. This requires a
> protocol ruling: [wall-clock cutoff wins / chain-time predicate wins
> / two-clock rule]. Until one is chosen, A2.1 shipping and A2.3
> refusal have not been compositionally reconciled.
>
> ## Consequent defect: the boundary repair uses the wrong boundary
> The new sentence registers the race only at confirmed_at = declared
> + δ… P5c's race is actually keyed to now = declared + Delta… The
> boundary sentence should be rewritten after the clock-precedence
> ruling, not independently.
>
> ## Smaller residual concerns
> 1. Stricter ε remains unnamed… 2. The opening still describes the
> proxy as literal time… 3. A2.0 retains the broad "Nothing is
> weakened."… 4. "Full VALID_STRICT" is slightly misleading…
>
> ## What is resolved
> [List of ten repaired items.] I also agree with declining Gemini's
> chain-neutral txid wording while Bitcoin/OTS remains the registered
> anchor construction. My verdict is therefore: not sign yet; sign
> after the clock-precedence ruling and the resulting boundary repair,
> plus the smaller wording corrections above. No files were changed
> during this audit.
