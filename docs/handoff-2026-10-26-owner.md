# Owner handoff, 2026-10-26 (updated at the planned instance switch) (Claude Opus 5.5, session tessera-47 / tessera-a3, unnamed)

For the next owner instance. Read this, then `recall()` in qhaway. The repository and the memory store are the record;
where this note disagrees with them, they win.

## Where V1 stands

- **Phase 1a is open.** The author signed the opening commit `52ee179` (2026-10-24) on
  `formal/freeze-v1/FREEZE-RECORD.md`. The freeze was assembled from `270ca49`. E9 is complete: every row has the
  author's decision (`docs/reviews/e9-packet/AUTHOR-RULINGS.md`), and **row 2 CUT the service-key listing** (the
  author's own narrowing). Reviewer reservations on rows 6, 10, 18 and 21 stand.
- **Frozen text is not edited.** Readings of frozen text that Phase 1a needs go into `docs/V1-CLARIFICATIONS.md`.
  They may narrow, never widen.
- **The contracts:**
  - `docs/V1-CONTRACT.md`: what a receipt establishes. §5 holds mappings, not pairs.
  - `docs/V1-SERVICE-CONTRACT.md`: the outside view. Ids S1–S8, AJ1–AJ7, L1–L3, F1–F12, binding since the tupay
    handoff.
  - `docs/V1-SERVICE-RESOLUTIONS.md`: Tessera's answers to the Undecided items, stamped at `2411714` before any
    Phase 1a code.
- **Five AUTHOR items** are in the resolutions (S7 cost, AJ2 publication length, AJ5 exit, AJ6 download length,
  AJ7 capture notice). Each has an owner recommendation. They need the author's word before 4 Dec.

## Phase 1a progress (dates: E10 by 13 Nov, the rest by 20 Nov)

| Item | State |
|---|---|
| Service verifier | Done in `service/verifier/`: 352/352 conformance agree, 135 tests. Production by default; never imports `prototype/`. Missing SHA-1DC is a startup refusal. Release assembler and production key still to do. |
| Release-format vectors | Done in `service/release-vectors/`: 9 cases. Ubuntu and upstream gpgv 2.4.4 both match. CL-01 and CL-02. |
| E10 | 53 vectors in `formal/e10/` (39 new). Codex: ACCEPTABLE AFTER E10R-01..06, being applied (`docs/reviews/e10/`). |
| Issuer API | **Built locally** in `service/issuer/` (design: `DESIGN.md`, including "Changes after review"). 98 tests pass; end-to-end on stand-ins gives VALID_STRICT through `service/verifier`. Codex review IS-01..11 fixed, each with a regression test. Receipts are served by per-request 5-minute pre-signed links. A Codex confirmation review (`docs/reviews/issuer/CODEX-CONFIRM.md`) found CF-01..05. All are fixed, with regression tests (108 tests pass). Its verdict was "ready for deployment work after CF-01..05"; a fresh confirmation pass on the CF fixes is a sensible first step for the next owner. **Before deployment:** install Terraform (the validate test is skipped); package the Lambda with the SHA-1DC binary and `install.json`; both real signers (slot-2 on GCP, and the KMS-slot signer) must adopt `sign_by` and `frame_ref` (IS-03, IS-09), or content is limited to about 145 KB against the stamped 1 MiB. |
| Signer split | **Open author question.** The owner corrected his own claim: separating where signers run does NOT stop a captured issuer from obtaining signatures (signers sign what the issuer sends). It buys policy the captor can't override and logs it can't erase. Recommendation: KMS key in a separate AWS signing account, with a small policy signer and an append-only log; slot 2 unchanged; no Azure or Linode in V1. Awaiting the author. The key-policy read needs `aws login --profile tessera`; sessions expire within hours. |
| P9 code inspection, missing-capture control, P3 assumption half, bounded local refusal, H3 | Not started. The issuer and verifier now exist, so these can begin. E10 vectors against AWS follow deployment. |
| E10 | Done: 53 vectors, 69 fixtures; the service verifier agrees on 69/69 (`formal/e10/`, `docs/reviews/e10/`). |

## Cross-project

- **tupay T1** builds from the service contract (client slice: S1–S8, L1–L3, F1–F12), with Grok on the
  implementation side and Claude on the model side. **EMBARGO:** send tupay nothing about Phase 1a or real-issuance
  findings until its steward says both T1 sides committed first versions. Correspondence is in `docs/requests/`.
- **khipumaq** depends on the shared ArangoDB at 192.168.111.127. When that host runs out of memory, `codex exec`
  hangs at MCP startup. Workaround for one run: `-c 'mcp_servers.khipumaq.enabled=false'`.

## Working lessons from this instance (also in qhaway)

- Before citing a registered rule as authority, check its trigger. The listing "cut" cited a cut order that applies
  only on a slip; the exit had not slipped.
- Every plain-language page has overclaimed under capture of both channels: four times, including the preamble draft.
  Run the capture-row check before any review.
- Verify that a check actually ran against the thing you think it did. A dry run "against the freeze" silently used a
  TEST freeze once; the driver now refuses that.
- A security claim needs the requester, not only the key location. The signer-split overclaim came from reasoning
  about where keys live, not about who can ask for a signature.
- Give Tony explicit `git add` paths, with `cd` and a leading `!`. His shell may be in another project's directory.
- Build V1 that works, with its limits stated. Not V12.
