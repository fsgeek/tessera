# S-P2 — signature-set completeness (anti-stripping): results

**STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not
adopted; the commit is the author's.** Predictions were frozen at
`5188e7a` (`PREDICTIONS.md`) before any model existed. This file records
predictions against observed outcomes in the registered three-outcome
vocabulary, the encoding notes, the findings, and the A3.3 ledger
entries S-P2 offers the suite. It does not change `formal/PROPERTIES.md`;
P2's tracker row is the author's to move. Nothing below is ratified;
the author's cold read of the correct model precedes any ratification
(`ENUMERATION.md` §5).

Tooling: ProVerif 2.05, `-lib formal/suite/lib/tessera_theory.pvl`
(library as of the D-5/D-6 entry of 2026-09-06). Models and outputs:
`formal/suite/s-p2/proverif/`; runner `run_ladder.sh`; timings and
boxes in `ladder.log`. Every run terminated in ≤ 1 s against boxes of
15–30 min. No run needed an encoding recut: the S-P3 encoding idioms
(parallel judge reports, judge-emitted honest witness, no library-name
shadowing) were applied from the first build, and no `.out` contains
"cannot be proved". One comment-only recut: the Q1 headers (both
variants) were corrected 2026-09-06 after the skeptic review (see
"Review log"); both models were re-run under the 900 s box and both
`.out` files are byte-identical to the pre-edit run (`ladder.log`, the
two `recut=header-only` lines). Unregistered ablation diagnostics:
`proverif/diagnostics/` (`diagnostics.log`, d1–d11; d7–d11 are the
strict-mode ablations added 2026-09-06) — evidence about the checking
arrangement, never about a registered query.

**Library dependency (uncommitted at the time of writing).** Every
S-P2 model uses `OT_ATTEST` (library divergence D-5), which exists
only in the working-tree `formal/suite/lib/tessera_theory.pvl` — the
D-5/D-6 entry of 2026-09-06 is not in `HEAD` (`git diff` shows it as
an addition). The library change must land in the same commit as, or
an earlier commit than, the S-P2 models, or the models do not build
and the `.out` files are not reproducible from the commit. Once
committed, the library's commit hash belongs beside `5188e7a` here.

## Ladder outcomes

| Query | Model | Registered prediction (p) | Observed | Outcome / branch fired |
|---|---|---|---|---|
| Q1 strict, DNS compromised | `sp2_q1_strict_dns_compromised` | all hold, both variants (0.65); violation (0.10); termination-after-recut (0.15); timeout (0.10) | `Stripped`, `SignerForged`, `SetAltered`, `Reattributed` unreachable (`.out` 386, 392, 398, 404); `HonestComplete(M1, …)` reachable (580); `HonestComplete(M2, …)` reachable (812); carried `HonestAccepted` reachable (1055) | **termination, as predicted** (0.65 branch) |
| Q1 strict, repo compromised | `sp2_q1_strict_repo_compromised` | same | identical lines (386, 392, 398, 404, 580, 812, 1055) | **termination, as predicted** |
| Q2 degraded, sole channel compromised — **the P2 claim** | `sp2_q2_degraded_compromised` | all unreachable, witnesses reachable (0.65); real violation, most plausibly `SetAltered` (0.15); timeout (0.20) | unreachable ×4 (354, 360, 366, 372); witnesses reachable (536, 756); `HonestAccepted` reachable (987) | **termination, as predicted** (0.65 branch) |
| Q3 companion: cardinality ignored | `sp2_q3_companion_cardinality_ignored` | `Stripped` reachable, no cryptographic step (0.75); recut (0.10); companion green (0.10); timeout (0.05) | `Stripped(M2, verified1(pk(skA2)))` **reachable**, trace found (`.out` 354–520); other three unreachable (526, 532, 538); witnesses reachable (702, 922, 1153) | **violation as required** (0.75 branch); red on exactly `Stripped` |
| Q4 companion: slot B unbound | `sp2_q4_companion_slot_unbound` | `SignerForged` reachable, adversary's own key over its own frame, no `dsks` (0.75); recut (0.15); timeout (0.10) | `SignerForged(M2, pk(k))`, `k` adversary-held, **reachable** (360–601); `Stripped`, `SetAltered`, `Reattributed` unreachable (353, 608, 615); witnesses reachable (780, 1001, 1233) | **violation as required** (0.75 branch); red on exactly `SignerForged`; trace matches the predicted shape |
| Q5-C1 note 2's companion as literally specified | `sp2_q5_c1_fponly_frame_mh` | `SetAltered` **unreachable**, companion cannot fail (0.65); reachable (0.25); timeout (0.10) | all four unreachable (354, 360, 366, 372); witnesses reachable (536, 756, 987) | **termination, as predicted** (0.65 branch) — recorded as the redundancy finding (F4), per `ENUMERATION.md` note 6 item 2, not as a miss |
| Q5-C2 the red companion | `sp2_q5_c2_fponly_frame_nomh` | `SetAltered` reachable (0.70); recut (0.10); companion green (0.10); timeout (0.10) | `SetAltered(pk(skB2), M2, authTuple(issuerId2, fp(pk(skB2)), signers0, algH, ver_2))` **reachable** (363–535); `Stripped`, `SignerForged`, `Reattributed` unreachable (349, 356, 542); witnesses reachable (706, 925, 1100) | **violation as required** (0.70 branch); red on exactly `SetAltered`; the exhibited instance differs from the plan's named instance (F3) |
| Q5-C3 green isolation | `sp2_q5_c3_manifestposs_frame_nomh` | `SetAltered` unreachable (0.70); `dsks` route (0.15); timeout (0.15) | all four unreachable (349, 356, 363, 370); witnesses reachable (534, 753, 983) | **termination, as predicted** (0.70 branch) |

