# Disposition (owner, 2026-10-13)
- F1 HIGH: accepted. Make the root check existential and order-independent; add a bad-first/good-second control in both trust-list orders.
- F2 HIGH: accepted. Owner decision, now in A9.5: a KSK's reliance period = signing period end + the maximum validity of the root DNSKEY RRSIGs it made, recorded with its source. KSK-2017: signing end 2026-10-11 (IANA), maximum validity taken from the archived captures' observed RRSIG windows, cited. The 23:59:59 end-of-day cutoff is withdrawn. Add an honest old-root/new-leaf fixture anchored after retirement and before expiry.
- F3, F4, F5, F6 MEDIUM: accepted as proposed.
- F7 MEDIUM: accepted. Exercise the fixed path and DNS equality in the step-11 tests.
- F8 LOW: accepted. Label new decisions in V1-PROFILE as OWNER DECISION 2026-10-13, not extraction.
- Five decisions: 1, 2 and 4 retained; 3 retained with the F1/F3 repairs; 5 replaced per F2.
- "Decisions A9 does not settle", items 1–7: label each in the profile as an OWNER profile decision or OPEN, per Codex's classification.
