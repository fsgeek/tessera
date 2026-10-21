# P9 as a contract inspection (`tessera-v1-strict`)

> **OWNER DRAFT 2026-10-19, revised after Codex review (docs/reviews/exit-pages/).** (Claude Opus 5.5, owner instance.) A9.2 exit item "P9 as
> a contract inspection" (`docs/phase-0-prereg-amendment-9.md:207`). It inspects the profile text, not code: the
> code inspection is a 20 Nov item (A9:214). It changes no registered sentence. If it disagrees with A9, A10 or the
> profile, they win and this page is wrong. Abbreviations: A9 = `docs/phase-0-prereg-amendment-9.md`, A10 =
> `…-amendment-10.md`, PROF = `docs/V1-PROFILE.md` **at commit `8ea8bfa`** (another session is editing the working copy on
> 2026-10-19, so its line numbers move; read with `git show 8ea8bfa:docs/V1-PROFILE.md`), VC = `docs/V1-CONTRACT.md`.

## What is checked

- **C6** (A9:145): "The verdict is a pure function of the bundle, the published verifier and its distributed trust
  configuration." **G8** (VC:32): "The verdict depends only on the inputs above", which are the receipt, the
  published verifier and its trust configuration (VC:21).
- **P9** as registered (`docs/phase-0-prereg-amendment-1.md:278-281`): "no service-side state, no live network
  dependency, appears in the decision". Its discharge is an input enumeration plus a two-machine vector
  (`docs/phase-0-prereg-amendment-4.md:59-71`). This page is the enumeration, read from the V1 profile.
- **Question per input:** where does it come from, and can anything Tessera runs (the issuing API, A9:164; the
  `wamason.com` DNS zone; the git repository; OTS stamping; release signing) change the verdict through it?

## The inputs

| # | Input | Declared at | Comes from | Can something Tessera runs change the verdict through it? |
|---|---|---|---|---|
| 1 | Bundle bytes: twelve members plus optional `issuer_record` | PROF:154-172; container rules PROF:178-199 | The holder | **Not at verification time.** The service writes them before shipping, and a receipt ships only when complete (A9:165). Changing them afterwards is an attack the checks cover (C1, C3; A9:140, :142). |
| 1a | — bundled spec, vectors, preamble, dependency manifest | PROF:168-171 | Inside the bundle | No. They are hashed against signed or catalog values, "never parsed as policy or executed" (PROF:104); the manifest is not interpreted (PROF:987-988). |
| 1b | — OTS pending attestations | PROF:1271-1272 | Inside the bundle | No. The calendar URI is "ignored" (PROF:1272); no calendar is contacted. |
| 1c | — Bitcoin headers | PROF:167 | Inside the bundle | No. Each must equal its pin (PROF:532-534; check rows 10.1-10.2, PROF:1497-1498). |
| 1d | — `issuer_record` (unsigned) | PROF:197-199 | Inside the bundle | No. Absence never affects the verdict; a malformed present record gives `INVALID / CONTAINER_SCHEMA` (PROF:185-187). Anyone holding the bytes can cause that INVALID; nobody can cause a VALID this way. |
| 2 | Request policy (`strict` only) | PROF:220-222 (D4) | The checker | No: any other value gives `UNVERIFIABLE / OUT_OF_PROFILE` (PROF:221). **Not named by C6 or G8** (finding F1). |
| 3 | Trust configuration (root KSKs, repository entries, header pins, `as_of`) | PROF:374-382; schema PROF:1411-1450 | Ships with the verifier release, never from the bundle (PROF:205, :374) | **Yes, through the release only.** Tessera's release process writes it and the release key authenticates it by a compiled-in hash (PROF:389-398). A later release can append pins and change T, or cover evidence that was `UNVERIFIABLE` (PROF:529-531; A9:337-339). No change happens inside one installed release. |
| 4 | Frozen spec catalog: object hashes, the one `alg` id, D, δ, ε, k, DNSSEC algorithms | PROF:100-119, :142-145 | Compiled into the verifier | Only by a new verifier release. It is "independent of the bundle and of trust-configuration updates" (PROF:117-118). |
| 5 | The verifier program and its release authentication | C6 (A9:145); bootstrap PROF:399-400 | The release, signed by the release key | Through the release only. Release-key compromise is distribution compromise, a stated boundary (A9:50-52; PROF:395-396). The release format and custody are still OPEN (PROF:1148-1158; finding F5). |
| 6 | Unicode 16.0.0 tables and the ES number formatter | PROF:1019-1027 | Pinned tables bundled with the runtime | **Yes.** Unicode tables and ES serialization affect acceptance (accepted strings and numbers; A9:145, :149; PROF:1010-1027). They belong to the fixed verifier/runtime. Mismatching Unicode tables cause startup refusal rather than a receipt verdict (PROF:1026-1027). The pinned objects do not yet exist (finding F6). |
| 7 | TEST provisioning environment variables (release record, release key, catalog) | PROF:321-325 (instrument level) | The process environment | **In TEST, yes:** these variables supply items 3-5. PROF §3.5 binds no production release (PROF:316-319; A10:656-657). Finding F3. |
| 8 | A previous trust configuration | PROF:330-331 | Release checker only | No. "The offline verifier never fetches a previous config" (PROF:1422-1423). |
| 9 | The current clock | — | — | No. DNSSEC is evaluated at T_snap; "no capture time, receipt T or wall clock is ever used" (PROF:864-866); RRSIG checks are "never 'now'" (PROF:872-873); verification "does not consult the current clock" (A10:307-308). |
| 10 | The network | — | — | No input is fetched. The claim is "with no network" (A9:33) and "offline verification after installation" (PROF:1224). No profile sentence states this as a verifier rule (finding F4). |
| — | Not inputs: listing-evidence package | A10:543 | Cut from V1 | Not an input: A10.4.1 is cut (`docs/decisions/2026-10-19-listing-cut.md:10-12`); the profile has no listing text (grep `service_keys`, 2026-10-19: no match). |
| — | Not inputs: outputs outside the verdict | A10:300-305; PROF:298-303 | Computed | `utc_assessment` and the diagnostics (config version and hash) are outputs. `utc_assessment` "does not change the six-field V1 stable result" (A10:303). |

