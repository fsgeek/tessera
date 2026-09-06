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

===== FILE: P4_VerifierStates_Broken.cfg =====
     1	CONSTANTS
     2	  Checks = {c1, c2, c3, c4, c5}
     3	  NonWaivable = {c1, c2}
     4	
     5	INIT Init
     6	NEXT Next
     7	
     8	INVARIANTS
     9	  Partition
    10	  Monotonicity
    11	  NoSilentPromotion
    12	  ValidNeedsNonWaivablePass
    13	  StrictMeansEverything
    14	  DegradedNeedsExplicitWaiver
    15	  UnverifiableIsHonest

===== FILE: P4_VerifierStates_Broken.out =====
1:TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)
13:Starting... (2026-07-05 10:24:43)
19:Error: Invariant StrictMeansEverything is violated by the initial state:
27:Finished in 00s at (2026-07-05 10:24:43)
----- final 40 lines -----
     1	TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)
     2	Warning: Please run the Java VM which executes TLC with a throughput optimized garbage collector by passing the "-XX:+UseParallelGC" property.
     3	(Use the -nowarning option to disable this warning.)
     4	Running breadth-first search Model-Checking with fp 45 and seed -1833024302997315497 with 1 worker on 128 cores with 30688MB heap and 64MB offheap memory [pid: 1577870] (Linux 6.18.33.2-microsoft-standard-WSL2 amd64, Ubuntu 11.0.31 x86_64, MSBDiskFPSet, DiskStateQueue).
     5	Parsing file /home/tony/projects/tessera/formal/tla/P4_VerifierStates_Broken.tla
     6	Parsing file /tmp/FiniteSets.tla
     7	Parsing file /tmp/Naturals.tla
     8	Parsing file /tmp/Sequences.tla
     9	Semantic processing of module Naturals
    10	Semantic processing of module Sequences
    11	Semantic processing of module FiniteSets
    12	Semantic processing of module P4_VerifierStates_Broken
    13	Starting... (2026-07-05 10:24:43)
    14	Computing initial states...
    15	Computed 2 initial states...
    16	Computed 4 initial states...
    17	Computed 8 initial states...
    18	Computed 16 initial states...
    19	Error: Invariant StrictMeansEverything is violated by the initial state:
    20	/\ waived = {}
    21	/\ status = ( c1 :> "pass" @@
    22	  c2 :> "pass" @@
    23	  c3 :> "pass" @@
    24	  c4 :> "pass" @@
    25	  c5 :> "unperformable" )
    26	
    27	Finished in 00s at (2026-07-05 10:24:43)

