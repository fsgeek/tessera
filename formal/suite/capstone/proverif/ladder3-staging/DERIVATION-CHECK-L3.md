# Ladder 3 staging: the derivation check

**STATUS: PROPOSED, 2026-10-01.** Produced by the AI collaborator (Claude Opus 5.5, capstone builder,
directed by the owner instance). Staged and **NOT installed**; not adopted; the commit is the author's.
Everything in this directory was made on wam-nuc by the commands named below. Nothing outside
`proverif/ladder3-staging/` was modified. `PREDICTIONS.md` was not touched.

The source is `docs/reviews/2026-10-01-codex-review-capstone-build.md`: findings 1-4 and the owner
instance's Dispositions 1-4.

## 1. The model

`capstone.pv` here is `../capstone.pv` (ladder 2, blob `a9fb7da1…`) with four hunks and nothing else.
`diff ../capstone.pv capstone.pv`:

| Hunk | What | Lines |
|---|---|---|
| `78a79,101` | the dated REPAIR block (BF-5, BF-6; ladder 3), placed after `set selFun = Term.`. The R-9 block and its setting are **unchanged**. | +23 |
| `834a858,876` | **BF-5**: in `StandingPath`, immediately after its `sStageCh` input, a 15-line dated comment and `let framed(=OT_WRAPPER, awi, iwi, kwi, mwi, cwi, wrap(cwii, (fbNA, sgNA, fbNB, sgNB))) = fbI in 0 else`. The rest of `StandingPath` is the `else` branch, byte-identical. | +19 |
| `1054c1096,1101` | **BF-6**: in `StandingJudge`, `event HonestStandingEstablished(kX, aidD)` becomes `if lyr <> L0 then event …`, under a dated comment. | 1 changed, +5 |
| `1064c1111,1115` | **BF-6**: in `ScopeAgreementJudge`, `event HonestWrappedStandingAgreed(a, l)` becomes `if l <> L0 then event …`, under a dated comment. `ScopeMisreported` is not guarded. | 1 changed, +4 |

| | blob |
|---|---|
| ladder 2 `capstone.pv` | `a9fb7da1e4851120677b21dea4a8c98a481ad43a` |
| **ladder 3 `capstone.pv` (staged)** | **`35d8c7020adc31f714d31b12c34a8eaf68010c9b`** |

**BF-5's choice.** The registration defines "wrapped" as *"an `OT_WRAPPER` frame whose payload field
is a `wrap()` term"* (`PREDICTIONS.md:942-944`), and the standing path's own `SUnwrap` descends on exactly
that pattern. So "innermost" is the layer whose frame does **not** match it. The guard is the complement
of `SUnwrap`'s pattern. It adds no verifier check and no envelope dependency, so (E1) is untouched. The
smaller-looking alternative, `let framed(=OT_ATTEST, …) = fbI in`, was rejected. It would copy envelope
check 5 into the standing path, where C-C13(i) cannot remove it, and it defines innermost by type, which
the registration does not do. **BF-6** guards the emissions exactly as the reviewer's
`capstone_wrapped_witness.pv` did. `HonestStandingEstablished`'s emission site does have the layer in
scope: `StandingJudge` reads `lyr` from `estCh`.

## 2. The derivation

`derive.py` here is `../derive.py` with **one** functional change (BF-7) and one added comment:

- `cc07i` (BF-7). `if sigFrameKfp(sb_, k_) = fp(k_) then` is replaced by the family's pattern match,
  `let framed(sfo_, sfa_, sfi_, =fp(k_), sfm_, sfc_, sfp_) = sb_ in`
  (`d6e_sp1_q8all_samekey_unbound.pv:258`), and `add_accessors` is no longer called for this companion.
  A dated comment explains the change.
- A dated **audit note** below `cc07ii` explains why `cc06` and `cc07ii` keep the catch-all accessors.
  There the fallback makes acceptance require `sb_ = fb_` with `fb_` already a `framed(…)` term, so a
  non-frame is rejected, as in the families. Their output is unchanged except for BF-5/BF-6.

