# Independent V1 verifier instrument report

Date: 2026-10-14. Status: implemented differential instrument with explicit
fail-closed gaps; **not a fully conformant positive V1 verifier**.

**Current hybrid follow-up:** the instrument implements the requested
candidate supplement's rule R and exact ML-DSA-65 SPKI, catalog branch selection,
profile §8 EA-31 and the owner decision **Codec registry per installation**.
The catalog alg determines which supplements are registered for decoding;
fallback installations use opaque codecs for the hybrid pair. See the final
addendum for current validation and source
hashes. Earlier dated build results below are retained as history, not current
fallback-only limitations. No dated hybrid registration is asserted.

Initial implementation access record (the later addenda record their own reads):
all added code, tests, examples, documentation and the local Python environment
are under `prototype/indep-verifier/`. No other Tessera implementation,
formal model, vector file or independent-verifier review was read or imported.
The three authorized documents supplied the requirements, with Amendment 9
as governor. Workflow skill instructions were consulted separately; they were
not normative implementation evidence. No memory files were read.

## Outcome and material limitations

The requested CLI exists:

```sh
python verify.py --trust TRUST_CONFIG --bundle BUNDLE [--catalog CATALOG]
```

It prints the exact six stable fields as canonical JSON after successful
startup. T is determined independently of unrelated checks. INVALID dominates
UNVERIFIABLE, and the reported reason follows the expanded §15.7 row order,
then each row's tie order. No network is used at verification time.

There are **60 expanded numbered check ids** in the implementation ledger.
59 have executable checks; **14.4 is explicitly unperformable** because a
pinned SHA-1DC implementation/version is not supplied in these normative
inputs. Ordinary SHA-1 is used only to reconstruct the proposed links and
stamp target; it never establishes collision detection. With obtainable git
objects this build contributes the visible instrument-specific reason
`INDEPENDENT_SHA1DC_UNAVAILABLE`. Accordingly **a complete otherwise valid
bundle returns UNVERIFIABLE, never VALID_STRICT, in this build**. This prevents
unsafe acceptance but also prevents testing honest positive V1 acceptance.
It does not meet the registered false-reject bar and is not C-row discharge.

Actual authenticated trust configuration, frozen catalog/spec/vector hashes,
release authentication, final hybrid registration, and official pinned UCD /
ECMA dependency artifacts are not furnished by the allowed sources. These are
build/release inputs, not policy to infer from bundles. The checked-in release
is unprovisioned and refuses to emit a verdict until explicit local instrument
provisioning. That step does not prove release authenticity or custody.

**Recorded entries: 18**, A01–A18 in [AMBIGUITIES.md](AMBIGUITIES.md), including
missing normative build inputs and explicit choices where rejection mapping
or framing remains underdetermined. Resolved entries are marked, including A14
under the registry owner decision. They are instrument readings or records of
superseding owner decisions. Their implemented locations and normative locators are
listed there.

## Check-table coverage

"Implemented" means code exists and the synthetic complete evidence path was
exercised; it does not mean every rejection combination has been covered or
that conformance has been discharged.

