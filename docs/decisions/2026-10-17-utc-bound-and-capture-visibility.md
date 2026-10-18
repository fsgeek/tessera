# Decision memo: a UTC upper bound and capture visibility for V1 (2026-10-17)

> **Status: RECOMMENDED (owner), not decided.** Drafted 2026-10-17 by Claude (Opus 5.5) for the owner. It answers
> the author's Codex review of 2026-10-17 (session `01a116dc…`, 00:38Z), which asks V1 to *keep* two objectives
> rather than only narrow its wording: (1) a defensible real-time upper bound on existence, and (2) capture
> visibility within a defined observation scope.
>
> Inputs: A9 (signed, `2ad3489`), proposed A10 (A10.1, A10.4), A2 §A2.1, A8 §A8.3/§A8.5, and `docs/V1-PROFILE.md`
> §3.4, §5, §6.3–6.4, §7, §14.2 and §15.5. Revised 2026-10-17 after the Codex review
> (`docs/reviews/utc-capture-memo/CODEX-REVIEW.md`, F01–F07, all accepted). The disposition is in the same
> directory.
>
> Labels: **[F]** fact, with source; **[A]** assumption; **[E]** estimate; **[R]** owner recommendation. No other file
> is changed by this memo.

## Summary

- **UTC bound: adopt U1.** V1 reports `U = max nTime(h* … h*+5) + 7200 s` in an assessment wrapper, outside the six
  stable fields. The accompanying claim is that the bytes and both signatures existed before U (UTC).
  - U rests on one new, named assumption, A-UTC. A-UTC is not consensus.
  - U uses only headers that V1 already requires and pins.
  - RFC 3161 tokens (U2) are recorded as a candidate, not as a V2 obligation.
- **Capture visibility: adopt the owner's proposal as an ordered three-outcome check.**
  - The release-signed trust configuration lists D's authorized service-key schedule.
  - A captor holding both channel credentials then also needs release authorization.
  - The scope is relying parties who run an authentic verifier release.
- **Release-key independence is a separate question for the author.** It is an existing prerequisite of A9.5's
  trust-configuration authority, and it is still OPEN (§14.2 item 1). Cutting the listing does not cure its absence.
- **A10 stops being "wording only".** It gains two BROADEN sections and drops the automatic V2 obligation in A10.4.
  **[E]** About 4–5 owner-days before 30 Oct, plus one review round.

## Part 1. The UTC upper bound

### What Bitcoin consensus does and does not bound

- **[F] Median-time-past (consensus).** A header is invalid if `nTime ≤ MTP(prev)`. MTP is the median of the
  previous 11 timestamps (Bitcoin Core `validation.cpp`, "time-too-old"; `chain.h`, `nMedianTimeSpan = 11`).
  - This bounds a timestamp below, relative to earlier timestamps only.
  - It does not bound a timestamp relative to real time. A miner may set any `nTime > MTP`, however late the block
    is actually mined.
- **[F] Two-hour future rule (node-local, not strict consensus).** A node rejects a header with
  `nTime > now + 7200 s` (`MAX_FUTURE_BLOCK_TIME = 2*60*60`, result `BLOCK_TIME_FUTURE`). The node can accept the
  block later.
  - Since Bitcoin Core 27.0, `now` is the receiving node's own system clock, not network-adjusted time (PR #28956).
  - The rule bounds nTime above the receiving node's clock at acceptance. If that clock is accurate to UTC, it
    implies acceptance no earlier than nTime − 2 h in UTC; otherwise its clock-error bound must also be included.
  - It supplies no real-time upper bound.
- **[F] Timewarp (BIP 54).** BIP 54 (specification status Complete) proposes period-start nTime ≥ previous
  nTime − 7200 s, and an additional period-end timestamp restriction.
  - It is not active on mainnet.
  - Open Core PR #35793 proposes implementing it with regtest-only activation.
  - These restrictions are header-relative and supply no UTC upper bound.
- **[F] Consequence (already registered, A2.1).** Consensus gives no finite bound on how far a header time may lag
  real time. A coalition with a majority of hash power can keep timestamps behind real time without limit, because
  MTP only has to creep upward.
- **[F] Context only.** mempool.space compared arrival at one observer with header time over 481 blocks (heights
  857514–858080): −69 s to +82 s, median 41 s. That is observer arrival, not production time, and not a bound.

