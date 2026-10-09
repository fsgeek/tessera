# GUESSES — where `docs/implementation-spec.md` did not determine the code

*Phase 1 of the throwaway prototype, 2026-10-06. Each entry gives the spec location (§ and line in
`docs/implementation-spec.md` as of this date), what was missing, what the prototype chose, and whether
the formal model abstracts the point. Model citations come from the spec's own MODELLED rows. `formal/`
was read only for the two attack traces. Code carries a matching `GUESS G-nn` tag where the choice
lives. Line numbers are where the cited requirement starts.*

**Count: 50 guesses (G-01 to G-50; G-03b and G-10b are sub-entries), plus 7 contradictions or
tensions (K-1 to K-7) at the end.**

Legend for the "Model" column:
- **frame structured**: the model's `framed(...)` is a seven-argument free constructor, and term
  equality stands in for byte equality (R-3.13 l.452, V6 l.1261).
- **tuple = manifest**: the manifest is reduced to the authority tuple `authTuple(id, kfpr, sset, alg,
  ver)`, with `mh = h(t)` and possession over `t` (R-3.36 l.629, V18 l.1292, V24 l.1303).
- **P8**: the obligation sits in P8's open territory (O-01, O-03, O-79).
- **untimed**: the symbolic families do not represent time; the TLA+ modules use integers and abstract
  signatures.

## A. Bytes and encodings (P8 territory)

