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

## Resolution of the two choices (steward, 2026-11-19)
The author, 2026-11-19, on being asked: "As steward, I will abide by your recommendation here." Both are adopted as
recommended above, as OWNER DECISIONS, and take registered effect when the author signs A12:
1. The termination bound overrides latched, timely attempts: an explicit registered change to A2.1/A2.3, worded as
   in choice 1 (refused `EVIDENCE_UNAVAILABLE` by the bound; no claim the lag exceeded S).
2. The rotation gap (at least nine days without new acceptances at each window change) is accepted for V1 and
   stated plainly in the contract and to clients. Shrinking it is a separate L1 operating choice, not part of A12.

## Rounds 2-4 and the exit (steward, 2026-11-20)
- **r2** (four HIGH): r2 described present code as providing guarantees it only partly provides (a clock read
  before a remote write as a commit-time tie; eventual availability as a 10-minute bound; COMPLETE-only URLs as an
  object fence; DNS cutover ignoring caches). r3 narrowed each and moved the rest into implementation duties.
- **r3** (three HIGH against promises): still promising real-time outcomes from an asynchronous system. r4 restated
  the bound as a rule of each invocation's behaviour and the gap from dates.
- **r4** (final scoped round; two HIGH against promises, one duty): the r4 text kept an absolute "only refuses from
  L_term" statement that contradicted its own per-invocation rule, and treated issuer clock readings as real time.
  By the pre-registered exit (no fifth round), r5 deletes both promises: L_term governs what each invocation attempts
  by its own reading and is disclaimed as a real-time cutoff; the gap's nine-day minimum is stated by the issuer's
  clock readings, with no real-time minimum. R4-03's conditions (reread on a lost fence; hash-named objects with the
  hash checked before a URL is minted) are added to the duties.
- **What A12 now promises:** never both COMPLETE and REFUSED; no client receipt for a request not durably COMPLETE;
  each invocation reading at or after L_term attempts only refusal; successor acceptance only after its fence. It
  promises no termination time and no real-time gap. Everything else is a gate before the bound is enabled.
- **Found along the way, independent of A12:** the deployed issuer stores each receipt at a fixed, overwritable key
  in an unversioned bucket (`result/<rid>/receipt.json`), so a stale delayed put could in principle replace a
  delivered receipt. Unlikely (it needs a put delayed across poller runs) and detectable (the API returns the
  receipt's hash; Yanantin checks it). Corrected by the content-addressing duty, deployed with Codex review whether
  or not A12 is signed.
- **Status:** r5 goes to the author for signing, with all four reviews. The author's first commit containing the final
  text is the signing act.
