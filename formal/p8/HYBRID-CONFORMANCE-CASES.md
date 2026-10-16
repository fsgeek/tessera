# Hybrid branch: profile-conformance cases for `prototype/conformance` (HS-04)

> **STATUS: DRAFT, 2026-10-14. Owner instance (Claude Opus 5.5).** These are required cases, written as a list for
> whoever maintains `prototype/conformance`. This file does not edit that directory.
>
> Source: Codex review `docs/reviews/hybrid-supplement/CODEX-REVIEW.md`, finding HS-04. Rules tested: V1-PROFILE §1
> (catalog entry; "Codec-known versus policy-supported", r2-F01; "Branch-not-taken id before registration", EA-09),
> §6.4 (M5), and §15.7 (rows 3.1, 5.1, 6.3, 7.1, 9.x).

**Why these cases are not in `formal/p8/vectors`.** The P8 codecs A (`gen.py`) and B (`check.py`) are
**candidate-codec and cryptographic-profile evidence** only:
- both hard-code the classical id and the pair id in one codec registry;
- both treat registry membership as the condition for verifying signatures;
- neither has an input for the selected catalog id or for the registration state.

So they cannot test the routing below. These cases need the profile verifier: its catalog, its registration state
and its row-ordered verdict.

The pair id throughout is `KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256`, and the classical id is
`OPENPGP4-ECDSA-P256-SHA256`. Neither the pair id nor the r2-F01 routing rule is altered by these cases.

## Cases

**(a) Before registration: the hybrid id is absent.**
- Installation: the hybrid supplement is not registered. The catalog id is the classical one.
- Input: a receipt and manifest whose frames carry the pair id consistently, with nonempty signatures in both
  slots.
  - Variant a1: a 3309-byte kms signature.
  - Variant a2: a 119-byte rule-O packet in kms.
  - Variant a3: arbitrary 1–65536-byte strings in both slots.
- Expected:
  - the codec takes both slots as **opaque** and accepts them, even where rule R or rule O would reject them;
  - key, signature and possession semantics are skipped, with no `KEY_FORMAT`, `SIG_*` or `POSSESSION_INVALID`;
  - outcome `UNVERIFIABLE / ALG_UNKNOWN`;
  - M5 contributes `ALG_UNKNOWN`, not `SCHEMA`.
- Also: an empty signature, or one above 65536 bytes, still fails the opaque codec (`SIG_EMPTY`, `LENGTH_CAP`):
  INVALID, which outranks UNVERIFIABLE.

**(b) After hybrid registration and selection: the classical id is still rule O.**
- Installation: the hybrid is registered, and the catalog id is the pair id.
- Input: a codec-valid classical-id receipt (rule O in both slots; for example the baseline R-01 bytes, or a fresh
  pair).
- Expected:
  - the codec applies **rule O** to both slots (not opaque) and accepts;
  - outcome `UNVERIFIABLE / ALG_UNKNOWN`;
  - key, signature and possession semantics are skipped, so a signature that would not verify produces no
    `SIG_INVALID`;
  - M5 contributes `ALG_UNKNOWN`, not `SCHEMA`.

**(c) After hybrid registration: codec-invalid classical signatures are still INVALID.**
- Installation: as in (b).
- Input: classical-id frames whose signature fails rule O. Use the baseline rejection bytes:
  - XA-19 (0xC2 header) → `SIG_PACKET`;
  - XA-22 (type 0x01) → `SIG_FORMAT`;
  - XA-14 (above 1024) → `LENGTH_CAP`;
  - XA-11 (empty) → `SIG_EMPTY`.
- Expected: `INVALID` with that ENC code (row 3.1). It outranks the `ALG_UNKNOWN` of row 7.1.

**(d) A wholly unknown, consistent id is opaque, with `ALG_UNKNOWN`.**
- Installation: either branch.
- Input: frames and a manifest that all carry a well-formed unregistered id. Examples are the near-miss
  `KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA384` (P8 XHR-09) and `X-UNKNOWN-ALG-1` (P8 A-02), with nonempty
  signatures of up to 65536 bytes.
- Expected: the opaque codec accepts; outcome `UNVERIFIABLE / ALG_UNKNOWN`; no `SCHEMA` from M5.

**(e) Unequal frame and manifest alg values fail receipt consistency, whether or not they are supported.**
- Installation: either branch.
- Inputs:
  - e1: the kms frame carries the pair id, the gpg frame the classical id, the manifest the pair id (the M9 shape;
    P8 XHR-08);
  - e2: both frames carry the pair id, the manifest the classical id;
  - e3: both frames carry an unknown id, the manifest a different unknown id.
- Expected:
  - e1: `INVALID / RECEIPT_COMMON_MISMATCH` (row 6.2, the common byte substrings differ);
  - e2 and e3: `INVALID / RECEIPT_MANIFEST_MISMATCH` (row 6.3).
- In each, the INVALID holds whatever the support state of the ids involved, and outranks any `ALG_UNKNOWN`.

## What a pass means

All five cases pass in the profile verifier, with the stated reason codes in row order, under both installation
states. That evidences the supplement's routing claims (§1, "Catalog"; §5). It says nothing more about the
cryptography, which the P8 candidate-codec evidence covers.
