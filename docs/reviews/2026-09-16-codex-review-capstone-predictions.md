# Codex non-author review of the capstone registration, first round (2026-09-15/16)

Reviewer: OpenAI Codex CLI (`gpt-6-astra`), run non-interactively by the
owner instance against the whole of `formal/suite/capstone/PREDICTIONS.md`
(first draft after the skeptic read and the companion additions; scratch
diagnostics on family-model copies under
`/tmp/tessera-capstone-review-wd6lw_kf/`). The reviewer found the
registration not ready to freeze. Every factual claim below was checked
against the tree before disposition. No capstone model exists; nothing
in the repository was run.

## Dispositions (owner instance, 2026-09-16)

1. **D7 omits its common-content consumer and companion.** ACCEPTED. Removing the three content equalities makes `Spliced` reachable while all three completeness correspondences stay true, so links 2a/2b cannot carry the common-content fact. D7's contract gains link 5's common-content conjunct as a consumer and a companion severing content agreement (a spliced-payload mutation) whose expected red is on link 5 and `Spliced`.
2. **C-C8-i is impossible as stated.** ACCEPTED. C-Q9 demands `checksign(ppf, kX) = (POSS, t)`; a fingerprint-only possession proof falsifies it by construction (C-Q9 false, `SetAltered` true, witnesses reachable). The isolation configurations are restated: joint protection of **set integrity** (`SetAltered`, combined removal) is one obligation; the exact **possession-message relation** (C-Q9) is another, already falsified by possession unbinding alone. C-C8-i is replaced by an isolation configuration that keeps possession over the manifest and removes only the frame's manifest-hash guard; the post-freeze amendment the file prescribed at `:1148-1158` is withdrawn as unnecessary.
3. **C-C15(i)'s retained set contradicts its mutation and the tree.** ACCEPTED. S-P7's Q6b source declares and emits `Reattributed`, and its recorded audit shows restoring the query makes Q6b red; the DSKS trace also violates link 5's frame-to-accepting-key equality. C-C15(i)'s retained set drops `Reattributed` and link 5; its evidential basis is corrected to `sp7_q6b_companion_key_outermost.pv:75-91` and `s-p7/RESULTS.md:58-71`.
4. **C-Q6 does not specify the event arguments or shared terms of its composition join.** ACCEPTED. The registration must fix the `EstablishedWrapped` signature and emission contract tying the standing report to the same wrapped presentation, its innermost key, the evidenced tuple and the attempt core; the representation mapping between S-P7's `(fbI, sgI)` extracted from `wrap(...)` and S-STANDING's identity derived from `attemptCore(t, ppf, sg, decl)`; the equalities that exclude attribution-for-A with standing-for-B; and the honest-key and unrestricted forms in strict and degraded mode (C-C12's conjunct statement is reconciled with C-Q6's). D11/D12/D13's consumption is not frozen until that is written.
5. **C-Q5 omits S-P2's one-key/one-manifest fixture restriction.** ACCEPTED. `MemberJudge` needs each honest key to sign exactly one manifest, which S-P2 registers (`s-p2/PREDICTIONS.md:201-214`, `RESULTS.md:444-447`); sharing slot A's key across the two honest manifests makes `SetAltered` reachable with no verifier change. The capstone fixture states the key assignment explicitly, or registers a provenance correspondence in its place.
6. **The "every other choice is determined" sentence at `:835-837` is withdrawn**; findings 4 and 5 were builder choices. The `REFUSAL` fork stands as the one routed item.

**Loop.** One repair pass with scratch runs, then one more owner-run Codex pass; the file goes to the author for the freeze commit only when the reviewer says it is ready or its remaining findings are, in the owner's judgement, things the build itself must decide.

## Codex review — verbatim

## 1. Query strength and discharge

**1. D7’s discharge row omits its common-content consumer and severing companion.**

D7 names `Spliced` among its producers, but lists only links 2a/2b as consumers and C-C9 as companion. Those links establish membership and completeness, not agreement between signers’ content. Link 5 explicitly consumes that agreement, yet its companions C-C2/C-C4/C-C8 remove key or manifest bindings while retaining content agreement. (`formal/suite/capstone/PREDICTIONS.md:693`, `:291–301`, `:592–598`.)

I removed the three content equalities from a copy of the existing slot-completeness diagnostic. `Spliced` became reachable; **all three completeness correspondences remained true**, with honest witnesses reachable. (`/tmp/tessera-capstone-review-wd6lw_kf/slots_content_unchecked.out:1337`, `:1366`, `:1381`, `:1396`, `:657`, `:886`.)

**Required repair:** include link 5’s common-content conjunct in D7’s discharge contract and register a companion severing that fact. A red on link 5’s key-binding half cannot substitute for this obligation. A3.3 requires failure of the query consuming the severed link. (`docs/phase-0-prereg-amendment-3.md:220–230`.)

## 2. Companion consistency

**2. C-C8-i cannot preserve C-Q9 while accepting fingerprint-only possession proofs.**

C-Q9 demands `checksign(ppf, kX) = (POSS, t)`. C-C8-i instead accepts `(POSS, fp(kX))`, while requiring C-Q9 green and honest acceptance reachable. The retained frame hash cannot change the message recovered from the possession signature. (`formal/suite/capstone/PREDICTIONS.md:491–501`, `:1145`.)

On a copy of the cited C-Q9 baseline, I changed only possession production and verification to fingerprint-only form. Results:

- C-Q9: **false**, against **true** in the baseline.
- `SetAltered`: still **true**.
- Both `HonestComplete` witnesses and `HonestAccepted`: reachable.

Evidence: `/tmp/tessera-capstone-review-wd6lw_kf/cc8_i.out:1263`, `:471`, `:643`, `:861`, `:1090`; baseline `base.out:1111`.

