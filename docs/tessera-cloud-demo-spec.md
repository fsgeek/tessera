# Willay-Cloud — Demonstration Project Spec

*(Working name "Willay-Cloud" — it's a cousin, not Willay; rename to your own.)*

## Objective

Two objectives, ranked.

1. **Primary (the demonstration).** Ship a real, security-first, cloud-native attestation service that exercises the AWS-native / SRE / observability cluster end-to-end — and *document the build as a learning loop* so the artifact proves the rare thing: a senior engineer closing a knowledge gap fast, using AI for mechanics while owning the architecture. The demonstration is for the people who can read work (a hiring manager, a CEO), not the ATS.
2. **Secondary (upside, not premise).** If it yields a viable commercial attestation-as-a-service, good. Validate who pays *separately and cheaply* before building any billing/customer infrastructure. Do not let the product dream expand the scope.

**Credibility line (non-negotiable):** every architecture decision is yours to own and defend cold. AI accelerates the typing, not the judgment. A reviewer who probes the design must find decisions you can justify, not config you can't explain — otherwise the demo proves the *deskilling* failure mode, not the healthy one.

## Capability-map rows this converts (Bridge/Gap → Direct)

ECS/Fargate · KMS · CloudTrail · GuardDuty/Security Hub · S3 Object Lock · the observability stack (OpenTelemetry/Prometheus/Grafana) · SLOs / error budgets / load testing / graceful degradation · CDK/Terraform IaC (reinforce) · FinOps (real cost governance). Reinforces existing Direct rows: Lambda, SQS, DynamoDB, security architecture, instrumentation.

## Architecture — shared core, forked edges

**Shared core (reuse from Willay unchanged, cloud-agnostic):** `canonical.py` (deterministic JSON + SHA-256), signing/verify (WHO layer), `models.py`, evaluators (retrieval-integrity, authority, composite, meta), ledger hash-chain logic, resolvers. This keeps most of the code real and tested, and keeps the cousin honestly *derived from* Willay.

**Forked edges (new, cloud-native):**

| Concern | Edge | Local | Real cloud |
|---|---|---|---|
| API / compute | FastAPI service, containerized | docker-compose | ECS/Fargate |
| Signing key | KMS-native asymmetric signing *(design fork — see below)* | LocalStack KMS | KMS |
| Ledger + bundles (immutable) | Append-only object store | LocalStack S3 | **S3 Object Lock** (WORM/compliance) |
| Receipt index / chain head | Key-value | DynamoDB Local | DynamoDB |
| Pipeline (resolve→evaluate→sign→anchor) | Async queue + workers | elasticmq / LocalStack | SQS + Lambda |
| Infra audit | — | (skip locally) | CloudTrail |
| Threat / posture | — | (skip locally) | GuardDuty, Security Hub |
| Observability | OTel traces/metrics, structured logs | Prometheus + Grafana + Jaeger (compose) | CloudWatch + OTel collector |
| IaC | Terraform modules, one definition both targets | `tflocal` against LocalStack | `terraform apply` to AWS |

**Design fork to decide (yours):** canonical Willay signs with GPG and pins a fingerprint so receipts verify with *no infrastructure* — that ethos stays in Willay. The cousin's job is to exercise cloud-native services, so KMS-native asymmetric signing is the legitimate choice here, accepting that verification now needs the KMS public key. Record the decision and its tradeoff in the journal; it's exactly the kind of judgment call the demonstration is about.

## Non-functional emphases

- **Security:** KMS key custody; IAM least-privilege per component; the product *is* security (signed, tamper-evident receipts); GuardDuty + Security Hub + CloudTrail enabled in the cloud window; secrets never in repo; dependency + IaC scanning (tfsec/checkov) gated in CI; signed commits.
- **Reliability:** idempotent pipeline stages; SQS retries + dead-letter queue; **graceful degradation** when OTS/Bitcoin anchoring or external resolvers lag (the OTS confirmation delay is a natural, honest degradation scenario to design for); hash-chain integrity check on read; immutable ledger.
- **Observability:** OpenTelemetry traces across the full resolve→evaluate→sign→anchor span; structured logs; metrics; defined **SLOs + error budget** (e.g., receipt-issue p99 latency, verify availability); reuse Willay's `self_assessment` evaluator as app-level observability.
- **Scalability:** stateless API (scale out on Fargate); queue-decoupled pipeline; S3/DynamoDB scale natively. Demonstrated by *architecture + a load test*, not by actually running at scale (cost). Be explicit that this is a design+load-test claim, not a production-traffic claim.
- **Usability:** one-command local bring-up (`docker-compose up`); clean CLI + API; portable receipt bundles that verify standalone; clear README. Usability is the ethos you already hold — keep it.

## Engineering discipline

- **Repo:** single repo; shared core as an installable package, edges alongside; `docs/blueprint.md`-style state file (you already do this in Willay).
- **CI/CD (GitHub Actions):** lint, type-check, unit + integration tests (LocalStack via testcontainers), container build, `terraform validate`/`plan`, security scans (deps + IaC), and on tag → deploy. Green CI required to merge.
- **Commit signing:** GPG-signed commits required (you're GPG-fluent and it's thematically apt; gitsign/sigstore is the keyless alternative if you want to demonstrate breadth). Branch protection: signed commits + passing CI + review.
- **PR discipline:** PR-per-feature with CI gates and a self-review checklist (solo project — be honest that approval is self, but the gates and history still demonstrate the practice).
- **Issue tracking:** GitHub Issues + a project board.
- **Pre-registration (your ethos):** Phase 0 writes the objective, the hypotheses (e.g., "vertical slice deployable to real AWS in N days; AI for mechanics, me for architecture"), the success criteria, and the capability-map rows targeted — *before* building. The journal then records reality against the pre-registration, including where it diverged. That's what makes it a demonstration and not a highlight reel.

## Local-first, and the honest boundary

Everything runs locally on LocalStack + docker-compose at ~$0 until real cloud is genuinely required. **The things that actually need real cloud (the honest impediments):** ECS/Fargate runtime behavior, GuardDuty, Security Hub, S3 Object Lock *compliance-mode* semantics, real CloudTrail, and real OTS/Bitcoin anchoring. LocalStack community covers S3/SQS/Lambda/DynamoDB/KMS/IAM well; treats the above as partial-or-absent. So: build and prove the whole pipeline locally, then a *time-boxed* cloud window validates only what can't be faked.

## Cost profile

Dev: ~$0 (LocalStack community + local Docker). Cloud window: minimal Fargate task, on-demand DynamoDB, S3, Lambda, SQS — pennies to low single digits; GuardDuty/Security Hub accrue per-event/per-check, so enable them briefly to capture config + evidence, then disable. **`terraform apply` to bring the demo up, `terraform destroy` to tear it down** — cloud cost accrues only during active demonstration. Disciplined target: under ~$25 total, plausibly under $10.

## Phasing (weeks, not months — speed is half the claim)

- **Phase 0 — Pre-register (≈1 day):** objective, protocol, success criteria, targeted rows. Start the dated journal.
- **Phase 1 — Local vertical slice (≈1–2 weeks):** shared core + FastAPI + LocalStack (S3/DynamoDB/SQS/Lambda/KMS) + Terraform-via-tflocal + CI + signed commits + local observability. End-to-end: issue a receipt, verify it, chain it — all local.
- **Phase 2 — Cloud cutover (≈1 week, time-boxed):** same Terraform → real AWS; Fargate, KMS, S3 Object Lock, CloudWatch/OTel, GuardDuty/Security Hub/CloudTrail enabled; run a load test; capture one real degradation/incident and its resolution. Tear down.
- **Phase 3 — Narrate (≈1–2 days):** clean the journal into the demonstration artifact; flip the capability-map rows to Direct; write the short "how I closed this gap" summary you'd actually send a human.

## Definition of done

End-to-end receipt issue + verify in real AWS; all five NFRs evidenced; CI green with signed commits; load test + one documented degradation handled; `destroy`/`apply` repeatability proven (cost control demonstrated); journal complete and honest about where AI helped vs. produced garbage you caught; capability-map rows converted; a one-page human-readable writeup of the learning loop.

---

*Right-sizing note: the documentation layer is a dated markdown journal, not an attestation system. The cleverness goes in the service, not the log.*
