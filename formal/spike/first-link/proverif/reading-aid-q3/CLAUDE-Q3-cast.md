# Q3 — cast list and typing note (collaborator-authored, 2026-09-06)

Model: `formal/spike/first-link/proverif/q3_mechanism_dns_compromised.pv`
(the `_repo_` variant differs in one line: `out(c, skR)` in place of
`out(c, skD)`). Line numbers below refer to the committed file with
its header; the stripped copy used for the blind explanation has
different numbering.

## Typing note

ProVerif has one type for every message: `bitstring`. A tuple is a
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
