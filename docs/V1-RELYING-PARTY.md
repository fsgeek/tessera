# Using a Tessera V1 receipt: a guide for users

> **OWNER DRAFT 2026-10-19, revised after Codex review (docs/reviews/exit-pages/).** (Claude Opus 5.5, owner instance.) The E12 page of the
> 30 Oct exit (A9.2, `docs/phase-0-prereg-amendment-9.md:208`; registered by
> `docs/phase-0-prereg-amendment-3.md:89-95`). It is based on `docs/V1-CONTRACT.md` (owner draft). It is written in
> the plain style of `docs/plain/STE-STYLE.md`. It adds no rule. If it differs from A9, A10, the V1 profile or the
> contract, they apply and this page is wrong. Markers such as [R4] point to the references at the end. The 4 Dec
> relying-party test will test this page; that test has not occurred [R27].

## What Tessera can establish, and what it does not establish

This list is copied without change from the 2026-07-28 ruling [R1]. Its words "package", "payload" and "issuer"
are the ruling's words.

> Tessera can establish:
> "This valid package reconstructs the same framed bytes recorded
> at issuance."
>
> Tessera does not establish:
> "The payload is true."
> "The issuer understood it."
> "The relying party interpreted it correctly."
> "This was the package the relying party expected."
> "The external thing named by the payload is authentic."

## What a VALID V1 receipt tells you

A receipt is the set of files that the service gives back for one content. The service is the Tessera V1
program that makes receipts. A verifier is the program that checks a receipt.

Some technical names appear in this guide. A key is a secret number that makes signatures. A signature is data that
only the holder of a key can make. Anyone can check a signature with the public part of the key. SHA-256 is a hash:
it turns any bytes into a short code. A change of one bit in the bytes changes the code.

DNS is the internet's name system. DNSSEC adds signatures to DNS records. Git is a system that saves versions of
files. A git commit is one saved version. Bitcoin is a public chain of blocks, and each block states a time.
OpenTimestamps records a hash in a Bitcoin block. A frame is the exact bytes that one service key signs. It fixes
the content and the receipt's common information.

If the verifier says VALID, these statements are true, under the conditions in "Conditions that V1 does not
check" below [R2]. Statements 2, 3 and 4 also need the authority-record condition in that section [R2a]:

1. The receipt fixes these exact content bytes. A change of one bit makes the check fail [R3].
2. Someone gave these bytes to the Tessera V1 service on some occasion [R3].
3. Both service keys signed them. A missing or changed signature makes the check fail [R3].
4. Two authority records named the two keys for `wamason.com`. One record is in DNS. The other is in a signed git
   commit that Bitcoin recorded at least 6 blocks before the receipt [R4].
5. The bytes and both signatures existed before a specific Bitcoin block. The verifier reports that block's
   chain time as T [R4].
6. The issue time that the service wrote is not before the start of the keys' window. T is not after the end of
   the window. The verifier makes no other comparison with the window. These two checks do not show that the signing
   happened inside the window [R5].

T is a chain time. A chain time is the time that a Bitcoin block header states. It is not a measurement of real
time [R6].

## What a VALID receipt does not tell you

A VALID verdict does not establish any of these [R7]:

- who gave the bytes to the service;
- what the bytes mean, or that they are true;
- that a key was not revoked (the report says `revocation: NOT_EVALUATED`);
- that a signature algorithm or key was still safe when it signed (`historical_security: NOT_EVALUATED`; see
  "Historical security" below);
- that the bytes existed after any time, or before other bytes;
- any standing (the report says `standing: ABSENT/NOT_ISSUED_IN_PROFILE`);
- that the two keys have different controllers. One controller holds both keys;
- that the authority records were public.

**Historical security.** To assess historical security, obtain authenticated safe-before cutoffs for each algorithm
and key. Compare them with T, using the registered chain-time uncertainty. Assess the theft of a key separately.
A comparison of T with a cutoff alone does not show that an algorithm was safe [R28].

**Real time.** The verifier can also report a value U in a separate field, `utc_assessment`. U is a real-time
upper bound only under an assumption, A-UTC. The verifier does not check A-UTC [R8]. A-UTC says this: at least one
of the selected Bitcoin block and its five successors states a chain time no more than two hours before the time
when the block was made [R9].

Use U only with a VALID receipt and A-UTC for the selected Bitcoin block and its five successors. A U beside
INVALID or CANNOT VERIFY does not show a valid service receipt [R8]. Always read U with A-UTC beside it.

