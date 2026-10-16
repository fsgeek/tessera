# Skeptic review: Amendment 9 (draft, unsigned)

2026-10-12. Reviewer: Claude (Opus 5.5) as a hostile but fair skeptic. This review is about substance, not line edits.
Fidelity and completeness belong to the separate Codex review. Read in full: `docs/phase-0-prereg-amendment-9.md`
(cited as A9:line). Consulted: `formal/p8/ENCODING-V1.md` §5.4, §7, §7.1, §7.2; `docs/V1-DERIVATION-DRAFT.md`;
`docs/V1-SCHEDULE.md`; `docs/reviews/anchor-signatures/CODEX-REVIEW.md`; `prototype/spike-pq/REPORT.md`;
`docs/phase-0-prereg.md:98-107`. Nothing was run.

Severity: **HIGH** means a V1 sentence is false or unexecutable as written, or the change opens a gap a reviewer
would exploit. **MEDIUM** means it overstates, adds a hidden obligation, or has an unhandled off-path case.
**LOW** means wording that a 2106 examiner would misread.
Dispositions: WORDING / MECHANISM / OMIT / REJECT / CUT.

Counts: **4 HIGH, 14 MEDIUM, 5 LOW.**

---

## Scope: what is load-bearing for the V1 claim?

Test applied: if the item is removed, does any V1 sentence (C1–C7, the claim paragraph, the success definition)
become false? Any claim text that was edited only to mention the item is excluded from the test.

| Added 2026-10-12 | Load-bearing? | If cut |
|---|---|---|
| Signature-inclusive anchor `A_sig`, issue order (A9.5) | **Yes.** C5 and the success definition say "signed … no later than T". Without it, CODEX-REVIEW 1 makes that false under later theft. | Not cuttable without a weaker claim routed to the author (CODEX-REVIEW 11). KEEP. |
| Existential root-KSK rule plus the rollover control | **Yes.** Without it every receipt from 2026-10-11 onward is falsely rejected, so C7 fails. This is a bug fix, not scope. | KEEP. |
| Git stamp targets the signed commit id (D-16) | **Yes**, for C4's git channel (pre-stage-then-sign of the assertion). Cheap. | KEEP. |
| `historical_security: NOT_EVALUATED` | Honesty field. It costs one field but is a permanent one (finding 13). | KEEP. |
| Issuance window, verifier rule (`ISSUANCE_WINDOW`) | **No.** C1–C7 as derived hold without it. Only guarantee 2 depends on it. | Removing it falsifies no V1 sentence once "pre-committed issuance window" is struck from the claim. Keeping it is still defensible: it is cheap in the verifier and it implements the author's own mitigation. KEEP the rule. |
| 30-day overlapping windows, 96 h stop, monthly rotation (operating parameters) | **No.** No verifier rule uses them. They conflict with the encoding (finding 2). | CUT from the instrument (findings 2, 10, 12). |
| Conditional PQ hybrid (ML-DSA-65 + P-256) | **No.** No sentence in C1–C7 needs it. V1 is not the production version that A3.6 gates on PQ. | CUT (finding 4). |
| Hardware token for `gpg`; offline hardware repository root | **No verdict depends on it.** The author asked for it. | Keep it as operational practice. Take it out of the spike pass condition and out of the fallback's definition (findings 1, 6, 15). |
| Exit procedure plus end-of-issuance statement | **No.** No verifier rule consults it (A9:276). | OMIT from the instrument and move it to a runbook (finding 11). |
| C3 single-controller non-claim | **Yes**, as a narrowing (row 15). | KEEP. |

On the current trajectory, four of today's five additions are scope that the V1 claim does not need. The amendment
puts four new items on the 30 Oct exit gate (A9:171-172) 18 days before that gate, and it has no registered cut
order (finding 18).

---

## Findings

### 1. HIGH: the queue-fed token signer is an oracle. An AWS compromise yields both slots.
**Quote:** A9:251-252, "slot `gpg` is **P-256** OpenPGP (rule O), on an **author hardware token** via gpg, on
author-controlled hardware outside AWS, pulling from a queue with no inbound path." Also C3 (A9:113), "separate
technical failure domains", and guarantee 2 (A9:289), "An adversary holding every required slot's key".

