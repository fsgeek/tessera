# Phase 1 report — throwaway prototype (issuer, verifier, attack replay)

*2026-10-06. Built by a Claude Opus 5.5 agent straight from `docs/implementation-spec.md` §2.3–§2.4,
§3, §4, §5 and §6. THROWAWAY: not service code, and none of it may be copied into the service. Nothing
is staged or committed. Reproduce with `cd prototype && uv sync && uv run pytest -q` (25 pass) and
`uv run python run_phase1.py`.*

## Outcome

Both attack traces fail against the verifier built from the spec, and both succeed once the check
that their companion removed is removed here too. The honest flow verifies.

| Run | Correct verifier | Mutated verifier | Goal event |
|---|---|---|---|
| Honest: issue → verify, strict | `VALID_STRICT`, standing `ESTABLISHED` / `TERMINAL_DISPOSITION_SHOWN` | — | — |
| **C-C2 reattribution** (degraded: `repo` waived, the `dns` key leaked as skS) | **`INVALID`**: V17[A] (frame fingerprint pin) and V18[A] (manifest hash), plus the same two on slot B | Pin and `mh` check removed: **`VALID_DEGRADED`** | `ReattributedA` fires on the mutant only |
| **C-C5 inner-signature transplant** (wrapped, degraded, DSKS **emulated**) | Outer layer `VALID_DEGRADED` (the attacker's own wrapper, a registered cost); inner layer **`INVALID`** on exactly V19[A] (the signature does not cover the presented frame) | Signature bytes unbound from the frame: inner layer **`VALID_DEGRADED`** | `InnerSigTransplanted` fires on the mutant only |
| C-C5 mutant *without* the DSKS hook | — | inner `INVALID` | The attack needs DSKS, as the trace says |
| C-C2 mutant, strict mode | — | `UNVERIFIABLE` (the attacker cannot produce `repo` evidence) | — |
| C-C2 mutant, replayed after declared + 80 h | — | `INVALID` on V34 | A defence that exists only concretely (see prediction 4) |

The pytest suite (`tests/test_phase1.py`, 25 tests) also covers:
- standing: S1, S2 (`SUPERSEDED`, on an attempt discarded because it was buried late), S3, S4 (`ISSUANCE_REFUSED`);
- the P8 ingestion rejections, a tampered frame (`INVALID`), and missing headers (`UNVERIFIABLE`);
- the unknown-algorithm canary (`UNVERIFIABLE`), revocation inside the window (`INVALID`), and an illegal waive-everything policy (refused);
- a demonstration of the registered degraded cost: a copy of the honest content under the attacker's key and the honest issuer id, with the sole required channel's key leaked, comes out `VALID_DEGRADED`, with `repo` evidence recorded as `absent`.

**What was stubbed.** The anchor is a local hash chain labelled STUB: no OpenTimestamps, no Bitcoin, no
proof of work. The DNSSEC and git authority channels are stubbed as Ed25519 channel keys, which is
exactly how the model treats them. KMS and GPG are in-process Ed25519 keys. The refusal record is not
built. Standing was cheap, so it is built.

## GUESSES summary

**50 guesses** (plus two sub-entries) and **7 contradictions or tensions** (K-1 to K-7), all in
`GUESSES.md`. By area: bytes and encodings 18, manifest and authority 7, temporal and anchor 8, verifier
procedure and output 9, issuance and standing 10.

The five that matter most:
1. **G-01 and G-15: the frame layout and the encoding map (O-01, O-79).** Every byte of every signed
   object is my invention: field widths, tag form, where the six attested fields sit inside the payload,
   and what "payload equal across slots" means in bytes. A second implementation built from the same
   spec would agree with this one on no signature.
2. **G-27: revocation has no input.** R-5.21 requires "no revocation effective at or before
   `anchor_time`". Neither the bundle (R-5.4) nor the trust configuration (R-5.8) carries any revocation
   fact. I added a `revocations` map to the trust configuration, which goes beyond R-5.8. Without it the
   check cannot be performed for any bundle at all.
3. **G-14 and G-22, with K-5: what the manifest hash and possession cover.** I used the tuple only
   (`mh = h(t)`, possession over `t`). Everything else a real manifest carries — keys, evidences, the
   binding-form set, the manifest's own anchor — is outside both.
4. **G-19 and K-2: one anchor, two frames.** Under reading (a) a two-signer receipt has two frames, but
   R-3.42 asks for "exactly one anchor proof over its canonical bytes". I anchored a length-prefixed
   digest of both frames.
5. **G-13 and K-3: the GPG slot.** An OpenPGP signature does not sign the frame alone, and R-3.12's
   "algorithm equal across slots" rules out KMS and GPG keys of different algorithms. I emulated the GPG
   slot as raw Ed25519.

Runners-up:
- **G-29 / K-6** changes a verdict: a missing required evidence is `INVALID` or `UNVERIFIABLE`, depending on which requirement you cite.
- **G-09**: what `key_fp` and `sset` mean for two signers. I took it from the trace rather than the spec.
- **G-10b**: an algorithm-specific fingerprint makes V16 unperformable on the canary vector. My first build failed it instead, and returned `INVALID` where R-3.53 requires `UNVERIFIABLE`.

## Predictions 1–4: the evidence (the owner scores)

**1. "Underdetermined in at least five places, mostly inside P8's territory."**
- The count clears five by a factor of ten: 50 guesses.
- "Mostly inside P8" is not supported: 18 of the 52 entries are byte or encoding guesses. The rest fall
  in places the prediction did not name:
  - which input revocation comes from (G-27);
  - what the issuer's ship guard and the TLR anchor measure tolerances against (G-39, G-50);
  - verifier output, where reason codes exist for almost no envelope check (G-30);
  - the standing-path outputs the model leaves undefined (G-34, G-35).
- Some are P8-adjacent but were assigned to other properties: the anchor-digest question (G-19) and the
  binding-form set's location (G-17).

**2. "The manifest-versus-authority-tuple abstraction forces a design choice the model never made."**
The evidence supports it. Building the manifest forced these choices:
- **(a) The binding-form set had to move.** It went into the attestation's signed `common`. Placed in
  the manifest, as the §3.4 table suggests (K-4), it would be bound by neither the authority evidence
  (map v1 is five fields) nor `mh`.
- **(b) Two hash scopes needed rules.** Choosing what `mh` hashes (G-14) and what possession signs (G-22)
  required a rule, because R-3.38 says "manifest" where the model says `t` (K-5).
- **(c) Keys bind only indirectly.** Public keys are bound only through fingerprints (G-23).
- **(d) The two-signer tuple had no rule.** `key_fp` versus `sset` (G-9) has no rule the spec states; I
  read it off a trace.
- **(e) Revocation has nowhere to live** in the tuple-shaped manifest (G-27).

Under (a)–(e) the prototype stays sound only because I kept `mh = h(t)` and pushed every other
manifest member either into the attestation's signed bytes or into a fingerprint comparison. That is a
stated rule, and the spec does not give it.

**3. "A verifier built from §5 rejects C-C2 and C-C5 with real signatures."**
- Confirmed for this build.
- **C-C2** is rejected by V17's `=fp(kX)` pin and V18's `mh = h(t)` — the two checks the companion
  removed. Removing them makes it accept.
- **C-C5** is rejected by V19 alone (the signature over the *presented* frame). Unbinding it makes it
  accept, but only with the emulated DSKS hook.
- The pairs behave as the model predicts. The spec and the model have not drifted on these checks.

Caveats for scoring:
- The replay runs against *my* encodings (G-09, G-15, G-41). A different encoding choice could only
  move V17/V18, never V19.
- In the C-C5 correct run the **outer** layer is `VALID_DEGRADED`, because it is the attacker's own
  wrapper with evidence minted under the leaked key. Per-layer reporting (R-5.42) puts a valid-looking
  outer verdict next to an `INVALID` inner one. That is correct, and it is a phase-2 reading problem.

**4. "Replaying a symbolic trace concretely needs at least one non-obvious translation."**
Confirmed, with four instances:
- **(a) DSKS has no real counterpart.** `dsks(s, r)` cannot be computed for Ed25519, so `DSKSOracle` in
  `crypto.py` emulates it as a test-only hook. The hook makes one seen signature verify under one fresh,
  attacker-held key, over that signature's original message only.
- **(b) C-C5's mutant has no concrete form under Ed25519** (the less obvious one). The symbolic
  `checksign` *returns* the signed message, so the mutation `let (=BYTES, anyb) = checksign(sg,k)` means
  "accept whatever the signature signed". Ed25519 has no message recovery. The mutant exists concretely
  only if the format carries the signed bytes beside the frame, so I had to invent an attached-message
  field (G-41) for the bug to be expressible.
  - The implication runs in the spec's favour: a detached-signature format with no attached payload
    cannot even express this bug.
- **(c) Anchoring the replay has a time limit.** "Anchor anything" means the attacker anchors its own
  receipt digest. The honest frame carries its declared time inside the signed bytes, so C-C2's
  reattribution only works within [declared − ε, declared + δ]. Past that, even the mutant says
  `INVALID` (V34). The untimed model has no such defence.
- **(d) The slots are underdetermined.** The trace leaves slot B's fingerprint and `mh` free. The
  concrete replay had to pick values (a copy of the honest frame). The trace's two-signer tuple shape
  also fixed G-09.

## What phase 2 should test

**Submitter.**
- The bundle at ship carries no TLR. "Complete standing evidence is late by construction" (R-4.88 iv).
  Here the issuer attaches the TLR after the fact, so a holder who verifies the shipped bundle at once
  gets `ABSENT` / `NO_TERMINAL_DISPOSITION_EVIDENCE`. Test how the submitter learns that more is coming
  and how it gets it, without a service dependency.
- Test what a submitter receives on refusal; the portable refusal record is not built yet.

**Relying party.** Give a fresh reader these real reports and ask what they would do:
1. C-C5 correct: outer `VALID_DEGRADED`, inner `INVALID`.
2. The degraded content copy: `VALID_DEGRADED`, issuer "wamason.com", `repo` = `absent`. This is
   indistinguishable from an honest bundle whose repo evidence was merely lost — same observation value.
3. `INVALID` + `SUPERSEDED`: an abandoned attempt.
4. `VALID_STRICT` + `ABSENT`: a fresh bundle without its TLR.

This is where prediction 5 will be scored.

**2106 examiner, no service alive.** Hand an agent with no repository access only a bundle file and its
embedded objects, and see what it needs. My expectation, from the build:
- the trust configuration: the channel keys of 2026 and header pins (R-5.8 places them outside the bundle);
- the revocation facts (G-27: nowhere);
- the fingerprint function, the frame layout and the algorithm registry (the embedded spec here is a
  one-paragraph stub);
- real OTS/Bitcoin header material.

**Interop.** Run a second implementation from the spec alone, by a different model, and diff the bytes
against this one. That measures G-01, G-15 and G-19 directly.
