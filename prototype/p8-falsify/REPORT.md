# Independent P8 proof review and falsification

2026-10-19. Reviewed the working-tree `formal/p8/PROOF.md`, the 2026-10-19
`ENCODING-V1.md`, and the registered hybrid supplement. The governing obligation
is A9.2, `docs/phase-0-prereg-amendment-9.md:203–208`. This report does not record
an author acceptance, registration, or discharge.

**Result:** no distinct accepted structures with identical canonical, frame, or
`A_sig` encodings were found. No successful decode produced different values or
different ordered anchor tuples in the two codecs under the same installation
registry. The framing/injectivity arguments survive. The unrestricted signature
binding claim in Lemma 9 is false, and the implementation evidence has three
additional conformance gaps. Three small text defects are also recorded below.

The search had a 20-minute ceiling, beginning at 20:46 UTC. The tests completed
within that ceiling; commands, logs, witnesses, and input hashes are here. All
files created by this review are under `prototype/p8-falsify/`. No existing
repository file was edited. The shared workspace also received unrelated changes
during the review; this report makes no claim to have tested those changes.

## Scope and reproduction

`B` means `formal/p8/vectors/check.py`; `I` means
`prototype/indep-verifier/codec.py`. Differential anchor tests pass
`I.registered_codecs(I.HYBRID_ALG)` explicitly. The baseline-only default in I
intentionally treats an uninstalled hybrid identifier as opaque; comparing that
default against B's compiled hybrid registry would manufacture a discrepancy.
This is confirmed by `docs/V1-PROFILE.md:977–982` and the call in
`prototype/indep-verifier/verify.py:173–176`.

Runtime: Python 3.14.6, Unicode 16.0.0, cryptography 50.0.2, rfc8785 0.1.4,
Hypothesis 6.170.2, Node v20.20.2. `inputs.json` records the reviewed artifacts'
SHA-256 values and Git HEAD. These are working-tree artifacts, including existing
uncommitted edits, rather than an assertion that HEAD contains the reviewed text.

Run from `/home/tony/projects/tessera`:

```sh
UV_CACHE_DIR=prototype/p8-falsify/.uv-cache uv pip install --python prototype/.venv/bin/python --target prototype/p8-falsify/deps hypothesis==6.170.2
prototype/.venv/bin/python -B prototype/p8-falsify/review.py probes
HYPOTHESIS_STORAGE_DIRECTORY=prototype/p8-falsify/.hypothesis prototype/.venv/bin/python -B prototype/p8-falsify/review.py properties
prototype/.venv/bin/python -B prototype/p8-falsify/review.py campaign
prototype/.venv/bin/python -B prototype/p8-falsify/review.py numbers
prototype/.venv/bin/python -B prototype/p8-falsify/targeted.py witness
prototype/.venv/bin/python -B prototype/p8-falsify/targeted.py lemma9
prototype/.venv/bin/python -B prototype/p8-falsify/targeted.py boundaries
prototype/.venv/bin/python -B prototype/p8-falsify/targeted.py oversize
prototype/.venv/bin/python -B prototype/p8-falsify/targeted.py text
prototype/.venv/bin/python -B prototype/p8-falsify/exhaustive.py
```

The supplied vector checker was also run read-only:

```sh
prototype/.venv/bin/python -B formal/p8/vectors/check.py
```

No vector generator was run: it would write files outside the authorized directory.
No service, signing key, network authority, OTS service, or live chain was used.

## Findings

### P8F-01 — PROOF-GAP: Lemma 9 infers equal hashes from signature verification

**Exact location:** `PROOF.md:320–328`, especially 325: “If … differs … a hash
match is a collision.” Verification by the same ECDSA packet does not establish
that hash match. This also limits the signature-reuse implication in Remark 10
(`PROOF.md:339–341`); different message bytes alone do not prove signature
separation under only assumption H.

