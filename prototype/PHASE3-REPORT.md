# Phase 3 report: real mechanisms in place of the stubs (throwaway prototype)

*2026-10-07. Built by a Claude Opus 5.5 agent on top of the phase-1 and phase-2 code. THROWAWAY: not
service code, and none of it may be copied into the service. Nothing is staged or committed.
Reproduce with `cd prototype && uv sync && uv run pytest -q` (75 pass: 25 + 25 + 25 new in
`tests/test_phase3.py`) and `uv run python run_phase3.py`. New code is in `tessera_proto/real/`.
The stub path is still the default. To use the real path, set `TESSERA_PROTO_MODE=real` (for
example, `TESSERA_PROTO_MODE=real uv run python run_phase2.py`) or call `scenarios.build("real")`.
Spec citations are to `docs/implementation-spec.md`.*

## Outcome

Real mechanisms did not break the core result. The two attack replays behave exactly as before on real
signatures: C-C2 is rejected by V17/V18, C-C5 is rejected by V19, and each is accepted once its
companion check is removed. The 20-run relying-party matrix from phase 2 comes out the same.

They did show that the model is wrong, or silent, in several places that matter:

1. **Third parties can change signature bytes, and that breaks standing.** The model treats a
   signature as a fixed term. A real ECDSA signature can be turned into a second valid one by anyone
   (replace s with n − s). An OpenPGP signature has an unsigned subpacket area that anyone can edit.
   The attempt identity is a hash over the signature bytes (R-3.25). So a mirror can turn an honest
   `ESTABLISHED` receipt into `ABSENT / STANDING_EVIDENCE_MISMATCH`, while every envelope check
   still passes. Ed25519, the only algorithm the stub used, is immune, which is why the stub hid this.
2. **The DNSSEC channel's key is not the issuer's key.** The model gives each channel its own
   verification key. In real DNSSEC, the key an offline verifier holds is the IANA root key, and it
   validates every signed name on the internet. What ties a snapshot to wamason.com is the record's
   owner name. Nothing compares that name with anything, and the spec calls the issuer identity
   "bound, not validated". Separately, **wamason.com is not DNSSEC-signed today**: `.com` returns a
   signed proof that no DS record exists. The registered evidence 1 (R-4.26) cannot be produced at all.
3. **A real OpenTimestamps proof is not "one anchor".** Each of the repo's Bitcoin-anchored stamps
   carries four attestations, at four heights, through four different transactions. The candidate
   `anchor_time` values span 8.6 h in one stamp and 12.6 h in the other. The proof contains no
   header, no time, no depth and no txid field. All of those come from outside.
4. **KMS and GPG cannot sign "the same canonical bytes" under one algorithm id without giving
   something up.** OpenPGP signs the frame plus a trailer of signer-chosen metadata, never the frame
   alone. The natural pairing, KMS ECDSA with a gpg OpenPGP signature, is `INVALID` under R-3.12's
   equal-algorithm rule. Two pairings pass:
   - make KMS produce OpenPGP signatures. The KMS custodian then signs a 32-byte digest it cannot
     interpret;
   - make gpg-agent produce raw ECDSA. That is no longer an OpenPGP signature.
5. **The precision rule's wording is not what JCS needs.** RFC 8785 gives `9.8` a canonical form.
   What JCS cannot handle is a number whose *value* would change on the way through a double. Under
   that reading (adopted here as "value-preserving"), the phase-2 SBOM with CVSS 9.8 is accepted
   inline.

One consumer outcome changed because of these mechanisms: the malleated receipts (finding 1), which
the careful integrator now falsely rejects. Two others changed because of rule choices made in this
phase: the inline SBOM is accepted (finding 5), and the 2106 examiner's blockers moved (see
"Consumer outcomes").

## What was built (`tessera_proto/real/`)

