"""Build formal/dependency-sources/dependency-manifest.json (profile section 15.6 schema).

Run: python3 -I gen_manifest.py  (reads downloads under ./dl, writes into the repo dir given below)
"""
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DL = HERE / "dl"
REPO = Path("/home/tony/projects/tessera")
OUT = REPO / "formal/dependency-sources"
sys.path.insert(0, str(REPO / "prototype/indep-verifier"))
from codec import jcs, parse_json  # noqa: E402  the repository canonicalizer

ARCH = "formal/dependency-sources/archive/"
NOT_DIST = "Not distributed with the verifier or the spec; retrieved by reference (digest above)."


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def t(p):
    return Path(str(p) + ".time").read_text().strip()


# ---- RFC errata (from https://www.rfc-editor.org/api/v1/errata.json) ----
errata = json.load(open(DL / "rfc/errata.json"))
by = collections.defaultdict(list)
for e in errata:
    by[e["doc-id"]].append(e)


def rfc_errata_counts(n):
    c = collections.Counter(e["errata_status_code"] for e in by.get("RFC" + n, []))
    if not c:
        return "No errata of any status at fetch time"
    return "Errata at fetch time: " + ", ".join(f"{k} {v}" for k, v in sorted(c.items()))


RFC_URL = "https://www.rfc-editor.org/rfc/rfc{}.txt"
RFC_REDIST = ("IETF Trust (BCP 78, TLP 4.e): unmodified copies may be redistributed. " + NOT_DIST)