**Finding 1 (C-C15(i)) produced no derivation change.** The verdict is **(R)**, a registration conflict;
see §6. `python3 derive.py` was run in this directory (`derive.log`) and wrote 79 files. With `capstone.pv`
that makes **80 files, the same 80 names as `../*.pv`**.

**The check, per file** (`tools/derivation_check.py`, which applies `tools/bf56_edit.py`; run from this directory). The four BF-5/BF-6 edits
are applied as exact-string replacements to the **ladder-2** file, with the degraded `(pkSv: pkey)`
signature substituted where needed. The result is compared with the staged file:

- **77 files**: the staged file is **byte-identical** to "ladder-2 file + the BF-5/BF-6 edits". The
  difference is +53/−2 lines in every one.
- **3 files** (`cap_cc07i_a/b/d`): after the BF-5/BF-6 edits, the remaining difference is **exactly**
  BF-7, the same in all three. It removes the 14-line accessor block (`sigFrameKfp`, `sigFrameOt`, and
  the comment and blank lines around them), and replaces the six `if sigFrameKfp(sb_, k_) = fp(k_) then`
  lines (ATTEST1, ATTEST2 ×2, WRAP1, WRAP2 ×2) by the six `let framed(…, =fp(k_), …) = sb_ in` lines.
- **No file has any other difference.** In particular the three `cap_cc15i_*` files differ only by
  BF-5/BF-6, and BF-4 is unchanged.

**Old blobs against the run record.** For every file, the ladder-2 blob in the table equals the
`blob=` on its last `ladder.log` line. `cap_cc05_d`'s last line is the `MECHFAIL-MEMORY` marker (`:78`),
which carries no blob, so its blob was checked against `:66`.

