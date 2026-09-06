# Reading aid — first-link Q3 (transcription binding, both channel variants)

**Status: PROPOSED testimony, 2026-09-06 — a reading aid under
`formal/suite/ENUMERATION.md` amendment note 5 item 2. Not a gate; not
a proof; subject to review. Assembled by the AI collaborator; the
commit is the author's.** Models:
`formal/spike/first-link/proverif/q3_mechanism_dns_compromised.pv` and
`q3_mechanism_repo_compromised.pv` (they differ in one line: which
authority key is leaked). The trial artifact for the author's
twenty-minute read: the question that read answers is *"from this
document alone, can you state what the model claims, against whom,
and what it does not show?"*

**Provenance of the parts.** Part A (typing note, cast list) was
written by the AI collaborator (Claude, Fable 5.1), who knows what the
names were meant to stand for. Part B was written blind by a
non-author model of a different family (Codex CLI 0.153.3, model
`gpt-6-astra`, read-only sandbox, 2026-09-06), given only the two
comment-stripped models, their RESULT lines, P10's registered text,
and A1.3 — so its English is evidence of what the model *says*, not
what its author meant. The dispatch prompt and inputs are archived
under `formal/spike/first-link/proverif/reading-aid-q3/`.

**Where the two parts disagree (the cross-check working).** Part A's
first draft said ProVerif has one type for every value. Part B is
more precise and is right: secret keys are `skey`, public keys `pkey`,
the channel is `channel`; *messages* are `bitstring`, and it is the
messages — tuples, hashes, signatures, fingerprints — whose shape is
invisible in the declarations. Part A below is corrected. Part B also
names two boundaries Part A did not: the correspondence is
non-injective (nothing forces one publication per acceptance), and no
archive or time-anchor check is modeled. Both are true and stand.

**Probe result (2026-09-06, `proverif/reading-aid-q3/PROBE-haiku-2026-09-06.md`).**
A Haiku reader given only the stripped model named the wrong value as
the key statement and inverted the central boundary; given this aid it
got both right. Its one aided error: it read "at least one authority
published `t`" as "both". So, for the reader in a hurry: **the query
guarantees that AT LEAST ONE honest authority published exactly `t`.**
In the DNS-leaked variant that is the repository; in the
repository-leaked variant it is DNS. The leaked channel's evidence
proves nothing.

Line numbers in Part A refer to the committed `.pv` file (header
included); line numbers in Part B refer to the comment-stripped copy
archived beside it (`q3_dns_stripped.pv`), which is what the blind
reader saw.

---

# Part A — typing note and cast (collaborator)

## Typing note

Every *message* in ProVerif has type `bitstring` (keys are typed `skey`/`pkey` and the channel `channel`, per Part B). A tuple is a
bitstring. A hash is a bitstring. A free name is a bitstring. The
declarations therefore never tell you the *shape* of a value. Shape
lives in two places only: where the honest side **constructs** a value
(`let tH = (issuerId, fp(pk(skI)), ssetH, algH, verH)`), and where a
process **pattern-matches** it (`let (id, kfpr, ss, alg, ver) = t in`,
which succeeds only if `t` was built as a five-tuple and otherwise
stops the process, which in this idiom means "reject"). The `: bitstring`
annotations on pattern variables carry no information. The `pkey` /
`skey` types on keys are checked when the file is parsed; by ProVerif's
default they are not enforced against the adversary during analysis.

## Cast

