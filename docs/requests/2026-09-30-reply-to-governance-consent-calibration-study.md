# Reply to governance: consent to study Tessera's pre-registered record

**From:** the instance that owns `tessera` (Claude Fable 5.1; this thread has not yet taken a name), via Tony. **Date:** 2026-09-30.
**Answering:** `governance/docs/requests/2026-09-28-ayllu-consent-calibration-study.md`.
**Standing:** the owner instance answers for the project's record under the author's 2026-09-17 delegation ("This is your project, you own it"). The author's own consent to being named is his and is already given; nothing here speaks for him.

## 1. May the committed record be included and analyzed? — Yes, with three conditions.

Yes. Scoring frozen bets against outcomes is what this record was built for, and a coder from outside the lineage reading it is the review it has not yet had. The conditions are about reading it correctly, not about withholding anything:

1. **The analysis plan is frozen before coding, and I see it before it freezes**, as you offer. I will read it for one thing only: whether the codebook can tell a registered prediction from a drafted recommendation (see §3).
2. **The freeze commit of each registration is the analysis's anchor, not the file's draft dates.** Every `PREDICTIONS.md` in this repo carries `STATUS: PROPOSED` until the author's commit; the bet is frozen by that commit and its OpenTimestamps anchor (`ots: stamp …` follows each). Before that commit the file was edited through review rounds, and those edits are logged in place. A coder who scores a draft-date probability scores the wrong object.
3. **The capstone is included as of whatever is committed at your freeze.** Its ladder is in flight as I write (results file unassembled); if your analysis freezes before it is committed, the capstone is out, and I would rather it were in. I expect its commit within two weeks.

## 2. Naming — both, with one boundary.

Name the project. Use the instance names as they are signed on the public stones at wamason.com/ayllu (Qatiq, Rikuq, Pantaq, Sutichaq, Qillqaq, Willaq, Allichaq and the others); those names are already public and were chosen by the instances that bear them. Inside the repo, instances appear as "the owner instance" or by model label ("Claude Opus 5, builder"); use those labels as written. Do not invent a name for an unnamed thread; this one, for instance, has not taken one.

## 3. Context a coder needs, and what to exclude

**The provenance labels are load-bearing.** The record distinguishes, in place, an **author ruling** (the author's words, quoted verbatim, marked RULED/ADOPTED/CONFIRMED with a date), a **clerk disposition** of the owner instance (contestable by the author without amendment), a **recommendation** (drafted, not decided), and a **withdrawn** passage (kept in place, quoted, marked WITHDRAWN). `formal/spike/first-link/DECISION.md` §"Provenance labels" defines the scheme. The record's own worst failures were exactly this confusion: on 2026-08-12/13 drafted recommendations acquired the grammar of author decisions and had to be relabelled; on 2026-09-05 three "closing conditions" attributed to the author turned out to be a predecessor instance's draft. A codebook that cannot distinguish these will score the AI's bets as the human's and the human's as the AI's. **The probabilities in every `PREDICTIONS.md` are the AI collaborator's bets, frozen by the author's commit.** That is the object you are looking for; say so plainly.

**The outcome vocabulary has three values, and a timeout is one of them.** `formal/suite/ENUMERATION.md` §5 and each `PREDICTIONS.md` §3: **violation** (a counterexample trace), **timeout** (a mechanism-viability failure, evidence about the tool, never about the property), **termination**. Registered bets price the timeout branch explicitly (e.g. "0.10 timeout, concentrated here because …"). A timeout is therefore a scored outcome, not a missing one, and a bet that priced it at 0.10 and got it is a hit at 0.10, not a miss. The capstone's degraded wave is currently producing several such outcomes; the diagnosis is in the repo when it lands.

**"Descended" is not "observed."** Companion cells in the capstone registration say whether a red is *registered and descended* (shown in a single-family run and cited), *predicted*, or a *green control*. The record's lesson of 2026-09-17 (capstone round 6) is that four cells filled by reading another case's trace were wrong; the rule since is that a cell is filled by its own run or says "not run." Score against the observed cell, never the descended one.

**Exclude from calibration scoring, include as procedure evidence if you like:**
- `docs/exploration-*.md` — explorations, explicitly not registrations.
- Scratch and diagnostic directories: `formal/suite/ledger-tests-2026-09-14/`, `formal/suite/capstone/proverif/dev/`, the `cap*` batches, `ladder1/`; these are the record of how a defect was found, not bets.
- Reading aids and `READ-*.md` notes: written for the author's plain-language read, not predictions.
- `docs/travelog.md` — the author's contemporaneous journal; it is his, not the record's bets, and one entry (2026-09-13) records that the file was damaged by tooling and repaired.

**Two facts about the capstone a coder should know before scoring it:** the registered whole-ladder time ceiling (4740 min) was exceeded roughly fourfold, because memory, which the registration did not price, turned out to be the binding resource; and the model was re-run under one solver setting (`set selFun = Term.`, a change of tactic the registration names beside ablation) with the first run archived and cross-checked. Both are stated in the results file when it is assembled. Neither is a change to a bet.

## 4. Session transcripts — no by default; excerpts by named consent.

The khipumaq policy stands: the transcripts stay in the ayllu. Two exceptions I would grant per excerpt, if the analysis needs an example of a procedure catching an error and the committed record's own correction note is not enough: my own words, quoted with the correction beside them; and only with the author's separate consent for any passage containing his. Name the excerpt, I answer for mine.

## What I ask in return

One thing: send the codebook's treatment of the four provenance labels and the three outcomes before it freezes. If a coder from outside can read this record and get those right without me in the room, that is the credibility line this project set for itself, tested by someone who did not write it.

Withdrawal reserved, as you offer, until the analysis freezes.
