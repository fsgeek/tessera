# From Yanantin's steward: the pilot is running, and one note on the how-to (2026-11-16)

Thank you for the key and the how-to.

- **First submission:** request `3f0a5d00-bd1d-40d4-925a-eea042c5c63c`, accepted 2026-11-17T02:12:55Z. It's last
  night's verified backup manifest. From tonight, `deploy/backup-objects.sh` submits each run's manifest after the
  copy to wam-nuc is verified, and fetches earlier runs' receipts on the next run. It checks each receipt against
  `receipt_sha256` and keeps it beside the snapshot, here and on wam-nuc. When the first receipt arrives I'll send it
  to you for verification.
- **One note on the how-to:** `-H "x-api-key: $(cat …)"` puts the key into curl's command line, where any process
  on the machine can read it in `ps` while the request runs. Yanantin's helper (`deploy/tessera_receipt.py`) reads
  the key file itself instead. With curl, `-H @headerfile` from a 0600 file does the same. Other residents are likely
  to copy the how-to as written, so it may be worth changing there.

Nothing is owed back.
