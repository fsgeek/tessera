# Tessera guarantee tiers — draft

> **STATUS: DRAFT, 2026-10-07, owner instance (Claude Opus 5.5), from the author's suggestion that day:**
> *"identify what someone just trying to stand up a test attestation service could do (minimal guarantees)
> and then identify what each additional layer allows us to claim."* Not adopted. Nothing here changes a
> registered sentence. Tier contents are a first cut, to be argued with.

## The idea

Each tier is a deployment choice plus **the one additional claim it buys**, and the evidence for that claim.
A deployer picks a tier, and a receipt states its tier, so a relying party knows exactly what it is being
told. Every tier keeps the defining constraint: **a receipt verifies with the Tessera service gone**, from the
bundle plus an archived trust-anchor store. A tier that needs a live service does not exist.

| Tier | The deployer adds | The claim it buys | Main new attack it must answer | Evidence today |
|---|---|---|---|---|
| **T0: anchored bytes** | one issuer key; canonical frame; an OpenTimestamps anchor | *These framed bytes existed no later than the anchor time and were signed by whoever held key K.* Nothing about who K is. | backdating; byte substitution; type confusion | P1, P5, P7 checked; **P8 open** |
| **T1: one authority channel** | K published under one domain via DNSSEC (or a git repo, which counts only with its own OTS anchor) | *K was published by whoever controlled domain D at issuance.* | issuer↔domain not tied (G-21); a stolen channel key; stale-status replay within an RRSIG window | P3, P10 single chain; G-21 missing |
| **T2: redundant channels** | a second, independent channel (DNS + repo); required channels fixed by **verifier policy** | *The claim survives compromise of any one channel* (strict mode). | a bundle choosing its own required set (G-17); one channel leaked | **the capstone**: strict cases (a)–(c), P2, P10 |
| **T3: diverse jurisdictions** | *n* keys under *n* country-code registries (e.g. .cn, .in, .br, .za); staggered lifetimes, none outliving domain ownership; *m*-of-*n* | *Forging, or hiding a revocation, needs coordinated compromise in at least m jurisdictions.* | coordinated capture; registry coercion | not modelled; generalises the capstone's cases from 2 channels to *n* |
| **T4: long-term validity** | revocation status captured after the anchor (LTV-style, RFC 5126 / ETSI EN 319 102-1); the archived trust-anchor store bound into the bundle; evidence-record renewal (RFC 4998); compromise time via invalidity date (RFC 5280) | *Revocation at or before the anchor is caught, and the receipt still verifies in 2106.* | stale-status replay (freshness bound); hash or signature algorithm ageing | P6 is right as a rule, but **missing a carrier** (G-27); not modelled |

**Across all tiers: the adjudicator's residual (option A).** A key compromise discovered after the window
(stolen in March, revoked in June) does not change the verifier's verdict (R-5.22). An adjudicator must be told
that such evidence can exist and how to weigh it. The verdict is mechanical; the judgement is not.

## Authority capture: out of scope to prevent, in scope to make visible (added 2026-10-08)

The author, 2026-10-08: *"perhaps the right way to attack the problem is distribution and admission that
governance changes are out of scope"*, and *"Authority capture must be visible in such instances. For an
adjudicator to be convinced incorrectly requires the takeover be invisible."*

**Out of scope.** Stopping a captured or merged authority from issuing new attestations under its own keys.
Jurisdictions can merge; a single authority can emerge. Distribution (T3) makes capture costly and unlikely,
but cannot rule it out.

