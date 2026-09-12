# Codex pre-read of the routed batch C (2026-09-11)

Before reading `formal/suite/ROUTED-2026-09-06.md` §C himself, the
author asked Codex (OpenAI Codex CLI, gpt-6-astra, run from his own
terminal, read-only: "I haven't rerun the models or edited the working
tree") to look it over. Its feedback, verbatim, is below; the
collaborator's dispositions precede it. Every factual claim Codex made
was checked against the tree before disposition.

## Dispositions (collaborator, 2026-09-11)

1. **C8's proposed fix would break two-key acceptance — ACCEPTED,
   verified.** `sp2_q2_degraded_compromised.pv` lines 188 and 190
   match each signer's frame against that signer's own fingerprint;
   two such frames cannot be equal. The routed text now presents the
   framing fork Codex named — (a) common content in signer-specific
   frames, (b) one shared frame with manifest-borne key binding — and
   recommends (a). The earlier one-line recommendation was wrong and
   is retained struck through in substance by the correction note.
2. **C3's summary was narrower than its own record — ACCEPTED,
   verified.** `formal/spike/tla-probes/P10/RESULTS-PROBE.md` §C3 had
   already widened the divergence set; the routed item now states it
   and the availability consequence (an adversary altering only waived
   evidence can turn `VALID_DEGRADED` into `INVALID` under the literal
   reading). Recommendation unchanged and strengthened.
3. **§A4.6 is too broad — ACCEPTED; the collaborator's drafting
   error.** The author ruled that the adjudicator decides; the drafted
   sentence generalised that to "never a defect", which would excuse
   P1 and A3.2-floor violations under a degraded label. Routed as C11
   with Codex's qualifier recommended verbatim.
4. **C2 and C4 supported — RECORDED.** C4 gains Codex's two
   refinements: evaluation bounded by bundle and declared inputs;
   inability to evaluate is itself a recorded observation.
5. **C5 is header honesty, not coverage — ACCEPTED.** The routed item
   now says so and names where coverage lives.

Net: batch C is corrected, not withdrawn; one item added (C11); no
recommendation reversed except C8's mechanism, which was wrong.

## Codex feedback — verbatim

> This is a useful decision brief, but I would not approve it as a batch without a few corrections. The review work has exposed meaningful gaps. Some recommendations, however, make the decisions sound simpler than the code supports.
>
> The document records A1–A8 as already adopted. Section C is the current business. My main observations are:
>
> 1. C8 identifies a real problem, but its proposed fix conflicts with the current framing.
>
> The intended requirement makes sense: all required signers should attest to the same content.
>
> But the recommendation says "one framed byte string" and proposes equality across signer slots. The current verifier (formal/suite/s-p2/proverif/sp2_q2_degraded_compromised.pv:188) requires signer A's frame to contain A's fingerprint, and signer B's frame to contain B's fingerprint. With distinct keys and perfect fingerprints, those frames cannot be identical.
>
> Simply adding fa = fb would prevent legitimate two-key acceptance. The decision should first distinguish:
>
> - common attested content inside separate, signer-specific frames; or
> - one shared frame whose key-binding structure accommodates all signers.
>
> That is a substantive framing decision. The current recommendation conceals it behind "one equality."
>
> 2. C3's summary is outdated relative to its own supporting record.
>
> C3 (formal/suite/ROUTED-2026-09-06.md:251) presents the choice chiefly as handling an otherwise valid authority statement naming another key. The probe's later correction (formal/spike/tla-probes/P10/RESULTS-PROBE.md:389) says the difference also includes invalid signatures, late anchors, and some UNVERIFIABLE cases.
>
> That matters to your decision. Under the stricter reading, an attacker can damage waived evidence, without compromising any authority, and turn an otherwise VALID_DEGRADED package into INVALID.
>
> I lean toward reporting the waived evidence's condition without letting it override the remaining required chain. But you should be shown that availability consequence explicitly, rather than asked to decide from the narrower example.
>
> 3. The general degraded-mode principle needs a boundary.
>
> I agree with your distinction between verifier and adjudicator. Nevertheless, Amendment 4's wording (docs/phase-0-prereg-amendment-4.md:164)—a correspondence failing in degraded mode is "never a defect" provided the verdict says degraded—is too broad.
>
> For example, accepting altered bytes under an honest key would still violate the narrowed P1 claim. Losing the final complete evidence chain would still violate Amendment 3's floor. A degraded label cannot excuse either.
>
> I would preserve your principle with this qualification:
>
> > Losses explicitly permitted by the declared waiver policy are degradation costs. Failures of the remaining required checks are defects.
>
> That constrains what Tessera claims to have verified without prescribing what the adjudicator must trust.
>
> 4. C2 and C4 are worthwhile improvements.
>
> C2 correctly distinguishes two machines agreeing from two machines producing the right answer. The expected verdict, repeat-presentation case, and contradictory-service case each address a different blind spot.
>
> C4 is particularly aligned with your survivability purpose: preserve both why policy permitted the waiver and what the verifier observed. "This check was waived" alone loses information a later adjudicator needs. Evaluation should remain bounded by the available bundle and declared inputs; inability to evaluate is itself an observation to record.
>
> 5. C9 and C10 have sensible aims; C5 remains actual review work.
>
> I support checking that the wrapper's recorded inner version is accurate, and preventing standing evidence from silently shifting an artifact from identity A to identity B.
>
> But C5's four header reads should remain separate judgments. "The header accurately describes this bounded model" and "this model sufficiently covers the registered property" are different questions. The new headers disclose important limits, including two-signer bounds and restricted issuer behavior; honest disclosure does not itself close the coverage gaps.
>
> I inspected the routed file, relevant amendments, review findings, model headers, and selected verifier code. I haven't rerun the models or edited the working tree. C8 is the first correction I would bring back to Claude, because its literal proposed implementation would break the very acceptance case it intends to strengthen.

## Second pass — verbatim, with dispositions

Both corrections verified and applied in the routed file the same day:
the C3 direction (P4's `UNVERIFIABLE` cases become `INVALID` under the
literal A3.2 reading, not the reverse — `RESULTS-PROBE.md` §C3 says
so); and C8(a)'s count (three of the six equalities are already carried
by the shared tuple; three are new). Codex: "I would now consider the
batch ready for your substantive read, with that C3 correction."

