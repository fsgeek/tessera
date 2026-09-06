You are writing the plain-language explanatory section for a ProVerif model, for a reader who is a senior systems engineer and cryptography-literate but has never used ProVerif and does not want to learn it. You have exactly these files and nothing else; do not assume any other context:

- q3_dns_stripped.pv — the model, comments removed. Variant: one authority channel's private key (skD) is leaked.
- q3_repo_stripped.pv — identical except which key is leaked (skR).
- q3_dns_RESULT.txt, q3_repo_RESULT.txt — the tool's verdict lines for each.
- P10-registered.txt — the registered property this model is meant to support.
- A1.3-adversary.txt — the registered adversary model.

Write ONE markdown document, at most 140 lines, in this order and with these headings:

1. "Reading notes" — 5 to 7 bullets on the notation, only what this reader needs: that every value has type bitstring and a tuple's shape lives in construction and pattern matching, not in declarations; what `in`/`out` on channel `c` mean when the adversary owns `c`; what `let (=A, =B) = checksign(s, k) in` does; what `!` means; what `new` and `out(c, skD)` do. Cite line numbers of q3_dns_stripped.pv.
2. "Cast" — a table: every name in the model (keys, tuple, evidence, proofs, tags, events), what it stands for in the design in plain words, where it is built (line), where it is consumed (line). Say explicitly which single value is the thing being attested and which is the key statement.
3. "What the verifier checks" — a table of each check in the Verifier process, one row per line, with a plain-meaning column. Then one sentence: which of these checks is the one the two variants differ on, if any.
4. "The claim" — one sentence a relying party could use, stating what an acceptance implies. Then a short paragraph explaining why the tool's "is true" means that sentence, naming the three things that must have happened earlier and stressing that they must involve the SAME values.
5. "The adversary" — what it can do in this model, what it cannot, and the single line where it gets its strongest capability. State what capability from A1.3 it does NOT have here (compare against A1.3-adversary.txt).
6. "Why the attack fails" — the simplest attack a reader would try (forge authority evidence with the leaked key for a manifest naming the adversary's own key) and the exact check that stops it.
7. "What this result does not show" — bullets. Include: single honest issuer/payload/tuple; hash and fingerprint injective by construction; idealized signatures (no key-substitution capability); n=2 channels; no vacuity/reachability query registered; nothing about meaning of bytes, encodings, rotation, code.
8. "Correspondence to P10" — two or three sentences: which part of P10-registered.txt this model supports and which parts it does not touch (degraded mode, possession semantics).

Rules: cite file:line for every claim about the model. Do not invent fields or behaviors not in the file. Do not use the words "obviously" or "simply". Do not praise the model. If something in the model is unused or suspicious, say so in one line under the relevant section (e.g. an input that is read and never checked). Output only the markdown document.