### U1: an explicit registered assumption on header times

**Notation.** h* is the selected inclusion height (A10.5). It counts as confirmation one, so h*+5 is confirmation
six. r(j) is the real (UTC) time at which block j was first produced.

**Derivation:**
1. **[F under registered assumptions]** `A_sig` existed before r(h*). The merkle root of block h* commits to
   `SHA256(A_sig)` through the OTS path, under the SHA-256, OTS and history assumptions in A9.
2. **[F under the hash assumption]** For every j ≥ h*, r(h*) ≤ r(j). Block j commits to the hash of a chain that
   contains h*.
3. **[A] A-UTC (Δ = 7200 s, m = 6).** Among blocks h* … h*+5, at least one satisfies `nTime(j) ≥ r(j) − Δ`. That is,
   its timestamp is no more than two hours earlier than its production.
4. For that block j: r(h*) ≤ r(j) ≤ nTime(j) + Δ ≤ max over i in [h*, h*+5] of nTime(i) + Δ.

**Result.** `A_sig`, and therefore the bytes and both signatures, existed before
**U = max nTime(h* … h*+5) + 7200 s**.
- In the requested form, U = T + X, with **X = 7200 s + (max nTime(h* … h*+5) − T)**.
- The second term comes from the receipt. With honest blocks it is typically about 50 minutes.
- The stronger assumption "h* itself is honest" would give X = 7200 s exactly. **[R]** Do not adopt it: it rests
  the whole claim on one miner.

**What is consensus and what is assumption.**
- Steps 1–2 rest on cryptographic and chain assumptions that are already registered.
- Step 3 is a new assumption of the UTC assessment. It is not consensus, and the bundle cannot check it.
  - A-UTC is a sufficient one-sided assumption, not a uniquely minimal one: `max nTime + 7200 ≥ r(h*)` would
    itself suffice.
  - m = 6 and Δ = 7200 s are not shown to be optimal. Δ is an author-selected tolerance; matching Bitcoin's
    forward tolerance does not validate it. Both are frozen in the governing specification, not in the mutable
    trust file.

**Context [E].** If a backdating coalition holds a share α of independently found blocks, all six are theirs with
probability α⁶ (7×10⁻⁴ at α = 0.3; 1.6% at α = 0.5). That is a fixed six-block experiment, not a security
probability against an adversary who chooses when to submit, retries, withholds blocks or selects among proofs.

**Relation to A2.1 (no conflict).** A2.1 refuses to bound B − C, the service's observation lag, and keeps
SLA-style bounds out of the assumption set. A-UTC bounds a different quantity (production versus header time), and
U never enters a verdict, the shipping predicate or S. The chain-order claims stand without A-UTC.

**Cost and long-term arithmetic.** U1 needs no new input: the six headers are already required, pinned and
qualified (§7.1).
- Verification of a preserved V1 receipt does not consult the current clock and can still run in 2106.
- Interpret each bundled nTime as the profile's unsigned epoch-seconds value. Widen it before arithmetic, and
  compute U without modular reduction:
  `U_seconds = 7200 + max(uint64(nTime(h*)), …, uint64(nTime(h*+5)))`. Encode the sum as an RFC 3339 UTC string,
  without reducing it modulo 2^32.
  - Example: for max nTime = 4294967295, U = 4294974495, which is `2106-02-07T08:28:15Z`. A uint32 addition would
    give 7199, in January 1970.
- This does not define timestamps for newly mined Bitcoin blocks after the 2106 wrap. That would need a future
  Bitcoin or profile rule. The profile's serial-time unwrapping applies to DNSSEC RRSIG fields only.

### U2: RFC 3161 tokens over SHA256(A_sig), alongside Bitcoin

**[F] Mechanism.**
- The TSA signs a TSTInfo containing `messageImprint = SHA256(A_sig)`, `genTime`, an optional `accuracy`, a policy
  OID and an optional nonce.
- The TSA certificate carries the critical EKU id-kp-timeStamping (RFC 3161 §2.1–2.4).
- RFC 5816 adds ESSCertIDv2, which binds the signing certificate with SHA-256.

**[A] Trust.**
- A single token supports "existed before genTime + accuracy". That holds only if the TSA's clock and signing
  authority were trustworthy when this token was produced.
