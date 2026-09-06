You are a non-author FALSIFICATION reviewer for a TLA+ model in a pre-registered formal-methods project. You are jailed to the files in this directory; nothing else exists. Read all of them. The .tla files are the models (a correct model plus one or more deliberately broken companions), the .cfg files are TLC configurations, the .out files are TLC's committed output, and the REGISTERED-*.txt / A2.*.txt files are the signed property text the model claims to discharge; A1.3.txt is the registered adversary.

Your job is to try to BREAK the correspondence between the model and the registered text, not to summarise it. Do all of the following and report only what you verified by reading the files:

1. Correspondence audit: for each invariant or property checked in the .cfg, quote the registered sentence it claims to discharge, and say whether the TLA+ formula actually says that — name every place the formula is weaker, stronger, or about a different quantity than the prose. Name any registered clause with no formula at all.
2. Vacuity: identify the vacuity witnesses (state predicates expected to be reachable) and confirm from the .out files that they fired; name any invariant that could be true vacuously because a guard is never enabled.
3. Attack attempts: propose at least three concrete traces (sequences of actions with values) that a reader would expect to violate the property, and for each say whether the model makes it representable and, if representable, which conjunct rejects it — cite line numbers. If a trace is UNREPRESENTABLE in the model, say so explicitly; unrepresentable attacks are the most important finding.
4. Companions: for each broken companion, state from its .out which invariants went red, whether that is exactly the named set, and whether a companion "could not fail" for a reason unrelated to the defect it is supposed to exhibit.
5. Scoped abstractions: list every abstraction the module names (in comments) and any abstraction you can see that the module does NOT name.
6. Verdict on the module header's honesty: does its "proves / does not prove" text (or equivalent) say what the checked formulas discharge, no more?

Output a markdown document of at most 220 lines with those six headings, citing file:line for every claim. Do not praise. Do not use "obviously". If you cannot run TLC (you cannot), say every claim is from reading, not re-running.

All files are inlined below because you have no shell. TLC .out files are trimmed to their invariant/error/summary lines plus their final 40 lines; cite them by inlined line number. Cite .tla/.cfg/.txt files by their inlined line numbers (cat -n).

===== FILE: A1.3.txt =====
     1	## A1.3 The adversary model (explicit capabilities)
     2	
     3	The Band 0 adversary can, at minimum:
     4	
     5	1. **Alter** any bytes of a package, receipt, manifest, or wrapper after
     6	   issue.
     7	2. **Strip, reorder, or duplicate** signatures within the signature set.
     8	3. **Substitute keys** — including choosing keypairs *after* seeing valid
     9	   signatures (the DSKS capability of P3) — and always self-sign with keys
    10	   it holds (possession is free to the adversary; see P10).
    11	4. **Replay** valid packages, receipts, or manifests in other contexts, and
    12	   re-frame objects across the P7 type boundaries.
    13	5. **Craft manifests** freely, and anchor anything: anchoring proves
    14	   existence at a time, not authority (A1.5, A1.6).
    15	6. **Control any proper subset of the external manifest-authority
    16	   channels** (P10).

