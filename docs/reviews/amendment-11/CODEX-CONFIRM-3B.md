**Verdict: bind the tested verifier tree to a ZIP produced by the trusted packager, then match that exact ZIP’s SHA-256 to AWS `CodeSha256` for the deployed function/version. `check_zip` alone does not establish the claim.**

Repository and git remained read-only. All probes and extraction outputs are under [the scratch directory](/tmp/tessera-a11c3b.yrZ1FWQq), including the [probe script](/tmp/tessera-a11c3b.yrZ1FWQq/probe.py) and [results](/tmp/tessera-a11c3b.yrZ1FWQq/results.json). No AWS calls were made.

**A11C3B-01 — High: the current check does not establish deployment identity. Evidence: demonstrated by code inspection.**

[`test_deployed_zip_identity`](/home/tony/projects/tessera/formal/p3-verification-profile/test_p3_profile.py:181) accepts a local path from `TESSERA_LAMBDA_ZIP` and calls `check_zip`. It neither queries AWS nor compares an archive digest with AWS’s reported digest. Passing a correctly constructed, undeployed ZIP therefore satisfies it.

[`check_zip`](/home/tony/projects/tessera/formal/p3-verification-profile/test_p3_profile.py:70) establishes a narrower fact: **Python’s selected archive entries contain the current verifier-tree bytes and the recorded native binding/WHEEL tag.** The assertion in its comment that this establishes exactly what extraction writes is too broad.

