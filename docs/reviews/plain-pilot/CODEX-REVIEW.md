# Codex faithfulness review of the A9 plain-language pilot

Reviewed 2026-10-16. **Result: revision required before reliance or publication.**

The pilot preserves much of A9, but it removes material conditions and changes several claims. It also omits entire source clauses. Passing the sentence-length check does not make it faithful.

Only this review file is an output of this review. No proposed change below amends A9 or approves a dictionary entry.

## Basis and method

Compared the complete `docs/plain/A9-PLAIN-PILOT.md` with the opening “The claim,” “The adversary,” and “The boundaries” and A9.1 rows C1–C7 of `docs/phase-0-prereg-amendment-9.md`. Applied `docs/plain/STE-STYLE.md`. Source references below use **A9**, **Pilot**, and **Style**, with their original line numbers. Referenced source rules were inspected where needed; other drafts do not override A9. The cited ENCODING-V1 clauses were also checked at A9's signing commit `2ad3489`; their line locators below refer to the workspace copy.

Snapshot: repository HEAD `44f921e2df2ea963eca7e32ab749349cc29c08ff`.

| Input | SHA-256 |
|---|---|
| Pilot | `301f982c5b8a3eb3e80e3b18b32ab30df2b9b9bdba603410c9740ff724c91a06` |
| Style | `a3798ce31c131ebb4e906e61eb64ff2e248a0a4cf79e0179000191cb3e208dea` |
| A9 | `ff09f9b1ff6bb717bcca2c2f803eb8674f4beb2d28e88d5718320fe9b63c9f05` |

A9's header still says “PROPOSED” and “not yet signed” (lines 3–4), but the same header defines the author's first containing commit as its signing act. Git history records that act at `2ad3489` on 2026-10-16. The pilot's statement that A9 governs is consistent with that house form. Git reported signature status `U` (unknown verification trust); this review does not claim independent cryptographic authentication of the signing commit.

The ledger includes every sentence and every sentence-like fragment, including metadata, list lead-ins, references, and owner notes: **79 units**. Headings are checked separately. Each unit has one primary decision. A primary DROPS can accompany a secondary meaning change; the finding explains both. FAITHFUL means locally faithful to the source, read with the surrounding qualifications; it does not certify the pilot as a whole or validate A9's underlying claim. Editorial safeguards and review instructions are identified as such, rather than mistaken for new V1 requirements.

For every non-FAITHFUL unit, the ledger quotes the pilot verbatim and links a finding that quotes A9 and proposes replacement text. Omission-only findings follow the ledger findings, because an absent sentence cannot receive a sentence ID.

**Replacement conventions.** Proposed plain text uses short, active sentences and “must” for requirements. Conditions are lists. Existing approved words keep their dictionary meanings. **[D]** marks text that requires the vocabulary additions or repairs described in the style findings. That text is a proposed faithful rendering, but it cannot honestly be certified against the current dictionary. The present dictionary cannot express all the requested source rules without such changes. **[A]** marks an unresolved source issue: wording preserves the explicit source rule, and does not invent a resolution.

## Sentence ledger

“Words” counts whitespace-separated words after removing list numbering and the editorial “Not claimed:” label. Hyphenated terms, dates, identifiers and paths each count as one word. The maximum with those two-word labels included is still 17. Instructions also fit the 20-word limit. Each bullet fragment is checked separately. Sentence IDs exclude heading labels such as “C1. The bytes.”

