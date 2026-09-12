# S-P1 — integrity (headline, operative form): results

**STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not
adopted; the commit is the author's.** Predictions were frozen at
`5188e7a` (`PREDICTIONS.md`) before any model existed. This file
records predictions against observed outcomes in the registered
three-outcome vocabulary, the one build fix, the findings, the
ablation probes that locate the load, and the A3.3 ledger entries S-P1
offers the suite. It does not change `formal/PROPERTIES.md`; P1's
tracker row is the author's to move. Falsification review: **RUN
2026-09-06** — cross-family, Codex `gpt-6-astra`; see "Status toward
discharge" and the review log. Author read: **pending**. *(Status
amended 2026-09-06 applying the cross-family review; it previously
read "Falsification review: **NOT RUN**". The two dated review-log
entries below that end "Falsification review remains NOT RUN" are the
records of the earlier skeptic passes and stay as written.)*

Tooling: ProVerif 2.05, `-lib formal/suite/lib/tessera_theory.pvl`
(with D-5/D-6 entered 2026-09-06). Models and outputs:
`formal/suite/s-p1/proverif/`. Run-1 outputs (before the Q3 build
fix) are archived under `proverif/run1/`; the ladder script is
`proverif/run-ladder.sh`; the unregistered ablation probes and their
outputs are under `proverif/probes/`. Every run terminated in ≤ 1 s
against boxes of 15–30 min (`proverif/ladder.log`). Runs 3 and 4
(2026-09-06, after the skeptic pass) are comment-only re-runs of the
whole ladder following the Q3 header correction below; all five
`.out` files are byte-identical to run 2, so run 2's line citations
stand throughout this file. Run 5 (2026-09-06, skeptic pass 2) is a
further comment-only re-run after a dated provenance note was appended
to `sp1_q2_degraded_compromised.pv` (below, review log); all five
`.out` again byte-identical, compared byte-for-byte against the run-4
files. Runs 6 and 7 (2026-09-06, applying the cross-family review) are
two further comment-only re-runs — run 6 after the header narrowings
were written in place, run 7 after each edited model gained a dated
LINE-COUNT NOTE; all five `.out` remain byte-identical to run 2, so
the `.out` line citations in this file still stand. The `.pv` line
citations, which the in-place header growth did move, were converted
(review log below).

## Ladder outcomes

| Query | Registered prediction (`PREDICTIONS.md`) | Observed (run 2, working-tree `.out`, uncommitted) | Outcome / branch fired |
|---|---|---|---|
| Q1 strict, DNS compromised — (i) unrestricted `Accept ⟹ IssuerSigned`; (ii) headline `AcceptedUnderHonestKey ⟹ IssuerSigned`; (iii) N1 `HonestAccepted` reachable | all three as stated (0.75); violation (0.15); timeout (0.10); box 15 min | (i) **true** (`.out:201`); (ii) **true** (`.out:208`); (iii) **reachable** (`.out:396`, trace at 213–395) | **termination, as predicted** (0.75 branch); 0 s |
| Q1 strict, repo compromised — same three | same | identical: `.out:201`, `:208`, `:396` | **termination, as predicted**; 0 s |
| Q2 degraded, sole channel compromised — (i) headline, **the registered P1 [model] claim for this leg** | unreachable, terminating (0.70); real violation (0.10); timeout (0.20); box 30 min | **true** (`.out:173`); the proof's derivation carries `IssuerSigned` in its hypothesis for both honest keys (`.out:171–172`) | **termination, as predicted** (0.70 branch); 0 s |
| Q2 (ii) unrestricted `AcceptS ⟹ IssuerSigned` | **violation, as registered** (0.85); unexpectedly unreachable (0.10) = model defect; timeout (0.05) | **false** (`.out:499`), trace found (`.out:498`): the adversary's own key `k` is vouched for by the compromised sole channel, self-possesses, self-signs its own frame (`.out:354`) | **violation, as registered** (0.85 branch) — impersonation, the degraded-mode cost (s-p3/RESULTS.md F8, RULED (author) 2026-09-05; Amendment 4 §A4.6) |
| Q2 (iii) N1 | reachable | **reachable** (`.out:349`, trace 178–348) | as predicted |
| Q3 companion A: signature not bound to presented bytes — headline **must go red**, N1 must stay reachable | violation, trace readable, `fb' ≠ fb` visible (0.80); cannot go red (0.10) = amendment trigger; timeout (0.10); box 15 min | headline **false** (`.out:331`), trace found (`.out:330`); N1 **reachable** (`.out:510`) | **red as required** (0.80 branch); trace-inspection rule satisfied (Finding F4); one build fix before the run (below); 0 s |
| Q4 companion B: frame fields outside the signature — headline **must go red**, N1 reachable | violation (0.80); companion could not fail (0.10); timeout (0.10); box 15 min | headline **false** (`.out:328`), trace found (`.out:327`); N1 **reachable** (`.out:504`) | **red as required** (0.80 branch); the altered fields are exactly the F7 bound-but-unchecked pair (Finding F6); 0 s |

Companion isolation, as required (red on exactly the named query, green
on the rest): in both companions the headline is the only query whose
verdict differs from Q2's. `HonestAccepted` is reachable in all five
models (`sp1_q1_*.out:396`, `sp1_q2_*.out:349`, `sp1_q3_*.out:510`,
`sp1_q4_*.out:504`). The unrestricted contrast (ii) is carried in the
companions for completeness and is **false** there
(`sp1_q3_*.out:663`, `sp1_q4_*.out:654`) exactly as it is in the
correct Q2 form (`sp1_q2_*.out:499`, registered red): it is not a
companion discriminator and is not claimed as one. No ProVerif warning
in any `.out`.

Fixture (`PREDICTIONS.md`, "Fixture statement"): every model carries
two honest issuers (`skI`, `skI2`) with honestly published manifests
and adversary-chosen payloads; the strict models carry two authority
channels with two honest tuples each; the N1 witness is judge-emitted.
The registered fixture was built as registered; nothing to record as
an omission.

## Prediction divergences

None. Four notes that are not divergences:

1. **Build fix, not a recut (Q3, run 1 → run 2).** Run 1 of
   `sp1_q3_companionA_sig_unbound.pv` failed to build (rc = 2:
   `Error: variable fbSigned should be declared with a type`,
   `run1/sp1_q3_companionA_sig_unbound.out:2`). The registered
   mutation — "verifies a signature and returns the presented bytes"
   — was written as `let (=BYTES, fbSigned) = checksign(sg, kX)`;
   ProVerif requires `fbSigned: bitstring`. One token added; the
   mutation, the queries, and every other line are unchanged. Run-1
   outputs of all five models are archived under `run1/`; the four
   models that built in run 1 have identical `RESULT` lines in run 2.
   The whole ladder was re-run (run 2) rather than Q3 alone.
2. **Q3's exhibited alteration is wider than the prediction's
   example.** The plan predicted "presents `fb'` with the same frame
   fields and a different payload". ProVerif's derivation leaves every
   unpinned frame field free (`.out:171`: `ot_1`, `cv_1`, `pl_1` are
   attacker terms) and the reconstructed trace instantiates all three
   with fresh attacker names (`a_4`, `a_5`, `a_6`) against the issuer's
   `OT_ATTEST`, `canonVerH`, `a_2`. The payload differs, as predicted;
   so do the two other unpinned fields. This is the same attack with
   more of the unsigned surface exercised, not a different one
   (Finding F4).
3. **The companions carry an unregistered third query (added
   2026-09-06, skeptic nit).** `PREDICTIONS.md` registers two queries
   per companion (headline red; N1 reachable). Both companion models
   also carry the unrestricted contrast (ii), unregistered for Q3/Q4;
   it is red there as in Q2 and is not used as a discriminator (see
   "Companion isolation"). An addition, not a change to any
   registered query or outcome.
4. **The frozen plan's adversary sentence overstates — recorded, the
   plan is NOT edited (cross-family review item 9, 2026-09-06).**
   `PREDICTIONS.md` "Adversary and modes" (lines 160–162) says "A1.3
   throughout: item 1 … is the capability under test; items 2–6 are
   present, not defended against here except as the verifier's other
   checks incidentally block them". Two of those items have no
   representation in any S-P1 model, so "present" is not true of them.
   **A1.3 item 2** (strip, reorder or duplicate signatures within the
   signature set): each verifier reads exactly one signature `sg`, and
   the manifest's signer-set field `ss` is destructured and never used
   (`sp1_q2_degraded_compromised.pv:169–172`), so no set operation can
   be posed at all. The reviewer's words for this are worth keeping:
   "a coverage failure, not an unreachable attack". **A1.3 item 5**'s
   anchoring half (anchor anything): no anchor term, event or process
   exists anywhere in this family. Item 4's re-framing half is present
   only as arbitrary payload terms — the reviewer's A6 adds an honest
   issuance of a wrapper-typed frame under a foreign version and the
   Q2 verifier accepts it
   (`falsification-2026-09-06/scratch/a6_foreign_type.pv`, RESULT `not
   event(Attack) is false` at `.out:747`, reproduced below) — which is
   unchanged signed-byte replay, not a re-framing parser. Item 3
   (DSKS) is genuinely present and exercised (A3/A4). The plan is
   frozen at `5188e7a` and nothing in it is edited; this entry records
   the gap between its sentence and the models. The corresponding
   narrowing in the headers is the BOUNDARY block each correct model
   now carries (review items 1–3). Not a divergence of a registered
   prediction, query or outcome.

## Findings

**F1 — The P1 [model] binding half holds in the hard case.** In
degraded mode with the sole authority channel compromised, under an
adversary that alters any bytes after issue, holds every key it uses
and has the D-4 DSKS capability, framed bytes accepted under an honest
issuer's key are exactly the bytes that issuer signed at an issuance
event (Q2(i), `sp1_q2_degraded_compromised.out:173`). Strict mode
(Q1) holds the same headline and, in addition, the unrestricted form:
every acceptance is under a key whose holder signed the accepted bytes
(`sp1_q1_*.out:201`), because the honest channel pins `t` to an honest
manifest and `fp` pins `kX` to an honest key before the frame is
inspected. *Amended 2026-09-06 (cross-family review item 10): this
read "inferred from S-P3 F1; not ablated in S-P1 — the probes ran on
the Q2 form only". The S-P1 probes still run on the Q2 form only, but
the review's mutants ablate the Q1 form directly, so the dependency is
now observed: (i) is red on removing the honest evidence check
(`m_D_evR.out:349`), its key or digest equality, the fingerprint match
(`m_D_fp.out:362`) or the manifest destructuring
(`m_D_tuple_binding.out:387`) — the last of which the headers had
omitted — and green when only the evidence domain tag is unbound
(`m_D_evR_tag.out:201`). See "The cross-family review's single-removal
matrix" below.* The first link itself is still consumed, not
re-established here (ledger entry 2).

**F2 — The load is the attestation-signature check, resting on
signature unforgeability — as the plan predicted, and unlike S-P3 (its
F5).** Two probes on the Q2 form (`proverif/probes/`, unregistered,
discharging nothing): removing `let (=BYTES, =fb) = checksign(sg, kX)`
makes the headline **false** (`probes/p6_no_attestation_sig.out:314`);
keeping every check but running against a library copy in which
`checksign` returns the message under *any* public key (total
exclusive-ownership / unforgeability failure —
`probes/lib_total_eo_failure.pvl`) makes the headline **false**
(`probes/p7_total_eo_failure.out:332`; the derivation at `:171` has no
`IssuerSigned` in its hypothesis at all — the adversary signs a frame
naming the honest fingerprint under a key of its own and the honest
key "verifies" it). S-P3 F5 ran the same total-failure theory and its
re-attribution results held; S-P1's headline does not. The two models
locate their load on different idealizations: S-P3 on `fp`
injectivity, S-P1 on signature unforgeability. Both are Layer 2 in the
library header; the capstone must carry both.

