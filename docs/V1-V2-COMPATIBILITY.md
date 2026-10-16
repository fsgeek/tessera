# V1 → V2 compatibility: which V1 choices break a V2 migration, and what is cheap to fix before the freeze

> **STATUS: DRAFT, 2026-10-13. Owner instance's analysis (Claude Opus 5.5). Not registered; decides nothing.**
> Every mitigation is **RECOMMENDED** in A9's sense (drafted, not decided). The question is the author's, from
> 2026-10-13: V2 may move signers to other providers, add a third key or m-of-n, move the API to another cloud, add
> rotation, evaluate revocation, and add standing and renewal. Which V1 choices become BREAKING, and which are cheap
> to make forward-compatible before the 30 Oct freeze? He is "dubious if we don't find any". There are some.
> Revised the same day to include the author's live-session input (§0.1).
>
> Sources: `docs/phase-0-prereg-amendment-9.md` (A9), `formal/p8/ENCODING-V1.md` (ENC), `formal/p8/PROOF.md`,
> `docs/V1-PROFILE.md` (PROF), `docs/V1-OPERATIONS-RUNBOOK.md` (RB), `docs/V1-DERIVATION-DRAFT.md` (DD),
> `prototype/spike/{verify_offline,selftest}.py`, `prototype/spike/trust-config.json`,
> `prototype/tessera_proto/real/gitchannel.py`. Citations are `file:line` in the working tree on 2026-10-13. Each item
> separates **Verified** (the cited text says it) from **Inference** (my reasoning from it).

## 0. Framing

- **Direction A: old verifier, new artifact.** A V1 verifier that relying parties already hold meets a V2 receipt,
  or a V1-profile receipt issued *after* some infrastructure moved. It must fail closed, and preferably return
  `UNVERIFIABLE` rather than `INVALID`: `INVALID` tells the relying party the receipt is false.
- **Direction B: new verifier, old receipt.** It must return the same verdict as before.
- **Severity.** *BREAKING:* an honest receipt gets a non-valid verdict from a verifier a relying party reasonably
  holds, or the move is impossible without a forced verifier release. *DEGRADES:* it still works, but loses a
  stated property, or forces V2 to invent something V1 could have fixed. *FINE:* unaffected, or fails closed.

**Structural fact (Verified).** A V1 receipt is self-contained apart from the trust configuration. The bundle carries:
- the DNSSEC snapshot and its OTS proof;
- the raw git objects and the commit's OTS proof;
- the receipt's OTS proof and its headers.

Sources: PROF:65-81; A9:139 (C6). **Inference:** a move of DNS hosting, git host or API cloud cannot change an old
receipt's verdict on its own. The risk sits in three places:
- the *shape* of the trust configuration;
- the frozen V1 verifier meeting V1-profile receipts issued after a move;
- the verdict contract for later verifiers.

### 0.1 The author's input, 2026-10-13 (live session, relayed by the coordinator), quoted as his statements

- **(a)** Git 3 is scheduled to switch to the SHA-256 object format in 2027. GitHub does not support SHA-256
  repositories or signatures there; GitLab does. This is a near-term forcing event, not a hypothetical. He suspects
  that "the protocol descriptors might be under-specified". *Not verified online, by instruction.* Addressed in §2.9
  and in the audit in §3.
- **(b)** On issuer-domain pinning: "when you stand up a new domain, you've created a branch Tessera
  implementation". This is recorded as **AUTHOR'S POSITION**, not as a gap. See §2.2.
- **(c)** For the full DNS record, he suggests referring to a URI, and notes that the URI "in turn also requires a
  signature and time anchor". §4 compares this with the owner's alternative, a hash commitment.

## 1. Summary

