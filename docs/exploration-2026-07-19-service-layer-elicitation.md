# Exploration notes — service-layer elicitation (issuer continuity, succession, registration structure)

> **STATUS: WORKING NOTES. NOT A PRE-REGISTRATION, NOT AN AMENDMENT, NOTHING
> DISCHARGED.** Session of 2026-07-19 (Tony + Claude Fable 5). Companion to
> `exploration-2026-07-18-causal-dag-commons.md`; same rules: everything here
> is a candidate, decisions marked as such are the author's, and the path to
> reality is adversary model → properties → formal discharge → non-author
> falsification → signed registration.
>
> Purpose: capture the service-layer design elicited from the author's memory
> before it evaporates again. The prior version of this design survived only
> in the author's head after the AI conversation that developed it was lost —
> this document exists so that failure mode is not repeated a second time.

## 1. The id-of-next design, recovered (row 2: issuer continuity)

The author's original design: each signed package pre-declares a UUID — "the
next identifier I'll use" — as a pre-registration of the successor slot.

**Mechanism (corrected from the assistant's initial mis-model):** the next-ID
is *public*, inside the current signed bytes. It is not a secrecy mechanism;
it is a *forcing* mechanism. Any continuation claiming legitimacy must occupy
the pre-declared slot:

- **Thief takes the slot** and the legitimate issuer is still publishing →
  two signed instances of one (issuer, UUID): *provable equivocation* under
  the lineage rule, not deniable concurrency.
- **Thief avoids the slot** → their validly-signed node does not occupy the
  declared successor position, and a verifier applying "the continuation of
  N is whatever bears N's declared next-ID" rejects it *as lineage* without
  detecting anything.

This is the fencing-token / generation-number move applied to issuance
lineage. Note the standing of the 07-18 doc's worst-error correction: the
Codex correction said DAG topology cannot detect takeover *unless* the
protocol defines "a unique causal position at which only one event is
permitted." id-of-next **is** that mechanism. The correction independently
derived the necessity of a design it did not know existed.

**Layer placement (repairs the 07-18 drop):** the 07-18 notes discarded
id-of-next because "a DAG has many concurrent children, so 'the next' is
undefined." That conflated rows: the *claim graph* (row 4) is a DAG with
legitimate concurrency; the *issuer's continuity thread* (row 2) is linear
per issuer. id-of-next is a row-2 mechanism and was dropped from the wrong
row.

**Two assumptions that must be registered as such:**

1. **The legitimate issuer survives to produce the collision** — this
   defends the split-brain case (its original name), not silent succession.
2. **The two instances meet somewhere an observer sees both** — detection,
   not auto-discovery (author's phrasing). In an unowned commons the same
   UUID can live in disjoint gossip partitions indefinitely. Synthesis: the
   next-ID in the signed bytes is the *rule* (portable, offline-checkable,
   survives operator death); a transparency overlay (row 3) is the *meeting
   point* where slot-occupancy is recorded and collisions become
   discoverable. Each half covers the other's weakness.

**The nonce refinement (author, this session):** the attacker's
gossip-exposure compounds with each forged message only if slot names are
generated deterministically for the chain's lifetime. Two distinct variants:

- **Public-deterministic** (next slot derivable from public chain state):
  every future slot is watchable; a forged continuation collides or is
  invalid-by-rule at *every* position, not just the first.
- **Secret-seeded** (slots derived from a nonce only the issuer holds): the
  signing-key thief can occupy the one pre-declared slot but cannot *name*
  valid slots after it. The nonce becomes a succession credential distinct
  from the signing key — a second thing that must be compromised
  concurrently (the attacker-cost currency of 07-18 §7 item 7). Cost: a new
  loss-of-continuity point, folding into the succession story.

**Prior art (structure-checked this session, not assumed):** KERI
pre-rotation. Each key event pre-commits a digest of the *next* keys; a
rotation is valid only if it reveals and is signed by the pre-committed
keys; recovery from current-key compromise is rotation to the pre-committed
unexposed keys. For key events this is strictly stronger than the UUID slot
(the thief lacks the successor credential entirely). Natural row-2 design:
KERI-style pre-rotation for *key* succession + UUID slots for *issuance*
succession + transparency overlay as meeting point. Refs:
<https://identity.foundation/keri/kids/kid0005.html>,
<https://www.vlei.wiki/concept/rotation>, <https://arxiv.org/pdf/1907.02143>.

## 2. Decision candidate (author, this session): the doppelganger exclusion

Silent usurpation — key stolen *and* issuer silenced/coerced/dead, thief
continues cleanly in-slot — is **explicitly excluded** from the row-2 threat
model as a declared residual risk (precedent: A1.3's insider boundary).
Solutions exist (witness cosigning, threshold control, delayed activation)
but all are standing infrastructure: a later band that prices out one more
adversary capability, not a requirement now. Author remains open to
solutions if cheap ones surface. NOT yet registered — candidate only.

## 3. Succession and the authority root (fork dissolved by the record)

The elicitation fork was: channel-rooted authority vs. self-certifying log
with channels as witnesses. The *registered* design (Amendment 1, authority
section) is a third thing that dissolves it: **plural archived evidence** —
two external authority evidences (DNSSEC chain snapshot for `wamason.com`;
anchored public-repository commit with OTS proof) archived *in the bundle*,
plus manifest self-signature as possession-only. "DNS and repositories are
discovery mechanisms, not verification mechanisms" — no live channel is in
the trust path; authority is the archived plural evidence at each event's
time.

Extension to succession (candidate): a key event (revocation, re-key) is
itself a published, anchored, plural-channel-evidenced statement; the
key-event log is the sequence of such archived events; id-of-next slots and
pre-rotation digests ride inside each event as the internal succession rule.
Channels disagreeing at one instant → fails VALID_STRICT. Internal lineage
disagreeing with channel evidence → a detectable, policy-classified event.

**Residual that carries forward and worsens:** correlated control. The
adversary who owns the author's operational sphere owns both revocation
channels too. Same misissuance boundary as A1.3 item 7; must be named in the
service-layer adversary model, not inherited silently.

## 4. Registration structure — the open decision (with the decision space)

The author challenged the assistant's three-option list (single program doc /
per-row docs / adversary-indexed bands) as possibly incomplete. Correct: the
list varied granularity while silently fixing other dimensions. The honest
decomposition:

- **Granularity:** one document; per-row documents; staged (adversary model
  first, properties second).
- **Organizing principle** (07-18 §7 q5, deferred there and still open):
  layer rows; adversary-indexed bands; guarantee lattice; cost-denominated
  bands.
- **Relation to existing registration:** new sibling registration (the
  07-18 §8b endorsed disposition) vs. amendment extending Band 0 (rejected:
  keep Band 0 narrow).
- **Timing:** register now vs. remain in working-notes mode until stable.
  (Mitigated regardless by committing captures like this one immediately.)
- **Methodology inside the document** (orthogonal): bespoke A1.3-style prose
  adversary model vs. structured methods (attack trees, STRIDE-per-element,
  SCITT role mapping) — can be combined.

Current assistant recommendation (not yet accepted): single-document *scope*
(seams between rows must live inside one reviewed artifact — every recurring
Band-0 finding was a composition failure), delivered in *stages*: register
the adversary model + row-handoff table first (short, high-quality review
cycle; properties then derive from a *reviewed* adversary model — same
ordering logic as not building the bridge model against an under-review A2);
properties follow as a second signed stage. Each row's section must state
what it hands to adjacent rows and what it assumes from them (the P5c↔P5P6
lesson applied at birth). Exit condition per stage: non-author review +
author signature — understanding is the gate; discharge is scheduled
separately.

## 5. Open questions register (this session's additions)

1. Public-deterministic vs. secret-seeded slot generation (or both, per
   epoch?). Interacts with the succession story and the attacker-cost model.
2. What exactly does the transparency overlay attest about slot occupancy,
   and under what observer/retention/non-collusion assumptions (07-18 §2
   bounded detectability)?
3. Succession legibility: full design of key-event statements (format,
   channels, anchoring) and their verifier policy classification.
4. Whether the doppelganger exclusion (§2 above) is ratified as registered
   text or narrowed by a cheap mitigation first.
5. Registration structure decision (§4 above) — routed to the author.
