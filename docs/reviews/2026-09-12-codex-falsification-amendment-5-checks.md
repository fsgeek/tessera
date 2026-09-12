# Codex cross-family falsification of the Amendment 5 verifier checks (2026-09-12)

**What this is.** The non-author falsification review of the three
post-freeze changes built and run on 2026-09-12 under Amendment 5
§A5.4–§A5.6: S-P2 Q6/Q6-C (common attested content), S-P7 Q7/Q7-C
(recorded inner version), S-STANDING SS.Q6/Q6-C (the tuple pin and the
alias companion). Reviewer: OpenAI Codex CLI 0.153.3, model
`gpt-6-astra`, run by the AI collaborator from the repository root with
read access to the whole tree and write access only to
`formal/suite/<family>/proverif/falsification-2026-09-12/scratch/`,
where every scratch model and its `.out` is retained (21 runs). The
prompt is archived beside each family's scratch directory
(`falsification-2026-09-12/PROMPT.md`). The review is reproduced
verbatim below the dispositions. Every factual claim it makes was
checked against the tree before disposition.

## Dispositions (collaborator, 2026-09-12)

Every `.out` line the review cites was opened before disposition. Model repairs are **comment-only, in place, same line count**, re-run the same day with the `.out` byte-identical (`cmp`) and logged in the family's `ladder.log` as `recut=header-only-2026-09-12-crossfamily out=identical`. Prose corrections are appended as dated "Cross-family review 2026-09-12 — dispositions applied" sections at the end of the affected `RESULTS.md` / `READING-AIDS.md`; existing sentences are left as written. No `PREDICTIONS.md`, library, amendment, `PROPERTIES.md`, `COVERAGE-MAP.md`, `ROUTED`/`READ-C5` file or scratch file was edited; nothing was committed.