===== FILE: A2.1-A2.3.txt =====
     1	## A2.1 "Confirmed within δ": one predicate, both sides
     2	
     3	**Vocabulary.** The anchor transaction is included in the block at height
     4	`h`. Confirmation count follows the Bitcoin convention: the including
     5	block is the first confirmation, so `c = tip_height − h + 1`, and the
     6	block that grants the k-th confirmation has height `h + k − 1`. Define
     7	
     8	    confirmed_at  :=  timestamp(block at height h + k − 1)
     9	
    10	**The rule.** Issuance is complete only if
    11	
    12	    confirmed_at  ≤  declared_issue_time + δ
    13	
    14	The issuer evaluates this conjunct **as part of the full three-conjunct
    15	temporal predicate** (the P5 temporal test inside `VALID_STRICT`; all
    16	three A2.2 conjuncts — not the whole verdict, which contains more than
    17	the temporal test) before shipping: under
    18	skewed, non-monotonic block timestamps the confirmation conjunct does
    19	not imply the anchor-time conjunct, so shipping on this conjunct alone
    20	could ship a receipt the verifier rejects (surfaced by the bridge model,
    21	`formal/tla/P5cP5P6_Bridge.tla`, 2026-07-21). The verifier evaluates the
    22	same conjuncts on the same chain observables at verification (A2.2),
    23	**under the issuance policy's tolerances**: the verifier-owns-tolerances
    24	discipline permits stricter verifier values of either tolerance (a
    25	stricter δ′ < δ, or a stricter ε′ on the anchor-time lower bound), and
    26	such a verifier may reject honestly-shipped receipts — the
    27	no-disagreement guarantee below is scoped to verification under the
    28	issuance policy's δ and ε.
    29	**Clock roles (ruling, 2026-07-21).** Chain time and wall time hold
    30	separate, explicitly-ranked roles. **Chain time governs evidence:** the
    31	three-conjunct predicate above, evaluated identically by issuer and
    32	verifier on the designated blocks' timestamps. **Wall time governs the
    33	attempt lifecycle:** the service waits through `declared + δ + S` before
    34	treating an attempt as expired, where S ≥ 0 is an **operational slack
    35	constant** joining δ, ε, k, N for ratification at Band 0 exit (working
    36	default S = 24 h, sized to the observation path — outages and polling,
    37	not timestamp skew alone). **No global bound on the backward observation
    38	lag is assumed.** Writing C = `confirmed_at` and B = the service's
    39	wall-clock observation of the designated block: Bitcoin consensus
    40	provides no finite bound on B − C (median-time-past and the two-hour
    41	future rule bound the forward direction only), and B additionally
    42	absorbs the entire observation path — network and header-store delay,
    43	polling, outage and recovery, wall-clock error. Registering a hard
    44	bound would assert, at Phase 0, a property of an operational stack that
    45	does not yet exist. Instead the guarantee is registered **conditionally
    46	on the observable antecedent**: *if B − C ≤ S for an attempt whose
    47	predicate holds, that attempt has a live shipping opportunity at
    48	eligibility* (slack-parameter analysis,
    49	`formal/tla/P5cP5P6_BridgeSlack.tla` and its `_Latch` variant;
    50	predictions-first record in
    51	`docs/reviews/2026-07-21-claude-predictions-slack-bench.md`). Since B
    52	and C are both observable, a violated antecedent is a detectable
    53	operating-envelope event, not a silently failed assumption. Timeliness
    54	is **latched at eligibility**: an attempt eligible within the envelope
    55	cannot be expired by later packaging or scheduling delay —
    56	eligible/finalizing, shipped, and expired/refused are mutually
    57	exclusive states (a construction obligation on the implementation,
    58	registered with the ruling). An attempt whose lag exceeds S may be
    59	refused; a chain-valid artifact of such an attempt remains
    60	cryptographically valid and evidentially admissible but carries **no
    61	protocol standing** (A2.4; enforcing that distinction against later
    62	publication is Amendment 3's lineage/standing obligation). If
    63	operational evidence later supports an SLA-style hard bound, it may
    64	enter a **deployment profile** with monitoring and an explicit
    65	violation outcome — never this pre-registration's assumption set. What
    66	the opportunity guarantee buys is opportunity, not outcome: "every
    67	timely-eligible attempt ships" is a contract obligation on the
    68	implementation, the same proof-versus-contract split as A2.3's refusal.
    69	
    70	**Boundary ties, registered per clock.** The chain-side predicate is
    71	stateless: at exactly `confirmed_at = declared + δ` it holds, and holds
    72	identically whenever evaluated — there is no chain-side race. The
    73	wall-side boundary is **resolved by the latch, not raced** (round-3
    74	repair, 2026-07-21: an earlier draft of this paragraph carried the
    75	fused-clock race forward; under latched eligibility there is none).
    76	Eligibility observed at exactly `B = declared + δ + S` is timely — the
    77	boundary is **inclusive and latch-winning**, matching the mechanized
    78	form (`burialAtWall <= declared + Delta + Slack` in the `_Latch`
    79	companion) — so such an attempt latches eligible/finalizing and cannot
    80	expire. Expiry (on the final attempt, refusal) applies only **strictly
    81	after** the boundary, and only to attempts with no timely-latched
    82	eligibility. Atomicity of the latch against the expiry transition is
    83	part of the mutual-exclusion construction obligation (A2.3). If the
    84	predicate fails at issuance time, the attempt is discarded and
    85	re-issued per the P5 corollary, subject to the attempt bound of A2.3.
    86	
    87	**Why chain time on both sides.** A wall-clock ship rule ("ship if depth k
    88	by `now ≤ declared + δ`") and a block-timestamp verifier check can
    89	disagree at the δ boundary by the consensus-bounded skew (block timestamps
    90	may run up to about two hours ahead of network-adjusted time). Defining
    91	the rule once, on the chain-visible quantity, removes the divergence: **no
    92	honestly-shipped receipt can fail the verifier's confirmation conjunct
    93	under the issuance policy's δ**, and the issuer's ship rule and the
    94	verifier predicate become the same intended statement about the same
    95	observable under the declared abstractions — the correspondence A1.4
    96	demands, asserted here and checked mechanically by the bridge model
    97	(`formal/tla/P5cP5P6_Bridge.tla`; its own non-author review pending).
    98	P5c's fused-clock guard (`now ≤ declared + δ` at depth k) is a locally
    99	*stronger* condition that implies the chain predicate under that
   100	module's single-clock abstraction; with the clocks decoupled, the
   101	bridge's `Ship` evaluates the chain quantities directly.
   102	
   103	**Named residuals.**
   104	
   105	- *Adversarial timestamping.* A miner can set `timestamp(h + k − 1)`
   106	  forward within the consensus bound, pushing an honest issuance into the
   107	  tail case. This is a griefing surface bounded to hours against δ = 72
   108	  hours; it can force a re-issue, never a false verdict.
   109	- *Non-monotonic timestamps.* Block timestamps are not monotonic;
   110	  `confirmed_at` may even precede `anchor_time`. The predicate is a single
   111	  comparison on one designated block and is well-defined regardless; no
   112	  monotonicity is assumed.
   113	- *`confirmed_at` is a proxy, including backward skew.* The observable is
   114	  the designated block's header timestamp — the chosen chain-time proxy
   115	  for burial, not a measurement of when depth k was reached in wall-clock
   116	  time. Median-time-past rules allow a block mined after a real-time
   117	  deadline to carry an in-window timestamp (the mirror of the
   118	  forward-skew griefing above). The predicate is well-defined on the
   119	  proxy; wall-clock burial lateness is not what it measures.
   120	- *Header provenance.* The conjunct's verdict is only as trustworthy as
   121	  the headers it is evaluated over. Bundled headers form a candidate
   122	  chain segment, not proof of canonicity: a privately-mined in-window
   123	  fork presented in a bundle, or a lying header store, yields false
   124	  acceptance under naive stateless evaluation. Header authentication
   125	  against the canonical chain — proof-of-work validity, cumulative-work
   126	  or checkpoint anchoring, store identity pinned in declared verifier
   127	  policy, bundle/store conflict rules — is part of the A2.2 evidence
   128	  obligation; its full specification is deferred to that obligation's
   129	  discharge, not silently assumed here.
   130	
   131	**Model-convention pin (off-by-one, fixed here so it cannot drift).**
   132	P5c's `depth` variable counts blocks mined *after* inclusion (`depth = 0`
   133	at inclusion), so `depth ≥ DepthK` corresponds to `c ≥ DepthK + 1`. The
   134	correspondence mapping instantiates **`DepthK = k − 1`** (for the strict
   135	default k = 6: `DepthK = 5`). δ, ε, k remain ratified (or revised, on the
   136	record) at Band 0 exit, as registered; δ's 72-hour sizing already included
   137	aggregation-to-confirmation lag, so this amendment does not move it.
   138	
   139	---
   140	
   141	## A2.2 P5, amended: the strict temporal check gains a third conjunct
   142	
   143	`VALID_STRICT` now requires all of:
   144	
   145	    declared_issue_time − ε  ≤  anchor_time                       (unchanged)
   146	    anchor_time              ≤  declared_issue_time + δ           (unchanged)
   147	    confirmed_at             ≤  declared_issue_time + δ           (new)
   148	
   149	Consequences, stated explicitly:
   150	
   151	- The **chain-late subclass** of the A2.0 abandoned-anchor artifact
   152	  (`confirmed_at > declared + δ`) is **rejected outright** — its
   153	  `confirmed_at` exceeds its own window. Within this system the conjunct
   154	  rejects *only* such artifacts: strict issuance ships nothing that fails
   155	  it (A2.1). An operationally abandoned but chain-valid artifact passes
   156	  this conjunct and is governed instead by the A2.1/A2.4 standing rules
   157	  (no protocol standing; closure of the two-receipts residue is
   158	  Amendment 3's obligation, per A2.0).
   159	- **Evidence obligation.** The verifier must evaluate `confirmed_at`
   160	  statelessly (P9): block headers `h … h + k − 1` are available either
   161	  archived in the bundle or from the verifier-distributed header store the
   162	  anchor check already requires — the same trust-configuration pattern as
   163	  A1.5's historical trust-anchor store. Header *authentication* rules
   164	  (canonicity, work validation, store identity in declared policy,
   165	  bundle/store conflict resolution — the header-provenance residual of
   166	  A2.1) are part of this obligation. This joins the H1a evidence
   167	  obligations.
   168	- **Waiver status.** Temporal-anchor consistency is already non-waivable
   169	  (A1.2.1); the new conjunct is part of it. The P4 partition applies
   170	  inside it: performed-and-failed → `INVALID`; unperformable (headers
   171	  unavailable) → `UNVERIFIABLE`; neither is promotable.
   172	
   173	---
   174	
   175	## A2.3 The re-issue loop terminates: bounded attempts, fail-closed refusal
   176	
   177	As registered, the P5 corollary's re-issue rule was an unbounded loop, and
   178	its dominant triggers — fee spikes, congestion, calendar outage — are
   179	*correlated across attempts*: retrying under the same conditions is not a
   180	fresh draw, so "re-issue until it works" can livelock. Fail-closed means
   181	issuance must be able to end in refusal, not only in success.
   182	
   183	Amended: issuance makes at most **N attempts**. The expiry clock is the
   184	**wall clock** (A2.1 clock roles): an attempt expires when wall time
   185	passes `declared + δ + S`, except that timely-latched eligibility
   186	excludes expiry — eligible/finalizing, shipped, and expired/refused are
   187	mutually exclusive states (construction obligation, registered with the
   188	ruling). Exhausting them obligates
   189	the implementation to terminate issuance in an **explicit refusal, durably
   190	recorded; reporting is a delivery obligation to be registered in
   191	Amendment 3** — a first-class protocol outcome, not an error path. N is a
   192	protocol constant ratified at Band 0 exit alongside δ, ε, k, and S
   193	(working default **N = 3**; per the A2.1 clock-roles ruling each
   194	attempt's lifecycle is wall-governed through δ + S, so N attempts give
   195	a **nominal lifecycle budget** of N × (δ + S) — twelve days at the
   196	working defaults δ = 72 h, S = 24 h — a nominal budget, not a proven
   197	wall-clock bound on the process; see the model note).
   198	[**Note:** refusal as a separate delivery obligation added 2026/07/21 per
   199	review process/response.]
   200	
   201	Model note: P5c's `MaxAttempts` is hereby promoted from a state-space
   202	bound to protocol semantics. The refusal state is modeled by **atomic
   203	entry** (the transition expiring the final attempt's window records the
   204	refusal in the same step; checked, with a broken companion red on
   205	exactly the silent-deadlock invariant among the checked set — review
   206	archived in
   207	`docs/reviews/2026-07-20-codex-p5c-refusal-review.md`). Scope of proof
   208	versus contract, per that review: the model proves the *conditional
   209	safety half* — the refusal state is entered atomically and latches; it
   210	does not prove the crossing occurs (no fairness is assumed), so
   211	**termination is a contract obligation on the implementation, not a
   212	proven liveness property**. The unbounded "eventually ships" claim
   213	likewise remains explicitly unproven. Storage durability, retrievability,
   214	and reporting of the refusal record are implementation/handoff
   215	obligations to be registered in Amendment 3 (planned, not yet in force).
   216	[**Note:** model-note scope split added 2026/07/21, same review cycle.]
   217	
   218	---
   219	

===== FILE: P5c_IssuanceProtocol_Broken.cfg =====
     1	\* MaxTime raised to 14 with the main cfg (2026-07-20) — constants are
     2	\* kept identical across companions so the only difference is the module.
     3	CONSTANTS
     4	  MaxTime = 14
     5	  Delta = 3
     6	  DepthK = 2
     7	  MaxAttempts = 3
     8	
     9	INIT Init
    10	NEXT Next
    11	
    12	INVARIANTS
    13	  NoShippedOrphan

===== FILE: P5c_IssuanceProtocol_Broken.out =====
1:TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)
11:Starting... (2026-07-20 21:24:42)
13:Finished computing initial states: 1 distinct state generated at 2026-07-20 21:24:42.
14:Error: Invariant NoShippedOrphan is violated.
15:Error: The behavior up to this point is:
71:29 states generated, 24 distinct states found, 10 states left on queue.
74:Finished in 00s at (2026-07-20 21:24:42)
----- final 40 lines -----
     1	/\ attempts = 1
     2	/\ shipped = FALSE
     3	
     4	State 3: <Tick line 40, col 3 to line 45, col 81 of module P5c_IssuanceProtocol_Broken>
     5	/\ now = 1
     6	/\ depth = 1
     7	/\ reorgs = 0
     8	/\ declared = 0
     9	/\ refused = FALSE
    10	/\ anchorAt = 0
    11	/\ shippedOrphaned = FALSE
    12	/\ attempts = 1
    13	/\ shipped = FALSE
    14	
    15	State 4: <Ship line 62, col 3 to line 67, col 34 of module P5c_IssuanceProtocol_Broken>
    16	/\ now = 1
    17	/\ depth = 1
    18	/\ reorgs = 0
    19	/\ declared = 0
    20	/\ refused = FALSE
    21	/\ anchorAt = 0
    22	/\ shippedOrphaned = FALSE
    23	/\ attempts = 1
    24	/\ shipped = TRUE
    25	
    26	State 5: <Reorg line 54, col 3 to line 58, col 60 of module P5c_IssuanceProtocol_Broken>
    27	/\ now = 1
    28	/\ depth = 0
    29	/\ reorgs = 1
    30	/\ declared = 0
    31	/\ refused = FALSE
    32	/\ anchorAt = -1
    33	/\ shippedOrphaned = TRUE
    34	/\ attempts = 1
    35	/\ shipped = TRUE
    36	
    37	29 states generated, 24 distinct states found, 10 states left on queue.
    38	The depth of the complete state graph search is 5.
    39	The average outdegree of the complete state graph is 2 (minimum is 1, the maximum 2 and the 95th percentile is 2).
    40	Finished in 00s at (2026-07-20 21:24:42)

===== FILE: P5c_IssuanceProtocol_BrokenSilent.cfg =====
     1	\* EXPECTED: RED on NoSilentDeadlock — the separately enabled Refuse can
     2	\* be postponed past the final deadline crossing, so the silent-deadlock
     3	\* state is reachable. The _Green companion cfg proves every OTHER
     4	\* invariant still holds, i.e. the break is isolated to exactly the
     5	\* deadlock invariant AMONG THE CHECKED SET (Codex finding 4 scoping).
     6	CONSTANTS
     7	  MaxTime = 14
     8	  Delta = 3
     9	  DepthK = 2
    10	  MaxAttempts = 3
    11	
    12	INIT Init
    13	NEXT Next
    14	
    15	INVARIANTS
    16	  NoShippedOrphan
    17	  ShippedIsSound
    18	  ExpiredCannotShip
    19	  RefusedOnlyWhenExhausted
    20	  NoSilentDeadlock
    21	
    22	PROPERTIES
    23	  RefusalLatched

===== FILE: P5c_IssuanceProtocol_BrokenSilent_Green.cfg =====
     1	\* The isolation control: every invariant EXCEPT NoSilentDeadlock, on the
     2	\* broken-silent module. EXPECTED: GREEN — establishing that the
     3	\* _BrokenSilent break is red on exactly the deadlock invariant among the
     4	\* checked set, and nothing else in it (Refuse's guard is honest, the
     5	\* latch holds, ship-side invariants untouched).
     6	CONSTANTS
     7	  MaxTime = 14
     8	  Delta = 3
     9	  DepthK = 2
    10	  MaxAttempts = 3
    11	
    12	INIT Init
    13	NEXT Next
    14	
    15	INVARIANTS
    16	  NoShippedOrphan
    17	  ShippedIsSound
    18	  ExpiredCannotShip
    19	  RefusedOnlyWhenExhausted
    20	
    21	PROPERTIES
    22	  RefusalLatched

===== FILE: P5c_IssuanceProtocol_BrokenSilent_Green.out =====
1:TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)
11:Starting... (2026-07-20 21:24:44)
13:Finished computing initial states: 1 distinct state generated at 2026-07-20 21:24:44.
14:Model checking completed. No error has been found.
16:  because two distinct states had the same fingerprint:
18:3825 states generated, 2310 distinct states found, 0 states left on queue.
21:Finished in 00s at (2026-07-20 21:24:44)
----- final 40 lines -----
     1	TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)
     2	Warning: Please run the Java VM which executes TLC with a throughput optimized garbage collector by passing the "-XX:+UseParallelGC" property.
     3	(Use the -nowarning option to disable this warning.)
     4	Running breadth-first search Model-Checking with fp 117 and seed -3223071300083296023 with 1 worker on 128 cores with 30688MB heap and 64MB offheap memory [pid: 79961] (Linux 6.18.33.2-microsoft-standard-WSL2 amd64, Ubuntu 11.0.31 x86_64, MSBDiskFPSet, DiskStateQueue).
     5	Parsing file /home/tony/projects/tessera/formal/tla/P5c_IssuanceProtocol_BrokenSilent.tla
     6	Parsing file /tmp/Integers.tla
     7	Parsing file /tmp/Naturals.tla
     8	Semantic processing of module Naturals
     9	Semantic processing of module Integers
    10	Semantic processing of module P5c_IssuanceProtocol_BrokenSilent
    11	Starting... (2026-07-20 21:24:44)
    12	Computing initial states...
    13	Finished computing initial states: 1 distinct state generated at 2026-07-20 21:24:44.
    14	Model checking completed. No error has been found.
    15	  Estimates of the probability that TLC did not check all reachable states
    16	  because two distinct states had the same fingerprint:
    17	  calculated (optimistic):  val = 1.9E-13
    18	3825 states generated, 2310 distinct states found, 0 states left on queue.
    19	The depth of the complete state graph search is 23.
    20	The average outdegree of the complete state graph is 1 (minimum is 0, the maximum 3 and the 95th percentile is 2).
    21	Finished in 00s at (2026-07-20 21:24:44)

