# Adversarial review: UTC bound and capture visibility

2026-10-17. **Result: revise the memo before adopting its amendment instructions.** The proposed U1 inequality is sound under A-UTC and the existing commitment/history assumptions. I found no counterexample satisfying those assumptions. The service-key listing also blocks substitution by a captor of both channels who cannot obtain release authorization or use the listed service keys. The substantive corrections concern the RFC 3161 comparison, output-contract accounting, time arithmetic, and the release-custody fallback. No HIGH or CRITICAL defect was found in either central construction.

This reviews a recommendation, not an adopted A10 or an implementation. Severity MEDIUM means a material correction to the decision or its proposed specification; LOW means a precision correction that does not defeat the central result.

## Scope and evidence

Read the complete decision memo, complete A9 and proposed A10; A2 §A2.1; A8 §A8.3/§A8.5; V1-PROFILE §5/§7/§15.5, and the output, authority, catalog, open-item and precedence provisions those sections invoke. A9 in the working tree is byte-identical to its version at signing commit `2ad34890359c446efaebcb116388b8e9ffbf6428`; the reviewed repository HEAD was `7d7f94d797048f96df9a2b129962a5604439f4ae`. A10 and the memo were untracked, proposed material. Memo locators below refer to `docs/decisions/2026-10-17-utc-bound-and-capture-visibility.md` before any revisions.

Checked primary Bitcoin Core code/release notes, BIP 54 and its implementation PR, RFC 3161/RFC 5816, and the CA/Browser Forum requirements. The mempool.space report's sample counts and statistics were also checked against its publisher's page. The memo's uncommitted TSA probes were not available for inspection; this review does not authenticate their historical results or reproduce their latency measurements. No formal-model or verifier-conformance result is claimed here.

## Findings and exact fixes

### F01 — MEDIUM: U2 drops accuracy when combining timestamps

**Location:** memo :82–86 and :121–123.

