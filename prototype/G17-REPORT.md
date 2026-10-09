# G-17 experiment: can a bundle choose its own required set? (THROWAWAY, 2026-10-07)

## Outcome

**It depends on what a "binding-form identifier" names, and the spec does not say which.**

- **The spec as literally written: no.** The spec's binding forms are the statement encodings
  `STMT_DIGEST` and `STMT_DIRECT` (l.792), not authority channels. The channels come from the
  verifier's trust configuration, and V23 says "both". The attacker in capstone case (b) holds
  the repo key and its own issuer key, but has no dns evidence. Under strict its bundle gets
  `UNVERIFIABLE`, because dns is required and absent. If the attacker instead writes `"repo"`
  into the set, the verifier rejects it as an unknown identifier (`UNVERIFIABLE`). This held on
  both the stub path and the real path.
- **The reading TRIAGE finding 1 feared: yes.** In that reading, the signed set names channels
  and the verifier takes the required set from the bundle. The attacker signs `{repo}` with its
  own key, presents only the leaked repo evidence, and gets **`VALID_STRICT`** on both paths. This
  is a strict acceptance of a key no honest issuer signed (link 1b / `Accept ⟹ IssuerSigned`
  red in case (b)). Signing the set does not help, because the attacker signs it.
- **The proposed fix: no.** Here the verifier's policy fixes the required channels, and V21 only
  checks that the bundle's set is well-formed. On the same bytes the verdict is `UNVERIFIABLE`
  (dns absent). Under a degraded policy it is `VALID_DEGRADED(policy=degraded-waive-dns)`, the
  registered cost from case (d).
- **The literal reading still leaves a smaller form of the same gap.** The verifier cannot
  require a particular *form*. A bundle that signs `{STMT_DIGEST}` is `VALID_STRICT` even when the
  verifier wants `STMT_DIRECT`. Both forms bind the same tuple, so this is a downgrade only in that
  the digest form adds a dependency on hash collision resistance.

## Evidence

Fourteen new tests: `tests/test_g17.py` × {stub, real}. All 89 tests pass; the 75 existing tests
are unchanged.

- The real path is `scenarios.build("real")`. The attacker's slot key is a KMS-OpenPGP P-256 key
  (alg `OPENPGP4-ECDSA-P256-SHA256`), anchored with real-format OTS on regtest. The channels are
  stub Ed25519 keys on both paths (`real/world.py` l.11).
- The attacker issues under Tessera's issuer id with its own slot key and the leaked repo channel
  only, and anchors on the public chain. Its own key signs the binding-form set.

| Bundle | `binding_ids` / `required_from` | Verdict (stub = real) |
|---|---|---|
| honest, {dns, repo} evidence | forms / bundle | `VALID_STRICT` |
| honest, signed set `["dns","repo"]` | channels / bundle and channels / policy | `VALID_STRICT` |
| attacker, signed set `["STMT_DIGEST"]`, repo only | forms / bundle (spec-literal) | `UNVERIFIABLE`, `V20[dns:STMT_DIGEST]` absent |
| attacker, signed set `["repo"]` | forms / bundle (spec-literal) | `UNVERIFIABLE`, V21 `BINDING_FORM_UNKNOWN` |
| attacker, signed set `["repo"]` | **channels / bundle** | **`VALID_STRICT`**: only `V20[repo]` is checked; standing `None` |
| attacker, signed set `["repo"]` | channels / policy | `UNVERIFIABLE` (V21 pass, dns absent); degraded: `VALID_DEGRADED`, observation `absent` |
| honest, signed set `["STMT_DIGEST"]`, policy wants `STMT_DIRECT` | forms / bundle → forms / policy | `VALID_STRICT` → `UNVERIFIABLE` |

How the switches are built:

- They are fields on `TrustConfig`: `binding_ids`, `required_from` and `policy_forms`, in
  `tessera_proto/verifier.py`.
- The issuer gained `declared_set`, so the signed `binding_forms` can carry channel names.
- The defaults reproduce the earlier behaviour exactly.

A side observation from the attack row: the envelope and standing paths disagree. The standing
path already fixes its channels from the trust configuration (`standing.py:26`), so under
channels / bundle it declines to evaluate while the envelope path says `VALID_STRICT`.

## Which sentences decide it

**These make the downgrade fail:**

- **l.792:** "binding-form identifier | `STMT_DIRECT`, `STMT_DIGEST`; extensible". This makes the
  vocabulary statement forms. R-4.30 (l.957) says the same.
- **V23 (l.1302):** "both external evidences validate". The channel requirement is fixed, not
  relative to any set.
- **R-5.8 (l.1217):** the channel keys are in the verifier-distributed trust configuration.
- **R-2.26 (l.282):** strict means no waived check.
- **R-2.37 (l.308):** an unknown identifier yields `UNVERIFIABLE`.

**These let the downgrade succeed, or fail to stop it:**

- **R-3.37 (l.635) / V21 (l.1300):** "a verifier must successfully validate every required
  form". "Required" is defined only by the envelope's own set, and the verifier is given no floor.
- **The §3.4 table (l.585):** "Who sets: issuer".
- **R-4.29 (l.955):** the evidence commits "through one or more … forms declared inside the
  signed envelope".
- **"extensible" (l.792):** nothing forbids a form whose scope is channel-specific.
- **No sentence links V21's forms to V23's channels.** Requiring every (channel × form) pair is
  the prototype's own guess (G-17), not the spec's.

## Would the capstone catch it?

**No: the capstone already assumes the fix, so the attack lies outside its model.**

- `capstone.pv:606-607` hard-codes `checksign(evD, pkDv)` and `checksign(evR, pkRv)` under
  `STMT_DIGEST`. Both channels and the form are fixed by the verifier, as CAP l.84-91 states, and
  the model reads no set from the bundle.
- Its green link 1b in cases (a) and (b) is therefore evidence for the policy reading only.
- It would show the attack only with a companion whose verifier takes the required channels from
  the bundle's signed set. The prediction is that link 1b and `Accept ⟹ IssuerSigned` go red in
  (a) and (b), matching the `VALID_STRICT` row above.

## One-sentence spec fix

> The verifier's declared policy, never the bundle, fixes which authority channels and which
> binding forms `VALID_STRICT` requires (every trust-configuration channel under every
> policy-required form); V21 checks the envelope's signed set only for well-formedness and
> support, and a policy-required channel or form the bundle does not evidence is a required check
> not performed.
