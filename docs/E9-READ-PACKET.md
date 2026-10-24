# E9 read packet: the 30 Oct V1 exit

> **For the author.** Owner draft, 2026-10-21 (Claude Opus 5.5), revised after Codex review E9-01 to E9-14
> ([disposition](reviews/e9-packet/DISPOSITION.md)). A9.2: "The author's E9 read is accept or reject per row"
> ([A9:222](phase-0-prereg-amendment-9.md#L222)). One ruling (row 2), accept or reject on the rest, 30–45 minutes.
> One outside read is required (row 22, 8 minutes). Links are for checking only.

## What the V1 exit establishes

**The claim.** A user holds a V1 receipt, an authenticated verifier release and its trust file. Without Tessera,
the user can check four things:

1. The receipt binds exact content bytes.
2. The verifier checks signatures by both keys named in the receipt, over frames that bind those bytes.
3. DNSSEC evidence and a signed git commit name those keys for `wamason.com`.
4. The bytes and both signatures existed before a specific Bitcoin block.

This establishes signatures by Tessera's actual service keys only if the authority records named those actual keys.
Capture of both authority records can defeat that assurance (row 2). Every item depends on the registered
assumptions about cryptography, key use, Bitcoin history and the verifier release.

**The attacker.** The attacker controls the network. Changing the content, or the frames and signatures committed
by the receipt anchor (`A_sig`), prevents acceptance unless the registered security assumptions fail. Some changes
outside that commitment remain valid: for example, another conforming possession signature over the same manifest.
Its own keys get no VALID verdict unless it captures the authority records. If it captures **both** the DNS record
and the git repository, its new receipts under its own keys **pass under CUT** (row 2); **under KEEP**, an authentic
verifier release refuses them, because its listing does not name those keys. Either way, receipts that the honest
service signed stay protected while the service keys stay secret and unmisused. Capture of the issuing AWS account
lets the attacker make receipts that pass.

**The boundaries.** V1 does not check who sent the bytes, what they mean, revocation, or past key or algorithm
safety. It gives no lower time bound. T is a Bitcoin header time, not real time; a real-time bound U holds only under
A-UTC, which the verifier does not check. V1 detects no capture and checks no publication. The same content can have
more than one valid receipt.

**What the exit is.** The packet reports the completed checks and names remaining work. Your ACCEPT answers
complete the author's E9 judgments. The owner must then close the remaining freeze prerequisites, including the
provisional release-checker choice, and reconcile the final objects and record. The signed opening commit follows
those checks. It permits V1-profile code only and discharges nothing in the original Band 0 gate.

## How the rows were filtered

A9.2's closure rule sends you a finding only if it is a concrete counterexample to C1–C7, or shows that a C-row lacks
its assigned evidence. The owner sorted all 93 findings since 19 Oct
([P8](reviews/p8-falsification/DISPOSITION.md), [E18](reviews/e18-signoff/DISPOSITION.md),
[E6a](reviews/e6a/DISPOSITION.md), [exit pages](reviews/exit-pages/DISPOSITION.md),
[profile](reviews/profile-2026-10-19/DISPOSITION.md), [preamble](reviews/preamble/DISPOSITION.md),
[Levadura](reviews/levadura-contradictions/DISPOSITION.md), [contract](reviews/v1-contract/DISPOSITION.md),
[real runs](../prototype/e2e/FINDINGS.md)). **None gates by that sort.** Four close calls are in their rows so you
can disagree: rows 3, 12, 15 and 21.

## Part A. The purpose preamble (row 1)

**Row 1. Do you accept this text as the purpose preamble that every V1 receipt binds?**
OWNER TEXT, revised after Codex review ([PA-01 to PA-08](reviews/preamble/DISPOSITION.md)). The bytes of
[`PREAMBLE.txt`](../formal/freeze-v1/PREAMBLE.txt) (1,205 bytes, SHA-256 `1eebd4a8…468f`):

```text
Tessera V1 receipt (tessera-v1-strict).

Check without Tessera using an authenticated verifier release and its trust file.
VALID_STRICT means all required checks passed.
Claims depend on registered assumptions about cryptography, key use and Bitcoin history.
Two keys signed bytes that bind the content.
A DNS record, authenticated by DNSSEC signatures, and a signed git commit named these keys for wamason.com.

One controller holds both keys.
Control of the issuing AWS account lets an attacker use both.
An attacker controlling both authority records can issue passing receipts without the original service.
V1 guarantees no detection or public exposure of capture.

The content and signatures existed before the selected Bitcoin block was mined.
Its header time T is not a UTC upper bound.
The separate UTC bound assumes unchecked A-UTC and never changes the verdict.

V1 checks no sender identity, content meaning or truth, signatures inside content, revocation, or past key or algorithm safety.
The same content can have more than one valid receipt.
It gives no lower time bound or priority.
It does not show that a replay suits your transaction.

See the specification, vectors and standards list.
```

**This text assumes CUT.** Under KEEP, the owner rewrites the "attacker controlling both authority records" line
and brings back R1. If only the preamble wording changes, only its object hash and the catalog change.

## Part B. Rulings and owner decisions on text you signed (rows 2–6)

**Row 2. The service-key listing: KEEP or CUT? AUTHOR RULING REQUIRED.**
**The listing cut is not authorized by the registered text.** You adopted option (e), with the listing (A10.4.1), on
18 Oct. The owner cut it on 19 Oct under A10 row 33, which amends A9.2's cut order. That order applies only "if the
30 Oct exit slips", and it had not slipped. Your adoption therefore governs until you rule
([owner correction](decisions/2026-10-19-listing-cut.md#L8-L14)). The freeze is assembled without the listing for now.

- **KEEP.** The owner builds A10.4.1 in the profile and the verifier, with conformance cases, and reassembles the
  freeze. The exit then lands about 29–30 Oct with no spare time. That date is a prediction.
- **CUT.** Your own narrowing of what you adopted. V1 states that receipts under a captor's own keys pass when both
  authority channels are captured. Honest receipts stay protected; release-key custody (A10.4.2) is unchanged.

**Owner recommendation: CUT, on the merits.** The protection is narrow: it holds only for users with an authentic
verifier release, and it moves trust from two credentials (DNS, repository key) to a third (the release key) that
the same custodian holds. It needs an evidence package that users must keep outside the receipt. **A CUT is
permanent for issued receipts:** a later listing protects only later receipts. Dependent on this ruling: the
opening, rows 1, 16, 19, 22, the [contract's capture row](V1-CONTRACT.md#L72) and the freeze objects.
*Optional read:* [decision file](decisions/2026-10-19-listing-cut.md), 52 lines, 4 minutes.

**Row 3. Do you accept the reading that C3's "fails" means "does not reach `VALID_STRICT`"?**
OWNER CLARIFY ([profile note 13](V1-PROFILE.md#L1331-L1340), from E6a). A missing possession signature or `a_sig`
gives CANNOT VERIFY (`UNVERIFIABLE / MEMBER_MISSING`), not INVALID. Both refuse the receipt. C3 then claims nothing
about which refusal is given.

**Row 4. Do you accept the two owner readings of A10's UTC text?**
OWNER CLARIFY ([profile notes 14–15](V1-PROFILE.md#L1341-L1348)). A10's "null exactly when T is null" applies to
the bound `utc_upper_bound`, not to the `utc_assessment` field on every report. Δ = 7200 s and m = 6 enter the frozen
catalog once, at the freeze, changing every TEST release hash before any production release (E-05).

**Row 5a. Do you accept that the frozen release format binds the envelope, not the verifier code?**
OWNER DECISION ([item 1](V1-FREEZE-OPEN.md#L316-L324); rules in [profile §15.9](V1-PROFILE.md#L1884)). The freeze
fixes the archive, release manifest, signature and TEST/production key rules; each release binds its code by hash.
It also fixes the custody procedure's required contents
([A10.4.2](phase-0-prereg-amendment-10.md#L628-L640)). Each release needs independent review against an approved
baseline outside the operational environment. Approval must name the exact archive hash. The procedure must cover
authorization, signing, backups and file transfer. Building and rehearsing that environment remains due before the
first public verifier release.

**Row 5b. Do you accept the owner's reading of "imports"?**
OWNER DECISION, same item. A9.2: service code "never imports" instrument code. "Imports" means a runtime or build
dependency. So the service verifier can be ported from `prototype/indep-verifier/`, and must then earn its own
evidence: E10 vectors and the P9 code inspection on its own bytes.

**Row 6. Do you accept the rule for the production release-key fingerprint channel?**
OWNER DECISION ([item 2](V1-FREEZE-OPEN.md#L325-L329)). The freeze fixes only the rule: at least two publication
channels outside the operational environment (the NUC, this repository, DNS, AWS). You name them before the first
public verifier release. Owner recommendation: Zenodo under your ORCID, and one printed copy.

## Part C. The twenty exit items (rows 7–26)

Claims in rows 7–14 and 17–20 come from each model's reading aid or results file, never stronger. Earlier reads
(C5 covered degraded Q2 headers) are context only.

**Row 7. P1 integrity, `checked`.**
*Claim:* With both authority channels required and one fully in the attacker's hands, the modelled strict verifier
accepts a package only under an honest service key. It then accepts only bytes that key signed.
*Attacker and limits:* It controls all traffic, holds one channel key and every key it uses, and can make a key that
verifies a seen signature. One of two channels leaked; terms stand for bytes (P8); accept or not only (P4); no time.
*Evidence:* [S-P1 aid, Q1d and Q1r](../formal/suite/s-p1/READING-AIDS.md#L329-L378).
*Question:* Does this statement describe what the evidence establishes, without claiming more?

**Row 8. P2 signature-set completeness, `checked`.**
*Claim:* In the same setting, the modelled verifier never accepts a package for an honest two-signer manifest that
carries only one of its signatures. It never accepts a signature by another key in a slot that the signed manifest
assigns to an honest signer.
*Attacker and limits:* As row 7. Sets of at most two; set encoding is P8's; which refusal is P4's. No E7 mapping
sentence (row 21).
*Evidence:* [S-P2 aid](../formal/suite/s-p2/READING-AIDS.md#L231-L278), [strict](../formal/suite/s-p2/READING-AIDS.md#L347-L426).
*Question:* Does this statement describe what the evidence establishes, without claiming more?

**Row 9. P3 key binding, [model] half, `checked`.**
*Claim:* With DNS fully the attacker's, the modelled verifier never accepts an honest service's signed bytes as
signed by another key. It never accepts an honest manifest self-signature as proof that another key owns it.
*Attacker and limits:* As row 7, without the repository or service keys. Perfect fingerprint and hash; nothing about
the signature library or encodings (the [assumption] half, after the exit). No E7 mapping sentence.
*Evidence:* [S-P3 aid](../formal/suite/s-p3/READING-AIDS.md#L195-L232).
*Question:* Does this statement describe what the evidence establishes, without claiming more?

**Row 10. P4 fail-closed verdict logic, `checked`.**
*Claim:* For five abstract checks, the modelled classifier returns INVALID exactly when a required check fails;
otherwise CANNOT VERIFY when a required check cannot be performed; otherwise VALID. TLC checked all 1,944
combinations: exhaustive for that finite instance only.
*Attacker and limits:* It chooses any outcome per check; no bytes, keys or actions. What each check is, and whether a
real verifier reports outcomes faithfully, is not modelled. The link to ProVerif acceptance (L-05) is prose.
*Evidence:* [P4 aid](../formal/tla/READING-AID-P4.md#L365-L393).
*Question:* Does this statement describe what the evidence establishes, without claiming more?

**Row 11. P5 temporal soundness, `checked`.**
*Claim:* Assuming the signatures existed no later than the anchor, the modelled time predicate accepts only receipts
inside the verifier's own three-part window. Tolerances that a receipt states never change the verdict.
*Attacker and limits:* A forger chooses the declared time, signing time and tolerances; no bytes or keys. Existence
before the block is assumed, not shown; signatures are assumed to pass. Finite instance. V1 does not use the
revocation half (P6).
*Evidence:* [P5P6 aid](../formal/tla/READING-AID-P5P6.md#L396-L428).
*Question:* Does this statement describe what the evidence establishes, without claiming more?

**Row 12. P5c issuance, `checked`, with the E-02 gap.**
*Claim:* In the bounded single-clock issuance model, a shipped attempt has an anchor inside its window, buried deep
enough that the permitted reorganizations cannot orphan it. An expired attempt cannot ship; final expiry without
shipping enters a refusal that stays.
*Attacker and limits:* The chain can delay inclusion and make two shallow reorganizations; no termination, delivery
or header authentication. Real run E-02 made a never-shipped signature; P5c has no state for it (gap open). OWNER
CLARIFY: a second receipt over the same honest frames breaks no guarantee ([contract](V1-CONTRACT.md#L58-L62)).
*Evidence:* [P5c aid](../formal/tla/READING-AID-P5c.md#L409-L436); [E-02](../prototype/e2e/FINDINGS.md#L19-L44).
*Question:* Does this statement describe what the evidence establishes, without claiming more?

**Row 13. P10 manifest authority, `checked`.**
*Claim:* In the abstract first-link model, with either channel key leaked, every acceptance follows publication of
the same key statement by at least one authority, the honest service's possession record for that key, and its
signature over the same bytes. S-P3 Q1 (row 9) repeats this with the structured frame.
*Attacker and limits:* As row 7, without the key-making ability. Channels are abstract: concrete DNSSEC and git
verification are not modelled. Possession signs a tag and fingerprint, not the actual manifest bytes.
*Evidence:* [Q3 aid](../formal/spike/first-link/READING-AID-Q3.md#L153-L187); [Q1](../formal/spike/first-link/RESULTS.md#L20-L31).
*Question:* Does this statement describe what the evidence establishes, without claiming more?

**Row 14. P7, type-separation half, `checked`.**
*Claim:* In the same setting as row 7, an object signed as one type is never accepted as another type. The type tag
is inside the signed bytes.
*Attacker and limits:* As row 7. Only acceptance as an attestation or a wrapper is tested; other types are distinct
only in P8's vectors. No E7 mapping sentence.
*Evidence:* [S-P7 aid](../formal/suite/s-p7/READING-AIDS.md#L230-L292), [strict](../formal/suite/s-p7/READING-AIDS.md#L329-L372).
*Question:* Does this statement describe what the evidence establishes, without claiming more?

**Row 15. P8 prose proof, vectors and falsification. Do you accept that bounded claim?**
The 20-minute review found a counterexample to the old signature-binding sentence: one signature verified over two
different frames under a constructed key. It found no complete passing receipt and no encoding collision. The
repaired P8 claim covers unambiguous encoding and anchor binding. Signature security remains with P1/P3 and their
assumptions. No vector changed. P8 has no adversary statement yet.
*Evidence:* [report](../prototype/p8-falsify/REPORT.md#L63-L95), [disposition](reviews/p8-falsification/DISPOSITION.md#L16).

**Row 16. P9 as a contract inspection. Do you accept it?** At verification time, nothing that Tessera runs can change
the verdict. Tessera writes the receipt and makes the release; C6 permits both. P9 stays `open` until the two-machine
vector runs. Under KEEP, its line on the listing is redone.
*Evidence:* [inspection](../formal/P9-CONTRACT-INSPECTION.md#L20-L40).

**Row 17. E6a with companions.**
*Claim:* E6a extends P4's abstract classification with algorithm and evidence cases. A well-formed, correctly bound
unsupported algorithm gives CANNOT VERIFY only when no independent required check fails. A definite required failure
gives INVALID.
*Attacker and limits:* These are bounded classification results for two slots and two evidence members. E6a adds
separate models; P4 was not edited.
*Evidence:* [results](../formal/tla/E6a/RESULTS.md#L10-L48); [review](reviews/e6a/DISPOSITION.md).
*Question:* Does this statement describe what the evidence establishes, without claiming more?

**Row 18. The 129 strict correct-form rows.**
*Claim:* Every strict correct-form query of the composed ProVerif model came out as registered. Interim statement:
one-acceptance linkage is tested against attackers holding one or both authority credentials; capture of both loses
unrestricted service-origin assurance.
*Attacker and limits:* No result establishes time, concrete encoding or implementation conformance. The capstone
stays open (two questions deferred 2026-10-07).
*Evidence:* [capstone](../formal/suite/capstone/RESULTS.md#L1758-L1785); [sheet](../formal/E8-E7-E11-SHEET.md#L88).
*Question:* Does this statement describe what the evidence establishes, without claiming more?

**Row 19. Statements M2 and M5.**
*Claim:* M2 fixes the service domain checked on both authority records. M5 fixes each manifest field through
authenticated authority evidence or a fixed profile constant.
*Attacker and limits:* Profile rules tested by vectors, not model results. The cut removes an additional key-list
check after M5; it does not remove M5. Under KEEP that check returns.
*Evidence:* [profile §6.4](V1-PROFILE.md#L816-L835).
*Question:* Does this statement describe what the evidence establishes, without claiming more?

**Row 20. E18 with its time-boxed sign-off.**
*Claim:* Codex signed off on A7.8 option (a) at the stated finite bounds (k = 6). The completed bridge run used skew
±1; the incomplete ±2 run supplies no passing evidence.
*Attacker and limits:* This establishes no arbitrary-skew or parameter-general result. E18-02 remains: provide a
repository-relative reproduction runner with a source-hash manifest.
*Evidence:* [sign-off](reviews/e18-signoff/CODEX-REVIEW.md#L45-L59).
*Question:* Does this statement describe what the evidence establishes, without claiming more?

**Row 21. The E8/E7/E11 sheet, gaps named. Do you accept it?**
The sheet contains the required prose correspondence and explicitly leaves composition unproved. Its E7 mapping gaps
remain. Its E11 index lacks V1 entries. Existing statements needing links: the bridge and k = 6 runs (in the P5c and
P5P6 aids) and E6a (its results file). Missing statements: first-link Q1, P8's adversary, the full capstone. A machine-checked signature-and-time composition is not by itself a V1
requirement. ACCEPT records the stated evidence and limits; it does not waive a registered prerequisite.
*Evidence:* [sheet gaps](../formal/E8-E7-E11-SHEET.md#L33-L95).

**Row 22. The E12 page. Do these sections state the supported reliance and its limits clearly?**
**Required read:** [`V1-RELYING-PARTY.md` lines 26–142](V1-RELYING-PARTY.md#L26-L142), about 1,200 words, 8
minutes: the bounded claim, conditions, release authentication and verdict guidance. This read does not establish
non-expert comprehension; the 4 Dec test remains. The capture paragraph (lines 98–105) describes CUT; under KEEP the
owner rewrites it.

**Row 23. Anchored-versus-unanchored-signature control. Accept?** A valid signature that is not the one committed in
`A_sig` fails: XR-10 to XR-14, 5/5; hybrid 1/1. GnuPG accepts all five alone.
*Evidence:* [PROOF.md](../formal/p8/PROOF.md#L496), [GnuPG](../formal/p8/PROOF.md#L525).

**Row 24. `ISSUANCE_WINDOW` and `DNS_WINDOW_LENGTH` vectors. Accept?** W-01, W-02, XW-01 to XW-03, XD-32, XD-33 and
DNS-02 (exactly 90 days) pass `check.py`. *Evidence:* [PROOF.md](../formal/p8/PROOF.md#L500).

**Row 25. Root-KSK rollover control. Accept?** Case L-60, a snapshot while KSK-A is published but not signing, gives
VALID. Its expected verdict and generator are in the frozen vectors object; its input bundle is not (it embeds
object hashes, EA-10), and the generator rebuilds it byte for byte.
*Evidence:* [inventory](../formal/freeze-v1/FREEZE-RECORD-DRAFT.md#L367), [generator](../prototype/conformance/cases.py#L980-L981).

**Row 26. Signer branch recorded. Accept?** HYBRID, registered 2026-10-16; stale profile lines fixed.
*Evidence:* [record](../formal/p8/HYBRID-REGISTRATION-RECORD.md#L1-L6), [hash](../formal/freeze-v1/FREEZE-RECORD-DRAFT.md#L37).

## What is NOT established

- **Instrument evidence counts for nothing** (A9.2): real receipts, differential runs, mutation tests, e2e controls.
- **Mappings are not pairs** (contract §5). G6, G7 and concrete authority have no model; G8 and G10 have no tests.
- **H2 is unadjudicated.** The H2 panel has not run.
- **After the exit:** the P3 [assumption] half, P9 code inspection, two-machine vector, C7's non-expert test,
  dead-service test. The capstone stays open; A-UTC is unchecked; no production release key exists.

## The form

KEEP or CUT on R2; ACCEPT or REJECT on the rest. Notes are optional.

```text
R1  preamble text: ACCEPT / REJECT
R2  service-key listing (AUTHOR RULING): KEEP / CUT
R3  C3 "fails" reading (OWNER CLARIFY): ACCEPT / REJECT
R4  UTC readings, notes 14-15: ACCEPT / REJECT
R5a release envelope and custody contents: ACCEPT / REJECT
R5b "imports" reading: ACCEPT / REJECT
R6  fingerprint channel rule: ACCEPT / REJECT
R7  P1: ACCEPT / REJECT
R8  P2: ACCEPT / REJECT
R9  P3 [model]: ACCEPT / REJECT
R10 P4: ACCEPT / REJECT
R11 P5: ACCEPT / REJECT
R12 P5c, E-02 gap open: ACCEPT / REJECT
R13 P10: ACCEPT / REJECT
R14 P7 type-separation half: ACCEPT / REJECT
R15 P8 bounded claim: ACCEPT / REJECT
R16 P9 contract inspection: ACCEPT / REJECT
R17 E6a with companions: ACCEPT / REJECT
R18 129 strict rows: ACCEPT / REJECT
R19 M2 and M5: ACCEPT / REJECT
R20 E18 sign-off: ACCEPT / REJECT
R21 E8/E7/E11 sheet, gaps named: ACCEPT / REJECT
R22 E12 page: ACCEPT / REJECT
R23 anchored-signature control: ACCEPT / REJECT
R24 window vectors: ACCEPT / REJECT
R25 root-KSK rollover control: ACCEPT / REJECT
R26 signer branch: ACCEPT / REJECT
```

ACCEPT records your judgment on the statement printed in that row. Owner decisions retain their provenance. R2
separately records your author ruling. REJECT is recorded with any explanation you provide; the owner identifies the
required correction or returns an explicit choice. Rejection alone does not select alternative semantics.

## What happens next

1. **Remaining owner work.** Under KEEP: build A10.4.1 with its cases; revise rows 1, 16, 19, 22 and the contract's
   capture row. Always: enter the release-checker choice in the profile (upstream GnuPG 2.4.4, as the
   [dependency manifest](../formal/dependency-sources/dependency-manifest.json) pins; the profile still says
   provisional); act on any REJECT; close E18-02; refresh A9 line references. Then reassemble the freeze once and
   finish the [freeze record](../formal/freeze-v1/FREEZE-RECORD-DRAFT.md). Only changed rows come back to you.
2. **Then the signed opening commit** (A9:218): yours, explicit, dated and signed, about 10 minutes. The owner gives
   you the exact command.
3. **If the exit slips by more than a week,** the slip rule brings you one choice: cut scope or stop
   ([V1-SCHEDULE](V1-SCHEDULE.md#L30-L31)).
