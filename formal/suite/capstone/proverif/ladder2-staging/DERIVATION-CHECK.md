# Ladder 2 staging — derivation check

**STATUS: PROPOSED — 2026-09-24 — produced by the AI collaborator (capstone builder, directed by the
owner instance); staged, NOT installed; not adopted; the commit is the author's.** Everything in this
directory was produced on wam-nuc (this machine) by the commands named below. Nothing outside
`proverif/ladder2-staging/` was modified.

## 1. The model

`capstone.pv` here is `../capstone.pv` (blob `c6969b4cc2f2e30be7a7a950af7609ea75e4c700`, ladder 1)
with **34 lines added and none removed or changed**: a blank line, a 32-line dated comment block
(RECUT 2026-09-24), and `set selFun = Term.`, inserted after the STATUS header block (after
original line 44, the blank line following the header's closing rule). `diff ../capstone.pv capstone.pv`
prints a single hunk, `44a45,78`, of `>` lines only.

| | blob |
|---|---|
| ladder 1 `capstone.pv` | `c6969b4cc2f2e30be7a7a950af7609ea75e4c700` |
| **ladder 2 `capstone.pv` (staged)** | **`a9fb7da1e4851120677b21dea4a8c98a481ad43a`** |

`set selFun = Term.` is the first non-comment line of the file, so it precedes every declaration.
`lib/tessera_theory.pvl` contains no `set` line (checked with `grep -n "^set" `), so there is no
conflicting setting from the library.

## 2. The derivation

`derive.py` and `run_ladder.sh` are byte-identical copies of `../derive.py` and `../run_ladder.sh`
(`cmp` clean). **`derive.py` needed no fix**: its block markers (`MARKS`), `qdrop` needles, the
degraded header rewrite and the C-C1 title rewrite all match text that lies below or inside the
original header and is untouched; the recut block contains none of those strings, and `derive.py`
makes no line-count assumption. `python3 derive.py` in this directory wrote **79 files**
(`capstone_b.pv`, `capstone_d.pv`, `cap_cc01_c.pv`, 76 companions), which with `capstone.pv` is
**80 files, the same 80 names as `../*.pv`**.

**Check, per file:** `diff ../<name>.pv <name>.pv`. For **all 80**: one hunk, 34 lines added, 0
removed, and the added text is **identical** to the added text of `capstone.pv`'s own diff (compared
as strings). The hunk is `44a45,78` in the four case files (`capstone`, `capstone_b`, `capstone_d`,
`cap_cc01_c`) and `59a60,93` in the 76 companions, whose generated 15-line header precedes it.
In every file `set selFun = Term.` is the first non-comment line. So each staged file is its
ladder-1 file plus the one block, and nothing else — which is also a regeneration check of ladder 1:
`derive.py` still reproduces every ladder-1 file exactly, modulo the block.

**Old blobs checked against the run record.** For the 56 files that have a line in the ladder-1 log
(mirrored at `/home/tony/tessera-ladder-vm-backup/proverif/ladder.log`, 106 lines), the old blob in the
table equals the `blob=` on every one of their lines; the other 24 (every `_d` companion) have no line
yet. The `.pv` files in the VM mirror are byte-identical to `../*.pv`.

The last column is the file's **last** line in the ladder-1 log (mirror line number), for the
owner's cross-check: every `rc=0` file must reproduce its RESULT lines in ladder 2.