| # | Seam | Dir. | Severity | Cheapest pre-freeze fix (RECOMMENDED) |
|---|---|---|---|---|
| 1 | The repository key is a singleton in the trust config, with no period | B, A | **BREAKING** | Entries of the form `{D, repo key, signing period}`, with an existential rule like the root-KSK rule |
| 2 | Issuer domain D | A, B | **FINE by design** (author's position), plus one verdict-class gap | A foreign D gives `UNVERIFIABLE`, not `INVALID` |
| 3 | The frozen V1 verifier rejects both registered rotation mechanisms | A | **BREAKING** | Register *sequential replacement*, or end V1 with its first window |
| 4 | A later verifier may change a V1 verdict under "a different policy" | B | **BREAKING** (permitted as written) | A profile-semantics sentence; later results are reported separately |
| 5 | Trust-config lists (KSKs, pins) are not stated append-only | B | **BREAKING** if pruned | Append-only; closed periods immutable; give the pin-set key a period |
| 6 | Two slots, `kms`/`gpg` names, a shared `common.alg` | A | FINE (fails closed) / DEGRADES | Slot names denote fingerprint schemes, not providers |
| 7 | DNS record: one RR, one string, exactly 255 bytes, no hash identifier | A | FINE for old receipts / DEGRADES | Nothing but a V1 record at `_tessera-v1.<D>`; V2 uses the §4 commitment |
| 8 | Version identifiers in signed bytes | A | FINE; gaps outside the signed bytes | Version the container and the trust-config format |
| 9 | Git: SHA-1 assumed and nowhere named as a format | A | **BREAKING** for V1 issuance after a format switch; FINE for old receipts | Name `object_format: sha1` in the evidence and the profile; pin a SHA-1 repository at a host that keeps SHA-1 |
| 10 | Renewal or standing embedding V1 receipts | — | DEGRADES | A canonical container; a named V1 statement identifier |
| 11 | API to another cloud; slot 2 to an HSM | — | FINE / DEGRADES | Keep the declared-time check in a signer process |
| 12 | PROOF assumption (K) forbids V1 keys signing V2 strings | — | DEGRADES | Restate (K) over every prefix-free Tessera tag, or use fresh keys |

## 2. Items

### 2.1 Repository root key: one key, no validity period — BREAKING (B, and A)

**Verified.**
- The trust config pins "the pair (D, repository root key)" (PROF:190, :273-276). `gpgsig` is verified "under the
  pinned repository key" (PROF:256).
- Root KSKs, by contrast, have signing periods and an existential rule (A9:285-289; PROF:194-199).
- The runbook says that losing YubiKey 2 with no backup "needs a new verifier release … Existing receipts are
  unaffected" (RB:21-23).
- The runbook's path past V1 certifies slot 2 "by the offline root" (RB:32-35).

**Inference.** "Unaffected" holds only if the new release *keeps* the old key, and the pair shape cannot express
that. If the new release replaces the key, every old receipt's git channel fails. If it keeps both keys with no
period, a compromised retired key can sign assertions that are accepted for receipts anchored after the compromise.
This is the KSK problem again, and A9.5 already solved it for KSKs. No source gives the verdict class for a
repo-key mismatch.

**RECOMMENDED.** Use entries `{D, repo key, signing_valid_from, signing_valid_until}`:
- The assertion is authentic if *some* entry whose period contains the commit's anchored time verifies `gpgsig`.
- An unconfigured key gives `UNVERIFIABLE / REPO_KEY_NOT_CONFIGURED`.
- A configured key outside its period gives `INVALID`.

This mirrors the spike's `root_ksks` code (verify_offline.py:99-118).

### 2.2 Issuer domain D — FINE by design (AUTHOR'S POSITION), with one verdict-class gap

**Verified.**
- D = `wamason.com` "as a demonstration" (A9:63-64). A9.3 lists "a non-personal D" as a precondition for attributed
  receipts (A9:228).
- D is signed (`common.issuer`, ENC:261). The DNS owner name is rebuilt from it (ENC:551-553). The git channel is
  "accepted only for the pinned D" (PROF:273-276).
- The verdict on a mismatch is not stated. The spike makes it a FAIL, so `INVALID` (verify_offline.py:59-60;
  selftest.py:25-27).
- The spike's DNSSEC walk hard-codes `com.` and `wamason.com.` (verify_offline.py:129). That is instrument code; the
  snapshot body format is still OPEN (PROF:341-342).

**Author's position (b).** A new domain is a branch Tessera implementation. Its trust configuration and verifier are
its own, and the `wamason.com` verifier keeps verifying `wamason.com` receipts. Direction B therefore does not arise:
no release replaces wamason.com's D. My earlier draft recommended a *set* of D entries; that is withdrawn as
contrary to this position.

**What remains (Inference).** In direction A, a `wamason.com` verifier handed a receipt from a branch says `INVALID`,
which reads as "forged". The author's own framing says it is "another implementation's receipt". **RECOMMENDED:** a
`common.issuer` that is not the pinned D gives `UNVERIFIABLE / ISSUER_NOT_CONFIGURED`. Under this position, §2.1's
entries are all for the one D, so they become `{repo key, period}`. The snapshot format must also walk an
arbitrary-depth chain, so that a branch with a deeper D can reuse the verifier code.

### 2.3 Rotation within V1 — BREAKING (A)

**Verified.** V1 has one window of at most 90 days: "Before the window ends, either a rotation mechanism is registered
(multiple records or per-key owner names) or issuance stops" (A9:342-345; RB:58-60). The frozen verifier rejects both
named mechanisms:
- multiple records: "exactly **one** TXT record … `DNS_RRSET`" (ENC:557);
- per-key owner names: the owner name is rebuilt from `issuer` alone, so any other name gives `DNS_OWNER`
  (ENC:551-553).

The git path is fixed, and a rotation mechanism "must define its own paths" (PROF:267-269).

**Inference.** Rotation under either named mechanism forces a verifier re-release. Every verifier already
distributed, including those of the 4 Dec tester and the dead-service test, rejects post-rotation receipts.

*Sequential replacement* already works with the frozen verifier:
- the successor record goes at the same owner name, and the successor blob at the same path;
- it has a new key and a new window, with not-before ≥ the old not-after;
- each receipt carries its own snapshot and commit, and no rule requires the record to be current.

The windows still bound minting (A9.6 guarantee 2). A1's "any rotation issues a new key" holds (A9:435-436). The
cost is an issuance gap at each boundary.

I have not checked this against P10 or the capstone model.

**RECOMMENDED.** Do one of these:
- register sequential replacement as V1's rotation mechanism, with two-window vectors; or
- state that V1 ends with its first window.

### 2.4 Verdict stability under revocation, standing and algorithm policy — BREAKING as permitted (B)

**Verified.**
- A9.4's contract holds "under the same governing V1 specification, policy, trust configuration …", and says that
  "Given a different trust configuration or policy (newer header pins, a prohibited algorithm), the result may
  change. Later adverse evidence feeds a separate, stronger assessment" (A9:261-266).
- The stable fields include `revocation` and standing (A9:156).
- Cases e and e′ are `VALID_STRICT` (A9:177).
- Slot `gpg` is P-256 in both signer branches (A9:298-301, :319-320), and strict needs both slots (A9:136-137).
- A search for a "V1 receipts are evaluated under V1 profile semantics" rule found none.

**Inference.** A V2 verifier that evaluates revocation can return `INVALID` on e′ and call that "a policy change". A
blanket P-256 prohibition flips every V1 receipt in both branches. That includes hybrid receipts anchored before any
break, which undoes A9.6 guarantee 1 (A9:360-367) by policy rather than by attack.

**RECOMMENDED** (one sentence):
> A bundle whose signed `common.profile` is `tessera-v1-strict` is evaluated under the spec named by its signed
> `common.spec`. The six stable fields are V1's. Later revocation, standing, renewal and historical-security results
> are a separate assessment and never overwrite them. Algorithm policy enters only as an authenticated safe-before
> cutoff per algorithm and per key, compared with T (A9:255-257).

### 2.5 Trust-config lists are not stated append-only — BREAKING if pruned (B)

**Verified.**
- The trust config holds two KSKs with periods and "a signed, versioned set" of header pins (A9:148-151).
- The pin-set key, its format and its versioning are OPEN (PROF:218-219).
- An uncovered header gives `UNVERIFIABLE / HEADERS_NOT_COVERED`, and an unconfigured KSK gives
  `NO_TRUSTED_KSK_USABLE` (PROF:209-217).
- KSK-2017 leaves the root on 2027-03-22 (PROF:202-203).

**Inference.** Two natural later edits each turn every old receipt `UNVERIFIABLE`: pruning pins, and dropping
KSK-2017 after it leaves the root. Keeping KSK-2017 is safe, because its signing period closed on 2026-10-11.

**RECOMMENDED.**
- Entries are append-only.
- A closed period is never reopened or extended.
- Pins are never removed.
- The pin-set key gets a signing period in §2.1's form.

### 2.6 Slot names, two-slot shape, shared `common.alg` — FINE for V1 verifiers; DEGRADES V2 design

**Verified.** The two-slot shape is fixed in five places:
- the `A_sig` count byte is 2 (ENC:383), and that byte is "not the place to carry the version" (ENC:425);
- `sset` holds exactly one `gpg-sha256:` (ENC:366);
- a frame's slot follows from its fingerprint prefix (ENC:318-320; PROOF:231-247);
- signature rules are keyed by `(common.alg, slot)` (ENC:436-442);
- one `common.alg` names the pair (ENC:486-488).

`gpg-sha256` is defined over a v4 **P-256** key packet (ENC:290). V2 tags give `TAG_UNKNOWN` (ENC:215-218). Unknown
labels give `OUT_OF_PROFILE` (ENC:742-743).

**Inference.**
- *A third slot or m-of-n:* a new profile. V1 fails closed.
- *Slot 2 on a cloud HSM with P-256:* fits V1's bytes if Tessera builds the OpenPGP packet, as it does for `kms`
  (ENC:474). It is still a key change, so §2.3 applies.
- *Slot 2 with raw or non-P-256 signatures:* impossible in V1; it needs a new profile.
- *Pair ids:* they grow combinatorially with n slots. That is V2's cost.

**RECOMMENDED.** Make no format change. Add one sentence: slot names denote fingerprint schemes, not providers.

### 2.7 The DNS record — FINE for old receipts; DEGRADES V1 evolvability

**Verified.**
- One RR, one string, a fixed field order, exactly 255 bytes; "A later field needs a new record version"
  (ENC:557-564).
- Extra fields give `DNS_FIELD_UNKNOWN`, and a wrong `v=` gives `DNS_VERSION` (ENC:603-604).
- "The `-v1` suffix lets a later profile publish next to it" (ENC:555).
- The `DNS_*` verdict class is OPEN (PROF:135-137).

**Inference.** A V2 record at `_tessera-v1.<D>` fails closed, and it also breaks V1 issuance while it is there. A V2
record at `_tessera-v2.<D>` is never read by V1. **RECOMMENDED:**
- nothing but a V1 record is ever published at `_tessera-v1.<D>`;
- settle the `DNS_*` class (my lean: `DNS_VERSION` gives `UNVERIFIABLE`, every other code gives `INVALID`);
- V2 uses §4's commitment.

### 2.8 Version identifiers — FINE; gaps outside the signed bytes

**Verified.** Version identifiers sit in every signed structure:
- every signed or stamped string starts with a `tessera-v1/` tag;
- frames carry `canonicalization_version`;
- `common` carries `profile` and `spec.id`/`spec.sha256`;
- the manifest carries `ver: map-v1`;
- the DNS record carries `v=tessera1` (ENC:724-733).

Future and withdrawn tags give `TAG_UNKNOWN` (ENC:215-217, :409-414).

**Inference.** Lemma 4's prefix-free headers rule out misparsing. The gaps:
- the bundle container is unversioned and OPEN (PROF:87-88);
- the trust-config format has no version in any source (only the spike's `"spike-1"`, trust-config.json:3).

**RECOMMENDED:** give both a version field; an unknown version gives `UNVERIFIABLE`.

### 2.9 Git channel: SHA-1, object format, host — BREAKING for V1-profile issuance after a format switch (A); FINE for old receipts (B)

**Verified.**
- This repository is `sha1` (`git rev-parse --show-object-format`, 2026-10-13).
- SHA-1 appears in the V1 texts only as a residual and as a dependency-manifest entry (A9:46, :154, :284; ENC:712-718;
  PROF:260, :368). **No V1 text names the git object format as a parameter, a bundle field or a check.**
- The git evidence member (PROF:75) has no format field.
- The stamped bytes are "the commit's lowercase hex id and LF", defined by repository convention (ENC:704-705), not
  by profile rule.
- The instrument hard-codes 40-hex ids and 20-byte tree entries (gitchannel.py:43, :163-166, :202).
- Publication is an issuer duty the verifier does not check (A9:421-426).

**Inference, given the author's statement (a).** If the key-assertion repository is created or converted under a
SHA-256 default during V1's life, the frozen verifier cannot verify any receipt that relies on it. It fails closed on
lengths or ids, by accident rather than by a named check: there is no `GIT_OBJECT_FORMAT` code.

Conversion also rewrites every commit id. Old receipts still verify from their own bytes, but the published copy no
longer contains the commits they name. That weakens the publication duty (DEGRADES).

The GitHub/GitLab split (author's statement) cuts both ways:
- a SHA-1 repository needs a host that keeps SHA-1;
- a V2 move to SHA-256 needs a host that supports it, plus a verifier that parses 64-hex ids and, I believe, git's
  separate SHA-256 signature header (not checked).

**RECOMMENDED.**
- Add `object_format: "sha1"` to the git evidence member. Any other value gives
  `UNVERIFIABLE / GIT_OBJECT_FORMAT`.
- Name SHA-1 in the profile as V1's git format.
- Pin V1's key-assertion repository to SHA-1 for V1's life, with an explicit `--object-format=sha1`.
- Make "40 lowercase hex + LF" a profile rule.
- Keep old commits published in a frozen mirror after any conversion or host move.

### 2.10 Renewal and standing embedding V1 receipts — DEGRADES

**Verified.**
- An honest renewal wrapper is `OUT_OF_PROFILE`, a registered false reject (A9:179).
- Custody needs the exact bytes (A9:290-292).
- The container is OPEN (PROF:87-88).
- `SHA256(A_sig)` is "an existence commitment, not an identifier", and no identifier may come from signature bytes
  (ENC:735-739).

**Inference.** Without a canonical container, two copies of one receipt hash differently, so renewal chains diverge.
Standing needs a statement identifier that is stable under signature malleability.

**RECOMMENDED.**
- Make the container deterministic when it is decided.
- Name the wrapper's exact-copy digest.
- Name the V1 statement identifier, e.g. `manifest_sha256` with `SHA256(JCS(common))`.

### 2.11 API and signer moves — FINE / DEGRADES

**Verified.**
- The API is AWS (A9:158), but no signed byte names a provider. The `kms` fingerprint is an SPKI hash (ENC:289).
- RB:42-43 plans a third-provider API.
- The declared-time check lives in the `gpg` signer (A9:335-338).

**Inference.** Moving the API is FINE. Moving a key is a key change (§2.3). A bare HSM loses the declared-time check.

**RECOMMENDED:** the check belongs to the slot-2 signer process, whatever holds the key.

### 2.12 PROOF assumption (K) — DEGRADES

**Verified.** "(K) Each V1 slot key signs only V1 tagged strings" (PROOF:109-110).

**Inference.** Reusing a V1 key for `tessera-v2/` strings falsifies (K) as written, even though the headers stay
prefix-free.

**RECOMMENDED:** restate (K) over every registered, prefix-free Tessera tag set, or commit V2 to fresh keys.

## 3. Descriptor audit, for the author's point (a)

For every hash and signature in a V1 receipt: does the encoding carry an algorithm or format identifier that a later
decoder can dispatch on? *Yes* means the identifier is in the bytes. *Via version* means only a tag or version string
implies the algorithm, so a change needs a new version.

| Hash or signature | Identifier in the bytes? | Evidence |
|---|---|---|
| Attestation and manifest frame canonicalization | **Yes**, u16 `canonicalization_version` | ENC:237 |
| `key_fp` in frames and manifest | **Yes**, `spki-sha256:` / `gpg-sha256:` | ENC:289-293 |
| `kms=` / `gpg=` fingerprints in DNS and the git blob | **No**: bare hex; hash implied by slot name + `v=tessera1` | ENC:294-295, :569-576 |
| `manifest_sha256`, `preamble_sha256`, `vectors_sha256`, `spec.sha256` | **Via version**: SHA-256 is in the member *name* of a closed schema | ENC:262-267 |
| Slot signatures, rule O | **Yes**, the OpenPGP packet carries pubalg 0x13 and hashalg 0x08; also `common.alg` | ENC:456, :440 |
| Slot signatures, rule R (hybrid `kms`) | **Partly**: only the *pair* id `common.alg`; raw bytes carry nothing | ENC:480-488 |
| Possession signatures over the manifest | **Yes**, rule O as above | ENC:368-369 |
| Receipt anchor digest `SHA256(A_sig)` | **Via version**: tag `tessera-v1/receipt-anchor-sig`; the OTS proof's own ops name SHA-256 | ENC:375-378 |
| DNSSEC snapshot digest | **Via version**: tag `tessera-v1/dnssec-snapshot`; body format OPEN | ENC:537-540; PROF:341 |
| DNSSEC RRSIG/DS within the chain | **Yes**: DNSSEC algorithm and digest-type numbers | verify_offline.py:143 |
| Git commit, tree and blob ids | **No**: the object format is named nowhere; SHA-1 is implied | §2.9 |
| Git commit-id stamp (`hex id + LF`) | **No**: repository convention; only the length (40 vs 64) discriminates | ENC:704-705 |
| Git `gpgsig` | **Yes**: an armored OpenPGP packet carries its algorithms | ENC:711 |
| Header pins (Bitcoin double-SHA-256) | **Via version**: the pin-set format is OPEN | PROF:218-219 |
| Trust-config KSK digests | **Via field name**: `ds_digest_sha256`; config unversioned | trust-config.json:5 |

**Finding.** The author's suspicion holds in three places:
- the **git descriptors** (no object format anywhere, and the stamp form is by convention only);
- the **DNS and git key-publication value** (bare hex with no hash identifier);
- **rule R** (the algorithm only through a pair id).

Everything inside the signed frames and anchors dispatches, either directly or by version. Versioning by tag is
adequate *for formats Tessera controls*, because changing the algorithm then means minting a new version. It is not
adequate for git, whose format changes outside Tessera's control (§2.9). The cheap fixes are §2.9's `object_format`
field, and §4 for the DNS value in V2.

## 4. The full DNS record: a URI versus a versioned hash commitment (author's point (c))

**The two options.**
- **URI (the author's suggestion).** The TXT record names where the key-publication document lives. As he notes, the
  document then needs its own signature and time anchor. The record authenticates a *location*, not content, so a
  verifier needs either a fetch, which fails under link rot and offline, or a bundled copy plus some binding of that
  copy to the URI. In practice that binding is a signature by a configured key (the repository root) and an OTS stamp
  on it, which is the git channel again. Content at a URI is mutable, so a 2106 verifier cannot tell which version a
  receipt relied on unless the content is pinned by hash. A URI plus a hash is the commitment option with a locator
  added.
- **Hash commitment (the owner's alternative).** The record would be, for example,
  `v=tessera2;profile=…;kp=sha-256:<64 hex>`. `kp` commits to a canonical (JCS, ENC §1) key-publication document that
  travels in the bundle. The DNSSEC-signed snapshot is the signature, and its OTS stamp is the time anchor, both
  already present in V1. There is no fetch, so the document survives link rot. The document can hold any number of
  keys, per-key windows, m-of-n, successor and rotation data, without the 255-byte ceiling. `sha-256:` is a dispatch
  identifier, which fixes §3's bare-hex row. The record stays far under 255 bytes. The git blob can *be* the same
  document, so both channels assert identical bytes, as they do today.
- **Costs of the commitment.** DNS alone no longer shows the keys to a casual reader; the document must be published,
  and the git channel already publishes it. Hash agility depends on the identifier being checked. Historical
  security of the zone's DNSSEC algorithms is unchanged.

**Owner's view (Inference, RECOMMENDED).** The commitment dominates the URI on the criterion that matters, which is
offline, long-horizon verification with no live party (C6). The URI's own requirement, a signature and a time anchor,
is met for free by DNSSEC plus the snapshot stamp only when the record commits to content.

**What V1 must change now to allow it in V2.** **Nothing in the bytes**, because V2 publishes at `_tessera-v2.<D>`
(ENC:555) and V1 receipts carry frozen snapshots. The pre-freeze items are the §2.7 rule (nothing but a V1 record at
`_tessera-v1.<D>`) and the §2.8 container version, so that a V2 bundle can carry the document as a new member.

**Adopting it for V1 itself** would mean:
- rewriting ENC §7's grammar and its 15-step rejection order;
- PROOF Lemma 11 (PROOF:337);
- the DNS, XD and W vectors, so the 71/173 counts change;
- the instrument's parser (gitchannel.py:145-148);
- a new bundle member.

That reopens P8 before 30 Oct. I do not recommend it for V1 unless rotation (§2.3) is wanted inside V1, in which
case it is the cleanest mechanism.

## 5. Cheapest pre-freeze set, by value (all RECOMMENDED)

1. Repo key as `{key, signing period}` entries; an unconfigured key, or a foreign D, gives `UNVERIFIABLE`
   (§2.1, §2.2).
2. The profile-semantics sentence (§2.4).
3. Sequential replacement as V1 rotation, or end V1 with its first window (§2.3).
4. `object_format: sha1` in the git evidence; pin a SHA-1 repository; the stamp form as a profile rule (§2.9).
5. An append-only trust config; a period for the pin-set key (§2.5).
6. A versioned, canonical container; a versioned trust-config format; a named statement identifier (§2.8, §2.10).
7. One-line clarifications: §2.6, §2.7, §2.11, §2.12.

Items 1, 2, 4 and 5 change no signed byte and no P8 vector. Item 3 needs two-window vectors. None of them reopens P8.