1. **§1 — the S-STANDING pin does more than gate `ESTABLISHED` alone.** ACCEPTED-verified. `ss_q1d_degraded_compromised.pv:352` sits before `lookup2` at `:354`, so `StandingDecide` (`:296–317` — S2, S4, `MALFORMED`) and the mismatch `else` (`:357`) are downstream. Boundary sentence added to the claim block (DNS `.pv:74`, repo `:76`, degraded `:77`) and to `s-standing/RESULTS.md` item 1.
2. **§2 S-P7 — "recorded equals declared, not produced".** ACCEPTED-verified, **no change needed**: already the stated boundary at `sp7_q2_degraded_compromised.pv:139–141`.
3. **§2 S-P7 — `versionCh` reports before `InnerCheck` completes.** ACCEPTED-verified: emitted in the parallel composition after `AcceptOuter`, beside the `InnerCheck` call (`.pv:330–334`), both paths sharing the identical `InnerCheck` (`:291–309`). Header repaired at `.pv:154–155` to say the report establishes **outer acceptance**; `s-p7/RESULTS.md` item 2.
4. **§2 S-STANDING — the pin binds the embedded tuple, not the signature frame's identity.** ACCEPTED-verified (`S/minted_core.out:1853,2097`). The frame identity is checked on the envelope path (`ss_q1d_degraded_compromised.pv:374–378`); the two run in parallel and the standing path alone does not check it — `ENUMERATION` note 4 item 2 as intended. Boundary recorded in `s-standing/RESULTS.md` item 2; no model change.
5. **§3 S-P7 — the registered honest-wrapper shape is EXHIBITED.** ACCEPTED-verified, and it **closes** the open cell at `s-p7/RESULTS.md:1034–1043` ("not refuted … not exhibited"). Both literal events are reachable in the reviewer's scratch: `literal_honest_wrapper.out:1537` (`VersionLied`) and `:1815` (`AcceptInner` under `wctx(pk(skW1[]), idW1[], …)`), with the guard restored making both unreachable (`literal_correct_control.out:1063,1078`). "What the companion establishes is exactly what the addendum asked of it" corrected in `s-p7/RESULTS.md` item 4; the closure is the reviewer's.
6. **§3 S-STANDING — the committed companion trace's provenance.** ACCEPTED-verified: `ss_q6_companion_alias_unchecked.out:2224` leaks `~M_19 = skD_4` and `:2296` builds the presented DNS statement under `~M_19`; the repository side is honest (`:2226,2228`). `s-standing/RESULTS.md:1016` ("honest evidence from both channels … neither forged") and `:1023–1025` ("no forged authority evidence … **Match: exact**") misdescribe it. Correction (item 3): the term **equals** the honest publication term, the exhibited **production** differs, and honest-channel provenance is exhibited only under the reviewer's restricted-adversary diagnostic (`literal_alias_honest_channels.out:2482`). The registered trace-shape prediction is met **at the term level, not the provenance level** — a recording error, not a model defect.
7. **§6 S-P7 — "stands as written for cvI, cvW and the base path".** ACCEPTED-verified as wrong for wrapped-path `cvI`, which `.pv:330` now compares with `cvIw`. Repaired in place at `.pv:144–145`; `s-p7/RESULTS.md:964–967` corrected in item 3 of its appended section.
8. **§6.1 S-STANDING — "beyond their having separate lineages".** ACCEPTED-verified: §A5.6 as signed (`docs/phase-0-prereg-amendment-5.md:211–216`) expressly leaves one-versus-two TLRs undecided. The sentence is the one **registered in the frozen addendum** (`s-standing/PREDICTIONS.md:787–792`), so this is a divergence between the frozen plan and the signed amendment and **the amendment wins**. Headers repaired to §A5.6's wording (DNS `.pv:75–77`, repo `:77–79`, degraded `:78–80`); `PREDICTIONS.md` untouched, its sentence standing on the record as wrong; `s-standing/RESULTS.md:1197–1199` corrected in item 4.
9. **§6.2 S-STANDING — "produces no report at all".** ACCEPTED-verified as overbroad: `S/wrap_routes.out:1944` shows `noTLR` still reporting over `wrapCore`. Headers repaired (DNS `.pv:87–88`, repo `:89–90`, degraded `:90–91`) to "no lineage-derived report (no mismatch, supersession or refusal report); the no-TLR report is unaffected"; `s-standing/RESULTS.md:1203–1207` corrected in item 5.
10. **§6.3 S-STANDING — "no ABSENT or UNVERIFIABLE reason-code branch acquires a new precondition".** ACCEPTED-verified as false: `alias_reasons_correct.out:2015,2023` (unreachable) against `alias_reasons_companion.out:2604,2898` (reachable). Pin comments repaired (DNS `.pv:379–381`, repo `:381–383`, degraded `:349–351`): the aggregate witnesses are unaffected; `SUPERSEDED`, `ISSUANCE_REFUSED` and `STANDING_EVIDENCE_MISMATCH` **do** acquire the pin as a precondition for alias presentations. Recorded in `s-standing/RESULTS.md` item 6 as a checked consequence of the registered placement, not a defect; the addendum's own "five witnesses and B9 cannot move" **held**.
11. **§6 S-STANDING RESULTS — "line numbers and the added query only"; "thirteen RESULT lines".** ACCEPTED-verified: the `.out` also differs by the changed `STANDING_EVIDENCE_MISMATCH` witness trace its own `:1043–1059` records (corrected in item 7); the count is twelve (`grep -c '^RESULT'` = 12), fixed in place at `:976` with a bracketed dated note.
12. **§6 S-P2 — no overclaim.** ACCEPTED-verified, **no change needed** (`sp2_q2_degraded_compromised.pv:54–59`; `s-p2/RESULTS.md:704–752`; `diagnostics/d12_q6c_registered_witness.out:1428`). Recorded in `s-p2/RESULTS.md` item 1, where the standing obligation "the cross-family review has not been run against the amended model" is discharged.
13. **§4 removal matrix and §5 vacuity.** ACCEPTED-verified, **no change needed**; recorded as confirmations. Matrix `P2/S/matrix.txt:1–7`; witnesses `sp2_q2_degraded_compromised.out:561,778,1007`, `sp7_q2_degraded_compromised.out:865,1061`, `ss_q1_strict_dns_compromised.out:829,1114,1397,1523,1804,1993`.
14. **§7 — verdict on the §A5.4 reading (a).** ACCEPTED-verified as a design note, **no action**: mixed-version bundles are rejected (`sp2_q2_degraded_compromised.pv:229–230`, or `:219–220` first), and accepting cross-version equivalence would need its own registered decision — §A5.4 does not grant it and the P8 exclusion (`.pv:58–59`) does not authorize it. Noted in `s-p2/RESULTS.md` item 3.
15. **Outside the review — `s-p7/READING-AIDS.md:207`.** ACCEPTED-verified: the row still reads "the wrapper's authorship is S-P3 entry 1", the misattribution the author's ROUTED C5 read returned NO on (`formal/suite/READ-C5-2026-09-12.md`, "Author's answers"); model line 55 was repaired in place earlier today. Correction added to that file's appended section, and an "Author read — 2026-09-12 (ROUTED C5)" paragraph added to `s-p7/RESULTS.md` in the form of the one ending `s-p1/RESULTS.md`, recording the NO on line 55, the repair, and the re-run with the byte-identical `.out` (`ladder.log`).

