# Independent verifier probe (throwaway)

This is a spec-sufficiency instrument, not service code or conformance evidence.
Requirements came only from the four files listed in ../GAPS.md. No existing
implementation, project vectors, prototype or formal suite was consulted.

Design: parse raw tagged objects; validate the implemented payload domain and
closed schemas; recover the exact ordered frame/signature tuple; check its
manifest bindings; stop before unsupported or unspecified checks. No execution
returns `VALID_STRICT`. Probe statuses and local reason labels are explicitly
separate from V1 verdicts. Even `REJECTED_SUBSET` is not an aggregate V1 verdict:
dispatch and global precedence have not been implemented.

Implemented: frame/anchor boundaries and limits; UTF-8, JSON syntax, depth,
duplicate names, Unicode 16 assignedness/NFC and number-free canonical bytes;
manifest and attestation schemas; common-byte equality and slot binding; rule O
packet header, body boundaries and MPIs; opaque unknown-algorithm slots; snapshot
envelope; the isolated inclusive issuance-window predicate.

Stops: numbers need exact ECMAScript serialization, not an unchecked Python
formatter; nonempty OpenPGP subpacket areas need a length encoding not reproduced
in the allowed sources. Raw-key parsing, mathematical signature verification,
possession proofs, dependency objects, DNSSEC, git paths, OTS, header histories,
dispatch and verdict aggregation are not implemented. `cryptography` is not
installed in the probe environment; nothing was installed. The Unicode runtime
must report 16.0.0 or the payload check stops. A recursive JSON parser can hit its
own limit before the specified category scan; that is a probe limitation, not a
protocol rejection. See GAPS.md for protocol questions, including what external
standards references do and do not supply.

Run locally constructed probes (no project fixtures):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/reviews/spec-sufficiency/indep-verifier/selftest.py
```

Inspect raw objects supplied by the caller:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/reviews/spec-sufficiency/indep-verifier/verifier.py \
  --anchor /path/to/raw-A_sig --manifest /path/to/raw-F_manifest
```

This raw-file API is a probe interface, not a proposed bundle container. A
structurally passing object produces `STOPPED`, with `v1_verdict: null` and
`T: null`. It establishes neither signature validity nor authority nor time.

The probes exercise boundary failures, duplicate-name and normalization traps,
UTF-16 member order, swapped slots, changed committed signatures, unknown
algorithms, explicit stopping points and window boundaries. They are not the
registered conformance suite, and a pass establishes only those local checks.
