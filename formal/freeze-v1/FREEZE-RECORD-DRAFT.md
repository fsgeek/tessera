# V1 freeze record (DRAFT)

> **Status: DRAFT, assembled 2026-10-21 by an owner subagent (Claude Opus 5.5).** Not signed, not committed. The
> preamble bytes are a drafted candidate, not authored text (see "Open before this becomes the freeze record"); the
> preamble, catalog and therefore every receipt-bound hash change if they are replaced. Profile section 14.2 item 7,
> section 15.8; `docs/V1-FREEZE-OPEN.md` §7; `docs/V1-EXIT-30OCT.md` §3.

## Named commit

`481d54a57a9e60e3bf1f0174cf6d67e262a24d89` (481d54a). Every part is a tracked regular-file blob at this commit (section 15.8 canonical recipe).
Signing commits checked: A9 `docs/phase-0-prereg-amendment-9.md` at 481d54a has the same blob as at `2ad3489`; A10
`docs/phase-0-prereg-amendment-10.md` at 481d54a has the same blob as at `9ade764` (PR-08).

Pre-assembly check: `git diff 481d54a --stat` showed only `docs/V1-CONTRACT.md` (uncommitted) and `timestamps/`; neither is a part.

## Objects

| Object | File | Bytes | SHA-256 |
|---|---|---|---|
| catalog.json | `formal/freeze-v1/objects/catalog.json` | 662 | `4ea643092bf52cd113bf782a57808df546524c18e9914e266e288af5fc986b65` |
| dependency-manifest.json | `formal/freeze-v1/objects/dependency-manifest.json` | 41181 | `20020475a8ef852fbd3d9331b370a3161e925a44cddf83c8f51d26be2ac9e063` |
| preamble.bin | `formal/freeze-v1/objects/preamble.bin` | 611 | `93eabba93422b3c97580c42f1671dff542b4dfb9fd135b949107c84886372729` |
| spec.bin | `formal/freeze-v1/objects/spec.bin` | 469354 | `3b2ba1ada8baa6ab6735d6d308a2f5faaa21a1bd066c40f75b5d505e43a1a0d9` |
| vectors.bin | `formal/freeze-v1/objects/vectors.bin` | 3123748 | `19ac772a155daf3808727587407a09410572e8291235524b8c36a1ac870bdf3f` |

Catalog (profile section 1): `alg` = `KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA256`, `D` = `wamason.com`, δ = 259200 s,
ε = 86400 s, k = 6, Δ (`utc_delta_s`) = 7200, m (`utc_m`) = 6, `alg_prohibited` = [], `binding_forms` = ["STMT_DIRECT"],
DNSSEC algorithms {8, 13}, DS digests {2, 4}, and the four object hashes above. Field names follow the TEST catalog
form of `prototype/e2e/freeze.py` without its `TEST` member. RFC 8785 canonical.

Dependency manifest: blob `ac5900fb650181084216a88fd2c4d7b99d3d918f` of `formal/dependency-sources/dependency-manifest.json`, verbatim; its hash equals the one in `formal/dependency-sources/MANIFEST.md`.

## Recorded beside, outside every part

- Current `formal/p8/PROOF.md` SHA-256: `cae680b781f00e2911cfa6d17e86fe8e04595843921d8234fddda51d53ec22bc` (HYBRID-SUPPLEMENT §9 baseline: `06910a5f81128e05694e4ee8c3034e8149fbac04b330dcb2a1ed9386fd21ff30`).
- Frozen `formal/p8/ENCODING-V1.md` SHA-256: `6da057fbdd0a45ab9002864d648451ad95b82fa3f2d342a3e7df6a3390ab5316` (registration record's post-§5.2 hash: `fe537b1fd68efa51d0a9e6cf29cb8572a9d8ef7906e6a9cf05de035dc446efd0`; the difference is ENC's 2026-10-19 change accounting, profile section 13 note 11).
- Spec-object hash for the branch-registration record (A9.6): `3b2ba1ada8baa6ab6735d6d308a2f5faaa21a1bd066c40f75b5d505e43a1a0d9`.

## Verification (2026-10-21)

- (a) Assembled twice from a clean `git worktree add --detach` of 481d54a in a `mktemp -d` directory: `diff -r` identical. Independent agreement check (`assemble.py --check`): every part re-parsed and compared with the clean checkout's file and with `git show`; all hashes and catalog fields recomputed: OK. Worktree removed.
- (b) Vectors object extracted part by part: `formal/p8/vectors/check.py` exit 0 (baseline 71/71, 173/173, 5/5; hybrid 35/35, 63/63, 1/1, 6/6); `test_check.py` 6 OK (3 skipped); `cases-index.json` 352 ids = 352 `expected.json`, 0 verdict/reason mismatches. `prototype/conformance/selfcheck.py` cannot run on the object: it needs `bundle.json`, which is excluded (EA-10).
- (c) `catalog.json` and `dependency-manifest.json` pass `parse_json(canonical=True)` (`prototype/indep-verifier/codec.py`); `rfc8785` 0.1.4 reproduces `catalog.json` byte for byte.
- (d) `e2e/driver.py init --mode dry --freeze-dir formal/freeze-v1` then `run`: freeze stage took this directory (catalog `4ea64309…`); independent verifier `VALID_STRICT / OK`, `utc_assessment` A-UTC-7200-6. Dry mode: TEST signers, stub chain and DNS, TEST release key.

## NOT in the freeze

- Instrument code: everything under `prototype/` except the vectors parts listed below (the four generator sources and `run.py` enter as vectors parts per `VECTORS-OBJECT.md`); `prototype/e2e/freeze.py`; this directory's `assemble.py`.
- Receipts: `prototype/e2e/receipts/real-1`, `real-2` (signed over TEST objects) and every conformance `bundle.json` (342), `release.json` and `trust.json` (344 each), case `catalog.json` (19), `universe-catalog*.json`, `universe-release-key.json`: they embed object hashes (EA-10). They must be reissued against these objects.
- `selfcheck.py`, `REPORT.md`, `VECTORS-OBJECT.md`, differential `results*.json`; L-94 and F04 "mixed" (not built; dispositions in `prototype/conformance/REPORT.md`).
- The trust configuration and release key (compiled into a release, section 15.9), and `docs/V1-CONTRACT.md`.

## Open before this becomes the freeze record

1. **Preamble bytes are a draft.** No authored purpose preamble exists at 481d54a (`V1-FREEZE-OPEN.md` §7: "Author the real preamble bytes"). The bytes in `objects/preamble.bin` restate profile §11 rows a/f/i (PR-01 wording) without TEST markings. Replacing them changes `preamble_sha256` and the catalog hash; spec, vectors and dependency hashes do not move.
2. The `A9:nnn` locator refresh (section 0) and the freeze commit of every source are not done here.
3. The vectors object includes generator sources that embed TEST stand-in constants, as `VECTORS-OBJECT.md` specifies.

## Part inventory

### spec (6 parts, bytewise path order)

| Path | Blob | Bytes |
|---|---|---|
| `docs/V1-PROFILE.md` | `02319def5ce8ec67b0f0d869781aa88d25b123de` | 187874 |
| `docs/phase-0-prereg-amendment-10.md` | `bfff9b2a671ae0b158891bd7382bc907efef2794` | 83064 |
| `docs/phase-0-prereg-amendment-9.md` | `a587742fd3053eac45b10d14001a44fd32cf565b` | 53060 |
| `formal/p8/ENCODING-V1.md` | `364177a86dc28de74038f3f3fc2be152ff02d2ea` | 62813 |
| `formal/p8/HYBRID-SUPPLEMENT.md` | `bf66174879ac32bbbc867154c42cdca906922239` | 40588 |
| `formal/p8/PROOF.md` | `cefa668ed9abc3e293b0918f91b7b938470e48b3` | 41651 |

### vectors (387 parts, bytewise path order)

