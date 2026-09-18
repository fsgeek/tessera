# Codex non-author review of the capstone registration, sixteenth round (2026-09-18) — the `REFUSAL` amendment

Reviewer: OpenAI Codex CLI (`gpt-6-astra`), `codex exec`, run
non-interactively by the owner instance on 2026-09-18 (22:06–22:25 UTC)
against the whole of `formal/suite/capstone/PREDICTIONS.md` as amended
(4246 lines) and a byte-exact pre-amendment copy, in parallel with a
full skeptic read. Subject: the author's ruling on the `REFUSAL` fork
(option (i), scoped) as entered — C-Q10, C-C18, the foreign-tag signer.
**Five findings, all accepted; two confirmations.** The reviewer re-ran
all six `cap27` copies (**all 76 `RESULT` lines at their archived line
numbers**), built one counterexample of his own under `/tmp` (two runs,
reproduced on our tree as `cap27g`/`cap27h`), and found the scoping
honest: *“No refusal-record claim is smuggled into the fixture.”*
Verdict: *“not yet ready to freeze as written”* pending three
corrections; *“The scoped ruling itself needs no reopening.”*

## Dispositions (owner instance, 2026-09-18)

All clerk dispositions; none touches a probability, a residual, a
timebox, the ruling or the four contestable choices.