**Scenario (a key stolen on day 2 of its window):** On day 2 an attacker obtains IAM credentials in the issuing AWS
account. The attacker does not touch the token. They call `kms:Sign` for the `kms` slot and enqueue arbitrary frames on
the queue the gpg host pulls from. The token signs whatever arrives. "No inbound path" protects the host, not what
it signs. The attacker mints `VALID_STRICT` receipts for any content until the window ends. The token was never
"stolen", so a reader of guarantee 2 ("holding every required slot's **key**") concludes this case is excluded. It is
not. The custody split resists key *extraction* only, not *oracle use*. The real security boundary of both slots
is the AWS account. CODEX-REVIEW 2 already asked for "signing capability", not "key".

**Simplest alternative reading:** two keys under two custodies means AWS alone cannot mint. That reading is false
under this architecture.

**Disposition:** WORDING. Use "signing capability for every required slot" throughout A9.6. Add to C3: "the `gpg`
signer signs frames delivered by the AWS-side issuer, so capture of the issuing account confers both signatures;
the token prevents key export, not misuse." Optional MECHANISM, not for V1: the gpg host keeps its own append-only
log and rate limit.

### 2. HIGH: "overlapping" windows cannot be expressed under the encoding this amendment adopts.
**Quote:** A9:267-268, "**30-day windows**, overlapping so a successor key is published before its predecessor
retires". Against `formal/p8/ENCODING-V1.md:541`: "**RRset:** exactly **one** TXT record at the owner name
(`DNS_RRSET` if there are zero or more)". One record carries both fingerprints and the window (:552-553). The owner
name `_tessera-v1.<D>` is fixed (:535).

**Scenario (first rotation, about day 26):** The issuer publishes the successor's record. There can be only one
record, so the predecessor's record disappears from DNS. Any predecessor attempt whose DNSSEC snapshot had not yet
been captured can no longer get one. The overlap the amendment promises cannot exist. The alternative, adding a
second TXT record, makes every snapshot `DNS_RRSET`, which rejects every receipt during the overlap. A9.1 makes
ENCODING-V1 the profile's encoding, so the two signed texts contradict each other.

**Disposition:** MECHANISM or CUT. Either (a) drop "overlapping" and register a hard cutover: stop predecessor
signing at not-after − (δ + skew), then swap the record, accepting an issuance pause; or (b) CUT 30-day windows
for V1 and publish one window that covers V1's horizon. The DNS-02 example already uses a one-year window
(ENCODING-V1:572). Option (b) also removes findings 10 and 12. Do not change the one-record rule: it is what makes
the record unambiguous.

### 3. HIGH: the code rule weakens the original's purpose and has an undefined trigger. It is labelled G, not W.
**Quote:** A9:163-166, "**no code that carries a V1 claim is written until that claim's exit row is `checked`.**
… Code built as an instrument … is allowed before exit. It is labelled as such, it never ships, and nothing it
produces discharges an obligation." The original (`phase-0-prereg.md:102-107`): "Before any code, the central
guarantee is established by a machine-checked formal model and proof … No time bound — a rushed proof is worse
than none".

**What the original was for:** do not build until the guarantee is *proven*, and do not trade proof quality for
time. The replacement departs from that purpose in four ways:
- **"checked" is not "established".** V1-DERIVATION:76: "'checked' means the tool passes. **No row is
  `discharged`.**" C1 (P8) rests on a *prose* proof plus vectors (A9:168), not a machine-checked one. The
  replacement lets service code be written on weaker evidence than the original required.
- **The time bound reverses "no time bound".** The original said "a rushed proof is worse than none". The
  amendment now has a 30 Oct ceiling, time-boxed reviews, and a closure rule that keeps late findings from gating
  (A9:177-179). This is a weakening. A9.7 row 1 labels it **G** (gate moved); it should be **W**.
- **"That claim's exit row" is undefined.** The exit gate (A9:167-172) lists property and evidence rows, not rows
  per claim. V1-DERIVATION:117 maps one E1 row to "C1–C5, C7" jointly. A per-claim rule invites partitioning:
  "this module carries only C2, and C2's row is checked, so I may write it." Meanwhile A9:176 says the *exit* opens
  Phase 1a. That makes two incompatible gates.
