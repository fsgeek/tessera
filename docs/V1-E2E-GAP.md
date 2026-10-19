# V1 end-to-end gap list: first real receipt, TEST-signed verifier

Date: 2026-10-19. Author: gap-list agent (read-only survey; nothing built).
Goal: one real V1 receipt issued on AWS, verified VALID_STRICT by a packaged verifier from a TEST-signed release.

How to read the labels. EXISTS means I read the file and it does the job as a prototype. PARTIAL says what is
missing. MISSING means I found nothing. "Checked" means I ran a command or read the file. "Prediction" means I did
not check it. Effort numbers are predictions.

Checks I ran today (2026-10-19):
- `dig +dnssec wamason.com DNSKEY` and `dig DS wamason.com` against the local stub resolver (127.0.0.53) gave SERVFAIL.
  That is a resolver problem on this machine, not evidence about the zone.
- The same queries against 1.1.1.1 worked. DNSKEY: two keys (flags 256 and 257), algorithm 13. The resolver set the
  `ad` flag. The DNSKEY RRSIG runs 2026-10-08 to 2026-12-08. DS at `.com`: key tag 2371, algorithm 13, digest type 2.
  Algorithm 13 and digest type 2 are inside the profile's supported set (V1-PROFILE.md:560-567). The zone is hosted
  at Cloudflare (NS kanye/courtney.ns.cloudflare.com).
- `dig @1.1.1.1 +short TXT _tessera-v1.wamason.com` returned nothing. The key-assertion record is not published.
- HTTPS to alice.btc, bob.btc (opentimestamps.org) and finney (eternitywall.com) calendars returned 200.
- Installed: `ots`, `gpg`, `git`, `aws`, `gcloud`, `uv`, Python 3.14 (in `.venv`). `aws sts get-caller-identity`
  failed with NoCredentials, so I could not check the AWS or GCP resources. Whether they still exist is a prediction.
- `git ls-tree HEAD` shows no `tessera-v1/` path in this repository. The repository has no Lambda, API Gateway,
  Terraform or other service code (grep and `git ls-files`).

## 1 and 2. Steps, in order, with status

Phase A: external prerequisites (no code needed from the verifier side).

| # | Step | Status | Evidence / what is missing |
|---|---|---|---|
| A1 | DNSSEC on wamason.com (alg 8 or 13, DS digest 2 or 4) | EXISTS | Checked above. Signed, DS present. Leaf RRSIG windows are short (about 2 days; joint window measured 26.4 h on 2026-10-09: `prototype/spike/SPIKE-REPORT.md` "Snapshot vs RRSIG window"). The snapshot must be anchored inside that window. |
| A2 | Publish TXT `_tessera-v1.wamason.com` (exact 255-byte ENC §7 value: kms fp, gpg fp, profile, window not-before and not-after, 90 days at most) | MISSING | Checked: empty. Needs the final key fingerprints first (A3, A4) and a Cloudflare DNS edit by Tony. A published window cannot be shortened (V1-PROFILE.md:643), so choose dates with care. |
| A3 | AWS KMS key, slot `kms`, ML-DSA-65 (hybrid branch registered 2026-10-16) | PARTIAL | Spike key `alias/tessera-pq-spike`, account 477139661040, us-east-2 (`prototype/spike-pq/REPORT.md`, KMS half). It signed genuine V1 hybrid frames with EXTERNAL_MU. The report says spike keys are kept only until the supplement review clears. No production-named key, no key policy for the issuer role. Existence today: prediction (no credentials). |
| A4 | GCP slot-2 signer (policy signer, HSM P-256, queue from AWS) | EXISTS (deployed spike) | `prototype/policy-signer/EVIDENCE.md`: queue to Cloud Run job to HSM, 3 to 70 s latency, refusals for epsilon, tag and key_fp all shown. Key is `slot2-spike` v1, fingerprint pinned in the signer. `ALLOWED_ALGS` holds only the hybrid pair id. If A3 or the gpg key is rotated, the pinned fingerprint and the job must be redeployed. Still running today: prediction. |
| A5 | Git channel repository with `tessera-v1/key-assertion` (blob byte-equal to the DNS value, no trailing LF), signed commit by the repository key, OTS-stamped on the commit id | MISSING | No such path or repository exists (checked). The verifier side exists (`prototype/tessera_proto/real/gitchannel.py`); the synthetic builder is `conformance/issue.py` `build_git`. Profile §14.2 item 6 asks that the repository root be P-256. YubiKey 2 arrives 2026-10-20 (handoff). |
| A6 | Wait until the git stamp has k=6 (`h_git+5` mined); upgrade the proof; validate it offline; record `h_git` | MISSING as a procedure | Rule: V1-OPERATIONS-RUNBOOK.md §5 and V1-PROFILE.md:341-347. Spike latency: 20.4 min to first attestation, 68 min to k=6 (`prototype/spike/out/latency.json`). That is one data point. |
| A7 | OpenTimestamps calendars | EXISTS | Reachable (checked). `ots` installed. Used successfully in the spike. |
| A8 | SHA-1DC detector | PARTIAL | Source pinned and vendored (`prototype/vendor/SHA1DC-PIN.md`, commit a06f1ad). `indep-verifier/sha1dc.py` shells out to a locally built `sha1dcsum` whose SHA-256 is pinned. The binary is git-ignored and compiler-dependent, so a packaged verifier must ship or build it. `indep-verifier/README.md` still says the build cannot return VALID_STRICT; that text is stale (the REPORT addendum and diff run 1 show 52/52 VALID_STRICT with the hook). |
| A9 | Real trust configuration values (§15.5 schema) | MISSING | The only real-data configs are the old spike form (`prototype/spike/trust-config.json`), not §15.5. Needed: both root KSK RDATA with archived sources, signing starts and ends (the KSK-2017 start is still OPEN, §14.2 item 3), the repository key entry, `as_of`, and header pins for every height used by the three proofs. The pins cannot exist until the three proofs are anchored. |
| A10 | Frozen catalog and the four hashed objects: spec object (§15.8 part format), vectors object, preamble, dependency manifest | MISSING for real | Only TEST stand-ins exist (`prototype/conformance/universe.py` ~l.596-654). No assembler script exists (grep for `tessera-v1-part` finds only universe.py). The spec hash, vectors hash and preamble hash are inside the signed bytes, so they must be fixed before step B3. |