# id -> (title, sections, disposition-of-verified-errata, failure consequence)
RFCS = {
    "1035": ("Domain names - implementation and specification",
             ["2.3.4 size limits", "3.1 name wire format", "3.2.1 RR format", "3.3.14 TXT RDATA"],
             "Verified 2130 (3.2.1: TTL is a 32-bit unsigned integer) is ADOPTED. Verified 562 (6.4.2) and 6601 "
             "(7.1) and the editorial errata do not touch the sections used.",
             "Snapshot names, RRs or TXT character-strings cannot be parsed: no DNS channel verdict "
             "(snapshot checks fail as INVALID/DNS_* or are unperformable)."),
    "1982": ("Serial number arithmetic", ["3 serial number arithmetic (RRSIG inception/expiration, 32-bit)"],
             "None.", "RRSIG validity windows cannot be compared at T_snap; DNS channel unperformable."),
    "2181": ("Clarifications to the DNS specification", ["5 RRsets", "11 name syntax"],
             "None verified (one rejected).", "RRset membership and name syntax ambiguous; DNS channel unperformable."),
    "3110": ("RSA/SHA-1 SIGs and RSA KEYs in the DNS", ["2 RSA public key RDATA (exponent length, exponent, modulus)"],
             "Verified 2811 (section 3: signature MUST be zero-padded to the modulus length) is ADOPTED; it agrees "
             "with profile section 6.1 'RSA signature width'. 4502 editorial.",
             "Algorithm-8 DNSKEYs (the root KSKs) cannot be decoded; no DNSSEC chain validates."),
    "3339": ("Date and time on the Internet: timestamps", ["5.6 internet date/time format"],
             "Verified 4110 (Appendix A, ISO 8601 note) and editorial 293, 1584, 3710 do not change the 5.6 grammar.",
             "Time strings in the payload and reports cannot be parsed or produced byte-identically."),
    "4034": ("Resource records for the DNS security extensions",
             ["2 DNSKEY RDATA", "3 RRSIG RDATA", "5 DS RDATA", "6 canonical form and order", "Appendix B key tag"],
             "Verified 4552 (Appendix B: carries retained, then folded) is ADOPTED: the Appendix B reference code "
             "governs, as it already folds the carry. Verified 1062 (6.2 item 3 list) is superseded by RFC 6840 "
             "section 5.1, which changes only NSEC (not a V1 type); RRSIG signer names stay lowercased. 3045 and "
             "193 do not affect V1.",
             "DNSKEY/RRSIG/DS cannot be parsed or canonicalized; no DNSSEC chain validates."),
    "4035": ("Protocol modifications for the DNS security extensions", ["2.2 signing all algorithms", "5.3.1-5.3.3 RRSIG checks and verification"],
             "Verified 5226 (3.1.4.1, server DS processing) and 3044 (header) do not touch validation. Adopted as "
             "updated by RFC 6840 where it touches the sections used.",
             "No DNSSEC validation procedure; DNS channel unperformable."),
    "4509": ("Use of SHA-256 in DNSSEC DS RRs", ["2 DS digest type 2"],
             "None verified (one held for document update).", "DS digest type 2 cannot be checked; delegations using it do not validate."),
    "4648": ("The Base16, Base32 and Base64 data encodings", ["3.5 canonical encoding (pad bits)", "4 base64"],
             "Verified errata are editorial (3.5, 5, 10, 16.2); two reported technical not adopted.",
             "Bundle base64 members and git armor cannot be decoded strictly (INVALID or parse failure)."),
    "5011": ("Automated updates of DNSSEC trust anchors", ["3 REVOKE flag bit"],
             "None.", "REVOKE flag meaning undefined; DNSKEY eligibility (REVOKE clear) cannot be checked."),
    "5280": ("Internet X.509 PKI certificate and CRL profile",
             ["4.1 certificate fields", "6.1 path validation (ICANN root-anchors .p7s signer)"],
             "Verified 5938 (6.1) and others not reviewed for the release-side .p7s check; release tooling uses "
             "OpenSSL's implementation. Informative for the bundle verifier.",
             "Release side only: the root-anchors.xml CMS signature cannot be path-validated, so KSK sourcing for "
             "the trust configuration loses its IANA authentication. No bundle verdict changes."),
    "5480": ("Elliptic curve cryptography SubjectPublicKeyInfo", ["2 SPKI for id-ecPublicKey with secp256r1"],
             "Verified 6670 (section 3) concerns signature algorithm identifiers, not the SPKI. Informative: ENC "
             "section 3.3 fixes the exact 26-byte P-256 SPKI prefix.",
             "None for verification (ENC fixes the bytes); loss only of the explanation of the fixed prefix."),
    "5652": ("Cryptographic Message Syntax (CMS)", ["5 SignedData (root-anchors.p7s)"],
             "Verified 6250 (9.2 AuthenticatedData) and 6546 are outside section 5.",
             "Release side only: root-anchors.p7s cannot be verified (as RFC 5280 above)."),
    "5702": ("RSA/SHA-256 and RSA/SHA-512 DNSKEY and RRSIG records", ["2.1 RSA/SHA-256 DNSKEY", "3.1 RSA/SHA-256 RRSIG"],
             "Verified 7090 (8.2, downgrade text) is security-considerations only; V1 validates a path, not all algorithms.",
             "Algorithm-8 signatures (the root) cannot be verified; no DNSSEC chain validates."),
    "6605": ("ECDSA for DNSSEC", ["2 SHA-384 DS (digest type 4)", "3 ECDSA parameters", "4 DNSKEY/RRSIG for algorithm 13"],
             "None.", "Algorithm-13 keys/signatures and DS type 4 cannot be checked; zones signed with them do not validate."),
    "6840": ("Clarifications and implementation notes for DNSSEC", ["5.1 canonical form type list"],
             "None verified. Not named in profile section 9; added because it updates RFC 4034 section 6.2, which "
             "V1 uses. Its 5.1 change concerns NSEC only.",
             "None for V1's record types; listed so that the RFC 4034 erratum disposition is traceable."),
    "7493": ("The I-JSON message format", ["2.1 noncharacters (cited by ENC section 1.1)"],
             "Two reported technical errata, not adopted.",
             "Loss of the stated reason for rejecting noncharacters; the rule itself is ENC section 1.1."),
    "8017": ("PKCS #1: RSA cryptography specifications v2.2", ["8.2.2 RSASSA-PKCS1-v1_5 verification", "9.2 EMSA-PKCS1-v1_5"],
             rfc_errata_counts("8017") + "; not reviewed individually. Not named in profile section 9; added because "
             "RFC 5702 algorithm 8 signatures are RSASSA-PKCS1-v1_5 (RFC 5702 cites RFC 3447, which RFC 8017 obsoletes).",
             "Algorithm-8 RRSIGs cannot be verified; no DNSSEC chain validates."),
    "8259": ("The JSON data interchange format", ["2-7 grammar", "8.1 UTF-8"],
             "Verified 7600 (6, leading zeros prose), 7603 (1, code points) and 7383 (ABNF case) align prose with "
             "the grammar; ADOPTED as clarifications, no behaviour change. 5210, 5318 editorial.",
             "JSON text cannot be parsed identically; payload and bundle JSON members unverifiable."),
    "8785": ("JSON Canonicalization Scheme (JCS)", ["3 (all subsections) canonical serialization"],
             "Verified 7920 (section 5: -0 SHOULD be an error) ADOPTED; V1 already rejects -0 (ENC 1.2). "
             "Verified 6292 corrects the ECMA-262 cross-reference to 24.5.2.2 (ADOPTED).",
             "Canonical payload bytes cannot be reproduced: A_sig, every frame hash and the receipt identity "
             "cannot be recomputed; INVALID/JSON_NONCANONICAL disagreements between verifiers."),
    "9102": ("TLS DNSSEC chain extension", ["3 chain serialization (informative only)"],
             "Verified 6860 (section 12) not relevant. Informative.", "None; informative."),
    "9580": ("OpenPGP", ["4.2 packet headers", "5.2.3 v4 signature packet", "5.2.3.7 subpacket lengths",
                         "5.2.3.11/12/35 creation time, issuer key ID, issuer fingerprint", "5.2.4 computing signatures",
                         "5.5.2 v4 public-key packet", "5.5.4.2 v4 fingerprint", "6, 6.1 armor and CRC-24",
                         "9.1 algorithm 19 ECDSA", "9.2 curve NIST P-256", "9.5 hash algorithm 8 SHA2-256"],
             "Verified 8454 (5.2.3: signatures may be native octets) does not apply to ECDSA (MPIs). 8465 (5.5.3 "
             "secret keys), 8466 (11.2), 8847 (9.1, wording), 8814 (5.6 compression) and editorial 8432, 9094 do "
             "not change rule O.",
             "Rule O signatures (both receipt slots under the fallback, the gpg slot, the git gpgsig, the release "
             "signature) cannot be parsed or verified: SIG_* outcomes and no release authentication."),
    "9718": ("DNSSEC trust anchor publication for the root zone", ["2 root-anchors.xml format", "3 signature (.p7s)"],
             "None.", "Release side only: KSK entries cannot be sourced from IANA material; no bundle verdict changes."),
    "9881": ("Algorithm identifiers for ML-DSA in X.509", ["2 id-ml-dsa-65 OID, parameters absent", "4 SPKI public key",
                                                         "Appendix D external mu"],
             "Verified 8699 (Appendix A: ML-DSA-87 size 2592) and 8700 editorial do not affect ML-DSA-65.",
             "Hybrid only: the kms ML-DSA-65 SPKI and the external-mu construction lose their citation; the "
             "supplement fixes the bytes, so verification continues if FIPS 204 is available."),
}

