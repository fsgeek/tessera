# Tessera Trust Marketplace

## Business Plan for a Value-Added Attestation Clearinghouse

Prepared for: Tony Mason  
Date: June 13, 2026  
Status: Defensible business-plan draft, not legal, accounting, tax, or investment advice  
Version: Marketplace revision

> **Core recommendation**  
> Build Tessera as a trust marketplace and attestation clearinghouse. Keep commodity timestamping free or near-free as the acquisition, trust, and artifact-registration substrate. Monetize the higher-value layer: independent third-party attestations, review reports, citation validations, AI-governance evidence packages, compliance-control attestations, semantic re-attestations, and enterprise/private clearinghouse workflows.

## Table of contents

1. Executive summary
2. Strategic correction: free timestamping is the substrate, not the business
3. The marketplace thesis
4. Product architecture: from receipts to claim graph
5. Initial wedge markets
6. Paid attestation categories
7. Marketplace participants and incentives
8. Revenue model
9. Pricing hypotheses
10. Launch sequence and cold-start strategy
11. Trust governance and validator quality
12. Technical architecture for the clearinghouse
13. Legal and regulatory posture
14. Competitive landscape
15. Go-to-market plan
16. Financial model and unit economics
17. Metrics, validation gates, and kill criteria
18. Risk register
19. Strategic conclusion
20. Appendices

# 1. Executive summary

## Recommendation

The most likely profitable model is not **timestamping as a service**. That should be the free tier and public-good layer. The defensible business is **Tessera as a clearinghouse for value-added attestations**: a place where a digital artifact can accumulate independently verifiable claims made by third parties.

In this model, a Tessera receipt is not merely a proof that some bytes existed at a time. It is the root of a durable claim graph:

- the artifact existed at time T;
- a named evaluator reviewed it under a declared scope;
- a citation was independently checked against its source;
- a report was issued about a document;
- an AI-governance package was reviewed against a published policy;
- a later wrapper re-anchored or re-attested the earlier object.

The preregistration already contains this opening: it identifies third-party findings such as audits, regulatory policies, ontologies, and citations as core attestation use cases, and it insists that receipts remain verifiable independently of the attestor. That combination is exactly the foundation for a marketplace: Tessera should standardize and preserve the **evidence envelope** around third-party claims, not try to make money from the commodity act of hashing a file. [S1]

## Commercial thesis

Tessera should become the neutral infrastructure where independent reviewers, validators, auditors, researchers, expert witnesses, and compliance specialists can sell attestations about digital artifacts. Tessera's commercial role is to:

1. register artifacts through free or low-cost timestamping;
2. standardize the schema for paid attestations;
3. verify and classify evaluator identities and credentials;
4. route requests to appropriate validators;
5. preserve the resulting evidence packages in a durable, offline-verifiable format;
6. support relying parties who need to understand what was attested, by whom, under what methodology, and with what limitations.

The marketplace model has stronger profit potential than raw attestation because it captures value from professional judgment, not from commodity compute. It also creates network effects: more artifacts attract validators, more validators attract buyers, and more relying-party recognition makes the Tessera receipt a more valuable place to attach claims.

## Best first wedge

The recommended first wedge is **validated citation and independent review attestations for high-stakes technical, legal, AI-governance, and compliance documents**.

This wedge is attractive because it is narrow enough to standardize, painful enough to pay for, and compatible with the existing Tessera ethos. Citation validation is an especially good first product because AI-assisted writing, expert reports, policy documents, and compliance reports increasingly contain references that need independent checking. A paid attestation saying "this citation exists, was checked, and supports this exact claim within these limits" is much more valuable than a free timestamp.

## Business model summary

| Layer | User-visible offer | Revenue role |
|---|---|---|
| Free timestamping | Create a receipt for an artifact; verify offline; optionally publish a public record | Acquisition, trust, standardization, artifact registration |
| Paid validation marketplace | Buy independent citation checks, document reviews, AI-governance reviews, compliance attestations, forensic reviews | Transaction fees, platform fees, escrow/settlement margin |
| Evidence Vault | Team workspace, private artifact registry, API, audit trail, validator routing, templates | Recurring SaaS revenue |
| Validator network | Credentialed third-party reviewers with schemas, work queues, reputation records, and payout tools | Supply-side liquidity; listing/verification fees where appropriate |
| Enterprise/private clearinghouse | Private marketplace for internal/external reviewers; custom schemas; integration with GRC, legal, AI-governance, or knowledge-management systems | High-value annual contracts and services |
| Lifecycle services | Wrapping, re-anchoring, post-quantum upgrades, semantic re-attestation | High-margin long-term trust maintenance |

## Why this is defensible

OpenTimestamps already provides independently verifiable timestamp proofs, C2PA provides a standard for media provenance, and Sigstore/Rekor plus GitHub artifact attestations cover important software-supply-chain provenance use cases. [S2-S5] Tessera should not compete by saying "we also timestamp things." It should compete by saying:

> **Tessera is where independently verifiable third-party claims about digital artifacts are requested, produced, preserved, and later checked.**

That is a higher-value category. It combines cryptographic evidence, human or organizational judgment, repeatable review methods, marketplace liquidity, and long-term verification.

# 2. Strategic correction: free timestamping is the substrate, not the business

The corrected model is:

> **Free timestamping creates the artifact identity. Paid attestations create the business.**

This distinction is essential. A free timestamped receipt solves only the question, "Did these bytes exist before this time?" That is valuable, but not enough for most paying customers. A paying customer usually needs one of the following:

- Did this citation actually support the claim made in the document?
- Did a competent third party review this report?
- Did the reviewer disclose the scope, methodology, and limitations of the review?
- Did an AI-governance artifact exist before deployment or publication?
- Did the organization preserve the evidence that it followed a policy?
- Did the document later receive a correction, qualification, or superseding review?
- Can a court, regulator, auditor, publisher, partner, or customer verify the record without depending on Tessera's continued operation?

The free tier should therefore be designed as an intake funnel and public trust layer. Every free receipt should make it easy to request a paid attestation, attach a third-party report, invite a reviewer, or place the artifact into a private Evidence Vault.