- Later compromise requires evidence that distinguishes preserved historical tokens from later fabrications.
- **Combining several TSAs:** for every required token i, determine a finite authenticated accuracy allowance a_i,
  from the token or its pinned policy.
  - Report U_TSA = max_i(genTime_i + a_i), rounded upward if the report has coarser precision.
  - Under the commitment assumptions, this bounds existence if at least one required TSA's clock and signing
    authority were trustworthy for its token.
  - A token with no established finite allowance cannot supply this finite bound.
  - Taking the minimum requires stronger trust assumptions.
- **[F] Endpoint names do not show independence.** On 2026-10-17, `timestamp.entrust.net` returned a token signed by
  *Sectigo* Public Time Stamping Signer R37.

**[F] Long-term verifiability.**
- Under the CA/B Forum Code Signing BRs (v3.11.0, §6.3.2), a TSA certificate is valid for at most 135 months, and
  its key may be used for signing for at most 15 months. These are two different lifetimes.
- **Pinning an intermediate CA** is a reasonable candidate. The intermediates observed on 2026-10-17 run to
  2038–2041.
  - It authorizes that CA's relevant issuance and moves rotation management up the chain.
  - It is therefore a trust choice, not merely a maintenance optimization.
- **Historical path verification:** certificate-path verification can evaluate validity at genTime using archived
  certificates.
  - This alone establishes neither historical TSA key safety nor revocation status.
  - If revocation and historical safety are not evaluated, report those omissions separately. A9.4 concerns the
    service receipt, not a new TSA trust policy.
- **Independent commitment to the token:** this can preserve the token against later signature forgery.
  - It is conditional on continuing commitment and history security, and on evidence that the commitment predates
    the relevant compromise or algorithm cutoff.
  - It does not authenticate a genTime that was already false.
  - Bitcoin anchoring is one available preservation mechanism. It is neither required by RFC 3161 nor a complete
    historical-trust assessment.
- The TSAs sampled here all used RSA keys. That describes this sample only; the requirements permit other key
  types.

**[F] Free endpoints answering from this host on 2026-10-17** (one SHA-256 query each; probe output not
committed): DigiCert `timestamp.digicert.com` 0.13 s; Sectigo `timestamp.sectigo.com` 0.46 s; GlobalSign
`…/tsa/r6advanced1` 0.57 s (accuracy 1 s); Certum `time.certum.pl` 0.66 s (accuracy 1 s); FreeTSA timed out at
20 s. Sectigo asks scripts to wait ≥ 15 s between requests (about 4 receipts per minute per client). Terms of use
were not verified. These are code-signing TSAs; eIDAS *qualified* stamps (Art. 41(2), presumption of accuracy) are
generally paid.

**[E] Changes U2 would need:** a token bundle member, a §15.5 TSA pin list, a CMS/DER parser (ESSCertIDv2, EKU,
policy, accuracy, imprint), about eight reason codes with §15.7 rows, a §4 issue-order step, a dependency-manifest
entry, vectors, and both differential implementations. About 6–9 owner-days, plus preservation work; estimates, not
measured. It does not fit before 30 Oct beside the 21 Oct hybrid and §14.2's open items.

### U3: both

The strongest option (two independent kinds of evidence), at U2's cost; not feasible before 30 Oct.

### Recommendation [R]: U1 for V1; record U2 as a candidate, not an obligation

1. **Trust.** U2 adds trust in the TSA's clock, certification and key use. For the long-horizon preservation
   candidate, keeping independent evidence of the token before later compromise is additional work. U1 instead adds
   the unverified A-UTC assumption to the existing commitment and history assumptions.
2. **Schedule.** U1 costs about 1 day; U2 costs 6–9 days and would displace freeze work.
3. **Record U2 as a candidate.** Use the design above: U_TSA over at least two independently operated TSAs, with
   pinned intermediates and independent preservation. It applies if a use turns out to need conventional or
   qualified timestamps. Do not register it as a V2 obligation (Codex point 4).
4. **Unresolved use requirements, recorded but not made V1 obligations:**
   - whether a court or another examiner will accept A-UTC;
   - whether a particular use needs qualified timestamps.

## Part 2. Capture visibility

### The proposal, made exact