**F3 — Every other verifier check is carried, not load-bearing, for
the headline.** Probes p1–p5 remove, one at a time, the fingerprint
match (`p1_no_fp_check.out:171`), the possession check
(`p2_no_possession.out:171`), the manifest-hash check
(`p3_no_manifest_hash.out:171`), the three pattern pins `=alg`, `=id`,
`=fp(kX)` — the pattern reads every field and pins none
(`p4_frame_unpinned.out:173`; with p3, that is all four P3 in-bytes
bindings, the manifest hash being the separate `if mh = h(t)` at Q2
line 180, not a pattern pin) — and
the sole-channel evidence check (`p5_no_authority_evidence.out:170`);
the headline stays **true** in each, and N1 stays reachable. So the
header's "carried, not exercised here" list (registered in
`PREDICTIONS.md` before any run) is confirmed from the runs, not
assumed: fingerprint match and manifest hash (S-P3), possession over
the manifest (A1.5/P10), the authority-evidence check (inert here by
construction, S-P3 F6), and the frame's `=alg`, `=id`, `=fp(kX)`
pins. None of these defends P1's binding half; the signature does.

**F4 — In companion A, the manifest-pinned fields survive the
signature bug; the unpinned ones do not.** Q3's trace
(`sp1_q3_companionA_sig_unbound.out:171`, reconstructed at 330):
issuer 2 is asked to sign payload `a_2` and emits
`IssuerSigned(pk(skI2), framed(OT_ATTEST, algH, issuerId2, fp(pk(skI2)),
h(m2), canonVerH, a_2))`; the verifier accepts, under `pk(skI2)`,
`framed(a_4, algH, issuerId2, fp(pk(skI2)), h(m2), a_5, a_6)` with
`a_4`, `a_5`, `a_6` fresh attacker names. The registered
trace-inspection rule holds: the accepted frame appears in no
`IssuerSigned` (the only issuance in the trace is over `a_2`). What the
trace also shows is which fields the adversary *could not* alter even
with the signature detached: `alg`, `id`, `fp` and `mh` are pinned by
the frame pattern to the manifest `t`, and `t` is pinned to the honest
issuer's own manifest by possession-over-manifest (D-3: only the honest
key self-signs `m2`, and `fp(kX) = kfpr` forces `kX` honest). So the
P3 field list plus D-3 bound the damage of a detached-signature bug to
object type, canonicalization version and payload. Since the payload is
the attested thing, P1 is still broken by the bug — this is defense in
depth for the *binding fields*, not a mitigation of the integrity
failure, and no claim is made from it beyond the observation. A P8
golden vector for the detached-signature case should exercise the
payload, not a pinned field, or it will pass for the wrong reason.

**F5 — The degraded-mode cost is bounded to the adversary's own key.**
Q2(ii)'s trace (`sp1_q2_degraded_compromised.out:354`, reconstructed
at 498) is impersonation: a key `k` the adversary holds, a manifest
naming `fp(pk(k))`, evidence signed with the public `skS`, possession
and attestation self-signed under `k`. No honest key appears. Q2(i)
true in the same model says an honest key cannot be made to vouch for
bytes it did not sign, altered or fresh, however the channel is
compromised (`PREDICTIONS.md`, "Relying-party consequence"). Under
Amendment 4 §A4.6 this is the registered cost of degradation, to be
stated in the relying-party story, provided the verdict says it is
degraded — which is P4's join (ledger entry 3), not this model's.

**F6 — Companion B alters exactly the two fields S-P3 F7 found
bound-but-unchecked.** Q4's trace
(`sp1_q4_companionB_frame_unsigned.out:171`, reconstructed at 327): the
issuer signs `(BYTES, a_2)` — the payload alone — and the verifier
accepts `framed(a_4, algH, issuerId2, fp(pk(skI2)), h(m2), a_5, a_2)`:
object type and canonicalization version altered, payload intact. The
plan's 0.10 "companion that could not fail" branch (only if the
verifier diverged from S-P3's, whose line 108 leaves `ot` and `cv`
unpinned) did not fire; the reused verifier is the S-P3 verifier line
for line in its checks (Q2 lines 171–180 against
`sp3_q2_degraded_compromised.pv` lines 101–109, with the possession
and acceptance reports to S-P3's `PossJudge` dropped, since S-P1
registers no possession query). Whether the object-type field's
integrity is P1's or P7's/P8's remains the contestable placement the
plan recorded; the run does not settle it.

**F7 — The judge encoding worked first time; no recut.** The
registered judge (judge H keyed on honest keys via a replicated
private output of each honest key; judge N1 keyed on honest `(key,
bytes)` reports; report outputs parallel with continuations) produced
proofs whose derivations name `IssuerSigned` for both honest keys
(`sp1_q2_*.out:171–172`, `sp1_q1_*.out:206–207`) — so Q2(i)/Q1(ii)
are proofs of a correspondence over reachable acceptances, not
vacuous truths — and reconstructed every red trace on the first
attempt. S-P3's recut-1 lesson (parallel report outputs) was applied
from the start; nothing here needed it tested again.

## Load-bearing / carried, from ablation (probes, unregistered)

| Probe (`proverif/probes/`) | Mutation of the Q2 form | Headline (i) | N1 | Reading |
|---|---|---|---|---|
| p1 | remove `if fp(kX) = kfpr` | true (`:171`) | reachable | carried |
| p2 | remove `let (=POSS, =t) = checksign(ppf, kX)` | true (`:171`) | reachable | carried |
| p3 | remove `if mh = h(t)` | true (`:171`) | reachable | carried |
| p4 | frame pattern pins nothing | true (`:173`) | reachable | carried |
| p5 | remove sole-channel evidence check | true (`:170`) | reachable | carried (inert, S-P3 F6) |
| p6 | remove `let (=BYTES, =fb) = checksign(sg, kX)` | **false** (`:314`) | reachable | **load-bearing** |
| p7 | unchanged model; library with total exclusive-ownership failure | **false** (`:332`) | reachable | **load rests on signature unforgeability** |

`probes/probes.log` records rc and box (30 min each) for the original
hand-run pass, which carried no timing field; the seven probes were
re-run 2026-09-06 through the archived wrapper `probes/run-probes.sh`
(same `timeout` + `date +%s` pattern as `run-ladder.sh`), which
appended rc, seconds and box to the log — all seven ≤ 1 s — and every
probe `.out` was byte-identical to the original. p7's
first attempt failed to build (a missing period in the edited `reduc`,
rc = 2) and was fixed; the log says so. The probes are the S-P1
analogue of S-P3's blind-review mutations, run by the collaborator, so
they do not count as review (cross-family falsification was NOT RUN
when this paragraph was written; it has since been run — see the
review log and the matrix below).
Re-run a third time 2026-09-06 (skeptic pass 2) after each probe's
banner line 2 was extended to say that the Q2 header it copies
describes Q2, not the probe (comment-only, line count preserved); all
seven `.out` byte-identical again (`probes.log`).