## What the free tier should include

The free tier should include enough capability to make Tessera receipts familiar and trusted:

- create a cryptographic receipt for a digital artifact or claim package;
- include hash, canonicalization version, timestamp evidence, and signer metadata;
- allow offline verification through an open verifier;
- optionally create a public artifact page that reveals only metadata chosen by the issuer;
- expose a "request independent attestation" action;
- expose a "attach reviewer report" action;
- expose a "validate citations" action.

The free tier should not include the labor-intensive or liability-bearing parts of the business: professional review, evaluator credentialing, conflict checks, private workrooms, enterprise workflow, escrow, review templates, advanced search, or organizational audit trails.

## Why free timestamping helps the marketplace

The free tier solves the cold-start problem on the demand side. It lets Tessera accumulate artifact registrations before there is a large validator network. Those registrations become latent demand. An artifact can later receive paid attestations without being re-created or re-uploaded. The free receipt becomes the stable object around which paid claims accumulate.

In marketplace terms, the timestamped receipt is the SKU identifier. The paid validator's claim is the transaction.

# 3. The marketplace thesis

## Marketplaces are viable here because the problem is not only technical

A commodity timestamp service has weak pricing power because the primitive can be reproduced. A clearinghouse has stronger pricing power because it coordinates scarce professional judgment. The hard part is not signing bytes. The hard part is answering:

- Who is qualified to make this kind of claim?
- What exactly did they review?
- What procedure did they follow?
- Were conflicts disclosed?
- What did the claim not cover?
- Can the result be verified years later?
- Can a relying party compare attestations across validators?

Tessera can standardize those answers.

## The claim graph

The core product concept should be a **claim graph** anchored to digital artifacts. Each node is an artifact, claim, report, policy, citation, evaluator identity, or wrapper. Each edge is an attestation: a signed, timestamped statement that one node bears a specified relationship to another.

Examples:

- `Document D cites Source S for Claim C.`
- `Validator V checked Citation X under Citation Validation Method v1.1.`
- `Reviewer R reviewed Document D under Scope S and issued Report P.`
- `Enterprise E approved AI model release package M under Policy P.`
- `Wrapper W re-anchors Receipt R under Algorithm A at Time T.`

A marketplace emerges when third parties are paid to create high-quality edges in this graph.

## Network effects

Tessera can develop several reinforcing network effects:

| Network effect | Mechanism | Strategic value |
|---|---|---|
| Artifact density | More free receipts create more objects that can later receive paid attestations | Reduces acquisition cost for paid services |
| Validator liquidity | More validators make it easier to find credible reviewers across domains | Increases buyer confidence and category coverage |
| Schema standardization | More paid attestations reuse Tessera methods and templates | Makes outputs more comparable and easier to trust |
| Reputation records | Validators accumulate verifiable histories of scoped reviews | Creates supply-side differentiation and retention |
| Relying-party recognition | Courts, auditors, regulators, journals, customers, and partners become familiar with Tessera receipts | Increases willingness to pay for Tessera-attested artifacts |
| Lifecycle lock-in without data lock-in | The verifier remains open, but the accumulated claim graph stays useful | Builds durable business value while preserving credibility |

The last point matters. Tessera should avoid dark-pattern lock-in. Its trust promise requires offline verification. The business moat should come from accumulated standardized claims, validator relationships, reputation records, and workflow convenience, not from trapping users' evidence.

# 4. Product architecture: from receipts to claim graph

## The receipt

The receipt is the cryptographic root. It identifies the artifact, records canonicalization and signature metadata, and supports independent verification. This is the layer protected by the preregistration's hard invariants: canonicalization is frozen and versioned, and verification must depend on zero service-side state. [S1]

## The attestation

An attestation is a signed claim about an artifact, another claim, a reviewer, a source, a process, or a wrapper. It should be explicit about:

- claim type;
- subject artifact or prior attestation;
- claimant identity;
- evaluator credentials or organization;
- scope;
- method;
- evidence considered;
- evidence excluded;
- limitations;
- conflict disclosures;
- result;
- confidence or disposition;
- timestamp;
- expiry, review-by date, or supersession policy where applicable.

## The review package

A review package is the commercial deliverable. It contains the human-readable report, machine-readable attestation, supporting evidence index, verification instructions, and limitation statement.

For example, a citation validation package might include:

- the original document hash;
- the citation location;
- the cited source hash, archive URL, DOI, case citation, statute, or other locator;
- a statement of whether the source exists;
- a statement of whether the cited source supports the exact claim;
- any qualifications;
- reviewer identity and method;
- timestamped signed attestation.

## The marketplace workroom

A marketplace workroom is where the buyer and validator interact. It should support:

- artifact intake;
- confidentiality controls;
- scoping template;
- quote and fee;
- conflict check;
- reviewer assignment;
- evidence upload;
- draft report;
- buyer comments limited to factual correction or scope clarification;
- final signed attestation;
- append-only correction or supersession.

The workroom is not the source of truth for verification. It is the workflow system. The final receipt and attestation package must remain independently verifiable.

## The public or private artifact page

Tessera can provide optional artifact pages. These pages should display only what the issuer chooses to disclose, but they should always distinguish:

- public metadata;
- private evidence;
- verified claims;
- pending requests;
- disputed or superseded claims;
- method versions;
- validator identities and credentials where disclosure is permitted.

# 5. Initial wedge markets

## 5.1 Citation validation for high-stakes documents

This is the best first paid marketplace wedge.

### Buyer pain

AI-assisted drafting, expert reports, legal memoranda, policy documents, grant applications, academic manuscripts, and compliance reports all depend on citations. Incorrect citations create reputational, legal, academic, and business risk. A timestamp proves that the document existed; it does not prove that the citations support the claims.

### Tessera offer

**Tessera Citation Validation** lets a buyer submit a document and request independent validation of selected citations. The output is a signed attestation saying which citations were checked, which claims were supported, which were unsupported, and which require qualification.

### Why it is commercially attractive

