# Pre-freeze trust-configuration values (profile 14.2 item 3), sourced 2026-10-19

Sources and hashes: `MANIFEST.md`. The profile was not edited. "Profile" means docs/V1-PROFILE.md section 5 and
prototype/e2e/trustcfg.py POLICY (the PROPOSED values).

## DNSKEY RDATA (RFC 4034 2.2: flags 257, protocol 3, algorithm 8, key)

Source: root-anchors.xml (p7s verified, see MANIFEST), `<Flags>257</Flags>`, `<Algorithm>8</Algorithm>`, `<PublicKey>`;
RDATA = 0x0101 || 0x03 || 0x08 || base64-decode(PublicKey). Computed here; key tag per RFC 4034 App. B and
SHA-256 DS digest (over 0x00 || RDATA) both reproduce the XML's `KeyTag` and `Digest`.

| Key | Tag | DS SHA-256 (XML `Digest`, matches computed) | RDATA base64 |
|---|---|---|---|
| KSK-2017 (id Klajeyz) | 20326 | E06D44B80B8F1D39A95C0B0D7C65D08458E880409BBC683457104237C7F8EC8D | AQEDCAMBAAGs/7QJvMk5+DH3oeXsiPelklXsUwQL5DICc5Ckzoltb5CG88Xhd/v+EYFjqux68UYsR5RZRMTiwCa+Xpi7ze0ll4Jy4ePgecUJTVc/DoPJLwKzLTUTsVULgmkpyA3Q+Syslm0Xdp/VhntkfD84Apq9xIFS648gcVnsxdIyx8FTfHn0t6wo/xFoLyFoG/bWq6VVAyv2+fA2vrKqpbN3jW7r+6a/nqGRvkqwyup1ni93Oh+QKcc+y41XNbkyHbCF8bji2AOP4pQZklSM7g1n3UVH4R3WOvnJ/BxUZvtoTPAJ1xl8LPeeeSq1AeaoocpRmvLLm19jZ+lMDUdQJFE1e+G1 |
| KSK-2024 (id Kmyv6jo) | 38696 | 683D2D0ACB8C9B712A1948B27F741219298D0A450D612C483AF444A4C0FB2B16 | AQEDCAMBAAGveo3rpJ2ZWnkq78gCY+mR79vIYTipMd6yxl1Wguq107A3OOPf3InZbaZMhsAiTZzgJRTShdowaLGQVOXnh7KWkFjpjhJWbIyAjEDAt2nh2xokob2bMeMDGEox/Hu1a4W7uoq8As1QQKREo21HaVlphJ4WrYVrtY6PrIhVIkQAMZvasiTYP8Dmaqsy/3S/6vD5HEVOaFChKVIHu9TN3o9v+wj6qXVcLjKE76AfmTk+GHhssTLx5m68ZRcxjhzoo7czfrtU0DWrV9lwbs2TUNSvrNgl5DyGaO7OiYGcr2gXr2LcT72C8OM/Zkeytr2hdfFGB/WfRjVFHmsn3ygu9z2H |

Live cross-check (`raw/dig-root-dnskey-1.1.1.1.txt`, 2026-10-19T23:22:45Z): the root DNSKEY RRset from 1.1.1.1 has
three DNSKEYs (one ZSK, flags 256; two flags-257 KSKs). Both KSK public keys equal the XML PublicKey byte for byte
(KSK-2017 not yet revoked; flags still 257). The RRSIG over the set is by 38696 only, inception 20261011000000,
expiration 20261101000000. Caveat: 1.1.1.1 is an unauthenticated-channel resolver, not itself a primary source.

## Dates