===== FILE: P4_VerifierStates_Broken.tla =====
     1	------------------------- MODULE P4_VerifierStates_Broken -------------------------
     2	(***************************************************************************)
     3	(* Tessera Band 0 — P4, DELIBERATELY BROKEN: the classic fail-open bug.   *)
     4	(* An unperformable check is silently treated as if it passed ("we        *)
     5	(* couldn't reach the trust root, assume it's fine") — precisely the      *)
     6	(* promotion of UNVERIFIABLE toward VALID that P4 forbids and §4.6 calls  *)
     7	(* the place fail-open bugs hide.                                          *)
     8	(*                                                                         *)
     9	(* Expected: TLC REPORTS AN INVARIANT VIOLATION (NoSilentPromotion, or    *)
    10	(* StrictMeansEverything) with the concrete status/policy assignment as   *)
    11	(* the counterexample. A green run of this module would mean the          *)
    12	(* invariants are vacuous.                                                 *)
    13	(***************************************************************************)
    14	EXTENDS FiniteSets
    15	
    16	CONSTANTS Checks, NonWaivable
    17	
    18	ASSUME NonWaivable \subseteq Checks
    19	
    20	Waivable == Checks \ NonWaivable
    21	
    22	Statuses == {"pass", "fail", "unperformable"}
    23	
    24	Verdicts == {"VALID_STRICT", "VALID_DEGRADED", "INVALID", "UNVERIFIABLE"}
    25	
    26	VARIABLES status, waived
    27	
    28	Init ==
    29	  /\ status \in [Checks -> Statuses]
    30	  /\ waived \in SUBSET Waivable
    31	
    32	Next == UNCHANGED <<status, waived>>
    33	
    34	RequiredUnder(W) == Checks \ W
    35	
    36	(* BROKEN: no unperformable clause — a check that cannot be performed is  *)
    37	(* skipped, i.e. treated as pass. Fail-open.                               *)
    38	VerdictFor(W) ==
    39	  IF \E c \in RequiredUnder(W) : status[c] = "fail"
    40	    THEN "INVALID"
    41	  ELSE IF W = {}
    42	    THEN "VALID_STRICT"
    43	    ELSE "VALID_DEGRADED"
    44	
    45	Verdict == VerdictFor(waived)
    46	
    47	(* Same invariants as the correct module. *)
    48	Partition == Verdict \in Verdicts
    49	
    50	Monotonicity ==
    51	  (\E c \in NonWaivable : status[c] = "fail") =>
    52	    \A W \in SUBSET Waivable : VerdictFor(W) = "INVALID"
    53	
    54	NoSilentPromotion ==
    55	  (\E c \in NonWaivable : status[c] = "unperformable") =>
    56	    \A W \in SUBSET Waivable :
    57	      VerdictFor(W) \in {"INVALID", "UNVERIFIABLE"}
    58	
    59	ValidNeedsNonWaivablePass ==
    60	  (Verdict \in {"VALID_STRICT", "VALID_DEGRADED"}) =>
    61	    \A c \in NonWaivable : status[c] = "pass"
    62	
    63	StrictMeansEverything ==
    64	  Verdict = "VALID_STRICT" => \A c \in Checks : status[c] = "pass"
    65	
    66	DegradedNeedsExplicitWaiver ==
    67	  Verdict = "VALID_DEGRADED" => (waived # {} /\ waived \subseteq Waivable)
    68	
    69	UnverifiableIsHonest ==
    70	  Verdict = "UNVERIFIABLE" =>
    71	    /\ \E c \in RequiredUnder(waived) : status[c] = "unperformable"
    72	    /\ \A c \in RequiredUnder(waived) : status[c] # "fail"
    73	
    74	===================================================================================

===== FILE: P4_VerifierStates.cfg =====
     1	CONSTANTS
     2	  Checks = {c1, c2, c3, c4, c5}
     3	  NonWaivable = {c1, c2}
     4	
     5	INIT Init
     6	NEXT Next
     7	
     8	INVARIANTS
     9	  Partition
    10	  Monotonicity
    11	  NoSilentPromotion
    12	  ValidNeedsNonWaivablePass
    13	  StrictMeansEverything
    14	  DegradedNeedsExplicitWaiver
    15	  UnverifiableIsHonest
    16	  ExactInvalid
    17	  ExactUnverifiable
    18	  ExactStrict
    19	  ExactDegraded

===== FILE: P4_VerifierStates.out =====
1:TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)
13:Starting... (2026-07-05 10:24:41)
25:Finished computing initial states: 1944 distinct states generated at 2026-07-05 10:24:42.
26:Model checking completed. No error has been found.
28:  because two distinct states had the same fingerprint:
30:3888 states generated, 1944 distinct states found, 0 states left on queue.
33:Finished in 00s at (2026-07-05 10:24:42)
----- final 40 lines -----
     1	TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)
     2	Warning: Please run the Java VM which executes TLC with a throughput optimized garbage collector by passing the "-XX:+UseParallelGC" property.
     3	(Use the -nowarning option to disable this warning.)
     4	Running breadth-first search Model-Checking with fp 60 and seed -4660530406594817087 with 1 worker on 128 cores with 30688MB heap and 64MB offheap memory [pid: 1577773] (Linux 6.18.33.2-microsoft-standard-WSL2 amd64, Ubuntu 11.0.31 x86_64, MSBDiskFPSet, DiskStateQueue).
     5	Parsing file /home/tony/projects/tessera/formal/tla/P4_VerifierStates.tla
     6	Parsing file /tmp/FiniteSets.tla
     7	Parsing file /tmp/Naturals.tla
     8	Parsing file /tmp/Sequences.tla
     9	Semantic processing of module Naturals
    10	Semantic processing of module Sequences
    11	Semantic processing of module FiniteSets
    12	Semantic processing of module P4_VerifierStates
    13	Starting... (2026-07-05 10:24:41)
    14	Computing initial states...
    15	Computed 2 initial states...
    16	Computed 4 initial states...
    17	Computed 8 initial states...
    18	Computed 16 initial states...
    19	Computed 32 initial states...
    20	Computed 64 initial states...
    21	Computed 128 initial states...
    22	Computed 256 initial states...
    23	Computed 512 initial states...
    24	Computed 1024 initial states...
    25	Finished computing initial states: 1944 distinct states generated at 2026-07-05 10:24:42.
    26	Model checking completed. No error has been found.
    27	  Estimates of the probability that TLC did not check all reachable states
    28	  because two distinct states had the same fingerprint:
    29	  calculated (optimistic):  val = 2.0E-13
    30	3888 states generated, 1944 distinct states found, 0 states left on queue.
    31	The depth of the complete state graph search is 1.
    32	The average outdegree of the complete state graph is 0 (minimum is 0, the maximum 0 and the 95th percentile is 0).
    33	Finished in 00s at (2026-07-05 10:24:42)

===== FILE: P4_VerifierStates_Sanity.cfg =====
     1	\* Vacuity check: run with `tlc2.TLC -continue`. TLC VIOLATING all four
     2	\* invariants is the healthy result — each violation exhibits a reachable
     3	\* state with that verdict, proving the main cfg's implication-shaped
     4	\* invariants are not vacuously true.
     5	CONSTANTS
     6	  Checks = {c1, c2, c3, c4, c5}
     7	  NonWaivable = {c1, c2}
     8	
     9	INIT Init
    10	NEXT Next
    11	
    12	INVARIANTS
    13	  VerdictNeverStrict
    14	  VerdictNeverDegraded
    15	  VerdictNeverInvalid
    16	  VerdictNeverUnverifiable

===== FILE: P4_VerifierStates_Sanity.out =====
1:TLC2 Version 2.19 of 08 August 2024 (rev: 5a47802)
13:Starting... (2026-07-05 10:24:44)
15:Error: Invariant VerdictNeverStrict is violated by the initial state:
19:Error: Invariant VerdictNeverDegraded is violated by the initial state:
24:Error: Invariant VerdictNeverDegraded is violated by the initial state:
28:Error: Invariant VerdictNeverDegraded is violated by the initial state:
33:Error: Invariant VerdictNeverDegraded is violated by the initial state:
37:Error: Invariant VerdictNeverDegraded is violated by the initial state:
41:Error: Invariant VerdictNeverDegraded is violated by the initial state:
45:Error: Invariant VerdictNeverDegraded is violated by the initial state:
50:Error: Invariant VerdictNeverInvalid is violated by the initial state:
54:Error: Invariant VerdictNeverInvalid is violated by the initial state:
58:Error: Invariant VerdictNeverInvalid is violated by the initial state:
62:Error: Invariant VerdictNeverDegraded is violated by the initial state:
66:Error: Invariant VerdictNeverInvalid is violated by the initial state:
70:Error: Invariant VerdictNeverDegraded is violated by the initial state:
74:Error: Invariant VerdictNeverDegraded is violated by the initial state:
78:Error: Invariant VerdictNeverDegraded is violated by the initial state:
83:Error: Invariant VerdictNeverUnverifiable is violated by the initial state:
91:Error: Invariant VerdictNeverUnverifiable is violated by the initial state:
99:Error: Invariant VerdictNeverUnverifiable is violated by the initial state:
107:Error: Invariant VerdictNeverDegraded is violated by the initial state:
115:Error: Invariant VerdictNeverUnverifiable is violated by the initial state:
123:Error: Invariant VerdictNeverDegraded is violated by the initial state:
131:Error: Invariant VerdictNeverDegraded is violated by the initial state:
139:Error: Invariant VerdictNeverDegraded is violated by the initial state:
147:Error: Invariant VerdictNeverInvalid is violated by the initial state:
151:Error: Invariant VerdictNeverInvalid is violated by the initial state:
155:Error: Invariant VerdictNeverDegraded is violated by the initial state:
159:Error: Invariant VerdictNeverInvalid is violated by the initial state:
163:Error: Invariant VerdictNeverDegraded is violated by the initial state:
167:Error: Invariant VerdictNeverInvalid is violated by the initial state:
171:Error: Invariant VerdictNeverDegraded is violated by the initial state:
175:Error: Invariant VerdictNeverDegraded is violated by the initial state:
180:Error: Invariant VerdictNeverInvalid is violated by the initial state:
184:Error: Invariant VerdictNeverInvalid is violated by the initial state:
188:Error: Invariant VerdictNeverInvalid is violated by the initial state:
192:Error: Invariant VerdictNeverInvalid is violated by the initial state:
196:Error: Invariant VerdictNeverInvalid is violated by the initial state:
200:Error: Invariant VerdictNeverInvalid is violated by the initial state:
204:Error: Invariant VerdictNeverDegraded is violated by the initial state:
208:Error: Invariant VerdictNeverDegraded is violated by the initial state:
212:Error: Invariant VerdictNeverInvalid is violated by the initial state:
220:Error: Invariant VerdictNeverInvalid is violated by the initial state:
228:Error: Invariant VerdictNeverUnverifiable is violated by the initial state:
236:Error: Invariant VerdictNeverInvalid is violated by the initial state:
244:Error: Invariant VerdictNeverUnverifiable is violated by the initial state:
252:Error: Invariant VerdictNeverInvalid is violated by the initial state:
260:Error: Invariant VerdictNeverDegraded is violated by the initial state:
268:Error: Invariant VerdictNeverDegraded is violated by the initial state:
276:Error: Invariant VerdictNeverUnverifiable is violated by the initial state:
284:Error: Invariant VerdictNeverUnverifiable is violated by the initial state:
292:Error: Invariant VerdictNeverDegraded is violated by the initial state:
300:Error: Invariant VerdictNeverUnverifiable is violated by the initial state:
308:Error: Invariant VerdictNeverDegraded is violated by the initial state:
316:Error: Invariant VerdictNeverUnverifiable is violated by the initial state:
324:Error: Invariant VerdictNeverDegraded is violated by the initial state:
332:Error: Invariant VerdictNeverDegraded is violated by the initial state:
340:Error: Invariant VerdictNeverInvalid is violated by the initial state:
348:Error: Invariant VerdictNeverInvalid is violated by the initial state:
----- final 40 lines -----
     1	/\ waived = {c3, c4}
     2	/\ status = ( c1 :> "unperformable" @@
     3	  c2 :> "unperformable" @@
     4	  c3 :> "unperformable" @@
     5	  c4 :> "unperformable" @@
     6	  c5 :> "unperformable" )
     7	
     8	Error: Invariant VerdictNeverUnverifiable is violated by the initial state:
     9	/\ waived = {c3, c5}
    10	/\ status = ( c1 :> "unperformable" @@
    11	  c2 :> "unperformable" @@
    12	  c3 :> "unperformable" @@
    13	  c4 :> "unperformable" @@
    14	  c5 :> "unperformable" )
    15	
    16	Error: Invariant VerdictNeverUnverifiable is violated by the initial state:
    17	/\ waived = {c4, c5}
    18	/\ status = ( c1 :> "unperformable" @@
    19	  c2 :> "unperformable" @@
    20	  c3 :> "unperformable" @@
    21	  c4 :> "unperformable" @@
    22	  c5 :> "unperformable" )
    23	
    24	Error: Invariant VerdictNeverUnverifiable is violated by the initial state:
    25	/\ waived = {c3, c4, c5}
    26	/\ status = ( c1 :> "unperformable" @@
    27	  c2 :> "unperformable" @@
    28	  c3 :> "unperformable" @@
    29	  c4 :> "unperformable" @@
    30	  c5 :> "unperformable" )
    31	
    32	Finished computing initial states: 1944 distinct states generated at 2026-07-05 10:24:44.
    33	Model checking completed. No error has been found.
    34	  Estimates of the probability that TLC did not check all reachable states
    35	  because two distinct states had the same fingerprint:
    36	  calculated (optimistic):  val = 2.0E-13
    37	3888 states generated, 1944 distinct states found, 0 states left on queue.
    38	The depth of the complete state graph search is 1.
    39	The average outdegree of the complete state graph is 0 (minimum is 0, the maximum 0 and the 95th percentile is 0).
    40	Finished in 00s at (2026-07-05 10:24:44)

===== FILE: P4_VerifierStates.tla =====
     1	---------------------------- MODULE P4_VerifierStates ----------------------------
     2	(***************************************************************************)
     3	(* Tessera Band 0 — P4: fail-closed verifier state logic.                 *)
     4	(* Authoritative property statements: Amendment 1 §A1.2 (P4) and §A1.2.1  *)
     5	(* (the waiver lattice). This module is the machine-checkable form.       *)
     6	(*                                                                         *)
     7	(* The verifier's verdict over a bundle is a pure function (P9) of the     *)
     8	(* per-check outcomes and the verifier's declared policy. TLC exhaustively *)
     9	(* enumerates every combination of check outcomes and every policy, and   *)
    10	(* checks the A1.2/A1.2.1 invariants over all of them. There is no        *)
    11	(* temporal behavior here — evaluation is instantaneous — so the "state   *)
    12	(* machine" is degenerate: all the content is in the Init enumeration and *)
    13	(* the invariants.                                                         *)
    14	(*                                                                         *)
    15	(* Reading guide (Tony): Checks is an abstract set of the verifier's      *)
    16	(* individual checks (signature-verifies, manifest-evidence-validates,    *)
    17	(* temporal-consistency, ...). NonWaivable \subseteq Checks per A1.2.1.   *)
    18	(* `status` assigns each check pass/fail/unperformable; `waived` is the   *)
    19	(* verifier's declared policy (the waived subset; {} = strict). The       *)
    20	(* companion P4_VerifierStates_Broken module implements the classic       *)
    21	(* fail-open bug and TLC produces the violating assignment.               *)
    22	(***************************************************************************)
    23	EXTENDS FiniteSets
    24	
    25	CONSTANTS Checks, NonWaivable
    26	
    27	ASSUME NonWaivable \subseteq Checks
    28	
    29	Waivable == Checks \ NonWaivable
    30	
    31	Statuses == {"pass", "fail", "unperformable"}
    32	
    33	Verdicts == {"VALID_STRICT", "VALID_DEGRADED", "INVALID", "UNVERIFIABLE"}
    34	
    35	VARIABLES status, waived
    36	
    37	(* Every combination of check outcomes and every legal policy. A1.2.1:   *)
    38	(* only Waivable checks may appear in a waiver set — a policy naming a    *)
    39	(* non-waivable check is not a legal policy at all.                       *)
    40	Init ==
    41	  /\ status \in [Checks -> Statuses]
    42	  /\ waived \in SUBSET Waivable
    43	
    44	Next == UNCHANGED <<status, waived>>
    45	
    46	(***************************************************************************)
    47	(* The verdict function, parameterized by the waiver set W so that the    *)
    48	(* monotonicity invariant can quantify over ALL policies for one status   *)
    49	(* assignment. Precedence decision (surfaced by this model, for author    *)
    50	(* ratification): when one required check FAILS and another is            *)
    51	(* UNPERFORMABLE, the verdict is INVALID — a definitive failure is        *)
    52	(* stronger evidence than an open question, and both are fail-closed.     *)
    53	(***************************************************************************)
    54	RequiredUnder(W) == Checks \ W
    55	
    56	VerdictFor(W) ==
    57	  IF \E c \in RequiredUnder(W) : status[c] = "fail"
    58	    THEN "INVALID"
    59	  ELSE IF \E c \in RequiredUnder(W) : status[c] = "unperformable"
    60	    THEN "UNVERIFIABLE"
    61	  ELSE IF W = {}
    62	    THEN "VALID_STRICT"
    63	    ELSE "VALID_DEGRADED"
    64	
    65	Verdict == VerdictFor(waived)
    66	
    67	(***************************************************************************)
    68	(* Invariants — each maps to a clause of A1.2 P4 / A1.2.1.                *)
    69	(***************************************************************************)
    70	
    71	(* P4: the four states partition all outcomes (totality; never a bare     *)
    72	(* boolean, never a fifth state).                                          *)
    73	Partition == Verdict \in Verdicts
    74	
    75	(* A1.2.1 monotonicity: a failed non-waivable check is INVALID under      *)
    76	(* EVERY policy — no waiver set may promote it.                            *)
    77	Monotonicity ==
    78	  (\E c \in NonWaivable : status[c] = "fail") =>
    79	    \A W \in SUBSET Waivable : VerdictFor(W) = "INVALID"
    80	
    81	(* A1.2.1: an unperformable non-waivable check never yields any VALID     *)
    82	(* state, under any policy. (INVALID is permitted: some other required    *)
    83	(* check may have definitively failed.)                                    *)
    84	NoSilentPromotion ==
    85	  (\E c \in NonWaivable : status[c] = "unperformable") =>
    86	    \A W \in SUBSET Waivable :
    87	      VerdictFor(W) \in {"INVALID", "UNVERIFIABLE"}
    88	
    89	(* P1-facing corollary: any VALID verdict means every non-waivable check  *)
    90	(* was performed and passed.                                               *)
    91	ValidNeedsNonWaivablePass ==
    92	  (Verdict \in {"VALID_STRICT", "VALID_DEGRADED"}) =>
    93	    \A c \in NonWaivable : status[c] = "pass"
    94	
    95	(* P4/§3.1: VALID_STRICT is the fail-closed default — every check, not    *)
    96	(* just the required ones, performed and passed.                           *)
    97	StrictMeansEverything ==
    98	  Verdict = "VALID_STRICT" => \A c \in Checks : status[c] = "pass"
    99	
   100	(* A1.2.1: VALID_DEGRADED only arises from an explicit, nonempty waiver   *)
   101	(* within the waivable set — never as a default.                           *)
   102	DegradedNeedsExplicitWaiver ==
   103	  Verdict = "VALID_DEGRADED" => (waived # {} /\ waived \subseteq Waivable)
   104	
   105	(* UNVERIFIABLE is honest: it arises only when some required check truly  *)
   106	(* could not be performed (and none failed).                               *)
   107	UnverifiableIsHonest ==
   108	  Verdict = "UNVERIFIABLE" =>
   109	    /\ \E c \in RequiredUnder(waived) : status[c] = "unperformable"
   110	    /\ \A c \in RequiredUnder(waived) : status[c] # "fail"
   111	
   112	(***************************************************************************)
   113	(* Exact classification (iff, not just one-way safety). The one-way       *)
   114	(* implications above would all pass under an over-conservative verdict   *)
   115	(* function (e.g. everything INVALID); these pin the classification in    *)
   116	(* both directions, so a future edit to VerdictFor cannot silently drift  *)
   117	(* toward misclassification in either the permissive or the conservative  *)
   118	(* direction. Together the four right-hand sides partition all outcomes.  *)
   119	(***************************************************************************)
   120	AnyRequiredFail == \E c \in RequiredUnder(waived) : status[c] = "fail"
   121	AnyRequiredUnperf == \E c \in RequiredUnder(waived) : status[c] = "unperformable"
   122	AllRequiredPass == \A c \in RequiredUnder(waived) : status[c] = "pass"
   123	
   124	ExactInvalid ==
   125	  (Verdict = "INVALID") <=> AnyRequiredFail
   126	
   127	ExactUnverifiable ==
   128	  (Verdict = "UNVERIFIABLE") <=> (~AnyRequiredFail /\ AnyRequiredUnperf)
   129	
   130	ExactStrict ==
   131	  (Verdict = "VALID_STRICT") <=>
   132	    (waived = {} /\ \A c \in Checks : status[c] = "pass")
   133	
   134	ExactDegraded ==
   135	  (Verdict = "VALID_DEGRADED") <=> (waived # {} /\ AllRequiredPass)
   136	
   137	(***************************************************************************)
   138	(* Vacuity checks — used ONLY by the _Sanity cfg (run with TLC -continue), *)
   139	(* where TLC VIOLATING all four is the healthy result: each verdict is    *)
   140	(* reachable under the correct verdict function, so the implication-      *)
   141	(* shaped invariants above are not vacuously true. If VerdictFor had a    *)
   142	(* bug making any verdict unsatisfiable, its invariants would pass        *)
   143	(* vacuously — these witnesses close that hole.                            *)
   144	(***************************************************************************)
   145	VerdictNeverStrict       == Verdict # "VALID_STRICT"
   146	VerdictNeverDegraded     == Verdict # "VALID_DEGRADED"
   147	VerdictNeverInvalid      == Verdict # "INVALID"
   148	VerdictNeverUnverifiable == Verdict # "UNVERIFIABLE"
   149	
   150	===================================================================================

===== FILE: REGISTERED-P4.txt =====
     1	## A1.2 The pre-registered properties (the theorem statements)
     2	
     3	These are the properties the Band 0 work must establish, stated in prose
     4	*before* any modeling begins, so that "the proof holds" has a fixed
     5	referent. Each names how it is discharged: **[model]** — proven in the
     6	machine-checked model under idealized primitives (Layer 1); **[proof]** —
     7	proven directly (not a state-machine claim); **[assumption]** — cited as an
     8	explicit Layer 2 assumption, not proven. Restating a property here in
     9	sharper form does not weaken the original's hard invariants; where an
    10	invariant (§4.3, §4.6) and a property overlap, the property is the
    11	checkable form of the invariant.
    12	
    13	- **P4 — Fail-closed state logic.** The verifier's four states partition
    14	  all outcomes. A required check that fails yields `INVALID`. A check that
    15	  cannot be performed yields `UNVERIFIABLE` — never any `VALID` state,
    16	  under any trace. `VALID_DEGRADED` arises only from an explicit, recorded
    17	  policy within A1.2.1's waivable set, never as a default or a fallback.
    18	  (The checkable form of §4.6.) **[model]**
    19	
    20	### A1.2.1 Degraded-policy semantics (the waiver lattice)
    21	
    22	`VALID_DEGRADED` exists so long-horizon verification does not collapse to
    23	a boolean — not as a universal escape hatch. Its scope is fixed here:
    24	
    25	**Non-waivable checks.** No verifier policy may waive: canonical-byte
    26	integrity (P1, P8); type/domain separation (P7); boundary framing (P8);
    27	key-to-issuer binding for every accepted signature (P3); temporal-anchor
    28	consistency (P5). A package failing any non-waivable check is `INVALID`
    29	under **every** policy — no degraded policy may promote it
    30	(*monotonicity*). A non-waivable check that *cannot be performed* yields
    31	`UNVERIFIABLE`, never any `VALID` state — the P4 partition applies inside
    32	the lattice: performed-and-failed → `INVALID`; unperformable →
    33	`UNVERIFIABLE`; neither is promotable.
    34	
    35	**Waivable checks (declared redundancy only).** Degraded policies may
    36	weaken only declared redundancy requirements: accepting a subset of the
    37	issue-time signature set (P2); accepting fewer than all external
    38	manifest-authority evidences (P10); accepting a signature whose trust root
    39	is no longer independently recoverable, where the remaining checks pass.
    40	
    41	**Recording.** Every `VALID_DEGRADED` verdict records the precise waived
    42	check set and the policy that authorized the waiver — the informed-consent
    43	act of §3.1, made auditable.
    44	
    45	---
    46	
