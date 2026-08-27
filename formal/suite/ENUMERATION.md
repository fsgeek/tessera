# Symbolic suite enumeration — per-property models, ledgers, capstone

> **STATUS: PROPOSED — clerk-drafted 2026-08-17, not adopted.** Drafted
> under the author's delegation of sequencing (2026-08-16, in session:
> the author asked the AI collaborator to choose the next work item;
> the choice of *this* work is therefore the collaborator's decision,
> on the record as such). Nothing in this document carries authority.
> It enumerates; it does not register. Predictions for every model are
> registered separately, per-model, before that model first runs — this
> document deliberately contains **no predictions**, so that reading it
> cannot contaminate a later predictions freeze. Adoption of the
> enumeration (that this is the right set of models) is an author
> decision after cold read.

Discharges toward: A3 §A3.3 (per-property models over a shared theory
library; assumes-from-elsewhere ledgers; the capstone composition
context gating Band 0 exit) and the open `PROPERTIES.md` checkboxes for
the symbolic-suite architecture, the per-lemma prose mapping, and the
TLA+ ↔ symbolic correspondence mapping.

## Inputs this enumeration is built from

- A3 §A3.3 registered obligation text (adopted `8ae4720`).
- The first-link spike (`formal/spike/first-link/`, decision entered
  `459aff0`): its models are the seed of the shared theory library and
  its ledger entries are the first population of the conservation
  schema.
- DECISION.md rulings: transcription binding selected; direct and
  digest forms with distinct domain tags (`STMT_DIRECT`/`STMT_DIGEST`);
  signed nonempty required set; cross-form substitution negative
  control gated to P7/P8 before a second form is implemented; standing
  tests S1–S3 with mandatory distinct reason codes and a collapsing
  negative control.
- `PROPERTIES.md` tool assignments (authoritative statements live in
  the amendments).

## 1. Shared theory library

One file, `formal/suite/lib/tessera_theory.pvl`, extracted from the
spike models — extraction, not invention; divergence from the spike's
declarations is a defect unless recorded:

- signature primitives (`sign`/`checksign`/`pk`), fingerprint `fp`;
- free constructor `h` **with its idealization stated in the header**
  (injective in the symbolic model; erases encoding ambiguity and
  concrete collision behavior — the Layer 2 residual every consumer
  ledger entry must cite, per spike ledger entry 5);
- domain-separation tags: `POSS`, `BYTES`, and per DECISION.md the
  form-distinct `STMT_DIRECT`/`STMT_DIGEST` replacing the spike's
  single `STMT` (the spike's single-form tag was ruled harmless
  in-spike and insufficient the moment both forms are legal);
