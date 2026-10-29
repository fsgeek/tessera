**Verdict: not ready to implement.** The direction is correct, but the eligibility definition, latch boundary, and claimed lifecycle bound need correction first.

Review was read-only. I checked the registered amendments, the profile at `270ca49`, the verifier and issuer, and searched `service/` and `docs/` for the requested strings.

1. **IL-01 — High: eligibility is incompletely defined.**  
   [Design lines 18–20 and 29–31](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:18) identify eligibility with rows 12.2/12.3. Those rows are only two comparisons; they neither establish an authenticated anchor nor check the lower temporal bound.

   Registered authority:

   > “The issuer evaluates this conjunct **as part of the full three-conjunct temporal predicate**” — [A2.1:91–94](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:91).

   > `declared_issue_time − ε ≤ anchor_time`  
   > `anchor_time ≤ declared_issue_time + δ`  
   > `confirmed_at ≤ declared_issue_time + δ` — [A2.2:220–224](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:220).

   [A3.7.3:659–673](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-3.md:659) explicitly preserves the **burial-depth requirement** alongside those three conjuncts, while distinguishing them from the whole `VALID_STRICT` verdict. A9.7 explicitly leaves A2.1’s predicate unchanged.

   For V1, the evidence must concern the attempt’s frozen `A_sig`: [A9.5:290–296](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:290) requires stamping `SHA256(A_sig)` and freezing signatures before stamping. Frozen profile §7.1, lines 860–900, requires selecting the lowest qualifying height, with the complete pinned, linked `h…h+5` segment; `confirmed_at` comes from that same selected branch.

   **Correction:** define eligibility over authenticated, attempt-bound evidence with six confirmations and all three temporal conjuncts. Keep the remaining pre-ship checks distinct. Rows 12.2/12.3 alone are insufficient.

2. **IL-02 — High: CF2-01’s early cutoff contradicts the registered latch boundary.**  
   [Design lines 38–42](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:38) require the latch decision at least `WRITE_LEASE_S` before expiry. That excludes eligibility observed during the final 15 minutes, including the exact registered boundary.

   Registered authority:

   > “Eligibility observed at exactly `B = declared + δ + S` is timely — the boundary is **inclusive and latch-winning**” — [A2.1:153–156](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:153).

   > “Expiry … applies only **strictly after** the boundary, and only to attempts with no timely-latched eligibility. Atomicity of the latch against the expiry transition is part of the mutual-exclusion construction obligation” — A2.1:157–160.

   CF2-01 addressed the owner’s requirement that **completion become visible before a deadline**. Registered eligibility instead protects an observation from subsequent packaging and scheduling delay. An owner write-lease rule cannot move that observation boundary earlier.

   A compare-and-set prevents both terminal transitions winning against the same record version; it does **not** alone ensure that timely observation wins. For example, one worker observes eligibility at the boundary, its write stalls, and another worker expires the unchanged record afterward.

   **Correction:** specify serialization of evidence observation, latch and expiry, including delayed writes and crash recovery. Expiry must account for pending timely observations. Any AWS commit-latency assumption remains an assumption; the existing clock-tolerance decision does not authorize shrinking A2’s boundary.

3. **IL-03 — Medium: permitting late-observed eligibility is allowed, but step 4 contradicts itself.**  
   The permissive choice at [design lines 40–42](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:40) is compatible with:

   > “An attempt whose lag exceeds S **may be refused**” — [A2.1:135–138](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:135).

   “May” does not require refusal. Accepting authenticated chain-valid evidence observed after the nominal boundary, before an irreversible expiry decision, is a permissible policy choice. It cannot revive an already expired/refused attempt.

   But “latch whenever the predicate holds before expiry is decided” conflicts with the preceding requirement to decide the latch **15 minutes before** the boundary. State one consistent policy: mandatory protection for timely eligibility, optional acceptance of late observations while the attempt remains open, and no reopening after expiry.

4. **IL-04 — Medium: twelve days is a nominal budget, not an upper bound.**  
   [Design lines 44 and 49](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:44) say the request ends “at up to” `N × (δ + S)`, plus clock tolerance. The registration explicitly disclaims that conclusion:

   > “a **nominal lifecycle budget** … a nominal budget, **not a proven wall-clock bound on the process**” — [A2.3:271–274](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:271).

   > “termination is a contract obligation on the implementation, not a proven liveness property” — A2.3:288–289.

   Polling outages, delayed retry starts, and latched finalization can exceed twelve days. The optional late-observation policy further prevents treating this arithmetic as a hard bound.

   **Correction:** describe twelve days as nominal attempt-window budgeting. Do not turn it into a replacement request deadline.

