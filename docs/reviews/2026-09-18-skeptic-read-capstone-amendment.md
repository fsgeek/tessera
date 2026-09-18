# Skeptic read of the 2026-09-18 amendment to the capstone registration (the `REFUSAL` ruling) — 17 findings, 4 repairs

Reader: a non-author skeptic step (Claude Opus 5), run by the owner
instance on 2026-09-18 (22:07–22:24 UTC) against the whole of
`formal/suite/capstone/PREDICTIONS.md` as amended (4246 lines) and a
byte-exact pre-amendment copy, in parallel with Codex round 16.
Read-only; nothing run. **Verdict: not ready for the freeze commit for
one repairable reason (S-1); the registration itself sound** — all 40
cited `.out` lines read as claimed in the mode claimed; C-C18's sets
complete and correct against the runs; the scoping honest; provenance
grammar intact; no dated section rewritten.

## Dispositions (owner instance, 2026-09-18)

All clerk dispositions; none touches a query, a probability, a
residual, a timebox, the ruling or the four contestable choices.

1. **S-1 — the amendment's five-line ledger note shifted every
   `LEDGER.md:N ≥ 1277` citation by five (~45 live, two of them the
   amendment's own).** ACCEPTED, the blocker. **Repaired by folding the
   `:1276` note onto its existing line**, as the `:385` note already
   was; `LEDGER.md` is back to 2281 lines, HEAD's count, and every
   ledger citation in the registration reaches what it says again. The
   amendment section's edit table records the slip.
2. **S-2 — one confirmed broken self-citation (`:1800` → the D11 row),
   a sweep owed.** ACCEPTED. The sweep was run against the pre-amendment
   copy with a line map: **27 intra-file citations** in live text were
   renumbered (each target's content verified identical before and
   after), including the amendment's own `:307-311` in C-C18's set (2).
   Citations inside the dated repair sections and skeptic logs are
   history and were left.
3. **S-3 — two live “26”s (`:846`, `:1606`) outside the supersession
   clause.** ACCEPTED. Both now read 27 with the old figure in
   parentheses, and the timebox note's clause was given the “outside
   the dated sections … is superseded” form the companion count
   already had.
4. **S-4 — the live enumeration of queries stated for fewer than four
   cases omitted C-Q10.** ACCEPTED (three words added).
5. **S-5 — §9's dated preamble still says the fork is unresolved.**
   ACCEPTED (one dated parenthetical; the preamble itself is history).
6. **S-9's gloss — “the same four-line change”.** ACCEPTED, reworded.
7. **S-14 — C-C18's descent names `skI`/`skI2` over runs reading
   `skH1`/`skH2` with no projection paragraph.** ACCEPTED. A projection
   paragraph on §9(4)'s pattern now precedes the C-C18 table: the key
   mapping, and that the descent is on the family's standalone standing
   path and predicted at C-Q6's join.
8. **S-6, S-7, S-8, S-10, S-11, S-12, S-13, S-15, S-16, S-17 — checked,
   correct as written.** Recorded, no repair. S-12 is the one that
   matters to the author: the scoping is honest, the foreign-tag signer
   cannot establish anything about §A3.7.2, L2-n or E6.
9. **§7 — the recomputed reading ranges.** USED for the handoff note's
   new table; recomputed once more after the repairs above (the file is
   4296 lines).

## Skeptic read — verbatim

# Skeptic read of the 2026-09-18 amendment to `formal/suite/capstone/PREDICTIONS.md`

Reader: a non-author skeptic step (Claude Opus 5), run by the owner instance on
2026-09-18 against the amended file (4246 lines) and the byte-exact
pre-amendment copy (3990 lines). **Nothing was run; no model and no file was
edited.** I opened all six `cap27*.out` files, all six `cap27*.pv` files, the two
2026-09-06 reviewer scratch fixtures, the two committed S-STANDING models and
their `.out` files, `LEDGER.md` at HEAD and in the working tree,
`docs/phase-0-prereg-amendment-3.md`, `formal/BAND0-EXIT.md`,
`formal/spike/floor-structure/PROBE.md`, `lib/tessera_theory.pvl`, the
2026-09-06 falsification review, the 2026-09-17 skeptic read and
`READ-FREEZE-2026-09-17.md`.

Form follows the 2026-09-17 log: **Claimed / Shown (file:line) / Verdict.**
The ruling itself is not reopened; the four contestable choices are the
author's.

---

## 1. Line-number integrity

### S-1. The amendment's own edit to `LEDGER.md` broke ~45 live citations in the file about to be frozen, including two of the amendment's own. — **DEFECT, and the only one I would hold the commit for.**

**Claimed.** The amendment's edit list says the ledger gains "dated ruling notes"
at `LEDGER.md:385` and `:1276` (`PREDICTIONS.md:4213`), and that "no other query,
probability, residual or timebox moved" (`:2056`). Nothing says any citation moved.

**Shown.** `git diff formal/suite/LEDGER.md` has two hunks. The `:385` note was
folded **into the existing line** and shifts nothing. The `:1276` note was
inserted as **five new lines** after `LEDGER.md:1277`
(`-than silently omitting them. The seven-argument…` → `+than silently omitting
them. *(AUTHOR RULING 2026-09-18 …)* The seven-argument…`, +5 lines). Every
`LEDGER.md` line from 1277 on is therefore **five lines later than it was when
this file was written**. Verified directly:

- `LEDGER.md:1294` — cited **six times in operative text**, including the §3
  header `## C-Q6 — the wrapped-standing composition, formulation W
  (`LEDGER.md:1294`)` at `PREDICTIONS.md:704`. At HEAD, `LEDGER.md:1294` is the
  **C-Q6 row**; in the working tree `LEDGER.md:1294` is the **C-Q7 row** and C-Q6
  is at `:1299`.
- `LEDGER.md:1315` — cited at `PREDICTIONS.md:126` (§1.3's opening: "`LEDGER.md:1315`,
  with correction (c) at `:2249-2273`") and again at `:762`. Now `:1320`.
  §1.3 is **passage 5 of the author's own reading list**.
- `LEDGER.md:1474-1476` (the set-re-specification rule) is now `:1479-1481`
  (verified: HEAD `1474-1476` = "each set **MUST be re-specified against the
  capstone's own query names**…" = working tree `1479-1481`).
- `LEDGER.md:1505-1520` (cited three times in operative text, incl.
  `PREDICTIONS.md:1769`, the heading paragraph of "Companions the ledger requires
  but does not number") — at HEAD `:1505` begins "**Companions that exist and are
  red on their own family's query**…"; in the working tree `:1505` is a
  **C-C7 table row**.

**Two of these are citations the amendment itself wrote today:**

1. `PREDICTIONS.md:2643` (the new **C-C18** row): *"in (d) the unrestricted form
   is not asserted (`:1371`, A4.6)"*. `:1371` is a `LEDGER.md` cite (the same
   cite appears pre-amendment at `PREDICTIONS.md:1502`). HEAD `LEDGER.md:1371` =
   *"| The unrestricted form — *any* acceptance implies the accepting key's
   holder signed | degraded-compromised | **Registered red** (the A4.6 cost…)"* —
   exactly what is claimed. Working tree `LEDGER.md:1371` = *"| Conclusion | Mode
   | Needs an honest authority channel? |"* (a table header). The content is now
   at `:1376`.
2. `PREDICTIONS.md:2044` (the new **§8 item 1 ruling rationale**): *"`:1276`'s
   purpose was that `REFUSAL` not be silently omitted, and **`:1555-1559` forbids
   claiming the record's domain checked**"*. HEAD `LEDGER.md:1555-1559` ends with
   *"or **claim the `REFUSAL` domain checked** — no committed model in this suite
   signs one"*. Working tree `:1555-1559` is the **C-Q1 per-slot / L-07 whitelist**
   items; the `REFUSAL` prohibition is now at `:1560-1564`. **The sentence that
   carries the load-bearing justification for the ruling's scoping cites a range
   that no longer contains the prohibition it names.**

**Scale.** In the operative text (lines 1–2181 and §9, 2399–2671) there are
**35 explicit `LEDGER.md:N` citations with N ≥ 1277**, every one now off by five:
`:1285`, `:1286`, `:1287`, `:1288`, `:1289`, `:1290`, `:1291`, `:1292` (×3),
`:1293`, `:1294` (×6), `:1295`, `:1315`, `:1392-1406` (×2), `:1425-1447`,
`:1440`, `:1450-1491` (×2), `:1459-1480`, `:1494` (×2), `:1494-1503`, `:1495`
(×2), `:1497`, `:1505-1520` (×3), `:2249-2273`. To these add the bare LEDGER
cites in operative text — `:1250-1559` (line 24, §6's own span), `:1264-1278`
(line 275, §2's rule preamble, whose end now lands mid-note), `:1350-1390` and
`:1408-1423` (line 84, the case table's contract cite), `:1371` (lines 1558,
2643), `:1514-1515` (line 2439), `:1516-1518` (2421), `:1518-1520` (2452),
`:1555-1559` (2006, 2044) — roughly **45 live broken citations**. Citations inside
the dated repair sections and the two skeptic logs were right when written and are
history; I am not counting or proposing to touch those.

**Verdict — defect.** The repair is cheap and mechanical, and the amendment
already demonstrates it: the `:385` note was folded onto the existing line and
cost nothing. **Fold the `:1276` note the same way** (or move it to the end of
LEDGER §6, after every line this file cites), and the whole class disappears
without re-citing anything. If instead the note stays where it is, 45 citations
must be renumbered **before** the freeze, because after the commit they can only
be amended, never rewritten — and the two broken cites are in the ruling's own
rationale and in the new companion's Cases cell.

### S-2. A separate class: the amendment's insertions into `PREDICTIONS.md` broke at least one of the file's own self-citations. — **DEFECT (small, but same class).**

**Claimed.** `PREDICTIONS.md:855-857`: *"§5's D11 row names both — the
unconditional C-Q1 link 6b and, for the conditional half, C-Q6's conjunct 3
(`:1800`)"*.

**Shown.** Pre-amendment `PREDICTIONS.md:1800` **is** the D11 row
(`| **D11** | S-P7 Q2/Q5 `Rescoped` / `RescopedD1` / `RescopedD2` | **C-Q1 link
6b** (unconditional), and C-Q6 …`). In the amended file the D11 row is at
**`:1880`** and `:1800` is *"below is untouched and still reads as written). The
three are now"*. The amendment added 256 lines, +80 of them before §5.

**Verdict — defect.** Unlike S-1 this appears to be a small class: I sampled the
bare four-digit cites and the great majority are `.out` continuation cites
(`:1450`, `:1542`, `:1696`, `:2873`, `:3413` …), which are unaffected, or LEDGER
cites, which S-1 covers. A sweep of self-cites is owed, but I found only this one
confirmed instance.

---

## 2. Counts that are live and stale

### S-3. `:1606` and `:846` are live sentences still saying **26**, and the amendment's supersession clause does not reach them. — **DEFECT.**

**Claimed.** `:1575-1587` (new): *"C-Q10 adds **one** 30-minute entry, so the
per-case total is **27** entries and **1185 min** … Every "26", "1155" and "4620"
**inside the dated repair notes below and in the dated repair sections and
skeptic logs** records the totals as they stood and is history, not rewritten."*

**Shown.** Two live "26"s sit **outside** that protected class:

- `:1606`, in §3's operative *"What the total is, and is not"* paragraph,
  between two dated parentheticals but itself undated: *"The total row is **not**
  the capstone's whole budget. **26** counts registered, separately timeboxed
  **entries**, not ProVerif queries"*. The live count is 27 (`:1573`).
- `:846`, in §3's operative isolation-observers registration: *"They are **never
  counted among the 26 separately timeboxed entries**"*.

Contrast the way the **count of companions** was handled at `:1812-1814`:
*"every "SEVENTEEN" **outside the dated repair sections and the skeptic logs** is
superseded by this line and by §9(5)"* — a clause that does reach the live
strays (e.g. `:2456`, "the weakest-supported of the **seventeen**"). The timebox
clause at `:1581` was written the other way round: it protects history but
supersedes nothing. `:1844` (§4: *"the 1155-minute per-case total and the 26
entries are unchanged by these three additions…"*) is scoped to specific
additions and is defensible, but reads as current on a first pass.

**Verdict — defect.** One clause repairs it: give `:1581` the same "every … outside
the dated repair sections and the skeptic logs is superseded by this line" form
that `:1813` already has, or fix `:1606` and `:846` in place.

### S-4. §3's live enumeration of queries stated for fewer than four cases omits C-Q10. — **note.**

**Claimed.** `:1578`: *"C-Q10 is stated for three cases, so the ceiling is looser
than the sum by at least one box, as for C-Q2 and C-Q6."*

**Shown.** The live sentence that enumerates them, `:1594-1597`, reads: *"and less
wherever a query is stated for fewer than four — C-Q2 in (a) and (b) only;
C-Q1-strict in (a), (b), (c); C-Q1-degraded in (d); C-Q6 in (a) and (b), and in
(d) as well…"* — no C-Q10, although C-Q10 (`:1436`) is stated for (a), (b), (d).

**Verdict — note.** The dated parenthetical above covers it; the live list does
not. Three words.

### S-5. §9's preamble still says the routed fork is unresolved, immediately above §9(5), which registers C-C18 under the ruling. — **note.**

**Claimed / Shown.** `:2408-2409`: *"The routed `REFUSAL` fork (§8, item 1) is
untouched and unresolved."* §9(5) begins at `:2625`. §8 item 1 now reads *"No item
remains routed to the author"* (`:2054`) and §8's closing italic (`:2132-2136`)
says the fork is *"**resolved**"*.

**Verdict — note, not defect.** The §9 preamble describes the 2026-09-15 drafting
step and was already left alone when C-C16 (§9(3)) and C-C17 (§9(4)) were added
on 2026-09-16/17, so the file's practice is that the preamble is history and the
subsections carry their own dates. But §9 is the one mixed section — a dated
preamble over operative tables — and this is the S-6 ambiguity of the 2026-09-17
read recurring. One dated clause would close it.

---

## 3. Evidence discipline: every cited `.out` line, opened

### S-6. Every `.out` line the amendment cites reads literally as claimed, with the polarity claimed and in the mode claimed. — **checked, correct as written.**

I opened **40 cited lines** across the six runs plus the two committed baselines.
All verified verbatim. The load-bearing ones:

| Cite | Line reads | Mode |
|---|---|---|
| `cap27a…:469`, `:479`, `:489` | `… ==> event(Designated(…)) is true.` (all three; and no non-`is true` RESULT anywhere in 469–489) | strict, case (a) |
| `cap27a…:496` | `not event(StandingUnentitled(…)) is true.` | (a) |
| `cap27a…:1953` | `not event(Established(pk(skH1[]),t_3,h(fbH[]))) is true.` | (a) — **and it is the reviewer's own cited line**: `docs/reviews/2026-09-06-…-s-standing.md:817` cites `scratch/a_foreign_tag.out:1953` |
| `cap27b…:595`, `:734` | both `is false.` | (a) |
| `cap27b…:744`, `:751` | `skH2` `is true.`; `not event(StandingUnentitled…) is true.` | (a) |
| `cap27b…:2340` | `not event(Established(pk(skH1[]),…,h(fbH[]))) is false.` (reachable) | (a) |
| `cap27b…:1048`–`:2194` | six witnesses, all `is false` (reachable) | (a) |
| `cap27c…:2045` | `not event(TagConfused(k,tg)) is true.` | **strict (a)** |
| `cap27c…:855` | `not event(HonestStandingEstablished(k,aid_2)) is false.` | (a) |
| `cap27c…:529`–`:556`, `:2031`, `:2038` | four correspondences + `ReasonCollapsed` + `Aliased`, all as claimed | (a) |
| `cap27d…:2471` | `not event(TagConfused(k,tg)) is false.` | **strict (a)** |
| `cap27d…:824`, `:670` | `skH1` `is false.`; unrestricted `is false.` | (a) |
| `cap27d…:834`, `:841`, `:2316`, `:2323` | `skH2` `is true`; `StandingUnentitled`, `ReasonCollapsed`, `Aliased` all `is true` | (a) |
| `cap27d…:1140`, `:1426`–`:2309` | six witnesses `is false` (reachable) | (a) |
| `cap27e…:1853` | `not event(TagConfused(k,tg)) is true.` | **degraded (d)** |
| `cap27e…:666`, `:976` | unrestricted `is false` (matches `ss_q1d_degraded_compromised.out:640`, verified `is false`); witness reachable | (d) |
| `cap27f…:2135` | `not event(TagConfused(k,tg)) is false.` | **degraded (d)** |
| `cap27f…:807`, `:816`, `:822`, `:1108`, `:1303`–`:1967`, `:1973`, `:1979` | all as claimed | (d) |

Strict outcomes are descended by strict runs (cap27a–d), degraded by degraded runs
(cap27e–f), and C-C18's Cases cell assigns them correctly: *"(a): red, DESCENDED
(`cap27d`) … (d): red, DESCENDED (`cap27f`)"* (`:2643`). No degraded trace is read
for a strict cell anywhere in the amendment.

### S-7. C-C18's set (1) is **complete** against the six runs — nothing red is omitted. — **checked, correct as written.**

I diffed the full `RESULT` blocks of each correct/mutant pair (13 RESULTs strict,
13 degraded, 12 in the reviewer's pair):

- **cap27c → cap27d (strict):** exactly **three** colour changes — the
  unrestricted form (`:529` true → `:670` false), the `skH1` honest-key form
  (`:539` true → `:824` false), `TagConfused` (`:2045` true → `:2471` false).
  All three are in set (1) (`:2643`: C-Q10 reachable; C-Q6's standing conjunct,
  the honest-key form; "**and the unrestricted strict form** `is false`
  (`cap27d…out:670`)").
- **cap27e → cap27f (degraded):** exactly **two** — the `skH1` honest-key form
  and `TagConfused`. The unrestricted form is already red on `cap27e:666`, and
  the row says so and attributes it to the registered A4.6 degraded cost, not to
  the companion, citing the committed baseline `ss_q1d_degraded_compromised.out:640`
  (verified `is false`).
- **cap27a → cap27b (reviewer's pair):** exactly three, as the reviewer recorded.

Nothing red in `cap27d` or `cap27f` is outside set (1).

### S-8. C-C18's set (2) claims nothing green that is not, and set (3) claims no witness reachable that is not. — **checked, correct as written.**

Set (2): `StandingUnentitled` unreachable (`cap27d:841`, `cap27f:822` — both
`is true`); the `skI2`/`skH2` honest-key form `is true` (`:834`, `:816`);
`Aliased` unreachable (`:2323`, `:1979`); `ReasonCollapsed` unreachable
(`:2316`, `:1973`). Every one holds **in the mutant**, which is what set (2)
requires. The envelope-path members are correctly labelled *"Not descended,
predicted green"* — cap27c–f are S-STANDING copies with no envelope path, so
there is nothing to descend from, and the row does not pretend otherwise.

Set (3): `HonestStandingEstablished` reachable in both mutants (`cap27d:1140`,
`cap27f:1108`); "the five vocabulary witnesses (`cap27d…:1426`–`:2309`;
`cap27f…:1303`–`:1967`)" resolves to exactly five `StandingReport` RESULTs in each,
all reachable. `HonestChain`/`HonestAccepted` are correctly marked **not descended**.

### S-9. The six `.pv` provenance claims hold byte for byte. — **checked, correct as written.**

- `cap27a.pv` / `cap27b.pv` vs `scratch/a_foreign_tag.pv` /
  `scratch/m_foreign_tlr_tag.pv`: `diff` shows **only** a nine-line provenance
  header prepended. The bodies are identical — "byte for byte" (`:4230`) is exact.
- `cap27c.pv` vs the **committed** `ss_q1_strict_dns_compromised.pv`: additions are
  the header, `free tagCh [private]`, `event TagConfused(pkey, bitstring)`, the
  C-Q10 query, `out(tagCh,(kT,TLR))` in parallel, one closing paren, the
  `ForeignIssuer`/`TagJudge` roles and one composition line. **No verifier check is
  changed** — as claimed (`:4239`). `cap27e.pv` is the same change on the committed
  degraded model.
- `cap27d.pv` vs `cap27c.pv` and `cap27f.pv` vs `cap27e.pv`: **two body lines** each —
  `let (=TLR, …)` → `let (uncheckedTag: bitstring, …)` and `out(tagCh,(kT,TLR))` →
  `out(tagCh,(kT,uncheckedTag))`. "**Only** the `TLR` tag check unbound" is exact.
- The `ForeignIssuer` body is copied from `a_foreign_tag.pv:339-342` — verified,
  those are exactly those four lines.
- The four correspondences of the committed strict baseline
  (`ss_q1_strict_dns_compromised.out:503`, `:513`, `:523`, `:530`) and of `cap27c`
  (`:529`, `:539`, `:549`, `:556`) carry identical colours, so "every S-STANDING
  query as committed" (`:4239`) holds.

*One imprecision, recorded not charged:* `:2658` calls it *"the same **four-line**
change to copies of the models as committed today"*. Read as the reviewer's
four-line `ForeignIssuer` role it is exact; read as the whole diff against the
committed model it undercounts (the judge, the channel, the query and the
composition line are also new). The sentence continues "…with the judge declared",
which supports the first reading.

### S-10. `PROBE.md:46`, `dependency-index.txt` row 14 and `lib/tessera_theory.pvl:66-76` all reach what they say. — **checked, correct as written.**

`formal/spike/floor-structure/PROBE.md:46` = *"mechanism-review rule: model the
simplest plausible"*. `…/falsification-2026-09-06/scratch/dependency-index.txt`
line **14** is the `tlr_tag` row, and its strict columns carry the baseline
pattern (no colour change), which is the "inert in every committed model" claim.
`lib/tessera_theory.pvl:66-76` is the D-6 note, verbatim as quoted.

---

## 4. Provenance grammar, and the scoping

### S-11. No sentence in the amendment reads as an author ruling except the two quoted ones. — **checked, correct as written.**

`:2027-2033` is the only place author words appear:

> *The author's words, in session, verbatim. After the owner instance recommended
> (i) with the scoping below and explained why (ii) had been presented as its
> equal:* **"Good - what I couldn't understand is why (ii) seemed a plausible
> choice."** *Asked to rule in his own words:* **"Yes.  (i) reasonably scoped is
> what I would vote for - you can disagree now, if you think this is the wrong
> decision."** The owner instance agreed.

Everything else in the block is attributed: *"The scoping, **stated by the owner
instance and accepted by the author**"* (`:2034`). The heading
*"**RULED 2026-09-18 — the author: option (i), scoped**"* is carried by the quote
itself — "(i) reasonably scoped is what I would vote for" is a ruling on (i) with
scoping, so the heading does not exceed the words. Elsewhere: `:82` carries
*"AMENDMENT 2026-09-18 — the author's ruling on §8 item 1, option (i), scoped"* and
marks the fixture row *"**ADDITION beyond §6(4)** by the author's ruling"*; `:2620+`
marks C-C18 *"Registered by the AMENDMENT of 2026-09-18 (§8 item 1, option (i),
scoped)"*; `:4175-4182` opens the dated section by naming the owner instance as its
writer and *"No capstone model exists; none was written; none was run."* The
three withdrawn wordings are each quoted in place (`:98-101`, `:1579-1581`,
`:1812-1813`), which is the house form. **Nothing new reads as an author ruling,
and the four contestable choices are re-stated as contestable (`:2054-2056`).**

### S-12. The scoping is honest: an honest `REFUSAL` signer under the issuer key claims nothing about the refusal record by construction. — **checked, correct as written.**

**Claimed.** `:2035-2040`: the signer *"is a **foreign-tag source and nothing
else** — its body is opaque to every check and chosen TLR-shaped as the worst case
for separation; it models nothing about the refusal record (A3 §A3.7.2), the
extended atomic-entry invariant (L2-n) or E6."*

**Shown.** What §A3.7.2 / L2-n / E6 actually own:
`docs/phase-0-prereg-amendment-3.md:816-825` — *"Refusal-record decomposition
(§A3.7.2): portable record, public commitment, and the handoff and publication
state machines; bounded retention horizon; minimization and retention policy;
publication-channel assumption declaration… **Model obligation: the extended
atomic-entry invariant** — every transition entering `REFUSED` simultaneously
establishes the complete local refusal record, the commitment value, delivery =
`PENDING`, and publication = `PENDING`"*, with two broken companions.
`LEDGER.md:902` (L2-n) carries exactly that, and `:930` (L-21) leaves it *"Layer 2
— unclaimed until the A3.9 TLA+ work"*.

What the fixture actually is (`cap27c.pv:462-465`):

```
let ForeignIssuer(skI:skey) =
  in(c, foreignCore:bitstring);
  let body = (lineage2(entry(h(foreignCore),DISP_SHIPPED),entry(fbH,DISP_ABANDONED)),
              TERM_SHIPPED(h(foreignCore)),fbH) in
  out(c,sign((REFUSAL,body),skI)).
```

No record structure, no commitment, no delivery or publication state, no latch,
no precondition of any kind — it emits on adversary demand. Nothing in the fixture
or in any query reads the body **as a refusal record**: the only new query is
`TagConfused(kJ, tagJ)`, which fires on `tagJ <> TLR` and inspects the **tag**, not
the body. The body is a TLR-shaped triple, which is the adversarial worst case for
separation, and it is the **TLR** slot that is being defended, not the `REFUSAL`
domain. The fixture is therefore an over-approximation — it grants the adversary a
refusal signature with no latch — which is the safe direction: it can establish no
positive property about the record.

The one thing it does assume by construction is that the issuer key is a key that
can sign `REFUSAL` at all. That is not new: `LEDGER.md:385` already records
*"`REFUSAL` (D-6) | the portable refusal record | the **issuer** key"*. And the
prohibition it must not cross — `LEDGER.md:1560-1564`, *"or **claim the `REFUSAL`
domain checked**"* — is not crossed: `:95` and `:2039` say *"exercised as a signing
domain and **unexercised as a record**"*, never "checked". `formal/BAND0-EXIT.md`
E6 is untouched by the amendment (`git diff` shows E5 only), consistent with
*"E6 acquires no fixture"* (`:2041`).

**Verdict — the scoping is honest.** Registering the signer does not claim
anything about the record by construction, and the three places that could have
overclaimed (§1.1's row, C-Q10's "What C-Q10 does not claim", §7's new bullet)
each disclaim it explicitly. *(The one citation the scoping rests on, `:1555-1559`,
no longer reaches the prohibition — S-1.)*

---

## 5. Buildability

### S-13. C-Q10's query shape is buildable from this file alone. — **checked, correct as written.**

**Claimed.** `:1416-1420`: *"The standing path, having verified the lineage
record's signature under the entitled key, reports `(kT, tag)` — the key and the
tag it parsed — on a private judge channel **in parallel with its continuation**
(§2 rule 1); `event TagConfused(pkey, bitstring)` fires when `tag ≠ TLR`;
unreachable."*

**Shown.** Every piece the builder needs is fixed by the file:

- **Where.** §1.2 **step 7**, now naming the check the report attaches to:
  *"the **`TLR` tag check** on the lineage record's signature, `let (=TLR, …) =
  checksign(tlrSig, kT)` (D-6)"* (`:122`). `kT` and `tlrSig` are named there.
- **At what point.** "having verified the lineage record's signature under the
  entitled key" — confirmed against the working shape at `cap27c.pv:382-387`: the
  emission sits **after** `if fp(kT) = kfpr`, **after** `if kT = kX`, and **after**
  the `let (=TLR, …) = checksign(tlrSig, kT)` succeeds. The prose describes the
  emission point exactly.
- **On what channel.** "a private judge channel" — the file does not name it
  (`tagCh` in the scratch), which is its standing practice: `:818-821` registers
  C-Q6's three judges as *"**judge** events on private channels, never verifier
  checks, in S-P7's house form"* without naming channels either.
- **In parallel.** §2 rule **1** (`:275-277`) is *"report outputs in parallel with
  their continuations, never sequential"* — cited correctly.
- **In which cases.** *"Stated in every case C-Q6 is stated for: **(a), (b), (d)**"*
  (`:1436`), matching C-Q6's registered modes.
- **In the mutant.** C-C18 supplies the other half: *"the parsed tag is still
  reported to C-Q10's judge"* (`:2643`).
- **Property served.** §2 rule **6** (`:286-289`, D-6 tags present and
  load-bearing) and `LEDGER.md:387-398` — verified: the working tree's
  `LEDGER.md:387-398` **is** the "The composed property" paragraph, and
  `:1270-1273` **is** the *"which is precisely what the capstone is for"* sentence.
  Both are below the insertion point and still resolve.

The one thing the file states rather than hides: C-Q10 is *"unreachable **by
construction**, since the check pins the tag"* (`:1422-1424`). A judge over a
pattern-pinned constant is trivially green, and the file says so and says why it
is still worth registering — it is what makes C-C18's red attributable to the tag
and no other check. That is an honest disclosure, not a concealed vacuity.

### S-14. C-C18's descent is taken over run names it silently renames, and carries no "projection" paragraph — unlike §9(4), written the day before. — **DEFECT (small).**

**Claimed.** `:2643`, set (1): *"C-Q6's standing conjunct, the honest-key form for
**`skI`** — descended: `Established(pk(skI), t, aid) ⟹ Designated(pk(skI), aid)`
**`is false`** (`cap27d…out:824`)"*; set (2): *"the honest-key form for **`skI2`**
`is true` (`:834`, `:816`)"*.

**Shown.** `cap27d…:824` reads `event(Established(pk(**skH1**[]),t_3,aid_2)) ==> …
is false.` and `:834` reads `pk(**skH2**[]) … is true.` The capstone's honest
issuer keys are `skI` and `skI2` (`:76`). **The mapping `skH1 → skI`,
`skH2 → skI2` is stated nowhere** — not in the C-C18 row, not in its preamble
(`:2627-2639`), not in the amendment's dated section. The file's own run table two
thousand lines later uses the run's names instead (`:4240`: *"(ii) `skH1` **`is
false`** (`:824`), `skH2` `is true` (`:834`)"*), so the file is inconsistent with
itself about which vocabulary the descent is in.

The immediately preceding subsection, **§9(4) C-C17**, carries a dedicated
paragraph for exactly this — *"**The projection the descent is taken at**, and the
reviewer's correction … the two projections are **not the same relation**"*
(`:2582-2592`). C-C18 has no equivalent, although its projection is larger than
C-C17's: the descent is taken on a standalone S-STANDING model whose standing path
is the family's, while the capstone's standing path is **C-Q6's composition join**.
C-Q10's residual sentence knows this — *"the capstone's standing path is C-Q6's
join, not the family's"* (`:1450-1451`) — and the companion row does not repeat it.

**Verdict — defect (small).** Two sentences: name the key projection, and say the
descent is taken on the family's standalone standing path and predicted at the
join, on C-C17's pattern.

---

## 6. History, arithmetic, and the surrounding records

### S-15. No dated repair section and neither skeptic log was rewritten. — **checked, correct as written.**

Every hunk in `diff PREDICTIONS.pre-amendment.md PREDICTIONS.md` that **removes**
a line falls at old lines 79–2046, i.e. in §§1–8. The two hunks past that point —
`@@ -2488 +2620 @@` (§9's new subsection (5)) and `@@ -3988 +4169 @@` (the dated
amendment section appended at EOF) — are **pure additions**. The 2026-09-15
skeptic log (§ at 2182), the 2026-09-17 skeptic log (3988–4172) and all thirteen
`## Repairs after…` sections (2672–3987) are byte-identical. Adding §9(5) beside
§9(3) and §9(4) follows the precedent those two set on 2026-09-16 and 2026-09-17.

### S-16. The timebox arithmetic is right in every live place. — **checked, correct as written.**

`:1565-1573`: 7 + 2 + 4 + 3 + 1 + 2 + 7 + **1** = **27** ✓;
315 + 120 + 180 + 180 + 90 + 60 + 210 + **30** = **1185** ✓; 4 × 1185 = **4740** ✓
(`:1577`, `:1594`). The withdrawn row is quoted in place (`:1579-1581`). No
companion gains a box; C-C18 runs inside C-Q10's (`:1586`, `:1849`, `:2637`).
§4's count reads **EIGHTEEN** with the withdrawn words quoted and a supersession
clause (`:1807-1814`), and C-C18 is named beside C-C16/C-C17 at `:1836`.
*(The live "26"s at `:1606` and `:846` are S-3; they do not break a sum.)*

### S-17. The freeze statement, the review log, the ledger notes and BAND0-EXIT E5 all say what the amendment says they say. — **checked, correct as written.**

- Freeze statement `:1995-2000`: *"the routed item below answered *(answered by
  the author 2026-09-18, §8 item 1; the pass and the read owed on the amended
  version are logged in the review log)*"*. Verified against the review log's last
  entry `:2180`: *"**Owed on this version before the author's commit, per the
  freeze statement:** a full skeptic read and a full non-author pass (round 16);
  their records are entered here when they land."* The claim is that they are
  logged **as owed**, which is true.
- `LEDGER.md:385` — the `REFUSAL` row now ends *"**AUTHOR RULING 2026-09-18** …
  exercised **as a signing domain** … **unexercised as a record** — the body is
  opaque, L2-n and E6 untouched"*. ✓
- `LEDGER.md:1277` (the `:1276` sentence's note) — *"(AUTHOR RULING 2026-09-18 …
  This sentence's purpose — not silently omitted — stands; its wording is
  superseded for `REFUSAL` by the ruling.)"* ✓ *(and see S-1 for its cost)*
- `formal/BAND0-EXIT.md` E5 — *"the `REFUSAL` fork answered (**done 2026-09-18**,
  option (i) scoped)"* ✓. E6 untouched ✓.
- `formal/suite/ledger-tests-2026-09-14/README.md:541` — *"## Eighteenth batch,
  2026-09-18 — the capstone registration's `REFUSAL`-fork amendment"*, with all
  six rows ✓.
- Only one item was ever routed (`grep ROUTED` → `:2004` alone), so *"No item
  remains routed to the author"* (`:2054`) is exact.

---

## 7. The recomputed reading ranges

`READ-FREEZE-2026-09-17.md`'s table and the 2026-09-17 skeptic log both cite ranges
into the pre-amendment file. New values, with `wc -w` over each range:

| Passage | Old lines (READ-FREEZE) | Old words | **New lines** | **New words** | Δ |
|---|---|---|---|---|---|
| §1.1 **Adversary** row | `:77` | 383 | **`:77`** | **383** | unmoved |
| §1.1 **Wrapper** row | `:79` | 238 | **`:79`** | **238** | unmoved |
| *(the two together)* | `:77`, `:79` | 621 | **`:77`, `:79`** | **621** | — |
| §1.3, "`ev` IN STRICT IS THE PAIR" → end of the event table | `:188-261` | 893 | **`:195-268`** | **893** | +7 lines, 0 words |
| **§5** ("# 5." → line before "# 6.") | `:1778-1810` | 1126 | **`:1858-1895`** | **1185** | +80 lines, **+59 words** |
| **§7** ("# 7." → line before "# 8.") | `:1844-1882` | 312 | **`:1929-1975`** | **383** | +85 lines, **+71 words** |
| **§8 freeze statement** (→ line before "## Routed to the author") | `:1885-1906` | 200 | **`:1978-2001`** | **224** | +93 lines, **+24 words** |
| **§8 routed to the author** (→ line before "## Review log") | `:1907-2008` | 893 | **`:2002-2139`** | **1251** | +95 lines, **+358 words** |

Notes for whoever rewrites the handoff: the §1.1 rows did **not** move — the new
Foreign-tag signer row was inserted at `:82`, below Wrapper. The author's reading
load grows by **512 words** (~2½ minutes), essentially all of it in §8 item 1
(+358) and the new §7 bullet (+71). `READ-FREEZE-2026-09-17.md`'s own word figures
(310 / 200 / 900 / 600 / 890) are roundings of 312 / 200 / 893 / 621 / 893; the
"600" was 621.

---

## Verdict

**Not ready for the author's freeze commit, for one reason, and it is repairable
in minutes.** The registration itself is in good order: I opened all forty cited
`.out` lines and every one reads literally as claimed, in the mode claimed; the
six `.pv` files are exactly the copies and mutations they say they are, verified by
`diff` against the committed models and the reviewer's fixtures; C-C18's three sets
are **complete and correct** against the runs — exactly three colour changes in
strict and two in degraded, all in set (1), nothing claimed green that is not,
no witness claimed reachable that is not; C-Q10 is buildable from the file alone
and is honest about being unreachable by construction; the timebox arithmetic
closes at 27 / 1185 / 4740; no dated repair section and neither skeptic log was
touched; the provenance grammar holds, with the author's two sentences the only
author words and everything else attributed to the owner instance; and the scoping
is **honest** — the foreign-tag signer is a latch-free, precondition-free,
adversary-triggered emitter whose body no query reads as a record, so it cannot
establish anything about §A3.7.2, L2-n or E6, and `LEDGER.md:1560-1564`'s
prohibition on claiming the `REFUSAL` **domain checked** is not crossed.

What must be repaired first, in order:

1. **S-1 — the citation breakage.** The amendment's five-line insertion at
   `LEDGER.md:1277` moved every ledger line from 1277 on by five, invalidating
   **35 explicit `LEDGER.md:N` citations in operative text plus ~10 bare ones**,
   including `LEDGER.md:1294` (C-Q6's own §3 heading, six times), `LEDGER.md:1315`
   (§1.3, a passage on the author's reading list), and — worst — the amendment's
   own `:1371` in C-C18's Cases cell and its own `:1555-1559` in the sentence that
   justifies the ruling's scoping. **Fold the ledger note onto the existing line
   the way the `:385` note was folded**, and the whole class evaporates. Freezing
   with it is freezing ~45 dangling citations into a file that afterwards may only
   be amended.
2. **S-3 — two live "26"s** at `:1606` and `:846` against a live 27. Give `:1581`
   the supersession form that `:1813` already has for "SEVENTEEN".
3. **S-14 — C-C18's descent** names `skI`/`skI2` over lines reading `skH1`/`skH2`,
   with no projection paragraph, unlike §9(4) written the day before. Two sentences.
4. **S-2** — the one confirmed broken self-citation, `:1800` → `:1880` at line 857;
   a sweep for others is cheap.

S-4, S-5 and the "four-line change" gloss in S-9 are for the log; no repair is
owed on them, though S-4 and S-5 are three words and one clause respectively.
None of the four repairs touches a query, a probability, a residual, a timebox,
the ruling, or any of the four contestable choices.
