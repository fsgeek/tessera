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

---

## Post-freeze addendum 1 — results, 2026-09-12

**STATUS: PROPOSED — 2026-09-12 — produced by the AI collaborator; not
adopted; the commit is the author's.** This section is appended, not
edited in: no sentence above it is changed. It records the run of the
addendum registered at the end of `PREDICTIONS.md` ("Post-freeze
addendum 1 — 2026-09-12: common attested content", Amendment 5 §A5.4,
ROUTED C8, ADOPTED (author) reading (a)). Tooling as above (ProVerif
2.05, `-lib formal/suite/lib/tessera_theory.pvl`); the whole ladder —
now ten entries — was re-run by `run_ladder.sh` in one pass
(`ladder.log`, entries 1–10 plus the restored history block). Every
run terminated in ≤ 1 s against 900–1800 s boxes; no `.out` contains
"cannot be proved"; no warnings; no recut.

### What changed in the model

`sp2_q2_degraded_compromised.pv` gained the registered encoding, and
nothing else:

- **Three equalities in `Verifier2S`** (lines 228, 229, 230, under the
  marked comment at 225–227), placed after both frames are
  destructured and both manifest-hash checks pass: `if ota = otb then`,
  `if cva = cvb then`, `if pla = plb then`. Each signer's frame keeps
  its own `=fp(kX)` (221, 223). `Verifier1S` is untouched.
- **One new private report channel** `contentCh` (157), declared like
  the other report channels, emitted **at the single `Accept2S` point**
  in parallel with the existing reports (235, inside the report block
  232–235). `setCh`, `slotCh` and `acceptCh` and their outputs are
  untouched.
