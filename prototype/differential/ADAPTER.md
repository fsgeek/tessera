# Differential adapter: conformance `run.py` to the independent verifier

`adapter.py` lets `prototype/conformance/run.py` drive `prototype/indep-verifier/` without changing either side's
verification logic or expectations. It translates only interface matters the V1 profile leaves unspecified. It
never reads a bundle, never computes or rewrites a verdict, and never emits a refusal of its own: every stable-six
object and every `TRUST_CONFIG_UNAUTHENTICATED` refusal on stdout/stderr is printed by indep's unchanged
`verify.main()`. Indep's release bindings (`release_constants`) are set in memory per invocation, exactly as
`build_release.py` would write them; no file in `indep-verifier/` is written.

Command used (from the repository root):

```
A="prototype/indep-verifier/.venv/bin/python prototype/differential/adapter.py"
prototype/.venv/bin/python prototype/conformance/run.py --verifier "$A" --release-checker "$A" \
    --json prototype/differential/results.json
```

Indep requires Python 3.14 / Unicode 16.0.0, hence its own venv. Indep row 14.4 uses the owner-pinned SHA-1DC
(`prototype/vendor/SHA1DC-PIN.md`, hook recorded in `indep-verifier/REPORT.md`, addendum).

## Translations

| # | Interface matter | Conformance side | Indep side | Translation | Why it cannot change a verdict |
|---|---|---|---|---|---|
| T1 | Release provisioning: which trust config is authorized (profile §5/§14.2 items 1–3; release-signature format OPEN, P:1053-1057) | EA-01: `TESSERA_V1_TEST_RELEASE` = signed TEST release (`format tessera-v1-test-release/1`, raw ECDSA P-256 r‖s over SHA-256 of the JCS body), key in `TESSERA_V1_TEST_RELEASE_KEY` | A01: unprovisioned `release_constants`; explicit local build pins `TRUST_SHA256`, catalog and Unicode-binary hash | Verify the TEST release signature with the TEST release key (signer SPKI hash must equal the key file's). If authentic, set `TRUST_SHA256 = release.trust_config_sha256`, the catalog (T2) and `UNICODE_MODULE_SHA256` (hash of the running interpreter's unicodedata binary, as `build_release.py` computes it). If not authentic, leave indep unprovisioned. | Bundle verdicts depend only on the trust bytes indep then hashes and parses itself. A refusal is always indep's own (`TRUST_SHA256` absent or mismatched, or `parse_trust` failing). See note 1. |
| T2 | Catalog transport (§1, §14.2 item 7; no wire schema) | Universe catalog object inside the signed release (`catalog_sha256` checked by the adapter), fields `D`, `TEST`, `spec_id`, … | A02: canonical JSON `{"entries":[entry],"format":"tessera-v1-independent-catalog/1"}`, closed `policy.CAT_KEYS` | Rename `D` → `issuer_domain`; copy the other eleven `CAT_KEYS` fields verbatim; drop `TEST` (a label); require `spec_id` to equal `tessera-v1-strict/verification-spec/1`, the constant indep checks at row 8.2, else stop with `ADAPTER_ERROR`; order the set-valued `dnssec_algorithms` and `ds_digest_types` ascending numerically (`["13","8"]` → `["8","13"]`). Serialize with indep's `jcs`. | Same members and values. The only reorders are of sets that indep compares by exact equality with the profile constants (`policy.py:67-68`), so the universe's order would only produce a spurious `CATALOG_UNAUTHENTICATED` startup failure, never a verdict. Any untranslatable field stops the adapter (exit 3, `ADAPTER_ERROR`, which `run.py` scores as ERROR, not as a verdict). |
| T3 | Request input (D4, P:213-215; no CLI flag) | EA-02: `--request degraded` appended for L-06 only | API `verify_bundle(..., request=...)`; CLI fixed to strict | Bind `request=<value>` into `verify.verify_bundle` (functools.partial) before calling indep's `main()`. | The request value is passed through unchanged to indep's own D4 check. |
| T4 | Output and refusal signalling (P:289-294, P:365-366) | EA-03: one JSON object with the six fields on stdout; refusal = nonzero exit, code on stdout or stderr, no six-field object | Canonical JSON six fields on stdout, exit 0; startup refusal exit 2, code on stderr, empty stdout | None needed: indep's CLI output already satisfies EA-03; passed through untouched. | No transformation. |
| T5 | Release checker (P:479-486; interface unspecified) | EA-12: `CMD --previous P --next N` printing ACCEPT or REJECT | A01: build-time `build_release.py --previous-trust`, i.e. `parse_trust` on both plus `policy.check_extension` | `--previous/--next` → `check_extension(parse_trust(P), parse_trust(N), P)`; no exception → `ACCEPT`, `Fault` → `REJECT <code>`. | Indep's checker decides; the adapter only prints its outcome. Each REJECT was confirmed to fail at the intended rule (see FINDINGS.md). |

## Notes

1. **T1 performs the EA-01 release-signature check, which indep does not have.** Indep's A01 treats release
   authentication as external to the instrument (`build_release.py` "does not sign a release"). So the three
   refusal cases whose only defect is an inauthentic release signer (L-51 captured repository key, L-52a DNS ZSK,
   L-52b AWS/kms key) are refused because T1 leaves indep unprovisioned; their agreement exercises the adapter's
   stand-in, not indep's code. The four other refusals (L-50 hash not compiled, L-50b unsorted `root_ksks`, L-50c
   invalid repository point, L-50d JSON number) are refused by indep's own startup checks.
2. The SHA-1DC hook (row 14.4) is a logic change on the indep side, not an adapter translation; it is recorded in
   `indep-verifier/REPORT.md` (addendum 2026-10-14) and `prototype/vendor/SHA1DC-PIN.md`.
3. No translation was needed that could change a verdict. None was refused.
