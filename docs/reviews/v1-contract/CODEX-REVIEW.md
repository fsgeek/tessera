References below use **A9** for `docs/phase-0-prereg-amendment-9.md` and **A10** for `docs/phase-0-prereg-amendment-10.md`.

1. **VC-01 — HIGH — Guarantees omit their governing assumptions.**

   **Contract:16:** “A checker who has the receipt, the published verifier and its trust configuration can establish:”

   **Registered:** A9:128–136 begins “Conditional on the registered cryptographic and key-use assumptions”; A9:32–34 requires that signing capability was not misused. A9:47–52 excludes whole-author-sphere capture, breaks of SHA-256 or OTS, specified git-linkage failures, and distribution compromise. These qualifications are missing, making especially G2 unconditional.

   **Replacement:** “These guarantees require the registered cryptographic, key-use, authority, chain-history and distribution assumptions, including no misuse of the service’s signing capability.”

2. **VC-02 — HIGH — Offline verification omits required evidence outside the bundle.**

   **Contract:27:** “The verdict depends only on the bundle, the verifier and its trust configuration.”

   **Registered:** A10:527–546 requires an installed, archived listing-evidence package outside the receipt bundle and declares its manifest, proofs, headers and independent-history evidence as verification inputs. A10:548–550 instructs holders to preserve that package and disclaims demonstrated dead-project reconstruction.

   **Replacement:** “Offline verification also requires the archived listing-evidence package and its declared history inputs, which the holder must preserve with the receipt.”

3. **VC-03 — HIGH — Release-key theft row promises protection from history authentication alone.**

   **Contract:57:** “Protected only for checkers who authenticate Bitcoin history independently (A10.4.1).”

   **Registered:** A10:503–514 requires a trusted conforming verifier, independently authenticated history for all relevant proofs, and retained provenance; it explicitly says an attacker-signed executable can omit the rule and later theft can produce new bad releases. Independent history alone is insufficient.

   **Replacement:** “Past listings have retrospective protection only with trusted conforming code, preserved listing evidence and independently authenticated history; theft can still produce new bad releases.”

4. **VC-04 — HIGH — Attacker-key rejection is incorrectly attributed to the two authority channels.**

   **Contract:54:** “Attacker uses its own keys and claims to be Tessera | Rejected (G4).”

   **Registered:** A10:425–430 allows new captor-key receipts after both channel credentials are captured; A10:586–591 prevents acceptance only within the trustworthy-release and listing scope. `prototype/conformance/cases-index.json:2659–2663` explicitly expects `AUTH-i-T`, with both channels asserting attacker keys, to be `VALID_STRICT`.

   **Replacement:** “Attacker keys fail when they contradict required authority evidence or the trustworthy release’s listing; captured channels alone do not prevent acceptance.”

5. **VC-05 — HIGH — G10 turns an anti-reattribution property into unconditional continued acceptance.**

   **Contract:29:** “If an attacker later takes over the DNS and git authority records, receipts the service's keys signed honestly still verify, and cannot be moved to other keys or bytes.”

   **Registered:** A10:417–421 protects honestly signed frames against reattribution, signer-set alteration and signature transplantation, provided the original service keys and signing capability remain uncompromised. It covers honest signing **before or after** credential disclosure. It does not promise acceptance regardless of missing evidence or other failed checks.

   **Replacement:** “With the original service keys and signing capability uncompromised, channel capture cannot reattribute honestly signed frames or transplant their signatures, whether signed before or after capture.”

6. **VC-06 — HIGH — G9 incorrectly promises rejection whenever anything remains unestablished.**

   **Contract:28:** “When something cannot be established, the verifier says so and does not accept.”

   **Registered:** A9:183–187 expressly returns `VALID_STRICT` despite unestablished non-revocation, submitter identity or valid party signatures. A9:135–136 excludes these matters from the receipt claim.

   **Replacement:** “Missing required verification evidence prevents acceptance, while a valid receipt still leaves revocation, historical security, submitter identity and content claims unestablished.”