There is an actual SHA-256/OpenPGP witness, not merely a hypothetical pair of
digest values. Two different codec-accepted attestation frames have different
SHA-256 digests of `F || T` with the same first 16 bits. One rule-O packet verifies
over both under one chosen P-256 public key, including I's signature policy.

Reproduce:

```sh
prototype/.venv/bin/python -B prototype/p8-falsify/targeted.py lemma9
```

Output:

```text
lemma9 actual-frame witness: attempts=195 indices=(114, 194)
frames-distinct=True SHA256-digests-distinct=True left16-equal=True
same-key same-packet B-verifies=[True, True] I/OpenSSL-verifies=[True, True] sig-policy=OK
F0/F1 codec B=OK/OK I=OK/OK
digest0=67c0a82553460d29163acd32374032434e0ec725c4be64909da5e7b784b88f4d
digest1=67c0c2f2e0361ca224f296d2a5cadec3808453a94b47325d555d0e20b30b5d3d
The chosen key does not match the frames' illustrative key_fp; no complete receipt is claimed.
```

Construction: let `r = x(2G) mod n`, let `z0,z1` be the actual digest integers,
choose `d = -(z0+z1)/(2r) mod n`, and set `s = (z0+rd)/2 mod n`.
Verification's points are `2G` and `-2G`, with the same x coordinate. A 16-bit
prefix birthday search supplies the OpenPGP left-16 requirement. Exact frames,
packet and public key are saved in `lemma9-witness.json`.

**Scope:** this refutes Lemma 9 as written, which has no prior honest-key or
frame-fingerprint condition. It is not a complete accepted receipt: the chosen
key is not bound by the illustrative fingerprint. It is not a SHA-256 collision,
nor an encoding collision: the two frames and their anchor encodings are distinct.
Lemmas 3, 5 and 7 need no signature verification assumption. Repair requires
restricting Lemma 9 to the injective `F || T` representation argument, or stating
and justifying an additional cryptographic binding assumption with precise key
and adversary conditions. Collision resistance alone is insufficient.

### P8F-02 — PROOF-GAP: accepted number spellings can crash B

**Exact locations:** `ENCODING-V1.md:139–146` accepts value-preserving spellings,
including arbitrary-exponent positive zero; `PROOF.md:188–191` asserts that
ingestion changes spellings only. `PROOF.md:96–97` asserts exact decoder-domain
and rejection-code conformance. B's `_decimal`, `check.py:218–227`, converts the
entire exponent to a Python integer without handling its digit limit.

Reproduce:

```sh
prototype/.venv/bin/python -B prototype/p8-falsify/targeted.py witness
```

Relevant output:

```text
zero-exponent-digits=4300 ingest B=OK I=OK
zero-exponent-digits=4301 ingest B=CRASH:ValueError I=OK
zero-exponent-digits=4301 payload B=CRASH:ValueError I=JSON_NONCANONICAL
large-exponent-0e-0 B=CRASH:ValueError I=OK
large-exponent-1e-0 B=CRASH:ValueError I=OK
large-exponent-1e-9 B=CRASH:ValueError I=JSON_NUMBER
```

The first crashing input is exactly `b'0e' + b'9'*4301`, 4,303 bytes, far below
the payload cap. Also accepted by the text but crashing B are `0e` and `1e`
followed by 4,301 zeros. This is an uncaught `ValueError`, not a declared P8
rejection. The threshold is the tested runtime's default integer digit limit.

**Scope:** an accepted ingestion input is missing from B's supported input
domain. Its canonical value is ordinary zero or one; no canonical encoding
collision follows. The existing huge-exponent vectors do not reach this limit.

### P8F-03 — PROOF-GAP: the declared first-failing-category rule is not implemented

**Exact locations:** `ENCODING-V1.md:199–211` requires checking all UTF-8 before
JSON syntax; `PROOF.md:96–97` asserts conformance with the stated codes. B checks
the BOM in `check.py:207–210` before decoding UTF-8.

Reproduce:

```sh
prototype/.venv/bin/python -B prototype/p8-falsify/targeted.py witness
```

