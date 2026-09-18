# Codex non-author review of the capstone registration, sixth round (2026-09-17)

Reviewer: OpenAI Codex CLI (`gpt-6-astra`), run non-interactively by the
owner instance on 2026-09-17 (18:42–18:50 UTC) against the whole of
`formal/suite/capstone/PREDICTIONS.md` after the round-five repairs;
scratch diagnostics on family-model copies under
`/tmp/tessera-capstone-r6/`. **The reviewer found the registration not
ready to freeze**, on six findings: one contract defect (link 6b) and
five on the per-case **Cases** cells the round-five repair added to
every companion. Every factual claim below was checked against the tree
before disposition; every run the reviewer cites was reproduced on our
tree (`formal/suite/ledger-tests-2026-09-14/cap17a`–`cap19d`, tenth
batch of that directory's README) at the reviewer's own `.out` line
numbers; and four runs the reviewer did not make — the
repository-compromised variants finding 5 asks for — were built and
run (`cap14d…_repo`, `cap16a/b/c…_repo`). No capstone model exists;
nothing in the repository was run. The reviewer confirms all eighteen
earlier accepted findings repaired except R5.2, the case assignment,
which it accepts only in part.

## What went wrong in round five, stated plainly

The round-five disposition asked for a **Cases** cell on every
companion and said each cell should be "filled from its descent". The
repair step filled the cells for companions with only degraded runs by
**reading their traces** and deciding, per companion, whether the
strict fixture could still present the attack — and it got four of
those readings wrong (C-C2, C-C3, C-C8, C-C16's basis) and applied an
all-green label to configurations with mixed outcomes (C-C7). The
lesson is the one this file's own discipline already states: **a
strict outcome is descended by a strict run or it is predicted**; a
reading of a degraded trace is neither. The owner instance directed
that repair and accepted its judgement calls; the error is the owner's.
Every strict outcome below is now backed by a run.

## Dispositions (owner instance, 2026-09-17)

All six are **clerk dispositions** of the owner instance.

1. **Link 6b, as written, does not observe the attribution its strict
   companion changes.** ACCEPTED. Link 6b is stated over the **inner
   frame's** `(issuerId, kfp)`; Q6a's mutation leaves the frame and its
   checks intact and changes only the envelope's **attribution report**
   (`cap14d_sp7_q1_strict_q6a.pv:235-245`). Reproduced: a literal
   frame-field judge (frame identity = tuple identity, frame fingerprint
   = accepting key) stays **green** on the strict baseline
   (`cap19c_sp7_strict_frame_judge_base.out:587`) **and on the Q6a
   mutant** (`cap19d_sp7_strict_frame_judge_q6a.out:585`) while the
   mutant's `Rescoped` is **red** (`:933`) and both witnesses reachable
   (`:1226`, `:1435`). **Repair:** link 6b is restated as S-P7's
   `Rescoped` shape transcribed **unconditionally, per layer**: for
   `lyr ≠ L0`, the envelope path's own **attribution report**
   `(aid, lyr, kA, idA)` — the `scopeCh` report S-P7's models emit, now
   declared in §1.3 beside `LayerAccepted` — names the innermost frame's
   `(fp(kX), id)`; `ChainBroken(lyr, LINK_6B)` fires when it does not.
   This is the **envelope path's own** report against its own innermost
   frame; it involves no standing path and is therefore distinct from
   conjunct 3, which joins the two paths. The old sentence is quoted.
   C-C15's three configurations red it as before, now for a reason the
   query can see; C-C4 (D2's) reds it at the inner layer as before.

2. **C-C2, C-C3 and C-C8 extrapolated degraded failed sets to strict on
   a false reading of their traces.** ACCEPTED. The round-five cells
   said those traces red "over the honestly evidenced tuple" with zero
   `dsks` steps; the traces in fact forge authority evidence over
   **changed** tuples (`m4_framepin_mh.out:608-616`,
   `sp2_q5_c2_fponly_frame_nomh.out:523-535`,
   `d10b_sp2_q9_manifest_unbound.out:661-673`), and S-P2's own strict
   ablation already shows `SetAltered` closed in strict
   (`s-p2/RESULTS.md:103-120`). Reproduced on the mutants with the
   second, uncompromised authority check added: **C-C2 strict is a
   green control** (`cap18a_sp2_strict_cc2.out:411`, `:424`, `:437`,
   `:450`, `:1129` all green; witnesses `:633`, `:869`, `:1116`);
   **C-C3 strict is a green control** (`cap18b…out:381`–`:402`;
   witnesses `:578`, `:809`, `:1051`); **C-C8 strict is mixed** —
   `SetAltered` green (`cap18c…out:509`) but **C-Q9 red** (`:1431`),
   `PossessionTransplanted` green (`:1202`), witnesses reachable
   (`:701`, `:935`, `:1180`) — which is exactly the (α)/(β) split C-C8's
   own cell already records for degraded. **C-C16's basis** is corrected
   (cap1's displayed attack uses an attacker-authored tuple,
   `cap1…out:1319-1337`) **without withdrawing its strict red**, which
   reproduces by another route (`cap18d_sp2_strict_cc16.out:1430`
   `Spliced` red; link-2b conjuncts green `:1456`, `:1468`, `:1480`;
   witnesses `:701`, `:942`, `:1194`). **C-C17 strict reds as in
   degraded** (`cap18e_sp2_strict_cc17.out:775` `SignerForged`, `:1754`
   `PossessionTransplanted`, `:2086` slot-to-key; witnesses `:981`,
   `:1222`, `:1474`). **Repair:** the four cells are rewritten **per
   query** from these runs; the withdrawn "no green-control reading,
   reason checked" sentences are quoted; and §4's preamble rule gains
   the sentence: *a strict outcome is descended by a strict run or it
   is predicted; a reading of a degraded trace is neither.*

3. **C-C7's cells labelled mixed outcomes as a green control.**
   ACCEPTED. Reproduced on strict S-P1 with the judges and the same-key
   wrapper signer: baseline all green
   (`cap17a_sp1_strict_judges_base.out:338`–`:358`, witness `:547`);
   **(i)** C-Q7 green (`cap17b…out:340`), both C-Q8 forms **red**
   (`:533`, `:709`), honest-key authorship **red** (`:887`), witness
   reachable (`:1079`); **(ii)** the same shape (`cap17c…out:375`,
   `:570`, `:748`, `:928`, `:1118`). **Repair:** both configurations'
   cells register these per-query strict outcomes, descended; neither
   configuration is a green control; the "green-control reading named"
   sentences are withdrawn, quoted.

4. **"(c) as (a)/(b)" is false: (c) leaks both keys.** ACCEPTED.
   Reproduced: on the strict Q6b mutant, leaking the second key makes
   `Rescoped`, `InnerSigTransplanted` and `Reattributed` **reachable**
   (`cap19b_sp7_strict_both_leaked_q6b.out:843`, `:1151`, `:1450`;
   witnesses `:1728`, `:1935`) while the correct model with both leaks
   stays green (`cap19a…out:562`–`:603`). **Repair:** §1.1 already says
   case (c) **is** companion C-C1 and not a correct-form run; every
   other companion's cell therefore says **"(c): not stated — (c) is
   C-C1's run"**, and every "(c) as (a)/(b)" is withdrawn, quoted (C-C4
   through C-C7, C-C15, and any other). C-C15(i)'s cell records
   `cap19b` as the **reason** its strict green is a control and not a
   dead mutation: restoring the attacker's authorized wrapper key
   restores the attack.

5. **Case (b) labelled descended without a repository-compromised
   run.** ACCEPTED, and the runs made: `cap14d_sp7_q1_strict_q6a_repo`
   (`Rescoped` red `:893`; `:907`, `:921` green; witnesses `:1186`,
   `:1395`) and `cap16a/b/c_…_repo` — **identical RESULT polarities
   line for line** with their DNS variants (the `_repo` files carry the
   same line numbers ±0). **Repair:** C-C11, C-C12 and C-C15(iii) label
   (b) **descended** by those runs; everywhere else (b) stays
   **predicted** with channel symmetry named as the basis and never as
   a second run; the family's own note that its second variant was not
   run (`s-standing/PREDICTIONS.md:341-349`) is left as the family's.

6. **C-C10 in strict does not say which evidence check is removed.**
   ACCEPTED. Reproduced: removing the **compromised** channel's check
   severs nothing — publication provenance and unrestricted authorship
   stay green (`cap17d_sp1_strict_cc10_drop_compromised.out:547`,
   `:539`; all else green `:335`–`:355`, witness `:531`); removing the
   **honest** channel's check reds both (`cap17e…out:858`, `:699`)
   while honest-key authorship (`:355`), C-Q7 and both C-Q8 (`:335`,
   `:341`, `:347`) stay green and the witness reachable (`:540`).
   **Repair:** C-C10's mutation is stated per mode: in (d) the sole
   check; in (a)/(b) the **honest** (uncompromised) channel's check is
   the one removed, the compromised channel's retained; set (1) in
   strict = link 1a, **link 1b** (publication provenance) and the
   unrestricted `Accept ⟹ IssuerSigned`; set (2) = honest-key
   authorship, C-Q7, both C-Q8 forms, and the rest; and the
   compromised-check removal is registered as C-C10's **isolation
   control** (`cap17d`), green, so the builder cannot choose which
   check to delete.

7. **The REFUSAL fork stands**, unresolved, owed at the freeze commit;
   the two contestable choices stand and none of the six findings
   reverses them.

**Loop.** One repair pass (Opus, briefed from these dispositions; every
strict cell written from a named run, no trace readings), then a
seventh owner-run full Codex pass.

## Codex review — verbatim

## 1. Query strength and discharge

Repository remained read-only. Diagnostics used family-model copies and a copied library under `/tmp/tessera-capstone-r6/`; no capstone model was built.

Below, **P** = `formal/suite/capstone/PREDICTIONS.md`, **T** = `/tmp/tessera-capstone-r6`, and **L** = `formal/suite/ledger-tests-2026-09-14`.

**1. Link 6b does not explicitly observe the attributed identity that its strict companion changes.**

Link 6b specifies the **inner frame’s** `(issuerId, kfp)`. `LayerAccepted` carries that frame, tuple and accepting key, but no separately attributed identity. Nevertheless, C-C15(iii) is required to red link 6b and now carries D11’s strict discharge. (`P:109–112`, `P:164–180`, `P:424–432`, `P:1969`.)

Q6a leaves the inner frame and its identity checks intact; only `AcceptInner` and the scope report substitute `idW` for `idI`. (`L/cap14d_sp7_q1_strict_q6a.pv:235–245`.)

I added a literal frame-field judge to matched copies of the strict baseline and cap14d: compare the inner frame’s identity with the inner tuple’s identity, and its fingerprint with the accepting key. It stays **green in both**, while the mutant’s `Rescoped` is **red** and both honest witnesses remain reachable. (`T/scope_identity.pv:117–122`, `T/scope_identity.out:585`, `:933`, `:1226`, `:1435`; baseline `T/scope_base.out:587`, `:615`.)

**Required repair:** explicitly bind link 6b to the envelope’s **reported attribution**, including identity, for the same acceptance and layer. C-Q6’s paired-report judge already observes it, but that conditional consumer cannot supply link 6b’s separately claimed unconditional discharge.

## 2. Companion consistency

**2. C-C2, C-C3 and C-C8 extrapolate their degraded failed sets to strict mode on a false account of the traces.**

Their Cases cells say the accepted tuple is honestly evidenced and therefore exclude a green-control reading. The cited attacks instead forge authority evidence over **changed tuples**:

- C-C2 accepts an attacker-key tuple while re-signing honest bytes. (`P:1362`; `L/m4_framepin_mh.out:608–616`.)
- C-C3 moves an honest key to a different, forged one-signer tuple. (`P:1363`; `formal/suite/s-p2/proverif/sp2_q5_c2_fponly_frame_nomh.out:523–535`.)
- C-C8’s `SetAltered` trace does the same. (`P:1368`; `L/d10b_sp2_q9_manifest_unbound.out:661–673`.)

Zero DSKS steps does **not** establish independence from compromised authority. S-P2 already records a strict C2 run with `SetAltered` **unreachable** and all witnesses reachable. (`formal/suite/s-p2/RESULTS.md:103–120`; `formal/suite/s-p2/proverif/diagnostics/d9_strict_c2_mutation.out:395`, `:578`, `:809`, `:1051`.)

On copies retaining the mutations and adding the second, uncompromised authority check:

| Companion | Strict DNS-compromised result |
|---|---|
| C-C2 | `Reattributed` **unreachable**; all source safety queries green |
| C-C3 | `SetAltered` **unreachable** |
| C-C8 | `SetAltered` **unreachable**, but C-Q9 **red** |

All source honest witnesses remain reachable. (`T/cc2_strict.out:450`, `:633`, `:869`, `:1116`; `T/cc3_strict.out:395`, `:578`, `:809`, `:1051`; `T/cc8_strict.out:509`, `:1431`, `:701`, `:935`, `:1180`.)

**Required repair:** assign outcomes **per query**, preserving C-C8’s distinction between possession-message failure and set-integrity failure. Its strict result is not an all-green control.

The same trace-reading error occurs in C-C16’s basis: cap1’s displayed attack uses an attacker-authored tuple, not an honestly evidenced manifest. Its strict red nevertheless reproduces through another route. Correct the basis without withdrawing that prediction. (`P:2075`; `L/cap1_sp2_content_unchecked.out:1319–1337`; `T/cc16_strict.out:1430`.)

**3. C-C7’s green-control classification confuses individual green queries with an all-green configuration.**

The Cases cell permits a green-control reading for configuration (i), although its same-key byte substitution needs no attacker-enrolled key. It also uses that reading for configuration (ii)’s C-Q7 alone. The definition requires **every query green**. (`P:1340–1348`, `P:1367`.)

Strict copies confirm:

- **(i):** C-Q7 green; both byte-binding judges and honest-key authorship **red**.
- **(ii):** C-Q7 green; both byte-binding judges and honest-key authorship **red**.

The matched strict baseline is green, and honest acceptance remains reachable throughout. (`T/base_strict.out:338–358`, `:547`; `T/cc7i_strict.out:340`, `:533`, `:709`, `:887`, `:1079`; `T/cc7ii_strict.out:375`, `:570`, `:748`, `:928`, `:1118`.)

**Required repair:** register these mixed outcomes rather than permitting either whole configuration to count as an all-green control.

**4. C-C15’s “(c) as (a)/(b)” assignment is false.**

Case (c) leaks **both** authority keys. It therefore supplies the attacker-controlled authorized wrapper key whose absence explains configuration (i)’s green strict controls. (`P:65`, `P:77`, `P:1969`.)

Adding only the second leak to cap14b makes `Rescoped`, `InnerSigTransplanted` and `Reattributed` **reachable**, with both witnesses reachable. The matched correct model with both leaks retains all four safety results. (`T/q6b_both.out:843`, `:1151`, `:1450`, `:1728`, `:1935`; `T/q6b_both_base.out:562–603`.)

**Required repair:** give (c) its own assignment. Audit the same shorthand in C-C4–C-C7; the single-channel enrollment restriction cannot justify their case-(c) outcomes. (`P:1364–1367`.)

## 3. Prediction bases and diagnostic citations

**5. Several case-(b) results are labelled descended without a repository-compromised run.**

C-C11 and C-C12 label **(a)/(b)** descended, but their cited family companions and structural copies leak DNS only. S-STANDING expressly records that its second companion variant was not run. (`P:1396–1397`; `formal/suite/s-standing/PREDICTIONS.md:341–349`, `:363–370`, `:394–398`; `L/cap16a_ss_q1_pairjudge_cc11_declared.pv:407`, `L/cap16b_ss_q1_pairjudge_cc11_unsigned.pv:405`, `L/cap16c_ss_q1_pairjudge_cc11_terminal.pv:391`.)

Likewise, cap14d establishes C-C15(iii)’s strict red in **(a)**: its sole leak is `skD`. It does not constitute a run of **(b)**. (`P:1969`; `L/cap14d_sp7_q1_strict_q6a.pv:279–284`.)

**Required repair:** distinguish demonstrated (a) outcomes from predicted (b) outcomes, or supply the missing variants. Channel symmetry is a basis for prediction, not a second recorded run.

The cap5a–cap16c result polarities cited in the repair tables match the archived outputs, including cap14d’s honest-wrapper trace. The defects above concern their interpretation and case assignment, not those result-line transcriptions. (`P:2251–2260`, `:2340–2344`, `:2434–2440`, `:2522–2535`.)

## 4. Builder-ready contracts

**6. C-C10 now requires strict runs without specifying which evidence check is removed.**

Its mutation still says “the degraded verifier’s evidence check removed,” while its Cases cell predicts strict reds and its retained set requires every other conclusion to preserve its baseline outcome. Strict verification has two checks; choosing which to remove changes those outcomes. (`P:1370`.)

On matched strict S-P1 copies:

- Remove the **compromised-channel** check: publication provenance and unrestricted authorship remain **true**.
- Remove the **honest-channel** check: both become **false**, despite honest-key authorship and honest acceptance surviving.

Evidence: `T/cc10_drop_compromised.out:539`, `:547`, `:531`; `T/cc10_drop_honest.out:699`, `:858`, `:355`, `:540`.

**Required repair:** specify the deleted check, retained check and observed evidence term separately for (a)/(b). Otherwise the builder selects whether C-C10 also severs publication provenance.

## 5. Routed and hidden choices

The **REFUSAL fork remains genuine**, with both options and costs stated: exercise the foreign signing domain and add its test, or retain declared-and-unexercised status and leave that test unavailable. Its resolution remains required before freeze. I leave it unresolved. (`P:1591–1618`; `formal/suite/LEDGER.md:1270–1276`; `formal/suite/lib/tessera_theory.pvl:66–76`.)

Same-key wrapping and compromised-channel-only enrollment remain explicit, contestable choices. Findings 2–4 identify consequences requiring consistent registration; none reverses either choice. Finding 6 exposes a further consequential builder choice. (`P:65–67`, `P:1670–1692`.)

## 6. Accepted findings and carried-forward corrections

The eighteen accepted findings were checked individually:

| Prior findings | Verification |
|---|---|
| R1.1–R1.3 | Common-content consumer/C-C16 present; possession versus set-integrity isolation repaired; C-C15’s key-binding losses recorded. `P:390–398`, `:2012–2036`, `:1969`. |
| R1.4–R1.6 | C-Q6 join specified; one-key/one-manifest assignment explicit; “every other choice determined” withdrawn. `P:655–792`, `:493–526`, `:1628–1669`. |
| R2.1–R2.4 | Independent standing path, corrected C-C12 boundary, C-C15’s C-Q7 loss, same-key wrapping and per-case enrollment all present. `P:663–748`, `:1069–1089`, `:1969`, `:65–67`. |
| R3.1–R3.4 | Layer-preserving projection; scope consumer; immutable terms separated from removable checks; authorship basis corrected. `P:302–347`, `:906–927`, `:786–792`, `:1271`. |
| R4.1–R4.2 | Pair comparison and identity-only configuration present; vocabulary-witness exception explicit. `P:925–966`, `:1969`, `:1194–1258`. |
| R5.1 | C-C17, membership consumer and `PossessionTransplanted` consequence correctly registered. `P:1484`, `:2112–2149`. |
| R5.2 | **Partially repaired:** Cases cells exist and C-C15(i)’s (a)/(b) controls match cap14b/c. Findings 2–6 prevent accepting the generalized repair. |

All three ledger corrections remain honoured: structural exact-byte verification without authorship overclaim; publication provenance as a correspondence; and fresh presentation identity with layer-preserving acceptance grouping. (`P:1150–1160`, `:259–273`, `:115–162`.)

**This registration is not ready to freeze. The author should see first finding 1, link 6b’s missing explicit attribution observation; finding 2, the contradicted strict failed sets and their false evidential basis; and finding 3, the all-green classification applied to demonstrably mixed C-C7 outcomes. The REFUSAL decision remains outstanding.**