### The cross-family review's single-removal matrix (2026-09-06, review items 4, 5, 10)

The falsification reviewer built 66 single-check mutants — 22 of each
correct model — and ran them. The `.pv` files are archived under
`proverif/falsification-2026-09-06/scratch/`; the `.out` files were
not archived, and the collaborator regenerated all of them on
2026-09-06 (review log), reproducing every RESULT line the review
quotes, line number included. Three things came out of it that the
probes could not.

1. **On the Q2 form the matrix agrees with p1–p7 exactly**: the
   headline stays true under every single removal except the
   attestation-signature check (`m_G_signature.out:314`) and its byte
   (`m_G_sig_bytes.out:331`) and key (`m_G_sig_key.out:338`)
   equalities; the unrestricted query was already red. Nothing in the
   Q2 header named an inert check load-bearing, so nothing there was
   narrowed.
2. **On the Q1 form the strict headers were narrowed** (item 10). The
   unrestricted query (i) is **false** on removing the honest
   channel's evidence check (`m_D_evR.out:349`), its key equality
   (`m_D_evR_key.out:366`), its digest equality
   (`m_D_evR_digest.out:357`), the fingerprint match
   (`m_D_fp.out:362`) or the **manifest destructuring**
   (`m_D_tuple_binding.out:387`) — and **true** when only the evidence
   domain tag is unbound (`m_D_evR_tag.out:201`). The manifest
   destructuring was missing from the headers' load-bearing list
   altogether, and the fingerprint dependency was inferred from S-P3
   F1 rather than observed; both are now stated as observed. The
   repository variant mirrors it with `m_R_evD*` (F1's reversal holds
   empirically as well as by symmetry).
3. **The honest channel's evidence check is individually inert for
   the headline** (`m_D_evR.out:356`, true) and individually
   load-bearing for (i); only its **domain tag** is inert for both,
   because the key and digest equalities carry the relation on their
   own (item 5). Recorded as defence in depth, the same shape as
   S-P3 F5 — not as a removable check.

**The caution the reviewer presses, adopted (item 4).** "Inert" here
means *these three registered queries do not change*. It does not mean
removable: each row is a single removal, and no set of them licenses a
joint removal; inertness also flips under composition (the domain
tag's work is cross-protocol, invisible to any one family). And most
of these checks are inert *for S-P1's queries* precisely because they
exist for another property's — which is why the verifier is left
whole.

## Ledger entries (A3.3 conservation fields) — offered, not entered

1. **Key binding — complementary to S-P3's ledger entry 1, not
   consumed** (ENUMERATION amendment note 6 item 1; `PREDICTIONS.md`
   ledger entry 1). Producer of the other axis:
   `sp3_q2_degraded_compromised.pv`, `Reattributed` unreachable. S-P3:
   honest bytes ⇒ the signer's key. S-P1: honest key ⇒ the bytes that
   key signed (Q2(i)). Shared terms: accepted key, framed bytes — the
   same `framed(…)` constructor, copied verbatim (library header: NOT
   promoted). Adversary at the join: A1.3 with D-4, sole channel
   compromised. **No severing companion fails an S-P1 query** (judge H
   is keyed on honest keys and is blind to honest bytes accepted under
   an adversary key by construction), so this is not an A3.3
   cross-model entry and none is claimed. The two are composed at the
   capstone, which must carry both queries. Residual Layer 2: `fp`
   collision resistance and what is fingerprinted (P8); `h`
   idealization for the manifest hash.
2. **First link (strict mode only) — consumed from the spike
   (`formal/spike/first-link/`, ledger entry 1) as re-established by
   S-P3 Q1.** Assumed fact: strict acceptance implies an uncompromised
   channel published the accepted tuple (A1.3 "never all", n = 2
   enumerated, not generalized). Used by Q1(i) only (F1); Q2 consumes
   nothing from it (the sole channel key is public, S-P3 F6, probe
   p5). Shared term: the manifest `t`. Severing companion: the
   spike's / S-P3's, not S-P1's. Residual: as recorded there.
   *Skeptic pass 2, 2026-09-06 — A3.3 fields added (Amendment 3
   lines 233–239: "producer module AND event/query"; cross-model
   entries also "broken mutation and expected failing query"); the
   text above is kept as first offered.* **Consumer query:** Q1(i)
   `Accept ⟹ IssuerSigned` (`sp1_q1_strict_dns_compromised.pv:145–146`;
   the repo variant, same lines), RESULT true at `sp1_q1_*.out:201`.
   **Producer module and query:** S-P3 Q1(ii), the first-link
   correspondence `Accept ⟹ (AuthorityPublishedDNS ∨
   AuthorityPublishedRepo) ∧ IssuerPossession ∧ IssuerSigned` —
   `formal/suite/s-p3/proverif/sp3_q1_strict_dns_compromised.pv:91–96`
   and `sp3_q1_strict_repo_compromised.pv:91–96`, RESULT `is true` at
   `sp3_q1_strict_dns_compromised.out:424` and
   `sp3_q1_strict_repo_compromised.out:424`; originally the spike's
   Q1/Q3 chain correspondence, `formal/spike/first-link/RESULTS.md`
   ledger entry 1 (with its 2026-08-12 documentation correction: n = 2
   is finite enumeration). **Adversary at the join:** A1.3 items 1–6
   with D-4, one of two channel keys public (both variants run;
   `sp1_q1_strict_dns_compromised.pv:208` / `…repo…pv:208`).
   **Cross-model fields — an unrun, labelled prediction, not
   evidence:** broken mutation: both channel keys public in the Q1
   form (`out(c, skD); out(c, skR)` in place of the single leak at
   line 208); expected failing query: Q1(i) `Accept ⟹ IssuerSigned`,
   red via impersonation under the adversary's own key (the Q2(ii)
   trace shape, `sp1_q2_*.out:354`), with the headline Q1(ii)
   expected to stay green and N1 reachable. **Not run** (the skeptic's
   fix said "run nothing"); nothing is claimed from it. If run, it is
   an unregistered probe on the Q1 form, to be logged beside p1–p7.
   **Residual Layer 2, made explicit:** `h` idealization (evidence
   binds `h(t)`; concrete-digest collision resistance, spike ledger
   entry 1); `fp` collision resistance (entry 1 above); n = 2
   enumerated, not generalized (A1.3 item 6).