| # | Spec location | What was missing | What I chose | Model |
|---|---|---|---|---|
| G-01 | §3.2 R-3.10 l.424, R-3.14 l.459, table row l.412 (O-01) | The frame's binary layout, field widths and endianness | `u8 tag_len ‖ ASCII tag ‖ u16 BE canon_version ‖ u64 BE payload_length ‖ payload` | frame structured; P8 |
| G-02 | §3.1 table l.353; §8 table "Canonicalization version id" | Canonicalization version identifiers ("identifiers not enumerated") | u16; `1` = JCS + precision rule. Anything else gets V1 `INVALID` | cv bound and unexercised (R-3.13); P8 |
| G-03 | §3.1 R-3.4 l.369 | "numbers not exactly representable as IEEE 754 doubles" has two readings: the decimal literal equals a double *exactly*, or it round-trips | The literal reading. `0.1` is rejected and must be string-encoded under R-3.2. Integers above 2^53 that are not exact are rejected | not modelled (V6: byte-encoding attacks are unrepresentable) |
| G-03b | R-3.4 "`-0` and numeric edge cases" | What the other "edge cases" are | Subnormals rejected; `-0` and `-0.0` rejected | not modelled |
| G-04 | R-3.4 "non-I-JSON strings" | The test for a non-I-JSON string | RFC 7493 §2.1: reject surrogate and noncharacter code points, member names included | not modelled |
| G-05 | R-3.4 "inputs relying on Unicode normalization assumptions" | What "relying on" means | Reject any string (member names included) that is not already NFC | not modelled |
| G-06 | R-3.4 "trailing bytes" | Whether the rule covers the submitted JSON text, the frame, or both; BOM; whitespace | Both. BOM rejected. Insignificant JSON whitespace accepted at ingestion and canonicalized away. The verifier requires payload bytes to be *exactly* canonical (V6) | not modelled |
| G-07 | §3.2 R-3.11 l.428 versus R-3.9 l.419 | R-3.11 lists a "domain-separation tag" *and* an "object type" in the signed bytes; the four-field frame has one tag slot | One ASCII tag `tessera/v0/<OT_NAME>`: the prefix does domain separation and the suffix names the type | objType is a constructor argument; tags are distinct constants (P7) |
| G-08 | §3.4 R-3.36 l.629 | The concrete encoding of the map-v1 tuple | A JCS object `{issuer_id, key_fp, sset, alg, ver}`; `ver = "map-v1"` | tuple = manifest; `authTuple` is a free constructor |
| G-09 | §3.4 R-3.36 l.629; V28 l.1327 | The two-signer tuple: which fingerprint goes in `key_fp`, what `sset` contains, how arity is computed | `key_fp` = slot A; `sset` = the other required slots' fingerprints, in order; arity = 1 + \|sset\|; duplicates rejected. **Copied from the C-C2 trace's honest tuple** `authTuple(issuerId2, fp(pk(skI)), signers1(fp(pk(skB2))), …)` so the replay would be faithful. The spec alone does not determine it | positional `signers0`/`signers1`, \|set\| ≤ 2 (V28) |
| G-10 | R-3.11 l.428; V16 l.1288 ("`fp` is a free constructor") | The fingerprint function | `"fp1:" + hex(sha256(alg ‖ 0x00 ‖ raw_pubkey))`. GPG v4 fingerprints are not used | fp is a free constructor; Layer 2 |
| G-10b | V14 l.1283, R-9.13 canary | Under G-10 the fingerprint depends on the algorithm, so for an unknown algorithm the verifier cannot compute fp(kX) at all | V16 and the in-frame `=fp(kX)` pin become *unperformable* for an unknown algorithm. My first build marked them *failed*, which turned the canary vector into `INVALID`, against R-3.53 (caught by a test) | not modelled (V14 is "not modelled") |
| G-11 | §3.4 R-3.41 l.658 (O-03) | Algorithm identifier strings and where they live | Strings in `common.alg` inside the payload, plus a presentation copy per slot. `Ed25519` is supported; `ML-DSA-65` and `ECDSA-P256-SHA256` are "known but unsupported"; anything else is unknown | `=alg` pin as a term (V13); P8 |
| G-15 | §3.2 R-3.12a l.439 (O-79, "the encoding map") | Where each of the seven symbolic bindings lives in bytes, and how "payload equal across signer slots" becomes a statement about bytes | Payload = JCS `{"common": {…}, "signer": {"key_fp": …}}`. Everything except `key_fp` sits in `common`, and V30 compares `common` byte-for-byte | frame structured; term equality (V30 l.1329) |
| G-16 | R-3.39 l.646, R-3.44 l.689 | Where `declared_issue_time` lives and how it is encoded. It must be authenticated, but no field is named | `common.declared_issue_time`, RFC 3339 UTC, second precision, inside the signed payload | untimed (ProVerif); TLA+ integers |
| G-17 | R-3.37 l.635 versus §3.4 table row l.585 | How the required binding-form set is encoded (P8 "defines" it), and whether it lives in the envelope or the manifest | A sorted, unique JSON array in `common.binding_forms`, in the attestation's signed bytes. An unsorted, duplicated or empty set is `INVALID` | V21 not modelled anywhere (O-73) |
| G-26 | §5.1 R-5.4 l.1184 | The bundle's format, member names and transport encoding | JSON; bytes as standard base64; `layers[]` outermost first; per-slot `{slot, alg, pubkey_b64, frame_b64, sig_b64}` | bundle tuple `(t, ev, kX, ppf, sg, fb)` (R-2.22) |
| G-41 | none (invented) | A signature entry that may carry an *attached* message (`signed_bytes_b64`). Needed only so the C-C5 mutant has a concrete form (see report, prediction 4) | The correct verifier never reads it; the mutant verifies over it | `checksign` returns the message (message recovery) |

## B. Manifest, authority, possession (the tuple-versus-manifest question)