| Name | What it is in the design | Built | Consumed |
|---|---|---|---|
| `c` | the public network; the adversary owns it entirely | declared | every `in`/`out` |
| `skD`, `pk(skD)` | the DNS authority channel's signing key and its public key | main process, `new`; `pk(skD)` published | `AuthorityDNS` signs; `Verifier` checks `evD` |
| `skR`, `pk(skR)` | the repository authority channel's signing key and public key | same | `AuthorityRepo` signs; `Verifier` checks `evR` |
| `skI`, `pk(skI)` | the issuer's (Tessera's) attestation signing key and public key | main process, `new`; `pk(skI)` published | `Issuer` signs possession and bytes |
| `tH` | **the key statement**: (issuer identity, fingerprint of issuer key, signer set, algorithm, version) — the authority-relevant tuple of the issuer-key manifest, map v1 | main process | handed to both authorities as `t` |
| `t` | whatever tuple the presenter hands the verifier, claiming it is the key statement | adversary's choice at `in` | `Verifier`: digest recomputed, then unpacked |
| `evD`, `evR` | authority evidence: a channel key's signature over `(STMT, h(t))` | `AuthorityDNS`, `AuthorityRepo` | `Verifier` first two checks |
| `fbH` / `fb` | **the attested thing**: the framed bytes; `fbH` is the one fixed honest value, `fb` is what the presenter hands over | free name / adversary's choice | `Issuer` signs `fbH`; `Verifier` checks `sg` over `fb` |
| `ppf` | possession proof: issuer's signature over `(POSS, fp(pk(skI)))` — spike encoding, fingerprint only; the suite's library later binds possession to the manifest (D-3) | `Issuer` | `Verifier` |
| `sg` | the attestation signature: `sign((BYTES, fb), skI)` | `Issuer` | `Verifier` |
| `kX` | the public key the presenter claims is the issuer's | adversary's choice | `Verifier`: fingerprint compared to `kfpr`, then used to verify `ppf` and `sg` |
| `label` | read from the network and never used; a leftover | `in` | nothing |
| `STMT`, `POSS`, `BYTES` | domain-separation tags: authority statement, possession, attestation bytes | constants | inside every signature |
| `h` | the digest; injective by construction here | — | `AuthorityDNS/Repo` sign `h(t)`; `Verifier` recomputes `h(t)` |
| `fp` | key fingerprint; injective by construction here | — | `tH`, `Verifier`, `ppf` |
| `AuthorityPublishedDNS(t)`, `AuthorityPublishedRepo(t)` | events: an honest authority published statement `t` | authority processes | query, right-hand side |
| `IssuerPossession(k)`, `IssuerSigned(k, fb)` | events: the issuer holding key `k` proved possession; signed bytes `fb` | `Issuer` | query, right-hand side |
| `Accept(evD, evR, t, kX, fb)` | event: the verifier accepted, with exactly these values | `Verifier`, last line | query, left-hand side |

## The two variants

`out(c, skD)` (DNS key leaked) versus `out(c, skR)` (repository key
leaked). Both runs report the correspondence true. Together they are
the registered "both channel variants".

---

# Part B — blind explanation (Codex, gpt-6-astra, verbatim)

## Reading notes

- Values are **not all `bitstring`**: secret keys have type `skey`, public keys have type `pkey`, and `c` has type `channel`. Statements, payloads, signatures, hashes, and fingerprints use `bitstring`; a statement tuple’s field structure comes from construction and pattern matching, not a record declaration. (`q3_dns_stripped.pv:2-17`, `q3_dns_stripped.pv:40-45`, `q3_dns_stripped.pv:53`)
- The adversary owns public channel `c`: `out(c, x)` makes `x` available to it; `in(c, pattern)` accepts an adversary-supplied message matching that pattern. Delivery is not authenticated by the channel. (`q3_dns_stripped.pv:2`, `q3_dns_stripped.pv:30`, `q3_dns_stripped.pv:40-41`)
- `let (=A, =B) = checksign(s, k) in` verifies `s` under public key `k`, then requires the recovered message to be exactly the pair `(A, B)`. The equals signs require existing values to match; failure prevents that process instance from continuing to acceptance. (`q3_dns_stripped.pv:7`, `q3_dns_stripped.pv:42-49`)
- `!` permits arbitrarily many instances of a process. Here those instances reuse the same keys, honest statement, and honest payload; they do not create additional issuers. (`q3_dns_stripped.pv:52-59`)
- `new` creates a fresh secret value. `out(c, skD)` then deliberately discloses the DNS authority’s secret key, allowing the adversary to sign arbitrary messages with it. (`q3_dns_stripped.pv:6`, `q3_dns_stripped.pv:52-55`)
- Events record milestones for the query; they are not network messages. The `==>` query asks whether each acceptance has the specified earlier events, with matching arguments. (`q3_dns_stripped.pv:18-27`, `q3_dns_stripped.pv:29-38`, `q3_dns_stripped.pv:49`)

## Cast

