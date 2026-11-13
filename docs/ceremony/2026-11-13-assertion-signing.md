# Key-assertion signing, 2026-11-13 (record)

The author signed the window's key-assertion commit with YubiKey A (repository root `6BDA…D30A`) on the Pangolin
under Tails, following `ASSERTION-SHEET.md` at commit `1601c08` (payload SHA-256 `4f0c54ee…dbfe4cbd`; window
`2026-11-15T00:00:00Z` to `2027-02-01T00:00:00Z`; kms `a33c216e…`, gpg `6a2d7e75…`).

**Deviation, and why.** `sign-assertion.sh` passed its session and form checks (the author saw `FORM OK, TREE
MATCH` with the right keys and dates), then failed at the card check: `the card is not YubiKey A (card holds '')`.
Cause: in a fresh keyring only a plain `gpg --card-status` links the card's key; the script read the card with
`--with-colons` and hid the error. The author removed the check and reran; signing then failed with `no secret key`
(same cause). The author finished by hand, as the owner instructed: import `root.pub.asc` into the shell's keyring,
`gpg --card-status`, detached-sign `payload.txt` (PIN and touch), verify, copy to OUT. OUT reached the NUC via the
author's Windows desktop over ssh (public data). Integrity does not rest on that path: the owner's assembly verified
the signature over the exact payload under the pinned root key.

**Result (owner, NUC).** `key_assertion.py assemble`: PASS. Commit **`aad530edb510734056b10ab9ba1107fae1f2e3e2`**,
signed by the repository root; path, rule-O signature and SHA-1DC checked with the verifier's code.
`payload.sig.asc` SHA-256 `5aeca57d…`, `commit.bin` `76fcf080…`. OpenTimestamps proof `git-stamp.txt.ots` submitted
2026-11-13 ~19:27Z (pending).

**Script fixed** for later sessions: a plain `gpg --card-status` (with retries) before the fingerprint check.

**DNS (author, Cloudflare, 2026-11-13).** The TEST record (spike keys, window ended 2026-10-26) was replaced. Owner's
check: exactly one TXT at `_tessera-v1.wamason.com` on the authoritative server (`kanye.ns.cloudflare.com`) and at
1.1.1.1 and 8.8.8.8, TTL 300; 255 bytes equal to `value.txt`, the value the root signed; DNSSEC fully validated
(`ad` flag; `delv`: fully validated).

**Anchored (owner, 2026-11-13 20:58Z).** `git-stamp.txt.ots` upgraded: BitcoinBlockHeaderAttestation(975705), merkle
root `e0f27ef1…080e6886`, equal to blockstream.info and mempool.space; tip 975712 at check, 8 confirmations (k = 6
met).
