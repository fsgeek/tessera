# V1 dependency manifest and its sources (profile section 14.2 item 15)

> **Status: OWNER WORKING ARTIFACT, 2026-10-19** (Claude Opus 5.5, owner instance). Builds the real dependency
> manifest that profile sections 9 and 15.6 specify, replacing the TEST stand-in in `prototype/e2e/freeze.py`.
> It edits no existing file. Every choice of edition below that the profile does not already make is an **owner
> choice**, listed under "Choices made here". Scope follows `docs/decisions/2026-10-19-horizon-cost.md`
> recommendation 3: pin editions and digests for everything, archive only the few at risk, disclose the rest.

## Files

| File | What it is |
|---|---|
| `dependency-manifest.json` | The manifest: `{"entries":[...],"format":"tessera-v1-deps/1"}`, 44 entries sorted by `id`, every entry with the nine section 15.6 fields. RFC 8785 canonical. No `TEST` anywhere. sha256 `20020475a8ef852fbd3d9331b370a3161e925a44cddf83c8f51d26be2ac9e063`, 41181 bytes. |
| `gen_manifest.py` | The generator. It read the downloads from a scratch directory (`dl/`, not kept); entry text lives in the script. |
| `sha1dc.SHA256SUMS` | sha256 of the six pinned SHA-1DC source files in `prototype/vendor/sha1collisiondetection/`; its hash is the `sha1dc` entry digest. |
| `archive/` | The at-risk sources (below), plus errata evidence. |

**Canonical-form check.** `parse_json(raw, canonical=True)` from `prototype/indep-verifier/codec.py` accepts the
bytes (it raises `JSON_NONCANONICAL` unless the bytes are their own JCS form). Independently, `rfc8785` 0.1.4
(`prototype/` uv project) gives `rfc8785.dumps(json.loads(raw)) == raw` → True.

## What is archived, and why

Archived (at risk of disappearing or changing, and lawful to redistribute):

| Archive path | Entry | Why it is at risk |
|---|---|---|
| `archive/bitcoin-core-formats/src/...` + `SHA256SUMS` | `bitcoin-core-formats` | No standards body. The header, txid, merkle and CompactSize formats are defined only by Bitcoin Core source, hosted on GitHub. MIT. |
| `archive/bip-0144/bip-0144.mediawiki` | `bip-0144` | BIP text on GitHub only; defines the SegWit marker V1 rejects. |
| `archive/gitformat-signature/gitformat-signature.adoc` | `gitformat-signature` | git documentation; its file was renamed once already (`.txt` to `.adoc`). GPL-2.0. |
| `archive/git-object-format/git/fsck.c`, `.../progit2/.../objects.asc` + `SHA256SUMS` | `git-object-format` | No formal specification of git objects exists; the tree ordering and mode rules live in git's `fsck.c`. Pro Git is CC BY-NC-SA 3.0 (non-commercial redistribution only). |
| `archive/opentimestamps/opentimestamps-0.4.5.tar.gz` | `opentimestamps` | No OTS specification exists; the reference reader is a small project. The sdist's sha256 equals PyPI's published digest. LGPL-3.0. |
| `archive/errata/*-potential-updates.xlsx` | `fips-186-5`, `fips-204`, `sp-800-186` | NIST's errata lists are mutable spreadsheets ("Last updated 7/31/2026" for FIPS 204); the errata dispositions were made against these bytes. |
| `archive/errata/rfc-errata-extract.json` | every `rfc*` entry | **Derived**, not as served: the records for the 24 RFCs, cut from `https://www.rfc-editor.org/api/v1/errata.json` (fetched 2026-10-19T23:30:47Z, 11.7 MB, not kept), JCS-encoded. The evidence for the RFC errata dispositions. |

Already archived elsewhere: SHA-1DC is vendored at `prototype/vendor/sha1collisiondetection/` and its six source
digests match `prototype/vendor/SHA1DC-PIN.md` (re-checked today). Not duplicated.

Not archived (pinned by edition and digest, disclosed):
- **RFCs** (22 RFCs plus RFC 6840 and RFC 8017): immutable text, permanently published by the RFC Editor. Three of
  them (4034, 5011, 9718) are byte-identical to the copies in `formal/trust-sources/raw/`.
