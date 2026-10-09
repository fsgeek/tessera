# Capstone run outputs — compressed archive

Raw ProVerif outputs (`*.out`) and peak-memory records (`*.rss`) total about 600 MB, so they are kept out of git
as raw files (see `.gitignore`) and preserved here as xz tarballs, about 7.7 MB in all. Archived 2026-10-09 by
the owner instance.

- `outputs-ladder3.tar.xz`: ladder 3, the files at `proverif/` top level, which `RESULTS.md` cites.
- `outputs-ladder2.tar.xz`, `outputs-ladder1.tar.xz`: the archived ladders under `ladder2/` and `ladder1/`.
- `outputs-dev.tar.xz`: diagnostics and probes under `dev/` (slice probe, abl_d, divergences, codex scratch).
- `SHA256SUMS`: the SHA-256 of every raw file, with its path relative to `proverif/`.

**To check any citation** such as `cap_cc02_a.out:4430`: from `formal/suite/capstone/proverif/`, run
`tar -xJf archive/outputs-ladder3.tar.xz && sha256sum -c archive/SHA256SUMS`, then open the file. The round
trip was verified when this archive was made (all 693 files matched; an earlier draft of this README said 2,079, which double-counted the per-part lists).
