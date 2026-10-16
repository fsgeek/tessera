# Independent V1 verifier instrument

This is differential-testing code under A9.2, not a service verifier and not
C-row discharge evidence. Read [REPORT.md](REPORT.md) and
[AMBIGUITIES.md](AMBIGUITIES.md) before interpreting its results.

**This build cannot return VALID_STRICT for a complete bundle:** the required
pinned SHA-1DC detector is not supplied by the allowed normative inputs. Row
14.4 is explicitly unperformable. The distributed release is also deliberately
unprovisioned: no real trust configuration or frozen catalog was provided.

## Local environment and tests

From this directory:

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install --no-cache-dir -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
source .venv/bin/activate
```

No global installation is required. Python must be 3.14 and its Unicode tables
must report 16.0.0. The local build also binds the Unicode implementation
binary (the executable when unicodedata is built in).

## Interface

Provisioning is a separate, explicit instrument build step:

```sh
python build_release.py --trust TRUST_CONFIG --catalog CATALOG
python verify.py --trust TRUST_CONFIG --bundle BUNDLE
python verify.py --trust TRUST_CONFIG --bundle BUNDLE --catalog CATALOG
```

The builder validates and embeds the catalog and pins both input hashes in
`release_constants.py`. It does not sign a release or establish independent
release-key custody. An external `--catalog` must match the compiled hash.
Trust-config schema is the profile's exact §15.5 schema. Catalog transport is
the explicitly documented instrument reading A02; see `policy.CAT_KEYS` and
`examples/catalog.json`. Nothing supplied by a bundle changes policy.

The catalog's single `alg` selects semantic support and registered supplements.
Every installation knows the ENCODING-V1 classical baseline. Only a hybrid
catalog registers the pair's codec: a fallback installation decodes both hybrid
slots as opaque, with cap 65536, before `UNVERIFIABLE / ALG_UNKNOWN`. A hybrid
installation knows both ids; unselected classical frames still use rule O.
The registered pair's kms slot uses
3309-byte raw ML-DSA-65, pure mode with empty context, and the exact 1974-byte
SPKI; gpg retains rule O. Unsupported receipt algorithms skip key and signature
semantics (EA-31), contributing `UNVERIFIABLE / ALG_UNKNOWN`; independent
codecs and other checks still apply. Draft/registration interpretation and K-R's
assumption status are recorded in the hybrid addenda to REPORT and AMBIGUITIES.

Optionally pass `--previous-trust PRIOR_CONFIG` to the builder to check the
append-only transition. The runtime never retrieves prior configs.

After successful startup the CLI prints exactly one canonical JSON object with
`T`, `historical_security`, `reason`, `revocation`, `standing`, `verdict`.
INVALID and UNVERIFIABLE are normal verdicts (exit 0). Startup and I/O refusals
use exit 2, stderr and **no stdout verdict**. There is no network access.

## Synthetic demonstration

`examples/` contains generated public inputs with fabricated Bitcoin headers
and trust pins. These are parser/logic fixtures, never historical evidence.
To regenerate them and provision a disposable local instrument:

```sh
python generate_example.py
python build_release.py --trust examples/trust.json --catalog examples/catalog.json
python verify.py --trust examples/trust.json --bundle examples/bundle.json
```

Expected reason: `INDEPENDENT_SHA1DC_UNAVAILABLE`, with the fixture's receipt T.
Unit tests temporarily provision generated release bindings and restore the
original constants in `finally`; they do not bind your instrument to their
random test keys. Test signatures and keys are generated locally, without any
Tessera fixture/implementation imports. Private keys are not written.

## Reading the result

A T reported with INVALID is not evidence of a valid service receipt. An
ISSUANCE_WINDOW failure can arise from presenting a later proof: request the
issuer's original proof. The verifier cannot establish public publication of
the git commit. It does not evaluate revocation or historical key/algorithm
safety, nor submitter identity, payload truth, priority, renewal or standing.
