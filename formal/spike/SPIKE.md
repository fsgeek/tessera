# Tool spike: Tamarin vs. ProVerif (bounded, pre-proof)

Governed by Amendment 1 §A1.4: this spike compares the two symbolic
verifiers **only on expressiveness and author-readability** for the
composition properties (P1–P3, P7) under the A1.3 adversary — explicitly
*not* on which tool proves the desired result. The choice, the rejected
alternative, and the reason are committed in `DECISION.md` before any
substantive proof work begins. Switching later requires a signed
amendment.

## The fragment

Both tools model the **same minimal fragment**, chosen because it is
small, has a real adversary move, and exercises exactly the modeling
idioms the full work will need:

**P2 (anti-stripping), minimal form.** An issuer signs a package whose
signed bytes commit to a required-signer manifest {K_kms, K_gpg}. The
adversary may strip either signature and re-present the package — both
directions are modeled (strip KMS → present as gpg_only, strip GPG →
present as kms_only). The verifier must not accept any package presenting
fewer signatures than its committed manifest requires. Rejection is
modeled as **non-acceptance** (the standard symbolic-tool idiom); the
typed verdict partition of P2/P4 (`INVALID` vs `UNVERIFIABLE`) is a
state-machine concern assigned to TLA+ by A1.4, and is deliberately not
part of this fragment.

This fragment forces each tool to express: (1) signed messages whose
*content includes the expected-signer set*, (2) an active adversary that
decomposes and re-assembles messages, (3) a verifier decision rule keyed
on the committed manifest — the three idioms P1/P3/P7 also need.

**Model alignment (apples-to-apples).** The two candidates model the
*same* system: a single issuer (Tamarin: `single_issuer` restriction;
ProVerif: one top-level keypair), three manifests (`both`, `gpg_only`,
`kms_only`), the same acceptance paths, and the same correspondence
property. Divergence between the models is a spike defect, not a tool
difference.

## Judging criteria (fixed before either model is written)

1. **Expressiveness:** can the fragment be stated without contortions
   (hand-encoded sets, unnatural role splitting, lossy abstraction)?
2. **Author-readability:** can Tony read the model and the tool's output
   well enough to *contest* it — the agreement-gate requirement? Judged
   by Tony reading both cold and writing one paragraph per tool.
3. **Trace quality:** when the property is deliberately broken (remove
   the manifest commitment), does the tool produce a counterexample trace
   a human can follow?

Explicitly NOT criteria: proof speed, whether the property verifies,
tool fashion.

## Toolchain status (2026-07-04)

- Tamarin 1.12.0: `~/.local/bin/tamarin-prover`, self-test passing
  (maude + graphviz via apt).
- ProVerif 2.05: `~/.local/bin/proverif`, built from source without the
  GTK GUI (the opam package hard-requires lablgtk/root; source build is
  the no-root path).
- TLC (TLA+): installed (`~/.local/share/tla/tla2tools.jar`, via java).
- Lean4: installed (elan).

## Review log

- 2026-07-04, Codex: three findings against the first-cut models
  (asymmetric stripping coverage; INVALID-vs-non-acceptance wording;
  issuer-cardinality mismatch between candidates), all confirmed and
  incorporated; Codex independently reproduced both tools' runs.
  Artifact: `docs/reviews/2026-07-04-codex-spike-review.md`.