| Module | Real mechanism | What stays emulated |
|---|---|---|
| `canonical.py` | RFC 8785 Appendix B number vectors (24); three readings of the precision rule; comparison with the `rfc8785` package (Trail of Bits) | — |
| `openpgp.py` | RFC 4880 / RFC 9580 v4 signature and key packets: parse, build, verify with `cryptography`, v4 fingerprints | v6 packets (gpg 2.4.4 makes v4 only) |
| `kms.py` | AWS-KMS Sign semantics: ECDSA_SHA_256 and RSASSA_PSS_SHA_256; RAW (≤ 4096 B) vs DIGEST | KMS itself: local `cryptography` keys; AWS behaviour taken from its documentation, not verified |
| `gpg.py` | `/usr/bin/gpg` 2.4.4 in a throwaway `GNUPGHOME` under `prototype/.gnupg-phase3/` (removed on exit); detached signatures; gpg-agent `PKSIGN`; a KMS-backed OpenPGP key that `gpg --import` accepts | — |
| `btc.py`, `ots.py` | python-opentimestamps 0.4.5. The repo's real stamps are verified against 151 archived mainnet headers (PoW and linkage checked). Real-format OTS proofs are built on a regtest chain: nonce, calendar merkle tree, OP_RETURN transaction, block merkle path, `BitcoinBlockHeaderAttestation` | Chain difficulty: REGTEST (`nBits 0x207fffff`), so PoW proves nothing for new receipts. Retarget validation is not implemented |
| `anchor.py` | Verifier stage (h) and standing step 8 over OTS. Same check ids as the stub | — |
| `dnssec.py` | dnspython RFC 4033–4035 validation, offline, at a chosen time. Captured on 2026-10-07 from 1.1.1.1: the wamason.com and ietf.org chains (`fixtures/`, plus `dig +dnssec` text) | Not wired into issuance (wamason.com is unsigned) |
| `gitchannel.py` | The real signed commit 03cd3db: the signed payload rebuilt, the OpenPGP signature verified without gpg, SHA-1 ids for commit → tree → blob | Not wired into issuance |
| `pairings.py`, `world.py`, `rerun.py` | The de-stubbed world: slot A is KMS-backed OpenPGP (P-256), slot B is a real gpg nistp256 key, both `OPENPGP4-ECDSA-P256-SHA256`; anchor is OTS on regtest | **Authority channels are still Ed25519 stubs**; DSKS is still emulated |

Phase-1 and phase-2 code was edited only at hooks, and every hook's default leaves stub behaviour
unchanged:
- `jcs.NUMBER_RULE`;
- `crypto.EXTRA_VERIFIERS`, and the DSKS oracle now records the honest key's algorithm;
- the `TrustConfig.header_policy` field;
- an OTS branch in `verifier._temporal` and in `standing` step 8;
- `issuer.anchor_layer` delegates to a chain that offers `anchor_receipt`, and `Issuer.issue` passes
  the slot key's algorithm;
- `attacks.replay_cc02` takes an optional `keygen`;
- `examiner` gains `_sig_ok` and an OTS branch;
- `scenarios.build(mode)`;
- `tests/test_phase2.py` now pins `build("stub")`.

## Item by item

### 1. Canonical form

**What the spec names.** RFC 8785, "adopted with the precision rule closing its gap" (R-3.1). The
precision rule says "any value not exactly a double ... is string-encoded" (R-3.2). R-3.4 lists
"numbers not exactly representable as IEEE 754 doubles" among the inputs that must be rejected. The
prereg calls JCS's "one sharp edge" that "numbers must be exactly representable".

**What RFC 8785 does.** It parses every number to the nearest double (the I-JSON model, RFC 7493 §2.2)
and prints it with ECMAScript's shortest round-trip algorithm. `9.8` canonicalizes to `9.8`. JCS also
rewrites number spellings: `9.80` becomes `9.8`, `1E2` becomes `100`, `-0` becomes `0`. So JCS is itself
a normalizing function on lexical form, and R-3.4's "never helpfully normalized" cannot mean "no
lexical change".

| Literal | literal (phase 1, G-03) | value-preserving | `rfc8785` package |
|---|---|---|---|
| `9.8` | REJECT | `9.8` | `9.8` |
| `5e-324` (an RFC 8785 Appendix B value) | REJECT | `5e-324` | `5e-324` |
| `333333333.33333329` | REJECT | REJECT (value would change) | `333333333.3333333` — **silently changes the value** |
| `123456789012345680000` | REJECT | accepted | REJECT (outside ±(2^53−1)) |
| `-0` | REJECT | REJECT | `0` |