Citation validation is:

- concrete and understandable;
- repeatable enough to standardize;
- narrow enough to limit liability;
- valuable for AI-era credibility;
- easy to attach to a document receipt;
- capable of generating many small transactions;
- a strong lead generator for larger document-review and expert-evidence packages.

### First customers

- expert witnesses;
- law firms;
- policy consultancies;
- academic authors;
- technical publishers;
- AI vendors publishing white papers or model evaluations;
- compliance and security teams publishing customer-facing trust documents.

## 5.2 Independent document review and report attestation

The next wedge is document-level review. The buyer wants a third party to review a report, policy, disclosure, model card, expert declaration, research preregistration, or compliance artifact and produce a signed, timestamped report.

The commercial deliverable is not "approved" or "certified" unless the reviewer is actually empowered to certify under a recognized standard. The safer offer is:

> **This document was independently reviewed by X under scope Y, using method Z, and Report R was issued on date T.**

That framing is honest and valuable. It avoids false regulatory implications while preserving the evidentiary benefit.

## 5.3 AI-governance evidence

AI governance is a strong wedge because obligations and scrutiny are increasing. The European Commission states that AI Act Article 50 transparency obligations related to marking, detection, and labelling of AI-generated content apply from August 2, 2026, and the Commission published a related Code of Practice on June 10, 2026. [S6]

Tessera should not position itself as an AI Act compliance oracle. It should position itself as evidence infrastructure for the artifacts organizations need when they claim to have followed a governance process:

- model cards;
- system cards;
- prompts or prompt classes;
- evaluation results;
- red-team reports;
- deployment approvals;
- human review records;
- transparency labels;
- C2PA manifests;
- policy exceptions;
- incident reviews;
- post-deployment monitoring summaries.

A paid reviewer can attest that a package was reviewed against a specific declared policy. Tessera preserves the package and the review result.

## 5.4 Legal, expert-witness, and forensic evidence

Legal and expert-witness work is attractive because the buyer already understands evidentiary value. The Canada Evidence Act places the burden of proving authenticity on a party seeking to admit an electronic document, and it addresses integrity of the electronic documents system for best-evidence purposes. [S8]

Tessera should not claim to make evidence admissible or true. It can help produce a stronger evidentiary record:

- what bytes were reviewed;
- when they existed;
- which expert or third party reviewed them;
- what report was produced;
- what was excluded;
- how a future opposing expert can verify the record.

This is a natural fit for founder-led consulting and early high-ticket proof packs.

## 5.5 Compliance and audit evidence

Compliance teams continuously produce evidence: control screenshots, access reviews, exception approvals, incident reports, risk acceptances, vendor reviews, vulnerability remediation records, policy sign-offs, and board materials.

Tessera's role is to preserve third-party or internal attestations around these artifacts. It can integrate with GRC platforms later, but it should not begin by trying to replace them. The wedge is durable evidence for the handful of artifacts that matter most in an audit, incident, dispute, or customer review.

# 6. Paid attestation categories

## Category 0: Free existence receipt

**Claim:** Artifact A existed before time T and can be verified through receipt R.  
**Price:** Free or near-free.  
**Purpose:** Acquisition, artifact identity, public trust, future paid attachment point.

## Category 1: Citation validation attestation

**Claim:** Citation C in Document D was checked by Validator V under Method M; the cited source supports, partially supports, does not support, or could not be resolved for Claim Q.  
**Price hypothesis:** $5-$25 per citation for simple checks; $150-$750 for small bundles; higher for legal, scientific, or technical claims.  
**Best early use:** AI-written reports, expert reports, policy documents, academic drafts.

## Category 2: Source existence and archival attestation

**Claim:** Source S exists at location L, was retrieved at time T, and a hash/archive reference was captured.  
**Price hypothesis:** $2-$10 per source at volume; $100-$500 for small packages.  
**Best early use:** anti-link-rot packages for reports and briefs.

## Category 3: Independent document review attestation

**Claim:** Reviewer R reviewed Document D under Scope S and issued Report P with Findings F and Limitations L.  
**Price hypothesis:** $1,500-$7,500 for ordinary technical review; $10,000-$50,000 for high-stakes legal, forensic, or regulated review.  
**Best early use:** expert reports, technical white papers, model cards, security claims.

## Category 4: AI-governance evidence attestation

**Claim:** Reviewer R reviewed AI Evidence Package E against Policy P or Checklist C and issued Report P2.  
**Price hypothesis:** $3,000-$25,000 depending on model/system criticality and review depth.  
**Best early use:** model releases, customer-facing AI trust reports, transparency evidence.

## Category 5: Compliance-control evidence attestation

**Claim:** Control artifact A was reviewed under Framework/Control C and Report R was issued.  
**Price hypothesis:** $1,000-$10,000 for selected control packages; enterprise subscriptions for ongoing workflows.  
**Best early use:** security questionnaires, SOC 2 evidence readiness, vendor trust packages.

## Category 6: Semantic re-attestation

**Claim:** A prior artifact or report was re-reviewed under a new context, method, or standard; Report R2 supersedes, qualifies, or extends prior Report R1.  
**Price hypothesis:** premium professional-service pricing.  
**Best early use:** long-lived reports, policies, litigation materials, post-quantum or standards migration.

## Category 7: Cryptographic wrapper / lifecycle attestation

**Claim:** Prior receipt R is bit-for-bit unchanged and has been re-anchored under a new key, signature algorithm, or time anchor.  
**Price hypothesis:** low to medium fixed fee for simple wrappers; premium for high-value archives.  
**Best early use:** long-term preservation, post-quantum transition, regulated archives.

# 7. Marketplace participants and incentives

## Buyers

Buyers pay because they want a claim to be more credible to someone else. They include:

- authors and publishers;
- expert witnesses;
- lawyers and litigation support teams;
- AI governance teams;
- compliance teams;
- security teams;
- research groups;
- policy organizations;
- vendors responding to due diligence;
- organizations producing public trust reports.

Their incentive is reduced credibility friction. Tessera helps them say, "Do not take only our word for this. Here is the artifact, the independent review, the scope, the limitation statement, and the verification path."