| # | Spec location | What was missing | What I chose | Model |
|---|---|---|---|---|
| G-14 | R-3.11 l.428; V18 l.1292 | What "manifest hash" hashes: the tuple or the whole manifest (keys, evidences, possession, binding forms, anchor) | `sha256(JCS(tuple))`. Nothing else in the manifest is under it | tuple = manifest (`mh = h(t)`) |
| G-21 | §3.4 R-3.32 l.605 | The DNSSEC snapshot and the git+OTS publication formats; how each evidence is "time-anchored" | **STUB.** Each channel is an Ed25519 key in trust config, signing an `OT_AUTHEVID` frame over `{"form":"STMT_DIGEST","digest":mh}` or `{"form":"STMT_DIRECT","statement":t}`. Evidence is not time-anchored | matches the model exactly (`sign((STMT_DIGEST,h(t)),skS)`, R-2.21) |
| G-22 | R-3.38 l.641 ("`sign((POSS, manifest), sk)`") versus V24 l.1303 (`(=POSS,=t)`) | Whether possession covers the manifest or the tuple | An `OT_MANIFEST` frame whose payload is the tuple's JCS bytes | tuple = manifest |
| G-23 | R-3.31 l.589 ("issuer public keys (or references)") | Where the public keys live | Keys are presented per slot; the manifest holds fingerprints only. No references are supported, so R-3.31a/R-5.13 resolution was not built | kX presented separately from the tuple |
| G-27 | §5.2(i) R-5.21 l.1358; R-5.8 l.1217 | **The input revocation comes from.** "No revocation effective at or before anchor_time" must be evaluated, but no bundle member and no listed trust-configuration member carries revocation facts | `TrustConfig.revocations: {fp: effective_time}`, which goes beyond R-5.8's list. Checked per slot as `REV[slot]` | TLA+ `revoked` is a state variable; no carrier |
| G-29 | R-2.30 l.290, R-2.31, R-2.37 l.308 | Whether a *required* channel evidence that is absent counts as failed (`INVALID`) or unperformable (`UNVERIFIABLE`) | Unperformable. R-2.37's "missing member → INVALID" is read as covering the binding-form set only | P4 abstracts check outcomes |
| G-46 | R-2.20, R-2.29, R-5.6 | What the verifier does when *handed* an illegal policy (waive every channel, enlarge δ) | It refuses to evaluate (`PolicyError`) rather than return a verdict | P4 `legal policy` precondition |

## C. Temporal and anchor

| # | Spec location | What was missing | What I chose | Model |
|---|---|---|---|---|
| G-19 | §3.5 R-3.42 l.679 | "Exactly one anchor proof … over its canonical bytes" when a two-signer receipt has two frames (reading (a)) | One anchor over `sha256("tessera/v0/receipt-digest\0" ‖ Σ u32len(frame) ‖ frame)`, in slot order; checked by V33a | untimed; V33a is "none" modelled (l.1343) |
| G-20 | §3.5, §4.5 | Everything about OTS proofs, Bitcoin headers, txid | **STUB** local hash chain: JCS headers, a SHA-256 merkle path, txid = double-SHA-256 of `"STUB-TX" ‖ digest`, blocks mined at chosen times, no PoW | TLA+ chain of timestamps |
| G-31 | V38 l.1348 ("not specified"); R-3.48 (docket) | Header authentication | Every bundled header hash must equal the verifier-distributed store's pin, and the headers must link. A height missing from the store is `UNVERIFIABLE` (the docket 6-7 reading) | not modelled |
| G-42 | R-3.43 l.685 | How the txid is protected in an *unwrapped* receipt ("the P7 wrapper discipline makes the containment tamper-evident" presumes a wrapper) | The verifier recomputes the txid from the proof's digest and requires equality | not modelled |
| G-38 | §4.5 R-4.45-R-4.49 | When the re-issue happens on the simulated clock | The next attempt is declared at max(last header time, declared + δ + S) + 1 | P5c fused clock |
| G-39 | R-2.20, R-4.40 | Which tolerances the issuer's ship guard uses (the issuance policy's or the verifier's) | The strict defaults for both | bridge `HonestShipAccepted` assumes they agree |
| G-40 | R-3.46 l.698 versus R-3.39 l.646 | Where the "observed anchor delay" lives. It cannot sit inside the bytes the anchor covers, yet R-3.39 wants everything later used to interpret the attestation authenticated | Policy version goes inside the signed common; observed delay goes in an unsigned `issuance_record` that nothing checks | not modelled |
| G-50 | R-6.14 l.1573 ("under the issuance policy's tolerances") | Which δ/ε apply to the TLR anchor at verification | The verifier trust configuration's | untimed (R-6.41) |

