# Spec-sufficiency gaps: resolutions (2026-10-13, owner-disposed 2026-10-14)

> **Status: OWNER-DISPOSED 2026-10-14, pending integration.** Drafted 2026-10-13 for the owner (Claude Opus 5.5).
> Revised 2026-10-14 to apply the owner's disposition (`DISPOSITION-RESOLUTIONS.md`) of the Codex adversarial
> review (`CODEX-REVIEW-RESOLUTIONS.md`, findings F01–F13 and its per-resolution table). Where Codex gave exact text,
> that text is used. Integration: `docs/V1-PROFILE.md` carries every rule below, tagged `[OWNER 2026-10-14, Gxx]`;
> `docs/V1-OPERATIONS-RUNBOOK.md` carries the issuer duty and the release-key section. **Not yet integrated:** the
> ENCODING-V1 wording edits named in G01, G02, G18, G28 and G38 (E is outside this revision's scope). Nothing binds
> until frozen on 30 Oct.
>
> Inputs: `GAPS.md` (the Codex probe, 39 rows), `docs/phase-0-prereg-amendment-9.md` (A9, governs; the owner applied
> F01–F04 there on 2026-10-14, see `a9-gap-fixes.diff`), `docs/V1-PROFILE.md` (P), `formal/p8/ENCODING-V1.md` (E),
> `formal/p8/PROOF.md` (R). Evidence of what works was read from `prototype/spike/` and `prototype/tessera_proto/real/`.
> It was treated as evidence, never as a rule.
>
> **Count.** GAPS marks 30 rows VERDICT-AFFECTING: G01–G29 plus G34. The brief's "29" is off by one.
>
> **Revised 2026-10-14 (r2-F16)** after `docs/reviews/v1-profile-r2/CODEX-REVIEW.md` F16: the owner's removal of the
> `T_git ≤ declared_issue_time` clock check is propagated to G02's CORRECT text, the issuer-duty paragraph, the G31
> reason list and conformance cases L-27/L-28. Changes are tagged `[OWNER 2026-10-14, r2-F16]`; withdrawn text is
> kept as dated corrections. The clock check is not reinstated to satisfy old vectors.

## What the 2026-10-14 revision changed

- **G02** (F01). The draft's CORRECT text is replaced by Codex's wording. A9 C4 now requires **chain-order
  pre-commitment** (`h_git + 5 < h_receipt`, BROADEN), and the verifier checks it. The issuer waits for k = 6 on the
  key-assertion stamp before issuing (runbook).
- **G03** (F03). Codex's text; the "about 2 h" bound is removed. A9 C5 now registers the lowest-height reading.
- **G05** (F02). Codex's text; A9 C6 now names the selected anchor as the referent. Its conformance cases are added.
- **G08** (F04). The dedicated trust-config signing key is **withdrawn**. Replaced by A9.5's trust-configuration
  authority: independent release allowlisting. Release-key custody is OPEN.
- **G16** (F05). Codex's root/DS text. DS digest type 4 is **retained**. The algorithm allowlist is a visible owner
  scope choice.
- **G26/G31/G32** (F06). A fixed reporting order; early exit only when every stable field is settled.
- **F07–F13** (G11, G19/G24, G20, G21, G14/G15/G17/G33, G09, G22) applied as proposed. **G23 = INVALID.**
- **Change accounting.** §K's blanket "none" is withdrawn. New completion choices are labelled **OWNER CHOICE
  (supported-path limit)**, not CLARIFY. "No signed byte change" is narrowed to **no attestation-frame layout
  change**; what does get new hashes or signatures is listed below the top table.
- **Conformance.** All cases are now in one list, §L.

## Top table

Labels: **CLARIFY** makes an existing registered rule precise. **OWNER CHOICE (supported-path limit)** is a new
completion choice that A9 delegates to the profile; where it rejects inputs another reasonable completion would
accept, the limit is visible. **BROADEN** extends coverage. **NARROW-CLAIM** is a visible scope limit for relying
parties. **NARROW-MODEL** concedes protection the world provides and goes to the author. **CORRECT** withdraws text
that claimed protection the external system does not supply. "A9" in the last column means the owner changed A9's
text on 2026-10-14 (A9 is still PROPOSED, so the change is in the instrument, not a separate amendment).

| Gap | One-line resolution | Label | Lands | A9 |
|---|---|---|---|---|
| G01 | Signed `binding_forms` must equal `["STMT_DIRECT"]`. Other ids give `UNVERIFIABLE`: `BINDING_FORM_UNSUPPORTED` for `STMT_DIGEST`, `BINDING_FORM_UNKNOWN` otherwise; the reason is the first offending element in canonical order | OWNER CHOICE (required-set selection) | P §6.4 | no |
| G02 | ~~`T_git ≤ declared_issue_time`~~ (dropped by owner 2026-10-14), **chain-order pre-commitment** `h_git + 5 < h_receipt`. Codex's CORRECT text replaces the draft's. The issuer waits for git k = 6 | CORRECT + ~~OWNER CHOICE (comparison)~~ (comparison dropped; r2-F16) + BROADEN (chain order, A9 C4) + issuer duty | P §6.3; runbook; E §7.1 wording (pending) | C4 edited |
| G03 | Earliest = **lowest block height** among qualifying attestations, not least nTime. T and `confirmed_at` both come from that segment | CLARIFY (registered in A9 C5) | P §7.1 | C5 edited |
| G04 | `confirmed_at` = nTime(h* + 5): inclusion plus five successors (k = 6, R-3.45). No monotonicity test | CLARIFY (depth); header-time proxy newly explicit | P §7.1 | no |
| G05 | Selection is existential over qualifying branches. A branch without its h..h+5 segment is nonqualifying, not a failure. Every supplied header is checked against the pins | OWNER CHOICE (registered reading, A9 C6) | P §7.1, §7.2 | C6 edited |
| G06 | The snapshot proof uses the same T rule and k = 6; all three conjuncts against the receipt's declared time; inside every selected RRSIG window | CLARIFY (T rule) + OWNER CHOICE (snapshot c3: acceptance restriction) | P §7.3 | no |
| G07 | Required headers are h*…h*+5 of each proof's selected attestation. No PoW or retarget check | CLARIFY (conditional on trustworthy pins) | P §7.2 | no |
| G08 | Trust configuration authenticated by **independent release allowlisting** (A9.5): each verifier release compiles in its config hash; releases signed by a key no authority-channel credential can use. Otherwise no verdict | New distribution design + stated boundary (A9.5) | P §5 | A9.5 edited; boundary added |
| G09 | Open end = usable through `as_of`. Release invariants freeze identity, key bytes, D, starts, L and finalized ends; `as_of` nondecreasing | OWNER CHOICE (endpoint convention A9.5 delegates) | P §5 | no |
| G10 | M5: `key_fp`, `sset` by both channel values; `issuer` by the owner name and the pinned-D gate; `alg`, `ver` by single-valued profile constants | CLARIFY | P §6.4 | no |
| G11 | Rule-O signature policy: exactly one hashed type-2 subpacket of four data octets, critical or not; hashed type 3 forbidden; unknown critical hashed subpackets rejected; unhashed area ignored | OWNER CHOICE (supported-path limit: signature profile) | P §8 | no |
| G12 | Frozen one-entry spec catalog; explicit empty prohibited set; other well-formed id `UNVERIFIABLE / ALG_UNKNOWN` | OWNER CHOICE (frozen policy selection) | P §1, §8 | no |
| G13 | Spec id exact; spec hash in catalog; objects match catalog; bundled bytes hashed, never executed; exact spec-object assembly format | OWNER CHOICE (packaging) | P §1, §2 | no |
| G14 | Closed container, one tuple route (`a_sig`). Absent member `UNVERIFIABLE`; present nonconforming or unknown member `INVALID`. Absence rule precedes the generic schema rule | OWNER CHOICE (supported-path limit: transport subset) | P §2 | no |
| G15 | Closed JCS dependency manifest; seven R-3.51 fields plus `id`, `title`; complete entry list; hash in catalog | BROADEN | P §9 | no |
| G16 | DNSSEC algorithms {8, 13}; DS digest types {2, 4}. Root passes only under A9.5 reliance. Explicit DS outcomes | NARROW-CLAIM (allowlist, visible owner scope choice) | P §6.1, §7.3, relying-party text | no |
| G17 | Container: strict canonical JCS, no JSON numbers, decimal-string grammar `0|[1-9][0-9]*`. Dispatch reads `profile`, the length of `layers` and the request policy, nothing else | OWNER CHOICE (supported-path limit: container, canonicality) | P §2, §3.1 | no |
| G18 | Years 0001–9999; LDH labels may be all-numeric. Codifies both codecs | CLARIFY | E §3.2 wording (pending) | no |
| G19 | Snapshot body = fixed-order sequence of uncompressed canonical RFC 1035 wire RRs; framing violations `INVALID`, missing groups `UNVERIFIABLE`; no wildcards | OWNER CHOICE (body format) + NARROW-CLAIM (no wildcard) | P §7.3 | no |
| G20 | Closed OTS grammar; txid = the declared calendar-transaction witness: the first sha256 pair's input must parse as a conforming non-witness transaction carrying the path commitment in an `OP_RETURN` output | OWNER CHOICE (supported-path limit: proof subset) | P §2, §7.1 | no |
| G21 | `gpg` key = v4 P-256 public-key body; `kms` = P-256 DER SPKI under the fallback or the supplement's ML-DSA-65 SPKI under the hybrid, selected by installed spec and slot | CLARIFY (with branch exception) | P §2, §8 | no |
| G22 | Full DNSKEY RDATA per KSK from an archived authenticated source carrying the key; REVOKE-bit RDATA never matches; concrete intervals recorded | OWNER CHOICE (trust serialization and acquisition) | P §5 | no |
| G23 | A supplied header at a pinned height with a different hash: `INVALID / HEADER_CONFLICTS_PIN`. "Outside the pins" means an uncovered height | OWNER reading of A9.1 | P §7.2 | no |
| G24 | A present nonconforming TXT is `INVALID` (E's codes) whether or not DNSSEC is performable; an absent TXT RRset is `UNVERIFIABLE / DNS_EVIDENCE_MISSING` | CLARIFY + completeness exception | P §3.2 | no |
| G25 | Closed git subset (commit headers, armor, canonical trees, SHA-1DC, P-256 repository key) | OWNER CHOICE (supported-path limit: git subset) + BROADEN (SHA-1DC) | P §6.3 | no |
| G26 | Physical order unrestricted; reporting uses one fixed total check order; early exit only when every stable field is settled | CLARIFY (A9.4 stable-field contract) | P §3.3 | no |
| G27 | RFC 1982 serial arithmetic around T_snap; an exact half-range difference and a reversed interval are explicit candidate failures | CLARIFY + OWNER CHOICE (edge outcomes) | P §7.3 | no |
| G28 | Subpacket lengths per RFC 9580; V1 accepts shortest form only | CLARIFY (V1 rule, not an RFC ban) | E §5.2 wording (pending) | no |
| G29 | `ES` = ECMA-262 Number::toString of a pinned edition, full algorithm including closest/ties-to-even digit selection; Unicode 16.0.0 tables pinned by digest | CLARIFY | P §9, §10 | no |
| G34 | One gate before both channels: `common.issuer` = `wamason.com`, else `INVALID / ISSUER_NOT_PINNED` | CLARIFY + new early failure classification | P §6.3 | no |
| G30–G33, G35–G39 | Reason-only or already resolved; see §J | see §J | P | no |

### Byte, hash and vector accounting (replaces "no signed byte changes")

**No resolution changes the attestation-frame layout** (E§3–§5, `A_sig`, the manifest frame), and no existing
fallback P8 golden or rejection vector needs rewriting merely to add above-codec policy. The following **do** get new
hashes or signatures:

1. **Spec and vectors objects.** Freezing edited V1-PROFILE/ENCODING-V1 text and the new conformance vectors changes
   the `spec`, `vectors`, `preamble` and `dependency_manifest` hashes. Receipts issued under the frozen spec carry the
   new `common.spec.sha256` and related hashes in their signed common bytes.
2. **DNSSEC snapshot body.** Converting from resolver-message JSON to the G19 body changes S and `SHA256(S)`. Each
   snapshot needs a fresh stamp. Previously stamped JSON snapshots cannot be reused.
3. **Trust configuration.** New bytes, a new hash compiled into a verifier release, and a new release signature by
   the release key (G08).
4. **Signature output.** G11's policy constrains what the issuer's OpenPGP adapters may emit before signing and
   stamping.
5. **Hybrid branch.** If taken, the authorized supplement changes the `kms` slot encoding and requires its own
   golden and rejection vectors (A9.6). That is an existing A9 obligation, excluded from any "no change" statement.
6. **Archived proofs.** Existing archived proof bytes cannot be converted in place while retaining their stamp.

New **non-P8** conformance vectors are required for the container, OTS, snapshot body, git evidence, trust
configuration, signature profile and full-profile verdicts (§L). A9.5 already requires the git cases before the
freeze.

**NARROW-MODEL:** none established. One conditional author surface remains: if release-key custody cannot be made
independent of every authority-channel credential (G08), a channel-capture path must be excluded, which is a
NARROW-MODEL for the author. See §K.

---

## Principles applied

1. **Fail-closed.** Where two readings differ, the one that cannot return `VALID_STRICT` on evidence the other
   rejects wins, unless it falsely rejects receipts from the documented issue path. Tensions are named per gap.
2. **Pruning equivalence, bounded (time cluster).** An OTS proof is unsigned, outside `A_sig` (E§5), and can be
   pruned to any one of its attestations without breaking the digest. Whoever presents a receipt can therefore already
   choose which verified attestation sets T (A9 C5: "presentation-sensitive T"). Within the coverage contract A9 C6
   now registers, ignoring a branch without headers yields no new cryptographic false accept. It does **not** make
   contradictory evidence harmless: a contradicted branch fails the proof. Nor does it make two different selection
   rules agree on the same input (G03).
3. **Verdict class.** Present evidence whose check runs and fails gives `INVALID` (R-2.31). Absent evidence gives
   `UNVERIFIABLE` (case d2). After dispatch, every codec rejection gives `INVALID` (E§8). Where a later, append-only
   trust configuration could legitimately cover the evidence, the class is `UNVERIFIABLE` (A9.5: "can improve an
   earlier UNVERIFIABLE result"). Where no later configuration could, it is `INVALID`.
4. **Verdict stability (A9.4).** Policy that decides a verdict (algorithm, parameters, binding forms, D, DNSSEC
   algorithm set) lives in the **frozen spec catalog** compiled into the verifier, not in the trust configuration.
   This moves P §5 item 5 (δ, ε, k) out of the trust configuration. A9.4's contract is exact stable-field identity
   for identical declared inputs. It is **not** a monotonic-verdict promise across configurations (G09).

---

## A. Container and evidence formats: G17, G14, G21, G19, G20

### G17: container and dispatch — OWNER CHOICE (supported-path limit)

- **Resolution.** A bundle is one UTF-8 JSON text. It must pass E§1.4 checks 1–5 and 7: strict UTF-8, RFC 8259
  syntax, depth, duplicate names, string rules, and canonical JCS. It contains **no JSON numbers**. Heights and
  durations are decimal strings with grammar `0|[1-9][0-9]*` and value at most 4294967295 (no aliasing by leading
  zeros). Binary values are RFC 4648 §4 base64 with padding that must round-trip (no non-zero pad bits, no line
  breaks). The size cap is 2^27 bytes.

  Top level is exactly `{"layers":[L],"profile":"tessera-v1-strict"}`. Dispatch, in order:
  - **D1.** The bytes are not strict JSON (checks 1–5), or they exceed the cap: `UNVERIFIABLE / OUT_OF_PROFILE`.
    No label can be read.
  - **D2.** `profile` is absent or not exactly `tessera-v1-strict`: `UNVERIFIABLE / OUT_OF_PROFILE`.
  - **D3.** `layers` is not an array of length 1: `UNVERIFIABLE / OUT_OF_PROFILE`. This covers cases c and h.
  - **D4.** The request policy is a **verifier input**, not a bundle member. Its only value is `strict`. Any other
    request gives `UNVERIFIABLE / OUT_OF_PROFILE` (detail `REQUEST_UNSUPPORTED`) with no evaluation, which is case
    d1's "waiver refused".

  After dispatch, rules apply in this order (F11): (1) a non-canonical container gives `INVALID / JSON_NONCANONICAL`;
  (2) **G14's absence rule**, including nested evidence members, and A9.5's `git.object_format` outcomes; (3) any other
  schema failure gives `INVALID / CONTAINER_SCHEMA`.
- **Layer `L` (closed schema).** Every value is base64 unless marked. Cardinality is exactly one of each.

  | Member | JSON type and content | Invariants |
  |---|---|---|
  | `a_sig` | string: `A_sig` bytes (E§5) | decoded by E§5 |
  | `manifest` | string: `F_manifest` | decoded by E§4 |
  | `possession` | object `{"gpg","kms"}`: each a detached signature over `F_manifest` per its slot rule | both keys present |
  | `keys` | object `{"gpg","kms"}` (G21) | both keys present |
  | `receipt_anchor` | object `{"ots","txid"}`; `ots` base64; `txid` 64 lowercase hex, display order | |
  | `headers` | object `{"<height>":"<160 lowercase hex>"}`: one shared pool for all three proofs | height grammar above; nonempty |
  | `dns` | object `{"ots","snapshot_body"}` (G19), both base64 | |
  | `git` | object `{"blob","commit","object_format","ots","trees"}`; `trees` an array of exactly 2 base64 strings [root, sub]; `object_format` a string | A9.5 descriptor rules |
  | `spec`, `vectors`, `preamble`, `dependency_manifest` | string: raw bytes | hashed only (G13) |
  | `issuer_record` | **optional** object `{"observed_anchor_delay_s","policy_version"}` (G33) | see G33 |
- **Rationale.** A9.5 fixes dispatch on an unsigned label and `OUT_OF_PROFILE` at dispatch. DD:70 names "profile,
  layer structure or request", and an explicit `layers` array makes case c and case h dispatch failures, not schema
  `INVALID`s. JSON reuses the strict parser the verifier already needs, so the container adds no codec. Banning
  numbers keeps the container clear of `ES`. The container is unsigned transport, so it adds no P8 construction.
- **Supported-path limit, visible.** Requiring canonical JCS makes a container that a holder's tool re-indented
  `INVALID`, which is permanent. It gains no security, because every member is checked byte for byte. It is a new
  custody restriction, not an inherited rule. The holder's custody text must say: keep the bytes, do not reformat.
  (Codex noted the prototype issuer emits indented JSON; that is an instrument, not a conforming V1 issuer.)
- **Rejected.** ZIP or tar: a new parser dependency. A tagged binary TLV: a new P8 construction. A request field
  inside the bundle: then an attacker sets it.

### G14: inventory and completeness — OWNER CHOICE (supported-path limit)

- **Resolution.** The member list is exactly G17's. Only `issuer_record` is optional. A required member that is
  **absent**, at any nesting level, gives `UNVERIFIABLE / MEMBER_MISSING:<path>`; for example, no `git` member is
  case d2. This rule is applied **before** the generic schema rule (G17). `git.object_format` follows A9.5 exactly:
  absent gives `UNVERIFIABLE / GIT_OBJECT_FORMAT_MISSING`; a present value other than `"sha1"` gives
  `UNVERIFIABLE / GIT_OBJECT_FORMAT`; neither is a generic schema `INVALID`. A member that is **present but
  nonconforming**, or a member the schema does not name, gives `INVALID / CONTAINER_SCHEMA`. There is **one tuple
  route**: the receipt tuple is taken only by decoding `a_sig` (E§5.3's first route).
- **Rationale.** E§5.3 makes both routes equal by Lemma 7 when they agree; offering one removes the reconciliation
  fork. This is a transport subset, not a claim that Lemma 7 mandates one route. One-key structural failures
  (`ANCHOR_COUNT`, `RECEIPT_SLOT`) are `INVALID` and dominate missing-channel `UNVERIFIABLE` (case d3).
- **Rejected.** Ignoring unknown members: lenient, no benefit on the issue path.

### G21: transported public keys — CLARIFY (with branch exception)

- **Resolution.**
  - `keys.gpg` is the **bare v4 public-key packet body**, exactly the `gpg-sha256` preimage of E§3.3: no `0x99`
    prefix, no packet header, no user IDs, no subkeys, no armour.
  - **F10 text:** "gpg must parse as the specified v4 P-256 public-key body. kms must parse as P-256 DER SPKI under
    the fallback, or as the exact ML-DSA-65 SPKI specified by the dated branch supplement under the hybrid. The rule
    is selected by the installed governing spec and slot, never by key bytes alone." Otherwise `INVALID / KEY_FORMAT`.
  - Each key must hash to its slot fingerprint (`INVALID / KEY_MISMATCH`).
  - Under the fallback the kms slot's OpenPGP rule-O signature is verified with the SPKI point. Its OpenPGP wrapper
    creation time is unbound (E§3.3, accepted).
- **Rationale.** These are exactly the bytes the fingerprints commit to. No subkey heuristic. Hybrid signed encodings
  and vectors remain an A9.6 obligation and are excluded from every "no change" statement.
- **Rejected.** An OpenPGP certificate or transferable public key: subkey selection forks.

### G19: DNSSEC snapshot body — OWNER CHOICE (body format) + NARROW-CLAIM (no wildcards)

- **Resolution.** `snapshot_body` is a concatenation of resource records. Each is in RFC 1035 §3.2.1 wire format,
  **uncompressed**, in RFC 4034 §6.2 canonical form: the owner name and **every domain-name field inside RDATA**
  (including the RRSIG signer name) are lowercase and uncompressed. Each RR is self-delimiting, so the body needs no
  extra framing. This is the chain shape of RFC 9102 §4. V1 adds a fixed order and a closed set:
  1. **Groups, in this order.** First the root DNSKEY group. Then, for each zone z below the root down to the TXT's
     signer zone, a DS group at z followed by a DNSKEY group at z. Last, the TXT group at `_tessera-v1.<D>`.
     - **Group boundary.** A group is a maximal run of RRs with the same owner name, CLASS IN, and either TYPE t (the
       RRset) or TYPE RRSIG with Type Covered t (its witnesses). Within a group the RRset comes first, in RFC 4034
       §6.3 canonical RDATA order with no duplicates, followed by zero or more RRSIGs covering it, in (key tag,
       inception, expiration, signature bytes) order.
     - Each z must be a proper descendant of the previous zone. A DS or DNSKEY RRSIG's signer name must be the zone
       the RFC requires (the parent for DS; z itself for DNSKEY; the root for the root group). Every TXT RRSIG's
       signer name must be the last z.
  2. **Fields.** CLASS is IN. The TTL is equal within an RRset (RFC 2181 §5.2) and is otherwise uninterpreted:
     validation uses the RRSIG's Original TTL (RFC 4035 §5.3.2).
  3. **Framing versus completeness (F08 text).** "A truncated RR encoding, forbidden RR type, duplicate RR,
     inconsistent owner/type within a group, or misordered supplied group is INVALID/SNAPSHOT_FORMAT. A
     syntactically complete sequence lacking a required RRset or its witness RRSIG is UNVERIFIABLE/DNS_EVIDENCE_MISSING
     (or the root-specific NO_TRUSTED_KSK_USABLE). Missing groups do not alone constitute order violations. All
     domain-name RDATA fields are encoded canonically under RFC 4034 §6.2." An empty body is `LENGTH_CAP` (G30).
     Forbidden types: any type other than DNSKEY, DS, TXT and RRSIG (SOA, NS, NSEC, NSEC3, CNAME, DNAME, …), and any
     RR at a name outside the chain. CNAME and DNAME are not followed.
  4. **No wildcards.** A TXT RRSIG whose Labels field is less than the owner's label count (a wildcard expansion,
     RFC 4035 §5.3.2) gives `INVALID / DNS_WILDCARD`. This is a visible NARROW-CLAIM: the issuer publishes an
     explicit record.
  5. **Envelope.** The stamped preimage is E§6: `header ‖ u32 len ‖ body`, with 1 ≤ len ≤ 2^24.
- **Rationale.** E§6 and P §7.3 leave the body to the profile. RRSIG verification needs canonical RR wire form
  anyway (RFC 4034 §6). The instrument (`spike/capture_dns.py`) stores whole resolver messages as base64 inside
  JSON; converting them is mechanical and happens **before stamping**. The conversion changes S and `SHA256(S)`, so
  each snapshot needs a fresh stamp; previously stamped JSON snapshots cannot be reused. P8's envelope construction
  and existing vectors do not change. No conforming explicit-owner V1 receipt is shown falsely rejected after fresh
  capture and conversion; the archived spike output is not a conforming V1 bundle.
- **Residual, stated.** Under DNSSEC an ancestor zone (root, `com`) can sign data for names below it. V1 inherits
  this trust (C4 "DNSSEC authenticated"), and the n = 2 git channel is what guards against it.
- **Rejected.** Raw resolver messages: compression and flag noise. JSON presentation format: re-parsing ambiguity.
  RFC 9102 order-independence: fail-closed prefers one order.

### G20: OTS and Bitcoin evidence encoding — OWNER CHOICE (supported-path limit)

- **Resolution, OTS grammar** (the OpenTimestamps `DetachedTimestampFile` serialization, major version 1, as
  specified here; python-opentimestamps 0.4.5 is the reference reader, not normative):
  - **Header.** Magic `00 4f70656e54696d657374616d7073 0000 50726f6f66 00 bf89e2e884e89294`, then varuint major
    version = 1, then file-hash op `08` (SHA-256 only), then the 32-byte digest, then one Timestamp, then end of
    input.
  - **Timestamp.** `Timestamp := (ff Item)* Item`, where `Item := 00 Attestation | Op Timestamp`.
  - **Ops.** `Op := 08` (sha256) `| f0 varbytes` (append) `| f1 varbytes` (prepend). An argument is 1–4096 bytes,
    and every message and result is at most 4096 bytes.
  - **Attestations.** `Attestation := tag(8) varbytes(payload)`, with payload at most 8192 bytes. A Bitcoin tag
    `0588960d73d71901` has a payload of exactly one varuint height, consumed exactly. A pending tag
    `83dfe30d2ef90c8e` has a payload of varbytes(URI ≤ 1000); its URI is ignored.
  - **Varuint.** LEB128 (7-bit groups, little-endian, high bit set for continuation), **shortest form only**, value
    at most 2^32 − 1, so at most 5 groups. A redundant form (for example a trailing `00` group after a continuation)
    gives `INVALID / OTS_FORMAT`. *This diverges from python-opentimestamps 0.4.5, which accepts redundant groups;
    the instrument must be updated. Real calendars write shortest form.*
  - **Bounds.** Recursion depth at most 256; at most 65536 ops and 4096 attestations per proof; proof bytes at most
    2^20. Duplicate identical branches are permitted and have no effect (selection is existential, G05).
  - **Rejections.** Any other op (SHA-1, RIPEMD-160, Keccak, reverse, hexlify), any other attestation tag, or any
    limit or grammar violation gives `INVALID / OTS_FORMAT`. The file digest must equal SHA256 of the stamped
    object: `A_sig` for the receipt (`INVALID / RECEIPT_ANCHOR_MISMATCH`), the E§6 envelope for the snapshot
    (`INVALID / SNAPSHOT_STAMP_MISMATCH`), and `<40-hex commit id>\n` for git (`INVALID / GIT_STAMP_MISMATCH`).
  - **Merkle link.** A Bitcoin attestation's message must be 32 bytes and equal bytes 36–68 of the bundled 80-byte
    header at that height (the merkle root, internal order).
- **Resolution, txid (F09, the supported-proof subset).** `txid` stays (R-3.42, R-3.43, registered: "the anchor
  transaction's id … identity/coherence handle"). On the path from the file digest to the **selected** attestation
  (G03), let the first two consecutive sha256 ops be the transaction pair, with input P. Let m be the message
  immediately before the maximal run of append/prepend ops that precedes the pair. The proof is in the supported
  subset only if:
  1. P parses exactly, consuming every byte, as a Bitcoin transaction in **non-witness serialization**: version (4),
     compact-size input count ≥ 1, inputs (32 + 4 + compact-size script length + script + 4), compact-size output
     count ≥ 1, outputs (8 + compact-size script length + script), locktime (4). A SegWit marker (`00 01` after the
     version) is not allowed. Compact sizes are shortest form.
  2. m is 32 bytes and some output script is exactly `6a 20 ‖ m` (an `OP_RETURN` push of the path commitment).
  3. `hex(reverse(SHA256d(P)))` equals `txid`. The remaining path from SHA256d(P) to the merkle root is the
     declared transaction-to-block path and is verified by the merkle link.
  Otherwise `INVALID / ANCHOR_TXID_MISMATCH`. If several attestation paths reach the selected height, any one of
  them may satisfy this.
- **Evidence.** All 127 real proofs in the repository (`timestamps/**`, the spike proofs) carry 344 Bitcoin and 500
  pending attestations, using **only** sha256, append and prepend. On every one of the 344 Bitcoin paths the first
  sha256 pair takes a 125-byte input that parses exactly as a non-witness transaction with an output `6a 20 ‖ m`,
  where m is the message before a run of two ops (prepend, append). Checked read-only on 2026-10-14 with the
  prototype environment's python-opentimestamps. (The draft's 126 files / 496 pending was one file short.)
- **Rationale.** Codex's counterexample (a proof that first double-hashes the digest into a commitment hash, then
  commits that in a real transaction) is a valid timestamp whose first double-hash is not a transaction id. The
  subset rule rejects it visibly rather than mislabelling the coherence handle. It is not a forged timestamp or a
  C1/C2 attack. The closed op and tag set is a scope restriction, not an A9 protection theorem: SHA-1 commitments are
  weaker, but rejecting strong unused operations protects nothing.
- **Rejected.** Requiring canonical re-serialization (library-specific sort order). Dropping the txid (registered).
  Trial-parsing any pair as a transaction (the instrument's `_is_tx`): a heuristic. Making the txid advisory: that
  would need a registered correction.

---

## B. The time cluster: G03–G07, with G23

One rule serves all three proofs: the receipt, the snapshot and the git commit.

**Qualifying attestation.** A Bitcoin attestation at height h *qualifies* if and only if all of the following hold:
- (a) the bundled header at h exists and its merkle root equals the attestation message;
- (b) headers h, h+1, …, h+5 are all bundled (k = 6, `DepthK = 5`);
- (c) each of those headers satisfies `hex(reverse(SHA256d(header))) = pin[height]`;
- (d) for i = h+1…h+5, `header_i.prev = SHA256d(header_{i−1})`.

**Selection rule (F02 text).** "Attestation selection is existential over qualifying branches. A syntactically valid
Bitcoin attestation without a complete h..h+5 segment is nonqualifying, not a required failed check. It supplies no
time or trust fact. All supplied headers, including unused ones, are independently checked against pins. For each
adjacent supplied pair at consecutive heights, the prev-hash link must match. Missing heights are not a broken-link
failure. The selected anchor, rather than every unverified attestation, is the referent of 'anchors beyond the newest
pin.'" A9 C6 now registers this reading (OWNER DECISION 2026-10-14, F02).

**Header-pool checks** (shared pool, every supplied header, used or not):
- **G23.** A supplied header at a pinned height with a different hash: `INVALID / HEADER_CONFLICTS_PIN`.
- **A9 rule.** A supplied header at a height with **no** pin: `UNVERIFIABLE / HEADERS_NOT_COVERED`.
- **Linkage.** For each pair of supplied headers at consecutive heights, a prev-hash mismatch gives
  `INVALID / HEADER_CHAIN_BROKEN`. A missing intermediate height is not a broken link.
- **Asymmetry, stated.** At an unselected height q, a present, correct, pinned inclusion header with missing
  successors is ignored (the branch is nonqualifying). A present **unpinned** header at q blocks the whole bundle
  (`UNVERIFIABLE`) by the pin rule above.

**Proof-level outcomes**, evaluated over every Bitcoin attestation in the proof:
- **Contradiction gives INVALID.** A supplied header at h that is pinned and whose merkle root ≠ the attestation
  message gives `INVALID / OTS_MERKLE_MISMATCH`.
- **No qualifying attestation.** If any Bitcoin attestation is present, `UNVERIFIABLE / HEADERS_MISSING`. If the
  proof has only pending attestations, `UNVERIFIABLE / ANCHOR_PENDING_ONLY`. The snapshot uses its own code,
  `SNAPSHOT_NOT_ANCHORED`, and git uses `GIT_NOT_ANCHORED`.
- **Otherwise.** h* = the **lowest** qualifying height. T(proof) = nTime(h*), and `confirmed_at`(proof) =
  nTime(h* + 5).

Times are integer seconds since 1970-01-01T00:00:00Z with no leap seconds. nTime is the header's uint32. RFC 3339
fields are converted by days-from-civil (proleptic Gregorian), and comparisons are inclusive as registered.

### G03: T and anchor_time — CLARIFY (A9 C5 as revised)

- **Resolution (F03 text).** "Earliest means lowest Bitcoin block height among qualifying attestations, not least
  nTime. Both T and confirmed_at come from that selected segment. Nonmonotone timestamps can make another selection
  rule return a different verdict on the same proof. This profile fixes the chain-order reading of A9 C5." For the
  receipt proof, T ≡ `anchor_time` ≡ nTime(h*). The same value feeds conjuncts 1 and 2, the C4 window rule and the
  reported T. Two qualifying attestations at the same height select the same header, so T and `confirmed_at` are the
  same either way.
- **Owner confirmation.** A9 C5 now reads "the verified attestation at the lowest block height in the presented OTS
  proof (both T and its confirmations come from that attestation; OWNER DECISION 2026-10-14, F03)". No amendment
  beyond that edit; no signed layout or P8 vector changes.
- **Withdrawn (2026-10-14).** The draft's "with non-monotone nTime (up to about 2 h)" is removed: the forward-clock
  check does not establish a general bound on nonmonotonicity. The draft's "smallest nTime mixes blocks" objection is
  also withdrawn: an implementation can take both values from the attestation selected by smallest nTime.
- **Rationale.** Lowest height is deterministic once qualification is fixed. It is not equivalent to lowest
  timestamp: with h1 < h2, `nTime(h1) = not-after + 1` and `nTime(h2) = not-after`, height selection gives
  `ISSUANCE_WINDOW` and time selection gives `VALID_STRICT`. A9 now fixes which rule governs.

### G04: confirmed_at — CLARIFY

- **Resolution.** `confirmed_at` = nTime(h* + 5) for the **selected** attestation: the including block plus five
  successors, which is k = 6 (R-3.45, R-4.42 `DepthK = k − 1`). Conjunct 3 is `confirmed_at ≤ declared + δ`. All
  three conjuncts are evaluated together (R-5.19). A failure gives `INVALID`: `TIME_BEFORE_DECLARED_EPSILON`,
  `TIME_AFTER_DECLARED_DELTA` or `CONFIRMATION_LATE`.
- **No monotonicity test.** Nonmonotone header times can give `confirmed_at < T`. That is not a failure; do not add
  an unstated monotonicity check. The header time as a chain-time proxy is now explicit (A9 C5 non-claim).
- **Rejected.** Counting six successors: contradicts R-3.45 ("the including block … being the first confirmation").

### G05: attestation selection and disqualification — OWNER CHOICE (registered reading, A9 C6)

- **Resolution.** As in the selection rule and outcomes above. A contradicted attestation fails the whole proof. An
  attestation without its complete segment is nonqualifying and ignored. A supplied but unpinned header gives
  `UNVERIFIABLE` through A9's pin rule.
- **A9 reading.** A9 C6 now reads: "A selected anchor (C5) beyond the newest pin is `UNVERIFIABLE`. Every supplied
  header must be pinned. An unselected attestation without its headers supplies no fact and is not a failure (OWNER
  DECISION 2026-10-14, F02)." The earlier wording ("Anchors beyond the newest pin are `UNVERIFIABLE`") was open to a
  universal reading; the owner chose the selected-anchor reading and recorded it in A9 rather than overriding it
  silently.
- **Rationale.** No new cryptographic false accept arises from ignoring a missing-header branch while a real,
  digest-linked, depth-6 pinned branch qualifies: removing the missing branch gives the same selected witness. The
  stricter reading would reject honest holder-upgraded proofs, the case A9.6's relying-party text addresses. A branch
  with no headers is an unverified assertion only, not a verified forgery. No NARROW-MODEL follows from pruning alone.
- **Departs from the instrument**, which returns `UNPERFORMABLE` for any uncovered attestation
  (`verify_offline.py` `check_ots`).
- **Rejected.** Ignoring contradicted attestations: that would let a presenter carry a forged branch.

### G06: the snapshot's anchored time — CLARIFY + OWNER CHOICE (snapshot c3)

- **Resolution.** T_snap = T(snapshot proof) under the same rule and depth. The verifier requires:
  - the three conjuncts with T_snap and `confirmed_at`(snapshot), against the **receipt's** signed declared time
    (P §7.3). A failure gives `INVALID / SNAPSHOT_TIME`;
  - for each selected witness RRSIG (G27, G35), inception ≤ T_snap ≤ expiration;
  - DNSSEC evaluated at T_snap only. No capture time, receipt T or wall clock is ever used.
- **Label.** The T rule and depth are CLARIFY. **Conjunct 3 on the snapshot is a new owner acceptance restriction**
  (fail-closed), not an existing CLARIFY. The instrument already applies it (`check_snapshot_time`).
- **Withdrawn (2026-10-14).** The draft's "honest-safe: the snapshot is stamped no later than the receipt" is
  withdrawn. A snapshot stamped earlier need not confirm earlier: distinct calendars and branches can confirm in a
  different order, and a receipt passing c3 does not imply the snapshot does. **Issuer duty:** check snapshot c3
  before shipping and recapture or retry if it fails (P §4).
- **Rejected.** Depth 1 for the snapshot: an unconfirmed anchor could be reorganized away.

### G07: pins and history coverage — CLARIFY (conditional on trustworthy pins)

- **Resolution.** Required: headers h*…h*+5 for each of the three proofs' selected attestations, all supplied in
  `headers`. Every supplied header must be pinned (A9.1). No PoW, nBits or retarget check is made; a hash that equals
  a pin implies all of it. Linkage is checked as in the header-pool rule.
- **Rationale.** A9.1 says "no retarget logic" because the pins cover every accepted header. Correct
  implementations differ only when the pins are wrong. `check_segment`'s `RETARGET_NOT_IMPLEMENTED` stop would
  falsely reject segments crossing a 2016-block boundary, so that stop is withdrawn.
- **Rejected.** Pinning only the inclusion header: it cannot establish depth.

### G23: header that conflicts with a pin — OWNER reading: INVALID

- **Resolution.** `INVALID / HEADER_CONFLICTS_PIN`. Same as the instrument. **OWNER DECISION 2026-10-14:** a
  conflicting pinned header is contradictory evidence.
- **A9 reading.** A9.1's "a bundle header outside the pins gives `UNVERIFIABLE / HEADERS_NOT_COVERED`" is read as
  **at a height the pins do not cover**. The alternative class is not left open in the frozen spec.
- **Rationale.** R-2.31: the evidence is present, the check runs and fails. Pins are append-only and a height has
  one canonical hash, so no later configuration can cover the header. `INVALID` is stable under A9.4.

---

## C. Trust formats: G08, G09, G22

### G08: authenticating the trust configuration — new distribution design (A9.5)

- **Withdrawn (2026-10-14).** The draft's dedicated trust-config signing key (a detached rule-O signature on the
  config by a third key, append-only enforced in CI) is withdrawn. Key inequality alone does not establish
  independence: a distinct key can still be callable through a captured channel account or shared signing service,
  and append-only CI cannot stop an attacker who can bypass CI from adding their own root KSK, repository key and
  pins (F04). The draft's rejected-option text "an unsigned config trusted because it came with the release" is also
  withdrawn: an unsigned config inside an authenticated, integrity-checked release can be trustworthy.
- **Resolution (A9.5 "Trust-configuration authority", and F04 text).** "The accepted trust-config authority is
  authenticated independently of the bundle and of both authority-channel credentials. Capture of any
  authority-channel credential grants no config signing capability, no ability to authorize a new config hash, and
  no ability to replace the verifier's compiled trust root or policy catalog. The dated custody record names and
  verifies that authorization boundary. The verifier accepts only configs authenticated by this declared mechanism;
  CI alone is not its authenticity check." The mechanism chosen is **independent release allowlisting**:
  - **Allowlist.** Each verifier release compiles in the SHA-256 of exactly one trust configuration, alongside the
    frozen spec catalog (G12). The config file itself carries no signature.
  - **Release authentication.** Each release (verifier binary or source archive, with its compiled config hash and
    catalog) is signed by the **release key**. The release key is usable by neither the DNS credential, the
    repository key (YubiKey 2) nor the issuing AWS account, nor by any service those credentials can invoke. The dated
    custody record names the key and its access boundary.
  - **Bootstrap.** The first release's signature is verified against the release public key, which is published
    with the verifier's documentation and in the relying-party text; its fingerprint is recorded in the freeze
    record. How a relying party first obtains it authentically is part of distribution and inside the stated boundary.
  - **Rotation.** A new release key is introduced only by a release signed by the current release key. Custody and
    rotation procedure are **OPEN** (see §K and the runbook).
  - **Version and genesis.** The config's `version` starts at `"1"` and increases by exactly 1. `previous_sha256` of
    version 1 is 64 `0` characters; otherwise it is the SHA-256 of the prior approved config.
  - **Invalid config.** A config whose SHA-256 is not the compiled hash, or that fails its schema, makes the verifier
    refuse to run with exit error `TRUST_CONFIG_UNAUTHENTICATED`. That is **no verdict**, never a V1 verdict
    computed on unauthenticated trust.
  - **Report.** Every report carries the config's `version` and SHA-256 as diagnostics (not stable fields). The
    config hash is archived as a declared verification input; reproducing a verdict exactly (A9.4) uses the release
    that compiled that hash.
- **Config file (F11 table).** One RFC 8785 JSON object with no numbers; every key required:

  | Key | Type and grammar | Invariants |
  |---|---|---|
  | `format` | `"tessera-v1-trust/1"` | |
  | `profile` | `"tessera-v1-strict"` | |
  | `version` | decimal string ≥ 1 | prior + 1 |
  | `previous_sha256` | 64 lowercase hex | genesis zeros; else prior config hash |
  | `as_of` | RFC 3339 `YYYY-MM-DDTHH:MM:SSZ` | nondecreasing across versions |
  | `issuer_domain` | `"wamason.com"` | equals profile D |
  | `header_pins` | object height-string → 64 lowercase hex (display order) | nonempty; one hash per height; existing pins immutable |
  | `root_ksks` | array of G22 entries, sorted by (`signing_start`, `key_tag`) | unique `dnskey_rdata` |
  | `repository_keys` | array of objects `{"domain","key","signing_end","signing_start","sources"}` | `domain` = D; `key` base64 v4 P-256 public-key body; times RFC 3339, `signing_end` nullable; `signing_start ≤ signing_end`; unique `key` |

  `sources`, here and in G22, is an array of objects `{"description","sha256","uri"}` (strings; `sha256` 64 lowercase
  hex of the archived source file).
- **Residual and boundary.** Compromise of the release key is distribution compromise. A9 now names it as a
  boundary ("compromise of the verifier's distribution, meaning its release and the trust configuration compiled
  into it"). Generating a third token is not by itself evidence of independence; the custody record must show the
  boundary.
- **Required test.** A captured repository signer (YubiKey 2, or the repository host credential) tries to authorize a
  config: it signs a config adding its own root KSK, repository key and pins. The verifier must refuse it
  (`TRUST_CONFIG_UNAUTHENTICATED`). The same for a captured DNS credential and the issuing AWS account.
- **Label.** New trust-distribution design plus an explicit assumption, not CLARIFY. With genuinely independent
  authorization it repairs an underspecified trust input and needs no protection concession. If independence cannot
  be supplied, a NARROW-MODEL excluding that capture path goes to the author (§K).

### G09: open intervals and closing them — OWNER CHOICE (endpoint convention)

- **Resolution.**
  - `signing_end: null` means "still signing as of `as_of`". The **finite reliance of an open KSK is
    [`signing_start`, `as_of`]**, stated as reliance policy; an open repository key is usable on
    [`signing_start`, `as_of`].
  - Evidence time t > `as_of` under an open entry, with no other usable entry, gives `UNVERIFIABLE / TRUST_HORIZON`.
    A later config can cover it.
- **Release invariants (F12), checked by the release checker before the release key signs:**
  1. Identity, key bytes, D, `signing_start` and L of every existing entry are immutable.
  2. `as_of` is nondecreasing; `version` increases by exactly 1; `previous_sha256` binds the prior approved config.
  3. Finalized ends are immutable. A transition `null → end` is allowed only if the resulting reliance end
     (`signing_end + L` for a KSK, `signing_end` for a repository key) is ≥ the **previous** config's `as_of`.
  4. Pins are unique per height and canonical; existing pin hashes are immutable; pins are only added.
  5. No entry is removed.
- **What this preserves, and what it does not.** With immutable entries and nondecreasing `as_of`, eligibility
  previously granted through `as_of` is preserved. Appending pins can make an earlier attestation in the same proof
  qualify and so change T, or even turn `VALID_STRICT` into `INVALID` (initially only h2 qualifies, inside c1; later
  coverage of h1 < h2 selects T1 before declared − ε). This does not violate A9.4's exact-output contract for
  identical declared inputs, because the config is a declared input and changed. It does refute any stronger claim
  that append-only updates preserve all verdicts. **No monotonic-verdict promise is made.**
- **Residual, stated.** If a release leaves a KSK open past its real retirement, receipts in that gap stay
  acceptable. Retired-KSK manufacture during the adopted L extension is A9's acknowledged residual. An inadvertently
  longer horizon is a release failure, not permission to claim the exposure is bounded by the real retirement date.
  Release discipline: close before `as_of` passes the announced end.
- **Rejected.** Open meaning unbounded: it accepts stolen-retired-key evidence indefinitely. Open meaning unusable:
  it falsely rejects every current receipt, because KSK-2024's end is unknown.

### G22: root KSK material — OWNER CHOICE (trust serialization and acquisition)

- **Resolution.** Each `root_ksks` entry has these fields (all strings unless marked):

  | Field | Type | Invariant |
  |---|---|---|
  | `name` | string, e.g. `"KSK-2017"` | unique |
  | `key_tag` | decimal string 0–65535 | equals RFC 4034 App. B tag of `dnskey_rdata` |
  | `algorithm` | decimal string | equals the RDATA algorithm octet; in G16's set |
  | `dnskey_rdata` | base64 of RFC 4034 §2.2 RDATA | flags 257 (Zone Key, SEP; REVOKE clear), protocol 3 |
  | `ds_sha256` | 64 lowercase hex | equals SHA-256 over root owner wire `00` ‖ RDATA |
  | `signing_start`, `signing_end` | RFC 3339; `signing_end` nullable | start ≤ end |
  | `reliance_lifetime_s` (L) | decimal string | immutable |
  | `publication`, `revocation` | RFC 3339 or null | informational only (A9.5) |
  | `sources` | array, as in G08 | nonempty |

  - **Source (F13).** RFC 9718's `publickeyinfo` is optional, so an XML archive can lack the key bytes. The publisher
    therefore uses an **archived authenticated source containing each full public key**, or obtains the key from an
    archived root DNSKEY RRset and cross-checks its DS digest against independently authenticated IANA material
    (`root-anchors.xml` with its `.p7s`, verified against the ICANN CA by a recorded bootstrap procedure). Source file
    digests go in `sources`.
  - **Matching.** A presented root DNSKEY RR is trusted only if its RDATA is **byte-equal** to some entry's
    `dnskey_rdata`; the DS digest is a cross-check. Byte equality excludes the RDATA **when the presented RDATA has
    the REVOKE bit set**; the reliance period, not revocation, supplies temporal exclusion (A9.5). An archived
    flags-257 RR is not rejected merely because evaluation happens after revocation.
  - **Values.** Exact RDATA and complete intervals (starts, ends, L) are recorded in the actual pre-freeze config.
    Proposed starts, to be confirmed against archived sources at freeze: KSK-2017 `signing_start`
    2018-10-11T00:00:00Z (the 2018 root KSK rollover); KSK-2024 `signing_start` 2026-10-11T00:00:00Z. Ends and L as
    in P §5.
- **Rationale.** A name or key tag is not a trust anchor. Carrying the full key makes the config self-contained for
  2106 and avoids depending on DS matching alone.
- **Rejected.** DS digest only: a 2106 reader then needs the key bytes from elsewhere.

---

## D. Authority binding: G01, G02, G10, G34, G24

### G01: required binding forms — OWNER CHOICE (required-set selection)

- **Resolution.**
  - The V1 required set, fixed by the verifier (A9 C4, P §6.4), is **{direct-form evidence on the DNS channel,
    direct-form evidence on the git channel}**. In each channel the "statement" is the E§7 canonical value.
  - The signed `common.binding_forms` must equal `["STMT_DIRECT"]`. Element by element, in canonical order:
    `STMT_DIRECT` is accepted; `STMT_DIGEST` gives `UNVERIFIABLE / BINDING_FORM_UNSUPPORTED`; any other id gives
    `UNVERIFIABLE / BINDING_FORM_UNKNOWN`. The reported reason is that of the **first offending element** in
    canonical order. Since the array is nonempty, sorted and unique, these rules are equivalent to exact equality.
- **Label.** A new owner selection within A9's delegated fixed set, not an extraction of the illustrative vector
  value. No amendment; no codec or golden change; new policy cases (§L).
- **Rationale.** R-3.37 (author-ADOPTED) says the envelope carries a signed required set that must validate; A9 says
  the verifier fixes the set. Equality satisfies both (P §13 disagreement 1). Classes and codes are SPEC:1945. Both
  channels publish the fingerprints directly (R-4.30). The spike uses `STMT_DIGEST` and is not conforming V1 evidence.
- **Note.** E§8's "single in-profile `UNVERIFIABLE`" covers P8's codec only; reword it "the single codec-level
  UNVERIFIABLE" (pending, E).
- **Rejected.** Ignoring the signed field. `INVALID` for unknown forms (contradicts the author-ADOPTED class).

### G02: the git assertion's time relation — CORRECT + OWNER CHOICE + BROADEN (A9 C4)

- **Resolution.** Let T_git and h_git be the git proof's T and selected height (section B rule), and h_receipt the
  receipt proof's selected height. The git assertion must satisfy all of:
  - T_git lies in some configured repository-key interval for D (A9.5);
  - ~~T_git ≤ `declared_issue_time`~~ *(dropped by owner 2026-10-14: chain order carries the protection; the clock check stops no attack chain order misses and adds an nTime false-reject hazard on the honest path)*;
  - **chain-order pre-commitment: `h_git + 5 < h_receipt`**, else `INVALID / GIT_NOT_PRECOMMITTED`;
  - no upper bound from δ, since the assertion is long-lived.
- **CORRECT text (current, V1-PROFILE §6.3)** [OWNER 2026-10-14, r2-F16]. "The same window value is authenticated
  by the anchored git assertion and by DNSSEC at the snapshot's own anchored time. No clock comparison between T_git
  and the declared issue time is made. Before honest issuance the issuer obtains and validates the git assertion's
  k=6 proof. The chain-order rule establishes that the window was confirmed at k = 6 in the chain before the receipt
  was anchored; pre-commitment is chain order, not UTC (A2.1), and DNSSEC evidence establishes no publication before
  issue." *Dated correction 2026-10-14 (r2-F16): the F01 CORRECT text previously quoted here read "… The verifier
  requires T_git <= declared_issue_time. This is a chain-time comparison with a signed declaration; it does not
  establish UTC ordering or that the git assertion predates the receipt anchor. …"; its clock sentence is withdrawn
  with the owner's removal of that check.* The chain-order rule above is what establishes that the git assertion was confirmed at depth 6 before the
  receipt's anchor block; A9 C4 now registers it as **chain-order pre-commitment** (OWNER DECISION 2026-10-14,
  BROADEN), expressly retaining A2.1's UTC limitation: pre-commitment is chain order, not UTC.
- **E§7.1 wording (CORRECT, pending in E).** "The window is therefore fixed in DNSSEC-authenticated and anchored
  authority evidence before any receipt that relies on it" overstates both channels. DNSSEC at T_snap does not
  establish publication before issue, and chronology comes only from the chain-order rule. Replace with the current
  CORRECT text above plus a pointer to the chain-order rule. [OWNER 2026-10-14, r2-F16] *(Dated correction
  2026-10-14: previously "…and the numeric T_git comparison does not establish chronology. Replace with the F01
  CORRECT text above…"; there is no longer a numeric T_git comparison.)* *Withdrawn draft text (2026-10-13), quoted as a
  dated correction:* "…fixed in the anchored git assertion before the receipt's declared issue time (V1-PROFILE §6.3),
  and confirmed by DNSSEC at the snapshot's own time." That replacement transferred the unsupported chronology claim
  from DNS to git.
- **Withdrawn rationale (2026-10-14).** The draft called `T_git ≤ declared` "the stricter (fail-closed) choice" than
  `T_git ≤ T`. That is wrong for T < declared: the two rules are incomparable over A9's domain. Codex's
  counterexample: an honest receipt declares 12:00 and anchors at height h with nTime 11:55; an assertion
  manufactured later anchors at j > h with nTime 11:59. Every proposed temporal comparison passed. The chain-order
  rule rejects it (j + 5 ≥ h).
- **Issuer duty (runbook).** Do not issue in a window until the key-assertion commit's stamp has k = 6
  confirmations and the receipt will anchor at a higher height. Because the receipt is stamped after the issuer has
  observed h_git + 5, its anchor block is at a height above h_git + 5, so the honest wait-first path passes the
  chain-order rule. "Ships complete" alone would not imply wait-before-sign. No clock comparison between T_git and
  `declared_issue_time` is checked or waited for (runbook §5). [OWNER 2026-10-14, r2-F16] *(Dated correction
  2026-10-14: this paragraph previously added "Block nTime can run ahead of UTC, so the issuer also checks
  `T_git ≤ declared_issue_time` explicitly and waits if it does not hold."; withdrawn with the verifier check.)*
- **Rejected.** Evidence time only. `T_git ≤ T` alone. `T_git ≤ issuance-not-before`: ties the verifier to a UTC
  margin; kept as issuer practice.

### G10: M5, the manifest tuple equals the authority tuple — CLARIFY

- **Resolution.** Statement M5, to be written into P §6.4:
  > The manifest tuple (`alg`, `issuer`, `key_fp`, `sset`, `ver`) is fully determined by authenticated sources.
  > - `key_fp` and `sset[0]` equal the DNS value's `kms`/`gpg` (prefix-adjusted, E§3.3), and the git blob is
  >   byte-equal to that DNS value.
  > - `issuer` equals the DNS owner name's suffix and the pinned D (G34).
  > - `alg` equals the frozen catalog's single registered id (G12), and `ver` = `map-v1` (schema).
  >
  > No tuple field is free of either channel authentication or a single-valued profile constant. The constants are
  > policy-authenticated by the verifier's frozen catalog; they are not channel-signed tuple fields.

  Mismatches give `INVALID`: `DNS_KEY_MISMATCH`, `CHANNEL_VALUE_MISMATCH`, `ISSUER_NOT_PINNED`, or the codec's
  `SCHEMA`.
- **Rationale.** The 255-byte TXT value is full (E§7). No amendment, layout or vector change.

### G34: one pinned-D gate — CLARIFY + early failure classification

- **Resolution.** Before either channel: `common.issuer` must be exactly `wamason.com`, the profile constant D,
  which must also equal the trust config's `issuer_domain`. Otherwise `INVALID / ISSUER_NOT_PINNED`.
- **M2 text** (P §6.4): "For both channels the authority evidence is for D = `common.issuer` = `wamason.com`. On
  DNS, the validated TXT owner equals `_tessera-v1.<D>` label by label, ignoring ASCII case. On git, the commit
  verifies under a repository entry whose domain is D."
- **Rationale.** D is an AUTHOR DECISION (Q5). No later configuration can make another D valid, so `INVALID` is
  stable. With git evidence absent and another D, the result is now `INVALID`, not `UNVERIFIABLE`. This claims no
  extra model protection: the mandatory git gate already blocked complete alternate-D strict acceptance.

### G24: DNS record failures — CLARIFY + completeness exception

- **Resolution.**
  - A TXT RRset that is present is run through E§7's fifteen-step order. Every failure is `INVALID` with E's code,
    **whether or not DNSSEC was performable**.
  - An absent TXT group gives `UNVERIFIABLE / DNS_EVIDENCE_MISSING` (G19 completeness rule).
  - E's `DNS_RRSET` "zero" case stays a codec vector. It cannot be reached from a V1 container; no P8 vector changes.
- **Rationale.** R-2.31, and E§8.

---

## E. DNSSEC validation: G16, G27 (G35 in §J)

### G16: DNSSEC algorithm and validation profile — NARROW-CLAIM (visible owner scope choice)

- **Root rule first (F05 text).** "The root RRset passes only under A9.5: a byte-matching configured KSK, usable in
  its reliance interval at T_snap, verifies a selected RRSIG valid at T_snap. G16 never replaces that eligibility
  condition. Candidate aggregation is existential and order-independent; extra candidates are informational after
  any eligible supported path passes." Root outcomes and their precedence are P §5's (valid; then
  `KSK_OUTSIDE_RELIANCE_PERIOD`; then `RRSIG_NOT_VALID_AT_EVAL_TIME`; then `TRUSTED_KSK_SIGNATURE_INVALID`; else
  `UNVERIFIABLE / NO_TRUSTED_KSK_USABLE`).
- **Supported set (owner scope choice).** DNSKEY and RRSIG algorithms 8 (RSA/SHA-256, RFC 5702, key per RFC 3110)
  and 13 (ECDSA P-256/SHA-256, RFC 6605). DS digest types **2 (SHA-256, RFC 4509) and 4 (SHA-384, RFC 6605)**. The
  DNSKEY used must have the Zone Key flag set and the REVOKE flag clear (RFC 5011 §2.1), protocol 3.
- **Validation.** RFC 4035 §5.3.1–5.3.3 at T_snap, with canonical form per RFC 4034 §6.
- **Witnesses per RRset.** Each DS RRset is signed by a key in the parent's validated DNSKEY set. Each child DNSKEY
  RRset is self-signed by a key that matches a validated DS. The TXT is signed by a key in the zone's validated
  DNSKEY set.
- **Outcomes for a non-root required RRset**, computed once after every candidate has been tried:

  | Condition | Result |
  |---|---|
  | Some supported path (matching authenticated DS → DNSKEY → RRSIG, all supported) validates at T_snap | pass; other candidates informational |
  | Else, the RRset or every witness RRSIG it needs is missing | `UNVERIFIABLE / DNS_EVIDENCE_MISSING` |
  | Else, an unsupported algorithm or digest type could supply the required path | `UNVERIFIABLE / DNSSEC_ALGORITHM_UNSUPPORTED` |
  | Else (every relevant possibility is supported and checked), some candidate verifies cryptographically but its window excludes T_snap | `INVALID / RRSIG_NOT_VALID_AT_EVAL_TIME` |
  | Else, some supported candidate fails cryptographically | `INVALID / DNSSEC_SIGNATURE_INVALID` |
  | Else (no child DNSKEY matches a validated DS) | `INVALID / DNSKEY_DS_MISMATCH` |

  So a DS RRset holding only an unsupported digest type gives `UNVERIFIABLE`; a supported nonmatching DS plus an
  unsupported DS that might match gives `UNVERIFIABLE`; only when every possibility is supported and none matches is
  the result `INVALID / DNSKEY_DS_MISMATCH`. An unrelated invalid or unsupported candidate never defeats a supported
  validating path.
- **Rationale.** The live chain is root and `com` at algorithm 8, wamason.com at 13, and DS type 2 at both
  delegations (SPIKE-REPORT). RFC 4035 would treat an unsupported algorithm as insecure; V1 must never let that pass.
  **Withdrawn (2026-10-14):** the draft's narrowing of DS digest types to {2} is reversed. Dropping type 4 had no
  security benefit under A9's cryptographic assumptions and could reject honest future chains.
- **Visible limit.** A chain that moves to an algorithm outside {8, 13} (for example a TLD or root move to Ed25519,
  algorithm 15) makes new snapshots `UNVERIFIABLE` under this frozen spec. *Withdrawn example (2026-10-14):* "a root
  move to ECDSA" was wrong, since algorithm 13 is already supported; a new unlisted KSK is a separate trust-coverage
  problem. **Issue-time duty:** the issuer validates the snapshot under this profile and does not ship a receipt that
  would be unsupported (fail before ship). This must appear in P §6.1 and the relying-party text. "Honest-safe today"
  is an observation, not a freeze guarantee.
- **Rejected.** Accept "whatever the validator library supports": that is GAPS's fork exactly.

### G27: DNSSEC time arithmetic — CLARIFY + OWNER CHOICE (edge outcomes)

- **Resolution.** RRSIG inception and expiration are 32-bit values v. Each is resolved to the unique absolute
  second t with t ≡ v (mod 2^32) and |t − T_snap| < 2^31, per RFC 4034 §3.1.5 and RFC 1982 (external serial
  arithmetic). RFC 1982 leaves the half-range case undefined, so V1 fixes the edges:
  - if v − T_snap ≡ 2^31 (mod 2^32), the candidate fails with `RRSIG_TIME_AMBIGUOUS`;
  - if resolved inception > resolved expiration, the candidate fails with `RRSIG_INTERVAL_REVERSED`;
  - inception = expiration is allowed; the window is that one second.
  These are candidate failures under the existential rule (informational if another candidate passes; otherwise
  reported as `INVALID` with that reason, at the position of `RRSIG_NOT_VALID_AT_EVAL_TIME` in G16's precedence).
  The witness check is inception ≤ T_snap ≤ expiration. The evaluation time is always T_snap, never "now", including
  in 2106.
- **Withdrawn (2026-10-14).** "T_snap is a uint32 nTime, so the resolution is exact for every V1 receipt": the
  half-range edge exists regardless.

---

## F. Git: G25 — OWNER CHOICE (supported-path limit: git subset) + BROADEN (SHA-1DC)

- **Resolution, the closed grammar.**
  - **Commit object** (raw body, without the `commit <len>\0` prefix):
    `tree <40 lhex>LF`, then `(parent <40 lhex>LF)*`, then `author <bytes>LF`, `committer <bytes>LF`, then exactly
    one `gpgsig <line>LF` followed by `( <line>LF)*` continuations, then `LF`, then the message.
    - Repeated `parent` headers with **distinct** ids are allowed (merge commits). A repeated identical parent id is
      `INVALID / GIT_COMMIT_FORMAT`.
    - The author and committer lines are not interpreted.
    - Any other header (`encoding`, `mergetag`, `gpgsig-sha256`, unknown), a second `tree`, `author`, `committer`
      or `gpgsig` gives `INVALID / GIT_COMMIT_FORMAT`.
    - The signed payload is the commit with the `gpgsig` line and its continuation lines removed
      (gitformat-signature(5)).
  - **Signature value** (continuations joined by LF, each with its one leading space stripped), exactly:
    `-----BEGIN PGP SIGNATURE-----` LF, one empty line, one or more base64 lines of 1–76 characters from the RFC 4648
    alphabet (with `=` padding only at the end of the last line), an optional CRC line `=` followed by 4 base64
    characters, then `-----END PGP SIGNATURE-----`, with no trailing LF inside the value. **No armor headers**, no
    other blank lines, no whitespace inside lines. The CRC-24, if present, must match. The dearmored bytes must satisfy
    rule O's grammar exactly (E§5.2) and rule O's policy (G11), with type 0x00. Otherwise `INVALID / GIT_SIG_FORMAT`.
  - **Trees.** Entries are `mode SP name NUL id20`. Modes come from {40000, 100644, 100755, 120000, 160000}, with no
    leading zero. Names are nonempty, without `/` or NUL, and not `.` or `..`. Entries are strictly sorted in git
    order (trees compare as `name/`) with no duplicate names, and the body is consumed exactly. Otherwise
    `INVALID / GIT_TREE_FORMAT`.
  - **Path** (P §6.3): root entry `tessera-v1` with mode 40000, then `key-assertion` with mode 100644, giving the
    blob. `git.trees` holds exactly [root, sub]. Violations give `INVALID / GIT_PATH`.
  - **Ids.** SHA-1 of `"<type> <len>\0" ‖ body`, computed **with collision detection** (SHA-1DC, as git since
    2.13). A detection gives `INVALID / GIT_SHA1_COLLISION`.
  - **Repository key.** A v4 public-key body in `repository_keys`, **ECDSA P-256** (rule O).
    - If some entry for D verifies the signature: when its interval contains T_git the check passes; otherwise
      `INVALID / GIT_SIGNER_OUTSIDE_INTERVAL`.
    - If no entry for D verifies it: `UNVERIFIABLE / GIT_SIGNER_NOT_CONFIGURED`.
  - **Stamp.** The git proof's file digest equals SHA256 of the 40 lowercase hex characters plus LF (A9.5),
    otherwise `INVALID / GIT_STAMP_MISMATCH`. `object_format` as in A9.5 and G14.
  - **Not checked.** That this commit *introduced* the blob.
- **Label.** A new git subset, a P-256 owner choice and the SHA-1DC defense; not all CLARIFY. Merges, armor headers
  and other root algorithms may be rejected; that limit is visible.
- **OPEN, owner act.** The deployed repository-root algorithm is not yet demonstrated: YubiKey 2 is not in hand.
  Confirm P-256 before the freeze; if another algorithm is used, list that one instead and add it to G15.
- **Rejected.** Shelling out to git or gpg. Accepting the `encoding` header.

---

## G. Signatures, algorithms, specification: G11, G12, G13, G28

### G11: rule-O signature policy — OWNER CHOICE (supported-path limit: signature profile)

- **Withdrawn (2026-10-14).** The draft's blanket ban on critical bits in either subpacket area, and its rationale
  ("A standards validator would reject such a signature"), are withdrawn. RFC 9580 distinguishes **unknown** critical
  subpackets from recognized ones and recommends marking creation time critical; a blanket ban rejects ordinary
  conforming signatures. Codex executed the counterexample: SIG-01 with the critical bit on its unhashed key-ID
  subpacket passes codec A and verifies mathematically.
- **Resolution (F07, adopted as proposed).** For every rule-O signature (attestation, possession, git):
  - **Codec.** E§5.2's grammar holds.
  - **Hashed area.**
    - exactly **one** signature-creation-time subpacket (type 2) with exactly **four data octets**, critical or not.
      It is never compared with anything (no wall-clock check);
    - **no** signature-expiration subpacket (type 3), critical or not. Never wall-clock expiry;
    - issuer key ID (16) and issuer fingerprint (33) are recognized, accepted critical or not, and never read (no
      SHA-1 key binding, D-6);
    - any other subpacket type: ignored if not critical; if critical, it is an unknown critical subpacket and the
      signature fails.
  - **Unhashed area.** Ignored entirely, critical bits included, consistent with E§3.5 (the unhashed area carries no
    meaning).
  - **ECDSA.** FIPS 186-5 with r, s ∈ [1, n−1]. Low-s is not required.
  - **Codes.** A policy failure gives `INVALID / SIG_POLICY`. A failed verification gives `SIG_INVALID`, or
    `POSSESSION_INVALID` for the manifest possession signatures.
  - **Possession proofs** use the same per-slot rule over `F_manifest` (rule R for kms under the hybrid). No
    revocation or current-time checks.
- **Issuer constraint.** The issuer adapters must emit signatures in this profile before signing and stamping.
- **Evidence.** The real GnuPG 2.4.4 signature in the spike has hashed subpackets {33, 2}, neither critical, and
  unhashed {16}. SIG-01/SIG-02 have the same shape and need not change. Signature-profile acceptance and rejection
  vectors are added separately from P8 codec vectors (§L); codec expectations are not changed to impose this policy.

### G12: algorithm policy — OWNER CHOICE (frozen policy selection)

- **Resolution.**
  - The verifier compiles in a **frozen spec catalog** with one V1 entry:

    | Field | Content |
    |---|---|
    | `spec_id`, `spec_sha256`, `vectors_sha256`, `preamble_sha256`, `dependency_manifest_sha256` | the frozen objects |
    | `alg` | exactly one id: `OPENPGP4-ECDSA-P256-SHA256` under the fallback, or the registered pair id under the hybrid |
    | `alg_prohibited` | `[]` |
    | `binding_forms` | `["STMT_DIRECT"]` |
    | `D`, δ, ε, k | profile constants |
    | DNSSEC sets | algorithms {8, 13}, DS digest types {2, 4} |
  - **Outcomes for `common.alg`.** Malformed gives `INVALID` (codec). Well-formed but not the catalog's id gives
    `UNVERIFIABLE / ALG_UNKNOWN`; that includes the id of the branch not taken.
  - The catalog is independent of bundle content and of trust-config updates. Future verifiers preserve this original
    policy for V1 bundles (A9.4, A9.7 row 29).
- **Rationale.** A9.4 requires the algorithm policy registered for the governing V1 spec, including its prohibited
  cases; writing the prohibited set as empty makes it defined. The A9.6 hybrid supplement is still required if the
  hybrid is taken; no extra amendment.

### G13: binding the specification and its objects — OWNER CHOICE (packaging)

- **Resolution.**
  - **Spec checks.** `common.spec.id` ≠ `tessera-v1-strict/verification-spec/1` gives `INVALID / SPEC_ID`. A
    `common.spec.sha256` not in the catalog gives `UNVERIFIABLE / SPEC_UNKNOWN`.
  - **Object checks.** `vectors_sha256` and `preamble_sha256` must equal the catalog entry's values, else
    `INVALID / SPEC_OBJECT_MISMATCH`. The bundled `spec`, `vectors`, `preamble` and `dependency_manifest` bytes
    must hash to their signed or catalog values, else `INVALID / BUNDLE_OBJECT_HASH`. They are never parsed as
    policy or executed. Their role is C6 readability.
  - **Assembly format.** The spec object and the vectors object each consist of one or more **parts**. A part is the
    ASCII line `tessera-v1-part <path> <length>` LF, followed by exactly `<length>` bytes (decimal, no leading zeros),
    followed by LF. `<path>` is the repository-relative path, UTF-8, no spaces. Parts are in bytewise-sorted path
    order. File bytes are included verbatim (UTF-8, LF line endings as committed). The spec object holds the frozen
    `docs/V1-PROFILE.md` and `formal/p8/ENCODING-V1.md`, plus the branch-registration supplement if the hybrid is
    taken. The vectors object holds every file under `formal/p8/vectors/` and the non-P8 conformance vectors (§L).
  - **Baseline.** A9 incorporates ENCODING-V1 **at its signing commit**. Freezing an edited E into the spec object is a
    change to the governing baseline; it is permitted only with authorized change accounting (A9's signing baseline
    plus the authorized hybrid supplement), never by silently substituting edited text.
  - The vectors may embed the spec hash; the spec never embeds the vectors' hash (no cycle).
- **Rationale.** A9.4: "always evaluated under its signed `common.spec`". The verifier holds that spec independently.
  Signed spec and vector hashes change on freeze assembly; the frame layout does not.
- **Rejected.** "Hash matches the bundled bytes" alone: a self-consistent alternative spec would pass.

### G28: OpenPGP subpacket lengths — CLARIFY

- **Resolution.** RFC 9580 §5.2.3.7:
  - first octet < 192: a one-octet length;
  - first octet 192–254: a two-octet length `((o1−192)<<8)+o2+192`, covering 192–16319;
  - first octet 255: a four-octet length.

  The length counts the type octet and must be ≥ 1. **V1 accepts only the shortest form** (E's existing rule): a
  longer-than-needed form gives `SIG_FORMAT`. This is a V1 rule; RFC 9580 does not ban all longer forms. Under rule
  O's 1024-byte cap the five-octet form never occurs. Add 191/192 boundary vectors if absent.
- **Rationale.** This is exactly codec B's `subpackets_ok`. Existing P8 vectors need not change.

---

## H. Dependencies, runtime, field grammars: G15, G29, G18

### G15: the dependency manifest — BROADEN

- **Resolution.** A closed JCS file, top level exactly `{"entries":[…],"format":"tessera-v1-deps/1"}`. `entries` is
  sorted by `id` and unique. Each entry is an object with these keys, all required:

  | Key | Type | Content |
  |---|---|---|
  | `id` | string `[a-z0-9-]+` | stable identifier |
  | `title` | string | |
  | `edition` | string | exact edition (R-3.51) |
  | `sections` | nonempty array of strings | normative sections used |
  | `errata` | string | errata disposition |
  | `digest_sha256` | 64 lowercase hex, or null where no canonical bytes exist | stable digest |
  | `retrieval` | string | retrieval identifier |
  | `redistribution` | string | redistribution status |
  | `failure_consequence` | string | |

  - **Entries.** A9's eight, plus everything the profile now relies on:

    | Area | Standards |
    |---|---|
    | E | RFC 8785; Unicode 16.0.0 UCD with its file digests; UAX #15 (NFC); RFC 8259; RFC 3339; RFC 9580; ECMA-262 Number::toString (pinned edition) |
    | Hashes, signatures | FIPS 180-4 (SHA-256, SHA-384, SHA-1); FIPS 186-5 (ECDSA P-256); RFC 6979 not required |
    | Container | RFC 4648 |
    | DNSSEC | RFC 1035, 1982, 2181, 3110, 4034, 4035, 4509, 5011, 5702, 6605, 9718; RFC 9102 (chain shape, informative) |
    | Trust sources | RFC 5652 (CMS, for the `.p7s` source authentication) |
    | OTS | the DetachedTimestampFile format (G20) |
    | Bitcoin | block header format, double SHA-256, merkle tree, non-witness transaction serialization |
    | Git | gitformat-signature(5), the git object format, SHA-1DC |
    | Hybrid only | FIPS 204 (ML-DSA-65) and the supplement's SPKI encoding |
  - **Checks.** A hash mismatch with the catalog gives `INVALID / BUNDLE_OBJECT_HASH`; an absent manifest gives
    `UNVERIFIABLE / MEMBER_MISSING`. Its contents are not interpreted by the verifier.
- **Rationale.** P §9 OPEN items, R-7.7 closure, A9.5 custody. The list is fixed at freeze and bound by hash.

### G29: number formatting and Unicode runtime — CLARIFY

- **Resolution.**
  - **ES.** `ES(d)` is ECMA-262 Number::toString of a pinned edition; the edition, section and document digest are
    recorded in the dependency manifest. The full algorithm, reproduced: if d is +0 or −0, `"0"`. If d < 0,
    `"-"` ‖ ES(−d). (NaN and infinities never reach ES under A9.8.) Otherwise let n, k, s be integers with k ≥ 1,
    10^(k−1) ≤ s < 10^k, s × 10^(n−k) = d as a double, and k as small as possible. If several s qualify, choose the
    s for which s × 10^(n−k) is closest in value to d; if two are equally close, choose the even s. Then:
    - k ≤ n ≤ 21: the k digits of s followed by n−k zeros;
    - 0 < n ≤ 21: the first n digits, `.`, the remaining k−n digits;
    - −6 < n ≤ 0: `0.`, then −n zeros, then the digits;
    - otherwise exponent form: the first digit, then `.` and the remaining digits if k > 1, then `e`, then `+` or
      `-`, then abs(n−1) in decimal.
  - **Formatter conformance.** Any formatter must reproduce N-01…N-22 and C-N01…C-N22. Python's `repr` is not ES.
  - **Unicode.** The tables must be Unicode 16.0.0, identified by the UCD file digests in G15. A runtime may use
    bundled pinned tables even if the host's Unicode differs; a runtime whose tables do not match refuses to run (no
    verdict). No new number policy; A9.8 governs.

### G18: timestamps and LDH names — CLARIFY

- **Resolution.** `utc` years run 0001–9999 (proleptic Gregorian, seconds 00–59). Labels match `[a-z0-9-]{1,63}`
  with no leading or trailing hyphen, and all-numeric labels (top label included) are allowed; at least two labels;
  at most 241 bytes. This is exactly `check.py` `date_ok` and `is_domain`, and the same in `gen.py`.
- **Rationale.** It codifies what both codecs already do; existing vectors need not change. Add year and
  numeric-label codec boundary cases (§L). Under G34 the issuer case is reason-only.
- **Withdrawn (2026-10-14).** "Any declared time or window outside the uint32 nTime range fails a conjunct or the
  window rule": too broad. Near the maximum, declared = T + 1 can pass ε, and a future window endpoint can exceed the
  range.

---

## I. Aggregation and reasons: G26 (and G31, G32 in §J)

### G26: all-failure aggregation — CLARIFY (A9.4 stable-field contract)

- **Withdrawn (2026-10-14).** "A verifier may stop early only on a failed check." A failed check settles the verdict
  but not the stable reason or T; two schedules could report different stable fields (F06).
- **Resolution (F06 text).** "Physical evaluation order is unrestricted, but reporting uses the fixed total check
  order. Early termination is permitted only when every earlier-priority reportable check is settled and every
  stable field, including T, is determined. A failure prevents only checks whose own necessary input cannot be
  obtained; it does not suppress independent receipt-anchor evaluation needed for T. Derived checks are unperformable
  when necessary inputs cannot be obtained, and never pass by default."
  - **Input-independent checks**, which run whenever their bytes are present: the codecs; the time-free
    cryptographic validity of RRSIGs; DNS record grammar; git grammar and ids; manifest and key binding; the receipt
    OTS proof and its T.
  - **Checks that depend on time inputs:** RRSIG windows, KSK reliance and repository intervals (on T_snap or T_git);
    the conjuncts, the window rule and chain-order (on T and heights).
  - **The unknown `alg` case** routes the slot as opaque (Lemma 7a). Possession and signature semantics that cannot be
    interpreted under that `alg` are unperformable; independent schema and hash checks still run.
  - **Verdict:** any failed → `INVALID`; else any unperformable → `UNVERIFIABLE`; else `VALID_STRICT` (R-2.26).
  - **Reported reason:** the first failed check in G31's total order; if none failed, the first unperformable one.
- **Rationale.** Verdict and all six stable fields are then schedule-independent (SPEC R-5.16, A9.4). No amendment
  or P8 change.

---

## J. The non-verdict rows

| Gap | Resolution | Label | Lands |
|---|---|---|---|
| G30 | An empty snapshot body, or a payload over its cap, gives `LENGTH_CAP`, checked before the JSON categories. The size gate is exact and separate for the container (2^27), the payload (E§1) and S (2^24) | CLARIFY | P §3.2 |
| G31 | **Total check order** for the reported reason (below). Failed checks are ordered first; unperformable ones only matter if none failed. This matters because the reason code is one of A9.4's six stable fields | CLARIFY | P §3.2 |
| G32 | Report = JCS object `{"historical_security":"NOT_EVALUATED","reason","revocation":"NOT_EVALUATED","standing":"ABSENT/NOT_ISSUED_IN_PROFILE","T","verdict"}`, the stable-output object. Success reason `OK`. **T criterion:** T is the RFC 3339 string of nTime(h*) when the receipt proof parses, its file digest equals SHA256 of the presented `a_sig` bytes, no attestation in it is contradicted (`OTS_MERKLE_MISMATCH`), and it has a qualifying attestation; otherwise `null`. T is reported whatever the verdict; relying-party text must say a T on `INVALID` is not proof of a valid service receipt. Diagnostics (config version and hash, spec hash, per-check list) go in a separate wrapper object outside the stable six | CLARIFY | P §3.4 |
| G33 | `issuer_record` (R-3.46) is **optional unsigned diagnostics**: `{"observed_anchor_delay_s","policy_version"}`; `observed_anchor_delay_s` uses the decimal grammar (seconds, ≤ 2^32 − 1); `policy_version` matches `tessera-v1-issue-policy/(0|[1-9][0-9]*)`. Its absence never affects the verdict. If present, its schema is checked (`INVALID / CONTAINER_SCHEMA`); its values never alter verification parameters and are not authenticated issue observations. The honest issuer always emits it | OWNER CHOICE | P §2.1 |
| G35 | Witness order: the **first eligible validating** witness in (key tag, inception, expiration, signature bytes, canonical RRSIG RDATA, canonical key RDATA) order. For the root, reliance eligibility precedes selection. Extra failing candidates are informational | CLARIFY | P §7.3 |
| G36 | "Repository key = offline root" is an operating fact (runbook), not verifier policy. It is distinct from G08's release-key boundary | CLARIFY | P §5 |
| G37 | The baseline is the frozen spec object hash in the catalog (G13). Do not substitute a frozen edited E for A9's incorporated signing baseline without authorized change accounting | CLARIFY | P §1 |
| G38 | Delete the stale "needs an author sentence" remarks (E:147-148, D-1; PROOF §6 last bullet); A9.8 governs | CLARIFY/CORRECT (pending, E and R) | E, R wording |
| G39 | Re-extract P §6 from A9.5 and A9.6: SHA-1 descriptor, 40 hex + LF, repository intervals, per-receipt window. No verifier non-overlap check. Successor registration is an issuance duty, not a verifier check. Descriptor exceptions as in G14 | CLARIFY | P §6 |

**G31 total check order.** Within a stage, subchecks run in the order listed; per-slot checks in manifest slot
order; per-member and per-candidate checks in canonical (JCS key, then array index) order; per-height checks in
ascending height.
1. Dispatch D1–D4.
2. Container: canonical JCS; absent members (first absent path); `git.object_format`; schema of present members
   (first offending path).
3. `a_sig` codec (E order).
4. Manifest codec; `manifest_sha256`.
5. Keys, per slot: `KEY_FORMAT`, `KEY_MISMATCH`.
6. Receipt consistency (E§5.3: `ANCHOR_COUNT`, `RECEIPT_SLOT`, …).
7. `alg` (`ALG_UNKNOWN`).
8. Profile constants: `ISSUER_NOT_PINNED`; `SPEC_ID`; `SPEC_UNKNOWN`; `SPEC_OBJECT_MISMATCH`; binding forms (first
   offending element).
9. Signatures, per slot: `SIG_FORMAT`, `SIG_POLICY`, `SIG_INVALID`; then possession per slot.
10. Header pool, ascending height: `HEADER_CONFLICTS_PIN`, `HEADERS_NOT_COVERED`, `HEADER_CHAIN_BROKEN`.
11. Receipt OTS: `OTS_FORMAT`; `RECEIPT_ANCHOR_MISMATCH`; `OTS_MERKLE_MISMATCH`; `HEADERS_MISSING` /
    `ANCHOR_PENDING_ONLY`; `ANCHOR_TXID_MISMATCH`.
12. Conjuncts: c1, c2, c3.
13. Snapshot: envelope and `LENGTH_CAP`; body format (`SNAPSHOT_FORMAT`, `DNS_WILDCARD`); OTS (as stage 11, with
    `SNAPSHOT_STAMP_MISMATCH`, `SNAPSHOT_NOT_ANCHORED`); DNSSEC, root group then each zone top-down then TXT
    (G16/P §5 outcomes, `DNS_EVIDENCE_MISSING`); TXT record (E§7 fifteen-step order); `SNAPSHOT_TIME`.
14. Git: `GIT_COMMIT_FORMAT`; `GIT_SIG_FORMAT`; `GIT_TREE_FORMAT`; `GIT_SHA1_COLLISION`; `GIT_PATH`; OTS (as stage
    11, with `GIT_STAMP_MISMATCH`, `GIT_NOT_ANCHORED`); `GIT_SIGNER_NOT_CONFIGURED` / `GIT_SIGNER_OUTSIDE_INTERVAL`;
    ~~`GIT_ASSERTION_AFTER_ISSUE`~~; `GIT_NOT_PRECOMMITTED`. *(r2-F16, 2026-10-14: `GIT_ASSERTION_AFTER_ISSUE` is
    removed; it was the dropped clock check's code and is not a V1 reason. This list is itself superseded by
    V1-PROFILE §15.7's numbered check table, r2-F11.)*
15. Channel equality: `DNS_KEY_MISMATCH`, `CHANNEL_VALUE_MISMATCH`.
16. `ISSUANCE_WINDOW`.
17. Bundle-object hashes (`BUNDLE_OBJECT_HASH`).

---

## K. For the author and owner (change accounting)

**§K's 2026-10-13 statements withdrawn:** "Needs an amendment: none" and "No signed byte changes, and no P8 vector
changes." A9 incorporates an ENCODING-V1 signing baseline and registers C4/C5/C6 meanings and the `object_format`
outcomes; a later profile cannot override those by relabelling a change as wording.

**A9 text the owner changed on 2026-10-14** (A9 is PROPOSED, so these are edits to the instrument, applied in
`a9-gap-fixes.diff`): the claim sentence and C4 (chain-order pre-commitment, BROADEN, F01); C5 (lowest block height,
F03); C6 (selected-anchor referent, F02); A9.5 "Trust-configuration authority" and the distribution-compromise
boundary in "The boundaries" (F04).

**NARROW-MODEL:** none established. Conditional author surfaces:
- **G08.** If release-key custody cannot be made independent of the DNS credential, the repository key and the
  issuing AWS account, a channel credential could rewrite distributed trust; excluding that capture path is a
  NARROW-MODEL. Custody is OPEN (YubiKey 2 is not in hand; see the note to Tony).
- **G02.** Resolved by BROADEN (chain-order pre-commitment), not by weakening the claim. Pre-commitment remains chain
  order, not UTC (A2.1).
- Candidates the author should confirm are not concessions: **G09** (a release that leaves a retired KSK open keeps
  that gap acceptable); **G19** (ancestor-zone signing authority is inherited from DNSSEC).

**NARROW-CLAIM** (visible to relying parties): G16, the DNSSEC algorithm set {8, 13} (DS types {2, 4}); G19's
wildcard exclusion.

**OWNER CHOICE (supported-path limits)**, visible but not concessions of protection available in A9's model: G01,
G05, G06 (snapshot c3), G09, G11, G12, G13, G14, G17, G19, G20, G22, G25, G27 edges, G33.

**CORRECT:** E§7.1's "fixed in DNSSEC-authenticated … evidence before any receipt" and the draft's own replacement
for it (G02).

**Readings of A9 now registered or stated:** G03 lowest height (A9 C5); G05 selected anchor (A9 C6); G23 "outside the
pins" means an uncovered height (stated here and in P §7.2).

**Owner acts before 30 Oct that these resolutions create:**
1. **Release key and its custody record** (G08). OPEN: the key, its holder and its access boundary are not chosen.
2. Confirm YubiKey 2's algorithm is P-256 (G25). OPEN: the token is not in hand.
3. Assemble the spec object, vectors object and catalog (G13).
4. Re-capture and re-stamp the snapshot in the G19 body form.
5. Runbook: issue only after the key-assertion stamp has k = 6 and the receipt will anchor higher (G02). Done in
   `docs/V1-OPERATIONS-RUNBOOK.md` §5.
6. Write the conformance vectors in §L.
7. Produce the actual pre-freeze trust configuration with sourced KSK RDATA and intervals (G22).
8. Record the signer branch; if hybrid, the supplement fixes the `kms` SPKI (G21).

**Where these resolutions differ from the instruments** (the instruments need updating; they are not evidence for a
C-row):

| Area | Instrument | Resolution |
|---|---|---|
| Uncovered attestations (G05) | `UNPERFORMABLE` | ignored |
| Retarget boundary (G07) | `RETARGET_NOT_IMPLEMENTED` stop | dropped |
| Snapshot body (G19) | JSON of resolver messages | RR sequence |
| KSK trust anchor (G22) | DS digest only | full DNSKEY RDATA |
| δ, ε, k | in the trust config | catalog constants |
| Trust-config authentication (G08) | none | compiled hash in a signed release |
| Git tree checks (G25) | duplicate names only | full canonical-tree checks |
| LEB128 (G20) | redundant groups accepted (library 0.4.5) | shortest form only |
| Binding form (G01) | `STMT_DIGEST` in spike | `STMT_DIRECT` only |
| Container (G17) | indented JSON | canonical JCS |

**Riskiest:**
1. **G19 + G16:** a from-RFC DNSSEC validator is the largest new code surface before the freeze.
2. **G08:** release-key custody is open; without a demonstrated independent boundary the F04 attack stands.
3. **G02:** the chain-order rule is new verifier behaviour; its boundary vectors (h_git + 5 = h_receipt − 1 and
   = h_receipt) must exist before the freeze.

---

## L. Consolidated conformance cases

All are **non-P8** vectors unless marked; each names its expected verdict / reason. The A9.5 rollover control and the
`docs/reviews/v1-profile/` F1/F2 vectors (P §5) are included by reference as L-60 to L-62.

**Container and dispatch (G17, G14, G33, G39)**
- L-01 Non-JSON bytes → `UNVERIFIABLE / OUT_OF_PROFILE`. L-02 Over 2^27 bytes → same.
- L-03 `profile` absent or other → same. L-04 two layers (case c) → same. L-05 wrapper (case h) → same.
- L-06 Request `degraded` (case d1) → `OUT_OF_PROFILE` / `REQUEST_UNSUPPORTED`; same bytes strict → `VALID_STRICT`.
- L-07 Re-indented container → `INVALID / JSON_NONCANONICAL`.
- L-08 Unknown member → `INVALID / CONTAINER_SCHEMA`.
- L-09 `git` absent (case d2) → `UNVERIFIABLE / MEMBER_MISSING:git`. L-10 nested `git.ots` absent → `MEMBER_MISSING:git.ots`.
- L-11 `git.object_format` absent → `UNVERIFIABLE / GIT_OBJECT_FORMAT_MISSING`; L-12 `"sha256"` → `GIT_OBJECT_FORMAT`.
- L-13 Height `"01"` → `INVALID / CONTAINER_SCHEMA`; L-14 height 4294967296 → same.
- L-15 `issuer_record` absent → verdict unchanged; L-16 present, `policy_version` malformed → `INVALID / CONTAINER_SCHEMA`.
- L-17 Case d3 (one key, one channel) → `INVALID` dominating missing-channel `UNVERIFIABLE`.

**Binding forms and constants (G01, G12, G13, G34)**
- L-18 `["STMT_DIGEST"]` → `UNVERIFIABLE / BINDING_FORM_UNSUPPORTED`. L-19 `["STMT_OTHER"]` → `BINDING_FORM_UNKNOWN`.
- L-20 `["STMT_DIGEST","STMT_DIRECT"]` → `BINDING_FORM_UNSUPPORTED` (first offending element).
- L-21 Branch-not-taken `alg` → `UNVERIFIABLE / ALG_UNKNOWN`.
- L-22 Wrong `spec.id` → `INVALID / SPEC_ID`; L-23 unknown spec hash → `UNVERIFIABLE / SPEC_UNKNOWN`; L-24 vectors hash
  ≠ catalog → `INVALID / SPEC_OBJECT_MISMATCH`; L-25 bundled preamble bytes altered → `INVALID / BUNDLE_OBJECT_HASH`.
- L-26 `issuer` = other domain, git absent → `INVALID / ISSUER_NOT_PINNED`.

**Git time and chain order (G02)**
- ~~L-27 T_git = declared → passes the numeric check. L-28 T_git = declared + 1 → `INVALID / GIT_ASSERTION_AFTER_ISSUE`.~~
  *(Withdrawn 2026-10-14, r2-F16: they tested the dropped clock check.)* [OWNER 2026-10-14, r2-F16]
- L-27 (replacement, positive control) T_git > `declared_issue_time` (by at least one second) with `h_git + 5 <
  h_receipt`, T_git in a repository interval, and every other check satisfied → `VALID_STRICT`. L-28 (replacement,
  positive control) T_git > receipt T with `h_git + 5 < h_receipt`, T_git in a repository interval, and every other
  check satisfied → `VALID_STRICT`. Both must pass; no clock comparison is made.
- L-29 h_git + 5 = h_receipt − 1 → passes. L-30 h_git + 5 = h_receipt → `INVALID / GIT_NOT_PRECOMMITTED`.
- L-31 Codex F01 schedule: receipt at h, nTime 11:55, declared 12:00; git assertion at j > h, nTime 11:59 →
  `INVALID / GIT_NOT_PRECOMMITTED`.

**Time cluster (G03–G07, G23)**
- L-32 Nonmonotone two-branch at c1: h1 < h2, nTime(h1) = declared − ε − 1, nTime(h2) = declared − ε → `INVALID /
  TIME_BEFORE_DECLARED_EPSILON` (lowest height selected).
- L-33 Same at c2 boundary (declared + δ) → `INVALID / TIME_AFTER_DECLARED_DELTA`.
- L-34 Same at not-after: nTime(h1) = not-after + 1, nTime(h2) = not-after → `INVALID / ISSUANCE_WINDOW`.
- L-35 Two qualifying attestations at the same height → one T, same verdict as either alone.
- L-36 `confirmed_at` = declared + δ → passes; + 1 → `CONFIRMATION_LATE`. L-37 fifth successor inside, sixth outside
  δ → passes (inclusion + five). L-38 `confirmed_at` < T (nonmonotone) → passes.
- L-39 Qualifying branch plus an attestation at q with no headers → passes.
- L-40 Plus partial q headers (pinned inclusion, missing successors) → passes.
- L-41 Plus an unpinned header at q → `UNVERIFIABLE / HEADERS_NOT_COVERED`.
- L-42 Plus a contradicted q branch (pinned header, merkle ≠ message) → `INVALID / OTS_MERKLE_MISMATCH`.
- L-43 Pending-only proof → `UNVERIFIABLE / ANCHOR_PENDING_ONLY`.
- L-44 Genuine holder-upgraded proof containing the complete original witness, new branches without headers → passes.
- L-45 Missing intermediate height between supplied headers → not a broken link. L-46 adjacent pair with wrong prev →
  `INVALID / HEADER_CHAIN_BROKEN`.
- L-47 Supplied header at a pinned height, other hash → `INVALID / HEADER_CONFLICTS_PIN`.
- L-48 Segment crossing a 2016-block boundary → passes.
- L-49 Receipt passes c3, snapshot fails c3 → `INVALID / SNAPSHOT_TIME`.

**Trust configuration and release (G08, G09, G22)**
- L-50 Config hash not compiled into the release → refusal, `TRUST_CONFIG_UNAUTHENTICATED`, no verdict.
- L-51 Captured repository signer signs a config adding its own KSK, repository key and pins → refused (no verdict).
  L-52 Same for a captured DNS credential and for the issuing AWS account.
- L-53 Release checker: changing L of a closed KSK → rejected. L-54 closing an end below the previous `as_of` →
  rejected. L-55 `as_of` decreasing, pin hash changed, entry removed → each rejected.
- L-56 Pin append that makes an earlier attestation qualify and changes T → documented verdict change, not a checker
  failure.
- L-57 Evidence after `as_of` under an open entry → `UNVERIFIABLE / TRUST_HORIZON`.
- L-58 Presented root DNSKEY with REVOKE set → no matching trusted KSK. L-59 RDATA differing from config → same.
- L-60 to L-62 Rollover control; failing trusted candidate before a validating one, both trust-list orders; old root
  within reliance passes, after reliance does not (P §5).

**DNSSEC (G16, G19, G24, G27, G35)**
- L-63 Root signed by a trusted retired KSK, RRSIG window valid, T_snap outside reliance → `INVALID /
  KSK_OUTSIDE_RELIANCE_PERIOD`.
- L-64 Mixed DS types 2 and 4, one matching → passes. L-65 DS type 4 only, matching → passes.
- L-66 DS type 1 only → `UNVERIFIABLE / DNSSEC_ALGORITHM_UNSUPPORTED`. L-67 supported nonmatching DS plus unsupported
  DS → same. L-68 all supported, none matching → `INVALID / DNSKEY_DS_MISMATCH`.
- L-69 Supported valid RRSIG plus unsupported-algorithm RRSIG → passes. L-70 only an algorithm-15 RRSIG → `UNVERIFIABLE /
  DNSSEC_ALGORITHM_UNSUPPORTED`.
- L-71 RRset without its witness RRSIG → `UNVERIFIABLE / DNS_EVIDENCE_MISSING`; root DNSKEY without RRSIG →
  `NO_TRUSTED_KSK_USABLE`. L-72 sequence ending before TXT → `DNS_EVIDENCE_MISSING`.
- L-73 Truncated RR, forbidden type, duplicate RR, misordered group → `INVALID / SNAPSHOT_FORMAT` (one each).
- L-74 Uppercase name inside RDATA → `INVALID / SNAPSHOT_FORMAT`. L-75 wildcard TXT RRSIG → `INVALID / DNS_WILDCARD`.
- L-76 Present malformed TXT with DNSSEC unperformable → `INVALID` with E's code. L-77 empty body → `LENGTH_CAP`.
- L-78 Extra expired RRSIG beside a valid one → passes; selected witness per G35.
- L-79 RRSIG time exactly 2^31 from T_snap → `RRSIG_TIME_AMBIGUOUS`; L-80 inception > expiration →
  `RRSIG_INTERVAL_REVERSED`; L-81 inception = expiration = T_snap → passes; L-82 2106 rollover around T_snap.

**OTS encoding (G20)**
- L-83 txid ≠ path-derived → `INVALID / ANCHOR_TXID_MISMATCH`. L-84 Codex F09 proof (digest double-hashed into a
  commitment, then a real transaction) → `INVALID / ANCHOR_TXID_MISMATCH` (supported-path limit).
- L-85 SegWit-serialized transaction preimage → same. L-86 redundant LEB128 → `INVALID / OTS_FORMAT`. L-87 SHA-1 or
  RIPEMD-160 op, unknown attestation tag, bound exceeded → `INVALID / OTS_FORMAT`.
- L-88 Receipt OTS digest ≠ SHA256(`A_sig`) → `INVALID / RECEIPT_ANCHOR_MISMATCH`.

**Git (G25)**
- L-89 Merge commit with two distinct parents → passes format. L-90 repeated identical parent → `GIT_COMMIT_FORMAT`.
- L-91 `encoding` header, second `gpgsig` → `GIT_COMMIT_FORMAT`. L-92 armor header line, CRC mismatch, 77-character
  line → `GIT_SIG_FORMAT`. L-93 noncanonical tree order, mode `040000` → `GIT_TREE_FORMAT`. L-94 SHA-1DC
  collision-pattern object → `GIT_SHA1_COLLISION`. L-95 signer verifies, T_git outside interval →
  `GIT_SIGNER_OUTSIDE_INTERVAL`; L-96 no configured signer verifies → `UNVERIFIABLE / GIT_SIGNER_NOT_CONFIGURED`.

**Signature profile (G11, G28; not P8 codec vectors)**
- L-97 Hashed creation time marked critical → passes. L-98 SIG-01 with critical bit on unhashed key ID → passes.
- L-99 Unknown critical hashed subpacket → `SIG_POLICY`. L-100 hashed type 3 → `SIG_POLICY`. L-101 two type-2 →
  `SIG_POLICY`. L-102 type 2 with 3 or 5 data octets → `SIG_POLICY`. L-103 no type 2 → `SIG_POLICY`.
- L-104 Subpacket length 191 and 192 in shortest and non-shortest form (codec boundary; P8 if absent there).

**Keys (G21)**
- L-105 Under the hybrid, the supplement's ML-DSA-65 SPKI in `kms` passes the key-format check; under the fallback
  the same bytes → `INVALID / KEY_FORMAT`.

**Aggregation and report (G26, G31, G32)**
- L-106 `KEY_MISMATCH` plus bad git signature, evaluated in both schedules → reason `KEY_MISMATCH`.
- L-107 Unknown `alg` plus an independent failure → `INVALID` with that failure's reason.
- L-108 Bad attestation signature plus a usable receipt anchor → `INVALID / SIG_INVALID` with T reported.
- L-109 Receipt proof with a contradicted branch → T `null`.

**Field grammars and numbers (G18, G29)**
- L-110 Year 0001 and 9999 accepted; 0000 rejected; numeric top label accepted (codec boundary cases).
- L-111 ES conformance: N-01…N-22, C-N01…C-N22, plus a tie case and −0.
