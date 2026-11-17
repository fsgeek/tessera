# Disposition: Codex review of the A12 draft, sections 1–2 (steward, 2026-11-17)

All eight findings stand; the draft is **not** ready for signing. The steward's context ran short; this records what
the next steward does, and the two choices that belong to the author (they change registered promises).

## Author choices (with the steward's recommendation)
1. **Does the termination bound override latched, timely attempts?** (A12-01, A12-02.) A2.1 promises that latched
   eligibility cannot be expired by later delay and that every timely-eligible attempt ships. A finite bound for all
   requests breaks that promise for an attempt that latched but cannot finish (e.g. storage down for 12 days).
   **Recommendation: yes, override it, as an explicit registered change to A2.1/A2.3,** consistent with the author's
   counsel of 2026-10-30 (bound it, FLP-style; an unbounded open request is a denial-of-service vector). Word it
   honestly: a request still open at L_term is refused `EVIDENCE_UNAVAILABLE` *by the bound*; this does not assert
   its lag exceeded S; its artifacts keep their evidential admissibility and gain no protocol standing as a receipt.
2. **Is a rotation gap acceptable?** (A12-07.) With L1's margins, each window change leaves at least nine days with
   no new acceptances (old acceptance stops 216 h before not-after; the successor cannot open before not-after).
   **Recommendation: accept it for V1 and state it plainly** in the contract and to clients (Yanantin was promised
   word by early December). Shrinking it means changing L1, an operating choice, separately.

## Steward work before re-review
- A12.1: specify the durable, fenced terminal transition at L_term: the single-writer guarded write, the tie rule,
  stale-write and delivery fencing (no receipt delivered after a refusal), and the availability assumptions under
  which termination is then guaranteed; extend the TLA+ lifecycle model to check it (A12-03). Make 14 days an
  author-selected cap and explain its interaction with the signing stop near the window's end (A12-04).
- A12.2: replace the successor DNS record only after the old window's last attempt has ended, not merely after its
  signing stop (A12-05); restate the vectors and model property to what the frozen verifier actually checks (it does
  not compare T with not-before or windows across receipts; A10.2) (A12-06); state the adversary scope: DNS+git
  capture and the issuing-account requester are not addressed by rotation (prechecks 1, 3).
- Inventory every registered sentence changed (A2.1 `:130-160`, A2.3 `:260-289`, A2.4 `:307-315`, A9 `:409-418`,
  A10.2 if its semantics change; reconcile the profile's descriptive "one window") (A12-08).
