"""Release bindings (profile 15.9 R2). Machine-independent facts only.

In a source tree this file is UNPROVISIONED: every binding is None, so a production run refuses with
TRUST_CONFIG_UNAUTHENTICATED. A production release's generated copy sets NAMESPACE = "PRODUCTION" and the three
hashes/bytes of its trust configuration and catalog. TEST provisioning never edits this file; it sets the bindings in
memory for one process (release_auth.provision).

Facts about one installation (the interpreter's unicodedata file hash, the SHA-1DC binary) are NOT here: they are in
the per-installation install.json, outside the signed archive (R2, "No machine-specific facts in the signed archive").
"""
NAMESPACE = None          # "PRODUCTION" or "TEST"
TRUST_SHA256 = None
CATALOG_SHA256 = None
CATALOG_BYTES = None      # the exact frozen catalog bytes (catalog.json)
UNICODE_VERSION = '16.0.0'