| Check ids | Implementation | Evidence / limitations |
|---|---|---|
| 1.1–1.4 | Strict dispatch, size cap, profile, one layer, strict request only | Malformed JSON and unsigned dispatch tests; API accepts an explicit request input, CLI requests strict |
| 2.1–2.4 | JCS, member absence under typed parents, descriptor exceptions, closed recursive container schema | Noncanonical JSON, numeric member, missing git, null parent/descriptor, unsupported descriptor and malformed optional diagnostics |
| 3.1 | Exact A_sig tag/count/slot lengths, per-frame JSON/schema, per-slot codec | Classical: O/O; candidate pair: R/O (3309/1024); others opaque. Known unselected ids retain their own codecs |
| 4.1–4.2 | Manifest frame/schema and each common manifest digest | Synthetic possession and tuple path; altered digest/manifest alg tests |
| 5.1–5.2 | Installed-spec SPKI/v4 bodies and SHA-256 fingerprints, gated by catalog support (EA-31) | Fallback: explicit P-256 point validation. Candidate hybrid kms: exact 1974-byte ML-DSA-65 SPKI; every raw 1952-byte key well formed. Unsupported ids skip these rows |
| 6.1–6.3 | Slot fingerprints, common byte identity, issuer/alg manifest equalities | Independently signed disagreeing common content and tuple mismatch tests; equal canonical common bytes are exact substrings by the closed frame grammar |
| 7.1 | Single catalog-supported algorithm, separate from codec routing | Unknown id with codec-valid opaque signatures yields ALG_UNKNOWN; no invented hybrid id |
| 8.1–8.5 | Pinned issuer, spec id/catalog lookup, catalog object hashes, binding forms | Pinned-domain and binding-form tests; unknown spec with independently valid/invalid bundled objects |
| 9.1–9.5 | Rule-O policy/hash prefix/ECDSA; pure empty-context ML-DSA-65 over exact frame/manifest; strict FIPS gates | Unsupported ids retain possession codec only. Bad raw internals become SIG_INVALID / POSSESSION_INVALID; rule R has no OpenPGP policy |
| 10.1–10.3 | All supplied header pins, coverage, consecutive links | Conflicting pin, unused unpinned header, nonmonotone times and complete three-proof pool |
| 11.1–11.5 | Closed OTS wire parser and bounds; digest; all contradicted branches; lowest qualifying height; selected-height tx/OP_RETURN/merkle suffix and txid | Depth 256/257, ops 65536/65537, attestations 4096/4097, shortest LEB128, non-32-byte Bitcoin message, payload trailing data; digest/txid and incomplete unselected branch tests |
| 12.1–12.3 | Inclusive three-conjunct receipt timing with frozen ε/δ/k | Each individual failure tested; confirmation time may precede T |
| 13.1–13.7 | Snapshot envelope/cap; wire body and recovery skeleton; global wildcard restriction; own OTS shape; DNSSEC root/non-root candidate aggregation; fifteen-step TXT codec; snapshot conjuncts | Root-only/omitted groups, metadata and selector mismatches, parent-blocked local math, extra invalid root witness in either order, open horizon and finalized reliance, serial wrap/ambiguity/reversal, snapshot c3; algorithm 13 plus RSA 8, DS 2 plus 4 |
| 14.1–14.3 | Closed signed commit, dearmor/CRC/codec/policy, canonical tree parser | Synthetic signed P-256 commit and parser boundary tests |
| **14.4** | **Unperformable; no SHA-1DC detector** | **Explicit fail-closed reason, prevents complete-bundle acceptance** |
| 14.5–14.8 | SHA-1 commit→root→subtree→blob path, signed-id OTS target, repository interval/horizon, h_git+5<h_receipt | Positive git time later than both declared and receipt T still passes its implemented checks; later-height git proof rejects GIT_NOT_PRECOMMITTED |
| 15.1–15.2 | Manifest fingerprints match TXT, git blob byte-equal to TXT | Full synthetic dual-channel authority tuple, with no framing bytes on blob |
| 16.1 | Declared≥not-before and T≤not-after, inclusive; no T≥not-before test | Both exact boundaries and one-second violations; DNS window >90 days fails before this row |
| 17.1–17.4 | Raw spec/vectors/preamble bytes to each signed hash, dependency bytes to known catalog only | Independent object failure dominates missing evidence / unknown spec; unknown catalog entry never supplies a dependency-manifest comparison target |

`policy.py` implements §15.5's closed trust configuration, canonical numbers as
strings, unique/sorted entries, DNSKEY and DS cross-checks, public-key checks,
open/finalized periods and pins. The explicit local build enforces the compiled
hash allowlist and embeds the independently supplied catalog. Its optional
previous-config check enforces the append-only key/period/pin invariants without
making the runtime fetch previous state. Runtime enforces Unicode 16.0.0 and
an instrument-pinned implementation binary; equivalence to unpublished official
UCD digests has not been established.

