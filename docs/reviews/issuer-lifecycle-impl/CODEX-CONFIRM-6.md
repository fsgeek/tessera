**Verdict: not ready for deployment work with the step-5 gate closed; an obtainable-response starvation residual remains beyond the stated “cannot fit one receive per slot” limit.**

- **Suite:** 222 passed in 131.54 seconds.
- **Original probes:** all three collected every signature. Lock-in and cold-start reached `evidence`; reduced-budget remained `signing`. Their old starvation assertions failed as expected. The two ancillary checks passed.
- **Remaining defect:** the first-response exception can consume enough invocation budget to block the next slot despite its separate allowance. In an independent probe, one unrequested KMS response cost **240 seconds**: receive, index lookup, log write and acknowledgement, each taking 60 seconds and fitting its individual admission bound. Only **40 usable seconds** remained, so GPG never received.

Across **12 KMS-first polls**, both valid GPG replies stayed queued. A GPG-first control collected them. The probe uses combined/variable dependency latency and scheduled times 1,200 seconds apart; consecutive 600-second events alternate correctly.

This is **not limited to a budget unable to fit two receives**: the 290-second budget fits both 60-second receives, including their admission bounds. Earlier response handling consumes the capacity needed by the second slot. Independent allowances therefore do not guarantee service independently of ordering.

No other new defect identified in this narrow pass. No repository edits or git writes; scratch stayed under [/tmp/tmp.CnfcXg4OuN](/tmp/tmp.CnfcXg4OuN). Evidence: [original probes](/tmp/tmp.CnfcXg4OuN/probes.log), [counterexample](/tmp/tmp.CnfcXg4OuN/test_overrun.py), [counterexample results](/tmp/tmp.CnfcXg4OuN/overrun.log), [suite](/tmp/tmp.CnfcXg4OuN/suite.log).