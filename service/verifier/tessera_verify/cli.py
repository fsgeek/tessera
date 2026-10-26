"""tessera-verify: the V1 service verifier command line (profile 3.5, 15.9).

  tessera-verify --trust TRUST --bundle BUNDLE [--catalog CATALOG] [--request strict]      (production, the default)
  tessera-verify --mode test --test-release R --test-release-key K --trust TRUST --bundle BUNDLE   (explicit TEST path)
  tessera-verify --previous PRIOR_TRUST --next NEXT_TRUST                                   (release checker, EA-12)

After a successful startup it prints exactly one canonical JSON object {"stable": <six fields>, "utc_assessment": ...}.
INVALID and UNVERIFIABLE are ordinary verdicts (exit 0). A startup or I/O refusal exits 2 with the code on stderr
and no verdict on stdout. There is no network access.
"""
import argparse
import sys
from pathlib import Path
from . import install_record, release_auth, release_constants
from .codec import Fault, demand, jcs, shahex
from .policy import check_extension, parse_catalog, parse_trust
from .verify import verify_bundle


def check_release(previous, nxt):
    try:
        p = Path(previous).read_bytes(); n = Path(nxt).read_bytes()
        check_extension(parse_trust(p), parse_trust(n), p)
        return 'ACCEPT'
    except (Fault, OSError):
        return 'REJECT'


def run(args):
    if args.previous or args.next:
        demand(bool(args.previous and args.next) and not args.bundle, 'USAGE')
        print(check_release(args.previous, args.next)); return 0
    demand(bool(args.trust and args.bundle), 'USAGE')
    release_auth.authenticate(args.mode, args.test_release, args.test_release_key)
    record_hash = install_record.load_and_apply(args.install_record)
    if args.diagnostics: print('install.json sha256: ' + record_hash, file=sys.stderr)
    trust = Path(args.trust).read_bytes()
    demand(release_constants.TRUST_SHA256 is not None and shahex(trust) == release_constants.TRUST_SHA256, 'TRUST_CONFIG_UNAUTHENTICATED')
    config = parse_trust(trust)
    catalog_raw = Path(args.catalog).read_bytes() if args.catalog else release_constants.CATALOG_BYTES
    demand(catalog_raw is not None and shahex(catalog_raw) == release_constants.CATALOG_SHA256, 'CATALOG_UNAUTHENTICATED')
    catalog = parse_catalog(catalog_raw)
    with open(args.bundle, 'rb') as f: bundle = f.read(2**27 + 1)   # bound the read, not just the later parse
    result, assessment = verify_bundle(bundle, config, catalog, request=args.request, utc=True)
    # Stable six under `stable` (EA-03); utc_assessment beside it, never inside it (profile 3.4, 7.4).
    print(jcs({'stable': result, 'utc_assessment': assessment}).decode())
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog='tessera-verify', description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--trust'); ap.add_argument('--bundle'); ap.add_argument('--catalog')
    ap.add_argument('--request', default='strict')
    ap.add_argument('--mode', choices=('production', 'test'), default='production')
    ap.add_argument('--test-release'); ap.add_argument('--test-release-key')
    ap.add_argument('--install-record', help='path of install.json (default: beside the package, or $TESSERA_VERIFY_INSTALL_JSON)')
    ap.add_argument('--diagnostics', action='store_true', help='report the install.json SHA-256 on stderr')
    ap.add_argument('--previous'); ap.add_argument('--next')
    args = ap.parse_args(argv)
    try: return run(args)
    except Fault as e: print(e.code, file=sys.stderr); return 2
    except OSError as e: print('INPUT_IO_ERROR: ' + str(e), file=sys.stderr); return 2


if __name__ == '__main__':
    raise SystemExit(main())