- **`event Spliced(bitstring, bitstring, bitstring)`** (160) and the
  registered query (164–165, the file's two-line query style):
  `query t: bitstring, fa: bitstring, fb: bitstring; event(Spliced(t,
  fa, fb)).` Every pre-existing query is carried **verbatim** and in
  its original order; the new one is appended after them.
- **`ContentJudge`** (275–284): reads `contentCh`, destructures both
  frames, fires `Spliced(tJ, faJ, fbJ)` when any of object type,
  canonicalization version or payload differs, and emits nothing
  otherwise. Judge locals are `…J`-suffixed (no library-name
  shadowing, the S-P3 rule). Added to the process at 299.
- **Header**: an `ADDENDUM 2026-09-12 (Amendment 5 §A5.4)` comment
  block at **51–70**, placed immediately after the existing claim
  block and before the `CORRECTION 2026-09-06` marker, carrying the
  two registered sentences — added to "This model proves": for
  required sets of two, the accepted frames agree on object type,
  canonicalization version and payload (Amendment 5 §A5.4); added to
  "This model does not prove": nothing about the encoding or ordering
  of the equal fields (P8). The block is not interleaved with the
  existing text, and the CORRECTION RECORD footer stays where it is
  (now 301–342).

`sp2_q6_companion_content_unchecked.pv` (new, 244 lines) is that file
with the three equalities **absent** — the n = 2 verifier exactly as it
stood — marked `MUTATION (Q6-C)` at 173–175, its own claim block at
1–41, and no CORRECTION RECORD footer (the other five companions carry
none either). Its body is otherwise line-for-line the amended Q2 body:
`diff` of amended Q2 94–299 against companion 43–244 shows exactly the
six-line-for-three-line mutation hunk and nothing else.

`run_ladder.sh` gained two entries after Q5-C3: `run
sp2_q2_degraded_compromised 900` (Q6 **is** the amended Q2 model; it is
re-run under its own registered 15-minute box and rewrites the same
`.out`) and `run sp2_q6_companion_content_unchecked 900` last.

### Predictions vs observed

| Query | Model | Registered prediction (p) | Observed | Outcome / branch fired |
|---|---|---|---|---|
| Q6 common attested content, correct model, degraded, sole channel compromised | `sp2_q2_degraded_compromised` (amended in place) | `Spliced` unreachable, terminating, Q2 lines unchanged (0.80); unexpectedly reachable = model defect (0.08); Q2 results changed = divergence (0.07); timeout (0.05) | `Spliced` **unreachable** (`.out` 1013); `Stripped`, `SignerForged`, `SetAltered`, `Reattributed` unreachable (378, 384, 390, 397); both N1 witnesses reachable (561, 778); carried `HonestAccepted` reachable (1007); `rc=0`, 1 s against a 900 s box | **unreachable, terminating, Q2 results unchanged — as predicted** (0.80 branch) |
| Q6-C content-splicing companion | `sp2_q6_companion_content_unchecked` | `Spliced` reachable with exactly the registered shape, no cryptographic step (0.85); recut needed (0.08); companion green (0.04); timeout (0.03) | `Spliced` **reachable** (`.out` 1213; goal 1017, derivation 1019–1181, trace 1187–1211); `Stripped`, `SignerForged`, `SetAltered`, `Reattributed` unreachable (372, 379, 386, 393); witnesses reachable (558, 779, 1011); `rc=0`, 0 s against a 900 s box | **violation as required** (0.85 branch); red on exactly `Spliced`; **no recut** — but the *exhibited* instance is not the plan's named instance (F9 below), so the "exactly that shape" half of the 0.85 branch is qualified, not claimed |

### RESULT lines, verbatim

Q6 — `proverif/sp2_q2_degraded_compromised.out`:

```
378:RESULT not event(Stripped(t_2,v)) is true.
384:RESULT not event(SignerForged(t_2,k)) is true.
390:RESULT not event(SetAltered(kH_2,m,t_2)) is true.
397:RESULT not event(Reattributed(kX_1,kH_2,fb_4)) is true.
561:RESULT not event(HonestComplete(authTuple(issuerId[],fp(pk(skA1[])),signers0,algH[],verH[]),verified1(k1))) is false.
778:RESULT not event(HonestComplete(authTuple(issuerId2[],fp(pk(skA2[])),signers1(fp(pk(skB2[]))),algH[],verH[]),verified2(k1,k2))) is false.
1007:RESULT not event(HonestAccepted(k,fb_4)) is false.
1013:RESULT not event(Spliced(t_2,fa_2,fb_4)) is true.
```

Q6-C — `proverif/sp2_q6_companion_content_unchecked.out`:

```
372:RESULT not event(Stripped(t_2,v)) is true.
379:RESULT not event(SignerForged(t_2,k)) is true.
386:RESULT not event(SetAltered(kH_2,m,t_2)) is true.
393:RESULT not event(Reattributed(kX_1,kH_2,fb_4)) is true.
558:RESULT not event(HonestComplete(authTuple(issuerId[],fp(pk(skA1[])),signers0,algH[],verH[]),verified1(k1))) is false.
779:RESULT not event(HonestComplete(authTuple(issuerId2[],fp(pk(skA2[])),signers1(fp(pk(skB2[]))),algH[],verH[]),verified2(k1,k2))) is false.
1011:RESULT not event(HonestAccepted(k,fb_4)) is false.
1213:RESULT not event(Spliced(t_2,fa_2,fb_4)) is false.
```

### The companion's trace, against the registered shape

The registered prediction named the trace: *honest signers A2 and B2 of
manifest `m2`, each fed a different adversary-chosen payload, both
frames presented under one tuple, `Accept2S` fires.* The exhibited
trace (`.out` 1187–1211) has the right **structure** and the wrong
**instance**. Structure: one adversary input to the n = 2 branch at
`{75}` carrying one tuple, two keys, two possession proofs over that
tuple, two attestation signatures and two frames; both frames carry the
same object type and canonicalization version and the **same manifest
hash** `h(t)`, and differ only in the payload field; `event Accept2S`
fires once at `{88}` (1205), the single `contentCh` report goes out at
`{94}` and is received at `{124}` (1207), and `event Spliced` fires at
`{128}` (1209). The only cryptographic step in the whole trace is the
channel evidence forged with the leaked `skS` published at `{10}`
(1201) — no `dsks`, no forgery, nothing the Dolev–Yao attacker does not
already hold. Instance: the tuple is `authTuple(a, fp(pk(a_1)),
signers1(fp(pk(a_2))), a_3, a_4)` and both slots are filled by
**adversary-generated keys** `a_1`, `a_2`, not by the honest `skA2` and
`skB2` — ProVerif exhibited the cheapest witness, which is the
registered degraded-mode impersonation cost (A4 §A4.6) carrying the
splice, rather than the honest-signer splice the plan named.

**F9 — the registered instance is reachable too; ProVerif exhibited a
cheaper one.** Recorded, not absorbed: this is the same shape as F3
(Q5-C2's exhibited witness differed from the plan's named witness), and
it is handled the same way, by an unregistered diagnostic rather than
by changing anything registered. **d12**
(`proverif/diagnostics/d12_q6c_registered_witness.pv`, box 900 s,
`diagnostics.log`) is Q6-C plus one extra query naming the registered
instance literally — `Spliced(m2, framed(OT_ATTEST, algH, issuerId2,
fp(pk(skA2)), h(m2), canonVerH, pla), framed(OT_ATTEST, algH,
issuerId2, fp(pk(skB2)), h(m2), canonVerH, plb))`. It is **reachable**:

```
1428:RESULT not event(Spliced(authTuple(issuerId2[],fp(pk(skA2[])),signers1(fp(pk(skB2[]))),algH[],verH[]),framed(OT_ATTEST,algH[],issuerId2[],fp(pk(skA2[])),h(authTuple(issuerId2[],fp(pk(skA2[])),signers1(fp(pk(skB2[]))),algH[],verH[])),canonVerH[],pla_2),framed(OT_ATTEST,algH[],issuerId2[],fp(pk(skB2[])),h(authTuple(issuerId2[],fp(pk(skA2[])),signers1(fp(pk(skB2[]))),algH[],verH[])),canonVerH[],plb_1))) is false.
```

Its trace (d12 `.out` 1362–1426; query 1214, derivation 1221–1356) is
exactly the registered shape: honest A2 takes payload `a_2` at `{38}`,
self-signs `m2` and frames and signs those bytes (1388–1396); honest
B2 takes a *different* payload `a_6` at `{50}` and does the same
(1408–1416); the adversary forges the channel evidence for `m2` with
the leaked `skS` and presents both honest possession proofs, both
honest attestation signatures and both honest frames in one input at
`{75}` (1418); `Accept2S` fires (1420), the one `contentCh` report is
read (1422), and `Spliced(m2, fa, fb)` fires (1424). No cryptographic
step: every honest signature is replayed as the honest signer
published it. So the registered shape is present in Q6-C and is what
the amended verifier's three equalities close; d12 is an unregistered
diagnostic and is evidence about the trace, never about a registered
query.

Because Spliced is unreachable in Q6 with the honest instance reachable
in Q6-C, the three equalities are **load-bearing for `Spliced`** and
that is the severing pair the addendum registered. Nothing else in
Q6-C's result set moved, so the equalities are also shown not to be
load-bearing for any other query.

### The eight-model comparison

Required by the addendum: "the ladder outcomes in `RESULTS.md` for
Q1–Q5 must be identical after the change below, and any difference is a
divergence to be recorded, never absorbed." The eight pre-existing
`.out` files were copied to `proverif/pre-addendum-2026-09-12/`
(together with `ladder.log.pre`) **before** the run, so the comparison
is on the record.

- **Seven models byte-identical** (`cmp`): `sp2_q1_strict_dns_compromised`,
  `sp2_q1_strict_repo_compromised`, `sp2_q3_companion_cardinality_ignored`,
  `sp2_q4_companion_slot_unbound`, `sp2_q5_c1_fponly_frame_mh`,
  `sp2_q5_c2_fponly_frame_nomh`, `sp2_q5_c3_manifestposs_frame_nomh`.
  Their `.pv` files were not touched. Every `.out` line citation into
  them anywhere in this file and in `READING-AIDS.md` still resolves
  unchanged.
- **Q2's seven pre-existing RESULT lines are identical in text**
  (`diff` of the RESULT lines with line numbers stripped: empty) and
  moved in the `.out` because the model file grew: 354→378, 360→384,
  366→390, 372→397, 536→561, 756→778, 987→1007. The eighth RESULT line
  (1013, `Spliced`) is the new one. Every `.out` line citation to Q2 in
  the "Ladder outcomes" table above, in the F-findings and in
  `READING-AIDS.md` §1c must be read against the new numbers; the old
  numbers are not corrected in place.
- **No divergence.** No registered query, prediction, companion,
  fixture, timebox or judge above this section changed; nothing was
  absorbed.

### Line-shift table (Q2 model body and header)

The Q2 `.pv` went from 291 to 342 lines. `RESULTS.md`, `READING-AIDS.md`
and the archived Codex review (`G.pv:N`) cite its **body** line
numbers; those citations are **not** corrected in place. Resolve any
pre-2026-09-12 citation `N` into
`sp2_q2_degraded_compromised.pv` with this table (verified line by line
against `git show HEAD:…/sp2_q2_degraded_compromised.pv`):

| Old lines | Shift | New lines | What the segment is |
|---|---|---|---|
| 1–50 | **+0** | 1–50 | STATUS, prediction, claim / does-not-prove / load-bearing / carried block — **every existing header citation into 14–27, 28–38, 39–47, 48–50 is unchanged** |
| — | — | 51–70 | **new**: the `ADDENDUM 2026-09-12` header block (20 lines) |
| 51–132 | **+20** | 71–152 | `CORRECTION 2026-09-06` marker (51→71), Theory (54→74), Fixture N2 (62→82), Encoding idioms (68→88), Run (72→92), declarations, events, and all seven existing queries (112–132 → 132–152) |
| — | — | 153–165 | **new**: the addendum declaration block (13 lines: `contentCh` 157, `event Spliced` 160, the `Spliced` query 164–165) |
| 133–191 | **+33** | 166–224 | `AuthorityS` (134→167), `Registrar` (139–140→172–173), `Signer` (146–155→179–188), `Verifier1S` (158–172→191–205), `Verifier2S` head through `if mhb = h(t)` (175–191→208–224) |
| — | — | 225–230 | **new**: the three equalities and their comment (6 lines) |
| 192–195 | **+39** | 231–234 | `event Accept2S` (192→231) and the first three report outputs |
| — | — | 235 | **new**: `\| out(contentCh, (t, fa, fb)) ).` — old line 195 was split, its closing `).` now sits here |
| 196–233 | **+40** | 236–273 | `SetJudge` (201–214→241–254), `MemberJudge` (220–226→260–266), `Judge` (229–233→269–273) |
| — | — | 274–284 | **new**: `ContentJudge` and its comment (11 lines) |
| 234–291 | **+51** | 285–342 | `process` (235→286), the parallel composition (248→299, edited in place to add `\| !ContentJudge`), and the CORRECTION RECORD footer (250–291→301–342) |

Two lines were edited in place rather than shifted: old 195 (the third
report line, split to carry `contentCh`) and old 248 (the process's
parallel composition, which gained `| !ContentJudge`). The CORRECTION
RECORD footer's own internal citations (to body lines 146–155, 165,
166, 167, 168, 184–191, 220–226, 245–246) are citations *into this
file* and are subject to the same table; they were **not** rewritten,
per amend-don't-rewrite.

