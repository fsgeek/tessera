# Review: S-P3.Q2 cold-read assistance, Codex

Author-dispatched review under the A1.7 discipline, on the S-P3 ladder
results of 2026-09-04 before the author's cold read. The reviewer read
the Q2 model, the judge, and the shared signature rules, re-ran Q2
independently, and reported that its three results match the recorded
`.out`. Nothing was changed by the reviewer.

## Reproducibility record

- **Reviewer:** Codex (OpenAI), dispatched directly by the author. Model
  per the session log of the dispatch (`~/.codex/sessions/2026/09/04/`,
  rollout 22:10:39 UTC): `gpt-6-astra`. (Earlier review records cite
  `gpt-5.6-sol`; the configured model has changed. Verified from the
  session file, not from a label.)
- **Inputs:** `formal/suite/s-p3/proverif/sp3_q2_degraded_compromised.pv`,
  `formal/suite/lib/tessera_theory.pvl`, the recorded `.out`; the
  reviewer's own re-run of Q2.
- **Repository state:** predictions frozen at `fe1517c`; the S-P3 models
  and `RESULTS.md` were untracked in the author's worktree at review time.
- **Text below:** verbatim as the author relayed it to the AI
  collaborator in session, 2026-09-04. Provenance header and this
  section are the collaborator's; the collaborator's disposition follows
  the text.

## Reviewer text (verbatim)

> Claude has identified a useful, bounded reading exercise. My reading is that Q2 supports its narrow key-binding claim under the declared assumptions. But the header and verifier alone are insufficient to assess that: the attack definition and shared signature rules matter too. I checked those and reran Q2; its three results match the recorded output.
> Nothing was changed.
>
> The distinction from your earlier concern is important. This model addresses substitution of a different key, not theft of the legitimate signing key. Your forward identifier addresses observable divergence between successors. Q2 contains neither succession nor disclosure of the honest issuer's private key.
>
> Here is the argument in terms you can inspect without becoming a ProVerif specialist.
>
> **The attempted deception**
>
> Alice signs an attestation. The attacker obtains those signed bytes and constructs a different key under which her existing signature also verifies. The attacker then supplies a replacement manifest naming that different key.
>
> Ordinary signature verification is deliberately insufficient in this model. The shared signature rules (formal/suite/lib/tessera_theory.pvl:75) explicitly grant that substitution capability. They also let the attacker sign new material with the derived private key.
>
> Furthermore, the attacker controls the sole authority channel accepted in this degraded case. Its endorsements therefore cannot rescue the verifier from the deception.
>
> **What the verifier demands**
>
> In the verifier process (formal/suite/s-p3/proverif/sp3_q2_degraded_compromised.pv:77), acceptance requires:
>
> | Check | Plain meaning |
> |---|---|
> | Authority signature covers STMT_DIGEST, h(t) | The authority evidence endorses this particular manifest tuple. |
> | fp(kX) = kfpr | The presented verification key matches the fingerprint named in that manifest. |
> | Possession signature covers POSS, t | That key verifies a self-signature over this same manifest. |
> | Attestation signature covers BYTES, fb | That key verifies the presented framed content, with the attestation tag. |
> | Frame matches alg, id, and fp(kX) | The signed content names the same algorithm, identity, and key fingerprint. |
> | mh = h(t) | The signed content commits to this same manifest. |
>
> One small syntax distinction helps: in the frame pattern, =id means require equality with the previously obtained identity. A bare name such as ot means read that field, without imposing an additional equality check.
>
> **Why the attack fails**
>
> The central argument is short:
>
> 1. Alice's honest framed content contains fp(AliceKey).
> 3. In this symbolic model, different keys cannot have equal fingerprints.
> 4. Therefore the same honest content cannot be accepted under another key—even when its signature verifies under that key.
>
> Changing the embedded fingerprint would produce different content. It would no longer be the existing message–signature pair the substitution attack was trying to reuse.
>
> The judge (formal/suite/s-p3/proverif/sp3_q2_degraded_compromised.pv:110) checks precisely this failure condition: an honest issuer reports content and its signing key; the verifier reports acceptance of the same content; the judge raises an alarm if the keys differ. Although that alarm compares keys rather than identities, the verifier separately requires the accepted identity to match the identity inside the content.
>
> That is the reasoning to understand and challenge. You do not need to memorize the process syntax.
>
> **Where your judgment is needed**
>
> Claude's two suggested abstraction boundaries are real:
>
> - The frame is already perfectly structured. Its fields cannot overlap, parse ambiguously, or acquire different meanings through competing byte decoders. That makes it suitable for examining the binding relationships, but actual encoding and parsing remain P8 obligations.
> - The manifest is reduced to the authority tuple. Here, signing the manifest, hashing the manifest, and binding the authority tuple all concern the same object. A richer implementation must explain how those operations relate when additional fields exist. This model does not establish that correspondence automatically.
>
> There are two further boundaries worth keeping visible:
>
> - Included does not mean semantically validated. Object type and canonicalization version are inside the signed structure, but this verifier does not check that they are supported or permitted. The algorithm identifier is compared between fields; it does not select between modeled cryptographic algorithms. Those are scope limits, not automatically defects in this key-binding argument.
> - Fingerprints and hashes are collision-free by construction here. The model checks the composition under that assumption; it does not establish the strength of concrete fingerprint or hash algorithms.
>
> I would therefore phrase your review question more concretely than "does the abstraction lie?":
>
> > Does this model preserve the attack and the defense we intend to study, and have we assigned every omitted detail to an explicit remaining obligation?
>
> Finally, I would qualify Claude's "companions discharge nothing." They do not prove the correct construction secure, but they supply essential evidence that the checking arrangement can detect the intended failures. You need not personally read every trace to understand that evidential role.
>
> My rerun found both attack events unreachable and acceptance reachable—the verifier is not succeeding merely by rejecting everything. That supports this bounded exercise. It does not by itself establish all of P3, the multi-signer case, implementation conformance, or resistance to actual signing-key compromise.

