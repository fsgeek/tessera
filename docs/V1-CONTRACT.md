# V1 service contract and failure model

> **Status: OWNER DRAFT, 2026-10-19** (Claude Opus 5.5, owner instance). It restates what A9.1 and A10 already
> registered. It changes no registered sentence; if it disagrees with A9 or A10, they win and this page is wrong.
> Revised the same day after a full Codex review (`docs/reviews/v1-contract/CODEX-REVIEW.md`, VC-01 to VC-25, all
> applied; `DISPOSITION.md`). Purpose: one page that the formal models, the conformance cases, the service and the
> testers are all checked against, so that when two of them disagree we can see whether the contract, the model or
> the code is at fault (the author's method, travelog 2026-10-19).

## 1. What a client gets

The client sends bytes. Tessera returns a **receipt**: a bundle that anyone can check later, without Tessera
running and without our help.

## 2. Guarantees

**Conditions.** Every guarantee assumes the registered cryptographic, key-use, authority, chain-history and
distribution assumptions (A9:32–52, A9:128–136). In particular: nobody misused the service's signing capability,
SHA-256 and OpenTimestamps hold, and the checker's verifier release is authentic.

When those hold, a checker who has the receipt, the published verifier, its trust configuration and the archived
listing evidence (A10:527–550) can establish:

| # | Guarantee | Source |
|---|---|---|
| G1 | **Exact bytes.** The receipt binds these exact bytes. Change one bit and the check fails. | C1 |
| G2 | **Presented to Tessera.** The bytes were presented to the Tessera V1 service at some issuance. | C2 |
| G3 | **Both signatures.** Both of the service's keys signed. A missing, stripped or swapped signature fails. | C3 |
| G4 | **The keys were Tessera's.** DNSSEC (`_tessera-v1.wamason.com`, at the snapshot's own anchored time) and a signed git commit (at its own evidence time) named the keys for the service's domain. The git commit was in the Bitcoin chain at least 6 blocks before the receipt. | C4, A10.6 |
| G5 | **Existed by a block.** The signed bytes and both signatures existed before a specific Bitcoin block: the lowest-height qualifying block in the presented proof, confirmed 6 deep. | C5, A10.1, A10.5 |
| G6 | **A real-time bound, under an unchecked assumption.** A-UTC says at least one of that block and its 5 successors has a time stamp at most 2 hours behind when it was made. If A-UTC holds, the bytes existed before U (the latest of those 6 times, plus 2 hours). U is reported separately and never changes the verdict. | A10.1.1 |
| G7 | **Window, two checks only.** The declared issue time is not before the keys' window opened, and the chain time T is not after it closed. This does not prove the signing happened inside the window. | C4, A10.2 |
| G8 | **No Tessera needed.** The verdict depends only on the inputs above. | C6 |
| G9 | **A typed verdict.** Once the trust configuration is authenticated, the verifier returns `VALID_STRICT`, `INVALID` or `UNVERIFIABLE`, with a reason code and `revocation: NOT_EVALUATED`, `historical_security: NOT_EVALUATED`, `standing: ABSENT/NOT_ISSUED_IN_PROFILE`. Missing required evidence prevents acceptance. A valid receipt still leaves everything in §3 unestablished. If the trust configuration is not authenticated, there is no receipt verdict. | C7, A10:558 |
| G10 | **Honest receipts cannot be moved.** If an attacker takes over the DNS and git authority records while the service's own keys stay secret and unmisused, it cannot move honestly signed frames to other keys or bytes, or change their signer sets, whether they were signed before or after the takeover. | A10.4 |
| G11 | **Attacker's own new keys rejected, with the listing.** A checker whose verifier release comes from a trustworthy release authority rejects receipts under keys not in that release's service-key listing for the exact domain, key pair and window, provided the first listing was confirmed before the receipt's anchor. | A10.4.1 |

If the listing is cut for schedule reasons (A10 row 33), G11 goes. G10 then holds only while the independent
release boundary of A9.5 holds, and new receipts under an attacker's keys may pass.

## 3. Not guaranteed

Each of these is a deliberate limit, not a missing feature.