**[F] Today.** A captor of both channel credentials (the DNS credential, and the repository key that the trust
configuration pins) can publish a key assertion naming its own keys. V1 then accepts receipts under those keys
(A10.4).

**Mechanism.** §15.5 gains `service_keys`, an array of `{domain, kms_fp, gpg_fp, not_before, not_after, sources}`
entries.
- Endpoints are finite, with not_before ≤ not_after.
- Fingerprints are canonical; entries are unique; the array has an explicit sort order.

The new authority check is an ordered classifier, by analogy with `HEADER_CONFLICTS_PIN` versus
`HEADERS_NOT_COVERED`:

> First, an exact match on D, both canonical fingerprints and both inclusive window endpoints passes this check.
> Otherwise, overlap with any listed window **or** not_before ≤ as_of yields INVALID / SERVICE_KEYS_NOT_LISTED.
> Otherwise yield UNVERIFIABLE / TRUST_HORIZON. Overlap includes a shared endpoint. Overall verdict and reason use
> the registered failure precedence, not an early return from this check.

**Completeness as authorization closure:**

> The initial release independently authorizes and records the complete service-key schedule through as_of. Later
> releases retain every existing entry unchanged, introduce no overlapping interval, and add an entry only if its
> not_before is strictly greater than the previous as_of. Thus absence through a past horizon is permanently
> closed. Completeness concerns authorized entries, not arbitrary channel assertions. The release authority must
> not authorize a new service-key tuple solely because the two potentially captured channels assert it.

**Issuer invariant.** No receipt ships under keys that are not listed in a published release.

**Verdict stability.**
- Passes and both INVALID conclusions survive every allowed append.
- An UNVERIFIABLE result may later pass. A9.5 permits this.
- This is local to this check. A9.4's contract remains identical output for identical declared inputs, the
  configuration included. Pin extensions can still change selection, T and U across releases.

**[F]** V1 registers one window only (A9.6). Its configuration lists exactly one entry, authorized at the freeze.

**Observation scope.** The guarantee covers relying parties who run an authentic verifier release whose trust
configuration lists D's service keys.
- "Authentic" means authenticated distribution plus trustworthy release-authority behaviour. Uncompromised key
  storage alone does not validate an authorization decision.
- Within this scope, a captor of both channel credentials who lacks release authorization cannot make a receipt
  under keys of its choosing pass V1. Codex's "relying parties with previously trusted issuer keys" is this set.
- **[F, honest limits]**
  - What this provides is non-acceptance, plus a contradiction verdict when the window overlaps a listed one or
    starts at or before `as_of`. It is not issuer detection and not public visibility.
  - A horizon result means the keys are not yet covered. It is not proof of a takeover.
  - A8.3 and A8.5 supply no evidence for this property, and no formal model run supports it. Its evidence is the
    check's construction plus prospective vectors.

### Failure modes

- **Release-key capture.** This is distribution compromise, already a stated boundary (A9).
  - A holder of release authorization can already substitute KSKs, repository keys and pins. The listing adds no
    new trust root.
  - A captor with both channels and the release key can ship a release that lists its own keys.
  - A *targeted* release, given to one victim, is invisible to everyone else. That residual is what a witnessed log
    addresses.
- **Stale trust file, honest new-window receipt.** The result is `UNVERIFIABLE / TRUST_HORIZON`, a safe false
  reject until the relying party updates.
  - This cannot occur in V1, which has one window.
  - After a registered rotation it is the expected outcome, and the relying-party text must say "update the
    verifier".
- **Rotation cost (post-V1).** One release per window (≤ 90 days), authorized before it opens; a timing
  obligation on an existing process.

### Does this change a registered claim?

**Yes. It is a BROADEN.**
- C4 gains a third authenticated source for the key set: the release.
- A9's adversary clause and A10.4 gain a protection: no new receipts under captor keys, within the scope above.
- The listing adds one check, one reason code, one schema field and the closure invariants.
- **Unchanged:** the signed bytes, the P8 encoding, `A_sig`, the existing two-channel checks and the
  scenario-mapping verdicts.
- **Not every verdict is unchanged:** a fresh captor-key receipt is deliberately a newly rejected case.
- **Amendment needed.** The listing changes C4, A9.1's trust-configuration description, A9.5's append-only entry
  list and the adversary text, and it needs a scoped statement under A9.6's first window. **[R]** Put it in A10 as
  one signing act, not a separate A11 (Codex point 5: one corrected description).