- the map-v1 authority-relevant tuple constructor;
- the five event kinds with two authority-publication branches (the
  author's ratified phrasing).

Every model in the suite includes this library and adds only its own
process structure, events, and queries. A model redeclaring a library
term is a build failure.

## 2. Per-property models

Per `PROPERTIES.md`, the properties with a ProVerif obligation are P1,
P2, P3, P7 (P10's symbolic content — the first link — was discharged by
the spike; its TLA+ manifest-authority model is out of scope here).
Each model ships with: header stating "This model proves… / does not
prove…" (author's registered suggestion, DECISION.md remediation 5);
per-lemma prose mapping to the registered property; an
assumes-from-elsewhere ledger block in A3.3 conservation-field form; at
least one broken companion that must go red on a named query.

- **S-P1 — integrity (headline, operative form).** The A3.1.2
  corrected claim: no transition reaches an accepted receipt over
  altered bytes. Symbolic leg complements the TLA+ leg (state logic
  stays in P4's model). Companion: bytes-substitution must break
  acceptance. Expected ledger: consumes key-binding from S-P3;
  exposes hash/encoding Layer 2 residuals.
- **S-P2 — signature-set completeness.** Acceptance implies every
  required signer signed the exact framed bytes; the required set is
  itself signed (the DECISION.md required-set grammar, applied to
  signers). Companion: drop one required signature → red; forge one →
  red. Expected ledger: consumes P8's canonical-encoding assumption
  (Layer 2 until P8's proof exists — then cites the proof, never
  silently absorbs it).
- **S-P3 — key binding, anti-DSKS.** The accepted key is bound into
  the signed object such that no key-substitution preserves
  verification. This is the suite's producer for the fingerprint
  relation the spike's models *consumed* (only `kfpr` is compared —
  author finding, criterion 2 qualification). Companion: DSKS-style
  re-attribution must be exhibited against the broken form.
- **S-P7 — wrapper/object-type soundness.** Wrapping does not re-scope
  identity or authority: standing binds to innermost issuance
  identity; a wrapper cannot re-scope it (the transplant threat named
  in the Kimi-2 discussion — the *targeted* piece lives here; the
  integrated lifecycle model remains a separate post-spike obligation
  gating the H1a freeze, NOT part of this suite). Companions:
  re-serialization attack (Antigravity's P7 finding, now mechanized);
  and — **gated: build only before any second binding form is
  implemented** — the cross-form substitution negative control
  (DECISION.md: a `STMT_DIGEST` binding read as `STMT_DIRECT` must
  fail).

**Standing tests S1–S3** (DECISION.md exit condition 3) are
conformance-vector obligations with reason codes, not symbolic
queries; they enter the suite only through S-P7's identity-binding
claims. Their collapsing negative control (S2/S3 same reason code must
fail discrimination) is a vector-level check and stays with P8/H1a
vectors. Recorded here so the suite is not later blamed for not
containing them.

## 3. Capstone composition context

One model, `formal/suite/capstone.pv`, transcribing the shared library
(the non-binding candidate registered in A3.3, now exercised by the
spike at representative complexity and selected by that evidence):

- **Linkage query proves the §A3.2 chain — the links, not just
  cardinalities, per layer** (A3's registered addition). The spike's
  Q1 recut is the first link's form; the capstone extends the
  correspondence through possession, signing, and acceptance with the
  shared terms crossing every join.
- **Every ledgered cross-model assumption** in the per-property models
  is discharged by a machine-checked producer query here or in the
  producing model, **and carries a broken companion that fails the
  query consuming the severed link** — the A3.3 gate text, verbatim
  in force. The discharge matrix (consumer entry → producer query →
  severing companion → expected red) is an appendix of this file once
  the models exist; it cannot honestly be written before them.
- **Layer 2 assumptions are enumerated, exposed, unclaimed** — the
  standing list from the spike: concrete hash resistance (digest
  form), canonical encoding pre-P8, historical trust-anchor
  correctness, chain availability, implementation fidelity,
  operational channel independence (n = 2 enumeration does not
  generalize — author finding 7 wording).

## 4. Cross-formalism joins (TLA+ ↔ symbolic)

ProVerif cannot consume a TLA+ result. Per A3.3 these joins are ledger
entries whose producer field names the TLA+ model and invariant, with
the shared term stated and the correspondence carried in the written
proof (the open `PROPERTIES.md` mapping checkbox). Known joins to
carry: temporal validity (producer: P5c/A2.1 `confirmed_at` predicate,
bridge-checked) consumed wherever a symbolic model assumes "anchor
valid"; refusal/standing state (producer: P5c refusal latch) consumed
by S-P7's standing claims. These entries are **never** marked
discharged by a symbolic query — mislabeling a cross-formalism join as
symbolically discharged is exactly the checkmark-relay defect (Sol
finding 2) and should be treated as a red-bar condition on review.

## 5. Discipline (unchanged, restated to bind this work)

Per-model, in order, before any run: predictions registered and frozen
(separate file per model, spike pattern); per-query timebox declared;
three named outcomes (violation = counterexample; timeout = mechanism
failure, not property evidence; termination = evidence for the checked
abstraction only). Broken companions red on exactly the named queries;
green isolation configs where the spike used them. Author cold read of
correct models precedes any ratification. Amend-don't-rewrite applies
to this file from its first commit.

## 6. Sequencing (clerk judgment, contestable)

S-P3 first (most-consumed producer; smallest model), then S-P1, S-P2,
S-P7, then the capstone last — the capstone composes chosen, checked
models, mirroring the placement argument that kept the Kimi-2 model
off the Band 0 gate. P8 proceeds in parallel on its own track ([proof]
+ golden vectors; A3.6 places it before Band 0 exit); S-P2's ledger
cites it either way.

## Amendment note 1 — 2026-08-27 (clerk; PROPOSED; amend-don't-rewrite)

Two findings from `formal/spike/first-link/READ-AND-CHALLENGE.md`
(author-side, non-discharging) bear on §2 above. The text above is
left as written; this note records what a cold read should weigh.

1. **S-P7's cross-form substitution companion cannot go red in
   ProVerif.** A scratch model with the *shared* `STMT` tag — repository
   publishes digest form, verifier reads direct form — reports `Accept`
   unreachable (guide appendix M5): `h(t)` and a five-tuple are distinct
   constructors and no pattern confuses them, tag or no tag. A symbolic
   companion for this control is therefore green for a reason unrelated
   to the tag ruling — the "companion that could not fail" pattern. The
   control is byte-level and belongs with P8's golden vectors. Proposed
   disposition: strike it from S-P7's companion list and record it as a
   P8 vector obligation, leaving DECISION.md's routing ("P7/P8") intact
   with the P8 half now the operative one.

2. **S-P3 must model registration, not only verification.** In every
   correct spike model the verifier's possession check is unexercised
   (guide headline; appendix M1): the `IssuerPossession` conjunct is
   discharged by the honest issuer firing the event before signing, and
   the check rejects nothing. What the spike "consumed" from S-P3 was an
   algebra in which DSKS is unrepresentable plus issuer honesty — not a
   producer query. For S-P3 to be a producer in the §A3.3 sense it must
   (a) model the authority channel publishing `fp(k)` only on a
   possession proof under `k`, with an adversary attempting to register
   a key it does not hold; (b) carry a companion where registration
   omits that demand, red on a key-substitution query; (c) extend the
   signature theory so key substitution is expressible; (d) carry the
   multi-key manifest case of A3.2 item 3. §2's S-P3 entry above is
   consistent with this but underspecified; the four items are what
   "producer for the fingerprint relation" has to mean.

Neither finding touches `459aff0`, criterion 0, or the selection of
transcription binding. Both are routed to the author with this note.

## Open questions routed to the author (none block drafting S-P3)

1. Adoption of this enumeration as the suite's scope (cold read).
2. Whether S-P1's symbolic leg may narrow to what the TLA+ leg does
   not already carry (scope ruling; affects S-P1 only).
3. Confirmation that standing S1–S3 vectors are H1a/P8-track artifacts
   rather than suite obligations (this document's assumption; stated
   in §2 and reversible without rework before S-P7 exists).
