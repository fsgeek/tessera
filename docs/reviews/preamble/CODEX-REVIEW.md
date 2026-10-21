The capture warning is substantively correct: **new receipts under attacker-selected keys can pass when both authority channels are captured**. The sentence saying the records “named” the keys preserves that boundary; it must not become “these were Tessera’s keys” or “Tessera issued this receipt.”

The mining wording correctly follows A10.1. Nothing claims signing occurred inside the issuance window, so I found no A10.2 overclaim. No files changed.

**PA-01 — HIGH — Unconditional security claim**

Sentence: “A VALID_STRICT result shows three things.”

Registered text: “Conditional on the registered cryptographic and key-use assumptions” ([A9:128](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:128)). The contract additionally names chain-history and distribution assumptions ([V1-CONTRACT:17–19](/home/tony/projects/tessera/docs/V1-CONTRACT.md:17)).

“Shows” omits those conditions. In particular, passing the checks does not independently establish historical key safety or actual service provenance under substituted authority records.

Replacement: “VALID means all required checks passed. Claims depend on registered assumptions about cryptography, key use and Bitcoin history.”

**PA-02 — HIGH — Missing verifier-authentication prerequisite**

Sentence: “With the verifier, anyone can check it without Tessera.”

Registered text: the trust configuration is “authenticated independently of the bundle and of both authority-channel credentials” ([A9:326–332](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:326)). V1 offers no protection to someone who skips release authentication ([V1-CONTRACT:63](/home/tony/projects/tessera/docs/V1-CONTRACT.md:63)).

Replacement: “Check without Tessera using an authenticated verifier release and its trust file.”

**PA-03 — HIGH — Two signatures can suggest independent approval**

Sentence: “The content bytes in this bundle were signed by two keys.”

Registered text: each key signs its designated frame, binding the content ([A9:130](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:130)). C3 explicitly claims “no separation of control and no independent fates”; capture of the issuing AWS account supplies signing capability for both slots ([A9:142](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:142)).

The sentence needs that nearby limit. It should also describe signatures over frames rather than imply direct signatures over bare content.

Replacement: “Two keys signed bytes that bind the content. One controller holds both keys. Control of the issuing AWS account lets an attacker use both.”

**PA-04 — HIGH — Historical security omitted**

Sentence: “It does not check revocation or standing.”

Registered text: V1 does not evaluate “whether a signing algorithm or key was safe when it signed” ([A9:259–260](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:259)); C7 expressly retains this non-claim ([A9:146](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:146)).

A reader needs this beside the signature claim: passing verification does not establish that the keys or algorithms were safe.

Replacement: “It does not check revocation or past key or algorithm safety. It does not check which attempts the service shipped.”

**PA-05 — MEDIUM — Capture wording obscures the precise limitation**

Sentence: “If one party took control of both the DNS record and the git signing key, receipts under that party’s keys also give VALID_STRICT; this receipt cannot tell them apart.”

Registered text: a captor can issue new receipts naming its own keys; V1 guarantees neither detection nor public visibility ([A10:425–430](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-10.md:425)). The listing cut expressly restores this boundary ([listing-cut:16–19](/home/tony/projects/tessera/docs/decisions/2026-10-19-listing-cut.md:16)).

“Cannot tell them apart” is unclear. Different fingerprints can be inspected; the receipt does not establish whether their controller is legitimate. The missing visibility limit also matters.

Replacement: “An attacker controlling both authority records can issue passing receipts without the original service. V1 guarantees no detection or public exposure of capture.”

**PA-06 — MEDIUM — A-UTC needs its unchecked status**

Sentence: “A UTC bound is reported only under the stated assumption A-UTC.”

Registered text: A-UTC “is not a Bitcoin consensus rule” and “the verifier does not check it” ([A10:280–283](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-10.md:280)). Its assessment does not change the stable result ([A10:300–305](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-10.md:300)).

The sentence is conditional, but does not explain that reporting the bound supplies no evidence that the assumption holds.

Replacement: “The separate UTC bound assumes unchecked A-UTC and never changes the verdict.”

**PA-07 — MEDIUM — Two short, useful non-claims are missing**

Relevant sentences: “The receipt does not identify who submitted the content.” / “The content and both signatures existed before a named Bitcoin block was mined.”

Registered text: C2 does not establish “whether a replay suits the transaction” ([A9:141](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:141)); C5 promises “No lower bound, no priority” ([A9:144](/home/tony/projects/tessera/docs/phase-0-prereg-amendment-9.md:144)).

These address ordinary reliance errors without explaining additional mechanisms.

Add: “It gives no lower time bound or priority. It does not show that a replay suits your transaction.”

**PA-08 — LOW — Paragraph length and project vocabulary**

Sentence: “This bundle is a Tessera V1 receipt.” Also, the capture sentence contains 29 words, and the entire text forms one 14-sentence paragraph.

The style requires at most six sentences per paragraph and 25 words per descriptive sentence ([STE-STYLE:16–21](/home/tony/projects/tessera/docs/plain/STE-STYLE.md:16)). Its dictionary uses “receipt” instead of “bundle” and plain “VALID” instead of `VALID_STRICT` ([STE-STYLE:47](/home/tony/projects/tessera/docs/plain/STE-STYLE.md:47), [STE-STYLE:123](/home/tony/projects/tessera/docs/plain/STE-STYLE.md:123)).

Replacement opening: “Tessera V1 receipt (tessera-v1-strict).” Divide the remaining text by topic, as below.

Complete revised preamble: **1,197 UTF-8 bytes, including the final newline**.

```text
Tessera V1 receipt (tessera-v1-strict).

Check without Tessera using an authenticated verifier release and its trust file.
VALID means all required checks passed.
Claims depend on registered assumptions about cryptography, key use and Bitcoin history.
Two keys signed bytes that bind the content.
A DNS record, authenticated by DNSSEC signatures, and a signed git commit named these keys for wamason.com.

One controller holds both keys.
Control of the issuing AWS account lets an attacker use both.
An attacker controlling both authority records can issue passing receipts without the original service.
V1 guarantees no detection or public exposure of capture.

The content and signatures existed before the selected Bitcoin block was mined.
Its header time T is not a UTC upper bound.
The separate UTC bound assumes unchecked A-UTC and never changes the verdict.

V1 checks no sender identity, content meaning or truth, signatures inside content, revocation, or past key or algorithm safety.
It does not check which attempts the service shipped.
It gives no lower time bound or priority.
It does not show that a replay suits your transaction.

See the specification, vectors and standards list.
```


