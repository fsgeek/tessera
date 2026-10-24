The byte checks pass. The record needs documentary corrections before signing; I found no security overclaim in its V1-only permission or its composition/capstone non-claims.

Verified independently:

- All five table sizes and SHA-256 hashes match `objects/` and `freeze-record.json`.
- JSON names `0a7b336180c1bb53da8158b795658c292460c086`.
- All 393 spec/vector inventory entries match that commit’s blob IDs, sizes and hashes.
- In a temporary detached worktree of `0a7b336`, `assemble.py --repo <worktree> --check /home/tony/projects/tessera/formal/freeze-v1` returned **agreement OK**. Fresh assembly reproduced all five objects and the JSON byte for byte. The worktree was removed.
- Vector checks passed: baseline 71/71 golden, 173/173 rejection, 5/5 controls; hybrid 35/35, 63/63, 1/1, plus 6/6 demonstrations.
- E9 totals are correct: **27 decisions, 26 ACCEPT and one CUT**, including the later R22 acceptance. Row 2’s author provenance and independence from the cut order are accurately summarized.

No repository files were edited. Formal models were not rerun.

1. **FR-01 — Medium — “Ready” precedes required locator reconciliation.**  
   [Record lines 3–5](/home/tony/projects/tessera/formal/freeze-v1/FREEZE-RECORD.md:3) supersede the draft without resolving its explicitly outstanding A9 locator refresh. This is required by [frozen profile §14.2 item 7](/home/tony/projects/tessera/docs/V1-PROFILE.md:1445), alongside the source identification already supplied by JSON. The locators remain stale: for example, the profile’s parameter reference `A9:217` points to “Not discharged”; parameters are at A9:223–225.

   **Replacement status pending completion:**

   > **Status: PROPOSED. Signing awaits the A9 locator reconciliation required by profile §0 and §14.2 item 7.** A9’s signing commit is `2ad3489`; the frozen source commit is `0a7b336180c1bb53da8158b795658c292460c086`.

   Before signing, supply the verified locator reconciliation outside the frozen parts. A general statement that stable section names govern does not complete the promised refresh.

2. **FR-02 — Medium — Hybrid registration’s final hash reconciliation is missing.**  
   The table supplies the current spec hash, and JSON supplies the current ENCODING hash, but the final record drops the draft’s explicit registration association and baseline-change accounting. [Profile §14.2 item 7](/home/tony/projects/tessera/docs/V1-PROFILE.md:1447) requires these together. R26’s packet reference still points to the superseded draft hash.

   **Replacement addition after the object table:**

   > **Hybrid registration completion.** For `formal/p8/HYBRID-REGISTRATION-RECORD.md`’s Specification entry, the frozen spec-object SHA-256 is `1755916c9a8528f38c5fc161df8d41c2e0609f69ce1e15140ee1848990d4111c`, superseding the draft record’s value. The selected branch remains HYBRID, registered 2026-10-16. Frozen ENCODING-V1 SHA-256 is `6da057fbdd0a45ab9002864d648451ad95b82fa3f2d342a3e7df6a3390ab5316`; its registered post-§5.2 baseline is `fe537b1fd68efa51d0a9e6cf29cb8572a9d8ef7906e6a9cf05de035dc446efd0`. The intervening changes are accounted for by ENCODING-V1’s 2026-10-19 change accounting and profile §13 note 11.

3. **FR-03 — Medium — Required post-exit work disappears from “Still to do.”**  
   [Lines 65–66](/home/tony/projects/tessera/formal/freeze-v1/FREEZE-RECORD.md:65) omit **P3’s assumption half**, **bounded local refusal**, and **E10 extraction by 13 November**, all explicit in [A9.2](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:214). The rulings also preserve P9 execution evidence.

   **Replacement:**

   > - **By 13 Nov:** E10 extraction.
   > - **By 20 Nov:** the V1 issuer on AWS behind an API; the service verifier; P3’s assumption half; E10 vectors run against AWS; P9 code inspection and its outstanding execution evidence, including the two-machine vector; bounded local refusal; A9.4’s missing-capture negative control; H3 measured.

4. **FR-04 — Low, non-blocking — E18-02 needs an explicit residual disposition.**  
   E18-02 remains open in the sign-off disposition and `RESULTS-K6.md`. The packet’s next steps nevertheless say to close it before completing the opening. Omitting it from the final record leaves those instructions unreconciled. The original reviewer expressly classified it as non-blocking; it is not a new A9.2 prerequisite.

   **Replacement addition:**

   > E18’s bounded sign-off stands. E18-02 remains open: provide a repository-relative reproduction runner with a source revision/hash manifest. It was classified as non-blocking in the E18 review. The owner must explicitly reconcile its deferral with the packet’s pre-opening instruction to close it.

5. **FR-05 — Low, non-blocking — R23’s corrected interpretation is omitted.**  
   [Line 39](/home/tony/projects/tessera/formal/freeze-v1/FREEZE-RECORD.md:39) omits R23 from the comment summary, although its corrected understanding is material in the rulings.

   **Replacement:**

   > Comments and clarified scope on rows 6, 10, 13, 18 and 21; row 23 accepted on the corrected understanding that the control binds temporal evidence to the exact receipt signatures committed in `A_sig`.

6. **FR-06 — Low, non-blocking — “Evidence for nothing” overstates the instrument restriction.**  
   [Line 59](/home/tony/projects/tessera/formal/freeze-v1/FREEZE-RECORD.md:59) is broader than A9.2, which expressly permits instrument outputs to select registered branches.

   **Replacement:**

   > Instrument outputs, including the two real receipts, do not constitute C-row evidence or discharge obligations. They may inform investigation and select among registered branches as A9.2 permits.

All twenty A9.2 exit-item categories are represented through E9 rows 7–26. The accepted sheet gaps and reviewer reservations remain visible; they do not justify inventing additional prerequisites. The deficiencies above concern completing the freeze record and preserving existing obligations.

READY TO SIGN: YES AFTER (FR-01 locator reconciliation, FR-02 hybrid-registration reconciliation, FR-03 post-exit obligations).