Relevant output:

```text
precedence-content-efbbbfff B=JSON_SYNTAX I=JSON_ENCODING
precedence-frame-BOM-invalid B=JSON_SYNTAX I=JSON_ENCODING
```

The four-byte ingestion witness is `ef bb bf ff`. The final `ff` is invalid
UTF-8, so the text requires `JSON_ENCODING`. The second case puts a BOM and
invalid trailing UTF-8 into an otherwise schema-valid frame payload and updates
its length, demonstrating the discrepancy through the signed-frame decoder too.
The randomized campaign independently found 24 instances of this discrepancy.

**Scope:** both reject. There is no differing accepted value, frame boundary,
or anchor tuple. This is a failure of rejection-code agreement, not injectivity.

### P8F-04 — PROOF-GAP: standalone payload acceptance exceeds the stated size domain

**Exact locations:** `ENCODING-V1.md:134–135,195–197` defines the payload cap and
standalone `payload(bytes)` entry point; `PROOF.md:159–163,177–186` claims that
payload acceptance is exactly canonical values “within the limits”. B's
`payload_value`, `check.py:358–362`, has no size check. I's generic JSON helper
also has no payload-size check; its frame wrapper supplies it.

Reproduce:

```sh
prototype/.venv/bin/python -B prototype/p8-falsify/targeted.py oversize
```

Output:

```text
standalone payload bytes=16777217 cap=16777216 B=OK I=OK
same-content framed bytes=16777912 B=LENGTH_CAP I=LENGTH_CAP
```

The standalone input is exactly `b'"' + b'a'*(2**24-1) + b'"'`. It is canonical,
but exceeds the accepted payload domain by one byte.

**Scope:** the “only if, within limits” statement does not describe the concrete
standalone payload helper. The whole-frame accepted domain remains correct:
both frame decoders enforce the limit before parsing. This can be resolved by
enforcing the cap at the documented payload entry point or explicitly qualifying
the implementation claim as acceptance through the frame wrapper. I's generic
JSON helper also serves non-payload uses and need not itself acquire that cap.

### P8F-05 — TEXT-DEFECT: the OpenPGP trailer length is understated by six bytes

**Exact locations:** `ENCODING-V1.md:368–372`; `PROOF.md:326–328`. The last u32
contains `6 + hlen`, the hashed signature-header length, whereas the full suffix
`T` has length `12 + hlen`. ENC also cites Lemma 7 here; the trailer argument is
in Lemma 9.

Reproduce:

```sh
prototype/.venv/bin/python -B prototype/p8-falsify/targeted.py text
```

Relevant output:

```text
SIG-01 trailer-length=41 final-u32=35
```

**Scope:** suffix recovery still works by taking the final u32 **plus six**.
Equality of the final u32 still implies equal trailer lengths, so the suffix
split argument survives this wording error. The separate signature-verification
inference does not survive, as P8F-01 shows. SIG-01 matches the displayed byte
formula; the vector is not defective.

### P8F-06 — TEXT-DEFECT: Lemma 4's final coverage sentence uses max incorrectly

**Exact location:** `PROOF.md:196–198`, “first `1 + max(...)` bytes, which both
headers cover.” Headers of unequal lengths do not both cover that prefix.

Reproduce:

```sh
prototype/.venv/bin/python -B prototype/p8-falsify/targeted.py text
```

Relevant output:

```text
lemma4 header-lengths=(18, 20) asserted-common-covered-prefix=20 both-cover=False
lemma4 first-bytes-differ=True prefix-free-result-still=True
```

**Scope:** the two preceding cases prove the lemma: unequal lengths differ at
byte zero; equal lengths differ within their common extent. Delete the final
coverage clause or use a common covered prefix. The prefix-free result is sound.

### P8F-07 — TEXT-DEFECT: the identifier table gives an attestation-only offset

**Exact location:** `ENCODING-V1.md:794` says canonicalization version is at
“frame offset 18.” A manifest's 19-byte tag puts this field at offset 20.