7. **VC-07 — HIGH — G5’s model mapping presents an assumed anchoring fact as a modeled guarantee.**

   **Contract:73:** “G5 | P5, P5c | OTS, proofs, time”

   **Registered:** A10:237–242 bases existence before the block on cryptographic and chain assumptions. `formal/PROPERTIES.md:39–40` distinguishes P5’s model and assumption halves. `formal/tla/P5P6_TemporalRevocation.tla:101–109` explicitly assumes that signed bytes existed when anchored; P5c supplies issuance and confirmation behavior.

   **Replacement:** “P5 and P5c check temporal and confirmation rules; existence before the selected block relies on the registered commitment and history assumptions.”

8. **VC-08 — MEDIUM — G9 incorrectly guarantees a receipt verdict for every invocation.**

   **Contract:28:** “One of `VALID_STRICT`, `INVALID`, `UNVERIFIABLE`, with a reason code, always with `revocation: NOT_EVALUATED` and `historical_security: NOT_EVALUATED`.”

   **Registered:** A10:558 specifies that missing or invalid required configuration or manifest yields `TRUST_CONFIG_UNAUTHENTICATED`, **“no receipt verdict.”** The index agrees at `prototype/conformance/cases-index.json:786–790`.

   **Replacement:** “After trust provisioning succeeds, receipt verification returns a typed verdict; unauthenticated required configuration stops provisioning without a receipt verdict.”

9. **VC-09 — MEDIUM — G10 omits the listing’s authorization and pre-commitment conditions.**

   **Contract:29:** “With the service-key listing, a checker using an authentic verifier release also rejects the attacker's own new keys.”

   **Registered:** A10:473–484 requires an exact domain/key-pair/window match and independent authorization with append-only closure. A10:497–499 requires the first-listing anchor plus five successors to precede the receipt anchor. A10:586–591 defines authenticity to include trustworthy release-authority behavior, not merely a valid signature.

   **Replacement:** “New-key protection requires a trustworthy release authority, an exact authorized key-and-window listing, and evidence that its first listing was confirmed before the receipt anchor.”

10. **VC-10 — MEDIUM — The listing-cut sentence drops its required release-independence condition.**

    **Contract:29:** “A10.4 lets the listing be cut for schedule reasons; G10 then keeps its first sentence only.”

    **Registered:** A10:769, row 33, permits that fallback only “while A9.5’s independent release boundary is established” and says cutting the listing does not cure failed release-key independence.

    **Replacement:** “If the listing is cut, honest-material protection remains only under the independent release boundary, and new attacker-key receipts may pass.”