Every model carries both registered N1 witnesses, reachable, and the
registered fixture (M1 one signer, M2 two signers, three honest keys,
adversary-chosen payloads, sole/compromised channel key public). Every
companion is red on exactly its named query and green on the rest (the
`.out` lines above).

## Prediction divergences

One additive divergence: an unregistered vacuity query
(`HonestAccepted`) in every model (item 2 below); the plan's query list
for Q1/Q2 is closed ("Queries as Q1": four unreachable plus two
witnesses), so adding a query changes the registered set even though
the addition is recorded — S-P3 treated its own N1/N2 additions the same
way. No registered query, companion, fixture, timebox or prediction
changed, and no encoding recut was needed. Three things were done that
the frozen text does not spell out, recorded here so they are not
mistaken for refinements:

1. **The three honest signer keys are private free names**
   (`free skA1: skey [private]`, Q2 lines 89–91) rather than top-level
   `new` as in S-P3. Reason: the registered N1 queries name the fixture
   terms `M1` and `M2` literally (`PREDICTIONS.md` lines 228–230), and a
   query cannot mention a `new`-bound name. A private free name and a
   top-level `new` before replication are the same object to the
   analysis (one fresh secret, unknown to the adversary); the fixture
   is unchanged. Offered as a suite idiom: *fixture keys a registered
   query must cite are private free names.*
2. **One unregistered query per model**: `HonestAccepted` reachable
   (Q2 lines 130–132), the N1 witness of the S-P3 judge that S-P2
   carries verbatim as its consumer-side check. Added so the carried
   judge is shown live rather than assumed; reachable in all eight.
3. **Q3's mutation shape.** The plan says the verifier "binds the
   tuple's `sset` field as a variable and never inspects it … and
   accepts a single-signature package for any tuple". Built as: the
   n = 1 branch's `=signers0` pattern replaced by a bound variable `ss`
   (Q3 line 128); the n = 2 branch left as in Q2, so the two-signer
   witness stays reachable and the companion is red on `Stripped`
   alone. The closest faithful reading; recorded because "for any
   tuple" could also be read as removing the n = 2 branch.

## Findings

**F1 — The P2 [model] claim holds in the hard case, and in strict
mode.** In degraded mode with the sole authority channel compromised,
under an adversary that holds every key it uses and the DSKS
capability: no honest manifest is accepted with fewer signers than its
signed set names; no slot the signed set assigns to an honest signer is
satisfied by another key; no honest key is accepted as a signer of a
manifest it never signed; and S-P3's key-binding relation is not
weakened (Q2). Strict mode (Q1, both leaked-channel variants) gives the
same four results, carried there by the honest channel's tuple pin
before the set is inspected (S-P3 F1's pattern; not re-ablated in
S-P2). *[Correction 2026-09-06, after the skeptic review — the preceding
sentence's mechanism claim is wrong for two of the four results and was
not backed by a run. Strict-mode ablations d7–d11 (`diagnostics/`, Q1d
as base, DNS key leaked): the honest channel's tuple pin closes
`SetAltered` alone (d9: both set-pins removed, still green) but NOT
`Stripped` or `SignerForged` (d7: the Q3 mutation, `Stripped(M2,
verified1(pk(skA2)))` reachable, `.out` 564; d8: the Q4 mutation,
`SignerForged(M2, pk(k))` with `k` adversary-held reachable, 645; no
`dsks` step in either): those two packages present the honestly
published tuple M2, which the honest channel endorses, so in both
modes they rest on the verifier's sset pattern and slot match, as
`PREDICTIONS.md` 180–181 anticipated ("stripping proper … does not
touch the manifest, so channel mode is not expected to matter to it").
`Reattributed` is closed in strict mode by the slot match against the
pinned tuple's `kfpr` (d10: frame's `=fp(kX)` unbound in every slot,
still green) and not by the pin alone (d11: slot matches removed too,
`Reattributed` reachable, 922 — honest framed bytes re-signed under the
adversary's own key, no `dsks` needed, S-P3 F5's point). The Q1
headers were corrected to this (comment-only recut, "Tooling"). The
repo-leaked variant was not re-ablated: it differs from Q1d only in
which channel key is public (`READING-AIDS.md` §3).]* The honest flow
is accepted for both set sizes — the P2 sentence's
"issued with one" (M1) and "issued with two" (M2) are both live
(`HonestComplete` reachable ×2 in every model). Required sets are at
most two signers, read from the map-v1 tuple's `kfp` and `sset`.

