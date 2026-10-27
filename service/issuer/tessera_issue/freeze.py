"""The frozen objects the receipts bind (the frozen objects directory of the freeze record), read as data and checked against the frozen
catalog before any use. Nothing here is parsed as policy except the catalog, with the verifier's own parser."""
import json
from dataclasses import dataclass
from pathlib import Path

from tessera_verify.policy import parse_catalog

from .util import sha256hex

FILES = ("spec.bin", "vectors.bin", "preamble.bin", "dependency-manifest.json", "catalog.json")


class FreezeError(Exception):
    pass


@dataclass
class Frozen:
    spec: bytes
    vectors: bytes
    preamble: bytes
    dependency_manifest: bytes
    catalog_bytes: bytes
    catalog: dict                 # the flat catalog object

    @property
    def parsed_catalog(self):
        return parse_catalog(self.catalog_bytes)


def load(objects_dir):
    d = Path(objects_dir)
    raw = {n: (d / n).read_bytes() for n in FILES}
    parse_catalog(raw["catalog.json"])          # closed, canonical, the frozen constants
    cat = json.loads(raw["catalog.json"])
    want = {"spec.bin": cat["spec_sha256"], "vectors.bin": cat["vectors_sha256"],
            "preamble.bin": cat["preamble_sha256"], "dependency-manifest.json": cat["dependency_manifest_sha256"]}
    for n, h in want.items():
        if sha256hex(raw[n]) != h:
            raise FreezeError(f"{n} does not hash to its catalog value")
    return Frozen(raw["spec.bin"], raw["vectors.bin"], raw["preamble.bin"], raw["dependency-manifest.json"],
                  raw["catalog.json"], cat)
