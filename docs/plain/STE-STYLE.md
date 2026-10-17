# Tessera plain-language style (inspired by ASD-STE100)

Owner instance, 2026-10-16. The author asked for documentation "written so someone whose native language isn't
Claude can understand it". These rules adapt the main writing rules of ASD-STE100 (Simplified Technical English).
We do not claim STE conformance: we have no approved STE dictionary check. We use the structure rules and our own
dictionary.

Revised 2026-10-16 after the faithfulness review of the A9 pilot (`docs/reviews/plain-pilot/CODEX-REVIEW.md`,
"Proposed dictionary work"). The revision adds the entries that the review lists and repairs receipt, anchor time,
window, authority record, key, AWS key, VALID and INVALID. It replaces "Google key" with "second key". It removes
"receipt ID", because its object was not defined. These entries are owner proposals. A reviewer must check each
new entry against its registered source before publication.

## Rules

1. One sentence gives one idea.
2. A sentence has a maximum of 20 words if it tells the reader to do something, and 25 words if it describes something.
3. A paragraph has a maximum of 6 sentences and one topic. A fragment such as a list item counts as a sentence.
4. Use the active voice. Say who or what does the action.
5. Use only the words in the dictionary below for project ideas. Each word has one meaning. Do not use a synonym.
6. Use technical names (for example "DNSSEC", "Bitcoin", "SHA-256") without change. Explain each one when you first use it.
7. Do not use idioms, metaphors or humour.
8. Write steps and conditions as numbered or bulleted lists.
9. Write "must" for a rule and "can" for a possibility. Do not use "should", "may" or "shall".
10. Do not refer to a document section number in the body. Put references at the end.

## Faithfulness

A plain document does not replace the signed or governing text. If the two differ, the governing text applies, and
the difference is a finding. Before publication, a reviewer checks each plain document against its source. The
reviewer confirms three things: the plain document contains no new rule, it removes no rule, and it changes no
meaning. The reviewer records each place where the source was unclear or contradictory.

A plain document does not resolve an unclear source. It renders the source as written and adds a visible marker,
for example "[A9 is unclear here: see A10 draft, item A01.]". The marker names the item that must resolve it.

## Dictionary

Code-style names (for example `A_sig`, `NOT_EVALUATED`) are technical identifiers. Use them without change and
explain them at first use.

### Content, receipts and the service

| Word | Meaning | Do not use |
|---|---|---|
| content | The bytes that a customer gives to the service. | data, document, payload |
| receipt | The set of files that the service gives back for one content. A receipt is the evidence. | attestation (alone), certificate, bundle |
| service | The Tessera V1 program that makes receipts. | Tessera (alone), issuer |
| issuance event | One occasion on which the service makes a receipt for content. | issuance (alone) |
| issue time | The time that the service writes into the frames when it signs. The verifier cannot check this time directly. | declared time |
| holder | The person who keeps a receipt. | custodian |
| user | The person who uses a verifier to make a decision about a receipt. | relying party (in plain text) |
| attacker | A person who tries to make a false receipt, to change a true receipt, or to make a false claim about a receipt. | adversary |
| operational sphere | Everything that the author uses to operate the service: the accounts, devices, credentials and signing capability. | — |
| registered | Written in the signed amendments to the Tessera pre-registration. | — |

### Keys and signatures

| Word | Meaning | Do not use |
|---|---|---|
| key | A private signing key of the service. V1 has two keys, one in each slot. | signer |
| slot | The named position of one service key in a receipt. V1 has two slots, `kms` and `gpg`. | — |
| AWS key | The service key in the `kms` slot. It is in a hardware security module in the service's AWS account. The registered branch sets its signature algorithm. | kms key |
| second key | The service key in the `gpg` slot. It is outside the AWS account, in non-exportable hardware. The dated custody record names that hardware. It uses ECDSA P-256. | Google key, gpg key, token |
| key fingerprint | A short value that the verifier computes from a public key. It identifies that key. | key ID |
| repository key | The key that signs the git commits that hold the git authority record. It is not a service key. | — |
| DNS root key | A key of the DNS root zone that the trust file lists. DNSSEC checks start from it. | KSK (in plain text) |
| release key | The key that authenticates each verifier release and its trust file. | — |
| signature | The result when a key signs bytes. | — |
| signature algorithm | The method that a key uses to make signatures and that a verifier uses to check them. | cipher |
| signing capability | The ability to make a key sign. A person can have this ability without a copy of the private key. | key possession |
| non-exportable | A property of a key in hardware: nobody can copy the private key out of the hardware. It does not stop use of the key. | — |
| authority-record credentials | The credentials that let a person change an authority record: the DNS credential and the repository key. | channel credentials |

### What the keys sign

| Word | Meaning | Do not use |
|---|---|---|
| bind | Bytes bind a value when they fix that exact value, directly or through its SHA-256 hash. | — |
| frame | The exact bytes that one service key signs. Each frame binds the content and the common metadata, and names the key fingerprint for its slot. | signed part, payload |
| common metadata | The fields that both frames must contain with the same values. They include the domain name of the service. | — |
| `A_sig` | The bytes that hold both frames and their exact signatures in a fixed format. | signed core |
| receipt anchor | The SHA-256 hash of `A_sig`. OpenTimestamps puts this hash into Bitcoin. | — |