**More than one receipt.** The same content can have more than one VALID receipt, each with its own T. Identify a
receipt by the SHA-256 hash of its `A_sig` bytes, not by the hash of its files [R10]. `A_sig` is the bytes that
hold both frames and their signatures.

## Conditions that V1 does not check

Each statement in "What a VALID V1 receipt tells you" is true only if these conditions are true [R2]:

- Nobody misused the signing capability of the service.
- The authority records named the service's actual keys [R2a].
- The registered signature and git-link security assumptions hold [R2a].
- SHA-256 and OpenTimestamps are not broken.
- The Bitcoin chain has no reorganization of 6 or more blocks [R11].
- Your verifier release is authentic.

**Capture of the authority records.** An attacker can get control of both the DNS record and the git repository.
Then the attacker can make new receipts under its own keys, and **the verifier says VALID for them** [R12]. V1 has
no protection against this: the service-key listing was removed from V1 [R13]. The verifier cannot see this
capture. V1 also does not check that the records were public [R14].

Receipts that the honest service signed stay protected in that case. This holds only while the service's own keys
stay secret and nobody misuses them. The attacker cannot move their signatures to other keys or other bytes [R12].

**Capture of the service's AWS account.** An attacker with the AWS account can sign with both keys. Its receipts
are VALID. V1 gives no protection against this [R15].

## Before you check a receipt

1. Get the verifier release from its publisher.
2. Check the release signature with an independently authenticated production release key [R16][R17].
3. Reject TEST keys. A release that is marked TEST is never for a real decision [R17].
4. Do not trust a key that came with the release. A substituted release brings its own key [R17].
5. Get all files of the receipt from the holder. The holder is the person who keeps a receipt.
6. Do not reformat the receipt files. A changed indentation makes the verdict INVALID [R18].

## How to read the verdict

The verifier gives one of three verdicts, with a reason code [R19]:

| Verdict | Meaning | What you do |
|---|---|---|
| VALID (`VALID_STRICT`) | All V1 checks passed. | Rely only on the statements in "What a VALID V1 receipt tells you". |
| INVALID | A check failed. | Reject the receipt. INVALID does not show that the content is false. |
| CANNOT VERIFY (`UNVERIFIABLE`) | The verifier does not have what it needs, or the receipt is outside V1. | Reject the receipt. If files are missing, ask the holder for them. |

Three special rules apply [R20]:

- The verifier can report a T with INVALID. That T is not evidence of a valid receipt.
- `INVALID / ISSUANCE_WINDOW` can come from a later OpenTimestamps proof. Ask the holder for the service's
  original proof.
- The verifier cannot check that the git commit was public.

## Decisions for each registered case

The registered mapping lists these cases [R21]. For each case, the verifier uses the strict check only.

The verdicts in the table are for the registered test files. Case b keeps the honest DNS and git evidence. Case d3
keeps the honest DNS evidence and has no git evidence. Case d1 uses honest receipt a. A different file can give a
different verdict [R21a].

| Case | Situation | Verdict | Your decision |
|---|---|---|---|
| a, g | An honest receipt, as the service shipped it. | VALID | Accept only this, under the conditions above: these bytes were given to the service, and they existed no later than chain time T. |
| b | An attacker signs the content again with its own keys. The honest DNS and git evidence stays. | INVALID | Reject. |
| c | Someone puts a receipt inside a second layer. | CANNOT VERIFY | Reject. |
| d1 | Someone asks for a check with fewer checks than strict, then asks for the strict check of honest receipt a. | The verifier refuses the first request. The strict check gives VALID. | Accept only the result of the strict check. The refused request does not become VALID. |
| d2 | An honest receipt without its git evidence. | CANNOT VERIFY | Reject. This is an honest receipt that V1 rejects. Ask the holder for the complete receipt. |
| d3 | A copy with one attacker key in both slots. It has the honest DNS evidence and no git evidence. | INVALID | Reject. |
| e, e′ | One key was revoked, before or after the issue time. | VALID | The receipt does not show that the key was not revoked. If your decision needs that, get other evidence. |
| f | Another person sends content through the honest service. | VALID | The receipt does not show who sent the content. If your decision needs the sender, check the sender yourself. |
| h | An honest receipt inside a renewal layer. | CANNOT VERIFY | Reject. This is an honest receipt that V1 rejects. |
| i | The content is a contract with two valid signatures of the parties. | VALID | Accept only this: the signed contract existed before the Bitcoin block whose chain time is T. T is not a real-time bound [OWNER 2026-10-19, PR-01]. You must check the parties' signatures and keys yourself. |
| i′ | The same, but one party signature does not verify. | VALID | Reject the contract. The receipt is valid, but your own check of a party signature fails. The service does not read the content. |