**REJECTED: none.** Every finding the review raised was reproduced against the tree.


## Codex review — verbatim

## 1. Correspondence

**The new checks resisted the tested bypasses. The S-STANDING report-preservation and trace-provenance claims did not.** Evidence: removal matrix `P2/S/matrix.txt:1–7`; standing counterexamples below.

Paths: `P2/`, `P7/`, and `SS/` mean `formal/suite/s-p2/proverif/`, `formal/suite/s-p7/proverif/`, and `formal/suite/s-standing/proverif/`. `S/` means `falsification-2026-09-12/scratch/` beneath each. `A5` means `docs/phase-0-prereg-amendment-5.md`; results-document paths below are relative to `formal/suite/`.

**S-P2.** Registered sentence:

> For a multi-signer attestation, the six non-fingerprint fields of every required signer's frame — object type, algorithm, identity, manifest hash, canonicalization version, payload — are equal across signer slots; only the key-fingerprint field differs.

`A5:177–182`. The bounded two-slot verifier implements that relationship exactly: shared algorithm/identity and independently checked `h(t)` at `P2/sp2_q2_degraded_compromised.pv:221–224`; three additional equalities at `:228–230`. Each slot retains its own fingerprint. This avoids the incompatible `fa = fb` fix identified at `docs/reviews/2026-09-11-codex-pre-read-of-routed-batch-c.md:50–55`.

M2 remains reachable (`P2/sp2_q2_degraded_compromised.out:778`):

```text
RESULT not event(HonestComplete(authTuple(issuerId2[],fp(pk(skA2[])),signers1(fp(pk(skB2[]))),algH[],verH[]),verified2(k1,k2))) is false.
```

The accepted witness uses **payload `a_2` in both frames**, with `canonVerH` and distinct A2/B2 fingerprints. Earlier signer invocations use other payloads, but those are not the accepted pair (`.out:736–768`).

**S-P7.** Registered sentence:

> Registered: the verifier checks the wrapper's recorded inner version against the inner frame's own canonicalization-version field and rejects on mismatch; a lying-wrapper companion must go red.

`A5:194–196`. The pattern at `P7/sp7_q2_degraded_compromised.pv:330` implements exactly the field comparison. It also requires a parseable inner frame before `AcceptOuter`; completed inner acceptance already requires that through `InnerCheck` (`:298–300`). It establishes declared-field consistency, not production provenance.

**S-STANDING.** Registered sentence:

> Registered: the standing path checks that the presented authority tuple equals the tuple embedded in the core it derives the artifact identity from

`A5:206–208`. The pins implement this equality exactly at `SS/ss_q1_strict_dns_compromised.pv:382`, `SS/ss_q1_strict_repo_compromised.pv:384`, and `SS/ss_q1d_degraded_compromised.pv:352`.

The registered placement additionally suppresses downstream reports for mismatched/non-`attemptCore` inputs. Thus it does **more than gate `ESTABLISHED` alone**: lookup, supersession, refusal, and some malformed-report branches also depend on it (`SS/ss_q1d_degraded_compromised.pv:296–317,352–357`).

## 2. Attacks without weakening the verifier

All diagnostics here retain the verifier checks. Fixture extensions and their limits are identified explicitly.

**S-P2 — fingerprint difference versus fingerprint substitution.** The observer checks both frame inequality and disagreement with the manifest’s slot fingerprints (`P2/S/field_attacks.pv:298–310`). Different frames are reachable; wrong slot fingerprints are unreachable:

```text
RESULT not event(FrameDifference) is false.
RESULT not event(WrongFingerprint) is true.
```

`P2/S/field_attacks.out:1273,1279`. The first is permitted signer-specific framing, not a content violation.

**S-P2 — nested framed payload.** A payload that is itself a `framed()` term is accepted; two different nested payload terms cannot satisfy the outer payload equality:

```text
RESULT not event(NestedPayload) is false.
RESULT not event(NestedDifference) is true.
```

`P2/S/field_attacks.out:1524,1530`; observer `:306–310`. Acceptance of a nested constructor does not supply a second interpretation of that term.

