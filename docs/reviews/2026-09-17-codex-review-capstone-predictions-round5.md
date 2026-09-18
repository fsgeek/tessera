# Codex non-author review of the capstone registration, fifth round (2026-09-17)

Reviewer: OpenAI Codex CLI (`gpt-6-astra`), run non-interactively by the
owner instance on 2026-09-17 (18:16–18:25 UTC) against the whole of
`formal/suite/capstone/PREDICTIONS.md` after the round-four repairs,
with the four earlier records as its starting point; scratch
diagnostics on family-model copies under `/tmp/tessera-capstone-r5/`.
**The reviewer found the registration not ready to freeze**, on two
findings — both on text no earlier round had touched, and both real —
while confirming that all sixteen accepted findings of rounds one to
four are repaired and that the round-four pair-scope and witness
repairs pass its controls. Every factual claim below was checked
against the tree before disposition, and every run the reviewer cites
was reproduced on our tree
(`formal/suite/ledger-tests-2026-09-14/cap13a`–`cap16c`, ninth batch of
that directory's README) at the reviewer's own `.out` line numbers; one
further run the reviewer did not make (`cap14d`) settles the question
finding 2 leaves open. No capstone model exists; nothing in the
repository was run.

## Dispositions (owner instance, 2026-09-17)

Both are **clerk dispositions** of the owner instance. Finding 1 adds a
companion; finding 2 adds a case assignment to every companion. Neither
touches the two contestable fixture choices, which the reviewer again
confirms explicit and which finding 2's repair carries rather than
reverses.

1. **D7's slot-membership half has no severing companion.** ACCEPTED.
   D7 claims discharge of three producers — `Stripped`, `SignerForged`,
   `Spliced` — and its two companions sever completeness (C-C9) and
   common content (C-C16); neither severs **membership**, and link 2a,
   which names `SignerForged` as its producer, registers no companion.
   Reproduced: on a copy of the completeness diagnostic with the
   **manifest-named** slot reported (as §1.3's contract requires; the
   reviewer corrected `cq1c`'s projection from `fp(kA)` to `kfprA`) and a
   structural slot-to-key judge added, the baseline is all green
   (`cap13a_sp2_membership_base.out:1206`); removing **only** slot B's
   `fp(kB) = kfprB` — S-P2 Q4's mutation — reds the slot-to-key judge
   (`cap13b_sp2_membership_unbound.out:1972`) and **`SignerForged`**
   (`:730`) while all three completeness conjuncts stay `is true`
   (`:1685`, `:1722`, `:1759`), `Stripped` (`:481`) and `Spliced`
   (`:1398`) unreachable, witnesses reachable (`:922`, `:1150`, `:1389`).
   **And a consequence the reviewer's run exposes:**
   `PossessionTransplanted` becomes reachable (`:1657`) — the unbound
   slot accepts a possession proof under a key the slot does not name —
   which the family's Q4 row does not record because S-P2's Q4 model
   declares no `PossJudge`. **Repair:** a new companion **C-C17** —
   S-P2 Q4 transcribed, *slot B's key-fingerprint equality removed on
   the two-signer branch, everything else retained* — with set (1):
   **C-Q1 link 2a** at the layer (`ChainBroken(lyr, LINK_2A)`
   reachable, not descended; its shape descended by the slot-to-key
   judge `cap13b:1972` against `cap13a:1206`), **`SignerForged`**
   (descended `cap13b:730`; family-local
   `sp2_q4_companion_slot_unbound.out:360-601`, `s-p2/RESULTS.md:46`),
   and **`PossessionTransplanted`** as a **recorded consequence**
   (`cap13b:1657`), never an assumed retention; set (2): link 2b's three
   conjuncts (`:1685`, `:1722`, `:1759`), `Stripped` (`:481`), `Spliced`
   (`:1398`), `SetAltered` (`:739`), C-Q3 (`:749`), C-Q9 (`:1666`), and
   predicted: links 1a, 1b, 3, 4, 5, 6a, 6b, C-Q2, C-Q7, C-Q8; set (3):
   both `HonestComplete` (`:922`, `:1150`), `HonestAccepted` (`:1389`),
   `HonestChain(L0, t)` predicted. D7's matrix row names three
   companions, one per producer. **Companion count sixteen → seventeen.**
   No timeboxed entry is added (companions carry the companion box).

2. **C-C15(i)'s failed set is a degraded-case result; in strict cases
   its transcription is green.** ACCEPTED, and generalized. Under the
   round-two enrolment reading the adversary holds no authorized wrapper
   key in (a)/(b), so Q6b's mutation — verify the inner signature under
   the **authorized** wrapper key — has nothing to exploit: reproduced
   on the strict model with both outer authority checks and the
   same-key wrapper signer retained, **every query green and every
   witness reachable** in both channel variants
   (`cap14b_sp7_q1_strict_q6b.out:550`, `:559`, `:568`, `:843`, `:1047`;
   `cap14c_sp7_q1_strict_repo_q6b.out`, identical lines). Same-key
   wrapping preserves the witness without producing reattribution. The
   registration listed configuration (i)'s reds with no case
   assignment, and invoked both C-Q1 forms. **The question the finding
   leaves open** — whether D11 is then discharged **at all** in strict
   cases — is settled by a run the reviewer did not make:
   configuration **(iii)**, S-P7 Q6a transcribed onto the strict model
   (`cap14d_sp7_q1_strict_q6a.out`), **reds `Rescoped` in strict**
   (`:892`) through the **honest-only route** — the honest wrapper
   `skW2` wrapping I2's attestation with `idW2` reported as the inner
   identity (trace at `:880-892`) — with `InnerSigTransplanted` and
   `Reattributed` unreachable (`:906`, `:920`) and the witnesses
   reachable (`:1185`, `:1394`). So in strict the identity half of
   conjunct 3 and link 6b are severed by (iii), the key half by nothing
   the strict fixture can present, and D11's discharge in (a)/(b) rests
   on (iii); in (d) on (i), (ii) and (iii). **Repair, generalized to
   every companion:** each companion row gains a **Cases** cell stating,
   per configuration, in which compromise cases its red is **registered
   and descended**, in which it is **predicted**, and in which the
   configuration is a **green control** — the mutation present, every
   query green, every witness reachable, registered so a green strict
   run of a degraded-only companion is a result and not a broken
   fixture. For C-C15: (i) red in (d) (descended, Q6b), **green control
   in (a)/(b)** (descended, `cap14b`/`cap14c`); (ii) red in (d)
   (descended, Q5c ran degraded only), predicted red in (a)/(b) if the
   depth-2 honest route exists, else green control — stated as an
   observation of the run; (iii) red in (a), (b) **and** (d) (descended,
   `cap14d` and the committed Q6a). Every other companion's cases are
   filled from its descent — degraded-only descent means "red in (d)
   descended; (a)/(b) predicted, with the green-control reading named
   where the enrolment rule removes the attack" — and C-C1 stays (c)
   only. Companions descended from strict runs (C-C14, the S-STANDING
   ones) say so.

3. **Conjunct 3's pair-form controls and the witness-rule controls,
   recorded as descent.** Pair form: none — mismatch, unentitled
   unreachable, witness reachable (`cap15a…out:570`, `:998`, `:958`);
   identity only — mismatch **reachable** (`cap15b…out:953`) with the
   key-only control judge **green** (`:576`), unentitled unreachable
   (`:1746`), witness reachable (`:1706`); key only — (`cap15c…out:947`,
   `:1378`, `:1334`); C-C12 only — mismatch unreachable, unentitled
   **reachable** (`cap15d…out:813`, `:1762`, `:1204`); both —
   (`cap15e…out:1192`, `:2140`, `:1581`). Witness rule: C-C11's Q2
   mutation and abl6 alternate keep honest standing, the agreement
   witness and **all five** vocabulary witnesses reachable
   (`cap16a…out:2581`, `:1450`, `:2826`–`:3738`; `cap16b…out:2548`,
   `:1436`, `:2790`–`:3665`); the Q4 alternate keeps the honest-flow
   witnesses (`cap16c…out:2873`, `:1542`) and loses exactly S2 and S4
   (`:3217`, `:3413`), as registered. These go into the file beside
   the round-four descent tables.

4. **The REFUSAL fork stands**, unresolved here, owed at the freeze
   commit. The two contestable choices stand.

**Loop.** One repair pass (Opus), then a sixth owner-run full Codex
pass. Round five's findings are the first since round one on text no
previous round had rewritten, which is the sign that the rewritten
contract has stabilized and the review has moved on to the rest of the
file.

## Codex review — verbatim

## 1. Query strength and discharge

Repository files were read only. Diagnostics used family-model copies and a copied library under `/tmp/tessera-capstone-r5/`; no capstone model was built.

Below, **P** means `formal/suite/capstone/PREDICTIONS.md`; **T** means `/tmp/tessera-capstone-r5`.

**1. D7 still lacks a companion severing its slot-membership consumer.**

D7 claims discharge of **all three producers**: `Stripped`, `SignerForged`, and `Spliced`. Its companions cover completeness and common content, but neither severs membership: C-C9 explicitly retains link 2a and `SignerForged`; C-C16 retains them too. Link 2a identifies `SignerForged` as its producer but registers no membership companion. (`P:276–284`, `P:1280`, `P:1382`, `P:1972`.)

This is a separate obligation. On a copy of the completeness diagnostic, I reported the **manifest-named slot**, as P’s event contract requires, and removed only `fp(kB) = kfprB`, S-P2 Q4’s mutation. All signature, possession, frame and common-content checks remained. (`P:164–169`; `T/membership_unbound.pv:245–249`, `:300–333`.)

Results:

- Structural slot-to-key safety: **false**, versus **true** in the matched baseline.
- `SignerForged`: **reachable**.
- All three completeness correspondences: **true**.
- `Stripped` and `Spliced`: **unreachable**.
- Both `HonestComplete` witnesses and `HonestAccepted`: **reachable**.

Evidence: `T/membership_base.out:1206`; `T/membership_unbound.out:1972`, `:730`, `:1685`, `:1722`, `:1759`, `:481`, `:1398`, `:922`, `:1150`, `:1389`.

**Required repair:** register a membership-severing configuration and its failure on **link 2a**, with its retained set and witnesses. S-P2 Q4 supplies an existing source. The diagnostic also makes `PossessionTransplanted` reachable, so that consequence needs recording rather than an assumed retention. (`formal/suite/s-p2/RESULTS.md:46`; `T/membership_unbound.out:1657`.) Completeness and content companions cannot establish the missing severing required by A3.3. (`docs/phase-0-prereg-amendment-3.md:220–230`.)

## 2. Companion consistency

**2. C-C15(i)’s failed set needs explicit compromise-case assignments: its strict transcription stays green.**

C-C15 registers Q6b’s outermost-key mutation with `Rescoped`, `InnerSigTransplanted`, C-Q3 and C-Q7 among its losses, without separating their outcomes by compromise case. Its row invokes both C-Q1 forms. Yet the chosen enrollment rule excludes attacker-controlled wrapper keys in strict cases (a)/(b). (`P:65`, `P:71–78`, `P:1867`.)

I transcribed Q6b’s mutation onto the correct strict S-P7 model, retaining both outer authority checks and its same-key wrapper signer. In **both** single-channel-compromise variants:

| Query | Result |
|---|---|
| `Rescoped` | Unreachable |
| `InnerSigTransplanted` | Unreachable |
| `Reattributed` | Unreachable |
| `HonestWrappedAccepted` | Reachable |
| `HonestAccepted` | Reachable |

Evidence: `T/scope_strict_q6b.pv:203–222`; `T/scope_strict_q6b.out:550`, `:559`, `:568`, `:843`, `:1047`; identical polarities and line numbers in `T/scope_strict_repo_q6b.out`.

The reason is substantive: Q6b verifies the inner signature under the authorized **wrapper key**. Strict authority prevents enrolling the DSKS-derived or attacker-owned wrapper key used by the degraded attacks. Same-key wrapping preserves the witness without producing reattribution. The source’s degraded attacks and this strict restriction are already documented separately. (`formal/suite/s-p7/RESULTS.md:54`; `formal/suite/s-p7/proverif/sp7_q1_strict_dns_compromised.pv:250–258`.)

**Required repair:** state each configuration’s compromise cases and expected outcomes explicitly, including where its red supplies discharge. If strict runs are intended as green controls, register that. If the failed set is intended only for degraded runs, say so. This preserves both contestable fixture choices.

**Round-four witness repair passes the tested controls.** On the paired-judge copies, C-C11’s declared-identity mutation and unsigned-TLR alternate preserve honest standing and agreement; all five vocabulary witnesses remain reachable. The terminal-unchecked alternate preserves those honest witnesses and loses exactly S2/S4 as registered. (`T/declared.out:1450`, `:2581`, `:2826–3738`; `T/unsigned.out:1436`, `:2548`, `:2790–3665`; `T/terminal.out:1542`, `:2873`, `:3217`, `:3413`.)

I found no dead honest-flow witness in the inspected source companion outputs. Capstone-only witnesses absent from those models remain predictions, not verified composition results.

## 3. Prediction bases

The cap5a–cap12g result citations agree with the archived outputs and README batches six through eight. The registration correctly distinguishes those diagnostics from capstone results. (`formal/suite/ledger-tests-2026-09-14/README.md:159–168`, `:200–204`, `:235–241`; `P:982–1006`.)

The requested **pair-form** controls also pass:

| Mutation | Pair-scope mismatch | Unentitled standing | Agreement witness |
|---|---|---|---|
| None | Unreachable | Unreachable | Reachable |
| Identity only | **Reachable** | Unreachable | Reachable |
| Key only | **Reachable** | Unreachable | Reachable |
| C-C12 only | Unreachable | **Reachable** | Reachable |
| Key mutation + C-C12 | **Reachable** | **Reachable** | Reachable |

Evidence: `T/correct.out:570`, `:998`, `:958`; `T/identity_keycontrol.out:953`, `:1746`, `:1706`; `T/key.out:947`, `:1378`, `:1334`; `T/cc12.out:813`, `:1762`, `:1204`; `T/both.out:1192`, `:2140`, `:1581`.

The identity-only run’s separate **key-only judge stays green**, confirming that the identity comparison causes the new red. Substitution remains excluded. (`T/identity_keycontrol.out:576`, `:569`.)

Finding **2** is an outcome-assignment defect; it does not contradict the cited degraded Q6b results. I found no additional supported probability defect.

## 4. Builder-ready contracts

Findings **1–2** require registration work before implementation: the missing membership companion and explicit compromise-case assignments for C-C15(i).

The two contestable fixture choices remain explicit, with alternatives and consequences recorded. I have not reversed either. Finding **2** identifies a further consequence of the enrollment choice that the companion specification must carry. (`P:65–67`, `P:1568–1590`.)

## 5. Routed and hidden choices

The **REFUSAL fork remains genuine**, with both options and costs stated:

- Exercise the foreign signing domain and add its query/companion.
- Leave it declared and unexercised, leaving that test unavailable.

The freeze statement requires its resolution before the author’s commit. I leave it unresolved. (`P:1488–1516`; `formal/suite/lib/tessera_theory.pvl:66–76`.)

The choices required by findings **1–2** should not be silently delegated as encoding details.

## 6. Accepted findings and carried-forward corrections

All sixteen accepted findings have their specified repairs present:

| Accepted finding | Verification |
|---|---|
| R1.1 — D7 common-content consumer | Link 5 and C-C16 added. `P:374–382`, `:1972`. Finding 1 above concerns the separate membership obligation. |
| R1.2 — C-C8 isolation contradiction | Possession-message and set-integrity obligations separated. `P:1909–1933`. |
| R1.3 — C-C15 retained key-binding guarantees | C-Q3/link 5 removed from configuration (i)’s retained set. `P:1867`. |
| R1.4 — C-Q6 composition join | Shared terms and independent paths specified; paired controls pass. `P:647–658`, `:770–776`. |
| R1.5 — One-key/one-manifest restriction | Explicit assignment and limitation. `P:66`, `:477–510`. |
| R1.6 — “Every other choice determined” | Withdrawn; choices exposed. `P:1526–1593`. |
| R2.1 — E1 shadows C-C12 | Independent intake/extraction; C-C12 still fails. `P:647–684`; `T/cc12.out:1762`. |
| R2.2 — C-C15(i) retains C-Q7 | C-Q7 moved into failed set. `P:1867`. |
| R2.3 — Same-key wrapping unspecified | Explicit contestable choice and consequences. `P:67`, `:1278`. |
| R2.4 — Enrollment unspecified | Explicit per-case contestable choice. `P:65`. |
| R3.1 — Completeness projection loses layer | Projection retains `(aid, lyr)`. `P:140–162`, `:286–319`. |
| R3.2 — Missing standing scope consumer | Paired-report conjunct 3 registered and independently severable. `P:890–911`. |
| R3.3 — Mapping restores fingerprint prerequisite | Immutable terms separated from removable checks; C-C12 retains `kT = kX`. `P:710–720`, `:770–776`. |
| R3.4 — Unsupported authorship generalization | Corrected against cap7b. `P:1207`. |
| R4.1 — Identity-only scope escape | Pair comparison and Q6a isolation configuration registered; identity-only test now red. `P:909–950`, `:1867`; `T/identity_keycontrol.out:953`. |
| R4.2 — Terminal alternate contradicts witness rule | Witness classes distinguished; S2/S4 loss explicitly registered. `P:1162–1196`, `:1307`. |

The three carried-forward ledger corrections remain honoured: structural exact-byte verification without authorship overclaim; publication provenance expressed as a correspondence; and fresh presentation identity with layer-preserving acceptance grouping. (`P:1108–1118`, `:259–273`, `:140–179`.)

**This registration is not ready to freeze. The author should see first: finding 1, D7’s missing membership-severing companion; finding 2, C-C15(i)’s unassigned strict-versus-degraded outcomes; and the unresolved REFUSAL decision required before freezing. The sixteen accepted repairs are present, and the round-four pair-scope and witness repairs pass the requested bounded controls.**