**Check-table cross-check.** Every row of the total check order (PROF:1473-1525) names its inputs. Each one is a
bundle member, a trust-configuration value (pins, `issuer_domain`, KSKs, repository keys), a catalog value or the
request. No row names another source (owner survey of the Inputs column, 2026-10-19).

## Result

On the contract text, **nothing Tessera runs at verification time reaches the verdict.** Tessera affects a
verdict in two ways only, and C6 permits both:
1. It wrote the bundle bytes before shipping (row 1).
2. It makes the verifier release, including its runtime, and the trust file that the checker installed (rows 3-6). Their authenticity is
   the distribution assumption (A9:50-52). Identical output is promised only for identical declared inputs,
   the configuration included (PROF:530-531; A9:267-270).

So G8 holds as worded, if "the inputs above" includes the request and the compiled-in catalog (F1). G8 is a
claim about the decision, not about who chose the release.

## Findings

- **F1 (CLARIFY).** C6 (A9:145) and G8 (VC:21, :32) name three inputs. The profile adds the request policy
  (PROF:220) and a compiled-in catalog (PROF:100-101). PROF:154-155 says "Nothing is taken from outside the bundle
  except the trust configuration", which omits both. Reading the catalog as part of "the published verifier"
  covers it; the request is a checker input with one legal value. Proposed: name both in the contract.
- **F2 (contract wording).** VC:62 says a different "pin set can select a different block". It does not say that
  a later release can also turn an `UNVERIFIABLE` verdict into `VALID_STRICT` (A9:337-339). A relying party who
  re-verifies under a newer release can see a different verdict.
- **F3 (open, after exit).** The TEST interface takes the release key and catalog from the environment
  (PROF:321-325). That is a verdict-relevant input outside C6's list. A10 requires production to reject TEST
  authority and a rehearsal that shows it, before the first public verifier release (A10:644-657). Until then,
  only TEST releases exist (A10:650-651).
- **F4 (CLARIFY).** No-network and no-clock are stated as claims (A9:33; PROF:1224; A10:307-308) and for DNSSEC
  only as a rule (PROF:864-866). The profile has no general rule "the verifier reads no input but these".
  The code inspection is governed by P9, C6 and A10's no-current-clock rule (A1:278-281; A9:145; A10:307-308); the profile should consolidate these requirements beside its input enumeration.
- **F5 (open, frozen by 30 Oct).** The "published verifier" is not yet an object: the release format and
  release-key custody are OPEN (PROF:1148-1158; A10:624-627). A10 freezes the format by 30 Oct (A10:639-641).
- **F6 (open).** The dependency manifest "is a schema for a future object, not the object" (PROF:990-994);
  Unicode tables, the ECMA-262 edition and SHA-1DC are not yet pinned (PROF:1219-1225). Input 6 is declared but
  not yet fixed.
- **F7 (tracker).** `formal/PROPERTIES.md:44` cites the standing probe's Q6 for the input list. That row lists
  "trust configuration only (channel public keys, `k`, `δ`)" (`formal/spike/standing-probe/RESULTS-PROBE.md:41`).
  This is stale: δ, ε and k moved to the catalog (PROF:144-145, :382-386). `docs/V1-EXIT-30OCT.md:104` cites a
  different file (`formal/spike/tla-probes/P9/RESULTS-PROBE.md`). This page supersedes both as the V1 input list.
- **F8 (schedule).** A4.1's second leg, the two-isolated-machine vector (`docs/phase-0-prereg-amendment-4.md:67-70`),
  is on neither A9.2 list (A9:205-216). The derivation places it at H1a (`docs/V1-DERIVATION-DRAFT.md:109`); the
  contract records it as not built (VC:93, :100). P9 stays `open` until it runs.
