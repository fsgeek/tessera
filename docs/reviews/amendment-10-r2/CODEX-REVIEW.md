# Non-author review: Amendment 10, revision 2

2026-10-17. **Result: revise before signing.** Eight findings: five MEDIUM and three LOW. No HIGH or CRITICAL defect found. The conditional UTC inequality is sound under A-UTC and the existing commitment/history assumptions. The ordered service-key classifier and authorization closure support the stated non-acceptance guarantee. The material corrections concern what the tolerance evidence establishes, counterfactual mining and proof selection, the plain custody explanation, and change accounting. This review makes no author ruling.

MEDIUM means a material correction to the proposed claim, its supporting argument, or its change record. LOW means a bounded precision or reproducibility correction that does not defeat either construction.

## Reviewed artifacts and validation

Read A10 in full, the tolerance evidence file including its embedded reproduction script, the complete decision memo, A9 in full at signing commit `2ad34890359c446efaebcb116388b8e9ffbf6428`, V1-PROFILE §5/§7/§14.2/§15.5 and its output provisions, and STE-STYLE in full. Also checked the memo's prior review and disposition to distinguish its recommendations from new evidence. Repository HEAD: `7d7f94d797048f96df9a2b129962a5604439f4ae`. A10 and the decision documents were untracked proposed material.

All A10 locators below refer to `docs/phase-0-prereg-amendment-10.md`; “evidence” means `docs/decisions/2026-10-17-a-utc-tolerance-evidence.md`. The reviewed A10 SHA-256 is `55f8a57ce0b5bafba50633069259605b5d29091748849ef9b24883f709367c8f`; the evidence SHA-256 is `71abfa3e5213bf4fc24aa592106b2bbef09f0731088717a06cad0f31c53be8d3`.

Cloned the primary dataset outside the workspace and verified HEAD equals the cited commit `1bb1c1b750dcc4633a54f01cbaaed8d789c3f4c0`. Extracted the evidence's fenced Python script verbatim and ran `python3 -I lag.py <dataset-repo>`. Its output was:

```text
559831 18.124000072479248 3917.6289999485016 1064.8840000629425 6135.137000083923 545 559718
```

These reproduce the reported block/window counts, median and maximum lag, largest window-minimum lag, minimum reported margin, and the 545-window MTP statistic. An additional calculation reproduced the median margin, `9908.319000005722` seconds, and the single-block threshold counts `93 / 20 / 5 / 0`. These are statistics of the retained observations, subject to F01 and F02. The header-timestamp CSV digest matches. The concatenated-data digest does not: F07.

Read the dataset's actual quality-check code and source descriptions. Its README confirms the two-hour QA restriction; the source descriptions confirm why the stratum files must be excluded. [Pinned dataset](https://github.com/bitcoin-data/block-arrival-times/tree/1bb1c1b750dcc4633a54f01cbaaed8d789c3f4c0), [QA implementation](https://github.com/bitcoin-data/block-arrival-times/blob/1bb1c1b750dcc4633a54f01cbaaed8d789c3f4c0/qa/block-timestamps/check-block-timestamps.py).