`ladder.log` is truncated by `run_ladder.sh` on every run, so the
hand-appended history from 2026-09-06 (the two `recut=` blocks) was
restored verbatim from `pre-addendum-2026-09-12/ladder.log.pre` under a
marked "history carried forward" line, followed by a dated note for
this run.

### Ledger

**Produced entry 1 is now read with §A5.4's meaning.** Its restated
plan sentence — "acceptance for manifest `m` implies a signature over
the exact framed bytes from every signer `m`'s signed set names, each
under that signer's own key, for |set| ≤ 2" (this file's Produced entry
1, line 288) — is read as Amendment 5 §A5.4 registers it: **every
required signer's frame over the same content, in its own frame.** The
six non-fingerprint fields agree across signer slots; only the
key-fingerprint field differs. Three of the six (algorithm, identity,
manifest hash) are carried by the shared tuple and were already pinned;
the other three (object type, canonicalization version, payload) are
what the verifier now checks. **No ledger entry is altered here** — not
Produced entry 1, not the `PREDICTIONS.md` copy of the same sentence,
neither of which the collaborator touches; this paragraph records the
reading, as the addendum's "Ledger" paragraph asks. The severing
companion for the common-content half of entry 1 is Q6-C; the residual
Layer-2 items are unchanged, plus one addition: the equalities are term
equality standing in for byte equality (the `h`/`fp` idealization note
of Consumed entry 3), so "same content" here means *same term*, and P8
still owes the encoding and ordering of the equal fields.

