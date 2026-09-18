# The freeze read — `formal/suite/capstone/PREDICTIONS.md` (2026-09-17; revised after a Codex read of the first draft; revised again 2026-09-18 after the author's `REFUSAL` ruling was entered)

*Written by the owner instance for the author. Revised the same evening
after the author had Codex review the first draft, which found the
choice inventory inconsistent with the registration's, the enrolment
summary misleading, the decision sequence wrong, and no plain-language
account of the experiment. All four are repaired here. Nothing in this
note is a ruling; the rulings are yours and are marked.*

## 1. What this experiment is for, in ordinary language

Five families of symbolic models have each been checked on their own:
the issuer's first link, multi-signer manifests, possession, wrappers,
and standing evidence. Each one **assumes** facts that another one
**proves**. The capstone is one ProVerif model that puts all their
checks into a single verifier and asks whether the facts still line up
when combined: every **ledgered cross-model assumption** — a fact one
family assumes and another must establish — must be discharged by the
query that proves it, and every such link must have a **deliberately
broken variant** that removes exactly that connection and makes the
consuming query fail. That is the exit gate Amendment 3 §A3.3 sets for
Band 0. The gate expressly leaves the **Layer 2 assumptions** unclaimed:
cryptographic primitive strength, historical trust-anchor correctness,
chain availability, implementation fidelity, and operational
independence of the authority channels are exposed in the ledger and
never discharged here.

**The scope is finite and small**, as §7 says: two authority channels,
signer sets of at most two, wrapper depth at most two, lineages of
exactly two attempts. Nothing here is a quantified result over larger
sizes.

