# What Tessera V1 promises, and under which conditions (plain version, pilot)

Status: PILOT, revision 2, owner instance, 2026-10-16. This is a plain rendering of the opening of Amendment 9 and
its claims C1 to C7. Amendment 9 is the signed text, and it governs. Words in this document have the meanings in
`docs/plain/STE-STYLE.md`. A reviewer must compare this text with Amendment 9 before anyone relies on it.

Revision 2 applies the faithfulness review of revision 1. Some Amendment 9 sentences are unclear. This text renders
them as Amendment 9 writes them and marks each one. A draft of Amendment 10 proposes the corrections.

## What V1 does

Tessera V1 is a service that makes receipts. wamason.com is the service's own domain name.

A receipt supports these four checks under both conditions:

- The registered cryptographic and key-use assumptions hold.
- Nobody misused the service's signing capability within the window.

Anybody can do the four checks without the internet and without help from the service:

1. The service received this exact content.
2. Both keys of the service signed it.
3. Two authority records said that these keys belong to wamason.com. They gave the window in which those keys can
   issue receipts. [A9 is unclear here: see A10 draft, item A02.]
4. The content and both signatures existed no later than the anchor time T. [A9 is unclear here: see A10 draft,
   item A01.]

The verifier must check each authority record at that record's evidence time.

DNS (the Domain Name System) holds one authority record. DNSSEC (Domain Name System Security Extensions) lets a
verifier authenticate DNS records with signatures. A git commit holds the other authority record. Git is a system
that stores versions of files and links them with hashes.

Bitcoin is a public system that adds blocks to a chain, one at a time. T comes from one Bitcoin block.
OpenTimestamps is a public system that puts hashes into Bitcoin blocks. SHA-256 is a hash function: it computes a
short fixed value from any bytes.

A person needs only the receipt, a verifier and its trust file to do the checks.

The verifier also checks the window. It makes only these two comparisons:

- The issue time must be at the start of the window or after it.
- T must be at the end of the window or before it.

The verifier does not compare T with the start of the window.

## What V1 protects against

V1 gives the correct verdict when an attacker does one of these things:

- The attacker changes a receipt.
- The attacker makes a false receipt.
- The attacker removes a part of a receipt.
- The attacker replaces a part of a receipt.
- The attacker presents a receipt again.
- The attacker claims that different keys or a different service made the receipt.
- The attacker claims an earlier issue time for a receipt.
- The attacker obtains authority-record credentials but cannot use either service key. [A9 is unclear here: see A10
  draft, item A04.]
- The attacker steals a key after Bitcoin anchors the receipt.
- The attacker gains signing capability after Bitcoin anchors the receipt.
- The attacker breaks a signature algorithm after Bitcoin anchors the receipt.

The authority-record credentials include the DNS credential and the repository key.

These protections depend on the registered cryptographic, key-use and Bitcoin history assumptions.

V1 does not promise that a receipt suits a new transaction when someone presents the receipt again.

## What V1 does not do

V1 does not tell you these things:

- who sent the content;
- what the content means, or if it is true.

V1 does not check these things:

- the revocation of a key;
- the historical security of a signature algorithm or key.

V1 offers none of these features:

- standing;
- renewal;
- wrappers;
- degraded verification.

V1 gives no earliest time for a receipt, and no order between receipts.

Amazon Web Services (AWS) is the cloud provider that runs the service. The issuing AWS account is the AWS account
that runs the service.

SHA-1 is an older hash function. Git uses SHA-1 to link its objects. The registered number k
is six.

V1 does not protect against these attackers:

- An attacker who has signing capability for both slots inside the window. Capture of the issuing AWS account gives
  this capability for both slots.
- An attacker who captures the author's whole operational sphere at issue time.
- An attacker who breaks SHA-256.
- An attacker who breaks OpenTimestamps.
- An attacker who changes Bitcoin history deeper than k. [A9 is unclear here: see A10 draft, item A03.]
- An attacker who finds different git bytes with the same SHA-1 hash as given git bytes.
- An attacker who influences the contents of a git commit.
- An attacker who compromises the release of the verifier or the trust file in it.

One person controls both keys.

## The seven claims

### C1. The content

The verifier rebuilds the exact frame for each key. Each key signs its own frame. Both frames must bind the same
content and common metadata. Each frame must name the key fingerprint for its assigned slot.

The frames can differ even when their content matches.

`A_sig` holds both frames and their exact signatures in a fixed format. The verifier reads `A_sig` in only one way.

V1 does not establish the meaning or truth of the content.

### C2. Presentation

The service received this content during at least one issuance event.

V1 does not establish who sent the content. V1 does not promise that a second presentation of the receipt suits a
new transaction.

### C3. The signatures

Each required signature must verify over the frame for its slot. The receipt is INVALID under any of these
conditions:

- A required signature is missing.
- An attacker removes a required signature.
- An attacker replaces a required signature.

One person controls both keys. The keys use separate technical systems. V1 does not promise independent control
or independent approval of content. V1 does not promise that the keys fail independently.

The second key signs frames that the AWS side of the service sends to it. So a person who captures the issuing AWS
account can make both keys sign. The non-exportable key cannot leave its hardware. This does not prevent an
attacker from using the permitted signing path.