### Brief comparison: a witnessed append-only log

Key assertions would enter a transparency log; the verifier would require an inclusion proof under a tree head
cosigned by k witnesses whose keys the release pins. It adds split-view resistance and issuer detection by
monitoring, at the cost of log and witness operators, 2106-lived witness keys, bundled proofs and a monitoring duty
(**[E]** weeks). **[R]** Record it as the candidate for the broader visibility objective, with no commitment (Codex
point 4), replacing A10.4's "named V2 obligation".

### Recommendation [R]

Adopt the service-key listing with the ordered classifier, the authorization-closure invariants, the scope sentence
and the limits.

**Cut order.** Adding the listing to the cut order, after the hybrid, is a gate and scope change and is labelled as
one. If the listing is cut for schedule reasons while A9.5's independent release boundary is established, retain
A10.4 option (a) and state the absence of new-key protection.

**Release independence, a matter for the author.**
- Release-key independence (§14.2 item 1, OPEN; YubiKey 2 is not in hand) is already a prerequisite of A9.5's
  trust-configuration authority, whatever happens to the listing.
- It already protects V1's KSKs, repository trust and header pins against the channel captor.
- If release independence itself cannot be established, follow profile §14.2 item 1: present a NARROW-MODEL of the
  affected channel-capture claim to the author before freeze.
- Cutting the listing alone does not resolve that existing prerequisite, and a custody failure must never be an
  automatic, invisible reversion of the threat model.

## Part 3. What A10 should say, and the minimal changes

**A10.1 (NARROW-CLAIM plus BROADEN).** Keep the chain-time reading of T, and add:

> *Under the registered assumption A-UTC (at least one of the blocks h* … h*+5 carries a header time no more than
> 7200 s before the time it was produced; an assumption of the UTC assessment, not a consensus rule, and not checked
> by the verifier), the bytes and both signatures existed before U = max nTime(h* … h*+5) + 7200 s, in UTC. V1
> reports U in `utc_assessment`, outside the six stable fields. A2.1's refusal to bound the observation lag B − C is
> unchanged.*

Point A9's sentence "requires an additional, explicit backward-skew assumption that V1 does not establish"
(:444-446) to A-UTC, scoped to U. Guarantee 2 keeps its chain-time meaning and is not translated to UTC.

**Output contract (F03): a wrapper, not a seventh stable field.** **[R]**

> `utc_assessment` contains `assumption_id: "A-UTC-7200-6"` and `utc_upper_bound` (RFC 3339 string or null). It is
> computed from the receipt proof's selected h* and its six qualified headers. Its bound is conditional on A-UTC
> and the existing commitment/history assumptions. It is null exactly when T is null. It does not change the
> six-field V1 stable result. Reporting a value with INVALID or UNVERIFIABLE does not establish a valid service
> receipt or valid service signatures.

**Why the wrapper.** It keeps A9.4's stable-field contract simplest.
- A9.1's and A9.4's six-field clauses stay as signed, so no supersession is needed.
- §3.4's stable JSON object, §3.5's CLI shape, the dispatch-null rule and the multi-failure agreement cases are all
  untouched.
- Nothing is lost by leaving U out of the stable set. U is a deterministic function of h*, whose headers are in the
  bundle, and T is already stable, so any later examiner can recompute U.
- U is still specified deterministically and tested.

**A10.4 (option (a) plus BROADEN).** Keep the recommended honest-material clause, and add:

> *Against a relying party running an authentic verifier release whose trust configuration lists D's service keys,
> a captor of both channel credentials who lacks release authorization cannot make a receipt under keys other than
> those listed pass V1. Such a receipt is INVALID when its window overlaps a listed window or starts at or before
> the configuration's `as_of`, and UNVERIFIABLE otherwise.*

Keep the boundary on publication, and add:

> *Release-key compromise is distribution compromise. A release delivered to one party is not detectable by others.
> V1 provides no issuer detection.*

Delete the automatic V2 obligation. Record the unmet broader objective, with the witnessed log as a candidate
approach.

**Elsewhere in A10:**
- Rewrite "adds no mechanism" in the plain-words section, the Weakening paragraph and "In sum". Withdraw "no
  verdict changes" in favour of "the scenario mapping's verdicts are unchanged".
