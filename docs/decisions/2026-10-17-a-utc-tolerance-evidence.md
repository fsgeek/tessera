# Evidence for the A-UTC tolerance (Δ = 7200 s, m = 6) (2026-10-17)

> **Status: RECOMMENDED (owner; the Codex review of the decision memo concurs), AUTHOR ADOPTED 2026-10-18 (see docs/reviews/amendment-10-r4/AUTHOR-RULINGS.md).** Drafted
> 2026-10-17 by Claude (Opus 5.5) for Amendment 10 §A10.1.1, which cites it. It justifies the tolerance of assumption
> A-UTC against the intended adversary. It does not establish that miners satisfy A-UTC: no data can. Adopting
> A-UTC is a trust assumption that the author's signature would accept; the verifier cannot check it.
>
> Labels: **[F]** fact, with source; **[A]** assumption; **[E]** estimate or interpretation; **[R]** recommendation.
> Mechanism details are from `docs/decisions/2026-10-17-utc-bound-and-capture-visibility.md` (the memo). Revised
> 2026-10-17 after the Codex review `docs/reviews/amendment-10-r2/CODEX-REVIEW.md` (F01, F02, F03, F05, F07 apply
> here; Codex's exact text); disposition in the same directory.

## 1. What A-UTC says and what would falsify it

**Notation (memo).** h* is the selected inclusion height of the receipt proof (confirmation one); h*+5 is
confirmation six. r(j) is the real (UTC) time at which block j was first produced. nTime(j) is its header time.

**[A] A-UTC (assumption_id `A-UTC-7200-6`).** At least one of the six blocks h* … h*+5 has
`nTime(j) ≥ r(j) − 7200 s`: its header time is no more than 7200 s before it was actually mined.

**Consequence (memo, Part 1; checked by Codex).** Under A-UTC and the registered commitment and history assumptions,
the bytes and both signatures existed before `U = max nTime(h* … h*+5) + 7200 s`.

**Failure condition.** A-UTC fails for a receipt exactly when **the miners of all six confirming blocks set lagging
timestamps**: every block h* … h*+5 has a header time more than 7200 s before it was actually mined. Only then can
U be earlier than the true existence time. (The weaker condition `max nTime + 7200 ≥ r(h*)` would itself suffice;
A-UTC is a sufficient one-sided assumption, not a minimal one.)

## 2. The intended adversary

A9's adversary includes "anyone who … backdates receipts" (A9:40). Against U, a backdater has bytes that exist only
at real time e, and wants a receipt whose U is earlier than e. The bytes must be committed in block h*, so
e < r(h*); a backdater gains only if all six header times lag. Three cases:

1. **A non-mining backdater** (a holder, a third party, or a captor of the service or its authority channels). It
   cannot set any header time. It can only choose when to stamp, and which presented proof to use. It succeeds only
   if a window of six consecutive blocks occurs in which every miner's timestamp lags by more than 7200 s. Section 3
   reports the recorded margins in historical windows, with the limits of that record.
2. **A backdater who bribes or controls miners.** To force failure independently of the other miners' behaviour, a
   backdater would need to make all six timestamps lag production by more than 7200 s. Failure can also occur
   without such control; it is the timestamp condition, not an attribution of miner intent. Consensus limits how far
   each timestamp may lag (section 4). If a coalition finds an independent share α of blocks, a fixed
   set of six is all theirs with probability α⁶: 7×10⁻⁴ at α = 0.3, 1.6% at α = 0.5 **[E]**. This is not a security
   probability against an adversary who chooses when to submit, retries, withholds blocks or selects among proofs.
   A coalition with a majority of hash power can keep timestamps behind real time without limit (A2.1).
3. **Selection of a favourable proof.** The verifier selects the lowest qualifying height in the presented proof.
   A presenter may still choose among available valid presentations, and later inclusion heights need not give
   larger U values. Under A-UTC for the selected six-block segment, every resulting U remains a valid conditional
   bound. Lowest-height selection supplies determinism for the presentation; it supplies no additional protection
   against selecting a segment where A-UTC fails.

**Why m = 6.** The six headers h* … h*+5 are already required, pinned and qualified for k = 6 (A2.1, profile §7.1).
U needs no new input. A larger m would need more headers; a smaller m would rest the claim on fewer miners. m = 6 is
not shown to be optimal **[F, Codex review]**.

**Why Δ = 7200 s.** It is an author-selected tolerance. It equals Bitcoin's node-local forward tolerance
(`MAX_FUTURE_BLOCK_TIME = 2*60*60`); that match is a convenience and does not validate it **[F, Codex review]**. The
data in section 3 show the observed margin under it.

## 3. Empirical header-time lag

### 3.1 Primary source: the Bitcoin Block Arrival Time Dataset

**[F] Source.** `bitcoin-data/block-arrival-times`, CC0 1.0, commit `1bb1c1b750dcc4633a54f01cbaaed8d789c3f4c0`
(2026-03-28), https://github.com/bitcoin-data/block-arrival-times . Each row gives height, header hash and the
millisecond time at which one observer node first received or connected the block. Observers include the KIT DSN
Bitcoin monitoring nodes (https://www.dsn.kastel.kit.edu/bitcoin/), 0xB10C's peer-observer and monitoring nodes, and
four independently operated Bitcoin Core nodes. Header times are from the dataset's
`qa/block-timestamps/block-timestamps.csv` (SHA-256
`85800b9110c2784f6711ebd348164f7de0a140692622251a4d8ee964a445046f`). All nineteen `data/*.csv` files, concatenated in
C-locale filename order, hash to `335249f1099fdd2a6cb1d7d82766912488bdf6d81588d1f12023c369bb6c0b4c`
(`LC_ALL=C bash -c 'cat data/*.csv' | sha256sum`, run in the dataset root). This all-files digest includes the two
`stratum_work_*` CSVs; the statistical calculation excludes them. *(Dated correction 2026-10-17, review F07: the
digest first given, `d83509d9…`, was not reproduced by the stated command, whose glob order depends on locale.)*

**Method.** For each height, *first-seen* is the earliest arrival across all observers. The `stratum_work_*` files
are excluded, because their row for height N records the arrival of block N−1. The lag of block j is
`first-seen(j) − nTime(j)`. A block is first seen after it is produced, so this lag is **an upper bound on
r(j) − nTime(j)**, the quantity A-UTC bounds, provided the observer clock is accurate. Computed 2026-10-17 by the
script in section 6.

**[F] Coverage.** 559,831 heights from 369,715 (2015-08-13) to 941,944 (2026-03-23), 97.8% of that range.

**[F] Lag of single blocks** (first-seen minus nTime, seconds):

| Statistic | Value |
|---|---|
| median | 18.1 |
| 25th / 75th percentile | 9.0 / 29.0 |
| 95th / 99th / 99.9th percentile | 48.4 / 80.0 / 237.0 |
| maximum | 3,917.6 (height 409,854, 2016) |
| blocks above 600 s / 1,800 s / 3,600 s / 7,200 s | 93 / 20 / 5 / 0 |
| blocks below 0 s (header time after first-seen) | 34,461 (6.2%); minimum −4,417.8 |

**[F] Six-block windows** (559,718 windows h … h+5 with all six heights covered):

| Statistic | Value |
|---|---|
| largest "smallest lag in the window" | 1,064.9 s |
| 99.9th percentile of "smallest lag in the window" | 30.1 s |
| U minus first-seen(h) (U computed as max nTime(h … h+5) + 7200) | minimum 6,135.1 s; median 9,908.3 s |
| X − 7200 = max nTime(h … h+5) − nTime(h) | median 2,727 s; 99th percentile 6,899 s |

**[E] Interpretation.** In every retained complete six-block window, at least one recorded arrival lag was at most
1064.9 s. The minimum computed U minus the inclusion block's recorded first-seen time was 6135.1 s; U's UTC
interpretation remains conditional on A-UTC. If the selected observer readings do not understate production time,
these observations support A-UTC for the sampled windows. Observer clock error is not bounded here. The dataset's
±7200 s quality filter and excluded incomplete windows prevent an inference about the frequency of A-UTC failures
outside the retained sample.

**[F] Limits of this source.**
- **Censoring at the threshold.** The dataset's CI (`qa/block-timestamps/check-block-timestamps.py`) fails if any
  arrival differs from its header time by more than 7200 s ("The listed timestamps might have been recorded during
  IBD or the system clock was wrong?"). The dataset therefore cannot contain a lag above 7200 s, whatever happened.
  Its zero count above 7200 s is not evidence. Among the retained observations, none lies between 3918 s and
  7200 s. This describes the selected sample; it does not remove the effect of the quality filter on inference about
  miner behaviour.
- **Observer clocks.** Lag includes propagation, observer delay and observer clock error. A fast observer clock
  inflates the lag (conservative); a slow one understates it. The negative lags (6.2% of blocks) show miner clock
  error, future-dated headers or observer clock error. The dataset does not separate them.
- **Missing heights.** Windows with a missing height (2.2% of heights) are excluded. If rows were removed for
  exceeding the CI threshold, the removal would hide exactly the windows of interest.
- **History, not adversary.** The sample shows ordinary miner behaviour from 2015 to 2026. It does not bound a
  coalition that sets lagging timestamps on purpose.

### 3.2 Corroborating sources

- **[F] mempool.space Block Time Report** (https://research.mempool.space/p/09defe3d-c836-44e7-b244-7f8434e72151).
  One observer, arrival over the mempool.space websocket versus header time, 481 blocks between heights 857,514
  and 858,080 (2024-08-19 to 2024-08-23): minimum −69 s, maximum +82 s, median 41 s, mean 40 s. The author describes
  it as "quick and dirty" and attributes the negative values to drifted clocks at some pools (Braiins, F2Pool,
  Foundry USA, Luxor, MARA Pool). Observer arrival, not production time.
- **[F] Bowden, Keeler, Krzesinski and Taylor, "Block arrivals in the Bitcoin blockchain", arXiv:1801.07447
  (2018), §II-B.** "Of the 500,000 blocks mined up to November 2017, 13,618 of them have a timestamp prior to that
  of the previous block and some 1,000 of them have timestamps more than 10 minutes prior to the previous block
  timestamp"; "Some inter-arrival times are more negative than −7,000 seconds but most are between −1,500 and 0
  seconds." The authors attribute out-of-order times largely to future-dated headers followed by correct ones, and
  to miners using the timestamp as an extra nonce. Our count from the dataset's header list over the same range is
  13,638; the source of the 20-block difference is not established.
- **[F] Chain-wide header order** (dataset header list, heights 1–942,357). 15,410 headers have nTime earlier than
  their predecessor's. The largest backward step is 7,125 s. Since height 700,000 (2021-09): 1,040 headers, largest
  backward step 2,032 s. A backward step measures disagreement between header times, not lag behind real time.

## 4. What consensus forces

**[F]** A header is invalid unless `nTime > MTP`, the median of the previous 11 header times (Bitcoin Core
`validation.cpp`, "time-too-old"). So the largest lag a miner of block j can choose is less than r(j) − MTP(j). If
r(j) − MTP(j) ≤ 7200 s, block j satisfies A-UTC whatever its miner does.

**[F] Measured** with first-seen as an upper bound on r(j), over the same 559,831 blocks: first-seen(j) − MTP(j)
has median 3,328 s, 99th percentile 7,824 s and maximum 21,779 s; it exceeds 7200 s for 1.9% of blocks. In only
**545 of 559,718** six-block windows (0.097%) did it exceed 7200 s at all six blocks.

**[E] Interpretation.** At the observed header history, 559173 of the 559718 complete windows contain a block with
first-seen minus MTP at most 7200 s. Holding that block's actual predecessors fixed, and assuming its recorded
arrival does not precede production, the MTP rule forces that block's timestamp within the tolerance. This is a
diagnostic of the observed history. It does not show that the six miners could not violate A-UTC by changing their
timestamps: earlier changes within the window can lower later MTPs. No count of windows requiring control outside
the six is established here.

## 5. Conclusion and what remains assumed

- **[R]** Δ = 7200 s and m = 6 remain a proposed trust tolerance. The retained observations show substantial
  recorded margins during ordinary operation, conditional on the observer-clock limitation. They do not validate the
  tolerance against an intentional timestamp coalition or establish a failure probability. Author acceptance of
  A-UTC remains necessary for the conditional UTC claim.
- **[A]** The author's signature on A10, if it adopts §A10.1.1, adopts A-UTC as a trust assumption of the UTC
  assessment. It does not establish that miners satisfy it. The verifier cannot check it; the bundle carries no
  evidence of production times.
- **Not decided here, recorded only:** whether a court or another examiner will accept A-UTC; whether a particular
  use needs qualified (eIDAS) timestamps. RFC 3161 tokens over `SHA256(A_sig)` are a recorded candidate, not an
  obligation (memo, U2).

## 6. Reproduction

Clone the dataset at the commit above into a fresh directory, keep the script elsewhere, and run
`python3 -I lag.py <repo>`. To check the input digest, run `LC_ALL=C bash -c 'cat data/*.csv' | sha256sum` in the
dataset root (C-locale filename order; all nineteen files, stratum files included). The script:

```python
import csv, sys, os, glob, statistics
repo = sys.argv[1]
nt = {int(h): int(t) for h, t in csv.reader(open(os.path.join(repo, 'qa/block-timestamps/block-timestamps.csv')))}
first = {}                                   # height -> earliest arrival (ms) across observers
for p in glob.glob(os.path.join(repo, 'data/*.csv')):
    if os.path.basename(p).startswith('stratum'): continue
    for r in csv.reader(open(p)):
        h, ms = int(r[0]), int(r[2])
        if h in nt and (h not in first or ms < first[h]): first[h] = ms
lag = {h: first[h] / 1000 - nt[h] for h in first}
mtp = lambda h: sorted(nt[h - i] for i in range(1, 12))[5]
room = {h: first[h] / 1000 - mtp(h) for h in first}
wins = [h for h in lag if all(h + i in lag for i in range(6))]
win_min = [min(lag[h + i] for i in range(6)) for h in wins]
margin = [max(nt[h + i] for i in range(6)) + 7200 - first[h] / 1000 for h in wins]
all_room = sum(1 for h in wins if all(room[h + i] > 7200 for i in range(6)))
print(len(lag), statistics.median(lag.values()), max(lag.values()), max(win_min), min(margin), all_room, len(wins))
```
