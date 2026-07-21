# Project Tessera

An AWS-native attestation service, built as a public demonstration of
principled engineering with AI as collaborator rather than substitute.

The primary objective is not the product alone. It is evidence that a
senior engineer can close a real knowledge gap quickly—using AI for
mechanics while owning architecture, judgment, and every decision that
must be defended cold. The secondary objective is commercial viability
as attestation-as-a-service; that upside is measured separately and is
not allowed to expand the demonstration’s scope.

**Credibility line (non-negotiable):** AI here contributes mechanics,
pushback, and rigor — drafting, modeling, adversarial review, even
recommendations. What it never contributes is ownership: every
load-bearing decision is read cold by the author, ratified or
overridden, and defensible by the author without the AI in the room.
Anything less proves the deskilling failure mode this project exists
to refuse.

Tony Mason  
Initiated 10 June 2026  
This README reflects the repository as of July 2026 (Band 0 — the formal foundation, H0).

---

## What this repository is

Tessera provides a neutral third party’s cryptographic binding to a
package of information at a fixed point in time. Attestation here means:
*this is what was presented in a bundle*, tied to a temporal anchor that
cannot be trivially regenerated. It does not by itself vouch for the
authenticity or truth of the contents; those guarantees, if any, ride in
the package.

The service is a cousin of [Willay](https://github.com/fsgeek/willay):
shared cryptographic and modeling ethos, forked edges for cloud-native
operation (KMS, S3 Object Lock, queues, observability, IaC).

The method is as load-bearing as the artifact:

1. **Pre-registration** — objectives, hypotheses, properties, and success
   criteria are written, signed, and OpenTimestamps-anchored *before*
   outcomes are known. The journal is measured against that record,
   including honest divergence.
2. **Formal foundation first (Band 0 / H0)** — machine-checked models of
   the core guarantees gate later code. No Phase 1 until the foundation
   holds or is amended on the record.
3. **Public, falsifiable process** — multi-round adversarial review,
   broken companions that must go red, named residuals, and a living
   property tracker. Theater is a failure mode, not a feature.

---

## Current status (July 2026)

| Layer | Status |
|-------|--------|
| Phase 0 pre-registration | Signed and amended (Amendment 1 in force; Amendment 2 draft through two non-author review rounds, sign-blocked on one author ruling — clock precedence) |
| Band 0 formal models | Active — TLA+ (P4, P5/P6, P5c issuance, bridge), ProVerif spike; see `formal/` |
| Cloud-independent crypto core | Not yet frozen (gated on Band 0) |
| LocalStack / AWS vertical slice | Not started |
| Application code | Minimal scaffolding only |

We are deliberately early in product code and late in protocol precision.
That ordering is intentional.

---

## How to read this repository

Recommended order for a new reader (human or collaborator instance):

1. **This file** — orientation and credibility line.
2. [`docs/phase-0-prereg.md`](docs/phase-0-prereg.md) — the signed intent
   and ranked objectives.
3. [`docs/phase-0-prereg-amendment-1.md`](docs/phase-0-prereg-amendment-1.md)
   — property list, adversary model, temporal-anchor semantics, agreement
   gate as falsification task.
4. [`docs/phase-0-prereg-amendment-2.md`](docs/phase-0-prereg-amendment-2.md)
   — draft refinement of confirmation, refusal, and anchor standing
   (status may still be DRAFT; check the header).
5. [`docs/tessera-cloud-demo-spec.md`](docs/tessera-cloud-demo-spec.md) —
   demonstration architecture and capability map.
6. [`docs/travelog.md`](docs/travelog.md) — contemporaneous journal of
   reality against the pre-registration.
7. [`formal/PROPERTIES.md`](formal/PROPERTIES.md) and `formal/tla/` —
   discharge status and the models themselves.
8. [`docs/reviews/`](docs/reviews/) — adversarial review artifacts and
   dispositions.

If the tracker and an amendment disagree, the **amendment wins**.

---

## Disciplines this repository enforces

- **GPG-signed commits** (author identity — *who*).
- **OpenTimestamps anchors** on commits (existence in time — *when*).
  These are two mechanisms; both are required for the public record.
- **Amend, do not silently rewrite** historical pre-registration
  documents.
- **AI as collaborator for mechanics and pushback; author owns all
  decisions** (division of labor is explicit in the pre-registration).
- **Falsification-style review** before load-bearing text is signed
  (see Amendment 1 §A1.7 and the review archive).

Setup for local hooks and OTS tooling lives under `scripts/` (see
`scripts/install-hooks.sh`).

---

## What this is not

- Not a highlight reel. Pre-registration exists so success and failure
  are both legible.
- Not formal-methods theater. Models state what they prove, what they
  assume, and what remains unclaimed (especially liveness vs. safety).
- Not an unbounded product fantasy. Commercial upside is secondary and
  deliberately constrained.

---

## License and contact

See repository metadata and commit history for authorship. The public
record of the work is the git history: signed, timestamped, and open to
scrutiny.

For the living narrative of how the work actually felt and where it
diverged from plan, start with the travelog.
