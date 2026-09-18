# Codex non-author review of the capstone registration, second round (2026-09-16), dispositioned 2026-09-17

Reviewer: OpenAI Codex CLI (`gpt-6-astra`), run non-interactively by the
owner instance on 2026-09-16 (02:53–02:59 UTC) against the whole of
`formal/suite/capstone/PREDICTIONS.md` after the first-round repairs,
with the first-round record
(`docs/reviews/2026-09-16-codex-review-capstone-predictions.md`) as its
starting point; scratch diagnostics on family-model copies under
`/tmp/tessera-capstone-r2-299yxsvr/`. **The reviewer found the
registration not ready to freeze.** Every factual claim below was
checked against the tree before disposition, and every run the
reviewer made was reproduced on our tree
(`formal/suite/ledger-tests-2026-09-14/cap5*`–`cap8*`, sixth batch of
that directory's README) at the reviewer's own `.out` line numbers.
No capstone model exists; nothing in the repository was run.

**Provenance note, recorded because it is a defect of the record and
not of the review.** The owner instance that dispatched this pass
ended its session at 02:56, three minutes before the pass finished,
having told the author it would read the result on his next message.
The report and its diagnostics sat unread in that session's scratchpad
and in `/tmp` until the successor instance found them on 2026-09-17.
Nothing was lost; the report below is the `-o` output byte for byte.

## Dispositions (owner instance, 2026-09-17)

Provenance labels per `formal/spike/first-link/DECISION.md`: every
disposition below is a **clerk disposition** by the owner instance under
the author's 2026-09-17 direction that the project's readings are the
owner's to take; two of them (findings 3 and 4) fix a fixture meaning
and are marked **contestable** so the author can overrule them at the
freeze commit without an amendment.

1. **C-Q6's repaired emission contract (E1) defeats C-C12.** ACCEPTED.
   Reproduced: `cap5a_ss_q3_companionB_asis.out` (the committed SS.Q3
   companion, unchanged) has `StandingUnentitled` reachable (`:860`),
   the unrestricted correspondence `is false` (`:628`) and the honest-key
   forms `is true` (`:642`, `:656`); `cap5b_ss_q3_e1_projection.out`,
   which adds **only** the guard `if fp(kX) = kfpr` to the standing path
   — the necessary condition E1 imposes by requiring `LayerAccepted` for
   the same `t` and `kX` — makes `StandingUnentitled` **unreachable**
   (`:476`) and the unrestricted form **`is true`** (`:449`) while honest
   standing stays reachable (`:773`). That is exactly the shadowing
   defect S-STANDING's own SS.Q3 prediction named as its p ≈ 0.2 branch
   (`s-standing/PREDICTIONS.md:385-392`): sequencing the standing path
   behind the envelope path makes the companion unable to fail. E1 did
   the sequencing by event dependency instead of by process order; the
   registration's own encoding rule (1) forbids it. **Repair:** (a) the
   fresh acceptance identifier `aid` is minted **at intake** by a
   front-end that reads the presented bundle once and forwards it on
   private channels to the envelope path and the standing path **in
   parallel**; both `LayerAccepted` and `EstablishedWrapped` carry that
   `aid`. The ledger's carried-forward correction ("one fresh name per
   acceptance, shared across its slots, followed by
   `AcceptanceComplete`") is preserved — a bundle yields at most one
   acceptance — and strengthened: the name exists before any check.
   (b) E1 is restated as **same presentation**: the standing path
   computes over the innermost `(t, ppf, sg, fb)` it extracts
   **structurally** from the same bundle (S-P7's `wrap()` destructuring),
   and neither waits for nor is conditioned on `LayerAccepted`. (c) E5
   (`fp(kX) = kfpr` and `kT = kX` inside the standing path) moves **out
   of the emission contract** into the correct verifier's checks: it is
   the very check C-C12 removes, and as an emission precondition it
   shadows the companion. (d) E4 ("wrapped", `lyr ≠ L0`) is the
   front-end's structural parse of the outer frame, not a fact derived
   from acceptance. (e) D13's judge `StandingUnentitledWrapped(kX, t)`
   observes the standing report under `aid` with the wrapped flag, as
   SS.Q3's judge does, and fires when `fp(kX) ≠ kfpr`; reachable under
   C-C12, unreachable in the correct model. (f) **The §(6)
   reconciliation is corrected, and it was wrong, not merely
   inconsistent:** under **C-C12** the honest-key forms **stay green**
   (`cap5a:642`, `:656`) and the unrestricted strict form goes red
   (`:628`) as a consequence of the entitled-key unbinding; it is under
   **C-C11** that the honest-key forms go red (SS.Q2,
   `ss_q2_companionA_identity_declared.out:808`, `:986`), which is D12's
   severing. C-C12's companion row had it right; §(6) conflated the two
   companions.

2. **C-C15(i) cannot retain C-Q7.** ACCEPTED. Reproduced: the C-Q7
   signature-term judge added to the correct S-P7 depth-1 model leaves
   `SigTransplanted` unreachable (`cap6a_sp7_q2_sigjudge.out:1099`);
   added to the Q6b companion (C-C15(i)'s source) it is **reachable**
   (`cap6b_sp7_q6b_sigjudge.out:1809`) with both honest witnesses
   reachable (`:1329`, `:1520`). Verifying an honest inner signature
   under the wrapper key is C-Q7's forbidden relation by definition.
   **Repair:** C-Q7 moves from set (2) to set (1) for configuration (i),
   **descended** (`cap6b:1809`); configuration (ii) is unchanged (Q5c
   transplants no signature across keys; C-Q7 green there is predicted,
   not descended). The red is a **consequence** of the scope severing,
   not a second severing of D5, on the pattern already used for C-Q4's
   `InnerSigTransplanted` in the same row; C-C6 remains C-Q7's own
   companion. The reviewer's alternative — excluding inner acceptances
   from C-Q7's observation — is rejected for the reason the reviewer
   gives: it would blind D5's producer.

3. **C-C7(ii)'s retained set depends on whether the fixture has a
   same-key wrapper signer.** ACCEPTED, with a fixture choice, **clerk
   disposition, contestable.** Reproduced: with an honest `OT_WRAPPER`
   signer under the **same** issuer key `skI` and manifest added to the
   S-P1 diagnostics (and the presented frame's type pinned to
   `OT_ATTEST`, as the capstone's check 5 pins it), correct byte binding
   keeps everything green (`cap7a_sp1_q8_wrapper_signer_base.out:310`,
   `:316`, `:322`, `:330`; witness `:507`), while the type-conditional
   waiver reds **C-Q7** (`cap7b…out:528`), **both** C-Q8 forms (`:711`,
   `:904`) and **honest-key authorship** (`:1072`), witness reachable
   (`:1250`). The trace at `cap7b…out:1032-1072` is the attack: an
   adversary-built `OT_ATTEST` frame presented under the honest key with
   the issuer's honest **wrapper** signature, accepted because the
   signed frame is not `OT_ATTEST` and byte equality is waived.
   **The choice:** the capstone fixture **has** same-key wrapping — `skI`
   wraps its own attestation, as S-P7's I1 does (`s-p7/RESULTS.md:54`,
   `:79-84`, finding F7 and divergence 7) — alongside the separate
   honest wrapper key `skW`. Reason: fidelity to S-P7, whose Q6b/Q5c
   witnesses (`HonestWrappedAccepted`, the descent of C-C15's set (3))
   are reachable **only** through I1 wrapping its own attestation;
   without same-key wrapping C-C15(i)'s wrapped witness is unreachable
   by fixture and the companion cannot show it is non-vacuous. The
   alternative (no same-key wrapping) would preserve C-C7(ii)'s
   registered contrast at the cost of C-C15(i)'s witness. **Consequence,
   descended:** C-C7(ii)'s sets are re-specified — set (1) gains C-Q7,
   honest-key authorship and the round-3 honest-filtered C-Q8 beside the
   structural C-Q8 and link 4; set (2) is the links and judges that do
   not touch byte binding (predicted); set (3) `HonestAccepted`. The
   quantifier-gap contrast (honest-filtered C-Q8 green while the
   structural form is red) is **shown family-locally**
   (`d6d_sp1_q8_type_conditional_unbound.out:315`, `:507`) and is
   registered **not** to reproduce in the composed fixture, because the
   honest wrapper signature is an honest-released signature term over
   non-attest bytes and the honest-filtered form catches it too. **Two
   follow-ups the reviewer did not make, both clean:** C-C6 is
   unchanged by the same-key signer —
   `cap7c_sp1_condunbind_wrapper_signer.out:448`, `:456`, `:633`, `:784`
   match `d5d…out:414`, `:422`, `:599`, `:750` result for result,
   because C-C6's waiver keys on the signed frame's `kfp`, which the
   wrapper frame does name; and C-C7(i) is unchanged —
   `cap7d_sp1_q8_samekey_unbound_wrapper_signer.out:312`, `:493`, `:681`,
   `:847`, `:1027`, `:1206` match `d6e…out:274`, `:455`, `:643`, `:809`,
   `:989`, `:1168`, because (i) demands that the signed frame name
   `fp(kX)` and the wrapper frame names the issuer's own fingerprint.

4. **"Adversary-enrolled issuer key" has no per-mode meaning.**
   ACCEPTED, **clerk reading, contestable.** Reproduced: the committed
   strict S-P1 Q1 baseline is green (`cap8a_sp1_q1_strict_base.out:201`,
   `:208`; witness `:396`); adding an adversary key whose tuple **both
   honest authority processes** publish evidence for — no verifier
   change — makes the unrestricted `Accept ⟹ IssuerSigned` **`is false`**
   (`cap8b_sp1_q1_strict_adversary_enrolled.out:398`) while honest-key
   authorship stays `is true` (`:405`) and the witness reachable
   (`:601`). That is not a defect of the design: a key genuinely
   enrolled by uncompromised authorities **is** an issuer to the
   verifier, and `IssuerSigned` is emitted only by the fixture's honest
   issuer processes. It is a defect of the fixture row, which did not say
   which reading it meant. **The reading:** "adversary-enrolled" means
   the adversary holds `skA` and a self-signed manifest `mA`, and
   authority evidence for `mA` exists **only where the compromise
   supplies it** — in (a)/(b) from the one compromised channel (minted
   with the leaked key, insufficient for strict acceptance at `L0`, so
   the unrestricted strict baseline stays green); in (c) from both (which
   is C-C1's registered red); in (d) from the sole channel (the A4.6
   registered red). **Never** from an uncompromised authority process.
   This inherits S-P7's strict-mode fixture sentence verbatim
   (`s-p7/PREDICTIONS.md:196-205`, the strict sentence itself at `:196-197`: *"In strict mode the adversary cannot
   obtain authority for a wrapper key of its own"*). The alternative
   reading is excluded by `cap8b`, and the skeptic's justification for
   the key (witnesses for C-Q3, C-Q5, C-Q7, C-Q8) needs only the
   compromised-channel route.

5. **The REFUSAL fork stands** as the one routed item; the reviewer
   confirms it is genuine and does not resolve it. Findings 3 and 4 were
   consequential fixture choices left to the builder; they are now this
   file's choices, fixed above, and §8's list of the file's own choices
   grows from two to four.

6. **The first round's six findings**: 1, 2, 5, 6 confirmed repaired by
   the reviewer; 3 partly (closed by finding 2 here); 4 not
   satisfactorily (closed by finding 1 here). The three carried-forward
   ledger corrections are honoured.

**Loop.** One repair pass on the registration (Opus, briefed from these
dispositions, in the file's "Repairs after …" pattern), then a third
owner-run full Codex pass; the file goes to the author for the freeze
commit only when the reviewer says it is ready or its remaining findings
are, in the owner's judgement, things the build itself must decide.

## Codex review — verbatim

## 1. Query strength and discharge

**1. C-Q6’s repaired event contract filters out the failure C-C12 must expose.**

E1 permits `EstablishedWrapped` only after `LayerAccepted` has fired for the same tuple and accepting key. The entitled-key judge likewise observes only reports bound to that successful acceptance. But C-C12’s source attack requires **envelope rejection**: an adversary key presents an honest evidenced tuple, fails the envelope’s fingerprint check, and independently obtains `ESTABLISHED` from the defective standing path. The new observation boundary excludes that attack. (`formal/suite/capstone/PREDICTIONS.md:545–550`, `:639–645`, `:858`; `formal/suite/s-standing/PREDICTIONS.md:363–391`.)

On a copy of the cited S-STANDING companion, I applied only the issuer-key condition inherited from successful envelope acceptance. The unrestricted correspondence changed from **false to true**, and `StandingUnentitled` became **unreachable**, while honest standing remained reachable. This is a bounded demonstration of the filtering problem, not a capstone run. (`/tmp/tessera-capstone-r2-299yxsvr/cc12_e1_projection.pv:254–255`; `cc12_original.out:628`, `:860`, `:1157`; `cc12_e1_projection.out:449`, `:476`, `:773`, all in that directory.)

**Required repair:** bind the standing assessment to the same presentation without conditioning its observation on envelope success, or explicitly revise D13’s consumer and severing test. Running processes in parallel does not preserve orthogonality if the queried event requires the other process’s success. The registration itself requires that independence. (`formal/suite/capstone/PREDICTIONS.md:88–93`, `:938`.)

The reconciliation also remains internally contradictory: it requires C-C12’s honest-key forms **red**, whereas the companion table requires them **green**, matching the source results. (`formal/suite/capstone/PREDICTIONS.md:652–661`, `:858`; `formal/suite/s-standing/RESULTS.md:32`.)

## 2. Companion consistency

**2. C-C15(i) cannot retain C-Q7 while exhibiting its registered signature transplant.**

The repaired row correctly moves `Reattributed` and link 5 into the failed set, but still requires **C-Q7 green**. The same row requires `InnerSigTransplanted` red through verification of an honest inner signature under the wrapper’s different key. That is precisely C-Q7’s forbidden relation. (`formal/suite/capstone/PREDICTIONS.md:686–695`, `:1384`.)

I added C-Q7’s generic signature-term judge to copies of the correct S-P7 model and Q6b companion, without changing their verifiers:

- Correct model: `SigTransplanted` **unreachable**.
- Q6b: `SigTransplanted` **reachable**.
- Both honest witnesses remained reachable.

Evidence: `/tmp/tessera-capstone-r2-299yxsvr/cc15_base.out:1099`; `/tmp/tessera-capstone-r2-299yxsvr/cc15.out:1809`, `:1329`, `:1520`; judge at `/tmp/tessera-capstone-r2-299yxsvr/cc15.pv:102–107`.

**Required repair:** move C-Q7 out of C-C15(i)’s retained set. Excluding inner acceptances from C-Q7 instead would undermine its role as D5’s producer.

**3. C-C7(ii)’s retained guarantees depend on excluding the same-key wrapper signer that C-C15’s witness needs.**

C-C7(ii) waives byte equality whenever the **signed** frame is not `OT_ATTEST`, yet requires both C-Q7 and honest-key authorship green. Its cited S-P1 diagnostic signs only attestations. S-P7’s fixture also signs wrappers under an issuer key, and C-C15(i)’s cited honest wrapped witness exists **only through that issuer wrapping its own attestation**. (`formal/suite/capstone/PREDICTIONS.md:828`, `:1384`; `formal/suite/ledger-tests-2026-09-14/d6d_sp1_q8_type_conditional_unbound.pv:286–296`; `formal/suite/s-p7/RESULTS.md:54`, `:79–84`.)

On paired copies of the cited S-P1 diagnostics, I added an honest `OT_WRAPPER` signer under the same issuer key and manifest, reporting its actual signed bytes. I also retained an `OT_ATTEST` check on presented bytes:

| Query | Correct byte binding | C-C7(ii) |
|---|---|---|
| C-Q7 transplant unreachability | True | **False** |
| Honest-key authorship | True | **False** |
| Honest acceptance | Reachable | Reachable |

Evidence: `/tmp/tessera-capstone-r2-299yxsvr/cc7_base.out:310`, `:330`, `:507`; `/tmp/tessera-capstone-r2-299yxsvr/cc7.out:528`, `:1072`, `:1250`. Added signer: `/tmp/tessera-capstone-r2-299yxsvr/cc7.pv:299–309`.

**Required repair:** freeze the issuer/wrapper signing-role assignment and reconcile both companions against it. The current fixture names a separate `skW` but does not specify the same-key wrapping needed by the inherited witness. This choice changes results. (`formal/suite/capstone/PREDICTIONS.md:64–67`.)

## 3. Prediction bases

Findings **1–3** concern specific failed/retained predictions, not merely uncertain termination under composition. In particular, C-C15(i)’s required transplant directly contradicts its C-Q7 retention, and C-C7(ii)’s supporting diagnostic omits a consequential signing endpoint.

The repaired C-C8 isolation predictions **do** match the tree: possession-only removal falsifies C-Q9 while preserving `SetAltered`; manifest-hash-only removal preserves both. (`formal/suite/ledger-tests-2026-09-14/cap2_sp2_poss_fponly.out:471`, `:1263`; `formal/suite/ledger-tests-2026-09-14/cap3_sp2_mh_guards_dropped.out:468`, `:1115`.)

## 4. Builder-ready contracts

**4. “Adversary-enrolled issuer key” needs a mode-specific enrollment contract; its literal strict-mode reading falsifies the registered baseline.**

The fixture adds an adversary-enrolled issuer key without restricting enrollment to compromised-channel cases. Nevertheless, strict cases (a)/(b) require unrestricted `Accept ⇒ IssuerSigned` green. (`formal/suite/capstone/PREDICTIONS.md:65`, `:71–78`, `:756`.)

An adversary-controlled key honestly enrolled by both authorities can sign acceptable objects without firing the honest issuer process’s `IssuerSigned` event. On a copy of strict S-P1, adding only such an enrollment—under a distinct identity, with no verifier change—made that correspondence **false**. Honest-key authorship remained **true**, and honest acceptance remained reachable. (`/tmp/tessera-capstone-r2-299yxsvr/enrolled_adversary.pv:202–218`; `/tmp/tessera-capstone-r2-299yxsvr/enrolled_adversary.out:398`, `:405`, `:601`; baseline `/tmp/tessera-capstone-r2-299yxsvr/enrolled_base.out:201`.)

**Required repair:** state whether “enrolled” means evidence minted only through compromised channels, or genuine enrollment by an uncompromised authority. Specify this per case and reconcile the unrestricted provenance predictions. The inherited S-P7 strict fixture explicitly excludes authority for an adversary-owned wrapper key. (`formal/suite/s-p7/PREDICTIONS.md:196–205`.)

## 5. Routed and hidden choices

The **REFUSAL fork remains genuine**, with both options and costs stated. Exercising the foreign signing domain makes tag removal testable; leaving it unexercised leaves that test unavailable. I do not resolve it. (`formal/suite/capstone/PREDICTIONS.md:1045–1066`; `formal/suite/lib/tessera_theory.pvl:66–76`.)

Findings **3–4** expose additional consequential fixture choices. Neither signing-role assignment nor strict adversary enrollment is a clerical implementation detail.

## 6. Accepted repairs and carried-forward corrections

The first review’s six accepted findings were checked individually:

| Previous finding | Verification |
|---|---|
| D7 omitted common-content consumption | **Repaired:** link 5 and C-C16 now cover it. `formal/suite/capstone/PREDICTIONS.md:302–310`, `:932`, `:1489`. |
| C-C8 isolation impossible | **Repaired:** the two obligations and isolation outcomes are separated. `formal/suite/capstone/PREDICTIONS.md:1426–1450`. |
| C-C15 retained `Reattributed` and link 5 incorrectly | **Those entries repaired**, but C-Q7 remains contradictory: finding 2. `formal/suite/capstone/PREDICTIONS.md:1384`. |
| C-Q6 join unspecified | **Not satisfactorily repaired:** terms are specified, but the acceptance prerequisite defeats the registered D13 test; its quantifier reconciliation also conflicts. Finding 1. |
| C-Q5 fixture restriction omitted | **Repaired:** explicit one-key/one-manifest assignment and conditional claim. `formal/suite/capstone/PREDICTIONS.md:66`, `:405–435`. |
| “Every other choice is determined” | **Withdrawn as requested.** Findings 3–4 identify remaining choices. `formal/suite/capstone/PREDICTIONS.md:1076–1107`. |

All three carried-forward corrections are honoured: C-Q8 states structural exact-byte verification without an authorship overclaim; link 1b is a correspondence; and each acceptance receives a fresh identifier shared across its slots. (`formal/suite/capstone/PREDICTIONS.md:704–714`, `:210–225`, `:115–130`.)

**This registration is not ready to freeze. The author should see first: finding 1, the standing-event gate that excludes C-C12’s attack; finding 2, C-C15(i)’s impossible C-Q7 retention; and finding 4, the unspecified enrollment boundary that can falsify the strict baseline without any verifier mutation. All probes used family-model copies under `/tmp`; no capstone model was built and no repository file was changed.**