- **Who submitted the bytes**, or that a replayed receipt suits the current transaction (case f).
- **What the bytes mean**, or that they are true. A contract inside the bytes is the checker's to verify (cases i, i′).
- **That a key was not revoked** (cases e, e′).
- **That an algorithm or a key was still safe** when it signed.
- **Any lower time bound or priority.** "Existed by" is never "existed after" or "came first".
- **Real time without A-UTC.** Without it, only chain order is claimed.
- **Standing** of any kind.
- **Separate control of the two keys.** One controller holds both. Capturing the issuing AWS account means both
  slots can sign.
- **Visibility.** Publishing the authority records is the issuer's duty; the verifier does not check it. V1
  guarantees no detection or public exposure of a capture, of new receipts, or of a release given to one party.
- **That DNSSEC shows publication before issue.**
- **Anything after a Bitcoin reorganization of 6 or more blocks.**
- **Renewal, degraded modes, or wrappers.** These are refused (`UNVERIFIABLE`), including honest ones (cases d2, h:
  the two registered false rejects).
- **Stability of T and U across different proofs.** A different proof or pin set can select a different block.
- **Protection for a checker who skips authenticating the verifier release** or runs a substituted one.

## 4. Failure model

| Failure or attacker | What still holds |
|---|---|
| Tessera disappears | Everything in §2, if the holder kept the receipt and the listing evidence. Reconstruction after the project dies is not demonstrated. |
| Attacker alters a receipt or moves its signatures | Rejected (G1, G3, G10). |
| Attacker uses its own keys, authority records not captured | Rejected: the required authority evidence does not name them (G4). |
| Attacker captures both DNS and git authority records | Honest receipts protected (G10). New receipts under its keys **pass** unless the listing rejects them (G11). |
| Attacker captures the issuing AWS account | **Not protected.** It can issue receipts that verify. |
| Attacker steals the release key | Past listings stay protected only for a checker with trusted conforming verifier code, the preserved listing evidence and independently authenticated Bitcoin history. A thief can still publish new bad releases. |
| Bitcoin miners lie about time | G5 holds (chain order). G6 holds only under A-UTC. |
| Bitcoin reorganizes fewer than 6 blocks | G5 holds. |

## 5. Pairing: where each guarantee is checked

The method needs every guarantee checked twice: once by a formal model or inspection, once by tests against the
implementation. When the two disagree, we fix the contract, the model or the code. This is a first mapping, not
yet checked case by case.

| # | Model side | Test side (`prototype/conformance/cases-index.json` groups) |
|---|---|---|
| G1 | P1, P8 (prose proof and vectors) | container, codec, field grammar, numbers, spec binding, receipt consistency, OTS |
| G2 | P1 | A9.1 mapping |
| G3 | P2, P3 | signature profile, possession, hybrid semantics, hybrid routing, hybrid positive, keys, receipt consistency |
| G4 | P10, S-P3: abstract authority and key binding only | DNSSEC, DNS record, git, chain order, authority isolation, pinned D |
| G5 | P5, P5c: temporal and confirmation rules. Existence before the block is an assumption, not modelled. | OTS, proofs, time |
| G6 | none | none (the `utc_assessment` wrapper is not built) |
| G7 | none (P5/P5c model related rules, not these endpoints) | time |
| G8 | P9: contract and code inspection; no discharging model is required | offline reproducibility vectors not built (`release checker` tests configuration updates) |
| G9 | P4 | dispatch, aggregation, A9.1 mapping, container (d2), trust config |
| G10 | S-P3 (honest-material key binding) | none named; honest-material transplant tests to be identified or built |
| G11 | none | none (listing not built) |

**Gaps this table shows.**
- Model and tests both missing: G6, G11.
- Model missing: G7's endpoints, and concrete authority (G4 beyond the abstract model).
- Tests missing: G8's offline reproducibility vectors, G10's honest-material transplant cases.

## 6. What the tester does (4 December)

One independent tester, who meets the criteria in `docs/V1-TESTER-BRIEF.md`, takes a receipt bundle and the
verifier release and runs the verifier. For each case in A9.1's scenario mapping, the tester decides from the
documentation alone whether to rely on the receipt, with no help from the project. **Pass:** no unsafe accepts,
and false rejects only on d2 and h. The result is that one tester's result.
