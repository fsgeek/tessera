"""Per-installation record install.json (profile 15.9 R2). Written by install.sh, outside the signed archive,
unsigned, no authority. The verifier checks it at start: Python 3.14, Unicode 16.0.0, the interpreter's unicodedata
file hash as recorded at install time, and the SHA-1DC binary. Its SHA-256 is reported as a diagnostic."""
import hashlib
import json
import os
import sys
import unicodedata
from pathlib import Path
from . import release_constants, sha1dc
from .codec import Fault, demand

ENV = 'TESSERA_VERIFY_INSTALL_JSON'
FIELDS = {'format', 'python', 'unicode_version', 'unicode_module_sha256', 'sha1dc_upstream_commit',
          'sha1dc_binary', 'sha1dc_binary_sha256'}


def default_path():
    return Path(os.environ.get(ENV) or Path(__file__).resolve().parent.parent / 'install.json')


def unicode_module_sha256():
    return hashlib.sha256(Path(getattr(unicodedata, '__file__', sys.executable)).read_bytes()).hexdigest()


def current_facts(sha1dc_binary, sha1dc_binary_sha256):
    return {'format': 'tessera-v1-install/1', 'python': '%d.%d' % sys.version_info[:2],
            'unicode_version': unicodedata.unidata_version, 'unicode_module_sha256': unicode_module_sha256(),
            'sha1dc_upstream_commit': sha1dc.UPSTREAM_COMMIT, 'sha1dc_binary': str(sha1dc_binary),
            'sha1dc_binary_sha256': sha1dc_binary_sha256}


def check_runtime():
    demand(sys.version_info[:2] == (3, 14), 'RUNTIME_UNSUPPORTED')
    demand(unicodedata.unidata_version == release_constants.UNICODE_VERSION, 'UNICODE_TABLES_UNSUPPORTED')


def load_and_apply(path=None):
    """Check the runtime against install.json and configure the SHA-1DC hook. Returns the record's SHA-256."""
    path = Path(path) if path else default_path()
    check_runtime()
    try:
        raw = path.read_bytes(); rec = json.loads(raw)
    except (OSError, ValueError):
        raise Fault('INSTALL_RECORD_MISSING') from None
    demand(isinstance(rec, dict) and set(rec) == FIELDS and rec['format'] == 'tessera-v1-install/1', 'INSTALL_RECORD_INVALID')
    demand(rec['python'] == '3.14' and rec['unicode_version'] == release_constants.UNICODE_VERSION, 'RUNTIME_UNSUPPORTED')
    demand(rec['unicode_module_sha256'] == unicode_module_sha256(), 'UNICODE_TABLES_UNSUPPORTED')
    demand(rec['sha1dc_upstream_commit'] == sha1dc.UPSTREAM_COMMIT, 'INSTALL_RECORD_INVALID')
    sha1dc.configure(rec['sha1dc_binary'], rec['sha1dc_binary_sha256'])
    demand(sha1dc.functional(), 'SHA1DC_UNAVAILABLE')   # missing or non-functional detector: startup refusal (15.9 R2)
    return hashlib.sha256(raw).hexdigest()
