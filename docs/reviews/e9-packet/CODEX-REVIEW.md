**The packet needs revision before it serves as the author’s sole E9 read.** All twenty A9.2 exit items appear, but several questions lack the claim the author must judge. The listing cut also remains framed as an owner decision despite the correction.

I reviewed the working tree at `17fc40b`. No files were edited. Severity below concerns the packet; it does not automatically classify a finding as an A9.2 technical gate.

1. **E9-01 — HIGH — Row 2, form R2, and dependent rows: the listing cut is still presented as decided.**

   [Row 2](/home/tony/projects/tessera/docs/E9-READ-PACKET.md:78) says “OWNER DECISION” and “override.” R2 repeats that label. A9.2’s trigger had not occurred, as the [dated correction](/home/tony/projects/tessera/docs/decisions/2026-10-19-listing-cut.md:8) now acknowledges. The summary, rows 19 and 22, and the proposed freeze nevertheless assume the cut.

   **Replacement:**

   > **AUTHOR RULING REQUIRED. The listing cut is not authorized by the registered text.** A9.2 permits this cut only if the 30 October exit slips. It had not slipped. Your adoption of option (e) therefore remains governing.
   >
   > **ACCEPT the owner’s proposed cut:** remove the listing and accept that new receipts under attacker-selected keys can pass after capture of both authority records.
   >
   > **REJECT the proposed cut:** retain option (e), complete its mechanism and vectors, and rebuild the affected freeze objects.
   >
   > **Owner recommendation: ACCEPT the cut**, because of its narrow protection and the evidence package users must preserve. Restoring it is estimated to cost four agent-days. The schedule estimate needs refreshing because assembly finished on 21 October.

   Change R2 to `listing cut — AUTHOR RULING REQUIRED`. Mark every dependent statement as conditional on this ruling. Also state the irreversible consequence: a later listing cannot protect earlier receipts.

2. **E9-02 — HIGH — Opening claim: it still promises signatures by the genuine service keys under the proposed cut.**

   [Lines 10–14](/home/tony/projects/tessera/docs/E9-READ-PACKET.md:10) say “Both service keys signed.” Under the capture case described immediately below, passing receipts can instead contain attacker-selected keys. The [contract’s capture row](/home/tony/projects/tessera/docs/V1-CONTRACT.md:72) expressly distinguishes these cases.

   **Replacement:**

   > The verifier checks signatures by both keys named in the receipt. DNSSEC evidence and a signed git commit name those keys for `wamason.com`. This establishes signatures by Tessera’s actual service keys only if the authority records named those actual keys. Under the proposed listing cut, capture of both authority records can defeat that assurance.

   Keep this condition beside the claim, rather than relying on a later boundary paragraph.

3. **E9-03 — HIGH — Opening adversary paragraph: arbitrary receipt changes are not always rejected.**

   [Lines 16–18](/home/tony/projects/tessera/docs/E9-READ-PACKET.md:16) say the verifier rejects changes to “any part” of a receipt. The profile explicitly permits replacing a possession signature with another conforming valid signature over the same manifest. That signature is outside `A_sig`. See [reconciliation note 13](/home/tony/projects/tessera/docs/V1-PROFILE.md:1331).

   **Replacement:**

   > Changing the content or the frames and signatures committed by the receipt anchor prevents acceptance unless the registered security assumptions fail. Some changes outside that commitment remain valid. For example, another conforming possession signature over the same manifest is permitted.

4. **E9-04 — HIGH — Rows 7–14 and 17–20: tool results are being substituted for the author’s claim read.**

   “TLC reports no error,” query names, and “anything since?” do not supply a statement whose faithfulness the author can judge. The earlier [C5 read](/home/tony/projects/tessera/formal/suite/READ-C5-2026-09-12.md:61) covered degraded Q2 headers; the packet now cites strict Q1 evidence. An unchanged result does not make those the same read. Row 18 was also previously presented with rulings deferred.

   The governing [agreement-gate explanation](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-4.md:139) requires the author’s judgment from the plain-language statement and cross-family review.

   **Replacement pattern for each affected row:**

   > **Claim:** [two sentences stating the V1 result].  
   > **Attacker and limits:** [one or two sentences].  
   > **Evidence:** [linked result and review].  
   > **Question:** Does this statement describe what the evidence establishes, without claiming more?

   For example, row 10 should state the required-failure/unperformable/pass precedence and its finite abstraction. Row 13 must distinguish abstract authority and key possession from concrete DNSSEC/git verification and possession over the actual manifest. Prior reads can remain useful context.