## D. Verifier procedure and output

| # | Spec location | What was missing | What I chose | Model |
|---|---|---|---|---|
| G-18 | §3.6 R-3.50 l.735 | What the verifier *does* with the spec id/hash bound into the signed bytes. No check in §5 consumes it | It is bound in `common.spec`, and the embedded spec object is carried with its own hash. Neither is checked; this is recorded as unconsumed | not modelled |
| G-28 | V6 l.1261 | The verdict for a JCS-valid payload that lacks the expected structure | V6 `INVALID`, code `P8_PAYLOAD_SCHEMA` | frame structured |
| G-30 | §5.3 reason-code table (~l.1440) | Reason codes for nearly every envelope check; only `KEY_FINGERPRINT_MISMATCH` is named | Invented codes (`P3_FRAME_BINDING_MISMATCH`, `P5_CONFIRMATION_LATE`, …); check ids are `Vn[slot]` / `Vn[channel:form]` | model has events, not codes |
| G-32 | V4 l.1259 ("the tag the caller is verifying against") | Where the expected type comes from. The caller has only the bundle | The outermost layer's declared type, restricted to `OT_ATTEST`/`OT_WRAPPER`; inner layers take the type from the bundle entry the wrapper points at | S-P7 pins by path |
| G-33 | §3.3 R-3.17 l.494, R-3.18 l.500, R-3.20 l.509; V12 l.1276 ("on failure: not specified") | Wrapper payload layout, and where the inner keys, manifest and anchor travel | `common.inner = {cv, slots:[{slot, frame_b64, sig_b64}]}` and `common.outer_cv`. Inner keys, manifest and anchor are presenter-supplied in the next bundle layer and *not* covered by the wrapper's signature (O-70). A wrapper with no inner layer is `INVALID` (V12) | `wrap(cvInner,(innerBytes,innerSig))`; completeness open |
| G-43 | V28 l.1327 | The verdict when the package presents extra or duplicate signer slots | `INVALID` | \|set\| ≤ 2, positional |
| G-45 | §5.3 R-5.44 l.1413 | The base assessment's concrete shape | Per-layer `{verification, waivers{group:{authorized_by_policy, observation}}, checks, failed, unperformable, protocol_standing}`, plus `governing` and a fixed `scope` string; no aggregate | not modelled |
| G-47 | R-3.53 l.755, R-3.51 | The conformance-vector object format | The canary vector is carried as a *label*. Conformance vectors, the standards-dependency manifest and the preamble are carried and never checked | not modelled |
| G-48 | V30 l.1329 (three fields; the other three via the tuple) | Exactly which bytes must be equal | The whole `common` (which includes the declared time, binding forms and spec) — stronger than the six fields | term equality on 3 fields |

## E. Issuance and standing

