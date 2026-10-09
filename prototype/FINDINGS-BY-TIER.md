# Prototype findings, by tier: one list for the author

*Owner instance, 2026-10-07. Sources: `TRIAGE.md` (71 findings), `PHASE3-REPORT.md` (18 mismatches),
`G17-REPORT.md`. 89 tests pass. Tiers follow `docs/guarantee-tiers-DRAFT.md`. "Capstone" means the composed
symbolic model must change. "Spec" means only the implementation spec changes. "Defer" means it is settled at
implementation.*

## Wrong: a model assumption shown false in reality

| # | Finding | Tier | Where the fix goes |
|---|---|---|---|
| W1 | **Signatures are malleable.** ECDSA (r, n−s) and OpenPGP's unhashed area let anyone re-form a valid signature. The attempt id hashes the signature bytes (R-3.25), so a mirror can flip an honest receipt's standing to `ABSENT`. The model treats `sign(m,k)` as unique. | T0 (all tiers) | **Spec**: allow only signatures that cannot be re-formed, or derive the attempt id from non-malleable data. **Capstone/S-STANDING**: model malleability so the proof covers it. |

## Missing: needed for the design's claims, not modelled

| # | Finding | Tier | Capstone? |
|---|---|---|---|
| M1 | **Revocation has no carrier** (G-27). Provisional direction: (B) long-term-validation capture, with (A) for late compromise. | T4 | No: P6/P9, plus a new attacker-plus-time model |
| M2 | **DNSSEC evidence doesn't name the issuer.** The root key validates every domain, and nothing checks the owner name (G-21, shown concretely). wamason.com is not DNSSEC-signed today. | T1 | Yes: the model's "one key only the issuer's channel holds" needs the owner-name check stated |
| M3 | **An OTS proof gives a range of anchor times** (four attestations, 8.6–12.6 h apart) and carries no header, time or depth. | T0 | Other model: P5's window rule needs a "which time" rule |
| M4 | **The required-set rule is underspecified** (G-17). Read literally (statement forms), the channel downgrade fails. Read as channels taken from the bundle, it succeeds (`VALID_STRICT`), shown. Smaller remaining gap: a verifier cannot require `STMT_DIRECT` over `STMT_DIGEST`. *The triage's HIGH rating overstated it: it read the set as channels.* | T2 | No: the capstone already models the fix (`capstone.pv:606-607`). Spec: one sentence |
| M5 | **"Manifest = authority tuple" holds only under a condition**, and the binding-form set is outside the hash (G-14, G-22). | T1–T2 | Yes: state the condition in the registration |
| M6 | **Per-layer verdicts have no combination rule**, and relying parties misread them (C-C5's `VALID_DEGRADED` over `INVALID`). | T2 | No: spec plus relying-party story |
| M7 | **Degraded mode cannot tell an honest receipt that lost evidence from a leaked-key attack.** | T2 | No: by design (the A4.6 cost), but it must be stated in the relying-party story |
| M8 | **The archived trust-anchor store is unnamed in the bundle**, and DNS snapshots expire within days, so captures need their own timestamp. | T4 | No |
| M9 | **KMS + GPG cannot share an algorithm cleanly** under R-3.12. | T2 | No: spec choice |

The rest of the 21 MISSING are lower-severity items in `TRIAGE.md` §4.

## Deferred to implementation

About 50 items: byte layouts (no two builds would interoperate today), JCS number-rule wording, OpenPGP
trailer handling, header-store policy, TLR delivery, and so on. The list is in `TRIAGE.md` §5 and
`PHASE3-REPORT.md`.

## What this means for the capstone

- **No capstone verdict is overturned.**
- Two registration statements are owed: M2's owner-name condition and M5's manifest condition.
- One modelling extension is owed: W1, signature malleability, most naturally in S-STANDING, with a capstone
  companion if standing's attempt id still depends on signature bytes after the spec fix.
- Everything else is spec or other-model work.
