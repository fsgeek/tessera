# run1/ — development encoding of SS.Q1 (DNS variant), archived

**STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not adopted; the commit is the author's.**

What this directory holds: the encoding of `ss_q1_strict_dns_compromised.pv`
as it stood before the one pre-ladder recut, re-run here for the archive
(S-P3 pattern: run-1 outputs kept when an encoding recut occurs).

- `ss_q1_strict_dns_compromised.pv` — lineage lookup as an inline case
  split over `lineage2(entry(a1, d1), entry(a2, d2))` (`if aid = a1 … else
  if aid = a2 … else MISMATCH`), and the shipped-identity local named
  `sid`.
- `ss_q1_strict_dns_compromised.out` — its output: **every RESULT line
  identical to the ladder run**, plus one warning at line 2,
  `Warning: identifier sid rebound` (`sid` is a ProVerif-reserved
  identifier for session identifiers; the warning is the tool's, not a
  modelling defect).

The recut (development, before the registered ladder was run; recorded in
`../../RESULTS.md` "Recuts"): the case split became a model-local
destructor `lookup2(aid, lin)` (one expansion of `StandingDecide` instead
of two) and the local was renamed `shippedId`. No result changed; the
warning is gone. The registered ladder in `..` was run once, on the recut
encoding; the ladder outputs are the evidence, this directory is the
provenance.
