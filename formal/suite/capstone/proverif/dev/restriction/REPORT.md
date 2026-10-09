EXPLORATORY ANALYSIS 2026-10-08 — read-only, non-discharging, not part of any registration; no ProVerif run

# Restricting degraded verification to the outermost layer (L0): effect on the eleven degraded failures

*Analysis by an Opus agent. Saved and condensed by the owner instance, because the harness refused the
agent's own write; the agent's full text is in the session record. Sources: PREDICTIONS.md §4 rows 1771–1777,
§9(1) 2503, §9(2) 2525–2592; RESULTS.md §3; `proverif/*.out`; `dev/slice_probe/`.*

**Proposal tested.** In case (d), a wrapped layer whose evidence supports only `VALID_DEGRADED` gets
`UNVERIFIABLE` instead, with its observations recorded. Strict verification is unchanged. In the model that
means no `LayerAccepted` at L1 or L2 in the (d) files.

## Per companion

| Companion | (d) reds and their layer | After the restriction | Seam | Still severable? |
|---|---|---|---|---|
| C-C2 | C-Q3 A/B, link 5: **L0** | unchanged | D1 | yes, in (d) |
| C-C3 | C-Q5, C-Q9, link 3: **L0** | unchanged | D10 | yes, in (d) |
| C-C4 | Rescoped, InnerSigTransplanted, link 6b: **L1**. C-Q3 A, link 5: L0 | the wrapped reds are gone | **D2** | **no, in any registered case** |
| C-C5 | InnerSigTransplanted: **L1**. C-Q8, link 4: L0 | the wrapped red is gone | **D5** | **no, in any registered case** |
| C-C6 | C-Q7, C-Q8, link 4: L0. InnerSigTransplanted: **L1** | the wrapped red is gone | D5 producer; D6 | D5 producer only, in (d) |
| C-C7(i), C-C7(ii) | C-Q8, link 4, authorship: L0 | unchanged | D6 | yes, already in strict |
| C-C8 | C-Q5, C-Q9, links 3 and 5: L0 | unchanged | D10 | yes, in (d) |
| C-C8-i | registered greens only | unchanged | D10 isolation | needs a full (d) run |
| C-C8-ii | C-Q9: L0; a required C-Q5 green | unchanged | D10 isolation | the green needs a full (d) run |
| C-C17 | link 2a, `SignerForged`: L0 | unchanged | D7 membership | yes, already in strict |

Eight of the eleven are untouched. Only C-C4, C-C5 and C-C6 have wrapped reds, and those were the only (d)
evidence for D2's and D5's consumers. `ScopeJudge` and `SigJudge` need `wctx`, so they can fire only on a
forwarded, wrapped layer (`capstone_d.pv:1025-1038`).

## D2 and D5 become unseverable in every registered case

- In (a) and (b), the removed checks are **redundant for these consumers**: check 1, plus enrolment with
  one channel uncompromised, denies the attacker the key the attack needs. They are **still load-bearing for
  D1 and D6** at L0.
- They become severable again only in **case (c)** (both channel keys leaked, strict): C-C4 and C-C5 (or
  C-C6) on the (c) fixture, against `cap_cc01_c`'s green baseline (`:10181`, `:9293`, `:10403`, `:7739`). That
  is a new registration, with unknown cost.

## Witnesses and side effects in (d)

- No correct-form verdict changes colour. A4.6's registered red has an L0 trace.
- **Four (d) witnesses die:** `HonestChain(L1)`, `HonestChain(L2)`, `HonestWrappedAccepted` and
  `HonestWrappedStandingAgreed`. Under C-N1 as frozen, every (d) file becomes a broken fixture until set (3)
  is re-registered. C-Q6 conjunct 3 becomes vacuous in (d).
- **A design fork.** If standing still establishes at wrapped (d) layers, a relying party sees `ESTABLISHED`
  beside an envelope `UNVERIFIABLE`. If standing is restricted too, D12's and D13's (d) severings vanish
  (strict severings remain).

## C-C15 and D11

- No (d) red of configuration (i) survives, including conjunct 3, which removes the object of Decision 3.
- D11 keeps its severings in (a) and (b) through (ii) and (iii).

## Verdict

**As a disposal of the eleven, the restriction costs more than it solves.** It also does not remove the
attack shapes: case (c) gives the adversary the same authority power under strict verification, so every
wrapped (d) attack shape remains reachable as `VALID_STRICT` under the mutations. This is predicted by
construction and supported by `cap19b…:843,:1151,:1450`. The RFC 4998 rationale is a design reason, not a
disposal. One possible upside, untested: a restricted (d) model resembles the slices that landed in about
100 s, so full (d) runs might become landable.