Reproduce:

```sh
prototype/.venv/bin/python -B prototype/p8-falsify/targeted.py text
```

Relevant output:

```text
M-01 version-at-offset18=7374 version-at-offset20=0001
```

**Scope:** the general frame formula, manifest vector, and both decoders agree.
Qualify the table entry by frame type, or state offset `1 + len(tag)`.

## Step-by-step proof audit

| Step and exact proof lines | Does it follow? |
|---|---|
| Domain and equality, 48–94 | Yes for typed JSON values, objects as maps, signatures as exact byte strings. Boolean true is not number one. Receipt equality includes signatures. This is not injectivity on JSON source texts or transport bundles. |
| Decoder characterization, 96–97 | Abstractly follows from the intended checks; not established for the concrete helper entry points and all declared codes: P8F-02, P8F-03, P8F-04. |
| Assumptions, 101–120 | N supplies numerical round-trip correctness; U determines acceptance. H belongs to computational binding, not the framing proof. The hybrid supplement explicitly replaces K for its raw slot. H alone does not establish Lemma 9. |
| Lemma 1 scalar escaping, 126–141 | Yes. Escapes invert scalar by scalar; controls cannot introduce an unescaped quote; strict UTF-8 and JSON escape parsing determine the closing quote. Empty strings also work. |
| Lemma 2(a), 150–151 | Yes for ECMAScript's specified decimal spelling, including zero and exponent signs. |
| Lemma 2(b), 152 | Yes, directly from N. |
| Lemma 2(c), 153–155 | Yes: applying the accepted-number rule to ES(d) gives the same finite d and the same exact decimal spelling/value. This is about canonical number tokens, not the completeness of B's ingestion parser for all alternative spellings. |
| Lemma 2(d), 156–157 | Yes. End, comma and closing brackets cannot extend a JSON number. |
| Lemma 3 induction, 165–175 | Yes. Typed literal/string/number bases and the array/object separators give a left inverse. Sorting is deterministic and map order is not part of equality. |
| Lemma 3 acceptance iff, 177–186 | Yes for an abstract decoder that enforces the limits. The concrete standalone helper does not enforce the size limit: P8F-04. Depth/size qualifications must remain attached to acceptance, rather than unrestricted parsing of arbitrary trees. |
| No-normalization remark, 188–191 | Correct for accepted canonical bytes and value-preserving ingestion. Operational completeness of ingestion has the P8F-02 exception. |
| Lemma 4, 193–202 | The case split proves prefix freedom and type separation. Its last coverage sentence is false but unnecessary: P8F-06. |
| Lemma 5 first identity, 204–227 | Yes. Tag/version/length fix all envelope boundaries; the supplied canonical payload passes its schema. All accepted frame lengths fit u32. |
| Lemma 5 second identity, 229–231 | Yes. Canonical reserialization, checked fixed fields and exact remaining length reproduce every byte. |
| Lemma 6(a), 233–245 | Yes. The closed schema puts common first; payload begins at 24, common at 34. Equality of JCS(common) implies value equality by Lemma 3. |
| Lemma 6(b,c), 246–253 | Yes for slot-specific acceptance/receipts. The distinct fingerprint prefixes are in the bytes, and manifest linkage fixes their slots. A generic attest decoder does not by itself check receipt slot placement. |
| Lemma 7a length gates, 259–269 | Yes: nonempty, capped and exactly extracted slot bytes. |
| Lemma 7a rule O, 270–281 | Yes. Old-format shortest header, explicit subpacket-area lengths and MPI bit counts determine all extents; exact consumption rejects extensions and second packets. This does not make signature serializations unique across all signer's choices, which are exact bytes in the domain. |
| Lemma 7a R/opaque, 282–290 | Yes. Registered ML-DSA is length-only at codec level; opaque is a nonempty bounded byte string. Internal ML-DSA malformations belong to verification. The supplement makes this explicit. |
| Lemma 7, 292–311 | Yes. The count, ordered length prefixes, and exact sub-decodes give a left inverse and exact re-encoding. Each slot's rule depends only on its preceding frame and slot position. No assumption of equal algorithms/common values is needed for Anc; the receipt checks impose those separately. |
| Withdrawn-anchor corollary, 313–315 | Yes. The old tag is absent, so failure precedes old-layout field interpretation. |
| Lemma 8, 317–318 | Yes. A bounded nonempty opaque snapshot body is recovered from its explicit length and exact end. |
| Lemma 9, 320–331 | **No as stated.** Equal signature verification does not imply equal hashes: P8F-01. The narrower `F || T` byte-split argument is valid after correcting the trailer length description, P8F-05. Excluding text mode avoids line-ending transformation. |
| Remark 10, 333–341 | Byte disjointness from the listed foreign formats follows from the first-byte alphabets. The subsequent signature-reuse conclusion needs more than byte inequality and H; see P8F-01. |
| Lemma 11, 343–352 | Yes for the specified fixed-field DNS value. Separators are absent from values, order and lengths are fixed, and window checks do not change parsing. Owner-name case equivalence is a comparison rule, not a claim that raw DNS wire names are injective over case spellings. |
| Theorem (i), 360–375 | Follows for the abstract accepted sets from Lemmas 3, 5, 7, 7a, 8. The receipt output includes enough information to recover M, C and both signatures. Concrete-helper conformance is subject to P8F-02/04. |
| Theorem (ii), 377–380 | Follows for frame, anchor, snapshot and slot boundaries. The OpenPGP hash-input suffix boundary also follows with P8F-05's +6 correction; it does not require the false verification implication of Lemma 9. |
| Theorem (iii), 382–389 | Follows for the four tagged construction sets and the manifest-linked signer slots. Literal foreign-format disjointness also follows. |
| Theorem (iv)(a,b), 391–407 | Yes as computational binding under H, not mathematical injectivity of a 256-bit digest. Different anchored tuples have different preimages by Lemma 7; equal digests for different preimages would be a SHA-256 collision. |
| Theorem (iv)(c,d), 408–418 | Correctly identifies additional signature and temporal assumptions instead of proving them from codec injectivity. P8F-01 does not establish a complete-receipt substitution attack. |