## Validators

Validators are the supply side. They include:

- research librarians;
- subject-matter experts;
- digital forensic specialists;
- auditors;
- compliance consultants;
- AI-governance reviewers;
- security reviewers;
- technical editors;
- domain-specific professional reviewers.

Their incentive is paid work, visible reputation, standardized evidence packaging, lower client acquisition cost, and a durable record of the work they performed.

## Relying parties

Relying parties may not pay at first, but they create demand. They include:

- courts;
- opposing experts;
- regulators;
- auditors;
- customers;
- investors;
- journals;
- standards bodies;
- procurement teams;
- public readers.

Their incentive is interpretability. They need to know what was actually attested and what was not.

## Tessera

Tessera earns revenue by coordinating trust, not by dictating truth. It should remain neutral among outcomes. A negative or qualified review is a valid marketplace output. Validators should be paid for review work, not for producing favorable findings.

This principle is essential. Without it, Tessera risks becoming a paid rubber-stamp marketplace. With it, Tessera can become a trusted venue for independent evidence.

# 8. Revenue model

## 8.1 Free tier

Free timestamping should be explicit and intentional.

Revenue role:

- acquire users;
- create artifact identities;
- establish public verifier trust;
- seed future paid attestation demand;
- build familiarity with Tessera receipts;
- support the credibility promise that verification is not a paywalled service.

Potential limits:

- rate limits;
- abuse controls;
- metadata-only public pages;
- basic support only;
- no professional review;
- no private workrooms beyond a small personal quota.

## 8.2 Marketplace transaction fees

Tessera should take a percentage of paid validator transactions. Early take-rate hypothesis: **15%-25%**, with lower negotiated rates for very large engagements.

What the fee covers:

- buyer discovery;
- validator onboarding;
- standardized scopes;
- workroom workflow;
- escrow or payment coordination;
- final receipt generation;
- dispute workflow;
- validator reputation record;
- long-term verification infrastructure.

## 8.3 Platform fee per attestation

For smaller transactions, a minimum platform fee may be better than a pure percentage. Example:

- $5-$25 platform fee for small citation packages;
- $50-$250 platform fee for document-review packages;
- custom fees for enterprise/private clearinghouses.

This prevents low-dollar checks from becoming unprofitable.

## 8.4 Evidence Vault subscriptions

Evidence Vault is the recurring SaaS layer.

Possible tiers:

| Tier | Price hypothesis | Included |
|---|---:|---|
| Individual | $15-$49/month | private receipts, small vault, citation requests, public verifier pages |
| Professional | $99-$249/month | branded artifact pages, templates, workrooms, client packages, API allowance |
| Team | $499-$1,500/month | team roles, private validators, review workflows, audit logs, policy templates |
| Enterprise | $25,000+/year | private clearinghouse, SSO, custom retention, GRC/legal/AI integrations, dedicated support |

These numbers are pricing hypotheses, not claims. The discovery process should test willingness to pay.

## 8.5 Validator credentialing and directory fees

Tessera can charge validators for identity and credential verification, but it must avoid pay-to-play trust inflation. A validator should not be able to buy credibility. Fees should be limited to costs and platform access, while quality signals come from verified credentials, completed work, dispute history, and peer or client references.

Possible fees:

- one-time identity and credential verification fee;
- annual directory maintenance fee;
- optional premium workflow tools;
- no ability to buy higher trust ranking.

## 8.6 Enterprise/private marketplace

Larger organizations may want their own clearinghouse:

- approved internal and external reviewers;
- custom review schemas;
- private artifact vault;
- legal hold and retention policies;
- procurement and vendor due-diligence workflows;
- AI-governance evidence flows;
- customer-facing trust portals.

This can support high-value annual contracts and implementation services.

## 8.7 Lifecycle services

Long-lived artifacts need maintenance:

- re-anchoring;
- algorithm migration;
- post-quantum wrappers;
- semantic re-review;
- superseding reports;
- archival export;
- expert explanation packages.

The preregistration already distinguishes integrity wrappers from semantic re-attestation and identifies semantic re-attestation as a separately priced service. [S1]

# 9. Pricing hypotheses

## Initial public pricing menu

| Offer | Buyer | Price hypothesis | Tessera revenue |
|---|---|---:|---:|
| Free receipt | Any user | Free | $0 |
| Citation validation - small bundle | Author, expert, student, analyst | $150-$750 | 20% or minimum platform fee |
| Citation validation - technical/legal bundle | Expert witness, law firm, policy team | $1,000-$5,000 | 15%-25% |
| Source archival package | Researcher, publisher, legal team | $100-$500 | 20% or platform fee |
| Independent document review | Expert, company, publisher | $1,500-$7,500 | 15%-25% |
| AI-governance evidence package | AI vendor or deployer | $3,000-$25,000 | 15%-25% or fixed enterprise fee |
| Compliance evidence package | Security/compliance team | $2,500-$15,000 | 15%-25% or subscription bundle |
| Expert/legal evidence package | Law firm, expert witness | $10,000-$50,000 | professional-service margin or referral/take rate |
| Private clearinghouse | Enterprise | $25,000-$150,000+/year | subscription + implementation |

## Pricing principles

1. **Price the risk reduced, not the hash generated.**
2. **Pay validators for independent work, not positive outcomes.**
3. **Use fixed scopes for small offerings.** Citation validation needs productized pricing.
4. **Use custom scoping for high-risk reviews.** Legal, AI-governance, and compliance reviews need bespoke limits.
5. **Separate Tessera's platform claim from the validator's substantive claim.** Tessera attests to workflow integrity and evidence preservation; validators attest to their findings.

# 10. Launch sequence and cold-start strategy

A two-sided marketplace has a cold-start problem. Tessera should not begin as an open marketplace. It should begin as a controlled clearinghouse with hand-selected validators and founder-led demand.

## Phase 0: Proof and credibility foundation

Do not sell before the core evidence promise is technically defensible. The preregistration's Band 0 formal foundation and hard invariants should remain gating constraints. [S1]

