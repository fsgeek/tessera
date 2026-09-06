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

===== FILE: A2.1-A2.2.txt =====
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

===== FILE: P5P6_TemporalRevocation_Broken.cfg =====
     1	CONSTANTS
     2	  MaxTime = 6
     3	  DeltaMax = 3
     4	  EpsilonMax = 1
     5	  RcptTolMax = 6
     6	
     7	INIT Init
     8	NEXT Next
     9	
    10	INVARIANTS
    11	  ForgeryRejected

===== FILE: P5P6_TemporalRevocation_BrokenConf.cfg =====
     1	\* Expected: ForgeryRejected and ReceiptIndependence HOLD (the
     2	\* abandoned-anchor artifact is not a forgery and touches no receipt
     3	\* tolerance); AbandonedArtifactRejected is VIOLATED — the counterexample
     4	\* is the A2.0 artifact itself. That asymmetry is this module's point:
     5	\* the pre-Amendment-2 invariant suite cannot see the gap.
     6	CONSTANTS
     7	  MaxTime = 6
     8	  DeltaMax = 3
     9	  EpsilonMax = 1
    10	  RcptTolMax = 6
    11	
    12	INIT Init
    13	NEXT Next
    14	
    15	INVARIANTS
    16	  ForgeryRejected
    17	  ReceiptIndependence
    18	  AbandonedArtifactRejected

===== FILE: P5P6_TemporalRevocation_BrokenConf.out =====
1:TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)
5:Parsing file /home/tony/projects/tessera/formal/tla/P5P6_TemporalRevocation_BrokenConf.tla
10:Semantic processing of module P5P6_TemporalRevocation_BrokenConf
11:Starting... (2026-07-07 10:22:31)
24:Error: Invariant AbandonedArtifactRejected is violated by the initial state:
35:Finished in 01s at (2026-07-07 10:22:32)
----- final 40 lines -----
     1	TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)
     2	Warning: Please run the Java VM which executes TLC with a throughput optimized garbage collector by passing the "-XX:+UseParallelGC" property.
     3	(Use the -nowarning option to disable this warning.)
     4	Running breadth-first search Model-Checking with fp 24 and seed -1194905896798107378 with 1 worker on 128 cores with 30688MB heap and 64MB offheap memory [pid: 2607666] (Linux 6.18.33.2-microsoft-standard-WSL2 amd64, Ubuntu 11.0.31 x86_64, MSBDiskFPSet, DiskStateQueue).
     5	Parsing file /home/tony/projects/tessera/formal/tla/P5P6_TemporalRevocation_BrokenConf.tla
     6	Parsing file /tmp/Integers.tla
     7	Parsing file /tmp/Naturals.tla
     8	Semantic processing of module Naturals
     9	Semantic processing of module Integers
    10	Semantic processing of module P5P6_TemporalRevocation_BrokenConf
    11	Starting... (2026-07-07 10:22:31)
    12	Computing initial states...
    13	Computed 2 initial states...
    14	Computed 4 initial states...
    15	Computed 8 initial states...
    16	Computed 16 initial states...
    17	Computed 32 initial states...
    18	Computed 64 initial states...
    19	Computed 128 initial states...
    20	Computed 256 initial states...
    21	Computed 512 initial states...
    22	Computed 1024 initial states...
    23	Computed 2048 initial states...
    24	Error: Invariant AbandonedArtifactRejected is violated by the initial state:
    25	/\ rcptDelta = 0
    26	/\ revoked = 1
    27	/\ declared = 0
    28	/\ confirmedAt = 1
    29	/\ signed = 0
    30	/\ polEps = 0
    31	/\ polDelta = 0
    32	/\ anchor = 0
    33	/\ rcptEps = 0
    34	
    35	Finished in 01s at (2026-07-07 10:22:32)