### Authority

| Word | Meaning | Do not use |
|---|---|---|
| authority record | A record that says which two keys belong to wamason.com and states their window. V1 has two authority records: one in DNS and one in a git commit. | key publication, channel |
| window | The period that the authority records state for the two keys. It has a start and an end. The verifier compares the issue time with the start and T with the end. It makes no other comparison with the window. | lifetime, validity |
| evidence time | The time at which the verifier checks one authority record. It is the chain time of that record's own selected block. | — |
| DNS snapshot | A saved copy of the DNS records and DNSSEC signatures for the DNS authority record. The service anchors it in Bitcoin. | — |
| DNS owner name | The complete DNS name that holds a DNS record. | — |
| commit | A git object that records a version of the files in a git repository. A key can sign a commit. | — |
| tree | A git object that lists the files and folders of one version. | — |
| blob | A git object that holds the bytes of one file. | — |
| object ID | The SHA-1 hash that git uses to identify a git object. | commit hash |

### Bitcoin and time

| Word | Meaning | Do not use |
|---|---|---|
| Bitcoin block | One block of the Bitcoin chain. Each block holds hashes and a header. | — |
| block number | The position of a block in the Bitcoin chain. The first block has number 0. | height (in plain text) |
| header | The part of a Bitcoin block that identifies the block and states its time. | — |
| chain time | The time that a block header states. It is a value from Bitcoin, not a measurement of real time. | block time |
| confirmation | The block that contains an anchor gives the first confirmation. Each later block gives one more confirmation. | — |
| reorganization | A change in the Bitcoin chain that removes recent blocks and puts other blocks in their place. | reorg |
| OpenTimestamps proof | A file that connects a hash to one or more Bitcoin blocks. | OTS proof (in plain text), timestamp |
| Bitcoin attestation | A statement in an OpenTimestamps proof that a Bitcoin block at a stated block number holds a hash. It is not a receipt. | attestation (alone) |
| proof path | The steps in an OpenTimestamps proof from the hash to one Bitcoin attestation. | branch |
| selected block | The block of the Bitcoin attestation that the verifier selects from an OpenTimestamps proof. | — |
| anchor time (T) | The chain time of the selected block for the receipt anchor. T is a chain time, not real time. | timestamp |
| pin | An entry in the trust file that gives the exact header for one block number. | checkpoint |

### The verifier and its results

| Word | Meaning | Do not use |
|---|---|---|
| verifier | The program that a person uses to check a receipt. | validator |
| trust file | The file that comes with a verifier. It lists the DNS root keys, the repository key and the pins. | trust configuration |
| verdict | The result of a check: VALID, INVALID or CANNOT VERIFY. | status, outcome |
| VALID | All of V1's registered checks passed. This does not mean that V1 checked revocation, historical security, standing, the sender or the truth of the content. | VALID_STRICT (in plain text) |
| INVALID | A registered check failed. INVALID does not show that the content is false. | — |
| CANNOT VERIFY | The verifier does not have what it needs to decide. This is not the same as INVALID. | UNVERIFIABLE (in plain text) |
| cryptographic assumption | A registered condition that V1 does not check: the hash functions and signature algorithms are not broken. | — |
| key-use assumption | A registered condition that V1 does not check: each key signs only the bytes that its rules permit. | key rules |
| Bitcoin history assumption | A registered condition that V1 does not check: the Bitcoin chain history stays intact and available. | — |
| revocation | A statement that a key must no longer be trusted. | — |
| historical security | Whether a signature algorithm or key was still safe at the time when it signed. | historical safety |
| status capture | Evidence about the revocation status of a key, saved after the anchor. V1 does not require it. | — |
| standing | Evidence of which result the service gave to an attempt: the shipped receipt, or an attempt that it replaced, refused or did not ship. | — |
| renewal | The addition of later evidence to a receipt, so that the receipt stays verifiable after an old mechanism becomes unsafe. | — |
| wrapper | An outer layer of evidence around a receipt, with its own verification. | — |
| degraded verification | Verification in which a policy waives some registered checks. | — |

### The 4 December test and build evidence

| Word | Meaning | Do not use |
|---|---|---|
| relying-party test | The registered test on 4 December 2026. One independent person uses only V1's documentation to decide each case of the registered mapping. | usability test |
| registered mapping | The registered list of test cases, with the expected verdict and the safe decision for each case. | scenario set |
| unsafe accept | A decision to rely on a claim that the evidence does not establish. It can concern a VALID receipt. | bad accept |
| false reject | A decision to reject an honest receipt. | — |
| independence conditions | The registered conditions for the test person: a computing background, no knowledge of this field or project, no talk with the author about Tessera, and no help during the test. | — |
| negative control | A test that must fail for a program with a known defect. It shows that the test can find that defect. | — |
| companion verifier | A verifier with one deliberate defect, made for a negative control. | broken verifier |