AWS documents `CodeSha256` as the SHA-256 of the deployment package. `GetFunction` also provides a download link for the package, optionally for a specified version. Those provide the missing deployment binding. [AWS FunctionConfiguration](https://docs.aws.amazon.com/lambda/latest/api/API_FunctionConfiguration.html), [AWS GetFunction](https://docs.aws.amazon.com/lambda/latest/api/API_GetFunction.html).

**A11C3B-02 — Medium: extractor behavior varies, and Lambda’s extractor is undocumented in the public AWS documentation reviewed. Evidence: documented; AWS implementation remains unknown.**

“Python reads the central directory” needs qualification: it enumerates entries there, but **also reads each selected local header and compares its decoded filename with the central entry’s original filename when opening that entry**. A simple local/central filename mismatch in `codec.py` is rejected. [CPython implementation](https://raw.githubusercontent.com/python/cpython/3.14/Lib/zipfile/__init__.py).

Widely used implementations differ as follows:

| Implementation | Local-header involvement |
|---|---|
| Java `ZipInputStream`, including its `JarInputStream` subclass | Reads local entries sequentially. Oracle explicitly describes `getNextEntry()` as reading the local header. |
| Apache Commons Compress `ZipArchiveInputStream` | Streams local entries; may return entries absent from the central directory. Its `ZipFile` instead reads the directory first. |
| libarchive | Has streaming and seeking ZIP readers. The streaming reader uses local headers; the seeking reader consults the central directory first. Selection depends on available seeking support. |
| Info-ZIP `unzip` | Uses the central directory **and** local headers. Here it warned about mismatched names and continued using the central filename. |
| uv’s historical streaming installer | Publicly documented local-entry versus central-directory differentials, including duplicate and stacked archives. This describes affected historical versions, not an assertion about current uv. |

Sources: [Oracle](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/zip/ZipInputStream.html), [Apache](https://commons.apache.org/proper/commons-compress/zip.html), [libarchive](https://github.com/libarchive/libarchive/wiki/FormatZip), [Info-ZIP source](https://raw.githubusercontent.com/madler/unzip/master/extract.c), [Astral advisory](https://astral.sh/blog/uv-security-advisory-cve-2025-54368).

AWS’s Python packaging documentation describes archive creation, layout and permissions, but does not identify the deployment extractor, its version, or its conflict-resolution policy. **I found no public AWS documentation establishing that Lambda uses Python `zipfile`, Info-ZIP, libarchive, or another particular extractor. Treat it as undocumented.** AWS examples using `zip` or `unzip` on the developer’s machine do not identify the server-side implementation. [AWS packaging documentation](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html).

Also distinguish **valid-format variation** from **recovery of malformed archives**. PKWARE requires one EOCD record and a corresponding central header for each local header. Multiple competing EOCDs and orphan local entries are therefore not simply two equally conforming interpretations of a valid archive. They remain relevant because real parsers accept such inputs differently. [PKWARE specification, §4.3](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT).

**A11C3B-03 — High: passing `check_zip` does not imply extractor agreement. Evidence: demonstrated locally.**

I ran 23 benign cases using **Python 3.14.6** from the verifier environment and Debian **Info-ZIP UnZip 6.00**. The harness executed the actual checker and its two helper functions, extracted from the repository’s AST without importing the test module. Baseline inputs included all current verifier files and the installed native binding matching F1.

Selected results:

| Constructed property | `check_zip` | Python extraction | Info-ZIP extraction |
|---|---|---|---|
| Baseline | Pass | Success | Success |
| Local name differs for checked `codec.py` | Reject | Reject | Warning; central name used |
| Local name differs for unchecked `notes.txt` | **Pass** | Reject | Warning; central name used |
| Local compression method differs for `codec.py` | **Pass** | Original bytes | Different bytes; CRC error |
| Local compressed/uncompressed sizes changed to 1 | **Pass** | Original bytes | Empty output file; inflate error |
| Local encryption bit differs | **Pass** | Success | Success |
| Local UTF-8 flag differs, ASCII filename | **Pass** | Success | Warning; same verifier bytes |
| Prepended benign bytes | **Pass** | Success | Warning; same verifier bytes |
| Appended benign bytes | **Pass** | Success | Success |
| Incorrect EOCD entry counts | **Pass** | Success | Error |
| Unreferenced local entry | **Pass** | Entry ignored | Entry ignored |
| Concatenated archives, expected archive last | **Pass** | Last archive selected | Warning; expected verifier extracted |
| Two directories/EOCDs, first EOCD comment encloses second | **Pass** | Success | Success |
| `./tessera_verify/codec.py` alias | Reject | Overwrites checked path | Overwrites checked path |
| Duplicate central filename | Reject | Accepted | Accepted |
| Unix-mode symlink entry | Reject | Extracted as ordinary content | Symlink created |
| File named `tessera_verify` alongside its children | **Pass** | Extraction error | Extraction error |

For the compression-method case, Python wrote the original **15,338-byte** `codec.py`; Info-ZIP wrote **5,693 different bytes** and reported failure. This demonstrates disagreement, **not successful silent exploitation or acceptance by Lambda**.

**A11C3B-04 — Medium: protection is partial across the documented ambiguity classes. Evidence: documented taxonomy, demonstrated cases, and code-derived conclusions.**

The public ZipDiff research identifies 14 classes, covered below. The detection assessments are my analysis of this checker; **D** marks a locally demonstrated example, and **I** a code-derived assessment without a dedicated probe. [ZipDiff, USENIX Security 2025, §5.2](https://www.jianjunchen.com/p/zipdiff.USESEC25.pdf).

| Class | Would this checker detect it? |
|---|---|
| Compression-method disagreement | **No, generally. D:** local method changed on a checked entry still passes. |
| Size disagreement, including descriptor/ZIP64 sources | **Partial. D:** local sizes can disagree and pass. Python rejects some corrupt streams, but the checker does not reconcile every size source. |
| Filename disagreement and Unicode Path extra fields | **Partial. D:** checked ordinary local/central mismatch rejects; unchecked mismatch passes. Unicode details below. |
| File/directory/type disagreement | **Partial. D:** Unix-mode symlinks reject, but file/ancestor-directory conflict passes. Other type representations are not comprehensively validated. |
| Encryption-flag disagreement | **Partial. D:** local-only encryption flag passes. Encryption Python recognizes on an opened entry requires credentials or fails. |
| Duplicate names | **Yes for Python-visible exact duplicates. D.** Hidden entries or aliases interpreted differently elsewhere escape that particular test. |
| Invalid/special characters | **Partial. D:** a raw NUL in an unchecked entry passes after Python sanitizes its visible name. No general character-policy check exists. |
| Path canonicalization | **Yes for the tested POSIX aliases. D:** dot components, redundant normalization and backslashes are addressed. Drive-letter syntax is not explicitly excluded. |
| Case sensitivity | **No case-collision check. D:** uppercase extra alias passes. It remains distinct on this Linux filesystem; Windows behavior is not Lambda evidence. |
| Streaming versus directory enumeration | **No. D:** an orphan local record passes. Descriptor boundaries, holes and some overlaps also require separate reasoning. |
| EOCD selection | **No uniqueness check. D:** one multiple-EOCD construction passes; another malformed construction rejects incidentally. |
| Directory-entry counts | **No consistency check. D:** false EOCD counts pass. |
| Directory/local-header offsets | **Partial. D/I:** prefix-offset compensation passes; some bad offsets fail inside Python. There is no independent archive-layout validation. |
| ZIP64 EOCD interpretation | **No explicit cross-source consistency check. I:** Python selects its interpretation; success is not proof another parser selects the same one. |

Additional qualifications:

- **Unicode is version-sensitive.** This Python 3.14.6 recognizes central Unicode Path field `0x7075`. Adding an alternate name that mapped onto `codec.py` was rejected as a duplicate. A **local-only** Unicode Path override passed; Info-ZIP warned and retained the central name. Thus “Python ignores Unicode Path fields” would be inaccurate here. Multiple fields and precedence combinations remain unexhausted. [CPython implementation](https://raw.githubusercontent.com/python/cpython/3.14/Lib/zipfile/__init__.py).
- **Prefixes, suffixes and concatenation are not expressly rejected.** Demonstrated above; acceptance alone does not imply altered verifier content.
- **CRC and overlap checks are inherited and selective.** Python checks CRC while reading selected content and rejects certain overlaps. `check_zip` does not read every payload or validate complete byte coverage, so those checks are not whole-archive conformance evidence. [CPython implementation](https://raw.githubusercontent.com/python/cpython/3.14/Lib/zipfile/__init__.py).

These tests establish bounded counterexamples, not an exhaustive classification of everything each extractor accepts.

**A11C3B-05 — High: exact archive hashing is the stronger deployment binding, provided the expected digest comes from the verified build. Evidence: demonstrated packager structure, documented AWS API, inferred assurance.**

[`write_zip`](/home/tony/projects/tessera/service/issuer/package.py:66) constructs a fresh archive with Python `zipfile`, sorted paths, fixed timestamps, regular-file modes and fresh `ZipInfo` objects. It writes staged bytes rather than copying ZIP headers from dependency archives. That substantially reduces the relevant parser-ambiguity surface.

For this pipeline, use:

1. Freeze or record the verifier bytes actually tested; verify their equality with the staged verifier bytes and retain the F1 native-binding check.
2. Produce the final deployable archive with the reviewed packager and record its SHA-256.
3. Deploy those exact bytes.
4. Compare `base64(SHA256(zip_bytes))` with AWS `CodeSha256` for **each relevant function/version**, retaining the AWS response and deployment identity.

The packager prints hexadecimal; AWS’s value uses base64 representation of the raw digest. Existing Terraform specifies `filebase64sha256(var.lambda_zip)` for both API and poller, but that configuration is not itself a retained post-deployment comparison. [Terraform configuration](/home/tony/projects/tessera/service/issuer/infra/main.tf:330), [provider documentation](https://registry.terraform.io/providers/hashicorp/aws/6.4.0/docs/data-sources/lambda_function.html?lang=typescript).

The trade-off is precise:

| Archive-content comparison | Exact trusted-build digest comparison |
|---|---|
| Can validate verifier content in independently assembled archives | Rejects every byte change from the recorded build |
| Accepts harmless repackaging differences | Requires the exact artifact; rebuilding may produce another digest |
| Depends on the checker’s archive interpretation | Depends on trustworthy build provenance and digest recording |
| Does not identify what AWS deployed | Establishes deployment-package identity through AWS’s reported digest |

**A digest does not resolve an already-ambiguous archive:** every extractor receives the same digest even if they interpret the bytes differently. The improvement comes from binding deployment to a **known packager output with verified inputs**, rather than accepting any ZIP that passes one parser. Astral explicitly documents different extraction outcomes despite an unchanged archive digest. [Astral advisory](https://astral.sh/blog/uv-security-advisory-cve-2025-54368).

Hash identity also does not independently prove which modules the runtime loaded, or cover layers and configuration. If the intended claim is literally about the **post-extraction filesystem**, add a deployed manifest check of the relevant files and native binding. Otherwise state the bounded artifact-identity claim and its build/AWS assumptions.

Prefer a published version when available. AWS supports publishing conditional on `CodeSha256` and `RevisionId`, which helps avoid recording one artifact and subsequently identifying another. Current Terraform does not publish versions. [AWS PublishVersion](https://docs.aws.amazon.com/lambda/latest/api/API_PublishVersion.html).

**A11C3B-06 — Recommendation: replace §A11.2 item 3(c) with an explicit evidence chain.**

Suggested wording:

> **(c)** the exact deployable ZIP produced by the recorded `service/issuer/package.py` build is retained with its SHA-256. Its verifier files are byte-identical to the recorded tree exercised by the passing floor run, and its cryptography binding and wheel tag match F1. After successful deployment, that ZIP’s SHA-256, encoded as base64, matches AWS `CodeSha256` for every function/version to which this discharge applies. The record identifies the source/test inputs, packager, archive digest, AWS function/version and comparison result. This establishes deployment-package identity under the recorded build and AWS deployment assumptions; it does not assert equivalence among arbitrary ZIP extractors.

If you require the stronger post-extraction claim, append:

> A deployed check additionally confirms that the relevant extracted verifier files and native binding match the recorded manifest.

This retains `check_zip` as useful build-content evidence while replacing its unsupported extraction-equivalence inference with an explicit deployment binding.

