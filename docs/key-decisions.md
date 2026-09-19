# Tessera — the load-bearing decisions

**STATUS: DRAFT — assembled by Claude Opus 5 for the owner instance, 2026-09-19; not adopted; provenance per entry.**

*Owner's note, 2026-09-19 (Claude Fable 5.1, owner instance): asked for by the author in session ("If the real decisions are few, what would be helpful is having a list of those key decisions and the reasons for them"). Every commit hash, quotation and section citation below was checked against the record by the owner instance before this file was placed; the docket item 27 citation in Decision 6 refers to the vocabulary ruling recorded inside that item, not to the item's headline. This is the seed of the stand-alone design story the author asked for on 2026-09-12; the path to each decision stays in the record, not here.*

This is the short list: decisions that, if reversed, would change what Tessera is. Consequences and bookkeeping —
counts, encodings, query shapes, parameters — are deliberately left out. Each entry names where it lives.

**Decision 1: What an attestation says, and what it does not.**
- Tessera attests the identity of the framed bytes presented at one issuance event, tied to a temporal anchor —
  nothing more. Meaning, truth, intended use, and the identity of what the payload refers to are outside it.
- Rules out: the reading that a valid Tessera receipt vouches for the contents of the package.
- Why: a claim stated exactly can be modelled and defended; a claim about truth cannot. The record also fixes the
  operative form: altering bytes is trivial; surviving verification over altered bytes is what is hard.
- Who and when: author-ruled 2026-07-28, adopted at `68b581c` (2026-08-07).
- Where: `docs/phase-0-prereg.md` §1; `docs/phase-0-prereg-amendment-3.md` §A3.1; `README.md` "What this repository is".

**Decision 2: The formal foundation is finished before any service code is written.**
- Machine-checked models of the central guarantees, the agreement gate, and a plain-language written proof must
  all exist before Phase 1a begins. The gate is written so failing it is legitimate: "the project does not
  proceed as designed."
- Rules out: building first and modelling afterwards, and the softer version where the two run alongside.
- Why: the central guarantee of an attestation service is the one thing that cannot be asserted and built around.
  Building on an unproven foundation would be the theatre the project exists to refuse.
- Who and when: signed in the original pre-registration (`75207ba`); "any code" clarified by the author 2026-08-29
  at `634c2f2` to mean code intended for the service — which is why the probes and spikes exist.
- Where: `docs/phase-0-prereg.md` §8 "The gate"; `README.md` method item 2;
  `formal/spike/standing-probe/DECISION-CRITERIA.md`, glossary "Band 0 / Band 0 exit".

**Decision 3: Two signatures from two independent failure domains.**
- The cloud key (KMS) signs the receipt and a local GPG key counter-signs the same canonical bytes.
- Rules out: signing with the cloud key alone — rejected not because that key is incapable, but because it puts
  the whole trust story in one operational domain.
- Why: the threat model is "will this adjudicate in fifty years," not "is it valid today." The two keys fail for
  uncorrelated reasons — an account or policy lapsing versus a local key leaking — so durability rests on no one
  domain, at near-zero cost.
- Who and when: the author's own decision in the signed pre-registration ("Decision: C").
- Where: `docs/phase-0-prereg.md` §3.1, under §3 "Architecture decisions (the part that is genuinely yours)". The
  same principle governs the project's own record: GPG-signed commits for *who*, OpenTimestamps anchors for
  *when*, both required (`README.md`, "Disciplines").

**Decision 4: A receipt must verify with Tessera dead.**
- The verification path touches no database, no live service, no network. The bundle carries what a future
  verifier needs: timestamped evidence that the issuer keys were authorized at issue time, and the spec itself.
- Rules out: verifying by asking Tessera, or resolving a key through live DNS or a reachable repository — those
  stay discovery mechanisms, never verification dependencies.
- Why: an attestation whose verification depends on its issuer's survival is not an attestation. The record is
  equally honest about the limit: survival after handoff is custody, not construction.
- Who and when: hard rule in the signed pre-registration; the survivability claim split three ways (portability /
  availability / long-horizon continuity) adopted 2026-08-07, registered in Amendment 3 (`8ae4720`).
- Where: `docs/phase-0-prereg.md` §4.4; `docs/phase-0-prereg-amendment-3.md` §A3.4.

**Decision 5: Evidence is transcribed into the envelope, not pointed at ("transcription binding").**
- The authority evidence carries the exact authority statement, or a declared digest of it, inside the signed
  envelope. The envelope names a signed, nonempty required set of binding forms and a verifier must validate
  every member — partial success is not success.
- Rules out: digest publication (the referent would have to be fetched from elsewhere) and a separately hashed
  manifest core (a second object and binding to audit). "Authorized tuple" is deferred, not rejected.
- Why: it removes both the external dependency and the manifest/evidence circularity, and it survived the
  registered attack in both channel-compromise variants while the broken companion produced a real attack.