Commercial work during this phase:

- interview potential buyers;
- recruit potential validators;
- define attestation schemas;
- create sample verification packages;
- develop pricing hypotheses;
- publish the public verifier and sample receipts when ready.

## Phase 1: Concierge proof packs

Offer a manual service to a narrow set of trusted early customers:

- validated citation packs;
- independent document review packages;
- expert evidence packages;
- AI-governance evidence packages.

The goal is not automation. The goal is to learn which paid attestations buyers actually value, what scopes validators can perform reliably, and what proof package format relying parties understand.

## Phase 2: Curated validator bench

Recruit a small number of validators in specific categories:

- citation/source validators;
- AI-governance reviewers;
- compliance reviewers;
- digital evidence specialists;
- subject-matter experts.

Keep the directory private or invitation-only until quality controls are proven.

## Phase 3: Transactional marketplace

Add buyer request flows, quoting, workrooms, escrow or payment coordination, final attestation packaging, and dispute handling.

The first transactional category should likely be citation validation because it can be standardized more readily than complex professional review.

## Phase 4: Enterprise/private clearinghouses

Sell private instances or dedicated workspaces for organizations that want an internal/external reviewer network.

This is likely the highest-value recurring offer:

- private validators;
- custom schemas;
- SSO;
- audit logs;
- API;
- retention policies;
- SIEM/GRC/legal integrations;
- customer-facing trust pages.

# 11. Trust governance and validator quality

The clearinghouse lives or dies on validator trust.

## Validator onboarding

Validator onboarding should include:

- identity verification;
- credential review;
- domain classification;
- conflict-of-interest policy;
- sample work review;
- agreement to method templates;
- agreement to no-guaranteed-positive-results policy;
- agreement to append-only correction and supersession processes.

## Validator categories

Use clear categories rather than a single generic "verified" badge.

Examples:

- Verified Identity;
- Verified Credential;
- Domain Specialist;
- Licensed Professional, where applicable;
- Tessera Method Trained;
- Enterprise Approved;
- Independent of Requester;
- Conflict Disclosed;
- Conflict Cleared.

## Review method templates

Each paid attestation category should have a method template. A method template should define:

- scope;
- required evidence;
- optional evidence;
- exclusion language;
- acceptable outcomes;
- confidence language;
- reviewer qualifications;
- minimum report contents;
- machine-readable fields;
- correction/supersession process.

## Conflict handling

Every paid attestation should include a conflict statement:

- no known conflict;
- disclosed relationship;
- paid by requester, outcome-independent;
- reviewer declined due to conflict;
- conflict accepted by relying party, where appropriate.

For credibility, validators should be paid for the work regardless of whether the finding is favorable, unfavorable, or qualified.

## Disputes and corrections

Tessera should be append-only. If a report is wrong, the remedy is not deletion. The remedy is:

- correction attestation;
- superseding review;
- dispute marker;
- withdrawn-by-validator marker;
- invalidated-method marker;
- administrative fraud marker, in extreme cases.

This aligns with the underlying evidence philosophy: preserve the record, then add new facts.

## Reputation without popularity theater

A simple star-rating system would be inappropriate. Validator reputation should be based on structured evidence:

- completed attestations by category;
- dispute rate;
- correction rate;
- average turnaround time;
- scope compliance;
- credential status;
- repeat buyers;
- peer review where applicable;
- disciplinary actions or suspensions;
- public/private visibility settings.

# 12. Technical architecture for the clearinghouse

## 12.1 Core evidence layer

The core evidence layer should preserve Tessera's commitments:

- versioned canonicalization;
- signature-set receipts;
- timestamp anchoring;
- public verification independent of Tessera's liveness;
- wrapper model for lifecycle upgrades;
- zero service-side state on the verification path.

This is the credibility foundation. It is also what lets a marketplace avoid becoming just another SaaS database.

## 12.2 Marketplace application layer

The application layer can depend on service-side state because it is workflow, not verification. It includes:

- accounts;
- organizations;
- validator profiles;
- marketplace listings;
- request/quote/order flows;
- workrooms;
- permissions;
- private file storage;
- payment and payout state;
- audit logs;
- notifications;
- evidence package assembly.

The output of this layer must be a portable attestation package.

## 12.3 Privacy model

The marketplace must support sensitive materials. Public receipts should be hash-first and metadata-minimal. Private workrooms should support:

- encrypted storage;
- restricted validator access;
- access logs;
- redaction workflows;
- content-expiry policies;
- legal hold where needed;
- artifact export;
- hash-only public references.

## 12.4 Interoperability

Tessera should interoperate with existing systems rather than try to replace them.

- OpenTimestamps can remain a timestamp anchor or compatible proof format. [S2]
- C2PA manifests can be included as artifacts or evidence inside Tessera packages. [S3]
- Sigstore/Rekor or GitHub artifact attestations can be attached as software provenance evidence where relevant. [S4-S5]
- Qualified timestamp providers can be partners for customers requiring eIDAS qualified trust-service presumptions. [S7]
- S3 Object Lock or similar WORM storage can support operational retention where the managed vault is part of the service. [S11]

## 12.5 AI-assisted review tooling

AI can help validators work faster, but it should not be the attesting party unless the product explicitly offers machine-generated analysis. The safer model is:

> AI may assist review; the named validator attests to the final claim, method, scope, limitations, and use of AI assistance.

For citation validation, AI can help locate candidate sources and compare claims, but the validator should confirm the result and sign the attestation.

# 13. Legal and regulatory posture

## Not a notary by default

Tessera should avoid marketing itself as a notary unless it actually performs a legally recognized notarial function in the relevant jurisdiction. "Independent attestation clearinghouse" and "digital evidence marketplace" are safer terms.

## Not a qualified trust service by default

In the EU, eIDAS gives electronic timestamps legal effect and gives qualified electronic timestamps a presumption of date/time accuracy and data integrity. [S7] Tessera can support evidence workflows and may integrate with qualified timestamp providers, but it should not imply qualified trust-service status unless it obtains that status or partners with a qualified provider.