E = []


def add(id, title, edition, sections, errata_, digest, retrieval, redistribution, failure):
    assert re.fullmatch(r"[a-z0-9-]+", id), id
    assert digest is None or re.fullmatch(r"[0-9a-f]{64}", digest)
    assert sections and all(isinstance(s, str) for s in sections)
    E.append({"digest_sha256": digest, "edition": edition, "errata": errata_, "failure_consequence": failure,
              "id": id, "redistribution": redistribution, "retrieval": retrieval, "sections": sections,
              "title": title})


for n, (title, secs, disp, fail) in RFCS.items():
    p = DL / f"rfc/rfc{n}.txt"
    add(f"rfc{n}", f"RFC {n}: {title}", f"RFC {n} (immutable RFC text)", secs,
        rfc_errata_counts(n) + ". " + disp, sha(p),
        f"{RFC_URL.format(n)} fetched {t(p.with_suffix(''))}; errata status from "
        f"https://www.rfc-editor.org/api/v1/errata.json fetched {(DL / 'rfc/errata.time').read_text().strip()}",
        RFC_REDIST, fail)

NIST = "Work of the US Government, not subject to copyright in the US; redistributable. " + NOT_DIST
nd = DL / "nist"
add("fips-180-4", "FIPS 180-4 Secure Hash Standard (SHA-1, SHA-256, SHA-384)", "FIPS 180-4, August 2015",
    ["6.1 SHA-1 (git object ids, before SHA-1DC)", "6.2 SHA-256", "6.5 SHA-384 (DS digest type 4)"],
    "No errata list published. CSRC planning note (03/07/2023): NIST has decided to revise FIPS 180-4; this "
    "edition is pinned regardless of any revision.",
    sha(nd / "NIST.FIPS.180-4.pdf"),
    f"https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf fetched {t(nd / 'NIST.FIPS.180-4.pdf')}",
    NIST, "No hash can be computed: every frame, anchor, fingerprint, OTS op and Bitcoin link fails; no verdict.")