The "**Pending author ruling (ROUTED C8)**" paragraph at the end of the
review log above is **not edited**. It is now historically superseded
by the author's ruling recorded in Amendment 5 §A5.4 (ADOPTED (author),
reading (a)), and the fork it describes is resolved in favour of the
first limb: the verifier gained the equality across signer slots and
S-P2 gained a splicing companion, "both recorded as a post-freeze,
unregistered addition" — which is what this section is. The second
limb (correcting the plan's exported sentence to per-slot frames) is
therefore not taken, and neither copy of the sentence is corrected.

### Status toward discharge — **unchanged**

**This section changes nothing about the tracker row.** P2's row stays
`open`, exactly as the "Status toward discharge" section above leaves
it. That section's recommendation — that the row stays `open` until the
author has read the narrowed headers (ROUTED C5) and ruled on ROUTED
C8 — is now half discharged and half not: ROUTED C8 **is** ruled
(Amendment 5 §A5.4, reading (a)), and this addendum implements the
ruling; the **author's C5 read is still owed** (the request is
`formal/suite/READ-C5-2026-09-12.md`), and the addendum has just added
a block to the Q2 header — the 51–70 block — which was not in the text
the C5 read was requested against. Tool passes are still yes on every
registered query, both N1 witnesses are still reachable in every model,
every companion is still red on exactly its named query, and Q6-C joins
them. None of that moves the row: the row is the author's, `checked`
still additionally needs the TLA+ leg's agreement per B2's analogue,
and the cross-family falsification review has not been re-run against
the amended model (it reviewed the pre-addendum body; the three
equalities, `contentCh`, `ContentJudge` and `Spliced` are unreviewed by
a non-author model). Recorded as an open obligation, not as a finding.