| Path | Blob | Bytes |
|---|---|---|
| `formal/p8/vectors/check.py` | `0843a824eae219cb9dee092fe0f1ffe4626fce98` | 47942 |
| `formal/p8/vectors/fuzz.py` | `c4e6ad30a2ea18efddb5d77954268fd5328bdb1d` | 12674 |
| `formal/p8/vectors/gen.py` | `44d4dcc9a0cb2e79129b80a62061f0767348e6c0` | 120291 |
| `formal/p8/vectors/golden.json` | `987f23cdcc789dc9c9eefa3bcab725ab4163589a` | 58777 |
| `formal/p8/vectors/hybrid-golden.json` | `246ac08aae5a0ae4dfcb5f6c10542b0b8170ba7e` | 635857 |
| `formal/p8/vectors/hybrid-reject.json` | `cf87f8a75e224890ab36ba8c58d9f3d2ca250140` | 1001903 |
| `formal/p8/vectors/reject.json` | `8a64f1a1dcad3fc5d2f297bd29ada50c43ada797` | 522238 |
| `formal/p8/vectors/test_check.py` | `e2fe8439a05fe517fe1d8786aba164ea854315e0` | 4565 |
| `prototype/conformance/cases-index.json` | `064bbb322b10a016d168c8a1702aa47af93194c7` | 72249 |
| `prototype/conformance/cases.py` | `ec99e108dd509024128598c288b8fec1e3109d82` | 146683 |
| `prototype/conformance/cases/A-a/expected.json` | `5596e1694bf3441d5d20e30ab72c87076dbc607d` | 826 |
| `prototype/conformance/cases/A-b/expected.json` | `678a5a9dfecf5f02ade6e0b9b40e4c4e7b6aee03` | 1081 |
| `prototype/conformance/cases/A-d3/expected.json` | `70ab54c3a475dc3e03bdc8a62b1217b9ecbcfb89` | 1063 |
| `prototype/conformance/cases/A-e/expected.json` | `7e866b1ac128e1eac038d956d7dfd0aeed4a9c4f` | 872 |
| `prototype/conformance/cases/A-e2/expected.json` | `515265cf0e1d45ce894e7689f82b82afadb4e6e2` | 778 |
| `prototype/conformance/cases/A-f/expected.json` | `3ec23f1cfc088352ae805d514402790292c9db79` | 813 |
| `prototype/conformance/cases/A-i/expected.json` | `399259f4f6bf58b88a30517b3aa71dc4c55d39e2` | 807 |
| `prototype/conformance/cases/A-i2/expected.json` | `6dd98be73f6400ec60134a2ccdcfc7be7a0d7f74` | 806 |
| `prototype/conformance/cases/AGG-a/expected.json` | `ac923bfaabe335082b196bc695ebac73dbe0b9a5` | 800 |
| `prototype/conformance/cases/AGG-b/expected.json` | `e425a15f978d5716b32d3ffcee77b916a2e440e0` | 779 |
| `prototype/conformance/cases/AGG-c/expected.json` | `e0aa100fa1ff2a8e113bb35090f89c0a55f61839` | 759 |
| `prototype/conformance/cases/AGG-d/expected.json` | `e5b2a7e36e1c9d6b047a646d3a716a1d4ddb6771` | 807 |
| `prototype/conformance/cases/AGG-e/expected.json` | `05e1f6109b20003248308bc0c7cee80ff03eb9e2` | 747 |
| `prototype/conformance/cases/AGG-f/expected.json` | `27c94ae82845055e4e86f29f9c34b0f846315f03` | 784 |
| `prototype/conformance/cases/AGG-g/expected.json` | `5e1974840ae7a90bcc815cd72f475034855c6603` | 776 |
| `prototype/conformance/cases/AGG-h/expected.json` | `7fb02380aa791a5bc468c4cc5e48bba1f4f5a7fe` | 794 |
| `prototype/conformance/cases/ALG-01/expected.json` | `89f3a80df05cae06b1716555601afe09ede54e1a` | 847 |
| `prototype/conformance/cases/ALG-02/expected.json` | `16b18b16a1cff47d79e710bf4e067f92a179f4e4` | 837 |
| `prototype/conformance/cases/ALG-03/expected.json` | `11b068ad50296494c444bc1d7fcd6035a98d348f` | 833 |
| `prototype/conformance/cases/ALG-04/expected.json` | `9d97b4c548833143be68a5c5b0440b865282a70d` | 892 |
| `prototype/conformance/cases/ALG-05/expected.json` | `b4d00e00870afd8958847385e2eb86255fe53318` | 807 |
| `prototype/conformance/cases/AUTH-i-T/expected.json` | `602ee3b5b8fb44a619442d24aa8ddeebbb517b0d` | 1042 |
| `prototype/conformance/cases/AUTH-i/expected.json` | `cf36193957ca3d7a464fb3dd7ae3385cdf31cae7` | 1518 |
| `prototype/conformance/cases/AUTH-ii-ds-T/expected.json` | `a5c38dbffd194031a7ceeb37316320ba943e4d70` | 1034 |
| `prototype/conformance/cases/AUTH-ii-ds/expected.json` | `967ca0a0e9ede822bb0c171c04a5ebf18ef39189` | 1798 |
| `prototype/conformance/cases/AUTH-ii-root-T/expected.json` | `5cd7696c1d2672520f82edebf8689d78b625d041` | 1106 |
| `prototype/conformance/cases/AUTH-ii-root/expected.json` | `d36420f6d3f41c059344b5bd88ebba679fd73c86` | 1953 |
| `prototype/conformance/cases/AUTH-ii-tag-T/expected.json` | `9e55c8beaaac3e132f2f79133bdb48ff26ab580e` | 1053 |
| `prototype/conformance/cases/AUTH-ii-tag/expected.json` | `d26b130637712399f497518eff877e04c585a3a2` | 1674 |
| `prototype/conformance/cases/AUTH-ii-zsk-T/expected.json` | `c6939f736ec38ef982bc404634eb4dfdef4f0f1d` | 1069 |
| `prototype/conformance/cases/AUTH-ii-zsk/expected.json` | `e8bd29905f52a1ecbf3f34fe100fde907326696d` | 1830 |
| `prototype/conformance/cases/AUTH-iii-T/expected.json` | `71b81a46156abe361ee993b6ab4595acee2ab9d4` | 1087 |
| `prototype/conformance/cases/AUTH-iii/expected.json` | `afe7cc65608981b176a05d31151f147bfcd1d165` | 1650 |
| `prototype/conformance/cases/AUTH-iv-end-T/expected.json` | `128718bb95a980ebba08ef2f9c76dd3f6bd68db1` | 1010 |
| `prototype/conformance/cases/AUTH-iv-end/expected.json` | `20f5b609f89205f8f275b6819767a7e510f31d3f` | 1512 |
| `prototype/conformance/cases/AUTH-iv-start-T/expected.json` | `bb19af8900081c3fce841130481c7e88bda1e337` | 960 |
| `prototype/conformance/cases/AUTH-iv-start/expected.json` | `6032e39c98b07bc40c3cc6a4019c1da197228269` | 1542 |
| `prototype/conformance/cases/AUTH-v-after-T/expected.json` | `8cd3d9c7c17dc3d0f5eee18bc2bee33eb84500ec` | 927 |
| `prototype/conformance/cases/AUTH-v-after/expected.json` | `30c45851330c03d495fb48d9d7194c5b7137d339` | 1391 |
| `prototype/conformance/cases/AUTH-v-eq-T/expected.json` | `38f84f2e2b819cb7eb824a2c06b3a0d55fb66785` | 959 |
| `prototype/conformance/cases/AUTH-v-eq/expected.json` | `81ada7b9774bc9874fe5e6b122a9b886a81c5d4a` | 1453 |
| `prototype/conformance/cases/AUTH-vi-T/expected.json` | `15e0b745f83b7f609bbe7264ec4fe36cf2c265cc` | 970 |
| `prototype/conformance/cases/AUTH-vi/expected.json` | `673beaf21fd46f8c3ea438cab4df0b5d0cb799f8` | 1889 |
| `prototype/conformance/cases/CH-01/expected.json` | `33ade0596e67e3e3c26dbe2a4d9e1d9ffba2bc69` | 784 |
| `prototype/conformance/cases/CH-02/expected.json` | `884a0e1e5e35810180e648b75b5a4ab8254e7af1` | 900 |
| `prototype/conformance/cases/CODEC-a/expected.json` | `e83d1e589a093ddf6db3d0a96ac7d5e9d129f3d9` | 760 |
| `prototype/conformance/cases/CODEC-b/expected.json` | `5df822a611f913257fd6e0a5fe9c427d842f52ec` | 747 |
| `prototype/conformance/cases/CODEC-c/expected.json` | `ce931cc1fec72a59eaf6c2c51fa8bd9f9422a224` | 762 |
| `prototype/conformance/cases/CODEC-d/expected.json` | `57b4aeda0999b29a132a9f988cdf2fabcd7ce1a5` | 771 |
| `prototype/conformance/cases/CODEC-e/expected.json` | `0d4939f045a30507ec4fa292ab66df27fcb52e47` | 795 |
| `prototype/conformance/cases/CODEC-f/expected.json` | `b19d3b3ba5610c7c9d3d9ae097513dc1a27bbba0` | 801 |
| `prototype/conformance/cases/DNS-expired/expected.json` | `4508965424f000611b227a44308903cbe75bae9a` | 780 |
| `prototype/conformance/cases/DNS-keys/expected.json` | `512369c5e6271caac08eb1043ad303deb9815342` | 786 |
| `prototype/conformance/cases/DNS-profile/expected.json` | `bc4142fed3d34dd57d56c1ba333a8138ad54f800` | 777 |
| `prototype/conformance/cases/DNS-rootsig/expected.json` | `dbda36040fea502637cd4d2dd2ee3863b05bb328` | 817 |
| `prototype/conformance/cases/DNS-sig/expected.json` | `0aa38d3de0d3080f3df8f490db7bfcd88f99043e` | 759 |
| `prototype/conformance/cases/DNS-wlen/expected.json` | `300f3379f2c549f69fcd703ff6006fb839c5c6af` | 790 |
| `prototype/conformance/cases/DNS-wlen90/expected.json` | `225469cc2ba7c0efb96783bba7781b50fb9a25ee` | 763 |
| `prototype/conformance/cases/F03-a/expected.json` | `685c76593acec4af0c6a63a900dd9fb08fb58bff` | 842 |
| `prototype/conformance/cases/F03-b/expected.json` | `8cb244c1e9657e6b60a0653aaeb7759d4f04a16e` | 840 |
| `prototype/conformance/cases/F03-c/expected.json` | `30c111ccfc31fdb21e7b6d3b8452b017d06fae8c` | 856 |
| `prototype/conformance/cases/F03-d/expected.json` | `ee2169b1ef2ca27688d576bb68c044126a140998` | 824 |
| `prototype/conformance/cases/F03-e/expected.json` | `7e21489a2a6c7dabeda82837ed2b770d260f57bc` | 841 |
| `prototype/conformance/cases/F03-f/expected.json` | `58e63578c5d222ae738396b6077de5f1111ebc33` | 808 |
| `prototype/conformance/cases/F03-g/expected.json` | `9af2162703f9acc86ba6d5472e07c398dcd860c4` | 802 |
| `prototype/conformance/cases/F03-h/expected.json` | `771f7dc84495df3be4b12160f66125b4b88b7f53` | 775 |
| `prototype/conformance/cases/F03-i/expected.json` | `c8983b98b6ac070457fb2d83859e38c13a2a7510` | 782 |
| `prototype/conformance/cases/F03-j/expected.json` | `70d98b24464d41dd221fcc3f4daeea0600cc2d76` | 832 |
| `prototype/conformance/cases/F05-a/expected.json` | `caa42599cfb76f8f159a42f933d1b5cbdd484004` | 800 |
| `prototype/conformance/cases/F05-b/expected.json` | `75874cc1989f4c5da4280bb916a9500236eae803` | 775 |
| `prototype/conformance/cases/F05-c/expected.json` | `7cdb422057104ef8e737dd68594d51ebddfe6f4e` | 783 |
| `prototype/conformance/cases/F05-d/expected.json` | `830f636be8e69b12618d7ca10f0295cac9608a32` | 796 |
| `prototype/conformance/cases/F05-e/expected.json` | `d78e12ae8625f4f9960795b64129c1efe8b36ef7` | 900 |
| `prototype/conformance/cases/F05-f/expected.json` | `c79d67bd102b80c44614bac62d3bb261058423b0` | 812 |
| `prototype/conformance/cases/F06-a/expected.json` | `41bb84ef3c897689ad935673ca8a0f8332841c38` | 810 |
| `prototype/conformance/cases/F06-b/expected.json` | `0a69c874326588525be9880642cfd24f14cb4588` | 813 |
| `prototype/conformance/cases/F06-c/expected.json` | `5111209e04dcdc1f7a7bf340a9d5912c41d10f8b` | 801 |
| `prototype/conformance/cases/F06-d/expected.json` | `110798db38b5b28f96aedfe204613a96e419e7e5` | 763 |
| `prototype/conformance/cases/F06-e/expected.json` | `a83acbf0724b294a1dab66742e4906f1b358c3b4` | 777 |
| `prototype/conformance/cases/F06-f/expected.json` | `551a1f918c5444d2912425d0e4a71ceda5399ee2` | 800 |
| `prototype/conformance/cases/F06-g/expected.json` | `2cda1513852adf7c9a61bb255f2d316fecb762f6` | 760 |
| `prototype/conformance/cases/F06-h/expected.json` | `8c567f1ec536dd3cff84550704cc66772f571b39` | 792 |
| `prototype/conformance/cases/F07-a/expected.json` | `803fac3073aee1222511d97a5a5ee3a38e8df815` | 780 |
| `prototype/conformance/cases/F07-b/expected.json` | `8c151f0a69c799e354f750517fc23833172bae39` | 825 |
| `prototype/conformance/cases/F07-c/expected.json` | `d0a6dba2e444d779eb35f88d8105b4c47d466eef` | 788 |
| `prototype/conformance/cases/F07-d/expected.json` | `3a3e367ca9dfcc7902df133b130c6c7956a0093e` | 745 |
| `prototype/conformance/cases/F08-a/expected.json` | `be563b93143fdc09bd54f3194829a8e07b5bff2f` | 829 |
| `prototype/conformance/cases/F09-a/expected.json` | `9b65ed14f9189c22dbadf8e2185187b16d03eb0f` | 809 |
| `prototype/conformance/cases/F09-b/expected.json` | `0c1f0b392c7e39bffbc0f3ad38344ac35063bfc9` | 818 |
| `prototype/conformance/cases/F09-c/expected.json` | `2855abc2319a098348c292fc68715f5b8648356c` | 768 |
| `prototype/conformance/cases/F09-d/expected.json` | `039a95aef490af3d6f15ec3b581590473384b5c8` | 761 |
| `prototype/conformance/cases/F09-e/expected.json` | `9b609cff6c061f3094a1c9e9a3c2fb150c8604e4` | 768 |
| `prototype/conformance/cases/F09-f/expected.json` | `c59d3773975b8833ac00ecda76555c4d88b07595` | 791 |
| `prototype/conformance/cases/F09-g/expected.json` | `d3c61d6477f299f19f1cf23390e0aa5644a48073` | 756 |
| `prototype/conformance/cases/F09-h/expected.json` | `2618ff88f7ca3d9667e33aa132a99d2d3be79451` | 784 |
| `prototype/conformance/cases/F09-i/expected.json` | `fb64197866359eb49f3235f0c0f9ceccd337ca32` | 741 |
| `prototype/conformance/cases/F10-a/expected.json` | `34bf446c997e6d7094199bbfa9cc9e941f415b0f` | 767 |
| `prototype/conformance/cases/F10-b/expected.json` | `005eeff3f5afa2e0b372e65e2ce7715643f19815` | 751 |
| `prototype/conformance/cases/F10-c/expected.json` | `2f2ea732216ecb94f5494ea593cde88b0911c1e9` | 795 |
| `prototype/conformance/cases/F10-d/expected.json` | `2f3aeb25f28a2bf27783280fbc01429ce89a400b` | 751 |
| `prototype/conformance/cases/F10-e/expected.json` | `f468a4582335a2766345a24d58f839f9f0989d16` | 763 |
| `prototype/conformance/cases/F10-f/expected.json` | `763d1b9455b69fd3d8dd8da118b4421d361e5361` | 792 |
| `prototype/conformance/cases/F10-g/expected.json` | `25a80fb23050cab296d3b3115cacfa20e8dd15c8` | 836 |
| `prototype/conformance/cases/F12-a/expected.json` | `d1e6cbb41db5936383b0f6dd4bedd5c3ec0af000` | 849 |
| `prototype/conformance/cases/F12-b/expected.json` | `37379557f7a02e8c8611fc50b8a179a9004a612f` | 865 |
| `prototype/conformance/cases/F15-a/expected.json` | `62ef1eb6b310b9d97e3a16029c4b566ddff6d13b` | 812 |
| `prototype/conformance/cases/F15-b/expected.json` | `0316706763ef790477a9e0a90b6ec9dcd8e00175` | 876 |
| `prototype/conformance/cases/GIT-path-a/expected.json` | `54b16e16fd2875a711a7292361e6bf4dbd342969` | 755 |
| `prototype/conformance/cases/GIT-path-b/expected.json` | `f0d4db27c891bb550d162d1de7ca757351033e80` | 765 |
| `prototype/conformance/cases/GIT-path-c/expected.json` | `68056c0fe78d8d1168343f022884278b25a11641` | 818 |
| `prototype/conformance/cases/GIT-path-d/expected.json` | `5bd11b721e011d43368d889b6bb51cfcb98f42c9` | 775 |
| `prototype/conformance/cases/GIT-pending/expected.json` | `8f58b2d3ec519a08b68c1606e76f1f2405a8bf18` | 759 |
| `prototype/conformance/cases/GIT-prefix/expected.json` | `dfd854dcc57d7ebdc3432ac7759673b65bb9345b` | 831 |
| `prototype/conformance/cases/GIT-shape/expected.json` | `ddb7b8f11921138f2ce4584a54d23b7a12de5a85` | 813 |
| `prototype/conformance/cases/GIT-stamp/expected.json` | `5dfeae9e92c38f3ac9fb3012e07b82ea14c3fc15` | 820 |
| `prototype/conformance/cases/HY-N1/expected.json` | `7a6cf3c1341ea7544d5c58a18d8fd8a1f6c3fcca` | 1041 |
| `prototype/conformance/cases/HY-N2/expected.json` | `a853cc47e64b26839d9cd6625f1641568ec7ff8d` | 915 |
| `prototype/conformance/cases/HY-N3/expected.json` | `1fa8ce48382ac6886eb6998463ba3cea2d64d0cc` | 871 |
| `prototype/conformance/cases/HY-N4/expected.json` | `4aceb98e4aca48fca990f2c8b84324bcdc921128` | 905 |
| `prototype/conformance/cases/HY-N5/expected.json` | `e8e339fbfe9d1cdb7dc81d397173b393d75620ad` | 905 |
| `prototype/conformance/cases/HY-N6/expected.json` | `5cae7da77689757eb213ede9c1cac6511a8a9081` | 948 |
| `prototype/conformance/cases/HY-V1/expected.json` | `ca831f251d33e46cefacf620d671b08918f5f5fe` | 1396 |
| `prototype/conformance/cases/HY-V2/expected.json` | `37168c35de8209476e1dab60352a05e033f6f634` | 1218 |
| `prototype/conformance/cases/HY-a1-C/expected.json` | `cf7fb638cd5865e3340298d5db38a72c3db23f6a` | 1490 |
| `prototype/conformance/cases/HY-a2-C/expected.json` | `30438a80b5db1f0668c8035e42e8281f80056fe5` | 1081 |
| `prototype/conformance/cases/HY-a3-C/expected.json` | `42217f1d9937fb8abe5b79f0c4ee9559f924e0a1` | 1087 |
| `prototype/conformance/cases/HY-a4-C/expected.json` | `98f7d98b7b4c7ffcd009020593d1bef06ab2953e` | 981 |
| `prototype/conformance/cases/HY-a5-C/expected.json` | `ffb19a26d332218da7dd29514024a7fac32071f5` | 944 |
| `prototype/conformance/cases/HY-ak-C/expected.json` | `5be3ec0baf2710371a740000f361b2a8e70fef58` | 1641 |
| `prototype/conformance/cases/HY-b1-H/expected.json` | `b955579de22e28cc161b044a7516514389bbe511` | 1486 |
| `prototype/conformance/cases/HY-b2-H/expected.json` | `5046e4371b28140e796f0616ff42864081200ccd` | 1500 |
| `prototype/conformance/cases/HY-c1-C/expected.json` | `33e9bf602ecb3425ca43797d93bbbe45f1976cd3` | 1189 |
| `prototype/conformance/cases/HY-c1-H/expected.json` | `bb2efc40f94b416a661aee1588602cf60f6e46b6` | 1183 |
| `prototype/conformance/cases/HY-c2-C/expected.json` | `f67a257a8583639a377c8a6cd5a093fbd46847d6` | 1166 |
| `prototype/conformance/cases/HY-c2-H/expected.json` | `e8987fb8128e5f2a01eb3c4fe6059a6ed1ac80bf` | 1160 |
| `prototype/conformance/cases/HY-c3-C/expected.json` | `375033ceb9eecb293b78e6a445a12de751a76562` | 1198 |
| `prototype/conformance/cases/HY-c3-H/expected.json` | `7429d39f3e016e543afbc6014cfe2e03b2f59a7d` | 1192 |
| `prototype/conformance/cases/HY-c4-C/expected.json` | `d8eb2f806ea89754f878c2aa5859eefed1b3c154` | 1160 |
| `prototype/conformance/cases/HY-c4-H/expected.json` | `16fc530258aad04d8197e6210ba7e870158f26e6` | 1154 |
| `prototype/conformance/cases/HY-d1-C/expected.json` | `719cecbc6833ee436d12bf7f48b1b9d790ce906d` | 1209 |
| `prototype/conformance/cases/HY-d1-H/expected.json` | `9d029c0b623327010f3f561098928ade580836ff` | 1203 |
| `prototype/conformance/cases/HY-d2-C/expected.json` | `5c953ba2c795bebc59b938e9b5a69e00c1a7d214` | 1155 |
| `prototype/conformance/cases/HY-d2-H/expected.json` | `a8b9730e480f8e1a015017dd68bca45c83ddcf81` | 1149 |
| `prototype/conformance/cases/HY-e1-C/expected.json` | `fca5fc0268da28fd6e39139eb074cea60bdfe703` | 1276 |
| `prototype/conformance/cases/HY-e1-H/expected.json` | `58bb806fc5e438a0fe4be102828bb889296d9d9a` | 1270 |
| `prototype/conformance/cases/HY-e2-C/expected.json` | `1b9ad04659cc7a4058a013ab9f345fcab2301030` | 1079 |
| `prototype/conformance/cases/HY-e2-H/expected.json` | `e83f0286ba67c00c6c108b20fbeb137fc72e2815` | 1073 |
| `prototype/conformance/cases/HY-e3-C/expected.json` | `35f6fc2548d4c143e5d105083a6f43692a2f3bc1` | 950 |
| `prototype/conformance/cases/HY-e3-H/expected.json` | `70eeeafaf2374ac123467a0608a42d966a4e19fd` | 944 |
| `prototype/conformance/cases/KEY-a/expected.json` | `558be3f5cafec310c41b5fb1207030e328672c0d` | 756 |
| `prototype/conformance/cases/KEY-b/expected.json` | `0661fd9ca537e72826b7d630d7fe50091240989f` | 746 |
| `prototype/conformance/cases/KEY-c/expected.json` | `250dd26d4de585df9842826409f220f8e09b1430` | 754 |
| `prototype/conformance/cases/KEY-d/expected.json` | `e16e2126eb337ae709d9b145934b2227bfe4add8` | 798 |
| `prototype/conformance/cases/L-01/expected.json` | `61a9e4029590d96431dc062af0b2b59ef5fa17be` | 538 |
| `prototype/conformance/cases/L-01b/expected.json` | `d164f0c787aa616cca663fec1a91e543422023cd` | 502 |
| `prototype/conformance/cases/L-01c/expected.json` | `008b817d742741247d40375bd07a5d6b9f8fa440` | 491 |
| `prototype/conformance/cases/L-01d/expected.json` | `342ccbde546ec402ece4a3ce6dc4fe21fa907b05` | 476 |
| `prototype/conformance/cases/L-02/base.json` | `ffd12db84cfb09c6b2a60f9a392bd8a924b53c8e` | 15379 |
| `prototype/conformance/cases/L-02/bundle.recipe.json` | `ae2423b92f22634a8420f6167c8eae44d55f675b` | 52 |
| `prototype/conformance/cases/L-02/expected.json` | `d5c9eaef1d69ebe94b70d89d15780be232f1294c` | 568 |
| `prototype/conformance/cases/L-02b/base.json` | `ffd12db84cfb09c6b2a60f9a392bd8a924b53c8e` | 15379 |
| `prototype/conformance/cases/L-02b/bundle.recipe.json` | `16abebc6dfd33ed707130bb7b9a86a6fd6b7b33d` | 52 |
| `prototype/conformance/cases/L-02b/expected.json` | `fc445449943bcfbe3b29a3599d87d0dfe1857293` | 650 |
| `prototype/conformance/cases/L-03/expected.json` | `8403d68e8abdf8e7975a62ac6be29b4e9432c088` | 762 |
| `prototype/conformance/cases/L-03b/expected.json` | `100e34d7fb1dce2887ae638d3d3a5ca64bf54595` | 771 |
| `prototype/conformance/cases/L-04/expected.json` | `0f2684e8ece4955d4a479c93101baaae45fe42ee` | 822 |
| `prototype/conformance/cases/L-04b/expected.json` | `87ae07c56cc2093390b8c27f1e55d646cf5bf65e` | 733 |
| `prototype/conformance/cases/L-05/expected.json` | `1eb391f4c31c53a8d1427f6ca6d2886889491b32` | 920 |
| `prototype/conformance/cases/L-06/expected.json` | `f625806264ca0abc562c5c9894ea87e0f22a3eb4` | 965 |
| `prototype/conformance/cases/L-06/request.txt` | `93279fe183c3c5dbe7ac7202afb09983bfd08c13` | 9 |
| `prototype/conformance/cases/L-06s/expected.json` | `2fe8fe51cd2d450176bacabcff6b1fcb30e1544f` | 786 |
| `prototype/conformance/cases/L-07/expected.json` | `f91162a4560f12cae750b0744efd0ea7d1dc93a2` | 875 |
| `prototype/conformance/cases/L-08/expected.json` | `0ff90291bfc60855c6814042a8873bd2076c172c` | 791 |
| `prototype/conformance/cases/L-09/expected.json` | `8dab8b38dd0b26480432d41e5d2d504f5aa30e6b` | 883 |
| `prototype/conformance/cases/L-10/expected.json` | `47ac40580abcd6a83626206c5ef4e154126b1a05` | 799 |
| `prototype/conformance/cases/L-100/expected.json` | `572bfb465088efc2b20d632bccb93f6e3713881c` | 775 |
| `prototype/conformance/cases/L-101/expected.json` | `18e68f99541dddc0b122ea32a76c8dec78a6bbe2` | 762 |
| `prototype/conformance/cases/L-102a/expected.json` | `c020a909545b78a27cdab30d4a9a5daf16b1dd6a` | 768 |
| `prototype/conformance/cases/L-102b/expected.json` | `f3b5f9a77e898ad6b3b1eb30ac21679b91274677` | 768 |
| `prototype/conformance/cases/L-103/expected.json` | `a7d533f0ea4eaa8472c463f0521a280f5e52a308` | 750 |
| `prototype/conformance/cases/L-104a/expected.json` | `501daa0dadd54341c9872cf3a22dba1df7627cd6` | 827 |
| `prototype/conformance/cases/L-104b/expected.json` | `8c56cf78f3a444f31d71efb933dddfb0de50eea5` | 792 |
| `prototype/conformance/cases/L-104c/expected.json` | `e2d02f8b7210f8203fee0ae2a0da8e1813ac18f1` | 841 |
| `prototype/conformance/cases/L-104d/expected.json` | `5296a10395e488dbb6b09fd78d2b1f98ffac8ebf` | 796 |
| `prototype/conformance/cases/L-105/expected.json` | `e9a338ee6598fb055ec2d57840f5a75c93c0d807` | 871 |
| `prototype/conformance/cases/L-106/expected.json` | `c00f4825251a02198d78a62150a9d665a320325e` | 804 |
| `prototype/conformance/cases/L-107/expected.json` | `86a60148bd20012a1745b75b61301d28b74e4f8f` | 832 |
| `prototype/conformance/cases/L-108/expected.json` | `a7cb52bb6061e8e12590b724a980f9cd84563ec5` | 815 |
| `prototype/conformance/cases/L-109/expected.json` | `342aeee94ed235d09739d208e61087765cd12012` | 787 |
| `prototype/conformance/cases/L-11/expected.json` | `0abc5db2c2cd2591842a4e3943b05d3965b6c076` | 821 |
| `prototype/conformance/cases/L-110a/expected.json` | `db8714e9f2775ce15d4f7d5bbd3c9d0961cdd14a` | 780 |
| `prototype/conformance/cases/L-110b/expected.json` | `60e58a1395513a2444f1f210960229c27c12b351` | 858 |
| `prototype/conformance/cases/L-110c/expected.json` | `86f601bb35064c2f7f3c5fba765e48c317068fcc` | 827 |
| `prototype/conformance/cases/L-110d/expected.json` | `390360c118ffe4712d1b6a20723b6493d5b7f949` | 815 |
| `prototype/conformance/cases/L-111a/expected.json` | `4b28a0ae890adb1ee58e094e5ad68895a7e2e404` | 836 |
| `prototype/conformance/cases/L-111b/expected.json` | `477a53bdb9773a2ba7744e0bc289ace7da4c10a7` | 767 |
| `prototype/conformance/cases/L-111c/expected.json` | `244bb559c2c307c38b1304a488bdb350c46af6f3` | 853 |
| `prototype/conformance/cases/L-12/expected.json` | `abff930b6bf9cb510643bd7c89d1ac656ba87b21` | 822 |
| `prototype/conformance/cases/L-13/expected.json` | `66b748187212491bdc0be85e485a89edb0f6864b` | 1088 |
| `prototype/conformance/cases/L-14/expected.json` | `3e46ec8232f983c1a424222d9ed46914c2c11e85` | 893 |
| `prototype/conformance/cases/L-15/expected.json` | `e4ab050c8fade911da108bf70567a108b54a8e92` | 824 |
| `prototype/conformance/cases/L-16/expected.json` | `33ccc5730127d40d0abb07912d301398d52ca403` | 822 |
| `prototype/conformance/cases/L-18/expected.json` | `310a440c377d56187761c4615c350e6f7372469d` | 798 |
| `prototype/conformance/cases/L-19/expected.json` | `5a36f4cdef01e459b5d2e6d0c91e4199ea9419f0` | 780 |
| `prototype/conformance/cases/L-20/expected.json` | `9c2926de7ad71e4fce3d8e65da0cbb9301e1199c` | 817 |
| `prototype/conformance/cases/L-21/expected.json` | `21b559cb5205e5e66ddeef69998e7a37a47b406d` | 1038 |
| `prototype/conformance/cases/L-22/expected.json` | `db80b442f48a151157080051efca5762682ba536` | 759 |
| `prototype/conformance/cases/L-23/expected.json` | `137667a09f0dbc552a23890405f3bec1fdd41bb3` | 915 |
| `prototype/conformance/cases/L-24/expected.json` | `2f2f3ad72b52c35cdd1b4e993bd79ef433c3dd8b` | 821 |
| `prototype/conformance/cases/L-24b/expected.json` | `2eedc04d79bea158119cda61a8339d7112325159` | 785 |
| `prototype/conformance/cases/L-25/expected.json` | `9693fc81f93d17f7c7300db7b13ca9361af89670` | 786 |
| `prototype/conformance/cases/L-25b/expected.json` | `2d93daa46e63309f40c04a95927f8dc06a6b7dee` | 823 |
| `prototype/conformance/cases/L-25c/expected.json` | `d14b02a1473458ba727c97b7792b55d68cf9aa1a` | 777 |
| `prototype/conformance/cases/L-26/expected.json` | `64876a2b62f87a286c3c218a275cf73acedeb124` | 832 |
| `prototype/conformance/cases/L-26b/expected.json` | `39285d209d620159ff331242c4d2c2451a3a85b4` | 805 |
| `prototype/conformance/cases/L-27/expected.json` | `18454dee8355e99306e67124d90341d3cc232b04` | 841 |
| `prototype/conformance/cases/L-28/expected.json` | `c832a4f5ce972d4b33cb15688bfecbc9f9a4e0b1` | 805 |
| `prototype/conformance/cases/L-29/expected.json` | `615d08e6e8eff2391d3ab782e06c94fa6f965f84` | 800 |
| `prototype/conformance/cases/L-30/expected.json` | `ce4ab3c14a27559891a9bd96fa199af8a6d6cd1f` | 791 |
| `prototype/conformance/cases/L-31/expected.json` | `8c394bfdb996a8c30f7b466419b9b9e0ab5bf707` | 839 |
| `prototype/conformance/cases/L-32/expected.json` | `c153932931b3235eb4a086a6d07d71a31b34ac66` | 908 |
| `prototype/conformance/cases/L-32r/expected.json` | `4de0f4aeebfa5b5aecccda27c7a5f5de06228def` | 829 |
| `prototype/conformance/cases/L-33/expected.json` | `18d8427f991609f07aa80da0d6466210e5025b29` | 851 |
| `prototype/conformance/cases/L-33r/expected.json` | `d8c5c3ef193961f6807c1759d7b0c80f5a1d0608` | 768 |
| `prototype/conformance/cases/L-34/expected.json` | `a0018b942e39bc08bd671359562fdf291fa38be5` | 845 |
| `prototype/conformance/cases/L-34r/expected.json` | `38f32070fd52675aebb3241fe27c470da5d021ea` | 759 |
| `prototype/conformance/cases/L-35/expected.json` | `809bea8a3d8a07539108d83d8539fb7938d988ca` | 781 |
| `prototype/conformance/cases/L-36/expected.json` | `a40893baf792b1bfc6540a6e0d561207546de85c` | 759 |
| `prototype/conformance/cases/L-36b/expected.json` | `ac05de82f16dc943da0ab39d26da28c99b570e30` | 771 |
| `prototype/conformance/cases/L-37/expected.json` | `c37f7852fb31d2962952eb5abdbc29a6c25c5251` | 809 |
| `prototype/conformance/cases/L-38/expected.json` | `f90760bf4d1fd968a5ddd7707a3ff72819d6684e` | 767 |
| `prototype/conformance/cases/L-39/expected.json` | `1086c913597e8280222fb9e2f619284f9aa60008` | 820 |
| `prototype/conformance/cases/L-40/expected.json` | `ee7c4a57637ca7b0146dbdc5a352fe1216ce26aa` | 883 |
| `prototype/conformance/cases/L-41/expected.json` | `426067cfaf71785d0221c6385bca94b8905f38d6` | 838 |
| `prototype/conformance/cases/L-42/expected.json` | `3cda1dcd6406876b9cc8a90d76e45edc25e0b4f5` | 866 |
| `prototype/conformance/cases/L-43/expected.json` | `1e8bebe936ce7c65b32dcebdba718ade08a0f687` | 625 |
| `prototype/conformance/cases/L-43b/expected.json` | `c5fad90794b8f93ea1eaebf7d87e224c40d9226e` | 620 |
| `prototype/conformance/cases/L-44/expected.json` | `aa0e740eaa5c40b8a803fc757e35822ab63d1ec9` | 810 |
| `prototype/conformance/cases/L-45/expected.json` | `9351fdcd0aa7deda1dba01f7c400f2a9eca678f3` | 785 |
| `prototype/conformance/cases/L-46/expected.json` | `ae109fa46ba5b5b4c5089ec32ca3da0afda097b4` | 822 |
| `prototype/conformance/cases/L-47/expected.json` | `3f3eb078e9144f7e27e78943f09fe0a09509b746` | 802 |
| `prototype/conformance/cases/L-48/expected.json` | `39ed1aa5363c6b0da4cd21dc50488d6f1f64c680` | 786 |
| `prototype/conformance/cases/L-49/expected.json` | `58c729747b3716a176ddbb14e50af3e9600888eb` | 780 |
| `prototype/conformance/cases/L-50/expected.json` | `4b9b06b1b9c79d94db003ad9e0051858f20a9be8` | 323 |
| `prototype/conformance/cases/L-50b/expected.json` | `19f49c565e79eb5e5adf635b146a9e977339637e` | 349 |
| `prototype/conformance/cases/L-50c/expected.json` | `61041d9fc93fee5102bf31c3d36b1ec2916e18c6` | 339 |
| `prototype/conformance/cases/L-50d/expected.json` | `d2523eca7b62bf5adae5d10d828e05198f8d2c84` | 306 |
| `prototype/conformance/cases/L-51/expected.json` | `d059e25205d84a191bf10e4e9140774307b71586` | 574 |
| `prototype/conformance/cases/L-52a/expected.json` | `8490dd5232eaec48516fbaa3bdfd66acea12bb1d` | 319 |
| `prototype/conformance/cases/L-52b/expected.json` | `bf5f941db8e7120ec536933e2194d0b7c8f8bd9c` | 310 |
| `prototype/conformance/cases/L-53/expected.json` | `6923b9b4ef633b2304a474aab2c070a0186d0a13` | 313 |
| `prototype/conformance/cases/L-53/next.json` | `1a4f4be644a837c77f702ec03e0a6b27c14432aa` | 4567 |
| `prototype/conformance/cases/L-53/previous.json` | `18db26f27d91d70206cc3f81cd728628c2c850a9` | 4567 |
| `prototype/conformance/cases/L-54/expected.json` | `afa2245561e48f2ec05e3a4ffb601089a0554e8c` | 348 |
| `prototype/conformance/cases/L-54/next.json` | `822835a00ddf94c79ca723a119c9f64c845e8b58` | 4585 |
| `prototype/conformance/cases/L-54/previous.json` | `18db26f27d91d70206cc3f81cd728628c2c850a9` | 4567 |
| `prototype/conformance/cases/L-54b/expected.json` | `a66adca03016ad4a92ed8fafa278bc3d1a15e948` | 319 |
| `prototype/conformance/cases/L-54b/next.json` | `9e4e02cbe7f63160fbab085b5fdc3e861a25073e` | 4585 |
| `prototype/conformance/cases/L-54b/previous.json` | `18db26f27d91d70206cc3f81cd728628c2c850a9` | 4567 |
| `prototype/conformance/cases/L-54c/expected.json` | `7ec27cfc832cea28af63544ebade1a40646b4804` | 307 |
| `prototype/conformance/cases/L-54c/next.json` | `971843b756c5a523ee1205bf0505e01c316ee0ed` | 4585 |
| `prototype/conformance/cases/L-54c/previous.json` | `18db26f27d91d70206cc3f81cd728628c2c850a9` | 4567 |
| `prototype/conformance/cases/L-55a/expected.json` | `1d94763afe99e841e53a6b19b7ba931f345bc73a` | 281 |
| `prototype/conformance/cases/L-55a/next.json` | `9bbeb97119a71e55f0ea5d4ed15a6aa77162ad5e` | 4567 |
| `prototype/conformance/cases/L-55a/previous.json` | `18db26f27d91d70206cc3f81cd728628c2c850a9` | 4567 |
| `prototype/conformance/cases/L-55b/expected.json` | `b6c40d28596f1a0635839ad4e8a9034fa0d1babd` | 300 |
| `prototype/conformance/cases/L-55b/next.json` | `08d7f310bca4a261017646e71f7ffc4eb8f13de6` | 4567 |
| `prototype/conformance/cases/L-55b/previous.json` | `18db26f27d91d70206cc3f81cd728628c2c850a9` | 4567 |
| `prototype/conformance/cases/L-55c/expected.json` | `59e63478da60ef64849a2ae5f32a6bd7aaf62f65` | 285 |
| `prototype/conformance/cases/L-55c/next.json` | `5850b1fc91f36e73d09578bc97e0b271c6b68fd8` | 3735 |
| `prototype/conformance/cases/L-55c/previous.json` | `18db26f27d91d70206cc3f81cd728628c2c850a9` | 4567 |
| `prototype/conformance/cases/L-56a/expected.json` | `140d1906683885f500e492c5ba5856fc2e0d61e5` | 896 |
| `prototype/conformance/cases/L-56b/expected.json` | `990fa10c4174b995858d13153d206abce2fd357d` | 838 |
| `prototype/conformance/cases/L-56c/expected.json` | `e08f91f4d58297b4ff659dd03fa4d83d23b1db21` | 299 |
| `prototype/conformance/cases/L-56c/next.json` | `d9dbf30810f79ada5583cd497d490b158f831980` | 4643 |
| `prototype/conformance/cases/L-56c/previous.json` | `18db26f27d91d70206cc3f81cd728628c2c850a9` | 4567 |
| `prototype/conformance/cases/L-57/expected.json` | `51a25ff088aff194dc257f60e739e7aa5c2f24b1` | 841 |
| `prototype/conformance/cases/L-57b/expected.json` | `8a4a69f568add93c447902360cd5dcd910bce13f` | 823 |
| `prototype/conformance/cases/L-57c/expected.json` | `90a768be1843f464bc3502a26ac404a1a38b149a` | 839 |
| `prototype/conformance/cases/L-58/expected.json` | `d6d372ce333ec8fbe99894d666cdf9f92f8191d9` | 912 |
| `prototype/conformance/cases/L-59/expected.json` | `ab0ff49feb7f3bcb19d076029868593aa1ce35ec` | 828 |
| `prototype/conformance/cases/L-60/expected.json` | `54be7ed0dbe98eb404ce843a1bb12c4e5b62796b` | 826 |
| `prototype/conformance/cases/L-61a/expected.json` | `3da9f49d7b4256084dafab6b8f99c001f9200135` | 894 |
| `prototype/conformance/cases/L-61b/expected.json` | `b583baa616b3510375841e13ad61dc47e6daf099` | 892 |
| `prototype/conformance/cases/L-62a/expected.json` | `c27f64753903aa2cdf7ff5095089b65ec8518dfb` | 852 |
| `prototype/conformance/cases/L-62b/expected.json` | `dd104294e9caf12808761ec7e8ca4e149e2a5eae` | 973 |
| `prototype/conformance/cases/L-63/expected.json` | `312257db8fe2e249883410844b93bc6a30bd9bc0` | 844 |
| `prototype/conformance/cases/L-64/expected.json` | `41b582dc4c485fa28a2d142736d5168e7eefebc3` | 791 |
| `prototype/conformance/cases/L-65/expected.json` | `b24e13785adba2f6be60174ed561f8d390b2d4f6` | 759 |
| `prototype/conformance/cases/L-66/expected.json` | `578ce24798e9694f5023b18da0fe43424642e0aa` | 879 |
| `prototype/conformance/cases/L-67/expected.json` | `1d5f6a2f0411ed8f92d6eb9b32f136456e3cc57a` | 808 |
| `prototype/conformance/cases/L-68/expected.json` | `5869148c2d23362f09af930c6053914c83597fed` | 810 |
| `prototype/conformance/cases/L-68b/expected.json` | `ccd9fb98ebd6e1fc824c01ae2f5477badb4a0dbe` | 765 |
| `prototype/conformance/cases/L-69/expected.json` | `a828ed073a46e3a1658fd5179f2a97dc09b01025` | 784 |
| `prototype/conformance/cases/L-70/expected.json` | `237ed0c8367d44f7db1ef3a234f4479e882c996f` | 830 |
| `prototype/conformance/cases/L-70b/expected.json` | `bc2cd10b7c8c4981dde6483c7b77af240eefabb3` | 980 |
| `prototype/conformance/cases/L-71a/expected.json` | `e6b62eda9c2be9c16de33d1e9c1e003795b6f331` | 789 |
| `prototype/conformance/cases/L-71b/expected.json` | `833c523d5614f5174c3b7cff3c8903633d78f251` | 807 |
| `prototype/conformance/cases/L-72/expected.json` | `086410aafb50017f219a353adf79ec481264accb` | 827 |
| `prototype/conformance/cases/L-73a/expected.json` | `579466c21f2dc70c4caac0666d3a58738b5592c6` | 777 |
| `prototype/conformance/cases/L-73b/expected.json` | `bdc70148259af57b6c252f7562949985c01c8202` | 773 |
| `prototype/conformance/cases/L-73c/expected.json` | `73fa6e817c5a9427a1139625cc5a646e9b079dde` | 799 |
| `prototype/conformance/cases/L-73d/expected.json` | `c1aaadb21e524bf72c0d9a6adbcf9ab682e87ff0` | 799 |
| `prototype/conformance/cases/L-74/expected.json` | `f22e79ce0b896b2244710ba8eddf23824ee4bca1` | 816 |
| `prototype/conformance/cases/L-74e/expected.json` | `60f0651431f4ad5652cadc7b5610fa893f039990` | 1114 |
| `prototype/conformance/cases/L-74l/expected.json` | `cd710e9c65209a73de3cb9c95b0bb1ed81b360f1` | 1114 |
| `prototype/conformance/cases/L-74v/expected.json` | `8c774b75b0ea7f3376d801922bdb5ae1fa859d1a` | 1109 |
| `prototype/conformance/cases/L-75/expected.json` | `7306a0654e571a8e192b995f834dbab0ad5a0253` | 802 |
| `prototype/conformance/cases/L-76/expected.json` | `5838895988ee30c371c5e9a447cbc8dbe932c4a5` | 835 |
| `prototype/conformance/cases/L-77/expected.json` | `7500741334458b3b87a116c9a6cf985b0c397dec` | 836 |
| `prototype/conformance/cases/L-78/expected.json` | `5989149321f1c261cb6db88a8f813c0c9e5aaa14` | 815 |
| `prototype/conformance/cases/L-79/expected.json` | `019e8897c9f8ed7dd4ffc3093248247d3351d0bf` | 778 |
| `prototype/conformance/cases/L-80/expected.json` | `514dbc19a63788485ce99faf4aaca15734c41fb1` | 769 |
| `prototype/conformance/cases/L-81/expected.json` | `0882e67237402d9d7883614f8ff25e2605005a0d` | 777 |
| `prototype/conformance/cases/L-82/expected.json` | `5853346aa6afb5b328345ca7302597eeeadb5d6b` | 842 |
| `prototype/conformance/cases/L-83/expected.json` | `bb4726c81e00c503b0f59c6811d68d1b8f6db9e3` | 809 |
| `prototype/conformance/cases/L-84/expected.json` | `c7c5fe24d850839c4bbe2f4f86acf9053db74bf5` | 881 |
| `prototype/conformance/cases/L-85/expected.json` | `496dfb71c4d26eae0dbc2f7e59fc9aa0c6830717` | 784 |
| `prototype/conformance/cases/L-86/expected.json` | `081627da17d26336137f632f688ac4a1f6575eae` | 799 |
| `prototype/conformance/cases/L-87a/expected.json` | `c334b4dae8b29e7c5c7c5697a1e1a978c2e156c7` | 738 |
| `prototype/conformance/cases/L-87b/expected.json` | `df83e882aa5df0df0e9d258a5ed919e56bd5378c` | 743 |
| `prototype/conformance/cases/L-87c/expected.json` | `081189e382f29c3711ec54f302ebcb91ae6e8184` | 734 |
| `prototype/conformance/cases/L-87d/expected.json` | `17b79beb202051eaea39c50ba8bf41469b7e1b75` | 778 |
| `prototype/conformance/cases/L-87e/expected.json` | `90dbdcba8e640274ab9c6b2fa87181b3cbb06031` | 845 |
| `prototype/conformance/cases/L-88/expected.json` | `bcb2f7f03f61d9590f1d4d037dc6ba9041df0cfb` | 898 |
| `prototype/conformance/cases/L-89/expected.json` | `a74b0eaa9dbfa4688fe084481f0102f1ab9da435` | 757 |
| `prototype/conformance/cases/L-90/expected.json` | `fd8ab8c1f7c1c00f87a4b66614cfbf9e0944fb11` | 760 |
| `prototype/conformance/cases/L-91a/expected.json` | `aff095d80327f7f0f06a2a5dd565fdd7bb2cb5af` | 761 |
| `prototype/conformance/cases/L-91b/expected.json` | `3968fde84407f464d13c327161254ad36ce7d7ee` | 761 |
| `prototype/conformance/cases/L-91c/expected.json` | `4a2a4117ceb7e30747b3b9655c041be890a92e25` | 765 |
| `prototype/conformance/cases/L-91d/expected.json` | `e0b1e4d932d7f489062658774651d07d73ded8b4` | 746 |
| `prototype/conformance/cases/L-92a/expected.json` | `f17a5a00e76fdac0484eb1555a635f7c7b918f3a` | 753 |
| `prototype/conformance/cases/L-92b/expected.json` | `d061fce88461504502fbc4e98c2504b20acd1e53` | 770 |
| `prototype/conformance/cases/L-92c/expected.json` | `4d6696ee04fb6a5b0612fed5c1ab50fbc0fb941d` | 773 |
| `prototype/conformance/cases/L-92d/expected.json` | `0cbe97cd61587c67bc35675875a3dbd4b4209bb9` | 754 |
| `prototype/conformance/cases/L-92e/expected.json` | `adec275fa41c66a8895934818e5e10b1fc45df91` | 770 |
| `prototype/conformance/cases/L-92f/expected.json` | `56ef9458de5d7d9230639acb2a94e4dc82d0472c` | 809 |
| `prototype/conformance/cases/L-92g/expected.json` | `a5bfc31e670e1815c7ef75a1998db122fb2a5ce7` | 826 |
| `prototype/conformance/cases/L-93a/expected.json` | `12151fb1abe1f16e240395425673b0eefaed253f` | 768 |
| `prototype/conformance/cases/L-93b/expected.json` | `70b3dc8c52bdd3702a0c14948d1a2c15b8c40bf8` | 763 |
| `prototype/conformance/cases/L-95/expected.json` | `95714617acc30fb498bd4e56f8d9fd70328df490` | 810 |
| `prototype/conformance/cases/L-96/expected.json` | `4d177857651c3ca2bd5cf524a1e8809521be20fc` | 806 |
| `prototype/conformance/cases/L-97/expected.json` | `657147806901b9a7c1e145ef25be6ab641fe732d` | 780 |
| `prototype/conformance/cases/L-98/expected.json` | `3f2caa4707a6e7e3fd3decae033fe6005cda3a47` | 797 |
| `prototype/conformance/cases/L-99/expected.json` | `f62e6ab5a8f01f83e03f5a3088b5d79fb36f535a` | 784 |
| `prototype/conformance/cases/POS-a/expected.json` | `ef440edd5ae05daa5048bcf9724f68bb1513c12a` | 785 |
| `prototype/conformance/cases/POS-b/expected.json` | `958e3d5fb8d1c78ed13136d70ef35213cbb826c2` | 774 |
| `prototype/conformance/cases/POS-c/expected.json` | `b989727f40cc7d312019dd752269cf45e2365636` | 789 |
| `prototype/conformance/cases/RC-a/expected.json` | `c4acdf95a3f4f7a314b288cd05de852c9e5f4d28` | 824 |
| `prototype/conformance/cases/RC-b/expected.json` | `7f7d4ea9f1df73e7bd9191a2e61fc986308cb4a7` | 780 |
| `prototype/conformance/cases/RC-c/expected.json` | `4185be76c7e52f1963f5f1844f4a54986399bba7` | 799 |
| `prototype/conformance/cases/RC-d/expected.json` | `81380a038f80e786c6ff721482d54733cfc3fafa` | 782 |
| `prototype/conformance/cases/SIG-newhdr/expected.json` | `c1d63e9b17ca60c02c6c079a56e0f123b20d34b0` | 805 |
| `prototype/conformance/cases/SIG-type1/expected.json` | `d2b61143ffd47b6cf9b0548d847adf0ccdb249ce` | 778 |
| `prototype/conformance/cases/SNAP-c1/expected.json` | `f92974dc4350c8c849a0a4f0e1aeffe80eb5a23a` | 775 |
| `prototype/conformance/cases/SNAP-c1b/expected.json` | `a85f86f958152ab74bc4c75c4a2c4714e750cf7c` | 757 |
| `prototype/conformance/cases/SNAP-c2/expected.json` | `cb58e5f073af5261f9d7675f762f48f7bbf508f5` | 777 |
| `prototype/conformance/cases/SNAP-otsfmt/expected.json` | `acffd1c6618126c91e416f65214833b3becba25d` | 799 |
| `prototype/conformance/cases/SNAP-pending/expected.json` | `8d1f1423a85ae632a7c6b98dfe32c1a155584a9b` | 737 |
| `prototype/conformance/cases/SNAP-shape/expected.json` | `8e46d9cfe5587ab2e374732483324c869b8d9cc9` | 849 |
| `prototype/conformance/cases/SNAP-stamp/expected.json` | `e7c156f69f4e9b50f72d73464adefe26afae1fec` | 811 |
| `prototype/conformance/cases/UTC-01/expected.json` | `4e618fc5065dbb68b8cb9984e814ccdc555c7163` | 944 |
| `prototype/conformance/cases/UTC-02/expected.json` | `b3d5d3b9543bf25202b510bb7b255bdfe12952a1` | 957 |
| `prototype/conformance/cases/UTC-03/expected.json` | `5556e55b550c59bd0dba0f2f5f75ac917a1f84fb` | 982 |
| `prototype/conformance/cases/UTC-04/expected.json` | `56ee6a315b0e504e34b0a379b4a3ae5eba99da45` | 1034 |
| `prototype/conformance/cases/UTC-05/expected.json` | `725ad0dbb5af0cbf4b17e7cd83509ab232554301` | 1027 |
| `prototype/conformance/cases/UTC-06/expected.json` | `54f1d43cecf6fa7c2bb87fae5f4893c549f7802e` | 1022 |
| `prototype/conformance/cases/UTC-07/expected.json` | `07f2d09bc8f15cc45af74efbe4adbe2caa8d1958` | 980 |
| `prototype/conformance/cases/UTC-08/expected.json` | `32ba426ff34d46c0eeafcfcdcf3b79150b0a3476` | 738 |
| `prototype/conformance/cases/UTC-09/expected.json` | `ddbd38f70fb5446fac23e703e662d782aca1893b` | 1004 |
| `prototype/conformance/cases/UTC-10/expected.json` | `f1adae9bcb81b356673965b6741bb12e920f8eef` | 608 |
| `prototype/conformance/cases/W-01/expected.json` | `04d5ddb27d2af386be03e2fe6e37e9f9eefcefa2` | 764 |
| `prototype/conformance/cases/W-02/expected.json` | `1e9b51dc6f9598df3ec19a79f197cba4a1d38c30` | 754 |
| `prototype/conformance/issue.py` | `d114b5c24e70e0131487b31d2bc24fa5125120f9` | 21191 |
| `prototype/conformance/run.py` | `1cb69d7e52128159c99eec31c1c4e9d5ed41ef5d` | 8972 |
| `prototype/conformance/tcrypto.py` | `a8500b0d73fe61f9fcca3e6354f3bf7c53f49a5c` | 10779 |
| `prototype/conformance/universe.py` | `a725aa0595146fe490c27573b2264d8b3ad34934` | 28790 |
