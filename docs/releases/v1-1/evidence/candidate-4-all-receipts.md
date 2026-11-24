# Candidate 4: every production receipt verifies under its trust file (steward, 2026-11-24)

Trust file: candidate 4's service/verifier/release/v1-1/trust.json, wrapped in a TEST release record only so the CLI runs (service/verifier tessera-verify --mode test). All 9 COMPLETE receipts fetched read-only from the results bucket by digest name; contents not recorded (client data).

```
2252a577077bd4debecd4fae503e0977a32facf1a15e172193a33f3a3300ba90  12 headers
4b9766c7542205895354bd4295d700edfba5f11b7676efebb58e85cb85e06f55  12 headers
e3b0425dba4e3cb3a4eb4058bdd78d8f37098fb737303291895980aadc5aa343  12 headers
948d3e46902bde59b0ea63e9a5a0a872b2d7dea38adb719e6cf1787fcc1a8d94  12 headers
aca4dfb2c8abb3b2d970ee9d9ab10a5438704845a19e89e9d64f84e647ed9f83  12 headers
ed68dc28f75e9f9a0a4ba90959ec6ecd24ccf075e589e80b553dd6837563dc8d  12 headers
48523ed5a3bb5d54497f54dbbc8ad3c2df9a79f62acacb0e8ae0a186f4c343ca  12 headers
78b987d9f4b5fe1f637a8e73cedcd6bf72982ae9cb75545180d9e2a2c7af7708  12 headers
d7e94b579aa997e3ab25c691f0e5ae291a82654586f1eee501c403b6ac093916  12 headers
exit 0 VALID_STRICT OK 2026-11-23T14:23:10Z 
exit 0 VALID_STRICT OK 2026-11-22T16:18:48Z 
exit 0 VALID_STRICT OK 2026-11-17T14:19:47Z 
exit 0 VALID_STRICT OK 2026-11-21T15:27:42Z 
exit 0 VALID_STRICT OK 2026-11-16T14:35:57Z 
exit 0 VALID_STRICT OK 2026-11-17T02:52:26Z 
exit 0 VALID_STRICT OK 2026-11-20T14:17:33Z 
exit 0 VALID_STRICT OK 2026-11-18T14:05:21Z 
exit 0 VALID_STRICT OK 2026-11-19T15:12:56Z 
```