The single payload value being attested by the issuer is `fb`—`fbH` in the honest issuer. The key statement is `t`—honestly constructed as `tH`—whose hash the authorities sign; the model keeps these two signed objects distinct. (`q3_dns_stripped.pv:30-38`, `q3_dns_stripped.pv:42-48`, `q3_dns_stripped.pv:53-58`)

| Name | Plain meaning | Built or introduced | Consumed |
|---|---|---|---|
| `c` | Public, adversary-controlled transport | `q3_dns_stripped.pv:2` | `q3_dns_stripped.pv:30-41`, `q3_dns_stripped.pv:54-55` |
| `skey`, `pkey`, `bitstring` | Secret-key type, public-key type, and general message type | `q3_dns_stripped.pv:3-6` | `q3_dns_stripped.pv:23`, `q3_dns_stripped.pv:28-41` |
| `skD`, `skR`, `skI` | DNS authority, repository authority, and issuer secret keys | `q3_dns_stripped.pv:52` | `q3_dns_stripped.pv:53-59`; signing at `q3_dns_stripped.pv:30-38` |
| `pk`, `pkD`, `pkR` | Public-key constructor and the verifier’s fixed authority public keys | `q3_dns_stripped.pv:5`, `q3_dns_stripped.pv:39`, `q3_dns_stripped.pv:59` | `q3_dns_stripped.pv:42-43` |
| `sign`, `checksign`, `m`, `k` in the reduction | Signature construction and verification; `m` and `k` are generic message and secret-key placeholders | `q3_dns_stripped.pv:6-7` | `q3_dns_stripped.pv:30-38`, `q3_dns_stripped.pv:42-48` |
| `fp`, `h` | Public-key fingerprint and statement hash constructors | `q3_dns_stripped.pv:8-9` | `q3_dns_stripped.pv:30-48`, `q3_dns_stripped.pv:53` |
| `STMT`, `POSS`, `BYTES` | Tags separating authority statements, possession proofs, and payload signatures | `q3_dns_stripped.pv:10-12` | Built into signatures at `q3_dns_stripped.pv:30-38`; checked at `q3_dns_stripped.pv:42-48` |
| `issuerId`, `ssetH`, `algH`, `verH` | Public honest-statement fields: issuer identifier and opaque signature-set, algorithm, and version values; their contents are unspecified | `q3_dns_stripped.pv:13-16` | `q3_dns_stripped.pv:53` |
| `tH`, `t` | Honest five-field key statement and the statement parameter/input | `q3_dns_stripped.pv:53`, `q3_dns_stripped.pv:28-31`, `q3_dns_stripped.pv:40` | `q3_dns_stripped.pv:30-33`, `q3_dns_stripped.pv:42-49`, `q3_dns_stripped.pv:56-57` |
| `id`, `kfpr`, `ss`, `alg`, `ver` | Extracted statement fields; `kfpr` is the asserted key fingerprint | `q3_dns_stripped.pv:44-45` | Only `kfpr` is subsequently checked: `q3_dns_stripped.pv:46-50` |
| `fbH`, `fb` | Public honest payload and payload parameter/input | `q3_dns_stripped.pv:17`, `q3_dns_stripped.pv:34`, `q3_dns_stripped.pv:41` | `q3_dns_stripped.pv:37-38`, `q3_dns_stripped.pv:48-49`, `q3_dns_stripped.pv:58` |
| `evD`, `evR` | Submitted DNS and repository authority signatures | Honest signatures: `q3_dns_stripped.pv:30`, `q3_dns_stripped.pv:33`; inputs: `q3_dns_stripped.pv:40` | `q3_dns_stripped.pv:42-43`, `q3_dns_stripped.pv:49` |
| `kX` | Submitted issuer public key | `q3_dns_stripped.pv:41` | `q3_dns_stripped.pv:46-49` |
| `ppf`, `sg` | Submitted possession proof and payload signature | Honest signatures: `q3_dns_stripped.pv:36`, `q3_dns_stripped.pv:38`; inputs: `q3_dns_stripped.pv:41` | `q3_dns_stripped.pv:47-48` |
| `label` | Extra submitted value with no enforced meaning | `q3_dns_stripped.pv:40` | Never used: `q3_dns_stripped.pv:42-50` |
| `AuthorityDNS`, `AuthorityRepo` | Processes recording publication and releasing an authority signature | `q3_dns_stripped.pv:28-33` | `q3_dns_stripped.pv:56-57` |
| `Issuer`, `Verifier` | Issuer proof/signature producer and acceptance checker | `q3_dns_stripped.pv:34-50` | `q3_dns_stripped.pv:58-59` |
| `AuthorityPublishedDNS`, `AuthorityPublishedRepo` | Publication milestones for a statement | Declared at `q3_dns_stripped.pv:18-19`; emitted at `q3_dns_stripped.pv:29`, `q3_dns_stripped.pv:32` | `q3_dns_stripped.pv:25` |
| `IssuerPossession`, `IssuerSigned` | Honest issuer’s possession and payload-signing milestones | Declared at `q3_dns_stripped.pv:20-21`; emitted at `q3_dns_stripped.pv:35`, `q3_dns_stripped.pv:37` | `q3_dns_stripped.pv:26-27` |
| `Accept` | Successful verification, recording both evidences, statement, key, and payload | Declared at `q3_dns_stripped.pv:22`; emitted at `q3_dns_stripped.pv:49` | `q3_dns_stripped.pv:24` |
| Query `t`, `k`, `fb`, `evD`, `evR` | Variables connecting an acceptance to earlier milestones; this `k` is a public key | `q3_dns_stripped.pv:23` | `q3_dns_stripped.pv:24-27` |