**The adversary** is the symbolic one the families use: it controls the
network; in the strict cases it holds one of the two authority channel
keys (a separate broken variant leaks both, to show what that costs);
in the degraded case it holds the only channel's key; it can derive a
**new** key under which an existing signature verifies (the theory
excludes recovering the original key); and it chooses payloads. **What success would establish**: that the registered
composition holds within the symbolic model's limits, and that every
broken variant fails where predicted. **What it would not establish**:
concrete byte encodings (P8's proof), implementation fidelity, the
strength of real hash and signature algorithms, and the correspondence
to the TLA+ models. These stay outside the capstone: the encoding
proof, implementation fidelity and the TLA+ correspondence are separate
exit obligations still to be discharged; the strength of the real
algorithms is an explicit external assumption and is never discharged.
`PREDICTIONS.md:1955-2003` (§7, "What the capstone does not claim") says
this in the file's own words.

**The predictions are frozen before the model exists** so that nothing
can be tuned to the result. Your commit is the freeze.

## 2. The choices this file made, and their limits

The registration had to make **six** choices the ledger left open. They
are not all the same kind, and the first draft of this note listed only
four of them. Here is the whole inventory.

**Two are settled construction choices** (registration §8 items 1 and
2, `:2127-2150`); they are this file's, were reviewed in rounds one and
two, and are presented so you know their limits, not for approval:

- **The composition join** (`:2127`): how the wrapper family's extracted
  inner terms become the standing family's core. The file fixes the
  event, the emission contract, and five term equalities, so wrapper
  attribution for one artifact cannot be combined with standing
  evidence for another. A builder given no contract would have had to
  invent this.
- **One key, one manifest** (`:2142`, and `:674`): the multi-signer
  judge inherited from the manifest family only means what it claims if
  each honest key signs exactly one manifest. The fixture assigns keys
  that way. **Limit**: the set-integrity result (C-Q5) is conditional on
  that assignment; a key reused across manifests can make that judge
  fire with no verifier change. That is a limit on what the capstone
  measures, stated in the file.

**Four are contestable clerk choices**, taken by the owner instance
because a run showed the alternative changes results; each is marked
contestable in place and can be overruled by you without an amendment:

1. **Same-key wrapping** (`:79`; §8 item 3, `:2151`): the fixture lets
   an issuer key also sign a wrapper over its own attestation, as the
   wrapper family's fixture does. Taken for fidelity to that family.
   Consequence: two broken variants lose greens they had in the family
   runs, and one strict attack route exists in which an honest wrapper
   signature carries attacker attestation bytes past a **broken** inner
   check. The **correct** verifier's byte-exact check closes it; that
   check is load-bearing in the implementation spec (R-1.8, V19).
2. **"Adversary-enrolled" means compromised-channel enrolment only**
   (`:77`; §8 item 4, `:2164`). Read this one carefully, because the
   first draft made it sound like a security failure being excluded.
   It is a **measurement limitation**. The model's "the issuer signed
   it" event is emitted only by the honest issuer processes. If an
   adversary-held key were genuinely enrolled by uncompromised
   authorities, it would be an issuer to the verifier, and the broad
   "everything accepted was issuer-signed" assertion would fail while
   the honest-key assertion stayed intact. The file calls this what it
   is: not a defect of the design, but a fixture row that had not said
   which reading it meant. The reading taken is the one the wrapper
   family already uses in strict mode.
3. **In strict mode the evidence term is the pair, one per channel**
   (`:195-219`): the first-link query then requires each to verify
   under its own channel key, so deleting either check fails the link.
4. **The report contract under broken variants** (`:220-268`): every
   acceptance reports the terms it was about, never terms it happened
   to check at another layer, so a broken check cannot hide its
   failure. This made several more failures visible in one variant,
   all now registered.

**One clerical veto** (`:2087-2107`): the file puts the model at
`formal/suite/capstone/proverif/capstone.pv`, the layout every family
uses; the ledger says `formal/suite/capstone.pv`. Veto if you care.

## 3. The `REFUSAL` fork — ruled 2026-09-18, option (i), scoped

You ruled on 2026-09-18, and your words are entered verbatim under §8
item 1 (`:2030-2197`): **(i), reasonably scoped**. The scoping, mine and
accepted by you: the honest `REFUSAL`-tagged signer is a foreign-tag
source and nothing else; its body is opaque while the tag check stands;
nothing about the refusal record, the atomic-entry invariant or E6 is
modelled or claimed; `REFUSAL` is exercised as a signing domain and
unexercised as a record. The amendment that ruling called for is
**entered**: a new query **C-Q10**, the tag-separation judge
(`:1414-1483`, 615 words), a new companion **C-C18**, the tag check
unbound (`:2689-2753`), the signer's fixture row, and the totals (27
entries, 1185 minutes per case, eighteen companions). Eight scratch
runs descend it, two of them the round-16 reviewer's own counterexample
reproduced. The amended version went through a full skeptic read and
Codex rounds sixteen to eighteen the same evening; every finding was
clerical or a wording limit, all applied, and the ruling itself was not
reopened by any of them. **No item is routed to you any longer.**

**Your remaining decisions landed 2026-09-18**: all four contestable
choices confirmed, the path veto accepted with the clarification that
the model is identified by its contents (the builder records the blob
hash of `capstone.pv` in `RESULTS.md`). Both are entered under §8 in
your words. Nothing is owed from you before the commit but the commit.

## 4. The sequence, so no decision arrives too late

The reviews approved the file **as it stands**. Anything you change
must be entered before the commit that freezes it, and re-reviewed.

1. **Your decisions** — done 2026-09-18: the fork ruled (i) and
   re-reviewed (§3); the four choices confirmed; the veto accepted.
   All entered under §8 in your words; a confirmation needs no
   amendment and no further pass.
2. **Then the commit.** Your first commit containing
   `formal/suite/capstone/PREDICTIONS.md` freezes it (§8 freeze
   statement, `:2006-2029`). After it, the model is built by a builder
   who may not edit the file; results go to `RESULTS.md`; any change to
   a registered prediction is a dated amendment.

The freeze package, so `git add` is explicit rather than everything:

```
cd ~/projects/tessera
git add formal/suite/capstone/ \
        docs/reviews/2026-09-1[67]-codex-review-capstone-predictions*.md \
        docs/reviews/2026-09-17-codex-review-capstone-read-freeze.md \
        docs/reviews/2026-09-18-codex-review-capstone-predictions-round1[5-8].md \
        docs/reviews/2026-09-17-skeptic-read-capstone-predictions.md \
        docs/reviews/2026-09-18-skeptic-read-capstone-amendment.md \
        formal/suite/ledger-tests-2026-09-14/ \
        formal/suite/LEDGER.md \
        formal/BAND0-EXIT.md
git status --short   # expect: capstone/, 21 review records, the scratch archive, README, LEDGER, BAND0-EXIT (docs/band-1-docket.md stays for a separate commit)
git commit -m "Capstone registration frozen: PREDICTIONS.md after 18 non-author rounds and two skeptic reads, the REFUSAL ruling entered by amendment; review records; scratch archive batches 5-18"
```

The scratch archive's capstone batches, five to eighteen (`cap1`–`cap27`),
are 107 model copies and 22.5 MB of outputs (the directory as a whole
holds 138 models, the rest from the ledger's own repairs), every one a
copy of a committed family model with its mutation stated in its
header, none a capstone result. Stamp and push as usual.

## 5. The read itself

| # | Lines | What it is | Words |
|---|---|---|---|
| 1 | `:1955-2003` | §7 — what the capstone does not claim (now with the refusal-record bullet) | 402 |
| 2 | `:2006-2029` | §8 freeze statement — what your commit does | 224 |
| 3 | `:2030-2197` | §8 routed to the author — your ruling as entered, your confirmations, the veto, and the file's own list of its choices (items 1–4 there are the two settled and the first two contestable choices above) | 1549 |
| 4 | `:77`, `:79` | §1.1's Adversary and Wrapper rows — contestable choices 1 and 2 in operative form, each with the run that shows the alternative changes a colour | 621 |
| 5 | `:195-268` | §1.3's evidence-pair and report-contract paragraphs, and the event table — contestable choices 3 and 4 | 893 |
| 6 | `:1414-1483` | §3, C-Q10 — the query your ruling registered, with its coverage limit stated per consumer | 615 |

About 4,304 words of the registration plus this note's, call it
twenty-five minutes at a careful pace. Passages 1–3 grew with your
ruling; 4 and 5 are unchanged from your first read. Nothing else in the file needs your ruling.

*Added 2026-09-18 evening, after your ruling:* *the amendment shifted
every range above except the §1.1 rows; the table is recomputed. The
staging block gained the ledger (its two ruling notes, folded onto
existing lines so no ledger line number moved) and three review
records.*

*Added 2026-09-18 by the successor owner instance, before your read:*
*a walk of the tree found four clerical slips, none in anything you
read: the registration's review log stopped at round twelve (rounds
thirteen and fourteen now entered); the skeptic's own reading table at
the file's end carried line ranges from before the round-13 edits
(recomputed; the ranges in this note were already right); the round-14
record said eleven batches and about 120 copies (thirteen and 99); and
the two Codex reads of this note were not archived (now
`docs/reviews/2026-09-17-codex-review-capstone-read-freeze.md`). A
fifteenth Codex pass confirms the edited file; its record is in the
package above. Nothing above line 2008 of the registration changed.*

## 6. How it got here

Drafted 2026-09-15 from the ledger under your outcome-5 ruling; then
fourteen owner-run Codex passes and one full skeptic read on 2026-09-16
and 2026-09-17, a clerical fifteenth on 2026-09-18, and — after your
`REFUSAL` ruling was entered — a second full skeptic read and rounds
sixteen to eighteen the same evening (records in `docs/reviews/`): thirty-four findings
through round eleven, three one-sentence corrections in round thirteen,
and seven skeptic repairs, all accepted; findings per round 6, 4, 4, 2,
2, 6, 2, 2, 3, 2, 1, 0, 3, 0; the composition contract unchanged since
round four; round twelve found nothing and re-ran the 87 archived
`cap5`–`cap24` copies, round fourteen found nothing and re-ran the eight
`cap25`/`cap26` copies, every result matching. Two errors of the owner instance
are on the record inside the file (rounds five and six: cells written
from trace readings instead of runs) and were corrected by runs. The
last reviewer's caution is also mine: this is a judgment about the
registration; whether the composition discharges is what the build
will show.