add("fips-186-5", "FIPS 186-5 Digital Signature Standard (ECDSA)", "FIPS 186-5, February 3, 2023",
    ["6.4.2 ECDSA signature verification"],
    "CSRC 'potential updates' spreadsheet (archived, " + ARCH + "errata/fips186-5-potential-updates.xlsx, sha256 "
    + sha(DL / 'csrc/fips186-5-potential-updates.xlsx') + "): A.3.3 deterministic ECDSA and B.10 prime "
    "construction only; none touches 6.4.2. No official errata.",
    sha(nd / "NIST.FIPS.186-5.pdf"),
    f"https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-5.pdf fetched {t(nd / 'NIST.FIPS.186-5.pdf')}",
    NIST, "ECDSA P-256 signatures (receipt slots, possession, git, release, DNSSEC algorithm 13) cannot be verified.")
add("sp-800-186", "NIST SP 800-186 Recommendations for discrete-logarithm-based cryptography: elliptic curve domain parameters",
    "SP 800-186, February 2023", ["3.2.1.3 P-256", "D.1.1 public key validation"],
    "CSRC potential-updates spreadsheet (archived, " + ARCH + "errata/sp800-186-potential-updates.xlsx, sha256 "
    + sha(DL / 'csrc/sp800-186-potential-updates.xlsx') + "): one item, section 3.2.2.1 (Montgomery curve Gv); "
    "not P-256. No official errata.",
    sha(nd / "NIST.SP.800-186.pdf"),
    f"https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-186.pdf fetched {t(nd / 'NIST.SP.800-186.pdf')}",
    NIST, "P-256 domain parameters and public-key validation (profile section 8) unavailable; KEY_FORMAT checks unperformable.")
add("fips-202", "FIPS 202 SHA-3 standard (SHAKE256)", "FIPS 202, August 2015", ["6.2 SHAKE256"],
    "CSRC planning note (03/13/2025): typographical error in non-normative Appendix B; NIST will update the "
    "publication. Not relevant to 6.2. Not named in profile section 9; added because rule R's external mu "
    "(ENC rule R) calls SHAKE256 directly.",
    sha(nd / "NIST.FIPS.202.pdf"),
    f"https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf fetched {t(nd / 'NIST.FIPS.202.pdf')}",
    NIST, "Hybrid only: ML-DSA-65 mu and verification cannot be computed; kms slot unverifiable.")
add("fips-204", "FIPS 204 Module-lattice-based digital signature standard (ML-DSA-65)", "FIPS 204, August 13, 2024",
    ["Algorithms 2, 3, 7, 8 (sign/verify, external mu)", "7.2 pkDecode/sigDecode encodings", "Table 1 ML-DSA-65 parameters"],
    "CSRC potential-updates spreadsheet, last updated 7/31/2026 (archived, " + ARCH + "errata/fips-204-potential-updates.xlsx, "
    "sha256 " + sha(DL / 'csrc/fips-204-potential-updates.xlsx') + "): NTT wording (2.5, 7.5), M to M' (6.2, 6.3), "
    "c-tilde order wording (3.3), Algorithm 3 step 2 returns false, Algorithm 40 bound, Table 1 repetitions "
    "and Table 3 loop limit. None changes a verification outcome; the Algorithm 3 change (false instead of "
    "bottom) is ADOPTED as the reading. No official errata.",
    sha(nd / "NIST.FIPS.204.pdf"),
    f"https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf fetched {t(nd / 'NIST.FIPS.204.pdf')}",
    NIST, "Hybrid only: the kms ML-DSA-65 slot cannot be verified; under the registered hybrid a receipt then has no VALID_STRICT path.")