### C4. Authority

Two authority records said that the keys belong to wamason.com, and they gave the window. The verifier checks each
record at its own evidence time. The verifier fixes the required set of authority records. The receipt cannot
choose that set.

The verifier checks the DNS authority record with DNSSEC:

- It must check the DNS owner name for wamason.com. [A9 is unclear here: see A10 draft, item A06.]
- It must check DNSSEC at the DNS snapshot's own evidence time.

The repository key signs a git commit. The verifier must check that signature. It must check the complete
commit-to-tree-to-blob path to the authority record. OpenTimestamps anchors the signed commit's object ID in
Bitcoin.

The verifier selects a Bitcoin block for the git record and another for the receipt. The selected git block number
plus five must be lower than the selected receipt block number. So the git record had six confirmations before the
block of the receipt anchor.

V1 does not check revocation. The verifier does not establish that the git commit was public. Neither authority
record commits to an individual receipt. The order is an order of Bitcoin blocks, not of real time. The DNS
evidence does not establish that the DNS record was public before issue.

### C5. Time

The frames and their exact signatures existed no later than T. [A9 is unclear here: see A10 draft, item A01.]

The verifier selects the verified Bitcoin attestation with the lowest block number in the presented OpenTimestamps
proof. [A9 is unclear here: see A10 draft, item A05.] T comes from the block of that Bitcoin attestation. The verifier
takes the confirmation count from that same Bitcoin attestation.

Six confirmations include the block that contains the receipt anchor. The sixth block has the selected block number
plus five. The following checks must all pass:

- The selected Bitcoin attestation must have at least six confirmations.
- T must be at least the issue time minus 24 hours.
- T must be at most the issue time plus 72 hours.
- The chain time of the sixth block must be at most the issue time plus 72 hours.

Different OpenTimestamps proofs for one receipt can give different values of T. V1 gives no earliest possible time.
V1 does not establish that this receipt came before a different receipt.

A Bitcoin block header gives a chain time. V1 does not promise that this time is close to real time.

A reorganization of Bitcoin history deeper than k is outside V1's protection. [A9 is unclear here: see A10 draft,
item A03.]

### C6. Without the service

The verdict depends only on the receipt, the verifier and its trust file. V1 does not establish that the holder
keeps the receipt. That is the holder's task. V1 has not demonstrated reconstruction after the project ends.

Unless another failed check requires INVALID, the verifier must give CANNOT VERIFY under either condition:

- The block number of the selected block for the receipt anchor is greater than the block number of the newest pin.
- A supplied header has no pin.

[A9 is unclear here: see A10 draft, item A05.]

The verifier must ignore an unselected Bitcoin attestation that supplies no headers. That Bitcoin attestation establishes
nothing and does not cause a failed check.

### C7. A safe decision (a test criterion, not yet a result)

The verdict has a type. The verdict reports these results separately:

- `revocation: NOT_EVALUATED` means that V1 did not check revocation.
- `historical_security: NOT_EVALUATED` means that V1 did not check the historical security of algorithms or keys.
- `standing: ABSENT/NOT_ISSUED_IN_PROFILE` means that V1 did not issue standing evidence.

V1 does not establish revocation, historical security or standing.

The relying-party test on 4 December 2026 checks one person's decisions on the registered mapping. The person must
meet the independence conditions. V1's documentation must let that person avoid every unsafe accept in those cases.
The test permits false rejects only for cases d2 and h. The test does not establish that all people can make safe
decisions. That result is not yet established.

An unsafe accept can concern a VALID receipt. For example, a VALID receipt does not identify the sender.

The build evidence must also include a negative control. The control uses a receipt with these properties:

- All V1 checks can run and pass.
- Only status capture is missing.

A companion verifier must fail the negative control under either condition:

- It gives INVALID only because status capture is missing.
- It gives CANNOT VERIFY only because status capture is missing.

## References

- Amendment 9 (`docs/phase-0-prereg-amendment-9.md`): the opening sections "The claim", "The adversary" and "The
  boundaries"; table A9.1, rows C1 to C7.
- The conditions: the A9.1 "Claim" paragraph. The independence conditions and the registered mapping: A9.1.
- The four confirmation and time checks: Amendment 2, A2.1 and A2.2; the parameters in A9.2.
- Whole operational sphere: R-2.15. Verdict precedence: A9.5, "Dispatch" (A4.2).
- The negative control: A9.4, "Contract for later verifiers". The standing value: the A9.1 scenario mapping.
- The DNS owner name: `formal/p8/ENCODING-V1.md`, section 7.
- The faithfulness review: `docs/reviews/plain-pilot/CODEX-REVIEW.md`.
- The corrections that the markers name: `docs/phase-0-prereg-amendment-10.md` (PROPOSED).

## Notes for the next faithfulness review (owner)

- Revision 2 applies findings F01 to F23 and O01 to O05 of the review, with the review's proposed text.
- The replay bullet describes another presentation of a receipt. The reattribution bullet describes a false claim
  about its keys or service.
- Each marker shows a place where Amendment 9 is unclear. This text does not resolve it.
- The dictionary entries for this revision are owner proposals. The reviewer must check each one against its
  source.
