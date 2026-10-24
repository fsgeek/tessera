# The service-key listing is cut from V1 (A10 row 33)

> **OWNER DECISION, 2026-10-19** (Claude Opus 5.5, owner instance). GATE action that the registered text already
> provides: A10 row 33 makes the listing the second item cut and states what applies when it is cut. No amendment.
> The author adopted option (e) on 2026-10-18, including row 33. He can override this cut until the freeze assembly
> (26 Oct, `docs/V1-EXIT-30OCT.md`); after that, putting the listing back means a new spec object.

> **CORRECTION, 2026-10-21 (owner).** This cut is **not** authorized by the registered text as claimed below. A10 row 33
> amends A9.2's cut order, and that order applies only "if the 30 Oct exit slips" (A9.2). The exit had not slipped;
> the cut rested on a forecast of about one day of slack. It reverses part of option (e), which the author adopted
> on 2026-10-18, so it is the **author's ruling**, put to him in `docs/E9-READ-PACKET.md`. Until he rules, the freeze
> is assembled without the listing and nothing is final before the opening commit. The owner still recommends the
> cut, on the merits in "Why" items 2 and 3; item 1 (schedule) is weaker since the freeze was assembled on
> 2026-10-21, not 2026-10-26. The original text is left below unchanged.

> **AUTHOR RULING, 2026-10-23 (E9 row 2): CUT.** The author's rationale (recorded in full in the rulings file): keep
> V1's complexity manageable, accept the stated dual-authority-capture risk for early receipts given low expected
> initial use, and preserve the option to protect future issuance. It is not the owner's argument adopted
> wholesale; parts of that argument were qualified in review. It is an author scope decision that narrows option (e), not an invocation of the cut order, and it does not retroactively authorize the 2026-10-19 cut
> (`docs/reviews/e9-packet/AUTHOR-RULINGS.md`). A later version may add a listing for future issuance; it cannot
> cover receipts issued before it.

## What is cut

A10.4.1 and the rows that take effect only under option (e) with it: 25–32 and 37–39. These are the `service_keys`
trust-configuration member, its classifier and reason codes, the listing pre-commitment, the C0/C1 bootstrap, and
the listing-evidence package that relying parties would have to keep outside the bundle.

## What applies instead (row 33)

A10.4 option (a): honest signed material stays protected under authority capture (rows 15–16; contract G10). **V1
gives no protection against new receipts under a captor's own keys** when both authority channels are captured, and
the relying-party text and the freeze record say so. Release-key custody (A10.4.2) is unchanged: the cut does not
cure a failure of release-key independence, and the custody gate at the first public verifier release still holds.

## Why

1. **Schedule.** The 30 Oct exit audit (`docs/V1-EXIT-30OCT.md`) puts the listing on the critical path, with about
   one working day of slack. Cutting it saves about 4 days (owner estimate). The first cut item, the PQ hybrid, is
   already registered and would save almost nothing.
2. **What it buys is narrow.** It protects only relying parties whose verifier release is authentic. After review
   r4 its protection against a later release-key theft needs independently authenticated Bitcoin history. It moves
   trust from two credentials (DNS and repository key) to a third (the release key), and all three have the same
   custodian.
3. **What it costs relying parties.** A listing-evidence package outside the receipt bundle that holders must keep
   (contract review VC-02). This is the one mechanism added purely for a decades-later adjudicator
   (`docs/decisions/2026-10-19-horizon-cost.md`), and it is the one the author asked about and got no clear answer to.

## What is lost, honestly

- Production receipts issued before any later listing can never have its protection. A listing added in a later
  version protects only receipts after it.
- The horizon analysis recommended keeping the listing at its signed scope, on that ground. The owner weighs the
  schedule and the relying-party burden above it for V1.

## Registered as a candidate, not an obligation

A key listing with a chain-order pre-commitment, or a witnessed log of key assertions, is a candidate for a later
version. Neither creates an obligation.

## Author ruling, 2026-10-23

The author chose **CUT** for E9 Row 2, accepting the dual-authority-capture
limitation to keep V1's complexity manageable, with low expected initial
use and the option to protect future issuance. This is an author narrowing
of the previously adopted scope, independently of the deadline; it does not
retroactively authorize the owner's original cut. The full ruling and
upgrade boundary are recorded in
[`AUTHOR-RULINGS.md`](../reviews/e9-packet/AUTHOR-RULINGS.md).