1. **C-Q10 observes the `TLR` consumer only and must not be credited
   with six-tag separation** (finding 1, with a tested counterexample:
   on a copy of `cap27e` with only the envelope's `BYTES` tag equality
   removed, a `REFUSAL` signature is accepted as an attestation while
   C-Q10 stays green — which C-Q8's registered relation rejects).
   ACCEPTED. C-Q10's section now carries a **coverage statement**: it
   observes the tag the standing path parses on the lineage-record
   slot; the envelope's consumer is C-Q8's, the possession slot C-Q9's,
   the authority evidence link 1a's; separation across all six tags is
   carried by the four together, and C-C18 severs the `TLR` consumer
   only. The reviewer's two runs are reproduced byte for byte as
   `cap27g` (control) and `cap27h` (mutant) at his own `.out` line
   numbers (`:1859`/`:1865`; `:2016`/`:2022`), batch eighteen.
2. **C-C18's set (2) repeated the degraded link-1b accounting defect of
   round 13** (finding 2). ACCEPTED. Set (2) is now case-qualified:
   link 1b in (a) and (b) only; C-Q2 in (a) and (b) only; the strict
   authorship query in (a) and (b) with the unrestricted degraded form
   registered red already.
3. **The six runs, the causal attribution and the Cases cell —
   confirmed** (finding 3). Recorded.
4. **No refusal-record claim smuggled; “opaque to every check” not
   literally true after tag unbinding** (finding 4). ACCEPTED: the
   fixture row and §8 item 1 now say “opaque while the tag check
   stands; under C-C18 read as a TLR's, never as a record's.”
5. **Live count statements** (finding 5): the two “26”s (also skeptic
   S-3) and C-C18's ordinal “fourth beyond the ledger's ten.” ACCEPTED;
   the ordinal now reads “the eighth beyond the ledger's ten numbered
   companions and, after C-C16 and C-C17, the third that no ledger line
   names.”
6. **Freeze compatibility and provenance — confirmed** (finding 6);
   **builder requirements supplied** (finding 7). Recorded.

**Round 17**, a confirmation pass on these repairs and the skeptic's,
follows before the author's commit.

## Codex review — verbatim

## 1. C-Q10’s claim and event contract

**1. C-Q10 observes the TLR consumer, not the entire six-tag property.** Its report contains the standing path’s parsed tag, compared only against `TLR`. That establishes a useful local property, but cannot alone establish separation across every signing domain named by the ledger. The broader attribution needs to identify the other consuming queries explicitly. (`formal/suite/capstone/PREDICTIONS.md:1416–1431`; `formal/suite/LEDGER.md:387–398`.)

**Tested counterexample:** on a `/tmp` copy of `cap27e`, I removed only the envelope’s `BYTES` tag equality, retaining signature verification, presented-byte binding, possession, authority evidence and frame checks. An attacker-held issuer key in degraded mode then supplies a `REFUSAL`-tagged signature that the envelope accepts as an attestation. C-Q10 remains green, with all thirteen original query polarities unchanged:

- Control: foreign-tag envelope acceptance unreachable; `TagConfused` unreachable. (`/tmp/tessera-round16-qba73enf/tag_scope_control.out:1859`, `:1865`.)
- Mutation: `EnvelopeForeignAccepted(k, REFUSAL)` reachable; `TagConfused` still unreachable. (`/tmp/tessera-round16-qba73enf/tag_scope_mutant.pv:388–401`; `/tmp/tessera-round16-qba73enf/tag_scope_mutant.out:2016`, `:2022`.)

This **does not evade the full registered ladder**: C-Q8’s specified relation rejects precisely that acceptance. The repair can therefore be an explicit coverage statement: C-Q10 covers foreign-tag consumption as TLR; C-Q8 covers `BYTES`, C-Q9 covers `POSS`, and link 1a covers authority evidence. Do not attribute their combined coverage to C-Q10 alone. I found no false-green escape through C-C18’s specified TLR parse when its actual parsed tag is faithfully reported. (`formal/suite/capstone/PREDICTIONS.md:1379–1389`, `:1400–1407`, `:330–346`.)

## 2. C-C18’s sets, causality and Cases cell

**2. Set (2) repeats the degraded link-1b accounting defect repaired in round 13.** It predicts green for “C-Q1 links 1a–6b” without excluding link 1b in case (d). But link 1b is unasserted there, and its correspondence already fails on an unmutated degraded baseline. It belongs in neither degraded companion set. Case-qualify this list; likewise retain the declared mode restrictions of C-Q2 and the strict authorship query rather than treating “every envelope-path query” as an all-case guarantee. (`formal/suite/capstone/PREDICTIONS.md:2643`, `:363–377`, `:3949`, `:3965`.)

**3. The cited severing results and strict/degraded descent are confirmed.** I reran all six `cap27a–f` copies under `/tmp` with ProVerif 2.05. All exited successfully; **all 76 `RESULT` lines, including their line numbers, matched the archives**. The registered result table accurately reports them. (`formal/suite/capstone/PREDICTIONS.md:4237–4242`.)

The strict and degraded control/mutant source pairs change only the tag equality and the report needed to preserve the actual parsed tag. The honest-key standing correspondence changes from green to red alongside `TagConfused`; the entitled-key and alias judges stay green, and the witnesses remain reachable. This supports the severed tag check as the cause, rather than merely observing an unrelated red. (`formal/suite/ledger-tests-2026-09-14/cap27c_ss_q1_strict_foreign_tag_correct.pv:386–389`; `formal/suite/ledger-tests-2026-09-14/cap27d_ss_q1_strict_foreign_tag_tlr_tag_unbound.pv:386–389`; `formal/suite/capstone/PREDICTIONS.md:2643`.)

The Cases cell correctly assigns **(a) descended from strict `cap27d`, (b) predicted by channel symmetry, (c) excluded, and (d) descended from degraded `cap27f`**. These remain family-copy results, not a run of the wrapped capstone join. (`formal/suite/capstone/PREDICTIONS.md:2643`, `:4244–4246`.)

## 3. Refusal-record scoping

**4. No refusal-record claim is smuggled into the fixture.** `ForeignIssuer` signs a deliberately TLR-shaped body over an adversary-chosen core. It introduces no refusal latch, durable-record creation, commitment creation, delivery state or publication state—the obligations that define A3 §A3.7.2 and E6. The narrow signing-domain exercise therefore does not incur the refusal-record modelling obligation. (`formal/suite/ledger-tests-2026-09-14/cap27c_ss_q1_strict_foreign_tag_correct.pv:456–465`; `docs/phase-0-prereg-amendment-3.md:569–610`; `formal/BAND0-EXIT.md:66`.)

“Opaque to every check” is not literally true of the attack: after tag unbinding, the standing path interprets its lineage and terminal fields **as a TLR**. That does not interpret or validate it as a refusal record. The substantive scoping statement—record, L2-n and E6 unclaimed—holds. (`formal/suite/capstone/PREDICTIONS.md:82`, `:1958–1966`, `:2643`.)

## 4. Counts and totals

**5. The arithmetic is correct, but live count statements remain inconsistent.**

- The table sums to **27 entries, 1185 minutes per case, 4740 minutes maximum**, and the companion count is **EIGHTEEN**. (`formal/suite/capstone/PREDICTIONS.md:1563–1587`, `:1810–1814`.)
- The operative observer-status paragraph still says “the **26** separately timeboxed entries.” (`formal/suite/capstone/PREDICTIONS.md:842–847`.)
- Outside the dated repair parenthetical, the operative budget explanation still says “**26 counts registered, separately timeboxed entries**.” (`formal/suite/capstone/PREDICTIONS.md:1605–1607`.)
- C-C18 calls itself “the **fourth** this file numbers beyond the ledger’s ten.” Eighteen minus ten is eight; the count paragraph identifies five transcribed companions and three further additions. (`formal/suite/capstone/PREDICTIONS.md:2628–2629`, `:1824–1839`.)

These need correction without rewriting historical totals.

## 5. Freeze and author-ruling provenance

**6. The amendment’s entry is compatible with the freeze discipline; it does not supply the outstanding review gates itself.** §8 still requires the author’s commit before capstone construction or execution, and the review log explicitly owes the amended-version skeptic read and non-author pass. The six diagnostics are identified as family copies, not capstone results. (`formal/suite/capstone/PREDICTIONS.md:1980–2001`, `:2180`, `:4223–4246`.)

The two author quotations are distinguished from the owner instance’s scoping explanation. I found no additional author decision attributed by the entry; its implementation details remain reviewable registration text. The four contestable choices remain contestable. The substantive inconsistency with an earlier repair is finding 2’s reintroduction of degraded link 1b into companion accounting. (`formal/suite/capstone/PREDICTIONS.md:2025–2059`, `:2135–2138`, `:3949`.)

## 6. Builder requirements

**7. The essential fixture and local wiring are supplied; no additional builder decision is needed for those points.** The signer uses **`skI` only**, runs in **(a), (b), (d)**, and supplies an adversary-chosen core through the cited signer construction. C-Q10 specifies a private parallel report and the event signature. Its cited implementation emits the report immediately after the signature/tag/body parse, before the anchor and tuple checks; the judge compares the reported tag against `TLR`. This preserves C-Q6’s independent standing path and does not require envelope acceptance. (`formal/suite/capstone/PREDICTIONS.md:82`, `:1416–1420`, `:903–913`; `formal/suite/ledger-tests-2026-09-14/cap27c_ss_q1_strict_foreign_tag_correct.pv:386–402`, `:471–473`.)

**The amended registration is not yet ready to freeze as written.** First correct C-C18’s case-qualified retained set and the live count errors, and make C-Q10’s limited contribution to six-tag separation explicit. The author should see the tested counterexample together with its crucial limit—it defeats C-Q10 alone, not the full ladder—and the confirmed C-C18 severing results. The scoped ruling itself needs no reopening; after these corrections and the amended-version review gates, readiness remains subject to the four contestable choices.
