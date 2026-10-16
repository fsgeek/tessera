# Skeptic read: V1-DERIVATION-DRAFT.md (2026-10-09)

> Reviewer: Claude Opus 5.5, skeptic instance, 2026-10-09. Read against `docs/V1-SCHEDULE.md`,
> `prototype/PHASE2-REPORT.md`, `prototype/PHASE3-REPORT.md` and `prototype/consumers/scenarios.py`. Citations
> are not checked line by line here; Codex is doing that in parallel. The draft is not edited.

**Verdict.**
1. The method is sound. The derivation from C1–C7 does reduce the gate. But as written, V1 is a **dual-signed timestamp notary for Tessera's own domain**, and A9 does not say so. Its "later path" also does not include the capability that would make it commercial (submitter identity).
2. Two phase-2 unsafe accepts survive into V1 with a `VALID_STRICT` headline: (e) revocation and (f) impostor. One of the draft's own V1 remedies, "check the issuer's revocation publication", refers to something that does not exist and is not on the 30 Oct list.
3. 30 Oct is reachable only if P8 and DNSSEC start now rather than after the 16 Oct signing, and items 10, 12 and 14 move off the path. Two items filed as "spec fixes" (Bitcoin header authentication, DNSSEC at T) are design work that could reopen the profile freeze.

## Findings

**1. Say what V1 actually is, and register the capability that would make it commercial.** In C4, D is the
*service's* domain (wamason.com), not the submitter's. A V1 receipt therefore says: "Tessera's two keys saw
these bytes no later than T." That is RFC 3161 TSA plus OTS, with two improvements: verification works offline,
and authority rests on DNSSEC and git instead of a CA. The success definition, "an organisation can obtain a
receipt … signed by key K whose authority is evidenced", invites the reader to think K is the organisation's
key. Phase-2 (f) shows exactly that misreading: an impostor gets `VALID_STRICT`, and both integrators accept it.
A9.3's future capabilities (LTV, renewal, standing, degraded) would not fix (f). Neither would anything else in
A9.3, because submitter identity or per-organisation issuance (PHASE2 design question 2) is not on the list.
So "thin unless the later path is real" is not an honest bound. The path, as listed, does not lead to the
commercial thing. There is also a usability point. Real SBOMs with floats are refused (`9.8`,
`P8_NUMBER_NOT_DOUBLE`, G-03), so in practice V1 users must pre-hash and submit a digest statement. *Change:*
(a) Put "D is the issuing service's domain; the receipt attests neither the submitter nor the referent" in the
claim sentence itself, not only in the non-claim column. (b) Add a row to A9.3: "Submitter attestation /
per-organisation issuer → **Attributed receipts**". (c) In A9.1 or the relying-party page, name the comparator
(RFC 3161 + OTS) and V1's two differentiators. (d) State the V1 payload rule for numbers, or digest-only, in
the profile.

**2. Case (e): the remedy A9.1 relies on does not exist.** A9.1 says the safe decision for (e) is "check the
issuer's revocation publication". PHASE2 §2.3 found that "no revocation publication, format or authenticated
effective time is defined (R-5.24), so there is nothing to fetch". A9.4's issuer duty, "publishes any
revocation in both channels, with its effective time", has no format and no work item in §5. It also cannot
work for DNS, which has no authenticated history: a removed TXT record does not prove *when* it was removed.
Only the git channel, through an OTS-anchored commit, can show that a revocation existed before
`anchor_time`. The phase-2 non-expert rule, "first entry `VALID_*` plus digest", still accepts (e) under V1,
because the headline is unchanged. *Change:* make the revocation publication NEEDED for V1. That means a git-channel
revocation record format with an OTS-anchored effective time, plus a step-by-step relying-party procedure in
E12. Size it (about 1 d). Drop "both channels" from A9.4, or state that DNS revocation is advisory only. Register
the predicted 4 Dec outcome honestly: a headline-only reader will fail (e) and (f), and the test measures
whether the documentation prevents that.

