# S-P3 — key binding (anti-DSKS): results

**Status: PROPOSED — collaborator-drafted 2026-09-04 from the committed
`.out` files; nothing here is ratified; the author's cold read of the
correct models precedes any ratification (ENUMERATION §5).** Predictions
were frozen at `fe1517c` before any model existed. This file records
predictions against observed outcomes in the registered three-outcome
vocabulary, the encoding recuts and why, four findings, and the A3.3
ledger entries S-P3 offers the suite. It does not change
`formal/PROPERTIES.md`; P3's tracker row is the author's to move.

Tooling: ProVerif 2.05, `-lib formal/suite/lib/tessera_theory.pvl`.
Models and outputs: `formal/suite/s-p3/proverif/`. Run 1 outputs (before
the recut) and the reconstruction diagnostics: `proverif/run1/`. Every
run terminated in ≤ 1 s against boxes of 15–30 min (`ladder.log`).

## Predictions vs observed

| Query | Registered prediction | Observed (final run) | Outcome |
|---|---|---|---|
| Q1 strict, DNS compromised | both hold (0.7) | `Reattributed` unreachable; `PossessionTransplanted` unreachable; first-link correspondence **true**; `Accept` reachable (N1) | **termination, as predicted** — after one encoding recut (see §Recuts) |
| Q1 strict, repo compromised | both hold (0.7) | identical | **as predicted**, same recut |
| Q2 degraded, sole channel compromised — **the P3 claim** | unreachable (0.6); real attack (0.2); timeout (0.2) | `Reattributed` unreachable; `PossessionTransplanted` unreachable; `AcceptS` reachable | **termination, as predicted** |
| Q3 companion A: frame unbound | red (0.75); recut (0.15) | `Reattributed` **reachable**, trace found | **red as required** — after the same recut; exhibited path is *not* the DSKS route (Finding 2) |
| Q4 companion B: possession unnamed | red (0.7); recut (0.2) | `PossessionTransplanted` **reachable**, trace found, derivation through `dsks`; `Reattributed` stays unreachable | **red as required**, no recut needed; the only query whose red *requires* the DSKS capability |
| Q5 correct, two signers | holds (0.55) | `ReattributedA`, `ReattributedB`, `PossessionTransplanted` all unreachable; `Accept2` reachable | **termination, as predicted** (per-role judges: recut 2) |
| Q5 companion as registered: B's frame omits its fingerprint | red on B only (0.55) | `ReattributedB` **unreachable** | **prediction MISSED** — a companion that could not fail (Finding 3). Nearest registered bucket: "encoding defect" (0.2); it is not an encoding defect but a redundancy in the field list |
| Q5 companion 2 (unregistered, added 2026-09-04): B's frame omits all binding fields | — | `ReattributedB` reachable, `ReattributedA` unreachable | red on exactly B; supplies the negative control the registered companion could not |

N1/N2 (ENUMERATION note 3): every model carries a reachability query on
its acceptance event, all reported reachable; every model carries two
honest issuers (or two honest two-signer manifests) with adversary-chosen
payloads. Neither was spelled out in the frozen plan; both are §5
obligations and were added at model-writing time. Recorded as a plan
omission, not a prediction change: no registered prediction refers to
them.

## Recuts (encoding, not property)

**Recut 1 — asynchronous judge reports (all models).** Run 1 returned
"cannot be proved" on Q1's acceptance witness and on Q3's
`Reattributed`: ProVerif found derivations (goal reachable) but could
not rebuild a trace. Horn-clause results were identical before and after.
Diagnostics (`run1/diagnostics/`, d1–d14): the failure survives a single
issuer (d1, d7), derivation-simplification settings (d2, d3), a
vacuity-only query (d4), a disequality judge (d5), and pattern-free judges
(d10, d11); it disappears when the judges are removed (d6), when the
possession judge alone is removed (d9), and when the report outputs are
placed in parallel with their continuations (d13, d14). Cause: ProVerif's
reconstruction unfolds only the replicated copies its derivation
mentions; a *synchronous* private-channel output that is off the goal
path has no receiver in the reconstructed interleaving and blocks the
trace. The spike's judge pattern had one private output per process and
never hit this. **Suite note:** report outputs to private-channel judges
must be `( out(priv, M) | continuation )`, never sequential. Registered
here for S-P1/S-P2/S-P7 and S-STANDING.

**Recut 2 — per-role judges (Q5 only).** A single `Reattributed` event
cannot state "red on exactly signer B"; the three Q5 models were recut
with `honestChA`/`honestChB` and `ReattributedA`/`ReattributedB`.
Results before the recut (`run1/q5-recut1/`) are consistent with the
per-role results.

