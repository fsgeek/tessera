"""Test session setup: the per-installation record (install.json) configures the SHA-1DC hook, as at run time.
Done at import so it precedes test-module imports that read sha1dc.available(). Without install.json the tests fail
here rather than silently running without the detector."""
from tessera_verify import install_record

install_record.load_and_apply()