5. **E9-05 — HIGH — Opening and next steps: “passed their registered checks” and “every ACCEPT → opening” are premature.**

   [Lines 27–28](/home/tony/projects/tessera/docs/E9-READ-PACKET.md:27) give an unconditional completion statement. [Next steps](/home/tony/projects/tessera/docs/E9-READ-PACKET.md:248) leave only record formatting and locator repair. However, the frozen profile still calls the `gpgv` version **provisional**, with an owner choice required before the freeze. See [profile R3](/home/tony/projects/tessera/docs/V1-PROFILE.md:1950).

   **Replacement:**

   > The packet reports the completed checks and names remaining work. Your ACCEPT answers complete the author’s E9 judgments. The owner must then close the remaining freeze prerequisites, including the provisional release-checker choice, and reconcile the final objects and record. The signed opening commit follows those checks.

   Fixing the checker choice is owner work; the packet must not manufacture an additional author ruling for it.

6. **E9-06 — MEDIUM — Rows 5–6: the A10 custody contents required at the freeze are missing from the read.**

   The packet describes the release envelope and fingerprint channels, but does not state the required custody-procedure contents. [A10.4.2](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-10.md:628) requires release authorization, signing location, external backups, independent review against an external baseline, approval bound to the exact archive hash, and controlled media crossing.

   **Replacement addition to row 5:**

   > The freeze also fixes the custody procedure’s required contents. Each release needs independent review against an approved baseline outside the operational environment. Approval must name the exact archive hash. The procedure must cover authorization, signing, backups and file transfer. Building and rehearsing that environment remains due before the first public verifier release.

   This records an adopted requirement; it does not ask the author to design the procedure now.

7. **E9-07 — MEDIUM — Row 17: the unsupported-algorithm statement omits its decisive condition.**

   [Row 17](/home/tony/projects/tessera/docs/E9-READ-PACKET.md:158) says a well-formed unsupported algorithm gives `UNVERIFIABLE`. An independently failed required check instead makes the verdict `INVALID`. The [E6a result](/home/tony/projects/tessera/formal/tla/E6a/RESULTS.md:14) states this explicitly. E6a also adds separate models; it did not edit P4.

   **Replacement:**

   > E6a extends P4’s abstract classification with algorithm and evidence cases. A well-formed, correctly bound unsupported algorithm gives CANNOT VERIFY only when no independent required check fails. A definite required failure gives INVALID. These are bounded classification results for two slots and two evidence members.

8. **E9-08 — MEDIUM — Row 21 and filtering paragraph: the residual account is incomplete.**

   [Row 21](/home/tony/projects/tessera/docs/E9-READ-PACKET.md:174) reduces the concern to missing mapping sentences and an interim capstone statement. The [sheet’s gap list](/home/tony/projects/tessera/formal/E8-E7-E11-SHEET.md:92) also identifies missing indexed statements for V1-relevant temporal/bridge material and first-link Q1. The packet does not distinguish these from omitted material outside V1.

   **Replacement:**

   > The sheet contains the required prose correspondence and explicitly leaves composition unproved. Its E7 mapping gaps remain. Its E11 index also lacks entries for [name the V1-relevant omissions]. The owner must distinguish existing statements needing links from statements that do not exist. ACCEPT records the stated evidence and limits; it does not waive a registered prerequisite.

   A missing machine-checked signature/time composition is not, by itself, a new V1 requirement: A9 deliberately asks for the bounded sheet. Assess the actual assigned evidence.

9. **E9-09 — MEDIUM — Row 15: “claimed more than it proved” hides the concrete P8 counterexample.**

   [Row 15](/home/tony/projects/tessera/docs/E9-READ-PACKET.md:146) does not give enough information to assess the owner’s narrowing. The [review](/home/tony/projects/tessera/prototype/p8-falsify/REPORT.md:71) found two distinct accepted frames whose different hashes admit one verifying signature under a constructed key. It did not construct a complete passing receipt.

   **Replacement:**

   > The 20-minute review found a counterexample to the old signature-binding sentence: one signature verified over two different frames under a constructed key. It found no complete passing receipt and no encoding collision. The repaired P8 claim covers unambiguous encoding and anchor binding. Signature security remains with P1/P3 and their assumptions. Do you accept that bounded claim?