- **NIST FIPS 180-4, 186-5, 202, 204, SP 800-186**: DOI-backed, stable URLs. Public domain.
- **Unicode 16.0.0 UCD files and UAX #15 rev. 56**: versioned, permanent paths.
- **ECMA-262 10th edition** (14 MB PDF): Ecma keeps every edition. Borderline: the URL RFC 8785 cites
  (`www.ecma-international.org/ecma-262/10.0/index.html`) has already moved once (it redirects to
  `262.ecma-international.org/10.0/`). The profile restates the ES algorithm and has vectors N-01 to N-22, so loss
  is survivable.
- **IEEE 754-2019**: paywalled, not redistributable; `digest_sha256` is null.
- **GnuPG 2.4.4 source** (7.9 MB): gnupg.org keeps old releases.

**Distributed with the verifier versus retrieved.** Only SHA-1DC is distributed with the verifier (vendored source,
built at install). The archived files above travel with the spec sources in this repository. Everything else is
retrieved by reference. The `redistribution` field of each entry says which (section 15.6 has no separate field).

## Fetch record (UTC; sha256 of the bytes as served)

All fetched 2026-10-19 with `curl -L`; the time is the end of the download. For multi-file entries the digest is
of the `SHA256SUMS` listing.

| Entry | URL | Fetched | sha256 |
|---|---|---|---|
| `bip-0144` | https://raw.githubusercontent.com/bitcoin/bips/130b8e0fa7f30fa45532f080b87b8db27a79e46e/bip-0144.mediawiki | 23:31:42Z | 7a8e28a18939bf4523b11170eb7988559db3937bd5f49d0afd210e5cb7d6963b |
| `bitcoin-core-formats` | https://raw.githubusercontent.com/bitcoin/bitcoin/9be056a8a72b624dae9623b2f7bded92c2a21c91/src/... (7 files) | 23:31:39Z | dd2648773b4f16f00688616fc644de330301dfc985dd2072428a9ddb7db93b92 |
| `ecma-262` | https://ecma-international.org/wp-content/uploads/ECMA-262_10th_edition_june_2019.pdf | 23:31:05Z | d68f9898a104c911352e0dc4f6e6f5370d188c0344d75e7a7b3642cf663f57f9 |
| `fips-180-4` | https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf | 23:30:57Z | 0455b406d89648d20cbde375561e19c245b9815e894164c2670772e3d54deb82 |
| `fips-186-5` | https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-5.pdf | 23:30:58Z | fbb9c7c2ba442f03c57b63b43c888311903c9d0f29f89b06efdebd9b619140c5 |
| `fips-202` | https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf | 23:31:00Z | 1592607831ff0908cc590632ce371c6c95e94025bb1a0c8ae90a4d0ec1ed025e |
| `fips-204` | https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf | 23:30:59Z | 57239b9f84c03227eda3ca0991204dc7764c79af9ce2e6824eda774918d46b6b |
| `git-object-format` | https://raw.githubusercontent.com/git/git/a018953688f1b10bddf91bff8747068f5f4746a4/fsck.c and https://raw.githubusercontent.com/progit/progit2/a013e3230a1207cfa5ae94d28ba7d2021063c337/book/10-git-internals/sections/objects.asc | 23:31:42Z | 40a1fd5254f3057508feeaa188a1dcf9b2ca0c2d61ad72015b33804903997fe2 |
| `gitformat-signature` | https://raw.githubusercontent.com/git/git/a018953688f1b10bddf91bff8747068f5f4746a4/Documentation/gitformat-signature.adoc | 23:31:42Z | e99e9de49bb4d7566199956a44e886643faaf68333974ed055099a310595daf4 |
| `gpgv` | https://gnupg.org/ftp/gcrypt/gnupg/gnupg-2.4.4.tar.bz2 | 23:31:50Z | 67ebe016ca90fa7688ce67a387ebd82c6261e95897db7b23df24ff335be85bc6 |
| `ieee-754` | doi:10.1109/IEEESTD.2019.8766229 (paywalled; not fetched) | — | null |
| `opentimestamps` | https://files.pythonhosted.org/packages/fb/2a/5f19420091d137e5a4c49cbe3de1964a3741d3264bad5e0a528e54aaef15/opentimestamps-0.4.5.tar.gz | 23:31:48Z | 56726ccde97fb67f336a7f237ce36808e5593c3089d68d900b1c83d0ebf9dcfa |
| `rfc1035` | https://www.rfc-editor.org/rfc/rfc1035.txt | 23:30:39Z | d14ae809fc9b41bbcae26bb38c937c9515808b944f3252b00de9fe0e95f4fdfb |
| `rfc1982` | https://www.rfc-editor.org/rfc/rfc1982.txt | 23:30:39Z | b22fa98e10e66340804f50fe22c7c9299f66dea7ed90cac17800a4bccda7dc15 |
| `rfc2181` | https://www.rfc-editor.org/rfc/rfc2181.txt | 23:30:39Z | c00423dc0b34d025e72b977a08c71f4357977e273d22670f29954109ac0f9c70 |
| `rfc3110` | https://www.rfc-editor.org/rfc/rfc3110.txt | 23:30:39Z | ccb56821a1d9edc9dc5ae14d8e6c6c18836cde0a8785d3847ba0e43c1c397b21 |
| `rfc3339` | https://www.rfc-editor.org/rfc/rfc3339.txt | 23:30:38Z | 9ab2b8864a85dca73a88f49b0927bc7bc85f596926e4fd1890905777924e700a |
| `rfc4034` | https://www.rfc-editor.org/rfc/rfc4034.txt | 23:30:39Z | 6c32963b76808ec4e5f1282b5e13c5216df4670d21e1590bf29af4066f49b355 |
| `rfc4035` | https://www.rfc-editor.org/rfc/rfc4035.txt | 23:30:40Z | 8978b120636c69b2080b12768266ec48cd4c0879583310863a62f7c409908084 |
| `rfc4509` | https://www.rfc-editor.org/rfc/rfc4509.txt | 23:30:40Z | b39ee3cf95b141215e8be464fb32f7f7c8b3606738911550446f47bd0ff4d8e9 |
| `rfc4648` | https://www.rfc-editor.org/rfc/rfc4648.txt | 23:30:39Z | 84e14418f795d503be5f34bf23ce4ebaa119e9ec7c9f667d8caeb111385b178f |
| `rfc5011` | https://www.rfc-editor.org/rfc/rfc5011.txt | 23:30:40Z | e00a848ca0fb6da1925ea828ea893a746f4d02528d70fedaab44b447c0778ed1 |
| `rfc5280` | https://www.rfc-editor.org/rfc/rfc5280.txt | 23:30:42Z | a2f2628c0a83b873fc4786abd921f9b2c02395954b655d190bf16b831633345d |
| `rfc5480` | https://www.rfc-editor.org/rfc/rfc5480.txt | 23:30:42Z | 593bf29fd0da2ff8b903c3ebf1c9d189a770039159e2ba46a0c3b91355037f26 |
| `rfc5652` | https://www.rfc-editor.org/rfc/rfc5652.txt | 23:30:41Z | dbd209ae7844031f51722c4d9e2d1fa3fff3081319851d581f914f5f0147f918 |
| `rfc5702` | https://www.rfc-editor.org/rfc/rfc5702.txt | 23:30:40Z | 04871fb7e95f0ee18298bea6960527579f2a892d9c1a2658b6c3f21b3ec03446 |
| `rfc6605` | https://www.rfc-editor.org/rfc/rfc6605.txt | 23:30:41Z | fa9b6f1fb4fb8426bdb0c56c134af3f1d962414082e3953f1c4e4e861ff459ee |
| `rfc6840` | https://www.rfc-editor.org/rfc/rfc6840.txt | 23:32:19Z | 32c2a8c755f37f3467b4ca098fc0283efe53d2648e93c3ae966cfa390a50bfaf |
| `rfc7493` | https://www.rfc-editor.org/rfc/rfc7493.txt | 23:30:41Z | a44ccf1451a7bf4f4bbb78b39e10ed0e9a27ff2ee5b639c6458042b5a7197062 |
| `rfc8017` | https://www.rfc-editor.org/rfc/rfc8017.txt | 23:33:35Z | 1e72dc473d18df3fc5598cdc12795a9f18f36f1aef15abc23a55eb0d58151d11 |
| `rfc8259` | https://www.rfc-editor.org/rfc/rfc8259.txt | 23:30:38Z | 61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7 |
| `rfc8785` | https://www.rfc-editor.org/rfc/rfc8785.txt | 23:30:38Z | 63d52294eb0e3f0014174288186d388b4ddbf2c67d1ce8af1d9726eb0c3ab240 |
| `rfc9102` | https://www.rfc-editor.org/rfc/rfc9102.txt | 23:30:42Z | 631fd65e4d50a0375589e64fc88dcca888e8b6557de4a0e3593c6a88db682cad |
| `rfc9580` | https://www.rfc-editor.org/rfc/rfc9580.txt | 23:30:38Z | 36540e57b63d24c0b17be0748b704bdeed3d643ce99a4fb1abb6469c1eb1ff18 |
| `rfc9718` | https://www.rfc-editor.org/rfc/rfc9718.txt | 23:30:41Z | 6b52bed66d8d7f26a2b4701d644a22c5d080666cd58509afcac409e1034fc475 |
| `rfc9881` | https://www.rfc-editor.org/rfc/rfc9881.txt | 23:30:41Z | 20ae3b519bc69e32989fa6e625ab8746453eddf457e20ddbfd79d841a44237a2 |
| `sha1dc` | vendored, `prototype/vendor/sha1collisiondetection/` (commit a06f1adb…a988) | 2026-10-14 (SHA1DC-PIN.md) | b132968a97ef3c9117376d9430d6d2a8dc673141b1d806ccc2c5e6908bc86d3c |
| `sp-800-186` | https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-186.pdf | 23:31:01Z | 53c7cf3340528aaa0a7bbeaef947f2099568192367d4341a7d4abceb55f78432 |
| `uax-15` | https://www.unicode.org/reports/tr15/tr15-56.html | 23:31:21Z | 29985d3b649dd8629a63bd8fcb72628b806e39578db8639bc0429f340087b70e |
| `ucd-compositionexclusions` | https://www.unicode.org/Public/16.0.0/ucd/CompositionExclusions.txt | 23:31:20Z | 89e83cf9cc8bef6c1f8bf77e42cf6f0341dfa42e66261f4dbe9b492e7a23c8ee |
| `ucd-derivedgeneralcategory` | https://www.unicode.org/Public/16.0.0/ucd/extracted/DerivedGeneralCategory.txt | 23:31:21Z | 7676ab755a41ef82108460238569e60ad65c191ddafe61b36c6765ec1353f293 |
| `ucd-derivednormalizationprops` | https://www.unicode.org/Public/16.0.0/ucd/DerivedNormalizationProps.txt | 23:31:20Z | 4d4c03892dea9146d674b686e495df2d55a28d071ac474041d73518f887abddc |
| `ucd-normalizationtest` | https://www.unicode.org/Public/16.0.0/ucd/NormalizationTest.txt | 23:31:20Z | d811971453e7075e1ad56fb1b301eece5aa80757b81f6156e74a1bfb3ae5ceb1 |
| `ucd-unicodedata` | https://www.unicode.org/Public/16.0.0/ucd/UnicodeData.txt | 23:31:20Z | ff58e5823bd095166564a006e47d111130813dcf8bf234ef79fa51a870edb48f |

