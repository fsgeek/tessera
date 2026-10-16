# V1 profile: `tessera-v1-strict`

> **STATUS: DRAFT, 2026-10-13. Not registered.** Author: owner instance (Claude). This is the E16 extract for V1
> (V1-DERIVATION-DRAFT §5, Track 2, step 7). It is built from Amendment 9 (itself PROPOSED), the derivation draft,
> `formal/p8/ENCODING-V1.md` and the implementation spec, **plus a separately listed set of dated owner profile
> decisions (section 0.1)**. It changes no registered sentence. Revised 2026-10-13 after `docs/reviews/v1-profile/`
> (F2, F8 and the "decisions A9 does not settle" list) and `docs/reviews/a9-custody/` finding 3. **Revised
> 2026-10-14** to integrate the owner-disposed spec-sufficiency resolutions
> (`docs/reviews/spec-sufficiency/RESOLUTIONS-DRAFT.md`, status OWNER-DISPOSED 2026-10-14, after
> `CODEX-REVIEW-RESOLUTIONS.md` and `DISPOSITION-RESOLUTIONS.md`). Each integrated rule is tagged
> `[OWNER 2026-10-14, Gxx]`; the full formats are in section 15; what remains open is in section 14. **Revised
> again 2026-10-14** after the second full review (`docs/reviews/v1-profile-r2/CODEX-REVIEW.md`, F01–F17, its
> section 14.2 additions and its contradiction list, all accepted by the owner). Each change is tagged
> `[OWNER 2026-10-14, r2-Fxx]` (`r2-14.2` for the section 14.2 additions, `r2-contra` for the contradiction list);
> withdrawn text is kept as dated corrections. Disposition: `docs/reviews/v1-profile-r2/DISPOSITION.md`.
> **Revised again 2026-10-14** after differential run 1 (`prototype/differential/FINDINGS.md`): fixes are tagged
> `[OWNER 2026-10-14, diff-1 F-x]`; readings both implementations chose independently are written in as rules tagged
> `[OWNER 2026-10-14, codified from diff-1, EA-xx/Axx]`; interface conventions are in section 3.5.

## What this document is for, and what it is not