ec = DL / "ecma/ECMA-262_10th_edition_june_2019.pdf"
add("ecma-262", "ECMA-262 ECMAScript 2019 Language Specification: NumberToString (the profile's Number::toString)",
    "ECMA-262 10th edition, June 2019 (the edition RFC 8785 cites)",
    ["7.1.12.1 NumberToString(m), including Note 2", "24.5.2.2 QuoteJSONString (RFC 8785 erratum 6292)"],
    "Ecma publishes no errata for this edition; later editions rename the operation Number::toString "
    "(6.1.6.1.20 in ES2020 and later) without changing its output.",
    sha(ec),
    "https://ecma-international.org/wp-content/uploads/ECMA-262_10th_edition_june_2019.pdf fetched " + t(ec)
    + "; HTML form https://262.ecma-international.org/10.0/ (RFC 8785's cited URL "
    "https://www.ecma-international.org/ecma-262/10.0/index.html redirects there), HTML sha256 "
    + sha(DL / 'ecma/es10.html') + " fetched 2026-10-19T23:31Z",
    "Ecma copyright; Ecma's notice permits copying and distributing the unmodified standard. " + NOT_DIST,
    "Number serialization (ES) undefined: the number rule (profile section 10) and JCS number output cannot be "
    "reproduced; the profile's restated ES recipe and vectors N-01..N-22 remain.")
add("ieee-754", "IEEE 754 binary64 floating point", "IEEE Std 754-2019",
    ["3.4 binary interchange format", "4.3.1 roundTiesToEven"],
    "IEEE errata not reviewed (document not freely available).", None,
    "IEEE Xplore, doi:10.1109/IEEESTD.2019.8766229 (paywalled; not fetched)",
    "IEEE copyright; not redistributable. Not distributed. Not named in profile section 9; added because ENC "
    "section 1.1 and the number rule are defined over binary64.",
    "The accepted number domain (binary64, round-half-even) loses its definition; the restated rule and vectors remain.")

UNI = ("Unicode License v3: redistributable with the notice. " + NOT_DIST)
ud = DL / "unicode"
for fid, fname, path, secs, fail in [
    ("ucd-unicodedata", "UnicodeData.txt", "UnicodeData.txt", ["General_Category, Canonical_Combining_Class, decomposition fields"],
     "NFC tables cannot be built; NFC checks unperformable."),
    ("ucd-derivedgeneralcategory", "DerivedGeneralCategory.txt", "extracted/DerivedGeneralCategory.txt", ["Cn (unassigned) ranges"],
     "The unassigned-code-point rule (ENC 1.1) cannot be applied; verifiers on other Unicode versions may disagree."),
    ("ucd-derivednormalizationprops", "DerivedNormalizationProps.txt", "DerivedNormalizationProps.txt", ["Full_Composition_Exclusion", "NFC_QC"],
     "NFC composition cannot be built exactly; NFC checks unperformable."),
    ("ucd-compositionexclusions", "CompositionExclusions.txt", "CompositionExclusions.txt", ["all"],
     "NFC composition cannot be built exactly; NFC checks unperformable."),
    ("ucd-normalizationtest", "NormalizationTest.txt", "NormalizationTest.txt", ["Part 0-3, NFC column (conformance test)"],
     "No conformance test for an NFC implementation; agreement cannot be demonstrated."),
]:
    p = ud / fname
    add(fid, f"Unicode 16.0.0 UCD {fname}", "Unicode 16.0.0 (UCD file dated 2024)", secs,
        "Unicode publishes no errata for released UCD files; corrections go to later versions, which V1 does not use.",
        sha(p), f"https://www.unicode.org/Public/16.0.0/ucd/{path} fetched {t(p)}", UNI, fail)
add("uax-15", "Unicode Standard Annex #15: Unicode normalization forms", "UAX #15 revision 56 (Unicode 16.0.0)",
    ["3 normalization forms", "Canonical composition algorithm", "9 detecting normalization forms"],
    "None published for this revision.", sha(ud / "tr15.html"),
    f"https://www.unicode.org/reports/tr15/tr15-56.html fetched {(ud / 'tr15.time').read_text().strip()}",
    "Unicode terms of use: redistributable unmodified. " + NOT_DIST,
    "NFC is undefined; string checks (ENC 1.1) unperformable.")