| ID | Pilot line | Pilot text (quotation) | Words | Decision | Finding or basis |
|---|---:|---|---:|---|---|
| S01 | 3 | “Status: PILOT, owner instance, 2026-10-16.” | 5 | **FAITHFUL** | Editorial status. |
| S02 | 3 | “This is a plain rendering of the opening of Amendment 9 and its claims C1 to C7.” | 17 | **FAITHFUL** | Editorial scope. |
| S03 | 4 | “Amendment 9 is the signed text, and it governs.” | 9 | **FAITHFUL** | Signing act and governing precedence; see basis. |
| S04 | 4 | “Words in this document have the meanings in `docs/plain/STE-STYLE.md`.” | 9 | **FAITHFUL** | Editorial dictionary reference; compliance checked separately. |
| S05 | 5 | “A faithfulness review must occur before anyone relies on this text.” | 11 | **FAITHFUL** | Editorial reliance safeguard; Style 23–26. |
| S06 | 9 | “Tessera V1 is a service that makes receipts for wamason.com.” | 10 | **FAITHFUL** | A9 32; own-domain service. |
| S07 | 11 | “A receipt proves four things:” | 5 | **DROPS** | [F01](#f01) |
| S08 | 13 | “The service received this exact content.” | 6 | **FAITHFUL** | A9 34; presentation, subject to F01. |
| S09 | 14 | “Both keys of the service signed it.” | 7 | **FAITHFUL** | A9 34–36; opening shorthand, qualified by C1. |
| S10 | 15 | “Two authority records said that these keys belong to wamason.com, for a stated window.” | 14 | **DROPS** | [F02](#f02) |
| S11 | 16 | “The content and both signatures existed at the anchor time T or before T.” | 14 | **FAITHFUL** | A9 36–37; source clock ambiguity A01 remains. |
| S12 | 16 | “Bitcoin fixes T.” | 3 | **FAITHFUL** | A9 37; selection addressed in F16. |
| S13 | 18 | “A person can check a receipt without Tessera and without the internet.” | 12 | **FAITHFUL** | A9 33–34; offline, independent check. |
| S14 | 18 | “The person needs only the receipt, a verifier and its trust file.” | 12 | **FAITHFUL** | C6; trust file means the distributed file. |
| S15 | 21 | “The receipt also checks the window.” | 6 | **CHANGES** | [F03](#f03) |
| S16 | 21 | “The issue time must be at the start of the window or after it.” | 14 | **FAITHFUL** | A9 37–38; inclusive lower bound on issue time. |
| S17 | 21 | “The anchor time T must be at the end of the window or before it.” | 15 | **FAITHFUL** | A9 37–38; inclusive upper bound on T. |
| S18 | 26 | “V1 gives the correct verdict when an attacker does one of these things:” | 13 | **FAITHFUL** | A9 40–43, conditional on assumptions; F06. |
| S19 | 28 | “The attacker changes a receipt, removes a part of it, or replaces a part of it.” | 16 | **FAITHFUL** | A9 40; tamper, strip and swap. |
| S20 | 29 | “The attacker makes a false receipt.” | 6 | **FAITHFUL** | A9 40; forge. |
| S21 | 30 | “The attacker uses a true receipt again for different content, or puts a false date on it.” | 17 | **DROPS** | [F04](#f04) |
| S22 | 31 | “The attacker controls the DNS account or the git repository, but cannot sign with the service keys.” | 17 | **DROPS** | [F23](#f23) |
| S23 | 32 | “The attacker steals a key after Bitcoin anchored the receipt.” | 10 | **DROPS** | [F05](#f05) |
| S24 | 33 | “The attacker breaks a signature algorithm after Bitcoin anchored the receipt.” | 11 | **FAITHFUL** | A9 42–43; later algorithm break. |
| S25 | 35 | “These protections are true only if the cryptography, the key rules and Bitcoin work as expected.” | 16 | **DROPS** | [F06](#f06) |
| S26 | 39 | “V1 does not tell you these things:” | 7 | **FAITHFUL** | Boundary-list lead-in. |
| S27 | 41 | “who sent the content;” | 4 | **FAITHFUL** | A9 45; no submitter identification. |
| S28 | 42 | “what the content means, or if it is true;” | 9 | **FAITHFUL** | A9 45 and C1; no meaning or truth claim. |
| S29 | 43 | “if a key was revoked;” | 5 | **FAITHFUL** | A9 45–46; revocation not evaluated. |
| S30 | 44 | “if a key or algorithm was still safe at the time of signing.” | 13 | **FAITHFUL** | A9 45–46; historical key and algorithm safety not evaluated. |
| S31 | 46 | “V1 does not protect against these attackers:” | 7 | **FAITHFUL** | Excluded-attacker list lead-in. |
| S32 | 48 | “An attacker who can sign with both keys during the window.” | 11 | **FAITHFUL** | A9 47–49; capability for both required keys. |
| S33 | 48 | “A person who controls the AWS account can do this.” | 10 | **FAITHFUL** | A9 48–49 and C3; the service’s issuing AWS account, in context. |
| S34 | 49 | “An attacker who controls all of the author's accounts at the same time.” | 13 | **CHANGES** | [F07](#f07) |
| S35 | 50 | “An attacker who breaks SHA-256, OpenTimestamps or more than six Bitcoin blocks.” | 12 | **DROPS** | [F08](#f08) |
| S36 | 51 | “An attacker who replaces the verifier or its trust file.” | 10 | **FAITHFUL** | A9 51–52; verifier and distributed trust compromise. |
| S37 | 53 | “One person controls both keys.” | 5 | **FAITHFUL** | A9 52; one controller, here the author. |
| S38 | 53 | “The two keys are in different technical systems, but not under different control.” | 13 | **FAITHFUL** | C3; separate technical domains and shared control; further omissions in F12. |
| S39 | 57 | “The verifier finds the exact signed parts of the receipt.” | 10 | **FAITHFUL** | C1; exact signed parts; vocabulary still needs repair. |
| S40 | 57 | “Both keys signed the same content.” | 6 | **DROPS** | [F09](#f09) |
| S41 | 58 | “The receipt ID has only one possible meaning.” | 8 | **CHANGES** | [F10](#f10) |
| S42 | 59 | “*Not claimed:* anything about the meaning or truth of the content.” | 9 | **FAITHFUL** | C1; content meaning and truth excluded. |
| S43 | 61 | “The service received the content at some time.” | 8 | **DROPS** | [F11](#f11) |
| S44 | 62 | “*Not claimed:* who sent it.” | 3 | **FAITHFUL** | C2; no submitter claim. |
| S45 | 62 | “*Not claimed:* that a second use of the receipt is correct for a new transaction.” | 13 | **FAITHFUL** | C2; no guarantee of transaction suitability on replay. |
| S46 | 64 | “Each signature is correct for its signed part.” | 8 | **FAITHFUL** | C3; each required service signature over its designated frame. |
| S47 | 64 | “If a signature is missing, removed or replaced, the receipt is INVALID.” | 12 | **FAITHFUL** | C3; failed required service-signature check. This does not mean every missing evidence item is INVALID (d2). |
| S48 | 66 | “*Not claimed:* that two people must agree before the service signs.” | 9 | **DROPS** | [F12](#f12) |
| S49 | 66 | “One person controls both keys.” | 5 | **FAITHFUL** | C3; single controller. |
| S50 | 66 | “A person who controls the AWS account can make both keys sign.” | 12 | **FAITHFUL** | C3; the service’s issuing AWS account confers capability for both. |
| S51 | 69 | “Two authority records said that the keys belong to wamason.com, for the window.” | 13 | **DROPS** | [F02](#f02) |
| S52 | 69 | “One record is in DNS, which DNSSEC signs.” | 8 | **CHANGES** | [F13](#f13) |
| S53 | 70 | “The other record is in a git repository, which the repository key signs.” | 13 | **CHANGES** | [F14](#f14) |
| S54 | 70 | “Bitcoin anchored the git record at least six blocks before it anchored the receipt.” | 14 | **DROPS** | [F15](#f15) |
| S55 | 72 | “*Not claimed:* revocation checks.” | 2 | **FAITHFUL** | C4; revocation not evaluated. |
| S56 | 72 | “*Not claimed:* that the git record was public.” | 6 | **FAITHFUL** | C4; no proof of public publication. The issuer’s publication duty remains (A9 495–500). |
| S57 | 72 | “*Not claimed:* an order in clock time.” | 5 | **FAITHFUL** | C4; no UTC-order claim. |
| S58 | 73 | “The order is in Bitcoin blocks.” | 6 | **FAITHFUL** | C4; block-height order. |
| S59 | 75 | “The signed parts and their exact signatures existed at time T or before T.” | 14 | **FAITHFUL** | C5; exact signatures included; source clock ambiguity A01 remains. |
| S60 | 75 | “T comes from the Bitcoin attestation with the lowest block number in the receipt.” | 14 | **DROPS** | [F16](#f16) |
| S61 | 76 | “Six blocks confirm it.” | 4 | **DROPS** | [F17](#f17) |
| S62 | 77 | “*Not claimed:* an earliest possible time.” | 4 | **FAITHFUL** | C5; no lower existence-time bound. |
| S63 | 77 | “*Not claimed:* that this receipt came before a different receipt.” | 8 | **FAITHFUL** | C5; no priority claim. |
| S64 | 77 | “A Bitcoin block time is close to the real time, but it is not exact.” | 15 | **ADDS** | [F18](#f18) |
| S65 | 80 | “The verdict depends only on the receipt, the verifier and its trust file.” | 13 | **FAITHFUL** | C6; pure function of receipt, verifier and distributed trust file. |
| S66 | 81 | “*Not claimed:* that the holder keeps the receipt.” | 6 | **FAITHFUL** | C6; custody is not a verifier guarantee. |
| S67 | 81 | “That is the holder's task.” | 5 | **FAITHFUL** | C6; holder’s custody responsibility. |
| S68 | 81 | “If T is after the last Bitcoin block in the trust file, the verdict is CANNOT VERIFY.” | 17 | **CHANGES** | [F19](#f19) |
| S69 | 84 | “The verdict has a type.” | 5 | **FAITHFUL** | C7; typed verdict. |
| S70 | 84 | “The verdict also says that V1 did not check revocation or the historical safety of the keys.” | 17 | **DROPS** | [F20](#f20) |
| S71 | 85 | “A person who is not an expert must not accept a bad receipt as good.” | 15 | **CHANGES** | [F21](#f21) |
| S72 | 85 | “The relying-party test on 4 December 2026 checks this.” | 9 | **FAITHFUL** | C7 and A9 215–216; scheduled test, read with F21. |
| S73 | 86 | “That test has not occurred yet.” | 6 | **FAITHFUL** | C7; criterion not established; stated test date is future at review. |
| S74 | 90 | “Amendment 9: opening sections "The claim", "The adversary", "The boundaries"; table A9.1 rows C1 to C7.” | 16 | **FAITHFUL** | Reference locator. |
| S75 | 94 | “C2, C6 and C7 lose some detail in this pilot.” | 10 | **FAITHFUL** | Editorial diagnosis; actual missing details identified below. |
| S76 | 94 | “Examples: the "existential" wording in C2; the pinned-header rule in C6; the missing-capture negative control in C7.” | 17 | **FAITHFUL** | Editorial examples. “At some time” preserves the existential quantifier; F11 concerns the issuance event. |
| S77 | 95 | “The review must decide if each loss changes a meaning.” | 10 | **FAITHFUL** | Editorial review instruction. |
| S78 | 96 | “In section 2, "uses a true receipt again" renders "replays" and "reattributes".” | 12 | **CHANGES** | [F22](#f22) |
| S79 | 96 | “Check that this is the same meaning.” | 7 | **FAITHFUL** | Editorial review instruction. |

Primary decisions: 55 FAITHFUL, 1 ADDS, 15 DROPS, 8 CHANGES.

## Findings for non-FAITHFUL sentences

### F01

**S07 — DROPS the condition on the four checks.** Pilot: “A receipt proves four things:”. A9 32–34: “Provided the service's signing capability was not misused within the key's window, a V1 receipt lets anyone, with no network and no help from Tessera, check four things”. The pilot's later statement about cryptography does not restore the condition on misuse. “Proves” also conceals the distinction between a conditional claim and an unconditional fact.

Proposed plain text **[D]**:

```text
A receipt supports these four checks under both conditions:
- The registered cryptographic and key-use assumptions hold.
- Nobody misused the service's signing capability within the window.
```

### F02

**S10 and S51 — DROPS the evidence-time qualification.** Pilot: “Two authority records said that these keys belong to wamason.com, for a stated window.” / “Two authority records said that the keys belong to wamason.com, for the window.” C4: “authenticated K for D, with the issuance window, at their evidence times.” These are historical assertions evaluated at particular evidence times, not a claim of continuing authority. The later descriptions never restore those evaluation times.

Proposed plain text **[D]**:

```text
Both authority records say the two keys belong to wamason.com.
They give the window in which those keys can issue receipts.
The verifier must check each authority record at that record's evidence time.
```

F13 and F14 specify the different checks for the two records.

### F03

**S15 — CHANGES who checks the window.** Pilot: “The receipt also checks the window.” A9 419–421: “Verifier rule (C4). A receipt is `INVALID / ISSUANCE_WINDOW` unless” the two stated comparisons hold. A receipt supplies evidence; the verifier performs the check.

Proposed plain text:

```text
The verifier also checks the window.
```

Keep S16 and S17 as a bulleted list after that sentence. Their two inclusive comparisons are faithful. Do not replace them with “both times must be inside the window”: A9 does not require that.

### F04

**S21 — DROPS ordinary replay and reattribution.** Pilot: “The attacker uses a true receipt again for different content, or puts a false date on it.” A9 40: “replays, reattributes or backdates receipts”. Reuse with different content describes one substitution attempt. It does not cover another presentation of the same receipt and content, or a false claim about which keys or service made it. C2 explicitly leaves transaction suitability unresolved.

Proposed plain text **[D]** (three bullets in the attack list):

```text
- The attacker presents a receipt again.
- The attacker claims that different keys or a different service made the receipt.
- The attacker claims an earlier issue time for a receipt.
```

These protections do not promise transaction-specific replay prevention. Keep C2's transaction non-claim beside them.

### F05

**S23 — DROPS later signing capability without key theft.** Pilot: “The attacker steals a key after Bitcoin anchored the receipt.” A9 42–43: “steals a key, gains signing capability, or breaks a signature algorithm after a receipt was anchored.” S24 covers the algorithm case. A non-exportable key can remain secret while an attacker gains permission to use it (C3; A9 387–388).

Proposed additional bullet **[D]**:

```text
- The attacker gains signing capability after Bitcoin anchors the receipt.
```

Keep the theft and algorithm bullets. Do not equate signing capability with possession of private key bytes.

### F06

**S25 — DROPS the registered nature and specificity of the assumptions.** Pilot: “These protections are true only if the cryptography, the key rules and Bitcoin work as expected.” A9 43: “under the registered cryptographic, key-use and chain assumptions.” “Work as expected” substitutes an unspecified expectation for a registered condition. It can also imply that correct cryptographic calculations alone establish historical key safety, which C7 explicitly does not evaluate.

Proposed plain text **[D]**:

```text
These protections depend on the registered cryptographic, key-use and Bitcoin history assumptions.
```

Put exact source references at the end. The reviewer cannot replace those assumptions with a general assurance.

### F07

**S34 — CHANGES whole operational capture into simultaneous account capture.** Pilot: “An attacker who controls all of the author's accounts at the same time.” A9 49: “whole-author-sphere capture (R-2.15)”. The referenced R-2.15 says “the author's entire operational sphere at issue time”; A1 452–458 makes the same distinction. The sphere includes operational control beyond accounts, and the source names issue time, not any simultaneous compromise at any time.

Proposed plain text **[D]**:

```text
V1 does not protect against capture of the author's whole operational sphere at issue time.
This includes the accounts, devices and signing capability that the author uses for the service.
```

The vocabulary needs an explicit definition of “operational sphere”; “all accounts” is not that definition.

### F08

**S35 — DROPS the git exclusions and obscures the Bitcoin-history exclusion.** Pilot: “An attacker who breaks SHA-256, OpenTimestamps or more than six Bitcoin blocks.” A9 49–51: “breaks of SHA-256, OpenTimestamps, Bitcoin history deeper than k, or, in git's links, a second-preimage break of SHA-1 or attacker influence over committed contents”. Individual blocks are not the object of the stated history-depth limit. Both git exclusions are entirely absent.

Proposed bullets **[D, A]**:

```text
- The attacker breaks SHA-256.
- The attacker breaks OpenTimestamps.
- The attacker changes Bitcoin history deeper than k, where k is six.
- The attacker finds different git bytes with the same SHA-1 hash as given git bytes.
- The attacker influences the contents of a git commit.
```

The SHA-1 sentence describes a second-preimage attack, not merely finding any two colliding objects. Explain the technical names at first use. A03 below identifies the unresolved history-depth counting boundary; the proposed text retains A9's threshold rather than choosing another one.

### F09

**S40 — DROPS common metadata, slot-specific key binding, and the frame distinction.** Pilot: “Both keys signed the same content.” C1: “both bind the same content and common metadata, the designated fingerprint in its slot”; non-claim: “Payload identity is not frame equality.” Equal content alone is a weaker condition. The signed frames contain additional information and need not be identical.

Proposed plain text **[D]**:

```text
Each key signs its own frame.
Both frames must bind the same content and common metadata.
Each frame must name the key fingerprint for its assigned slot.
The frames can differ even when their content matches.
```

Define frame, common metadata, key fingerprint and slot before this use. The last sentence restores C1's otherwise missing non-claim.

### F10

**S41 — CHANGES an unambiguous encoding into a claim about a receipt ID.** Pilot: “The receipt ID has only one possible meaning.” C1: “The receipt-anchor preimage `A_sig` over both frames and both signatures is unambiguous.” The dictionary defines receipt ID as a SHA-256 hash of an undefined “signed core” (Style 34). That is a different object and property. Unique parsing of `A_sig` does not assert unconditional uniqueness of every possible hash preimage, nor the meaning or truth of content.

Proposed plain text **[D]**:

```text
A_sig holds both frames and their exact signatures in a fixed format.
The verifier reads A_sig in only one way.
```

Here `A_sig` is an unchanged technical identifier, explained by the first sentence. Repair the dictionary separately if receipt ID remains in a future pilot. Do not describe `A_sig` as a frame or a hash.

### F11

**S43 — DROPS “at some issuance event,” not the existential quantifier.** Pilot: “The service received the content at some time.” C2: “The content was presented at some issuance event of the V1 service (existential).” “At some time” correctly preserves “there was at least one”; it does not assert a unique event or an earliest time. But ordinary receipt of content by the service, for example before an unsuccessful attempt, is broader than presentation at an issuance event.

Proposed plain text **[D]**:

```text
The service received this content during at least one issuance event.
```

Do not add “this receipt's only issuance event” or “the person holding it submitted it.” Neither follows from C2.

### F12

**S48 — DROPS independent fates and narrows independent approval to two people.** Pilot: “Not claimed: that two people must agree before the service signs.” C3: “V1 claims no separation of control and no independent fates, and no independent approval of content.” S37–S38 and S49 restore shared control and separate technical systems. They do not restore independent-fate or content-approval non-claims. Independent approval is not simply a count of people.

Proposed plain text **[D]**:

```text
One person controls both keys.
The keys use separate technical systems.
V1 does not promise independent control or independent approval of content.
V1 does not promise that the keys fail independently.
```

Also restore the non-exportability distinction as O02. Separate technical systems do not establish independent availability or independent signing fates (A9 393–394).

### F13

**S52 — CHANGES DNSSEC validation into DNSSEC doing the signing, and DROPS its evaluation time.** Pilot: “One record is in DNS, which DNSSEC signs.” C4: “DNSSEC (owner name D, evaluated at the snapshot's own anchored time)”. DNSSEC is the mechanism used to authenticate the DNS evidence; the pilot makes the protocol the signer of DNS itself. It also omits the required owner-name check and the snapshot's independent evaluation time.

Proposed plain text **[D, A]**:

```text
The verifier checks the DNS authority record with DNSSEC.
It must check the required DNS owner name for wamason.com.
It must check DNSSEC at the DNS snapshot's own anchor time.
```

Explain DNSSEC first. Do not substitute the receipt's T for the snapshot's time. A06 addresses the source's shorthand “owner name D.”

### F14

**S53 — CHANGES the signed object and DROPS full-path verification.** Pilot: “The other record is in a git repository, which the repository key signs.” C4: “the anchored git key assertion (full commit→tree→blob path)”. The opening identifies “a signed, timestamped git commit” (A9 35). A9 297–299 specifies “the signed commit's object id” and verification of `gpgsig` and the path. Signing an entire repository is not the stated mechanism; merely signing some record is insufficient.

Proposed plain text **[D]**:

```text
The repository key signs a git commit.
The verifier must check that signature.
It must check the complete commit-to-tree-to-blob path to the authority record.
OpenTimestamps anchors the signed commit's object ID in Bitcoin.
```

Define repository key, commit, tree, blob and object ID. The dictionary's service-only definition of “key” currently cannot cover the repository key without qualification.

### F15

**S54 — DROPS selection of the two anchors used for the ordering test.** Pilot: “Bitcoin anchored the git record at least six blocks before it anchored the receipt.” C4: “the git assertion's selected anchor height plus 5 is lower than the receipt's selected anchor height”. A comparison between any convenient pair of anchors is not the registered comparison. The omitted “selected” matters when a proof contains multiple attestations.

Proposed plain text **[D]**:

```text
The verifier selects a Bitcoin block for the git record and another for the receipt.
The selected git block number plus five must be lower than the selected receipt block number.
```

There is **no arithmetic off-by-one error** in the pilot's “at least six blocks before” by itself: integer heights satisfying `g + 5 < r` have `r − g ≥ 6`. The sixth confirmation of the git anchor is at `g + 5`; the receipt anchor must follow it. This is distinct from source issue A03 about reorganization depth.

### F16

**S60 — DROPS verified proof scope and presentation-sensitive selection.** Pilot: “T comes from the Bitcoin attestation with the lowest block number in the receipt.” C5: “the verified attestation at the lowest block height in the presented OTS proof (both T and its confirmations come from that attestation”; its non-claim is “Presentation-sensitive T.” A low number merely appearing in a receipt is not verified evidence. The same selected proof path supplies T and confirmations, and a different presented proof can give a different T for the same signed receipt.

Proposed plain text **[D, A]**:

```text
The verifier selects the verified Bitcoin block with the lowest number in the presented OpenTimestamps proof.
T comes from that block.
The verifier takes the confirmation count from that same proof path.
Different proofs for one receipt can give different values of T.
```

A05 below identifies a source ambiguity about selecting evidence that is not covered by pins; this replacement does not silently resolve it.

### F17

**S61 — DROPS the three time comparisons.** Pilot: “Six blocks confirm it.” C5: “the three-conjunct predicate holds at k = 6.” The pilot supplies only the count, without even stating the inclusive counting convention. A9 510 preserves A2.1's predicate. A2.2, lines 222–224, gives:

> `declared_issue_time − ε ≤ anchor_time`
>
> `anchor_time ≤ declared_issue_time + δ`
>
> `confirmed_at ≤ declared_issue_time + δ`

A9 223 fixes ε = 24 h and δ = 72 h; A2.1 80–85 counts the anchor block as confirmation one and identifies the sixth block. Six confirmations alone do not establish those time comparisons.

Proposed plain text **[D]**:

```text
Six confirmations include the block that contains the receipt anchor.
The sixth block has the selected block number plus five.
The following checks must all pass:
- The selected proof must give at least six confirmations.
- T must be at least the issue time minus 24 hours.
- T must be at most the issue time plus 72 hours.
- The sixth block's time must be at most the issue time plus 72 hours.
```

The first bullet is the count condition; the remaining three are the three time comparisons. Keep these separate from the two issuance-window comparisons. These are Bitcoin time values, not a promise of real-time latency.

### F18

**S64 — ADDS an assurance of closeness to real time.** Pilot: “A Bitcoin block time is close to the real time, but it is not exact.” C5: “Header times are chain-time proxies.” A9 444–446: “Translating this into a finite UTC cutoff requires an additional, explicit backward-skew assumption that V1 does not establish: A2.1 registers no finite bound on B − C”. The pilot turns a proxy with an explicit unbounded backward residual into a closeness promise.

Proposed plain text **[D]**:

```text
A Bitcoin block gives a chain-time value.
V1 does not promise that this time is close to real time.
```

A01 addresses the source's own “existed no later than T” wording. Do not repair that source ambiguity by inventing a numeric clock-error bound.

### F19

**S68 — CHANGES block-height coverage into an ambiguous time comparison and DROPS the all-header rule.** Pilot: “If T is after the last Bitcoin block in the trust file, the verdict is CANNOT VERIFY.” C6: “A selected anchor (C5) beyond the newest pin is `UNVERIFIABLE`. Every supplied header must be pinned.” T is a header time, not a block number; C5 itself says header times are not monotone. The selected anchor can be within the covered range while another supplied header is outside it.

Proposed plain text **[D]**:

```text
Unless another failed check requires INVALID, the verifier must give CANNOT VERIFY under either condition:
- The selected anchor's block number exceeds the newest pin's block number.
- Any supplied header lacks a pin.
```

Define header and pin. A9 287 retains A4.2 verdict precedence; missing coverage does not override another established failure. O04 restores the other C6 non-claims and the special rule for an unselected attestation without headers.

### F20

**S70 — DROPS algorithm safety and separate standing reporting.** Pilot: “The verdict also says that V1 did not check revocation or the historical safety of the keys.” C7: “reports `revocation: NOT_EVALUATED`, `historical_security: NOT_EVALUATED` and standing separately”; non-claim: “Revocation, historical security and standing are not claimed.” Historical security concerns algorithms as well as keys (A9 259–260). The earlier boundary on algorithms does not restore this reporting requirement. Standing vanishes entirely.

Proposed plain text **[D]**:

```text
The verdict reports these results separately:
- revocation: NOT_EVALUATED means V1 did not check revocation.
- historical_security: NOT_EVALUATED means V1 did not check historical algorithm or key safety.
- standing: ABSENT/NOT_ISSUED_IN_PROFILE means V1 did not issue standing evidence.
```

The exact standing value comes from A9 171–173. These unchanged technical field names need explanations and dictionary support. O01 also restores the scope exclusions.

### F21

**S71 — CHANGES a bounded, unestablished acceptance criterion into a general rule about bad receipts.** Pilot: “A person who is not an expert must not accept a bad receipt as good.” C7: “a non-expert makes no unsafe accept on the mapping (4 Dec criterion, not yet established).” A9 118–122 limits the evidence to one independent human tester and expressly says it is “not as a result about relying parties in general.” An unsafe accept also includes relying on a valid receipt for something it does not establish: e/e′ need non-revocation, f does not establish submitter identity, and i′ can have a valid Tessera receipt with an invalid party signature (A9 183–187). “Bad receipt” loses these distinctions. S73 preserves the fact that testing is unfinished, but does not repair the scope of the criterion.

Proposed plain text **[D]**:

```text
The 4 December 2026 test checks one person's decisions on the registered cases.
The person must meet the registered independence conditions.
V1's documentation must let that person avoid every unsafe accept in those cases.
The test permits false rejects only for cases d2 and h.
The test does not establish that all people can make safe decisions.
That result is not yet established.
```

Explain an unsafe accept as reliance on a claim that the evidence does not establish. Keep the full registered mapping and independence conditions in the references. This correction does not announce that V1 has passed the test.

### F22

**S78 — CHANGES the relation between replay and reattribution in an editorial claim.** Pilot: “In section 2, ‘uses a true receipt again’ renders ‘replays’ and ‘reattributes’.” (The original uses double quotation marks.) A9 40 lists “replays, reattributes” separately. Re-presentation and false attribution are different actions; neither phrase alone expresses both. This is a claim about the translation, not a new V1 rule, but it is still incorrect. See F04 for the substantive repair.

Proposed owner note **[D]**:

```text
The replay bullet describes another presentation of a receipt.
The reattribution bullet describes a false claim about its keys or service.
```

Put any section locator in the references, rather than this note's body.

### F23

**S22 — DROPS disclosure of authority credentials that does not amount to account or repository control.** Pilot: “The attacker controls the DNS account or the git repository, but cannot sign with the service keys.” A9 41–42: “captures authority-channel credentials while signing capability stays uncompromised”. The trust-boundary explanation names “the DNS credential” and “the repository key” separately (A9 327–331). Possession of the repository signing key is not the same thing as control of the hosted repository, particularly when C4 does not prove public publication. The plain wording must include that credential exposure, rather than replace it with host or account control.

Proposed plain text **[D]**:

```text
The attacker obtains authority-record credentials but cannot use either service key.
This includes the repository signing key.
```

Define authority-record credentials and the repository key. A04 separately asks which receipt properties A9 protects after that capture; preserving the source's credential scope does not resolve that question.

## Source clauses with no pilot sentence

These are additional DROPS findings. Each quotes the nearest pilot text to show the omission in context. A sentence ledger alone cannot detect a whole missing sentence.

### O01 — capabilities excluded from V1

Pilot boundary list: “V1 does not tell you these things:” followed by sender, content meaning, revocation and historical safety. A9 46–47: “It offers no standing, renewal, wrappers or degraded verification”. None of these four exclusions appears elsewhere in the pilot. The lack of lower time bounds and priority *is* restored in C5, so those are not counted as missing.

Proposed addition **[D]**:

```text
V1 offers none of these features:
- standing;
- renewal;
- wrappers;
- degraded verification.
```

The current dictionary has no entries for these concepts; silently omitting them is not a dictionary-compliance strategy.

### O02 — a non-exportable key can still sign for an attacker

Pilot C3 ends: “A person who controls the AWS account can make both keys sign.” C3 continues in A9: “the non-exportable key prevents key export, not misuse.” This matters because the source distinguishes stealing key material from gaining signing capability. The pilot's explanation otherwise invites the wrong inference that hardware protection prevents this attack.

Proposed addition **[D]**:

```text
Hardware prevents export of the protected key.
It does not prevent an attacker from using the permitted signing path.
```

This describes the source's non-exportable key, not a universal property of every kind of hardware.

### O03 — what authority evidence does not establish

Pilot C4 non-claims: “Not claimed: revocation checks. Not claimed: that the git record was public. Not claimed: an order in clock time.” C4 also says: “The verifier fixes the required set”; “Neither channel commits to any receipt”; and “DNSSEC evidence establishes no publication before issue.” All three are missing. Historical authority evidence is not authority endorsement of this individual receipt. DNS evidence does not inherit the git evidence's pre-commitment order.

Proposed additions **[D]**:

```text
The verifier fixes the required set of authority records.
The receipt cannot choose that set.
Neither authority record commits to an individual receipt.
The DNS evidence does not establish that the DNS record was public before issue.
```

C4's git public-publication non-claim remains. A9 495–500 separately retains public publication as an issuer duty that the verifier cannot prove.

### O04 — C6's remaining limits and ignored evidence

Pilot C6: “The verdict depends only on the receipt, the verifier and its trust file.” Its remaining text covers custody and “If T is after the last Bitcoin block…”. C6 also says: “Dead-project reconstruction not demonstrated” and “An unselected attestation without its headers supplies no fact and is not a failure”. Both are missing. F19 separately restores the all-supplied-header rule.

Proposed additions **[D, A]**:

```text
V1 has not demonstrated reconstruction after the project ends.
The verifier must ignore an unselected attestation that supplies no headers.
That attestation establishes nothing and does not cause a failed check.
```

Here “attestation” is specifically an OpenTimestamps proof object, not a Tessera receipt. It needs distinct vocabulary; applying the dictionary's receipt synonym mechanically would change the object. A05 addresses the selection ambiguity in A9.

### O05 — C7's assigned build evidence

Pilot C7 mentions only: “The relying-party test on 4 December 2026 checks this. That test has not occurred yet.” C7 also says: “Assigned build evidence includes A9.4's missing-capture negative control.” A9 282–283 specifies: “for an otherwise valid, fully performable bundle where missing status capture is the sole difference, a companion returning `INVALID` or `UNVERIFIABLE` must go red.” That is separate build evidence, not the human comprehension test. No pilot sentence states it.

Proposed addition **[D]**:

```text
The build test must include a negative control.
The control uses a receipt with these properties:
- All V1 checks can run and pass.
- Only status capture is missing.
A companion verifier must fail the test under either condition:
- It gives INVALID only because status capture is missing.
- It gives CANNOT VERIFY only because status capture is missing.
```

Define status capture as the historical status evidence that V1 does not require, and define companion verifier and negative control. This does not allow a missing signature, required authority record or pinned header to pass.

## Findings about A9 itself for the next amendment

These are source findings exposed by the rendering, separate from translation defects and dictionary defects. Some are ambiguities requiring clarification, not demonstrated failures of the implementation or formal models. The pilot must not settle them silently. References outside the requested paragraphs identify rules A9 itself invokes; they do not substitute another draft for A9.

### A01 — “existed no later than T” needs an explicit clock meaning

A9 36–37: “the bytes and both signatures existed no later than a time T fixed by Bitcoin.” C5 repeats “existed no later than T” and also says “Header times are chain-time proxies.” A9 444–446 says a finite UTC cutoff needs an additional backward-skew assumption and “A2.1 registers no finite bound on B − C”.

Those sentences do not support the ordinary-language interpretation that the bytes existed before the real-world instant denoted by T. An inclusion block can carry a backward-skewed header time. The preimage must exist before inclusion; it need not exist before that header's nominal UTC reading. Merely saying “not exact” or “close” does not solve this.

**Next amendment finding:** explicitly distinguish existence before inclusion in the selected block from an upper bound in real-world time. State which meaning the claim adopts. If it adopts a UTC bound, register the additional assumption and evidence; otherwise qualify the opening and C5. This is a source-level tension, not only the pilot's unsupported closeness assertion. S11 and S59 reproduce the source faithfully but inherit it.

### A02 — “inside the window” overstates the actual two comparisons

A9 441: “Signing capability mints only inside the window, in chain time.” A9 419–421 specifies only declared issue time ≥ not-before and T ≤ not-after, and explicitly says “T itself is not compared with not-before.” A9's opening and A9.1 repeat those asymmetric comparisons. A9 407 calls the values an “Issuance window”.

These are not a rule that both time values, or the actual act of signing, lie inside the interval. Two numerical examples expose the distinction under A2's preserved tolerances:

| Example | Declared issue time | T | Designated sixth-block time | Why the stated comparisons permit it |
|---|---|---|---|---|
| Before-start T | window start | start minus 1 hour | start plus 1 hour | T ≥ declared minus 24 hours; all upper time bounds hold. T need not reach the window start. |
| After-end declared time | window end plus 1 hour | window end | end plus 1 hour | Declared time meets the lower window bound, T meets the upper bound, and all three A2 comparisons can hold. |

These are arithmetic witnesses to what the verifier comparisons establish, not executed receipt vectors or a claim that an honest issuer necessarily ships them. The issuer's stop duty does not create an additional verifier comparison.

**Next amendment finding:** narrow the guarantee's heading and any literal “allowed to sign during” description to the actual comparisons, or explicitly change the registered checks. Preserve the inclusive endpoints and chain-time limitation. Do not let the plain dictionary's “window” definition decide this policy question.

### A03 — the history-depth exclusion needs an explicit counting convention

A9 49–50 excludes “Bitcoin history deeper than k”; C5 says “Reorganization deeper than k is a residual.” A9 223 sets k = 6. But A9 105 imports “k = 6 under `DepthK = k − 1`”, and the A2.1 convention counts the inclusion block as confirmation one. At six confirmations, five blocks follow the anchor block.

If a reorganization's depth means the number of old tip blocks removed, replacing six blocks at that point can remove the anchor. “Deeper than six” excludes seven and above, leaving the equality case apparently covered. If the source uses another depth convention, it must state it. The model's `DepthK` guard is not itself a definition of the ordinary phrase “history deeper than k”.

**Next amendment finding:** define reorganization depth and state the exact excluded equality boundary relative to confirmation count. Check the intended assumption against the model convention. This is a counting ambiguity with a concrete boundary case, not a claim that a model run failed. It is distinct from the correctly translated C4 six-block gap.

### A04 — authority capture needs a stated property scope

A9 40–43 promises that verdicts hold against anyone who “captures authority-channel credentials while signing capability stays uncompromised (A8.3's sense of capture)”. A8.3 72–76 defines credential disclosure with honest signing keys secret, but bounds its tested property to preventing reattribution of honest frames, alteration of honest signer sets, and carrying honest signatures onto other bytes or keys. A8.5 123–124 explicitly puts “preventing a captured or merged authority from issuing new attestations” out of scope.

A9's opening can read as protecting the *presentation-to-the-service claim for arbitrary new receipts* under credential capture. That is stronger than protecting an already signed receipt against reattribution. “Signing capability” also needs an object: capability for the original service keys, or for any keys a captured authority can name? Whole-author-sphere capture is excluded, but compromising authority credentials does not necessarily compromise the author's entire operational sphere.

**Next amendment finding:** state whether the capture claim concerns existing honest receipts, new receipts, or both, and which credentials and signing keys it quantifies over. If new receipts are included, name the invariant that prevents attacker-selected key assertions from establishing service presentation. This is a scope ambiguity, not a demonstrated forged-receipt result. The pilot's short account-control bullet hides it rather than resolving it.

### A05 — “verified” selection and unpinned evidence need an order of evaluation

C5 selects “the verified attestation at the lowest block height in the presented OTS proof”. C6 says “A selected anchor (C5) beyond the newest pin is `UNVERIFIABLE`”, “Every supplied header must be pinned”, and “An unselected attestation without its headers supplies no fact and is not a failure”.

The word “verified” can mean verification including pin coverage, or verification of the proof operations before that coverage check. The first reading appears to prevent an uncovered anchor from becoming selected at all; the second allows selection followed by CANNOT VERIFY. Likewise, a bare lower-height attestation without headers cannot simply win selection by announcing a low height, but the source does not make that candidate rule explicit in these clauses.

**Next amendment finding:** state the selection stages: which candidates can supply a verified height, when coverage is checked, what makes an anchor selected, and when a headerless candidate is ignored. Include a covered path plus a lower purported/headerless path, and an anchor beyond the pins. This identifies ambiguity in A9's abbreviated rule; it does not assert that the implementation specification lacks an algorithm.

### A06 — “owner name D” can identify the wrong DNS name

C4 says “DNSSEC (owner name D …)”; A9 68 identifies D as `wamason.com`. The encoding A9 adopts (A9 149) instead uses `_tessera-v1.wamason.com` as the required TXT owner. `formal/p8/ENCODING-V1.md` 634–635 requires exact matching of that prefixed owner. A9 414–415 rejects a substituted per-key owner name.

In ordinary DNS language, the owner name is the complete name owning the record. A literal rendering of “owner name D” would therefore check `wamason.com`, not the required prefixed name. “For domain D” can be harmless shorthand for the domain's authority record, but it is not the same as specifying the owner name.

**Next amendment finding:** say “the fixed authority-record owner for D” and name the exact construction, or explicitly state the intended name. F13's proposed text avoids choosing a different owner and refers to the required name.

### Apparent source issues that are already resolved, or belong elsewhere

- **C2's existential presentation:** A9 is explicit. “At some time” preserves the existential quantifier. The pilot loses the issuance event, not the quantifier. No amendment finding about uniqueness is justified.
- **Public publication:** C4's non-claim and A9 495–500's public-publication duty are compatible: the issuer must publish, but the verifier does not prove publication. The pilot must not remove that distinction.
- **Current key safety versus old receipts:** A9 433–440 expressly separates survival after later compromise from unevaluated historical authenticity assumptions. It does not establish past safety merely because the signatures verify.
- **C7's achievement status:** “4 Dec criterion, not yet established” is explicit. The pilot's universal instruction is a translation defect; A9 does not claim a completed general usability result.
- **Six-block git gap:** `g + 5 < r` means at least six height increments. This is not a source contradiction.
- **Stale PROPOSED header:** the signing-act rule and history resolve adoption for this review. Record it as a provenance presentation issue, not evidence that A9 is unsigned.
- **Google custody, receipt ID, and the meaning of INVALID:** the dictionary defects below are not contradictions in A9. A9 explicitly permits custody alternatives and a classical fallback.

## Style review

### Length, paragraphs and one idea

**Sentence length: PASS.** All 79 units fit the applicable limits: no more than 17 words under the stated counting method, including the “Not claimed:” labels when present. The two explicit review instructions S77 and S79 fit 20 words, as do the “must” sentences. No length violation is hidden by a wrapped line. Metadata, fragments, references and notes were also checked.

**Paragraphs: revise C4.** Pilot 69–73 is one Markdown paragraph. It has eight period-terminated units after the heading label, including three non-claim fragments. If fragments count as sentences, it exceeds six. Counting only full grammatical sentences gives five; Style does not specify how fragments count. Split the claim, checks and non-claims into separate paragraphs or lists so neither reading exceeds six. C5 has six such units; the other paragraphs fit. Heading labels are not counted as sentences.

**One idea: revise where lists carry the distinction.** S21 combines replay/substitution and backdating; S35 combines several unrelated security failures. The proposed separate bullets preserve their distinct meanings. C1 and C7 also benefit from separate sentences for each check or report field. Parallel wording alone is not a substitute for preserving separate rules.

### Active voice and clear actors

| Pilot location | Wording | Assessment and proposed form |
|---|---|---|
| 43 / S29 | “if a key was revoked” | Passive with no actor. Use “V1 does not check key revocation.” [D] This preserves *not evaluated*, rather than promising that every revocation has an identifiable actor in the receipt. |
| 64–65 / S47 | “If a signature is missing, removed or replaced” | “Removed” and “replaced” have an omitted actor. Put conditions in a list: “A required signature is missing”; “An attacker removes a required signature”; “An attacker replaces a required signature.” [D] Keep the required service-signature scope. |
| 59; 62; 66; 72–73; 77; 81 | Repeated “Not claimed:” fragments | Reduced passive wording with no actor. Use “V1 does not establish …” or “V1 does not promise …”, with the actual non-claim as the object. For public publication: “The verifier does not establish that the git commit was public.” [D] |
| 21 / S15 | “The receipt also checks the window” | Grammatically active but the wrong actor; use F03. |
| 70 / S52–S53 | “DNSSEC signs”; “the repository key signs” the repository | Active grammar does not make the actor/object technically correct; use F13 and F14. |
| 5 / S05 | “A faithfulness review must occur” | Active, but does not name the reviewer. Clearer: “A reviewer must compare this text with Amendment 9 before anyone relies on it.” |

“The receipt is INVALID,” “the protections are true,” “the content is true,” “keys are in different technical systems,” and “the time is not exact” are stative constructions, not passive voice. Do not fail them merely for containing “is,” “are,” or “was.”

### Dictionary-only project vocabulary: FAIL

Style 14 limits **project ideas** to the dictionary. It does not restrict ordinary English grammar to a 19-entry word list. The following project vocabulary lacks an entry, uses a forbidden synonym, or needs a narrower definition. Technical proper names are allowed by rule 6, subject to first-use explanation; that exception does not approve every generic security term.

| Pilot occurrence | Problem |
|---|---|
| 18, heading C6 | “without Tessera” uses “Tessera” alone where the dictionary requires “service”. The introductory proper name “Tessera V1” at 9 is appropriate. |
| 57, 64, 75 | “signed parts” has no dictionary meaning for a frame. It must distinguish the content, each frame, both signatures, and the anchor encoding. |
| 58 | “receipt ID” is approved vocabulary, but the pilot uses it for C1's different property. Its definition's “signed core” is undefined. |
| 31, 48–51, 66–71 | Account-control, repository-control, repository key, git record and git repository concepts lack entries. “Key” is defined only as a private service key, not a repository or DNS authority key. |
| 33, 35, 44, 85 | Signature algorithm, cryptography, key rules, historical safety and revocation/revoked lack entries. These are substantive conditions, not interchangeable ordinary adjectives. |
| 62 | Transaction and replay suitability lack entries. “Second use” describes replay but does not define its limits. |
| 75–78, 81–82 | Bitcoin block, block number, confirmation, proof and pin coverage need defined meanings. “Attestation” at 76 is also a forbidden receipt synonym under a literal reading of the dictionary. In context it means an OTS object, so replacing it with “receipt” is wrong. |
| 81 | Holder is an undefined custody role. Use “the person who keeps the receipt,” or approve the role. |
| 84–86 | Verdict type, historical safety, relying-party test and “bad receipt” are not defined. The last phrase also confuses an invalid receipt with unsafe reliance on a valid one. |
| 94–96 | The editorial notes use existential, pinned-header, missing-capture negative control, replay and reattribute terminology without dictionary entries. Keeping them internal does not make the entire pilot dictionary-only. |

The absence of “should”, “may” and “shall” does not cure these vocabulary failures.

**Proposed dictionary work, confined to this review:**

- Add **frame**: the exact bytes a particular service key signs. Explain that it contains content and common metadata, with a slot-specific fingerprint.
- Add **common metadata**, **key fingerprint**, **slot**, **A_sig** and **receipt anchor**. Keep “content” for customer bytes. Do not use “signed part” as an undefined substitute.
- Repair **receipt ID**: if retained, name the exact `SHA256(A_sig)` object and distinguish it from injective parsing of `A_sig`. A9's adopted encoding defines that anchor digest; neither “signed core” nor content alone is an adequate definition.
- Repair **anchor time**: do not say the *whole receipt* existed at T. The dictionary defines receipt as all returned files, while C5 bounds the frames and exact signatures. Proof outputs and confirmation evidence are outside `A_sig` (A9 290–296; ENCODING-V1 402–405). Resolve source issue A01 before promising a real-world time bound.
- Repair **window**: describe the actual declared-time lower bound and selected-T upper bound. Do not imply that V1 measures the real signing instant or compares T to both endpoints. A02 remains an amendment finding.
- Add **signing capability**, **non-exportable**, **operational sphere**, **issuance event**, **signature algorithm**, **cryptographic assumption**, **key-use assumption**, **history assumption**, **revocation**, **historical security**, and **status capture**. Use the exact source meanings; possession of key bytes and permission to sign must remain distinct.
- Add role-qualified **repository key**, **DNS root key**, and the release-authentication key if mentioned. The service-only “key” definition cannot serve all those roles unchanged.
- Add **DNS snapshot**, **evidence time**, **DNS owner name**, and the git objects **commit**, **tree**, **blob**, **object ID**. Explain the complete path to an authority record.
- Add **Bitcoin block**, **block number**, **header**, **pin**, **confirmation**, **OpenTimestamps proof**, **proof path**, and a term for its Bitcoin attestation. The last term must not be a synonym for the Tessera receipt.
- Add **standing**, **renewal**, **wrapper** and **degraded verification** before restoring O01. Define standing from the governing standing rules, not as mere key safety or revocation. Likewise, renewal is preservation with later evidence; a wrapper is an outer verification layer; degraded verification waives specified checks. These require their registered definitions before publication.
- Add **registered mapping**, **unsafe accept**, **false reject**, **independence conditions**, **negative control**, **companion verifier**, and a defined term for the person using the verifier. An unsafe accept concerns an unsupported relying decision, including decisions involving otherwise VALID receipts.
- Narrow the definitions of **VALID** and **INVALID** to V1's registered checks. “All checks passed” must not imply evaluated revocation, historical security, standing, submitter identity or content truth. An INVALID result is not evidence that customer content itself is false. A later presented proof can also fail the window check for an otherwise unchanged signed receipt (A9 425–426).
- Make **AWS key** and **Google key** definitions conditional on the chosen branch and dated custody choice. A9 351–374 has an ML-DSA hybrid and a P-256 fallback; A9 375–381 permits a hardware token or another provider's HSM. A9 does not universally require Google custody. The pilot does not currently use “Google key”; this is a dictionary/source mismatch, not a pilot sentence defect.

These are proposals, not approved vocabulary. Accordingly, replacements marked [D] pass the structural rules but still need dictionary work. Claiming that they already meet the current dictionary would repeat the pilot's central problem: hiding a missing prerequisite.

### Technical names and first-use explanations: FAIL

- **wamason.com**, first at 9: identify it as the service's own domain name, not merely a customer label.
- **Bitcoin**, first at 16: explain that it supplies the chain evidence and the selected block's time. “Bitcoin fixes T” does not explain the system or its clock limitation.
- **DNS** and **git**, first at 31: explain their roles as the two authority-record systems before using account/repository compromise in the adversary list.
- **AWS**, first at 48: expand Amazon Web Services and identify the issuing account. The dictionary's separate “AWS key” entry is not an explanation of this account.
- **SHA-256** and **OpenTimestamps**, first at 50: explain the hash function and Bitcoin anchoring proof system. These are allowed unchanged names, not dictionary violations merely because they are proper technical names.
- **DNSSEC**, first at 70: expand Domain Name System Security Extensions and explain that it authenticates signed DNS records. “DNSSEC signs” supplies an inaccurate explanation.

The replacement text also introduces unchanged technical identifiers and git objects; define them before their first use as specified above. A reference to Style does not satisfy “Explain each one when you first use it” inside this pilot.

### Modals, lists, references and idioms

**Forbidden modals: PASS.** Case-insensitive whole-word inspection finds no “should”, “may” or “shall” in the pilot. Its uses of “must” and “can” are compatible with Style's modal convention, except that S71 invents the wrong requirement; that is a faithfulness error, not a forbidden-modal error.

**Steps and conditions: revise.** The four checks and adversary lists already use lists. The condition on the protections at 35, the two window conditions at 21–22, the missing/removed/replaced signature conditions at 64–65, and the pin condition at 81–82 need lists under rule 8. The proposed replacements supply them. Format the restored cryptographic assumptions, time checks and negative-control conditions as lists too.

**Section-number references: one violation.** Owner note S78 says “In section 2” in the body (Pilot 96); move the locator to References. Heading numbers themselves are not body cross-references. The existing references section is appropriately placed.

**Idioms/metaphors/humour:** no humour or idiom finding. “Bitcoin fixes T” is terse but can mean “determines T”; its problem is missing explanation and selection detail, not necessarily a metaphor. “A receipt proves” has the substantive qualification problem in F01. “The receipt checks” names the wrong actor in F03. Do not inflate those into unrelated style findings.

**Headings:** “What Tessera V1 promises” and “A safe decision” need the same visible qualification as the claims: C7 is a criterion, not an achieved result. The C1 label “The bytes” can become “The content” to use the dictionary's project term. Replace the C6 heading “Without Tessera” with “Without the service.” The claim labels C1–C7 themselves are reference identifiers and can remain.

## Validation and limits of this review

The ledger covers all 79 units in original order, including the four boundary fragments, every non-claim fragment and the owner notes. The primary decisions are 55 FAITHFUL, 1 ADDS, 15 DROPS and 8 CHANGES, with five additional omission-only findings. The six A-series findings concern source wording and scope; they are not silently repaired by the pilot. Sentence counts and forbidden-modal checks are mechanical; active voice, vocabulary, and semantic decisions are manual judgments with source quotations.

This is a document review, not an implementation, formal-discharge or completed relying-party-test result. Proposed wording has no governing effect. Items marked [D] cannot receive a dictionary-compliance pass until the style vocabulary is repaired, and items marked [A] retain the stated source rule pending an amendment decision.
