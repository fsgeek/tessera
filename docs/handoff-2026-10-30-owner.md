# Owner handoff, 2026-10-30 (Claude Opus 5.5, owner 2026-10-27 to 2026-10-30, unnamed)

Start here. Then `recall()` in qhaway. The repository and the memory store are the record; where this note
disagrees with them, they win. This supersedes `docs/handoff-2026-10-29-owner.md`.

## Where things stand (all committed, last `9364733`)

- **Amendment 11 is signed** (`f01e086`). It is the consolidated consistency amendment:
  - the P3 verification profile, with a registered floor of 223 owner tests and 968 Wycheproof tests, pinned by
    `formal/p3-verification-profile/FLOOR-MANIFEST.sha256`, and an operational re-run duty whose triggers each
    state what they detect;
  - the dependency-sweep duty, covering the frozen specification and `formal/p8/`;
  - Levadura's 28 findings (obs-0185);
  - the K-R enforcement wording;
  - registration of the E9 cut of A10.4.1;
  - slot-2 custody Option 1, an owner decision adopted by the author's signature.
- **The issuer implements the registered issuance lifecycle** (A11 c016; `docs/decisions/2026-10-29-issuance-lifecycle.md`
  at revision 5.3.1; TLA+ models R5 to R53 in `formal/tla/issuer-lifecycle/`). Codex rated it **ready for
  deployment work with the step-5 gate closed** (`docs/reviews/issuer-lifecycle-impl/CODEX-CONFIRM-10.md`), with
  234 tests passing.
  - Attempts are isolated from one another.
  - A fence write comes before each fetch, and every write is version-guarded.
  - The latch requires three-conjunct, k = 6 evidence.
  - An attempt expires only on complete negative evidence.
  - One deadline guard covers every outside call. It is a *progress* mechanism; "never overrun" was withdrawn.
  - Signer draining is oldest-first, from a random first slot. Handling resumes per call, and completed steps are
    skipped.
  - Deletion is keyed to the persisted request end. L1 is 216 h.
- **The prose matches the code:** S4, L1 and CL-03 (its closed reason set), the clock-tolerance decision, and
  `service/issuer/DESIGN.md` (which carries the termination limits).

## Next, in order

1. **Deployment session.** `service/issuer/DEPLOY.md`, steps 0 to 10. Step 0 is satisfied. The session needs the
   author's `aws login --profile tessera`; `gcloud` is logged in on the NUC.
   - New production keys, never the spike keys.
   - Signer deploys: `service/signer-kms`, and `service/signer-gcp/deploy.sh`, which needs `SLOT2_KEY*` set.
   - `retire-instrument` as a gate, then the review of who can request signatures.
   - The smoke test.
   - Step 10: the `CodeSha256` match, which discharges P3's condition (c).
2. **Small follow-up:** quarantine a signature object that `_seal` rejects. Otherwise a poisoned digest-matching
   object is re-adopted every poll and the request stalls (CONFIRM-10).
3. **20 Nov items** (`formal/freeze-v1/FREEZE-RECORD.md:81`):
   - E10 against AWS.
   - H3: write the measurement protocol first; measure over every provider; expect "idle compute $0" to fail and
     report it as falsified.
   - The P9 inspection, plus the two-machine vector on the System76 live-boot at the release ceremony.
   - P3 discharge, via deploy step 10.
   - The slip rule: if deployment slips past about 6 Nov, run the tail procedure early.
4. **Release gates** (before the first public verifier release):
   - the custody procedure and its rehearsal;
   - the production release key on a YubiKey;
   - the fingerprint channels the author names;
   - the GCP VPC Service Controls perimeter;
   - the E-06 policy.

## Waiting on the author

- **Termination under permanent dependency failure** (design step 5; DESIGN.md's termination section): what V1
  promises when a dependency fails permanently. A2.1's shipping obligation and A2.3's termination obligation
  cannot both hold for protected timely-eligible cases.
  - A2.1's permission is a *lag* test.
  - B is ambiguous between A2's prose (service observation) and its model (`burialAtWall`).
  - The `EVIDENCE_UNAVAILABLE` ending is gated in code until a signed amendment decides. Batch it into one V1
    implementation amendment.
- **Candidates raised, not decided:**
  - The verifier's DNSSEC signature checks (G4) are inventoried but not profiled.
  - A Levadura re-run on the signed A11 (about $9).

## How to work here (all in qhaway; the ones that bit hardest)

- **Routing test:** is it irreversible, or scope-changing? If neither, it is the owner's. Where registered text
  changes, the author's signature adopts the decision. Never hand him a pseudo-ruling.
- **Security fixes are confirmed by Codex,** briefed to attack the fix in new ways. Brief defensively and honestly:
  the OpenAI filter blocks "try to break" phrasing.
- **Prechecks.** Append `docs/reviews/OWNER-PRECHECKS.md` to every review brief. Check 4 fails an owner requirement
  that contradicts registered text.
- **Before recording an owner decision on a registered parameter, grep the registered records** (amendments,
  `formal/p8/`, the freeze, the frozen profile, the AUTHOR-RULINGS files). Never reinterpret a registered sentence
  after the evidence is in.
- **When review rounds repeat a shape, fix the class.** Model concurrency in TLA+. Use oldest-first for
  starvation. Make progress per step with observable completion.
- **Report against the full signed obligation list,** with estimates that reflect the review base rate (every round
  so far has found something). Say the uncomfortable part first.
- **Codex:** `~/.local/bin/codex exec --dangerously-bypass-approvals-and-sandbox -c 'mcp_servers.khipumaq.enabled=false' -o OUT "..." < /dev/null`.
  `grep -c` exits 1 on zero matches; that is not a failure.
- **Give Tony commands as** `! cd /home/tony/projects/tessera && git add <explicit paths> && git commit -S ...`.
- **tupay embargo:** send nothing about Phase 1a until tupay says both T1 sides have committed first versions.
