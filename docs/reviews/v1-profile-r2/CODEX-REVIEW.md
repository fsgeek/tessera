# Full review of V1-PROFILE, revision 2 — 2026-10-14

**Answer: not yet.** A9 + the 1045-line V1-PROFILE + ENCODING-V1 now specify substantially more of a verifier, including concrete container, snapshot, git and OTS formats. They still do not determine a unique verdict and six-field report on every input. There are acknowledged freeze inputs still to supply, and additional forks in algorithm routing, nested absence, DNSSEC candidate classification, proof checks and reason ordering. Section 14.2 is not complete.

**Recommendation: revise before freezing; retain DRAFT.** No implemented full-verifier forgery is demonstrated here. Most findings concern rejection class or stable reason; several concern acceptance versus rejection. Release-key independence remains a conditional security boundary requiring evidence, rather than a newly demonstrated attack. This review neither chooses owner policy nor discharges C1–C7, P8, the 30 Oct gate or implementation readiness.

## Authority, read boundary and severity

A9 governs as the task instructs, despite its PROPOSED label. The user's latest owner correction governs G02: **no `T_git <= declared_issue_time` check; only `h_git + 5 < h_receipt` remains**, together with the repository signer interval check. I read V1-PROFILE lines 1–1045 in full, A9, ENCODING-V1, the runbook, GAPS, RESOLUTIONS-DRAFT, CODEX-REVIEW-RESOLUTIONS and DISPOSITION-RESOLUTIONS. The dispositions were compared with every G01–G39 integration group, including the grouped tags. Local codec/probe snippets were inspected only to establish that missing rules exist elsewhere; they do not supply normative rules for the three-document sufficiency question.

The review distinguishes two questions:

1. **Can a verifier be built today from these documents alone?** No: branch, authenticated trust bytes, frozen objects/catalog and dependency editions are not furnished. Some of these are explicitly scheduled owner acts.
2. **After supplying the acknowledged freeze inputs, is the written decision function total and unique?** Still no, for the forks below. A matching frozen object hash removes byte-assembly ambiguity at runtime; it does not repair ambiguities in the rules that those bytes instruct implementers to apply.

“Every input” must mean every bundle/request given an installed, authenticated verifier and valid declared trust input. The profile deliberately specifies **no verdict** for an unauthenticated configuration or incompatible Unicode runtime. That is appropriate fail-closed startup behavior; it should not be advertised as a bundle verdict. Resource exhaustion or host failure is also not evidence that a bundle is INVALID.

Severity: **High** is an acceptance/registered-outcome or load-bearing interoperability defect; **Medium** is a remaining verdict/report fork, format stop, or unsupported evidence/policy assertion; **Low** is misleading accounting or wording without a demonstrated decision fork. Exact fixes below are proposed text or concrete edit instructions, not adopted rules.

## Remaining forks and exact fixes

### F01 — High: algorithm policy, codec routing and M5 do not compose

**Locations:** P:88–93, 176–179, 226–228, 541–554, 665–670, 1017–1023; E:385–394, 436–442. G10/G12/G21/G26.

Three rules disagree at their join. E chooses the signature codec from each frame's own `common.alg`, and recognizes the classical id as rule O. P says an id other than the frozen catalog id, including the unchosen branch, is `UNVERIFIABLE / ALG_UNKNOWN`; P's aggregation paragraph says an unknown alg routes the slot as opaque. M5 separately says manifest `alg` equals the catalog's single id and mismatches are INVALID. Literal M5 enforcement can therefore turn the intended unknown-algorithm canary into INVALID even when both frames and manifest agree on the same well-formed unknown id. On a hybrid installation, a classical id can select rule O under E or opaque handling under P; non-rule-O signature bytes distinguish those codecs. Other independent failures may still make either complete bundle INVALID; the routing fork exists before them.

**Exact fix:** distinguish **codec-known** from **policy-supported**:

> Each frame is decoded with E §5.2's codec registry, including any authorized supplement, using its own alg and slot. A codec-known but unselected branch still uses its specified codec; an id absent from that registry uses the opaque codec. Signature/possession verification semantics are performed only for the catalog-supported id. Receipt/manifest alg equality is checked independently for every syntactically valid id. M5's catalog-alg condition is performable only for a policy-supported id; unsupported ids contribute ALG_UNKNOWN, not an additional SCHEMA failure.

This preserves A9's encoding baseline and the catalog's single selected branch without inventing opaque decoding for an E-known scheme. If the owner instead wants every catalog-unsupported id opaque, expressly change the incorporated codec baseline and its vectors. Add unknown-id and branch-not-taken tests with codec-valid and codec-invalid signatures, both matching and mismatching manifest algs.

### F02 — Medium: “receipt consistency (ENC §5.3)” is not a complete normative subcheck list

**Locations:** P:189–195, 1018–1020; E:303–320, 362–369, 491–511. G10/G31.

Common-byte equality and slot binding are required in prose, but the total order refers to E §5.3 for receipt consistency. That section does not enumerate common mismatch, manifest issuer/alg mismatch, or their reason order. P also does not give a reason code for a bad `manifest_sha256`. An implementer reading only these three documents cannot import the codecs' `RECEIPT_COMMON_MISMATCH` and `RECEIPT_MANIFEST_MISMATCH` definitions. A receipt whose frames disagree on content and whose manifest issuer also disagrees must be rejected, but its stable reason is not determined. Moving manifest-hash comparison to stage 4 without naming its code adds another overlap with stage 6.

**Exact fix:** insert an explicit ordered consistency table:

> Both frames' signer fingerprints equal the corresponding manifest fingerprints (RECEIPT_SLOT); their common byte substrings are equal (RECEIPT_COMMON_MISMATCH); common issuer and alg equal manifest issuer and alg (RECEIPT_MANIFEST_MISMATCH). Stage 4 checks common.manifest_sha256 against SHA256(F_manifest), using RECEIPT_MANIFEST_MISMATCH; when both common objects are available, check each in kms/gpg order. These checks never require signature validity or channel authentication.

