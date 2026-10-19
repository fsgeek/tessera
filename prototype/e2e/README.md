# prototype/e2e: the first real V1 receipt (instrument)

**Instrument code under A9.2.** It lives under `prototype/`, service code never imports it, and it is evidence for
nothing. It implements steps 2, 3, 4 and 6 of `docs/V1-E2E-GAP.md`. Owner decision for this build, not reopened
here: the first receipt uses the spec object **without** the A10 service-key listing and **without**
`utc_assessment`. It is a TEST pipeline proof, not a keepsake.

All mutable state, including TEST private keys, lives in `work/`, which `.gitignore` excludes. Do not commit `work/`
as it is. Copy out the public files you want to keep.

## Files

| File | Gap step | What it does |
|---|---|---|
| `freeze.py` | 2 | TEST freeze. Assembles the §15.8 spec and vectors objects from tracked blob bytes at one named commit, plus a TEST preamble, a TEST dependency manifest (§15.6 schema) and the catalog (hybrid pair id). Writes the hashes to `freeze-record.json` outside the parts. Includes an independent byte-agreement check (`git show` against the parsed parts). |
| `trustcfg.py` | 3 | §15.5 trust configuration. `fetch-roots` archives IANA `root-anchors.xml`, `.p7s` and `icannbundle.pem` with URL, time and sha256. `roots` builds the KSK-2017 and KSK-2024 entries: RDATA from the XML, DS digest cross-checked, RDATA byte-matched against the archived live root DNSKEY RRsets, `.p7s` checked with openssl. Also builds the repository entry and the pins. |
| `repo.py` | 4 | TEST repository key: a throwaway GnuPG P-256 key in a fresh `mkdtemp` GNUPGHOME under `work/`. The git repository under `work/` holds `tessera-v1/key-assertion`, the 255-byte value with no LF, signed by the TEST key. Checks run before export: closed headers, rule-O codec, signature, path. No stamping here. |
| `signers.py` | 6 | Slot signers: `TestKms` and `TestGpg` (conformance tcrypto); `AwsKmsMldsa` (boto3, always EXTERNAL_MU); `PolicySignerGpg` (SQS, via `policy-signer/client.py`). |
| `otsutil.py` | 6 | Issuer-side OTS reader in the closed §15.2 grammar. Also: lowest-height selection, tx-shape and merkle-suffix checks, txid. `RealOts` runs `ots stamp` and `ots upgrade`. `StubOts` is a persisted synthetic calendar and chain. |
| `dnssnap.py` | 6 | Live DNSSEC capture (read-only queries), conversion to §15.3, no-wildcard check, and dnspython validation at a given time under {8, 13} / {2, 4} with only the configured root KSKs trusted. The stub resolver builds wire responses from the TEST hierarchy. |
| `btcheaders.py` | 6 | Header fetch from two explorers that must agree (the logic of `spike/finalize.py`). |
| `driver.py` | 6 | The issuer driver. It has 19 resumable stages, each recorded in `<run>/state.json`. It runs in `dry` or `real` mode. |
| `smoke_network.py` | — | The one allowed network smoke test: an OTS stamp of 32 random bytes, plus the six newest mainnet headers. |
| `tests/` | — | 18 pytest tests (units, plus the whole driver in dry mode with negatives). |

## How to run (from `prototype/`)

```sh
uv run pytest e2e/tests -q                       # 18 tests, ~10 s, offline
uv run python e2e/driver.py dry-run [--run DIR]  # whole pipeline, TEST signers, stubbed OTS and DNS, ~6 s
uv run python e2e/freeze.py [--commit C]         # TEST freeze only
uv run python e2e/trustcfg.py fetch-roots        # archive IANA root anchors (network, once)

# real run (owner; see "What blocks the real run")
uv run --with boto3 python e2e/driver.py init --run e2e/work/runs/real-1 --mode real \
    --kms-key-id alias/tessera-pq-spike --not-before 2026-10-21T00:00:00Z --not-after 2026-12-31T00:00:00Z
uv run --with boto3 python e2e/driver.py run --run e2e/work/runs/real-1 --until assertion   # -> txt-record.txt
#   ... Tony publishes txt-record.txt ...
uv run --with boto3 python e2e/driver.py run --run e2e/work/runs/real-1   # resumes; exit 75 = still waiting, rerun later
uv run python e2e/driver.py status --run e2e/work/runs/real-1
```