Phase B: issuance (profile §4 order).

| # | Step | Status | Evidence / what is missing |
|---|---|---|---|
| B1 | Client submits bytes to an operated API (API Gateway, Lambda, KMS) | MISSING | No service code, no client. A9 names the shape (phase-0-prereg-amendment-9.md:164). Nothing else in the chain needs an API; a script can stand in (see plan). |
| B2 | Fix manifest and common metadata, `declared_issue_time` | PARTIAL | Synthetic: `conformance/issue.py`. Real hybrid frames: `prototype/spike-pq/spike_v1_hybrid.py`. Both use TEST or spike inputs, not the frozen hashes. |
| B3 | Build both frames (ENCODING-V1 codec) | EXISTS | `formal/p8/` reference encoder (`gen.py`), also vendored in `policy-signer/signer/p8_codec.py`. |
| B4 | Sign `kms` frame and possession (AWS KMS ML-DSA-65, EXTERNAL_MU above 4 KB) | PARTIAL | Works from a laptop with credentials (`spike_v1_hybrid.py`, EVIDENCE.md item (a)). Not in a Lambda; no issuer role or key policy. |
| B5 | Sign `gpg` frame and possession via SQS to the GCP policy signer | EXISTS | `prototype/policy-signer/client.py`. |
| B6 | Verify both signatures on the exact bytes, freeze, build `A_sig`, stamp `SHA256(A_sig)` (one stamp) | PARTIAL | Pieces exist: `spike_v1_hybrid.py` computes the anchor digest; `ots stamp` works. No driver does it for real material and keeps the proofs. |
| B7 | DNSSEC snapshot: capture live chain, convert to the §15.3 wire body, check no wildcard RRSIG and the joint window, stamp with its own proof | PARTIAL | Capture: `spike/capture_dns.py` (old JSON form; profile says each snapshot needs conversion and a fresh stamp, V1-PROFILE.md:861-863). Serializer for the §15.3 body exists in `conformance/universe.py` but builds from the synthetic hierarchy. Needs a live-resolver to §15.3 converter. |
| B8 | Wait for the receipt and snapshot proofs to reach k=6; upgrade; check c1 to c3, `h_git+5 < h_receipt`, tx-shape and merkle-suffix subset on all three proofs | PARTIAL | Checks exist in `conformance/issue.py` `preship()` and in the verifier. Header fetch with two-source agreement: `spike/finalize.py`. No real-material driver. |
| B9 | Assemble the canonical JCS container (§15.1) and ship | PARTIAL | `conformance/issue.py` does it for the synthetic universe. Real inputs are not wired. |

