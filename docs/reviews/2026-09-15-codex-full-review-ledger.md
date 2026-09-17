# Codex non-author full review of the ledger register, second round (2026-09-15)

Reviewer: OpenAI Codex CLI (`gpt-6-astra`), run by the author in his own
session against the whole of `formal/suite/LEDGER.md` (the 2026-09-14
repaired draft, uncommitted), with one targeted diagnostic on a copy of
the S-P7 model; the author pasted the answer to the owner instance with
the note that he had asked for a full review "not just the subset of
lines you requested". The reviewer would not yet approve the register
as the capstone plan. Every factual claim below was checked against the
tree before disposition.

## Dispositions (owner instance, 2026-09-15)

**Process finding first.** The owner routed only §5 to the author and
did not run a full non-author pass on the document before routing.
From this review on, a document goes to the author only after a full
Codex pass run by the owner and a full skeptic read; the author's read
stays as short as the record allows, the reviewer's does not.

1. **D5 names an insufficient producer fact.** ACCEPTED. The reviewer added an explicit honest-key authorship query to a copy of S-P7 and a mutation that keeps byte binding when the signature's embedded fingerprint matches the verification key and permits unbinding otherwise: authorship held, `InnerSigTransplanted` became reachable, honest witnesses stayed reachable. So S-P1's narrower theorem ("honest-key acceptance implies those bytes were signed") does not supply what S-P7's consumer needs, which is the signature-to-presented-bytes relation under the presented key. Repair: L-06/D5 name that exact relation; identify or register a producer that establishes it; D5 stays provisional until the argument is explicit; C-C5 is retagged as showing that byte binding matters, not as the discharge.
2. **L-07's global key-use rule contradicts S-STANDING's `sign((TLR, body), skI)`.** ACCEPTED. The whitelist is incomplete: the issuer key legitimately signs framed objects under `BYTES`, the manifest under `POSS`, terminal lineage records under `TLR`, and refusal records under `REFUSAL` (library D-6). Repair: enumerate the permitted signing domains and message shapes from the library's tags and state that their domain separation is what the composition must preserve.
3. **L-09 promises common content without naming the query that establishes it.** ACCEPTED. The producer row gains S-P2 Q6's `Spliced` unreachability (green as registered, 2026-09-12) with its shared-term mapping; authorship stays with L-06.
4. **Ruling consequences not propagated.** ACCEPTED. D1 and D2 become provisional on R-2 (not firm); R-3's consequences for L-16/L-17 are stated as depending on the composition query's formulation; R-1's argument no longer cites D5.
5. **Companion instructions contradict their evidence.** ACCEPTED. §6's "exactly its named query" is replaced by, per companion: expected failed-query set, retained guarantees, required witnesses. C-C2 is the minimal two-removal mutation (frame pin + manifest hash), since the three-removal alternative reds `SignerForged`, which the register requires green.
6. **"Layer 2 forever" includes internal obligations.** ACCEPTED. The classification distinguishes permanent external assumptions (primitive security, trust-anchor history, chain availability, implementation fidelity, operational channel independence) from internal proof obligations currently carried as assumptions (canonical encoding pre-P8; the §A3.7.2 invariant pre-E6), each of which cites the exit item that will discharge it.

**On the three decisions.** The reviewer's recommendations coincide with the owner's: R-1 requires an exact producer-to-consumer argument per row (copied code settles nothing); R-2 represents and tests both routes; R-3 builds the composition query and derives its dependencies from it. The author's confirm/overrule is deferred until the repaired register has passed a full skeptic read and a full Codex pass run by the owner.

## Codex review — verbatim (as pasted by the author)