| file | ladder-2 blob | ladder-3 blob (staged) | diff | ladder-2 last line | re-run in ladder 3? |
|---|---|---|---|---|---|
| `cap_cc01_c.pv` | `22f1139f65d7e9b10227548ec7ef74e1c7ae1c63` | `36e1b35ac4b756ce5aee90ac8c6440afdfd4aa62` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:70` | yes |
| `cap_cc02_a.pv` | `d6fda1805ed0c4f9b36bdef4990d5910ed8df812` | `edf9cddc2b1d8abe861ed6be79766599fcdddd86` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:11` | yes |
| `cap_cc02_b.pv` | `8484999ebb257235998366bd31828a9926c15a9b` | `3f73504b56975ed631debfba4c075e9225950dac` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:38` | yes |
| `cap_cc02_d.pv` | `e53e37fe5f73eb6c7f4251c1cb650d9d9424cab0` | `221b997477a282092c8e9e2e5eec718523eee873` | BF-5/BF-6 hunks only (+53/-2) | rc=124 `:64` | **no** (ladder-2 mechanism failure; not re-run under this blob) |
| `cap_cc03_a.pv` | `b763a099592769d950bf1768d44895151b55afba` | `d4ce5c178b082904debdba455b4cb5cdddbc22c6` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:9` | yes |
| `cap_cc03_b.pv` | `70c53f47867f7825f70775010e6d834dbfc20129` | `fa2fc0b7118c263414af67d9e16336766331fcc3` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:36` | yes |
| `cap_cc03_d.pv` | `30ae458d0e2c7aaa4547929722e9e3932380a757` | `cc6f21c8928a00021820ee6f6617c8cdbe283140` | BF-5/BF-6 hunks only (+53/-2) | rc=124 `:65` | **no** (ladder-2 mechanism failure; not re-run under this blob) |
| `cap_cc04_a.pv` | `97a2e5216458cdd41b393b2aa730cdc001573423` | `a59d3758072722e5041d92d519f5771f8a6feedb` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:10` | yes |
| `cap_cc04_b.pv` | `c8e70fb5d86eb73815eb9900951d8ae1585bc20d` | `36ba72438ab2571f62d82ec775cc900405b7f848` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:37` | yes |
| `cap_cc04_d.pv` | `7d47b6be151a8ec15803a17df9769a0e2d70ddf8` | `a88ded5036dbfe14f9ea79ba66d5b3f22286d12a` | BF-5/BF-6 hunks only (+53/-2) | rc=124 `:63` | **no** (ladder-2 mechanism failure; not re-run under this blob) |
| `cap_cc05_a.pv` | `6ab8fc3ad3474711a9411e595a5854b5ba03e584` | `f6c8fad1550db7405cc370d0770871241f44ed22` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:12` | yes |
| `cap_cc05_b.pv` | `37f4229817dcf592d9b213731a35e4b55961cd2a` | `430e986e435005cdc8d68b5170284fad9ef8d398` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:39` | yes |
| `cap_cc05_d.pv` | `818e616dbf0063d76ca1e618333bb4ba59fd373b` | `897f56809be6b8e8f315a34de88d452455505525` | BF-5/BF-6 hunks only (+53/-2) | rc=143 `:66`, MECHFAIL-MEMORY `:78` | **no** (ladder-2 mechanism failure; not re-run under this blob) |
| `cap_cc06_a.pv` | `fd5d38d05868a5fba60d7ecd6d165452319b7821` | `b1dba38d6630ba30f74937af81c831e3dec7eb21` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:13` | yes |
| `cap_cc06_b.pv` | `131dab307b5da57d33e34ffb5674b2513a510f55` | `8063278f62fe5860eab3c8ff8c175bd039230089` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:40` | yes |
| `cap_cc06_d.pv` | `23ea7fce8e804f096c20f3b0213815e5b30400c5` | `ee1bce1be260392bea5e052d6baa52aecf566226` | BF-5/BF-6 hunks only (+53/-2) | rc=124 `:67` | **no** (ladder-2 mechanism failure; not re-run under this blob) |
| `cap_cc07i_a.pv` | `bedf99f99117b6e13055f59db237567d46462538` | `71cf46e440c5149aee6251ea61666b7cf0659d76` | BF-5/BF-6 hunks (+53/-2) **plus BF-7** (+6/-20: accessor block removed, six `if sigFrameKfp…` lines → `let framed(…, =fp(k_), …) = sb_ in`) | rc=0 `:14` | yes |
| `cap_cc07i_b.pv` | `6242e48590ecb0c7d7a15954d61a97bb3c901f3e` | `01b6127ba1b0b1e3c755ba83201cf82262263bda` | BF-5/BF-6 hunks (+53/-2) **plus BF-7** (+6/-20: accessor block removed, six `if sigFrameKfp…` lines → `let framed(…, =fp(k_), …) = sb_ in`) | rc=0 `:41` | yes |
| `cap_cc07i_d.pv` | `ad3282d9ab9c74bf4bb125d50de58990d696e824` | `ff70204731186f62d7f5f1c5d98ed33ea7718073` | BF-5/BF-6 hunks (+53/-2) **plus BF-7** (+6/-20: accessor block removed, six `if sigFrameKfp…` lines → `let framed(…, =fp(k_), …) = sb_ in`) | rc=124 `:68` | **no** (ladder-2 mechanism failure; not re-run under this blob) |
| `cap_cc07ii_a.pv` | `e5d29cd526eecb80dba3e801b43c48be37e84f53` | `00ecd4be5e62ed1015cf0be29cf727cc89f4030a` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:17` | yes |
| `cap_cc07ii_b.pv` | `7b5741a1a6e9158a16eb68fab746d5e2e44e4b07` | `5dfb85395e3fe5532dda52ea0867788a21ba2a3a` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:44` | yes |
| `cap_cc07ii_d.pv` | `46fb100f7cba026e3c414d1a4bd8d22b62aeeae2` | `14434b6185ef96684aaecc13b883c86dc9fe4f52` | BF-5/BF-6 hunks only (+53/-2) | rc=124 `:79` | **no** (ladder-2 mechanism failure; not re-run under this blob) |
| `cap_cc08_a.pv` | `5e07571f35544650c3be8b2bab7d51a953359f86` | `f0809874f360d691e79d24a572717d5fb2d8e288` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:15` | yes |
| `cap_cc08_b.pv` | `ab545d851ce16fb23c01ab5c15398f776611b22a` | `f1f63cc376ad8a10d345d1c043bd8badb488d097` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:42` | yes |
| `cap_cc08_d.pv` | `061a0c7430718217d5efa8892f3f5df41e9b5bf2` | `0406e86f91951d419b9c9dfb1a506efe05f8634c` | BF-5/BF-6 hunks only (+53/-2) | rc=124 `:80` | **no** (ladder-2 mechanism failure; not re-run under this blob) |
| `cap_cc08i_a.pv` | `6484782b186938f86402e830595c43857a890732` | `30a737f06fe0346dd6a8b707a6503f707bf0e986` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:16` | yes |
| `cap_cc08i_b.pv` | `32b3bbb6b9fde9e6db233293920a2fa0c6b4f4fb` | `cae21d561c6e2d8e52b41a5aa73eab60091b84e6` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:43` | yes |
| `cap_cc08i_d.pv` | `1f1ee48d480514c46afbabdcbcf4399dfb94026c` | `8b1e819568ced16116a922db9804319c6c8caddb` | BF-5/BF-6 hunks only (+53/-2) | rc=143 `:83` | **no** (ladder-2 mechanism failure; not re-run under this blob) |
| `cap_cc08ii_a.pv` | `64a909495713bed099133c44110c104baaaaa6fe` | `9f6532620bb0c5ad34e17964287eb0ce27f8ca01` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:19` | yes |
| `cap_cc08ii_b.pv` | `7abe23e1bf3a47513b5a7ae6ee1bcda146222043` | `bdecf6970227b5fb303ccd80ec54b0f480669da0` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:46` | yes |
| `cap_cc08ii_d.pv` | `2d1550408339f4d7225499f965ae73a2d398e084` | `d862bf69b234bddeed681ae1a1f1c99df71edac1` | BF-5/BF-6 hunks only (+53/-2) | rc=143 `:82` | **no** (ladder-2 mechanism failure; not re-run under this blob) |
| `cap_cc09_a.pv` | `36810d30679a9ed6026135f782c3b934a903c7b9` | `71194b8b8be59b7da032886290d756b2dc7347a4` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:18` | yes |
| `cap_cc09_b.pv` | `80c42a41460cd636645e27356bae943d5f571770` | `77f6929b5a09f74694c852d814ac9a6a9f4ffd9c` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:45` | yes |
| `cap_cc09_d.pv` | `44a30c9ec408ae852c056de7dbe660ff597284c4` | `9ec7691145a3238ee69a0d5813121c7b81e4007b` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:81` | yes |
| `cap_cc10_a.pv` | `f22c091639dba9b72ed4e5f1f2f59cc07d38d95a` | `83a3aeaf8f9c84047465fdec37db599f36082f02` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:20` | yes |
| `cap_cc10_b.pv` | `ba5abd0ae5314649ffd155be73e0c1fef63db1ba` | `790f4cc5b4912d7f266e46c473efab14cffa2393` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:47` | yes |
| `cap_cc10_d.pv` | `10738015d86023ec38186bb1027a0fdc42c0964e` | `4fcdb65becf7943b37e0bebbca3e3379f3044488` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:84` | yes |
| `cap_cc10iso_a.pv` | `5f41d6c90a90130ea579faa13621e28fabd9e71c` | `390df111c4446e509a253964901c615960453b04` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:21` | yes |
| `cap_cc10iso_b.pv` | `242a2e5fafda23f786435512207477ecb8913691` | `fb8f541e2e96ab24cd325e907bf78441c323a163` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:48` | yes |
| `cap_cc11_a.pv` | `ec1c7287ec9ca1f34521260485f939f5f1c5fa5c` | `ebf2ca4168eb4d4720b6a2070abe8fed18b04b13` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:23` | yes |
| `cap_cc11_b.pv` | `a9ff0de314aaa966a8e0017b530266c81557c57e` | `0458dee2999bc34eb87d0343cd91a21d7a533fb4` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:50` | yes |
| `cap_cc11_d.pv` | `98620011b02fbbc0f089fcdc873deba5c3504e23` | `ee8617437505993b547edc14110a8caae52a2a8b` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:86` | yes |
| `cap_cc11abl6_a.pv` | `54517e5d667276d0f34ee6726c56a9320d17eb6b` | `3ca0a1ca1271e7752af33572a9d65c25f49c411a` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:22` | yes |
| `cap_cc11abl6_b.pv` | `4391bb805c68bf562779fcb33315b564818a3d1d` | `edf03bf20bbf96eaf55986b79c07531968a6c3d0` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:49` | yes |
| `cap_cc11abl6_d.pv` | `31506250df3f10dd90264591c5e784f9d720a232` | `51f47b69bbccab2393f714128cd5b9d8b4c4b63b` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:85` | yes |
| `cap_cc11q4_a.pv` | `9296067b71b4012edcdd145e4e85f33e612c741c` | `476d6e68b8d53dd72f8693ed640343e44ab3cb34` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:25` | yes |
| `cap_cc11q4_b.pv` | `ea37d58203949b2000660272f92e7b07569f71c6` | `e27668945738074da1a2ef2c7bf5438a8242c560` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:52` | yes |
| `cap_cc11q4_d.pv` | `c768bb4c44ac0c8f4eadc48c8bdba709ca1ff710` | `70e802bf694f1d5c8eaf69959805dddfd739864f` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:88` | yes |
| `cap_cc12_a.pv` | `057899bb6ce90b19365e1f3966f3eaf60726d6c5` | `d4c7bf62dc18fa8468afc2c99dca857d8f6c87f3` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:26` | yes |
| `cap_cc12_b.pv` | `525ea9e13992833e094fc3bb48830e72d0d93257` | `d3a19adfd245e4797200517a7facd21f39db977a` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:53` | yes |
| `cap_cc12_d.pv` | `3746c11d394c5b5c3027c6fd1c99be9cbb5dec95` | `10545d60f59da655fd6d8a8b0adc02e307bb0c2f` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:89` | yes |
| `cap_cc13i_a.pv` | `59b3ac68d0135e8356f9f49d1794d845147d6dce` | `4135aa5836cab498aba30436392a82983a68ae0c` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:24` | yes |
| `cap_cc13i_b.pv` | `e1ed73216548408fab17cb48cc0b3b3de175d2d5` | `52ce5c5704292041dacb7c0af9636ff8bcf86746` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:51` | yes |
| `cap_cc13i_d.pv` | `63e6d59696d7800d74897425c6ce67fe44b83fc9` | `f40f10875d55d15db30b92c9416420633a748be0` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:87` | yes |
| `cap_cc13ii_a.pv` | `84a4108c9bd16aee82545a6ad4e92673a0bbc70a` | `0ace64ca9418e7a226eedfe3efde5b7d864c9b3d` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:28` | yes |
| `cap_cc13ii_b.pv` | `376b589df1a856c47802bcea9dcf7f3a2194c69c` | `c16b426da843626438138f3a4f0875e2788925bb` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:55` | yes |
| `cap_cc13ii_d.pv` | `f34336dbd2c6b1f8edfff259aa4ad00495d2377b` | `0e277e90b85244e5a9c228d71286b1bd98d20590` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:92` | yes |
| `cap_cc14_a.pv` | `307cfd9d76cb8148a4fa93c72350d513d51d1f29` | `9f47115a1a60262d544f9b71c3e6365a7e316061` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:29` | yes |
| `cap_cc14_b.pv` | `a2f2398212e2705e360e7c83ab170d466076c580` | `3a4b64b69f45514a3519489dd5c1fbb66cf58c46` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:56` | yes |
| `cap_cc15i_a.pv` | `b5dbf3d233b9e91f198ed2342c3896d8bedff32b` | `ccaba043b7b935392626a36180fe2caf958648cb` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:101` | yes |
| `cap_cc15i_b.pv` | `95426aeef93dbbe72118e6f89e2f5cadc871ea01` | `28a45fcd329d5f520b8298a04eb5a319b2135565` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:102` | yes |
| `cap_cc15i_d.pv` | `bc00b8310f7f77211c4ce540ede7f318a3e688ac` | `93e8a663712517fbd84b6dff8de686c3e39b5453` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:103` | yes |
| `cap_cc15ii_a.pv` | `3bd03e9f3f04983e8224eb1d57f607f5f74d99d2` | `1b8faa4d5bdd4c5bece15e0f72278c5731b06193` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:31` | yes |
| `cap_cc15ii_b.pv` | `a394ffc80ed3b0a60aca7aec03cdcd1188d6bed2` | `574f91ad3184522269443f9bc27f1ebca49baa90` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:58` | yes |
| `cap_cc15ii_d.pv` | `d14bcde51ed64a4e9584bac40eed3613f1a9e3e0` | `94efa8f27d24592bb46e2aad7b1f3b9566c7d007` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:90` | yes |
| `cap_cc15iii_a.pv` | `f014d7abc2f3ebb18bce194bb6a0c8e5231a4dc9` | `f862c7513ca71ba64335ef52c0b7732dff3257e8` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:32` | yes |
| `cap_cc15iii_b.pv` | `a2e3d45158fdfba3aebfe3eff1d206f5adf2e41e` | `02443a3a4f1203b0a0c80a29ee95d37d2ad3f33e` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:59` | yes |
| `cap_cc15iii_d.pv` | `9e7df164c1de6a56d27c2fab7a6fcb7b152deef8` | `053e3de4a5a4db1c1095182960597f29ac32f1b9` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:93` | yes |
| `cap_cc16_a.pv` | `dd22ca2e8e9dc48a204b8f759955498ac9810091` | `f9deb0474b02f7a91a733f1e4f8da2972f162e3e` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:30` | yes |
| `cap_cc16_b.pv` | `2ab5f17c32bb743e39526dbb5d1595a0a5709fb1` | `994002371990027460e4ecd244e1620b6d9be6e3` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:57` | yes |
| `cap_cc16_d.pv` | `7dcc4f87a33cae72061d5977821378a68f5616ce` | `fc614b06d95ad9105c65423b139a4d82197371ed` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:94` | yes |
| `cap_cc17_a.pv` | `99023e81a0e1296e7253ef6115685086f619dab0` | `7e9e5f6c2c573bc57b8eb1dc49f3c68d142a7d5a` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:34` | yes |
| `cap_cc17_b.pv` | `94d9d7bd1539c6939d086a82b93177d729e5e9e6` | `012ba9a157de7cf22000f7582d7c42c61b749266` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:61` | yes |
| `cap_cc17_d.pv` | `79dc5880ff9b74a2621282be9b7e6c422b7f5ec0` | `19b706af3d835c32355c288f23def063d3cf5676` | BF-5/BF-6 hunks only (+53/-2) | rc=143 `:95` | **no** (ladder-2 mechanism failure; not re-run under this blob) |
| `cap_cc18_a.pv` | `5107592245dffdd5b91bb4e6238ef90eae587f33` | `dcd243952b19879184c88d2a1546759ddacf5eb0` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:33` | yes |
| `cap_cc18_b.pv` | `7c5a37d76ab5bfc2c92f4ab566685c7161c88d94` | `792b3171d1dd0e8f54088125fd7bf056f1846b0a` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:60` | yes |
| `cap_cc18_d.pv` | `0360cff8e6d02f3291da788beac4d0297b20aa1e` | `3d2eeb978ee8abd1bcc9ef53aac9abea0def075a` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:96` | yes |
| `capstone.pv` | `a9fb7da1e4851120677b21dea4a8c98a481ad43a` | `35d8c7020adc31f714d31b12c34a8eaf68010c9b` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:5` | yes |
| `capstone_b.pv` | `7e17e0574c7577784f52de6fe45a489886b84d8a` | `79cf13133ae8933947117adaed7068729a97b076` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:4` | yes |
| `capstone_d.pv` | `5ea1082c8fedb09b7698e76d608fd557b4ae5bd7` | `527ff7e35d9cda12377046295bd2c24e4bd34f92` | BF-5/BF-6 hunks only (+53/-2) | rc=0 `:7` | yes |

