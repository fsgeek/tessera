# SHA-1DC pin (owner decision 2026-10-14)

Normative SHA-1 collision detector for V1 row 14.4 (profile §15.4, §14.2 item 15):

- Upstream: https://github.com/cr-marcstevens/sha1collisiondetection
- Pinned commit: `a06f1adbe5522f3c939cd6a3f13d5ec7f4c1a988` (tree `b31e5144f6a3039a6cfabce35d5a2179a248c2ee`,
  `git describe`: `stable-v1.0.3-38-ga06f1ad`, committed 2025-10-30). Cloned 2026-10-14; the nested `.git`
  was removed after recording these hashes so the source is vendored as plain files.
- Source digests (SHA-256): `lib/sha1.c` 364a00322dd93914cf319d4ae45e3644ba45b713dc2e403c8382921abfdcf8e5,
  `lib/sha1.h` 78f97f092c20329d1fa8d9a8cbb3d53bb90be19cbc49f1917605a9ddf520de83,
  `lib/ubc_check.c` 7b0db83569ba82965dc0d16e51e9ad85167cdfdab343f9a02c2c475bfdd93956,
  `lib/ubc_check.h` 4a140693701da167b4709c4c1b330800a0c29f2a065d0d819567a27b3171a09f,
  `src/main.c` abb081e087604a2aa27ace3059ee1fdc840b903405e6ecb97e160ae857af53ed,
  `Makefile` 7c394be47a03e6843a9780e2e8bc4e16e0a44800305715edcd09364cd44fdfb2.
- Build: `make` in `sha1collisiondetection/` (cc Ubuntu 13.3.0, default flags, safe-hash on, reduced-round
  detection off). Local binary `bin/sha1dcsum` SHA-256
  `3fa8472a23ff8ecc6c91b5193bc6e6e7a7ef1a1bbfbbff769a89bda0634dd5fb` (compiler-dependent; a local build pin,
  not a distribution digest). `bin/` is git-ignored by the vendored `.gitignore`; rebuild with `make`.
- Prescribed collision-return behaviour used: `SHA1DCFinal` returns nonzero, which `sha1dcsum` prints as
  `<hex> *coll* <name>`; exit status is 0 either way. Input is the git-framed object
  `"<type> <len>\0" ‖ body`, read on stdin (`sha1dcsum -`).

Demonstration (2026-10-14):

| Input | sha1dcsum output | Result |
|---|---|---|
| `shattered-1.pdf` fetched from https://shattered.io/static/shattered-1.pdf (SHA-256 2bb787a73e37352f92383abe7e2902936d1059ad9f1ba6daaa9c1e58ee6970d0, plain SHA-1 38762cf7f55934b34d179ae6a4c80cadccbb7f0a) | `16e96b70000dd1e7c85b8368ee197754400e58ec *coll*` | detected (safe hash differs from plain SHA-1) |
| `sha1collisiondetection/README.md` | `68fd1a1f5867e4146ee08523bbf57c739a51f6c2` (= plain SHA-1) | passes |
| `"blob 422435\0" ‖ shattered-1.pdf` (git-framed) | `ba9aaa145ccd24ef760cf31c74d8f7ca1a2e47b0` (= `git hash-object`) | passes: the 12-byte git header shifts the SHAttered near-collision blocks off their 64-byte alignment, so a git-framed collision needs its own chosen-prefix computation (this is why conformance L-94 is not built) |