Stages, in this order: `freeze`, `keys`, `assertion`, `repo`, `stamp-git`, `wait-git` (k = 6 on the commit stamp), `frames`
(real mode first checks that the published TXT validates and equals the assertion), `sign`, `asig`,
`stamp-receipt` (refused unless tip ≥ h_git + 5), `dns`, `stamp-dns`, `wait`, `headers`, `check`, `assemble`,
`trust`, `release`, `verify`. A stage that has finished is never rerun. Each one reads its inputs from files written
by earlier stages, so a run can stop at any point and resume in a new process. The tests cover this: they stop
after `frames`, then resume.

Verification goes through `prototype/differential/adapter.py`, with `TESSERA_V1_TEST_RELEASE` and `..._KEY` set.
The adapter checks the TEST release signature (`tessera-v1-test-release/1`, ECDSA P-256) and then provisions the
independent verifier. A release signed by any other key gives no verdict. Moving that check into `verify.py`
itself is gap step 7, which this build does not do. A concurrent session was building step 7 in the working tree
on 2026-10-19 (`indep-verifier/release_auth.py`, uncommitted). The dry-run bundle also returns `VALID_STRICT`
through it: `uv run python indep-verifier/verify.py --trust R/trust.json --bundle R/bundle.json --test-release
R/release.json --test-release-key R/release-key.json`.

## What the dry run proved

Command and output (2026-10-19; the final JSON line printed by the driver):

```
$ uv run python e2e/driver.py dry-run --run e2e/work/runs/dry-readme
...
[e2e] stage check done: {"T": "2026-10-19T13:58:43Z", "h_receipt": 950007, "h_git": 950001, "h_snapshot": 950007, "txid": "065ca4d0…a1", "checks": 24}
[e2e] independent verifier: {"T":"2026-10-19T13:58:43Z","historical_security":"NOT_EVALUATED","reason":"OK","revocation":"NOT_EVALUATED","standing":"ABSENT/NOT_ISSUED_IN_PROFILE","verdict":"VALID_STRICT"}
```

What it proves:
- The driver produces a 3.7 MB canonical container. The independent verifier, provisioned only by a TEST-signed
  release, returns `VALID_STRICT / OK`.
- These pieces are real: the TEST freeze objects (assembled from commit 475387c), the frame and anchor encoders,
  ML-DSA-65 EXTERNAL_MU signing for the kms slot (local TEST key), rule O for the gpg slot (local TEST key), GnuPG
  2.4.4 key generation, and a git 2.43 signed commit. Its `gpgsig` passes the rule-O codec and the verifier's
  §15.4 checks.
- All 24 pre-ship checks pass on all three proofs: digest, no contradiction, anchored, tx shape and merkle suffix,
  c1 to c3 for the receipt and the snapshot, `h_git + 5 < h_receipt`, window, no wildcard, DNSSEC valid at T_snap,
  and DNS value = git blob = assertion.
- The tests also show:
  - flipping one bit of the signed content gives `INVALID`;
  - a swapped txid gives `INVALID / ANCHOR_TXID_MISMATCH`;
  - a release signed by another key gives no verdict (`TRUST_CONFIG_UNAUTHENTICATED`, exit 2);
  - stamping the receipt before the git proof reaches k = 6 is refused.

What it does not prove: the dry run stubs the signers, the OTS calendars and chain, the DNS resolver and the root
KSKs (TEST hierarchy). Those code paths were exercised separately, as listed below.

**Ran on real material, outside the dry run:**
- `smoke_network.py` stamped 32 random bytes at four public calendars. The issuer reader parsed the proof (4
  pending attestations, digest = SHA-256 of the file). It fetched heights 972150 to 972155 from both explorers;
  pins and prev links qualify.