- Add A10.7 rows for:
  - A9's opening claim (:36-37, U);
  - C4 (the listing);
  - C5 (U);
  - A9.1's trust-configuration item;
  - A9.5's append-only list;
  - A9.6's first-window statement;
  - the adversary clause and boundaries;
  - the cut order (A9.2, marked as a gate change).
- No six-to-seven rows are needed.

**Minimal spec and verifier changes:**

| # | Where | Change | [E] effort |
|---|---|---|---|
| 1 | Profile §7.1, §3.4, spec catalog | U's definition, with uint64 arithmetic; Δ and m frozen in the catalog; the `utc_assessment` wrapper; relying-party sentence on A-UTC | 0.5 d |
| 2 | Verifier (both differential implementations) | Compute U from the six qualified headers, widened before addition | 0.25 d |
| 3 | Profile §5, §15.5, release checker | `service_keys` schema; immutability, non-overlap and strict-after-`as_of` additions | 0.75 d |
| 4 | Profile §6.4, §15.7 | Ordered service-key classifier after M5, with its precedence row; §4 issuer invariant | 0.75 d |
| 5 | Vectors (§14.2 item 8) | See the list below | 1 d |
| 6 | A10 text, its review, and new spec/vector hashes at freeze | As above, with one Codex pass | 1 d plus the review |

Row 5's vectors: for U, nonmonotone times, the maximum at h*+5, the uint32 maximum (expect
`2106-02-07T08:28:15Z`) and an old receipt under a 2106 clock; for the classifier, listed, exact future match,
overlap conflict, unlisted future overlap with a prelisted window, shared endpoint, unlisted at or before `as_of`,
and horizon; a captured-channels fixture (valid DNS and git under captor keys) expecting INVALID; and release-checker
additions at versus strictly after `as_of`.

**Total [E]: about 4–5 owner-days** in the 13 days to 30 Oct, competing with the 21 Oct hybrid and §14.2's open
items.
- **Unchanged:** ENCODING-V1, P8, `A_sig`, the signed frames, every existing check and reason code, the
  scenario-mapping verdicts and the six stable fields. The specification hash does change.
- **Release independence (§14.2 item 1)** remains an existing prerequisite, decided separately (Part 2).

## Sources

- Bitcoin Core `src/validation.cpp` (ContextualCheckBlockHeader) and `src/chain.h`, master, fetched 2026-10-17:
  https://github.com/bitcoin/bitcoin ; 27.0 release notes: https://bitcoincore.org/en/releases/27.0/
- Bitcoin Core PR #28956 and PR #29623: https://bitcoincore.reviews/28956 ; https://mirror.b10c.me/bitcoin-bitcoin/29623/
- BIP 54: https://github.com/bitcoin/bips/blob/master/bip-0054.md ; PR #35793 (open):
  https://github.com/bitcoin/bitcoin/pull/35793
- mempool.space, Block Time Report: https://research.mempool.space/p/09defe3d-c836-44e7-b244-7f8434e72151
- RFC 3161 (§2.4.2 accuracy, §4 security considerations); RFC 5816 (ESSCertIDv2); RFC 5652 (CMS)
- CA/Browser Forum Code Signing BRs v3.11.0 (§6.1.5, §6.3.2, §6.8):
  https://cabforum.org/working-groups/code-signing/requirements/
- Sectigo time-stamping guidance (15 s spacing): https://sectigo.com/resource-library/time-stamping-server
- DigiCert RFC 3161 server: https://knowledge.digicert.com/general-information/rfc3161-compliant-time-stamp-authority-server
- Regulation (EU) No 910/2014 (eIDAS), Art. 41(2)
- Endpoint probe, 2026-10-17, `openssl ts`: latencies, certificate subjects and dates as quoted above (scratch
  output, not committed)
- Codex review of this memo: `docs/reviews/utc-capture-memo/CODEX-REVIEW.md`
- Repository: A2 §A2.1; A8 §A8.3, §A8.5; A9 (opening, A9.4–A9.6); A10 (A10.1, A10.4, A10.5);
  `docs/V1-PROFILE.md` §3.4, §5, §6.3–6.4, §7.1–7.3, §14.2, §15.5; `docs/guarantee-tiers-DRAFT.md`, "Authority
  capture"