The eleven rows marked **no** are the owner instance's disposition: they are not re-run under this
blob. Their staged files exist so that the derivation stays total. `cap_cc07i_d` is one of them, so
BF-7 is exercised in ladder 3 by `cap_cc07i_a` and `cap_cc07i_b` only.

## 3. Smoke test: `capstone.pv`, case (a)

This ran on wam-nuc, one run at a time, under `ulimit -v 10485760; nice -n 19; timeout 1800`, from
`smoke/run1.sh`. The log is `smoke/smoke.log`.

| file | rc | seconds | peak RSS | RESULT lines |
|---|---|---|---|---|
| `capstone.pv` (blob `35d8c702…`) | 0 | 225 | 0.34 GiB | 47 |

Ladder 2's `capstone.pv` took 487 s on ubuntu24 (`../ladder.log`). The machines differ, so the two times
are not comparable.

**Verdicts.** `diff <(grep ^RESULT ../capstone.out) <(grep ^RESULT smoke/capstone.out)` is **empty**. All
47 RESULT lines are byte-identical to ladder 2's, so **no verdict moved**: every correct-form query has
the same polarity, and every witness is reachable. **What did change is the traces of the two standing
witnesses**, which BF-6 forces onto wrapped layers:

- `HonestStandingEstablished`: `smoke/capstone.out:9138` `is false` (REACHABLE). The trace's standing
  report is `estCh (aid_7, L1, pk(skI2), …)` (`:9130`), preceded by `EstablishedWrapped(aid_7, L1, …)`
  (`:9128`). The `L0` frame is an `OT_WRAPPER` `wrap()` frame (`:9116`). At `L1`, the frame slot is an
  adversary term `a_16`, which is not a wrapper, so descent stops there. `skI2`'s honest `OT_ATTEST`
  signature over `M1` is in the signature slot (`:9118`). The standing path pins `sg`, `t` and `ppf`,
  and not `fb` (E2), so this is the registered structural join. In ladder 2 the trace was at `L0`
  (`../capstone.out:9059`).