The mempool.space page was fetched directly and its 481-block count and −69/+82/41/40-second statistics match. Bowden et al. §II-B contains the cited header-order observations. Neither source supplies a production-clock bound. [mempool.space report](https://research.mempool.space/p/09defe3d-c836-44e7-b244-7f8434e72151), [Bowden et al.](https://arxiv.org/html/1801.07447v1#S2.SS2).

## Findings and exact fixes

### F01 — MEDIUM: the empirical conclusions drop the censoring and clock qualifications

**Locations:** A10 :73–74, :257–271; evidence :95–110 and :149–152.

The measurements reproduce. The limitations are candidly recorded in the technical body, but the interpretation says A-UTC held and the plain summary says measurements found no six-block failure. Those are stronger statements than this dataset establishes. The dataset rejects arrivals outside ±7200 seconds of header time, and no lower bound on observer clock error is supplied. Taking the earliest observer arrival can select a slow clock. Propagation delay alone makes arrival lag conservative; an unbounded negative clock error does not.

Writing an observer's recorded arrival as `a = r + propagation_delay + clock_error`, the inference `r − nTime ≤ a − nTime` needs `propagation_delay + clock_error ≥ 0`. Evidence :70 acknowledges that dependency. The interpretation and conclusion must retain it. The absence of retained observations between 3918 and 7200 seconds is descriptive evidence about this selected sample; it does not validate the excluded tail, the uncensored frequency of A-UTC failure, or an adversarial success probability. The sample also excludes windows with missing heights.

**Exact fix:** replace evidence :95–98 with:

> In every retained complete six-block window, at least one recorded arrival lag was at most 1064.9 s. The minimum computed U minus the inclusion block's recorded first-seen time was 6135.1 s; U's UTC interpretation remains conditional on A-UTC. If the selected observer readings do not understate production time, these observations support A-UTC for the sampled windows. Observer clock error is not bounded here. The dataset's ±7200 s quality filter and excluded incomplete windows prevent an inference about the frequency of A-UTC failures outside the retained sample.

Replace evidence :104–105's “distribution below the threshold is not censored” sentence with:

> Among the retained observations, none lies between 3918 s and 7200 s. This describes the selected sample; it does not remove the effect of the quality filter on inference about miner behaviour.

Replace the first conclusion bullet at evidence :149–152 with:

> [R] Δ = 7200 s and m = 6 remain a proposed trust tolerance. The retained observations show substantial recorded margins during ordinary operation, conditional on the observer-clock limitation. They do not validate the tolerance against an intentional timestamp coalition or establish a failure probability. Author acceptance of A-UTC remains necessary for the conditional UTC claim.

In the plain summary replace :73–74 with these bullets:

> - The retained measurements cover 2015 to 2026. In each complete set of six, one recorded arrival was no later than chain time plus 1065 seconds.
> - The dataset rejects arrival times more than two hours from the chain time. It cannot show failures beyond that limit.
> - Observer clocks can also be wrong. These measurements do not show that A-UTC was true.

Keep A10 :268–271's technical limitations. Do not replace them with an unconditional empirical assurance elsewhere.

### F02 — MEDIUM: the MTP count does not establish what consensus forces when the six miners change their timestamps

**Locations:** A10 :262–267; evidence :138–145.

The number 545 is correct for MTPs calculated from the actual header history. The inference “whatever the six miners did,” and the conclusion that most windows require controlling blocks outside those six, do not follow. Later MTPs in a window include earlier blocks of that same window. Changing those timestamps changes the later MTPs. The evidence itself mentions this dependency at :144 but then draws the stronger conclusion at :145; A10 repeats it.

**Concrete arithmetic counterexample:** fix the eleven preceding header times at `0, 600, …, 6000`. Let the next six production times and original header times be `11000, 11001, …, 11005`. Their production-minus-observed-MTP values are:

```text
8000, 7401, 6802, 6203, 5604, 5005
```

This window belongs to the group with at least one value at most 7200. Yet changing only the six new timestamps to `3001, 3002, …, 3006` satisfies `nTime > MTP` at every step, with no change to any preceding header, and all six timestamps lag production by 7999 seconds. This is a counterexample to the counterfactual inference, not a Bitcoin receipt or a measured attack.

**Exact fix:** replace evidence :142–145 with:

> At the observed header history, 559173 of the 559718 complete windows contain a block with first-seen minus MTP at most 7200 s. Holding that block's actual predecessors fixed, and assuming its recorded arrival does not precede production, the MTP rule forces that block's timestamp within the tolerance. This is a diagnostic of the observed history. It does not show that the six miners could not violate A-UTC by changing their timestamps: earlier changes within the window can lower later MTPs. No count of windows requiring control outside the six is established here.

Replace A10 :262–267 with:

> Consensus requires each timestamp to exceed the median of the preceding eleven header times. The evidence reproduces 545 windows in which every recorded first-seen-minus-MTP value exceeds 7200 s. These MTPs use the actual predecessor timestamps and the observer-clock qualification. The count does not bound a coalition changing the six timestamps, since changes within the window also change later MTPs. A majority coalition can sustain lagging timestamps; A-UTC is not consensus protection against that adversary.

The numerical table and script need no change for this correction.

### F03 — MEDIUM: lowest-height selection does not eliminate favourable proof presentation

**Locations:** A10 :256–257; evidence :42–44.

The selector fixes the lowest qualifying height **within the presented proof**. It does not force presentation of every available attestation, and height order does not make the maximum of a moving six-header window monotone. The categorical conclusion that presentation sensitivity cannot help is unsupported even for actual historical header times.

For example, the cited header list gives the following seven times at heights 376155–376161:

```text
1443230374, 1443229712, 1443229703, 1443230048,
1443230063, 1443230298, 1443230312
```

The six-header formula gives `1443237574` at h = 376155 and `1443237512` at h = 376156: moving one height later lowers the reported value by 62 seconds. These are formula evaluations, not evidence that one real receipt has both attestations. They refute the claimed monotonic reason for excluding favourable selection; the profile permits presentation-sensitive selection.

**Exact fix:** replace evidence :42–44 with:

> The verifier selects the lowest qualifying height in the presented proof. A presenter may still choose among available valid presentations, and later inclusion heights need not give larger U values. Under A-UTC for the selected six-block segment, every resulting U remains a valid conditional bound. Lowest-height selection supplies determinism for the presentation; it supplies no additional protection against selecting a segment where A-UTC fails.

Replace A10's “Lowest-height selection gives it no favourable choice” with:

> Lowest-height selection fixes the result within a presented proof, but does not eliminate choice among available presentations. The UTC assessment relies on A-UTC for the selected segment in every case.

Retain the evidence's existing warning that the illustrative α⁶ calculation is not a security probability for an adaptive presenter.

### F04 — MEDIUM: the plain custody rule excludes people rather than access paths

**Locations:** A10 :101–103; compare :450–458, A9 :326–332, profile §5 :389–407 and §14.2 item 1.

“Nobody with the DNS credential, the repository key or the AWS account can use the release key” is stronger than the registered rule. It prevents the same authorized person from holding operational credentials and separately authorizing a release. The technical requirement is that capture of those credentials/accounts confers no release-signing or release-authorization capability. The project retains one controller; technical access separation does not establish separate human control. This is a STE-STYLE faithfulness finding, not a request to change custody architecture.

**Exact fix:** replace :101–103 with:

> AWS means Amazon Web Services, the provider of the service's cloud account. Amendment 9 already requires these access limits:
>
> - The DNS credential and the repository key must not give access to the release key.
> - Access to the AWS account must not give access to the release key.
> - Hardware or offline software for the release key is acceptable only with a written procedure.

The existing following bullets give the procedure's contents. Explain AWS here at first use, as STE-STYLE rule 6 requires. The amendment's technical custody rule can stay as written.

### F05 — LOW: row 24 conflates failure of a sufficient assumption with failure of the numerical bound

**Locations:** A10 :544, with :254–255; evidence :22–25 and :37–41.

Row 24 says the assessment “fails if” all six miners set lagging timestamps, without stating the 7200-second threshold. A small ordinary lag is not failure of A-UTC. Even all six lags exceeding 7200 seconds makes A-UTC false, but need not make the existence bound numerically false. The body correctly calls A-UTC sufficient rather than minimal.

For example, let production times be `100000 + 600i` and timestamps `92700 + 600i`, i = 0…5. All six lags are 7300 seconds; the formula still gives `102900`, later than the inclusion production time `100000`. Also, six lagging timestamps need not imply that an attacker controlled all six miners: clock faults or coincident behaviour can satisfy the same failure condition.

**Exact fix:** replace row 24's failure clause with:

> A-UTC is false exactly when every one of the six confirming blocks has a header time more than 7200 s before its production. In that case the conditional UTC guarantee is unavailable; the computed value need not itself be false.

Replace evidence :37's “It must control the timestamps of all six consecutive blocks” with:

> To force failure independently of the other miners' behaviour, a backdater would need to make all six timestamps lag production by more than 7200 s. Failure can also occur without such control; it is the timestamp condition, not an attribution of miner intent.

Keep the clear necessary-condition formulation at evidence :22–25, and keep the fixed-experiment α⁶ illustration separate from a necessary attack capability or a failure probability.

### F06 — MEDIUM: row 32 adds prerequisites, and the definition of GATE contradicts row 33

**Locations:** A10 :119–124, :415–417, :552–555 and :571–575.

Row 32 is CLARIFY/K, but A9 :410–418 does not require a release to authorize the initial service-key entry at freeze or a successor listing before the window opens. Those are new timing prerequisites of the proposed listing. They are legitimate recommendations awaiting a ruling, not unchanged meaning. Row 33 correctly admits a gate **and scope** change, while the plain definition says a GATE “does not change a claim.” Cutting the listing conditionally removes its added protection, even though it leaves the old checks intact.

**Exact fix:** change row 32 to **GATE | G**, and change the plain GATE definition to:

> GATE: the change adds or changes a prerequisite, a trigger, or a cut order. The row states any scope change that follows.

Update the totals to **fifteen NARROW-CLAIM, one CORRECT, five CLARIFY, ten BROADEN and four GATE**. List the GATE rows as 32–35 and remove row 32 from the clarification list. Keep row 33's explicit loss of the added protection on a schedule cut. The successor requirement remains conditional on a separately registered rotation; this relabelling creates no automatic successor project.

### F07 — LOW: the concatenated-data digest is not reproduced by the stated command

**Location:** evidence :63–65 and §6.

At exactly the cited clean dataset commit, the timestamp CSV has the reported digest, but `cat data/*.csv | sha256sum` under this environment's C.UTF-8 collation gives:

```text
335249f1099fdd2a6cb1d7d82766912488bdf6d81588d1f12023c369bb6c0b4c
```

This differs from the document's `d83509d9…`. Python concatenation in sorted filename order gives the same `335249f1…` value. Excluding stratum files does not produce the document's digest either. The statistical reproduction succeeds, so this is a provenance/recipe correction, not evidence that those reported numbers are wrong.

**Exact fix:** specify the ordering and replace the digest with the value above for:

```sh
LC_ALL=C bash -c 'cat data/*.csv' | sha256sum
```

If another manifest/order was intended, record that exact manifest and its command instead. State explicitly that this all-files digest includes stratum CSVs, while the statistical calculation excludes them.

### F08 — LOW: the promised adjacent A-UTC qualification is not consistently present in standalone summary statements

**Locations:** A10 :58–60, :75–81 and :132; compare the explicit policy at :237–238.

The recommended technical existence claims and output object do carry A-UTC. However, the standalone formula bullet at :59 and rollover sentence at :80–81 use U without the adjacent qualification required by the review brief and the amendment itself. The glossary also calls U a “UTC time only if A-UTC is true.” The computed RFC 3339 value exists regardless of the assumption; what depends on A-UTC is its interpretation as an upper bound on existence.

**Exact fix:** use these local replacements:

> - Under A-UTC, U is a UTC upper bound: the latest chain time of the six confirming blocks, plus two hours.
> - The verifier reports U with its assumption identifier, `A-UTC-7200-6`, in `utc_assessment`.
> - U, conditional on A-UTC, is outside the six fields that later verifiers must reproduce. U does not change the verdict.

Replace the rollover calculation sentence with:

> The calculation of U, whose UTC claim depends on A-UTC, stays correct for the saved headers of older blocks.

Replace the U glossary entry with:

> Under A-UTC, a UTC upper bound: the latest chain time of the six confirming blocks, plus two hours.

Retain the definition and verifier non-check of A-UTC beside these statements. Arithmetic can be performed without establishing A-UTC; never present that arithmetic alone as an established UTC existence claim.

## Checks without a further finding

**UTC construction and contract.** The proof is `e < r(h*) ≤ r(j) ≤ nTime(j)+7200 ≤ max(nTime(h*…h*+5))+7200` for the j supplied by A-UTC. Inclusion is confirmation one, so the segment ends at h*+5. No new bound on service observation delay B−C is inferred. Guarantee 2 remains a chain-time statement. The wrapper contains the assumption identifier, is null exactly when T is null, stays outside the six stable fields, and does not establish service authenticity when reported with INVALID or UNVERIFIABLE. No seventh stable field or changed A9.4 contract is introduced.

**2106.** The explicit uint64 widening, non-modular addition and preserved-header boundary are correct. Direct evaluation of `4294967295 + 7200` gives `2106-02-07T08:28:15Z`. The text distinguishes old-receipt verification from defining timestamps for newly produced post-rollover Bitcoin blocks. DNSSEC serial-time unwrapping is not misapplied to Bitcoin.

**Key substitution.** The exact tuple match precedes overlap/horizon classification, including future prelisted matches. A shared endpoint is overlap. An unlisted tuple within an overlapping interval or the closed horizon is INVALID; a disjoint unlisted future interval is UNVERIFIABLE. Overall failure precedence remains in force. For append-only releases, the existing matching tuple, overlapping interval, or old closed horizon preserves every prior pass/INVALID conclusion of this check. A finite scratch enumeration of 117600 permitted single-addition comparisons found no change to such prior outcomes; this illustrates the construction, not implementation conformance or formal discharge. Pin extensions can still change selection and other results across different configurations.

The initial schedule's authorization is a trusted release-authority act, not something a release checker discovers from real-world channel assertions. Trustworthy authorization behaviour is expressly required. A captor lacking release authorization and the listed service-signing capability cannot make captor-key receipts pass this check. Neither the listing nor a horizon result is evidence that anybody detects or exposes a takeover. The targeted-release residual is stated. A8.3/A8.5 and previous formal runs are not misrepresented as evidence for the new mechanism.

**Issuer invariant.** “No receipt ships under keys that are not listed in a published release” is a valid added issuer duty. It supplements, rather than replaces, the existing complete-receipt shipping duty and the exact pair/window verifier check. V1 has exactly one listed entry; a successor remains unauthorized without the separately registered rotation and its release prerequisites. This is not a claim that arbitrary attacker-created receipts obey the honest issuer's duty.

**Custody gate.** At the preregistration level it is concrete enough to check: the existing profile requires the actual key, holder and implemented access boundary shown unusable by the three operational credentials/accounts; A10 adds a written authorization/signing/backup procedure, a dated custody-record reference and review before freeze. Hardware purchase alone is explicitly insufficient. Profile §14.2's bootstrap, rotation and bounded recovery requirements remain standing. Nothing reviewed supplies the actual custody evidence or closes independence. A completed procedure is not itself proof of independence. If independence fails, the author must receive the affected NARROW-MODEL; cutting the list does not repair the old trust boundary or authorize silently freezing a reduced claim.

**Table and decision status.** Rows 1–35 are present, unique and consecutive. Their current category counts reproduce as 15/1/6/10/3 in the order NARROW-CLAIM/CORRECT/CLARIFY/BROADEN/GATE. The quoted A9 source fragments match their cited lines at `2ad3489`; row 26 explicitly refers to text added by row 16 rather than pretending A9 contained it. The assembled C5 cell reconciles rows 4 and 17. Rows 15–16 and 20–35 are explicitly pending, with conditional application for options (a)/(e); no new recommendation is labelled an author ruling. F06 corrects the category meaning/count, not the row total or source locators.

**Future scope and plain style.** The old automatic V2 obligation is withdrawn. TSAs, a witnessed log and unresolved examiner requirements remain recorded candidates/questions. Conditional prerequisites for an optional future rotation do not require that rotation to happen. The plain summary otherwise uses short sentences, parallel bullets, technical identifiers and visibly proposed glossary additions. Its material fidelity problems are F01/F04/F08; AWS also needs the first-use explanation supplied in F04. No new architectural mechanism or future project is required to resolve these findings.

## Validation limits and disposition

No issuer/verifier implementation, conformance vector or formal-model run was added or executed. The reproduced observational numbers, arithmetic examples and finite classifier exercise do not establish A-UTC, deployed custody, empirical adversarial security or public capture visibility. Prospective vectors and profile updates remain prospective work following any author ruling.

Resolve the findings in the proposed documents, then obtain the author's own rulings on A10.1.1, A10.4 and A10.4.2. This review recommends no change to the central UTC inequality, the six-field contract, or the selected service-key construction. Only this review file was written in the repository.
