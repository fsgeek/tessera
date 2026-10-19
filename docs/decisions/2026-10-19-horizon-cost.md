# What the 2106 horizon costs V1, and what a 10-year horizon would change (2026-10-19)

> **Status: OWNER ANALYSIS, not a decision.** Written by the owner instance (Claude Opus 5.5) at the owner's
> request. Every statement in this file is OWNER ANALYSIS unless it quotes the record, and each claim about the
> record cites file:line. Estimates are labelled **[doc E]** when a cited document gives them and **[owner E]**
> when they are mine and unmeasured. Nothing here changes a registered sentence. Sources read: A9, A10 (signed at
> `9ade764`), `docs/V1-PROFILE.md`, `docs/V1-SCHEDULE.md`, `docs/V1-V2-COMPATIBILITY.md`,
> `docs/V1-RELEASE-KEY-CUSTODY-DRAFT.md`, both `docs/decisions/2026-10-17-*.md`, plus the A1, A3 and A4 lines cited.

## 1. In plain words — OWNER ANALYSIS

**Two properties, often blurred.**
- *Exit survival:* a receipt can be checked with Tessera gone. No server, no help from us.
- *Horizon length:* how many years after issue that check still works and still means something.

They are independent. A receipt can survive our exit and still fail after 15 years, because an algorithm weakens or
a standard is lost. The author's distinctive claim is the first one.

**What the long horizon is for.** The record imagines an adjudicator decades later, deciding on what survives.
The author: *"In 2106, Tessera won't exist in its current form and the only honest story is the adjudicator will
have to make the decisions based upon the information available to them"* (`docs/phase-0-prereg-amendment-4.md:173-177`).
Typed verdicts exist because *"Tessera cannot know the policy of a party eighty years out"*
(`docs/key-decisions.md:71-72`). It serves a relying party who is not born yet: a court, an archivist, an heir.

**What the record already says about the horizon.** It is softer than the "2106 examiner" label suggests.
- *"The century horizon is aspirational, not a guarantee or membership criterion"* (`docs/phase-0-prereg-amendment-3.md:322-326`).
- Long-horizon continuity needs renewal by custodians (`docs/phase-0-prereg-amendment-3.md:273-278`). V1 offers no
  renewal (`docs/phase-0-prereg-amendment-9.md:343-344`); renewal is a carried-forward obligation
  (`docs/phase-0-prereg-amendment-9.md:239`).
- The clean-room "dead-project" demonstration is not run for V1. The dead-service test is
  (`docs/phase-0-prereg-amendment-9.md:482`, row 18; `:216`).
- So V1's registered 4 Dec test is an **exit-survival** test. "2106-examiner test" appears only in the schedule's
  milestone table (`docs/V1-SCHEDULE.md:28`); A9, which governs, calls it the dead-service test
  (`docs/phase-0-prereg-amendment-9.md:216`).

**Consequence.** No V1 claim names a horizon. Most of V1's complexity comes from exit survival and from the
authority-capture adversary, not from the year 2106. A small set of items is horizon-driven. One of them is large.

## 2. Mechanism by mechanism — OWNER ANALYSIS

Driver key: **EXIT** = verify with Tessera gone; **CAPTURE** = the authority-capture adversary; **AGREE** = two
verifiers must give the same answer today; **HORIZON** = needed mainly for decades-later use; **PREF** = author preference.

