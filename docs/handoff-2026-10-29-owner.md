# Owner handoff, 2026-10-29 (Claude Opus 5.5, owner since 2026-10-27, unnamed)

Read this, then `recall()` in qhaway. The repository and the memory store are the record. Where this note disagrees
with them, they win.

## State

- **Amendment 11 is SIGNED** (`f01e086`, stamped). It is the consolidated consistency amendment:
  - the P3 verification profile: a registered floor of 223 owner tests plus 968 Wycheproof tests, pinned by
    `formal/p3-verification-profile/FLOOR-MANIFEST.sha256`, with discharge conditions (a)–(d) and an operational
    re-run duty whose triggers each say what they detect;
  - the dependency-sweep duty;
  - all 28 Levadura panel findings (obs-0185; `levadura_salvaje/docs/tessera-a11-canary-scorecard.md`);
  - the K-R enforcement wording;
  - registration of the E9 cut of A10.4.1;
  - slot-2 custody, Option 1 (an owner decision adopted by the author's signature): `service/signer-gcp/` runs
    under conditions (i)–(iv).
- **P3** stays `checked`. Discharge needs (c): the deployed zip's `CodeSha256` matched for both issuer functions
  (`service/issuer/DEPLOY.md` step 10).
- **Owner repairs from A11 §A11.7.** c093, c136 and the deploy gate (c036) are done (`8793966`). **c016 is open**:
  the issuer lifecycle.

## The long pole: the issuance lifecycle (c016) — updated 2026-10-30

- **Design.** `docs/decisions/2026-10-29-issuance-lifecycle.md` is at revision 5.3.1. It has had four Codex
  confirmations (`docs/reviews/issuance-lifecycle/`) and model runs R4 to R53 (`formal/tla/issuer-lifecycle/`,
  RESULTS.md §1–8):
  - expiry only on complete negative evidence;
  - a fence write before each fetch, and version guards on every write;
  - a rolling window over completed intervals, with an allowance ≥ 1;
  - an explicit "Implementation boundary": the `EVIDENCE_UNAVAILABLE` ending is **gated** until the author decides
    by amendment.
- **Author decision pending** (design step 5). Under sustained evidence loss, A2.1's shipping obligation and A2.3's
  termination obligation cannot both hold for the protected timely-eligible cases (paths a and b). It is framed per
  ILC4-03:
  - A2.1's permission is a *lag* test;
  - B is ambiguous between A2's prose (service observation) and A2's model (`burialAtWall`).

  It can be batched into one later V1 implementation amendment.
- **Implementation** (uncommitted, `service/issuer/`): the ungated core is built and passes 158 tests. The L1 margin
  is now 216 h, derived from δ + S + 24 h, in `window.py`. The prose is updated: S4, L1, CL-03 items 1–2, the
  clock-tolerance decision.
- **Codex implementation review** (`docs/reviews/issuer-lifecycle-impl/CODEX-REVIEW.md`): not ready. ILI-01 to
  ILI-09 are being repaired by the implementation sub-agent. The main items:
  - the incurable-failure classification;
  - a snapshot-impossibility ending;
  - complete contradiction treated as conclusive;
  - reconciling signatures before signing closure;
  - work budgeting within the 300 s Lambda;
  - a pruning test;
  - capped reason fields;
  - a content check before allocation.

  **Update 2026-10-30:** after the review rounds ILI, ILC-I, ILC-I2, -I3, then CONFIRM-4 to -10
  (`docs/reviews/issuer-lifecycle-impl/`), Codex rated the issuer **ready for deployment work with the step-5
  gate closed** (CONFIRM-10).
  - 234 tests pass; 45 mutants; `ILCI7_ONESTORE` was retired by the owner as superseded by per-call resumption.
  - Signer draining is oldest-first: one receive per round from a random slot.
  - Handling resumes per call; completed steps are observable and skipped.
  - One deadline guard covers every call. "Never overrun" was withdrawn (an owner decision): the budget is a
    progress mechanism.
  - **Follow-up for deployment work (not a blocker):** quarantine a signature object that `_seal` rejects.
    Otherwise a poisoned digest-matching object is re-adopted each poll and the request stalls (it requires
    storage poisoning, which is outside the trust model).
  - **Next:** commit, then the deployment session (`service/issuer/DEPLOY.md`).
- **Commit pending:** the author's command covers everything; see the end of the 2026-10-30 session.

## Other open items

- **20 Nov** (`formal/freeze-v1/FREEZE-RECORD.md:81`):
  - deployment, which waits on the lifecycle;
  - E10 against AWS;
  - H3: measure it as registered over every provider, with a measurement protocol written first, and expect "idle
    compute $0" to fail;
  - the P9 inspection and the two-machine vector: the System76 live-boot at the release ceremony is the second
    machine;
  - P3 discharge (deploy step 10).
- **Done for 20 Nov:** bounded local refusal (CL-03), the A9.4 missing-capture control
  (`formal/e10/missing-capture/`), and the P3 floor.
- **Release gates** (before the first public verifier release): the custody procedure and its rehearsal, the
  production release key on a YubiKey, the fingerprint channels the author names, the GCP VPC Service Controls
  perimeter, and the E-06 policy.
- **A candidate raised to the author** (not in A11): the verifier's DNSSEC signature checks (RSA alg 8, ECDSA alg
  13, which ground G4) are inventoried but not profiled.
- **Levadura re-run on the signed A11:** the author's call (about $9).
- **tupay embargo:** send nothing about Phase 1a until tupay says both T1 sides have committed first versions.

## How to work here (lessons from these three days, also in qhaway)

- **Routing.** Tony's test: is it irreversible, or scope-changing? If neither, decide it yourself. Where registered
  text changes, his signature adopts the decision. Don't send him pseudo-rulings.
- **Security fixes are confirmed by Codex,** briefed to attack the fix in new ways. The owner's own tests are not
  enough.
- **Prechecks.** `docs/reviews/OWNER-PRECHECKS.md` goes into every review brief. Check 4 now also fails an owner
  requirement that contradicts registered text.
- **Sweeps cover all registered texts,** including the frozen specification, `formal/p8/`, the registration records
  and `spec.bin`. Grep for the vocabulary; don't fix one copy at a time.
- **Never reinterpret a registered sentence after the evidence is in.** Discharge against the text as written, and
  put any stronger requirement in a forward amendment that says it was informed by the outcome.
- **When two review rounds find the same shape, brief a sweep of the class.** For concurrency, model it in TLA+
  instead of iterating prose.
- **Report against the full signed obligation list,** with time estimates that reflect the review base rate. Say
  the uncomfortable part first.
- **Codex runs** use `< /dev/null` and `-c 'mcp_servers.khipumaq.enabled=false'`. OpenAI's filter can block briefs
  phrased as "try to break". Describe the defensive purpose honestly.
