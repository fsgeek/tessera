# Mutation testing of V1 verification: search for false accepts (independent verifier), 2026-10-14

Saved by the owner from the run agent's final report; the harness blocked the agent from writing it. The per-id
list is in `valid_strict.tsv` and the index in `valid_strict_index.md`. Reproduce with `mutate.py --count`,
`campaign.py --jobs 12` (resumable, about 3.5 h), `summarize.py`, `classify.py`; emit a single mutant with
`mutate.py --emit <op>/<seed>/<n> --out FILE`.

| | |
|---|---|
| Mutants (52 VALID_STRICT seeds × 7 operators) | 253,363 |
| VALID_STRICT | 4,503, all class A (benign) |
| INVALID / UNVERIFIABLE | 242,073 / 6,787 |
| (B) false accepts | **none** |
| Robustness (crash, timeout, non-six-field output, nonzero exit, stderr) | **none**; slowest 3.1 s |

Operators: op1 bit flips in every byte of A_sig, manifest, possession and git signature (129,294); op1x sampled
flips in all other members (67,629); op2 member swaps across seeds and foreign keys (14,433); op3 evidence
transplants (dns, git, receipt OTS, header pools; 14,648); op4 structural changes (drop, duplicate, reorder,
unknown members, re-encoding, OTS-internal; 21,535); op5 semantic edits unsigned, attacker-re-signed and fully
attacker-re-keyed (4,212, **0 VALID**); op6 targeted signature malleation (1,612).

The benign classes (claim bytes a_sig/manifest/keys unchanged, all OTS file digests unchanged, snapshot, commit and
blob unchanged, T unchanged):
- A1 `issuer_record` (340): unsigned diagnostics (P§2.1).
- A2 possession-signature malleation (2,095): unhashed area ignored, low-s not required (P:899-900); each mutated
  possession signature re-verified with gen.py (2,095/2,095). The same malleations inside A_sig were rejected
  (RECEIPT_ANCHOR_MISMATCH).
- A3 OTS bytes for the same digest with T unchanged (2,033): pending branches, unheadered attestations, duplicate
  branches (P:795, P:1250, P:1259).
- A4 header pool with T unchanged (35): unused pinned headers (P:827, P:832).

Observations, with owner actions:
1. A VALID_STRICT bundle is not byte-unique: anyone can rewrite A1–A4 bytes with no key. **Owner:** the profile
   states that a receipt's identity is SHA256(A_sig), not the bundle hash, and that "keep the exact bytes"
   custody (P:195) means the claim-bearing bytes.
2. Possession signatures are the only signature bytes not protected by a stamp, by design (P:899-900).
3. A fully attacker-re-keyed receipt stops at RECEIPT_ANCHOR_MISMATCH, so this campaign cannot show that the
   later authority rows (15.1, DNSSEC, git signer) reject a re-stamped attacker receipt on their own. **Owner:**
   add conformance cases where the attacker re-stamps consistently and fails only at authority.
4. Two op4 labels say "headered height" where the height had no bundled header; one mutant labelled "header
   height key as JSON number" is invalid JSON, so OUT_OF_PROFILE is expected.

Limitations: only the independent verifier was exercised; op1x, op2b and the op4 sibling drops are sampled; op1 flips
one seeded bit per byte; no mutant carries a fresh valid OTS, DNSSEC or repository signature, because trust and
release were held fixed.
