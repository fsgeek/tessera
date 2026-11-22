"""D5 includes every verifier codec Fault code a signer can forward (both signers pass codec faults through)."""
import pathlib
import re

import tessera_verify.codec as codec

from tessera_watch import watcher


def test_every_codec_fault_code_alarms_under_d5():
    src = pathlib.Path(codec.__file__).read_text()
    codes = (set(re.findall(r"Fault\('([A-Z_]+)'\)", src)) | set(re.findall(r"demand\([^\n]*?,\s*'([A-Z_]+)'\)", src))
             | set(re.findall(r"code\s*=\s*'([A-Z_]+)'", src)))
    assert codes and codes <= watcher.D5_REASONS, sorted(codes - watcher.D5_REASONS)