- **Instrument outputs already gate the exit.** "The signer branch recorded" (A9:172) is decided by the spike's
  output. "The root-KSK rollover control" cites SPIKE-REPORT. So "nothing it produces discharges an obligation"
  is already strained. The rule also does not say whether the vector generators and the verifier count as
  instruments or as claim-carrying code. "Never ships" is unenforceable as stated: `prototype/spike/issue.py` and
  `poller.py` are the obvious seed for the issuer.

**Disposition:** MECHANISM plus WORDING. (a) Make it one gate: "no V1 issuer or verifier code before the 30 Oct exit
is recorded". (b) Define *instrument* by containment, not by intent: it lives under `prototype/`, no V1 code imports
from it or copies from it, and its outputs may *select* among pre-registered branches but never stand as evidence
for a C-row. (c) Relabel row 1 as **W** and state plainly that the time box replaces "no time bound". (d) Commit
the instruments. `prototype/spike/` and `prototype/spike-pq/` are untracked today (git status), so the 2106
examiner has no record of the code that shaped the KSK rule and the signer choice.

### 4. HIGH: the conditional PQ hybrid carries no V1 claim. Cut it.
**Quote:** A9:250-262, and row 25 (A9:331), "If the spike passes, V1 is that deployment profile".

**Scenario (the spike half-passes on 21 Oct):** The KMS ML-DSA-65 signature verifies in two implementations, but
rule R vectors are incomplete, or the pair id's R-3.12 and P3-model pass is unfinished. The fallback is taken, and
nine days of work are discarded. If it fully passes instead, the 9 days between 21 Oct and the 30 Oct freeze must
re-run P3's model for a mixed-format pair, regenerate the golden and rejection vectors for 3309-byte `kms`
signatures, and settle a new P4' partition entry. All of that lands in the exit window the slip rule protects.

**What it buys within V1:** nothing that can be verified. Guarantee 2 already bounds minting after not-after under
the fallback. A quantum break of P-256 before V1's windows expire is not a credible scenario. For historical
receipts, `historical_security` is `NOT_EVALUATED` under both branches. Row 25 also edits A3.6's registered deferral
by condition, which drags a production-gate question into a demonstration profile.

**Disposition:** CUT. Register the classical P-256 pair (P4') as V1's only signer profile, and delete row 25 and
A9.4's PQ sentence (finding 9). Record the 2026-10-12 PQ spike as an instrument result for the production version.

### 5. MEDIUM: a window cannot be shortened after theft, and the amendment does not say so.
**Quote:** A9:291-292, "Inside the window, such a thief mints receipts that pass; detecting that is the B(ii)
add-on, not V1."

**Scenario (key stolen on day 2):** The operator detects the theft on day 3. Re-publishing a shorter window is "a new
authority event", but the old, anchored evidence with the long window remains valid evidence. The thief keeps 27
days. Readers will take the author's rationale ("limit their lifetime … mitigate the potential damage") to mean the
operator can respond. The amendment never says the operator cannot. The mechanics are also more favourable than the
amendment says. The 30 Oct snapshot rule (V1-DERIVATION:94) requires the snapshot's anchored time to fall within
[declared − ε, declared + δ]. Withdrawing the TXT record therefore bounds new mints to roughly the remaining RRSIG
validity of a replayed signed RRset plus ε + δ. That is an unclaimed quasi-revocation, and it depends on spec text
A9 does not contain.

**Disposition:** WORDING. Either state "a published window cannot be shortened; detection changes no V1 verdict",
or, if the DNS-withdrawal bound is wanted, claim it with its mechanism (RRSIG validity + ε + δ) and a vector. Do
not leave customers to infer either.

### 6. MEDIUM: both signer branches depend on a token whose type the author has not chosen.
**Quote:** A9:256-257, "a real P-256 signature from the hardware token via gpg verifies offline". A9:258-259, the
fallback: "the gpg key on the hardware token". Open item A9:358: "Whether the hardware token is a YubiKey or a TPM
2.0 (asked of the author 2026-10-12, unanswered)."

**Scenario (the author is unavailable until November):** No token means the hybrid fails its pass condition, and
the fallback is not executable as defined either. The 30 Oct "signer branch recorded" item cannot be met on either
branch. A "registered fallback" should not share the risky dependency of the primary.

**Disposition:** MECHANISM. Define the fallback without the token: "`gpg` slot on author-controlled hardware;
hardware token when available". The token then becomes a hardening step, not a gate.

### 7. MEDIUM: "fixed before the spike runs" leaves out a spike that already ran.
**Quote:** A9:254, "*Pass condition* (OWNER DECISION 2026-10-12, fixed before the spike runs)".

**Evidence:** `prototype/spike-pq/REPORT.md` and `run.log` (untracked, 2026-10-12 00:23 UTC) ran ML-DSA-65 in two
implementations, external μ on a 6354-byte frame, and SLH-DSA with only one implementation. The pass condition
then required "two implementations" and replaced SLH-DSA with P-256 (ENCODING-V1:425). Both choices look
informed by that run. The *real-KMS* spike has not run, but a 2106 examiner reading "fixed before" will assume no
data informed the condition.

**Disposition:** WORDING, moot if finding 4 is adopted. Say "fixed after an offline pre-spike (`prototype/spike-pq/`,
committed at <hash>) and before the KMS spike", and commit the pre-spike.

