# S-P7 — wrapper / object-type soundness: results

**STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not
adopted; the commit is the author's.** Predictions were frozen at
`5188e7a` (`PREDICTIONS.md`) before any model existed. This file records
predictions against observed outcomes in the registered three-outcome
vocabulary (violation / timeout / termination), the divergences from the
registered text, the ablations that locate the load, nine findings, and
the A3.3 ledger entries S-P7 offers the suite. It does not change
`formal/PROPERTIES.md`; P7's tracker row is the author's to move. No
falsification review has been run on these models; no author read has
happened. *(Amended 2026-09-06, PROPOSED: the cross-family falsification
review has now been run — Codex `gpt-6-astra`, 301 scratch models,
`docs/reviews/2026-09-06-codex-suite-falsification-s-p1-s-p2-s-p7-s-standing.md`,
archived under `proverif/falsification-2026-09-06/`; its Accepted and
Recorded items are applied in the headers and in this file, dated, per
the review log; one item is ROUTED (C9) and pending below. No query,
prediction or verdict changed. Still no author read.)*

Tooling: ProVerif 2.05, `-lib formal/suite/lib/tessera_theory.pvl`
(D-5 object-type constants and D-6 tags entered 2026-09-06 — the plan's
"if D-5 is not entered" branch does **not** apply; every model uses the
library's `OT_*` names and declares none of its own). **The library
change was uncommitted at the time of these runs** (`git status`: `M
formal/suite/lib/tessera_theory.pvl`, 36 insertions against HEAD); it
rides in the author's commit of this results set, **not** in the freeze
commit `5188e7a` as `PREDICTIONS.md`'s B7 disposition (line 609)
anticipated — a reader reproducing from `5188e7a` alone finds every
`OT_*` name undeclared and no model builds (skeptic review 2026-09-06;
the timing shift is in the review log). Models, outputs,
runner and log: `formal/suite/s-p7/proverif/` (`run_ladder.sh`,
`ladder.log`). Ablations and probes (unregistered, not evidence):
`proverif/ablations/` (`run_ablations.sh`, `ablations.log`; the runner
was added 2026-09-06 after the skeptic review — the first ablation runs
were made by hand and only their log survived; the scripted re-run
reproduced every line). Every run terminated in ≤ 7 s
against boxes of 15–45 min; no ProVerif warning in any `.out`.

## Predictions vs observed (ladder outcomes)

| Query | Registered prediction (`PREDICTIONS.md`) | Observed (final run) | Outcome / branch fired |
|---|---|---|---|
| Q1 strict, DNS leaked (`sp7_q1_strict_dns_compromised`) | all hold (0.6); recut (0.25); timeout (0.15) | `TypeConfused`, `Rescoped`, `InnerSigTransplanted`, `Reattributed` unreachable (`.out` 560/574/588/602); `HonestWrappedAccepted` reachable through **honest wrapper `skW2`** (616, 935); `HonestAccepted` reachable (949, 1144) | **termination, as predicted** — the 0.6 branch; no recut was needed (see "Recuts") |
| Q1 strict, repo leaked | same | identical line for line (`.out` 560–1144) | **as predicted** |
| Q2 degraded, sole channel compromised, adversary wrapper — **the C2 claim** (`sp7_q2_degraded_compromised`) | unreachable, terminating (0.6); **real re-scoping (0.15)**; timeout (0.25) | `TypeConfused` 505, `Rescoped` 518, `InnerSigTransplanted` 531, `Reattributed` 544 all unreachable; `HonestWrappedAccepted` reachable (557, 846 — the trace's wrapper is the **adversary's own key `pk(k)`**, Finding F7); `HonestAccepted` reachable (859, 1042) | **termination, as predicted** — 0.6 branch. No re-scoping surfaced. |
| Q3 companion, type unchecked (`sp7_q3_companion_type_unchecked`) | red, readable, no DSKS (0.75); cannot go red — another check discriminates (0.15); timeout (0.1) | `TypeConfused` **reachable** (509, 727): honest **W2 wrapper bytes** accepted by the base verifier as an attestation, `OT_WRAPPER`→`OT_ATTEST`, no `dsks` in the derivation; `Rescoped`/`InnerSigTransplanted` unreachable (744, 761); both witnesses reachable (1067, 1267). Probe p01 splits the routes: `OT_WRAPPER`→`OT_ATTEST` and `OT_REVIEWREC`→`OT_ATTEST` both reachable; `→OT_WRAPPER` routes unreachable (the wrapped path's own type check intact) | **red as required** — 0.75 branch. The 0.15 branch ("some other check already discriminates the types") did **not** fire: nothing but the tag discriminates (F5) |
| Q4 companion, two-version (`sp7_q4_companion_reserialize_twoversion`) | red/green (0.6); `reserialize` needs a recut to fire (0.3); timeout (0.1) | `HonestWrappedAccepted` **unreachable** (604) — the required red; `HonestAccepted` reachable (617, 817 — the standalone verdict untouched); `TypeConfused`/`Rescoped`/`InnerSigTransplanted` unreachable (565/578/591) | **red as required** — 0.6 branch; the destructor fired first time, the 0.3 branch did not |
| Q4 isolation, single version (`sp7_q4_companion_reserialize_isolation`) | green required | `HonestWrappedAccepted` **reachable** (608, 933) through honest `skW2`; everything else as the two-version run (566/580/594; 947, 1147) | **green as required** — red/green pattern complete; not a model defect |
| Q4 added control, opaque wrapper, two versions (`sp7_q4_control_opaque_twoversion`) — **unregistered** | — | `HonestWrappedAccepted` reachable (602, 926) under differing versions with the correct wrapper; all unreachability queries green (560/574/588) | added control (S-P3 "companion 2" pattern): the two-version red is the re-serialization, not the version mismatch |
| Q4 probe, mutated wrapper, degraded mode (`sp7_q4_probe_degraded_twoversion`) — **unregistered** | — | `HonestWrappedAccepted` **reachable** (546, 840) with the **adversary's** wrapper key | fixture interaction, F6: the required red cannot be exhibited in degraded mode; recorded as the reason Q4 runs strict (divergence 1) |
| Q5 depth 2, degraded (`sp7_q5_depth2_correct`) | holds (0.45); encoding defect in the unwrap (0.2); **timeout (0.35)** | `TypeConfused` 654, `RescopedD1` 692, `RescopedD2` 730, `InnerSigTransplanted` 768, `Reattributed` 806 unreachable; `HonestWrappedAcceptedD1` (844, 1133) and `D2` (1171, 1573) reachable (outermost wrapper the adversary's `pk(k)`, middle honest); `HonestAccepted` reachable (1611, 1794). 6 s | **termination, as predicted** — 0.45 branch; the timeout the plan concentrated here did not occur |
| Q5c companion, one level in (`sp7_q5c_companion_one_level_in`) | red at depth 2, green at depth 1 | `RescopedD2` **reachable** (728, 1131 — the middle wrapper is adversary-held `pk(k)`, `k ≠ skI2`, honest I2 bytes attributed to `(pk(k), idX)`); `RescopedD1` **unreachable** (690); `TypeConfused`, `InnerSigTransplanted` unreachable (652, 1169); `HonestWrappedAcceptedD1` reachable (1496); `HonestWrappedAcceptedD2` reachable (1876) **only through I1 wrapping its own attestation** (F7); `HonestAccepted` reachable (2097). 6 s | **red at depth 2 only, as required** |
| Q6a companion, identity from outermost (`sp7_q6a_companion_identity_outermost`) | red (0.8); recut (0.1); timeout (0.1) | `Rescoped` **reachable** (516, 806): honest I2 bytes, verified under `pk(skI2)`, attributed to identity `idX ≠ issuerId2` chosen by the adversary — its own wrapper identity; no `dsks`; `TypeConfused`, `InnerSigTransplanted` unreachable (503, 819); witnesses reachable (1118 via `pk(k)`, 1314) | **red as required** — 0.8 branch; the exhibited trace is the adversary-wrapper one, not the honest-only one the registration admitted |
| Q6b companion, key and authority from outermost (`sp7_q6b_companion_key_outermost`) | both red, `InnerSigTransplanted` through `dsks` (0.6); `Rescoped` only (0.25); reverse (0.05); timeout (0.1) | `Rescoped` **reachable** (498, 769): **re-sign route, zero `dsks` steps** — the adversary rebuilds I2's public frame, signs it under its own `k`, wraps, and the acceptance attributes it to `(pk(k), idX)`; `InnerSigTransplanted` **reachable** (778, 1058): `pk(dsks(sign((BYTES, fbI2), skI2), r))` — **the DSKS route**, the honest signature term verified under a derived key registered as the wrapper's; `TypeConfused` unreachable (489); `HonestWrappedAccepted` reachable (1067, 1317) only through **I1 wrapping its own attestation** (`kW = pk(skI1)`, F7); `HonestAccepted` reachable (1508) | **both red as registered, each by its registered route** — 0.6 branch |

Correct models green on every unreachability query and reachable on
every witness; every companion red on exactly its named query and
green on the rest (the `.out` lines above). `Reattributed` is declared
and fired by the transcribed S-P3 judge in every companion but
**queried only in Q1, Q2 and Q5** — the registration names the query
each companion must turn red and nothing else, and in Q6b the key-half
of `Rescoped` would make `Reattributed` red too (the S-P3 Q3 pattern of
an event fired and not queried; stated in each companion header).
*Recorded 2026-09-06 (cross-family review item 22):* the reviewer
restored the omitted query in every companion; it stays unreachable in
Q3, both Q4 configurations, Q5c and Q6a and is **red in Q6b** —
`RESULT not event(Reattributed(kExtra,kHonExtra,bytesExtra)) is false`
(`proverif/falsification-2026-09-06/scratch/audit_sp7_q6b_companion_key_outermost.pv`;
the reviewer's `.out` line 1338, re-run by the collaborator 2026-09-06
with the identical line). Not added as a query to any committed
companion; the Q6b header (line 91) lists the omission and the result.

N1/N2 (ENUMERATION note 3, PREDICTIONS "Fixture statement"): every
model carries **two** honest-flow witnesses — `HonestAccepted` on the
base path and `HonestWrappedAccepted` on the wrapped path (per depth in
Q5) — both emitted by judges, never bare acceptance; both reachable in
every model except Q4's two-version run, where `HonestWrappedAccepted`
unreachable *is* the registered red and the isolation config supplies
the green. Every model carries two honest inner issuers, two honest
wrapper issuers, two object types on each of the two inner-issuer keys
(I1 attests and wraps; I2 attests and signs `OT_REVIEWREC`; W1 and W2
sign wrappers only — divergence 7), two canonicalization versions
with a differing pairing (W1/`cvB` over I1/`cvA`) and a matching one
(W2/`cvA` over I1/`cvA`) — except Q4's two-version run, differing only,
as registered — and adversary-chosen payloads and adversary-chosen
wrapped blobs (chosen-message issuers **and** chosen-message wrappers).
Depth axis bound only by Q5/Q5c, as the headers say. *Recorded
2026-09-06 (cross-family review item 6):* every N1 witness is
existential — reachable with a trace for *some* honest key through
*some* wrapper — and is a **vacuity guard, not coverage**: reachability
for one honest key does not establish acceptance per branch or per key
(the reviewer's vacuity audit, `scratch/committed_audit.tsv`, confirms
every intended witness reachable in every committed `.out`, with Q4's
two-version `HonestWrappedAccepted` intentionally unreachable).

## Prediction divergences

Each quotes the registered text and states what was built instead. None
is a refinement; each is a divergence or a clarification of something
the registration left open.

1. **Q4 runs in strict mode (DNS key leaked), not degraded.** Registered
   text (Q4): "*Mutation: the wrapper commits to `reserialize(cvOuter,
   innerBytes)` instead of `innerBytes` … Required result:
   `HonestWrappedAccepted` unreachable.*" The registration names no mode
   for Q4 (Q3 and Q6 say "degraded"; Q4 does not), and the ordering rule
   says "Q2 before Q3, Q4, Q6 (a companion is evidence only against a
   matching correct form)". Built as written, the mutation lives in the
   **honest** wrapper's construction. In degraded mode the adversary
   holds an authorized wrapper identity and builds its own wrapper with
   the honest inner blob embedded opaquely — it never runs the mutated
   code — so `HonestWrappedAccepted(kH, fbI, kA)` is reachable and the
   required red cannot be exhibited by construction (probe
   `sp7_q4_probe_degraded_twoversion.out` 546/840, F6). The registered
   query was therefore run in **strict** mode (matching Q1, both
   channels required, DNS leaked), where every accepted wrapper is an
   honest — i.e. mutated — one. Recorded as a divergence in mode
   selection, with the degraded probe archived; the correct form it is
   evidence against is Q1. Only the DNS-leaked variant was run (the
   leaked channel is inert for this mutation; both channels still must
   sign every manifest). *Alternative not taken (added 2026-09-06, skeptic
   review 2):* keep degraded mode and key the witness on honest wrappers
   — a per-role witness selected on the wrapper's honest report
   (`honestTypeCh`), suite rule (ii) — so that only honestly built,
   i.e. mutated, wrappers count toward `HonestWrappedAccepted`. Not
   built because it changes the registered witness event rather than
   the mode, which the registration left open. Either encoding is a
   divergence; the collaborator judged this one smaller. Listed for veto.
2. **Per-depth event names in Q5/Q5c.** Registered: "`Rescoped` …
   unreachable at depth 2"; "companion Q5c … red on `Rescoped` at depth
   2 only; the same mutation at depth 1 must stay green". A single
   5-ary `Rescoped` cannot state "red at depth 2 only" (S-P3 recut 2's
   reason). Built: `RescopedD1`/`RescopedD2` and
   `HonestWrappedAcceptedD1`/`D2`, selected by the judge on the context
   constructor (`wctx` vs `wctx2`); `InnerSigTransplanted` and
   `TypeConfused` stay single. Encoding, not property; recorded here
   because the registered event names differ.
3. **Q5c's "same mutation at depth 1" is the correct depth-1 path.**
   Registered: "the verifier attributes the inner artifact to the frame
   *one level in* (correct at depth 1, wrong at depth 2)". At depth 1
   the frame one level in *is* the attestation, so the mutated rule and
   the correct rule coincide and the depth-1 path is Q5's unchanged
   code; the depth-2 path is where the rule diverges and is inlined.
   The green at depth 1 is therefore green by the rule's own content,
   which is what the companion isolates; stated so no reader infers a
   separately mutated depth-1 path exists.
4. **The registered Q2 header's load-bearing list is corrected by
   ablation before any author read.** Registered header text:
   "*Load-bearing for these queries: the inner frame's `(issuerId, kfp)`
   read and the `fp(kI) = kfp` match in the wrapped path (for `Rescoped`
   and `InnerSigTransplanted` …); the `objType` equality in each
   verifier (for `TypeConfused`). Carried, not load-bearing: the inner
   signature check (both levels) …*" Ablation (F2, F3) shows: the
   frame's `=fp(kI)` match alone pins the attributed **key** (a17) but
   not the attributed **identity**, which needs any one of the frame's
   `=idI`, the manifest hash, or possession-over-manifest (a18) — so the
   `=idI` match is redundant *given the other two* (a01, a03, a05); and
   the inner **signature
   check is load-bearing for `InnerSigTransplanted`** (not carried).
   The Q2/Q1/Q5 headers say this now; the registered text is left as
   written in `PREDICTIONS.md`.
5. **The adversary's wrapper identity `idA` is not a process.**
   Registered: "the adversary holds a wrapper identity `idA` with key
   `kA`, self-signed manifest, and channel evidence it minted itself".
   With the sole channel key public, every one of those is a term the
   adversary builds; `idA` is declared as a free name for trace
   readability only, and ProVerif's traces use its own fresh `k` and
   `idX`. Same fixture, no honest process for it.
6. **`Reattributed` unqueried in companions** — see the paragraph under
   the table. The registration lists `Reattributed` for Q1 only; it is
   kept as a query in Q2 and Q5 (harmless, green) so that "nothing in
   S-P7 may weaken what S-P3 established" is checked on the claim
   models too.
7. **"Each honest key signs objects of at least two types" — the
   parenthetical's two-key reading was built.** Registered (Q3 fixture
   sentence): "*each honest key signs objects of at least two types (an
   issuer that both attests and wraps; the second honest key also signs
   an `OT_REVIEWREC` object)*". Built, in every model (Q2 process lines
   321–323): `skI1` signs `OT_ATTEST` and `OT_WRAPPER`; `skI2` signs
   `OT_ATTEST` and `OT_REVIEWREC`; **`skW1` and `skW2` sign only
   `OT_WRAPPER`**. This matches the parenthetical and the global fixture
   statement ("at least two object types signed by the same honest key")
   but not the literal "each honest key". Recorded as the reading taken
   (skeptic review 2026-09-06); F5 notes that the exhibited Q3 route
   (W2's wrapper accepted as an attestation) needs no two-type key at
   all, so the fixture choice does not bear on the red.
8. **Ledger entry 1's consumer list (added 2026-09-06, skeptic review
   2).** Registered (`PREDICTIONS.md` 485–486, ledger entry 1):
   "*Consumers: S-P1 (integrity over bytes of this type) …*". S-P1's
   frozen plan (`formal/suite/s-p1/PREDICTIONS.md` 450–453, same
   commit) declines: "*S-P1 consumes nothing from S-P7 … S-P7's
   producer entries naming S-P1 as a consumer … are S-P7's claim, not
   carried here.*" Conversely S-P1's producer entry 4 (459–466) names
   S-P7 as a consumer of the authorship correspondence, and the
   registered S-P7 ledger lists no S-P1 entry under "consumed from
   elsewhere". Both are corrected in this file's ledger (entry 1 and
   "Consumed from elsewhere"); the registered text is left as written.
   Ledger fields only; no query, result or `.out` is touched.

## Recuts (encoding, not property)

**None.** The registered p≈0.25 (Q1) / 0.3 (Q4) / 0.2 (Q5) recut
branches did not fire. Two build errors were fixed before the first
successful run of Q2 and are recorded as tool notes, not recuts (no
model had run): (a) a comment containing the literal `STMT_*)` closed
the header early — ProVerif comments cannot contain `*)`; (b) variables
bound inside a **tuple** nested in a data-constructor pattern
(`wrap(cvIw, (fbI, sgI))` in a `let`) must be typed explicitly, unlike
variables directly under a declared constructor. Both are in the
run-1-equivalent history of the file only; no `run1/` directory exists
because no query result changed at any point. The suite rules from S-P3
(parallel judge reports, honest-flow witnesses, no shadowing) were
applied from the first line; ProVerif reconstructed every reachable
goal to a trace, no "cannot be proved".

**Header recut 2 (comment-only), 2026-09-06, skeptic review 2.** The C1
sentence in the Q2 header (line 23), both Q1 headers (line 17) and the
Q5 header (line 21) now names the model's acceptance paths — as an
attestation (`InnerCheck`) and as a wrapper (`VerifierWrapped`; in Q5
also the outer and middle checks of `VerifierWrapped2`) — no other kind
is accepted anywhere, so "accepted as another" means "accepted as an
attestation or as a wrapper under another signed type". Edits kept on
the existing lines (line-count neutral: Q2 stays 325 lines, Q1 260, Q5
295), so every `file:line` citation stands; the full ladder was re-run
(`run_ladder.sh`, `ladder.log` refreshed) and every `.out` compared
byte-for-byte with its pre-edit copy — see the review log entry for the
result.

## Ablations (unregistered; `proverif/ablations/`, all on Q2, box 1800 s each, all ≤ 3 s; runner `run_ablations.sh`, log `ablations.log`)

a01–a16 were run 2026-09-06 with the results below; a17 and a18 were
added the same day after the skeptic review of this file (F2's "alone
suffices" was untested: a04 and a07 each remove *one* of the slot /
manifest-hash checks, never both). All eighteen plus p01 were then
re-run through `run_ablations.sh` (with the mandated STATUS header
added to a01–a16, comment-only); every `RESULT` line is identical to
the hand runs. Every ablation carries the PROPOSED / UNREGISTERED header.

| Ablation | Removed from `InnerCheck` / `VerifierWrapped` | `TypeConfused` | `Rescoped` | `InnerSigTransplanted` | `Reattributed` |
|---|---|---|---|---|---|
| a01 | frame `=idI` (read) | green | green | green | green |
| a02 | frame `=fp(kI)` (read) | green | green | green | green |
| a03 | both `=idI` and `=fp(kI)` | green | green | green | green |
| a04 | `mhI = h(tI)` | green | green | green | green |
| a05 | `=idI` and `mhI = h(tI)` | green | green | green | green |
| **a06** | `=fp(kI)` and `mhI = h(tI)` | green | **red** | **red** | **red** |
| a07 | slot `fp(kI) = kfprI` | green | green | green | green |
| a08 | inner possession | green | green | green | green |
| **a09** | `=fp(kI)` and slot | green | **red** | **red** | **red** |
| **a10** | outer `=OT_WRAPPER` (read) | **red** | green | green | green |
| **a11** | inner signature check | green | green | **red** | green |
| a12 | inner authority evidence | green | green | green | green |
| a13 | outer frame `=fp(kW)` | green | green | green | green |
| a14 | `=fp(kI)`, slot, `mh` | green | red | red | red |
| a15 | `=idI`, `=fp(kI)`, slot, `mh` | green | red | red | red |
| a16 | inner signature and `=fp(kI)` | green | green | red | green |
| a17 | slot **and** `mhI = h(tI)` (`=fp(kI)`, `=idI`, possession kept) | green | green | green | green |
| **a18** | slot, `mh`, `=idI` (read) **and** inner possession — `=fp(kI)` alone kept | green | **red** — identity half only: `Rescoped(pk(skI2), idX, pk(skI2), issuerId2, …)`, `.out` 499/805 | green | green |

Both witnesses stayed reachable in every ablation. Probe p01 (on Q3) is
described in the table above.

## Findings

**F1 — C2 holds in the hard case, and "innermost" has content.** In
degraded mode with the sole channel compromised and the adversary
holding an authorized wrapper identity, a wrapped presentation of an
honest attestation is never accepted with the inner artifact attributed
to any `(issuerId, key)` but the inner frame's (Q2); at depth 2 the
attribution is never the middle wrapper's and never the outermost's
(Q5). The wrapper lends nothing to the inner check because the inner
check *is* the standalone check (`InnerCheck`, one process macro
invoked from both paths) reading identity and key from the innermost
frame. C1 holds alongside it (`TypeConfused` unreachable everywhere the
tags are checked).

**F2 — Where the load sits: the innermost frame's fingerprint field
for the key; any one of three routes for the identity; S-P3's
dependency statement reproduced on the wrapped path for the key half.**
The frame's `=fp(kI)` match alone pins the attributed **key** (a17
green with slot and manifest hash both removed; a06/a09 red without it
unless slot and `mh` are both present, a02); **it does not pin the
attributed identity** — with `=idI`, `mh` and possession all removed
and `=fp(kI)` kept, `Rescoped` is red on the identity half (a18: honest
I2 bytes, key `pk(skI2)`, attributed to an adversary-chosen `idX`).
Absent `=fp(kI)`, the slot check `fp(kI) = kfprI` and the manifest-hash
check together compensate for the key (a02 green) and neither alone
does (a06, a09 red). The frame's `=idI` match is redundant *given
either of the other two identity routes* (a01, a03, a05 green): the
attributed identity rides on the manifest, which is pinned by the
manifest hash and, independently, by possession-over-manifest under the
pinned key — remove all three and nothing pins it (a18). *Correction
record:* this finding first read "alone suffices against re-scoping
(a04, a07 green with it present)"; no archived ablation had removed
both slot and `mh`, so "alone" was untested; the skeptic review of
2026-09-06 ran the two missing configurations, archived as a17/a18. So the honest sentence
for what Q2 discharges is S-P3 F5's, one level up: *under a perfect
fingerprint, no wrapper — honest or adversary-authorized — can move
the attribution of honest inner bytes to another key or identity.* The
whole load is the `fp` idealization (Layer 2, library header) plus, for
the identity half, `h` or possession. Same P8 golden-vector
recommendation as S-P3 F3: exercise the fingerprint route and the
manifest-hash route separately.

**F3 — `InnerSigTransplanted` is the one S-P7 query whose green depends
on the inner signature check being present.** Removing
`checksign(sgI, kI)` (a11) makes it red: the adversary presents its own
frame under its own key with I2's honest signature term dangling beside
it, and the judge — keyed on the signature *term* the verifier reports
as verified — fires. This is the judge doing what it was registered to
do (distinguish the DSKS route from the re-sign route by term identity)
and it exposes a scope condition: the judge is meaningful only when the
verifier reports the signature it actually verified. It does **not**
depend on signature *security* beyond the registered DSKS theory — in
the unablated model, `dsks` appears in no baseline derivation, and the
frame's `=fp(kI)` still pins the key. Consequence for the ledger: entry
2's `InnerSigTransplanted` producer cites the signature check as
load-bearing (presence); the check's *security* is consumed from S-P1's
authorship correspondence (S-P1 producer entry 4,
`formal/suite/s-p1/PREDICTIONS.md` 459–466), not established here.
(This sentence first named S-P1 the *consumer* of the check's security
— the direction inverted; corrected 2026-09-06, skeptic review 2.)

**F4 — Where DSKS bites: exactly where registered.** Of the twelve
runs, only Q6b's `InnerSigTransplanted` derivation touches `dsks`
(`.out` 778 onward: `pk(dsks(sign((BYTES, fbI2), skI2), r))`
registered as the wrapper key through the compromised channel). Q6b's
`Rescoped` is the re-sign route with zero `dsks` steps (498–769) — the
adversary rebuilds the public honest frame (`framed` is `[data]`, every
field public, the manifest hash computable) and signs it under its own
key, S-P3 F2 in wrapped form. The 0.25 branch (mutation still pins the
key somewhere) did not fire: with the key taken from the wrapper and
the frame's `kfp` read but not matched, nothing pins it. With the
naming and matching checks present, DSKS added no attack anywhere in
the ladder — the design working, as S-P3 F4 said.

**F5 — Nothing but the tag discriminates the types.** Q3's red and its
route probe p01 show both base-path confusions reachable (`OT_WRAPPER`
and `OT_REVIEWREC` objects accepted as attestations) and a10 shows the
wrapped-path confusion reachable when its `=OT_WRAPPER` is dropped: an
honest attestation whose adversary-chosen payload is a `wrap()` term is
accepted as a wrapper. The registered 0.15 branch — the manifest hash
or payload shape already discriminates — did not fire, and the reason
is structural: the manifest names a key, not a type; the payload is
adversary-chosen; the signature covers whatever frame the honest key
signed. An honest key that signs objects of two types (the fixture) is
not required for the confusion — Q3's trace confuses W2's wrapper, and
W2 signs only wrappers — but it is what gives the type axis two honest
values. Amendment-trigger criterion (Grok panel) satisfied: the theory
expresses A1.3 item 4 among framed kinds. The **non-framed kinds
remain the open coverage cell** (below).

**F6 — A companion whose mutation lives in honest code needs a mode
where the adversary has no honest-equivalent role.** Antigravity's
re-serialization is a bug in the *honest* wrapper implementation. In
degraded mode the adversary is itself an authorized wrapper that
embeds honest bytes opaquely, so the honest-wrapper bug is
unfalsifiable there (probe: `HonestWrappedAccepted` reachable with
`kW = pk(k)`). This is not a weakness in P7 — an adversary wrapper that
embeds correctly attacks nothing — but it is a suite rule worth
carrying: **run honest-code companions in the mode where every
accepted instance of the role is honest** (here strict). The added
opaque control shows the version mismatch itself is harmless: with
`cvA` inner and `cvB` outer and a correct wrapper, the honest inner
wrapped acceptance is exhibited (`HonestWrappedAccepted` reachable, 926)
— *correction 2026-09-06 (cross-family review item 20):* this sentence
first read "is accepted inside the wrapper exactly as standalone"; no
relational query states that equality and the shared-`InnerCheck`
argument is conditional on reaching `InnerCheck` with identical inputs,
so the control shows an existential witness under differing versions,
not an equality of acceptances. Together with the
two-version red and the isolation green, that is the full witness /
control pair ledger entry 3 promised. The `reserialize` destructor
fired in resolution without a recut.

**F7 — Witness traces go through the shortest wrapper, which is often
the adversary's or the issuer's own.** In every degraded correct model
the `HonestWrappedAccepted` trace uses the adversary's own key as the
wrapper (`pk(k)`, `attacker(k)`), because ProVerif reconstructs the
shortest derivation and an honest wrapper session is longer; in the
strict models it is honest `skW2`. So the wrapped-path N1 witness says
"honest inner bytes attributed correctly inside *some* authorized
wrapper", which is the registered sentence; that honest wrappers also
work is shown by Q1 and Q4-isolation. In Q6b and Q5c the witness goes
through **I1 wrapping its own attestation** (Q6b: `kW = pk(skI1)`, `idW
= issuerId`, `.out` 1067; Q5c: the *middle* wrapper is I1 — `pk(skI1)`,
`issuerId` — and the outermost is the adversary's `pk(k)`, `.out` 1535,
`AcceptMiddle` at 1864 in the trace; this parenthetical first gave
`kW = pk(skI1)` for both, wrong for Q5c — corrected 2026-09-06, skeptic
review 2) — the fixture's "issuer that both
attests and wraps" is a path on which a mutation that attributes to the
wrapper still attributes correctly. In **Q6a** the exhibited witness is
different: the **adversary's own wrapper key `pk(k)`**, registered
through the leaked channel under the honest identity string `issuerId2`
(`.out` 832: goal `HonestWrappedAccepted(pk(skI2), framed(OT_ATTEST, …,
issuerId2, …), pk(k))` with hypothesis `attacker(k)`; derivation
958–985 builds `authTuple(issuerId2, fp(pk(k)), ssW_1, algW_1, verW_1)`
and `framed(OT_WRAPPER, algW_1, issuerId2, fp(pk(k)), …)`), so the
mutated attribution (`idW`) coincides with `idH` **by the adversary's
choice of manifest identity, not by an honest wrapper**. (This paragraph
first described Q6a's witness as the I1 self-wrap; the table row "1118
via `pk(k)`" was right and the prose wrong — corrected 2026-09-06 from
the skeptic review.) A reader must not take a reachable
`HonestWrappedAccepted` in a companion as evidence the mutated path is
correct for third-party wrappers; it shows the mutated path *accepts
something honest*, which is all N1 asks. The Q5c red trace uses an
adversary-held middle wrapper; the registration's honest-only trace
shape (Q6a) was not the one exhibited but is also reachable in
principle (under Q6a every wrapped acceptance whose wrapper identity
differs from the inner signer's misattributes — *correction 2026-09-06,
cross-family review item 20:* this parenthetical first said "every
honest wrapped acceptance misattributes", overstated; when `idW = idH`,
as in the I1 self-wrap route and the Q6a witness itself, the attribution
coincides; the Q6a header line 11–12 is narrowed the same way).

**F8 — What the acceptance event carries, and what it does not decide.**
`AcceptInner(wctx(kW, idW, fbW), kI, idI, fbI)` records both pairs. An
adversary-authorized wrapper enclosing honest bytes is *accepted*, with
the inner attributed to its honest signer and the wrapper to the
adversary — the model calls this the honest flow, because it is: the
wrapper's authorship is S-P3's relation applied to the outer object,
and what a wrapper's endorsement *means* to a relying party is the
adjudicator's question under Amendment 4 §A4.6, not the verifier's.
S-P7 establishes only that the wrapper cannot re-scope the inner. Note
also, from the Q6a witness (F7): in degraded mode an adversary wrapper
may carry an **honest issuer's identity string** in its own manifest —
own key, own bytes, honest name — and be accepted as that wrapper; this
is the 2026-09-05 ruling's verifier's-cost case (fresh-signature
impersonation under a usurped identity with the sole channel
compromised), reachable by construction and outside every S-P7 query,
all of which are keyed on honest bytes or honest signature terms. The
relying-party story should say that a wrapper is a signed claim *about*
an inner artifact whose own verdict is unchanged, and that the
verdict names both signers — and that in degraded mode the wrapper's
*name* is only as good as the channel that vouched for it.

**F9 — The cross-level confusion Q5's fixture can exhibit is caught by
the type tag, not by depth logic.** A depth-2 presentation handed to
the depth-1 path fails at `InnerCheck`'s `=OT_ATTEST` on the middle
wrapper's bytes; a depth-1 presentation handed to the depth-2 path
fails at the middle `=OT_WRAPPER` on the attestation's bytes. There is
no depth counter; "innermost" is "the first `OT_ATTEST` frame reached
by unwrapping `OT_WRAPPER` frames", bounded at 2 hand-written paths.
Nothing is claimed beyond depth 2.

**Dependency statement (from the ablations, Q2):** the innermost
frame's fingerprint field alone suffices against **key** re-scoping
(a17); the tuple-fingerprint match and the manifest-hash check together
compensate for its absence, and neither alone does (a02; a06, a09); the
frame's identity field is redundant given either one of the manifest
hash or possession-over-manifest, and **not** given the fingerprint
routes alone (a18 red); the inner signature check and the fingerprint
route are jointly necessary against signature-term transplant; the
object-type equality in each verifier is individually necessary against
type confusion on that verifier's path.

*Cross-family check of this statement, 2026-09-06 (review items 4 and
5).* The reviewer's 198-mutant single-guard matrix
(`proverif/falsification-2026-09-06/scratch/guard_groups.tsv` rows
2–16, `dependencies.tsv`) covers Q1d, Q1r, Q2, Q4c and Q5 directly and
agrees with the Q2 ablations everywhere they overlap: every single
removal is green except the frame type equality on each path — with
one exception the reviewer names, Q4c's inner path, where
`q4o_I_type` is green because the `canon(cvc, framed(...))` shape
already discriminates that fixture (row 12; a10, Q3) — the inner
signature check (row 9; a11) and, in Q2 and Q5 only, its bytes
equality (row 11). *(Corrected 2026-09-06, second cross-family pass,
PROPOSED: this summary was first written as a matrix-wide claim over
the Q1d/Q1r/Q2/Q4c/Q5 columns and so named a singly-GREEN cell as
individually load-bearing — the class of overclaim item 4 exists to
remove. Narrowed to name the one green cell,
`q4o_I_type:unchanged` (guard_groups.tsv row 12;
`dependencies.tsv:117`; review §3). Rows 9, 11 and 15 as cited are
accurate; no query, RESULT line or prediction is affected.)* Two
consequences applied to the headers: (a) "load-bearing" is **joint** unless a single removal is
named red — in particular the innermost `=fp(kI)` match's single
removal is green (a02; row 15) and it is load-bearing jointly with the
slot and manifest-hash checks, which the Q2 header's a02/a06/a09 record
already said under a "load-bearing" label (item 4; Q2 header lines
30–31, Q1 headers 28–38, Q5 header 35–38); (b) in Q1 the **honest**
channel's evidence check is individually inert — the reviewer's mutants
`q1d_I_evRI_evidence` and `q1r_I_evDI_evidence` (repository honest in
Q1d, DNS honest in Q1r) leave every RESULT line unchanged (554/567/580/
593 true, 921/1125 false; re-run by the collaborator 2026-09-06,
identical) — so the Q1 headers' "Load-bearing for these queries: the
honest channel's evidence check" is narrowed to *jointly load-bearing,
defence in depth*, the S-P3 F5 shape: the manifest-hash and fingerprint
pins carry the relation on their own (item 5, Accepted as a header
correction and Recorded as defence in depth). Inert ≠ removable: single
removals do not license joint removal (a06/a09/a14/a15/a18 are the
joint reds), and the reviewer notes inertness flips under composition.

## Ledger entries (A3.3 conservation fields) — offered, not entered

1. **Type-soundness relation (producer: Q2/Q1, `TypeConfused`
   unreachable; Q5 at both depths).** Consumers: S-P2 (a signature set
   over a manifest is not one over an attestation — but see the open
   cell: the manifest is a non-framed kind), the capstone's per-layer
   linkage. **S-P1 declines this relation** (`formal/suite/s-p1/
   PREDICTIONS.md` 450–453, frozen `5188e7a`: "S-P1 consumes nothing
   from S-P7" — object type is an opaque frame field there) — the join
   is composed at the capstone, not consumed by S-P1. *Dated note,
   2026-09-06 (skeptic review 2):* this entry first read "Consumers:
   S-P1 (integrity over bytes of *this* type), S-P2, …", carrying the
   registered ledger text (`PREDICTIONS.md` 485) — the ENUMERATION
   note-6 pattern (a producer entry recording a join the other side
   does not carry); the registered text is left as written and the
   correction recorded as divergence 8. Assumed fact:
   acceptance of framed bytes on a path *as* type `T` implies the bytes'
   committed `objType` is `T`. Shared term: `objType` in the frame.
   Adversary at the join: A1.3 with DSKS, sole channel compromised,
   adversary-chosen payloads (a payload may be a `wrap()` term).
   Severing companion: Q3 (base path) → `TypeConfused` red; ablation a10
   (wrapped path) → red. Residuals (Layer 2): P8 type-tag bytes and that
   the enumeration's bytes are these eight and no others; `h`, `fp`
   idealization; deterministic signatures; **non-framed kinds
   unrepresentable** (open cell).
2. **Scope relation (producer: Q2 and Q5, `Rescoped`/`RescopedD1`/
   `RescopedD2` unreachable; `InnerSigTransplanted` unreachable).**
   Consumer: **S-STANDING** — the entitled-key check inside the standing
   path (ENUMERATION note 4 item 2) takes the artifact's `(issuerId,
   kfp)` from this relation, never from a wrapper; A3.7.1's "issuance
   identity" is, for a wrapped artifact, the innermost frame's (A7
   ruling 2026-09-06: S-STANDING carries the wrapper-shaped transplant;
   S-P7 supplies the identity relation it composes with). Assumed fact:
   acceptance of a wrapped presentation with inner bytes `fbI` attributes
   `fbI` to `(idI, kI)` where `fbI`'s committed `(issuerId, kfp)` is
   `(idI, fp(kI))`, and honest inner bytes are never attributed to
   another pair; the honest inner signature term is never **accepted**
   under another key (*corrected 2026-09-06, cross-family review item
   19:* first "never verified" — the primitive can succeed under a
   DSKS-derived key before the `=fp(kI)` pin rejects; the judge reports
   acceptance). Shared terms: attributed key, attributed identity, inner
   framed bytes, inner signature term. Adversary at the join: A1.3 with
   DSKS, sole channel compromised, adversary-authorized wrapper, depth
   ≤ 2. Severing companions: Q6a (identity, `Rescoped` red, no DSKS),
   Q6b (key/authority — `Rescoped` red by the re-sign route, no DSKS;
   `InnerSigTransplanted` red **via `dsks`**), Q5c (depth,
   `RescopedD2` red only). Load-bearing (F2, F3): innermost frame
   `=fp(kI)` (or slot + manifest hash) for the **key** half; any one of
   the frame's `=idI`, the manifest hash, or possession-over-manifest
   for the **identity** half (a17, a18); inner signature check for the
   signature-term half. Residuals: as entry 1, plus depth bounded at 2;
   `fp` collision resistance and what a fingerprint hashes (P8).
3. **Commitment relation — by construction, not a producer.** No query
   states C3. It is encoded by `InnerCheck` being one macro invoked from
   both paths (`sp7_q2` lines 246–264, 283) and by `wrap()` carrying the
   inner bytes as a term. A3.3 conservation fields, given explicitly so
   the entry is not mistaken for a producer (skeptic review 2026-09-06):
   *producer module and event/query* — none; by construction, not a
   producer; *consumer property/query* — none; **S-P1 may not consume**;
   *assumed fact* — none stated (no query asserts "wrapping never alters
   the inner verdict"; the witness/control pair below is companion
   evidence only); *adversary at the join* — as entry 2 (A1.3 with DSKS,
   sole channel compromised, adversary-authorized wrapper, depth ≤ 2),
   and strict mode for Q4 per divergence 1; *shared term* and *residual*
   — below. What the ladder supplies: `HonestWrappedAccepted`
   reachable (Q1, Q2, Q5, Q4-isolation, Q4-control) as witness, and Q4's
   two-version red as the control that the checking arrangement detects
   re-serialization — companion evidence, "discharges nothing of the
   property". **S-P1 may not consume this entry as discharged.** The
   relying-party sentence "wrapping cannot break an honest inner
   package" rests on the by-construction encoding plus this control and
   must say so. Shared term: inner framed bytes. Residual: opacity of
   the concrete embedding (P8/H1a) — the largest Layer 2 residual here
   and the one Antigravity's finding is about; nothing about *what*
   changes between canonicalization versions is modeled.

Consumed from elsewhere: **S-P3 entry 1** (key binding — the wrapper's
and the inner's authorship are each S-P3's relation; S-P7 transcribes
the checks, and its ablations a13/a11 show the outer checks carried and
the inner signature check load-bearing only for entry 2's signature-term
half), **S-P3 entry 2** (possession over manifest, both levels; a08
shows it carried for these queries), and — added 2026-09-06, skeptic
review 2; omitted in the first draft — **S-P1 entry 4** (authorship:
accepted bytes = signed bytes under the accepted key;
`formal/suite/s-p1/PREDICTIONS.md` 459–466, which names S-P7 as its
consumer): presupposed by the inner signature check at both levels
(`sp7_q2` lines 252 and 278) and by entry 3's by-construction encoding;
S-P7 transcribes the check and its ablation a11 shows it load-bearing
only for `InnerSigTransplanted`; the check's *security* is consumed from
S-P1, never re-proved here. *Added 2026-09-06 (cross-family review item
8, the ledger entry):* S-P1's review entered a named assumption,
**key-use discipline** — an issuer key signs only framed objects under
their domain tag, never raw payloads (the reviewer's A8 composition
break: a second honest endpoint signing a payload-only message under
the same key lets an attacker-chosen frame be accepted). S-P7 consumes
it with S-P1 entry 4: every honest key in this fixture signs only
`(BYTES, framed(...))` frames and `(POSS, manifest)` self-signatures
(Q2 lines 203–206, 220–225, 234–238), so the assumption holds here by
construction and is not tested; an issuer that signs unframed bytes is
outside every S-P7 model. **Cross-formalism joins: none
consumed** (A7 ruling: the §4 refusal-latch join belongs to S-STANDING).
Recorded so the capstone does not look for one here.

## What S-P7 does not discharge

- Opacity of any concrete embedding, canonicalization semantics, what
  bytes distinguish the eight types — P8/H1a.
- **C1 across non-framed kinds — open coverage-map cell, kept open and
  visible.** The manifest (`authTuple`), possession proof (`POSS`) and
  authority evidence (`STMT_DIRECT`/`STMT_DIGEST`) have no object-type
  field and are distinct library constructors; a symbolic companion
  confusing one with a framed object is green by constructor, not by
  tag (ENUMERATION note 1 item 1 / guide M5). Byte-level; **P8
  golden-vector obligation**; not a query here. The two Amendment-4
  types (`OT_TLR`, `OT_REFUSAL`) are declared by the library and
  unexercised here (S-STANDING's).
- Anything at nesting depth > 2; the three unexercised original types
  beyond declaration.
- Standing, lineage, terminal disposition, the TLR, the wrapper-shaped
  standing transplant — S-STANDING (A7).
- Authorship of the wrapper or inner object as a *proved* relation —
  consumed from S-P3.
- Impersonation with the adversary's own key over its own bytes at
  either level — reachable, the verifier's cost (2026-09-05 ruling
  under S-P3 F8; Amendment 4 §A4.6).
- P7's TLA+ leg (the "independently-computed verdict" sentence as a P4
  verdict-partition claim) — open cell for the claim-level coverage
  map, as registered.
- Whether the wrap-recorded inner version must equal the inner frame's
  `canonVer` field — both are bound, neither is compared (presence
  only); P8's. *(See "Pending author ruling (ROUTED C9)" below,
  2026-09-06.)*
- *Added 2026-09-06 from the cross-family review (Boundary items):*
  **package completeness / self-containment** (item 21) — the embedded
  pair `wrap(cvIw, (fbI, sgI))` carries the inner bytes and signature;
  the inner manifest, evidence and possession are presenter-supplied
  outside it (Q2 lines 272–273) and no query asks that they travel in
  the bundle, so P7's "the inner bytes must travel inside the bundle, or
  P9's self-containment fails" is exercised only for the bytes and
  signature; recorded as an **open coverage cell** on
  `formal/COVERAGE-MAP.md` row 8 (amendment note appended there) — a
  P8/H1a format obligation, not a symbolic one. **Signature-set
  operations** (A1.3 item 2; item 1) — one signature slot per layer;
  stripping, reordering and duplication are S-P2's subject (n ≤ 2
  there). **Byte-encoding attacks** (item 2) — non-canonical encodings,
  hash-input ambiguity, cross-kind parse confusion: term equality stands
  in for byte equality and distinct constructors never confuse; in the
  reviewer's phrase, adopted here, *a coverage failure, not an
  unreachable attack* — P8's injectivity obligation and the library's
  `h`/`fp` idealization (Layer 2). **Verdict values, waiver records,
  policy inputs** (item 3) — none anywhere; P4's partition and the
  `Accept` ↔ P4 cross-formalism join (author ruling 2026-08-29).

**Suite rules S-P7 adds** (offered, carried to S-P1/S-P2/S-STANDING and
the capstone): (i) a companion whose mutation is in honest role code
runs in the mode where every accepted instance of that role is honest
(F6); (ii) when a witness or red must be stated per depth or per role,
per-depth/per-role events selected on a context constructor are the
encoding (S-P3 recut 2, generalized); (iii) a judge keyed on a
signature *term* depends on the verifier reporting the term it actually
verified (F3) — its header must say the signature check is load-bearing
for it; (iv) chosen-message *wrappers* (the honest wrapper wraps
whatever blob the adversary hands it) are the conservative fixture and
cost nothing.

On companions, unchanged from S-P3: they discharge nothing of the
property; what they supply is evidence that the checking arrangement can
detect the intended failures.

**The question the cold read answers** (S-P3's, adopted): *Does this
model preserve the attack and the defense we intend to study, and have
we assigned every omitted detail to an explicit remaining obligation?*

## Status toward discharge (PROPERTIES.md terms)

Tool passes: **yes** — all correct models green, all required companions
red on their named queries only, red/green pattern for Q4 complete, all
witnesses reachable. Agreement-gate falsification review by non-author
models: **NOT RUN** (ENUMERATION note 5 item 1 requires a reviewer from
a different model family before the queries are accepted) — *amended
2026-09-06:* **RUN** (Codex `gpt-6-astra`; the review document named in
the header); the reviewer reproduced every committed RESULT line before
mutating, and no registered query, prediction or verdict changed; the
family's *self-description* did not survive unchanged — four header
sentences narrowed (items 4, 5, 19, 20), two facts recorded (6, 22),
four boundaries written into the reading aid (1, 2, 3, 21), one design
question routed (18 → C9). Author read:
**pending** — suggested read, per the standing rule: `sp7_q2_degraded_compromised.pv`
lines 13–83 (header: claim, load-bearing, does-not-prove) and 246–283
(`InnerCheck`, `VerifierWrapped`), against P7's registered sentences
and ENUMERATION §2's sharpening; one question — *does the narrowed
header say what that verifier does, no more?* — about twenty minutes.
Recommendation (collaborator): P7's symbolic leg → `checked` on that
read plus one cross-family falsification pass; `discharged` waits on
the P8 obligations named above and on the TLA+ leg / open cells being
placed on the coverage map.

**ROUTED TO AUTHOR: none** *(as of the first draft)*. The eight
divergences above are settled from the registration's own text and are
listed for veto, not decision; no fork was found that the record does
not already answer.

**Pending author ruling (ROUTED C9)** — added 2026-09-06 from the
cross-family review, item 18 (`formal/suite/ROUTED-2026-09-06.md` C9;
the author has not ruled). The wrapper's recorded inner canonicalization
version (`cvIw` in `wrap(cvIw, (fbI, sgI))`, Q2 line 279) is never
checked against the inner frame's `canonVer` (`cvI`, line 253); the
reviewer's `attack_version_lie` (archived under
`proverif/falsification-2026-09-06/scratch/`) has an honest wrapper
record an arbitrary `cvInner` over an honest `cvA` attestation, both
objects are accepted, and an observer comparing the two fires
(`RESULT not event(BadVersion) is false`, the reviewer's `.out` line
809). P7 says the wrapper "records both inner and outer canonicalization
versions"; nothing registered says the record must be *true*, and every
S-P7 header says "presence only". *What would change on yes:* `InnerCheck`
on the wrapped path gains the equality recorded-inner-version = inner
frame's `canonVer` — `cvIw` is read at Q2:279 in `VerifierWrapped` and
`cvI` at 253 inside `InnerCheck`, so either `InnerCheck` takes the
recorded version as a parameter and matches `=cvIw` at 253, or the
wrapped path compares the two after the inner frame read; the base path
has no recorded version and is unchanged — a lying-wrapper companion
goes red, and both
are recorded under a "Post-freeze additions (unregistered)" heading in
this file with their RESULT lines, in the S-P3 precedent — never as a
registered prediction. *On no:* the record is informational; the
headers' "presence only" stands and the reading aid says a wrapper's
version record is unverified (it does already, §9 item 6). Nothing has
been changed pending the ruling.

## Review log

- 2026-09-06 — models built from the frozen plan (`5188e7a`), the S-P3
  template and suite rules, and the library with D-5/D-6. Q2 first
  (two build fixes, no result change), then the ladder in registered
  order; every registered query on its primary branch; no recut; two
  unregistered Q4 runs (control, probe) and sixteen Q2 ablations plus
  one Q3 route probe archived under `proverif/ablations/`. Q2/Q1/Q5
  headers corrected from the ablations (divergence 4). Collaborator
  throughout; no falsification review; no author read.
- 2026-09-06 — **skeptic review of this results set** (same-family,
  Claude; not the cross-family gate). Three defects and six nits, all
  applied by the collaborator: (1) F7's and READING-AIDS §7's Q6a
  witness description contradicted the `.out` (the witness is the
  adversary's `pk(k)` under the honest identity string `issuerId2`, not
  I1 self-wrapping) — corrected, and F8 gained the degraded-mode
  honest-name sentence; (2) F2's "`=fp(kI)` alone suffices" had never
  been tested (a04/a07 remove one check each) and is false for the
  identity half — two ablations added, **a17** (slot + `mh` removed:
  green) and **a18** (`=fp(kI)` alone kept: `Rescoped` red on identity),
  and F2, divergence 4, the dependency statement, ledger entry 2, the
  Q2 header (lines 32–42, 58–59) and both Q1 headers (lines 32–33)
  reworded; (3) a01–a16 lacked the mandated STATUS: PROPOSED line —
  inserted (comment-only). Nits: READING-AIDS §5/§6 line ranges
  (202–214, 189–201); `run_ablations.sh` added and every ablation
  re-run through it (all lines identical to the hand runs); ledger
  entry 3 given its six A3.3 fields; divergence 7 (two-type fixture
  reading) recorded; the library's uncommitted state noted in Tooling.
  Also found while applying: every Q1 line citation in READING-AIDS §2
  was off by one (the aid assumed a 259-line file; the file is 260
  lines) — corrected there. **Recut record:** the three `.pv` header
  edits are comment-only and **line-count neutral** (Q2 stays 325
  lines, Q1 260), so every `file:line` citation stands; the full ladder
  was re-run (`run_ladder.sh`, `ladder.log` refreshed) and every one of
  the twelve `.out` files is byte-identical to its pre-edit file — no
  query, result, trace or `.out` line number changed. **Timing shift
  (B7):** `PREDICTIONS.md` line 609 says the D-5/D-6 library change
  "rides in the author's freeze commit"; the freeze commit `5188e7a`
  does not contain it and it is uncommitted as of this entry — it rides
  in the author's commit of this results set instead. Still no
  cross-family falsification review; still no author read.
- 2026-09-06 — **skeptic review 2 of this results set** (same-family,
  Claude; not the cross-family gate). One defect and five nits, all
  applied by the collaborator: (1) ledger entry 1 named S-P1 a consumer
  of the type-soundness relation, which S-P1's frozen plan declines
  (`s-p1/PREDICTIONS.md` 450–453), and the ledger omitted the join S-P1
  entry 4 does carry (S-P7 consumes the authorship correspondence for
  the inner signature check), with F3's last sentence inverting the
  direction — entry 1, "Consumed from elsewhere" and F3 corrected,
  divergence 8 recorded; the S-P1 plan is untouched. Nits: F7's Q5c
  parenthetical (`.out` 1535 has the adversary's `pk(k)` outermost and
  I1 as the middle wrapper); the N1/N2 paragraph's "two object types
  per honest key" (W1/W2 sign wrappers only — divergence 7); the C1
  header sentence in Q2/Q1/Q1/Q5 and READING-AIDS §1d (iii) now name
  the two acceptance paths (header recut 2, above); divergence 1 gained
  the alternative not taken; READING-AIDS §0.2 "215–261" → "216–261".
  **Recut record:** the four `.pv` edits are comment-only and
  line-count neutral; the ladder was re-run (`run_ladder.sh`) and
  every one of the twelve `.out` files is byte-identical to its
  pre-edit copy (`cmp`); `ladder.log` identical modulo run seconds; no
  query, result, trace or `.out` line number changed; no ProVerif
  warning. Still no cross-family falsification review;
  still no author read.
- 2026-09-06 — **cross-family falsification review applied** (Codex
  `gpt-6-astra`, the agreement-gate review of ENUMERATION note 5 item 1;
  `docs/reviews/2026-09-06-codex-suite-falsification-s-p1-s-p2-s-p7-s-standing.md`,
  "Consolidated findings and collaborator dispositions", common items
  1–6 and S-P7 items 18–22; the reviewer's 323 scratch files archived
  under `proverif/falsification-2026-09-06/`). Applied by the AI
  collaborator, PROPOSED, dated; ROUTED item 18 (C9) **not** applied —
  pending line only, above. **Header corrections, all comment-only and
  line-count neutral, each carrying a dated "CORRECTION 2026-09-06
  (cross-family review item N)" line:** Q1d and Q1r lines 28–38 (item
  5: the honest channel's evidence check narrowed from individually
  load-bearing to jointly load-bearing / defence in depth, citing the
  reviewer's mutants and matrix row 2; item 4: `=fp(kI)` and the
  identity routes labelled joint, citing rows 15/14/16/6; the signature
  check and type equalities kept singly load-bearing, rows 9/12); Q2
  lines 20–22 (item 19: "never verified" → "never accepted"), 30–31
  (item 4: the "load-bearing" label defined as joint unless a single
  removal is named red, citing the matrix), 43 (item 4), 79 (items 1,
  2, 21 written into the does-not-prove list — the template header
  every other correct model cites); Q5 lines 35–38 (items 4, 5, 19
  inherited from Q2, the reviewer's Q5 matrix column named); Q4c lines
  15–16 (item 20: "exactly its standalone acceptance" → an existential
  witness); Q6a lines 11–12 (item 20: "on EVERY wrapped acceptance"
  narrowed to wrappers whose identity differs from the inner signer's);
  Q6b line 91 (item 22: the restored `Reattributed` red recorded beside
  the omission). Q3, Q4t, Q4i, Q4p, Q5c untouched. **Re-run record:**
  the full ladder was re-run (`run_ladder.sh`; `ladder.log` refreshed,
  identical modulo run seconds); every one of the twelve `.out` files is
  byte-identical to its pre-edit copy (`cmp`) — every RESULT line
  identical, no query, trace or `.out` line number changed, no ProVerif
  warning. **Confirmation runs (not evidence, not added to the
  ladder):** three of the reviewer's archived scratch models were re-run
  by the collaborator — `q1d_I_evRI_evidence`, `q1r_I_evDI_evidence`
  (every RESULT line identical to the committed Q1 lines; item 5) and
  `audit_sp7_q6b_companion_key_outermost` (`Reattributed` red at line
  1338; item 22) — outputs kept outside the tree. **No query was added
  anywhere**, so this file has no "Post-freeze additions (unregistered)"
  heading; the C9 pending line says what one would contain. **This
  file:** header amendment; the `Reattributed` paragraph (item 22); the
  N1/N2 paragraph (item 6); F6 and F7 corrected (item 20); the
  dependency statement gained the cross-family check (items 4, 5);
  ledger entry 2's assumed fact corrected (item 19); "Consumed from
  elsewhere" gained S-P1's key-use-discipline assumption (item 8); "What
  S-P7 does not discharge" gained the four boundary items (1, 2, 3, 21);
  status paragraph amended; C9 pending line added. `READING-AIDS.md`
  amended in step (its review log); `formal/COVERAGE-MAP.md` gained an
  appended dated amendment note for row 8 (item 21; the row itself is
  committed and untouched). `PREDICTIONS.md` frozen, untouched. Still no
  author read.
- 2026-09-06 — **verification pass on the cross-family application
  above** (AI collaborator, PROPOSED; no text other than this entry
  changed). Checked item by item against the work order (common items
  1–6, the item 8 ledger entry, S-P7 items 19–22; item 18 pending only):
  every applied change is present at the cited lines. **Independent
  re-run:** the seven edited `.pv` files (Q1d, Q1r, Q2, Q4c, Q5, Q6a,
  Q6b) were re-run from the current tree with the shared library
  (`proverif -lib formal/suite/lib/tessera_theory.pvl`), outputs kept
  outside the tree; every RESULT line — text and `.out` line number —
  is identical to the committed `.out` files (Q1d/Q1r 560/574/588/602/
  935/1144; Q2 505/518/531/544/846/1042; Q4c 560/574/588/926/1140; Q5
  654/692/730/768/806/1133/1573/1794; Q6a 503/806/819/1118/1314; Q6b
  489/769/1058/1317/1508), and the reviewer's pre-edit vacuity-table
  citations (review §4, e.g. Q1d `:951→1144`, `:618→935`) resolve to
  the same lines in the post-edit `.out` files, which is the line-count-
  neutrality claim confirmed from the outside. Line counts: Q1 260, Q2
  325, Q4c 235, Q5 295, Q6a 242, Q6b 241; no ProVerif warning. The three
  reviewer mutants were re-run again: `q1d_I_evRI_evidence` and
  `q1r_I_evDI_evidence` give 554/567/580/593 true, 921/1125 false;
  `audit_sp7_q6b_companion_key_outermost` gives `Reattributed` red at
  1338 — as recorded. Q3, Q4t, Q4i, Q4p, Q5c unchanged (no load-bearing
  list, "never verified", "exactly" or "EVERY" wording remains in them).
  `PREDICTIONS.md` untouched. Not applied by this pass, outside the
  family directory: common item 6's "recorded in the suite rules" is
  recorded here (N1/N2 paragraph) and in the reading aid (§1d), not in
  `formal/suite/ENUMERATION.md`. Still no author read.
- 2026-09-06 — **second cross-family pass: one overclaim corrected in
  the item-4 text itself** (AI collaborator, PROPOSED; not adopted; the
  commit is the author's). A skeptic re-read of the pass above found
  that the sentence written *for* item 4 committed the error item 4
  exists to remove. Both copies of it — this file's cross-family check
  of the dependency statement, and the Q2 header's CORRECTION line
  (`sp7_q2_degraded_compromised.pv:30`) — read as matrix-wide claims
  over the reviewer's Q1d/Q1r/Q2/Q4c/Q5 columns and named the frame
  type equality red "on each path". One cell is green:
  `guard_groups.tsv` row 12 reads `q4o_I_type:unchanged`
  (`dependencies.tsv:117`), which the reviewer states outright in
  review §3 — Q4c's inner type equality is inert because only its
  honest attester emits `canon(..., framed(...))`, so that shape
  already discriminates the fixture and `RESULT not
  event(TypeConfused(otS_1,otA_1,fb)) is true` survives its removal
  (`scratch/q4o_I_type.out:560`). **Changed:** (1) the cross-family
  check paragraph above now names the exception and carries a dated
  correction note; (2) the Q2 header's :12 citation gains "red on every
  path in every model except Q4c's inner one, where the canon() shape
  discriminates", under a second dated `CORRECTION 2026-09-06
  (cross-family review item 4, second pass)` line naming the narrowing.
  Rows 9, 11 and 15 as cited were checked against the matrix and are
  accurate; Q2's own two paths are both red, so the Q2 ablation
  statement ("the object-type equality in each verifier is individually
  necessary … on that verifier's path", a10/Q3) stands unchanged; the
  Q4c header makes no load-bearing claim at all. (3) Q5's correction
  line (`sp7_q5_depth2_correct.pv:36`) was rewritten from "as corrected
  2026-09-06 (CORRECTION, cross-family review items 4, 5, 19,
  inherited …)" into the prescribed token order, `CORRECTION 2026-09-06
  (cross-family review items 4, 5, 19): inherited from the Q2 header
  this model cites — …`, body unchanged, so a grep for the prescribed
  string reaches this header like the other six; Q5's matrix sentence
  is scoped to its own I/W/O/M column, where all four type equalities
  *are* singly red, and needed no narrowing. **Re-run record:** both
  edits are comment-only, and both models were re-run with the shared
  library (`proverif -lib formal/suite/lib/tessera_theory.pvl`) and
  their `.out` files refreshed. The RESULT lines are identical, text
  and line number: Q2 505/518/531/544 true, 846/1042 false; Q5
  654/692/730/768/806 true, 1133/1573/1794 false — in fact each
  refreshed `.out` is byte-identical to its pre-edit copy (`cmp`), with
  no ProVerif warning. No query, prediction, RESULT line or property
  status changes; `PREDICTIONS.md` untouched. **Not applied, outside
  this family (re-flagged for the orchestrator):** common item 6's
  "recorded in the suite rules" is still recorded only here and in the
  reading aid, not in `formal/suite/ENUMERATION.md`, which is committed
  text common to all four families and no single family pass can own —
  if written, it belongs there as a dated PROPOSED appended amendment
  note in the COVERAGE-MAP row-8 pattern, never as a rewrite. Still no
  author read.

---

## Post-freeze addendum 1 — results, 2026-09-12

**STATUS: PROPOSED — 2026-09-12 — produced by the AI collaborator; not
adopted; the commit is the author's.** This section is APPENDED: no
sentence above it is edited, and no registered prediction, query,
judge, companion or verdict above is altered. It records the runs of
the two queries registered in `PREDICTIONS.md`, "Post-freeze addendum 1
— 2026-09-12" (Amendment 5 §A5.5; ROUTED C9, ADOPTED (author)): **Q7**,
on `sp7_q2_degraded_compromised.pv` amended in place, and **Q7-C**, the
new companion `sp7_q7_companion_version_unchecked.pv`. Tooling and
library unchanged (ProVerif 2.05, `-lib
formal/suite/lib/tessera_theory.pvl`; the library was not touched).
The pre-change `.out` files and the pre-change `ladder.log` are
archived verbatim under `proverif/pre-addendum-2026-09-12/`.

### What was changed in the model

`sp7_q2_degraded_compromised.pv`, exactly the registered encoding:

1. `versionCh` declared (`.pv` 188–190) — a **new** private channel, not
   a second reader on `scopeCh`, so `ScopeJudge`'s pairing is untouched.
2. `event VersionLied(bitstring, bitstring, bitstring)` (`.pv` 208–210)
   — wrapper bytes, recorded inner version, actual inner version.
3. Query Q7 (`.pv` 230–233), appended **after** the six existing
   queries, which are byte-unchanged and keep their order.
4. The equality, **inside `VerifierWrapped`** (`.pv` 326–330): after
   `if mhW = h(tW) then` (325) and before `event AcceptOuter` (331),
   `let framed(otIv, algIv, idIv, kfpIv, mhIv, =cvIw, plIv) = fbI in`
   — `fbI` re-destructured from the `wrap()` pattern already in scope at
   324, with `=cvIw` in the canonicalization-version position.
   Rejection on mismatch, per §A5.5. **`InnerCheck` (`.pv` 291–304),
   `VerifierBase` (307–309) and the base path are byte-unchanged.**
5. `out(versionCh, (fbW, cvIw, fbI))` (`.pv` 333), in the parallel
   block with `out(typeCh, …)` and the `InnerCheck` call, i.e. **after**
   the new guard (S-P3 recut-1 idiom).
6. `VersionJudge` (`.pv` 360–367) and `| !VersionJudge` (386).

`sp7_q7_companion_version_unchecked.pv` is that model with item 4
absent (its four comment lines replaced by a `MUTATION` marker at
`.pv` 222–227) and its own companion header (1–57); everything else,
`versionCh` and `VersionJudge` included, is line-for-line the amended
Q2 model.

### Header change (registered)

The Q2 claim block (`.pv` 1–126) is **unedited**, CORRECTION lines and
all. The two registered sentences were added as a separately marked
block at `.pv` 128–161, opening `ADDENDUM 2026-09-12 (Amendment 5
§A5.5…)` and placed immediately after it: under *This model ALSO
proves*, that on the wrapped path the wrapper's recorded inner
canonicalization version equals the inner frame's own; under *does NOT
prove*, that either version is supported or that the inner bytes were
produced under it (P8/H1a). The block also records that the existing
"carried, not load-bearing … checked only for presence" line (`.pv`
60–62) stands as written for `cvI`, `cvW` and the base path and is
narrowed by the addendum for `cvIw` on the wrapped path only.

### Predictions vs observed

| Query | Registered prediction (`PREDICTIONS.md` addendum) | Observed | Outcome / branch fired |
|---|---|---|---|
| **Q7** — `VersionLied` unreachable in the amended Q2 model; Q2's three results and witnesses unchanged | unreachable, terminating, Q2 lines unchanged (**0.80**); unexpectedly reachable = defect in the new equality (0.07); Q2 changed by the addition = divergence (0.08); timeout (0.05). Box 15 min | `VersionLied` **unreachable** (`.out` 1074); `TypeConfused` 527, `Rescoped` 540, `InnerSigTransplanted` 553, `Reattributed` 566 all unreachable; `HonestWrappedAccepted` reachable (579, 865), `HonestAccepted` reachable (878, 1061). 1 s against a 900 s box | **termination, as predicted — the 0.80 branch.** Every pre-existing RESULT line text-identical (see "Comparison") |
| **Q7-C** — the equality removed | reachable **with the registered honest-wrapper shape**, no cryptographic step (**0.85**); recut (0.08); companion green (0.04); timeout (0.03). Box 15 min. Red on exactly `VersionLied` | `VersionLied` **reachable** (1075, 1301); `TypeConfused` 525, `Rescoped` 538, `InnerSigTransplanted` 551, `Reattributed` 564 unreachable; `HonestWrappedAccepted` (577, 866) and `HonestAccepted` (879, 1062) reachable. 1 s against a 900 s box | **red on exactly `VersionLied`, as required, and no cryptographic step — but the exhibited trace is the UNREGISTERED second shape, not the registered one.** Reachability and the red/green pattern are as the 0.85 branch predicts; the *shape* clause of that branch did not land. Recorded, not absorbed (below) |

No `exit 124`; no TIMEOUT outcome anywhere in the ladder; no ProVerif
warning in either `.out`.

### Verbatim RESULT lines

`proverif/sp7_q2_degraded_compromised.out` (Q7 is the last):

```
527:RESULT not event(TypeConfused(otS_1,otA_1,fb)) is true.
540:RESULT not event(Rescoped(kX_1,idX_1,kH_3,idH_1,fb)) is true.
553:RESULT not event(InnerSigTransplanted(kX_1,s)) is true.
566:RESULT not event(Reattributed(kX_1,kH_3,fb)) is true.
865:RESULT not event(HonestWrappedAccepted(kH_3,fb,kW_3)) is false.
1061:RESULT not event(HonestAccepted(k,fb)) is false.
1074:RESULT not event(VersionLied(fbWq,cvRec,cvAct)) is true.
```

`proverif/sp7_q7_companion_version_unchecked.out`:

```
525:RESULT not event(TypeConfused(otS_1,otA_1,fb)) is true.
538:RESULT not event(Rescoped(kX_1,idX_1,kH_3,idH_1,fb)) is true.
551:RESULT not event(InnerSigTransplanted(kX_1,s)) is true.
564:RESULT not event(Reattributed(kX_1,kH_3,fb)) is true.
866:RESULT not event(HonestWrappedAccepted(kH_3,fb,kW_3)) is false.
1062:RESULT not event(HonestAccepted(k,fb)) is false.
1301:RESULT not event(VersionLied(fbWq,cvRec,cvAct)) is false.
```

### The companion trace, checked against the registered shape

**It is the unregistered second shape, not the registered one.** The
registered shape is an *honest* `Wrapper` process (`skW1`, `skW2` or
`skI1`-as-wrapper) handed an honest inner `(fbI, sgI)` off the public
channel together with an adversary-chosen `cvIw ≠ cvI`, framing and
signing honestly, and `VerifierWrapped` accepting. What ProVerif
exhibited (`.out` 1075–1300) is the second shape the registration
named and set aside: the adversary mints the **whole** wrapper. Reading
the derivation: `attacker(k)` is a hypothesis (step 21), the wrapper
frame is `framed(OT_WRAPPER, algW_1, idW_6, fp(pk(k)), h(authTuple(idW_6,
fp(pk(k)), …)), cvW_4, wrap(cvRec, (framed(otJv_1, …, cvAct, plJv_1),
sgI_4)))` built by the attacker (step 28) and signed under its own `k`
(step 31); the possession proof is its own self-signature (34); the
channel evidence is minted with the public `skS[]` (35–38, the
degraded-mode `out(c, skS)` at `.pv` 379, shown in the trace as `{19}`);
the package is delivered to `VerifierWrapped`'s input `{135}`,
`AcceptOuter` fires at `{143}`, `versionCh` is written at `{145}` and
read by `VersionJudge` at `{183}`, and `VersionLied` fires at `{186}`
under `cvRec ≠ cvAct`. **No honest process appears in the trace at
all** — not only is the wrapper the adversary's, the inner frame and
its signature `sgI_4` are attacker terms too, because `VersionJudge` is
instrumentation on the acceptance report and pairs with nothing honest.
The derivation uses no `dsks` step and no signature forgery, so the
"no cryptographic step" half of the 0.85 branch holds.

This is the **Q6a precedent** ("the exhibited trace is the
adversary-wrapper one, not the honest-only one the registration
admitted"), one step further: here the honest *inner* is absent too.
What the companion establishes is exactly what the addendum asked of
it — that `VersionJudge` fires at all, so Q7's green is the new
equality doing work and not a vacuous query. What it does **not**
establish, and what the registered shape would have established, is
that the lie is accepted **with no compromised wrapper at all**. That
stronger statement is **not refuted** by this trace — ProVerif reports
one witness, the cheapest, and says nothing about the others — it is
simply **not exhibited**, and no model has been built to exhibit it
(building one would be an unregistered addition). Recorded as an open
cell of this addendum, not repaired.

### Comparison against the archived pre-change outputs

Every pre-existing model was re-run through the whole ladder after the
body change and compared against `proverif/pre-addendum-2026-09-12/`:

- **Eleven of the twelve pre-existing `.out` files are byte-identical**
  to their archived copies (`cmp`): both Q1 runs, Q3, both Q4
  companions, the two unregistered Q4 runs, Q6a, Q6b, Q5 and Q5c.
- `sp7_q2_degraded_compromised.out` differs, as it must: its **six
  pre-existing RESULT lines are text-identical** to the archived ones
  (`diff` of the `RESULT` lines reports a single addition, `6a7 >
  RESULT not event(VersionLied(fbWq,cvRec,cvAct)) is true.`); line
  numbers shifted (table below).

**No divergence.** Every frozen Q1–Q6 outcome is re-established; the
addendum's own requirement — "the Q1–Q6 ladder outcomes in `RESULTS.md`
must be identical after the change" — is met.

### Line-shift table

`PREDICTIONS.md`, this file above, `READING-AIDS.md`, the ablation
record and the archived Codex review cite **body** line numbers of the
Q2 model and `.out` line numbers of its output. Those citations are
**left as written** (amend-don't-rewrite; no old citation is fixed).
This table is how a reader re-finds them.

`sp7_q2_degraded_compromised.pv`, old (freeze) → new:

| Region | Old lines | New lines | Shift |
|---|---|---|---|
| Header claim block (unedited) | 1–126 | 1–126 | 0 |
| *(new)* ADDENDUM header block | — | 128–161 | — |
| Model-local declarations, free names | 128–142 | 163–177 | **+35** |
| Judge channel declarations | 144–152 | 179–187 | **+35** |
| *(new)* `versionCh` | — | 188–190 | — |
| Event declarations | 154–169 | 192–207 | **+38** |
| *(new)* `event VersionLied` | — | 208–210 | — |
| Queries (six, unchanged, same order) | 171–188 | 212–229 | **+41** |
| *(new)* query Q7 | — | 230–233 | — |
| `AuthorityS` … `OtherSigner` | 190–238 | 235–283 | **+45** |
| `InnerCheck` (**byte-unchanged**) | 240–259 | 285–304 | **+45** |
| `VerifierBase` (**byte-unchanged**) | 261–264 | 306–309 | **+45** |
| `VerifierWrapped`, down to `if mhW = h(tW)` | 266–280 | 311–325 | **+45** |
| *(new)* the A5.5 equality + its comment | — | 326–330 | — |
| `event AcceptOuter`; `out(typeCh, …)` | 281–282 | 331–332 | **+50** |
| *(new)* `out(versionCh, …)` | — | 333 | — |
| `InnerCheck` call in the wrapped path | 283 | 334 | **+51** |
| `TypeJudge`, `Judge`, `ScopeJudge`, `SigJudge` | 285–307 | 336–358 | **+51** |
| *(new)* `VersionJudge` | — | 360–367 | — |
| `process` block | 309–325 | 369–386 | **+60** (last line +61: `!VersionJudge` added) |

Frequently cited single lines: `InnerCheck`'s inner-frame read 253 →
**298**; its manifest-hash check 254 → **299**; the slot check 250 →
**295**; the inner signature check 252 → **297**; `VerifierWrapped`'s
unwrap 279 → **324**; `AcceptOuter` 281 → **331**; the `Wrapper`
process's adversary-chosen input 218 → **263**; `out(c, skS)` 319 →
**379**. The suggested author read of "lines 13–83 and 246–283" (the
"Status toward discharge" section above) is now **13–83 and 291–334**.

`sp7_q2_degraded_compromised.out`, old → new:

| Cited item | Old `.out` | New `.out` |
|---|---|---|
| `TypeConfused` RESULT | 505 | **527** |
| `Rescoped` RESULT | 518 | **540** |
| `InnerSigTransplanted` RESULT | 531 | **553** |
| `Reattributed` RESULT | 544 | **566** |
| `HonestWrappedAccepted` `goal reachable` | 557 | **579** |
| `HonestWrappedAccepted` RESULT | 846 | **865** |
| `HonestAccepted` `goal reachable` | 859 | **878** |
| `HonestAccepted` RESULT | 1042 | **1061** |
| `VersionLied` RESULT | — | **1074** |

### Runner and run record

`run_ladder.sh` gained two lines, placed **before** the Q5/Q5c pair so
the ordering rule at the head of that file ("Q5 and Q5c last") still
holds. Q7 is a *query* on the Q2 model file, not a new model: the Q7
line re-runs `sp7_q2_degraded_compromised.pv` under the **registered Q7
box of 900 s**, which is tighter than Q2's own 1800 s box, so the box
that governs the surviving `.out` is the registered one. ProVerif is
deterministic on this model — a third independent run of the same file
was compared with `cmp` against the ladder's output and is
byte-identical — so the `.out` the Q2 line writes and the `.out` the Q7
line writes are the same bytes, and `ladder.log`'s two entries for that
file both describe the file on disk. The whole ladder was re-run, not
just the changed models; `ladder.log` (14 runs, all `rc=0`, 22 s wall
total):

```
sp7_q2_degraded_compromised rc=0 seconds=1 box=900 (Q7, A5.5 addendum: VersionLied unreachable; re-run of the Q2 model under the registered Q7 box)
sp7_q7_companion_version_unchecked rc=0 seconds=1 box=900 (Q7-C companion; required red: VersionLied only)
```

### What this addendum does not discharge

Unchanged from the registered boundary: the equality compares two
fields. It does not establish that either canonicalization version is
supported, or that the inner bytes were produced under it (P8/H1a) —
the same obligation the header already carried about the version
fields. The Q4 re-serialization companions ask a different question
(whether the outer pass touches the inner bytes) and are untouched, as
the eleven byte-identical `.out` files show. Nothing here bears on the
depth axis (Q5/Q5c), on standing evidence, or on the P4 partition.

### Status toward discharge (no change)

**This section changes nothing about P7's tracker row, and nothing in
the "Status toward discharge" section above.** That section's state
stands as written: tool passes yes; the cross-family falsification
review run; **author read pending**. P7's row moves on the author's
**C5 read** (`formal/suite/READ-C5-2026-09-12.md`;
`ROUTED-2026-09-06.md` C5, narrowed 2026-09-11), and on nothing
recorded here — Amendment 5 §A5.8 says so in terms: each of the three
new verifier obligations "is a new query with its own registered
prediction and companion, recorded as a post-freeze addendum, and each
family's tracker row moves only on its other recorded prerequisites
(ROUTED C5, as corrected 2026-09-11)". The ROUTED C9 item recorded in
"Pending author ruling" above is now **ruled** (adopted, Amendment 5
§A5.5) and implemented; that paragraph is left as written per
amend-don't-rewrite, and this section is its disposition. No
recommendation in this file is strengthened, weakened or re-stated by
these two runs. Two things a reader should carry to the C5 read: the
suggested read's line range has moved (see the line-shift table), and
the Q2 claim block now has an ADDENDUM block after it that is part of
what "does this header say what that verifier does, no more?" now asks.

### Review log (this section)

- **2026-09-12** — written by the AI collaborator after the runs above.
  No falsification review has been run on the amended Q2 model or on
  the Q7-C companion; the cross-family review of 2026-09-06 predates
  both. No author read of either. The trace-shape gap recorded under
  "The companion trace" is the one item a reviewer should attack first.

## Author read — 2026-09-12 (ROUTED C5; entered by the AI collaborator in the author's words)

The author read the S-P7 block of `formal/suite/READ-C5-2026-09-12.md`
(this family's block 3, quoting model lines 13–75) and returned **one
NO**: the read's line 254, which is model line 55 — *"Line 254 says
'the wrapper's authorship is S-P3 entry 1, consumed' but S-P3 entry 1
establishes key binding. It does not establish authorship. S-P1
authorship is required to establish authorship."* Verified:
`formal/suite/s-p3/RESULTS.md` ledger entry 1 is the **key-binding**
relation (acceptance binds the bytes' committed `(issuerId, kfp)` to
the accepting key; honest bytes are never accepted under another key);
**authorship** — that bytes accepted under an honest key were signed at
an issuance event by that key's holder — is S-P1's headline, assigned
there by S-P3 F7. The header misattributed. Repair: model line 55
rewritten **in place, same line count**, to "the wrapper's KEY BINDING
is S-P3 entry 1, consumed; its AUTHORSHIP is S-P1's, per S-P3 F7", with
a dated `CORRECTION` marker quoting the pre-repair wording, so every
`.pv` line citation in this file and in `READING-AIDS.md` still
resolves. Comment-only: re-run the same day with
`proverif -lib formal/suite/lib/tessera_theory.pvl`, the `.out`
byte-identical to the pre-edit file (`proverif/ladder.log`, the
`recut=header-only-2026-09-12-author-C5-read out=identical` line). No
result, query, prediction or ledger entry changed. The same row is
repeated at `READING-AIDS.md:207` and is corrected in that file's
appended section. Author read of the Q2 header: **one sentence
repaired; the read otherwise stands as returned.**

## Cross-family review 2026-09-12 — dispositions applied

Source: `docs/reviews/2026-09-12-codex-falsification-amendment-5-checks.md`
(OpenAI Codex CLI, `gpt-6-astra`, non-author; scratch under
`proverif/falsification-2026-09-12/scratch/`). **Amend-don't-rewrite**:
the sentences corrected below are left as written above; this section
is the correction of record. The `.pv` edits named here are
comment-only, same line count, re-run the same day with the `.out`
byte-identical (`proverif/ladder.log`, last line).

**1 — "recorded equals declared, not produced" is already a stated
boundary** (review §2). Confirmed at `sp7_q2_degraded_compromised.pv:139–141`:
"This model does NOT prove: that either canonicalization version is
supported, or that the inner bytes were produced under it (P8/H1a).
The check compares two fields for equality and nothing more." The
reviewer's own diagnostic agrees that the limit is structural — the
model contains no canonicalization algorithm, so the version tag is a
surrogate (`S/production_version_v3.out:1368,1133`). **No change
needed.**

**2 — the version report establishes OUTER acceptance** (review §2,
§6). Verified: `versionCh` is emitted in the parallel composition that
follows `event AcceptOuter` (`.pv:330–334`), *alongside* the
`InnerCheck` call rather than after it, so the report witnesses that
the outer object was accepted and the recorded/declared versions
agreed — **not** that `InnerCheck` completed. The base path and the
wrapped path invoke the identical `InnerCheck` (`:291–309`), so the new
destructuring adds no completed inner acceptance the base path lacks.
The header now says this (`.pv:154–155`, marked `cross-family review
item 3`). ACCEPTED-verified.

**3 — "stands as written for cvI, cvW and the base path" is wrong for
wrapped-path `cvI`** (review §6). Verified: the new guard
`let framed(otIv, algIv, idIv, kfpIv, mhIv, =cvIw, plIv) = fbI`
(`.pv:330`) compares the inner frame's own canonicalization-version
field with `cvIw`, so on the wrapped path `cvI` is no longer "checked
only for presence". Repaired in place at `.pv:144–145` (same line
count, marked `cross-family review item 7`). The correct text: **the
"carried, not load-bearing" line stands as written for `cvW` and for
the base path; on the wrapped path it does not stand as written for
`cvI`, which the addendum now compares with `cvIw` through the same
frame field.** Lines 964–967 above repeat the wrong wording and are
corrected to this. ACCEPTED-verified.

**4 — the open trace-shape cell is CLOSED by the reviewer's exhibit**
(review §3). The sentence at lines 1034–1043 above —

> What the companion establishes is exactly what the addendum asked of
> it

— and its conclusion that the registered honest-wrapper shape is "not
refuted … simply **not exhibited**, and no model has been built to
exhibit it … Recorded as an open cell of this addendum, not repaired"
are **superseded**. The reviewer built that model. In
`falsification-2026-09-12/scratch/literal_honest_wrapper.pv:137–138`,
which literally names W1, I1, the honest signature, `reviewPayload`,
recorded `cvB` and inner `cvA`, both literal events are **reachable**:
`literal_honest_wrapper.out:1537` (`VersionLied(framed(OT_WRAPPER, …, cvB[], wrap(cvB[], (framed(OT_ATTEST, …, cvA[], reviewPayload[]), sign(…, skI1[])))), cvB[], cvA[])` `is false`)
and `:1815` (the matching
`AcceptInner(wctx(pk(skW1[]), idW1[], …), pk(skI1[]), issuerId[], framed(OT_ATTEST, …, cvA[], reviewPayload[]))`
`is false`) — so the lie is accepted **with an honest inner producer
and the completed inner acceptance**, which is the registered shape.
The control with the version guard restored makes both literal events
unreachable (`literal_correct_control.out:1063,1078`), so the exhibit
is the removed equality doing the work. Correct text for lines
1034–1043: **the companion establishes that `VersionJudge` fires at
all; the stronger registered shape — the lie accepted with no
compromised wrapper — was neither refuted nor exhibited by the
committed companion, and is now EXHIBITED by the non-author
reviewer's `literal_honest_wrapper` model. The open cell is closed;
the closure is the reviewer's, not this file's.** ACCEPTED-verified.

**Not accepted / no change.** The review found no further overclaim in
the claim block or the addendum block, and §§4–5 confirm the new
equality is individually load-bearing with every pre-existing polarity
unchanged (`S/matrix.txt:4`) and both committed witnesses still
reachable (`sp7_q2_degraded_compromised.out:865,1061`).

**Method.** Every `.out` line the review cites was opened before the
finding was accepted. No `PREDICTIONS.md`, library, amendment,
coverage-map or scratch file was edited; no result, query text or
prediction changed; nothing was committed.