| Value | Sourced value | Source file and quoted evidence | Profile PROPOSED | Differs? |
|---|---|---|---|---|
| KSK-2017 signing start | day 2018-10-11; time 16:00:00Z | raw/icann-summary-30-10-2018.html: "When 11 October arrived, we went through the operational plans step-by-step and at 1600 UTC, the KSK used to sign the root zone was changed to the new key that had been generated in 2017." Day: raw/iana-dnssec-files.html: "KSK-2017 ... Signed between 2018-10-11 and 2026-10-11." The blog does not name the key or tag; the identification "new key" = KSK-2017 rests on the day and on IANA's table. Both are operational accounts, not RRSIG inception evidence. | 2018-10-11T16:00:00Z | no |
| KSK-2017 signing end | day 2026-10-11 (no time of day) | iana-dnssec-files.html: "Rollover to KSK-2024 11 October 2026 KSK-2024 is now signing the zone; KSK-2017 is no longer signing the zone." and "Signed between 2018-10-11 and 2026-10-11." Time of day: not stated by any fetched primary source. Live RRSIG by 38696 has inception 2026-10-11T00:00:00Z (dig file), consistent with 00:00:00Z but that is RRSIG evidence, not an announced switch time. | 2026-10-11T00:00:00Z (policy) | no (time of day unsourced) |
| KSK-2024 signing start | day 2026-10-11; time unstated | iana-dnssec-files.html: "KSK-2024 Active ... Signing since 2026-10-11." icann-completed-2026-10-15.html: "the scheduled rollover of the cryptographic key ... was completed on 11 October 2026." Live RRSIG inception 20261011000000. | 2026-10-11T00:00:00Z (policy) | no (time of day unsourced) |
| KSK-2017 publication | 2017-07-11 | raw/icann-ksk-rollover-2018.html: "July 11 2017: Publication of new KSK in DNS." (trust-anchor validFrom in root-anchors.xml is 2017-02-02T00:00:00Z, a different event: when IANA began listing it.) | 2017-08-11T00:00:00Z (trustcfg.py POLICY and root-ksks.json; not stated in the profile prose) | YES: one month earlier |
| KSK-2024 publication | 2025-01-11 | iana-dnssec-files.html: "Publication of KSK-2024 11 January 2025 KSK-2024 was introduced in the DNS root zone." icann-blog-prep-27jul26.html: "the new key was first published in the root zone on 11 January 2025." (XML validFrom 2024-07-18 is the trust-anchor listing date.) | none (null, "informational, left unsourced") | new value available |
| KSK-2017 revocation | 2027-01-11 (scheduled, future) | iana-dnssec-files.html: "Revocation of KSK-2017 11 January 2027 KSK-2017 is scheduled to be published in the root zone with the REVOKE bit set, allowing resolvers that follow RFC 5011 to revoke it as a trust anchor." Removal "22 March 2027". icann-completed-2026-10-15.html: "the scheduled revocation of the previous KSK in January 2027." | 2027-01-11 | no. It is a schedule, not an event; today is 2026-10-19. |
| Reliance lifetime L | 21 days = 1814400 s | Not an announcement. Live RRSIG: inception 20261011000000, expiration 20261101000000 (dig file) = 21 d. Profile's 2026-10-09 KSK-2017 sample is in the repo capture, not re-fetched. Remains "observed", not a maximum. | 1814400 | no |
| KSK-2017 reliance end | 2026-11-01T00:00:00Z | derived (signing end + L); no primary source states it | 2026-11-01T00:00:00Z | no |
| KSK-2024 signing end / reliance | open | IANA table lists no end ("Active") | null | no |

## Not sourced to a primary document

- Time of day of the KSK-2017 signing end and KSK-2024 signing start (sources give the day only).
- That the 1600 UTC 2018 sentence concerns KSK-2017 by name (the ICANN blog says "the new key ... generated in 2017"; IANA's table supplies the key name and day).
- L is observed RRSIG validity, not a published policy value.
- The ICANN CA used to verify the p7s was fetched over the same channel (no independent bootstrap).
- The 2017 and 2024 IANA ceremony attestation PDFs were archived but yielded no extractable dates.