3. **Cross-formalism join — `Accept`/`AcceptS` ↔ P4 verdict partition
   (not symbolically dischargeable).** Assumed fact: every symbolic
   path that stops short of the acceptance event lands in `INVALID` or
   `UNVERIFIABLE` in P4's model, never in a valid verdict; `Accept`
   (strict) / `AcceptS` (degraded) correspond to `VALID_STRICT` /
   `VALID_DEGRADED`, the latter only under an explicit recorded waiver.
   Producer: `formal/tla/P4_VerifierStates.tla`, invariants named in
   `PREDICTIONS.md` Target. Shared term: the acceptance predicate.
   Carried in the written proof and `formal/COVERAGE-MAP.md` row 1;
   **never marked discharged by any symbolic query** (ENUMERATION §4).
   F5 depends on this join for its "provided the verdict says it is
   degraded". *Skeptic pass 2, 2026-09-06 — two A3.3 fields added; text
   above kept as first offered.* **Adversary at the join:** A1.3
   items 1–6 with D-4, both modes (strict: one of two channel keys
   public; degraded: the sole channel key public). **Residual:** the
   `Accept`/`AcceptS` ↔ P4 acceptance-predicate mapping is prose
   (A3.3 standing rule, ENUMERATION §4), never symbolic; it is a
   cross-formalism correspondence carried in the written proof and
   `formal/COVERAGE-MAP.md` row 1, not a Layer 2 cryptographic
   assumption, and no query on either side discharges it.
4. **Integrity / authorship correspondence — PRODUCER (Q2(i),
   `AcceptedUnderHonestKey ⟹ IssuerSigned`, `sp1_q2_*.out:173`).**
   Consumers: S-P2 (each accepted signature covers the exact framed
   bytes); S-P7 (a wrapper's commitment to the inner package's exact
   bytes presupposes accepted bytes = signed bytes for the inner
   signature); the capstone's last link ("accepted signature verifying
   under that key → the exact framed bytes", §A3.2 chain); the
   relying-party story's can-establish line. Shared terms: accepted
   key, framed bytes. Adversary at the join: A1.3 items 1–6 with D-4,
   sole channel compromised. Severing companion: Q3
   (`sp1_q3_companionA_sig_unbound.pv`, signature unbound from
   presented bytes) → headline red (`.out:331`). Residual Layer 2:
   **signature unforgeability** (Dolev–Yao; confirmed as the load by
   probes p6/p7 — F2; the verification profile is P3's [assumption]
   half, H1a); deterministic signatures (the judge equates more than a
   byte-level judge — conservative); **canonical encoding — P8's
   injectivity obligation** (term equality stands in for canonical-byte
   equality until P8's proof exists; then this entry cites the proof,
   never silently absorbs it); `h` idealization; frame layout (P8);
   implementation fidelity.

