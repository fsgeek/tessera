Reviewed all 53 specifications and INDEX at checkout `57f45c6`, including the untracked extraction. No files changed.

The intended V1 verdicts and reason codes are sound under the stated constructions, subject to the ambiguous alternatives below. TMP-10 correctly follows V1’s `VALID_STRICT / OK` despite P6’s rejection; E6A-07 correctly follows `UNVERIFIABLE / MEMBER_MISSING:a_sig` despite the model’s INVALID. Both disagreements are disclosed. No service-key-listing or revocation check should be added.

**E10R-01 — HIGH — This does not yet complete A1.7’s extraction/concretizer obligation.**

[E10-SPEC.md:45](/home/tony/projects/tessera/formal/e10/E10-SPEC.md:45) supplies specifications containing prose operations, symbolic expressions and hooks. It supplies neither a concretizer nor concrete outputs for the new cases. A1.7 requires mechanical extraction into concrete fixtures and independent review of that translation ([A1:536](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-1.md:536)).

**Fix:** supply a reproducible materializer, concrete fixture references/outputs and executable sequence definitions, then review and spot-audit those outputs. This review can accept the scenario design conditionally; it cannot certify a concretizer that is absent. The later AWS execution remains a separate obligation.

**E10R-02 — MEDIUM — Some “covered” references need separate expectations or narrower classifications.**

- [E6A-01:36](/home/tony/projects/tessera/formal/e10/vectors/E10-E6A-01.json:36) permits HY-b2-H **or HY-e1-C**, but supplies only `UNVERIFIABLE / ALG_UNKNOWN`. HY-e1-C requires `INVALID / RECEIPT_COMMON_MISMATCH`. The prose acknowledges this; the executable expectation and INDEX do not distinguish it.
- [P4-03:42](/home/tony/projects/tessera/formal/e10/vectors/E10-P4-03.json:42) includes L-06s, whose strict-request result is `VALID_STRICT / OK`, under the degraded-request expectation.
- TMP-04’s UTC-03 reference matches the nonmonotonic scenario, but its T is `14:00Z`, versus this vector’s `12:20Z`.

**Fix:** represent alternatives and controls as explicit subcases with their own requests and reports; distinguish exact coverage from analogous coverage.

The **14 covered / 39 new** count remains defensible: every covered vector has at least one matching existing case. These secondary references do not all represent identical cases.

**E10R-03 — MEDIUM — Several specifications lack a complete, deterministic report oracle.**

Eleven ordinary verifier expectations omit T. [SP1-01:54](/home/tony/projects/tessera/formal/e10/vectors/E10-SP1-01.json:54) instead gives the prose string `"null if not re-stamped"`; other vectors allow optional restamping without separate expected reports. V1 makes T part of the stable six, including for INVALID results ([profile:294](/home/tony/projects/tessera/docs/V1-PROFILE.md:294)).

**Fix:** give every executable subcase all six stable fields. Split restamped and unstamped variants, or specify an independently checkable derivation from the fixed fixture. Specify the required A10 UTC-assessment output separately.

**E10R-04 — HIGH — The four issuer cases need defined staging sequences and observations before they are exercisable as claimed.**

The proposed controls are plausible, but the current descriptions are insufficient:

| Vector | Remaining execution gap | Fix |
|---|---|---|
| [ISS-01:41](/home/tony/projects/tessera/formal/e10/vectors/E10-ISS-01.json:41) | The TEST issuer’s exception demonstrates c2 refusal, but cannot demonstrate discard or counting against N. The bridge invariant establishes only non-shipping. | Observe the attempt identity, discard transition and counter increment in the actual issuer. |
| [ISS-02:33](/home/tony/projects/tessera/formal/e10/vectors/E10-ISS-02.json:33) | The recipe supplies header times but does not implement its chosen wall-clock state. `ships:false` could pass because of an unrelated lifecycle expiry. | Drive and record the clock, confirmed proof and ship-decision point; include a successful control. |
| [ISS-03:25](/home/tony/projects/tessera/formal/e10/vectors/E10-ISS-03.json:25) | Removing a supplied header tests evidence completeness, not the live sequence before confirmation. Public polling can miss a premature shipment. | Hold the simulated chain at each confirmation count, observe responses, then release the sixth confirmation. State explicitly that model depth 5 means six confirmations. |
| [ISS-04:32](/home/tony/projects/tessera/formal/e10/vectors/E10-ISS-04.json:32) | No executable TEST recipe; an ongoing outage does not distinguish a latched refusal from a stalled issuer. | Observe three expiries and terminal refusal, restore availability/deliver late evidence, and verify that the refused request cannot ship. |

**Fix:** define these controls and observations, and retain their “requires staging harness” status until available. None is fully established through the public API alone.

**E10R-05 — MEDIUM — SP3-01’s L0 requirement contradicts its construction.**

[SP3-01:48](/home/tony/projects/tessera/formal/e10/vectors/E10-SP3-01.json:48) labels the case L0 but requests a TEST-signed other document. That material will not normally match a production receipt’s manifest key.

**Fix:** use the same receipt’s `S_kms` as `possession.kms`. It is already a service-key signature over another document, requires only a post-issue edit, and produces `INVALID / POSSESSION_INVALID`. I verified that construction in memory.

**E10R-06 — LOW — Repair source locators and distinguish formulas from run evidence.**

[SP2-04:18](/home/tony/projects/tessera/formal/e10/vectors/E10-SP2-04.json:18) combines two filenames into one nonexistent literal path. Both underlying files exist and the cited queries support the scenario. Several other entries omit line locators or cite a formula where they claim a reachable witness; for example, POS-01 should cite `runs/sanity/NeverInStrict_V1.out:44` for the E6a witness. E10-SPEC’s A1 concretizer citation should point to lines 550–554, rather than 555–559.

**Fix:** use one source object per file, explicit line ranges, and separate property-definition and execution-evidence references.

The registered-case mapping otherwise holds: late burial, missing headers, all three P9 components, and A3.9 are represented. **P7 is correctly deferred by A9 row 26**; P7-01/02 are optional V1 analogues, not discharge of A6.1. P7-04 separately exercises the retained type-separation obligation.

Validation included checking the cited artifacts and archived TLC results, running all **24 distinct referenced conformance cases** through the independent verifier with agreement on all six stable fields, and materializing representative new mutations in memory. The temporal cases, signature/stripping cases and P7 reserialization example agreed with their stated outcomes. I did not rerun TLC or exercise a live AWS issuer.

**VERDICT: ACCEPTABLE AFTER (E10R-01 through E10R-06).**