===== FILE: P5c_IssuanceProtocol_BrokenSilent.out =====
1:TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)
11:Starting... (2026-07-20 21:24:43)
13:Finished computing initial states: 1 distinct state generated at 2026-07-20 21:24:43.
14:Error: Invariant NoSilentDeadlock is violated.
15:Error: The behavior up to this point is:
181:1207 states generated, 798 distinct states found, 198 states left on queue.
184:Finished in 00s at (2026-07-20 21:24:43)
----- final 40 lines -----
     1	/\ attempts = 3
     2	/\ shipped = FALSE
     3	
     4	State 13: <Tick line 54, col 3 to line 58, col 34 of module P5c_IssuanceProtocol_BrokenSilent>
     5	/\ now = 10
     6	/\ depth = 0
     7	/\ reorgs = 0
     8	/\ declared = 8
     9	/\ refused = FALSE
    10	/\ anchorAt = -1
    11	/\ shippedOrphaned = FALSE
    12	/\ attempts = 3
    13	/\ shipped = FALSE
    14	
    15	State 14: <Tick line 54, col 3 to line 58, col 34 of module P5c_IssuanceProtocol_BrokenSilent>
    16	/\ now = 11
    17	/\ depth = 0
    18	/\ reorgs = 0
    19	/\ declared = 8
    20	/\ refused = FALSE
    21	/\ anchorAt = -1
    22	/\ shippedOrphaned = FALSE
    23	/\ attempts = 3
    24	/\ shipped = FALSE
    25	
    26	State 15: <Tick line 54, col 3 to line 58, col 34 of module P5c_IssuanceProtocol_BrokenSilent>
    27	/\ now = 12
    28	/\ depth = 0
    29	/\ reorgs = 0
    30	/\ declared = 8
    31	/\ refused = FALSE
    32	/\ anchorAt = -1
    33	/\ shippedOrphaned = FALSE
    34	/\ attempts = 3
    35	/\ shipped = FALSE
    36	
    37	1207 states generated, 798 distinct states found, 198 states left on queue.
    38	The depth of the complete state graph search is 15.
    39	The average outdegree of the complete state graph is 1 (minimum is 0, the maximum 3 and the 95th percentile is 2).
    40	Finished in 00s at (2026-07-20 21:24:43)

