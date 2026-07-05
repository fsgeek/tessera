# Review: Band 0 tool-spike models (P2 fragment), Codex

Review artifact for the A1.4 tool-spike working material
(`formal/spike/`), kept under the same archive-and-disposition discipline
as the A1.7 pre-registration reviews. Reviewer: Codex (OpenAI), the
project's designated adversarial-test author per §4.5 of the original
pre-registration — here reviewing spike models, not authoring the H1a
suite. Date: 2026-07-04. The reviewer independently reproduced both
tools' runs locally before reporting.

## Disposition summary (author + AI collaborator, 2026-07-04)

1. **Asymmetric stripping coverage (Medium) — confirmed, fixed.**
   SPIKE.md promised "strip either signature"; the models only exercised
   strip-KMS-present-gpg_only. The symmetric case is isomorphic, but
   "isomorphic, trust me" is a shortcut this project does not take. All
   four models now carry a `kms_only` issuance path, verifier path, and
   (correct models) reachability lemma/query. Re-run: correct models
   verify with all three acceptance paths reachable; broken models still
   falsified.
2. **INVALID vs non-acceptance (Medium) — confirmed as a SPIKE.md wording
   defect, not a model defect.** The typed verdict partition (`INVALID`
   vs `UNVERIFIABLE`) is P4's state-machine concern, assigned to TLA+ by
   Amendment 1 §A1.4's tool split; in the symbolic fragment, rejection is
   modeled as non-acceptance (the standard idiom). SPIKE.md and both
   correct models now say this explicitly instead of borrowing P2's
   verdict vocabulary loosely.
3. **Issuer-cardinality mismatch (Low) — confirmed, fixed.** Tamarin's
   `Register_Issuer` fired unboundedly while ProVerif created one
   keypair, weakening the apples-to-apples comparison. Tamarin now pins
   registration to a single firing (`single_issuer` restriction); a
   model-alignment section in SPIKE.md makes the parity requirement
   explicit.

## Full review text (verbatim)

Findings

- Medium: The spike objective says the adversary may strip either
  signature, but both models only exercise the downgrade to gpg_only.
  There is no kms_only manifest, issuance path, verifier path, or
  reachability/property coverage. See
  formal/spike/tamarin/p2_commitment_correct.spthy:48 and
  formal/spike/proverif/p2_commitment_correct.pv:52. This tests "strip
  KMS, present GPG-only," but not "strip GPG, present KMS-only," despite
  formal/spike/SPIKE.md:19.

- Medium: The objective says the verifier must reject as INVALID, but the
  models only prove non-acceptance via correspondence. There is no
  Invalid/Rejected event or query showing that a concrete stripped
  package is classified invalid. See the Tamarin accept-only verifier
  rules at formal/spike/tamarin/p2_commitment_correct.spthy:57 and the
  ProVerif accept-only processes at
  formal/spike/proverif/p2_commitment_correct.pv:57. If "invalid" is just
  shorthand for "not accepted," this is fine; if it is an observable
  verifier decision, it is under-modeled.

- Low: The two "same fragment" models differ on issuer cardinality.
  Tamarin's Register_Issuer can run unboundedly, while ProVerif creates
  one keypair in the top-level process. See
  formal/spike/tamarin/p2_commitment_correct.spthy:30 versus
  formal/spike/proverif/p2_commitment_correct.pv:68. This probably does
  not invalidate P2 here, but it weakens the apples-to-apples
  readability/expressiveness comparison.

I ran both target files locally: tamarin-prover --prove verifies all
three Tamarin lemmas, and proverif verifies the correspondence while the
two reachability sanity queries fail as intended.