Phase C: release and verify.

| # | Step | Status | Evidence / what is missing |
|---|---|---|---|
| C1 | Build the trust configuration (A9) with pins for the three proofs, hash it; compile hash and catalog into a release | PARTIAL | `indep-verifier/build_release.py` rewrites `release_constants.py` with the trust hash, catalog bytes and Unicode binary hash. It states that it signs nothing. |
| C2 | TEST release record, signed by a TEST release key; verifier refuses an unsigned or foreign-signed config | PARTIAL | Format `tessera-v1-test-release/1` and signer are in `conformance/universe.py` `make_release`. The check that reads `TESSERA_V1_TEST_RELEASE` and `..._KEY` is in `differential/adapter.py` (T1) and `conformance/run.py`, not in `indep-verifier/verify.py`. The adapter note 1 says this plainly. A packaged verifier has no release signature check yet. The release format is OPEN until the 30 Oct freeze (V1-PROFILE.md §14.2 item 2). |
| C3 | Package the verifier (archive, Python 3.14 plus Unicode 16.0.0 binding, SHA-1DC binary, dependencies) | MISSING | Only a `.venv` instrument. No archive or install procedure. |
| C4 | Relying party runs `verify --trust --bundle` and gets VALID_STRICT | PARTIAL | The verifier decides all 60 checks (REPORT.md). 342/342 agreement with the conformance suite on synthetic material (`prototype/differential/results-run5.json`). It has never seen real mainnet-pinned, real-DNSSEC, real-KMS input. |

## 3. Which A10 items a TEST-signed release needs

Status of A10 itself. The author's rulings are recorded (A10:24-32). The handoff says A10 awaits his signing commit,
and `docs/phase-0-prereg-amendment-10.pdf` is untracked in git. I did not check whether it is signed. The profile
has no `service_keys` or `utc_assessment` text yet (grep count 0, V1-PROFILE.md), and neither verifier implements
them (grep of `prototype/` found no hit in code). The handoff schedules this for before the 30 Oct freeze.

**Custody gate (A10.4.2): not required for a TEST release used by testers.** Governing lines:
- A10:635-636: "**When: the first public verifier release, not the freeze.**"
- A10:644-645: "Every verifier release made before that gate is signed with a separate TEST release key."
- A10:650-651: "*Offering restriction.* No pre-gate artifact is offered for production reliance: pre-gate releases are
  offered only as TEST releases, never as releases on which relying parties may rely."
- A10:148-150: "The service must not offer an early release for real use."
- Required before the first public release only: the rehearsal at A10:652-654 and the independence record.

So a TEST release for the 4 Dec tester, labelled as TEST, is allowed. It must not be offered for reliance.
Unclear point (I will not guess): V1-SCHEDULE.md says testers use "the verification tool", and A10:650 says pre-gate
artifacts are not "offered for production reliance". I read a tester exercise as not reliance. Tony should confirm.

**Service-key listing (A10.4.1): the text has no TEST exemption. Unclear whether it binds a TEST release.**
- For it: A10:486 "No receipt ships under keys that are not listed in a published release." A10:765 and :775 (rows
  29, 39) add that "Every verifier release is OpenTimestamps-stamped" and that before issuing, "an installed
  configuration with coverage of the stamp of the release that first lists the exact entry is available ... the
  receipt selects a height strictly greater than h_C0+5." A10:582-584: "V1's configuration lists exactly one entry,
  authorized at the freeze."
- Against: A10:769 (row 33) makes the listing the "second item cut" and says if it is cut "A10.4 option (a) applies
  and the absence of new-key protection is stated." That is a stated cut path, not a TEST carve-out.
- What follows (my reading, not text): if the TEST verifier implements A10, a receipt passes only with a matching
  `service_keys` entry, and honest issuance needs the C0 then C1 bootstrap (A10:516-529): publish C0, stamp it, wait
  six blocks, publish C1 with those six pins, then issue at a height above h_C0+5. That adds one more OTS wait and
  one more release before the first receipt. If the TEST verifier is built to the pre-A10 spec, no listing is needed,
  but then its spec hash differs from the one A10 says changes (A10:609 "The specification hash changes").
  Because the spec hash is inside the signed bytes, the choice must be made before the first receipt is signed.

**`utc_assessment` (A10.1.1): not required for VALID_STRICT.** A10:212: "It enters no verdict, no reason code and no
stable field." The output contract is A10:300-303. It changes the spec and catalog hash (constants Δ = 7200 s, m = 6),
so the same ordering point applies. It needs about 20 lines in a verifier. A TEST verifier can omit it only if its
spec object is also the pre-A10 one.