## Cross-family review 2026-09-12 — dispositions applied

Source: `docs/reviews/2026-09-12-codex-falsification-amendment-5-checks.md`
(OpenAI Codex CLI, `gpt-6-astra`, non-author; scratch under
`proverif/falsification-2026-09-12/scratch/`). **No S-P2 file was
changed by this pass**; the review found no overclaim in this family.
The open obligation recorded at the end of the section above — that
the cross-family falsification review had not been run against the
amended model — is hereby **discharged**.

**1 — no overclaim in the Q2/Q6 header.** Checked: the ADDENDUM block's
bounded term-equality claim and its explicit encoding exclusion
(`sp2_q2_degraded_compromised.pv:54–59`) say no more than the verifier
does, and this file's §on the companion distinguishes the generic
attacker-key trace from the honest-instance diagnostic
(`RESULTS.md:704–752`; `proverif/diagnostics/d12_q6c_registered_witness.out:1428`).
No change.

**2 — the three new equalities are individually load-bearing, and the
witnesses are intact.** Confirmed from the reviewer's single-removal
matrix: removing `ota = otb`, `cva = cvb` or `pla = plb` alone each
turns exactly one query — `Spliced` — red, with every pre-existing
polarity unchanged (`falsification-2026-09-12/scratch/matrix.txt:1–3`;
`no_type.out:1213`, `no_version.out:1213`, `no_payload.out:1213`). The
committed witnesses M1, M2 and the carried honest acceptance stay
reachable (`sp2_q2_degraded_compromised.out:561,778,1007`), and the
companion is red on `Spliced` only (`sp2_q6_companion_content_unchecked.out:1213`,
with `Stripped`/`SignerForged`/`SetAltered`/`Reattributed` green at
`:372,379,386,393`). Attacks that keep the verifier intact did not
break it: wrong slot fingerprints, nested-payload difference and
unequal accepted manifest hashes are all unreachable
(`field_attacks.out:1279,1530`; `second_manifest.out:1648,1412`).
Confirmations; no change.

**3 — the reviewer's verdict on the §A5.4 reading (a), noted.** The
reviewer's design reading, recorded here as a note and **not** as an
action: reading (a) is coherent as agreement on *one* canonical
representation, and it deliberately **rejects mixed-version bundles** —
a relying party presenting A's version-V frame beside B's frame
re-canonicalized under V′ is rejected by the new version equality
(`sp2_q2_degraded_compromised.pv:229–230`), or earlier by the signature
check if B's bytes were altered under B's old signature (`:219–220`).
Any policy that would *accept* cross-version semantic equivalence would
need its own registered design decision: Amendment 5 §A5.4 does not
grant it, and the P8 exclusion carried in the header
(`.pv:58–59`) is an exclusion of encoding and ordering obligations, not
an authorization to accept them as equivalent. **No action.**

## Author read 2026-09-12 — status correction (appended 2026-09-13; AI collaborator, recording the record)

Sentences above that say the author's ROUTED C5 read of this family's narrowed headers is owed or pending are superseded and left as written per amend-don't-rewrite. The read was completed on 2026-09-12 and its four answers are entered at `formal/suite/READ-C5-2026-09-12.md`, "Author's answers" (S-P1: one NO, repaired; S-P2: YES; S-P7: one NO, repaired; S-STANDING: YES). No further author read of any suite claim block is requested by the record. What remains for the author on these families is different in kind and happens once: the adjudication of the cross-family review findings that moves rows from `checked` to `discharged` (`formal/BAND0-EXIT.md` item E9), assembled into one sitting by the owner instance.