Cases e, f and i′ have one hazard. The verdict is VALID, but the receipt does not answer your question [R22].

## Open items in this draft

- The release key and its fingerprint are not yet fixed. A TEST release key must never appear on this page [R23].
- The scenario wording follows the registered mapping. A10 narrowed T to chain time and the window to two
  comparisons; this page uses the narrowed meaning [R5][R6].
- The registered text says the opening list is "verbatim" [R24]. The ruling asks for the list "nearly
  verbatim" [R25]. This page copies it exactly.
- A chain change to a DNSSEC algorithm outside {8, 13} makes new receipts CANNOT VERIFY. The service does not ship
  those receipts [R26].

## References

Line numbers in `docs/V1-PROFILE.md` are for commit `8ea8bfa`. Another session is editing the working copy
on 2026-10-19.


- [R1] `docs/reviews/2026-07-28-identity-boundary-evidence-floors-ruling.md:79-88`; required by
  `docs/phase-0-prereg-amendment-3.md:89-95`.
- [R2] `docs/V1-CONTRACT.md:17-21`; A9 "The boundaries", `docs/phase-0-prereg-amendment-9.md:45-52`.
- [R2a] `docs/phase-0-prereg-amendment-9.md:45-52`; `docs/phase-0-prereg-amendment-10.md:417-430` (new receipts under
  the captor's own keys).
- [R3] `docs/V1-CONTRACT.md:25-27` (G1-G3); `docs/phase-0-prereg-amendment-9.md:140-142` (C1-C3).
- [R4] `docs/V1-CONTRACT.md:28-29` (G4, G5); `docs/phase-0-prereg-amendment-9.md:143-144` (C4, C5).
- [R5] `docs/V1-CONTRACT.md:31` (G7); `docs/phase-0-prereg-amendment-10.md:363-371` (A10.2).
- [R6] `docs/phase-0-prereg-amendment-10.md:45-46`, `:230` (A10.1); `docs/V1-CONTRACT.md:48`.
- [R7] `docs/V1-CONTRACT.md:43-53`; `docs/phase-0-prereg-amendment-9.md:45-47`; report fields
  `docs/V1-CONTRACT.md:33` (G9).
- [R8] `docs/V1-CONTRACT.md:30` (G6); `docs/phase-0-prereg-amendment-10.md:300-305`.
- [R9] `docs/phase-0-prereg-amendment-10.md:186`, `:289-291`.
- [R10] `docs/V1-CONTRACT.md:58-61`; `docs/V1-PROFILE.md:1000-1005`.
- [R11] `docs/V1-CONTRACT.md:55`, `:76`.
- [R12] `docs/V1-CONTRACT.md:34-37` (G10, "No G11"), `:72`.
- [R13] `docs/decisions/2026-10-19-listing-cut.md:16-18`.
- [R14] `docs/V1-CONTRACT.md:52-53`.
- [R15] `docs/V1-CONTRACT.md:50-51`, `:73`; `docs/phase-0-prereg-amendment-9.md:142` (C3).
- [R16] `docs/V1-PROFILE.md:399-400`; `docs/V1-CONTRACT.md:63`, `:74`.
- [R17] `docs/phase-0-prereg-amendment-10.md:644-655`; the first production key may stay unpublished until the first
  public release, `:668-673`.
- [R18] `docs/V1-PROFILE.md:194-195`.
- [R19] `docs/V1-CONTRACT.md:33` (G9); `docs/V1-PROFILE.md:298-303`.
- [R20] `docs/V1-PROFILE.md:308-312`.
- [R21] `docs/phase-0-prereg-amendment-9.md:171-187`; `docs/V1-PROFILE.md` scenario mapping ("The A9.1 scenario mapping").
- [R21a] `docs/V1-PROFILE.md@8ea8bfa:1055-1069` (fixtures for b and d3); `docs/phase-0-prereg-amendment-9.md:178-182`.
- [R22] `docs/phase-0-prereg-amendment-9.md:189-191`.
- [R23] `docs/phase-0-prereg-amendment-10.md:644-646`, `:668-673`.
- [R24] `docs/phase-0-prereg-amendment-3.md:91-92`.
- [R25] `docs/reviews/2026-07-28-identity-boundary-evidence-floors-ruling.md:74-76`.
- [R26] `docs/V1-PROFILE.md:617-619`.
- [R27] `docs/phase-0-prereg-amendment-9.md:146` (C7, "not yet established"); `docs/V1-CONTRACT.md:102-107`.
- [R28] `docs/phase-0-prereg-amendment-9.md:259-277`.