**Production-only (not needed for a TEST release):** the production release key and its bootstrap record (A10:669-673),
the custody procedure review, the TEST-refusal rehearsal, and the retained listing-evidence package for third parties
(A10:538-562). Last item: the package is described as "installed" with the trust file, so a TEST verifier that
implements the listing would still need a minimal one. Whether a minimal package is acceptable for TEST is unclear.

## 4. Shortest ordered build plan (effort is a prediction)

1. Decide the A10 question for the TEST build: pre-A10 spec for the first receipt (fast) or A10 with listing.
   Decision only; 0.5 h of Tony's time. Recommendation in section 5.
2. TEST freeze of objects at one named commit: assembler for §15.8 parts, spec, vectors, preamble, dependency manifest,
   catalog, hashes recorded outside the parts. 1 to 2 days. Needed before any signing.
3. Real-material trust config builder (§15.5): archive root KSK sources, pins script from `spike/finalize.py` logic,
   repo key entry. 1 day, plus the sourcing work left open in §14.2 item 3.
4. Pick the TEST repository key (throwaway P-256 key via GnuPG) and a git repository; write the blob; sign; stamp;
   wait for k=6 (about 70 min if latency matches the spike). 0.5 day including the wait. Swap in YubiKey 2 later.
5. Publish the TXT record in Cloudflare (Tony, 15 min) with the chosen window.
6. Issuer driver script on real material (this is the missing code): frames, KMS sign, SQS to GCP, verify, `A_sig`,
   stamp, snapshot capture and §15.3 conversion and stamp, wait for k=6, checks c1 to c3, header fetch, container.
   3 to 5 days. Reuse `issue.py`, `spike_v1_hybrid.py`, `client.py`, `capture_dns.py`, `finalize.py`.
7. Add the `TESSERA_V1_TEST_RELEASE` and `_KEY` check, with the `tessera-v1-test-release/1` signature, into
   `indep-verifier/verify.py` (lift from `differential/adapter.py` T1 and `universe.make_release`). 0.5 day.
8. Build the release: trust config with the real pins, TEST-sign it, ship `sha1dcsum` build, a pinned Python 3.14
   environment, and a one-command install. 1 to 2 days.
9. Issue the receipt, wait for k=6, assemble pins into trust config v1, build release, run the verifier. Expected:
   VALID_STRICT. Wall clock about 3 hours of waiting spread over two OTS cycles.
10. Add the Lambda and API Gateway shell around the driver. 2 to 4 days. Not needed for the first verified receipt;
    do it for the 20 Nov milestone.

Total to first verified receipt without the API shell: roughly 8 to 12 working days. With the A10 listing in the
TEST verifier add about 4 to 5 days (the handoff's own estimate for listing plus utc_assessment in the profile and
both verifiers) and one more OTS cycle.

**Single biggest blocker:** there is no issuer driver for real material. Every end-to-end path in the repository
runs on the synthetic universe or on spike scripts. Nothing joins real KMS, the GCP signer, live DNSSEC, a real git
commit and real OTS proofs into a bundle that a release can then pin. The frozen-object hashes (step 2) are the first
thing the driver needs, because they go into the signed bytes.

## 5. Required by the text but unnecessary for the first working receipt (OPINION)

- The service-key listing and its C0/C1 bootstrap. It adds a release, a stamp and a wait to a path whose goal is one
  receipt. Build the first receipt on the pre-A10 spec object, and add the listing in the same release series as the
  freeze work. A10:769 already treats the listing as cuttable. Risk: the first receipt carries a spec hash that
  later verifiers will not list, so it is a pipeline proof, not a keepsake.
- `utc_assessment`. No verdict effect.
- YubiKey 2 and the offline root ceremony for the repository key. A throwaway P-256 key exercises the same verifier
  path, and the runbook calls repository custody "an operating fact, not verifier policy" (V1-PROFILE.md:537-538).
- Production-quality slot-2 custody choice and the HSM monoculture check (runbook §1, profile §14.2 item 5). The
  deployed spike signer already meets the pass condition.
- The API Gateway and Lambda shell. A script on Tony's machine with the same credentials proves the chain.
- Conformance case locator refresh (about 281 stale `P:nnn` citations) and the full release-key custody procedure.
- The 24 to 96 h retirement margin, successor-window and rotation machinery, and exit procedure.