## Evidence support, not admissibility guarantee

In Canada, electronic-document authenticity and system integrity are legal concepts under the Canada Evidence Act. [S8] Tessera can help create evidence relevant to authenticity and integrity, but it should not promise admissibility, truth, or legal sufficiency. The correct language is:

> Tessera helps preserve and explain evidence of artifact identity, timing, review scope, and third-party findings. It does not prove that a document is true, lawful, complete, or admissible.

## Marketplace liability

The marketplace will need careful contracts:

- validator agreement;
- buyer terms;
- limitation of liability;
- confidentiality terms;
- intellectual-property terms;
- data processing terms;
- conflict disclosure terms;
- payment and refund policies;
- dispute process;
- insurance requirements for high-risk categories.

## Payments and regulated activity

If Tessera handles marketplace payments, it should use a payment processor and avoid holding funds in a way that creates unnecessary money-transmission risk. Early manual invoicing may be simpler. Later marketplace payments should use a platform product designed for split payments, onboarding, tax forms, and payouts.

## No outcome-guaranteed reviews

A key policy should be:

> Buyers purchase review work and attestation packaging, not a favorable conclusion.

This protects credibility and reduces legal/reputational risk.

# 14. Competitive landscape

## Commodity timestamping

OpenTimestamps already supports provable timestamps and independent verification. [S2] Tessera's free tier can use or interoperate with this layer, but selling the timestamp alone is unlikely to produce strong pricing power.

## Media provenance

C2PA provides an open technical standard for establishing the origin and edits of digital content. [S3] Tessera should not compete head-on with C2PA. It should preserve C2PA manifests and attach independent review claims to them.

## Software-supply-chain provenance

Sigstore/Rekor provides a tamper-resistant transparency log for software supply-chain metadata, and GitHub artifact attestations provide signed build provenance and integrity claims for software artifacts. [S4-S5] Tessera can attach or preserve those artifacts, but software build provenance is not the best first wedge.

## E-signature and notary platforms

E-signature platforms capture agreement workflows. Online notary platforms capture identity and notarial acts where legally recognized. Tessera's narrower and stronger position is different: it preserves portable third-party claims about digital artifacts.

## GRC and audit platforms

GRC tools manage compliance programs. They are systems of workflow and evidence collection. Tessera can complement them by making selected evidence packages independently verifiable and attachable to third-party reviews.

## Expert networks and consulting marketplaces

Expert networks route buyers to expertise. Tessera's differentiation is that the output is not only advice or a report. It is a signed, timestamped, portable attestation package with a defined verification path.

# 15. Go-to-market plan

## Positioning

Use language like:

> **Tessera is a marketplace for independently verifiable claims about digital artifacts.**

Supporting language:

> Start with a free timestamped receipt. Then attach independent validations, citation checks, reviewer reports, audit evidence, AI-governance reviews, or later re-attestations. Years later, a relying party can verify what was claimed, by whom, under what scope, and when.

Avoid language like:

- blockchain notarization;
- proves truth;
- certified compliant;
- legally admissible by default;
- AI hallucination solved;
- trustless marketplace.

## First customers

The first 25 customer conversations should target:

- expert witnesses;
- law firms handling technical evidence;
- AI governance leads;
- AI safety/evaluation consultancies;
- research integrity officers;
- academic editors;
- policy institutes;
- compliance/security leaders;
- technical publishers;
- consultants producing customer-facing reports.

## First validator partners

The first 10 validator conversations should target:

- research librarians or citation specialists;
- digital forensic consultants;
- AI-governance reviewers;
- security/compliance consultants;
- domain experts with report-writing experience;
- technical editors who understand evidence standards.

## First public artifacts

Publish sample artifacts:

1. a free receipt for a report;
2. a citation validation attestation;
3. an independent document review attestation;
4. an AI-governance evidence package;
5. a superseding/correction attestation;
6. a wrapper/re-anchoring attestation.

Each sample should show both human-readable and machine-readable forms.

## Content strategy

The content strategy should educate rather than hype:

- "What a timestamp proves and does not prove";
- "How to validate citations in AI-assisted reports";
- "How to preserve an expert report for future adversarial review";
- "What a third-party attestation should disclose";
- "Why negative findings improve trust";
- "How to verify a Tessera package if Tessera disappears."

## Sales motion

Start founder-led and consultative:

1. identify a document whose credibility matters;
2. create a free receipt;
3. choose one high-value claim to validate;
4. produce a paid attestation package;
5. ask who the relying party is;
6. design the output for that relying party;
7. convert repeat users to Evidence Vault.

# 16. Financial model and unit economics

The financial model is based on hypotheses, not asserted market facts. The key insight is that raw cloud cost is unlikely to be the limiting cost. AWS KMS charges per key and per request, and Lambda/DynamoDB/S3-style serverless components can support low-volume receipt creation inexpensively relative to professional review fees. [S9-S11]

The true cost base is trust operations:

- validator onboarding;
- review-method design;
- customer support;
- dispute handling;
- legal terms;
- insurance;
- security review;
- evidence package QA;
- enterprise sales and onboarding.


## Illustrative Year 1 model: concierge and validation learning

This is a learning year rather than a scaled marketplace. A plausible founder-led target is approximately **$244,000** in gross revenue across a small number of paid engagements:

- Citation validation bundles: 100 packages at an average of $300, producing about $30,000 gross revenue.
- Independent document reviews: 20 reviews at an average of $3,500, producing about $70,000 gross revenue.
- AI-governance evidence packages: 8 packages at an average of $7,500, producing about $60,000 gross revenue.
- Legal/expert evidence packages: 5 packages at an average of $12,000, producing about $60,000 gross revenue.
- Evidence Vault subscriptions: 20 accounts at $100/month, producing about $24,000 annual recurring revenue.

The Year 1 question is not whether this is a venture-scale business. The question is whether buyers will pay for scoped validation and whether relying parties understand the resulting packages.

## Illustrative Year 2 model: curated marketplace

