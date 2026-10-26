#!/usr/bin/env python3
"""Check a gpgv binary against every case.  Usage: python3 -I run.py /path/to/gpgv"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: run.py /path/to/gpgv")
    gpgv = sys.argv[1]
    os.makedirs(os.path.join(HERE, "work"), exist_ok=True)
    home = subprocess.run(["mktemp", "-d", os.path.join(HERE, "work", "rungpgv.XXXXXX")],
                          check=True, capture_output=True, text=True).stdout.strip()
    ver = subprocess.run([gpgv, "--version"], capture_output=True, text=True).stdout.splitlines()[:1]
    print("gpgv:", gpgv, ver)
    bad = 0
    cdir = os.path.join(HERE, "cases")
    for cid in sorted(os.listdir(cdir)):
        d = os.path.join(cdir, cid)
        e = json.load(open(os.path.join(d, "expected.json")))
        r = subprocess.run([gpgv, "--homedir", home, "--keyring", os.path.join(d, e["keyring"]),
                            os.path.join(d, e["signature"]), os.path.join(d, e["archive"])],
                           capture_output=True, text=True)
        ok = (r.returncode == 0) if e["gpgv_exit"] == "0" else (r.returncode != 0)
        bad += not ok
        print("%-8s %-40s exit=%d expected=%s accept=%s"
              % ("match" if ok else "MISMATCH", cid, r.returncode, e["gpgv_exit"], e["accept"]))
    print("%d/%d match" % (len(os.listdir(cdir)) - bad, len(os.listdir(cdir))))
    sys.exit(1 if bad else 0)


main()