| # | Mechanism | Main driver | Effort / schedule cost | Under a 10-year horizon |
|---|---|---|---|---|
| 1 | Self-contained bundle: DNSSEC snapshot with its own OTS proof, raw git objects and stamp, receipt proof and headers (`docs/V1-V2-COMPATIBILITY.md:26-35`) | EXIT | Built; differential run agrees 342/342 (`docs/handoff-2026-10-18-owner-tessera-e4.md:23-25`) | **Keep.** This *is* exit survival. |
| 2 | Spec, vectors and purpose preamble inside every bundle, hashes in the signed bytes (`docs/V1-PROFILE.md:168-170`; A3 at `docs/phase-0-prereg-amendment-3.md:292-302`) | EXIT, partly HORIZON | Sunk; in P8's signed bytes | **Keep.** Removing it reopens P8 and needs an amendment. |
| 3 | Root KSK history with signing and reliance periods (`docs/phase-0-prereg-amendment-9.md:309-325`; `docs/V1-PROFILE.md:412-455`) | EXIT. DNSSEC must be judged at a past time; a root RRSIG lives about 21 days (`docs/V1-PROFILE.md:445-450`) | **[doc E]** 1 d for snapshot and two-KSK config (`docs/V1-DERIVATION-DRAFT.md:309`); still open: sourcing KSK-2017's start (`docs/V1-PROFILE.md:508-518`) | **Keep.** Needed even at a one-month horizon. KSK-2017 signed for 8 years (`docs/V1-PROFILE.md:441-442`, `:513`), so a 10-year horizon likely spans another rollover. |
| 4 | Repository-key entries with signing intervals; append-only trust file (`docs/phase-0-prereg-amendment-9.md:333-342`) | EXIT, and V2 migration (`docs/V1-V2-COMPATIBILITY.md:67-88`) | Sunk | **Keep.** |
| 5 | Bitcoin header pins: every header pinned, no proof-of-work logic (`docs/phase-0-prereg-amendment-9.md:154-157`; `docs/V1-PROFILE.md:820-834`) | EXIT plus simplicity. HORIZON adds a reason: the history must stay intact "over the adjudication horizon" (`docs/phase-0-prereg-amendment-1.md:505-511`) | **[doc E]** 0.75 d (`docs/V1-DERIVATION-DRAFT.md:310`), built. **Ongoing:** a receipt above the newest pin is unverifiable until a release adds pins, and every release goes through release-key custody (`docs/V1-OPERATIONS-RUNBOOK.md:137-140`). No release cadence is decided anywhere. | **Keep in V1** (registered in A9). Proof-of-work from a pinned checkpoint would end per-receipt pin releases and suits a short horizon, but it needs an amendment and new verifier logic. Record it as a V2 candidate. Batch pin releases (operating choice). |
| 6 | SHA-1 git objects, SHA-1DC pinned (`docs/phase-0-prereg-amendment-9.md:299-301`; `docs/V1-PROFILE.md:1222-1224`) | AGREE; GitHub has no SHA-256 (`docs/V1-V2-COMPATIBILITY.md:39-42`) | Part of item 15 below | **Keep.** A shorter horizon makes the SHA-1 second-preimage residual (`docs/phase-0-prereg-amendment-9.md:50-51`) less worrying. |
| 7 | Unicode 16.0.0 pin, NFC rejected not normalized (`formal/p8/ENCODING-V1.md:103-106`) | AGREE (two verifiers on different Unicode versions could disagree) | Sunk | **Keep.** Not horizon-driven. |
| 8 | Dependency manifest schema: edition, sections, errata, digest, retrieval, redistribution, failure consequence (`docs/V1-PROFILE.md:975-977`) | EXIT; A3's rule is to *disclose* dependencies (`docs/phase-0-prereg-amendment-3.md:362-365`) | Schema done | **Keep.** |
| 9 | Dependency closure: build and archive the referenced normative bytes and tables (`docs/V1-PROFILE.md:1219-1225`, item 15) | Mostly HORIZON (offline reconstruction from documents alone, the dead-project idea) | No doc estimate. **[owner E]** 2–4 owner-days for full archiving; about 1 d for editions, digests and the SHA-1DC pin alone | **Weaken (owner level).** Pin editions and digests for all; archive only the at-risk few (SHA-1DC source, git object and signature formats, OTS file format, Bitcoin formats). Disclose the rest, as A3 asks. |
| 10 | Service-key listing: tuple classifier, closure invariants (A10.4.1, `docs/phase-0-prereg-amendment-10.md:467-486`) | CAPTURE (the author's visibility standard, `:407-413`) | **[doc E]** 4–5 owner-days with the UTC item (`docs/decisions/2026-10-17-utc-bound-and-capture-visibility.md:30`, `:348-363`) | **Keep.** Not horizon-driven. |
| 11 | **Listing chain-order pre-commitment:** release stamping, C0/C1 bootstrap, listing-evidence package, 3 subchecks, 4 reason codes, independent Bitcoin history (`docs/phase-0-prereg-amendment-10.md:488-575`) | **HORIZON.** Its stated gap: *"A release key stolen decades later can sign a forked … release chain"* (`:493-494`). It came from the author's question on how a 2106 adjudicator knows the listing (`docs/reviews/amendment-10-r4/AUTHOR-RULINGS.md:5-6`) | Not in the 4–5 d estimate, which predates it. **[owner E]** 2–3 owner-days in profile, two verifiers and vectors; one extra production release (an author ceremony) and about one hour of confirmations before the first receipt (`:516-525`); a lasting holder preservation duty (`:548-550`) | **Split.** Keep the issue-side evidence: stamp every release and run C0 before the first receipt. Skipping it is irreversible (section 3). Keep the verifier check as signed. Build no tooling for "independently authenticated history"; it is already a stated non-claim (`:503-509`). |
| 12 | Release-key custody and the first-public-release gate (A10.4.2, `docs/phase-0-prereg-amendment-10.md:612-676`) | CAPTURE (A9.5 trust authority, `docs/phase-0-prereg-amendment-9.md:326-332`) | No doc estimate; *"The time for one release is an estimate until rehearsal measures it"* (`docs/V1-RELEASE-KEY-CUSTODY-DRAFT.md:300`). Author's November time accepted (`docs/phase-0-prereg-amendment-10.md:663-664`) | **Keep.** Only the long-lived extras are horizon-flavoured. For loss of all copies, take the draft's option "V1 has no assured recovery path and new releases stay stopped" (`docs/V1-RELEASE-KEY-CUSTODY-DRAFT.md:316-319`) rather than designing an independent recovery channel. |
| 13 | A-UTC and `utc_assessment` (A10.1.1, `docs/phase-0-prereg-amendment-10.md:266-356`) | Examiners and courts want UTC (`docs/decisions/2026-10-17-utc-bound-and-capture-visibility.md:177-179`) | **[doc E]** about 1 d (`:173`); the 2106 widening is part of a 0.25 d row (`:351`) | **Keep.** The 2106 arithmetic is trivial. |
| 14 | RRSIG serial arithmetic, "never now, including in 2106" (`docs/V1-PROFILE.md:868-873`) | AGREE (RFC 4034 requires it anyway) | Trivial | **Keep.** |
| 15 | ML-DSA-65 hybrid slot (`docs/V1-PROFILE.md:900-902`) | PREF (`docs/phase-0-prereg-amendment-9.md:101-102`); its security value is mostly HORIZON (`:262-265`) | Done; registered 2026-10-16 | **Keep.** Sunk cost. |
| 16 | Append-only trust file and the verdict-stability contract (`docs/phase-0-prereg-amendment-9.md:267-283`) | Later verifiers and V2 migration (`docs/V1-V2-COMPATIBILITY.md:141-179`) | Sunk | **Keep.** Needed at any horizon beyond one release. |
| 17 | Renewal (RFC 4998), revocation status capture | HORIZON | Already deferred (`docs/phase-0-prereg-amendment-9.md:236`, `:239`) | **No change.** This is already where the long horizon lives. |
| 18 | RFC 3161 tokens (U2); a witnessed log | Candidates only | **[doc E]** 6–9 owner-days (`docs/decisions/2026-10-17-utc-bound-and-capture-visibility.md:161`); log "weeks", with "2106-lived witness keys" (`:266`) | **No change.** Not built either way. |

**Reading the table.** Items 9 and 11 are the horizon-driven costs still ahead. Item 15 is horizon-motivated but
already paid. Everything else is driven by exit survival, capture or verifier agreement. It stays under any horizon
that includes "Tessera is gone".

## 3. What a shorter horizon costs in claim strength, and what is irreversible — OWNER ANALYSIS

**Claim strength.** Small, because V1 registered none.
- No C1–C7 sentence names a horizon (`docs/phase-0-prereg-amendment-9.md:128-146`). A stated 10-year design horizon
  changes no verdict, reason code or stable field.
- What changes is the relying-party text. Today it implies a 2106 reader. It should say: designed to be checked
  without Tessera for at least 10 years; beyond that, it depends on the listed dependencies, on Bitcoin history
  staying available (`docs/phase-0-prereg-amendment-1.md:505-511`), and on renewal, which V1 does not offer.
- Under item 9's weakening, a distant examiner may have to find some standards on their own. A3 already accepts
  this as an *"exposed Designated Community assumption"* (`docs/phase-0-prereg-amendment-3.md:362-365`).
- Under item 11 as recommended, nothing is lost. If the pre-commitment were removed instead, key-substitution
  protection would hold only while the release key is uncompromised. That is the existing distribution boundary
  (`docs/phase-0-prereg-amendment-10.md:597-599`).

**Irreversible: what no V2 can add to a V1 receipt later.** Only evidence that must exist at issue time.
- **Release stamps before the first receipt.** If V1 does not stamp the listing release before its receipts, no
  later verifier can prove the listing came first. Cheap now; impossible later. This is why item 11 keeps it.
- **Revocation status at issue.** Not captured (`docs/phase-0-prereg-amendment-9.md:253-258`). Already a non-claim.
- **An independent clock witness (RFC 3161).** Not captured; a later token proves nothing about 2026. Already a
  recorded candidate only (`docs/phase-0-prereg-amendment-10.md:351-354`).
- **At-risk dependency bytes.** If SHA-1DC's exact source or a format document disappears before anyone archives
  it, that is permanent. Hence "archive the at-risk few" in item 9.

**Reversible: what a V2 can extend.**
- Algorithm ageing (P-256, ML-DSA-65, SHA-1 links, SHA-256). A custodian can wrap a V1 receipt before the
  mechanism weakens (`docs/phase-0-prereg-amendment-3.md:273-278`). V1 already supports this: the receipt identity
  is SHA256(A_sig) (`docs/V1-PROFILE.md:1000-1005`), and the container is canonical. The limit: only receipts that
  someone keeps and wraps in time are extended. A receipt left in a drawer for 30 years is not.
- Header pins. Later releases can add pins (append-only, `docs/phase-0-prereg-amendment-9.md:333-336`).

## 4. Recommendation — OWNER ANALYSIS

**Name the horizon; do not rebuild V1 around it.** The shorter horizon buys back little, because most of V1's
weight is exit survival and capture protection. Those stay.

**Owner-level, no amendment:**
1. **State a V1 design horizon of 10 years** in the profile and the relying-party text, with the sentence in
   section 3. This is a CLARIFY. It agrees with A3's "aspirational" century (`docs/phase-0-prereg-amendment-3.md:322-326`).
2. **Relabel the 4 Dec test** "dead-service test (Tessera off)", as A9 already names it
   (`docs/phase-0-prereg-amendment-9.md:216`). Correct `docs/V1-SCHEDULE.md:28` with a dated note.
3. **Narrow dependency closure** (item 9): editions, digests and the SHA-1DC pin for all; archive only the at-risk
   few; disclose the rest. It stops being a freeze gate. **[owner E]** saves 1–3 owner-days.
4. **Implement A10.4.1 at its signed scope, no wider** (item 11): stamp every release, C0/C1 before the first
   receipt, the verifier subchecks. No independent-history tooling; relying-party text only.
5. **Custody recovery** (item 12): take the "no assured recovery path; releases stop" option.
6. **Decide a pin-release cadence** in the runbook (item 5). Each release costs the author a ceremony. It is not a
   horizon question, but the gap is real.

**Would need an amendment (recommended against now):**
- Removing or moving the listing pre-commitment (A10 rows 37–39, `docs/phase-0-prereg-amendment-10.md:773-775`).
  It saves **[owner E]** 1–2 owner-days and costs a review cycle; A10 grew to 32 pages under review
  (`docs/handoff-2026-10-18-owner-tessera-e4.md:66`). The issue-side half must stay in any case.
- Replacing pins with proof-of-work (`docs/phase-0-prereg-amendment-9.md:154-157`). A V2 candidate.
- Dropping the in-bundle spec and vectors or the hybrid. Sunk; no saving.

**Registering the long horizon for V2.** It is already registered. Renewal and long-term validation are carried
obligations (`docs/phase-0-prereg-amendment-9.md:236`, `:239`), and A3 keeps the century as an aspiration. No new
amendment is needed. If the author wants the words "long horizon" on a V2 obligation, fold them into the next
amendment that is needed anyway, such as a successor-window registration (`docs/phase-0-prereg-amendment-9.md:410-418`).

**The two biggest horizon-attributable items.**
1. The listing's chain-order pre-commitment and its evidence package (A10.4.1). It is the one mechanism added
   explicitly for a decades-later adjudicator.
2. Dependency closure (profile §14.2 item 15): archiving normative bytes so that the procedure can be rebuilt from
   documents alone. This is the dead-project property, which V1 does not test.
