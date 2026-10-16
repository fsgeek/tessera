# Codex brief: does Tessera V1's anchor need to cover the signatures?

Repo: /home/tony/projects/tessera. Read formal/p8/ENCODING-V1.md (all, esp. §3 frames and §5 receipt-anchor preimage),
docs/V1-DERIVATION-DRAFT.md §1 (claim C1-C7, especially C3 "Nothing about the key lifecycle after T" and C5),
docs/implementation-spec.md R-3.9 and R-2.40 (adversary), and docs/phase-0-prereg-amendment-3.md §A3.6 (PQ deferral).

Owner's claim (Claude, 2026-10-12): §5's anchor preimage covers the two frames but not the signatures. Attack:
(1) in year T an attacker composes frames with arbitrary content and OTS-stamps a preimage over them (stamping is
public); (2) later the attacker obtains a Tessera signing key (CRQC against ECDSA P-256, or theft of a key on
decommissioned hardware after the service exits); (3) signs the pre-staged frames; the receipt verifies as
"presented to Tessera, no later than T". Fix: include both signatures (length-prefixed) in the anchor preimage, so
only signatures that provably existed by T count. Claimed consequence: classical signatures then survive a later
algorithm break or key compromise for receipts anchored before it (the CAdES-T / RFC 3161 signature-timestamp idea).

Review fully, adversarially:
1. Is the attack real against V1 as specified? Does anything else already block it (DNSSEC snapshot anchoring, the git
   key assertion, frame fields such as issuance time, the verifier's checks, the authority evidence's own anchors)?
2. Does the fix close it? Does it introduce new problems (signature malleability W1 — ECDSA/OpenPGP signatures are
   malleable; injectivity of the new preimage; ordering of issue steps; the R-3.42 single-anchor rule; what P8's proof
   and vectors must change)?
3. Is the claimed consequence (post-break survival) correct, and what does the 2106 verifier then need to know (e.g.
   a break date) for it to be usable? State the honest residual.
4. Anything the owner is missing, including a simpler alternative.

Write findings to docs/reviews/anchor-signatures/CODEX-REVIEW.md: numbered, each with severity, evidence (file:line),
and a recommended disposition (WORDING / MECHANISM / OMIT / REJECT). Do not edit any other file. Do not commit.