# ---- archived, at-risk sources ----
A = OUT / "archive"
BTC_COMMIT = "9be056a8a72b624dae9623b2f7bded92c2a21c91"
add("bitcoin-core-formats", "Bitcoin header, double SHA-256, merkle root and non-witness transaction formats (Bitcoin Core source)",
    f"Bitcoin Core v31.1, commit {BTC_COMMIT}",
    ["src/primitives/block.h CBlockHeader (80-byte header)", "src/primitives/block.cpp GetHash (double SHA-256)",
     "src/primitives/transaction.h/.cpp CTransaction serialization and txid", "src/consensus/merkle.cpp merkle root",
     "src/serialize.h CompactSize", "src/hash.h Hash/CHash256"],
    "Source code; no errata. The profile (sections 7.2, 15.2) restates every field it uses; this archive is the reference.",
    sha(A / "bitcoin-core-formats/SHA256SUMS"),
    f"https://raw.githubusercontent.com/bitcoin/bitcoin/{BTC_COMMIT}/<path> fetched {t(DL / 'btc/primitives_block.h')}; "
    "digest is of SHA256SUMS listing every archived file",
    f"MIT licence; redistributed. Archived in {ARCH}bitcoin-core-formats/ (distributed with the spec sources).",
    "Header, txid and merkle checks lose their external reference; the profile's restatement remains normative.")
add("bip-0144", "BIP 144: segregated witness peer services (witness serialization marker and flag)",
    "bitcoin/bips commit 130b8e0fa7f30fa45532f080b87b8db27a79e46e", ["Serialization (marker 0x00, flag 0x01)"],
    "None. Informative: defines what V1 rejects ('no SegWit marker', profile section 15.2).",
    sha(A / "bip-0144/bip-0144.mediawiki"),
    "https://raw.githubusercontent.com/bitcoin/bips/130b8e0fa7f30fa45532f080b87b8db27a79e46e/bip-0144.mediawiki fetched "
    + t(DL / "bips/bip-0144.mediawiki"),
    f"BSD-2-Clause (per BIP header); redistributed. Archived in {ARCH}bip-0144/.",
    "None for verification; the rejected form loses its definition.")
GIT_COMMIT = "a018953688f1b10bddf91bff8747068f5f4746a4"
add("gitformat-signature", "gitformat-signature(5): git cryptographic signature formats", f"git v2.56.0, commit {GIT_COMMIT}",
    ["Commit signatures (gpgsig header, signed payload)"],
    "Documentation; no errata.", sha(A / "gitformat-signature/gitformat-signature.adoc"),
    f"https://raw.githubusercontent.com/git/git/{GIT_COMMIT}/Documentation/gitformat-signature.adoc fetched "
    + t(DL / "git/gitformat-signature.adoc"),
    f"GPL-2.0 (git); redistributed. Archived in {ARCH}gitformat-signature/.",
    "The git signed payload loses its external reference; profile section 15.4 restates it.")
add("git-object-format", "git object format: object header, commit and tree encoding, tree ordering",
    f"git v2.56.0 fsck.c (commit {GIT_COMMIT}) and Pro Git 2nd ed. section 10.2 (progit2 commit a013e3230a1207cfa5ae94d28ba7d2021063c337)",
    ["Object header '<type> <len>\\0'", "Commit headers", "Tree entries, modes and sort order (fsck.c verify_ordered)"],
    "No formal specification or errata exist; profile section 15.4 is the normative restatement.",
    sha(A / "git-object-format/SHA256SUMS"),
    f"https://raw.githubusercontent.com/git/git/{GIT_COMMIT}/fsck.c and "
    "https://raw.githubusercontent.com/progit/progit2/a013e3230a1207cfa5ae94d28ba7d2021063c337/book/10-git-internals/sections/objects.asc "
    f"fetched {t(DL / 'git/fsck.c')}; digest is of SHA256SUMS",
    f"fsck.c GPL-2.0; Pro Git CC BY-NC-SA 3.0 (non-commercial redistribution); archived in {ARCH}git-object-format/.",
    "Git ids, trees and commits lose their external reference; profile section 15.4 restates them.")