Then list these exact subchecks in §15.7. Keep anchor digest verification in receipt OTS; with the a_sig-only route there is no second externally transported tuple to reconcile. A9's bytes/signature binding remains required; this is specification completion, not permission to omit the checks.

### F03 — Medium: nested absence contradicts the diagnostic and descriptor exceptions

**Locations:** P:141–151, 491–495, 878–898, 1015–1016. G14/G17/G33/G39.

“Required member absent at any nesting level” gives MEMBER_MISSING. Yet missing `git.object_format` has its own A9 code, while a present malformed `issuer_record` must be INVALID. Consider otherwise good inputs with (a) `git` present but `object_format` missing; (b) `issuer_record: {}`; (c) `keys: null`; (d) one required member absent plus another present member malformed. The generic absence rule can report MEMBER_MISSING:git.object_format before the descriptor check; the empty diagnostics object can give UNVERIFIABLE for missing nested fields instead of the promised INVALID; a null parent can be treated either as a malformed object or as absent descendants. Absence-first is a reason order, not authorization to ignore independent INVALID checks (A9/P §3.3).

**Exact fix:** add:

> A missing required evidence member contributes UNVERIFIABLE/MEMBER_MISSING:<path>, except git.object_format, which contributes GIT_OBJECT_FORMAT_MISSING. A present parent of the wrong type contributes CONTAINER_SCHEMA; do not synthesize missing descendants beneath it. Absence of issuer_record is allowed; any defect in a present issuer_record, including absent internal fields, contributes INVALID/CONTAINER_SCHEMA. Absence and schema failures are collected independently; INVALID still dominates. Nested absence is inspected only beneath correctly typed parents.

State whether non-string `object_format` is the unsupported-value exception or CONTAINER_SCHEMA; A9 says unsupported value, and RES says any present value other than sha1 is UNVERIFIABLE. The least divergent integration is to make that exception explicit for **all** present non-sha1 values. Define MEMBER_MISSING paths as layer-relative dotted schema paths (matching L-09/L-10), and compare missing paths using JCS key order with array indices numeric. Add all four cases above and `object_format: null`.

### F04 — Medium: TRUST_HORIZON overlaps the root/repository interval failure tables

**Locations:** P:361–390, 488–490, 998–999, 1029–1033. G09/G22/G25/G27.

For a signature that verifies under a configured open key at time `as_of + 1`, §5 says UNVERIFIABLE/TRUST_HORIZON. The root table says a verifying key outside its reliance period is INVALID/KSK_OUTSIDE_RELIANCE_PERIOD; the git table says a verifying repository key outside its interval is INVALID/GIT_SIGNER_OUTSIDE_INTERVAL. These are the same input with different verdict classes. Mixed candidates make the overlap worse: one finalized out-of-period candidate and one open-horizon candidate have no stated aggregation. Root edge-time failures have also been added without updating the root outcome table.

**Exact fix:** define candidate outcomes before aggregation: eligible pass; open entry with t > as_of is horizon-unperformable; finalized out-of-period is an interval failure; time-window/edge failure; crypto failure; no configured candidate. A proposed deterministic precedence is:

> Any eligible validating candidate passes. Otherwise a cryptographically validating, time-valid candidate limited only by an open horizon gives TRUST_HORIZON. Otherwise use finalized interval failure, time failure (including G27), crypto failure, then no configured candidate, in that order. Multiple reasons within one class use the G35 canonical candidate order.

Use the same classification for root and repository checks, and explicitly add TRUST_HORIZON to §15.7. A different precedence is an owner choice, but one must be selected. Authentication of the key and signature is still necessary before claiming horizon alone prevents acceptance.

### F05 — Medium: DNSSEC's candidate outcome table does not cover all failed RFC checks

**Locations:** P:430–445, 649–654, 1029–1030. G16/G27/G35.