===== FILE: P5P6_TemporalRevocation_BrokenConf.tla =====
     1	----------------- MODULE P5P6_TemporalRevocation_BrokenConf -----------------
     2	(***************************************************************************)
     3	(* Tessera Band 0 — P5 DELIBERATELY BROKEN: the PRE-AMENDMENT-2 verifier. *)
     4	(* This verifier checks the anchor block time against the window and      *)
     5	(* nothing else — exactly the acceptance predicate as registered before   *)
     6	(* A2.2 added the confirmation-timing conjunct. It therefore ACCEPTS the  *)
     7	(* abandoned-anchor artifact of A2.0: a discarded issuance attempt whose  *)
     8	(* anchor landed in-window but buried past the window, whose transaction  *)
     9	(* confirmed anyway, paired with the never-shipped receipt.                *)
    10	(*                                                                          *)
    11	(* THE POINT OF THIS MODULE (the A2.0 correction, made mechanical): the   *)
    12	(* artifact is NOT a forgery — every anchor-only invariant PASSES here.   *)
    13	(* ForgeryRejected holds (the anchor still bounds signing), and           *)
    14	(* ReceiptIndependence holds (receipt tolerances are still ignored).      *)
    15	(* Only AbandonedArtifactRejected — the invariant born from the A2.2      *)
    16	(* conjunct — is VIOLATED. Expected result: TLC green on ForgeryRejected  *)
    17	(* and ReceiptIndependence, VIOLATING AbandonedArtifactRejected with a    *)
    18	(* concrete artifact (anchor in-window, confirmedAt past it, accepted).   *)
    19	(* A green run on all three would mean the new conjunct is decorative.    *)
    20	(*                                                                          *)
    21	(* (The main module's extended WindowRespected / VerifierOwnsTolerances   *)
    22	(* contain the confirmedAt clause and would flag here too; they are       *)
    23	(* omitted from the cfg so the report names the most specific catcher,    *)
    24	(* per the sanity-ordering working rule.)                                  *)
    25	(* State space and variables match the correct module exactly; only the   *)
    26	(* missing conjunct differs.                                                *)
    27	(***************************************************************************)
    28	EXTENDS Integers
    29	
    30	CONSTANTS MaxTime, DeltaMax, EpsilonMax, RcptTolMax
    31	
    32	ASSUME DeltaMax \in Nat /\ EpsilonMax \in Nat /\ MaxTime \in Nat
    33	       /\ RcptTolMax \in Nat /\ RcptTolMax > DeltaMax
    34	
    35	NoRev == MaxTime + 1
    36	
    37	VARIABLES declared, signed, anchor, confirmedAt, revoked,
    38	          polDelta, polEps, rcptDelta, rcptEps
    39	
    40	Init ==
    41	  /\ declared  \in 0..MaxTime
    42	  /\ anchor    \in 0..MaxTime
    43	  /\ confirmedAt \in 0..MaxTime
    44	  /\ signed    \in 0..anchor
    45	  /\ revoked   \in 0..MaxTime \cup {NoRev}
    46	  /\ polDelta  \in 0..DeltaMax
    47	  /\ polEps    \in 0..EpsilonMax
    48	  /\ rcptDelta \in 0..RcptTolMax
    49	  /\ rcptEps   \in 0..RcptTolMax
    50	
    51	Next == UNCHANGED <<declared, signed, anchor, confirmedAt, revoked,
    52	                    polDelta, polEps, rcptDelta, rcptEps>>
    53	
    54	(* BROKEN: the A2.2 confirmation-timing conjunct is MISSING — the         *)
    55	(* verifier as registered before Amendment 2.                              *)
    56	TemporalOKWith(rd, re) ==
    57	  /\ anchor >= declared - polEps
    58	  /\ anchor <= declared + polDelta
    59	
    60	AuthorizedThroughWindow ==
    61	  /\ revoked > declared
    62	  /\ revoked > anchor
    63	
    64	StrictAcceptWith(rd, re) == TemporalOKWith(rd, re) /\ AuthorizedThroughWindow
    65	
    66	StrictAccept == StrictAcceptWith(rcptDelta, rcptEps)
    67	
    68	(* Anchor-only invariants from the correct module. EXPECTED: BOTH HOLD —  *)
    69	(* the artifact is not a forgery and involves no receipt tolerance.        *)
    70	ForgeryRejected ==
    71	  (revoked <= signed) => ~StrictAccept
    72	
    73	ReceiptIndependence ==
    74	  \A rd \in 0..RcptTolMax : \A re \in 0..RcptTolMax :
    75	    StrictAcceptWith(rd, re) <=> StrictAccept
    76	
    77	(* The Amendment 2 invariant. EXPECTED: VIOLATED — the counterexample IS  *)
    78	(* the abandoned-anchor artifact.                                           *)
    79	AbandonedArtifactRejected ==
    80	  (/\ anchor >= declared - polEps
    81	   /\ anchor <= declared + polDelta
    82	   /\ confirmedAt > declared + polDelta)
    83	  => ~StrictAccept
    84	
    85	==============================================================================

===== FILE: P5P6_TemporalRevocation_Broken.out =====
1:TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)
5:Parsing file /home/tony/projects/tessera/formal/tla/P5P6_TemporalRevocation_Broken.tla
10:Semantic processing of module P5P6_TemporalRevocation_Broken
11:Starting... (2026-07-07 10:22:27)
27:Error: Invariant ForgeryRejected is violated by the initial state:
38:Finished in 00s at (2026-07-07 10:22:27)
----- final 40 lines -----
     1	TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)
     2	Warning: Please run the Java VM which executes TLC with a throughput optimized garbage collector by passing the "-XX:+UseParallelGC" property.
     3	(Use the -nowarning option to disable this warning.)
     4	Running breadth-first search Model-Checking with fp 128 and seed 2377937344545500320 with 1 worker on 128 cores with 30688MB heap and 64MB offheap memory [pid: 2607434] (Linux 6.18.33.2-microsoft-standard-WSL2 amd64, Ubuntu 11.0.31 x86_64, MSBDiskFPSet, DiskStateQueue).
     5	Parsing file /home/tony/projects/tessera/formal/tla/P5P6_TemporalRevocation_Broken.tla
     6	Parsing file /tmp/Integers.tla
     7	Parsing file /tmp/Naturals.tla
     8	Semantic processing of module Naturals
     9	Semantic processing of module Integers
    10	Semantic processing of module P5P6_TemporalRevocation_Broken
    11	Starting... (2026-07-07 10:22:27)
    12	Computing initial states...
    13	Computed 2 initial states...
    14	Computed 4 initial states...
    15	Computed 8 initial states...
    16	Computed 16 initial states...
    17	Computed 32 initial states...
    18	Computed 64 initial states...
    19	Computed 128 initial states...
    20	Computed 256 initial states...
    21	Computed 512 initial states...
    22	Computed 1024 initial states...
    23	Computed 2048 initial states...
    24	Computed 4096 initial states...
    25	Computed 8192 initial states...
    26	Computed 16384 initial states...
    27	Error: Invariant ForgeryRejected is violated by the initial state:
    28	/\ rcptDelta = 0
    29	/\ revoked = 1
    30	/\ declared = 0
    31	/\ confirmedAt = 0
    32	/\ signed = 1
    33	/\ polEps = 0
    34	/\ polDelta = 1
    35	/\ anchor = 1
    36	/\ rcptEps = 0
    37	
    38	Finished in 00s at (2026-07-07 10:22:27)