DNSSEC candidate outcomes are aggregated once per required RRset. Eligible
supported candidates dominate failing extras; root horizon precedes finalized
interval/time/crypto failures. Non-root aggregation separately considers
absence, selector-matching unsupported paths, locally valid but parent-blocked
paths and the ordered failing-candidate classes. Candidate ordering is the
G35 tuple, not transport order. Global wildcard and body-framing restrictions
remain independent of candidate eligibility.

## Validation

Environment used: CPython 3.14.6, Unicode 16.0.0, cryptography 50.0.2, in the
local `.venv`. cryptography's packaged dependencies were installed there;
no global package installation was performed.

Command:

```sh
.venv/bin/python -m unittest discover -s tests -v
```

Result: **61 tests pass**. One test additionally exercises **180 seeded
malformed binary-member mutations**. Parser tests were initially run against
missing modules and failed; discovered selector, global-wildcard, RSA-width
and CLI/runtime issues were reproduced before their corrections.

The tests generate independent P-256 signatures, a delegated DNSSEC snapshot,
a signed git commit with raw trees/blob, three distinct non-witness Bitcoin
transactions and OTS operation paths, and synthetic pinned headers. A complete
fixture yields 145 passing subchecks, one explicit unperformable SHA-1DC check,
and no blocked expanded rows. These headers are fabricated test inputs, not
mainnet evidence or a timestamp claim.

The CLI is exercised in subprocesses with embedded and explicit catalog routes,
canonical stable output, unpinned config refusal and no stdout verdict on
startup failure. Tests restore the original release constants after temporary
local provisioning. `examples/` is a reviewable synthetic bundle/config/catalog;
[README.md](README.md) gives the commands to use it. Private keys are not saved.

## Known gaps and non-demonstrations

- Mandatory SHA-1DC is not implemented. This is the sole explicit unperformable
  check on the complete fallback fixture, and a material limitation.
- The hybrid supplement remains a draft in these inputs. Its requested candidate
  codecs/semantics are implemented and independently tested, without asserting
  dated registration, freeze authenticity or real deployed-signer evidence.
- Local hash provisioning is not an authenticated Tessera release. Release-key
  custody, bootstrap/rotation/recovery and actual archival trust sources remain
  external assumptions and open owner work.
- Unicode/ECMA implementation behavior is pinned for the instrument; no agreement
  run against the future official dependency manifest or frozen P8 vectors was
  performed. The repository vectors were deliberately not read.
- Tests cover the grammar families and representative mixed outcomes, not all
  candidate combinations, every table rejection code, every resource-size edge,
  all historical time endpoints or real mainnet/DNSSEC fixtures. There is no
  differential comparison against another Tessera implementation in this run.
- Spec, vectors, purpose preamble and dependency objects are hashed as raw bytes,
  never interpreted or executed as policy. No freeze object assembler or archival
  source-validation service is claimed; runtime does not need either to hash a
  presented object against independently frozen values.
- A9's issuer clock policy, custody, public publication, non-overlap of successive
  receipts, release signing and the human safe-decision test are not verifier
  checks. No result here establishes them.

A T printed with INVALID is not evidence of a valid service receipt. A later
presented proof may cause ISSUANCE_WINDOW; request the original issuer proof.
The verifier does not establish public publication of the git assertion.
Revocation and historical security remain NOT_EVALUATED; standing is
ABSENT/NOT_ISSUED_IN_PROFILE.

## Normative-source record