**Required repair:** distinguish joint protection of **set integrity** from the exact **possession-message relation**. The former needs combined removal in this fixture; the latter already fails after possession unbinding alone. The mandatory post-freeze amendment prescribed at `formal/suite/capstone/PREDICTIONS.md:1148–1158` is avoidable: this contradiction is established before freeze.

**3. C-C15(i)’s retained key-binding guarantees contradict its mutation and existing evidence.**

C-C15 requires `Reattributed` and link 5 green while verifying an honest inner signature under the wrapper key and dropping the inner fingerprint/hash matches. It also says the source models do not declare `Reattributed`. (`formal/suite/capstone/PREDICTIONS.md:1111`.)

The source **does declare and emit** that event. Its recorded audit already establishes that restoring the query makes Q6b **red**. (`formal/suite/s-p7/proverif/sp7_q6b_companion_key_outermost.pv:75–91`; `formal/suite/s-p7/RESULTS.md:58–71`.)

I restored only the query on a copy: `Reattributed` was reachable, with both honest witnesses reachable. (`/tmp/tessera-capstone-review-wd6lw_kf/cc15_i.out:1788`, `:1317`, `:1508`.) The DSKS trace accepts honest inner bytes under another key; their embedded fingerprint therefore also violates link 5’s frame-to-accepting-key equality. (`formal/suite/s-p7/proverif/sp7_q6b_companion_key_outermost.pv:192–199`; `formal/suite/capstone/PREDICTIONS.md:291–296`.)

**Required repair:** correct the retained set and its claimed evidential basis. Preserved type soundness does not imply preserved key binding.

## 3. Prediction bases

Finding **3** is a prediction contradicted by evidence already in the tree, not merely an uncertain composition prediction. Finding **2** is an impossible required combination under the stated query and live-witness requirement. Neither should be deferred to post-freeze “recut” uncertainty.

## 4. Builder-ready contracts

**4. C-Q6 does not specify the event arguments or shared terms establishing its central composition join.**

The registration gives only `EstablishedWrapped ⟹ Designated` and `StandingUnentitled`, without an `EstablishedWrapped` signature or emission contract tying the report to the same wrapped presentation, its innermost key, tuple and attempt core. (`formal/suite/capstone/PREDICTIONS.md:412–420`.)

This is substantive: S-P7 extracts `(fbI, sgI)` from `wrap(...)`; S-STANDING derives identity from `attemptCore(t, ppf, sg, decl)`. The registration does not fix how those representations are connected. (`formal/suite/s-p7/proverif/sp7_q2_degraded_compromised.pv:317–334`; `formal/suite/s-standing/proverif/ss_q1_strict_dns_compromised.pv:352–385`.)

Independently valid wrapper attribution for artifact A and independently valid standing evidence for artifact B can satisfy the two family checks. C-Q6 needs shared arguments and equality requirements that exclude precisely that substitution. Simply naming the standing event `EstablishedWrapped` supplies no such binding.

There is also an unresolved quantifier choice: C-Q6’s sentence is unrestricted in strict mode, while C-C12 says its standing conjunct is **not** unrestricted and relies on honest-key forms. (`formal/suite/capstone/PREDICTIONS.md:413–426`, `:627`.)

**Required repair:** register the complete correspondence, report contract, representation mapping and honest-key/unrestricted forms before freezing D11/D12/D13’s consumption.

**5. C-Q5 omits the fixture restriction required by its inherited judge.**

`MemberJudge` detects acceptance under a manifest **different from one observed honest manifest**; it cannot detect that the key **never signed** the accepted manifest unless each honest key signs exactly one manifest. S-P2 explicitly registers that restriction and records a key-reuse false positive. The capstone does not preserve it or specify the one-signer manifest’s key assignment. (`formal/suite/capstone/PREDICTIONS.md:64–66`, `:391–397`; `formal/suite/s-p2/PREDICTIONS.md:201–214`; `formal/suite/s-p2/RESULTS.md:444–447`.)

Sharing slot A’s honest key between the two honestly signed manifests makes `SetAltered` reachable with **no verifier change**, while exact possession binding and honest witnesses remain intact. (`/tmp/tessera-capstone-review-wd6lw_kf/shared_slot_a.out:644`, `:1284`, `:816`, `:1034`.)

**Required repair:** specify the one-key/one-manifest fixture mapping, or register a correspondence expressing actual signing provenance.

## 5. Routed and hidden choices

The **REFUSAL fork is genuine and presents both options and costs**: exercise the domain with an additional signer/companion, or retain declared-and-unexercised status and leave that test unavailable. I do not resolve it. (`formal/suite/capstone/PREDICTIONS.md:805–825`; `formal/suite/lib/tessera_theory.pvl:66–76`.)

However, the assertion that every other choice is determined is premature: findings **4–5** leave consequential query and fixture choices to the builder. (`formal/suite/capstone/PREDICTIONS.md:835–837`.)

## 6. Carried-forward corrections

All three are honoured:

- **Exact bytes without authorship overclaim:** C-Q8 is structural, unrestricted by honest origin, and includes verification failure. (`formal/suite/capstone/PREDICTIONS.md:470–484`.)
- **Link 1b as correspondence:** publication provenance is excluded from `ChainBroken`. (`:210–225`.)
- **Fresh acceptance identifier:** one fresh name per acceptance, shared across its slots, followed by `AcceptanceComplete`. (`:115–130`.)

**This registration is not ready to freeze. The author should see first: finding 4, the unspecified wrapped-standing join; finding 2, the impossible C-C8-i isolation requirement; and finding 1, D7’s missing common-content discharge companion. These are registration defects. The probes used family-model copies under `/tmp`; no capstone model was built and no repository file was changed.**

