# Lower-ceiling reader probe — Q3 reading aid (2026-09-06)

Per `formal/suite/ENUMERATION.md` amendment note 5 item 2. Reader:
Claude Haiku 4.5, two fresh contexts, no tools in condition 1, Read of
exactly two files in condition 2. Same three questions both times:
the claim (naming the attested value and the key statement), the
adversary (and the line that empowers it), three boundaries.

## Condition 1 — comment-stripped model + RESULT line only

- Claim: got possession and signing; **missed the authority-publication
  conjunct entirely**; named `fb` as attested (right) and **`kX` as the
  key statement (wrong — it is `t`)**.
- Adversary: right (`out(c, skD)`; cannot forge the issuer's signature).
- Boundary: **inverted** — listed "protects against a compromised DNS
  authority" as something the result does *not* show, which is exactly
  what it does show. Asked: "is this testing that repository-only
  verification suffices, or showing a problem with the design?"
- Confidence: medium.

## Condition 2 — reading aid (`READING-AID-Q3.md`) + stripped model

- Claim: `fb` attested (right), `t` the key statement with the
  fingerprint in field 2 (right), the three conjuncts with the same
  values (right). One slip: said **both** authorities published the
  statement; the query and the aid both say **at least one**, and in
  this variant only the repository publication is guaranteed honest.
- Adversary: right, including what it cannot do and the absence of
  the DSKS capability.
- Boundary: three correct (hash/fingerprint idealised; non-injective
  correspondence; no archive or anchor).
- Confidence: medium. Relied most on Part B (the blind explanation);
  Part A's cast confirmed `fb`/`t`. No contradiction found between
  parts. Noted Part B's boundary list is "exhaustive and somewhat
  abstract".

## Reading

The aid is doing work: the stripped reader got the key statement
wrong and the central boundary backwards; the aided reader got both
right. The one aided error (both vs. at least one) is a defect to fix
in the aid's claim sentence — state the "or" in bold and say which
channel is honest in each variant. The probe does not say the aid is
sufficient for the author; that is the author's read.