- `HonestWrappedStandingAgreed`: `smoke/capstone.out:9804` `is false` (REACHABLE). The goal event is
  `HonestWrappedStandingAgreed(aid_7, L1)` (`:9800`). In ladder 2 it was `(aid_7, L0)`
  (`../capstone.out:9576`).

BF-5 does not change the correct model's C-Q6 verdicts in (a). Conjunct 1 (all three forms), conjunct 2
and conjunct 3 are green, as before. That is expected: a green over every layer stays green over the
innermost one.

**`cap_cc07i_a.pv` was NOT smoke-tested.** Ladder 2 ran it in 12 423 s (3.45 h) at 5.6 GB peak
(`../ladder.log`, `cap_cc07i_a rc=0 seconds=12423 peakRSSkB=5570084`). That is far beyond this test's
30-minute limit. The run that counts is ladder 3's. Its file is checked here by the derivation check above
only.

## 4. Finding-2 probe, adapted to the repaired model (BF-5)

The probes are **not ladder results and not registered queries**. `probes/mk_probes.py` applies the
reviewer's edits (`dev/codex/scratch/capstone_d_noninnermost_attest.pv` against ladder-2 `capstone_d.pv`)
to the staged models:

- a private `probeFrameCh`;
- `SUnwrap` additionally reports `(aid, lyrOut, fbIA)`;
- `ProbeJudge` fires `ProbeNonInnermostStanding(a, l)` iff the frame at `(a, l)` is an `OT_WRAPPER`
  `wrap()` frame whose inner frame is `OT_ATTEST`, **and** the standing path sent its ESTABLISHED report
  for `(a, l)` on `estCh`;