5. **Key-use discipline — a named assumption, not a cross-model
   obligation (entered 2026-09-06 from the cross-family review, item
   8).** **Consumer property/query:** P1 [model] binding, every S-P1
   correspondence — Q1(i)/(ii) and Q2(i) alike, since each reads
   "signed at an issuance event" off the fact that the only signatures
   an honest issuer key ever makes are the ones this fixture's
   `Issuer` makes. **Assumed fact:** an issuer key signs only framed
   objects under the `BYTES` domain tag (and its own manifest under
   `POSS`) — never a raw payload, never bytes of another shape, at any
   endpoint anywhere in the system. This is the P7 domain-separation
   design stated as an obligation on issuer *code*, outside every
   symbolic model. **Producer module and event/query: none — Layer 2 /
   implementation fidelity, unclaimed.** No symbolic model in this
   suite quantifies over the endpoints that hold an issuer key; the
   fixture's producer set is closed by construction, which is exactly
   what the assumption makes explicit. **Shared term:** the honest
   issuer key `pk(skI)`/`pk(skI2)` and the `IssuerSigned` event that
   records what it signed. **Adversary at the join:** A1.3 items 1–6
   with D-4; the adversary chooses the message handed to any signing
   endpoint (chosen-message issuer, already the fixture's shape).
   **Evidence that the assumption is load-bearing (severing witness,
   run by the reviewer and reproduced here):** add a second honest
   endpoint under the same key that signs a payload-only message, ask
   it to sign a complete attacker-chosen inner frame *as payload*, and
   replay that signature to the unchanged Q2 verifier. The verifier
   accepts the inner frame with no matching issuance event —
   `RESULT event(AcceptedUnderHonestKey(k,fb_5)) ==> event(IssuerSigned(k,fb_5)) is false.`
   (`falsification-2026-09-06/scratch/a8_cross_broken_endpoint.pv`,
   `.out:428`; the attack judge at `.out:948`). The reviewer is
   explicit, and it is worth repeating, that **the added endpoint is
   broken by construction and the committed fixture is not falsified**:
   what fails is unrestricted *composition* of the correspondence, not
   the model. No query changes.
   **The H1a red-bar vector this obligation buys:** a conformance
   vector in which an issuing endpoint is asked to sign unframed bytes
   under an issuer key — the reference issuer must **refuse**; an
   implementation that signs it is non-conforming, and the red bar is
   how the assumption is discharged outside the symbolic layer, since
   nothing inside it can. **Residual Layer 2:** implementation
   fidelity (the whole of it — this assumption is a statement about
   code, not about cryptography); and, for any deployment that reuses
   an issuer key across protocols, cross-protocol domain separation,
   whose symbolic work is invisible to any single-family model (the
   library's D-6 note, S-STANDING review item 27, same shape).

Layer 2 residuals exposed, collected: signature unforgeability and the
verification profile (H1a) — the load; canonical encoding / framing
injectivity (P8, pre-proof); concrete hash collision resistance
(manifest hash) and fingerprint collision resistance (via entry 1) —
carried, not load-bearing here; implementation fidelity — including
**key-use discipline** (entry 5), which is the sharpest form
implementation fidelity takes in this family. Enumerated, exposed,
unclaimed.

## What S-P1 does not discharge

- The verdict partition, or anything about `INVALID`/`UNVERIFIABLE`
  (P4; ledger entry 3).
- Freshness, uniqueness, or context of an acceptance — replay is
  permitted (§A3.1 item 1); every correspondence is non-injective by
  registration.
- That the accepted key belongs to an honest issuer in
  degraded-compromised mode — reachable by construction (Q2(ii), F5).
- Re-attribution of honest bytes to another key — S-P3's (entry 1).
- Multi-signer completeness — S-P2's.
- That `framed(…)` is the P8 frame, or anything about byte layout or
  encoding ambiguity — P8's.
- Cross-type confusion or wrapper re-serialization — P7's (Q4 alters
  the object-type field without interpreting it).
- Whether the object-type and canonicalization-version fields' integrity
  is P1's or P7/P8's — contestable placement, recorded in the plan (Q4)
  and unchanged by the run (F6).
- Coverage of every branch, key or payload shape. N1 is reachable in
  all five models and every committed witness trace uses `skI2`; the
  query is existential, so it rules out a vacuous model and nothing
  more (cross-family review item 6, recorded for the suite; the rule's
  home is `ENUMERATION.md`, outside this directory and not amended
  here).
- Anything temporal — P5/P6.

## Status toward discharge (PROPERTIES.md line 12 terms)

Tool passes: **yes** — all three correct-model runs (Q1 both
variants, Q2) green on every registered
query (Q2(ii) red as registered), both companions red on exactly the
headline with N1 reachable. Falsification review by a non-author model
of a different family (ENUMERATION note 5 item 1): **RUN 2026-09-06**
— Codex `gpt-6-astra`, 83 scratch models, archived under
`proverif/falsification-2026-09-06/`; the review is
`docs/reviews/2026-09-06-codex-suite-falsification-s-p1-s-p2-s-p7-s-standing.md`.
Its outcome for this family: **no registered query, prediction or
result changed** — the reviewer reproduced every committed RESULT line
before mutating — and **the self-description did not survive**: items
7, 10 and 5 narrowed header sentences, item 8 put a named assumption
in the ledger (entry 5), item 9 recorded a divergence between the
frozen plan's adversary sentence and the models, item 11 recorded an
inconclusive probe, and items 1–3 fixed three boundaries that cannot
be posed in this family at all. All eleven are Accepted, Boundary or
Recorded; **none is routed** (the three routed questions, C8–C10, are
other families'). The dispositions and the text they produced are the
collaborator's and carry no authority until the author reads them
(ROUTED C5 covers that read). Author
read: **pending** — the read this file asks for is
`sp1_q2_degraded_compromised.pv` lines 18–56 (the header, which the
2026-09-06 review narrowed in place) and 168–182
(the verifier) against P1's registered sentence and §A3.1 item 2, one
question: does the header say what that verifier does, no more? (Per
the standing rule, that is the only read requested.) Per
`PREDICTIONS.md` disposition B2, P1 → `checked` needs (a) this ladder,
(b) P4 `checked` (already), and (c) the `Accept` ↔ P4 join written in
the coverage map; `discharged` adds the cross-family review and the
author's read. The row move is the author's commit. One correction
announced by `PREDICTIONS.md` disposition B3 is **not yet made**:
`formal/COVERAGE-MAP.md` row 1 (unmodified since `5188e7a`) still
reads "none — S-P1 enumerated (ENUM §2), not built" in the symbolic-leg
cell and "Consumes SP3 ledger entry 1 (key binding)" in the join cell;
both are contradicted by this record (five models built and run;
ledger entry 1 above, complementary not consumed). The pending change
is a dated PROPOSED amendment note on the map (amend-don't-rewrite),
outside this directory; it is named here so the gap is visible until
it is made.

Pending author ruling (ROUTED C8/C9/C10): **none applies to S-P1** —
C8 is S-P2's common-content question, C9 S-P7's wrapper version
record, C10 S-STANDING's tuple-to-core binding
(`formal/suite/ROUTED-2026-09-06.md` lines 307, 316, 323); no ruling
on any of the three would change an S-P1 header, query, result or
ledger entry. *(Added 2026-09-06 so the line the cross-family work
order named is present and grep-able in this family too; the same
statement already stood in the review log below and in
`READING-AIDS.md` §8, which are left as written.)*

## Review log

- 2026-09-06 — models written by the AI collaborator from the frozen
  plan (`5188e7a`), S-P3's Q1/Q2 verifiers and the recut-3 idioms, and
  the library with D-5/D-6. Ladder run 1: Q1 (both), Q2, Q4 as
  predicted; Q3 rc = 2 (type annotation). Build fix; ladder run 2: all
  five as predicted; `run1/` archived. Seven ablation probes run on the
  Q2 form (p1–p7); load located on the attestation-signature check and
  signature unforgeability. No author read; no non-author review.
- 2026-09-06 — skeptic pass on S-P1 (AI reviewer; findings verified
  against the `.out` files by the AI collaborator). Two defects: (1)
  `sp1_q3_companionA_sig_unbound.pv` header lines 33–34 said "only the
  payload differs", contradicted by its own `.out:171`/`:330` (object
  type, canonicalization version and payload differ); corrected with
  a dated note at the end of the file, header line count preserved so
  READING-AIDS.md citations hold; the whole ladder re-run twice (runs
  3 and 4, `ladder.log`), all five `.out` byte-identical to run 2. (2)
  The COVERAGE-MAP.md row-1 correction that B3 announces was never
  made — recorded above under "Status toward discharge" as pending;
  the map is outside this directory and is not amended here. Nits
  applied: stray duplicated fragment on the Q3 header line 30 removed;
  F3 and READING-AIDS §1b row 120 now attribute three pattern pins to
  p4 and the manifest-hash binding to p3; probes re-run through the
  new `probes/run-probes.sh` so `probes.log` carries seconds (all
  `.out` byte-identical); "both correct models" → "all three
  correct-model runs"; divergences note 3 records the companions'
  unregistered third query. No result changed; no PREDICTIONS.md text
  touched. Falsification review remains NOT RUN; author read pending.
- 2026-09-06 — skeptic pass 2 on S-P1 (AI reviewer; each finding
  verified against the record by the AI collaborator before applying).
  Two defects: (1) ledger entry 2 named no producer query or evidence
  and its cross-model fields pointed at another model's companion;
  entry 3 had no adversary-at-the-join and no residual field
  (Amendment 3 §A3.3 lines 233–239) — both amended above with dated
  additions, the original text kept; entry 2's cross-model fields are
  recorded as an unrun, labelled prediction, not run. (2)
  `READING-AIDS.md`'s preamble claimed every LOAD-BEARING / CARRIED
  label came from S-P1's own runs, but the domain-tag label rests on
  S-P3 F7 alone and the Q1 strict-only rows are inferred from S-P3 F1
  (no probe touches a tag or the Q1 form) — preamble and §1b amended
  there. Nits: the Q2 header's "Confirmed by the S-P1 probes" (lines
  37–39) predates the probes by mtime (Q2 `.pv` 18:26:57; probes
  18:29–18:41; the probe files are byte-copies of Q2 plus a banner) —
  a dated provenance note is appended at the end of the file, header
  line count preserved; the whole ladder re-run (run 5, `ladder.log`),
  all five `.out` byte-identical to run 4. Each probe's banner line 2
  now says the copied Q2 header describes Q2, not the probe; probes
  re-run through `run-probes.sh`, all seven `.out` byte-identical.
  "committed `.out`" → "working-tree `.out`, uncommitted" (ladder
  table header; READING-AIDS review log — the only two occurrences;
  the "Companion isolation" paragraph the finding also named does not
  contain the word). F1 now says the strict-mode pinning mechanism is
  inferred from S-P3 F1, not ablated in S-P1. The three logs
  (`ladder.log`, `run1/ladder.log`, `probes/probes.log`) carry the
  PROPOSED label line with a dated note; both run scripts emit it when
  a log is first created. No result changed; no `PREDICTIONS.md` text
  touched. Falsification review remains NOT RUN; author read pending.
- 2026-09-06 — **cross-family falsification review applied** (the
  agreement gate of `ENUMERATION.md` amendment note 5 item 1).
  Reviewer: Codex CLI, model `gpt-6-astra`, jailed to this family's
  files plus the shared library, the registered property text, §A1.3
  and the frozen plan; it ran ProVerif on its own mutants and attack
  fixtures (83 scratch models). Review:
  `docs/reviews/2026-09-06-codex-suite-falsification-s-p1-s-p2-s-p7-s-standing.md`
  (consolidated items 1–29; items 1–6 common, 7–11 S-P1). Archive:
  `proverif/falsification-2026-09-06/` — the review, the prompt, the
  model line, and 75 `.pv` files under `scratch/`.
  **Nothing changed in any model's checks, queries, fixtures or
  results.** Every change below is header, results or reading-aid text.

  *Reproduction first.* All 75 archived `.pv` files were re-run by the
  collaborator (`proverif -lib ../../lib/tessera_theory.pvl`, outside
  the repository since the reviewer's `.out` files are deliberately not
  archived); all 75 terminated rc = 0, and **every RESULT line the
  review quotes was reproduced, line number included** — the 66
  mutants' H/U/N matrix exactly as tabulated, and the attacks A1
  (`:582` true), A2 (`:583` true), A3 (`:585` true), A4 (`:783`
  false), A5 (`:689` `cannot be proved`), A6 (`:747` false), A7
  (`:747` false), A8 (`:428` headline false, `:948` attack false). No
  `.out` file was added to the repository; the archive note explains
  why they are regenerable rather than stored.

  *Items applied.* **1–3 (Boundary):** each correct model's header
  gains a dated BOUNDARY block, and READING-AIDS §1d/§2d gain
  plain-language paragraphs, saying that signature-set operations
  (A1.3 item 2 — one signature slot; S-P2's subject), byte-encoding
  attacks (term equality standing in for byte equality — P8's
  injectivity obligation, Layer 2; the reviewer's "a coverage failure,
  not an unreachable attack" is adopted verbatim) and verdicts,
  waivers and policy inputs (P4's partition, ledger entry 3) cannot be
  posed in this family at all. **4 (Accepted):** no S-P1 header named
  an inert check load-bearing, so nothing was reworded on that count;
  the Q2 header gains a RECORDED block and this file a new section,
  "The cross-family review's single-removal matrix", carrying the
  reviewer's two cautions — single removals license neither joint
  removal nor "inert for the verifier". **5 (Accepted / Recorded):**
  the strict headers now say the honest channel's evidence check is
  individually inert for the headline and load-bearing for (i), with
  only its domain tag inert for both because the key and digest
  equalities carry it; recorded as defence in depth (S-P3 F5 shape).
  **7 (Accepted):** "Carried checks" in all three correct models
  listed "object type (P7); canonicalization version and algorithm
  profile (P8/H1a)" as *checks*; there are none — `ot` and `cv` are
  bound by the frame pattern and never compared, and the reviewer's A6
  replays a wrapper-typed frame under a foreign version into the Q2
  verifier and it is accepted (`a6_foreign_type.out:747`). Reworded as
  **signed fields carried as obligations** for P7 and P8/H1a. **8
  (Recorded → ledger):** ledger entry 5, *key-use discipline*, with
  its A3.3 fields, the A8 severing witness, and the H1a red-bar vector
  (an endpoint asked to sign unframed bytes under an issuer key must
  be refused by the reference issuer). Not a query change; the added
  endpoint is broken by construction and the fixture is not falsified.
  **9 (Accepted):** divergence note 4 above records that the frozen
  plan's "items 2–6 are present" overstates for A1.3 items 2 and 5;
  `PREDICTIONS.md` is frozen and untouched. **10 (Accepted):** the
  strict headers' load-bearing list for (i) gains the
  manifest-destructuring dependency it omitted and states the
  fingerprint dependency as observed rather than inferred, citing the
  matrix; F1 and READING-AIDS §2b are amended to match, and §2b gains
  a row for line 181. **11 (Recorded):** the Q2 header records that
  A5 returned `cannot be proved` — inconclusive, and injectivity is
  not a registered requirement (§A3.1 registers the non-injective
  form). **6 (Recorded):** N1 is a vacuity guard, not coverage —
  entered under "What S-P1 does not discharge" and in READING-AIDS
  §0.2; the suite-wide home for that rule is `ENUMERATION.md`, outside
  this directory and **not** amended here.

  *No "Pending author ruling" line is added.* The three ROUTED items
  (C8/C9/C10, review items 12, 18, 23) belong to S-P2, S-P7 and
  S-STANDING; none is S-P1's, so there is nothing here awaiting a
  ruling beyond the standing ROUTED C5 read of the narrowed headers,
  which "Status toward discharge" already names. *(Superseded in form,
  not in substance, 2026-09-06, skeptic pass 3: the literal line the
  work order named **was** added under "Status toward discharge" so a
  cross-family grep finds it in all four families; it states exactly
  what this paragraph states — none of C8/C9/C10 is S-P1's. This
  paragraph is left as written.)*

  *Mechanism note, and the one regression this pass repaired.* The
  header narrowings were written **in place** (permitted: these `.pv`
  files are uncommitted drafts), which grew each Q1 header from 63
  lines to 129 and the Q2 header from 65 to 124, moving every body
  line by +66 and +59. That silently invalidated every `.pv` line
  citation in this file and in `READING-AIDS.md`. All of them have
  been converted, each one checked against the file it cites, and each
  edited model now ends with a dated LINE-COUNT NOTE giving the
  old → new mapping, so the reviewer's own `D:nn`/`R:nn`/`G:nn`
  citations (left as received, in the pre-review numbering) and the
  archived mutants remain readable. The seven probe copies under
  `probes/` carry the pre-review Q2 header by construction and were
  deliberately **not** re-cut: their `.out` files are the evidence this
  file cites. Ladder run 7 (`ladder.log`) re-ran all five models after
  the LINE-COUNT NOTES; all five `.out` byte-identical to run 6, whose
  own `.out` files were independently re-verified byte-identical at
  the start of this pass. Ladder run 6 is the run that carried the
  in-place header narrowings; both runs are comment-only, no encoding
  change.

  *Not applied, deliberately.* Nothing in `PREDICTIONS.md` (frozen).
  Nothing in `formal/COVERAGE-MAP.md` (outside this directory; the B3
  correction it still owes is named under "Status toward discharge").
  Nothing in `ENUMERATION.md` (the suite rule item 6 belongs in). No
  other family's directory. Review item 7 applies verbatim to S-P3's
  eight headers, which are committed and already reviewed; a one-line
  pointer was added to `formal/suite/s-p3/RESULTS.md`'s review log
  instead, deferring the wording fix to S-P3's next recut.
  Author read: **pending**.
- 2026-09-06 — skeptic pass 3 on S-P1 (AI reviewer of the
  cross-family-review application; each finding verified against the
  record by the AI collaborator before applying). One defect: the
  file's own status block (lines 10–11) still read "Falsification
  review: **NOT RUN**" after the cross-family review had been applied
  and recorded twice inside this file ("Status toward discharge" and
  the review log) — amended in place above, dated, original quoted.
  The two earlier passes' log entries that end "Falsification review
  remains NOT RUN" are dated records of their own moment and were left
  as written; `RESULTS.md` line 263 was already amended in the
  previous pass. Nits applied: the preamble's re-run narrative, which
  stopped at run 5, now carries runs 6 and 7 so its warrant ("all five
  `.out` byte-identical to run 2, so run 2's line citations stand")
  covers the pass that moved every `.pv` body line; a grep-able
  "Pending author ruling (ROUTED C8/C9/C10)" line was added under
  "Status toward discharge" recording that none of the three applies
  to S-P1 (the previous pass's "*No 'Pending author ruling' line is
  added*" paragraph is left as written and carries a dated note that
  the line was subsequently added in form, not in substance;
  `READING-AIDS.md` §8 is unchanged); `READING-AIDS.md` line 25 now
  attributes the sibling `.out` files to ladder run 7 (byte-identical
  to run 2, whose numbers it cites) rather than to run 2, which
  `proverif/ladder.log` does not name as current; and
  `READING-AIDS.md` §7's "every `.pv` line number in this document was
  converted" is qualified to the body, with the mapping for the
  numbers its own dated log entries keep (old §1b row 120 → 179; old
  §2b rows 113/114/116 → 179/180/182). The skeptic-pass-1 entry above
  ("READING-AIDS §1b row 120") is a dated record and was **not**
  touched. Independent re-verification this pass: all five models
  re-run with `proverif -lib formal/suite/lib/tessera_theory.pvl`, every
  `.out` byte-identical to the working tree; `run1/*.out` byte-identical
  for Q1d, Q1r, Q2 and Q4 (Q3 differs only because run 1 was the rc = 2
  build failure). No `.pv` file was changed, so no re-run was owed; no
  result, no registered query text and no `PREDICTIONS.md` text
  touched; no ROUTED item applied. Author read: **pending**.

## Author read — 2026-09-12 (ROUTED C5; entered by the AI collaborator in the author's words)

The author read the Q2 claim block (lines 18–73) against P1's operative
form via `formal/suite/READ-C5-2026-09-12.md` and returned **one NO**:
line 28, "in degraded-compromised mode it is not", is too strong —
*"honest key acceptance is also reachable as the model explicitly checks
this case."* Verified: N1 `HonestAccepted` reachable, `.out:396`. Line 28
rewritten in place to "it need not be" with a dated CORRECTION marker
citing the witness; same line count, so every citation in this file and
in `READING-AIDS.md` still resolves. Comment-only: re-run same day, the
`.out` byte-identical to the pre-edit file (`ladder.log`, last line).
No result, query, prediction or ledger entry changed. The frozen draft
header in `PREDICTIONS.md` (line 256) keeps the original wording.
Author read of the Q2 header: **one sentence repaired; the read
otherwise stands as returned** — the row's other prerequisites (B2:
the `Accept` ↔ P4 join written in the coverage map) are unchanged.