===== FILE: P5P6_TemporalRevocation_Broken.tla =====
     1	--------------------- MODULE P5P6_TemporalRevocation_Broken ---------------------
     2	(***************************************************************************)
     3	(* Tessera Band 0 — P6 DELIBERATELY BROKEN: point-evaluated authorization. *)
     4	(* This is P6 exactly as it stood after review round 1 — authorization    *)
     5	(* checked only at declared_issue_time — the weakness GPT-5.5's round-2   *)
     6	(* review found by hand. The model reproduces that attack mechanically:   *)
     7	(* expected result is TLC VIOLATING ForgeryRejected with the concrete     *)
     8	(* assignment (declared just before revocation, signed at/after it,       *)
     9	(* anchor still inside the delta window).                                   *)
    10	(*                                                                          *)
    11	(* A green run of this module would mean the security invariant is        *)
    12	(* vacuous. State space and variables match the correct module exactly    *)
    13	(* (apples-to-apples, incl. the post-Amendment-2 confirmedAt observable   *)
    14	(* and its A2.2 conjunct, which is CORRECT here); only                     *)
    15	(* AuthorizedPointOnly differs.                                             *)
    16	(***************************************************************************)
    17	EXTENDS Integers
    18	
    19	CONSTANTS MaxTime, DeltaMax, EpsilonMax, RcptTolMax
    20	
    21	ASSUME DeltaMax \in Nat /\ EpsilonMax \in Nat /\ MaxTime \in Nat
    22	       /\ RcptTolMax \in Nat /\ RcptTolMax > DeltaMax
    23	
    24	NoRev == MaxTime + 1
    25	
    26	VARIABLES declared, signed, anchor, confirmedAt, revoked,
    27	          polDelta, polEps, rcptDelta, rcptEps
    28	
    29	Init ==
    30	  /\ declared  \in 0..MaxTime
    31	  /\ anchor    \in 0..MaxTime
    32	  /\ confirmedAt \in 0..MaxTime
    33	  /\ signed    \in 0..anchor
    34	  /\ revoked   \in 0..MaxTime \cup {NoRev}
    35	  /\ polDelta  \in 0..DeltaMax
    36	  /\ polEps    \in 0..EpsilonMax
    37	  /\ rcptDelta \in 0..RcptTolMax
    38	  /\ rcptEps   \in 0..RcptTolMax
    39	
    40	Next == UNCHANGED <<declared, signed, anchor, confirmedAt, revoked,
    41	                    polDelta, polEps, rcptDelta, rcptEps>>
    42	
    43	TemporalOK ==
    44	  /\ anchor >= declared - polEps
    45	  /\ anchor <= declared + polDelta
    46	  /\ confirmedAt <= declared + polDelta   \* A2.2 conjunct, correct here
    47	
    48	(* BROKEN: authorization evaluated at the declared time ONLY — the        *)
    49	(* anchor-window clause is missing.                                        *)
    50	AuthorizedPointOnly == revoked > declared
    51	
    52	StrictAccept == TemporalOK /\ AuthorizedPointOnly
    53	
    54	(* Same security theorem as the correct module. EXPECTED: VIOLATED.       *)
    55	ForgeryRejected ==
    56	  (revoked <= signed) => ~StrictAccept
    57	
    58	=================================================================================

===== FILE: P5P6_TemporalRevocation_BrokenTol.cfg =====
     1	CONSTANTS
     2	  MaxTime = 6
     3	  DeltaMax = 3
     4	  EpsilonMax = 1
     5	  RcptTolMax = 6
     6	
     7	INIT Init
     8	NEXT Next
     9	
    10	INVARIANTS
    11	  VerifierOwnsTolerances

===== FILE: P5P6_TemporalRevocation_BrokenTol.out =====
1:TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)
5:Parsing file /home/tony/projects/tessera/formal/tla/P5P6_TemporalRevocation_BrokenTol.tla
10:Semantic processing of module P5P6_TemporalRevocation_BrokenTol
11:Starting... (2026-07-07 10:22:28)
26:Error: Invariant VerifierOwnsTolerances is violated by the initial state:
37:Finished in 00s at (2026-07-07 10:22:29)
----- final 40 lines -----
     1	TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)
     2	Warning: Please run the Java VM which executes TLC with a throughput optimized garbage collector by passing the "-XX:+UseParallelGC" property.
     3	(Use the -nowarning option to disable this warning.)
     4	Running breadth-first search Model-Checking with fp 100 and seed 961990381018500154 with 1 worker on 128 cores with 30688MB heap and 64MB offheap memory [pid: 2607521] (Linux 6.18.33.2-microsoft-standard-WSL2 amd64, Ubuntu 11.0.31 x86_64, MSBDiskFPSet, DiskStateQueue).
     5	Parsing file /home/tony/projects/tessera/formal/tla/P5P6_TemporalRevocation_BrokenTol.tla
     6	Parsing file /tmp/Integers.tla
     7	Parsing file /tmp/Naturals.tla
     8	Semantic processing of module Naturals
     9	Semantic processing of module Integers
    10	Semantic processing of module P5P6_TemporalRevocation_BrokenTol
    11	Starting... (2026-07-07 10:22:28)
    12	Computing initial states...
    13	Computed 2 initial states...
    14	Computed 4 initial states...
    15	Computed 8 initial states...
    16	Computed 16 initial states...
    17	Computed 32 initial states...
    18	Computed 64 initial states...
    19	Computed 128 initial states...
    20	Computed 256 initial states...
    21	Computed 512 initial states...
    22	Computed 1024 initial states...
    23	Computed 2048 initial states...
    24	Computed 4096 initial states...
    25	Computed 8192 initial states...
    26	Error: Invariant VerifierOwnsTolerances is violated by the initial state:
    27	/\ rcptDelta = 4
    28	/\ revoked = 1
    29	/\ declared = 0
    30	/\ confirmedAt = 4
    31	/\ signed = 0
    32	/\ polEps = 0
    33	/\ polDelta = 0
    34	/\ anchor = 0
    35	/\ rcptEps = 0
    36	
    37	Finished in 00s at (2026-07-07 10:22:29)

===== FILE: P5P6_TemporalRevocation_BrokenTolStrict.cfg =====
     1	\* Expected: the three safety invariants HOLD (the narrowing bug is
     2	\* invisible to them); ReceiptIndependence is VIOLATED. That asymmetry is
     3	\* this module's entire point.
     4	CONSTANTS
     5	  MaxTime = 6
     6	  DeltaMax = 3
     7	  EpsilonMax = 1
     8	  RcptTolMax = 6
     9	
    10	INIT Init
    11	NEXT Next
    12	
    13	INVARIANTS
    14	  ForgeryRejected
    15	  WindowRespected
    16	  VerifierOwnsTolerances
    17	  ReceiptIndependence

===== FILE: P5P6_TemporalRevocation_BrokenTolStrict.out =====
1:TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)
5:Parsing file /home/tony/projects/tessera/formal/tla/P5P6_TemporalRevocation_BrokenTolStrict.tla
10:Semantic processing of module P5P6_TemporalRevocation_BrokenTolStrict
11:Starting... (2026-07-07 10:22:29)
24:Error: Invariant ReceiptIndependence is violated by the initial state:
35:Finished in 01s at (2026-07-07 10:22:31)
----- final 40 lines -----
     1	TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)
     2	Warning: Please run the Java VM which executes TLC with a throughput optimized garbage collector by passing the "-XX:+UseParallelGC" property.
     3	(Use the -nowarning option to disable this warning.)
     4	Running breadth-first search Model-Checking with fp 10 and seed 3768887423278929604 with 1 worker on 128 cores with 30688MB heap and 64MB offheap memory [pid: 2607578] (Linux 6.18.33.2-microsoft-standard-WSL2 amd64, Ubuntu 11.0.31 x86_64, MSBDiskFPSet, DiskStateQueue).
     5	Parsing file /home/tony/projects/tessera/formal/tla/P5P6_TemporalRevocation_BrokenTolStrict.tla
     6	Parsing file /tmp/Integers.tla
     7	Parsing file /tmp/Naturals.tla
     8	Semantic processing of module Naturals
     9	Semantic processing of module Integers
    10	Semantic processing of module P5P6_TemporalRevocation_BrokenTolStrict
    11	Starting... (2026-07-07 10:22:29)
    12	Computing initial states...
    13	Computed 2 initial states...
    14	Computed 4 initial states...
    15	Computed 8 initial states...
    16	Computed 16 initial states...
    17	Computed 32 initial states...
    18	Computed 64 initial states...
    19	Computed 128 initial states...
    20	Computed 256 initial states...
    21	Computed 512 initial states...
    22	Computed 1024 initial states...
    23	Computed 2048 initial states...
    24	Error: Invariant ReceiptIndependence is violated by the initial state:
    25	/\ rcptDelta = 0
    26	/\ revoked = 1
    27	/\ declared = 0
    28	/\ confirmedAt = 1
    29	/\ signed = 0
    30	/\ polEps = 0
    31	/\ polDelta = 1
    32	/\ anchor = 0
    33	/\ rcptEps = 0
    34	
    35	Finished in 01s at (2026-07-07 10:22:31)