### 8. MEDIUM: "Neither is a verdict V1 computes" is false for guarantee 2.
**Quote:** A9:280, "**The two product guarantees, stated conditionally (CODEX-REVIEW 7).** Neither is a verdict V1
computes." Guarantee 2 is exactly the `INVALID / ISSUANCE_WINDOW` rule (A9:265-266). The C4 row (A9:114) and the
claim (A9:105) include the window.

**Why it matters:** under the closure rule (A9:178), a late finding gates V1 only if it hits C1–C7. If guarantee 2
is "not a verdict", a counterexample to it (for example finding 1) can be routed to the register instead of gating.

**Disposition:** WORDING. Say: "Guarantee 2 is the C4 window rule, stated as a property. Guarantee 1 is not
computed." Make findings against guarantee 2 C4 findings for the purposes of the closure rule.

### 9. MEDIUM: "A PQ leg removes the need for a quantum cutoff" overstates.
**Quote:** A9:217.

**Alternative reading:** the PQ leg *replaces* a P-256 quantum cutoff with two other conditions: an ML-DSA-65
historical-security assumption (lattice cryptanalysis also needs a cutoff), and the integrity of KMS custody. Under
one controller (C3), a quantum-capable insider still needs only KMS access. Strict mode also needs both slots, so
the PQ leg helps only while ML-DSA-65 and KMS custody both hold.

