# Identity boundary and evidence floors — P1 rulings

**STATUS: DIALOGUE DECISIONS (2026-07-28), DOCUMENT PENDING COLD
READ.** Per the three-state discipline (Codex review, 2026-08-07):
the rulings below are *dialogue decisions* — the author selected them
in the 2026-07-28 session; this document is the *record pending cold
read*; adoption occurs when the author has cold-read, resolved the
marked forks, and committed. "Ruled" below means ruled in dialogue,
never adopted-on-the-record.

**STATUS UPDATE (2026-08-07, end of session): AUTHOR ACCEPTED AS
WRITTEN** — see "Tony's notes" at the end of this document. The cold
read occurred and evolved into two adversarial review rounds with
revisions, so the acceptance is of the reviewed text, with the
recorded proviso that issues detected later require further
amendment. Adoption completes at the author's signed commit and OTS
stamp.

**Adoption route (author decision; framed in Codex review round 2):**
two forks remain open — manifest digest vs authorized tuple for the
chain's first link; independent per-layer vs aggregate verdicts. (A
third, concise vs enumerated floor formulation, was dissolved by
author ruling 2026-08-07 — see Ruling 2 item 5: both forms register,
bound by a mapping clause.) Two coherent routes:
(a) resolve all three before adopting these artifacts; or (b) adopt
now a deliberately minimal floor requirement and docket the exact
realization for Amendment 3. Both reviewers (Codex, Claude) favor
(b) with the adopted decision limited to:

> Every valid verdict requires at least one continuous accepted
> evidentiary chain per independently evaluated attestation layer;
> redundant paths may be waived, but the final complete chain may
> not be.

"Independently evaluated" settles the per-layer question
consistently with P7; the exact links are then resolved in A3
before the spike.

**Date of rulings:** 2026-07-28. **Ruling author:** Tony Mason.
**Consultation:** Codex dialogue (2026-07-28 session), Claude
concurring with one accepted correction (linked-form floors).

**Provenance note (honesty requirement):** this document was drafted
2026-08-07 by the assistant (Claude, Fable 5) from the structured
session record of 2026-07-28, because the ruling doc was not written
in that session. The Codex dialogue verbatim was recovered later the
same day from the on-disk primary source
(`~/.codex/sessions/2026/07/28/rollout-2026-07-28T14-38-00-019fa929-3f2c-75e2-92d6-87b7e4147d09.jsonl`)
and is quoted below; llm-memory did not hold this session (enrollment
gap, reported separately). Nothing in this draft is on the record
until the author has read it cold.

**Provenance portability (Codex review, incorporated):** the transcript
path above is a private local file; future public readers cannot
inspect it. The quotations embedded in this document — and, once
adopted, this document's text itself — are the public record; the
inaccessible transcript is background evidence only. Whether to
additionally archive a sanitized extract of the session in the
repository is an author decision.

## Ruling 1 — the identity boundary

Tessera attests the **identity of the framed bytes presented at an
issuance event** — computational identity under the declared
construction — and nothing more. Explicitly outside the attestation:
meaning, truth, intended use, future interpretation, and the
metaphysical identity of the payload's referent.

Consequences:

1. **Replay of a genuinely issued package preserves identity.**
   Whether a given replay is inappropriate is caller-context policy;
   Tessera must not invent that policy on the caller's behalf.
2. **The relying-party story opens with the boundary.** Codex's
   "can establish / does not establish" list should open the
   relying-party document nearly verbatim. The list (recovered
   verbatim, 2026-07-28T16:12Z):

   > Tessera can establish:
   > "This valid package reconstructs the same framed bytes recorded
   > at issuance."
   >
   > Tessera does not establish:
   > "The payload is true."
   > "The issuer understood it."
   > "The relying party interpreted it correctly."
   > "This was the package the relying party expected."
   > "The external thing named by the payload is authentic."

   Codex's care note, same message: Tessera establishes
   *computational* identity of the framed representation under the
   declared construction and assumptions, not metaphysical identity
   of the payload's referent — "If the frame says 'this image depicts
   Tony,' Tessera can preserve that exact assertion; it cannot
   establish who the image depicts."
3. **P1's statement stands as existential issuance-event
   authenticity** — a ProVerif non-injective correspondence — with
   context and replay scoped out of P1 and into caller policy.

## Ruling 2 — evidence floors, ruled in LINKED form

Codex proposed counted floors: every valid verdict requires ≥1
accepted authorized signature AND ≥1 accepted external authority
evidence. The author ruled in dialogue for the **linked** form
instead, accepting Claude's correction:

> Every valid verdict requires **at least one accepted signature whose
> authorizing manifest is itself supported by at least one accepted
> external authority evidence**, plus proof-of-possession per P10.
> Policy records waived redundant members.

Rationale for linked over counted — the two-worlds attack: in the
counted form, the external evidence can support manifest M′ while the
accepted signature claims authority from manifest M; both counters
pass with the chain between them broken (aTLS genus). The floor must
be one evidence chain, not two tallies.

Scope and registration:

1. **Quantified per attestation layer** (inner and outer manifests
   under wrapping).
2. **No change to P4's partition** — the floors bound entry into the
   VALID states; they do not add states.