5. **IL-05 — Medium: specify V1’s atomic durable refusal and API outcome; do not import portable-refusal machinery.**  
   [Design lines 21 and 36–37](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:21) correctly require explicit refusal, but the implementation section should require the terminal state and reason to become durable together.

   Registered authority:

   > “explicit refusal, durably recorded” — [A2.3:265–268](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:265).

   > “the transition expiring the final attempt’s window records the refusal in the same step” — A2.3:279–281.

   A3 adds portable records, commitments, handoff and publication. However, [A9.7 row 12:476](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:476) replaces the refusal-record decomposition with:

   > “Bounded local refusal returned by the API”.

   Thus V1 needs an atomic, final, locally durable refusal with a reason, exposed through its authenticated API and retained under its declared policy. It does **not** need A3’s portable record, public commitment, publication channel or acknowledgment workflow. “Recorded reason” suffices only if it means durable terminal operator state, not merely a log message.

   The owner-document list also misses [CL-03 item 1:34–35](/home/tony/projects/tessera/docs/V1-CLARIFICATIONS.md:34): its closed reason set lacks `ATTEMPTS_EXHAUSTED` and `SIGNING_CLOSED`, and associates accepted-request failures with `FAILED`.

6. **IL-06 — Medium: the change inventory omits operational deadline sites and tests.**  
   The listed documents cover the principal prose locations, apart from CL-03 item 1. They do not enumerate every executable use of the old rule.

   The requested search found these active implementation sites:

   | File | Locations requiring review |
   |---|---|
   | [service.py](/home/tony/projects/tessera/service/issuer/tessera_issue/service.py:7) | `DEADLINE_S`, line 7 |
   | [api.py](/home/tony/projects/tessera/service/issuer/tessera_issue/api.py:52) | completion settlement, lines 52–75; `fail_after`, line 94; import, line 12 |
   | [pipeline.py](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:81) | `_end`, lines 84–85; `advance`, 149–150; signer `sign_by`, 263; post-check rejection, 480–481; header commentary/import |
   | [test_faults.py](/home/tony/projects/tessera/service/issuer/tests/test_faults.py:125) | deadline expectations, lines 125–144 and 181 |
   | [test_review_fixes.py](/home/tony/projects/tessera/service/issuer/tests/test_review_fixes.py:95) | deadline-crossing expectations, lines 95–106 |
   | [test_confirm_fixes.py](/home/tony/projects/tessera/service/issuer/tests/test_confirm_fixes.py:46) | deadline fixtures and CF2-01 expectations, including lines 46, 178 and 198 onward |

   The authoritative prose sites are S4, L1, CL-03, the clock-tolerance decision and issuer `DESIGN.md`, as anticipated. Historical issuer reviews and dispositions also contain the old rule: preserve their historical text and add a supersession pointer where they serve as current implementation guidance.

   Other matches describe **ε**, **S**, or the retirement margin; those are separate rules and should retain their registered values.

   Finally, `fail_after = current attempt expiry` becomes misleading once eligibility latches, and it never promises request termination when another attempt remains. Specify its public semantics for retries and finalization.

7. **IL-07 — Medium: retry isolation and post-latch failure handling need design decisions.**  
   The attempt list is a start, but [design steps 1–3](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:28) omit several consequential transitions.

   Registered authority:

   > “A retry that changes any committed byte needs a fresh stamp” — [A9.5:295](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:295).

   > “If the predicate fails at issuance time, the attempt is discarded and re-issued … subject to the attempt bound” — [A2.1:161–162](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-2.md:161).

   Before implementation, specify:

   - **Attempt isolation:** separate frames, signature jobs, proofs and latch evidence by attempt identity. Current work-object names are reused, and signature-response handling resolves through the request’s current jobs ([pipeline.py:194–214](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:194)). A late response must never populate a later attempt.
   - **Known-invalid evidence:** define discard/retry when a temporal conjunct fails, rather than only retrying after wall expiry.
   - **Finalization failures:** distinguish retryable packaging/evidence unavailability from irreversible refusal. Current pre-ship paths recapture snapshots or end `FAILED` ([pipeline.py:475–491](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:475)); merely adding a latch will not resolve their interaction with the shipping obligation.
   - **Signing closure:** closing signing prevents fresh signatures; it does not itself justify expiring an already latched attempt or abandoning an already signed attempt that can finish without more signing.

   The design correctly states `N = 3`, strict per-attempt expiry after `declared + δ + S`, and A9’s no-ship invariant for `T > not-after`. The new acceptance margin is an owner operating choice, not a registered guarantee of completion.

The owner prechecks, applied to the design note:

| Check | Result | Evidence |
|---|---|---|
| **1. Capture row** | **PASS** | [Lines 18–24](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:18) make lifecycle claims, with no claim that dual-channel capture rejects attacker keys or exposes capture. The contract’s attacker-key acceptance remains applicable. |
| **2. Trigger clause** | **FAIL** | [Lines 38–42](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:38) transplant CF2-01’s completion-deadline consequence into eligibility latching. That deadline requirement is being removed; registered latch precedence governs instead. |
| **3. Requester** | **PASS** | [Lines 13–14 and 35–37](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:13) require fresh signing and respect signing controls; they make no key-storage or independent-approval security claim. This pass does not establish isolation of retry jobs. |
| **4. Binding text** | **FAIL** | [Lines 18–19, 38–39 and 44–49](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:18) respectively narrow the registered predicate, impose a contradictory owner latch cutoff, and promote nominal budgeting into an upper bound. |