Errata evidence fetched for the dispositions: `fips186-5-potential-updates.xlsx` (23:32Z),
`fips-204-potential-updates.xlsx` (23:32Z), `sp800-186-potential-updates.xlsx` (23:32Z), all from
`https://csrc.nist.gov/files/pubs/.../docs/`; CSRC publication pages read for planning notes.

**Check run on the Unicode pin.** The verifier's Python (3.14.6, `unicodedata.unidata_version == '16.0.0'`) agrees
with the fetched files: 19,965 `NormalizationTest.txt` lines, 0 NFC mismatches; 0 code points where
`category == 'Cn'` differs from `DerivedGeneralCategory.txt`.

## A9's eight entries, mapped

| A9.1 "Bundle" name | Manifest entries |
|---|---|
| RFC 8785 | `rfc8785`, `ecma-262`, `ieee-754`, `rfc7493` |
| OpenPGP | `rfc9580` (the profile pins RFC 9580, not RFC 4880) |
| The signature algorithms in use | `fips-186-5`, `sp-800-186`, `rfc5480`; hybrid: `fips-204`, `fips-202`, `rfc9881` |
| SHA-256 | `fips-180-4` (6.2) |
| SHA-1 for git object linkage | `fips-180-4` (6.1), `sha1dc`, `git-object-format`, `gitformat-signature` |
| The DNSSEC algorithms in the chain | `rfc5702`, `rfc3110`, `rfc8017` (alg 8); `rfc6605` (alg 13, DS 4); `rfc4509` (DS 2); core `rfc1035`, `rfc1982`, `rfc2181`, `rfc4034`, `rfc4035`, `rfc6840`, `rfc5011`; trust sourcing `rfc9718`, `rfc5652`, `rfc5280`; `rfc9102` informative |
| OTS | `opentimestamps` (profile section 15.2 is the normative grammar) |
| Bitcoin headers | `bitcoin-core-formats`, `bip-0144` |