A curated marketplace can begin once repeatable scopes and validator supply are proven. A plausible Year 2 shape is approximately **$570,000** in Tessera revenue:

- Marketplace citation packages: 750 packages at $250 average order value, or $187,500 GMV. At a 20% take rate, Tessera earns about $37,500.
- Marketplace document reviews: 100 reviews at $2,500 average order value, or $250,000 GMV. At a 20% take rate, Tessera earns about $50,000.
- AI/compliance packages: 40 packages at $8,000 average order value, or $320,000 GMV. At an 18% take rate, Tessera earns about $57,600.
- Professional and Team subscriptions: 100 accounts at $200/month, producing about $240,000 annual recurring revenue.
- Enterprise/private clearinghouses: 5 customers at $25,000/year, producing about $125,000 annual recurring revenue.
- Services and onboarding: 20 engagements at $3,000, producing about $60,000.

At this stage, Tessera should still be more concerned with repeatability, dispute burden, validator quality, and relying-party comprehension than with maximizing transaction volume.

## Illustrative Year 3 model: repeatable marketplace

A repeatable marketplace becomes attractive when subscription revenue and marketplace GMV reinforce each other. A plausible Year 3 shape is approximately **$4.18M** in Tessera revenue:

- Citation/source validation: 5,000 packages at $150 average order value, or $750,000 GMV. At a 20% take rate, Tessera earns about $150,000.
- Document/review marketplace: 500 reviews at $2,000 average order value, or $1,000,000 GMV. At an 18% take rate, Tessera earns about $180,000.
- AI/compliance/legal packages: 150 packages at $10,000 average order value, or $1,500,000 GMV. At a 15% take rate, Tessera earns about $225,000.
- Evidence Vault subscriptions: 500 accounts at $250/month, producing about $1,500,000 annual recurring revenue.
- Enterprise/private clearinghouses: 20 customers at $50,000/year, producing about $1,000,000 annual recurring revenue.
- Lifecycle and re-attestation services: 250 packages at $500, producing about $125,000.

These numbers are not forecasts. They are a testable shape of the business. If paid validation demand is real, the company can become profitable without needing massive commodity timestamp volume. If only free timestamping is adopted, the business should not scale spending.

## Gross margin implications

- Free timestamping should be cost-controlled and rate-limited.
- Software subscriptions should have high gross margin once support is controlled.
- Marketplace take-rate revenue has high margin only if dispute and quality costs are controlled.
- High-ticket services may carry good early margins but will not scale without validator supply.
- Enterprise/private clearinghouses may produce the best recurring revenue but require sales and implementation effort.

# 17. Metrics, validation gates, and kill criteria

## Marketplace validation metrics

| Metric | Why it matters | Early target hypothesis |
|---|---|---:|
| Free receipt to paid request conversion | Tests whether free timestamping creates paid demand | 2%-5% in targeted segments |
| Buyer willingness to pay | Validates value-added attestation | At least 10 paid pilots |
| Validator acceptance rate | Tests supply-side interest | 10 credible validators recruited |
| Average order value | Determines economics | $250+ for citation bundles; $2,000+ for reviews |
| Take-rate tolerance | Tests marketplace monetization | 15%-25% without buyer/seller rejection |
| Repeat purchase rate | Tests workflow value | 30%+ of paid buyers return within 6 months |
| Dispute/correction rate | Measures trust ops burden | Track, do not suppress |
| Relying-party comprehension | Tests evidence-package clarity | 80% can explain what was and was not attested |
| Time to complete validation | Determines operational viability | Citation bundle under 5 business days |
| Subscription conversion | Tests recurring SaaS layer | 20+ paying vault accounts before heavy product spend |

## Go/no-go gates

### Gate 1: Problem validation

Proceed only if at least 10 credible buyers can identify a concrete document, citation, report, or evidence package they would pay to validate.

### Gate 2: Paid pilot validation

Proceed to marketplace tooling only if at least 5 paid pilots are completed and at least 3 buyers say the attestation package would be useful to an external relying party.

### Gate 3: Supply validation

Proceed to open validator onboarding only if at least 10 credible validators are willing to accept standardized scopes and outcome-independent payment.

### Gate 4: Repeatability validation

Proceed to subscription and workflow investment only if at least two attestation categories can be delivered repeatedly with bounded scope, predictable turnaround, and acceptable dispute rate.

### Gate 5: Enterprise validation

Proceed to private clearinghouse sales only if at least two organizations ask to route multiple documents or reviewers through Tessera.

## Kill criteria

Stop pursuing the marketplace if:

- buyers like free receipts but will not pay for validation;
- validators will only participate if they can control or suppress unfavorable outcomes;
- relying parties do not understand the resulting packages;
- quality control costs exceed marketplace take-rate revenue;
- the business drifts into making claims Tessera cannot defend;
- the product requires locking users in to preserve revenue.

# 18. Risk register

| Risk | Why it matters | Mitigation |
|---|---|---|
| Commodity perception | Buyers may see Tessera as just timestamping | Lead with paid review outcomes and examples, not cryptographic primitives |
| Marketplace cold start | Two-sided marketplaces are hard to start | Start concierge, narrow category, hand-pick validators |
| Rubber-stamp perception | Paid validation can look biased | Pay for work, not outcomes; publish negative/qualified result policy |
| Bad validator | One weak reviewer can damage trust | Credential checks, method templates, audits, suspension process |
| Conflict of interest | Reviewers may have undisclosed relationships | Mandatory conflict disclosures and append-only conflict corrections |
| Liability creep | Buyers may overstate what was proven | Strict scope language and package-level limitation statements |
| Legal-status ambiguity | Users may confuse Tessera with notary/QTSP/certifier | Clear positioning; partner where qualified status is required |
| Privacy breach | Documents may be sensitive | Hash-first public records, private encrypted workrooms, access logs |
| Dispute overload | Review disagreements could consume support | Structured dispute workflow and minimum fees for high-risk categories |
| Free-tier abuse | Free timestamping can attract spam | Rate limits, abuse monitoring, paid tiers for high volume |
| Overbuilding | Marketplace features can consume time before demand exists | Build only after paid pilots establish repeatable workflows |
| Validator supply quality | Good experts may not want small transactions | Start with professional-service pricing, then productize narrow checks |
| Relying-party indifference | The market only works if third parties care | Design sample packages for courts, auditors, editors, customers, and regulators |
| Platform neutrality | Tessera could be pressured to hide bad findings | Append-only policy, no deletion of unfavorable final attestations except fraud/legal process markers |
| Trust proof gap | Commercial credibility depends on the formal foundation | Preserve preregistration H0 gate and avoid premature security claims |