**S-P2 — second honestly signed manifest.** I added M3 with the same two keys and a different manifest version, plus honest signing processes for M3 (`P2/S/second_manifest.pv:315–322`). Unequal accepted manifest hashes remain unreachable:

```text
RESULT not event(ManifestDifference) is true.
RESULT not event(Spliced(t_2,fa_2,fb_6)) is true.
RESULT not event(SetAltered(kH_2,m,t_2)) is false.
```

`P2/S/second_manifest.out:1648,1412,766`. The old `SetAltered` judge becomes red because this fixture violates its **one-key, one-manifest** premise; it compares acceptance with another honest manifest record. This is not a common-content bypass (`P2/sp2_q2_degraded_compromised.pv:260–266,312–320`).

**S-P7 — recorded equals declared, not produced.** An added producer signs a `cvA` frame containing `encodedUnder(cvB, payload)`; the observer restricts acceptance to I1’s key (`P7/S/production_version_v3.pv:375–391,405`):

```text
RESULT not event(DeclaredNotProduced) is false.
RESULT not event(VersionLied(fbWq,cvRec,cvAct)) is true.
```

`P7/S/production_version_v3.out:1368,1133`. This exhibits acceptance of conflicting symbolic production metadata while the two checked fields agree. **Actual canonicalization under another algorithm cannot be tested here because the model contains no canonicalization algorithm; the public tag is a surrogate, not authenticated provenance.** That limitation is registered at `P7/sp7_q2_degraded_compromised.pv:139–141`.

**S-P7 — outer acceptance with an unacceptable inner type.** With matching version fields, an outer wrapper containing a non-attestation frame can reach `AcceptOuter`, but that inner frame cannot reach wrapped `AcceptInner` (`P7/S/outer_vs_inner_v2.pv:375–383`):

```text
RESULT not event(OuterNonAttestation) is false.
RESULT not event(InnerNonAttestation) is true.
```

`P7/S/outer_vs_inner_v2.out:1353,1366`. The new destructuring introduces no completed inner acceptance absent from the base path: both invoke the identical `InnerCheck`. However, `versionCh` reports before that check finishes (`P7/sp7_q2_degraded_compromised.pv:291–309,330–334`).

**S-STANDING — A7 outer artifact.** Established standing over `wrapCore` is unreachable; a no-TLR report over it remains reachable; its mismatch-report route is unreachable:

```text
RESULT not event(Established(k,t_3,h(wrapCore(x,y)))) is true.
RESULT not event(StandingReport(ABSENT,NO_TERMINAL_DISPOSITION_EVIDENCE,k,t_3,h(wrapCore(x,y)))) is false.
RESULT not event(StandingReport(ABSENT,STANDING_EVIDENCE_MISMATCH,k,t_3,h(wrapCore(x,y)))) is true.
```

`SS/S/wrap_routes.out:1827,1944,1951`; literal queries `SS/S/wrap_routes.pv:231–236`.

**S-STANDING — adversary-minted core.** A different embedded tuple remains impossible, but a matching embedded tuple can coexist with a signature whose frame names another identity:

```text
RESULT not event(EmbeddedAlias) is true.
RESULT not event(SignatureIdentityMismatch) is false.
```

`SS/S/minted_core.out:1853,2097`; observer `SS/S/minted_core.pv:414–420`. The exhibited attacker owns the evidenced key, constructs the core and TLR, and reaches `Established` at `{138}` (`.out:2085–2093`). The standing pin binds the **embedded tuple**, not the signature’s frame identity. The separate envelope path checks that identity (`SS/ss_q1d_degraded_compromised.pv:374–378`).

## 3. Exhibit the registered S-P7 shape

**Reachable, including completed inner acceptance.** `P7/S/literal_honest_wrapper.pv:137–138` literally names W1, I1, the honest signature, `reviewPayload`, recorded `cvB`, and inner `cvA`. Top-level fresh honest keys were expressed as equivalent private free names solely to name them in queries (`:74`).

`P7/S/literal_honest_wrapper.out:1537`:

```text
RESULT not event(VersionLied(framed(OT_WRAPPER,algH[],idW1[],fp(pk(skW1[])),h(authTuple(idW1[],fp(pk(skW1[])),ssetH[],algH[],verH[])),cvB[],wrap(cvB[],(framed(OT_ATTEST,algH[],issuerId[],fp(pk(skI1[])),h(authTuple(issuerId[],fp(pk(skI1[])),ssetH[],algH[],verH[])),cvA[],reviewPayload[]),sign((BYTES,framed(OT_ATTEST,algH[],issuerId[],fp(pk(skI1[])),h(authTuple(issuerId[],fp(pk(skI1[])),ssetH[],algH[],verH[])),cvA[],reviewPayload[])),skI1[])))),cvB[],cvA[])) is false.
```

