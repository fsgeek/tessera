# The issuer implements the registered issuance lifecycle (2026-10-29, revised after review)

> **Status: OWNER DECISION**, by the owner instance (Claude Opus 5.5). It corrects an owner defect found by the
> Levadura consistency panel (finding c016, `levadura_salvaje/docs/tessera-a11-canary-scorecard.md`). Resolution S4
> (`docs/V1-SERVICE-RESOLUTIONS.md:23`) and the issuer failed every request 24 hours after acceptance. The
> registered lifecycle (A2.1, A2.2, A2.3, with A9.2's parameters) has no such deadline and makes "every
> timely-eligible attempt ships" an obligation on the implementation (`phase-0-prereg-amendment-2.md:143-145`).
> Registered text governs. No registered sentence changes; owner documents and code do. Revised the same day after
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

## What the issuer does (revision 3, after `CODEX-CONFIRM.md` ILC-01 to ILC-05; steps 3-6 and 10 revision 4, after `CODEX-CONFIRM-2.md` ILC2-01 to ILC2-03)

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
5. **Evidence that stays unobtainable.** If an attempt's evidence cannot be completed, it stays open. After an
   operating period past B (runbook), an *unlatched* attempt whose evidence is still incomplete may be ended with
   `EVIDENCE_UNAVAILABLE`. This rests on A2.1's permission, "an attempt whose lag exceeds S may be refused"
   (`phase-0-prereg-amendment-2.md:135-138`), and on A2.3's termination obligation (`:288-289`). A latched attempt
   is never ended for unavailability.

   **Stated residual:** an on-time observation by an invocation killed before its write, followed by permanent loss
   of the evidence for the whole operating period. This is the one case where a refused attempt might have been
   observed eligible by B. It is named in the model as a witness (step 10), not hidden here.
6. **Permanent failure before B.** The same rule as step 4: discard before B only on complete evidence that fails
   a conjunct.
7. **After the latch.** The preserved qualifying presentation is used for assembly; it is never swapped for a
   different, worse one. A transient failure (store, explorer, calendar, DNS snapshot) is retried. The attempt is
   discarded only for a failure the frozen attempt cannot cure even with recovered evidence: T of the preserved
   presentation > not-after (A9 `:422`), or a verifier reason that depends only on the attempt's committed bytes.
   Each discard records its reason (ILC-04).
8. **Next attempt and refusal.** Ending attempt i and allocating attempt i+1 happen in one guarded write. So a crash
   cannot leave the request between attempts, and a retry cannot run twice. If i = N, or a new attempt would need
   signing after the stop, the same write ends the request REFUSED with `ATTEMPTS_EXHAUSTED`, `SIGNING_CLOSED` or
   `EVIDENCE_UNAVAILABLE`. A closed signing window never ends a latched or already signed and stamped attempt.
9. **Public view and tolerance.** `fail_after` is withdrawn. The status shows `state`, `attempt` i of N, and for an
   open, unlatched attempt its B, with a note that the twelve days are nominal. The 15-minute visibility tolerance
   applies as stated; it never moves B.
10. **Mechanized check before code** (revision 4 adds the cases from ILC2: observation-to-send delay, a commit
    delayed after the send, a crash before persistence, timely burial with no observation, partial header recovery,
    and duplicate transition retries; the property is the registered one, on `burialAtWall`, not on the durable
    latch). The protocol in steps 1–8 (one writer, a killed invocation's delayed write,
    latch, expiry after `B + lease`, discard, allocation of the next attempt) is modelled by extending the existing
    latch model (`formal/tla/P5cP5P6_BridgeSlack_Latch.tla`), with a broken companion that must go red. The model
    is the paired formal side of the issuer change.

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
- `docs/V1-SERVICE-CONTRACT.md` is unchanged (S4 there says only that completion is not immediate). Nothing goes to
  tupay (embargo).

## How this happened

S4 was resolved from the outside view, and every review brief since took the resolutions and the design as its
source of truth, so none compared S4 with A2. Precheck 4 now fails an owner requirement that contradicts a
registered sentence. Its first catch was this document's own first version, which carried an owner margin into a
registered boundary.