**F2 — Stripping is closed by verifier logic alone; S-P3's verifier
shape is P2-broken.** Q3's trace (`.out` 354–520) has no cryptographic
step: the package is A2's honest possession proof, honest signature and
honest frame for M2, with the sole channel's evidence for M2 (which the
honest channel itself emits; the derivation builds it with the leaked
key, term-equal). It is accepted through the n = 1 branch because that
branch no longer demands `sset = signers0` (Q3 line 128 versus Q2 line
163). No `dsks` step, no leaked-key step that an honest run would not
also produce. The mutated line is exactly S-P3 Q2's verifier line 102
(`let authTuple(id, kfpr, ss, alg, ver) = t in`, `ss` discarded), so
this companion is the record that S-P3's verifiers, correct for P3, do
not check P2 — "each model proves only its property" made visible.

**F3 — The set-shrinking surface is wider than the plan's single
trace.** The plan named `SetAltered(pk(skA2), M2, M2')` with `M2' =
authTuple(issuerId2, fp(pk(skA2)), signers0, algH, verH)` — A2 kept as
sole signer. C2's exhibited witness is instead `SetAltered(pk(skB2), M2,
authTuple(issuerId2, fp(pk(skB2)), signers0, algH, ver_2))`: **B2
promoted to sole signer, A2 removed, and the version field replaced by
an adversary-chosen value** (`.out` 363; trace 477–534). Diagnostic d5
(C2 plus the plan's literal instance as an extra query) reports that
instance reachable too (`diagnostics/d5_c2_registered_witness.out`
714). So, under note 2's broken encoding, every member the set names
is a candidate sole signer, and every tuple field the frame does not
carry is alterable around the honest key. Which fields those are:
`framedNoMh` retains `=alg` and `=id` (C2 lines 135, 155–156), so
algorithm and identity are still pinned by the frame even in C2; the
signer set and the version are not — the version is not a frame field
at all. The guide's phrase "signer set, algorithm, or version"
(`READ-AND-CHALLENGE.md` 513–514) is therefore, in this frame,
"signer set or version"; algorithm is held by S-P3's field list. The
relying-party story should say which fields the frame pins and which
only possession-over-manifest pins.

**F4 — C1 is the redundancy finding, and the dependency statement is
confirmed.** As registered (predicted green, p ≈ 0.65), note 2's
companion as literally specified cannot fail: with fingerprint-only
possession but the frame's `mh = h(t)` retained (C1 lines 128, 131),
A2's honest frame carries `h(M2)` and the shrunk tuple hashes to
something else (`h` injective, library 119–131). Removing the hash too
(C2) goes red; keeping the hash out but restoring possession over the
manifest (C3) stays green. The three runs together give the statement
`PREDICTIONS.md` registered (lines 438–447): *frame-carried manifest
hash and possession-over-manifest are each individually sufficient
against set-shrinking and jointly redundant; the former rests on `h`
injectivity, the latter on signature unforgeability (the adversary
would need A2's or B2's signature over `(POSS, M2'')`, which D-4 does
not grant — no `dsks` step appears in any S-P2 derivation); neither
is exercised by stripping proper (Q3), which rests on verifier logic
alone.* `ENUMERATION.md` note 6 item 2's disposition (C2 satisfies
note 2; C1 recorded as redundancy) is what the runs show.

**F5 — Q4's red is the adversary's own key over its own frame, and the
slot fingerprint match is symmetric.** The Q4 trace (`.out` 360–601):
`kUsed = pk(k)` with `k` adversary-held, possession `sign((POSS, M2),
k)`, frame `framed(otb_1, algH, issuerId2, fp(pk(k)), h(M2), cvb_1,
plb_1)` signed by `k` — object type and canonicalization version are
adversary-chosen in the trace (`otb_1`, `cvb_1`), a visible instance of
S-P3 F7's unexercised fields. No `dsks` step: the derived-key route over
B2's honest frame is closed by the retained `=fp(kB)` (Q4 line 154), as
the plan traced. Diagnostic d6 (Q2 with the slot-A match removed in
both branches) makes `SignerForged` reachable and leaves `Reattributed`
unreachable (`d6…out` 599, 615): the slot match carries membership; the
frame's own `=fp(kX)` carries re-attribution on its own — S-P3's
dependency statement seen from P2's side.

**F6 — The carried checks are carried: ablation, not assumption.**
Q2's header names four checks as carried for other properties. Each
was removed in a diagnostic and every RESULT line stayed identical to
Q2's: the authority-evidence check (d2 — inert by construction, the
sole channel key is public; S-P3 F6), the frame's `=id` and `=alg`
conjuncts (d3), and the attestation-signature check itself on both
slots (d4). The last is the one to hold onto: with no signature check
at all, no S-P2 judge fires and both witnesses remain reachable,
because the judges compare the *keys the verifier used* against the
*set the manifest names* and never ask who authored the bytes. A
fabricated signature accepted under the honest named key is an
authorship failure and is S-P1's obligation (S-P3 F7; `PREDICTIONS.md`
367–379). Q2's header says so; d4 is the evidence.

**F7 — Fixture robustness at the set-size granularity.** Note 3's
two-values rule is met on the manifest, issuer-identity and set-size
axes (M1/M2, `issuerId`/`issuerId2`, `signers0`/`signers1`), but each
*set size* has exactly one honest manifest. Diagnostic d1 adds a third
honest manifest `M3` (second two-signer manifest, own identity, own two
keys) and changes nothing (`d1…out` 455–1112). Recorded so that no
S-P2 result is later read as carried by M2 being the only two-signer
manifest. Not run: two two-signer manifests sharing a signer key — the
registered fixture binds each key to exactly one manifest
(`PREDICTIONS.md` 211–214), and a shared key is a different design
question (succession, docket item 25), not P2.

**F8 — What was not separately exercised.** (a) *Duplicate* (one honest
signature in both slots of M2): the plan assigns it to the same
slot-fingerprint check as Q4 (M2's two named fingerprints are distinct),
and no separate run was made; the claim is by inspection of Q2 lines
182–183, not by a result. (b) *Reorder*: unrepresentable, P8 (consumed
ledger entry 3). (c) The S-P3 F5-class mutation (total
exclusive-ownership failure, "any key verifies any signature") requires
editing the library's `checksign` rules, which a model may not
redeclare; not run. The plan's prediction that the S-P2 judges would
stay unreachable under it rests on the judges' `kUsed ≠ kH` /
`t ≠ m` conditions and on d4, not on a run.

**Dependency statement (from Q3, Q4, C1–C3, d2–d4, d6):** the sset
pattern alone carries `Stripped`; the per-slot fingerprint match alone
carries `SignerForged`, in either slot; the frame's manifest hash and
possession-over-manifest each alone carry `SetAltered` and neither is
needed while the other stands; the frame's fingerprint field alone
carries `Reattributed`; the evidence check, the frame's identity and
algorithm conjuncts, and the attestation-signature check carry nothing
any S-P2 judge can see. *Strict mode (added 2026-09-06, from d7–d11):*
the honest channel's tuple pin alone carries `SetAltered`; it carries
`Reattributed` only jointly with the slot match; it carries neither
`Stripped` nor `SignerForged`, whose load-bearing checks are the same
as in degraded mode.

## Ledger entries (A3.3 conservation fields) — offered, not entered

**Consumed** (as registered, `PREDICTIONS.md` 495–533; status after the
runs):

1. **Key-binding relation** — producer S-P3 Q2 (`Reattributed`
   unreachable), `s-p3/RESULTS.md` ledger entry 1. Consumed here as
   the carried judge (Q2 lines 229–233), unreachable in all eight
   models and live (`HonestAccepted` reachable). Shared terms:
   `framed` (copied verbatim, Q2 line 76), `authTuple`, `fp`.
   Adversary at the join: A1.3 with DSKS, sole channel compromised.
   Residual: as S-P3 entry 1 (`fp` and `h` idealizations, frame
   layout, verification profile).
2. **Possession binds the manifest to the named key** — producer S-P3
   Q2/Q4 correct form, S-P3 ledger entry 2, which names "S-P2's
   degraded-mode signer-stripping companion (note 2)" as its consumer.
   Consumed by Q5: C3 is the configuration in which this link alone
   carries `SetAltered`; C2 severs it (with the hash) and goes red.
   Shared terms: `POSS`, the manifest term. Adversary at the join:
   A1.3 with DSKS, sole channel compromised. Residual: as entry 1 plus
   signature unforgeability (Dolev–Yao idealization; no `dsks` step in
   any S-P2 derivation).
3. **P8 canonical encoding of the required set — Layer 2, cross-track,
   never symbolically discharged.** Unchanged by the runs: reorder has
   no query; the set is positional (`signers0`/`signers1`, Q2 lines
   82–83); bounds beyond n = 2 and uniqueness are P8's. Adversary at
   the join: A1.3 item 2 at the byte level (reorder, duplicate) — not
   representable here; Layer 2, unclaimed. Cites P8 **[proof]** (open)
   until it exists.
4. **`Accept` ↔ P4 verdict partition** — cross-formalism join, never
   marked symbolically discharged. Every S-P2 path that stops short of
   `Accept1S`/`Accept2S` on a stripped or substituted set is a
   performed-and-failed check; its `INVALID` landing is P4's model's.
   Adversary at the join: A1.3 as above on the symbolic side; P4's
   model's own adversary on the TLA+ side (cross-formalism, not
   compared here). The waived-subset case is not modeled here (see
   "What S-P2 does not discharge").

**Produced** (offered for entry only after the author's read):

1. **Set-completeness relation** (producer: Q2, `Stripped` and
   `SignerForged` unreachable). Assumed fact for consumers: acceptance
   for manifest `m` implies a signature over the exact framed bytes
   from every signer `m`'s signed set names, each under that signer's
   own key, for |set| ≤ 2. Consumers: the capstone (A3.2 chain, per
   signer, item 3); S-P1 (integrity over bytes presupposes which
   signatures are required over them); S-P7 (per-layer completeness,
   A3.2 item 4). Shared terms: `authTuple`'s `sset` family, `framed`,
   the verified keys. Adversary at the join: A1.3 with DSKS, sole
   channel compromised. Severing companions: Q3 (cardinality half →
   `Stripped` red), Q4 (membership half → `SignerForged` red).
   Residual Layer 2: `fp` idealization (the slot match is key equality
   only under it); `h` idealization; P8 set encoding (entry 3 above);
   authorship of the bytes under the named key (S-P1, F6).
2. **Set integrity around an honest key** (producer: Q2, `SetAltered`
   unreachable). Assumed fact: no honest key is accepted as a signer
   of a manifest it never signed — the sole-channel adversary cannot
   alter the signer set or version around an honest key. Consumer: the
   relying-party story's degraded-mode cost statement (note 2, last
   bullet; A4 §A4.6) — with F3's refinement of which fields the frame
   pins and which only possession pins. Shared terms: the manifest
   term (`authTuple`), `POSS`, the frame's `mh` field. Adversary at the
   join: A1.3 with DSKS, sole channel compromised. Severing companion:
   Q5-C2 (both pins removed → red); isolation: C1 and C3 (either pin
   alone → green). Residual: `h` idealization (frame pin) and signature
   unforgeability (possession pin), each cited as the pin it supports.
3. **Cross-formalism join (not symbolically dischargeable):** nothing
   in S-P2 assumes anchor validity or a refusal state; no TLA+ join is
   consumed other than the `Accept` ↔ P4 partition (consumed entry 4).
   Recorded so the capstone does not look for another.

## What S-P2 does not discharge

- The `VALID_DEGRADED` waiver of a signature subset (A1.2.1 waivable
  item; P2's second clause): left to P4's leg on the Question 2
  precedent, disposition B5 (`ROUTED-2026-09-06.md`); the *recorded*
  half is an open coverage-map cell, not a ruling. Nothing in S-P2
  models a waiver.
- Required sets of more than two signers; canonical ordering,
  uniqueness, bounds (P8); the empty-set and malformed-member cases
  (unrepresentable in map v1 / in the algebra; P8 vectors).
- The frame's byte layout, or that `framed(...)` is the P8 frame.
- Impersonation with the adversary's own key over its own manifest and
  bytes in degraded mode: reachable by construction, out of scope, the
  registered cost (A4 §A4.6).
- Authorship — that bytes accepted under an honest named key were
  signed by that key (F6, d4): S-P1.
- The DSKS capability's practicality; the verification profile.
- Anything in strict mode beyond "the four results also hold" and what
  d7–d11 establish about the honest channel's tuple pin (F1 correction
  note, 2026-09-06). Not ablated in strict mode: the repo-leaked
  variant (Q1r) — d7–d11 use Q1d as base; the evidence check, `=id`,
  `=alg` and the attestation-signature check (d2–d4 are degraded-mode
  runs); and any check jointly with the pin other than the slot match
  (d10/d11).

**Suite rules from S-P2** (offered, in addition to S-P3's): fixture
keys that a registered query must cite are private free names; a
carried consumer judge carries its own reachable witness; a companion's
*exhibited* instance is compared to the plan's *named* instance and any
difference is a finding, since ProVerif reports the first derivation it
finds, not the one the plan traced (F3). *Added 2026-09-06 from the
cross-family falsification review, item 6 (recorded, applies to every
family):* an N1 witness is **existential** — reachable with one trace,
for one honest key on one branch — so it is a vacuity guard, not
coverage; a green safety query plus a reachable witness never licenses
a per-branch or per-key reading.

## Status toward discharge (PROPERTIES.md terms)

Tool passes: **yes** — all correct models green on every registered
query, both N1 witnesses reachable in every model, every companion red
on exactly its named query, C1 green as registered. Falsification
review by a reviewer from a different model family (ENUMERATION note 5
item 1, the gate): **RUN 2026-09-06** (non-author, `gpt-6-astra`;
report, prompt and scratch archived under
`proverif/falsification-2026-09-06/`); findings applied as
dispositioned (review log below). No registered query, prediction or
result changed. Blind reverse translation against P2's
sentence (the comparator): not run. Author read of the Q2 header
(lines 14–50) against P2's registered sentence
(`docs/phase-0-prereg-amendment-1.md` 121–128): **pending.** Reading
aids: `READING-AIDS.md`, testimony, probe not run. Collaborator's
recommendation, for the author to weigh and not a ruling: P2's symbolic
leg is at the point S-P3's was on 2026-09-04 before its reviews; the
tracker row stays `open` until the author has read the narrowed
headers (ROUTED C5) and ruled on ROUTED C8; `checked` then needs the TLA+ leg's
agreement per B2's analogue for P2 (P4 already `checked`; the `Accept`
↔ P4 join written in the coverage map).

**The question the cold read answers** (S-P3's, adopted): *Does this
model preserve the attack and the defense we intend to study, and have
we assigned every omitted detail to an explicit remaining obligation?*
For S-P2 the attack is stripping and set-shrinking (Q3, C2 exhibit
them); the defense is the signed set read by pattern, the per-slot
fingerprint match, and the two set-pins (Q2 carries them; the
companions sever each in turn).

## Review log

- 2026-09-06 — models built by the AI collaborator from the frozen
  plan (`5188e7a`) with `framed` copied verbatim from S-P3 and the
  S-P3 encoding idioms applied from the first build; Q2 trial-run in
  the scratchpad (identical results), then the ladder run once in the
  registered order (`run_ladder.sh`, `ladder.log`); no recut, no
  "cannot be proved", no warnings. Six unregistered diagnostics run and
  archived under `proverif/diagnostics/`. This file and
  `READING-AIDS.md` written from the `.out` files. No non-author
  review; no author read.
- 2026-09-06 — **Skeptic review of S-P2 (non-author; verified
  findings): one blocking, three defects, three nits — all applied.**
  Blocking: the Q1 headers (both variants, original lines 24–29)
  claimed the honest channel's tuple pin closed `Stripped`/`SetAltered`
  "by the channel alone"; the reviewer refuted the `Stripped` half by
  running the strict model with the Q3 mutation. Applied: the strict
  ablations were re-run and archived as d7 (strict + Q3 mutation:
  `Stripped` red), d8 (strict + Q4 mutation: `SignerForged` red), d9
  (strict + C2 mutation: `SetAltered` green), plus two the fix text did
  not ask for — d10 (frame `=fp` unbound, slot match kept: green) and
  d11 (slot matches removed too: `Reattributed` red) — because the
  reviewer's proposed replacement sentence said the pin closes
  "SetAltered and Reattributed on its own", and the `Reattributed`
  half was itself an untested mechanism claim (d11 shows the pin alone
  does not close it; d10 shows the slot match against the pinned tuple
  does). The Q1 headers were rewritten to what d7–d11 show
  (comment-only recut, both `.out` byte-identical, `ladder.log`).
  Defects applied: F1 correction note (above); `READING-AIDS.md` §2
  Claim and Checks paragraphs corrected and §1b sources extended
  (d7–d11), Q1d/Q1r line citations shifted by the header's +10 lines;
  ledger Consumed entry 2 and Produced entry 2 given the missing
  adversary/shared-term fields (Consumed 3 and 4 given adversary lines
  too). Nits applied: "Prediction divergences" reworded to one
  additive divergence; Q2 header range 14–50; the uncommitted D-5/D-6
  library dependency stated under "Tooling". Nothing in
  `PREDICTIONS.md` changed. Author read still pending; the
  cross-family falsification review (note 5 item 1) is still not run —
  this skeptic review was a record review with verification runs, not
  the registered gate.
- 2026-09-06 — **Cross-family falsification review of S-P2 (non-author,
  `gpt-6-astra`; the registered gate of note 5 item 1): findings applied
  as dispositioned in
  `docs/reviews/2026-09-06-codex-suite-falsification-s-p1-s-p2-s-p7-s-standing.md`.**
  The reviewer's report, prompt, model line and scratch (seven attack
  fixtures, 169 single-check mutants, `dependencies.tsv`, baseline
  reruns) are archived verbatim under
  `proverif/falsification-2026-09-06/`. Nothing in `PREDICTIONS.md`
  changed; no query was added, removed or altered; no verifier line
  changed; no result changed. Applied, all comment-only:
  *(a)* Q1d and Q1r headers (items 2, 4, 5, 13, 15, 17) — the two
  set-pins and "the frame's fingerprint (`Reattributed`)" now read
  **jointly** load-bearing, since each single removal is green
  (`dependencies.tsv:19,43,47`; `10,28,31`; `18,42,46`), and the honest
  channel's own evidence check (140 / 160) is recorded as individually
  inert defence in depth (`tsv:5–7,23–25`), the shape item 5 records in
  S-P1 and S-P7; the "no set-shrinking around an honest key" sentence
  carries Q2's one-key/one-manifest qualifier (item 13); object type
  stays carried (item 15) and byte-encoding attacks stay a coverage
  failure, not an unreachable attack (item 2).
  *(b)* Q2's header (items 2, 4, 13, 14, 15) — claim (3) now states the
  fixture rule ONE KEY, ONE MANIFEST and says the `SetAltered` judge is
  instrumentation, not a verifier check (item 13, the reviewer's
  `a_key_reuse` false positive); the two set-pins read **jointly**
  (item 4); the attestation-signature check is carried for S-P1 as a
  whole, not only in its authorship content (item 14,
  `tsv:102–104,120–125` — the review cites `:102–104,122–127`; the
  attestation rows for the n = 2 branch are in fact `:120–125`, since
  126–127 are the frame `alg`/`id` ablations, item 4's separate row);
  object type carried (item 15); byte-encoding
  unrepresentable (item 2).
  *(c)* Q1d was narrowed **within its existing line count**, so every
  `file:line` citation into it is unchanged. Q2's header is the same
  total length, but its sub-blocks shifted by one to two lines: the
  claim block 14–26 is now 14–27, "This model does not prove" 27–37 is
  now 28–38, "Carried …" 46–50 is now 48–50, and the Fixture (N2) note
  now begins at 62. The archived review's `G.pv:20–21`, `:27–37`,
  `:35–37`, `:46–50` and `:61–66` are header citations and must be read
  against those new ranges; every citation into Q2's **body** (72
  onward) and every citation into Q1d is unchanged. Q1r's header is
  also the same total length, but not line-for-line either: its first
  block gained a line (16–22 → 16–23) and its load-bearing block lost
  one (24–45 → 25–45), so the boundary block's last line, "the
  verification profile).", moved from 23 to 24 and the load-bearing
  block now runs 25–34 with the CORRECTION beginning at 35; the
  review's `R.pv:15–35` still spans claim + boundary + load-bearing but
  now reaches one line into the CORRECTION, and `R.pv:134–176` (body)
  is unchanged. The CORRECTION RECORD block was appended after the
  process in all three files.
  *(c2)* CORRECTION 2026-09-06 (cross-family review item, second pass):
  the sentence at *(c)* originally read "each of the three headers was
  narrowed **within its existing line count** … so every `file:line`
  citation in this file, in `READING-AIDS.md` and in the archived review
  is unchanged." That self-certification was false for Q2 and imprecise
  for Q1r; it is replaced above. Verified by diffing the three files
  against `proverif/falsification-2026-09-06/scratch/baseline_sp2_*.pv`.
  *(d)* `READING-AIDS.md`: the §1b `=fp(kX)` row reworded to
  load-bearing **jointly** with the slot match, with the matrix lines
  (items 4, 17); the §1c `SetAltered` meaning and the §1d Claim's third
  sentence qualified by one key, one manifest (item 13); a new §1d
  block of boundary sentences for items 1, 2, 3, 6, 14, 15 and 16; the
  §2 "Second header correction" paragraph; the front-matter note that
  the line citations survive the correction.
  **Re-run:** the three edited models were re-run with
  `proverif -lib ../../lib/tessera_theory.pvl` and their `.out` files
  refreshed; **all seven RESULT lines in each are identical to the
  pre-edit run, at the same output line numbers** — in fact each `.out`
  is byte-identical (Q1d/Q1r 386, 392, 398, 404 true; 580, 812, 1055
  false; Q2 354, 360, 366, 372 true; 536, 756, 987 false). Recorded in
  `ladder.log` as `recut=comment-only-crossfamily-2026-09-06
  out=identical`. The five companions (Q3, Q4, C1, C2, C3) were **not**
  edited and not re-run: the reviewer found no overclaim in their
  headers, and C2's header names one concrete exhibited attack rather
  than a general "never signed" reading, so item 13's qualifier lands
  on Q2 (and the two Q1 variants that inherit its claim), as
  dispositioned. **Post-freeze additions (unregistered): none** — this
  application added no query, so there is nothing to record under the
  S-P3 precedent. Items 1, 2, 3, 6, 14, 15, 16 are boundary/recorded
  findings and are carried as reading-aid sentences, not as new
  obligations here; item 8's ledger entry (key-use discipline) is
  S-P1's finding and belongs to S-P1's record, not S-P2's. Author read
  still pending.
- 2026-09-06 — **Second-pass skeptic review of the application above
  (non-author): six findings verified and applied. Comment/record text
  only; no `.pv` file was touched, so nothing was re-run and no `.out`
  changed.** Applied:
  *(i)* review-log item *(c)* rewritten (see *(c2)* there): the
  self-certification "each of the three headers was narrowed within its
  existing line count … so every `file:line` citation … is unchanged"
  was **false for Q2** — the header's total length is unchanged (a +2
  hunk at 15–53 offset by a −2 hunk at 55–71) but its sub-blocks moved
  (claim 14–26 → 14–27; "does not prove" 27–37 → 28–38; "Carried …"
  46–50 → 48–50; Fixture (N2) 61 → 62), so the archived review's
  `G.pv:20–21`, `:27–37`, `:35–37`, `:46–50` and `:61–66` must be read
  against the new ranges. Verified by diffing
  `proverif/falsification-2026-09-06/scratch/baseline_sp2_q2_degraded_compromised.pv`
  against the current file; every Q2 citation into the body (72 onward)
  is identical line for line.
  *(ii)* **The second-pass finding itself was corrected on one point
  before being applied.** It stated that "Q1d and Q1r are genuinely
  unchanged — both of their header hunks are equal-length (16,19c16,19
  and 21,45c21,45)". Those two hunks are **Q1d's**. Q1r diffs as
  `16,22c16,23` and `24,45c25,45` — a +1 and a −1 — so its header is
  the same total length but not line-for-line: "the verification
  profile)." moved from 23 to 24 and the load-bearing block moved from
  24–35 to 25–34, with the CORRECTION beginning at 35. The review's
  `R.pv:15–35` still spans claim + boundary + load-bearing, now
  reaching one line into the CORRECTION; `R.pv:134–176` (body) is
  unchanged. *(c)* and the reading aid's front matter say so.
  *(iii)* "Status toward discharge": the gate now reads **RUN
  2026-09-06** with the archive path, replacing "**NOT RUN.**", which
  the entry above contradicted; the tracker-row sentence now waits on
  the author's read of the narrowed headers (ROUTED C5) and a ruling on
  ROUTED C8, not on a run that has happened. Recording that a run
  happened is a statement of fact, not an author decision.
  *(iv)* the Pending-ROUTED-C8 note now names the **second, editable**
  copy of the routed sentence — Produced ledger entry 1 at line 288
  restates the frozen plan's "a signature over the exact framed bytes
  from every signer" verbatim for its consumers — so a "no" ruling
  cannot correct the plan's copy while the ledger's stands. Nothing was
  changed in either copy; `PREDICTIONS.md` was not touched.
  *(v)* item *(b)*'s `tsv:102–104,120–125` and the reading aid's item 14
  sentence both gain a half-sentence recording that the archived review
  cites `:102–104,122–127` for the same claim and that `:120–125` is
  the correct range (G's 40 rows are `tsv:94–133`; 120–125 are
  `G:186`/`G:187` drop/tag/binding, all TTTTFFF, while 126–127 are the
  frame `alg`/`id` ablations belonging to item 4's row) — so a later
  reader does not read the divergence as a transcription error.
  *(vi)* `READING-AIDS.md`: §1d's two stale Q2 header citations
  corrected (Claim 14–26 → **14–27**; Boundary 27–37 → **28–38**);
  §1c's `.out` lines (354, 360, 366, 372, 536, 756, 987) and §1b's
  check table (161/179, 163/181, 164/182, 165/184–185, 166/186–187,
  167/188,190, 168/189,191) were re-checked and still resolve. The
  item 15 boundary sentence's `scratch/a_wrapper_replay.out:588` now
  says the `.out` is regenerable and not archived (`ARCHIVE-NOTE.md`:
  265 `.pv`/index files archived, **0** `.out` files); the citation is
  substantively sound — the run was reproduced here with `proverif -lib
  ../../../lib/tessera_theory.pvl a_wrapper_replay.pv`, giving `RESULT
  not event(Attack) is false.` at line **588** and the four registered
  queries green at 594/600/606/612, matching `CODEX-REVIEW.md`. The
  regenerated `.out` was written to a scratch path outside the tree and
  **not** added to the archive, which records those files as
  deliberately not archived. The item 1 sentence cites
  `scratch/a_reordered_keys.pv`, a file that is archived; it needs no
  change.
  *(vii)* **one finding extended.** The second-pass review said §1d's
  two citations were "the only two citations in the document that the
  Q2 edit invalidated". §9's first bullet was a third: it cited "Q2's
  header (lines 38–45)" for the load-bearing block, which now runs
  39–47, and asserted "the header text was not edited", which the
  application above makes false. The bullet is corrected in place with
  its own dated note; nothing else in §9 cites a Q2 header line.
  `RESULTS.md`'s own "Author read of the Q2 header (lines 14–50)" is
  **correct as written** and was not changed: the claim, boundary,
  load-bearing and carried text still ends at line 50, with the
  CORRECTION RECORD beginning at 51. **Post-freeze additions
  (unregistered): none** — this pass added no query. `PREDICTIONS.md`
  unchanged; no verifier line, registered query, prediction or result
  changed. Author read still pending.

**Pending author ruling (ROUTED C8)** — finding 12 of the cross-family
review: two honest signers under one manifest may sign *different*
framed payloads and the verifier accepts (the reviewer's
`a_mixed_payload`, reachable, all four registered queries green), and
P2's registered text does not say the signers sign a *common* content.
If the author rules that P2 means one framed byte string signed by every
required signer, the Q2 verifier would gain an equality across signer
slots and S-P2 would gain a splicing companion, both recorded as a
post-freeze, unregistered addition; if the author rules that it does
not, the frozen plan's exported sentence "a signature over the exact
framed bytes from every signer" is corrected to per-slot frames and the
relying-party story says a multi-signer attestation is a set of
per-signer attestations of possibly different bytes — and with it the
identical sentence in this file's Produced ledger entry 1 (line 288),
which restates the plan's wording for consumers (the capstone, S-P1,
S-P7); both copies stand or are corrected together. Nothing has been
changed in either on the collaborator's own motion.