Profile section 9 extras: Unicode → five `ucd-*` entries and `uax-15`; RFC 8259 → `rfc8259`; RFC 3339 →
`rfc3339`; RFC 4648 → `rfc4648`; the release-signature dependency (item 15) → `gpgv`.

## Choices made here (owner level; none changes a registered sentence)

1. **One entry per document**, not per A9 concept, so that each entry has one edition and one digest. Multi-file
   sources (Bitcoin Core, git) take the digest of a `SHA256SUMS` listing.
2. **ECMA-262 10th edition (June 2019), section 7.1.12.1 NumberToString with Note 2**: the edition RFC 8785
   itself cites.
3. **Bitcoin Core v31.1** (commit 9be056a8…) as the reference for formats the profile restates in full.
4. **git v2.56.0** (commit a0189536…) for `gitformat-signature` and `fsck.c`; Pro Git at progit2 a013e323….
5. **GnuPG 2.4.4** for `gpgv`, because it is the version observed. R3/R6 have not pinned a version yet.
6. **Errata**: verified RFC errata that touch a section used are adopted where they clarify (8785 #7920, 3110
   #2811, 4034 #4552, 8259 #7600/#7603/#7383, 1035 #2130); NIST "potential updates" are not official changes, and
   none changes a verification outcome. RFC 8017 and RFC 5280 errata were counted, not reviewed one by one (stated
   in their entries).
7. **Excluded**: FIPS 205 (cited in ENC rule R as a class, not used by the registered hybrid branch); ITU-T X.690
   (ENC and the supplement fix the DER bytes exactly); Python, `cryptography` and other wheels (R6's release lock,
   not normative standards).

## Where the profile's section 9 / 15.6 text and what I found disagree

Not edited here; for the owner.

1. **Section 15.6 "The entry list is section 9's."** Section 9 names concepts (A9's eight) mixed with documents,
   and its "Extra standards" list groups several RFCs per line. A per-document manifest cannot be "section 9's
   list" literally. The mapping above is the correspondence.
2. **Section 9's list omits standards the frozen text uses:** RFC 8017 (RSASSA-PKCS1-v1_5, needed for algorithm-8
   RRSIGs; RFC 5702 cites its predecessor RFC 3447); FIPS 202 (SHAKE256, called directly in ENC rule R); SP 800-186
   (named in profile section 8, not in section 9); RFC 9881 (cited by ENC and the supplement; section 9 says only
   "the supplement's SPKI encoding"); RFC 7493 and IEEE 754 (both in ENC section 1.1); RFC 6840 (updates RFC 4034
   section 6.2, which section 6.1 uses); RFC 5280 (RFC 5652 alone does not verify the `.p7s` certificate path).
   All are added.
3. **"ECMA-262 Number::toString (pinned edition)"** (sections 9 and 10): no edition is named anywhere. In the
   edition RFC 8785 cites (ES2019), the operation is called NumberToString (7.1.12.1); "Number::toString" is the
   ES2020+ name (6.1.6.1.20). The output is the same. The profile's name and the pinned edition's name differ.
4. **Section 15.6 has one `digest_sha256` per entry** and does not say what to hash when canonical bytes are many
   files (Bitcoin Core, git, SHA-1DC) or when only an HTML and a PDF form exist (ECMA-262: PDF chosen; the HTML
   digest is in `retrieval`). It also has no field for "informative" (RFC 9102, RFC 5480, BIP 144) or for
   "distributed with the verifier versus retrieved" (item 15 asks for both). Both went into free text.
5. **"The DNSSEC algorithms in the chain"** (A9, section 9 row 6) versus section 6.1's supported set {8, 13} with
   DS {2, 4}. The manifest pins the supported set, which is wider than any one chain.
6. **SHA-1DC "implementation and version"** (sections 15.4, 14.2 item 15): upstream has no release at the pin; the
   pin is a commit (`stable-v1.0.3-38-ga06f1ad`). The manifest uses the commit.
7. **The release-signature dependency** (item 15; freeze note R3 "pinned `gpgv`"): no version is pinned anywhere.
   The relying party's actual binary here is Ubuntu's patched `2.4.4-2ubuntu17.6`, not upstream bytes, so a source
   digest does not identify what runs.
8. **OTS**: section 9 calls python-opentimestamps 0.4.5 the reference reader, and no OTS format document exists.
   The `opentimestamps` entry's normative content is therefore profile section 15.2; the archived library is
   reference only, and diverges as section 9 already says.
9. **Line numbers moved during this work**: `docs/V1-PROFILE.md` was being edited concurrently (section 6.1's
   supported-set text moved from line 591 to 641). Cite sections, not lines, when this manifest is frozen.