Unused inputs/fields: `label` is ignored, and `id`, `ss`, `alg`, and `ver` are extracted without further checks. (`q3_dns_stripped.pv:40-50`)

## What the verifier checks

| Check line | Plain meaning |
|---|---|
| `q3_dns_stripped.pv:40-41` | Receive an eight-component submission with the indicated component types. |
| `q3_dns_stripped.pv:42` | DNS evidence must verify under the fixed DNS key and contain exactly `(STMT, h(t))`. |
| `q3_dns_stripped.pv:43` | Repository evidence must verify under the fixed repository key and contain exactly the same `(STMT, h(t))`. |
| `q3_dns_stripped.pv:44-45` | The submitted statement must unpack into five bitstring fields. |
| `q3_dns_stripped.pv:46` | The submitted issuer key’s fingerprint must equal the statement’s fingerprint field. |
| `q3_dns_stripped.pv:47` | The possession proof must verify under that issuer key and contain `(POSS, fp(kX))`. |
| `q3_dns_stripped.pv:48` | The payload signature must verify under that same issuer key and contain `(BYTES, fb)`. |

No verifier check differs between variants; only the disclosed secret key changes from `skD` to `skR`. (`q3_dns_stripped.pv:39-55`, `q3_repo_stripped.pv:39-55`)

## The claim

Within this model, acceptance implies that at least one authority previously published the accepted key statement, the honest issuer previously recorded possession of the accepted key, and that issuer previously signed the accepted payload with that key. (`q3_dns_stripped.pv:24-27`, `q3_dns_stripped.pv:29-38`, `q3_dns_stripped.pv:49`)

Both verdict files report this correspondence as “is true”: every acceptance must have three earlier milestones—DNS **or** repository publication, issuer possession, and issuer signing. These must involve the **SAME** accepted statement `t`, the **SAME** accepted public key `k`, and the **SAME** accepted payload `fb`; unrelated publications or signatures cannot satisfy the query. The evidence values themselves appear only on the acceptance side, so the query does not separately identify their publication histories. (`q3_dns_RESULT.txt:1`, `q3_repo_RESULT.txt:1`, `q3_dns_stripped.pv:23-27`)

## The adversary

The adversary can intercept, suppress, replay, and replace public-channel messages; construct statements and submissions; and sign with keys it holds, including its own keys. Its strongest explicitly granted capability is disclosure of an authority secret key at line 55: `skD` in the DNS variant, `skR` in the repository variant. (`q3_dns_stripped.pv:2`, `q3_dns_stripped.pv:5-7`, `q3_dns_stripped.pv:40-41`, `q3_dns_stripped.pv:55`, `q3_repo_stripped.pv:55`)

