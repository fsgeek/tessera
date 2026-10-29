# Wycheproof vectors: source record

Fetched 2026-10-28 from C2SP/wycheproof. The pinned commit is the `main` head at fetch time, as reported by
`GET https://api.github.com/repos/C2SP/wycheproof/commits/main`:

**commit `d17cc89fa5c8f4f4d378b5385ebf75da5d0926c9`** (committer date 2026-10-23T18:06:41Z)

| File | URL | SHA-256 | Schema | Tests |
|---|---|---|---|---|
| `ecdsa_secp256r1_sha256_test.json` | https://raw.githubusercontent.com/C2SP/wycheproof/d17cc89fa5c8f4f4d378b5385ebf75da5d0926c9/testvectors_v1/ecdsa_secp256r1_sha256_test.json | `182db4f3e230f6f9fa9f800d2a614dede30284b8e8438bbfe1171905402e9332` | `ecdsa_verify_schema_v1.json` | 484 |
| `ecdsa_secp256r1_sha256_p1363_test.json` | https://raw.githubusercontent.com/C2SP/wycheproof/d17cc89fa5c8f4f4d378b5385ebf75da5d0926c9/testvectors_v1/ecdsa_secp256r1_sha256_p1363_test.json | `c60de693930e386c3a5472d08081623ef8504decc54b38ac01ec6b2a2575c986` | `ecdsa_p1363_verify_schema_v1.json` | 262 |
| `mldsa_65_verify_test.json` | https://raw.githubusercontent.com/C2SP/wycheproof/d17cc89fa5c8f4f4d378b5385ebf75da5d0926c9/testvectors_v1/mldsa_65_verify_test.json | `1ca235f61928421a173a171780beb00264ae9155dc33c52a11e1766cc7979034` | `mldsa_verify_schema.json` | 210 |

The files are stored byte for byte as fetched (each digest was re-checked against a second fetch).
`test_wycheproof.py::TestSource` checks the digests and the per-file test counts. None of the three files contains
an `acceptable` result.

How the cases are routed through the verifier, and which layer decided each one, is in the docstring of
`../test_wycheproof.py`.