===== FILE: P5c_IssuanceProtocol_BrokenSilent.tla =====
     1	------------------ MODULE P5c_IssuanceProtocol_BrokenSilent ------------------
     2	(***************************************************************************)
     3	(* Tessera Band 0 — P5c refusal semantics, DELIBERATELY BROKEN: the       *)
     4	(* construction the round-3 review warned against, implemented verbatim.  *)
     5	(* "Merely adding a separately enabled Refuse action does not show that   *)
     6	(* it eventually fires: TLA+ requires a liveness property and, commonly,  *)
     7	(* an appropriate fairness assumption when an enabled action could        *)
     8	(* otherwise be postponed." Here Refuse IS a separately enabled action    *)
     9	(* and there is NO fairness — so the state "final window expired, nothing *)
    10	(* shipped, no refusal recorded" is reachable: the silent-deadlock STATE  *)
    11	(* the atomic-entry construction makes unrepresentable.                    *)
    12	(*                                                                          *)
    13	(* Expected result: TLC VIOLATES NoSilentDeadlock — shortest trace is     *)
    14	(* the straight-line run to exhaustion, ending in the Tick that crosses   *)
    15	(* the final deadline with Refuse not yet fired. Every OTHER invariant    *)
    16	(* of the main module must HOLD (checked by the _Green cfg): Refuse's     *)
    17	(* guard is honest (RefusedOnlyWhenExhausted), nothing unsets refused     *)
    18	(* (RefusalLatched), and the ship-side invariants are untouched. Red on   *)
    19	(* exactly the deadlock invariant — AMONG THE CHECKED SET (Codex          *)
    20	(* finding 4): the red run plus the _Green control demonstrate isolation  *)
    21	(* over the enumerated invariants and property, not absence of every      *)
    22	(* conceivable semantic difference. Within that scope the point stands:   *)
    23	(* NoSilentDeadlock isolates the atomicity of the entry, not any other    *)
    24	(* property of the refusal design.                                         *)
    25	(*                                                                          *)
    26	(* Identical state space and actions except: Tick does not record the     *)
    27	(* refusal; a separate Refuse action does, whenever it gets around to it.  *)
    28	(***************************************************************************)
    29	EXTENDS Integers
    30	
    31	CONSTANTS MaxTime, Delta, DepthK, MaxAttempts
    32	
    33	ASSUME Delta \in Nat /\ DepthK \in Nat \ {0} /\ MaxTime \in Nat
    34	       /\ MaxAttempts \in Nat \ {0}
    35	
    36	NoAnchor == -1
    37	
    38	VARIABLES now, declared, anchorAt, depth, shipped, shippedOrphaned,
    39	          attempts, reorgs, refused
    40	
    41	vars == <<now, declared, anchorAt, depth, shipped, shippedOrphaned,
    42	          attempts, reorgs, refused>>
    43	
    44	Init ==
    45	  /\ now = 0 /\ declared = 0
    46	  /\ anchorAt = NoAnchor /\ depth = 0
    47	  /\ shipped = FALSE /\ shippedOrphaned = FALSE
    48	  /\ attempts = 1 /\ reorgs = 0
    49	  /\ refused = FALSE
    50	
    51	(* THE BREAK: Tick advances time but records nothing — crossing the final *)
    52	(* deadline leaves refused = FALSE until Refuse happens to fire.           *)
    53	Tick ==
    54	  /\ now < MaxTime
    55	  /\ now' = now + 1
    56	  /\ depth' = IF anchorAt # NoAnchor /\ depth < DepthK THEN depth + 1 ELSE depth
    57	  /\ UNCHANGED <<declared, anchorAt, shipped, shippedOrphaned, attempts,
    58	                 reorgs, refused>>
    59	
    60	Anchor ==
    61	  /\ ~shipped /\ anchorAt = NoAnchor
    62	  /\ anchorAt' = now /\ depth' = 0
    63	  /\ UNCHANGED <<now, declared, shipped, shippedOrphaned, attempts, reorgs,
    64	                 refused>>
    65	
    66	Reorg ==
    67	  /\ anchorAt # NoAnchor /\ depth < DepthK
    68	  /\ reorgs < 2
    69	  /\ anchorAt' = NoAnchor /\ depth' = 0 /\ reorgs' = reorgs + 1
    70	  /\ shippedOrphaned' = (shipped \/ shippedOrphaned)
    71	  /\ UNCHANGED <<now, declared, shipped, attempts, refused>>
    72	
    73	Ship ==
    74	  /\ ~shipped /\ anchorAt # NoAnchor
    75	  /\ depth >= DepthK
    76	  /\ now <= declared + Delta
    77	  /\ shipped' = TRUE
    78	  /\ UNCHANGED <<now, declared, anchorAt, depth, shippedOrphaned, attempts,
    79	                 reorgs, refused>>
    80	
    81	Reissue ==
    82	  /\ ~shipped /\ now > declared + Delta
    83	  /\ attempts < MaxAttempts
    84	  /\ declared' = now /\ anchorAt' = NoAnchor /\ depth' = 0
    85	  /\ attempts' = attempts + 1
    86	  /\ UNCHANGED <<now, shipped, shippedOrphaned, reorgs, refused>>
    87	
    88	(* The separately enabled Refuse: guard is the honest exhaustion          *)
    89	(* condition (so RefusedOnlyWhenExhausted still holds), but nothing       *)
    90	(* forces it to fire before — or ever after — the deadline crossing.       *)
    91	Refuse ==
    92	  /\ ~shipped /\ ~refused
    93	  /\ attempts = MaxAttempts /\ now > declared + Delta
    94	  /\ refused' = TRUE
    95	  /\ UNCHANGED <<now, declared, anchorAt, depth, shipped, shippedOrphaned,
    96	                 attempts, reorgs>>
    97	
    98	Next == Tick \/ Anchor \/ Reorg \/ Ship \/ Reissue \/ Refuse
    99	
   100	(***************************************************************************)
   101	(* Invariants — copied verbatim from the main module; only their          *)
   102	(* verdicts differ.                                                        *)
   103	(***************************************************************************)
   104	
   105	NoShippedOrphan == ~shippedOrphaned
   106	
   107	ShippedIsSound ==
   108	  shipped =>
   109	    /\ anchorAt # NoAnchor
   110	    /\ anchorAt >= declared
   111	    /\ anchorAt <= declared + Delta
   112	    /\ depth >= DepthK
   113	
   114	ExpiredCannotShip ==
   115	  (~shipped /\ now > declared + Delta) => ~ENABLED Ship
   116	
   117	NoSilentDeadlock ==
   118	  (~shipped /\ attempts = MaxAttempts /\ now > declared + Delta) => refused
   119	
   120	RefusedOnlyWhenExhausted ==
   121	  refused => /\ ~shipped
   122	             /\ attempts = MaxAttempts
   123	             /\ now > declared + Delta
   124	
   125	RefusalLatched == [][refused => refused']_vars
   126	
   127	================================================================================

===== FILE: P5c_IssuanceProtocol_Broken.tla =====
     1	---------------------- MODULE P5c_IssuanceProtocol_Broken ----------------------
     2	(***************************************************************************)
     3	(* Tessera Band 0 — P5 issuance corollary, DELIBERATELY BROKEN: shipping  *)
     4	(* on a shallow anchor. Ship requires only inclusion (depth >= 1), not    *)
     5	(* burial at depth k — "it's in a block, ship it." This is the exact bug  *)
     6	(* Gemini's review named: a transient reorganization then orphans the     *)
     7	(* block under an already-shipped receipt, leaving it permanently          *)
     8	(* unverifiable.                                                            *)
     9	(*                                                                          *)
    10	(* Expected result: TLC VIOLATES NoShippedOrphan, with the trace          *)
    11	(* declare -> anchor -> one confirmation -> ship -> reorg. A green run    *)
    12	(* would mean the depth-k rule buys nothing in this model.                  *)
    13	(* Identical state space and actions except Ship's depth precondition —   *)
    14	(* including the 2026-07-20 refusal machinery (atomic entry in Tick),     *)
    15	(* carried verbatim so that claim stays literally true.                    *)
    16	(***************************************************************************)
    17	EXTENDS Integers
    18	
    19	CONSTANTS MaxTime, Delta, DepthK, MaxAttempts
    20	
    21	ASSUME Delta \in Nat /\ DepthK \in Nat \ {0} /\ MaxTime \in Nat
    22	       /\ MaxAttempts \in Nat \ {0}
    23	
    24	NoAnchor == -1
    25	
    26	VARIABLES now, declared, anchorAt, depth, shipped, shippedOrphaned,
    27	          attempts, reorgs, refused
    28	
    29	vars == <<now, declared, anchorAt, depth, shipped, shippedOrphaned,
    30	          attempts, reorgs, refused>>
    31	
    32	Init ==
    33	  /\ now = 0 /\ declared = 0
    34	  /\ anchorAt = NoAnchor /\ depth = 0
    35	  /\ shipped = FALSE /\ shippedOrphaned = FALSE
    36	  /\ attempts = 1 /\ reorgs = 0
    37	  /\ refused = FALSE
    38	
    39	Tick ==
    40	  /\ now < MaxTime
    41	  /\ now' = now + 1
    42	  /\ depth' = IF anchorAt # NoAnchor /\ depth < DepthK THEN depth + 1 ELSE depth
    43	  /\ refused' = (refused \/ (~shipped /\ attempts = MaxAttempts
    44	                                      /\ now + 1 > declared + Delta))
    45	  /\ UNCHANGED <<declared, anchorAt, shipped, shippedOrphaned, attempts, reorgs>>
    46	
    47	Anchor ==
    48	  /\ ~shipped /\ anchorAt = NoAnchor
    49	  /\ anchorAt' = now /\ depth' = 0
    50	  /\ UNCHANGED <<now, declared, shipped, shippedOrphaned, attempts, reorgs,
    51	                 refused>>
    52	
    53	Reorg ==
    54	  /\ anchorAt # NoAnchor /\ depth < DepthK
    55	  /\ reorgs < 2
    56	  /\ anchorAt' = NoAnchor /\ depth' = 0 /\ reorgs' = reorgs + 1
    57	  /\ shippedOrphaned' = (shipped \/ shippedOrphaned)
    58	  /\ UNCHANGED <<now, declared, shipped, attempts, refused>>
    59	
    60	(* BROKEN: ships on mere inclusion — depth >= 1, not DepthK.               *)
    61	Ship ==
    62	  /\ ~shipped /\ anchorAt # NoAnchor
    63	  /\ depth >= 1
    64	  /\ now <= declared + Delta
    65	  /\ shipped' = TRUE
    66	  /\ UNCHANGED <<now, declared, anchorAt, depth, shippedOrphaned, attempts,
    67	                 reorgs, refused>>
    68	
    69	Reissue ==
    70	  /\ ~shipped /\ now > declared + Delta
    71	  /\ attempts < MaxAttempts
    72	  /\ declared' = now /\ anchorAt' = NoAnchor /\ depth' = 0
    73	  /\ attempts' = attempts + 1
    74	  /\ UNCHANGED <<now, shipped, shippedOrphaned, reorgs, refused>>
    75	
    76	Next == Tick \/ Anchor \/ Reorg \/ Ship \/ Reissue
    77	
    78	(* Same harm invariant as the correct module. EXPECTED: VIOLATED.          *)
    79	NoShippedOrphan == ~shippedOrphaned
    80	
    81	================================================================================

===== FILE: P5c_IssuanceProtocol.cfg =====
     1	\* MaxTime = 14 (raised from 8, 2026-07-20; 12 -> 14 same day on Codex
     2	\* finding 5): the refusal invariants need the FINAL attempt's window to
     3	\* be expirable within the bound — minimum MaxAttempts * (Delta + 1) = 12,
     4	\* below which refusal is unreachable and NoSilentDeadlock passes
     5	\* VACUOUSLY (the _Sanity RefusalUnreachable witness catches this). The
     6	\* + DepthK headroom (14) additionally exercises the post-refusal burial
     7	\* path — at 12 refusal lands exactly at the bound and no Tick can deepen
     8	\* an anchor afterwards (the RefusalBuriedAnchorUnreachable witness
     9	\* catches THAT).
    10	CONSTANTS
    11	  MaxTime = 14
    12	  Delta = 3
    13	  DepthK = 2
    14	  MaxAttempts = 3
    15	
    16	INIT Init
    17	NEXT Next
    18	
    19	INVARIANTS
    20	  NoShippedOrphan
    21	  ShippedIsSound
    22	  ExpiredCannotShip
    23	  NoSilentDeadlock
    24	  RefusedOnlyWhenExhausted
    25	
    26	\* "Durably recorded": the refusal record latches (action property).
    27	PROPERTIES
    28	  RefusalLatched

===== FILE: P5c_IssuanceProtocol.out =====
1:TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)
11:Starting... (2026-07-20 21:24:39)
13:Finished computing initial states: 1 distinct state generated at 2026-07-20 21:24:39.
14:Model checking completed. No error has been found.
16:  because two distinct states had the same fingerprint:
18:3606 states generated, 2190 distinct states found, 0 states left on queue.
21:Finished in 00s at (2026-07-20 21:24:39)
----- final 40 lines -----
     1	TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)
     2	Warning: Please run the Java VM which executes TLC with a throughput optimized garbage collector by passing the "-XX:+UseParallelGC" property.
     3	(Use the -nowarning option to disable this warning.)
     4	Running breadth-first search Model-Checking with fp 12 and seed 510523806675586915 with 1 worker on 128 cores with 30688MB heap and 64MB offheap memory [pid: 79680] (Linux 6.18.33.2-microsoft-standard-WSL2 amd64, Ubuntu 11.0.31 x86_64, MSBDiskFPSet, DiskStateQueue).
     5	Parsing file /home/tony/projects/tessera/formal/tla/P5c_IssuanceProtocol.tla
     6	Parsing file /tmp/Integers.tla
     7	Parsing file /tmp/Naturals.tla
     8	Semantic processing of module Naturals
     9	Semantic processing of module Integers
    10	Semantic processing of module P5c_IssuanceProtocol
    11	Starting... (2026-07-20 21:24:39)
    12	Computing initial states...
    13	Finished computing initial states: 1 distinct state generated at 2026-07-20 21:24:39.
    14	Model checking completed. No error has been found.
    15	  Estimates of the probability that TLC did not check all reachable states
    16	  because two distinct states had the same fingerprint:
    17	  calculated (optimistic):  val = 1.7E-13
    18	3606 states generated, 2190 distinct states found, 0 states left on queue.
    19	The depth of the complete state graph search is 23.
    20	The average outdegree of the complete state graph is 1 (minimum is 0, the maximum 3 and the 95th percentile is 2).
    21	Finished in 00s at (2026-07-20 21:24:39)

===== FILE: P5c_IssuanceProtocol.READ-AND-CHALLENGE.md =====
     1	# P5c — read-and-challenge annotation
     2	
     3	**Status: author-side, NON-DISCHARGING. Not a review.**
     4	
     5	This file is a *teaching artifact*, not a verification artifact. It was
     6	produced with AI assistance (Claude) against a model that was itself written
     7	with AI assistance. That is precisely the correlated-blind-spot configuration
     8	the project's non-author falsification gate (A1.7) exists to defeat. Nothing
     9	here discharges anything, upgrades any status in `PROPERTIES.md`, or counts as
    10	independent review. If a claim in here and the model ever disagree, that is a
    11	question to *investigate*, not a verdict.
    12	
    13	Its only purpose: to demonstrate the *shape* of the questions a skeptic asks
    14	of a formal model, on a model whose system you already understand — so the
    15	read-and-challenge muscle is yours, not borrowed. The questions are the
    16	product. The answers are yours to reach.
    17	
    18	A model can only ever be wrong in three places. Every question below is an
    19	instance of one of them:
    20	
    21	1. **The abstraction lies** — the model omits or simplifies something whose
    22	   omission is load-bearing for the property.
    23	2. **The property is too weak** — the invariant passes but doesn't actually
    24	   say what the English claim says.
    25	3. **The seam is unguarded** — the model proves its half, another artifact
    26	   proves the other half, and the join between them is asserted, not checked.
    27	
    28	Read each question and ask yourself: *which of the three is this, and do I
    29	believe the model's answer?*
    30	
    31	---
    32	
    33	## A. Does the abstraction lie? (the single-clock collapse)
    34	
    35	The module header is admirably explicit that block timestamps equal real time
    36	and blocks arrive one per tick. That honesty is exactly what makes the next
    37	question askable.
    38	
    39	**Q1. The consequence you were told, made concrete.** The header says the
    40	single-clock abstraction means "issuance-side anchors never precede
    41	declaration, so the epsilon side does not appear." Walk it yourself: `Anchor`
    42	sets `anchorAt' = now`, and `now` only ever increases from `declared`'s value.
    43	So `anchorAt >= declared` is true *by construction of the clock*, not because
    44	the protocol enforces it. **Ask:** in the real system, is there any path where
    45	a block timestamp is *earlier* than your declared issue time? (Bitcoin block
    46	timestamps are not monotonic and can legitimately move backward by up to ~2
    47	hours under the median-time-past rule.) If yes — is that path supposed to be
    48	caught here, or is it explicitly handed to epsilon on the verifier side? Find
    49	the sentence in A1.6 that catches it. If you can't find it, you've found a
    50	seam (§C), not a bug — but you need to *know* it's handed off, not assume it.
    51	
    52	**Q2. One tick, one block, one confirmation.** `Tick` both advances the clock
    53	*and* deepens the anchor by exactly one. So in this model, time and
    54	confirmation-depth are the same quantity. **Ask:** in reality, can time pass
    55	*without* a confirmation arriving (a slow block, a mining lull)? If it can,
    56	then real `now <= declared + Delta` and real `depth >= k` are two independent
    57	race conditions, and this model has fused them into one. Does that fusion
    58	*help* the attacker or the defender? Work out which — a fused model that
    59	happens to be conservative is fine; a fused model that hides an adversarial
    60	interleaving is not. Convince yourself which one this is. (Hint: ask what the
    61	`Ship` guard would have to check if `Tick` could advance `now` while leaving
    62	`depth` unchanged.)
    63	
    64	---
    65	
    66	## B. Is the property too weak? (what the invariants actually say)
    67	
    68	**Q3. `NoShippedOrphan` and the reorg bound.** `Reorg` has the guard
    69	`reorgs < 2` and the header calls this a "reachability witness" bound. But
    70	look at what it does to the *harm* claim: the invariant `NoShippedOrphan` only
    71	gets to fail if a reorg can *reach* a shipped-but-shallow receipt. **Ask:** is
    72	`NoShippedOrphan` holding because the *depth-k rule* genuinely prevents the
    73	harm, or partly because `reorgs < 2` caps the adversary before it can dig
    74	deep? These are different reasons. The broken companion is the control that
    75	answers this — it holds `reorgs < 2` fixed and *only* weakens `Ship` to
    76	`depth >= 1`, and the harm becomes reachable. So the difference *is* isolated
    77	to the ship rule. Good. **But now ask the follow-up:** does `reorgs < 2` bound
    78	the *depth* a reorg can reach, or only the *number* of reorgs? Re-read
    79	`Reorg`: it only fires when `depth < DepthK`. So a reorg can never orphan a
    80	depth-k anchor *by construction of the guard*, not by the number 2. Is that
    81	guard the A1.6 assumption ("depth >= k is permanent") wearing a disguise? If
    82	so, `NoShippedOrphan` is partly *assuming* what it looks like it's proving.
    83	That's not necessarily wrong — the header says depth-k permanence is a
    84	precondition, not a result — but you should be able to say out loud: **"the
    85	model proves the ship rule respects the permanence assumption; it does not
    86	prove the permanence assumption."** Can you?
    87	
    88	**Q4. `ShippedIsSound` — is the conjunction complete?** It asserts
    89	`anchorAt >= declared`, `anchorAt <= declared + Delta`, `depth >= DepthK`.
    90	**Ask:** the English claim is "temporally sound and buried." Is "buried within
    91	delta of *the declared time*" the same as "buried within delta of *when a
    92	verifier will later evaluate it*"? The A2 resolution made issuer and verifier
    93	share *one* predicate on chain-time. Does this invariant reference that shared
    94	predicate, or a proxy for it that happens to coincide under the single clock?
    95	(This is the same fusion as Q2, viewed from the invariant instead of the
    96	action. If Q2's fusion is safe, this is too — but check them *separately*,
    97	because a proxy that coincides in the model can diverge in the code.)
    98	
    99	**Q5. `ExpiredCannotShip` uses `ENABLED Ship`.** This is a clever, honest way
   100	to state "no expired attempt can ship." **Ask:** `ENABLED Ship` is evaluated
   101	against *this module's* `Ship`. If you later change `Ship` (as the broken
   102	companion does), this invariant's *meaning* changes with it silently. Is that
   103	what you want? (It is defensible — the invariant is "whatever shipping means,
   104	an expired attempt can't do it." But notice you've coupled a safety property
   105	to an action definition. In the broken companion, is `ExpiredCannotShip` even
   106	checked? Look at its cfg. If not — why is it safe to drop, and did you decide
   107	that on purpose?)
   108	
   109	---
   110	
   111	## C. Is the seam unguarded? (where P5c hands off)
   112	
   113	This is the highest-value section for the integrity headline (P1), because
   114	P1's soundness lives in the *joins* between models, not inside any one.
   115	
   116	**Q6. The verifier-permanence handoff.** The header's whole reason for
   117	existing: "it discharges the obligation the verifier-side model's scope
   118	boundary names: that the verifier may take `anchor` as an already-permanent
   119	block time." So P5P6 (verifier) *assumes* permanence; P5c (issuer) is supposed
   120	to *earn* it. **Ask the seam question:** does P5c earn *exactly* the thing
   121	P5P6 assumes — same predicate, same depth convention, same delta? The A2.1
   122	convention pin (`DepthK = k - 1`, block-after-inclusion vs Bitcoin's
   123	count-the-including-block) is *precisely* the kind of off-by-one that lives in
   124	a seam. Open `P5P6_TemporalRevocation.tla`, find its `confirmedAt`, and check
   125	by hand that the two modules mean the identical block by "confirmed at depth
   126	k." If they're off by one in *opposite* directions, both models pass and the
   127	composed system is wrong. **This is the check no single model can perform on
   128	itself.** It is the strongest argument for outsourced review (option 3) — not
   129	because the models are hard, but because the *seam* is invisible to each side.
   130	
   131	**Q7. Liveness is explicitly not checked.** The header is honest: "eventually
   132	ships" is not verified; termination is "by construction (A2.3)" via
   133	`MaxAttempts`. **Ask:** "by construction" is a proof obligation, not a proof.
   134	Is there anywhere — prose, another model — that actually argues N attempts
   135	terminate in a *reported* refusal rather than a silent stall? The
   136	`PROPERTIES.md` tracker still has "A2.2 conformance-vector cases" unchecked.
   137	Is the refusal-is-reported claim discharged anywhere, or is it currently a
   138	promise? (A silent stall on attempt N is exactly the fail-*open* the whole
   139	project is against. Worth knowing if it's proven or asserted.)
   140	
   141	---
   142	
   143	## THE HEADLINE WEAKNESS (sharpened from Q6, after reading P5P6)
   144	
   145	Not a general "check the seam" — a specific undischarged correspondence.
   146	Still author-side, still non-discharging. Go falsify it; don't trust it.
   147	
   148	The two temporal modules agree on the confirmation-time *formula* in prose —
   149	both cite A2.1's `confirmedAt := timestamp(block h+k-1)`. Good: the off-by-one
   150	convention is at least *named* on both sides, not silently divergent. But they
   151	model the underlying quantity **incompatibly**, and nothing checks that the
   152	prose agreement survives the modeling gap:
   153	
   154	- **P5c models depth operationally.** `depth` is a state variable; `Tick`
   155	  increments it; `Ship` guards on `depth >= DepthK` with `DepthK = k-1`. The
   156	  `h+k-1` burial is *enacted*.
   157	- **P5P6 does not model depth at all.** There is no `depth` variable. It has
   158	  `confirmedAt \in 0..MaxTime` — a *free integer* — constrained only by
   159	  `confirmedAt <= declared + polDelta`. The `h+k-1` provenance is a comment
   160	  (line 37) and is then discarded; the verifier treats `confirmedAt` as an
   161	  arbitrary number it is handed.
   162	
   163	**The unguarded seam:** P5c's *output* is a shipped receipt anchored at a
   164	specific block; P5P6's *input* is a bare `confirmedAt` integer. The join —
   165	"the `confirmedAt` the verifier reads is the timestamp of the very block P5c
   166	shipped on" — is **modeled nowhere.** It lives entirely in the shared comment.
   167	A bug (or adversary) that made P5c ship on the wrong block would emit a
   168	`confirmedAt` P5P6 still accepts, because P5P6 cannot see *which* block it is —
   169	only that the number is `<= declared + polDelta`.
   170	
   171	This is the tracker's `Cross-model correspondence mapping` line — except the
   172	correspondence that bites first is **TLA+ ↔ TLA+**, between your own two
   173	temporal modules, and it is *not* itemized on the tracker as distinct from the
   174	TLA+↔symbolic mapping. That is the gap.
   175	
   176	**Work-through exercise (this is the training aid):**
   177	
   178	1. Take a P5c terminal state: `shipped = TRUE`, with `declared`, `anchorAt`,
   179	   `depth = DepthK`. Ask: what value of `confirmedAt` does P5P6 receive for
   180	   this receipt? P5c never computes a "timestamp of the h+k-1 block" as a
   181	   quantity distinct from `anchorAt` — under its single clock, block-time *is*
   182	   the tick. So the mapping forces the Q2 clock-fusion back into the open,
   183	   now from the seam side.
   184	2. Decide: does P5P6's `confirmedAt` correspond to P5c's `anchorAt`, or to
   185	   `anchorAt + (k-1)`? Under the single clock they may coincide; in reality
   186	   the k-1 burial ticks are real elapsed time. If P5P6 is implicitly treating
   187	   `anchorAt` and `confirmedAt` as the same instant, **the entire h+k-1 burial
   188	   delay has disappeared in the handoff** — the verifier would accept a receipt
   189	   whose k-th confirmation actually landed *outside* the window.
   190	
   191	If that last line is true, it is a real hole, found before Band-0 exit — the
   192	method working. If it is false, you will have discharged a correspondence
   193	obligation *by hand* and earned the read. Either way the next move is a signed
   194	amendment (A1.1) — either adding the TLA+↔TLA+ correspondence obligation to the
   195	tracker, or recording that you checked it and it holds. Do not edit the models
   196	in place to "fix" it before deciding which.
   197	
   198	I could not settle this myself, and you should not let me — a cross-model
   199	correspondence blessed by the same AI that helped write the models is the
   200	correlated-blind-spot case A1.7 exists for. This is the sharpest argument in
   201	the whole file for outsourced human review (option 3): the seam is invisible
   202	to each model *and* to the assistant that wrote both.
   203	
   204	---
   205	
   206	## How to use this
   207	
   208	Pick **one** question — Q6 is the one I'd start with, it has the most teeth
   209	and it's a hand-check, not a tool run. Answer it *without* trusting me: open
   210	both modules, trace the block index, and decide for yourself whether the seam
   211	holds. If you can do that and defend the answer cold, you have the
   212	read-and-challenge skill for this model. Then the questions I *didn't* think to
   213	ask are the ones that matter next — and those are yours to find.
   214	
   215	If any of these turns out to point at a real gap, the fix is a signed amendment
   216	(A1.1), not an edit to the model in place — and the *discovery* is the method
   217	working, not a failure.
   218	
   219	---
   220	
   221	## Postscript (2026-07-19, appended before archiving)
   222	
   223	The HEADLINE section above went through the non-author gate in the
   224	2026-07-18/19 session: Codex checked the alarming form — "the burial delay
   225	disappears in the handoff" — and it does **not** reproduce (384-state check,
   226	invariant holds; the initial framing was wrong and the falsification gate
   227	killed it). What survives is narrower: an undischarged **TLA+↔TLA+
   228	correspondence obligation**, now itemized in `formal/PROPERTIES.md` and
   229	destined for Amendment 3 disposition per the break-the-chain decision. See
   230	`docs/exploration-2026-07-18-causal-dag-commons.md` (§0 finding 1, §8, §8b).
   231	
   232	The questions remain a teaching artifact; the headline should no longer be
   233	read as a live alarm. Original text above is unedited, per the
   234	record-preservation rule.
   235	
   236	## Postscript 2 (2026-07-20, appended after the refusal-state bench work)
   237	
   238	Q7's question — "is the refusal-is-reported claim discharged anywhere, or
   239	is it currently a promise?" — now has a precise partial answer. The model
   240	carries a `refused` state entered by **atomic entry** (the Tick expiring
   241	the final window records it in the same transition; round-3 ruling 4),
   242	with `NoSilentDeadlock`, `RefusedOnlyWhenExhausted`, and the
   243	`RefusalLatched` latch checked, and a `_BrokenSilent` companion
   244	(separately enabled, postponable Refuse) red on exactly the deadlock
   245	invariant among the checked set. What is discharged (wording narrowed
   246	2026-07-20 by the Codex review of this work, which withdrew its own
   247	earlier "durably recorded and available for retrieval" as too strong):
   248	**the abstract refusal state is entered atomically and latches**.
   249	Storage durability, retrievability, and reporting all remain promises —
   250	the record→report gap is an Amendment 3 disposition item (A2.3's draft
   251	text was aligned to this split on 2026-07-21). Q7's "silent stall on attempt N" is now unrepresentable *as a
   252	state*: no reachable state has the final window expired without the
   253	refusal recorded. It is not excluded *as a behavior* — without fairness,
   254	Tick can be postponed indefinitely before the crossing, and a mid-loop
   255	stall (Reissue postponed forever, attempts unexhausted) is likewise
   256	representable; both are the explicitly-unclaimed liveness, named in the
   257	module header. This work has passed one non-author falsification pass
   258	(`docs/reviews/2026-07-20-codex-p5c-refusal-review.md`); discharge
   259	status is the tracker's to say, not this file's.

===== FILE: P5c_IssuanceProtocol_Sanity.cfg =====
     1	\* Vacuity check: run with `tlc2.TLC -continue`, piping through
     2	\* `scripts/filter-tlc-output.sh` before committing the .out — the
     3	\* committed artifact keeps the first violation trace per witness and
     4	\* drops the repetitions (at MaxTime = 14 the raw dump is ~100k lines;
     5	\* record-norms ruling 2026-07-21). TLC VIOLATING all seven
     6	\* invariants is the healthy result — shipping is reachable at all, after
     7	\* a re-issue, and after surviving a reorg; refusal is reachable at all,
     8	\* after a reorg, with a live (late, worthless) anchor present, and with
     9	\* that anchor buried to full depth post-refusal — so the main cfg's
    10	\* invariants are not vacuously true. If RefusalUnreachable survives,
    11	\* MaxTime is too small for the final window to expire (need
    12	\* MaxTime >= MaxAttempts * (Delta + 1)); if
    13	\* RefusalBuriedAnchorUnreachable survives, the post-refusal burial path
    14	\* is untested (need the + DepthK headroom = 14).
    15	\*
    16	\* ORDER MATTERS: TLC reports only the FIRST failing invariant per state.
    17	\* Shipped states and refused states are disjoint, so the two families
    18	\* cannot mask each other — but within each family the broad witness
    19	\* (ShipUnreachable / RefusalUnreachable) fails in every shipped/refused
    20	\* state and is listed last so it cannot mask the specific ones.
    21	\* RefusalBuriedAnchor states are a subset of RefusalWithLiveAnchor
    22	\* states, so the buried witness is listed before the live-anchor one.
    23	CONSTANTS
    24	  MaxTime = 14
    25	  Delta = 3
    26	  DepthK = 2
    27	  MaxAttempts = 3
    28	
    29	INIT Init
    30	NEXT Next
    31	
    32	INVARIANTS
    33	  ReorgShipUnreachable
    34	  ReissueShipUnreachable
    35	  ShipUnreachable
    36	  RefusalAfterReorgUnreachable
    37	  RefusalBuriedAnchorUnreachable
    38	  RefusalWithLiveAnchorUnreachable
    39	  RefusalUnreachable

===== FILE: P5c_IssuanceProtocol_Sanity.out =====
1:TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)
11:Starting... (2026-07-21 06:10:25)
13:Finished computing initial states: 1 distinct state generated at 2026-07-21 06:10:25.
14:Error: Invariant ShipUnreachable is violated.
15:Error: The behavior up to this point is:
71:Error: Invariant ReorgShipUnreachable is violated.
72:Error: The behavior up to this point is:
150:Error: Invariant ReissueShipUnreachable is violated.
151:Error: The behavior up to this point is:
262:Error: Invariant RefusalUnreachable is violated.
263:Error: The behavior up to this point is:
429:Error: Invariant RefusalWithLiveAnchorUnreachable is violated.
430:Error: The behavior up to this point is:
607:Error: Invariant RefusalBuriedAnchorUnreachable is violated.
608:Error: The behavior up to this point is:
785:Error: Invariant RefusalAfterReorgUnreachable is violated.
786:Error: The behavior up to this point is:
974:### filter-tlc-output.sh: 506 further violation report(s) of already-witnessed invariants omitted; full output reproduces from the .cfg ###
975:3606 states generated, 2190 distinct states found, 0 states left on queue.
978:Finished in 01s at (2026-07-21 06:10:26)
----- final 40 lines -----
     1	/\ shipped = FALSE
     2	
     3	State 15: <Tick line 137, col 3 to line 142, col 81 of module P5c_IssuanceProtocol>
     4	/\ now = 10
     5	/\ depth = 0
     6	/\ reorgs = 1
     7	/\ declared = 8
     8	/\ refused = FALSE
     9	/\ anchorAt = -1
    10	/\ shippedOrphaned = FALSE
    11	/\ attempts = 3
    12	/\ shipped = FALSE
    13	
    14	State 16: <Tick line 137, col 3 to line 142, col 81 of module P5c_IssuanceProtocol>
    15	/\ now = 11
    16	/\ depth = 0
    17	/\ reorgs = 1
    18	/\ declared = 8
    19	/\ refused = FALSE
    20	/\ anchorAt = -1
    21	/\ shippedOrphaned = FALSE
    22	/\ attempts = 3
    23	/\ shipped = FALSE
    24	
    25	State 17: <Tick line 137, col 3 to line 142, col 81 of module P5c_IssuanceProtocol>
    26	/\ now = 12
    27	/\ depth = 0
    28	/\ reorgs = 1
    29	/\ declared = 8
    30	/\ refused = TRUE
    31	/\ anchorAt = -1
    32	/\ shippedOrphaned = FALSE
    33	/\ attempts = 3
    34	/\ shipped = FALSE
    35	
    36	### filter-tlc-output.sh: 506 further violation report(s) of already-witnessed invariants omitted; full output reproduces from the .cfg ###
    37	3606 states generated, 2190 distinct states found, 0 states left on queue.
    38	The depth of the complete state graph search is 23.
    39	The average outdegree of the complete state graph is 1 (minimum is 0, the maximum 3 and the 95th percentile is 2).
    40	Finished in 01s at (2026-07-21 06:10:26)

===== FILE: P5c_IssuanceProtocol.tla =====
     1	------------------------- MODULE P5c_IssuanceProtocol -------------------------
     2	(***************************************************************************)
     3	(* Tessera Band 0 — P5's issuance-protocol corollary: "issuance is not    *)
     4	(* complete until the anchor is confirmed — buried at a minimum           *)
     5	(* confirmation depth k — within delta of declared_issue_time. If         *)
     6	(* confirmation is delayed past delta for benign reasons (calendar        *)
     7	(* outage, fee spikes, reorg), the receipt is re-issued with a fresh      *)
     8	(* declared time and re-anchored — the failed attempt is discarded, not   *)
     9	(* shipped." (Amendment 1 §A1.2 P5 corollary, §A1.6.)                     *)
    10	(*                                                                          *)
    11	(* Unlike the stateless enumerations (P4, P5/P6 verifier-side), this IS a *)
    12	(* state machine: time advances, anchors land, blocks deepen, reorgs      *)
    13	(* orphan shallow blocks, the issuer ships or re-issues. It discharges    *)
    14	(* the obligation the verifier-side model's scope boundary names: that    *)
    15	(* the verifier may take `anchor` as an already-permanent block time.     *)
    16	(*                                                                          *)
    17	(* SEMANTIC FORK, RESOLVED (Amendment 2, ratified 2026-07-07): the        *)
    18	(* registered "confirmed ... within delta" is ratified in its STRICT      *)
    19	(* reading, defined on the chain-visible observable (A2.1):               *)
    20	(*   confirmed_at := timestamp(block h+k-1)  <=  declared + delta         *)
    21	(* evaluated IDENTICALLY by the issuer at Ship and by the verifier (the   *)
    22	(* A2.2 third conjunct; see P5P6_TemporalRevocation's confirmedAt).       *)
    23	(* Under this module's single-clock abstraction (block timestamps equal   *)
    24	(* real time, blocks arrive one per tick) Ship's "now <= declared +       *)
    25	(* Delta" at depth k IS the chain-time predicate, so the action needed    *)
    26	(* no change. Convention pin (A2.1): this module's depth counts blocks    *)
    27	(* AFTER inclusion (depth 0 = just included); Bitcoin convention counts   *)
    28	(* the including block as the first confirmation; hence DepthK = k - 1    *)
    29	(* (strict default k = 6 => DepthK = 5). MaxAttempts is protocol          *)
    30	(* semantics per A2.3 — N attempts, then explicit fail-closed refusal     *)
    31	(* (N ratified at Band 0 exit, working default 3) — no longer a mere      *)
    32	(* state-space bound; see the abstractions note below.                     *)
    33	(*                                                                          *)
    34	(* CLOCK-ROLES RULING (2026-07-21, resolves the round-2 A2 blocker):      *)
    35	(* chain time governs evidence; wall time governs the attempt lifecycle   *)
    36	(* and refusal. Under the ruling this module's single clock READS AS THE  *)
    37	(* WALL CLOCK: its expiry `now > declared + Delta` is the S = 0 instance  *)
    38	(* of the ruled lifecycle envelope `declared + Delta + S`; the slack      *)
    39	(* analysis lives in P5cP5P6_BridgeSlack{,_Latch}.tla, and eligibility    *)
    40	(* latching (a timely-eligible attempt cannot be expired by scheduling    *)
    41	(* delay) is a construction obligation registered with the ruling, not    *)
    42	(* modeled here. The coincidence noted above — Ship's fused guard IS the  *)
    43	(* chain predicate — is a property of the single-clock abstraction only;  *)
    44	(* decoupled, the seams are checked in the bridge and its companions.     *)
    45	(* Ruling archive: docs/reviews/2026-07-21-clock-precedence-ruling.md.     *)
    46	(*                                                                          *)
    47	(* REFUSAL STATE (2026-07-20, round-3 ruling 4, AUTHOR-ADOPTED FOR        *)
    48	(* STAGE-ONE DRAFTING): the refusal is modeled by ATOMIC ENTRY — the      *)
    49	(* Tick that expires the FINAL attempt's window records `refused` in the  *)
    50	(* same transition. Reaching refusal is thereby a transition-level        *)
    51	(* SAFETY fact; no separately enabled Refuse action, no fairness          *)
    52	(* assumption, no liveness claim. The discharged claim (narrowed          *)
    53	(* 2026-07-20 on Codex review of this work, which withdrew its own        *)
    54	(* round-3 phrase "durably recorded and available for retrieval" as too   *)
    55	(* strong): the ABSTRACT REFUSAL STATE IS ENTERED ATOMICALLY AND          *)
    56	(* LATCHES. A latched Boolean proves in-model persistence — not storage   *)
    57	(* durability, not retrievability, not reporting. Those three are         *)
    58	(* implementation/handoff obligations routed to Amendment 3, not          *)
    59	(* silently absorbed here — and A2.3's draft text now carries the same    *)
    60	(* split itself (aligned 2026-07-21; its earlier "reported" wording was   *)
    61	(* narrowed on review).                                                    *)
    62	(* Honest residuals, named: (a) Reissue is postponable, so a run can      *)
    63	(* stall mid-loop with attempts unexhausted and no refusal; (b) Tick      *)
    64	(* itself is postponable, so even the final crossing is not guaranteed    *)
    65	(* to occur — atomic entry proves that IF the crossing Tick occurs, its   *)
    66	(* post-state contains the refusal, never that it occurs. Both are the    *)
    67	(* explicitly-unclaimed liveness ("eventual issuance remains unclaimed";  *)
    68	(* round-3 clean rationale: a bounded, explicit negative result is        *)
    69	(* preferable to silent deadlock). What IS claimed: no reachable state    *)
    70	(* has the final window expired without the refusal recorded              *)
    71	(* (NoSilentDeadlock), the record is entered only on genuine exhaustion   *)
    72	(* (RefusedOnlyWhenExhausted), and it latches (RefusalLatched, an         *)
    73	(* action property). Companion P5c_IssuanceProtocol_BrokenSilent          *)
    74	(* implements the review's warned construction (separately enabled       *)
    75	(* Refuse) and must go red on exactly NoSilentDeadlock among the          *)
    76	(* checked set.                                                            *)
    77	(*                                                                          *)
    78	(* Abstractions, named:                                                     *)
    79	(* - Single clock: block timestamps equal real time here. Bitcoin         *)
    80	(*   timestamp skew is verifier-side, absorbed into epsilon (A1.6), out   *)
    81	(*   of scope. Consequence: issuance-side anchors never precede           *)
    82	(*   declaration in this model, so the epsilon side does not appear.      *)
    83	(* - Reorgs never exceed depth k: the A1.6 Layer 2 assumption ("anchors   *)
    84	(*   at depth >= k are treated as permanent") is a PRECONDITION of the    *)
    85	(*   Reorg action, not something proven. The broken companion shows what  *)
    86	(*   the depth-k ship rule buys GIVEN that assumption.                     *)
    87	(* - MaxTime bounds the state space. MaxAttempts, post-A2.3, is protocol  *)
    88	(*   semantics: exhausting it means issuance terminates in explicit       *)
    89	(*   refusal (a first-class outcome, durably recorded — see the refusal   *)
    90	(*   note above for what "recorded" does and does not claim), not an      *)
    91	(*   artifact of the bounded model. The unbounded "eventually ships"      *)
    92	(*   liveness claim is NOT checked (bounded model), and the safety        *)
    93	(*   claims are what this module discharges. MaxTime must be at least     *)
    94	(*   MaxAttempts * (Delta + 1) or the final window cannot expire and      *)
    95	(*   every refusal invariant passes VACUOUSLY — the _Sanity witnesses     *)
    96	(*   exist to catch exactly that misconfiguration. The committed cfgs     *)
    97	(*   use MaxAttempts * (Delta + 1) + DepthK = 14: the extra DepthK        *)
    98	(*   ticks exercise the post-refusal burial path (anchor lands after or   *)
    99	(*   at the refusal, deepens to full depth, Ship stays disabled) —        *)
   100	(*   without them that path is claimed but unreachable (Codex finding 5,  *)
   101	(*   2026-07-20).                                                          *)
   102	(*                                                                          *)
   103	(* Reading guide (Tony): this module has real actions. Tick advances      *)
   104	(* time and deepens an included anchor by one block per tick (block       *)
   105	(* arrival = clock tick, a deliberate simplification). Anchor lands the   *)
   106	(* stamp in the chain (depth 0 = just included; k more ticks to bury).    *)
   107	(* Reorg orphans any anchor shallower than k. Ship completes issuance    *)
   108	(* under the strict rule. Reissue discards a timed-out attempt and        *)
   109	(* redeclares at the current time.                                          *)
   110	(***************************************************************************)
   111	EXTENDS Integers
   112	
   113	CONSTANTS MaxTime, Delta, DepthK, MaxAttempts
   114	
   115	ASSUME Delta \in Nat /\ DepthK \in Nat \ {0} /\ MaxTime \in Nat
   116	       /\ MaxAttempts \in Nat \ {0}
   117	
   118	NoAnchor == -1
   119	
   120	VARIABLES
   121	  now,             \* the clock
   122	  declared,        \* declared_issue_time of the CURRENT attempt
   123	  anchorAt,        \* block time of the current anchor (NoAnchor if none)
   124	  depth,           \* confirmations of that anchor (capped at DepthK)
   125	  shipped,         \* issuance completed
   126	  shippedOrphaned, \* a SHIPPED receipt's anchor was orphaned (must stay FALSE)
   127	  attempts,        \* issuance attempts so far
   128	  reorgs,          \* reorg count (capped; for reachability witnesses)
   129	  refused          \* the durable refusal record (A2.3 / round-3 ruling 4)
   130	
   131	vars == <<now, declared, anchorAt, depth, shipped, shippedOrphaned,
   132	          attempts, reorgs, refused>>
   133	
   134	Init ==
   135	  /\ now = 0 /\ declared = 0
   136	  /\ anchorAt = NoAnchor /\ depth = 0
   137	  /\ shipped = FALSE /\ shippedOrphaned = FALSE
   138	  /\ attempts = 1 /\ reorgs = 0
   139	  /\ refused = FALSE
   140	
   141	(* Time advances; an included, unorphaned anchor gains one confirmation   *)
   142	(* per tick (depth capped at DepthK — beyond k, nothing changes).          *)
   143	(*                                                                          *)
   144	(* ATOMIC ENTRY (round-3 ruling 4, construction 1): the tick that carries *)
   145	(* the clock past the FINAL attempt's window records the refusal in the   *)
   146	(* SAME transition. There is no separately enabled Refuse action to       *)
   147	(* postpone — the state in which the last window has expired but no       *)
   148	(* refusal is recorded does not exist. The disjunct also keeps `refused`  *)
   149	(* latched (belt; no action ever unsets it — RefusalLatched is the        *)
   150	(* checked form of that claim).                                            *)
   151	Tick ==
   152	  /\ now < MaxTime
   153	  /\ now' = now + 1
   154	  /\ depth' = IF anchorAt # NoAnchor /\ depth < DepthK THEN depth + 1 ELSE depth
   155	  /\ refused' = (refused \/ (~shipped /\ attempts = MaxAttempts
   156	                                      /\ now + 1 > declared + Delta))
   157	  /\ UNCHANGED <<declared, anchorAt, shipped, shippedOrphaned, attempts, reorgs>>
   158	
   159	(* The OTS calendar lands the stamp in a block — at any time (delays are  *)
   160	(* modeled by this action simply not firing yet). Deliberately NOT        *)
   161	(* guarded on ~refused: a discarded attempt's stamp landing after the     *)
   162	(* refusal is exactly the A2.4 case "a discarded attempt's transaction    *)
   163	(* confirming later confers nothing" — the model keeps that path          *)
   164	(* reachable, and the Ship guard, not this one, is what makes the late    *)
   165	(* anchor worthless. Witness coverage, stated precisely (Codex finding    *)
   166	(* 5): RefusalWithLiveAnchorUnreachable shows an anchor PRESENT in a      *)
   167	(* refused state; RefusalBuriedAnchorUnreachable shows it BURIED to full  *)
   168	(* depth post-refusal with Ship still disabled — the latter needs the     *)
   169	(* +DepthK headroom in MaxTime (14), and at 12 it is unreachable.          *)
   170	Anchor ==
   171	  /\ ~shipped /\ anchorAt = NoAnchor
   172	  /\ anchorAt' = now /\ depth' = 0
   173	  /\ UNCHANGED <<now, declared, shipped, shippedOrphaned, attempts, reorgs,
   174	                 refused>>
   175	
   176	(* A reorganization orphans any anchor shallower than DepthK. Depth >= k  *)
   177	(* is permanent BY ASSUMPTION (A1.6) — that is the Layer 2 line this      *)
   178	(* model builds on, not a result it proves. If a shipped receipt's anchor *)
   179	(* is orphaned, the harm flag latches (the correct Ship rule makes that   *)
   180	(* unreachable; the broken companion makes it reachable).                  *)
   181	Reorg ==
   182	  /\ anchorAt # NoAnchor /\ depth < DepthK
   183	  /\ reorgs < 2
   184	  /\ anchorAt' = NoAnchor /\ depth' = 0 /\ reorgs' = reorgs + 1
   185	  /\ shippedOrphaned' = (shipped \/ shippedOrphaned)
   186	  /\ UNCHANGED <<now, declared, shipped, attempts, refused>>
   187	
   188	(* Issuance completes — STRICT rule per the registered text: the anchor   *)
   189	(* is buried at depth k AND we are still within delta of the declared     *)
   190	(* time. (anchorAt <= now always, so the block time is in-window a        *)
   191	(* fortiori.)                                                               *)
   192	(*                                                                          *)
   193	(* BOUNDARY RACE, intentional (Codex finding 1): with integral time,      *)
   194	(* Ship's guard (now <= declared + Delta) and the refusal trigger         *)
   195	(* (now + 1 > declared + Delta, i.e. now >= declared + Delta) BOTH hold   *)
   196	(* at exactly now = declared + Delta — and there is no tick where         *)
   197	(* neither holds. At the deadline instant a fully-buried anchor may       *)
   198	(* ship, or the clock may advance and refuse; the scheduler's choice is   *)
   199	(* the model's honest image of the physical race between burial and       *)
   200	(* clock. Both branches are safe and the outcomes are mutually            *)
   201	(* exclusive (RefusedOnlyWhenExhausted). Eligibility at the boundary      *)
   202	(* does not oblige shipping — the deadline governs completion; a          *)
   203	(* "qualification guarantees issuance" contract would be a liveness       *)
   204	(* claim, and this module makes none.                                      *)
   205	Ship ==
   206	  /\ ~shipped /\ anchorAt # NoAnchor
   207	  /\ depth >= DepthK
   208	  /\ now <= declared + Delta
   209	  /\ shipped' = TRUE
   210	  /\ UNCHANGED <<now, declared, anchorAt, depth, shippedOrphaned, attempts,
   211	                 reorgs, refused>>
   212	
   213	(* The window expired without completion: discard the attempt, redeclare  *)
   214	(* fresh. The old attempt never ships — its declared time is gone.         *)
   215	Reissue ==
   216	  /\ ~shipped /\ now > declared + Delta
   217	  /\ attempts < MaxAttempts
   218	  /\ declared' = now /\ anchorAt' = NoAnchor /\ depth' = 0
   219	  /\ attempts' = attempts + 1
   220	  /\ UNCHANGED <<now, shipped, shippedOrphaned, reorgs, refused>>
   221	
   222	Next == Tick \/ Anchor \/ Reorg \/ Ship \/ Reissue
   223	
   224	(* Terminal states (shipped, or out of time/attempts) deadlock at the     *)
   225	(* MaxTime bound — run TLC with -deadlock (checking disabled); the        *)
   226	(* deadlocks are artifacts of the bounded model, not protocol defects.    *)
   227	
   228	(***************************************************************************)
   229	(* Invariants — what "the verifier may assume anchor is permanent" costs  *)
   230	(* and buys.                                                                *)
   231	(***************************************************************************)
   232	
   233	(* THE HARM INVARIANT (Gemini's finding, discharged): a shipped receipt's *)
   234	(* anchor is never orphaned — no receipt in the wild ever becomes         *)
   235	(* permanently unverifiable through reorg. Holds because Ship requires    *)
   236	(* depth >= k and Reorg touches only depth < k.                            *)
   237	NoShippedOrphan == ~shippedOrphaned
   238	
   239	(* A shipped receipt is temporally sound and buried: block time within    *)
   240	(* the window of ITS OWN declared time, at full depth. (Post-ship,        *)
   241	(* declared/anchorAt/depth are frozen: Reissue is disabled by shipped,    *)
   242	(* Anchor by anchorAt, Reorg by depth.)                                     *)
   243	ShippedIsSound ==
   244	  shipped =>
   245	    /\ anchorAt # NoAnchor
   246	    /\ anchorAt >= declared
   247	    /\ anchorAt <= declared + Delta
   248	    /\ depth >= DepthK
   249	
   250	(* Discarded attempts stay discarded: after a re-issue, the live declared *)
   251	(* time is the fresh one — there is no state in which an expired          *)
   252	(* declaration ships. (Equivalent state form: an unshipped attempt past   *)
   253	(* its window is exactly an attempt that cannot Ship.)                     *)
   254	ExpiredCannotShip ==
   255	  (~shipped /\ now > declared + Delta) => ~ENABLED Ship
   256	
   257	(* THE DEADLOCK INVARIANT (round-3 ruling 4): no silent terminal failure. *)
   258	(* If the final attempt's window has expired and nothing shipped, the     *)
   259	(* refusal record already exists — there is NO reachable state in which   *)
   260	(* issuance is dead but undocumented. This is the state-level shadow of   *)
   261	(* the atomic entry in Tick; the _BrokenSilent companion (separately      *)
   262	(* enabled Refuse) must violate exactly this invariant and nothing else.   *)
   263	NoSilentDeadlock ==
   264	  (~shipped /\ attempts = MaxAttempts /\ now > declared + Delta) => refused
   265	
   266	(* The negative outcome is sound: refusal is recorded ONLY on genuine     *)
   267	(* exhaustion — final attempt, window expired, nothing shipped. (The      *)
   268	(* conjuncts stay true once entered: Reissue is disabled by               *)
   269	(* attempts = MaxAttempts so declared is frozen, now is monotone, and     *)
   270	(* Ship is disabled forever by the expired window — so refused and        *)
   271	(* shipped are mutually exclusive as a corollary.)                         *)
   272	RefusedOnlyWhenExhausted ==
   273	  refused => /\ ~shipped
   274	             /\ attempts = MaxAttempts
   275	             /\ now > declared + Delta
   276	
   277	(* The in-model latch: every step either preserves refused or sets it;    *)
   278	(* no step unsets it. Action property (PROPERTIES in the cfg, not         *)
   279	(* INVARIANTS). This proves LOGICAL state persistence only — storage      *)
   280	(* durability, retrievability, and reporting are implementation/handoff   *)
   281	(* obligations (see the header's narrowed claim).                          *)
   282	RefusalLatched == [][refused => refused']_vars
   283	
   284	(* Vacuity witnesses — _Sanity cfg, TLC -continue; VIOLATIONS are the     *)
   285	(* healthy result: shipping is reachable at all, after a re-issue, and    *)
   286	(* after surviving a reorg; refusal is reachable at all, after a reorg,   *)
   287	(* with a live (late, worthless) anchor present — the A2.4                *)
   288	(* discarded-attempt case — and with that anchor BURIED to full depth     *)
   289	(* post-refusal while Ship stays disabled (the off-happy-path trace of    *)
   290	(* Codex finding 5). If RefusalUnreachable is NOT violated, the refusal   *)
   291	(* invariants above are vacuous — check MaxTime >=                        *)
   292	(* MaxAttempts * (Delta + 1); if RefusalBuriedAnchorUnreachable is NOT    *)
   293	(* violated, the post-refusal burial path is untested — check the         *)
   294	(* + DepthK headroom (14).                                                 *)
   295	ShipUnreachable        == ~shipped
   296	ReissueShipUnreachable == ~(shipped /\ attempts > 1)
   297	ReorgShipUnreachable   == ~(shipped /\ reorgs > 0)
   298	RefusalUnreachable               == ~refused
   299	RefusalAfterReorgUnreachable     == ~(refused /\ reorgs > 0)
   300	RefusalWithLiveAnchorUnreachable == ~(refused /\ anchorAt # NoAnchor)
   301	RefusalBuriedAnchorUnreachable   == ~(refused /\ depth >= DepthK)
   302	
   303	================================================================================