> Reviewing the whole document was worthwhile. I would request another repair before approving it as the capstone plan. The earlier fingerprint-removal error is corrected, but several dependencies and instructions remain inconsistent.
>
> 1. D5 still names an insufficient producer fact.
> L-06 (formal/suite/LEDGER.md:250) claims S-P1's honest-key authorship correspondence supplies what S-P7's InnerSigTransplanted query needs.
>
> I tested that distinction directly. Starting from the current S-P7 model, I added an explicit honest-key authorship query and a diagnostic mutation that preserves byte binding when the signature's embedded fingerprint matches the verification key, but permits unbinding otherwise.
>
> The results were:
>
> | Check | Baseline | Diagnostic |
> |---|---|---|
> | Honest-key acceptance implies those bytes were signed | Holds | Holds |
> | Signature transplant unreachable | Holds | Fails |
> | Both honest-acceptance witnesses | Reachable | Reachable |
>
> This shows that the named authorship claim can hold while the consumer claim fails. The revised C-C5 demonstrates that byte binding matters, but does not establish that S-P1's narrower theorem supplies the needed fact.
>
> Repair: name the exact signature-to-presented-bytes relation the consumer requires, and identify or register a producer that establishes it. Keep D5 provisional until that argument is explicit. Diagnostic files and outputs (/tmp/tessera-ledger-full-review-tljucfnr)
>
> 2. The global key-use rule contradicts S-STANDING's legitimate signing behavior.
> L-07 (formal/suite/LEDGER.md:269) says an issuer key signs only framed objects under BYTES, plus its manifest under POSS, "at any endpoint anywhere in the system."
>
> But S-STANDING signs:
>
> sign((TLR, body), skI)
>
> using that issuer key. The literal global restriction cannot hold in the composed fixture.
>
> Repair: enumerate the permitted signing domains and message shapes, including TLRs, and establish that their composition preserves the claimed separation. The underlying concern—preventing unrestricted signing endpoints—is sound; the current whitelist is incomplete.
>
> 3. L-09 promises common content without naming the query that establishes it.
> L-09 (formal/suite/LEDGER.md:297) includes "every required signer's frame over the same content," but its producer row names only Stripped and SignerForged.
>
> Those queries do not establish common content; that was precisely the C8 finding. The record now has Spliced, but lists its broken companion without adding the corresponding correct-model result to the producer.
>
> Repair: include the Spliced unreachability result and its shared-term mapping in L-09/D7. Keep authorship separately supplied by L-06.
>
> 4. The ruling consequences are not consistently propagated.
>
> - R-2 says its answer determines D1 and D2, but the matrix still counts them among nine firm rows.
> - If R-3 adds a query combining wrapper processing with standing, the ledger must reconsider L-16/L-17, currently classified complementary because they lack a symbolic consumer. The new query may consume their standing guarantees as well as S-P7's scope guarantee. Its precise formulation should determine those dependencies.
> - R-1 still uses D5's disputed authorship dependency as evidence for its recommended interpretation.
>
> These matter because you should be approving a clear consequence, not a classification whose meaning changes elsewhere in the document.
>
> 5. The companion instructions contradict their own evidence.
> Section 6 (formal/suite/LEDGER.md:667) requires each companion to fail "exactly its named query," while C-C4 explicitly fails three queries.
>
> C-C2 also permits removing all three bindings while requiring SignerForged to remain green—even though the matrix records that this alternative makes SignerForged red.
>
> Repair: specify each companion's expected set of failed queries, retained guarantees, and required witnesses. For C-C2, select the minimal two-removal mutation if the stated retained guarantees are required.
>
> 6. "Layer 2 forever" incorrectly includes temporarily unproved encoding obligations.
> The classification table (formal/suite/LEDGER.md:68) says these assumptions remain unclaimed "forever," while including canonical encoding pre-P8. Elsewhere, the ledger correctly says the encoding entry should cite P8's proof when available.
>
> Repair: distinguish permanent external assumptions from internal proof obligations currently treated as assumptions. Otherwise, the ledger risks permanently exempting work the project explicitly owes.
>
> My recommendations on the three decisions remain:
>
> - R-1: copied code alone does not settle dependency classification; require the exact producer-to-consumer argument.
> - R-2: represent and test both redundant routes explicitly.
> - R-3: build the wrapped-standing composition query and derive its dependencies from that query.
>
> The document is becoming a useful map of the remaining work. These findings concern the accuracy of that map; they do not show that the underlying Tessera construction is broken. I reviewed the full ledger and ran the targeted diagnostic above; I changed no repository files.
