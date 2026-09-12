# Run 1 — preserved (shadowed witnesses)

STATUS: PROPOSED — 2026-09-06 — produced by the AI collaborator; not
adopted; the commit is the author's. PROBE — NON-DISCHARGING.

First TLC pass over the companion and sanity configurations, each cfg
listing several invariants and run with `-continue`. Every companion
`.out` here reports `Purity` violated and is silent on `Agreement`;
every `_Sanity.out` reports at most four of the eight witnesses. The
silence is not unreachability: TLC reports only the FIRST violated
invariant in a violating state, so an invariant listed after another
that the same states violate is never reported. `Agreement` can only
be violated in a state where some verdict differs from the others,
which also violates `Purity` (listed first); `NeverAllRuns` (two runs
completed) is violated only in states that also violate one of the
run-record witnesses listed before it. Recorded as a tool finding in
`../RESULTS-PROBE.md` (F-T1). The run-2 configurations in the parent
directory split the checks so each invariant has a state that violates
it and nothing listed before it. These files are kept as the record of
the diagnosis; nothing in them is cited.