**Recut 3 — honest-flow witness, shadowing fix, header narrowing (all
models), 2026-09-05.** After the two blind falsification reviews
(`docs/reviews/2026-09-05-blind-falsification-sp3-q2.md`): (a) the N1
witness is now `HonestAccepted(k, fb)`, emitted by the judge when the
accepted key *is* the signer's — the bare acceptance witness was
satisfiable by impersonation alone; reachable in all eight models;
(b) judge locals renamed so the library's `fbH` is no longer shadowed
(no ProVerif warnings remain); (c) every header's "This model proves"
narrowed to what the queries discharge (F5–F8 below). No result
changed. Run-2 outputs archived under `run2/`.

## Findings

**F1 — The P3 [model] claim holds in the hard case.** In degraded mode
with the sole authority channel compromised, under an adversary that
holds every key it uses *and* can derive a fresh key verifying any one
seen signature, the honest issuer's framed bytes are never accepted
under a key other than the signer's, and an honest possession proof is
never accepted for another key (Q2). The frame's in-bytes binding and
possession-over-manifest are what carry it; strict mode (Q1) is carried
by the cross-channel fingerprint agreement before the frame is even
inspected.

**F2 — Companion A's red is impersonation colliding with honest bytes,
not key substitution.** With no binding fields in the frame, the
adversary's own signature over `framedU(objType, alg, canonVer,
payload)` under its own key is term-equal to the honest issuer's bytes
over the same adversary-chosen payload; the judge fires on that
collision. The DSKS capability was not used. Consequence for the
relying-party story: under the spike's opaque-bytes shape, impersonation
(note 2's admitted degraded-mode cost — adversary-authored bytes
*claiming an honest identity*, under the adversary's own key, accepted
because the sole compromised channel vouches for that key) and
"re-attribution of the honest issuer's bytes" are *the same event*;
the in-bytes binding is what separates them. The story should say so.

**F3 — The P3 field list is redundant, across two Layer-2 assumptions.**
The registered companion for Q5 — B's frame keeps issuer identity and
manifest hash but drops its fingerprint — cannot go red: the manifest
hash pins the tuple, the tuple pins both fingerprints, and the verifier's
slot check `fp(kB) = kfprB` does the rest. In this abstraction the
minimal load-bearing binding is the **manifest hash** (with the tuple's
fingerprint match); issuer identity and fingerprint in the frame add
nothing against re-attribution. They are not useless: the manifest-hash
route rests on `h`'s collision resistance and the fingerprint route on
`fp`'s (both Layer 2, library header); the field list is defense in
depth across two independent hardness assumptions, and a P8 golden
vector should exercise each separately. Recorded as a **prediction
miss** on the registered companion and discharged by an added companion
that removes all three binding fields (red on B only).

**F4 — Where DSKS actually bites.** Of five queries, only Q4's red
*requires* the substitution capability: the honest issuer's own manifest
self-signature, verified under a derived key, is accepted as that key's
possession when the verifier omits the naming check. This is the
concrete mechanism behind ENUMERATION note 2's claim that possession
must be over the manifest *and* checked against the accepted key; the
spike's fingerprint-only possession would fail Q4's correct form
trivially (the adversary signs `(POSS, fp(pk(k')))` with `k'` it holds).
Note also that with the naming check present, DSKS added no attack
anywhere in this ladder — which is the P3 design working, not the
capability being weak: the library's D-4 rule is sufficient to exhibit
the attack when the defence is removed.

**F5 — The result does not depend on signature security; it depends on
fingerprint injectivity.** (Blind review, both reviewers.) Removing the
attestation-signature check, or replacing the library's signature
theory with *total* exclusive-ownership failure (any key verifies any
signature), leaves both Q2 queries unreachable; `dsks` appears nowhere
in the baseline derivation. Two fingerprint-collision theories make one
or both reachable. So the honest sentence for what Q2 discharges is:
*under a perfect fingerprint, key substitution cannot move an
acceptance of honest bytes to another key.* This is a stronger result
than the header first claimed (it holds under a stronger adversary),
and a narrower one (its whole load is the `fp` idealization, Layer 2).
DSKS bites the moment the tuple-fingerprint check is removed, which is
F4 with the load located.

**F6 — The compromised sole channel is the adversary's condition, not
something the checks defend against.** Removing the authority-evidence
check changes nothing, because the channel key is public by
construction. The fixture is strictly stronger than A1.3 item 6 (which
licenses a *proper* subset of channels) in the conservative direction.
Q2's header now says so.

**F7 — Five of P3's seven fields are included but unexercised by these
queries.** Issuer identity, algorithm identifier, object type,
canonicalization version, and the domain tag can be unbound or removed
without changing either result; key fingerprint and (redundantly)
manifest hash are the only load-bearing fields — which sharpens F3.
P3's text requires inclusion; their *checks* belong to other
properties: object type → P7; canonicalization version and algorithm
profile → P8/H1a; algorithm identifier → the A3 §1 identifier-binding
invariant; identity → F8. The attestation-signature check itself is
unexercised by re-attribution and is exercised by an *authorship*
correspondence (accepted under an honest key ⇒ that key signed those
bytes) — S-P1's integrity claim, carried there as a consumer
obligation; Q1's strict-mode first-link correspondence exercises it
already.

**F8 — Key-based judge, identity-based sentence.** Reviewer 1 observed
that P3's opening sentence speaks of *issuer identity* while the judge
compares keys, and exhibited an adversary key accepted under an honest
identity with adversary-authored bytes. Disposition (reasoned in the
review record, item 6): the binding P3 states — signature to the
identity *committed in the signed bytes* — holds in that trace; what
is forged is the identity→key *authority*, which is P10 / the first
link, and in degraded mode with the sole channel compromised is the
registered waiver cost (Q5b). P3's registered threat is re-attribution
of an existing signature. If the author reads P3's sentence more
broadly, that is a ruling on P3's scope, not a model defect. Flagged.

**Dependency statement (both reviewers, consistent):** the frame's
fingerprint field alone suffices against re-attribution; the tuple
fingerprint match and the manifest-hash check together compensate for
its absence, and neither alone does; the tuple fingerprint match and
possession-over-manifest are jointly necessary and individually
insufficient against possession transplant.

## Ledger entries (A3.3 conservation fields) — offered, not entered

1. **Key-binding relation (producer: Q2, `Reattributed` unreachable).**
   Consumer: S-P1, S-P2, S-P7 (each presupposes whose bytes are whose),
   S-STANDING (entitled-key check inside the standing path, ENUMERATION
   note 4). Assumed fact: acceptance of framed bytes under `kX`
   implies the bytes' committed `(issuerId, kfp)` is `(id, fp(kX))`,
   and honest bytes are never accepted under a key other than their
   signer's. Shared terms: accepted key, issuer identity, framed bytes.
   Adversary at the join: A1.3 with item 3 expressible (D-4), sole
   channel compromised, possession free. Severing companion: Q3
   (frame unbound) → `Reattributed` red. Residual Layer 2: `fp`
   collision resistance and what a fingerprint hashes (P8); `h`
   idealization for the manifest hash; deterministic signatures
   (conservative for the judge); frame layout (P8); the verification
   profile (P3's [assumption] half, H1a).
2. **Possession binds the manifest to the named key (producer: Q2/Q4
   correct form, `PossessionTransplanted` unreachable) — an A1.5/P10
   result carried in S-P3** (ENUMERATION §2's "producer for the
   fingerprint relation" scope is wider than P3's registered text;
   blind review item 8).** Consumer:
   S-P2's degraded-mode signer-stripping companion (note 2). Assumed
   fact: an accepted possession proof under `kX` is a signature over
   the accepted manifest, which names `fp(kX)`. Shared terms: accepted
   key, manifest. Adversary at the join: as above. Severing companion:
   Q4 (naming check dropped) → `PossessionTransplanted` red, via
   `dsks`. Residual: as entry 1.
3. **Cross-formalism join (not symbolically dischargeable):** nothing in
   S-P3 assumes anchor validity; no TLA+ join is consumed. Recorded so
   the capstone does not look for one.

### Fingerprint binding — what the record must state (reviewer conclusion, 2026-09-04)

From the Codex review's addendum (`docs/reviews/2026-09-04-codex-sp3-q2-review.md`),
accepted: the fingerprint check is a conjunct, so it cannot enlarge the
set of substitute keys the verifier accepts; what it adds is a second
constraint whose strength is an implementation fact. Four statements
the record owes, each assigned:

1. Exactly what key representation is fingerprinted, with which
   algorithm and parameters — **P8 golden vectors / H1a profile**.
2. That acceptance requires the presented key to match the signed
   fingerprint — **the verifier specification** (modeled here as
   `fp(kX) = kfpr` and the frame's `=fp(kX)`).
3. That the symbolic model assumes distinct keys have distinct
   fingerprints — **library header** (fp idealization), cited by ledger
   entry 1.
4. That the implementation instead depends on the difficulty of finding
   a different key with the target fingerprint, alongside its signature
   and encoding assumptions — **Layer 2 ledger**, H1a evidence.

Constraint on reading F3: "defense in depth across two independent
hardness assumptions" is qualitative. No combined or quantified
security level is claimed or may be derived from it.

## What S-P3 does not discharge

- P3's [assumption] half (verification profile, H1a evidence).
- Anything about impersonation with the adversary's own key over its
  own bytes in degraded mode: reachable by construction, out of scope,
  and — per F2 — indistinguishable from re-attribution only when the
  frame is unbound.
- Frame layout, encoding, or that `framed(...)` is the P8 frame.
- The DSKS capability's practicality against Ed25519; the rule grants
  it because A1.3 registers it.
- Semantic validation of what the frame carries (Codex review,
  2026-09-04): object type and canonicalization version are bound but
  not checked for support; the algorithm identifier is compared
  between fields, not used to select among modeled algorithms. Scope
  limits of the key-binding claim, assigned to P7 (object types) and
  P8/H1a (versions, algorithm profile).
- Manifests richer than the bare authority tuple: here signing,
  hashing, and binding all act on one object; the correspondence for a
  manifest with non-authoritative fields is P8's and map v1's, not
  established here.

**Suite rules from S-P3** (carried to S-P1, S-P2, S-P7, S-STANDING):
report outputs to private-channel judges are parallel with their
continuations (recut 1); the N1 witness is honest-flow acceptance
emitted by the judge, never bare acceptance (recut 3); judge locals
never shadow library names; each model's header names which of its
checks are load-bearing for its queries and which are carried for
other properties (F7).

**The question the cold read answers** (reviewer's phrasing, adopted):
*Does this model preserve the attack and the defense we intend to
study, and have we assigned every omitted detail to an explicit
remaining obligation?*

On companions: they discharge nothing of the property; what they
supply is evidence that the checking arrangement can detect the
intended failures — without them a green correct model is
uninformative.

## Status toward discharge (PROPERTIES.md line 12 terms)

Tool passes: yes, all correct models green, all required companions red
(one via an added companion, recorded). Agreement-gate falsification
review by non-author models: **run, two models, 2026-09-05** — no query,
prediction, or verdict changed; the model's self-description was
narrowed (F5–F8), one witness made honest, one warning removed. Per-lemma prose mapping: this
file's F1 and ledger entry 1 are the draft; the author's cold read of
`sp3_q2_degraded_compromised.pv` against P3's registered sentence is the
gate. Recommendation (collaborator): P3 → `checked` on the author's read of
the corrected Q2 header against P3's sentence; `discharged` waits on
the [assumption] half (H1a) regardless.

## Review log

- 2026-09-04 — ladder run 1 (sequential judge reports): Q2 green, Q4
  red, Q1/Q3 "cannot be proved"; diagnostics d1–d14; recut 1; ladder
  run 2 all as registered except Q5's companion (F3); Q5 recut 2 for
  per-role judges; companion 2 added and run. Collaborator throughout;
  no author read yet.
- 2026-09-04 — Codex (`gpt-6-astra`, author-dispatched) read Q2, the
  judge, and the library's signature rules and re-ran Q2: three results
  match. First non-author replication. Two scope limits added above;
  review question adopted; record at
  `docs/reviews/2026-09-04-codex-sp3-q2-review.md`. Author read still
  pending.
- 2026-09-05 — two blind falsification reviews (Claude Opus 5, Claude
  Sonnet 5; jailed to the model, the library, P3's text, A1.3); 45
  mutation/attack/probe files archived under `run2/falsification/`;
  twelve consolidated findings dispositioned in
  `docs/reviews/2026-09-05-blind-falsification-sp3-q2.md`; recut 3
  applied and the ladder re-run, no result changed. Author read still
  pending.
- 2026-09-05 — **Author read (agreement gate, P3 [model] half): PASSED.**
  The author read `sp3_q2_degraded_compromised.pv` lines 41–56 (recut-3
  header) and 98–130 (verifier) against P3's registered sentence and
  said: "I agree that the narrowed header says what that verifier
  does, no more." `formal/PROPERTIES.md` P3 row moved `open` →
  `checked` with this file as artifact; `discharged` waits on the
  [assumption] half. Recorded by the collaborator in the author's
  words; the commit is the author's.