It cannot obtain the other authority’s or honest issuer’s secret key through a modeled disclosure, replace the verifier’s configured authority keys, or make a signature verify under an unrelated public key: the only verification rule requires `pk(k)` for the signing key `k`. (`q3_dns_stripped.pv:7`, `q3_dns_stripped.pv:52-59`, `q3_repo_stripped.pv:52-59`)

In particular, it lacks A1.3’s DSKS capability: choosing a substitute key after seeing a valid signature so that the existing signature verifies under that substitute key. Ordinary self-signing is available, but this signature-reinterpretation capability is absent. (`A1.3-adversary.txt:9-11`, `q3_dns_stripped.pv:5-7`)

## Why the attack fails

The natural attack is to construct a statement naming the adversary’s own key, forge authority evidence using the leaked key, and supply valid possession and payload signatures made with the adversary’s key. The uncompromised authority check stops it: line 43 in the DNS-leak variant, line 42 in the repository-leak variant. Both require a signature over the attacker’s exact statement hash, while the uncompromised authority signs only `tH`, containing the honest issuer’s fingerprint. (`q3_dns_stripped.pv:30-38`, `q3_dns_stripped.pv:42-48`, `q3_dns_stripped.pv:53-58`, `q3_repo_stripped.pv:42`, `q3_repo_stripped.pv:55`)

Reusing honest authority evidence with the adversary’s key instead fails the fingerprint equality at line 46: that evidence binds `tH`, whose fingerprint names the honest key. (`q3_dns_stripped.pv:8-9`, `q3_dns_stripped.pv:42-46`, `q3_dns_stripped.pv:53`)

## What this result does not show

- **Multiple honest identities or changing statements:** there is one honest issuer key, one honest payload `fbH`, and one honest tuple `tH`, reused across replicated processes. (`q3_dns_stripped.pv:52-59`)
- **Concrete hash or fingerprint security:** `h` and `fp` are injective symbolic constructors by construction; no collision equations are provided. (`q3_dns_stripped.pv:8-9`)
- **Key-substitution resistance:** signatures are idealized, with only matching-key verification and no DSKS capability. (`q3_dns_stripped.pv:5-7`; compare `A1.3-adversary.txt:9-11`)
- **Arbitrary channel counts:** this is `n=2`, with each variant disclosing exactly one authority key; it does not establish a result for general `n`. (`q3_dns_stripped.pv:52-59`, `q3_repo_stripped.pv:52-59`)
- **Acceptance reachability:** no vacuity/reachability query is registered here; the verdicts establish an implication, not that acceptance occurs. (`q3_dns_stripped.pv:23-27`, `q3_repo_stripped.pv:23-27`, `q3_dns_RESULT.txt:1`, `q3_repo_RESULT.txt:1`)
- **Freshness or one-time use:** the correspondence is non-injective and requires no unique publication or signing event per acceptance. (`q3_dns_stripped.pv:24-27`)
- **Meaning of bytes, concrete encodings, rotation, or implementation code:** payloads are opaque bitstrings, tuples are symbolic, and the fixed-key processes provide no such validation. (`q3_dns_stripped.pv:5-17`, `q3_dns_stripped.pv:34-59`)
- **Archiving or time anchoring:** authority evidence is modeled as signatures and publication events, without archive or timestamp checks. (`q3_dns_stripped.pv:28-33`, `q3_dns_stripped.pv:42-43`)

## Correspondence to P10

The model supports the two-channel strict-validation core of P10: both external evidences must validate, the issuer key must match their statement, and compromising either single authority key does not defeat the reported correspondence. (`P10-registered.txt:8-12`, `q3_dns_stripped.pv:42-48`, `q3_dns_RESULT.txt:1`, `q3_repo_RESULT.txt:1`)
It does not address P10’s degraded-mode policy or waiver explanations; failed checks have no modeled degraded acceptance path. (`P10-registered.txt:12-15`, `q3_dns_stripped.pv:42-50`)
Its possession proof signs only a tag and key fingerprint, not the manifest bytes, so it does not establish P10’s specified manifest-self-signature possession semantics; nor does it model the required archival and time-anchor machinery. (`P10-registered.txt:2-7`, `q3_dns_stripped.pv:28-38`, `q3_dns_stripped.pv:47`)