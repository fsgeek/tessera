# Exploration note — landscape reconciliation: RFC 9943, convergent outside derivations, and the verifier-as-product question

> **STATUS: WORKING NOTES. NOT A PRE-REGISTRATION, NOT AN AMENDMENT,
> NOTHING DISCHARGED.** This document captures findings from an
> evening session (2026-08-11, Tony + Claude Fable 5) comparing two
> outside commercial analyses of Tessera against the repository's own
> record. It exists so the reconciliation is preserved on the record
> rather than left to memory or a session transcript.
>
> Everything here is a **candidate** or a dated observation. Nothing
> has been registered, reviewed by a non-author, or signed. The
> author has stated explicitly that this material does **not** imply
> an Amendment 4, and the engineering sequence (DECISION.md → bridge
> spike → core convergence) is unchanged by anything below. Items
> graduate the same way band-1 docket items do: by being registered
> (amendment or Band 1 specification) or disposed with reasons.

## Provenance

The author solicited independent commercial analyses of Tessera from
outside models (a Gemini analysis, then a GPT-family response to it;
neither is in this repository — the GPT response was supplied into
the 2026-08-11 session verbatim). Claude verified the two
load-bearing external facts by web search in-session and then
compared both analyses against the repository record: the June 13
business plan, the band-1 docket, PROPERTIES.md, and the first-link
spike artifacts.

## Verified landscape facts (new since the record's commercial documents)

Dated observations, verified 2026-08-11:

1. **SCITT is now a published standard.** RFC 9943, "An Architecture
   for Trustworthy and Transparent Digital Supply Chains," published
   June 2026 (<https://datatracker.ietf.org/doc/rfc9943/>). The
   record's SCITT mentions (cloud demo spec, marketplace business
   plan of 2026-06-13, prereg) all predate publication and treat it
   as a draft. RFC 9943 makes the same registration-vs-accuracy
   distinction Tessera's README makes: registration proves a
   statement was registered, not that it is true; the RFC describes
   registration as "akin to a notarization procedure."
2. **Microsoft has shipped a SCITT-compliant transparency service.**
   The Signing Transparency Ledger issues independently verifiable
   COSE receipts
   (<https://learn.microsoft.com/en-us/azure/confidential-ledger/about-microsoft-signing-transparency-ledger>).
   Its trust chain terminates in Microsoft's enclave and service;
   Tessera's terminates in a temporal anchor no participant operates.
   That difference is the current candidate answer to "why Tessera
   rather than MST + SCITT" — untested against real relying parties.

## Finding 1 — convergent derivation of the envelope thesis

The GPT analysis proposed, as its central product idea, that Tessera
become the durable "evidentiary envelope" in which stronger claims
made by other mechanisms (SCITT receipts, C2PA credentials, provider
attestations, human signatures) ride — Tessera's own claim staying
narrow: *this exact set was bound together at this time*.

This is not new. The marketplace business plan (2026-06-13) states,
nearly verbatim: "Tessera should standardize and preserve the
**evidence envelope** around third-party claims, not try to make
money from the commodity act of hashing a file," with the receipt as
the root of a durable claim graph.

An outside analyst with different priors, working from public
sources, rederived the June thesis independently two months later.
That is treated here as convergent validation of the envelope shape,
not as a new idea entering the record.

## Finding 2 — what the outside analyses caught that the record lacks

1. **The landscape facts above are not on record.** The business
   plan's competitive-landscape section is now stale in two material
   respects (RFC publication; MST shipping). This note is the dated
   correction.
2. **No explicit SCITT/COSE interoperability decision.** Band-1
   docket items 5 and 9 fix envelope encodings and byte budgets, but
   no item asks whether Tessera's envelope/receipt formats should be
   SCITT/COSE-interoperable or deliberately not. If unasked, Band 1
   format choices will answer it implicitly. **Parked question:**
   decide explicitly, on the record, before any Band 1 envelope
   format freeze. Candidate docket item; register if adopted.
3. **A sharper cheap-validation instrument.** The GPT analysis's
   customer probe is narrower than anything in the business plan's
   go-to-market section: *"When an AI-assisted review or decision
   matters enough that an auditor, regulator, opposing counsel,
   customer, or board might challenge it two years later, how do you
   currently prove exactly what evidence and criteria existed at the
   time?"* — followed by listening, with follow-ups keyed to
   "CloudTrail" (how does an external relying party verify?), "we
   retain PDFs" (how is existence-at-time established?), and "our
   GRC product" (does verification survive the vendor?). This
   belongs to the commercial track, which per the pre-registration
   is secondary and may not expand the demonstration's scope; it
   costs conversations, not code.

## Finding 3 — what the record holds that the outside analyses missed

1. **The damaged-chain layer.** Neither analysis touches what
   happens when custodians die, evidence is partially unavailable,
   or the transparency service itself is the casualty. The record's
   tending/custody machinery (docket items 13–16, including the
   dead-project demonstration: an old bundle's `VALID_STRICT`
   unaffected when custodial records are `UNVERIFIABLE`), and the
   first-link spike's compromised/unreachable results (Q5/Q5b red as
   registered, Q6 unreachable ×4 with machine-documented waiver
   costs), are exactly the layer outside eyes did not examine. SCITT
   as published largely assumes a live transparency service.
   Tessera's differentiation is deepest where nobody outside looked.