## Testing without a collision or successful-parse discrepancy

Counts are executions, not necessarily distinct inputs; accepted distinct counts
are stated separately. Overlapping campaigns are not claimed to be disjoint.

| Test class | Count and result |
|---|---|
| Registered baseline vectors | 71/71 golden round-trips; 173/173 rejects with their recorded codes; 5/5 negative controls. |
| Registered hybrid vectors | 35/35 golden round-trips; 63/63 rejects with their recorded codes; 1/1 negative control; 6/6 gate demonstrations. |
| Additional B/I vector comparisons | 32 payloads, 14 frames, 6 anchors; 33 content, 47 attest-frame, 4 manifest-frame and 46 anchor rejection vectors. All agree. Remaining supplied vectors are covered by the registered checker above, not claimed as full I-verifier comparisons. |
| Hypothesis typed value-pair properties | 3,000 pairs, 6,000 payload round-trips, no collision or decoder disagreement. Includes arbitrary finite binary64 values, nested arrays/maps, strings, literals, controls and supplementary Unicode. |
| Seeded accepted payload/frame generation | 12,000 payloads and 12,000 frames; 7,966 distinct payload structures in the collision table; no collision, no accepted-value disagreement. |
| Seeded accepted anchor generation | 10,000 anchors, 9,754 distinct ordered tuples; classical, hybrid and unknown opaque algorithms. No collision; decoded tuples and byte-for-byte re-encodings agree. |
| Seeded byte mutation | 20,000 ingestion texts, 20,000 frames, 20,000 anchors. Accepted counts 2,773 / 952 / 2,019. No accepted-value or tuple disagreements; 24 ingestion rejection-code discrepancies of P8F-03. |
| Seeded signature grammar mutation | 12,000 packets; 4,833 accepted; no verdict/code disagreement. Varied subpacket-length forms, old packet headers and inner lengths. |
| ECMAScript numerical differential | 106,235 finite binary64 cases B vs Node, including neighbors of powers of two across the subnormal and normal exponent range; 5,000 I vs Node. No formatting difference. |
| Unicode scalar domain | All 1,114,112 code points checked individually against B's domain predicate and an independently written condition; no disagreement. Both use the pinned Unicode tables. This is not exhaustive testing of multi-code-point NFC interactions. |
| Unicode parser boundaries | 31 selected escaped scalar/surrogate/noncharacter cases; agreement. |
| Depth boundaries | 8 each through ingest, payload and whole frame; boundaries at 62/64 enforced as specified. |
| Schema boundaries | 7 time, 7 issuer, 7 algorithm and 9 binding-form cases. Includes years 0001/9999, Gregorian leap days, leap-second rejection, numeric DNS labels, domain/identifier bounds, set ordering and uniqueness. Agreement. |
| Size boundaries | Whole frames at 16 MiB - 1, 16 MiB, 16 MiB + 1 payload bytes: accept / accept / LENGTH_CAP in both. Five snapshot sizes tested through B: empty rejected, 1 through cap round-trip, cap+1 rejected. Standalone-helper exception is P8F-04. |
| Signature caps and tags | 72 rule/slot/length cases; 12 construction-tag cross-tests. Agreement. |
| Real e2e seed | real-1's 5,090-byte anchor and both embedded frames successfully decoded in B/I. No complete-receipt policy or chain verdict asserted. |
| Exhaustive real-seed local mutations | 40,720 anchor single-bit changes; 12,920 frame single-bit changes; 5,090 proper anchor truncations; 256 one-byte suffixes. No verdict/code or accepted decode disagreement. |
| Additional structural enumeration | 81 nested signature-length cases; 1,032 MPI cases; 8 packet/subpacket length boundaries; 9 mixed-algorithm anchors; 512 frame and 256 anchor u8 tag-length cases. No disagreement. |