- Who and when: entered by the author 2026-08-13 at `459aff0`, against criteria registered before any evidence.
- Where: `formal/spike/first-link/DECISION.md`, §§ "Proposed decision", "Binding-form disposition", "Rejected alternatives".

**Decision 6: Tessera reports; the adjudicator decides — and the report is never one checkmark.**
- Verification returns a typed state (`VALID_STRICT`, `VALID_DEGRADED`, `INVALID`, `UNVERIFIABLE`), never a bare
  true/false. Standing is reported beside that verdict as its own value, so an artifact can honestly be valid and
  have no standing. The verifier is a pure function of bundle plus policy; the relying party decides trust.
- Rules out: collapsing "this failed a check" and "this check could not be performed" into one boolean, which is
  where fail-open bugs hide; and Tessera deciding trust for the adjudicator.
- Why: those distinctions are what a future decision turns on, and Tessera cannot know the policy of a party
  eighty years out. Standing is reported and never waived; accepting an artifact that has none is the relying
  party's own recorded decision.
- Who and when: typed verdict signed in the original pre-registration; standing as an orthogonal dimension
  registered in Amendment 3 (`8ae4720`, 2026-08-09); the verifier/adjudicator vocabulary RULED (author)
  2026-09-06. Standing's mechanism — the **terminal lineage record**, binding issuance identity, attempt lineage
  and terminal disposition — was ADOPTED (author) 2026-08-31 on the scorer's recommendation, entered 2026-09-04.
- Where: `docs/phase-0-prereg.md` §4.6; `docs/phase-0-prereg-amendment-3.md` §A3.7 item 1;
  `formal/spike/standing-probe/DECISION.md` sub-ruling 5 (entered at `fbf6387`); `docs/band-1-docket.md` item 27.

**Decision 7: Issuance is allowed to end in refusal, and the refusal is a durable record.**
- Issuance makes at most N attempts (working default 3), then terminates in an explicit refusal — a first-class
  protocol outcome, not an error path. The refusal latches atomically and creates, in the same step, the portable
  record, its public commitment value, and pending delivery and publication status.
- Rules out: the unbounded "re-issue until it works" loop, whose triggers are correlated across attempts, so a
  retry is not a fresh draw and the loop can livelock.
- Why: fail-closed means the system can say no. And a mortal authority cannot make evidence of its own decision
  externally durable at the instant it decides, so the design exposes that partial order rather than close it.
- Who and when: Amendment 2, adopted 2026-07-21 (`62f0c5f`); durability, handoff and publication obligations
  assigned in Amendment 3 (`8ae4720`, 2026-08-09).
- Where: `docs/phase-0-prereg-amendment-2.md` §A2.3; `docs/phase-0-prereg-amendment-3.md` §A3.7 item 2.

**Decision 8: Band 0 ends only when the models compose, each seam with a deliberately broken twin.**
- Every fact one model assumes and another must establish is written into a ledger. Exit requires a single
  composed model where each such fact is proved by a real query and carries a broken companion that makes the
  consuming query fail. Assumptions no model can discharge — concrete cryptography, channel independence,
  implementation fidelity, chain availability, anchor correctness — are listed as unclaimed, never absorbed.
- Rules out: calling the foundation done because each model passes alone, and carrying a cross-model assumption
  as though it were proved.
- Why: per-property proofs can each hold while the joins between them do not, and the broken companion is what
  shows a green result is a result rather than a vacuous model.
- Who and when: registered in Amendment 3 (`8ae4720`, 2026-08-09); the composition's shape — one composed
  verifier, not several — RULED (author) 2026-09-15 ("composition is the right answer here"), with his concern
  recorded and not dissolved: "the real burden for testing these claims will fall on the adjudicator."
- Where: `docs/phase-0-prereg-amendment-3.md` §A3.3; `formal/suite/LEDGER.md` §5 (the ruling) and §6 (what the
  composed model must contain); `formal/BAND0-EXIT.md` row E5.

## Not on this list, and why

- **The k = 6 confirmation-depth evidence** (`formal/BAND0-EXIT.md` E18) — work showing that a registered
  parameter's value does not change what the models prove: evidence for decisions already made.
- **The encoding map** (`docs/band-1-docket.md` item 33) — it says where each already-decided binding lives in
  bytes. A layout follows from the decisions above; it does not make one.
- **The composition join and query shapes in the capstone** (`formal/suite/LEDGER.md` §6,
  `formal/suite/capstone/PREDICTIONS.md`) — Decision 8 carried out; which query serves which ledger row is
  bookkeeping under the 2026-09-15 ruling.
- **Two author statements that are not decisions of this kind.** The 2026-09-18 `REFUSAL`-tag ruling
  (`formal/suite/capstone/PREDICTIONS.md` §8 item 1) is real, but rules on what one symbolic fixture exercises
  and changes nothing in Decision 7. And "the adjudicator decides; the Layer 2 register is their checklist"
  (`docs/band-1-docket.md` item 35) is entered as a candidate, *not registered*; its live half is Decision 6,
  and the plain-language register it asks for is an owed artifact, not a decision taken.
