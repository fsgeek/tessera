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