Trace: I1 receives the payload `{36}`, signs `{42}`, and publishes `{47}`; W1 receives `(cvB, honest-frame, honest-signature)` at `{93}`, signs `{98}`, and publishes `{100}`. Verifier input `{131}` reaches `AcceptOuter {139}`, report `{141} → {179}`, and `VersionLied {182}` (`.out:1497–1533`).

The additional completed-acceptance query is also reachable (`.out:1815`):

```text
RESULT not event(AcceptInner(wctx(pk(skW1[]),idW1[],framed(OT_WRAPPER,algH[],idW1[],fp(pk(skW1[])),h(authTuple(idW1[],fp(pk(skW1[])),ssetH[],algH[],verH[])),cvB[],wrap(cvB[],(framed(OT_ATTEST,algH[],issuerId[],fp(pk(skI1[])),h(authTuple(issuerId[],fp(pk(skI1[])),ssetH[],algH[],verH[])),cvA[],reviewPayload[]),sign((BYTES,framed(OT_ATTEST,algH[],issuerId[],fp(pk(skI1[])),h(authTuple(issuerId[],fp(pk(skI1[])),ssetH[],algH[],verH[])),cvA[],reviewPayload[])),skI1[]))))),pk(skI1[]),issuerId[],framed(OT_ATTEST,algH[],issuerId[],fp(pk(skI1[])),h(authTuple(issuerId[],fp(pk(skI1[])),ssetH[],algH[],verH[])),cvA[],reviewPayload[]))) is false.
```

Its trace reaches `AcceptInner {150}` after the same honest producer sequence (`.out:1767–1811`). Restoring the version guard makes **both literal events unreachable** (`P7/S/literal_correct_control.out:1063,1078`).

**S-STANDING’s committed trace is not exactly the claimed provenance.** It leaks DNS key `~M_19` at `{13}`, obtains repository evidence from an honest process, then constructs the DNS signature using `~M_19` in the verifier input. No honest DNS publication occurs in that readable trace (`SS/ss_q6_companion_alias_unchecked.out:2224–2228,2296`). The resulting signature term equals the honest publication term, but its exhibited production differs.

I therefore added a literal honest-core query and suppressed only the DNS-key disclosure to force honest-channel provenance (`SS/S/literal_alias_honest_channels.pv:177–180,371`). This restricts the adversary; a reachable trace remains available in the original companion.

`SS/S/literal_alias_honest_channels.out:2482`:

```text
RESULT not event(Aliased(pk(skH1[]),authTuple(issuerIdAlias[],fp(pk(skH1[])),ssetH[],algH[],verH[]),authTuple(issuerId[],fp(pk(skH1[])),ssetH[],algH[],verH[]),h(attemptCore(authTuple(issuerId[],fp(pk(skH1[])),ssetH[],algH[],verH[]),sign((POSS,authTuple(issuerId[],fp(pk(skH1[])),ssetH[],algH[],verH[])),skH1[]),sign((BYTES,framed(OT_ATTEST,algH[],issuerId[],fp(pk(skH1[])),h(authTuple(issuerId[],fp(pk(skH1[])),ssetH[],algH[],verH[])),canonVerH[],pReview)),skH1[]),dReview)))) is false.
```

Honest repository publication `{35}/{36}` and DNS publication `{23}/{24}` occur at `.out:2396–2402`. H1 designates the core `{58}` and releases its TLR `{61}`; input `{132}` reaches `Established {152}`, report `{155} → {191}`, and `Aliased {194}` (`.out:2466–2478`).

## 4. Single-removal matrix for the new checks only

Each equality was removed alone. For pattern guards, I replaced the equality pattern with a fresh variable, retaining destructuring. **Every check is individually load-bearing for its named query; none requires joint removal. All pre-existing query polarities remain unchanged**, including witnesses and standing’s already-failing degraded unrestricted correspondence (`P2/S/matrix.txt:1–7`).