The individual-token expression includes accuracy, but the multiple-TSA expression takes only the maximum `genTime`. That is insufficient even when every TSA is honest within its declared accuracy. RFC 3161 §2.4.2 derives the upper endpoint by adding accuracy; an omitted accuracy field may obtain its value from the TSA policy. Omission does not establish zero uncertainty. [RFC 3161](https://www.rfc-editor.org/rfc/rfc3161.html#section-2.4.2)

**Counterexample:** use seconds relative to an arbitrary epoch. The bytes exist at 99, and both TSAs issue at 100. Token A says `genTime=0, accuracy=100`; token B says `genTime=90, accuracy=10`. Both clock intervals include issuance. `max(genTime)=90` is earlier than the bytes, while `max(genTime+accuracy)=100` is a valid upper endpoint.

**Exact fix:** replace the multiple-TSA sentences with:

> For every required token i, determine a finite authenticated accuracy allowance a_i, from the token or its pinned policy. Report U_TSA = max_i(genTime_i + a_i), rounded upward if the report has coarser precision. Under the commitment assumptions, this bounds existence if at least one required TSA's clock and signing authority were trustworthy for its token. A token with no established finite allowance cannot supply this finite bound. Taking the minimum requires stronger trust assumptions.

Use that expression in the recommendation as well. This correction does not require implementing U2 in V1.

### F02 — MEDIUM: U2's archival treatment conflates preservation, historical trust and continuing algorithm security

**Location:** memo :82–97 and :117–123.

The risks are real, but the proposed remedy and comparison are too categorical. Anchoring a token preserves its exact bytes against fabrication *after that anchor*. It does not establish that the TSA's clock or authority was sound when it produced the token. A thief can manufacture a falsely backdated token and then anchor it. Establishing historical trust needs a trustworthy cutoff and evidence that the preserved token predates it; a header's nominal UTC time alone cannot establish that comparison. This is the same distinction A9.4/A9.6 already make for service signatures.

Nor does A9.4 automatically justify disregarding TSA revocation: it concerns V1's service-receipt assessment, not a newly introduced TSA trust policy. RFC 3161 §4 explicitly addresses TSA compromise, revocation, independent timestamps and renewal. A cryptographically checkable historical token is different from an established historical UTC assertion. [RFC 3161 security considerations](https://www.rfc-editor.org/rfc/rfc3161.html#section-4)

**Exact fix:** replace :82's “has never been misused” with “was trustworthy when this token was produced; later compromise requires evidence distinguishing preserved historical tokens from later fabrications”. Replace :93–97 with:

> Historical certificate-path verification can evaluate validity at genTime using archived certificates. This alone establishes neither historical TSA key safety nor revocation status. If revocation and historical safety are not evaluated, report those omissions separately. An independent commitment to the token can preserve it against later signature forgery, conditional on continuing commitment/history security and evidence that the commitment predates the relevant compromise or algorithm cutoff. It does not authenticate an already false genTime. Bitcoin anchoring is one available preservation mechanism, not a property required by RFC 3161 or a complete historical-trust assessment.

Replace :118–119 with:

> U2 adds TSA clock, certification and key-use trust. For the long-horizon preservation candidate, retaining independent evidence of the token before later compromise is additional work. U1 instead adds the unverified A-UTC assumption to the existing commitment/history assumptions.

The 135-month certificate validity and 15-month signing-use limits are correctly quoted for the cited code-signing ecosystem. They concern different lifetimes. Pinning an intermediate is a reasonable candidate, but authorizes that CA's relevant issuance and moves rotation management up the chain; it is not merely a maintenance optimization without a trust consequence. The requirements also cover key retirement and permit non-RSA TSA keys: “every observed TSA” must remain a statement about the documented sample. [CA/B Forum §6.3.2 and §6.1.5](https://cabforum.org/working-groups/code-signing/requirements/)

**Decision implication:** deferring U2 remains reasonable for the author's evidence-preservation use if the author accepts a conditional UTC bound under A-UTC. The memo does not establish that a court or another examiner will accept that assumption, or that a particular use needs qualified timestamps. Record those as unresolved use requirements. Do not turn them into new V1 obligations. The schedule estimates are estimates, not independently measured implementation costs.

### F03 — MEDIUM: a seventh stable field is an intentional contract change; choose and account for it explicitly

**Location:** memo :208, :222–234; A9 :162, :267–280; profile :288–329.

A9.4 guarantees the six-field result under the same governing specification and other declared inputs. The memo recognizes that “six” would become “seven”, but its minimal change list does not complete the output-format and compatibility consequences. The profile specifies the stable JSON object, diagnostic wrapper, CLI shape, dispatch-null behavior and multi-failure agreement cases. Merely computing another value in both implementations does not settle those interfaces.

**Does this break A9.4?** Inserting a mandatory seventh field into the old stable object changes the registered contract. It cannot be presented as unchanged conformance to that same governing specification. An explicit A10 supersession before the profile freeze can legitimately define the revised contract under the resulting specification hash. It does not retroactively authorize changing results for an older specification. Adding a value outside the stable six is a smaller alternative.

**Exact minimal fix:** retain the six-field stable object and report the additional result in a documented assessment wrapper, for example:

> `utc_assessment` contains `assumption_id: "A-UTC-7200-6"` and `utc_upper_bound` (RFC 3339 string or null). It is computed from the receipt proof's selected h* and its six qualified headers. Its bound is conditional on A-UTC and the existing commitment/history assumptions. It is null exactly when T is null. It does not change the six-field V1 stable result. Reporting a value with INVALID or UNVERIFIABLE does not establish a valid service receipt or valid service signatures.

Specify deterministic computation and test it even though it is outside the stable six. Remove the proposed “six → seven” amendment rows if this alternative is chosen.

If the owner deliberately wants a seventh **stable** field instead, explicitly supersede A9.1 :162 and every relevant A9.4 six-field clause, and update profile §3.4, §3.5, the scheduling/completeness rule, agreement cases and report consumers. Bind this behavior to the amended frozen specification; preserve old-spec behavior if any older-spec bundles are ever supported. This is bounded work, but it belongs in the cost and amendment inventory. The current pre-freeze state makes the change possible; it does not make it a wording-only change.

### F04 — MEDIUM: the profile does not supply Bitcoin-era unwrapping, and U must not use uint32 arithmetic

**Location:** memo :74–75, :230–234; profile §7.1 :803–805 and §7.3 :868–873.

The profile interprets Bitcoin `nTime` as its raw unsigned 32-bit epoch-seconds value. Its serial-time unwrapping rule applies to **DNSSEC RRSIG** fields relative to T_snap. It does not infer an era for Bitcoin timestamps. The memo's statement that Bitcoin's wrap is already handled is therefore unsupported.

There is also a boundary before wrap: for `max nTime = 4294967295`, the correct sum is `4294974495`, or `2106-02-07T08:28:15Z`. A uint32 addition produces 7199, in January 1970. That would defeat the mathematical result in an implementation even when A-UTC holds.

**Exact fix:** replace :74–75 with:

> Verification of a preserved V1 receipt does not consult the current clock and can still run in 2106. Interpret each bundled nTime as the profile's unsigned epoch-seconds value, widen it before arithmetic, and compute U without modular reduction. This does not define timestamps for newly mined post-wrap Bitcoin blocks; that would require a future Bitcoin/profile rule.

Add this normative arithmetic sentence to the proposed §7.1 change:

> `U_seconds = 7200 + max(uint64(nTime(h*)), …, uint64(nTime(h*+5)))`; encode the sum as an RFC 3339 UTC string without reducing it modulo 2^32.

Add the maximum-uint32 boundary vector and a preserved-old-receipt verification case with a 2106 verifier clock. No new Bitcoin-era design is needed for V1's old receipts.

### F05 — MEDIUM: cutting the listing does not repair a failure of the existing release-independence prerequisite

**Location:** memo :162–168 and :198–201; A9.5 :326–332; profile §14.2 item 1.

The failure-mode paragraph correctly names the existing NARROW-MODEL route. The final recommendation then appears to allow “cut the listing” and return to A10.4 option (a) if release independence is unavailable. That is incomplete: independent release authentication already protects V1's KSKs, repository trust and header pins against this adversary. Its failure is not specific to the new key list. Merely deleting `service_keys` cannot restore the original capture claim.

**Exact fix:** replace :199–201 with:

> If the listing is cut for schedule reasons while A9.5's independent release boundary is established, retain A10.4 option (a) and state the absence of new-key protection. If release independence itself cannot be established, follow profile §14.2 item 1: present a NARROW-MODEL of the affected channel-capture claim to the author before freeze. Cutting the listing alone does not resolve that existing prerequisite.

Keep the BROADEN label for the listing and label its new cut-order amendment as an actual gate/scope change. Do not make a custody failure an automatic, invisible reversion of the threat model.

### F06 — LOW: distinguish node clock from UTC, and a BIP implementation proposal from activation

**Location:** memo :31–38.

The memo correctly identifies the **receiving validating node's system clock**, rather than the miner's clock or current peer-adjusted time. Bitcoin Core 27.0 removed network-adjusted time from this code. The subsequent inference “above real time” still needs that node's clock-error assumption. [Core 27.0 release notes](https://bitcoincore.org/en/releases/27.0/), [header validation](https://github.com/bitcoin/bitcoin/blob/v27.0/src/validation.cpp)

**Exact fix:** replace :34–35 with:

> This bounds nTime above the receiving node's clock at acceptance. If that clock is accurate to UTC, it implies acceptance no earlier than nTime − 2 h in UTC; otherwise its clock-error bound must also be included. It supplies no real-time upper bound.

BIP 54's status is **Complete**, and its stated period-start inequality is correct. Complete does not mean deployed. At review time PR #35793 was **open** and proposes enabling its rules on regtest only; saying it “enables” them can imply merged behavior. Also, BIP 54 contains a period-end timestamp restriction in addition to the cited period-start rule. Neither anchors timestamps to UTC. [BIP 54](https://github.com/bitcoin/bips/blob/master/bip-0054.md), [PR #35793](https://github.com/bitcoin/bitcoin/pull/35793)

**Exact fix:** replace :36–38 with:

> BIP 54 (specification status Complete) proposes period-start nTime ≥ previous nTime − 7200 s and an additional period-end timestamp restriction. It is not active on mainnet. Open Core PR #35793 proposes implementing it with regtest-only activation. These restrictions are header-relative and supply no UTC upper bound.

These corrections do not change U1's derivation: it does not rely on the two-hour future rule or BIP 54.

### F07 — LOW: make the service-key classifier ordered and define completeness as authorization closure

**Location:** memo :133–149 and :232–234.

The table is sound when interpreted as an ordered classifier. Its literal conditions overlap: a listed future window also starts after `as_of`, and an unlisted future window may overlap a prelisted window. The INVALID-versus-horizon priority should be explicit before this becomes a total decision function. Likewise, “every window” cannot mean every attacker-created interval. Completeness must refer to the release authority's authorized schedule, with permanent closure against later backfilling. A release checker can enforce transitions; it cannot discover omitted real-world authorizations in the initial configuration.

**Exact fix:** replace the three conditions and completeness wording with:

> First, an exact match on D, both canonical fingerprints and both inclusive window endpoints passes this check. Otherwise, overlap with any listed window **or** not_before ≤ as_of yields INVALID / SERVICE_KEYS_NOT_LISTED. Otherwise yield UNVERIFIABLE / TRUST_HORIZON. Overlap includes a shared endpoint. Overall verdict and reason use the registered failure precedence, not an early return from this check.
>
> The initial release independently authorizes and records the complete service-key schedule through as_of. Later releases retain every existing entry unchanged, introduce no overlapping interval, and add an entry only if its not_before is strictly greater than the previous as_of. Thus absence through a past horizon is permanently closed. Completeness concerns authorized entries, not arbitrary channel assertions. The release authority must not authorize a new service-key tuple solely because the two potentially captured channels assert it.

The schema should require finite endpoints with not_before ≤ not_after, canonical fingerprint encodings, unique entries, and an explicit sort order. These are details of the proposed schema, not a new architecture. Add vectors for exact future match, unlisted future overlap, a shared-endpoint overlap, and additions at versus strictly after the old horizon. An authentic release means both authenticated distribution and the trusted release-authority behavior; uncompromised key storage alone does not validate an authorization decision.

## Questions checked without a central counterexample

### 1. Bitcoin facts and the U1 proof

**MTP:** correct. For ordinary mainnet heights, the timestamp must be strictly greater than the median of the preceding eleven header timestamps. It is not required to exceed its immediate predecessor's timestamp. This is a chain-relative restriction. It supplies no useful upper bound on real mining time. [Bitcoin Core median calculation](https://github.com/bitcoin/bitcoin/blob/master/src/chain.h)

**Counts and clocks:** h* is the receipt's **inclusion** block. A2.1 counts that block as confirmation one, so confirmation six is h*+5. T is nTime(h*); `confirmed_at` is nTime(h*+5). U uses the maximum of **all six**, not just either endpoint, and not the minimum. The DNS and git proofs' selected heights do not enter this receipt U. The selected receipt branch remains the lowest qualifying height, not the branch with the most favorable timestamp. Qualification already requires the six linked, pinned headers. There is no confirmation-count off-by-one.

Let e be the real existence time of the bytes committed in `A_sig`, including the two exact signature byte strings. Let r_i be the first production time of the selected valid block at height i. Under the commitment/preimage and authentic-history assumptions:

```text
e < r_h*
r_h* ≤ r_j                                  for j in [h*, h*+5]
A-UTC supplies j with r_j ≤ nTime(j) + 7200
therefore e < r_h* ≤ r_j ≤ nTime(j)+7200 ≤ U.
```

The strict existence claim comes from commitment preceding block production, not a strict timestamp comparison. Mining order need not make header timestamps monotone. A six-block segment in which five timestamps lag arbitrarily far behind is still safe if the sixth satisfies A-UTC. A segment in which every timestamp lags more than two hours can invalidate the advertised UTC assertion, but that violates A-UTC and is not a counterexample under it.

**How minimal is A-UTC?** It needs only one one-sided lag witness, not an honest inclusion miner, an honest majority of the six, synchronized clocks for every miner, or a bound on service observation delay. That is a small, intelligible operational assumption. It is not the logically weakest sufficient assumption: `max nTime + 7200 ≥ r(h*)` would itself suffice, and a successor timestamp could satisfy that without approximating its own mining time. Retain A-UTC because its per-block interpretation is intelligible; call it “a sufficient one-sided assumption”, not a uniquely minimal one. Neither m=6 nor Δ=7200 is established as optimal. Two hours is an author-selected backward tolerance; matching Bitcoin's forward tolerance does not validate it.

The α⁶ calculation is correct for the explicitly hypothetical independent, fixed six-block experiment. It is not a security probability for a captor who chooses when to submit, retries, withholds blocks, or selects among proofs. Add that sentence after :65. The sample and its stated −69/+82/41-second statistics match the publisher's report, which concerns observer arrival versus timestamp, not directly known production times. It remains context only. [mempool.space report](https://research.mempool.space/p/09defe3d-c836-44e7-b244-7f8434e72151)

**A2 compatibility:** the distinction at :69–72 is valid. A-UTC does not bound delivery/observation delay B−C, does not supply an issuance opportunity, and does not enter the verdict, shipping predicate or S. It must nevertheless be registered as a **new assumption of the UTC assessment**, rather than treated as inherited consensus evidence. Existing chain-order claims remain available without it.

### 2. Capture, append-only trust and verdict stability

For a configuration C, write L(C) for its immutable listed tuples and a(C) for its horizon. With F07's ordering:

| Prior check result | Why an allowed append preserves the relevant witness |
|---|---|
| Pass | Its exact tuple remains in L(C). |
| INVALID because of overlap | The overlapping listed interval remains, and the conflicting tuple cannot be added. |
| INVALID because start ≤ a(C) | The old closed horizon prohibits adding that tuple later. |
| UNVERIFIABLE beyond the horizon | It may later pass or become a closed conflict as the authorized schedule becomes known. |

This preserves positive witnesses and the classifier's closed-negative conclusions. It does **not** establish whole-verifier monotonicity across configurations: header-pin extensions can change qualifying selection, T, U and other checks (profile §5 :524–531). A9.4 requires identical stable output for identical declared inputs, including the same governing specification and configuration. Do not replace that with an unconditional same-verdict promise across releases. The memo's local argument is compatible with that contract when read this way.

**Channel-captor attack:** a captor can create valid DNS and git evidence naming its own keys, obtain their signatures, and anchor everything. Those actions do not add the tuple to the release's list. Choosing the old window gives the new INVALID reason; choosing a disjoint window beyond the horizon gives UNVERIFIABLE. Neither accepts. Choosing the listed tuple requires producing signatures under its keys, contrary to the stated service-signing boundary. Later release authorization is a separate required capability. Normal replay or obtaining an honestly issued receipt remains possible and is not a forged receipt under captor-selected keys.

**Observation scope:** :151–158 honestly states rejection/contradiction for parties using authentic releases, and explicitly disclaims issuer detection and public visibility. A future horizon result is lack of coverage, not proof of a takeover. A targeted malicious release remains outside the trusted-distribution boundary; release signing alone provides no public observation guarantee. A8.3 protects honest material under credential disclosure, not arbitrary new captor-key issuance, and A8.5 does not supply evidence for this added listing property. The memo correctly disclaims a formal-model result for it. Required vectors remain prospective evidence, not already checked evidence.

### 3. Minimal change, labels and scope discipline

The mechanism choices stay within “resolve these two deficiencies”. U1 reuses existing evidence, and the listing extends an existing independent distribution channel. Comparing a TSA and witnessed log is useful decision support. Neither comparison requires building a new architecture, nor should either become an automatic V2 obligation. The proposed removal of that obligation is appropriate.

**BROADEN is correct** for an additional conditional UTC assessment and for the narrower new-key non-acceptance guarantee. It must remain paired with the explicit A-UTC assumption and release-authority boundary. It is not evidence that the old unconditional UTC reading was sound, or that capture becomes publicly visible. Keep the existing NARROW-CLAIM corrections for the old prose and keep the original two-channel checks.

The minimum amendment inventory also needs the service-key list in A9.1's trust-configuration description and A9.5's append-only entry list, not only C4/adversary/boundaries; a scoped statement in A9.6's first-window discussion; the new assessment and assumption in the output/catalog specification; and the precise cut/fallback rule. Freeze Δ=7200 and m=6 in the governing specification, not mutable trust-file policy. Preserve guarantee 2's chain-time meaning. Do not turn the nearby removal of “V1 does not establish” into an unqualified UTC guarantee for that window rule.

At minimum, register new-check and assessment vectors as exit evidence, update the trust schema/release checker and reason precedence, and assemble new specification/vector hashes. Original signed-frame grammar and P8 layout can stay unchanged even though the signed specification hash changes. Any claim that **all** verdicts remain unchanged must be withdrawn: the fresh captor-key receipt is deliberately a newly rejected case. The existing scenario mapping may keep its verdicts; that is a narrower statement. Instrument verifier changes remain subject to A9.2's existing distinction between instruments and post-exit service code.

## Validation limits

The proof above is the principal arithmetic argument. A read-only finite check exercised 343,937 ordered-mining/arbitrary-header assignments satisfying the lag assumption in a small integer domain, with no inequality violation. A separate 14,280-case finite check of allowed single service-list additions preserved prior pass and INVALID results. These checks illustrate the arguments; they are not Bitcoin-conformance tests or formal discharge. The uint32 boundary and the TSA accuracy counterexample were evaluated directly. No real captured-channel receipt vector was executed in this review.

The memo's old-receipt archival objective can be met conditionally without imposing U2 on V1. The owner still has to accept the stated assumption and narrower observation scope, supply the already-required release boundary, and register the concrete changes. This review neither makes those author decisions nor reopens the architecture.