> Yes—the revision addresses the substantive concerns. It now presents C8 as an actual framing decision, adds the degraded-mode boundary as C11, preserves the observations needed by an adjudicator in C4, and separates header honesty from coverage in C5.
>
> One factual wording error remains in C3, line 273 (formal/suite/ROUTED-2026-09-06.md:273):
>
> > "turns the verdict INVALID, and some cases become UNVERIFIABLE."
>
> The direction is reversed. The supporting probe says cases that are UNVERIFIABLE under P4 become INVALID under the literal A3.2 reading. A precise replacement is:
>
> > The literal A3.2 reading changes some cases from VALID_DEGRADED or UNVERIFIABLE to INVALID when waived evidence fails.
>
> That correction does not change the recommendation.
>
> C8(a) is now coherent with the current model: common content and matching non-fingerprint fields, with each signer retaining its own fingerprint. Three equalities—algorithm, identity, and manifest hash—are already enforced through the shared tuple, so "six equalities" describes the intended relationship rather than six necessarily new checks.
>
> I would now consider the batch ready for your substantive read, with that C3 correction. This is an assessment of the revised proposals; the model changes and their validation still follow your decisions.

## Third pass — verbatim, with dispositions

The author went back a third time ("because I only get one cold
read"). All four sentences repaired in the routed file the same day:
(1) C5's status promise replaced — a yes completes the header review;
rows move to `checked` only when their other recorded prerequisites
hold (verified against `formal/suite/s-p2/RESULTS.md` "Status toward
discharge", which names the C8 ruling and the `Accept` ↔ P4 agreement);
(2) C11's recommended qualifier replaced with Codex's clearer wording,
with the reason recorded; (3) C3 "not consulted" → "do not determine
the verdict"; (4) C8's recommendation count → three new equalities.

> Not entirely. My previous "ready for your read" was premature. The main technical objections are addressed, including C3's direction error, but I found two remaining substantive wording problems and two smaller inconsistencies.
>
> 1. C5 promises a status change its supporting record does not authorize.
>
> The routed file (formal/suite/ROUTED-2026-09-06.md:423) says a yes on C5 moves all four properties to checked.
>
> But S-P2's results (formal/suite/s-p2/RESULTS.md:370) explicitly require the C8 ruling and agreement with the TLA+ leg through the documented Accept ↔ P4 connection. Header approval alone is insufficient.
>
> Replace that promise with:
>
> > A yes on C5 completes the author's header review. Each tracker row moves to checked only when its other recorded prerequisites are satisfied.
>
> 2. C11 carries an ambiguity from my own proposed wording.
>
> "Failures of the remaining required checks are defects" could mean that discovering an invalid signature is a construction defect. It isn't; correctly reporting that failure is intended behavior.
>
> A clearer replacement is:
>
> > Only losses permitted by the registered waiver rules and the declared policy are degradation costs. A degraded label does not excuse violating a non-waivable requirement or misreporting a required check's outcome.
>
> This also explicitly prevents a declared policy from waiving the final evidence chain.
>
> Two smaller repairs would remove avoidable confusion:
>
> - C3: "waived checks are not consulted" should say "waived checks do not determine the verdict." C4 proposes evaluating and recording them.
> - C8: its recommendation still says "costs six equalities," although the revised explanation correctly identifies three additional equalities. Change the recommendation to match.
>
> Otherwise, the original objections are answered: C8 identical frames impossible for distinct signer fingerprints — corrected; C3 divergence set and availability consequence — corrected, including direction; C4 observations bounded by available inputs — addressed; C11 degraded mode cannot excuse every failure — intent addressed, wording refinement needed; C5 header honesty differs from coverage — distinction addressed; status promise still needs correction.
>
> These findings come from rereading the current documents and supporting code, not rerunning the proofs. I haven't edited anything. I would resolve these four sentences before your cold read.
