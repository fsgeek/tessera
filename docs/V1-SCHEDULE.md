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
| 4 Dec | Relying-party test (non-expert integrator, documentation only) and dead-service test (Tessera off; A9:216. Renamed 2026-10-19 by the owner: V1 tests exit survival, not an 80-year horizon; `docs/decisions/2026-10-19-horizon-cost.md`) pass. **Ship or stop: the author's decision.** |

**Slip rule.** If a milestone slips by more than a week, it is not extended quietly. The owner runs the tail
procedure on what is blocking it and brings the author one choice: cut scope or stop.

**Budget.** The author's time: about 2 h a week and at most 8 load-bearing rulings in total. Tokens: within the
subscription, tiered Sonnet core / Opus advisor / Haiku grunt, no Fable unless justified. AWS: a small monthly
cap, set by the author.

> **Correction, 2026-10-27 (owner).** The budget paragraph was the owner instance's planning figure. It was never
> put to the author, and the author did not accept it with the dates: *"I didn't even know there was a ruling
> budget before this."* It does not bind. The owner still routes only load-bearing decisions to the author. The
> count of eight is withdrawn; earlier documents that cite it (`V1-DERIVATION-DRAFT.md:277` and the reviews that
> quote it) are left as written, because they are history.

## What "ship" means on 4 December — OWNER PROPOSAL, 2026-10-27

The author asked the owner to propose this. He recalled that at the start he had pictured *"a usable endpoint
someone can call"*. Shipping V1 means all of the following:

1. **A usable endpoint.** `POST /v1/requests` on AWS (API Gateway and Lambda, as built in `service/issuer/`), with
   both real signers. Clients are invited and get an API key. V1 is free (the S7 recommendation), the content
   limit is 1 MiB, and there is no availability target (S8).
2. **A public verifier release**, signed with the release key on the author's YubiKey, in the live-boot ceremony
   on the System76 machine (`docs/V1-RELEASE-KEY-CUSTODY-DRAFT.md`). This is the custody gate the author ruled on
   2026-10-18. It takes one session with the author, planned for the week of 16 November.
3. **A service page on wamason.com.** It states the claim, the §3 limits of `docs/V1-CONTRACT.md` (including the
   case where both channels are captured), how to call the endpoint, and how to verify without us.
4. **The two 4 Dec tests pass.**
   - *Relying party:* a model from a family that has not worked on Tessera or tupay's T1 gets only the published
     documentation and must reach the safe verdict on every scenario. If the author knows a human integrator
     willing to try, their run counts as well, and more.
   - *Dead service:* on a clean Azure VM, with the AWS endpoint switched off, receipts are verified using only the
     public release and the receipts (`docs/decisions/2026-10-27-v1-signer-placement.md` §4).

Ship or stop stays the author's decision. This list says what he would be deciding on.