| # | Spec location | What was missing | What I chose | Model |
|---|---|---|---|---|
| G-12 | §2.1 R-2.1 l.226; §4.3 R-4.13 l.917 | KMS and GPG custody | Both slots are in-process Ed25519 keys. Not built | the model's keys are names |
| G-13 | R-4.13 ("both over the same canonical bytes") | An OpenPGP signature covers `data ‖ hashed-subpacket trailer`, never the frame alone; the spec has no OpenPGP profile | The GPG slot is emulated as a raw Ed25519 signature over the frame (see K-3) | `sign((BYTES, fb), k)` |
| G-24 | R-3.25; V27 l.1306 | The attempt core and derived identity for n slots | `aid = sha256(JCS({tuple, possession[], signatures[] in slot order, declared_issue_time}))`. Because the core is built *from the presented tuple*, the §A5.6 alias attack cannot be expressed in this format | `attemptCore(t, ppf, sg, decl)`, 1 key |
| G-25 | R-6.9 l.1563 | The "entitled key" for a two-signer issuer | The slot-A key | single key |
| G-34 | R-6.24 step 1 l.1614 | The output when the standing path "does not proceed" (the model emits no report) | `value: null` with an invented reason | no report |
| G-35 | R-6.24 step 6 l.1619 (O-74) | The outcome when the TLR key ≠ the presented key | `UNVERIFIABLE` / `STANDING_EVIDENCE_SIGNATURE_INVALID` | none modelled |
| G-36 | R-6.14 l.1573 | The TLR body format and what is anchored (model: `h(tlrSig)`; spec: "the TLR's digest") | Body `{tag, lineage[{aid,disposition}], terminal{kind,aid?}, declared_terminal_time}` in an `OT_TLR` frame; the anchor covers the frame digest | `anchorProof(h(tlrSig))`, inert |
| G-37 | R-6.40 (O-76) | Lineages longer than two entries | List lookup by aid | `lineage2` only |
| G-44 | R-6.44 | Standing for wrapped layers | Evaluated on the outermost `OT_ATTEST` layer only | routed to S-P7 |
| G-49 | §4.6 R-4.61 l.1031 | The refusal record, commitment, delivery and publication machines | **NOT BUILT** (a stub dict) | not modelled (R-4.71) |

## Contradictions and tensions inside the spec

None of these is resolved here. Each is a place where code had to take a side.

- **K-1 (apparent).** R-3.36 l.629 and R-4.32 l.961 say "only the key fingerprint is compared …
  `issuerId`, `sset`, `alg` and `ver` are carried through the binding without any policy check — bound,
  not validated." But V28/V29 (l.1327) read the required arity from `sset` and compare every `sset`
  member against a presented key, and V13/V17 pin `=alg` and `=id` against the frame. It reconciles if
  "validated" means "checked against a policy" and equality pins don't count. The spec does not say so.
- **K-2.** R-3.42 l.679 requires "exactly one anchor proof (the OTS proof over its canonical bytes)",
  while R-3.12 l.432 (reading (a)) gives a two-signer receipt two signer-specific frames. "Its canonical
  bytes" picks out no single byte string (G-19).
- **K-3 (tension).** R-2.1 and R-4.13 have KMS and local GPG "both over the same canonical bytes", and
  V19 requires `checksign(sg, kX) = (BYTES, fb)`. An OpenPGP signature never signs `fb` alone. And R-3.12
  requires the *algorithm* to be equal across signer slots, with one `alg` per tuple. Two independent
  custody domains running different algorithms (KMS ECDSA-P256 next to GPG Ed25519, say) would therefore
  be unrepresentable as one receipt.
- **K-4 (mild).** The §3.4 table l.585 lists the required binding-form set among *manifest* members,
  while R-3.37 l.635 says "an *envelope* carries a signed … set". It matters: a manifest member outside
  map-v1 is not covered by the authority evidence (G-17).
- **K-5 (mild).** R-3.38 l.641 has possession over "manifest", while V24 l.1303 and the model have it
  over `t`. Combined with R-3.31's "the manifest itself anchored", a manifest that is more than the tuple
  leaves open which bytes possession and the anchor cover (G-14, G-22).
- **K-6.** R-2.37 l.308: "a missing … member … yields `INVALID`". R-2.30 l.290 and P4 R-5.14: a required
  check that cannot be performed yields `UNVERIFIABLE`. For a *missing required authority evidence*,
  either reading can be cited (G-29).
- **K-7 (mild).** R-3.43 l.685: the txid is outside the signed bytes and "the wrapper discipline of P7
  makes the containment tamper-evident". A base receipt has no wrapper (G-42).
