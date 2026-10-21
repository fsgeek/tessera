# Trust-source archive (profile section 14.2 item 3)

All files fetched 2026-10-19 (UTC times below are file write times, within seconds of the fetch) with
`curl -L -A tessera-trust-sources`. Files in `raw/` are as served; no edits. The three IANA anchor files are
byte-identical to the earlier archive in `prototype/e2e/work/root-anchors/` (same sha256).

| File | URL | Fetched (UTC) | sha256 |
|---|---|---|---|
| root-anchors.xml | https://data.iana.org/root-anchors/root-anchors.xml | 2026-10-19T23:22:35Z | 3ccaab38830025ee0a0f6c1f25769427544f81ea2865aa860468f3ef5278b908 |
| root-anchors.p7s | https://data.iana.org/root-anchors/root-anchors.p7s | 2026-10-19T23:22:35Z | 644e0e22842c6b7a57fda13d286941fd7449a179f0a3763578fa9a251d307dd1 |
| icannbundle.pem | https://data.iana.org/root-anchors/icannbundle.pem | 2026-10-19T23:22:35Z | 18ce7215812d1a2cad8d9d4d3d7c26f7235a9b5ec6f0c1e214e15230fd4f9e24 |
| raw/iana-dnssec-files.html | https://www.iana.org/dnssec/files | 2026-10-19T23:21:59Z | f0893dc381b211b89fc23b0bd6f7b53c2204b7aca8c7396d95b5ccdcec6530a8 |
| raw/iana-dnssec.html | https://www.iana.org/dnssec | 2026-10-19T23:21:59Z | f9b1d9416e387807404d73c152d91f2c858e888f0767d31f2b5c7cc112119626 |
| raw/icann-ksk-rollover.html | https://www.icann.org/resources/pages/ksk-rollover-en | 2026-10-19T23:21:59Z | 78fe7e3e0c969134fe01a6eab9674213f5a8dd1c9416bdacf4b526af2bac6d3f |
| raw/icann-ksk-rollover-2018.html | https://www.icann.org/resources/pages/ksk-rollover-2018-en | 2026-10-19T23:22:05Z | 4441835c2b28c7bed9464a1f4c91eb02c21881e8c07f68d3a51a6b25d1ae4e7b |
| raw/icann-ksk-rollover-2024.html | https://www.icann.org/resources/pages/ksk-rollover-2024-08-23-en | 2026-10-19T23:22:05Z | 72911162f121393552ced6a46a85cd3b5fdcedd1483cd29359f5b2c502618a7e |
| raw/icann-completed-2026-10-15.html | https://www.icann.org/en/announcements/details/icann-reports-root-zone-ksk-rollover-completed-as-planned-15-10-2026-en | 2026-10-19T23:22:04Z | 63420c4dff45ab190c3ebd960f680309aa615734b7adca44201dd09022b0e92e |
| raw/icann-blog-prep-27jul26.html | https://www.icann.org/en/blogs/details/preparing-for-the-root-zone-ksk-rollover-what-you-need-to-know-27-07-2026-en | 2026-10-19T23:22:06Z | 6018e6cbb9b9f315524a139965a4f44d837a61e26e3e24aa47b825ac8b4f1415 |
| raw/icann-expect-27jul26.pdf | https://www.icann.org/en/system/files/files/ksk-rollover-expect-27jul26-en.pdf | 2026-10-19T23:22:05Z | 5dd14182f1036314be666e58472d5aeca8a788bb2d2bc69fb3957d1aaabcad1d |
| raw/icann-faq-22may26.pdf | https://www.icann.org/en/system/files/files/root-zone-ksk-rollover-faq-22may26-en.pdf | 2026-10-19T23:22:05Z | 4cfb0a4211f62fd74ced929df699cb96015aae07ca9dfe4ad1167c7150e981fb |
| raw/icann-summary-30-10-2018.html | https://www.icann.org/en/blogs/details/the-recent-ksk-rollover-summary-and-next-steps-30-10-2018-en | 2026-10-19T23:22:25Z | 2025918ecb25dacf72d3b99d2f44d34a19ebac1225d44cbfdfa3cd4107760e0d |
| raw/iana-root-ksk-2017.pdf | https://www.iana.org/reports/2017/root-ksk-2017.pdf (ceremony attestation; no extractable dates used) | 2026-10-19T23:22:26Z | 7d6f82d8e809de30c9eccff655c5ed347fb06654b463d4e55ca30368a4b5be66 |
| raw/iana-root-ksk-2024.pdf | https://www.iana.org/reports/2024/root-ksk-2024.pdf (ceremony attestation; no extractable dates used) | 2026-10-19T23:22:27Z | ead86fdd9c0b02686bc3b6ad77e4e407d149838d89eb76fe549e75a861de2278 |
| raw/rfc4034.txt | https://www.rfc-editor.org/rfc/rfc4034.txt | 2026-10-19T23:22:28Z | 6c32963b76808ec4e5f1282b5e13c5216df4670d21e1590bf29af4066f49b355 |
| raw/rfc5011.txt | https://www.rfc-editor.org/rfc/rfc5011.txt | 2026-10-19T23:22:27Z | e00a848ca0fb6da1925ea828ea893a746f4d02528d70fedaab44b447c0778ed1 |
| raw/rfc9718.txt | https://www.rfc-editor.org/rfc/rfc9718.txt | 2026-10-19T23:22:28Z | 6b52bed66d8d7f26a2b4701d644a22c5d080666cd58509afcac409e1034fc475 |
| raw/dig-root-dnskey-1.1.1.1.txt | `dig . DNSKEY @1.1.1.1 +dnssec +noall +answer` (live resolver output, not a fetched document) | 2026-10-19T23:22:45Z | 4084d7d2a087a8e958594ea6918abc0cceeece4152bb7891efd540b1d15db0d1 |

## Signature verification of root-anchors.xml

`openssl cms -verify -binary -inform DER -in root-anchors.p7s -content root-anchors.xml -CAfile icannbundle.pem -out /dev/null`
(OpenSSL 3.0.13) prints `CMS Verification successful`. Signer: O=ICANN, CN=DNSSEC Trust Anchor Verification,
issued by ICANN Root CA. Without `-binary` verification FAILS (S/MIME line-ending canonicalisation of the
detached content); `-binary` is required. Limit: icannbundle.pem came over the same HTTPS channel, so this is
not an independent bootstrap of the ICANN CA (profile section 5 "recorded bootstrap procedure" remains
unmet by this check). The raw/ html pages are TLS-fetched only, with no signature.
