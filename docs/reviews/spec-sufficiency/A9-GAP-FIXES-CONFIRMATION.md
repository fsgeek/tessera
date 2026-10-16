# A9 gap-fixes confirmation — 2026-10-14

**Result: F01–F04 APPLIED. No new HIGH issue found in the applied A9 changes.**

Scope: confirmation of `a9-gap-fixes.diff` as applied to `docs/phase-0-prereg-amendment-9.md`, against `CODEX-REVIEW-RESOLUTIONS.md` F01–F04 and `DISPOSITION-RESOLUTIONS.md`. This is a document-level confirmation, not implementation validation, conformance-test evidence, custody discharge or adoption of A9. A9 remains PROPOSED and unsigned. Only this report is written.

| Finding | Status | Confirmation in A9 |
|---|---|---|
| F01 | **APPLIED** | A9.1 claim, lines 131–134, and C4, line 143, require chain-order pre-commitment: the selected git height plus five must be strictly below the selected receipt height. C4 explicitly disclaims UTC pre-commitment and DNSSEC publication-before-issue. The change is visibly labelled OWNER DECISION / BROADEN. |
| F02 | **APPLIED** | C6, line 145, identifies the selected anchor as the coverage referent, preserves pin checking for every supplied header, and says an unselected attestation without headers supplies no fact and is not a failure. This records the owner reading needed to remove the registered coverage ambiguity. |
| F03 | **APPLIED** | C5, line 144, fixes lowest block height, rather than least nTime, and takes T and confirmations from the same attestation. It expressly recognizes nonmonotone header times. |
| F04 | **APPLIED** | A9.5, lines 326–332, selects independent release allowlisting: each release compiles in its configuration hash, and release authentication uses a key inaccessible through DNS credentials, the repository key or the issuing AWS account. The boundary at lines 51–52 expressly excludes verifier-distribution compromise. CI is expressly insufficient as the authenticity check. |

## Chain-order rule and honest issuance

Read with the F02/F03 selection rules adopted in the disposition, each proof independently selects the lowest **qualifying** Bitcoin attestation height. Qualification requires the digest-linked merkle witness and a complete pinned, linked h…h+5 segment. An incomplete branch supplies no selected height; supplied contradictory evidence is not made harmless by nonselection. C5's “verified attestation” is therefore not the lowest syntactically asserted height regardless of qualification. The resolutions draft's time-cluster opening explicitly applies one selection rule to receipt, snapshot and git proofs.

Writing those selected heights as g and r, C4 requires:

`g + 5 < r`

This is well-defined on the shared pinned mainnet history. Same-height candidates cannot introduce a time tie: a pinned height fixes the header, its nTime and the fifth successor's nTime. Nonmonotone nTime cannot reverse this height comparison. Missing-header attestations do not supply alternative heights. If either required proof has no qualifying witness, pre-commitment is not established; the inequality cannot manufacture one.

The honest wait-first issue path passes this additional rule. Suppose the issuer validates the git assertion's sixth confirmation at height g+5, then builds, signs and freezes the receipt, and stamps its signature-inclusive anchor following A9.5. Under the continuing commitment/history assumptions, those newly created committed bytes cannot already have been included in the completed block g+5. Their inclusion height r is at least g+6. The first possible next-block inclusion passes: `g+5 < g+6`. Equality r=g+5 correctly fails; waiting only before shipment would not justify the same argument.

Presentation of an earlier qualifying git witness can only decrease the selected g and cannot defeat this honest ordering. A genuinely earlier receipt witness for those exact newly frozen signatures would contradict the assumptions used above. Header-clock skew does not invalidate the height argument. Other timestamp, window, signature and coverage checks still apply; this confirms that the new inequality adds no false rejection to the wait-first path, not that waiting guarantees every other check will pass.

## Boundary and C6 consistency

C6 remains a pure function of the bundle, the published verifier and its distributed trust configuration. Independently authenticating the release and fixing its accepted configuration hash determines which verifier/configuration inputs are trusted; it does not require Tessera to answer an online query during receipt verification. Changing the configuration bytes cannot become authorized merely through possession of an authority-channel credential. Independent release authentication is essential: the compiled hash alone would not authenticate an attacker-built release.

The new exclusion is consistent with the adversary paragraph: authority-channel capture remains in scope, while replacement of the independently authenticated verifier distribution is an explicit external boundary. The prohibition on AWS access to the release key also avoids conflating the slot-2 signing queue's capabilities in A9.6 with release authority. Append-only configuration obligations in A9.5 and the identical-declared-input stability contract in A9.4 remain applicable to authorized releases; the new authentication rule does not replace them. A9.1's signed, versioned trust set is compatible with independent release allowlisting and is not permission to accept any configuration signed by a channel key.

## Evidence limits

The disposition leaves release-key custody OPEN. A9 states the required authorization boundary; this pass does not establish that a dated custody record or deployed boundary exists. The captured-repository-signer negative test, selection/boundary vectors and release/bootstrap details remain implementation and freeze obligations, not evidence supplied by this diff.

`RESOLUTIONS-DRAFT.md` still contains pre-disposition G02/G03/G05/G08 wording, including the old distribution model and the nonmonotonicity rationale rejected in the review. The disposition adopts replacements, and the applied A9 records the governing choices. The APPLIED statuses above confirm this A9 patch; they do not certify that those downstream edits or the disposition's claimed added tests have been completed. No additional HIGH finding is raised on that basis in this bounded confirmation pass.
