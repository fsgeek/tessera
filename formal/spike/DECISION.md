# Tool decision: ProVerif (Tamarin rejected)

Committed per Amendment 1 §A1.4 **before any substantive proof work**.
Switching tools later requires a signed amendment naming the blocker.

## Decision

**ProVerif 2.05** is the symbolic protocol verifier for the Band 0
composition properties (P1–P3, P7 under the A1.3 adversary).

**Rejected alternative: Tamarin 1.12.0.**

## How the decision was made (division of labor, honestly)

The comparison ran the pre-registered spike (SPIKE.md): the same P2
anti-stripping fragment in both tools, correct and deliberately-broken
variants, judged on the three criteria fixed before either model was
written. The recommendation was formed by the AI collaborator (Claude)
on those criteria; the author (Tony Mason) read both correct models cold
and ratified the recommendation without override. Author's criterion-2
assessment, on the record: both models read as reasonable; this was his
first ProVerif model, and it was readable regardless.

## Scoring against the pre-registered criteria

1. **Expressiveness — tie.** Both models state the fragment in ~100
   lines with no contortions. Tamarin needed one `restriction` to pin
   single-issuer; ProVerif got it structurally. Neither hand-encoded
   anything unnatural.
2. **Author-readability — roughly a tie.** The author can read and
   contest both. Tamarin's multiset-rewrite rules sit closer to the TLA+
   state-machine idiom he already owns; ProVerif's applied pi calculus
   was new to him and still readable on first contact.
3. **Counterexample quality — edge to ProVerif, and the tie-breaker.**
   ProVerif's attack derivation is a numbered prose narrative, readable
   unaided in the committed `.out` evidence file
   (`proverif/p2_commitment_broken.out`). Tamarin's falsification is a
   constraint-solving proof script, opaque cold; its graphical trace
   explorer is good but requires running an interactive server. For a
   project whose evidence must speak from the repository, the
   self-explanatory counterexample wins.

Explicitly NOT criteria, per SPIKE.md: proof speed (both ~1–2s here),
whether the property verified (both tools verified the correct model and
falsified the broken one — no tool-shopping signal exists in this
comparison), and tool fashion.

## Context recorded, not counted

The author noted that recent TEE verification work also uses ProVerif —
reassuring ecosystem depth, but "who else uses it" is not one of the
three pre-registered criteria, so it is recorded here as context and was
not a deciding reason. (Flagged by the AI collaborator under A1.4's own
anti-tool-shopping discipline.)

## Consequences

- All symbolic lemmas for P1–P3/P7 are written in ProVerif, each with a
  prose mapping to its A1.2 property (A1.4 obligation).
- The cross-model correspondence mapping (A1.4) runs between the TLA+
  specs and the ProVerif models.
- Tamarin remains installed (`~/.local/bin/tamarin-prover`) and its
  spike artifacts remain committed as the comparison evidence; it is not
  used for proof work absent a signed amendment.
