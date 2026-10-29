**Verdict: ready for the author’s custody ruling and signature.** No blocking finding in the three edits.

- **A11I4-01 — PASS, c016.** [A11:279–288](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:279) accurately identifies the residual in the [lifecycle design:68–76](/home/tony/projects/tessera/docs/decisions/2026-10-29-issuance-lifecycle.md:68). It preserves A2.1/A2.3 as governing requirements and explicitly prevents A11’s signature from accepting that residual. This confirms the boundary, not the lifecycle design’s conformance.

- **A11I4-02 — PASS, deployment gate.** [c036:289–291](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:289) and [DEPLOY:39–45](/home/tony/projects/tessera/service/issuer/DEPLOY.md:39) correctly require the signed custody ruling before deployment. Both respect the ruling’s alternatives and [FREEZE-RECORD:62–64](/home/tony/projects/tessera/formal/freeze-v1/FREEZE-RECORD.md:62). DEPLOY requires rewriting all steps under Option 2; c036’s narrower list does not exempt the remaining steps.

- **A11I4-03 — PASS, operational triggers.** [Item 4:95–109](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:95) retains mandatory reruns, records and operator attestation. It explains each trigger’s purpose and labels the calendar interval as an operating guess with a review point. These are operational duties proposed for adoption, not registered results or guarantees of detection. No claim is widened, and no contradiction with A11’s bounded evidence or discharge conditions was found.

- **A11I4-04 — Additional change identified.** Comparing the complete A11 snapshot captured in `codex-confirm-row8.log` with the current file found only the three described edits **plus** [row 8:134](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:134): `:462-579` became `:462-611, all of A10.4.1`. This locator correction was already disclosed in [DISPOSITION:114](/home/tony/projects/tessera/docs/reviews/amendment-11/DISPOSITION.md:114). Nothing else changed.

Owner prechecks, applied to these edits:

| Check | Result | Evidence |
|---|---|---|
| Capture row | **PASS** | A11:95–109, 279–291 add no attacker-key rejection or capture-visibility promise; consistent with V1-CONTRACT:37, 52–53, 72. |
| Trigger clause | **PASS** | A11:183–218, 289–291 and DEPLOY:39–45 leave the ruling pending; neither option’s consequence is activated prematurely. |
| Requester | **PASS** | DEPLOY:41 incorporates ruling conditions (i)–(iv), including enqueue versus key-invocation authority and review of every principal able to cause signing (A11:191–202). |
| Binding text | **PASS** | A11:281–288 subordinates the owner design to registered A2 requirements; item 4 remains an explicitly proposed duty; DEPLOY:39–45 waits for signed authority. |

Review was read-only; scratch was confined to a fresh `mktemp -d`.