| file | ladder-1 blob | ladder-2 blob (staged) | diff | ladder-1 last line |
|---|---|---|---|---|
| `cap_cc01_c.pv` | `ee786ce258980d317d3c48b1818006df19d785d5` | `22f1139f65d7e9b10227548ec7ef74e1c7ae1c63` | 34 added, 0 removed | rc=143, ladder.log:24 |
| `cap_cc02_a.pv` | `c873de562b487a73b2c5c5e4796799f573538f4b` | `d6fda1805ed0c4f9b36bdef4990d5910ed8df812` | 34 added, 0 removed | rc=0, ladder.log:32 |
| `cap_cc02_b.pv` | `41105e29b80d798cb8050dbb722c060e4e7af217` | `8484999ebb257235998366bd31828a9926c15a9b` | 34 added, 0 removed | rc=0, ladder.log:59 |
| `cap_cc02_d.pv` | `f91ce6b684528b753f2f19d1f6c17098e85b7b35` | `e53e37fe5f73eb6c7f4251c1cb650d9d9424cab0` | 34 added, 0 removed | no line (not run to a logged rc) |
| `cap_cc03_a.pv` | `71ca214b335275ec359188ea4e30420eaaac6624` | `b763a099592769d950bf1768d44895151b55afba` | 34 added, 0 removed | rc=0, ladder.log:30 |
| `cap_cc03_b.pv` | `5b317c876ef76b93641b6eb2b7a2291211d2d4c8` | `70c53f47867f7825f70775010e6d834dbfc20129` | 34 added, 0 removed | rc=0, ladder.log:57 |
| `cap_cc03_d.pv` | `a7bb187d2cc38efe6c42e8402a38f9fafa6bf686` | `30ae458d0e2c7aaa4547929722e9e3932380a757` | 34 added, 0 removed | no line (not run to a logged rc) |
| `cap_cc04_a.pv` | `b75ffb09de4a21ebfb81b6c71bf5f8f8a0c40c6e` | `97a2e5216458cdd41b393b2aa730cdc001573423` | 34 added, 0 removed | rc=0, ladder.log:31 |
| `cap_cc04_b.pv` | `329d264042d928e04b75c6bb16996a0abc4db73f` | `c8e70fb5d86eb73815eb9900951d8ae1585bc20d` | 34 added, 0 removed | rc=0, ladder.log:58 |
| `cap_cc04_d.pv` | `1fb3a8f9f8a2c8809f3657f4e22f1dec2ada0143` | `7d47b6be151a8ec15803a17df9769a0e2d70ddf8` | 34 added, 0 removed | no line (not run to a logged rc) |
| `cap_cc05_a.pv` | `9553504d16d361a87c0fd5f0e4ba6fdca46fe921` | `6ab8fc3ad3474711a9411e595a5854b5ba03e584` | 34 added, 0 removed | rc=0, ladder.log:78 |
| `cap_cc05_b.pv` | `1c41913242ca62dff3bb090dd5006cc8d471b750` | `37f4229817dcf592d9b213731a35e4b55961cd2a` | 34 added, 0 removed | rc=0, ladder.log:84 |
| `cap_cc05_d.pv` | `55119b7c13282c78d2e807320399c958f5bca29d` | `818e616dbf0063d76ca1e618333bb4ba59fd373b` | 34 added, 0 removed | no line (not run to a logged rc) |
| `cap_cc06_a.pv` | `545e5c93fee184ffc17946934bc68340c1f8e7dd` | `fd5d38d05868a5fba60d7ecd6d165452319b7821` | 34 added, 0 removed | rc=0, ladder.log:35 |
| `cap_cc06_b.pv` | `8ee212a581a927d59afcc3ae331713750505b8ce` | `131dab307b5da57d33e34ffb5674b2513a510f55` | 34 added, 0 removed | rc=0, ladder.log:85 |
| `cap_cc06_d.pv` | `54ab055d5a140dcb1137bba6f006572320fc5c90` | `23ea7fce8e804f096c20f3b0213815e5b30400c5` | 34 added, 0 removed | no line (not run to a logged rc) |
| `cap_cc07i_a.pv` | `dc832a2fb092afe657d92ca2b23531219d5a7eda` | `bedf99f99117b6e13055f59db237567d46462538` | 34 added, 0 removed | rc=124, ladder.log:79 |
| `cap_cc07i_b.pv` | `f325f66a819b45f740edea85258821b2576ab8bf` | `6242e48590ecb0c7d7a15954d61a97bb3c901f3e` | 34 added, 0 removed | rc=124, ladder.log:87 |
| `cap_cc07i_d.pv` | `b95b65ea24638a001e8a76fa900e431e60823fb6` | `ad3282d9ab9c74bf4bb125d50de58990d696e824` | 34 added, 0 removed | no line (not run to a logged rc) |
| `cap_cc07ii_a.pv` | `7c0be5b5cb21da04e4afd824526c533ee86deb7a` | `e5d29cd526eecb80dba3e801b43c48be37e84f53` | 34 added, 0 removed | rc=143, ladder.log:81 |
| `cap_cc07ii_b.pv` | `384e7efd3a5083a2a01a06c82990a387a20257e2` | `7b5741a1a6e9158a16eb68fab746d5e2e44e4b07` | 34 added, 0 removed | rc=143, ladder.log:86 |
| `cap_cc07ii_d.pv` | `23a73e2ee843257599c66c923c28ac56bad39d75` | `46fb100f7cba026e3c414d1a4bd8d22b62aeeae2` | 34 added, 0 removed | no line (not run to a logged rc) |
| `cap_cc08_a.pv` | `69bef9c616c7c3c2b21cee488c805add5f34c12f` | `5e07571f35544650c3be8b2bab7d51a953359f86` | 34 added, 0 removed | rc=0, ladder.log:37 |
| `cap_cc08_b.pv` | `84007b5c50f345e11af92d0f86f20e66d7399152` | `ab545d851ce16fb23c01ab5c15398f776611b22a` | 34 added, 0 removed | rc=0, ladder.log:89 |
| `cap_cc08_d.pv` | `e5b5ee98550f0f3c04cef91ec638287bd03754fa` | `061a0c7430718217d5efa8892f3f5df41e9b5bf2` | 34 added, 0 removed | no line (not run to a logged rc) |
| `cap_cc08i_a.pv` | `aa0393691751df77d9a4f107278f72a955abe9ca` | `6484782b186938f86402e830595c43857a890732` | 34 added, 0 removed | rc=0, ladder.log:36 |
| `cap_cc08i_b.pv` | `f8b65eacb9537ccaf2d6c6e610b26858a27f78f1` | `32b3bbb6b9fde9e6db233293920a2fa0c6b4f4fb` | 34 added, 0 removed | rc=0, ladder.log:64 |
| `cap_cc08i_d.pv` | `e61485eabee3e2385d92173a2769db245f271abe` | `1f1ee48d480514c46afbabdcbcf4399dfb94026c` | 34 added, 0 removed | no line (not run to a logged rc) |
| `cap_cc08ii_a.pv` | `6693ff18840f962746189df7e9ccefac37729802` | `64a909495713bed099133c44110c104baaaaa6fe` | 34 added, 0 removed | rc=0, ladder.log:40 |
| `cap_cc08ii_b.pv` | `f395e663a6d271c737760586aca3b7d67b67d817` | `7abe23e1bf3a47513b5a7ae6ee1bcda146222043` | 34 added, 0 removed | rc=0, ladder.log:88 |
| `cap_cc08ii_d.pv` | `55dfc26466ab4764b7f0c41d9b5cff317e80cf85` | `2d1550408339f4d7225499f965ae73a2d398e084` | 34 added, 0 removed | no line (not run to a logged rc) |
| `cap_cc09_a.pv` | `4399e08d839bc072adf5561f23ed0a80806eb433` | `36810d30679a9ed6026135f782c3b934a903c7b9` | 34 added, 0 removed | rc=0, ladder.log:39 |
| `cap_cc09_b.pv` | `ecb2f42a4854224d001ae5bb501a41a45df8609f` | `80c42a41460cd636645e27356bae943d5f571770` | 34 added, 0 removed | rc=0, ladder.log:90 |
| `cap_cc09_d.pv` | `00537fab238690d2adfadef75a655890b96c84e4` | `44a30c9ec408ae852c056de7dbe660ff597284c4` | 34 added, 0 removed | no line (not run to a logged rc) |
| `cap_cc10_a.pv` | `e7b7da99d043aa3cd4d6fc3dd75a68cc89fcce17` | `f22c091639dba9b72ed4e5f1f2f59cc07d38d95a` | 34 added, 0 removed | rc=0, ladder.log:41 |
| `cap_cc10_b.pv` | `d8df5a1b4e6d93da57dc1107934ea10c6c6e3933` | `ba5abd0ae5314649ffd155be73e0c1fef63db1ba` | 34 added, 0 removed | rc=0, ladder.log:91 |
| `cap_cc10_d.pv` | `f346c842bdfc91bc8e835759162cf018bc801838` | `10738015d86023ec38186bb1027a0fdc42c0964e` | 34 added, 0 removed | no line (not run to a logged rc) |
| `cap_cc10iso_a.pv` | `befaea669fec8f37f458279dedbfabc36591edea` | `5f41d6c90a90130ea579faa13621e28fabd9e71c` | 34 added, 0 removed | rc=0, ladder.log:42 |
| `cap_cc10iso_b.pv` | `b455b81d0c445734d667b70abdcedf0ada5b13db` | `242a2e5fafda23f786435512207477ecb8913691` | 34 added, 0 removed | rc=0, ladder.log:92 |
| `cap_cc11abl6_a.pv` | `9d12106ced11d707a0ee7f58086b7b8fc18d4b72` | `54517e5d667276d0f34ee6726c56a9320d17eb6b` | 34 added, 0 removed | rc=0, ladder.log:43 |
| `cap_cc11abl6_b.pv` | `9f578f2d7275b40efce9cbdcda359e09c15b9df4` | `4391bb805c68bf562779fcb33315b564818a3d1d` | 34 added, 0 removed | rc=0, ladder.log:93 |
| `cap_cc11abl6_d.pv` | `5988a8e64b89448ae8bf051e5f6b5608f427e18a` | `31506250df3f10dd90264591c5e784f9d720a232` | 34 added, 0 removed | no line (not run to a logged rc) |
| `cap_cc11_a.pv` | `ae887ef812b480705a1bc640584aedef7420c211` | `ec1c7287ec9ca1f34521260485f939f5f1c5fa5c` | 34 added, 0 removed | rc=0, ladder.log:44 |
| `cap_cc11_b.pv` | `66eadecb10a44f02bf024c7028f6d717187bc043` | `a9ff0de314aaa966a8e0017b530266c81557c57e` | 34 added, 0 removed | rc=0, ladder.log:95 |
| `cap_cc11_d.pv` | `8dafaa8afe34739a0ce1961fc1cfef8a5f8dc5ab` | `98620011b02fbbc0f089fcdc873deba5c3504e23` | 34 added, 0 removed | no line (not run to a logged rc) |
| `cap_cc11q4_a.pv` | `407dea09337a84d6549632ab7d1dfee9891607ad` | `9296067b71b4012edcdd145e4e85f33e612c741c` | 34 added, 0 removed | rc=0, ladder.log:46 |
| `cap_cc11q4_b.pv` | `a5d00625a1cc48b9535f4ba7ed7bcf94707c1905` | `ea37d58203949b2000660272f92e7b07569f71c6` | 34 added, 0 removed | rc=0, ladder.log:94 |
| `cap_cc11q4_d.pv` | `e30d9d4303e599253e0ba3f0f28257d8e5d0cee5` | `c768bb4c44ac0c8f4eadc48c8bdba709ca1ff710` | 34 added, 0 removed | no line (not run to a logged rc) |
| `cap_cc12_a.pv` | `1548b4cfef2556ef38e48141fbda611661d2590b` | `057899bb6ce90b19365e1f3966f3eaf60726d6c5` | 34 added, 0 removed | rc=0, ladder.log:47 |
| `cap_cc12_b.pv` | `ad1848e75b4682f993f0911de5d567649f3d8ca0` | `525ea9e13992833e094fc3bb48830e72d0d93257` | 34 added, 0 removed | rc=0, ladder.log:97 |
| `cap_cc12_d.pv` | `b0c0e2f6cbe0826ee3956c700e597cbad19cc05d` | `3746c11d394c5b5c3027c6fd1c99be9cbb5dec95` | 34 added, 0 removed | no line (not run to a logged rc) |
| `cap_cc13i_a.pv` | `1300437b31b66a2f092af63d521a6edc0725689f` | `59b3ac68d0135e8356f9f49d1794d845147d6dce` | 34 added, 0 removed | rc=0, ladder.log:45 |
| `cap_cc13i_b.pv` | `a2be31da4433322935dc8f2bd0af0349dd7f5cdf` | `e1ed73216548408fab17cb48cc0b3b3de175d2d5` | 34 added, 0 removed | rc=0, ladder.log:96 |
| `cap_cc13i_d.pv` | `724c935b31a1e55dbba6ad73b7950088562bb98d` | `63e6d59696d7800d74897425c6ce67fe44b83fc9` | 34 added, 0 removed | no line (not run to a logged rc) |
| `cap_cc13ii_a.pv` | `7f2ec452c2f157bf5378469a2c29d33a0a0998d2` | `84a4108c9bd16aee82545a6ad4e92673a0bbc70a` | 34 added, 0 removed | rc=0, ladder.log:49 |
| `cap_cc13ii_b.pv` | `48adaf7c21caef7f2460e603ba096ae773553e89` | `376b589df1a856c47802bcea9dcf7f3a2194c69c` | 34 added, 0 removed | rc=0, ladder.log:98 |
| `cap_cc13ii_d.pv` | `6a05732a495d627e8fd93ceae2eb2a23d3df81b6` | `f34336dbd2c6b1f8edfff259aa4ad00495d2377b` | 34 added, 0 removed | no line (not run to a logged rc) |
| `cap_cc14_a.pv` | `6ed862086dbb01af57a12a8bca40e584c7820b22` | `307cfd9d76cb8148a4fa93c72350d513d51d1f29` | 34 added, 0 removed | rc=143, ladder.log:80 |
| `cap_cc14_b.pv` | `4acb5bc2ca44796bc47abb1bd9c32e95451219b9` | `a2f2398212e2705e360e7c83ab170d466076c580` | 34 added, 0 removed | rc=143, ladder.log:99 |
| `cap_cc15i_a.pv` | `133ad05fbe21d3ddc2dfb5af4df42d987006b66d` | `9a19904bb64e3944c6735c8feab2808693dd281f` | 34 added, 0 removed | rc=0, ladder.log:48 |
| `cap_cc15i_b.pv` | `8868cb3fdcebfcdbaf001ddde5993e1ae4a96f32` | `5bd381d16a199442b4b84ce7a2fb0de110da615f` | 34 added, 0 removed | rc=0, ladder.log:100 |
| `cap_cc15i_d.pv` | `41397b0bd5cf387d21e2436dfac1f02bacbd5fe7` | `03365225821bafbd55fb25f7a15dd939b7f30d70` | 34 added, 0 removed | no line (not run to a logged rc) |
| `cap_cc15ii_a.pv` | `a017f519a0d687cbf4b4c175df111fa2722dd765` | `3bd03e9f3f04983e8224eb1d57f607f5f74d99d2` | 34 added, 0 removed | rc=0, ladder.log:52 |
| `cap_cc15ii_b.pv` | `a11248bf35175de990addbc81198b1f9149d331f` | `a394ffc80ed3b0a60aca7aec03cdcd1188d6bed2` | 34 added, 0 removed | rc=0, ladder.log:101 |
| `cap_cc15ii_d.pv` | `c39b9af1710fb20c1367813ba9526fd0e62f3d6d` | `d14bcde51ed64a4e9584bac40eed3613f1a9e3e0` | 34 added, 0 removed | no line (not run to a logged rc) |
| `cap_cc15iii_a.pv` | `d42ba7972e6c7cdbad29d1635469a0eb9b425724` | `f014d7abc2f3ebb18bce194bb6a0c8e5231a4dc9` | 34 added, 0 removed | rc=0, ladder.log:51 |
| `cap_cc15iii_b.pv` | `2efae44f570fdf8a0f2bafa34a509ec19e0aa129` | `a2e3d45158fdfba3aebfe3eff1d206f5adf2e41e` | 34 added, 0 removed | rc=0, ladder.log:102 |
| `cap_cc15iii_d.pv` | `5a7f77eda6c86bf180702c7ce695020b04e8f917` | `9e7df164c1de6a56d27c2fab7a6fcb7b152deef8` | 34 added, 0 removed | no line (not run to a logged rc) |
| `cap_cc16_a.pv` | `b80681f4ecfae4db371b6c2c39068def8cc7f70e` | `dd22ca2e8e9dc48a204b8f759955498ac9810091` | 34 added, 0 removed | rc=0, ladder.log:53 |
| `cap_cc16_b.pv` | `25ef4e3d026daa96c795b41b9095e4c2be204954` | `2ab5f17c32bb743e39526dbb5d1595a0a5709fb1` | 34 added, 0 removed | rc=0, ladder.log:103 |
| `cap_cc16_d.pv` | `b033f8dbb178f90dc8efe5317093865c84d0a4b4` | `7dcc4f87a33cae72061d5977821378a68f5616ce` | 34 added, 0 removed | no line (not run to a logged rc) |
| `cap_cc17_a.pv` | `5c783913d33f2d35fb033206fbbe7acee0d23130` | `99023e81a0e1296e7253ef6115685086f619dab0` | 34 added, 0 removed | rc=0, ladder.log:82 |
| `cap_cc17_b.pv` | `ab6221accd77a69caacdb328960f34e2d3721df4` | `94d9d7bd1539c6939d086a82b93177d729e5e9e6` | 34 added, 0 removed | rc=0, ladder.log:105 |
| `cap_cc17_d.pv` | `8e47115b5914833e616391c5d5b44013fbf2a1bd` | `79dc5880ff9b74a2621282be9b7e6c422b7f5ec0` | 34 added, 0 removed | no line (not run to a logged rc) |
| `cap_cc18_a.pv` | `dfed3db392bdba3a430b0c99b29fb222540d0d46` | `5107592245dffdd5b91bb4e6238ef90eae587f33` | 34 added, 0 removed | rc=0, ladder.log:54 |
| `cap_cc18_b.pv` | `15f53b5048382ccbc4b29056a18671e7bf5f7530` | `7c5a37d76ab5bfc2c92f4ab566685c7161c88d94` | 34 added, 0 removed | rc=0, ladder.log:104 |
| `cap_cc18_d.pv` | `a7144d19e2e23358365b0455d4859d757a30226c` | `0360cff8e6d02f3291da788beac4d0297b20aa1e` | 34 added, 0 removed | no line (not run to a logged rc) |
| `capstone_b.pv` | `65503ff3ce59eb62df36cd4cb74502ae391e86c0` | `7e17e0574c7577784f52de6fe45a489886b84d8a` | 34 added, 0 removed | rc=0, ladder.log:16 |
| `capstone_d.pv` | `d4f0851db6cd81e760c5cb847664b558a194911c` | `5ea1082c8fedb09b7698e76d608fd557b4ae5bd7` | 34 added, 0 removed | rc=0, ladder.log:25 |
| `capstone.pv` | `c6969b4cc2f2e30be7a7a950af7609ea75e4c700` | `a9fb7da1e4851120677b21dea4a8c98a481ad43a` | 34 added, 0 removed | rc=0, ladder.log:15 |