3. **Registration is an A1.2.1 tightening in Amendment 3**
   ("at least one", linked form). The capstone composition model must
   prove the **linkage**, not just the cardinalities.
4. **Codex's epistemic argument, on the record:** without a floor, the
   model's IssuanceEvent correspondence becomes privileged historical
   knowledge unavailable to a real verifier — the proof would be of
   the wrong model.
5. **Codex withdrew the counted form and expanded the linked form
   into an explicit witness chain** (recovered verbatim,
   2026-07-28T17:07Z): "Claude's correction holds. My counted floors
   were insufficient because they established existence of
   components, not continuity of the evidentiary path between them.
   [...] I withdraw the two independent-count formulation." Codex's
   recommended enumerated chain:

   > accepted external evidence
   > → exact manifest
   > → issuer and key
   > → proof of key possession
   > → accepted signature
   > → exact framed bytes

   and its recommended author ruling text:

   > Tessera validity attests framed-byte identity, not meaning.
   > Every `VALID_STRICT` or `VALID_DEGRADED` verdict requires, for
   > each attestation layer contributing to that verdict, at least
   > one complete accepted evidentiary chain linking an external
   > manifest-authority evidence to the exact manifest, issuer,
   > signing key, proof of possession, accepted signature, and framed
   > bytes. Degraded policy may waive redundant members but may not
   > break or eliminate every complete chain. Every waiver is
   > recorded.

   `[FORK DISSOLVED — AUTHOR RULING IN DIALOGUE, 2026-08-07.]` The
   two formulations are complementary, not rivals — the same
   requirement at two altitudes. **A3 registers both:** the concise
   linked form as the property statement (the A1.2.1 tightening; the
   form the relying-party story and the defend-it-cold essay carry),
   and the enumerated witness chain as its normative expansion —
   bound by a **mapping clause**: "continuous accepted evidentiary
   chain" means exactly the enumerated links and nothing weaker. The
   capstone spike (2026-08-07-survivability-mechanisms-ruling.md §2)
   targets the enumerated links; the prose cannot drift from them.
   Codex's drafting warning ("whose authorizing manifest ... could
   hide another unmodeled join") is discharged by the mapping clause,
   not by choosing a winner — choosing would have lost the
   human-legible property or hidden the joins in prose, respectively.

   This follows standing discipline (every symbolic lemma carries a
   prose mapping to its A1.2 property) and the author's stated
   general stance, recorded here because it is load-bearing beyond
   this ruling: **give relying parties the demonstrated data and
   defer interpretation to their risk tolerance.** Building for a
   future we cannot claim to see clearly means "honesty about what is
   demonstrated" is itself the legitimate deferral of interpretation
   to that future — a defend-it-cold fragment in the same family as
   "not meaning but identity."

   **Linkage correction found in non-author review (2026-08-07;
   citation corrected round 2, verified against A1 §A1.5):** the
   chain's first link as written — "external evidence → exact
   manifest" — exceeds the registered publication mechanism. A1.5
   specifies exactly **two external authority evidences** — the
   DNSSEC chain snapshot and the anchored repository publication —
   both publishing **issuer-key fingerprints**, not exact manifest
   digests, and both *archived in the bundle*, which carries the
   evidences but is not itself a third authority publication. A3 must
   choose: (a) extend the external publications to commit to the
   exact manifest digest — a publication-mechanism change, stated
   explicitly; or (b) restate the first link as external evidence
   authorizing an exact tuple (issuer identity, key fingerprint,
   validity/epoch) that the manifest contains. This is itself the
   kind of hidden join the capstone exists to expose, and must not be
   left to implementation interpretation. Additionally,
   proof-of-possession must be by the **same key** whose signature is
   accepted — an existential self-signature from another key in a
   multi-key manifest does not close the chain (consistent with
   A1.5's rule that the self-signature is never an authority
   channel).
6. **P4's status under the floors, Codex verbatim:** "P4 remains
   correct but incomplete by abstraction, exactly as the Sol handoff
   warned" — the linked-chain rule is a precondition bounding entry
   into the two VALID states, not a change to the verdict function.

## Process notes

- Sequence reaffirmed in the 2026-07-28 session: Amendment 3 →
  assumption-ledger interface → suite scaffold. (Amended 2026-08-07:
  the ledger interface merges into the capstone mechanism spike — see
  `2026-08-07-survivability-mechanisms-ruling.md`.)
- The defend-it-cold essay grows one ruling at a time; this document
  contributes "not meaning but identity."
- Non-author panel review of these rulings: pending; disposition to be
  registered in Amendment 3.

## Tony's notes

This document had its "cold read" and then went through multiple rounds
of adversarial review, and further revision.  Thus, subsequent reads
are not cold reads any longer.

Offered a fork about linkage and counting, I observed that both are viable
and then suggested that Tessera's primary goal shouldn't be to predict
the future well enough to define interpretation of the artifacts and instead
focus on reporting _what was done_ and deferring the decision to some future
reviewer's verification. Why?  Because to me this is about identifying
levels of certainty, and a bad model of the future means pre-decisions here
are inherently unreliable.  By reporting data, we don't have as simple an
answer, but we have one that might survive in the future.

With the current revisions, I accept it as written.  That doesn't mean it is
correct, but it means that it appears to be so now, with the proviso that
issues detected later will require further amendment.
