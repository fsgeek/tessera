# Disposition: Levadura's contradiction search of the V1 rules

> **OWNER DISPOSITION, 2026-10-19** (Claude Opus 5.5, owner's editor for the V1 spec texts). Input:
> `/home/tony/projects/levadura_salvaje/docs/requests/2026-10-16-reply-to-tessera-contradiction-search.md`
> (10 confirmed, 6 contested, plus one preface finding). Also disposed here: V1-PROFILE §14.2 item 9, the stale
> signer-branch lines, and the listing cut (`docs/decisions/2026-10-19-listing-cut.md`).
>
> **House rules applied.** Registered texts were not edited: the prereg and amendments (A9, A10), and
> `formal/p8/HYBRID-SUPPLEMENT.md` and `HYBRID-REGISTRATION-RECORD.md`. Where an editable text contradicted a
> registered one, the editable text was fixed. Where two registered texts contradict each other, a reconciliation
> note was added to V1-PROFILE §13. Every edit is tagged `[OWNER 2026-10-19]` in place.

## Re-check against the current files

Levadura read a working tree of 2026-10-16 ~21:00Z. On 2026-10-19, before any edit, all four texts still had the
hashes Levadura recorded:

| File | SHA-256 on 2026-10-19 | Same as Levadura's copy |
|---|---|---|
| `docs/phase-0-prereg-amendment-9.md` | `ff09f9b1…9c05` | yes |
| `docs/V1-PROFILE.md` | `08bf1918…220f` | yes |
| `formal/p8/ENCODING-V1.md` | `fe537b1f…efd0` | yes |
| `formal/p8/HYBRID-SUPPLEMENT.md` | `6e7e02ff…ce9c` | yes |

So every finding was live as read. One thing changed around them: **A10 was signed** by the author's commit
`9ade764` (2026-10-18). A10.5 settles contested item 2, and A10 rows 5, 6 and 33 bear on the profile (below).

## Counts

Levadura's 17 items (10 confirmed, 6 contested, 1 preface):

| Disposition | Count | Items |
|---|---|---|
| FIXED | 9 | C1, C2, C3, C4, C5, C6; contested 1, 5, 6 |
| ALREADY FIXED | 2 | preface (supplement not in git); contested 2 (by A10.5; citation added) |
| RECONCILED (§13 note) | 6 | C7, C8, C9 (one note), C10 (note 8), contested 3 (note 9), contested 4 (note 10) |
| REJECTED | 0 | |

Also done: the rest of profile §14.2 item 9 (G18, G28, G38 and the G37 accounting), the listing-cut statement and
cut order, one contract fix (V1-CONTRACT G9's source), and one new §13 note (11) for a consequence of these edits.

## Confirmed by both verifiers (10)

| # | Finding | Disposition | Where |
|---|---|---|---|
| C1 | ENC §7.1 "fixed … before any receipt that relies on it" vs A9 C4 non-claim | **FIXED** (G02 CORRECT) | ENC §7.1: replaced with chain-order pre-commitment (h_git + 5 < h_receipt) and A9 C4's "DNSSEC evidence establishes no publication before issue". Profile §6.3's pending note now says done. |
| C2 | ENC §3.2 "V1 issues OPENPGP4-ECDSA-P256-SHA256" vs supplement §1 (classical id policy-unsupported under hybrid) | **FIXED** | ENC §3.2: the comment now says "the catalog id", and a new bullet names the pair id and the classical id's `UNVERIFIABLE / ALG_UNKNOWN`. The supplement is registered and governs; its superseded-statement list omitting §3.2 needed no note once ENC agrees. |
| C3 | Profile §1 "OPEN: not yet taken" and §14.1 "still open" vs §8 "Branch taken: HYBRID" | **FIXED** | Profile §1 "Branch recorded", §8 hybrid bullet, §14.1 lead paragraph, §14.2 item 4 (closed). |
| C4 | ENC §7.2 "That commit adds the assertion blob" vs profile §15.4 "Not checked: that the commit introduced the blob" | **FIXED** | ENC §7.2: "That commit's tree contains the assertion blob at the profile path … Whether this commit introduced the blob is not checked." A9.5's git stamp target says only commit→tree→blob, so nothing registered required "adds". |
| C5 | ENC §8 "single in-profile UNVERIFIABLE" vs the profile's further in-profile UNVERIFIABLE outcomes | **FIXED** (G01) | ENC §8: "single **codec-level** in-profile UNVERIFIABLE", with a pointer to profile §3.1 item 5. |
| C6 | ENC §2 "Every V1 byte string that a V1 key signs or that OTS stamps begins with the same header" vs A9.5's git stamped message (40 hex + LF) | **FIXED** | ENC §2: the sentence is scoped to slot-key signatures and the two tagged OTS preimages; it names the git stamped message and the TXT value as untagged. ENC §0's "Nothing else … is signed or anchored directly" gets the same exception (the same defect, found while fixing C6). |
| C7 | A9.7 rows 22–23 omit SPEC V6 | **RECONCILED** | Profile §13: note 5 existed; a 2026-10-19 note covering notes 1, 5 and 7 says A9 governs and why: A9.8 replaces the rule for the profile outright, so A9.7's incomplete list keeps no SPEC sentence alive. Two registered-side texts are not edited. |
| C8 | A9.7 rows 7–9 omit SPEC R-5.21 | **RECONCILED** | Same note (A9.4 governs). |
| C9 | A9 C4 "verifier fixes the required set" vs SPEC R-3.37/V21; no A9.7 row | **RECONCILED** | Same note (A9 C4 governs; profile §6.4 G-17 already follows it, with exact equality to `["STMT_DIRECT"]` satisfying R-3.37 too). |
| C10 | Supplement §10.4 "Met 2026-10-14" vs §11 "still owed" (same registered text) | **RECONCILED** | Profile §13 note 8: §10.4 and the registration record's item 4 govern (`prototype/policy-signer/EVIDENCE.md`); §11 is the pre-evidence state frozen into the byte-identical body. |

## Contested (6): owner decisions

| # | Finding | Decision | Where |
|---|---|---|---|
| 1 | ENC §7.1 "earliest" vs A9 C5 "lowest block height" | **FIXED.** The Opus verifier is right that A9 C5 defines "earliest" as chain order, but the word is a trap for a reader of ENC alone, and the profile's own dated correction says the two readings can give different verdicts. Removed the trap. | ENC §7.1: "the header time of the qualifying attestation at the **lowest block height** … (A9 C5; A10.5's stages)". |
| 2 | A9:156 "header outside the pins → HEADERS_NOT_COVERED" vs profile G23 `HEADER_CONFLICTS_PIN` | **ALREADY FIXED** by registered text. A10.5 stage 1 (signed 2026-10-18) states exactly the profile's split as A9's meaning. | Profile §7.2 now cites A10.5; §13 note 12. |
| 3 | A9.6 requires the supplement to name the exact spec hash; the supplement says "entered at the 30 Oct freeze" | **RECONCILED.** Real, and it cannot be cured before the freeze: the spec object exists only at freeze assembly. A9.6 governs; its own deadline for the registration is "before the 30 Oct freeze", so the registration is complete only when the freeze record enters that hash. | Profile §13 note 9; §14.2 item 7 now carries the obligation. |
| 4 | A9.7 tally "plus one disposition left open" vs A9's "OWNER DECISION 2026-10-12: public publication remains an issuer duty" | **RECONCILED.** Real but harmless: the tally is stale wording. The dated OWNER DECISION governs; the item is uncounted, not open. | Profile §13 note 10. |
| 5 | ENC §5.3 "UNVERIFIABLE: the algorithm id is not registered" (two senses of "registered") | **FIXED.** Removed the trap. | ENC §5.3: "`UNVERIFIABLE` (`ALG_UNKNOWN`): well-formed but not the installation's catalog-supported id"; codec-known is not policy-supported. |
| 6 | Profile 344 paths / 127 proofs vs 352 / 129 | **FIXED.** Not a rule conflict, but two unexplained counts invite one. | Profile §15.2: the first count is dated to RES G20 and pointed at the later check. |

## Preface finding

- **The supplement was untracked when read.** **ALREADY FIXED:** `HYBRID-SUPPLEMENT.md` and
  `HYBRID-REGISTRATION-RECORD.md` were committed in `ad0ab70`; the supplement's hash equals the record's
  (`6e7e02ff…ce9c`).

## Profile §14.2 item 9 (ENCODING-V1 and PROOF wording edits)

| Source | Edit | Disposition |
|---|---|---|
| G01 (E§8 "codec-level") | as C5 | FIXED |
| G02 (E§7.1 CORRECT) | as C1 | FIXED |
| G18 (E§3.2 grammars) | ENC §3.2 "Field grammars" bullet (years 0001–9999; LDH label rule; ≤ 241 bytes); ENC §7 ABNF comment (years) | FIXED |
| G28 (E§5.2 subpacket lengths) | ENC §5.2 rule O: RFC 9580 §5.2.3.7's three forms, shortest only, V1 rule | FIXED |
| G38 (E:147-148, D-1, PROOF §6) | ENC §1.2 and D-1: "A9.8 registers it"; PROOF §6: the "not registered yet" bullet replaced | FIXED |
| r2-contra: E§7.1 "earliest" | as contested 1 | FIXED |
| r2-contra: E§7.2 "commit adds blob" | as C4 | FIXED |
| G37 change accounting | ENC CHANGELOG 2026-10-19 entry: wording only; no codec rule, code, order, golden byte or vector changes; the governing baseline stays ENC at `2ad3489` plus the supplement | FIXED |

Two stale baseline statements that the registered supplement says stay "the baseline's text, unedited" (ENC §8's
PQ scope bullet; PROOF §6's rule-R bullet) were **annotated, not rewritten**, so the supplement's direction is kept.

Profile §14.2 item 9 is marked done; profile §6.3, §10 (twice) no longer say "pending".

## Listing cut (`docs/decisions/2026-10-19-listing-cut.md`)

- **Added** to profile §5 a bullet "No service-key listing in V1": A10.4.1 is cut under A10 row 33 with rows
  25–32 and 37–39; A10.4 option (a) applies; **V1 gives no protection against new receipts under a captor's own keys
  when both authority channels are captured**; A10.4.2 custody is unchanged.
- **Listing text to remove:** none. A search of the profile, ENC and PROOF for `service_keys`, listing subchecks,
  listing codes, C0/C1 and the listing-evidence package found nothing; the profile never implemented A10.4.1. The new
  bullet says each piece is not in V1.
- **Fixed** profile §12's cut order ("the PQ hybrid first, nothing else"), which A10 row 33 replaced.
- Added A10 to the profile's source table (§0) so the tags resolve.
- **V1-CONTRACT.md:** consistent with the cut (its "No G11" paragraph and §4 row already say the same). One
  contradiction found and fixed: G9's source cell cited `A10:558`, which is a **listing subcheck row** of the cut
  A10.4.1. It now cites A9.5 trust-configuration authority and profile §5 (`TRUST_CONFIG_UNAUTHENTICATED`), where the
  refusal rule actually lives. Nothing else in the contract changed.

## New §13 note caused by these edits

- **Note 11.** The registration record names ENC after the §5.2 edit as `fe537b1f…efd0`; this disposition changes
  ENC's hash. The registered baseline governs, and the edited ENC replaces it only through the freeze record with
  the CHANGELOG as change accounting (G37). §14.2 item 7 now asks the freeze record to name both hashes.

## Further contradictions noticed (listed, not fixed)

1. **A10.1.1 is not in the profile.** A10 rows 20–22 (signed) add `utc_assessment` (`assumption_id
   "A-UTC-7200-6"`, `utc_upper_bound`) outside the stable six, with Δ = 7200 s and m = 6 frozen in the
   specification catalog. Profile §1's catalog entry lists its contents without Δ and m, and §3.4's report encoding
   has no `utc_assessment`. V1-CONTRACT G6 depends on it and already says it is not built. A10's open items assign
   this profile reconciliation; it is new mechanism, so it is the largest remaining profile gap before the freeze.
2. **Profile §11 safe decisions vs A10 rows 5–6.** Rows a, g ("presented to Tessera by T") and i ("existed by T")
   keep A9's wording that A10 replaced with "before the selected Bitcoin block was mined; its header time T is not
   a UTC upper bound".
3. **PROOF Theorem (iv)(d)** says `SHA256(A_sig)` "existed by time T" and the signatures "existed by T". It is
   qualified by "chain-time residuals", but A10.1's reading is "existed before the selected block was mined; T is
   chain time". Not a P8 claim ((iv)(d) is C5's), so it does not block the P8 falsification attempt. One sentence.
4. **Profile §14.2 items 1–2 timing vs A10.4.2 (rows 34–36).** The profile lists release-key custody and the
   release format as "still open before 30 Oct"; A10.4.2 moves the custody gate to the first public verifier release
   and adds the TEST-release-key rule. A10's open items assign this reconciliation.
5. **Stale A9 status in the profile.** The STATUS block calls A9 "PROPOSED", §0's table says "(PROPOSED)", and §0
   says "Nothing binds until the author signs A9". A9 was signed at `2ad3489` (2026-10-16). The same is true of
   §0.1's "Until the freeze they are proposals".
6. **Profile §14.2 item 5 (slot-2 custody)** is still open, while the registered supplement (§11, resolved item 2)
   and the registration record name the GCP Cloud KMS HSM through the policy signer. The dated custody entry in the
   profile that A9.6 asks for is not yet written.
7. **PROOF (K)** says each slot key signs "as OpenPGP type-0x00 documents"; under the hybrid the kms slot signs raw
   FIPS 204. The supplement's (K-R) governs for that slot and ENC §5.2 says so, and the supplement directs that
   PROOF (K) stay unedited. A reader trap, not a governing conflict.

## Readiness for a falsification attempt

**ENCODING-V1 and PROOF are ready for their P8 falsification attempt.** Every known contradiction inside or between
them, and between them and A9, A10 or the supplement, is fixed or reconciled, except further item 3 (PROOF (iv)(d)
wording, a C5 matter that P8 explicitly does not claim) and item 7 (a reader trap governed by the supplement). The
2026-10-19 edits change no accepted set, so the vectors and the agreement-run results stand. The attempt should
read ENC with the registered supplement (rule R and the pair id) and be told that PROOF §6's rule-R bullet is
superseded for the hybrid by supplement §8.
