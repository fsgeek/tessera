**Not ready for deployment work with the step-5 gate closed: deterministic starvation remains beyond the stated capacity limit.**

- **Suite:** 221 passed in 132.96 seconds.
- **Four original probes:** rerun unchanged; three hit removed interfaces, and the cold-start starvation assertion failed because signatures were collected. Scratch adaptations preserve their workloads and check collection: **6 passed**.
- **New counterexample:** 290-second budget, SQS calls taking 50 seconds, DynamoDB calls taking 30 seconds, valid replies queued on both slots. Across 12 polls for **each possible first slot**, no signature reached its job record. Both receives occur; handling then exhausts admission capacity, and request servicing cannot reconcile the stored signature. The same situation repeats.
- **Capacity control:** one receive plus complete handling **and acknowledgement succeeds in 250 seconds**, with identical dependencies and budget. Thus this falls outside exception (b), and randomness cannot fix it.

The cause is [pipeline.py:385](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:385): the next-receive guard reserves **one store operation**, not a message’s complete handling cost. Both receive orders produce the same failure, so this is deterministic starvation, not an unlucky sequence whose probability vanishes.

[DESIGN.md:225](/home/tony/projects/tessera/service/issuer/DESIGN.md:225) explicitly describes probability-1 selection and the capacity limit, but **understates the residual**: “starvation-free by construction” and “whatever the schedule” do not hold. No additional distinct defect identified in this narrow pass.

Evidence: [counterexample and control](/tmp/tmp.1c5WQ5xzIA/test_capacity.py), [results](/tmp/tmp.1c5WQ5xzIA/capacity.log), [adapted probes](/tmp/tmp.1c5WQ5xzIA/adapted.log), [suite](/tmp/tmp.1c5WQ5xzIA/suite.log).

No repository edits or git writes. I missed redirecting pytest fixture scratch: the suite also used `/tmp/pytest-of-tony`, outside the requested fresh scratch directory.