| Scratch model run | Sole removal | Changed query; verbatim RESULT and output line |
|---|---|---|
| `P2/S/no_type.pv` | `ota = otb` | `no_type.out:1213`: `RESULT not event(Spliced(t_2,fa_2,fb_4)) is false.` |
| `P2/S/no_version.pv` | `cva = cvb` | `no_version.out:1213`: `RESULT not event(Spliced(t_2,fa_2,fb_4)) is false.` |
| `P2/S/no_payload.pv` | `pla = plb` | `no_payload.out:1213`: `RESULT not event(Spliced(t_2,fa_2,fb_4)) is false.` |
| `P7/S/no_version.pv` | inner `=cvIw` | `no_version.out:1303`: `RESULT not event(VersionLied(fbWq,cvRec,cvAct)) is false.` |
| `SS/S/no_pin_dns.pv` | standing `=t` | `no_pin_dns.out:2326`: `RESULT not event(Aliased(kX_3,t_3,tc,aid_2)) is false.` |
| `SS/S/no_pin_repo.pv` | standing `=t` | `no_pin_repo.out:2326`: `RESULT not event(Aliased(kX_3,t_3,tc,aid_2)) is false.` |
| `SS/S/no_pin_degraded.pv` | standing `=t` | `no_pin_degraded.out:2068`: `RESULT not event(Aliased(kX_3,t_3,tc,aid_2)) is false.` |

The seven matrix files above and fourteen files below are the **complete 21-model run inventory**. Every `.pv` and matching `.out` is retained. Successful runs returned 0; the two failed drafts returned 2 (`P2/S/runs.txt:3–57`, `P7/S/runs.txt:3–64`, `SS/S/runs.txt:3–116`).

| Other scratch model run | Outcome and matching `.out` evidence |
|---|---|
| `P2/S/field_attacks.pv` | Frame difference/nested payload reachable; wrong fingerprint/hash/nested difference unreachable (`:1273–1530`). |
| `P2/S/second_manifest.pv` | `SetAltered` reachable; splice/hash difference unreachable (`:766,1412,1648`). |
| `P7/S/literal_honest_wrapper.pv` | Both literal instances reachable (`:1537,1815`). |
| `P7/S/literal_correct_control.pv` | Both literal instances unreachable (`:1063,1078`). |
| `P7/S/outer_vs_inner.pv` | Parse failure: unterminated generated comment (`:1–2`); retained unchanged. |
| `P7/S/outer_vs_inner_v2.pv` | Outer non-attestation reachable; inner non-attestation unreachable (`:1353,1366`). |
| `P7/S/production_version.pv` | Same generated-comment parse failure (`:1–2`); retained unchanged. |
| `P7/S/production_version_v2.pv` | Symbolic production-tag mismatch reachable (`:1376`); unrestricted signer observer. |
| `P7/S/production_version_v3.pv` | Same mismatch reachable with observer restricted to I1 (`:1368`). |
| `SS/S/wrap_routes.pv` | Established/mismatch unreachable; no-TLR report reachable (`:1827,1944,1951`). |
| `SS/S/minted_core.pv` | Embedded alias unreachable; signature-frame identity mismatch reachable (`:1853,2097`). |
| `SS/S/alias_reasons_correct.pv` | Literal alias superseded/refused reports unreachable (`:2015,2023`). |
| `SS/S/alias_reasons_companion.pv` | Both reports reachable (`:2604,2898`). |
| `SS/S/literal_alias_honest_channels.pv` | Literal alias with honest-channel provenance reachable (`:2482`). |

## 5. Vacuity and companion exactness

**Every pre-existing honest witness remains reachable in the amended models.** The committed lines are:

| Witness | Committed `.out` lines |
|---|---|
| S-P2 M1, M2, carried honest acceptance | `P2/sp2_q2_degraded_compromised.out:561,778,1007` |
| S-P7 wrapped and base honest acceptance | `P7/sp7_q2_degraded_compromised.out:865,1061` |
| Standing N1 | DNS/repo `ss_q1_strict_*_compromised.out:829`; degraded `ss_q1d_degraded_compromised.out:950` |
| Standing five vocabulary witnesses | DNS/repo `:1114,1397,1523,1804,1993`; degraded `:1145,1341,1450,1642,1809` |

Apart from M2 quoted in task 1, their verbatim RESULT texts are:

```text
RESULT not event(HonestComplete(authTuple(issuerId[],fp(pk(skA1[])),signers0,algH[],verH[]),verified1(k1))) is false.
RESULT not event(HonestAccepted(k,fb_4)) is false.
RESULT not event(HonestWrappedAccepted(kH_3,fb,kW_3)) is false.
RESULT not event(HonestAccepted(k,fb)) is false.
RESULT not event(HonestStandingEstablished(k,aid_2)) is false.
RESULT not event(StandingReport(ESTABLISHED,TERMINAL_DISPOSITION_SHOWN,k,t_3,a)) is false.
RESULT not event(StandingReport(ABSENT,SUPERSEDED,k,t_3,a)) is false.
RESULT not event(StandingReport(ABSENT,NO_TERMINAL_DISPOSITION_EVIDENCE,k,t_3,a)) is false.
RESULT not event(StandingReport(ABSENT,ISSUANCE_REFUSED,k,t_3,a)) is false.
RESULT not event(StandingReport(ABSENT,STANDING_EVIDENCE_MISMATCH,k,t_3,a)) is false.
```

Each new companion is red **only on its named safety query**, with expected reachable witnesses excluded from “red”:

- **P2:** `Spliced` false at `sp2_q6_companion_content_unchecked.out:1213`; `Stripped`, `SignerForged`, `SetAltered`, `Reattributed` true at `:372,379,386,393`; witnesses false at `:558,779,1011`.
- **P7:** `VersionLied` false at `sp7_q7_companion_version_unchecked.out:1301`; `TypeConfused`, `Rescoped`, `InnerSigTransplanted`, `Reattributed` true at `:525,538,551,564`; witnesses false at `:866,1062`.
- **Standing:** `Aliased` false at `ss_q6_companion_alias_unchecked.out:2308`; all three correspondences true at `:505,519,530`; `StandingUnentitled` and `ReasonCollapsed` true at `:537,2004`; six witnesses false at `:836,1123,1408,1536,1819,1997`.

The named red lines, verbatim:

```text
RESULT not event(Spliced(t_2,fa_2,fb_4)) is false.
RESULT not event(VersionLied(fbWq,cvRec,cvAct)) is false.
RESULT not event(Aliased(kX_3,t_3,tc,aid_2)) is false.
```

Executable differences match the intended companion removals (`P2/sp2_q6_companion_content_unchecked.pv:173–180`; `P7/sp7_q7_companion_version_unchecked.pv:222–231`; `SS/ss_q6_companion_alias_unchecked.pv:293–304`). All archived pre-existing RESULT texts match current outputs after excluding the new queries (`P2/S/audit.txt:1–78`).

## 6. Header honesty

**S-P2:** No additional overclaim found in the ADDENDUM block’s bounded term-equality claim and explicit encoding exclusion (`P2/sp2_q2_degraded_compromised.pv:54–59`). Its results document distinguishes the generic attacker-key trace from the honest-instance diagnostic (`s-p2/RESULTS.md:704–752`; `P2/diagnostics/d12_q6c_registered_witness.out:1428`).

**S-P7:** The principal claim and production/support exclusion are bounded correctly (`P7/sp7_q2_degraded_compromised.pv:134–141`). However, the statement that the prior “checked only for presence, never for consistency or support” wording:

> stands as written for cvI, cvW and the base path

is inaccurate for wrapped-path **cvI**, which is now compared with `cvIw` through the same frame field (`:142–150,330`). The results document repeats this at `s-p7/RESULTS.md:964–967`.

The statement:

> What the companion establishes is exactly what the addendum asked of it

overstates completion of the registered shape requirement; the following prose admits the missing honest-wrapper exhibit (`s-p7/RESULTS.md:1034–1043`). Task 3 supplies that exhibit. Also, the version report establishes outer acceptance, not completion of `InnerCheck` (`P7/sp7_q2_degraded_compromised.pv:331–334`).

**S-STANDING has three substantive wording failures:**

1. **Undecided lineage policy asserted:** “beyond their having separate lineages” (`SS/ss_q1_strict_dns_compromised.pv:78–80`; repo `:80–82`; degraded `:78–80`). Amendment 5 explicitly leaves one-versus-two TLRs undecided and permits one TLR to name cores from both identities (`A5:212–216`). The results document repeats the assertion (`s-standing/RESULTS.md:1197–1199`).

2. **Overbroad silence claim:** “such a presentation now produces no report at all rather than a mismatch report” (DNS header `:86–88`; repo `:88–90`; degraded `:89–91`). Task 2’s `wrap_routes.out:1944` falsifies the unconditional wording: `noTLR` still reports. The results repeat it at `s-standing/RESULTS.md:1203–1207`.

