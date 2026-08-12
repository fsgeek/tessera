# Exploration note — outward verification: what RFC 9943 and CCF actually prove

> **STATUS: WORKING NOTES. NOT A PRE-REGISTRATION, NOT AN AMENDMENT,
> NOTHING DISCHARGED.** This document records the first time this
> project's verification instrument has been pointed at anything
> outside its own record. It was prompted by the author's observation
> (2026-08-12) that no prior instance had checked the formal claims of
> the RFC or of the shipping SCITT implementation, and by a candidate
> claim in the 2026-08-11 note that had not been earned.
>
> Everything here is a **candidate** or a dated observation. Nothing
> has been registered, reviewed by a non-author, or signed. Items
> graduate the same way band-1 docket items do: by registration or by
> disposition with reasons.

## Provenance

Read 2026-08-12 by Claude (Opus 5), at the author's direction, from
primary sources supplied by the author or fetched in-session:

- RFC 9943, "An Architecture for Trustworthy and Transparent Digital
  Supply Chains" (Birkholz, Delignat-Lavaud, Fournet, Deshpande,
  Lasker; June 2026), text form, in `docs/references/rfc9943.txt`
  (1772 lines). Line citations below refer to that file.
- `microsoft/scitt-ccf-ledger`, cloned to `tmp/scitt-ccf-ledger`.
- `ietf-wg-scitt/draft-ietf-scitt-architecture`, cloned to
  `tmp/draft-ietf-scitt-architecture`.
- Howard, Kuppe, Ashton, Chamayou, Crooks, "Smart Casual Verification
  of the Confidential Consortium Framework," NSDI '25
  (arXiv:2406.17455v2). Pages 1–8 read directly.
