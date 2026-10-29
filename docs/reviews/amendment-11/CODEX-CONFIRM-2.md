**NOT READY FOR SIGNATURE — A11C-01 remains open: a ZIP pathname alias passes the identity check while replacing verifier code on extraction.** The slot-2 and K-R items are author rulings, not review defects.

Read-only review completed; scratch artifacts are under `/tmp/tmp.lWLnjgFLwZ`. No repository edits or git writes.

1. **A11C-01: not closed.** [test_p3_profile.py:75](/home/tony/projects/tessera/formal/p3-verification-profile/test_p3_profile.py:75) checks only archive names starting literally with `tessera_verify/`. My controls produced:

   | Package | `check_zip` |
   |---|---|
   | Matching verifier and recorded wheel | PASS |
   | Changed `tessera_verify/codec.py` | REJECT |
   | Matching files plus changed `./tessera_verify/codec.py` | **PASS** |

   Python’s `ZipFile.extractall` normalized the last entry and overwrote the checked `codec.py` with `raise RuntimeError("substituted verifier")`. Thus different deployed verifier code can pass. Reject noncanonical paths and extraction collisions, or compare the safely extracted artifact’s effective verifier files. Preserve the separate requirement to authenticate that artifact as deployed.

   **Manifest: PASS.** All 15 entries verify. Its SHA-256 is `4a6c644af2e38882bd40d17cb9d234623f6e52787dc023904c20c6fd38c49d66`, matching [the amendment:58](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:58).

2. **K-R reconciliation: adequate for the author’s ruling.** [Item 5:147](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:147) accurately preserves the message restriction, pure mode, empty context, EXTERNAL_MU, dedication, and administrative-capture limitation while explicitly changing the computation and signing roles. The supplement’s actual role sentence is currently at **173–174**, beneath the cited line-170 heading.

   No additional contradiction found in the implementation: [signer.py:99](/home/tony/projects/tessera/service/signer-kms/tessera_sign_kms/signer.py:99) computes pure-mode, empty-context μ from the raw public key and frame; [line 231](/home/tony/projects/tessera/service/signer-kms/tessera_sign_kms/signer.py:231) validates before signing. The [key policy:52](/home/tony/projects/tessera/service/signer-kms/infra/main.tf:52) grants signing to the signer role and explicitly denies other principals. Administrative policy changes remain possible, as disclosed.

3. **Deployment-key repair: passes the bounded check.** `keyiam`, `job`, and `harden` reject missing inputs and `slot2-spike` before any cloud call. Retirement independently targets `SPIKE_KEY`; it does not require production-key inputs. Bash syntax passed, and a scratch copy with a mocked cloud command completed retirement with already-absent resources. This is not live retirement evidence.

4. **Minor repaired-text inaccuracies:** [item 5:150](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-11.md:150) says “as deployed,” although deployment remains pending. Also, [deploy.sh:31](/home/tony/projects/tessera/service/signer-gcp/deploy.sh:31) and [DEPLOY.md:28](/home/tony/projects/tessera/service/issuer/DEPLOY.md:28) say there are no defaults, but `SLOT2_KEY_VERSION` defaults to `1`. Neither introduces a spike-key production default.

Owner prechecks on the amendment:

| Check | Result | File:line evidence |
|---|---|---|
| Capture row | **PASS** | `docs/phase-0-prereg-amendment-11.md:40–42,147–155`: bounded evidence and signing controls; no attacker-key rejection or capture-visibility promise. Consistent with `docs/V1-CONTRACT.md:37,72–73`. |
| Trigger clause | **PASS** | Amendment `:116–124,141–146`: replacement qualification remains a proposed ruling; deletion retains its conditions; row-25 removal follows the recorded CUT. |
| Requester | **PASS** | Amendment `:125–133,150–155`: covers enqueue/requester paths, signer authority, and administrative override. |
| Binding text | **PASS** | Amendment `:116–124,139,147`: identifies the proposed ruling and unregistered operational resolution; does not invoke the schedule’s ruling budget. |