11. **VC-11 — MEDIUM — G6 leaves A-UTC undefined and omits its output limits.**

    **Contract:25:** “If assumption A-UTC holds, they existed before a UTC time U (the latest of the 6 confirming blocks' times, plus 2 hours).”

    **Registered:** A10:277–293 defines the six blocks, including the inclusion block, and requires at least one header time to lag actual production by at most 7,200 seconds. A10:300–305 says the assumption is unchecked, U is reported separately, and U establishes no valid service receipt when reported with `INVALID` or `UNVERIFIABLE`.

    **Replacement:** “Under unchecked A-UTC, at least one of the inclusion block and its five successors is at most two hours backdated; U is a separate conditional assessment and never changes the verdict.”

12. **VC-12 — MEDIUM — Standing is missing from both output and non-claims.**

    **Contract:28:** “always with `revocation: NOT_EVALUATED` and `historical_security: NOT_EVALUATED`”

    **Registered:** A9:146 requires standing to be reported separately; A9:171–173 fixes it as `ABSENT/NOT_ISSUED_IN_PROFILE` for every scenario. A9:45–47 excludes standing.

    **Replacement:** “Every receipt report also states `standing: ABSENT/NOT_ISSUED_IN_PROFILE`; V1 establishes no standing.”

13. **VC-13 — MEDIUM — Historical key safety is omitted.**

    **Contract:38:** “**That the algorithms were still safe** when they signed.”

    **Registered:** A9:135 and A9:259–265 exclude historical safety of both algorithms **and keys**, retaining per-key custody and theft-cutoff assumptions.

    **Replacement:** “V1 does not establish that either signing algorithm or either key was safe when used.”

14. **VC-14 — MEDIUM — Replay suitability is missing.**

    **Contract:35:** “**Who submitted the bytes.** An impostor can submit content through the honest service (case f).”

    **Registered:** A9:141 states presentation is existential and excludes both “who submitted it” and “whether a replay suits the transaction.”

    **Replacement:** “V1 identifies no submitter and does not establish that a replayed receipt suits the current transaction.”

15. **VC-15 — MEDIUM — No lower time bound or priority is stated.**

    **Contract:39:** “**Real time without A-UTC.** Without that assumption, only chain order is claimed.”

    **Registered:** A9:144 explicitly retains “No lower bound, no priority”; A10:779–780 preserves that limit. A conditional UTC upper bound does not establish either.

    **Replacement:** “V1 establishes no lower time bound or priority, even when its conditional UTC upper bound is available.”

16. **VC-16 — MEDIUM — G7 omits the explicit limits of the window comparisons.**

    **Contract:26:** “The declared issue time is not before the keys' window opened, and the chain time is not after it closed.”

    **Registered:** A10:364–373 gives exactly those two inclusive comparisons, then explicitly disclaims establishing T ≥ not-before, declared time ≤ not-after, or any signing act inside the interval.

    **Replacement:** “Only declared time ≥ not-before and T ≤ not-after are checked; neither proves that signing occurred inside the window.”

17. **VC-17 — MEDIUM — G5 omits presentation-sensitive anchor selection.**

    **Contract:24:** “The signed bytes and both signatures existed before a specific Bitcoin block, confirmed 6 deep.”

    **Registered:** A10:253–257 specifies the lowest-height qualifying attestation in the presented proof, with T and confirmations from that same attestation. A9:144 retains “Presentation-sensitive T”; A10:576–580 says changed proof or pin inputs can change selection, T and U.

    **Replacement:** “The bound uses the lowest-height qualifying block in the presented proof; changing declared proof or pin inputs can change that block, T and U.”

18. **VC-18 — MEDIUM — G4 omits the distinct evidence times.**

    **Contract:23:** “Two channels named the keys for the service's domain: DNS (`_tessera-v1.wamason.com`, DNSSEC) and a signed git commit.”

    **Registered:** A9:143 evaluates DNSSEC at the snapshot’s own anchored time and authenticates both channels at their evidence times; it expressly says DNSSEC establishes no publication before issue. A10:719–724 corrects the owner name without removing those qualifications.

    **Replacement:** “DNSSEC authenticates the assertion at the snapshot’s anchored time, and git authenticates it at its own evidence time; DNSSEC proves no publication before issue.”

19. **VC-19 — MEDIUM — Private publication is not the full visibility limitation.**

    **Contract:42:** “**That an attacker publishes what it does.** A captor can keep a substitute authority record private.”

    **Registered:** A10:425–430 retains public publication as an issuer duty and disclaims publication, capture detection and public visibility. A10:593–599 additionally disclaims issuer detection and says a release delivered to one party is not detectable by others.

    **Replacement:** “Publication remains an issuer duty that the verifier does not check; V1 guarantees no issuer detection, public exposure or visibility of new receipts or targeted releases.”

20. **VC-20 — MEDIUM — The acceptance bar permits an all-reject result.**

    **Contract:86:** “Pass: no unsafe accept.”

    **Registered:** A9:115–122 requires zero unsafe accepts **and false rejects only on d2 and h**, using one independent tester with specified qualifications and no project help. Results must be stated as that tester’s result.

    **Replacement:** “Pass requires zero unsafe accepts and false rejects only on d2 and h, demonstrated by one qualified independent tester without project help.”

21. **VC-21 — MEDIUM — P9 is incorrectly described as an open model requirement.**

    **Contract:76:** “G8 | P9 (open) | trust config, release checker”  
    **Contract:80–81:** “G8's model half (P9) is open.”

    **Registered:** `formal/PROPERTIES.md:44` assigns P9 **inspection plus a conformance vector**, with a non-discharging TLA+ probe. A9:207 and A9:214 require contract inspection and later code inspection. The `release checker` cases at `prototype/conformance/cases-index.json:842–848` test configuration updates, not offline reproducibility.

    **Replacement:** “G8 requires P9 contract and code inspection plus offline reproducibility vectors; P9 has no required discharging model.”

22. **VC-22 — MEDIUM — P5/P5c do not model G7’s key-window endpoints.**

    **Contract:75:** “G7 | P5, P5c | time”

    **Registered:** A10:364–373 defines G7’s issuance-not-before/not-after comparisons. `formal/PROPERTIES.md:39–40` assigns P5 temporal soundness and P5c issuance confirmation; their models use declared/anchor/confirmation timing, not these authenticated key-window endpoints (`formal/tla/P5P6_TemporalRevocation.tla:98–138`).

    **Replacement:** “The `time` cases test G7’s key-window comparisons; P5 and P5c cover related temporal rules, while a model of these endpoint checks is unlisted.”

23. **VC-23 — MEDIUM — G4’s model mapping overstates concrete authority coverage.**

    **Contract:72:** “G4 | P10, S-P3 | DNSSEC, DNS record, git, chain order, authority isolation, pinned D”

    **Registered:** `formal/PROPERTIES.md:37,45` assigns P3 key binding and P10 manifest authority. S-P3’s header expressly excludes concrete verification-profile evidence (`formal/suite/s-p3/proverif/sp3_q1_strict_dns_compromised.pv:17–20`). Those results do not themselves model DNSSEC snapshot evaluation, git object traversal or C4’s height gap.

    **Replacement:** “P10 and S-P3 cover abstract authority and key binding; the listed groups test concrete authority checks, whose full model coverage remains to be identified.”

24. **VC-24 — MEDIUM — G10’s test group does not identify honest-material transplant coverage.**

    **Contract:78:** “G10 | S-P3 (honest-material half) | authority isolation; listing cases not built”

    **Registered:** A10:417–421 concerns reattribution and transplantation of honestly signed material. The `authority isolation` entries instead exercise attacker-keyed receipts and authority-path controls, including accepted captured-channel twins (`prototype/conformance/cases-index.json:2659–2663,2749–2753`). They cannot alone establish the stated honest-material property.

    **Replacement:** “S-P3 covers honest-material key binding; name explicit honest-material transplant tests separately, while listing tests remain unbuilt.”

25. **VC-25 — LOW — Several conformance mappings omit directly relevant existing groups.**

    **Contract:69:** “G1 | P1, P8 (prose proof and vectors) | container, codec, field grammar, numbers, spec binding”  
    **Contract:71:** “G3 | P2, P3 | signature profile, possession, hybrid semantics, hybrid routing, keys”  
    **Contract:77:** “G9 | P4 | dispatch, aggregation, A9.1 mapping”

    **Registered/artifacts:** C1 requires common-content consistency (A9:140), tested in `receipt consistency` (`cases-index.json:2112–2116`); exact anchored signature bytes are tested in `OTS` (`:1682–1686`). Slot swapping is in `receipt consistency` (`:2128–2132`), and successful hybrid signatures are in `hybrid positive` (`:2578–2592`). Registered false-reject case d2 (A9:181) is in `container`, not `A9.1 mapping`.

    **Replacement:** “Add `receipt consistency` and `OTS` to G1, `receipt consistency` and `hybrid positive` to G3, and `container` to G9.”