Only these Tessera artifacts supplied requirements (byte hashes below identify
this reading's working-tree snapshot, not a signed freeze):

- `docs/phase-0-prereg-amendment-9.md`: SHA-256 `ff09f9b1ff6bb717bcca2c2f803eb8674f4beb2d28e88d5718320fe9b63c9f05`.
- `docs/V1-PROFILE.md`: SHA-256 `493e72a89675da4d4aaa0bf318fd0c8690b4d947448f6118fdd7c96bbdea7316`.
- `formal/p8/ENCODING-V1.md`: SHA-256 `d9ea82eb3e893fef865f124a612ecb6784932ea131559d792be8f01e597eb5ec`.

External references consulted: [RFC 4034](https://www.rfc-editor.org/rfc/rfc4034), [RFC 4035](https://www.rfc-editor.org/rfc/rfc4035), [RFC 1982](https://www.rfc-editor.org/rfc/rfc1982), [RFC 9580](https://www.rfc-editor.org/rfc/rfc9580.txt), and the profile-cited [RFC 3110](https://www.rfc-editor.org/rfc/rfc3110.txt), [RFC 5702](https://www.rfc-editor.org/rfc/rfc5702.txt), [RFC 6605](https://www.rfc-editor.org/rfc/rfc6605.txt); [OpenTimestamps serialization reference](https://github.com/opentimestamps/python-opentimestamps/blob/master/opentimestamps/core/serialize.py); Bitcoin [transaction](https://developer.bitcoin.org/reference/transactions.html) and [header](https://developer.bitcoin.org/reference/block_chain.html) formats. Git signature documentation endpoints were attempted; the implemented closed grammar and object-id preimages come directly from the authorized profile and encoding document. External dependencies do not override the profile's supported-path restrictions.

## Addendum 2026-10-14: SHA-1DC hook (operator change, not by the independent builder)

Owner decision 2026-10-14 pinned the normative SHA-1DC detector: github.com/cr-marcstevens/sha1collisiondetection
at commit `a06f1adbe5522f3c939cd6a3f13d5ec7f4c1a988`, vendored under `prototype/vendor/sha1collisiondetection/`
(pin record and detector demonstration: `prototype/vendor/SHA1DC-PIN.md`). This supplies the input whose absence
A04 recorded; it is the only change to this instrument's verification logic for the differential run, and it
implements no reading of the profile.

- New `sha1dc.py`: runs the pinned `sha1dcsum` (binary SHA-256 pinned locally) on stdin over the git-framed bytes
  `"<type> <len>\0" ‖ body` and returns the detector's prescribed collision return (`*coll*` marker).
- `verify.py` row 14.4: when the pinned binary is present, each present object (tie order commit, root tree, sub
  tree, blob) contributes pass or `INVALID / GIT_SHA1_COLLISION` (profile §15.4, §15.7 row 14.4). If the pinned
  binary is absent or a detector call fails, the original `UNVERIFIABLE / INDEPENDENT_SHA1DC_UNAVAILABLE` remains.
  Ids for row 14.5 are still computed with hashlib SHA-1; they equal SHA-1DC's output whenever 14.4 passes.
- Tests: `tests/test_verifier.py` now expects `VALID_STRICT / OK` for the complete synthetic bundle when the
  detector is built (the old expectation otherwise), plus one test that the hook frames commit, both trees and the
  blob and maps a detection to `GIT_SHA1_COLLISION`. 62 tests pass.
- Consequence: the statements above that "a complete otherwise valid bundle returns UNVERIFIABLE, never
  VALID_STRICT" and "14.4 is explicitly unperformable" no longer hold when the pinned detector is built; A04 is
  resolved by the owner pin. Note that SHAttered's raw collision is detected but the same file git-framed as a blob
  is not (the header misaligns its blocks), so no available fixture exercises a positive detection end to end.

## Addendum 2026-10-14: independent diff-1 corrections

Read the revised profile only, plus this instrument's own code and tests; no
conformance, differential or other implementation source was read. A lightweight
memory-registry search found no verifier-specific guidance and supplied no
implementation evidence. The initial report's no-memory statement describes
its original build. All edits in this follow-up remain within this directory.
Profile snapshot SHA-256:
`89eb8d50c660163133e2c658dd1158ac8ec54a832a3dd9d752ed4f143a57cb0a`.

- §15.3 point 3, OWNER diff-1 F-1: inspect RRSIG signer-name bytes during body
  parsing. Observable uppercase ASCII or compression pointers now reject as
  INVALID / SNAPSHOT_FORMAT before witness aggregation, even beside a valid
  witness. Other malformed supported RDATA remains candidate-local.
- Coverage, OWNER diff-1 F-3: row-2.4-invalid headers already were excluded by
  schema extraction. Added regression tests for invalid heights and malformed
  values, including selected receipt, snapshot and git heights. Remaining
  entries determine anchor availability and T; invalid entries contribute only
  CONTAINER_SCHEMA and cannot introduce pin/coverage/link failures.
- G35: malformed RRSIG sorting now preserves independently readable tag,
  inception, expiration and signature fields. Only unavailable fields fall back
  to zero/empty, followed by raw RDATA and key RDATA. The same extraction is
  used for malformed-candidate failure ordering at root and non-root groups.
  The previously used all-zero tuple could reject correctly serialized bodies.

Validation: `.venv/bin/python -m unittest discover -s tests -q`:
**66 tests passed**, including four new regression methods. Before the fixes,
noncanonical signer tests demonstrated acceptance beside a valid witness and
three readable-field ordering cases rejected correctly sorted bodies. Header
regressions passed before any production change. A12 is now owner-resolved;
A06 records the corrected per-field fallback. No differential comparison was
run in this follow-up, and no conformance or discharge claim is made.

## Addendum 2026-10-14: requested hybrid branch and EA-31

Historical implementation record. The global codec-registration interpretation
in this addendum is superseded by the final installation-registry addendum.

All reads for this change were confined to this instrument's own files, the four
authorized Tessera specifications below, and `prototype/differential/ADAPTER.md`
for the CLI/catalog interface. External normative references consulted were
[FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) and
[RFC 9881](https://www.rfc-editor.org/rfc/rfc9881.html). The permitted third-party
cryptography API was inspected in the instrument's existing local environment.
No conformance code, differential code, formal vectors, other implementation
source, review/decision files linked from the supplement, or memory files were
read. All edits and temporary provisioning artifacts stayed within this directory.

**Behavior.** The codec registry contains the exact pair id
`KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256`, alongside the classical id.
Each slot uses its own frame's alg and slot. For pair/kms, rule R accepts exactly
3309 raw bytes without inspecting them: zero is SIG_EMPTY, shorter nonzero is
SIG_FORMAT, longer is LENGTH_CAP. Pair/gpg still uses rule O with cap 1024.
Other ids retain the opaque codec and cap 65536. Codec checks apply even to an
unselected known branch.

The catalog independently selects semantic support; unknown spec lookup does
not alter algorithm selection. Key format and fingerprint binding run only for
catalog-supported receipt slots (EA-31). Hybrid kms requires exactly the
supplement's 22-byte prefix followed by 1952 raw key bytes: DER SPKI with
id-ml-dsa-65, absent parameters and zero unused bits, total 1974. Every raw
1952-byte key is well formed. The fingerprint is `spki-sha256:` plus lowercase
hex SHA-256 of the entire exact SPKI. Supported fallback receipts still reject
ML-DSA SPKI as KEY_FORMAT. Unsupported algorithms skip key format/binding,
signature policy/math and possession policy/math, contributing ALG_UNKNOWN;
independent schema, codecs, manifest/common equalities and hashes still run.
Honest fallback/hybrid receipts shown to the other installation are
UNVERIFIABLE / ALG_UNKNOWN, with no KEY_FORMAT contribution.

Rule R verifies pure ML-DSA-65, explicit empty context, over exact `F` or
`F_manifest`; no prehash, trailer, normalization, received μ or signing-mode
input is accepted. Before the backend, independent FIPS gates enforce bounded
nondecreasing hint counts, strictly increasing indices within each polynomial
(duplicates rejected), zero unused hint padding and `|z| < 2^19 − 196`.
The backend performs the lattice verification. Internal defects become
SIG_INVALID / POSSESSION_INVALID, preserving the length-only codec. Rule R's
OpenPGP-policy rows pass vacuously; rule O and repository signing remain classical.

**K-R is an assumption, not a verifier check.** The kms key is dedicated to
V1 attest/manifest frames, pure mode, empty context; the issuer computes μ using
this key's raw public key and uses EXTERNAL_MU for both operations. Exclusive
key use and the issuer/IAM restriction cannot be inferred from a receipt.
RAW and EXTERNAL_MU signatures over the same frame are indistinguishable to
verification; this instrument certifies neither the signing API path nor IAM.
K-O remains the separate gpg key-use assumption. Neither is discharged here.

**Interpretation record.** A03 is superseded. A14–A18 in AMBIGUITIES.md record
draft-versus-requested codec registration scope, unsupported codec-versus-semantic
evaluation, per-slot/missing-receipt prerequisites, raw policy-row mapping, and
catalog provisioning/unknown-spec behavior. The fixed crypto parameters, SPKI,
fingerprint and K-R status were explicit, not guesses. The draft remains a draft;
compiling its codecs does not date or authenticate registration.

**Validation.** Existing environment: CPython 3.14.6, Unicode 16.0.0,
**cryptography 50.0.2**, packaged backend **OpenSSL 4.0.3 (29 Sep 2026)**.
The existing `requirements.txt` already pins cryptography 50.0.2; no dependency
installation or pin change was needed. The local owner-pinned SHA-1DC hook was
available during this run; its implementation was neither inspected nor changed.

```sh
.venv/bin/python -m unittest discover -s tests -v
```

Result: **83 tests pass**, comprising the prior 66 and **17 new hybrid methods**.
The first new-test run failed (11 assertion failures, 3 errors) on missing
hybrid codec/key/verification behavior and unconditional key evaluation; after
implementation all pass. Tests independently generate ML-DSA/P-256 keys,
external-μ signatures over frames larger than 4096 bytes, signatures over the
manifest, and the existing synthetic DNS/git/OTS evidence. Both selected
branches pass; both wrong-installation directions give ALG_UNKNOWN. The hybrid
CLI passes with embedded and explicit catalog routes, with release constants
restored after testing.

Rejections cover exact raw length boundaries within anchors and possession,
wrong slot codec, exact SPKI alternatives (P-256/44/87, NULL parameters,
unused bits, DER length defects, bare/PEM/truncated/trailing), mismatched
fingerprints, wrong frames/manifests, nonempty context, HashML-DSA/SHA-256,
missing `00 00` in μ, strict hints/padding/counts/z, unknown spec, independent
hash failure under unknown alg, mixed pair ids, and another valid signature
failing the original anchored tuple. A permissive mock backend confirms every
strict encoding gate stops verification before the library is called; repeated
indices across different polynomials remain allowed. Malformed hints also fail
the complete receipt/possession paths with the required codes.

This is independently authored profile/codec evidence, using one shared
third-party crypto backend for test signing and verification. It is not two
independent ML-DSA implementations, FIPS certification, a real KMS capture,
differential agreement, formal discharge, or proof of all V1 conformance.
The retained release-authentication and frozen-dependency limitations still apply.

Source snapshot SHA-256 (working-tree bytes, not signing/freeze hashes):

| Authorized source | SHA-256 |
|---|---|
| `docs/phase-0-prereg-amendment-9.md` | `ff09f9b1ff6bb717bcca2c2f803eb8674f4beb2d28e88d5718320fe9b63c9f05` |
| `docs/V1-PROFILE.md` | `78dc6be38384895092829424fca8a3cd871910cdf9c35f43620899bbd5780519` |
| `formal/p8/ENCODING-V1.md` | `d9ea82eb3e893fef865f124a612ecb6784932ea131559d792be8f01e597eb5ec` |
| `formal/p8/HYBRID-SUPPLEMENT-DRAFT.md` | `4e8e675326ed59e0af43e6f5372f17db14ca0504b533cb3bb7325e88fca8549f` |

## Addendum 2026-10-14: codec registry per installation, differential run 4

Implements the owner decision in `docs/V1-PROFILE.md` §8, lines 900–905.
The earlier global registry was wrong for fallback installations: compiled
hybrid code imposed rule R/O before unsupported-algorithm semantics could run.
That interpretation and A14's earlier reading are superseded, visibly retained
above as history.

`codec.registered_codecs(catalog_alg)` returns the ENCODING-V1 classical baseline
plus the hybrid pair only when the installed catalog's alg is the exact pair id.
`verify_bundle` derives this immutable registry before decoding the receipt and
passes it to both receipt and possession codecs. Each slot still selects its
rule using its own frame's alg; possession uses the manifest alg when no receipt
decodes. Defaults are baseline-only. No process-global registration state,
bundled spec lookup or bundle bytes can register a supplement.

A fallback installation treats both slots of a hybrid receipt as opaque:
nonempty lengths through 65536 pass without inner decoding, and semantics
contribute `UNVERIFIABLE / ALG_UNKNOWN`. Empty signatures remain `SIG_EMPTY`;
lengths above 65536 are `INVALID / LENGTH_CAP`, including a declared over-cap
length with absent bytes. A declared in-cap extent with absent bytes is
`TRUNCATED`. Independent invalid findings still dominate ALG_UNKNOWN.
A hybrid installation retains both codec ids: classical frames use rule O
before ALG_UNKNOWN for unsupported classical semantics, while hybrid frames
use the registered rule R/O and supported semantics. Unknown catalog ids add
no supplement and cannot manufacture semantic support.

**Validation.** The starting suite passed **83 tests**. Five initial regression
methods produced **21 failing assertions** under the global registry, covering
opaque receipt/possession slots, cap-before-truncation ordering, unknown spec
lookup and repeated installation selection. After the change, the full suite
passes **90 tests**, including seven added methods and revised existing cases:

```sh
.venv/bin/python -m unittest discover -s tests -v
```

Coverage includes both slots at lengths 0, 1, 3308, 3310, 65536 and 65537;
freshly stamped mutated receipt tuples preserve independently established T;
unsupported key/signature/possession semantics stay blocked. Both classical
slots still enforce their receipt and possession codecs in a hybrid
installation. Direct decoders default to baseline-only; possession parsing
retains installation registration when receipt decoding fails. Alternating
classical, hybrid and unknown catalog selections shows no registration leakage.
CLI tests exercise both embedded and explicit authenticated catalog routes for
an honest hybrid receipt, a 3308-byte possession proof and an over-opaque-cap
proof under both installations. Release constants are restored by the tests.

**Read boundary and scope.** Requirements for this change came only from A9,
V1-PROFILE, ENCODING-V1 and HYBRID-SUPPLEMENT-DRAFT, alongside this instrument's
own code/tests/docs. No other Tessera implementation, conformance/differential
source, vectors or review artifacts were consulted. Workflow skills and a brief
governance-memory lookup were consulted separately; memory supplied no codec or
implementation evidence. All edits and test provisioning stayed under
`prototype/indep-verifier/`. REPORT, AMBIGUITIES and the README registry paragraph
now describe the installation-specific behavior. No differential comparison,
formal discharge, actual frozen catalog or dated supplement registration is
claimed; existing build/release limitations remain.

Source snapshot SHA-256 (working-tree bytes, not signing/freeze hashes):

| Authorized source | SHA-256 |
|---|---|
| `docs/phase-0-prereg-amendment-9.md` | `ff09f9b1ff6bb717bcca2c2f803eb8674f4beb2d28e88d5718320fe9b63c9f05` |
| `docs/V1-PROFILE.md` | `738295af85f5e461bf74cc6b67f129ccc8d3a7ad6e619235be830b86cee15be8` |
| `formal/p8/ENCODING-V1.md` | `d9ea82eb3e893fef865f124a612ecb6784932ea131559d792be8f01e597eb5ec` |
| `formal/p8/HYBRID-SUPPLEMENT-DRAFT.md` | `4e8e675326ed59e0af43e6f5372f17db14ca0504b533cb3bb7325e88fca8549f` |
