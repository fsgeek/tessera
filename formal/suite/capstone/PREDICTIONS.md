# The capstone composition context: query plan and registered predictions

**Status: PROPOSED, drafted by the AI collaborator (Claude Opus 5),
directed by the owner instance, 2026-09-15; not adopted; the commit is
the author's. Not frozen. No capstone model exists; no capstone query
has been run.** *(REPAIR 2026-09-17, skeptic read S-5. The withdrawn
sentence, quoted: “No model exists. Nothing has been run.” It was
unqualified, and since 2026-09-16 this file cites roughly ninety
ProVerif runs made **for** it — `cap1`–`cap25` under
`formal/suite/ledger-tests-2026-09-14/`, in thirteen dated “Scratch runs
made for this repair” tables and one dated note. Those runs are
**family-copy diagnostics**: copies of committed family models, mutated
and re-run to descend a prediction. **Not one of them is a capstone
result**, no repository model was edited or run, and every section that
cites them says so in place. The file's own round-7 rule is that an
unqualified all-clear claim is what goes wrong; this header was the last
one.)* Per
`formal/suite/ENUMERATION.md` §5 (`:149-158`), predictions are
registered and frozen, by the author's signing commit containing this
file, **before any capstone model is written or run**. Post-freeze
changes are prediction divergences, never refinements. Amend-don't-
rewrite applies from this file's first commit.

**Provenance.** Drafted from `formal/suite/LEDGER.md` §6 (`:1250-1559`)
under the author's ruling of 2026-09-15 (`:55-71`, `:941-955`): **outcome
5**, R-1 = Reading B (composed), R-2 = yes, R-3 = formulation W. The
author's words are quoted verbatim in the ledger and are not paraphrased
here. The three post-ruling corrections (`:2156-2281`) and the four
dispositions of
`docs/reviews/2026-09-15-codex-full-review-ledger-round4.md` are honoured
throughout. **This file registers nothing and discharges nothing.**

## The gate this file serves

Amendment 3 §A3.3 (`docs/phase-0-prereg-amendment-3.md:220-230`),
verbatim:

> Band 0 exit is gated on a capstone composition context in which
> every ledgered **cross-model** assumption — a fact one symbolic
> model assumes and another must establish — is discharged by a
> machine-checked producer query and carries a broken companion that
> **fails the query consuming the severed link**. Layer 2 assumptions
> (cryptographic primitive security, historical trust-anchor
> correctness, chain availability, implementation fidelity,
> operational independence of authority channels) are explicitly
> exposed and unclaimed in the ledger — never discharged, never
> silently absorbed. Any termination-forced scoping is named in-module
> and disposed by amendment discipline, never silently.

And ENUM §3's linkage obligation (`ENUMERATION.md:116-117`): *"Linkage
query proves the §A3.2 chain — the links, not just cardinalities, per
layer"*.

## What the capstone is

**One model**, `formal/suite/capstone/proverif/capstone.pv`, built with
`proverif -lib formal/suite/lib/tessera_theory.pvl`. It transcribes the
shared library and composes the families' verifier checks into **one
acceptance path per layer**, plus a wrapped-standing composition. Under
R-1 Reading B the producer's fact and the consumer's query live in the
same model, so the joins the ledger calls cross-model become internal to
this one verifier and the families' severing mutations become this
model's own companions (`LEDGER.md:664-682`, `:707-731`). Nothing here
is a result; every colour below is a prediction written before the model
exists.

---

# 1. Registered specification

## 1.1 The fixture (`LEDGER.md:1392-1406`)

| Element | Registered content |
|---|---|
| Authority channels | `skD` (DNS) and `skR` (repository), strict form; one sole channel in the degraded form. n = 2, a finite enumeration, never a quantified result (L2-h, `:882`) |
| Issuer keys | `skI` and `skI2` — §6(4)'s **(N2)**, which is ENUM amendment note 3's two-honest-values rule (`ENUMERATION.md:244`, `:262-263`; *line cite added — skeptic 2026-09-15*) |
| Adversary | `dsks(s, r)` throughout (D-4) and adversary-chosen payloads, both §6(4)'s. **ADDITION beyond §6:** *an adversary-enrolled issuer key of its own* — `:1392-1406` does not list one. Justification: C-Q7 and C-Q8 are registered unreachable over acceptances “whoever made `sg`” (`:1290`), and C-Q3 / C-Q5 are stated over an adversary key the manifest does not name; without an adversary key that is not a `dsks` derivative those queries are satisfied for want of a witness. Source lines: `:1289`, `:1290`, `:1292`. *(Marked — skeptic 2026-09-15.)* **What “adversary-enrolled” MEANS, stated per case** *(REPAIR 2026-09-17, Codex round 2 finding 4 — **this file's clerk reading, contestable by the author at the freeze commit**; the row added the key without saying which reading it meant, and the two readings differ in colour)*: the adversary holds `skA` and a **self-signed manifest** `mA`, and authority evidence for `mA` exists **only where the compromise supplies it** — in **(a)** and **(b)** from the **one compromised channel** alone (evidence minted with the leaked key, **insufficient for strict acceptance at `L0`**, which needs both channels, so the unrestricted strict `Accept ⟹ IssuerSigned` baseline stays **green**); in **(c)** from **both** channels, which is **C-C1**'s registered red; in **(d)** from the **sole** channel, which is the **A4.6 registered red** (`docs/phase-0-prereg-amendment-4.md:156-171`). **NEVER from an uncompromised authority process.** This inherits S-P7's strict-mode fixture sentence verbatim (`s-p7/PREDICTIONS.md:196-205`; the sentence itself at `:196-197`: *“In strict mode the adversary cannot obtain authority for a wrapper key of its own”*). **The other reading — genuine enrolment by uncompromised authorities — is excluded, and excluded on evidence:** it falsifies the registered strict baseline **with no verifier change at all**. The committed strict baseline is green (`cap8a_sp1_q1_strict_base.out:201`; honest-key authorship `:208`; witness `:396`), and adding **only** an adversary key whose tuple **both honest authority processes** publish evidence for makes the unrestricted `Accept ⟹ IssuerSigned` **`is false`** (`cap8b_sp1_q1_strict_adversary_enrolled.out:398`) while honest-key authorship stays `is true` (`:405`) and the witness stays reachable (`:601`). That is **not** a defect of the design — a key genuinely enrolled by uncompromised authorities **is** an issuer to the verifier, and `IssuerSigned` is emitted only by the fixture's honest issuer processes — it is a defect of this row, repaired here. **The skeptic's justification above needs only the compromised-channel route:** C-Q3, C-Q5, C-Q7 and C-Q8 get their witnesses from it |
| Required-signer set | Size two: `skI` in slot A, `skB2` in slot B; positional `signers0` / `signers1(·)` (D-2). Both the one- and two-signer branches are exercised. **The key assignment is fixed here, not left to the builder** *(REPAIR 2026-09-16, Codex finding 5)*: the two-signer manifest `M2` names `fp(pk(skI))` in slot A and `fp(pk(skB2))` in slot B; **the one-signer manifest `M1` names `fp(pk(skI2))`, and `skI2` signs `M1` and nothing else**. **ONE KEY, ONE MANIFEST** — each honest signing key signs exactly one manifest and signs possession over that manifest only — which is **S-P2's registered fixture restriction, inherited** (`s-p2/PREDICTIONS.md:201-214`, and `s-p2/RESULTS.md:444-447`, where Q2's claim (3) states the rule and records that `SetAltered` is instrumentation, not a verifier check, after the reviewer's `a_key_reuse` false positive). See C-Q5 below for why the restriction is load-bearing and for the scratch run that shows it |
| Wrapper | `skW` over an `OT_WRAPPER` frame, S-P7's `wrap()` / `InnerCheck` idiom, **depth ≤ 2** (layers `L0`, `L1`, `L2`). **The fixture ALSO has SAME-KEY WRAPPING** *(REPAIR 2026-09-17, Codex round 2 finding 3 — **this file's fixture choice, contestable by the author at the freeze commit**; it is not the ledger's and is not an author ruling)*: **`skI` wraps its own attestation**, exactly as S-P7's **I1** does (`s-p7/RESULTS.md:79-84`, *“I1 attests and wraps; I2 attests and signs `OT_REVIEWREC`; W1 and W2 sign wrappers only — divergence 7”*; and `:54`, finding **F7**, where Q6b's `HonestWrappedAccepted` is reachable *“only through I1 wrapping its own attestation”*), **alongside** the separate honest wrapper key `skW`. **Reason:** fidelity to S-P7, whose Q6b and Q5c honest wrapped witnesses — the descent of **C-C15**'s set (3), §9(1) — are reachable **only** through the issuer wrapping its own attestation; without same-key wrapping **C-C15(i)'s wrapped witness is unreachable by fixture** and the companion cannot be shown non-vacuous. **The alternative, and its cost:** no same-key wrapping — only `skW` (and a second wrapper key) signs `OT_WRAPPER` frames and no issuer key ever does — which would preserve **C-C7(ii)**'s registered contrast (the quantifier gap of `d6d_sp1_q8_type_conditional_unbound.out:315` against `:507`) at the cost of C-C15(i)'s witness. **The choice changes results**, so it is taken here and not left to the builder; its consequences are carried in §4's **C-C7** row (`cap7a`, `cap7b`) and its non-consequences in §4's **C-C6** row (`cap7c`) and C-C7(i) (`cap7d`) |
| Lineage | Exactly two attempts, S-STANDING's shape, both terminal dispositions present across the fixture. **ADDITION beyond §6(4)**, which lists no lineage: required by C-Q6 under the ruled formulation W, whose inherited residual **is** the two-entry-lineage scoping (`:1294`, `:510`, and D12's transcribe column `:761`). *(Marked — skeptic 2026-09-15.)* |
| Standing path | `wrapCore`, `attemptCore`, `h(core)`, the `TLR` tag (D-6), `OT_TLR`, the lineage/terminal/declaration triple. **Not from §6(4)** but from the *“What `capstone.pv` must transcribe”* cells of D12 (`:761`), D13 (`:762`) and D11 (`:705`); carried here so the source is on the record. *(Marked — skeptic 2026-09-15.)* |
| Foreign-tag signer *(AMENDMENT 2026-09-18 — the author's ruling on §8 item 1, option (i), scoped)* | `ForeignIssuer(skI)`: the honest issuer key emits `sign((REFUSAL, body), skI)` for an adversary-chosen core, `body` a TLR-shaped triple — copied from the 2026-09-06 cross-family reviewer's fixture `s-standing/proverif/falsification-2026-09-06/scratch/a_foreign_tag.pv:339-342`, the only demonstration on record of D-6's tag check doing any work (`lib/tessera_theory.pvl:66-76`; review item 27). **What it is:** a **foreign-tag source**, so that the standing path's `TLR` tag check has something to separate. **What it is not:** the refusal record. Its body is opaque to every check while the tag check stands, and chosen TLR-shaped as the worst case for separation — under C-C18 the standing path reads its lineage and terminal fields **as a TLR's**, never as a refusal record's *(worded so — Codex round 16 finding 4)*; **nothing about A3 §A3.7.2's record, the extended atomic-entry invariant (L2-n) or E6 is modelled, claimed or exercised**, and `REFUSAL` is thereby **exercised as a signing domain and unexercised as a record**. **ADDITION beyond §6(4)** by the author's ruling; `LEDGER.md:1276`'s instruction to record `REFUSAL` as declared-and-unexercised is overridden for the capstone by that ruling and carries a dated note there. Runs in every case C-Q6 is stated for — (a), (b), (d) — and needs no compromise to run. Exercised by **C-Q10**; severed by **C-C18** |

**The four compromise cases**, each its own run, and which queries are
stated for which (`:1350-1390`, `:1408-1423`):

| Case | Fixture | Queries stated |
|---|---|---|
| **(a)**, **(b)** | strict, `skD` public / `skR` public | every query; C-Q1-strict, **including link 1b** |
| **(c)** | strict, **both** channel keys public | this is companion **C-C1**, not a correct-form run: `Accept ⟹ IssuerSigned` and link 1b registered **red**, every structural link green |
| **(d)** | degraded, sole channel public | C-Q1-degraded: **link 1b not asserted**; link 1a and links 2a, 2b, 3, 4, 5, 6a, 6b asserted exactly as in strict. The unrestricted `AcceptS ⟹ IssuerSigned` is registered **red**, the A4.6 cost (`docs/phase-0-prereg-amendment-4.md:156-171`) |

**L-07's signing-domain enumeration is exercised in the same fixture**
(`:1273-1277`, `:352-406`): `STMT_DIGEST` under an authority-channel
key; `POSS`, `BYTES`, `TLR` **and `REFUSAL`** under the **same** issuer
key; `STMT_DIRECT` recorded as declared-and-unexercised rather than
silently omitted. *(AMENDMENT 2026-09-18, the author's ruling on §8
item 1. The withdrawn wording, quoted: “`POSS`, `BYTES` and `TLR` under
the **same** issuer key; `STMT_DIRECT` and `REFUSAL` recorded as
declared-and-unexercised rather than silently omitted. See §8, routed
item 1.” `REFUSAL` is now exercised **as a signing domain only** — the
foreign-tag row above, C-Q10 and C-C18 — and unexercised as a record.)*
See §8, item 1.

## 1.2 The verifier: one acceptance path per layer

Carried in the order the families' models perform them. Step 1 is first
because A3 §A3.2's chain begins with accepted external evidence
(`docs/phase-0-prereg-amendment-3.md:110-120`). The standing path runs
**parallel to**, never sequenced behind, the envelope path: S-STANDING's
SS.Q3 prediction records that sequencing them shadows the missing check
and makes a companion unable to fail (`s-standing/PREDICTIONS.md:385-392`).

| Order | Check | Family transcribed |
|---|---|---|
| 1 | Accepted authority evidence, `checksign(ev, kCh) = (STMT_DIGEST, h(t))` (D-1) | S-P1 / first-link spike |
| 2 | Key binding: the frame's `kfp` is `fp(kX)`, and `mh = h(t)` | S-P3 |
| 3 | Set logic: the signed `t`'s required set names the slot, `fp(kX) = kfpr`, every required slot satisfied | S-P2 |
| 4 | Common content: `ota = otb`, `cva = cvb`, `pla = plb`, plus the three fields pinned through `t` | S-P2 Q6 |
| 5 | Type, opacity and recorded-version checks, and `InnerCheck` for `lyr ≠ L0` | S-P7 |
| 6 | Possession over the **accepted manifest** under the **accepting key**, `checksign(ppf, kX) = (POSS, t)` (D-3) | S-P3 / S-P2 |
| 7 | The standing path: lineage lookup on `h(attemptCore(...))`, terminal disposition, entitled-key comparison against `t`'s `kfpr`; and the **`TLR` tag check** on the lineage record's signature, `let (=TLR, …) = checksign(tlrSig, kT)` (D-6) — the check **C-C18** unbinds *(named here by the AMENDMENT of 2026-09-18)* | S-STANDING |

## 1.3 The `LayerAccepted` event, exactly as LEDGER §6 fixes it

`LEDGER.md:1315`, with correction (c) at `:2249-2273`:

```
event LayerAccepted(bitstring, bitstring, bitstring, bitstring,
                    bitstring, pkey, bitstring, bitstring, bitstring).
(* aid, lyr, t, ev, slot, kX, ppf, sg, fb *)
```

`aid` is **a fresh `new aid: bitstring`, minted once per presentation
AT INTAKE, and nothing else**: the aggregate package term does **not**
serve, because replaying one package gives distinct executions the same
term. *(REPAIR 2026-09-17, Codex round 2 finding 1. The withdrawn
wording, quoted: “**a fresh `new aid: bitstring`, minted once per
completed acceptance, and nothing else**”. It placed the mint **after**
the checks, which is what let C-Q6's (E1) read the shared name as a
certificate that the envelope path had **succeeded**. Nothing else about
`aid` changes.)*

**Where `aid` is minted** *(REPAIR 2026-09-17, Codex round 2 finding 1)*.
The fresh name is minted **at intake**, by a **front-end process that
reads the presented bundle once** and forwards it on **private channels
to the envelope path and the standing path in parallel** — §1.2's
“parallel to, never sequenced behind” and encoding rule (1) of §2.
Both `LayerAccepted` **and** `EstablishedWrapped` (§3, C-Q6 (1)) carry
**that** `aid`. **The ledger's carried-forward correction is preserved
and strengthened, not relaxed** (`LEDGER.md:2249-2273`): **one fresh name
per acceptance, shared across its slots, followed by
`AcceptanceComplete`** — and the name still cannot be duplicated by
replay, because it is `new` per **presentation** rather than derived
from the package term. What changes is only that **the name exists
before any check runs**, so a path may carry it without thereby
asserting that the other path succeeded.

**THE PER-ACCEPTANCE NAME IS THE PAIR `(aid, lyr)`, NOT `aid` ALONE**
*(REPAIR 2026-09-17, Codex round 3 finding 1)*. *The withdrawn wording,
quoted: “a bundle still yields **at most one** acceptance”.* That is
**wrong for a wrapped bundle**. A wrapped presentation is accepted once
**per layer**: each layer's acceptance closes with its own
`AcceptanceComplete(aid, lyr, t)`, so one bundle yields **one
acceptance per layer** and up to three (`L0`, `L1`, `L2`) at depth 2.
Since the round-2 repair moved the mint to **intake**, all of them
share the **one** `aid`, and §1.1's same-key wrapping with the
one-key/one-manifest assignment lets them share `t` as well. The unit
the ledger's carried-forward correction names — *one fresh name per
acceptance, shared across its slots* — is therefore the **pair
`(aid, lyr)`**: `aid` fresh per **presentation** (no replay can
duplicate it), `lyr` distinguishing the acceptances **within** one
presentation. Every construction in this file that means *"this
acceptance"* — link 2b's grouping, its permitted projection (§3, link
2b), and C-Q6's join — is read against the **pair**. **Shown:**
`cap9_sp2_slots_projection_no_lyr.out` — two layers sharing one intake
`aid` and one `t`, slot B reported at one layer only — leaves the
`aid`-only projection **`is true`** (`:1239`) while the layer-indexed
form is **`is false`** (`:1454`), with the witnesses reachable (`:675`,
`:913`, `:1162`). Nothing else about `aid` changes, and §1.3's
signature is unchanged: `lyr` was always an argument of both events.

`lyr` is the layer index (`L0` / `L1` / `L2`, depth bounded at 2);
`t` the accepted authority tuple `authTuple(id, kfpr, sset, alg, ver)`
(D-2); `ev` **the accepted evidence term** this acceptance consumed — **in strict, the PAIR of such terms, one per channel** *(REPAIR 2026-09-17, Codex round 7 finding 2; the paragraph below)*;
`slot` the signer-slot identifier, `kfpr` as the signed set names it; `kX`
the accepting key; `ppf` the accepted possession proof; `sg` the accepted
signature term; `fb` the **presented** framed bytes. Emitted **once per
signer slot**, all slots of one acceptance carrying the **same `aid`**,
the report output in parallel with its continuation. **The standing
path's `EstablishedWrapped` carries the same intake `aid` and is emitted
by that path on its own, without waiting for `LayerAccepted`** (§3,
C-Q6 (2), (E1) as repaired 2026-09-17).

**`ev` IN STRICT IS THE PAIR** *(REPAIR 2026-09-17, Codex round 7 finding 2)*.
The strict fixture has **two** authority channels and the verifier reads an
evidence term on **each**, so "the accepted evidence term" is ambiguous
exactly where C-C10's isolation control lives: with the compromised
channel's check deleted, the verifier checks one term and the acceptance
carries the other unexamined. **In strict, `ev` in `LayerAccepted` is the
pair of evidence terms the acceptance carried, one per channel; in
degraded it is the sole term.** *The withdrawn phrase, quoted: "`ev` **the
accepted evidence term** this acceptance consumed".* Its sense is not
withdrawn — this is that phrase **made exact for two channels** — and
**`LayerAccepted`'s signature is not changed**: `ev` remains one argument,
whose term in strict is a pair. **This is a CONTESTABLE contract term**, a
clerk disposition of the owner instance, open to the author at the freeze
commit: the alternative — observing only the **retained, checked** term —
is a second contract choice that does not follow from deleting the
opposite check, and it would leave C-C10's isolation control all green.
The reading registered here is the one under which **deleting either
check reds link 1a**, the right property for a binding link. **Shown, on
copies of a committed family model:** the channel-specific link-1a judge
is **green** on the strict baseline
(`cap20d_sp1_strict_base_evidence.out:589`) and **red** on both deletions
(`cap20f_sp1_strict_cc10_drop_compromised_evidence.out:737`,
`cap20g_sp1_strict_cc10_drop_honest_evidence.out:1055`). No capstone model
exists and none of these is a capstone result.

**THE REPORT CONTRACT UNDER COMPANIONS** *(REPAIR 2026-09-17, Codex
round 9 finding 1 — **this file's contract term, CONTESTABLE by the
author at the freeze commit; the FOURTH such choice**, beside same-key
wrapping, the compromised-channel-only reading of "adversary-enrolled",
and `ev` as the pair in strict)*. **Under every companion,
`LayerAccepted` and every judge report at a layer carry the terms THAT
LAYER'S ACCEPTANCE WAS ABOUT** — the **presented** `(t, ppf, sg, fb)` of
that layer, under the key the (mutated) verifier verified against — and
**never** terms checked at **another** layer. **This is already what the
immutable join requires** (`t = tI`, `ppf = ppfI`; §3, C-Q6 (3), the
term-equality column, which is immutable and which no companion
removes). It is **stated** here because it was left unspecified, and an
unspecified report is a **builder choice that changes a result**: a
builder could make a companion's failure invisible by reporting **what
the verifier did check** in place of what the acceptance was about.
**Shown, on copies of a committed family model.** C-C15(i)'s strict
transcription checks the **outer** possession proof and then verifies the
inner signature under `kW`; it never checks the presented inner `tI` or
`ppfI`. With the C-Q9 structural possession judge added and **nothing
else changed**, the inner acceptance reporting the **presented inner**
`(kW, tI, ppfI)` makes C-Q9 **red** in both channel variants
(`cap22e_sp7_strict_q6b_q9_inner.out:1334`;
`cap22f_sp7_strict_q6b_q9_inner_repo.out:1334`) while the four S-P7
queries stay green (`cap22e:569`, `:578`, `:587`, `:596`) and both
witnesses stay reachable (`:871`, `:1075`); reporting the **checked
outer** `(kW, tW, ppfW)` instead makes the same judge **green**
(`cap22g_sp7_strict_q6b_q9_outer.out:1084`) — **the rejected reading**;
and the **unchanged strict baseline**, whose acceptance reports its own
**checked** inner terms, is green
(`cap22d_sp7_strict_base_q9.out:1186`). **Why it is contestable, in one
line:** the alternative — report the terms the verifier actually
verified, whatever layer they came from — is a second contract choice
that does not follow from any mutation, and under it C-C15(i)'s C-Q9
stays green, so the two readings give **opposite colours on the same
verifier**. The reading registered here is the one under which a
companion that **stops checking** a term cannot hide that by
**reporting** a different one. **`LayerAccepted`'s signature is
unchanged** — this fixes what its existing arguments **denote** under a
mutation, exactly as the `ev`-pair paragraph above does — and **no
query, no companion, no probability and no timebox moves.** No capstone
model exists and none of these `.out` files is a capstone result.

| Event | Arguments | Emitted |
|---|---|---|
| `AuthorityEvidence` | `t`, `ev`, the channel key `ev` verified under | after the evidence check, before anything else is read (`:1314`) |
| `ScopeReported` *(DECLARED HERE — REPAIR 2026-09-17, Codex round 6 finding 1)* | `aid`, `lyr`, `kA`, `idA` — the **envelope path's own attribution report**: the key and the issuer identity that path attributes the acceptance to | on the `scopeCh` report, **in parallel with the continuation** (encoding rule (1), §2), at every layer. **It is not a new check and not a new extraction**: it is the `scopeCh` report S-P7's models already emit — the correct model's at `sp7_q2_degraded_compromised.pv:303` (`out(scopeCh, (ctx, kI, idI, fbI))`), read by `ScopeJudge` at `:351` — carried here with §1.3's per-acceptance pair `(aid, lyr)` in place of the family's `ctx`. It is declared here because **link 6b now observes it** (§3, link 6b, as repaired for round 6 finding 1) and because **C-Q6's conjunct 3 consumes it** (§3, C-Q6 (5), where it was already named at `:1146-1151` but not declared beside `LayerAccepted`) |
| `AcceptanceComplete` | `aid`, `lyr`, `t` | at the **single** acceptance point of that layer, after every `LayerAccepted` of that acceptance (`:1316`) |
| `ChainBroken` | `lyr`, the failed link's name | by the judge; the subject of links 1a, 2a, 3, 4, 5, 6a, 6b **only**. Links 1b and 2b are correspondences (`:1317`, `:2213-2247`) |
| `HonestChain` | `lyr`, `t` | the honest-flow witness; **must be reachable** (C-N1, `:1318`) |

---

# 2. Encoding rules bound from the start

So that no recut is needed to obtain them (`s-p3/RESULTS.md:38-73`,
`LEDGER.md:1264-1278`): (1) **report outputs in parallel with their
continuations**, never sequential, since a synchronous output off the
goal path blocks trace reconstruction (recut 1); (2) **per-role judges**,
because a single event cannot say "red on exactly signer B" or "exactly
layer L1", so per-slot and per-layer judge channels and events are
declared from the start (recut 2); (3) **`-lib` with the shared
library**, nothing redeclared, redeclaring a library term being a build
failure (ENUM §1); (4) **`framed` is NOT promoted**, the seven-argument
constructor copied verbatim from S-P3 as S-P1 and S-P2 copied it
(`lib/tessera_theory.pvl:77-84`), with the capstone checking the copies
agree; (5) **the D-1 `STMT_DIRECT` / `STMT_DIGEST` split**, the spike's
single `STMT` being a build failure (`:1266-1268`); (6) **D-6's `TLR` and
`REFUSAL` tags present and load-bearing under composition**, which is
precisely what the capstone is for (`lib/tessera_theory.pvl:66-76`,
`LEDGER.md:387-398`; see routed item 1); and (7) **the honest-flow witness is the
judge's `HonestAccepted(k, fb)`**, never bare acceptance (recut 3).

---

# 3. The ladder

**Outcome vocabulary, registered once and binding on every query below**
(ENUM §5): **violation** = a counterexample trace, to be classified;
**timeout** = mechanism-viability failure, evidence about the tool or the
encoding and **never** about the property, disposed by ablation or a
change of tactic; **termination** = evidence for the checked abstraction
only. **Ablation on any timeout**, in order, break point recorded: drop
the depth-2 layer, then `skI2`, then the second lineage shape, then the
`|set| = 2` branch. **Ordering:** C-Q1's links before every companion;
(a), (b), (d) before (c); C-Q7, C-Q8, C-Q9 before links 3 and 4 and
before C-Q6. **Timeboxes** are per run, each compromise case getting the
full box, and are raised above the families' 15 to 30 minutes because the
capstone's term space is the product of what the families ran separately
(seven check groups, three layers, two slots, two channels, two issuers,
a two-entry lineage, and correspondences with an acceptance-identifier
grouping no family model carried).

## C-Q1 — the linkage query (`LEDGER.md:1285`, contract `:1297-1423`)

**Two forms**, C-Q1-strict and C-Q1-degraded, same events and same
judge, differing only in link 1b and in the fixture's channel leak
(`:1386-1390`); predictions freeze separately for each: **C-Q1-strict's
frozen prediction is the nine link predictions below; C-Q1-degraded's is
the same eight excluding link 1b**, which it does not assert. **Each of
the nine links is a separate ProVerif query.** *[ADDITION beyond §6 —
skeptic 2026-09-15: `:1317` declares **one** `ChainBroken(lyr, link)`
event carrying "the name of the link that failed", which one query could
cover. Splitting it per link is this file's encoding choice, binding
from here, justified by S-P3 **recut 2** (a single event cannot say "red
on exactly layer L1") and by the per-link companions C-C9 and C-C10,
which need per-link resolution to show what they severed. It changes no
property and adds no obligation.]*

### C-Q1 link 1a — evidence → this acceptance

**Query.** The evidence term this acceptance carried is evidence over
the statement this acceptance consumed; a declared-but-unconsumed
`AuthorityEvidence` event does not discharge it, the binding being to
`aid`. `checksign(ev, kCh) = (STMT_DIGEST, h(t))` (or `(STMT_DIRECT, t)`,
D-1), **including the case where `ev` does not verify at all** (the
destructor's `else` branch); `ChainBroken(lyr, LINK_1A)` unreachable.
**Serves** D4's evidence conjunct (`:698`, `:1331`); **structural, no
producer named and none claimed**; strict **and** degraded (`:1368`);
companion **C-C10**.

**PER CHANNEL, IN STRICT** *(REPAIR 2026-09-17, Codex round 7 finding 2)*:
`ev` is §1.3's **pair**, and this query requires **each** carried term to
verify over the consumed `t` **under its own channel key** —
`checksign(ev_i, kCh_i) = (STMT_DIGEST, h(t))` (or `(STMT_DIRECT, t)`) for
**both** `i`, **including the case where a carried term does not verify at
all**. In degraded there is one term and one key and the form is
unchanged. **Basis, and the term is CONTESTABLE** (a clerk disposition of
the owner instance, open to the author at the freeze commit): the
channel-specific judge is **green** on the strict baseline
(`cap20d_sp1_strict_base_evidence.out:589`) and so is the weaker
either-key form (`cap20c_sp1_strict_base_evidence_either.out:585`), and
both are **red** on C-C10's isolation control
(`cap20f_sp1_strict_cc10_drop_compromised_evidence.out:737`;
`cap20e_sp1_strict_cc10_drop_compromised_either.out:732`), so the runs do
not separate them and the stronger is registered. What is contestable is
**which term is observed**, not which key: this is the reading under which
**deleting either channel's check reds link 1a** (`cap20f…:737` for the
compromised deletion, `cap20g_sp1_strict_cc10_drop_honest_evidence.out:1055`
for the honest one), where observing only the retained, checked term would
leave the isolation control all green. It adds **no query, no companion and
no timeboxed entry**, and this entry's prediction, probability, residual
decomposition, witnesses and 45-minute timebox are **untouched**.
**Prediction: green, p ≈ 0.8**. Basis: the mutation and its contrast are run
on a copy in the degraded fixture, `cq1a_sp1_evidence_base.out:322`
`is true` against `cq1b_sp1_evidence_unchecked.out:466` `is false`
(residual: 0.15 recut over the `else` branch and the two-key
disjunction, 0.05 timeout). **Witnesses:** `HonestChain` at `L0`, `L1`,
`L2`, and `HonestAccepted`; **timebox** 45 min.

### C-Q1 link 1b — authority → tuple (correspondence, strict only)

**Query.** Acceptance implies a prior authority-publication event for
the consumed tuple; **not a `ChainBroken` conjunct**, since a judge
cannot observe that a publication event never occurred (`:2213-2247`).
In the library's own event names (`lib/tessera_theory.pvl:190-191`):
`event(LayerAccepted(aid, lyr, t, ev, slot, kX, ppf, sg, fb)) ==> (event(AuthorityPublishedDNS(t)) || event(AuthorityPublishedRepo(t)))`.
**Serves** D4's publication conjunct; producer S-P3 Q1(ii), green
(`:1332`); **strict only**, not asserted in (d) (`:1369`); companion
**C-C1**.
**Prediction: `is true` in (a) and (b), p ≈ 0.8; `is false` in (c)**,
which is C-C1's requirement. Basis: S-P3 Q1(ii)'s committed green
(`sp3_q1_strict_dns_compromised.out:424`) and the same correspondence
shape (residual: 0.15 recut, the antecedent may need a projection to a
two-place `AcceptedTuple(aid, t)`; 0.05 timeout). **Witnesses:** as link
1a; **timebox** 45 min.

### C-Q1 link 2a — tuple → slot

**Query.** `t`'s signer set names `slot`, and `fp(kX) = slot`, read from
the **signed** tuple; `ChainBroken(lyr, LINK_2A)` unreachable.
**Serves** D7; producer S-P2 Q2 `SignerForged`, green
(`sp2_q2_degraded_compromised.out:384`; `:1333`); both modes; companion
**C-C17** *(REPAIR 2026-09-17, Codex round 5 finding 1. The withdrawn
wording, quoted: “**Serves** D7; producer S-P2 Q2 `SignerForged`, green
(`sp2_q2_degraded_compromised.out:384`; `:1333`); **both modes.**” — it
named **no companion at all**.)* **Why one was owed here.** D7 claims
discharge of **three** producers; C-C9 severs **completeness** and C-C16
severs **common content**, and **both retain link 2a and `SignerForged`**
(§4, §9(3)). Neither severs **membership** — the fact this link consumes
— so under A3.3 (`docs/phase-0-prereg-amendment-3.md:220-230`) the query
consuming the severed link had no companion failing it. **C-C17**,
registered in §9(4), is that companion: S-P2 Q4 transcribed, slot B's
key-fingerprint equality removed on the two-signer branch, everything
else retained — which reds the slot-to-key judge
(`cap13b_sp2_membership_unbound.out:1972` against the matched baseline
`cap13a_sp2_membership_base.out:1206`) and **`SignerForged`** (`:730`)
while all three of link 2b's completeness conjuncts stay `is true`
(`:1685`, `:1722`, `:1759`).
**Prediction: green, p ≈ 0.8**. Basis: committed producer, direct per-slot
pattern match (residual: 0.15 recut, 0.05 timeout). **Witnesses:** both
`HonestComplete` and `HonestChain` at every layer; **timebox** 45 min.

### C-Q1 link 2b — required set → completeness (correspondence)

**Query.** A `LayerAccepted` record for **every** required slot of `t`,
grouped under the same `aid`. Per-slot membership does not imply it:
every reported slot can belong to the manifest and match its key while a
required slot has no report at all. One conjunct per required-set shape
(`:1334`): for `signers0`,
`event(AcceptanceComplete(aid, lyr, authTuple(id, fpA, signers0, alg, ver))) ==> event(LayerAccepted(aid, lyr, …, fpA, …))`;
for `signers1(fpB)`, **both** the `fpA` and the `fpB` conjunct. The
capstone may project `LayerAccepted` to
**`SlotSatisfied(aid, lyr, t, slot)`** for the antecedent's sake —
**the projection RETAINS THE LAYER** *(REPAIR 2026-09-17, Codex round 3
finding 1; the withdrawn wording, quoted: “The capstone may project
`LayerAccepted` to `SlotSatisfied(aid, t, slot)` for the antecedent's
sake.”)*. **Why the layer cannot be dropped.** Since the round-2 repair
mints `aid` **at intake** (§1.3), every layer of one presentation
carries the **same** `aid`; §1.1's same-key wrapping and the
one-key/one-manifest assignment let the wrapper layer and the inner
layer be accepted over the **same** tuple `t` as well — `skI` wraps its
own attestation, so the same issuer key, the same manifest `M2` and the
same required set appear at both layers. Under an `aid`-only
projection a slot report emitted at **another layer** of the same
presentation therefore satisfies the correspondence's antecedent, and
the query stays `is true` with a required slot **unreported at the
layer that completed**. **Shown:**
`cap9_sp2_slots_projection_no_lyr.out`, two layers sharing one intake
`aid` and one `t` with slot B reported at `L1` only — the projected
form without `lyr` is **`is true`** (`:1239`) while the otherwise
identical layer-indexed form is **`is false`** (`:1454`), every S-P2
query and the three original conjuncts unchanged, witnesses reachable
(`:675`, `:913`, `:1162`). Intake freshness excludes **replay** mixing;
only `lyr` excludes **layer** mixing within one presentation. The three
conjuncts above are unchanged in every other respect, and
`AcceptanceComplete(aid, lyr, t)` already carried `lyr`. **Serves** D7;
producer S-P2 Q2 `Stripped`, green; both modes; companion **C-C9**.
**Prediction: all three conjuncts `is true`, p ≈ 0.55**. Basis: the lowest
number on the ladder, for encoding reasons, not doubt about the
property. The three conjuncts are `is true` on a copy
(`cq1c_sp2_slots_base.out:1161`, `:1175`, `:1189`), but that copy is a
single-family fixture with one acceptance point, while the capstone
groups slot reports across three layers and four cases under a
per-acceptance fresh name (residual: 0.35 recut, the `SlotSatisfied`
projection or an `AcceptanceComplete` arity change; 0.10 timeout,
concentrated here because a correspondence with a fresh-name antecedent
is the most expensive shape in the model). **Witnesses:** both
`HonestComplete` and `HonestAccepted`; **timebox** 60 min.

### C-Q1 link 3 — slot → possession

**Query.** `checksign(ppf, kX) = (POSS, t)`, possession over the
**accepted manifest** under the **accepting key** (D-3);
`ChainBroken(lyr, LINK_3)` unreachable. **Serves** D4, D7, D10.
**Producer: NONE today; it is C-Q9**, which the capstone registers
(`:1335`); both modes; companions **C-C3**, **C-C8**.
**Prediction: green, p ≈ 0.8**. Basis: C-Q9's feasibility run is green
(`d10a_sp2_q9_base.out:1111`) and red under the manifest unbinding
(`d10b…:1462`) (residual: 0.15 recut, 0.05 timeout). **Witnesses:** both
`HonestComplete` and `HonestAccepted`; **timebox** 45 min.

### C-Q1 link 4 — possession → signing

**Query.** `checksign(sg, kX) = (BYTES, fb)` over the **presented**
`fb`, for **every** accepted triple including one whose signature does
not verify at all; it says nothing about who produced the signature
(`:2165-2211`); `ChainBroken(lyr, LINK_4)` unreachable. **Serves** D6.
**Producer: NONE today; it is C-Q8 as rewritten** (`:1336`); both modes;
companions **C-C5**, **C-C7**.
**Prediction: green, p ≈ 0.75**. Basis: C-Q8 is green on the committed S-P1
verifier (`d6c_sp1_q8_judge_all.out:284`) and red under both C-C7
configurations; lower than link 3 because the structural form must fire
on the destructor's failure branch at every layer including `InnerCheck`,
which no committed model does (residual: 0.2 recut, 0.05 timeout).
**Witnesses:** `HonestAccepted`, `HonestWrappedAccepted`, `HonestChain`;
**timebox** 45 min.

### C-Q1 link 5 — signing → bytes

**Query.** `fb = framed(ot, alg, id, fp(kX), h(t), cv, pl)`: the frame's
fourth field is the accepting key's fingerprint and its fifth the
accepted tuple's hash; and for `|set| = 2` the six non-fingerprint
fields agree across slots, by the §A5.4 guards `ota = otb`, `cva = cvb`,
`pla = plb` with `=alg`, `=id` and `mh = h(t)` pinned through `t`
(L-09's shared-term mapping); `ChainBroken(lyr, LINK_5)` unreachable.
**Serves** D1, D2, D7. **Two halves, two producers** (`:1337`):
cross-slot agreement is S-P2 Q2 + Q6 `Spliced`, green; frame-to-key is
L-01's key binding, whose producer S-P3 Q2 `Reattributed` **is this
link's producer under the ruled Reading B**. Both modes; companions
**C-C2**, **C-C4**, **C-C8**, and **C-C16** for the common-content half.
**This link's common-content conjunct — the three §A5.4 guards `ota =
otb`, `cva = cvb`, `pla = plb` — is D7's common-content consumer**
*(REPAIR 2026-09-16, Codex finding 1)*: links 2a and 2b establish
per-slot membership and required-set completeness and say nothing about
agreement between the signers' content, so `Spliced`'s fact is consumed
**here** and nowhere else. A red on this link's **frame-to-key** half
does not discharge that obligation; A3.3 requires failure of the query
consuming the **severed** link (`docs/phase-0-prereg-amendment-3.md:220-230`),
and the severing companion for the content half is **C-C16** (§9(3)).
**Prediction: green, p ≈ 0.65**. Basis: the two halves are separately
committed green (`base_sp2.out:397`, `base_sp2.out:1013`), but this is the one
link where two families' pins compose into a single conjunct across
three layers and two slots, and the ledger's own single-removal matrix
shows the binding is defended by two independent routes whose
interaction under composition no run has observed (`:198-238`)
(residual: 0.25 recut, most likely splitting the conjunct into a
frame-to-key query and a cross-slot query; 0.05 a genuine violation;
0.05 timeout). **Witnesses:** both `HonestComplete`,
`HonestWrappedAccepted`, `HonestAccepted`; **timebox** 60 min.

### C-Q1 link 6a — bytes → layer TYPE

**Query.** `ot` is the object type this layer was processed *as* (D-5's
`OT_*` constants); `ChainBroken(lyr, LINK_6A)` unreachable. **Serves**
D8; producer S-P7 Q2/Q1 `TypeConfused`, green
(`sp7_q2_degraded_compromised.out:527`; `:1338`); both modes; companion
**C-C13** (§9).
**Prediction: green, p ≈ 0.85**. Basis: committed producer, direct pattern
match, no composition interaction known (residual: 0.1 recut, 0.05
timeout). **Witnesses:** `HonestWrappedAccepted`, `HonestChain(L1, t)`,
`HonestChain(L2, t)`; **timebox** 45 min.

### C-Q1 link 6b — bytes → innermost-issuer SCOPE

**Query** *(RESTATED IN PLACE — REPAIR 2026-09-17, Codex round 6
finding 1)*. For `lyr ≠ L0`, the **envelope path's own attribution
report** `ScopeReported(aid, lyr, kA, idA)` (§1.3) names the
**innermost frame's** `(fp(kX), id)`: `kA` is the key the innermost
frame's `kfp` field is the fingerprint of — the accepting key at that
layer — and `idA` is the innermost frame's issuer identity, not the
wrapper's. `ChainBroken(lyr, LINK_6B)` fires when it is not, and is
registered **unreachable**. This is **S-P7's `Rescoped` shape
transcribed unconditionally, per layer**: the relation `Rescoped`
observes in S-P7's models, asserted at **every** layer `lyr ≠ L0`,
with no conditional consumer and no second path.

*The withdrawn query sentence, quoted: “For `lyr ≠ L0`, the inner
frame's `(issuerId, kfp)` is the innermost issuance identity, not the
wrapper's; `ChainBroken(lyr, LINK_6B)` unreachable.”* **Why it was
withdrawn, and the run that shows it.** As written, the link observed
the **inner frame's own fields**, and a judge of exactly that shape —
frame identity against the inner tuple's identity, frame fingerprint
against the accepting key — is **green on the strict baseline**
(`cap19c_sp7_strict_frame_judge_base.out:587`) **and still green on the
Q6a mutant** (`cap19d_sp7_strict_frame_judge_q6a.out:585`), while that
mutant's `Rescoped` is **red** (`:933`) and both honest witnesses stay
reachable (`:1226`, `:1435`). Q6a leaves the inner frame and every one
of its checks intact and changes only what the envelope path
**attributes** the acceptance to (`cap14d_sp7_q1_strict_q6a.pv:235-245`,
the `scopeCh` output at `:244`, `idW` in place of `idI`). The withdrawn
form therefore could not see the very mutation **C-C15(iii)** is
registered to red against this link.

**THIS IS NOT C-Q6's CONJUNCT 3, AND THE DIFFERENCE IS THE POINT.**
Link 6b compares the **envelope path's own** report against the
**envelope path's own** innermost frame: **one path, no join**, asserted
**unconditionally** wherever `lyr ≠ L0`, in both modes, and that is the
unconditional discharge D11 requires (`LEDGER.md:705`). C-Q6's conjunct
3 (§3, C-Q6 (5)) compares that same envelope report against the
**standing path's** independently extracted `(kX, id)` — a **two-path
join**, stated only where a standing verdict exists and **conditional on
C-Q6 terminating**. Neither can stand in for the other: conjunct 3's
conditionality is exactly why it cannot supply link 6b's unconditional
claim, and link 6b's single-path form is why it says nothing about
agreement between the two paths.

**A separate property from
6a**, shown separate by S-P7's own Q6b companion: `TypeConfused` stays
`is true` (`sp7_q6b_companion_key_outermost.out:489`) while `Rescoped`
goes `is false` (`:769`). **Serves D11 unconditionally**, under every
R-3 formulation; producer S-P7 Q2/Q5 `Rescoped` / `RescopedD1` /
`RescopedD2`, green (`:1339`, `:705`); both modes; companions **C-C4** (D2's, which
reds 6b as one of its five) and **C-C15** (D11's own, §9).
**Prediction: green, p ≈ 0.8**. Basis: committed producer at both depths
(residual: 0.15 recut, the depth-2 case needs `RescopedD2`'s per-depth
judge; 0.05 timeout). **Witnesses:** `HonestWrappedAccepted`,
`HonestChain(L1, t)`, `HonestChain(L2, t)`; **timebox** 45 min.

## C-Q2 — the §A3.2.1 boundary judge (`LEDGER.md:1286`)

**Query.** Two authority-distinct manifests are never supportable by the
same evidence **pair** (pair form only, per L-24; the single-evidence
form is Addendum 1's and is not implied). `STMT_DIGEST` (D-1),
`authTuple` (D-2), `h`, a two-worlds private-channel judge over the
pair; `TwoWorldsBroken` unreachable. **Serves** D9; producer first-link
Q4 both variants, green (`q4_attack_dns_compromised.out:97`,
`q4_attack_repo_compromised.out:97`); strict, (a) and (b); companion
**C-C14** — the first-link Q2 broken companion transcribed, numbered and
specified in §9.
**Prediction: green, p ≈ 0.65**. Basis: the spike's Q4 is green in both
variants, but the spike's judge ran over a bare first-link fixture,
where in the capstone it runs over a verifier that also performs set
logic, wrapper processing and standing assessment, and the two-worlds
judge is the query the spike itself found most sensitive to fixture
shape (residual: 0.25 recut; 0.05 a genuine violation, an A3.2.1
amendment trigger rather than a recut; 0.05 timeout). **Witnesses:**
`HonestChain(L0, t)`, `HonestAccepted`; **timebox** 45 min.

## C-Q3 — the multi-signer key-binding judge (`LEDGER.md:1287`)

**Query.** S-P2's carried `Reattributed` over the capstone's two-signer
set fixture: honest framed bytes are never accepted under a key other
than their signer's. Per-role (`ReattributedA` / `ReattributedB`, recut
2), unreachable. **Serves D1**, a matrix row under the ruling; all four
cases; companion **C-C2**.
**Prediction: green, p ≈ 0.8**. Basis: committed green in all eight S-P2
models (`base_sp2.out:397`) (residual: 0.15 recut, 0.05 timeout).
**Witnesses:** both `HonestComplete` and `HonestAccepted`; **timebox**
45 min.

## C-Q4 — the wrapped-attribution judges (`LEDGER.md:1288`)

**Query.** Two judges over a fixture carrying both an issuer key and a
wrapper key: `Rescoped` (attribution and standing bind to the innermost
issuance identity) and `InnerSigTransplanted` (the honest inner
signature term is never **accepted** under another key); both
unreachable, at depths 1 and 2; `wrap()`, `InnerCheck`, `OT_ATTEST` /
`OT_WRAPPER`, `dsks`. **Serves D2** (`Rescoped`) and **D5**
(`InnerSigTransplanted`); all four cases; companions **C-C4** (whose set
reds three queries by design) and **C-C5**.
**Prediction: both green, p ≈ 0.75**. Basis: committed green in S-P7
(`base_sp7.out:540`, `:553`); the reduction is for the composed fixture,
where the wrapper path now also carries S-P2's set logic (residual: 0.2
recut, 0.05 timeout). **Witnesses:** `HonestWrappedAccepted`,
`HonestAccepted`; **timebox** 60 min.

## C-Q5 — `SetAltered` (`LEDGER.md:1292`)

**Query.** No honest key is reported as a signer of a manifest it never
signed (S-P2's `MemberJudge` shape); `SetAltered` unreachable.
**Serves** D10; the producer of what D10's consumer needs is **C-Q9**;
all four cases; companions **C-C3**, **C-C8**.

**The inherited fixture restriction, stated** *(REPAIR 2026-09-16, Codex
finding 5; the draft named the judge and omitted the restriction the
judge needs).* `MemberJudge` pairs an **observed honest** `(key,
manifest)` report with a slot report and fires `SetAltered` when the
**same** honest key satisfies a slot of a **different** tuple. It
therefore detects *"accepted under a manifest other than one this key
was observed signing"*, **not** *"accepted under a manifest this key
never signed"*. The two coincide only when **each honest key signs
exactly one manifest**. That is **S-P2's registered restriction**
(`s-p2/PREDICTIONS.md:201-214`: *"Each honest signer's key is bound to
exactly one manifest; it signs possession over that manifest only"*;
`s-p2/RESULTS.md:444-447`, which records the reviewer's `a_key_reuse`
false positive and states the rule **ONE KEY, ONE MANIFEST** in Q2's
claim (3)). **The capstone inherits it and its key assignment is named
in §1.1**: `skI` → slot A of `M2`, `skB2` → slot B of `M2`, `skI2` →
the sole slot of `M1`, and no key signs two manifests.

**The choice, and why it was taken.** The alternative the review left
open was to **register a provenance correspondence** in `MemberJudge`'s
place — an `HonestSignedManifest(k, m)` producer event and a
correspondence `SlotSatisfied(aid, lyr, t, fp(k)) ⟹
HonestSignedManifest(k, t)` *(the projection's arity follows link 2b's,
repaired 2026-09-17, Codex round 3 finding 1; this alternative is still
**not taken**)*, which would detect the real relation without any fixture
restriction. **This file takes the restriction, not the
correspondence**, for one reason: **C-Q5 is `LEDGER.md:1292`'s query,
"S-P2's `MemberJudge` shape", and S-P2 is the family whose restriction
it is.** Replacing the judge with a correspondence would register a
query the ledger did not name, retire `SetAltered` as D10's consumer,
and orphan C-C3's and C-C8's descent, which is cited against
`SetAltered` `.out` lines throughout §4. The cost is recorded, not
hidden: **C-Q5's green is conditional on the §1.1 key assignment**, and
a capstone fixture that shares a key across manifests reds C-Q5 with no
verifier change whatever.

**Shown by scratch run** (`ledger-tests-2026-09-14/cap4_sp2_shared_slotA_key.pv/.out`,
a copy of `d10a_sp2_q9_base.pv` in which **the fixture alone** is
mutated — `M2`'s slot-A key re-keyed from `skA2` to `skA1`, the key
that already signs `M1`, with **every verifier check, judge and query
untouched**): **`SetAltered` `is false`** (`:640`) — reachable — while
`Stripped` (`:455`), `SignerForged` (`:462`), `Reattributed` (`:647`),
`Spliced` (`:1260`), `PossessionTransplanted` (`:1267`) and **C-Q9**
(`:1274`) all stay `is true` and both `HonestComplete` witnesses
(`:810`, `:1026`) and `HonestAccepted` (`:1253`) stay reachable. Key
reuse alone, with no check removed, turns D10's consumer red. This
reproduces the reviewer's `/tmp` diagnostic on our own tree.
**Prediction: green, p ≈ 0.8**. Basis: committed green in the surviving-route
configurations (`sp2_q5_c1_fponly_frame_mh.out:366`), red only under the
two-removal C2 shape (residual: 0.15 recut, 0.05 timeout).
**Witnesses:** C-Q5w; **timebox** 45 min.

## C-Q5w — the honest-flow witness for C-Q5 (`LEDGER.md:1293`)

**Query.** `HonestComplete` over each set size, reachable in the correct
model **and in both isolation configurations** (either pin alone), so
that C-C3's red is a severing and not a broken fixture.
**Prediction: reachable, p ≈ 0.85**. Basis: committed reachable in all three
C1/C2/C3 configurations (`…c1….out:536`, `:756`, `:987`;
`…c3….out:534`, `:753`, `:983`) (residual: 0.1 recut, 0.05 timeout).
**Timebox** 30 min.

## C-Q6 — the wrapped-standing composition, formulation W (`LEDGER.md:1294`)

**Query, in formulation W, the conclusion being a standing verdict:**
*"an `ESTABLISHED` report computed over a **wrapped** presentation
implies the **innermost** issuer designated the reported identity, and
the key it is computed against is the one the evidenced tuple names."*
S-P7's wrapper processing (`wrap()`, `InnerCheck`, depth ≤ 2) feeding
S-STANDING's standing assessment (`wrapCore`, `attemptCore`, `h(core)`,
the `TLR` tag, the lineage/terminal/declaration triple, `authTuple`'s
`kfpr` field, `fp`). **Three conjuncts** *(REPAIR 2026-09-17, Codex
round 3 finding 2; the withdrawn wording, quoted: “**Two conjuncts:**
`EstablishedWrapped ⟹ Designated`, and `StandingUnentitled`
unreachable.”)*: `EstablishedWrapped ⟹ Designated`;
`StandingUnentitled` unreachable; and **scope agreement**,
`ScopeMisreported` unreachable (§(5), conjunct 3, an **ADDITION beyond
`LEDGER.md:1294`**). **Serves D12 and D13** (§2(c), `:759-762`) through
conjuncts 1 and 2, and **D11's conditional second half through conjunct
3**, which is the only conjunct that observes the envelope path's
**attribution** and therefore the only one a scope mutation can red. **Formulation N, which
stops at the attributed identity and consumes neither, is not built.**
Strict (a) and (b); **in degraded (d), conjunct 1's HONEST-KEY forms,
conjunct 2 and conjunct 3 are all asserted, and only conjunct 1's
UNRESTRICTED form is not** *(REPAIR 2026-09-17, skeptic read S-2. The
withdrawn phrase, quoted: “degraded (d) for the entitled-key conjunct
only”. It predates the round-3 repair that added conjunct 3 and the
round-5/6 repairs that wrote the companion cells against §(5).
**§(5) governs**: conjunct 1's honest-key forms are registered **green**
in (a), (b) and (d); conjunct 2 is registered **unreachable** in (a),
(b) and (d); and conjunct 3 is registered **unreachable** in (a), (b)
and (d), “the same mode coverage as conjunct 2”. C-C11's Cases cell
(§9(1)) already reads that way — “in (d) C-Q6's standing conjunct is
asserted only in its **honest-key** forms (§3, §(5))” — and so does §3's
timebox note, as repaired below. **No mode, query, probability or
timebox moves**; this sentence is brought forward to what §(5) already
registers)*, since S-STANDING's own unrestricted correspondence is
registered red in degraded mode (L-18, `:534`: Q1d (i) `ss_q1d_degraded_compromised.out:640`
`is false`, the A4.6 cost, while (ii) `:649`/`:658` and (iii) `:664` stay
`is true`); companions **C-C11**, **C-C12**, and **C-C15** for D11's
conditional second half (§9). *[ADDITION beyond §6 —
skeptic 2026-09-15: `:1294` fixes C-Q6's formulation and its consumed
rows but states **no modes** for it. The mode assignment above is this
file's, justified by L-18's registered degraded cost; it is registered
here so a builder does not read it as the ledger's.]*

### C-Q6's composition join, written out

*REPAIR 2026-09-16, Codex finding 4. The draft gave the two conjuncts
and no event signature, no emission contract and no shared terms, so
independently valid wrapper attribution for artifact **A** and
independently valid standing evidence for artifact **B** would have
satisfied both family checks and the composition query with them.
Naming the standing event `EstablishedWrapped` supplies no binding.
**D11's conditional half and D12's and D13's consumption are frozen
only with the contract below**; until it stood, they were not
builder-ready. Nothing here changes C-Q6's formulation, its modes, its
probability or its timebox.*

**(1) The event signature.** Argument names are taken from the shared
library and from LEDGER §6's own `LayerAccepted` contract (`:1315`)
wherever those fix a name, and from S-STANDING's own parameter names
where the library fixes none; this is said so the builder does not read
the review brief's names as the library's.

```
event EstablishedWrapped(bitstring, bitstring, bitstring, pkey,
                         bitstring, bitstring).
(* aid, lyr, t, kX, core, verdict *)
```

- **`aid`** — the capstone's **fresh acceptance identifier** (§1.3),
  `new aid: bitstring`, minted once per completed acceptance. **It is
  NOT S-STANDING's `aid`.** S-STANDING calls its *derived attempt
  identity* `aid` too (`ss_q1_strict_dns_compromised.pv:359`, `let aid =
  h(core)`), and the two must not be confused: the derived identity is
  `h(core)` and appears **in the conclusion**, never as an argument.
  *(This collision of names is recorded here because it is the first
  place in the suite where both meanings appear in one sentence.)*
- **`lyr`** — the layer index (`L0` / `L1` / `L2`), as `LayerAccepted`
  carries it. For C-Q6 it is the **innermost** layer of the wrapped
  presentation and is `≠ L0` by the emission contract.
- **`t`** — the evidenced authority tuple `authTuple(id, kfpr, sset,
  alg, ver)` (D-2), the one **the innermost acceptance accepted**.
- **`kX`** — the accepting key, `LayerAccepted`'s own name for it. For
  C-Q6 it is the **innermost accepting key**: the `kI` of S-P7's
  `InnerCheck`, not the wrapper's `kW`. *(The review brief called this
  argument `kInner`; the name in this file is `kX`, because that is
  `:1315`'s name for the accepting key and the join's whole point is
  that it is the **same** argument.)*
- **`core`** — S-STANDING's own parameter name (`ss_q1…:352-353`) for the
  term the identity is derived from; here required to be an
  `attemptCore(...)` term, never a `wrapCore(...)` one.
- **`verdict`** — the standing report's verdict constant,
  `ESTABLISHED` / `ABSENT` / `UNVERIFIABLE` (S-STANDING's report
  vocabulary). *(The brief called this `standingValue`.)*

**C-Q6's three judge events, declared here so they are in one place**
*(the two scope-agreement events added by the REPAIR of 2026-09-17,
Codex round 3 finding 2)*: `StandingUnentitledWrapped(pkey, bitstring)`
over *(key the report was computed against, evidenced tuple)*, §(5)
conjunct 2;
**`ScopeMisreported(bitstring, bitstring, pkey, bitstring, pkey, bitstring)`**
over *(`aid`, `lyr`, the standing path's reported key `kX` **and reported
innermost issuer identity `id`**, the envelope path's attributed key `kA`
**and attributed identity `idA`**)*, §(5) conjunct 3 — **six places, the
pair form** *(REPAIR 2026-09-17, Codex round 4 finding 1; the withdrawn
declaration, quoted: “**`ScopeMisreported(bitstring, bitstring, pkey,
pkey)`** over *(`aid`, `lyr`, the standing path's reported key `kX`, the
envelope path's attributed key `kA`)*”, which compared the **key only**
and could not see an identity-only re-scoping)*; and its witness
**`HonestWrappedStandingAgreed(bitstring, bitstring)`** over
*(`aid`, `lyr`)*. All three are **judge** events on private channels,
never verifier checks, in S-P7's house form
(`sp7_q2_degraded_compromised.pv:349-353`, `ScopeJudge`).

**TWO ISOLATION OBSERVERS, DECLARED HERE SO THE BUILDER DOES NOT INVENT
THEM** *(REPAIR 2026-09-17, skeptic read S-10 — **a clerk decision of
the owner instance**, not an author ruling, and contestable at the
freeze commit like every other clerk disposition in this file)*.
**C-C15(iii)**, the isolation configuration of §9(1), requires conjunct
3's **identity** comparison to fire and its **key** comparison not to,
in **one** configuration. Under the single pair-form judge above those
are the **same query**, and the sets as they stood required it red and
green at once. The capstone therefore declares **ONE registered pair
judge**, `ScopeMisreported`, which **is** conjunct 3, **and TWO
observers beside it**:

```
event ScopeKeyOnly(bitstring, bitstring, pkey, pkey).
(* aid, lyr, kX, kA — fires on kA <> kX alone *)
event ScopeIdentityOnly(bitstring, bitstring, bitstring, bitstring).
(* aid, lyr, id, idA — fires on idA <> id alone *)
```

Both are fired by the **same** judge, from the **same** two reports,
each **on its own half's inequality alone**. Neither adds a verifier
check, a report, an extraction or any synchronisation between the paths,
and neither changes what `ScopeMisreported` does.

**Their status, stated exactly, because it is what keeps them from
becoming evidence.** They are **observers, not queries**. They are
**queried only in the isolation configurations that name them** — as of
this registration, **C-C15(iii)** alone. They are **never counted among
the 27 separately timeboxed entries** *(26 before the 2026-09-18 amendment)* and are **never timeboxed on their
own**: they run inside link 6b's 45-minute and C-Q6's 90-minute boxes,
exactly as configuration (iii) itself does. And **no discharge of any
matrix row ever rests on either of them**: a colour from an observer is
a **diagnosis of which comparison fired**, never a result about D11,
whose **C-Q6 half**'s consumer is conjunct 3; D11's **unconditional**
consumer is **C-Q1 link 6b**, which no observer touches *(REPAIR
2026-09-17, Codex round 13 finding 1. **The withdrawn phrase, quoted:**
“whose consumer is conjunct 3 and nothing else”. **What was wrong:** it
narrowed D11 to **one** of its **two** consumers. §5's D11 row names both
— the unconditional C-Q1 link 6b and, for the conditional half, C-Q6's
conjunct 3 (`:1906`) — and §3 states at length why conjunct 3, being
conditional on C-Q6 terminating and a two-path join, **cannot** stand in
for link 6b's unconditional single-path claim (`:563-574`). **What the
sentence was for is unchanged:** an observer's colour is never a result
about D11 under **either** consumer)*. **This is the shape the
diagnostics already used** — `KeyOnlyScopeWrong` and `ScopeIdentityWrong`
in the `cap12e` / `cap12f` / `cap12g` / `cap15d` / `cap16a` family
copies — registered here under the capstone's own names so the builder
transcribes it rather than inventing it, and so that no cell of this
file descends a capstone green on an event the capstone does not
declare. **And the shape is now DESCENDED at the reviewer's projection**
*(REPAIR 2026-09-17, Codex round 13 — the observers confirmed; an
addition, nothing withdrawn)*: with these two declarations transcribed
beside the six-place pair judge onto the pair-judge copies, the
**correct control** leaves the pair judge and **both** observers
unreachable (`cap26b_ss_q1_pairjudge_correct_observers.out:576`, `:583`,
`:590`), an **identity-only** scope mutation fires the pair judge and
the **identity** observer alone (`cap26c…:959`, `:1334`, the key
observer green at `:1341`), and a **key-only** scope mutation fires the
pair judge and the **key** observer alone (`cap26d…:955`, `:1340`, the
identity observer green at `:963`) — witnesses reachable in all three.
Each observer fires on exactly its own half, which is what
**C-C15(iii)** requires of them. These are **family-copy** runs
(seventeenth batch), **not** capstone results and **not** S-STANDING
results.

**(2) The emission contract.** `EstablishedWrapped` is emitted **by the
standing path only**, at the point where S-STANDING's `StandingDecide`
emits `Established(kT, t, aid)` (`ss_q1…:333`), **in parallel** with the
existing report outputs (encoding rule (1), never sequenced), and
**only** when, in the same execution — **(E1)–(E4); (E5) was
withdrawn from the contract on 2026-09-17 and is kept below, marked withdrawn, so
the withdrawal is not silent**:

- **(E1) Same PRESENTATION** *(REPAIR 2026-09-17, Codex round 2
  finding 1; restated from “Same acceptance”)*. The standing path
  computes over the innermost `(t, ppf, sg, fb)` that **it extracts
  structurally, itself, from the same bundle** the front-end forwarded
  to it — S-P7's `wrap()` destructuring of the wrapper's payload field
  (`sp7_q2_degraded_compromised.pv:317-334`), performed on the standing
  path's own copy — under the **same intake `aid`** (§1.3). It
  **neither waits for nor is conditioned on `LayerAccepted`**: no event
  of the envelope path, and no success of it, is a precondition of
  `EstablishedWrapped`. The binding is the shared **intake** name plus
  the **structural** extraction, and that is what excludes the
  artifact-A / artifact-B substitution of §(4).

  *The withdrawn wording, quoted: “**(E1) Same acceptance.** `event
  LayerAccepted(aid, lyr, t, ev, slot, kX, ppf, sg, fb)` has fired for
  the **innermost layer of that same acceptance** — the same fresh
  `aid`, the same `lyr`, the same `t`, the same `kX`, the same `ppf`,
  the same `sg`, the same `fb`. The standing path is computed over
  **that** presentation, not over a presentation the presenter supplies
  beside it.”* **Why it is withdrawn.** It made envelope **success** a
  necessary condition of the standing report. That is the sequencing
  S-STANDING's own SS.Q3 prediction named as its **p ≈ 0.2** branch —
  *“the model's verifier sequentializes the envelope path before the
  standing path so the envelope's fingerprint check shadows the missing
  one”* (`s-standing/PREDICTIONS.md:385-392`) — and which §1.2 and
  encoding rule (1) forbid. E1 did the sequencing **by event dependency
  instead of by process order**, which the rule forbids just as much:
  running the two paths in parallel does not preserve orthogonality if
  the queried event requires the other path's success. **Shown,
  family-locally:** adding to the committed C-C12 source **only** the
  guard E1's necessary condition imposes (`if fp(kX) = kfpr` before the
  standing report) makes `StandingUnentitled` **unreachable**
  (`cap5b_ss_q3_e1_projection.out:476`) and the unrestricted
  correspondence **`is true`** (`:449`), with honest standing still
  reachable (`:773`), where the unguarded baseline has them
  **reachable** (`cap5a_ss_q3_companionB_asis.out:860`) and
  **`is false`** (`:628`). **C-C12 could not fail**, and the companion
  the A3.3 gate requires would have been vacuous.
- **(E2) Same core, built from the acceptance's own terms.**
  `core = attemptCore(t, ppf, sg, decl)` for exactly the `t`, `ppf` and
  `sg` of (E1), with `decl` the declared time. The `=t` pin is
  S-STANDING's own Amendment 5 §A5.6 tuple pin
  (`ss_q1…:382`, `let attemptCore(=t, ppfS, sgS, declS) = core`),
  extended here to the possession proof and the signature term.
- **(E3) Derived identity.** The reported identity is `h(core)` —
  derived by the verifier, never read from the bundle
  (`ss_q1…:359`). It is not an argument of the event; it is written
  `h(core)` in the correspondence's conclusion.
- **(E4) Wrapped.** `lyr ≠ L0`; at depth 2 the innermost layer is
  `L2`. A base-path acceptance emits `Established`, not
  `EstablishedWrapped`. *(REPAIR 2026-09-17, Codex round 2 finding 1:
  the wrapped flag is the **front-end's structural parse of the outer
  frame** — an `OT_WRAPPER` frame whose payload field is a `wrap()`
  term — and **not** a fact derived from any acceptance. The standing
  path reads it from the bundle it was handed, as it reads
  `(t, ppf, sg, fb)` under (E1).)*
- **(E5) — WITHDRAWN AS AN EMISSION PRECONDITION and MOVED into the
  correct verifier's checks** *(REPAIR 2026-09-17, Codex round 2
  finding 1)*. *The withdrawn text, quoted: “**(E5) Entitled key inside
  the standing path.** `fp(kX) = kfpr` for `t`'s fingerprint field, and
  the TLR key `kT = kX` (`ss_q1…:366`, `:368`).”* Those two
  equalities are **check 7 of §1.2** — the correct verifier's own
  entitled-key comparison (`ss_q1_strict_dns_compromised.pv:366`,
  `:368`). **C-C12 removes `fp(kT) = kfpr` ONLY, and RETAINS `kT = kX`**
  *(REPAIR 2026-09-17, Codex round 3 finding 3; the withdrawn wording,
  quoted: “and they are **exactly the check C-C12 removes**”, which
  named **both** equalities as the mutation's boundary and so
  mis-stated what the companion does)*. The companion's own source says
  so: `ss_q3_companionB_entitled_via_envelope.pv:259-265` carries the
  mutation comment *“NO `fp(kT) = kfpr` check in the standing path …
  the entitled-key determination is left to the envelope path”* and
  keeps `if kT = kX then` immediately below it (at **`:263`**). So
  `kT = kX` — the TLR key equals the key the report is computed against
  — **survives the companion** and is not what it severs; only the
  tuple-fingerprint comparison is. As an
  **emission precondition** they shadow the companion: a standing path
  that cannot report unless the key is entitled can never report an
  unentitled key, so `StandingUnentitledWrapped` would be unreachable in
  the **broken** model as well as the correct one and **D13's severing
  test would not exist**. Shown: `cap5b_ss_q3_e1_projection.out:476`
  (unreachable, `:449` `is true`) against
  `cap5a_ss_q3_companionB_asis.out:860` (reachable, `:628` `is false`) —
  the same projection that condemns E1, since E1's necessary condition
  **is** this check. They therefore appear **only** as checks of the
  correct verifier, where C-C12 can delete them, and **never** in the
  emission contract.

**(3) The representation mapping — how S-P7's `(fbI, sgI)` becomes
S-STANDING's `attemptCore(t, ppf, sg, decl)`.** This is the join the
draft left unwritten. S-P7 extracts the inner pair **by destructuring
the wrapper's payload field**:

```
let framed(=OT_WRAPPER, =algW, =idW, =fp(kW), mhW, cvW,
           wrap(cvIw, (fbI, sgI))) = fbW in
```

(`sp7_q2_degraded_compromised.pv:317-334`), and `InnerCheck` then
requires `checksign(sgI, kI) = (BYTES, fbI)` and
`framed(=OT_ATTEST, =algI, =idI, =fp(kI), mhI, cvI, plI) = fbI` with
`mhI = h(tI)`. S-STANDING derives identity from
`attemptCore(t, ppf, sg, decl)` and `aid = h(core)`
(`ss_q1_strict_dns_compromised.pv:352-385`). **The term equalities that
connect them are the FIVE TERM EQUALITIES below, and they are what is
required; the verifier CHECKS in the fourth column are the CORRECT
VERIFIER'S and are removable by the companions named**
*(REPAIR 2026-09-17, Codex round 3 finding 3. The withdrawn wording,
quoted: “**The term equalities that connect them, all four required:**”
— it said “four” of five rows, and it folded each row's **verifier
check** into the equality, so `kX = kI` read as *“`kX = kI`, with
`fp(kX) = kfpr` from `t`”* and a builder following the mapping would
have re-imposed inside the join exactly the fingerprint precondition
(E5)'s withdrawal took out of it. The columns are now separate.)*

**How to read the two columns.** The **term equality** is
**immutable**: it *defines the join*, it is how the standing path's
`core` is built from the presentation the front-end handed it, and **no
companion removes it** — removing one does not sever a producer fact,
it un-joins the composition and makes C-Q6 vacuous. The **verifier
check** is a check of the **correct** verifier (§1.2's numbered steps)
and is **removable by the named companion**, which is exactly what a
companion is for.

| S-P7 term | S-STANDING term | Term equality (immutable; defines the join) | Verifier check it enables (the correct verifier's; removable) |
|---|---|---|---|
| `sgI`, extracted from `wrap(cvIw, (fbI, sgI))` | `sg`, `core`'s third field | **`sg = sgI`** — the *same signature term*, not merely one that verifies | **none — the pin itself.** Nothing removes it; **shown load-bearing**: with the fingerprint guard kept and the `=sgI` pin relaxed to a free term, the artifact-A/artifact-B substitution becomes **reachable** (`cap11c_ss_q3_structural_join_sg_unpinned.out:847`) while wrapped designation stays `is true` (`:495`) |
| `fbI`, the inner framed bytes | `fb`, the frame the envelope path checks | **`fb = fbI`** | `checksign(sg, kX) = (BYTES, fb)` — **link 4**, check 4/6 of §1.2; removed by **C-C5** and **C-C7** |
| `tI`, the inner evidenced tuple | `t`, `core`'s first field and the event's third argument | **`t = tI`**, pinned by `=t` in the `attemptCore` destructuring (`ss_q1…:382`) | the **evidence checks** — check 1 of §1.2, `checksign(ev, kCh) = (STMT_DIGEST, h(t))`; removed by **C-C10** (and subverted by **C-C14**) |
| `kI`, the inner accepting key | `kX`, the key the report is computed against | **`kX = kI`** | **`fp(kX) = kfpr`** from `t` — **check 7** of §1.2, the entitled-key comparison; **removed by C-C12**. *(This is (E5), withdrawn from the emission contract; it may appear **here and nowhere else**.)* |
| `ppfI`, the inner possession proof | `ppf`, `core`'s second field | **`ppf = ppfI`** | `checksign(ppf, kX) = (POSS, t)` — **link 3**, check 6; removed by **C-C3** and **C-C8** |

**The split is shown, not argued.** On a structural-join rewrite of the
C-C12 source — fresh intake name, front-end forwarding to both paths in
parallel, the standing path destructuring the wrapper itself, and
`attemptCore` pinned to the presentation's own `t`, `ppf` and `sg`,
**with no fingerprint precondition** — the join **works**:
`cap11a_ss_q3_structural_join.out` gives wrapped designation **`is
false`** as C-C12 requires (`:735`), the artifact-A/artifact-B
substitution **unreachable** (`:756`), `StandingUnentitled`
**reachable** (`:1307`) and honest standing reachable (`:1657`). Add
the mapping's fingerprint clause back **anywhere in the join** and
C-C12 is suppressed again:
`cap11b_ss_q3_structural_join_fp_pin.out` gives designation **`is
true`** (`:495`) and `StandingUnentitled` **unreachable** (`:553`) —
the same shadowing `cap5b` showed for (E1). The term equalities
therefore carry the join and the checks carry the severability.

`decl` is the standing path's own declared time and is unconstrained by
S-P7; it is the one core field the wrapper path does not supply, and
its freedom is what `h`'s injectivity (L2-c) carries, as L-16's
inherited residual already records.

**(4) What the equalities exclude, stated as the substitution they
forbid.** Without (E1)–(E3) and the table above, an adversary presents
**artifact A** through the wrapper path — honest inner bytes `fbI_A`
under `kI_A`, so C-Q4's `Rescoped` and link 6b are satisfied — and
**artifact B** to the standing path — a core `attemptCore(t_B, ppf_B,
sg_B, decl_B)` whose identity `h(core_B)` an honest issuer really did
designate, so S-STANDING's Q1 is satisfied — and the conjunction of the
two family checks holds while **nothing ties the standing verdict to
the attributed artifact**. **(E1) forbids it by the shared fresh
intake name and the structural extraction** — the pair `(aid, lyr)` of
§1.3, which no replay and no second presentation can duplicate *(named
as the pair by the REPAIR of 2026-09-17, Codex round 3 finding 1)*;
**(E2) forbids it by requiring `core`'s own three content fields to be
the accepted `t`, `ppf` and `sg` of that acceptance**; and
the `sg = sgI` row forbids the weaker escape in which `core` is built
over a *different* signature that happens to verify under the same key.
`sg = sgI` is a **term** equality, not a verification equality, which
is what makes it immune to the D-4 `dsks` route: a DSKS-derived key
verifies the **one seen signature**, so requiring the same signature
term denies the adversary a second `(key, signature)` pairing to build
a core from. **This is what the structural join achieves without any
verifier check** *(REPAIR 2026-09-17, Codex round 3 finding 3)*: on
`cap11a` the substitution is **unreachable** (`:756`) with **no**
fingerprint precondition present, while C-C12 can still fail
(`:1307`); relax the `sg = sgI` pin alone and the substitution becomes
**reachable** (`cap11c…:847`). The exclusion rests on the **term
equalities**, not on the removable checks of §(3)'s fourth column.

**(5) The three conjuncts, in both forms, in both modes** *(REPAIR
2026-09-17, Codex round 3 finding 2; the withdrawn heading, quoted:
“**(5) The two conjuncts, in both forms, in both modes.**”)*.

**Conjunct 1, the standing verdict (D12).**

- **Unrestricted form, strict (a) and (b):**
  `event(EstablishedWrapped(aid, lyr, t, kX, core, ESTABLISHED)) ==> event(Designated(kX, h(core)))`.
  **Registered green.**
- **Honest-key forms, all three modes** — one per issuer key of §1.1's
  fixture, which is ENUM note 3's two-honest-values rule:
  `event(EstablishedWrapped(aid, lyr, t, pk(skI), core, ESTABLISHED)) ==> event(Designated(pk(skI), h(core)))`
  and the same with `pk(skI2)`. **Registered green in (a), (b) and
  (d).** These are S-STANDING Q1(ii)'s shape (`ss_q1…:224-226`).
- **Degraded (d):** the **unrestricted** form is **registered red**,
  the A4.6 cost, exactly as S-STANDING's own Q1d (i) is
  (`ss_q1d_degraded_compromised.out:640` `is false`, L-18 `:534`);
  the honest-key forms stay green (`:649`, `:658`). C-Q1's link 1b is
  not asserted in (d) for the same reason and the same amendment
  (`docs/phase-0-prereg-amendment-4.md:156-171`). **A red on the
  unrestricted form in (d) is a registered cost, never a finding.**

**Conjunct 2, the entitled key (D13).** `event StandingUnentitledWrapped(pkey, bitstring)`
over *(key the report was computed against, evidenced tuple)*, fired by
the standing path's judge when `fp(kX) ≠ kfpr`; **unreachable in
(a), (b) and (d)** — S-STANDING Q1(iii)'s shape and its registered
mode coverage (`ss_q1_strict_dns_compromised.out:530`,
`ss_q1d_degraded_compromised.out:664`).

**What the judge observes** *(REPAIR 2026-09-17, Codex round 2
finding 1; the withdrawn clause, quoted: “fired by the standing path's
judge when `fp(kX) ≠ kfpr` **for a report carried under an `aid` that
(E1) binds to a wrapped acceptance**”)*: the judge observes **the
standing path's own report**, under the **intake** `aid` and with the
(E4) wrapped flag — exactly as SS.Q3's judge observes S-STANDING's
(`ss_q3_companionB_entitled_via_envelope.pv`, whose `StandingUnentitled`
is reachable at `cap5a_ss_q3_companionB_asis.out:860`) — and it fires
on `fp(kX) ≠ kfpr` **whether or not the envelope path accepted**. It is
therefore **reachable under C-C12**, which is what makes C-C12 a
severing of D13 at all, and **unreachable in the correct model**, where
check 7 of §1.2 rejects the unentitled key. The withdrawn clause made
the judge's reachability conditional on the very acceptance the mutation
is designed to fail.

**Conjunct 3, scope agreement (D11's conditional half).** **ADDITION
beyond `LEDGER.md:1294`, and marked so** *(REPAIR 2026-09-17, Codex
round 3 finding 2)*. `:1294` fixes C-Q6's formulation and the rows it
consumes; it states two conjuncts and **no** scope observation. This
conjunct is **this file's**, registered here so a builder does not read
it as the ledger's.

**Why it is added.** The round-two repair made the standing path
extract the innermost terms **itself** and consume **no** envelope
event — which is right for D13, since it is what lets C-C12 fail
(`cap11a…:1307`), and which **severs the consumption D11's conditional
half claims**. With only conjuncts 1 and 2, **nothing in C-Q6 observes
the envelope path's attribution at all**, so C-C15's scope mutations —
which change the **reported** key and leave the innermost material
untouched (`sp7_q5c_companion_one_level_in.pv:229-241`, the mutated
`out(scopeCh, …)` report at `:240`) — cannot red C-Q6, and D11's
conditional half would have had no falsifiable consumer. Conjunct 3
restores the consumption **without re-sequencing the paths**.

**The judge, in S-P7's `ScopeJudge` house form**
(`sp7_q2_degraded_compromised.pv:349-353`, a judge over two private
channels that fires its mismatch event or its witness). The capstone's
judge reads, on private channels:

- the **standing path's** report `(aid, lyr, kX, id)` — the key the
  standing verdict was computed against **and the innermost issuer
  identity `id`**, the first field of the `authTuple(id, kfpr, sset,
  alg, ver)` the standing path **extracted itself** under (E1); the
  path already reports `kX` for conjunct 2's judge and `id` is read off
  the same term, so no new extraction and no new check is introduced;
  and
- the **envelope path's** attribution report `(aid, lyr, kA, idA)` —
  the `scopeCh` report S-P7's models already emit — the correct
  model's at `sp7_q2_degraded_compromised.pv:303`
  (`out(scopeCh, (ctx, kI, idI, fbI))`), read by `ScopeJudge` at
  `:351`, and the **mutated** form, which reports the middle layer's
  `(kM, idM)`, at `sp7_q5c_companion_one_level_in.pv:240`.

It fires **`ScopeMisreported(aid, lyr, kX, id, kA, idA)`** when
**`(kA, idA) ≠ (kX, id)`**, and is **registered unreachable in (a),
(b) and (d)** — the same mode coverage as conjunct 2.

**THE COMPARISON IS OVER THE PAIR, KEY AND IDENTITY, NOT THE KEY
ALONE** *(REPAIR 2026-09-17, Codex round 4 finding 1. The withdrawn
sentence, quoted: “It fires **`ScopeMisreported(aid, lyr, kX, kA)`**
when `kA ≠ kX`, and is **registered unreachable in (a), (b) and (d)** —
the same mode coverage as conjunct 2.” The withdrawn event signature is
quoted at its declaration in §(1).)* **Why.** The inherited scope
relation D11 names covers **both** the attributed key and the
attributed issuer identity: S-P7's own judge fires
`Rescoped(kIrep, idIrep, kH, idH, fbI)` on *"an acceptance of the same
`fbI` with `(kIrep, idIrep) ≠ (kH, idH)`"* and emits
`HonestWrappedAccepted` when they are **equal**
(`s-p7/PREDICTIONS.md:226-237`). A key-only judge is strictly weaker
than the relation it is supposed to consume, and the gap is not
hypothetical: **S-P7's Q6a companion is exactly the identity-only
case** — verification under `kI` retained, the wrapper's identity
reported — and it is a **committed** companion of this suite.

**Shown twice, in both directions.**

- **The escape, at the reviewer's projection.** On the structural join
  with **only the reported issuer identity changed** and the key left
  alone — `cap12e_ss_q1_join_scope_identity.out` — **all three C-Q6
  conjuncts stay green**: conjunct 1 unrestricted `is true` (`:542`)
  and honest-key `is true` (`:556`), conjunct 2 `StandingUnentitled`
  unreachable (`:1368`), and the **key-only** `ScopeMisreported`
  unreachable (`:570`) — while the identity judge
  `ScopeIdentityWrong` is **reachable** (`:945`), the artifact-A /
  artifact-B substitution stays excluded (`:563`) and honest standing
  stays reachable (`:1718`). A key-only conjunct 3 therefore sees
  nothing at all where the identity alone is re-scoped.
- **The committed companion is that case.** On a copy of S-P7's own
  Q6a companion with a **key-only** scope judge added beside the
  committed full `Rescoped` query —
  `cap12f_sp7_q6a_keyjudge.out` — the key-only judge is **green**
  (`:1339`, unreachable) while the committed pair-form `Rescoped` is
  **red** (`:818` `is false`), with `HonestWrappedAccepted` (`:1130`)
  and `HonestAccepted` (`:1326`) reachable. The family's own committed
  companion is precisely what the key-only judge cannot see.

**What does not change.** Conjunct 3 stays a **judge over two reports
the two paths already emit**; no verifier check is added, neither path
waits for the other, C-Q6's probability, residual decomposition and
90-minute timebox stand, and the conjunct remains an **ADDITION beyond
`LEDGER.md:1294`**. What changes is the **arity of the comparison**.

**The independence is preserved, and that is the point of the judge
form.** The **judge** waits for both reports; **neither path waits for
the other**, neither path's report is conditioned on the other's
success, and no verifier check is added anywhere. The round-two
independence therefore stands and **D13's severing is not
re-shadowed**: under C-C12 the standing path still reports an
unentitled key without the envelope path's cooperation.

**Witness.** **`HonestWrappedStandingAgreed(aid, lyr)`**, fired by the
same judge when the two reports **agree** for an honest wrapped
acceptance; **must be reachable**, on the `HonestWrappedAccepted`
pattern of `ScopeJudge`'s own `if … then` branch
(`sp7_q2_degraded_compromised.pv:352`), so that an unreachable
`ScopeMisreported` is a severing test that ran and not a judge that
never paired.

**Shown, at the reviewer's projection.** On the structural join with
**only the envelope's reported attribution key changed** and nothing
else — `cap10_ss_q3_scope_report_only.out` — `ScopeMisreported` is
**reachable** (`:779`), while wrapped designation (`:798`, `:811`),
entitled-key safety (`:856`) and honest standing (`:1205`) all stay
green/reachable. That is precisely the shape the finding needs: a scope
mutation leaves conjuncts 1 and 2 untouched and reds conjunct 3 alone.

**Descent at the reviewer's projection** *(REPAIR 2026-09-17, Codex
round 4 disposition 3; the conjunct is **descended at a projection and
predicted for the capstone**, on the pattern §9(1) uses for
"descended … but isolated at the reviewer's projection")*. The judge
above — the **actual paired-report judge**, reading `(aid, lyr, …)` from
both paths on the private channels `scopeStanding` and `scopeEnvelope`
— was built on the **correct** S-STANDING strict model with the
structural join and run against four controls. It severs on its own and
does not re-shadow D13's severing:

| Control, on the structural join | Conjunct 3, `ScopeMisreported` | Conjunct 2, `StandingUnentitled` | Substitution | Witness `HonestWrappedStandingAgreed` |
|---|---|---|---|---|
| **Correct checks** — `cap12a_ss_q1_join_correct.out` | unreachable (`:570`) | unreachable (`:998`) | unreachable (`:563`) | reachable (`:958`) |
| **C-C12's mutation** — `cap12b_ss_q1_join_cc12.out` | unreachable (`:813`) | **reachable** (`:1762`) | — | reachable (`:1204`) |
| **Key-scope mutation** — `cap12c_ss_q1_join_scope_key.out` | **reachable** (`:947`) | unreachable (`:1378`) | — | reachable (`:1334`) |
| **Both** — `cap12d_ss_q1_join_cc12_scope_key.out` | **reachable** (`:1192`) | **reachable** (`:2140`) | — | reachable (`:1581`) |

The two severings are **independent**: conjunct 3 fires on a scope
mutation with conjunct 2 green, conjunct 2 fires on C-C12 with conjunct
3 green, and under both mutations both fire. **Both paths emit
independently; only the judge waits**, which is what the round-two
independence requires and what the witness's reachability in all four
runs shows. These are bounded depth-1 structural diagnostics on a
**family-model copy**, not reproductions of C-C15's complete
configurations and not capstone results.

**THE PAIR FORM, RUN** *(REPAIR 2026-09-17, Codex round 5 disposition 3)*. The four controls above were built on
the **key-only** judge of the round-three registration. Round four made
the comparison a **pair**, key and identity, and the reviewer then built
and ran the **pair-form** judge — conjunct 3 exactly as §(5) now states
it — on the same structural join, with a **key-only judge kept beside
it as a control**. The five runs below are that set. They do **not**
replace the table above; they are the same controls re-run at the
registered arity, and they show the pair form severing on an
identity-only mutation the key-only form cannot see while leaving
conjunct 2 and the witness exactly where the round-four table put them.

| Mutation, on the pair-judge join | Conjunct 3, pair-form `ScopeMisreported` | Conjunct 2, `StandingUnentitled` | Witness `HonestWrappedStandingAgreed` | Key-only control judge |
|---|---|---|---|---|
| **None** — `cap15a_ss_q1_pairjudge_correct.out` | unreachable (`:570`) | unreachable (`:998`) | reachable (`:958`) | — |
| **Identity only** — `cap15b_ss_q1_pairjudge_identity.out` | **reachable** (`:953`) | unreachable (`:1746`) | reachable (`:1706`) | **green** (`:576`) — the identity comparison is what fires |
| **Key only** — `cap15c_ss_q1_pairjudge_key.out` | **reachable** (`:947`) | unreachable (`:1378`) | reachable (`:1334`) | — |
| **C-C12 only** — `cap15d_ss_q1_pairjudge_cc12.out` | unreachable (`:813`) | **reachable** (`:1762`) | reachable (`:1204`) | — |
| **C-C12 + key scope** — `cap15e_ss_q1_pairjudge_cc12_key.out` | **reachable** (`:1192`) | **reachable** (`:2140`) | reachable (`:1581`) | — |

The round-four independence result **survives the arity change**:
conjunct 3 fires on either scope mutation with conjunct 2 green,
conjunct 2 fires on C-C12 with conjunct 3 green, both fire under both,
and the agreement witness is reachable in all five. These too are
bounded structural diagnostics on a **family-model copy**, **descended
at a projection and predicted for the capstone**, not capstone results.

**No new timeboxed entry.** The conjunct belongs to C-Q6, whose **90
min** stands, and §3's timebox table, its 26 entries and its 1155 min
per-case total are unchanged *(by this conjunct; 27 and 1185 since the
2026-09-18 amendment added C-Q10's entry)*. *(C-Q6 is already an entry counting more
than one ProVerif query — §3's “What the total is, and is not” records
it as such.)*

**(6) Reconciliation with C-C11 and C-C12** *(the quantifier discrepancy
the first round found: C-Q6's sentence reads unrestricted while C-C12's
§4 note says its standing conjunct is "not written in that unrestricted
form" and relies on honest-key forms).* **CORRECTED 2026-09-17, Codex
round 2 finding 1. The 2026-09-16 text was WRONG, not merely
inconsistent, and it is withdrawn in place.**

*The withdrawn sentence, quoted: “**C-C12's severing is registered
against the honest-key forms**, whose red is what shows D12's producer
severed rather than the A4.6 cost re-appearing.”* It **conflated the
two standing companions**. The tree says the opposite, and **C-C12's own
companion row in §4 had it right**:

- **Under C-C12** (S-STANDING Q3 transcribed; D13's companion) the
  **honest-key forms STAY GREEN** — `cap5a_ss_q3_companionB_asis.out:642`
  and `:656` both `is true`, the committed C-C12 source re-run
  unchanged — and the **unrestricted** strict form goes **red**
  (`:628` `is false`) as a **consequence** of the entitled-key
  unbinding, **not a second severing**. C-C12's own severing is
  **conjunct 2**, `StandingUnentitled` reachable (`:860`).
- **Under C-C11** (S-STANDING Q2 transcribed; D12's companion) the
  **honest-key forms GO RED** —
  `ss_q2_companionA_identity_declared.out:808` and `:986` both
  `is false`, with the unrestricted form red beside them (`:630`) —
  **and that is D12's severing**: the attempt identity is read from the
  bundle instead of derived as `h(attemptCore(...))`, so even an honest
  key's `ESTABLISHED` no longer implies designation.

So the honest-key forms are **what C-C12 must keep green** and **what
C-C11 must turn red**; the unrestricted strict form is red under both,
under C-C11 as the severing and under C-C12 as a consequence
(`LEDGER.md:524`). C-C12's set (2) names the honest-key forms **under
honest keys other than the one the companion unbinds**, which is what
`:642` and `:656` show family-locally; **C-C11's set (1) names the
honest-key forms**, which is what `:808` and `:986` show.

**Inherited residual**,
because W consumes L-16: `h` injectivity carries *"the whole load of the
transplant result"* (L2-c, `:510`), and lineages are exactly two entries.
**Prediction: all three conjuncts hold, p ≈ 0.5** *(REPAIR 2026-09-17,
Codex round 3 finding 2; the withdrawn wording, quoted: “**Prediction:
both conjuncts hold, p ≈ 0.5**”. **The probability, its residual
decomposition and the 90-minute timebox are unchanged**; conjunct 3 is
a judge over two reports the two paths already emit, of the shape
S-P7's `ScopeJudge` is committed green in, and it is registered inside
C-Q6's existing entry)*. Basis: both producers are
committed green on their own side
(`ss_q1_strict_dns_compromised.out:503`, `:513`, `:523`, `:530`) and
S-P7's scope relation is committed green, but **no query in any model
ranges over this composition** (`:483`, `:744-750`), so nothing has ever
been observed about the two paths running together (residual: 0.25 recut,
most likely the lineage lookup over a two-entry structure inside a
wrapper-derived core, or a report witness "cannot be proved" of the
recut-1 kind; 0.10 a genuine strict-mode violation, a finding about the
composition and an amendment trigger on the construction, not a recut;
0.15 timeout, the largest timeout mass on the ladder). **Witnesses:**
`HonestStandingEstablished` over a **wrapped** presentation,
`HonestWrappedAccepted`, `HonestChain(L1, t)`, `HonestChain(L2, t)`,
**`HonestWrappedStandingAgreed(aid, lyr)`** *(added with conjunct 3 —
REPAIR 2026-09-17, Codex round 3 finding 2; a witness, not an entry,
and C-N1's rule at `:1489-1490` applies to it as to the others)*, and
the S4-row witness `(ABSENT, ISSUANCE_REFUSED)` — **a VOCABULARY
witness, not an honest-flow witness** *(REPAIR 2026-09-17, Codex round
4 finding 2)*: reachable in every correct-form run, and **unreachable
under C-C11's Q4 alternate as a registered consequence of that
mutation**, because the alternate deletes the terminal branch that
produces the report (see C-N1's two kinds, above, and §4's **C-C11**
row, which names the consequence). The four other witnesses in this
list are **honest-flow** witnesses and no exception applies to them;
**timebox** 90 min,
justified by the largest term space in the model (wrapper depth × lineage
entries × terminal dispositions × two issuers) and by its being the only
query with no prior observation of its fixture.

## C-Q7 — the signature-TERM judge (`LEDGER.md:1289`)

**Query.** The honest issuer releases `sg = sign((BYTES, fb), skI)` to a
private judge; the verifier reports `(acceptedKey, sg)`;
`event SigTransplanted(pkey, bitstring)` fires when `kX ≠ pk(skI)`;
unreachable. An **honest-origin / transplant** claim, which is supposed
to quantify over honest-released signature terms, because that is what
"transplant" means. **Serves D5, and nothing else.** It is **not** D6's
producer: it observes `(acceptedKey, signature)` and cannot see
different bytes presented under the same key
(`d6b_sp1_q8_samekey_unbound.out:246` green while authorship goes red at
`:593`). All four cases; companion **C-C6**.
**Prediction: green, p ≈ 0.8**. Basis: feasibility green
(`d5c_sp1_sigjudge.out:203`), red under its companion
(`d5d_sp1_sigjudge_condunbind.out:414`) (residual: 0.15 recut, 0.05
timeout). **Witnesses:** `HonestAccepted`, `HonestChain`; **timebox**
45 min.

## C-Q8 — the signature/bytes judge, structural (`LEDGER.md:1290`)

**Query.** For **every** acceptance, the signature `sg` accepted under
key `kX` over presented framed bytes `fb` satisfies
`checksign(sg, kX) = (BYTES, fb)` for the **presented** `fb`. The judge
has **no honest-signature filter** and fires including the case where
`sg` does not verify under `kX` at all; it does not, and cannot, say who
produced `sg` (`:2165-2211`).
`event SigBytesUnbound(pkey, bitstring, bitstring)` over *(accepting
key, signature term, presented framed bytes)* is reported at **every**
acceptance point, every layer, every signer slot, whoever made `sg`;
unreachable. **Serves D6** and C-Q1's link 4; registered unreachable in
**all four** cases, the relation being structural; companion **C-C7**,
both configurations.
**Prediction: green, p ≈ 0.75**. Basis: green on the committed S-P1 verifier
(`d6c_sp1_q8_judge_all.out:284`), red under both escapes (`d6d…:507`,
`d6e…:643`); the reduction from 0.8 is the destructor `else` branch at
three layers plus `InnerCheck` (residual: 0.2 recut, 0.05 timeout).
**Witnesses:** `HonestAccepted(kH, fbH)` and `HonestChain` in the same
fixture; **timebox** 60 min.

## C-Q9 — the possession/manifest judge (`LEDGER.md:1291`)

**Query.** For a completed acceptance reporting key `kX` and accepted
manifest `t`, the accepted possession proof `ppf` satisfies
`checksign(ppf, kX) = (POSS, t)` for the same `t` the verifier accepted.
`event PossessionUnbound(pkey, bitstring, bitstring)` is reported at
every acceptance point once per signer slot, firing including when `ppf`
does not verify; unreachable. **Serves D10** and C-Q1's link 3. S-P3's
`PossessionTransplanted` is **not** this relation's producer: it
compares keys only. All four cases; companion **C-C8**.
**Prediction: green, p ≈ 0.8**. Basis: green on the committed S-P2 verifier
(`d10a_sp2_q9_base.out:1111`), red under the combined manifest unbinding
that leaves `PossessionTransplanted` green (`d10b…:1462` against
`:1297`) (residual: 0.15 recut, 0.05 timeout). **Witnesses:** both
`HonestComplete` and `HonestAccepted`; **timebox** 60 min.

## C-Q10 — the D-6 tag-separation judge (no ledger line; AMENDMENT 2026-09-18, the author's ruling on §8 item 1)

**Query.** The standing path, having verified the lineage record's
signature under the entitled key, reports `(kT, tag)` — the key and
**the tag it parsed** — on a private judge channel **in parallel with
its continuation** (§2 rule 1); `event TagConfused(pkey, bitstring)`
fires when `tag ≠ TLR`; unreachable. A **structural** judge in C-Q8's
sense: no honest-signature filter, nothing about who made the
signature. With the tag check present it is unreachable **by
construction**, since the check pins the tag, and that is the point: it
is the direct observation that C-C18's red is the tag's and no other
check's (the report contract, §1.3). **Serves the composed D-6
property** of `LEDGER.md:387-398` and §2's rule 6 — a signature under
one tag never parses as a signature under another — which is **not a
matrix row**: it is L-07's enumeration under composition, the property
the ledger says *“is precisely what the capstone is for”*
(`:1270-1273`), and this is the only registered query in the suite that
exercises it **at the `TLR` consumer**. **What C-Q10 covers, stated so
the six-tag property is not attributed to it alone** *(Codex round 16
finding 1, with its tested counterexample)*: C-Q10 observes the tag the
**standing path** parses on the lineage-record slot, and nothing else.
A foreign tag consumed elsewhere is another query's: a `REFUSAL`
signature accepted by the **envelope** as an attestation is **C-Q8**'s
red (`checksign(sg, kX) = (BYTES, fb)` for the presented `fb`, §3), a
foreign tag on the possession slot is **C-Q9**'s, and on the authority
evidence **link 1a**'s. The reviewer showed the limit by run: on a copy
of `cap27e` with **only the envelope's `BYTES` tag equality** removed
(signature verification, byte binding, possession, authority evidence
and frame checks retained), an adversary-held issuer key in degraded
mode gets a `REFUSAL`-tagged signature accepted as an attestation while
C-Q10 stays green and every other polarity is unchanged
(`cap27h_ss_q1d_degraded_foreign_tag_envelope_bytes_tag_unbound.out:2016`
reachable against its control
`cap27g_ss_q1d_degraded_foreign_tag_envelope_observer.out:1859`;
`TagConfused` unreachable in both, `:2022`, `:1865`) — and that
acceptance is exactly what C-Q8's registered relation rejects, so the
ladder as a whole is not evaded. Domain separation across all six tags
is therefore carried by **C-Q10, C-Q8, C-Q9 and link 1a together**, one
per consumer, and C-C18 severs the `TLR` consumer only. **Its consuming
query is C-Q6's standing conjunct**: with
the foreign-tag signer present and the tag check unbound, a
`REFUSAL`-tagged signature over a TLR-shaped body is accepted as the
issuer's lineage record and `ESTABLISHED` is reported for a core the
issuer never designated — that is what C-C18 registers red. Stated in
every case C-Q6 is stated for: **(a), (b), (d)**; companion **C-C18**.
**Prediction: green, p ≈ 0.85**. Basis: unreachable on the **committed**
strict S-STANDING model with the foreign-tag signer and the judge added
and every check correct
(`cap27c_ss_q1_strict_foreign_tag_correct.out:2045`), and on the
committed degraded model likewise
(`cap27e_ss_q1d_degraded_foreign_tag_correct.out:1853`); reachable
under its companion in both modes
(`cap27d_ss_q1_strict_foreign_tag_tlr_tag_unbound.out:2471`,
`cap27f_ss_q1d_degraded_foreign_tag_tlr_tag_unbound.out:2135`); and the
2026-09-06 reviewer fixture re-run on our tree byte for byte gives the
same separation without the judge
(`cap27a_ss_foreign_tag_reviewer_fixture.out:469-489` all `is true`
against `cap27b_ss_foreign_tag_reviewer_tlr_tag_unbound.out:595`,
`:734`) (residual: 0.10 recut — the parallel tag report is new in the
standing path and the capstone's standing path is C-Q6's join, not the
family's — 0.05 timeout). **Witnesses:** `HonestStandingEstablished`
(`cap27c…out:855`, `cap27e…out:976`) and, in the capstone, `HonestChain`;
**timebox** 30 min.
**What C-Q10 does not claim.** Nothing about the refusal record. The
foreign signer's body is opaque; the record's content and decomposition
(A3 §A3.7.2), the extended atomic-entry invariant (**L2-n**) and **E6**
are untouched, unclaimed here, and owed exactly where they were.
`REFUSAL` is exercised as a signing domain and unexercised as a record;
§7 says so.

## C-N1 — the vacuity witness (`LEDGER.md:1295`)

**Query.** Honest-flow acceptance emitted by the judge, never bare
acceptance, one per fixture. **Prediction: reachable in all four cases,
p ≈ 0.85**. Basis: reachable in every committed family model (residual: 0.1
recut, 0.05 timeout). **A run in which any registered witness is
unreachable is a broken fixture and not a result** (`:1503-1510`).
**Timebox** 30 min.

**THE RULE ADMITS ONE NAMED EXCEPTION: THE REGISTERED WITNESSES ARE OF
TWO KINDS** *(REPAIR 2026-09-17, Codex round 4 finding 2. The rule
sentence is **not** withdrawn — it stands for every witness of the first
kind — but it is **qualified**, and the qualification is quoted against
it. The withdrawn reading, quoted: “**A run in which any registered
witness is unreachable is a broken fixture and not a result**”, read as
covering **every** registered witness under **every** companion,
including a companion whose mutation **deletes the branch the witness
reports from**.)*

- **Honest-flow witnesses** — `HonestStandingEstablished`,
  `HonestWrappedStandingAgreed`, `HonestWrappedAccepted`,
  `HonestAccepted`, both `HonestComplete` forms, and `HonestChain` at
  every layer. These say *the correct path can still complete*, which
  is what makes a companion's red a **severing** and not a broken
  model. They **must survive every companion**, and an unreachable one
  is a broken fixture exactly as `:1489-1490` says. **No exception
  applies to this kind.**
- **Vocabulary witnesses** — the standing report-shape witnesses
  **S1** `(ESTABLISHED, TERMINAL_DISPOSITION_SHOWN)`, **S2**
  `(ABSENT, SUPERSEDED)`, **S3**
  `(ABSENT, NO_TERMINAL_DISPOSITION_EVIDENCE)`, **S4**
  `(ABSENT, ISSUANCE_REFUSED)` and **MISMATCH**
  `(ABSENT, STANDING_EVIDENCE_MISMATCH)`. These say *the verifier can
  still produce each report shape the vocabulary declares*. They are
  **reachable in every correct-form run** — that is a registered
  prediction and its failure in a correct-form run **is** a broken
  fixture — but a **named companion whose mutation deletes the branch
  that produces one of them** makes it unreachable **as a registered
  consequence of the mutation, never a broken fixture**. The
  consequence must be **named in that companion's row before the
  freeze**; an unreachable vocabulary witness under a companion whose
  row does **not** name it is still a broken fixture.

**This is the family's own reading, inherited, not invented here.**
S-STANDING already classifies these witnesses that way and already
records the case: its Q4 row reads *"S2 and S4 witnesses **unreachable**
(`1708`, `1838` — consequence of the mutation, the branches no longer
exist)"* (`s-standing/RESULTS.md`, SS.Q4 row; the term "vocabulary
witnesses" is the family's, `s-standing/RESULTS.md:345`), with its N1
honest-flow witness **reachable** in the same run
(`ss_q4_companionC_terminal_unchecked.out:1425`). **The one companion
of this file that names the consequence is C-C11, under its Q4
alternate** (§4); every other companion on the record leaves all five
reachable, which is recorded in that row.

**DESCENT AT THE REVIEWER'S PROJECTION — THE THREE C-C11-FAMILY
CONTROLS** *(REPAIR 2026-09-17, Codex round 5 disposition 3)*. The two-kinds rule above was registered on the
committed S-STANDING outputs and on `cap12g`. The reviewer then ran
**all three** C-C11 configurations on the **pair-judge** structural join
of `cap15a` — the correct S-STANDING strict model with the round-four
conjunct 3 — which is the projection nearest the capstone that exists
in any model. The rule holds at that projection, and the only
vocabulary loss is the registered one:

| Configuration, on the pair-judge join | Honest standing `HonestStandingEstablished` | Agreement witness `HonestWrappedStandingAgreed` | Vocabulary witnesses S1–S4, MISMATCH |
|---|---|---|---|
| **C-C11 proper** — S-STANDING Q2, declared identity — `cap16a_ss_q1_pairjudge_cc11_declared.out` | reachable (`:2581`) | reachable (`:1450`) | **all five reachable** (`:2826`, `:3067`, `:3258`, `:3497`, `:3738`), with the standing correspondences red (`:766`, `:1012`, `:1696`, `:1942`, `:2188`) and conjunct 3 green (`:1026`) |
| **Alternate abl6** — the TLR unsigned — `cap16b_ss_q1_pairjudge_cc11_unsigned.out` | reachable (`:2548`) | reachable (`:1436`) | **all five reachable** (`:2790`–`:3665`), correspondences red (`:762`–`:2156`) |
| **Alternate Q4** — terminal disposition unchecked — `cap16c_ss_q1_pairjudge_cc11_terminal.out` | reachable (`:2873`) | reachable (`:1542`) | **S2 and S4 UNREACHABLE** (`:3217`, `:3413`) — the registered consequence — the other three reachable (`:3208`, `:3404`, `:3652`); correspondences red (`:810`–`:2514`) |

**What this settles.** The **honest-flow** witnesses survive **every**
C-C11 configuration, so no configuration of this companion is a broken
fixture; and the **vocabulary** loss occurs under **exactly one**
alternate, the one §4's C-C11 row names. **Checked, not assumed**, at the
projection as well as on the committed outputs. These are structural
diagnostics on a **family-model copy**, not capstone results.

## The REQUIRED retained queries (`LEDGER.md:1425-1447`)

Registered in addition to C-Q1…C-Q9 and C-N1, because the companions
must falsify or preserve them. Naming them does not predict their
colour; each carries its own frozen prediction. Timebox 30 min each.

| Query | Shape | Modes | Prediction |
|---|---|---|---|
| `Accept ⟹ IssuerSigned` (strict) | D3's own query, S-P1 Q1(i) transcribed | (a), (b) green; **(c) registered red**, which is C-C1. *(The (a)/(b) green depends on §1.1's reading of “adversary-enrolled” — compromised-channel enrolment only — without which it is falsified with no verifier change, `cap8b_sp1_q1_strict_adversary_enrolled.out:398`; REPAIR 2026-09-17, Codex round 2 finding 4.)* | green in (a)/(b), p ≈ 0.85 (`base_sp1q1.out:201`); red in (c), p ≈ 0.9 (`s6_bothchannels.out:361`) |
| `AcceptedUnderHonestKey ⟹ IssuerSigned` | S-P1 Q2(i), honest-key authorship | all four | green, p ≈ 0.85 (`sp1_q2_*.out:173`). **Basis sentence corrected** *(REPAIR 2026-09-17, Codex round 3 finding 4; the withdrawn generalization, quoted: “green in every mutant that reds C-Q7”)*: it is green in every **S-P1-only** mutant that reds C-Q7 — on the record that is **`d5d_sp1_sigjudge_condunbind.out`**, C-Q7 `is false` (`:414`) with authorship `is true` (`:422`) — and it is **red beside C-Q7 under C-C7(ii) in the COMPOSED fixture**, where §1.1's same-key wrapper signer puts an honest `OT_WRAPPER` signature within reach of the type-conditional waiver: `cap7b_sp1_q8_wrapper_signer_type_conditional.out:528` (C-Q7 `is false`) **and** `:1072` (authorship `is false`, trace `:1032-1072`), which §4's C-C7 row already registers. *(**`d6e_sp1_q8all_samekey_unbound.out` is NOT an instance of the corrected sentence either**, and is named here so no one reads it as one: its C-Q7 is **green** (`:274`), so it is not a mutant that reds C-Q7, and its authorship is **red** (`:809`) — C-C7(i)'s registered red. The round-3 disposition cited it beside `d5d` as a supporting mutant; the `.out` does not support it on either count.)* **The p ≈ 0.85 baseline prediction stands and is unchanged** — C-C7(ii)'s red is registered in §4 as that companion's expected failed set, not as a divergence from this row |
| `Stripped` | S-P2 `SetJudge` | all four | green, p ≈ 0.8 (`base_sp2.out:378`) |
| `SignerForged` | S-P2 `MemberJudge`, slot form | all four | green, p ≈ 0.8 (`base_sp2.out:384`) |
| `Spliced` | S-P2 Q6 `ContentJudge` over the two frames of one acceptance | all four | green, p ≈ 0.75 (`base_sp2.out:1013`; the §A5.4 guards are the newest checks in the suite) |
| `TypeConfused` | S-P7 Q2/Q1 | all four | green, p ≈ 0.85 (`base_sp7.out:527`) |
| `VersionLied` | S-P7's canonicalization-version judge | all four | green, p ≈ 0.85 (`s4_innerfp_mh.out:1949`, green even under C-C4) |

`Rescoped` and `SetAltered` appear in the same ledger table; they are
registered above as C-Q4 and C-Q5 and are not counted twice. The
unrestricted degraded form `AcceptS ⟹ IssuerSigned` is **registered red
in case (d)**, the A4.6 cost, not a defect (`:1371`); C-Q1 must not
assert it.

## Timeboxes declared

| Group | Box | Queries | Subtotal |
|---|---|---|---|
| C-Q1 links 1a, 1b, 2a, 3, 4, 6a, 6b | 45 min | 7 | 315 |
| C-Q1 links 2b, 5 | 60 min | 2 | 120 |
| C-Q2, C-Q3, C-Q5, C-Q7 | 45 min | 4 | 180 |
| C-Q4, C-Q8, C-Q9 | 60 min | 3 | 180 |
| C-Q6 | 90 min | 1 | 90 |
| C-Q5w, C-N1 | 30 min | 2 | 60 |
| Retained queries | 30 min | 7 | 210 |
| C-Q10 *(AMENDMENT 2026-09-18)* | 30 min | 1 | 30 |
| **Total declared, per compromise case** | | **27** | **1185 min (19 h 45 m)** |

*(AMENDMENT 2026-09-18, the author's ruling on §8 item 1: C-Q10 adds
**one** 30-minute entry, so the per-case total is **27** entries and
**1185 min**, and the ceiling is at most **4 × 1185 = 4740 min (79 h)**;
C-Q10 is stated for three cases, so the ceiling is looser than the sum
by at least one box, as for C-Q2 and C-Q6. The withdrawn row, quoted:
“**Total declared, per compromise case** | | **26** | **1155 min (19 h
15 m)**”. Every “26”, “1155” and “4620” **outside the dated repair sections
and the skeptic logs** is superseded by this note and by the row above
(the two live sentences of *“What the total is, and is not”* and §3's
observer paragraph now carry the new totals with the old in
parentheses); every one **inside** the dated repair notes, the dated
repair sections and the skeptic logs records the totals **as they
stood** and is history, not rewritten: the sums
7 + 2 + 4 + 3 + 1 + 2 + 7 = 26 and 315 + 120 + 180 + 180 + 90 + 60 + 210
= 1155 were right when written and become 26 + 1 = **27** and
1155 + 30 = **1185**. No companion gains a box: C-C18 runs inside
C-Q10's.)*

**What the total is, and is not** *(skeptic 2026-09-15: the row read
"Total declared" with the four compromise cases unaccounted for, while
the ladder above declares the box **per run**).* **1185 min is the
per-case sum** *(1155 before the 2026-09-18 amendment added C-Q10)*. Each compromise case gets the full box, so the declared
wall-clock ceiling for the ladder is the per-case sum taken over the
cases each query is stated for: **at most 4 × 1185 = 4740 min (79 h)** *(4 × 1155 = 4620 before the 2026-09-18 amendment)*,
and less wherever a query is stated for fewer than four — C-Q2 in (a)
and (b) only; C-Q1-strict in (a), (b), (c); C-Q1-degraded in (d); C-Q6
in (a) and (b), and **in (d) as well, for everything except conjunct
1's unrestricted form**; C-Q10 in (a), (b), (d) *(AMENDMENT 2026-09-18)* *(REPAIR 2026-09-17, skeptic read S-2. The
withdrawn phrase, quoted: “with the entitled-key conjunct also in (d)”.
**§(5) governs**: in (d), conjunct 1's honest-key forms, conjunct 2 and
conjunct 3 are all asserted, and only conjunct 1's **unrestricted** form
is not. **The arithmetic does not move** — C-Q6 is one separately
timeboxed entry in every case it is stated for, and it is stated for
three cases either way, so the per-case totals and the 4 × 1155 = 4620
min ceiling stand exactly as written)*. The total
row is **not** the capstone's whole budget. **27** *(26 before the 2026-09-18 amendment)* counts registered,
separately timeboxed **entries**, not ProVerif queries: C-Q3 is per-role
(`ReattributedA` / `ReattributedB`), C-Q4 carries two judges, C-Q6
**three** conjuncts *(REPAIR 2026-09-17, skeptic read S-3. The withdrawn
word, quoted: “C-Q6 **two** conjuncts”. C-Q6 has had **three** since the
round-3 repair added conjunct 3, scope agreement; that repair pointed at
this very paragraph and left the count standing. **The totals are
unchanged, and this is a stale gloss and not a broken sum**: C-Q6 is one
separately timeboxed entry however many conjuncts it carries, so
7 + 2 + 4 + 3 + 1 + 2 + 7 = **26** and
315 + 120 + 180 + 180 + 90 + 60 + 210 = **1155 min** both still check,
as does 4 × 1155 = 4620. The same stale count inside the **2026-09-15
skeptic log** is **history and is correctly left as it stands**)*,
C-Q5w two set sizes and link 2b three correspondence
conjuncts — each inside its entry's box. **A timeout is a
mechanism-viability failure, not property evidence** (§3), and is
disposed by the ablation order there, never by raising the box after
the fact.

---

# 4. Companions

**Three sets per companion** (`LEDGER.md:1450-1491`): (1) the expected
failed-query set; (2) the guarantees that must stay green; (3) the
witnesses that must stay reachable. Each must sever **the named producer
fact**, not merely turn some consumer query red.

**The rule from ENUM §5 and `LEDGER.md:1459-1480`.** The withdrawn rule
was *"and no other; a red outside this set is a broken fixture, not a
severing."* In its place: the sets below are **re-specified against the
capstone's own query names**, which is what `:1474-1476` requires of this
file, and they descend from family-local runs and cite them; and **a
companion failing outside its set, or a witness dying, is a broken
fixture to be diagnosed and recorded, never a finding** until the
diagnosis distinguishes a broken fixture from a real consequence of
composition the single-family run could not exhibit.

**CASES, AND THE GREEN CONTROL** *(REPAIR 2026-09-17, Codex round 5 finding 2)*. Every companion row
below, in the unnumbered table, and in §9 now carries a **Cases** cell.
A companion's registered reds are **not the same in every compromise
case**, and this file stated its failed sets without case assignment.
Each cell says, per configuration, which of §1.1's four cases the red is
**registered and descended** in, which it is **predicted** in, and which
the configuration is a **green control** in. **A green control is a
REGISTERED OUTCOME, not a broken fixture**: the mutation is present,
**every query is green and every witness is reachable**, because that
compromise case does not supply the material the mutation needs — most
often because §1.1's **compromised-channel-only** enrolment denies the
adversary the authorized key the family's degraded trace used.
**C-N1's rule does not classify a green control as a broken fixture**
(§3, C-N1): that rule governs an **unreachable witness**, and in a green
control every witness is reachable — what is absent is the **attack**,
not the honest path. The case is recorded in `RESULTS.md` as the result
it is. Where a cell says **predicted**, which way it falls is an
**observation of the run**, recorded there and never repaired by editing
this file. **The case assignment adds no query, no companion and no
timeboxed entry**; it says in which runs each already-registered red is
expected. The shown instance is C-C15(i): red in **(d)**, and a
**green control** in **(a)/(b)** on the strict transcription
(`cap14b_sp7_q1_strict_q6b.out:550`, `:559`, `:568`, `:843`, `:1047`;
`cap14c_sp7_q1_strict_repo_q6b.out` identical), §9(1).

**A STRICT OUTCOME IS DESCENDED BY A STRICT RUN OR IT IS PREDICTED; A
READING OF A DEGRADED TRACE IS NEITHER** *(REPAIR 2026-09-17, Codex round 6 finding 2)*. This is
the discipline this file already states, made a rule of the **Cases**
cell because round five's repair broke it: that repair filled the
strict cells of companions having only degraded runs by **reading their
degraded traces** — counting `dsks` steps and calling the accepted
tuple honestly evidenced — and **four of those readings were wrong**
(C-C2, C-C3, C-C8, and C-C16's basis), while a fifth (C-C7) gave an
all-green label to configurations with **mixed** outcomes. **The owner
instance directed that repair and accepted its judgement calls; the
error is the owner's, not the reviewer's and not the file's earlier
drafters'.** From here: a cell may say **descended** only where it
**names a run in that mode**; otherwise it says **predicted** and names
its basis — channel symmetry, or the descent from the degraded run
where the mutation's route is structural. A count of `dsks` steps in a
degraded trace is **neither**, and no cell below uses one.

**A FAMILY COPY'S DECLARED QUERIES ARE NOT THE CAPSTONE'S QUERY SET**
*(REPAIR 2026-09-17, Codex round 7 finding 1)*. The class rule, in the
owner instance's words at the disposition: *a family copy's declared
queries are not the capstone's query set; a configuration may be called a
green control only over the capstone's queries, each of which is either
declared in the copy or predicted and marked so; "descended green
control" is written only when every capstone query the copy can carry is
declared in it.* Round six's repair broke this the way round five broke
the rule above it: it read **all green** off `cap18b` and `cap17d`, which
declare, respectively, **no C-Q9 judge** and **no link-1a judge**, and
adding the missing judge **reds each** (`cap20a_sp2_strict_cc3_q9.out:1319`;
`cap20e_sp1_strict_cc10_drop_compromised_either.out:732`,
`cap20f_sp1_strict_cc10_drop_compromised_evidence.out:737`). **The owner
instance directed that repair too, and this error is the owner's**, not
the reviewer's and not the file's earlier drafters'. Two cells changed
under this rule — **C-C3**'s and **C-C10's isolation control** — and both
now name their reds; no other cell in the file was written from a copy
silently missing a capstone query.

**“GREEN CONTROL, DESCENDED” IS RETIRED AS A LABEL FOR A WHOLE
CONFIGURATION** *(REPAIR 2026-09-17, Codex round 8 finding 2)*. Rounds five, six,
seven and eight have every one of them been about the same thing: a
**configuration-level** colour read off a **family copy** that declares
only part of the capstone's query set. Repairing it one cell per round
did not close the class, so the label goes. In the owner instance's words
at the disposition: *“green control, descended” is **no longer a label
this file uses for a whole configuration**. Every Cases cell states its
strict outcome **per query**, in three lists — **descended green**
(naming the run), **descended red** (naming the run), **predicted**
(naming the basis) — and “green control” survives only as a
**predicted** configuration-level reading beside those lists, never as a
descended one.* Two consequences are mechanical and are applied to every
cell below, in the unnumbered table and in §9: **(1)** a per-query
**descended** entry may cite **only a copy that declares that query**,
which is the round-seven rule restated without the label it was attached
to; **(2)** a **strict** outcome is descended by a **named strict run**
or it is **predicted**, which is the round-six rule above. The
definition of a green control — the mutation present, every query green,
every witness reachable, because the compromise case does not supply the
material the mutation needs — **stands as a description of an outcome**;
what is retired is the claim that a family copy's all-green `.out`
**establishes** it for the capstone's query set. **This paragraph amends
the round-five paragraph above rather than rewriting it, and its shown
instance is withdrawn and quoted:** *“The shown instance is C-C15(i):
red in **(d)**, and a **green control** in **(a)/(b)** on the strict
transcription (`cap14b_sp7_q1_strict_q6b.out:550`, `:559`, `:568`,
`:843`, `:1047`; `cap14c_sp7_q1_strict_repo_q6b.out` identical), §9(1).”*
`cap14b` and `cap14c` declare **four S-P7 safety queries and two
witnesses** and neither C-Q7, C-Q8, C-Q9 nor any linkage conjunct
(`cap14b_sp7_q1_strict_q6b.pv:113-130`), so what those runs descend is
**four greens and two reachable witnesses**, not a configuration. **There
is no longer a shown instance of a descended green control, because the
label no longer exists.** The reviewer's own limit is carried with it:
missing coverage was established, **not** that the unqueried relations
are false.

| # | Mutation, in the capstone's terms | (1) Expected failed set, in capstone query names | (2) Must stay green | (3) Witnesses that must stay reachable | Row | Descends from | Cases |
|---|---|---|---|---|---|---|---|
| **C-C1** | `out(c, skD); out(c, skR)` in place of the single leak; case (c), strict | `Accept ⟹ IssuerSigned`; **C-Q1 link 1b correspondence `is false`** | `AcceptedUnderHonestKey ⟹ IssuerSigned`; **link 1a and links 2a, 2b, 3, 4, 5, 6a, 6b**; C-Q3, C-Q4, C-Q5, C-Q7, C-Q8, C-Q9 | `HonestChain` at `L0`, `L1`, `L2`; `HonestAccepted`; both `HonestComplete` | D3, D4 | `s6_bothchannels.out:361`, `:368`, `:559`; baseline `base_sp1q1.out:201`, `:208`, `:396` | **(c) ONLY — descended.** C-C1 **is** case (c), the both-channels-leaked strict run (`s6_bothchannels.out:361`, `:368`, `:559`, against the baseline `base_sp1q1.out:201`, `:208`, `:396`). It is **not** a configuration of (a), (b) or (d), and it has **no green-control reading**: in (a)/(b) the second channel is not leaked, and in (d) there is no second channel. *(REPAIR 2026-09-17, Codex round 5 finding 2)* **STRICT OUTCOME IN THREE LISTS** *(REPAIR 2026-09-17, Codex round 8 finding 2)*. C-C1 **is** case **(c)** and is stated for no other. **Descended green:** `AcceptedUnderHonestKey ⟹ IssuerSigned` (`s6_bothchannels.out:368`). **Descended red:** the unrestricted `Accept ⟹ IssuerSigned` (`:361`). **Witness descended reachable:** `HonestAccepted` (`:559`). **Predicted:** **C-Q1 link 1b red** — `ChainBroken` is declared in no model and `LEDGER.md:1494` records the member as *“NOT YET SHOWN”*; and **predicted green** — link 1a, links 2a, 2b, 3, 4, 5, 6a, 6b, C-Q3, C-Q4, C-Q5, C-Q7, C-Q8, C-Q9, with the `HonestChain` and `HonestComplete` witnesses reachable, `s6_bothchannels` declaring **three** results and no others. **No configuration-level green-control reading is offered, descended or predicted.** |
| **C-C2** | The frame's `=fp(k_)` pin **and** the manifest-hash equality removed, multi-signer path. Not the pin alone | **C-Q3** (`Reattributed`); **C-Q1 link 5**, frame-to-key half | `Stripped`, `SignerForged`, **C-Q5**, `Spliced`, C-Q8, C-Q9, links 2a, 2b, 3, 4 | both `HonestComplete`, `HonestAccepted`, `HonestChain(L0, t)` | D1 | `m4_framepin_mh.out:620`, `:379`, `:392`, `:405`, `:1263`, `:791`, `:1015`, `:1250`; isolation `m1_framepin.out:399` | **(d)** red, **descended** — the cited run is a copy of a **degraded, sole-channel** family model. (`m4_framepin_mh`, a copy of S-P2's degraded Q2 model.) **(a): THE THREE LISTS** *(REPAIR 2026-09-17, Codex round 8 finding 2)*. C-C2's mutation transcribed onto the **strict** fixture (the second, uncompromised authority process and its check added, DNS leaked, the mutation itself retained). **Descended green — the five queries the copy declares, and its three witnesses:** `Stripped` (`cap18a_sp2_strict_cc2.out:411`), `SignerForged` (`:424`), C-Q5 `SetAltered` (`:437`), **C-Q3** `Reattributed` (`:450`) and `Spliced` (`:1129`), with both `HonestComplete` branches (`:633`, `:869`) and `HonestAccepted` (`:1116`) reachable. **Descended red: NONE.** **Predicted green, basis the descent of the retained set column:** **C-Q8**, **C-Q9**, **link 2b** and **every other linkage conjunct** — links 1a, 1b, 2a, 3, 4, 5, 6a, 6b — together with C-Q2, C-Q4, C-Q7, `TypeConfused` and `VersionLied`; `cap18a_sp2_strict_cc2.pv:145-176` declares **five queries and three witnesses and nothing else**, so none of them is descended here. **Set (1)'s own members** — C-Q3 and **link 5's frame-to-key half** — are **green in (a)**: C-Q3 descended at `:450`, link 5 **predicted** green, no model declaring it. **(b): the same three lists, every entry PREDICTED** — basis **channel symmetry** (the two authority processes are interchangeable in §1.1's fixture); a basis for prediction and **never a second recorded run**. **The label is withdrawn. The withdrawn text, quoted:** “**(a): GREEN CONTROL, DESCENDED** *(REPAIR 2026-09-17, Codex round 6 finding 2)* — C-C2's mutation transcribed onto the **strict** fixture (the second, uncompromised authority process and its check added, DNS leaked, the mutation itself retained) leaves **every query green**: `Stripped` (`cap18a_sp2_strict_cc2.out:411`), `SignerForged` (`:424`), `SetAltered` (`:437`), `Reattributed` (`:450`), `Spliced` (`:1129`), with both `HonestComplete` branches (`:633`, `:869`) and `HonestAccepted` (`:1116`) reachable. **(b): green control, PREDICTED** — basis **channel symmetry** (the two authority processes are interchangeable in §1.1's fixture); this is a basis for prediction and **never a second recorded run**.” **What was wrong:** “every query green” was true of `cap18a`'s **five** and false of the capstone's set, and “green control, descended” is no longer a label this file uses for a configuration. **The outcome is not reversed — nothing here is red — and the reviewer's limit is carried: missing coverage was established, not that the unqueried relations fail.** **(c): not stated — (c) is C-C1's run** (§1.1's cases table). **The withdrawn text, quoted:** “(a), (b), (c): red predicted. No green-control reading is named, and the reason is checked rather than assumed: the trace behind `m4_framepin_mh.out:620` takes zero `dsks` steps, and the red is over the honestly evidenced tuple `t`, the adversary's key entering through a frame rather than through enrolment, so §1.1's compromised-channel-only rule removes nothing the mutation needs.” **It was a reading of a degraded trace, and it was false of the trace itself**: `m4_framepin_mh.out:608-616` forges authority evidence over a **changed** tuple, not over the honestly evidenced one. The strict run above reds nothing |
| **C-C3** | Both `SetAltered` routes removed: the frame's manifest-hash pin **and** possession-over-manifest (Q5-C2 shape) | **C-Q5**; **C-Q9**; **C-Q1 link 3** | `Stripped`, `SignerForged`, C-Q3, **`Spliced`** (absent from the C1/C2/C3 ladder models; the capstone's transcription carries it and must add it here) | both `HonestComplete`, `HonestAccepted`, **and the same in both isolation configurations** | D10 | `sp2_q5_c2_fponly_frame_nomh.out:535`, `:349`, `:356`, `:542`, `:706`, `:925`, `:1100`; isolation `…c1….out:366`, `…c3….out:363` | **(d)** red, **descended** — the cited run is a copy of a **degraded, sole-channel** family model. (`sp2_q5_c2_fponly_frame_nomh`, S-P2's degraded C2 configuration.) **(a): MIXED, DESCENDED** *(REPAIR 2026-09-17, Codex round 7 finding 1; it was registered as a green control)* — the same mutation made strict the same way is **green on C-Q5 and on the other three safety queries** and **red on C-Q9 and on link 3**. **Green**, with the registered per-slot possession report and the C-Q9 structural judge added and nothing else changed: `SetAltered` (`cap20a_sp2_strict_cc3_q9.out:430`), `Stripped` (`:414`), `SignerForged` (`:422`), `Reattributed` (`:439`), witnesses reachable (`:616`, `:848`, `:1091`) — the same four greens `cap18b_sp2_strict_cc3.out` records (`:381`, `:388`, `:395`, `:402`; witnesses `:578`, `:809`, `:1051`), and it still **matches S-P2's own strict ablation** over the queries that ablation declares (`s-p2/RESULTS.md:103-120`, `d9_strict_c2_mutation.out:395`, `:578`, `:809`, `:1051`). **Red: C-Q9 `PossessionUnbound` `is false`** (`cap20a…:1319`) **and link 3 with it** — the mutation produces and accepts `(POSS, fp(kX))` where C-Q9 and link 3 require `(POSS, t)`, which strict authority verification does not repair. **Which removal reds it, shown by isolation:** restoring possession-over-tuple with the frame's manifest-hash guard **still absent** makes **C-Q9 green** (`cap20b_sp2_strict_cc3_q9_poss_restored.out:1098`), the four safety queries green (`:414`–`:438`), witnesses reachable (`:615`, `:847`, `:1090`) — **the red is the fingerprint-only possession, not the missing hash guard**. This is the **(α)/(β) split C-C8's cell already records** (§9(2)): set integrity green, the exact possession-message relation red. **Set-completeness note, corrected** *(REPAIR 2026-09-17, Codex round 7 finding 1)*: `cap18b` declares **neither `Spliced` nor C-Q9**; **C-Q9 is now descended** by `cap20a`, and **`Spliced`'s green in strict remains predicted**, on the descent of the retained set column, not descended here. **(b): MIXED, PREDICTED the same way** — basis **channel symmetry** (the two authority processes are interchangeable in §1.1's fixture), never a second run. **The round-six text, withdrawn and quoted:** “**(a): GREEN CONTROL, DESCENDED** *(REPAIR 2026-09-17, Codex round 6 finding 2)* — the same mutation made strict the same way leaves **every query the model declares green**: `Stripped` (`cap18b_sp2_strict_cc3.out:381`), `SignerForged` (`:388`), `SetAltered` (`:395`), `Reattributed` (`:402`), with both `HonestComplete` branches (`:578`, `:809`) and `HonestAccepted` (`:1051`) reachable. It **matches S-P2's own strict ablation** (`s-p2/RESULTS.md:103-120`, `d9_strict_c2_mutation.out:395`, `:578`, `:809`, `:1051`). **Set-completeness note:** `cap18b` declares **no `Spliced` query** — as the source model does not — so `Spliced`'s green in strict is **predicted**, on the descent of the retained set column, not descended here. **(b): green control, PREDICTED** — basis **channel symmetry**, never a second run.” — its “every query the model declares green” was true of `cap18b` and false of the capstone's query set, and its set-completeness note named the smaller of the two omissions. **(c): not stated — (c) is C-C1's run.** **The withdrawn text, quoted:** “(a), (b), (c): red predicted. No green-control reading: the trace behind `sp2_q5_c2_fponly_frame_nomh.out:535` takes zero `dsks` steps and reds over the honestly evidenced tuple, the adversary's key entering through the unbound manifest binding rather than through enrolment.” **False of the trace**: `sp2_q5_c2_fponly_frame_nomh.out:523-535` moves an honest key onto a **different, forged** one-signer tuple **STRICT OUTCOME IN THREE LISTS** *(REPAIR 2026-09-17, Codex round 8 finding 2)*. **(a) descended green:** C-Q5 `SetAltered` (`cap20a_sp2_strict_cc3_q9.out:430`), `Stripped` (`:414`), `SignerForged` (`:422`), C-Q3 `Reattributed` (`:439`); witnesses both `HonestComplete` (`:616`, `:848`) and `HonestAccepted` (`:1091`). **(a) descended red:** C-Q9 `PossessionUnbound` (`:1319`). **(a) predicted:** **link 3 red**, `ChainBroken` being declared in no model — what is descended is link 3's **relation**, judged structurally by `cap20a`'s C-Q9 judge; and **predicted green** — `Spliced`, `TypeConfused`, `VersionLied`, C-Q2, C-Q4, C-Q7, C-Q8, links 1a, 1b, 2a, 2b, 4, 5, 6a, 6b, on the descent of the retained set column, `cap20a` declaring none of them. **(b): the same three lists, every entry PREDICTED** — basis channel symmetry; no `_repo` variant of `cap20a` was made or exists. **No green-control reading in any case, descended or predicted.** |
| **C-C4** | The complete key-binding relation removed inside `InnerCheck`: inner `=fp(kI)` pin **and** `mhI = h(tI)` | **Five, in capstone names** — three family-local by design (C-Q4's `Rescoped` `s4_innerfp_mh.out:864`, `InnerSigTransplanted` `:1207`, and C-Q3 `:1431`) **plus** **link 6b** and **link 5**'s frame-to-key half at the inner layer, neither of which any family model declares. **Link 6b's red survives its restatement** *(REPAIR 2026-09-17, Codex round 6 finding 1)*: under the restated form (§3, link 6b) the link compares the **envelope path's attribution report** against the **innermost frame's** `(fp(kX), id)`, and C-C4 removes the inner `=fp(kI)` pin and `mhI = h(tI)` **inside `InnerCheck`**, so the inner frame the report is compared against is no longer bound to the accepting key at all — the red is at the **inner layer**, as before, and for the same mechanism. The membership is **not descended** either way. *[Corrected — skeptic 2026-09-15: the cell read "three by design" and then listed five; the ledger's "three" is the family-local count (`:1497`), not the capstone set.]* **Simplest alternative, which does not sever:** the inner `=fp(kI)` pin alone leaves every query green (`s3_innerfp.out:527`–`:566`) | `TypeConfused`, `VersionLied`, **link 6a** | `HonestWrappedAccepted`, `HonestAccepted` | D2 | `s4_innerfp_mh.out:864`, `:1207`, `:1431`, `:526`, `:1949`, `:1734`, `:1933`; isolation `s3_innerfp.out:527`-`:566` | **(d)** red, **descended** — the cited run is a copy of a **degraded, sole-channel** family model. (`s4_innerfp_mh`, a copy of S-P7's degraded depth-1 model.) **(a)/(b): red predicted, WITH THE GREEN-CONTROL READING NAMED.** S-P7's degraded fixture admits an **adversary-held wrapper key** (finding F7, `s-p7/RESULTS.md:45`), while its **strict** runs reach the wrapped witness only through the **honest wrapper `skW2`** (`:43-44`) and carry both outer authority checks, which §1.1's enrolment rule denies an adversary key. So in (a)/(b) this configuration is **either** red through a route the strict fixture can present **or** a **green control** — the shown instance of the same mechanism is C-C15(i) at `cap14b…:550`. **(c): not stated — (c) is C-C1's run** *(REPAIR 2026-09-17, Codex round 6 finding 4)*: §1.1's cases table registers (c) as companion **C-C1** and not as a correct-form run, so no other companion is stated for it. *The withdrawn phrase, quoted: “(c) as (a)/(b).”* It was false in substance as well as in form — (c) leaks **both** channel keys and so supplies the attacker-controlled authorized wrapper key whose absence is the whole reason (a)/(b) can be green controls (`cap19b_sp7_strict_both_leaked_q6b.out:843`, `:1151`, `:1450`). Which way the strict runs fall is an **observation of the run**, recorded in `RESULTS.md`. *(REPAIR 2026-09-17, Codex round 5 finding 2)* **STRICT OUTCOME IN THREE LISTS** *(REPAIR 2026-09-17, Codex round 8 finding 2)*. **(a)/(b) descended green: NONE. Descended red: NONE.** `s4_innerfp_mh` and `s3_innerfp` are **degraded** S-P7 models and **no strict run of this companion exists**. **Predicted, all of it:** either the five members of set (1) red with set (2) green and both witnesses reachable, **or** the configuration green throughout — the fork this cell already states, now stated as a **predicted configuration-level reading** and never a descended one. **The cross-reference it rests on is amended:** C-C15(i) at `cap14b…:550` is **descended green over the four S-P7 queries and two witnesses `cap14b`/`cap14c` declare** and **predicted** over C-Q7, C-Q8, C-Q9 and the linkage conjuncts (§9(1), C-C15's Cases cell), so it is no longer the shown instance of anything at configuration level. **(c)/(d): unchanged.** **WHAT THE INNER ACCEPTANCE REPORTS UNDER THIS MUTATION** *(REPAIR 2026-09-17, Codex round 9 finding 1)*: C-C4 removes the inner `=fp(kI)` pin and `mhI = h(tI)` **inside `InnerCheck`** and leaves the accepting key and the possession and evidence checks alone, so under §1.3's report contract the inner `LayerAccepted` carries the **presented inner** `(tI, ppfI, sgI, fbI)` under **`kI`** — the key this mutated verifier still verifies the inner signature against — and those are the same terms checks 1 and 6 examine. **No predicted outcome changes:** C-Q9 and link 3 stay **predicted green** and their green does **not** turn on the report choice, the possession check being over exactly the reported `(t, ppf)` pair; what the mutation unbinds is the frame's key and hash binding, which is why set (1) already names **link 5's frame-to-key half** and **link 6b** and no possession member. |
| **C-C5** | The inner signature unbound from the presented bytes inside `InnerCheck`: `let (=BYTES, anyb) = checksign(sgI, kI)` | C-Q4's `InnerSigTransplanted`; **C-Q8** and **link 4** at the inner layer | `TypeConfused`, C-Q4's `Rescoped`, C-Q3, `VersionLied`, links 6a, 6b | `HonestWrappedAccepted`, `HonestAccepted` | D5, **as evidence that byte binding matters, not as the discharge** | **Nearest alternative, which severs a *different* fact:** removing the inner signature check outright reds the same query but by severing an S-P7 check, the a11 shape (`s2_sig_removed.out:852`) — *named here as the mechanism-review contrast the ledger states at `:1498` and the draft cited without saying what it contrasts (skeptic 2026-09-15).* `s1_sig_unbound.out:897`, `:537`, `:560`, `:920`, `:1464`, `:1233`, `:1442`; contrast `s2_sig_removed.out:852` | **(d)** red, **descended** — the cited run is a copy of a **degraded, sole-channel** family model. (`s1_sig_unbound`, S-P7 degraded.) **(a) AND (b): MIXED, DESCENDED** *(REPAIR 2026-09-17, Codex round 8 finding 1)*. C-C5's registered unbinding transcribed onto the **correct strict** S-P7 model, with C-Q8's structural signature/bytes judge (`BytesUnbound`) added over accepted `(key, signature, presented bytes)` triples and **restricted to wrapped inner acceptances**, and with the fixture, both authority checks, the possession checks and the frame checks all intact, is **red on C-Q8** and **green on the rest**. **Descended red:** C-Q8's structural judge — `cap21d_sp7_strict_cc5_wrapped.out:869` in case **(a)** (DNS leaked) and `cap21e_sp7_strict_cc5_wrapped_repo.out:868` in case **(b)** (repository leaked). **Link 4 red with it, by shape:** `ChainBroken(lyr, LINK_4)` is declared in no model, so link 4's red is **not descended as a `ChainBroken` result**; what **is** descended is **link 4's relation, judged structurally on a family copy**, exactly as `cap20a` descends C-Q9 for C-C3 and `cap13b` descends link 2a's shape for C-C17. **Descended green:** C-Q4's `InnerSigTransplanted` (`cap21d:956`; `cap21e:954`), C-Q4's `Rescoped` (`cap21d:927`; `cap21e:926`), `TypeConfused` (`cap21d:898`; `cap21e:897`) and C-Q3 `Reattributed` (`cap21d:985`; `cap21e:982`). **Witnesses descended reachable:** `HonestWrappedAccepted` (`cap21d:1336`; `cap21e:1333`) and `HonestAccepted` (`cap21d:1563`; `cap21e:1559`). **Against the matched strict baseline, green on the same judge:** `cap21b_sp7_strict_base_sigbytes_wrapped.out:594`. **Predicted, with the basis named:** `VersionLied`, links 6a and 6b, and every other member of the retained set column — green, on the descent of that column; **`cap21b`, `cap21d` and `cap21e` declare C-Q8's judge, the four S-P7 safety queries and two witnesses and nothing else** (`cap21d_sp7_strict_cc5_wrapped.pv:126-145`). **THE ATTACK, STATED:** the issuer's **honest wrapper signature**, made under its **honestly authorized** key, is carried as the **inner** signature accompanying different, **attacker-built** attestation bytes; both authority checks pass, and **no adversary-enrolled key is needed**. It is the **same-key-wrapping consequence C-C7(ii) already records** (§4, C-C7, `cap7b…:1032-1072`), now at the **inner** layer, and §1.1's compromised-channel-only enrolment rule does not reach it. **The whole-configuration green-control alternative is WITHDRAWN. The withdrawn text, quoted:** “**(a)/(b): red predicted, WITH THE GREEN-CONTROL READING NAMED.** The trace behind `s1_sig_unbound.out:897` runs the **D-4 `dsks` route**, and a `dsks`-derived key needs authority for **its own** tuple, which §1.1's compromised-channel-only rule denies in strict. The configuration may therefore be a **green control** in (a)/(b) — a registered outcome.” **What was wrong:** the `dsks` reading explains why `InnerSigTransplanted` can stay green in strict; it says **nothing** about C-Q8 and link 4, whose structural relation an **honestly authorized** key can break. **Neither contestable fixture choice is reversed** — same-key wrapping and the compromised-channel-only enrolment reading both stand, and finding 1 is a **consequence** the enrolment argument does not exclude, not a reversal of it. **Set (1)'s C-Q8 and link 4 are therefore DESCENDED IN STRICT as well as registered in (d)**; set (1) itself is unchanged, this row having listed them since it was written. **(c): not stated — (c) is C-C1's run** *(REPAIR 2026-09-17, Codex round 6 finding 4)*; *the withdrawn phrase, quoted: “(c) as (a)/(b)”* — (c) leaks both keys and is not a configuration of (a)/(b) (`cap19b…:843`). Which way the strict runs fall is an **observation of the run**, recorded in `RESULTS.md`. *(REPAIR 2026-09-17, Codex round 5 finding 2)* |
| **C-C6** | The **conditional** unbinding: presented bytes must equal signed bytes only when the signed frame's own `kfp` matches the verifying key | **C-Q7**; C-Q4's `InnerSigTransplanted`; **predicted** also C-Q8 and link 4, since the structural relation fails wherever the condition waives it | **the whole point**: `AcceptedUnderHonestKey ⟹ IssuerSigned` stays green, C-Q3 stays green, with `TypeConfused`, C-Q4's `Rescoped`, `VersionLied` | `HonestAccepted`, `HonestWrappedAccepted` | D5, D6 | `d5a_sp1_condunbind.out:195`, `:371`; `d5b_sp7_condunbind.out:654`, `:1060`, `:1037`, `:677`, `:700`, `:1599`, `:1370`, `:1576`; `d5d…:414`, `:422`, `:599`. **UNCHANGED by §1.1's same-key wrapper signer** *(REPAIR 2026-09-17, Codex round 2 finding 3)*: with the honest `OT_WRAPPER` signer under `skI` and the `OT_ATTEST` pin added to C-C6's own mutation, `cap7c_sp1_condunbind_wrapper_signer.out:448`, `:456`, `:633`, `:784` match `d5d_sp1_sigjudge_condunbind.out:414`, `:422`, `:599`, `:750` **result for result** — C-Q7 `is false`, honest-key authorship `is true`, witness reachable, Q2(ii) `is false` — because **C-C6's waiver keys on the signed frame's own `kfp`, which the wrapper frame does name**. This run the reviewer did not make | **(d)** red, **descended** — the cited run is a copy of a **degraded, sole-channel** family model. (`d5d_sp1_sigjudge_condunbind`, S-P1 degraded.) **(a)/(b): red predicted, WITH THE GREEN-CONTROL READING NAMED** — the trace behind `d5d…:414` runs the **D-4 `dsks` route**, whose derived key §1.1's rule denies authority in strict. **(c): not stated — (c) is C-C1's run** *(REPAIR 2026-09-17, Codex round 6 finding 4)*; *the withdrawn phrase, quoted: “(c) as (a)/(b)”* — (c) leaks both keys and is not a configuration of (a)/(b) (`cap19b…:843`). Which way the strict runs fall is an **observation of the run**, recorded in `RESULTS.md`. *(REPAIR 2026-09-17, Codex round 5 finding 2)* **STRICT OUTCOME IN THREE LISTS** *(REPAIR 2026-09-17, Codex round 8 finding 2)*. **(a)/(b) descended green: NONE. Descended red: NONE.** `d5d_sp1_sigjudge_condunbind` and `cap7c_sp1_condunbind_wrapper_signer` are **degraded** S-P1 models and **no strict run of this companion exists**. **Predicted, all of it:** C-Q7 and C-Q4's `InnerSigTransplanted` red, C-Q8 and link 4 red, set (2) green, both witnesses reachable — **or** the configuration green, which is this cell's stated fork, now a **predicted** configuration-level reading and never a descended one. **AND THE GREEN-CONTROL READING IS WEAKENED, NOT WITHDRAWN** *(REPAIR 2026-09-17, Codex round 8 finding 1)*: C-C6's waiver keys on the **signed frame's own `kfp`**, which §1.1's same-key **wrapper** frame does name — that is why `cap7c_sp1_condunbind_wrapper_signer.out:448` matches `d5d…:414` result for result — so the **honest wrapper signature under an honestly authorized key** that reds C-C5's C-Q8 in strict (`cap21d…:869`) is material §1.1's fixture supplies **without any enrolled key**. The enrolment rule therefore does not by itself secure a green control here. **Which way (a) and (b) fall is an observation of the run, and this cell predicts neither colour.** **THE STRICT RUN NOW EXISTS, AND (a) AND (b) ARE DESCENDED GREEN OVER WHAT IT DECLARES** *(REPAIR 2026-09-17, Codex round 9 disposition 4 — the test the reviewer was asked for, and made)*. **Two sentences are withdrawn.** *First, quoted: “**Which way (a) and (b) fall is an observation of the run, and this cell predicts neither colour.**”* *Second, the round-eight qualification, quoted in full: “**AND THE GREEN-CONTROL READING IS WEAKENED, NOT WITHDRAWN** *(REPAIR 2026-09-17, Codex round 8 finding 1)*: C-C6's waiver keys on the **signed frame's own `kfp`**, which §1.1's same-key **wrapper** frame does name — that is why `cap7c_sp1_condunbind_wrapper_signer.out:448` matches `d5d…:414` result for result — so the **honest wrapper signature under an honestly authorized key** that reds C-C5's C-Q8 in strict (`cap21d…:869`) is material §1.1's fixture supplies **without any enrolled key**. The enrolment rule therefore does not by itself secure a green control here.”* **What it got wrong:** it inferred from C-C5's strict red that C-C6's waiver reaches the same material. It does not — and the reason is the very clause it cited. **The run.** C-C6's conditional unbinding applied to the **strict** S-P7 copy carrying C-Q8's wrapped byte-binding judge, with §1.1's same-key wrapping retained and nothing else changed: **(a), DNS leaked — descended green on the five queries the copy declares:** the wrapped C-Q8 relation `BytesUnbound` (`cap22b_sp7_strict_cc6.out:692`), `TypeConfused` (`:722`), C-Q4's `Rescoped` (`:752`), **C-Q4's `InnerSigTransplanted`** (`:782`) and C-Q3 `Reattributed` (`:812`); **witnesses descended reachable:** `HonestWrappedAccepted` (`:1161`) and `HonestAccepted` (`:1386`); against the matched strict baseline, green on the same judge (`cap22a_sp7_strict_cc6_base.out:594`–`:658`; witnesses `:993`, `:1204`). **(b), repository leaked — the same, descended in its own right:** `cap22c_sp7_strict_cc6_repo.out:693`–`:817` (the five at `:693`, `:724`, `:755`, `:786`, `:817`), witnesses `:1167`, `:1393`. **Descended red: NONE, in either case.** **Why C-C5's route does not open here:** C-C6 waives byte equality **only when the signed frame's own `kfp` does NOT match the verifying key**, and §1.1's same-key wrapper frame **names the verifying key's fingerprint** — so on that route equality is **demanded**, not waived, and C-C5's strict failure does not reproduce. **Predicted green, with the basis named:** **C-Q7**, the generic signature-term judge, and the **linkage conjuncts** — links 1a, 1b, 2a, 2b, 3, 4, 5, 6a, 6b — together with C-Q5, C-Q9, `Stripped`, `SignerForged`, `Spliced` and `VersionLied`; `cap22a`/`cap22b`/`cap22c` declare **five queries and two witnesses and nothing else**, so none of these is descended, and the basis is the descent of the retained column plus the waiver's own condition above. **Configuration-level reading: a GREEN CONTROL in (a) and (b), PREDICTED and never descended** — the mutation is present, every query the copies declare is green and both witnesses are reachable, and the predicted members carry the basis just stated. It is a **predicted** reading exactly as §4's preamble requires; “green control, descended” remains a label this file does not use. **Set (1) is not edited:** C-Q7 and C-Q4's `InnerSigTransplanted` remain registered reds for **(d)**, descended there (`d5d…:414`; `d5b_sp7_condunbind.out:1037`), and C-Q8 and link 4 remain **predicted** reds for (d); their strict green is a **registered per-case outcome**, the same shape as C-C7(ii)'s C-Q7 — red in the composed degraded run, green in strict — and not a divergence. |
| **C-C7** | **Two configurations, both required.** (i) same-key byte unbinding: the signature must verify under `kX` over *some* frame naming `fp(kX)`, not over the presented bytes. (ii) type-conditional unbinding: byte equality required only when the signed frame's `objType` is `OT_ATTEST` | **C-Q8** and **link 4**, in both configurations; in (i) also `AcceptedUnderHonestKey ⟹ IssuerSigned`; **AND, IN (a) AND (b), THE UNRESTRICTED `AcceptS ⟹ IssuerSigned`, IN BOTH CONFIGURATIONS, RED — (a) DESCENDED, (b) PREDICTED** *(DESCENT SPLIT — REPAIR 2026-09-17, Codex round 13 finding 3. **The withdrawn label, quoted:** “**AND, IN (a) AND (b), THE UNRESTRICTED `AcceptS ⟹ IssuerSigned`, IN BOTH CONFIGURATIONS, DESCENDED RED**”. **What was wrong:** the two runs it rests on leak `skD` **only** — `cap17b_sp1_strict_cc7i.out:1243` and `cap17c_sp1_strict_cc7ii.out:1284` — so both are **case (a)** runs; **case (b) was never run a second time** and is **predicted on channel symmetry**, exactly as this row's Cases cell already says of every case-(b) entry. **The prediction is unchanged — red in both cases and both configurations, and it stays in set (1) for (a) and (b) alike; only the DESCENT label is corrected**, and nothing else moves: no query, no probability, no timebox, no witness, no companion count)* *(REPAIR 2026-09-17, skeptic read S-4. **The withdrawn set-(1) text, quoted:** “**C-Q8** and **link 4**, in both configurations; in (i) also `AcceptedUnderHonestKey ⟹ IssuerSigned`.” **What was wrong:** the Cases cell of this same row descends the unrestricted form **red in strict** — configuration (i) `cap17b_sp1_strict_cc7i.out:1243`, configuration (ii) `cap17c_sp1_strict_cc7ii.out:1284`, both `RESULT event(AcceptS(…)) ==> event(IssuerSigned(…)) is false` — against a **green** matched strict baseline, `cap17a_sp1_strict_judges_base.out:555` `is true`, so in strict the red **is** a mutation effect; and the retained-query table registers that query **green** in (a)/(b). It was in **no** set, which under §4's replacement rule makes the builder read a registered severing as a broken fixture. **§4's builder note (2) does not cover it** — *“the registered-red baselines are not mutation effects”* is about **degraded** runs, where the unmutated baseline is already `is false` for the Q2(ii) cost; here the strict baseline is green. **In (d) the unrestricted form is NOT listed here**, for exactly that reason. **Nothing else moves:** no query, no probability, no timebox, no witness, no companion count, and set (2) and set (3) are not edited)*. **CONFIGURATION (ii) RE-SPECIFIED 2026-09-17** *(REPAIR 2026-09-17, Codex round 2 finding 3, as a **consequence** of §1.1's same-key-wrapping fixture choice, not as a new severing)*: in the **composed** fixture (ii)'s failed set is larger and also contains **C-Q7** (`cap7b_sp1_q8_wrapper_signer_type_conditional.out:528` `is false`), **honest-key authorship** `AcceptedUnderHonestKey ⟹ IssuerSigned` (`:1072` `is false`), and the **round-3 honest-filtered C-Q8** (`:711` `is false`) **beside** the structural C-Q8 (`:904` `is false`) and link 4. **The attack, from the trace at `cap7b…:1032-1072`:** an adversary-built `OT_ATTEST` frame presented under the honest key `pk(skI)`, carrying the issuer's own honest **wrapper** signature, accepted because the **signed** frame is not `OT_ATTEST` and byte equality is waived for it. **Descended** (`cap7b`), against a baseline in which the same signer breaks nothing under correct byte binding (`cap7a_sp1_q8_wrapper_signer_base.out:310`, `:316`, `:322`, `:330` all `is true`; witness `:507`) | in (i) **C-Q7 stays green** — `d6e…:274`, and with §1.1's wrapper signer present `cap7d_sp1_q8_samekey_unbound_wrapper_signer.out:312`. **For (ii) the “whole point” sentence is WITHDRAWN IN PLACE** *(REPAIR 2026-09-17, Codex round 2 finding 3)*. *The withdrawn text, quoted: “**the whole point**: in (i) **C-Q7 stays green**; in (ii) **C-Q7 and honest-key authorship both stay green**.”* In the **composed** fixture they do not: §1.1's same-key wrapping puts an honest `OT_WRAPPER` signature under `skI` within reach of the waiver, and both go red (`cap7b…:528`, `:1072`). **(ii)'s set (2) is therefore the links and judges that do not touch byte binding** — C-Q3, C-Q4's `Rescoped` and `InnerSigTransplanted`, C-Q5, C-Q9, links 1a, 1b *(in strict only — C-Q1-degraded does not assert link 1b, `:314-318`; REPAIR 2026-09-17, Codex round 13 finding 2, carried)*, 2a, 2b, 3, 5, 6a, 6b, `Stripped`, `SignerForged`, `Spliced`, `TypeConfused`, `VersionLied` — **predicted, not descended**, the S-P1 diagnostic declaring none of them. **And the quantifier-gap contrast (ii) used to carry is registered NOT to reproduce here:** the contrast — the round-3 honest-filtered C-Q8 **green** while the structural form is **red** — is shown **family-locally** at `d6d_sp1_q8_type_conditional_unbound.out:315` against `:507`, and it is registered **not** to reproduce in the composed fixture, **because** the honest wrapper signature is an **honest-released signature term over non-attest bytes**, so the honest filter no longer excludes the attack and the filtered form catches it too (`cap7b…:711`). **A green honest-filtered C-Q8 in the capstone's (ii) is a divergence from this registration, not a success** | `HonestAccepted` in both — (i) `d6e…:989`, with the signer `cap7d…:1027`; (ii) `d6d…:692`, with the signer `cap7b…:1250` | D6 | baseline `d6c_sp1_q8_judge_all.out:284`, `:272`, `:292`, `:469`; (i) `d6e…:643`, `:274`, `:989`; (ii) `d6d…:507`, `:315`, `:308`, `:515`, `:692`. **Same-key-wrapper-signer runs, 2026-09-17** (Codex round 2 finding 3): baseline `cap7a_sp1_q8_wrapper_signer_base.out:310`, `:316`, `:322`, `:330`, `:507`; (ii) `cap7b_sp1_q8_wrapper_signer_type_conditional.out:528`, `:711`, `:904`, `:1072`, `:1250`; **(i) unchanged by the signer** — `cap7d_sp1_q8_samekey_unbound_wrapper_signer.out:312`, `:493`, `:681`, `:847`, `:1027`, `:1206` match `d6e_sp1_q8all_samekey_unbound.out:274`, `:455`, `:643`, `:809`, `:989`, `:1168` **result for result**, because (i) demands that the **signed** frame name `fp(kX)` and the wrapper frame names the issuer's own fingerprint. The `cap7d` run the reviewer did not make | **(d)** red, **descended** — the cited runs are copies of **degraded, sole-channel** S-P1 models (`d6e` for (i), `d6d` for (ii), and the composed `cap7b`). **(a): BOTH CONFIGURATIONS MIXED, DESCENDED PER QUERY** *(REPAIR 2026-09-17, Codex round 6 finding 3)*. The matched **strict** baseline — S-P1 strict with the C-Q7 judge, both C-Q8 judges and §1.1's same-key `OT_WRAPPER` signer added, every check correct — is **all green**: C-Q7 (`cap17a_sp1_strict_judges_base.out:338`), both C-Q8 (`:344`, `:350`), honest-key authorship (`:358`), the unrestricted `AcceptS ⇒ IssuerSigned` (`:555`), witness reachable (`:547`). **(i) same-key byte unbinding, on that model:** **C-Q7 green** (`cap17b_sp1_strict_cc7i.out:340`); **both C-Q8 forms red** (`:533`, `:709`); **honest-key authorship red** (`:887`); the unrestricted form red (`:1243`); witness reachable (`:1079`). **(ii) type-conditional unbinding:** the **same shape** — C-Q7 green (`cap17c_sp1_strict_cc7ii.out:375`), both C-Q8 red (`:570`, `:748`), honest-key authorship red (`:928`), witness reachable (`:1118`). **NEITHER CONFIGURATION IS A GREEN CONTROL IN ANY CASE.** The preamble's definition requires **every** query green; in both configurations three are red and one is green. **Case-dependence, stated rather than hidden:** set (1) registers **C-Q7 red for (ii)** on the composed **degraded** run (`cap7b…:528`); in **strict** (ii)'s C-Q7 is **green** (`cap17c…:375`), and that difference is a registered per-case outcome, not a divergence. **(b): the same per-query outcomes, PREDICTED** — basis **channel symmetry**, never a second run. **(c): not stated — (c) is C-C1's run** *(REPAIR 2026-09-17, Codex round 6 finding 4)*. *The withdrawn text, quoted: “(a)/(b): red predicted, and the two configurations read differently. For (ii) the composed attack of `cap7b…:1032-1072` is an adversary-built `OT_ATTEST` frame presented under the honest key `pk(skI)` carrying the issuer's own honest wrapper signature — an honest-key route, which §1.1's enrolment rule does not touch, so no green-control reading is named for (ii)'s authorship and structural-C-Q8 reds. For (i), and for (ii)'s C-Q7 red, whose block runs the D-4 `dsks` route, the green-control reading IS named. (c) as (a)/(b).”* **What was wrong:** it offered a green-control reading for **configuration (i) as a whole**, which the strict run shows **mixed**, and it made the same offer for a **single query** of (ii) — a green control is a property of a **configuration**, every query green, never of one query inside a mixed one **STRICT OUTCOME IN THREE LISTS** *(REPAIR 2026-09-17, Codex round 8 finding 2)*. **(a), configuration (i) — descended green:** C-Q7 (`cap17b_sp1_strict_cc7i.out:340`). **Descended red:** the **round-3 honest-filtered** C-Q8 `SigBytesUnbound` (`:533`) and the **structural** C-Q8 `SigBytesUnboundAll` (`:709`) *(ATTRIBUTIONS EXCHANGED — REPAIR 2026-09-17, Codex round 9 finding 3. The withdrawn wording, quoted: “the structural C-Q8 (`:533`), the honest-filtered C-Q8 (`:709`)”. `cap17b_sp1_strict_cc7i.out:533` is `RESULT not event(SigBytesUnbound(kX_4,s,fbP_2)) is false.` and `:709` is `RESULT not event(SigBytesUnboundAll(kX_4,s,fbP_2)) is false.` — **both red, so the polarity is unchanged and no prediction moves; only the provenance of each citation is corrected**)*, honest-key authorship `AcceptedUnderHonestKey ⟹ IssuerSigned` (`:887`) and the unrestricted `AcceptS ⟹ IssuerSigned` (`:1243`). **Witness descended reachable:** `HonestAccepted` (`:1079`). **Predicted:** **link 4 red**, `ChainBroken` declared in no model and its relation descended by the two C-Q8 judges; **predicted green** — C-Q3, C-Q4, C-Q5, C-Q9, links 1a, 1b, 2a, 2b, 3, 5, 6a, 6b, `Stripped`, `SignerForged`, `Spliced`, `TypeConfused`, `VersionLied`, the S-P1 diagnostic declaring none of them. **(a), configuration (ii) — descended green:** C-Q7 (`cap17c_sp1_strict_cc7ii.out:375`). **Descended red:** both C-Q8 forms (`:570`, `:748`), honest-key authorship (`:928`) and the unrestricted form (`:1284`). **Witness:** `HonestAccepted` (`:1118`). **Predicted:** the same list as (i). **(b): the same three lists in both configurations, every entry PREDICTED** — basis channel symmetry, never a second run. **Neither configuration is a green control in any case, and neither is offered as a predicted one.** |
| **C-C8** | Both manifest-binding protections removed together: possession made fingerprint-only (the D-3 under-encoding, a broken companion by library definition) **and** the frames' `mh = h(t)` guards dropped. Seven-field frames, per-slot pins, tuple fingerprint matches and the three §A5.4 guards all retained | **C-Q9**; **C-Q5**; **link 3**, and **link 5**'s `mh` half | **the whole point**: S-P3's transcribed `PossessionTransplanted` stays green, with `Stripped`, `SignerForged`, C-Q3, `Spliced` | both `HonestComplete`, `HonestAccepted` | D10 | `d10b_sp2_q9_manifest_unbound.out:1462`, `:673`, `:1297`, `:454`, `:464`, `:683`, `:1287`, `:851`, `:1072`, `:1277`; baseline `d10a…:1111`, `:1104` **C-C8 severs TWO obligations, not one — REPAIRED 2026-09-16 (Codex finding 2).** (α) **Set integrity**: `SetAltered` (C-Q5), which needs the **combined** removal — either protection alone leaves it green. (β) **The exact possession-message relation**: C-Q9, `checksign(ppf, kX) = (POSS, t)`, which **possession unbinding alone already falsifies, by construction** — a fingerprint-only proof recovers `(POSS, fp(kX))` and no retained frame guard can change the message a possession signature recovers to. So **C-C8 is minimal for (α) and over-determined for (β)**, and this is established **before the freeze**, not left to a post-freeze amendment. **Shown by scratch run** (`ledger-tests-2026-09-14/cap2_sp2_poss_fponly.pv/.out`, possession made fingerprint-only and **nothing else**): **C-Q9 `is false`** (`:1263`) while **`SetAltered` stays `is true`** (`:471`), with `Stripped` (`:457`), `SignerForged` (`:464`), `Reattributed` (`:478`), `Spliced` (`:1097`), `PossessionTransplanted` (`:1104`) green and both `HonestComplete` (`:643`, `:861`) and `HonestAccepted` (`:1090`) reachable — against the baseline `d10a_sp2_q9_base.out:1111` `is true`. Reproduces the reviewer's `/tmp` diagnostic on our own tree. **The two isolation configurations `C-C8-i` and `C-C8-ii` are re-specified accordingly in §9(2)**, which the builder MUST run and record BEFORE C-C8's reds count; **`C-C8-i` is now the manifest-hash-only removal** (possession over the manifest **retained**), the one configuration that can be required to keep C-Q9 green, and **`C-C8-ii` the possession-only removal**, whose C-Q9 red is **registered, not a fixture break**. C-C8's minimality for `SetAltered` is still **shown by the isolation runs, not assumed** — the discipline C-C2 (`LEDGER.md:1495`), C-C3 (`:1496`) and C-C4 (`:1497`) carry and which `:1501` does not state for C-C8. | **(d)** red, **descended** — the cited run is a copy of a **degraded, sole-channel** family model. (`d10b_sp2_q9_manifest_unbound`, S-P2 degraded.) **(a): MIXED, DESCENDED PER QUERY** *(REPAIR 2026-09-17, Codex round 6 finding 2)* — C-C8's mutation made strict the same way (the second, uncompromised authority process and check added, DNS leaked, the mutation retained): **`SetAltered` green** (`cap18c_sp2_strict_cc8.out:509`), **`PossessionTransplanted` green** (`:1202`), **C-Q9 RED** (`:1431`), with `Stripped` (`:487`), `SignerForged` (`:498`), `Reattributed` (`:520`) and `Spliced` (`:1191`) green and the witnesses reachable (`:701`, `:935`, `:1180`). **This is exactly the (α)/(β) split this row already records** — obligation (β), the exact possession-message relation, reds in strict because possession unbinding falsifies it **by construction**; obligation (α), set integrity, does **not** red in strict. It is therefore **neither a green control nor an all-red companion**, and both halves are registered as run. **(b): the same split, PREDICTED** — basis **channel symmetry**, never a second run. **(c): not stated — (c) is C-C1's run** *(REPAIR 2026-09-17, Codex round 6 finding 4)*. **The withdrawn text, quoted:** “(a), (b), (c): red predicted. No green-control reading: the trace behind `d10b…:1462` takes zero `dsks` steps and the accepted tuple is honestly evidenced.” **False of the trace** — `d10b_sp2_q9_manifest_unbound.out:661-673` forges authority evidence over a **changed** tuple — **and false of the outcome**: C-Q5 is green in strict. **The two isolation configurations of §9(2) carry the same split**, stated there **STRICT OUTCOME IN THREE LISTS** *(REPAIR 2026-09-17, Codex round 8 finding 2)*. **(a) descended green:** C-Q5 `SetAltered` (`cap18c_sp2_strict_cc8.out:509`), `PossessionTransplanted` (`:1202`), `Stripped` (`:487`), `SignerForged` (`:498`), C-Q3 `Reattributed` (`:520`) and `Spliced` (`:1191`); witnesses (`:701`, `:935`, `:1180`). **(a) descended red:** C-Q9 `PossessionUnbound` (`:1431`). **(a) predicted:** **link 3 and link 5's `mh` half red**, `ChainBroken` declared in no model and the relation descended by `cap18c`'s C-Q9 judge; **predicted green** — C-Q2, C-Q4, C-Q7, C-Q8, links 1a, 1b, 2a, 2b, 4, 6a, 6b, `TypeConfused`, `VersionLied`. **(b): the same three lists, every entry PREDICTED** — basis channel symmetry, never a second run. **No green-control reading in any case; the cell's own (α)/(β) split is what the three lists make explicit.** **LINK 5's `mh` HALF IS DESCENDED GREEN IN STRICT, AND LINK 3 IS DESCENDED RED** *(REPAIR 2026-09-17, Codex round 9 finding 2)*. *The withdrawn wording, quoted: “**(a) predicted:** **link 3 and link 5's `mh` half red**, `ChainBroken` declared in no model and the relation descended by `cap18c`'s C-Q9 judge”.* **It was wrong on both halves, and wrong in the same way: C-Q9 tests the possession message, not the frame's manifest hash**, so it could descend the one relation and never the other. A judge reporting each accepted slot's `(t, frame)` and firing on **`mh ≠ h(t)`** was added to `cap18c`'s shape and run. **(a) descended GREEN — link 5's `mh` half:** `cap22h_sp2_strict_cc8_mh.out:1478`, with **C-Q9 still red** (`:1466`), the rest green (`:512`, `:524`, `:536`, `:549`, `:1224`, `:1236`) and the witnesses reachable (`:731`, `:966`, `:1212`). **(b) descended GREEN, the same:** `cap22i_sp2_strict_cc8_mh_repo.out:1477`, C-Q9 red (`:1465`), the rest green (`:512`, `:524`, `:536`, `:548`, `:1223`, `:1235`), witnesses reachable (`:730`, `:965`, `:1211`) — so **(b) is descended here in its own right and not predicted**. **The degraded control, red, which is what makes the strict green a result and not a dead judge:** the same judge on C-C8's degraded source is **red** (`cap22j_sp2_degraded_cc8_mh.out:1665`), beside `SetAltered` red (`:701`) and C-Q9 red (`:1499`), with the witnesses reachable (`:882`, `:1105`, `:1311`). **The reason, stated:** in strict the **honest channel's tuple pin** keeps `mh = h(t)` even with the frames' guards dropped — the adversary cannot present a tuple the honest authority did not evidence — while in degraded the sole channel is forgeable and the dropped guard is exploitable. **Link 3 STAYS descended red**, and its descent is unchanged in kind: `ChainBroken(lyr, LINK_3)` is declared in no model, but **link 3's relation IS C-Q9's**, which `cap18c…:1431` and `cap22h:1466` / `cap22i:1465` red directly. **What the runs therefore show is a (β)-ONLY strict split:** of C-C8's four set (1) members, **C-Q9 and link 3 red in strict** (obligation β) while **C-Q5 `SetAltered` and link 5's `mh` half are GREEN in strict** (obligation α, and now the frame-hash half with it). **Set (1) is not edited:** C-Q5 and link 5's `mh` half remain registered reds for **(d)**, where they are descended (`d10b…:673`; `cap22j:701`, `:1665`), and their strict green is a **registered per-case outcome**, exactly as C-Q5's already is in this cell — not a divergence. **This strengthens, and does not disturb, the (α)/(β) split this row has recorded since 2026-09-16.** |
| **C-C9** | The required-set requirement dropped from the one-signer branch: `let authTuple(id, kfprA, =signers0, alg, ver) = t in` becomes `… ss …`, so a two-signer manifest completes through the one-signer branch. **Every per-slot check retained** | **C-Q1 link 2b**, the two-signer set's slot-B conjunct — **stated over the layer-indexed projection `SlotSatisfied(aid, lyr, t, slot)`, at the layer whose `AcceptanceComplete(aid, lyr, t)` fired** *(REPAIR 2026-09-17, Codex round 3 finding 1: the row named the conjunct and inherited the projection from §3, which then carried no `lyr`; under an `aid`-only projection this companion's slot-B red can be absorbed by a slot-B report from another layer of the same presentation, `cap9_sp2_slots_projection_no_lyr.out:1239` against `:1454`)*; **`Stripped`** | **the point**: link 2b's slot-A and one-signer conjuncts, **at the same layer and over the same layer-indexed projection** *(REPAIR 2026-09-17, Codex round 3 finding 1)*, **link 2a**, `SignerForged`, C-Q5, C-Q3, `Spliced`, **C-Q9** | both `HonestComplete`, `HonestAccepted` | **D7** | `cq1d_sp2_slots_missing.out:1519`, `:643`, `:1353`, `:1333`, `:650`, `:657`, `:664`, `:1305`, `:1312`, `:1319`; baseline `cq1c…:1161`, `:1175`, `:1189` | **(d)** red, **descended** — the cited run is a copy of a **degraded, sole-channel** family model. (`cq1d_sp2_slots_missing`, S-P2 degraded.) **(a), (b): red PREDICTED**, basis the **structural descent** of the degraded run rather than any reading of its trace: the mutation makes a two-signer manifest complete through the **one-signer branch**, so the slot-B report **never occurs** and the route needs **no adversary key and no authority evidence at all** — nothing the enrolment rule or the channel count bounds is in it. **(c): not stated — (c) is C-C1's run** *(REPAIR 2026-09-17, Codex round 6 finding 4)*; *the withdrawn phrase, quoted: “(a), (b), (c): red predicted”*. **No strict run of this companion exists, so neither (a) nor (b) is descended** *(REPAIR 2026-09-17, Codex round 6 finding 2)*. *Also withdrawn and quoted: “(`cq1d…out:1519`, zero `dsks` steps)” — a `dsks` count in a degraded trace is not a basis for a strict outcome.* Which way the strict runs fall is an **observation of the run**, recorded in `RESULTS.md`. *(REPAIR 2026-09-17, Codex round 5 finding 2)* **STRICT OUTCOME IN THREE LISTS** *(REPAIR 2026-09-17, Codex round 8 finding 2)*. **(a)/(b) descended green: NONE. Descended red: NONE** — `cq1d_sp2_slots_missing` is a **degraded** S-P2 model and **no strict run of this companion exists**. **Predicted red:** link 2b's slot-B conjunct and `Stripped`, basis the **structural descent** this cell already states — the mutation completes a two-signer manifest through the one-signer branch, so the slot-B report never occurs and the route needs no adversary key and no authority evidence at all. **Predicted green:** link 2b's slot-A and one-signer conjuncts at the same layer, link 2a, `SignerForged`, C-Q5, C-Q3, `Spliced`, C-Q9, and the rest of the ladder; both witnesses reachable. **No green control, descended or predicted.** |
| **C-C10** | **STATED PER MODE** *(REPAIR 2026-09-17, Codex round 6 finding 6)*, because **strict verification has two evidence checks and which one is deleted changes the outcome**. *The withdrawn wording, quoted: “The degraded verifier's evidence check removed, and nothing else: `let (=STMT_DIGEST, =h(t)) = checksign(ev, pkS) in` deleted, so the accepted evidence term is carried in unexamined. Everything else retained.” It named a **single** check, which exists only in (d), and left the builder to choose in (a)/(b).* **In (d)** — the **sole** channel's check, which is the only one there: `let (=STMT_DIGEST, =h(t)) = checksign(ev, pkS) in` deleted, the accepted evidence term carried in unexamined. **In (a) and (b)** — the **HONEST (uncompromised) channel's** check is the one deleted; the **compromised channel's check is RETAINED**, and so is every other check. The **observed evidence term** is the one the deleted check would have examined: the honest channel's `ev`, carried in unexamined and emitted to `AuthorityEvidence` with that channel's key. **The opposite deletion is not this companion**: it is registered below as C-C10's **isolation control** | **PER MODE** *(REPAIR 2026-09-17, Codex round 6 finding 6)*. **In (d):** **C-Q1 link 1a**, as before. **In (a)/(b):** **C-Q1 link 1a**; **C-Q1 link 1b**, the publication-provenance correspondence; **and the unrestricted `Accept ⇒ IssuerSigned`** — the last two **descended in (a)** (and **predicted in (b)** on channel symmetry, `cap17e` leaking `skD` only) on the strict model with the honest channel's check deleted, `AcceptS ⇒ (AuthorityPublishedDNS ∨ AuthorityPublishedRepo)` **`is false`** (`cap17e_sp1_strict_cc10_drop_honest.out:858`) and `AcceptS ⇒ IssuerSigned` **`is false`** (`:699`). **Link 1a is now DESCENDED too** *(REPAIR 2026-09-17, Codex round 7 finding 2)*: the structural link-1a judge over the carried evidence pair (§3, link 1a, per-channel form) is **red** on that same strict model — `cap20g_sp1_strict_cc10_drop_honest_evidence.out:1055` — beside link 1b (`:887`) and the unrestricted authorship (`:728`), with honest-key authorship (`:384`), C-Q7 and both C-Q8 (`:364`–`:376`) green and the witness reachable (`:569`). *The withdrawn text, quoted: “Link 1a itself stays **not descended** (`ChainBroken` is declared in no model); what is descended is **link 1b's shape**, as the correspondence”.* `ChainBroken` is still declared in no model; what `cap20g` descends is **link 1a's relation, judged structurally on a family copy**, the way `cap20a` descends C-Q9 for C-C3 | **PER MODE** *(REPAIR 2026-09-17, Codex round 6 finding 6)*. **In (d):** every other conclusion keeps its baseline outcome, in particular C-Q7, **C-Q8**, honest-key authorship, and links 2a–6b. **In (a), descended:** **honest-key authorship** `AcceptedUnderHonestKey ⇒ IssuerSigned` (`cap17e…:355`), **C-Q7** (`:335`) and **both C-Q8 forms** (`:341`, `:347`) all green, with the witness reachable (`:540`); **predicted green**, on the same descent: links 2a–6b, C-Q2–C-Q6, C-Q9. **In (b): the same, PREDICTED** — basis **channel symmetry**, never a second run; `cap17e` leaks `skD` only. **Note the asymmetry this makes explicit:** link 1b and the unrestricted authorship conclusion move **into** set (1) in strict, where in (d) link 1b is not asserted at all (§1.1's cases table) | `HonestAccepted`, `HonestChain(L0, t)` | **D4** | `cq1b_sp1_evidence_unchecked.out:466`, `:301`, `:307`, `:313`, `:474`, `:638`; baseline `cq1a…:304`, `:310`, `:316`, `:322`, `:330`, `:507` | **(d)** red, **descended** — the cited run is a copy of a **degraded, sole-channel** family model. (`cq1b_sp1_evidence_unchecked`, S-P1 degraded.) **(a): red, DESCENDED** *(REPAIR 2026-09-17, Codex round 6 finding 6)* — on the strict model with the **honest** channel's evidence check deleted, publication provenance is **red** (`cap17e_sp1_strict_cc10_drop_honest.out:858`) and the unrestricted `AcceptS ⇒ IssuerSigned` is **red** (`:699`), while honest-key authorship (`:355`), C-Q7 (`:335`) and both C-Q8 (`:341`, `:347`) stay green and the witness is reachable (`:540`). **(b): red, PREDICTED** — basis **channel symmetry**, never a second run. **(c): not stated — (c) is C-C1's run** *(REPAIR 2026-09-17, Codex round 6 finding 4)*. **ISOLATION CONTROL, REGISTERED AND MIXED** *(REPAIRED 2026-09-17, Codex round 7 finding 2; it was registered green)*: deleting the **COMPROMISED** channel's check instead **does sever link 1a**, and severs nothing else. **Link 1a red:** the verifier checks the retained channel's term but the acceptance carries §1.3's **pair**, the deleted channel's term among them unexamined, so the structural link-1a judge is **red** — channel-specific `cap20f_sp1_strict_cc10_drop_compromised_evidence.out:737`, and the weaker either-key form red too (`cap20e_sp1_strict_cc10_drop_compromised_either.out:732`). **Green:** publication provenance, link 1b's shape (`cap17d_sp1_strict_cc10_drop_compromised.out:547`; `cap20e…:572`, `cap20f…:577`) and the unrestricted `AcceptS ⇒ IssuerSigned` (`cap17d…:539`; `cap20e…:564`), C-Q7 and both C-Q8 and honest-key authorship (`cap17d…:335`–`:355`), witness reachable (`cap17d…:531`; `cap20e…:556`, `cap20f…:560`). **The withdrawn text, quoted:** “**ISOLATION CONTROL, REGISTERED AND GREEN** *(REPAIR 2026-09-17, Codex round 6 finding 6)*: deleting the **COMPROMISED** channel's check instead severs **nothing** — publication provenance (`cap17d_sp1_strict_cc10_drop_compromised.out:547`) and unrestricted authorship (`:539`) stay green, as do C-Q7 and both C-Q8 and honest-key authorship (`:335`–`:355`), witness reachable (`:531`). The control is **registered so the builder cannot choose which check to delete**: if the capstone's C-C10 run in (a)/(b) comes back all green, the wrong check was deleted, and that is a **broken fixture to be diagnosed**, not a finding. It adds **no companion, no query and no timeboxed entry**, running inside link 1a's existing box.” — it was read off a model that **declares no link-1a judge**, which is §4's preamble rule of this round. **The distinguishing signal, restated:** the control still stops the builder choosing which check to delete, but it is read off **link 1b**, not off all-green — **link 1b red ⇒ the HONEST check was deleted**, which is the companion C-C10 itself (`cap20g_sp1_strict_cc10_drop_honest_evidence.out:887` provenance red, `:728` unrestricted authorship red, `:1055` link 1a red); **link 1b green and link 1a red ⇒ the COMPROMISED check was deleted**, which is this control (`cap20e…:572` green against `:732` red). A run that comes back **all green, link 1a included**, is neither, and is a **broken fixture to be diagnosed**, not a finding. It adds **no companion, no query and no timeboxed entry**, running inside link 1a's existing box. *The withdrawn text, quoted: “(a), (b), (c): red predicted. No green-control reading, structurally: the mutation deletes the evidence check itself, so an unexamined evidence term is carried in and no key needs authority for anything. This is the one companion in the file whose red cannot depend on the enrolment reading.”* The last sentence stands; what was missing is **which** check, and the runs show the two choices give opposite outcomes **STRICT OUTCOME IN THREE LISTS** *(REPAIR 2026-09-17, Codex round 8 finding 2)*. **THE COMPANION (the HONEST channel's check deleted), (a) — descended red:** link 1b's publication-provenance correspondence (`cap17e_sp1_strict_cc10_drop_honest.out:858`; `cap20g_sp1_strict_cc10_drop_honest_evidence.out:887`), the unrestricted `AcceptS ⟹ IssuerSigned` (`cap17e:699`; `cap20g:728`) and **link 1a's structural judge** (`cap20g:1055`). **Descended green:** honest-key authorship (`cap17e:355`; `cap20g:384`), C-Q7 (`cap17e:335`; `cap20g:364`) and both C-Q8 forms (`cap17e:341`, `:347`; `cap20g:370`, `:376`). **Witness descended reachable:** `HonestAccepted` (`cap17e:540`; `cap20g:569`). **Predicted green:** links 2a–6b, C-Q2–C-Q6 and C-Q9, neither copy declaring them. **(b): the same three lists, every entry PREDICTED** — basis channel symmetry; `cap17e` and `cap20g` leak `skD` only. **THE ISOLATION CONTROL (the COMPROMISED channel's check deleted), (a) — descended red:** link 1a, channel-specific (`cap20f_sp1_strict_cc10_drop_compromised_evidence.out:737`) and either-key (`cap20e_sp1_strict_cc10_drop_compromised_either.out:732`). **Descended green:** link 1b (`cap17d_sp1_strict_cc10_drop_compromised.out:547`; `cap20e:572`; `cap20f:577`), the unrestricted authorship conclusion (`cap17d:539`; `cap20e:564`), C-Q7, both C-Q8 forms and honest-key authorship (`cap17d:335`–`:355`). **Witness descended reachable:** `HonestAccepted` (`cap17d:531`; `cap20e:556`; `cap20f:560`). **Predicted green:** links 2a–6b, C-Q2–C-Q6, C-Q9. **(b): the same, PREDICTED.** **The control is MIXED; it is not a green control and is not offered as a predicted one.** |

**Two notes the builder carries.** (1) **C-C3 and C-C8 overlap in the
composed fixture**: both remove the manifest binding, by different
routes, and both are predicted to red C-Q5, C-Q9 and link 3. They stay
two registered mutations because the ledger registers them for two
obligations (C-C3 is D10's consumer-side severing, C-C8 is C-Q9's
producer-side companion); whether their capstone sets coincide is
recorded as an observation of the run, not assumed either way. (2) **The
registered-red baselines are not mutation effects**: in every degraded
run `AcceptS ⟹ IssuerSigned` is `is false` in the unmutated baseline as
well as in the mutants (the Q2(ii) cost), and no set above claims it
(`:1499`, `:1500`, `:1503`).

## Companions the ledger requires but does not number

`LEDGER.md:1505-1520` says S-STANDING Q2, Q4, abl6 (D12) and Q3 (D13)
are *"to be transcribed rather than rebuilt"*, and that *"the capstone's
work is to show the same mutation red on the **consuming** query"*. The
A3.3 gate requires a companion that fails the **consuming** query, and
C-Q6 is that consumer; the ledger names the mutations and gives them no
number. They are registered here so the obligation is not lost, and the
numbering is flagged for the non-author review.

| # | Mutation | (1) Expected failed set | (2) Must stay green | (3) Witnesses | Row | Descends from | Cases |
|---|---|---|---|---|---|---|---|
| **C-C11** | S-STANDING Q2 transcribed: the TLR names attempts by a label read from the bundle instead of `h(attemptCore(...))`. Alternates Q4 (terminal disposition unchecked) and abl6 (TLR unsigned) | **C-Q6's standing conjunct — the HONEST-KEY forms and the unrestricted strict form alike**, descended `ss_q2_companionA_identity_declared.out:808`, `:986` (honest-key, `is false`) and `:630` (unrestricted) *(REPAIR 2026-09-17, Codex round 2 finding 1: the forms are named here so this row and C-Q6 §(6) agree; **the honest-key reds are D12's severing**, and they are what distinguishes C-C11 from C-C12, where the honest-key forms stay green)* | C-Q6's entitled-key conjunct; **C-Q6's conjunct 3, scope agreement** *(added 2026-09-17, REPAIR, Codex round 3 finding 2: a **standing** mutation does not change what the **envelope** path reports, so the two attribution reports still agree and `ScopeMisreported` stays unreachable; **predicted**, no model declaring C-Q6)*; C-Q4's `Rescoped`; link 6b | `HonestStandingEstablished` over a wrapped presentation, **and `HonestWrappedStandingAgreed`** *(added 2026-09-17 with conjunct 3)*. **VOCABULARY-WITNESS CONSEQUENCE, REGISTERED 2026-09-17** *(REPAIR 2026-09-17, Codex round 4 finding 2)*: under this row's **Q4 alternate** — the terminal disposition unchecked, `StandingDecide` reporting `ESTABLISHED` after lineage membership alone (`ss_q4_companionC_terminal_unchecked.pv:231-237`) — the **S2** witness `(ABSENT, SUPERSEDED)` and the **S4** witness `(ABSENT, ISSUANCE_REFUSED)` are **UNREACHABLE**, and that is a **registered consequence of the mutation, never a broken fixture**: the alternate deletes the branches that produce those two report shapes. Without this entry a faithful transcription of the alternate would be classified as a broken fixture by C-N1's rule, since C-Q6 lists the S4 witness among its required witnesses; C-N1 now carries the two-kinds distinction and this row carries the naming that distinction requires. **Descended, committed:** `ss_q4_companionC_terminal_unchecked.out:1708` (S2) and `:1838` (S4), both `is true` — unreachable — with the N1 honest-flow witness still **reachable** (`:1425`), exactly as `s-standing/RESULTS.md`'s SS.Q4 row already records (*"S2 and S4 witnesses **unreachable** … consequence of the mutation, the branches no longer exist"*). **Reproduced on the structural join with the paired scope judge:** `cap12g_ss_q1_join_terminal_unchecked.out` — S2 unreachable (`:3217`), S4 unreachable (`:3413`), while **`HonestStandingEstablished` stays reachable** (`:2873`) and the agreement witness **`HonestWrappedStandingAgreed` stays reachable** (`:1542`), and the standing correspondences go **red**: `EstablishedWrapped ⟹ Designated` unrestricted `is false` (`:810`) and its honest-key form `is false` (`:1136`), with S-STANDING's own honest-key `Established ⟹ Designated` forms `is false` at `:2190` and `:2514`. **C-Q6's conjunct 3 stays green in that run** — the key comparison and the identity comparison both unreachable, in the shapes §(1) now registers as the observers **`ScopeKeyOnly`** (`:1152`) and **`ScopeIdentityOnly`** (`:1160`) *(names registered 2026-09-17, skeptic read S-11; `cap12g`'s own `ScopeMisreported` is the withdrawn four-place key-only form, which is `ScopeKeyOnly`'s shape, and `ScopeIdentityWrong` is `ScopeIdentityOnly`'s)* — and the substitution stays excluded (`:1144`), which is what shows the alternate severs **standing** and not scope. **No other companion on the record has this effect, and that is checked rather than assumed:** under this row's **abl6** alternate (TLR unsigned) all five vocabulary witnesses stay reachable (`abl6_no_tlr_signature.out:1472`, `:1648`, `:1771`, `:1943`, `:2090`, all `is false`); under C-C11's own **Q2** mutation all five stay reachable (`ss_q2_companionA_identity_declared.out:1692`, `:1868`, `:1996`, `:2170`, `:2346`); and under **C-C12** all five stay reachable (`ss_q3_companionB_entitled_via_envelope.out:1357`, `:1558`, `:1686`, `:1883`, `:2055`). **The Q4 alternate is the only registered exception in this file** | D12 | `ss_q2_companionA_identity_declared.out:630`, `:808`, `:986`, `:1182`, `:1514`; `ss_q4…out:576`, `:849`, `:1123`, **and the vocabulary-witness lines `:1708`, `:1838`, `:1425` (2026-09-17)**; `abl6_no_tlr_signature.out:616`, `:788`, `:960`. **Structural-join reproduction of the Q4 alternate, 2026-09-17** (Codex round 4 finding 2): `cap12g_ss_q1_join_terminal_unchecked.out:810`, `:1136`, `:2190`, `:2514`, `:3217`, `:3413`, `:2873`, `:1542`, `:1144`, `:1152`, `:1160` | **(a) red, DESCENDED; (b) red, DESCENDED** — **the two cases are now separated and each has its own run** *(REPAIR 2026-09-17, Codex round 6 finding 5)*. *The withdrawn label, quoted: “(a)/(b) red, DESCENDED FROM STRICT RUNS”* — every run it cited leaks **`skD` only**, which is case **(a)**; none of them was a run of **(b)**. **(a):** S-STANDING's Q2, Q4 and abl6 models are **strict, DNS-compromised** (`ss_q2_companionA_identity_declared.out:808`, `:986`, `:630`; `ss_q4…out:576`, `:849`, `:1123`; `abl6_no_tlr_signature.out:616`, `:788`, `:960`), and all three are reproduced on the **strict** pair-judge join (`cap16a…out`, `cap16b…out`, `cap16c…out`; see C-N1's descent table). **(b):** the **repository-compromised** variants of those three joins, made for this repair — one line changed, `out(c, skR)` for `out(c, skD)` — red the same correspondences: `cap16a_ss_q1_pairjudge_cc11_declared_repo.out:766`, `:1012`, `:1696`, `:1942`, `:2188` (scope conjunct green `:1026`, honest standing `:2581`, agreement witness `:1450`); `cap16b_…_unsigned_repo.out:762`, `:1002`, `:1677`, `:1917`, `:2157` (scope `:1016`, honest standing `:2549`, agreement `:1437`); `cap16c_…_terminal_repo.out:810`, `:1136`, `:1866`, `:2190`, `:2514` (scope `:1152`, honest standing `:2873`, agreement `:1542`, S2 and S4 unreachable `:3217`, `:3413`). **Polarities are identical to the DNS variants query for query**; `cap16a_repo` and `cap16c_repo` land at the **same line numbers**, and `cap16b_repo` is offset **+1** from its third `RESULT` on, so its own numbers are cited above. **(d): red predicted** — in (d) C-Q6's standing conjunct is asserted only in its **honest-key** forms (§3, §(5)), which are what this companion must red, and no degraded S-STANDING companion run exists. **No green control arises in any case**: the mutation reads the attempt label from the bundle and needs **no adversary key**. **(c)** is C-C1's run and this companion is not stated for it. *(REPAIR 2026-09-17, Codex round 5 finding 2)* **STRICT OUTCOME IN THREE LISTS** *(REPAIR 2026-09-17, Codex round 8 finding 2)*. **(a) descended red:** C-Q6's standing conjunct, unrestricted and honest-key alike, on the **strict** pair-judge join (`cap16a_ss_q1_pairjudge_cc11_declared.out:766`, `:1012`, `:1696`, `:1942`, `:2188`) and family-locally (`ss_q2_companionA_identity_declared.out:630`, `:808`, `:986`). **(a) descended green:** C-Q6's **entitled-key conjunct** `StandingUnentitled` (`cap16a…:2195`) and **conjunct 3** — the registered pair judge `ScopeMisreported` unreachable (`:1026`) and the isolation observer **`ScopeIdentityOnly`** unreachable with it (`:1033`) *(NAME REGISTERED 2026-09-17, skeptic read S-11. The withdrawn name, quoted: “`ScopeIdentityWrong` (`:1033`)”. `ScopeIdentityWrong` is the **scratch copy's** name and is declared in **no** capstone registration, so this cell descended a capstone green on a query the capstone did not have; §(1) now declares the observer as **`ScopeIdentityOnly`**, and it is cited here by that name. The `.out` line and its polarity are unchanged, and the observer is an **observer** — it is not a discharge and is not timeboxed)* — with the substitution excluded (`:1019`). **Witnesses descended reachable:** `HonestStandingEstablished` (`:2581`) and `HonestWrappedStandingAgreed` (`:1450`). **(a) predicted green:** C-Q4's `Rescoped` and **link 6b** — `cap16a` declares neither. **(b): the same three lists, DESCENDED on the `_repo` variants** — red at `cap16a_ss_q1_pairjudge_cc11_declared_repo.out:766`, `:1012`, `:1696`, `:1942`, `:2188`; green at `:2195`, `:1026`, `:1033`, `:1019`; witnesses reachable at `:2581`, `:1450` — with `Rescoped` and link 6b still **predicted**. **(d): every entry predicted**, C-Q6's standing conjunct being asserted there only in its honest-key forms. **No green control in any case.** |
| **C-C12** | S-STANDING Q3 transcribed: the standing path checks the TLR key against the artifact's presented key but not against the evidenced tuple's `kfpr` | **C-Q6's entitled-key conjunct** (`StandingUnentitled` reachable). *Set-completeness note — skeptic 2026-09-15, **CORRECTED 2026-09-16 (Codex finding 4)**: the family-local run also reds S-STANDING Q1(i), the **unrestricted** `Established ⟹ Designated` (`ss_q3_companionB_entitled_via_envelope.out:628`, `LEDGER.md:524`). The draft disposed of that by saying C-Q6's standing conjunct **is not written** in the unrestricted form. **That is no longer true**: C-Q6 §(5) registers the standing conjunct in **both** an unrestricted strict form and honest-key forms. The reconciliation is C-Q6 §(6): the **unrestricted** strict form is **registered red under C-C12 too**, as a **consequence** of the entitled-key unbinding and **not a second severing of D12**; the **honest-key** forms are what must stay green, and they do family-locally at `:642`, `:656`. The set is still not exhaustive of the `.out`. **REPAIR 2026-09-17, Codex round 2 finding 1: this row was RIGHT and C-Q6 §(6) was WRONG; §(6) is corrected in place and the two now agree.** Re-run unchanged as the baseline of the round-2 dispositions, the committed source gives exactly what this row says: honest-key forms **green** (`cap5a_ss_q3_companionB_asis.out:642`, `:656`), unrestricted strict form **red** (`:628`) as a consequence, `StandingUnentitled` **reachable** (`:860`), `HonestStandingEstablished` reachable (`:1157`); it is **C-C11** that reds the honest-key forms (`ss_q2_companionA_identity_declared.out:808`, `:986`), which is D12's severing. **And the consuming event is now reachable in this companion by construction**: under the repaired contract `StandingUnentitledWrapped` observes the standing path's own report and does not depend on envelope success, where under the withdrawn (E1)/(E5) it would have been unreachable here too (`cap5b_ss_q3_e1_projection.out:476`).* | C-Q6's standing conjunct under honest keys; **C-Q6's conjunct 3, scope agreement** *(added 2026-09-17, REPAIR, Codex round 3 finding 2: C-C12 mutates the **standing** path's entitled-key comparison and changes neither path's attribution report, so the judge still pairs in agreement; **predicted**, no model declaring C-Q6)*; C-Q4; link 6b | `HonestStandingEstablished`, **and `HonestWrappedStandingAgreed`** *(added 2026-09-17 with conjunct 3)* | D13 | `ss_q3_companionB_entitled_via_envelope.out:860`, `:642`, `:656`, `:1157` | **(a) red, DESCENDED; (b) red, PREDICTED** *(REPAIR 2026-09-17, Codex round 6 finding 5)*. *The withdrawn label, quoted: “(a)/(b) red, DESCENDED FROM A STRICT RUN”* — the run it cites leaks **`skD` only**, which is case **(a)**. **(a):** `ss_q3_companionB_entitled_via_envelope` is **strict, DNS-compromised** (`…out:860`, `:642`, `:656`, `:1157`; re-run as `cap5a…out:860`), reproduced on the strict pair-judge join at `cap15d_ss_q1_pairjudge_cc12.out:1762` with the agreement witness reachable (`:1204`) and conjunct 3 green (`:813`). **(b):** **PREDICTED**, basis **channel symmetry** — and stated as predicted **although the repair that descended C-C11's (b) was available**, because the `_repo` variants made for finding 5 are of `cap14d` and `cap16a/b/c`, and **no `_repo` variant of `cap15d`, which is C-C12's shape, was made or exists**. Channel symmetry is a basis for prediction and **never a second recorded run**; if the builder wants (b) descended for C-C12 it is one file and one line away, and that is an observation for the run rather than a claim here. **(d): red predicted** — conjunct 2 is asserted in (d) (§3, §(5)) and no degraded run of this companion exists. **No green control arises**: the mutation removes a **verifier check** and needs no adversary key. **(c)** is C-C1's run and this companion is not stated for it. *(REPAIR 2026-09-17, Codex round 5 finding 2)* **STRICT OUTCOME IN THREE LISTS** *(REPAIR 2026-09-17, Codex round 8 finding 2)*. **(a) descended red:** C-Q6's **entitled-key conjunct** `StandingUnentitled` (`cap15d_ss_q1_pairjudge_cc12.out:1762`; family-locally `ss_q3_companionB_entitled_via_envelope.out:860`) and, as the **registered consequence** §(6) records and not as a second severing, the **unrestricted** standing forms (`cap15d:782`, `:1466`; family-locally `:628`). **(a) descended green:** C-Q6's standing conjunct in its **honest-key** forms (`cap15d:797`, `:1478`, `:1490`; family-locally `:642`, `:656`) and **conjunct 3** — the registered pair judge `ScopeMisreported` unreachable (`:813`) and the isolation observer **`ScopeIdentityOnly`** unreachable with it (`:821`, the copy's `ScopeIdentityWrong`) *(names registered 2026-09-17, skeptic read S-11: the halves are cited by the names §(1) declares, the scratch names being declared in no capstone registration; polarities and `.out` lines unchanged, and an observer is never a discharge)* — with the substitution excluded (`:805`). **Witnesses descended reachable:** `HonestWrappedStandingAgreed` (`:1204`) and `HonestStandingEstablished` (`:2113`). **(a) predicted green:** C-Q4 and **link 6b** — `cap15d` declares neither. **(b): the same three lists, every entry PREDICTED** — basis channel symmetry, and **no `_repo` variant of `cap15d` exists**, as this cell already records. **(d): predicted. No green control in any case.** |

**GAP, recorded not repaired — skeptic 2026-09-15.** The same argument
that produced C-C11 and C-C12 reaches **three further companions this
file leaves unnumbered and without a three-set specification**: D8's
(S-P7 Q3 + ablation a10, consumer **link 6a**), D9's (first-link Q2,
consumer **C-Q2**) and D11's (S-P7 Q6a / Q6b / Q5c, consumer **link
6b**). `LEDGER.md:1505-1520` lists all five together as *"to be
transcribed rather than rebuilt"*; §5's matrix names all five in its
"severing companion" column; only D12's and D13's are numbered and
specified here. Under A3.3 each of the three owes a companion that fails
**the consuming query**, and the consuming queries (C-Q2, link 6a, link
6b) exist in no model, so their sets cannot be re-specified from a
family-local `.out` the way C-C1–C-C10's are. Writing them would mean
inventing sets, which a skeptic pass may not do and which
`:1474-1476` reserves for the drafting step. **Flagged for the
non-author pass owed before the author's commit**, alongside the
C-C11/C-C12 numbering.

**GAP CLOSED — 2026-09-15, after the skeptic read** (§9; the skeptic log
below is untouched and still reads as written). The three are now
numbered and specified in the same three-set form as **C-C13** (D8,
consumer **link 6a**), **C-C14** (D9, consumer **C-Q2**) and **C-C15**
(D11, consumer **link 6b**, and C-Q6's scope conjunct conditionally).
Their sets are stated **in the capstone's query names**, as `:1474-1476`
requires of this file, with the family-local descent cited by `.out`
line and the capstone-only members — `ChainBroken`, C-Q2, C-Q6, C-Q8,
C-Q9 and the `HonestChain` witnesses — marked as **not descended**,
because no family model declares them.

**The count.** **EIGHTEEN companions are registered in this file**
*(AMENDMENT 2026-09-18, the author's ruling on §8 item 1, which added
**C-C18**, §9(5). The withdrawn words, quoted: “**SEVENTEEN companions
are registered in this file**”; every “SEVENTEEN” outside the dated
repair sections and the skeptic logs is superseded by this line and by
§9(5).)* *(REPAIR 2026-09-17, Codex round 5 finding 1, which added **C-C17**.
The withdrawn sentence, quoted: “**Sixteen companions are registered in
this file** *(fifteen until 2026-09-16, when Codex finding 1 added
**C-C16**; every earlier “fifteen” in this file outside the skeptic log
is superseded by this line and by §9(3))*”. Every earlier “sixteen” and
“fifteen” in this file **outside the skeptic log and outside the dated
repair sections** is superseded by this line and by §9(4); the dated
repair sections record the count **as it stood at each round** and are
not rewritten)*:
**C-C1–C-C10**, the ledger's own numbered companions
(`LEDGER.md:1494-1503`), and **C-C11–C-C15**, this file's numbering of
the five companions `:1505-1520` requires *"transcribed rather than
rebuilt"* and leaves unnumbered — D8's (`:1509`), D9's (`:1509-1510`),
D11's (`:1514-1515`), D12's and D13's (`:1515-1516`); **and C-C16**,
registered 2026-09-16 under Codex finding 1 as D7's **common-content**
severing companion, which no ledger line names because the ledger
assigned D7's whole discharge to links 2a/2b (§9(3)); **and C-C17**,
registered 2026-09-17 under Codex round 5 finding 1 as D7's
**membership** severing companion and **link 2a's**, which no ledger line
names for the same reason — the ledger assigned D7's whole discharge to
links 2a/2b and registered a companion for neither producer but
`Stripped` (§9(4)); **and C-C18**, registered 2026-09-18 under the
author's ruling on the `REFUSAL` fork as the **D-6 tag-severing**
companion, which no ledger line names because the ledger recorded
`REFUSAL` as unexercised (§9(5)). *Twelve was the
count before the 2026-09-15 addition; every earlier "twelve", including
the skeptic log's, is superseded by this line and by §9.* **No companion
carries a timebox**: §3's timebox table is over registered **queries**
only, and a companion runs inside the box of the query it is predicted
to red, so the 1155-minute per-case total and the 26 entries are
unchanged by these three additions, by C-C16, **by C-C17** *(REPAIR
2026-09-17, Codex round 5 finding 1)*, and by C-C8's two isolation
configurations. **C-C17 runs inside link 2a's 45-minute box** (§3) and
**C-C16 runs inside link 5's 60-minute box**
(§3), as C-C9 runs inside link 2b's; **C-C18 runs inside C-Q10's
30-minute box** (§3), the box the 2026-09-18 amendment added for the
query and not for the companion; **the timebox table is unchanged
by every repair of 2026-09-16**, which added no query and no entry —
C-Q6's composition join writes out an entry the table already counted,
and link 5's content conjunct was already inside link 5's box.

---

# 5. The discharge matrix as predictions

**Nothing below is discharged.** The last column states what the run
would establish if the predictions hold, not what is established. Cells
from `LEDGER.md:684-705` and `:759-762`. **D1–D11 are §2(a)'s
cross-model matrix (eleven rows, the count); D12 and D13 are §2(c)'s
standing-verdict rows, outside the matrix and outside its count**
(`:743-746`, `:786`) — *stated here because the single table below
would otherwise read as a thirteen-row matrix (skeptic 2026-09-15).*

| # | Producer query | Consumer query | Severing companion | Expected red | Today | If predictions hold |
|---|---|---|---|---|---|---|
| **D1** | S-P3 Q2 `Reattributed`, transcribed | **C-Q3** | **C-C2** | C-Q3, and link 5's frame-to-key half | firm; shown in scratch | **shown** |
| **D2** | S-P3 Q2 `Reattributed`, transcribed | **C-Q4** `Rescoped` | **C-C4** | C-Q4 `Rescoped` (**four** further reds — C-C4's set (1); *corrected from "two", skeptic 2026-09-15*) | firm; shown in scratch | **shown** |
| **D3** | S-P3 Q1(ii) chain correspondence | `Accept ⟹ IssuerSigned` | **C-C1** | `Accept ⟹ IssuerSigned` | firm; shown in scratch | **shown** |
| **D4** | link 1b: S-P3 Q1(ii); link 1a: **structural, none claimed** | **C-Q1 links 1a and 1b** | **C-C1** (1b) and **C-C10** (1a) | link 1b correspondence `is false`; link 1a `ChainBroken` reachable | firm; NOT YET SHOWN | **shown**, both conjuncts |
| **D5** | **C-Q7**, to be registered | **C-Q4** `InnerSigTransplanted` | **C-C5** (and **C-C6** for C-Q7 itself) | `InnerSigTransplanted` | `prov(P)` | **shown**; `prov(P)` retired if C-Q7 is green |
| **D6** | **C-Q8**, to be registered, structural | **C-Q1 link 4** | **C-C7**, both configurations | link 4 `ChainBroken` reachable; C-Q8 red | `prov(P)` | **shown**; `prov(P)` retired if C-Q8 is green |
| **D7** | S-P2 Q2 `Stripped` / `SignerForged` + Q6 `Spliced` | **C-Q1 links 2a and 2b**, **and link 5's common-content conjunct** for the `Spliced` half *(added 2026-09-16, Codex finding 1)* | **THREE companions, one per producer** *(REPAIR 2026-09-17, Codex round 5 finding 1. The withdrawn cell, quoted: “**C-C9** (set/completeness half) and **C-C16** (common-content half)” — it left the `SignerForged` producer, **membership**, with no severing companion at all, both named companions **retaining** link 2a and `SignerForged`.)*: **C-C9** for `Stripped`, the **set/completeness** half; **C-C16** for `Spliced`, the **common-content** half; and **C-C17** for `SignerForged`, the **membership** half (§9(4)) | C-C9: link 2b's slot-B conjunct `is false`, and `Stripped`. C-C16: **link 5's content conjunct** `ChainBroken(lyr, LINK_5)` reachable, and **`Spliced`** `is false`. **C-C17** *(added 2026-09-17, Codex round 5 finding 1)*: **link 2a** `ChainBroken(lyr, LINK_2A)` reachable — its shape descended by the slot-to-key judge, `cap13b_sp2_membership_unbound.out:1972` `is false` against `cap13a_sp2_membership_base.out:1206` `is true` — and **`SignerForged`** `is false` (`cap13b…:730`), with **`PossessionTransplanted` reachable** (`:1657`) as a **recorded consequence** | firm; NOT YET SHOWN | **shown**, all three producers |
| **D8** | S-P7 Q2/Q1 `TypeConfused` | **C-Q1 link 6a** | **C-C13** (S-P7 Q3 + ablation a10, transcribed; numbered and specified §9) | link 6a `ChainBroken` reachable | firm; NOT YET SHOWN | **shown** |
| **D9** | first-link Q4 `TwoWorldsBroken`, both variants | **C-Q2** | **C-C14** (first-link Q2, transcribed; numbered and specified §9) | C-Q2's boundary judge red | firm; NOT YET SHOWN | **shown** |
| **D10** | **C-Q9**, to be registered | **C-Q5** `SetAltered` | **C-C3** (and **C-C8** for C-Q9 itself) | `SetAltered` | `prov(P)` | **shown**; `prov(P)` retired if C-Q9 is green |
| **D11** | S-P7 Q2/Q5 `Rescoped` / `RescopedD1` / `RescopedD2` | **C-Q1 link 6b** (unconditional), and C-Q6 — *the C-Q6 half's consumption is frozen **only** with C-Q6's composition-join contract (§3, C-Q6 (1)–(6)), registered 2026-09-16 under Codex finding 4 **and revised 2026-09-17 under Codex round 2 finding 1** — `aid` minted **at intake**, (E1) restated as **same presentation**, (E4) a structural parse, (E5) **withdrawn** from the emission contract into the correct verifier's checks, §(6) corrected; before the contract that half was not builder-ready, and before the revision it was not severable* — **and the consumer of this half is C-Q6's CONJUNCT 3, scope agreement** *(REPAIR 2026-09-17, Codex round 3 finding 2)*: after the round-2 revision made the standing path independent of envelope success, conjuncts 1 and 2 observe **no** envelope attribution, so a C-C15 scope mutation could not red C-Q6 at all and this half had no falsifiable consumer (`cap10_ss_q3_scope_report_only.out:779` reachable, with `:798`, `:811`, `:856`, `:1205` green/reachable). Conjunct 3 — the `ScopeJudge`-form judge over the standing path's `(aid, lyr, kX, id)` report and the envelope path's `(aid, lyr, kA, idA)` attribution report, firing `ScopeMisreported` on **`(kA, idA) ≠ (kX, id)`** *(the **pair**, key and identity: REPAIR 2026-09-17, Codex round 4 finding 1; the withdrawn wording of this cell, quoted: “the standing path's `(aid, lyr, kX)` report … firing `ScopeMisreported` on `kA ≠ kX`”, which compared the key alone and so did not consume the identity half of the scope relation D11 names, `s-p7/PREDICTIONS.md:226-237`)* — is an **ADDITION beyond `LEDGER.md:1294`**, marked as such in §3, and restores the consumption **without** re-sequencing the paths | **C-C15** (S-P7 Q6b and Q5c, transcribed, two severing configurations, **and Q6a transcribed as configuration (iii), the isolation run for conjunct 3's identity half** *(REPAIR 2026-09-17, Codex round 4 finding 1; the withdrawn wording, quoted: “with Q6a as the isolation contrast”, which named it and specified no sets)*; numbered and specified §9) | link 6b `ChainBroken` reachable | firm; NOT YET SHOWN | **shown** on the C-Q1 half; the C-Q6 half too if C-Q6 terminates |
| **D12** | S-STANDING Q1(i)/(ii) `Established ⟹ Designated` | **C-Q6**, standing conjunct — *frozen only with C-Q6's composition-join contract, §3 C-Q6 (1)–(6) **as revised 2026-09-17 (Codex round 2 finding 1)**; its consumption is of the **unrestricted strict** and **honest-key** forms of §(5), not of an unspecified `EstablishedWrapped ⟹ Designated`, and §(6) now states correctly that **C-C11 reds the honest-key forms** (`ss_q2_companionA_identity_declared.out:808`, `:986`) — which is this row's severing* | **C-C11** | C-Q6's standing conjunct `is false` | §2(c) row; NOT YET SHOWN | **shown** |
| **D13** | S-STANDING Q1(iii) `StandingUnentitled` | **C-Q6**, entitled-key conjunct — *frozen only with C-Q6's composition-join contract, §3 C-Q6 (1)–(6) **as revised 2026-09-17 (Codex round 2 finding 1)**; the consuming event is `StandingUnentitledWrapped(kX, t)` of §(5), which observes the **standing path's own report** under the **intake** `aid` with the (E4) wrapped flag and fires on `fp(kX) ≠ kfpr` **whether or not the envelope path accepted** — the withdrawn “bound to a wrapped acceptance by (E1)” made this row's test unavailable, `cap5b_ss_q3_e1_projection.out:476` against `cap5a_ss_q3_companionB_asis.out:860`* | **C-C12** | `StandingUnentitled` reachable | §2(c) row; NOT YET SHOWN | **shown** |

If every prediction holds, eleven matrix rows and two §2(c) rows are
shown and the three `prov(P)` tags are retired by their producers'
registration. If any fails, it is classified by the three named outcomes
and recorded in `RESULTS.md`; it is never repaired by editing this file.
*(AMENDMENT 2026-09-18: C-Q10 and C-C18 discharge no matrix row and no
§2(c) row; they exercise the composed D-6 tag property of §2 rule 6,
which the ledger lists among what the capstone is for and not in the
matrix. If C-Q10 fails, or C-C18 does not red it, the result is
classified and recorded exactly as a row's is.)*

---

# 6. The Layer 2 register, carried (`LEDGER.md:848-915`)

**None of these is discharged by anything in this suite, and no capstone
query may mark either table checked.**

**6(a) Permanent external assumptions** (`:872-885`): **L2-a** signature
unforgeability (Dolev-Yao idealization, DSKS granted but bounded by D-4);
**L2-b** `fp` collision resistance and injectivity; **L2-c** `h`
idealization and concrete digest collision resistance; **L2-e** the
verification profile, P3's `[assumption]` half and H1a evidence; **L2-f**
deterministic signatures; **L2-g** implementation fidelity, including
key-use discipline for endpoints the suite does not model; **L2-h**
operational independence of authority channels, A1.3's "never all" as an
**n = 2 finite enumeration, not a quantified result**; **L2-k**
historical trust-anchor correctness; **L2-m** chain availability;
**L2-l** cross-protocol domain separation, a standing caution on every
single-removal "inert" label.

**6(b) Internal proof obligations carried as assumptions** (`:887-900`).
Exposed and unclaimed **today**, never a matrix row; each names the exit
item that discharges it, and when that item lands the entry **cites the
proof instead of assuming the fact**. *"Forever" does not apply to this
table.*

| Id | Obligation | Discharged by |
|---|---|---|
| **L2-d** | Canonical encoding and framing injectivity; frame layout; set encoding; the core's byte composition; the canonical-encoding half of L2-b | **`formal/BAND0-EXIT.md` E3**, the P8 framing proof, its golden vectors, non-author review, the author's read. Not begun |
| **L2-i** | P8 type-tag bytes; that the enumerated signed-object set is these eight and no others | **E3** |
| **L2-j** | Opacity of any concrete embedding; canonicalization semantics; what changes between canonicalization versions | **E3** |
| **L2-n** | The §A3.7.2 extended atomic-entry invariant, carried by L-21 | **`formal/BAND0-EXIT.md` E6**: P5c gains the invariant with two companions, both red; reading aids; review; author read. Not begun |

---

# 7. What the capstone does not claim

- **Named scoping, disposed by amendment discipline and never silently**
  (`:909-915`): **n = 2 authority channels**, a finite enumeration of
  A1.3's "never all", not a quantified result (L2-h); **two-attempt
  lineages** (L-16, `:510`); **wrapper depth ≤ 2** (L-13, `:911`);
  **required sets of at most two signers** — the size bound `|set| ≤ 2`
  is **L-09**'s named scoping (`:911`), while canonical ordering,
  uniqueness and bounds beyond n = 2 are **L-08**'s P8 obligation,
  LAYER-2(b) and unclaimed until E3 (`:408-419`). *[Corrected — skeptic
  2026-09-15: the draft assigned the size bound to L-08; `:911` assigns
  it to L-09.]*
- **Term equality for byte equality (P8).** The model's `framed(...)` is
  not the P8 frame and the capstone claims nothing about frame layout.
- **`h` and `fp` idealization.** Both are free constructors, injective by
  construction, with no collisions and no preimages; any query whose
  truth depends on either being hard to invert or collide is proving a
  symbolic fact about a perfect function
  (`lib/tessera_theory.pvl:118-142`).
- **Cross-formalism joins, never symbolically discharged** (ENUM §4,
  `ENUMERATION.md:135-147`; `LEDGER.md:919-937`): **L-05**, `Accept` /
  `AcceptS` ↔ P4's verdict partition, producer
  `formal/tla/P4_VerifierStates.tla`; **L-19**, TLR anchor temporal
  validity, producers `P5c_IssuanceProtocol.tla` and the bridge;
  **L-21**, the refusal latch to terminal disposition, producer
  incomplete until E6. Marking any of them symbolically discharged is the
  checkmark-relay red bar.
- **The integrated adversarial lifecycle model** (A3.9, H1a) is not this
  model and is not Band 0.
- **Nothing about the refusal record** *(AMENDMENT 2026-09-18)*. The
  `REFUSAL`-tagged signer of §1.1 is a foreign-tag source whose body is
  opaque to every check while the tag check stands (under C-C18 it is
  read as a lineage record's, never as a refusal record's); C-Q10 and
  C-C18 show only that the `TLR` tag check separates signing domains
  under composition. The record's
  content and decomposition (A3 §A3.7.2), the extended atomic-entry
  invariant (**L2-n**) and **E6** are neither modelled nor claimed, and
  `REFUSAL` is exercised as a signing domain and unexercised as a
  record.
- **Nothing about the adjudicator's decision.** Per A4.6 the verifier's
  job in degraded mode is to hand the adjudicator the evidence of what
  could and could not be excluded, marked degraded; a correspondence that
  holds strict and fails degraded is a registered **cost**, not a defect.
- **No absorption.** No query here may absorb an L2-a…L2-n item into a
  checked cell, treat L-14's by-construction encoding as a producer, or
  read L-01 as discharging S-P1's authorship (`:1522-1529`).

---

# 8. Freeze, sequencing, and what is routed

## Freeze statement

**This file is frozen by the author's commit containing it**, and nothing
in the capstone may be written or run before that commit (ENUM §5;
`LEDGER.md:1261-1262`). After the freeze: (1) **the model is built by a
builder who may not edit this file**, and every prediction above is read
as written; (2) **results go to `formal/suite/capstone/RESULTS.md`**,
never here; (3) **recuts for encoding are logged** in a "Recuts
(encoding, not property)" section of `RESULTS.md` on the S-P3 pattern
(`s-p3/RESULTS.md:38-73`), while a recut of a **property**, of a query's
shape, or of a registered prediction is an **amendment**, appended and
dated, never a rewrite; (4) **a non-author cross-family falsification
review** then runs against the built model and its results, by a reviewer
from a different model family; (5) **the author's read** is of the
**plain-language statement** of claim, adversary and boundary, per A4
§A4.4 (`docs/phase-0-prereg-amendment-4.md:125-143`): the written proof
is the collection of each checked model's plain-language statement, and
tool fluency is neither asked of the author nor a gate. **Owed before the
author's commit**, per the round-4 review's own termination note: a full
non-author pass and a full skeptic read of **this file**, and the routed
item below answered *(answered by the author 2026-09-18, §8 item 1; the
pass and the read owed on the amended version are logged in the review
log)*.

## Routed to the author

**1. ROUTED: the `REFUSAL` tag, and whether the capstone exercises it.**
`LEDGER.md:1276` instructs the capstone to record `STMT_DIRECT` and
`REFUSAL` as **declared-and-unexercised**, and `:1555-1559` forbids any
claim that the `REFUSAL` domain is checked, no committed model signing
one. But `:1270-1273` also requires the D-6 tags to be *"present and
load-bearing under composition, which is precisely what the capstone is
for"*, and the library's D-6 note records the only demonstration anyone
has of that: an honest `REFUSAL`-tagged signer over a TLR-shaped body,
after which removing the tag check turns the strict standing
correspondence red (`lib/tessera_theory.pvl:66-76`). The two instructions
cannot both be followed. **(i)** Add an honest
`sign((REFUSAL, body), skI)` signer, which exercises the domain, makes
the tag check load-bearing and permits a tag-removal companion; cost,
`REFUSAL` is no longer declared-and-unexercised and the §A3.7.2 / E6
obligation that owns the refusal record (L2-n) acquires a symbolic
fixture ahead of the artifact meant to settle it. **(ii)** Leave
`REFUSAL` declared and unexercised as `:1276` says; cost, the composed
tag property, the one thing the ledger says the capstone exists to
exercise, stays inert and no companion can be registered for it. A
builder cannot make this choice. **No prediction above depends on the
answer**: no `REFUSAL` query is registered either way, and option (i)
would add one query and one companion by amendment before the freeze.

**RULED 2026-09-18 — the author: option (i), scoped.** *The author's
words, in session, verbatim. After the owner instance recommended (i)
with the scoping below and explained why (ii) had been presented as its
equal:* **“Good - what I couldn't understand is why (ii) seemed a
plausible choice.”** *Asked to rule in his own words:* **“Yes.  (i)
reasonably scoped is what I would vote for - you can disagree now, if
you think this is the wrong decision.”** The owner instance agreed.
**The scoping, stated by the owner instance and accepted by the
author:** the honest `REFUSAL`-tagged signer is a **foreign-tag source
and nothing else** — its body is opaque to every check while the tag
check stands, and chosen TLR-shaped as the worst case for separation
(under C-C18 it is read as a TLR's, never as a record's); it models nothing about
the refusal record (A3 §A3.7.2), the extended atomic-entry invariant
(L2-n) or E6, which stay exactly where they were; `REFUSAL` is thereby
**exercised as a signing domain and unexercised as a record**. **On
that scoping the cost named for (i) above is not incurred**: E6 acquires
no fixture, because the fixture claims nothing about the record. **Why
(ii) was never the obedient reading:** `:1276`'s purpose was that
`REFUSAL` not be silently omitted, and `:1555-1559` forbids claiming
the **record's** domain checked; a tag-separation companion claims
neither. Under (ii) Band 0 would exit with D-6's load-bearing status
resting on one unregistered scratch run, the single-removal “inert”
label L2-l warns against. **Entered by this amendment** (and listed in
the dated section at the end of this file): §1.1's foreign-tag row;
§1.2's step 7 naming the check; **C-Q10** (§3, 30-min box — **27**
entries, **1185 min** per case); **C-C18** (§9(5)); §5's and §7's
notes; the count (**EIGHTEEN**); dated ruling notes on the ledger's
`REFUSAL` row (`:385`) and `:1276`; the scratch batch `cap27a`–`cap27f`
(README batch eighteen). **No item remains routed to the author.** The
four contestable choices below stand and remain contestable at the
commit; no other query, probability, residual or timebox moved.

**2. Clerk disposition, offered for veto, not routed.** ENUM §3
(`ENUMERATION.md:112`) and `LEDGER.md:11` name the model
`formal/suite/capstone.pv`; this file names
`formal/suite/capstone/proverif/capstone.pv`, following the layout every
family uses and keeping `PREDICTIONS.md`, `RESULTS.md` and the model in
one directory. The divergence is clerical, is recorded rather than
silently taken, and is the author's to veto.

**ACCEPTED 2026-09-18 — the author, with one clarification.** *The
author's words, in session, verbatim:* **“Is the path veto the clerical
one?  If so, then I accept the clerical modification: the file contents
matters, not the path.  The clarification would just to be ensure we
all know what the "file contents" are.”** The path stands as this file
names it. **The clerk reading of the clarification, the owner
instance's:** the model is identified by its **contents**, not its
path — the builder records, at the first run, the git blob hash of
`capstone.pv` as committed in `RESULTS.md`'s header beside the path,
and every result cites that hash; a model at the registered path with
a different hash is a different model. That is what “we all know what
the file contents are” means here, and it is a recording duty on the
builder, not a change to any prediction.

*[WITHDRAWN 2026-09-16, Codex finding 6. The draft read: "**No other
fork was found. After four non-author rounds and three post-ruling
corrections, the ledger's contract determines every other choice this
file had to make.**" **The second sentence was premature and is
withdrawn.** The `REFUSAL` fork remains the one item routed to the
author, and finding 6 does not disturb it; but the ledger's contract
did **not** determine every other choice. **FOUR** consequential
choices were left to the builder by omission, and all four are **fixed
by this file** — they are choices taken here, not facts inherited
*(items 1 and 2 on 2026-09-16; **items 3 and 4 added by the REPAIR of
2026-09-17, Codex round 2 findings 3, 4 and 5**, the second round having
found two more. The 2026-09-16 wording is withdrawn in place and quoted:
“**Two** consequential choices were left to the builder by omission,
and **both** are **fixed by this file** as of this repair.” Items 3 and
4 are **clerk dispositions of the owner instance, contestable by the
author at the freeze commit without an amendment**; they are not author
rulings and are not routed)*:*

1. **The `EstablishedWrapped` event signature, its emission contract,
   and the representation mapping joining S-P7's extracted
   `(fbI, sgI)` to S-STANDING's `attemptCore(t, ppf, sg, decl)`**
   (Codex finding 4). `LEDGER.md:1294` fixes C-Q6's *formulation* and
   the rows it consumes and fixes **no** event arguments and **no**
   shared terms. The six arguments, the emission contract —
   **(E1)–(E4) as revised 2026-09-17 under Codex round 2 finding 1;
   the withdrawn wording of this item read “(E1)–(E5)”, and (E5)
   now sits among the correct verifier's checks, not in the contract**
   — the five term equalities, the unrestricted and honest-key forms
   in strict and degraded mode, and the `StandingUnentitledWrapped`
   event are **this file's choices**, registered in §3 under
   *"C-Q6's composition join, written out"*. A builder given the draft would have had to invent
   them, and a wrong invention would have let wrapper attribution for
   one artifact combine with standing evidence for another.
2. **C-Q5's fixture key assignment** (Codex finding 5).
   `LEDGER.md:1292` names *"S-P2's `MemberJudge` shape"* and does not
   carry S-P2's one-key/one-manifest restriction, which that judge
   needs to mean what C-Q5 claims. §1.1 now names the assignment —
   `skI` → `M2` slot A, `skB2` → `M2` slot B, `skI2` → `M1`, no key in
   two manifests — and §3's C-Q5 entry records that the alternative
   (a provenance correspondence in the judge's place) was considered
   and **not** taken, with the reason. Both are **this file's
   choices**.
3. **Same-key wrapping in the fixture** (Codex round 2 finding 3),
   **contestable**. `LEDGER.md:1392-1406` names a wrapper key and does
   **not** say whether an **issuer** key also signs an `OT_WRAPPER`
   frame, and the answer changes results: **with** it, C-C15(i)'s
   honest wrapped witness exists and **C-C7(ii)** loses C-Q7 and
   honest-key authorship from its retained set
   (`cap7b_sp1_q8_wrapper_signer_type_conditional.out:528`, `:1072`);
   **without** it, C-C7(ii)'s registered contrast survives and
   C-C15(i)'s wrapped witness is unreachable by fixture. §1.1's
   Wrapper row **takes same-key wrapping**, for fidelity to S-P7's I1
   (`s-p7/RESULTS.md:54`, `:79-84`), and §4's C-C7 row carries the
   consequence while §4's C-C6 row and C-C7(i) record what it does
   **not** disturb (`cap7c`, `cap7d`). **This file's choice.**
4. **The meaning of “adversary-enrolled issuer key”** (Codex round 2
   finding 4), **contestable**. §1.1's Adversary row added the key
   without saying how it is enrolled, and the literal alternative —
   genuine enrolment by **uncompromised** authorities — falsifies the
   registered strict baseline with **no verifier change at all**
   (`cap8b_sp1_q1_strict_adversary_enrolled.out:398` against
   `cap8a_sp1_q1_strict_base.out:201`). §1.1 now fixes the reading
   **per case**: compromised-channel enrolment only, never from an
   uncompromised authority process, inheriting S-P7's strict-mode
   sentence (`s-p7/PREDICTIONS.md:196-205`). **This file's reading.**

*The `REFUSAL` fork above is still the only item routed to the author,
and it is still unresolved here.]*

*(AMENDMENT 2026-09-18: the `REFUSAL` fork is **resolved** by the
author's ruling entered under item 1 above. No item is routed to the
author; the four contestable choices remain contestable at the freeze
commit without an amendment.)*

**THE FOUR CONTESTABLE CHOICES — CONFIRMED 2026-09-18 by the author.**
*The author's words, in session, verbatim, after reading
`READ-FREEZE-2026-09-17.md`:* **“I confirm all four choices.”** The
four are, as that note and this section list them: **same-key wrapping
in the fixture** (item 3 above; §1.1's Wrapper row); **“adversary-
enrolled” meaning compromised-channel enrolment only** (item 4; §1.1's
Adversary row); **`ev` as the pair in strict** (§1.3); **the report
contract under companions** (§1.3). Each stays marked as **this file's
choice**, now confirmed by the author rather than overruled; the
marking is kept so the record shows who chose and who confirmed.
Nothing else in this file was contestable, nothing is routed, and no
query, probability, residual or timebox moves. *(Entered by the owner
instance; a confirmation needs no amendment and no further pass, per
`READ-FREEZE-2026-09-17.md` §4.)*

## Review log

- **2026-09-15**. Basis: drafted by the AI collaborator (Claude Opus 5),
  directed by the owner instance, from `formal/suite/LEDGER.md` §6 under
  the author's outcome-5 ruling with §§1-5 read whole;
  `docs/phase-0-prereg-amendment-3.md` §§A3.2, A3.2.1, A3.3;
  `ENUMERATION.md` §§3, 4, 5; `s-p2/PREDICTIONS.md` and
  `s-standing/PREDICTIONS.md` for the house form; `lib/tessera_theory.pvl`;
  `s-p3/RESULTS.md` "Recuts (encoding, not property)";
  `docs/phase-0-prereg-amendment-4.md` §§A4.4, A4.6; and the round-4
  Codex review. **No capstone model exists; nothing was written or run;
  no scratch run was made for this file.** Every `.out` line cited is a
  family-local or ledger-scratch result already on the record, cited as
  the descent of a prediction and never as a capstone result.

- **Eighteen Codex non-author rounds and two full skeptic reads,
  2026-09-15 to 2026-09-18** *(REPAIR 2026-09-17, skeptic read S-9: this
  log carried the drafting entry alone, so a reader asking what review
  this file has been through found one bullet, although the dated
  repair sections below are each self-describing. One line per
  round, each pointing at its record; the dispositions at each record's
  head are **clerk dispositions of the owner instance**, never author
  rulings, and each round's repairs are in its own dated `## Repairs
  after…` section below.)*
  - **Round 1**, 2026-09-15/16, 6 accepted findings — `docs/reviews/2026-09-16-codex-review-capstone-predictions.md`.
  - **Round 2**, 2026-09-16, dispositioned 2026-09-17, 4 accepted — `docs/reviews/2026-09-16-codex-review-capstone-predictions-round2.md`.
  - **Round 3**, 2026-09-17, 4 accepted — `docs/reviews/2026-09-17-codex-review-capstone-predictions-round3.md`.
  - **Round 4**, 2026-09-17, 2 accepted — `docs/reviews/2026-09-17-codex-review-capstone-predictions-round4.md`.
  - **Round 5**, 2026-09-17, 2 accepted — `docs/reviews/2026-09-17-codex-review-capstone-predictions-round5.md`.
  - **Round 6**, 2026-09-17, 6 accepted — `docs/reviews/2026-09-17-codex-review-capstone-predictions-round6.md`.
  - **Round 7**, 2026-09-17, 2 accepted — `docs/reviews/2026-09-17-codex-review-capstone-predictions-round7.md`.
  - **Round 8**, 2026-09-17, 2 accepted — `docs/reviews/2026-09-17-codex-review-capstone-predictions-round8.md`.
  - **Round 9**, 2026-09-17, 3 accepted — `docs/reviews/2026-09-17-codex-review-capstone-predictions-round9.md`.
  - **Round 10**, 2026-09-17, 2 accepted — `docs/reviews/2026-09-17-codex-review-capstone-predictions-round10.md`.
  - **Round 11**, 2026-09-17, 1 accepted — `docs/reviews/2026-09-17-codex-review-capstone-predictions-round11.md`.
  - **Round 12**, 2026-09-17, **0 findings, ready to freeze subject to the author's items**; its one disposition is the `cap25` dated note in §9(1) — `docs/reviews/2026-09-17-codex-review-capstone-predictions-round12.md`.
  - **Full skeptic read**, 2026-09-17, after round twelve, S-1–S-13, **not ready for the author's freeze read**; seven repairs applied and logged below — `docs/reviews/2026-09-17-skeptic-read-capstone-predictions.md`.
  - **Round 13**, 2026-09-17, after the skeptic repairs, 3 accepted (one-sentence corrections of the skeptic repair) — `docs/reviews/2026-09-17-codex-review-capstone-predictions-round13.md`.
  - **Round 14**, 2026-09-17, after the round-13 corrections, **0 findings, ready to freeze subject to the author's items**; re-ran `cap25`/`cap26` — `docs/reviews/2026-09-17-codex-review-capstone-predictions-round14.md`. *(Rounds 13 and 14 entered 2026-09-18 by the owner instance: the round-13 repair left the log at twelve rounds, and no round adds its own line; clerical, nothing else moves.)*
  - **Round 15**, 2026-09-18, clerical confirmation of the 2026-09-18 edits against a byte-exact round-14 copy: lines 1–2008 identical, **0 findings in the registration, ready to freeze subject to the author's items** — `docs/reviews/2026-09-18-codex-review-capstone-predictions-round15.md`. *(Entered after the round, as every last line must be.)*
  - **Amendment 2026-09-18** — the author's ruling on the `REFUSAL` fork, option (i) scoped (§8 item 1): C-Q10 and C-C18 registered, batch eighteen `cap27a`–`cap27f`, entered by the owner instance in the dated section at the end of this file. **Owed on this version before the author's commit, per the freeze statement:** a full skeptic read and a full non-author pass (round 16) — both run in parallel the same evening, records below.
  - **Skeptic read of the amendment**, 2026-09-18, S-1–S-17, **not ready for one repairable reason** (the ledger note had shifted ~45 `LEDGER.md` citations; refolded), 4 repairs applied, 10 checked-correct — `docs/reviews/2026-09-18-skeptic-read-capstone-amendment.md`.
  - **Round 16**, 2026-09-18, on the amendment, 5 accepted (C-Q10's coverage stated per consumer, with the reviewer's counterexample reproduced as `cap27g`/`cap27h`; C-C18's set (2) case-qualified; “opaque” reworded; the ordinal; the live counts) — `docs/reviews/2026-09-18-codex-review-capstone-predictions-round16.md`.
  - **Round 17**, 2026-09-18, confirmation of the round-16 and skeptic repairs: 3 accepted (the citation sweep had renumbered eleven bare references that were ledger, model or output lines — reverted — and two genuine self-references landed short; the handoff's inline ranges; §7's “opaque” sentence), 5 confirmations — `docs/reviews/2026-09-18-codex-review-capstone-predictions-round17.md`.
  - **Round 18**, 2026-09-18, confirmation of the round-17 corrections: **0 findings, ready to freeze subject to the four contestable choices and the path veto** — `docs/reviews/2026-09-18-codex-review-capstone-predictions-round18.md`. *(Entered after the round, as every last line must be.)*
  - **The author's decisions, 2026-09-18**, entered under §8 after round 18: the four contestable choices **confirmed**, the path veto **accepted** with one clarification (the model is identified by its contents; the builder records the blob hash). Clerical; no round.

## Skeptic log (2026-09-15)

*A non-author skeptic read of this file against `LEDGER.md` §6
(`:1250-1559`), the three post-ruling corrections (`:2156-2281`), the
round-4 dispositions, A3 §§A3.2/A3.2.1/A3.3, ENUM §§3-5,
`lib/tessera_theory.pvl` and the house form. **Nothing was run and no
model was touched.** Every edit below is in this file only; none of them
changes a query, a probability, a companion's obligation or the routed
fork. Format: **item — what changed — why — what was checked.*

### Edits made

1. **Provenance, the ruling cite.** `:52-68` → `:55-71`. The ruling
   block runs `:55-71`; `:52-53` are the round-4 repair note and `:69-71`
   carry *"the commit is the author's"*, which this file relies on.
   Checked `LEDGER.md:50-72`.
2. **§2, encoding rule (6).** Bare `` `:387-398` `` re-pathed to
   `LEDGER.md:387-398`. It followed a `lib/tessera_theory.pvl` cite and
   so read as a library line; the library is 195 lines long. `:387-398`
   is the ledger's *"The composed property"* paragraph on cross-tag
   domain separation, which is what the rule asserts. Checked
   `lib/tessera_theory.pvl` length and `LEDGER.md:387-398`.
3. **§2 preamble and §8(3), the S-P3 recuts cite.** `s-p3/RESULTS.md:38-57`
   → `:38-73` (both places). Recut 1 is `:38-56`, recut 2 `:58-62`, recut
   3 `:64-73`; this file invokes all three (parallel report outputs,
   per-role judges, `HonestAccepted` over bare acceptance), and the
   shorter range reaches only the first. Checked `s-p3/RESULTS.md:34-76`.
4. **§1.1, case (d), the A4.6 cost.** `amendment-4.md:154-165` →
   `:156-171`. `:154` sits inside §A4.5 and `:165` truncates the quoted
   principle, which closes at `:171`. Checked
   `docs/phase-0-prereg-amendment-4.md:120-180`.
5. **§1.2, the SS.Q3 sequencing warrant.** `s-standing/PREDICTIONS.md:376-386`
   → `:385-392`. The shadowing statement this file rests the
   parallel-standing-path rule on is the SS.Q3 prediction bullet at
   `:385-392`; `:376-384` is the correspondence discussion. Checked
   `s-standing/PREDICTIONS.md:370-396`.
6. **§8, clerk disposition 2.** `LEDGER.md:14` → `:11`. `:11` is the
   line that names `formal/suite/capstone.pv`; `:14` is the
   family-file-precedence rule and names no model. The disposition
   itself is untouched and is still the author's to veto. Checked
   `LEDGER.md:11-16` and every `capstone.pv` occurrence in the ledger.
7. **§7, named scoping.** The `|set|` size bound was attributed to
   **L-08**; `LEDGER.md:911` assigns `|set| ≤ 2` to **L-09**, and L-08
   (`:408-419`) is the P8 canonical-encoding obligation — LAYER-2(b),
   unclaimed until E3 — which is what owns ordering, uniqueness and
   bounds beyond n = 2. Both are now named, with their own lines.
   Checked `LEDGER.md:408-420`, `:911`.
8. **§3 link 5 and the retained-query table.** Bare `` `.out:1013` ``
   resolved to `base_sp2.out:1013`, twice. A bare extension is not a
   citation, and the same basename convention is used elsewhere in the
   file for two different models. Verified the line reads
   `RESULT not event(Spliced(t_2,fa_2,fb_4)) is true.`
9. **§3, C-Q6's modes.** The clause *"S-STANDING's own unrestricted
   correspondence is registered red in degraded mode"* carried no
   source; it now cites L-18 (`:534`) and
   `ss_q1d_degraded_compromised.out:640`, and the mode assignment is
   **marked as this file's addition**, because `:1294` fixes C-Q6's
   formulation and its consumed rows and states no modes for it.
10. **§4 C-C4 set (1) and §5's D2 row.** *"Three by design"* listed five
    entries; it now reads **five in capstone names** — the ledger's
    *"three"* (`:1497`) is the family-local count, and links 6b and 5 are
    capstone queries no family model declares. D2's expected-red cell
    *"two further reds"* → **four**. The row's obligation (`Rescoped`,
    D2) is unchanged. Checked `LEDGER.md:1497`, `:696`,
    `s4_innerfp_mh.out:864`, `:1207`, `:1431`.
11. **§3, the timebox table.** The total row is now labelled **per
    compromise case**, with the four cases accounted for: the box is
    declared per run and each case gets the full box, so the ladder's
    declared ceiling is at most 4 × 1155 = 4620 min, less for the
    queries stated in fewer than four cases (named). Also recorded that
    **26** counts separately timeboxed *entries*, not ProVerif queries —
    C-Q3 is per-role, C-Q4 two judges, C-Q6 two conjuncts, C-Q5w two set
    sizes, link 2b three conjuncts — and that a timeout is a
    mechanism-viability failure disposed by §3's ablation order, never
    by raising the box. **The arithmetic itself was correct**
    (315 + 120 + 180 + 180 + 90 + 60 + 210 = 1155; 7 + 2 + 4 + 3 + 1 + 2 + 7 = 26)
    and is unchanged.
12. **§5, the discharge matrix.** Labelled **D1–D11 as §2(a)'s eleven
    matrix rows and D12/D13 as §2(c)'s**, outside the matrix and its
    count (`:743-746`, `:786`). One table of thirteen rows otherwise
    reads as a thirteen-row matrix, which is exactly the convention
    defect §2 was split to retire.
13. **§3, the C-Q1 header.** Made explicit which link predictions
    constitute each separately-frozen form — strict is the nine,
    degraded the same eight without 1b — since `:1386-1390` freezes the
    two forms separately and the ladder gives one prediction per link.
    Also **marked the per-link query split as this file's encoding
    addition**: `:1317` declares one `ChainBroken(lyr, link)` event
    carrying the failed link's name, which one query could cover.
    Justification recorded in place (recut 2; C-C9 and C-C10 need
    per-link resolution). No property changes.
14. **§4, C-C12.** Added the set-completeness note the ledger's own
    C-C6/C-C7/C-C10 rows carry: the family-local run also reds
    S-STANDING Q1(i), the **unrestricted** correspondence
    (`ss_q3…out:628`, `LEDGER.md:524`), which C-Q6's standing conjunct is
    not written in — the per-key forms stay `is true` at `:642`, `:656`.
    That red is **not** a severing of D12 and the set is not exhaustive
    of the `.out`.
15. **§1.1, four fixture rows.** Marked and sourced. `:1392-1406` lists
    no adversary-enrolled issuer key, no lineage and no standing path.
    The adversary key and the lineage are now flagged **ADDITION beyond
    §6** with their justification and source lines (`:1289`, `:1290`,
    `:1292`; `:1294`, `:510`, `:761`); the standing path is sourced to
    D11/D12/D13's transcribe columns (`:705`, `:761`, `:762`); the issuer
    keys' *"note 3"* gloss now carries its line (`ENUMERATION.md:244`,
    `:262-263`). No fixture element was added or removed.
16. **§4, after the C-C11/C-C12 table — GAP recorded, not repaired.**
    The same argument that numbered C-C11 and C-C12 reaches three more
    transcribed companions this file leaves unnumbered and without
    three-set specifications: D8's (S-P7 Q3 + a10 → link 6a), D9's
    (first-link Q2 → C-Q2) and D11's (S-P7 Q6a/Q6b/Q5c → link 6b), all
    five being listed together at `:1505-1520` and all five appearing in
    §5's companion column. Their consuming queries exist in no model, so
    their sets cannot be re-specified from a family-local `.out`;
    inventing them is the drafting step's, reserved at `:1474-1476`, not
    a skeptic's. Flagged for the non-author pass owed before the commit.
17. **§4, the mechanism-review rule** (*"model the simplest plausible
    alternative, not the strawman"*, `formal/spike/floor-structure/PROBE.md:46`).
    Applied to all twelve companions. Two were short: **C-C5**'s
    `s2_sig_removed.out:852` was cited without saying what it contrasts
    — it is now named as the nearest alternative that reds the same
    query by severing a *different* fact (`:1498`); **C-C8** has **no
    single-removal isolation run** anywhere on the record, unlike C-C2
    (`m1_framepin.out:399`), C-C3 (the C1/C3 configurations) and C-C4
    (`s3_innerfp.out`), so its two-removal minimality is recorded as
    **asserted, not shown** — an observation for the run, not a
    prediction this file may add. **C-C4**'s isolation contrast was
    cited but unexplained and is now stated (edit 10).

### Checked, correct as written — no change

18. **`LayerAccepted`'s contract (§1.3) against `:1315`.** Nine
    arguments, `pkey` in position six, order `aid, lyr, t, ev, slot, kX,
    ppf, sg, fb` — an exact match, including the fresh-name `aid` per
    correction (c) (`:2249-2273`), the accepted evidence term, the
    signature term, the presented framed bytes and the signer slot.
    **Two arguments the review brief named are in no LEDGER §6 signature
    and were NOT added**: an *attributed innermost identity* (that is
    link 6b's conjunct over the inner frame, `:1339`) and a *standing
    value* (that is C-Q6's conclusion, `:1294`). Adding either would put
    this file ahead of the contract it registers.
19. **`AuthorityEvidence`, `AcceptanceComplete`, `ChainBroken`,
    `HonestChain`** against `:1314`, `:1316`, `:1317`, `:1318` — all
    four match, including that `ChainBroken` is the subject of 1a, 2a,
    3, 4, 5, 6a, 6b **only** and that 1b and 2b are correspondences
    (`:2213-2247`).
20. **Link 2b** requires a record for every required slot under one
    `aid`, with the `signers0` conjunct and **both** `signers1(fpB)`
    conjuncts (`:1334`). **Link 6** is split 6a/6b with separate
    producers (`:1338`, `:1339`). **C-Q8** ranges over every accepted
    triple with no honest-signature filter, including failed
    verification (`:1290`, and correction (a) `:2165-2211`, which
    forbids the authorship gloss — this file states it cannot say who
    produced `sg`). **C-Q9** is over the **accepted manifest**
    (`:1291`). All as written.
21. **C-N1 is not an addition.** It is `LEDGER.md:1295`, a §6 query, and
    is correctly left unmarked. C-C11 and C-C12 **are** additions and
    are already marked, justified and sourced to `:1505-1520`.
22. **Every query, companion and matrix row against §6.** C-Q1 `:1285`,
    C-Q2 `:1286`, C-Q3 `:1287`, C-Q4 `:1288`, C-Q7 `:1289`, C-Q8
    `:1290`, C-Q9 `:1291`, C-Q5 `:1292`, C-Q5w `:1293`, C-Q6 `:1294`,
    C-N1 `:1295`; links `:1331`-`:1339`; strict/degraded `:1368`,
    `:1369`, `:1371`; companions C-C1–C-C10 `:1494`-`:1503`; retained
    queries `:1425-1447` (nine listed, seven here, `Rescoped` and
    `SetAltered` correctly not double-counted). Every cited line is the
    line it claims.
23. **Encoding rules (1)–(7)** against `s-p3/RESULTS.md:38-73` and
    `:1264-1278`: parallel report outputs, per-role judges, `-lib` with
    nothing redeclared, `framed` copied verbatim and NOT promoted, the
    D-1 split, the D-6 tags, `HonestAccepted` over bare acceptance. All
    seven match and all are stated as binding from the start.
24. **Every `.out` cited exists and is not a family run that was never
    made.** All 31 files in `formal/suite/ledger-tests-2026-09-14/`
    resolve, as do the committed family outputs; spot-checked
    `sp3_q1_strict_dns_compromised.out:424`, `base_sp1q1.out:201`,
    `base_sp2.out:1013`, `d5c_sp1_sigjudge.out:203`,
    `sp2_q5_c1_fponly_frame_mh.out:366`,
    `sp7_q2_degraded_compromised.out:527`, `sp1_q2_*.out:173` — every
    one reads as claimed. **No prediction rests on a run that does not
    exist**, and every probability carries a residual decomposition.
25. **The three named outcomes** are stated once (§3, *"registered once
    and binding on every query below"*), match ENUM §5 `:151-155`, and
    are referenced rather than restated in §5.
26. **§6's Layer 2 tables** against `:872-885` and `:887-900`: ten
    permanent entries (L2-a, b, c, e, f, g, h, k, m, l) and four
    internal obligations (L2-d, i, j → **E3**; L2-n → **E6**), with
    *"forever does not apply"* and *"no capstone query may mark either
    table checked"* both carried.
27. **§7's "does not claim"** covers all eight required topics: n = 2
    channels, two-attempt lineages, depth ≤ 2, term-vs-byte equality
    (P8), `h`/`fp` idealization, the three cross-formalism joins with
    their TLA+ producers, the A3.9 lifecycle model, and the
    adjudicator's decision — plus the no-absorption clause.
28. **§8's freeze statement** carries all of: frozen by the author's
    first commit; the builder may not edit it; results go to
    `RESULTS.md`; **encoding recuts are logged, property recuts are
    amendments**; the non-author review and the author's plain-language
    read. **No author words are quoted anywhere in this file** — the
    only block quote is A3 §A3.3, verified verbatim against
    `docs/phase-0-prereg-amendment-3.md:220-230`.
29. **The routed fork is genuine and is left open.** Routed item 1
    (`REFUSAL`) states both options and both costs, and the two
    instructions it sits between really do conflict (`:1270-1273`
    against `:1276` and `:1555-1559`), which a clerk cannot settle.
    **Not resolved here.** Routed item 2 is correctly *offered for veto,
    not routed* — a clerical path divergence from `ENUMERATION.md:112`
    and `LEDGER.md:11`, recorded rather than taken. Nothing else in the
    file is routed that a clerk could settle, and edit 16's gap is
    flagged to the reviewer, not to the author.
30. **Matrix expected reds against companion failed sets**, row by row:
    D1/C-C2, D3/C-C1, D4/C-C1+C-C10, D5/C-C5, D6/C-C7, D7/C-C9,
    D10/C-C3, D11, D12/C-C11, D13/C-C12 all agree. D2/C-C4 did not and
    is edit 10. D8's and D9's companions are the unnumbered ones of
    edit 16.

---

## Additions after the skeptic read (2026-09-15)

*Cited elsewhere in this file as **§9**.*

*Written by the drafting step after the skeptic pass above, which
recorded two gaps it was not permitted to repair (edits 16 and 17).
**Nothing was run and no model was touched.** Every `.out` line below is
a family-local or ledger-scratch result already on the record, cited as
the **descent** of a prediction and never as a capstone result. The
skeptic log is untouched. The routed `REFUSAL` fork (§8, item 1) is
untouched and unresolved *(as of this preamble's date; resolved by the
author 2026-09-18 — §8 item 1 and subsection (5) below)*. These additions change no query, no
probability, no timebox and no existing companion's obligation; they
number and specify three companions the ledger already requires, and
register two runs the builder owes before an existing companion's
minimality may be counted.*

### (1) The three transcribed companions, numbered and specified

`LEDGER.md:1505-1520` names five companions that *"exist and are red on
their own family's query, to be transcribed rather than rebuilt"* and
says *"the capstone's work is to show the same mutation red on the
**consuming** query, which is the A3.3 gate text's actual demand"*
(`:1516-1518`). §4 numbered D12's and D13's as **C-C11** and **C-C12**
and left three unnumbered. They are numbered here, in the three-set form
`LEDGER.md:1450-1491` fixes, with their sets **re-specified against the
capstone's own query names** per `:1474-1476`.

**What "not descended" means below.** Each set is split into the members
a family-local `.out` establishes, cited by line, and the members that
**no family model declares** — `ChainBroken` at any link, C-Q2, C-Q6,
C-Q8, C-Q9 and the `HonestChain` / `HonestStandingEstablished`
witnesses. The second group is predicted, not transcribed, exactly as
C-C1's link-1b member is (`LEDGER.md:1494`: *"It is **NOT YET
SHOWN**"*), and the withdrawn exhaustiveness rule does not apply to
either group (`:1459-1480`).

| # | Mutation, in the capstone's terms | (1) Expected failed set, in capstone query names | (2) Must stay green | (3) Witnesses that must stay reachable | Row | Descends from | Cases |
|---|---|---|---|---|---|---|---|
| **C-C13** | **Two configurations, both required**, because D8's link is asserted at every layer and the ledger names both mutations (`:702`, `:1509`). **(i) Type equality relaxed on the acceptance path** — S-P7 Q3 transcribed: in the capstone's check 5 the frame's object-type equality is dropped, `let framed(=OT_ATTEST, =alg, =id, =fp(k), mh, cv, pl) = fb` becomes `let framed(ot, =alg, =id, =fp(k), mh, cv, pl) = fb`, so an object signed as one enumerated `OT_*` type is accepted as another. **(ii) The wrapper type unread** — ablation a10 transcribed: the wrapped path's outer `=OT_WRAPPER` equality is dropped, so an honest attestation whose payload is a `wrap()` term is processed as a wrapper (`s-p7/READING-AIDS.md:210`). **Everything else retained**, in particular link 6b's inner `(issuerId, kfp)` conjunct, so the two severings stay separate (round-4 finding 2) | **C-Q1 link 6a** — `ChainBroken(lyr, LINK_6A)` reachable: at `L0` in (i), and **at the WRAPPER LAYER ONLY in (ii)** — `L0` at depth 1, `L0` and `L1` at depth 2, and **never the innermost attestation layer** *(REPAIR 2026-09-17, Codex round 10 finding 2; the withdrawn phrase, quoted: “at `L1` and `L2` in (ii)”; the per-depth assignment and its evidence are in the Cases cell)* — **not descended** (`ChainBroken` is declared in no model); **and** the retained query **`TypeConfused`**, which is the same severing seen by S-P7's transcribed judge and **is** descended: `is false` in both configurations, (i) `sp7_q3_companion_type_unchecked.out:727` (goal `:509`), (ii) `ablations/a10_no_wrapper_type.out:723`. Both modes | **link 6b** and C-Q4's `Rescoped` — the round-4 finding-2 separation, and the whole point of this companion: (i) `sp7_q3…:744`, (ii) `a10:738`, both `is true`; C-Q4's `InnerSigTransplanted` (i) `:761`, (ii) `a10:753`; C-Q3 `Reattributed` (ii) `a10:768`. **Not descended, predicted:** links 1a, 1b, 2a, 2b, 3, 4, 5; C-Q5, C-Q7, C-Q8, C-Q9; `Stripped`, `SignerForged`, `Spliced`. **Set-completeness note:** neither model declares `VersionLied`, and `sp7_q3…` declares no `Reattributed` either; the capstone's transcription carries both and **must add them to this set**, on the pattern the ledger uses for `Spliced` in C-C3's set (2) (`LEDGER.md:1440`, `:1496`) | `HonestWrappedAccepted` (i) `sp7_q3…:1067`, (ii) `a10:1072`; `HonestAccepted` (i) `:1267`, (ii) `a10:1270`. **Not descended:** `HonestChain(L1, t)` and `HonestChain(L2, t)`, which no S-P7 model declares and which `:1489-1490` makes a fixture condition of the run | **D8** (`:702`) | S-P7 Q3 + ablation a10 (`:702`, `:1509`); baseline `base_sp7.out:527` `TypeConfused` `is true`, with `:540`, `:553`, `:566`, `:1074`; committed producer `sp7_q2_degraded_compromised.out:527`, `sp7_q1_strict_dns_compromised.out:560` | **(d) red, descended, both configurations** — `sp7_q3_companion_type_unchecked` and `ablations/a10_no_wrapper_type` are **degraded, sole-channel** depth-1 models (`…:727`, `a10:723`). **(a)/(b): red predicted, and NO green-control reading is named.** S-P7's own Q3 row records the route as **honest W2 wrapper bytes** accepted as an attestation, *“no `dsks` in the derivation”* (`s-p7/RESULTS.md:46`) — an **honest-only** route, of exactly the kind `cap14d_sp7_q1_strict_q6a.out:892` shows survives the strict fixture. **No strict run of this companion exists**, so (a) and (b) are **predicted**, not descended — the basis is the honest-only route named above, not any reading of a `dsks` count *(REPAIR 2026-09-17, Codex round 6 finding 2)*. **(c): not stated — (c) is C-C1's run** *(REPAIR 2026-09-17, Codex round 6 finding 4)*; *the withdrawn phrase, quoted: “(c) as (a)/(b)”* — (c) leaks both channel keys and is not a configuration of (a)/(b) (`cap19b…:843`). Which way the strict runs fall is an **observation of the run**, recorded in `RESULTS.md`. *(REPAIR 2026-09-17, Codex round 5 finding 2)* **STRICT OUTCOME IN THREE LISTS** *(REPAIR 2026-09-17, Codex round 8 finding 2)*. **(a)/(b) descended green: NONE. Descended red: NONE** — `sp7_q3_companion_type_unchecked` and `ablations/a10_no_wrapper_type` are **degraded** depth-1 models and **no strict run of either configuration exists**. **Predicted red:** link 6a and the retained `TypeConfused`, basis the **honest-only route** this cell already names (`s-p7/RESULTS.md:46`, with `cap14d_sp7_q1_strict_q6a.out:892` as the instance of an honest-only route surviving the strict fixture). **Predicted green:** link 6b, C-Q4's `Rescoped` and `InnerSigTransplanted`, C-Q3, links 1a–5, C-Q5, C-Q7, C-Q8, C-Q9, `Stripped`, `SignerForged`, `Spliced`, and — once the transcription adds them — `VersionLied` and `Reattributed`; both witnesses reachable. **No green control is named in any case, descended or predicted.** **WHAT THE ACCEPTANCE REPORTS UNDER THESE TWO MUTATIONS** *(REPAIR 2026-09-17, Codex round 9 finding 1)*: both configurations touch **only the object-type equality** — (i) drops it on the acceptance path, (ii) drops the outer `=OT_WRAPPER` equality — and neither changes the key a layer's terms are verified against, so under §1.3's report contract each layer's `LayerAccepted` carries the **presented** `(t, ppf, sg, fb)` of that layer under its own accepting key `kX`, exactly as in the correct verifier. **No predicted outcome changes, and none of them depends on the report choice:** C-Q8, C-Q9, links 3, 4 and 5 stay predicted green because the terms reported are the terms checks 4, 5 and 6 still examine; what is severed is the **type** the bytes were processed as, which is link 6a and `TypeConfused`. **WHICH LAYER (ii) SEVERS, STATED PER DEPTH** *(REPAIR 2026-09-17, Codex round 10 finding 2)*. *The withdrawn phrase, quoted: “at `L1` and `L2` in (ii)”* — it assigned link 6a's red to the **innermost attestation layer**, whose type guard this configuration **retains**. **What a10 actually relaxes:** the wrapped path's own frame parse, `let framed(otW, =algW, =idW, =fp(kW), mhW, cvW, wrap(…)) = fbW` (`s-p7/proverif/ablations/a10_no_wrapper_type.pv:162`, inside `VerifierWrapped`, `:154-166`), while `InnerCheck`'s `let framed(=OT_ATTEST, =algI, =idI, =fp(kI), mhI, cvI, plI) = fbI` (`:136`, inside `InnerCheck`, `:129-142`, called from the wrapped path at `:166`) is **kept**. **The layer indexing, against this file's own convention.** §1.2's check 5 runs *“`InnerCheck` for `lyr ≠ L0`”*, so `L0` is the layer whose acceptance parses the **outermost presented frame**; (E4) fixes *“`lyr ≠ L0`; at depth 2 the innermost layer is `L2`”*; and §1.3 records *“one acceptance per layer and up to three (`L0`, `L1`, `L2`) at depth 2”*. **Therefore, at depth 1** the presentation has two layers — the **wrapper frame at `L0`** and the **innermost attestation at `L1`**, which is where this row's sibling C-C15(i) places its link-6b red — and (ii) removes the `=OT_WRAPPER` equality **at `L0` only**. **At depth 2** there are three — the outermost wrapper at `L0`, the wrapper immediately enclosing the innermost at `L1`, and the **innermost attestation at `L2`** — and (ii) removes that equality **wherever the wrapped path parses a wrapper frame: at `L0` and at `L1`**. **Link 6a's `ChainBroken(lyr, LINK_6A)` is therefore reachable at THOSE WRAPPER LAYERS ONLY and NEVER at the innermost attestation layer** — never `L1` at depth 1, never `L2` at depth 2 — because `=OT_ATTEST` is retained there. **A red at the innermost layer is configuration (i)'s**, which drops the equality **inside** the acceptance path's own frame parse; it is not (ii)'s, and a red there under (ii) would be a transcription defect to diagnose and record (`:1459-1480`), never a repair of this cell. **Shown, on copies of a committed family model, with the inner and outer type relations judged SEPARATELY:** on the correct model both are green — `WrongInnerType` (`cap23g_sp7_strict_type_base.out:1111`) and `WrongOuterType` (`:1124`), `VersionLied` green (`:1098`); under a10's mutation the **inner relation stays GREEN** (`cap23h_sp7_strict_type_outer.out:1313`) while the **outer is RED** (`:1520`), with the aggregate `TypeConfused` red beside it (`:749`), `Rescoped` (`:764`), `InnerSigTransplanted` (`:779`) and `Reattributed` (`:794`) green and both witnesses reachable (`:1100`, `:1298`). **What those two runs are, stated exactly: DEGRADED, SOLE-CHANNEL, DEPTH-1 copies** — their bodies are `sp7_q2_degraded_compromised.pv`'s, one authority key, the sole channel leaked (`cap23g_sp7_strict_type_base.pv:391`, `:400`; `cap23h_sp7_strict_type_outer.pv:214`, `:223`) — **despite the `strict` in the reviewer's filenames and the README's fourteenth-batch row calling them copies of `cap14a`**. **So NOTHING STRICT MOVES in this cell:** **(a)/(b) keep “descended green: NONE. Descended red: NONE”**, link 6a and `TypeConfused` stay **predicted** red there on the honest-only route this cell already names, and what `cap23g`/`cap23h` establish is the **layer assignment**, descended in **(d)**, where `TypeConfused`'s aggregate red is and **stays descended** (`ablations/a10_no_wrapper_type.out:723`). **And the aggregate does not establish the per-layer set:** `TypeConfused` fires over an accepted frame without naming the layer, which is exactly why the separated observers were needed. |
| **C-C14** | **The first-link Q2 broken companion transcribed** (`:703`, `:1509-1510`): the authority evidence commits to a **proper subset** of the D-2 tuple — the **issuer identity alone**, not `kfpr`, `sset`, `alg` or `ver` — in **both** the authority-channel processes and the capstone's check 1, so `checksign(ev, kCh) = (STMT_DIGEST, h(t))` becomes `= (STMT_DIGEST, id)`. The **two-worlds private-channel judge over the evidence *pair*** is retained unchanged (L-24, pair form only; `:703`). Strict form, cases (a) and (b) — the cases C-Q2 is stated for | **C-Q2** — `TwoWorldsBroken` reachable, which is D9's requirement and the consuming query A3.3 demands. **Descended, both variants:** `q2_broken_dns_compromised.out:464` and `q2_broken_repo_compromised.out:464`, both `is false`, against the producer's `is true` at `q4_attack_{dns,repo}_compromised.out:97`. **And, in the capstone:** **C-Q1 link 1a** (the accepted evidence no longer binds the accepted `t`), **link 1b** and the retained **`Accept ⟹ IssuerSigned`** — **not descended as three**: the spike carries all three in **one** formula, which this mutation reds in both variants (`:243` `is false`, baseline `q1_chain_dns_compromised.out:88` `is true`). The capstone's split is what resolves which conjunct fails; the spike cannot, and this file does not predict a different answer than "all three" | C-Q3, C-Q4's `Rescoped` and `InnerSigTransplanted`, C-Q5, C-Q7, C-Q8, C-Q9; links 2a, 2b, 3, 4, 5, 6a, 6b; `Stripped`, `SignerForged`, `Spliced`, `TypeConfused`, `VersionLied`. **Set-completeness note, and the sharpest one in this file: set (2) descends from nothing.** The spike's Q2 models declare **exactly two queries** (`:243`, `:464`) and no others, so every member above is **predicted, not transcribed**. **Also deliberately absent:** the single-evidence form `TwoWorldsSingle` (spike Q6, `q6_single_dns_compromised.out:93`), which per L-24 C-Q2 does not carry and which this companion therefore may not be read as preserving | `HonestChain(L0, t)` and `HonestAccepted`. **No family-local descent exists:** no first-link model declares a reachability witness at all (`q1_chain_dns_compromised.out` carries one RESULT line, `:88`; `q4_attack_dns_compromised.out` one, `:97`), so the witness half of this companion is the capstone's own obligation under `:1420-1421` and is **not** a transcription. Recorded so the builder does not look for a witness `.out` that does not exist | **D9** (`:703`) | first-link Q2 (`:703`, `:1509-1510`): `q2_broken_dns_compromised.out:243`, `:464`; `q2_broken_repo_compromised.out:243`, `:464`. Baselines: `q1_chain_dns_compromised.out:88`, `q4_attack_dns_compromised.out:97`, `q4_attack_repo_compromised.out:97` | **(a)/(b) red, DESCENDED FROM STRICT RUNS** — the first-link Q2 companion is a **strict** fixture and both variants are cited: `q2_broken_dns_compromised.out:464` and `q2_broken_repo_compromised.out:464`, with `:243` in both. **(c) and (d) are not stated**: C-Q2 is registered for (a) and (b) only (§3), so this companion has **no** configuration in the other two cases. **No green control arises**: the mutation changes the **evidence commitment itself** and needs no adversary key. *(REPAIR 2026-09-17, Codex round 5 finding 2)* **STRICT OUTCOME IN THREE LISTS** *(REPAIR 2026-09-17, Codex round 8 finding 2)*. **(a) descended red:** C-Q2 `TwoWorldsBroken` (`q2_broken_dns_compromised.out:464`) and the spike's **single combined chain formula** (`:243`), which carries link 1a, link 1b and `Accept ⟹ IssuerSigned` together. **(b) descended red:** the same two, on the repository variant (`q2_broken_repo_compromised.out:464`, `:243`). **Descended green: NONE in either case** — the spike's Q2 models declare **exactly those two queries and no others**, which is this row's own set-completeness note: *set (2) descends from nothing*. **Predicted green:** every member of set (2), and both witnesses reachable. **Predicted, and unresolved by the descent:** which of the three conjuncts inside `:243` fails — the capstone's split is what resolves it, and this file predicts no different answer than “all three”. **(c)/(d): not stated. No green control.** |
| **C-C15** | **Two configurations, both required**, because D11's consumer asserts scope at **both** depths (`:705`, `:1514-1515`). **(i) Outermost scope** — S-P7 Q6b transcribed: on the wrapped path the key and authority are read from the **wrapper** frame — the inner signature verified under `kW` instead of `kI`, and the inner frame's `kfp`, `id` and `mh` read but **not matched** — so the attribution is the wrapper's, not the innermost issuer's. Depth 1. **(ii) One level in** — S-P7 Q5c transcribed: at depth 2 the scope is taken from the **middle** layer rather than the innermost. **Everything else retained**, in particular the type equalities, which is what makes 6a and 6b separate conjuncts | (i) **C-Q1 link 6b at `L1`** — `ChainBroken(L1, LINK_6B)` reachable, **not descended** — and C-Q4's `Rescoped`, **descended**: `sp7_q6b_companion_key_outermost.out:769` `is false`. **And, added 2026-09-16 (Codex finding 3), two more this row previously listed as RETAINED: `C-Q3` (`Reattributed`) and `C-Q1 link 5`.** Configuration (i) verifies an **honest inner signature under the wrapper key** `kW`, which *is* S-P3's key-binding relation broken: the source **declares and emits** `Reattributed` and omits only the query, and its own header records that restoring the query makes Q6b **red** — `sp7_q6b_companion_key_outermost.pv:75-91` (declaration at `:75`, the recorded audit note at `:91`) and `s-p7/RESULTS.md:58-71` (*"it stays unreachable in Q3, both Q4 configurations, Q5c and Q6a and is **red in Q6b**"*, `RESULT not event(Reattributed(kExtra,kHonExtra,bytesExtra)) is false`). **Descended, therefore, not predicted.** The same trace accepts honest inner bytes under another key, so the inner frame's embedded `kfp` is no longer the accepting key's fingerprint and **link 5's frame-to-key equality fails at the inner layer too** (`sp7_q6b_companion_key_outermost.pv:192-199`, where `sgI` is checked under `kW` and the inner frame's `kfpI`, `idI`, `mhI` are read but not matched; against link 5's conjunct as this file states it, §3). **AND, added 2026-09-17 (REPAIR 2026-09-17, Codex round 2 finding 2), one more this row previously listed as RETAINED: `C-Q7`, for configuration (i) only.** Configuration (i) verifies an **honest inner signature under the wrapper key** `kW ≠ kI`, and that **is** C-Q7's forbidden relation by definition — an honest-released signature **term** accepted under a key that is not its issuer's. **Descended:** the C-Q7 signature-term judge (`GenericSigJudge`, `SigTransplanted`) added to the Q6b companion with the companion's own mutation and every registered query unchanged makes `SigTransplanted` **reachable** (`cap6b_sp7_q6b_sigjudge.out:1809` `is false`), where the **same judge on the correct S-P7 depth-1 model** leaves it **unreachable** (`cap6a_sp7_q2_sigjudge.out:1099` `is true`); both honest witnesses stay reachable in the companion (`cap6b…:1329`, `:1520`), so the red is a **severing and not a broken fixture**. **The red is a CONSEQUENCE of the scope severing, not a second severing of D5** — the same pattern this row already uses for C-Q4's `InnerSigTransplanted` just below — and **C-C6 remains C-Q7's own companion** (§4, D5/D6 row), so D5's discharge is untouched. **The reviewer's alternative — excluding inner acceptances from C-Q7's observation — is rejected**, for the reason the reviewer himself gives: it would **blind D5's producer**, C-Q7 being what D5's consumer (C-Q4's `InnerSigTransplanted` at the inner layer) consumes. **AND, IN (d), THE SAME FOUR RELATIONS ARE PREDICTED RED UNDER THE REPORT CONTRACT** *(REPAIR 2026-09-17, Codex round 10 finding 1, **corrected 2026-09-17 under Codex round 13 finding 2**)*, **for configuration (i) only**: **link 1a**, **link 2a's primary-slot relation**, **link 5's `mh` half** and **C-Q5's relation** *(REPAIR 2026-09-17, Codex round 13 finding 2: **link 1b comes OUT of this (d) list**. **The withdrawn membership, quoted:** “**THE SAME FIVE RELATIONS** … **link 1a**, **link 1b**, **link 2a's primary-slot relation**, **link 5's `mh` half** and **C-Q5's relation**” — five, now **four**. **Why:** **C-Q1-degraded does not assert link 1b at all** — the two forms differ in exactly that link and the fixture's channel leak, and C-Q1-degraded's frozen prediction is *“the same eight excluding link 1b”* (this file, `:314-318` and `:369-378`; §1.1's cases table at `:91`) — so **no (d) set of any companion can carry it**, at either colour. And the reviewer shows why it could not be read as a severing even if it were asserted: adding link 1b's publication-provenance correspondence to the **UNMUTATED** degraded S-P3 model already makes it `is false` (`cap26a_sp3_degraded_publication_baseline.out:676`, with `HonestAccepted` reachable at `:376`) — a **degraded baseline cost**, not evidence of C-C15's severing. **Link 1b's STRICT outcomes stand unchanged**, descended red in (a) and (b) with their cites, here and in the Cases cell.)*. The mutation is the one the strict copies carry — the presented inner tuple and evidence are **never checked** — and the degraded fixture is strictly weaker, so under §1.3's contract the inner acceptance reports, at either mode, terms no check touches. **PREDICTED, not descended: no degraded copy carries the observers** — `sp7_q6b_companion_key_outermost` declares none of these five judges, and `cap23c`–`cap23f` are **strict** copies (two authority processes, `out(c, skD)` / `out(c, skR)`) — so the degraded statement is an a fortiori prediction and nothing more. **The family's S-P7 Q6b row is NOT edited**: this is a capstone-side reading of the same transcription, registered here. **AND, IN (d), `SignerForged` IS PREDICTED RED TOO, UNDER THE SAME CONTRACT** *(REPAIR 2026-09-17, Codex round 11 finding 1)*, **for configuration (i) only**: the inner acceptance reports its own presented tuple and the manifest-named slot it reports as satisfied, and the degraded fixture is strictly weaker than the strict one in which the relation is **descended red** (`cap24b_sp7_strict_q6b_member.out:3211`, `cap24c…:3211`, against the all-green baseline `cap24a…:1421`), so the a fortiori reading carries. **PREDICTED, not descended, for the same reason as the four above: no degraded copy carries the membership observer** — `sp7_q6b_companion_key_outermost` declares no `SignerForged` judge and `cap24a`–`cap24c` are **strict** copies — and **the family's S-P2 and S-P7 rows are not edited**. **AND, IN (a) AND (b), EIGHT MORE MEMBERS FOR CONFIGURATION (i) — SEVEN RELATIONS, ALL DESCENDED RED** *(REPAIR 2026-09-17, skeptic read S-1)*. Rounds 9, 10 and 11 descended these **red in strict** on the Cases cell of this same row and each said, in terms, that memberships were not being edited; set (2) therefore went on listing them as retained in **both** configurations, and under §4's replacement rule — *“a companion failing outside its set … is a broken fixture to be diagnosed and recorded, never a finding”* — a builder running C-C15(i) in strict would have had to classify a **registered severing** as a broken fixture. **The three withdrawn sentences of the Cases cell, quoted:** “**Set (1), set (2) and set (3) memberships are not edited here; what changes is the descent**”, and, twice, “**Set (1), set (2) and set (3) memberships are again NOT edited here; what changes is the descent per case**”. They were accurate as round-by-round bookkeeping and false as a statement of this row's sets; the memberships are edited **here**, once, with the descent carried from the Cases cell and **not re-derived**. **The members, with the cites the Cases cell already carries** — **C-Q9** and **link 3**, which are one relation (`cap22e_sp7_strict_q6b_q9_inner.out:1334` in case **(a)**, `cap22f_sp7_strict_q6b_q9_inner_repo.out:1334` in case **(b)**; again at `cap23d…:1459` / `cap23f…:1459`); **link 1a** (`cap23d_sp7_strict_q6b_observers_tuple.out:2573`, `cap23f…:2573`); **link 1b** (`:1735`, `cap23f…:1735`); **link 2a's primary-slot relation** (`:2297`, `cap23f…:2297`); **link 5's `mh` half** (`:2017`, `cap23f…:2017`); **C-Q5's relation** (`:2883`, `cap23f…:2883`); and **`SignerForged`** (`cap24b_sp7_strict_q6b_member.out:3211`, `cap24c…:3211`), against the all-green matched strict baselines `cap22d_sp7_strict_base_q9.out:1186`, `cap23b_sp7_strict_base_observers_tuple.out:1306`, `:1329`, `:1343`, `:1357`, `:1371`, `:1385` and `cap24a_sp7_strict_base_member.out:1421`, with the four declared S-P7 queries green and both witnesses reachable in every mutant. **How they are descended is unchanged:** as **relations**, judged structurally on **strict** family copies, `ChainBroken` and `SetAltered` being declared in no copy — the round-nine shape, restated here and not re-derived. **They are in set (1) for CONFIGURATION (i), CASES (a) AND (b), and there only**: in **(d)** **SEVEN** of the same eight — **the eight LESS link 1b** — are **predicted** red, as the round-10 and round-11 blocks above register *(REPAIR 2026-09-17, Codex round 13 finding 2; **the withdrawn wording, quoted:** “in **(d)** the same eight are **predicted** red”, which carried link 1b into the degraded case along with the rest. **The (a)/(b) membership of link 1b is NOT touched**)*, and configurations **(ii)** and **(iii)** are untouched. **Nothing else moves:** no query, no probability, no timebox, no witness, no companion count, and the count of descended reds in (i) is still **SEVEN**, exactly as round eleven left it. **Configuration (ii) is unchanged**: Q5c leaves `Reattributed` unreachable on the restored query (`s-p7/RESULTS.md:58-71`) and takes scope from the middle layer without transplanting a signature across keys, so C-Q3, link 5 **and C-Q7** stay in **set (2)** for (ii) alone — C-Q7 green there **predicted, not descended**, since `cap6a`/`cap6b` are depth-1 copies and no S-P7 model declares C-Q7. (ii) **link 6b at `L2`** and C-Q4's `RescopedD2` half, **descended**: `sp7_q5c_companion_one_level_in.out:1131` `is false` while `RescopedD1` stays `is true` (`:690`) — which is what shows (ii) severs the innermost binding and not scope generally. **Under R-3 formulation W**, both configurations also red **C-Q6's CONJUNCT 3, scope agreement** — **`ScopeMisreported(aid, lyr, kX, id, kA, idA)` reachable** over a wrapped presentation, D11's conditional second consumer (`:705`) — **not descended**, no model declaring C-Q6, but **isolated at the reviewer's projection**: with only the envelope's reported attribution key changed, `cap10_ss_q3_scope_report_only.out:779` makes the judge's event **reachable**. **(i)** reports the **wrapper** frame's key **and identity**, so `(kA, idA) = (kW, idW) ≠ (kI, idI) = (kX, id)`; **(ii)** reports the **middle** layer's key and identity (`sp7_q5c_companion_one_level_in.pv:240`), so `(kA, idA) = (kM, idM) ≠ (kI, idI) = (kX, id)`; in both the standing path's own extraction is untouched and reports `(kX, id) = (kI, idI)`. *(Signature and comparison updated in place — REPAIR 2026-09-17, Codex round 4 finding 1; the withdrawn wording, quoted: “`ScopeMisreported(aid, lyr, kX, kA)` **reachable** … **(i)** reports the **wrapper** key, so `kA = kW ≠ kI = kX`; **(ii)** reports the **middle** layer's key … so `kA = kM ≠ kI = kX`; in both the standing path's own extraction is untouched and reports `kX = kI`.” **Both configurations misreport the key as well as the identity, so both stay in set (1) under the pair form; what the pair form adds is configuration (iii)**, Q6a, which misreports the identity **alone** and which a key-only judge could not see.)* *(RE-SPECIFIED 2026-09-17, Codex round 3 finding 2. **The withdrawn membership, quoted:** “**Under R-3 formulation W**, both configurations also red **C-Q6's standing conjunct** over a wrapped presentation, D11's conditional second consumer (`:705`) — **not descended**, no model declaring C-Q6.” That was **wrong after the round-2 repair**: the standing conjunct is computed on the standing path's own structural extraction, which a scope mutation does not touch, so it stays **green** — it moves to set (2) below, together with the entitled-key conjunct.)* **Set-completeness note:** configuration (i) *also* reds C-Q4's `InnerSigTransplanted` family-locally (`sp7_q6b…:1058` `is false`), a **consequence** of verifying the inner signature under `kW` and not a separate severing; configuration (ii) leaves it green (`sp7_q5c…:1169`). **Mechanism-review contrast (`formal/spike/floor-structure/PROBE.md:46`):** the nearest alternative that severs the same fact with one fewer red is **Q6a**, identity-only from the outermost frame — `Rescoped` red (`sp7_q6a_companion_identity_outermost.out:806`) with `TypeConfused` (`:503`) **and** `InnerSigTransplanted` (`:819`) both green. **(iii) ISOLATION CONFIGURATION — S-P7 Q6a TRANSCRIBED, *identity from the outermost frame, key retained*, REGISTERED 2026-09-17** *(REPAIR 2026-09-17, Codex round 4 finding 1. The withdrawn phrase, quoted: “It is registered here as the **isolation contrast**, not as a third configuration.” Q6a was named as a contrast and given **no three-set specification**, so nothing in this file required it to be run and nothing recorded what it must do to conjunct 3. Round 4's finding 1 made it load-bearing: Q6a **is** the identity-only case the withdrawn key-only judge could not see, so it is the run that isolates conjunct 3's **identity** half. It is a **third configuration of C-C15, of the isolation kind** — the pattern §9(2) uses for `C-C8-i` / `C-C8-ii` — and it adds **no companion**: the count stays **sixteen** *(dated clause, REPAIR 2026-09-17, skeptic read S-6: **this count is SUPERSEDED by §4's count paragraph**, which registers **SEVENTEEN** companions after round five added C-C17 and which supersedes every earlier “sixteen” in this file outside the skeptic log and the dated repair sections. This clause carries a dated repair marker but sits in the operative §9(1) table, so whether it was superseded was a reading; it is settled here. It is **left in place as round four wrote it**, and what it asserts — that configuration (iii) adds **NO** companion — stands unchanged; only its arithmetic is stale)*, and it carries no timebox of its own, running inside link 6b's 45-minute and C-Q6's 90-minute boxes.)* **The mutation:** on the wrapped path the inner signature is verified under `kI` **as in the correct model** and the inner frame's `kfp` **is matched**, while the **attributed issuer identity** is read from the **wrapper** frame — `idW` in place of the innermost `idI`. Depth 1. Everything else retained, including the type equalities and the whole key binding. **Set (1), expected failed:** **C-Q6's conjunct 3 — the registered pair judge `ScopeMisreported(aid, lyr, kX, id, kA, idA)` REACHABLE, and the isolation observer `ScopeIdentityOnly(aid, lyr, id, idA)` REACHABLE WITH IT**, with `kA = kX` and `idA = idW ≠ idI = id`: the **pair** differs, so conjunct 3 fires, and the observer records that it is the **identity** comparison alone that made it fire *(NAMES REGISTERED 2026-09-17, skeptic read S-10, on the §(1) declaration of the same date. **The withdrawn wording, quoted:** “**C-Q6's conjunct 3, and specifically its IDENTITY half** — `ScopeMisreported(aid, lyr, kX, id, kA, idA)` **reachable** with `kA = kX` and `idA = idW ≠ idI = id`”. **What was wrong:** it called the pair judge a “half”, and set (2) below called the other “half” a thing that must stay green — which under **one** pair-form judge is the same query in both sets, required red and green in one configuration. §(1) now declares **one** pair judge and **two** observers; conjunct 3 is the pair judge and it is **here, in set (1), reachable**)* — **not descended**, no model declaring C-Q6, but **isolated at the reviewer's projection**, where the identity observer on the structural join is **reachable** with the key unchanged (`cap12e_ss_q1_join_scope_identity.out:945`, the copy's `ScopeIdentityWrong`, which is `ScopeIdentityOnly`'s shape); **C-Q4's `Rescoped`**, **descended**: `sp7_q6a_companion_identity_outermost.out:806` `is false`, goal at `:516`; and **C-Q1 link 6b at `L1`** — `ChainBroken(L1, LINK_6B)` reachable — **not descended**, `ChainBroken` being declared in no model. **Set (2), must stay green — and this is the point of the configuration: it contains the ISOLATION OBSERVER `ScopeKeyOnly(aid, lyr, kX, kA)`, which must be UNREACHABLE here** *(NAMES REGISTERED 2026-09-17, skeptic read S-10. **The withdrawn wording, quoted:** “**Set (2), must stay green — and this is the point of the configuration: it includes CONJUNCT 3's KEY HALF.** A judge comparing the **key alone** is **unreachable** here”. **What was wrong:** the “key half” is **not a query of this file**. §(1) declares **one** registered pair judge, `ScopeMisreported`, and **two observers**; conjunct 3 **is** the pair judge, it is **reachable** here, and it is in **set (1)** above. What set (2) contains is the **observer** `ScopeKeyOnly` — never counted as a query, never timeboxed, never a discharge. Read as it stood, the two sets put one registered query in both, at opposite colours)*, so the run shows that what fires the pair judge is the **identity** comparison and nothing else. **Descended, on the committed companion itself:** a key-only scope judge — `ScopeKeyOnly`'s shape — added beside Q6a's own unchanged `Rescoped` query stays **green** (`cap12f_sp7_q6a_keyjudge.out:1339`) while the committed pair-form `Rescoped` is **red** (`:818`); at the reviewer's projection the key-only judge is likewise unreachable with only the identity changed (`cap12e…:570`, the copy's four-place `ScopeMisreported`, which is `ScopeKeyOnly`'s shape). Also green: **`TypeConfused`** (`sp7_q6a…:503`) and **C-Q4's `InnerSigTransplanted`** (`:819`), both **descended**; **C-Q6's conjunct 1** (the standing verdict, unrestricted and honest-key) and **conjunct 2** (the entitled key), both **predicted green** on the round-two independence — a scope mutation does not touch the standing path's own structural extraction — and isolated at the projection (`cap12e…:542`, `:556`, `:1368`, with the substitution excluded at `:563`); **link 6a**; and, **not descended, predicted:** C-Q3, C-Q5, C-Q7, C-Q8, C-Q9, links 1a, 1b, 2a, 2b, 3, 4, 5, `Stripped`, `SignerForged`, `Spliced`, `VersionLied`. **Set (3), witnesses that must stay reachable — the honest wrapped witnesses, descended:** `HonestWrappedAccepted` (`sp7_q6a_companion_identity_outermost.out:1118` `is false`) and `HonestAccepted` (`:1314` `is false`); in the capstone also `HonestChain(L1, t)` and, for the C-Q6 half, `HonestStandingEstablished` over a wrapped presentation and `HonestWrappedStandingAgreed`, **not descended** (honest standing is reachable at the projection, `cap12e…:1718`). **Configurations (i) and (ii) remain the two SEVERING configurations, both required, exactly as the mutation column states; (iii) is the isolation run that shows conjunct 3's two halves are separately live.** | **link 6a** and `TypeConfused` — the round-4 finding-2 separation and the whole point of this companion, shown on **committed** output in both configurations: (i) `sp7_q6b…:489`, (ii) `sp7_q5c…:652`, both `is true`; in (ii) also `RescopedD1` (`:690`) and `InnerSigTransplanted` (`:1169`). **In configuration (ii) only:** C-Q3 (`Reattributed`), **link 5** and **C-Q7** — see set (1), where all three are moved out of the retained set for configuration (i): C-Q3 and link 5 on 2026-09-16 (Codex finding 3), **C-Q7 on 2026-09-17 (REPAIR 2026-09-17, Codex round 2 finding 2)**. For (ii), C-Q7 is **predicted** green, not descended. **ADDED FOR BOTH CONFIGURATIONS 2026-09-17** *(REPAIR 2026-09-17, Codex round 3 finding 2)*: **C-Q6's conjunct 1, the standing verdict** (both the unrestricted strict and the honest-key forms) **and C-Q6's conjunct 2, the entitled key** (`StandingUnentitledWrapped` unreachable) — both **predicted green**, because after the round-2 repair the standing path extracts the innermost `(t, ppf, sg, fb)` structurally and is **untouched by a scope mutation**, which changes only what the **envelope** path reports. **Isolated at the reviewer's projection:** with only the reported attribution key changed, wrapped designation stays green (`cap10_ss_q3_scope_report_only.out:798`, `:811`), entitled-key safety stays green (`:856`) and honest standing stays reachable (`:1205`), while `ScopeMisreported` goes reachable (`:779`) — set (1). **SET (2) IS READ PER CASE, AND THE CASES LISTS GOVERN** *(REPAIR 2026-09-17, skeptic read S-1, on the pattern set (2) of **C-C17** already uses — “`PossessionTransplanted` is **NOT** in this set — it is in set (1), as the run requires” — and the per-case wording C-C6 and C-C8 already carry. **The withdrawn membership, quoted:** “**Not descended, predicted, both configurations:** C-Q5, C-Q8, C-Q9; links 1a, 1b, 2a, 2b, 3, 4; `Stripped`, `SignerForged`, `Spliced`, `VersionLied`.” **What was wrong:** seven of those relations are descended **RED** in (a) and (b) for configuration **(i)** by the Cases cell of this same row — C-Q9 and link 3, links 1a, 1b and 2a, C-Q5 and `SignerForged`, with link 5's `mh` half beside them — so the row required them retained and severed at once. They are now in **set (1)**, for (i) in (a)/(b), with their existing cites.)* **Configuration (i), cases (a) and (b):** set (2) does **not** contain C-Q5, C-Q9, links 1a, 1b, 2a or 3, or `SignerForged`; what remains of the withdrawn list is **C-Q8, link 2b, link 4, `Stripped`, `Spliced`** and **`VersionLied`**, each **not descended, predicted green**, with its basis stated in the Cases cell. **Configuration (i), case (d):** **SIX** of the same seven come out of set (2) there too, **predicted red** under §1.3's report contract (set (1)'s round-10 and round-11 blocks); **link 1b comes out of set (2) in (d) WITHOUT entering set (1) — it is in NO (d) set of this configuration, being unasserted in degraded** *(REPAIR 2026-09-17, Codex round 13 finding 2; **the withdrawn membership, quoted:** “the same seven come out of set (2) there too, **predicted red**”, which assigned a **failure** to a query C-Q1-degraded does not assert. **Why:** **C-Q1-degraded does not assert link 1b at all** — the two forms differ in exactly that link and the fixture's channel leak, and C-Q1-degraded's frozen prediction is *“the same eight excluding link 1b”* (this file, `:314-318` and `:369-378`; §1.1's cases table at `:91`) — so **no (d) set of any companion can carry it**, at either colour. And the reviewer shows why it could not be read as a severing even if it were asserted: adding link 1b's publication-provenance correspondence to the **UNMUTATED** degraded S-P3 model already makes it `is false` (`cap26a_sp3_degraded_publication_baseline.out:676`, with `HonestAccepted` reachable at `:376`) — a **degraded baseline cost**, not evidence of C-C15's severing. **Link 1b's STRICT outcomes stand unchanged**, descended red in (a) and (b) with their cites, here and in the Cases cell.)*; the remaining six — C-Q8, link 2b, link 4, `Stripped`, `Spliced`, `VersionLied` — stand. **Configurations (ii) and (iii), every case:** the withdrawn list stands **exactly as written** — C-Q5, C-Q8, C-Q9; links 1a, 1b, 2a, 2b, 3, 4; `Stripped`, `SignerForged`, `Spliced`, `VersionLied`, **not descended, predicted green** — no strict run of (ii) existing, and (iii) checking every one of the terms those relations are over. *(REPAIR 2026-09-17, Codex round 13 finding 2, carried: **link 1b is a member of this list in (a) and (b) only** — C-Q1-degraded does not assert it (`:314-318`, `:369-378`), so in (d) it is **not asserted**, neither green nor red, for (ii) and (iii) as for (i).)* **No query, probability, timebox, witness or companion count moves; what moves is which set a registered red is read out of.** *(The earlier withdrawal of C-Q7 from this list stands as written below.)* *(Withdrawn 2026-09-17 and quoted: “**Not descended, predicted, both configurations:** C-Q5, **C-Q7**, C-Q8, C-Q9; …” — C-Q7's membership in this set for configuration **(i)** is withdrawn, and it was never “not descended” once the judge was run: `cap6b_sp7_q6b_sigjudge.out:1809`.)* **Set-completeness note, CORRECTED 2026-09-16 (Codex finding 3):** the draft said *neither model declares `Reattributed`*. **That is false of the source.** `sp7_q6b_companion_key_outermost.pv:75-91` declares the event, fires it from the transcribed S-P3 judge and records the restored-query red; only the **query** is omitted, on the S-P3 Q3 pattern. `VersionLied` is genuinely undeclared in both and the capstone's transcription must add it. **The principle the draft got wrong, stated so it is not repeated: preserved type soundness does not imply preserved key binding.** `TypeConfused` staying green under Q6b says the object was processed *as* the type it was signed as; it says nothing about *whose key* the bytes were accepted under, and Q6b is precisely the mutation that keeps the first and breaks the second | (i) `HonestWrappedAccepted` (`sp7_q6b…:1317`), `HonestAccepted` (`:1508`); (ii) `HonestWrappedAcceptedD1` (`sp7_q5c…:1496`), `HonestWrappedAcceptedD2` (`:1876`), `HonestAccepted` (`:2097`) — in the capstone, `HonestChain(L1, t)` and `HonestChain(L2, t)`. **Not descended:** `HonestStandingEstablished` over a wrapped presentation, required for the C-Q6 half | **D11** (`:705`) — **RE-STATED WITH ITS CASES** *(REPAIR 2026-09-17, Codex round 5 finding 2. The withdrawn sentence, quoted: “the **C-Q1 link-6b half unconditionally**, under **both C-Q1 forms** and every R-3 formulation; the **C-Q6 half conditionally**, and only if C-Q6 terminates” — it invoked both C-Q1 forms with **no case assignment**, which is what let configuration (i)'s failed set read as holding in strict, where its transcription is **green**.)*: the **C-Q1 link-6b half** is served **in every case the relevant configuration fires in**, which the Cases cell states configuration by configuration — in **(d)** by (i), (ii) and (iii); in **(a)/(b)** by **(iii) alone**, (i) being **green in strict over the four queries `cap14b`/`cap14c` declare and PREDICTED green over the rest** there (`cap14b…:550`) *(REPAIR 2026-09-17, Codex round 8 finding 2)* — **amended in place 2026-09-17** *(REPAIR 2026-09-17, Codex round 9 finding 1)*: *“PREDICTED green over the rest”* **no longer holds for C-Q9 and link 3**, which are now **descended RED** in (a) and (b) under §1.3's report contract (`cap22e_sp7_strict_q6b_q9_inner.out:1334`; `cap22f_sp7_strict_q6b_q9_inner_repo.out:1334`); the rest of the phrase stands, and **D11's discharge in (a)/(b) still rests on configuration (iii)**, C-Q9 and link 3 being **D10's** consumers and not D11's — *the withdrawn phrase, quoted: “(i) being a **green control** there”* and (ii) an observation of the run. **AND AMENDED AGAIN 2026-09-17** *(REPAIR 2026-09-17, Codex round 10 finding 1)*: the surviving half of that phrase — *“PREDICTED green over the rest”* — now covers **five fewer members**. **Links 1a, 1b, 2a, link 5's `mh` half and C-Q5 are descended RED in (a) and (b) as well** (`cap23d_sp7_strict_q6b_observers_tuple.out:2573`, `:1735`, `:2297`, `:2017`, `:2883`; `cap23f_sp7_strict_q6b_observers_tuple_repo.out` at the same lines), so the phrase now holds only over the predicted-green list the Cases cell states member by member. **D11's discharge in (a)/(b) is unchanged and still rests on configuration (iii)**: the C-Q1 half D11's row names is the **link-6b** half (`:705`), and **none of the five is link 6b**. The **C-Q6 half** is conditional, and only if C-Q6 terminates. **D11's strict discharge therefore rests on configuration (iii)**, whose strict red is descended at `cap14d_sp7_q1_strict_q6a.out:892` in case **(a)** and at `cap14d_sp7_q1_strict_q6a_repo.out:893` in case **(b)** *(REPAIR 2026-09-17, Codex round 6 finding 5)* | S-P7 Q6b and Q5c, **and Q6a, transcribed 2026-09-17 as configuration (iii)** (`:705`, `:1514-1515`); **configuration (iii)'s descent, 2026-09-17** (Codex round 4 finding 1): `sp7_q6a_companion_identity_outermost.out:806` (`Rescoped` `is false`, goal `:516`), `:503` (`TypeConfused` green), `:819` (`InnerSigTransplanted` green), witnesses `:1118`, `:1314`; the key-only judge on that same companion green at `cap12f_sp7_q6a_keyjudge.out:1339` beside the committed `Rescoped` red at `:818`, witnesses `:1130`, `:1326`; the identity-only projection `cap12e_ss_q1_join_scope_identity.out:945` (identity judge reachable) against `:570` (key-only judge unreachable), with `:542`, `:556`, `:1368`, `:563`, `:1718`; baseline `base_sp7.out:540` and committed producer `sp7_q2_degraded_compromised.out:540`, `Rescoped` `is true`. **C-Q7 scratch runs, 2026-09-17** (Codex round 2 finding 2): `cap6b_sp7_q6b_sigjudge.out:1809` (reachable in (i)), witnesses `:1329`, `:1520`, the companion's own reds unchanged (`:781`, `:1070`) and `TypeConfused` green (`:501`); baseline `cap6a_sp7_q2_sigjudge.out:1099` (unreachable on the correct model), every registered query as committed (`:539`, `:552`, `:565`, `:578`, `:1086`), witnesses `:877`, `:1073` | **Per configuration, as round five's disposition 2 fixes them** *(REPAIR 2026-09-17, Codex round 5 finding 2)*. **(i) Q6b, outermost scope:** red in **(d)**, **descended** (`sp7_q6b_companion_key_outermost.out:769`, `:1058`; C-Q7 at `cap6b…:1809`); **IN (a) AND (b), THE THREE LISTS** *(REPAIR 2026-09-17, Codex round 8 finding 2)* — Q6b's mutation transcribed onto the **correct strict** model with **both outer authority checks and the same-key wrapper signer retained**. **Descended green — the four S-P7 queries the copies declare, and their two witnesses:** C-Q4's `Rescoped` (`cap14b_sp7_q1_strict_q6b.out:550`), C-Q4's `InnerSigTransplanted` (`:559`), C-Q3 `Reattributed` (`:568`) and `TypeConfused` (`:541`), with `HonestWrappedAccepted` (`:843`) and `HonestAccepted` (`:1047`) reachable; `cap14c_sp7_q1_strict_repo_q6b.out` is identical line for line, which is what makes **(b)** descended and not predicted here. **Descended red: NONE.** **Predicted green, with the basis stated:** **C-Q7**, **C-Q8**, **C-Q9** and the **linkage conjuncts** — links 1a, 1b, 2a, 2b, 3, 4, 5, 6a, 6b — together with C-Q5, `Stripped`, `SignerForged`, `Spliced` and `VersionLied`. `cap14b_sp7_q1_strict_q6b.pv:113-130` and `cap14c_sp7_q1_strict_repo_q6b.pv:113-130` declare **four queries and two witnesses and nothing else**. **The basis, stated rather than assumed:** in this strict transcription the inner signature is verified under `kW` over `fbI` **with byte binding retained** — the presented bytes are the signed bytes — so **round 8 finding 1's route does not open here**: C-C5's red comes from *unbinding* the inner signature from the presented bytes, which this configuration does not do. C-Q7 is predicted green in strict for the same reason §1.1's enrolment rule gives: the adversary has no authorized wrapper key, so the transplant that makes C-Q7 reachable in **(d)** (`cap6b_sp7_q6b_sigjudge.out:1809`) has no strict counterpart. **These are predictions with a stated basis, and which way they fall is an observation of the run.** **C-Q9 AND LINK 3 ARE NOW DESCENDED RED IN (a) AND (b)** *(REPAIR 2026-09-17, Codex round 9 finding 1)*. *The withdrawn wording, quoted: “**Predicted green, with the basis stated:** **C-Q7**, **C-Q8**, **C-Q9** and the **linkage conjuncts** — links 1a, 1b, 2a, 2b, 3, 4, 5, 6a, 6b — together with C-Q5, `Stripped`, `SignerForged`, `Spliced` and `VersionLied`.”* **C-Q9 and link 3 come out of that list; every other member of it stands unchanged.** **Why.** Under §1.3's **report contract** the inner acceptance of this configuration reports the **presented inner** `(kW, tI, ppfI)` — the terms that layer's acceptance was about — and this mutation **never checks the presented `tI` or `ppfI` at all**: it checks the **outer** possession proof and then verifies the inner signature under `kW`. **Descended red, in (a) and (b):** C-Q9's structural possession judge — `cap22e_sp7_strict_q6b_q9_inner.out:1334` in case **(a)** (DNS leaked) and `cap22f_sp7_strict_q6b_q9_inner_repo.out:1334` in case **(b)** (repository leaked) — with the four S-P7 queries still green (`cap22e:569`, `:578`, `:587`, `:596`; `cap22f` the same) and both witnesses still reachable (`cap22e:871`, `:1075`; `cap22f:871`, `:1075`), so the red is a **severing and not a broken fixture**. **Link 3 red with it, by shape:** `ChainBroken(lyr, LINK_3)` is declared in no model, so link 3's red is **not descended as a `ChainBroken` result**; what **is** descended is **link 3's relation — which is C-Q9's** — judged structurally on a family copy, exactly as `cap20a` descends it for C-C3 and `cap21d` descends link 4's for C-C5. **The rejected reading, recorded with its run:** reporting the **checked outer** `(kW, tW, ppfW)` makes the same judge **green** (`cap22g_sp7_strict_q6b_q9_outer.out:1084`); §1.3's contract rejects it because it makes this companion's failure invisible by reporting what the verifier did check. **The matched strict baseline, reporting its own checked inner terms, is green** (`cap22d_sp7_strict_base_q9.out:1186`). **And the round-eight basis sentence falls by half.** *The withdrawn sentence, quoted: “**The basis, stated rather than assumed:** in this strict transcription the inner signature is verified under `kW` over `fbI` **with byte binding retained** — the presented bytes are the signed bytes — so **round 8 finding 1's route does not open here**: C-C5's red comes from *unbinding* the inner signature from the presented bytes, which this configuration does not do.”* **Its C-Q8 half is RETAINED and is still true:** byte binding **is** retained in this transcription, C-C5's unbinding route does **not** open, and **C-Q8 stays predicted green**. What falls is the **C-Q9 half** — the sentence was read as covering C-Q9 too, and C-Q9's relation is not about bytes but about the **possession message over the accepted manifest**, which this mutation leaves unchecked. **C-Q7 stays predicted green**, on §1.1's enrolment reason, unchanged. **Set (1), set (2) and set (3) memberships are not edited here; what changes is the descent**: *the round-eight line “**Descended red: NONE.**” is withdrawn for configuration (i)* and replaced by the two reds above, and this configuration is no longer green throughout in strict over the capstone's query set. **AND FIVE MORE MEMBERS OF THAT LIST ARE NOW DESCENDED RED IN (a) AND (b)** *(REPAIR 2026-09-17, Codex round 10 finding 1)*. *The withdrawn wording, quoted: “**C-Q9 and link 3 come out of that list; every other member of it stands unchanged.**”* **What stands unchanged is smaller than that sentence claimed.** Under §1.3's **report contract** the inner acceptance of this configuration reports the **presented inner** terms, and this mutation checks **none of them**: it checks the **outer** tuple, evidence and possession, verifies the inner signature under `kW`, and reads the inner frame's `kfp`, `id` and `mh` **without matching them**. Every registered relation **over the reported inner terms** is therefore exposed, not possession alone. **The route, stated:** an honest **same-key** wrapper's **valid** inner signature, with its bytes and the **outer credentials retained**, and the **presented inner tuple and evidence replaced** — **no adversary-authorized wrapper key**, and **neither contestable choice reversed** (same-key wrapping stands; compromised-channel-only enrolment stands). **Descended red in (a) and (b), beside C-Q9 and link 3:** **link 1a** — the presented inner evidence verifies over `tI` — (`cap23d_sp7_strict_q6b_observers_tuple.out:2573`); **link 1b** — the inner tuple has a prior authority publication — (`:1735`); **link 2a's primary-slot relation**, `fp(k) = kfpr` (`:2297`); **link 5's `mh` half**, `mh = h(tI)` (`:2017`); and **C-Q5's relation** — an honest accepting key reports its **sole** signed manifest — (`:2883`); with **C-Q9** red beside them (`:1459`), the four S-P7 queries the copy declares still **green** (`:686`–`:716`) and both witnesses still **reachable** (`:992`, `:1199`), so these are **severings and not a broken fixture**. **Case (b) descends in its own right** on the repository-leaked variant, line for line: `cap23f_sp7_strict_q6b_observers_tuple_repo.out:1735`, `:2017`, `:2297`, `:2573`, `:2883`, with C-Q9 `:1459`, the four queries `:686`–`:716` and the witnesses `:992`, `:1199`. **The matched strict baseline is ALL GREEN** — the same six observers on the **correct** strict model, reports restricted to well-formed `authTuple` terms: `cap23b_sp7_strict_base_observers_tuple.out:1329`, `:1343`, `:1357`, `:1371`, `:1385`, with C-Q9 green at `:1306` — which is what makes the reds **results** and not artefacts of the observers. **How these reds are descended, in the round-nine shape:** `ChainBroken(lyr, LINK_*)` is declared in no model, so **none of links 1a, 1b, 2a and 5 is descended as a `ChainBroken` result**, and neither copy declares `SetAltered`; what **is** descended is each member's **relation**, judged structurally on a **strict** family copy — exactly as `cap20a` descends link 3's relation for C-C3, `cap21d` link 4's for C-C5 and `cap22h` link 5's `mh` half for C-C8. **The contrast with C-C8 is not a contradiction:** C-C8's strict `mh` half is **green** (`cap22h_sp2_strict_cc8_mh.out:1478`) because there the honest channel's tuple pin keeps `mh = h(t)` for the tuple the acceptance is about; here the tuple the acceptance is about is the **presented inner** one, which this mutation never pins. **What remains PREDICTED GREEN, each with its basis:** **C-Q7** — §1.1's compromised-channel-only enrolment gives the adversary no authorized wrapper key in strict, so the transplant that reds C-Q7 in **(d)** (`cap6b_sp7_q6b_sigjudge.out:1809`) has no strict counterpart; **C-Q8** — **byte binding is retained**, the inner signature being verified under `kW` over the **presented** `fbI`, so C-C5's unbinding route does not open (the retained half of the round-eight basis sentence); **link 4** — possession-to-signing over that same retained byte binding; **link 2b** — this configuration removes **no set-logic check** and adds no slot, and **no observer on the completeness correspondence was run**, so it stays a prediction; **link 6a** — the type equalities are **retained**, which is this configuration's whole separation from C-C13; **`Stripped`** — a set-logic relation whose red is **NOT** inferred from the membership result recorded below, no judge for it being declared in any copy *(REPAIR 2026-09-17, Codex round 11 finding 1: `SignerForged` is removed from this list and is now descended red — see the round-11 block below. The withdrawn clause, quoted: “**`Stripped`** and **`SignerForged`** — the set-logic relations over the **outer** tuple this mutation still checks in full, neither judge declared in these copies”)*; **`Spliced`** — the common-content equalities are untouched; **`VersionLied`** — the recorded-version check is untouched. **These are predictions with a stated basis, and which way they fall is an observation of the run.** **Link 6b is stated where it already is** — in the Row column's D11 sentence, where (i)'s link-6b red is **not** produced in (a)/(b) and D11's strict discharge therefore rests on **(iii)** — and it is not restated in this list. **Set (1), set (2) and set (3) memberships are again NOT edited here; what changes is the descent per case**: configuration (i) now carries **six descended reds** in (a) and in (b), and **no descended green beyond the four S-P7 queries and two witnesses the copies declare**. **AND `SignerForged` IS NOW DESCENDED RED IN (a) AND (b), SO THE COUNT IS SEVEN** *(REPAIR 2026-09-17, Codex round 11 finding 1)*. *The withdrawn clause, quoted: “configuration (i) now carries **six descended reds** in (a) and in (b)”.* **Why the outer-tuple basis fails.** The withdrawn justification called `SignerForged` a relation over the **outer** tuple, which this mutation still checks in full. Under §1.3's **report contract** the inner acceptance reports its **own presented** tuple and the **manifest-named slot** it reports as satisfied — terms this mutation never checks — so the set-logic judge reads the presented inner pair and not the checked outer one. **Descended red, in (a) and (b):** S-P2's registered membership observer (`MemberJudge`'s first arm, `s-p2/PREDICTIONS.md:270-273`: an honest `(key, manifest)` from `honestKeyCh` against a reported `(manifest, slot fingerprint, accepting key)` from `slotCh`, firing when the accepting key is not the honest signer) added to the round-ten copies with their fixtures and verifier checks unchanged makes `SignerForged` **reachable** — `cap24b_sp7_strict_q6b_member.out:3211` in case **(a)** (DNS leaked) and `cap24c_sp7_strict_q6b_member_repo.out:3211` in case **(b)** (repository leaked), identical line for line — with the four S-P7 queries the copies declare still **green** (`cap24b:708`–`:738`) and both witnesses still **reachable** (`:1014`, `:1221`), so this is a **severing and not a broken fixture**. **The matched strict baseline keeps it unreachable**, the same observer on the **correct** strict model with the round-ten reports: `cap24a_sp7_strict_base_member.out:1421`. **The route, stated** (`cap24b:3199-3211`): the same-key wrapper's **valid** wrapping credentials retained, the **other** honest issuer's manifest presented as the inner tuple, and its named slot reported as satisfied by the **wrapper** key — `SignerForged(M2, pk(skI1))`. **No adversary-enrolled identity is used and neither contestable choice is reversed** (same-key wrapping stands; compromised-channel-only enrolment stands). **How it is descended:** as a **relation**, judged structurally on a **strict** family copy — the round-nine shape, and `SetAltered` is declared in neither copy, so nothing is claimed for `SetAltered`. **LINK 2b AND `Stripped` STAY PREDICTED, on the reviewer's own limits:** the reviewer ran an exploratory link-2b completeness projection and **expressly declined to count it**, because that family projection **lacks the capstone's retained two-signer set logic** and therefore cannot settle link 2b — which this configuration in any case leaves structurally untouched, adding no slot and removing no set-logic check; and `Stripped`'s red is **not inferred** from the membership result, `SignerForged` and `Stripped` being different relations and no `Stripped` judge being declared in any copy. **Both remain predictions with a stated basis, and which way they fall is an observation of the run.** **Set (1), set (2) and set (3) memberships are again NOT edited here; what changes is the descent per case.** **AND C-Q7's AND C-Q8's RELATIONS ARE NOW DESCENDED GREEN IN (a) AND (b)** *(DATED NOTE, 2026-09-17, after the twelfth Codex non-author round, `docs/reviews/2026-09-17-codex-review-capstone-predictions-round12.md`, which found **no new run-backed defect**. This is a **strengthening entered as a note, not a repair**: no finding is dispositioned, nothing is withdrawn, and two **predicted** greens become **descended** greens.)* The reviewer's four control runs, reproduced on our tree as the **sixteenth batch** of `formal/suite/ledger-tests-2026-09-14/README.md`, add to the round-eleven strict copies a **signature-term observer** (C-Q7's relation, `GenericTransplant`) and a **structural byte-binding observer** (C-Q8's relation, `GenericBytesUnbound`), with every fixture, verifier check and registered query otherwise unchanged. **Descended green in (a)**, DNS leaked: `cap25a_sp7_strict_q6b_sigjudges.out:1306` (C-Q7's relation `is true`) and `:1317` (C-Q8's relation `is true`), with the four S-P7 queries green (`:777`–`:810`), both witnesses reachable (`:1087`, `:1295`) and `SignerForged` still red (`:3315`), as in `cap24b`. **Descended green in (b)**, repository leaked: `cap25b_sp7_strict_q6b_sigjudges_repo.out:1306`, `:1317`, with `SignerForged` red at `:3314`. **Each observer is shown live against its own negative control, so the greens are results and not an inert judge:** unbinding the inner signature from the presented bytes reds the **byte** observer (`cap25c_sp7_strict_q6b_sigjudges_bytes_control.out:2249` `is false`) while the signature-term observer stays green (`:1948`); leaking **both** channel keys — case **(c)**, where §1.1 gives the adversary an authorized wrapper key — reds the **signature-term** observer (`cap25d_sp7_strict_q6b_sigjudges_transplant_control.out:2505` `is false`) while the byte observer stays green (`:2517`); witnesses reachable in both controls (`cap25c:1727`, `:1936`; `cap25d:1982`, `:2194`). **So C-Q7 and C-Q8 come out of the round-ten “What remains PREDICTED GREEN” list for (a) and (b) and are DESCENDED GREEN there; every other member of that list stands unchanged**, and their stated bases — §1.1's compromised-channel-only enrolment for C-Q7, retained byte binding for C-Q8 — are now confirmed **by run** rather than by reasoning. **In (d) nothing moves:** C-Q7 stays **descended red** (`cap6b_sp7_q6b_sigjudge.out:1809`) and C-Q8 stays predicted. **No set (1), set (2) or set (3) membership, no query, no probability, no timebox and no companion count moves.** These four are **family-copy diagnostics and not capstone results**; no capstone model exists and nothing in the repository was run. **The label is withdrawn. The withdrawn text, quoted:** “**GREEN CONTROL in (a) and (b), DESCENDED** — Q6b's mutation transcribed onto the **correct strict** model with **both outer authority checks and the same-key wrapper signer retained** leaves **every query green and both witnesses reachable** in both channel variants (`cap14b_sp7_q1_strict_q6b.out:550`, `:559`, `:568`, `:843`, `:1047`; `cap14c_sp7_q1_strict_repo_q6b.out` identical line for line).” **What was wrong:** “every query green” was true of the **four** these copies declare and false of the capstone's set, and neither copy declares generic C-Q7, structural C-Q8 or C-Q9, nor any structural linkage judge. The reason is substantive: Q6b verifies the inner signature under the **authorized wrapper key**, and §1.1's compromised-channel-only enrolment gives the adversary no authorized wrapper key in strict, while same-key wrapping preserves the witness without producing reattribution. **This is a registered result, not a broken fixture.** **AND THE CONTROL IS NOW SHOWN TO BE A CONTROL AND NOT A DEAD MUTATION** *(REPAIR 2026-09-17, Codex round 6 finding 4)*: adding **only the second leak** to the same strict Q6b model — case **(c)**, where §1.1 gives the adversary an **authorized wrapper key** — **restores the attack**, `Rescoped` (`cap19b_sp7_strict_both_leaked_q6b.out:843`), `InnerSigTransplanted` (`:1151`) and `Reattributed` (`:1450`) all reachable, witnesses reachable (`:1728`, `:1935`), while the **correct** strict model with both leaks stays green on all four (`cap19a_sp7_strict_both_leaked_base.out:562`, `:576`, `:589`, `:603`; witnesses `:927`, `:1139`). So the green in (a)/(b) is the **absence of the authorized wrapper key** and nothing else — the mutation is live the moment that key exists. **(ii) Q5c, one level in:** red in **(d)**, **descended** (`sp7_q5c_companion_one_level_in.out:1131`, `:690`) — **Q5c ran degraded only**. In **(a)/(b)**: **red predicted IF the depth-2 honest route exists**, else a **green control**; S-P7's own Q5c row records the middle wrapper as **adversary-held `pk(k)`** and the depth-2 wrapped witness as reachable *“only through I1 wrapping its own attestation”* (`s-p7/RESULTS.md:52`), so which it is turns on whether the honest same-key route reaches depth 2 in the strict fixture. **Stated as an observation of the run, not predicted either way here.** **(iii) Q6a, identity from the outermost frame:** red in **(a)**, **(b)** and **(d)** — **descended in STRICT, IN CASE (a),** by `cap14d_sp7_q1_strict_q6a.out:892` (`Rescoped` reachable; trace `:880-892`, the **honest-only route**: the honest wrapper `skW2` wraps I2's honest attestation and the inner is attributed to `(pk(skI2), idW2)`), with `InnerSigTransplanted` (`:906`), `Reattributed` (`:920`) and `TypeConfused` (`:558`) green and the witnesses reachable (`:1185`, `:1394`); and **descended in DEGRADED** by the committed Q6a companion (`sp7_q6a_companion_identity_outermost.out:806`, goal `:516`, with `:503`, `:819` green and witnesses `:1118`, `:1314`). **CASE (b) IS NOW DESCENDED IN ITS OWN RIGHT** *(REPAIR 2026-09-17, Codex round 6 finding 5)*: `cap14d` leaks **`skD` only** and is therefore a run of **(a)**; the repository-compromised variant made for this repair — one line changed, `out(c, skR)` for `out(c, skD)` — gives the same result, `Rescoped` **red** (`cap14d_sp7_q1_strict_q6a_repo.out:893`) with `InnerSigTransplanted` (`:907`), `Reattributed` (`:921`) and `TypeConfused` (`:558`) green and the witnesses reachable (`:1186`, `:1395`). *The withdrawn label, quoted: “red in (a), (b) and (d) — descended in STRICT by `cap14d_sp7_q1_strict_q6a.out:892`”, which named one run for two cases.* **(c): not stated — (c) is C-C1's run** *(REPAIR 2026-09-17, Codex round 6 finding 4)*; *the withdrawn phrase, quoted: “(c) as (a)/(b)”* — (c) leaks **both** channel keys, which is the case that **restores** C-C15(i)'s attack (`cap19b…:843`), so it is not a configuration of (a)/(b) in either direction. **And the link-6b red this configuration carries is now one the query can see** *(REPAIR 2026-09-17, Codex round 6 finding 1)*: under the restated link 6b (§3) the comparison is against the **envelope path's own attribution report**, which is exactly what Q6a changes (`cap14d_sp7_q1_strict_q6a.pv:244`); under the withdrawn frame-field form a literal judge stayed **green on this very mutant** (`cap19d_sp7_strict_frame_judge_q6a.out:585`) while `Rescoped` was red (`:933`). **CONSEQUENCE FOR D11, STATED:** in strict the **identity half** of conjunct 3 and **link 6b** are severed by **(iii)**, the **key half** by nothing the strict fixture can present, so **D11's discharge in (a)/(b) rests on (iii)**; in (d) it rests on (i), (ii) and (iii) together. **STRICT OUTCOME IN THREE LISTS, CONFIGURATIONS (ii) AND (iii)** *(REPAIR 2026-09-17, Codex round 8 finding 2)*. **(ii) Q5c, one level in — (a)/(b) descended green: NONE; descended red: NONE.** `sp7_q5c_companion_one_level_in` ran **degraded only** and no strict run of this configuration exists. **Predicted:** link 6b at `L2` and C-Q4's `RescopedD2` red **if the depth-2 honest route exists in the strict fixture**, else green throughout — which this cell already states as an **observation of the run** and predicts neither way; set (2) green; the three witnesses reachable. **“Green control” here is a PREDICTED configuration-level reading and never a descended one.** **WHAT THE INNER ACCEPTANCE REPORTS UNDER (ii)** *(REPAIR 2026-09-17, Codex round 9 finding 1)*: Q5c takes the **attribution** from the middle layer and leaves every verification alone, so under §1.3's report contract the innermost `LayerAccepted` carries the **presented innermost** `(tI, ppfI, sgI, fbI)` under **`kI`** — the key that layer's verifier still verifies against, and the terms it still checks — while the **envelope path's `ScopeReported`** carries the middle layer's `(kM, idM)`. **No predicted outcome changes:** C-Q9, C-Q8 and links 3, 4 and 5 stay **predicted green** and none of those greens turns on the report choice, because at the innermost layer the reported terms and the checked terms are the same; what the mutation moves is the **attribution report**, which is what link 6b at `L2` and C-Q6's conjunct 3 observe. **This is the contrast with (i):** (i) changes the **key the inner signature is verified under** and stops checking the presented inner tuple and proof, which is why its C-Q9 is descended **red**; (ii) does neither. **(iii) Q6a, identity from the outermost frame — (a) descended red:** C-Q4's `Rescoped` (`cap14d_sp7_q1_strict_q6a.out:892`). **(a) descended green:** C-Q4's `InnerSigTransplanted` (`:906`), C-Q3 `Reattributed` (`:920`), `TypeConfused` (`:558`); witnesses `HonestWrappedAccepted` (`:1185`) and `HonestAccepted` (`:1394`) reachable. **(a) predicted:** **C-Q6's conjunct 3 red, with the isolation observer `ScopeIdentityOnly` reachable beside it** *(names registered 2026-09-17, skeptic read S-10; withdrawn wording, quoted: “C-Q6's conjunct 3, identity half, red”)* and **link 6b at `L1` red** — neither `ChainBroken` nor C-Q6 is declared in any model, and what is descended is their **relation**, at the reviewer's projection (`cap12e_ss_q1_join_scope_identity.out:945`) and through `Rescoped` above; **predicted green** — the isolation observer **`ScopeKeyOnly`** *(same marker; withdrawn wording, quoted: “conjunct 3's **key half**”)* (`cap12f_sp7_q6a_keyjudge.out:1339`; `cap12e…:570`), C-Q6's conjuncts 1 and 2 (`cap12e…:542`, `:556`, `:1368`, substitution excluded `:563`), link 6a, C-Q3, C-Q5, C-Q7, C-Q8, C-Q9, links 1a, 1b, 2a, 2b, 3, 4, 5, `Stripped`, `SignerForged`, `Spliced`, `VersionLied`. **(b): the same three lists, DESCENDED on the `_repo` variant** — `Rescoped` red (`cap14d_sp7_q1_strict_q6a_repo.out:893`), `InnerSigTransplanted` (`:907`), `Reattributed` (`:921`) and `TypeConfused` (`:558`) green, witnesses reachable (`:1186`, `:1395`) — with the undeclared members still **predicted**. **(d): descended by the committed Q6a companion** (`sp7_q6a_companion_identity_outermost.out:806`, with `:503`, `:819` green and witnesses `:1118`, `:1314`). **WHAT THE INNER ACCEPTANCE REPORTS UNDER (iii)** *(REPAIR 2026-09-17, Codex round 9 finding 1)*: Q6a verifies the inner signature under **`kI`** as the correct model does and **matches** the inner frame's `kfp`, changing only the **attributed issuer identity**, read as `idW` from the wrapper frame. Under §1.3's report contract the inner `LayerAccepted` therefore carries the **presented innermost** `(tI, ppfI, sgI, fbI)` under `kI` — the terms this verifier actually checks — while `ScopeReported` carries `(kX, idW)`. **No predicted outcome changes, and the predicted greens here do NOT depend on the report choice:** C-Q9 and link 3 stay **predicted green** because the reported terms are the checked ones, which is precisely what distinguishes (iii) from (i). **No configuration of C-C15 is called a green control at configuration level any more, in any case.** |

**Three notes the builder carries on these three.** (1) **C-C13 and
C-C15 are the pair the ledger forbids collapsing.** `:1542-1546`
forbids assigning link 6b's scope conjunct to D8's type producer;
C-C13's set (2) requires `Rescoped` and link 6b green, and C-C15's set
(2) requires `TypeConfused` and link 6a green. If either pair fails
together, that is the round-4 finding-2 separation not reproducing under
composition, an observation to diagnose and record (`:1459-1480`), never
a repair of this file. (2) **C-C4 and C-C15 overlap at link 6b**, as
C-C3 and C-C8 overlap at C-Q5 and C-Q9: C-C4 is D2's key-binding
severing, which reds 6b as one of its five, and C-C15 is D11's scope
severing. They stay two registered mutations for two obligations, and
`:1518-1520` is explicit that **Q6b is not a companion for D2 or D5**.
Whether their capstone sets coincide at 6b is an observation of the run.
(3) **C-C14 is the only companion in this file whose sets (2) and (3)
descend from no `.out` at all.** Its prediction is correspondingly the
weakest-supported of the **seventeen** *(REPAIR 2026-09-17, Codex round
5 finding 1; “sixteen” superseded by §9(4))*, and it inherits C-Q2's own residual
(§3, p ≈ 0.65, the two-worlds judge being *"the query the spike itself
found most sensitive to fixture shape"*).

### (2) C-C8's two isolation configurations, registered

The skeptic recorded (edit 17) that **C-C8 has no single-removal
isolation run anywhere on the record**, unlike C-C2 (`m1_framepin.out:399`,
`LEDGER.md:1495`), C-C3 (the C1/C3 configurations, `:1496`) and C-C4
(`s3_innerfp.out`, `:1497`), so its *"both together"* minimality is
asserted. `:1501` states no isolation for it. The two runs that would
show it are registered here, in the form C-C2/C-C3/C-C4 use.
*[The 2026-09-15 draft added here: "**They are registered, not run: no
run was made for this file, and no result below is claimed.**"
**Superseded 2026-09-16**: both configurations have now been run on
**copies of a committed family model**, `cap2_sp2_poss_fponly` and
`cap3_sp2_mh_guards_dropped` under
`formal/suite/ledger-tests-2026-09-14/`, and their `.out` lines are
cited in the table below. **They remain scratch runs on a family copy,
not capstone results**: no capstone model exists, none was built, and
what they establish is the shape of the obligation, not its
discharge.]*

| Config | Removal, in the capstone's terms | Retained | Required outcome | Nearest thing on the record — and why it does not settle it | Cases |
|---|---|---|---|---|---|
| **C-C8-i** *(REPLACED 2026-09-16, Codex finding 2; this label formerly carried the possession-only removal, which is now C-C8-ii)* | **The frames' manifest-hash guards alone**: `if mh = h(t)` dropped from every frame check, on both the one- and the two-signer branch | **Everything else**, in particular **possession over the accepted manifest under the accepting key**, `checksign(ppf, kX) = (POSS, t)`, in full; the seven-field frames; the per-slot `=fp(kX)` pins; the tuple fingerprint matches; the three §A5.4 content guards | **C-Q9 green** (`PossessionUnbound` unreachable) **and** C-Q5 `SetAltered` green, with **both `HonestComplete` branches and `HonestAccepted` reachable**; C-Q3, `Stripped`, `SignerForged`, `Spliced` green | **SHOWN, on a copy, 2026-09-16** — `ledger-tests-2026-09-14/cap3_sp2_mh_guards_dropped.pv/.out`, a copy of `d10a_sp2_q9_base.pv` with the `mh = h(t)` guards and nothing else removed: **C-Q9 `is true`** (`:1115`), **`SetAltered` `is true`** (`:468`), `Stripped` (`:452`), `SignerForged` (`:460`), `Reattributed` (`:476`), `Spliced` (`:1099`), `PossessionTransplanted` (`:1107`) all `is true`, witnesses reachable (`:642`, `:861`, `:1091`). S-P2's Q5-**C3** configuration has the same shape family-locally and leaves `SetAltered` green (`sp2_q5_c3_manifestposs_frame_nomh.out:363`, with `:349`, `:356`, `:370` and witnesses `:534`, `:753`, `:983`) but **declares no `PossessionUnbound` query**, which is why the run above was made | **(d) descended** (`cap3_sp2_mh_guards_dropped`, a copy of the S-P2 degraded model); **(a)/(b): PREDICTED**, carrying C-C8's strict split *(REPAIR 2026-09-17, Codex round 6 finding 2)* — on the strict run of the **combined** removal, `SetAltered` is **green** (`cap18c_sp2_strict_cc8.out:509`), so this single removal's registered **green on C-Q5 and on C-Q9** is predicted to hold in strict a fortiori; **no strict run of this isolation configuration exists**, so neither (a) nor (b) is descended. **(c): not stated — (c) is C-C1's run** *(REPAIR 2026-09-17, Codex round 6 finding 4)*. *The withdrawn text, quoted: “(a)/(b)/(c) predicted, the same reading as C-C8's row — zero `dsks` steps, honestly evidenced tuple, no green-control reading.”* The reading it referred to was a **degraded-trace reading** and has been withdrawn from C-C8's row. This configuration's required outcome is **green on C-Q9**, which is not a green control but the isolation result itself **STRICT OUTCOME IN THREE LISTS** *(REPAIR 2026-09-17, Codex round 8 finding 2)*. **(a)/(b) descended green: NONE. Descended red: NONE** — `cap3_sp2_mh_guards_dropped` is a copy of the **degraded** S-P2 model and **no strict run of this isolation configuration exists**. **Predicted green:** C-Q9 `PossessionUnbound` and C-Q5 `SetAltered`, basis C-C8's own strict split (`cap18c_sp2_strict_cc8.out:509` green, so this single removal's green holds a fortiori), with C-Q3, `Stripped`, `SignerForged`, `Spliced` green and all three witnesses reachable. **Predicted red: NONE.** **The all-green required outcome here is the ISOLATION RESULT, not a green control**, and in strict it is **predicted**, never descended. **DATED NOTE, 2026-09-17** *(REPAIR 2026-09-17, Codex round 9 finding 2)*: this configuration is the **manifest-hash-only** removal, so C-C8's new strict runs bear on it directly and **strengthen its predicted green without descending it**. On the **combined** removal in strict a judge firing on `mh ≠ h(t)` is **green** in both channel variants (`cap22h_sp2_strict_cc8_mh.out:1478`; `cap22i_sp2_strict_cc8_mh_repo.out:1477`) and **red** on the degraded source (`cap22j_sp2_degraded_cc8_mh.out:1665`), so **link 5's `mh` half is predicted green here in (a) and (b) a fortiori** — the honest channel's tuple pin keeps `mh = h(t)` in strict even with the guards dropped — while it stays the registered **(d)** red. **Still no strict run of this isolation configuration exists**, and neither (a) nor (b) is descended; **C-C8-ii is unaffected**, its mutation touching the possession binding and not the frame guards. |
| **C-C8-ii** *(KEPT as the second single removal; its required outcome is corrected, its mutation is the one C-C8-i formerly carried)* | **The possession binding alone**: possession made fingerprint-only, `let (=POSS, =fp(kX)) = checksign(ppfX, kX)` — the library's D-3 under-encoding, a broken companion by library definition (`:1501`) | **Everything else**, in particular the frames' `mh = h(t)` guards, the seven-field frames, the per-slot `=fp(kX)` pins, the tuple fingerprint matches and the three §A5.4 content guards | **C-Q5 `SetAltered` green** — this is the set-integrity isolation, obligation (α) — with `Stripped`, `SignerForged`, C-Q3, `Spliced` green and **both `HonestComplete` branches and `HonestAccepted` reachable**. **C-Q9 is registered RED here**, obligation (β): the exact possession-message relation is falsified by possession unbinding alone, so its red is a **registered expectation, not a broken fixture** | **SHOWN, on a copy, 2026-09-16** — `ledger-tests-2026-09-14/cap2_sp2_poss_fponly.pv/.out`: **C-Q9 `is false`** (`:1263`) with **`SetAltered` `is true`** (`:471`), `Stripped` (`:457`), `SignerForged` (`:464`), `Reattributed` (`:478`), `Spliced` (`:1097`), `PossessionTransplanted` (`:1104`) `is true` and witnesses reachable (`:643`, `:861`, `:1090`); baseline `d10a_sp2_q9_base.out:1111`. S-P2's Q5-**C1** configuration has the same shape family-locally (`sp2_q5_c1_fponly_frame_mh.out:366`, with `:354`, `:360`, `:372` and witnesses `:536`, `:756`, `:987`) and likewise declares no `PossessionUnbound` query | **(d) descended** (`cap2_sp2_poss_fponly`, same provenance); **(a)/(b): PREDICTED**, carrying C-C8's strict split *(REPAIR 2026-09-17, Codex round 6 finding 2)* — C-Q9 **red**, `SetAltered` **green**, which is exactly what the strict run of the combined removal shows (`cap18c…:1431` red, `:509` green); **no strict run of this isolation configuration exists**, so neither case is descended. **(c): not stated — (c) is C-C1's run** *(REPAIR 2026-09-17, Codex round 6 finding 4)*. *The withdrawn text, quoted: “(a)/(b)/(c) predicted, same reading, no green-control reading.”* Its **C-Q9 red is registered in every case it is run in**, being falsified **by construction** rather than by any adversary capability — which is the one basis in this cell that a mode change cannot touch **STRICT OUTCOME IN THREE LISTS** *(REPAIR 2026-09-17, Codex round 8 finding 2)*. **(a)/(b) descended green: NONE. Descended red: NONE** — `cap2_sp2_poss_fponly` is a copy of the **degraded** S-P2 model and **no strict run of this isolation configuration exists**. **Predicted red:** C-Q9, falsified **by construction** rather than by any adversary capability, which is the one basis in this cell a mode change cannot touch, and which C-C8's strict run exhibits at `cap18c…:1431`. **Predicted green:** C-Q5 `SetAltered` (`cap18c…:509`), C-Q3, `Stripped`, `SignerForged`, `Spliced`, `PossessionTransplanted`, with all three witnesses reachable. **No green control, descended or predicted.** |

**The two obligations, stated apart** *(REPAIRED 2026-09-16, Codex
finding 2; the draft ran them together and required both isolation
configurations to keep C-Q9 green, which is impossible for the
possession-only removal).*

- **(α) Set integrity — `SetAltered` (C-Q5), and `SetAltered` needs the
  combined removal.** Either protection alone leaves it green: the
  manifest-hash guards alone (`cap3…out:468`), the possession binding
  alone (`cap2…out:471`), family-locally `sp2_q5_c1…:366` and
  `sp2_q5_c3…:363`. **C-C8 is a minimal two-removal severing of this
  obligation, and that is now shown rather than asserted.**
- **(β) The exact possession-message relation — C-Q9,
  `checksign(ppf, kX) = (POSS, t)`.** C-Q9 demands that the accepted
  possession proof recover `(POSS, t)` for the accepted `t`. A
  fingerprint-only proof recovers `(POSS, fp(kX))`, and **no retained
  frame guard can change the message a signature recovers to**, so the
  possession removal alone falsifies C-Q9 **by construction**:
  `cap2_sp2_poss_fponly.out:1263` `is false` against the baseline
  `d10a_sp2_q9_base.out:1111` `is true`, with `SetAltered` and every
  other retained query green and all three witnesses reachable.
  **C-C8's red on C-Q9 is therefore over-determined**, and the minimal
  severing of (β) is **C-C8-ii, the possession unbinding alone**.

**Withdrawn: the mandatory post-freeze amendment.** The draft's
sentence *"If either single removal already reds C-Q9… the companion is
re-specified **by amendment** … before its result stands"* is
**withdrawn as unnecessary**. It prescribed a post-freeze amendment for
a contradiction that is now established **before** the freeze, in this
file, on the record: the re-specification is the repair above, and no
amendment is owed for it. What remains binding is the run discipline —
**both configurations are run before C-C8's reds are counted and their
outcomes are recorded in `RESULTS.md` whichever way they fall** — and
the ordinary amendment rule of §8 freeze statement (3), which applies
to any *other* divergence, exactly as it applies to every prediction in
this file. The C-C3/C-C8 overlap note in §4 is decided by C-C8-i and
C-C8-ii's outcomes on evidence rather than left open.

**What this subsection does not change.** C-C8's mutation, its three
sets, its row (D10) and its predicted reds are exactly as §4 registers
them; the isolation configurations are two additional runs, not a
fourth and fifth companion, and they carry no timebox of their own —
they run inside C-Q9's 60-minute box (§3), as C-C3's do inside C-Q5's.

### (3) C-C16 — D7's common-content severing companion, registered 2026-09-16

*Registered under Codex finding 1
(`docs/reviews/2026-09-16-codex-review-capstone-predictions.md`), which
found that D7 named `Spliced` among its producers and listed only links
2a/2b as consumers and C-C9 as companion. Those links establish
**membership** and **completeness**; neither says anything about
**agreement between the signers' content**. The consumer of the
common-content fact is **link 5's content conjunct**, and A3.3 requires
a companion that fails **the query consuming the severed link**
(`docs/phase-0-prereg-amendment-3.md:220-230`). C-C16 is that companion.
It is the sixteenth, and the second this file numbers beyond the
ledger's ten; like C-C11–C-C15 its capstone-only members are marked
**not descended**.*

| # | Mutation, in the capstone's terms | (1) Expected failed set, in capstone query names | (2) Must stay green | (3) Witnesses that must stay reachable | Row | Descends from | Cases |
|---|---|---|---|---|---|---|---|
| **C-C16** | **The spliced-payload severing**: in the `\|set\| = 2` branch of the capstone's **check 4**, the three §A5.4 cross-slot content equalities `ota = otb`, `cva = cvb`, `pla = plb` are dropped, so **one signer slot may carry different content from the other** — a different payload, object type or canonicalization version — while both slots are otherwise fully checked. **Everything else retained**: the per-slot `=fp(kX)` pins, the `=alg` / `=id` fields pinned through `t`, the frames' `mh = h(t)` guards, the required-set reads on **both** branches, possession over the accepted manifest, and every signature check. *(This is the capstone-side restatement of S-P2's own Q6-C companion.)* **Mechanism-review contrast (`formal/spike/floor-structure/PROBE.md:46`):** the narrower alternative — dropping **`pla = plb` alone**, the literal "spliced payload" — is the simplest plausible mutation; **whether one equality alone suffices to red link 5's content conjunct is an observation for the run, not asserted here**, and no run on the record settles it. The three-equality removal is what the 2026-09-16 scratch run exercises and is what this companion registers | **C-Q1 link 5's common-content conjunct** — `ChainBroken(lyr, LINK_5)` reachable — **not descended** (`ChainBroken` is declared in no model), **and** the retained query **`Spliced`**, which **is** descended: `ledger-tests-2026-09-14/cap1_sp2_content_unchecked.out:1337` `is false` against the baseline `cq1c_sp2_slots_base.out:1133` `is true`, and family-locally S-P2 Q6-C (`.out:1213`, `LEDGER.md` D7 row). Both modes, all four cases. **Note on link 5's two halves:** link 5 is one query with a frame-to-key half and a content half; C-C16 severs **only** the content half, and if link 5's registered residual is taken (§3, *"most likely splitting the conjunct into a frame-to-key query and a cross-slot query"*) the red resolves onto the cross-slot query alone. Which half fails is recorded; that the query fails is the obligation | **The whole point — links 2a and 2b stay green**, which is what shows they cannot carry D7's common-content fact. **Descended:** all three link-2b completeness conjuncts `is true` (`cap1…out:1366`, `:1381`, `:1396`), `Stripped` (`:465`), `SignerForged` (`:472`), C-Q5 `SetAltered` (`:479`), C-Q3 `Reattributed` (`:486`), `PossessionTransplanted` (`:1344`) and **C-Q9** (`:1351`). **Not descended, predicted:** links 1a, 1b, 3, 4, 6a, 6b, and link 5's **frame-to-key** half; C-Q2, C-Q4, C-Q7, C-Q8; `TypeConfused`, `VersionLied`. **Set-completeness note:** the diagnostic model declares no `TypeConfused` and no `VersionLied`; the capstone's transcription carries both and **must add them to this set**, on the pattern used for C-C13 and C-C15 | both `HonestComplete` branches (`cap1…out:657`, `:886`) and `HonestAccepted` (`:1126`), **descended**; **not descended:** `HonestChain` at `L0`, `L1`, `L2` | **D7** (`LEDGER.md:701`) — the **common-content** half, which C-C9 does not touch | S-P2 Q6 `Spliced` producer green (`base_sp2.out:1013`); S-P2's own Q6-C companion red (`.out:1213`); and the 2026-09-16 scratch run `cap1_sp2_content_unchecked.pv/.out` on a copy of `cq1c_sp2_slots_base.pv` | **(d) red, descended** — `cap1_sp2_content_unchecked` is a copy of the S-P2 **degraded** slots diagnostic (`…out:1337`). **(a): red, DESCENDED** *(REPAIR 2026-09-17, Codex round 6 finding 2)* — the same mutation made strict (the second, uncompromised authority process and check added, DNS leaked) reds **`Spliced`** (`cap18d_sp2_strict_cc16.out:1430`) while **link 2b's three completeness conjuncts stay green** (`:1456`, `:1468`, `:1480`) and the rest stay green (`:497`, `:504`, `:511`, `:518`, `:1437`, `:1444`), witnesses reachable (`:701`, `:942`, `:1194`). **The strict red therefore STANDS, by a route other than `cap1`'s displayed trace. (b): red, PREDICTED** — channel symmetry, never a second run. **(c): not stated — (c) is C-C1's run** *(REPAIR 2026-09-17, Codex round 6 finding 4)*. **THE BASIS IS CORRECTED, THE PREDICTION IS NOT WITHDRAWN** *(REPAIR 2026-09-17, Codex round 6 finding 2)*. *The withdrawn basis, quoted: “(a), (b), (c): red predicted — the row states this companion for all four cases. No green-control reading is named: the trace behind `cap1…out:1337` takes zero `dsks` steps and the accepted tuple is the honestly evidenced manifest, the content disagreement entering through a frame rather than through enrolment.”* **That account of the trace is false**: `cap1_sp2_content_unchecked.out:1319-1337` displays an attack over an **attacker-authored tuple**, not an honestly evidenced manifest. The conclusion it was offered for survives; the reason it was offered does not **STRICT OUTCOME IN THREE LISTS** *(REPAIR 2026-09-17, Codex round 8 finding 2)*. **(a) descended red:** `Spliced` (`cap18d_sp2_strict_cc16.out:1430`). **(a) descended green:** link 2b's three completeness conjuncts (`:1456`, `:1468`, `:1480`), `Stripped` (`:497`), `SignerForged` (`:504`), C-Q5 `SetAltered` (`:511`), C-Q3 `Reattributed` (`:518`), `PossessionTransplanted` (`:1437`) and C-Q9 (`:1444`); witnesses both `HonestComplete` (`:701`, `:942`) and `HonestAccepted` (`:1194`). **(a) predicted:** **link 5's common-content conjunct red**, `ChainBroken` declared in no model and its relation descended by `Spliced`; **predicted green** — links 1a, 1b, 2a, 3, 4, 6a, 6b and link 5's **frame-to-key** half, C-Q2, C-Q4, C-Q7, C-Q8, `TypeConfused`, `VersionLied`, and the `HonestChain` witnesses at `L0`, `L1`, `L2`. **(b): the same three lists, every entry PREDICTED** — basis channel symmetry, never a second run. **No green control in any case.** |

**Why this companion had to be registered, shown rather than argued.**
The run `cap1_sp2_content_unchecked` removes the three content
equalities **and nothing else** from a copy of the link-2b completeness
diagnostic. The result is the exact separation the review claimed:
**`Spliced` becomes reachable** (`:1337` `is false`) **while all three
completeness correspondences stay `is true`** (`:1366`, `:1381`,
`:1396`) and every other retained query — `Stripped` (`:465`),
`SignerForged` (`:472`), `SetAltered` (`:479`), `Reattributed` (`:486`),
`PossessionTransplanted` (`:1344`), C-Q9 (`:1351`) — stays green with
both `HonestComplete` witnesses (`:657`, `:886`) and `HonestAccepted`
(`:1126`) reachable. **Links 2a and 2b cannot carry D7's common-content
fact**, and a red on link 5's key-binding half cannot substitute for
C-C16's obligation. This reproduces the reviewer's `/tmp` diagnostic on
our own tree.

---

### (4) C-C17 — D7's membership severing companion, registered 2026-09-17

*Registered under Codex round 5 finding 1
(`docs/reviews/2026-09-17-codex-review-capstone-predictions-round5.md`),
which found that D7 claims discharge of **three** producers — `Stripped`,
`SignerForged` and `Spliced` — while its two companions sever
**completeness** (C-C9) and **common content** (C-C16) and **both retain
link 2a and `SignerForged`**. The fact link 2a consumes is **membership**:
that the signed tuple's required set names the slot and `fp(kX) = kfpr`
for it. Nothing in this file severed it, so under A3.3 the query
consuming the severed link had no companion failing it
(`docs/phase-0-prereg-amendment-3.md:220-230`). C-C17 is that companion.
It is the **seventeenth**, and the third this file numbers beyond the
ledger's ten; like C-C11–C-C16 its capstone-only members are marked
**not descended**. **It adds no timeboxed entry** — it runs inside link
2a's 45-minute box (§3), as C-C16 runs inside link 5's — and it changes
no query, no probability, no residual decomposition and no timebox.*

**The projection the descent is taken at, and the reviewer's correction
of it** *(REPAIR 2026-09-17, Codex round 5 finding 1)*. The diagnostic is the link-2b completeness model
with **the slot report naming the MANIFEST-NAMED slot** — `kfprA` /
`kfprB` — which is what §1.3's `LayerAccepted` contract requires
(*“`slot` the signer-slot identifier, `kfpr` as the signed set names
it”*), where `cq1c_sp2_slots_base` reported **`fp(kA)`**. The reviewer
corrected the projection before running it, and the correction is
recorded here because the two projections are **not the same relation**:
a report that names `fp(kX)` cannot disagree with the accepting key **by
construction**, so a structural slot-to-key judge is **unsatisfiable at
`cq1c`'s projection and live at §1.3's**. At §1.3's projection the
matched baseline is all green, the judge included
(`cap13a_sp2_membership_base.out:1206` `is true`, with the four S-P2
queries `:481`–`:502`, `Spliced` `:1143`, `PossessionTransplanted`
`:1150`, C-Q9 `:1157` and the three link-2b conjuncts `:1171`, `:1185`,
`:1199` all `is true` and the witnesses reachable at `:673`, `:899`,
`:1136`).

| # | Mutation, in the capstone's terms | (1) Expected failed set, in capstone query names | (2) Must stay green | (3) Witnesses that must stay reachable | Row | Descends from | Cases |
|---|---|---|---|---|---|---|---|
| **C-C17** | **S-P2 Q4 transcribed — slot B's key-fingerprint equality removed.** In the `\|set\| = 2` branch of the capstone's **check 3**, `fp(kB) = kfprB` is dropped for **slot B only**, so a key the signed set does not name satisfies that slot. **Everything else retained**: slot A's equality, the required-set reads on **both** branches, every signature check, possession over the accepted manifest under the accepting key, the seven-field frames, the frames' `mh = h(t)` guards, the tuple fingerprint matches and the three §A5.4 content guards. *(The family source is `s-p2/proverif/sp2_q4_companion_slot_unbound.pv`, whose row is `s-p2/RESULTS.md:46` — *“red on exactly `SignerForged`”*.)* **Mechanism-review contrast (`formal/spike/floor-structure/PROBE.md:46`):** the nearest alternative is dropping the **required-set read** instead of the slot equality — which is **C-C9's** mutation and severs **completeness**, not membership. The two are registered apart for that reason, and the run shows they do not collapse: under C-C17's removal all three completeness conjuncts stay `is true` while the slot-to-key judge reds | **C-Q1 link 2a** — `ChainBroken(lyr, LINK_2A)` reachable — **not descended** (`ChainBroken` is declared in no model), but its **shape IS descended**, by the structural slot-to-key judge added at §1.3's projection: **`is false`** under the mutation (`cap13b_sp2_membership_unbound.out:1972`) against **`is true`** in the matched baseline (`cap13a_sp2_membership_base.out:1206`). **And the retained query `SignerForged`, descended:** `is false` (`cap13b…:730`); family-locally `sp2_q4_companion_slot_unbound.out:601` `is false` with its trace at `:360-601` (`k` adversary-held, its own key over its own frame, **no `dsks` step**), recorded at `s-p2/RESULTS.md:46`. **AND A RECORDED CONSEQUENCE, NEVER AN ASSUMED RETENTION: `PossessionTransplanted` becomes reachable** (`cap13b…:1657` `is false`) — the unbound slot accepts a possession proof under a key the slot does not name. **The family's Q4 row does not record it, and the reason is stated so the omission is not read as a divergence: S-P2's Q4 model declares NO `PossJudge` at all**, so the family run could not have seen it; the capstone's transcription carries one, and the consequence is therefore registered **here, before the freeze**, rather than met as a red outside the set. It is a **consequence of the membership severing, not a second severing of D10** — **C-C3 and C-C8 remain D10's companions** — on the pattern C-C15's row already uses for C-Q4's `InnerSigTransplanted` | **The whole point — link 2b's three completeness conjuncts stay green**, which is what shows C-C9 cannot carry D7's membership fact: **descended**, all three `is true` (`cap13b…:1685`, `:1722`, `:1759`). Also **descended green**: `Stripped` (`:481`), `Spliced` (`:1398`), **C-Q5** `SetAltered` (`:739`), **C-Q3** `Reattributed` (`:749`) and **C-Q9** `PossessionUnbound` (`:1666`). **Not descended, predicted:** links **1a**, **1b**, **3**, **4**, **5**, **6a**, **6b**; **C-Q2**, **C-Q7**, **C-Q8**. **Set-completeness note:** the diagnostic declares no `TypeConfused` and no `VersionLied`; the capstone's transcription carries both and **must add them to this set**, on the pattern used for C-C13, C-C15 and C-C16. **And the note the round-five finding forces:** `PossessionTransplanted` is **NOT** in this set — it is in set (1), as the run requires | Both **`HonestComplete`** branches, **descended** (`cap13b…:922`, `:1150`), and **`HonestAccepted`**, **descended** (`:1389`). **Not descended:** **`HonestChain(L0, t)`**, which no S-P2 model declares and which `:1420-1421` makes a fixture condition of the capstone run | **D7** (`LEDGER.md:701`) — the **membership** half, which **neither C-C9 nor C-C16 touches**; consumer **C-Q1 link 2a** | S-P2 Q2 `SignerForged` producer green (`base_sp2.out:384`; committed `sp2_q2_degraded_compromised.out:384`); S-P2's own **Q4 companion** red (`sp2_q4_companion_slot_unbound.out:601`, trace `:360-601`; `s-p2/RESULTS.md:46`); and the 2026-09-17 scratch runs `cap13a_sp2_membership_base.pv/.out` and `cap13b_sp2_membership_unbound.pv/.out`, copies of `cq1c_sp2_slots_base.pv` with the **manifest-named** slot report of §1.3 and a structural slot-to-key judge added (ninth batch of `formal/suite/ledger-tests-2026-09-14/README.md`) | **(d)** red, **descended** — `cap13b` is a copy of the S-P2 **degraded, sole-channel** slots diagnostic. **(a): red, DESCENDED** *(REPAIR 2026-09-17, Codex round 6 finding 2)* — the same mutation made strict the same way reds exactly what this row registers: **`SignerForged`** (`cap18e_sp2_strict_cc17.out:775`), **`PossessionTransplanted`** (`:1754`) and the **structural slot-to-key judge** — link 2a's shape — (`:2086`), while **link 2b's three completeness conjuncts stay green** (`:1781`, `:1813`, `:1845`) with `Stripped` (`:513`), `SetAltered` (`:785`), `Reattributed` (`:795`), `Spliced` (`:1483`) and C-Q9 (`:1764`) green and the witnesses reachable (`:981`, `:1222`, `:1474`). **The (α)-style separation this companion exists for therefore holds in strict as in degraded. (b): red, PREDICTED** — channel symmetry, never a second run. **(c): not stated — (c) is C-C1's run** *(REPAIR 2026-09-17, Codex round 6 finding 4)*. *The withdrawn text, quoted: “(a), (b), (c): red predicted. No green-control reading is named, and the reason is checked rather than assumed: the trace behind `cap13b…:730` takes zero `dsks` steps, and the accepted tuple is the honestly evidenced manifest `M2` — the adversary's key enters through the unbound slot, not through enrolment, so §1.1's compromised-channel-only rule removes nothing this mutation needs.”* The conclusion is now **run** rather than read off a degraded trace **STRICT OUTCOME IN THREE LISTS** *(REPAIR 2026-09-17, Codex round 8 finding 2)*. **(a) descended red:** `SignerForged` (`cap18e_sp2_strict_cc17.out:775`), `PossessionTransplanted` (`:1754`) and the **structural slot-to-key judge** — link 2a's shape — (`:2086`). **(a) descended green:** link 2b's three completeness conjuncts (`:1781`, `:1813`, `:1845`), `Stripped` (`:513`), C-Q5 `SetAltered` (`:785`), C-Q3 `Reattributed` (`:795`), `Spliced` (`:1483`) and C-Q9 (`:1764`); witnesses both `HonestComplete` (`:981`, `:1222`) and `HonestAccepted` (`:1474`). **(a) predicted:** **link 2a's `ChainBroken` red**, declared in no model, its relation descended by the judge above; **predicted green** — links 1a, 1b, 3, 4, 5, 6a, 6b, C-Q2, C-Q7, C-Q8, `TypeConfused`, `VersionLied`, and `HonestChain(L0, t)`. **(b): the same three lists, every entry PREDICTED** — basis channel symmetry, never a second run. **No green control in any case.** |

**Why this companion had to be registered, shown rather than argued.**
The run `cap13b_sp2_membership_unbound` removes **only** slot B's
`fp(kB) = kfprB` from the corrected baseline and changes nothing else.
The result is the exact separation the finding claimed: the
**slot-to-key judge goes `is false`** (`:1972`) and **`SignerForged`
becomes reachable** (`:730`) **while all three completeness
correspondences stay `is true`** (`:1685`, `:1722`, `:1759`) and
`Stripped` (`:481`), `SetAltered` (`:739`), `Reattributed` (`:749`),
`Spliced` (`:1398`) and C-Q9 (`:1666`) stay green, with both
`HonestComplete` witnesses (`:922`, `:1150`) and `HonestAccepted`
(`:1389`) reachable. **Completeness and common-content companions cannot
establish the missing severing A3.3 requires**, and the reds of C-C9 and
C-C16 cannot substitute for C-C17's obligation. The one thing the run
adds beyond the finding is the consequence set (1) now carries:
`PossessionTransplanted` reachable at `:1657`, which the family's Q4
model could not have recorded.

---

---

### (5) C-C18 — the D-6 tag-severing companion, registered 2026-09-18 under the author's ruling on the `REFUSAL` fork

*Registered by the AMENDMENT of 2026-09-18 (§8 item 1, option (i),
scoped). It is the **eighteenth**: the eighth beyond the ledger's ten
numbered companions and, after C-C16 and C-C17, the third that no
ledger line names at all *(the ordinal corrected — Codex round 16
finding 5; the draft said “fourth”)*; unlike C-C11–C-C17 it severs **no
matrix row**: it severs the composed D-6 property of §2 rule 6, the tag
separation `LEDGER.md:387-398` records as *“load-bearing under
composition”* on the strength of one unregistered scratch run. **Its
consuming query is C-Q6's standing conjunct**, and it is the only
companion in this file whose red is descended in **both** modes from
copies of the models **as committed today** (with the 2026-09-12 tuple
pin and alias judge), not from a 2026-09-06 snapshot. **It adds no
timeboxed entry of its own** — it runs inside C-Q10's 30-minute box
(§3) — and it changes no other query, no probability, no residual
decomposition and no timebox.*

**The projection the descent is taken at** *(skeptic read 2026-09-18,
S-14, on §9(4)'s pattern)*. The six runs are S-STANDING family copies,
and the row below is written in the capstone's names: the family's
honest issuer keys **`skH1` and `skH2` are the capstone's `skI` and
`skI2`** (§1.1), so `cap27d…out:824` reads `Established(pk(skH1[]), …)
… is false` and is cited here as the `skI` form, and `:834` reads
`pk(skH2[])` and is cited as the `skI2` form; the family's `Established
⟹ Designated` is C-Q6's standing conjunct at the family's projection.
**The descent is taken on the family's standalone standing path**, in
which the tag report is emitted immediately after the signature parse
and before the anchor-proof and tuple-pin checks; **the capstone's
standing path is C-Q6's composition join**, and the red is **predicted
at the join** on the same route, exactly as C-C11 and C-C12's are. That
is the larger projection C-Q10's residual names, and it is why C-Q10
carries 0.10 recut rather than less.

| # | Mutation, in the capstone's terms | (1) Expected failed set, in capstone query names | (2) Must stay green | (3) Witnesses that must stay reachable | Row | Descends from | Cases |
|---|---|---|---|---|---|---|---|
| **C-C18** | **The `TLR` tag check unbound.** In the capstone's **check 7** (the standing path), `let (=TLR, (lin, terminal, declT)) = checksign(tlrSig, kT)` becomes `let (uncheckedTag, (lin, terminal, declT)) = checksign(tlrSig, kT)`, so a signature under **any** tag over a TLR-shaped body verifies as the issuer's lineage record; the parsed tag is still reported to C-Q10's judge. **Everything else retained**: the entitled-key comparison `fp(kT) = kfpr`, `kT = kX`, the anchor-proof binding, the tuple pin, the lineage lookup, the terminal predicate, and every envelope-path check. **Mechanism-review contrast (`formal/spike/floor-structure/PROBE.md:46`):** the simplest alternative — removing the foreign-tag **signer** rather than the check — is not a companion at all: with no honest signer emitting another tag the check is inert and its removal changes no colour (the family's single-removal matrix, row 14, `s-standing/proverif/falsification-2026-09-06/scratch/dependency-index.txt`), which is exactly why the signer is in the fixture. The signer is honest; **no compromise is needed for the red** | **C-Q10** — `TagConfused` reachable, **descended** in strict (`cap27d_ss_q1_strict_foreign_tag_tlr_tag_unbound.out:2471`) and degraded (`cap27f_ss_q1d_degraded_foreign_tag_tlr_tag_unbound.out:2135`); **and C-Q6's standing conjunct, the honest-key form for `skI`** — descended: `Established(pk(skI), t, aid) ⟹ Designated(pk(skI), aid)` **`is false`** (`cap27d…out:824`; `cap27f…out:807`; the reviewer's own fixture `cap27b…out:734`), the trace being the `REFUSAL` signature over the adversary's TLR-shaped body accepted as the lineage record and `ESTABLISHED` reported for a core `skI`'s holder never designated; **and the unrestricted strict form** `is false` (`cap27d…out:670`) — in (d) the unrestricted form is not asserted (`:1371`, A4.6) and is red on the baseline already (`cap27e…out:666` against `ss_q1d_degraded_compromised.out:640`, the registered degraded cost, not this companion's red). **Not descended, predicted:** `ChainBroken` at **no** link — the envelope path is untouched | **C-Q6's entitled-key conjunct** — `StandingUnentitled` unreachable, descended (`cap27d…out:841`, `cap27f…out:822`); **the honest-key form for `skI2`** `is true` (`:834`, `:816`) — the foreign signer holds `skI` only; **SS.Q6 `Aliased`** unreachable (`:2323`, `:1979`); `ReasonCollapsed` unreachable (`:2316`, `:1973`). **Not descended, predicted green, each in the cases it is stated for** *(case-qualified — Codex round 16 finding 2, the round-13 link-1b rule)*: every envelope-path query — C-Q1 links 1a, 2a, 2b, 3, 4, 5, 6a, 6b in (a), (b), (d) and **link 1b in (a) and (b) only** (C-Q1-degraded does not assert it, `:314-318`, and it is red on the unmutated degraded baseline, `cap26a`); C-Q2 in (a) and (b) only; the strict `Accept ⟹ IssuerSigned` in (a) and (b) only, with the unrestricted `AcceptS ⟹ IssuerSigned` **registered red in (d)** already (A4.6); C-Q3, C-Q4, C-Q5, C-Q5w, C-Q7, C-Q8, C-Q9 and the remaining retained queries in every case — because the mutation touches the standing path only; and C-Q6's conjuncts 2 and 3, for the same reason | `HonestStandingEstablished` reachable, descended (`cap27d…out:1140`, `cap27f…out:1108`), and the five vocabulary witnesses (`cap27d…out:1426`–`:2309`; `cap27f…out:1303`–`:1967`); **not descended:** `HonestChain` at `L0`, `L1`, `L2`, and `HonestAccepted` | **none** — the composed D-6 property, `LEDGER.md:387-398`, §2 rule 6 | the 2026-09-06 reviewer fixtures `a_foreign_tag.pv` / `m_foreign_tlr_tag.pv` (item 27 of `docs/reviews/2026-09-06-codex-suite-falsification-s-p1-s-p2-s-p7-s-standing.md`), re-run byte for byte as `cap27a`/`cap27b` with the reviewer's cited `RESULT` at his line (`cap27a…out:1953`); and `cap27c`–`cap27f` on copies of the **committed** strict and degraded models | **(a): red, DESCENDED** (`cap27d`). **(b): red, PREDICTED** — channel symmetry, never a second run. **(c): not stated — (c) is C-C1's run.** **(d): red, DESCENDED** (`cap27f`). **No green control in any case**: the foreign signer is honest and needs no compromise to run |

**Why this companion had to be registered, shown rather than argued.**
The tag check is **inert in every committed model**: the 2026-09-06
single-removal matrix (row 14) removes it from the strict and degraded
S-STANDING models and changes no colour, because no honest signer in
any family fixture emits another tag over a TLR-shaped body. The
reviewer's fixture adds exactly one such signer, and the two runs
re-made here on our tree show the separation at his own line numbers:
with the check present every standing correspondence holds and the
attack is unreachable (`cap27a_ss_foreign_tag_reviewer_fixture.out:469`,
`:479`, `:489`, `:1953`); with **only** the check unbound the honest-key
correspondence for `skH1` and the unrestricted form go `is false`
(`cap27b…out:734`, `:595`) and the attack is reachable (`:2340`), while
`skH2`'s form (`:744`), the entitled-key judge (`:751`) and every witness
(`:1048`–`:2194`) are unchanged. The same signer, with the judge and its channel declared and the
parsed tag reported, added to copies of the models **as committed
today** reproduces it in both modes: `TagConfused` unreachable with the check (`cap27c…out:2045`,
`cap27e…out:1853`) and reachable without it (`cap27d…out:2471`,
`cap27f…out:2135`), the `skI` correspondence red in both
(`cap27d…out:824`, `cap27f…out:807`), and the alias judge, the
entitled-key judge and every witness unchanged. **That is a property no
single-family model can exhibit and the ledger says the capstone exists
to exhibit**; without this companion Band 0 would have exited with it
resting on a scratch run nothing registers. **What these six runs are
not:** capstone results — no capstone model exists — and not evidence
about the refusal record, whose body here is an opaque adversary-chosen
term.

## Repairs after the 2026-09-16 Codex review

*Written by the drafting step directed by the owner instance after
`docs/reviews/2026-09-16-codex-review-capstone-predictions.md` (six
findings, all accepted, all dispositions recorded there). **The skeptic
log above is untouched**, as are the review log, the freeze statement
and the routed `REFUSAL` fork, which is **not** resolved here. **No
capstone model exists; none was written; none was run.** The four runs
below are ProVerif 2.05 runs on **copies of committed family models**
under `formal/suite/ledger-tests-2026-09-14/`, each a copy whose header
states what it mutates, each `rc=0`; **no repository model was edited
or run**, and no `.out` below is a capstone result.*

### Edits, by finding

| # | Finding | Edit |
|---|---|---|
| **1** | D7 omitted its common-content consumer and companion | §3 **link 5** now names its **common-content conjunct as D7's consumer** and adds companion **C-C16**; §5's **D7 row** gains link 5's content conjunct in the consumer column, **C-C16** in the companion column and C-C16's expected red; **C-C16 registered in §9(3)** in the three-set form with its descent cited by `.out` line and its capstone-only members marked *not descended*; count 15 → **16** |
| **2** | C-C8-i was impossible as stated | §4's **C-C8 cell** now states the **two distinct obligations** — (α) set integrity, `SetAltered`, which needs the combined removal; (β) the exact possession-message relation, C-Q9, falsified by possession unbinding alone — and records that C-C8 is minimal for (α) and **over-determined** for (β). §9(2)'s two isolation configurations are re-specified: **C-C8-i is now the manifest-hash-only removal** (possession retained), required to keep **C-Q9 green**; **C-C8-ii is the possession-only removal**, whose **C-Q9 red is registered**, not a fixture break, and whose required outcome is **`SetAltered` green**. *The labels moved with the repair and the move is stated in both places, so no renumbering is silent.* The **post-freeze amendment paragraph is withdrawn** in place, with the withdrawn sentence quoted: the contradiction is established **before** the freeze, so no amendment is owed for it; the run discipline and §8's ordinary amendment rule stand |
| **3** | C-C15(i)'s retained set contradicted its mutation and the tree | §9(1)'s **C-C15 row**: `Reattributed` (C-Q3) and **link 5** **moved out of the retained set** into set (1) **for configuration (i)**, marked **descended**; evidential basis corrected to **`sp7_q6b_companion_key_outermost.pv:75-91`** (event declared and emitted; the header's recorded audit) and **`s-p7/RESULTS.md:58-71`** (*"red in Q6b"*), with the DSKS trace's violation of link 5's frame-to-accepting-key equality cited to `sp7_q6b_companion_key_outermost.pv:192-199`; the false claim *"neither model declares `Reattributed`"* corrected; configuration (ii) unchanged; and the principle stated: **preserved type soundness does not imply preserved key binding** |
| **4** | C-Q6 did not specify its composition join | §3 gains **"C-Q6's composition join, written out"**, (1)–(6): the `EstablishedWrapped(aid, lyr, t, kX, core, verdict)` **signature** with each argument named in the library's and `:1315`'s terms (and the `aid` name collision with S-STANDING's derived identity recorded); the **emission contract** (E1)–(E5) tying the report to the **same** wrapped acceptance, its innermost key, its evidenced tuple and its attempt core; the **representation mapping** from S-P7's `wrap(cvIw, (fbI, sgI))` extraction (`sp7_q2_degraded_compromised.pv:317-334`) to S-STANDING's `attemptCore(t, ppf, sg, decl)` (`ss_q1_strict_dns_compromised.pv:352-385`) as **five term equalities**; **what the equalities exclude**, stated as the attribution-for-A / standing-for-B substitution they forbid, including why `sg = sgI` must be a **term** equality under D-4; and the **unrestricted and honest-key forms in strict and degraded mode**, with the degraded unrestricted form **registered red** as the A4.6 cost. **C-C12's note is reconciled** with §(6). **D11's conditional half and D12's and D13's consumption are marked frozen only with this contract** in §5 |
| **5** | C-Q5 omitted S-P2's one-key/one-manifest restriction | §1.1's **required-signer-set row** names the key assignment — `skI` → `M2` slot A, `skB2` → `M2` slot B, **`skI2` → the one-signer manifest `M1`**, **one key, one manifest** — citing `s-p2/PREDICTIONS.md:201-214` and `s-p2/RESULTS.md:444-447`; §3's **C-Q5 entry** states why the judge needs it, **takes the restriction rather than the provenance correspondence** and says why (C-Q5 is `LEDGER.md:1292`'s *"S-P2's `MemberJudge` shape"*, and replacing it would orphan C-C3's and C-C8's descent), and records the cost: **C-Q5's green is conditional on the §1.1 key assignment** |
| **6** | *"every other choice is determined"* was premature | §8's closing sentence is **withdrawn in place, quoted**, and replaced by the two builder choices findings 4 and 5 exposed — **C-Q6's event signature, emission contract and representation mapping**, and **C-Q5's fixture key assignment** — each named as **this file's choice**, now fixed. The `REFUSAL` fork remains the one routed item and is **not** resolved |

### Scratch runs made for this repair

All four are ProVerif 2.05, `proverif -lib formal/suite/lib/tessera_theory.pvl <copy>.pv`, `rc=0`, on copies under
`formal/suite/ledger-tests-2026-09-14/`. Three reproduce the reviewer's
`/tmp` diagnostics on our own tree; the fourth (`cap3`) the reviewer did
not make.

| Run | Copy of | Mutation | Result |
|---|---|---|---|
| `cap1_sp2_content_unchecked` | `cq1c_sp2_slots_base.pv` | the three §A5.4 cross-slot content equalities deleted, nothing else | **`Spliced` `is false`** (`:1337`) while **all three link-2b completeness conjuncts stay `is true`** (`:1366`, `:1381`, `:1396`); `Stripped` (`:465`), `SignerForged` (`:472`), `SetAltered` (`:479`), `Reattributed` (`:486`), `PossessionTransplanted` (`:1344`), C-Q9 (`:1351`) green; witnesses reachable (`:657`, `:886`, `:1126`). **Finding 1 reproduced** |
| `cap2_sp2_poss_fponly` | `d10a_sp2_q9_base.pv` | possession production and verification made fingerprint-only, **nothing else** | **C-Q9 `is false`** (`:1263`) while **`SetAltered` stays `is true`** (`:471`); `Stripped` (`:457`), `SignerForged` (`:464`), `Reattributed` (`:478`), `Spliced` (`:1097`), `PossessionTransplanted` (`:1104`) green; witnesses reachable (`:643`, `:861`, `:1090`); baseline `d10a…out:1111` `is true`. **Finding 2 reproduced** |
| `cap3_sp2_mh_guards_dropped` | `d10a_sp2_q9_base.pv` | the frames' `mh = h(t)` guards deleted on both branches, possession over the accepted manifest **retained**, nothing else | **C-Q9 `is true`** (`:1115`) **and `SetAltered` `is true`** (`:468`); `Stripped` (`:452`), `SignerForged` (`:460`), `Reattributed` (`:476`), `Spliced` (`:1099`), `PossessionTransplanted` (`:1107`) green; witnesses reachable (`:642`, `:861`, `:1091`). **The new C-C8-i, shown possible** |
| `cap4_sp2_shared_slotA_key` | `d10a_sp2_q9_base.pv` | **the fixture only**: `M2`'s slot-A key re-keyed to `M1`'s key, so one honest key signs two manifests; **no verifier, judge or query changed** | **`SetAltered` `is false`** (`:640`) with `Stripped` (`:455`), `SignerForged` (`:462`), `Reattributed` (`:647`), `Spliced` (`:1260`), `PossessionTransplanted` (`:1267`), C-Q9 (`:1274`) all green and witnesses reachable (`:810`, `:1026`, `:1253`). **Finding 5 reproduced** |

**Findings 3, 4 and 6 are not run-showable and were not run.** Finding
3 is settled by evidence **already committed** in the tree
(`sp7_q6b_companion_key_outermost.pv:75-91`, `:192-199`;
`s-p7/RESULTS.md:58-71`), which is why the correction cites those lines
rather than a new run; finding 4 is a registration contract for a query
that exists in no model; finding 6 is a withdrawal.

**What did not change.** No query was added or removed; no probability,
no residual decomposition and no timebox was altered; the **26**
timeboxed entries and the **1155 min** per-case total stand; the
fixture's elements are unchanged apart from **naming** the key
assignment that was already implied by the inherited S-P2 restriction;
the skeptic log is untouched; and the routed `REFUSAL` fork (§8, item 1)
is untouched and unresolved.

---

## Repairs after the 2026-09-16 Codex review, second round (dispositioned and repaired 2026-09-17)

*Written by the drafting step directed by the owner instance after the
second non-author round,
`docs/reviews/2026-09-16-codex-review-capstone-predictions-round2.md`
(four findings, all accepted; the verdict was **not ready to freeze**),
whose six dispositions at its head are this repair's specification. Two
of those dispositions — findings 3 and 4 below — fix a fixture
meaning and are **clerk dispositions of the owner instance, marked
contestable**: they are **this file's choices**, not author rulings, and
the author may overrule either at the freeze commit without an
amendment. **The skeptic log above is untouched**, as are the review log,
the freeze statement, every probability, every timebox, and the routed
`REFUSAL` fork, which is **not** resolved here. **No capstone model
exists; none was written; none was run.** The ten runs below are
ProVerif 2.05 runs on **copies of committed family models** under
`formal/suite/ledger-tests-2026-09-14/` (sixth batch of that directory's
README), each a copy whose header states what it mutates, each `rc=0`;
eight are the reviewer's own `/tmp` diagnostics copied byte for byte and
re-run on our tree, landing at the reviewer's own `.out` line numbers.
**No repository model was edited or run**, and **no `.out` below is a
capstone result**.*

### Edits, by finding

| # | Finding | Edit |
|---|---|---|
| **1** | C-Q6's repaired emission contract (E1) shadowed C-C12 and made D13's severing test unavailable | §1.3: `aid` is minted **at intake**, by a front-end that reads the presented bundle once and forwards it on **private channels to the envelope path and the standing path in parallel**; both `LayerAccepted` and `EstablishedWrapped` carry it; the withdrawn *“minted once per **completed** acceptance”* is quoted in place, and the ledger's carried-forward correction (one fresh name per acceptance, shared across its slots, followed by `AcceptanceComplete`) is stated as **preserved and strengthened**. §3, C-Q6 (2): **(E1) restated as “same presentation”** — the standing path extracts the innermost `(t, ppf, sg, fb)` **structurally** from the same bundle (S-P7's `wrap()` destructuring) and **neither waits for nor is conditioned on `LayerAccepted`** — with the withdrawn (E1) quoted; **(E4)** named as the front-end's **structural parse** of the outer frame; **(E5) withdrawn from the emission contract**, quoted, and moved into the correct verifier's checks as **the very check C-C12 removes**. §3, C-Q6 (5): conjunct 2's judge `StandingUnentitledWrapped(kX, t)` observes **the standing path's own report** under the intake `aid` with the wrapped flag, as SS.Q3's judge does, and fires on `fp(kX) ≠ kfpr` **whether or not the envelope path accepted** — reachable under C-C12, unreachable in the correct model. §3, C-Q6 (6): **corrected, the 2026-09-16 sentence being wrong and not merely inconsistent** and quoted in place — under **C-C12** the honest-key forms **stay green** (`cap5a:642`, `:656`) and the unrestricted strict form goes red (`:628`) as a consequence; it is under **C-C11** that the honest-key forms go red (`ss_q2_companionA_identity_declared.out:808`, `:986`), **which is D12's severing**. §4: **C-C12's** set-completeness note records that **this row was right and §(6) wrong**, and **C-C11's** set (1) now names the forms; §5's **D11, D12 and D13** cells point at the **revised** contract |
| **2** | C-C15(i) could not retain C-Q7 while exhibiting its registered transplant | §9(1)'s **C-C15 row**: **C-Q7 moves from set (2) to set (1) for configuration (i)**, **descended** — the C-Q7 signature-term judge on the Q6b companion makes `SigTransplanted` **reachable** (`cap6b_sp7_q6b_sigjudge.out:1809`) where the same judge on the correct depth-1 model leaves it **unreachable** (`cap6a_sp7_q2_sigjudge.out:1099`), both honest witnesses staying reachable (`cap6b:1329`, `:1520`). The red is registered as a **consequence of the scope severing, not a second severing of D5**, on the pattern the row already uses for C-Q4's `InnerSigTransplanted`; **C-C6 remains C-Q7's own companion**. **Configuration (ii) is unchanged** — Q5c transplants no signature across keys, and C-Q7 green there is **predicted, not descended**. The reviewer's alternative (excluding inner acceptances from C-Q7) is **rejected**: it would blind D5's producer. The withdrawn set-(2) membership is quoted in place |
| **3** | C-C7(ii)'s retained set depends on a fixture choice the file had not made — **contestable** | §1.1's **Wrapper row**: the fixture **has same-key wrapping** — `skI` wraps its own attestation, as S-P7's I1 does (`s-p7/RESULTS.md:79-84`, divergence 7; `:54`, finding F7) — **alongside** the separate honest wrapper key `skW`; the **reason** (C-C15's set-(3) wrapped witnesses descend from runs where they are reachable **only** through I1 wrapping its own attestation, so without it C-C15(i)'s witness is unreachable by fixture) and **the alternative and its cost** are named. §4's **C-C7 row**: configuration (ii)'s three sets **re-specified from `cap7a`/`cap7b`** — set (1) gains **C-Q7** (`cap7b:528`), **honest-key authorship** (`:1072`, attack trace `:1032-1072`) and the **round-3 honest-filtered C-Q8** (`:711`) beside the structural C-Q8 (`:904`) and link 4; set (2) is the links and judges that do not touch byte binding, **predicted**; set (3) `HonestAccepted` (`:1250`); baseline with the signer all green (`cap7a:310`, `:316`, `:322`, `:330`, witness `:507`). The **“whole point”** sentence for (ii) is **withdrawn in place and quoted**: the quantifier-gap contrast is shown **family-locally** (`d6d:315` against `:507`) and is registered **NOT** to reproduce in the composed fixture, because the honest wrapper signature is an honest-released signature term over non-attest bytes and the honest-filtered form catches it too. **C-C6 and C-C7(i) are recorded unchanged by the signer**: `cap7c` ↔ `d5d` and `cap7d` ↔ `d6e`, result for result |
| **4** | “Adversary-enrolled issuer key” had no per-mode meaning, and its literal reading falsifies the strict baseline — **contestable** | §1.1's **Adversary row** now defines it **per case**: the adversary holds `skA` and a self-signed manifest `mA`, and authority evidence for `mA` exists **only where the compromise supplies it** — (a)/(b) the **one compromised channel** (insufficient for strict acceptance at `L0`, so the strict baseline stays green); (c) **both** channels, C-C1's registered red; (d) the **sole** channel, the A4.6 registered red — and **never from an uncompromised authority process**, inheriting S-P7's strict-mode sentence verbatim (`s-p7/PREDICTIONS.md:196-205`). The other reading is excluded **on evidence**: `cap8b:398` `is false` against the committed baseline `cap8a:201` `is true`, with honest-key authorship green (`cap8b:405`) and the witness reachable (`:601`). §3's retained-queries table names the reading in its strict-baseline cell |
| **5** | Findings 3 and 4 are consequential fixture choices, not clerical details | §8's list of **this file's own choices** grows from **two to four** — the 2026-09-16 wording is withdrawn in place and quoted — adding **same-key wrapping** and **the enrolment reading**, both marked **contestable**. The `REFUSAL` fork (§8, item 1) **remains the one routed item** and is **not** resolved |
| **6** | The first round's six findings, re-checked by the reviewer | 1, 2, 5 and 6 confirmed repaired; 3 partly, **closed by finding 2 here**; 4 not satisfactorily, **closed by finding 1 here**. The three carried-forward ledger corrections are honoured, and finding 1's repair **strengthens** the acceptance-identifier one rather than relaxing it. No edit of its own |

### Scratch runs made for this repair

All ten are ProVerif 2.05, `proverif -lib formal/suite/lib/tessera_theory.pvl <copy>.pv`, `rc=0`, on copies under
`formal/suite/ledger-tests-2026-09-14/` (sixth batch). Eight reproduce
the reviewer's `/tmp` diagnostics on our own tree at his own `.out` line
numbers; two (`cap7c`, `cap7d`) the reviewer did not make.

| Run | Copy of | Mutation | Result |
|---|---|---|---|
| `cap5a_ss_q3_companionB_asis` | `s-standing/proverif/ss_q3_companionB_entitled_via_envelope.pv`, **unchanged** | none — the committed C-C12 source re-run as the baseline | `StandingUnentitled` reachable (`:860`); unrestricted `Established ⟹ Designated` `is false` (`:628`); honest-key forms `is true` (`:642`, `:656`); `HonestStandingEstablished` reachable (`:1157`) |
| `cap5b_ss_q3_e1_projection` | `cap5a` | **one guard added to the standing path**, `if fp(kX) = kfpr then` before the report — the necessary condition of C-Q6's E1 (a `LayerAccepted` for the same `t` and `kX`); nothing else | `StandingUnentitled` **unreachable** (`:476`); unrestricted form **`is true`** (`:449`); honest-key forms `is true` (`:459`, `:469`); honest standing still reachable (`:773`). **Finding 1: E1 as written shadows C-C12** — the SS.Q3 p ≈ 0.2 branch, reproduced by event dependency instead of process order |
| `cap6a_sp7_q2_sigjudge` | `s-p7/proverif/sp7_q2_degraded_compromised.pv` (correct model, degraded, depth 1) | **adds** the C-Q7 signature-term judge (`GenericSigJudge`, `SigTransplanted`); verifier and every registered query unmutated | `SigTransplanted` **unreachable** (`:1099`); every registered query as committed (`:539`, `:552`, `:565`, `:578`, `:1086`); witnesses reachable (`:877`, `:1073`) |
| `cap6b_sp7_q6b_sigjudge` | `s-p7/proverif/sp7_q6b_companion_key_outermost.pv` (C-C15(i)'s source) | **adds** the same C-Q7 judge; the companion's own mutation unchanged | `SigTransplanted` **reachable** (`:1809`), with `Rescoped` (`:781`) and `InnerSigTransplanted` (`:1070`) red as committed, `TypeConfused` green (`:501`), witnesses reachable (`:1329`, `:1520`). **Finding 2: C-C15(i) cannot retain C-Q7** |
| `cap7a_sp1_q8_wrapper_signer_base` | `d6c_sp1_q8_judge_all.pv` (S-P1 Q2 + C-Q7 + both C-Q8 judges) | **adds** an honest `OT_WRAPPER` signer (`ForeignIssuer`) under the **same** issuer key `skI` and manifest `m`, releasing its signature and bytes to every judge; **pins** the presented frame's type to `OT_ATTEST` (where `d6c` read `ot`); byte binding **correct** | C-Q7 (`:310`), round-3 C-Q8 (`:316`), structural C-Q8 (`:322`) and honest-key authorship (`:330`) all `is true`; witness reachable (`:507`); Q2(ii) `is false` (`:658`) as registered. *The signer alone breaks nothing under correct byte binding* |
| `cap7b_sp1_q8_wrapper_signer_type_conditional` | `d6d_sp1_q8_type_conditional_unbound.pv` (C-C7(ii)'s source) | the same wrapper signer and `OT_ATTEST` pin added to the **type-conditional** byte unbinding | **C-Q7 `is false`** (`:528`), **both** C-Q8 forms `is false` (`:711`, `:904`), **honest-key authorship `is false`** (`:1072`, trace `:1032-1072`: an adversary-built `OT_ATTEST` frame under `pk(skI)` carrying the issuer's honest **wrapper** signature); witness reachable (`:1250`). **Finding 3: C-C7(ii)'s registered retained set does not survive a same-key wrapper signer** |
| `cap7c_sp1_condunbind_wrapper_signer` | `d5d_sp1_sigjudge_condunbind.pv` (C-C6's mutation + the C-Q7 judge) | the same wrapper signer and `OT_ATTEST` pin added to C-C6's **conditional** unbinding | **identical to `d5d` result for result**: C-Q7 `is false` (`:448` ↔ `d5d:414`), honest-key authorship `is true` (`:456` ↔ `:422`), witness reachable (`:633` ↔ `:599`), Q2(ii) `is false` (`:784` ↔ `:750`). *C-C6 keys on the signed frame's `kfp`, which the wrapper frame names; unchanged.* **A follow-up the reviewer did not make** |
| `cap7d_sp1_q8_samekey_unbound_wrapper_signer` | `d6e_sp1_q8all_samekey_unbound.pv` (C-C7(i) against every judge) | the same wrapper signer and `OT_ATTEST` pin added to C-C7(i)'s **same-key** unbinding | **identical to `d6e` result for result**: C-Q7 `is true` (`:312` ↔ `d6e:274`), both C-Q8 forms `is false` (`:493`, `:681` ↔ `:455`, `:643`), authorship `is false` (`:847` ↔ `:809`), witness reachable (`:1027` ↔ `:989`), Q2(ii) `is false` (`:1206` ↔ `:1168`). *C-C7(i) demands the signed frame name `fp(kX)`; unchanged.* **A follow-up the reviewer did not make** |
| `cap8a_sp1_q1_strict_base` | `s-p1/proverif/sp1_q1_strict_dns_compromised.pv`, **unchanged** | none — the committed strict baseline re-run | `Accept ⟹ IssuerSigned` `is true` (`:201`); honest-key authorship `is true` (`:208`); witness reachable (`:396`) |
| `cap8b_sp1_q1_strict_adversary_enrolled` | `cap8a` | **the fixture only**: an adversary key `skAdv` (published) with tuple `mAdv` under a distinct identity, for which **both honest authority processes** publish evidence; verifier and every query unmutated | **`Accept ⟹ IssuerSigned` `is false`** (`:398`) while honest-key authorship stays `is true` (`:405`) and the witness reachable (`:601`). **Finding 4: a genuinely enrolled adversary key falsifies the strict unrestricted baseline with no verifier change**, so “adversary-enrolled” must mean compromised-channel enrolment only |

**Findings 5 and 6 are not run-showable and were not run.** Finding 5 is
a bookkeeping consequence of findings 3 and 4 (§8's list of this file's
own choices); finding 6 is the reviewer's re-check of the first round and
is closed by findings 1 and 2 here.

**What did not change.** No query was added or removed; **no
probability, no residual decomposition and no timebox was altered**; the
**26** timeboxed entries and the **1155 min** per-case total **stand**,
as does the 4 × 1155 = 4620 min ceiling and everything §3's
“What the total is, and is not” says about it; the **companion count
stays sixteen** (no companion was added or removed — C-C7(ii)'s and
C-C15(i)'s **sets** were re-specified, and re-specification is what
`LEDGER.md:1474-1476` reserves to this file); the ladder, the ordering
and the ablation order are untouched; the **skeptic log** is untouched;
the **review log** and the **freeze statement** are untouched; and the
routed **`REFUSAL` fork** (§8, item 1) is untouched and **unresolved**.
The fixture's elements are unchanged apart from **saying what two of
them mean** — same-key wrapping in the Wrapper row and the enrolment
boundary in the Adversary row — both marked as **this file's
contestable choices** in §8.

---

## Repairs after the 2026-09-17 Codex review, third round

*Written by the drafting step directed by the owner instance after the
third non-author round,
`docs/reviews/2026-09-17-codex-review-capstone-predictions-round3.md`
(**three registration findings and one basis defect, all accepted**;
the verdict was **not ready to freeze**), whose five dispositions at its
head are this repair's specification. **They are clerk dispositions of
the owner instance, not author rulings.** None of them fixes a fixture
meaning; **finding 2's repair is an ADDITION beyond `LEDGER.md` §6
(`:1294`) and is marked as such where it is registered** (§3, C-Q6 (5),
conjunct 3). The reviewer confirms in its §6 that **all ten accepted
findings of rounds one and two are repaired**, except where the three
findings below reopen them — R1.4 and R2.1, both through finding 3 —
and that **the two contestable fixture choices of round two (same-key
wrapping, the enrolment reading) are now stated so a builder cannot
misread them; neither is reversed here and both stand.** All three
findings are on the text round two rewrote, which is the expected shape
of a convergent loop. **The skeptic log above is untouched**, as are the
review log, the freeze statement, every probability, every residual
decomposition, every timebox, the **26** timeboxed entries, the
**1155 min** per-case total, and the routed `REFUSAL` fork, which is
**not** resolved here. **No capstone model exists; none was written;
none was run.** The five runs below are ProVerif 2.05 runs on **copies
of committed family models** under
`formal/suite/ledger-tests-2026-09-14/` (seventh batch of that
directory's README), each a copy whose header states what it mutates,
each `rc=0`; all five are the reviewer's own `/tmp` diagnostics copied
byte for byte and re-run on our tree, landing at the reviewer's own
`.out` line numbers. **No repository model was edited or run**, and
**no `.out` below is a capstone result**.*

### Edits, by finding

| # | Finding | Edit |
|---|---|---|
| **1** | Link 2b's permitted projection dropped `lyr`, so one layer's slot report can satisfy another layer's completeness correspondence | §3, **link 2b**: the permitted projection becomes **`SlotSatisfied(aid, lyr, t, slot)`** and the old sentence is **quoted in place**; the reason is stated — round two's **intake** `aid` is shared by every layer of one presentation, and §1.1's same-key wrapping with the one-key/one-manifest assignment lets the wrapper and inner layers share `t` too, so only `lyr` excludes layer mixing (intake freshness excludes only **replay** mixing). §1.3: the round-two sentence *“a bundle still yields **at most one** acceptance”* is **withdrawn and quoted** — a **wrapped** bundle yields **one acceptance per layer**, each closing with its own `AcceptanceComplete(aid, lyr, t)` — and the per-acceptance name the ledger's carried-forward correction requires (`LEDGER.md:2249-2273`) is named as the **pair `(aid, lyr)`**: `aid` fresh per presentation, `lyr` distinguishing the layers within it. §4's **C-C9 row**: set (1) and set (2) now name the **layer-indexed** projection, at the layer whose `AcceptanceComplete` fired. §3's C-Q5 entry: the **not-taken** provenance-correspondence alternative follows the projection's arity. **Descended:** `cap9_sp2_slots_projection_no_lyr.out:1239` (projected form `is true`) against `:1454` (layer-indexed `is false`), witnesses `:675`, `:913`, `:1162` |
| **2** | After round two severed C-Q6 from envelope success, **no C-Q6 conjunct observed the envelope's attribution**, so C-C15's scope mutations could not red C-Q6 and D11's conditional half had no falsifiable consumer | §3, C-Q6 gains **conjunct 3, scope agreement**, marked **ADDITION beyond `LEDGER.md:1294`** with its reason: round two's independence is right for D13 (it is what lets C-C12 fail, `cap11a…:1307`) and severed D11's conditional half; conjunct 3 restores the consumption **without re-sequencing the paths**. The judge is in **S-P7's `ScopeJudge` house form** (`sp7_q2_degraded_compromised.pv:349-353`): it reads, on private channels, the standing path's report `(aid, lyr, kX)` and the envelope path's attribution report `(aid, lyr, kA, idA)` — the `scopeCh` report S-P7's models already emit (`sp7_q2_degraded_compromised.pv:303`, mutated at `sp7_q5c_companion_one_level_in.pv:240`) — and fires **`ScopeMisreported(aid, lyr, kX, kA)`** when `kA ≠ kX`; **unreachable in (a), (b), (d)**. **The judge waits for both reports; neither path waits for the other**, so the round-two independence stands and D13's severing is not re-shadowed. Witness **`HonestWrappedStandingAgreed(aid, lyr)`**, fired when the reports agree for an honest wrapped acceptance. Both event names are declared in C-Q6 **(1)**. §(5)'s heading *“The **two** conjuncts”* and C-Q6's opening *“**Two conjuncts**”* are **withdrawn and quoted**, now **three**; the *“Serves D12 and D13”* sentence now assigns **D11's conditional half to conjunct 3**. §5's **D11 row** names conjunct 3 as that half's consumer. §9(1)'s **C-C15 row**: set (1) for **both** configurations gains conjunct 3 — (i) `kA = kW ≠ kI`, (ii) `kA = kM ≠ kI` — and the membership *“both configurations also red **C-Q6's standing conjunct**”* is **withdrawn and quoted**; the **standing and entitled-key conjuncts move to set (2)** for both configurations, **predicted green**. §4's **C-C11** and **C-C12** rows gain conjunct 3 in set (2), **predicted** (a standing mutation changes neither path's attribution report). **No timeboxed entry is added: C-Q6's 90 min stands.** **Descended at the reviewer's projection:** `cap10_ss_q3_scope_report_only.out:779` (`ScopeMisreported` reachable when only the reported key changes) with `:798`, `:811`, `:856`, `:1205` green/reachable |
| **3** | The representation mapping still carried the fingerprint **precondition** that (E5)'s withdrawal removed, and (E5)'s text mis-stated C-C12's boundary | §3, C-Q6 **(3)**: the mapping table is rewritten with **two columns per row** — the **term equality** (immutable, defines the join, removed by no companion) and the **verifier check it enables** (the correct verifier's, removable by the named companion): `kX = kI` \| `fp(kX) = kfpr`, **check 7**, removed by **C-C12**; `ppf = ppfI` \| `checksign(ppf, kX) = (POSS, t)`, **link 3**, removed by **C-C3/C-C8**; `fb = fbI` \| `checksign(sg, kX) = (BYTES, fb)`, **link 4**, removed by **C-C5/C-C7**; `sg = sgI` \| **none — the pin itself**; `t = tI` \| the **evidence checks**. The introduction's *“all four required”* is **withdrawn and quoted** and corrected to the **five term equalities** as required, the checks as the verifier's. §(4) now rests the artifact-A/artifact-B exclusion on the **term** equalities, citing the join that carries it with **no** precondition. **(E5)**'s *“exactly the check C-C12 removes”* is **withdrawn and quoted**: **C-C12 removes `fp(kT) = kfpr` only and RETAINS `kT = kX`** (`ss_q3_companionB_entitled_via_envelope.pv:259-265`, the mutation comment, with `if kT = kX then` immediately below it at **`:263`**). **Descended:** the structural join works — `cap11a…:735` (designation `is false`, as C-C12 requires), `:756` (substitution unreachable), `:1307` (`StandingUnentitled` reachable), `:1657` (honest standing reachable); the fingerprint clause kept anywhere in the join **re-shadows C-C12** — `cap11b…:495` `is true`, `:553` unreachable; and the `sg` pin is **load-bearing, not decoration** — `cap11c…:847` reachable with `:495` still `is true` |
| **4** | A basis generalization in the retained-query table contradicted by round two's own evidence | §3's **retained-queries table**, honest-key authorship row: *“green in every mutant that reds C-Q7”* is **withdrawn and quoted** and replaced by what the runs show — green in every **S-P1-only** mutant that reds C-Q7 (`d5d_sp1_sigjudge_condunbind.out:414` C-Q7 `is false`, `:422` authorship `is true`), and **red beside C-Q7 under C-C7(ii) in the composed fixture** (`cap7b…:528` and `:1072`, the attack trace at `:1032-1072`), which §4's C-C7 row already registers. The row also records that **`d6e_sp1_q8all_samekey_unbound.out` is not an instance either way** — its C-Q7 is **green** (`:274`) and its authorship **red** (`:809`) — so it cannot support the generalization. **The p ≈ 0.85 baseline prediction stands**; only the supporting sentence changed |
| **—** | Consequential edits in §5 and §9, listed once so no renumbering is silent | §5: the **D11** row names conjunct 3 as the consumer of its conditional half (finding 2); no matrix row, producer, consumer, companion or expected red is otherwise changed, and **D12 and D13 are untouched**. §9(1): the **C-C15** row's sets (1) and (2) are **re-specified** for finding 2, with the withdrawn membership quoted in place; **its mutation, its row (D11), its configurations and its witnesses are unchanged**, and re-specification is what `LEDGER.md:1474-1476` reserves to this file. §4: **C-C9**, **C-C11** and **C-C12** gain the members named above; **no companion was added or removed and the count stays sixteen** |

### Scratch runs made for this repair

All five are ProVerif 2.05,
`proverif -lib formal/suite/lib/tessera_theory.pvl <copy>.pv`, `rc=0`,
on copies under `formal/suite/ledger-tests-2026-09-14/` (seventh batch).
All five reproduce the reviewer's `/tmp` diagnostics on our own tree at
his own `.out` line numbers. Three of them (`cap11a`–`cap11c`) are the
reviewer's **structural-join rewrite** of the SS.Q3 companion — the
round-two repair of C-Q6's (E1) built on a family-model copy — and are
the first runs on the record in which that join exists in any model.

| Run | Copy of | Mutation | Result |
|---|---|---|---|
| `cap9_sp2_slots_projection_no_lyr` | `cq1c_sp2_slots_base.pv` | **two layers** (`L0`, `L1`) sharing one intake `aid` and one tuple `t`; slot B reported at `L1` only; the link-2b correspondence stated twice — **projected without `lyr`** (`SlotSatisfied(aid, t, slot)`, as the file then permitted) and **layer-indexed** (`LayerSlot(aid, lyr, t, slot)`) | projected form **`is true`** (`:1239`) while the layer-indexed form is **`is false`** (`:1454`); every S-P2 query and the three original link-2b conjuncts unchanged (`:483`–`:504`, `:1169`–`:1225`); witnesses reachable (`:675`, `:913`, `:1162`). **Finding 1: the projection can borrow another layer's slot report; it must keep `lyr`** |
| `cap10_ss_q3_scope_report_only` | `cap11b` (the structural join **with** the fingerprint guard) | **only the envelope's reported attribution key changed** (`reportK = pk(dsks(sg, decl))` in place of `kX`) and a scope-agreement judge added that fires `ScopeMisreported(kX, reportK)` when they differ; **standing path untouched** | **`ScopeMisreported` reachable** (`:779`) while wrapped designation (`:798`, `:811`), the substitution guard (`:817`), entitled-key safety (`:856`) and honest standing (`:1205`) stay green/reachable. **Finding 2: a scope mutation leaves every C-Q6 conjunct green; C-Q6 needs a scope consumer** |
| `cap11a_ss_q3_structural_join` | `s-standing/proverif/ss_q3_companionB_entitled_via_envelope.pv` (C-C12's source) | the **structural join**: `Front` process, `standingIn`/`envelopeIn` private channels, `wrap()` destructuring in both paths, `let attemptCore(=t, =ppfI, =sgI, decl) = core`, `EstablishedWrapped(intake, L1, t, kT, core, ESTABLISHED)` emitted by the standing path alone, a `Substituted(core, expected)` guard; **no** fingerprint precondition | wrapped designation **`is false`** (`:735`) as C-C12 requires; honest-key form `is true` (`:749`); **`Substituted` unreachable** (`:756`); `StandingUnentitled` **reachable** (`:1307`); honest standing reachable (`:1657`). **The round-two structural repair works at this projection** |
| `cap11b_ss_q3_structural_join_fp_pin` | `cap11a` | one guard added, `if fp(kX) = kfpr then` — the mapping row's *“with `fp(kX) = kfpr` from `t`”* read as a **precondition** | wrapped designation **`is true`** (`:495`); `Substituted` unreachable (`:514`); **`StandingUnentitled` unreachable** (`:553`); honest standing reachable (`:902`). **Finding 3: the fingerprint clause, kept anywhere in the join, re-shadows C-C12** |
| `cap11c_ss_q3_structural_join_sg_unpinned` | `cap11b` | the `attemptCore` signature-term pin `=sgI` relaxed to a free `otherSg` (fingerprint guard retained) | **`Substituted` reachable** (`:847`) while wrapped designation stays `is true` (`:495`). **The `sg = sgI` term equality is load-bearing**: without it a core over a different signature passes |

**Finding 4 is not run-showable and was not run.** It is settled by
evidence **already on the record** — `d5d_sp1_sigjudge_condunbind.out`,
`d6e_sp1_q8all_samekey_unbound.out` and the round-two run
`cap7b_sp1_q8_wrapper_signer_type_conditional.out` — which is why the
correction cites those `.out` lines rather than a new run.

**What did not change.** No query was added or removed — **conjunct 3
is a third conjunct of the registered query C-Q6, not a new registered
query**, and it adds no timeboxed entry; **no probability, no residual
decomposition and no timebox was altered**; the **26** timeboxed
entries and the **1155 min** per-case total **stand**, as does the
4 × 1155 = 4620 min ceiling and everything §3's *“What the total is,
and is not”* says about it; the **companion count stays sixteen** (no
companion was added or removed — C-C9's, C-C11's, C-C12's and
C-C15's **sets** were re-specified, which `LEDGER.md:1474-1476`
reserves to this file); **the fixture is entirely unchanged**, including
the two contestable choices of round two (same-key wrapping and the
enrolment reading), which this round confirms and does not reverse; the
ladder, the ordering and the ablation order are untouched; §5's matrix
rows, producers, consumers, companions and expected reds are unchanged
apart from D11's named consumer; the **skeptic log** is untouched; the
**review log** and the **freeze statement** are untouched; and the
routed **`REFUSAL` fork** (§8, item 1) is untouched and **unresolved**.

---

## Repairs after the 2026-09-17 Codex review, fourth round

*Written by the drafting step directed by the owner instance after the
fourth non-author round,
`docs/reviews/2026-09-17-codex-review-capstone-predictions-round4.md`
(**two findings, both accepted**; the verdict was **not ready to
freeze**), whose dispositions at its head are this repair's
specification. **They are clerk dispositions of the owner instance, not
author rulings.** Neither fixes a fixture meaning. The reviewer's own
closing sentence is quoted because it bounds what this repair may
touch: **"I found two supported defects, not a third to manufacture.
The repaired structural join passes the requested independence and
substitution controls."** The reviewer confirms in its §6 that **all
fourteen accepted findings of rounds one to three are repaired**, R1.4
and R3.2 reopened only by finding 1 here, and that **all three ledger
corrections are honoured**; it confirms the **two contestable fixture
choices** — same-key wrapping and the compromised-channel-only reading
of "adversary-enrolled" — are explicit with their alternatives and
consequences stated, and **does not reverse either; both stand**. Both
findings fall on round three's new conjunct and on the witness rule
that conjunct's mutation set exposed; **nothing outside the repaired
text was found**. **The skeptic log above is untouched**, as are the
review log, the freeze statement, every probability, every residual
decomposition, every timebox, the **26** timeboxed entries and the
**1155 min** per-case total, and the routed `REFUSAL` fork, which is
**not** resolved here and which the reviewer names, correctly, as owed
before the author's commit. **No capstone model exists; none was
written; none was run.** The seven runs below are ProVerif 2.05 runs on
**copies of committed family models** under
`formal/suite/ledger-tests-2026-09-14/` (eighth batch of that
directory's README), each a copy whose header states what it mutates,
each `rc=0`; all seven are the reviewer's own `/tmp` diagnostics copied
byte for byte and re-run on our tree, landing at the reviewer's own
`.out` line numbers. **No repository model was edited or run**, and
**no `.out` below is a capstone result**.*

### Edits, by finding

| # | Finding | Edit |
|---|---|---|
| **1** | Conjunct 3's judge compared the attributed **key** only, so an identity-only re-scoping left all three C-Q6 conjuncts green; the inherited scope relation D11 names covers key **and** issuer identity, and S-P7's committed Q6a companion is exactly the identity-only case | §3, C-Q6 **(1)**: the event declaration becomes **`ScopeMisreported(bitstring, bitstring, pkey, bitstring, pkey, bitstring)`** over *(`aid`, `lyr`, `kX`, `id`, `kA`, `idA`)*, and the four-place declaration is **withdrawn and quoted**. §3, C-Q6 **(5) conjunct 3**: the standing path's report becomes **`(aid, lyr, kX, id)`**, `id` being the innermost issuer identity read off the `authTuple(id, kfpr, sset, alg, ver)` **the standing path extracted itself** under (E1) — no new extraction, no new verifier check; the judge fires **`ScopeMisreported(aid, lyr, kX, id, kA, idA)`** when **`(kA, idA) ≠ (kX, id)`**, **unreachable in (a), (b) and (d)**; the key-only firing sentence is **withdrawn and quoted**. The pair form is **S-P7's own** (`s-p7/PREDICTIONS.md:226-237`: `Rescoped(kIrep, idIrep, kH, idH, fbI)` fires on *"an acceptance of the same `fbI` with `(kIrep, idIrep) ≠ (kH, idH)`"*). §5's **D11** row restates the consumer in the pair form, quoting the withdrawn cell wording. §9(1)'s **C-C15** row: the phrase *"It is registered here as the **isolation contrast**, not as a third configuration"* is **withdrawn and quoted**, and Q6a is registered as **configuration (iii), the isolation configuration** with a full three-set specification — set (1) conjunct 3's **identity half**, C-Q4's `Rescoped` (descended) and link 6b at `L1` (predicted); set (2) **everything else including conjunct 3's KEY half**, so the run shows the identity comparison is what fires; set (3) the honest wrapped witnesses. **Descended:** the escape — `cap12e…out:945` (identity judge **reachable**) with `:570` (key-only judge **unreachable**), `:542`, `:556`, `:1368` (all three conjuncts green), `:563` (substitution excluded), `:1718` (honest standing reachable); the committed companion is that case — `cap12f…out:1339` (key-only judge **green**) against `:818` (committed `Rescoped` **red**), witnesses `:1130`, `:1326`. **No companion was added: the count stays sixteen**, and configuration (iii) adds no timeboxed entry |
| **2** | C-C11's Q4 alternate deletes the terminal branches, so the S2 and S4 report-shape witnesses cannot fire; C-Q6 lists the S4 witness as required and C-N1 called any unreachable registered witness a broken fixture, so a faithful transcription of the alternate was classified as a broken fixture | §3, **C-N1**: the rule sentence is **kept and qualified**, with the withdrawn *reading* quoted — the registered witnesses are of **two kinds**. **Honest-flow witnesses** (`HonestStandingEstablished`, `HonestWrappedStandingAgreed`, `HonestWrappedAccepted`, `HonestAccepted`, both `HonestComplete`, `HonestChain`) **must survive every companion** and no exception applies to them. **Vocabulary witnesses** (S1–S4 and MISMATCH, the standing report shapes) are reachable in **every correct-form run**, and their disappearance under a **named** companion is a **registered consequence of the mutation, never a broken fixture** — but only where that companion's row names it; an unnamed disappearance is still a broken fixture. The distinction is the family's own, inherited (`s-standing/RESULTS.md`, SS.Q4 row and `:345`). §3, **C-Q6's witness list**: the S4-row witness is marked a **vocabulary** witness with a pointer to C-C11. §4, **C-C11's row**, set (3): the consequence is registered — under the **Q4 alternate** S2 and S4 are **unreachable**, **descended** from the committed `ss_q4_companionC_terminal_unchecked.out:1708`, `:1838` (with N1 reachable at `:1425`) and reproduced on the structural join at `cap12g…out:3217`, `:3413`, with **honest standing reachable** (`:2873`), the **agreement witness reachable** (`:1542`), the standing correspondences **red** (`:810`, `:1136`, and S-STANDING's own honest-key forms `:2190`, `:2514`) and conjunct 3 green in both halves (`:1152`, `:1160`). **Checked, not assumed, for the other companions:** all five vocabulary witnesses stay reachable under **abl6** (`abl6_no_tlr_signature.out:1472`, `:1648`, `:1771`, `:1943`, `:2090`), under C-C11's own **Q2** mutation (`ss_q2_companionA_identity_declared.out:1692`, `:1868`, `:1996`, `:2170`, `:2346`) and under **C-C12** (`ss_q3_companionB_entitled_via_envelope.out:1357`, `:1558`, `:1686`, `:1883`, `:2055`) — **the Q4 alternate is the only registered exception in this file** |
| **3** | Disposition 3, not a finding: conjunct 3's independence and substitution controls were **asserted**, and the reviewer built and ran the actual paired-report judge | §3, C-Q6 **(5) conjunct 3**: a **"Descent at the reviewer's projection"** table is added, citing the four paired-judge controls on the structural join over the **correct** S-STANDING strict model — correct checks, `cap12a…out`: conjunct 3 unreachable (`:570`), conjunct 2 unreachable (`:998`), substitution unreachable (`:563`), witness reachable (`:958`); **C-C12**, `cap12b…out`: conjunct 3 unreachable (`:813`), conjunct 2 **reachable** (`:1762`), witness reachable (`:1204`); **key-scope mutation**, `cap12c…out`: conjunct 3 **reachable** (`:947`), conjunct 2 unreachable (`:1378`), witness reachable (`:1334`); **both**, `cap12d…out`: both **reachable** (`:1192`, `:2140`), witness reachable (`:1581`). The two severings are **independent**; **both paths emit independently and only the judge waits**. Marked **descended at a projection, predicted for the capstone**, the vocabulary §9(1) already uses |
| **—** | Consequential edits, listed once so no renumbering is silent | §5: the **D11** row's consumer cell restates the pair form and renames Q6a as configuration (iii); **no matrix row, producer, consumer, companion or expected red is otherwise changed**, and D12 and D13 are untouched. §9(1): the **C-C15** row gains configuration (iii) and its three sets, and its descent column gains that configuration's `.out` lines; **its mutation for (i) and (ii), its row (D11) and their sets and witnesses are unchanged**. §4: **C-C11**'s set (3) and descent column gain the vocabulary-witness consequence; **no companion was added or removed and the count stays sixteen** |

### Scratch runs made for this repair

All seven are ProVerif 2.05,
`proverif -lib formal/suite/lib/tessera_theory.pvl <copy>.pv`, `rc=0`,
on copies under `formal/suite/ledger-tests-2026-09-14/` (eighth batch of
that directory's README). All seven reproduce the reviewer's `/tmp`
diagnostics on our own tree at his own `.out` line numbers. `cap12a` is
the reviewer's construction of the **round-three contract on the correct
S-STANDING strict model** — the structural join of `cap11a` plus the
**paired scope-agreement judge** of conjunct 3, reading `(aid, lyr, …)`
reports from both paths on the private channels `scopeStanding` and
`scopeEnvelope` and firing `ScopeMisreported` or the witness
`HonestWrappedStandingAgreed`. `cap12b`–`cap12d` are its controls
(disposition 3); `cap12e`–`cap12g` are the two findings.

| Run | Copy of | Mutation | Result |
|---|---|---|---|
| `cap12a_ss_q1_join_correct` | `s-standing/proverif/ss_q1_strict_dns_compromised.pv` (correct strict model) | the structural join + paired scope-agreement judge; **all checks correct** | wrapped designation `is true` (`:542`, `:556`); `Substituted` unreachable (`:563`); **`ScopeMisreported` unreachable** (`:570`); identity judge unreachable (`:577`); **`HonestWrappedStandingAgreed` reachable** (`:958`); `StandingUnentitled` unreachable (`:998`); honest standing reachable (`:1348`) |
| `cap12b_ss_q1_join_cc12` | `cap12a` | **C-C12's mutation** — the standing path's `fp(kT) = kfpr` check removed, nothing else | wrapped designation **`is false`** (`:782`), honest-key form `is true` (`:797`); `ScopeMisreported` **unreachable** (`:813`); **`StandingUnentitled` reachable** (`:1762`); agreement witness reachable (`:1204`); honest standing reachable (`:2113`). *D13 still severable beside conjunct 3* |
| `cap12c_ss_q1_join_scope_key` | `cap12a` | **key-scope mutation** — the envelope's attribution report names a DSKS-derived key in place of `kX` when the wrapper identity differs; standing path untouched | **`ScopeMisreported` reachable** (`:947`); every C-Q6 conjunct 1/2 form `is true` (`:548`, `:562`); `StandingUnentitled` unreachable (`:1378`); agreement witness reachable (`:1334`). *Conjunct 3 severable on its own* |
| `cap12d_ss_q1_join_cc12_scope_key` | `cap12b` | both mutations | `ScopeMisreported` reachable (`:1192`) **and** `StandingUnentitled` reachable (`:2140`); agreement witness reachable (`:1581`). *The two severings are independent* |
| `cap12e_ss_q1_join_scope_identity` | `cap12a` | **identity-only scope mutation** — the envelope's attribution report names the **wrapper's identity** `iw` in place of the inner `id`; the key unchanged; a `ScopeIdentityWrong(aid, lyr)` judge added | all three C-Q6 conjuncts green (`:542`, `:556`, **key-only `ScopeMisreported` unreachable `:570`**) while **`ScopeIdentityWrong` reachable** (`:945`); `Substituted` unreachable (`:563`); honest standing reachable (`:1718`). **Finding 1: a key-only judge misses identity-only re-scoping** |
| `cap12f_sp7_q6a_keyjudge` | `s-p7/proverif/sp7_q6a_companion_identity_outermost.pv` (S-P7's identity-from-outermost companion) | **adds** a key-only scope judge (`KeyOnlyScopeWrong`) beside the committed full `Rescoped` query; the companion's mutation unchanged | **key-only judge `is true`** (`:1339`) while the committed **`Rescoped` `is false`** (`:818`); `HonestWrappedAccepted` reachable (`:1130`), `HonestAccepted` reachable (`:1326`). **Finding 1: the family's own companion is exactly the case the key-only judge cannot see** |
| `cap12g_ss_q1_join_terminal_unchecked` | `cap12a` | **S-STANDING Q4's mutation** — `StandingDecide` ignores the terminal disposition and reports `ESTABLISHED` after lineage membership | standing correspondences **`is false`** (`:810`, `:1136`; S-STANDING's own honest-key forms `:2190`, `:2514`); `Substituted`, `ScopeMisreported`, identity judge unreachable (`:1144`, `:1152`, `:1160`); agreement witness reachable (`:1542`); honest standing reachable (`:2873`); **S2 and S4 vocabulary witnesses unreachable** (`:3217`, `:3413`) — the branches no longer exist, as the committed `ss_q4…out:1708`, `:1838` already records. **Finding 2: C-C11's Q4 alternate must register that disappearance as a consequence** |

**What did not change.** No query was added or removed — **conjunct 3
is still one conjunct of the registered query C-Q6, now comparing a
pair instead of a key**, and it adds no timeboxed entry; **no
probability, no residual decomposition and no timebox was altered**;
the **26** timeboxed entries and the **1155 min** per-case total
**stand**, as does the 4 × 1155 = 4620 min ceiling and everything §3's
*"What the total is, and is not"* says about it; the **companion count
stays sixteen** — C-C15 gained a **configuration**, not a companion,
on the `C-C8-i`/`C-C8-ii` pattern, and C-C11's and C-C15's **sets**
were re-specified, which `LEDGER.md:1474-1476` reserves to this file;
**the fixture is entirely unchanged**, including the two contestable
choices, which this round confirms and does not reverse; the ladder,
the ordering and the ablation order are untouched; §5's matrix rows,
producers, consumers, companions and expected reds are unchanged apart
from D11's consumer cell restating conjunct 3 in the pair form; the
**skeptic log** is untouched; the **review log** and the **freeze
statement** are untouched; and the routed **`REFUSAL` fork** (§8, item
1) is untouched and **unresolved**.

---

## Repairs after the 2026-09-17 Codex review, fifth round

*Written by the drafting step directed by the owner instance after the
fifth non-author round,
`docs/reviews/2026-09-17-codex-review-capstone-predictions-round5.md`
(**two findings, both accepted**; the verdict was **not ready to
freeze**), whose four dispositions at its head are this repair's
specification. **They are clerk dispositions of the owner instance, not
author rulings.** Neither finding fixes a fixture meaning, and **the two
contestable fixture choices of round two — same-key wrapping and the
compromised-channel-only reading of “adversary-enrolled” — stand**: the
reviewer confirms both are explicit with their alternatives and
consequences stated, does not reverse either, and finding 2's repair
**carries** the enrolment choice rather than reversing it, since the
green control it registers is a consequence of that very choice. The
reviewer confirms in its §6 that **all sixteen accepted findings of
rounds one to four have their specified repairs present**, and that the
**round-four pair-scope and witness repairs pass its bounded controls**.
Both findings fall on text **no earlier round had rewritten**, which is
the first time that has happened since round one. **The skeptic log
above is untouched**, as are the review log, the freeze statement, every
probability, every residual decomposition, every timebox, the **26**
timeboxed entries, the **1155 min** per-case total, and the routed
`REFUSAL` fork, which is **not** resolved here and which the reviewer
again names, correctly, as owed before the author's commit. **The
companion count changes: sixteen → SEVENTEEN**, C-C17 being registered
in §9(4) as D7's membership severing companion; §4's count paragraph
carries the change and quotes the withdrawn sentence. **No capstone
model exists; none was written; none was run.** The fourteen runs below
are ProVerif 2.05 runs on **copies of committed family models** under
`formal/suite/ledger-tests-2026-09-14/` (ninth batch of that directory's
README), each a copy whose header states what it mutates, each `rc=0`;
thirteen are the reviewer's own `/tmp` diagnostics copied byte for byte
and re-run on our tree, landing at the reviewer's own `.out` line
numbers, and the fourteenth (`cap14d`) the reviewer did not make. **No
repository model was edited or run**, and **no `.out` below is a
capstone result**.*

### Edits, by finding

| # | Finding | Edit |
|---|---|---|
| **1** | D7 claims discharge of three producers and had a severing companion for two: C-C9 severs completeness and C-C16 common content, and **both retain link 2a and `SignerForged`**, so the **membership** half — the fact link 2a consumes — had no companion failing its consuming query, which A3.3 requires | **C-C17 registered in §9(4)**, in the three-set form §9(3) uses for C-C16: S-P2 Q4 transcribed, **slot B's `fp(kB) = kfprB` removed on the two-signer branch** of the capstone's check 3, everything else retained (family source `s-p2/proverif/sp2_q4_companion_slot_unbound.pv`, `s-p2/RESULTS.md:46`). Set (1): **C-Q1 link 2a** at the layer — `ChainBroken(lyr, LINK_2A)` reachable, **not descended**, its **shape** descended by the structural slot-to-key judge (`cap13b…:1972` `is false` against `cap13a…:1206` `is true`) — **`SignerForged`** descended (`cap13b…:730`; family-locally `sp2_q4_companion_slot_unbound.out:601`, trace `:360-601`), and **`PossessionTransplanted`** as a **recorded consequence** (`cap13b…:1657`), with the reason stated: **S-P2's Q4 model declares no `PossJudge`**, so the family run could not have recorded it. Set (2): link 2b's three conjuncts (`:1685`, `:1722`, `:1759`), `Stripped` (`:481`), `Spliced` (`:1398`), `SetAltered` (`:739`), C-Q3 (`:749`), C-Q9 (`:1666`), and **predicted:** links 1a, 1b, 3, 4, 5, 6a, 6b, C-Q2, C-Q7, C-Q8. Set (3): both `HonestComplete` (`:922`, `:1150`), `HonestAccepted` (`:1389`), `HonestChain(L0, t)` predicted. **The reviewer's correction of the projection is recorded**: the slot report names the **manifest-named** slot `kfprA`/`kfprB` per §1.3, where `cq1c` reported `fp(kA)`, and the judge is unsatisfiable at `cq1c`'s projection and live at §1.3's. §3, **link 2a** now names **C-C17** as its companion, with the withdrawn *“both modes.”* clause quoted. §5's **D7 row** now names **three companions, one per producer**, with the withdrawn cell quoted and C-C17's expected red stated. §4's count: **sixteen → seventeen**, withdrawn sentence quoted. **No timeboxed entry is added** — C-C17 runs inside link 2a's 45-minute box |
| **2** | C-C15(i)'s failed set is a **degraded-case** result: transcribed onto the strict model with both outer authority checks and the same-key wrapper signer retained, **every query is green and every witness reachable**, because the enrolment rule gives the adversary no authorized wrapper key in (a)/(b). The registration listed its reds with **no case assignment** and invoked both C-Q1 forms | **Generalized to every companion.** §4's preamble gains the rule: each row carries a **Cases** cell stating, per configuration, where the red is **registered and descended**, where it is **predicted**, and where the configuration is a **green control** — mutation present, every query green, every witness reachable — **registered as a result, not a broken fixture**, with **C-N1's rule explicitly not classifying it as one** (that rule governs an unreachable *witness*). A **Cases** column is added to §4's numbered table, §4's unnumbered table, §9(1), §9(2) and §9(3). **C-C15** exactly as disposition 2 fixes it: **(i)** red in **(d)** descended (Q6b), **green control in (a)/(b)** descended (`cap14b…:550`, `:559`, `:568`, `:843`, `:1047`; `cap14c…` identical line for line); **(ii)** red in **(d)** descended, Q5c having run **degraded only**, with (a)/(b) **red predicted if the depth-2 honest route exists, else a green control** — stated as an **observation of the run**, not predicted either way; **(iii)** red in **(a)**, **(b)** and **(d)** — **descended in strict** by `cap14d_sp7_q1_strict_q6a.out:892` (trace `:880-892`, the **honest-only route**: honest wrapper `skW2` wrapping I2's attestation, identity `idW2` reported), with `:906`, `:920`, `:1185`, `:1394`, and **in degraded** by the committed Q6a. **D11's discharge in (a)/(b) is stated to rest on (iii)**; in (d) on (i), (ii) and (iii). The C-C15 row's sentence invoking **“both C-Q1 forms”** without case assignment is **withdrawn and quoted** in the Row column. Every other companion's cell is filled from its descent — degraded-only descent gives *“red in (d) descended; (a)/(b) predicted”* with the **green-control reading named where the enrolment rule removes the attack** and **declined, with its reason, where it does not** — **C-C1** stays **(c) only**, and **C-C14** and the S-STANDING-derived **C-C11** and **C-C12** are recorded as **descended from strict runs** |
| **3** | Disposition 3, not a finding: the reviewer built and ran the **pair-form** conjunct-3 judge and the three C-C11-family controls, which the file had at the key-only arity and on the committed outputs only | §3, C-Q6 **(5) conjunct 3**: a second *“Descent at the reviewer's projection”* table, **the pair form, run** — none (`cap15a…:570`, `:998`, `:958`); identity only (`cap15b…:953` reachable with the **key-only control green** at `:576`, `:1746`, `:1706`); key only (`cap15c…:947`, `:1378`, `:1334`); C-C12 only (`cap15d…:813`, `:1762`, `:1204`); both (`cap15e…:1192`, `:2140`, `:1581`). The round-four independence result **survives the arity change**. §3, **C-N1**'s two-kinds rule gains the **three C-C11-family controls** on that same join: C-C11 proper (`cap16a…:2581`, `:1450`, all five vocabulary witnesses `:2826`–`:3738`), abl6 (`cap16b…:2548`, `:1436`, all five `:2790`–`:3665`) and the Q4 alternate (`cap16c…:2873`, `:1542`, **S2 and S4 unreachable** `:3217`, `:3413`, the other three reachable). The honest-flow witnesses survive **every** configuration and the vocabulary loss occurs under **exactly one** alternate — the one §4's C-C11 row names |
| **—** | Consequential edits, listed once so no renumbering is silent | §3: **link 2a** gains its companion (finding 1); no other query, prediction, probability, residual or timebox is touched. §4: the **Cases** rule paragraph and column; the **count** paragraph goes **sixteen → seventeen** with the withdrawn sentence quoted, and the earlier *“sixteen”* and *“fifteen”* inside the **dated repair sections** are left as written, because those sections record the count **as it stood at each round** and are not rewritten. §5: the **D7** row only — no other matrix row, producer, consumer, companion or expected red changes, and D11, D12 and D13 are untouched apart from D11's discharge reading stated in C-C15's Cases cell. §9(1): the three rows gain **Cases** cells and C-C15's Row column is re-stated with its withdrawn sentence quoted; **its mutation, its three configurations, its sets and its witnesses are otherwise unchanged**. §9(2) and §9(3): **Cases** cells only. §9(4): **new**, C-C17. **No query was added or removed, no companion was removed, and no timeboxed entry was added** |

### Scratch runs made for this repair

All fourteen are ProVerif 2.05,
`proverif -lib formal/suite/lib/tessera_theory.pvl <copy>.pv`, `rc=0`,
on copies under `formal/suite/ledger-tests-2026-09-14/` (ninth batch of
that directory's README). Thirteen reproduce the reviewer's `/tmp`
diagnostics on our own tree at his own `.out` line numbers; the
fourteenth (`cap14d`) the reviewer did not make, and it is the run that
settles the question finding 2 leaves open.

| Run | Copy of | Mutation | Result |
|---|---|---|---|
| `cap13a_sp2_membership_base` | `cq1c_sp2_slots_base.pv` | the slot report names the **manifest-named** slot `kfprA`/`kfprB` (as the capstone's `LayerAccepted` contract requires; `cq1c` reported `fp(kA)`), and a structural slot-to-key judge `SlotKeyWrong` added; verifier unmutated | all green: four S-P2 queries (`:481`–`:502`), `Spliced` (`:1143`), `PossessionTransplanted` (`:1150`), C-Q9 (`:1157`), three link-2b conjuncts (`:1171`, `:1185`, `:1199`), **slot-to-key `is true`** (`:1206`); witnesses reachable (`:673`, `:899`, `:1136`) |
| `cap13b_sp2_membership_unbound` | `cap13a` | **S-P2 Q4's mutation** — only slot B's `fp(kB) = kfprB` removed on the two-signer branch; every signature, possession, frame and common-content check retained | **slot-to-key `is false`** (`:1972`); **`SignerForged` reachable** (`:730`); **`PossessionTransplanted` reachable** (`:1657`, a consequence the family's Q4 model, which declares no `PossJudge`, could not record); all three link-2b conjuncts `is true` (`:1685`, `:1722`, `:1759`); `Stripped` (`:481`), `SetAltered` (`:739`), `Reattributed` (`:749`), `Spliced` (`:1398`), C-Q9 (`:1666`) green; witnesses reachable (`:922`, `:1150`, `:1389`). **Finding 1: D7's membership half needs its own companion; completeness and content companions do not sever it** |
| `cap14a_sp7_q1_strict_base` | `s-p7/proverif/sp7_q1_strict_dns_compromised.pv`, **unchanged** | none — the committed correct STRICT model re-run | all four queries green (`:560`, `:574`, `:588`, `:602`); `HonestWrappedAccepted` (`:935`), `HonestAccepted` (`:1144`) reachable |
| `cap14b_sp7_q1_strict_q6b` | `cap14a` | **Q6b's mutation transcribed onto the STRICT model** — the inner check inlined, the inner signature verified under the wrapper key `kW`, inner `kfp`/`id`/`mh` read but not matched; both outer authority checks and the same-key wrapper signer retained; DNS leaked | **every query green** — `TypeConfused` (`:541`), `Rescoped` (`:550`), `InnerSigTransplanted` (`:559`), `Reattributed` (`:568`) — and both witnesses reachable (`:843`, `:1047`). **Finding 2: in strict, with no authorized adversary wrapper key, C-C15(i) has nothing to exploit — a GREEN CONTROL** |
| `cap14c_sp7_q1_strict_repo_q6b` | `cap14b` | the same, repository channel leaked | identical, line for line (`:541`–`:1047`) |
| `cap14d_sp7_q1_strict_q6a` | `cap14a` | **Q6a's mutation transcribed onto the STRICT model** (not the reviewer's run) — the inner check inlined byte for byte, except that the scope report (and `AcceptInner`) name the **wrapper's** identity `idW` instead of the inner `idI`; key retained | **`Rescoped` reachable** (`:892`; trace `:880-892`: honest wrapper `skW2` wraps I2's honest attestation and the inner is attributed to `(pk(skI2), idW2)`, the **honest-only route**); `InnerSigTransplanted` (`:906`), `Reattributed` (`:920`), `TypeConfused` (`:558`) green; witnesses reachable (`:1185`, `:1394`). **Configuration (iii) fires in strict where (i) cannot; D11's strict discharge rests on it** |
| `cap15a_ss_q1_pairjudge_correct` | `cap12a` | the paired scope judge now compares the **`(key, identity)` pair** — conjunct 3 in its round-4 form; all checks correct | pair mismatch unreachable (`:570`), unentitled unreachable (`:998`), substitution excluded (`:563`), agreement witness reachable (`:958`); five vocabulary witnesses reachable (`:1685`–`:2775`) |
| `cap15b_ss_q1_pairjudge_identity` | `cap15a` | **identity-only** scope mutation, with a separate **key-only** judge kept as a control | **pair mismatch reachable** (`:953`) while the key-only control stays **green** (`:576`); unentitled unreachable (`:1746`); agreement witness reachable (`:1706`). *The identity comparison is what fires* |
| `cap15c_ss_q1_pairjudge_key` | `cap15a` | key-only scope mutation | pair mismatch reachable (`:947`); unentitled unreachable (`:1378`); witness reachable (`:1334`) |
| `cap15d_ss_q1_pairjudge_cc12` | `cap15a` | C-C12's mutation only | pair mismatch unreachable (`:813`); **unentitled reachable** (`:1762`); witness reachable (`:1204`) |
| `cap15e_ss_q1_pairjudge_cc12_key` | `cap15d` | C-C12's mutation plus the key-scope mutation | both reachable (`:1192`, `:2140`); witness reachable (`:1581`) |
| `cap16a_ss_q1_pairjudge_cc11_declared` | `cap15a` | **C-C11 proper** — S-STANDING Q2's mutation, the TLR names attempts by labels read from the bundle | standing correspondences red (`:766`, `:1012`, `:1696`, `:1942`, `:2188`); scope conjunct green (`:1026`); honest standing (`:2581`), agreement witness (`:1450`) and **all five vocabulary witnesses** (`:2826`, `:3067`, `:3258`, `:3497`, `:3738`) reachable |
| `cap16b_ss_q1_pairjudge_cc11_unsigned` | `cap15a` | **C-C11 alternate abl6** — the TLR unsigned | the same shape: correspondences red (`:762`–`:2156`); honest standing (`:2548`), agreement witness (`:1436`) and all five vocabulary witnesses (`:2790`–`:3665`) reachable |
| `cap16c_ss_q1_pairjudge_cc11_terminal` | `cap15a` | **C-C11 alternate Q4** — terminal disposition unchecked | correspondences red (`:810`–`:2514`); honest standing (`:2873`) and agreement witness (`:1542`) reachable; **S2 and S4 unreachable** (`:3217`, `:3413`), the other three vocabulary witnesses reachable (`:3208`, `:3404`, `:3652`). *Exactly the registered consequence, nothing else* |

**What did not change.** **No query was added or removed** — C-C17 is a
**companion**, not a query, and it adds **no timeboxed entry**, running
inside link 2a's existing 45-minute box; **no probability, no residual
decomposition and no timebox was altered**; the **26** timeboxed entries
and the **1155 min** per-case total **stand**, as does the
4 × 1155 = 4620 min ceiling and everything §3's *“What the total is, and
is not”* says about it; **the fixture is entirely unchanged**, including
the **two contestable choices** of round two, which this round again
confirms and does not reverse — finding 2's repair **carries** the
enrolment choice, the green control it registers being a consequence of
it; the ladder, the ordering and the ablation order are untouched;
§5's matrix rows, producers, consumers and expected reds are unchanged
apart from **D7's** companion and expected-red cells; the **skeptic log**
is untouched; the **review log** and the **freeze statement** are
untouched; and the routed **`REFUSAL` fork** (§8, item 1) is untouched
and **unresolved**. **What did change and is stated once here: the
companion count is now SEVENTEEN**, and every companion row in §4 and
§9 now carries a **Cases** cell.

---

## Repairs after the 2026-09-17 Codex review, sixth round

*Written by the drafting step directed by the owner instance after the
sixth non-author round,
`docs/reviews/2026-09-17-codex-review-capstone-predictions-round6.md`
(**six findings, all accepted**; the verdict was **not ready to
freeze**), whose seven dispositions at its head are this repair's
specification. **They are clerk dispositions of the owner instance, not
author rulings.** **What this round is about, stated plainly and
without hedging: the round-five repair filled the strict-case cells of
companions that had only degraded runs by READING THEIR DEGRADED
TRACES, and four of those readings were wrong** — C-C2, C-C3 and C-C8
extrapolated failed sets that the strict runs do not produce, and
C-C16's basis described a trace that does not say what the cell said it
said — **while a fifth cell, C-C7's, applied an all-green
“green control” label to configurations whose strict runs are mixed.**
**The owner instance directed that repair and accepted its judgement
calls; the error is the owner's.** The rule the file already carried is
now written into §4's preamble: **a strict outcome is descended by a
strict run or it is predicted; a reading of a degraded trace is
neither**, and **every strict cell in the file now cites a named strict
run or says “predicted” and names its basis**. Finding 1 is the one
contract defect of the round: **link 6b, as written, observed the inner
frame's own fields and could not see the attribution its own strict
companion changes**; it is restated in place as S-P7's `Rescoped` shape
transcribed unconditionally per layer over the envelope path's
attribution report, which is now declared in §1.3. **The two
contestable fixture choices of round two — same-key wrapping and the
compromised-channel-only reading of “adversary-enrolled” — stand**:
the reviewer again confirms both explicit with their alternatives and
consequences stated and reverses neither, and finding 4's repair
**carries** the enrolment choice, `cap19b` showing that the green
controls it produces are controls and not dead mutations. **The skeptic
log is untouched**, as are the review log, the freeze statement, every
probability, every residual decomposition, every timebox, the **26**
timeboxed entries, the **1155 min** per-case total, and the routed
`REFUSAL` fork, which is **not** resolved here and which the reviewer
again names, correctly, as owed at the author's commit. **The companion
count is unchanged at SEVENTEEN** — this round adds no companion, no
query and no timeboxed entry; C-C10's isolation control is a control,
on the pattern C-C8-i / C-C8-ii and C-C15(iii) already use, and runs
inside link 1a's existing box. **No capstone model exists; none was
written; none was run.** The eighteen runs below are ProVerif 2.05 runs
on **copies of committed family models** under
`formal/suite/ledger-tests-2026-09-14/` (**tenth batch** of that
directory's README), each a copy whose header states what it mutates,
each `rc=0`; fourteen are the reviewer's own `/tmp` diagnostics copied
byte for byte and re-run on our tree, landing at the reviewer's own
`.out` line numbers, and four (`*_repo`) the reviewer did not make.
**No repository model was edited or run**, and **no `.out` below is a
capstone result**.*

### Edits, by finding

| # | Finding | Edit |
|---|---|---|
| **1** | Link 6b was stated over the **inner frame's** `(issuerId, kfp)`, which C-C15(iii)'s mutation leaves entirely intact: Q6a changes only what the **envelope path attributes** the acceptance to (`cap14d_sp7_q1_strict_q6a.pv:235-245`). A literal frame-field judge stays green on the baseline (`cap19c…:587`) **and on the mutant** (`cap19d…:585`) while the mutant's `Rescoped` reds (`:933`) — so the link as written could not fail on its own registered companion | §3, **link 6b**: the **Query** sentence restated in place as S-P7's `Rescoped` shape transcribed **unconditionally, per layer**, over the envelope path's **attribution report** `(aid, lyr, kA, idA)` against the innermost frame's `(fp(kX), id)`; the old sentence **quoted**; a paragraph stating why it is **distinct from C-Q6's conjunct 3** (one path, no join, unconditional — against conjunct 3's two-path, conditional join). §1.3: **`ScopeReported` declared** in the event table beside `LayerAccepted`, as the `scopeCh` report S-P7's models already emit (`sp7_q2_degraded_compromised.pv:303`). §9(1): C-C15(iii)'s cell records that its link-6b red is now one the query can see; §4: C-C4's set (1) records that its inner-layer link-6b red survives the restatement |
| **2** | C-C2, C-C3, C-C8 and C-C16's basis extrapolated degraded failed sets to strict on **false accounts of their traces** (all three forge authority evidence over **changed** tuples: `m4_framepin_mh.out:608-616`, `sp2_q5_c2_fponly_frame_nomh.out:523-535`, `d10b_sp2_q9_manifest_unbound.out:661-673`; `cap1_sp2_content_unchecked.out:1319-1337` displays an attacker-authored tuple) | §4 **preamble**: the rule *a strict outcome is descended by a strict run or it is predicted; a reading of a degraded trace is neither* added, with the round-five error named as the owner's. **Cases cells rewritten per query**: **C-C2** and **C-C3** are **green controls in (a), descended** (`cap18a`, `cap18b`) and predicted in (b); **C-C8** is **mixed in (a), descended** — `SetAltered` green, `PossessionTransplanted` green, **C-Q9 red** (`cap18c:509`, `:1202`, `:1431`) — which is its own (α)/(β) split, carried into §9(2)'s **C-C8-i** and **C-C8-ii** cells as **predicted**; **C-C16**'s basis corrected **without withdrawing its strict red**, which reproduces by another route (`cap18d:1430`, link-2b conjuncts `:1456`, `:1468`, `:1480`); **C-C17** gains its strict descent (`cap18e:775`, `:1754`, `:2086`). **C-C9** and **C-C13** lose their `dsks`-count bases and say **predicted** with a structural basis. Every withdrawn sentence is quoted beside its replacement |
| **3** | C-C7's cell called configuration (i) a **green control** and used that reading for (ii)'s C-Q7 alone, although the definition requires **every** query green | §4, **C-C7**'s Cases cell rewritten **per query** from `cap17b` ((i): C-Q7 green `:340`, both C-Q8 red `:533`, `:709`, authorship red `:887`, unrestricted red `:1243`, witness `:1079`) and `cap17c` ((ii): `:375`, `:570`, `:748`, `:928`, `:1118`) against the matched baseline `cap17a:338`–`:358`, `:547`, `:555`; **neither configuration is a green control in any case**; the withdrawn sentences quoted; the **case-dependence of (ii)'s C-Q7** (red in the composed degraded run, green in strict) stated rather than hidden |
| **4** | “(c) as (a)/(b)” is false: case (c) leaks **both** authority keys and so supplies the very authorized wrapper key whose absence explains the (a)/(b) green controls (`cap19b:843`, `:1151`, `:1450` against `cap19a:562`–`:603`) | **Every** Cases cell that said “(c) as (a)/(b)” or “(c): red predicted” now says **“(c): not stated — (c) is C-C1's run”**, quoting the withdrawn phrase once per cell: C-C2, C-C3, C-C4, C-C5, C-C6, C-C7, C-C8, C-C9, C-C10, C-C13, C-C15(iii), C-C8-i, C-C8-ii, C-C16, C-C17. §1.1's cases table already said so. **C-C15(i)**'s cell adds `cap19b` as the **reason** its strict green is a control and not a dead mutation |
| **5** | Case (b) was labelled **descended** on runs that leak the **DNS** key only | §4, **C-C11**: (a) and (b) separated, (b) **descended** by `cap16a/b/c_…_repo`, cited at those files' own line numbers; **C-C12**: (a) descended, **(b) predicted** — the `_repo` variants made for this repair are of `cap14d` and `cap16a/b/c`, and **none is of `cap15d`**, which is C-C12's shape; §9(1), **C-C15(iii)**: (b) **descended** by `cap14d_sp7_q1_strict_q6a_repo.out:893`, and the one-run-for-two-cases label corrected in place. Everywhere else (b) says **predicted**, names **channel symmetry** as the basis, and says it is **never a second run** |
| **6** | C-C10's mutation said “the degraded verifier's evidence check removed”, while strict has **two** checks and the choice changes the outcome | §4, **C-C10**: the mutation **stated per mode** — in (d) the sole check, in (a)/(b) the **honest** channel's check deleted and the **compromised** channel's retained, with the observed evidence term named; set (1) in strict gains **link 1b** and the unrestricted `Accept ⇒ IssuerSigned` (descended `cap17e:858`, `:699`); set (2) records honest-key authorship (`:355`), C-Q7 (`:335`) and both C-Q8 (`:341`, `:347`) green with the witness reachable (`:540`); and the opposite deletion is registered as C-C10's **isolation control**, green (`cap17d:547`, `:539`, `:335`–`:355`, `:531`), so the builder cannot choose which check to delete. The withdrawn wording is quoted |
| **—** | Consequential edits, listed once so nothing is silent | §1.3: one **event-table row** added (`ScopeReported`), declaring a report the file already consumed at §3 C-Q6 (5); **no event signature changed**, `LayerAccepted`'s least of all. §3: **link 6b**'s query restated; its **prediction, probability, residual decomposition, witnesses and 45-minute timebox are untouched**. §4: the preamble gains the descent rule; **fifteen Cases cells** rewritten or amended; C-C10's mutation and set cells restated per mode. §9(1), (2), (3), (4): C-C15, C-C8-i/-ii, C-C16 and C-C17's Cases cells rewritten. **No query, companion, probability, residual or timebox is added, removed or altered anywhere** |

### Scratch runs made for this repair

All eighteen are ProVerif 2.05,
`proverif -lib formal/suite/lib/tessera_theory.pvl <copy>.pv`, `rc=0`,
on copies under `formal/suite/ledger-tests-2026-09-14/` (**tenth
batch** of that directory's README). Fourteen reproduce the reviewer's
`/tmp` diagnostics on our own tree at his own `.out` line numbers; the
four `*_repo` runs the reviewer did not make, and they are what lets
case **(b)** be descended rather than asserted.

| Run | Copy of | Mutation | Result |
|---|---|---|---|
| `cap17a_sp1_strict_judges_base` | `s-p1/proverif/sp1_q1_strict_dns_compromised.pv` | **strict** S-P1 with the C-Q7 judge, both C-Q8 judges and §1.1's same-key `OT_WRAPPER` signer added; all checks correct | all green: C-Q7 (`:338`), both C-Q8 (`:344`, `:350`), honest-key authorship (`:358`), unrestricted authorship (`:555`); witness reachable (`:547`) |
| `cap17b_sp1_strict_cc7i` | `cap17a` | **C-C7(i)** same-key byte unbinding | **C-Q7 green** (`:340`); **both C-Q8 red** (`:533`, `:709`); **honest-key authorship red** (`:887`); unrestricted red (`:1243`); witness reachable (`:1079`). *Mixed, not a green control* |
| `cap17c_sp1_strict_cc7ii` | `cap17a` | **C-C7(ii)** type-conditional byte unbinding | the same shape: C-Q7 green (`:375`); both C-Q8 red (`:570`, `:748`); authorship red (`:928`); witness reachable (`:1118`) |
| `cap17d_sp1_strict_cc10_drop_compromised` | `cap17a` | **C-C10 with the COMPROMISED channel's check removed**; a publication-provenance correspondence (link 1b's shape) added | **everything green**, including provenance (`:547`) and unrestricted authorship (`:539`); witness reachable (`:531`). *Removing the forgeable channel's check severs nothing — C-C10's isolation control* |
| ↳ *dated note, 2026-09-17 (Codex round 7 finding 2)* | — | — | **The row above is left as written, being the record of that round; this note amends it.** `cap17d` **declares no link-1a judge**, so its “everything green” is complete only over its own declared queries. Adding the structural link-1a judge over the accepted evidence and nothing else makes it **red** — `cap20f_sp1_strict_cc10_drop_compromised_evidence.out:737` (channel-specific), `cap20e_sp1_strict_cc10_drop_compromised_either.out:732` (either-key) — while provenance (`cap20e:572`, `cap20f:577`) and unrestricted authorship (`cap20e:564`) stay green and the witness stays reachable (`cap20e:556`, `cap20f:560`). **The words “*Removing the forgeable channel's check severs nothing*” are withdrawn:** the control is **mixed** — link 1a red, link 1b and the rest green (§4, C-C10, and the seventh-round repairs below). |
| `cap17e_sp1_strict_cc10_drop_honest` | `cap17a` | **C-C10 with the HONEST channel's check removed** | **provenance red** (`:858`), **unrestricted authorship red** (`:699`); honest-key authorship (`:355`), C-Q7 and both C-Q8 (`:335`, `:341`, `:347`) green; witness reachable (`:540`). *This is C-C10's strict form* |
| `cap18a_sp2_strict_cc2` | `m4_framepin_mh.pv` (C-C2's source) | the second, uncompromised authority process and check added (**strict**, DNS leaked); C-C2's mutation retained | **all green** — `Stripped` (`:411`), `SignerForged` (`:424`), `SetAltered` (`:437`), `Reattributed` (`:450`), `Spliced` (`:1129`); witnesses reachable (`:633`, `:869`, `:1116`). *C-C2 is a green control in strict* |
| `cap18b_sp2_strict_cc3` | `s-p2/proverif/sp2_q5_c2_fponly_frame_nomh.pv` (C-C3's source) | made strict the same way | **all green** (`:381`, `:388`, `:395`, `:402`); witnesses reachable (`:578`, `:809`, `:1051`). *C-C3 is a green control in strict; matches S-P2's own strict ablation d9. The model declares no `Spliced` query* |
| ↳ *dated note, 2026-09-17 (Codex round 7 finding 1)* | — | — | **The row above is left as written, being the record of that round; this note amends it.** `cap18b` **declares no C-Q9 judge**, so its “all green” is complete only over its own declared queries. Adding the registered per-slot possession report and the C-Q9 structural judge, and nothing else, makes **C-Q9 red** (`cap20a_sp2_strict_cc3_q9.out:1319`) while those four stay green (`:414`, `:422`, `:430`, `:439`) and the witnesses stay reachable (`:616`, `:848`, `:1091`); restoring possession-over-tuple with the hash guard still absent makes it green again (`cap20b…:1098`). **The words “*C-C3 is a green control in strict*” are withdrawn:** C-C3 in strict is **mixed** — C-Q5 green, C-Q9 and link 3 red (§4, C-C3, and the seventh-round repairs below). |
| `cap18c_sp2_strict_cc8` | `d10b_sp2_q9_manifest_unbound.pv` (C-C8's source) | made strict the same way | **mixed**: `SetAltered` green (`:509`), `PossessionTransplanted` green (`:1202`), **C-Q9 red** (`:1431`); the rest green (`:487`, `:498`, `:520`, `:1191`); witnesses reachable (`:701`, `:935`, `:1180`). *C-C8's (β) obligation reds in strict, its (α) does not* |
| `cap18d_sp2_strict_cc16` | `cap1_sp2_content_unchecked.pv` (C-C16's source) | made strict the same way | **`Spliced` red** (`:1430`); link-2b conjuncts green (`:1456`, `:1468`, `:1480`); the rest green; witnesses reachable (`:701`, `:942`, `:1194`). *C-C16's strict red reproduces, by a route other than cap1's displayed trace* |
| `cap18e_sp2_strict_cc17` | `cap13b_sp2_membership_unbound.pv` (C-C17's source) | made strict the same way | **`SignerForged` red** (`:775`), **`PossessionTransplanted` red** (`:1754`), **slot-to-key red** (`:2086`); link-2b conjuncts green (`:1781`, `:1813`, `:1845`); witnesses reachable (`:981`, `:1222`, `:1474`). *C-C17 reds in strict as in degraded* |
| `cap19a_sp7_strict_both_leaked_base` | `cap14a` (correct strict S-P7) | **both** channel keys leaked — case (c) | all four queries green (`:562`, `:576`, `:589`, `:603`); witnesses reachable (`:927`, `:1139`) |
| `cap19b_sp7_strict_both_leaked_q6b` | `cap14b` (Q6b on strict) | both keys leaked — C-C15(i) in case (c) | **`Rescoped`** (`:843`), **`InnerSigTransplanted`** (`:1151`), **`Reattributed`** (`:1450`) reachable; witnesses reachable (`:1728`, `:1935`). *The attacker's authorized wrapper key restores the attack; (c) is not (a)/(b)* |
| `cap19c_sp7_strict_frame_judge_base` | `cap14a` | a literal **inner-frame-field judge** added — frame identity vs tuple identity, frame fingerprint vs accepting key: link 6b as this file wrote it | judge green (`:587`); all else as `cap14a` |
| `cap19d_sp7_strict_frame_judge_q6a` | `cap14d` (Q6a on strict) | the same judge on the identity-from-outermost mutant | **judge still green** (`:585`) while **`Rescoped` red** (`:933`); witnesses reachable (`:1226`, `:1435`). *Link 6b as written cannot see the attribution Q6a changes — finding 1* |
| `cap14d_sp7_q1_strict_q6a_repo` | `cap14d` | the repository key leaked instead of the DNS key | `Rescoped` red (`:893`); `:907`, `:921`, `:558` green; witnesses (`:1186`, `:1395`). *Case (b) of C-C15(iii), descended* |
| `cap16a_ss_q1_pairjudge_cc11_declared_repo` | `cap16a` | the repository key leaked instead of the DNS key | correspondences red (`:766`, `:1012`, `:1696`, `:1942`, `:2188`); scope conjunct green (`:1026`); honest standing (`:2581`) and agreement witness (`:1450`) reachable. *Same line numbers as the DNS variant* |
| `cap16b_ss_q1_pairjudge_cc11_unsigned_repo` | `cap16b` | the repository key leaked instead of the DNS key | correspondences red (`:762`, `:1002`, `:1677`, `:1917`, `:2157`); scope conjunct green (`:1016`); honest standing (`:2549`) and agreement witness (`:1437`) reachable. **Polarities identical to the DNS variant query for query, but the line numbers are offset +1 from the third `RESULT` on** — the README's tenth-batch row says “at the same line numbers”, which holds for `cap16a_repo` and `cap16c_repo` and not for this file; its own numbers are what this file cites |
| `cap16c_ss_q1_pairjudge_cc11_terminal_repo` | `cap16c` | the repository key leaked instead of the DNS key | correspondences red (`:810`, `:1136`, `:1866`, `:2190`, `:2514`); scope conjunct green (`:1152`); honest standing (`:2873`) and agreement witness (`:1542`) reachable; **S2 and S4 unreachable** (`:3217`, `:3413`), the registered vocabulary-witness consequence. *Same line numbers as the DNS variant* |

**What did not change.** **No query was added or removed**, and **no
companion was added or removed** — the count stands at **SEVENTEEN**;
C-C10's isolation control is a **control**, on the pattern C-C8-i /
C-C8-ii and C-C15(iii) already use, and it adds **no timeboxed entry**,
running inside link 1a's existing box. **No probability, no residual
decomposition and no timebox was altered**; the **26** timeboxed
entries and the **1155 min** per-case total **stand**, as does the
4 × 1155 = 4620 min ceiling and everything §3's *“What the total is,
and is not”* says about it. **The fixture is entirely unchanged**,
including the **two contestable choices** of round two, which this
round again confirms and does not reverse — finding 4's repair
**carries** the enrolment choice, `cap19b` being the run that shows the
green controls it produces are live mutations denied their material and
not dead ones. The ladder, the ordering and the ablation order are
untouched; §5's matrix rows, producers, consumers and expected reds are
unchanged; **link 6b's prediction, probability, residual decomposition,
witnesses and timebox are untouched** — only its **query sentence** is
restated, and `LayerAccepted`'s signature is not touched at all. The
**skeptic log** is untouched; the **review log** and the **freeze
statement** are untouched; and the routed **`REFUSAL` fork** (§8,
item 1) is untouched and **unresolved**, owed at the author's commit.
**What did change and is stated once here: every strict-case outcome in
this file now cites a named strict run, or says “predicted” and names
its basis.**

---

## Repairs after the 2026-09-17 Codex review, seventh round

*Written by the drafting step directed by the owner instance after the
seventh non-author round,
`docs/reviews/2026-09-17-codex-review-capstone-predictions-round7.md`
(**two findings, both accepted**; the verdict was **not ready to
freeze**), whose three dispositions at its head are this repair's
specification. **They are clerk dispositions of the owner instance, not
author rulings**, and disposition 2 fixes one **contract term** — what
`ev` is in strict — which is marked **CONTESTABLE** and is the author's
to overrule at the freeze commit. **What this round is about, stated
plainly: two cells were read as all-green controls off family copies
that DECLARE NO SUCH QUERY.** `cap18b` (C-C3 in strict) declares no
C-Q9 judge; `cap17d` (C-C10's isolation control) declares no link-1a
judge. Adding the missing judge and changing nothing else **reds each**
— C-Q9 `is false` at `cap20a_sp2_strict_cc3_q9.out:1319`, link 1a
`is false` at `cap20f_sp1_strict_cc10_drop_compromised_evidence.out:737`
and `cap20e_sp1_strict_cc10_drop_compromised_either.out:732`. Both cells
are now **mixed**, both name their reds, and the class rule is written
into §4's preamble in the disposition's own words: **a family copy's
declared queries are not the capstone's query set.** **The owner
instance directed the round-six repair that wrote those two cells; the
error is the owner's**, not the reviewer's and not the file's earlier
drafters'. The reviewer **confirms the round-six repairs** — the
attribution-based link 6b, the case-(b) descents, the case-(c)
withdrawal, the mixed C-C7 and C-C8 cells — **and all twenty-four
earlier accepted findings except these two cells**. **The two
contestable fixture choices of round two — same-key wrapping and the
compromised-channel-only reading of "adversary-enrolled" — stand**,
confirmed again and reversed neither. **The skeptic log is untouched**,
as are the review log, the freeze statement, every probability, every
residual decomposition, every timebox, the **26** timeboxed entries and
the **1155 min** per-case total; and the routed **`REFUSAL` fork** is
**not** resolved here — the reviewer again names it, correctly, as the
existing author decision owed at the author's commit, not a newly
invented defect. **The companion count is unchanged at SEVENTEEN** —
this round adds no companion, no query and no timeboxed entry; C-C10's
isolation control remains a **control**, running inside link 1a's
existing box. **No capstone model exists; none was written; none was
run.** The seven runs below are ProVerif 2.05 runs on **copies of
committed family models** under `formal/suite/ledger-tests-2026-09-14/`
(**eleventh batch** of that directory's README), each `rc=0`, all seven
the reviewer's own `/tmp` diagnostics copied byte for byte under a
provenance header and re-run on our tree, landing at the reviewer's own
`.out` line numbers. **No repository model was edited or run**, and **no
`.out` below is a capstone result**. The round-six records are **amended
by dated notes under their rows**, not rewritten: rows 2 and 6 of that
round's "Edits, by finding" table stand as the record of what that round
did, and the two scratch rows they rest on now carry their corrections.*

### Edits, by finding

| # | Finding | Edit |
|---|---|---|
| **1** | C-C3's strict case (a) was registered **GREEN CONTROL, DESCENDED** off `cap18b`, which **declares neither C-Q9 nor a possession-binding judge**, while C-C3's own failed set names **C-Q9** and **link 3**. The mutation produces and accepts `(POSS, fp(kX))` where both require `(POSS, t)`, and strict authority verification does not repair that structural mismatch | §4, **C-C3**'s Cases cell rewritten: **(a) MIXED, DESCENDED** — C-Q5 and the other three safety queries green (`cap20a:430`, `:414`, `:422`, `:439`; witnesses `:616`, `:848`, `:1091`), **C-Q9 and link 3 red** (`cap20a:1319`), with the isolation showing the red is the **fingerprint-only possession** and not the missing hash guard (`cap20b:1098`, safety `:414`–`:438`, witnesses `:615`, `:847`, `:1090`); **(b) mixed, PREDICTED** on channel symmetry; **(c)** unchanged, not stated. The “green control, DESCENDED” wording is **withdrawn and quoted** in the cell, and the `Spliced`-only set-completeness note is replaced: `cap18b` declares **neither `Spliced` nor C-Q9**, **C-Q9 is now descended** by `cap20a`, **`Spliced` stays predicted**. §4 **preamble** gains the class rule verbatim from the disposition. The round-six scratch table's `cap18b` row keeps its text and gains a **dated note** withdrawing “*C-C3 is a green control in strict*” |
| **2** | C-C10's isolation control (the **compromised** channel's check deleted) was registered **green** and said to “sever nothing”, off `cap17d`, which **declares no link-1a judge**. In that control the verifier checks the retained term while the acceptance carries the unchecked one, so an attacker can retain a valid tuple and its honest-channel evidence and replace the carried `ev`. The **evidence-selection contract** was unspecified for two channels | §1.3: `ev` stated as the **pair** in strict, the sole term in degraded, with the old phrase quoted and the term marked **CONTESTABLE**; `LayerAccepted`'s signature is **not** changed. §3, **link 1a**: the **per-channel** form stated — each carried term verifies over the consumed `t` under **its own** channel key, including the non-verifying case — with the baseline greens cited (`cap20d:589` channel-specific, `cap20c:585` either-key) and the contestable choice given its one-line reason. §4, **C-C10**: set (1) gains **link 1a descended** (`cap20g:1055`, beside `:887` and `:728`) where it said “not descended”, quoted; the Cases cell's isolation control becomes **MIXED** — link 1a **red** (`cap20f:737`, `cap20e:732`), link 1b and unrestricted authorship **green** (`cap17d:547`, `:539`; `cap20e:572`, `:564`), witness reachable (`cap20e:556`, `cap20f:560`) — with “severs nothing” and “REGISTERED AND GREEN” withdrawn and quoted, and the distinguishing signal restated: **link 1b red ⇒ the honest check was deleted** (the companion, `cap20g:887`, `:728`, `:1055`); **link 1b green and link 1a red ⇒ the compromised check was** (the control). The round-six scratch table's `cap17d` row gains a **dated note** withdrawing “*severs nothing*” |
| **—** | Consequential edits, listed once so nothing is silent | §1.3: the `ev` gloss amended in place and one paragraph added; **no event signature changed**. §3, **link 1a**: one paragraph added to the **query**; its **prediction, probability, residual decomposition, witnesses and 45-minute timebox are untouched**. §4: one **preamble paragraph** (the class rule) and the two Cases cells above; **no row, no column and no companion added**. §9(2): **no edit** — C-C8-i and C-C8-ii carry **C-C8's own** strict split from `cap18c`, not C-C3's cell, so nothing there rested on the withdrawn reading. The round-six section: **two dated note rows**, no row rewritten |

### Scratch runs made for this repair

All seven are ProVerif 2.05,
`proverif -lib formal/suite/lib/tessera_theory.pvl <copy>.pv`, `rc=0`,
on copies under `formal/suite/ledger-tests-2026-09-14/` (**eleventh
batch** of that directory's README). All seven reproduce the reviewer's
`/tmp/tessera-capstone-r7/` diagnostics on our own tree at his own
`.out` line numbers. None is an S-P1, S-P2 or capstone result.

| Run | Copy of | Mutation | Result |
|---|---|---|---|
| `cap20a_sp2_strict_cc3_q9` | `cap18b_sp2_strict_cc3.pv` (C-C3 strict) | the per-slot possession report and the **C-Q9 structural judge** (`PossessionUnbound`) added; fixture and verifier unchanged | **C-Q9 red** (`:1319`) while `Stripped`, `SignerForged`, `SetAltered`, `Reattributed` stay green (`:414`, `:422`, `:430`, `:439`); witnesses reachable (`:616`, `:848`, `:1091`). *C-C3 in strict is mixed: (α) set integrity green, (β) possession-message relation red* |
| `cap20b_sp2_strict_cc3_q9_poss_restored` | `cap20a` | possession-over-tuple **restored**; the frame's manifest-hash guard still absent | **C-Q9 green** (`:1098`); the four safety queries green (`:414`–`:438`); witnesses reachable (`:615`, `:847`, `:1090`). *The red is the fingerprint-only possession, not the missing hash guard* |
| `cap20c_sp1_strict_base_evidence_either` | `cap17a_sp1_strict_judges_base.pv` | a structural **link-1a judge** over the accepted evidence term, accepting evidence that verifies over the consumed tuple under **either** authority key | judge green (`:585`); all else as `cap17a` (`:362`–`:382`, `:571`, `:579`) |
| `cap20d_sp1_strict_base_evidence` | `cap17a` | the same judge in its **channel-specific** form (each carried term under its own channel key) | judge green (`:589`); all else as `cap17a`. *The baseline does not separate the two forms; the channel-specific one is registered* |
| `cap20e_sp1_strict_cc10_drop_compromised_either` | `cap17d_sp1_strict_cc10_drop_compromised.pv` (C-C10's isolation control) | the either-key link-1a judge added | **link-1a judge red** (`:732`) while publication provenance (`:572`) and unrestricted authorship (`:564`) stay green; witness reachable (`:556`). *The control is mixed, not green* |
| `cap20f_sp1_strict_cc10_drop_compromised_evidence` | `cap17d` | the channel-specific link-1a judge added | **red** (`:737`); provenance green (`:577`); witness reachable (`:560`) |
| `cap20g_sp1_strict_cc10_drop_honest_evidence` | `cap17e_sp1_strict_cc10_drop_honest.pv` (C-C10's strict form) | the channel-specific link-1a judge added | **link 1a red** (`:1055`) beside link 1b (`:887`) and unrestricted authorship (`:728`) red; honest-key authorship (`:384`), C-Q7 and both C-Q8 (`:364`–`:376`) green; witness reachable (`:569`). *This is what descends link 1a for C-C10* |

**What did not change.** **No query was added or removed**, and **no
companion was added or removed** — the count stands at **SEVENTEEN**;
C-C10's isolation control remains a **control**, on the pattern C-C8-i /
C-C8-ii and C-C15(iii) already use, and it adds **no timeboxed entry**,
running inside link 1a's existing box. **No probability, no residual
decomposition and no timebox was altered**; the **26** timeboxed entries
and the **1155 min** per-case total **stand**, as does the
4 × 1155 = 4620 min ceiling and everything §3's *"What the total is, and
is not"* says about it. **`LayerAccepted`'s signature is untouched** —
what changed is what its `ev` argument denotes in strict, and that is a
**contestable** clerk disposition, not an author ruling. **The fixture is
entirely unchanged**, including the **two contestable choices** of round
two, which this round again confirms and does not reverse. The ladder,
the ordering and the ablation order are untouched; §5's matrix rows,
producers, consumers and expected reds are unchanged; §9's cells are
unchanged. The **skeptic log** is untouched; the **review log** and the
**freeze statement** are untouched; and the routed **`REFUSAL` fork**
(§8, item 1) is untouched and **unresolved**, owed at the author's
commit. **What did change and is stated once here: no cell in this file
now calls a configuration a green control over queries the cited copy
does not declare.**

**DATED NOTE, 2026-09-17 (Codex round 8, finding 2).** *The sentence
immediately above is **withdrawn**, and quoted here rather than removed:
“**What did change and is stated once here: no cell in this file now
calls a configuration a green control over queries the cited copy does
not declare.**”* **It was false when written.** Two cells still carried
the label off copies declaring none of the queries at issue — **C-C2**
case (a), off `cap18a_sp2_strict_cc2.pv:145-176` (five queries and three
witnesses; no C-Q8, no C-Q9, no link-2b judge), and **C-C15(i)** cases
(a)/(b), off `cap14b_sp7_q1_strict_q6b.pv:113-130` and
`cap14c_sp7_q1_strict_repo_q6b.pv:113-130` (four S-P7 queries and two
witnesses; no generic C-Q7, no structural C-Q8 or C-Q9, no linkage
judge). **The round-seven section is otherwise not rewritten**: rows 1
and 2 of its “Edits, by finding” table and its seven scratch rows stand
as the record of what that round did. What replaces the withdrawn claim
is not a stronger claim of the same kind but the **retirement of the
label**, entered in §4's preamble and applied to every Cases cell; the
round-eight section below records it.

## Repairs after the 2026-09-17 Codex review, eighth round

*Written by the drafting step directed by the owner instance after the
eighth non-author round,
`docs/reviews/2026-09-17-codex-review-capstone-predictions-round8.md`
(**two findings, both accepted**; the verdict was **not ready to
freeze**), whose three dispositions at its head are this repair's
specification. **They are clerk dispositions of the owner instance, not
author rulings.** **What this round is about, stated plainly.** Finding 1
is a **result**: C-C5's strict cases (a)/(b) were offered as a possible
**green control** on the ground that the degraded trace runs the `dsks`
route, which strict authority denies. That ground is sound for
`InnerSigTransplanted` and says nothing about **C-Q8 and link 4**, whose
structural relation an **honestly authorized** key can break — and it
does: with C-Q8's structural judge added and restricted to wrapped inner
acceptances, the strict baseline is green
(`cap21b_sp7_strict_base_sigbytes_wrapped.out:594`) and C-C5's unbinding
reds the judge in **both** channel variants
(`cap21d_sp7_strict_cc5_wrapped.out:869`,
`cap21e_sp7_strict_cc5_wrapped_repo.out:868`) while the four S-P7 safety
queries stay green and both witnesses stay reachable. The attack carries
the issuer's **honest wrapper signature, under its honestly authorized
key**, as the **inner** signature for attacker-built attestation bytes:
the same-key-wrapping consequence **C-C7(ii)** already records, now at
the inner layer, and **no adversary-enrolled key is needed**. C-C5's
strict outcome is **mixed, descended**, and the whole-configuration
green-control alternative is withdrawn and quoted in the cell. Finding 2
is a **class**: C-C2 and C-C15(i) still carried “green control,
descended” off copies declaring none of C-Q7/C-Q8/C-Q9 or the linkage
conjuncts, and the round-seven section's closing claim that no other cell
had the omission was **false** and is withdrawn, quoted, in a dated note
under that section. **Rounds five through eight have every one of them
been this same class**, so the disposition retires the label rather than
repairing one more cell: **“green control, descended” is no longer a
label this file uses for a whole configuration.** Every Cases cell now
states its strict outcome **per query** in three lists — **descended
green** (naming the run), **descended red** (naming the run),
**predicted** (naming the basis) — and “green control” survives only as
a **predicted** configuration-level reading beside those lists.
**The owner instance directed the round-five, round-six and round-seven
repairs that wrote these cells; the error is the owner's**, not the
reviewer's and not the file's earlier drafters'. **The reviewer's own
limit is carried:** he established **missing coverage**, not that the
unqueried relations are false, and no prediction is flipped to red on
his account — only finding 1's two reds are, and those are run.
**The three contestable choices stand** — same-key wrapping, the
compromised-channel-only reading of “adversary-enrolled”, and `ev` as
the pair in strict — confirmed again and reversed by neither finding;
finding 1 is a **consequence** the enrolment argument does not exclude,
which is exactly what the reviewer says of it. **The skeptic log is
untouched**, as are the review log, the freeze statement, every
probability, every residual decomposition, every timebox, the **26**
timeboxed entries and the **1155 min** per-case total; and the routed
**`REFUSAL` fork** (§8, item 1) is **not** resolved here — the reviewer
again names it, correctly, as the existing author decision owed at the
author's commit, not a newly invented defect. **The companion count is
unchanged at SEVENTEEN** — this round adds no companion, no query, no
configuration and no timeboxed entry. **No capstone model exists; none
was written; none was run.** The five runs below are ProVerif 2.05 runs
on **copies of committed family models** under
`formal/suite/ledger-tests-2026-09-14/` (**twelfth batch** of that
directory's README), each `rc=0`, all five the reviewer's own
`/tmp/tessera-capstone-r8/` diagnostics copied **byte for byte** under a
provenance header and re-run on our tree, landing at the reviewer's own
`.out` line numbers. **No repository model was edited or run**, and **no
`.out` below is a capstone result**. The earlier repair sections are
**amended by dated notes**, not rewritten: the round-seven section keeps
its text and carries the withdrawal of its closing sentence.*

### Edits, by finding

| # | Finding | Edit |
|---|---|---|
| **1** | C-C5's strict green-control alternative overlooks a **same-key byte-binding failure**. The `dsks` argument protects `InnerSigTransplanted`; it does not protect **C-Q8** or **link 4** against substitution under an **honestly authorized** key | §4, **C-C5**'s Cases cell: (a) and (b) rewritten to **MIXED, DESCENDED**. **Descended red** — C-Q8's structural judge, `cap21d:869` in (a) and `cap21e:868` in (b), with **link 4 red by shape**, `ChainBroken` being declared in no model (the `cap20a`/`cap13b` pattern). **Descended green** — `InnerSigTransplanted` (`cap21d:956`; `cap21e:954`), `Rescoped` (`:927`; `:926`), `TypeConfused` (`:898`; `:897`), C-Q3 `Reattributed` (`:985`; `:982`); **witnesses reachable** (`:1336`, `:1563`; `:1333`, `:1559`); **matched strict baseline green on the same judge** (`cap21b:594`). **Predicted** — `VersionLied`, links 6a/6b and the rest of the retained column, `cap21b`/`cap21d`/`cap21e` declaring only C-Q8's judge, four S-P7 queries and two witnesses (`cap21d_sp7_strict_cc5_wrapped.pv:126-145`). **The attack is stated in the cell**; the green-control passage is **withdrawn and quoted**. Set (1) already listed C-Q8 and link 4 and is **unchanged**; what is new is that they are **descended in strict**. §4, **C-C6**: a dated qualification — C-C6's waiver keys on the signed frame's own `kfp`, which the wrapper frame names (`cap7c:448` matching `d5d:414`), so the same honest-wrapper material is available to it; the green-control reading there is **weakened to “predicts neither colour”**, not withdrawn |
| **2** | C-C2 and C-C15(i) still claimed **descended green controls** from copies missing capstone queries they can carry, and the round-seven section's claim that no other cell did was false | §4 **preamble**: one paragraph retiring **“green control, descended” as a label for a whole configuration**, in the disposition's own words, with the two mechanical consequences restated and the round-five paragraph's “shown instance” sentence **withdrawn and quoted**. **Every Cases cell in the file** rewritten into the three lists (see the consequential row). **C-C2** (a): “GREEN CONTROL, DESCENDED” **withdrawn and quoted**; descended green on the **five** queries and **three** witnesses `cap18a_sp2_strict_cc2.pv:145-176` declares; C-Q8, C-Q9, link 2b and every other linkage conjunct **predicted**. **C-C15(i)** (a)/(b): “GREEN CONTROL … DESCENDED” **withdrawn and quoted**; descended green on the **four** S-P7 queries and **two** witnesses `cap14b_sp7_q1_strict_q6b.pv:113-130` and `cap14c_sp7_q1_strict_repo_q6b.pv:113-130` declare; **C-Q7, C-Q8, C-Q9 and the linkage conjuncts predicted green with the basis stated** — the inner signature is verified under `kW` over `fbI` **with byte binding retained**, so finding 1's route does not open. The **round-seven** section gains a **dated note** withdrawing its closing sentence |
| **—** | Consequential edits, listed once so nothing is silent | **Nineteen Cases cells** now carry the three lists: §4's table — **C-C1, C-C2, C-C3, C-C4, C-C5, C-C6, C-C7, C-C8, C-C9, C-C10** (companion **and** isolation control); the unnumbered table — **C-C11, C-C12**; §9(1) — **C-C13, C-C14, C-C15** in all three configurations; §9(2) — **C-C8-i, C-C8-ii**; §9(3) — **C-C16**; §9(4) — **C-C17**. §9(1), **C-C15**'s **Row** column: the phrase “(i) being a **green control** there” **withdrawn and quoted**, replaced by the per-query statement; **D11's discharge is unchanged** — in (a)/(b) it still rests on configuration (iii). §4, **C-C4**: the cross-reference to C-C15(i) as the shown instance is amended in place. **No query, no companion, no configuration, no probability, no residual decomposition and no timebox was added, removed or altered**; **no row and no column was added to any table**; §1.1, §1.2, §1.3, §2, §3, §5, §6, §7 and §8 are **untouched** |

### Scratch runs made for this repair

All five are ProVerif 2.05,
`proverif -lib formal/suite/lib/tessera_theory.pvl <copy>.pv`, `rc=0`,
on copies under `formal/suite/ledger-tests-2026-09-14/` (**twelfth
batch** of that directory's README). All five reproduce the reviewer's
`/tmp/tessera-capstone-r8/` diagnostics on our own tree at his own
`.out` line numbers. None is an S-P7 result and none is a capstone
result.

| Run | Copy of | Mutation | Result |
|---|---|---|---|
| `cap21a_sp7_strict_base_sigbytes` | `cap14a_sp7_q1_strict_base.pv` (correct strict S-P7) | **C-Q8's structural signature/bytes judge** (`BytesUnbound`) added over every accepted `(key, signature, presented bytes)` triple; nothing else | judge green (`:592`); the four S-P7 queries green (`:606`–`:648`); witnesses reachable (`:981`, `:1190`) |
| `cap21b_sp7_strict_base_sigbytes_wrapped` | `cap21a` | the judge **restricted to wrapped inner acceptances** (the report carries the wrapper context) | judge green (`:594`); the rest as `cap21a` (`:610`–`:658`, `:993`, `:1204`). *This is C-C5's matched strict baseline* |
| `cap21c_sp7_strict_cc5` | `cap21a` | **C-C5's mutation**: `let (=BYTES, =fbI) = checksign(sgI, kI)` becomes `let (=BYTES, anyb) = …` inside `InnerCheck`; strict, DNS leaked | **judge red** (`:808`) while `TypeConfused`, `Rescoped`, `InnerSigTransplanted`, `Reattributed` stay green (`:832`–`:904`); witnesses reachable (`:1250`, `:1472`) |
| `cap21d_sp7_strict_cc5_wrapped` | `cap21b` | C-C5's mutation, judge restricted to wrapped inner acceptances | **judge red** (`:869`); the four S-P7 queries green (`:898`, `:927`, `:956`, `:985`); witnesses reachable (`:1336`, `:1563`). *In strict, C-C5 reds C-Q8/link 4 through an honest wrapper signature under an honestly authorized key; `InnerSigTransplanted` stays green. Mixed, not a green control — **case (a), descended*** |
| `cap21e_sp7_strict_cc5_wrapped_repo` | `cap21d` | the repository key leaked instead of the DNS key | the same: judge red (`:868`); S-P7 queries green (`:897`–`:982`); witnesses reachable (`:1333`, `:1559`). *Case (b), descended* |

**What did not change.** **No query was added or removed**, and **no
companion and no configuration was added or removed** — the count stands
at **SEVENTEEN**, C-C8-i/C-C8-ii and C-C10's isolation control remain
**controls**, and C-C15(iii) remains C-C15's isolation configuration.
**No probability, no residual decomposition and no timebox was altered**;
the **26** timeboxed entries and the **1155 min** per-case total
**stand**, as does the 4 × 1155 = 4620 min ceiling and everything §3's
*“What the total is, and is not”* says about it. **The fixture is
entirely unchanged**, including the **three contestable choices** —
same-key wrapping, compromised-channel-only enrolment, and `ev` as the
pair in strict — which this round again confirms and reverses in no
part; `LayerAccepted`'s signature is untouched. The ladder, the
ordering, the ablation order and §5's matrix rows, producers, consumers
and expected reds are unchanged. **No set (1), set (2) or set (3)
membership changed**: C-C5's set (1) already named C-Q8 and link 4, and
what this round adds is that they are **descended in strict** rather
than predicted there. The **skeptic log** is untouched; the **review
log** and the **freeze statement** are untouched; and the routed
**`REFUSAL` fork** (§8, item 1) is untouched and **unresolved**, owed at
the author's commit. **What did change and is stated once here: this
file no longer has a label that lets a family copy's all-green `.out`
stand in for the capstone's query set — every strict colour in every
Cases cell is now either DESCENDED, and names its run, or PREDICTED, and
names its basis.**

**DATED NOTE, 2026-09-17 (Codex round 9, disposition 4).** *The C-C6
clause of row 1 of the table above is **superseded**, and quoted here
rather than removed: “§4, **C-C6**: a dated qualification — C-C6's waiver
keys on the signed frame's own `kfp`, which the wrapper frame names
(`cap7c:448` matching `d5d:414`), so the same honest-wrapper material is
available to it; the green-control reading there is **weakened to
“predicts neither colour”**, not withdrawn.”* **The inference was
backwards.** C-C6 waives byte equality **only when the signed frame's
`kfp` does NOT match the verifying key**, and the same-key wrapper frame
**does** name it — so on that route equality is **demanded** and C-C5's
strict failure does **not** reproduce. The reviewer built and ran the
test this file asked for: on the strict S-P7 copy with the wrapped
byte-binding judge and same-key wrapping retained, **every declared
query is green and both witnesses are reachable** in both channel
variants (`cap22b_sp7_strict_cc6.out:692`, `:722`, `:752`, `:782`,
`:812`, `:1161`, `:1386`; `cap22c_sp7_strict_cc6_repo.out:693`–`:817`,
`:1167`, `:1393`). C-C6's cell now carries **descended green** on those
five queries and two witnesses, with C-Q7 and the linkage conjuncts
**predicted green** and a **predicted** green control at configuration
level; “predicts neither colour” is withdrawn and quoted there. **Row 2
and the consequential row of the table above, and its five scratch rows,
stand as the record of what round eight did**, and finding 1's C-C5 result — the substance
of that round — is **not** disturbed: C-C5 unbinds the inner signature
from the presented bytes and C-C6 does not, which is the whole
difference.

## Repairs after the 2026-09-17 Codex review, ninth round

*Written by the drafting step directed by the owner instance after the
ninth non-author round,
`docs/reviews/2026-09-17-codex-review-capstone-predictions-round9.md`
(**three findings, all accepted, plus the requested C-C6 test**; the
verdict was **not ready to freeze**), whose five dispositions at its head
are this repair's specification. **They are clerk dispositions of the
owner instance, not author rulings.** **What this round is about, stated
plainly.** Finding 1 is a **builder gap that changes a result**: what an
inner acceptance **reports** to the judges, under a companion that stops
checking a term, was never specified — and the two readings give
opposite colours on the same verifier. C-C15(i)'s strict transcription
checks the outer possession proof and verifies the inner signature under
`kW`, never touching the presented inner `tI` or `ppfI`; with the C-Q9
judge added and the inner acceptance reporting the **presented inner**
terms, C-Q9 is **red** in both channel variants
(`cap22e_sp7_strict_q6b_q9_inner.out:1334`;
`cap22f_sp7_strict_q6b_q9_inner_repo.out:1334`), and reporting the
**checked outer** terms instead makes it **green**
(`cap22g_sp7_strict_q6b_q9_outer.out:1084`). The term is fixed in §1.3
as **the report contract**: a layer's report carries **the terms that
layer's acceptance was about**, never terms checked at another layer.
**That term is CONTESTABLE — the FOURTH contestable choice in this
file**, joining same-key wrapping, the compromised-channel-only reading
of "adversary-enrolled" and `ev` as the pair in strict, and it is owed to
the author at the freeze commit with the other three. Its consequence is
recorded where it falls: **C-C15(i)'s C-Q9 and link 3 move from
predicted green to descended red in (a) and (b)**, and the outer-report
reading is kept as the **rejected alternative** with `cap22g` as its
evidence. Finding 2 is a **contradicted prediction**: C-C8's strict cell
claimed link 5's `mh` half red "descended by `cap18c`'s C-Q9 judge", but
C-Q9 tests the **possession message**, not the frame's manifest hash — a
direct `mh ≠ h(t)` judge is **green** on the strict mutant in both
variants (`cap22h:1478`; `cap22i:1477`) and **red** on the degraded
source (`cap22j:1665`), because in strict the honest channel's tuple pin
keeps `mh = h(t)` even with the guards dropped. Finding 3 is a **swapped
citation**, corrected at the same polarity. **Nothing in this round
flips a colour the runs do not show**, and the reviewer's own limit is
carried: finding 1 establishes a **choice**, not an unconditional
counterexample to every possible transcription. **The skeptic log is
untouched**, as are the review log, the freeze statement, every
probability, every residual decomposition, every timebox, the **26**
timeboxed entries and the **1155 min** per-case total; and the routed
**`REFUSAL` fork** (§8, item 1) is **not** resolved here — the reviewer
again names it, correctly, as the existing author decision owed at the
author's commit. **The companion count is unchanged at SEVENTEEN** —
this round adds no companion, no query, no configuration and no
timeboxed entry. **No capstone model exists; none was written; none was
run.** The ten runs below are ProVerif 2.05 runs on **copies of
committed family models** under `formal/suite/ledger-tests-2026-09-14/`
(**thirteenth batch** of that directory's README), each `rc=0`, all ten
the reviewer's own `/tmp/tessera-capstone-r9/` diagnostics copied **byte
for byte** under a provenance header and re-run on our tree, landing at
the reviewer's own `.out` line numbers. **No repository model was edited
or run**, and **no `.out` below is a capstone result**. The earlier
repair sections are **amended by dated notes**, not rewritten: the
round-eight section keeps its text and carries the supersession of its
finding-1 C-C6 clause.*

### Edits, by finding

| # | Finding | Edit |
|---|---|---|
| **1** | Under a companion, **which terms an inner acceptance reports** is an unspecified builder choice that **changes C-Q9's result**. C-C15(i) never checks the presented inner `tI` or `ppfI`; reporting them reds C-Q9, reporting the checked outer terms greens it | §1.3, a new paragraph after the `ev`-pair paragraph: **THE REPORT CONTRACT UNDER COMPANIONS** — under every companion, `LayerAccepted` and every judge report at a layer carry **the presented `(t, ppf, sg, fb)` of that layer under the key the (mutated) verifier verified against**, never terms checked at another layer; said to be what the immutable join already requires (`t = tI`, `ppf = ppfI`, §3 C-Q6 (3)), and stated so a builder cannot make a companion's failure invisible by reporting what the verifier did check. **Marked CONTESTABLE, the fourth such choice**, with its reason in one line. Cites `cap22e:1334`, `cap22f:1334` (presented inner reported, C-Q9 red), `cap22g:1084` (checked outer reported, green — the rejected reading), baseline `cap22d:1186`. §9(1), **C-C15**'s Cases cell, configuration (i): **C-Q9 and link 3 move from predicted green to DESCENDED RED in (a) and (b)** (`cap22e:1334`; `cap22f:1334`; the four S-P7 queries still green `:569`–`:596`; witnesses `:871`, `:1075`); link 3 red **by shape**, its relation being C-Q9's; the “predicted green … C-Q9” wording **withdrawn and quoted**; the round-eight sentence saying finding 1's route does not open **half withdrawn and quoted** — **its C-Q8 half is retained and still true**, byte binding being retained here; `cap22g` recorded as the **rejected reading**; the round-eight “Descended red: NONE.” withdrawn for (i). §9(1), C-C15's **Row** column: the D11 phrase amended in place, **D11's discharge in (a)/(b) still resting on configuration (iii)** |
| **2** | **C-C8's strict `mh` prediction is contradicted by a direct judge.** C-Q9 tests the possession message, not the frame's manifest hash, so it cannot descend the `mh` relation | §4, **C-C8**'s Cases cell: link 5's `mh` half → **DESCENDED GREEN** in (a) (`cap22h_sp2_strict_cc8_mh.out:1478`) and (b) (`cap22i_sp2_strict_cc8_mh_repo.out:1477`), C-Q9 red beside it (`:1466`, `:1465`), the rest green (`:512`, `:524`, `:536`, `:549`/`:548`, `:1224`/`:1223`, `:1236`/`:1235`) and witnesses reachable (`:731`, `:966`, `:1212`; `:730`, `:965`, `:1211`), so **(b) is descended in its own right**; the **degraded control red** (`cap22j:1665`, with `SetAltered` `:701` and C-Q9 `:1499`), which is what makes the strict green a result. “link 3 and link 5's `mh` half red … descended by `cap18c`'s C-Q9 judge” **withdrawn and quoted**; **link 3 stays descended red**, its relation being C-Q9's; the reason stated — the honest channel's tuple pin keeps `mh = h(t)` in strict even with the guard dropped; the **(β)-only strict split** stated as what the runs show. §9(2), **C-C8-i**: a dated note carrying the same result as an a fortiori **predicted** green, still undescended; **C-C8-ii** unaffected |
| **3** | **C-C7(i)'s two C-Q8 citations are swapped**: `:533` is `SigBytesUnbound`, `:709` is `SigBytesUnboundAll` | §4, **C-C7**'s Cases cell: the attributions **exchanged** in the three-lists entry, the withdrawn wording quoted, both `.out` lines transcribed verbatim, and it recorded that **both are red, so the polarity is unchanged and no prediction moves**. The round-six and round-eight repair sections were checked: neither attributes `:533` or `:709` to a form — the round-six edit row and its `cap17b` scratch row both read “both C-Q8 red (`:533`, `:709`)” — so **neither repeats the error and neither needs a note** |
| **4** | **C-C6, the requested test.** Every declared query green and both witnesses reachable, in both strict variants | §4, **C-C6**'s Cases cell: **descended green** on the five declared queries (`cap22b:692`, `:722`, `:752`, `:782`, `:812`) and two witnesses (`:1161`, `:1386`) in (a), and the same in (b) (`cap22c:693`–`:817`, `:1167`, `:1393`), against the matched baseline `cap22a:594`–`:658`; **descended red: NONE**; **C-Q7 and the linkage conjuncts predicted green**, the copies declaring five queries and two witnesses and nothing else; a **PREDICTED** green control at configuration level, never a descended one. “this cell predicts neither colour” **withdrawn and quoted**, and the round-eight **weakened-reading paragraph withdrawn and quoted in full**, with the reason: C-C6's waiver keys on the signed frame's own `kfp`, which the same-key wrapper frame **does** name, so equality is demanded on that route and C-C5's strict failure does not reproduce. Set (1) is **not edited**: C-Q7 and `InnerSigTransplanted` remain (d)'s registered reds and their strict green is a **registered per-case outcome** |
| **—** | Consequential edits, listed once so nothing is silent | §4, **C-C4**, §9(1), **C-C13**, and §9(1), **C-C15** configurations **(ii)** and **(iii)**: one sentence each stating, under §1.3's contract, **which terms the inner acceptance reports under that mutation** and whether any predicted outcome changes — in all four, **none does**, and in all four the reported terms are the terms that verifier still checks, which is what distinguishes them from C-C15(i). §4, **C-C8-i** (§9(2)): the dated note of finding 2. The **round-eight section**: a **dated note** superseding its finding-1 C-C6 clause, its other rows standing. **No query, no companion, no configuration, no probability, no residual decomposition and no timebox was added, removed or altered**; **no row and no column was added to any table**; §1.1, §1.2, §2, §5, §6, §7 and §8 are **untouched**, and §1.3 gains one paragraph and no change to `LayerAccepted`'s signature |

**Note, 2026-09-17 (Codex round 10 finding 1).** Finding 1's consequence above is **carried further** by the tenth round: under the same report contract, C-C15(i) also reds **links 1a, 1b, 2a, link 5's `mh` half and C-Q5** in cases (a) and (b) (`cap23d_sp7_strict_q6b_observers_tuple.out:2573`, `:1735`, `:2297`, `:2017`, `:2883`; `cap23f…` at the same lines). The rows above **stand as written**; what moved is **extended**, not corrected — the round-ten section records it.

### Scratch runs made for this repair

All ten are ProVerif 2.05,
`proverif -lib formal/suite/lib/tessera_theory.pvl <copy>.pv`, `rc=0`,
on copies under `formal/suite/ledger-tests-2026-09-14/` (**thirteenth
batch** of that directory's README). All ten reproduce the reviewer's
`/tmp/tessera-capstone-r9/` diagnostics on our own tree at his own
`.out` line numbers. None is an S-P7 or S-P2 result and none is a
capstone result.

| Run | Copy of | Mutation | Result |
|---|---|---|---|
| `cap22a_sp7_strict_cc6_base` | `cap21b_sp7_strict_base_sigbytes_wrapped.pv`, **unchanged** | none — the baseline for the C-C6 question | all green (`:594`–`:658`); witnesses reachable (`:993`, `:1204`) |
| `cap22b_sp7_strict_cc6` | `cap22a` | **C-C6's conditional byte unbinding** inside `InnerCheck` (byte equality demanded only when the signed frame's own `kfp` matches the verifying key); same-key wrapping retained; DNS leaked | **all green** — wrapped C-Q8 (`:692`), `TypeConfused` (`:722`), `Rescoped` (`:752`), `InnerSigTransplanted` (`:782`), `Reattributed` (`:812`); witnesses reachable (`:1161`, `:1386`). *C-C5's strict route does not open under C-C6: the same-key wrapper frame names the verifying key, so equality is demanded — **case (a), descended*** |
| `cap22c_sp7_strict_cc6_repo` | `cap22b` | the repository key leaked instead | the same (`:693`–`:817`, `:1167`, `:1393`). *Case (b), descended* |
| `cap22d_sp7_strict_base_q9` | `cap14a_sp7_q1_strict_base.pv` | the **C-Q9 structural possession judge** added, firing including on verification failure; the inner acceptance reports its checked inner `(kI, tI, ppfI)` | C-Q9 green (`:1186`); all else as `cap14a` (`:588`–`:630`, `:963`, `:1172`) |
| `cap22e_sp7_strict_q6b_q9_inner` | `cap14b_sp7_q1_strict_q6b.pv` (C-C15(i) on strict) | the C-Q9 judge added; the inner acceptance reports the **presented inner** `(kW, tI, ppfI)` — the terms it was about, never checked by this mutant | **C-Q9 red** (`:1334`) while the four S-P7 queries stay green (`:569`–`:596`) and witnesses reachable (`:871`, `:1075`). *Case (a), descended* |
| `cap22f_sp7_strict_q6b_q9_inner_repo` | `cap22e` | the repository key leaked instead | the same (`:1334`; `:569`–`:596`; `:871`, `:1075`). *Case (b), descended* |
| `cap22g_sp7_strict_q6b_q9_outer` | `cap22e` | the inner acceptance reports the **checked outer** `(kW, tW, ppfW)` instead | **C-Q9 green** (`:1084`). *The **rejected** report reading: it hides the companion's failure by reporting what the verifier did check* |
| `cap22h_sp2_strict_cc8_mh` | `cap18c_sp2_strict_cc8.pv` (C-C8 strict) | a judge reporting each accepted slot's `(t, frame)` and firing on **`mh ≠ h(t)`** added | **manifest-hash judge green** (`:1478`) while C-Q9 stays red (`:1466`); the rest green (`:512`–`:549`, `:1224`, `:1236`); witnesses reachable (`:731`, `:966`, `:1212`). *Link 5's `mh` half, case (a), descended green* |
| `cap22i_sp2_strict_cc8_mh_repo` | `cap22h` | the repository key leaked instead | the same (`:1477`; `:1465`; witnesses `:730`, `:965`, `:1211`). *Case (b), descended* |
| `cap22j_sp2_degraded_cc8_mh` | `d10b_sp2_q9_manifest_unbound.pv` (C-C8's degraded source) | the same manifest-hash judge, as the control | **judge red** (`:1665`), `SetAltered` red (`:701`), C-Q9 red (`:1499`); witnesses reachable (`:882`, `:1105`, `:1311`). *In degraded the dropped guard is exploitable; in strict the honest channel's tuple pin keeps `mh = h(t)`* |

**What did not change.** **No query was added or removed**, and **no
companion and no configuration was added or removed** — the count stands
at **SEVENTEEN**, C-C8-i/C-C8-ii and C-C10's isolation control remain
**controls**, and C-C15(iii) remains C-C15's isolation configuration.
**No probability, no residual decomposition and no timebox was
altered**; the **26** timeboxed entries and the **1155 min** per-case
total **stand**, as does the 4 × 1155 = 4620 min ceiling and everything
§3's *“What the total is, and is not”* says about it. **The fixture is
entirely unchanged**, including the **three earlier contestable
choices** — same-key wrapping, compromised-channel-only enrolment, and
`ev` as the pair in strict — which this round again confirms and
reverses in no part; **a fourth contestable choice joins them**, the
report contract of §1.3, which fixes what `LayerAccepted`'s **existing**
arguments denote under a mutation and **changes its signature not at
all**. The ladder, the ordering, the ablation order and §5's matrix
rows, producers, consumers and expected reds are unchanged. **No set
(1), set (2) or set (3) membership changed** in any companion: what
moved is **descent and colour per case** — C-C15(i)'s C-Q9 and link 3
into descended red, C-C8's `mh` half into descended green in strict,
C-C6's five declared queries into descended green in strict — and every
one of those is a **registered per-case outcome** of a set the row
already carried. The **skeptic log** is untouched; the **review log**
and the **freeze statement** are untouched; and the routed **`REFUSAL`
fork** (§8, item 1) is untouched and **unresolved**, owed at the
author's commit. **What did change and is stated once here: this file
now says what a layer's acceptance REPORTS, and it is a contestable
clerk term — the first of the four that can, by itself, turn a
registered green red.**


## Repairs after the 2026-09-17 Codex review, tenth round

*Written by the drafting step directed by the owner instance after the
tenth non-author round,
`docs/reviews/2026-09-17-codex-review-capstone-predictions-round10.md`
(**two findings, both accepted**; the verdict was **not ready to
freeze**), whose three dispositions at its head are this repair's
specification. **They are clerk dispositions of the owner instance, not
author rulings.** **What this round is about, stated plainly.** Both
findings are **consequences of round nine's report contract** that round
nine did not follow all the way out. Finding 1: C-C15(i)'s round-nine
repair moved C-Q9 and link 3 to descended red and then said *“every
other member of it stands unchanged”* — but this mutation checks the
**outer** tuple, evidence and possession and verifies the inner
signature under `kW`, **never examining the presented inner tuple or
evidence at all**, so under §1.3's contract **every registered relation
over the reported inner terms is exposed**, not possession alone. Five
more are now **descended red** in (a) and (b), on **strict** copies
carrying structural observers: **link 1a**
(`cap23d_sp7_strict_q6b_observers_tuple.out:2573`), **link 1b**
(`:1735`), **link 2a's primary-slot relation** (`:2297`), **link 5's
`mh` half** (`:2017`) and **C-Q5's relation** (`:2883`), with C-Q9
beside them (`:1459`), the four declared S-P7 queries green
(`:686`–`:716`), both witnesses reachable (`:992`, `:1199`) and the
matched baseline **all green**
(`cap23b_sp7_strict_base_observers_tuple.out:1329`–`:1385`); case (b)
descends line for line on
`cap23f_sp7_strict_q6b_observers_tuple_repo.out`. **The route needs no
adversary-authorized key and reverses neither contestable fixture
choice**: an honest same-key wrapper's valid inner signature, its bytes
and the outer credentials retained, the presented inner tuple and
evidence replaced. Finding 2: C-C13(ii) relaxes **only** the outer
`=OT_WRAPPER` guard and keeps `=OT_ATTEST` inside `InnerCheck`
(`s-p7/proverif/ablations/a10_no_wrapper_type.pv:136`, `:162`), so link
6a's red belongs to the **wrapper layer** — `L0` at depth 1, `L0` and
`L1` at depth 2 — and **never to the innermost attestation layer**;
separated observers show the **inner** type relation green and the
**outer** red under that mutation
(`cap23h_sp7_strict_type_outer.out:1313`, `:1520`) against a both-green
baseline (`cap23g_sp7_strict_type_base.out:1111`, `:1124`). **Nothing in
this round flips a colour the runs do not show**, and one correction
runs the other way: `cap23g`/`cap23h` are **degraded, sole-channel,
depth-1** copies despite the `strict` in their filenames, so **no strict
outcome of C-C13 moves** and its (a)/(b) three lists stand exactly as
round eight left them. **The four contestable choices stand** — same-key
wrapping, compromised-channel-only enrolment, `ev` as the pair in
strict, and §1.3's report contract — and **none is reversed here**;
finding 1 operates entirely within the first two, as the reviewer
confirms. **The skeptic log is untouched**, as are the review log, the
freeze statement, every probability, every residual decomposition, every
timebox, the **26** timeboxed entries and the **1155 min** per-case
total; and the routed **`REFUSAL` fork** (§8, item 1) is **not** resolved
here — the reviewer again names it, correctly, as the existing author
decision owed at the author's commit. **The companion count is unchanged
at SEVENTEEN** — this round adds no companion, no query, no
configuration and no timeboxed entry. **No capstone model exists; none
was written; none was run.** The eight runs below are ProVerif 2.05 runs
on **copies of committed family models** under
`formal/suite/ledger-tests-2026-09-14/` (**fourteenth batch** of that
directory's README), each `rc=0`, all eight the reviewer's own
`/tmp/tessera-capstone-r10/` diagnostics copied **byte for byte** under a
provenance header and re-run on our tree, landing at the reviewer's own
`.out` line numbers. **No repository model was edited or run**, and **no
`.out` below is a capstone result**. The earlier repair sections are
**amended by dated notes**, not rewritten: the round-nine section keeps
its text and carries a dated note extending its finding-1 consequence.*

### Edits, by finding

| # | Finding | Edit |
|---|---|---|
| **1** | **C-C15(i) retains guarantees that fail under the report contract.** The mutation checks the outer tuple, evidence and possession and verifies the inner signature under `kW`; it never examines the **presented** inner tuple or evidence, so under §1.3 every relation over the reported inner terms is exposed — not C-Q9 alone | §9(1), **C-C15**'s Cases cell, configuration (i)'s three lists: **links 1a, 1b, 2a, link 5's `mh` half and C-Q5's relation move from predicted green to DESCENDED RED in (a) and (b)** (`cap23d_sp7_strict_q6b_observers_tuple.out:2573`, `:1735`, `:2297`, `:2017`, `:2883`, C-Q9 `:1459`, queries `:686`–`:716`, witnesses `:992`, `:1199`; case (b) on `cap23f…` at the same lines), against the all-green baseline `cap23b…:1329`, `:1343`, `:1357`, `:1371`, `:1385` (C-Q9 `:1306`). The sentence *“every other member of it stands unchanged”* is **withdrawn and quoted**. The reds are descended **as relations**, `ChainBroken` and `SetAltered` being declared in neither copy — the round-nine shape, and the same shape as `cap20a`, `cap21d`, `cap22h`. **The route is stated** (honest same-key wrapper, valid inner signature, bytes and outer credentials retained, presented inner tuple and evidence replaced; no adversary key; neither contestable choice reversed), and the **contrast with C-C8's strict green `mh` half** (`cap22h:1478`) is stated so the two do not read as contradictory. **Predicted green, each with a one-clause basis:** C-Q7, C-Q8, link 4, link 2b, link 6a, `Stripped`, `SignerForged`, `Spliced`, `VersionLied`; link 6b is left where it already is, in the Row column's D11 sentence. §9(1), C-C15's **set (1)**: in **(d)** the same five are added as **PREDICTED red** under the contract, with the reason they are not descended — **no degraded copy carries the observers**, `cap23c`–`cap23f` being strict — and **the family's S-P7 Q6b row is not edited**. §9(1), C-C15's **Row** column: a dated note extending the D11 amendment — the five are red in (a)/(b) too, and **D11's discharge still rests on configuration (iii)**, none of the five being link 6b |
| **2** | **C-C13(ii) assigns link 6a's red to layers whose type check is intact.** a10 relaxes only the outer `=OT_WRAPPER` guard and keeps `=OT_ATTEST` inside `InnerCheck`; an outer-frame type violation cannot be reported as the innermost layer's | §9(1), **C-C13**'s set (1): *“at `L1` and `L2` in (ii)”* **withdrawn and quoted**, replaced by **the wrapper layer only** — `L0` at depth 1, `L0` and `L1` at depth 2 — pointing to the Cases cell. §9(1), C-C13's **Cases** cell, appended: **WHICH LAYER (ii) SEVERS, STATED PER DEPTH** — what a10 relaxes (`a10_no_wrapper_type.pv:162`, inside `VerifierWrapped` `:154-166`) and what it keeps (`:136`, inside `InnerCheck` `:129-142`, called at `:166`); the indexing stated against **(E4)** (*“`lyr ≠ L0`; at depth 2 the innermost layer is `L2`”*), §1.2's check 5 (*“`InnerCheck` for `lyr ≠ L0`”*) and §1.3's *“one acceptance per layer and up to three (`L0`, `L1`, `L2`) at depth 2”*, all three quoted; **never the innermost attestation layer**, and **an innermost-layer red is configuration (i)'s, not (ii)'s**. Evidence: `cap23g…:1111`, `:1124` (baseline both green, `VersionLied` `:1098`), `cap23h…:1313` (inner green), `:1520` (outer red), `:749` (`TypeConfused` aggregate red), `:764`, `:779`, `:794` green, witnesses `:1100`, `:1298`. **`TypeConfused`'s aggregate red stays descended** in (d) (`ablations/a10_no_wrapper_type.out:723`), and it is stated that the aggregate **does not** establish the per-layer set |
| **—** | Consequential, listed once so nothing is silent | §9(1), **C-C13**'s Cases cell also records what `cap23g`/`cap23h` **are**: **degraded, sole-channel, depth-1** copies (`cap23g…pv:391`, `:400`; `cap23h…pv:214`, `:223`), **not** strict copies of `cap14a` as their filenames and the README's fourteenth-batch row say — so **(a)/(b) keep “descended green: NONE. Descended red: NONE”** and C-C13's strict predictions are untouched. The **round-nine repair section** gains a **dated note** under its edits table, extending its finding-1 consequence to the five new members; its rows stand as written. **No query, no companion, no configuration, no probability, no residual decomposition and no timebox was added, removed or altered**; **no row and no column was added to any table**; §1.1, §1.2, §1.3, §2, §3, §5, §6, §7 and §8 are **untouched**, and `LayerAccepted`'s signature is unchanged |

### Scratch runs made for this repair

All eight are ProVerif 2.05,
`proverif -lib formal/suite/lib/tessera_theory.pvl <copy>.pv`, `rc=0`,
on copies under `formal/suite/ledger-tests-2026-09-14/` (**fourteenth
batch** of that directory's README). All eight reproduce the reviewer's
`/tmp/tessera-capstone-r10/` diagnostics on our own tree at his own
`.out` line numbers. None is an S-P7 result and none is a capstone
result.

| Run | Copy of | Mutation | Result |
|---|---|---|---|
| `cap23a_sp7_strict_base_observers` | `cap14a_sp7_q1_strict_base.pv` (correct strict S-P7) | five **structural observers on the inner acceptance's reported terms** added — link 1b (the inner tuple has a prior authority publication), link 5 (inner frame `mh = h(tI)`), link 2a's primary-slot relation (`fp(k) = kfpr`), link 1a (presented inner evidence verifies over `tI`), C-Q5's relation (an honest accepting key reports its sole signed manifest) — plus the C-Q9 judge; nothing else | all green (`:1302`, `:1325`, `:1339`, `:1353`, `:1367`, `:1381`); the four S-P7 queries green (`:700`–`:742`); witnesses reachable (`:1077`, `:1288`) |
| `cap23b_sp7_strict_base_observers_tuple` | `cap23a` | the reports restricted to well-formed `authTuple` terms | all green (`:1306`, `:1329`, `:1343`, `:1357`, `:1371`, `:1385`); witnesses (`:1081`, `:1292`). *The matched baseline for configuration (i)* |
| `cap23c_sp7_strict_q6b_observers` | `cap23a` | **C-C15(i)'s mutation** (Q6b on strict): outer tuple, evidence and possession checked, inner signature verified under `kW`, the presented inner tuple and evidence unchecked; the inner acceptance **reports the presented inner terms** per §1.3's contract; DNS leaked | **C-Q9 red** (`:1471`), **link 1b red** (`:1727`), **link 5 `mh` red** (`:1987`), **link 2a red** (`:2267`), **link 1a red** (`:2523`), **C-Q5 red** (`:2811`); the four S-P7 queries green (`:682`–`:712`); witnesses reachable (`:996`, `:1203`) |
| `cap23d_sp7_strict_q6b_observers_tuple` | `cap23c` | reports restricted to well-formed tuples | the same: `:1459`, **`:1735`, `:2017`, `:2297`, `:2573`, `:2883`** red; `:686`–`:716` green; witnesses `:992`, `:1199`. *The route needs no adversary key: an honest same-key wrapper's valid inner signature and outer credentials retained, the presented inner tuple and evidence replaced — **case (a), descended*** |
| `cap23e_sp7_strict_q6b_observers_repo` | `cap23c` | the repository key leaked instead | identical line for line to `cap23c` |
| `cap23f_sp7_strict_q6b_observers_tuple_repo` | `cap23d` | the repository key leaked instead | identical line for line to `cap23d` (`:1735`, `:2017`, `:2297`, `:2573`, `:2883` red). *Case (b), descended* |
| `cap23g_sp7_strict_type_base` | `cap14a` **per the README's row; the body is `sp7_q2_degraded_compromised.pv`'s** — degraded, sole channel compromised, depth 1 (`…pv:391`, `:400`) | separate structural observers for the **inner** frame's type relation and the **outer** wrapper's type relation (the A5.5 version judge carried) | both green (`:1111`, `:1124`); `VersionLied` green (`:1098`); the rest as the base model. *Degraded: it descends (d), not (a)/(b)* |
| `cap23h_sp7_strict_type_outer` | `cap23g` | **ablation a10's mutation** — the outer `=OT_WRAPPER` equality relaxed, the inner `=OT_ATTEST` retained (C-C13(ii)) | **inner type relation green** (`:1313`) while the **outer is red** (`:1520`); `TypeConfused` red in aggregate (`:749`), `Rescoped` (`:764`), `InnerSigTransplanted` (`:779`), `Reattributed` (`:794`) green; witnesses reachable (`:1100`, `:1298`). *The type failure is at the wrapper layer only — and, being degraded (`…pv:214`, `:223`), it descends (d)* |

**What did not change.** **No query was added or removed**, and **no
companion and no configuration was added or removed** — the count stands
at **SEVENTEEN**, C-C8-i/C-C8-ii and C-C10's isolation control remain
**controls**, and C-C15(iii) remains C-C15's isolation configuration.
**No probability, no residual decomposition and no timebox was
altered**; the **26** timeboxed entries and the **1155 min** per-case
total **stand**, as does the 4 × 1155 = 4620 min ceiling and everything
§3's *“What the total is, and is not”* says about it. **The fixture is
entirely unchanged**, including all **four contestable choices** —
same-key wrapping, compromised-channel-only enrolment, `ev` as the pair
in strict, and §1.3's report contract — which this round again confirms
and reverses in no part; finding 1's route is constructed **inside** the
first two, and §1.3 itself is **not edited here**. The ladder, the
ordering, the ablation order and §5's matrix rows, producers, consumers
and expected reds are unchanged. **No set (1), set (2) or set (3)
membership changed** in any companion — what moved is **descent and
colour per case** in C-C15(i) (five relations from predicted green to
descended red in (a) and (b), and the same five added to (d) as
predictions), and **a layer assignment** in C-C13(ii), which was a
statement about *where* a registered red falls and not about what the
set contains. The **skeptic log** is untouched; the **review log** and
the **freeze statement** are untouched; and the routed **`REFUSAL`
fork** (§8, item 1) is untouched and **unresolved**, owed at the
author's commit. **What did change and is stated once here: round
nine's report contract has now been carried to the two places it was
not, and one of them cost C-C15(i) five more strict greens.**

## Repairs after the 2026-09-17 Codex review, eleventh round

*Written by the drafting step directed by the owner instance after the
eleventh non-author round,
`docs/reviews/2026-09-17-codex-review-capstone-predictions-round11.md`
(**one finding, accepted**; the verdict was **not ready to freeze**),
whose two dispositions at its head are this repair's specification.
**They are clerk dispositions of the owner instance, not author
rulings.** The reviewer wrote, and it is recorded here rather than
smoothed over: “**Only one new defect is established, so I cannot
honestly supply three independent findings.**” **What this round is
about, stated plainly.** It is the third consecutive round in which
§1.3's **report contract** — one of the four contestable choices — has
cost C-C15(i) a strict green that was justified by reasoning about the
terms the mutation **does** check. The withdrawn justification called
`SignerForged` a relation over the **outer** tuple; the contract makes
the inner acceptance report its **own presented** tuple and the
**manifest-named slot** it reports as satisfied, which this mutation
never checks. S-P2's **registered** membership observer
(`MemberJudge`'s first arm, `s-p2/PREDICTIONS.md:270-273`) added to the
round-ten copies makes `SignerForged` **reachable** in both channel
variants (`cap24b_sp7_strict_q6b_member.out:3211`,
`cap24c_sp7_strict_q6b_member_repo.out:3211`) against an **unreachable**
matched strict baseline (`cap24a_sp7_strict_base_member.out:1421`), with
the four declared S-P7 queries green (`cap24b:708`–`:738`) and both
witnesses reachable (`:1014`, `:1221`) — a **severing, not a broken
fixture**. The trace (`cap24b:3199-3211`) retains the same-key wrapper's
valid credentials, presents the **other** honest issuer's manifest as
the inner tuple and reports its named slot as satisfied by the wrapper
key: `SignerForged(M2, pk(skI1))`. **No adversary-enrolled identity is
used and neither contestable choice is reversed.** **Nothing in this
round flips a colour the runs do not show, and two things the reviewer
declined to count are carried as declined:** the exploratory **link 2b**
completeness projection is **not** a finding, because that family
projection **lacks the capstone's retained two-signer set logic**, and
**`Stripped`'s red is not inferred** from the membership result — both
stay **predicted**, in his words and on his limits. **The four
contestable choices stand** — same-key wrapping, compromised-channel-only
enrolment, `ev` as the pair in strict, and §1.3's report contract — and
**none is reversed here**; finding 1 operates entirely inside the first
two, as the reviewer confirms. **The skeptic log is untouched**, as are
the review log, the freeze statement, every probability, every residual
decomposition, every timebox, the **26** timeboxed entries and the
**1155 min** per-case total; and the routed **`REFUSAL` fork** (§8, item
1) is **not** resolved here — the reviewer again names it, correctly, as
the existing author decision owed at the author's commit. **The
companion count is unchanged at SEVENTEEN** — this round adds no
companion, no query, no configuration and no timeboxed entry. **No
capstone model exists; none was written; none was run.** The three runs
below are ProVerif 2.05 runs on **copies of committed family models**
under `formal/suite/ledger-tests-2026-09-14/` (**fifteenth batch** of
that directory's README), each `rc=0`, all three the reviewer's own
`/tmp/tessera-capstone-r11/` diagnostics copied **byte for byte** under
a provenance header and re-run on our tree, landing at the reviewer's
own `.out` line numbers. **No repository model was edited or run**, and
**no `.out` below is a capstone result**. The earlier repair sections
are **not rewritten**: this round's edits are in place in §9(1), each
carrying its own dated marker and its withdrawn text quoted.*

### Edits, by finding

| # | Finding | Edit |
|---|---|---|
| **1** | **C-C15(i) still predicted `SignerForged` green by reasoning about the checked outer tuple.** The retained-list justification called it a relation over the **outer** tuple; under §1.3 the inner acceptance reports its own **presented** tuple and manifest-named slot, which this mutation leaves unchecked. The two instructions give different answers, and the run settles it | §9(1), **C-C15**'s Cases cell, configuration (i)'s three lists: **`SignerForged` moves from predicted green to DESCENDED RED in (a) and (b)** (`cap24b_sp7_strict_q6b_member.out:3211`; case (b) `cap24c_sp7_strict_q6b_member_repo.out:3211`, identical line for line), against the **unreachable** matched strict baseline (`cap24a_sp7_strict_base_member.out:1421`), with the four declared S-P7 queries green (`cap24b:708`–`:738`) and both witnesses reachable (`:1014`, `:1221`). The clause *“**`Stripped`** and **`SignerForged`** — the set-logic relations over the **outer** tuple this mutation still checks in full, neither judge declared in these copies”* is **withdrawn and quoted**, and `Stripped` re-stated alone with its own basis. The red is descended **as a relation** on a **strict** family copy — the round-nine shape — and **nothing is claimed for `SetAltered`**, which neither copy declares. The **route is stated** (same-key wrapper's valid credentials retained, the other honest issuer's manifest presented as the inner tuple, its named slot reported as satisfied by the wrapper key, `SignerForged(M2, pk(skI1))`, trace `cap24b:3199-3211`); **no adversary-enrolled identity, neither contestable choice reversed**. The round-ten count sentence *“configuration (i) now carries **six descended reds** in (a) and in (b)”* is **withdrawn and quoted**; the count is **SEVEN**. **Carried explicitly, on the reviewer's own limits: link 2b and `Stripped` STAY PREDICTED** — the exploratory completeness projection cannot settle link 2b because that family projection lacks the capstone's retained two-signer set logic, and `Stripped` red is **not inferred** from a `SignerForged` result. §9(1), C-C15's **set (1)**: in **(d)** `SignerForged` is added as **PREDICTED red** under the same contract, with the reason it is not descended — **no degraded copy carries the membership observer**, `cap24a`–`cap24c` being strict — and **no family row is edited** |
| **—** | Consequential, listed once so nothing is silent | **D7's matrix row does not name C-C15 and is therefore not touched**, and no other §5 row, producer, consumer or expected red changes. **Configurations (ii) and (iii) are untouched**: their `SignerForged` stays where each already has it, (iii)'s in its predicted-green list. **No query, no companion, no configuration, no probability, no residual decomposition and no timebox was added, removed or altered**; **no row and no column was added to any table**; §1.1, §1.2, §1.3, §2, §3, §5, §6, §7 and §8 are **untouched**, and `LayerAccepted`'s signature is unchanged |

### Scratch runs made for this repair

All three are ProVerif 2.05,
`proverif -lib formal/suite/lib/tessera_theory.pvl <copy>.pv`, `rc=0`,
on copies under `formal/suite/ledger-tests-2026-09-14/` (**fifteenth
batch** of that directory's README). All three reproduce the reviewer's
`/tmp/tessera-capstone-r11/` diagnostics on our own tree at his own
`.out` line numbers. None is an S-P7 result, none is an S-P2 result and
none is a capstone result.

| Run | Copy of | Mutation | Result |
|---|---|---|---|
| `cap24a_sp7_strict_base_member` | `cap23b_sp7_strict_base_observers_tuple.pv` (correct strict S-P7 with the round-10 observers) | **S-P2's membership observer** added — the registered `MemberJudge` relation: an honest `(key, manifest)` paired with the reported `(tuple, slot fingerprint, accepting key)`, `SignerForged` firing when another key satisfies that honest signer's slot | **`SignerForged` unreachable** (`:1421`); the four S-P7 queries green (`:726`–`:768`); witnesses reachable (`:1103`, `:1314`). *The matched baseline for configuration (i)* |
| `cap24b_sp7_strict_q6b_member` | `cap23d_sp7_strict_q6b_observers_tuple.pv` (C-C15(i) on strict, presented inner terms reported) | the same membership observer; DNS leaked | **`SignerForged` reachable** (`:3211`; trace `:3199-3211`: `SignerForged(M2, pk(skI1))` — the wrapper key `skI1` reported as satisfying issuer 2's manifest slot); the four S-P7 queries green (`:708`–`:738`); witnesses reachable (`:1014`, `:1221`). *Case (a), descended* |
| `cap24c_sp7_strict_q6b_member_repo` | `cap24b` | the repository key leaked instead | identical line for line (`:3211`). *Case (b), descended* |

**What did not change.** **No query was added or removed**, and **no
companion and no configuration was added or removed** — the count stands
at **SEVENTEEN**, C-C8-i/C-C8-ii and C-C10's isolation control remain
**controls**, and C-C15(iii) remains C-C15's isolation configuration.
**No probability, no residual decomposition and no timebox was
altered**; the **26** timeboxed entries and the **1155 min** per-case
total **stand**, as does the 4 × 1155 = 4620 min ceiling and everything
§3's *“What the total is, and is not”* says about it. **The fixture is
entirely unchanged**, including all **four contestable choices** —
same-key wrapping, compromised-channel-only enrolment, `ev` as the pair
in strict, and §1.3's report contract — which this round again confirms
and reverses in no part; finding 1's route is constructed **inside** the
first two, and §1.3 itself is **not edited here**. The ladder, the
ordering, the ablation order and §5's matrix rows, producers, consumers
and expected reds are unchanged — **D7's row does not name C-C15 and was
left alone**. **No set (1), set (2) or set (3) membership changed** in
any companion — what moved is **descent and colour per case** in
C-C15(i) (`SignerForged` from predicted green to descended red in (a)
and (b), and added to (d) as a prediction). The **skeptic log** is
untouched; the **review log** and the **freeze statement** are
untouched; and the routed **`REFUSAL` fork** (§8, item 1) is untouched
and **unresolved**, owed at the author's commit. **What did change and
is stated once here: the last strict green in C-C15(i) that was
justified by the terms the mutation checks has been withdrawn, and the
two results the reviewer declined to count are carried as declined —
link 2b and `Stripped` stay predicted.**

## Repairs after the 2026-09-17 Codex review, twelfth round

*Written by the drafting step directed by the owner instance after the
twelfth non-author round,
`docs/reviews/2026-09-17-codex-review-capstone-predictions-round12.md`
(**no finding**; the verdict was **ready to freeze subject to the
author's items**), whose disposition 1 at its head is this section's
whole specification. **It is a clerk disposition of the owner instance,
not an author ruling.** **There is no repair in this round, and that is
the point of the section.** The reviewer found no new run-backed defect,
re-ran **all 87 archived `cap5`–`cap24` diagnostic copies** under
ProVerif 2.05 with every `RESULT` line matching its archive, and checked
all eleven disposition records against the operative text, finding all
**thirty-four** accepted findings' repairs present. He wrote, and it is
carried here verbatim: “**This registration is ready to freeze from this
non-author review, subject to the REFUSAL ruling, the author's
disposition of the four contestable choices, and the stated pre-freeze
review prerequisites.**” **What this round changes in the file is one
dated NOTE and nothing else.** The reviewer's four control runs put a
**signature-term observer** (C-Q7's relation) and a **structural
byte-binding observer** (C-Q8's relation) on C-C15(i)'s strict copies,
found both **green** in both single-channel-compromise variants, and
showed each observer live against its own negative control. That moves
two of configuration (i)'s **predicted** greens to **descended** greens
— a **strengthening**, entered in §9(1)'s C-C15 Cases cell as a **dated
note** and **not as a repair**, because no finding was made and nothing
is withdrawn. **No set (1), set (2) or set (3) membership changed; no
query, no companion, no configuration, no probability, no residual
decomposition and no timebox moved**; the **26** timeboxed entries, the
**1155 min** per-case total, the 4 × 1155 = 4620 min ceiling and the
count of **SEVENTEEN** companions all stand. The **four contestable
choices** stand and none is reversed. The **skeptic log**, the **review
log**'s existing entry and the **freeze statement** are untouched, and
the routed **`REFUSAL` fork** (§8, item 1) is **not** resolved here — the
reviewer names it again, correctly, as the author's own decision, owed
at his commit. **The earlier repair sections are not rewritten.** **No
capstone model exists; none was written; none was run.** The four runs
below are ProVerif 2.05 runs on **copies of committed family models**
under `formal/suite/ledger-tests-2026-09-14/` (**sixteenth batch** of
that directory's README), each the reviewer's own
`/tmp/tessera-capstone-r12-4akx1iw4/` diagnostic copied **byte for
byte** under a provenance header and re-run on our tree at his own
`.out` line numbers. **No repository model was edited or run**, and **no
`.out` below is a capstone result.*

### The dated note, and where it is

| # | Disposition | Entry |
|---|---|---|
| **1** | **No finding to disposition.** The four control runs let C-C15(i)'s **C-Q7** and **C-Q8** become **descended** greens in (a) and (b) — a strengthening | A **dated note** in the **C-C15 row's Cases cell**, §9(1), configuration (i), beside the round-9/10/11 blocks: C-Q7's and C-Q8's relations **descended green** on `cap25a` (case (a)) and `cap25b` (case (b)), each observer shown live by its own negative control (`cap25c`, `cap25d`); **C-Q7 and C-Q8 come out of the round-ten “What remains PREDICTED GREEN” list for (a) and (b)** and every other member of that list stands. In **(d)** nothing moves |
| **—** | Consequential, listed once so nothing is silent | **Nothing.** §5's matrix rows, producers, consumers and expected reds are untouched; C-C15's three sets are untouched by this note; the retained-query table is untouched; and no other companion, row or cell changes |

### Scratch runs made for this repair

All four are ProVerif 2.05,
`proverif -lib formal/suite/lib/tessera_theory.pvl <copy>.pv`, `rc=0`,
on copies under `formal/suite/ledger-tests-2026-09-14/` (**sixteenth
batch** of that directory's README). All four reproduce the reviewer's
`/tmp/tessera-capstone-r12-4akx1iw4/` diagnostics on our own tree at his
own `.out` line numbers. None is an S-P7 result and none is a capstone
result.

| Run | Copy of | Mutation | Result |
|---|---|---|---|
| `cap25a_sp7_strict_q6b_sigjudges` | `cap24b_sp7_strict_q6b_member.pv` (C-C15(i) on strict, presented inner terms reported, membership observer) | a **signature-term observer** (C-Q7's relation, `GenericTransplant`) and a **structural byte-binding observer** (C-Q8's relation, `GenericBytesUnbound`) added; DNS leaked | **both green** (`:1306`, `:1317`); four S-P7 queries green (`:777`–`:810`); witnesses reachable (`:1087`, `:1295`); `SignerForged` red as in `cap24b` (`:3315`). *Case (a), descended* |
| `cap25b_sp7_strict_q6b_sigjudges_repo` | `cap25a` | the repository key leaked instead | the same (`:1306`, `:1317` green; `:3314` red). *Case (b), descended* |
| `cap25c_sp7_strict_q6b_sigjudges_bytes_control` | `cap25a` | the inner signature unbound from the presented bytes — the **byte observer's negative control** | **byte observer red** (`:2249`); signature-term observer green (`:1948`); `Rescoped` and `Reattributed` red (`:1106`, `:1446`); witnesses reachable (`:1727`, `:1936`) |
| `cap25d_sp7_strict_q6b_sigjudges_transplant_control` | `cap25a` | both channel keys leaked — case (c) — the **signature-term observer's negative control** | **signature-term observer red** (`:2505`); byte observer green (`:2517`); `Rescoped`, `InnerSigTransplanted`, `Reattributed` red (`:1088`, `:1399`, `:1701`); witnesses reachable (`:1982`, `:2194`) |

**What did not change.** **Everything except the dated note.** No query
was added or removed; no companion and no configuration was added or
removed — the count stands at **SEVENTEEN**; no set membership moved; no
probability, residual decomposition or timebox was altered; the fixture
and all **four contestable choices** are untouched; §5's matrix is
untouched; the **skeptic log**, the **review log**'s existing entry and
the **freeze statement** are untouched; and the routed **`REFUSAL`
fork** is untouched and **unresolved**, owed at the author's commit.
**What did change and is stated once here: two strict greens of
C-C15(i) that were predictions with a stated basis are now descended,
and the file's last non-author round is closed in the file rather than
only in its record.**

## Repairs after the 2026-09-17 Codex review, thirteenth round

*Written by the drafting step directed by the owner instance after the
thirteenth non-author round,
`docs/reviews/2026-09-17-codex-review-capstone-predictions-round13.md`,
whose four dispositions at its head are this section's whole
specification. **They are clerk dispositions of the owner instance, not
author rulings**, and each is contestable at the freeze commit like
every other clerk disposition in this file. The round was run **against
the file as the 2026-09-17 skeptic read left it**, and what it found is
narrow and of one kind: **three bounded corrections of the skeptic
repair itself**, all accepted, each one sentence. **It demonstrated no
new query escape**, confirmed that the two isolation observers declared
under S-10 carry consistent arities and behave as registered on family
copies, that the timebox totals still add — **26** entries, **1155 min**
per case, 4 × 1155 = **4620 min** — that the `cap25` note is exact (he
re-ran `cap25a`–`cap25d`, every `RESULT` matching the archive), and that
the `REFUSAL` fork and the four contestable choices are unchanged.
**The observers were also CONFIRMED by run**, which is the round's one
addition rather than a correction. **No probability, no residual
decomposition, no timebox, no companion count — still SEVENTEEN — and
no set (3) moves here.** The **freeze statement**, the **review log**'s
existing entries, the **2026-09-15 and 2026-09-17 skeptic logs** (save
one dated one-line correction under S-4, added rather than rewritten)
and the routed **`REFUSAL` fork** (§8, item 1) are untouched; the fork
remains **unresolved**, owed at the author's commit. **The earlier
repair sections are not rewritten.** **No capstone model exists; none
was written; none was run.** The four runs below are ProVerif 2.05 runs
on **copies of committed family models** under
`formal/suite/ledger-tests-2026-09-14/` (**seventeenth batch** of that
directory's README), each the reviewer's own
`/tmp/tessera-capstone-r13-w3lu9otg/` diagnostic copied **byte for
byte** under a provenance header and re-run on our tree at his own
`.out` line numbers. **No repository model was edited or run**, and **no
`.out` below is a capstone result.*

### Edits, by finding

**The line numbers in the Findings column are the REVIEWER'S, against
the file as it then stood**; this round's own edits shifted them (the
§(1) observer sentence, the **C-C7** row, the **C-C15** row and the
2026-09-17 skeptic log's S-4 entry are the four places meant).

| # | Finding, in the reviewer's terms | Disposition | Edit |
|---|---|---|---|
| **1** | **S-10's observer paragraph names conjunct 3 as D11's only consumer** (`:841-844`) — but D11 also requires the **unconditional C-Q1 link 6b**, and this file explains at length why conditional conjunct 3 cannot replace it (`:556-567`, `:1776`) | **ACCEPTED.** A narrowing introduced by the skeptic repair, not a query defect | §(1)'s observer paragraph: the sentence is qualified to **D11's C-Q6 half**, with D11's unconditional consumer named beside it; the withdrawn phrase quoted. **The query, the observers' status and the timeboxes are unchanged** |
| **2** | **C-C15(i) assigns a degraded failure to an EXCLUDED query**: set (1) predicts **link 1b red in (d)** and the repaired set (2) repeats the assignment, while C-Q1-degraded is **strict-only** and does not assert link 1b (`:2280`, `:307-311`, `:362-371`) | **ACCEPTED**, and the reviewer's own diagnostic settles why it is not merely a bookkeeping slip: adding the correspondence to the **unmutated** degraded model is already `is false` — a **baseline cost**, never a severing | §9(1), **C-C15**, configuration **(i)** only: link 1b comes **out** of the (d) list of set (1) (five relations → **four**), out of the S-1 block's “same eight” carry-over in (d) (→ **seven**), and out of the (d) clause of the case-qualified set (2) (seven → **six**) **without entering set (1)** — it is in **no (d) set** of that configuration. Each withdrawn membership quoted in place. **Link 1b's STRICT outcomes in (a) and (b) stand with their cites**; configurations **(ii)** and **(iii)** are untouched; the count of descended reds in (i) is still **SEVEN** |
| **3** | **S-4 upgraded an unrun case from predicted to descended**: C-C7's repaired set (1) calls the unrestricted authorship red **descended in both (a) and (b)**, while the row's own Cases cell says every case-(b) entry is predicted from channel symmetry (`:1655`, `:3752-3757`) | **ACCEPTED.** `cap17b`/`cap17c` leak `skD` only, so both are case-(a) runs | §4, **C-C7** set (1): the label becomes **red — (a) descended (`cap17b…:1243`, `cap17c…:1284`), (b) predicted on channel symmetry, never a second run**; the withdrawn label quoted. In the **2026-09-17 skeptic log**, a **dated one-line correction** is added under the S-4 entry, which is otherwise **left as written** |
| **—** | **The observers, confirmed** (not a finding) | **Entered as the observers' descent at the projection** | §(1)'s observer paragraph gains one sentence: correct control leaves the pair judge and both observers unreachable; identity-only fires the pair judge and the identity observer alone; key-only fires the pair judge and the key observer alone. **An addition; nothing is withdrawn, no set moves, and these are family-copy runs, not capstone results** |

### Scratch runs made for this repair

All four are ProVerif 2.05,
`proverif -lib formal/suite/lib/tessera_theory.pvl <copy>.pv`, `rc=0`,
on copies under `formal/suite/ledger-tests-2026-09-14/`
(**seventeenth batch** of that directory's README). All four reproduce
the reviewer's `/tmp/tessera-capstone-r13-w3lu9otg/` diagnostics on our
own tree at his own `.out` line numbers. None is an S-P3 or S-STANDING
result and none is a capstone result.

| Run | Copy of | Mutation | Result |
|---|---|---|---|
| `cap26a_sp3_degraded_publication_baseline` | `s-p3/proverif/sp3_q2_degraded_compromised.pv`, **unmutated** | link 1b's publication-provenance correspondence added as an observer; nothing else | **`is false`** (`:676`) on the **unmutated** degraded baseline; `HonestAccepted` reachable (`:376`). *This is finding 2's evidence: link 1b is a degraded **baseline cost**, not a severing, and it belongs in no degraded companion set* |
| `cap26b_ss_q1_pairjudge_correct_observers` | `cap15a_ss_q1_pairjudge_correct.pv` | the two registered isolation observers `ScopeKeyOnly(aid, lyr, kX, kA)` / `ScopeIdentityOnly(aid, lyr, id, idA)` declared beside the six-place pair judge; checks correct | pair judge, identity observer and key observer **all unreachable** (`:576`, `:583`, `:590`); witnesses reachable (`:971`, `:1361`) |
| `cap26c_ss_q1_pairjudge_identity_observers` | `cap15b_ss_q1_pairjudge_identity.pv` (identity-only scope mutation) | the same two observers | pair judge red (`:959`), **identity observer red** (`:1334`), key observer **green** (`:1341`); witnesses (`:1719`, `:2109`) |
| `cap26d_ss_q1_pairjudge_key_observers` | `cap15c_ss_q1_pairjudge_key.pv` (key-only scope mutation) | the same two observers | pair judge red (`:955`), **key observer red** (`:1340`), identity observer **green** (`:963`); witnesses (`:1719`, `:2114`). *Each observer fires on exactly its own half* |

**What did not change.** **Everything the four dispositions do not
name.** No query was added or removed and none was re-specified; no
companion and no configuration was added or removed — the count stands
at **SEVENTEEN**; no probability, residual decomposition or timebox was
altered — **26** timeboxed entries, **1155 min** per case, **4620 min**
ceiling; no set (3) and no witness moved; §5's matrix rows, producers
and consumers are untouched; the retained-query table is untouched; the
fixture and all **four contestable choices** stand, none reversed; the
**freeze statement**, the **review log**'s existing entries and the
**2026-09-15 skeptic log** are untouched, and the **2026-09-17 skeptic
log** gains a dated correction under S-4 and nothing else; and the
routed **`REFUSAL` fork** is untouched and **unresolved**, owed at the
author's commit. **What did change, stated once here: two of the skeptic
repair's own sentences are narrowed to what their runs support, one
excluded query is taken out of a degraded companion set, and the two
observers the skeptic repair declared are now descended rather than
merely declared.**

## Skeptic log (2026-09-17)

*A full non-author skeptic read of **this file as it then stood**, run
by the owner instance on 2026-09-17 evening after the twelfth Codex
round — 3,504 lines, start to finish — against
`formal/suite/ledger-tests-2026-09-14/` (batches 1–16) for every cite
spot-checked, the round-10, round-11 and round-12 records under
`docs/reviews/`, and `LEDGER.md` §6 where this file's own cites needed
resolving. The report is
`docs/reviews/2026-09-17-skeptic-read-capstone-predictions.md`; its
verdict was **not ready for the author's freeze read**, with six repairs
owed and a seventh, S-10, flagged as a build decision the file had to
make before the builder did. **Nothing was run and no model was
touched** — the reader opened 26 cited `.out` lines and found every one
as claimed, with the polarity claimed. The dispositions at the report's
head are **clerk dispositions of the owner instance**, never author
rulings; every edit made under them is **in this file only** and **none
of them changes a query, a probability, a companion's obligation, a
timebox or the routed fork**. Format, following the 2026-09-15 log:
**item — what was claimed — what the text or the run showed — what was
done.*

### Findings, and what was done with each

1. **S-1 — C-C15's set (2) listed seven relations the same row descends
   red.** *Claimed:* set (2), *“Not descended, predicted, both
   configurations”*, included C-Q5, C-Q9, links 1a, 1b, 2a and 3 and
   `SignerForged`. *Shown:* the Cases cell of the **same row** descends
   all seven **red** in (a) and (b) for configuration **(i)**, on runs
   the reader opened and verified — `cap22e…:1334`, `cap22f…:1334`;
   `cap23d…:2573`, `:1735`, `:2297`, `:2017`, `:2883`;
   `cap24b…:3211` against the green baseline `cap24a…:1421` — so
   §4's replacement rule made the builder read a registered severing as
   a broken fixture. *Done:* **repaired under S-1**, on C-C17's pattern
   — set (1) gains the eight members (seven relations) for
   configuration (i) in (a)/(b) with their existing cites carried and
   not re-derived, set (2) is **case-qualified** and the Cases lists
   govern, and the three *“memberships are … NOT edited here”*
   sentences are quoted as withdrawn.
2. **S-2 — C-Q6's degraded coverage stated three incompatible ways.**
   *Claimed:* §3's header sentence said *“degraded (d) for the
   entitled-key conjunct only”* and the timebox note said *“with the
   entitled-key conjunct also in (d)”*. *Shown:* §(5) registers conjunct
   1's honest-key forms **green** in (a), (b) and (d), conjunct 2
   **unreachable** in all three and conjunct 3 **unreachable** in all
   three, and C-C11's Cases cell already agrees with §(5); only conjunct
   1's **unrestricted** form is not asserted in (d). *Done:* **repaired
   under S-2** — both sentences brought forward to §(5)'s coverage with
   the old text quoted; §(5) is not edited.
3. **S-3 — “C-Q6 two conjuncts” in §3's timebox note.** *Claimed:* two.
   *Shown:* three since the round-3 repair added conjunct 3, and that
   repair pointed at this very paragraph. *Done:* **repaired under
   S-3**, one word, with the old word quoted and the totals stated
   unchanged — **26** entries and **1155 min** both still check.
4. **S-4 — C-C7's strict-descended unrestricted authorship red was in
   no set.** *Claimed:* set (1) was *“C-Q8 and link 4, in both
   configurations; in (i) also `AcceptedUnderHonestKey ⟹
   IssuerSigned`”*. *Shown:* `cap17b…:1243` and `cap17c…:1284` are
   both `is false` against the green strict baseline `cap17a…:555`,
   and §4's builder note about registered-red baselines covers only
   **degraded** runs. *Done:* **repaired under S-4** — the unrestricted
   `AcceptS ⟹ IssuerSigned` joins set (1) for (a)/(b) in both
   configurations as a **descended red**, old set-(1) text quoted.
   *Corrected 2026-09-17 (Codex round 13 finding 3): the red is
   **descended in case (a)** — `cap17b…:1243` and `cap17c…:1284` both
   leak `skD` only — and **predicted in case (b)** on channel symmetry,
   never a second run; the set-(1) entry now says so, and the prediction
   itself is unchanged. This entry is left as it was written.*
5. **S-5 — the status header said “Nothing has been run.”** *Claimed:*
   an unqualified all-clear. *Shown:* since 2026-09-16 the file cites
   roughly ninety family-copy diagnostics made **for** it, every one of
   them scrupulously labelled in place — but the header, which the
   author reads first, was not. *Done:* **repaired under S-5** — the
   header now says **no capstone model exists and no capstone query has
   been run**, names the diagnostics as what they are, and quotes the
   withdrawn sentence.
6. **S-6 — “the count stays sixteen” inside C-C15(iii).** *Claimed:*
   sixteen companions. *Shown:* §4's count paragraph registers
   **seventeen** and supersedes every earlier count outside the skeptic
   log and the dated repair sections; this clause carries a dated marker
   but sits in the operative §9(1) table, so whether it was superseded
   was a reading. *Done:* **recorded, and a dated clause added beside
   it** saying §4's count paragraph supersedes it; the clause is left as
   round four wrote it and what it asserts — that (iii) adds no
   companion — stands.
7. **S-7 — the round-12 disposition was not in the file.** *Claimed:*
   nothing; the file contained no occurrence of `cap25` and no
   round-twelve section. *Shown:* the reviewer's four control runs are
   reproduced in the sixteenth README batch, and his disposition said
   they were to be *“entered in the file as a dated note”*. *Done:*
   **repaired under S-7** — the dated note is in C-C15's Cases cell,
   moving C-Q7 and C-Q8 from predicted to **descended** green in (a) and
   (b) with their negative controls, and a **twelfth-round** section is
   above, in the house form.
8. **S-8 — evidence discipline otherwise holds.** *Claimed:* every
   “descended” label sits over a run that declares the query. *Shown:*
   26 opened `.out` lines across `cap8`, `cap9`, `cap11`, `cap13`,
   `cap16`, `cap17`, `cap20`, `cap22`, `cap23`, `cap24` and four
   committed family outputs all read as claimed, with no “descended”
   label over a run that does not declare its query, including the
   honest self-correction that `cap23g`/`cap23h` are **degraded**
   despite `strict` in their filenames; no probability lost its basis.
   *Done:* **recorded, no repair.**
9. **S-9 — the review log recorded one round of twelve.** *Claimed:*
   nothing false; the eleven repair sections are each dated and
   self-describing. *Shown:* a reader asking what review this file has
   been through found one bullet. *Done:* **repaired under S-9** — the
   review log gains one line per Codex round and one for this read, each
   pointing at its record under `docs/reviews/`.
10. **S-10 — conjunct 3 had one registered event and two required
    halves.** *Claimed:* C-C15(iii) put conjunct 3's identity half in
    set (1) and its key half in set (2). *Shown:* §(1) declares exactly
    **one** judge, `ScopeMisreported`, firing on `(kA, idA) ≠ (kX, id)`,
    so under one pair-form judge the two sets required one query red and
    green in a single configuration; the diagnostics that showed the
    split used two extra events, `ScopeIdentityWrong` and
    `KeyOnlyScopeWrong`, which exist in the scratch copies only. *Done:*
    **repaired under S-10, as a clerk decision of the owner instance** —
    §(1) now declares **one** registered pair judge and **two isolation
    observers**, `ScopeKeyOnly(aid, lyr, kX, kA)` and
    `ScopeIdentityOnly(aid, lyr, id, idA)`, each firing on its own
    half's inequality, queried only in the isolation configurations that
    name them, **never counted as queries, never timeboxed and never a
    discharge**; C-C15(iii)'s set (1) now names the pair judge
    **reachable** with `ScopeIdentityOnly` beside it and set (2) names
    `ScopeKeyOnly` **unreachable**, with the old “half” wording quoted.
11. **S-11 — C-C11's and C-C12's cells descended a capstone green on a
    non-capstone event.** *Claimed:* conjunct 3 green *“in both halves,
    `ScopeMisreported` and `ScopeIdentityWrong`”*. *Shown:*
    `ScopeIdentityWrong` is the diagnostic's second judge and is
    declared in no capstone registration. *Done:* **repaired under S-11
    with S-10** — both rows now cite the observers by their registered
    names, with the `.out` lines and polarities unchanged.
12. **S-12 — `ScopeReported` is the one declared event with no ProVerif
    signature.** *Claimed:* the §1.3 event table gives it as
    `aid`, `lyr`, `kA`, `idA` where five neighbouring events carry
    explicit type lists. *Shown:* the types are inferable from
    `ScopeMisreported`'s — `bitstring, bitstring, pkey, bitstring`.
    *Done:* **recorded, no repair.**
13. **S-13 — the provenance labels read correctly.** *Claimed:* four
    contestable choices and one routed fork. *Shown:* all four carry the
    required form and are gathered again in §8; the `REFUSAL` fork
    states both options and both costs and closes *“still the only item
    routed to the author, and it is still unresolved here”*; the
    model-path divergence is *“offered for veto, not routed”*; every
    ADDITION beyond §6 carries its marker; **no sentence in this file
    reads as an author ruling**, and the only block quote is A3 §A3.3,
    verified verbatim by the 2026-09-15 log. *Done:* **recorded, no
    finding.**

### What the author must read to freeze responsibly

*The skeptic's §5, carried here with the line ranges recomputed after
the repairs above. Four passages, ~2,600 words; the fifth is optional
and adds ~1,100. Passages 2–4 are the whole of what is contestable;
nothing else in this file needs the author's ruling, and the round-12
reviewer's own answer was the same list in the same order.* *(Ranges
and word counts recomputed again 2026-09-18 by the owner instance: the
round-13 edits had shifted §7 and §8 by 24 lines after this table was
first computed, and passage 4 runs to the end of the event table at
`:261`, not `:253`. The author's read, `READ-FREEZE-2026-09-17.md`,
carries these same ranges. Clerical; nothing else moves.)*
*(Recomputed a second time after the 2026-09-18 amendment and its repairs, and once more after the author's confirmations were entered the same evening, which added lines before every passage but the §1.1 rows: freeze statement `:2006-2029` (224 words), routed items `:2030-2197` (1549), rows `:77` and `:79` (621), §1.3 `:195-268` (893), §5 `:1884-1921` (1185), §7 `:1955-2003` (402), C-Q10 `:1414-1483` (615). The table below is left as it stood this morning; `READ-FREEZE-2026-09-17.md` carries the current ranges.)*

| # | Lines, this file | What it is | Words |
|---|---|---|---|
| 1 | `:1885-1906` | §8 freeze statement — what the commit does and what is owed before it | 200 |
| 2 | `:1907-2008` | §8 routed to the author — the `REFUSAL` fork with both costs (his one decision), the model-path veto, and the four contestable choices in one place | 893 |
| 3 | `:77` and `:79` | §1.1's Adversary and Wrapper rows — contestable choices 1 and 2 in their operative form, each with the run that shows the alternative changes a colour | 621 |
| 4 | `:188-261` | §1.3's `ev`-pair and report-contract paragraphs — contestable choices 3 and 4, and the `LayerAccepted` / `ScopeReported` event table | 893 |
| 5 (optional) | `:1778-1810` | §5's thirteen-row matrix — what the whole ladder buys if every prediction holds | 1,126 |

**What this read did not do.** It resolved **no** routed item: the
`REFUSAL` fork (§8, item 1) is **untouched and unresolved**, owed at the
author's commit. It changed **no** query, **no** probability, **no**
residual decomposition, **no** timebox — the **26** entries, the
**1155 min** per-case total and the 4 × 1155 = 4620 min ceiling all
stand — **no** companion count (**SEVENTEEN**), and **none** of the four
contestable choices, every one of which stands and is still contestable
by the author at the freeze commit. The **2026-09-15 skeptic log**, the
**review log**'s 2026-09-15 entry, the **freeze statement**'s substance
and the eleven earlier repair sections are **not rewritten**. Two
observers were **declared** and none was added to the query count. **No
capstone model exists; none was written; none was run**, and nothing in
the repository was run for this read.

## Amendment 2026-09-18 — the author's ruling on the `REFUSAL` fork: option (i), scoped

*Written by the owner instance on 2026-09-18, after the author's read of
`READ-FREEZE-2026-09-17.md` and his ruling on §8 item 1, entered there
verbatim. This is the only amendment this file has carried that was not
a repair after a review: it enters an **author ruling** and the
registration that ruling calls for. Everything below was entered
**before** the author's freeze commit, and the version carrying it is
re-read (skeptic) and re-reviewed (Codex round 16) before that commit,
as the freeze statement requires. **No capstone model exists; none was
written; none was run.***

### The ruling, and its scoping

Option **(i)**: the capstone exercises the `REFUSAL` signing domain
with an honest `REFUSAL`-tagged signer under the issuer key, registers
the D-6 tag-separation judge **C-Q10** and the tag-severing companion
**C-C18**. **Scoped**: the signer is a foreign-tag source and nothing
else; its body is opaque to every check; nothing about the refusal
record (A3 §A3.7.2), L2-n or E6 is modelled or claimed; `REFUSAL` is
exercised as a signing domain and unexercised as a record. The author's
words are under §8 item 1.

### Edits, by location

| Where | What |
|---|---|
| §1.1 fixture table | new row **Foreign-tag signer**, ADDITION beyond §6(4) by author ruling |
| §1.1, the L-07 paragraph | `REFUSAL` moves from declared-and-unexercised to exercised as a domain; the withdrawn wording quoted in place |
| §1.2 step 7 | the `TLR` tag check named as part of the transcribed standing path — the check C-C18 unbinds |
| §3 ladder | **C-Q10** registered after C-Q9: query, prediction green p ≈ 0.85 with basis, witnesses, 30-min box, and what it does not claim |
| §3 timeboxes | one row; **27** entries, **1185 min** per case, ceiling 4 × 1185 = 4740; the withdrawn row quoted; the two live sentences of *“What the total is, and is not”* carry the new totals with the old in parentheses; every “26/1155/4620” in dated notes is history |
| C-Q6's join, *“No new timeboxed entry”* | parenthetical carrying the new totals |
| §4, *“The count”* | **EIGHTEEN**; C-C18 named beside C-C16 and C-C17; *“C-C18 runs inside C-Q10's box”* |
| §5 | one dated sentence: C-Q10/C-C18 discharge no matrix row |
| §7 | one bullet: nothing about the refusal record |
| §8 freeze statement | the routed item marked answered |
| §8 item 1 | the ruling, verbatim, with the scoping, the non-cost, and why (ii) was never the obedient reading; the closing italic marked resolved |
| §9(5) | **C-C18** in the three-set form with Cases, descended in (a) and (d) |
| Review log | one line |
| `LEDGER.md:385`, `:1276` | dated ruling notes, each folded onto its existing line so **no ledger line number moves** (the `:1276` note was first inserted as five new lines, which shifted every `LEDGER.md:N ≥ 1277` citation in this file by five — skeptic read 2026-09-18, S-1; refolded the same day) |
| `formal/BAND0-EXIT.md` E5 | the ruling recorded |
| `formal/suite/ledger-tests-2026-09-14/README.md` | batch eighteen |

**What did not move.** Every other query, probability, residual
decomposition and timebox; the four contestable choices (§8 items 1–4
of the file's own list), which remain contestable at the commit; the
composition join; every earlier repair section and both skeptic logs,
which are history and are not rewritten.

### Scratch runs made for this amendment

Eight ProVerif 2.05 runs on copies under
`formal/suite/ledger-tests-2026-09-14/` (**eighteenth batch** of that
directory's README; the last two added after Codex round 16), each
`rc=0`, seconds each, with
`proverif -lib formal/suite/lib/tessera_theory.pvl`. Two are the
2026-09-06 reviewer's committed scratch fixtures **byte for byte** under
a provenance header; four are copies of the **committed** strict and
degraded S-STANDING models with the foreign-tag signer and the tag
judge added, correct and tag-unbound. **No repository model was edited
or run; no `.out` below is a capstone result.**

| File | Copy of | Mutation | Result |
|---|---|---|---|
| `cap27a_ss_foreign_tag_reviewer_fixture.pv/.out` | `s-standing/…/scratch/a_foreign_tag.pv`, **unchanged** | none — the reviewer's fixture (strict, DNS leaked, honest `REFUSAL` signer under `skH1`, verifier unchanged) | (i) `is true` (`:469`); (ii) both `is true` (`:479`, `:489`); (iii) unreachable (`:496`); witnesses reachable (`:793`–`:1939`); the attack unreachable (`:1953` — **the reviewer's cited line, exactly**) |
| `cap27b_ss_foreign_tag_reviewer_tlr_tag_unbound.pv/.out` | `s-standing/…/scratch/m_foreign_tlr_tag.pv`, **unchanged** | the reviewer's mutant: **only** the `TLR` tag check unbound | (i) **`is false`** (`:595`); (ii) `skH1` **`is false`** (`:734`), `skH2` `is true` (`:744`); (iii) unreachable (`:751`); witnesses reachable (`:1048`–`:2194`); the attack **reachable** (`:2340`) |
| `cap27c_ss_q1_strict_foreign_tag_correct.pv/.out` | `s-standing/proverif/ss_q1_strict_dns_compromised.pv` (**committed**, with the 2026-09-12 pin and alias judge) | `ForeignIssuer(skH1)` and the tag judge added; the standing path reports the parsed tag in parallel; **no check changed** | every S-STANDING query as committed (`:529`–`:556`); witnesses (`:855`–`:2024`); B9 (`:2031`); SS.Q6 `Aliased` unreachable (`:2038`); **`TagConfused` unreachable (`:2045`)** — C-Q10 green |
| `cap27d_ss_q1_strict_foreign_tag_tlr_tag_unbound.pv/.out` | `cap27c` | **only** the `TLR` tag check unbound — **C-C18, case (a)** | (i) `is false` (`:670`); (ii) `skH1` **`is false`** (`:824`), `skH2` `is true` (`:834`); (iii) unreachable (`:841`); witnesses (`:1140`–`:2309`); B9 (`:2316`); `Aliased` unreachable (`:2323`); **`TagConfused` reachable (`:2471`)** |
| `cap27e_ss_q1d_degraded_foreign_tag_correct.pv/.out` | `s-standing/proverif/ss_q1d_degraded_compromised.pv` (**committed**) | as `cap27c`, on the degraded model | (i) `is false` (`:666`) — **the registered degraded cost, as on the baseline** (`ss_q1d_degraded_compromised.out:640`); (ii) both `is true` (`:675`, `:684`); (iii) unreachable (`:690`); witnesses (`:976`–`:1835`); `Aliased` unreachable (`:1847`); **`TagConfused` unreachable (`:1853`)** |
| `cap27f_ss_q1d_degraded_foreign_tag_tlr_tag_unbound.pv/.out` | `cap27e` | **only** the `TLR` tag check unbound — **C-C18, case (d)** | (ii) `skH1` **`is false`** (`:807`), `skH2` `is true` (`:816`); (iii) unreachable (`:822`); witnesses (`:1108`–`:1967`); `Aliased` unreachable (`:1979`); **`TagConfused` reachable (`:2135`)** |
| `cap27g_ss_q1d_degraded_foreign_tag_envelope_observer.pv/.out` *(round 16, the reviewer's `tag_scope_control`, byte for byte)* | `cap27e` | an **envelope-side** observer `EnvelopeForeignAccepted(kX, tag)` declared beside the correct `BYTES` tag check; no check changed | every polarity as `cap27e`; the observer unreachable (`:1859`); `TagConfused` unreachable (`:1865`) |
| `cap27h_ss_q1d_degraded_foreign_tag_envelope_bytes_tag_unbound.pv/.out` *(round 16, the reviewer's `tag_scope_mutant`, byte for byte)* | `cap27g` | **only** the envelope's `BYTES` tag equality removed; the standing path and its `TLR` check untouched | the observer **reachable** (`:2016`) — a `REFUSAL` signature accepted by the envelope as an attestation — while **`TagConfused` stays unreachable** (`:2022`) and every other polarity is unchanged: **C-Q10 does not see the envelope's consumer; C-Q8 does** (C-Q10's coverage statement, §3) |

These eight results are **not** S-STANDING results and no family file
records them, and they are **not** capstone results — no capstone model
exists. They are the descent of C-Q10's prediction and C-C18's sets,
and (`cap27g`/`cap27h`) of C-Q10's coverage limit.
