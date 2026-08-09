# Travelog

This is a contemporaneous journal of the work I've done in building this project.

## June 10, 2026

This was the initiation of the project.  The basic goal is to build an AWS-based
attestation service that has a similar service guarantee as [Willay](https://github.com/fsgeek/willay).

The purpose of an attestation service is to provide a third party verification of specific artifacts. What it doesn't do is
say anything about the authenticity of those document, including signature, or contents.  Such additional guarantees can be provided as part of an attestation package.  The key to recall here is that attestation says _this is what was presented in a bundle_ and it ties it to a particular timestamp (the _temporal anchor_) in such a way that the timestamp cannot be trivially regenerated.

At some point I should explain the cryptographic chain within this project but for now I'm going to lean on Willay for that documentation.

### Founding

Today was about setting up infrastructure.  Note that the repository is set up for code signing with OTS signed timestamps that anchor the work into the record (and Claude insists I point out these are two mechanisms, one that establishes _who_ and the other _when_).  We've decided to implement a CI/CD pipeline, with all changes at some point (soon) done via PRs - no check-ins to main.  Github issues will be used to track work.

## July 5, 2026

Finally got back to this.  Spent yesterday pushing forward on the formal side of things. Interestingly enough, we'd agreed to use ProVerif for proofs only for me to read that there is now an active CVE against the variout TEEs because the bugs in the IETF attestation protocol itself is fundamentally incorrect (e.g., it validated connection, but not intermediate run-time state.  See CVE‑2026‑33697 as well as current conversations about the issues in remote attestation.)

It was interesting to me (at least) because key management is one of the things to which we pointed and said "oh, we can just use a TEE" but this work suggests that's not guaranteed, at least for now.  ProVerif was used to demonstrate that the current attestation is itself not meeting the security guarantees afforded the work; that doesn't mean using it will make our work correct (the model still needs to be done) but it speaks well to the broader applicability.

### Formal Work

The formal work is proceeding.  In addition to the ProVerif proofs, we are also working on TLA+ proofs. The former help establish state-related correctness and TLA+ helps establish temporal-related correctness; or at least that's the argument.  I continue to use multi-round adversarial review, including codex (ChatGPT-5.5) and gemini (agy-cli with gemini flash 3.5) plus my own manual review of the models.

## July 7, 2026

Back looking at this.  The honest challenge here is that I really am playing the role of "principle investigator" where I understand the goals and objectives, but when it comes to the specifics of the implementation I need to parse what's being asked.  This is slow going because I have to ask dumb questions and clarify things.  So, for example I get the following feedback after I model the questions in P5c: "Net assessment: keep the policy, with three repairs — mirror the strict rule into the verification predicate (chain timestamps make this possible), give the retry loop a fail-closed terminal state or an explicit liveness disclaimer, and bind receipts to their anchor txid while confining declared times to existed-by semantics. With those, the P5c strict modeling you'd be ratifying matches what verifiers actually enforce, which is the alignment that matters."  I then vote to adopt the revised protocol and get back this comment from left field: "Yes — with one point pinned down explicitly, because my "revised version" left an either/or open in repair 2, and a ratification needs definite text. Let me first look at how the registered text and the P5c fork flag currently read, so the ratified policy lands in the right places."

So I go re-read the commentary and wonder if I'm being sandbagged by the brilliant researcher - "um, what either/or open in repair 2?"  Then I see the landmine  "... a fail-closed terminal state or an explicit liveness disclaimer..." - which read to me like an implementation decision but was a hidden policy decision.  Then I think "I'm reading the FLP proof again, and the 'kick the can down the road' construction."

Then I get my favorite part - the "ask the ~~idiot~~ human a question" tool:

Which form of the strict confirmation policy should Amendment 2 register?

```
1. A: Symmetric chain-time predicate (Recommended)
     "Confirmed within δ" = timestamp(block h+k−1) ≤ declared+δ, checked identically by issuer at ship and verifier at verification. Exact model↔verifier correspondence; abandoned-anchor artifacts rejected; requires k headers in evidence, non-waivable.

2. B: Issuer-only strict + scope statement
     Your policy verbatim; verifier keeps block-time-only checks. Registered text explicitly demotes the ship rule to issuer-side hygiene (NoShippedOrphan + freshness); duplicate-receipt residue handled by txid binding alone.

3. Type something.
```

I'd say about 80% of the time what I am given isn't really a set of disjoint options, its a weird ordering issue or one clear issue with multiple distractors. The irony is that the current AI coding agents seem to make this sort of exploration as painful as possible.

## August 8, 2026

Clearly I'm not doing a good job of keeping this updated.  The progress has been slow for the past while.  I think we're still in various rounds of amending the protocol.  Today I expressed a concern that at some point planning becomes an excuse to avoid implementing.  Having said that, I must also admit that this project, while conceptually simple, is trying to demonstrate a challenging principle - trying to produce a service that is honest about its abilities and limitations. The infrastructure seeks to embody these ideas, but in the end, I'm also looking forward to building it. Most people will never look at this side of the service we're building, but it is an important piece of it.

### Addendum 16:51 PT

I took the entire package - P0 preregistration + 3 amendments, and handed them to four cold models: KIMI 2.6, Deepseek V4, Grok 4.5, and Gemini Flash 3.7.  Those have been saved in the project and handed to Claude for analysis.   Gemini at least identified "fatal issues" that sounded more like implementation concerns than design concerns, but I'll see what the verdict is.

### Addendum 17:26 PT

I was asked one specific question and rather than just answer it I chose to explore:

Claude: That leaves exactly one ruling before signature: Kimi 2, the integrated lifecycle model, as a Band 0 exit obligation — yes or no.

Tony: So, rather than decide right now, I'll ask you to give me the three best arguments for making the integrated lifecycle model as a Band 0 exit obligation, and then the three best arguments for not making the integrated lifecycle model as a Band 0 exit obligation.  Then, I'm going to ask you to pick a low probability argument against each of those two positions.  For each of those low probability completions ask if it changes the way you look at the claim; if it doesn't, look for an additional candidate completion against that has p ~ 0.5 times the prior completion.  Repeat this until you find one that does change the way you look at the claim - that's where you stop.  Once you have the set of 8 arguments (3 best for, 3 best against, 1 look changing against, 1 look changing for) let's consider them and see if we have a clear argument.

Claude:
> This is a genuinely good procedure — it forces me to search the low-probability tail instead of stopping at the arguments that come easily. Here is the full set, chains shown.

> Three best arguments FOR (Band 0 exit obligation)

> F1 — Composition is where this project's real failure modes have actually lived. The bridge finding was an interaction fault between two models' clock abstractions. The checkmark relay is a composition failure between verification and rendering. The two-worlds attack composes channels. Per-property models each hold their own invariant while the adversary walks a seam between them; the capstone ledger records assumptions at joins but cannot exhibit an attack trace that threads several stages. §8's own words are "proving our own composition" — an integrated adversarial model is the most literal reading of the registered gate, not an addition to it.

> F2 — The cost asymmetry favors before-freeze. An interaction fault discovered after the crypto core freezes forces an amendment against frozen bands or a silent model/implementation divergence — both far costlier than one more model now. And the marginal cost is bounded: the integrated model composes state machines the per-property work already defines; it invents nothing.

> F3 — Standing is A3's newest dimension and is only adversarially exercised in composition. Its entire threat model is cross-stage: an artifact from issuance, laundered through wrapping, presented at verification. No per-property model ever sees that path. Exiting Band 0 with standing's mechanism chosen but never composed against the wrapper means exiting with the least-tested dimension untested exactly where it's weakest.

> Three best arguments AGAINST

> A1 — Gate creep is the theater failure mode wearing rigor's clothes. H0 was set "rigorous and achievable in our control." There is always one more composition worth checking; a gate that absorbs every good suggestion becomes unreachable, and your own diagnosis this week is that the spec stays pristine because nothing can fail. Accepting a panel singleton into H0 sets the precedent that reviews expand the gate.

> A2 — The integrated model may be uncheckable, and its failure mode is ambiguous. Six composed stages plus the A1.3 adversary is where symbolic tools blow up. Under the registered three-outcome discipline, a timeout is "mechanism failure, not property evidence" — so this obligation risks buying an unfalsifiable artifact that blocks the runway while teaching nothing. The per-property-plus-ledger design was chosen to keep every query inside checkable bounds; this un-chooses it.

> A3 — The named attack may be coverable far more cheaply. The transplant is one trace. A targeted companion on the P7 wrapper model ("standing binds to innermost issuance identity; a wrapper cannot re-scope it") plus a ledger entry connecting P7 to A3.7.1 might kill the named threat without buying full lifecycle generality nobody has shown is needed.

> Chain 1 — low-probability arguments against the FOR position

> - 1a (low p): a green integrated model creates false confidence about the implementation's composition — the model-to-code gap is largest where the model is most impressive. No change: that gap is an already-named residual applying to every model equally; the project explicitly refuses to let green models claim implementation safety.
> - 1b (p ≈ half of 1a): Kimi 2 is a singleton from one reviewer while the panel's convergence all points at the spike; elevating it weights one model's taste over four models' agreement. No change: singletons can be right — Kimi's addendum singleton was source-confirmed hours ago. Provenance isn't merit.
> - 1c (p ≈ half again) — stops the chain: The integrated model cannot be written until the standing and first-link mechanisms are chosen — both of which are outputs of the spike. As a Band 0 exit obligation it is therefore necessarily the last model written, sitting at the end of the critical path, and every mechanism wobble the spike produces re-opens it. The obligation's real content would be: "the runway opens only after a model that depends on every currently-open choice successfully composes them all." This changes how I look at the claim — the question stops being whether the model is valuable (it is) and becomes where it sits: gate obligations should not be maximally sensitive to decisions the gate's own process hasn't made yet.

> Chain 2 — low-probability arguments against the AGAINST position

> - 2a (low p): the blowup fear is pattern-matched from equivalence queries, which the integrated model doesn't need — reachability and correspondence queries suffice for the transplant companion, and the stages are sequential with small per-stage state. No change: plausible but speculative until the spike; it weakens A2 without flipping anything.
> - 2b (p ≈ half) — stops the chain: A3's "cheap targeted companion" is a checkmark relay between models. Checking "standing binds to innermost identity" on the P7 model alone assumes P7's abstraction of standing matches the standing mechanism's actual evidence object — a cross-model correspondence claim asserted in prose, exactly the class of claim the bridge finding proved can silently diverge, and exactly what four reviewers did to the Ship action yesterday. The only non-relayed check of a cross-model claim is a model that contains both sides. This changes how I look at the claim — the cheap alternative stops looking safe, because it reproduces, at the formal layer, the precise failure pattern this project keeps catching everywhere else.

> Do we have a clear argument?

> I think we do, because the two look-changers don't collide — they answer different questions, and together they dictate a placement neither pure position saw:

> 1c says: not at the gate. The model depends on every open mechanism choice; putting it in H0 makes the gate hostage to decisions H0's own process hasn't made.
> 2b says: not optional either. The cheap substitute is structurally unsound; the integrated model is the only non-relayed check of the one genuinely cross-cutting new dimension.

> The synthesis: register the integrated lifecycle model as a mandatory obligation triggered after the spike and gating the H1a crypto-core freeze — not Band 0 exit. The runway commit happens on the current H0 terms; the spike fixes the mechanisms; the integrated model then composes real chosen mechanisms rather than placeholders; and nothing freezes until it's green or its timeout is disposed by amendment. That preserves F2's cost asymmetry (it lands before anything freezes), honors 2b (it exists and is mandatory), respects A1 (H0 doesn't grow), and defuses A2's worst case (a timeout delays freeze, not the start of building). Since A3 is being signed anyway, it's one registered obligation with a declared trigger — no A4.

> That's my read of the eight. Your move — see a hole in the synthesis, or shall I draft the registration text?

Note that ultimately, the decision was that this is not a gate to P0, but it is work that will need to be addressed.

Thus, I've decided to sign off.

My biggest concern(s) right now are if the models still work, if they conform to the revised specification and - most importantly - if our _implementation_ of them implements the model.
