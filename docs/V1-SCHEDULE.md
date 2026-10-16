# V1: success definition and schedule

> **Dates ACCEPTED by the author, 2026-10-09** (*"I'll accept those dates"*). The success definition below is the
> owner instance's revision of a Codex draft. It goes into the 16 October amendment for adoption, and is not
> adopted yet. Owner instance: Claude Opus 5.5.

## Success definition (to be adopted by amendment by 16 Oct)

V1 succeeds when:

1. **An organisation can obtain a receipt**, at a stated cost and latency, asserting that *these exact bytes were
   presented, signed by key K whose authority is evidenced by named channels, no later than time T*.
2. **A relying party can verify that claim** without Tessera running and without the authors' help. From V1's
   documentation alone, it reaches the safe decision on every case in the prototype's scenario set, including
   the cases whose answer is "not established".
3. **V1 ships by 4 December 2026**, or the project stops pursuing V1 by explicit decision at that point.

## Milestones (Fridays) — ceilings, not targets

The author, 2026-10-09: *"nothing says we can't end before those dates."* Each date is the latest a milestone
may land. Finishing early is the expected case, not a bonus.

| No later than | Done means |
|---|---|
| 16 Oct | V1 definition and claim adopted. Band 0 re-scoped by amendment to the formal foundation for V1's claims, with design-level guarantees registered as future obligations. |
| 30 Oct | V1 profile frozen. P8 encoding settled (prose proof plus golden vectors). Spec fixes landed: malleability, issuer-name binding, anchor-time rule, revocation "not evaluated by the verifier", verifier-fixed required set. The DNS channel works for the issuer's domain. |
| 20 Nov | V1 issuing on AWS through an API (KMS + GPG). Model-derived conformance vectors run against it. |
| 4 Dec | Relying-party test (non-expert integrator, documentation only) and 2106-examiner test (Tessera off) pass. **Ship or stop: the author's decision.** |

**Slip rule.** If a milestone slips by more than a week, it is not extended quietly. The owner runs the tail
procedure on what is blocking it and brings the author one choice: cut scope or stop.

**Budget.** The author's time: about 2 h a week and at most 8 load-bearing rulings in total. Tokens: within the
subscription, tiered Sonnet core / Opus advisor / Haiku grunt, no Fable unless justified. AWS: a small monthly
cap, set by the author.