## Collaborator disposition (2026-09-04, for the author's read)

Each reviewer claim checked against the model and the record:

1. **Independent replication** of Q2's three results: accepted as the
   first non-author confirmation; recorded in `RESULTS.md` review log.
2. **The check table and the "why the attack fails" argument** are
   faithful to the verifier at the cited lines, including the note that
   the judge compares keys while the verifier separately pins identity.
   (The argument's numbering skips 2; content unaffected.)
3. **Scope distinction** — substitution of a different key, not theft of
   the honest key; no succession; no private-key disclosure — matches
   A1.3 as registered and the D1/docket-25 boundary. Accepted.
4. **Two further boundaries** — (a) inclusion is not semantic validation
   (object type, canonicalization version unchecked for support; the
   algorithm identifier is compared, not used to select an algorithm);
   (b) collision-free `h`/`fp` — (b) was already in `RESULTS.md` and the
   library header; (a) was **not** and is added to `RESULTS.md` §"What
   S-P3 does not discharge". Accepted as an omission.
5. **Reframed review question** — adopted verbatim into `RESULTS.md`
   as the question the cold read answers.
6. **"Companions discharge nothing" qualification** — accepted as
   phrasing. The registered sense (spike ledger entry 2: "exists to
   prove the queries can go red") is the reviewer's "evidence that the
   checking arrangement can detect the intended failures"; the two
   agree. `RESULTS.md` now says both halves.
7. **Closing limits** — not all of P3 (the [assumption] half), the
   multi-signer case (the reviewer read Q2 only; Q5 is in
   `RESULTS.md`), implementation conformance, real key compromise —
   all consistent with `RESULTS.md` as written.

No change to any model, query, prediction, or result followed from
this review. Two sentences were added to `RESULTS.md`; nothing was
removed.

## Addendum — reviewer conclusion after discussion with the author (verbatim, relayed 2026-09-04)

> For this substitution attack, the fingerprint check adds a constraint: a substitute key must both verify the existing signature and match the fingerprint already committed in the signed content. Adding that check cannot enlarge the set of acceptable substitute keys.
>
> Your distinction about Tessera's responsibility is the right one. It should state:
>
> - Exactly what key representation is fingerprinted, with which algorithm and parameters.
> - That acceptance requires the presented key to match the signed fingerprint.
> - That the symbolic model assumes different keys have different fingerprints.
> - That the implementation instead depends on the difficulty of finding a different key with the target fingerprint, alongside its signature and encoding assumptions.
>
> Tessera can explain the additional defense without claiming a quantified increase in cryptographic strength. The binding mechanism and its dependencies need to be defensible; an invented combined security level does not.

**Collaborator disposition.** Accepted in full. The monotonicity point
is exact: acceptance is a conjunction, and adding a conjunct cannot
enlarge the accepted set. The four statements are now carried as one
obligation block in `RESULTS.md` ("Fingerprint binding — what the
record must state"), each assigned to the document that owns it. The
caution against a quantified combined strength is adopted as a
constraint on how `RESULTS.md` F3 ("defense in depth across two
independent hardness assumptions") may be read: qualitative, never a
summed or multiplied security level. Provenance: reviewer conclusion
reached with the author in discussion; not an author ruling.