This is the one place an implementer of the V1 verifier or issuer can read what V1 requires. It lists the
requirements, and each one points to where it was decided (source section and rule name; line numbers are
locators only, section 0). Together with A9 and ENCODING-V1 it is intended to be **sufficient with the frozen
catalog, the authenticated trust configuration and the pinned normative dependencies**; those external immutable
inputs do not disappear. [OWNER 2026-10-14, r2-F17, r2-14.2] *(Dated correction 2026-10-14: previously "each one
points to the line where it was decided"; that overstated it where a requirement points only to a later owner tag.)*

It is mostly an extraction. Where a rule is already decided, the source is tagged. Where it is not, the gap is
marked `OPEN` and says what must be decided. It also records a small number of **new** choices that no source makes;
each is labelled `OWNER PROFILE DECISION 2026-10-13`, is listed in section 0.1, and is not an A9 citation. It does not restate the byte encoding: for that, read
`formal/p8/ENCODING-V1.md`. It does not hold operating numbers (window dates, stop margins, hardware): those are in
`docs/V1-OPERATIONS-RUNBOOK.md` and are not profile rules. It is not the 2929-line spec, which stays as the design
reference and is synced after V1.

Where this document and a signed amendment disagree, the amendment wins.

## 0. How to read the tags

Every requirement ends with a tag `[source:line]`. Sources:

| Short | File |
|---|---|
| A9 | `docs/phase-0-prereg-amendment-9.md` (PROPOSED) |
| DD | `docs/V1-DERIVATION-DRAFT.md` |
| ENC | `formal/p8/ENCODING-V1.md` (section numbers and line numbers) |
| SPEC | `docs/implementation-spec.md` |
| RB | `docs/V1-OPERATIONS-RUNBOOK.md` (reference only) |
| SR | `prototype/spike/SPIKE-REPORT.md` (instrument evidence, never a rule by itself) |
| FT, GU | `prototype/FINDINGS-BY-TIER.md`, `prototype/GUESSES.md` (finding labels only) |
| RES | `docs/reviews/spec-sufficiency/RESOLUTIONS-DRAFT.md` (owner-disposed 2026-10-14; rationale and conformance list §L) |

**Locators** [OWNER 2026-10-14, r2-F17]. A9 section identifiers (A9.1 … A9.8) and stable rule names ("Root-KSK
rule", "Trust-configuration authority", "Git stamp target", C4, …) govern. Many `A9:nnn` line numbers in this
document were taken from an earlier A9 layout and are now approximate locators only (example: section 8's fallback
bullet cited A9:338-340, which in the reviewed snapshot is A9.5 trust-configuration authority; the rule it means is
A9.6 "Signers"). Where a line number and a section or rule name disagree, the section and rule name govern. Every
`A9:nnn` locator is refreshed against the A9 **signing commit**, which the freeze record names together with the
freeze commit of every other source (section 14.2 item 7).
A tag `[OWNER 2026-10-14, Gxx]` marks a rule decided by the owner's 2026-10-14 disposition of spec-sufficiency gap
Gxx (RES). Its rationale, label (CLARIFY, OWNER CHOICE (supported-path limit), BROADEN, NARROW-CLAIM, CORRECT) and
conformance cases are in RES under that gap. These are owner profile decisions in the sense of section 0.1, except
where they cite A9 text the owner changed on 2026-10-14 (A9 C4, C5, C6, A9.5 trust-configuration authority).

Decision labels follow A9's: AUTHOR DECISION, OWNER DECISION, RECOMMENDED (A9:12-18). Nothing binds until the
author signs A9 (A9:24). A label `OWNER DECISION` with an A9 tag is an A9 decision carried in. A label
`OWNER PROFILE DECISION 2026-10-13` marks a choice made in this document, not in A9 (section 0.1).

### 0.1 Owner profile decisions, and how they are adopted

A9's signature ratifies only A9's own recorded items (A9:24-26); it does not ratify later additions to this
unregistered profile. The items below are therefore **owner profile decisions**, not extraction. They take effect
as part of this profile at the 30 Oct profile freeze, the point by which A9 already requires the owner to record
dated profile choices (A9.6: signer branch and slot-2 custody "in the profile before the 30 Oct freeze"). Where one
of them conflicts with A9, A9 wins. Until the freeze they are proposals the instrument code may implement.

Classification of the seven items `docs/reviews/v1-profile/CODEX-REVIEW.md` lists as "decisions stated in the
profile that A9 does not settle" (disposition 2026-10-13: label each as an owner profile decision or OPEN, per
Codex's classification):

| # | Item | Classification |
|---|---|---|
| 1 | Pairing the repository key with D, and the mandatory signed-issuer == pinned-D gate (sections 5, 6.3) | OWNER PROFILE DECISION 2026-10-13 |
| 2 | Fixed path `tessera-v1/key-assertion`, no framing bytes, entry modes 100644 / 40000 (section 6.3) | OWNER PROFILE DECISION 2026-10-13 |
| 3 | KSK-2017's concrete periods (section 5). The end-of-day cutoff is **withdrawn**; the reliance-period rule itself is now in A9.5 (OWNER DECISION 2026-10-13, A9:296-303). The concrete dates and their evidence are this profile's | OWNER PROFILE DECISION 2026-10-13 (values); rule: A9.5 |
| 4 | The INVALID / UNVERIFIABLE root-case split and its reason codes, including `SNAPSHOT_NOT_ANCHORED` (section 5). The snapshot's own-anchor requirement is inherited; the split and codes are new | OWNER PROFILE DECISION 2026-10-13 |
| 5 | The repository key described as the public half of an offline root (section 5). Source is the runbook; neither adopted as profile policy nor A9's | **Closed 2026-10-14:** an operating fact, not verifier policy [OWNER 2026-10-14, G36] |
| 6 | The twelve-member inventory (section 2.1) and the ten-stage table (section 3.2). Extraction from ENC/SPEC, not a decision; the container encoding and any stage order or reason precedence remain open, and the table is not an execution order | **Closed 2026-10-14:** container fixed [G14, G17]; reporting order fixed [G31]; the ten-stage table stays descriptive (section 15.1, 15.7) |
| 7 | The seven per-entry dependency-manifest fields (section 9). Inherited from SPEC R-3.51, not from A9's eight-entry list; whether V1 adopts them as a profile requirement is not decided | **Closed 2026-10-14:** adopted, plus `id` and `title` [OWNER 2026-10-14, G15] |

`OPEN (step 8):` marks a spec fix that step 8 must settle (all closed 2026-10-14, section 14.1). `OPEN (other):`
marks a gap that belongs to another step or to a dated owner act. Section 14 lists them all.

## 1. Profile identity

- **Profile id:** `tessera-v1-strict`. It appears in the signed bytes as `common.profile` and in the DNS and git
  record as `profile=`. [ENC §3.2:264; ENC §7:569; A9:142]
- **Spec binding:** `common.spec.id` is `tessera-v1-strict/verification-spec/1` and `common.spec.sha256` is the hash
  of the specification bytes. [ENC §3.2:265-266]
  - `common.spec.id` other than that value gives `INVALID / SPEC_ID`. The verifier compiles in a **frozen spec
    catalog**; a `common.spec.sha256` not in it gives `UNVERIFIABLE / SPEC_UNKNOWN`. The signed `vectors_sha256` and
    `preamble_sha256` must equal the catalog entry (`INVALID / SPEC_OBJECT_MISMATCH`), and the bundled `spec`,
    `vectors`, `preamble` and `dependency_manifest` bytes must hash to their signed or catalog values
    (`INVALID / BUNDLE_OBJECT_HASH`). Bundled objects are hashed, never parsed as policy or executed. The spec and
    vectors objects are assembled by the part format of section 15.8. [OWNER 2026-10-14, G13]
  - **Comparison targets** [OWNER 2026-10-14, r2-F12]. Bundled spec → signed `common.spec.sha256`; bundled vectors →
    signed `vectors_sha256`; bundled preamble → signed `preamble_sha256`, each independently of catalog lookup
    (`BUNDLE_OBJECT_HASH`). Signed `vectors_sha256` / `preamble_sha256` → catalog entry only if the spec lookup
    succeeds (`SPEC_OBJECT_MISMATCH`). Bundled dependency manifest → catalog entry only if the lookup succeeds;
    otherwise that comparison is unperformable, never compared with an unrelated entry. Other independent failures
    still dominate `SPEC_UNKNOWN`. Bundled objects never become policy because their hashes are self-consistent.
    *(Dated correction 2026-10-14: "must hash to their signed or catalog values" did not say which comparisons
    remain performable for an unknown spec hash.)*
  - **Catalog entry** (one, for V1): the frozen object hashes; exactly one `alg` id (`OPENPGP4-ECDSA-P256-SHA256`
    under the fallback, or the registered pair id under the hybrid); `alg_prohibited` = `[]`; `binding_forms` =
    `["STMT_DIRECT"]`; D, δ, ε, k; DNSSEC algorithms {8, 13} and DS digest types {2, 4}. A well-formed `common.alg`
    other than the catalog id, including the branch not taken, gives `UNVERIFIABLE / ALG_UNKNOWN`. The catalog is
    independent of the bundle and of trust-configuration updates, and later verifiers apply it unchanged to V1
    bundles (A9.4, A9.7 row 29). [OWNER 2026-10-14, G12]
  - **Codec-known versus policy-supported** [OWNER 2026-10-14, r2-F01]: "Each frame is decoded with E §5.2's codec
    registry, including any authorized supplement, using its own alg and slot. A codec-known but unselected branch
    still uses its specified codec; an id absent from that registry uses the opaque codec. Signature/possession
    verification semantics are performed only for the catalog-supported id. Receipt/manifest alg equality is checked
    independently for every syntactically valid id. M5's catalog-alg condition is performable only for a
    policy-supported id; unsupported ids contribute ALG_UNKNOWN, not an additional SCHEMA failure." The incorporated
    codec baseline and its vectors are unchanged.
  - **Branch-not-taken id before registration.** Until a dated branch-registration supplement registers the hybrid
    pair id, that id (or any stand-in for it) is absent from the codec registry: its frames use the opaque codec and
    the outcome is `UNVERIFIABLE / ALG_UNKNOWN`, with signature and possession semantics unperformable and M5's alg
    condition contributing `ALG_UNKNOWN`, not `SCHEMA`. [OWNER 2026-10-14, codified from diff-1, EA-09]
  - **Baseline.** The governing baseline is the frozen spec object hash in the catalog. A9 incorporates ENCODING-V1 at
    its signing commit; a frozen edited ENCODING-V1 replaces it only with authorized change accounting.
    [OWNER 2026-10-14, G37]
- **Encoding:** `formal/p8/ENCODING-V1.md` at the signing commit, including D-1 to D-17. If the hybrid signer
  branch is taken, the signing-commit baseline plus the dated branch-registration supplement governs. [A9:143-144;
  A9:321-326]
- **Mode:** strict only. One layer. No wrappers, no renewal, no TLR, no waiver policy. `VALID_DEGRADED` is never
  returned. [A9:155; DD:67]
- **Claim and sub-claims:** C1 to C7 as in A9:123-140. This document does not restate them.
- **Authority:** DNSSEC for D plus the git key assertion. Both are required (n = 2). [A9:147; DD:65]
- **Issuance:** an operated API (API Gateway, Lambda, KMS). A receipt ships only when complete. [A9:158-159]
- **Parameters:** δ = 72 h, ε = 24 h, k = 6, N = 3, S = 24 h. The author's signature on A9 ratifies these five.
  [A9:217-219] The verifier owns δ, ε and k; a receipt cannot choose them. [SPEC R-5.9:1219; SPEC R-3.46:698-700]
  N and S govern the issuer only. δ, ε and k are frozen catalog constants, not trust-configuration data.
  [OWNER 2026-10-14, G12]
- **Branch recorded:** hybrid or fallback signer branch. `OPEN (other):` not yet taken. The hybrid spike has a
  21 Oct deadline; the owner records the branch, dated, in ENC §5.2 and in this document before the freeze.
  [A9:298-326] Fallback: both slots OpenPGP P-256. Hybrid: slot `kms` ML-DSA-65, slot `gpg` OpenPGP P-256. (Still open, section 14.2 item 4.)

## 2. Bundle format

### 2.1 Members

A V1 bundle carries these twelve members. Nothing is taken from outside the bundle except the trust configuration
(section 5). The last column is the container member that carries each one (section 15.1). [OWNER 2026-10-14, G14,
G17]

| # | Member | Source | Container member |
|---|---|---|---|
| 1 | Unsigned profile label (read first, for dispatch) | [ENC §8:742-743] | top-level `profile` |
| 2 | The receipt tuple `(F_kms, S_kms, F_gpg, S_gpg)`, or `A_sig`, which encodes it | [ENC §5.3:493-497] | `a_sig` only (one tuple route) |
| 3 | The manifest frame `F_manifest` and each key's possession signature over it | [ENC §4:362-369; A9:311-312] | `manifest`, `possession` |
| 4 | The two public keys, checked against the manifest fingerprints | [ENC §5.3:509] | `keys` |
| 5 | The DNSSEC snapshot (envelope per ENC §6) and its own OTS proof | [ENC §6:536-542; DD:94] | `dns` |
| 6 | The git key-assertion evidence: raw signed commit object, the tree objects on the path, the blob, and the OTS proof stamped on the commit id | [ENC §7.2:706-710; A9:282-284] | `git` |
| 7 | The receipt's OTS proof and the anchor transaction id | [SPEC R-3.42:679-682] | `receipt_anchor` |
| 8 | Bitcoin block headers needed by the proof, each of which must be in the pinned set | [A9:150; DD:99] | `headers` (one pool) |
| 9 | The verification specification bytes (content-addressed) | [A9:152-153; ENC §3.2:281] | `spec` |
| 10 | The conformance vector bytes (content-addressed) | [A9:152-153; ENC §3.2:281] | `vectors` |
| 11 | The plain-language purpose preamble, bound by hash in the signed bytes | [A9:153; ENC §3.2:281] | `preamble` |
| 12 | The dependency manifest (section 9) | [A9:153-154] | `dependency_manifest` |
| — | Observed anchor delay and issue-time policy version (R-3.46), optional diagnostics | [SPEC R-3.46:698-700] | `issuer_record` |

- Members 9, 10 and 11 are bound by SHA-256 of their raw bytes, inside the signed common bytes. They are never signed
  or anchored on their own. [ENC §0:71-72; ENC §3.2:281]
- The OTS proof, txid, headers and confirmation evidence are outside `A_sig`. [ENC §5:402-405]
- The txid sits in the bundle outside the signed bytes. [SPEC R-3.43:685-687]
- **Container.** One canonical JCS JSON text, no JSON numbers, top level exactly
  `{"layers":[L],"profile":"tessera-v1-strict"}`, with the closed layer schema of section 15.1. ~~A required member
  that is absent, at any nesting level, gives `UNVERIFIABLE / MEMBER_MISSING:<path>`; this rule precedes the generic
  schema rule.~~ *(Withdrawn 2026-10-14, r2-F03: it contradicted the `object_format` and `issuer_record`
  exceptions and left a null parent ambiguous.)* **Absence and presence** [OWNER 2026-10-14, r2-F03]: "A missing
  required evidence member contributes UNVERIFIABLE/MEMBER_MISSING:<path>, except git.object_format, which
  contributes GIT_OBJECT_FORMAT_MISSING. A present parent of the wrong type contributes CONTAINER_SCHEMA; do not
  synthesize missing descendants beneath it. Absence of issuer_record is allowed; any defect in a present
  issuer_record, including absent internal fields, contributes INVALID/CONTAINER_SCHEMA. Absence and schema failures
  are collected independently; INVALID still dominates. Nested absence is inspected only beneath correctly typed
  parents." `<path>` is the layer-relative dotted schema path (`git`, `git.ots`, `keys.gpg`; array members by
  numeric index); several missing paths are compared in JCS key order with array indices numeric. A present
  `git.object_format` that is a JSON string other than `"sha1"` is A9.5's unsupported value (`UNVERIFIABLE /
  GIT_OBJECT_FORMAT`); a present non-string value, `null` included, is a schema failure (`INVALID /
  CONTAINER_SCHEMA`), not absence (**owner choice**, fail-closed; the honest issuer emits `"sha1"`). A present
  nonconforming member or an unnamed member gives `INVALID / CONTAINER_SCHEMA`. The receipt
  tuple is taken only by decoding `a_sig`. Re-indenting a container makes it `INVALID / JSON_NONCANONICAL`
  (a visible custody restriction: keep the bytes, do not reformat). [OWNER 2026-10-14, G14, G17] *(Was:
  "`OPEN (other):` the container and transport encoding, member names and member order", 2026-10-13.)*
- **Observed delay and policy version** are carried in the optional `issuer_record` member: unsigned diagnostics.
  Absence never affects the verdict; a present record is schema-checked (`INVALID / CONTAINER_SCHEMA`); its values
  never alter verification parameters and are not authenticated observations. The honest issuer always emits it.
  [OWNER 2026-10-14, G33] *(Was: "`OPEN (other):` where the observed anchor delay and the issue-time policy version
  are recorded", 2026-10-13.)*

### 2.2 What the bundle never supplies

The bundle never supplies the trust configuration, δ, ε, k or any verifier policy. [A9:148; SPEC R-5.9:1219]

## 3. Verifier dispatch, stages and precedence

### 3.1 Dispatch

1. The verifier reads the bundle's unsigned profile label first. An unrecognized label gives
   `UNVERIFIABLE / OUT_OF_PROFILE`, and nothing else is evaluated. [ENC §8:742-743; A9:272]
2. Out-of-profile layer structure or request gives the same result without evaluation. [DD:70; A9:272]
   Cases c (two-layer transplant) and h (renewal wrapper) land here. [A9:173, 179]
3. **Dispatch reads exactly three things**, in order, and nothing else [OWNER 2026-10-14, G17]:
   - **D1.** The bytes are not strict JSON (ENC §1.4 checks 1–5), or exceed 2^27 bytes: `UNVERIFIABLE /
     OUT_OF_PROFILE`.
   - **D2.** Top-level `profile` absent or not exactly `tessera-v1-strict`: same.
   - **D3.** `layers` not an array of length 1: same (cases c and h).
   - **D4.** The request policy is a **verifier input**, never a bundle member; its only value is `strict`. Any other
     request: `UNVERIFIABLE / OUT_OF_PROFILE`, detail `REQUEST_UNSUPPORTED`, with no evaluation (case d1's waiver
     refused).
   *(Was: "`OPEN (step 8):` what exactly dispatch inspects … Decide the fields dispatch reads, and where the request
   type lives", 2026-10-13.)*
4. Once dispatched to `tessera-v1-strict`, every codec rejection is `INVALID`. That includes a signed `profile` other
   than `tessera-v1-strict`, an unknown tag and an unknown canonicalization version. [ENC §8:744-746]
5. The one **codec-level** in-profile `UNVERIFIABLE` that concerns the bytes is a well-formed unknown `alg`.
   [ENC §8:747-748; SPEC R-2.37:308] The profile adds further in-profile `UNVERIFIABLE` outcomes (missing members,
   unknown spec hash, binding forms, and the evidence outcomes below); they are not turned `INVALID` by this
   sentence. [OWNER 2026-10-14, r2-contra] *(Dated correction 2026-10-14: previously "The one in-profile
   `UNVERIFIABLE` …", repeating ENC §8's stale wording, which G01 already requires to say "codec-level".)*

### 3.2 Stages

The stage names follow the spec's. The spec registers no order between stages, only that the verdict does not
depend on evaluation order. [SPEC:1237-1248; SPEC R-5.16:1250] There are ten stages after dispatch. The
table presents ENC/SPEC material; it is not a newly fixed execution order (section 0.1, item 6).

| Stage | What V1 does | Source |
|---|---|---|
| (a) Parse | Decode every frame, the manifest and `A_sig` under ENC §1 to §5. Reason codes are reported in ENC's order. | [ENC §1.4:172-190; ENC §3.1:241-248; ENC §5:385-394] |
| (b) Type | Tag must be in T and be the expected one: `TAG_UNKNOWN`, `TAG_MISMATCH`. No wrapper stage: one layer only. | [ENC §2:215-218; A9:155] |
| (c) Algorithm | A well-formed unknown `common.alg` gives `UNVERIFIABLE`. A malformed, missing or substituted id gives `INVALID`. | [ENC §3.2:276; SPEC V13-V15:1282-1284] |
| (d) Key binding | Each presented key hashes to its slot's manifest fingerprint (`KEY_MISMATCH`). `manifest_sha256` equals the hash of the manifest frame. | [ENC §5.3:509; ENC §3.2:280] |
| (e) Authority | DNS channel and git channel (section 6), the issuance window, possession proofs. | [A9:137; A9:338-340] |
| (f) Signature set | Both slots are required, from the signed manifest, never from what the bundle presents. Common bytes are byte-equal across slots. | [SPEC V28-V31:1327-1330; ENC §3.4:303-320] |
| (g) Integrity | `SHA256(A_sig)` is the digest the OTS evidence attests. Each committed `S` verifies over its committed `F`. Any difference from the committed tuple gives `RECEIPT_ANCHOR_MISMATCH`; a bad signature gives `SIG_INVALID`. | [ENC §5.3:498-511] |
| (h) Temporal | The three-conjunct predicate at k = 6, plus the T rule (section 7). | [A9:138; SPEC V33-V36:1342-1346; SPEC R-5.19:1352] |
| (i) Revocation | Not evaluated. The report says so. | [A9:248-252] |
| (j) Partition | Section 3.3. | [SPEC R-5.25:1368] |

- The issuance-window check is part of stage (e) (C4). [A9:338-340; ENC §7.1:636-643]
- **Reported reason.** The reported reason is the first failed check in the **total check order** of section 15.7;
  if none failed, the first unperformable check in that order. The order is a reporting order, not an execution
  order. [OWNER 2026-10-14, G31] *(Was: "`OPEN (step 8):` which reason code is reported when several different
  checks fail", 2026-10-13.)*
- **`DNS_*` record class.** A TXT RRset that is present is run through ENC §7's fifteen-step order; every failure is
  `INVALID` with ENC's code, whether or not DNSSEC was performable. An absent TXT group is `UNVERIFIABLE /
  DNS_EVIDENCE_MISSING`. ENC's `DNS_RRSET` zero case stays a codec vector, unreachable from a V1 container.
  [OWNER 2026-10-14, G24] *(Was: "`OPEN (step 8):` the verdict class of the `DNS_*` record rejections", 2026-10-13.)*
- **Size gates.** An empty snapshot body or a payload over its cap gives `LENGTH_CAP`, before the JSON categories.
  The gates are exact and separate: container 2^27 bytes, payload per ENC §1, snapshot body 2^24. [OWNER 2026-10-14,
  G30] For an empty snapshot body this profile governs over ENC §6's `1 ≤ len` wording and over
  `formal/p8/vectors/gen.py` (`decode_snapshot`, which reports `SCHEMA`): the outcome is `INVALID / LENGTH_CAP`.
  [OWNER 2026-10-14, codified from diff-1, EA-20]

### 3.3 Precedence and verdicts

- Order of decision: any required check failed gives `INVALID`; else any required check unperformable gives
  `UNVERIFIABLE`; else `VALID_STRICT`. There is no waiver set, so the degraded branch never applies. [SPEC
  R-5.25:1368; A9:155]
- `INVALID` dominates `UNVERIFIABLE`. [A9:176; SPEC R-5.26:1370; SPEC R-2.33:300] Case d3 depends on it.
- The unperformable rule applies to required checks only. [SPEC R-2.32:298]
- A verdict is never a bare boolean. `UNVERIFIABLE` is never promoted. [SPEC R-2.34:302; SPEC R-5.38:1394]
- No fallback, negotiation or normalization during verification. [SPEC R-5.18:1266; ENC §1.2:156-158]
- **Aggregation.** Physical evaluation order is unrestricted, but reporting uses the fixed total check order (section
  15.7). Early termination is permitted only when every earlier-priority reportable check is settled and every
  stable field, including T, is determined. A failure prevents only checks whose own necessary input cannot be
  obtained; it does not suppress independent receipt-anchor evaluation needed for T. Derived checks are unperformable
  when necessary inputs cannot be obtained, and never pass by default. ~~An unknown `alg` routes the slot as opaque
  (Lemma 7a)~~: signature and possession semantics under an `alg` other than the catalog-supported id are
  unperformable; independent schema and hash checks still run. Codec routing is section 1's codec-known versus
  policy-supported rule. [OWNER 2026-10-14, G26; r2-F01] *Dated correction 2026-10-14: the resolutions draft's "a
  verifier may stop early only on a failed check" is withdrawn; it let two schedules report different stable
  fields. Dated correction 2026-10-14 (r2-F01): "an unknown `alg` routes the slot as opaque" is withdrawn; it
  conflicted with ENC's codec selection for a codec-known but unselected id.*

### 3.4 Output

Every report carries these six fields, and they are the stable set that later verifiers must reproduce: the verdict,
its reason code, T, `revocation`, `historical_security` and standing. [A9:156; A9:262-268]

- `revocation: NOT_EVALUATED`. [A9:248-252]
- `historical_security: NOT_EVALUATED`. The documentation names what a later examiner must supply: an authenticated
  safe-before cutoff per algorithm and per key, compared with T and A2.1's chain-time uncertainty. [A9:253-259]
- Standing: `ABSENT/NOT_ISSUED_IN_PROFILE`, reported separately and never folded in. [A9:166-167; SPEC R-1.16:163]
- No aggregate checkmark. [SPEC R-5.47:1419]
- **Report encoding.** The stable-output object is the JCS object `{"historical_security":"NOT_EVALUATED",
  "reason","revocation":"NOT_EVALUATED","standing":"ABSENT/NOT_ISSUED_IN_PROFILE","T","verdict"}`; the success
  reason is `OK`. T is the RFC 3339 string of nTime(h*) when the receipt proof parses, its file digest equals SHA256
  of the presented `a_sig` bytes, no attestation in it is contradicted, and it has a qualifying attestation;
  otherwise `null`. T is reported whatever the verdict. Diagnostics (trust-config version and hash, spec hash,
  per-check list) go in a separate wrapper object, outside the stable six. [OWNER 2026-10-14, G32]
- **T for dispatch-terminal outcomes.** A D1–D4 outcome (section 3.1) evaluates nothing, the receipt proof
  included, so its T is `null`; this holds for D4 too, even when the same bundle bytes under a strict request would
  give a T. "T is reported whatever the verdict" applies to every outcome reached after dispatch.
  [OWNER 2026-10-14, codified from diff-1, EA-05]
- Relying-party text must say that a T reported with `INVALID` is not evidence of a valid service receipt.
  [OWNER 2026-10-14, G32]
- Relying-party text must say that `INVALID / ISSUANCE_WINDOW` can come from presenting a later proof, and that the
  holder should be asked for the issuer's original proof. [A9:344-345]
- Relying-party text must say that the verifier cannot check public publication of the git commit. [A9:413-418]

### 3.5 Verifier CLI and release-provisioning interface (instrument level)

**Interface convention, not a verdict rule.** This subsection records how the conformance suite and the
differential harness drive a verifier under test. It changes no verdict, reason or T, binds no production release,
and gives way to the release artefact and release-signature format when those are decided (section 14.2 items 1,
2). Both implementations of differential run 1 used it. [OWNER 2026-10-14, interface convention from diff-1,
EA-01/EA-02/EA-03/EA-12]
- **Invocation and compiled-in inputs (EA-01).** `CMD --trust <config> --bundle <bundle>`. The compiled-in trust
  configuration hash and catalog (section 1, section 5) are provisioned for TEST by environment: the TEST release
  record from `TESSERA_V1_TEST_RELEASE`, authenticated by the public key in `TESSERA_V1_TEST_RELEASE_KEY`, and the
  catalog from `TESSERA_V1_TEST_CATALOG`. A config whose hash is not the one compiled by an authentically signed
  release is refused (`TRUST_CONFIG_UNAUTHENTICATED`, no verdict).
- **Request (EA-02).** The request (D4) is `strict` by default; `--request <value>` supplies any other value.
- **Output and refusal (EA-03).** A verdict is one JSON object on stdout carrying the six stable fields, either at
  top level or under `stable`, `result` or `report`; diagnostics may accompany it. A startup refusal is a nonzero
  exit with the refusal code on stdout or stderr and no six-field object.
- **Release checker (EA-12).** `CMD --previous <config> --next <config>` prints `ACCEPT` or `REJECT` for the release
  invariants of section 5.

## 4. Issue order (issuer side, binding on the build)

1. Fix the manifest and common metadata, including `declared_issue_time`.
2. Build both frames.
3. Sign each frame.
4. Verify both signatures with the exact bytes to be committed.
5. Freeze the signature bytes. Any re-framing happens before this point.
6. Build `A_sig` and stamp its SHA-256. One stamp per receipt.
7. Obtain and validate the confirmation and time evidence.
8. Ship the complete receipt.

[ENC §5.4:515-525; A9:278-281] That is eight steps in both sources. A retry that changes any committed byte needs a
fresh stamp. The frame-only anchor is withdrawn, with no fallback. [A9:277; ENC §5.1:407-414]

Issuer duties that are not verifier rules: an attempt whose T would exceed not-after is not shipped [A9:341-342]; the
`gpg` signer refuses a frame whose `declared_issue_time` is more than ε from its clock [A9:327-330]; the issuer never
re-authorizes a key [A9:260]; public publication of the commit stays an issuer duty [A9:413-418]; the issuer
re-captures the DNSSEC snapshot before shipping if it fails the snapshot rule [DD:94].

Further issuer duties [OWNER 2026-10-14]:
- **Chain-order pre-commitment.** Do not issue in a window until the key-assertion commit's stamp has k = 6
  confirmations and the receipt will anchor at a higher height (A9 C4). Before honest issuance the issuer obtains and
  validates the git assertion's k = 6 proof. A receipt stamped after the issuer has observed h_git + 5 anchors above
  it, so it passes the verifier's `h_git + 5 < h_receipt` rule (section 6.3). [G02; RB §5]
- **Snapshot c3.** Check all three conjuncts on the snapshot's own proof before shipping; recapture or retry if they
  fail. A snapshot stamped before the receipt need not confirm before it. [G06]
- **DNSSEC support.** Validate the snapshot under this profile's algorithm set (section 6.1); do not ship a receipt
  whose chain would be `DNSSEC_ALGORITHM_UNSUPPORTED`. [G16]
- **Snapshot body.** Convert to the section 15.3 body before stamping. [G19]
- **Signature output.** Both OpenPGP adapters emit signatures that satisfy the rule-O policy of section 8 before
  signing is final and before stamping. [G11]
- **Canonical container.** Emit the container as canonical JCS (section 15.1). [G17]
- **Pre-ship checks for the 2026-10-14 r2 completions** [OWNER 2026-10-14, r2-F07, r2-F08, r2-F09, r2-F10]: the
  snapshot body carries no RRSIG with fewer Labels than its owner (section 15.3); the selected path of each of the
  three proofs (receipt, snapshot, git) satisfies the transaction-shape subset and the conventional merkle suffix
  (section 15.2), else the proof is re-stamped or the attempt abandoned; both OpenPGP adapters and the repository
  signer emit type-16/type-33 subpackets only in the shapes section 8 allows. All 352 Bitcoin paths in the
  repository's 129 proofs satisfy the shape and suffix rules (owner check, 2026-10-14); this is evidence, not a rule.

## 5. Trust configuration

It ships with the verifier and is never read from the bundle. [A9:148; SPEC R-5.8:1217; SPEC R-2.17:262] It holds:

| # | Item | Source |
|---|---|---|
| 1 | Root KSK-2017 | [A9:148-149; DD:66] |
| 2 | Root KSK-2024 | [A9:148-149; DD:66] |
| 3 | Repository entries: D = `wamason.com`, the repository key, an inclusive signing interval | OWNER PROFILE DECISION 2026-10-13 (section 6.3); A9.5 repository entries; [A9:63-65] |
| 4 | A versioned set of pinned mainnet header hashes, authenticated by the release allowlist | [A9:149; DD:66]; A9.5 trust-configuration authority |
| 5 | ~~The parameters δ, ε, k~~ | moved to the frozen spec catalog (section 1) [OWNER 2026-10-14, G12] |

*Dated correction 2026-10-14:* item 5 previously read "The parameters δ, ε, k [A9:217; SPEC R-5.8:1217]". A
trust-configuration release can be extended, so verdict-deciding parameters now live in the frozen spec catalog,
which cannot. Item 3 previously read "The pair (D, repository root key)"; A9.5's repository entries also carry a
signing interval.

- **Authority: independent release allowlisting** (A9.5 "Trust-configuration authority", OWNER DECISION 2026-10-14).
  The trust configuration is authenticated independently of the bundle and of both authority-channel credentials.
  Each verifier release compiles in the SHA-256 of exactly one trust configuration; the config file itself carries no
  signature. Releases are signed by the **release key**, which neither the DNS credential, the repository key nor the
  issuing AWS account can use; the dated custody record names that key and its access boundary. Capture of any
  authority-channel credential grants no ability to sign a release, authorize a configuration hash, or replace the
  compiled trust root or policy catalog. CI is not the authenticity check. Compromise of the release key is
  distribution compromise, a stated boundary (A9 "The boundaries"). [OWNER 2026-10-14, G08]
  - A config whose SHA-256 is not the compiled hash, or that fails the section 15.5 schema, makes the verifier refuse
    to run with exit error `TRUST_CONFIG_UNAUTHENTICATED`: no verdict.
  - Bootstrap: the release public key is published with the verifier's documentation and relying-party text, and its
    fingerprint is in the freeze record. A new release key is introduced only by a release signed by the current one.
  - `version` starts at `"1"` and increases by 1; `previous_sha256` is 64 zeros for version 1, else the prior config's
    hash. Every report carries the config version and hash as diagnostics; reproducing a verdict exactly (A9.4) uses
    the release that compiled that hash.
  - Required test: a captured repository signer (and, separately, a captured DNS credential and the issuing AWS
    account) signs a config adding its own KSK, repository key and pins; the verifier refuses it.
  - **OPEN:** release-key custody, holder and access boundary; the release artefact and release-signature format
    (section 14).
  - *Dated correction 2026-10-14:* the 2026-10-13 resolutions draft proposed a dedicated trust-config key giving the
    config a detached rule-O signature, with append-only enforced in CI. Withdrawn: key inequality does not establish
    independence, and CI cannot stop an attacker who bypasses it (`CODEX-REVIEW-RESOLUTIONS.md` F04).

- **Root KSKs, three periods each.** The trust configuration records each KSK's signing and reliance periods
  separately from its publication and revocation dates. [A9:153; A9:302-303] The instrument spike found that
  conflating signing with publication falsely rejected every snapshot from 2026-10-11. [SR:73-78]
- **Root rule.** The root DNSKEY set is valid at the snapshot's anchored time if some trusted KSK whose **reliance
  period** contains that time validates it. Each KSK entry records signing-start, signing-end and a sourced reliance lifetime L; the reliance
  interval is [signing-start, signing-end + L]. L is an acceptance-policy value from cited RRSIG validity evidence,
  labelled observed, not a proven global maximum. The extension admits authentic pre-retirement evidence anchored
  later and does not prove signing before retirement: a thief of a retired KSK can manufacture eligible evidence
  during it (A9.5; AUTHOR ADOPTED 2026-10-13, kind CORRECT). *Dated correction 2026-10-13: the earlier wording
  ("maximum validity … it made"; "usable for that long and no longer") overclaimed provenance and is withdrawn.* The rule is existential and
  order-independent: a candidate that fails is informational, and the result is computed once, after every eligible
  key has been tried. A trusted KSK that is published but did not sign is informational, never a failure.
  [A9.5, A9:296-303, OWNER DECISION 2026-10-13 after `docs/reviews/v1-profile/` F1, F2]
- **Rollover control (required vector).** A snapshot taken while one trusted KSK is published but not signing must
  pass. [A9:307-308] Further required vectors (`docs/reviews/v1-profile/` F1, F2 dispositions): a failing trusted
  candidate listed before a validating one, in both trust-list orders, must pass; an honest old root signed before
  retirement and anchored after retirement but within reliance must pass, and the same evidence after reliance must
  not.
  - **Both orders.** `root_ksks` is sorted (section 15.5), so a conforming configuration has one order. "Both
    trust-list orders" is met by the failing trusted candidate sorting first and, separately, sorting second in the
    canonical candidate order (G35), which also covers both snapshot-body RRSIG orders. [OWNER 2026-10-14, codified
    from diff-1, EA-08]
  - **Expected reason after reliance.** Only a time-valid candidate is in the finalized-interval class. With L at
    least the RRSIG validity (L = 21 days observed), pre-retirement evidence anchored after reliance always has an
    expired RRSIG, so the "must not pass" vector reports the time class, `INVALID / RRSIG_NOT_VALID_AT_EVAL_TIME`;
    `KSK_OUTSIDE_RELIANCE_PERIOD` needs an RRSIG window longer than L. [OWNER 2026-10-14, codified from diff-1,
    EA-14]
- **Known facts for the periods.** KSK-2024 signs the root from 2026-10-11. KSK-2017 is revoked 2027-01-11 and
  removed 2027-03-22. [DD:66; SR:70-71] **OWNER PROFILE DECISION 2026-10-13** (values under the A9.5 rule):
  - KSK-2017 signing period ends **2026-10-11T00:00:00Z**: IANA, the root zone begins using KSK-2024 on 2026-10-11
    and KSK-2017 ceases signing (SR:70-71; IANA sources as cited in `docs/reviews/v1-profile/CODEX-REVIEW.md` F2).
    Corroborated by the 2026-10-12 capture, whose only root DNSKEY RRSIG is by KSK-2024 with inception
    2026-10-11T00:00:00Z.
  - Observed root DNSKEY RRSIG validity, used as L: **21 days** (observed, not a proven maximum), from the archived captures. `prototype/spike/out/dns-snapshot.json`
    (captured 2026-10-09): the KSK-2017 RRSIG runs 2026-10-01T00:00:00Z to 2026-10-22T00:00:00Z (21 d), the only
    KSK-2017 root RRSIG archived. `prototype/spike/out-ksk2024/dns-snapshot.json` (captured 2026-10-12): the KSK-2024
    RRSIG runs 2026-10-11T00:00:00Z to 2026-11-01T00:00:00Z (21 d), corroborating. One KSK-2017 signature is the
    whole observed sample.
  - KSK-2017 reliance period ends **2026-11-01T00:00:00Z** (= 2026-10-11T00:00:00Z + 21 d). KSK-2024's reliance end
    stays open until its signing end is recorded.
  - The earlier end-of-day cutoff (2026-10-11T23:59:59Z) is **withdrawn**: it rejected authentic pre-retirement
    evidence anchored later (`docs/reviews/v1-profile/` F2). Extending reliance also extends a retired-key
    compromise window; A9.4 leaves historical key safety unevaluated either way.
  - Implemented in `prototype/spike/trust-config.json` (`signing_source`, `max_validity_source`, `reliance_rule`).
- **No usable trusted KSK — OWNER PROFILE DECISION 2026-10-13** (under R-2.26; repaired after
  `docs/reviews/v1-profile/` F1, F3). Each candidate signature is classified separately, and only after every trusted
  KSK has been tried:
  - a signature that verifies under a trusted KSK, is within its own RRSIG window, and whose KSK's reliance period
    contains the snapshot's anchored time: the set is valid, whatever the other candidates show;
  - otherwise, a signature that **verifies** but whose KSK's reliance period excludes that time:
    `INVALID / KSK_OUTSIDE_RELIANCE_PERIOD`;
  - otherwise, a signature that verifies but is outside its own inception/expiration window at that time: `INVALID`
    (`RRSIG_NOT_VALID_AT_EVAL_TIME` in the instrument);
  - otherwise, a signature bearing a trusted KSK's tag that does not verify: `INVALID`
    (`TRUSTED_KSK_SIGNATURE_INVALID` in the instrument). A key tag is a selector, not proof of authorship, so a
    forged tag never produces the reliance reason;
  - otherwise (signed only by keys the trust configuration does not hold, or the RRset, RRSIG or message missing):
    `UNVERIFIABLE / NO_TRUSTED_KSK_USABLE`.
  - **Superseding precedence** [OWNER 2026-10-14, r2-F04]. The list above is replaced by one candidate
    classification used for both root and repository checks (section 6.3). Each candidate is first classified:
    *eligible pass*; *horizon-unperformable* (verifies cryptographically, its RRSIG window and edge checks pass, and
    it is limited only by an open entry with T_snap > `as_of`); *finalized interval failure* (verifies, time-valid,
    reliance period of a finalized entry excludes the time); *time failure* (verifies; window or G27 edge failure);
    *crypto failure* (a trusted KSK's selector, does not verify); *no configured candidate*. Then: "Any eligible
    validating candidate passes. Otherwise a cryptographically validating, time-valid candidate limited only by an
    open horizon gives TRUST_HORIZON. Otherwise use finalized interval failure, time failure (including G27), crypto
    failure, then no configured candidate, in that order. Multiple reasons within one class use the G35 canonical
    candidate order." Codes: `UNVERIFIABLE / TRUST_HORIZON`; `INVALID / KSK_OUTSIDE_RELIANCE_PERIOD`; `INVALID /
    RRSIG_NOT_VALID_AT_EVAL_TIME`, `RRSIG_TIME_AMBIGUOUS` or `RRSIG_INTERVAL_REVERSED`; `INVALID /
    TRUSTED_KSK_SIGNATURE_INVALID` (these are now the profile's codes, not only the instrument's); a candidate
    bearing a trusted KSK's tag whose supported RDATA is malformed or whose non-temporal metadata is inconsistent is
    a crypto-class failure reported as `DNSSEC_FORMAT` / `DNSSEC_RRSIG_METADATA` (section 6.1); `UNVERIFIABLE /
    NO_TRUSTED_KSK_USABLE`. Horizon is claimed only after the key and signature are authenticated. Within the time
    class the edge reason follows section 15.7 (candidate G35 tuple, then endpoint inception before expiration,
    then ambiguous / reversed / window). This is an owner selection of Codex's proposed precedence: it keeps A9.5's
    existential rule, under which a failing extra candidate is informational while a validating one may still
    become eligible. *(Dated correction 2026-10-14: the list above gave verifying-but-outside-period as
    `KSK_OUTSIDE_RELIANCE_PERIOD` while the open-endpoint bullet below gave the same input `TRUST_HORIZON`, and it
    omitted the G27 edge reasons.)*
  - **Before signing start.** A cryptographically validating, time-valid candidate whose time precedes its KSK
    entry's `signing_start` is a finalized interval failure, `INVALID / KSK_OUTSIDE_RELIANCE_PERIOD`, whether the
    entry is open or finalized: the open horizon (`TRUST_HORIZON`) covers only time after `as_of`.
    [OWNER 2026-10-14, codified from diff-1, A08]
  - A snapshot without its own anchor is `UNVERIFIABLE / SNAPSHOT_NOT_ANCHORED`; no stand-in time is used. Missing
    snapshot evidence of any kind is `UNVERIFIABLE`, never an exception, unless another required check fails.
- **Unlisted rollover.** The periods are those known at release. A snapshot taken after an unlisted rollover is
  `UNVERIFIABLE`. [A9:150-151]
- **Root KSK material.** Each KSK entry holds its full DNSKEY RDATA (RFC 4034 §2.2) and the fields of section 15.5.
  A presented root DNSKEY is trusted only if its RDATA is byte-equal to an entry's `dnskey_rdata`; the DS digest is a
  cross-check. Byte equality excludes the RDATA when the presented RDATA has the REVOKE bit set; the reliance period,
  not revocation, supplies temporal exclusion. Publication and revocation dates are informational. The publisher
  takes each full public key from an archived authenticated source that contains it, or from an archived root DNSKEY
  RRset cross-checked against independently authenticated IANA material (`root-anchors.xml` and its `.p7s`, verified
  against the ICANN CA by a recorded bootstrap procedure), and records source digests. Proposed starts, to be
  confirmed against archived sources at freeze: ~~KSK-2017 signing start 2018-10-11T00:00:00Z~~; KSK-2024 signing
  start 2026-10-11T00:00:00Z. [OWNER 2026-10-14, G22]
- **Signing starts: evidence versus policy** [OWNER 2026-10-14, r2-F15]. IANA records KSK-2017 signing from
  2018-10-11 (the day is sourced); ICANN's operational account puts the switch at 16:00 UTC; neither establishes the
  inception of the first applicable root RRSIG. The freeze record keeps three values apart for each KSK: the
  operational switch time, the RRSIG inception evidence, and the chosen acceptance-policy `signing_start`, with
  rationale and archived source digests. **Owner choice (fail-closed):** KSK-2017's proposed policy
  `signing_start` is the sourced switch time **2018-10-11T16:00:00Z**, with a boundary vector; it is still OPEN
  until the sources are archived, and if historical RRSIG/ceremony evidence is obtained and differs, the freeze
  record says which value is chosen and why. KSK-2024's start (2026-10-11T00:00:00Z) and KSK-2017's end
  (2026-10-11T00:00:00Z) are likewise proposed acceptance-policy endpoints, not sourced exact signing events, until
  the same three-way record exists. *(Dated correction 2026-10-14: the proposed KSK-2017 start
  2018-10-11T00:00:00Z was a remembered day presented at midnight; midnight is not established.)*
- **Open endpoints.** `signing_end: null` means still signing as of the config's `as_of`. The finite reliance of an
  open KSK is [signing-start, `as_of`]; an open repository key is usable on [signing-start, `as_of`]. Evidence later
  than `as_of` under an open entry, with no other usable entry, gives `UNVERIFIABLE / TRUST_HORIZON`.
  [OWNER 2026-10-14, G09] Its rank among the other candidate outcomes is the r2-F04 precedence above (root) and in
  section 6.3 (repository); `TRUST_HORIZON` is listed in section 15.7. [OWNER 2026-10-14, r2-F04]
- **Release invariants** (checked before the release key signs) [OWNER 2026-10-14, G09]: identity, key bytes, D,
  signing-start and L of every existing entry are immutable; `as_of` is nondecreasing; `version` increases by 1 and
  `previous_sha256` binds the prior config; finalized ends are immutable; a transition null → end is allowed only if
  the resulting reliance end (signing-end + L for a KSK, signing-end for a repository key) is ≥ the previous
  config's `as_of`; pins are unique per height and existing pin hashes immutable; nothing is removed. These preserve
  eligibility granted through `as_of`. They do **not** preserve every verdict: appending pins can make an earlier
  attestation qualify and change T. A9.4's contract is exact output for identical declared inputs (the config is one);
  no monotonic-verdict promise is made.
- **Header pins.** A bundle header at a height with no pin gives `UNVERIFIABLE / HEADERS_NOT_COVERED`. A **selected**
  anchor (section 7.1) beyond the newest pin is `UNVERIFIABLE`; an unselected attestation without its headers
  supplies no fact and is not a failure. [A9:150; A9 C6 as revised 2026-10-14; OWNER 2026-10-14, G05]
- **Pin-set authentication** is the release allowlist above. [OWNER 2026-10-14, G08] *(Was: "`OPEN (other):` the
  key that signs the pin set, its format and its versioning rule. A9 says only 'signed, versioned'", 2026-10-13.)*
- **Repository custody.** "The repository key is the public half of an offline root" is an operating fact (RB §1),
  not verifier policy; no verifier check concerns custody. It is distinct from the release-key boundary above.
  [OWNER 2026-10-14, G36] *(Was: "`OPEN (other):` whether the repository key being the public half of an offline root
  is profile policy", 2026-10-13.)*

## 6. Authority channels

Both channels must pass (n = 2). Neither commits to any receipt. [A9:137, 147] Both carry the same issuance
window. [A9:332-333; ENC §7.1:630-634]

### 6.1 DNS channel

- Owner name is `_tessera-v1.<D>`. The verifier rebuilds it from the signed `issuer` and compares label by label,
  ignoring ASCII case. Anything else is `DNS_OWNER`. [ENC §7:551-556] This is the owner-name check (G-21 / M2).
- One TXT RRset, one RR, one character-string. The value grammar, the fifteen-step rejection order and the
  exact-255-byte rule are in ENC §7. [ENC §7:557-612]
- The record carries `kms`, `gpg`, `profile`, `issuance-not-before` and `issuance-not-after`, all mandatory, in a
  fixed order. [ENC §7:569-579]
- The DNSSEC chain is validated against the root rule (section 5) at the snapshot's own anchored time (section 7.3).
  [A9:137; A9:285-287]
- **Root rule first.** The root RRset passes only under A9.5: a byte-matching configured KSK, usable in its reliance
  interval at T_snap, verifies a selected RRSIG valid at T_snap. The algorithm profile below never replaces that
  eligibility condition. Candidate aggregation is existential and order-independent; extra candidates are
  informational after any eligible supported path passes. Root outcomes and their precedence are section 5's.
  [OWNER 2026-10-14, G16]
- **Supported DNSSEC set (NARROW-CLAIM, visible owner scope choice).** DNSKEY and RRSIG algorithms 8 (RSA/SHA-256,
  RFC 5702, key per RFC 3110) and 13 (ECDSA P-256/SHA-256, RFC 6605); DS digest types 2 (SHA-256, RFC 4509) and 4
  (SHA-384, RFC 6605). The DNSKEY used has the Zone Key flag set, REVOKE clear, protocol 3. Validation is RFC 4035
  §5.3.1–5.3.3 at T_snap with RFC 4034 §6 canonical form. DS is signed by a key in the parent's validated DNSKEY
  set; a child DNSKEY RRset is self-signed by a key matching a validated DS; the TXT is signed by a key in its zone's
  validated DNSKEY set. [OWNER 2026-10-14, G16]
- **Outcomes for each non-root required RRset**, computed once after every candidate is tried [OWNER 2026-10-14,
  G16]:
  1. some supported path (matching authenticated DS → DNSKEY → RRSIG) validates at T_snap: pass;
  2. else the RRset or the witness RRSIG it needs is missing: `UNVERIFIABLE / DNS_EVIDENCE_MISSING`;
  3. else an unsupported algorithm or digest type could supply the path: `UNVERIFIABLE /
     DNSSEC_ALGORITHM_UNSUPPORTED`;
  4. else (every possibility supported and checked) a candidate verifies but its window excludes T_snap, or its
     times are edge failures (section 7.3): `INVALID / RRSIG_NOT_VALID_AT_EVAL_TIME` (or that edge reason);
  5. else a supported candidate fails cryptographically: `INVALID / DNSSEC_SIGNATURE_INVALID`;
  6. else no child DNSKEY matches a validated DS: `INVALID / DNSKEY_DS_MISMATCH`.
- **Complete candidate table** [OWNER 2026-10-14, r2-F05]. Supersedes the six rows above where they differ. DS →
  DNSKEY matching (DNSKEY RRsets) is separate from RRset → RRSIG → DNSKEY matching (DS and TXT RRsets, and each
  DNSKEY RRset's self-signature). Each candidate takes the first failing RFC 4035 §5.3.1 precondition below; the
  RRset outcome is computed once, after every candidate:
  1. some supported eligible path validates at T_snap: pass;
  2. else the RRset, its witness RRSIG, or the signer zone's DNSKEY RRset is absent: `UNVERIFIABLE /
     DNS_EVIDENCE_MISSING`;
  3. else a **potentially usable unsupported path** exists: `UNVERIFIABLE / DNSSEC_ALGORITHM_UNSUPPORTED`. Defined
     by authenticated DS metadata and matching selectors only: for a DNSKEY RRset, an authenticated DS of
     unsupported digest type or algorithm whose key tag and algorithm match a child DNSKEY; for any RRset, an RRSIG
     of unsupported algorithm whose signer name, algorithm and key tag match a DNSKEY in the signer zone's
     authenticated set. An unrelated unsupported RR does not qualify;
  4. else the parent's authentication is blocked (the parent RRset's outcome is unperformable) and some candidate is
     locally valid (well-formed, metadata consistent, verifies under a supplied matching DNSKEY of its signer zone,
     window contains T_snap): the authenticated-path check is unperformable and carries no reason of its own (the
     parent's reason is earlier in section 15.7);
  5. else, `INVALID`, by the most-progressed failing candidate, in this order: verifies but window or edge failure
     (`RRSIG_NOT_VALID_AT_EVAL_TIME`, `RRSIG_TIME_AMBIGUOUS`, `RRSIG_INTERVAL_REVERSED`); supported candidate fails
     cryptographically (`DNSSEC_SIGNATURE_INVALID`); present supported witness with no matching eligible DNSKEY
     (signer name, algorithm and key tag matching a DNSKEY with Zone Key set, protocol 3, REVOKE clear) in the
     signer zone's set (`DNSSEC_KEY_MISMATCH`); no child DNSKEY matches a validated DS (`DNSKEY_DS_MISMATCH`);
     Labels greater than the owner's label count, or other non-temporal metadata mismatch (`DNSSEC_RRSIG_METADATA`);
     malformed supported DNSKEY or RRSIG RDATA (`DNSSEC_FORMAT`). Ties within a class: G35 candidate order.
  Locally obtainable checks (framing, TXT grammar, signature mathematics against supplied keys) run whether or not
  the parent is authenticated; under row 4 they become reportable failures (row 5) only when no candidate of that
  RRset is locally valid, which preserves the existential rule. This is the bridge from RFC 4035's failures to the
  V1 partition, not a claim that RFC 4035 is unspecified. **Owner choice (fail-closed):** an unmatched selector is
  `INVALID / DNSSEC_KEY_MISMATCH`, not insufficient evidence; the honest issuer validates the chain before
  shipping. *(Dated correction 2026-10-14: the six rows above gave no outcome for an unmatched key tag, Labels
  defects, bad flags/protocol or malformed supported RDATA, and "an unsupported algorithm could supply the path" did
  not define which candidates count.)*
  - **Unrelated unsupported witness only.** An RRSIG of an unsupported algorithm whose signer name, algorithm and
    key tag match no DNSKEY in the signer zone's set is neither a potentially usable unsupported path (row 3) nor a
    supported witness (row 5's `DNSSEC_KEY_MISMATCH`). If it is the only RRSIG covering the RRset, the RRset has no
    usable witness: `UNVERIFIABLE / DNS_EVIDENCE_MISSING` (row 2). The fail-closed unmatched-selector choice above
    applies to supported-algorithm witnesses only. [OWNER 2026-10-14, codified from diff-1, EA-11]
  - **RSA signature width.** An algorithm-8 RRSIG whose signature field is not exactly the modulus length of the
    DNSKEY it is checked against is malformed supported RRSIG RDATA, `INVALID / DNSSEC_FORMAT`, not
    `DNSSEC_SIGNATURE_INVALID`. [OWNER 2026-10-14, codified from diff-1, A13]
- **Relying-party text (visible limit).** A chain that moves to an algorithm outside {8, 13} (for example Ed25519,
  algorithm 15) makes new snapshots `UNVERIFIABLE` under this frozen spec; the issuer does not ship such receipts.
  [OWNER 2026-10-14, G16]
- **No wildcards (NARROW-CLAIM).** A TXT RRSIG whose Labels field is less than the owner's label count gives
  `INVALID / DNS_WILDCARD`. The issuer publishes an explicit record. [OWNER 2026-10-14, G19]
  - **Owner choice: a global body restriction, not witness eligibility** [OWNER 2026-10-14, r2-F07]. The rule
    above is a **transport restriction on the snapshot body** (the "no-wildcard body restriction"), separate from
    witness eligibility: any RRSIG anywhere in the body whose Labels field is less than its owner's label count
    gives `INVALID / DNS_WILDCARD`, even beside a valid explicit-owner witness. Accordingly the promise that extra
    candidates are informational after an eligible path passes (above, and section 7.3) does **not** cover such an
    RRSIG. Chosen as the fail-closed reading; the honest issuer publishes an explicit record and checks the body
    before stamping (section 4). *(Dated correction 2026-10-14: the bullet left open whether an extra wildcard
    candidate beside a valid explicit witness rejects the snapshot; it now does. It previously named only TXT
    RRSIGs.)*
- **Inherited residual.** An ancestor zone (root, `com`) can sign data for names below it; V1 inherits that DNSSEC
  trust, and the git channel (n = 2) guards against it. [OWNER 2026-10-14, G19]

### 6.2 Issuance window (C4 verifier rule)

- The window `issuance-not-after − issuance-not-before` is at most 90 days. A record that violates it is rejected
  (`DNS_WINDOW_LENGTH`). V1 has one window and no overlap. [A9:334-337; ENC §7:578-580]
- A receipt is `INVALID / ISSUANCE_WINDOW` unless `issuance-not-before` ≤ declared issue time and T ≤
  `issuance-not-after`. Both bounds are inclusive. T is compared as registered, with no margin. T is not compared
  with not-before. [A9:338-340; ENC §7.1:636-643, 662-663]
- The guarantee is in chain time. A UTC cutoff would need a backward-skew bound V1 does not establish. [A9:360-366;
  ENC §7.1:661-671]
- A published window cannot be shortened. [A9:343]
- The window, its dates and the stop margin are operating facts, not profile rules. [A9:341-342; RB §2]

### 6.3 Git channel

The OTS stamp targets the signed commit's object id, never a tree, blob or unsigned commit. [A9:282-284; ENC
§7.2:685-691] The verifier does four things:

1. Recomputes the commit id from the presented raw commit object.
2. Verifies `gpgsig` over the object without that header, under the pinned repository key.
3. Follows commit, then tree, then blob, down the fixed path below.
4. Checks that the stamped bytes name that id.

[ENC §7.2:706-710] SHA-1 linkage (the commit id and the commit-tree-blob links) is a stated residual. [A9:284;
ENC §7.2:712-718]

ENC §7.2 says the blob's path and any byte framing around the value are "not P8's" (ENC:680-682). These three owner
profile decisions fill that gap (section 0.1, items 1 and 2). Reference implementation, instrument only:
`prototype/tessera_proto/real/gitchannel.py` (`verify_key_path`; `verify_profile_key_assertion` pins the fixed path
and compares the blob with the validated DNS TXT value byte for byte), tests in `prototype/tests/test_gitpath.py`.
Coverage limit: the instrument does not yet verify `gpgsig` under the pinned key, the commit's OTS stamp, or signed
issuer == pinned D together with the path (`docs/reviews/v1-profile/` F7).

- **Closed git grammar** (OWNER CHOICE, supported-path limit): commit headers, armor, canonical trees, the path,
  SHA-1 with collision detection, and the P-256 repository key, exactly as section 15.4. [OWNER 2026-10-14, G25]
- **Repository signer.** If some repository entry for D verifies `gpgsig` and its interval contains T_git, the check
  passes; if one verifies but its interval excludes T_git, `INVALID / GIT_SIGNER_OUTSIDE_INTERVAL`; if none verifies,
  `UNVERIFIABLE / GIT_SIGNER_NOT_CONFIGURED`. [A9.5; OWNER 2026-10-14, G25]
  - **Candidate precedence** [OWNER 2026-10-14, r2-F04]: section 5's classification, with repository entries as
    candidates: any entry for D that verifies with T_git in its interval passes; otherwise a verifying entry
    limited only by an open interval with T_git > `as_of` gives `UNVERIFIABLE / TRUST_HORIZON`; otherwise a
    verifying finalized entry whose interval excludes T_git gives `INVALID / GIT_SIGNER_OUTSIDE_INTERVAL`;
    otherwise `UNVERIFIABLE / GIT_SIGNER_NOT_CONFIGURED`. Multiple entries in a class are ordered by (signing_start,
    key bytes). *(Dated correction 2026-10-14: an open entry verifying at T_git > `as_of` was both
    `GIT_SIGNER_OUTSIDE_INTERVAL` here and `TRUST_HORIZON` in section 5.)* A verifying entry with T_git before its
    `signing_start` is `INVALID / GIT_SIGNER_OUTSIDE_INTERVAL`, open entries included: the open horizon covers
    only T_git > `as_of`. [OWNER 2026-10-14, codified from diff-1, A08]
  - **Git signature mapping** [OWNER 2026-10-14, r2-F11]: every armor, codec and rule-O policy violation of the
    `gpgsig` value is `INVALID / GIT_SIG_FORMAT` (the exception to section 8's generic `SIG_POLICY`); failed
    mathematics, including a hash-prefix mismatch, is "none verifies" above (`GIT_SIGNER_NOT_CONFIGURED`).
- **Descriptor and stamp.** `object_format` absent gives `UNVERIFIABLE / GIT_OBJECT_FORMAT_MISSING`, a value other
  than `"sha1"` gives `UNVERIFIABLE / GIT_OBJECT_FORMAT` (A9.5). The proof's file digest is SHA256 of the 40
  lowercase hex commit id plus LF, else `INVALID / GIT_STAMP_MISMATCH`. The V1 verifier checks each receipt's own
  window and does not check non-overlap between receipts; successor registration is an issuance duty. [A9.5, A9.6;
  OWNER 2026-10-14, G39]

- **OWNER PROFILE DECISION 2026-10-13 (path).** The key-assertion blob is at the fixed path `tessera-v1/key-assertion` in the
  issuer repository. One window per record (A9:334-337) means one path is enough. A rotation mechanism, if one is ever
  registered, must define its own paths. [ENC §7.2:680-682 for the gap; A9:334-337]
- **OWNER PROFILE DECISION 2026-10-13 (framing).** None. The blob's bytes equal the ENC §7 canonical value byte for byte. A
  trailing LF or any other byte is rejected. The leaf tree entry mode must be 100644 and each intermediate entry must
  be 40000. [ENC §7:566-586; ENC §7.2:679-682] A blob that is the DNS value plus a trailing LF (or any other extra
  or differing byte) is rejected by row 15.2 as `INVALID / CHANNEL_VALUE_MISMATCH`, not as `GIT_PATH`.
  [OWNER 2026-10-14, codified from diff-1, EA-21]
- **OWNER PROFILE DECISION 2026-10-13 (issuer domain D in the git channel).** The ENC §7 value does not carry D, so D is not
  extracted from the blob. D comes from the verifier's trust configuration, which pins the pair (D, repository root
  key). The git channel is accepted only for the pinned D. The verifier checks that the D bound in the receipt's
  signed bytes (`common.issuer`) equals the pinned D. [ENC §7:566-575; ENC §3.2:279]
  - **Correction.** This supersedes the derivation draft's "exact extraction of D and the key set" (DD:94). The key
    set is still taken from the blob, parsed with the ENC §7 grammar. D is not.
- The git value and the DNS value must be identical, window included. [A9:333; ENC §7.2:679-681]
- **One pinned-D gate for both channels.** Before either channel, `common.issuer` must be exactly `wamason.com`,
  the profile constant D, which must also equal the trust configuration's `issuer_domain`; otherwise
  `INVALID / ISSUER_NOT_PINNED`. With git evidence absent and another D, the result is `INVALID`, not
  `UNVERIFIABLE`. [OWNER 2026-10-14, G34] *(Was: "`OPEN (step 8):` whether the pinned-D equality check also gates the
  DNS channel", 2026-10-13.)*
- **Git time relation.** Let T_git and h_git be the git proof's T and selected height (section 7.1 rule on the git
  proof), and h_receipt the receipt proof's selected height. The git assertion must satisfy:
  - T_git lies in some configured repository-key interval for D (A9.5);
  - **chain-order pre-commitment: h_git + 5 < h_receipt**, else `INVALID / GIT_NOT_PRECOMMITTED` (A9 C4 as revised
    2026-10-14, OWNER DECISION, BROADEN);
  - no upper bound from δ.

  The same window value is authenticated by the anchored git assertion and by DNSSEC at the snapshot's own anchored
  time. No clock comparison between T_git and the declared issue time is made. *(Owner 2026-10-14: the `T_git ≤ declared_issue_time` check was dropped. Chain order carries the protection, and the clock check only added an nTime false-reject hazard on the honest path.)* Before
  honest issuance the issuer obtains and validates the git assertion's k=6 proof. The chain-order rule establishes
  that the window was confirmed at k = 6 in the chain before the receipt was anchored; pre-commitment is chain order,
  not UTC (A2.1), and DNSSEC evidence establishes no publication before issue. [OWNER 2026-10-14, G02] *(Was:
  "`OPEN (step 8):` the time relation the git assertion must have to the receipt", 2026-10-13. Dated correction
  2026-10-14: ENC §7.1's "fixed in DNSSEC-authenticated and anchored authority evidence before any receipt that
  relies on it" overstates both channels; the replacement wording for ENC is pending.)*

### 6.4 Required set, owner name and manifest (step 8 fixes)

- **G-21 / M2 (owner name).** Decided for DNS (section 6.1). Decided for git by the pin (section 6.3). [A9:202;
  FT:19, 39] **M2:** "For both channels the authority evidence is for D = `common.issuer` = `wamason.com`. On DNS,
  the validated TXT owner equals `_tessera-v1.<D>` label by label, ignoring ASCII case. On git, the commit verifies
  under a repository entry whose domain is D." [OWNER 2026-10-14, G34] *(Was: "`OPEN (step 8):` write M2",
  2026-10-13.)*
- **G-17 (verifier-fixed required set).** Decided: the verifier fixes the required set. It does not read it from the
  bundle. [A9:137; DD:93; FT:21] **V1 value:** {direct-form evidence on the DNS channel, direct-form evidence on the
  git channel}; in each channel the statement is the ENC §7 canonical value, which publishes the fingerprints
  directly (R-4.30). The signed `common.binding_forms` must equal `["STMT_DIRECT"]`: element by element in canonical
  order, `STMT_DIRECT` is accepted, `STMT_DIGEST` gives `UNVERIFIABLE / BINDING_FORM_UNSUPPORTED`, any other id
  gives `UNVERIFIABLE / BINDING_FORM_UNKNOWN`, and the reported reason is the first offending element's. This is an
  owner selection, not an extraction of ENC's illustrative value. [OWNER 2026-10-14, G01] *(Was: "`OPEN (step 8):`
  the V1 value of the fixed set … the check on the signed `common.binding_forms` … how the DNS and git records …
  correspond to a binding form", 2026-10-13.)*
- **M5 (manifest = authority tuple).** [FT:22, 39] **M5:** "The manifest tuple (`alg`, `issuer`, `key_fp`, `sset`,
  `ver`) is fully determined by authenticated sources. `key_fp` and `sset[0]` equal the DNS value's `kms`/`gpg`
  (prefix-adjusted, ENC §3.3), and the git blob is byte-equal to that DNS value. `issuer` equals the DNS owner
  name's suffix and the pinned D. `alg` equals the frozen catalog's single registered id, and `ver` = `map-v1`
  (schema). No tuple field is free of either channel authentication or a single-valued profile constant. The
  constants are policy-authenticated by the verifier's frozen catalog; they are not channel-signed tuple fields."
  Mismatches give `INVALID`: `DNS_KEY_MISMATCH`, `CHANNEL_VALUE_MISMATCH`, `ISSUER_NOT_PINNED`, or the codec's
  `SCHEMA`. [OWNER 2026-10-14, G10] *(Was: "`OPEN (step 8):` state it", 2026-10-13.)* The `alg` condition is
  performable only for the policy-supported id; for any other well-formed id it contributes `UNVERIFIABLE /
  ALG_UNKNOWN`, not an additional `SCHEMA` failure (section 1). [OWNER 2026-10-14, r2-F01]
- **Receipt consistency, explicit** [OWNER 2026-10-14, r2-F02]: "Both frames' signer fingerprints equal the
  corresponding manifest fingerprints (RECEIPT_SLOT); their common byte substrings are equal
  (RECEIPT_COMMON_MISMATCH); common issuer and alg equal manifest issuer and alg (RECEIPT_MANIFEST_MISMATCH). Stage 4
  checks common.manifest_sha256 against SHA256(F_manifest), using RECEIPT_MANIFEST_MISMATCH; when both common objects
  are available, check each in kms/gpg order. These checks never require signature validity or channel
  authentication." All are `INVALID`. Anchor digest verification stays in the receipt OTS check; with the
  `a_sig`-only route there is no second externally transported tuple to reconcile. A9's bytes/signature binding
  remains required; this completes the specification and permits omitting none of these checks. Listed in section
  15.7 (rows 4 and 6).
- **W1 (malleability).** Decided. No V1 semantic, standing or attempt identifier is derived from signature bytes. The
  anchor digest commits to them by design and is not an identifier. V1 does not require unique signatures and
  normalizes none. The unhashed OpenPGP area carries no meaning. A changed signature fails the anchor
  (`RECEIPT_ANCHOR_MISMATCH`). [ENC §3.5:339-355; ENC §8:735-739; A9:280-281] The half-day argument that no strict
  query relies on signature uniqueness is a separate item (DD:89; step 10).

## 7. Time

### 7.1 The T rule

- T is the time of the verified attestation at the **lowest block height** in the presented OTS proof; both T and
  its confirmations come from that attestation. It is presentation-sensitive: a different presentation of the same
  receipt can select a different T. [A9 C5 as revised 2026-10-14; DD:56, 98-99; OWNER 2026-10-14, G03] *Dated
  correction 2026-10-14: this bullet previously read "T is the time of the earliest verified attestation", A9's
  earlier wording. "Earliest" means chain order, not least nTime: header times are not monotone, and the two
  selection rules can give different verdicts on the same proof.*
- No lower bound and no priority. Header times are chain-time proxies. [A9:138]
- The three conjuncts at k = 6 (`DepthK = k − 1 = 5`): `declared − ε ≤ anchor_time`; `anchor_time ≤ declared + δ`;
  `confirmed_at ≤ declared + δ`. All three are evaluated together. [SPEC R-4.41:985; SPEC R-5.19:1352; SPEC
  V33-V36:1342-1346; A9:99]
- A real proof carries several attestations hours apart and nothing in the proof names T (M3). [FT:20; DD:98]
- **T ≡ `anchor_time`.** For the receipt proof, T = `anchor_time` = nTime(h*), where h* is the lowest qualifying
  height. The same value feeds conjuncts 1 and 2, the C4 window rule and the reported T. Two qualifying attestations
  at the same height give the same T. [OWNER 2026-10-14, G03] *(Was: "`OPEN (step 8):` one sentence stating whether
  T is the `anchor_time` of the three conjuncts", 2026-10-13.)*
- **`confirmed_at`** = nTime(h* + 5): the including block plus five successors, k = 6 (SPEC R-3.45, R-4.42). A
  failure gives `INVALID`: `TIME_BEFORE_DECLARED_EPSILON`, `TIME_AFTER_DECLARED_DELTA` or `CONFIRMATION_LATE`.
  Nonmonotone header times can give `confirmed_at` < T; that is not a failure, and there is no monotonicity check.
  [OWNER 2026-10-14, G04]
- **Qualifying ("verified") attestation.** A Bitcoin attestation at height h qualifies if and only if (a) the
  bundled header at h exists and its merkle root equals the attestation message; (b) headers h … h+5 are all
  bundled; (c) each equals its pin, `hex(reverse(SHA256d(header))) = pin[height]`; (d) for i = h+1 … h+5,
  `header_i.prev = SHA256d(header_{i−1})`. [OWNER 2026-10-14, G05] *(Was: "`OPEN (step 8):` what 'verified' means
  for an attestation", 2026-10-13.)*
- **Selection.** Attestation selection is existential over qualifying branches. A syntactically valid Bitcoin
  attestation without a complete h..h+5 segment is nonqualifying, not a required failed check. It supplies no time or
  trust fact. All supplied headers, including unused ones, are independently checked against pins (section 7.2).
  The selected anchor, rather than every unverified attestation, is the referent of "anchors beyond the newest pin"
  (A9 C6 as revised 2026-10-14). [OWNER 2026-10-14, G05]
- **Proof outcomes.** A pinned bundled header at h whose merkle root ≠ the attestation message: `INVALID /
  OTS_MERKLE_MISMATCH` (a contradicted branch fails the proof). No qualifying attestation: `UNVERIFIABLE /
  HEADERS_MISSING` if any Bitcoin attestation is present, `UNVERIFIABLE / ANCHOR_PENDING_ONLY` if only pending ones;
  the snapshot uses `SNAPSHOT_NOT_ANCHORED` and git `GIT_NOT_ANCHORED`. [OWNER 2026-10-14, G05]
- **Time arithmetic.** Times are integer seconds since 1970-01-01T00:00:00Z without leap seconds; nTime is the
  header's uint32; RFC 3339 fields convert by days-from-civil (proleptic Gregorian); comparisons are inclusive.
  [OWNER 2026-10-14, G03]
- **OTS and txid encoding**: section 15.2. [OWNER 2026-10-14, G20]
- **txid scope and selected-height aggregation** [OWNER 2026-10-14, r2-F08]: "§15.2's transaction-shape and
  txid-equality check applies only to receipt_anchor. The snapshot/git proofs use the closed OTS grammar and header
  qualification, with no txid comparison. Select h* before the receipt txid check; any satisfying qualifying path at
  exactly h* passes that check. Never switch to a higher height merely to find a matching txid." **Owner choice
  (fail-closed), stated separately:** the **transaction-shape and merkle-suffix subset** (section 15.2, parts 1, 2
  and 4, without part 3's txid comparison) also applies to the selected height of the snapshot and git proofs; a
  failure there is `INVALID / OTS_TX_SHAPE`, and any qualifying path at exactly that proof's h* satisfying the
  subset passes. No receipt txid is compared with the snapshot or git proof; the three proofs normally anchor in
  different transactions. *(Dated correction 2026-10-14: section 15.7's "OTS (as 11 …)" imported the receipt's
  txid check into proofs that carry no txid.)*

### 7.2 Header pins

- Every bundle header must be in the pinned set. Otherwise the verdict is `UNVERIFIABLE / HEADERS_NOT_COVERED`.
  There is no retarget logic, because the pins cover every accepted header. [A9:150; DD:99]
- **Conflict.** A supplied header at a pinned height with a different hash gives `INVALID / HEADER_CONFLICTS_PIN`:
  it is contradictory evidence. A9.1's "a bundle header outside the pins" is read as a header **at a height the pins
  do not cover**. [OWNER 2026-10-14, G23] *(Was: "`OPEN (step 8):` the verdict for a header that … conflicts with a
  pin", 2026-10-13.)*
- **Coverage.** Required: headers h* … h*+5 of the selected attestation of each of the three proofs (receipt,
  snapshot, git), all in the shared `headers` pool. Every supplied header, used or not, is checked against the pins.
  A `headers` entry that fails row 2.4 is not a supplied header: it contributes `CONTAINER_SCHEMA` only, and rows
  10.x, 11.x, 13.4 and 14.6 use the remaining entries [OWNER 2026-10-14, diff-1 F-3].
  For each pair of supplied headers at consecutive heights, a prev-hash mismatch gives `INVALID /
  HEADER_CHAIN_BROKEN`; a missing intermediate height is not a broken link. No PoW, nBits or retarget check: a hash
  equal to a pin implies all of it. At an unselected height, a pinned header with missing successors is ignored,
  while an unpinned header blocks the bundle (`HEADERS_NOT_COVERED`). [OWNER 2026-10-14, G07, G05] *(Was: "`OPEN
  (step 8):` which heights the pins must cover for a given proof", 2026-10-13.)*

### 7.3 The DNSSEC snapshot rule

- The issuer anchors the DNSSEC snapshot with its own OTS proof. The envelope is ENC §6 under the tag
  `tessera-v1/dnssec-snapshot`. [DD:94; ENC §6:536-542]
- The verifier checks that the snapshot's anchored time lies inside every RRSIG window in the chain and within
  [declared − ε, declared + δ]. The issuer re-captures before shipping if it does not. [DD:94] This is an owner
  decision carried in, not routed. [A9:99-101]
  - "declared" is the receipt's signed `declared_issue_time`, not the snapshot's capture time. Capture-to-anchor
    latency is a separate observation, not this predicate. (`docs/reviews/v1-profile/` F6, accepted 2026-10-13.)
  - "every RRSIG window in the chain" means the one witness signature selected to authenticate each required RRset,
    not every signature offered: an extra expired or invalid signature beside a valid one neither fails the RRset
    nor narrows the joint window. The instrument's selection order is (key tag, inception, expiration, signature
    bytes), first that validates. (`docs/reviews/v1-profile/` F5, accepted 2026-10-13.) Exception: an RRSIG
    with fewer Labels than its owner fails the body restriction wherever it appears (section 6.1).
    [OWNER 2026-10-14, r2-F07]
  - **Frozen witness rule.** The selected witness is the **first eligible validating** candidate in (key tag,
    inception, expiration, signature bytes, canonical RRSIG RDATA, canonical key RDATA) order. For the root, reliance
    eligibility precedes selection. [OWNER 2026-10-14, G35] *(Previously described only as the instrument's order.)*
  - Conjunct 3 (`confirmed_at` of the snapshot ≤ declared + δ) is a new owner acceptance restriction, fail-closed. A
    failure of any conjunct gives `INVALID / SNAPSHOT_TIME`. [OWNER 2026-10-14, G06]
- The chain is evaluated at the snapshot's anchored time, not at T of the receipt. [A9:137]
- Why: the joint RRSIG window measured 1.6 days, shorter than δ (M8). [DD:93]
- **Snapshot body.** A fixed-order sequence of uncompressed RFC 1035 wire RRs in RFC 4034 §6.2 canonical form,
  section 15.3. Framing violations are `INVALID / SNAPSHOT_FORMAT`; a syntactically complete body lacking a required
  RRset or its witness RRSIG is `UNVERIFIABLE / DNS_EVIDENCE_MISSING` (root: `NO_TRUSTED_KSK_USABLE`). The conversion
  from resolver messages happens before stamping and changes S, so each snapshot needs a fresh stamp; earlier
  stamped JSON snapshots cannot be reused. [OWNER 2026-10-14, G19] *(Was: "`OPEN (step 8):` the snapshot body
  format", 2026-10-13.)*
- **Snapshot time.** T_snap = T of the snapshot's own proof under the section 7.1 rule, at the same depth k = 6, and
  `confirmed_at`(snapshot) likewise. DNSSEC is evaluated at T_snap only; no capture time, receipt T or wall clock is
  ever used. [OWNER 2026-10-14, G06] *(Was: "`OPEN (step 8):` how the snapshot's anchored time is derived",
  2026-10-13.)*
- **RRSIG time arithmetic.** Inception and expiration are 32-bit values v, each resolved to the unique absolute
  second t with t ≡ v (mod 2^32) and |t − T_snap| < 2^31 (RFC 4034 §3.1.5, RFC 1982). If v − T_snap ≡ 2^31 (mod 2^32)
  the candidate fails with `RRSIG_TIME_AMBIGUOUS`; if resolved inception > expiration it fails with
  `RRSIG_INTERVAL_REVERSED`; inception = expiration is allowed. These are candidate failures under the existential
  rule, ranked with `RRSIG_NOT_VALID_AT_EVAL_TIME`. The witness check is inception ≤ T_snap ≤ expiration, never "now",
  including in 2106. [OWNER 2026-10-14, G27]

## 8. Signers and keys

- Fallback: both slots OpenPGP P-256 (rule O), KMS-backed for kms, and slot-2 custody per A9.6 for gpg. The dated pre-freeze custody record identifies the selected implementation. [A9.6 "Signers" (was cited A9:338-340, a stale locator; OWNER 2026-10-14, r2-F17); A9.6 slot-2 custody; ENC §5.2:438-444; `docs/reviews/a9-custody/` finding 3]
- Hybrid, only if the spike passes by 21 Oct: `kms` is ML-DSA-65 (rule R), `gpg` is P-256 (rule O). One pair
  algorithm id names both. [A9:298-302; ENC §5.2:441]
- Key fingerprints: `spki-sha256:` for `kms`, `gpg-sha256:` for `gpg`. No SHA-1 for key binding. [ENC §3.3:285-301]
- The two keys are separate technical failure domains under one controller. V1 claims no separation of control and no
  independent fates. [A9:136; A9:368-372]
- Each slot's signature is exactly one detached signature in the serialization its rule pins. [ENC §5.2:429-436]
- **Transported keys.** `keys.gpg` is the bare v4 public-key packet body, exactly the `gpg-sha256` preimage (no
  `0x99` prefix, packet header, user IDs, subkeys or armour). gpg must parse as the specified v4 P-256 public-key
  body. kms must parse as P-256 DER SPKI under the fallback, or as the exact ML-DSA-65 SPKI specified by the dated
  branch supplement under the hybrid. The rule is selected by the installed governing spec and slot, never by key
  bytes alone. Otherwise `INVALID / KEY_FORMAT`; a key not hashing to its slot fingerprint is `INVALID /
  KEY_MISMATCH`. [OWNER 2026-10-14, G21] Under the fallback, any `keys.kms` that is not a P-256 DER SPKI,
  including an ML-DSA-65 SPKI (OID 2.16.840.1.101.3.4.3.18), is `INVALID / KEY_FORMAT`; this outcome does not depend
  on the hybrid supplement's exact SPKI encoding. [OWNER 2026-10-14, codified from diff-1, EA-24]
  **Scope of the key-format rule (OWNER DECISION 2026-10-14, EA-31; supersedes the literal reading of the sentences
  above where they conflict).** The installed-spec key rule applies only when the receipt's `common.alg` is the
  installation's catalog-supported id (row 7.1). For a well-formed but unsupported alg, key format, key/fingerprint
  semantics, signatures and possession are not evaluated (r2-F01), and the outcome is `UNVERIFIABLE / ALG_UNKNOWN`,
  not `KEY_FORMAT`. So a genuine hybrid receipt shown to a fallback installation, or a fallback receipt shown to a
  hybrid installation, is "cannot evaluate", never "invalid". Rationale: an examiner holding the wrong installation
  must not be told that an honest receipt is forged. EA-24 still holds when the receipt's alg IS the fallback id
  and its kms key is ML-DSA: that is a malformed fallback receipt.
  **Codec registry per installation (OWNER DECISION 2026-10-14, differential run 4).** An installation's codec
  registry is the ENCODING-V1 baseline plus only the supplement(s) that installation registered. A fallback
  installation, which has no hybrid supplement, does not know the hybrid pair id: frames bearing it use the opaque
  codec (its length cap), and semantics give `UNVERIFIABLE / ALG_UNKNOWN`. A hybrid installation knows both ids,
  because the classical id is in the baseline: the classical id uses rule O, then `ALG_UNKNOWN` for semantics (case
  (b)). Knowing an id's codec is a property of the installation, never of the verifier's source code.
- **Rule-O signature policy** (attestation, possession and git signatures; OWNER CHOICE, supported-path limit)
  [OWNER 2026-10-14, G11]:
  - ENC §5.2's grammar holds.
  - Hashed area: exactly one signature-creation-time subpacket (type 2) with exactly four data octets, critical or
    not, never compared with anything; no signature-expiration subpacket (type 3), critical or not; issuer key ID
    (16) and issuer fingerprint (33) accepted critical or not and never read (no SHA-1 key binding, D-6); any other
    type ignored if not critical and a failure if critical.
  - Unhashed area: ignored entirely, critical bits included (ENC §3.5: the unhashed area carries no meaning).
  - ECDSA per FIPS 186-5 with r, s ∈ [1, n−1]; low-s not required.
  - **Out-of-range r or s.** An r or s outside [1, n−1] is a policy failure, `INVALID / SIG_POLICY` (rows 9.1, 9.4;
    git: `GIT_SIG_FORMAT`, section 6.3), not `SIG_INVALID`, except that an r or s of zero fails ENC §5.2's MPI
    grammar (1 to 256 bits) first and is `SIG_FORMAT` (git: `GIT_SIG_FORMAT`). [OWNER 2026-10-14, codified from
    diff-1, EA-23/A11]
  - Policy failure: `INVALID / SIG_POLICY`. Failed verification: `SIG_INVALID`, or `POSSESSION_INVALID` for the
    manifest possession signatures. Possession proofs use the same per-slot rule over `F_manifest` (rule R for kms
    under the hybrid). No revocation or current-time checks.
  - **Advisory metadata, structural validation (owner choice, fail-closed)** [OWNER 2026-10-14, r2-F10]. Codex's
    proposal treated types 16 and 33 as opaque advisory octets; the owner instead selects exact structural
    validation, in the hashed area: at most one type-16 subpacket, with exactly 8 data octets; at most one type-33
    subpacket, with exactly 21 data octets whose first octet is `04` (v4 fingerprint); if both are present, the
    type-16 value equals the last 8 octets of the type-33 fingerprint. Otherwise `INVALID / SIG_POLICY`. A
    zero-data critical type 33 is therefore `SIG_POLICY`. Their values are never compared with the transported
    key and confer no key-selection authority; critical bits are recognized and confer nothing. Other unhashed
    contents are semantically ignored after structural parsing under ENC (subpacket framing still holds). This
    overrides generic OpenPGP metadata interpretation for V1 and is not a claim of full RFC metadata conformance;
    no keyring library decides it. GnuPG's output (hashed type 33 of 21 octets, type 16 unhashed) satisfies it.
    *(Dated correction 2026-10-14: "accepted critical or not and never read" left payload length, repetition and
    cross-field consistency unspecified.)*
  - **Hash prefix** [OWNER 2026-10-14, r2-F10]: the two hash-prefix octets must match the first two octets of
    SHA256(document ‖ ENC trailer), else `SIG_INVALID` / `POSSESSION_INVALID` (git: its signature-verification
    outcome, section 6.3).
  - **Public-key validity** [OWNER 2026-10-14, r2-F10]: every P-256 key (transported `gpg`, fallback `kms`, the
    repository key) must be a finite on-curve P-256 point passing FIPS 186-5 / SP 800-186 public-key validation for
    P-256, checked by the verifier, not by library default; otherwise `INVALID / KEY_FORMAT`. A configuration key
    that fails is a startup refusal (`TRUST_CONFIG_UNAUTHENTICATED`).
  - **Possession code mapping** [OWNER 2026-10-14, r2-F11]: a possession signature's codec failures take ENC's
    exact codes (`SIG_EMPTY`, `SIG_PACKET`, `TRUNCATED`, `TRAILING`, `LENGTH_CAP`, `SIG_FORMAT`, in ENC order) with
    the slot as diagnostic, then `SIG_POLICY`, then `POSSESSION_INVALID`. Receipt signature codec failures are
    reported only at `a_sig` decoding (section 15.7 row 3).
  - *Dated correction 2026-10-14:* the resolutions draft's "no subpacket in either area has the critical bit set" is
    withdrawn. RFC 9580 rejects only unknown critical subpackets and recommends a critical creation time; the blanket
    ban rejected conforming signatures.
- **Subpacket lengths.** RFC 9580 §5.2.3.7: first octet < 192, one octet; 192–254, two octets
  `((o1−192)<<8)+o2+192` (192–16319); 255 followed by a four-octet big-endian value (five octets total). The length
  counts the type octet and is ≥ 1. V1 accepts the shortest form only (a V1 rule, not an RFC ban); a longer form is
  `SIG_FORMAT`. [OWNER 2026-10-14, G28; r2-F14] *(Dated correction 2026-10-14: "255, four octets" misdescribed the
  five-octet form.)*
- Revocation is not evaluated. Loss or theft handling is operations. [A9:248-252; RB §1]

## 9. Dependency manifest

The dependency manifest is a bundle member (section 2.1, member 12). A9 names eight entries. [A9:153-154]

| # | Entry named in A9 | Where V1 uses it |
|---|---|---|
| 1 | RFC 8785 | canonical payload [ENC §1.3:160-170] |
| 2 | OpenPGP | signature rule O, key fingerprint [ENC §5.2:444-478; ENC §3.3:290] |
| 3 | The signature algorithms in use | ECDSA P-256 (fallback); plus ML-DSA-65 under the hybrid [A9:298-319] |
| 4 | SHA-256 | frames, anchors, fingerprints [ENC §3.3:289-290] |
| 5 | SHA-1, for git object linkage | commit id and commit-tree-blob links [ENC §7.2:712-718] |
| 6 | The DNSSEC algorithms in the chain | snapshot validation |
| 7 | OpenTimestamps | receipt, snapshot and commit proofs |
| 8 | Bitcoin headers | temporal check [A9:150] |

DD:63 lists the same eight (with ECDSA P-256 in place of "the algorithms in use"). [DD:63]

- Each entry records: exact edition, normative sections used, errata disposition, stable digest where canonical bytes
  exist, retrieval identifier, redistribution status, failure consequence. That is seven fields. [SPEC
  R-3.51:743-748] **Adopted** as a profile requirement, plus `id` and `title`; the file format is section 15.6.
  [OWNER 2026-10-14, G15] *(Was: "`OPEN (other):` … whether V1 adopts them as a profile requirement is not
  decided", 2026-10-13.)*
- **Extra standards: added.** Beyond A9's eight, the manifest names: Unicode 16.0.0 UCD (with file digests) and UAX
  #15 (NFC); RFC 8259; RFC 3339; RFC 9580; ECMA-262 Number::toString (pinned edition); FIPS 180-4; FIPS 186-5;
  RFC 4648; RFC 1035, 1982, 2181, 3110, 4034, 4035, 4509, 5011, 5702, 6605, 9718, and RFC 9102 (informative); RFC
  5652 (CMS, for `.p7s` source authentication); the OTS DetachedTimestampFile format (section 15.2); Bitcoin header,
  double SHA-256, merkle and non-witness transaction formats; gitformat-signature(5), the git object format and
  SHA-1DC; under the hybrid, FIPS 204 and the supplement's SPKI encoding. [OWNER 2026-10-14, G15] *(Was: "`OPEN
  (other):` ENC depends on more standards than A9's eight entries name … Decide whether to add these", 2026-10-13.)*
- The manifest's hash is fixed in the catalog: a mismatch gives `INVALID / BUNDLE_OBJECT_HASH`, an absent manifest
  `UNVERIFIABLE / MEMBER_MISSING`. The verifier does not interpret its contents. [OWNER 2026-10-14, G15] The catalog comparison is performable only when the spec lookup succeeds; under `SPEC_UNKNOWN` it is
  unperformable (section 1). [OWNER 2026-10-14, r2-F12]
- **Not yet the object** [OWNER 2026-10-14, r2-F14]. The list above and section 15.6 are a schema for a future
  object, not the object: pinned editions, errata and digests for ECMA-262, UAX #15 / Unicode 16.0.0, git and
  SHA-1DC, the Bitcoin formats and the release verifier are not yet supplied, and the listed names alone do not let
  an implementer build NFC tables or RSA/DNSSEC/CMS. Constructing and archiving the actual manifest and its
  referenced bytes is section 14.2 item 15.
- **Reference OTS reader divergence.** python-opentimestamps 0.4.5, section 15.2's reference reader, rejects a
  timestamp at depth 256 (its limit is 255), while this profile allows depth ≤ 256 with the root at depth 0
  (section 15.2); a depth-256 proof that is otherwise valid is `VALID_STRICT`. It also accepts redundant LEB128
  groups and SHA-1/RIPEMD-160 ops, which V1 rejects (`OTS_FORMAT`). A verifier must not rely on that library
  unmodified for the V1 OTS grammar. [OWNER 2026-10-14, codified from diff-1, EA-26]
- Long-horizon validity depends on this manifest and on the holder keeping the exact bytes. V1 offers no renewal. [Clarified, OWNER 2026-10-14, after mutation testing]: "the exact bytes" means the claim-bearing bytes (A_sig, the
  manifest, the keys, and the evidence each check consumes). A receipt's identity is SHA256(A_sig), not the hash
  of the bundle: an otherwise identical bundle can differ in unsigned diagnostics (`issuer_record`), possession-signature
  malleation (unhashed area, s versus n−s), non-qualifying OTS branches and unused pinned headers, and still return
  the same six fields (`prototype/mutation/REPORT.md`, classes A1–A4). Deduplicate and refer to receipts by
  SHA256(A_sig).
  [A9:290-292]

## 10. Number rule

Accept a number exactly when RFC 8785's canonical serialization preserves its value. Reject otherwise. The three
conditions (not negative zero, finite after round-half-even, exact decimal value of `ES(d)` equals the literal) and
the accepted and rejected examples are in ENC §1.2. [A9:438-443; ENC §1.2:118-148; ENC D-1:752-755] Proof:
`formal/p8/PROOF.md` Lemma 3. Vectors: `formal/p8/vectors/`.

This replaces the literal "exactly representable as an IEEE 754 double" rule for this profile only. [A9:405-406;
A9:440-443] The stale "needs an author sentence" remarks in ENC (ENC:147-148, D-1) and PROOF §6 are superseded by
A9.8. [OWNER 2026-10-14, G38; the ENC and PROOF wording edits are pending]

**`ES` recipe.** `ES(d)` is ECMA-262 Number::toString of a pinned edition (edition, section and digest in the
dependency manifest). If d is +0 or −0: `"0"`. If d < 0: `"-"` ‖ ES(−d). Otherwise let n, k, s be integers with
k ≥ 1, 10^(k−1) ≤ s < 10^k, s × 10^(n−k) = d as a double, and k as small as possible; if several s qualify, choose
the one for which s × 10^(n−k) is closest in value to d, and if two are equally close, the even one. Then: if
k ≤ n ≤ 21, the k digits followed by n−k zeros; if 0 < n ≤ 21, the first n digits, `.`, the remaining k−n digits;
if −6 < n ≤ 0, `0.`, −n zeros, the digits; otherwise the first digit, then `.` and the remaining digits if k > 1,
then `e`, `+` or `-`, and abs(n−1) in decimal. Any formatter must reproduce N-01…N-22 and C-N01…C-N22; Python's
`repr` is not ES. Unicode tables must be 16.0.0, identified by the UCD file digests in the dependency manifest; a
runtime may use bundled pinned tables, and one whose tables do not match refuses to run (no verdict).
[OWNER 2026-10-14, G29]

**Field grammars.** `utc` years run 0001–9999 (proleptic Gregorian, seconds 00–59). LDH labels match
`[a-z0-9-]{1,63}` with no leading or trailing hyphen; all-numeric labels, the top label included, are allowed; at
least two labels; at most 241 bytes. This is what both P8 codecs already do. [OWNER 2026-10-14, G18; the ENC §3.2
wording edit is pending]

## 11. The A9.1 scenario mapping

Registered before any V1 run. Every row: profile `tessera-v1-strict`, strict request, `revocation: NOT_EVALUATED`,
`historical_security: NOT_EVALUATED`, standing `ABSENT/NOT_ISSUED_IN_PROFILE`. [A9:165-167] Eleven rows cover
thirteen cases (a, g, b, c, d1, d2, d3, e, e′, f, h, i, i′). [A9:169-181; DD:195-207 has the same first ten rows]

| Case | Fixture | Expected verdict | Safe decision |
|---|---|---|---|
| a, g | Honest receipt as shipped (a's TLR removed) | `VALID_STRICT` | Accept as: these bytes were presented to Tessera by T |
| b | Reattribution under attacker keys | `INVALID` | Reject |
| c | Two-layer transplant | `UNVERIFIABLE / OUT_OF_PROFILE` | Reject |
| d1 | a's bundle; degraded request, then strict | Waiver refused; strict `VALID_STRICT` | Accept under strict only |
| d2 | a with repo evidence removed | `UNVERIFIABLE` | Reject: registered false reject |
| d3 | Clone, TLR removed (one key, one channel) | `INVALID` (A4.2 precedence) | Reject |
| e, e′ | a's bytes; slot-B key revoked inside (declared, anchor], or (e′) before declared | `VALID_STRICT` | Non-revocation not established; a transaction needing it must not rely on this receipt alone |
| f | Impostor's content through the honest service | `VALID_STRICT` | The receipt attests no submitter |
| h | Honest renewal wrapper | `UNVERIFIABLE / OUT_OF_PROFILE` | Reject: registered false reject |
| i | `content` = a contract plus two valid party signatures, issued honestly | `VALID_STRICT` | Accept as: this signed contract existed by T. The parties' signatures and keys are the relying party's to check |
| i′ | As i, one party signature does not verify | `VALID_STRICT` (Tessera does not read `content`) | Reject the contract: the receipt is valid, a party signature fails the relying party's own check |

**Fixtures for b and d3** [OWNER 2026-10-14, codified from diff-1, EA-27]. A9.1 names the outcome, not the fixture;
the conformance fixtures are:
- **b:** the attacker re-signs the content under its own two keys and manifest (consistent, with valid possession and
  signatures) and presents the honest DNS and git evidence: `INVALID / DNS_KEY_MISMATCH` (row 15.1, kms slot).
  Presenting the attacker's own DNS chain instead would give `UNVERIFIABLE / NO_TRUSTED_KSK_USABLE`, which
  contradicts A9's `INVALID` and is not the case-b fixture.
- **d3 ("one key, one channel"):** one attacker key in both slots, honest DNS evidence, `git` absent: `INVALID /
  DNS_KEY_MISMATCH` (row 15.1), dominating `UNVERIFIABLE / MEMBER_MISSING:git` (section 3.3).

The success bar: zero unsafe accepts; false rejects only on d2 and h. [A9:112-116] Registered prediction: a
headline-only reader fails e and f, and i′ is the same hazard. [A9:183-186] The A9.4 missing-capture negative control
is C7 evidence, not a mapping row. [A9:140; A9:267-268]

Note on case d1's expected verdict and dispatch: the "degraded request" half needs the request type to be visible at
dispatch. It is a verifier input, refused at D4 (section 3.1). [OWNER 2026-10-14, G17]

## 12. Gate items this profile feeds (for tracking only)

- Exit statements M2 and M5, the E6a dispatch and precedence cases, and the E12 page are 30 Oct items. [A9:199-204]
- After exit: vectors run against AWS, the missing-capture control, and the dead-service test. [A9:208-210]
- Cut order if 30 Oct slips: the PQ hybrid first, nothing else. `A_sig`, the root-KSK rule and the git stamp target
  are required. [A9:205-207]

## 13. Reconciliation notes

Counts checked against the source files when this draft was written:

| List | Count here | Source count |
|---|---|---|
| Bundle members (section 2.1) | 12 | A9:152-154 names spec, vectors, preamble, dependency manifest (4); the other eight come from ENC and SPEC as cited per row |
| Trust configuration items (section 5) | 4 (+1 moved) | A9:148-151 names 4 (two KSKs, repository key, pin set); item 3 is the 2026-10-13 pair, now with A9.5 intervals; item 5 (SPEC R-5.8 parameters) moved to the spec catalog 2026-10-14 (G12) |
| Stable output fields | 6 | A9:156 |
| Dependency manifest entries | 8 named by A9 (+ the 2026-10-14 additions, section 9) | A9:153-154; DD:63 |
| Per-entry fields | 7 | SPEC R-3.51:743-748 |
| Issue-order steps | 8 | ENC §5.4:517-524; A9:278-281 |
| Scenario rows / cases | 11 / 13 | A9:169-181 |
| DNS rejection steps | 15 | ENC §7:595-612 |
| Parameters | 5 | A9:217 |

Disagreements between sources, found while drafting:

1. **Required set.** SPEC R-3.37 (635-638) and V21 (1300) say the envelope carries the required set. A9:137 and
   DD:93 say the verifier fixes it. DD:93 already notes "the spec drifted". This profile follows A9.
2. **Stale derivation wording.** DD:52 and DD:56 describe the anchor as covering the frames only. A9:134, 138 and ENC
   §5 cover frames and exact signatures. DD:61 is already correct. DD:64 (P-256 signers only) and DD:218 (parameters
   ratified) are superseded by A9:298-326 and A9:217-219.
3. **KSK periods.** DD:66 gives each KSK "its IANA validity period". A9:302-303 requires signing and reliance
   periods kept apart from publication and revocation. SR:76-78 is the evidence for the split; the reliance values
   are in section 5.
4. **Extraction of D.** DD:94 says "exact extraction of D". Superseded by the 2026-10-13 decision (section 6.3).
5. **Number rule restated in the spec.** SPEC V6 (1261) still reads "numbers not exactly IEEE 754 doubles". A9.7 rows
   22 and 23 (A9:405-406) do not list SPEC:1261, though row 15 lists spec restatements. A9.8 governs.
6. **ENC note on the derivation.** ENC:147-148 and ENC D-1 (752-755) say the derivation's profile line keeps the old
   number rule. DD:62 now states the value-preserving rule. The ENC remark is stale.
7. **Spec revocation text.** SPEC R-5.21 (1358) requires the revocation conjunct for `VALID_STRICT`. A9.4 and A9.7 rows
   7 to 9 replace it for V1. Not a defect; listed so an implementer does not read the spec alone.


## 14. OPEN items

### 14.1 Closed on 2026-10-14

Every `OPEN (step 8)` group and seven of the eight `OPEN (other)` items of the 2026-10-13 list are closed by the
owner-disposed spec-sufficiency resolutions (RES). Each closing rule carries its tag where it now stands. The
eighth, the signer branch, is still open (14.2 item 4).

| 2026-10-13 OPEN item | Closed by | Where |
|---|---|---|
| 1. Dispatch inputs | G17 | section 3.1 |
| 2. Cross-stage reason precedence | G31, G26 | sections 3.2, 3.3, 15.7 |
| 3. Verdict class of `DNS_*` rejections | G24 | section 3.2 |
| 4. Pinned-D gate on DNS | G34 | section 6.3 |
| 5. Git assertion time relation | G02 (with A9 C4 chain order) | section 6.3 |
| 6. M2 text | G34 | section 6.4 |
| 7. G-17 required set, `binding_forms` check, channel mapping | G01 | section 6.4 |
| 8. M5 condition | G10 | section 6.4 |
| 9. T versus `anchor_time`; meaning of "verified" | G03, G04, G05 | section 7.1 |
| 10. Pin conflict and coverage; snapshot body and time | G23, G07, G19, G06 | sections 7.2, 7.3 |
| Container and transport encoding | G14, G17 | sections 2.1, 15.1 |
| Observed delay and policy version | G33 | section 2.1 |
| Key, format and versioning of the pin set | G08 (A9.5 release allowlisting), G09 | section 5 |
| Extra standards in the dependency manifest | G15 | section 9 |
| SPEC's seven per-entry fields | G15 | sections 9, 15.6 |
| Repository key as offline root | G36 (operating fact) | section 5 |
| Inventory and stage table as extraction | G14, G17, G31 | sections 2.1, 15.7 |

### 14.2 Still open before 30 Oct

Each is a decision or owner act the freeze needs. None is settled by this document. Items 1–10 are the 2026-10-14
list, amended where marked; items 11–16 are added by the second review. [OWNER 2026-10-14, r2-14.2] They are bounded
to verifier sufficiency and already-stated release/freeze work; they add no V2 capability and do not move the V1
finish line.

1. **Release-key custody** (G08, A9.5). Which key signs verifier releases, who holds it, and its access boundary,
   shown to be unusable by the DNS credential, the repository key and the issuing AWS account. YubiKey 2 is not in
   hand. If independence cannot be supplied, a NARROW-MODEL excluding the channel-capture path goes to the author.
   **Expanded (r2-F17):** the custody record also covers the release key's authenticated bootstrap, rotation and
   bounded loss/compromise recovery (RB §6, all OPEN there). Release independence is load-bearing under the
   channel-capture adversary; the author must be told if it cannot be supplied.
2. **Release artefact and release-signature format** (G08). What exactly a release is (binary, source archive or
   both), the signature format over it, and the bootstrap publication of the release public key. The **trust
   configuration's byte format is specified** (section 15.5); its actual values are item 3. **Expanded (r2-14.2,
   r2-F17):** authenticated bootstrap, release-key rotation and bounded loss/compromise recovery; the exact signed
   release preimage and verification format, with dependency pinning. None of these becomes a bundle-verifier rule.
3. **The pre-freeze trust configuration's values** (G22, G09). Sourced KSK RDATA, confirmed signing starts
   (~~KSK-2017 2018-10-11~~ KSK-2017 2018-10-11T16:00:00Z policy start, r2-F15, and KSK-2024 2026-10-11 are
   proposed), ends, L, the repository entry, the pins and their source digests. **Expanded (r2-14.2):** the complete
   machine-checkable trust schema (section 15.5 as amended) and the horizon/candidate aggregation (r2-F04), plus
   sourced precise endpoints with switch time, RRSIG inception and policy value recorded separately (r2-F14,
   r2-F15).
4. **The hybrid branch** (A9.6; section 1). Signer branch taken, due 21 Oct; under the hybrid, the
   branch-registration supplement, the pair algorithm id and the exact ML-DSA-65 SPKI encoding (G21, G12).
5. **Slot-2 custody choice** (A9.6; section 8): token or non-AWS HSM, recorded dated in this profile, with the
   throughput measurement and the HSM monoculture check (RB §1). **Expanded (r2-F17):** for the hybrid, the final
   custody implementation must have completed the deployed-slot pass-condition evidence by **21 Oct**; a choice
   deferred to before 30 Oct is allowed only among implementations that already met that deadline, otherwise the
   registered fallback is taken (A9.6 "Deadline").
6. **Repository-root algorithm** (G25). Confirm that the deployed repository root (YubiKey 2) is P-256; otherwise
   list its algorithm and add it to the dependency manifest.
7. **Freeze assembly** (G13). Build the spec object, the vectors object and the catalog; record their hashes.
   **Expanded (r2-F13, r2-F14, r2-F17):** the exact tracked part inventory from a named freeze commit (section
   15.8), an assembler plus an independent byte-agreement check, the external catalog, the authored bytes and
   hashes of the purpose preamble and of the dependency manifest, and A9's archival distribution (as a spec part,
   section 15.8). Actual spec/vector/catalog hashes go in a separate release/freeze record **outside** the frozen
   spec parts. The freeze record also names the A9 signing commit and the freeze commit of every source, and
   refreshes every `A9:nnn` locator against them (section 0).
8. **Conformance vectors** (RES §L, cases L-01 to L-111), including A9.5's git cases, before the freeze.
   **Amended (r2-F16):** L-27 and L-28 are withdrawn and replaced by RES's amended positive controls (T_git >
   declared and T_git > receipt T with `h_git + 5 < h_receipt` → pass); the obsolete `GIT_ASSERTION_AFTER_ISSUE`
   code is not a V1 reason. Referencing the old L list as a whole is insufficient. **Added:** the distinguishing
   cases named in r2-F01 to r2-F14: unknown-id and branch-not-taken `alg` with codec-valid and codec-invalid
   signatures, matching and mismatching manifest `alg` (F01); frames disagreeing on content plus manifest issuer
   mismatch, bad `manifest_sha256` (F02); `git` present without `object_format`, `issuer_record: {}`, `keys: null`,
   one absent plus one malformed member, `object_format: null` (F03); open-horizon versus finalized out-of-period
   candidates, mixed (F04); mixed unsupported/selector-mismatch, no matching key, bad flags/protocol, wrong Labels,
   malformed supported RDATA, parent-blocked child (F05); root-only → TXT, missing last DNSKEY, missing DS, missing
   root, wrong-owner TXT, malformed character-string (F06); valid explicit witness plus a wildcard RRSIG (→
   `DNS_WILDCARD`), both serialization orders of a primary-key tie, duplicate RRSIG (F07); three different anchor
   transactions, two paths at the same selected height one satisfying and one failing the txid subset, a snapshot
   or git path failing `OTS_TX_SHAPE` (F08); non-32-byte Bitcoin message, non-shortest CompactSize, pending payload
   not consumed, depth/ops bound edges, non-conventional merkle suffix, non-125-byte, multi-input/output and
   witness-stripped transaction controls (F09, and the G20 assessment); metadata shape (zero-data critical type 33,
   two type 33, inconsistent 16/33), wrong hash prefix, invalid public point, nonzero-pad-bit armor (F10);
   multiple-failure stable-six-field cases across and within stages, including possession, DNS and git (F11);
   unknown spec plus independently bad signed-object bytes, unknown spec plus unmatched dependency bytes (F12);
   KSK-2017 policy-start boundary (F15).
9. **ENCODING-V1 and PROOF wording edits** named in G01 (E§8 "codec-level"), G02 (E§7.1 CORRECT), G18 (E§3.2),
   G28 (E§5.2) and G38 (E:147-148, D-1, PROOF §6), with the change accounting G37 requires. **Expanded (r2-14.2,
   r2-contra):** E §7.1's exact selection sentence ("earliest") changed to A9 C5's lowest block height, not only its
   publication/pre-commitment explanation; E §7.2's "commit adds blob" replaced by "whose tree contains the
   assertion blob at the profile path"; this profile's own codec-level qualification (section 3.1, done); and
   accounting for any codec/policy change chosen under r2-F01 (none chosen: the codec baseline is unchanged).
10. **Snapshot re-capture** in the section 15.3 body form, freshly stamped (G19).
11. **Decision-function completion** (r2-F01–F03, F12): codec-known versus supported algorithm routing; explicit
    receipt/manifest equalities and codes; absent/present/diagnostics/descriptor exceptions; unknown-spec
    object-check dependencies. Text now in sections 1, 2.1, 6.4 and 15.7; vectors in item 8.
12. **DNSSEC/body completion** (r2-F04–F07): exhaustive candidate/metadata failures, horizon and edge precedence,
    missing-zone skeleton, root signing, malformed TXT boundary, wildcard/global-candidate decision and body sort
    ties. Text now in sections 5, 6.1, 15.3; vectors in item 8.
13. **Proof completion** (r2-F08, F09): varbytes/CompactSize, message-size outcomes, resource-count conventions,
    txid scope and selected-height path aggregation. Text now in sections 7.1 and 15.2; vectors in item 8.
14. **Signature completion** (r2-F10, F11): complete advisory-subpacket policy, public-key validation, v4
    hash-prefix choice, git armor aliases and possession/git code mapping. Text now in sections 6.3, 8 and 15.4;
    vectors in item 8.
15. **Dependency closure** (r2-F14): construct and archive the actual dependency manifest plus the referenced
    normative bytes/tables or immutable retrievable source artifacts, with exact editions, sections, errata and
    digests (ECMA-262 edition, Unicode 16.0.0 UCD and UAX #15, git object format, SHA-1DC, Bitcoin formats, the
    release-signature dependency); identify which are distributed with the verifier and which are retrieved at
    build time. Pin the SHA-1DC detection implementation and version and its prescribed collision-return behaviour
    (section 15.4). Offline verification after installation is the claim; offline reconstruction from the three
    documents alone is not furnished until this item is done.
16. **A genuinely total report-check table** (r2-F11): section 15.7 now gives check ids, inputs, availability,
    failure/unperformable codes and tie keys; it must be followed by multi-failure stable-six-field agreement cases
    (item 8) run by the differential verifier (`docs/reviews/v1-profile-r2/DISPOSITION.md`, owner process decision).

## 15. Evidence formats and check order [OWNER 2026-10-14]

### 15.1 Container [OWNER 2026-10-14, G14, G17, G33]

A bundle is one UTF-8 JSON text that passes ENC §1.4 checks 1–5 and 7 and is canonical JCS. It contains no JSON
numbers. Heights and durations are decimal strings matching `0|[1-9][0-9]*` with value at most 4294967295. Binary
values are RFC 4648 §4 base64 with padding that round-trips (no non-zero pad bits, no line breaks). Size cap 2^27
bytes. Top level: exactly `{"layers":[L],"profile":"tessera-v1-strict"}`. After dispatch (section 3.1): a
non-canonical container is `INVALID / JSON_NONCANONICAL`; then the absence rule (section 2.1) and A9.5's
`git.object_format` outcomes; then any other schema failure is `INVALID / CONTAINER_SCHEMA`. Absence is inspected
only beneath correctly typed parents, a present non-string `object_format` is `CONTAINER_SCHEMA`, and a present
`issuer_record` with an absent internal field is `CONTAINER_SCHEMA` (section 2.1). [OWNER 2026-10-14, r2-F03]

**Numbers.** JSON numbers are admitted syntactically at dispatch (D1's strict-JSON checks do not exclude them, and
D2/D3 read only `profile` and the length of `layers`) and rejected after dispatch by the container schema: a JSON
number anywhere in the layer is `INVALID / CONTAINER_SCHEMA` (row 2.4, after row 2.1), never `OUT_OF_PROFILE`.
[OWNER 2026-10-14, codified from diff-1, A10]

Layer `L` (closed; each member exactly once; all values base64 unless marked):

| Member | JSON type and content | Invariants |
|---|---|---|
| `a_sig` | string: `A_sig` bytes | decoded by ENC §5 |
| `manifest` | string: `F_manifest` | decoded by ENC §4 |
| `possession` | object `{"gpg","kms"}`: detached signature over `F_manifest` per slot rule | both present |
| `keys` | object `{"gpg","kms"}` (section 8) | both present |
| `receipt_anchor` | object `{"ots","txid"}`; `txid` 64 lowercase hex, display order | |
| `headers` | object `{"<height>":"<160 lowercase hex>"}` (80-byte raw header) | height grammar; nonempty; shared pool |
| `dns` | object `{"ots","snapshot_body"}` | body per 15.3 |
| `git` | object `{"blob","commit","object_format","ots","trees"}`; `trees` array of exactly 2 strings [root, sub]; `object_format` string | A9.5 |
| `spec`, `vectors`, `preamble`, `dependency_manifest` | string: raw bytes | hashed only |
| `issuer_record` | optional object `{"observed_anchor_delay_s","policy_version"}`; delay in the decimal grammar (seconds); `policy_version` matches `tessera-v1-issue-policy/(0|[1-9][0-9]*)` | diagnostics only |

### 15.2 OTS proofs and the txid [OWNER 2026-10-14, G20]

OWNER CHOICE (supported-path limit). python-opentimestamps 0.4.5 is the reference reader, not normative.
- **Header.** Magic `00 4f70656e54696d657374616d7073 0000 50726f6f66 00 bf89e2e884e89294`, varuint major version 1,
  file-hash op `08` (SHA-256 only), the 32-byte digest, one Timestamp, end of input.
- **Timestamp.** `Timestamp := (ff Item)* Item`; `Item := 00 Attestation | Op Timestamp`.
- **Ops.** `08` (sha256), `f0 varbytes` (append), `f1 varbytes` (prepend). Arguments 1–4096 bytes; every message and
  result at most 4096 bytes.
- **Attestations.** `tag(8) varbytes(payload)`, payload at most 8192 bytes. Bitcoin `0588960d73d71901`: payload is
  exactly one varuint height. Pending `83dfe30d2ef90c8e`: payload varbytes(URI ≤ 1000), URI ignored.
- **Wire completion** [OWNER 2026-10-14, r2-F09]. `varbytes := varuint byte_count || exactly byte_count octets`.
  Both the pending and the Bitcoin payloads must be consumed exactly (the pending payload's inner URI framing
  included); otherwise `OTS_FORMAT`. A Bitcoin attestation whose message is not exactly 32 bytes is `INVALID /
  OTS_FORMAT`, independently of header availability. Timestamp depth: the root Timestamp has depth 0, each Op →
  Timestamp step adds 1, `ff` siblings do not add. Op and attestation counts are of serialized items, duplicates
  included; duplicates are semantically inert only within those limits.
- **Varuint.** LEB128, shortest form only, value ≤ 2^32 − 1. (python-opentimestamps 0.4.5 accepts redundant groups;
  V1 does not.)
- **Bounds.** Depth ≤ 256; ≤ 65536 ops and ≤ 4096 attestations per proof; proof ≤ 2^20 bytes. Duplicate identical
  branches are permitted and have no effect.
- **Rejections.** Any other op or tag, or any grammar or bound violation: `INVALID / OTS_FORMAT`. File digest must be
  SHA256(`A_sig`) for the receipt (`RECEIPT_ANCHOR_MISMATCH`), SHA256 of the ENC §6 envelope for the snapshot
  (`SNAPSHOT_STAMP_MISMATCH`), SHA256 of `<40-hex commit id>\n` for git (`GIT_STAMP_MISMATCH`).
- **Merkle link.** A Bitcoin attestation's message is 32 bytes and equals bytes 36–68 of the bundled header at that
  height.
- **Header fields** [OWNER 2026-10-14, r2-F09]. In a raw 80-byte header: prev = `header[4:36]`, merkle root =
  `header[36:68]`, nTime = `uint32le(header[68:72])`.
- **txid (supported-proof subset).** On the path to the **selected** attestation, let the first two consecutive
  sha256 ops have input P, and let m be the message immediately before the maximal run of append/prepend ops that
  precedes them. Required: (1) P parses exactly, consuming every byte, as a non-witness Bitcoin transaction —
  version (4), compact-size input count ≥ 1, inputs (32 + 4 + compact-size script length + script + 4), compact-size
  output count ≥ 1, outputs (8 + compact-size length + script), locktime (4); no SegWit marker; compact sizes
  shortest form; (2) m is 32 bytes and some output script is exactly `6a 20 ‖ m`; (3) `hex(reverse(SHA256d(P)))`
  equals `receipt_anchor.txid`. Otherwise `INVALID / ANCHOR_TXID_MISMATCH`. Any one path to the selected height may
  satisfy this. (All 344 Bitcoin paths in the repository's 127 proofs have this shape, RES G20.)
- **CompactSize and transaction fields** [OWNER 2026-10-14, r2-F09]. A first byte < 253 is the value; `fd` then u16le,
  `fe` then u32le, `ff` then u64le; shortest form only; a length or count exceeding the remaining bytes is rejected
  before allocation. Version, value and locktime are parsed as their fixed-width bytes (4, 8, 4) and not
  interpreted. Consensus validity and script execution are supplied by authentic pinned history, not revalidated
  here.
- **(4) Merkle suffix (owner choice, fail-closed)** [OWNER 2026-10-14, r2-F09]. After the two sha256 ops that
  produce the txid, the path to the selected attestation consists only of zero or more repetitions of (append or
  prepend of exactly 32 bytes, sha256, sha256); an empty suffix is a one-transaction block. Otherwise `INVALID /
  ANCHOR_TXID_MISMATCH` for the receipt. Without it, arbitrary allowed operations could follow the identified
  transaction. All 352 Bitcoin paths in the repository's 129 proofs have this suffix (owner check 2026-10-14;
  evidence, not a rule). This is a missing structural definition, not a demonstrated forged timestamp.
- **Scope** [OWNER 2026-10-14, r2-F08]. Parts (1), (2) and (4) apply at the selected height of the receipt, snapshot
  and git proofs; part (3), the txid equality, applies to `receipt_anchor` only. Snapshot or git failure of (1), (2)
  or (4) at every qualifying path at its h*: `INVALID / OTS_TX_SHAPE`. h* is selected first (section 7.1); a failing
  path never moves selection to a higher height.

### 15.3 DNSSEC snapshot body [OWNER 2026-10-14, G19, G24, G30]

A concatenation of RRs, each in RFC 1035 §3.2.1 wire format, uncompressed, in RFC 4034 §6.2 canonical form (owner
name and every domain-name field inside RDATA, including the RRSIG signer name, lowercase and uncompressed).
1. **Groups, in order:** the root DNSKEY group; then for each zone z below the root down to the TXT's signer zone, a
   DS group at z and a DNSKEY group at z; last the TXT group at `_tessera-v1.<D>`. A group is a maximal run of RRs
   with the same owner, CLASS IN, and TYPE t (the RRset) or TYPE RRSIG with Type Covered t (its witnesses). The RRset
   comes first, in RFC 4034 §6.3 canonical RDATA order without duplicates, then zero or more RRSIGs in (key tag,
   inception, expiration, signature bytes) order. Each z is a proper descendant of the previous zone. Signer names:
   the parent for DS, z for DNSKEY, the root for the root group, the last z for TXT.
   - **Serialization ties and duplicates** [OWNER 2026-10-14, r2-F07]. Canonical RRSIG RDATA is the final body
     serialization sort key: RRSIGs sort by (key tag, inception, expiration, signature bytes, canonical RRSIG
     RDATA). A duplicate is an RR identical in owner, class, type and RDATA (`SNAPSHOT_FORMAT`); TTL consistency
     within an RRset is checked separately (point 2).
   - **Raw time fields in sort keys.** Inception and expiration in these sort keys, and in the G35 candidate tuple
     (section 7.3), are the raw 32-bit unsigned RRSIG field values compared numerically (equivalently, as
     big-endian bytes), not the absolute times resolved by section 7.3's serial arithmetic; the two orders differ
     only across the 2^32 wrap. [OWNER 2026-10-14, codified from diff-1, EA-13]
   - **Too-short RRSIG.** An RRSIG whose RDATA (within a consistent RDLENGTH) is too short for RFC 4034 §3.1's
     fixed fields and signer name is attributed to the group of the immediately preceding RRs at the same owner,
     not treated as a framing failure, and is malformed supported RRSIG RDATA: `INVALID / DNSSEC_FORMAT`
     (section 6.1). [OWNER 2026-10-14, codified from diff-1, A06]
   - **Chain skeleton, recovery grammar** [OWNER 2026-10-14, r2-F06]. The root is the initial zone. The ordered zone
     skeleton is constructed from the supplied DS and DNSKEY owners and the RRSIG signer names: each names a zone,
     and the zones, ordered by descent, must form one chain from the root. Omitted DS, DNSKEY, root DNSKEY or TXT
     groups are admitted as missing evidence (`UNVERIFIABLE / DNS_EVIDENCE_MISSING`; root:
     `NO_TRUSTED_KSK_USABLE`); omission alone is never a format failure. Direct signing of the TXT by the root, or
     by any ancestor zone in the skeleton, is permitted (section 6.1 retains ancestor signing authority); "the last
     z" is the TXT RRSIG's signer zone, which is the root when no below-root zone is supplied. Conflicting supplied
     transitions or signer names (names not forming one descent chain, a DS group not signed by its parent zone in
     the skeleton, a DNSKEY group not signed by its own zone, a group after the TXT group) are `INVALID /
     SNAPSHOT_FORMAT`. A supplied final TXT owner is checked by ENC §7's `DNS_OWNER`, even when wrong; its existence
     does not itself constitute an "outside-chain" framing failure. *(Dated correction 2026-10-14: the grammar did
     not say whether a skipped zone was omission or inconsistency, and "the last z" was undefined for a TXT signed
     by the root.)*
2. **Fields.** CLASS IN. TTL equal within an RRset and otherwise uninterpreted; validation uses the RRSIG's Original
   TTL.
3. **Framing versus completeness.** A truncated RR encoding, forbidden RR type, duplicate RR, inconsistent
   owner/type within a group, or misordered supplied group is `INVALID / SNAPSHOT_FORMAT`. Among RDATA defects,
   RR boundary/RDLENGTH truncation and any domain-name field inside RDATA that is not in the canonical form above (an
   uppercase ASCII letter or a compression pointer, including in the RRSIG signer name) are `INVALID /
   SNAPSHOT_FORMAT`, whatever other witnesses the body carries; TXT's internal character-string parsing uses ENC's
   `DNS_RDATA` / `DNS_STRINGS`, and other malformed supported DNSKEY/RRSIG RDATA is `DNSSEC_FORMAT` (section 6.1).
   [OWNER 2026-10-14, diff-1 F-1: the earlier wording let a non-canonical RRSIG beside a valid witness reach
   `VALID_STRICT` in one implementation and `INVALID` in another; fail-closed chosen.]
   A defect in an RR's owner-name wire encoding is `SNAPSHOT_FORMAT`; a defect of the RRSIG signer-name field
   other than the non-canonical forms just named (which are `SNAPSHOT_FORMAT` under diff-1 F-1) and other than a
   recovery-grammar conflict is malformed supported RRSIG RDATA, `DNSSEC_FORMAT`. [OWNER 2026-10-14, codified from
   diff-1, A12]
   [OWNER 2026-10-14, r2-F06, r2-F05] A syntactically complete
   sequence lacking a required RRset or its witness RRSIG is `UNVERIFIABLE / DNS_EVIDENCE_MISSING` (root:
   `NO_TRUSTED_KSK_USABLE`). Missing groups alone are not order violations. Forbidden: any type other than DNSKEY, DS,
   TXT and RRSIG, and any RR at a name outside the chain (the final TXT group excepted, see the recovery grammar);
   CNAME and DNAME are not followed. An empty body is `LENGTH_CAP`.
4. **Wildcards:** `INVALID / DNS_WILDCARD` (section 6.1). This is the global no-wildcard body restriction: any
   RRSIG in the body with Labels less than its owner's label count, whatever other witnesses the body carries.
   [OWNER 2026-10-14, r2-F07] The Labels octet is read, and this restriction applied, whenever an RRSIG's RDATA
   has at least 4 bytes (Type Covered, Algorithm, Labels), however malformed the rest of that RDATA is.
   [OWNER 2026-10-14, codified from diff-1, A07]
5. **Envelope:** ENC §6, `header ‖ u32 len ‖ body`, 1 ≤ len ≤ 2^24.

### 15.4 Git evidence [OWNER 2026-10-14, G25]

OWNER CHOICE (supported-path limit) plus SHA-1DC (BROADEN).
- **Commit body** (without `commit <len>\0`): `tree <40 lhex>LF`, `(parent <40 lhex>LF)*`, `author <bytes>LF`,
  `committer <bytes>LF`, exactly one `gpgsig <line>LF` with `( <line>LF)*` continuations, `LF`, message. Repeated
  `parent` headers with distinct ids are allowed (merges); a repeated identical id, any other header (`encoding`,
  `mergetag`, `gpgsig-sha256`, unknown), or a second `tree`, `author`, `committer` or `gpgsig` gives
  `INVALID / GIT_COMMIT_FORMAT`. Author and committer are not interpreted. The signed payload is the commit without
  the `gpgsig` line and its continuations (gitformat-signature(5)).
  - **Empty identity values.** The `<bytes>` of `author` and of `committer` are nonempty: `author` or `committer`
    followed by an empty value is `INVALID / GIT_COMMIT_FORMAT`. [OWNER 2026-10-14, codified from diff-1, A09]
- **Signature value** (continuations joined by LF, one leading space stripped from each): `-----BEGIN PGP
  SIGNATURE-----` LF, one empty line, one or more base64 lines of 1–76 RFC 4648 characters (`=` padding only at the
  end of the last), an optional CRC line `=` plus 4 base64 characters, `-----END PGP SIGNATURE-----`, no trailing LF.
  No armor headers, no other blank lines, no whitespace inside lines. A present CRC-24 must match. Dearmored bytes
  satisfy rule O's grammar and policy (section 8) with type 0x00. Otherwise `INVALID / GIT_SIG_FORMAT`.
  The concatenated base64 lines obey strict RFC 4648 round-trip and padding (no nonzero pad bits), as in section
  15.1; CRC presence and validity remain as above. Every armor, codec and policy violation is `GIT_SIG_FORMAT`, the
  stated exception to section 8's `SIG_POLICY`; failed mathematics is `GIT_SIGNER_NOT_CONFIGURED` (section 6.3).
  [OWNER 2026-10-14, r2-F10, r2-F11]
- **Trees.** Entries `mode SP name NUL id20`; modes {40000, 100644, 100755, 120000, 160000} without leading zero;
  names nonempty, no `/` or NUL, not `.` or `..`; strictly sorted in git order (trees compare as `name/`), no
  duplicates, body consumed exactly. Otherwise `INVALID / GIT_TREE_FORMAT`.
- **Path.** Root entry `tessera-v1` (40000), then `key-assertion` (100644), the blob; `git.trees` is exactly
  [root, sub]. Otherwise `INVALID / GIT_PATH`.
  - A commit whose `tree` header names an id other than the SHA-1 id of `git.trees[0]` is `INVALID / GIT_PATH`
    (row 14.5); there is no dedicated code. [OWNER 2026-10-14, codified from diff-1, EA-22]
- **Ids.** SHA-1 of `"<type> <len>\0" ‖ body` with collision detection (SHA-1DC); a detection is
  `INVALID / GIT_SHA1_COLLISION`. SHA-1DC is a pinned detection implementation and version named in the dependency
  manifest, with its prescribed collision-return behaviour, not whatever a library calls SHA-1 (section 14.2 item
  15). [OWNER 2026-10-14, r2-F14]
- **Repository key.** v4 ECDSA P-256 public-key body, rule O (signer outcomes in section 6.3).
- **Not checked:** that the commit introduced the blob.

### 15.5 Trust configuration [OWNER 2026-10-14, G08, G09, G22]

One RFC 8785 JSON object, no numbers, every key required; authenticated only by the release allowlist (section 5).

**Closure and grammar** [OWNER 2026-10-14, r2-F14]. The schema is closed recursively: every object at every level
(top level, KSK entries, repository entries, `sources` items) has exactly the listed keys. Parsing is strict UTF-8
and JCS with no JSON numbers; binary values are canonical base64 (section 15.1); times use the `utc` grammar of
section 10; decimal strings are canonical unsigned decimals (`0|[1-9][0-9]*`) with per-field ranges: `version` 1 to
4294967295; `key_tag` 0 to 65535; `algorithm` 0 to 255; `reliance_lifetime_s` 1 to 2592000 (**owner choice**,
fail-closed: at most 30 days; the observed value is 1814400); heights as in section 15.1. `root_ksks` is sorted by
(`signing_start`, numeric `key_tag`, `dnskey_rdata` bytes); `repository_keys` by (`signing_start`, `key` bytes).
`root_ksks`, `repository_keys` and every `sources` array are nonempty, and every key in them valid (section 8). An
entry with `signing_end` null must have `signing_start` ≤ `as_of`. A schema failure is a startup refusal
(`TRUST_CONFIG_UNAUTHENTICATED`, no verdict), never a bundle `INVALID`. Cross-release invariants stay in the
release checker; the offline verifier never fetches a previous config. *(Dated correction 2026-10-14: "every key
required" did not say closed at every level, and the sort and decimal rules were less concrete than section 15.1.)*

| Key | Type and grammar | Invariants |
|---|---|---|
| `format` | `"tessera-v1-trust/1"` | |
| `profile` | `"tessera-v1-strict"` | |
| `version` | decimal string ≥ 1 | prior + 1 |
| `previous_sha256` | 64 lowercase hex | 64 zeros for version 1; else the prior config's hash |
| `as_of` | RFC 3339 `YYYY-MM-DDTHH:MM:SSZ` | nondecreasing |
| `issuer_domain` | `"wamason.com"` | equals D |
| `header_pins` | object height-string → 64 lowercase hex (display order) | nonempty; one per height; immutable |
| `root_ksks` | array of KSK entries, sorted by (`signing_start`, `key_tag`) | unique `dnskey_rdata` |
| `repository_keys` | array of `{"domain","key","signing_end","signing_start","sources"}` | `domain` = D; `key` base64 v4 P-256 body; `signing_end` nullable; start ≤ end; unique `key` |

KSK entry (strings unless marked):

| Field | Type | Invariant |
|---|---|---|
| `name` | e.g. `"KSK-2017"` | unique |
| `key_tag` | decimal string 0–65535 | equals RFC 4034 App. B tag of `dnskey_rdata` |
| `algorithm` | decimal string | equals the RDATA algorithm; in {8, 13} |
| `dnskey_rdata` | base64 of RFC 4034 §2.2 RDATA | flags 257, REVOKE clear, protocol 3 |
| `ds_sha256` | 64 lowercase hex | SHA-256 over root owner wire `00` ‖ RDATA |
| `signing_start`, `signing_end` | RFC 3339; `signing_end` nullable | start ≤ end |
| `reliance_lifetime_s` (L) | decimal string | immutable |
| `publication`, `revocation` | RFC 3339 or null | informational |
| `sources` | nonempty array of `{"description","sha256","uri"}` | `sha256` of the archived source |

### 15.6 Dependency manifest [OWNER 2026-10-14, G15]

A closed JCS object, exactly `{"entries":[…],"format":"tessera-v1-deps/1"}`; `entries` sorted by `id`, unique. Each
entry has all of: `id` (`[a-z0-9-]+`), `title`, `edition`, `sections` (nonempty array of strings), `errata`,
`digest_sha256` (64 lowercase hex, or null where no canonical bytes exist), `retrieval`, `redistribution`,
`failure_consequence`; strings unless marked. The entry list is section 9's.

### 15.7 Total check order for the reported reason [OWNER 2026-10-14, G31, G26; r2-F11]

**Numbered check table** [OWNER 2026-10-14, r2-F11; incorporates r2-F02–F10 and r2-F12]. The reported reason is
the first **failed** row in (row id, tie key) order; if no row failed, the first **unperformable** row. A row whose
necessary input cannot be obtained because of an earlier row's failure or unperformability is unperformable and
contributes no reason of its own; the table is ordered so that every such dependency points to an earlier row.
Rows 11.1–11.4 are evaluated whatever else fails, because they determine T (section 3.4). Slot order is kms, then
gpg. Candidates are ordered by the G35 tuple (section 7.3), never by their position in a transport array; members
and missing paths by JCS key order with numeric array indices; heights ascending. The verdict rule (section 3.3) is
unchanged: INVALID over UNVERIFIABLE, and no early exit before every earlier-priority row and every stable field,
including T, is settled.

| Row | Check | Inputs | Available when | Fails as (INVALID) | Unperformable as (UNVERIFIABLE) | Tie key |
|---|---|---|---|---|---|---|
| 1.1–1.4 | Dispatch D1–D4 (section 3.1) | bytes, request | always | — | `OUT_OF_PROFILE` (D4: detail `REQUEST_UNSUPPORTED`); terminal, nothing else evaluated | D1…D4 |
| 2.1 | Canonical JCS | bytes | dispatched | `JSON_NONCANONICAL` | — | — |
| 2.2 | Required member present | layer | parent present and correctly typed | — | `MEMBER_MISSING:<path>`; `git.object_format`: `GIT_OBJECT_FORMAT_MISSING` | path |
| 2.3 | `object_format` supported | `git.object_format` | present JSON string | — | `GIT_OBJECT_FORMAT` | — |
| 2.4 | Schema of present members (incl. non-string `object_format`, present `issuer_record`) | layer | member present | `CONTAINER_SCHEMA` | — | first offending path |
| 3.1 | `a_sig` codec, ENC §5 order, including the receipt signature codec (`SIG_EMPTY`, `SIG_PACKET`, `TRUNCATED`, `TRAILING`, `LENGTH_CAP`, `SIG_FORMAT`) | `a_sig` | 2.4 passes for `a_sig` | ENC's code | — | ENC order, then slot |
| 4.1 | Manifest codec, ENC §4 order | `manifest` | 2.4 passes for it | ENC's code | — | ENC order |
| 4.2 | `common.manifest_sha256` = SHA256(`F_manifest`) | frames, manifest | 3.1, 4.1 | `RECEIPT_MANIFEST_MISMATCH` | — | slot |
| 5.1 | Key format incl. public-point validation (section 8) | `keys.<slot>`, installed spec, slot | key present **and row 7.1's alg is catalog-supported** (EA-31) | `KEY_FORMAT` | — | slot |
| 5.2 | Key hashes to manifest fingerprint | key, manifest | 4.1, 5.1 | `KEY_MISMATCH` | — | slot |
| 6.1 | Frame signer fingerprints = manifest fingerprints | frames, manifest | 3.1, 4.1 | `RECEIPT_SLOT` | — | slot |
| 6.2 | Common byte substrings equal | both frames | 3.1 | `RECEIPT_COMMON_MISMATCH` | — | — |
| 6.3 | Common issuer, then alg, = manifest issuer, alg | frames, manifest | 3.1, 4.1 | `RECEIPT_MANIFEST_MISMATCH` | — | field (issuer, alg), slot |
| 7.1 | `common.alg` is the catalog-supported id (section 1) | frames, catalog | 3.1 | — | `ALG_UNKNOWN` | slot |
| 8.1 | Pinned D | `common.issuer`, D, `issuer_domain` | 3.1 | `ISSUER_NOT_PINNED` | — | — |
| 8.2 | Spec id | `common.spec.id` | 3.1 | `SPEC_ID` | — | — |
| 8.3 | Spec hash in catalog | `common.spec.sha256` | 3.1 | — | `SPEC_UNKNOWN` | — |
| 8.4 | Signed `vectors_sha256`, `preamble_sha256` = catalog | frames, catalog entry | 8.3 succeeded | `SPEC_OBJECT_MISMATCH` | (blocked: 8.3) | vectors, preamble |
| 8.5 | Binding forms (section 6.4) | `common.binding_forms` | 3.1 | — | `BINDING_FORM_UNSUPPORTED` / `BINDING_FORM_UNKNOWN` | first offending element |
| 9.1 | Receipt signature rule-O policy, incl. type-16/33 shape (section 8) | `S_slot` | 3.1, 7.1 | `SIG_POLICY` | (blocked: 7.1) | slot |
| 9.2 | Receipt signature verifies, incl. hash prefix | `F`, `S`, key | 5.1, 5.2, 7.1, 9.1 | `SIG_INVALID` | (blocked) | slot |
| 9.3 | Possession codec | `possession.<slot>` | present | ENC's code (slot diagnostic) | — | slot, ENC order |
| 9.4 | Possession policy | possession | 9.3, 7.1 | `SIG_POLICY` | (blocked: 7.1) | slot |
| 9.5 | Possession verifies over `F_manifest` | possession, key, manifest | 4.1, 5.1, 5.2, 9.4 | `POSSESSION_INVALID` | (blocked) | slot |
| 10.1 | Header equals its pin | headers, pins | — | `HEADER_CONFLICTS_PIN` | — | height |
| 10.2 | Header height pinned | headers, pins | — | — | `HEADERS_NOT_COVERED` | height |
| 10.3 | Consecutive-height prev link | header pairs | — | `HEADER_CHAIN_BROKEN` | — | lower height |
| 11.1 | Receipt OTS grammar, bounds, message sizes (section 15.2) | `receipt_anchor.ots` | present | `OTS_FORMAT` | — | byte offset |
| 11.2 | File digest = SHA256(`a_sig`) | proof, `a_sig` | 11.1 | `RECEIPT_ANCHOR_MISMATCH` | — | — |
| 11.3 | No contradicted branch | attestations, headers | 11.1 | `OTS_MERKLE_MISMATCH` | — | height, then path serialization order |
| 11.4 | Qualifying attestation; selects h*, T | proof, headers, pins | 11.1 | — | `HEADERS_MISSING` / `ANCHOR_PENDING_ONLY` | — |
| 11.5 | Txid subset (1)–(4) at h* | paths at h*, `txid` | 11.4 | `ANCHOR_TXID_MISMATCH` | — | — |
| 12.1–12.3 | Receipt conjuncts c1, c2, c3 | T, `confirmed_at`, declared | 11.4 | `TIME_BEFORE_DECLARED_EPSILON`, `TIME_AFTER_DECLARED_DELTA`, `CONFIRMATION_LATE` | — | c1, c2, c3 |
| 13.1 | Snapshot envelope and size | `dns.snapshot_body` | present | ENC §6 code, `LENGTH_CAP` | — | — |
| 13.2 | Body framing and recovery grammar (section 15.3) | body | 13.1 | `SNAPSHOT_FORMAT` | — | byte offset of first offending RR |
| 13.3 | No-wildcard body restriction | body | 13.2 framing parsed | `DNS_WILDCARD` | — | body order |
| 13.4 | Snapshot OTS: grammar; stamp digest; contradiction; qualification; shape subset (no txid) | `dns.ots`, headers | present | `OTS_FORMAT`; `SNAPSHOT_STAMP_MISMATCH`; `OTS_MERKLE_MISMATCH`; `OTS_TX_SHAPE` | `SNAPSHOT_NOT_ANCHORED` | as 11.1–11.4, in that order, then shape |
| 13.5 | DNSSEC: root group (section 5 classification, incl. `TRUST_HORIZON`), then each zone top-down (DS, then DNSKEY), then TXT (section 6.1 table) | body, trust config, T_snap | 13.2, 13.4 | section 5 / 6.1 codes | section 5 / 6.1 codes | zone order; within an RRset, the selected failing candidate's G35 tuple, then endpoint (inception before expiration), then ambiguous / reversed / window |
| 13.6 | TXT record, ENC §7 fifteen-step order | TXT RRset | present | ENC's `DNS_*` code | `DNS_EVIDENCE_MISSING` if absent | ENC order |
| 13.7 | Snapshot conjuncts | T_snap, `confirmed_at`, declared | 13.4 qualifying | `SNAPSHOT_TIME` | — | c1, c2, c3 |
| 14.1 | Commit format | `git.commit` | present | `GIT_COMMIT_FORMAT` | — | — |
| 14.2 | `gpgsig` armor, codec, policy | commit | 14.1 | `GIT_SIG_FORMAT` | — | — |
| 14.3 | Trees | `git.trees` | present | `GIT_TREE_FORMAT` | — | root, sub |
| 14.4 | SHA-1DC | commit, trees, blob | present | `GIT_SHA1_COLLISION` | — | commit, root, sub, blob |
| 14.5 | Path | commit, trees, blob | 14.1, 14.3 | `GIT_PATH` | — | — |
| 14.6 | Git OTS: grammar; stamp digest; contradiction; qualification; shape subset (no txid) | `git.ots`, headers | present | `OTS_FORMAT`; `GIT_STAMP_MISMATCH`; `OTS_MERKLE_MISMATCH`; `OTS_TX_SHAPE` | `GIT_NOT_ANCHORED` | as 13.4 |
| 14.7 | Repository signer (section 6.3 classification) | commit, sig, config, T_git | 14.1, 14.2, 14.6 | `GIT_SIGNER_OUTSIDE_INTERVAL` | `TRUST_HORIZON`, `GIT_SIGNER_NOT_CONFIGURED` | entry order (section 6.3) |
| 14.8 | Chain order `h_git + 5 < h_receipt` | h_git, h_receipt | 11.4, 14.6 | `GIT_NOT_PRECOMMITTED` | — | — |
| 15.1 | DNS value keys = manifest fingerprints | TXT value, manifest | 13.6 parsed, 4.1 | `DNS_KEY_MISMATCH` | — | slot |
| 15.2 | Git blob = DNS value | blob, TXT value | 14.5, 13.6 parsed | `CHANNEL_VALUE_MISMATCH` | — | — |
| 16.1 | Issuance window | declared, T, window | 11.4, 13.6 parsed | `ISSUANCE_WINDOW` | — | — |
| 17.1–17.3 | Bundled spec, vectors, preamble → signed hashes | objects, frames | 3.1 | `BUNDLE_OBJECT_HASH` | — | spec, vectors, preamble |
| 17.4 | Bundled dependency manifest → catalog | object, catalog entry | 8.3 succeeded | `BUNDLE_OBJECT_HASH` | (blocked: 8.3) | — |

Multiple-failure agreement cases across and within rows (possession, DNS, git included) are required vectors
(section 14.2 item 8).

*Dated correction 2026-10-14 (r2-F11): the stage sketch below, adopted from RES G31, is superseded by the table
above. It omitted possession codec codes, repeated receipt signature syntax at stage 9, left DNS edge reasons in
one unordered rank, imported the receipt txid check into snapshot and git OTS ("as 11"), omitted `TRUST_HORIZON`,
mapped git policy failures inconsistently, gave bundled-object checks no catalog dependency, and ordered candidates
by transport position. Withdrawn text:*

> Within a stage, subchecks in the order listed; per-slot checks in manifest slot order; per-member and per-candidate
> checks in canonical (JCS key, then array index) order; per-height checks ascending.
> 1. Dispatch D1–D4.
> 2. Container: canonical JCS; absent members (first absent path); `git.object_format`; schema of present members
>    (first offending path).
> 3. `a_sig` codec (ENC order).
> 4. Manifest codec; `manifest_sha256`.
> 5. Keys, per slot: `KEY_FORMAT`, `KEY_MISMATCH`.
> 6. Receipt consistency (ENC §5.3).
> 7. `ALG_UNKNOWN`.
> 8. `ISSUER_NOT_PINNED`; `SPEC_ID`; `SPEC_UNKNOWN`; `SPEC_OBJECT_MISMATCH`; binding forms (first offending element).
> 9. Signatures, per slot: `SIG_FORMAT`, `SIG_POLICY`, `SIG_INVALID`; then possession per slot.
> 10. Header pool, ascending height: `HEADER_CONFLICTS_PIN`, `HEADERS_NOT_COVERED`, `HEADER_CHAIN_BROKEN`.
> 11. Receipt OTS: `OTS_FORMAT`; `RECEIPT_ANCHOR_MISMATCH`; `OTS_MERKLE_MISMATCH`; `HEADERS_MISSING` /
>     `ANCHOR_PENDING_ONLY`; `ANCHOR_TXID_MISMATCH`.
> 12. Conjuncts c1, c2, c3.
> 13. Snapshot: envelope and `LENGTH_CAP`; body (`SNAPSHOT_FORMAT`, `DNS_WILDCARD`); OTS (as 11, with
>     `SNAPSHOT_STAMP_MISMATCH`, `SNAPSHOT_NOT_ANCHORED`); DNSSEC, root group, then each zone top-down, then TXT
>     (section 5 and 6.1 outcomes, `DNS_EVIDENCE_MISSING`); TXT record (ENC §7 order); `SNAPSHOT_TIME`.
> 14. Git: `GIT_COMMIT_FORMAT`; `GIT_SIG_FORMAT`; `GIT_TREE_FORMAT`; `GIT_SHA1_COLLISION`; `GIT_PATH`; OTS (as 11,
>     with `GIT_STAMP_MISMATCH`, `GIT_NOT_ANCHORED`); `GIT_SIGNER_NOT_CONFIGURED` / `GIT_SIGNER_OUTSIDE_INTERVAL`;
>     `GIT_NOT_PRECOMMITTED`.
> 15. `DNS_KEY_MISMATCH`, `CHANNEL_VALUE_MISMATCH`.
> 16. `ISSUANCE_WINDOW`.
> 17. `BUNDLE_OBJECT_HASH`.

### 15.8 Spec and vectors object assembly [OWNER 2026-10-14, G13]

Each object is one or more parts. A part is the ASCII line `tessera-v1-part <path> <length>` LF, then exactly
`<length>` bytes (decimal, no leading zeros), then LF. `<path>` is repository-relative UTF-8 without spaces. Parts are
in bytewise-sorted path order; file bytes verbatim as committed. The spec object holds the frozen
`docs/V1-PROFILE.md` and `formal/p8/ENCODING-V1.md` (plus the branch-registration supplement under the hybrid). The
vectors object holds every file under `formal/p8/vectors/` and the non-P8 conformance vectors (RES §L). The vectors
may embed the spec hash; the spec never embeds the vectors' hash.

**Canonical recipe** [OWNER 2026-10-14, r2-F13]. Supersedes the header and inventory sentences above where they
differ.
- **Header grammar.** `tessera-v1-part` SP `<path>` SP `<length>` LF, with fixed single literal spaces. `<path>` is an
  ASCII repository-relative path matching `[A-Za-z0-9._/-]+`, with no empty, `.` or `..` component, no leading
  slash, and unique within the object; `<length>` matches `0|[1-9][0-9]*`.
- **Bytes.** Only tracked regular-file **blob bytes** from a named freeze commit: no newline conversion, no symlink
  following, no generated caches, no working-tree overlay.
- **Inventory.** The freeze record publishes the exact sorted path inventory of each object, including the non-P8
  conformance vector files (RES §L names cases, not paths), with an assembler and an independent byte-agreement
  check.
- **A9 is a part (owner choice).** The spec object also carries the governing A9 bytes
  (`docs/phase-0-prereg-amendment-9.md` at its signing commit) as a part, so the object is the complete archival
  spec; this was chosen over distributing A9 separately with a bound digest.
- **Hashes live outside.** Actual spec, vectors and catalog hashes are recorded in a separate release/freeze record
  **outside** the frozen spec parts; recording them inside an included file would be self-reference.
- The part format is a new packaging choice, not an inherited P8 construction or a proven archival format. Once
  exact catalog hashes exist, runtime hash checks are unique; runtime never parses these objects as policy.
  *(Dated correction 2026-10-14: "repository-relative UTF-8 without spaces" admitted LF, CR, tab, absolute and
  dot paths and duplicates; "every file under formal/p8/vectors/" did not select tracked regular files; "the
  non-P8 conformance vectors (RES §L)" named cases, not files.)*
