"""Explicit local instrument provisioning; does not authenticate/sign a release."""
import argparse
import unicodedata
import sys
from pathlib import Path
from codec import shahex,demand
from policy import parse_trust,parse_catalog,check_extension

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--trust',required=True); p.add_argument('--catalog',required=True)
    p.add_argument('--previous-trust'); args=p.parse_args()
    demand(unicodedata.unidata_version=='16.0.0','UNICODE_TABLES_UNSUPPORTED')
    unicode_hash=shahex(Path(getattr(unicodedata,'__file__',sys.executable)).read_bytes())
    trust=Path(args.trust).read_bytes(); catalog=Path(args.catalog).read_bytes()
    current=parse_trust(trust); parse_catalog(catalog)
    if args.previous_trust:
        prior=Path(args.previous_trust).read_bytes(); check_extension(parse_trust(prior),current,prior)
    content=(f'"""Local instrument release binding; no release-signature claim."""\n'
             f'TRUST_SHA256 = {shahex(trust)!r}\nCATALOG_SHA256 = {shahex(catalog)!r}\n'
             f'CATALOG_BYTES = {catalog!r}\nUNICODE_VERSION = "16.0.0"\nUNICODE_MODULE_SHA256 = {unicode_hash!r}\nSHA1DC_AVAILABLE = False\n')
    Path(__file__).with_name('release_constants.py').write_text(content)
    print('Bound local instrument inputs; release authentication remains external.')
if __name__=='__main__': main()