The seeded campaign totals **106,185 executions**, seed `0x50384620261019`,
92.708 seconds; its full histograms are in `campaign.json`. The exhaustive
local-mutation campaign totals **60,884 executions**, with zero disagreements;
histograms are in `exhaustive.json`. `numbers.log`, `properties.log`,
`boundaries.log`, `vector-check.log`, `witness.log`, `oversize.log`, `text.log`
and `lemma9.log` retain command outputs.

No existing vector was found inconsistent with the operative byte layout or
its declared codec entry point. In particular, SIG-H5/H6 sign archived spike
messages with a non-T tag, explicitly described as signature-only comparative
captures in HYBRID-SUPPLEMENT:344–346; they are not golden accepted frames.
M-01 and SIG-01 expose text defects, not vector defects.

The supplied mutation report's benign bundle/possession/OTS/header changes are
consistent with a claim over `(M,C,S_kms,S_gpg)` and `A_sig`, rather than over all
transport bytes. HYBRID-REGISTRATION-RECORD item 5 supplied a historical coverage
baseline; its 90,400 fuzz and 342 conformance counts were not silently counted as
new executions here. The real-1 bundle supplied the new exhaustive seed.

This is a bounded falsification pass, not an exhaustive proof over all byte
strings. It does not establish cryptographic security, honest key generation,
key/fingerprint authority, historical signing, anchor time, implementation
readiness or the complete A9 exit gate. No main-claim COUNTEREXAMPLE or
VECTOR-DEFECT was found. P8F-01 is a concrete counterexample to an auxiliary
lemma and is classified as a gap in the offered proof of the scoped encoding claim.

VERDICT: SURVIVED WITH GAPS (P8F-01, P8F-02, P8F-03, P8F-04; text defects P8F-05, P8F-06, P8F-07)