**What a standard choice implies.**
- The value-preserving reading is the one the precision rule's own examples point at (hashes, 256-bit
  integers, addresses).
- It accepts the phase-2 SBOM.
- It refuses exactly the inputs JCS would alter.
- Adopting it means R-3.4 must say "numbers whose value is not preserved by RFC 8785 serialization",
  and that "no normalization" means no *value* change.
- The three implementations agree on output bytes for all 24 Appendix B vectors, but not on which
  inputs they accept. Only R-3.6's negative vectors can pin that. "Bind to an existing standard"
  alone does not.
- The phase-1 subnormal rule (G-03b) refuses an input RFC 8785 itself treats as ordinary.

### 2. Signatures

**Exactly which bytes are signed.**
- **KMS ECDSA_SHA_256, RAW:** ECDSA over SHA-256(frame). KMS sees the frame.
- **KMS DIGEST:** the caller sends SHA-256(frame), and KMS never sees the frame. DIGEST is forced
  above 4096 B, and the KMS-backed OpenPGP slot always uses it. The signature still verifies over the
  frame with an ordinary verifier. So "signs the frame bytes" holds at the verifier, but the
  independent custody domain checks nothing about content.
- **RSA-PSS:** randomized, salt 32.
- **OpenPGP v4 (gpg):** the hash input is `frame ‖ hashed_header ‖ 0x04 0xFF ‖ len`. The
  hashed header holds the signer-chosen creation time and the issuer fingerprint.
  - ECDSA signs that hash. Raw ECDSA over the frame fails, as the tests show.
  - For gpg 2.4's default ed25519 key, Ed25519 signs the 32 *digest bytes*. It verifies over neither
    the frame nor frame ‖ trailer, only over SHA-256(frame ‖ trailer).

**Does "signs the frame bytes" hold?** Only if the verification primitive is "OpenPGP signature over
document fb". If it is, V19 holds for the GPG slot. The trailer is then signed metadata outside the
frame, and OpenPGP verifiers use its creation time to judge key expiry and revocation (R-3.39).

**Does the same-algorithm rule block a realistic pairing?** Yes (P1 and P2 `INVALID` on V13, V16, V19,
V24). Only two pairings pass:

| Pairing | Result | Cost |
|---|---|---|
| P1 KMS ECDSA + gpg OpenPGP (P-256) | `INVALID` | — |
| P2 KMS ECDSA + gpg OpenPGP (Ed25519, gpg's default) | `INVALID` | — |
| P3 KMS ECDSA + gpg-agent `PKSIGN` over SHA-256(frame) | `VALID_STRICT` | The GPG slot is a raw DER signature; `gpg --verify` cannot check it. The "portable WHO layer" is gone |
| P4 KMS-backed OpenPGP + gpg OpenPGP | `VALID_STRICT` (the de-stubbed world) | KMS signs an uninterpretable digest. The KMS key needs an invented OpenPGP creation time, and its v4 fingerprint (the one DNS and git would publish) depends on it |

**Malleability** (finding 1). This holds for ECDSA (both KMS and OpenPGP) and for every OpenPGP
signature through its unhashed area. It does not hold for RSA-PSS (randomized, but only the signer
can re-sign) or for Ed25519 under RFC 8032 (`cryptography` rejects s + L).

**DSKS** stayed emulated. Two real-mechanism facts are relevant:
- OpenPGP v4 signatures already hash the issuer's fingerprint. That is an existing key-binding
  defence the spec does not use.
- An *inline* OpenPGP message (`gpg --sign`, gpg's default mode) carries the signed content inside
  the signature. That is the "message recovery" phase 1 had to invent (G-41) for the C-C5 mutant to
  be expressible. A GPG slot built on inline signing would make that bug class natural.

### 3. Anchor (OpenTimestamps)

Test vectors: `timestamps/anchored/03cd3db…` and `fcaa11b…` (copied to `fixtures/`), with mainnet
headers 956576–956644 and 959013–959094 fetched once from Blockstream's API. The tests check every
header's PoW and linkage, so the API is not trusted.

| Spec | What the OTS proof gives |
|---|---|
| "exactly one anchor proof ... together with the anchor transaction's id" (R-3.42) | One file, **four** Bitcoin attestations (heights 956582/586/620/639), four distinct txids, plus four `PendingAttestation`s. The txid is not a field: it is implicit in the operations. Each transaction is a calendar's aggregation transaction, shared with every other stamp in that round |
| `anchor_time` = "the Bitcoin block time of the OTS anchor" (R-3.44) | Four candidates, spanning 8.6 h (03cd3db) and 12.6 h (fcaa11b). This prototype takes the **earliest** verified attestation (G-55), the strongest true "existed by". The proof is outside the signed bytes, so a presenter can prune attestations. Under "earliest", pruning can only move `anchor_time` later; under any other rule the presenter chooses it. Which one is used decides V33–V35 near their bounds and decides REV (R-5.21) |
| k-confirmation depth (V36), `confirmed_at` (V35) | Not in the proof. Headers h … h+k−1 must come from the bundle or a store |
| Header store (R-2.19, V38 "not specified") | Authentication needs PoW, linkage, retarget rules and a pinned checkpoint. Two policies are built: phase 1's "pin every header" and R-3.48's candidate "checkpoint+pow". Under the second, a verifier with an old store accepts new headers only if the bundle carries every header from the store's tip to h+k−1 (80 B each). R-3.48's "embed the k-header segment" is enough only when the store is at most one block stale. The full mainnet header chain is about 77 MB (≈ 956,600 × 80 B), and growing about 4 MB a year |
| One anchor, two frames (G-19 / K-2) | `ots stamp a b` aggregates two files into one commitment but yields **two** proofs, one per file. "Exactly one proof over its canonical bytes" is satisfiable only by stamping a constructed preimage (G-19 kept) |
| Issuer anchors and re-anchors (R-4.48–R-4.51) | The issuer never owns a transaction. It submits a digest to calendars (live third-party services) and polls them to upgrade the pending proof. Calendar availability is an unnamed *issuance* dependency (not a P9 one) |
| A 2106 examiner | Bitcoin's `nTime` is a uint32 that ends at 2106-02-07T06:28:15Z. 2026 headers stay readable, but re-anchoring after that date needs a consensus change |

### 4. Authority channels

**DNSSEC** (captured 2026-10-07; validated offline with dnspython):
- wamason.com is `INSECURE`. `.com` signs an NSEC3 denial of any DS record, so no DNSSEC evidence for
  the issuer exists.
- ietf.org (the positive control) is `SECURE`, validated from the root KSK 20326 alone.
- Every RRSIG on the ietf.org chain is valid *together* only for **1.6 days**; for the wamason.com
  denial chain it is 5.4 days.
- Validated at a 2106 clock, both chains are `BOGUS` (expired). RFC 4035 §5.3.1 checks the current
  time.

An offline 2106 verifier must archive:
- every DNSKEY, DS and RRSIG from the root down. That is about 4.2 KB of wire for ietf.org;
- the 2026 root KSK;
- implementations of DNSSEC algorithms 8 (RSA/SHA-256) and 13 (ECDSA P-256), both used on these
  chains;
- **an authenticated time inside every window.** That means the snapshot needs its own OTS anchor,
  made within days of capture. A receipt holds "exactly one anchor proof" (R-3.42), so this is a
  second proof the spec does not count.

**git** (commit 03cd3db, verified offline without git or gpg):
- The signature covers the commit object **minus** its `gpgsig` header. The commit id (SHA-1) covers
  the signature.
- The commit's dates and the signature creation time are both asserted by the signer (equal here).
- The repo's own OTS stamp covers SHA-256 of the 41-byte text "<commit id>\n". Time and content are
  therefore linked only through **SHA-1** (commit → tree → blob), and SHA-1 is not in the bundle's
  dependency manifest.
- The proof material for one file was 35 KB (commit, two trees, the blob, and the signature).
- **Nothing in this evidence shows the commit was ever public.** An unpushed commit gives identical
  bytes. The channel's root is the commit-signing key, which the author holds (R-2.15).
- That key (`…42C73835`, expires 2026-12-07) follows OpenPGP revocation semantics, not R-5.21's:
  - "key compromised" invalidates every signature regardless of time;
  - expiry is judged against the signer's own creation time.

## MISMATCHES

Consequence: **GUARANTEE** means a modelled property fails, or is vacuous, once the real mechanism is
used. **ASSUMPTION** means the spec or model assumes something the standard does not give; a stated
rule is needed. **IMPL** means a builder choice the spec must pin, with vectors.

| # | Standard | Spec location | What the spec / model assumes | What the standard does | Consequence |
|---|---|---|---|---|---|
| 1 | ECDSA (FIPS 186-5; AWS KMS ECDSA_SHA_256), RFC 4880/9580 §5.2.3 unhashed subpackets | R-3.25, §5.1 "Attempt core" row, R-6.24 step 3 | Signatures are fixed terms (`sign(m,k)`), so `aid = h(t, ppf, sg, decl)` is stable | Anyone can produce new valid signature bytes: (r, n−s), or an edited unhashed area | **GUARANTEE**: a third party turns honest `ESTABLISHED` into `ABSENT / STANDING_EVIDENCE_MISMATCH` (m1–m3) with every envelope check passing. Holds for every non-Ed25519 slot |
| 2 | RFC 4033–4035 (root trust anchor, owner names) | R-2.21 (`pk(skS)` per channel), R-2.18, R-3.36 "bound, not validated" | The DNS channel's verification key is specific to the issuer's channel | The offline trust anchor is the root KSK, which validates every signed name. Binding to wamason.com is by RRset owner name only | **GUARANTEE**: as modelled, anyone with their own signed domain mints evidence that verifies under "the DNS channel key". A real verifier must pin the owner name, a check absent from both spec and model |
| 3 | RFC 4035 §5.3.1 (RRSIG inception/expiration) | R-3.32, R-4.26 "chain to the root as it existed at issue time"; R-2.18 | An archived snapshot verifies later against archived root keys | RRSIGs live for days (here the joint window is 1.6 days); validation at a later clock is `BOGUS` | **ASSUMPTION**: the verifier must validate at an authenticated time inside every window, so the snapshot needs its own anchor. The spec names neither the time nor that second proof |
| 4 | DNSSEC deployment (wamason.com, 2026-10-07) | R-4.26 evidence 1; R-2.12 | The issuer's DNSSEC records exist | `.com` proves no DS for wamason.com (NSEC3 opt-out): the zone is unsigned | **IMPL / operational**: no receipt can be `VALID_STRICT` until DNSSEC is enabled and the fingerprint records are published |
| 5 | git object format + OpenPGP; OTS stamping in this repo | R-4.27, R-2.10, R-3.51 | The repository channel evidences a *public* publication, time-anchored, with SHA-256-era hashes | The evidence is "this key signed this commit, and the commit id existed by the OTS time". Publication is not evidenced. Content is reached through SHA-1 | **ASSUMPTION**: the channel is a second author-held key plus a timestamp. SHA-1 is an undeclared dependency |
| 6 | RFC 4880 §5.2.4 / RFC 9580 (v4 signature trailer; EdDSA over the digest) | R-2.1, R-4.13 "both over the same canonical bytes"; V19 `checksign(sg,kX) = (BYTES, fb)` | The GPG signature is over the frame | OpenPGP signs H(frame ‖ hashed header). Ed25519 keys sign the digest bytes. Creation time and issuer fingerprint are signed metadata outside the frame | **ASSUMPTION**: V19 holds only with "OpenPGP over document fb" as the primitive. Then signed, interpretation-relevant metadata sits outside the envelope (R-3.39) |
| 7 | AWS KMS key specs and Sign; OpenPGP | R-3.12 / R-4.16 (one algorithm across slots), R-3.36 (one `alg` per tuple), versus R-2.1 | KMS + GPG can co-sign one receipt | Natural pairings are `INVALID` (P1, P2). Only all-OpenPGP (P4) or no-OpenPGP (P3) pass | **ASSUMPTION** (K-3 confirmed by construction): the design must choose, and each choice gives up part of R-2.1's rationale |
| 8 | AWS KMS Sign MessageType (RAW ≤ 4096 B, DIGEST) | R-4.13 "KMS signs the cloud receipt"; independent failure domains | The KMS custody domain signs the frame | Frames over 4 KB, and every OpenPGP-framed KMS signature, go as a 32-byte DIGEST the custodian cannot interpret | **ASSUMPTION**: independence is key custody only; the custodian checks nothing about content (emulated; AWS limits from AWS documentation) |
| 9 | RFC 4880 §12.2 v4 fingerprint (SHA-1 over a key packet including creation time); KMS SPKI | R-3.11 "key fingerprint", R-4.26/R-4.27 published fingerprints, G-10 | One fingerprint per key | Three for the same key: the OpenPGP v4 fp, the SPKI/KMS identity, and Tessera's fp. A KMS key's OpenPGP fp depends on an invented creation time | **IMPL**: the spec must say which fingerprint the channels publish and the frame pins |
| 10 | OpenTimestamps proof format | R-3.42 "exactly one anchor proof ... the anchor transaction's id"; §3.5 table | One proof, one transaction, one block | Four attestations, four transactions (shared calendar transactions), four blocks; no txid field | **ASSUMPTION**: "the txid" and "the anchor" are undefined for a real proof. G-55 is needed |
| 11 | OTS + Bitcoin `nTime` | R-3.44, V33–V35, R-5.21 | `anchor_time` is one number | Candidates span 8.6 h and 12.6 h; the attestation set is unsigned and prunable | **ASSUMPTION**: the selection rule decides REV and window edges. Only "earliest" resists a presenter's choice |
| 12 | OTS + Bitcoin headers | V36–V38, R-2.19, R-3.47, R-3.48 | Depth and time are evaluable from the bundle plus a store | The proof holds neither. Authentication needs PoW, linkage, retarget rules and a checkpoint; a stale store needs every gap header | **IMPL** (O-22, made concrete): "k-header segment" (R-3.48) suffices only for a store at most one block stale |
| 13 | OTS calendars | R-4.48–R-4.51 (re-anchor; a discarded attempt's transaction "confers nothing") | The issuer anchors its own transaction | The issuer submits to calendars and polls them for the upgrade; it owns no transaction | **ASSUMPTION** (operational): calendar availability is an unregistered issuance dependency |
| 14 | OTS file stamping | R-3.42 "its canonical bytes" with a two-frame receipt (K-2, G-19) | One proof covers the receipt | Stamping two frames gives two proofs sharing one commitment | **IMPL**: still open. G-19's constructed preimage is one option; two proofs is the native one |
| 15 | RFC 8785 §3.2.2.3; RFC 7493 §2.2 | R-3.2, R-3.4, prereg §4.3 "must be exactly representable" | JCS needs numbers exactly representable; "no normalization" | JCS maps numbers to doubles and prints shortest round-trip (`9.8` is fine); it normalizes spellings itself | **ASSUMPTION**: the rule must be "value preserved" (G-56). The literal reading refuses every decimal SBOM score |
| 16 | RFC 8785 implementations (`rfc8785` package) | R-3.1 "bind to an existing deterministic standard", R-3.6 | A standard binding makes implementations agree | Same bytes on Appendix B, different input domains (2^53 limit, silent rounding) | **IMPL**: R-3.6's negative vectors must pin the domain |
| 17 | Bitcoin block header `nTime` (uint32) | 2106 examiner; §7.5 renewal | — | The last representable second is 2106-02-07T06:28:15Z | **ASSUMPTION** (horizon): re-anchoring after that date depends on a Bitcoin consensus change |
| 18 | OpenPGP key expiry and revocation reasons | R-5.21–R-5.23 (revocation effective at a time) | Channel keys and issuer keys revoke time-relatively | A "compromised" revocation voids all signatures; expiry is judged against signer-asserted creation time | **ASSUMPTION**: the git channel's and GPG slot's own key lifecycle does not follow R-5.21 |

## Consumer outcomes: stub versus de-stubbed

| Consumer | Phase 2 (stub) | Phase 3 (real) | Why |
|---|---|---|---|
| Submitter, inline SBOM | Refused, `P8_NUMBER_NOT_DOUBLE` (CVSS 9.8) | **Accepted**; the attested statement holds the SBOM | The value-preserving reading (item 1). A rule choice, not a mechanism |
| Submitter, self-check with its pre-submission release | `UNVERIFIABLE` (V38 `HEADER_NOT_IN_TRUST_STORE`) | Same under "pin every header". **`VALID_STRICT`** under "checkpoint+pow" (`EXTENDED_BY_POW_FROM_PINNED_HEADER`) | The regtest store is one block stale, so R-3.48's k-header segment links. A store months old would also need the gap headers. On regtest, PoW proves nothing |
| Relying party, phase 2's 20 runs | Non-expert: 6 unsafe accepts. Careful: 5 unsafe accepts and 5 false rejects | **Identical**, run for run | The stub was faithful for every case phase 2 built |
| Relying party, new cases m1–m3 (mirror-malleated honest receipt) | Not expressible (Ed25519) | `VALID_STRICT / ABSENT / STANDING_EVIDENCE_MISMATCH`. Non-expert correct; **careful integrator falsely rejects** | Mismatch 1 |
| C-C2 / C-C5 replays | Rejected by V17+V18 / V19; mutants accept | **Same**: rejected by V17+V18 / V19; mutants accept with `VALID_DEGRADED`; goal events fire on the mutants only | The attacker must use the frame's algorithm, because `alg` is inside the frame. The phase-1 replay's Ed25519 attacker keys were rejected for that unrelated reason (V13/V16/V19), so `keygen` was added |
| 2106 examiner, bundle as is | 5 blockers: procedure, receipt digest, anchor path, k/δ/ε, revocation | 7 blockers: the anchor path is **no longer blocked**, because a standard format can be followed (OTS and Bitcoin, still unlisted). **New blockers:** both signatures and the possession proofs, because OpenPGP and ECDSA are not in the dependency manifest | Real formats move the gap from "private format" to "undeclared standard" |
| 2106 examiner, complete spec handed over | Only revocation blocks | Only revocation blocks | Unchanged |

## For GUESSES.md bookkeeping (phase-3 guesses)

- **G-55.** For an OTS proof with several Bitcoin attestations, `anchor_time` is the earliest
  verified one, and its path's transaction is "the txid".
- **G-56.** The precision rule means value-preserving. That reading is the de-stubbed world's
  `jcs.NUMBER_RULE`.
- **G-57.** Algorithm ids name the scheme, not just the curve: `OPENPGP4-ECDSA-P256-SHA256` means "a
  v4 OpenPGP binary-document signature whose document is the frame". The verifier refuses any other
  public-key or hash algorithm in the packet. `ECDSA-P256-SHA256` means a raw DER signature with an
  SPKI key.
- **G-58.** KMS slots use RAW up to 4096 B and DIGEST above that.
- **G-59.** One OTS stamp covers G-19's two-frame preimage. The bundle carries `headers_hex` for h …
  h+k−1 from the earliest attestation.
- **G-60.** V38 has two policies (`TrustConfig.header_policy`). Retarget validation is absent: a
  segment crossing a 2016-block boundary is unperformable.
- **G-61.** The C-C2 attacker generates keys of the honest frame's algorithm.
- **G-62.** The DSKS emulation crosses algorithms: an Ed25519 `kD` "verifies" an OpenPGP signature
  over its original message. This is more generous than any real DSKS. The replay needs it only to
  reproduce the trace.

## Not done

- No DSKS or key-substitution construction (by instruction).
- No AWS calls.
- No new receipt was anchored on mainnet: the de-stubbed path is regtest-difficulty OTS, and the
  mainnet vectors test the same verification code.
- No RFC 9580 v6 packets.
- DNSSEC and git evidence are not wired into issuance (finding 2 / mismatch 4 make the DNS half
  impossible for wamason.com today).
- Bitcoin retarget rules are not validated.