add("sha1dc", "SHA-1DC collision detection (git object ids), with prescribed collision return",
    "cr-marcstevens/sha1collisiondetection commit a06f1adbe5522f3c939cd6a3f13d5ec7f4c1a988 (stable-v1.0.3-38-ga06f1ad)",
    ["lib/sha1.c SHA1DCFinal nonzero on detection", "safe-hash on, reduced-round detection off (default flags)"],
    "Source code; no errata. Detection maps to INVALID/GIT_SHA1_COLLISION (profile section 15.4).",
    sha(OUT / "sha1dc.SHA256SUMS"),
    "https://github.com/cr-marcstevens/sha1collisiondetection at the commit above; vendored at "
    "prototype/vendor/sha1collisiondetection/ (pin record prototype/vendor/SHA1DC-PIN.md); digest is of "
    "formal/dependency-sources/sha1dc.SHA256SUMS (the six pinned source files)",
    "MIT licence; distributed with the verifier as vendored source, built at install (packaging/install.sh checks the digests).",
    "Git object ids cannot be computed with collision detection; GIT_SHA1_COLLISION unperformable and the git channel fails.")
ots = A / "opentimestamps/opentimestamps-0.4.5.tar.gz"
add("opentimestamps", "OpenTimestamps DetachedTimestampFile format (python-opentimestamps reference reader)",
    "python-opentimestamps 0.4.5 sdist (tag python-opentimestamps-v0.4.5, commit a90094e3ca9a8229abd016be8816d7b90b9fd1e6)",
    ["opentimestamps/core/timestamp.py DetachedTimestampFile, Timestamp", "core/op.py ops 08, f0, f1",
     "core/notary.py attestation tags 0588960d73d71901, 83dfe30d2ef90c8e", "core/serialize.py varuint, varbytes"],
    "No specification or errata exist. Profile section 15.2 is normative and narrower: the library is the "
    "reference reader only, and diverges at depth 256, redundant LEB128 and SHA-1/RIPEMD-160 ops (section 9).",
    sha(ots),
    "https://files.pythonhosted.org/packages/fb/2a/5f19420091d137e5a4c49cbe3de1964a3741d3264bad5e0a528e54aaef15/opentimestamps-0.4.5.tar.gz "
    f"fetched {t(DL / 'ots/opentimestamps-0.4.5.tar.gz')} (sha256 equals PyPI's published digest)",
    f"LGPL-3.0; redistributed unmodified. Archived in {ARCH}opentimestamps/.",
    "OTS proofs lose their external reference; profile section 15.2's grammar remains normative.")
gp = DL / "gnupg/gnupg-2.4.4.tar.bz2"
add("gpgv", "gpgv (GnuPG) release-signature checker, OpenPGP RFC 9580 rule O subset",
    "GnuPG 2.4.4 upstream source (as observed; release R3/R6 'pinned gpgv' version not yet decided)",
    ["gpgv exit status 0 on <archive>.sig <archive> with a single-key keyring (release R3)"],
    "Not applicable (software). Observed relying-party binary on the owner machine is Ubuntu 2.4.4-2ubuntu17.6, "
    "a patched build whose bytes differ from upstream.",
    sha(gp), f"https://gnupg.org/ftp/gcrypt/gnupg/gnupg-2.4.4.tar.bz2 fetched {t(gp)}",
    "GPL-3.0; not distributed with the verifier; the relying party installs it.",
    "Release authentication only: a release cannot be authenticated, so the verifier's own authenticity rests on "
    "assumption (contract section 2). No bundle verdict changes.")

E.sort(key=lambda e: e["id"])
ids = [e["id"] for e in E]
assert len(ids) == len(set(ids))
for e in E:
    for k, v in e.items():
        if k == "digest_sha256":
            continue
        for s in (v if isinstance(v, list) else [v]):
            assert isinstance(s, str) and s and s.isascii() and "TEST" not in s, (e["id"], k, s)
raw = jcs({"entries": E, "format": "tessera-v1-deps/1"})
parse_json(raw, canonical=True)  # repository check: raises unless raw is its own JCS form
(OUT / "dependency-manifest.json").write_bytes(raw)

# errata extract for the RFCs (evidence for the dispositions)
ext = {f"RFC{n}": by.get("RFC" + n, []) for n in RFCS}
(A / "errata/rfc-errata-extract.json").write_bytes(jcs(ext))
print(len(E), "entries;", hashlib.sha256(raw).hexdigest(), len(raw), "bytes")