- The OTS reader, selection and txid code ran on the archived 2026-10-09 mainnet spike proof with its archived
  headers (unit test).
- The §15.3 converter and validator ran on the archived 2026-10-12 live capture (unit test). The same code ran on
  a fresh read-only live capture today (`work/live-dns-check/`): root → wamason.com DNSKEY validates under the
  archived IANA KSK-2024 (tags 38696, 8763, 19718, 65344, 2371). The TXT record is absent, as expected.
- The IANA root anchors were fetched and archived (`work/root-anchors/`). The `.p7s` verifies with openssl against
  `icannbundle.pem`, but that bundle came over the same HTTPS channel, so this is **not** the independent bootstrap
  §5 asks for. KSK-2017 and KSK-2024 RDATA match the archived live RRsets byte for byte. The entries parse under
  the independent verifier's §15.5 parser.

**Not run (predictions):**
- every AWS call (`AwsKmsMldsa`, the SQS client);
- the policy signer;
- `ots upgrade` reaching k = 6 on a real stamp;
- a real `wait-git`, `wait`, `headers`, `check`, `trust` and `verify` on real proofs;
- a live snapshot that includes the TXT.

I predict the real run returns `VALID_STRICT`, but it has not been demonstrated.

## TEST namespace

The freeze goes to `work/test-freeze/<commit>/`, and its record says `"namespace": "TEST"`. The preamble and the
dependency manifest contain "TEST" in their bytes, so every receipt signed over them carries TEST hashes inside
its signed bytes. The catalog has a `TEST` member.

The spec and vectors objects are exact §15.8 assemblies of the named commit and are not themselves marked, because
the recipe admits only tracked blobs. The vectors inventory (`formal/p8/vectors/` plus
`prototype/conformance/cases-index.json`) is a TEST choice; the real RES §L inventory is a freeze decision. KSK
periods are the profile's PROPOSED values (§14.2 item 3 is still open). `as_of` is the later of now and the newest
pinned header time, so open entries are never at the trust horizon for the evidence used.

## What blocks the real run (owner or Tony)

1. **AWS login** (Tony): `aws login --profile tessera` (credentials expired 2026-10-19). Then the owner confirms
   the kms-slot key: `alias/tessera-pq-spike` still exists, or a new ML-DSA-65 key replaces it, with `kms:Sign`
   (EXTERNAL_MU) and `kms:GetPublicKey` allowed for the issuer role. Run with `uv run --with boto3` (boto3 is not
   in `pyproject.toml`).
2. **Window** (owner): choose `issuance-not-before` / `issuance-not-after`, at most 90 days. A published window
   cannot be shortened, and the receipt's T must be at or before not-after.
3. **TXT record** (Tony, Cloudflare): publish `_tessera-v1.wamason.com` TXT with exactly the 255-byte value in
   `<run>/txt-record.txt`, as one character-string. With the spike keys it would be
   `v=tessera1;profile=tessera-v1-strict;kms=d1b35a0e5273912ee85c7f88ee97929cef311e7854ad30c58faa3e0250c4a7a4;gpg=b6e37f7c8120ca19cca86cc9617d4ec50b2875a799ee976d9d0253e01c7a077c;issuance-not-before=<T>;issuance-not-after=<T>`.
   These fingerprints were computed offline from `spike-pq/out-kms` and `out-gcp` capture.json. They are valid
   only if those two keys sign. The `frames` stage refuses until this record validates.
4. **Slot-2 signer** (owner): confirm the Cloud Run job, its scheduler and the two SQS queues are still deployed.
   Its pinned `KEY_FP` must be `gpg-sha256:b6e37f7c…077c` and `ALLOWED_ALGS` must hold the pair id. The `sign`
   stage then sends two frames through the queue (attest and manifest). This needs the same AWS login.
5. **Wall clock**: about 70 min for the git stamp to reach k = 6, then about 70 min for the receipt and snapshot
   proofs (one spike data point each). Rerun `run` until it exits 0. Exit 75 means still waiting.
6. The real run uses the throwaway TEST repository key, not YubiKey 2.
