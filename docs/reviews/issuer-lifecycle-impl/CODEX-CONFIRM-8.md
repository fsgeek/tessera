**Not ready for deployment work with the step-5 gate closed: deterministic starvation remains when actual handling fits but per-call admission blocks completion.**

- **Suite:** [223 passed in 133.45 seconds](/tmp/tessera-confirm8.cl8D1KZ7/suite.log).
- **Prior counterexample fixed:** both first-slot choices now collect a signature. Earlier collection probes pass. The share-overrun probe needs its populated slot selected explicitly; that check also passes. [Results](/tmp/tessera-confirm8.cl8D1KZ7/verified.log).
- **Coherence:** [DESIGN.md:231](/home/tony/projects/tessera/service/issuer/DESIGN.md:231) does not explicitly distinguish actual latency from admission capacity. Interpreted as actual latency, its probability-1 claim is false. Interpreted as complete worst-case capacity, the condition is unmet by the AWS configuration.
- **New counterexample:** SQS **20 s**, DynamoDB **24 s**, S3 **47 s**. One receive plus complete handling takes **254 s**, or **278 s on redelivery**, both within **280 usable seconds**. Nevertheless, a guarded call encounters **70 s remaining against its 73 s admission requirement**. Across 12 polls for each first slot, no signature reaches the record; request servicing also cannot reconcile it. Larger-budget controls complete those same paths. [Probe](/tmp/tessera-confirm8.cl8D1KZ7/test_admission.py), [results](/tmp/tessera-confirm8.cl8D1KZ7/verified.log).

The required condition must include **every call’s admission headroom**, not merely total actual duration. Random selection cannot repair this failure. Also, `_handle_worst` omits the additional DynamoDB log write on redelivery of an already logged “used” signature.

No repository edits or git writes; all test scratch, caches and basetemp stayed under the fresh scratch directory.