**In scope, after capture.** "Capture" here means disclosed authority-channel credentials while honest
signing keys stay secret (the capstone's cases (c) and (d)). Under it, the capstone's case-(c)/(d) companions
test that a captor cannot:
- reattribute an honest party's existing frames;
- alter an honest signer set;
- carry an honest signature onto other bytes or keys.

Separately, the temporal-anchor models (P5/P6, TLA+), under their own assumptions, are meant to stop anything
being backdated into the time before the capture. The capstone runs do not test that.

**In scope: making capture visible.** The record already splits this two ways (Band 1 docket items 25–27,
including the author's earlier *"change of control for companies is generally visible"*):
- **Open capture**, such as governance change or legal change of control. *Often* visible, not visible by
  construction. Anchoring prevents backdating, but a governance change need not alter cryptographic
  continuity: new controllers can keep issuing under the same keys. Visibility then rests on public records
  outside Tessera, and on whatever the governance record (T3) captured at issuance.
- **Silent capture**, such as credential theft or an insider. It is invisible by default, because the captor
  issues under the legitimate key.
  - The record has three candidate mechanisms: fork legibility (item 25, the forward link, visible to any
    holder of both successors), third-party log buildability (item 27, *"the design is a floor, not a
    ceiling"*), and bounded key lifetimes (item 26).
  - **No symbolic model leaks the issuer key**, so this case is unmodelled.

**Governance diversity bounds; it does not guarantee** (the author, 2026-10-08: *"governments change,
boundaries change, rules change. Any adjudicator 80 years hence … just needs to be able to see that. What I
don't think we can do is guarantee it, we can only bound it."*). T3 therefore records the governance
structure **as it was at issuance**, in two parts:
- **Mechanically checkable.** The DNSSEC chain of trust (root → ccTLD → domain) proves which registries each
  channel's evidence ran through. The verifier can state and check: "forgery at issuance required at least m
  of these n channels, through these jurisdictions."
- **Declared.** Who held each registration, under which legal entity, signed and anchored at issuance. This
  is a contemporaneous claim for the adjudicator to weigh, not a verifier input.

**Diversity is per layer** (author, 2026-10-09, correcting the owner: the author's domains *"do not present
jurisdictional diversity … there is registrar diversity"*). A domain's authority passes through four layers, and
an attacker needs only the weakest. The governance record must state each layer, and "m of n" is meaningful per
layer:

| Layer | What it controls | Example (the author's five domains, 2026-10-09) |
|---|---|---|
| Registry (TLD operator) | delegation and DS in the parent zone | several TLDs, one holder |
| Registrar (account) | nameservers, DS replacement or removal | diverse: GoDaddy, register.ca, Namecheap |
| DNS operator | zone signing, served keys | single: Cloudflare |
| Holder (person) | all of the above | single |

T3's claim: *at issuance, compromise required at least m of n channels, through these recorded
jurisdictions, held by these declared parties. Whether they were in fact independent, and what happened to
them since, is the adjudicator's judgement from the record.*

**The claim this gives, as a target, not a result:** *under the stated capture model, pre-capture honest
material cannot be reattributed, re-membered or re-bound, and backdating is excluded under the anchor's
assumptions. Post-capture misdirection requires the capture to be unnoticed by any surviving holder of the
honest lineage* (A3's survivability floor: "visible failure while an observer possessing the relevant state
survives"). Preserved evidence still has availability and interpretation limits (A3 §A3.4). This draft is
**not** part of the Amendment 8 approval. Its proposed deferral of T3/T4 obligations past Band 0 must be
reconciled with existing commitments before any adoption.

## The freshness rule, per tier

- **T1:** status evidence must be no staler than one bound F relative to `anchor_time`. In practice F is the
  channel's RRSIG validity window, which is weak.
- **T3:** at least *m* of *n* channels must be fresh within F. Key lifetimes cap F from above.
- **T4:** the captured status is itself anchored, so its own time is evidenced, not asserted.

## What this could mean for Band 0 (a proposal; the scope decision is the author's)

- **Band 0 verifies T0–T2 completely.** That is most of what exists: the capstone is T2's composition. P8 is
  the real gap at T0, and G-17 and G-21 are spec fixes at T1/T2.
- **T3 and T4 are registered as layered claims**, each with its own model obligation (the attacker-plus-time
  revocation model, an *m*-of-*n* generalisation of the capstone's cases), done after Band 0. They are not
  conditions of Band 0's exit.
- **Commercially,** tiers can be offered separately, or all of them implemented to show what is possible.

## Open questions in this draft

1. Is T1 with git alone a real tier, or does git only ever count alongside DNS?
2. Where does standing (the terminal lineage record) sit: T2 or T4?
3. Does T0 need any revocation story, or are short-lived keys plus "nothing about who K is" enough?
