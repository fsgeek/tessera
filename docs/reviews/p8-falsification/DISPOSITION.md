# P8 falsification review: disposition

2026-10-19. Owner instance (Claude Opus 5.5). Review: `prototype/p8-falsify/REPORT.md` (summary
`CODEX-REVIEW.md` here), verdict **SURVIVED WITH GAPS** (P8F-01 to P8F-04; text defects P8F-05 to P8F-07). No
encoding collision, accepted-decode disagreement or vector defect was found. This disposition records owner
repairs. It is not an author acceptance or registration.

Rules applied: PROOF.md and ENCODING-V1.md are owner texts and were edited (tagged `[OWNER 2026-10-19, P8F-nn]`
in place, with CHANGELOG entries). HYBRID-SUPPLEMENT.md and the prereg and amendments were not edited. No codec
rule, reason code, reason order or vector changed. Claims were narrowed rather than given new mechanism.

## Dispositions

| Finding | Class | Disposition | Where | Evidence |
|---|---|---|---|---|
| P8F-01 Lemma 9 infers equal hashes from signature verification | PROOF-GAP | **NARROW-CLAIM.** Lemma 9 now states only the byte split: `(F, T) ↦ F ‖ T` is injective over valid trailers (final u32 is `6 + h`, `\|T\| = 12 + h`). The inference "same packet verifies over `F'` ⇒ `F' = F` under (H)" is removed, with a note citing the witness and assigning cross-document verification to P1/P3. (H) no longer lists Lemma 9. Remark 10 keeps byte disjointness and drops the key-reuse conclusion. "What is not claimed" gains the bullet. Theorem (ii) cites Lemma 9 only for the split; Theorem (iv) never used it. | PROOF.md CHANGELOG, §2 (H), Lemma 9 and its note, Remark 10, Theorem (ii), §4 "What is not claimed" | Witness unchanged (it shows a property P8 no longer claims): `lemma9` output below. HYBRID-SUPPLEMENT:168 ("PROOF uses (K) only in Remark 10, and Remark 10's argument holds unchanged with message = `F`") stays true: Remark 10 still cites (K), and its byte argument is unchanged. |
| P8F-02 accepted number spellings crash B | PROOF-GAP (implementation) | **Implementation repaired** to match E§1.2. B's `_decimal` no longer calls `int()` on an unbounded exponent: it strips leading zeros and clamps exponents of more than 18 significant digits to ±10^18. That preserves every verdict, because a literal is at most 2^24 bytes, so no nonzero literal with such an exponent is a finite nonzero double (`number()` rejects it before comparing) and zero is decided first. **Owner-found, same class:** implementation A (`gen.py`) crashed on the same inputs, and its direct-decision bound (\|exponent\| > 100000) wrongly rejected value-preserving literals such as `1` + 200000 zeros + `e-200000`; A now uses the same 18-digit bound. No text change. | `formal/p8/vectors/check.py` `_decimal`; `formal/p8/vectors/gen.py` `number_value` | `witness` rerun below; `test_check.py` `test_oversized_exponents` (A and B); I regressions in `test_parsers.py`. |
| P8F-03 first-failing-category order not implemented | PROOF-GAP (implementation) | **Implementation repaired** to match E§1.4 (JSON_ENCODING over the whole input before JSON_SYNTAX). B and A now decode strict UTF-8 first, then reject a leading U+FEFF as `JSON_SYNTAX`. XC-19 (BOM + `{}`) is still `JSON_SYNTAX`. No text change. | `check.py` `parse_text`; `gen.py` `_parse_tree` | `witness` rerun below; the review's campaign rerun: disagreement classes `[]` (was 24 `mutant-ingest` JSON_SYNTAX/JSON_ENCODING), `campaign-rerun.log` here. |
| P8F-04 standalone payload exceeds the size domain | PROOF-GAP (implementation) | **Implementation repaired**: B's `payload_value` and A's `decode_payload` reject more than 2^24 bytes with `LENGTH_CAP` before parsing, as the frame's `payload_length` check already does. **CLARIFY** in E§1.4 stating this for `payload(bytes)`. `LENGTH_CAP` is an existing code, and every frame-path outcome is unchanged. I's generic `parse_json` is left uncapped, as the report allows: I has no standalone payload entry point, and its frame reader enforces the cap. | `check.py` `payload_value`; `gen.py` `decode_payload`; ENCODING-V1 §1.4 | `oversize` rerun below; `test_standalone_payload_cap` (A and B). |
| P8F-05 OpenPGP trailer length understated by six | TEXT-DEFECT | **CORRECT.** E§3.5: the final u32 is `6 + hlen`, the hashed-header length; the trailer is `12 + hlen` bytes; split = final u32 plus six; citation corrected from Lemma 7 to Lemma 9. Lemma 9's proof uses the same corrected statement. | ENCODING-V1 §3.5; PROOF Lemma 9 | `text`: `SIG-01 trailer-length=41 final-u32=35` (41 = 35 + 6). The vector was right; the text was wrong. |
| P8F-06 Lemma 4's coverage sentence uses max | TEXT-DEFECT | **CORRECT.** The clause becomes "the difference falls at a position both headers cover (byte 0, or byte `1 + j < 1 + \|t\| = 1 + \|t'\|`)". | PROOF Lemma 4 | `text`: `header-lengths=(18, 20) … both-cover=False`; the old clause was false, the lemma was not. |
| P8F-07 identifier table gives an attest-only offset | TEXT-DEFECT | **CORRECT.** The canonicalization version is at frame offset `1 + len(tag)`: 18 for attest, 20 for manifest. | ENCODING-V1 §8 table | `text`: `M-01 version-at-offset18=7374 version-at-offset20=0001`. |

PROOF.md's status header now records that the time-boxed falsification ran 2026-10-19 and survived with these gaps,
now repaired.

## Reproduction reruns (after the repairs)

From the repository root, `prototype/.venv/bin/python -B prototype/p8-falsify/targeted.py <cmd>`.

`witness` (P8F-02, P8F-03; relevant lines):

```text
zero-exponent-digits=4300 ingest B=OK I=OK
zero-exponent-digits=4300 payload B=JSON_NONCANONICAL I=JSON_NONCANONICAL
zero-exponent-digits=4301 ingest B=OK I=OK
zero-exponent-digits=4301 payload B=JSON_NONCANONICAL I=JSON_NONCANONICAL
BOM-invalid-UTF8 B=JSON_ENCODING I=JSON_ENCODING
precedence-content-efbbbfff B=JSON_ENCODING I=JSON_ENCODING
precedence-frame-BOM-invalid B=JSON_ENCODING I=JSON_ENCODING
large-exponent-0e-0 B=OK I=OK
large-exponent-1e-0 B=OK I=OK
large-exponent-1e-9 B=JSON_NUMBER I=JSON_NUMBER
```

(Was: `B=CRASH:ValueError` on the 4301-digit and large-exponent lines, `B=JSON_SYNTAX` on the precedence lines.)
The `hybrid-short default B=SIG_FORMAT I=OK` line is unchanged and expected: I's default registry is baseline-only
(REPORT "Scope").

`oversize` (P8F-04):

```text
standalone payload bytes=16777217 cap=16777216 B=LENGTH_CAP I=OK
same-content framed bytes=16777912 B=LENGTH_CAP I=LENGTH_CAP
```

(Was `B=OK`. `I=OK` is I's generic JSON helper, which the report says need not carry the cap.)

`text` (P8F-05 to P8F-07): output unchanged, as expected, because the script measures the bytes, not the prose:

```text
lemma4 header-lengths=(18, 20) asserted-common-covered-prefix=20 both-cover=False
lemma4 first-bytes-differ=True prefix-free-result-still=True
M-01 version-at-offset18=7374 version-at-offset20=0001
SIG-01 trailer-length=41 final-u32=35
```

The texts now state the measured facts: no common-prefix claim, offset `1 + len(tag)`, and trailer = final u32 + 6.

`lemma9` (P8F-01): output unchanged (`frames-distinct=True SHA256-digests-distinct=True left16-equal=True`,
`same-key same-packet B-verifies=[True, True] I/OpenSSL-verifies=[True, True]`). The witness still exists; Lemma 9
no longer claims what it refutes.

`review.py campaign` (rerun with the review's evidence file backed up and restored, so `prototype/p8-falsify/`
is unchanged): 106,185 executions, collision_count 0, disagreement classes `[]`.

## Suites

- `formal/p8/vectors/check.py`: baseline golden 71/71, rejection 173/173, negative controls 5/5; hybrid golden
  35/35, rejection 63/63, negative controls 1/1, gate demonstrations 6/6.
- `formal/p8/vectors/test_check.py` (new; `prototype/.venv/bin/python -B -m unittest discover -s formal/p8/vectors
  -p 'test_*.py'`): 6/6 OK (3 for B, 3 for A).
- `gen.py` regenerated in a scratch copy: `golden.json`, `reject.json`, `hybrid-golden.json` and
  `hybrid-reject.json` byte-identical to the committed files.
- `formal/p8/vectors/fuzz.py`: 60,000 cases, 0 disagreements; hybrid 90,400 cases, 0 disagreements.
- Indep-verifier (`prototype/indep-verifier`, `.venv/bin/python -m unittest discover -s tests`): 112 tests OK,
  including the new `test_p8_falsification_regressions`.
- Differential (`prototype/differential/ADAPTER.md` command, output to a scratch file): `{"AGREE": 352}`, run twice
  (after the B repair and after the A repair). Baseline 352/352.