**3. Q3 is missing a cheaper option.** A V1 receipt ships only after k = 6 confirmations, which is after
`anchor_time`. At ship time the issuer can embed, or publish, an anchored statement from the git channel
saying "no revocation of K effective at or before ship time". That covers the whole window
(declared, anchor]. It is not full LTV capture: there is no freshness bound F and no renewal. But it might turn
`NOT_EVALUATED` into an evaluated conjunct for honest issuance. *Change:* size this option (owner estimate
needed; it looks like days, not 2–3 weeks) and add it to Q3 as (d). Option (b) is a strawman nobody will pick,
so drop it or say so.

**4. Strict-only is safe. The success definition then fails on its own wording.** In `scenarios.py`, (d2)
"honest, repo evidence lost" and (h) "honest renewal wrapper" both have `should_accept=True`. V1 gives both
`UNVERIFIABLE`, so the relying party rejects an honest receipt. A9.1 re-registers the *verdicts* but leaves the
*safe-decision* column alone. Against "reaches the safe decision on every case", V1 therefore fails twice by
construction. Excluding degraded mode itself is right: it removes both remaining phase-2 unsafe accepts, (c)
C-C5 composition and the d3 = d2 leaked-key collision. *Change:* re-register a decision column per case. Split
"safe" (no unsafe accept) from "complete" (no false reject), and allow false rejects only on (d2) and (h),
named in advance. Rewrite success clause 2 to "zero unsafe accepts; false rejects only on the registered
cases".

**5. Standing `ABSENT` on every receipt needs one sentence and one invariant.** The phase-2 careful integrator
required `ESTABLISHED`, so under V1 it would reject everything. The new code `ABSENT/NOT_ISSUED_IN_PROFILE`
correctly separates (g) "too early" from "abandoned". *Change:* (a) E12 must tell integrators to ignore standing
in V1. (b) Add an issuer invariant to A9.1: "a V1 receipt ships only when complete; an operator refusal never
concerns a shipped receipt". This closes PHASE2 design question 4 (R-4.88(i), a refusal after shipping) for V1.
Without it, a refused attempt can verify `VALID_STRICT` offline while its refusal exists only behind the API.

**6. Bitcoin header authentication is design work, not a spec fix.** §5 item 7 files "header rule (PoW +
linkage + checkpoint)" inside 2.5 d of spec edits. PHASE3 says retarget validation is not implemented (G-60),
no mainnet receipt has been anchored, PoW on regtest proves nothing, and a stale store needs every gap header
(about 4 MB a year; the full chain is 77 MB). "PoW" without retarget rules accepts a cheaply mined
low-difficulty chain. Even with retarget, k = 6 rests on an economic assumption: forging six mainnet blocks
costs more than the receipt is worth. That assumption must be stated as C5's non-claim. *Change:* make it its
own NEEDED item (about 1–1.5 d) that defines retarget, checkpoint and gap-header carriage, and gets one real
mainnet-anchored receipt verified offline *before* the 30 Oct freeze. Add the economic assumption to C5.