- the query list is replaced by that probe plus five positive controls.

Each probe ran under the same limits as §3.

| Probe | Model | rc / s | `ProbeNonInnermostStanding` | `EstablishedWrapped` at `L1` / `L2` | `HonestWrappedStandingAgreed` at `L1` / `L2` | `HonestStandingEstablished` |
|---|---|---|---|---|---|---|
| `probe_d_noninnermost_attest_l3` | staged `capstone_d.pv` (BF-5/6) | 0 / 147 | **`is true` — UNREACHABLE** (`smoke/probe_d.out:2588`) | reachable / reachable (`:3119`, `:3705`) | reachable / reachable (`:4505`, `:5417`) | reachable (`:6034`) |
| `probe_a_noninnermost_attest_l3` | staged `capstone.pv` (BF-5/6) | 0 / 22 | **`is true` — UNREACHABLE** (`smoke/probe_a.out:2591`) | reachable / reachable (`:3101`, `:3666`) | reachable / reachable (`:4332`, `:5066`) | reachable (`:5588`) |
| `probe_a_noninnermost_attest_L2CONTROL` | **unrepaired** ladder-2 `capstone.pv` | 0 / 22 | `is false`, REACHABLE (`smoke/probe_a_L2control.out:3117`) | reachable / reachable | reachable / reachable | reachable |
| the reviewer's `capstone_d_noninnermost_attest` | **unrepaired** ladder-2 `capstone_d.pv` | — | REACHABLE (`dev/codex/scratch/capstone_d_noninnermost_attest.out:3020`) | — | — | — |

