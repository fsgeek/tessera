# The issuer implements the registered issuance lifecycle (2026-10-29, revised after review)

> **Status: OWNER DECISION**, by the owner instance (Claude Opus 5.5). It corrects an owner defect found by the
> Levadura consistency panel (finding c016, `levadura_salvaje/docs/tessera-a11-canary-scorecard.md`). Resolution S4
> (`docs/V1-SERVICE-RESOLUTIONS.md:23`) and the issuer failed every request 24 hours after acceptance. The
> registered lifecycle (A2.1, A2.2, A2.3, with A9.2's parameters) has no such deadline and makes "every
> timely-eligible attempt ships" an obligation on the implementation (`phase-0-prereg-amendment-2.md:143-145`).
> Registered text governs. This design changes no registered sentence. Where it cannot meet one (the step-5
> residual), it says so and leaves the choice to the author. Revised the same day after
> Codex's design review (`docs/reviews/issuance-lifecycle/CODEX-REVIEW.md`, IL-01 to IL-07; two prechecks failed on
> the first version: it carried CF2-01's lease margin into the latch, and it called a nominal budget a bound).

## What is registered

- **Parameters** (A9.2; frozen profile §1): δ = 72 h, ε = 24 h, k = 6, N = 3, S = 24 h.
- **Attempts** (A2.3, `:259-268`): at most N. Each has its own declared issue time. A retry that changes any
  committed byte needs a fresh stamp (A9.5, `phase-0-prereg-amendment-9.md:295`), and its signatures are frozen
  before it is stamped (A9.5, `:290-296`).
- **Eligibility** (A2.1 `:91-94`; A2.2 `:220-224`; A3.7.3 `:659-673`): the attempt's own authenticated evidence for
  `SHA256(A_sig)`, with the lowest qualifying height buried k = 6 deep on the pinned, linked segment (profile §7.1),
  satisfies all three conjuncts: `declared − ε ≤ T`, `T ≤ declared + δ`, and `confirmed_at ≤ declared + δ`. This
  is narrower than the whole `VALID_STRICT` verdict, and the remaining pre-ship checks stay separate. Rows 12.2 and
  12.3 of the verifier are two of the conjuncts, not the predicate.
- **Latch and expiry** (A2.1 `:150-162`): eligibility observed at or before `B = declared + δ + S` is timely. The
  boundary is inclusive and "latch-winning", and a latched attempt cannot expire. Expiry applies only strictly
  after B, and only to attempts with no timely-latched eligibility. Atomicity of latch against expiry is an
  obligation on the implementation (A2.3). If the predicate fails at issuance time, the attempt is discarded and
  re-issued, subject to N (A2.1 `:161-162`). A lag beyond S *may* be refused (A2.1 `:135-138`); refusing it is not
  required.
- **Refusal** (A2.3 `:265-268, :279-281`): exhausting N ends issuance in an explicit refusal, durably recorded, and
  the transition that expires the final attempt records the refusal in the same step. In V1 the refusal is local and
  returned by the API (A9.7 row 12; `docs/V1-CLARIFICATIONS.md` CL-03). A3's portable record, commitment and
  publication are not V1.
- **Budget** (A2.3 `:271-274, :288-289`): N × (δ + S), twelve days, is a *nominal* budget, "not a proven wall-clock
  bound". Termination is an obligation on the implementation, not a proven liveness property.
- **Window** (A9 `:422`): an attempt whose T would exceed not-after is not shipped.
- **No SLA here** (A2.1 `:139-142`): a hard latency bound may enter only as a deployment-profile item with monitoring
  and an explicit violation outcome. It never kills an eligible attempt.

## What the issuer does (revision 3; steps 3-6 and 10 revision 4 after `CODEX-CONFIRM-2.md`; steps 5, 8 and 10 revision 5, step 5 revisions 5.1–5.3, after the TLA+ model (R5–R53) and `CODEX-CONFIRM-3.md`)

The second revision let any worker latch or expire, and relied on compare-and-set plus re-observation. Codex found
interleavings in which a stale or partial fetch expires an attempt that another, stalled worker had already observed
on time (ILC-01). Compare-and-set makes the writes exclusive. It does not make the earlier observation win. Revision 3
removes the concurrency instead of arbitrating it.

1. **One writer.** Every lifecycle transition (start an attempt, latch, discard, expire, refuse, complete) is made
   only by the poller, which runs with reserved concurrency 1 (`service/issuer/infra/main.tf:354`). The API is
   read-only for the lifecycle: `api.status` no longer calls `settle` (`api.py:194`). Every transition is a write
   guarded on the expected state *and* attempt id, so a write meant for an ended attempt fails (ILC-05).
2. **Attempt isolation.** As before: each attempt's declared time, frames, signature jobs, proofs and evidence live
   under its id. A late response names its attempt and can never fill another.
3. **Latch (revision 4).** On each poll, for each open attempt, the poller fetches and upgrades the attempt's
   evidence and evaluates the predicate. If it holds, the poller writes the latch with `observed_at` and the
   qualifying presentation itself, not only its digests. A latch may be written at any time while the attempt is
   open, however late the observation. Timeliness is a chain fact (the registered model's `burialAtWall`,
   `formal/tla/P5cP5P6_BridgeSlack_Latch.tla:49, :68-71`), not the moment of the issuer's write.
4. **Expiry only on a conclusive negative (revision 4, after `CODEX-CONFIRM-2.md` ILC2-01 to ILC2-03).** Absence of
   evidence is never evidence of absence. An unlatched attempt expires only when, after B, the poller's own evidence
   for it is **complete** and fails the predicate. Complete means three things:
   - every calendar the attempt was stamped to has returned a Bitcoin attestation;
   - for every attestation, the full pinned, linked `h…h+5` segment has been obtained (profile §7.1,
     `270ca49:docs/V1-PROFILE.md:879-891`);
   - so the lowest qualifying height, its T and its confirmation are fixed and fail a conjunct.

   Stale, pending, partial or unavailable evidence never expires an attempt. No lease timing is relied on: whatever
   a killed invocation saw, a later invocation will see at least the same complete evidence. Calendars do not
   retract, the chain is public, and shallower reorganisations are absorbed by k-deep burial.
5. **Evidence that stays unobtainable (revision 5, after the TLA+ model, `formal/tla/issuer-lifecycle/RESULTS.md`).**
   An attempt whose evidence cannot be completed stays open. "Cannot be completed" includes sources that are up but
   answer with stale or partial data, not only outages (R5-F4). Revision 5.1 applies the R5 model findings:
   - **Fence first (R5-F3).** Before an invocation fetches for an attempt, it makes a guarded write that bumps the
     attempt's version, and continues only after that write commits. A write left in flight by a killed earlier
     invocation then fails its guard, so a leftover ending write can no longer beat a live latch.
   - **Reading taken before the fetch (R5-F1).** `unavailable_since` takes the wall reading made *before* the fetch
     starts, and only fetches started after B count.
   - **Reset only by a committed success (R5-F2).** A poll whose fetch succeeds (complete, or showing the predicate
     holding) clears `unavailable_since` and `failed_polls` in its committed write. A success that never commits
     resets nothing. That is the attainable form of the rule, as the model checks it.
   - **Sustained failure over a rolling window (revision 5.3, after `CODEX-CONFIRM-3.md` ILC3-03).** Time is cut
     into fixed poll intervals, indexed absolutely (`floor(fetch_start / poll_interval)`). A committed failed poll
     adds the index of the interval its *fetch started* in to `failed_intervals`, a set, so each interval counts at
     most once. A committed success clears the set. An *unlatched* attempt may end with `EVIDENCE_UNAVAILABLE` only
     when **the most recent full operating period of completed intervals** is covered: every one of those intervals,
     less the allowance, is in the set. The current, incomplete interval is excluded. Read literally, the current
     interval would hold only the decider's own uncommitted failure, and the attempt would strand (R53-F1). The window rolls with time. An interval with no failed
     fetch only delays the end, until a later window is fully covered, and never strands the attempt. Revision 5.2's
     window was fixed at the first failure and could become impossible to complete (ILC3-03). The runbook states
     the operating period and the poll interval, with the period a whole number of intervals. **The allowance is at
     least 1**, and smaller than the number of intervals. That is checked only for a window of two intervals. For
     longer windows, alternating fence slips can leave every other interval empty, and an allowance of 1 is then
     not enough (ILC4-02: a four-interval, allowance-1 probe went red). Before the gated path is enabled, its
     parameters must satisfy a coverage rule checked in the model (for slips of at most one interval, allowance ≥
     half the intervals is the candidate). The fence wait can move a fetch into the next interval, and
     with an allowance of 0 that slip can leave two intervals empty forever, so the attempt never ends (R53-F2). With
     an allowance of at least 1, termination is green in the model, and red with an allowance of 0, with the literal
     window and with the fixed window (`formal/tla/issuer-lifecycle/RESULTS.md` §8).
   - **Every lifecycle write is version-guarded (R5.1 finding 3).** That covers the fence, the latch, the
     `failed_intervals` update, the ending write, and the end-and-allocate write. A retried or leftover update
     therefore cannot count a failure twice or act on a version it did not read.
   - The ending decision re-fetches immediately before its guarded write.

   The basis is A2.1's permission, "an attempt whose lag exceeds S may be refused" (`phase-0-prereg-amendment-2.md:135-138`),
   together with A2.3's termination obligation (`:288-289`). A latched attempt is never ended for unavailability. An
   attempt that is not the last ends this way, and the next one starts (step 8). This is the usual end for an
   attempt that never confirms, because only complete evidence can expire it (model finding 5).

   **The residual, as the model found it (finding 2; revised after ILC3-01).** A refused attempt might have been on
   time on three paths. Here "B" is the deadline `declared + δ + S`; the burial time and the issuer's observation
   time are named separately.
   - (a) The issuer observed an eligible presentation but its latch never committed, because the invocation was
     killed, or the write was dropped or rejected by its guard. Afterwards a committed failed fetch was recorded in
     every interval of an operating period, less the allowance.
   - (b) No poll observed it as eligible, and a committed failed fetch was recorded in every interval of an operating
     period, less the allowance. These are sampled failures, not proof that the evidence was unobtainable at every
     instant.
   - (c) A killed invocation's leftover ending write commits before a live invocation's latch.

   Revisions 5.2 and 5.3 narrow (a) and (b) to sustained, sampled failure over a full rolling window. The fence
   write closes the leftover-write race (c): the R5.1 model finds it unreachable, and reachable again without the
   fence. The earlier (c) trace also observed eligibility after the deadline, so it was not a timely observation in
   every instance (ILC3-02 qualification). It does not remove (a) or (b). Whether A2.1's permission covers (b) depends on what A2 means by B. Its prose
   reads B as the service's observation time (`:115-124`); its mechanized model uses the time the burial happened
   (`formal/tla/P5cP5P6_BridgeSlack_Latch.tla:49, :68-71`). Paths (a) and (c) are not covered under either reading.
   **This departs from registered text, so it is an author decision, not an owner rule (precheck 4; framing per
   ILC4-03).** The conflict concerns *protected* timely-eligible cases: those A2.1 protects (`:130-160`).
   - Path (a) is always one: an eligible presentation was observed and only its persistence failed.
   - Path (b) is one under the burial-time reading of B (A2's model). Under the service-observation reading (A2's
     prose), it may fall outside the protection, but only when the observation lag actually exceeds S. Failed samples
     alone do not establish that.

   A2.1's permission is a *lag* test ("an attempt whose lag exceeds S may be refused", `:135-138`), not a deadline
   test. Under either reading, an already-protected eligibility does not become refusable because a write failed or
   time passed. For the protected cases:
   - Ending the attempt honours A2.3's termination obligation (`:288-289`) and gives up the shipping opportunity.
   - Never ending it preserves the *opportunity* to ship but cannot recover evidence that is permanently lost, so
     it does not guarantee shipment either.
   - A longer operating period delays the trade-off and may make it rarer. It does not resolve it.

   **The decision is broader than step 5 (2026-10-30, after `docs/reviews/issuer-lifecycle-impl/CODEX-CONFIRM-2.md`
   §E).** The implementation review lists other ways a request stays open indefinitely, outside the step-5 gate,
   because a dependency fails permanently and no impossibility proof exists. Examples: calendars that never accept a
   stamp, a chain that never reaches the git pre-commitment depth, a store or queue that stays down, an operator who
   never repairs the configuration or the catalog, a snapshot whose impossibility cannot be proven. Disclosing them
   does not discharge A2.3's termination obligation (`:288-289`). So the author's decision is one question: **what
   V1 promises about termination when a dependency fails permanently**. Step 5's sampled-unavailability ending is
   one answer for one class. One amendment should decide all of them together. The issuer implements the ending rule only
   after the author decides, by amendment, which obligation yields and how. Until then the design states the
   conflict and does not resolve it by operating rule.
6. **Permanent failure before B.** The same rule as step 4: discard before B only on complete evidence that fails
   a conjunct.
7. **After the latch.** The preserved qualifying presentation is used for assembly; it is never swapped for a
   different, worse one. A transient failure (store, explorer, calendar, DNS snapshot) is retried. The attempt is
   discarded only for a failure the frozen attempt cannot cure even with recovered evidence: T of the preserved
   presentation > not-after (A9 `:422`), or a verifier reason that depends only on the attempt's committed bytes.
   Each discard records its reason (ILC-04).
8. **Next attempt and refusal.** Ending attempt i and allocating attempt i+1 happen in one guarded write. So a crash
   cannot leave the request between attempts, and a retry cannot run twice. Each ended attempt records
   its own reason: `EXPIRED` (complete negative evidence after B); `DISCARDED` (complete negative evidence before B,
   step 7, or a signer's refusal, `SIGNER_REFUSED:<reason>`: an unsigned, unstamped attempt cannot be timely
   eligible); or `EVIDENCE_UNAVAILABLE` (step 5, gated). If i = N, the same write ends the request REFUSED with
   `ATTEMPTS_EXHAUSTED`, listing each attempt's reason. If a new attempt would need signing after the stop, the
   reason is `SIGNING_CLOSED`. A closed signing window never ends a latched or already signed and stamped attempt
   (revision 5, model finding 6).
9. **Public view and tolerance.** `fail_after` is withdrawn. The status shows `state`, `attempt` i of N, and for an
   open, unlatched attempt its B, with a note that the twelve days are nominal. The 15-minute visibility tolerance
   applies as stated; it never moves B.
10. **Mechanized check before code** (revision 4 adds the cases from ILC2: observation-to-send delay, a commit
    delayed after the send, a crash before persistence, timely burial with no observation, partial header recovery,
    and duplicate transition retries; the property is the registered one, on `burialAtWall`, not on the durable
    latch). The protocol in steps 1–8 (one writer, a killed invocation's delayed write,
    latch, expiry only on complete negative evidence, discard, allocation of the next attempt) is modelled by extending the existing
    latch model (`formal/tla/P5cP5P6_BridgeSlack_Latch.tla`), with a broken companion that must go red. The model
    is the paired formal side of the issuer change.

## Implementation boundary until the author decides (after `CODEX-CONFIRM-4.md` §C)

**Built now** (common to every option the author may choose):
- attempt isolation and immutable attempt material;
- the single lifecycle writer, the fence and version-guarded writes;
- the latch with its preserved presentation;
- expiry and discard on complete negative evidence;
- atomic end-and-allocate, and the atomic final refusal when N attempts end by permitted paths;
- the storage-lifetime fix;
- the public view.

Failure history (`unavailable_since`, `failed_intervals`) is recorded for diagnosis.

**Gated off** until a signed amendment decides step 5:
- committing `EVIDENCE_UNAVAILABLE` from sampled failure;
- ending an attempt, or allocating its successor, *because of* that condition;
- a final refusal, cleanup or terminal status derived from it;
- any timeout, signing-closure path, deployment deadline or age rule that would produce the same ending indirectly;
- any claim of full lifecycle compliance, or of guaranteed termination, while the gate is closed.

With the gate closed, an attempt whose evidence never completes stays open.

## Owner documents and code to change

- **Prose:**
  - S4: drop the 24-hour FAILED. "Usually within 3 hours" stays, stated and unguaranteed. State the attempt
    lifecycle, the nominal twelve-day budget, and REFUSED with its reasons.
  - L1: acceptance stops at least δ + S + 24 h before signing stops (an operating margin).
  - CL-03 item 1 (the closed reason set) and item 2 (it cites 24 hours).
  - The clock-tolerance decision.
  - `service/issuer/DESIGN.md`.
  - Historical reviews and dispositions keep their text and gain a supersession pointer where they still read as
    current guidance.
- **Code** (Codex IL-06 inventory):
  - `service.py:7` (`DEADLINE_S`).
  - `api.py:12, :52-75, :94`.
  - `pipeline.py:84-85, :149-150, :194-214` (response routing by attempt), `:263` (`sign_by`), `:475-491`, and the
    module header.
  - Tests: `test_faults.py:125-144, :181`; `test_review_fixes.py:95-106`; `test_confirm_fixes.py` (deadline
    fixtures, CF2-01) are rewritten against the registered lifecycle. The CF2-01 tests become latch and expiry
    serialization tests.
- **Storage lifetime (ILC3-04).** `service/issuer/infra/main.tf:101` expires every object under `content/`,
  `work/`, `frames/` and `result/` 31 days after creation, whatever state its request is in. Under the registered
  lifecycle an attempt can live longer than that, so the rule could delete a live attempt's frozen material or its
  preserved presentation. Revision 5.3.1 (after `CODEX-CONFIRM-4.md` ILC4-01): no age rule applies to a
  live request's objects. Deletion is keyed to the persisted request-end time: the existing cleanup obligation
  deletes content, work and frames at the end, and the receipt 30 days after `ended_at` (S5). The S3 lifecycle rule
  is only a backstop. It expires objects carrying a `cleanup-due` tag, which the cleanup obligation sets only once
  their deletion is due and then retries. An object's creation age therefore never makes it deletable early. A large preserved presentation is written as an
  immutable S3 object *before* the latch commits a reference to it (DynamoDB's item limit; no transaction spans
  DynamoDB and S3).
- `docs/V1-SERVICE-CONTRACT.md` is unchanged (S4 there says only that completion is not immediate). Nothing goes to
  tupay (embargo).

## How this happened

S4 was resolved from the outside view, and every review brief since took the resolutions and the design as its
source of truth, so none compared S4 with A2. Precheck 4 now fails an owner requirement that contradicts a
registered sentence. Its first catch was this document's own first version, which carried an owner margin into a
registered boundary.