**7. "DNSSEC at T" may make honest receipts `UNVERIFIABLE`, and M8 appears twice.** PHASE3 measured a joint
RRSIG window of 1.6 days. T can be as late as declared + 72 h, and the window that remains at capture is shorter
than 1.6 days. So validating at T can be `BOGUS` for an honest receipt whose anchoring was slow. Validating at
an upper bound is also the wrong time: C4 is about authority *at issuance*. M8 sits in §5 item 7 ("DNSSEC at T
(M8)") as V1 work and also in A9.3 under T4 ("archived store in bundle (M8)"). Separately, and worth checking
against IANA: the root KSK-2024 roll is scheduled for about 11 Oct 2026, but the prototype pins KSK-2017
(tag 20326) alone. *Change:* define the evaluation time (for example, "some t within [T − δ − ε, T] inside
every RRSIG window", or a capture time anchored separately) as a NEEDED design decision. Measure Route 53's
actual windows on the real D once it is signed. Split M8 explicitly into a V1 half and a T4 half. Ship both
root KSKs in the trust configuration.

**8. Classification corrections.**
- *Move out of the 30 Oct path:* E10 specification (item 12; it serves 20 Nov), the slice-batch read (item 14;
  DESIGN by the draft's own table), and most of E8/E7/E11 (item 10). V1 needs a one-page E8 argument that the
  ProVerif and TLA+ verdicts compose for C3 × C5, not a 2-day mapping.
- *Move in:* the revocation publication (2), the header rule (6), the DNSSEC evaluation-time rule (7), and a
  second independent frame encoder. P8 says "two implementations agree", but nothing budgets the second one.
- *Ask:* E18 was run at `DepthK = 5`, and V1's k is 6. Either state why depth-5 evidence carries to k = 6, or
  list it as a gap. Do not leave it as a Codex pass only.

**9. A9 has the convergence failure Codex diagnosed, in new words.** These phrases have no closing rule:
"every finding dispositioned" (item 1), "plus one Codex review" (7), "a Codex falsification run" (6),
"reviewed by Codex" (12), "Codex's full pass" (13), "rigorous prose proof" (A9.2), "each row's *surviving*
review findings" (A9.2 clause 2), and "V1 rows marked `discharged`" (15). Each review can produce findings,
each finding can become an obligation, and nothing says when a finding stops gating. "Surviving" has no
definition and no named judge. *Change:* add a closure rule to A9.2:
- Each review is time-boxed and dated.
- A finding raised after the review date gates V1 only if it gives a concrete counterexample to C1–C7. Every
  other finding goes to the A9.3 register with a named capability.
- "Surviving" means a finding the owner has not dispositioned with a reason. The author's E9 read is
  accept/reject per row and raises no new questions.
- P8 "rigorous" means a proof plus vectors that pass a time-boxed Codex falsification attempt with no
  counterexample.

**10. A9.7 undercounts what changes.** "One property is weakened" is true of properties only. §3 rows 2, 4, 8
and 10 defer *gates* that were registered as preconditions: the capstone gate, the degradation red-bar,
standing before Band 0 exit, and the lifecycle model before the freeze. An author who reads only A9.7 will
think less changed than did. *Change:* "One property weakened (P6), one hypothesis withdrawn (H1b), four gates
deferred to named capabilities (rows 2, 4, 8, 10), and the v1-product done-line separated (row 3)."

**11. Schedule: the critical path is serial and has no slack.** The listed items add up to about 16.5 d before
the corrections above, and about 19 d with them. Parallel agents help only off the critical path, which is:
A9 signed (16 Oct) → profile doc (2 d) → P8 (4 d, plus the falsification run) → E9 assembly (about 27 Oct) →
author read → E17 (30 Oct). That is 10 working days with almost no float, plus about 5–6 h of author time
against a 6 h budget. A single Codex finding that needs a ruling slips the milestone. DNSSEC is a parallel path
that starts with a registrar check the author must do. The build for 20 Nov is not sized anywhere. It includes
KMS-backed OpenPGP (custom packet construction around a digest signature), a queue signer on the author's
hardware, real OTS parsing, and offline DNSSEC validation at a chosen time. Two of those could reopen the
freeze (6, 7). *Change:*
- Start P8 and the DNSSEC registrar check today. Neither depends on any Q1–Q5 answer.
- Apply the cuts from 8. Cut first: the slice-batch read, the E10 specification, and E8/E7/E11 reduced to
  one page.
- Edit the 400-line profile only. Mark the 2929-line spec as design reference and sync it after V1. Editing
  both doubles item 7.
- Add a 1-day spike before 23 Oct: one real mainnet receipt, verified offline, with DNSSEC on the real D.

**12. The author questions.**
- *Q1 bundles four rulings into one "yes"* (success definition, separation from the product done-line, H1b,
  expectations). The expectations table is the one that matters (finding 4), so ask it separately.
- *Q2 contains decisions that are not the author's.* "P8 by prose plus vectors" is a method choice for the
  owner. The author's question is whether to re-scope the gate to the NEEDED set under the closure rule in 9.
  Parameter ratification is the author's, and is fine there.
- *Q3 is a false trinary* (finding 3).
- *Q5 is a false binary.* A third option keeps Decision C's independence without the author's hardware: a
  second signer in another provider, or an HSM or VPS outside AWS. Today V1's availability, and the author's
  2 h a week, depend on a machine in his house. P4' versus P3' is engineering and should not be a ruling.
- *Missing questions that really are the author's:* who the 4 Dec tester is (draft finding 5 raises it but
  asks nothing), and whether a personal domain (wamason.com) should be the issuing authority for anything
  beyond a demo.
- *Ruling budget.* Five of the eight rulings are spent by 16 Oct, which leaves three for 20 Nov, 4 Dec and
  ship-or-stop. Say so in the budget line.