# 19. Strategic conclusion

The corrected business model is stronger than a proof-pack service alone.

Tessera should be a **trust marketplace for digital artifacts**. Free timestamping gives every artifact a durable identity. Paid third-party attestations add value. The Evidence Vault and private clearinghouse make the workflow repeatable. Validators earn money and reputation. Buyers gain independently verifiable credibility. Relying parties gain a clearer record of what was claimed, when, by whom, under what scope, and with what limitations.

The simplest expression is:

> **Tessera is where digital artifacts go to accumulate independently verifiable trust.**

The first profitable business is likely not high-volume commodity issuance. It is a curated marketplace for validated citations, independent document reviews, AI-governance evidence, compliance attestations, and legal/expert evidence packages. The free timestamp is the doorway. The paid attestation graph is the business.

# 20. Appendices

## Appendix A: Example Citation Validation Attestation

**Subject artifact:** Document hash and receipt ID  
**Citation locator:** Section, paragraph, footnote, or page  
**Claim being supported:** Exact sentence or proposition  
**Cited source:** DOI, URL, statute, case, report, database record, archive hash  
**Validator:** Identity, organization, credentials, conflict statement  
**Method:** Citation Validation Method v1.0  
**Evidence reviewed:** Source text, archived copy, quoted passage, surrounding context  
**Outcome:** Supports / partially supports / does not support / source not found / source inaccessible / claim requires qualification  
**Limitations:** No independent verification of source truth unless separately scoped  
**Report:** Human-readable note  
**Signature and timestamp:** Tessera attestation receipt  
**Verification:** Offline verifier instructions

## Appendix B: Example Independent Document Review Attestation

**Subject artifact:** Report hash and receipt ID  
**Scope:** Review for internal consistency, citation sufficiency, methodology description, and disclosed limitations  
**Reviewer:** Named reviewer or organization  
**Method:** Document Review Method v1.0  
**Exclusions:** No legal advice; no independent factual investigation beyond listed evidence; no certification of truth  
**Findings:** Structured summary and report  
**Disposition:** Reviewed with no material exceptions / reviewed with qualifications / reviewed with material exceptions / declined  
**Signature and timestamp:** Tessera attestation receipt  
**Supersession:** Method for corrections and later reports

## Appendix C: Example AI-Governance Evidence Package

**Subject system:** Model or AI system identifier  
**Artifacts:** Model card, eval results, red-team report, deployment approval, transparency label, C2PA manifest where relevant  
**Policy:** Organization policy or regulatory checklist  
**Reviewer:** AI-governance reviewer or internal control owner  
**Method:** AI Governance Evidence Review Method v1.0  
**Claim:** Evidence package was reviewed against the named policy/checklist  
**Limitations:** Not a guarantee of compliance, safety, non-infringement, or truth  
**Signature and timestamp:** Tessera attestation receipt  
**Future review:** Required when policy, model, or deployment context changes

## Appendix D: Customer discovery questions

1. What document, report, citation, policy, model card, or evidence package would you most want a third party to validate?
2. Who is the relying party: court, regulator, auditor, customer, publisher, partner, investor, or internal committee?
3. What would make the validation credible to that relying party?
4. Would a negative or qualified finding still be valuable?
5. What credentials would the validator need?
6. What scope and limitations would be acceptable?
7. What would you pay for a 5-day citation validation package?
8. What would you pay for a 2-week independent document review?
9. Do you need the artifact content private, public, or hash-only public?
10. Would you want the same artifact to accumulate later attestations?
11. What would make you trust a Tessera package five years later?
12. What would make you reject it?

## Appendix E: Source notes

[S1] Tessera Phase 0 Pre-Registration, uploaded by Tony Mason, June 13, 2026. It identifies third-party findings such as audit, regulatory policy, ontology, or citation as attestation use cases; states that receipts should be independently verifiable; defines hard invariants around versioned canonicalization and zero service-side verification state; and distinguishes integrity wrapping from semantic re-attestation.

[S2] OpenTimestamps, official project page. The project defines operations for creating provable timestamps and later independently verifying them, with Bitcoin support.

[S3] Coalition for Content Provenance and Authenticity (C2PA), official site. C2PA provides an open technical standard for establishing the origin and edits of digital content.

[S4] Sigstore Rekor documentation. Rekor aims to provide an immutable, tamper-resistant ledger of software-supply-chain metadata.

[S5] GitHub documentation on artifact attestations. GitHub describes artifact attestations as signed claims that establish build provenance and integrity for software artifacts.

[S6] European Commission, Code of Practice on Transparency of AI-Generated Content, published June 10, 2026. The page states that Article 50 AI Act transparency obligations related to marking, detection, and labelling of AI-generated content apply from August 2, 2026.

[S7] EUR-Lex consolidated eIDAS Regulation, Article 41. Electronic timestamps cannot be denied legal effect solely because they are electronic, and qualified electronic timestamps enjoy a presumption of date/time accuracy and data integrity.

[S8] Canada Evidence Act, sections 31.1-31.2. A party seeking to admit an electronic document bears the burden of proving authenticity, and the best-evidence rule can be satisfied through evidence of electronic-document system integrity.

[S9] AWS KMS pricing. AWS lists monthly charges for KMS keys and request-based pricing for key operations.

[S10] AWS Lambda pricing. AWS lists request-based and duration-based pricing for Lambda functions.

[S11] AWS S3 Object Lock documentation. AWS describes Object Lock as a WORM mechanism to prevent objects from being deleted or overwritten for a fixed time or indefinitely.
