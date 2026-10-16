Full adversarial review of docs/reviews/spec-sufficiency/RESOLUTIONS-DRAFT.md (repo /home/tony/projects/tessera). It proposes rules closing the gaps that your own spec-sufficiency probe found (GAPS.md, same directory). The owner decides each one before the 30 Oct V1 profile freeze.
Read: RESOLUTIONS-DRAFT.md in full, GAPS.md, docs/phase-0-prereg-amendment-9.md (governs), docs/V1-PROFILE.md, formal/p8/ENCODING-V1.md. You may read prototype/ to check claims about real artifacts.
For each resolution:
(1) Would an independent implementer now reach a unique verdict? Name any fork that remains.
(2) Does it allow a false accept, meaning VALID_STRICT on evidence an adversary in A9's model can produce? Construct the input if you can.
(3) Does it falsely reject honest receipts from the documented issue path?
(4) Is the change label honest? In particular, test that nothing labelled CLARIFY actually narrows the model, and check the agent's claim that no NARROW-MODEL is needed.
(5) Does it need an amendment, or change a signed byte or a P8 vector, despite the draft saying it doesn't?
Give special scrutiny to: G05 (ignoring uncovered OTS attestations); G02 (git assertion time <= declared issue time, plus the CORRECT); the trust-configuration signing-key finding; G16 (DNSSEC algorithms 8/13, DS type 2 only); G03 ("earliest" = lowest height).
Write findings with severity and an exact proposed fix to docs/reviews/spec-sufficiency/CODEX-REVIEW-RESOLUTIONS.md. Edit nothing else.
