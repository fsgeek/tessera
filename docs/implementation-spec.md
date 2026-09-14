# Tessera — Implementation Specification (the current contract)

> **STATUS: PROPOSED — first draft 2026-09-13 — assembled by the AI
> collaborator (Claude, Fable 5.1, owner instance for sequencing and
> mechanics, directing Claude Opus 5 extraction, drafting, skeptic and
> integration agents; pipeline in
> `docs/reviews/2026-09-13-implementation-spec-assembly-log.md`) from the
> adopted artifacts; not adopted; the commit is the
> author's.** This document is band-1 docket item 31. It states the
> current contract and nothing else: what each behaviour consumes, checks,
> reports, and leaves to the adjudicator; the objects and their formats;
> the invariants; the parameters; the obligations still open. Every
> requirement carries a provenance tag naming the amendment, ruling, or
> model that justifies it. Where the record leaves a decision open, the
> requirement says so and §11 lists it. Where two parts of the record
> disagree, §12 states both and routes the question to the author;
> **nothing in this document resolves a contradiction**. If this document
> and a signed amendment disagree, the amendment wins and the disagreement
> is a defect here.

## 0. How to read this document

**Who it is for.** An implementer of the Band 1 cloud-independent core
and the reference verifier, and any reader who wants the design without
its history. The travelog, the review archive and the decision records
remain the places to challenge or revise the contract; this document
links into them and does not repeat them.

**Provenance tags.** Every requirement ends with one tag:

| Tag | Meaning |
|-----|---------|
| `[REGISTERED …]` | Signed pre-registration or amendment text, in force. Cited by section and file:lines. |
| `[RULED (author) date …]` | An author ruling recorded in the text under the `DECISION.md` provenance labels (ADOPTED (author), RULED (author), `[AUTHOR DECISION]`). In force from the commit named. |
| `[DECIDED …]` | A mechanism selection made under the registered decision pattern (criteria before evidence). |
| `[MODELLED family, file:lines]` | What a checked model implements. A MODELLED tag with no REGISTERED companion marks behaviour the models fix but no signed sentence requires; the assembler raises it, never adopts it. |
| `[PROPOSED …]` | A collaborator draft on the record, not adopted. Included only where it governs a behaviour and always so labelled. |
| `[DOCKET n — candidate]` | A band-1 docket item: unregistered, parked so it does not drop. Never a requirement. |
| `[DEFERRED …]` | A registered plan with nothing implemented and a named activation condition. |
| `[OPEN — §11 O-n]` | The point is undecided; §11 says what will settle it. |
| `[CONTRADICTION — §12 C-n]` | Two parts of the record disagree; §12 states both and routes the question. |

### 0.1 Which texts are in force, and since when

| Text | Commit | Date, and what the record says |
|---|---|---|
| Original pre-registration | `75207ba` | |
| Amendment 1 | `03cd3db` | |
| Amendment 2 | `62f0c5f` | 2026-07-21 |
| Amendment 3 | `8ae4720` | 2026-08-09. Its own status block still reads DRAFT, retained under amend-don't-rewrite; the tracker, the README and Amendments 4, 5 and 6 all cite `8ae4720` as its adoption. §12 S-02 cites this |
| Amendment 4 | `5188e7a` | 2026-09-06, confirmed by the author 2026-09-12 (A5 §A5.0) |
| Amendment 5 | `504e662` | 2026-09-12 |
| Amendment 6 | `c105be7` | 2026-09-12 |
| Amendment 7 | — | PROPOSED 2026-09-14; in force on the author's first commit containing it. Its rulings are tagged `[RULED (author) 2026-09-14; instrument A7 §A7.n, PROPOSED]` |
| First-link mechanism decision | `459aff0` | 2026-08-13 |
| Standing-evidence decision | `fbf6387` | entered 2026-09-04 |
| Identity-boundary ruling of 2026-07-28 | `68b581c` | 2026-08-07 |

Every `[REGISTERED A3 …]` tag in this document rests on `8ae4720`, so the
§1 and §3 section heads point here instead of carrying a caveat of their own.

**Normative words.** MUST, MUST NOT and SHALL appear only where the
source is normative. Descriptive source text stays descriptive here;
this document does not upgrade a description into an obligation.

**Requirement IDs** are `R-<section>.<n>` and are stable from this
document's first commit; a withdrawn requirement keeps its number and is
marked withdrawn, per amend-don't-rewrite.

**Vocabulary.** *Verifier*: the pure function of bundle and declared
policy that returns a typed verdict (P9). *Adjudicator*: whoever decides
what to do with a verdict; never Tessera. *Bundle*: the self-contained
package presented to a verifier. *Issuer*: the Tessera service at
issuance. *Authority channel*: a source of archived, time-anchored
evidence that a key was an authorized issuer key. *Standing*: the
orthogonal assessment of an artifact's protocol standing, reported
separately from the verdict. Definitions are §1 and §2's; this list is
only so the reader can start.

**Sections.** §1 what Tessera attests and does not (with the relying-party
story, §1.5) · §2 actors, channels, trust configuration, adversary · §3
objects and formats · §4 issuance protocol · §5 verification procedure ·
§6 standing assessment · §7 survivability, custody, tending, agility,
renewal · §8 parameters · §9 invariants and failure behaviour · §10
outstanding obligations · §11 register of unresolved decisions · §12
contradictions routed to the author · Appendix A requirement index.

**What this document is not.** Not a pre-registration, not an amendment,
not a decision record, not a tracker: it registers nothing, adopts
nothing, moves no tracker row, and weakens no property (A1 §A1.1).
It is not the relying-party story's home of record; §1.5 is that page's
first draft and it is also published stand-alone as the registered exit
artifact. It is not the Band 1 specification: Band 1 items live on the
docket until registered.

**Sources this draft was assembled from** (read in full by the extraction
pass, 2026-09-13): `docs/phase-0-prereg.md` §3–§4; Amendments 1–6;
`formal/spike/first-link/DECISION.md`; `formal/spike/standing-probe/DECISION.md`
and `AMENDMENTS-2026-08-31.md`; `formal/suite/ENUMERATION.md` and
`ROUTED-2026-09-06.md` author dispositions; the shared library
`formal/suite/lib/tessera_theory.pvl`; the five suite families' claim
blocks and `RESULTS.md`; the TLA+ modules and their reading aids;
`formal/PROPERTIES.md`, `formal/COVERAGE-MAP.md`, `formal/BAND0-EXIT.md`;
`docs/band-1-docket.md`; the 2026-07-28 identity-boundary ruling. The
extraction cards (759, with file:line citations) are working papers, not
part of the record.

---

## 1. What Tessera attests, and what it does not

*Provenance: every `[REGISTERED A3 …]` tag in this section rests on Amendment 3's adoption at `8ae4720`; see §0.1.*

### 1.1 The identity boundary

**R-1.1** Tessera attests the identity of the framed bytes presented at an issuance event — computational identity under the declared construction and assumptions — and nothing more. [REGISTERED A3 §A3.1, docs/phase-0-prereg-amendment-3.md:61-66; author-ruled 2026-07-28, docs/reviews/2026-07-28-identity-boundary-evidence-floors-ruling.md:61-67]

**R-1.2** Explicitly outside the attestation: meaning, truth, intended use, future interpretation, and the metaphysical identity of the payload's referent. [REGISTERED A3 §A3.1, docs/phase-0-prereg-amendment-3.md:64-66]

**R-1.3** Tessera establishes *computational* identity of the framed representation, not metaphysical identity of the payload's referent: "If the frame says 'this image depicts Tony,' Tessera can preserve that exact assertion; it cannot establish who the image depicts." [RULED (author) 2026-07-28, docs/reviews/2026-07-28-identity-boundary-evidence-floors-ruling.md:90-95]

**R-1.4** The can/does-not-establish list is recorded verbatim and is the opening of the relying-party story. [REGISTERED A3 §A3.1 item 4, docs/phase-0-prereg-amendment-3.md:89-96; verbatim text at docs/reviews/2026-07-28-identity-boundary-evidence-floors-ruling.md:79-88]

> Tessera can establish:
> "This valid package reconstructs the same framed bytes recorded
> at issuance."
>
> Tessera does not establish:
> "The payload is true."
> "The issuer understood it."
> "The relying party interpreted it correctly."
> "This was the package the relying party expected."
> "The external thing named by the payload is authentic."

### 1.2 Replay, and the operative headline

**R-1.5** Re-presenting a genuinely issued package preserves identity, and P1 permits it. Whether a replay is appropriate in a transaction is policy belonging to a context that must supply transaction identity, nonce, audience, or purpose; Tessera does not invent that context. [REGISTERED A3 §A3.1 item 1, docs/phase-0-prereg-amendment-3.md:68-74]

**R-1.6** P1's symbolic statement is existential issuance-event authenticity (a non-injective correspondence), with replay and context scoped to caller policy. [REGISTERED A3 §A3.1 item 1, docs/phase-0-prereg-amendment-3.md:71-74; MODELLED S-P1, formal/suite/s-p1/proverif/sp1_q2_degraded_compromised.pv:163-164 (the correspondence query), :168-181 (the verifier)]

**R-1.7** The operative form of the H0 headline is: alteration is trivial; surviving verification over altered bytes is what is hard — no transition leads to an accepted receipt over altered bytes. The earlier form ("altering any part requires solving a computationally hard problem") is superseded as a claim-correspondence repair. [REGISTERED A3 §A3.1 item 2, docs/phase-0-prereg-amendment-3.md:75-83]

**R-1.8** The load-bearing modelled check for the operative form is that the presented key signed exactly the presented bytes; every other single removal from the verifier leaves the headline true. [MODELLED S-P1, formal/suite/s-p1/proverif/sp1_q2_degraded_compromised.pv:38-47, 176-177 — modelled, and registered only in the A3 §A3.1 item 2 form]

**R-1.9** The repository shall carry a coverage map from package component to defending property — bytes → P1, signature set → P2, type/wrapper → P7, manifest authority → P10, anchor identity → A2.4, framing → P8 — with open cells visible. [REGISTERED A3 §A3.1 item 3, docs/phase-0-prereg-amendment-3.md:84-88]

### 1.3 The adjudicator boundary

**R-1.10** In degraded mode — any verdict other than `VALID_STRICT`, including the sole-channel-compromised case — the verifier's job is to hand the adjudicator the evidence of what could and could not be excluded, marked as degraded per §A1.2.1's explicit-policy logic. Tessera does not decide whether the adjudicator should trust the attestation and must not try to. [RULED (author) A4 §A4.6, docs/phase-0-prereg-amendment-4.md:156-172]

**R-1.10a** The bearer of A2 §A2.4's prohibition on ordering competing receipts by declared time is Tessera itself: no Tessera verifier policy, report, rendering or marketplace rule presents `declared_issue_time` as evidence of first-to-file priority, and Tessera makes no priority claim. What an adjudicator does with a declared time in its own reasoning is the adjudicator's (R-1.22, A4 §A4.6), and this is not a service-refusal requirement: Tessera does not refuse service, verification or reporting on the ground that a relying party might so reason. The prohibition's ground — that re-issue gives the issuer discretion over declared times — is unchanged. [RULED (author) 2026-09-14; instrument A7 §A7.4, PROPOSED; §12 C-06. A7 §A7.4 records this as a narrowing of A2 §A2.4's bearer, stated as such on the record]

**R-1.11** A correspondence that holds in strict mode and fails in degraded mode is a registered cost of degradation, to be stated in the relying-party story, never a defect of the construction — provided the verdict says it is degraded. [RULED (author) A4 §A4.6, docs/phase-0-prereg-amendment-4.md:167-171]

**R-1.12** R-1.11 is bounded: "Only losses permitted by the registered waiver rules and the declared policy are degradation costs. A degraded label does not excuse violating a non-waivable requirement or misreporting a required check's outcome." [RULED (author) A5 §A5.7, docs/phase-0-prereg-amendment-5.md:221-241, quoted sentence at :233-236]

**R-1.13** `VALID_STRICT` attests envelope soundness, never payload truth. The registered text records that "nothing previously registered prevented a future API or UI from relaying envelope validity as content validity" and then registers the prohibition: "Nor may the system collapse envelope verification, protocol standing, payload interpretability, or custodial health into one judgment." [REGISTERED A3 §A3.8, docs/phase-0-prereg-amendment-3.md:679-684]

**R-1.14** No unqualified aggregate checkmark is part of the conforming result. [REGISTERED A3 §A3.8, docs/phase-0-prereg-amendment-3.md:703-704]

**R-1.15** The base assessment is an unsigned, reproducible computation; it reports what the verifier can establish at evaluation time and leaves the relying party to decide whether those facts meet its requirements. [REGISTERED A3 §A3.8, docs/phase-0-prereg-amendment-3.md:686-689; the "unsigned" choice itself is `[AUTHOR DECISION — ratified -- 2026-08-08]` at :722-734]

**R-1.16** Verification verdict and protocol standing are reported separately and never collapsed: an artifact may honestly be `verification = VALID_STRICT` and `protocol_standing = ABSENT`; relying-party policy decides whether those facts meet its own requirements. [REGISTERED A3 §A3.7.1, docs/phase-0-prereg-amendment-3.md:542-548]

**R-1.17** Standing is reported, never waived; no verifier policy, strict or degraded, rewrites the reported standing value. A relying party may accept `ABSENT` or `UNVERIFIABLE` standing, but that acceptance is the policy's own recorded decision outside the verdict. [REGISTERED A3 §A3.7.1 `[PANEL-DRIVEN CLARIFICATION — 2026-08-08]`, docs/phase-0-prereg-amendment-3.md:550-557]

**R-1.18** A wrapper commits to the inner package's bytes, not to the inner receipt's verification result at wrap time; wrapping never alters the inner package's independently computed verdict. [REGISTERED prereg §3.1, docs/phase-0-prereg.md:356-364; A1 P7, docs/phase-0-prereg-amendment-1.md:248-253]

**R-1.19** A tending record proves only that a named custodian made the recorded assessment; mechanical checks prove only their bounded results. Tending health never changes a receipt's P4 verdict or protocol standing. [REGISTERED A3 §A3.5, docs/phase-0-prereg-amendment-3.md:403-405, 418-419]

**R-1.20** The century horizon is aspirational, not a guarantee or membership criterion; Tessera makes no prediction that today's bundle, standards, algorithms, or competence declaration will suffice one century hence. [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:322-326]

### 1.4 Verifier / adjudicator vocabulary

**R-1.21** The **verifier** is P9's pure function: bundle plus declared policy in, verdict out. "if the verifier requires anything from an optional service, it is fundamentally broken." [RULED (author) 2026-09-06, recorded in band-1 docket item 27, docs/band-1-docket.md:517-521; registered with A4 §A4.6, docs/phase-0-prereg-amendment-4.md:176-182]

**R-1.22** The **adjudicator** (the relying party) decides trust using the verdict plus anything else available, including any third-party log anyone built, and "is not prohibited from using that log as part of its own verification." [RULED (author) 2026-09-06, recorded in band-1 docket item 27, docs/band-1-docket.md:521-525]

**R-1.23** An enumeration or observability API may feed a log and may never feed a verdict. [RULED (author) A4 §A4.6, docs/phase-0-prereg-amendment-4.md:181-182; docs/band-1-docket.md:525 ("an enumeration API")]

**R-1.24** The relying-party story defines both terms. [RULED (author) 2026-09-06, docs/band-1-docket.md:524]

**R-1.25** The relying-party story is a required Band 0 exit artifact: one page; a person holds a receipt and a verdict; these are the decisions they may and may not make on it. It opens with the can/does-not-establish list. [REGISTERED A3 §A3.1 item 4, docs/phase-0-prereg-amendment-3.md:89-96] [OPEN — §11 O-66]

**R-1.26** The relying-party story is the human-facing statement of the boundaries whose machine-facing twins are the structured base-assessment fields. [REGISTERED A3 §A3.8, docs/phase-0-prereg-amendment-3.md:736-737]

---

### 1.5 The relying-party story

*Draft toward the registered artifact of R-1.25; not itself an adopted artifact. Every sentence below rests on registered or author-ruled text; the candidate paragraph carried in the first draft (docket 24(c), the anchor's survivability under hash failure) was removed in the 2026-09-14 drafting repair, which also separated the two `UNVERIFIABLE` dimensions, added the `INVALID` paragraph, qualified what standing evidence establishes, and restated the horizon sentence as a verification property.* [OPEN — §11 O-66]

**What Tessera can establish.** This valid package reconstructs the same framed bytes recorded at issuance.

**What Tessera does not establish.** That the payload is true. That the issuer understood it. That you interpreted it correctly. That this was the package you expected. That the external thing named by the payload is authentic. [docs/reviews/2026-07-28-identity-boundary-evidence-floors-ruling.md:79-88]

Tessera keeps the *bytes* honest. If the frame says "this image depicts Tony," Tessera can preserve that exact assertion; it cannot establish who the image depicts. [docs/reviews/2026-07-28-identity-boundary-evidence-floors-ruling.md:90-95]

**What a bundle presented alone gives you.** A verdict about the envelope, computed offline from the bundle and your own declared policy, with the service dead and no network. [docs/phase-0-prereg.md:519-525] A `VALID_STRICT` verdict says: the bytes in front of you are the bytes that were signed at issuance, by a key the manifest's authority evidence supports, with the timestamp anchor consistent with the declared issue time. It says nothing about whether the content is correct, useful, or the one you were promised. [the three-part gloss is A1's properties, not the can/does-not-establish list: P1, docs/phase-0-prereg-amendment-1.md:116-119; §A1.5, :444-448; P5 with A2 §A2.2, docs/phase-0-prereg-amendment-2.md:220-224. "Envelope soundness, never payload truth": docs/phase-0-prereg-amendment-3.md:679-684]

**What standing adds.** Cryptographic validity alone confers no protocol standing. A bundle can be perfectly valid and still be an artifact the service abandoned — an attempt that was superseded, or refused, or that was never the one shipped. Standing evidence is what tells you which designation the presented evidence supports; it does not establish that no contradictory terminal record exists, since two terminal lineage records under the entitled key each report `ESTABLISHED` in their own bundle. [formal/suite/s-standing/RESULTS.md:540-546, "What S-STANDING does not discharge", first bullet] Missing standing evidence leaves the artifact evidentially admissible but without protocol standing: you may still use it, on your own judgement, but Tessera is not asserting it. [docs/phase-0-prereg-amendment-3.md:531-535, 546-549] Standing is reported beside the verdict and never folded into it, and no policy can rewrite the reported standing value. [docs/phase-0-prereg-amendment-3.md:550-557]

**What a degraded verdict means for you.** `VALID_DEGRADED` means you asked the verifier to accept less than the full evidence, and it did, and it wrote down exactly what it let go and why. [docs/phase-0-prereg-amendment-1.md:325-327] The verifier's job in that mode is to hand you the evidence of what could and could not be excluded, marked as degraded. Tessera does not decide whether you should trust the attestation, and must not try to. [docs/phase-0-prereg-amendment-4.md:156-172] Two limits on that: the final complete evidence chain can never be waived — redundant paths may go, the last one may not [docs/phase-0-prereg-amendment-3.md:102-109, 139-145] — and a degraded label never excuses violating a non-waivable requirement or misreporting a required check's outcome [docs/phase-0-prereg-amendment-5.md:233-236]. One cost is recorded and belongs here: a package may be reported `VALID_DEGRADED` while its bundle carries waived evidence that is present and demonstrably fails, including evidence naming a different key, which is evidence of equivocation and not mere absence. The record will say so. [docs/phase-0-prereg-amendment-5.md:123-132]

**What `INVALID` means.** A required check was performed and it failed. That is a different answer from a check that could not be performed, and the two are never merged: collapsing them into one boolean is exactly where fail-open bugs hide. [docs/phase-0-prereg-amendment-1.md:152-158; docs/phase-0-prereg.md:555-562]

**What `UNVERIFIABLE` means.** Not "no" and not "yes": *could not check*. On the envelope: a required public key unavailable to the verifier, an algorithm this verifier does not know, block headers you could not obtain. [docs/phase-0-prereg.md:327-337; docs/phase-0-prereg-amendment-3.md:146-149, 503-505; docs/phase-0-prereg-amendment-2.md:245-248] Standing has its own `UNVERIFIABLE`, reported beside the verdict and not part of it: standing evidence that is internally inconsistent, or whose own anchor does not check out. [the standing-anchor case is `STANDING_EVIDENCE_TEMPORAL_MISMATCH`, formal/spike/first-link/DECISION.md:844-847; docs/phase-0-prereg-amendment-3.md:541-546] Neither is ever silently promoted to a valid answer, and a definite failure always outranks an open question. [docs/phase-0-prereg.md:335-337; docs/phase-0-prereg-amendment-4.md:88-98]

**What the anchor bounds.** The anchor bounds *when*, not *whether*: it proves the bytes existed not after a given block, gives no lower bound, and does not make a contemporaneous second record discoverable. [docs/phase-0-prereg-amendment-1.md:477-491; docs/band-1-docket.md:337-347]

**What you have to do yourself.** Keep the bundle. Availability after handoff is your custody, not the service's. [docs/phase-0-prereg-amendment-3.md:270-272, 280-288] And decide, on your own stakes, whether an attestation that verifies is an attestation you should act on. That decision is yours by design; verification must not depend on Tessera still existing — "An attestation must verify with the service **dead**" — and any other arrangement would imply service guarantees it cannot honestly make. [docs/phase-0-prereg.md:519-525; docs/phase-0-prereg-amendment-4.md:172-177]

---

## 2. Actors, channels, trust configuration, adversary

### 2.1 Actors

| Actor | Definition | Source |
|---|---|---|
| Issuer | The service; signs with two keys from independent failure domains over the same canonical bytes, anchors, and ships only on a confirmed anchor | docs/phase-0-prereg.md:273-298; docs/phase-0-prereg-amendment-1.md:186-197 |
| Verifier | P9's pure function: bundle plus declared policy in, verdict out | docs/phase-0-prereg-amendment-4.md:176-182 |
| Adjudicator / relying party | Decides trust using the verdict and anything else available | docs/phase-0-prereg-amendment-4.md:178-181 |
| Custodian | Holds the bundle, or the refusal record, after handoff; performs tending | docs/phase-0-prereg-amendment-3.md:314-320, 583-596 |

**R-2.1** The issuer signs with two keys from independent failure domains — KMS for cloud-native custody, local GPG counter-signing for a portable independent WHO layer — both over the same canonical bytes. [REGISTERED prereg §3.1 "Decision: C.", docs/phase-0-prereg.md:273-298]

**R-2.2** Issuance is not complete until the anchor is confirmed at depth k within δ of `declared_issue_time`; a receipt never ships on a shallow anchor. [REGISTERED A1 P5 corollary, docs/phase-0-prereg-amendment-1.md:186-197; A2 §A2.1 "The rule", docs/phase-0-prereg-amendment-2.md:87-89]

**R-2.3** The issuer evaluates the full three-conjunct temporal predicate of A2.2 before shipping; evaluation of conjunct 3 alone is insufficient and is forbidden. The ship guard is that predicate plus the burial-depth requirement, and the issuer does not re-run envelope verification (P1–P3) at ship. [REGISTERED A3 §A3.7.3, docs/phase-0-prereg-amendment-3.md:654-663; REGISTERED A3 §A3.7.3 `[PANEL-DRIVEN REPAIR — 2026-08-08]`, :665-675] [RULED — §12 C-08, A7 §A7.6]

**R-2.4** Issuance makes at most N attempts (working default N = 3); exhausting them obligates termination in an explicit, durably recorded refusal — a first-class protocol outcome, not an error path. [REGISTERED A2 §A2.3, docs/phase-0-prereg-amendment-2.md:252-276]

**R-2.5** The verifier's verdict is a pure function of the bundle and the verifier's declared policy: no service-side state, no live network dependency appears in the decision. An attestation must verify with the service dead. [REGISTERED A1 P9, docs/phase-0-prereg-amendment-1.md:278-281; prereg §4.4, docs/phase-0-prereg.md:519-525]

**R-2.6** For horizons requiring availability and evidentiary continuity, the Designated Community is not only the bundle's audience but its custodian; availability and evidentiary continuity are declared custodial dependencies. [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:314-320]

**R-2.7** Custodial renewal wraps, it never replaces; renewal must occur before the old mechanism becomes unreliable. Tending is the custodian's recorded assessment, with outcomes `NO_ACTION_REQUIRED`, `RENEWED`, `ACTION_DUE`, `FAILED`. [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:273-278; REGISTERED A3 §A3.5, :384-394]

**R-2.8** For refusal records, the generating authority retains the complete record until the first of `ACKNOWLEDGED` (a declared custodian, the submitter by default, confirms possession of a record that verifies against the commitment value), `DELIVERY_FAILED`, or `DELIVERY_EXPIRED`; after acknowledgment continued availability is a custodial dependency. [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:583-596]

**R-2.9** The terminal lineage record is carried, not maintained: the service's duty is punctual, not custodial, and everything the standing report needs is in the bundle, whose custodian is the relying party. [RULED (author) at adoption, formal/spike/standing-probe/DECISION.md:130-140, 386-390 — decided, not registered in an amendment]

### 2.2 Authority channels

**R-2.10** The issuer-key manifest carries two independent, archived, time-anchored authority-publication evidences — the DNSSEC chain snapshot and the anchored repository publication — plus a manifest self-signature by the issuer keys. [REGISTERED A1 P10 / §A1.5, docs/phase-0-prereg-amendment-1.md:283-297, 430-442]

**R-2.11** The manifest self-signature is proof of possession only and is never counted as an authority channel: an attacker's invented key self-signs for free. [REGISTERED A1 §A1.5 item 3, docs/phase-0-prereg-amendment-1.md:439-442]

**R-2.12** `VALID_STRICT` requires all external authority evidences to validate, plus proof of possession. [REGISTERED A1 P10, docs/phase-0-prereg-amendment-1.md:290-291; A1 §A1.5, :444-448]

**R-2.13** The channels are generalised: "DNS" means any domain, "repository" means any public repository source; multiple authority-key services are permitted. A1.3 item 6 is already n-ary; the models are the n = 2 instance and say so. [RULED (author) in session 2026-09-06, recorded inside band-1 docket item 26, which is headed "candidate; not registered anywhere in the record", docs/band-1-docket.md:465-468] [OPEN — §11 O-69]

**R-2.14** Two carried caveats on channel count: channel count is not strength — an inert check adds nothing — and each added channel raises the frequency of degraded verdicts. [RULED (author) in session 2026-09-06, recorded inside band-1 docket item 26 (candidate, not registered), docs/band-1-docket.md:469-471]

**R-2.15** Declared residual: both present external channels are ultimately operated by the same author; their independence is real against channel failure and single-channel compromise, weaker against an adversary who owns the author's entire operational sphere at issue time. That adversary sits at the misissuance boundary and is met operationally, not cryptographically. [REGISTERED A1 §A1.5, docs/phase-0-prereg-amendment-1.md:450-458]

**R-2.16** Recorded as candidate, not registered: the attestation company itself is the weak spot, since it holds the accounts on every channel plus the issuer key — correlated custody at the account layer; compromise of control (credential theft, insider) is distinguished from Tessera by no model in the record. [PROPOSED — docket item 26, docs/band-1-docket.md:471-481]

### 2.3 The verifier's trust configuration

**R-2.17** The verifier's pre-bundle inputs are trust configuration only: channel public keys, `k`, and `δ`. Everything else is read from the bundle. [MODELLED standing-probe Q6, formal/spike/standing-probe/RESULTS-PROBE.md:41; DECIDED, formal/spike/standing-probe/DECISION.md:71-72 (G2) — modelled and decided, not registered in an amendment]

**R-2.18** The reference verifier maintains an archived historical trust-anchor store (DNS root keys and repository signing keys, by validity period), distributed with the verifier as trust configuration — not service-side state, so P9 is not violated. [REGISTERED A1 §A1.5, docs/phase-0-prereg-amendment-1.md:459-469]

**R-2.19** Block headers `h … h + k − 1` are available either archived in the bundle or from the verifier-distributed header store — the same trust-configuration pattern as the historical trust-anchor store. [REGISTERED A2 §A2.2, docs/phase-0-prereg-amendment-2.md:236-244]

**R-2.20** δ and ε belong to the verifier, not the receipt. A receipt records its issue-time policy version and the observed anchor delay; it may not choose its own temporal tolerances. A verifier may choose stricter bounds; no degraded policy may enlarge δ or ε beyond the strict maxima (δ = 72 h, ε = 24 h). [REGISTERED A1 P5, docs/phase-0-prereg-amendment-1.md:173-184] [OPEN — §11 O-44]

**R-2.21** In the symbolic models the verifier's only trust input is the authority channel's verification key, supplied as a process parameter (`VerifierS(pkS: pkey)`, instantiated `!VerifierS(pk(skS))`); the strict form takes one such key per channel. [MODELLED S-P3, formal/suite/s-p3/proverif/sp3_q2_degraded_compromised.pv:98, 149-153; S-STANDING strict, formal/suite/s-standing/proverif/ss_q1_strict_dns_compromised.pv:348-356]

**R-2.22** Everything else arrives on the public channel as the presented bundle. The modelled bundle input is `(t, ev, kX, ppf, sg, fb)` — evidenced tuple, authority evidence, presented key, possession proof, attestation signature, framed bytes. [MODELLED S-P3, formal/suite/s-p3/proverif/sp3_q2_degraded_compromised.pv:98-100; S-P1 unchanged, formal/suite/s-p1/proverif/sp1_q2_degraded_compromised.pv:166-170]

**R-2.23** The standing path takes standing evidence and the attempt core in the same input (`(t, ev, kX, core, fb, se)`) and evaluates the evidenced tuple and the entitled key itself; it inherits nothing from the envelope path. [MODELLED S-STANDING, formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:319-326; RULED, docs/phase-0-prereg-amendment-5.md:202-219]

**R-2.24** P9's discharge is [inspection + vector]: an enumeration of the reference verifier's inputs, re-checked against the reference verifier at H1a, plus one H1a red-bar vector. The vector carries the expected verdict determined by bundle and declared policy; each machine's verdict is compared to that, not only to the other machine's; one case presents the same bundle twice on one machine and requires the same verdict both times; and the "consults an optional service" clause is discharged by the inspection leg together with one case in which the optional service is reachable and contradicts the bundle. [RULED A4 §A4.1, docs/phase-0-prereg-amendment-4.md:60-71, as rewritten by A5 §A5.1, docs/phase-0-prereg-amendment-5.md:58-91]

### 2.4 Strict and degraded modes

**R-2.25** Verification yields exactly one of `VALID_STRICT`, `VALID_DEGRADED(policy=...)`, `INVALID`, `UNVERIFIABLE` — a typed result, never a bare boolean. [REGISTERED prereg §3.1, docs/phase-0-prereg.md:327-337; prereg §4.6, :555-562; MODELLED P4, formal/tla/P4_VerifierStates.tla:70]

**R-2.26** `VALID_STRICT` requires all issue-time signatures to verify and no waived check; the modelled decision procedure is: any required check failed → `INVALID`; else any required check unperformable → `UNVERIFIABLE`; else empty waiver set → `VALID_STRICT`; else `VALID_DEGRADED`. [REGISTERED prereg §3.1, docs/phase-0-prereg.md:307-311; MODELLED P4, formal/tla/P4_VerifierStates.tla:96-105]

**R-2.27** No verifier policy may waive: canonical-byte integrity (P1, P8); type/domain separation (P7); boundary framing (P8); key-to-issuer binding for every accepted signature (P3); temporal-anchor consistency (P5). A package failing any non-waivable check is `INVALID` under every policy; no degraded policy may promote it. [REGISTERED A1 §A1.2.1, docs/phase-0-prereg-amendment-1.md:309-317]

**R-2.28** Degraded policies may weaken only declared redundancy: a subset of the issue-time signature set (P2); fewer than all external manifest-authority evidences (P10); a signature whose trust root is no longer independently recoverable, where the remaining checks pass. [REGISTERED A1 §A1.2.1, docs/phase-0-prereg-amendment-1.md:319-323]

**R-2.29** The P10 waiver is tightened to fewer, but never zero: redundant members of the A1.5 evidence set may be waived; the final complete chain may not be broken or eliminated. Every valid verdict requires at least one continuous accepted evidentiary chain per independently evaluated attestation layer. [REGISTERED A3 §A3.2, docs/phase-0-prereg-amendment-3.md:102-109, 139-145]

**R-2.30** If every external authority evidence for a layer is unavailable, unsupported, or otherwise unperformable, the layer's verdict is `UNVERIFIABLE` — never `VALID_DEGRADED`. [REGISTERED A3 §A3.2, docs/phase-0-prereg-amendment-3.md:146-149]

**R-2.31** Required evidence that is present and whose validation is performed but fails yields `INVALID`. Evidence the declared policy has waived is evaluated, its condition recorded, and never determines the verdict. [RULED A5 §A5.2, docs/phase-0-prereg-amendment-5.md:93-121, rewriting A3 §A3.2 item 2] [RULED — §12 C-05, A7 §A7.3]

**R-2.31a** Object scope, made explicit. A2 §A2.2's three temporal conjuncts apply to **the receipt's own shipped anchor** and are non-waivable: a late receipt anchor is performed-and-failed and yields `INVALID`, never an observation. A5 §A5.3's `anchor-late` is an observation recorded against **a waived redundant authority evidence's own anchor** and never determines the verdict. No waiver may remove the final complete evidence chain (R-2.29). A2 §A2.2 and A5 §A5.3 are each correct on their own object. [RULED (author) 2026-09-14; instrument A7 §A7.3, PROPOSED; §12 C-05]

> **Reading confirmed by the author 2026-09-14 (A7 §A7.3; was marked for correction).** The author's second sentence as typed reads "the receipt's required temporal checks are still *not* non-waivable"; A7 instruments it as "still non-waivable", the reading its own third sentence, A2 §A2.2 and A3 §A3.2's linked floor all require. If the author meant the words as typed, A7 §A7.3 is withdrawn and C-05 returns to §12 as open.

**R-2.32** P4's unperformable rule applies to *required* checks only. A4 quotes P4's sentence — "A check that cannot be performed yields `UNVERIFIABLE` — never any `VALID` state, under any trace" — and states that it "is read, and is hereby written, as" "A **required** check that cannot be performed…". [RULED (author) A4 §A4.2, docs/phase-0-prereg-amendment-4.md:100-109]

**R-2.33** When one required check fails and another cannot be performed, the verdict is `INVALID`; a definite failure is stronger evidence than an open question, and the alternative would make the verdict depend on evaluation order. `INVALID` dominates `UNVERIFIABLE`. [RULED (author) A4 §A4.2, docs/phase-0-prereg-amendment-4.md:88-98; RULED, formal/spike/first-link/DECISION.md:385-391]

**R-2.34** `UNVERIFIABLE` is never silently promoted to `VALID`. [REGISTERED prereg §4.6, docs/phase-0-prereg.md:335-337; MODELLED P4 `NoSilentPromotion`, formal/tla/P4_VerifierStates.tla:124]

**R-2.35** Every `VALID_DEGRADED` verdict records the precise waived check set and the policy that authorized the waiver — the informed-consent act, made auditable. [REGISTERED A1 §A1.2.1, docs/phase-0-prereg-amendment-1.md:325-327]

**R-2.36** For each waived check the record additionally holds the verifier's observation of the waived evidence: at least the six values absent, unperformable, invalid, anchor-late, names-other-key, would-pass. Evaluation is bounded by the bundle and the declared inputs; inability to evaluate is itself one of the recorded observations and never a reason to consult anything. [RULED A5 §A5.3, docs/phase-0-prereg-amendment-5.md:134-155] [OPEN — §11 O-06] [RULED — §12 C-05, A7 §A7.3]

**R-2.37** Where the binding assessment is concerned, a well-formed identifier unknown to the verifier, or known but unsupported, yields `UNVERIFIABLE` with an appropriate reason; a missing, malformed, duplicate, substituted, or inconsistently encoded member — or an empty required set — yields `INVALID`. No inference, negotiation, normalization, or fallback is permitted during verification. [RULED (author) — the source's own label is ADOPTED (author) 2026-08-13, formal/spike/first-link/DECISION.md:366-383 — decided in a spike DECISION.md, not registered in an amendment]

**R-2.38** The two `UNVERIFIABLE` cases — unknown identifier and known but unsupported — must not share a reason code. [RULED, formal/spike/first-link/DECISION.md:393-397]

**R-2.39** The floors bound entry into the two `VALID` states; they add no states and alter no verdict semantics. Standing is an orthogonal assessment dimension, not a fifth P4 state. [REGISTERED A3 §A3.2, docs/phase-0-prereg-amendment-3.md:165-167; A3 §A3.7.1, :541-546]

### 2.5 The adversary model

**R-2.40** The Band 0 adversary can, at minimum: (1) alter any bytes of a package, receipt, manifest, or wrapper after issue; (2) strip, reorder, or duplicate signatures within the signature set; (3) substitute keys, including choosing keypairs after seeing valid signatures (DSKS), and always self-sign with keys it holds; (4) replay valid packages, receipts, or manifests in other contexts and re-frame objects across the P7 type boundaries; (5) craft manifests freely and anchor anything; (6) control any proper subset of the external manifest-authority channels. [REGISTERED A1 §A1.3, docs/phase-0-prereg-amendment-1.md:331-346]

**R-2.41** Item 6 reads "Control any proper subset of the external manifest-authority channels" (the record's shorthand for it is "never all", not item 6's own words) and is n-ary as written; the symbolic models are the n = 2 instance. For n = 2 the baseline and two single-compromise variants exhaust the proper subsets — a finite enumeration, not a quantified result. [REGISTERED A1 §A1.3 item 6, docs/phase-0-prereg-amendment-1.md:344-346; MODELLED, formal/spike/first-link/RESULTS.md:84-107 with documentation correction 2026-08-12] [OPEN — §11 O-69]

**R-2.42** The degraded-mode fixtures are strictly stronger than item 6: they publish the sole channel's signing key, so the accepted channel is fully compromised rather than a proper subset. The boundary-invariant result under that fixture does not rest on "never all". [MODELLED S-P3, formal/suite/s-p3/proverif/sp3_q2_degraded_compromised.pv:143-154; DECIDED, formal/spike/first-link/DECISION.md:770-778]

**R-2.43** DSKS is modelled as a constructor `dsks(s, r)` with a second rewrite, built by the adversary from one seen signature; every suite query therefore holds, if it holds, under an adversary with the registered DSKS capability. It does not grant forging under a key the adversary does not hold, does not make a derived key verify any other signature, and gives no key recovery. [MODELLED library, formal/suite/lib/tessera_theory.pvl:46-53, 98-101, 110, 114-115; REGISTERED A1 §A1.3 item 3, docs/phase-0-prereg-amendment-1.md:339-342]

**R-2.44** Ed25519 signature verification alone does not provide protocol-level issuer binding or exclusive ownership; acceptance binds each signature to the issuer identity committed in the signed bytes. This property may not fall between the layers. [REGISTERED A1 P3, docs/phase-0-prereg-amendment-1.md:129-150]

**R-2.45** Out of scope for the cryptographic construction: an adversary who drives the legitimate issuance path with authorized credentials (misissuance). The model documents the boundary; it does not pretend to cover it. Misissuance is met by authorization controls and audit logs, not cryptography. [REGISTERED A1 §A1.3 item 7, docs/phase-0-prereg-amendment-1.md:347-353; prereg §3.1, docs/phase-0-prereg.md:388-404]

**R-2.46** Out of scope: breaking the idealized primitives — signature unforgeability, hash collision/preimage resistance, the temporal-anchor assumptions — which are the cited Layer 2 assumptions. [REGISTERED A1 §A1.3, docs/phase-0-prereg-amendment-1.md:353-355]

**R-2.47** Issuer-key compromise is not covered by any model: every symbolic model leaks channel keys only and never the issuer key, so an adversary holding the issuer key is indistinguishable from the issuer in every model. No declared maximum validity window for the issuer key, no rotation cadence, and no verifier behaviour at the window boundary is registered. [PROPOSED — docket item 26, candidate 2026-09-05, docs/band-1-docket.md:385-400] [OPEN — §11 O-19]

**R-2.48** Recorded without objection but not registered: rotation is the moment a channel's trust root is replaced and therefore the most attractive moment for a holder of a stolen key; that threat is absent from A1.3 and should be registered. [PROPOSED — docket item 26, docs/band-1-docket.md:429-433] [OPEN — §11 O-19]

**R-2.49** H0 is falsified if any A1.2 property cannot be discharged without excluding a declared A1.3 adversary capability (one of four listed weakenings). Any such weakening requires a further signed, dated amendment stating what was weakened and why; absent that amendment, Phase 1 does not begin. [REGISTERED A1 §A1.1, docs/phase-0-prereg-amendment-1.md:71-95]

---

## 3. Objects and formats

Scope: the byte-level and structural contract — what an object is, what fields it carries, who
writes each field, who checks it. Verdict semantics are §5; standing semantics are §6. Requirements
carry the source's own normative force; descriptive text is not upgraded to a MUST here.

*Provenance: every `[REGISTERED A3 …]` tag in this section rests on Amendment 3's adoption at `8ae4720`; see §0.1.*

---

### 3.1 Payload and canonical form

| Field / rule | Type / domain | Who sets | Who checks | Source |
|---|---|---|---|---|
| `payload` | JCS (RFC 8785) bytes over a JSON value in the accepted domain | issuer | verifier, by independent reconstruction | A1 §A1.2 P8 |
| canonicalization version | version identifier, recorded per layer; unknown version rejected | issuer | verifier | prereg §4.3; A1 P8 |
| non-double values | string-encoded, never a JSON number | issuer / ingestion boundary | verifier (rejection list) | prereg §4.3 |
| accepted domain | closed by explicit rejection; no normalization | — | verifier | A1 §A1.2 P8 |

**R-3.1** The canonical form binds to RFC 8785 (JSON Canonicalization Scheme, JCS) rather than a
bespoke `canonical()`; JCS is cited as Informational, not standards-track, adopted with the
precision rule below closing its gap. [REGISTERED prereg §4.3, docs/phase-0-prereg.md:496-506]

**R-3.2** Any value not exactly a double (hashes, large/256-bit integers, blockchain addresses,
opaque identifiers) is string-encoded, never a JSON number.
[REGISTERED prereg §4.3, docs/phase-0-prereg.md:502-506]

**R-3.3** `canonical()` is injective on its accepted payload domain and the encoding is
boundary-unambiguous; injectivity over that domain is discharged by direct proof.
[REGISTERED A1 §A1.2 P8, docs/phase-0-prereg-amendment-1.md:255-277]

**R-3.4** The accepted domain is closed by explicit rejection: anything outside it is refused, never
"helpfully" normalized. Rejection is required, at minimum, for duplicate object names;
`NaN`/`Infinity`; numbers not exactly representable as IEEE 754 doubles; `-0` and numeric edge
cases; non-I-JSON strings; inputs relying on Unicode normalization assumptions; unknown
canonicalization versions; trailing bytes; type-tag mismatch; length-prefix mismatch.
[REGISTERED A1 §A1.2 P8, docs/phase-0-prereg-amendment-1.md:264-273]

**R-3.5** The canonical form is frozen and explicitly versioned: it never changes silently, any
change is a new versioned canonical form, and every receipt records which version it used.
[REGISTERED prereg §4.3, docs/phase-0-prereg.md:486-494]

**R-3.6** Every canonicalization version has byte-for-byte golden examples and canonicalization test
vectors are part of the public verifier conformance suite; golden vectors evidence the positive
domain and the rejection suite the negative domain, both H1a obligations.
[REGISTERED prereg §4.3, docs/phase-0-prereg.md:508-512; A1 §A1.2 P8, docs/phase-0-prereg-amendment-1.md:273-276]

**R-3.7** The claim made for the length binding is boundary-unambiguity; no blanket
"length-extension-resistant" claim is made. [REGISTERED prereg §4.3, docs/phase-0-prereg.md:514-517]

**R-3.8** Schema validation rejects raw JSON numerics exceeding IEEE 754 exact range before
canonicalization, so string-encoding is enforced at the ingestion boundary rather than assumed of
clients. [DOCKET 4 — candidate, not registered, docs/band-1-docket.md:32-36] [OPEN — §11 O-02]

**Two byte strings, separated.** The **canonical payload bytes** are `canonical(payload)`: the JCS
(RFC 8785) serialization under the precision rule above. The **signed frame** is the framed envelope
of §3.2, whose fourth field *is* the canonical payload bytes. Signatures and anchors commit to the
signed frame, and the length is a frame field. The original §4.3 sentence "Length is bound into the
canonical bytes (not a side field)" (`docs/phase-0-prereg.md:492-494`) is superseded by A1 P8, as
A1 §A1.8 already implies, and is read from Amendment 7 on as "the length is bound into the signed
bytes"; the original is not edited. Golden vectors are owed for the two strings separately (P8: the
canonical payload bytes; the frame layout: the signed frame).
[RULED (author) 2026-09-14; instrument A7 §A7.1, PROPOSED; §12 C-03]

---

### 3.2 The frame

| Field | Type / domain | Who sets | Who checks | Source |
|---|---|---|---|---|
| `type_tag` | domain-separation tag from P7's enumerated set | issuer | verifier; mismatch rejected | A1 P7, P8 |
| `canonicalization_version` | version identifier | issuer | verifier; unknown version rejected | A1 §A1.2 P8 |
| `payload_length` | length prefix the frame supplies, JCS carrying no length header | issuer | verifier; mismatch rejected | A1 §A1.2 P8 |
| `payload` | the JCS bytes | issuer | verifier | A1 §A1.2 P8 |
| binary layout, widths, endianness | not fixed | — | — | A1 P8 [OPEN — §11 O-01] |

*Terms.* The **signed frame** is the four-field envelope tabulated above; the **canonical payload
bytes** are its fourth field, `canonical(payload)`. `payload_length` is a field of the frame and not
part of the canonical payload bytes; signatures and anchors commit to the signed frame.
[RULED (author) 2026-09-14; instrument A7 §A7.1, PROPOSED; §12 C-03]

**R-3.9** Signatures and anchors commit to a framed envelope
`type_tag || canonicalization_version || payload_length || payload`, where `payload` is the JCS
bytes; the issuer constructs the frame, the verifier reconstructs it independently and rejects any
mismatch. [REGISTERED A1 §A1.2 P8, docs/phase-0-prereg-amendment-1.md:255-264]

**R-3.10** The exact binary layout is fixed, with golden vectors, before the Band 1 freeze; it is an
outstanding obligation, not a settled specification.
[REGISTERED A1 §A1.2 P8, docs/phase-0-prereg-amendment-1.md:262-264] [OPEN — §11 O-01]

**R-3.11** The signed bytes include, at minimum: domain-separation tag, object type (per P7's
enumeration), algorithm identifier, issuer identity, key fingerprint, manifest hash, and
canonicalization version. [REGISTERED A1 §A1.2 P3, docs/phase-0-prereg-amendment-1.md:140-144]

**R-3.12** For a multi-signer attestation the six non-fingerprint fields of every required signer's
frame — object type, algorithm, identity, manifest hash, canonicalization version, payload — are
equal across signer slots; only the key-fingerprint field differs. Reading (a), common attested
content in separate signer-specific frames, is registered; if reading (b), one shared frame, was
meant, P3's field list and P8's frame change.
[RULED (author) A5 §A5.4 — ADOPTED (author), docs/phase-0-prereg-amendment-5.md:165-190 (the (a)/(b) fork at :165-179; the six-field sentence at :179-183)] [RULED — §12 C-15, A7 §A7.9]

**R-3.12a** P8's four-field signed frame and A5 §A5.4's seven signer-specific bindings (object type,
algorithm, identity, manifest hash, canonicalization version, payload, key fingerprint) both stand
and are not in conflict, *provided* an **encoding map** shows where each symbolic binding lives in
bytes: as an envelope field (type tag, canonicalization version, payload), inside the canonical
payload under P3's obligations (the A3 §A3.6.1 precedent for the algorithm identifier, docket 25's
for the forward link), or in the manifest tuple the frame commits to by hash. The map must also
separate the requester's content from the signer-specific metadata around it, so that "payload equal
across signer slots" is a statement about bytes. It is a pre-freeze obligation (§10.2; band-1 docket
item 33); until it is settled the frame layout remains open (§11 O-01, O-79) and no golden vector for
the signed frame is final. The symbolic library's seven-argument `framed` constructor is an
abstraction of both, not a byte layout.
[RULED (author) 2026-09-14; instrument A7 §A7.9, PROPOSED; §12 C-15] [OPEN — §11 O-79]

**R-3.13** As modelled the frame is the seven-field transparent constructor
`framed(objType, alg, issuerId, kfp, manifestHash, canonVer, payload)`, copied verbatim between
families and deliberately not promoted into the shared library; the in-bytes pins exercised are
`=alg`, `=id`, `=fp(kX)` with `mh = h(t)`, while object type and canonicalization version are bound
and unexercised outside S-P7, and no model claims `framed(...)` is the P8 frame.
[MODELLED LIB, formal/suite/lib/tessera_theory.pvl:77-84; MODELLED S-P3, formal/suite/s-p3/proverif/sp3_q2_degraded_compromised.pv:60, :107-109; formal/suite/s-p3/RESULTS.md:261-275]

**R-3.14** Explicit binary widths and endianness for `payload_length` and `canonicalization_version`,
for cross-language byte determinism.
[DOCKET 5 — candidate, not registered, docs/band-1-docket.md:37-40] [OPEN — §11 O-01]

---

### 3.3 Signed object types

| Type | Tag (as modelled) | Commits to | Signed by | Verdict / standing rules |
|---|---|---|---|---|
| base attestation | `OT_ATTEST` | the framed payload bytes | issuer keys in the manifest's required set | §5 |
| wrapper | `OT_WRAPPER` | inner package's exact bytes, opaque; inner and outer canonicalization versions | wrapper issuer key | §5, per layer |
| issuer-key manifest | `OT_MANIFEST` | the authority tuple / manifest bytes | manifest self-signature, possession only | §5, §3.4 |
| authority evidence | `OT_AUTHEVID` | the exact authority statement consumed | the authority channel | §5, §3.4 |
| conformance vector | `OT_CONFVEC` | one fixed-floor test case | issuer | §5 |
| review-recency attestation | `OT_REVIEWREC` | when the service was last adversarially reviewed | issuer | prereg §4.7 |
| terminal lineage record (TLR) | `OT_TLR`, body tag `TLR` | derived identity, attempt lineage, terminal disposition | the entitled key | §6 |
| portable refusal record | `OT_REFUSAL`, body tag `REFUSAL` | attempt identity, disposition, disclosable reasons, verifying evidence | generating authority | §6 |
| specification object | member added by A3; no tag recorded | the verification specification, content-addressed | issuer | §5 |
| tending record | none recorded | custodial assessment for one outcome | named custodian | §6 |
| base assessment | unsigned by decision | the evaluation-time result | nobody | §5 |
| attested verification report | "a distinct typed wrapper"; no tag recorded | the complete base result plus evaluator and environment identity | the separate report profile's signer | §5 |
| renewal wrapper | wrapper (A3.4 claim 3) | the wrapped package with its accumulated evidence | custodian | §5 [OPEN — §11 O-30] |

**R-3.15** Every signed object carries a domain-separation type tag inside the signed bytes, drawn
from the enumerated set: base attestation, wrapper, issuer-key manifest, authority evidence,
conformance vector, review-recency attestation. No trace exists in which an object of one type is
accepted as another. [REGISTERED A1 §A1.2 P7, docs/phase-0-prereg-amendment-1.md:235-240]

**R-3.16** The set gains the terminal lineage record and the portable refusal record, each with its
own domain-separation tag inside its signed bytes, no trace accepting either as another type; and it
gains the specification member, the verification specification and its conformance vectors being
embedded in each receipt bundle as typed, content-addressed objects.
[REGISTERED A4 §A4.5, docs/phase-0-prereg-amendment-4.md:144-151; REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:295-300]

**R-3.17** A wrapper commits to the inner package's exact bytes, embedded as an opaque byte string
(e.g. base64 of the inner package's framed bytes), never as parsed JSON, and outer canonicalization
must be structurally unable to re-serialize, re-escape or otherwise touch the inner byte stream.
Hash-only commitment is rejected: the inner bytes must travel inside the bundle, or P9's
self-containment fails. [REGISTERED A1 §A1.2 P7, docs/phase-0-prereg-amendment-1.md:240-248]

**R-3.18** The wrapper records both inner and outer canonicalization versions, and the verifier
checks the recorded inner version against the inner frame's own canonicalization-version field and
rejects on mismatch: the record is a checked claim, not an informational one.
[REGISTERED A1 §A1.2 P7, docs/phase-0-prereg-amendment-1.md:248-249; RULED (author) A5 §A5.5, docs/phase-0-prereg-amendment-5.md:192-200]

**R-3.19** The wrapper attests the inner bytes, never the inner verification result; wrapping never
alters the inner package's independently-computed verdict.
[REGISTERED A1 §A1.2 P7, docs/phase-0-prereg-amendment-1.md:249-253]

**R-3.20** As modelled the wrapper embedding is `wrap(cvInner, (innerBytes, innerSig))` carried as
the payload of `framed(OT_WRAPPER, …)`; the inner manifest, authority evidence and possession proof
are presenter-supplied outside that pair and no query states package completeness.
[MODELLED S-P7, formal/suite/s-p7/proverif/sp7_q2_degraded_compromised.pv:94-96, :316-318; formal/COVERAGE-MAP.md:55] [OPEN — §11 O-70]

**R-3.21** The complete portable refusal record carries attempt identity, disposition, reasons that
may be disclosed, and the evidence needed to verify it; the transition entering `REFUSED` also
creates its non-identifying public commitment value, delivery status `PENDING` and publication
status `PENDING`. [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:572-581]

**R-3.22** The commitment construction must resist practical guessing or correlation of identifying
fields under its declared threat model; it corroborates a disclosed record and does not reconstruct
a lost one. [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:648-653] [OPEN — §11 O-07]

**R-3.23** One signing act at terminal disposition produces the disposition fact — (attempt
identity, terminal disposition) — and both disposition-bearing records are projections of that one
signed fact: the TLR adds the attempt lineage, the portable refusal record adds the disclosable
reasons and the public commitment value. Whether the projections are one object or two remains
unpreferred. [RULED (author) SC-2 2026-08-31/09-04, formal/spike/standing-probe/DECISION.md:96-115]

**R-3.24** As probed, the TLR is signed by the entitled key and binds derived identity, lineage and terminal
disposition; a TLR under any other key returns `STANDING_EVIDENCE_SIGNATURE_INVALID`. The source records this
as G0 "pass (evidential)" and adds "the probe is a stub fixture; this is design evidence, not conformance."
[MODELLED standing-probe G0 (Q2/Q3), formal/spike/standing-probe/DECISION.md:61-66; the mechanism selection itself
is ADOPTED (author), :378-384 — not registered in an amendment]

**R-3.25** As modelled the standing objects are `attemptCore(t, ppf, sg, decl)` with identity derived
as `aid = h(core)`, `entry(attemptId, disposition)` inside `lineage2` (exactly two entries, which
does not generalize), `TERM_SHIPPED(id)` / `TERM_REFUSED`, and standing evidence
`withTLR(tlrKey, tlrSig, anchorProof)` or `noTLR`.
[MODELLED S-STANDING, formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:122-142]

**R-3.26** A tending record has exactly one of four outcomes — `NO_ACTION_REQUIRED`, `RENEWED`,
`ACTION_DUE`, `FAILED` — and every outcome exposes the policy and version applied, observations and
their provenance, mechanically evaluated trigger results, judgment-based conclusions, unavailable
observations, and, when applicable, the renewal-artifact reference and predecessor-link result.
[REGISTERED A3 §A3.5, docs/phase-0-prereg-amendment-3.md:384-402 — amendment text, no `[AUTHOR DECISION]` marker on this passage]

**R-3.27** The base assessment is an unsigned, reproducible computation carrying at least: identities
of the input receipt, bundle members and evidence actually evaluated; the P4 envelope-verification
result; protocol standing; a machine-readable scope for every claim; governing specification,
policy, trust configuration and declared evaluation context; material reasons, observations,
unavailable evidence and recorded waivers; and payload Representation Information status when
requested. No unqualified aggregate checkmark is part of the conforming result.
[REGISTERED A3 §A3.8, docs/phase-0-prereg-amendment-3.md:686-704; the "unsigned" choice is `[AUTHOR DECISION — ratified -- 2026-08-08]` at :722-734]

**R-3.28** A party needing portable attribution, evaluation-time evidence or tamper-evident transport
may separately attest the complete base result as a distinct typed wrapper, whose bounded claim is
that an identified evaluator assessed an identified bundle under an identified environment and
obtained the enclosed result; signer authority, key lifecycle and report policy belong to that
separate attestation profile. [REGISTERED A3 §A3.8, docs/phase-0-prereg-amendment-3.md:712-720]

**R-3.29** Long-horizon evidentiary continuity uses RFC 4998 (ERS) renewal under an RFC 4810-style
cryptographic-maintenance policy; renewal wraps, it never replaces.
[REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:273-278]

**R-3.30** Candidates, not registered: that a renewal chain is the per-layer case extended in time,
judged link by link under each link's epoch; that simple non-cumulative renewal is excluded; that a
wrap commits to the full known lineage of prior wrappers; that each epoch's wrapper is independent
testimony only through its own contemporaneous anchor. Per-prior verdict snapshots are registered
against inside the renewal wrapper and provided for by the A3.8 report wrapper instead.
[DOCKET 19-23 — candidates, not registered, docs/band-1-docket.md:245-320] [OPEN — §11 O-30 to O-34]

---

### 3.4 Manifest and authority

| Field | Type / domain | Who sets | Who checks | Source |
|---|---|---|---|---|
| issuer identity | map-v1 tuple field 1, authority-relevant | issuer, published by the channels | bound, not validated | LIB D-2; first-link |
| key fingerprint | map-v1 tuple field 2 | issuer | compared against the accepted key | first-link; S-P3 |
| signer set `sset` | map-v1 tuple field 3 | issuer | required arity read from the signed tuple | LIB D-2; S-P2 |
| algorithm id | map-v1 tuple field 4 | issuer | bound, not validated | LIB D-2 |
| statement version | map-v1 tuple field 5 | issuer | bound, not validated | LIB D-2 |
| authority evidence, per channel | `sign((STMT_DIGEST, h(tuple)), skChannel)`, or the direct form | authority channel | verifier, against the archived channel key | first-link; LIB D-1 |
| possession proof | `sign((POSS, manifest), sk)` | the manifest-named issuer key | verifier, same key whose signature is accepted | A1 §A1.5; LIB D-3 |
| required binding-form set | signed, nonempty set of form identifiers | issuer | verifier: every required form validates | first-link |
| forward-link / successor slot | inside the canonical payload; mechanism not frozen | issuer | — | DOCKET 25 [OPEN — §11 O-10] |
| algorithm identifier | inside the canonical payload; encoding open | issuer | verifier | A3 §A3.6.1 [OPEN — §11 O-03] |

**R-3.31** The bundle carries an issuer-key manifest: the issuer public keys (or references) plus
timestamped evidence that those keys were authorized issuer keys at issue time, the manifest itself
anchored; DNS and repository remain useful for finding keys and are not required to verify.
[REGISTERED prereg §4.4, docs/phase-0-prereg.md:527-535] [RULED — §12 C-04, A7 §A7.2]

**R-3.31a** "(or references)" stands, bounded. A reference in the manifest is permitted when its
target is resolvable either (i) from material inside the bundle or (ii) from an input the verifier's
declared policy explicitly names as trusted (the §2.3 trust configuration) — and never by a live
lookup. Under (ii) the reference stays inside P9's pure function, the declared policy being one of
its two arguments. A reference the verifier can resolve from neither makes the check that needs it
unperformable: `UNVERIFIABLE` for that required check, under the P4 partition. A1 §A1.5's "archived
in the bundle" for the two authority evidences is unchanged; (ii) does not license archiving an
authority evidence outside the bundle.
[RULED (author) 2026-09-14; instrument A7 §A7.2, PROPOSED; §12 C-04. "Explicitly declared" is A7's
stated reading of how P9 is preserved, recorded there so it can be corrected]

**R-3.32** The manifest carries two independent, archived, time-anchored authority-publication
evidences — the DNSSEC chain snapshot with the signature chain to the root as it existed at issue
time, and the public git commit publishing the same fingerprints with its signature, proof material
and OTS proof — plus a manifest self-signature that proves possession only and is never counted as
an authority channel. Verification uses the archive, never live repository availability.
[REGISTERED A1 §A1.2 P10, docs/phase-0-prereg-amendment-1.md:283-297; A1 §A1.5, docs/phase-0-prereg-amendment-1.md:430-442]

**R-3.33** External authority evidence must unambiguously bind the exact authority statement the
verifier consumes; two manifests differing in any authority-relevant fact must not be supportable by
the same evidence, while differences explicitly declared non-authoritative may remain outside that
binding. [REGISTERED A3 §A3.2.1, docs/phase-0-prereg-amendment-3.md:178-184]

**R-3.34** Transcription binding is the first-link mechanism discharging that invariant: authority
evidence commits to the exact versioned map-v1 authority-relevant statement through one or more
authenticated, domain-separated binding forms declared inside the signed envelope. Both the direct
form (over the canonical authority-statement representation) and the digest form (over a declared
digest of that same representation) are permitted protocol forms.
[DECIDED — first-link mechanism selection, entered by the author 2026-08-13 at `459aff0`, formal/spike/first-link/DECISION.md:1-9; text at :145-159 sits under the heading "Proposed decision" and carries no per-statement RULED/ADOPTED label (see the label discipline at :125-143); not registered in an amendment]

**R-3.35** Distinct tags per form — `STMT_DIRECT` versus `STMT_DIGEST` — make the two forms
cryptographically non-interchangeable; the tags are authenticated verification semantics, not
authority-relevant identity fields, and do not change map v1.
[DECIDED — first-link selection, formal/spike/first-link/DECISION.md:353-362 (unlabelled sections "Selected: authenticated, domain-separated forms" and "Map v1 ruling"; the enabling observation at :338-344 is the author's, 2026-08-12); MODELLED LIB D-1, formal/suite/lib/tessera_theory.pvl:144-150]

**R-3.36** Authority-relevance map v1 is the tuple (issuer identity, key fingerprint, signer set,
algorithm id, statement version), anchor identity excluded by citation. Only the key fingerprint is
compared against the accepted key; `issuerId`, `sset`, `alg` and `ver` are carried through the
binding without any policy check — the fields are bound, not validated.
[MODELLED LIB D-2, formal/suite/lib/tessera_theory.pvl:170-175; RULED (author) formal/spike/first-link/DECISION.md:237-243]

**R-3.37** An envelope carries a signed, nonempty required set of binding-form identifiers; a
verifier must successfully validate every required form, and partial success is not success. P8
defines the set's canonical encoding, ordering, uniqueness and bounds, and no inference,
negotiation, normalization or fallback is permitted during verification.
[RULED (author) — the source's own label is ADOPTED (author) 2026-08-13, "Labelled ADOPTED rather than RULED because the reasoning originated in the cross-review", formal/spike/first-link/DECISION.md:366-383]

**R-3.38** Possession is the manifest self-signature `sign((POSS, manifest), sk)`, not a signature
over a fingerprint, and must be by the same key whose signature is accepted; an existential
self-signature by another key in a multi-key manifest does not close the chain.
[REGISTERED A3 §A3.2, docs/phase-0-prereg-amendment-3.md:153-157; MODELLED LIB D-3, formal/suite/lib/tessera_theory.pvl:37-45]

**R-3.39** Anything fixed at attestation time and later used to interpret, verify, scope or evaluate
the attestation must be authenticated inside the envelope; outside statements are fungible
testimony, the artifact-derived attestation handle being the narrow exception.
[RULED (author) 2026-08-12, formal/spike/first-link/DECISION.md:338-344]

**R-3.40** The forward-link / predeclared successor slot rides inside the canonical payload under
P3's obligations, leaving P8's four-field frame unchanged, and is an independent identifier (not a
back-hash) carried inside the signed bytes; the mechanism is not frozen and may be substituted so
long as key compromise is made legible, registration completing before format freeze with a
slot-bearing golden vector.
[RULED (author) 2026-09-04, formal/spike/standing-probe/DECISION.md:368-377; DOCKET 25, docs/band-1-docket.md:355-384] [OPEN — §11 O-10]

**R-3.41** The algorithm identifier and all parameters that affect interpretation are unambiguously
parsed and cryptographically bound to the exact signed object, no substitution or alternative
interpretation preserving verification; its location is pinned inside the canonical payload under
P3's obligations with P8's four-field frame layout unchanged, leaving only the exact encoding open,
which P8's framing proof and golden vectors must fix before Band 0 exit.
[RULED (author) A3 §A3.6.1, docs/phase-0-prereg-amendment-3.md:486-502] [OPEN — §11 O-03]

---

### 3.5 Anchor and temporal evidence

| Field | Type / domain | Who sets | Who checks | Source |
|---|---|---|---|---|
| OTS proof | exactly one proof, over the receipt's canonical bytes | issuer | verifier, the shipped proof and no other | A2 §A2.4 |
| anchor txid | double-SHA-256 of the anchor transaction; in the bundle, outside the signed bytes | issuer | verifier, as identity handle only | A2 §A2.4 |
| `declared_issue_time` | issuer's claim; an existed-by claim only | issuer | verifier, temporal predicate | A1 §A1.6; A2 §A2.4 |
| `anchor_time` | Bitcoin block time of the OTS anchor | chain | verifier | A1 §A1.6 |
| `confirmed_at` | `timestamp(block at height h + k − 1)` | chain | issuer before shipping, and verifier | A2 §A2.1 |
| δ, ε, k | verifier-owned tolerances and depth; strict defaults 72 h / 24 h / 6 | verifier policy, never the receipt | verifier | A1 §A1.2 P5 |
| block headers `h … h + k − 1` | archived in the bundle or in the verifier-distributed store | issuer or trust config | verifier | A2 §A2.2 |

**R-3.42** A shipped receipt contains exactly one anchor proof (the OTS proof over its canonical
bytes) together with the anchor transaction's id, which serves as the identity handle binding the
receipt to its chain transaction — an identity/coherence handle, not by itself a retrieval
mechanism. Verification evaluates the shipped proof and no other.
[REGISTERED A2 §A2.4, docs/phase-0-prereg-amendment-2.md:299-312]

**R-3.43** The txid necessarily lives in the bundle outside the signed bytes, since the anchor is
computed over those bytes; the wrapper discipline of P7 makes the containment tamper-evident.
[REGISTERED A2 §A2.4, docs/phase-0-prereg-amendment-2.md:321-323]

**R-3.44** `declared_issue_time` is what the issuer claims and asserts only that the artifact existed
by that time; `anchor_time` is the Bitcoin block time of the OTS anchor, establishing only that the
anchored bytes existed not after that block.
[REGISTERED A1 §A1.2 temporal vocabulary, docs/phase-0-prereg-amendment-1.md:111-114, restated A1 §A1.6 at :482-491; A2 §A2.4, docs/phase-0-prereg-amendment-2.md:324-327]

**R-3.45** `confirmed_at := timestamp(block at height h + k − 1)`, the including block at height `h`
being the first confirmation (`c = tip_height − h + 1`).
[REGISTERED A2 §A2.1, docs/phase-0-prereg-amendment-2.md:80-86]

**R-3.46** A receipt records its issue-time policy version and the observed anchor delay; it may not
choose its own temporal tolerances — δ and ε belong to the verifier, not the receipt.
[REGISTERED A1 §A1.2 P5, docs/phase-0-prereg-amendment-1.md:173-177]

**R-3.47** The verifier must evaluate `confirmed_at` statelessly: block headers `h … h + k − 1` are
available either archived in the bundle or from the verifier-distributed header store, the same
trust-configuration pattern as A1.5's historical trust-anchor store. Header authentication rules are
part of that evidence obligation; bundled headers form a candidate chain segment, not proof of
canonicity. [REGISTERED A2 §A2.2, docs/phase-0-prereg-amendment-2.md:236-244; the candidate-chain-segment and header-provenance sentences are A2 §A2.1, :197-206] [OPEN — §11 O-22]

**R-3.48** Embed the k-header segment in `authority_evidence` so a standalone verifier needs no
header database; and let verifier policy pin checkpoint hashes or a minimum cumulative-work
threshold travelling with the trust configuration, absence of a pin being an explicit `UNVERIFIABLE`
case. [DOCKET 6-7 — candidates, not registered, docs/band-1-docket.md:41-49] [OPEN — §11 O-09, O-22]

**R-3.49** "Where the bundle ships before chain confirmation, it carries a pending anchor proof; **the holder
bears the upgrade duty** for their own proof". An un-upgraded proof weakens only that holder's temporal bound,
visibly.
[RULED (author) SC-1 cost (ii), adopted 2026-09-04, formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:56-58, 65-69]

---

### 3.6 The bundle

| Member | Type / domain | Who sets | Who checks | Source |
|---|---|---|---|---|
| receipt: framed bytes plus signature set | signed object | issuer | verifier | A1 P2, P8 |
| manifest, authority evidences, possession | §3.4 objects, archived | issuer | verifier | A1 §A1.5 |
| anchor proof, txid, header material | §3.5 objects | issuer | verifier | A2 §A2.2, §A2.4 |
| verification-spec identifier and hash | bound into the signed bytes | issuer | verifier | A3 §A3.4 |
| embedded specification and conformance vectors | typed, content-addressed objects | issuer | verifier / Designated Community | A3 §A3.4 |
| fixed-floor conformance vectors | the in-bundle layer of the two-layer scheme | issuer | verifier | A3 §A3.5 |
| standards-dependency manifest | layered, per external standard edition | issuer | Designated Community | A3 §A3.4 |
| Representation Information companion | optional, typed; receipt commits to its exact bytes | submitter | verifier, identity only | A3 §A3.4 |
| purpose preamble | plain-language, typed and bound | issuer | reader | A3 §A3.4 |
| standing evidence: TLR plus anchor proof | typed object, in-bundle | issuer | standing path | §6 |

**R-3.50** The bundle carries an unambiguous verification-spec identifier and its hash bound into the
signed bytes, so a verifier can prove which procedure governs; the Tessera verification
specification and its conformance vectors are embedded in each individual receipt bundle as typed,
content-addressed objects, which an aggregate preservation package may deduplicate without changing
their identity or semantics; and a plain-language purpose preamble (WIPP-marker style) is typed and
bound Representation Information for intent.
[REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:290-304]

**R-3.51** The bundle identifies, for each Tessera-verification dependency, the exact external
standard edition, the normative sections used, known-errata disposition, stable digest where
canonical bytes exist, retrieval identifier, redistribution status, and failure consequence;
Tessera-authored procedure and conformance artifacts are embedded, external standards embedded
opportunistically when lawful and otherwise precisely referenced.
[REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:342-352]

**R-3.52** Payload-interpretation dependencies travel as an optional typed Representation
Information companion; the receipt commits to the companion's exact bytes, and Tessera preserves its
identity without asserting its correctness, sufficiency, legality, availability, or the payload
meaning it proposes. [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:357-363]

**R-3.53** Conformance vectors are two layers: a fixed floor in the bundle (memorizable, and
acceptably so) and novelty minted outside the bundle as custodial practice. The fixed floor ships
the canary vector: "a signature in an algorithm you do not know; the correct verdict is
`UNVERIFIABLE`."
[REGISTERED A3 §A3.5, docs/phase-0-prereg-amendment-3.md:453-458; A3 §A3.6.2, docs/phase-0-prereg-amendment-3.md:517-520]

**R-3.54** A possessed bundle can be verified without Tessera: it carries the data (P7/P9/P10, A1.5,
A2.2), an unambiguous identifier and hash for the governing verification specification, and the
Tessera-specific procedure itself; the verdict is a pure function of the bundle and the verifier's
declared policy.
[REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:261-269; A1 §A1.2 P9, docs/phase-0-prereg-amendment-1.md:278-281]

**R-3.55** In the S-P7 models the wrapper's embedded pair carries the inner bytes and signature only;
the inner manifest, authority evidence and possession proof are presenter-supplied outside it and no
query states package completeness. Bundle completeness is recorded as a P8/H1a format obligation and
an open coverage cell. [MODELLED S-P7, formal/COVERAGE-MAP.md:55] [OPEN — §11 O-70]

**R-3.56** A declared per-bundle byte budget, above which content is carried by content-addressed
reference plus a published store; where the budget pushes transcribed authority content behind a
reference, first-link criterion 4 must be re-scored and custody of the exact referenced
representation answered before any Band 1 freeze.
[DOCKET 9, docs/band-1-docket.md:54-56; DOCKET 17, docs/band-1-docket.md:133-206; consequence recorded at first-link criterion 4 as a construction-level judgment ("PASS, WEAKLY (not query-discharged)"), formal/spike/first-link/DECISION.md:261-275] [OPEN — §11 O-08, O-42]

**R-3.57** Third-party logs are an intended consumer, so the format freeze preserves the fields a log
builder needs — issuer identity, the forward identifier, anchor evidence, and a stable indexing key
— even where no relying party needs them; no field is known to be missing (identity and manifest
hash in the signed frame, forward identifier in the payload, anchor evidence in the bundle, the
attestation's own digest as index key), so this is a preservation constraint at freeze, not an
addition. [DOCKET 27 — candidate, not registered, docs/band-1-docket.md:483-516]

---

### 3.7 Identifiers, versions and reason-code namespaces

| Identifier | Domain | Who sets | Who checks | Source |
|---|---|---|---|---|
| canonicalization version | per layer; unknown rejected | issuer | verifier | prereg §4.3; A1 P8 |
| binding-form identifier | `STMT_DIRECT`, `STMT_DIGEST`; extensible | issuer, in the required set | verifier: all required forms | first-link |
| verification-spec identity and hash | bound into the signed bytes | issuer | verifier | A3 §A3.4 |
| algorithm identifier | inside the canonical payload; encoding open | issuer | verifier | A3 §A3.6.1 |
| statement version `ver` | map-v1 tuple field 5 | issuer | bound, not validated | LIB D-2 |
| registry version / policy epoch | deferred; nothing implemented | — | — | DOCKET 18 |

**R-3.58** Each layer records which canonical form it used; wrappers record both inner and outer
canonicalization versions.
[REGISTERED prereg §3.1/§4.3, docs/phase-0-prereg.md:348-352, :508-512]

**R-3.59** Verdict namespace: `VALID_STRICT`, `VALID_DEGRADED(policy=...)`, `INVALID`,
`UNVERIFIABLE` — a typed result, never a bare `true`/`false`. Semantics are §5.
[REGISTERED prereg §4.6, docs/phase-0-prereg.md:555-562]

**R-3.60** Standing namespace as registered in the S-series table: verdict "standing" / "no standing"
with reason codes `TERMINAL_DISPOSITION_SHOWN` (S1), `SUPERSEDED` (S2),
`NO_TERMINAL_DISPOSITION_EVIDENCE` (S3), `ISSUANCE_REFUSED` (S4); S2, S3 and S4 must return pairwise
distinct reason codes.
[RULED (author) 2026-08-12 / 2026-09-04, formal/spike/first-link/DECISION.md:790-832] [RULED — §12 C-10, A7 §A7.7]

**R-3.60a** One vocabulary. The standing report's value set is A3 §A3.7.1's `ESTABLISHED` /
`ABSENT` / `UNVERIFIABLE`, each with a reason code; the S-series' "standing" / "no standing" are
readable as that series' names for `ESTABLISHED` / `ABSENT` and are not a third value. The mapping,
copied from A7 §A7.7 with the reason codes retained and pairwise distinct as registered:

| Row | S-series verdict | Standing value | Reason code |
|-----|------------------|----------------|-------------|
| S1 | standing | `ESTABLISHED` | `TERMINAL_DISPOSITION_SHOWN` |
| S2 | no standing | `ABSENT` | `SUPERSEDED` |
| S3 | no standing | `ABSENT` | `NO_TERMINAL_DISPOSITION_EVIDENCE` |
| S4 | no standing | `ABSENT` | `ISSUANCE_REFUSED` |
| — | — | `UNVERIFIABLE` | `STANDING_EVIDENCE_MALFORMED` (SC-3, internally inconsistent evidence) |
| — | — | `UNVERIFIABLE` | `STANDING_EVIDENCE_TEMPORAL_MISMATCH` (SC-3, the TLR's anchor failing A2.1) |

The H1a standing vectors carry the mapped values. The two probe-observed codes
`STANDING_EVIDENCE_MISMATCH` and `STANDING_EVIDENCE_SIGNATURE_INVALID` are not registered by this
ruling and stay open.
[RULED (author) 2026-09-14; instrument A7 §A7.7, PROPOSED; §12 C-10] [OPEN — §11 O-75]

**R-3.61** Standing namespace as registered in the standing-probe and SC-3 texts: `ESTABLISHED` /
`ABSENT` / `UNVERIFIABLE`. Two of the four standing-error codes are registered and two are not.
`STANDING_EVIDENCE_MALFORMED` and `STANDING_EVIDENCE_TEMPORAL_MISMATCH` are RULED by SC-3 —
internally inconsistent standing evidence yields `UNVERIFIABLE` and never `ESTABLISHED`.
`STANDING_EVIDENCE_MISMATCH` and `STANDING_EVIDENCE_SIGNATURE_INVALID` are probe-observed only: the
cited scoring passage names them among "Distinct defined outcomes observed" under a finding headed
"pass with remediation (evidential)" and routes additions for registration; no amendment or exit
condition registers them, so §3's output schema does not freeze them.
[REGISTERED A3 §A3.7.1 for the `ESTABLISHED` / `ABSENT` / `UNVERIFIABLE` triple, docs/phase-0-prereg-amendment-3.md:542-546; RULED (author) 2026-09-04 (SC-3) for `STANDING_EVIDENCE_MALFORMED` and `STANDING_EVIDENCE_TEMPORAL_MISMATCH`, formal/spike/first-link/DECISION.md:834-847] [MODELLED standing probe, formal/spike/standing-probe/DECISION.md:116-129, for `STANDING_EVIDENCE_MISMATCH` and `STANDING_EVIDENCE_SIGNATURE_INVALID`] [OPEN — §11 O-75] [RULED — §12 C-10, A7 §A7.7]

**R-3.62** Binding-form reason codes: a well-formed identifier unknown to the verifier and one known
but unsupported must not share a reason code, and unknown identifiers are `UNVERIFIABLE`, never
`INVALID`. [RULED (author) 2026-08-13, formal/spike/first-link/DECISION.md:393-405]

**R-3.63** The envelope reason code `KEY_FINGERPRINT_MISMATCH` exists, and a bundle failing it must
not receive a standing report computed against an unentitled key; the entitled-key binding is
checked inside the standing path. [Suite obligation carried from the blind re-scoring — not an author ruling and not registered in an amendment, formal/suite/ENUMERATION.md:502-509]

**R-3.64** A degraded verdict records, for each waived check, the policy that authorized the waiver
and the verifier's observation of the waived evidence — at least the six values absent,
unperformable, invalid, anchor-late, names-other-key, would-pass. The record format is an H1a
obligation on the band-1 docket.
[RULED (author) A5 §A5.3, docs/phase-0-prereg-amendment-5.md:134-155; DOCKET 28, docs/band-1-docket.md:62-66] [OPEN — §11 O-06]

**R-3.65** As modelled the standing report carries (verdict, reason, key, tuple, derived identity)
with branch labels `PATH_S2`/`PATH_S3`/`PATH_S4`, so a discrimination judge can detect two branches
emitting the same reason code.
[MODELLED S-STANDING, formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:144-159, :175-176]

**R-3.66** Reason-carrying output is a conformance requirement, not a rendering nicety: no standing
because no lineage context was presented and no standing because lineage was presented and this
artifact was superseded must not collapse into one output.
[RULED (author) 2026-08-12, formal/spike/first-link/DECISION.md:748-768]

**R-3.67** Retrieval failure for externally referenced verification inputs yields `UNVERIFIABLE` with
a reason code distinguishing *not retrieved* from other unverifiable causes.
[DOCKET 17 — candidate, not registered, docs/band-1-docket.md:168-172]

---

## 4. Issuance protocol

Scope: the issuer's behaviour from ingestion to a shipped receipt or a latched refusal. Verifier behaviour is §5/§6; standing *reporting* is §7. Requirements below carry the normative force of their source and no more.

---

### 4.1 Step 1 — Ingestion and rejection

**Consumes:** a submitted payload plus the requested issuance parameters. **Produces:** either a payload inside P8's accepted domain, or a rejection. **Invariant kept:** the accepted domain is closed by explicit rejection.

**R-4.1** The accepted payload domain is closed by explicit *rejection*: anything outside it is refused, never "helpfully" normalized. [REGISTERED A1 P8, docs/phase-0-prereg-amendment-1.md:264-273]

**R-4.2** Rejection is required at minimum for: duplicate object names; `NaN`/`Infinity`; numbers not exactly representable as IEEE 754 doubles; `-0` and numeric edge cases; non-I-JSON strings; inputs relying on Unicode normalization assumptions; unknown canonicalization versions; trailing bytes; type-tag mismatch; length-prefix mismatch. [REGISTERED A1 P8, docs/phase-0-prereg-amendment-1.md:264-273]

**R-4.3** Any value not exactly a double (hashes, large/256-bit integers, blockchain addresses, opaque identifiers) is string-encoded, never a JSON number. [REGISTERED prereg §4.3, docs/phase-0-prereg.md:502-506]

**R-4.4** Schema validation rejecting raw JSON numerics exceeding IEEE 754 exact range *before* canonicalization, so string-encoding is enforced at the boundary rather than assumed of clients, is a candidate for the Band 1 ingestion spec and conformance vectors; it is not registered. [DOCKET 4 — candidate, docs/band-1-docket.md:32-36] [OPEN — §11 O-02]

**R-4.5** Golden vectors evidence the positive domain and the rejection suite evidences the negative domain; both are H1a obligations. [REGISTERED A1 P8, docs/phase-0-prereg-amendment-1.md:273-276]

---

### 4.2 Step 2 — Canonicalize and frame

**Consumes:** the accepted payload. **Produces:** the framed envelope bytes that every signature and the anchor commit to. **Invariant kept:** `canonical()` is injective on its accepted payload domain, and the frame is reconstructible by the verifier without issuer assistance.

**R-4.6** The canonical form binds to RFC 8785 (JSON Canonicalization Scheme, JCS) rather than a bespoke `canonical()`. [REGISTERED prereg §4.3, docs/phase-0-prereg.md:496-506]

**R-4.7** The canonical form is frozen and explicitly versioned: it never changes silently; any change is a new, versioned canonical form, and every receipt records which version it used. [REGISTERED prereg §4.3, docs/phase-0-prereg.md:486-494]

**R-4.8** Signatures and anchors commit to a framed envelope, `type_tag || canonicalization_version || payload_length || payload`, where `payload` is the JCS bytes. The issuer constructs the frame; the verifier reconstructs it independently and rejects any mismatch. [REGISTERED A1 P8, docs/phase-0-prereg-amendment-1.md:255-264]

**R-4.9** The exact binary layout of the frame is fixed, with golden vectors, before the Band 1 freeze; it is not fixed in the record read here. [REGISTERED A1 P8, docs/phase-0-prereg-amendment-1.md:262-264] [OPEN — §11 O-01]

**R-4.10** Every signed object carries a domain-separation type tag inside the signed bytes, drawn from the enumerated set: base attestation, wrapper, issuer-key manifest, authority evidence, conformance vector, review-recency attestation. [REGISTERED A1 P7, docs/phase-0-prereg-amendment-1.md:235-240]

**R-4.11** The enumerated set gains two members with their own tags: the terminal lineage record and the portable refusal record (A3 §A3.7.2). [REGISTERED A4 §A4.5, docs/phase-0-prereg-amendment-4.md:144-151]

**R-4.12** The algorithm identifier rides inside the canonical payload under P3's obligations; P8's four-field frame layout is unchanged. The exact encoding is left to P8's framing proof and golden vectors. [RULED (author) 2026-08-08, A3 §A3.6.1, docs/phase-0-prereg-amendment-3.md:493-502] [OPEN — §11 O-03]

---

### 4.3 Step 3 — Sign

**Consumes:** the framed envelope bytes. **Produces:** a signature set. **Invariant kept:** each signature is bound to the issuer identity committed in the signed bytes; both signatures cover the same canonical bytes.

**R-4.13** The issuer signs with two keys from independent failure domains: KMS signs the cloud receipt to demonstrate cloud-native custody, and local GPG counter-signs to preserve a portable, independent WHO layer. Both signatures cover the same canonical bytes. Decision: C. [RULED prereg §3.1, docs/phase-0-prereg.md:273-298]

**R-4.14** The attestation carries a *set* of signatures (a JSON map of key-type to signature), not an AND/OR rule; verification policy lives with the verifier, not frozen into the receipt. [REGISTERED prereg §3.1, docs/phase-0-prereg.md:307-311]

**R-4.15** The signed bytes include, at minimum: domain-separation tag, object type (per P7's enumeration), algorithm identifier, issuer identity, key fingerprint, manifest hash, and canonicalization version. [REGISTERED A1 P3, docs/phase-0-prereg-amendment-1.md:129-150]

**R-4.16** For a multi-signer attestation, the six non-fingerprint fields of every required signer's frame (object type, algorithm, identity, manifest hash, canonicalization version, payload) are equal across signer slots; only the key-fingerprint field differs. [RULED (author) A5 §A5.4, docs/phase-0-prereg-amendment-5.md:156-190]

**R-4.17** Reading (a) governs R-4.16: common attested content in separate, signer-specific frames. If the author meant (b), one shared frame, P3's field list and P8's frame change and the S-P2 addendum is withdrawn. [RULED (author) C8, formal/suite/ROUTED-2026-09-06.md:470-479; stated as correctable at docs/phase-0-prereg-amendment-5.md:166-182]

**R-4.18** Revocation is terminal: a revoked key is never re-authorized; re-keying issues a *new* key with a new fingerprint and a new manifest entry. This is a design commitment the model assumes and operational policy enforces, deliberately not filed under Layer 2. [REGISTERED A1 P6, docs/phase-0-prereg-amendment-1.md:216-224]

**R-4.19 (OPERATIONS)** The commit-signing key (Tyst, ed25519, `...42C73835`) is passphraseless with a 6-month TTL (expires 2026-12-07) on a firewalled workstation. Host compromise is an accepted threat, mitigated by short TTL plus an already-generated revocation certificate. The text states this would NOT be acceptable for a production root-of-trust. [REGISTERED prereg §4.2, docs/phase-0-prereg.md:454-463]

**R-4.20 (OPERATIONS)** Trigger to revisit: if anyone relies on issued attestations, shorten the TTL toward monthly *and* move to the deferred enclave/HSM model. [REGISTERED prereg §4.2, docs/phase-0-prereg.md:465-469]

**R-4.21 (OPERATIONS)** Key material is never logged; the control is structured logging that cannot serialize key types plus a CI secret-scan gate that fails the build if signing material reaches a log sink. [REGISTERED prereg §4.1, docs/phase-0-prereg.md:447-452]

**R-4.22 (OPERATIONS)** No declared maximum validity window for the *issuer* key, no rotation cadence, and no verifier behaviour at the window boundary is registered anywhere in the record. [DOCKET 26 — candidate, docs/band-1-docket.md:385-400] [OPEN — §11 O-19]

**R-4.23 (OPERATIONS)** The execution model by which the service edge invokes the firewalled local GPG signer, and the attempt-loop behaviour when that signer is unreachable, are unspecified; a transient partition must not manufacture a false `REFUSED` terminal state. [DOCKET 1 — candidate, docs/band-1-docket.md:11-17] [OPEN — §11 O-14]

---

### 4.4 Step 4 — Manifest and authority evidence

**Consumes:** issuer public keys, the archived channel evidences, the map-v1 authority-relevant statement. **Produces:** the issuer-key manifest carried in the bundle. **Invariant kept:** the bundle is self-contained; verification touches no live channel.

**R-4.24** The bundle carries an issuer-key manifest: the issuer public keys (or references) plus timestamped evidence that those keys were authorized issuer keys at issue time, the manifest itself anchored. DNS/repo remain useful for *finding* keys; they are not required to *verify*. [REGISTERED prereg §4.4, docs/phase-0-prereg.md:527-535] [RULED — §12 C-04, A7 §A7.2]

**R-4.25** The manifest carries two independent, archived, time-anchored authority-publication evidences (the DNSSEC chain snapshot and the anchored repository publication, A1.5) plus a manifest self-signature by the issuer keys. [REGISTERED A1 P10, docs/phase-0-prereg-amendment-1.md:283-297]

**R-4.26** Evidence 1 is the `wamason.com` DNSSEC records publishing the issuer-key fingerprints, with the signature chain to the root as it existed at issue time, archived in the bundle. [REGISTERED A1 §A1.5, docs/phase-0-prereg-amendment-1.md:430-433]

**R-4.27** Evidence 2 is the public git commit publishing the same fingerprints, with the commit object, its signature, the relevant proof material, and the OTS proof archived in the bundle; verification uses the archive, never live repository availability. [REGISTERED A1 §A1.5, docs/phase-0-prereg-amendment-1.md:434-438]

**R-4.28** The manifest self-signature is proof of possession only. It binds the manifest bytes to the asserted keys and is never counted as authority evidence: an attacker's invented key self-signs for free. [REGISTERED A1 §A1.5, docs/phase-0-prereg-amendment-1.md:439-442]

**R-4.29** Transcription binding is the §A3.2.1 first-link mechanism: authority evidence commits to the exact versioned map-v1 authority-relevant statement through one or more authenticated, domain-separated binding forms declared inside the signed envelope. [DECIDED 2026-08-13, formal/spike/first-link/DECISION.md:145-152]

**R-4.30** Two binding forms are permitted protocol forms: the direct form commits to the canonical authority-statement representation; the digest form commits to a declared digest of that same representation. Distinct tags per form, `STMT_DIRECT` versus `STMT_DIGEST`, make the two cryptographically non-interchangeable. [DECIDED, formal/spike/first-link/DECISION.md:153-159, 353-357]

**R-4.31** The map-v1 authority-relevant tuple is (issuer identity, key fingerprint, signer-set, algorithm id, statement version). [MODELLED LIB D-2, formal/suite/lib/tessera_theory.pvl:170-175]

**R-4.32** The tuple's fields are *bound*, not *validated*. Only the key fingerprint is compared against the accepted key; `issuerId`, `sset`, `alg` and `ver` are carried through the binding without any policy check. [DECIDED, formal/spike/first-link/DECISION.md:237-243]

**R-4.33** Binding-form tags are authenticated verification semantics, not authority-relevant identity fields; distinct tags do not change map v1. [RULED (author) 2026-08-12, formal/spike/first-link/DECISION.md:359-363]

**R-4.34** Anything fixed at attestation time and later used to interpret, verify, scope, or evaluate the attestation must be authenticated inside the envelope; outside statements are fungible testimony. The artifact-derived attestation handle is the narrow exception. [RULED (author) 2026-08-12, formal/spike/first-link/DECISION.md:338-344]

**R-4.35** Tessera records the representation version, binding form, hash algorithm where applicable, and the guarantees claimed at issuance. It supports algorithm agility but does not promise that an issuance-time assumption remains adequate forever. [DECIDED, formal/spike/first-link/DECISION.md:310-317]

**R-4.36 — envelope re-verification at ship.** The issuer does not re-run envelope verification at ship. Exactly, from the panel repair: "the bridge model's Ship guard is the three-conjunct temporal predicate plus the burial-depth requirement (its header registers exactly this), and the issuer does not re-run envelope verification (P1–P3) at ship." The §A3.9 obligations summary states the other reading in one line: "A2.1 prose repair (issuer ships on full `VALID_STRICT`)." Both readings stand in the same signed amendment; neither is withdrawn. [REGISTERED A3 §A3.7.3, marker `[PANEL-DRIVEN REPAIR — 2026-08-08, from the Kimi addendum, clerk-verified against the model]`, docs/phase-0-prereg-amendment-3.md:665-673; docs/phase-0-prereg-amendment-3.md:832] [RULED — §12 C-08, A7 §A7.6]

---

### 4.5 Step 5 — Anchor

**Consumes:** the framed, signed bytes and `declared_issue_time`. **Produces:** an OTS proof plus the anchor transaction id. **Invariant kept:** a receipt never ships on a shallow anchor, and no shipped receipt can be orphaned by a tolerated reorganization.

**R-4.37** Issuance is not complete until the anchor is confirmed, buried at a minimum confirmation depth k on the Bitcoin chain (strict default k = 6), within δ of `declared_issue_time`. [REGISTERED A1 P5 corollary, docs/phase-0-prereg-amendment-1.md:186-197]

**R-4.38** Confirmation vocabulary: the anchor transaction is included in the block at height `h`; the including block is the first confirmation, so `c = tip_height − h + 1`, and the block granting the k-th confirmation has height `h + k − 1`. Define `confirmed_at := timestamp(block at height h + k − 1)`. [REGISTERED A2 §A2.1, docs/phase-0-prereg-amendment-2.md:80-86]

**R-4.39** Issuance is complete only if `confirmed_at ≤ declared_issue_time + δ`. [REGISTERED A2 §A2.1, docs/phase-0-prereg-amendment-2.md:87-89]

**R-4.40** The issuer evaluates that conjunct as part of the full three-conjunct temporal predicate (the P5 temporal test inside `VALID_STRICT`) before shipping. Evaluation of conjunct 3 alone is insufficient and is forbidden. [REGISTERED A2 §A2.1, docs/phase-0-prereg-amendment-2.md:91-98; authoritative prose repair REGISTERED A3 §A3.7.3, docs/phase-0-prereg-amendment-3.md:654-663]

**R-4.41** The three conjuncts are `declared_issue_time − ε ≤ anchor_time`; `anchor_time ≤ declared_issue_time + δ`; `confirmed_at ≤ declared_issue_time + δ`. [REGISTERED A2 §A2.2, docs/phase-0-prereg-amendment-2.md:218-224]

**R-4.42** The model convention pin is `DepthK = k − 1`, because P5c's `depth` counts blocks mined after inclusion; for the strict default k = 6, `DepthK = 5`. [REGISTERED A2 §A2.1, docs/phase-0-prereg-amendment-2.md:208-214]

**R-4.43** As modelled, the Ship guard is `~shipped /\ anchorH # NoAnchor /\ Len(chain) >= IssuerDesignatedH /\ declared - Epsilon <= chain[anchorH] /\ chain[anchorH] <= declared + Delta /\ IssuerConfirmedTs <= declared + Delta`, with `IssuerDesignatedH == anchorH + DepthK`. [MODELLED Bridge, formal/tla/P5cP5P6_Bridge.tla:145-153, 168-178]

**R-4.44** The pin is checked, not assumed: `PinAgreement == DepthK = KConf - 1` is an invariant, deliberately not an `ASSUME`, so an off-by-one in transcription or cfg goes red. [MODELLED Bridge, formal/tla/P5cP5P6_Bridge.tla:26-30, 188-192]

**R-4.45 (OPERATIONS)** Wall time governs the attempt lifecycle: the service waits through `declared + δ + S` before treating an attempt as expired, where S ≥ 0 is an operational slack constant (working default S = 24 h, sized to the observation path). [RULED (author) 2026-07-21 clock roles, registered A2 §A2.1, docs/phase-0-prereg-amendment-2.md:106-113]

**R-4.46** No global bound on the backward observation lag B − C is assumed; the guarantee registered is conditional on the observable antecedent: if B − C ≤ S for an attempt whose predicate holds, that attempt has a live shipping opportunity at eligibility. [REGISTERED A2 §A2.1, docs/phase-0-prereg-amendment-2.md:113-130]

**R-4.47** Timeliness is latched at eligibility; eligibility observed at exactly `B = declared + δ + S` is timely, the boundary being inclusive and latch-winning. Expiry applies only strictly after the boundary and only to attempts with no timely-latched eligibility. [RULED, registered A2 §A2.1, docs/phase-0-prereg-amendment-2.md:130-135, 150-160] [SETTLED — §12 S-12]

**R-4.48** If the predicate fails at issuance time, the attempt is discarded and re-issued per the P5 corollary, subject to the attempt bound of A2.3. [REGISTERED A2 §A2.1, docs/phase-0-prereg-amendment-2.md:160-162]

**R-4.49** Re-issue uses a fresh declared time and re-anchors; the failed attempt is discarded, not shipped. `declared_issue_time` asserts the artifact existed by that time; re-declaration on re-issue moves it forward, which weakens and never falsifies. [REGISTERED A1 P5 corollary, docs/phase-0-prereg-amendment-1.md:186-197; A2 §A2.4, docs/phase-0-prereg-amendment-2.md:324-327]

**R-4.50** Reorg handling is scoped, not modelled: anchors at depth ≥ k are treated as permanent, a Layer 2 assumption exposed and not discharged; the P5c `Reorg` action is guarded on `depth < DepthK` and re-checking the correspondence under reorg is not discharged by the bridge. [REGISTERED A1 §A1.6, docs/phase-0-prereg-amendment-1.md:500-511; MODELLED P5c, formal/tla/P5c_IssuanceProtocol.tla:83-86, 231-241; SCOPED-OUT Bridge, formal/tla/P5cP5P6_Bridge.tla:43-69]

**R-4.51** A discarded attempt's transaction confirming later confers nothing; the Ship guard, not the anchor action, makes the late anchor worthless. [REGISTERED A2 §A2.4, docs/phase-0-prereg-amendment-2.md:307-312; MODELLED P5c, formal/tla/P5c_IssuanceProtocol.tla:209-229]

**R-4.52** A miner may set `timestamp(h + k − 1)` forward within the consensus bound, pushing an honest issuance into the tail case; this is a griefing surface bounded to hours against δ = 72 hours and can force a re-issue, never a false verdict. [REGISTERED A2 §A2.2, docs/phase-0-prereg-amendment-2.md:182-185]

---

### 4.6 Step 6 — Bounded attempts and refusal

**Consumes:** the attempt counter and the wall clock. **Produces:** either a further attempt or a latched refusal with its local records. **Invariant kept:** refusal is entered atomically and latches; reporting failure never reopens issuance.

**R-4.53** Issuance makes at most N attempts. Fail-closed means issuance must be able to end in refusal, not only in success. [REGISTERED A2 §A2.3, docs/phase-0-prereg-amendment-2.md:252-262]

**R-4.54** Exhausting the attempts obligates the implementation to terminate issuance in an explicit refusal, durably recorded: a first-class protocol outcome, not an error path. [REGISTERED A2 §A2.3, docs/phase-0-prereg-amendment-2.md:266-270]

**R-4.55** `MaxAttempts` is promoted from a state-space bound to protocol semantics; the refusal state is modelled by atomic entry, the transition expiring the final attempt's window recording the refusal in the same step. [REGISTERED A2 §A2.3, docs/phase-0-prereg-amendment-2.md:278-284]

**R-4.56** As modelled, there is no separately enabled `Refuse` action: `refused' = (refused \/ (~shipped /\ attempts = MaxAttempts /\ now + 1 > declared + Delta))` and `refusedAt' = IF refused' /\ ~refused THEN now + 1 ELSE refusedAt`, inside `Tick`. [MODELLED P5c, formal/tla/P5c_IssuanceProtocol.tla:199-207, 189-198]

**R-4.57** `RefusalLatched == [][refused => refused']_vars`; the latch proves logical persistence only, not storage durability, retrievability, or reporting. [MODELLED P5c, formal/tla/P5c_IssuanceProtocol.tla:332-337, 47-61]

**R-4.58** The boundary race at `now = declared + Delta` is intentional and named in the module: Ship's `now <= declared + Delta` and the refusal trigger `now + 1 > declared + Delta` both hold there, and the scheduler chooses. Both branches are safe and the outcomes are mutually exclusive. [MODELLED P5c, formal/tla/P5c_IssuanceProtocol.tla:248-259]

**R-4.59** Termination is a contract obligation on the implementation, not a proven liveness property: the model proves the conditional safety half only, no fairness being assumed. [REGISTERED A2 §A2.3, docs/phase-0-prereg-amendment-2.md:284-290]

**R-4.60** `REFUSED` latches atomically when A2.3's terminal condition occurs; it is final and independent of all later reporting states. Delivery or publication failure cannot reopen issuance, consume another attempt, or erase the refusal. [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:569-572]

**R-4.61** The same transition creates, as local durable state (creation is neither delivery nor publication): the complete portable refusal record; its non-identifying public commitment value; delivery status `PENDING`; and publication status `PENDING`. [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:572-581]

**R-4.62** The complete portable refusal record carries attempt identity, disposition, reasons that may be disclosed, and the evidence needed to verify it. [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:576-578]

**R-4.63** Handoff state machine: the generating authority retains the complete record until the first of `ACKNOWLEDGED` (a declared custodian, the submitter by default, confirms possession of a record that verifies against the commitment value), `DELIVERY_FAILED` (a non-retryable delivery failure is established), or `DELIVERY_EXPIRED` (the declared bounded retention horizon ends without acknowledgment). [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:583-589]

**R-4.64** Failure and expiry are visible terminal dispositions, never silent deletion; the retained record's subsequent disposition follows the declared minimization and retention policy, and that disposition is itself recorded. [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:589-592]

**R-4.65** Publication is a separate state machine: `PENDING`; `PUBLISHED`, only on acknowledgment from the declared external channel; `PUBLICATION_FAILED`; `PUBLICATION_EXPIRED`. [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:599-602]

**R-4.66** Creating the commitment value is not publication, and the handoff acknowledgment does not substitute for the channel's; conflating the two acknowledgments would hide the crash interval this decomposition exposes. [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:602-605]

**R-4.67 — the pre-handoff death interval, a named impossibility.** If the authority dies after the local refusal transition but before handoff and publication, no surviving observer holds evidence of the refusal disposition; even the failure statuses die with the authority. Tessera minimizes the interval, retries while alive, refuses to report the reporting workflow as complete, and names this residual rather than disguising it as `PUBLICATION_FAILED`. [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:623-632]

**R-4.68** The interval costs the auditability of the refusal, never the integrity of what can be claimed on it: under §A3.7.1 no artifact lacking terminal-disposition evidence can claim protocol standing. [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:632-637]

**R-4.69** Emission with verified handoff is the discharge moment; after acknowledgment, continued availability of the complete record is a custodial dependency under the §A3.4 survivability floor. The handoff mechanism remains open. [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:592-597] [OPEN — §11 O-18]

**R-4.70** The retention horizon and the post-terminal minimization policy are declared per deployment; no value is fixed. [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:583-592] [OPEN — §11 O-48]

**R-4.71 — registered but unmodelled.** The extended atomic-entry invariant, "every transition entering `REFUSED` simultaneously establishes the complete local refusal record, the commitment value, delivery = `PENDING`, and publication = `PENDING` (the archived P5c proof covers the latch alone)", with a primary broken companion latching refusal while postponing or omitting one of those creations and a second companion in which `DELIVERY_FAILED` or any reporting state re-enters issuance or decrements the attempt bound, both to go red, is registered against the P5c module and is not modelled. Tracker row `A3.7.2`, status `open`, artifact "—". [REGISTERED A3 §A3.9, docs/phase-0-prereg-amendment-3.md:814-831; tracker formal/PROPERTIES.md:48, 260]

**R-4.72 (OPERATIONS)** While the authority lives, the submitter and a declared operational monitor can observe pending and failed states; after `PUBLISHED`, the public can observe the external trace under the channel's declared assumptions. The reporting surface is not frozen. [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:614-621] [OPEN — §11 O-18]

**R-4.73 (OPERATIONS)** Refusal reporting is issuance-time operational machinery, not §A3.5 tending; the two may share implementation later without sharing registration. [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:616-619]

---

### 4.7 Step 7 — Ship

**R-4.74** A shipped receipt contains exactly one anchor proof (the OTS proof over its canonical bytes) together with the anchor transaction's id, which serves as the identity handle binding the receipt to its chain transaction. [REGISTERED A2 §A2.4, docs/phase-0-prereg-amendment-2.md:299-307]

**R-4.75** The txid is an identity/coherence handle, not by itself a retrieval mechanism; txid to transaction availability requires chain access and is an implementation obligation under the evidence discipline. [REGISTERED A2 §A2.4, docs/phase-0-prereg-amendment-2.md:299-307]

**R-4.76** The txid necessarily lives in the bundle outside the signed bytes, since the anchor is computed over those bytes; the P7 wrapper discipline makes the containment tamper-evident. [REGISTERED A2 §A2.4, docs/phase-0-prereg-amendment-2.md:321-323]

**R-4.77** An anchor not shipped inside a receipt confers no validity, no priority, and no claimed anchor identity in verification or dispute. [REGISTERED A2 §A2.4, docs/phase-0-prereg-amendment-2.md:307-312]

**R-4.78** No verifier policy, and no downstream marketplace rule, may order competing receipts by declared time (first-to-file semantics). [REGISTERED A2 §A2.4, docs/phase-0-prereg-amendment-2.md:327-333] The rule's bearer is Tessera and its own surfaces (R-1.10a). [RULED — §12 C-06, A7 §A7.4]

**R-4.79** As modelled, a shipped receipt satisfies `shipped => (anchorAt # NoAnchor /\ anchorAt >= declared /\ anchorAt <= declared + Delta /\ depth >= DepthK)` and `~shippedOrphaned`. [MODELLED P5c, formal/tla/P5c_IssuanceProtocol.tla:288-303]

**R-4.77a (the ship guard)** The §A3.7.3 panel-driven repair governs: the issuer ships on A2 §A2.2's
three temporal conjuncts plus burial depth `DepthK = k − 1`, and does not re-run envelope
verification (P1–P3) at ship. The §A3.9 obligations summary line "A2.1 prose repair (issuer ships on
full `VALID_STRICT`)" (`docs/phase-0-prereg-amendment-3.md:832`) is the unrepaired wording and is
superseded; it is not edited in its own file.
[RULED (author) 2026-09-14; instrument A7 §A7.6, PROPOSED; §12 C-08. A7 reads the author's "burial
death" as "burial depth", the `DepthK` conjunct of the bridge's `Ship` guard]

**R-4.80** As modelled at the seam, `shipped => VerdictValid(declared, anchorH)` and `shipped => (IssuerDesignatedH = VerifierDesignatedH(anchorH) /\ IssuerConfirmedTs = VerifierConfirmedTs(anchorH))`. [MODELLED Bridge, formal/tla/P5cP5P6_Bridge.tla:194-207] [SETTLED — §12 S-10]

---

### 4.8 Step 8 — Standing: the terminal lineage record

**R-4.81** Cryptographic validity alone confers no protocol standing. Any artifact claiming standing must present verifiable standing evidence binding its issuance identity, attempt lineage, and terminal disposition. Missing standing evidence leaves the artifact evidentially admissible but without protocol standing. [REGISTERED A3 §A3.7.1, docs/phase-0-prereg-amendment-3.md:531-535]

**R-4.82** The terminal lineage record (TLR) is the selected standing-evidence mechanism. [RULED (ADOPTED author) 2026-08-31, entered 2026-09-04, formal/spike/standing-probe/DECISION.md:3-26, 378-398]

**R-4.83** The probe's TLR is signed by the entitled key and binds derived identity, lineage, and terminal disposition; a TLR under any other key returns `STANDING_EVIDENCE_SIGNATURE_INVALID`. The source states its own boundary: "the probe is a stub fixture; this is design evidence, not conformance." [PROPOSED (probe scoring draft; DECISION.md:28 retains "Status: PROPOSED — scoring draft, nothing decided."), formal/spike/standing-probe/DECISION.md:61-67]

**R-4.84** The TLR must be handle-bound, not ordinal-bound: the handle-bound TLR rejects both transplants, the ordinal-bound variant accepts both. [PROPOSED (probe scoring draft, gate G1; DECISION.md:28), formal/spike/standing-probe/DECISION.md:68-71]

**R-4.85 — SC-2.** One signing act at terminal disposition produces the disposition fact, (attempt identity, terminal disposition); both disposition-bearing records are projections of that one signed fact: the TLR adds the attempt lineage, the portable refusal record adds the disclosable reasons and the public commitment value. Whether the projections are one object or two remains unpreferred. [RULED (ADOPTED author) 2026-08-31, text adopted 2026-09-04, formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:96-116]

**R-4.86 — SC-1.** At terminal disposition the issuer submits the TLR's digest to the anchoring channel, and the resulting anchor proof travels in the bundle beside the TLR. The verifier evaluates the registered A2.1 predicate against the TLR's anchor with the TLR's declared terminal-disposition time in place of the declared issue time: `confirmed_at := timestamp(block at height h + k − 1)`, `confirmed_at ≤ declared_terminal_time + δ`, with the A2.2 anchor-time lower-bound conjunct under ε. [RULED (ADOPTED author) 2026-09-04, formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:22-47]

**R-4.87 — SC-1 boundary.** The anchor bounds *when* standing evidence could have been fabricated, to the [−ε, +δ] window about the declared terminal disposition, and does not narrow *whether* a second, contradictory TLR exists within that window. [RULED, formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:48-54]

**R-4.88 — SC-1 costs, adopted with the amendment.** (i) A second anchoring event per issuance at terminal disposition, after the shipped attempt's anchor confirms; anchor-channel unavailability at that moment is an issuance failure mode of A2.3's class and must be treated by the refusal machinery, not absorbed silently. (ii) Where a bundle ships before confirmation it carries a pending anchor proof and the holder bears the upgrade duty. (iii) δ is bounded below by anchor-confirmation latency. (iv) Complete standing evidence is late by construction. [RULED (ADOPTED author) 2026-09-04, formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:56-81]

**R-4.89 — SC-3.** Internally inconsistent standing evidence yields `UNVERIFIABLE` with `STANDING_EVIDENCE_MALFORMED` and never `ESTABLISHED`; a TLR whose anchor fails the A2.1 predicate against its declared terminal-disposition time yields `UNVERIFIABLE` with `STANDING_EVIDENCE_TEMPORAL_MISMATCH`. [RULED (ADOPTED author) 2026-09-04, formal/spike/first-link/DECISION.md:834-847]

**R-4.90 — S-series.** S1 lineage-present and the artifact is the shipped anchor gives standing, `TERMINAL_DISPOSITION_SHOWN`; S2 lineage-present and superseded gives no standing, `SUPERSEDED`; S3 lineage-absent, presented alone, gives no standing, `NO_TERMINAL_DISPOSITION_EVIDENCE`; S4 lineage-present whose terminal disposition is `REFUSED` gives no standing, `ISSUANCE_REFUSED`. S2, S3 and S4 must return pairwise distinct reason codes. [DECIDED 2026-08-12 and RULED 2026-09-04, formal/spike/first-link/DECISION.md:790-832] [RULED — §12 C-10, A7 §A7.7]

**R-4.91** The TLR is carried, not maintained; the service's duty is punctual, not custodial. Everything the standing report needs is in the bundle. [RULED (ADOPTED author) at adoption; the wording at :386-390 is the collaborator's record of the author's in-session resolution, his own quoted words there being "Item 5 adopted.", formal/spike/standing-probe/DECISION.md:130-140, 386-390]

**R-4.92** The TLR does not detect equivocation: two TLRs from the entitled key each report `ESTABLISHED` in their own bundle. [PROPOSED (probe scoring draft, gate G4; DECISION.md:28), formal/spike/standing-probe/DECISION.md:78-82]

**R-4.93** Whether an issuer holding two identities on one key keeps one terminal lineage record or two is explicitly not decided. [REGISTERED A5 §A5.6, docs/phase-0-prereg-amendment-5.md:214-219] [OPEN — §11 O-36]

**R-4.94 — D1, the forward-link slot.** The predeclared successor slot will be registered; the mechanism is not frozen and may be substituted under the criterion that key compromise be made legible. The slot rides inside the canonical payload under P3's obligations, leaving P8's four-field frame unchanged. The forward identifier is an independent identifier, not a back-hash, carried inside N's signed bytes. Registration completes before format freeze. [RULED (author) 2026-09-04, DOCKET 25, docs/band-1-docket.md:355-384; formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:159-206] [OPEN — §11 O-10]

**R-4.95** The TLR chains attempts within one issuance, backward; the slot chains issuances across the service's life, forward. [RULED, formal/spike/standing-probe/DECISION.md:344-366]

**R-4.96** As adopted with the selection, the log-and-receipt enrichment remains separately registrable per issuance class and never load-bearing. [RULED (ADOPTED author) sub-ruling 5, formal/spike/standing-probe/DECISION.md:378-384; the fuller "remains available as a separately registered, never-load-bearing option per issuance class" at :313-321 sits under "RECOMMENDED (not adopted, and carrying the scorer's non-blindness)", and the composition wording at :185-195 is labelled "an input to the rule-3 fork, not a selection"]

---

### 4.9 Step 9 — Tending obligations at issuance; publication of the commitment

**R-4.97** No §A3.5 tending obligation falls on the issuer at issuance. Tending is custodial assessment with its own record, and refusal reporting is expressly not tending. [REGISTERED A3 §A3.5, docs/phase-0-prereg-amendment-3.md:384-405; A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:616-619]

**R-4.98** What issuance owes §A3.5 is the bundle's fixed floor of conformance vectors, memorizable and acceptably so; novelty is minted outside the bundle as custodial practice. [REGISTERED A3 §A3.5, docs/phase-0-prereg-amendment-3.md:453-458]

**R-4.99** The bundle's fixed floor ships the canary vector: "a signature in an algorithm you do not know; the correct verdict is `UNVERIFIABLE`". [REGISTERED A3 §A3.6.2, docs/phase-0-prereg-amendment-3.md:517-520]

**R-4.100** Tending health never changes a receipt's P4 verdict or protocol standing. [REGISTERED A3 §A3.5, docs/phase-0-prereg-amendment-3.md:418-419]

**R-4.101** The cadence parameter lives in each custodial policy or profile, not as one universal constant. [RULED A3 §A3.5, docs/phase-0-prereg-amendment-3.md:447-452] [OPEN — §11 O-47]

**R-4.102** The base protocol does not require public disclosure of the complete refusal record; a deployment profile may require it for a declared issuance class. [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:639-642]

**R-4.103** The commitment construction must resist practical guessing or correlation of identifying fields under its declared threat model. [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:648-650]

**R-4.104** The commitment corroborates a disclosed record and does not reconstruct a lost one; absent a separately registered transparency mechanism, it does not prove that every refusal was published. No construction is named. [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:650-653] [OPEN — §11 O-07]

**R-4.105 (OPERATIONS)** The publication channel must declare its survival, availability, privacy and inclusion assumptions, and the independence of its failure modes from the declared refusal triggers, or the correlation. [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:605-612]

**R-4.106** Tessera does not maintain a foundational auditor-membership registry: the submitter may disclose its portable record to an auditor, who verifies it against the published commitment. [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:642-648]

---

### 4.10 As registered vs as modelled — issuance protocol

| # | Registered sentence | P5c / bridge implementation | Divergence |
|---|---|---|---|
| 1 | "issuance makes at most **N attempts**" (A2 §A2.3:252-262) | P5c `MaxAttempts = 3`, enforced by `Init` and `Reissue`'s guard, no separate invariant | Bridge models **one attempt**: no `Reissue`, no refusal, no attempt bound (`P5cP5P6_Bridge.tla:43-69`) |
| 2 | Clock roles: chain time governs evidence, wall time the lifecycle (A2 §A2.1:106-113) | P5c uses **one fused clock**, `now` reading as the wall clock at S = 0 (`P5c_IssuanceProtocol.tla:34-45, 78-82`); bridge **decouples** wall time from `chain` | P5c's fusion is the divergence; the decoupled seam is checked only in the bridge |
| 3 | Ship on the full three-conjunct predicate plus burial depth (A2 §A2.1:91-98; A3 §A3.7.3:665-675) | P5c Ship guard: `depth >= DepthK /\ now <= declared + Delta` (`:243-266`) | P5c's fused guard is **locally stronger**, not equivalent; it carries no ε side and no explicit `confirmed_at`. Bridge Ship carries all three conjuncts |
| 4 | Verifier's `VALID_STRICT` temporal test, three conjuncts (A2 §A2.2:218-224) | Bridge `VerdictValid(d,h)` (`:161-166`) | None at the bridge; P5c has no verifier |
| 5 | Two-sided window, ε bounds post-dating (A1 P5:159-171) | P5c `ShippedIsSound` requires `anchorAt >= declared` (`:294-303`) | **Stronger than the registered ε-tolerant bound**; the ε side is unrepresentable under the fused clock (`:78-82`) |
| 6 | Expiry only strictly after the boundary, and only for attempts with no timely-latched eligibility (A2 §A2.1:150-160) | P5c `ExpiredCannotShip == (~shipped /\ now > declared + Delta) => ~ENABLED Ship` (`:305-310`) | **Stronger than registered**; P5c is the pre-latch S = 0 instance. Latch semantics live in `P5cP5P6_BridgeSlack_Latch.tla`, declared ruling evidence, not protocol semantics |
| 7 | Boundary tie is inclusive and latch-winning (A2 §A2.1:150-160) | P5c: at `now = declared + Delta` both Ship and the refusal trigger hold; the scheduler chooses (`:248-259`) | The module names the race as **intentional**; the registered latch would exclude it |
| 8 | Refusal entered atomically and latches (A2 §A2.3:278-284) | P5c: no separate `Refuse`; `refused`/`refusedAt` set inside `Tick` (`:199-207`) | None for the latch |
| 9 | Entering `REFUSED` also establishes the record, the commitment value, delivery `PENDING`, publication `PENDING` (A3 §A3.9:814-831) | Not modelled; `refused` is a Boolean (`:47-61`) | **Registered but unmodelled**; tracker row `A3.7.2` `open`, artifact "—" (`formal/PROPERTIES.md:48`) |
| 10 | Termination on exhaustion (A2 §A2.3:284-290) | Not proven; `Tick` and `Reissue` are postponable (`:62-76`) | Contract obligation, not a liveness property |
| 11 | Anchors at depth ≥ k are permanent (A1 §A1.6:500-511) | P5c `Reorg` guarded on `depth < DepthK`, `reorgs < 2` (`:231-241`); bridge has no reorgs | Precondition, not a result; reorg re-verification of the seam **not discharged** |
| 12 | Strict default k = 6 (A1 P5 corollary:186-190) | P5c cfg `DepthK = 2` (k = 3); bridge cfg `KConf = 3`, `DepthK = 2` | **k = 3 checked, k = 6 registered**; `PinAgreement` checks only `DepthK = KConf − 1` [RULED — §12 C-13, A7 §A7.8] |
| 13 | `confirmed_at` is chain-visible to both sides (A2 §A2.1:80-98) | P5c has no explicit `confirmed_at`; bridge computes `IssuerConfirmedTs` and `VerifierConfirmedTs(h)` independently and joins them (`:145-159, 194-201`) | P5c cannot express the quantity; the join exists only in the bridge |
| 14 | Headers unavailable yields `UNVERIFIABLE` (A2 §A2.2:245-248) | Bridge: verdict operators evaluated only under definedness guards (`:70-75`) | The `UNVERIFIABLE` arm is **out of scope** in the bridge; tracked open |

**Ruling note on row 3 (2026-09-14).** The registered sentence row 3 compares against is the ship
guard as the §A3.7.3 repair states it — the three temporal conjuncts plus burial depth, with no
envelope re-verification at ship (R-4.77a). The §A3.9 summary line is superseded and is not a second
registered reading. Row 3's divergence is unchanged: it is P5c's fused guard, not the guard's
content. [RULED (author) 2026-09-14; instrument A7 §A7.6, PROPOSED; §12 C-08]

---

## 5. Verification procedure

The verifier is P9's pure function: bundle plus declared policy in, verdict out. Everything below is that function. Nothing below may consult a service.

### 5.1 Inputs

**R-5.1** The verdict is a pure function of the bundle and the verifier's declared policy; no service-side state and no live network dependency appears in the decision. [REGISTERED A1 §A1.2 P9, docs/phase-0-prereg-amendment-1.md:278-281]

**R-5.2** An attestation must verify with the service dead: the verification path touches no database, no live service, and no cloud reachability. [REGISTERED prereg §4.4, docs/phase-0-prereg.md:519-525]

**R-5.3** If the verifier requires anything from an optional service, it is fundamentally broken. An enumeration or observability API may feed a log and may never feed a verdict. [RULED (author) 2026-09-06, docs/band-1-docket.md:520-530] [RULED A4 §A4.6, docs/phase-0-prereg-amendment-4.md:176-182]

**R-5.4** The bundle supplies, at minimum: the framed bytes of every layer; the signature set; the issuer-key manifest, comprising the authority tuple (issuer identity, key fingerprint, signer set, algorithm identifier, statement version) and its authority-relevant statement; the two archived, time-anchored external authority evidences (DNSSEC chain snapshot; anchored repository publication) plus the manifest self-signature as proof of possession; the OTS anchor proof and the anchor transaction id as identity handle; the block headers `h … h + k − 1` where they are not in the header store; standing evidence where standing is claimed; the verification-spec identifier and hash; the embedded specification and conformance-vector objects; the standards-dependency manifest; the purpose preamble; and any typed payload Representation Information companion. [REGISTERED A1 §A1.5, docs/phase-0-prereg-amendment-1.md:430-448; A2 §A2.2, docs/phase-0-prereg-amendment-2.md:236-244, :299-307; A3 §A3.4/§A3.9, docs/phase-0-prereg-amendment-3.md:290-304, :754-759]

#### Bundle field to consuming check

| Bundle member | Consumed by | Source |
|---|---|---|
| Framed bytes `fb` per layer, `type_tag \|\| canonicalization_version \|\| payload_length \|\| payload` | V2–V5, V17, V19, V32 | A1 §A1.2 P8, a1:255-264 |
| Object-type field inside the frame | V4, V8 | A1 §A1.2 P7, a1:235-240 |
| Algorithm identifier inside the canonical payload | V13–V15 | A3 §A3.6.1, a3:486-502 |
| Signature set, one signature per required signer slot | V19, V28–V31 | prereg §3.1, p0:307-311 |
| Issuer-key manifest / authority tuple `authTuple(id, kfpr, sset, alg, ver)` | V18, V22, V23, V28 | A1 §A1.2 P10, a1:283-297; library D-2 |
| Authority evidence 1: archived DNSSEC chain snapshot | V20, V23 | A1 §A1.5, a1:430-433 |
| Authority evidence 2: anchored repository publication with commit object, signature, proof material and OTS proof | V20, V23 | A1 §A1.5, a1:434-438 |
| Manifest self-signature (possession only, never an authority channel) | V24 | A1 §A1.5, a1:439-442 |
| Required binding-form identifier set (signed, nonempty) | V21 | first-link/DECISION.md:366-383 |
| OTS anchor proof over the canonical bytes | V33a, V33–V36 | A2 §A2.4, a2:299-307 |
| The anchor proof's merkle path and the block it authenticates | V33a: binds the receipt's canonical bytes to the block used for V33–V36's depth and timestamp comparisons | A2 §A2.4, a2:316-320 |
| Anchor transaction id (identity handle, outside the signed bytes, inside the P7 wrapper) | anchor identity only; not a retrieval mechanism | A2 §A2.4, a2:299-323 |
| Block headers `h … h + k − 1`, or the verifier-distributed header store | V35–V38 | A2 §A2.2, a2:236-244 |
| Standing evidence: TLR key, TLR signature, anchor proof | V27, V40, standing branch | standing-probe/DECISION.md:61-67 |
| Attempt core (evidenced tuple, possession proof, attestation signature, declared time) | V27; identity derived as `aid = h(core)`, never read from a label | A3 §A3.7.1, a3:531-535, registers only that standing evidence must bind "issuance identity, attempt lineage, and terminal disposition"; the `attemptCore` composition and `aid = h(core)` are [MODELLED S-STANDING ss_q1d:328-329, :352] |
| Verification-spec identifier and its hash, bound into the signed bytes | proof of which procedure governs | A3 §A3.4, a3:290-294 |
| Embedded Tessera specification and conformance vectors, as typed content-addressed objects | reconstructability; the fixed conformance floor | A3 §A3.4, a3:295-300 |
| Layered standards-dependency manifest | dependency closure layers 1–3 | A3 §A3.4, a3:342-352 |
| Purpose preamble (WIPP-marker style) | intent, before checkability | A3 §A3.4, a3:301-304 |
| Optional typed payload Representation Information companion | payload interpretability only; never the P4 verdict | A3 §A3.4, a3:357-364 |

**R-5.5** The declared policy supplies the waiver set. Only members of the A1.2.1 waivable class may appear in it: accepting a subset of the issue-time signature set (P2); accepting fewer than all external manifest-authority evidences (P10); accepting a signature whose trust root is no longer independently recoverable, where the remaining checks pass. [REGISTERED A1 §A1.2.1, docs/phase-0-prereg-amendment-1.md:319-323]

**R-5.6** The waivable P10 item is bounded to fewer, but never zero: redundant members of the A1.5 evidence set may be waived; the final complete chain may not be broken or eliminated. [REGISTERED A3 §A3.2, docs/phase-0-prereg-amendment-3.md:139-145]

**R-5.7** No policy may waive canonical-byte integrity (P1, P8), type/domain separation (P7), boundary framing (P8), key-to-issuer binding for every accepted signature (P3), or temporal-anchor consistency (P5). [REGISTERED A1 §A1.2.1, docs/phase-0-prereg-amendment-1.md:309-317]

**R-5.8** The trust configuration is distributed with the verifier, not with the bundle, and comprises: the authority channels' public keys; the confirmation depth `k`; the tolerances δ and ε; and the archived historical trust-anchor store (DNS root keys and repository signing keys, by validity period). Distribution with the verifier is what keeps P9 intact. [REGISTERED A1 §A1.5, docs/phase-0-prereg-amendment-1.md:459-469 — these lines register only the archived historical trust-anchor store and its distribution with the verifier; δ and ε as verifier-owned are A1 §A1.2 P5, docs/phase-0-prereg-amendment-1.md:173-184. The authority channels' public keys and `k` as members of the trust configuration appear only in the modelled probe enumeration below, not in registered text] [MODELLED standing probe Q6: "Pre-bundle inputs: trust configuration only (channel public keys, `k`, `δ`). Everything else read from the bundle", formal/spike/standing-probe/RESULTS-PROBE.md:41]

**R-5.9** δ and ε belong to the verifier, not the receipt. A receipt records its issue-time policy version and the observed anchor delay; it may not choose its own temporal tolerances. [REGISTERED A1 §A1.2 P5, docs/phase-0-prereg-amendment-1.md:173-177] [MODELLED P5/P6 `ReceiptIndependence`, formal/tla/P5P6_TemporalRevocation.tla:201-221]

**R-5.10** A verifier MUST NOT consume: any live DNS lookup or live repository fetch (discovery channels only); any Tessera service endpoint; any third-party log; any custodial or tending record; any verifier-local history of prior evaluations; and any receipt-declared temporal tolerance. [REGISTERED prereg §4.4, docs/phase-0-prereg.md:527-535; A1 §A1.5, docs/phase-0-prereg-amendment-1.md:434-438; A3 §A3.5, docs/phase-0-prereg-amendment-3.md:415-419, :700-702] [REGISTERED A1 §A1.2 P5, docs/phase-0-prereg-amendment-1.md:173-177, for the receipt-declared tolerance; A4 §A4.6, docs/phase-0-prereg-amendment-4.md:181-182, for the log ("An enumeration or observability API may feed a log and may never feed a verdict.")] [REGISTERED A5 §A5.1's three stateful verifiers `LIVE_FALLBACK`, `LIVE_FAILCLOSED`, `REPLAY_LATCH`, docs/phase-0-prereg-amendment-5.md:65-80 — those lines report what the two-machine vector fails to catch; they state no prohibition. "Any verifier-local history of prior evaluations" has no registered prohibition sentence of its own and rests on P9's purity clause]

**R-5.11** Evaluation of waived evidence is bounded by the bundle and the declared inputs; inability to evaluate is itself a recorded observation and never a reason to consult anything. [RULED A5 §A5.3, docs/phase-0-prereg-amendment-5.md:150-153]

**R-5.12** Custodial health and tending state are not inputs to the base receipt verdict. (The cited lines do not mention refusal-reporting state; A3 §A3.7.2's reporting states are not addressed there.) Tending health never changes a receipt's P4 verdict or protocol standing. [REGISTERED A3 §A3.5/§A3.8, docs/phase-0-prereg-amendment-3.md:418-419, :700-702]

**R-5.13** A manifest entry expressed as a reference is permitted exactly when the verifier can resolve it from the bundle or from an input the declared policy names as trusted (§2.3); a reference requiring a live lookup is inconsistent with R-5.1 and is never resolved. An unresolvable reference does not fail the bundle by itself: it makes the check that needs it unperformable, `UNVERIFIABLE` for that required check. [RULED (author) 2026-09-14; instrument A7 §A7.2, PROPOSED; R-3.31a] [RULED — §12 C-04, A7 §A7.2]

### 5.2 The decision procedure, in order

**R-5.14** The four verdicts partition all outcomes; the procedure below assigns exactly one. A required check that fails yields `INVALID`; a required check that cannot be performed yields `UNVERIFIABLE`, never any `VALID` state. [REGISTERED A1 §A1.2 P4, docs/phase-0-prereg-amendment-1.md:152-157] [RULED A4 §A4.2 "required" qualifier, docs/phase-0-prereg-amendment-4.md:100-109]

**R-5.15** Each layer of a wrapped package is evaluated independently and carries its own complete evidentiary chain; the procedure below runs once per layer. [REGISTERED A3 §A3.2 item 4, docs/phase-0-prereg-amendment-3.md:158-164]

#### Stage order

| Stage | Content | Is the order registered? |
|---|---|---|
| (a) | Parse and P8 rejection | Yes in effect: a frame that does not reconstruct has no fields to check. The rejection list is registered, the sequence within it is not |
| (b) | Object type and wrapper handling, per layer | No. A5 §A5.5 (a5:192-200) registers the check and the rejection, not its position. Modelled only: [MODELLED S-P7 places the §A5.5 re-destructure before `event AcceptOuter` and before `InnerCheck`, sp7_q2:326-330] |
| (c) | Algorithm identifier | Not registered as an ordinal position; the verdict boundary is registered |
| (d) | Key binding | Modelled order: evidence → tuple destructure → fingerprint → possession → signature → frame → manifest hash, identical in S-P3, S-P1, S-P2, S-P7 and S-STANDING |
| (e) | Manifest authority and possession | Not registered. Modelled: the first link precedes the fingerprint match in every model |
| (f) | Signature-set completeness | Not registered as an ordinal position. Modelled: arity is read from the signed tuple before any slot is checked (sp2_q2:195-196, 213-214) |
| (g) | Integrity | Not registered. Modelled: the attestation-signature check is the last `checksign` in stage (d); the frame destructure and the manifest-hash equality follow it (row (d)'s own order), so it is not stage (d)'s last step |
| (h) | Temporal | All three conjuncts are evaluated together (R-5.19); their internal order is not registered |
| (i) | Revocation | The window's bounds are registered (A1 §A1.2 P6, a1:199-233); "so it follows (h)" is an unregistered inference of this document, not a recorded ordering |
| (j) | Partition and precedence | Last: the verdict is a function of the whole per-check outcome map, not of evaluation order (R-5.26) |

**R-5.16** No stage order may make the verdict depend on evaluation order. The fail-versus-unperformable precedence exists precisely to prevent that. [RULED A4 §A4.2, docs/phase-0-prereg-amendment-4.md:88-98]

#### (a) Parse and P8 rejection

| # | Check | Predicate | Property | On failure | Registered | Modelled | Registered vs modelled |
|---|---|---|---|---|---|---|---|
| V1 | Canonicalization version not unknown | the source's predicate is the rejection list's "unknown canonicalization versions": a canonicalization version unknown to the verifier is rejected | P8 | `INVALID` | A1 §A1.2 P8, a1:264-273; the rejection list at a1:267-273 | none | Gap: no P8 proof, no golden vectors, no rejection suite; COVERAGE-MAP row 9. A canonicalization version the verifier recognizes but does not implement is a different case, which the cited source neither equates to this one nor gives a verdict [OPEN — §11 O-78] |
| V2 | Frame reconstruction | verifier independently reconstructs `type_tag \|\| canonicalization_version \|\| payload_length \|\| payload` and rejects any mismatch | P8 | `INVALID` | A1 §A1.2 P8, a1:255-264 | none | Gap: exact binary layout unfixed [OPEN — §11 O-01] |
| V3 | Trailing bytes | no bytes after the declared payload length | P8 | `INVALID` | A1 §A1.2 P8, a1:264-273 | none | Gap |
| V4 | Type-tag match | frame's type tag = the tag the caller is verifying against | P7, P8 | `INVALID` | A1 §A1.2 P8, a1:264-273 | S-P7 `=OT_ATTEST` / `=OT_WRAPPER` frame pins | Modelled as a term pin, not a byte comparison |
| V5 | Length-prefix match | `payload_length` = actual payload length | P8 | `INVALID` | A1 §A1.2 P8, a1:264-273 | none | Gap |
| V6 | JCS domain rejection | reject duplicate object names; `NaN`/`Infinity`; numbers not exactly IEEE 754 doubles; `-0` and numeric edge cases; non-I-JSON strings; inputs relying on Unicode normalization | P8 | `INVALID`, never "helpfully" normalized | A1 §A1.2 P8, a1:264-273 | none | Gap: byte-encoding attacks are unrepresentable in every symbolic family and are recorded there as "a coverage failure, not an unreachable attack" |
| V7 | Retrieval of anything outside the envelope | none is required; where a check nonetheless cannot obtain its input | P9 | `UNVERIFIABLE` with a reason distinct from every failure reason, confined outside the envelope verdict: "Retrieval failure yields `UNVERIFIABLE` with a reason code distinguishing *not retrieved* from other unverifiable causes, and per item 16 must not contaminate the base verdict" | docket 17, docs/band-1-docket.md:133-145, :163-171 | none | [DOCKET 17 — candidate, not a member of the check map]: V7 is not in `Checks` and never enters the R-5.25 aggregation, and the candidate names no alternative result destination; no owner assigned for retention, replication, discovery, or retrieval-testing [OPEN — §11 O-42] |

**R-5.17** The accepted domain is closed by explicit rejection: anything outside it is refused, never normalized. [REGISTERED A1 §A1.2 P8, docs/phase-0-prereg-amendment-1.md:264-273]

**R-5.18** No inference, negotiation, normalization, or fallback is permitted during verification. [ADOPTED (author) 2026-08-13, formal/spike/first-link/DECISION.md:366-383; the source declines the RULED label at :369-372]

#### (b) Object type and wrapper handling, per layer

| # | Check | Predicate | Property | On failure | Registered | Modelled | Registered vs modelled |
|---|---|---|---|---|---|---|---|
| V8 | Domain-separation type tag inside the signed bytes | frame's `objType` ∈ {base attestation, wrapper, issuer-key manifest, authority evidence, conformance vector, review-recency attestation, specification, terminal lineage record, portable refusal record}; no object of one type accepted as another | P7 | `INVALID` | A1 §A1.2 P7, a1:235-240; A3 §A3.4, a3:295-300; A4 §A4.5, a4:144-151 | S-P7 `let framed(=OT_ATTEST, …)` sp7_q2:298; `let framed(=OT_WRAPPER, …)` sp7_q2:324; `TypeConfused` unreachable | Three enumerated object types plus `OT_TLR`/`OT_REFUSAL` are declared but unexercised; the manifest, possession proof and authority evidence have no object-type field at all and are distinguished "by constructor, not by tag"; open cell |
| V9 | Opaque inner embedding | wrapper commits to `wrap(cvInner, (innerBytes, innerSig))` as an opaque byte string; outer canonicalization structurally unable to re-serialize, re-escape or touch it; hash-only commitment rejected | P7 | `INVALID` | A1 §A1.2 P7, a1:240-248 | S-P7 Q4 opaque control green; two re-serialization companions red | Modelled by construction only; no query states the commitment relation. Concrete opacity of the embedding is P8's and is the family's largest Layer 2 residual |
| V10 | Recorded inner canonicalization version | re-destructure the inner frame with the wrapper's recorded version pinned in the canonicalization-version position; reject on mismatch | P7 | `INVALID` | A5 §A5.5, a5:192-200 | S-P7 Q7 `let framed(otIv, algIv, idIv, kfpIv, mhIv, =cvIw, plIv) = fbI`, sp7_q2:326-330; companion Q7-C red on exactly `VersionLied` | Checks two fields for equality and nothing more; it does not check that either version is supported or that the bytes were produced under it |
| V11 | Verdict independence per layer | inner verdict = the same inner bundle's standalone verdict, under every P4 verdict value | P7 | wrapper never alters the inner verdict | A1 §A1.2 P7, a1:248-253; A6 §A6.1, a6:31-56 | S-P7 Q4 control + companions | Discharge completed only by an H1a conformance vector, not yet built [DOCKET 32 — candidate] |
| V12 | Package completeness | the inner manifest, authority evidence and possession proof travel inside the bundle | P7, P9 | not specified | A1 §A1.2 P7, a1:240-248 | not modelled; presenter-supplied in every S-P7 model | Open coverage cell, COVERAGE-MAP amendment note 1 |

#### (c) Algorithm identifier

| # | Check | Predicate | Property | On failure | Registered | Modelled | Registered vs modelled |
|---|---|---|---|---|---|---|---|
| V13 | Identifier binding | identifier and all interpretation-affecting parameters unambiguously parsed and cryptographically bound to the exact signed object; located inside the canonical payload under P3 | A3 §A3.6.1 | no substitution or alternative interpretation may preserve verification | A3 §A3.6.1, a3:486-502 | S-P3/S-P1/S-P2/S-P7 pin `=alg` between tuple and frame | Modelled as a field comparison; the identifier is never used to select an algorithm. Exact encoding open [OPEN — §11 O-03] |
| V14 | Unsupported algorithm | well-formed, correctly bound, but unsupported identifier | A3 §A3.6.2 | `UNVERIFIABLE`, "for exactly one case" | A3 §A3.6.2, a3:503-505 | not modelled | PROPERTIES row `A3.6.2`, status `open`, artifact "—". "Exactly one case" bounds **this check's** outcomes only: within the algorithm-identifier check, one and only one input shape yields `UNVERIFIABLE`. Every other required check yields `UNVERIFIABLE` independently when it cannot be performed (P4, A4 §A4.2); the standing dimension's `UNVERIFIABLE` is a value of the orthogonal assessment, not a P4 verdict [RULED — §12 C-07, A7 §A7.5] |
| V15 | Malformed algorithm handling | missing identifier; identifier/signature encoding mismatch; malformed parameters; an identifier prohibited by applicable policy; substitution of the signed identifier; a known algorithm whose signature fails | A3 §A3.6.2 | `INVALID` | A3 §A3.6.2, a3:505-508 | not modelled | Same open row; the registered fail-open broken companion ("a verifier that fail-opens past an unknown algorithm must go red") does not exist |

#### (d) Key binding

| # | Check | Predicate | Property | On failure | Registered | Modelled | Registered vs modelled |
|---|---|---|---|---|---|---|---|
| V16 | Fingerprint slot match | `if fp(kX) = kfpr then` | P3 | `INVALID` (reason `KEY_FINGERPRINT_MISMATCH`) | A1 §A1.2 P3, a1:129-150 | S-P3 sp3_q2:103; S-P1 sp1_q2:173; S-P2 per slot sp2_q2:197,215-216; S-P7 sp7_q2:295 | `fp` is a free constructor in the models; the implementation depends on the fingerprint function's collision resistance; Layer 2 |
| V17 | In-bytes binding pattern | `let framed(ot, =alg, =id, =fp(kX), mh, cv, pl) = fb in` | P3 | `INVALID` | A1 §A1.2 P3, a1:129-150 | S-P3 sp3_q2:107-108 | `ot`, `mh`, `cv`, `pl` are bound, not pinned, at this line. `ot` and `cv` are bound and not checked at this layer; the obligation to validate them is not S-P3's but P7's (object type) and P8/H1a's (canonicalization version). The model headers are accurate as they stand; the two S-P3 reading-aid rows that list the fields inside a column of check statuses (`READING-AIDS.md:177, :302`) are corrected in place in that file with a dated marker, and no model is edited [RULED — §12 C-12, A7 §A7.10] |
| V18 | Manifest hash | `if mh = h(t) then` | P3 | `INVALID` | A1 §A1.2 P3, a1:129-150 | S-P3 sp3_q2:109 | Minimal load-bearing binding in this abstraction is the manifest hash together with the fingerprint match (S-P3 F3) |
| V19 | Attestation signature over the presented bytes | `let (=BYTES, =fb) = checksign(sg, kX) in` | P1, P3 | `INVALID` | A1 §A1.2 P1/P3, a1:116-150 | S-P1 sp1_q2:176-177 marked LOAD-BEARING; S-P3 sp3_q2:106 carried | Ed25519 verification alone does not provide protocol-level issuer binding; the P3 verification profile is an [assumption], undischarged |

#### (e) Manifest authority and possession

| # | Check | Predicate | Property | On failure | Registered | Modelled | Registered vs modelled |
|---|---|---|---|---|---|---|---|
| V20 | First link, digest form | `let (=STMT_DIGEST, =h(t)) = checksign(ev, pkS) in` (S-P3/S-P1/S-P2/S-P7 spelling; S-STANDING strict spells the two channels `checksign(evD, pkD)` / `checksign(evR, pkR)`) | A3 §A3.2.1 | `INVALID` | A3 §A3.2.1, a3:178-184; first-link DECISION.md:145-159 | S-P3 sp3_q2:101; S-P1 sp1_q2:171; S-P2 sp2_q2:194,212; S-P7 sp7_q2:293; S-STANDING ss_q1d:325-326 | Transcription binding is the selected mechanism; two forms are permitted (`STMT_DIRECT`, `STMT_DIGEST`) with distinct tags, and every suite model exercises only `STMT_DIGEST` |
| V21 | Binding-form required set | envelope carries a signed, nonempty required set of binding-form identifiers; every required form must validate; partial success is not success | A3 §A3.2.1 | unknown identifier → `UNVERIFIABLE`; known-but-unsupported → `UNVERIFIABLE` with a **different** reason code; missing, malformed, duplicate, substituted, inconsistently encoded, or empty set → `INVALID` | ADOPTED (author) 2026-08-13, first-link/DECISION.md:366-405 — the source declines the RULED label at :369-372 ("Labelled ADOPTED rather than RULED because the reasoning originated in the cross-review") | not modelled; no family carries a required-set-of-forms input | Registered but unmodelled anywhere [OPEN — §11 O-73] |
| V22 | Manifest destructuring | `let authTuple(id, kfpr, ss, alg, ver) = t in` | P10 | `INVALID` | A1 §A1.2 P10, a1:283-297 | S-P3 sp3_q2:102 and each family | Map v1 fields are **bound, not validated**: only the key fingerprint is compared; `issuerId`, `sset`, `alg`, `ver` are carried through the binding without any policy check |
| V23 | Strict authority: both channels | both external evidences validate, and both endorse the same exact authority tuple | P10 | `INVALID` | A1 §A1.2 P10, a1:283-297; A1 §A1.5, a1:444-448 | S-STANDING strict `checksign(evD, pkD)` and `checksign(evR, pkR)`, ss_q1_strict_dns_compromised.pv:355-356; spike Q1/Q3 | "Never all" is an n = 2 finite enumeration; it does not generalize. The strict rule guarantees only that *at least one uncompromised channel published this exact authority tuple* |
| V24 | Possession, chain-internal | `let (=POSS, =t) = checksign(ppf, kX) in`; possession by the same key whose signature is accepted | P10, A3 §A3.2 item 3 | `INVALID` | A1 §A1.5 item 3, a1:439-442; A3 §A3.2, a3:153-157 | S-P3 sp3_q2:104-105 (library divergence D-3) | The self-signature is never authority evidence and is never counted as an authority channel; an adversary's invented key self-signs for free. The spike signed `POSS` over the fingerprint alone; the suite corrects this |
| V25 | Degraded authority | fewer external evidences than all, under an explicit recorded policy naming which evidence was waived and why; never zero | P10, A3 §A3.2 | `VALID_DEGRADED` only under explicit recorded policy | A1 §A1.2 P10, a1:294-297; A3 §A3.2, a3:139-145 | S-P3 Q2 degraded sole-channel-compromised; P4 `ExactDegraded` | The never-zero floor is a P10-instance constraint P4's generic model does not carry [PROPOSED C7 — ROUTED-2026-09-06.md:313-322 records C6 and C7 as "settled by the collaborator, listed for veto", not as an author ruling] |
| V26 | All external evidence unperformable | every external authority evidence for a layer unavailable, unsupported, or otherwise unperformable | A3 §A3.2 item 2 | `UNVERIFIABLE`; never `VALID_DEGRADED` | A3 §A3.2, a3:146-149 | P4 `NoSilentPromotion` | Unavailability is not waiver |
| V27 | Standing tuple pin | `let attemptCore(=t, ppfS, sgS, declS) = core in`; the presented authority tuple equals the tuple embedded in the core the artifact identity is derived from | A5 §A5.6 | no else branch: the standing path emits no lineage-derived report | A5 §A5.6, a5:202-219 | S-STANDING ss_q1d:343-352; alias companion | Standing row; not in `Checks` (R-5.25). The pin sits before the lineage lookup, so supersession, refusal, malformed and mismatch reports are all conditioned on it [SETTLED — §12 S-05] |

#### The witness chain, link by link

The §A3.2 chain is the evidence floor. Each link names the check that establishes it and the model that carries it.

| Link | Established by | Modelled by | Severing companion |
|---|---|---|---|
| accepted external authority evidence | V20, V23 | S-P3 Q1 strict; spike Q1/Q3 | S-P1 strict Q1: removing the honest channel's evidence check, its key, or digest equality goes red |
| → the exact authority statement consumed from the manifest | V20 with V22 | transcription binding: `checksign(ev, pkCh)` yields `(STMT_DIGEST, h(t))` for the same `t` that is destructured | spike Q1 recut; two-worlds pair judge |
| → issuer identity and signing key | V16, V17 (`=id`, `=fp(kX)` pinned inside the frame) | S-P3 `Reattributed` unreachable | S-P3 Q3, frame unbound → `Reattributed` red |
| → proof of possession by that same key | V24 | S-P3 `PossessionTransplanted` unreachable | S-P3 Q4, naming check dropped → red via `dsks` |
| → accepted signature verifying under that key | V19 | S-P1 headline, marked LOAD-BEARING | S-P1 Q3, signature unbound from presented bytes → headline red |
| → the exact framed bytes | V19 with V2 | S-P1 ledger entry 4 (integrity / authorship correspondence) | as above; residual is P8 canonical encoding, term equality standing in for byte equality |

**R-5.34** The chain is quantified per contributing layer, and the proof obligation quantifies over every contributing layer. [REGISTERED A3 §A3.2 item 4, docs/phase-0-prereg-amendment-3.md:158-164]

#### (f) Signature-set completeness

| # | Check | Predicate | Property | On failure | Registered | Modelled | Registered vs modelled |
|---|---|---|---|---|---|---|---|
| V28 | Required arity from the signed tuple | arity read from the signed tuple's `sset` pattern, never from what the package presents | P2 | `INVALID` | A1 §A1.2 P2, a1:121-128 | S-P2 sp2_q2:195-196, 213-214; `Stripped` unreachable, severed by Q3 | Modelled for \|set\| ≤ 2 only; the set is positional. Ordering, uniqueness, bounds beyond 2, the empty set and malformed members are P8's and are unmodelled |
| V29 | Per-slot binding | `fp(kB) = kfprB`; `(=POSS, =t) = checksign(ppfB, kB)`; `(=BYTES, =fb) = checksign(sgB, kB)`; `framed(otb, =alg, =id, =fp(kB), mhb, cvb, plb) = fb`; `mhb = h(t)` | P2, P3 | `INVALID` | A1 §A1.2 P2/P3 | S-P2 sp2_q2:197-201, 215-224; `SignerForged`, `SetAltered` unreachable | `SetAltered`'s claim holds only under the fixture rule one key, one manifest |
| V30 | Common attested content | `if ota = otb then` / `if cva = cvb then` / `if pla = plb then`; the three non-fingerprint frame fields not already pinned through the shared tuple are equal across signer slots; the other three (algorithm, identity, manifest hash) are carried by the shared tuple | P2 | `INVALID` | A5 §A5.4, a5:156-190 | S-P2 sp2_q2:225-230; Q6 green, Q6-C red on exactly `Spliced` | Reading (a): common content in separate signer-specific frames. If the author meant (b), one shared frame, P3's field list and P8's frame change and the addendum is withdrawn [OPEN — §11 O-05]. Term equality stands in for byte equality; encoding and ordering are P8's |
| V31 | Set completeness | a package presenting fewer signatures than its manifest requires | P2 | `INVALID`; `VALID_DEGRADED` only under an explicit, recorded policy within the A1.2.1 waivable set | A1 §A1.2 P2, a1:121-128 | S-P2 models no waiver at all | The waived-subset case is left to P4's leg; the "recorded" half is an open coverage cell |

#### (g) Integrity

| # | Check | Predicate | Property | On failure | Registered | Modelled | Registered vs modelled |
|---|---|---|---|---|---|---|---|
| V32 | Integrity, operative form | no transition leads to an accepted receipt over altered bytes; surviving verification over altered bytes is what is hard, not altering | P1 | `INVALID` | A1 §A1.2 P1, a1:116-119; A3 §A3.1, a3:75-83 | S-P1 headline `event(AcceptedUnderHonestKey(k, fb)) ==> event(IssuerSigned(k, fb))`, sp1_q2:141-145 (the query; :198-202 is the JudgeH process that emits the event) | Non-injective by registration: replay is permitted and is caller policy. The result holds for a **closed producer set**; a same-key signing endpoint outside the fixture falsifies it (key-use discipline, a Layer 2 assumption) |

#### (h) Temporal

| # | Check | Predicate | Property | On failure | Registered | Modelled | Registered vs modelled |
|---|---|---|---|---|---|---|---|
| V33 | Anchor lower bound (ε side) | `declared_issue_time − ε ≤ anchor_time` | P5 | `INVALID` | A1 §A1.2 P5, a1:159-171; A2 §A2.2, a2:218-224 | `anchor >= declared - polEps`, formal/tla/P5P6_TemporalRevocation.tla:130-140 | Bounds post-dating |
| V33a | Receipt-to-anchor binding | the shipped anchor proof is evaluated over **this receipt's canonical bytes** and over no other proof ("Verification evaluates the shipped proof and no other"), and the block its merkle path authenticates is the block used for V33–V36's depth and timestamp comparisons ("the OTS proof's merkle path binds the anchored bytes to the block independently of the handle") | P5, A2 §A2.4 | `INVALID` | A2 §A2.4, a2:299-320 (the two quoted clauses at :307-308 and :319-320) | none: the TLA+ modules take anchor and signature validity as given — "Signature checks are abstracted as passing (that face belongs to the ProVerif models and P4); this module isolates the temporal/authorization face", formal/tla/P5P6_TemporalRevocation.tla:52-56 | Open coverage cell: nothing models the receipt-to-block binding, so a valid signature over one receipt presented together with another receipt's genuine, in-window anchor evidence is excluded by no model. V38 authenticates headers and does not supply this binding |
| V34 | Anchor upper bound (δ side) | `anchor_time ≤ declared_issue_time + δ` | P5 | `INVALID` | A1 §A1.2 P5, a1:159-171 | `anchor <= declared + polDelta`, P5P6:130-140 | Bounds backdating; backdating within the window is not eliminated, only bounded |
| V35 | Confirmation timing | `confirmed_at ≤ declared_issue_time + δ`, where `confirmed_at := timestamp(block at height h + k − 1)` | P5 as amended | `INVALID` (chain-late subclass rejected outright) | A2 §A2.1/§A2.2, a2:80-89, :218-235 | `confirmedAt <= declared + polDelta`, P5P6:130-140; `AbandonedArtifactRejected` P5P6:188-199; companion `_BrokenConf` red | The observable is the designated block's header timestamp, a chain-time proxy for burial, not a wall-clock measurement. Block timestamps are non-monotonic; `confirmed_at` may precede `anchor_time` |
| V36 | Burial depth | designated block is `anchorH + DepthK`, with `DepthK = k − 1` | P5 corollary | `INVALID` | A2 §A2.1, a2:208-214 | `PinAgreement == DepthK = KConf - 1`, formal/tla/P5cP5P6_Bridge.tla:188-192; `ShippedDesignatedAgree` :194-201; `_BrokenPin` red | The configured instances are `DepthK = 2`, `KConf = 3`, i.e. k = 3, not the registered strict default k = 6; no parameter-independence argument exists [OPEN — §11 O-44] |
| V37 | Header availability | headers `h … h + k − 1` present, from the bundle or the verifier-distributed header store | P5, P9 | `UNVERIFIABLE` | A2 §A2.2, a2:236-248 | not modelled; the bridge evaluates verdict operators only under definedness guards; the `UNVERIFIABLE` arm is out of scope | Registered conformance-vector case (headers unavailable → `UNVERIFIABLE`) tracked as an open obligation |
| V38 | Header authentication | proof-of-work validity, cumulative-work or checkpoint anchoring, store identity pinned in declared verifier policy, bundle/store conflict rules | P5 evidence obligation | not specified | A2 §A2.2, a2:197-206 | not modelled | Bundled headers are a candidate chain segment, not proof of canonicity; full specification deferred [OPEN — §11 O-22] |
| V39 | Tolerance ownership | the verdict is identical under every receipt-declared tolerance pair | P5 | receipt tolerances ignored | A1 §A1.2 P5, a1:173-184 | `ReceiptIndependence` P5P6:201-221; `VerifierOwnsTolerances` :177-186; companions `_BrokenTol`, `_BrokenTolStrict` red | `VerifierOwnsTolerances` compares against the **global** maxima, not the verifier's chosen policy; the two invariants are complementary, not nested |
| V40 | Standing evidence anchor | the same three-conjunct predicate applied to the TLR's own anchor, with the declared terminal-disposition time in place of the declared issue time | A5 §A5.6 / SC-1 | `UNVERIFIABLE` / `STANDING_EVIDENCE_TEMPORAL_MISMATCH` | standing-probe AMENDMENTS-2026-08-31.md:22-47; the forbidding of the bare phrase is at :228-234 | S-STANDING `let anchorProof(=h(tlrSig)) = ap in`, ss_q1d:341-342; carried, inert; time is not represented | Standing row; not in `Checks` (R-5.25): the `UNVERIFIABLE` is the standing report's, never the envelope verdict's. Bare "within δ" is forbidden in the registered text; the predicate must be cited explicitly |

**R-5.19** All three temporal conjuncts are evaluated together. Evaluation of the confirmation conjunct alone is insufficient and is forbidden. [REGISTERED A3 §A3.7.3, docs/phase-0-prereg-amendment-3.md:654-663] [MODELLED bridge `Ship` guard, formal/tla/P5cP5P6_Bridge.tla:168-178]

**R-5.20** A verifier may choose stricter bounds; no degraded policy may enlarge δ or ε beyond the strict maxima. Temporal-anchor consistency is non-waivable, and the P4 partition applies inside it. [REGISTERED A1 §A1.2 P5, docs/phase-0-prereg-amendment-1.md:177-184; A2 §A2.2, docs/phase-0-prereg-amendment-2.md:245-248]

#### (i) Revocation time-relativity

**R-5.21** `VALID_STRICT` requires `key_authorized(declared_issue_time)` and no revocation effective at or before `anchor_time`. Revocation effective at or before `anchor_time` yields `INVALID`. [REGISTERED A1 §A1.2 P6, docs/phase-0-prereg-amendment-1.md:199-233] Prereg §4.4 states the opposite outcome for a key revoked after issue; the conflict is not resolved here. [SETTLED — §12 S-15, A1 P6 as clarified by A4 §A4.3; see R-5.23]

**R-5.22** The registered sentence, as written by A4 §A4.3, is: "Revocation effective after both `anchor_time` and `declared_issue_time` does not retroactively change the verdict." [RULED A4 §A4.3, docs/phase-0-prereg-amendment-4.md:111-123] [MODELLED `AuthorizedThroughWindow == revoked > declared /\ revoked > anchor`, formal/tla/P5P6_TemporalRevocation.tla:142-149; `AuthorizedAtDeclared == StrictAccept => declared < revoked`, :223-233]

**R-5.23** The interval rule is deliberately stricter than point evaluation and may fail honest receipts; the only honest receipts it sacrifices are those whose key was revoked inside `(declared, anchor]`. [REGISTERED A1 §A1.2 P6, docs/phase-0-prereg-amendment-1.md:199-233] [MODELLED `HonestCostIsExactlyTheWindow`, formal/tla/P5P6_TemporalRevocation.tla:235-245] The original prereg §4.4 says such an attestation "remains `VALID_STRICT`". [SETTLED — §12 S-15, A1 P6 as clarified by A4 §A4.3]

**R-5.24** Revocation is terminal: a revoked key is never re-authorized; re-keying issues a new key with a new fingerprint and a new manifest entry. This is a design commitment assumed by the model and enforced by operational policy, deliberately not filed under Layer 2. [REGISTERED A1 §A1.2 P6, docs/phase-0-prereg-amendment-1.md:216-224]

#### (j) Partition and precedence

**R-5.25** The verdict is computed by, in order: (1) if any required check failed, `INVALID`; (2) else if any required check was unperformable, `UNVERIFIABLE`; (3) else if the waiver set is empty, `VALID_STRICT`; (4) else `VALID_DEGRADED`. Required means `Checks \ waived`. The check map `Checks` contains the envelope checks of stages (a)–(i) and those only: V27 (the standing-core tuple pin) and V40 (the TLR's temporal check) are standing checks whose outcomes feed the §6 standing report and never the envelope verdict, and V7 is a docket candidate outside the map. Standing is \"an **orthogonal assessment dimension**, not a fifth P4 state\", reported \"alongside the unchanged P4 envelope verdict\" and never folded into it; it \"is not a member of the A1.2.1 waiver lattice: it is reported, never waived\". [REGISTERED A3 §A3.7.1, docs/phase-0-prereg-amendment-3.md:542-557] [MODELLED P4 `VerdictFor(W)`, formal/tla/P4_VerifierStates.tla:94-105 — the ladder aggregates whatever belongs to `Checks` and does not itself fix that set's membership] [MODELLED S-STANDING keeps `StandingPath` and `EnvelopePath` separate, formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:322-363, :365-379]

**R-5.26** When one required check fails and another cannot be performed, the verdict is `INVALID`. A definite failure is stronger evidence than an open question; both outcomes are fail-closed; the alternative would make the verdict depend on evaluation order. [RULED (author) A4 §A4.2, docs/phase-0-prereg-amendment-4.md:88-98] [MODELLED branch order, formal/tla/P4_VerifierStates.tla:96-99]

**R-5.27** `INVALID` dominates `UNVERIFIABLE` in the binding-form required set for the same reason. [ADOPTED (author), formal/spike/first-link/DECISION.md:385-391, inside the block the source labels ADOPTED rather than RULED (:369-372)]

**R-5.28** The verdict function satisfies, for every check-outcome assignment and every legal policy: `Partition` (the verdict is one of the four); `Monotonicity` (a failed non-waivable check is `INVALID` under every policy); `NoSilentPromotion` (an unperformable non-waivable check never yields a `VALID` state under any policy); `ValidNeedsNonWaivablePass`; `StrictMeansEverything` (`VALID_STRICT` implies every check, not only the required ones, passed); `UnverifiableIsHonest`; and the four biconditional pins `ExactInvalid`, `ExactUnverifiable`, `ExactStrict`, `ExactDegraded`. [MODELLED formal/tla/P4_VerifierStates.tla:111-175]

**R-5.29** `VALID_DEGRADED` arises only from an explicit, nonempty waiver set inside the waivable class; never as a default or a fallback. [REGISTERED A1 §A1.2/§A1.2.1, docs/phase-0-prereg-amendment-1.md:152-157, :319-327] [MODELLED `DegradedNeedsExplicitWaiver`, formal/tla/P4_VerifierStates.tla:140-143]

**R-5.30** A waived check may hold any status, including `fail` and `unperformable`, without changing the verdict: required evidence that is present and whose validation is performed but fails yields `INVALID`; evidence the declared policy has waived is evaluated, its condition recorded, and never determines the verdict. [RULED A5 §A5.2, docs/phase-0-prereg-amendment-5.md:93-121] [MODELLED `ExactDegraded`, formal/tla/P4_VerifierStates.tla:174-175]

**R-5.31** The registered cost of R-5.30 is recorded: a package may be reported `VALID_DEGRADED` while its bundle carries waived evidence that is present and demonstrably fails, including one naming a different key, which is evidence of equivocation and not mere absence. [REGISTERED A5 §A5.2, docs/phase-0-prereg-amendment-5.md:123-132]

**R-5.32** In degraded mode the verifier's job is to hand the adjudicator the evidence of what could and could not be excluded, marked as degraded. A correspondence that holds in strict mode and fails in degraded mode is a registered cost of degradation, never a defect of the construction, provided the verdict says it is degraded. [RULED A4 §A4.6, docs/phase-0-prereg-amendment-4.md:156-171]

**R-5.33** R-5.32 is bounded by: "Only losses permitted by the registered waiver rules and the declared policy are degradation costs. A degraded label does not excuse violating a non-waivable requirement or misreporting a required check's outcome." [RULED A5 §A5.7, docs/phase-0-prereg-amendment-5.md:221-241]

**R-5.35** Every valid verdict requires at least one continuous accepted evidentiary chain per independently evaluated attestation layer: accepted external authority evidence → the exact authority statement consumed from the manifest → issuer identity and signing key → proof of possession by that same key → accepted signature verifying under that key → the exact framed bytes, and nothing weaker. Redundant paths may be waived; the final complete chain may not. [REGISTERED A3 §A3.2, docs/phase-0-prereg-amendment-3.md:102-121]

**R-5.36** Counted floors are prohibited: "≥1 accepted signature AND ≥1 accepted external evidence" admits the two-worlds attack, in which evidence supports manifest M′ while the accepted signature claims authority from M. Floors are linked, never counted. [REGISTERED A3 §A3.2, docs/phase-0-prereg-amendment-3.md:131-137]

**R-5.37** Every symbolic path that stops short of the acceptance event lands in `INVALID` or `UNVERIFIABLE`, never in a valid verdict. This join is cross-formalism and is never marked symbolically discharged. [RULED (author) 2026-08-29, formal/suite/ENUMERATION.md:410-418]

### 5.3 Output

**R-5.38** Verification yields one of `VALID_STRICT`, `VALID_DEGRADED(policy=...)`, `INVALID`, or `UNVERIFIABLE`: a typed result, never a bare `true`/`false`. A boolean collapses `INVALID` and `UNVERIFIABLE`, which is exactly where fail-open bugs hide. [REGISTERED prereg §4.6, docs/phase-0-prereg.md:555-562] [MODELLED `Verdicts`, formal/tla/P4_VerifierStates.tla:70]

| Verdict | Exact meaning | Source |
|---|---|---|
| `VALID_STRICT` | Registered: all issue-time signatures verify, and the waiver set is empty. Modelled only: "every check passed, not only the required ones" — no supplied registered sentence defines strict this way (see §9.3 `StrictMeansEverything`) | prereg §3.1, p0:327-337 (the state list §4.6 points to); `ExactStrict`, P4:170-172 |
| `VALID_DEGRADED(policy=...)` | Accepted under an explicit, recorded weaker policy the verifier chose, inside the A1.2.1 waivable class; every check the policy still requires passed | prereg §3.1, p0:327-337 (the state list §4.6 points to); A1 §A1.2.1, a1:319-327; `ExactDegraded`, P4:174-175 |
| `INVALID` | A required check was performed and failed | A1 §A1.2 P4, a1:152-157; `ExactInvalid`, P4:164-165 |
| `UNVERIFIABLE` | No required check failed, and at least one required check could not be performed. Never silently promoted to `VALID`. Any required check can be the one that could not be performed: A3 §A3.6.2's "exactly one case" bounds the algorithm-identifier check alone [RULED — §12 C-07, A7 §A7.5] | prereg §3.1, p0:335-337 (the state list §4.6 points to); `ExactUnverifiable`, P4:167-168 |

**R-5.39** Every `VALID_DEGRADED` verdict records the precise waived check set and the policy that authorized the waiver. [REGISTERED A1 §A1.2.1, docs/phase-0-prereg-amendment-1.md:325-327]

**R-5.40** For each waived check the record holds both the policy that authorized the waiver **and** the verifier's observation of the waived evidence: at least the six values `absent`, `unperformable`, `invalid`, `anchor-late`, `names-other-key`, `would-pass`. [RULED A5 §A5.3, docs/phase-0-prereg-amendment-5.md:134-154] `anchor-late` is an observation against **a waived redundant authority evidence's own anchor**; the receipt's own anchor conjuncts are non-waivable and a late receipt anchor is `INVALID`, never an observation (R-2.31a). [RULED — §12 C-05, A7 §A7.3]

**R-5.41** The degraded-record format is an H1a obligation. [OPEN — §11 O-06] [DOCKET 28 — candidate, docs/band-1-docket.md:62-66]

**R-5.42** The base assessment reports each layer's result without replacement by an aggregate judgment; a higher-level relying-party policy may consume those results. [RULED A3 §A3.2 item 4, docs/phase-0-prereg-amendment-3.md:161-164]

**R-5.43** The base assessment is an unsigned, reproducible computation. A mandatory signature would introduce a verifier-signing authority, key lifecycle and additional trust claim into the P9 path, while strengthening nothing about the reproduced computation itself. [RULED A3 §A3.8, docs/phase-0-prereg-amendment-3.md:686-689, :722-736]

**R-5.44** The base assessment carries at least: identities of the input receipt, bundle members, and evidence actually evaluated; the P4 envelope-verification result; protocol standing (§A3.7.1); a machine-readable scope for every claim; governing specification, policy, trust configuration, and declared evaluation context; material reasons, observations, unavailable evidence, and recorded waivers; and payload Representation Information status when requested. [REGISTERED A3 §A3.8, docs/phase-0-prereg-amendment-3.md:689-700]

**R-5.45** The scope-bearing dimensions the record names are: `verification` (the P4 envelope verdict), `protocol_standing`, payload interpretability / Representation Information status, and custodial health as separately obtainable current information. An artifact may honestly be `verification = VALID_STRICT` and `protocol_standing = ABSENT`. [REGISTERED A3 §A3.7.1/§A3.8, docs/phase-0-prereg-amendment-3.md:541-549, :700-702]

**R-5.46** Standing reports at least `ESTABLISHED`, `ABSENT`, or `UNVERIFIABLE`, with evidence and reasons, alongside the unchanged P4 envelope verdict. Standing is an orthogonal assessment dimension, not a fifth P4 state; it is reported, never waived, and no verifier policy rewrites the reported value. [REGISTERED A3 §A3.7.1, docs/phase-0-prereg-amendment-3.md:541-546] [RULED A3 §A3.7.1, docs/phase-0-prereg-amendment-3.md:550-557] [MODELLED `event StandingReport(bitstring, bitstring, pkey, bitstring, bitstring).`, whose comment reads "verdict, reason, key, tuple, derived identity", formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:175-176]

**R-5.47** No unqualified aggregate checkmark is part of the conforming result. The system may not collapse envelope verification, protocol standing, payload interpretability, or custodial health into one judgment. [REGISTERED A3 §A3.8, docs/phase-0-prereg-amendment-3.md:677-684, :703-704]

**R-5.48** Every Tessera-controlled or conforming third-party surface that renders a result also renders its scope and the material independent dimensions. A surface showing a checkmark without those boundaries fails conformance. Tessera does not claim an adversarial relay cannot discard the result and invent or strip presentation. [REGISTERED A3 §A3.8, docs/phase-0-prereg-amendment-3.md:706-710] The mechanical CI check that makes this testable is a candidate. [DOCKET 11 — candidate, docs/band-1-docket.md:78-82]

**R-5.49** A party needing portable attribution, evaluation-time evidence, or tamper-evident transport may separately attest the complete base result as a distinct typed wrapper. Its bounded claim is that an identified evaluator assessed an identified bundle under an identified environment and obtained the enclosed result. It neither changes that result nor elevates envelope validity into payload truth; signer authority, key lifecycle and report policy belong to that separate attestation profile and are not smuggled into the base verifier contract. [REGISTERED A3 §A3.8, docs/phase-0-prereg-amendment-3.md:712-720]

**R-5.50** Reason-carrying output is a conformance requirement, not a rendering nicety. Two outcomes that agree on the verdict but differ in what was not established must not collapse into one output. [RULED (author) 2026-08-12, formal/spike/first-link/DECISION.md:748-768]

#### Per-layer result shape

| Field | Content | Waivable? | Source |
|---|---|---|---|
| `verification` | one of the four P4 verdicts, for this layer alone | the waiver set is a policy input to it; the verdict itself is never rewritten | A3 §A3.8, a3:690-698 |
| `protocol_standing` | `ESTABLISHED` / `ABSENT` / `UNVERIFIABLE`, with evidence and reasons — the one vocabulary; the S-series' standing / no standing are its aliases under R-3.60a's mapping [RULED — §12 C-10, A7 §A7.7] | No. Reported, never waived | A3 §A3.7.1, a3:541-557 |
| scope | machine-readable, for every claim | No | A3 §A3.8, a3:690-698 |
| evaluated inputs | identities of the input receipt, bundle members, and evidence actually evaluated | No | A3 §A3.8, a3:690-698 |
| governing context | specification, policy, trust configuration, declared evaluation context | No | A3 §A3.8, a3:690-698 |
| reasons and observations | material reasons, observations, unavailable evidence, and recorded waivers, including for each waived check both the authorizing policy and the observation (R-5.39) | No | A3 §A3.8, a3:690-698; A5 §A5.3, a5:134-154 |
| payload Representation Information status | on request only; absence never affects the P4 verdict | n/a | A3 §A3.4/§A3.8, a3:357-364, :690-698 |
| aggregate checkmark | must not exist | n/a | A3 §A3.8, a3:703-704 |

#### Reason codes the record names

| Reason code | Emitted by | Meaning | Source |
|---|---|---|---|
| `TERMINAL_DISPOSITION_SHOWN` | standing (S1) | lineage present; this artifact is the shipped anchor | first-link/DECISION.md:790-806 |
| `SUPERSEDED` | standing (S2) | lineage present; this artifact was superseded | first-link/DECISION.md:790-806 |
| `NO_TERMINAL_DISPOSITION_EVIDENCE` | standing (S3) | lineage absent; artifact presented alone | first-link/DECISION.md:790-806 |
| `ISSUANCE_REFUSED` | standing (S4) | lineage present; terminal disposition is `REFUSED` | first-link/DECISION.md:818-832 |
| `STANDING_EVIDENCE_MALFORMED` | standing | internally inconsistent standing evidence; yields `UNVERIFIABLE`, never `ESTABLISHED` | RULED SC-3, first-link/DECISION.md:834-843 |
| `STANDING_EVIDENCE_TEMPORAL_MISMATCH` | standing | the TLR's anchor fails the A2.1 predicate against its declared terminal-disposition time | RULED SC-3, first-link/DECISION.md:844-847 |
| `STANDING_EVIDENCE_MISMATCH` | standing | derived identity not found in the presented lineage | probe-observed, not registered: [MODELLED standing probe, formal/spike/standing-probe/DECISION.md:116-129] [OPEN — §11 O-75] |
| `STANDING_EVIDENCE_SIGNATURE_INVALID` | standing | a TLR under any key other than the entitled key | probe-observed, not registered: [MODELLED standing probe, formal/spike/standing-probe/DECISION.md:116-129] [OPEN — §11 O-75] |
| `KEY_FINGERPRINT_MISMATCH` | envelope | presented key does not match the fingerprint the manifest names | standing-probe/AMENDMENTS-2026-08-31.md:210-219 |
| (unnamed) unknown binding-form identifier | binding forms | identifier unknown to this verifier → `UNVERIFIABLE` | first-link/DECISION.md:393-405 |
| (unnamed) known-but-unsupported binding form | binding forms | must not share a reason code with the preceding row | first-link/DECISION.md:393-397 |

**R-5.51** S2, S3 and S4 MUST return pairwise distinct reason codes; a mechanism that collapses any pair is vacuous, and a broken companion collapsing any pair must fail the discrimination check. [RULED first-link/DECISION.md:806-810, :818-832] [MODELLED `ReasonCollapsed` judge over `PATH_S2`/`PATH_S3`/`PATH_S4`, formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:392-396] The modelled judge is evidence about the model's constants and nothing else; the implementation-level check is an H1a/P8 vector obligation.

**R-5.52** The standing report has one output vocabulary — `ESTABLISHED` / `ABSENT` / `UNVERIFIABLE`, each with a reason code — onto which the S-series' standing / no standing map as aliases; the mapping is R-3.60a's table. The two probe-observed codes remain unregistered. [RULED (author) 2026-09-14; instrument A7 §A7.7, PROPOSED] [RULED — §12 C-10, A7 §A7.7] [OPEN — §11 O-75]

### 5.4 What the verifier leaves to the adjudicator

**R-5.53** Tessera attests the identity of the framed bytes presented at an issuance event, computational identity under the declared construction and assumptions, and nothing more. Outside the attestation: meaning, truth, intended use, future interpretation, and the metaphysical identity of the payload's referent. [REGISTERED A3 §A3.1, docs/phase-0-prereg-amendment-3.md:61-66]

**R-5.54** Tessera does not decide whether the adjudicator should trust the attestation and must not try to. The adjudicator is the relying party who decides trust using the verdict and anything else available, including any third-party log. [RULED A4 §A4.6, docs/phase-0-prereg-amendment-4.md:156-182]

**R-5.55** `VALID_STRICT` attests envelope soundness, never payload truth. No API or UI may relay envelope validity as content validity. [REGISTERED A3 §A3.8, docs/phase-0-prereg-amendment-3.md:677-684]

**R-5.56** Standing is orthogonal: relying-party policy decides whether `verification` and `protocol_standing` together meet its own requirements; Tessera does not collapse them into one checkmark. A relying party may accept `ABSENT` or `UNVERIFIABLE` standing, but that acceptance is the policy's own recorded decision outside the verdict. [REGISTERED A3 §A3.7.1, docs/phase-0-prereg-amendment-3.md:546-549] [RULED A3 §A3.7.1, docs/phase-0-prereg-amendment-3.md:550-557]

**R-5.57** Whether a replay is appropriate is caller policy: re-presenting a genuinely issued package preserves identity and P1 permits it; the context that supplies transaction identity, nonce, audience or purpose is not Tessera's to invent. [REGISTERED A3 §A3.1, docs/phase-0-prereg-amendment-3.md:68-74]

**R-5.58** Misissuance (an authorized or compromised issuer path signing content it should not) is out of scope for the cryptographic construction and is met by operational controls. The model documents the boundary; it does not pretend to cover it. [REGISTERED prereg §3.1, docs/phase-0-prereg.md:388-404; A1 §A1.3, docs/phase-0-prereg-amendment-1.md:347-355]

**R-5.59** Equivocation by the entitled key is not detected by the standing mechanism: two contradictory terminal lineage records under one key each report `ESTABLISHED` when presented alone. [MODELLED standing-probe gate G4, formal/spike/standing-probe/DECISION.md:78-82] [MODELLED S-STANDING, formal/suite/s-standing/RESULTS.md:540-556]

#### The boundary, stated

| Tessera establishes | Tessera does not establish | Source |
|---|---|---|
| "this valid package reconstructs the same framed bytes recorded at issuance" | "the payload is true; the issuer understood it; …" | A3 §A3.1.4, a3:89-96, quoting the 2026-07-28 ruling doc verbatim |
| the identity of the framed bytes presented at an issuance event, under the declared construction and assumptions | meaning, truth, intended use, future interpretation, the metaphysical identity of the payload's referent | A3 §A3.1, a3:61-66 |
| that the bytes existed not after `anchor_time` | any lower bound: old bytes can be stamped today, and a forger with compromised keys can sign new bytes today | A1 §A1.6, a1:477-491 |
| that at least one uncompromised channel published this exact authority tuple (strict, two channels) | that any particular presented evidence artifact is individually provenance-guaranteed; the *statement* is, not the artifacts | first-link/DECISION.md:778-788 |
| unconditionally, that this evidence supports exactly one authority tuple | provenance, without an honesty assumption | first-link/DECISION.md:770-788 |
| that a named custodian made the recorded tending assessment | that a judgment-based `NO_ACTION_REQUIRED` conclusion is true | A3 §A3.5, a3:403-405 |
| whether the presented artifact carries terminal-disposition evidence | that no second, contradictory terminal lineage record exists; the anchor bounds *when* standing evidence could have been fabricated, not *whether* | standing-probe/AMENDMENTS-2026-08-31.md:48-54 |
| that a possessed bundle can be verified without Tessera | continued availability of a copy, which requires retention and custody immediately, not merely past the first algorithm death | A3 §A3.4, a3:261-272 |

**R-5.60** The relying-party story is the human-facing statement of these boundaries; the structured fields are their machine-facing twins. It is a required Band 0 exit artifact. [REGISTERED A3 §A3.1.4/§A3.8, docs/phase-0-prereg-amendment-3.md:89-96, :736-737]

**R-5.61** The log-versus-verdict boundary; that any service-side enumeration API may feed a log and never a verdict, a log being a correlated subject and not a verifier input; is stated as a clerk's reading, not registered text. [PROPOSED formal/COVERAGE-MAP.md row 14] [OPEN — §11 O-72]

**R-5.62** No verifier policy, and no downstream marketplace rule, may order competing receipts by declared time. [REGISTERED A2 §A2.4, docs/phase-0-prereg-amendment-2.md:327-333] The bearer of that rule is Tessera's own surfaces, policies and claims (R-1.10a): Tessera never presents `declared_issue_time` as evidence of priority and makes no priority claim; adjudicators reason for themselves; and it is not a service-refusal requirement. [RULED — §12 C-06, A7 §A7.4]

### 5.5 Coverage

Columns: what models the registered check today; what nothing models; what the coverage map records as an open cell.

| Registered verifier check | Modelled in | Not modelled anywhere | Open coverage cell |
|---|---|---|---|
| P1 integrity, operative form | S-P1 (five models, run) | none | COVERAGE-MAP row 1 records "no model on either assigned leg"; superseded by amendment note 3 but the row text stands [SETTLED — §12 S-09] |
| P2 set completeness and membership | S-P2 (eight models + Q6/Q6-C) | signature-set operations at the byte level (A1.3 item 2): reorder has no query; the set is positional; bounds beyond n = 2, uniqueness, empty set, malformed members | Recorded waiver of a signature subset: "Nothing in S-P2 models a waiver"; the recorded half is an open cell |
| P2 common attested content (§A5.4) | S-P2 Q6 / Q6-C | encoding and ordering of the equal fields | Reading (a) vs (b) fork [OPEN — §11 O-05] |
| P3 key binding, in-bytes | S-P3 (eight models) | the P3 [assumption] half: verification profile, library and version, accepted encodings, public-key validation, low-order points, cofactor variant | `discharged` blocked on the [assumption] half |
| P3 fields carried but unexercised | none | S-P3 F7 names five: issuer identity, algorithm identifier, object type, canonicalization version, and the domain tag — each can be unbound or removed without changing either result | Assigned onward by F7: object type → P7; canonicalization version and algorithm profile → P8/H1a; algorithm identifier → A3 §A3.6.1; identity → F8 |
| P4 verdict partition and waiver lattice | `formal/tla/P4_VerifierStates.tla`, 11 invariants, `_Broken` fail-open companion, `_Sanity` witnesses | the waiver *record* (a set, not a record); hostile policy input; everything below the verdict | Recording of the waived set and authorizing policy is an H1a artifact |
| P4 unknown-algorithm transition | none | the entire A3 §A3.6.2 item 3 obligation with its fail-open companion | PROPERTIES row `A3.6.2`, status `open`, artifact "—" [OPEN — §11 O-71] |
| P5 temporal window and P6 revocation | `P5P6_TemporalRevocation.tla` with four companions | k, depth, blocks, heights, reorgs, canonical-chain selection (bridge's); header availability and authentication | Parameters unratified; no reorg re-verification |
| P5/P5c correspondence | `P5cP5P6_Bridge.tla` (`PinAgreement`, `ShippedDesignatedAgree`, `HonestShipAccepted`, `LateBurialRejected`) | the `UNVERIFIABLE` arm (headers unavailable); the retry loop and reorgs | Conformance-vector case "headers unavailable → `UNVERIFIABLE`" open |
| P7 type soundness and scope | S-P7 (twelve models + Q7/Q7-C) | anything at depth > 2; opacity of any concrete embedding; distinguishability of the three unexercised object types plus `OT_TLR`/`OT_REFUSAL` in bytes | **Package completeness / self-containment**: the inner manifest, evidence and possession proof are presenter-supplied and no query asks that they travel in the bundle; COVERAGE-MAP row 8 amendment note 1 |
| P7 cross-kind confusion | none | manifest, possession proof and authority evidence have no object-type field; a confusion companion is green by constructor, not by tag | Routed to P8 golden vectors |
| P8 framing and canonicalization | none | injectivity proof; four-field frame layout; the whole rejection list; golden vectors; byte-encoding attacks in every symbolic family ("a coverage failure, not an unreachable attack") | COVERAGE-MAP row 9: no proof, no vectors. Nothing in any checked cell is stronger than the P8 residual it cites |
| P9 statelessness | none (probe only, non-discharging) | a model of P9; the probe's green is not evidence and no tracker row cites it | Discharge is [inspection + vector]; the two-machine vector with an expected-verdict oracle is owed |
| P10 manifest authority | first-link Q1/Q3; S-P3 Q1 strict; possession half S-P3 ledger 2 | no model on the tracker's originally assigned leg | "Never all" is n = 2 finite enumeration, does not generalize |
| P10 binding-form required set | none | the required-set ruling is not modelled by any suite verifier: no family carries a required-set-of-forms input | [OPEN — §11 O-73] |
| A2 §A2.4 receipt-to-anchor binding (V33a) | none | the proof's commitment to the presented framed bytes, and the identity of its authenticated block with the block used for the depth and timestamp comparisons; the TLA+ modules abstract proof and signature validity (`P5P6_TemporalRevocation.tla:52-56`) | No model and no vector; recorded here with COVERAGE-MAP row 12's "no tracker row" |
| A2 §A2.4 anchor identity | bridge `ShippedDesignatedAgree`; P5P6 `AbandonedArtifactRejected` (chain-late subclass only) | "a discarded attempt confers nothing" has no named invariant; declared-time non-ordering has no tool leg by declaration | COVERAGE-MAP row 12: no tracker row |
| SC-3 internal-consistency rule (malformed standing evidence) | S-STANDING emits `STANDING_EVIDENCE_MALFORMED` on two branches only (ss_q1d:312, :317) | the rule's other shapes: `TERM_REFUSED` against a lineage entry reading `DISP_SHIPPED`, and an entry reading `DISP_SHIPPED` under a terminal designating another identity — `StandingDecide` inspects `d` on neither (ss_q1d:296-317) | "Anything about malformed standing evidence beyond emitting the code" is assigned to the vector track, formal/suite/s-standing/RESULTS.md:547-549; the H1a vector is in §10.2 [REGISTERED SC-3, formal/spike/first-link/DECISION.md:834-843] |
| A3 §A3.7.1 standing | S-STANDING (seven models + SS.Q6/Q6-C) | equivocation (two contradictory TLRs each valid); anything temporal; which identity a wrapped bundle's standing binds to; that S2/S3/S4 are distinct in the implementation; lineages other than two attempts | PROPERTIES row `SC`, `open`; panel criterion 4 condition 2 not claimed satisfied; Band 0 exit gated on it |
| A3 §A3.7.2 refusal record | none | the extended atomic-entry invariant (record + commitment + delivery `PENDING` + publication `PENDING`) and its two companions | PROPERTIES row `A3.7.2`, status `open`, artifact "—" [OPEN — §11 O-71] |
| `AcceptS` ↔ P4 join | none | reachability of `AcceptS` is unqueried in S-STANDING and "not shown reachable in the `.out`, so the proviso is assumed met by P4, not shown" | Cross-formalism; never marked symbolically discharged |
| Verifier / adjudicator boundary | none | no registered claim text says it in these words; no tool leg | COVERAGE-MAP row 14, PROPOSED |
| Algorithm identifier selection | none | no leg checks selection-by-identifier; `alg` is compared between fields, never used to select | COVERAGE-MAP row 15: no tracker row |

**Ruling note on the key-binding row (2026-09-14).** S-P1's authorship claim and S-P3's key binding
compose as **complementary** claims, not as a producer-consumer pair: S-P1's ledger entry 1 stands as
written (complementary, not consumed, no cross-model entry claimed), and S-P3's ledger entry 1 is
read as naming S-P1 a *related* family, not a consumer. The rule: a cross-model ledger entry exists
only where severing the producer would falsify the consumer's query. Each consumer makes its own
dependency analysis; S-P2 and S-P7 determine their own position against S-P3's entry when their
entries are entered (`formal/BAND0-EXIT.md` E5a), and the capstone discharge matrix (§10.1 E5)
carries no cross-model key-binding row between S-P3 and S-P1. Recorded in `formal/COVERAGE-MAP.md`
by an appended note. [RULED (author) 2026-09-14; instrument A7 §A7.10, PROPOSED; §12 C-11]

---

## 6. Standing assessment

### 6.1 The invariant

**R-6.1** The registered standing invariant, in full: "Cryptographic validity alone confers no protocol standing. Any artifact claiming standing must present verifiable standing evidence binding its issuance identity, attempt lineage, and terminal disposition. Missing standing evidence leaves the artifact evidentially admissible but without protocol standing." [REGISTERED A3 §A3.7.1, docs/phase-0-prereg-amendment-3.md:530-535]

**R-6.2** Standing is "an **orthogonal assessment dimension**, not a fifth P4 state. The base result reports at least `ESTABLISHED`, `ABSENT`, or `UNVERIFIABLE`, with evidence and reasons, alongside the unchanged P4 envelope verdict." [REGISTERED A3 §A3.7.1, docs/phase-0-prereg-amendment-3.md:541-546]

**R-6.3** Verdict and standing are reported separately and never collapsed: "an artifact may honestly be `verification = VALID_STRICT` and `protocol_standing = ABSENT`. Relying-party policy decides whether those facts meet its own requirements; Tessera does not collapse them into one checkmark." The field names `verification` and `protocol_standing` appear verbatim in the registered text. [REGISTERED A3 §A3.7.1, docs/phase-0-prereg-amendment-3.md:545-548]

**R-6.4** Standing "is not a member of the A1.2.1 waiver lattice: it is reported, never waived. No verifier policy, strict or degraded, rewrites the reported standing value." A relying party may accept `ABSENT` or `UNVERIFIABLE` standing, but that acceptance "is the policy's own recorded decision outside the verdict." [REGISTERED A3 §A3.7.1, marker `[PANEL-DRIVEN CLARIFICATION — 2026-08-08, from the Kimi cold read]` — not an author decision, docs/phase-0-prereg-amendment-3.md:550-557]

**R-6.5** Protocol standing is one of the base assessment's required fields, carried alongside the P4 envelope-verification result and a machine-readable scope for every claim; "No unqualified aggregate checkmark is part of the conforming result." [REGISTERED A3 §A3.8, docs/phase-0-prereg-amendment-3.md:690-698; :703-704]

**R-6.5a** The base assessment carrying the standing field "is an unsigned, reproducible computation. It reports what the verifier can establish at evaluation time and leaves the relying party to decide whether those facts meet its requirements." [RULED (author) 2026-08-08, docs/phase-0-prereg-amendment-3.md:686-689; :722-736]

**R-6.5b** No surface may collapse "envelope verification, protocol standing, payload interpretability, or custodial health into one judgment." A surface showing a checkmark without those boundaries "fails conformance." [REGISTERED A3 §A3.8, docs/phase-0-prereg-amendment-3.md:677-684; :706-710]

**R-6.6** The mechanism discharging the invariant "must be testable on an abandoned artifact presented alone, not only when competing artifacts happen to meet." Comparative visibility is insufficient, because "a presenter of the abandoned artifact could omit a later lineage record." [REGISTERED A3 §A3.7.1, docs/phase-0-prereg-amendment-3.md:524-530; :536-540]

**R-6.7** Standing and A2.4 coexist without amendment: for an abandoned artifact presented alone, terminal-disposition evidence is absent and the artifact has no protocol standing. "An abandoned artifact is not certified by the attestation service. Nothing prevents a client from accepting it on its own judgment, but Tessera must not claim an affirmative standing signal it did not issue." A2.4 confines protocol standing and does not render such artifacts inadmissible as evidence. [RULED (author) 2026-08-12, formal/spike/first-link/DECISION.md:700-733; REGISTERED A2 §A2.4, docs/phase-0-prereg-amendment-2.md:307-316]

### 6.2 The selected construction: the terminal lineage record (TLR)

**R-6.8** The terminal lineage record is the selected standing-evidence mechanism. [RULED (ADOPTED author) 2026-08-31, entered 2026-09-04, author commit `fbf6387`, formal/spike/standing-probe/DECISION.md:3-13; :378-398] [SETTLED — §12 S-13]

**R-6.9** The probe's TLR "is signed by the entitled key and binds derived identity, lineage, and terminal disposition; a TLR under any other key returns `STANDING_EVIDENCE_SIGNATURE_INVALID`." The source states its own boundary: "the probe is a stub fixture; this is design evidence, not conformance." [PROPOSED (probe scoring draft, gate G0; DECISION.md:28 retains "Status: PROPOSED — scoring draft, nothing decided."), formal/spike/standing-probe/DECISION.md:61-67]

**R-6.10** The TLR is handle-bound, not ordinal-bound. Registered polarity: "handle-bound TLR rejects both transplants (`ABSENT`/`STANDING_EVIDENCE_MISMATCH`, `SUPERSEDED`); the ordinal-bound broken variant accepts both (`ESTABLISHED`)." [PROPOSED (probe scoring draft, gate G1, evidential; DECISION.md:28), formal/spike/standing-probe/DECISION.md:68-71]

**R-6.11** The standing report is offline: "Zero inputs beyond the bundle and the trust configuration; the verifier's reads are enumerated." [PROPOSED (probe scoring draft, gate G2; DECISION.md:28), formal/spike/standing-probe/DECISION.md:72-74]

**R-6.12** The TLR travels in the bundle. Custody of the TLR is "carried, not maintained; the service's duty is punctual, not custodial; costs fall on the service's beneficiaries." The bundle's custodian is the relying party, "whose custody is correlated with its own interest," so the construction creates no new custody subject. [RULED (ADOPTED author) at adoption; the wording at :386-390 is the collaborator's record of the author's in-session resolution, his own quoted words there being "Item 5 adopted.", formal/spike/standing-probe/DECISION.md:130-140; :386-390]

**R-6.13 (SC-2)** One signing act at terminal disposition produces the disposition fact, "(attempt identity, terminal disposition)", and both disposition-bearing records are projections of that one signed fact: the TLR adds the attempt lineage; the portable refusal record (§A3.7.2) adds the disclosable reasons and the public commitment value. "Whether the projections are one object or two remains unpreferred." [RULED (ADOPTED author) 2026-08-31 / text 2026-09-04, formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:96-116; DECISION.md:327-338]

**R-6.14 (SC-1)** "The TLR is anchored: at terminal disposition the issuer submits the TLR's digest to the anchoring channel, and the resulting anchor proof travels in the bundle beside the TLR." The verifier "additionally evaluates the registered A2.1 predicate against the TLR's anchor, with the TLR's declared terminal-disposition time in the place of the declared issue time: `confirmed_at := timestamp(block at height h + k − 1)`, `confirmed_at ≤ declared_terminal_time + δ`, together with the A2.2 anchor-time lower-bound conjunct under ε, under the issuance policy's tolerances (verifier-owns-tolerances applies as in A2.1)." It is "not a new window: it is the same three-conjunct temporal test the attestation's own anchor passes, applied to a second anchored object." [RULED (ADOPTED author) 2026-09-04, formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:22-47]

**R-6.15 (SC-1 boundary)** "the anchor bounds **when** standing evidence could have been fabricated — to the [−ε, +δ] window about the declared terminal disposition, per A2.1/A2.2 — and does not narrow **whether** a second, contradictory TLR exists within that window." A holder of the entitled key after that window, including after the service's death, "can no longer mint standing evidence that verifies." [RULED (ADOPTED author) 2026-09-04, formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:48-54]

**R-6.16 (SC-1 cost i)** A second anchoring event per issuance occurs at terminal disposition, after the shipped attempt's anchor confirms. "anchor-channel unavailability at that moment is an issuance failure mode of A2.3's class and must be treated by the refusal machinery, not absorbed silently". [RULED (ADOPTED author) 2026-09-04, formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:56-64]

**R-6.16a (SC-1 costs ii-iv)** Where a bundle ships before confirmation it carries a pending anchor proof and "**the holder bears the upgrade duty**"; "**δ is bounded below by anchor-confirmation latency**"; and "**Complete standing evidence is late by construction**", by two anchor-confirmation latencies in sequence plus the lifecycle wait S on the refusal path. [RULED (ADOPTED author) 2026-09-04, formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:64-81]

**R-6.17** Bare "within δ" is forbidden in registered text: SC-1 and the SC-3 temporal outcome cite the A2.1 predicate explicitly, because the bare phrase "would have let a conformant verifier pick a symmetric window or the block-h timestamp." [RULED (author) 2026-09-04, formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:223-241]

**R-6.18 (SC-3, mandatory red outcomes)** Two defined outcomes are added "in the first-link verifier-boundary spirit (no inference, fallback, or normalization)":

| Reason code | Trigger | Verdict |
|---|---|---|
| `STANDING_EVIDENCE_MALFORMED` | "internally inconsistent standing evidence (e.g., a terminal disposition contradicting the lineage's own entry for that attempt, probe finding F1)" | `UNVERIFIABLE`; "it never yields `ESTABLISHED`" |
| `STANDING_EVIDENCE_TEMPORAL_MISMATCH` | "the TLR's anchor failing the A2.1 predicate against its declared terminal-disposition time (Amendment 1)" | `UNVERIFIABLE` |

"The S-series test vectors MUST include the F1 shape, and a broken companion that accepts it MUST fail." [RULED (ADOPTED author) 2026-09-04, formal/spike/first-link/DECISION.md:834-847 = formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:146-155]

**R-6.19 (§A5.6 tuple pin)** "the standing path checks that the presented authority tuple equals the tuple embedded in the core it derives the artifact identity from — `ENUMERATION.md` note 4 item 2's principle (the standing path relies on nothing the envelope path established), applied to the tuple as it is already applied to the key; an alias companion must go red." [RULED (ADOPTED author) A5 §A5.6, docs/phase-0-prereg-amendment-5.md:202-219]

**R-6.20 (D1 slot location)** The forward-link / predeclared successor slot will be registered; **Location RULED (author, 2026-09-04):** "inside the canonical payload under P3's obligations, per the A3 §1 precedent, leaving P8's four-field frame unchanged" (band-1 docket); the same ruling reads, in `DECISION.md`, "the slot rides inside the canonical payload under P3's obligations, the location A3 §1 pinned for the algorithm identifier, leaving P8's four-field frame unchanged" (author annotation: "concur with proposal to adopt (a)"). The slot as a P8 frame field was not adopted. Registration completes before format freeze; P8's golden vectors gain a slot-bearing vector at registration. It is "Not gated on, and does not gate, the S-STANDING model." Relation: "the terminal lineage record chains attempts within one issuance, backward; the slot chains issuances across the service's life, forward." [RULED (author) 2026-09-04, formal/spike/standing-probe/DECISION.md:368-377; formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:182-206; docs/band-1-docket.md:355-383]

**R-6.21** The forward identifier "has to be inside the signed package — otherwise, it isn't tied to the attestation": an independent identifier, not a back-hash, carried inside the signed bytes at the payload location ruled in R-6.20. [RULED (author) 2026-09-04, docs/band-1-docket.md:378-385]

**R-6.22** As adopted with the selection, the log-and-receipt enrichment "remains separately registrable per issuance class and never load-bearing" (sub-ruling 5). The fuller phrasing the draft record carries — the enrichment "remains available as a separately registered, never-load-bearing option per issuance class" — and the composition "issue the TLR always, in-bundle, load-bearing; log it and carry the receipt as **optional enrichment** where an issuance class wants equivocation visibility — receipts never load-bearing" are the scorer's, one headed "**RECOMMENDED (not adopted, and carrying the scorer's non-blindness)**" and the other "an input to the rule-3 fork, not a selection". [RULED (ADOPTED author) sub-ruling 5, formal/spike/standing-probe/DECISION.md:378-384; scorer wording PROPOSED, :185-195, :313-321]

**R-6.22a (alternatives named rejected at selection)** The transparency witness survived the gates but was not selected: it is "one new custody subject, uncorrelated", the log "must survive for the enrichment to mean anything at year 80", retention has no assigned owner, and it adds "an **issuance-time availability dependency**: no bundle ships while the log is down". The capability construction "Fails **G0** (the attempt lineage is unbound, by design) and **G3** (S2 and S3 are both 'no token present')". [PROPOSED (probe scoring draft; DECISION.md:28) — candidate not selected, formal/spike/standing-probe/DECISION.md:144-183, :197-204]

**R-6.22b** Two further outcomes for the optional witness enrichment ("inclusion proof invalid; log key unknown to the trust configuration (`UNVERIFIABLE`, its own reason)") are criteria-level and unadopted; they govern only the enrichment, which was not selected. [PROPOSED (unadopted), formal/spike/standing-probe/DECISION.md:166-168]

### 6.3 The standing decision procedure, as modelled

The procedure as S-STANDING models it runs as a process parallel to the envelope path on the same bundle input. The steps in R-6.24 are the model's; where the registered contract is wider, the difference is stated below rather than folded into the table.

**R-6.23 (inputs)** The standing path consumes the bundle tuple `(t, ev, kX, core, fb, se)`: evidenced authority tuple, authority evidence, presented key, attempt core, framed bytes, standing evidence. "The standing path evaluates the evidenced tuple and the entitled key ITSELF (ENUMERATION note 4 item 2); it inherits nothing from the envelope path." [MODELLED S-STANDING, formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:318-324]

**R-6.24 (steps, in order)**

| # | Step | Model term | Failure outcome |
|---|---|---|---|
| 1 | Authority evidence binds this exact tuple | `let (=STMT_DIGEST, =h(t)) = checksign(ev, pkS)` | path does not proceed |
| 2 | Tuple destructuring | `let authTuple(id, kfpr, ss, alg, ver) = t` | path does not proceed |
| 3 | Derive the attempt identity | `let aid = h(core)`; "identity is DERIVED by the verifier from the core it holds, never read" | n/a |
| 4 | No standing evidence | `if se = noTLR` | `ABSENT` / `NO_TERMINAL_DISPOSITION_EVIDENCE` (S3) |
| 5 | Entitled key, inside the standing path | `if fp(kT) = kfpr` | `UNVERIFIABLE` / `STANDING_EVIDENCE_SIGNATURE_INVALID` |
| 6 | TLR key equals presented key | `if kT = kX` | none modelled [OPEN — §11 O-74] |
| 7 | TLR signature under the entitled key, library tag `TLR` | `let (=TLR, (lin, terminal, declT)) = checksign(tlrSig, kT)` | `UNVERIFIABLE` / `STANDING_EVIDENCE_SIGNATURE_INVALID` |
| 8 | Anchor proof is over the TLR presented | `let anchorProof(=h(tlrSig)) = ap` | `UNVERIFIABLE` / `STANDING_EVIDENCE_TEMPORAL_MISMATCH` |
| 9 | §A5.6 tuple pin | `let attemptCore(=t, ppfS, sgS, declS) = core` | no else branch |
| 10 | Lineage lookup | `let d = lookup2(aid, lin)` | `ABSENT` / `STANDING_EVIDENCE_MISMATCH` |
| 11 | Terminal disposition | `StandingDecide`: `TERM_REFUSED` → S4; `TERM_SHIPPED(shippedId)`, `shippedId = aid`? | S4 `ABSENT`/`ISSUANCE_REFUSED`; S2 `ABSENT`/`SUPERSEDED`; non-`TERM_*` → `UNVERIFIABLE`/`STANDING_EVIDENCE_MALFORMED` |
| 12 | Per-entry disposition | `if d = DISP_SHIPPED` | `ESTABLISHED`/`TERMINAL_DISPOSITION_SHOWN` (S1), else `UNVERIFIABLE`/`STANDING_EVIDENCE_MALFORMED` |

Between steps 4 and 5 the model destructures `let withTLR(kT, tlrSig, ap) = se`, which has no else branch: standing evidence that is neither `noTLR` nor a `withTLR` term produces no report at all. [MODELLED S-STANDING, formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:288-292; :296-317; :322-363, the `withTLR` destructuring at :334]

**R-6.24a (registered SC-3 internal-consistency rule, evaluated before the model's step 11)** Internally inconsistent standing evidence — "a terminal disposition contradicting the lineage's own entry for that attempt, probe finding F1" — "yields `UNVERIFIABLE` with this reason", `STANDING_EVIDENCE_MALFORMED`, and "it never yields `ESTABLISHED`". The rule is not confined to the one branch the model checks at step 12: a signed TLR declaring `TERM_REFUSED` while its own lineage entry for the presented attempt reads `DISP_SHIPPED`, and an entry reading `DISP_SHIPPED` under a terminal designating another identity, are both internally inconsistent standing evidence and take this outcome instead of step 11's ordinary refusal or supersession outcome. [REGISTERED SC-3, formal/spike/first-link/DECISION.md:834-843; adopted text formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:146-151]

*Registered vs modelled, steps 11–12.* `StandingDecide` returns refusal without inspecting `d`, and supersession without inspecting `d`; only the terminally designated identity reaches the `d = DISP_SHIPPED` check (formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:296-317). The model is therefore narrower than R-6.24a, and both shapes named there receive ordinary S4 and S2 reports in it. This is a model-coverage fact, not a contradiction: the family's own record assigns "Anything about malformed standing evidence beyond emitting the code" to the vector track (formal/suite/s-standing/RESULTS.md, "What S-STANDING does not discharge", :547-549). The coverage cell is in §5.5; the H1a vector is in §10.2.

**R-6.25** The entitled-key check is inside the standing path by registered obligation: "a faithful implementation and the S-STANDING model MUST check the entitled-key binding **inside** the standing path, so a bundle whose envelope fails `KEY_FINGERPRINT_MISMATCH` cannot receive a standing report computed against an unentitled key." A companion establishing the link only through the envelope MUST fail. [PROPOSED — the source is headed "Carry note (drafter, not an amendment)", and `ENUMERATION.md` amendment note 4 carrying it is headed "(clerk; PROPOSED; …)"; the MUST wording is the drafter's, not the author's. formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:210-219; formal/suite/ENUMERATION.md:486, :502-509]

**R-6.26** The §A5.6 pin is placed after the `noTLR`, `withTLR`, entitled-key and TLR-signature branches and immediately before the lineage lookup, and has no else branch. The consequence recorded at registration read "no ABSENT or UNVERIFIABLE reason-code branch acquires a new precondition"; that sentence was corrected on 2026-09-12 as false, and the corrected form is: the aggregate vocabulary witnesses S1–S4 and `STANDING_EVIDENCE_MISMATCH`, quantified over free variables, "are unaffected and stay reachable", but for an alias presentation the lineage-derived reports `SUPERSEDED`, `ISSUANCE_REFUSED` and `STANDING_EVIDENCE_MISMATCH` "DO acquire the pin as a new precondition" — "A checked consequence of the registered placement, not a defect." A core that is not an `attemptCore` over `t` yields "no lineage-derived report (no mismatch, supersession or refusal report); the no-TLR report is unaffected". [MODELLED S-STANDING, formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:343-352; :77; corrections verified formal/suite/s-standing/RESULTS.md:1335-1348, :1350-1370]

**R-6.27 (frame identity is the envelope path's, not the standing path's)** "The standing path checks `attemptCore(=t, ppfS, sgS, declS) = core` and nothing about the identity named inside the *signature frame*; that identity is checked on the **envelope** path". The two paths run in parallel; this is "`ENUMERATION` note 4 item 2 working as intended … not a gap in the pin. Recorded as a boundary; no model change." [MODELLED S-STANDING (boundary, 2026-09-12 cross-family review), formal/suite/s-standing/RESULTS.md:1270-1280]

**R-6.28** The envelope path is carried in the model verbatim from S-P3 and is not queried; "A3.7.1's orthogonality is structural." [MODELLED S-STANDING, formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:365-378]

**R-6.29** The model's producer ledger entry P-2 makes the entitled-key check a checked shape: `Established(kX, t, aid)` implies `fp(kX) = kfpr(t)` for the evidenced `t`; consumer is the H1a conformance profile. [MODELLED S-STANDING, formal/suite/s-standing/RESULTS.md:454-467]

### 6.4 Outputs

**R-6.29a (producer ledger P-1, the standing relation)** An `ESTABLISHED` report against an honest entitled key `kH` for derived identity `aid` implies the issuer holding `kH` signed one TLR whose lineage contains `aid` and whose terminal designates it. Consumers: A3.8's `protocol_standing`, the relying-party story, A3.9, and S-P7's innermost-identity claim. [MODELLED S-STANDING, formal/suite/s-standing/RESULTS.md:434-453]

**R-6.29b (alias instrumentation)** The §A5.6 alias judge is "INSTRUMENTATION, not a verifier check": on an `ESTABLISHED` emission it compares the presented tuple with the tuple embedded in the core and emits `Aliased` on a difference. It emits nothing when the core is not an `attemptCore` term. [MODELLED S-STANDING (SS.Q6), formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:398-406]

**R-6.29c (wrapper transplant)** The wrapper-shaped outer artifact is built by no honest process; the adversary may build one. The literal transplant query, required reachable on the label-bound companion only, is "Evidence only against the label-bound companion and discharges nothing of the property". [MODELLED S-STANDING, formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:125-128; formal/suite/s-standing/RESULTS.md:395-431]

**R-6.30 (the S-series rows)** Registered standing test conditions, with the reason code each MUST return:

| # | Form | Presented with lineage? | Standing verdict | Required reason code |
|---|---|---|---|---|
| S1 | Lineage-present, artifact **is** the shipped anchor | yes | **standing** | `TERMINAL_DISPOSITION_SHOWN` |
| S2 | Lineage-present, artifact **superseded** by the shipped anchor | yes | **no standing** | `SUPERSEDED` |
| S3 | Lineage-absent — abandoned artifact presented **alone** | no | **no standing** | `NO_TERMINAL_DISPOSITION_EVIDENCE` |
| S4 | Lineage-present, lineage's terminal disposition is `REFUSED` | yes | **no standing** | `ISSUANCE_REFUSED` |

"(A refused-lineage attempt presented *alone* remains S3: absent evidence is absent evidence.)" [REGISTERED (exit condition 3, 2026-08-12) + dated amendment SC-3 2026-09-04, formal/spike/first-link/DECISION.md:798-801; :826-832]

**R-6.31 (discrimination)** "S2, S3, and S4 all return 'no standing' and MUST return pairwise distinct reason codes; the negative-control obligation extends to a companion collapsing any pair." "A standing mechanism that collapses them is vacuous in exactly the way the panel criterion warned about." [REGISTERED / dated amendment, formal/spike/first-link/DECISION.md:804-810; :828-832]

**R-6.32 (reason-carrying output)** "the verdict is always 'no protocol standing,' and the test MUST emit the reason." No standing for want of lineage context and no standing through supersession "must not collapse into one output"; reason-carrying output "is a conformance requirement, not a rendering nicety." [RULED (author) 2026-08-12, formal/spike/first-link/DECISION.md:748-768]

**R-6.33 (the alone case is the hard case)** "Per the DeepSeek panel criterion, **every** standing / dead-project test records whether the artifact was presented with or without lineage context; the lineage-absent case is mandatory and is the hard case." [REGISTERED (exit condition 3), formal/spike/first-link/DECISION.md:790-796]

**R-6.34 (orthogonality condition on the tests)** All conditions are evaluated "with the standing result reported *orthogonally to the P4 verdict*. S3 in particular must leave an old bundle's `VALID_STRICT` unaffected while the standing report is negative and any custodial-record check reports `UNVERIFIABLE`." Observed in the probe: "the envelope verdict was `VALID_STRICT` across all three presentations — orthogonality held." [REGISTERED (A3 §A3.9; docket 16), formal/spike/first-link/DECISION.md:812-816; formal/spike/standing-probe/DECISION.md:74-77]

**R-6.35 (one vocabulary, with the S-series mapped onto it)** The standing report's value set is A3 §A3.7.1's `ESTABLISHED` / `ABSENT` / `UNVERIFIABLE`, each with a reason code. The registered S-series table's "**standing**" / "**no standing**" are that series' names for `ESTABLISHED` / `ABSENT` and are not a third value. The mapping, copied from A7 §A7.7 with the reason codes retained and pairwise distinct as registered:

| Row | S-series verdict | Standing value | Reason code |
|-----|------------------|----------------|-------------|
| S1 | standing | `ESTABLISHED` | `TERMINAL_DISPOSITION_SHOWN` |
| S2 | no standing | `ABSENT` | `SUPERSEDED` |
| S3 | no standing | `ABSENT` | `NO_TERMINAL_DISPOSITION_EVIDENCE` |
| S4 | no standing | `ABSENT` | `ISSUANCE_REFUSED` |
| — | — | `UNVERIFIABLE` | `STANDING_EVIDENCE_MALFORMED` (SC-3, internally inconsistent evidence) |
| — | — | `UNVERIFIABLE` | `STANDING_EVIDENCE_TEMPORAL_MISMATCH` (SC-3, the TLR's anchor failing A2.1) |

The H1a standing vectors carry the mapped values. `STANDING_EVIDENCE_MISMATCH` and `STANDING_EVIDENCE_SIGNATURE_INVALID` are not registered by this ruling (R-6.36). [REGISTERED, formal/spike/first-link/DECISION.md:798-801, :838-847; docs/phase-0-prereg-amendment-3.md:541-546; formal/spike/standing-probe/DECISION.md:61-71, :138-141] [RULED (author) 2026-09-14; instrument A7 §A7.7, PROPOSED] [RULED — §12 C-10, A7 §A7.7]

**R-6.36 (two further codes, registered home unstated)** `STANDING_EVIDENCE_MISMATCH` and `STANDING_EVIDENCE_SIGNATURE_INVALID` are emitted by the modelled verifier and recorded in the probe, but no amendment or exit condition registers them the way SC-3 registers the two codes of R-6.18. [PROPOSED (probe scoring draft, probe-recorded; DECISION.md:28), formal/spike/standing-probe/DECISION.md:61-67, :68-71, :119; MODELLED S-STANDING, formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:144-155] [OPEN — §11 O-75]

**R-6.36a (what the discrimination requirement is for)** The registered concern is testability, not entitlement: the alone case does not demand an affirmative standing signal; "a standing test whose answer is unconditionally 'no' regardless of input is not a test", and vacuity is the failure mode being checked. [DECIDED (first-link DECISION.md, entered by the author 2026-08-13 at `459aff0`), formal/spike/first-link/DECISION.md:735-746]

**R-6.36b (collapsing companion)** Both obligations stand together: build the reason-code collapsing companion and keep the S-series vector obligation. In the model, the discrimination judge fires `ReasonCollapsed` when two distinct branch labels emit the same reason code. [PROPOSED (clerk disposition B9; no author ruling on this item is recorded) ROUTED 2026-09-06, formal/suite/ROUTED-2026-09-06.md:158-161; MODELLED S-STANDING, formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:156-159, :392-396]

**R-6.37** The model's report event is the family's output surface: `StandingReport(verdict, reason, key, tuple, derived identity)`, with five vocabulary-liveness witnesses queried for reachability (S1, S2, S3, S4, `STANDING_EVIDENCE_MISMATCH`). Reachability of a code in the model is "evidence about the model's constants … and about nothing else"; the implementation-level discrimination check is an H1a/P8 S-series vector obligation. [MODELLED S-STANDING, formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:175-176, :208-218, :392-396; quoted sentence formal/suite/s-standing/RESULTS.md:274-280]

### 6.5 Boundaries

**R-6.38 (equivocation by the entitled key)** The TLR does not detect equivocation: "two TLRs from the entitled key, each bundle alone reports `ESTABLISHED`, no detection." Equivocation by the entitled key remains the A2 residue, governed by the G4 boundary statement; closure is not claimed. [PROPOSED (probe scoring draft, gate G4 content half; DECISION.md:28), formal/spike/standing-probe/DECISION.md:78-82; :108-115]

**R-6.39** Except for the F1 malformed case cured by SC-3, "Absent, mis-signed, mismatched, refused: each yields `ABSENT`/`UNVERIFIABLE` with its reason; no path yields a false `ESTABLISHED`". [PROPOSED (probe scoring draft, C3; DECISION.md:28), formal/spike/standing-probe/DECISION.md:138-141]

**R-6.40 (lineage arity)** The modelled lineage is exactly two entries (`lineage2`); the model does not cover "lineages other than two attempts", and n = 2 does not generalize. No registered text states the behaviour for other arities. [MODELLED S-STANDING, formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:130-136; formal/suite/s-standing/RESULTS.md:540-556] [OPEN — §11 O-76]

**R-6.41 (temporal aspects)** Nothing temporal is represented in the symbolic standing family; the anchor-proof check is carried and inert. TLR anchor temporal validity is consumed ledger entry C-2, cross-formalism, and "must never be marked discharged by anything in this directory": it is owed to the P5c/P5/P6 bridge. [MODELLED S-STANDING, formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:341-342; formal/suite/s-standing/RESULTS.md:484-536] [OPEN — §11 O-77]

**R-6.42 (two identities on one key)** §A5.6 does not decide "whether an issuer holding two identities on one key keeps one terminal lineage record or two. The check settles only that a core issued under one identity cannot gain standing when presented under the other; a single TLR under that key may still name cores from both." [RULED (ADOPTED author) A5 §A5.6 (non-decision), docs/phase-0-prereg-amendment-5.md:214-219] [OPEN — §11 O-36]

**R-6.43 (degraded mode)** In degraded mode with the sole authority channel compromised, the unrestricted standing sentence does not hold; what holds is the per-honest-key sentence and the entitled-key sentence. This is a registered cost, not a defect, and "No severing companion is owed for a cost." [MODELLED S-STANDING (ledger P-3), formal/suite/s-standing/RESULTS.md:468-482; RULED (author) A4 §A4.6 (section header reads "RULED (author)"; signing commit `5188e7a`), docs/phase-0-prereg-amendment-4.md:156-167]

**R-6.44** Which identity a wrapped bundle's standing binds to is not covered by S-STANDING and is routed to S-P7. A wrapper transplanting standing evidence from a valid inner artifact onto a forged outer artifact must make the standing query go red. [MODELLED S-STANDING (not-covered), formal/suite/s-standing/RESULTS.md:540-556; REGISTERED A3 §A3.9, docs/phase-0-prereg-amendment-3.md:779-795]

---

## 7. Survivability, custody, tending, agility, renewal

### 7.1 Survivability claims and the layered bundle

**R-7.1** The claim "attestation survives Tessera's termination" is split into three registered claims with different truth conditions: (1) **portability / self-containment**, "a possessed bundle can be verified without Tessera"; (2) **availability**, "a copy remains obtainable only through retention and custody. Custody is necessary **immediately**, not merely past the first algorithm death"; (3) **long-horizon evidentiary continuity**, requiring "renewal by custodians **before** the old mechanism becomes unreliable — RFC 4998 (ERS) renewal, under an RFC 4810-style cryptographic-maintenance policy; renewal wraps, it never replaces." [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:261-278]

**R-7.2 (the survivability floor)** For every artifact class Tessera produces, survivability guarantees are limited to "creation and the protocol obligations it can observe; verifiable handoff when acknowledgment occurs; portable identity; and visible failure while an observer possessing the relevant state survives. Continued availability after handoff is conditional on custody. No construction can guarantee recovery after every holder of the complete artifact loses it." [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:280-288]

**R-7.3 (bundle additions for claim 1)** The bundle carries: an unambiguous verification-spec identifier "**and its hash bound into the signed bytes**"; "**The Tessera verification specification and its conformance vectors embedded in each individual receipt bundle as typed, content-addressed objects**" (P7's enumerated type set gains the specification member); and "**A plain-language purpose preamble** (WIPP-marker style)". An aggregate preservation package "may deduplicate those immutable objects without changing their identity or semantics." [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:290-304]

**R-7.4 (Designated Community declaration)** "A member of the Designated Community — human, machine, or collaboration — can reconstruct Tessera verification and interpret its bounded result using only the preserved receipt bundle and the exact external standards dependencies declared by that bundle, without Tessera-specific institutional knowledge." The claim is "scoped to survivability claim 1 alone; it promises nothing about availability or evidentiary continuity." For claims 2 and 3 the Designated Community is "not only the bundle's *audience* but its *custodian*"; the custodial dependency "is permanent and honest." [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:305-320]

**R-7.5** "The century horizon is aspirational, not a guarantee or membership criterion." Tessera "makes no prediction that today's bundle, standards, algorithms, or competence declaration will suffice one century hence." [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:322-326]

**R-7.6 (competence profile, the rotation baseline)** A Designated Community member can, using ordinary documented computing tools: interpret the bundle's declared public-standard dependencies; implement or execute the deterministic Tessera verification procedure; run and interpret its positive, negative and broken conformance cases; and distinguish each structured assessment dimension from payload meaning. "Every custodial challenge declares any prerequisite beyond this baseline; failure on a challenge exceeding it does not by itself establish a bundle defect." [RULED (author) 2026-08-08, docs/phase-0-prereg-amendment-3.md:328-341]

**R-7.7 (dependency closure layer 1)** Tessera owns the closure over framing, canonicalization, signatures, hashes, temporal proofs and evidence formats needed to verify its own claim. "The bundle identifies each exact external standard edition, the normative sections used, known-errata disposition, stable digest where canonical bytes exist, retrieval identifier, redistribution status, and failure consequence." [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:342-352]

**R-7.7a (layer 2, issuance-profile dependencies)** For mechanisms chosen by an issuer or deployment profile: "The profile author declares them; Tessera requires an unambiguous cryptographic binding and exposes unavailable interpretation as `UNVERIFIABLE` for the affected check." [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:353-356] [RULED — §12 C-07, A7 §A7.5]

**R-7.7b (layer 3, payload-interpretation dependencies)** Submitter-supplied schemas, vocabularies, software, ontologies, codecs or contextual material are an optional typed Representation Information companion; the receipt commits to its exact bytes, and Tessera "does not assert its correctness, sufficiency, legality, availability, or the payload meaning it proposes." "Absence or uninterpretability affects payload interpretability, never the P4 envelope verdict." [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:357-364]

**R-7.8 (embedding rule)** "Tessera-authored procedure and conformance artifacts are embedded; external standards are embedded opportunistically when lawful, otherwise precisely referenced." Continued availability and correct interpretation of referenced but unembedded standards "are exposed Designated Community assumptions. An unavailable normative dependency is a visible preservation failure." [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:350-352; :366-370]

**R-7.9 (registered demonstrations)** The dead-service test (P9: verify with Tessera unreachable) and the dead-project (clean-room) test, in which "a verifier with no project-specific context receives bundle plus broken companions only, must reconstruct the procedure and reach correct verdicts including the INVALID/UNVERIFIABLE traps." Each dead-project run records its evaluation conditions: "verifier provenance, challenge creation time, disclosure state, candidate access". [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:371-379]

**R-7.10** Candidate, not registered: a declared per-bundle byte budget for embedded specifications, above which a content-addressed reference plus published store is used. [DOCKET 9 — candidate, not registered, docs/band-1-docket.md:54-56]

**R-7.11** Candidate, not registered: the embedded verification specification executable-in-principle, as "Formal fragment or pure-function reference implementation in a frozen-semantics language, not prose+vectors alone." The docket notes this "Interacts with the §A3.4 Designated Community claim — may warrant registration rather than quiet build-phase adoption." [DOCKET 10 — candidate, not registered, docs/band-1-docket.md:57-61]

**R-7.12** Candidate, not registered: the historical trust-anchor store as a standalone object, "Versioned, decoupled from the verifier binary, exportable." As registered today the archived historical trust-anchor store ships with the verifier as trust configuration, so P9 is not violated. [DOCKET 8 — candidate, not registered, docs/band-1-docket.md:50-53; REGISTERED A1 §A1.5, docs/phase-0-prereg-amendment-1.md:459-469]

### 7.2 Custody

**R-7.13 (refusal record: what the refusal transition creates)** "`REFUSED` latches atomically when A2.3's terminal condition occurs; it is final and independent of all later reporting states. Delivery or publication failure cannot reopen issuance, consume another attempt, or erase the refusal." The same transition creates, as local durable state ("creation is neither delivery nor publication"): the complete portable refusal record (attempt identity, disposition, reasons that may be disclosed, and the evidence needed to verify it); its non-identifying public commitment value; delivery status `PENDING`; and publication status `PENDING`. [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:569-581]

**R-7.14 (custodians and handoff)** "The generating authority retains the complete record until the first of: `ACKNOWLEDGED` — a declared custodian (the submitter by default) confirms possession of a record that verifies against the commitment value; `DELIVERY_FAILED` — a non-retryable delivery failure is established; or `DELIVERY_EXPIRED` — the declared bounded retention horizon ends without acknowledgment." Failure and expiry "are visible terminal dispositions, never silent deletion". [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:583-592]

**R-7.15 (the discharge moment)** "Emission with verified handoff is the discharge moment: after acknowledgment, continued availability of the complete record is a custodial dependency under the §A3.4 survivability floor, not a dependency on the generating authority. The handoff mechanism remains open." [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:592-597] [OPEN — §11 O-18]

**R-7.16 (publication is a separate state machine)** "`PENDING`; `PUBLISHED`, only on acknowledgment from the declared external channel; `PUBLICATION_FAILED`; `PUBLICATION_EXPIRED`." Creating the commitment value is not publication, and the handoff acknowledgment does not substitute for the channel's. [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:599-605]

**R-7.17** The publication channel "must declare its survival, availability, privacy, and inclusion assumptions, **and** the independence of its failure modes from the declared refusal triggers — or the correlation." [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:605-612]

**R-7.18 (named residual)** If the authority dies after the local refusal transition but before handoff and publication, no surviving observer holds evidence of the refusal disposition. Tessera "minimizes the interval, retries while alive, refuses to report the reporting workflow as complete, and names this residual rather than disguising it as `PUBLICATION_FAILED`." Under §A3.7.1 no artifact lacking terminal-disposition evidence can claim protocol standing, so "the interval costs the auditability of the refusal, never the integrity of what can be claimed on it." [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:623-637]

**R-7.18a (observer roles for refusal reporting)** "While the authority lives, the submitter and a declared operational monitor can observe pending and failed states." After `PUBLISHED`, "the public can observe the external trace under the channel's declared assumptions." Observer roles are registered; the reporting surface is not frozen. [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:614-621] [OPEN — §11 O-18]

**R-7.18b (disclosure architecture)** "The base protocol does not require public disclosure of the complete record. A deployment profile may require it for a declared issuance class." "Tessera does not maintain a foundational auditor-membership registry: the submitter may disclose its portable record to an auditor, who verifies it against the published commitment." Service-side copies and identifying metadata follow the declared minimization and retention policy; "the amendment makes no legal-process guarantee." [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:639-648] [OPEN — §11 O-48]

**R-7.18c (the commitment value)** "The commitment construction must resist practical guessing or correlation of identifying fields under its declared threat model." "It corroborates a disclosed record and does not reconstruct a lost one; absent a separately registered transparency mechanism, it does not prove that every refusal was published." No construction is named. [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:648-653] [OPEN — §11 O-07]

**R-7.18d (who bears the obligations)** §A3.7.2 assigns A2.3's durability, retrievability and reporting obligations "to the generating authority until verified handoff, to the declared custodian after it, with the published commitment — once externally acknowledged — becoming the surviving public trace". "No A2.3 obligation weakens: refusal remains atomic, latching, and first-class." [REGISTERED A3 §A3.10, docs/phase-0-prereg-amendment-3.md:852-864]

**R-7.19 (externally referenced inputs: the open questions)** Docket 17 records that items 13 to 16 assign no "retention, replication, discovery, or retrieval-testing responsibility for bytes a verifier must fetch from outside the envelope," and that the item "must answer before any Band 1 freeze: what exactly must remain obtainable; who is expected to retain it; how a verifier discovers it; and how retrieval is tested." [DOCKET 17 — candidate, not registered, docs/band-1-docket.md:139-186] [OPEN — §11 O-42]

**R-7.19a (docket 17's provenance)** The item is "the custody half of the 2026-08-12 finding that **existence is anchorable and availability is not**". "Anchoring cannot close it; only custody can." [DOCKET 17 — candidate, not registered, docs/band-1-docket.md:194-198]

**R-7.20 (constraints docket 17 states as not free choices)** The answer "cannot be 'Tessera, in perpetuity'". "Discovery should rest on intrinsic identity (content addressing) with location as a revocable hint, since locators rot on exactly the schedule the threat model cares about. Retrieval failure yields `UNVERIFIABLE` with a reason code distinguishing *not retrieved* from other unverifiable causes, and per item 16 must not contaminate the base verdict." "*No availability promise is made or implied.*" [DOCKET 17 — candidate, not registered, docs/band-1-docket.md:163-173]

**R-7.21 (scope of docket 17 today)** With no form lifecycle or issuance-state distinction implemented, subject (b) (the versioned historical trust/registry store) "has nothing to judge" and subject (c) (retired binding forms' specifications and vectors) "is empty". "**Only subject (a) is live**", the exact referenced representation wherever item 9's size budget pushes transcribed authority content behind a content-addressed reference. The A/B fork on whether a self-contained-tier verdict judges issuance-time binding-form validity "is moot on the same grounds and revives only with item 18." [DOCKET 17 — candidate, not registered, docs/band-1-docket.md:199-208; DEFERRED docket 18]

**R-7.22 (correlated vs uncorrelated custody)** Candidate reading of DECISION-CRITERIA C2 as registered: "An anchor's evidentiary value is the number of independent surviving references it must remain consistent with, not the work to recompute it — a **correlated** custody subject the world maintains for its own reasons, as against an **uncorrelated** one (a project-specific log) that only this project's relying parties have reason to keep." It "is **not** entered into the criteria, which are frozen at `74ee46e`". [DOCKET 24(a) — candidate, not registered, docs/band-1-docket.md:326-341]

**R-7.23** Candidate: anchoring standing evidence "bounds *when* each record was made … and so defeats backdated equivocation by a post-mortem key holder. It does **not** make a contemporaneous second record *discoverable*". "The honest split: the anchor narrows *when*; only a log narrows *whether*; and the log is the uncorrelated subject of (a)." [DOCKET 24(b) — candidate, not registered, docs/band-1-docket.md:336-347]

**R-7.24 (third-party log buildability)** Candidate: a registered statement that third-party logs are an intended consumer, "so that the format freeze preserves the fields a log builder needs — issuer identity, the forward identifier, anchor evidence, and a stable indexing key — even where no relying party needs them." Correction recorded the same day: "no field is known to be missing"; item 27 "is a **preservation** constraint at freeze, not an addition." Scope: "what is loggable is what is presented". Pre-freeze, alongside items 17 and 25. [DOCKET 27 — candidate, not registered, docs/band-1-docket.md:485-517]

**R-7.25 (verifier / adjudicator vocabulary)** "the **verifier** is P9's pure function — bundle plus declared policy in, verdict out; *'if the verifier requires anything from an optional service, it is fundamentally broken.'* The **adjudicator** (the relying party) decides trust using the verdict plus anything else, including any log anyone built". An enumeration API "may feed a log and may never feed a verdict." [RULED (author) 2026-09-06 in substance, docs/band-1-docket.md:517-526]

### 7.3 Tending

**R-7.26 (the four-outcome tending record)** "Tending records custodial assessment, not an assumption that every assessment produces a renewal artifact. The record has one of four outcomes":

| Outcome | Condition |
|---|---|
| `NO_ACTION_REQUIRED` | "the custodian evaluated the declared triggers and recorded that none had fired" |
| `RENEWED` | "a trigger fired, or discretionary renewal occurred; the record references the resulting renewal artifact and its predecessor linkage is mechanically checked" |
| `ACTION_DUE` | "renewal is required but has not yet completed" |
| `FAILED` | "an attempted required renewal did not complete" |

"The last two outcomes make the gap visible rather than issuing a reassuring heartbeat." [REGISTERED A3 §A3.5, docs/phase-0-prereg-amendment-3.md:384-397 — no author-decision marker on this passage; the `[AUTHOR DECISION — ratified -- 2026-08-08]` block begins at :424]

**R-7.27 (record contents)** "Every outcome exposes the policy and version applied; observations and their provenance; mechanically evaluated trigger results; judgment-based conclusions; unavailable observations; and, when applicable, the renewal-artifact reference and predecessor-link result." "The record proves only that a named custodian made the recorded assessment." [REGISTERED A3 §A3.5, docs/phase-0-prereg-amendment-3.md:399-405]

**R-7.28 (conditional visibility)** "Given an available monitoring clock and custodial record, crossing a trigger without the required tending record produces a visible stale condition." "The claim that a chosen trigger precedes an unforeseen failure of the protected mechanism is an exposed operational assumption, periodically reassessed — never a Tessera guarantee." [REGISTERED A3 §A3.5, docs/phase-0-prereg-amendment-3.md:407-414]

**R-7.29 (who can observe)** "Custodial-health monitoring and any relying party holding a current custodial record may observe the condition. The stateless verifier of an old bundle cannot: silence is not contained in the bundle." [REGISTERED A3 §A3.5, docs/phase-0-prereg-amendment-3.md:415-418]

**R-7.30 (tending never enters a bundle verdict)** "Tending health therefore never changes a receipt's P4 verdict or protocol standing." Reaffirmed among the things A3 explicitly does not change: "P9 statelessness (tending state never enters a bundle verdict)". Custodial health "is separately obtainable current information, not an input to the stateless base receipt verdict." [REGISTERED A3 §A3.5 / §A3.8 / §A3.10, docs/phase-0-prereg-amendment-3.md:418-419; :702-704; :865-871]

**R-7.31 (clock roles)** "The custodial policy declares its trigger classes, observation sources, uncertainty treatment, and any maximum assessment interval. Operational observation time governs when an assessment becomes due; external chain time supplies existed-by evidence for tending and renewal artifacts. Staleness is evaluated relative to the policy's declared operational clock and trust assumptions, never inferred from raw block timestamps alone." [RULED (author) 2026-08-08, docs/phase-0-prereg-amendment-3.md:438-445]

**R-7.32 (cadence)** "The cadence parameter lives in each custodial policy or profile, not as one universal constant; what Band 0 ratifies is the required parameter schema and the clock-role invariants above." No global duration is frozen "before custodial practice exists." [RULED (author) 2026-08-08, docs/phase-0-prereg-amendment-3.md:447-452] [OPEN — §11 O-47]

**R-7.33 (design obligations left open)** "Exact trigger expressions, cadence, clock, monitoring surface, and succession mechanism remain design obligations. They receive their own trust assumptions and do not reuse δ, ε, or k merely because the temporal modeling pattern is familiar." [REGISTERED A3 §A3.5, docs/phase-0-prereg-amendment-3.md:419-423] [OPEN — §11 O-37]

**R-7.34** Candidates, not registered: observable deadlines carried on `ACTION_DUE`/`FAILED` with the visibility boundary stated explicitly (13); the renewal window itself attested and visible in the tending record, "so a custodian cannot claim the trigger never fired" (14); a minimal tending-policy skeleton for the demonstration, flagged in the docket as a registration change if required at Band 0 exit (15); and a dead-project demonstration that explicitly tests that "an old bundle's `VALID_STRICT` is unaffected when custodial records are unavailable and the tending check reports `UNVERIFIABLE`" (16). [DOCKET 13-16 — candidates, not registered, docs/band-1-docket.md:117-132]

**R-7.34a (challenge rotation: two conformance-vector layers)** Conformance vectors are two layers: "a **fixed floor** in the bundle (memorizable, and acceptably so — a floor need only catch a naive fail-open verifier), and **novelty minted outside the bundle as custodial practice**." "A bundled generator cannot by itself guarantee non-exposure or replace custodial rotation". Custodial minting "records its evaluation conditions." [REGISTERED A3 §A3.5, docs/phase-0-prereg-amendment-3.md:453-461]

**R-7.34b (a failed new challenge has three readings)** When an existing verifier fails a new challenge, the failure is "a **measurement with three readings**, disposed under amendment discipline": contamination exposed; the challenge exceeds the Designated Community's declared competence, in which case discard it or amend the declaration; or the bundle genuinely lacks what the challenge needs, a real gap to be fixed in the bundle. [REGISTERED A3 §A3.5, docs/phase-0-prereg-amendment-3.md:461-469]

**R-7.35** Refusal reporting "is issuance-time operational machinery, not §A3.5 tending — the two may share implementation later without sharing registration." [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:616-619]

### 7.4 Agility

**R-7.36 (identifier-binding invariant)** "The algorithm identifier and all parameters that affect interpretation are unambiguously parsed and cryptographically bound to the exact signed object. No substitution or alternative interpretation may preserve verification." [REGISTERED A3 §A3.6, docs/phase-0-prereg-amendment-3.md:485-490]

**R-7.37 (identifier location)** The location is pinned "inside the canonical payload under P3's obligations; P8's four-field frame layout is unchanged", leaving open only the exact encoding, "which P8's framing proof and golden vectors must fix before Band 0 exit." A mandatory canonical-payload field "is the current implementation candidate … but the amendment does not freeze that tactic before the proof and vectors." [RULED (author) 2026-08-08, docs/phase-0-prereg-amendment-3.md:491-502] [OPEN — §11 O-03]

**R-7.38 (verdict boundary)** "`UNVERIFIABLE` for exactly one case — a well-formed, correctly bound, but unsupported algorithm identifier. `INVALID` for: missing identifier; identifier/signature encoding mismatch; malformed parameters; an identifier prohibited by applicable policy; substitution of the signed identifier; a known algorithm whose signature fails." [REGISTERED A3 §A3.6.2 (adopted, exact), docs/phase-0-prereg-amendment-3.md:503-508] [RULED — §12 C-07, A7 §A7.5]

**R-7.39 (landed twice)** Required: "a software red-bar suite verifying the signing-provider interface with the PQ implementation stubbed; and the formal model's P4-partition transition with a broken companion — a verifier that fail-opens past an unknown algorithm must go red." [REGISTERED A3 §A3.6, docs/phase-0-prereg-amendment-3.md:509-512]

**R-7.40 (the permanent canary)** "one permanently reserved unrecognized algorithm identifier remains in the test suite after a real PQ provider lands, so the `UNVERIFIABLE` path is exercised forever." A conformance vector ships in the bundle's fixed floor: "a signature in an algorithm you do not know; the correct verdict is `UNVERIFIABLE`." [REGISTERED A3 §A3.6, docs/phase-0-prereg-amendment-3.md:513-520]

**R-7.41 (the PQ path)** "The PQ signature implementation is deferred from the proof of concept and **gates the production version** — the demonstrated capacity to add an algorithm is the registered 'future resistant' claim, not a bet on which algorithm survives." "The portable GPG leg is the real gap; OTS is the independent temporal anchor and does not fill a signing gap." No PQ algorithm is selected. [REGISTERED A3 §A3.6, docs/phase-0-prereg-amendment-3.md:473-480; REGISTERED prereg §4, docs/phase-0-prereg.md:339-345]

**R-7.42 (hybrid dual signing)** "Hybrid classical+PQ dual signing is explicitly deferred to a deployment profile or later amendment — with a clear conscience, recorded here." [REGISTERED (deferral) A3 §A3.6, docs/phase-0-prereg-amendment-3.md:480-483] [OPEN — §11 O-13]

**R-7.43 (key lifetime and rotation)** Candidate, not registered anywhere in the record. The author's concern, in his words: *"key lifetime becomes a safeguard against someone surreptitiously taking over the service and pretending to be Tessera."* Facts established the same day: no declared maximum validity window for the issuer key, no rotation cadence, and no verifier behaviour at the window boundary is registered; "lifecycle" in the record means binding-form lifecycle (item 18) and "rotation" in A3.5 means challenge-vector rotation. Candidate for registration before format freeze "if the window or boundary behaviour affects the bundle's fields; otherwise Band 1 policy." [DOCKET 26 — candidate, not registered, docs/band-1-docket.md:386-410]

**R-7.44** Candidate rules under docket 26, neither agreed: (i) "a replacement key is accepted only inside a declared band before the current key's expiry"; (ii) the authority channels' expiry bands are staggered so no instant has more than one channel in rotation. The author's reason, in his words: *"By staggering rotation periods it makes it more difficult for a single entity to compromise them in a way that is not detectable."* [DOCKET 26 — candidate, not registered, docs/band-1-docket.md:411-418; :434-446] [OPEN — §11 O-19]

**R-7.44a** What stands in docket 26 without collaborator objection: "rotation is the moment a channel's trust root is replaced and therefore the most attractive moment for a holder of a stolen key; that threat is absent from A1.3 and should be registered." The narrower condition the staggering argument needs is that "**channel-key rotation must itself be a visible, endorsed object** … and verifiers must check key history, not only the current key." [DOCKET 26 — candidate, not registered, docs/band-1-docket.md:429-433; :448-453]

**R-7.44b** Recorded facts bearing on the governance premise: the present channels are "organisationally distinct but under one jurisdiction", so multi-government resistance "is not held by the present channel choice"; and the attestation company itself is named as the weak spot, "since it holds the accounts on every channel plus the issuer key: correlated custody at the account layer." Key-rotation policy is "explicitly deferred from the current round by the author". [DOCKET 26 — candidate, not registered, docs/band-1-docket.md:454-458; :470-475; :505-508]

### 7.5 Renewal

**R-7.45** Renewal is RFC 4998 (ERS) renewal under an RFC 4810-style cryptographic-maintenance policy, by custodians, before the old mechanism becomes unreliable; "renewal wraps, it never replaces". [REGISTERED A3 §A3.4 claim 3, docs/phase-0-prereg-amendment-3.md:273-278]

**R-7.46** Old payloads are never re-signed: "a **superseding attestation wraps the original package** and signs *that* with the new-algorithm key. The inner attestation's bytes, signatures, and OTS proof are immutable; the wrapper is a new layer with its own time-anchor." Each layer records which canonical form it used; nesting depth is bounded by willingness to pay, "not by a protocol cap." [REGISTERED prereg §4, docs/phase-0-prereg.md:339-355]

**R-7.47** The wrapper "commits to the inner package's **bytes**, **not** to the inner receipt's *verification result* at wrap time" and does not re-evaluate the original claim. [REGISTERED prereg §4, docs/phase-0-prereg.md:356-364]

**R-7.48 (cumulative wrapping)** Candidate: state that simple RFC 4998 timestamp renewal is excluded and only hash-tree (cumulative) renewal is used, "cumulative wrapping stops the hash-transition case being special and stops a broken middle link severing the chain." The docket records this as "One registered sentence; no mechanism change." [DOCKET 20 — candidate, not registered, docs/band-1-docket.md:269-282]

**R-7.49 (verdict composition along a renewal chain)** Candidate, not registered: (a) that a renewal chain is the A3.2 item 4 per-layer case extended in time, evaluated link by link under each link's epoch, which "depends on the registry-epoch material deferred under item 18"; (b) what one `UNVERIFIABLE` link means for the links beneath it, the honest candidate rule being "*report per link, never propagate as `INVALID`, and state which links the verifier could reach from its trust root*"; (c) where standing sits on a chain, namely the innermost issuance identity. "Disposition is the author's; nothing here is adopted." [DOCKET 19 — candidate, not registered, docs/band-1-docket.md:245-267] [OPEN — §11 O-30]

**R-7.50 (lineage completeness)** Candidate, not registered: "A wrap commits to the *full known lineage* of prior wrappers, unfavorable members included, so that pruning by omission becomes discoverable evidence rather than silent loss." Wrapper-level equivocation, "two wraps of the same package by one key, each claiming completeness", is the A2 residue one level up "and should be named with the standing decision's G4 treatment (boundary stated, closure not claimed), never as a closure." [DOCKET 21 — candidate, not registered, docs/band-1-docket.md:284-292]

**R-7.51 (independence comes from anchors, not custody)** Candidate, not registered: "cumulative depth from one custody line is one thread that merely looks dense, and each epoch's wrapper is independent testimony *only* through its own contemporaneous anchor. A 2106 examiner's forgery-cost estimate rests on the anchors, not on the wrap count." [DOCKET 22 — candidate, not registered, docs/band-1-docket.md:294-302]

**R-7.52 (per-prior verdict snapshots: registered AGAINST)** The renewal wrapper is ruled out for carrying snapshots of prior links' verdicts, by author decision, because that "would be a form of re-evaluation." The role exists as A3.8's optional signed verification report, "a distinct typed wrapper" whose bounded claim is that an identified evaluator assessed an identified bundle under an identified environment and obtained the enclosed result. A density report "is buildable, from A3.8 report wrappers interleaved with A3.4 renewal wrappers, and must not be folded into the renewal wrapper itself." Docket disposition: "no change to the record". [REGISTERED prereg §4 + A3 §A3.8, docs/phase-0-prereg.md:356-364; docs/phase-0-prereg-amendment-3.md:712-720; DOCKET 23 — no change, docs/band-1-docket.md:303-320]

**R-7.53** Signer authority, key lifecycle and report policy for the optional signed verification report "belong to that separate attestation profile; they are not smuggled into the base verifier contract." [REGISTERED A3 §A3.8, docs/phase-0-prereg-amendment-3.md:718-720]

### 7.6 Form lifecycle

**R-7.54** The binding-form lifecycle and the reference-verifier obligation are a registered plan with nothing implemented: "**RULED 2026-08-13 (author): DEFERRED — plan retained, nothing implemented.**" The retained plan comprises the three form states (registered / issuable / retired), issuance-time registry-epoch judgment with the epoch inside the envelope and checked against the independently established issuance interval, append-only reference-verifier support at the shared binding layer, and CI gating before a form becomes issuable. Both direct and digest remain permitted protocol forms; the deferral removes the lifecycle's issuable/retired classification, not the permission. Activation: the lifecycle is "Inert until a second binding form becomes issuable, which is separately gated on the P7/P8 cross-form substitution negative control"; the deferral was checked to be free because "no envelope field is required under any live candidate". Taking item 18 up also revives docket 17 subjects (b) and (c) and the custody A/B fork. [DEFERRED docket 18, docs/band-1-docket.md:220-232, :202-208; RULED (author) 2026-08-13, formal/spike/first-link/DECISION.md:436-461, :946-955]

---

## 8. Parameters and constants

Scope: protocol constants and the values the models actually check. Review boxes and timeboxes are PROCESS and are excluded. Every protocol constant below is ratified or revised, on the record, at Band 0 exit.

**R-8.1** δ and ε belong to the verifier, not the receipt; a receipt records its issue-time policy version and the observed anchor delay and may not choose its own temporal tolerances. [REGISTERED A1 P5, docs/phase-0-prereg-amendment-1.md:173-177]

**R-8.2** A verifier may choose stricter bounds; no degraded policy may enlarge δ or ε beyond the strict maxima. [REGISTERED A1 P5, docs/phase-0-prereg-amendment-1.md:177-184]

**R-8.3** δ, ε, k, N and S are ratified (or revised, on the record) at Band 0 exit. [REGISTERED A1 P5, docs/phase-0-prereg-amendment-1.md:180-190; A2 §A2.1/§A2.3, docs/phase-0-prereg-amendment-2.md:106-113, 270-274; tracker formal/PROPERTIES.md:167-168]

**R-8.4** N attempts give a nominal lifecycle budget of N × (δ + S), twelve days at the working defaults: a nominal budget, not a proven wall-clock bound on the process. [REGISTERED A2 §A2.3, docs/phase-0-prereg-amendment-2.md:270-274]

**R-8.5** Bare "within δ" is forbidden in registered text; the A2.1 predicate is cited explicitly, `confirmed_at` at depth k, one-sided against the declared time, with ε on the lower bound. [RULED (author) 2026-09-04, formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:223-241]

**R-8.6** Custodial trigger expressions, cadence, clock, monitoring surface and succession receive their own trust assumptions and do not reuse δ, ε or k merely because the temporal modeling pattern is familiar. [REGISTERED A3 §A3.5, docs/phase-0-prereg-amendment-3.md:419-423]

**R-8.7** Nesting depth for wrappers is bounded by willingness to pay, not by a protocol cap. [REGISTERED prereg §3.1, docs/phase-0-prereg.md:352-355]

| Symbol | Meaning | Working default | Where registered | Ratification | Value each model checks |
|---|---|---|---|---|---|
| δ | Backdating bound; upper side of the anchor and confirmation windows | **72 h** | A1 P5, docs/phase-0-prereg-amendment-1.md:177-184 | Ratified or revised at Band 0 exit | P5P6 `DeltaMax = 3` (cfg:1-5); P5c `Delta = 3` (cfg:15-19); Bridge `Delta = 2` (cfg:1-14). Scaled stand-ins; the models check the window's logic, not the magnitudes |
| ε | Post-dating bound; lower side of the anchor window | **24 h** | A1 P5, docs/phase-0-prereg-amendment-1.md:177-184 | Ratified or revised at Band 0 exit | P5P6 `EpsilonMax = 1`; Bridge `Epsilon = 1`. **Absent from P5c** (no ε side under the fused clock, `P5c_IssuanceProtocol.tla:78-82`) |
| k | Minimum confirmation depth for a shipped anchor | **6** | A1 P5 corollary, docs/phase-0-prereg-amendment-1.md:186-190 | Ratified with δ and ε at Band 0 exit | Header says k = 6 (`P5c_IssuanceProtocol.tla:26-29`); P5c cfg `DepthK = 2` is **k = 3**; Bridge cfg `KConf = 3`. The checked `DepthK = 2` is evidence for the checked abstraction, not evidence at the registered parameter; the default is not changed to match it, and the evidence is owed by exit item E18 (R-8.9) [RULED — §12 C-13, A7 §A7.8] |
| `DepthK` | Model convention, blocks after inclusion; `DepthK = k − 1` | **5** (for k = 6) | A2 §A2.1, docs/phase-0-prereg-amendment-2.md:208-214 | With k | P5c cfg `DepthK = 2`; Bridge cfg `DepthK = 2`, with `PinAgreement == DepthK = KConf - 1` checked as an invariant, never `KConf = 6` (`P5cP5P6_Bridge.tla:188-192`) |
| N (`MaxAttempts`) | Bound on issuance attempts before refusal | **3** | A2 §A2.3, docs/phase-0-prereg-amendment-2.md:252-274 | Ratified at Band 0 exit alongside δ, ε, k, S | P5c `MaxAttempts = 3` (cfg:15-19). **Not modelled in the bridge** (single attempt) |
| S | Operational slack constant on the attempt lifecycle, `declared + δ + S` | **24 h** | A2 §A2.1 clock-roles ruling, docs/phase-0-prereg-amendment-2.md:106-113 | Joins δ, ε, k, N for ratification at Band 0 exit | Only in `P5cP5P6_BridgeSlack.tla` / `_Latch.tla` as `Slack`, declared ruling evidence rather than protocol semantics. P5c is the **S = 0** instance (`P5c_IssuanceProtocol.tla:34-45`) |
| Review-staleness threshold | Staleness past which the review-recency invariant fails | **none declared** | prereg §4.7, docs/phase-0-prereg.md:564-572 | Undeclared | Not modelled [OPEN — §11 O-45] |
| Key TTL (commit-signing key) | Validity window of the passphraseless local key | **6 months**, expires 2026-12-07 | prereg §4.2, docs/phase-0-prereg.md:454-463 | Revisit trigger at real reliance (`:465-469`) | Not modelled. No issuer-key lifetime or rotation cadence registered [DOCKET 26, docs/band-1-docket.md:385-400] [OPEN — §11 O-19] |
| Canonicalization version id | Per-layer identifier of the frozen canonical form | RFC 8785 (JCS); identifiers not enumerated | prereg §4.3, docs/phase-0-prereg.md:486-512; A1 P8, docs/phase-0-prereg-amendment-1.md:255-264 | Binary layout and golden vectors fixed before the Band 1 freeze | A frame field in the theory library (`framed`, D-5/D-6); no version values checked [OPEN — §11 O-01] |
| Tending cadence | Maximum custodial assessment interval | per custodial policy; no universal constant | A3 §A3.5, docs/phase-0-prereg-amendment-3.md:447-452 | Band 0 ratifies the parameter schema and the clock-role invariants, not a duration | Not modelled [OPEN — §11 O-47] |
| T (retention horizon) | Bounded horizon after which the refusal record's delivery expires | **none declared** | A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:583-592; DOCKET 2, docs/band-1-docket.md:18-24 | Declared per deployment | Not modelled [OPEN — §11 O-15, O-48] |
| Bundle-size budget | Declared per-bundle byte budget; above it, content-addressed reference plus published store | **none declared** | DOCKET 9, docs/band-1-docket.md:54-56 | Candidate, not registered | Not modelled. If it pushes transcribed content behind a reference, first-link criterion 4 must be re-scored (`formal/spike/first-link/DECISION.md:261-275`) [OPEN — §11 O-08] |

**Model-harness bounds, not protocol constants:** P5P6 `MaxTime = 6`, `RcptTolMax = 6` (`RcptTolMax > DeltaMax` so receipts *can* overclaim); P5c `MaxTime = 14`, which must be at least `MaxAttempts * (Delta + 1) = 12` or every refusal invariant passes vacuously; Bridge `MaxTime = 6`, `MaxSkew = 2`, `MaxBlocks = 4`. [MODELLED, formal/tla/P5P6_TemporalRevocation.cfg:1-5; formal/tla/P5c_IssuanceProtocol.tla:87-101; formal/tla/P5cP5P6_Bridge.cfg:1-14]

**R-8.8** `MaxSkew` in the slack modules is a declared environment/operational-policy assumption, not a consensus bound; every result there reads conditionally. [MODELLED BridgeSlack header, formal/tla/P5cP5P6_BridgeSlack.tla:1-59]

**R-8.9** The strict default k = 6 (`DepthK = 5`) stands, subject to ratification at Band 0 exit as registered; the default is not changed to match a small checked configuration. The P5c and bridge configurations checked at `DepthK = 2` remain evidence for the checked abstraction and are not evidence at the registered parameter, as the reading aid already states (`formal/tla/READING-AID-P5c.md:226-231`). Band 0 exit item **E18** owes either (a) the P5c, P5P6 and bridge modules re-run at `DepthK = 5` with `MaxTime` and the other bounds sized so that every registered witness still fires, or (b) a written argument, reviewed by a non-author model, that every checked invariant is independent of the value of `DepthK` above the minimum the witnesses need. Green at (a) is evidence at the parameter; (b) is evidence for the family of parameters. The tracker's parameter box is unchanged. [RULED (author) 2026-09-14; instrument A7 §A7.8, PROPOSED; §12 C-13] [OPEN — §11 O-44]

---

## 9. Invariants and failure behaviour

### 9.1 The hard rules as invariants

**R-9.1** Key material is never logged: not private keys, not passphrases, not "redacted-but-present," not in a debug branch, not as a joke. Enforced by structured logging that cannot serialize key types plus a CI secret-scan gate that fails the build if signing material reaches a log sink. Discipline is not the control; the type system and CI are. [REGISTERED prereg §4.1, docs/phase-0-prereg.md:447-452]

**R-9.2** The canonical form is frozen and explicitly versioned: it never changes silently; any change is a new, versioned canonical form, and every receipt records which version it used. [REGISTERED prereg §4.3, docs/phase-0-prereg.md:486-494]

**R-9.3** The canonical form binds to RFC 8785 (JCS); any value not exactly a double is string-encoded, never a JSON number. Canonicalization test vectors are part of the public verifier conformance suite; every canonicalization version has byte-for-byte golden examples; wrappers record both inner and outer canonicalization versions. [REGISTERED prereg §4.3, docs/phase-0-prereg.md:496-512]

**R-9.4** The claim is boundary-unambiguity only. No blanket "length-extension-resistant" claim is made. [REGISTERED prereg §4.3, docs/phase-0-prereg.md:514-517] Length is registered as bound into the canonical bytes and not a side field, while P8 places `payload_length` in the frame around the JCS payload. [RULED — §12 C-03, A7 §A7.1]

**R-9.5** The verification path depends on zero service-side state. The operational database is never on the path that verifies an attestation. [REGISTERED prereg §4.4, docs/phase-0-prereg.md:519-525]

**R-9.6** Verification yields a typed result, never a bare boolean (R-5.38). [REGISTERED prereg §4.6, docs/phase-0-prereg.md:555-562]

**R-9.7** The red-bar suite's attacks are authored by a different model than the one that wrote the implementation; test/code separation is CI-enforced. [REGISTERED prereg §4.5, docs/phase-0-prereg.md:548-553]

**R-9.8** The service attests when it was last adversarially reviewed, signed and timestamped, and review staleness beyond a declared threshold fails the invariant. No threshold value is declared anywhere in the record. [REGISTERED prereg §4.7, docs/phase-0-prereg.md:564-572] [OPEN — §11 O-45]

**R-9.9** The `canonical(payload) → bytes` function is the true root of trust and must be frozen and explicitly versioned; the verification path must depend on zero service-side state. These are the two hard invariants the signing decision incurs. [REGISTERED prereg §3.1, docs/phase-0-prereg.md:413-415]

**R-9.10** The extractability boundary is not a design priority, with one load-bearing exception: the canonicalization function, which is a hard invariant. [RULED prereg §3.1, docs/phase-0-prereg.md:417-435]

**R-9.11** The commit-signing key is passphraseless with a declared TTL on a firewalled workstation; the host-compromise threat is accepted, mitigated by short TTL plus an already-generated revocation certificate. The registered trigger to revisit is reliance: if anyone relies on issued attestations, shorten the TTL toward monthly and move to the deferred enclave/HSM model so passphraseless-ness stops being acceptable at all. [REGISTERED prereg §4.2, docs/phase-0-prereg.md:454-469]

**R-9.12** Old payloads are never re-signed. A superseding attestation wraps the original package and signs that with the new-algorithm key; the inner attestation's bytes, signatures and OTS proof are immutable, and the wrapper is a new layer with its own time-anchor. Nesting depth is bounded by willingness to pay, not by a protocol cap. [REGISTERED prereg §3.1, docs/phase-0-prereg.md:339-355]

**R-9.13** One permanently reserved unrecognized algorithm identifier remains in the test suite after a real PQ provider lands, so the `UNVERIFIABLE` path is exercised forever, and a conformance vector ships in the bundle's fixed floor: "a signature in an algorithm you do not know; the correct verdict is `UNVERIFIABLE`." [REGISTERED A3 §A3.6.2, docs/phase-0-prereg-amendment-3.md:513-520]

### 9.2 Fail-closed behaviour by failure mode

**R-9.14** Every row below whose provenance tag is REGISTERED or RULED is required behaviour; rows tagged DOCKET are candidates and are not requirements. No row's result may be replaced by an aggregate judgment. [REGISTERED A3 §A3.2 item 4, docs/phase-0-prereg-amendment-3.md:161-164; A3 §A3.8, docs/phase-0-prereg-amendment-3.md:703-704]

| Failure mode | Required outcome | Source |
|---|---|---|
| Fewer signatures than the manifest requires | `INVALID`; `VALID_DEGRADED` only under an explicit, recorded policy inside the A1.2.1 waivable set | [REGISTERED A1 §A1.2 P2, docs/phase-0-prereg-amendment-1.md:121-128] |
| Signer slots signing different content — **any one** of the six non-fingerprint fields (object type, algorithm, identity, manifest hash, canonicalization version, payload) unequal across required signer slots; the registered rule is that all six are equal, so one differing field suffices. Registered under reading (a) of the §A5.4 framing fork [OPEN — §11 O-05] | `INVALID` | [RULED A5 §A5.4, docs/phase-0-prereg-amendment-5.md:156-190] [MODELLED S-P2 Q6-C red on exactly `Spliced`] |
| Well-formed, correctly bound, unsupported algorithm identifier | `UNVERIFIABLE` | [REGISTERED A3 §A3.6.2, docs/phase-0-prereg-amendment-3.md:503-505] |
| Missing, mismatched, malformed, prohibited, or substituted algorithm identifier; known algorithm whose signature fails | `INVALID` | [REGISTERED A3 §A3.6.2, docs/phase-0-prereg-amendment-3.md:505-508] |
| Unknown binding-form identifier; known-but-unsupported binding form | `UNVERIFIABLE`, with two distinct reason codes | [ADOPTED (author) first-link/DECISION.md:366-405; labelled ADOPTED, not RULED, at :369-372] |
| Missing, malformed, duplicate, substituted, inconsistently encoded, or empty required binding-form set | `INVALID`, which dominates a co-occurring `UNVERIFIABLE` | [ADOPTED (author) first-link/DECISION.md:366-391; labelled ADOPTED, not RULED, at :369-372] |
| Late anchor: `confirmed_at > declared + δ` | `INVALID` (the chain-late subclass rejected outright) | [REGISTERED A2 §A2.2, docs/phase-0-prereg-amendment-2.md:228-235] [MODELLED `AbandonedArtifactRejected`, formal/tla/P5P6_TemporalRevocation.tla:188-199] |
| Anchor outside `[declared − ε, declared + δ]` | `INVALID` | [REGISTERED A1 §A1.2 P5, docs/phase-0-prereg-amendment-1.md:159-171] [MODELLED `WindowRespected`, formal/tla/P5P6_TemporalRevocation.tla:169-175] |
| Block headers `h … h + k − 1` unavailable | `UNVERIFIABLE` | [REGISTERED A2 §A2.2, docs/phase-0-prereg-amendment-2.md:236-248]; not modelled |
| Revocation effective at or before `anchor_time`, or at or before `declared_issue_time` | `INVALID` | [REGISTERED A1 §A1.2 P6, docs/phase-0-prereg-amendment-1.md:199-233] [RULED A4 §A4.3] [MODELLED `AuthorizedThroughWindow`, `ForgeryRejected`, formal/tla/P5P6_TemporalRevocation.tla:142-167] |
| Every external authority evidence for a layer unavailable or unperformable | `UNVERIFIABLE`; never `VALID_DEGRADED` | [REGISTERED A3 §A3.2 item 2, docs/phase-0-prereg-amendment-3.md:146-149] |
| Required evidence present, validation performed, fails | `INVALID` | [RULED A5 §A5.2, docs/phase-0-prereg-amendment-5.md:93-121] |
| Waived evidence present and failing | verdict unchanged; the observation is recorded (one of the six values). `anchor-late` as a waived-check observation sits against A2 §A2.2's non-waivability of temporal-anchor consistency [RULED — §12 C-05, A7 §A7.3] | [RULED A5 §A5.2/§A5.3, docs/phase-0-prereg-amendment-5.md:93-154] |
| Custody retrieval failure of anything outside the envelope | `UNVERIFIABLE` with a distinct reason, and no required check may depend on such a fetch (R-5.3) | [DOCKET 17 — candidate, docs/band-1-docket.md:133-145] |
| Malformed standing evidence (terminal disposition contradicting the lineage's own entry) | `UNVERIFIABLE` / `STANDING_EVIDENCE_MALFORMED`; never `ESTABLISHED` | [RULED first-link/DECISION.md:834-843] [MODELLED S-STANDING ss_q1d:302-317] |
| TLR anchor failing the A2.1 predicate against the declared terminal-disposition time | `UNVERIFIABLE` / `STANDING_EVIDENCE_TEMPORAL_MISMATCH` | [RULED first-link/DECISION.md:844-847] |
| TLR signed by any key other than the entitled key | `STANDING_EVIDENCE_SIGNATURE_INVALID` | [DECIDED standing-probe/DECISION.md:61-67] [MODELLED ss_q1d:334-340, 360-363] |
| Transplanted standing evidence (handle mismatch) | `ABSENT` / `STANDING_EVIDENCE_MISMATCH`, or `SUPERSEDED` for the second transplant shape; the ordinal-bound variant accepts both and is the red bar | [DECIDED standing-probe/DECISION.md:68-71] |
| Wrapper lies about the inner canonicalization version | reject the wrapper layer | [RULED A5 §A5.5, docs/phase-0-prereg-amendment-5.md:192-200] [MODELLED S-P7 Q7-C red on exactly `VersionLied`] |
| Spliced frames across signer slots | `INVALID`; a payload-splicing companion must go red | [RULED A5 §A5.4, docs/phase-0-prereg-amendment-5.md:156-190] |
| Issuance: predicate fails at issuance time | attempt discarded and re-issued, counted against N; never shipped | [REGISTERED A2 §A2.1/§A2.3, docs/phase-0-prereg-amendment-2.md:160-162, :252-262] [MODELLED `ExpiredCannotShip`, formal/tla/P5c_IssuanceProtocol.tla:305-310] |
| Issuance: N attempts exhausted | explicit refusal, durably recorded, entered atomically with the transition that expires the final attempt's window; a first-class protocol outcome, not an error path | [REGISTERED A2 §A2.3, docs/phase-0-prereg-amendment-2.md:266-284] [MODELLED `NoSilentDeadlock`, `RefusedOnlyWhenExhausted`, `RefusalLatched`, formal/tla/P5c_IssuanceProtocol.tla:312-337] |
| Refusal: delivery or publication failure | cannot reopen issuance, consume another attempt, or erase the refusal; `DELIVERY_FAILED` / `DELIVERY_EXPIRED` / `PUBLICATION_FAILED` / `PUBLICATION_EXPIRED` are visible terminal dispositions, never silent deletion | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:571-572, :583-602]; not modelled [OPEN — §11 O-71] |
| Refusal: authority dies between the local transition and handoff | named as an irreducible residual; never disguised as `PUBLICATION_FAILED`. No artifact lacking terminal-disposition evidence can claim protocol standing | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:623-637] |
| Tending record unavailable, or a trigger crossed without one | a visible stale condition given an available monitoring clock and custodial record; the stateless verifier of an old bundle cannot observe it; the receipt's verdict and standing are unaffected | [REGISTERED A3 §A3.5, docs/phase-0-prereg-amendment-3.md:407-419] |
| Payload Representation Information absent or uninterpretable | affects payload interpretability, never the P4 envelope verdict | [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:363-364] |
| Issuance-profile dependency interpretation unavailable | `UNVERIFIABLE` for the affected check | [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:353-356] |

### 9.3 "Never happens" invariants

Each is tagged MODELLED with the registered claim it serves. A modelled invariant is evidence for the checked abstraction only.

| Invariant | Plain-language statement | Registered claim | Source |
|---|---|---|---|
| `Partition` | The verdict is always one of the four states; there is no fifth outcome and no boolean | A1 §A1.2 P4 | [MODELLED P4, formal/tla/P4_VerifierStates.tla:111-113] |
| `Monotonicity` | A failed non-waivable check is `INVALID` under every legal policy; no waiver set promotes it | A1 §A1.2.1 | [MODELLED P4, formal/tla/P4_VerifierStates.tla:115-119] |
| `NoSilentPromotion` | An unperformable non-waivable check never yields any `VALID` state under any policy | A1 §A1.2.1, read with A4 §A4.2 | [MODELLED P4, formal/tla/P4_VerifierStates.tla:121-127] |
| `ValidNeedsNonWaivablePass` | Any `VALID` verdict implies every non-waivable check was performed and passed | A1 §A1.2.1 | [MODELLED P4, formal/tla/P4_VerifierStates.tla:129-133] |
| `StrictMeansEverything` | `VALID_STRICT` implies every check passed, not only the required ones | P4 / prereg §3.1 fail-closed default; the reading aid records that no supplied registered sentence defines strict this way | [MODELLED P4, formal/tla/P4_VerifierStates.tla:135-138] |
| `DegradedNeedsExplicitWaiver` | Degraded arises only from an explicit, nonempty waiver inside the waivable set | A1 §A1.2 "never as a default or a fallback" | [MODELLED P4, formal/tla/P4_VerifierStates.tla:140-143] |
| `UnverifiableIsHonest` | `UNVERIFIABLE` implies a required check was unperformable and none failed | A1 §A1.2 P4 with A4 §A4.2 precedence | [MODELLED P4, formal/tla/P4_VerifierStates.tla:145-150] |
| `ExactInvalid` / `ExactUnverifiable` / `ExactStrict` / `ExactDegraded` | Classification is pinned in both directions, so an over-conservative verdict function cannot pass | A1 §A1.2 P4 totality and exactness | [MODELLED P4, formal/tla/P4_VerifierStates.tla:160-175] |
| `ForgeryRejected` | Bytes signed at or after revocation are never strict-accepted, under every verifier policy, though the verifier cannot observe the signing moment | A1 §A1.2 P6 | [MODELLED P5/P6, formal/tla/P5P6_TemporalRevocation.tla:160-167] |
| `WindowRespected` | No strict-accepted receipt sits outside the verifier-policy window on any of the three conjuncts | A1 §A1.2 P5, A2 §A2.2 | [MODELLED P5/P6, formal/tla/P5P6_TemporalRevocation.tla:169-175] |
| `VerifierOwnsTolerances` | Acceptance never exceeds the global strict maxima whatever the receipt declares | A1 §A1.2 P5 | [MODELLED P5/P6, formal/tla/P5P6_TemporalRevocation.tla:177-186] |
| `ReceiptIndependence` | The verdict is identical under every receipt-declared tolerance pair; narrowing is caught as well as enlargement | A1 §A1.2 P5 | [MODELLED P5/P6, formal/tla/P5P6_TemporalRevocation.tla:201-221] |
| `AbandonedArtifactRejected` | An anchor whose block is in-window but whose k-th confirmation arrived past the window is never strict-accepted | A2 §A2.0/§A2.2 | [MODELLED P5/P6, formal/tla/P5P6_TemporalRevocation.tla:188-199] |
| `AuthorizedAtDeclared` | Acceptance implies the key was authorized at the declared issue time itself | A4 §A4.3 | [MODELLED P5/P6, formal/tla/P5P6_TemporalRevocation.tla:223-233] |
| `HonestCostIsExactlyTheWindow` | The only honest receipts the interval rule sacrifices are those revoked inside `(declared, anchor]` | A1 §A1.2 P6 fail-closed cost | [MODELLED P5/P6, formal/tla/P5P6_TemporalRevocation.tla:235-245] |
| `PinAgreement` | The depth convention `DepthK = k − 1` is checked, not assumed, so an off-by-one in either transcription goes red | A2 §A2.1 | [MODELLED bridge, formal/tla/P5cP5P6_Bridge.tla:188-192] |
| `ShippedDesignatedAgree` | For a shipped receipt, the block and timestamp the issuer evaluated are the ones the verifier derives from the shipped headers | A1.4 cross-model correspondence | [MODELLED bridge, formal/tla/P5cP5P6_Bridge.tla:194-201] |
| `HonestShipAccepted` | No honestly-shipped receipt fails the verifier under the issuance policy's tolerances | A2 §A2.1 no-disagreement guarantee | [MODELLED bridge, formal/tla/P5cP5P6_Bridge.tla:203-207] |
| `LateBurialRejected` | An abandoned artifact whose true k-th-confirmation timestamp falls outside the window is `INVALID` | A2 §A2.0/§A2.2 | [MODELLED bridge, formal/tla/P5cP5P6_Bridge.tla:209-217] |
| `NoShippedOrphan` | No shipped receipt's anchor is ever orphaned; nothing in the wild becomes permanently unverifiable through a tolerated reorg | A1 §A1.2 P5 corollary | [MODELLED P5c, formal/tla/P5c_IssuanceProtocol.tla:288-292] |
| `ShippedIsSound` | A shipped receipt has an anchor, in-window, buried to depth k, with those values frozen post-ship | A1 §A1.2 P5 corollary, A2 §A2.1 | [MODELLED P5c, formal/tla/P5c_IssuanceProtocol.tla:294-303] |
| `ExpiredCannotShip` | No expired declaration ever ships; discarded attempts stay discarded | A1 §A1.2 P5 corollary | [MODELLED P5c, formal/tla/P5c_IssuanceProtocol.tla:305-310]; stronger than the registered latched-eligibility expiry [SETTLED — §12 S-12] |
| `NoSilentDeadlock` | No reachable state has issuance dead but undocumented | A2 §A2.3 atomic entry | [MODELLED P5c, formal/tla/P5c_IssuanceProtocol.tla:312-319] |
| `RefusedOnlyWhenExhausted` | Refusal is recorded only on genuine exhaustion; shipped and refused are mutually exclusive | A2 §A2.3 | [MODELLED P5c, formal/tla/P5c_IssuanceProtocol.tla:321-330] |
| `RefusalLatched` | No step ever unsets a recorded refusal | A2 §A2.3 "and latches" | [MODELLED P5c, formal/tla/P5c_IssuanceProtocol.tla:332-337] |
| `Reattributed` unreachable | Honest bytes are never accepted under a key other than their signer's, even against an adversary with the registered DSKS capability | A1 §A1.2 P3, A1.3 item 3 | [MODELLED S-P3, formal/suite/s-p3/RESULTS.md:203-216; severed by Q3] |
| `PossessionTransplanted` unreachable | An accepted possession proof is a signature over the accepted manifest, which names the presented key's fingerprint | A1 §A1.5 item 3 / P10 | [MODELLED S-P3, formal/suite/s-p3/RESULTS.md:217-227; severed by Q4] |
| `Stripped` / `SignerForged` unreachable | Acceptance implies a signature from every signer the manifest's signed set names, each under that signer's own key | A1 §A1.2 P2 | [MODELLED S-P2, formal/suite/s-p2/RESULTS.md:285-299; severed by Q3, Q4] |
| `SetAltered` unreachable | No honest key is accepted as a signer of a manifest it never signed (under the fixture rule one key, one manifest) | A1 §A1.2 P2 | [MODELLED S-P2, formal/suite/s-p2/RESULTS.md:300-313; severed by Q5-C2] |
| `Spliced` unreachable | Required signers never attest different content in their own frames | A5 §A5.4 | [MODELLED S-P2 Q6, formal/suite/s-p2/proverif/sp2_q2_degraded_compromised.pv:275-284] |
| `TypeConfused` unreachable | Acceptance of framed bytes on a path as type T implies the bytes' committed object type is T | A1 §A1.2 P7 | [MODELLED S-P7, formal/suite/s-p7/RESULTS.md:495-517; severed by Q3 and ablation a10] |
| `Rescoped` / `InnerSigTransplanted` unreachable | A wrapper cannot rescope the inner artifact to another identity or key, and cannot transplant an inner signature | A1 §A1.2 P7 | [MODELLED S-P7, formal/suite/s-p7/RESULTS.md:518-545; severed by Q6a, Q6b, Q5c] |
| `VersionLied` unreachable | A wrapper's recorded inner canonicalization version always matches the inner frame's own | A5 §A5.5 | [MODELLED S-P7 Q7, companion Q7-C red on exactly this] |
| `StandingUnentitled` unreachable | An `ESTABLISHED` standing report is never computed against a key the presented tuple does not name | A3 §A3.7.1, ENUMERATION note 4 item 2 | [MODELLED S-STANDING, formal/suite/s-standing/RESULTS.md:454-467; severed by Q3] |
| `ReasonCollapsed` unreachable | Two different no-standing branches never emit the same reason code | ROUTED B9 | [MODELLED S-STANDING, formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:392-396] |
| `Aliased` unreachable | An `ESTABLISHED` report is never computed for a presented tuple other than the one embedded in the core its identity derives from | A5 §A5.6 | [MODELLED S-STANDING SS.Q6, formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:398-406] |
| P1 headline | Bytes accepted under an honest key are bytes that key signed | A1 §A1.2 P1, A3 §A3.1 | [MODELLED S-P1, formal/suite/s-p1/proverif/sp1_q2_degraded_compromised.pv:141-145; severed by Q3] |

**R-9.15** Every implication-shaped invariant above is guarded by a vacuity witness whose violation is the healthy result. TLC reports one violated invariant per state even under `-continue`, so a witness list is sound only if each witness has a state that violates it and none listed above it; the modules order witnesses most-specific-first. [PROPOSED C6 — ROUTED-2026-09-06.md:313-318 records C6 as "settled by the collaborator, listed for veto", not as an author ruling] [MODELLED `_Sanity` configurations, formal/tla/P4_VerifierStates.tla:177-188; formal/tla/P5P6_TemporalRevocation.tla:247-262; formal/tla/P5c_IssuanceProtocol.tla:348-369]

**R-9.16** Every invariant above is paired with at least one broken companion that must go red on exactly its named query: `P4_VerifierStates_Broken` (fail-open on unperformable), `P5P6_TemporalRevocation_Broken` (point-evaluated authorization), `_BrokenConf` (no confirmation conjunct), `_BrokenTol` / `_BrokenTolStrict` (receipt-enlarged / receipt-narrowed tolerances), `P5c_IssuanceProtocol_Broken` (shallow-anchor ship), `_BrokenSilent` (separately enabled refusal), `P5cP5P6_Bridge_BrokenAnchorSubst`, `_BrokenWallClock`, `_BrokenPin`, and the symbolic severing companions named in the table. [MODELLED companion set, formal/PROPERTIES.md; formal/tla/*_Broken*.tla]

**R-9.17** Termination is a contract obligation on the implementation, not a proven liveness property: the model proves the conditional safety half, that the refusal state is entered atomically and latches, and does not prove that the crossing occurs. The unbounded "eventually ships" claim likewise remains explicitly unproven. [REGISTERED A2 §A2.3, docs/phase-0-prereg-amendment-2.md:284-290] [MODELLED P5c scoped-out liveness, formal/tla/P5c_IssuanceProtocol.tla:62-76]

**R-9.18** A checked model is a model believed, not guaranteed, correct: a checked model plus a broken companion is evidence for the checked abstraction only. Timeout is mechanism failure, not property evidence. [RULED (author) 2026-08-29, formal/suite/ENUMERATION.md:426-452] [REGISTERED A3 §A3.3, docs/phase-0-prereg-amendment-3.md:245-248]

---

## 10. Outstanding obligations

This section lists what the record still owes, by the phase that owes it.
It copies status from `formal/PROPERTIES.md` and `formal/BAND0-EXIT.md`
and adds nothing; if it lags them, it is the defect.

### 10.1 Band 0 exit (the gate before any service code)

The finite list is `formal/BAND0-EXIT.md` §2, items E1–E18 (E18 added 2026-09-14 by A7 §A7.8). The items an
implementer will feel, with their effect on this document:

| Item | Obligation | Effect on this document when done |
|------|------------|-----------------------------------|
| E3 | P8 framing proof; golden vectors that fix the frame layout and the algorithm-identifier encoding | §3.2 frame layout and §3.4 identifier encoding move from OPEN to REGISTERED; §5.2 row (a) gains the exact rejection tests |
| E4 | P9 inspection artifact against the enumerated inputs; two-machine vector specified | §5.1 input list becomes the checked list |
| E5 | Capstone composition with the discharge matrix; ledger entries entered | §5.5 coverage table loses its "assumed from elsewhere" rows; cross-model joins become checked |
| E6 | Unknown-algorithm P4 transition; extended atomic-entry refusal invariant (tracker rows `A3.6.2`, `A3.7.2`) | §5.2 row (c) and §4 step 6 gain MODELLED tags |
| E8 | TLA+ ↔ symbolic correspondence mapping | §5.2's "registered vs modelled" column can cite one document |
| E9 | Author adjudication of the cross-family reviews; rows to `discharged` | Tags stay; the tracker status changes |
| E10 | Model-derived conformance vectors extracted | §5 gains vector references per check; run at H1a |
| E12 | Relying-party story published stand-alone | §1.5 becomes a pointer to the registered page |
| E14 | Parameter ratification δ, ε, k, N (and S) | §8 status column |
| E16 | This document | — |
| E18 | Confirmation-depth evidence at the registered parameter: either the P5c, P5P6 and bridge modules re-run at `DepthK = 5` with every registered witness still firing, or a non-author-reviewed argument that each checked invariant is independent of `DepthK` above the witnesses' minimum [RULED (author) 2026-09-14; instrument A7 §A7.8, PROPOSED] | §8's k row and R-8.9 gain evidence at k = 6, or a parameter-general argument; the §4.10 row 12 divergence closes |

### 10.2 H1a (Band 1 freeze) obligations named in the record

| Obligation | Source |
|------------|--------|
| Golden vectors (positive domain) and the rejection suite (negative domain) for `canonical()` and the frame | A1 §A1.2 P8; prereg §4.3 |
| Verification profile for P3's [assumption] half: library, encodings, low-order points, cofactor | A1 §A1.2 P3; COVERAGE-MAP row 3 |
| Model-derived conformance vectors run against the reference verifier; the concretizer reviewed under non-author discipline | A1 §A1.7 item 2 |
| A2.2 vector cases: late burial → `INVALID`; headers unavailable → `UNVERIFIABLE` | A2 §A2.2; PROPERTIES box |
| P9 two-machine vector with the §A5.1 cases (same bundle twice on one machine; optional service reachable and contradicting the bundle) | A5 §A5.1; docket 30 |
| P7 verdict-independence vector under each P4 verdict value, re-serializing wrapper as the red bar | A6 §A6.1; docket 32 |
| A3.9 issuance-path vector (`anchor_time = declared+δ+1`, `confirmed_at = declared+δ−1` → refuse to ship) and the bridge `_BrokenConjunct3Only` companion | A3 §A3.9; PROPERTIES P5c entry |
| P8 golden vectors for "what bytes are fingerprinted" and for each of the two fingerprint hardness routes separately; slot-bearing vector at forward-link registration | S-P3 RESULTS F3; docket 25 |
| Signing-provider red-bar suite with the PQ implementation stubbed; the permanent unrecognized-identifier canary | A3 §A3.6.2 items 3–4 |
| Renderer conformance vectors; rendering red bars | A3 §A3.8; docket 11 |
| Standing vectors S1–S4 with reason codes and a collapsing companion | ENUM note 4; H1a/P8 track |
| Standing vector: internally inconsistent TLR (terminal disposition contradicting the lineage entry) → `UNVERIFIABLE / STANDING_EVIDENCE_MALFORMED` | SC-3, formal/spike/first-link/DECISION.md:834-843; the vector-track assignment at formal/suite/s-standing/RESULTS.md:547-549 |
| Integrated adversarial lifecycle model (issuance → wrapping → supersession → refusal → verification → tending) | A3 §A3.9 (Kimi 2); gates the H1a freeze, not Band 0 |
| Degraded-verdict record format | A5 §A5.3; docket 28 |
| Encoding map for the signed frame: where each of A5 §A5.4's seven signer-specific bindings lives in bytes (envelope field, canonical payload under P3, or the manifest tuple committed to by hash), separating the requester's content from the signer-specific metadata; **pre-freeze**, and until settled the frame layout stays open and no signed-frame golden vector is final | A7 §A7.9 [RULED (author) 2026-09-14, PROPOSED]; docket 33; §11 O-79 |
| Forward-link / successor slot registration, including the four-mechanism × four-trace comparison, before format freeze | docket 25 (RULED location) |
| Custody of externally referenced verification inputs: what must remain obtainable, who retains it, discovery, retrieval testing, before any Band 1 freeze | docket 17 |
| Third-party log buildability as a preservation constraint at freeze | docket 27 |

### 10.3 Band 1 docket (unregistered; parked so nothing drops)

Items 1–32 of `docs/band-1-docket.md`, by area. None is a requirement
until registered; §11 carries each as an open item.

| Area | Items |
|------|-------|
| Issuance / operational | 1 local-GPG signing under automation; 2 refusal-residual bounding (T, `DELIVERY_EXPIRED` / `PUBLICATION_EXPIRED`); 3 OTS congestion behaviour |
| Verifier / bundle format | 4 numeric-precision rejection at ingestion; 5 fixed-width envelope encodings; 6 SPV header segment; 7 header authentication pinning; 8 historical trust-anchor store; 9 bundle-size budget; 10 embedded spec executable-in-principle; 28 degraded-verdict record format; 29 three verifier checks (now run, §A5.4–§A5.6) |
| Surfaces / conformance | 11 renderer vectors; 12 signed report as the only relayable form; 30 P9 vector cases; 31 this document; 32 P7 verdict-independence vector |
| Tending / custody / renewal | 13 tending visibility deadlines; 14 attested renewal-window parameter; 15 minimal tending-policy skeleton; 16 old-bundle stability without custodial records; 17 custody of external inputs; 18 binding-form lifecycle (DEFERRED); 19 verdict composition along a renewal chain; 20 renewal always cumulative; 21 wrapper-lineage completeness; 22 independence from anchors, not custody; 23 per-prior verdict snapshots (registered AGAINST in the renewal wrapper); 24 correlated vs uncorrelated custody; 25 forward-link slot (registration scheduled); 26 issuer key lifetime and rotation; 27 third-party log buildability |

### 10.4 Deferred by the pre-registration, gated on reliance or revenue

Higher-assurance signing (enclave/HSM), hardware token for the local
key, independent human formal-methods review, independent adjudication
of review counterexamples, billing, PCI certification. Sources: prereg
§4.2, §5, §8; A1 §A1.7.

---

## 11. Register of unresolved decisions

Every entry below is a decision the record leaves unmade, or a candidate the
record carries without registering. Nothing here is resolved by this
specification. "Working assumption" is what the record currently uses in the
absence of a decision; a blank means the record names none. Deadline values are
only those the record itself states: `pre-freeze` (before the Band 1 format
freeze), `Band 0 exit`, `H1a`, `none`.

Docket entries are `docs/band-1-docket.md` items, which that file's own header
declares unregistered: "Nothing here is registered; the purpose is that nothing
silently drops." Item 18 is DEFERRED by author ruling and item 23 is registered
AGAINST; both are carried here with that status. Entries marked *reading to
veto* are the five clerk readings collected in `formal/BAND0-EXIT.md` §5, which
that file offers for veto in one place. IDs are stable labels, not sort keys: O-67 and O-68 were added
after the first pass and sit in their areas below, O-69 to O-77 were added at the 2026-09-13 assembly to carry
section end-list items that had no register entry, O-78 was added by the 2026-09-13 repair pass
after the Codex review, O-79 was added by the 2026-09-14 Amendment 7 repair pass (the encoding map
A7 §A7.9 makes a pre-freeze precondition of O-01), and two IDs are absent by
withdrawal. **O-35** (the standing-evidence construction) is withdrawn: the
author's commit `fbf6387` (2026-09-04, "Another round: mostly decisions, a few
small clarifications.  Ratified and time to move forward.") is the commit that
carried the "Entered, 2026-09-04" note into
`formal/spike/standing-probe/DECISION.md`, so the terminal lineage record is the
selected construction (see S-13, and `formal/suite/ENUMERATION.md:486`,
amendment note 4). **O-60** (the C5 header read) is withdrawn: the read was
completed 2026-09-12 and all four answers are entered in
`formal/suite/READ-C5-2026-09-12.md` "Author's answers" (S-P1 one NO repaired,
S-P2 YES, S-P7 one NO repaired, S-STANDING YES).

77 open entries follow: Format 14, Issuance 9, Verification 19, Standing 5, Survivability-custody 7, Parameters 5, Process-exit 18.

| ID | Area | The decision | Working assumption | Settling artifact | Deadline | Sources |
|----|------|--------------|--------------------|-------------------|----------|---------|
| O-01 | Format | The exact binary layout of the P8 framed envelope (`type_tag \|\| canonicalization_version \|\| payload_length \|\| payload`) | The four-field frame, order fixed; widths and endianness unstated. Now waits on O-79: A7 §A7.9 makes the encoding map a precondition, and until it is settled the layout stays open and no signed-frame golden vector is final | Band 1 spec plus golden vectors, after the O-79 encoding map | pre-freeze | docs/phase-0-prereg-amendment-1.md:255-264; docs/band-1-docket.md:37-40 (item 5); formal/BAND0-EXIT.md:63 (E3); A7 §A7.9 |
| O-02 | Format | Whether schema validation rejects raw JSON numerics outside IEEE 754 exact range at ingestion, before canonicalization | Non-double values string-encoded, enforcement point unassigned | Band 1 ingestion spec and conformance vectors | none | docs/band-1-docket.md:32-36 (item 4) |
| O-03 | Format | Where and how the algorithm identifier is encoded | "A mandatory canonical-payload field is the current implementation candidate because it preserves P8's four-field frame" | P8 framing proof and golden vectors | Band 0 exit | docs/phase-0-prereg-amendment-3.md:491-493, 499-502, 878-885 |
| O-04 | Format | The construction that binds an authority statement to the signed object | Left open among "a separately hashed manifest core, an exact authorized tuple, or another construction" | Post-spike mechanism selection, then amendment | none | docs/phase-0-prereg-amendment-3.md:186-207, 878-885 |
| O-05 | Format | Multi-signer framing: (a) common attested content in separate signer-specific frames, or (b) one shared frame with key binding moved into the manifest | (a), registered on a stated reading of the author's words, "stated so it can be corrected" | Author correction or amendment; withdrawal of the S-P2 addendum if (b) | none | docs/phase-0-prereg-amendment-5.md:166-182 |
| O-06 | Format | The record format for a degraded verdict (per waived check: authorizing policy plus the verifier's observation, at least six values) | Six observation values named: absent, unperformable, invalid, anchor-late, names-other-key, would-pass | H1a obligation on the docket | H1a | docs/phase-0-prereg-amendment-5.md:143-155; docs/band-1-docket.md:62-66 (item 28) |
| O-07 | Format | The commitment construction for the refusal commitment value | Only the resistance property and the non-claims registered; no construction named | Amendment or Band 1 spec | none | docs/phase-0-prereg-amendment-3.md:648-653 |
| O-08 | Format | A declared per-bundle byte budget for embedded specifications, and the content-addressed reference above it | None | Band 1 spec | none | docs/band-1-docket.md:54-56 (item 9) |
| O-09 | Format | Whether the k-header SPV segment is embedded in `authority_evidence` so the verifier needs no header database | None | Band 1 spec | none | docs/band-1-docket.md:41-43 (item 6) |
| O-10 | Format | Registration of the forward-link / predeclared successor slot; the mechanism may still be substituted | Location RULED 2026-09-04: inside the canonical payload under P3's obligations, P8's four-field frame unchanged; an independent identifier, not a back-hash | Registration including the 07-19 four-mechanism comparison; a slot-bearing golden vector | pre-freeze | docs/band-1-docket.md:355-383 (item 25); formal/spike/standing-probe/DECISION.md sub-ruling 4 |
| O-11 | Format | A registered statement that third-party logs are an intended consumer, so the freeze preserves the fields a log builder needs | Correction of the same day: "no field is known to be missing"; item 27 is a preservation constraint, not an addition | Registration before format freeze | pre-freeze | docs/band-1-docket.md:483-516 (item 27) |
| O-12 | Format | The post-quantum algorithm | None chosen; "it will be a *different* key algorithm, a real architectural choice encoded per-receipt"; the PQ implementation "gates the production version" | Later amendment or deployment profile | none | docs/phase-0-prereg.md:339-345; docs/phase-0-prereg-amendment-3.md:477-480 |
| O-13 | Format | Hybrid classical+PQ dual signing | "explicitly deferred to a deployment profile or later amendment" | Deployment profile or later amendment | none | docs/phase-0-prereg-amendment-3.md:480-483 |
| O-79 | Format | The encoding map joining P8's four-field signed frame to A5 §A5.4's seven signer-specific bindings: where each binding lives in bytes (envelope field, inside the canonical payload under P3's obligations, or in the manifest tuple the frame commits to by hash), and the separation of the requester's content from the signer-specific metadata so that "payload equal across signer slots" is a statement about bytes | Both texts stand; neither field count alone answers the question. No map exists | The map, on the band-1 docket as item 33, then the frame layout and its golden vectors (O-01) | pre-freeze | A7 §A7.9 [RULED (author) 2026-09-14, PROPOSED]; docs/band-1-docket.md:76-88 (item 33); docs/phase-0-prereg-amendment-1.md:255-264; docs/phase-0-prereg-amendment-5.md:178-190 |
| O-14 | Issuance | The execution model for invoking the firewalled local GPG signer during automated issuance, and the attempt-loop behaviour when it is unreachable | None; the record requires only that "a transient partition must not manufacture a false `REFUSED` terminal state" | Band 1 spec | none | docs/band-1-docket.md:11-17 (item 1) |
| O-15 | Issuance | A declared maximum delivery/publication latency T with `DELIVERY_EXPIRED`/`PUBLICATION_EXPIRED`, and the precomputed-commitment variant | None | Amendment (both touch A3.7.2's registered decomposition) | none | docs/band-1-docket.md:18-24 (item 2) |
| O-16 | Issuance | OTS fee-bumping and aggregator-delay behaviour relative to S | S = 24h adopted working default; revision by A2.1's own terms | Band 1 spec | none | docs/band-1-docket.md:25-28 (item 3) |
| O-67 | Issuance | Whether an SLA-style hard bound on backward lag enters the record | None. "If operational evidence later supports an SLA-style hard bound, it may enter a **deployment profile** with monitoring and an explicit violation outcome — never this pre-registration's assumption set." The opportunity guarantee "buys is opportunity, not outcome" | Deployment profile, on operational evidence | none | docs/phase-0-prereg-amendment-2.md:139-143 |
| O-17 | Issuance | Closure of the A2 residue: two verifiable receipts for the same content with different declared times | Not closed; two named candidates, neither chosen: a lineage/equivocation-evidence mechanism, or an explicit dedup rule. A3 §A3.7.1's standing invariant is registered as "replac[ing] the docketed lineage-vs-dedup fork" | Amendment | none | docs/phase-0-prereg-amendment-2.md:60-69, 375-377; docs/phase-0-prereg-amendment-3.md:878-885 |
| O-18 | Issuance | Durability, retrievability, reporting surface and handoff mechanism of the refusal record | "The handoff mechanism remains open"; "Observer roles are registered here; the reporting surface is not frozen" | Amendment 3 discharge / Band 1 spec | none | docs/phase-0-prereg-amendment-2.md:290-292; docs/phase-0-prereg-amendment-3.md:596-597, 614-617 |
| O-19 | Issuance | Issuer signing-key lifetime and rotation policy: maximum validity window, rotation cadence, verifier behaviour at the boundary | None registered anywhere. Two candidate rules stated and objected to in the same entry (replacement only inside a declared pre-expiry band; staggered non-overlapping expiry bands across authority channels) | Registration before format freeze if the window affects bundle fields; otherwise Band 1 policy | pre-freeze (conditional) | docs/band-1-docket.md:385-481 (item 26) |
| O-20 | Issuance | Binding-form lifecycle and the reference-verifier obligation (three-state lifecycle, issuance-time registry epoch, append-only verifier support, CI gating, the δ-width rollback residual) | **DEFERRED 2026-08-13 by author ruling**: "plan retained, nothing implemented"; inert until a second binding form becomes issuable | Author ruling to activate; then amendment | none | docs/band-1-docket.md:220-243 (item 18); formal/spike/first-link/DECISION.md:436-461, 946-950 |
| O-21 | Issuance | Whether the "authorized tuple" is a distinct mechanism or the selected family under another name | DEFERRED, not rejected; "classified non-blocking for signature" | Candidate definitions at sufficient precision, then a naming correction or a mechanism decision | none | formal/spike/first-link/DECISION.md:857-871, 957-959 |
| O-22 | Verification | Full specification of header authentication: proof-of-work validity, cumulative-work or checkpoint anchoring, store identity pinned in declared verifier policy, bundle/store conflict rules; and whether absence of a pin is an explicit `UNVERIFIABLE` case | Deferred to the A2.2 evidence obligation's discharge | Registration before build (touches registered verdict semantics) | none | docs/phase-0-prereg-amendment-2.md:201-206, 236-244; docs/band-1-docket.md:44-49 (item 7) |
| O-68 | Verification | The P3 verification profile: exact library and version, accepted signature encodings, public-key validation behaviour, low-order-point handling, cofactor equation variant, and negative test vectors for each | None specified; the profile is the **[assumption]** half of P3's split discharge, "named in Layer 2 and discharged as H1a evidence". P3 reaches `discharged` on its [model] half with the [assumption] half named open | H1a evidence recorded in the repository | H1a | docs/phase-0-prereg-amendment-1.md:137-149, 584; formal/BAND0-EXIT.md:83 |
| O-23 | Verification | The historical trust-anchor store as a versioned standalone object, decoupled from the verifier binary | An archived historical trust-anchor store ships with the verifier (A1.5) | Band 1 spec | none | docs/band-1-docket.md:50-53 (item 8) |
| O-24 | Verification | Whether the embedded verification specification is executable-in-principle (formal fragment or pure-function reference implementation) rather than prose plus vectors | Prose plus vectors | "may warrant registration rather than quiet build-phase adoption" | none | docs/band-1-docket.md:57-61 (item 10) |
| O-25 | Verification | Renderer conformance vectors and the mechanical CI check that fails malformed renderings | None | Band 1 spec | none | docs/band-1-docket.md:78-81 (item 11) |
| O-26 | Verification | Whether Tessera-controlled surfaces may emit only the attested report when a result will be relayed | None | Policy decision; "register if adopted" | none | docs/band-1-docket.md:82-85 (item 12) |
| O-27 | Verification | The three verifier checks pending their symbolic legs (multi-signer common content; the wrapper's recorded inner canonicalization version; the standing path's tuple pin) | Registered as invariants; H1a reference-verifier obligations "entered once their symbolic legs run" | H1a obligation on the docket | H1a | docs/band-1-docket.md:67-74 (item 29); docs/phase-0-prereg-amendment-5.md §A5.4-§A5.6 |
| O-28 | Verification | The P9 conformance vector's cases (expected verdict from bundle and policy; same bundle twice on one machine; optional service reachable and contradicting the bundle) | None | H1a obligation on the docket | H1a | docs/band-1-docket.md:86-91 (item 30); docs/phase-0-prereg-amendment-5.md §A5.1 |
| O-29 | Verification | The P7 verdict-independence vector under each of the four P4 verdict values, with a re-serializing wrapper as red bar | None | H1a obligation on the docket | H1a | docs/band-1-docket.md:93-96 (item 32); docs/phase-0-prereg-amendment-6.md:48-53 |
| O-30 | Verification | Verdict composition along a renewal chain: (a) a chain as the A3.2 item 4 per-layer case extended in time, (b) what one `UNVERIFIABLE` link means for links beneath it, (c) where standing sits on a chain | Not registered. Honest candidate rule named for (b): "report per link, never propagate as `INVALID`, and state which links the verifier could reach from its trust root" | Author disposition; "nothing here is adopted" | none | docs/band-1-docket.md:245-267 (item 19) |
| O-31 | Verification | A registered sentence that renewal is always cumulative and simple timestamp renewal is excluded | The cumulative form is already built by original §4; the exclusion is unstated | "One registered sentence; no mechanism change" | none | docs/band-1-docket.md:269-282 (item 20) |
| O-32 | Verification | A completeness rule for wrapper lineage: a wrap commits to the full known lineage of prior wrappers | "Not registered anywhere"; wrapper-level equivocation to be named with the standing decision's G4 treatment, never as a closure | Amendment | none | docs/band-1-docket.md:284-292 (item 21) |
| O-33 | Verification | A registered statement that each epoch's wrapper is independent testimony only through its own contemporaneous anchor | Unstated; "One sentence, near A3.4 claim 3" | Amendment | none | docs/band-1-docket.md:294-302 (item 22) |
| O-34 | Verification | Per-prior verdict snapshots inside the renewal wrapper | **Registered AGAINST**: original §4 rules the renewal wrapper out for that role; the role exists as A3.8's optional signed verification report. "Disposition: no change to the record" | None; entry is a correction to the conversation | none | docs/band-1-docket.md:304-319 (item 23) |
| O-69 | Verification | The authority-channel count is n-ary as ruled, but every model, ledger entry and evidence-set rule in the record is written at n = 2; no rule states how the strict "all external evidences" requirement, the waiver lattice, or the "never all" enumeration behave for n > 2 | The n = 2 instance throughout | Registration of the n-ary rules, or an amendment | none | docs/band-1-docket.md:465-468 (RULED (author) 2026-09-06, inside item 26, whose heading reads candidate); docs/phase-0-prereg-amendment-1.md:283-297, 344-346 |
| O-70 | Verification | Package completeness and self-containment: whether the inner manifest, authority evidence and possession proof must travel inside the bundle as P7 requires of the inner bytes | Presenter-supplied in every S-P7 model; no query states package completeness | Band 1 spec; a P8/H1a format obligation | none | formal/COVERAGE-MAP.md:55 and amendment note 1; formal/suite/s-p7/proverif/sp7_q2_degraded_compromised.pv:316-318; formal/suite/s-p7/RESULTS.md:646-654 |
| O-72 | Verification | Whether the log-versus-verdict boundary enters registered text: that a service-side enumeration or observability API may feed a log and never a verdict, a log being a correlated subject and not a verifier input | Stated as a clerk's reading only, PROPOSED, with no tool leg | Registration, or an author ruling recorded as one | none | formal/COVERAGE-MAP.md row 14; docs/band-1-docket.md:520-530 |
| O-73 | Verification | Whether the registered binding-form required-set rule gets a model or symbolic leg: no suite family carries a required-set-of-forms input, and the form lifecycle that would exercise it is deferred with nothing implemented | None; the ruling stands registered and unmodelled | A model or an H1a vector; item 18's activation for the lifecycle half | none | formal/spike/first-link/DECISION.md:366-405, :436-461 |
| O-78 | Verification | A canonicalization version the verifier recognizes but does not implement: no registered verdict. The registered P8 rejection list names only "unknown canonicalization versions" (V1); the recognized-but-unimplemented case is neither equated to it nor given a transition of its own | None | Amendment, or an author ruling recorded as one | none | docs/phase-0-prereg-amendment-1.md:267-273 |
| O-36 | Standing | Whether an issuer holding two identities on one key keeps one terminal lineage record or two | Expressly not decided; "a single TLR under that key may still name cores from both" | Amendment | none | docs/phase-0-prereg-amendment-5.md:212-219; formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:78 |
| O-74 | Standing | Whether the standing path's `if kT = kX` check, that the TLR key equals the presented key, is a conformance requirement | "a fixture-shape restriction no registered text requires"; whether it is a conformance requirement is unstated | Registration or an author ruling | none | formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:51-52, :337-338 |
| O-75 | Standing | Where `STANDING_EVIDENCE_MISMATCH` and `STANDING_EVIDENCE_SIGNATURE_INVALID` are registered; they have no registered home comparable to SC-3's registration of the other two codes | Emitted by the modelled verifier and recorded in the probe; registered nowhere | Amendment, on the SC-3 pattern | none | formal/spike/standing-probe/DECISION.md:61-71, :119; formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:144-155 |
| O-76 | Standing | Standing behaviour for lineages of other than two attempts, which is neither modelled nor registered | None; the modelled lineage is exactly two entries (`lineage2`) and does not generalize | Band 1 spec, or a model recut | none | formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:130-136; formal/suite/s-standing/RESULTS.md:540-556 |
| O-77 | Standing | The TLR anchor's temporal validity (SC-1), a cross-formalism consumed obligation owed to the bridge and one that "must never be marked discharged" by the symbolic standing family | Carried and inert in S-STANDING; nothing temporal is represented there | The capstone join against the P5c/P5/P6 bridge | none | formal/suite/s-standing/RESULTS.md:484-536; formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:22-47 |
| O-37 | Survivability-custody | Exact custodial trigger expressions, cadence, clock, monitoring surface, and succession mechanism | Design obligations; "They receive their own trust assumptions and do not reuse δ, ε, or k" | Amendment or Band 1 spec | none | docs/phase-0-prereg-amendment-3.md:419-423, 878-885 |
| O-38 | Survivability-custody | Observable deadlines on `ACTION_DUE`/`FAILED` and an explicit visibility boundary | None | Band 1 spec | none | docs/band-1-docket.md:117-120 (item 13) |
| O-39 | Survivability-custody | Whether the renewal window is itself attested and visible in the tending record | None | Band 1 spec | none | docs/band-1-docket.md:121-123 (item 14) |
| O-40 | Survivability-custody | A minimal tending-policy skeleton for the demonstration | None; the docket notes that requiring it at Band 0 exit "is a registration change" and `BAND0-EXIT.md` §3 excludes it | Author decision; registration change if required at exit | none | docs/band-1-docket.md:124-128 (item 15); formal/BAND0-EXIT.md:84 |
| O-41 | Survivability-custody | The dead-project demonstration that an old bundle's `VALID_STRICT` is unaffected when custodial records are unavailable | None | Band 1 spec | none | docs/band-1-docket.md:129-132 (item 16) |
| O-42 | Survivability-custody | Custody of externally-referenced verification inputs: what must remain obtainable, who retains it, how a verifier discovers it, how retrieval is tested; and the unselected A/B fork (bundle carries its own authenticated registry entry, versus the self-contained tier not judging issuance-time binding-form validity) | Neither branch selected. Scope reduced 2026-08-13 by item 18's deferral: "Only subject (a) is live". Constraints already implied: not "Tessera, in perpetuity"; discovery on intrinsic identity; retrieval failure yields `UNVERIFIABLE` with a distinguishing reason code | Answer required before any Band 1 freeze | pre-freeze | docs/band-1-docket.md:133-218 (item 17) |
| O-43 | Survivability-custody | Whether correlated-versus-uncorrelated custody enters the decision criteria, and what anchoring standing evidence buys | Citable "as an interpretation of C2 as registered"; explicitly "**not** entered into the criteria, which are frozen at `74ee46e`" | Criteria amendment if it is to be entered | none | docs/band-1-docket.md:321-353 (item 24) |
| O-44 | Parameters | Ratification or revision of δ, ε, k, N, S at Band 0 exit | Working defaults δ = 72h, ε = 24h, k = 6, N = 3, S = 24h; N's budget is "a nominal budget, not a proven wall-clock bound" | "one dated ruling in an amendment or the exit commit's record" (author act) | Band 0 exit | docs/phase-0-prereg-amendment-1.md:180-190, 492-499; docs/phase-0-prereg-amendment-2.md:110-113, 208-214, 270-274, 372-375; formal/PROPERTIES.md:167-168; formal/BAND0-EXIT.md:74 (E14) |
| O-45 | Parameters | The numeric review-staleness threshold | None; §4.7 and the §5 done-line require staleness "past a declared threshold" and no value is given | Amendment or Band 1 spec | none | docs/phase-0-prereg.md:564-572, 595-598 |
| O-46 | Parameters | The per-query symbolic timebox value | Declared per query before running, with three named outcomes; the value itself "not frozen here" | Per-query declaration in each family's PREDICTIONS.md | none | docs/phase-0-prereg-amendment-3.md:245-248 |
| O-47 | Parameters | The custodial cadence value | RULED: "The cadence parameter lives in each custodial policy or profile, not as one universal constant"; Band 0 ratifies only the parameter schema and clock-role invariants | Per-policy declaration; schema ratified at Band 0 | Band 0 exit (schema only) | docs/phase-0-prereg-amendment-3.md:447-452 |
| O-48 | Parameters | The bounded retention horizon and the minimization/retention policy for refusal records | Declared per deployment; no value fixed | Deployment profile | none | docs/phase-0-prereg-amendment-3.md:583-592, 645-646, 814-817 |
| O-49 | Process-exit | A quantitative forgery-cost analysis of the combined construction | Qualitative argument only; "not yet done", deferred and funded by a future customer | Future work, gated on revenue | none | docs/phase-0-prereg.md:406-411 |
| O-50 | Process-exit | Higher-assurance signing: enclave/secure-sandbox signing and a hardware token for the local GPG layer | "considered, deferred"; gated on "real reliance". `BAND0-EXIT.md` §3 lists it as not on the exit list | Later decision on reliance | none | docs/phase-0-prereg.md:454-479; formal/BAND0-EXIT.md:85 |
| O-51 | Process-exit | Tamarin versus ProVerif (fixed by a bounded spike before theorem-proving), and the form of the P8 discharge: "Lean4 if warranted, rigorous prose proof plus the golden-vector and rejection suites if that is honest sufficiency" | ProVerif in use across the suite; the P8 form is undecided and routed | Criteria-before-evidence decision on the proof's form, DECISION.md pattern, routed to the author (E3a) | Band 0 exit | docs/phase-0-prereg-amendment-1.md:369-386; formal/BAND0-EXIT.md:63, 117 |
| O-52 | Process-exit | Whether semantic re-attestation exists at all, and at what interface and price | Named as "a separate, priced business offering" that "*may not be available years later*"; no interface or obligation registered | Business decision; out of the base service | none | docs/phase-0-prereg.md:364-369 |
| O-53 | Process-exit | Independent human formal-methods review, and independent adjudication of reviewer counterexamples | Not a resolution requirement; "an optional enhancement gated on a revenue stream, and its absence is a declared residual risk" | Gated on revenue | none | docs/phase-0-prereg.md:723-728; docs/phase-0-prereg-amendment-1.md:556-561 |
| O-54 | Process-exit | The capstone transcription tactic | "a non-binding implementation candidate, subject to the spike" | Spike evidence, then the capstone build (E5) | Band 0 exit | docs/phase-0-prereg-amendment-3.md:248-249, 878-880 |
| O-55 | Process-exit | Whether the optional non-discharging TLA+ probe of two-layer verdict composition is built | Optional, on A4.1's terms; "a green result is not evidence and is cited by no tracker row"; a red or unrepresentable finding "is dispositioned before exit" | Collaborator schedule; disposition before exit if red | Band 0 exit (conditional) | docs/phase-0-prereg-amendment-6.md:53-57 |
| O-56 | Process-exit | Whether P7 moves `checked` to `discharged` | `checked` on Amendment 6's signature; "`discharged` waits on the author's read of the two cross-family reviews" | Author read (E9) | Band 0 exit | docs/phase-0-prereg-amendment-6.md:59-65 |
| O-57 | Process-exit | Ratification of the suite enumeration | "ADOPTED (author), provisionally"; the enumeration is "the suite's *working scope*"; "Nothing in §1–§6 is ratified by this entry" | Ratification after the S-P3 draft and the author's cold read | none | formal/suite/ENUMERATION.md:393-402 |
| O-58 | Process-exit | Panel criterion 4's second condition: a standing model in this suite under the A1.3 adversary before Band 0 exit | Condition 1 (author selection) satisfied; condition 2 open; SC row `open` on the tracker | Owner assessment proposing `checked`, then E9 | Band 0 exit | formal/suite/ENUMERATION.md:511-513; formal/PROPERTIES.md:256; formal/BAND0-EXIT.md:62 (E2) |
| O-59 | Process-exit | Whether SC-1 needs its own TLA+ instance (B8) | "an open cell in the coverage map (row 13), decided when the capstone's ledger is written; it does not gate the S-STANDING freeze" | Capstone ledger | none | formal/suite/ROUTED-2026-09-06.md:154-157, 205 |
| O-61 | Process-exit | The implementation specification (this document) as a Band 0 exit companion | "Sequenced as a Band 0 exit companion, not a Band 1 item"; collaborator-proposed, not registered | Docket item 31 / E16 | Band 0 exit | docs/band-1-docket.md:98-113 (item 31); formal/BAND0-EXIT.md:76 (E16) |
| O-62 | Process-exit | *Reading to veto (a)*: whether `discharged`, not `checked`, is the exit status for every tracker row | The clerk reads §8 clause 2 plus A4.4 as requiring `discharged` for every row including SC and the two E6 rows. "If the author reads §8 as satisfied by `checked` plus one aggregate read, E9 shrinks to one sitting and this reading is withdrawn" | Author veto or acceptance at exit | Band 0 exit | formal/BAND0-EXIT.md:96 |
| O-63 | Process-exit | *Reading to veto (b)*: whether vectors are specified and reviewed at Band 0 and run at H1a | The clerk reads A1 §A1.2 P8 and A3 §A3.6.1 together as putting the proof and the layout-fixing vectors at exit and execution against code at H1a; the A1.7 model-derived vectors follow the same split | Author veto or acceptance at exit | Band 0 exit | formal/BAND0-EXIT.md:97 |
| O-64 | Process-exit | *Reading to veto (c)*: whether "offered, not entered" ledger entries satisfy A3.3 | The clerk reads them as not satisfying it: "an offered entry is not ledgered". Entering them is the first capstone step (E5a) | Author veto or acceptance at exit | Band 0 exit | formal/BAND0-EXIT.md:98 |
| O-65 | Process-exit | *Reading to veto (d)*: whether A4.4 subsumed A1.4's TLA+ to symbolic correspondence-mapping sentence | The clerk reads amend-don't-rewrite as keeping the A1.4 sentence, so E8 stays on the list. "If the author rules that A4.4 subsumed it, E8 is withdrawn" | Author veto or acceptance at exit | Band 0 exit | formal/BAND0-EXIT.md:99 |
| O-66 | Process-exit | *Reading to veto (e)*: whether the relying-party story is one page published stand-alone as well as written inside the specification | The clerk reads A3 §A3.1.4's "one page" as requiring both: "the specification is not a substitute for the registered artifact" | Author veto or acceptance at exit | Band 0 exit | formal/BAND0-EXIT.md:100 |
| O-71 | Process-exit | Two registered Band 0 model obligations are unmodelled: the unknown-algorithm P4-partition transition with its fail-open companion, and the extended atomic-entry refusal invariant with its two companions | None; both tracker rows read `open` with no artifact | E6 on the Band 0 exit list | Band 0 exit | formal/PROPERTIES.md:47-48, :260; docs/phase-0-prereg-amendment-3.md:509-512, 814-831 |

---

## 12. Contradictions routed to the author

Twenty-seven conflicts: eleven ruled by the author on 2026-09-14 (instrument
Amendment 7, PROPOSED), sixteen already settled by later text, **none open**.
Numbering is stable: C-09 was moved to the settled table
as S-13 at assembly, and C-01, C-02 and C-14 as S-14 to S-16 the same day (each answered by a later signed text or by the tree); the eleven that stood open, C-03 to C-08 and C-10 to C-15, were ruled on 2026-09-14 and moved to the ruled subsection below, C-15 having been entered at the 2026-09-13 assembly. One entry per conflict between two passages of the record that a
reader must resolve before implementing. Both cited passages were opened and verified before
the entry was written. No entry states which side should win on this document's
authority; the ruled entries record the author's ruling and the instrument that
carries it.

### Open, author ruling needed

*No entry remains open as of 2026-09-14: the eleven entries that stood here (C-03 to C-08, C-10 to C-13, C-15) were ruled by the author on 2026-09-14 and are recorded in the subsection below; C-09 was settled at assembly as S-13 and C-01, C-02 and C-14 as S-14 to S-16 on 2026-09-13. IDs are not reused.*

### Ruled 2026-09-14, instrument Amendment 7 (PROPOSED)

Eleven entries, one per conflict, answered by the author on 2026-09-14 in one
message. The instrument is `docs/phase-0-prereg-amendment-7.md`, which quotes
him verbatim and instruments each ruling; it is PROPOSED and becomes in force on
his first commit containing it. Each entry keeps its two passages and its
implementer note unchanged, and gains the ruling, the instrument section, and —
where A7 marks a word it read against its typing — the reading marked for
correction. Nothing here resolves a contradiction on this document’s own
authority: the ruling is the author’s and the instrumentation is A7’s.

#### C-03 Is the length bound inside the canonical bytes or in the frame around them
- **A**: "Length is bound into the canonical bytes (not a side field), so the encoding is **boundary-unambiguous** by construction". `docs/phase-0-prereg.md:492-494`
- **B**: "JCS (RFC 8785) itself carries no length header, so the frame supplies it: signatures and anchors commit to a **framed envelope** — `type_tag || canonicalization_version || payload_length || payload` — where `payload` is the JCS bytes." `docs/phase-0-prereg-amendment-1.md:255-262`
- **Implementer**: under A the length is inside `canonical(payload)`; under B it is an envelope field outside the JCS bytes. The two documents use "canonical bytes" for different byte strings, which changes what a golden vector fixes and what a signature covers.
- **Status**: RULED (author) 2026-09-14 — instrument Amendment 7 §A7.1 (PROPOSED; in force on the author’s commit).
- **Ruling**: "I think it would be useful to clearly separate canonical payload bytes from the signed frame."
- **Instrument**: Two byte strings, fixed: the canonical payload bytes are `canonical(payload)` under the original §4.3 precision rule; the signed frame is A1 P8’s `type_tag || canonicalization_version || payload_length || payload`, whose fourth field is the canonical payload bytes. Signatures and anchors commit to the signed frame; the length is a frame field. The original §4.3 sentence is superseded by A1 P8 and is not edited. Golden vectors are owed for both strings separately. Carried to §3.1, §3.2, §9.1.
- **Governs**: Bundle format (P8 frame); canonicalization

#### C-04 May the issuer-key manifest carry references rather than keys
- **A**: "the bundle carries an **issuer-key manifest**: the issuer public keys (or references) plus *timestamped evidence*". `docs/phase-0-prereg.md:530-531`
- **B**: P9: "The verdict is a pure function of the bundle and the verifier's declared policy — no service-side state, no live network dependency, appears in the decision." A1.5 requires both external evidences "*archived in the bundle*", "never live repository availability — P9". `docs/phase-0-prereg-amendment-1.md:278-281, 430-438`
- **Implementer**: under A a manifest may name a key by reference; under B any reference that must be dereferenced at verification time breaks P9. A1 never withdraws "or references".
- **Status**: RULED (author) 2026-09-14 — instrument Amendment 7 §A7.2 (PROPOSED; in force on the author’s commit).
- **Ruling**: "B. You should allow references to be resolved entirely from the bundle or from explicitly declared trusted inputs. Note that a reference shouldn’t require a network lookup (e.g., offline, albeit limitations are permissible.)"
- **Instrument**: "(or references)" stands: a reference is permitted when resolvable from inside the bundle or from an input the declared policy explicitly names as trusted (§2.3), never by a live lookup; unresolvable makes the needing check unperformable (`UNVERIFIABLE` for that required check). A1 §A1.5’s "archived in the bundle" for the two authority evidences is unchanged. Carried to R-3.31a, R-4.24, R-5.13.
- **Governs**: Bundle format (manifest); P9 statelessness

#### C-05 Is anchor lateness ever a waivable observation
- **A**: "Temporal-anchor consistency is already non-waivable (A1.2.1); the new conjunct is part of it. The P4 partition applies inside it: performed-and-failed → `INVALID`". `docs/phase-0-prereg-amendment-2.md:245-248`
- **B**: `anchor-late` is one of the six observation values recorded for a waived check whose condition never determines the verdict; A5.2's fork lists "late anchor" among failures a waived channel evidence may exhibit while `VALID_DEGRADED` stands. `docs/phase-0-prereg-amendment-5.md:96-100, 145-150`
- **Implementer**: whether a late anchor forces `INVALID` or is recorded as an observation beside a standing `VALID_DEGRADED`. The two may be scoped to different objects (the receipt's own temporal anchor versus an authority evidence's anchor); neither registered text says so.
- **Status**: RULED (author) 2026-09-14 — instrument Amendment 7 §A7.3 (PROPOSED; in force on the author’s commit).
- **Ruling**: "I’d suggest making the object scope explicit: the receipt’s required temporal checks are still not non-waivable. This still permits a waived redundant authority to carry a late-anchor observation. I wouldn’t permit any waiver to eliminate the final complete chain."
- **Reading confirmed by the author 2026-09-14** (was marked for correction): A7 §A7.3 reads the author’s "still not non-waivable" as **"still non-waivable"**, the reading his own third sentence, A2 §A2.2 and A3 §A3.2’s linked floor all require; if he meant the words as typed, §A7.3 is withdrawn and this item returns to open.
- **Instrument**: A2 §A2.2’s three conjuncts apply to the receipt’s own shipped anchor and are non-waivable: a late receipt anchor is `INVALID`. A5 §A5.3’s `anchor-late` is an observation against a waived redundant authority evidence’s own anchor and never determines the verdict. No waiver removes the final complete chain. Carried to R-2.31a, R-5.40, §9.2.
- **Governs**: Verifier waiver lattice (A1.2.1, P4 partition)

#### C-06 Prohibiting declared-time ordering versus not deciding for the adjudicator
- **A**: "**No verifier policy, and no downstream marketplace rule, may order competing receipts by declared time** (first-to-file semantics)"; enforced by policy. `docs/phase-0-prereg-amendment-2.md:327-329`
- **B**: "Tessera does not decide whether the adjudicator should trust the attestation and must not try to"; the adjudicator "decides trust using the verdict and anything else available". `docs/phase-0-prereg-amendment-4.md:165-168, 178-182`
- **Implementer**: under A the implementation must refuse to serve, or must forbid, declared-time ordering by relying parties; under B it must not constrain the adjudicator at all. A4 is later and general; A2.4 is earlier and specific; neither cites the other.
- **Status**: RULED (author) 2026-09-14 — instrument Amendment 7 §A7.4 (PROPOSED; in force on the author’s commit).
- **Ruling**: "Tesser should not present declared time as proof of first-to-file priority. Rather, this is a decision that an adjudicator could use in their own reasoning - not because Tessera provides any claims. This limitation is not a service-refusal requirement."
- **Instrument**: A2 §A2.4’s commitment binds Tessera’s own surfaces, policies and claims; adjudicators reason for themselves; it is not a service-refusal requirement. A7 records the narrowing of the rule’s bearer as a change on the record. Carried to R-1.10a, R-4.78, R-5.62.
- **Governs**: Adjudicator boundary; verifier policy scope

#### C-07 `UNVERIFIABLE` "for exactly one case" versus its other registered assignments
- **A**: "**The verdict boundary (adopted, exact):** `UNVERIFIABLE` for exactly one case — a well-formed, correctly bound, but unsupported algorithm identifier." `docs/phase-0-prereg-amendment-3.md:503-505`
- **B**: "If every external authority evidence for a layer is unavailable, unsupported, or otherwise unperformable, the layer's verdict is `UNVERIFIABLE`" (`:146-149`); an issuance-profile dependency's unavailable interpretation is exposed "as `UNVERIFIABLE` for the affected check" (`:353-356`); the standing dimension reports `UNVERIFIABLE` as one of its values (`:541-546`).
- **Implementer**: whether the verifier's `UNVERIFIABLE` production points number one or four. **Corrected 2026-09-14 (A7 §A7.5; the non-author reviewer found the original sentence logically mistaken).** Scoping A to algorithm-identifier handling does *not* leave `:146-149` and `:353-356` in conflict with it: they are independent unperformable checks, each yielding `UNVERIFIABLE` in its own right under P4 and A4 §A4.2, and A’s bound is on one check’s outcomes, not on the verifier’s count of `UNVERIFIABLE` production points. The standing dimension’s value is not a P4 verdict at all (A itself says standing is "an **orthogonal assessment dimension**, not a fifth P4 state").
- **Status**: RULED (author) 2026-09-14 — instrument Amendment 7 §A7.5 (PROPOSED; in force on the author’s commit).
- **Ruling**: "You should scope ‘exactly one case’ to handling of the algorithm-identifier. This allows other required checks to be unperformable independently. The standing is still a separate assessment."
- **Instrument**: A3 §A3.6.2 item 2’s "exactly one case" bounds the algorithm-identifier check’s outcomes only; every other required check yields `UNVERIFIABLE` independently under P4 and A4 §A4.2, and the standing dimension’s `UNVERIFIABLE` is the orthogonal assessment’s value, not a P4 verdict. Carried to V14, §5.3, R-7.7a, R-7.38.
- **Governs**: Verifier verdict vocabulary (P4)

#### C-08 What the issuer evaluates at ship
- **A**: The panel-driven repair, quoted with the source's own inner quotation marks: "An earlier form of this repair said the issuer evaluates "the full `VALID_STRICT` predicate" at ship. That overstates the model and the obligation ... the issuer does not re-run envelope verification (P1–P3) at ship." `docs/phase-0-prereg-amendment-3.md:665-673`
- **B**: The §A3.9 obligations summary: "A2.1 prose repair (issuer ships on full `VALID_STRICT`)." `docs/phase-0-prereg-amendment-3.md:832`
- **Implementer**: whether the ship guard is the three-conjunct temporal predicate plus burial depth, or the full envelope verification. B is the unrepaired wording A exists to correct, and both stand in the same amendment.
- **Status**: RULED (author) 2026-09-14 — instrument Amendment 7 §A7.6 (PROPOSED; in force on the author’s commit).
- **Ruling**: "A. The summary appears to be stale. Can you ensure explicit repair governs, so that three temporal conjuncts plus burial death are what matters."
- **Reading confirmed by the author 2026-09-14** (was marked for correction): A7 §A7.6 reads the author’s "burial death" as **"burial depth"**, the `DepthK` conjunct of the bridge’s `Ship` guard.
- **Instrument**: A3 §A3.7.3’s panel-driven repair governs: the issuer ships on the three temporal conjuncts plus burial depth `DepthK = k − 1` and does not re-run envelope verification (P1–P3) at ship. The §A3.9 summary line is the unrepaired wording and is superseded, not edited. Carried to R-2.3, R-4.36, R-4.77a, §4.10.
- **Governs**: Issuance ship predicate (A2.1)

#### C-10 Two vocabularies for the standing report
- **A**: The registered S-series table's "Standing verdict" column is "**standing**" / "**no standing**", with reason codes `TERMINAL_DISPOSITION_SHOWN`, `SUPERSEDED`, `NO_TERMINAL_DISPOSITION_EVIDENCE`, and (SC-3) `ISSUANCE_REFUSED`. `formal/spike/first-link/DECISION.md:797-801, 826`
- **B**: The same file's SC-3 additions and the standing probe's scoring state outcomes as `ESTABLISHED` / `ABSENT` / `UNVERIFIABLE`: malformed evidence "yields `UNVERIFIABLE` with this reason; it never yields `ESTABLISHED`"; a rejected transplant gives "`ABSENT`/`STANDING_EVIDENCE_MISMATCH`". `formal/spike/first-link/DECISION.md:838-847`; `formal/spike/standing-probe/DECISION.md:61-71, 116-129`. A3 registers the base result as "at least `ESTABLISHED`, `ABSENT`, or `UNVERIFIABLE`" (`docs/phase-0-prereg-amendment-3.md:541-546`).
- **Implementer**: the standing report schema. Whether "no standing" is `ABSENT`, or `UNVERIFIABLE`, or a separate boolean carrying a reason code. No document maps one vocabulary onto the other.
- **Status**: RULED (author) 2026-09-14 — instrument Amendment 7 §A7.7 (PROPOSED; in force on the author’s commit).
- **Ruling**: "B. It needs an explicit mapping of S1 to ESTABLISHED and S[2-4] to ABSENT. We need to retain the specific reasons. A malformed or temporally inconsistent standing evidence means it is UNVERIFIABLE (the existing rules)."
- **Instrument**: One value set — `ESTABLISHED` / `ABSENT` / `UNVERIFIABLE`, each with a reason code — with the S-series mapped onto it (S1 → `ESTABLISHED`; S2–S4 → `ABSENT`, reasons retained and pairwise distinct; malformed or temporally inconsistent standing evidence → `UNVERIFIABLE`). "standing" / "no standing" are the S-series’ names for the first two, not a third value. The two probe-observed codes stay unregistered (O-75). Carried to R-3.60a, R-5.52, R-6.35, §5.3.
- **Governs**: Standing report schema (verifier output)

#### C-11 Is key binding a cross-model ledger entry with a severing companion
- **A**: S-P3 ledger entry 1, key-binding relation: "Consumer: S-P1, S-P2, S-P7 (each presupposes whose bytes are whose) ... Severing companion: Q3 (frame unbound) → `Reattributed` red." `formal/suite/s-p3/RESULTS.md:203-216`
- **B**: S-P1 ledger entry 1: "Key binding — complementary to S-P3's ledger entry 1, not consumed ... **No severing companion fails an S-P1 query** ..., so this is not an A3.3 cross-model entry and none is claimed." `formal/suite/s-p1/RESULTS.md:330-345`
- **Implementer**: whether the capstone discharge matrix carries a producer-consumer row for key binding between S-P3 and S-P1 (with an expected red) or composes the two as independent axes. A3.3's gate text requires every ledgered cross-model assumption to be discharged by a producer query with a severing companion.
- **Status**: RULED (author) 2026-09-14 — instrument Amendment 7 §A7.10 (PROPOSED; in force on the author’s commit).
- **Ruling**: "B for S-P1. Authorship and key binding compose as complementary claims. We should not create a dependency if said dependency cannot falsify the claim of the consumer. Different consumers will need their own dependency analysis."
- **Instrument**: S-P1’s ledger entry 1 stands as written (complementary, not consumed, no cross-model entry claimed); S-P3’s ledger entry 1 is read as naming S-P1 a *related* family, not a consumer. The rule: a cross-model ledger entry exists only where severing the producer would falsify the consumer’s query. S-P2 and S-P7 make their own determination when their entries are entered (`formal/BAND0-EXIT.md` E5a). Recorded by an appended note in `formal/COVERAGE-MAP.md`. Carried to §5.5.
- **Record note carried from the open entry**: No later dated note in either family reconciles the two.
- **Governs**: Capstone discharge matrix (A3.3); process

#### C-12 Are `ot` and `cv` carried checks or bound-but-unexercised fields
- **A**: All eight S-P3 model headers: "identity, algorithm, object type, canonicalization version and domain tags are included in the signed bytes but unexercised by these two queries." `formal/suite/s-p3/proverif/sp3_q2_degraded_compromised.pv:53-55`
- **B**: The verifier-check tables label them inside a column of check statuses: "`ot`, `cv`: **CARRIED** unchecked (F7: object type → P7; canonicalization version → P8/H1a)" and "`=alg`, `=id`, `ot`, `cv`: **CARRIED**". `formal/suite/s-p3/READING-AIDS.md:177, 302`
- **Implementer**: whether a conforming verifier owes a check on `ot` and `cv` at this layer, or only carries the fields as obligations for P7 and P8/H1a. S-P3's own record calls B "a weaker version of the same conflation" and defers the fix: "nothing is edited here: this is deferred to S-P3's next recut ... Proposed by the AI collaborator; not adopted; the commit is the author's." `formal/suite/s-p3/RESULTS.md:346-367`
- **Status**: RULED (author) 2026-09-14 — instrument Amendment 7 §A7.10 (PROPOSED; in force on the author’s commit).
- **Ruling**: "Code description needs to be accurate: the fields are bound, they are not checks done by S-P3 and the obligation to validate is not here, it is somewhere else."
- **Instrument**: The model headers are accurate as they stand: `ot` and `cv` are bound in the signed bytes and are not checks at this layer, the validation obligations being P7’s (object type) and P8/H1a’s (canonicalization version). The two S-P3 reading-aid rows that list them inside a column of check statuses are corrected in place with a dated marker; no model is edited. Carried to V17.
- **Record note carried from the open entry**: the S-P3 recut fix was proposed and not adopted; A7 §A7.10 adopts it as a reading-aid correction only.
- **Governs**: Verifier check set at the P3 layer

#### C-13 Which k the P5c family checks
- **A**: Module header: "hence DepthK = k - 1 (strict default k = 6 => DepthK = 5)". `formal/tla/P5c_IssuanceProtocol.tla:26-29`
- **B**: The checked configurations use `DepthK = 2`, that is k = 3 (`formal/tla/P5c_IssuanceProtocol.cfg:15-19`), and the bridge states the quantity a third time as `KConf = 3`, `DepthK = 2`, with `PinAgreement` checking only `DepthK = KConf - 1` (`formal/tla/P5cP5P6_Bridge.cfg:1-14`). The tracker's unchecked box still reads "δ = 72h, ε = 24h, k = 6" (`formal/PROPERTIES.md:167-168`).
- **Implementer**: whether the checked evidence covers the registered strict default. The reading aid discloses this as item 20, Boundary: "`DepthK = 2` represents k = 3 ..., **not the registered strict default k = 6**" (`formal/tla/READING-AID-P5c.md:226-231`). No parameter-independence argument exists in the record.
- **Status**: RULED (author) 2026-09-14 — instrument Amendment 7 §A7.8 (PROPOSED; in force on the author’s commit).
- **Ruling**: "We should preserve the intended production parameter by using commission evidence at said parameter, or at a parameter-general argument. We should not change the default to match a small checked configuration."
- **Instrument**: The registered strict default k = 6 (`DepthK = 5`) is preserved; the checked `DepthK = 2` is evidence for the checked abstraction, not evidence at the registered parameter, and the default is not changed to match it. Band 0 exit item **E18** owes (a) a re-run at `DepthK = 5` with every registered witness still firing, or (b) a non-author-reviewed parameter-independence argument. Carried to R-8.9, §8, §10.1 E18, §4.10 row 12.
- **Record note carried from the open entry**: Interacts with O-44 (parameter ratification at exit).
- **Governs**: Parameters (k); scope of checked TLA+ evidence

#### C-15 Four fields in the frame, or the multi-signer frame's seven
- **A**: "signatures and anchors commit to a **framed envelope** — `type_tag || canonicalization_version || payload_length || payload` — where `payload` is the JCS bytes." `docs/phase-0-prereg-amendment-1.md:255-264`
- **B**: A5 §A5.4 describes every required signer's frame as carrying object type, algorithm, identity, manifest hash, canonicalization version, payload and key fingerprint, while stating that P3's field list and P8's frame are unchanged. `docs/phase-0-prereg-amendment-5.md:178-190`
- **Implementer**: how many fields the frame carries, and whether the six equal non-fingerprint fields sit inside P8's four-field envelope or beside it. O-05 asks a different question of the same passage: which of the two readings, (a) separate signer-specific frames or (b) one shared frame, was meant.
- **Status**: RULED (author) 2026-09-14 — instrument Amendment 7 §A7.9 (PROPOSED; in force on the author’s commit).
- **Ruling**: "We should preserve the concrete four-field envelope and the signer specific semantic bindings _if_ an explicit encoding map demonstrates both requirements. We should settle the map before format freeze because neither field count alone gives us an answer."
- **Instrument**: Both stand — P8’s four-field signed frame and A5 §A5.4’s seven signer-specific bindings — joined by an explicit **encoding map** saying where each binding lives in bytes, settled before format freeze (band-1 docket item 33, §10.2, §11 O-79). Until it is settled the frame layout stays open (O-01) and no signed-frame golden vector is final. Carried to R-3.12a.
- **Record note carried from the open entry**: Entered at the 2026-09-13 assembly, from the §3 draft's end list, which had no register entry.
- **Governs**: Bundle format (P8 frame); multi-signer framing

### Apparent contradictions already settled by later text

Each row is a conflict a reader will still meet in the tree, because the record
amends rather than rewrites. The settling text is a record fact, not a
resolution taken here.

| # | Conflict | Passage A | Passage B | Settled by |
|---|----------|-----------|-----------|------------|
| S-01 | Is Amendment 4 in force | "**Status: DRAFT — adopted in session, not yet signed.**" `docs/phase-0-prereg-amendment-4.md:6` | "**Amendment 4 (signed 2026-09-06, `5188e7a`)** moved P10 to `checked`" `formal/PROPERTIES.md:17-23`; contra "whether the stamp or the status line governs is the author's call" `formal/tla/P4_VerifierStates.tla:46-51`; `formal/spike/tla-probes/P9/RESULTS-PROBE.md:8-21` | SETTLED BY `docs/phase-0-prereg-amendment-5.md:48-56` (§A5.0, in force from `504e662`): "The author confirms it: `5188e7a` is Amendment 4's signing commit and Amendment 4 has been in force since." Every P4/P5P6 card citing §A4.2 or §A4.3 inherited this question |
| S-02 | Is Amendment 3 in force | "Amendment 3 — ADOPTED (2026-08-08)" `docs/phase-0-prereg-amendment-3.md:1` versus "**Status: DRAFT — not signed, not in force.**" `:3-20` | Both stand unamended in the file | SETTLED BY the tracker and the later amendments, which cite A3 as signed at `8ae4720`: `formal/PROPERTIES.md:75` ("2026-08-09, commit `8ae4720`"); `docs/phase-0-prereg-amendment-4.md:18`; `-5.md:27`; `-6.md:12` |
| S-03 | The first-link residual's closing conditions | Classify the RESULT lines cold, write the Q3 argument without the file open, reproduce the M1/M7 mutations by hand `formal/spike/first-link/DECISION.md:59` | For each symbolic result, state claim, adversary and boundary "with the record open and without the AI present"; "the ability to write or reproduce the ProVerif artifacts is not a condition" `:63-87` | SETTLED BY `formal/spike/first-link/DECISION.md:63-87` (Correction PROPOSED 2026-09-05, **ADOPTED (author) 2026-09-06**, "accepted as-is"). The original sentence is retained per amend-don't-rewrite (`:121-123`) |
| S-04 | §A5.6 on two identities sharing one key | Model header: it "does NOT decide whether an issuer holding two identities on one key keeps one terminal lineage record or two" `formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:78` | RESULTS quotes the pre-correction wording: does not prove "anything about two identities legitimately sharing one key **beyond their having separate lineages**" `formal/suite/s-standing/RESULTS.md:1197-1199` (registered verbatim at `PREDICTIONS.md:787-792`) | SETTLED BY `formal/suite/s-standing/RESULTS.md:1318-1333` (cross-family review item 4, 2026-09-12, ACCEPTED-verified): "a divergence between the frozen plan and the signed amendment, and the **amendment governs**" |
| S-05 | What a `wrapCore` presentation produces after the pin | Header: "no LINEAGE-DERIVED report (no mismatch, supersession or refusal report); the no-TLR report is unaffected" `ss_q1d_degraded_compromised.pv:88-91` | RESULTS: "no report at all rather than an `ABSENT / STANDING_EVIDENCE_MISMATCH` report" `formal/suite/s-standing/RESULTS.md:1203-1207` | SETTLED BY `formal/suite/s-standing/RESULTS.md:1335-1348` (item 5, 2026-09-12): the overbroad wording is falsified by `wrap_routes.out:1944` and "Lines 1203–1207 above repeat the overbroad wording and are corrected to this" |
| S-06 | Does the "presence only" version line still stand for `cvI` | Addendum block: it "stands as written for cvW and for the base path; on the WRAPPED path it does NOT stand as written for cvI" `formal/suite/s-p7/proverif/sp7_q2_degraded_compromised.pv:142-145` | RESULTS: it "stands as written for `cvI`, `cvW` and the base path and is narrowed by the addendum for `cvIw` on the wrapped path only" `formal/suite/s-p7/RESULTS.md:964-967` | SETTLED BY `formal/suite/s-p7/RESULTS.md:1240-1250` (cross-family review item 3, 2026-09-12): "Lines 964-967 above repeat the wrong wording and are corrected to this. ACCEPTED-verified" |
| S-07 | The Q7-C companion's registered trace shape | Companion: "Registered trace shape: an HONEST Wrapper process ... and VerifierWrapped accepts" `formal/suite/s-p7/proverif/sp7_q7_companion_version_unchecked.pv:22-35` | RESULTS: "It is the unregistered second shape, not the registered one ... **No honest process appears in the trace at all** ... Recorded as an open cell" `formal/suite/s-p7/RESULTS.md:1005-1043` | SETTLED BY `formal/suite/s-p7/RESULTS.md:1251-1279` (item 4, 2026-09-12): the reviewer's `literal_honest_wrapper` model exhibits the registered shape; "The open cell is closed; the closure is the reviewer's, not this file's" |
| S-08 | Who consumes the type-soundness relation | Registered S-P7 ledger entry: "Consumers: S-P1 (integrity over bytes of *this* type), S-P2, ..." (`PREDICTIONS.md:485`) | S-P1's frozen plan: "S-P1 consumes nothing from S-P7" (`s-p1/PREDICTIONS.md:450-453`, frozen `5188e7a`) | SETTLED BY `formal/suite/s-p7/RESULTS.md:495-509` (dated note 2026-09-06, skeptic review 2): "**S-P1 declines this relation** ... the join is composed at the capstone, not consumed by S-P1"; the registered text "is left as written and the correction recorded as divergence 8" |
| S-09 | COVERAGE-MAP row 1 versus the S-P1 record | Row 1: symbolic leg "none — S-P1 enumerated (ENUM §2), not built"; join "Consumes SP3 ledger entry 1 (key binding)" `formal/COVERAGE-MAP.md:23` | S-P1: both "are contradicted by this record (five models built and run; ledger entry 1 above, complementary not consumed)", and the announced correction "is **not yet made**" `formal/suite/s-p1/RESULTS.md:536-548` | SETTLED BY `formal/COVERAGE-MAP.md:85` (Correction 2026-09-12, **PROPOSED**): row 1's three cells declared superseded, TRK status now `checked`. The row text itself is unchanged |
| S-10 | Is the P5c ↔ P5P6 correspondence exact by construction | Header: "the correspondence between this module's acceptance and P5c's Ship is exact by construction, not by argument" `formal/tla/P5P6_TemporalRevocation.tla:14-19` | Tracker: the two "model the quantity incompatibly ... the join was asserted, not checked" `formal/PROPERTIES.md:101-104`; `P5c_IssuanceProtocol.tla:23-26` still says "Ship's fused guard IS the chain-time predicate" | SETTLED BY `formal/tla/P5P6_TemporalRevocation.tla:21-36` (CORRECTION 2026-09-06 item 12, **PROPOSED**): the sentence "predates the bridge model and overstates ... the correspondence was ASSERTED in comments and checked nowhere until `P5cP5P6_Bridge.tla`"; the bridge checks it as `ShippedDesignatedAgree` (`formal/PROPERTIES.md:105-108`) |
| S-11 | Does `+DepthK` headroom 14 exercise post-refusal burial | Tracker body: "+DepthK headroom = 14 exercises post-refusal burial, the `RefusalBuriedAnchorUnreachable` witness guards" `formal/PROPERTIES.md:190-222` | Tracker falsification bullet: the witness "fires at `MaxTime = 12` ... recut owed" `formal/PROPERTIES.md:156-160` | SETTLED BY `formal/PROPERTIES.md:223-250` (Note 2026-09-06, **PROPOSED**): the recut adds `refusedAt`, `RefusalTimeConsistent` and `~(refused /\ anchorAt >= refusedAt /\ depth >= DepthK)`, unreachable at 12 and 13 and firing at 14, "so the sentence above is true of the recut witness". All three statuses coexist in the tracker |
| S-12 | Is `ExpiredCannotShip` the registered expiry rule | `ExpiredCannotShip == (~shipped /\ now > declared + Delta) => ~ENABLED Ship` makes every unshipped attempt past its window unable to ship `formal/tla/P5c_IssuanceProtocol.tla:309-310` | The registered lifecycle latches eligibility: "a timely-eligible attempt cannot be expired by scheduling delay" `formal/tla/READING-AID-P5c.md:265-272` | SETTLED BY `formal/tla/P5c_IssuanceProtocol.tla:118-126` (CORRECTION 2026-09-06 item 16, **PROPOSED**): latching "is the registered lifecycle ... and is MODELED AND CHECKED in `P5cP5P6_BridgeSlack_Latch.tla`. This module is the earlier, S = 0, pre-latch instance ... the reader is sent to the Latch module for the lifecycle claim" |
| S-13 | The standing decision's own status | "The standing-evidence mechanism decision — terminal lineage record — is thereby **entered**." (Entered, 2026-09-04; "author commit pending".) `formal/spike/standing-probe/DECISION.md:15-26` | "**Status: PROPOSED — scoring draft, nothing decided.**", retained deliberately: "The registered PROPOSED header is retained below, per amend-don't-rewrite." `formal/spike/standing-probe/DECISION.md:28, 12-13` | SETTLED BY the author's commit `fbf6387` (2026-09-04, "Another round: mostly decisions, a few small clarifications.  Ratified and time to move forward."), which is the commit that added the "Entered, 2026-09-04" note to that file (`git log` on `formal/spike/standing-probe/DECISION.md`); the selection is carried forward in `formal/suite/ENUMERATION.md:486` amendment note 4. The PROPOSED header stands in the file per amend-don't-rewrite |
| S-14 | (was C-01) Is the Band 0 gate machine-checked when P8 may be discharged in prose | "The gate is **machine-checked**, by design." `docs/phase-0-prereg.md:715, 723` | A1 §A1.4: "The original said 'TLA+ and/or Lean4.' That was reached for on familiarity, and the review contested it"; P8 is "direct proof over the encoding rules (Lean4 if warranted, rigorous prose proof plus the golden-vector and rejection suites if that is honest sufficiency)" `docs/phase-0-prereg-amendment-1.md:359-378` | SETTLED by A1 §A1.4, a signed amendment that names the original sentence it revises. The form of the P8 proof remains a decision to make (§11, `BAND0-EXIT.md` E3a) but is not a contradiction. Moved from the open table 2026-09-13 by the owner instance, recording the record. |
| S-15 | (was C-02) Revocation after declared issue time but at or before `anchor_time` | Original §4.4: a key revoked after issue leaves the attestation `VALID_STRICT` `docs/phase-0-prereg.md:537-546` | A1 §A1.2 P6: `VALID_STRICT` requires no revocation effective at or before `anchor_time`, "deliberately stricter" `docs/phase-0-prereg-amendment-1.md:199-233`; A4 §A4.3 writes the sentence "Revocation effective after both `anchor_time` and `declared_issue_time` does not retroactively change the verdict" with the author's "fix the prose to conform with the intent" `docs/phase-0-prereg-amendment-4.md:111-123` | SETTLED by A1 P6 (an amendment tightening the original, which A1 §A1.1 discipline permits) as clarified by A4 §A4.3. The verifier applies P6's two-conjunct rule. Moved from the open table 2026-09-13 by the owner instance. |
| S-16 | (was C-14) Are the P4/P5/P5c/P6 reading aids written | Tracker: "Author reads of the plain-language statements: not yet possible (reading aids for these modules not yet written)." `formal/PROPERTIES.md:161-162` | `formal/tla/READING-AID-P4.md`, `READING-AID-P5P6.md`, `READING-AID-P5c.md` exist, dated 2026-09-06 | SETTLED by the tree; a tracker-currency defect, corrected by an appended note in `formal/PROPERTIES.md` dated 2026-09-13. The author read itself is item E9 of `BAND0-EXIT.md`. |

**Note on the settled table.** Four of the sixteen settling texts (S-09, S-10,
S-11, S-12) carry a `PROPOSED` or "not adopted; the commit is the author's"
label. They settle the conflict as a record fact; whether they are in force is
the author's to state. S-01, S-02, S-03 and S-13 are settled by signed or
author-committed text; S-04 through S-08 by dated review dispositions marked
ACCEPTED-verified in the family record.

---

## Appendix A — requirement index

Every requirement in this document, in document order: its identifier, the
first eight words of its statement, and its provenance tags verbatim.
Generated from the assembled text on 2026-09-13.

| ID | Statement (first eight words) | Provenance tag(s) |
|---|---|---|
| R-1.1 | Tessera attests the identity of the framed bytes | [REGISTERED A3 §A3.1, docs/phase-0-prereg-amendment-3.md:61-66; author-ruled 2026-07-28, docs/reviews/2026-07-28-identity-boundary-evidence-floors-ruling.md:61-67] |
| R-1.2 | Explicitly outside the attestation: meaning, truth, intended use, | [REGISTERED A3 §A3.1, docs/phase-0-prereg-amendment-3.md:64-66] |
| R-1.3 | Tessera establishes *computational* identity of the framed representation, | [RULED (author) 2026-07-28, docs/reviews/2026-07-28-identity-boundary-evidence-floors-ruling.md:90-95] |
| R-1.4 | The can/does-not-establish list is recorded verbatim and is | [REGISTERED A3 §A3.1 item 4, docs/phase-0-prereg-amendment-3.md:89-96; verbatim text at docs/reviews/2026-07-28-identity-boundary-evidence-floors-ruling.md:79-88] |
| R-1.5 | Re-presenting a genuinely issued package preserves identity, and | [REGISTERED A3 §A3.1 item 1, docs/phase-0-prereg-amendment-3.md:68-74] |
| R-1.6 | P1's symbolic statement is existential issuance-event authenticity (a | [REGISTERED A3 §A3.1 item 1, docs/phase-0-prereg-amendment-3.md:71-74; MODELLED S-P1, formal/suite/s-p1/proverif/sp1_q2_degraded_compromised.pv:163-164 (the correspondence query), :168-181 (the verifier)] |
| R-1.7 | The operative form of the H0 headline is: | [REGISTERED A3 §A3.1 item 2, docs/phase-0-prereg-amendment-3.md:75-83] |
| R-1.8 | The load-bearing modelled check for the operative form | [MODELLED S-P1, formal/suite/s-p1/proverif/sp1_q2_degraded_compromised.pv:38-47, 176-177 — modelled, and registered only in the A3 §A3.1 item 2 form] |
| R-1.9 | The repository shall carry a coverage map from | [REGISTERED A3 §A3.1 item 3, docs/phase-0-prereg-amendment-3.md:84-88] |
| R-1.10 | In degraded mode — any verdict other than | [RULED (author) A4 §A4.6, docs/phase-0-prereg-amendment-4.md:156-172] |
| R-1.10a | The bearer of A2 §A2.4's prohibition on ordering | [RULED (author) 2026-09-14; instrument A7 §A7.4, PROPOSED; §12 C-06. A7 §A7.4 records this as a narrowing of A2 §A2.4's bearer, stated as such on the record] |
| R-1.11 | A correspondence that holds in strict mode and | [RULED (author) A4 §A4.6, docs/phase-0-prereg-amendment-4.md:167-171] |
| R-1.12 | R-1.11 is bounded: "Only losses permitted by the | [RULED (author) A5 §A5.7, docs/phase-0-prereg-amendment-5.md:221-241, quoted sentence at :233-236] |
| R-1.13 | `VALID_STRICT` attests envelope soundness, never payload truth. The | [REGISTERED A3 §A3.8, docs/phase-0-prereg-amendment-3.md:679-684] |
| R-1.14 | No unqualified aggregate checkmark is part of the | [REGISTERED A3 §A3.8, docs/phase-0-prereg-amendment-3.md:703-704] |
| R-1.15 | The base assessment is an unsigned, reproducible computation; | [REGISTERED A3 §A3.8, docs/phase-0-prereg-amendment-3.md:686-689; the "unsigned" choice itself is `[AUTHOR DECISION — ratified -- 2026-08-08]` at :722-734] |
| R-1.16 | Verification verdict and protocol standing are reported separately | [REGISTERED A3 §A3.7.1, docs/phase-0-prereg-amendment-3.md:542-548] |
| R-1.17 | Standing is reported, never waived; no verifier policy, | [REGISTERED A3 §A3.7.1 `[PANEL-DRIVEN CLARIFICATION — 2026-08-08]`, docs/phase-0-prereg-amendment-3.md:550-557] |
| R-1.18 | A wrapper commits to the inner package's bytes, | [REGISTERED prereg §3.1, docs/phase-0-prereg.md:356-364; A1 P7, docs/phase-0-prereg-amendment-1.md:248-253] |
| R-1.19 | A tending record proves only that a named | [REGISTERED A3 §A3.5, docs/phase-0-prereg-amendment-3.md:403-405, 418-419] |
| R-1.20 | The century horizon is aspirational, not a guarantee | [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:322-326] |
| R-1.21 | The **verifier** is P9's pure function: bundle plus | [RULED (author) 2026-09-06, recorded in band-1 docket item 27, docs/band-1-docket.md:517-521; registered with A4 §A4.6, docs/phase-0-prereg-amendment-4.md:176-182] |
| R-1.22 | The **adjudicator** (the relying party) decides trust using | [RULED (author) 2026-09-06, recorded in band-1 docket item 27, docs/band-1-docket.md:521-525] |
| R-1.23 | An enumeration or observability API may feed a | [RULED (author) A4 §A4.6, docs/phase-0-prereg-amendment-4.md:181-182; docs/band-1-docket.md:525 ("an enumeration API")] |
| R-1.24 | The relying-party story defines both terms. | [RULED (author) 2026-09-06, docs/band-1-docket.md:524] |
| R-1.25 | The relying-party story is a required Band 0 | [REGISTERED A3 §A3.1 item 4, docs/phase-0-prereg-amendment-3.md:89-96] [OPEN — §11 O-66] |
| R-1.26 | The relying-party story is the human-facing statement of | [REGISTERED A3 §A3.8, docs/phase-0-prereg-amendment-3.md:736-737] |
| R-2.1 | The issuer signs with two keys from independent | [REGISTERED prereg §3.1 "Decision: C.", docs/phase-0-prereg.md:273-298] |
| R-2.2 | Issuance is not complete until the anchor is | [REGISTERED A1 P5 corollary, docs/phase-0-prereg-amendment-1.md:186-197; A2 §A2.1 "The rule", docs/phase-0-prereg-amendment-2.md:87-89] |
| R-2.3 | The issuer evaluates the full three-conjunct temporal predicate | [REGISTERED A3 §A3.7.3, docs/phase-0-prereg-amendment-3.md:654-663; REGISTERED A3 §A3.7.3 `[PANEL-DRIVEN REPAIR — 2026-08-08]`, :665-675] [RULED — §12 C-08, A7 §A7.6] |
| R-2.4 | Issuance makes at most N attempts (working default | [REGISTERED A2 §A2.3, docs/phase-0-prereg-amendment-2.md:252-276] |
| R-2.5 | The verifier's verdict is a pure function of | [REGISTERED A1 P9, docs/phase-0-prereg-amendment-1.md:278-281; prereg §4.4, docs/phase-0-prereg.md:519-525] |
| R-2.6 | For horizons requiring availability and evidentiary continuity, the | [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:314-320] |
| R-2.7 | Custodial renewal wraps, it never replaces; renewal must | [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:273-278; REGISTERED A3 §A3.5, :384-394] |
| R-2.8 | For refusal records, the generating authority retains the | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:583-596] |
| R-2.9 | The terminal lineage record is carried, not maintained: | [RULED (author) at adoption, formal/spike/standing-probe/DECISION.md:130-140, 386-390 — decided, not registered in an amendment] |
| R-2.10 | The issuer-key manifest carries two independent, archived, time-anchored | [REGISTERED A1 P10 / §A1.5, docs/phase-0-prereg-amendment-1.md:283-297, 430-442] |
| R-2.11 | The manifest self-signature is proof of possession only | [REGISTERED A1 §A1.5 item 3, docs/phase-0-prereg-amendment-1.md:439-442] |
| R-2.12 | `VALID_STRICT` requires all external authority evidences to validate, | [REGISTERED A1 P10, docs/phase-0-prereg-amendment-1.md:290-291; A1 §A1.5, :444-448] |
| R-2.13 | The channels are generalised: "DNS" means any domain, | [RULED (author) in session 2026-09-06, recorded inside band-1 docket item 26, which is headed "candidate; not registered anywhere in the record", docs/band-1-docket.md:465-468] [OPEN — §11 O-69] |
| R-2.14 | Two carried caveats on channel count: channel count | [RULED (author) in session 2026-09-06, recorded inside band-1 docket item 26 (candidate, not registered), docs/band-1-docket.md:469-471] |
| R-2.15 | Declared residual: both present external channels are ultimately | [REGISTERED A1 §A1.5, docs/phase-0-prereg-amendment-1.md:450-458] |
| R-2.16 | Recorded as candidate, not registered: the attestation company | [PROPOSED — docket item 26, docs/band-1-docket.md:471-481] |
| R-2.17 | The verifier's pre-bundle inputs are trust configuration only: | [MODELLED standing-probe Q6, formal/spike/standing-probe/RESULTS-PROBE.md:41; DECIDED, formal/spike/standing-probe/DECISION.md:71-72 (G2) — modelled and decided, not registered in an amendment] |
| R-2.18 | The reference verifier maintains an archived historical trust-anchor | [REGISTERED A1 §A1.5, docs/phase-0-prereg-amendment-1.md:459-469] |
| R-2.19 | Block headers `h … h + k − | [REGISTERED A2 §A2.2, docs/phase-0-prereg-amendment-2.md:236-244] |
| R-2.20 | δ and ε belong to the verifier, not | [REGISTERED A1 P5, docs/phase-0-prereg-amendment-1.md:173-184] [OPEN — §11 O-44] |
| R-2.21 | In the symbolic models the verifier's only trust | [MODELLED S-P3, formal/suite/s-p3/proverif/sp3_q2_degraded_compromised.pv:98, 149-153; S-STANDING strict, formal/suite/s-standing/proverif/ss_q1_strict_dns_compromised.pv:348-356] |
| R-2.22 | Everything else arrives on the public channel as | [MODELLED S-P3, formal/suite/s-p3/proverif/sp3_q2_degraded_compromised.pv:98-100; S-P1 unchanged, formal/suite/s-p1/proverif/sp1_q2_degraded_compromised.pv:166-170] |
| R-2.23 | The standing path takes standing evidence and the | [MODELLED S-STANDING, formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:319-326; RULED, docs/phase-0-prereg-amendment-5.md:202-219] |
| R-2.24 | P9's discharge is : an enumeration of the | [RULED A4 §A4.1, docs/phase-0-prereg-amendment-4.md:60-71, as rewritten by A5 §A5.1, docs/phase-0-prereg-amendment-5.md:58-91] |
| R-2.25 | Verification yields exactly one of `VALID_STRICT`, `VALID_DEGRADED(policy=...)`, `INVALID`, | [REGISTERED prereg §3.1, docs/phase-0-prereg.md:327-337; prereg §4.6, :555-562; MODELLED P4, formal/tla/P4_VerifierStates.tla:70] |
| R-2.26 | `VALID_STRICT` requires all issue-time signatures to verify and | [REGISTERED prereg §3.1, docs/phase-0-prereg.md:307-311; MODELLED P4, formal/tla/P4_VerifierStates.tla:96-105] |
| R-2.27 | No verifier policy may waive: canonical-byte integrity (P1, | [REGISTERED A1 §A1.2.1, docs/phase-0-prereg-amendment-1.md:309-317] |
| R-2.28 | Degraded policies may weaken only declared redundancy: a | [REGISTERED A1 §A1.2.1, docs/phase-0-prereg-amendment-1.md:319-323] |
| R-2.29 | The P10 waiver is tightened to fewer, but | [REGISTERED A3 §A3.2, docs/phase-0-prereg-amendment-3.md:102-109, 139-145] |
| R-2.30 | If every external authority evidence for a layer | [REGISTERED A3 §A3.2, docs/phase-0-prereg-amendment-3.md:146-149] |
| R-2.31 | Required evidence that is present and whose validation | [RULED A5 §A5.2, docs/phase-0-prereg-amendment-5.md:93-121, rewriting A3 §A3.2 item 2] [RULED — §12 C-05, A7 §A7.3] |
| R-2.31a | Object scope, made explicit. A2 §A2.2's three temporal | [RULED (author) 2026-09-14; instrument A7 §A7.3, PROPOSED; §12 C-05] |
| R-2.32 | P4's unperformable rule applies to *required* checks only. | [RULED (author) A4 §A4.2, docs/phase-0-prereg-amendment-4.md:100-109] |
| R-2.33 | When one required check fails and another cannot | [RULED (author) A4 §A4.2, docs/phase-0-prereg-amendment-4.md:88-98; RULED, formal/spike/first-link/DECISION.md:385-391] |
| R-2.34 | `UNVERIFIABLE` is never silently promoted to `VALID`. | [REGISTERED prereg §4.6, docs/phase-0-prereg.md:335-337; MODELLED P4 `NoSilentPromotion`, formal/tla/P4_VerifierStates.tla:124] |
| R-2.35 | Every `VALID_DEGRADED` verdict records the precise waived check | [REGISTERED A1 §A1.2.1, docs/phase-0-prereg-amendment-1.md:325-327] |
| R-2.36 | For each waived check the record additionally holds | [RULED A5 §A5.3, docs/phase-0-prereg-amendment-5.md:134-155] [OPEN — §11 O-06] [RULED — §12 C-05, A7 §A7.3] |
| R-2.37 | Where the binding assessment is concerned, a well-formed | [RULED (author) — the source's own label is ADOPTED (author) 2026-08-13, formal/spike/first-link/DECISION.md:366-383 — decided in a spike DECISION.md, not registered in an amendment] |
| R-2.38 | The two `UNVERIFIABLE` cases — unknown identifier and | [RULED, formal/spike/first-link/DECISION.md:393-397] |
| R-2.39 | The floors bound entry into the two `VALID` | [REGISTERED A3 §A3.2, docs/phase-0-prereg-amendment-3.md:165-167; A3 §A3.7.1, :541-546] |
| R-2.40 | The Band 0 adversary can, at minimum: (1) | [REGISTERED A1 §A1.3, docs/phase-0-prereg-amendment-1.md:331-346] |
| R-2.41 | Item 6 reads "Control any proper subset of | [REGISTERED A1 §A1.3 item 6, docs/phase-0-prereg-amendment-1.md:344-346; MODELLED, formal/spike/first-link/RESULTS.md:84-107 with documentation correction 2026-08-12] [OPEN — §11 O-69] |
| R-2.42 | The degraded-mode fixtures are strictly stronger than item | [MODELLED S-P3, formal/suite/s-p3/proverif/sp3_q2_degraded_compromised.pv:143-154; DECIDED, formal/spike/first-link/DECISION.md:770-778] |
| R-2.43 | DSKS is modelled as a constructor `dsks(s, r)` | [MODELLED library, formal/suite/lib/tessera_theory.pvl:46-53, 98-101, 110, 114-115; REGISTERED A1 §A1.3 item 3, docs/phase-0-prereg-amendment-1.md:339-342] |
| R-2.44 | Ed25519 signature verification alone does not provide protocol-level | [REGISTERED A1 P3, docs/phase-0-prereg-amendment-1.md:129-150] |
| R-2.45 | Out of scope for the cryptographic construction: an | [REGISTERED A1 §A1.3 item 7, docs/phase-0-prereg-amendment-1.md:347-353; prereg §3.1, docs/phase-0-prereg.md:388-404] |
| R-2.46 | Out of scope: breaking the idealized primitives — | [REGISTERED A1 §A1.3, docs/phase-0-prereg-amendment-1.md:353-355] |
| R-2.47 | Issuer-key compromise is not covered by any model: | [PROPOSED — docket item 26, candidate 2026-09-05, docs/band-1-docket.md:385-400] [OPEN — §11 O-19] |
| R-2.48 | Recorded without objection but not registered: rotation is | [PROPOSED — docket item 26, docs/band-1-docket.md:429-433] [OPEN — §11 O-19] |
| R-2.49 | H0 is falsified if any A1.2 property cannot | [REGISTERED A1 §A1.1, docs/phase-0-prereg-amendment-1.md:71-95] |
| R-3.1 | The canonical form binds to RFC 8785 (JSON | [REGISTERED prereg §4.3, docs/phase-0-prereg.md:496-506] |
| R-3.2 | Any value not exactly a double (hashes, large/256-bit | [REGISTERED prereg §4.3, docs/phase-0-prereg.md:502-506] |
| R-3.3 | `canonical()` is injective on its accepted payload domain | [REGISTERED A1 §A1.2 P8, docs/phase-0-prereg-amendment-1.md:255-277] |
| R-3.4 | The accepted domain is closed by explicit rejection: | [REGISTERED A1 §A1.2 P8, docs/phase-0-prereg-amendment-1.md:264-273] |
| R-3.5 | The canonical form is frozen and explicitly versioned: | [REGISTERED prereg §4.3, docs/phase-0-prereg.md:486-494] |
| R-3.6 | Every canonicalization version has byte-for-byte golden examples and | [REGISTERED prereg §4.3, docs/phase-0-prereg.md:508-512; A1 §A1.2 P8, docs/phase-0-prereg-amendment-1.md:273-276] |
| R-3.7 | The claim made for the length binding is | [REGISTERED prereg §4.3, docs/phase-0-prereg.md:514-517] |
| R-3.8 | Schema validation rejects raw JSON numerics exceeding IEEE | [DOCKET 4 — candidate, not registered, docs/band-1-docket.md:32-36] [OPEN — §11 O-02] |
| R-3.9 | Signatures and anchors commit to a framed envelope | [REGISTERED A1 §A1.2 P8, docs/phase-0-prereg-amendment-1.md:255-264] |
| R-3.10 | The exact binary layout is fixed, with golden | [REGISTERED A1 §A1.2 P8, docs/phase-0-prereg-amendment-1.md:262-264] [OPEN — §11 O-01] |
| R-3.11 | The signed bytes include, at minimum: domain-separation tag, | [REGISTERED A1 §A1.2 P3, docs/phase-0-prereg-amendment-1.md:140-144] |
| R-3.12 | For a multi-signer attestation the six non-fingerprint fields | [RULED (author) A5 §A5.4 — ADOPTED (author), docs/phase-0-prereg-amendment-5.md:165-190 (the (a)/(b) fork at :165-179; the six-field sentence at :179-183)] [RULED — §12 C-15, A7 §A7.9] |
| R-3.12a | P8's four-field signed frame and A5 §A5.4's seven | [RULED (author) 2026-09-14; instrument A7 §A7.9, PROPOSED; §12 C-15] [OPEN — §11 O-79] |
| R-3.13 | As modelled the frame is the seven-field transparent | [MODELLED LIB, formal/suite/lib/tessera_theory.pvl:77-84; MODELLED S-P3, formal/suite/s-p3/proverif/sp3_q2_degraded_compromised.pv:60, :107-109; formal/suite/s-p3/RESULTS.md:261-275] |
| R-3.14 | Explicit binary widths and endianness for `payload_length` and | [DOCKET 5 — candidate, not registered, docs/band-1-docket.md:37-40] [OPEN — §11 O-01] |
| R-3.15 | Every signed object carries a domain-separation type tag | [REGISTERED A1 §A1.2 P7, docs/phase-0-prereg-amendment-1.md:235-240] |
| R-3.16 | The set gains the terminal lineage record and | [REGISTERED A4 §A4.5, docs/phase-0-prereg-amendment-4.md:144-151; REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:295-300] |
| R-3.17 | A wrapper commits to the inner package's exact | [REGISTERED A1 §A1.2 P7, docs/phase-0-prereg-amendment-1.md:240-248] |
| R-3.18 | The wrapper records both inner and outer canonicalization | [REGISTERED A1 §A1.2 P7, docs/phase-0-prereg-amendment-1.md:248-249; RULED (author) A5 §A5.5, docs/phase-0-prereg-amendment-5.md:192-200] |
| R-3.19 | The wrapper attests the inner bytes, never the | [REGISTERED A1 §A1.2 P7, docs/phase-0-prereg-amendment-1.md:249-253] |
| R-3.20 | As modelled the wrapper embedding is `wrap(cvInner, (innerBytes, | [MODELLED S-P7, formal/suite/s-p7/proverif/sp7_q2_degraded_compromised.pv:94-96, :316-318; formal/COVERAGE-MAP.md:55] [OPEN — §11 O-70] |
| R-3.21 | The complete portable refusal record carries attempt identity, | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:572-581] |
| R-3.22 | The commitment construction must resist practical guessing or | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:648-653] [OPEN — §11 O-07] |
| R-3.23 | One signing act at terminal disposition produces the | [RULED (author) SC-2 2026-08-31/09-04, formal/spike/standing-probe/DECISION.md:96-115] |
| R-3.24 | As probed, the TLR is signed by the | [MODELLED standing-probe G0 (Q2/Q3), formal/spike/standing-probe/DECISION.md:61-66; the mechanism selection itself is ADOPTED (author), :378-384 — not registered in an amendment] |
| R-3.25 | As modelled the standing objects are `attemptCore(t, ppf, | [MODELLED S-STANDING, formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:122-142] |
| R-3.26 | A tending record has exactly one of four | [REGISTERED A3 §A3.5, docs/phase-0-prereg-amendment-3.md:384-402 — amendment text, no `[AUTHOR DECISION]` marker on this passage] |
| R-3.27 | The base assessment is an unsigned, reproducible computation | [REGISTERED A3 §A3.8, docs/phase-0-prereg-amendment-3.md:686-704; the "unsigned" choice is `[AUTHOR DECISION — ratified -- 2026-08-08]` at :722-734] |
| R-3.28 | A party needing portable attribution, evaluation-time evidence or | [REGISTERED A3 §A3.8, docs/phase-0-prereg-amendment-3.md:712-720] |
| R-3.29 | Long-horizon evidentiary continuity uses RFC 4998 (ERS) renewal | [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:273-278] |
| R-3.30 | Candidates, not registered: that a renewal chain is | [DOCKET 19-23 — candidates, not registered, docs/band-1-docket.md:245-320] [OPEN — §11 O-30 to O-34] |
| R-3.31 | The bundle carries an issuer-key manifest: the issuer | [REGISTERED prereg §4.4, docs/phase-0-prereg.md:527-535] [RULED — §12 C-04, A7 §A7.2] |
| R-3.31a | "(or references)" stands, bounded. A reference in the | [RULED (author) 2026-09-14; instrument A7 §A7.2, PROPOSED; §12 C-04. "Explicitly declared" is A7's stated reading of how P9 is preserved, recorded there so it can be corrected] |
| R-3.32 | The manifest carries two independent, archived, time-anchored authority-publication | [REGISTERED A1 §A1.2 P10, docs/phase-0-prereg-amendment-1.md:283-297; A1 §A1.5, docs/phase-0-prereg-amendment-1.md:430-442] |
| R-3.33 | External authority evidence must unambiguously bind the exact | [REGISTERED A3 §A3.2.1, docs/phase-0-prereg-amendment-3.md:178-184] |
| R-3.34 | Transcription binding is the first-link mechanism discharging that | [DECIDED — first-link mechanism selection, entered by the author 2026-08-13 at `459aff0`, formal/spike/first-link/DECISION.md:1-9; text at :145-159 sits under the heading "Proposed decision" and carries no per-statement RULED/ADOPTED label (see the label discipline at :125-143); not registered in an amendment] |
| R-3.35 | Distinct tags per form — `STMT_DIRECT` versus `STMT_DIGEST` | [DECIDED — first-link selection, formal/spike/first-link/DECISION.md:353-362 (unlabelled sections "Selected: authenticated, domain-separated forms" and "Map v1 ruling"; the enabling observation at :338-344 is the author's, 2026-08-12); MODELLED LIB D-1, formal/suite/lib/tessera_theory.pvl:144-150] |
| R-3.36 | Authority-relevance map v1 is the tuple (issuer identity, | [MODELLED LIB D-2, formal/suite/lib/tessera_theory.pvl:170-175; RULED (author) formal/spike/first-link/DECISION.md:237-243] |
| R-3.37 | An envelope carries a signed, nonempty required set | [RULED (author) — the source's own label is ADOPTED (author) 2026-08-13, "Labelled ADOPTED rather than RULED because the reasoning originated in the cross-review", formal/spike/first-link/DECISION.md:366-383] |
| R-3.38 | Possession is the manifest self-signature `sign((POSS, manifest), sk)`, | [REGISTERED A3 §A3.2, docs/phase-0-prereg-amendment-3.md:153-157; MODELLED LIB D-3, formal/suite/lib/tessera_theory.pvl:37-45] |
| R-3.39 | Anything fixed at attestation time and later used | [RULED (author) 2026-08-12, formal/spike/first-link/DECISION.md:338-344] |
| R-3.40 | The forward-link / predeclared successor slot rides inside | [RULED (author) 2026-09-04, formal/spike/standing-probe/DECISION.md:368-377; DOCKET 25, docs/band-1-docket.md:355-384] [OPEN — §11 O-10] |
| R-3.41 | The algorithm identifier and all parameters that affect | [RULED (author) A3 §A3.6.1, docs/phase-0-prereg-amendment-3.md:486-502] [OPEN — §11 O-03] |
| R-3.42 | A shipped receipt contains exactly one anchor proof | [REGISTERED A2 §A2.4, docs/phase-0-prereg-amendment-2.md:299-312] |
| R-3.43 | The txid necessarily lives in the bundle outside | [REGISTERED A2 §A2.4, docs/phase-0-prereg-amendment-2.md:321-323] |
| R-3.44 | `declared_issue_time` is what the issuer claims and asserts | [REGISTERED A1 §A1.2 temporal vocabulary, docs/phase-0-prereg-amendment-1.md:111-114, restated A1 §A1.6 at :482-491; A2 §A2.4, docs/phase-0-prereg-amendment-2.md:324-327] |
| R-3.45 | `confirmed_at := timestamp(block at height h + k | [REGISTERED A2 §A2.1, docs/phase-0-prereg-amendment-2.md:80-86] |
| R-3.46 | A receipt records its issue-time policy version and | [REGISTERED A1 §A1.2 P5, docs/phase-0-prereg-amendment-1.md:173-177] |
| R-3.47 | The verifier must evaluate `confirmed_at` statelessly: block headers | [REGISTERED A2 §A2.2, docs/phase-0-prereg-amendment-2.md:236-244; the candidate-chain-segment and header-provenance sentences are A2 §A2.1, :197-206] [OPEN — §11 O-22] |
| R-3.48 | Embed the k-header segment in `authority_evidence` so a | [DOCKET 6-7 — candidates, not registered, docs/band-1-docket.md:41-49] [OPEN — §11 O-09, O-22] |
| R-3.49 | "Where the bundle ships before chain confirmation, it | [RULED (author) SC-1 cost (ii), adopted 2026-09-04, formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:56-58, 65-69] |
| R-3.50 | The bundle carries an unambiguous verification-spec identifier and | [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:290-304] |
| R-3.51 | The bundle identifies, for each Tessera-verification dependency, the | [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:342-352] |
| R-3.52 | Payload-interpretation dependencies travel as an optional typed Representation | [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:357-363] |
| R-3.53 | Conformance vectors are two layers: a fixed floor | [REGISTERED A3 §A3.5, docs/phase-0-prereg-amendment-3.md:453-458; A3 §A3.6.2, docs/phase-0-prereg-amendment-3.md:517-520] |
| R-3.54 | A possessed bundle can be verified without Tessera: | [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:261-269; A1 §A1.2 P9, docs/phase-0-prereg-amendment-1.md:278-281] |
| R-3.55 | In the S-P7 models the wrapper's embedded pair | [MODELLED S-P7, formal/COVERAGE-MAP.md:55] [OPEN — §11 O-70] |
| R-3.56 | A declared per-bundle byte budget, above which content | [DOCKET 9, docs/band-1-docket.md:54-56; DOCKET 17, docs/band-1-docket.md:133-206; consequence recorded at first-link criterion 4 as a construction-level judgment ("PASS, WEAKLY (not query-discharged)"), formal/spike/first-link/DECISION.md:261-275] [OPEN — §11 O-08, O-42] |
| R-3.57 | Third-party logs are an intended consumer, so the | [DOCKET 27 — candidate, not registered, docs/band-1-docket.md:483-516] |
| R-3.58 | Each layer records which canonical form it used; | [REGISTERED prereg §3.1/§4.3, docs/phase-0-prereg.md:348-352, :508-512] |
| R-3.59 | Verdict namespace: `VALID_STRICT`, `VALID_DEGRADED(policy=...)`, `INVALID`, `UNVERIFIABLE` — a | [REGISTERED prereg §4.6, docs/phase-0-prereg.md:555-562] |
| R-3.60 | Standing namespace as registered in the S-series table: | [RULED (author) 2026-08-12 / 2026-09-04, formal/spike/first-link/DECISION.md:790-832] [RULED — §12 C-10, A7 §A7.7] |
| R-3.60a | One vocabulary. The standing report's value set is | [RULED (author) 2026-09-14; instrument A7 §A7.7, PROPOSED; §12 C-10] [OPEN — §11 O-75] |
| R-3.61 | Standing namespace as registered in the standing-probe and | [REGISTERED A3 §A3.7.1 for the `ESTABLISHED` / `ABSENT` / `UNVERIFIABLE` triple, docs/phase-0-prereg-amendment-3.md:542-546; RULED (author) 2026-09-04 for the four reason codes, formal/spike/standing-probe/DECISION.md:116-129, :138-141; formal/spike/first-link/DECISION.md:834-847] [RULED — §12 C-10, A7 §A7.7] |
| R-3.62 | Binding-form reason codes: a well-formed identifier unknown to | [RULED (author) 2026-08-13, formal/spike/first-link/DECISION.md:393-405] |
| R-3.63 | The envelope reason code `KEY_FINGERPRINT_MISMATCH` exists, and a | [Suite obligation carried from the blind re-scoring — not an author ruling and not registered in an amendment, formal/suite/ENUMERATION.md:502-509] |
| R-3.64 | A degraded verdict records, for each waived check, | [RULED (author) A5 §A5.3, docs/phase-0-prereg-amendment-5.md:134-155; DOCKET 28, docs/band-1-docket.md:62-66] [OPEN — §11 O-06] |
| R-3.65 | As modelled the standing report carries (verdict, reason, | [MODELLED S-STANDING, formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:144-159, :175-176] |
| R-3.66 | Reason-carrying output is a conformance requirement, not a | [RULED (author) 2026-08-12, formal/spike/first-link/DECISION.md:748-768] |
| R-3.67 | Retrieval failure for externally referenced verification inputs yields | [DOCKET 17 — candidate, not registered, docs/band-1-docket.md:168-172] |
| R-4.1 | The accepted payload domain is closed by explicit | [REGISTERED A1 P8, docs/phase-0-prereg-amendment-1.md:264-273] |
| R-4.2 | Rejection is required at minimum for: duplicate object | [REGISTERED A1 P8, docs/phase-0-prereg-amendment-1.md:264-273] |
| R-4.3 | Any value not exactly a double (hashes, large/256-bit | [REGISTERED prereg §4.3, docs/phase-0-prereg.md:502-506] |
| R-4.4 | Schema validation rejecting raw JSON numerics exceeding IEEE | [DOCKET 4 — candidate, docs/band-1-docket.md:32-36] [OPEN — §11 O-02] |
| R-4.5 | Golden vectors evidence the positive domain and the | [REGISTERED A1 P8, docs/phase-0-prereg-amendment-1.md:273-276] |
| R-4.6 | The canonical form binds to RFC 8785 (JSON | [REGISTERED prereg §4.3, docs/phase-0-prereg.md:496-506] |
| R-4.7 | The canonical form is frozen and explicitly versioned: | [REGISTERED prereg §4.3, docs/phase-0-prereg.md:486-494] |
| R-4.8 | Signatures and anchors commit to a framed envelope, | [REGISTERED A1 P8, docs/phase-0-prereg-amendment-1.md:255-264] |
| R-4.9 | The exact binary layout of the frame is | [REGISTERED A1 P8, docs/phase-0-prereg-amendment-1.md:262-264] [OPEN — §11 O-01] |
| R-4.10 | Every signed object carries a domain-separation type tag | [REGISTERED A1 P7, docs/phase-0-prereg-amendment-1.md:235-240] |
| R-4.11 | The enumerated set gains two members with their | [REGISTERED A4 §A4.5, docs/phase-0-prereg-amendment-4.md:144-151] |
| R-4.12 | The algorithm identifier rides inside the canonical payload | [RULED (author) 2026-08-08, A3 §A3.6.1, docs/phase-0-prereg-amendment-3.md:493-502] [OPEN — §11 O-03] |
| R-4.13 | The issuer signs with two keys from independent | [RULED prereg §3.1, docs/phase-0-prereg.md:273-298] |
| R-4.14 | The attestation carries a *set* of signatures (a | [REGISTERED prereg §3.1, docs/phase-0-prereg.md:307-311] |
| R-4.15 | The signed bytes include, at minimum: domain-separation tag, | [REGISTERED A1 P3, docs/phase-0-prereg-amendment-1.md:129-150] |
| R-4.16 | For a multi-signer attestation, the six non-fingerprint fields | [RULED (author) A5 §A5.4, docs/phase-0-prereg-amendment-5.md:156-190] |
| R-4.17 | Reading (a) governs R-4.16: common attested content in | [RULED (author) C8, formal/suite/ROUTED-2026-09-06.md:470-479; stated as correctable at docs/phase-0-prereg-amendment-5.md:166-182] |
| R-4.18 | Revocation is terminal: a revoked key is never | [REGISTERED A1 P6, docs/phase-0-prereg-amendment-1.md:216-224] |
| R-4.19 | The commit-signing key (Tyst, ed25519, `...42C73835`) is passphraseless | [REGISTERED prereg §4.2, docs/phase-0-prereg.md:454-463] |
| R-4.20 | Trigger to revisit: if anyone relies on issued | [REGISTERED prereg §4.2, docs/phase-0-prereg.md:465-469] |
| R-4.21 | Key material is never logged; the control is | [REGISTERED prereg §4.1, docs/phase-0-prereg.md:447-452] |
| R-4.22 | No declared maximum validity window for the *issuer* | [DOCKET 26 — candidate, docs/band-1-docket.md:385-400] [OPEN — §11 O-19] |
| R-4.23 | The execution model by which the service edge | [DOCKET 1 — candidate, docs/band-1-docket.md:11-17] [OPEN — §11 O-14] |
| R-4.24 | The bundle carries an issuer-key manifest: the issuer | [REGISTERED prereg §4.4, docs/phase-0-prereg.md:527-535] [RULED — §12 C-04, A7 §A7.2] |
| R-4.25 | The manifest carries two independent, archived, time-anchored authority-publication | [REGISTERED A1 P10, docs/phase-0-prereg-amendment-1.md:283-297] |
| R-4.26 | Evidence 1 is the `wamason.com` DNSSEC records publishing | [REGISTERED A1 §A1.5, docs/phase-0-prereg-amendment-1.md:430-433] |
| R-4.27 | Evidence 2 is the public git commit publishing | [REGISTERED A1 §A1.5, docs/phase-0-prereg-amendment-1.md:434-438] |
| R-4.28 | The manifest self-signature is proof of possession only. | [REGISTERED A1 §A1.5, docs/phase-0-prereg-amendment-1.md:439-442] |
| R-4.29 | Transcription binding is the §A3.2.1 first-link mechanism: authority | [DECIDED 2026-08-13, formal/spike/first-link/DECISION.md:145-152] |
| R-4.30 | Two binding forms are permitted protocol forms: the | [DECIDED, formal/spike/first-link/DECISION.md:153-159, 353-357] |
| R-4.31 | The map-v1 authority-relevant tuple is (issuer identity, key | [MODELLED LIB D-2, formal/suite/lib/tessera_theory.pvl:170-175] |
| R-4.32 | The tuple's fields are *bound*, not *validated*. Only | [DECIDED, formal/spike/first-link/DECISION.md:237-243] |
| R-4.33 | Binding-form tags are authenticated verification semantics, not authority-relevant | [RULED (author) 2026-08-12, formal/spike/first-link/DECISION.md:359-363] |
| R-4.34 | Anything fixed at attestation time and later used | [RULED (author) 2026-08-12, formal/spike/first-link/DECISION.md:338-344] |
| R-4.35 | Tessera records the representation version, binding form, hash | [DECIDED, formal/spike/first-link/DECISION.md:310-317] |
| R-4.36 | The issuer does not re-run envelope verification at | [REGISTERED A3 §A3.7.3, marker `[PANEL-DRIVEN REPAIR — 2026-08-08, from the Kimi addendum, clerk-verified against the model]`, docs/phase-0-prereg-amendment-3.md:665-673; docs/phase-0-prereg-amendment-3.md:832] [RULED — §12 C-08, A7 §A7.6] |
| R-4.37 | Issuance is not complete until the anchor is | [REGISTERED A1 P5 corollary, docs/phase-0-prereg-amendment-1.md:186-197] |
| R-4.38 | Confirmation vocabulary: the anchor transaction is included in | [REGISTERED A2 §A2.1, docs/phase-0-prereg-amendment-2.md:80-86] |
| R-4.39 | Issuance is complete only if `confirmed_at ≤ declared_issue_time | [REGISTERED A2 §A2.1, docs/phase-0-prereg-amendment-2.md:87-89] |
| R-4.40 | The issuer evaluates that conjunct as part of | [REGISTERED A2 §A2.1, docs/phase-0-prereg-amendment-2.md:91-98; authoritative prose repair REGISTERED A3 §A3.7.3, docs/phase-0-prereg-amendment-3.md:654-663] |
| R-4.41 | The three conjuncts are `declared_issue_time − ε ≤ | [REGISTERED A2 §A2.2, docs/phase-0-prereg-amendment-2.md:218-224] |
| R-4.42 | The model convention pin is `DepthK = k | [REGISTERED A2 §A2.1, docs/phase-0-prereg-amendment-2.md:208-214] |
| R-4.43 | As modelled, the Ship guard is `~shipped /\ | [MODELLED Bridge, formal/tla/P5cP5P6_Bridge.tla:145-153, 168-178] |
| R-4.44 | The pin is checked, not assumed: `PinAgreement == | [MODELLED Bridge, formal/tla/P5cP5P6_Bridge.tla:26-30, 188-192] |
| R-4.45 | Wall time governs the attempt lifecycle: the service | [RULED (author) 2026-07-21 clock roles, registered A2 §A2.1, docs/phase-0-prereg-amendment-2.md:106-113] |
| R-4.46 | No global bound on the backward observation lag | [REGISTERED A2 §A2.1, docs/phase-0-prereg-amendment-2.md:113-130] |
| R-4.47 | Timeliness is latched at eligibility; eligibility observed at | [RULED, registered A2 §A2.1, docs/phase-0-prereg-amendment-2.md:130-135, 150-160] [SETTLED — §12 S-12] |
| R-4.48 | If the predicate fails at issuance time, the | [REGISTERED A2 §A2.1, docs/phase-0-prereg-amendment-2.md:160-162] |
| R-4.49 | Re-issue uses a fresh declared time and re-anchors; | [REGISTERED A1 P5 corollary, docs/phase-0-prereg-amendment-1.md:186-197; A2 §A2.4, docs/phase-0-prereg-amendment-2.md:324-327] |
| R-4.50 | Reorg handling is scoped, not modelled: anchors at | [REGISTERED A1 §A1.6, docs/phase-0-prereg-amendment-1.md:500-511; MODELLED P5c, formal/tla/P5c_IssuanceProtocol.tla:83-86, 231-241; SCOPED-OUT Bridge, formal/tla/P5cP5P6_Bridge.tla:43-69] |
| R-4.51 | A discarded attempt's transaction confirming later confers nothing; | [REGISTERED A2 §A2.4, docs/phase-0-prereg-amendment-2.md:307-312; MODELLED P5c, formal/tla/P5c_IssuanceProtocol.tla:209-229] |
| R-4.52 | A miner may set `timestamp(h + k − | [REGISTERED A2 §A2.2, docs/phase-0-prereg-amendment-2.md:182-185] |
| R-4.53 | Issuance makes at most N attempts. Fail-closed means | [REGISTERED A2 §A2.3, docs/phase-0-prereg-amendment-2.md:252-262] |
| R-4.54 | Exhausting the attempts obligates the implementation to terminate | [REGISTERED A2 §A2.3, docs/phase-0-prereg-amendment-2.md:266-270] |
| R-4.55 | `MaxAttempts` is promoted from a state-space bound to | [REGISTERED A2 §A2.3, docs/phase-0-prereg-amendment-2.md:278-284] |
| R-4.56 | As modelled, there is no separately enabled `Refuse` | [MODELLED P5c, formal/tla/P5c_IssuanceProtocol.tla:199-207, 189-198] |
| R-4.57 | `RefusalLatched == _vars`; the latch proves logical persistence | [MODELLED P5c, formal/tla/P5c_IssuanceProtocol.tla:332-337, 47-61] |
| R-4.58 | The boundary race at `now = declared + | [MODELLED P5c, formal/tla/P5c_IssuanceProtocol.tla:248-259] |
| R-4.59 | Termination is a contract obligation on the implementation, | [REGISTERED A2 §A2.3, docs/phase-0-prereg-amendment-2.md:284-290] |
| R-4.60 | `REFUSED` latches atomically when A2.3's terminal condition occurs; | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:569-572] |
| R-4.61 | The same transition creates, as local durable state | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:572-581] |
| R-4.62 | The complete portable refusal record carries attempt identity, | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:576-578] |
| R-4.63 | Handoff state machine: the generating authority retains the | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:583-589] |
| R-4.64 | Failure and expiry are visible terminal dispositions, never | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:589-592] |
| R-4.65 | Publication is a separate state machine: `PENDING`; `PUBLISHED`, | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:599-602] |
| R-4.66 | Creating the commitment value is not publication, and | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:602-605] |
| R-4.67 | If the authority dies after the local refusal | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:623-632] |
| R-4.68 | The interval costs the auditability of the refusal, | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:632-637] |
| R-4.69 | Emission with verified handoff is the discharge moment; | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:592-597] [OPEN — §11 O-18] |
| R-4.70 | The retention horizon and the post-terminal minimization policy | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:583-592] [OPEN — §11 O-48] |
| R-4.71 | The extended atomic-entry invariant, "every transition entering `REFUSED` | [REGISTERED A3 §A3.9, docs/phase-0-prereg-amendment-3.md:814-831; tracker formal/PROPERTIES.md:48, 260] |
| R-4.72 | While the authority lives, the submitter and a | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:614-621] [OPEN — §11 O-18] |
| R-4.73 | Refusal reporting is issuance-time operational machinery, not §A3.5 | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:616-619] |
| R-4.74 | A shipped receipt contains exactly one anchor proof | [REGISTERED A2 §A2.4, docs/phase-0-prereg-amendment-2.md:299-307] |
| R-4.75 | The txid is an identity/coherence handle, not by | [REGISTERED A2 §A2.4, docs/phase-0-prereg-amendment-2.md:299-307] |
| R-4.76 | The txid necessarily lives in the bundle outside | [REGISTERED A2 §A2.4, docs/phase-0-prereg-amendment-2.md:321-323] |
| R-4.77 | An anchor not shipped inside a receipt confers | [REGISTERED A2 §A2.4, docs/phase-0-prereg-amendment-2.md:307-312] |
| R-4.77a | The §A3.7.3 panel-driven repair governs: the issuer ships | [RULED (author) 2026-09-14; instrument A7 §A7.6, PROPOSED; §12 C-08. A7 reads the author's "burial death" as "burial depth", the `DepthK` conjunct of the bridge's `Ship` guard] |
| R-4.78 | No verifier policy, and no downstream marketplace rule, | [REGISTERED A2 §A2.4, docs/phase-0-prereg-amendment-2.md:327-333] [RULED — §12 C-06, A7 §A7.4] |
| R-4.79 | As modelled, a shipped receipt satisfies `shipped => | [MODELLED P5c, formal/tla/P5c_IssuanceProtocol.tla:288-303] |
| R-4.80 | As modelled at the seam, `shipped => VerdictValid(declared, | [MODELLED Bridge, formal/tla/P5cP5P6_Bridge.tla:194-207] [SETTLED — §12 S-10] |
| R-4.81 | Cryptographic validity alone confers no protocol standing. Any | [REGISTERED A3 §A3.7.1, docs/phase-0-prereg-amendment-3.md:531-535] |
| R-4.82 | The terminal lineage record (TLR) is the selected | [RULED (ADOPTED author) 2026-08-31, entered 2026-09-04, formal/spike/standing-probe/DECISION.md:3-26, 378-398] |
| R-4.83 | The probe's TLR is signed by the entitled | [PROPOSED (probe scoring draft; DECISION.md:28 retains "Status: PROPOSED — scoring draft, nothing decided."), formal/spike/standing-probe/DECISION.md:61-67] |
| R-4.84 | The TLR must be handle-bound, not ordinal-bound: the | [PROPOSED (probe scoring draft, gate G1; DECISION.md:28), formal/spike/standing-probe/DECISION.md:68-71] |
| R-4.85 | One signing act at terminal disposition produces the | [RULED (ADOPTED author) 2026-08-31, text adopted 2026-09-04, formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:96-116] |
| R-4.86 | At terminal disposition the issuer submits the TLR's | [RULED (ADOPTED author) 2026-09-04, formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:22-47] |
| R-4.87 | The anchor bounds *when* standing evidence could have | [RULED, formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:48-54] |
| R-4.88 | (i) A second anchoring event per issuance at | [RULED (ADOPTED author) 2026-09-04, formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:56-81] |
| R-4.89 | Internally inconsistent standing evidence yields `UNVERIFIABLE` with `STANDING_EVIDENCE_MALFORMED` | [RULED (ADOPTED author) 2026-09-04, formal/spike/first-link/DECISION.md:834-847] |
| R-4.90 | S1 lineage-present and the artifact is the shipped | [DECIDED 2026-08-12 and RULED 2026-09-04, formal/spike/first-link/DECISION.md:790-832] [RULED — §12 C-10, A7 §A7.7] |
| R-4.91 | The TLR is carried, not maintained; the service's | [RULED (ADOPTED author) at adoption; the wording at :386-390 is the collaborator's record of the author's in-session resolution, his own quoted words there being "Item 5 adopted.", formal/spike/standing-probe/DECISION.md:130-140, 386-390] |
| R-4.92 | The TLR does not detect equivocation: two TLRs | [PROPOSED (probe scoring draft, gate G4; DECISION.md:28), formal/spike/standing-probe/DECISION.md:78-82] |
| R-4.93 | Whether an issuer holding two identities on one | [REGISTERED A5 §A5.6, docs/phase-0-prereg-amendment-5.md:214-219] [OPEN — §11 O-36] |
| R-4.94 | The predeclared successor slot will be registered; the | [RULED (author) 2026-09-04, DOCKET 25, docs/band-1-docket.md:355-384; formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:159-206] [OPEN — §11 O-10] |
| R-4.95 | The TLR chains attempts within one issuance, backward; | [RULED, formal/spike/standing-probe/DECISION.md:344-366] |
| R-4.96 | As adopted with the selection, the log-and-receipt enrichment | [RULED (ADOPTED author) sub-ruling 5, formal/spike/standing-probe/DECISION.md:378-384; the fuller "remains available as a separately registered, never-load-bearing option per issuance class" at :313-321 sits under "RECOMMENDED (not adopted, and carrying the scorer's non-blindness)", and the composition wording at :185-195 is labelled "an input to the rule-3 fork, not a selection"] |
| R-4.97 | No §A3.5 tending obligation falls on the issuer | [REGISTERED A3 §A3.5, docs/phase-0-prereg-amendment-3.md:384-405; A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:616-619] |
| R-4.98 | What issuance owes §A3.5 is the bundle's fixed | [REGISTERED A3 §A3.5, docs/phase-0-prereg-amendment-3.md:453-458] |
| R-4.99 | The bundle's fixed floor ships the canary vector: | [REGISTERED A3 §A3.6.2, docs/phase-0-prereg-amendment-3.md:517-520] |
| R-4.100 | Tending health never changes a receipt's P4 verdict | [REGISTERED A3 §A3.5, docs/phase-0-prereg-amendment-3.md:418-419] |
| R-4.101 | The cadence parameter lives in each custodial policy | [RULED A3 §A3.5, docs/phase-0-prereg-amendment-3.md:447-452] [OPEN — §11 O-47] |
| R-4.102 | The base protocol does not require public disclosure | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:639-642] |
| R-4.103 | The commitment construction must resist practical guessing or | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:648-650] |
| R-4.104 | The commitment corroborates a disclosed record and does | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:650-653] [OPEN — §11 O-07] |
| R-4.105 | The publication channel must declare its survival, availability, | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:605-612] |
| R-4.106 | Tessera does not maintain a foundational auditor-membership registry: | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:642-648] |
| R-5.1 | The verdict is a pure function of the | [REGISTERED A1 §A1.2 P9, docs/phase-0-prereg-amendment-1.md:278-281] |
| R-5.2 | An attestation must verify with the service dead: | [REGISTERED prereg §4.4, docs/phase-0-prereg.md:519-525] |
| R-5.3 | If the verifier requires anything from an optional | [RULED (author) 2026-09-06, docs/band-1-docket.md:520-530] [RULED A4 §A4.6, docs/phase-0-prereg-amendment-4.md:176-182] |
| R-5.4 | The bundle supplies, at minimum: the framed bytes | [REGISTERED A1 §A1.5, docs/phase-0-prereg-amendment-1.md:430-448; A2 §A2.2, docs/phase-0-prereg-amendment-2.md:236-244, :299-307; A3 §A3.4/§A3.9, docs/phase-0-prereg-amendment-3.md:290-304, :754-759] |
| R-5.5 | The declared policy supplies the waiver set. Only | [REGISTERED A1 §A1.2.1, docs/phase-0-prereg-amendment-1.md:319-323] |
| R-5.6 | The waivable P10 item is bounded to fewer, | [REGISTERED A3 §A3.2, docs/phase-0-prereg-amendment-3.md:139-145] |
| R-5.7 | No policy may waive canonical-byte integrity (P1, P8), | [REGISTERED A1 §A1.2.1, docs/phase-0-prereg-amendment-1.md:309-317] |
| R-5.8 | The trust configuration is distributed with the verifier, | [REGISTERED A1 §A1.5, docs/phase-0-prereg-amendment-1.md:459-469 — these lines register only the archived historical trust-anchor store and its distribution with the verifier; δ and ε as verifier-owned are A1 §A1.2 P5, docs/phase-0-prereg-amendment-1.md:173-184. The authority channels' public keys and `k` as members of the trust configuration appear only in the modelled probe enumeration below, not in registered text] [MODELLED standing probe Q6: "Pre-bundle inputs: trust configuration only (channel public keys, `k`, `δ`). Everything else read from the bundle", formal/spike/standing-probe/RESULTS-PROBE.md:41] |
| R-5.9 | δ and ε belong to the verifier, not | [REGISTERED A1 §A1.2 P5, docs/phase-0-prereg-amendment-1.md:173-177] [MODELLED P5/P6 `ReceiptIndependence`, formal/tla/P5P6_TemporalRevocation.tla:201-221] |
| R-5.10 | A verifier MUST NOT consume: any live DNS | [REGISTERED prereg §4.4, docs/phase-0-prereg.md:527-535; A1 §A1.5, docs/phase-0-prereg-amendment-1.md:434-438; A3 §A3.5, docs/phase-0-prereg-amendment-3.md:415-419, :700-702] [REGISTERED A1 §A1.2 P5, docs/phase-0-prereg-amendment-1.md:173-177, for the receipt-declared tolerance; A4 §A4.6, docs/phase-0-prereg-amendment-4.md:181-182, for the log ("An enumeration or observability API may feed a log and may never feed a verdict.")] [REGISTERED A5 §A5.1's three stateful verifiers `LIVE_FALLBACK`, `LIVE_FAILCLOSED`, `REPLAY_LATCH`, docs/phase-0-prereg-amendment-5.md:65-80 — those lines report what the two-machine vector fails to catch; they state no prohibition. "Any verifier-local history of prior evaluations" has no registered prohibition sentence of its own and rests on P9's purity clause] |
| R-5.11 | Evaluation of waived evidence is bounded by the | [RULED A5 §A5.3, docs/phase-0-prereg-amendment-5.md:150-153] |
| R-5.12 | Custodial health and tending state are not inputs | [REGISTERED A3 §A3.5/§A3.8, docs/phase-0-prereg-amendment-3.md:418-419, :700-702] |
| R-5.13 | A manifest entry expressed as a reference is | [RULED (author) 2026-09-14; instrument A7 §A7.2, PROPOSED; R-3.31a] [RULED — §12 C-04, A7 §A7.2] |
| R-5.14 | The four verdicts partition all outcomes; the procedure | [REGISTERED A1 §A1.2 P4, docs/phase-0-prereg-amendment-1.md:152-157] [RULED A4 §A4.2 "required" qualifier, docs/phase-0-prereg-amendment-4.md:100-109] |
| R-5.15 | Each layer of a wrapped package is evaluated | [REGISTERED A3 §A3.2 item 4, docs/phase-0-prereg-amendment-3.md:158-164] |
| R-5.16 | No stage order may make the verdict depend | [RULED A4 §A4.2, docs/phase-0-prereg-amendment-4.md:88-98] |
| R-5.17 | The accepted domain is closed by explicit rejection: | [REGISTERED A1 §A1.2 P8, docs/phase-0-prereg-amendment-1.md:264-273] |
| R-5.18 | No inference, negotiation, normalization, or fallback is permitted | [ADOPTED (author) 2026-08-13, formal/spike/first-link/DECISION.md:366-383; the source declines the RULED label at :369-372] |
| R-5.34 | The chain is quantified per contributing layer, and | [REGISTERED A3 §A3.2 item 4, docs/phase-0-prereg-amendment-3.md:158-164] |
| R-5.19 | All three temporal conjuncts are evaluated together. Evaluation | [REGISTERED A3 §A3.7.3, docs/phase-0-prereg-amendment-3.md:654-663] [MODELLED bridge `Ship` guard, formal/tla/P5cP5P6_Bridge.tla:168-178] |
| R-5.20 | A verifier may choose stricter bounds; no degraded | [REGISTERED A1 §A1.2 P5, docs/phase-0-prereg-amendment-1.md:177-184; A2 §A2.2, docs/phase-0-prereg-amendment-2.md:245-248] |
| R-5.21 | `VALID_STRICT` requires `key_authorized(declared_issue_time)` and no revocation effective at | [REGISTERED A1 §A1.2 P6, docs/phase-0-prereg-amendment-1.md:199-233] [SETTLED — §12 S-15, A1 P6 as clarified by A4 §A4.3; see R-5.23] |
| R-5.22 | The registered sentence, as written by A4 §A4.3, | [RULED A4 §A4.3, docs/phase-0-prereg-amendment-4.md:111-123] [MODELLED `AuthorizedThroughWindow == revoked > declared /\ revoked > anchor`, formal/tla/P5P6_TemporalRevocation.tla:142-149; `AuthorizedAtDeclared == StrictAccept => declared < revoked`, :223-233] |
| R-5.23 | The interval rule is deliberately stricter than point | [REGISTERED A1 §A1.2 P6, docs/phase-0-prereg-amendment-1.md:199-233] [MODELLED `HonestCostIsExactlyTheWindow`, formal/tla/P5P6_TemporalRevocation.tla:235-245] [SETTLED — §12 S-15, A1 P6 as clarified by A4 §A4.3] |
| R-5.24 | Revocation is terminal: a revoked key is never | [REGISTERED A1 §A1.2 P6, docs/phase-0-prereg-amendment-1.md:216-224] |
| R-5.25 | The verdict is computed by, in order: (1) | [MODELLED P4 `VerdictFor(W)`, formal/tla/P4_VerifierStates.tla:94-105] |
| R-5.26 | When one required check fails and another cannot | [RULED (author) A4 §A4.2, docs/phase-0-prereg-amendment-4.md:88-98] [MODELLED branch order, formal/tla/P4_VerifierStates.tla:96-99] |
| R-5.27 | `INVALID` dominates `UNVERIFIABLE` in the binding-form required set | [ADOPTED (author), formal/spike/first-link/DECISION.md:385-391, inside the block the source labels ADOPTED rather than RULED (:369-372)] |
| R-5.28 | The verdict function satisfies, for every check-outcome assignment | [MODELLED formal/tla/P4_VerifierStates.tla:111-175] |
| R-5.29 | `VALID_DEGRADED` arises only from an explicit, nonempty waiver | [REGISTERED A1 §A1.2/§A1.2.1, docs/phase-0-prereg-amendment-1.md:152-157, :319-327] [MODELLED `DegradedNeedsExplicitWaiver`, formal/tla/P4_VerifierStates.tla:140-143] |
| R-5.30 | A waived check may hold any status, including | [RULED A5 §A5.2, docs/phase-0-prereg-amendment-5.md:93-121] [MODELLED `ExactDegraded`, formal/tla/P4_VerifierStates.tla:174-175] |
| R-5.31 | The registered cost of R-5.30 is recorded: a | [REGISTERED A5 §A5.2, docs/phase-0-prereg-amendment-5.md:123-132] |
| R-5.32 | In degraded mode the verifier's job is to | [RULED A4 §A4.6, docs/phase-0-prereg-amendment-4.md:156-171] |
| R-5.33 | R-5.32 is bounded by: "Only losses permitted by | [RULED A5 §A5.7, docs/phase-0-prereg-amendment-5.md:221-241] |
| R-5.35 | Every valid verdict requires at least one continuous | [REGISTERED A3 §A3.2, docs/phase-0-prereg-amendment-3.md:102-121] |
| R-5.36 | Counted floors are prohibited: "≥1 accepted signature AND | [REGISTERED A3 §A3.2, docs/phase-0-prereg-amendment-3.md:131-137] |
| R-5.37 | Every symbolic path that stops short of the | [RULED (author) 2026-08-29, formal/suite/ENUMERATION.md:410-418] |
| R-5.38 | Verification yields one of `VALID_STRICT`, `VALID_DEGRADED(policy=...)`, `INVALID`, or | [REGISTERED prereg §4.6, docs/phase-0-prereg.md:555-562] [MODELLED `Verdicts`, formal/tla/P4_VerifierStates.tla:70] |
| R-5.39 | Every `VALID_DEGRADED` verdict records the precise waived check | [REGISTERED A1 §A1.2.1, docs/phase-0-prereg-amendment-1.md:325-327] |
| R-5.40 | For each waived check the record holds both | [RULED A5 §A5.3, docs/phase-0-prereg-amendment-5.md:134-154] [RULED — §12 C-05, A7 §A7.3] |
| R-5.41 | The degraded-record format is an H1a obligation. | [OPEN — §11 O-06] [DOCKET 28 — candidate, docs/band-1-docket.md:62-66] |
| R-5.42 | The base assessment reports each layer's result without | [RULED A3 §A3.2 item 4, docs/phase-0-prereg-amendment-3.md:161-164] |
| R-5.43 | The base assessment is an unsigned, reproducible computation. | [RULED A3 §A3.8, docs/phase-0-prereg-amendment-3.md:686-689, :722-736] |
| R-5.44 | The base assessment carries at least: identities of | [REGISTERED A3 §A3.8, docs/phase-0-prereg-amendment-3.md:689-700] |
| R-5.45 | The scope-bearing dimensions the record names are: `verification` | [REGISTERED A3 §A3.7.1/§A3.8, docs/phase-0-prereg-amendment-3.md:541-549, :700-702] |
| R-5.46 | Standing reports at least `ESTABLISHED`, `ABSENT`, or `UNVERIFIABLE`, | [REGISTERED A3 §A3.7.1, docs/phase-0-prereg-amendment-3.md:541-546] [RULED A3 §A3.7.1, docs/phase-0-prereg-amendment-3.md:550-557] [MODELLED `event StandingReport(bitstring, bitstring, pkey, bitstring, bitstring).`, whose comment reads "verdict, reason, key, tuple, derived identity", formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:175-176] |
| R-5.47 | No unqualified aggregate checkmark is part of the | [REGISTERED A3 §A3.8, docs/phase-0-prereg-amendment-3.md:677-684, :703-704] |
| R-5.48 | Every Tessera-controlled or conforming third-party surface that renders | [REGISTERED A3 §A3.8, docs/phase-0-prereg-amendment-3.md:706-710] [DOCKET 11 — candidate, docs/band-1-docket.md:78-82] |
| R-5.49 | A party needing portable attribution, evaluation-time evidence, or | [REGISTERED A3 §A3.8, docs/phase-0-prereg-amendment-3.md:712-720] |
| R-5.50 | Reason-carrying output is a conformance requirement, not a | [RULED (author) 2026-08-12, formal/spike/first-link/DECISION.md:748-768] |
| R-5.51 | S2, S3 and S4 MUST return pairwise distinct | [RULED first-link/DECISION.md:806-810, :818-832] [MODELLED `ReasonCollapsed` judge over `PATH_S2`/`PATH_S3`/`PATH_S4`, formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:392-396] |
| R-5.52 | The standing report has one output vocabulary — | [RULED (author) 2026-09-14; instrument A7 §A7.7, PROPOSED] [RULED — §12 C-10, A7 §A7.7] [OPEN — §11 O-75] |
| R-5.53 | Tessera attests the identity of the framed bytes | [REGISTERED A3 §A3.1, docs/phase-0-prereg-amendment-3.md:61-66] |
| R-5.54 | Tessera does not decide whether the adjudicator should | [RULED A4 §A4.6, docs/phase-0-prereg-amendment-4.md:156-182] |
| R-5.55 | `VALID_STRICT` attests envelope soundness, never payload truth. No | [REGISTERED A3 §A3.8, docs/phase-0-prereg-amendment-3.md:677-684] |
| R-5.56 | Standing is orthogonal: relying-party policy decides whether `verification` | [REGISTERED A3 §A3.7.1, docs/phase-0-prereg-amendment-3.md:546-549] [RULED A3 §A3.7.1, docs/phase-0-prereg-amendment-3.md:550-557] |
| R-5.57 | Whether a replay is appropriate is caller policy: | [REGISTERED A3 §A3.1, docs/phase-0-prereg-amendment-3.md:68-74] |
| R-5.58 | Misissuance (an authorized or compromised issuer path signing | [REGISTERED prereg §3.1, docs/phase-0-prereg.md:388-404; A1 §A1.3, docs/phase-0-prereg-amendment-1.md:347-355] |
| R-5.59 | Equivocation by the entitled key is not detected | [MODELLED standing-probe gate G4, formal/spike/standing-probe/DECISION.md:78-82] [MODELLED S-STANDING, formal/suite/s-standing/RESULTS.md:540-556] |
| R-5.60 | The relying-party story is the human-facing statement of | [REGISTERED A3 §A3.1.4/§A3.8, docs/phase-0-prereg-amendment-3.md:89-96, :736-737] |
| R-5.61 | The log-versus-verdict boundary; that any service-side enumeration API | [PROPOSED formal/COVERAGE-MAP.md row 14] [OPEN — §11 O-72] |
| R-5.62 | No verifier policy, and no downstream marketplace rule, | [REGISTERED A2 §A2.4, docs/phase-0-prereg-amendment-2.md:327-333] [RULED — §12 C-06, A7 §A7.4] |
| R-6.1 | The registered standing invariant, in full: "Cryptographic validity | [REGISTERED A3 §A3.7.1, docs/phase-0-prereg-amendment-3.md:530-535] |
| R-6.2 | Standing is "an **orthogonal assessment dimension**, not a | [REGISTERED A3 §A3.7.1, docs/phase-0-prereg-amendment-3.md:541-546] |
| R-6.3 | Verdict and standing are reported separately and never | [REGISTERED A3 §A3.7.1, docs/phase-0-prereg-amendment-3.md:545-548] |
| R-6.4 | Standing "is not a member of the A1.2.1 | [REGISTERED A3 §A3.7.1, marker `[PANEL-DRIVEN CLARIFICATION — 2026-08-08, from the Kimi cold read]` — not an author decision, docs/phase-0-prereg-amendment-3.md:550-557] |
| R-6.5 | Protocol standing is one of the base assessment's | [REGISTERED A3 §A3.8, docs/phase-0-prereg-amendment-3.md:690-698; :703-704] |
| R-6.5a | The base assessment carrying the standing field "is | [RULED (author) 2026-08-08, docs/phase-0-prereg-amendment-3.md:686-689; :722-736] |
| R-6.5b | No surface may collapse "envelope verification, protocol standing, | [REGISTERED A3 §A3.8, docs/phase-0-prereg-amendment-3.md:677-684; :706-710] |
| R-6.6 | The mechanism discharging the invariant "must be testable | [REGISTERED A3 §A3.7.1, docs/phase-0-prereg-amendment-3.md:524-530; :536-540] |
| R-6.7 | Standing and A2.4 coexist without amendment: for an | [RULED (author) 2026-08-12, formal/spike/first-link/DECISION.md:700-733; REGISTERED A2 §A2.4, docs/phase-0-prereg-amendment-2.md:307-316] |
| R-6.8 | The terminal lineage record is the selected standing-evidence | [RULED (ADOPTED author) 2026-08-31, entered 2026-09-04, author commit `fbf6387`, formal/spike/standing-probe/DECISION.md:3-13; :378-398] [SETTLED — §12 S-13] |
| R-6.9 | The probe's TLR "is signed by the entitled | [PROPOSED (probe scoring draft, gate G0; DECISION.md:28 retains "Status: PROPOSED — scoring draft, nothing decided."), formal/spike/standing-probe/DECISION.md:61-67] |
| R-6.10 | The TLR is handle-bound, not ordinal-bound. Registered polarity: | [PROPOSED (probe scoring draft, gate G1, evidential; DECISION.md:28), formal/spike/standing-probe/DECISION.md:68-71] |
| R-6.11 | The standing report is offline: "Zero inputs beyond | [PROPOSED (probe scoring draft, gate G2; DECISION.md:28), formal/spike/standing-probe/DECISION.md:72-74] |
| R-6.12 | The TLR travels in the bundle. Custody of | [RULED (ADOPTED author) at adoption; the wording at :386-390 is the collaborator's record of the author's in-session resolution, his own quoted words there being "Item 5 adopted.", formal/spike/standing-probe/DECISION.md:130-140; :386-390] |
| R-6.13 | One signing act at terminal disposition produces the | [RULED (ADOPTED author) 2026-08-31 / text 2026-09-04, formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:96-116; DECISION.md:327-338] |
| R-6.14 | "The TLR is anchored: at terminal disposition the | [RULED (ADOPTED author) 2026-09-04, formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:22-47] |
| R-6.15 | "the anchor bounds **when** standing evidence could have | [RULED (ADOPTED author) 2026-09-04, formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:48-54] |
| R-6.16 | A second anchoring event per issuance occurs at | [RULED (ADOPTED author) 2026-09-04, formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:56-64] |
| R-6.16a | Where a bundle ships before confirmation it carries | [RULED (ADOPTED author) 2026-09-04, formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:64-81] |
| R-6.17 | Bare "within δ" is forbidden in registered text: | [RULED (author) 2026-09-04, formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:223-241] |
| R-6.18 | Two defined outcomes are added "in the first-link |  |
| R-6.19 | "the standing path checks that the presented authority | [RULED (ADOPTED author) A5 §A5.6, docs/phase-0-prereg-amendment-5.md:202-219] |
| R-6.20 | The forward-link / predeclared successor slot will be | [RULED (author) 2026-09-04, formal/spike/standing-probe/DECISION.md:368-377; formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:182-206; docs/band-1-docket.md:355-383] |
| R-6.21 | The forward identifier "has to be inside the | [RULED (author) 2026-09-04, docs/band-1-docket.md:378-385] |
| R-6.22 | As adopted with the selection, the log-and-receipt enrichment | [RULED (ADOPTED author) sub-ruling 5, formal/spike/standing-probe/DECISION.md:378-384; scorer wording PROPOSED, :185-195, :313-321] |
| R-6.22a | The transparency witness survived the gates but was | [PROPOSED (probe scoring draft; DECISION.md:28) — candidate not selected, formal/spike/standing-probe/DECISION.md:144-183, :197-204] |
| R-6.22b | Two further outcomes for the optional witness enrichment | [PROPOSED (unadopted), formal/spike/standing-probe/DECISION.md:166-168] |
| R-6.23 | The standing path consumes the bundle tuple `(t, | [MODELLED S-STANDING, formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:318-324] |
| R-6.24 |  |  |
| R-6.24a | Internally inconsistent standing evidence — "a terminal | [REGISTERED SC-3, formal/spike/first-link/DECISION.md:834-843; adopted text formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:146-151] |
| R-6.25 | The entitled-key check is inside the standing path | [PROPOSED — the source is headed "Carry note (drafter, not an amendment)", and `ENUMERATION.md` amendment note 4 carrying it is headed "(clerk; PROPOSED; …)"; the MUST wording is the drafter's, not the author's. formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:210-219; formal/suite/ENUMERATION.md:486, :502-509] |
| R-6.26 | The §A5.6 pin is placed after the `noTLR`, | [MODELLED S-STANDING, formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:343-352; :77; corrections verified formal/suite/s-standing/RESULTS.md:1335-1348, :1350-1370] |
| R-6.27 | "The standing path checks `attemptCore(=t, ppfS, sgS, declS) | [MODELLED S-STANDING (boundary, 2026-09-12 cross-family review), formal/suite/s-standing/RESULTS.md:1270-1280] |
| R-6.28 | The envelope path is carried in the model | [MODELLED S-STANDING, formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:365-378] |
| R-6.29 | The model's producer ledger entry P-2 makes the | [MODELLED S-STANDING, formal/suite/s-standing/RESULTS.md:454-467] |
| R-6.29a | An `ESTABLISHED` report against an honest entitled key | [MODELLED S-STANDING, formal/suite/s-standing/RESULTS.md:434-453] |
| R-6.29b | The §A5.6 alias judge is "INSTRUMENTATION, not a | [MODELLED S-STANDING (SS.Q6), formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:398-406] |
| R-6.29c | The wrapper-shaped outer artifact is built by no | [MODELLED S-STANDING, formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:125-128; formal/suite/s-standing/RESULTS.md:395-431] |
| R-6.30 | Registered standing test conditions, with the reason code |  |
| R-6.31 | "S2, S3, and S4 all return 'no standing' | [REGISTERED / dated amendment, formal/spike/first-link/DECISION.md:804-810; :828-832] |
| R-6.32 | "the verdict is always 'no protocol standing,' and | [RULED (author) 2026-08-12, formal/spike/first-link/DECISION.md:748-768] |
| R-6.33 | "Per the DeepSeek panel criterion, **every** standing / | [REGISTERED (exit condition 3), formal/spike/first-link/DECISION.md:790-796] |
| R-6.34 | All conditions are evaluated "with the standing result | [REGISTERED (A3 §A3.9; docket 16), formal/spike/first-link/DECISION.md:812-816; formal/spike/standing-probe/DECISION.md:74-77] |
| R-6.35 | One vocabulary, with the S-series mapped onto | [REGISTERED, formal/spike/first-link/DECISION.md:798-801, :838-847; docs/phase-0-prereg-amendment-3.md:541-546; formal/spike/standing-probe/DECISION.md:61-71, :138-141] [RULED (author) 2026-09-14; instrument A7 §A7.7, PROPOSED] [RULED — §12 C-10, A7 §A7.7] |
| R-6.36 | `STANDING_EVIDENCE_MISMATCH` and `STANDING_EVIDENCE_SIGNATURE_INVALID` are emitted by the modelled | [PROPOSED (probe scoring draft, probe-recorded; DECISION.md:28), formal/spike/standing-probe/DECISION.md:61-67, :68-71, :119; MODELLED S-STANDING, formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:144-155] [OPEN — §11 O-75] |
| R-6.36a | The registered concern is testability, not entitlement: the | [DECIDED (first-link DECISION.md, entered by the author 2026-08-13 at `459aff0`), formal/spike/first-link/DECISION.md:735-746] |
| R-6.36b | Both obligations stand together: build the reason-code collapsing | [PROPOSED (clerk disposition B9; no author ruling on this item is recorded) ROUTED 2026-09-06, formal/suite/ROUTED-2026-09-06.md:158-161; MODELLED S-STANDING, formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:156-159, :392-396] |
| R-6.37 | The model's report event is the family's output | [MODELLED S-STANDING, formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:175-176, :208-218, :392-396; quoted sentence formal/suite/s-standing/RESULTS.md:274-280] |
| R-6.38 | The TLR does not detect equivocation: "two TLRs | [PROPOSED (probe scoring draft, gate G4 content half; DECISION.md:28), formal/spike/standing-probe/DECISION.md:78-82; :108-115] |
| R-6.39 | Except for the F1 malformed case cured by | [PROPOSED (probe scoring draft, C3; DECISION.md:28), formal/spike/standing-probe/DECISION.md:138-141] |
| R-6.40 | The modelled lineage is exactly two entries (`lineage2`); | [MODELLED S-STANDING, formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:130-136; formal/suite/s-standing/RESULTS.md:540-556] [OPEN — §11 O-76] |
| R-6.41 | Nothing temporal is represented in the symbolic standing | [MODELLED S-STANDING, formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv:341-342; formal/suite/s-standing/RESULTS.md:484-536] [OPEN — §11 O-77] |
| R-6.42 | §A5.6 does not decide "whether an issuer holding | [RULED (ADOPTED author) A5 §A5.6 (non-decision), docs/phase-0-prereg-amendment-5.md:214-219] [OPEN — §11 O-36] |
| R-6.43 | In degraded mode with the sole authority channel | [MODELLED S-STANDING (ledger P-3), formal/suite/s-standing/RESULTS.md:468-482; RULED (author) A4 §A4.6 (section header reads "RULED (author)"; signing commit `5188e7a`), docs/phase-0-prereg-amendment-4.md:156-167] |
| R-6.44 | Which identity a wrapped bundle's standing binds to | [MODELLED S-STANDING (not-covered), formal/suite/s-standing/RESULTS.md:540-556; REGISTERED A3 §A3.9, docs/phase-0-prereg-amendment-3.md:779-795] |
| R-7.1 | The claim "attestation survives Tessera's termination" is split | [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:261-278] |
| R-7.2 | For every artifact class Tessera produces, survivability guarantees | [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:280-288] |
| R-7.3 | The bundle carries: an unambiguous verification-spec identifier "**and | [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:290-304] |
| R-7.4 | "A member of the Designated Community — human, | [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:305-320] |
| R-7.5 | "The century horizon is aspirational, not a guarantee | [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:322-326] |
| R-7.6 | A Designated Community member can, using ordinary documented | [RULED (author) 2026-08-08, docs/phase-0-prereg-amendment-3.md:328-341] |
| R-7.7 | Tessera owns the closure over framing, canonicalization, signatures, | [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:342-352] |
| R-7.7a | For mechanisms chosen by an issuer or deployment | [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:353-356] [RULED — §12 C-07, A7 §A7.5] |
| R-7.7b | Submitter-supplied schemas, vocabularies, software, ontologies, codecs or contextual | [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:357-364] |
| R-7.8 | "Tessera-authored procedure and conformance artifacts are embedded; external | [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:350-352; :366-370] |
| R-7.9 | The dead-service test (P9: verify with Tessera unreachable) | [REGISTERED A3 §A3.4, docs/phase-0-prereg-amendment-3.md:371-379] |
| R-7.10 | Candidate, not registered: a declared per-bundle byte budget | [DOCKET 9 — candidate, not registered, docs/band-1-docket.md:54-56] |
| R-7.11 | Candidate, not registered: the embedded verification specification executable-in-principle, | [DOCKET 10 — candidate, not registered, docs/band-1-docket.md:57-61] |
| R-7.12 | Candidate, not registered: the historical trust-anchor store as | [DOCKET 8 — candidate, not registered, docs/band-1-docket.md:50-53; REGISTERED A1 §A1.5, docs/phase-0-prereg-amendment-1.md:459-469] |
| R-7.13 | "`REFUSED` latches atomically when A2.3's terminal condition occurs; | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:569-581] |
| R-7.14 | "The generating authority retains the complete record until | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:583-592] |
| R-7.15 | "Emission with verified handoff is the discharge moment: | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:592-597] [OPEN — §11 O-18] |
| R-7.16 | "`PENDING`; `PUBLISHED`, only on acknowledgment from the declared | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:599-605] |
| R-7.17 | The publication channel "must declare its survival, availability, | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:605-612] |
| R-7.18 | If the authority dies after the local refusal | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:623-637] |
| R-7.18a | "While the authority lives, the submitter and a | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:614-621] [OPEN — §11 O-18] |
| R-7.18b | "The base protocol does not require public disclosure | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:639-648] [OPEN — §11 O-48] |
| R-7.18c | "The commitment construction must resist practical guessing or | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:648-653] [OPEN — §11 O-07] |
| R-7.18d | §A3.7.2 assigns A2.3's durability, retrievability and reporting obligations | [REGISTERED A3 §A3.10, docs/phase-0-prereg-amendment-3.md:852-864] |
| R-7.19 | Docket 17 records that items 13 to 16 | [DOCKET 17 — candidate, not registered, docs/band-1-docket.md:139-186] [OPEN — §11 O-42] |
| R-7.19a | The item is "the custody half of the | [DOCKET 17 — candidate, not registered, docs/band-1-docket.md:194-198] |
| R-7.20 | The answer "cannot be 'Tessera, in perpetuity'". "Discovery | [DOCKET 17 — candidate, not registered, docs/band-1-docket.md:163-173] |
| R-7.21 | With no form lifecycle or issuance-state distinction implemented, | [DOCKET 17 — candidate, not registered, docs/band-1-docket.md:199-208; DEFERRED docket 18] |
| R-7.22 | Candidate reading of DECISION-CRITERIA C2 as registered: "An | [DOCKET 24(a) — candidate, not registered, docs/band-1-docket.md:326-341] |
| R-7.23 | Candidate: anchoring standing evidence "bounds *when* each record | [DOCKET 24(b) — candidate, not registered, docs/band-1-docket.md:336-347] |
| R-7.24 | Candidate: a registered statement that third-party logs are | [DOCKET 27 — candidate, not registered, docs/band-1-docket.md:485-517] |
| R-7.25 | "the **verifier** is P9's pure function — bundle | [RULED (author) 2026-09-06 in substance, docs/band-1-docket.md:517-526] |
| R-7.26 | "Tending records custodial assessment, not an assumption that |  |
| R-7.27 | "Every outcome exposes the policy and version applied; | [REGISTERED A3 §A3.5, docs/phase-0-prereg-amendment-3.md:399-405] |
| R-7.28 | "Given an available monitoring clock and custodial record, | [REGISTERED A3 §A3.5, docs/phase-0-prereg-amendment-3.md:407-414] |
| R-7.29 | "Custodial-health monitoring and any relying party holding a | [REGISTERED A3 §A3.5, docs/phase-0-prereg-amendment-3.md:415-418] |
| R-7.30 | "Tending health therefore never changes a receipt's P4 | [REGISTERED A3 §A3.5 / §A3.8 / §A3.10, docs/phase-0-prereg-amendment-3.md:418-419; :702-704; :865-871] |
| R-7.31 | "The custodial policy declares its trigger classes, observation | [RULED (author) 2026-08-08, docs/phase-0-prereg-amendment-3.md:438-445] |
| R-7.32 | "The cadence parameter lives in each custodial policy | [RULED (author) 2026-08-08, docs/phase-0-prereg-amendment-3.md:447-452] [OPEN — §11 O-47] |
| R-7.33 | "Exact trigger expressions, cadence, clock, monitoring surface, and | [REGISTERED A3 §A3.5, docs/phase-0-prereg-amendment-3.md:419-423] [OPEN — §11 O-37] |
| R-7.34 | Candidates, not registered: observable deadlines carried on `ACTION_DUE`/`FAILED` | [DOCKET 13-16 — candidates, not registered, docs/band-1-docket.md:117-132] |
| R-7.34a | Conformance vectors are two layers: "a **fixed floor** | [REGISTERED A3 §A3.5, docs/phase-0-prereg-amendment-3.md:453-461] |
| R-7.34b | When an existing verifier fails a new challenge, | [REGISTERED A3 §A3.5, docs/phase-0-prereg-amendment-3.md:461-469] |
| R-7.35 | Refusal reporting "is issuance-time operational machinery, not §A3.5 | [REGISTERED A3 §A3.7.2, docs/phase-0-prereg-amendment-3.md:616-619] |
| R-7.36 | "The algorithm identifier and all parameters that affect | [REGISTERED A3 §A3.6, docs/phase-0-prereg-amendment-3.md:485-490] |
| R-7.37 | The location is pinned "inside the canonical payload | [RULED (author) 2026-08-08, docs/phase-0-prereg-amendment-3.md:491-502] [OPEN — §11 O-03] |
| R-7.38 | "`UNVERIFIABLE` for exactly one case — a well-formed, | [REGISTERED A3 §A3.6.2 (adopted, exact), docs/phase-0-prereg-amendment-3.md:503-508] [RULED — §12 C-07, A7 §A7.5] |
| R-7.39 | Required: "a software red-bar suite verifying the signing-provider | [REGISTERED A3 §A3.6, docs/phase-0-prereg-amendment-3.md:509-512] |
| R-7.40 | "one permanently reserved unrecognized algorithm identifier remains in | [REGISTERED A3 §A3.6, docs/phase-0-prereg-amendment-3.md:513-520] |
| R-7.41 | "The PQ signature implementation is deferred from the | [REGISTERED A3 §A3.6, docs/phase-0-prereg-amendment-3.md:473-480; REGISTERED prereg §4, docs/phase-0-prereg.md:339-345] |
| R-7.42 | "Hybrid classical+PQ dual signing is explicitly deferred to | [REGISTERED (deferral) A3 §A3.6, docs/phase-0-prereg-amendment-3.md:480-483] [OPEN — §11 O-13] |
| R-7.43 | Candidate, not registered anywhere in the record. The | [DOCKET 26 — candidate, not registered, docs/band-1-docket.md:386-410] |
| R-7.44 | Candidate rules under docket 26, neither agreed: (i) | [DOCKET 26 — candidate, not registered, docs/band-1-docket.md:411-418; :434-446] [OPEN — §11 O-19] |
| R-7.44a | What stands in docket 26 without collaborator objection: | [DOCKET 26 — candidate, not registered, docs/band-1-docket.md:429-433; :448-453] |
| R-7.44b | Recorded facts bearing on the governance premise: the | [DOCKET 26 — candidate, not registered, docs/band-1-docket.md:454-458; :470-475; :505-508] |
| R-7.45 | Renewal is RFC 4998 (ERS) renewal under an | [REGISTERED A3 §A3.4 claim 3, docs/phase-0-prereg-amendment-3.md:273-278] |
| R-7.46 | Old payloads are never re-signed: "a **superseding attestation | [REGISTERED prereg §4, docs/phase-0-prereg.md:339-355] |
| R-7.47 | The wrapper "commits to the inner package's **bytes**, | [REGISTERED prereg §4, docs/phase-0-prereg.md:356-364] |
| R-7.48 | Candidate: state that simple RFC 4998 timestamp renewal | [DOCKET 20 — candidate, not registered, docs/band-1-docket.md:269-282] |
| R-7.49 | Candidate, not registered: (a) that a renewal chain | [DOCKET 19 — candidate, not registered, docs/band-1-docket.md:245-267] [OPEN — §11 O-30] |
| R-7.50 | Candidate, not registered: "A wrap commits to the | [DOCKET 21 — candidate, not registered, docs/band-1-docket.md:284-292] |
| R-7.51 | Candidate, not registered: "cumulative depth from one custody | [DOCKET 22 — candidate, not registered, docs/band-1-docket.md:294-302] |
| R-7.52 | The renewal wrapper is ruled out for carrying | [REGISTERED prereg §4 + A3 §A3.8, docs/phase-0-prereg.md:356-364; docs/phase-0-prereg-amendment-3.md:712-720; DOCKET 23 — no change, docs/band-1-docket.md:303-320] |
| R-7.53 | Signer authority, key lifecycle and report policy for | [REGISTERED A3 §A3.8, docs/phase-0-prereg-amendment-3.md:718-720] |
| R-7.54 | The binding-form lifecycle and the reference-verifier obligation are | [DEFERRED docket 18, docs/band-1-docket.md:220-232, :202-208; RULED (author) 2026-08-13, formal/spike/first-link/DECISION.md:436-461, :946-955] |
| R-8.1 | δ and ε belong to the verifier, not | [REGISTERED A1 P5, docs/phase-0-prereg-amendment-1.md:173-177] |
| R-8.2 | A verifier may choose stricter bounds; no degraded | [REGISTERED A1 P5, docs/phase-0-prereg-amendment-1.md:177-184] |
| R-8.3 | δ, ε, k, N and S are ratified | [REGISTERED A1 P5, docs/phase-0-prereg-amendment-1.md:180-190; A2 §A2.1/§A2.3, docs/phase-0-prereg-amendment-2.md:106-113, 270-274; tracker formal/PROPERTIES.md:167-168] |
| R-8.4 | N attempts give a nominal lifecycle budget of | [REGISTERED A2 §A2.3, docs/phase-0-prereg-amendment-2.md:270-274] |
| R-8.5 | Bare "within δ" is forbidden in registered text; | [RULED (author) 2026-09-04, formal/spike/standing-probe/AMENDMENTS-2026-08-31.md:223-241] |
| R-8.6 | Custodial trigger expressions, cadence, clock, monitoring surface and | [REGISTERED A3 §A3.5, docs/phase-0-prereg-amendment-3.md:419-423] |
| R-8.7 | Nesting depth for wrappers is bounded by willingness | [REGISTERED prereg §3.1, docs/phase-0-prereg.md:352-355] |
| R-8.8 | `MaxSkew` in the slack modules is a declared | [MODELLED BridgeSlack header, formal/tla/P5cP5P6_BridgeSlack.tla:1-59] |
| R-8.9 | The strict default k = 6 (`DepthK = | [RULED (author) 2026-09-14; instrument A7 §A7.8, PROPOSED; §12 C-13] [OPEN — §11 O-44] |
| R-9.1 | Key material is never logged: not private keys, | [REGISTERED prereg §4.1, docs/phase-0-prereg.md:447-452] |
| R-9.2 | The canonical form is frozen and explicitly versioned: | [REGISTERED prereg §4.3, docs/phase-0-prereg.md:486-494] |
| R-9.3 | The canonical form binds to RFC 8785 (JCS); | [REGISTERED prereg §4.3, docs/phase-0-prereg.md:496-512] |
| R-9.4 | The claim is boundary-unambiguity only. No blanket "length-extension-resistant" | [REGISTERED prereg §4.3, docs/phase-0-prereg.md:514-517] [RULED — §12 C-03, A7 §A7.1] |
| R-9.5 | The verification path depends on zero service-side state. | [REGISTERED prereg §4.4, docs/phase-0-prereg.md:519-525] |
| R-9.6 | Verification yields a typed result, never a bare | [REGISTERED prereg §4.6, docs/phase-0-prereg.md:555-562] |
| R-9.7 | The red-bar suite's attacks are authored by a | [REGISTERED prereg §4.5, docs/phase-0-prereg.md:548-553] |
| R-9.8 | The service attests when it was last adversarially | [REGISTERED prereg §4.7, docs/phase-0-prereg.md:564-572] [OPEN — §11 O-45] |
| R-9.9 | The `canonical(payload) → bytes` function is the true | [REGISTERED prereg §3.1, docs/phase-0-prereg.md:413-415] |
| R-9.10 | The extractability boundary is not a design priority, | [RULED prereg §3.1, docs/phase-0-prereg.md:417-435] |
| R-9.11 | The commit-signing key is passphraseless with a declared | [REGISTERED prereg §4.2, docs/phase-0-prereg.md:454-469] |
| R-9.12 | Old payloads are never re-signed. A superseding attestation | [REGISTERED prereg §3.1, docs/phase-0-prereg.md:339-355] |
| R-9.13 | One permanently reserved unrecognized algorithm identifier remains in | [REGISTERED A3 §A3.6.2, docs/phase-0-prereg-amendment-3.md:513-520] |
| R-9.14 | Every row below whose provenance tag is REGISTERED | [REGISTERED A3 §A3.2 item 4, docs/phase-0-prereg-amendment-3.md:161-164; A3 §A3.8, docs/phase-0-prereg-amendment-3.md:703-704] |
| R-9.15 | Every implication-shaped invariant above is guarded by a | [PROPOSED C6 — ROUTED-2026-09-06.md:313-318 records C6 as "settled by the collaborator, listed for veto", not as an author ruling] [MODELLED `_Sanity` configurations, formal/tla/P4_VerifierStates.tla:177-188; formal/tla/P5P6_TemporalRevocation.tla:247-262; formal/tla/P5c_IssuanceProtocol.tla:348-369] |
| R-9.16 | Every invariant above is paired with at least | [MODELLED companion set, formal/PROPERTIES.md; formal/tla/*_Broken*.tla] |
| R-9.17 | Termination is a contract obligation on the implementation, | [REGISTERED A2 §A2.3, docs/phase-0-prereg-amendment-2.md:284-290] [MODELLED P5c scoped-out liveness, formal/tla/P5c_IssuanceProtocol.tla:62-76] |
| R-9.18 | A checked model is a model believed, not | [RULED (author) 2026-08-29, formal/suite/ENUMERATION.md:426-452] [REGISTERED A3 §A3.3, docs/phase-0-prereg-amendment-3.md:245-248] |

### Counts

| Section | Requirements |
|---|---|
| §1 What Tessera attests, and what it does not | 27 |
| §2 Actors, channels, trust configuration, adversary | 50 |
| §3 Objects and formats | 70 |
| §4 Issuance protocol | 107 |
| §5 Verification procedure | 62 |
| §6 Standing assessment | 55 |
| §7 Survivability, custody, tending, agility, renewal | 65 |
| §8 Parameters and constants | 9 |
| §9 Invariants and failure behaviour | 18 |
| **Total** | **463** |

| Provenance kind | Tag occurrences |
|---|---|
| REGISTERED | 273 |
| RULED | 98 |
| DECIDED | 10 |
| ADOPTED | 2 |
| MODELLED | 66 |
| PROPOSED | 19 |
| DOCKET | 35 |
| DEFERRED | 2 |
| OPEN | 50 |
| CONTRADICTION | 20 |
| SETTLED | 3 |
| SCOPED-OUT (uncatalogued) | 1 |
| Suite obligation (uncatalogued) | 1 |
| **Total** | **580** |

**Note (2026-09-14).** The provenance-kind table above was generated on
2026-09-13 and two of its rows are stale after the Amendment 7 pass:
`[CONTRADICTION — §12 C-n]` markers in §1–§9 now number **0** (the two C-02
markers were retagged `[SETTLED — §12 S-15 …]` by the owner instance the same day), the other eighteen having become
`[RULED — §12 C-n, A7 §A7.m]`; RULED occurrences rise correspondingly, and seven
requirements were added. The table is not regenerated here: the method that
produced it was not reproduced by this pass either.

---

## Appendix B — sources

Every distinct file path cited in a provenance tag in this document,
sorted. 38 paths. Two entries, `first-link/DECISION.md` and
`standing-probe/DECISION.md`, are the abbreviated spellings some tags use for
files that sit under `formal/spike/`.

- `docs/band-1-docket.md`
- `docs/phase-0-prereg-amendment-1.md`
- `docs/phase-0-prereg-amendment-2.md`
- `docs/phase-0-prereg-amendment-3.md`
- `docs/phase-0-prereg-amendment-4.md`
- `docs/phase-0-prereg-amendment-5.md`
- `docs/phase-0-prereg.md`
- `docs/reviews/2026-07-28-identity-boundary-evidence-floors-ruling.md`
- `first-link/DECISION.md`
- `formal/COVERAGE-MAP.md`
- `formal/PROPERTIES.md`
- `formal/spike/first-link/DECISION.md`
- `formal/spike/first-link/RESULTS.md`
- `formal/spike/standing-probe/AMENDMENTS-2026-08-31.md`
- `formal/spike/standing-probe/DECISION.md`
- `formal/spike/standing-probe/RESULTS-PROBE.md`
- `formal/suite/ENUMERATION.md`
- `formal/suite/ROUTED-2026-09-06.md`
- `formal/suite/lib/tessera_theory.pvl`
- `formal/suite/s-p1/proverif/sp1_q2_degraded_compromised.pv`
- `formal/suite/s-p2/RESULTS.md`
- `formal/suite/s-p2/proverif/sp2_q2_degraded_compromised.pv`
- `formal/suite/s-p3/RESULTS.md`
- `formal/suite/s-p3/proverif/sp3_q2_degraded_compromised.pv`
- `formal/suite/s-p7/RESULTS.md`
- `formal/suite/s-p7/proverif/sp7_q2_degraded_compromised.pv`
- `formal/suite/s-standing/RESULTS.md`
- `formal/suite/s-standing/proverif/ss_q1_strict_dns_compromised.pv`
- `formal/suite/s-standing/proverif/ss_q1d_degraded_compromised.pv`
- `formal/tla/*_Broken*.tla`
- `formal/tla/P4_VerifierStates.tla`
- `formal/tla/P5P6_TemporalRevocation.cfg`
- `formal/tla/P5P6_TemporalRevocation.tla`
- `formal/tla/P5cP5P6_Bridge.cfg`
- `formal/tla/P5cP5P6_Bridge.tla`
- `formal/tla/P5cP5P6_BridgeSlack.tla`
- `formal/tla/P5c_IssuanceProtocol.tla`
- `standing-probe/DECISION.md`