3. **False reason-preservation rationale:** “no ABSENT or UNVERIFIABLE reason-code branch acquires a new precondition” (`SS/ss_q1_strict_dns_compromised.pv:379–380`; repo `:381–382`; degraded `:349–350`; `s-standing/RESULTS.md:914–915`). Literal alias presentations yielding supersession and refusal disappear, despite aggregate vocabulary witnesses surviving:

```text
RESULT not event(StandingReport(ABSENT,SUPERSEDED,pk(skH1[]),authTuple(issuerIdAlias[],fp(pk(skH1[])),ssetH[],algH[],verH[]),h(attemptCore(authTuple(issuerId[],fp(pk(skH1[])),ssetH[],algH[],verH[]),pp,sg_1,dc)))) is true.
RESULT not event(StandingReport(ABSENT,ISSUANCE_REFUSED,pk(skH1[]),authTuple(issuerIdAlias[],fp(pk(skH1[])),ssetH[],algH[],verH[]),h(attemptCore(authTuple(issuerId[],fp(pk(skH1[])),ssetH[],algH[],verH[]),pp,sg_1,dc)))) is true.
```

`SS/S/alias_reasons_correct.out:2015,2023`. The companion gives:

```text
RESULT not event(StandingReport(ABSENT,SUPERSEDED,pk(skH1[]),authTuple(issuerIdAlias[],fp(pk(skH1[])),ssetH[],algH[],verH[]),h(attemptCore(authTuple(issuerId[],fp(pk(skH1[])),ssetH[],algH[],verH[]),pp,sg_1,dc)))) is false.
RESULT not event(StandingReport(ABSENT,ISSUANCE_REFUSED,pk(skH1[]),authTuple(issuerIdAlias[],fp(pk(skH1[])),ssetH[],algH[],verH[]),h(attemptCore(authTuple(issuerId[],fp(pk(skH1[])),ssetH[],algH[],verH[]),pp,sg_1,dc)))) is false.
```

`SS/S/alias_reasons_companion.out:2604,2898`.

**Additional standing RESULTS errors:** “honest evidence from both channels … neither forged” and “no forged authority evidence … Match: exact” do not describe the committed trace’s DNS-key construction (`s-standing/RESULTS.md:1016,1023–1025`; task 3). “differs — line numbers and the added query only” omits changed witness traces (`:1074–1076`, contradicted by its own `:1043–1059`). “the companion’s thirteen RESULT lines” miscounts twelve (`:976`; committed companion `.out:505–2308`).

**Two line-shift samples per family checked successfully:**

| Family | Samples | Read-back evidence |
|---|---|---|
| P2 | Signer `146 → 179`; `Accept2S` `192 → 231` | `P2/S/audit.txt:79–80`, against archived reviewer baseline |
| P7 | Inner-frame check `253 → 298`; `AcceptOuter` `281 → 331` | `P2/S/audit.txt:81–82`, against archived reviewer baseline |
| Standing | DNS unrestricted RESULT `457 → 503`; N1 RESULT `781 → 829` | `P2/S/audit.txt:83–84`, against archived pre-addendum outputs |

## 7. Verdict on §A5.4 reading (a) as a design

**Reading (a) is coherent for agreement on one canonical representation. It deliberately rejects mixed-version representations even when someone considers their meanings equivalent.** The deciding checks are `P2/sp2_q2_degraded_compromised.pv:228–230`; the preserved two-key witness is `.out:768–778`.

The simplest plausible alternative is registered reading **(b)**: all required keys sign one common frame, with signer-key binding carried by its committed manifest. That removes the per-signer fingerprint difference but changes P3’s field list and P8’s frame layout (`A5:163–169`).

Consider a relying party presenting A’s original version-V frame alongside B’s frame re-canonicalized under later version V′:

- If the relying party changed B’s bytes while retaining B’s old signature, the signature check rejects first (`P2/sp2_q2_degraded_compromised.pv:219–220`).
- If B legitimately signed the V′ representation, the new version equality rejects the bundle, even if the payload terms happen to agree; differing payload terms independently fail (`:229–230`).
- If both frames claim V but one was actually produced under V′, these equalities cannot establish the truth of that production claim. Concrete canonicalization and encoding obligations remain with P8; the symbolic model compares terms (`P2/sp2_q2_degraded_compromised.pv:58–59`; `P7/sp7_q2_degraded_compromised.pv:139–141`).

Thus the visible mixed-version bundle is handled by rejection. Any policy accepting cross-version semantic equivalence would require an additional registered design decision; the present P8 exclusion does not authorize accepting it.