Summary of the last column: **49** files `rc=0` (landed); **2** `rc=124` (`cap_cc07i_a`, `cap_cc07i_b`,
timeout at the 71100 s box); **5** last logged `rc=143` (`cap_cc01_c` :24, terminated on wam-nuc and
never rerun; `cap_cc14_a` :80, `cap_cc07ii_a` :81, `cap_cc07ii_b` :86, `cap_cc14_b` :99, by the 80 GB
guard); **24** no line (the degraded companions — wave 5 was in flight when the mirror was taken).

**One pre-existing observation, not fixed, identical in both ladders.** `derive.py`'s `degraded()`
has a second header rewrite meant to add *"Derived from capstone.pv by derive.py's degraded()
transformation; a documented copy, see RESULTS.md."* (`derive.py:133-135`). Its search string's
padding does not match `capstone.pv`'s line 7, so it is a silent no-op, in ladder 1 as here
(`../capstone_d.pv` lines 6-7 carry only the first rewrite). It is comment text only. It was **not**
fixed: fixing it would make `capstone_d.pv` differ from its ladder-1 file by more than the recut
block, which the uniformity rule forbids. Flagged for the owner.

## 3. Smoke test

Run on wam-nuc, 2026-09-24T15:08:52Z, from this directory, alone (no other ProVerif process), under
`ulimit -v 8388608` (8 GiB), `nice -n 19`, `timeout 900`:
`/usr/bin/time -f %M -o smoke_capstone.rss proverif -lib ../../../lib/tessera_theory.pvl capstone.pv > smoke_capstone.out`.
The record line is `smoke.log:1`, verbatim:

```
smoke capstone rc=0 seconds=224 peakRSSkB=340072 blob=a9fb7da1e4851120677b21dea4a8c98a481ad43a results=47 started=2026-09-24T15:08:52Z host=wam-nuc-ubuntu-2204
```

**Result: 47 RESULT lines, identical to ladder 1's.** `diff <(grep '^RESULT' ../capstone.out)
<(grep '^RESULT' smoke_capstone.out)` is empty (33 `is true`, 14 `is false`, the same in both).
**Cost: 224 s and 340 072 kB (0.32 GiB) peak RSS, against ladder 1's 374 s for the same case**
(`../ladder.log:15`, which predates per-run RSS recording). This is the correct form, case (a) only.
It is not evidence about any companion.

**Note on the `-lib` path.** From this staging directory the library is at `../../../lib/`. The runner's
`LIB=../../lib/tessera_theory.pvl` is only correct from `proverif/` itself. See §4.

## 4. `run_ladder.sh` with a fresh `ladder.log`: read, not run

The staged copy is byte-identical to `../run_ladder.sh`. A fresh, empty `ladder.log` does **not**
cause anything to be skipped. The skip guard (`run_ladder.sh:73` in `run()`, and again at `:98` in
`wave()`) is `grep -E "^<name> rc=" ladder.log | grep -vE "rc=(137|143) " | grep -q .`, reading only
`./ladder.log`. I tested that pipeline in isolation (not the script) against an empty file, and it
returns RUN. Against the ladder-1 log it returns SKIP for `capstone` and for `cap_cc07i_a` (its
`rc=124` counts as landed), and RUN for `cap_cc14_a` and `cap_cc02_d`. There is no other reference
to earlier history. The header lines record the new blob automatically (`git hash-object
capstone.pv`, `:54`). Five things the installer must get right, none of which requires editing the
script:

1. **Install into `proverif/`, and do not run the script from `ladder2-staging/`.** `LIB` is relative
   (`:45`, `../../lib/tessera_theory.pvl`), and from the staging directory it points at a
   non-existent `capstone/lib/`. Every ProVerif call would then fail at once with a non-zero rc other
   than 137/143. The skip guard would read each of those as **landed**, and the log would be poisoned.
2. **Move ladder 1's `ladder.log` out before launching.** Left in place, it makes the runner skip
   every ladder-1 `rc=0` and `rc=124` file (51 of 80), the three failing companions' timeouts
   included.
3. **Move ladder 1's `.out`/`.rss` into `proverif/ladder1/` first.** The runner overwrites
   `<name>.out` and `<name>.rss` in place (`:78`, `:82`), and those files are the cross-check.
4. **No `*.mechfail` may be present.** Any `<name>.mechfail` makes the runner log `rc=MECHFAIL-MEMORY`
   and skip that file (`:65-68`). None exists in `proverif/` or in the VM mirror today. Check again on
   the machine that runs ladder 2.
5. The boxes are unchanged (`:47-48`, 71100 s strict and 65700 s degraded). `JOBS` defaults to 3
   (`:46`). ubuntu24 ran with `JOBS=2` from the environment. The memory guard is a separate script
   and is not part of this staging. `mem_guard_all.sh` exits when it sees `^DONE` in `./ladder.log`,
   which a fresh log does not yet contain.