RFC 4035 §5.3.1 requires matching signer, algorithm and key tag, a usable Zone Key, and Labels constraints, among other checks. The profile says to perform that validation, but gives result classes only for missing evidence, potentially supported paths, time failure, crypto failure and DS mismatch. An intact TXT RRset with a supported RRSIG whose tag matches **no** DNSKEY is not a missing RRSIG, not a checked crypto failure, and not a child-DNSKEY/DS mismatch. Labels greater than the owner count, protocol/flag defects, and supported malformed key/signature encodings have similarly missing outcomes. “Unsupported ... could supply the path” does not define which mismatching/unauthenticated candidates count as potentially usable. One implementation can call an unmatched selector missing evidence, another INVALID, another mislabel it DNSKEY_DS_MISMATCH. [RFC 4035 §5.3.1](https://www.rfc-editor.org/rfc/rfc4035.html#section-5.3.1).

**Exact fix:** supply a table mapping every supported validation precondition failure to a code/class, and separate DS→DNSKEY matching from RRset→RRSIG matching. Proposed entries: malformed supported key/RRSIG RDATA = INVALID/DNSSEC_FORMAT; present supported witness with no matching eligible DNSKEY = INVALID/DNSSEC_KEY_MISMATCH; Labels too large or other non-temporal metadata mismatch = INVALID/DNSSEC_RRSIG_METADATA; absent required RRset/RRSIG = UNVERIFIABLE/DNS_EVIDENCE_MISSING. Define “potentially unsupported path” by authenticated DS metadata and matching algorithm/tag/name selectors, not any unrelated unsupported RR. If insufficient evidence is intended to cover an unmatched key instead, select that classification expressly and test it.

Also state dependencies: a downstream *authenticated-path* check blocked by parent authentication is unperformable, while locally obtainable framing, TXT grammar and signature mathematics may still be checked. Specify which local candidate failures become reportable required-check failures when no path validates. Add mixed unsupported/selector-mismatch, no-key, bad flags/protocol, wrong Labels, malformed supported RDATA and parent-blocked-child tests. This is not a claim that RFC 4035 is unspecified; it is the missing bridge from its failures to the frozen V1 partition/report.

### F06 — Medium: snapshot grammar cannot uniquely distinguish missing groups from a different chain

**Locations:** P:417–420, 639–644, 930–945. G19/G24.

“Missing groups alone are not order violations” is useful, but the remaining sequence is not a complete chain declaration. With a root DNSKEY group followed directly by a TXT group signed by wamason.com, is wamason.com the omitted last zone (UNVERIFIABLE), or is its signer inconsistent with the last supplied zone (INVALID/SNAPSHOT_FORMAT)? A DS group at a zone whose DNSKEY group is omitted creates the analogous fork. With no below-root z, “the last z” is undefined for TXT signed by root, although §6.1 expressly retains ancestor-zone signing authority. A present wrong-owner TXT can be rejected as an RR outside the chain or reach E's DNS_OWNER check. The body grammar also does not say whether an internally malformed TXT character-string is SNAPSHOT_FORMAT or E's DNS_RDATA.

**Exact fix:** give a recovery grammar that treats the root as the initial zone, constructs the ordered zone skeleton from supplied DS/DNSKEY owners and RRSIG signer names, admits omitted DS/DNSKEY/root/TXT groups as missing evidence, and explicitly permits direct root signing. Conflicting supplied transitions/signer names are SNAPSHOT_FORMAT; omission alone is DNS_EVIDENCE_MISSING. State that a supplied final TXT owner is checked by E §7's DNS_OWNER even when wrong; its existence does not itself constitute an “outside-chain” framing failure. Only RR boundary/RDLENGTH truncation is SNAPSHOT_FORMAT; TXT's internal character-string parsing uses DNS_RDATA/DNS_STRINGS. Add root-only→TXT, missing last DNSKEY, missing DS, missing root, wrong-owner TXT and malformed character-string vectors. If the owner wants a narrower chain skeleton instead, define it and label the restriction.

### F07 — Medium: wildcard rejection can defeat an otherwise eligible witness

**Locations:** P:427–450, 628–634, 940–946. G16/G19/G35.

The profile promises that extra invalid candidates are informational after an eligible path passes, but also says **a TXT RRSIG** with fewer Labels causes DNS_WILDCARD, and lists that code among body checks before DNSSEC. A canonical snapshot offering a valid explicit-owner signature plus an extra less-Labels signature distinguishes “reject any offered wildcard” from “exclude wildcard candidates and accept the valid explicit witness.” Both are credible readings. Canonical group RRSIG ordering also has no final tie-breaker for signatures equal on tag/inception/expiration/signature bytes but differing in other RDATA; G35 fixes witness order, not wire group order.

**Exact fix:** choose explicitly. To preserve the stated existential policy:

> A less-Labels TXT RRSIG is an ineligible wildcard candidate; it contributes DNS_WILDCARD only if no supported eligible explicit-owner path validates and its failure class is selected by the DNSSEC table. It is not a global snapshot-format failure. Extra failing candidates remain informational after a valid explicit witness.

Alternatively retain a global no-wildcard-in-body transport restriction and name it separately from witness eligibility; then narrow the “extra invalid candidates” promise accordingly. Append canonical RRSIG RDATA as the final **body serialization** sort key, and specify duplicates as identical owner/class/type/RDATA (TTL consistency separately). Test a valid explicit witness plus a wildcard candidate, both serialization orders of a primary-key tie, and duplicate RRSIG handling.

### F08 — Medium: “OTS (as 11)” imports a receipt-only txid check into proofs with no txid

**Locations:** P:893–896, 919–926, 1025–1033. G20/G31.

Snapshot and git carry `ots` but no transaction id. Their stage definitions say “OTS (as 11, with ... substitutions)”; stage 11 includes ANCHOR_TXID_MISMATCH. One reader runs only the receipt's txid check; another applies the shape check to all proofs and compares snapshot/git transactions with receipt_anchor.txid; another calls those checks unperformable because no per-proof txid exists. Snapshot/git normally anchor in different transactions, so this changes honest outcomes. The selected-height rule also does not let a failing first txid candidate defeat another satisfying path at the same selected height; implementations need that aggregation explicitly.

**Exact fix:** enumerate snapshot/git OTS subchecks instead of “as 11”: grammar, object digest, contradictory branch, qualification/no-anchor. State:

> §15.2's transaction-shape and txid-equality check applies only to receipt_anchor. The snapshot/git proofs use the closed OTS grammar and header qualification, with no txid comparison. Select h* before the receipt txid check; any satisfying qualifying path at exactly h* passes that check. Never switch to a higher height merely to find a matching txid.

If the intended supported subset applies transaction shape to all proofs, say so separately and compare no receipt txid there. Add three different anchor transactions and two paths at the same selected height, one satisfying and one failing the txid subset.

### F09 — Medium: OTS/Bitcoin wire completion and malformed attestation outcomes remain implicit

**Locations:** P:584–597, 902–926. G05/G20.

`varbytes` is used but never defined. CompactSize width/byte order is only named, not pinned inline or to an exact normative section in the three documents; transaction parsing otherwise looks like a complete recipe. A Bitcoin attestation message must be 32 bytes, but no outcome is given when it is shorter/longer and its header is absent. A grammar rejection (OTS_FORMAT), a nonqualifying branch (UNVERIFIABLE), or OTS_MERKLE_MISMATCH are all possible implementations. Pending payloads are not expressly required to consume their inner URI framing exactly. Depth counts are undefined (operations, Timestamp nesting or ff items); branches declared effect-free still count against bounds, but the text does not say that.

**Exact fix:** define `varbytes := varuint byte_count || exactly byte_count octets`; require exact consumption of both pending and Bitcoin payloads. Define Timestamp depth as root depth 0, each Op→Timestamp incrementing by 1, ff siblings not incrementing; count serialized ops/attestations including duplicates, with duplicates semantically inert **within** those limits. Reject non-32-byte Bitcoin messages as OTS_FORMAT independently of header availability. Specify CompactSize: byte <253 is its value; fd/u16le, fe/u32le, ff/u64le, shortest form; reject lengths/counts exceeding remaining bytes before allocation. State that transaction version/value/locktime are parsed as their fixed-width bytes and that consensus/script execution is supplied by authentic pinned history, not revalidated here. Pin the raw-header nTime extraction (`uint32le(header[68:72])`), prev field (`header[4:36]`) and CompactSize/transaction dependency. [Bitcoin transaction format](https://developer.bitcoin.org/reference/transactions.html#raw-transaction-format).

The remaining OTS operations already give a cryptographic commitment path to a pinned merkle root. If the txid claim is also intended to assert a conventional transaction-to-block merkle branch, define its suffix as repeated append/prepend of a 32-byte sibling followed by two SHA256 operations, permitting an empty suffix for a one-transaction root. Currently arbitrary allowed operations can follow the identified transaction pair. This is a missing structural definition, not a demonstrated forged timestamp under secure hash/history assumptions.

### F10 — Medium: the rule-O policy does not settle metadata syntax, hash-prefix and key validation

**Locations:** P:665–688, 958–962; E:289–290, 324–331, 455–468. G11/G21/G25/G28.

Accepting type 16/33 whether critical is sound for a verifier that binds the actual supplied key by SHA-256 and verifies with it. It does not establish the metadata's claimed identity. “Never read” leaves malformed payloads, duplicate subpackets and conflicting type-16/type-33 values unspecified relative to the cited RFC. A zero-data critical type 33 is a concrete syntax-versus-ignore fork. The unhashed area must still be structurally parsed under E even though its **semantics** are ignored.

The two-byte hash prefix is outside the OpenPGP signed hash input. Mathematical ECDSA verification alone can therefore pass with an altered prefix, while a packet validator may reject. The profile has no explicit v4 prefix policy. Similarly a byte-shaped P-256 SPKI/key packet is not necessarily a valid public point; on-curve, finite and subgroup validation must not depend on library defaults. Git armor permits base64 characters but does not inherit the container's round-trip requirement, leaving nonzero-pad-bit aliases unspecified.

**Exact fix:** declare the small V1 policy complete:

> Beyond subpacket framing and the type-2/type-3 rules, types 16 and 33 are opaque advisory octets in V1, including payload length, repetition and cross-field consistency; their critical bits are recognized but confer no key-selection authority. Other unhashed contents are also semantically ignored after structural parsing. This overrides generic OpenPGP metadata interpretation for V1 and is not a claim of full RFC metadata conformance.

If structural type-16/type-33 validation is wanted, replace that proposal with exact lengths/versions/cardinality and failure codes; do not leave it to a keyring library. State explicitly that the two hash-prefix octets must match SHA256(document || E trailer), else SIG_INVALID/POSSESSION_INVALID (git uses its signature-verification outcome). Require a finite on-curve P-256 public point and the FIPS public-key validation appropriate to P-256, else KEY_FORMAT (configuration keys rejected at startup). Apply strict RFC 4648 round-trip/padding to concatenated git armor base64; CRC presence/validity remains as specified. [RFC 9580 subpackets](https://www.rfc-editor.org/rfc/rfc9580.html#section-5.2.3.7), [issuer fingerprint](https://www.rfc-editor.org/rfc/rfc9580.html#section-5.2.3.35).

These are completion choices. No end-to-end service forgery follows merely from advisory metadata being ignored, prefix aliasing, or armor aliases. Add metadata-shape, wrong-prefix, invalid-public-point and nonzero-pad-bit vectors.

### F11 — Medium: the “total check order” is still not total

**Locations:** P:201–229, 1010–1036; E:178–190, 385–394, 429–468. G26/G31/G32.

The stable reason contract is sound, and early exit is correctly limited by stable T. The remaining problem is enumeration. Stage 9 lists SIG_FORMAT but omits SIG_EMPTY, SIG_PACKET, TRUNCATED, TRAILING and LENGTH_CAP for possession signatures. It gives no possession format/policy reason mapping. Receipt signature syntax is already decoded inside a_sig at stage 3, so its listed stage-9 syntax check either repeats an earlier result or moves priority. Root/window edge reasons occupy one rank with no selected reason rule; snapshot OTS and git OTS inherit the scope defect F08; TRUST_HORIZON is absent. Git policy failure is SIG_POLICY under §8 but GIT_SIG_FORMAT under §15.4. Bundled object hash checks have four members but no explicit dependency on catalog lookup. The candidate-order fallback “JCS key, then array index” orders objects in transport arrays, whereas G35 orders candidates by cryptographic fields; it does not order an unordered set of candidate outcomes.

**Exact fix:** replace the stage sketches with a numbered check table. Each row must give check id, inputs, availability condition, failure/unperformable code and tie key. Keep receipt signature codec failures only at stage 3; give possession codec failures E's exact codes with slot diagnostics, then SIG_POLICY, then POSSESSION_INVALID. Select one git mapping (proposed: all armor/codec/policy violations → GIT_SIG_FORMAT; failed mathematics → GIT_SIGNER_NOT_CONFIGURED per §6.3) and expressly make it the exception to §8's generic policy code. Order DNS edge reasons within their class by the selected failing candidate's G35 tuple, then endpoint (inception before expiration), then ambiguous/reversed/window check order. Incorporate F02–F10 and F12. Add multiple-failure tests across stages and within possession/DNS/git, not just reversed schedules with one failure per stage.

This is a reason/report blocker under A9.4 even where all implementations reject the same input. Do not weaken INVALID-over-UNVERIFIABLE or permit early exit before an independently obtainable receipt T is settled.

### F12 — Medium: an unknown spec hash does not define which object comparisons remain performable

**Locations:** P:80–96, 720–721, 1022, 1036. G13/G15/G26.

For an unknown common.spec.sha256 the catalog lookup has no entry. “Signed or catalog values” does not specify whether vectors/preamble/dependency are compared with the sole installed entry anyway or become unperformable. A bundle with an unknown spec hash, internally matching signed spec/vector/preamble objects, and a dependency manifest different from the installed entry distinguishes UNVERIFIABLE/SPEC_UNKNOWN from INVALID/BUNDLE_OBJECT_HASH. Bundled objects must not become policy just because their hashes are self-consistent.

**Exact fix:** enumerate targets: bundled spec → signed common.spec.sha256; vectors → signed vectors_sha256; preamble → signed preamble_sha256, independently of catalog lookup. Signed vectors/preamble → catalog entry only if spec lookup succeeds. Dependency manifest → catalog entry only if lookup succeeds; otherwise that comparison is unperformable, not compared with an unrelated entry. Other independent failures still dominate SPEC_UNKNOWN. List this availability in §15.7 and add unknown-spec plus independently bad signed-object bytes, and unknown-spec plus unmatched dependency bytes.

### F13 — Medium: the part-line assembly is not a fully canonical freeze recipe

**Locations:** P:86–87, 94–99, 859–871, 1038–1045. G13/G15/G37.

The ASCII header simultaneously permits UTF-8 paths without spaces. It does not exclude LF, CR, tab, absolute paths, dot components or duplicate paths. Nor does “every file under formal/p8/vectors/” select tracked regular files versus generated/untracked files, symlinks and directories. “The non-P8 conformance vectors (RES §L)” refers to cases, not concrete file paths. These choices change signed hashes at assembly time. Once exact catalog hashes exist, runtime hash checks are unique; runtime must still never parse these objects as policy.

**Exact fix:** choose a safe header grammar, for example ASCII repository-relative paths matching `[A-Za-z0-9._/-]+`, no empty/dot/dot-dot components, no leading slash, unique paths; length `0|[1-9][0-9]*`; fixed literal spaces and LF. Include only tracked regular file **blob bytes** from a named freeze commit; no newline conversion, symlink following, generated caches or working-tree overlay. Publish an exact sorted vector-path inventory in the freeze record, including non-P8 vectors, and an assembler plus independent byte agreement check. Put actual spec/vector/catalog hashes in a separate release/freeze record **outside the frozen spec parts**; otherwise recording them inside the included profile creates self-reference despite the stated no-cycle rule.

The two-part spec also refers normatively to A9 without carrying it. Include the governing A9 bytes as a part or distribute/archive them separately with a bound digest and say that the object alone is not the complete archival spec. This affects independent reconstruction/readability, not executable policy loading. The invented framing is a defensible new packaging choice, not an inherited P8 construction or a proven archival format.

### F14 — Medium: exact dependency closure and trust-schema completion are still missing freeze work

**Locations:** P:379–399, 686–688, 708–745, 973–1008. G08/G09/G15/G22/G28/G29.

The dependency list names standards but does not supply pinned editions/errata/digests for ECMA-262, UAX #15, git/SHA-1DC, Bitcoin and the release verifier. Its seven fields are a schema for a future object, not that object. Reading precisely three Markdown files cannot implement Unicode 16 NFC tables or complete RSA/DNSSEC/CMS from the listed names alone. Offline **verification after installation** is possible in principle; offline **reconstruction from only these files** is not yet furnished. SHA-1DC detection, in particular, must use a pinned detection implementation/version and prescribed collision-return behavior rather than whatever a future library calls SHA-1.

The trust schema says every key is required but does not expressly say closed at every object level. Its decimal/key-tag sort rules are less concrete than §15.1: string or numeric key_tag comparison, leading-zero policy, source-object extra fields and an open entry with signing_start > as_of are not resolved. These primarily affect release construction/startup validity, since a release compiles one exact hash, rather than granting a bundle authority to rewrite trust.

**Exact fix:** add a §14.2 item to construct and archive the actual dependency manifest plus the referenced normative bytes/tables or immutable retrievable source artifacts, with exact editions, sections, errata and digests; identify which are distributed versus externally retrieved at build time. Pin SHA-1DC and release-signature dependencies. Make §15.5 closed recursively, use strict UTF-8/JCS/no-number parsing, canonical base64, the UTC grammar in §10, canonical unsigned-decimal strings with per-field ranges, numeric key_tag sorting and a complete tie key (dnskey_rdata bytes). Require signing_start ≤ as_of for open entries, nonempty valid key/source arrays, and select maximum/range rules for L/version. Schema failures are startup refusal, not bundle INVALID. Keep cross-release invariants in the release checker, not a need for the offline verifier to fetch a previous config.

Correct G28's “255, four octets” to **255 followed by a four-octet big-endian value (five octets total)**. RFC 9580 gives that precise form. Under the 1024-byte rule-O cap a conforming shortest form never needs it, so this is mainly a parser/rejection-boundary wording defect. The 192–254 two-octet range and 16319 maximum are correct. [RFC 9580 §5.2.3.7](https://www.rfc-editor.org/rfc/rfc9580.html#section-5.2.3.7).

### F15 — Medium: KSK-2017's day is sourced now; its midnight signing start is not established

**Locations:** P:344–360, 385–387, 859–861. G22.

IANA currently records KSK-2017 signing from **2018-10-11**, so the remembered **day** was correct. The proposed `2018-10-11T00:00:00Z` is a stronger claim: ICANN's operational account says the switch occurred at **16:00 UTC**. That does not by itself identify the inception of the first pre-generated root RRSIG; publication/switch time and RRSIG inception must remain distinct. Neither a remembered day nor a day-granularity IANA table proves midnight. [IANA key status](https://www.iana.org/dnssec/files), [ICANN operational account](https://www.icann.org/en/blogs/details/the-recent-ksk-rollover-summary-and-next-steps-30-10-2018-en).

**Exact fix:** retain the proposed start as OPEN, but label the midnight value as a proposed **acceptance-policy endpoint**, not a sourced exact signing event. Archive the cited sources with digests; obtain the historical first applicable signed root RRset/ceremony evidence if claiming an exact inception-based endpoint. Record separately the operational switch (16:00), RRSIG inception and chosen policy signing_start, with rationale. If using actual switch time as the policy, choose 2018-10-11T16:00:00Z with a boundary vector; do not silently infer it from a day or assume it is the RRSIG inception. The same evidence distinction applies to KSK-2024's precise start and KSK-2017's precise end.

This has no shown effect on the ordinary 2026 V1 issuance path. It matters for truthful sourced configuration, interval-boundary inputs and future reproducibility. The proposed status and §14.2 item 3 correctly prevent the memory-derived value being presented as frozen trust material.

### F16 — Medium: the adopted clock-check removal is not propagated to RES's text and vector obligations

**Locations:** P:515–529, 869–871; RES G02 and §J/§L; RB §5. G02/G31.

P and RB correctly remove the clock comparison. RES's struck-out resolution/top table also records removal, but its quoted CORRECT text still says the verifier requires it; the issuer-duty paragraph still tells the issuer to check/wait for it; G31 still lists GIT_ASSERTION_AFTER_ISSUE; L-27/L-28 still test it, with L-28 requiring INVALID at declared + 1. P §14.2 imports all L-01–L-111 as freeze obligations. Thus the profile is correct locally yet imports a contradictory vector expectation. The user correction resolves authority: do **not** reinstate the clock check to satisfy the old vectors.

**Exact fix:** replace those RES occurrences with the current P:522–526 wording; remove GIT_ASSERTION_AFTER_ISSUE from the reason list; replace L-27/L-28 by positive controls with T_git > declared and T_git > receipt T but `h_git + 5 < h_receipt`, repository interval and all other checks satisfied. Those controls must pass. Keep L-29–L-31 as chain-order controls. Until RES is edited, P's import should explicitly exclude the withdrawn numeric expectations and name replacement tests. Only the review is edited in this task.

### F17 — Low: extraction citations and open-list accounting can conceal real deadlines

**Locations:** P:29, 47–49, 658–660, 825–872. A9.6 slot-2 deadline; RB §6.

Numerous A9 line references are from an earlier layout (for example P:658 cites A9:338–340 for fallback; that current range is trust-configuration authority). Section identifiers are more reliable. §14.2's custody item does not repeat A9's **21 Oct deployed-slot evidence deadline for the hybrid**; choice before 30 Oct is allowed only among implementations that already met it. Release-key rotation/recovery/loss procedures are explicitly OPEN in the runbook but not individually named in §14.2. The frozen purpose preamble is absent from the freeze-assembly item. “Each requirement points to where decided” is also weaker than stated when a requirement points only to a later owner tag and RES is itself inconsistent (F16).

**Exact fix:** refresh A9 references against the reviewed snapshot, prefer section + stable rule name, and include the signing/freeze commit in the source table. Expand item 5 with the 21 Oct condition. Expand items 1–2 to explicitly cover bootstrap, release-key rotation and authenticated loss/compromise recovery, or explicitly bound which recovery capabilities V1 omits. Expand item 7 to include the preamble and dependency object hashes and their authored bytes. Do not turn those operations into additional bundle-verifier rules.

## Audit of every owner-tagged integration group

“Matches” means faithful to the dated disposition, not proof that its rule is sufficient or sound on all inputs. Grouped rows below enumerate every G01–G39; untagged 2026-10-13 decisions were also reviewed above.

| Gap(s) | Profile location | Disposition/integration assessment |
|---|---|---|
| G01 | §6.4 | Matches required direct-form set and first offending element; E §8 wording remains pending. |
| G02 | §4, §6.3 | Matches the latest owner removal and A9 C4 chain order; supersedes RES's surviving clock text. F16. |
| G03 | §7.1 | Matches A9 C5 lowest-height selection; no least-nTime substitution. |
| G04 | §7.1 | Matches fifth-successor nTime; nonmonotone timestamps expressly allowed. |
| G05 | §5, §7.1–7.2 | Matches selected-anchor reading and contradiction/coverage asymmetry. Message-length outcome still needs F09. |
| G06 | §4, §7.3 | Matches snapshot T/depth and added c3; honest issuer checks before ship. |
| G07 | §7.2 | Matches shared pool, all supplied pins and adjacent-pair links; no retarget/PoW requirement introduced. |
| G08 | §5, §15.5 | Matches independent release allowlisting and no-verdict refusal. Custody/format are visibly OPEN, not established. |
| G09 | §5, §15.5 | Matches finite open horizons and release invariants; failure-table join unresolved, F04. |
| G10 | §6.4 | Matches M5 constants/channel distinction; unsupported alg and consistency/report joins need F01/F02. |
| G11 | §4, §8 | Matches revised creation-time/expiry/critical-bit policy, including 16/33 choice; metadata semantics completeness F10. |
| G12 | §1 | Matches catalog constants, selected id and empty prohibited set; codec/policy routing needs F01. |
| G13 | §1, §15.8 | Matches the new part framing and hashed-not-executed rule; unknown-catalog checks and assembly need F12/F13. |
| G14 | §2.1, §15.1 | Matches one tuple route and absent/present split; nested diagnostic/descriptor exceptions need F03. |
| G15 | §9, §15.6 | Matches expanded standards, seven fields plus id/title and catalog hash; actual object/closure still missing, F14/F17. |
| G16 | §4, §6.1 | Matches root reliance priority, algorithms 8/13, DS 2/4 and visible support limit; exhaustive outcomes need F05. |
| G17 | §3.1, §15.1 | Matches D1–D4 and canonical container. “Exactly three things” excludes syntax/cap gates but says four named dispatch checks; harmless wording, clarify to “four checks.” |
| G18 | §10 | Matches years 0001–9999 and numeric LDH labels; pending E wording correctly listed. |
| G19 | §4, §6.1, §7.3, §15.3 | Matches RR body, fresh stamp and no-wildcard choice; missing-chain and candidate/global rules need F06/F07. |
| G20 | §7.1, §15.2 | Matches declared transaction-preimage subset, not merely first-hash heuristic. **No normative 125-byte requirement was added.** F08/F09 remain. |
| G21 | §8 | Matches branch-specific transported keys selected by installed spec; explicit public-key validity F10. |
| G22 | §5, §15.5 | Matches full RDATA/source acquisition and REVOKE-bit exclusion; starts remain proposed, correctly. F04/F14/F15. |
| G23 | §7.2 | Matches owner INVALID for a conflicting pinned height; uncovered heights remain UNVERIFIABLE. |
| G24 | §3.2, §7.3 | Matches present malformed TXT INVALID independent of DNSSEC and absent group UNVERIFIABLE; body/codec boundary F06. |
| G25 | §6.3, §15.4 | Matches closed git grammar, distinct merge parents, P-256, SHA-1DC and signer outcomes; policy/code overlap and key/armor checks F10/F11. |
| G26 | §3.3, §15.7 | Matches corrected early-exit contract; RES's explicit input-independent/dependent list is not reproduced, though P retains its general principle. Complete concrete check table needed, F11. |
| G27 | §7.3 | Matches half-range failure, resolved reversed failure and equal endpoints allowed; edge reason aggregation needs F04/F11. |
| G28 | §8 | Matches thresholds/shortest form; reproduces misleading “four octets” phrasing for five-octet form, F14. |
| G29 | §10 | Matches closest-decimal/ties-to-even ES recipe and Unicode pinning; actual edition/table digests still needed, F14. |
| G30 | §3.2, §15.3 | Matches separate caps and empty snapshot LENGTH_CAP. |
| G31 | §3.2, §15.7 | Matches adopted stage sketch and correctly removes obsolete git clock reason locally; sketch still not total, F02/F11/F16. |
| G32 | §3.4 | Matches six-field JCS, OK, null criterion, T despite unrelated INVALID and warning text. Does not require txid match to display T; that is deliberate, not a new fork. |
| G33 | §2.1, §15.1 | Matches optional unsigned diagnostics and malformed INVALID. Missing internal-field exception needs F03. |
| G34 | §6.3–6.4 | Matches common pinned-D gate and M2; alternate-D plus missing git correctly INVALID. |
| G35 | §7.3 | Matches eligible validating witness and full tie-breakers; body serialization has only shorter sort tuple, F07. |
| G36 | §0.1, §5 | Matches custody as operating fact; repository root is distinct from release key. |
| G37 | §1 | Matches signing-baseline/change-accounting requirement; does not authorize arbitrary edits to E. |
| G38 | §10 | Matches A9.8 superseding stale warnings; pending edits are correctly visible. |
| G39 | §6.3 | Matches sha1 descriptor, exact commit-id+LF stamp and per-receipt window scope; successor authorization stays issuer-side. |

There is no general integration reversal of the owner disposition. The principal mismatches are contradictory imported G02 conformance obligations, nested exception composition and incomplete joins between otherwise faithfully copied rules. Faithful copying alone does not establish specification sufficiency.

## Soundness of the six agent choices specifically requested

| Choice | Assessment |
|---|---|
| G20 transaction subset / OP_RETURN | A defensible **new supported-proof limit** after the earlier heuristic counterexample. P requires a parsed non-witness **serialization** with an output exactly `6a 20 || m`; it does **not** require 125 bytes, a fixed transaction version, or the observed two-op construction. The 125-byte corpus statement is evidence, not policy. Witness-stripped serialization of an actual SegWit transaction can satisfy the rule and gives its txid; it is the witness serialization that is excluded. A timestamp whose first double-hash is only a commitment is intentionally rejected. It gains no general calendar-availability guarantee. Resolve F08/F09 and add non-125-byte, multi-input/output and witness-stripped controls. |
| G33 optional unsigned issuer_record | Sound as diagnostics under the selected transport policy. Attacker changes may make a copy INVALID or remove the diagnostics entirely; they cannot authenticate issue observations or change δ/ε/k. This is an explicit custody/schema restriction, not an authenticity check. Absence is deliberately harmless. F03 is needed for missing internal fields; the policy is otherwise faithful to disposition. |
| G11 critical/noncritical type 16/33 | Recognizing these critical types is reasonable; ignoring their identity claims does not weaken SHA-256-bound key verification. Do not call that full RFC metadata processing, or let a library use them to choose a different key. Resolve payload/cardinality/consistency and prefix rules in F10. The critical bit itself is not the defect. |
| G13 part-line format | New and permissible packaging, not extraction. With safe paths, explicit inventory, verbatim blobs and an external catalog it can be unambiguous and avoids loading bundle policy. F13/F14 remain; the current ASCII/UTF-8/path recipe is not fully canonical. |
| G27 half-range/reversed/equal | Sound as explicit owner edge policy: half-range has no unique nearest lift; resolved inception > expiration cannot contain T_snap; equal endpoints describe a one-second inclusive window. It does not prove support for every long DNSSEC interval or remove the need to aggregate edge reasons. Time is historical T_snap, not wall clock. [RFC 1982 comparison](https://www.rfc-editor.org/rfc/rfc1982.html#section-3.2). |
| KSK-2017 start from memory | The day is confirmed by primary sources; midnight is not established as the actual switch/inception. Keeping it proposed is correct. F15 supplies the exact source/policy separation needed before freeze. |

## Contradictions with the governing artifacts

| Artifact / issue | Conclusion |
|---|---|
| A9 C4 and RB §5 versus dropped T_git clock gate | P is correct; RES prose/reason/vector residue is stale. F16. No clock gate should be restored. |
| A9 C5 versus E §7.1 “earliest” | A9's revised lowest-height reading governs. P implements it correctly. Change E's exact selection sentence, not only its publication/pre-commitment explanation, in §14.2 item 9. |
| A9 C6 versus partial/uncovered attestations | P correctly preserves all-supplied-header pin checks while ignoring nonqualifying no-header branches. A contradicted pinned branch fails the proof. This is explicitly registered, not a silent broadening. |
| A9.4 frozen algorithm policy versus E's registry / M5 | The installed policy and E codec registry must be distinguished. F01; preserving algorithm policy does not automatically rewrite E's signature grammar. |
| A9.5 append-only versus G09 open endpoints | The endpoint convention is delegated and visible; P correctly disclaims monotonic verdicts across different configs. F04 is an outcome-table conflict, not a demand for a stronger monotonic promise. |
| A9.5 full git path / E:685 “commit adds blob” versus P:971 | A9 requires authenticated path linkage, not proof of introduction. P's no-introduction check is reasonable, but E's “adds” overstates what is checked. Replace it with “whose tree contains the assertion blob at the profile path.” Add this to pending E edits. |
| E §8 single in-profile byte UNVERIFIABLE | P:178–179 repeats the stale statement although P now adds missing-member/spec/form cases. Qualify it as **codec-level**, as G01 already requires in E. It is not a reason to turn those adopted cases INVALID. |
| E rule O says codec ignores contents versus P G11 | A profile policy above the codec is permitted and labelled new; this alone is not a contradiction. Do not retrofit policy into codec vectors or infer generic keyring behavior. |
| E rule O legacy packet header versus actual signer | Already an explicit supported signature serialization. Reframing happens before stamp; no verifier normalization. No new defect shown here. |
| E number warnings / older exact-double wording | A9.8 governs; P correctly applies value preservation. These warnings are source drift, not an open number-rule decision. |
| RB repository-root algorithm/custody and release custody | P correctly keeps them separate and OPEN. RB does not establish YubiKey 2 possession, P-256 generation or release independence. |
| RB release rotation/recovery/loss OPEN | Missing from the detailed §14.2 accounting. F17. |
| A9 hybrid deployed-slot deadline | P's brief open custody item omits the 21 Oct constraint but does not override A9. Add the condition, F17. |

## Section 14.2 completeness: exact additions

Keep the ten existing items, with these amendments and additions. These are bounded to verifier sufficiency and already stated release/freeze work; they do not add V2 capabilities or move the V1 finish line.

1. **Expand item 2:** authenticated bootstrap, release-key rotation and bounded loss/compromise recovery; exact signed release preimage and verification format, with dependency pinning.
2. **Expand item 3:** complete machine-checkable trust schema and horizon/candidate aggregation, plus sourced precise endpoints; F04/F14/F15.
3. **Expand item 5:** hybrid deployed-slot evidence by 21 Oct, with any later choice limited to already passing implementations.
4. **Expand item 7:** exact tracked part inventory, assembler agreement, external catalog, preamble and dependency-manifest bytes/hashes, and A9 archival distribution; F13/F14/F17.
5. **Amend item 8:** withdraw/replace L-27/L-28 and the obsolete clock code; add the distinguishing cases named in F01–F14. Referencing the old L list as a whole is insufficient.
6. **Expand item 9:** E §7.1 lowest-height selection and E §7.2's “adds blob” wording; P's own codec-level qualification; account for any chosen codec/policy changes. The existing five-G list omits these.
7. **Add decision-function completion:** codec-known versus supported algorithm routing; explicit receipt/manifest equalities and codes; absent/present/diagnostics/descriptor exceptions; unknown-spec object-check dependencies; F01–F03/F12.
8. **Add DNSSEC/body completion:** exhaustive candidate/metadata failures, horizon and edge precedence, missing-zone skeleton, root signing, malformed TXT boundary, wildcard/global-candidate decision and body sort ties; F04–F07.
9. **Add proof completion:** varbytes/CompactSize, message-size outcomes, resource-count conventions, txid scope and selected-height path aggregation; F08/F09.
10. **Add signature completion:** complete advisory-subpacket policy, public-key validation, v4 hash-prefix choice, git armor aliases and possession/git code mapping; F10/F11.
11. **Add a genuinely total report-check table:** check ids, input dependencies, failure/unperformable mapping and tie keys, followed by multi-failure stable-six-field agreement cases; F11.

Release independence is load-bearing under the channel-capture adversary; the author must be told if it cannot be supplied. Ordinary evidence-format completion, reason ordering and the source corrections above can be decided by the owner within the stated profile scope, with change accounting. The three-document claim should then be stated as “sufficient with the frozen catalog, authenticated trust configuration and pinned normative dependencies,” rather than implying those external immutable inputs have disappeared.

## Validation evidence and limits

- Fresh read-only run: `PYTHONDONTWRITEBYTECODE=1 python3 formal/p8/vectors/check.py` returned **71/71 golden round-trips, 173/173 same-code rejections and 5/5 negative controls**. This validates the current P8 codec suite, not the new full profile or the proposed fixes.
- A targeted read of the codec's receipt function confirms that RECEIPT_COMMON_MISMATCH and RECEIPT_MANIFEST_MISMATCH are implemented there. Their existence is not a substitute for normative definitions in the requested three files; no policy was inferred from that code.
- Primary sources were checked for RFC 9580 subpacket/issuer semantics, RFC 4035 validation preconditions, RFC 1982 half-range comparison, Bitcoin transaction framing and IANA/ICANN KSK-2017 timing. A GitHub fetch for the OTS reader source failed; the profile's inline grammar, not that unavailable page, is the review basis. No new claim is made about today's corpus counts or calendar output stability.
- Distinguishing inputs above are rule-level constructions, not executed end-to-end V1 bundles. No service code, formal model, trust ceremony or new conformance suite was run. No signature or Bitcoin history break is demonstrated.
- Only `docs/reviews/v1-profile-r2/CODEX-REVIEW.md` was written by this review. Existing workspace edits were preserved.

Reviewed input SHA-256 (live snapshot):

| File | SHA-256 |
|---|---|
| docs/V1-PROFILE.md | `18d52ff92f2354b46507b52f2c8355759cf982d01cee491da04ecfd1bfb52e50` |
| docs/phase-0-prereg-amendment-9.md | `ff09f9b1ff6bb717bcca2c2f803eb8674f4beb2d28e88d5718320fe9b63c9f05` |
| formal/p8/ENCODING-V1.md | `d9ea82eb3e893fef865f124a612ecb6784932ea131559d792be8f01e597eb5ec` |
| docs/V1-OPERATIONS-RUNBOOK.md | `187695732e7773a2d749ae90092333815436efc6091942a3ca5a989426d4b376` |
| docs/reviews/spec-sufficiency/GAPS.md | `b95a123c2c7f4afdf9b80b1dd76082e5be53b6f546d9e6d68124b28c317c0b58` |
| docs/reviews/spec-sufficiency/RESOLUTIONS-DRAFT.md | `2d44d68906e3c950427d4f99f66703610c04b715cf42ba9ed787654c007ec7d1` |
| docs/reviews/spec-sufficiency/CODEX-REVIEW-RESOLUTIONS.md | `f8a024fd4cab4f63fe5ab28f57b02420a9c9babc7bedc611dd951b5af4213b63` |
| docs/reviews/spec-sufficiency/DISPOSITION-RESOLUTIONS.md | `9f523cbb4b5f7e0948795f918cd0f186ea787e35b51a8f145e80c5cb975cd70f` |