- CCF documentation on receipt verification
  (<https://ccf.dev/main/use_apps/verify_tx.html>).

**Not read, and therefore not claimed on:** RFC 9942 (COSE Receipts),
which RFC 9943 delegates all VDS security considerations to (line
1342–1344); the remainder of the NSDI paper past page 8; the CCF
codebase itself. Searches of the `scitt-ccf-ledger` tree were shallow
(grep over tracked text) and absence there is weak evidence.

## Finding 1 — RFC 9943 contains no formal model, and this is unsurprising

A search of the full text for `formal`, `machine-checked`, `theorem`,
`TLA+`, `ProVerif`, `Tamarin`, `Coq`, and `model check` returns
nothing. Every occurrence of "proof" in the document is a
*cryptographic* proof — inclusion proofs, consistency proofs,
Verifiable Data Structure Proofs — not a mathematical proof about the
architecture.

The security guarantees are stated in three prose sentences (lines
1283–1297) and the threat model (§9.7) is thirty lines of prose.

**This is not a criticism and must not be recorded as one.**
Architecture RFCs are prose documents; that is what the genre is. The
correct statement is narrow: at the architecture layer there is no
machine-checked artifact to compare against Band 0, so any Tessera
claim of the form "we modelled this and they did not" is comparing
against a document that never undertook to model anything.

## Finding 2 — CCF's formal verification is real, serious, and better bound to reality than Tessera's

This is the finding that costs us something, and it is stated first
among the substantive ones deliberately.

The NSDI '25 paper describes TLA+ specifications of CCF's consensus
protocol (17 actions over 13 variables) and of its client consistency
model, checking State Machine Safety via the invariants `LogInv`,
`AppendOnlyProp`, and `MonoLogInv`, plus "a further 27
invariants/properties" (§4). Critically, the specs are **bound to the
C++ implementation by trace validation** (§6): implementation traces
are checked for membership in the set of behaviours admitted by the
spec, and the whole apparatus runs in CCF's CI pipeline. The approach
found six subtle bugs in design and implementation before production.

Two honest comparisons follow:

1. This is stronger practice than most production distributed systems
   achieve, and the "smart casual" framing — rigour where it pays,
   integrated into CI rather than performed once — is closer to this
   project's stated values than to its rhetoric about competitors.
2. **Their models are tied to a running implementation and ours are
   not.** Band 0 is machine-checked against nothing that executes.
   Trace validation is precisely the discipline Tessera has not yet
   earned the right to claim, because there is no implementation to
   validate traces from. Any comparative claim about rigour should
   register this asymmetry against us until Phase 1 exists.

## Finding 3 — the scope of what CCF verifies, precisely

The specifications cover the correct operation of a **live** service:
consensus safety under node failure, network asynchrony, and
reconfiguration; and the externally observable consistency guarantees
offered to clients. The client consistency spec states explicitly that
"by design this spec does not model the internal details of the service
itself" (§5), and trace collection excludes the bootstrapping phase, "as
this phase is not modeled in our consensus spec" (§6.1).

Not covered anywhere in the verified scope: receipts as long-lived
artifacts, key rotation, service identity endorsement, disaster
recovery, or the meaning of a receipt after the service stops running.
Offline log integrity is a stated CCF *requirement* (§2.1, signature
transactions), and the append-only property of the log is modelled —
but what is proved is that the ledger is produced correctly, not that
a receipt remains interpretable once the operator is gone. Those are
different theorems.

**Candidate conclusion, narrowly stated:** the durability-past-operator
property is unverified at both layers — not because anyone failed, but
because it is nobody's property. It sits outside the RFC's architecture
scope and outside CCF's verification scope.

## Finding 4 — the RFC's own normative text supports Finding 5 of the 2026-08-11 note

The 2026-08-11 note argued that the loose differentiator ("SCITT didn't
think about service death") dies on rebuttal, and the precise one
survives: *the receipt outlives the service; the accountability dies
with it.* The published text supports the precise form, from four
directions:

1. **Offline verification is explicit.** A Receipt "is universally
   verifiable without online access to the TS" (line 595). The loose
   form is definitively dead; cite this line whenever it resurfaces.
2. **But the trust chain terminates in an identity, normatively.** "A
   Relying Party MUST trust the verification key or certificate **and
   the associated identity** of at least one Issuer of a Receipt"
   (lines 1236–1237). A key with no one left to defend the identity
   behind it still satisfies the letter and not the substance.
3. **Accountability requires a live service.** "Anyone with access to
   the TS can independently verify its consistency" (line 601), and
   reputable TSs are incentivised to behave "as any inconsistency can
   easily be pinpointed by any Auditor with read access to the TS"
   (lines 607–609). Read access is to a running service. The
   incentive structure the RFC relies on for honesty evaporates when
   the service does — which is the split the 08-11 note named, now
   sourced to the RFC's own rationale rather than to our inference.
4. **Receipts are re-issuable renderings, not fixed artifacts.**
   "Requesting a Receipt can result in the production of a new Receipt
   for the same Signed Statement. A Receipt's verification key,
   signing algorithm, validity period, header parameters or other
   claims MAY change each time a Receipt is produced" (lines 596–599).
   Combined with the MUST in §9.4 that TSs "rotate their keys at a
   cryptoperiod appropriate for the key-algorithm" (line 1337): if
   long-term validity requires a receipt under a current key,
   obtaining one requires a live TS. This is a sharper form of the
   key-rot argument than the record currently holds and it is sourced
   entirely to normative text.

## Finding 5 — the rollback clause (new; not previously in the record)

§9.4.2, lines 1350–1353:

> TSs whose receipt signing keys have been compromised can roll back
> their Statement Sequence to a point before compromise, establish new
> credentials, and use the new credentials to issue fresh Receipts
> going forward.

And immediately after (lines 1355–1356): "Revocation strategies for
compromised keys are out of scope for this document."

Three observations, offered as candidates:

1. The append-only ledger has an explicit operator-invoked escape
   hatch. Statements registered before the rollback point can cease to
   be registered. "Linear and irrevocable history" (line 118) is
   qualified by this clause.
2. There is no protocol mechanism by which a relying party learns a
   rollback occurred. The RFC's remedy is exhortation — "it is
   important for Issuers and TSs to clearly communicate when keys are
   compromised" (lines 1348–1350) — and revocation is out of scope.
3. Because verification is offline (Finding 4.1), a relying party
   never asks. **An old receipt continues to verify correctly after
   the fact it attests has been withdrawn.** This is the mirror image
   of the failure mode the record has been studying: not a receipt
   that stops working, but one that keeps working after it should have
   stopped.

`scitt-ccf-ledger` contains no rollback, revocation, or key-rotation
handling that a shallow grep can find. Given the caveat in Provenance,
this is suggestive only.

## Finding 6 — what CCF *did* build for continuity, and why it is not the same property

Fairness requires recording the strongest counter-evidence. CCF has
real machinery for surviving service death-and-recovery: a recovered
service carries a `serviceEndorsements` list, an ordered chain of
previous service identities, so a receipt issued under an earlier
service identity remains verifiable after recovery by walking the
chain. Verification remains offline; the endorsements ride in the
receipt.

That is genuine engineering for continuity, and any Tessera claim that
CCF ignored the problem is false. The distinction that survives:

- CCF handles service **recovery** — the same consortium re-forms,
  and the new identity is endorsed by the prior one.
- It does not handle service **death** — there is no successor to
  issue the endorsement, and the chain still terminates in a root
  someone operates and must keep defensible.

Tessera's candidate differentiator therefore narrows correctly to the
form the 08-11 note already reached: not "we survive service death"
but *our trust chain never contained anyone whose death matters.* The
adjustment is that this must now be argued against a competitor that
has thought carefully about the adjacent problem, not against one that
overlooked it.

## Disposition — what is earned and what is not

**Earned, and citable:**

- SCITT receipts verify offline (line 595). The loose differentiator
  is dead and should not be restated.
- The verify/accountability split is supported by the RFC's own
  rationale text (Finding 4.3).
- Durability-past-operator is unverified at both the architecture and
  implementation layers, and is nobody's stated property (Finding 3).

**Not earned, and to be retracted if it appears anywhere:**

- Any claim that Tessera's formal work is more rigorous than CCF's.
  The opposite is currently true in the dimension that matters most:
  theirs is bound to a running implementation by trace validation and
  ours is bound to nothing that executes (Finding 2).
- Any claim that SCITT or CCF ignored service death (Finding 6).

**Candidate docket items** (register or dispose; not adopted here):

1. The rollback clause (Finding 5) as a named contrast case — a
   registered property of the form *a Tessera verdict cannot be
   withdrawn by the operator after issuance* would sit directly
   opposite RFC 9943 §9.4.2. This may be the sharpest available
   differentiator and it is not currently on record.
2. Trace validation as the eventual Band 1 / Phase 1 discipline. The
   NSDI paper is a worked example of tying TLA+ to an implementation
   in CI, and it is the standard this project should expect to be held
   to once code exists.
3. The SCITT/COSE interoperability question parked in the 2026-08-11
   note remains open and is now sharper: `scitt-ccf-ledger`'s own
   alignment doc still tracks Architecture Draft 11 rather than the
   published RFC, so the interoperability target is itself moving.

## Explicit non-implications

- No amendment arises from this note.
- The engineering sequence is unchanged: DECISION.md, then the
  capstone/bridge spike, then core convergence.
- Nothing here weakens or reinterprets any registered property,
  ruling, or amendment. Findings 2 and 6 constrain what the record may
  *claim* about others; they do not touch what it has proved about
  itself.
