**Verdict: not ready for deployment work with the step-5 gate closed; a reduced-budget scheduling defect remains.**

Validation: **217 passed in 130.67 seconds**. No repository edits or git writes; scratch: [/tmp/tmp.6rbTsKov9q](/tmp/tmp.6rbTsKov9q).

**ILC-I4-01 — Medium: rotation can remain stuck when an empty first queue consumes the checkpoint budget.**

At [pipeline.py:392](/home/tony/projects/tessera/service/issuer/tessera_issue/pipeline.py:392), an empty batch leaves rotation unchanged. A later non-empty batch triggers the rotation write without reserving its cost.

Independent reproduction, using the real guarded adapters:

- Poll budget **190 seconds**, SQS calls **60 seconds**, KMS empty, two valid GPG responses queued.
- Two receives consume 120 seconds, leaving **60 seconds** after the reserve. The rotation write requires **73 seconds** admission and is refused. Request-position writes cannot rescue it under that budget.
- After **12 polls**, durable rotation remained zero, both GPG signatures were absent, and both replies remained queued.
- Forcing GPG to start under the **same budget** allowed both signatures to be recorded.

This demonstrates avoidable scheduling starvation with obtainable responses. The reproduction uses a reduced budget; the original 290-second scenario is repaired. Evidence: [probe](/tmp/tmp.6rbTsKov9q/test_rotation.py), [log](/tmp/tmp.6rbTsKov9q/rotation.log). Reserve the rotation checkpoint before spending receives, and ensure empty-queue turns advance fairly.

The other requested confirmations:

1. **Original cold-start probe: repaired.** GPG was served, all four signatures were recorded, and the request reached `evidence`. Its old starvation assertion failed as expected. [Log](/tmp/tmp.6rbTsKov9q/third.log).
2. **Write guarding: yes.** Rotation uses the same deadline-guarded `cursor_put` as other poller-position writes. Reads are strongly consistent; writes are unconditional, with infrastructure limiting the poller to one concurrent invocation. Budget refusal can nevertheless cause ILC-I4-01.
3. **DESIGN drain wording: accurate.** [Lines 224–226](/home/tony/projects/tessera/service/issuer/DESIGN.md:224) correctly describe cooperative allocation and possible overshoot. The rotation statement needs qualification or the repair above.
4. **No other new defect identified in this narrow pass.** Step 5 remains closed; diagnostic unavailability history authorizes no ending.