===== FILE: P5P6_TemporalRevocation_BrokenTolStrict.tla =====
     1	---------------- MODULE P5P6_TemporalRevocation_BrokenTolStrict ----------------
     2	(***************************************************************************)
     3	(* Tessera Band 0 — P5 DELIBERATELY BROKEN, the SUBTLE variant:           *)
     4	(* receipt-NARROWED tolerances. The implementation honors the SMALLER of  *)
     5	(* the verifier's tolerance and the receipt-declared one ("the receipt    *)
     6	(* only asks for a tighter window — surely stricter is safe?").            *)
     7	(*                                                                          *)
     8	(* Why this is a real bug and not extra safety: it hands the ISSUER       *)
     9	(* control over verification outcomes. An issuer can craft a receipt      *)
    10	(* that verifies for parties checking promptly but fails for anyone      *)
    11	(* whose anchor-to-declared gap exceeds the receipt's narrowed window —   *)
    12	(* issuer-selected verdict manipulation, violating "delta and epsilon     *)
    13	(* belong to the verifier" (A1.2 P5) just as surely as enlargement does.  *)
    14	(*                                                                          *)
    15	(* THE POINT OF THIS MODULE: every pure safety invariant PASSES here —    *)
    16	(* VerifierOwnsTolerances holds (narrowed acceptance is still inside the  *)
    17	(* maxima), WindowRespected holds, ForgeryRejected holds. Only            *)
    18	(* ReceiptIndependence catches it. Expected result: TLC green on all     *)
    19	(* safety invariants, VIOLATING ReceiptIndependence — proving that        *)
    20	(* invariant is load-bearing, not decorative.                              *)
    21	(* Identical state space; only the effective-tolerance computation        *)
    22	(* differs.                                                                 *)
    23	(***************************************************************************)
    24	EXTENDS Integers
    25	
    26	CONSTANTS MaxTime, DeltaMax, EpsilonMax, RcptTolMax
    27	
    28	ASSUME DeltaMax \in Nat /\ EpsilonMax \in Nat /\ MaxTime \in Nat
    29	       /\ RcptTolMax \in Nat /\ RcptTolMax > DeltaMax
    30	
    31	NoRev == MaxTime + 1
    32	
    33	VARIABLES declared, signed, anchor, confirmedAt, revoked,
    34	          polDelta, polEps, rcptDelta, rcptEps
    35	
    36	Init ==
    37	  /\ declared  \in 0..MaxTime
    38	  /\ anchor    \in 0..MaxTime
    39	  /\ confirmedAt \in 0..MaxTime
    40	  /\ signed    \in 0..anchor
    41	  /\ revoked   \in 0..MaxTime \cup {NoRev}
    42	  /\ polDelta  \in 0..DeltaMax
    43	  /\ polEps    \in 0..EpsilonMax
    44	  /\ rcptDelta \in 0..RcptTolMax
    45	  /\ rcptEps   \in 0..RcptTolMax
    46	
    47	Next == UNCHANGED <<declared, signed, anchor, confirmedAt, revoked,
    48	                    polDelta, polEps, rcptDelta, rcptEps>>
    49	
    50	Min(a, b) == IF a < b THEN a ELSE b
    51	
    52	(* BROKEN: effective tolerances honor receipt-declared NARROWING — in     *)
    53	(* every conjunct, including the A2.2 confirmation-timing one.             *)
    54	TemporalOKWith(rd, re) ==
    55	  /\ anchor >= declared - Min(polEps, re)
    56	  /\ anchor <= declared + Min(polDelta, rd)
    57	  /\ confirmedAt <= declared + Min(polDelta, rd)
    58	
    59	AuthorizedThroughWindow ==
    60	  /\ revoked > declared
    61	  /\ revoked > anchor
    62	
    63	StrictAcceptWith(rd, re) == TemporalOKWith(rd, re) /\ AuthorizedThroughWindow
    64	
    65	StrictAccept == StrictAcceptWith(rcptDelta, rcptEps)
    66	
    67	(* Safety invariants from the correct module. EXPECTED: ALL HOLD — the    *)
    68	(* narrowing bug is invisible to them.                                      *)
    69	ForgeryRejected ==
    70	  (revoked <= signed) => ~StrictAccept
    71	
    72	WindowRespected ==
    73	  StrictAccept => (/\ anchor - declared <= polDelta
    74	                   /\ declared - anchor <= polEps
    75	                   /\ confirmedAt - declared <= polDelta)
    76	
    77	VerifierOwnsTolerances ==
    78	  StrictAccept =>
    79	    (/\ anchor - declared <= DeltaMax
    80	     /\ declared - anchor <= EpsilonMax
    81	     /\ confirmedAt - declared <= DeltaMax)
    82	
    83	(* Independence invariant from the correct module. EXPECTED: VIOLATED —   *)
    84	(* the verdict now varies with the receipt-declared tolerances.            *)
    85	ReceiptIndependence ==
    86	  \A rd \in 0..RcptTolMax : \A re \in 0..RcptTolMax :
    87	    StrictAcceptWith(rd, re) <=> StrictAccept
    88	
    89	=================================================================================

===== FILE: P5P6_TemporalRevocation_BrokenTol.tla =====
     1	------------------- MODULE P5P6_TemporalRevocation_BrokenTol -------------------
     2	(***************************************************************************)
     3	(* Tessera Band 0 — P5 DELIBERATELY BROKEN: receipt-controlled            *)
     4	(* tolerances. The implementation bug A1.2 P5 forbids: the verifier       *)
     5	(* honors the LARGER of its own tolerance and the receipt-declared one    *)
     6	(* ("the receipt says 96 hours is fine, so 96 hours is fine"). A          *)
     7	(* malicious issuer writes an enormous window into the receipt and the    *)
     8	(* temporal guarantee dissolves.                                            *)
     9	(*                                                                          *)
    10	(* Expected result: TLC VIOLATES VerifierOwnsTolerances — exhibiting an   *)
    11	(* acceptance whose anchor-to-declared gap exceeds the strict maxima,     *)
    12	(* enabled by an oversized rcptDelta/rcptEps. A green run would mean the  *)
    13	(* invariant cannot detect receipt-controlled enlargement.                  *)
    14	(* State space and variables match the correct module exactly; only the   *)
    15	(* effective-tolerance computation differs.                                 *)
    16	(***************************************************************************)
    17	EXTENDS Integers
    18	
    19	CONSTANTS MaxTime, DeltaMax, EpsilonMax, RcptTolMax
    20	
    21	ASSUME DeltaMax \in Nat /\ EpsilonMax \in Nat /\ MaxTime \in Nat
    22	       /\ RcptTolMax \in Nat /\ RcptTolMax > DeltaMax
    23	
    24	NoRev == MaxTime + 1
    25	
    26	VARIABLES declared, signed, anchor, confirmedAt, revoked,
    27	          polDelta, polEps, rcptDelta, rcptEps
    28	
    29	Init ==
    30	  /\ declared  \in 0..MaxTime
    31	  /\ anchor    \in 0..MaxTime
    32	  /\ confirmedAt \in 0..MaxTime
    33	  /\ signed    \in 0..anchor
    34	  /\ revoked   \in 0..MaxTime \cup {NoRev}
    35	  /\ polDelta  \in 0..DeltaMax
    36	  /\ polEps    \in 0..EpsilonMax
    37	  /\ rcptDelta \in 0..RcptTolMax
    38	  /\ rcptEps   \in 0..RcptTolMax
    39	
    40	Next == UNCHANGED <<declared, signed, anchor, confirmedAt, revoked,
    41	                    polDelta, polEps, rcptDelta, rcptEps>>
    42	
    43	Max(a, b) == IF a > b THEN a ELSE b
    44	
    45	(* BROKEN: effective tolerances honor receipt-declared enlargement — in   *)
    46	(* every conjunct, including the A2.2 confirmation-timing one.             *)
    47	(* Parameterized shape matches the correct module (apples-to-apples).      *)
    48	TemporalOKWith(rd, re) ==
    49	  /\ anchor >= declared - Max(polEps, re)
    50	  /\ anchor <= declared + Max(polDelta, rd)
    51	  /\ confirmedAt <= declared + Max(polDelta, rd)
    52	
    53	AuthorizedThroughWindow ==
    54	  /\ revoked > declared
    55	  /\ revoked > anchor
    56	
    57	StrictAcceptWith(rd, re) == TemporalOKWith(rd, re) /\ AuthorizedThroughWindow
    58	
    59	StrictAccept == StrictAcceptWith(rcptDelta, rcptEps)
    60	
    61	(* Same invariant as the correct module. EXPECTED: VIOLATED.              *)
    62	VerifierOwnsTolerances ==
    63	  StrictAccept =>
    64	    (/\ anchor - declared <= DeltaMax
    65	     /\ declared - anchor <= EpsilonMax
    66	     /\ confirmedAt - declared <= DeltaMax)
    67	
    68	=================================================================================

===== FILE: P5P6_TemporalRevocation.cfg =====
     1	CONSTANTS
     2	  MaxTime = 6
     3	  DeltaMax = 3
     4	  EpsilonMax = 1
     5	  RcptTolMax = 6
     6	
     7	INIT Init
     8	NEXT Next
     9	
    10	INVARIANTS
    11	  ForgeryRejected
    12	  WindowRespected
    13	  VerifierOwnsTolerances
    14	  AbandonedArtifactRejected
    15	  ReceiptIndependence
    16	  AuthorizedAtDeclared
    17	  HonestCostIsExactlyTheWindow

===== FILE: P5P6_TemporalRevocation.out =====
1:TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)
5:Parsing file /home/tony/projects/tessera/formal/tla/P5P6_TemporalRevocation.tla
10:Semantic processing of module P5P6_TemporalRevocation
11:Starting... (2026-07-07 10:19:11)
35:Finished computing initial states: 4302592 distinct states generated at 2026-07-07 10:21:45.
36:Model checking completed. No error has been found.
38:  because two distinct states had the same fingerprint:
41:8605184 states generated, 4302592 distinct states found, 0 states left on queue.
44:Finished in 02min 38s at (2026-07-07 10:21:48)
----- final 40 lines -----
     1	Parsing file /home/tony/projects/tessera/formal/tla/P5P6_TemporalRevocation.tla
     2	Parsing file /tmp/Integers.tla
     3	Parsing file /tmp/Naturals.tla
     4	Semantic processing of module Naturals
     5	Semantic processing of module Integers
     6	Semantic processing of module P5P6_TemporalRevocation
     7	Starting... (2026-07-07 10:19:11)
     8	Computing initial states...
     9	Computed 2 initial states...
    10	Computed 4 initial states...
    11	Computed 8 initial states...
    12	Computed 16 initial states...
    13	Computed 32 initial states...
    14	Computed 64 initial states...
    15	Computed 128 initial states...
    16	Computed 256 initial states...
    17	Computed 512 initial states...
    18	Computed 1024 initial states...
    19	Computed 2048 initial states...
    20	Computed 4096 initial states...
    21	Computed 8192 initial states...
    22	Computed 16384 initial states...
    23	Computed 32768 initial states...
    24	Computed 65536 initial states...
    25	Computed 131072 initial states...
    26	Computed 262144 initial states...
    27	Computed 524288 initial states...
    28	Computed 1048576 initial states...
    29	Computed 2097152 initial states...
    30	Computed 4194304 initial states...
    31	Finished computing initial states: 4302592 distinct states generated at 2026-07-07 10:21:45.
    32	Model checking completed. No error has been found.
    33	  Estimates of the probability that TLC did not check all reachable states
    34	  because two distinct states had the same fingerprint:
    35	  calculated (optimistic):  val = 1.0E-6
    36	  based on the actual fingerprints:  val = 3.2E-11
    37	8605184 states generated, 4302592 distinct states found, 0 states left on queue.
    38	The depth of the complete state graph search is 1.
    39	The average outdegree of the complete state graph is 0 (minimum is 0, the maximum 0 and the 95th percentile is 0).
    40	Finished in 02min 38s at (2026-07-07 10:21:48)

===== FILE: P5P6_TemporalRevocation_Sanity.cfg =====
     1	\* Vacuity check: run with `tlc2.TLC -continue`. TLC VIOLATING all four
     2	\* invariants is the healthy result — each violation exhibits a reachable
     3	\* state satisfying a defined-predicate antecedent, proving the main
     4	\* cfg's implication-shaped invariants are not vacuously true.
     5	\* Order matters (most specific first): NonMonotonicAccept is a subset of
     6	\* Acceptance; LateBurial witnesses the A2.0 artifact for
     7	\* AbandonedArtifactRejected.
     8	CONSTANTS
     9	  MaxTime = 6
    10	  DeltaMax = 3
    11	  EpsilonMax = 1
    12	  RcptTolMax = 6
    13	
    14	INIT Init
    15	NEXT Next
    16	
    17	INVARIANTS
    18	  NonMonotonicAcceptUnreachable
    19	  AcceptanceUnreachable
    20	  LateBurialCaseUnreachable
    21	  HonestCostCaseUnreachable

===== FILE: P5P6_TemporalRevocation_Sanity.out =====
1:TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)
5:Parsing file /home/tony/projects/tessera/formal/tla/P5P6_TemporalRevocation.tla
10:[... 1078294 violation reports elided from this evidence file; the sanity
11: methodology EXPECTS violations (vacuity witnesses). Per-invariant counts:
12:    441098 Invariant AcceptanceUnreachable is violated
13:    101528 Invariant HonestCostCaseUnreachable is violated
14:    267736 Invariant LateBurialCaseUnreachable is violated
15:    267932 Invariant NonMonotonicAcceptUnreachable is violated
20:8605184 states generated, 4302592 distinct states found, 0 states left on queue.
23:Finished in 52s at (2026-07-07 10:23:56)
----- final 40 lines -----
     1	TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)
     2	Warning: Please run the Java VM which executes TLC with a throughput optimized garbage collector by passing the "-XX:+UseParallelGC" property.
     3	(Use the -nowarning option to disable this warning.)
     4	Running breadth-first search Model-Checking with fp 0 and seed -4029338531182993631 with 1 worker on 128 cores with 30688MB heap and 64MB offheap memory [pid: 2608494] (Linux 6.18.33.2-microsoft-standard-WSL2 amd64, Ubuntu 11.0.31 x86_64, MSBDiskFPSet, DiskStateQueue).
     5	Parsing file /home/tony/projects/tessera/formal/tla/P5P6_TemporalRevocation.tla
     6	Parsing file /tmp/Integers.tla
     7	Parsing file /tmp/Naturals.tla
     8	Semantic processing of module Naturals
     9	
    10	[... 1078294 violation reports elided from this evidence file; the sanity
    11	 methodology EXPECTS violations (vacuity witnesses). Per-invariant counts:
    12	    441098 Invariant AcceptanceUnreachable is violated
    13	    101528 Invariant HonestCostCaseUnreachable is violated
    14	    267736 Invariant LateBurialCaseUnreachable is violated
    15	    267932 Invariant NonMonotonicAcceptUnreachable is violated
    16	 Full raw output (11.9M lines) recoverable at commit 70f2105. ...]
    17	
    18	  calculated (optimistic):  val = 1.0E-6
    19	  based on the actual fingerprints:  val = 1.2E-11
    20	8605184 states generated, 4302592 distinct states found, 0 states left on queue.
    21	The depth of the complete state graph search is 1.
    22	The average outdegree of the complete state graph is 0 (minimum is 0, the maximum 0 and the 95th percentile is 0).
    23	Finished in 52s at (2026-07-07 10:23:56)

===== FILE: P5P6_TemporalRevocation.tla =====
     1	------------------------ MODULE P5P6_TemporalRevocation ------------------------
     2	(***************************************************************************)
     3	(* Tessera Band 0 — P5 (two-sided temporal soundness) and P6 (revocation  *)
     4	(* over the uncertainty window), jointly: they share the temporal          *)
     5	(* vocabulary of A1.6 and P6's whole content is its interaction with       *)
     6	(* P5's window. Authoritative statements: Amendment 1 §A1.2 (P5, P6),      *)
     7	(* §A1.6.                                                                   *)
     8	(*                                                                          *)
     9	(* SCOPE BOUNDARY (revised by Amendment 2): this module discharges the    *)
    10	(* VERIFIER-SIDE face of P5 — the acceptance predicate over declared/      *)
    11	(* anchor/confirmedAt/policy. P5's issuance-protocol corollary (ship       *)
    12	(* rule, re-issue, attempt bound) remains ISSUER-side behavior, modeled    *)
    13	(* in P5c_IssuanceProtocol. Amendment 2 (A2.2) gave the corollary a        *)
    14	(* verifier-checkable face — the confirmation-timing conjunct              *)
    15	(* confirmedAt <= declared + delta — and that face lives HERE: it is the   *)
    16	(* same predicate the issuer's Ship rule evaluates (A2.1, one predicate    *)
    17	(* on one chain-visible observable, both sides), so the correspondence     *)
    18	(* between this module's acceptance and P5c's Ship is exact by             *)
    19	(* construction, not by argument.                                           *)
    20	(*                                                                          *)
    21	(* Time is abstract small integers (TLC-bounded); DeltaMax and EpsilonMax  *)
    22	(* are scaled-down stand-ins for the ratified 72h/24h strict maxima — the  *)
    23	(* model checks the LOGIC of the window, not the magnitudes. Signature     *)
    24	(* checks are abstracted as passing (that face belongs to the ProVerif    *)
    25	(* models and P4); this module isolates the temporal/authorization face.   *)
    26	(*                                                                          *)
    27	(* Reading guide (Tony):                                                    *)
    28	(*   declared  - declared_issue_time, what the issuer claims (adversarial: *)
    29	(*               unconstrained; a forger declares whatever helps).          *)
    30	(*   signed    - the actual signing moment. NOT observable by the          *)
    31	(*               verifier; it exists in the model so the security          *)
    32	(*               invariant can quantify over what the verifier cannot see. *)
    33	(*   anchor    - Bitcoin block time of the OTS anchor. The one Layer 2     *)
    34	(*               fact: bytes existed not-after anchor, hence signed <=     *)
    35	(*               anchor is a model CONSTRAINT (the anchor assumption, not  *)
    36	(*               a verifier check).                                         *)
    37	(*   confirmedAt - timestamp of the block granting the k-th confirmation  *)
    38	(*               (height h+k-1; A2.1). Chain-visible to issuer and        *)
    39	(*               verifier alike. Deliberately UNCONSTRAINED relative to   *)
    40	(*               anchor: block timestamps are not monotonic (A2.1), so    *)
    41	(*               confirmedAt < anchor is a legal state and the model      *)
    42	(*               assumes no ordering.                                      *)
    43	(*   revoked   - the key's revocation time; NoRev = never. Lifecycle is    *)
    44	(*               monotonic per P6 (revocation is terminal), which is what  *)
    45	(*               lets one number represent it.                              *)
    46	(*   polDelta, polEps   - the VERIFIER's chosen tolerances; may be         *)
    47	(*               stricter than the strict maxima, never larger (A1.2 P5:   *)
    48	(*               "delta and epsilon belong to the verifier").               *)
    49	(*   rcptDelta, rcptEps - tolerances DECLARED BY THE RECEIPT, adversarial, *)
    50	(*               possibly enormous. The verifier must IGNORE these: they   *)
    51	(*               appear in the state precisely so the invariants can       *)
    52	(*               check that acceptance never depends on them. A future     *)
    53	(*               edit routing them into TemporalOK breaks                   *)
    54	(*               VerifierOwnsTolerances - see the _BrokenTol companion.    *)
    55	(* The verifier sees declared, anchor, confirmedAt, revoked, and its own   *)
    56	(* policy — never signed.                                                   *)
    57	(***************************************************************************)
    58	EXTENDS Integers
    59	
    60	CONSTANTS MaxTime, DeltaMax, EpsilonMax, RcptTolMax
    61	
    62	ASSUME DeltaMax \in Nat /\ EpsilonMax \in Nat /\ MaxTime \in Nat
    63	       /\ RcptTolMax \in Nat /\ RcptTolMax > DeltaMax  \* receipts CAN overclaim
    64	
    65	NoRev == MaxTime + 1  \* revocation never happens (sorts after all times)
    66	
    67	VARIABLES declared, signed, anchor, confirmedAt, revoked,
    68	          polDelta, polEps, rcptDelta, rcptEps
    69	
    70	(* Every combination the universe permits. The one constraint is the      *)
    71	(* anchor upper-bound assumption: the signed bytes existed when anchored.  *)
    72	(* confirmedAt carries NO constraint relative to anchor — non-monotonic   *)
    73	(* block timestamps, A2.1.                                                  *)
    74	Init ==
    75	  /\ declared  \in 0..MaxTime
    76	  /\ anchor    \in 0..MaxTime
    77	  /\ confirmedAt \in 0..MaxTime
    78	  /\ signed    \in 0..anchor         \* Layer 2: existence not-after anchor
    79	  /\ revoked   \in 0..MaxTime \cup {NoRev}
    80	  /\ polDelta  \in 0..DeltaMax       \* verifier may choose stricter, never larger
    81	  /\ polEps    \in 0..EpsilonMax
    82	  /\ rcptDelta \in 0..RcptTolMax     \* adversarial receipt claims, incl. oversized
    83	  /\ rcptEps   \in 0..RcptTolMax
    84	
    85	Next == UNCHANGED <<declared, signed, anchor, confirmedAt, revoked,
    86	                    polDelta, polEps, rcptDelta, rcptEps>>
    87	
    88	(***************************************************************************)
    89	(* The verifier's temporal/authorization checks — over observables only,  *)
    90	(* and over the VERIFIER'S tolerances only. The computation is written    *)
    91	(* with the receipt tolerances as EXPLICIT ARGUMENTS it deliberately      *)
    92	(* ignores: ReceiptIndependence below quantifies over all argument values *)
    93	(* and pins the ignoring. Any future edit that routes receipt tolerances  *)
    94	(* into the window — enlarging (see _BrokenTol) or, subtler,              *)
    95	(* narrowing (see _BrokenTolStrict: issuer-controlled verdict             *)
    96	(* manipulation that every pure safety invariant misses) — breaks it.     *)
    97	(***************************************************************************)
    98	
    99	(* P5: two-sided consistency under the verifier's policy, plus the A2.2   *)
   100	(* confirmation-timing conjunct (third line) — the verifier-checkable     *)
   101	(* face of the issuance corollary, on the verifier's OWN delta. rd/re are *)
   102	(* the receipt-declared tolerances — unused by design; the signature      *)
   103	(* exists so independence is checkable.                                     *)
   104	TemporalOKWith(rd, re) ==
   105	  /\ anchor >= declared - polEps
   106	  /\ anchor <= declared + polDelta
   107	  /\ confirmedAt <= declared + polDelta   \* A2.2: k-th confirmation in-window
   108	
   109	TemporalOK == TemporalOKWith(rcptDelta, rcptEps)
   110	
   111	(* P6: authorization throughout the uncertainty window —                  *)
   112	(*   key_authorized(declared)  i.e. revocation, if any, is after declared *)
   113	(*   AND no revocation effective at or before anchor.                     *)
   114	(* Note both conjuncts are needed: with polEps > 0 the anchor may precede *)
   115	(* declared, so revoked > anchor does not imply revoked > declared.        *)
   116	AuthorizedThroughWindow ==
   117	  /\ revoked > declared
   118	  /\ revoked > anchor
   119	
   120	(* The strict-path temporal verdict (this module's face of VALID_STRICT). *)
   121	StrictAcceptWith(rd, re) == TemporalOKWith(rd, re) /\ AuthorizedThroughWindow
   122	
   123	StrictAccept == StrictAcceptWith(rcptDelta, rcptEps)
   124	
   125	(***************************************************************************)
   126	(* Invariants.                                                              *)
   127	(***************************************************************************)
   128	
   129	(* THE P6 SECURITY THEOREM (the round-2 attack, defeated): bytes signed   *)
   130	(* at or after revocation are never strict-accepted — even though the     *)
   131	(* verifier cannot observe the signing time, and under EVERY verifier     *)
   132	(* policy choice. The proof shape: signed <= anchor (Layer 2), so revoked *)
   133	(* <= signed forces revoked <= anchor, which AuthorizedThroughWindow      *)
   134	(* rejects. TLC checks it exhaustively.                                     *)
   135	ForgeryRejected ==
   136	  (revoked <= signed) => ~StrictAccept
   137	
   138	(* P5, restated over acceptance: no strict-accepted receipt sits outside  *)
   139	(* the verifier-policy window (backdating bounded by polDelta,            *)
   140	(* post-dating by polEps).                                                  *)
   141	WindowRespected ==
   142	  StrictAccept => (/\ anchor - declared <= polDelta
   143	                   /\ declared - anchor <= polEps
   144	                   /\ confirmedAt - declared <= polDelta)
   145	
   146	(* A1.2 P5, "delta and epsilon belong to the verifier, not the receipt":  *)
   147	(* acceptance NEVER exceeds the strict maxima, whatever tolerances the    *)
   148	(* receipt declares. In this (correct) model rcptDelta/rcptEps are        *)
   149	(* ignored, so this holds; the _BrokenTol companion routes them into the  *)
   150	(* window and TLC exhibits a receipt-enlarged acceptance violating it.    *)
   151	VerifierOwnsTolerances ==
   152	  StrictAccept =>
   153	    (/\ anchor - declared <= DeltaMax
   154	     /\ declared - anchor <= EpsilonMax
   155	     /\ confirmedAt - declared <= DeltaMax)
   156	
   157	(* THE A2.0 ARTIFACT, REJECTED (Amendment 2): an anchor whose block is    *)
   158	(* in-window but whose k-th confirmation arrived past the window — the    *)
   159	(* discarded-attempt artifact that strict issuance never ships but whose  *)
   160	(* transaction typically confirms anyway. The pre-A2 verifier             *)
   161	(* (anchor-only checks) accepts it; the _BrokenConf companion carries     *)
   162	(* that verifier, passes every anchor-only invariant, and violates        *)
   163	(* exactly this one.                                                        *)
   164	AbandonedArtifactRejected ==
   165	  (/\ anchor >= declared - polEps
   166	   /\ anchor <= declared + polDelta
   167	   /\ confirmedAt > declared + polDelta)
   168	  => ~StrictAccept
   169	
   170	(* Full noninterference, "ignore receipt tolerances" taken literally: the *)
   171	(* verdict is IDENTICAL under every receipt-declared tolerance pair — not *)
   172	(* merely bounded by the maxima. This is strictly stronger than           *)
   173	(* VerifierOwnsTolerances: a bug giving the receipt a NARROWING influence *)
   174	(* (effective window = min of policy and receipt) passes every safety     *)
   175	(* invariant above — acceptance stays inside the maxima — yet hands the   *)
   176	(* issuer control over other parties' verification outcomes. Only this    *)
   177	(* invariant catches it (_BrokenTolStrict).                                *)
   178	ReceiptIndependence ==
   179	  \A rd \in 0..RcptTolMax : \A re \in 0..RcptTolMax :
   180	    StrictAcceptWith(rd, re) <=> StrictAccept
   181	
   182	(* P6 second clause standing alone: acceptance implies the key was        *)
   183	(* authorized at the declared issue time itself.                           *)
   184	AuthorizedAtDeclared ==
   185	  StrictAccept => declared < revoked
   186	
   187	(* P6 fail-closed cost, made exact (not just accepted rhetorically): the  *)
   188	(* ONLY honest receipts the interval rule sacrifices are those whose key  *)
   189	(* was revoked inside (declared, anchor] — signed before revocation       *)
   190	(* (honest) but revoked before the anchor confirmed. Everything else      *)
   191	(* honest is accepted if temporally consistent.                            *)
   192	HonestCostIsExactlyTheWindow ==
   193	  (/\ TemporalOK
   194	   /\ signed < revoked          \* honestly signed while authorized
   195	   /\ revoked > declared        \* authorized at declaration too
   196	   /\ ~StrictAccept)
   197	  => (revoked <= anchor)        \* ...then revocation landed in the window
   198	
   199	(* Vacuity checks — used ONLY by the _Sanity cfg (run with TLC            *)
   200	(* -continue), where TLC VIOLATING both is the healthy result: each       *)
   201	(* violation exhibits a reachable state satisfying a defined-predicate    *)
   202	(* antecedent, so the implications above are not vacuously true.           *)
   203	NonMonotonicAcceptUnreachable ==      \* accepted with confirmedAt < anchor:
   204	  ~(StrictAccept /\ confirmedAt < anchor)  \* non-monotonicity (A2.1) exercised
   205	AcceptanceUnreachable == ~StrictAccept
   206	LateBurialCaseUnreachable ==          \* the A2.0 artifact is reachable, so
   207	  ~(/\ anchor >= declared - polEps    \* AbandonedArtifactRejected is not vacuous
   208	    /\ anchor <= declared + polDelta
   209	    /\ confirmedAt > declared + polDelta)
   210	HonestCostCaseUnreachable ==
   211	  ~(/\ TemporalOK
   212	    /\ signed < revoked
   213	    /\ revoked > declared
   214	    /\ ~StrictAccept)
   215	
   216	=================================================================================

===== FILE: REGISTERED-P5-P6.txt =====
     1	- **P5 — Temporal soundness (two-sided).** The anchor is an upper bound on
     2	  creation time, and only that (A1.6). Strict verification requires the
     3	  anchor to be consistent with the declared issue time **in both
     4	  directions**:
     5	
     6	      declared_issue_time − ε  ≤  anchor_time  ≤  declared_issue_time + δ
     7	
     8	  The δ side **bounds** *backdating*: a forger signing new bytes cannot
     9	  obtain a conforming anchor for a claimed time more than δ in the past —
    10	  backdating within the tolerance window is not eliminated, only bounded.
    11	  The ε side **bounds** *post-dating*: an issuer cannot declare an issue
    12	  time more than ε after the anchor and later present the receipt as
    13	  fresh.
    14	
    15	  **δ and ε belong to the verifier, not the receipt.** A receipt records
    16	  its issue-time policy version and the observed anchor delay; it may not
    17	  choose its own temporal tolerances — a receipt-controlled tolerance
    18	  would let a malicious issuer write an enormous window into the signed
    19	  bytes. The reference verifier's strict policy fixes the maxima: **δ =
    20	  72 hours** (OTS aggregation-to-confirmation lag plus Bitcoin timestamp
    21	  skew), **ε = 24 hours** (Bitcoin block timestamps may lag real time by
    22	  hours under the median-time-past rule). A verifier may choose stricter
    23	  bounds; no degraded policy may enlarge δ or ε beyond the strict maxima.
    24	  Both maxima are ratified (or revised, on the record) at Band 0 exit.
    25	  Temporal-anchor consistency is **non-waivable** (A1.2.1). **[model]**,
    26	  resting on the Bitcoin/OTS assumptions of A1.6 **[assumption]**.
    27	
    28	  *Issuance-protocol corollary (so honest receipts cannot rot):* issuance
    29	  is not complete until the anchor is **confirmed** — buried at a minimum
    30	  confirmation depth **k** on the Bitcoin chain (strict default **k = 6**,
    31	  ratified with δ and ε at Band 0 exit) — within δ of
    32	  `declared_issue_time`. Depth is what "confirmed" *means*: a
    33	  one-confirmation anchor orphaned by a transient reorganization would
    34	  leave an already-shipped receipt permanently unverifiable, so a receipt
    35	  never ships on a shallow anchor. If confirmation is delayed past δ for
    36	  benign reasons (calendar outage, fee spikes, reorg), the receipt is
    37	  **re-issued** with a fresh declared time and re-anchored — the failed
    38	  attempt is discarded, not shipped. Without this rule, honest-but-late
    39	  anchoring would be permanently indistinguishable from backdating.
    40	
    41	- **P6 — Revocation time-relativity (evaluated over the uncertainty
    42	  window).** The anchor proves only that the signed bytes existed *not
    43	  after* `anchor_time`; it cannot locate the signing moment inside
    44	  [`declared_issue_time`, `anchor_time`]. Evaluating authorization only
    45	  at `declared_issue_time` would therefore admit a revocation/backdating
    46	  interaction: a key revoked inside the δ window could sign *after*
    47	  revocation while declaring a time just before it, and pass both P5 and
    48	  a point-evaluated P6. Accordingly, `VALID_STRICT` requires
    49	  authorization **throughout the uncertainty window**:
    50	
    51	      key_authorized(declared_issue_time)
    52	      ∧ no revocation effective at or before anchor_time
    53	
    54	  Revocation effective *after* `anchor_time` does not retroactively
    55	  change the verdict. Revocation effective at or before `anchor_time`
    56	  yields `INVALID`.
    57	
    58	  **Key lifecycle is monotonic, by design commitment.** Revocation is
    59	  terminal: a revoked key is never re-authorized; re-keying issues a *new*
    60	  key with a new fingerprint and a new manifest entry. Without
    61	  monotonicity, "no revocation effective at or before `anchor_time`"
    62	  would be ambiguous across revoke–re-authorize cycles; with it, the
    63	  interval check is well-defined. This is an issuer key-management rule
    64	  that the model *assumes* and operational policy *enforces* — a design
    65	  commitment, not a cryptographic assumption, and deliberately not filed
    66	  under Layer 2.
    67	
    68	  This interval evaluation is deliberately stricter than checking
    69	  `declared_issue_time` alone, and it can fail honest receipts whose key
    70	  was revoked between declaration and anchor confirmation — the correct
    71	  fail-closed outcome: the system cannot honestly prove such a receipt
    72	  was signed before the revocation, and the issuance protocol (P5
    73	  corollary) already treats unconfirmed issuance as incomplete. (The
    74	  checkable form of §4.4's revocation paragraph, in A1.6's vocabulary.)
    75	  **[model]**
    76	