**Reading.** In both modes, after BF-5, standing **cannot** be established at a layer whose frame is
itself a wrapper. The same probe on the unrepaired model finds that state in both (a) and (d). Honest
standing at the innermost layer stays reachable at **both** wrapped depths (`L1`, `L2`). `EstablishedWrapped`
also stays reachable at both (it is reachable with an adversarial core as well; that is not a property
claim, only that the event is not dead). **The repair removes the intermediate-wrapper reports and nothing
the registration defines.**

## 5. One-sentence confirmation, for the BF-5 entry

*"Confirmed by probe on the repaired model: the reviewer's intermediate-wrapper state is unreachable in
(a) and (d) (`ladder3-staging/smoke/probe_a.out:2591`, `probe_d.out:2588`), where the same probe on the
unrepaired model reaches it (`probe_a_L2control.out:3117`; the reviewer's `:3020`), while honest wrapped
standing stays reachable at `L1` and `L2`; the correct model's 47 verdicts in (a) are unchanged
(`smoke/capstone.out`)."*

## 6. Finding 1 (C-C15(i)'s accepting-key join): verdict (R), a registration conflict. Not repaired.

The full routed text is in `RESULTS-L3-ADDITIONS.md` §5. In brief:

**The two sentences.**

- **(1)** `PREDICTIONS.md:786-791`: *"`kX` — the accepting key, `LayerAccepted`'s own name for it. For
  C-Q6 it is the **innermost accepting key**: the `kI` of S-P7's `InnerCheck`, not the wrapper's `kW`"*.
  It is joined by the immutable `kX = kI` (`:1005-1009`, `:1019`).
- **(2)** C-C15(i)'s cell (`:2503`): the inner signature is *"verified under `kW` instead of `kI`"*, the
  inner acceptance *"reports the **presented inner** `(kW, tI, ppfI)`"*, and *"the standing path's own
  extraction is untouched and reports `(kX, id) = (kI, idI)`"*. Conjunct 3 is predicted red **because**
  `(kA, idA) = (kW, idW) ≠ (kI, idI) = (kX, id)`.

Under (i) the key that accepts is `kW` and the standing key is the presented `kI`. Sentence (1) needs
them to be the same argument; sentence (2) predicts a red from their differing.

**Why (R) and not (E).** Only three encodings could make the standing key equal the accepting key, and
each breaks a registered sentence:

- the standing path reads the envelope's key, which (E1) forbids;
- the companion re-keys the standing path to `kW`, which breaks sentence (2)'s "untouched" and its
  conjunct-3 rationale;
- the inner signature is verified under `kI`, which is no longer Q6b. That shape is configuration (iii).

The current files keep the **term** equality: both paths take the one intake's presented `kI`. In Q6b,
`InnerCheck`'s `kI` is a presented, unused input (`s-p7/proverif/sp7_q6b_companion_key_outermost.pv:181-198`).
What the files cannot also satisfy is sentence (1)'s "accepting key". `derive.py:cc15i` is therefore
**unchanged**. Configurations (ii) and (iii) do not change the inner verification key, so the conflict is
confined to (i).