10. **E9-10 — MEDIUM — Row 20: the sign-off’s finite scope and remaining defect are understated.**

    [Row 20](/home/tony/projects/tessera/docs/E9-READ-PACKET.md:170) gives only `k = 6`. The [sign-off](/home/tony/projects/tessera/docs/reviews/e18-signoff/CODEX-REVIEW.md:55) excludes arbitrary skew and a parameter-general theorem. The completed bridge run used `MaxSkew=1`; the wider run was incomplete. E18-02 also concerns a runner that cannot execute directly from the checkout, not merely a missing hash list.

    **Replacement:**

    > Codex signed off on A7.8 option (a) at the stated finite bounds. The completed bridge run used skew ±1; the incomplete ±2 run supplies no passing evidence. This establishes no arbitrary-skew or parameter-general result. E18-02 remains: provide a repository-relative reproduction runner with a source-hash manifest.

11. **E9-11 — MEDIUM — Row 22: accepting the E12 page requires more than the optional excerpt supplied.**

    [Row 22](/home/tony/projects/tessera/docs/E9-READ-PACKET.md:180) asks acceptance of the page while making its only read optional. The excerpt ends before the [release-authentication instructions](/home/tony/projects/tessera/docs/V1-RELYING-PARTY.md:109) and verdict guidance. Those contain one of the two HIGH repairs cited as grounds for acceptance.

    **Replacement:**

    > Read the bounded claim, conditions, release-authentication instructions and verdict guidance reproduced below. Do they state the supported reliance and its limits clearly? This author read does not establish non-expert comprehension; the registered 4 December test remains.

    Reproduce that material in the packet, or name linked mandatory ranges and their length. Make the capture paragraph conditional on R2.

12. **E9-12 — MEDIUM — All rows: evidence navigation does not support a 30–45 minute sitting.**

    The packet contains only three Markdown links. Most references are code-formatted filenames; some are only query names or case IDs. Rows 23–24 have no evidence location. The filtering paragraph uses an unresolved `<name>` placeholder. Row 5 points into a proposal file rather than directly to the final profile rules.

    **Replacement:** give every row a compact, clickable source line:

    > **Evidence — optional verification:** [exact result], lines X–Y; [review/disposition], lines X–Y.  
    > **Required read:** none; the claim and limits are reproduced above.

    Where an external read is required, name its file, exact range, line count and estimated time. For rows 23–24, link the actual vector entries and checker result. For row 25, link the frozen inventory, L-60 expectation and generator. For row 26, link the registration evidence and freeze-record hash entry. Row 2’s advertised “all 44 lines” is stale: its decision file now has 52.

13. **E9-13 — MEDIUM — Form and rejection procedure: acceptance and rejection have overbroad consequences.**

    [Lines 207–208](/home/tony/projects/tessera/docs/E9-READ-PACKET.md:207) say acceptance “ratifies” all owner decisions. [Lines 253–255](/home/tony/projects/tessera/docs/E9-READ-PACKET.md:253) assume every rejection means repair and return, and row 3 predetermines that rejection requires `INVALID`. A rejection could concern the explanation or evidence. R2 is an author scope ruling, not an owner repair task.

    **Replacement:**

    > ACCEPT records your judgment on the statement printed in that row. Owner decisions retain their provenance. R2 separately records your author ruling. REJECT is recorded with any explanation you provide; the owner identifies the required correction or returns an explicit choice. Rejection alone does not select alternative semantics.

    Qualify the preamble-hash promise too: **if only the preamble wording changes**, only its object hash and catalog change.

14. **E9-14 — LOW — Row 19 and plain language throughout: shorthand obscures the decisions.**

    [Row 19](/home/tony/projects/tessera/docs/E9-READ-PACKET.md:166) calls the removed check the “M5 classifier.” The [exit audit](/home/tony/projects/tessera/docs/V1-EXIT-30OCT.md:147) describes a separate listing classifier placed **after M5**. M5 itself remains required.

    **Replacement:**

    > M2 fixes the service domain checked on both authority records. M5 fixes each manifest field through authenticated authority evidence or a fixed profile constant. The proposed listing cut removes an additional key-list check after M5; it does not remove M5.

    Apply [STE-STYLE](/home/tony/projects/tessera/docs/plain/STE-STYLE.md:16) elsewhere: explain technical terms on first use; replace “near the line,” “went red,” “slack,” and “reaches the verdict”; move source references to row ends. Split row 5’s compound question. Use VALID and CANNOT VERIFY in explanations, retaining exact identifiers beside them where needed.

The stated preamble bytes and all listed freeze hashes match the files on disk. I reran the P8 checker: baseline **71/71, 173/173, 5/5**; hybrid **35/35, 63/63, 1/1**, with **6/6** gate demonstrations. The correct-form result table contains **47 + 47 + 35 = 129** strict rows. I inspected the archived formal results and reviews; I did not rerun the full TLC or ProVerif campaigns.


