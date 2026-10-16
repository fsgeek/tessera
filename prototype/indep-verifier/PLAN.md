# Independent instrument plan

Purpose: differential testing of the V1 stable six fields, derived solely from
Amendment 9, V1-PROFILE and ENCODING-V1 plus their cited external standards.
No other implementation, vectors, reviews or formal artifacts are inputs.

1. Write parser tests from the grammars, observe missing-module failure.
2. Implement strict JSON/JCS, frame, signature, OTS, Bitcoin, DNS and git parsers.
3. Implement P-256/RSA verification and DNSSEC candidate aggregation.
4. Implement trust schema, explicit build-time release binding and external catalog.
5. Implement every numbered reporting row, independently collecting failures and
   unperformability, including receipt T even when unrelated checks fail.
6. Exercise parser boundaries, candidate order, synthetic signed evidence and
   multi-failure reporting; record unresolved dependencies and actual coverage.

Files: codec.py (JSON/frames/signatures), anchors.py (OTS/Bitcoin), dnssec.py
(snapshot/RFC validation), git_channel.py (git), policy.py (trust/catalog),
verify.py (CLI/row aggregation), tests/, AMBIGUITIES.md, REPORT.md.
All outputs and dependencies stay in this directory. No service imports,
production claims, network at verification time, commits or external writes.