**Disposition:** WORDING ("removes the need for a P-256 quantum cutoff, at the price of an ML-DSA-65 cutoff and the
KMS custody assumption"), or OMIT with finding 4.

### 10. MEDIUM: the author's availability becomes a runtime dependency of the service.
**Quote:** A9:251-252 (the token on author hardware), A9:270-271 ("the repository key is an offline hardware root
used only for rotations"), A9:267 (30-day windows), and V1-SCHEDULE:33 (the author's budget: "about 2 h a week").

**Scenario (the author is away for a month):** No rotation is signed by the repository root and no successor record
is published. The current key stops signing at not-after − 96 h, and issuance halts. If the token host is offline,
issuance halts on the first day. That fails safe, but success criterion 1 ("at a stated cost and latency") now
depends on a personal machine's uptime and a monthly ceremony that takes more than the 2 h/week budget can
reliably cover. Nothing in the amendment states the availability this implies.

**Disposition:** MECHANISM or CUT. Use one window covering V1 (finding 2(b)), so the repository root is needed once.
State the expected availability of the token host in H3's latency number, or accept and register "issuance pauses
when the author is unavailable".

### 11. MEDIUM: the exit procedure is a permanent obligation that no claim needs.
**Quote:** A9:274-278, "When V1 stops issuing: destroy the keys (KMS scheduled deletion; hardware token reset), and
publish an **end-of-issuance statement** …".

**Scenarios:**
- (a) On 4 Dec the author decides "stop". The procedure is now owed on the stop date, by a project that has just
  stopped.
- (b) The token is lost. A "hardware token reset" is impossible, and nothing says what happens instead.
- (c) The procedure destroys the signing keys but says nothing about the repository root, which can still sign a
  new window.
- (d) "The issuance window … bounds minting after exit" (A9:277). With 30-day windows, an exit on day 5 leaves 25
  days in which a thief who already has signing capability can mint.

**Disposition:** OMIT from the instrument and move it to an operations runbook. If one sentence stays, make it
"the issuer stops signing; keys are destroyed when practicable; the last window's not-after is the effective end",
and align exit with a window's end.

### 12. MEDIUM: registering operating parameters turns them into amendment-grade obligations.
**Quote:** A9:267-271. The parameters are introduced as "*Operating parameters* (not verifier rules)", yet they sit
in the signed instrument: 30 days, overlap, 96 h, offline root.

**Scenario:** In week 3 the 30-day cadence proves too costly (finding 10). Under amend-don't-rewrite, changing "30"
needs Amendment 10. Changing it without one leaves the record showing a registered parameter that was violated.

**Disposition:** CUT the specific values from A9. Register only the invariant a verifier-side guarantee needs: "the
issuer never ships a receipt whose T could exceed not-after; its stop margin is at least δ plus the A2.1 skew
bound". Put the values in an operations document.

### 13. MEDIUM: the "contract for later verifiers" binds every future verifier, and the trust configuration will move under it.
**Quote:** A9:219-221, "a later verifier given a V1 bundle returns the same verdict and values in a declared stable
field set".

**Off-path:** A later verifier ships newer header pins. A bundle that was `UNVERIFIABLE / HEADERS_NOT_COVERED` (A9:126)
under the old pins is now `VALID_STRICT`. That breaks "same verdict". The same happens when the next root-KSK
rollover changes the trust configuration (finding 22). The text reads as a clarification but is a compatibility
promise with no expiry, extending to verifiers that do not yet exist.

**Disposition:** WORDING. Say "the same verdict **given the same trust configuration**, and never a weaker verdict
because of missing status capture". Name it as an A9.3-style obligation of later profiles, not a property of V1.

### 14. MEDIUM: "registered as named future obligations, not commitments" contradicts itself.
**Quote:** A9:200.

**Why it matters:** in this project's vocabulary, a registered obligation needs an amendment to retire. Four V2
drivers, including separation of control, now sit in the pre-registration with that status. That is the "new
obligations disguised as clarifications" pattern.

**Disposition:** WORDING. Say "candidate capabilities, recorded for context; they create no obligation and need no
amendment to drop."

### 15. MEDIUM: hardware keys are specified, but their loss is not.
**Quote:** A9:252, A9:270-271.

**Scenarios:**
- A non-exportable `gpg` key on a lost token means issuance stops until a new key is published under a new window.
  The loss cannot be told apart from theft, so the lost key's window has to be treated as compromised until
  not-after (finding 5).
- If the "offline hardware root" is also a single token and it is lost, no new key assertion can be signed by the
  key in the verifier's trust configuration. That needs a new verifier release, and every relying party has to
  update.

**Disposition:** MECHANISM (a backup root held separately) or OMIT the hardware specifics from the instrument.
If the specifics stay, the failure cases must stay with them.

### 16. MEDIUM: one unnamed tester supports "a relying party can verify … from documentation alone".
**Quote:** A9:92-95, together with Decision C ("a human tester") and Q4, which is open.

**Alternative reading:** one non-expert reached the safe decision on 13 rows, against documentation written by
the same owner who built the fixtures. That is an existence demonstration (n = 1), not evidence about relying
parties in general. If the tester has seen the project, the registered prediction ("a headline-only reader fails e
and f", A9:158) cannot be tested.

**Disposition:** WORDING. State n, the tester's independence criteria (no prior exposure to Tessera; no access to
the owner during the test), and that criterion 2 is demonstrated for one reader.

### 17. MEDIUM: the governance loop on Q1 is circular, and bulk ratification blurs the provenance labels.
**Quote:** A9:58-59 (the author: "The decision to change that rule isn't mine, it is the owner of the project");
A9:19 ("Nothing here binds until the author signs"); A9:181 ("The author's signature on this amendment ratifies
both").

**Scenarios:** If the author is unavailable on 16 Oct, the owner's "decision" binds nothing and the 16 Oct milestone
slips. If he signs, one signature "ratifies" every OWNER DECISION in the file. The 2106 examiner then cannot tell
which choices the author actually weighed, which is the reason the labels exist. The schedule's budget of 8
load-bearing rulings is quietly spent as one.

**Disposition:** WORDING. Say what the signature means for OWNER items. Recommended: "the author's signature
adopts the instrument and permits the owner decisions; it does not convert them into author rulings." Keep A9:181
only for δ, ε, k, N, S, which A9.2 explicitly puts to him.

### 18. MEDIUM: the 30 Oct gate grew today, and no cut order is registered.
**Quote:** A9:171-172, "Added 2026-10-12: the anchored-versus-unanchored-signature negative control;
`ISSUANCE_WINDOW` vectors; the root-KSK rollover control (A9.5); the signer branch recorded (A9.6)." Also the
slip rule (V1-SCHEDULE:30-31).

**Scenario:** On 6 Nov the exit is a week late. The slip rule gives the author "cut scope or stop", but nothing says
*what* to cut. The choice is improvised under pressure, by an author with a limited ruling budget.

**Disposition:** MECHANISM. Register the cut order now, using the scope table above: PQ hybrid first, then 30-day
windows and their operating parameters, then the exit procedure, then the token requirement. Never cut `A_sig`, the
KSK rule or D-16.

### 19. LOW: "breaks of … the SHA-1 links in git" names a break that has already happened.
**Quote:** A9:39-40.

**Point:** SHA-1 chosen-prefix collisions are practical (2017 and 2020 results). A 2106 examiner will read this
residual as having fired before V1 shipped. The property actually relied on is second-preimage resistance, plus the
fact that the author, not an attacker, chooses the blob contents.

**Disposition:** WORDING. Say "a second-preimage break of SHA-1, or attacker influence over committed contents".
Optional, later: a SHA-256 object-format repository for key assertions.

### 20. LOW: "inside that window" is two-sided, but the check is one-sided on T.
**Quote:** A9:29 ("inside that window") and A9:106 ("T lies inside the keys' issuance window"). The rule (A9:265-266)
is not-before ≤ `declared_issue_time` and T ≤ not-after.

**Point:** T ≥ not-before follows only through the temporal predicate. The text claims something more direct than
the rule checks.

**Disposition:** WORDING. State what is checked: the declared time is no earlier than not-before, and T is no later
than not-after.

### 21. LOW: anyone can turn an honest receipt into `INVALID / ISSUANCE_WINDOW` by re-stamping it.
**Point:** T is the earliest attestation *in the presented proof* (A9:115). Anyone can OTS-stamp `SHA256(A_sig)`
again after not-after and present only that proof. The honest receipt then reports `INVALID`, a verdict that reads
as evidence of forgery, not of a bad presentation. This is safe in direction (a false reject), but the verdict type
misleads, and an intermediary can cause it.

**Disposition:** WORDING. Document this in the relying-party text: "`ISSUANCE_WINDOW` can result from presenting a
later proof; ask the holder for the issuer's original proof."

### 22. LOW: the trust configuration has an unstated validity horizon.
**Quote:** A9:124-125 and A9:239-243.

**Scenario (the KSK rolls again):** KSK-2024's signing period is open-ended in the shipped configuration. Snapshots
taken after the next rollover fail under an old verifier until a new configuration ships. Separately, if KSK-2024
is retired and its end date is never recorded, the open-ended period stays trusted. For V1's horizon this is
unlikely to fire, but a 2106 examiner needs to know it.

**Disposition:** WORDING. Say "the trust configuration's KSK periods are as known at release; snapshots after an
unlisted rollover are `UNVERIFIABLE`." Check that the result is `UNVERIFIABLE` and not `INVALID`.

### 23. LOW: the headline drops the key-secrecy condition.
**Quote:** A9:25-26, "A V1 receipt lets anyone … check four things: that particular bytes were presented to the
Tessera V1 service".

**Point:** The condition is added two paragraphs later (A9:34). Under finding 1's scenario, "presented to the
service" is false while the verdict is `VALID_STRICT`. A reader who stops at the headline is exactly the failure
the registered prediction expects (A9:157-158).

**Disposition:** WORDING. Put "provided the service's signing capability was not misused within the key's window"
in the first sentence.

---

## Not found to be a problem

- The signature-inclusive anchor and the issue order follow CODEX-REVIEW 1, 4 and 6 faithfully. With no fallback,
  there is no downgrade path.
- The existential root-KSK rule is the standard RFC 5011-style reading. The control case is real (SPIKE-REPORT).
- Rows i and i′ are an honest addition. The registered prediction makes them a test of the documentation, not of
  the verifier.
- The C3 narrowing (row 15) is a genuine weakening, and it is labelled as such.