2. **Verdict-state semantics are already registered, not
   aspirational.** The GPT analysis flagged the
   verified/unverifiable/incomplete/superseded state vocabulary as a
   commercially interesting *hypothesis*; in the record it is
   ruling-governed adopted semantics. The outside analysis thought
   it was suggesting; the record had adopted.
3. **The adjudicator audience.** Contributed by the author in the
   2026-08-11 session, explicitly as *an* audience, not the entire
   list: courts and judges, regulators, arbitrators, mediators.
   Rationale (Claude, same session, candidate): adjudicators are the
   one professional population with centuries of native practice
   consuming exactly Tessera's narrow claim — a notary's seal does
   not prove the affidavit true; authentication is deliberately
   separate from weight. They will not misread "binding, not truth"
   as weakness. And independent temporal anchoring matters most in
   *adversarial* settings, where no party will stipulate to trusting
   the counterparty's vendor. If this audience is named in a
   registered or decision document (e.g., DECISION.md), the
   relying-party-story gap from Sol's 2026-07-28 findings has a
   candidate closure.

## Finding 4 — missed on both sides: the verifier is the product (candidate thesis)

Band-1 docket items 6 (embedded SPV header segment), 8 (standalone
versioned trust-anchor store), and 10 (executable-in-principle
verification spec) are, together, the components of a self-contained,
vendor-independent verifier. No document — inside the record or in
either outside analysis — states the thesis those pieces imply:

> For the adjudicator audience, the standalone verifier is the
> product surface. Customers use the attestation service; **relying
> parties** use the free verifier; and relying-party adoption is
> what makes attestations worth paying for.

**Parked question:** whether to name this thesis in DECISION.md
design content or a Band 1 specification, tying items 6/8/10 to it
explicitly. Candidate only; not registered.

## Finding 5 — the differentiator, sharpened (added same session)

The loose form — "SCITT didn't think about service death" — does not
survive rebuttal: SCITT receipts are explicitly designed to verify
offline, without consulting the service. The precise form does:

**A receipt's trust chain terminates in the operator's signing key,
and a dead operator's key rots.** A receipt from a sunset service
verifies forever against a key nobody can rotate, revoke, or defend;
no one answers an equivocation challenge once the log is gone; and
transparency's accountability guarantee — that a misbehaving log gets
*caught* — requires ongoing auditing of a live log. The receipt
outlives the service; the accountability dies with it. Tessera's
anchor is operator-independent by construction: the differentiator is
not "we survive service death" but **"our trust chain never contained
anyone whose death matters."** The tending/custody machinery,
explicit `UNVERIFIABLE` verdicts, and the dead-project demonstration
are the protocol *behaving well* during the decay other designs treat
as out of scope.

Why the gap exists (candidate explanation, not a criticism of
competence): standpoint. RFC 9943's author list is substantially
Microsoft Research / CCF — operators of live services, for whom
service death is an externality of the threat model. Tessera's design
center is archival (the "Designated Community" language of docket
item 10 is OAIS vocabulary), where the ten-years-later reader with no
one left to call is the normal case. The record saw the layer because
it was built from the grave backward.

Actuarial support for the adjudicator audience specifically: the
common risk is product sunset, not corporate death, and **evidence
lifetimes systematically exceed product lifetimes** — statutes of
limitations, appeals, patent and contract disputes make a
several-year-old attestation under challenge litigation's ordinary
case, and that horizon outlives most cloud products' support windows.

Candidate compression of Findings 1 + 5, offered for the DECISION.md
audience paragraph or wherever the relying-party story lands:

> **Tessera is the evidentiary envelope that outlives every issuer
> inside it** — including, someday, the SCITT services whose receipts
> it carries.

## Explicit non-implications

- No Amendment 4 arises from this note (author's explicit
  direction, 2026-08-11).
- The engineering sequence is unchanged: DECISION.md, then the
  capstone/bridge spike, then core convergence. The author has
  flagged inversion risk (record growing faster than foundation);
  this note is deliberately a parking record, not new process.
- Nothing here weakens or reinterprets any registered property,
  ruling, or amendment. If any parked item touches registered text
  when it graduates, it does so by the registered path.
