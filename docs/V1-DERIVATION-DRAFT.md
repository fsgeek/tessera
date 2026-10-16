# V1 derivation: from the claim to the evidence

> **STATUS: DRAFT, revised once 2026-10-09 after the Codex review and the skeptic read
> (`docs/reviews/v1-derivation/`). No further review round: the author is the final gate.** Owner instance (Claude
> Opus 5.5). Not adopted. Nothing here changes a registered sentence. §4 drafts Amendment 9, and every section in
> it is RECOMMENDED until the author rules. §6 records how each review finding was disposed of. The revision rule
> was the owner's: *narrow the claim until it is true*; add a mechanism only where the narrowed claim would stop
> meeting `V1-SCHEDULE.md`'s success definition.
>
> **Dated reconciliation, 2026-10-13** (not a review round; the decision history is preserved). Three slot-2
> custody passages (§2 C3 row, §2 *Signers*, §4 A9.6) are brought into line with A9.6's slot-2 custody (OWNER
> DECISION 2026-10-13) using the exact replacements of `docs/reviews/a9-custody/CODEX-REVIEW.md` finding 3. The
> replaced 2026-10-09 wording is quoted in place, marked *reconciled 2026-10-13*.

**Method.** Start from V1's claim, derive the evidence each part needs, then classify every exit item (§3). An
item the claim does not need is either registered as a named future obligation or listed as an omission with its
source line. Nothing is dropped quietly. (Codex's diagnosis: the closure process is *"better at discovering,
preserving and elaborating obligations than at retiring them"*.)

---

> **AUTHOR DECISIONS 2026-10-10, made before the amendment as Codex recommended. Amendment 9 is to implement exactly these.**
> - **A, the V1 promise: accepted as recommended.** His words: *"I accept your recommendation."* The non-promises
>   are approved with it: submitter identity, standing (reported ABSENT), wrappers and renewal, degraded
>   verification, and revocation (B).
> - **B, revocation: (i) "not evaluated".** His words: *"(i) seems to be the only honest answer; (ii) can be added
>   as an additional service without promising anything more."* The anchored "no revocation as of ship time"
>   statement is an optional add-on service that adds no promise to V1.
> - **C, the 4 Dec acceptance bar: accepted as recommended.** Zero unsafe accepts; false rejects allowed only on
>   the two named honest cases V1 does not support; a human tester. Naming the tester is separate (Q4).
> - **Q1 (adopting A9 as the instrument): OWNER DECISION 2026-10-12, adopt.** The author returned the ruling to the
>   owner: *"The decision to change that rule isn't mine, it is the owner of the project."* The owner adopts A9.
>   Formal-first stays, but tied to V1's finite claim set and not to the whole design. The throwaway prototype and
>   the spike showed that code built as an instrument sharpens the model and does not anchor it, so A9.2 replaces
>   "Before any code" (`phase-0-prereg.md:102`) with the rule A9.2 states. The author signs the amendment commit.
> - **Usage-model correction (author pushback, 2026-10-12).** The owner had said V1 cannot serve agent-to-agent
>   contracts because it attests no submitter. The author pushed back, and he is right. Parties who sign a contract and
>   put it with their signatures in `content` get exactly what a timestamp is for: the receipt shows those signatures
>   existed no later than T. Tessera vouches for no one's identity. The relying party checks the parties' signatures
>   itself. Nothing in V1 prohibits this. The scenario mapping gains cases i and i′ (A9.1) so the 4 Dec test covers it.

## 1. The claim

**V1 claim (one sentence).** *Conditional on the registered cryptographic and key-use assumptions, a V1 receipt
lets anyone holding it establish, without Tessera, that the attested content was presented to the Tessera V1
service, whose own domain is D; that each of the service's two keys K = {K_kms, K_gpg} signed its own frame
binding that content; that two named channels authenticated these keys for D at the stated evidence times; and
that the signed frames existed no later than T. Effective revocation is not evaluated, and the receipt attests
neither the submitter nor the content's meaning. The verdict is typed and says what was not established.*

V1 is, plainly, a dual-signed timestamp notary for Tessera's own domain. Its comparator is an RFC 3161 TSA token
plus an OTS proof. Its two differentiators are verification with no network and no live party, and authority
evidenced through DNSSEC and a time-anchored repository assertion instead of a CA.

| # | Atomic sub-claim | Non-claim kept beside it |
|---|---|---|
| C1 | **Bytes.** The verifier reconstructs each required signer's exact frame from the bundle. Both frames bind the same attested content and common metadata, with the designated signer's fingerprint in its slot. The receipt-anchor preimage over the two frames is defined and unambiguous. | Nothing about meaning or truth (A3 §A3.1). Payload-byte identity is not equality of the two frames. |
| C2 | **Presentation.** The content was presented at some issuance event of the V1 service (existential, not unique). | Not who submitted it (f), nor whether a replay suits the transaction (R-1.5). |
| C3 | **Signature.** Each required signature verifies over its designated frame; a missing, stripped or substituted one fails. The symbolic queries reject reattribution of the modelled signed bytes through the required key/frame bindings. | DSKS was only emulated in the prototype; concrete library/curve resistance is H1a evidence (P3 assumption half). The two keys are separate *technical* failure domains (AWS KMS and the selected slot-2 custody; with the hybrid, lattice and elliptic-curve) *[reconciled 2026-10-13; the 2026-10-09 text read "cloud HSM and local hardware token"]* under a **single controller**. V1 does not claim separation of control or independent fates, and does not claim independent approval of content (owner correction 2026-10-12). Nothing about the key lifecycle after T. |
| C4 | **Authority.** The named channels authenticated K for D at their stated evidence times: (i) a DNSSEC chain whose owner name is D, captured at issuance, validated against the verifier's own root-key configuration at the snapshot's own anchored time; (ii) an authenticated, time-anchored key assertion under the distributed repository key (a signed, OTS-anchored commit whose full commit→tree→blob path is verified). The verifier fixes the required set. | **Effective revocation is not evaluated.** Not public publication of the commit. Not the domain holder's honesty; whole-author-sphere capture is R-2.15. |
| C5 | **Time.** The framed bytes existed no later than T, the earliest verified attestation **in the presented OTS proof**. The authenticated anchor and k-th confirmation header timestamps satisfy the registered three-conjunct predicate. This is presentation-sensitive: a different presentation of the same receipt can select a different T. | No lower bound, no priority (A7 §A7.4). Header timestamps are chain-time proxies (skew, non-monotonic; A2.1). k = 6 assumes forging six mainnet blocks costs more than a receipt is worth, and canonical history at the pinned headers. A reorganization deeper than k is a residual. |
| C6 | **Verifiable without Tessera.** The verdict is a pure function of the bundle, the published V1 verifier and its distributed trust configuration. No network, no author help. The bundle carries the verification-spec identifier and hash in the signed bytes, and the spec and conformance vectors as content-addressed objects. | Custody is the holder's job. Dead-project reconstruction is not demonstrated (§3, omission 15). A receipt anchored beyond the newest pinned header is `UNVERIFIABLE` until a later configuration is obtained (an availability limit). |
| C7 | **Safe decision** (the 4 Dec acceptance criterion, not yet established). The verdict is typed. It reports `revocation: NOT_EVALUATED` and the standing value separately and never folds them in. Using the documentation alone, a non-expert makes no unsafe accept on the registered scenario mapping (A9.1). | Revocation (A9.4) and standing (A9.3) are not claimed. False rejects are allowed only on the registered cases. |

**V1's fixed profile,** `tessera-v1-strict`, carried inside the signed bytes:
- **Receipt anchor (owner decision 2026-10-12, `docs/reviews/anchor-signatures/`).** The OTS-stamped preimage commits to both frames *and* their exact signatures (tag `tessera-v1/receipt-anchor-sig`, ENCODING-V1 §5). Signatures are made and frozen before stamping. A signature made after T cannot fit the anchor, which closes pre-staging followed by later signing under keys compromised after T. The git assertion's stamp targets the signed commit id (§7.1). The verdict reports `historical_security: NOT_EVALUATED`.
- **Encoding.** `formal/p8/ENCODING-V1.md`: RFC 8785 under the **value-preserving number rule** (accept a number exactly when RFC 8785's canonical form preserves its value; this replaces the registered literal rule, see A9.8), in tag-headed frames with u16 version and u32 length. The two signer frames share the common bytes and differ only in the fingerprint slot. KMS key: `sha256` of the SPKI. GPG key: `sha256` of the OpenPGP key packet (no SHA-1). DNS key publication: TXT at `_tessera-v1.<D>`. P8 prose proof: `formal/p8/PROOF.md`; vectors with two agreeing decoders in `formal/p8/vectors/`.
- **Bundle contents.** Spec identifier and hash (signed); spec and conformance vectors (embedded, content-addressed); a bound plain-language purpose preamble; a dependency manifest (exact editions of RFC 8785, OpenPGP, ECDSA P-256, SHA-256, SHA-1 for git object linkage, the DNSSEC algorithms in the chain, OTS, Bitcoin headers).
- **Signers.** KMS-backed OpenPGP P-256 plus gpg OpenPGP P-256 (P4'). The gpg slot uses rule O under A9.6's selected slot-2 custody, through a queue-pulling policy signer outside the issuing AWS account. *[Reconciled 2026-10-13; the 2026-10-09 text read "GPG runs on author-controlled hardware outside AWS (A9.6)."]*
- **Authority.** DNSSEC for D plus the git key assertion, both required, n = 2.
- **Trust configuration** (ships with the verifier, never taken from the bundle): root KSK-2017 and KSK-2024, each with its IANA validity period (KSK-2024 signs the root from 2026-10-11; KSK-2017 is revoked 2027-01-11 and removed 2027-03-22); the repository key; a signed, versioned set of pinned mainnet header hashes covering accepted histories.
- **Verification.** Strict only. One layer, no wrappers, no renewal, no TLR, no waiver policy. Revocation not evaluated.
- **Parameters.** δ = 72 h, ε = 24 h, k = 6, N = 3, S = 24 h (A2's operational slack, wall clock).
- **Issuance.** Operated API (API Gateway + Lambda + KMS). A receipt ships only when complete; refusal never concerns a shipped receipt.
- **Dispatch.** An unrecognized profile, layer structure or request gets `UNVERIFIABLE / OUT_OF_PROFILE` without evaluating it. Inside the profile, A4.2's precedence holds: a failed required check gives `INVALID` even when another is unperformable.

---

## 2. Each sub-claim: evidence needed, held, missing

Status words are the tracker's. "checked" means the tool passes. **No row is `discharged`.** "30 Oct" items gate the
profile freeze; "H1a" items gate 20 Nov / 4 Dec.

**C1 Bytes.**
- *Needs.* A P8 prose proof of injectivity and boundary-unambiguity over the V1 domain, covering both frames and the anchor preimage; golden and rejection vectors; P1's headline.
- *Held.* P1 checked. **P8 `open`, nothing written.** The prototype shows the gap: "no two builds would interoperate today" (`FINDINGS-BY-TIER.md`); three JCS implementations agree on RFC 8785 vectors but accept different inputs (PHASE3 finding 5). A7 §A7.1/§A7.9 split frame and payload; the O-79 map is unwritten (O-79, O-01, O-03).
- *Missing (30 Oct).* The proof; the O-79 map (requester content versus signer metadata, slot order, lengths, anchor preimage, spec-id/hash and preamble fields, the KMS OpenPGP public-key packet, creation time and fingerprint); vectors; the O-78 rejection rule. *(H1a)* The V1 build reproduces the vectors byte for byte; that build is the second implementation.

**C2 Presentation.** Checked (S-P1; strict capstone). Missing: the relying-party text that a receipt does not attest the submitter (f).

**C3 Signature.**
- *Needs.* P1 (R-1.8); P2 with both slots required; P3 [model]; P3 [assumption] (O-68: library, encodings, public-key validation, explicit-curve rejection); no V1 identifier derived from signature bytes.
- *Held.* P1, P2, P3 [model] checked. Strict capstone: every strict file landed, and all 129 correct-form rows of cases (a) 47, (b) 47 and (c) 35 are as registered (`RESULTS.md` §1; (c) is the both-channels-compromised negative control). The 10 divergent companions are reds beyond their registered sets in broken variants; they cannot weaken a correct-form verdict, and V1 cites none of them nor the withheld C-C15(i) C-Q6 results. **W1:** ECDSA and OpenPGP signatures are malleable; the model assumes `sign(m,k)` unique. **M9:** KMS ECDSA + gpg OpenPGP is `INVALID` under R-3.12; only P3' and P4' pass (PHASE3 §2).
- *Missing.* *(30 Oct)* W1 at spec level (no identifier from signature bytes; unhashed OpenPGP area carries no meaning); a half-day argument that no strict query relies on signature uniqueness. *(H1a)* The P3 assumption half, at its registered phase.

**C4 Authority.**
- *Needs.* P10 and strict (a)(b)(c); owner-name check (RRset owner is D, D bound in the signed bytes); verifier-fixed required set; the M5 condition; DNSSEC validity at the snapshot's anchored time; full git path verification; a real DNSSEC chain and a real key commit.
- *Held.* P10 checked; first-link mechanism decided 2026-08-13. G-17: the capstone models the verifier-fixed set (`capstone.pv:606-607`); the spec drifted (R-3.37 / V21). **G-21 / M2:** nothing checks the owner name. **M5:** "manifest = authority tuple" holds only conditionally. **M8:** the joint RRSIG window measured 1.6 days, shorter than δ, so the snapshot needs its own time. **`gitchannel.py:125-134` checks object IDs and the commit→root-tree link only, not the path to the key blob.** **wamason.com: no DS, no AD flag** (`dig +dnssec @1.1.1.1`, re-run 2026-10-09); the author is enabling DNSSEC.
- *Missing (30 Oct).* Spec text for owner name, required set, M5, and the snapshot rule: the issuer anchors the DNSSEC snapshot with its own OTS proof; the verifier checks that the snapshot's anchored time lies inside every RRSIG window in the chain and within [declared − ε, declared + δ]; the issuer re-captures before shipping if it does not. Registration statements M2 and M5. Full commit→tree→subtree→blob verification with exact extraction of D and the key set, and a substituted-blob negative case. The two-KSK trust configuration. [A] DNSSEC live.

**C5 Time.**
- *Needs.* P5, P5c, the bridge at k = 6; the T rule; V33a; offline header authentication; ratified parameters.
- *Held.* P5, P5c, bridge checked. E18 done by path (a), 2026-09-14, at `DepthK = 5`, which is k = 6 under the registered convention `DepthK = k − 1` (`formal/PROPERTIES.md:177`); Codex's full pass is owed. **M3:** a real OTS proof carries four attestations 8.6–12.6 h apart and nothing names T; the prototype takes the earliest presented (G-55). V33a not modelled. O-22 open. E14 not begun. The prototype's header check rejects retarget crossings (`btc.py:84-87`) and pins only the k-segment (`anchor.py:85-91`).
- *Missing (30 Oct).* The T rule, registered as presentation-sensitive; pruned-proof vectors at both window boundaries; the header rule: every bundle header must be in the pinned set, otherwise `UNVERIFIABLE / HEADERS_NOT_COVERED` (no retarget logic, because the pins cover every accepted header); negative vectors for a header absent from the pins and a header conflicting with them; parameters ratified (A9.2); the E18 Codex pass, time-boxed.

**C6 Verifiable without Tessera.**
- *Needs.* P9 (A4 §A4.1, A5 §A5.1); the trust configuration; the bundle contents above; the dead-service test.
- *Held.* **P9 `open`;** inputs listed in `RESULTS-PROBE.md` Q6, no inspection artifact. Examiner and consumer personas exist in the prototype.
- *Missing.* *(30 Oct)* P9 as an inspection of the verifier's declared dependency contract; a one-page trust-configuration note. *(H1a)* Inspection of the actual verifier, the two-machine vector, and the dead-service run; E10 extraction.

**C7 Safe decision.**
- *Needs.* P4's partition; E6a (dispatch, A4.2 precedence, a fail-open companion); the relying-party page; the scenario mapping registered before any V1 run; the A9.4 missing-capture test.
- *Held.* P4 checked. E6 rows not modelled. E12 drafted only (spec §1.5). Phase 2: both integrators accepted (e) and (f) on the headline.
- *Missing.* E6a with a mixed failed/unperformable case and missing-signature versus missing-evidence cases; the relying-party page; the mapping (A9.1).

---

## 3. Every exit item and open tracker row, classified

| Item | Class | Sub-claim or capability | When | Real state, 2026-10-09 |
|---|---|---|---|---|
| E1 P1–P5, P5c, P7 type-separation, P10 | **NEEDED** | C1–C5, C7 | 30 Oct | All checked, none discharged |
| E1 / P6 | **DESIGN** (+ weakening, A9.4) | Long-term validation (T4) | later | Checked; V1 does not evaluate it |
| E2 / SC standing row | **DESIGN** | Protocol standing | later | `open`; A8.4 query in the running batch |
| E3 / P8 | **NEEDED** | C1: both frames, preimage, spec binding, number domain | 30 Oct | Not begun |
| E4 / P9 | **NEEDED** | C6: contract inspection at exit; code + dead-service at H1a | 30 Oct / 4 Dec | Inputs listed, no inspection |
| E5 strict (a)(b)(c), correct form | **NEEDED** | C3, C4 (129 rows as registered) | done | Landed; capstone rulings deferred 2026-10-07 |
| E5 case (d) eleven + slice batch | **DESIGN** | Degraded verification | later | Batch running; read after V1. Not a V1 gate |
| E6a unknown-algorithm / dispatch | **NEEDED** | C7 | 30 Oct | Not modelled |
| E6b extended refusal entry | **DESIGN** | Portable refusal records; bounded local refusal stays NEEDED as operated behaviour | later / 20 Nov | Not modelled |
| E7 prose mapping per lemma | **PROCESS** | V1 queries only; on the one-page E8 sheet | 30 Oct | Claim blocks exist |
| E8 TLA+ ↔ symbolic correspondence | **NEEDED** | C3 × C5: one page naming each join; the unproved composition stated | 30 Oct | Not begun |
| E9 author adjudication | **PROCESS**, mandatory | V1 rows, under the A9.2 closure rule | 28 Oct | S-P3 and C5 headers read |
| E10 conformance vectors | **NEEDED** | C6, C7: spec + extraction by 13 Nov (A9.2 changes BAND0-EXIT reading (b)) | 13 Nov | Not begun |
| E11 written-proof index | **PROCESS** | Traceability; on the E8 sheet | 30 Oct | Reading aids exist |
| E12 relying-party story | **NEEDED** | C7: page by 30 Oct, acceptance test 4 Dec | 30 Oct | Draft (spec §1.5) |
| E13 coverage map | **PROCESS** | Refresh, listing excluded cells | 30 Oct | Done for the full scope |
| E14 parameters, including S | **NEEDED** (author ratifies) | C5 | 16 Oct | Not ruled |
| E15 first-link residual | **PROCESS** | Disposition recorded by the author inside E9 | 28 Oct | Partial |
| E16 implementation spec | **NEEDED** as the V1 profile extract; full spec is design reference, synced after V1 | C1–C7 | 30 Oct | 2929-line draft |
| E17 exit act | **PROCESS** | V1-scoped exit; discharges no unoffered capability | 30 Oct | — |
| E18 k = 6 evidence | **NEEDED** (runs) + PROCESS (time-boxed sign-off) | C5 | 30 Oct | Runs done; Codex pass owed |
| P3 [assumption] half | **NEEDED** at its registered phase | C3 | 20 Nov | Open |
| A2.2 vector cases | **NEEDED** | C5, C7: header and pruned-proof vectors at 30 Oct, extraction at H1a | 30 Oct | Not extracted |
| W1 in S-STANDING | **DESIGN** (V1 identifier rule stays NEEDED, C3) | Protocol standing | later | — |
| Integrated lifecycle model | **DESIGN**, trigger overridden in A9 | Wrapping and renewal | later | Not begun |

**Counts:** 13 NEEDED (E1, E3, E4, E5-strict, E6a, E8, E10, E12, E14, E16, E18, P3-assumption, A2.2); 6 DESIGN (P6,
E2, E5-(d), E6b, W1-standing, lifecycle); 6 PROCESS (E7, E9, E11, E13, E15, E17), all required for V1.

**Retained without change:** H3's three cost numbers (prereg:232-248, measured at 20 Nov; they are V1's "stated
cost"); the red-bar/CI separation rule (prereg:548-553); unloggable keys; break-chain attacks on the receipt,
authority and anchor chains (prereg:203-205).

**Commitments V1 omits or changes.** Kind: **W** property weakened, **C** capability not offered, **G** gate or
trigger moved, **H** hypothesis withdrawn, **T** test registration changed. Paths are `docs/` unless given.

| # | Registered sentence | file:line | What V1 does | Kind | A9 § |
|---|---|---|---|---|---|
| 1 | §8 gate: "Band 0 (H0) must be resolved before Phase 1 begins" | `phase-0-prereg.md:714-724` | A V1 profile gate replaces it for V1 code only; the original H0 stays unresolved | G | A9.2 |
| 2 | Capstone gate: "every ledgered cross-model assumption … discharged … broken companion" | `phase-0-prereg-amendment-3.md:220-231` | Strict correct-form rows only; case (d), divergences and withheld results stay with the capstone | G | A9.2/.3 |
| 3 | The "v1 product" done-line and kill criterion | `phase-0-prereg.md:590-617` | Not V1; kept as the later product done-line. PCI, scale and ownership objectives are unfulfilled at V1 | C | A9.1 |
| 4 | H1a red-bar "for … each degradation scenario" | `phase-0-prereg.md:205` | Degradation and wrapper cases move to their capabilities; break-chain stays | G | A9.5 |
| 5 | H1b: LocalStack at 1/sec within 7 days of the H1a freeze | `phase-0-prereg.md:210-224` | Withdrawn for V1; not falsified | H | A9.1 |
| 6 | P6: `key_authorized(declared)` and "no revocation effective at or before anchor_time"; A4.3's boundary; prereg §4.4 | `phase-0-prereg-amendment-1.md:199-214`; `phase-0-prereg-amendment-4.md:111-123`; `phase-0-prereg.md:539-546` | Neither condition evaluated for V1 bundles | W | A9.4 |
| 7 | "The PQ signature implementation … gates the production version" | `phase-0-prereg-amendment-3.md:473-476` | V1 is not the production version; the trigger stands | C | A9.1 |
| 8 | Standing modelled before Band 0 exit; standing invariant | `formal/spike/FIRST-LINK-SPIKE.md:50-56`; `phase-0-prereg-amendment-3.md:531-557` | No TLR; standing `ABSENT/NOT_ISSUED_IN_PROFILE`, reported separately (the separation itself is kept); A2 residue O-17 disclosed | C, G | A9.3 |
| 9 | Refusal-record decomposition, commitment, both companions | `phase-0-prereg-amendment-3.md:572-580`, `:816-828` | Bounded local refusal, returned by the API; no portable record | C | A9.3 |
| 10 | Integrated lifecycle model green "before the H1a crypto-core freeze" | `phase-0-prereg-amendment-3.md:783-806` | Trigger overridden for V1. The 30 Oct profile freeze is not the crypto-core freeze, which follows at H1a | G | A9.3 |
| 11 | Custodial renewal "before the old mechanism becomes unreliable" | `phase-0-prereg-amendment-3.md:273-278` | No renewal protocol, no wrapper interpretation; custody and algorithm dependency stated | C | A9.5 |
| 12 | Dual signing with "local GPG" in an independent failure domain | `phase-0-prereg.md:292-294` | Kept (A9.6) | — | A9.6 |
| 13 | A8.4's spec edits (O-74, R-6.44 innermost) | `phase-0-prereg-amendment-8.md` §A8.4 | Postponed with standing; A8 remains the source record | G | A9.3 |
| 14 | Prototype scenario expectations | `prototype/consumers/scenarios.py:72-133` | Preserved as history; V1 mapping registered prospectively | T | A9.1 |
| 15 | Dead-project (clean-room reconstruction) demonstration | `phase-0-prereg-amendment-3.md:371-378` | Not run for V1; the dead-service test is run | G | A9.2 |
| 16 | Forward-link successor slot registered "before format freeze with a slot-bearing golden vector" | `implementation-spec.md:651-656`; `formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:159-206` | Not in the V1 profile; a later profile id carries it with its own vector | C, G | A9.3 |
| 17 | §4.7 review recency attested (hard rule) | `phase-0-prereg.md:564-572` | Not offered by V1; moves with the product done-line | C | A9.1 |
| 18 | Custodial parameter schema and clock roles ratified at Band 0 | `phase-0-prereg-amendment-3.md:435-451` | Trigger moves to the renewal capability | G | A9.3 |

---

## 4. Draft: Amendment 9

```
# Tessera — Phase 0 Pre-Registration, Amendment 9 — V1: the claim, the profile, the re-scoped gate,
  and the obligations carried forward (2026-10-xx)

> Status: PROPOSED. The author's first commit containing this file is its signing act (the house form
> since Amendment 5). Drafted by the AI collaborator (Claude Opus 5.5, owner instance) from
> docs/V1-SCHEDULE.md and docs/V1-DERIVATION-DRAFT.md. Layered on the original and Amendments 1–8,
> none edited. Every change is listed by kind in V1-DERIVATION §3; nothing outside that list changes.
```

**A9.1 V1's success definition, claim and scenario mapping. RECOMMENDED.**
- *Adopts* `V1-SCHEDULE.md`'s success definition with §1's claim sentence, and refines clause 2 to: *zero unsafe accepts on the registered mapping; false rejects only on the cases registered below.*
- *Distinguishes* V1 (a profile and milestone) from the "v1 product" done-line (`phase-0-prereg.md:590-617`), which stands with the H2 panel and kill criterion. V1 is not the production version, so PQ does not gate it. Omissions 3, 7, 17 apply.
- *Withdraws H1b for V1* (`phase-0-prereg.md:210-224`); recorded as withdrawn, not falsified.
- *Issuer invariant.* A V1 receipt ships only when complete; an operator refusal never concerns a shipped receipt.
- *Registers, before any V1 run, the V1 mapping* (prototype results preserved as history). In every row: profile `tessera-v1-strict`, strict request, `revocation: NOT_EVALUATED`, standing `ABSENT/NOT_ISSUED_IN_PROFILE`.

| Case | Fixture transformation | Expected verdict | Safe decision |
|---|---|---|---|
| a, g | Honest receipt as shipped (a's TLR removed: V1 issues none) | `VALID_STRICT` | Accept as: these bytes were presented to Tessera by T |
| b | Unchanged (reattribution under attacker keys) | `INVALID` | Reject |
| c | Unchanged (two-layer transplant) | `UNVERIFIABLE/OUT_OF_PROFILE` | Reject |
| d1 | a's bundle; degraded request, then a strict request | Waiver request refused; strict request `VALID_STRICT` | Accept under strict only |
| d2 | a with repo evidence removed | `UNVERIFIABLE` (required evidence missing) | Reject: **registered false reject** |
| d3 | Unchanged clone, TLR removed (one key, one channel) | `INVALID` (missing required signature outranks the missing channel, A4.2) | Reject |
| e, e′ | a's bytes; slot-B key revoked inside (declared, anchor], or (e′) before declared | `VALID_STRICT` | Non-revocation **not established**; a transaction that needs it must not rely on this receipt alone |
| f | Unchanged (impostor's content through the honest service) | `VALID_STRICT` | The receipt attests no submitter; do not treat it as the named organisation's statement |
| h | Unchanged (honest renewal wrapper) | `UNVERIFIABLE/OUT_OF_PROFILE` | Reject: **registered false reject** |
| i | New fixture: `content` = a contract plus two valid party signatures over it, issued honestly | `VALID_STRICT` | Accept as: this signed contract existed by T. The parties' signatures and keys are the relying party's to check; the receipt says nothing about them |
| i′ | As i, but one party signature does not verify | `VALID_STRICT` (Tessera does not read `content`) | Reject the *contract*: the receipt is valid, but a party signature fails the relying party's own check |

- *Predicted 4 Dec outcome, registered:* a headline-only reader fails (e) and (f). The test measures whether the documentation prevents that. The model-derived vectors (E10) form the larger conformance set; they test the verifier, not comprehension.

**A9.2 The Band 0 gate, re-scoped to V1's claims. RECOMMENDED.**
- *Exit gate (30 Oct), for profile `tessera-v1-strict` only:* P1, P2, P3 [model], P4, P5, P5c, P10 and P7's type-separation half `checked`; P8 by prose proof plus golden and rejection vectors that survive a time-boxed falsification attempt (A1 §A1.4; O-51); P9 as a contract inspection; E6a with its companions; the 129 strict correct-form rows plus statements M2 and M5; E18 with its time-boxed sign-off; the one-page E8/E7/E11 sheet; the E12 page.
- *Acceptance gates after exit:* 20 Nov: P3 assumption half, code inspection for P9, E10 vectors run against AWS, bounded local refusal, H3 measured. 4 Dec: relying-party test and dead-service test. E10 extraction moves to 13 Nov (BAND0-EXIT reading (b) changed); P8's layout vectors stay before the freeze.
- *Not discharged:* the original H0, the full capstone gate, and every A9.3 obligation. The exit opens Phase 1a for V1-profile code only.
- *Replaces "Before any code"* (`phase-0-prereg.md:102`, author clarification 2026-08-29: code intended for the service) with: **no code that carries a V1 claim is written until that claim's exit row is `checked`.** Code built as an instrument (prototypes, spikes, probes) is allowed before exit. It must be labelled as such, it never ships, and nothing it produces discharges an obligation.
  *Superseded by Amendment 9 A9.2 (2026-10-12 review disposition): one gate, no V1 issuer or verifier code before the whole 30 Oct exit; instrument code defined by location (`prototype/`, `formal/spike*/`); relabelled a weakening (W).*
- *Closure rule.* Each review is time-boxed and dated. A finding raised after its review date gates V1 only if it (a) gives a concrete counterexample to C1–C7, or (b) shows that one of C1–C7 lacks the evidence this document assigns it (an evidence gap, with no attack needed); *(widened 2026-10-10 after Codex's review at the author's request: the counterexample-only rule would have excluded legitimate evidence gaps)* any other finding goes to the A9.3 register with a named capability. The author's E9 read is accept or reject per row and raises no new gating questions.
- *Parameters.* δ = 72 h, ε = 24 h, k = 6, N = 3, S = 24 h ratified (E14).

**A9.3 Obligations carried forward, each named with its capability. RECOMMENDED.** Each stays registered with its
original text; its V1-era trigger is replaced by "before the named capability is offered", and only a later
profile offers it.

| Obligation | Future capability |
|---|---|
| Submitter attestation, per-organisation issuer (PHASE2 design question 2) | **Attributed receipts**, the commercial path; comparator RFC 3161 + OTS |
| SC row, A8.4 query, W1 in S-STANDING, O-74, R-6.44, TLR | **Protocol standing** |
| P6 status capture and freshness bound F, continuing DNSSEC status capture, revocation-timing vectors (before declared; between anchor and declared, both orders; after both; conflicting; backdated) | **Long-term validation (T4)** |
| Forward-link successor slot and its vector (omission 16) | **Service succession** |
| E6b, refusal decomposition and both companions (omission 9) | **Portable refusal records** |
| Lifecycle model, P7 wrapper half, A6.1 vector, O-30, custodial parameter schema, RFC 4998 renewal | **Wrapping and renewal** |
| Case (d) eleven, A8.3 slices, A1 §A1.2.1 waiver lattice, A5.3 record, M6, M7 | **Degraded verification** |
| n-ary channels (O-69), *m*-of-*n* | **Jurisdictional diversity (T3)** |
| PQ path (A3 §A3.6) | **Production version** |

**A9.4 Revocation in V1. RECOMMENDED; a weakening under A1 §A1.1.**
- *What is weakened.* For `tessera-v1-strict` bundles, `VALID_STRICT` evaluates neither of P6's conditions: `key_authorized(declared_issue_time)` against effective revocation, and no revocation effective at or before `max(anchor_time, declared_issue_time)` (A4.3). V1 verifies the channel assertions and their bindings only. Every report carries `revocation: NOT_EVALUATED`, displayed next to the verdict.
- *Why.* Under the registered text, a verifier that cannot evaluate revocation would return `UNVERIFIABLE` for every receipt (P4). That result would still show which checks passed, but it would make no overall claim.
- *Issuer duty.* The V1 issuer never re-authorizes a key (R-5.24). V1 defines no revocation publication, and the documentation sends relying parties to none.
- *Contract for later verifiers (b).* Missing LTV capture does not by itself invalidate a V1 receipt: a later verifier, given a v1 bundle with no captured status, returns the same verdict and the same values in a declared stable field set. Later authenticated adverse evidence may change a later, stronger assessment, which is reported separately. **This is not non-repudiation.** Evidence: a missing-capture companion that returns `INVALID` or `UNVERIFIABLE` must go red; honest AWS receipts frozen as `G_v1` are regression evidence, not a proof of the contract.

**A9.5 Strict-only and standalone. RECOMMENDED.**
- *Dispatch and aggregation.* As in the profile: out-of-profile at dispatch, A4.2 precedence inside it. An unsupported request over an intact bundle is distinguished from a fresh strict request.
- *H1a's suite.* Forge, tamper, backdate, break-chain (retained chains), strip-one-signature, out-of-profile, and the A9.1 mapping. Degradation and wrapper instances move to their capabilities.
- *Future compatibility.* A later wrapper must preserve the inner V1 assessment under identical declared inputs and report its outer and LTV assessments separately. This is a future obligation, not something already checked.
- *Custody.* V1 offers no renewal. Long-horizon validity depends on the dependency manifest's algorithms (including SHA-1 in git object linkage) and on the holder keeping the bundle. Independent custodians may later renew under another profile.

**A9.6 Signers. RECOMMENDED (owner's engineering decision, stated for the record).** P4' pairing: KMS-backed
OpenPGP P-256 plus gpg OpenPGP P-256. The verification primitive is "an OpenPGP signature over the designated
frame"; KMS signs a digest it cannot interpret. The gpg slot uses rule O under A9.6's selected slot-2 custody,
through a queue-pulling policy signer outside the issuing AWS account. *[Reconciled 2026-10-13. Decision history,
the 2026-10-09 text: "GPG runs on author-controlled hardware outside AWS, pulling from a queue with no inbound path,
as registered ("local GPG", `phase-0-prereg.md:292-294`). V1's stated availability includes that machine. A VPS at
a second provider was considered and set aside: it would exceed H3's $5/month footprint and depart from the
registered placement."]* No identifier is derived from signature bytes (W1).

**A9.8 The number rule, for the V1 profile. RECOMMENDED; supersedes a registered sentence.** prereg §4.3 and A1 P8 reject
a number not exactly representable as an IEEE 754 double. That rule does not compose with RFC 8785: it accepts
inputs whose canonical form it then rejects (`formal/p8/ENCODING-V1.md` §9 D-1). For `tessera-v1-strict`, the rule is
replaced by: accept a number exactly when RFC 8785's canonical serialization preserves its value; reject otherwise.
Proof: `formal/p8/PROOF.md` Lemma 3. Vectors: `formal/p8/vectors/`. The prototype's SBOM case (CVSS 9.8) is
accepted under the new rule. The superseded sentences are named and left standing.

**A9.7 What changed.** One property is weakened (P6, both conditions, V1 bundles only). One hypothesis is withdrawn
(H1b). Nine gates or triggers are moved (§3 kind G: rows 1, 2, 4, 8, 10, 13, 15, 16, 18). The product done-line is
separated, and the capabilities in rows 3, 7, 8, 9, 11, 16 and 17 are not offered. One test registration changes
(row 14). The credibility line and §8's "does not proceed" clause are unchanged. A8 remains the source record.

**Owner decisions, not routed:** P8's method; signers (A9.6); standing omitted; the header-pin rule; the DNSSEC
snapshot rule; E18 read as k = 6 under `DepthK = k − 1`; the V1 build as the second encoder.

**Author questions (5 of the 8-ruling budget; 3 remain for 20 Nov, 4 Dec and ship-or-stop):**
1. **Q1. Adopt A9: (now including A9.8, the number rule)** the narrowed claim, the re-scoped gate under the closure rule, the 18 listed changes, and the parameters (δ 72 h, ε 24 h, k 6, N 3, S 24 h)? *Owner recommends yes.*
2. **Q2. The 4 Dec criterion:** adopt the A9.1 mapping, with "zero unsafe accepts; false rejects only on d2 and h"? *Owner recommends yes.*
3. **Q3. Revocation:** (a) `NOT_EVALUATED`, as in A9.4; or (b) at ship time (after k = 6, so after `anchor_time`), the issuer embeds a git-channel statement, OTS-anchored, that no revocation of K was effective at or before ship time. (b) turns one conjunct into an evaluated, issuer-asserted check. It stops a thief who holds K but not the repository key from minting receipts that pass after a revocation. It does not catch a revocation decided later with a backdated effective time. It costs about 1.5 owner-days before 30 Oct and adds one more anchoring cycle, a few hours, to every receipt's latency. *Owner recommends (a):* the narrowed claim already meets the success definition, and (b) can be added later in its own profile.
4. **Q4. Who is the 4 Dec tester?** *Owner recommends* one named human non-expert integrator, with a fresh non-author model as extra evidence only. A model as the sole tester would change the success definition, and that needs your ruling here.
5. **Q5. Should wamason.com, a personal domain, be the issuing authority?** *Owner recommends* yes for V1, stated as a demonstration, with a non-personal domain as a precondition of Attributed receipts. This needs an answer before the DNSSEC set-up finishes, because D goes into the signed bytes.
   > **RULED by the author 2026-10-09: yes.** His words: *"I do control wamason.com, so it's a perfectly reasonable choice for now."*

---

## 5. Remaining work to 30 October

Today is Fri 9 Oct, which leaves 15 working days. Sizes are owner or agent effort. **[A]** marks a step that needs
the author. Three tracks run in parallel. P8 starts Monday and does not wait for the 16 Oct signing, because its
inputs are owner decisions fixed above.

**Track 1, the critical path (Opus).**
1. **P8**, 12–16 Oct, **4 d.** The O-79 map (both frames, anchor preimage, spec-id/hash and preamble fields, OpenPGP fingerprint definition), the prose proof, and golden and rejection vectors.
2. **P8 falsification**, 19–20 Oct, a **2-day time-box** (Codex). No counterexample means P8 is done. A counterexample gets one repair day (21 Oct). If it needs more than that, the slip rule applies.
3. **Vectors frozen**, 22 Oct. Spike findings are merged by 23 Oct.
4. **E9 packet**, 26–27 Oct, **1 d.** One file holding each V1 row's statement, its open findings under the closure rule, P8's plain-language statement and the E12 page.
5. **[A] E9 read**, 28 Oct, **about 2 h.** Accept or reject per row, plus the E15 disposition.
6. **[A] E17**, 30 Oct, **10 min.** The signed V1-scoped exit commit.

**Track 2, the profile (Sonnet).**
7. **Profile document** (E16 extract), 12–14 Oct, **2 d.** Bundle format, profile id, dispatch and stages, trust configuration, dependency manifest, number rule, the A9.1 mapping. Each requirement is tagged to its source. Only this document is edited; the 2929-line spec is synced after V1.
8. **Spec fixes in the profile**, 15–20 Oct, **2.5 d.** W1; G-21 and M2; G-17; M5; the T rule (presentation-sensitive); the header-pin rule; the DNSSEC snapshot rule; `NOT_EVALUATED`; dispatch and precedence.
9. **E6a**, 19 Oct, **1 d.** With the mixed-case and missing-signature versus missing-evidence companions.
10. **E12 page, P9 contract inspection, one-page E8/E7/E11 sheet, malleability argument, E18 Codex pass (time-boxed)**, 20–23 Oct, **3 d.**

**Track 3, the mechanisms and the spike (Sonnet, prototype `real/` code).**
11. **Git path verification**, 13 Oct, **3 h.** Full commit→tree→blob path, exact extraction of D and the key set, and a substituted-blob negative case.
12. **DNSSEC snapshot**, 14–15 Oct, **1 d.** Its own OTS anchor, the RRSIG-window check, and the two-KSK trust configuration.
13. **Pinned headers and vectors**, 16 Oct, **0.75 d.** The pin set, two negative vectors, and pruned-proof vectors at both window boundaries.
14. **[A] DNSSEC live for D.** In progress. The AD flag and the key TXT record are needed by 19 Oct.
15. **Real-world spike**, 21–22 Oct, **1 d.** One mainnet receipt under the real D, verified offline on a second machine. Measure Route 53's actual RRSIG windows. A finding that changes bytes goes into step 3.
16. **[A] Two small author acts.** Sign the key commit for step 15 (10 min) and set the AWS monthly cap (10 min).

**Off the path (after 30 Oct):** the E10 spec and extraction (by 13 Nov), the slice-batch read, the full-spec
sync, and the 20 Nov build. The build includes KMS-backed OpenPGP packet construction and the queue signer, and is
sized at the start of November.

**Critical path:** P8 (12–16 Oct) → falsification (19–20) → repair, if needed (21) → freeze (22) → E9 packet
(26–27) → author read (28) → E17 (30). The DNS branch (DNSSEC live by 19 Oct → spike 21–22 → merge 23) joins at the
freeze. Float is about 2 days: 23 Oct, plus 29 Oct.

**Totals.** About 19 owner-days across three tracks, 1 of them contingent on a repair. Author time: about 4.5 h,
covering the A9 read, the DNSSEC set-up, the E9 read and the two small acts, within the 6 h budget.

**Verdict on 30 Oct.** Credible as a ceiling, with about 2 days of float, provided three things hold: DNSSEC for D is
live by 19 Oct; P8's falsification finds nothing that needs more than one repair day; and the author is available
on 16 and 28 Oct. If DNSSEC is late, or the spike forces a change to the bytes, the realistic date is **6 Nov**,
which is within the slip rule's one week. That would be brought to the author as a cut-or-stop choice, not
extended quietly.

---

## 6. Review dispositions

Codex = `CODEX-REVIEW.md` §n; S = `SKEPTIC.md` finding n. Two findings were split by the owner's pre-disposition
and are marked "split".

| Finding | Disposition | Where applied |
|---|---|---|
| Codex 1 two signer-specific frames | WORDING | C1, C3; the O-79 map defines both frames and the anchor preimage (P8, §5 step 1) |
| Codex 2 P6 removes more than one conjunct | WORDING | Claim sentence, C4, A9.4 (both conditions), omission 6, case e′ |
| Codex 3 non-repudiation test false; A4.3 boundary | WORDING | A9.4 contract (b), `max(anchor, declared)`; timing vectors moved to T4 (A9.3) |
| Codex 4 git channel is not publication; path gap | split: WORDING + MECHANISM (3 h) | C4 "authenticated, time-anchored key assertion"; §5 step 11 |
| Codex 5 M8 contains V1 work | MECHANISM (1 d) | Profile trust configuration (both KSKs); C4 snapshot rule; §5 step 12; status capture moved to T4 |
| Codex 6 earliest-attestation pruning | WORDING | C5 presentation-sensitive; pruning claim deleted; vectors in §5 step 13 |
| Codex 7 chain time versus wall clock | WORDING | C5, profile S = 24 h; latency claim removed |
| Codex 8 header authentication incomplete | MECHANISM (0.75 d) | Pinned headers; `HEADERS_NOT_COVERED` limit in C6; §5 step 13 |
| Codex 9 C2/C3 overreach | WORDING | Claim conditional; C3 non-claims; A9.6 (custody, not approval); P8 fingerprint input |
| Codex 10 bundle content, dead-project test | split: MECHANISM (0.5 d, in P8 and the profile) + OMIT | Profile bundle contents, C6; omission 15 |
| Codex 11 out-of-profile overrides P4 precedence | WORDING | Profile dispatch, A9.5, E6a cases |
| Codex 12 C7 is an acceptance test | WORDING | C7 marked 4 Dec criterion; case e decision; Q4 |
| Codex 13 fixtures do not fit the profile | WORDING | A9.1 mapping table; omission 14 kind T |
| Codex 14 missing commitments | OMIT | Omissions 16–18; H3, break-chain, red-bar/CI and number rule retained (§3) |
| Codex 15 omission-row audit | WORDING | §3 rows 1–14 (paths, kinds, sources) |
| Codex 16 classification audit | WORDING | §3 table rebuilt with a "When" column; counts 13/6/6; "worthwhile only if T4" removed |
| Codex 17 "173/173" misstated | WORDING | C3 held: 129 correct-form strict rows; divergences not cited |
| Codex 18 A9 supersession | WORDING | §3 Kind column; A9.2 gates split; A9.7 |
| Codex 19 30 Oct plan not a schedule | WORDING | §5 re-planned with tracks, dates and critical path |
| Codex 20 long-horizon assumptions | WORDING | Profile dependency manifest; A9.5 |
| Codex 21 current-evidence language | WORDING | DNS re-checked and dated; `UNVERIFIABLE` is described as scoped results, not useless |
| S1 what V1 is; attribution | WORDING | Claim (D is the service's own domain), comparator, A9.3 Attributed receipts, number rule |
| S2 case (e) remedy does not exist | WORDING | A9.4 issuer duty (no publication; "both channels" dropped); A9.1 safe decision and prediction |
| S3 a cheaper revocation option | WORDING | Q3 (b), evaluated; the old (b) strawman and (c) are dropped |
| S4 success definition fails by construction | WORDING | A9.1 clause 2 refined; registered false rejects d2, h |
| S5 standing `ABSENT`, ship invariant | WORDING | Issuer invariant (profile, A9.1); E12 covers standing |
| S6 header authentication is design work | MECHANISM (with Codex 8) | Pins instead of retarget; C5 economic assumption; spike (§5 step 15) |
| S7 DNSSEC at T, M8 twice | MECHANISM (with Codex 5) | Snapshot evaluated at its own anchored time; M8 split |
| S8 classification corrections | WORDING | Cuts in §5; second encoder is the V1 build. *E18 sub-point rejected:* `DepthK = 5` is k = 6 by `DepthK = k − 1` (`PROPERTIES.md:177`) |
| S9 non-converging review phrasing | WORDING | A9.2 closure rule; time-boxes in §5 |
| S10 A9.7 undercounts | WORDING | A9.7 counts by kind |
| S11 schedule serial, no slack | WORDING | §5 critical path, early start, spike |
| S12 author questions | WORDING | Q1–Q5 rebuilt; engineering choices listed as owner decisions; tester and domain questions added |
