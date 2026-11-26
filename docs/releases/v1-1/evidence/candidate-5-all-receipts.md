# Candidate 5: every production receipt checked under its trust file (steward, 2026-11-26)

Trust file: candidate 5's service/verifier/release/v1-1/trust.json (sha256 3ef97f19…0e69a176), wrapped in a TEST release record only so the CLI runs (service/verifier tessera-verify --mode test). All 12 COMPLETE receipts (DynamoDB lstate = COMPLETE) fetched read-only from the results bucket by digest name; each file's SHA-256 equals its name; contents not recorded (client data).

Expected before the run: 11 VALID_STRICT; 301a4bb7 (anchored at 977690 on 2026-11-26, not pinned: tip 977695 < h+10) UNVERIFIABLE / HEADERS_NOT_COVERED.

```
2252a577077bd4debecd4fae503e0977a32facf1a15e172193a33f3a3300ba90 exit 0 VALID_STRICT OK 2026-11-23T14:23:10Z 
301a4bb7c612471d77d25da7877e48885401f29268baed7d1bf342b2aadf1045 exit 0 UNVERIFIABLE HEADERS_NOT_COVERED  
48523ed5a3bb5d54497f54dbbc8ad3c2df9a79f62acacb0e8ae0a186f4c343ca exit 0 VALID_STRICT OK 2026-11-20T14:17:33Z 
4b9766c7542205895354bd4295d700edfba5f11b7676efebb58e85cb85e06f55 exit 0 VALID_STRICT OK 2026-11-22T16:18:48Z 
5e8439d27d99adf095ad0ba3859943869da68bc2a33f7773309a30999fa754ca exit 0 VALID_STRICT OK 2026-11-25T15:44:40Z 
78b987d9f4b5fe1f637a8e73cedcd6bf72982ae9cb75545180d9e2a2c7af7708 exit 0 VALID_STRICT OK 2026-11-18T14:05:21Z 
948d3e46902bde59b0ea63e9a5a0a872b2d7dea38adb719e6cf1787fcc1a8d94 exit 0 VALID_STRICT OK 2026-11-21T15:27:42Z 
aca4dfb2c8abb3b2d970ee9d9ab10a5438704845a19e89e9d64f84e647ed9f83 exit 0 VALID_STRICT OK 2026-11-16T14:35:57Z 
b0889e18cfef8d79092534bdfed94898b2f59cad6023f784cdda09894dfc0aa8 exit 0 VALID_STRICT OK 2026-11-24T14:18:35Z 
d7e94b579aa997e3ab25c691f0e5ae291a82654586f1eee501c403b6ac093916 exit 0 VALID_STRICT OK 2026-11-19T15:12:56Z 
e3b0425dba4e3cb3a4eb4058bdd78d8f37098fb737303291895980aadc5aa343 exit 0 VALID_STRICT OK 2026-11-17T14:19:47Z 
ed68dc28f75e9f9a0a4ba90959ec6ecd24ccf075e589e80b553dd6837563dc8d exit 0 VALID_STRICT OK 2026-11-17T02:52:26Z 
```
