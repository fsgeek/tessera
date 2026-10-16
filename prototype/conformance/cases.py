#!/usr/bin/env python3
"""Generate the V1 conformance cases into prototype/conformance/cases/<ID>/.

Each case directory holds:
  bundle.json   the bundle bytes (or bundle.recipe.json + base.json for the >2^27-byte cases; run.py materializes)
  trust.json    the trust configuration presented with --trust
  release.json  the TEST release that "compiles in" one trust-config hash and the catalog (see REPORT.md)
  expected.json the six stable fields (top level) plus `_meta` (citations, derivation, ambiguity ids)
  request.txt   only where the request is not `strict` (L-06)
Release-checker cases (L-53..L-56 checker half) hold previous.json / next.json and an expected checker result.

Citations are `docs/V1-PROFILE.md` line numbers ("P:nnn") as of 2026-10-14, and RES §L case ids.
Run:  prototype/.venv/bin/python prototype/conformance/cases.py [--only ID,ID]
"""
import base64
import copy
import hashlib
import json
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import issue as I  # noqa: E402
import tcrypto as tc  # noqa: E402
import universe as U  # noqa: E402
from tcrypto import gen  # noqa: E402

OUT = HERE / "cases"
HB = 900000
TB = U.ts("2026-11-10T12:00:00Z")
DAY, HOUR = 86400, 3600
DELTA, EPS = U.DELTA, U.EPS
CASES = []

STABLE = {"revocation": "NOT_EVALUATED", "historical_security": "NOT_EVALUATED",
          "standing": "ABSENT/NOT_ISSUED_IN_PROFILE"}


def case(cid, group, title, verdict=None, reason=None, T="auto", cite=(), why="", amb=(), amb_fields=(),
         detail=None, refusal=None, request=None, kind="bundle", installation=None, isolation=None, alt=None,
         owner_decision=None):
    """installation: None (the classical universe, as for every pre-2026-10-14 case) or "classical" / "hybrid"
    (written to _meta; "hybrid" also writes catalog.json). isolation: authority-isolation metadata (_meta).
    alt: the outcome under the alternative reading of an ambiguity (_meta.alternative)."""
    def deco(fn):
        CASES.append(dict(id=cid, group=group, title=title, verdict=verdict, reason=reason, T=T, cite=list(cite),
                          why=why, amb=list(amb), amb_fields=list(amb_fields), detail=detail, refusal=refusal,
                          request=request, kind=kind, fn=fn, installation=installation, isolation=isolation,
                          alt=alt, owner_decision=owner_decision))
        return fn
    return deco


# ----------------------------------------------------------------------------------------------- helpers
def b64(b):
    return base64.b64encode(b).decode()


def rebuild(c):
    c.bundle = U.jcs(c.container)
    return c


def layer(c):
    return c.container["layers"][0] if hasattr(c, "container") else c.layer


def hk(**hooks):
    return hooks


def plan_set(name, **attrs):
    def f(c):
        g = c.plan.g[name]
        for k, v in attrs.items():
            setattr(g, k, v(c) if callable(v) else v)
    return f


def sig(key, inc, exp, **kw):
    return U.Sig(key, inc, exp, **kw)


def zk():
    return I.zone_keys()


def resign(slot, **kw):
    """sign hook: replace one slot's receipt signature (before A_sig is built and stamped)."""
    def f(c):
        key = c.kms if slot == "kms" else c.gpg
        F = c.F_kms if slot == "kms" else c.F_gpg
        s = tc.pgp_sign(F, key, c.sig_time, **kw)
        setattr(c, "S_" + slot, s)
    return f


def sp(t, data, crit=False, form="shortest"):
    return tc.subpacket(t, data, crit, form)


def gnu_h(c, key=None, t=None):
    key = key or c.gpg
    return tc.gnupg_hashed(key, c.sig_time if t is None else t)


def ct(c):
    return struct.pack(">I", c.sig_time)


def rt(t):
    return U.rfc3339(t)


# ======================================================================================== A9.1 scenario rows
@case("A-a", "A9.1 mapping", "Honest receipt as shipped (cases a, g)", "VALID_STRICT", "OK",
      cite=["P:951", "P:281-294"], why="Honest issue path; every required check passes; T = nTime(h_receipt).")
def _(): return I.issue()


@case("A-e", "A9.1 mapping", "Case e: a's bytes; slot-B key revoked out of band inside (declared, anchor]",
      "VALID_STRICT", "OK", cite=["P:957", "P:284"],
      why="Revocation is not evaluated (revocation: NOT_EVALUATED); the bundle bytes are a's.")
def _(): return I.issue()


@case("A-e2", "A9.1 mapping", "Case e': slot-B key revoked before declared (out of band)", "VALID_STRICT", "OK",
      cite=["P:957", "P:284"], why="As e.")
def _(): return I.issue()


@case("A-f", "A9.1 mapping", "Case f: impostor's content through the honest service", "VALID_STRICT", "OK",
      cite=["P:958"], why="The receipt attests no submitter; content is arbitrary V.")
def _(): return I.issue(content={"TEST": "impostor claims authorship of this text", "author": "not-the-submitter"})


def _contract(bad):
    a, b = U.Keys.p256("party-a"), U.Keys.p256("party-b")
    text = "TEST contract: party A sells party B one TEST widget."
    h = hashlib.sha256(text.encode()).digest()
    sa, sb = a.sign_digest(h), b.sign_digest(h)
    if bad:
        sb = (sb[0], (sb[1] + 1) % U.gen.N)
    return {"contract": text, "signatures": [
        {"party": "A", "pub": a.point.hex(), "rs": f"{sa[0]:064x}{sa[1]:064x}"},
        {"party": "B", "pub": b.point.hex(), "rs": f"{sb[0]:064x}{sb[1]:064x}"}]}


@case("A-i", "A9.1 mapping", "Case i: content = a contract plus two valid party signatures", "VALID_STRICT", "OK",
      cite=["P:960"], why="Honest issue; Tessera does not read content.")
def _(): return I.issue(content=_contract(False))


@case("A-i2", "A9.1 mapping", "Case i': as i, one party signature does not verify", "VALID_STRICT", "OK",
      cite=["P:961"], why="Tessera does not read content; the receipt is valid.")
def _(): return I.issue(content=_contract(True))


def _honest_value(c):
    k, g = U.Keys.p256("kms-signer"), U.Keys.p256("gpg-signer", 1790000000)
    c.value = gen.dns_value(k.fp_kms.split(":")[1], g.fp_gpg.split(":")[1], c.window[1], c.window[0]).encode()


@case("A-b", "A9.1 mapping", "Case b: reattribution under attacker keys, honest DNS and git evidence",
      "INVALID", "DNS_KEY_MISMATCH", cite=["P:952", "P:1393", "P:684-691"], amb=["EA-27"],
      why="Attacker re-signs the content with its own keys and manifest; both channels publish the honest keys. "
          "Row 15.1 fails (kms slot); no earlier row fails (keys, possession and signatures are the attacker's own "
          "and consistent). M5 / row 15.1 -> DNS_KEY_MISMATCH.")
def _(): return I.issue(kms_seed="attacker-kms", gpg_seed="attacker-gpg", adversarial=True,
                        hooks=hk(value=_honest_value))


@case("A-d3", "A9.1 mapping", "Case d3 / L-17: clone with one key (both slots) and one channel (git absent)",
      "INVALID", "DNS_KEY_MISMATCH", cite=["P:956", "P:263", "RES L-17"], amb=["EA-27"],
      why="One attacker key fills both slots; DNS publishes the honest keys (row 15.1 INVALID); git absent "
          "(row 2.2 UNVERIFIABLE MEMBER_MISSING:git). INVALID dominates UNVERIFIABLE (P:263); reported reason is "
          "the first failed row (P:1333-1335).")
def _():
    def drop_git(c):
        del layer(c)["git"]
    return I.issue(kms_seed="attacker-single", gpg_seed="attacker-single", adversarial=True,
                   hooks=hk(value=_honest_value, container=drop_git))


# ======================================================================================== container / dispatch
def _honest_bytes():
    return I.issue().bundle


@case("L-01", "dispatch", "Non-JSON bytes", "UNVERIFIABLE", "OUT_OF_PROFILE", T=None,
      cite=["P:209-210", "P:1345", "RES L-01"], amb=["EA-05"], amb_fields=["T"],
      why="D1: not strict JSON -> OUT_OF_PROFILE, terminal; nothing else evaluated, so T is null (EA-05).")
def _(): return {"bundle": b"TEST: this is not a JSON text\n"}


@case("L-01b", "dispatch", "Duplicate top-level member names (ENC 1.4 check 4)", "UNVERIFIABLE", "OUT_OF_PROFILE",
      T=None, cite=["P:209-210", "ENC 1.4 check 4"], amb=["EA-05"], amb_fields=["T"], why="D1 runs ENC 1.4 checks 1-5.")
def _():
    b = _honest_bytes()
    return {"bundle": b.replace(b',"profile":"tessera-v1-strict"}', b',"profile":"tessera-v1-strict","profile":"tessera-v1-strict"}')}


@case("L-01c", "dispatch", "UTF-8 BOM before the container", "UNVERIFIABLE", "OUT_OF_PROFILE", T=None,
      cite=["P:209-210", "ENC 1.4 check 2"], amb=["EA-05"], amb_fields=["T"], why="BOM is JSON_SYNTAX in ENC 1.4 -> D1.")
def _(): return {"bundle": b"\xef\xbb\xbf" + _honest_bytes()}


@case("L-01d", "dispatch", "Invalid UTF-8 inside a string", "UNVERIFIABLE", "OUT_OF_PROFILE", T=None,
      cite=["P:209-210", "ENC 1.4 check 1"], amb=["EA-05"], amb_fields=["T"], why="ENC 1.4 check 1 -> D1.")
def _():
    c = I.issue()
    return {"bundle": c.bundle.replace(b'"policy_version":"tessera-v1-issue-policy/1"',
                                       b'"policy_version":"tessera-v1-issue-policy/\xc0\xaf"')}


@case("L-02", "dispatch", "Container over 2^27 bytes (valid JSON, padded)", "UNVERIFIABLE", "OUT_OF_PROFILE",
      T=None, cite=["P:209-210", "P:255-256", "RES L-02"], amb=["EA-05"], amb_fields=["T"],
      why="D1: exceeds 2^27 bytes. Materialized by run.py from base.json + recipe (134217729 bytes).")
def _(): return {"recipe": {"kind": "pad_layer", "target_size": (1 << 27) + 1}, "base": _honest_bytes()}


@case("L-02b", "dispatch", "Container of exactly 2^27 bytes (control: passes D1, then unknown member)",
      "INVALID", "CONTAINER_SCHEMA", cite=["P:209-210", "P:1135-1140", "P:186"],
      why="Exactly 2^27 does not exceed the cap; the padding member `zz_pad` is unnamed -> CONTAINER_SCHEMA "
          "(row 2.4). T is computed independently (rows 11.1-11.4).")
def _(): return {"recipe": {"kind": "pad_layer", "target_size": 1 << 27}, "base": _honest_bytes(),
                 "T": I.issue().T}


@case("L-03", "dispatch", "Top-level `profile` absent", "UNVERIFIABLE", "OUT_OF_PROFILE", T=None,
      cite=["P:211", "RES L-03"], amb=["EA-05"], amb_fields=["T"], why="D2.")
def _():
    c = I.issue()
    del c.container["profile"]
    return rebuild(c)


@case("L-03b", "dispatch", "Top-level `profile` = other label", "UNVERIFIABLE", "OUT_OF_PROFILE", T=None,
      cite=["P:204-205", "P:211"], amb=["EA-05"], amb_fields=["T"], why="D2.")
def _():
    c = I.issue()
    c.container["profile"] = "tessera-v2-strict"
    return rebuild(c)


@case("L-04", "dispatch", "Two layers (case c, two-layer transplant)", "UNVERIFIABLE", "OUT_OF_PROFILE", T=None,
      cite=["P:212", "P:953", "RES L-04"], amb=["EA-05"], amb_fields=["T"], why="D3: layers not an array of length 1.")
def _():
    c = I.issue()
    other = I.issue(content={"TEST": "a second receipt transplanted as a layer"})
    c.container["layers"] = [layer(c), layer(other)]
    return rebuild(c)


@case("L-04b", "dispatch", "Zero layers", "UNVERIFIABLE", "OUT_OF_PROFILE", T=None, cite=["P:212"], amb=["EA-05"], amb_fields=["T"],
      why="D3.")
def _():
    c = I.issue()
    c.container["layers"] = []
    return rebuild(c)


@case("L-05", "dispatch", "Renewal wrapper (case h)", "UNVERIFIABLE", "OUT_OF_PROFILE", T=None,
      cite=["P:206-207", "P:212", "P:959", "RES L-05"], amb=["EA-05", "EA-07"], amb_fields=["T"],
      why="D3. The profile defines no wrapper encoding; a wrapper is realized as a second (renewal) layer "
          "around the original (EA-07).")
def _():
    c = I.issue()
    renewal = {"renews": "layer-0", "ots": layer(c)["receipt_anchor"]["ots"], "TEST": "renewal wrapper"}
    c.container["layers"] = [layer(c), renewal]
    return rebuild(c)


@case("L-06", "dispatch", "Case d1: a's bundle under a degraded request", "UNVERIFIABLE", "OUT_OF_PROFILE",
      T=None, detail="REQUEST_UNSUPPORTED", request="degraded", cite=["P:213-215", "P:954", "P:967-968", "RES L-06"],
      amb=["EA-02", "EA-04", "EA-05"], amb_fields=["T"],
      why="D4: the request is a verifier input; any request other than strict is refused without evaluation.")
def _(): return I.issue()


@case("L-06s", "dispatch", "Case d1: the same bytes, strict request", "VALID_STRICT", "OK",
      cite=["P:954", "RES L-06"], why="Strict evaluation of a's bytes.")
def _(): return I.issue()


@case("L-07", "container", "Re-indented container", "INVALID", "JSON_NONCANONICAL",
      cite=["P:187-188", "P:1136-1137", "P:1346", "RES L-07"],
      why="Passes D1 (still strict JSON); row 2.1 fails. Rows 11.1-11.4 still determine T (P:1337-1338).")
def _():
    c = I.issue()
    c.bundle = json.dumps(c.container, indent=1, sort_keys=True).encode()
    return c


@case("L-08", "container", "Unknown member in the layer", "INVALID", "CONTAINER_SCHEMA",
      cite=["P:186", "P:1349", "RES L-08"], why="Unnamed member -> row 2.4.")
def _():
    c = I.issue()
    layer(c)["extension"] = "TEST"
    return rebuild(c)


@case("L-09", "container", "Case d2: `git` absent", "UNVERIFIABLE", "MEMBER_MISSING:git",
      cite=["P:175-181", "P:955", "P:1347", "RES L-09"],
      why="Row 2.2. Git-dependent rows (14.x, 15.2, chain order) are unperformable without reasons of their own.")
def _():
    c = I.issue()
    del layer(c)["git"]
    return rebuild(c)


@case("L-10", "container", "Nested `git.ots` absent", "UNVERIFIABLE", "MEMBER_MISSING:git.ots",
      cite=["P:175-182", "RES L-10"], why="Row 2.2, layer-relative dotted path.")
def _():
    c = I.issue()
    del layer(c)["git"]["ots"]
    return rebuild(c)


@case("L-11", "container", "`git.object_format` absent", "UNVERIFIABLE", "GIT_OBJECT_FORMAT_MISSING",
      cite=["P:176-177", "P:628-629", "RES L-11"], why="Row 2.2 exception for object_format.")
def _():
    c = I.issue()
    del layer(c)["git"]["object_format"]
    return rebuild(c)


@case("L-12", "container", "`git.object_format` = \"sha256\"", "UNVERIFIABLE", "GIT_OBJECT_FORMAT",
      cite=["P:182-184", "P:1348", "RES L-12"], why="Row 2.3: a present string other than sha1.")
def _():
    c = I.issue()
    layer(c)["git"]["object_format"] = "sha256"
    return rebuild(c)


def _extra_header_key(key):
    def f():
        c = I.issue()
        layer(c)["headers"][key] = c.chain.headers[HB + 24].hex()
        return rebuild(c)
    return f


case("L-13", "container", "Header height key \"01\"", "INVALID", "CONTAINER_SCHEMA",
     cite=["P:1213-1214", "P:1235", "P:1455", "P:828-829 (diff-1 F-3)", "RES L-13"],
     why="Height grammar 0|[1-9][0-9]* violated -> row 2.4. T [OWNER 2026-10-14, diff-1 F-3; was EA-06]: an entry "
         "failing row 2.4 is not a supplied header; it contributes CONTAINER_SCHEMA only, and rows 10.x/11.x/13.4/14.6 "
         "use the remaining (honest) entries, so T is the honest receipt T.")(_extra_header_key("01"))
case("L-14", "container", "Header height 4294967296", "INVALID", "CONTAINER_SCHEMA",
     cite=["P:1213-1214", "P:1455", "P:828-829 (diff-1 F-3)", "RES L-14"],
     why="Value above 4294967295 -> row 2.4; T from the remaining entries as L-13 [diff-1 F-3; was EA-06].")(
    _extra_header_key("4294967296"))


@case("L-15", "container", "`issuer_record` absent", "VALID_STRICT", "OK", cite=["P:178-179", "P:190-194", "RES L-15"],
      why="Absence of issuer_record is allowed and never affects the verdict.")
def _():
    c = I.issue()
    del layer(c)["issuer_record"]
    return rebuild(c)


@case("L-16", "container", "`issuer_record.policy_version` malformed", "INVALID", "CONTAINER_SCHEMA",
      cite=["P:179-180", "P:1155", "RES L-16"], why="Present issuer_record is schema-checked.")
def _():
    c = I.issue()
    layer(c)["issuer_record"]["policy_version"] = "tessera-v1-issue-policy/01"
    return rebuild(c)


@case("F03-a", "container", "`issuer_record: {}`", "INVALID", "CONTAINER_SCHEMA", cite=["P:179-180", "P:1139-1140"],
      why="Present issuer_record with absent internal fields -> CONTAINER_SCHEMA, not MEMBER_MISSING.")
def _():
    c = I.issue()
    layer(c)["issuer_record"] = {}
    return rebuild(c)


@case("F03-b", "container", "`keys: null`", "INVALID", "CONTAINER_SCHEMA", cite=["P:177-178", "P:1138-1139"],
      why="A present parent of the wrong type -> CONTAINER_SCHEMA; no missing descendants are synthesized.")
def _():
    c = I.issue()
    layer(c)["keys"] = None
    return rebuild(c)


@case("F03-c", "container", "`vectors` absent and `preamble` non-string", "INVALID", "CONTAINER_SCHEMA",
      cite=["P:179-181", "P:263"], why="Absence (UNVERIFIABLE) and schema (INVALID) collected independently; "
                                        "INVALID dominates.")
def _():
    c = I.issue()
    del layer(c)["vectors"]
    layer(c)["preamble"] = True
    return rebuild(c)


@case("F03-d", "container", "`git.object_format: null`", "INVALID", "CONTAINER_SCHEMA",
      cite=["P:184-185", "P:1139"], why="A present non-string object_format, null included, is a schema failure.")
def _():
    c = I.issue()
    layer(c)["git"]["object_format"] = None
    return rebuild(c)


@case("F03-e", "container", "`dns.ots` and `git.ots` both absent", "UNVERIFIABLE", "MEMBER_MISSING:dns.ots",
      cite=["P:181-182", "P:1347"], why="Several missing paths compared in JCS key order: dns.ots < git.ots.")
def _():
    c = I.issue()
    del layer(c)["dns"]["ots"]
    del layer(c)["git"]["ots"]
    return rebuild(c)


@case("F03-f", "container", "Base64 member with nonzero pad bits", "INVALID", "CONTAINER_SCHEMA",
      cite=["P:1134-1135"], why="Base64 must round-trip (no nonzero pad bits) -> row 2.4.")
def _():
    c = I.issue()
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    for m in ("preamble", "spec", "vectors", "dependency_manifest", "manifest", "a_sig"):
        v = layer(c)[m]
        if v.endswith("="):
            s = v.rstrip("=")
            s = s[:-1] + alphabet[alphabet.index(s[-1]) | 1]
            assert base64.b64decode(s + "=" * (len(v) - len(s))) == base64.b64decode(v)
            layer(c)[m] = s + "=" * (len(v) - len(s))
            c.mutated_member = m
            return rebuild(c)
    raise RuntimeError("no padded member")


@case("F03-g", "container", "A JSON number inside the container", "INVALID", "CONTAINER_SCHEMA",
      cite=["P:171", "P:1133-1134"], why="The container contains no JSON numbers.")
def _():
    c = I.issue()
    layer(c)["issuer_record"]["observed_anchor_delay_s"] = 1200
    return rebuild(c)


@case("F03-h", "container", "`receipt_anchor.txid` in uppercase hex", "INVALID", "CONTAINER_SCHEMA",
      cite=["P:1150"], why="txid is 64 lowercase hex.")
def _():
    c = I.issue()
    layer(c)["receipt_anchor"]["txid"] = layer(c)["receipt_anchor"]["txid"].upper()
    return rebuild(c)


@case("F03-i", "container", "`git.trees` with three elements", "INVALID", "CONTAINER_SCHEMA",
      cite=["P:1153"], why="trees is an array of exactly 2 strings.")
def _():
    c = I.issue()
    layer(c)["git"]["trees"].append(layer(c)["git"]["trees"][1])
    return rebuild(c)


@case("F03-j", "container", "`possession.kms` absent", "UNVERIFIABLE", "MEMBER_MISSING:possession.kms",
      cite=["P:175-182", "P:1148"], why="Required nested member absent beneath a correctly typed parent.")
def _():
    c = I.issue()
    del layer(c)["possession"]["kms"]
    return rebuild(c)


# ======================================================================================== constants / binding
@case("L-18", "binding forms", "binding_forms [\"STMT_DIGEST\"]", "UNVERIFIABLE", "BINDING_FORM_UNSUPPORTED",
      cite=["P:678-681", "P:1363", "RES L-18"], why="Row 8.5.")
def _(): return I.issue(binding_forms=["STMT_DIGEST"])


@case("L-19", "binding forms", "binding_forms [\"STMT_OTHER\"]", "UNVERIFIABLE", "BINDING_FORM_UNKNOWN",
      cite=["P:678-681", "RES L-19"], why="Row 8.5.")
def _(): return I.issue(binding_forms=["STMT_OTHER"])


@case("L-20", "binding forms", "binding_forms [\"STMT_DIGEST\",\"STMT_DIRECT\"]", "UNVERIFIABLE",
      "BINDING_FORM_UNSUPPORTED", cite=["P:678-681", "RES L-20"], why="First offending element.")
def _(): return I.issue(binding_forms=["STMT_DIGEST", "STMT_DIRECT"])


HYBRID_PLACEHOLDER = "TEST-HYBRID-MLDSA65-OPENPGP4-P256"


@case("L-21", "algorithm", "Branch-not-taken alg (hybrid pair id placeholder), rule-O signature bytes",
      "UNVERIFIABLE", "ALG_UNKNOWN", cite=["P:113-115", "P:117-123", "P:1358", "RES L-21"], amb=["EA-09"],
      why="Well-formed id other than the catalog id; codec-unknown (no supplement registered) -> opaque codec; "
          "signature and possession semantics unperformable; M5 alg contributes ALG_UNKNOWN, not SCHEMA.")
def _(): return I.issue(alg=HYBRID_PLACEHOLDER, adversarial=True)


def _opaque(n):
    def f(c):
        c.S_kms = tc.drbg("opaque-kms", n)
        c.S_gpg = tc.drbg("opaque-gpg", n)
    return f


@case("ALG-01", "algorithm", "Unknown-alg canary with opaque 300-byte signatures", "UNVERIFIABLE", "ALG_UNKNOWN",
      cite=["P:113-115", "P:220-222", "ENC 5.2:442"], why="Canary: unknown well-formed id is UNVERIFIABLE.")
def _():
    def poss(c):
        c.P_kms, c.P_gpg = tc.drbg("opaque-pk", 300), tc.drbg("opaque-pg", 300)
    return I.issue(alg="TEST-CANARY-ALG-X1", adversarial=True, hooks=hk(sign=_opaque(300), possession=poss))


@case("ALG-02", "algorithm", "Unknown alg with an empty kms signature (codec-invalid)", "INVALID", "SIG_EMPTY",
      cite=["P:1350", "ENC 5:388-389"], why="Opaque codec still rejects an empty signature (row 3.1).")
def _():
    def f(c):
        c.S_kms = b""
    return I.issue(alg="TEST-CANARY-ALG-X1", adversarial=True, hooks=hk(sign=f))


@case("ALG-03", "algorithm", "Unknown alg with a 65537-byte gpg signature (codec-invalid)", "INVALID",
      "LENGTH_CAP", cite=["P:1350", "ENC 5.2:442"], why="Opaque cap 65536 -> LENGTH_CAP at a_sig decoding.")
def _():
    def f(c):
        c.S_gpg = tc.drbg("big", 65537)
    return I.issue(alg="TEST-CANARY-ALG-X1", adversarial=True, hooks=hk(sign=f))


@case("ALG-04", "algorithm", "Frames carry an unknown alg; manifest carries the catalog alg", "INVALID",
      "RECEIPT_MANIFEST_MISMATCH", cite=["P:694-699", "P:1357", "P:121"],
      why="Row 6.3 (common alg != manifest alg) is checked for every syntactically valid id.")
def _(): return I.issue(alg="TEST-CANARY-ALG-X1", manifest_alg=U.ALG_V1, adversarial=True)


@case("ALG-05", "algorithm", "Frames carry the catalog alg; manifest carries an unknown alg", "INVALID",
      "RECEIPT_MANIFEST_MISMATCH", cite=["P:694-699", "P:1357"], why="Row 6.3.")
def _(): return I.issue(manifest_alg="TEST-CANARY-ALG-X1", adversarial=True)


OTHER_SPEC = U.part_object([("prototype/conformance/TEST-SPEC.txt", b"TEST ONLY. A different spec object.\n")])
OTHER_VEC = U.part_object([("prototype/conformance/TEST-VECTORS.txt", b"TEST ONLY. Different vectors.\n")])
OTHER_PRE = b"TEST ONLY. A different purpose preamble.\n"
OTHER_DEP = U.DEP_BYTES.replace(b'"edition":"TEST"', b'"edition":"TEST-2"', 1)


@case("L-22", "spec binding", "Wrong common.spec.id", "INVALID", "SPEC_ID", cite=["P:97", "P:1360", "RES L-22"],
      why="Row 8.2.")
def _(): return I.issue(spec_id="tessera-v1-strict/verification-spec/2", adversarial=True)


@case("L-23", "spec binding", "Unknown spec hash (self-consistent bundled spec)", "UNVERIFIABLE", "SPEC_UNKNOWN",
      cite=["P:97-98", "P:103-108", "P:1361", "RES L-23"],
      why="Row 8.3 unperformable; rows 8.4 and 17.4 blocked; 17.1-17.3 pass (bundled spec hashes to the signed value).")
def _(): return I.issue(spec_sha256=hashlib.sha256(OTHER_SPEC).hexdigest(), bundled_spec=OTHER_SPEC)


@case("F12-a", "spec binding", "Unknown spec plus altered bundled preamble", "INVALID", "BUNDLE_OBJECT_HASH",
      cite=["P:103-108", "P:1396"], why="17.3 is independent of the catalog lookup; INVALID dominates SPEC_UNKNOWN.")
def _(): return I.issue(spec_sha256=hashlib.sha256(OTHER_SPEC).hexdigest(), bundled_spec=OTHER_SPEC,
                        bundled_preamble=OTHER_PRE)


@case("F12-b", "spec binding", "Unknown spec plus unmatched dependency-manifest bytes", "UNVERIFIABLE",
      "SPEC_UNKNOWN", cite=["P:106-107", "P:906-907", "P:1397"],
      why="17.4 is blocked by 8.3 (never compared with an unrelated entry).")
def _(): return I.issue(spec_sha256=hashlib.sha256(OTHER_SPEC).hexdigest(), bundled_spec=OTHER_SPEC,
                        bundled_dep=OTHER_DEP)


@case("L-24", "spec binding", "Signed vectors_sha256 != catalog (bundled vectors self-consistent)", "INVALID",
      "SPEC_OBJECT_MISMATCH", cite=["P:98-99", "P:1362", "RES L-24"], why="Row 8.4.")
def _(): return I.issue(vectors_sha256=hashlib.sha256(OTHER_VEC).hexdigest(), bundled_vectors=OTHER_VEC,
                        adversarial=True)


@case("L-24b", "spec binding", "Signed preamble_sha256 != catalog", "INVALID", "SPEC_OBJECT_MISMATCH",
      cite=["P:98-99", "P:1362"], why="Row 8.4 (preamble).")
def _(): return I.issue(preamble_sha256=hashlib.sha256(OTHER_PRE).hexdigest(), bundled_preamble=OTHER_PRE,
                        adversarial=True)


@case("L-25", "spec binding", "Bundled preamble bytes altered", "INVALID", "BUNDLE_OBJECT_HASH",
      cite=["P:100-101", "P:1396", "RES L-25"], why="Row 17.3.")
def _(): return I.issue(bundled_preamble=OTHER_PRE)


@case("L-25b", "spec binding", "Bundled spec bytes altered", "INVALID", "BUNDLE_OBJECT_HASH",
      cite=["P:103-104", "P:1396"], why="Row 17.1 (lookup uses the signed hash, which is in the catalog).")
def _(): return I.issue(bundled_spec=OTHER_SPEC)


@case("L-25c", "spec binding", "Bundled dependency manifest altered", "INVALID", "BUNDLE_OBJECT_HASH",
      cite=["P:905-906", "P:1397"], why="Row 17.4.")
def _(): return I.issue(bundled_dep=OTHER_DEP)


@case("L-26", "pinned D", "issuer = other domain, git absent", "INVALID", "ISSUER_NOT_PINNED",
      cite=["P:647-650", "P:1359", "RES L-26"], why="Row 8.1; INVALID, not UNVERIFIABLE, even with git absent.")
def _():
    def drop(c):
        del layer(c)["git"]
    return I.issue(issuer="example.org", adversarial=True, hooks=hk(container=drop))


@case("L-26b", "pinned D", "issuer = other domain, all evidence present", "INVALID", "ISSUER_NOT_PINNED",
      cite=["P:647-650", "P:1359"], why="Row 8.1 precedes DNS_OWNER (13.6).")
def _(): return I.issue(issuer="example.org", adversarial=True)


# ======================================================================================== git time / chain order
@case("L-27", "chain order", "T_git = declared + 1 s (> declared), h_git + 5 < h_receipt", "VALID_STRICT", "OK",
      cite=["P:652-660", "RES L-27 (replacement)"], why="No clock comparison between T_git and declared.")
def _(): return I.issue(times={HB + 2: TB + 1})


@case("L-28", "chain order", "T_git > receipt T, h_git + 5 < h_receipt", "VALID_STRICT", "OK",
      cite=["P:652-660", "RES L-28 (replacement)"], why="Chain order, not clock order.")
def _(): return I.issue(times={HB + 2: TB + 20 * 60 + HOUR})


@case("L-29", "chain order", "h_git + 5 = h_receipt - 1 (r = g + 6)", "VALID_STRICT", "OK",
      cite=["P:655-656", "P:1392", "RES L-29"], why="h_git + 5 < h_receipt holds.")
def _(): return I.issue(h_git=HB + 18)


@case("L-30", "chain order", "h_git + 5 = h_receipt (r = g + 5)", "INVALID", "GIT_NOT_PRECOMMITTED",
      cite=["P:655-656", "P:1392", "RES L-30"], why="Row 14.8.")
def _(): return I.issue(h_git=HB + 19, adversarial=True)


@case("L-31", "chain order", "Codex F01 schedule: receipt h nTime 11:55, declared 12:00, git at j > h nTime 11:59",
      "INVALID", "GIT_NOT_PRECOMMITTED", cite=["P:655-656", "RES L-31"], why="Row 14.8; T = 11:55.")
def _(): return I.issue(h_git=HB + 26, times={HB + 24: TB - 300, HB + 26: TB - 60}, adversarial=True)


# ======================================================================================== time cluster
@case("L-32", "time", "Nonmonotone pair at c1: h1 < h2, nTime(h1) = declared - eps - 1, nTime(h2) = declared - eps",
      "INVALID", "TIME_BEFORE_DECLARED_EPSILON", cite=["P:713-718", "P:724-727", "RES L-32"],
      why="Lowest qualifying height selected (h1); c1 fails. T = nTime(h1).")
def _(): return I.issue(receipt_branches=[{"h": HB + 24}, {"h": HB + 30}],
                        times={HB + 24: TB - EPS - 1, HB + 30: TB - EPS}, adversarial=True)


@case("L-32r", "time", "Reverse pair: nTime(h1) = declared - eps, nTime(h2) = declared - eps - 1", "VALID_STRICT",
      "OK", cite=["P:713-718"], why="Lowest height selected, not least nTime; c1 holds at h1.")
def _(): return I.issue(receipt_branches=[{"h": HB + 24}, {"h": HB + 30}],
                        times={HB + 24: TB - EPS, HB + 30: TB - EPS - 1})


@case("L-33", "time", "Nonmonotone pair at c2: nTime(h1) = declared + delta + 1, nTime(h2) = declared + delta",
      "INVALID", "TIME_AFTER_DECLARED_DELTA", cite=["P:713-718", "P:720-722", "RES L-33"], why="c2 fails at h1.")
def _(): return I.issue(receipt_branches=[{"h": HB + 24}, {"h": HB + 30}],
                        times={HB + 24: TB + DELTA + 1, HB + 30: TB + DELTA}, adversarial=True)


@case("L-33r", "time", "Reverse pair at c2 boundary", "VALID_STRICT", "OK", cite=["P:720-722"],
      why="T = declared + delta passes (inclusive).")
def _(): return I.issue(receipt_branches=[{"h": HB + 24}, {"h": HB + 30}],
                        times={HB + 24: TB + DELTA, HB + 30: TB + DELTA + 1})


NA34 = TB + HOUR


@case("L-34", "time", "Nonmonotone pair at not-after: nTime(h1) = not-after + 1, nTime(h2) = not-after",
      "INVALID", "ISSUANCE_WINDOW", cite=["P:585-587", "P:713-718", "RES L-34"], why="Row 16.1 at T = nTime(h1).")
def _(): return I.issue(window=("2026-11-01T00:00:00Z", rt(NA34)), receipt_branches=[{"h": HB + 24}, {"h": HB + 30}],
                        times={HB + 24: NA34 + 1, HB + 30: NA34}, adversarial=True)


@case("L-34r", "time", "Reverse pair at not-after", "VALID_STRICT", "OK", cite=["P:585-587"],
      why="T = not-after passes (inclusive).")
def _(): return I.issue(window=("2026-11-01T00:00:00Z", rt(NA34)), receipt_branches=[{"h": HB + 24}, {"h": HB + 30}],
                        times={HB + 24: NA34, HB + 30: NA34 + 1})


@case("W-01", "time", "declared = issuance-not-before (inclusive)", "VALID_STRICT", "OK", cite=["P:585-587"],
      why="Both bounds inclusive.")
def _(): return I.issue(window=(rt(TB), rt(TB + 30 * DAY)))


@case("W-02", "time", "declared = issuance-not-before - 1 s", "INVALID", "ISSUANCE_WINDOW", cite=["P:585-587"],
      why="Row 16.1.")
def _(): return I.issue(window=(rt(TB + 1), rt(TB + 30 * DAY)), adversarial=True)


@case("L-35", "time", "Two qualifying attestations at the same height", "VALID_STRICT", "OK",
      cite=["P:724-727", "RES L-35"], why="Same height, same T.")
def _(): return I.issue(receipt_branches=[{"h": HB + 24}, {"h": HB + 24}])


@case("L-36", "time", "confirmed_at = declared + delta", "VALID_STRICT", "OK", cite=["P:728-731", "RES L-36"],
      why="c3 inclusive.")
def _(): return I.issue(times={HB + 29: TB + DELTA})


@case("L-36b", "time", "confirmed_at = declared + delta + 1", "INVALID", "CONFIRMATION_LATE",
      cite=["P:728-731", "RES L-36"], why="Row 12.3.")
def _(): return I.issue(times={HB + 29: TB + DELTA + 1}, adversarial=True)


@case("L-37", "time", "Fifth successor inside delta, sixth outside (h+6 header supplied)", "VALID_STRICT", "OK",
      cite=["P:728-729", "RES L-37"], why="confirmed_at = nTime(h* + 5).")
def _(): return I.issue(times={HB + 29: TB + DELTA, HB + 30: TB + DELTA + 1}, supply_extra=[HB + 30])


@case("L-38", "time", "confirmed_at < T (nonmonotone)", "VALID_STRICT", "OK", cite=["P:730-731", "RES L-38"],
      why="No monotonicity check.")
def _(): return I.issue(times={HB + 29: TB + 20 * 60 - HOUR})


@case("L-39", "time", "Qualifying branch plus an attestation at q > h with no headers", "VALID_STRICT", "OK",
      cite=["P:737-741", "RES L-39"], why="Nonqualifying attestation supplies no fact.")
def _(): return I.issue(receipt_branches=[{"h": HB + 24}, {"h": HB + 33, "headers": False}])


@case("L-40", "time", "Plus an attestation at q < h with partial pinned headers (q, q+1)", "VALID_STRICT", "OK",
      cite=["P:737-741", "P:774-775", "RES L-40"],
      why="q is nonqualifying (missing successors); lowest *qualifying* height is h; T = nTime(h).")
def _(): return I.issue(receipt_branches=[{"h": HB + 24}, {"h": HB + 21, "headers": [HB + 21, HB + 22]}])


@case("L-41", "time", "Plus an attestation at q whose supplied header is unpinned", "UNVERIFIABLE",
      "HEADERS_NOT_COVERED", cite=["P:487-489", "P:763-764", "P:1370", "RES L-41"], why="Row 10.2; T from h.")
def _(): return I.issue(receipt_branches=[{"h": HB + 24}, {"h": HB + 36, "headers": [HB + 36]}],
                        pins_exclude=[HB + 36])


@case("L-42", "time", "Plus a contradicted branch at q (pinned header, merkle != message)", "INVALID",
      "OTS_MERKLE_MISMATCH", T=None, cite=["P:742-743", "P:291-293", "P:1374", "RES L-42"],
      why="Row 11.3; a contradicted attestation makes T null (P:291-293).")
def _(): return I.issue(receipt_branches=[{"h": HB + 24}, {"h": HB + 33, "contradict": True, "headers": [HB + 33]}],
                        adversarial=True)


@case("L-43", "time", "Pending-only receipt proof", "UNVERIFIABLE", "ANCHOR_PENDING_ONLY", T=None,
      cite=["P:743-745", "P:1375", "RES L-43"], why="Row 11.4.")
def _(): return I.issue(receipt_branches=[{"kind": "pending"}], adversarial=True)


@case("L-43b", "time", "Bitcoin attestation without its headers", "UNVERIFIABLE", "HEADERS_MISSING", T=None,
      cite=["P:743-745", "P:1375"], why="Row 11.4.")
def _(): return I.issue(receipt_branches=[{"h": HB + 24, "headers": False}], adversarial=True)


@case("L-44", "time", "Holder-upgraded proof: original witness plus new branches without headers",
      "VALID_STRICT", "OK", cite=["P:737-741", "RES L-44"], why="Existential selection.")
def _(): return I.issue(receipt_branches=[{"h": HB + 24}, {"kind": "pending"}, {"h": HB + 34, "headers": False}])


@case("L-45", "time", "Missing intermediate height between supplied headers", "VALID_STRICT", "OK",
      cite=["P:771-772", "RES L-45"], why="Not a broken link.")
def _(): return I.issue(supply_extra=[HB + 31])


@case("L-46", "time", "Adjacent supplied pair with wrong prev (pinned)", "INVALID", "HEADER_CHAIN_BROKEN",
      cite=["P:771-772", "P:1371", "RES L-46"], why="Row 10.3 on unused, pinned headers.")
def _(): return I.issue(prev_override={HB + 33: b"\x00" * 32}, supply_extra=[HB + 32, HB + 33], adversarial=True)


@case("L-47", "time", "Supplied header at a pinned height with another hash", "INVALID", "HEADER_CONFLICTS_PIN",
      cite=["P:765-767", "P:1369", "RES L-47"], why="Row 10.1.")
def _():
    def alt(c):
        h = c.chain.headers[HB + 33]
        c.header_bytes[HB + 33] = h[:76] + struct.pack("<I", (struct.unpack("<I", h[76:])[0] + 1) & 0xFFFFFFFF)
    return I.issue(supply_extra=[HB + 33], adversarial=True, hooks=hk(pins=alt))


@case("L-48", "time", "h..h+5 segment crosses a 2016-block boundary (901152)", "VALID_STRICT", "OK",
      cite=["P:773-775", "RES L-48"], why="No retarget check.")
def _(): return I.issue(hb=901126)


@case("L-49", "time", "Receipt passes c3, snapshot fails c3", "INVALID", "SNAPSHOT_TIME",
      cite=["P:795-796", "P:1384", "RES L-49"], why="Row 13.7.")
def _(): return I.issue(times={HB + 17: TB + DELTA + 1}, adversarial=True)


@case("SNAP-c1", "time", "Snapshot T_snap = declared - eps - 1", "INVALID", "SNAPSHOT_TIME",
      cite=["P:781-783", "P:795-796"], why="Row 13.7, c1.")
def _(): return I.issue(times={HB + 12: TB - EPS - 1}, adversarial=True)


@case("SNAP-c1b", "time", "Snapshot T_snap = declared - eps (boundary)", "VALID_STRICT", "OK",
      cite=["P:781-783"], why="Inclusive.")
def _(): return I.issue(times={HB + 12: TB - EPS})


@case("SNAP-c2", "time", "Snapshot T_snap = declared + delta + 1", "INVALID", "SNAPSHOT_TIME",
      cite=["P:781-783", "P:795-796"], why="Row 13.7, c2.")
def _(): return I.issue(times={HB + 12: TB + DELTA + 1}, adversarial=True)


# ======================================================================================== trust configuration
def _refusal(trust_bytes, release, bundle, **extra):
    d = {"bundle": bundle, "trust_bytes": trust_bytes, "release": release}
    d.update(extra)
    return d


@case("L-50", "trust config", "Config hash not compiled into the release", refusal="TRUST_CONFIG_UNAUTHENTICATED",
      cite=["P:365-366", "RES L-50"], why="Startup refusal, no verdict.")
def _():
    c = I.issue()
    other = copy.deepcopy(c.trust)
    other["as_of"] = "2026-12-30T00:00:00Z"
    return _refusal(c.trust_bytes, U.make_release(U.jcs(other)), c.bundle)


@case("L-50b", "trust config", "Compiled config that fails the 15.5 schema (root_ksks unsorted)",
      refusal="TRUST_CONFIG_UNAUTHENTICATED", cite=["P:365-366", "P:1291-1295"], why="Schema failure is a refusal.")
def _():
    c = I.issue()
    t = copy.deepcopy(c.trust)
    t["root_ksks"] = list(reversed(t["root_ksks"]))
    tb = U.jcs(t)
    return _refusal(tb, U.make_release(tb), c.bundle)


@case("L-50c", "trust config", "Compiled config whose repository key is not a valid P-256 point",
      refusal="TRUST_CONFIG_UNAUTHENTICATED", cite=["P:858-861"], why="Public-key validity of a config key.")
def _():
    c = I.issue()
    t = copy.deepcopy(c.trust)
    body = bytearray(base64.b64decode(t["repository_keys"][0]["key"]))
    body[-1] ^= 1
    t["repository_keys"][0]["key"] = b64(bytes(body))
    tb = U.jcs(t)
    return _refusal(tb, U.make_release(tb), c.bundle)


@case("L-50d", "trust config", "Compiled config containing a JSON number", refusal="TRUST_CONFIG_UNAUTHENTICATED",
      cite=["P:1283", "P:1287-1288"], why="No numbers.")
def _():
    c = I.issue()
    t = copy.deepcopy(c.trust)
    t["version"] = 1
    tb = U.jcs(t)
    return _refusal(tb, U.make_release(tb), c.bundle)


def _attacker_config(c):
    t = copy.deepcopy(c.trust)
    evil = U.zkey("attacker-root-KSK", 13, 257)
    t["root_ksks"].append(U.ksk_entry("ATTACKER-KSK", evil, "2026-10-12T00:00:00Z", None))
    t["root_ksks"].sort(key=lambda e: (U.ts(e["signing_start"]), int(e["key_tag"]),
                                       base64.b64decode(e["dnskey_rdata"])))
    t["repository_keys"].append(U.repo_entry(U.Keys.p256("attacker-repo"), start="2026-10-02T00:00:00Z"))
    t["header_pins"]["999999"] = "11" * 32
    t["version"], t["previous_sha256"] = "2", hashlib.sha256(c.trust_bytes).hexdigest()
    return U.jcs(t)


@case("L-51", "trust config", "Captured repository signer signs a config (own KSK, repository key, pins)",
      refusal="TRUST_CONFIG_UNAUTHENTICATED", cite=["P:372-373", "P:357-364", "RES L-51"],
      why="Release signed by the repository key, not the release key: the config hash is not compiled in by an "
          "authentic release. The config is a superset of the honest one, so a verifier that skipped "
          "authentication would return VALID_STRICT.")
def _():
    c = I.issue()
    tb = _attacker_config(c)
    return _refusal(tb, U.make_release(tb, signer=c.repo), c.bundle)


@case("L-52a", "trust config", "Captured DNS credential (wamason.com ZSK) signs a config",
      refusal="TRUST_CONFIG_UNAUTHENTICATED", cite=["P:372-373", "RES L-52"], why="As L-51.")
def _():
    c = I.issue()
    tb = _attacker_config(c)
    return _refusal(tb, U.make_release(tb, signer=U.zkey("wamason-ZSK", 13, 256).priv), c.bundle)


@case("L-52b", "trust config", "Issuing AWS account (kms signer) signs a config",
      refusal="TRUST_CONFIG_UNAUTHENTICATED", cite=["P:372-373", "RES L-52"], why="As L-51.")
def _():
    c = I.issue()
    tb = _attacker_config(c)
    return _refusal(tb, U.make_release(tb, signer=c.kms), c.bundle)


# ---- release checker (not bundle cases) -----------------------------------------------------------------------
def _next(prev, mut):
    n = copy.deepcopy(prev)
    n["version"] = str(int(prev["version"]) + 1)
    n["previous_sha256"] = hashlib.sha256(U.jcs(prev)).hexdigest()
    mut(n)
    return n


def _rc(mut, result):
    prev = I.issue().trust
    return {"release_check": result, "previous": U.jcs(prev), "next": U.jcs(_next(prev, mut))}


def _ksk(n, name):
    return [e for e in n["root_ksks"] if e["name"] == name][0]


case("L-53", "release checker", "Changing L of a closed KSK", kind="release_check", refusal="REJECT",
     cite=["P:479-486", "RES L-53"], why="L of every existing entry is immutable.")(
    lambda: _rc(lambda n: _ksk(n, "TEST-KSK-A").update(reliance_lifetime_s="1900000"), "REJECT"))
case("L-54", "release checker", "Closing KSK-B so that its reliance end (end + L) < previous as_of",
     kind="release_check", refusal="REJECT", cite=["P:481-483", "RES L-54"], why="null -> end needs end + L >= as_of.")(
    lambda: _rc(lambda n: _ksk(n, "TEST-KSK-B").update(signing_end="2026-11-01T00:00:00Z"), "REJECT"))
case("L-54b", "release checker", "Closing the repository key below previous as_of", kind="release_check",
     refusal="REJECT", cite=["P:481-483"], why="Repository reliance end = signing_end.")(
    lambda: _rc(lambda n: n["repository_keys"][0].update(signing_end="2026-12-01T00:00:00Z"), "REJECT"))
case("L-54c", "release checker", "Closing KSK-B with end + L >= previous as_of (control)", kind="release_check",
     refusal="ACCEPT", cite=["P:481-483"], why="Allowed transition.")(
    lambda: _rc(lambda n: (_ksk(n, "TEST-KSK-B").update(signing_end="2026-12-15T00:00:00Z"),
                           n.update(as_of="2026-12-31T00:00:00Z")), "ACCEPT"))
case("L-55a", "release checker", "as_of decreasing", kind="release_check", refusal="REJECT",
     cite=["P:480", "RES L-55"], why="as_of nondecreasing.")(
    lambda: _rc(lambda n: n.update(as_of="2026-12-30T00:00:00Z"), "REJECT"))
case("L-55b", "release checker", "Existing pin hash changed", kind="release_check", refusal="REJECT",
     cite=["P:484", "RES L-55"], why="Existing pin hashes immutable.")(
    lambda: _rc(lambda n: n["header_pins"].update({str(HB): "22" * 32}), "REJECT"))
case("L-55c", "release checker", "Entry removed (KSK-A)", kind="release_check", refusal="REJECT",
     cite=["P:484", "RES L-55"], why="Nothing is removed.")(
    lambda: _rc(lambda n: n.update(root_ksks=[e for e in n["root_ksks"] if e["name"] != "TEST-KSK-A"]), "REJECT"))
case("L-56c", "release checker", "Pin append (new heights)", kind="release_check", refusal="ACCEPT",
     cite=["P:484-486", "RES L-56"], why="Appending pins is allowed.")(
    lambda: _rc(lambda n: n["header_pins"].update({str(HB + 100): "33" * 32}), "ACCEPT"))


@case("L-56a", "trust config", "Pin append, before: h* segment supplied but unpinned", "UNVERIFIABLE",
      "HEADERS_NOT_COVERED", cite=["P:484-486", "P:487-489", "RES L-56"],
      why="Under config v1 the h1 headers are unpinned (row 10.2); h2 qualifies, so T = nTime(h2).")
def _(): return I.issue(receipt_branches=[{"h": HB + 24}, {"h": HB + 30}], pins_exclude=range(HB + 24, HB + 30),
                        adversarial=True)


@case("L-56b", "trust config", "Pin append, after: the same bundle under the appended config", "VALID_STRICT",
      "OK", cite=["P:484-486", "RES L-56"], why="Appended pins make h1 qualify; T changes to nTime(h1).")
def _(): return I.issue(receipt_branches=[{"h": HB + 24}, {"h": HB + 30}])


@case("L-57", "trust config", "Snapshot after as_of under the open KSK-B", "UNVERIFIABLE", "TRUST_HORIZON",
      cite=["P:474-478", "P:434-437", "RES L-57"], why="Open entry, T_snap > as_of, no other usable entry.")
def _(): return I.issue(as_of="2026-11-06T00:00:00Z", adversarial=True)


@case("L-57b", "trust config", "Git T_git after as_of under the open repository key", "UNVERIFIABLE",
      "TRUST_HORIZON", cite=["P:474-478", "P:618-621", "P:1391"], why="Row 14.7 horizon class.")
def _(): return I.issue(as_of="2026-11-11T00:00:00Z", times={HB + 2: TB + 2 * DAY}, adversarial=True)


def _root_sigs(*sigs_fn):
    def f(c):
        c.plan.g["root"].sigs = [s(c) for s in sigs_fn]
    return f


A_LONG = lambda c: sig(U.ksk_a(), U.ts("2026-10-25T00:00:00Z"), U.ts("2026-11-30T00:00:00Z"), signer=".")  # noqa
A_PRE = lambda c: sig(U.ksk_a(), U.ts("2026-10-01T00:00:00Z"), U.ts("2026-10-22T00:00:00Z"), signer=".")  # noqa
B_STD = lambda c: sig(U.ksk_b(), c.root_inc, c.root_exp, signer=".")  # noqa


@case("L-57c", "trust config", "Mixed root: finalized KSK-A outside reliance + open KSK-B after as_of",
      "UNVERIFIABLE", "TRUST_HORIZON", cite=["P:429-438"], why="Horizon class precedes finalized interval failure.")
def _(): return I.issue(as_of="2026-11-06T00:00:00Z", adversarial=True, hooks=hk(dns_plan=_root_sigs(A_LONG, B_STD)))


@case("L-58", "trust config", "Presented root KSK-B with REVOKE set (signing with it)", "UNVERIFIABLE",
      "NO_TRUSTED_KSK_USABLE", cite=["P:455-457", "P:427-428", "RES L-58"],
      why="Byte equality excludes REVOKE-set RDATA; its key tag is not a configured KSK's; KSK-A does not sign.")
def _():
    def f(c):
        rv = U.ksk_b().rdata(flags=385)
        c.plan.g["root"].rdatas = [U.ksk_a().rdata(), rv, c.zk["rzsk"].rdata()]
        c.plan.g["root"].sigs = [sig(U.ksk_b(), c.root_inc, c.root_exp, signer=".", key_rdata=rv)]
    return I.issue(adversarial=True, hooks=hk(dns_plan=f))


@case("L-59", "trust config", "Presented root KSK-B RDATA differs from config (flags 256)", "UNVERIFIABLE",
      "NO_TRUSTED_KSK_USABLE", cite=["P:455-456", "RES L-59"], why="Not byte-equal; tag differs.")
def _():
    def f(c):
        rv = U.ksk_b().rdata(flags=256)
        c.plan.g["root"].rdatas = [U.ksk_a().rdata(), rv, c.zk["rzsk"].rdata()]
        c.plan.g["root"].sigs = [sig(U.ksk_b(), c.root_inc, c.root_exp, signer=".", key_rdata=rv)]
    return I.issue(adversarial=True, hooks=hk(dns_plan=f))


@case("L-60", "trust config", "Rollover control: KSK-A published but not signing", "VALID_STRICT", "OK",
      cite=["P:393-394", "RES L-60"], why="A published, non-signing trusted KSK is informational.")
def _(): return I.issue()


TB_OCT20 = "2026-10-20T12:00:00Z"


@case("L-61a", "trust config", "Failing trusted candidate (KSK-A, corrupt) sorted first, KSK-B validates",
      "VALID_STRICT", "OK", cite=["P:390-391", "P:394-395", "RES L-61"], amb=["EA-08"],
      why="Existential, order-independent. T_snap inside both reliance periods.")
def _():
    a_bad = lambda c: sig(U.ksk_a(), U.ts("2026-10-01T00:00:00Z"), U.ts("2026-10-22T00:00:00Z"), signer=".",  # noqa
                          corrupt=True)
    return I.issue(timebase=TB_OCT20, hooks=hk(dns_plan=_root_sigs(a_bad, B_STD)))


@case("L-61b", "trust config", "Failing trusted candidate (KSK-B, corrupt) sorted second, KSK-A validates",
      "VALID_STRICT", "OK", cite=["P:390-391", "P:394-395", "RES L-61"], amb=["EA-08"],
      why="Other order. KSK-A is within reliance at T_snap (Oct 20 < Nov 1).")
def _():
    b_bad = lambda c: sig(U.ksk_b(), c.root_inc, c.root_exp, signer=".", corrupt=True)  # noqa
    return I.issue(timebase=TB_OCT20, hooks=hk(dns_plan=_root_sigs(A_PRE, b_bad)))


@case("L-62a", "trust config", "Honest old root: KSK-A signed before retirement, anchored after, within reliance",
      "VALID_STRICT", "OK", cite=["P:383-391", "P:395-397", "RES L-62"], why="T_snap Oct 15 in [start, Nov 1].")
def _(): return I.issue(timebase="2026-10-15T12:00:00Z", hooks=hk(dns_plan=_root_sigs(A_PRE)))


@case("L-62b", "trust config", "Same old-root evidence (window Oct 1-22) anchored after reliance", "INVALID",
      "RRSIG_NOT_VALID_AT_EVAL_TIME", cite=["P:395-397", "P:429-440", "RES L-62"], amb=["EA-14"],
      why="Must not pass. The candidate verifies but its RRSIG window excludes T_snap (Nov 10): time class, which "
          "ranks before nothing else here.")
def _(): return I.issue(adversarial=True, hooks=hk(dns_plan=_root_sigs(A_PRE)))


@case("L-63", "trust config", "Retired KSK-A, RRSIG window valid, T_snap outside reliance", "INVALID",
      "KSK_OUTSIDE_RELIANCE_PERIOD", cite=["P:420-421", "P:432-438", "RES L-63"], why="Finalized interval failure.")
def _(): return I.issue(adversarial=True, hooks=hk(dns_plan=_root_sigs(A_LONG)))


def _f15(t_snap):
    tb = U.ts("2018-10-11T20:00:00Z")
    return I.issue(timebase=U.rfc3339(tb), times={HB + 12: t_snap}, adversarial=True,
                   repo_entries=[U.repo_entry(U.Keys.p256("repository-key", 1759276800), start="2018-01-01T00:00:00Z")],
                   hooks=hk(dns_plan=_root_sigs(lambda c: sig(U.ksk_a(), c.root_inc, c.root_exp, signer="."))))


case("F15-a", "trust config", "KSK-A policy signing_start boundary: T_snap = 2018-10-11T16:00:00Z", "VALID_STRICT",
     "OK", cite=["P:467-469"], why="Reliance interval includes its start.")(
    lambda: _f15(U.ts("2018-10-11T16:00:00Z")))
case("F15-b", "trust config", "KSK-A policy signing_start boundary: T_snap = 2018-10-11T15:59:59Z", "INVALID",
     "KSK_OUTSIDE_RELIANCE_PERIOD", cite=["P:467-469", "P:432-438"],
     why="Verifies, time-valid, finalized entry's reliance excludes T_snap.")(
    lambda: _f15(U.ts("2018-10-11T15:59:59Z")))


# ======================================================================================== DNSSEC
def _w_ds(*rds):
    def f(c):
        c.plan.g["w_ds"].rdatas = [r(c) for r in rds]
    return f


DS2_OK = lambda c: U.ds_rdata("wamason.com", c.zk["w_ksk"].rdata(), 2)  # noqa
DS4_OK = lambda c: U.ds_rdata("wamason.com", c.zk["w_ksk"].rdata(), 4)  # noqa
DS1_OK = lambda c: U.ds_rdata("wamason.com", c.zk["w_ksk"].rdata(), 1)  # noqa
DS2_BAD = lambda c: U.ds_rdata("wamason.com", c.zk["w_ksk"].rdata(), 2, digest=b"\x5a" * 32)  # noqa
DS4_BAD = lambda c: U.ds_rdata("wamason.com", c.zk["w_ksk"].rdata(), 4, digest=b"\x5a" * 48)  # noqa

case("L-64", "DNSSEC", "Mixed DS types 2 and 4, only type 4 matching", "VALID_STRICT", "OK",
     cite=["P:517-519", "RES L-64"], why="Some supported path validates.")(lambda: I.issue(hooks=hk(dns_plan=_w_ds(DS2_BAD, DS4_OK))))
case("L-65", "DNSSEC", "DS type 4 only, matching", "VALID_STRICT", "OK", cite=["P:517-519", "RES L-65"],
     why="SHA-384 supported.")(lambda: I.issue(hooks=hk(dns_plan=_w_ds(DS4_OK))))
case("L-66", "DNSSEC", "DS type 1 only (matching selectors)", "UNVERIFIABLE", "DNSSEC_ALGORITHM_UNSUPPORTED",
     cite=["P:540-544", "RES L-66"], why="Potentially usable unsupported path. TXT locally valid: parent-blocked, "
                                         "no reason of its own (row 4).")(
    lambda: I.issue(adversarial=True, hooks=hk(dns_plan=_w_ds(DS1_OK))))
case("L-67", "DNSSEC", "Supported nonmatching DS plus unsupported DS", "UNVERIFIABLE", "DNSSEC_ALGORITHM_UNSUPPORTED",
     cite=["P:540-544", "RES L-67"], why="Row 3 precedes row 5.")(
    lambda: I.issue(adversarial=True, hooks=hk(dns_plan=_w_ds(DS2_BAD, DS1_OK))))
case("L-68", "DNSSEC", "All DS supported (type 2), none matching", "INVALID", "DNSKEY_DS_MISMATCH",
     cite=["P:553", "RES L-68"], why="Row 5, no child DNSKEY matches a validated DS.")(
    lambda: I.issue(adversarial=True, hooks=hk(dns_plan=_w_ds(DS2_BAD))))
case("L-68b", "DNSSEC", "All DS supported (types 2 and 4), none matching", "INVALID", "DNSKEY_DS_MISMATCH",
     cite=["P:553"], why="As L-68.")(lambda: I.issue(adversarial=True, hooks=hk(dns_plan=_w_ds(DS2_BAD, DS4_BAD))))


def _txt_sigs(*fns):
    def f(c):
        c.plan.g["txt"].sigs = [fn(c) for fn in fns]
    return f


TXT_OK = lambda c: sig(c.zk["w_zsk"], c.inc, c.exp, signer="wamason.com")  # noqa
ED_STRAY = U.zkey("stray-ed25519", 15, 256)
ED_ZONE = U.zkey("wamason-ED25519", 15, 256)


case("L-69", "DNSSEC", "TXT: valid alg-13 RRSIG plus an alg-15 RRSIG", "VALID_STRICT", "OK",
     cite=["P:525", "RES L-69"], why="A supported path validates.")(
    lambda: I.issue(hooks=hk(dns_plan=_txt_sigs(TXT_OK, lambda c: sig(ED_STRAY, c.inc, c.exp, signer="wamason.com")))))


@case("L-70", "DNSSEC", "TXT signed only by an alg-15 key present in the zone's DNSKEY set", "UNVERIFIABLE",
      "DNSSEC_ALGORITHM_UNSUPPORTED", cite=["P:540-544", "P:564-566", "RES L-70"], why="Row 3.")
def _():
    def f(c):
        c.plan.g["w_dnskey"].rdatas.append(ED_ZONE.rdata())
        c.plan.g["txt"].sigs = [sig(ED_ZONE, c.inc, c.exp, signer="wamason.com")]
    return I.issue(adversarial=True, hooks=hk(dns_plan=f))


case("L-70b", "DNSSEC", "TXT signed only by an alg-15 key absent from the zone (unrelated unsupported RRSIG)",
     "UNVERIFIABLE", "DNS_EVIDENCE_MISSING", cite=["P:538-544", "P:551-553"], amb=["EA-11"], amb_fields=["verdict", "reason"],
     why="Not row 3 (selector does not match), not row 5 (not a supported witness). Read as no usable witness "
         "-> row 2 (EA-11).")(
    lambda: I.issue(adversarial=True, hooks=hk(dns_plan=_txt_sigs(lambda c: sig(ED_STRAY, c.inc, c.exp, signer="wamason.com")))))
case("L-71a", "DNSSEC", "TXT RRset without its witness RRSIG", "UNVERIFIABLE", "DNS_EVIDENCE_MISSING",
     cite=["P:526", "P:800-802", "RES L-71"], why="Row 2.")(lambda: I.issue(adversarial=True, hooks=hk(dns_plan=_txt_sigs())))
case("L-71b", "DNSSEC", "Root DNSKEY without RRSIG", "UNVERIFIABLE", "NO_TRUSTED_KSK_USABLE",
     cite=["P:427-428", "P:800-802", "RES L-71"], why="Root case of missing witness.")(
    lambda: I.issue(adversarial=True, hooks=hk(dns_plan=_root_sigs())))


def _order(*drop):
    def f(c):
        c.plan.order = [n for n in c.plan.order if n not in drop]
    return f


case("L-72", "DNSSEC", "Sequence ending before the TXT group", "UNVERIFIABLE", "DNS_EVIDENCE_MISSING",
     cite=["P:1225-1226", "P:1383", "RES L-72"], why="Omission is missing evidence, not format.")(
    lambda: I.issue(adversarial=True, hooks=hk(dns_plan=_order("txt"))))


@case("L-73a", "DNSSEC", "Truncated RR (last RDATA one byte short)", "INVALID", "SNAPSHOT_FORMAT",
      cite=["P:1237-1239", "RES L-73"], why="Row 13.2.")
def _():
    def f(c):
        c.body = c.body[:-1]
    return I.issue(adversarial=True, hooks=hk(dns_body=f))


@case("L-73b", "DNSSEC", "Forbidden RR type (A at wamason.com)", "INVALID", "SNAPSHOT_FORMAT",
      cite=["P:1243-1244", "RES L-73"], why="Row 13.2.")
def _():
    def f(c):
        c.plan.g["w_dnskey"].extra_rrs.append((U.name_wire("wamason.com"), U.T_A, 3600, bytes([192, 0, 2, 1])))
    return I.issue(adversarial=True, hooks=hk(dns_plan=f))


@case("L-73c", "DNSSEC", "Duplicate RR in the wamason.com DNSKEY group", "INVALID", "SNAPSHOT_FORMAT",
      cite=["P:1219-1221", "P:1237-1238", "RES L-73"], why="Row 13.2.")
def _():
    def f(c):
        g = c.plan.g["w_dnskey"]
        g.extra_rrs.append((U.name_wire("wamason.com"), U.T_DNSKEY, g.ttl, c.zk["w_zsk"].rdata()))
    return I.issue(adversarial=True, hooks=hk(dns_plan=f))


@case("L-73d", "DNSSEC", "Misordered groups (com DNSKEY before com DS)", "INVALID", "SNAPSHOT_FORMAT",
      cite=["P:1212-1213", "P:1237-1238", "RES L-73"], why="Row 13.2.")
def _():
    def f(c):
        c.plan.order = ["root", "com_dnskey", "com_ds", "w_ds", "w_dnskey", "txt"]
    return I.issue(adversarial=True, hooks=hk(dns_plan=f))


case("L-74", "DNSSEC", "Uppercase signer name inside TXT RRSIG RDATA", "INVALID", "SNAPSHOT_FORMAT",
     cite=["P:1210-1211", "RES L-74"], why="Canonical form: names inside RDATA lowercase.")(
    lambda: I.issue(adversarial=True, hooks=hk(dns_plan=_txt_sigs(
        lambda c: sig(c.zk["w_zsk"], c.inc, c.exp, signer="wamason.com", signer_wire=U.name_wire("Wamason.com"))))))


def _upper_signer(shift):
    return lambda c: sig(c.zk["w_zsk"], c.inc + shift, c.exp, signer="wamason.com",
                         signer_wire=U.name_wire("Wamason.com"))


# The three diff-1 probe bundles (prototype/differential/probe_l74.py), now suite cases: an honest TXT witness plus an
# uppercase-signer TXT RRSIG in each body sort position. Under [OWNER 2026-10-14, diff-1 F-1] the non-canonical
# signer name is SNAPSHOT_FORMAT whatever other witnesses the body carries, so the honest witness does not rescue it.
for _cid, _shift, _pos in [("L-74e", -DAY, "inception one day earlier: sorts first"),
                           ("L-74l", 1, "inception one second later: sorts last"),
                           ("L-74v", 0, "same inception: issuer sort order")]:
    case(_cid, "DNSSEC", f"Valid TXT witness plus uppercase-signer TXT RRSIG ({_pos})", "INVALID", "SNAPSHOT_FORMAT",
         cite=["P:1294-1295", "P:1330-1336 (diff-1 F-1)", "P:1485", "RES L-74"],
         why="Row 13.2 [diff-1 F-1]: a domain-name field inside RDATA not in canonical form (uppercase signer name) "
             "is SNAPSHOT_FORMAT whatever other witnesses the body carries; the valid explicit witness does not make "
             "the extra candidate informational. Fail-closed.")(
        (lambda s: lambda: I.issue(adversarial=True, hooks=hk(dns_plan=_txt_sigs(TXT_OK, _upper_signer(s)))))(_shift))
case("L-75", "DNSSEC", "Wildcard TXT RRSIG (Labels 2 < 3) as the only witness", "INVALID", "DNS_WILDCARD",
     cite=["P:567-568", "P:1246-1248", "RES L-75"], why="Row 13.3.")(
    lambda: I.issue(adversarial=True, hooks=hk(dns_plan=_txt_sigs(
        lambda c: sig(c.zk["w_zsk"], c.inc, c.exp, signer="wamason.com", labels=2)))))
case("F07-a", "DNSSEC", "Valid explicit TXT witness plus a wildcard RRSIG", "INVALID", "DNS_WILDCARD",
     cite=["P:569-577"], why="Global body restriction.")(
    lambda: I.issue(adversarial=True, hooks=hk(dns_plan=_txt_sigs(
        TXT_OK, lambda c: sig(c.zk["w_zsk"], c.inc, c.exp, signer="wamason.com", labels=2)))))


def _value(fn):
    def f(c):
        c.value = fn(c)
    return f


@case("L-76", "DNSSEC", "Malformed TXT value (v=tessera2) with DNSSEC unperformable (root unsigned)", "INVALID",
      "DNS_VERSION", cite=["P:250-252", "P:1383", "RES L-76"], why="Row 13.6 INVALID dominates.")
def _():
    return I.issue(adversarial=True, hooks=hk(value=_value(lambda c: c.value.replace(b"v=tessera1", b"v=tessera2")),
                                              dns_plan=_root_sigs()))


@case("L-77", "DNSSEC", "Empty snapshot body", "INVALID", "LENGTH_CAP", cite=["P:254", "P:1245", "RES L-77"],
      amb=["EA-20"], why="Row 13.1; the profile says LENGTH_CAP (gen.py's codec says SCHEMA: EA-20).")
def _():
    def f(c):
        c.body = b""
    return I.issue(adversarial=True, hooks=hk(dns_body=f))


case("L-78", "DNSSEC", "Extra expired TXT RRSIG beside a valid one", "VALID_STRICT", "OK",
     cite=["P:786-789", "RES L-78"], why="Selected witness per G35; extra candidate informational.")(
    lambda: I.issue(hooks=hk(dns_plan=_txt_sigs(TXT_OK, lambda c: sig(c.zk["w_zsk"], c.T_snap - 20 * DAY,
                                                                      c.T_snap - 10 * DAY, signer="wamason.com")))))
case("L-79", "DNSSEC", "TXT RRSIG inception exactly 2^31 from T_snap", "INVALID", "RRSIG_TIME_AMBIGUOUS",
     cite=["P:809-814", "RES L-79"], why="G27.")(
    lambda: I.issue(adversarial=True, hooks=hk(dns_plan=_txt_sigs(
        lambda c: sig(c.zk["w_zsk"], c.T_snap + (1 << 31), c.exp, signer="wamason.com")))))
case("L-80", "DNSSEC", "TXT RRSIG inception > expiration", "INVALID", "RRSIG_INTERVAL_REVERSED",
     cite=["P:811-812", "RES L-80"], why="G27.")(
    lambda: I.issue(adversarial=True, hooks=hk(dns_plan=_txt_sigs(
        lambda c: sig(c.zk["w_zsk"], c.T_snap + DAY, c.T_snap - DAY, signer="wamason.com")))))
case("L-81", "DNSSEC", "TXT RRSIG inception = expiration = T_snap", "VALID_STRICT", "OK",
     cite=["P:812-814", "RES L-81"], why="Allowed; inclusive.")(
    lambda: I.issue(hooks=hk(dns_plan=_txt_sigs(lambda c: sig(c.zk["w_zsk"], c.T_snap, c.T_snap, signer="wamason.com")))))


@case("L-82", "DNSSEC", "2106 rollover: RRSIG expirations wrap past 2^32 around T_snap", "VALID_STRICT", "OK",
      cite=["P:809-814", "RES L-82"], amb=["EA-13"], why="Serial arithmetic resolves the wrapped expiration.")
def _(): return I.issue(timebase="2106-02-07T05:00:00Z", as_of="2106-02-07T06:28:15Z")


case("DNS-sig", "DNSSEC", "TXT RRSIG cryptographically invalid", "INVALID", "DNSSEC_SIGNATURE_INVALID",
     cite=["P:555"], why="Row 5.")(lambda: I.issue(adversarial=True, hooks=hk(dns_plan=_txt_sigs(
         lambda c: sig(c.zk["w_zsk"], c.inc, c.exp, signer="wamason.com", corrupt=True)))))
case("DNS-expired", "DNSSEC", "Only TXT RRSIG expired at T_snap", "INVALID", "RRSIG_NOT_VALID_AT_EVAL_TIME",
     cite=["P:549-550"], why="Row 5, time class.")(lambda: I.issue(adversarial=True, hooks=hk(dns_plan=_txt_sigs(
         lambda c: sig(c.zk["w_zsk"], c.T_snap - 20 * DAY, c.T_snap - 1, signer="wamason.com")))))
case("DNS-rootsig", "DNSSEC", "Root RRSIG by KSK-B cryptographically invalid", "INVALID",
     "TRUSTED_KSK_SIGNATURE_INVALID", cite=["P:424-426", "P:439-440"], why="Crypto class at the root.")(
    lambda: I.issue(adversarial=True, hooks=hk(dns_plan=_root_sigs(
        lambda c: sig(U.ksk_b(), c.root_inc, c.root_exp, signer=".", corrupt=True)))))
case("F05-a", "DNSSEC", "TXT signer DNSKEY has Zone Key flag clear", "INVALID", "DNSSEC_KEY_MISMATCH",
     cite=["P:551-553", "P:559-560"], why="No eligible matching DNSKEY.")(
    lambda: I.issue(adversarial=True, hooks=hk(dns_plan=lambda c: (
        setattr(c.plan.g["w_dnskey"], "rdatas", [c.zk["w_ksk"].rdata(), c.zk["w_zsk"].rdata(flags=0)]),
        setattr(c.plan.g["txt"], "sigs", [sig(c.zk["w_zsk"], c.inc, c.exp, signer="wamason.com",
                                              key_rdata=c.zk["w_zsk"].rdata(flags=0))])))))
case("F05-b", "DNSSEC", "TXT signer DNSKEY has protocol 2", "INVALID", "DNSSEC_KEY_MISMATCH",
     cite=["P:551-553"], why="No eligible matching DNSKEY.")(
    lambda: I.issue(adversarial=True, hooks=hk(dns_plan=lambda c: (
        setattr(c.plan.g["w_dnskey"], "rdatas", [c.zk["w_ksk"].rdata(), c.zk["w_zsk"].rdata(protocol=2)]),
        setattr(c.plan.g["txt"], "sigs", [sig(c.zk["w_zsk"], c.inc, c.exp, signer="wamason.com",
                                              key_rdata=c.zk["w_zsk"].rdata(protocol=2))])))))
case("F05-c", "DNSSEC", "TXT RRSIG Labels 4 > owner label count 3", "INVALID", "DNSSEC_RRSIG_METADATA",
     cite=["P:554"], why="Non-temporal metadata failure.")(
    lambda: I.issue(adversarial=True, hooks=hk(dns_plan=_txt_sigs(
        lambda c: sig(c.zk["w_zsk"], c.inc, c.exp, signer="wamason.com", labels=4)))))
case("F05-d", "DNSSEC", "TXT RRSIG alg 13 with a 63-byte signature", "INVALID", "DNSSEC_FORMAT",
     cite=["P:555", "P:1239-1240"], why="Malformed supported RRSIG RDATA.")(
    lambda: I.issue(adversarial=True, hooks=hk(dns_plan=_txt_sigs(
        lambda c: sig(c.zk["w_zsk"], c.inc, c.exp, signer="wamason.com", sig_bytes=b"\x11" * 63)))))
case("F05-e", "DNSSEC", "Parent-blocked child (DS type 1 only) with a locally invalid TXT signature", "INVALID",
     "DNSSEC_SIGNATURE_INVALID", cite=["P:545-548", "P:556-558"],
     why="Row 4 needs a locally valid candidate; none, so row 5 is reportable and INVALID dominates.")(
    lambda: I.issue(adversarial=True, hooks=hk(dns_plan=lambda c: (_w_ds(DS1_OK)(c), _txt_sigs(
        lambda c: sig(c.zk["w_zsk"], c.inc, c.exp, signer="wamason.com", corrupt=True))(c)))))
case("F05-f", "DNSSEC", "TXT RRSIG key tag matching no DNSKEY", "INVALID", "DNSSEC_KEY_MISMATCH",
     cite=["P:551-553", "P:559-560"], why="Unmatched selector is INVALID (owner choice).")(
    lambda: I.issue(adversarial=True, hooks=hk(dns_plan=_txt_sigs(
        lambda c: sig(c.zk["w_zsk"], c.inc, c.exp, signer="wamason.com", tag=(c.zk["w_zsk"].tag + 1) & 0xFFFF)))))


@case("F06-a", "DNSSEC", "Root-only -> TXT (TXT signed directly by the root ZSK)", "VALID_STRICT", "OK",
      cite=["P:1226-1228"], why="Ancestor signing permitted; the last z is the root.")
def _():
    def f(c):
        c.plan.order = ["root", "txt"]
        c.plan.g["txt"].sigs = [sig(c.zk["rzsk"], c.inc, c.exp, signer=".")]
    return I.issue(hooks=hk(dns_plan=f))


case("F06-b", "DNSSEC", "Missing last DNSKEY group (wamason.com DNSKEY)", "UNVERIFIABLE", "DNS_EVIDENCE_MISSING",
     cite=["P:1224-1226", "P:538-539"], why="Signer zone's DNSKEY absent.")(
    lambda: I.issue(adversarial=True, hooks=hk(dns_plan=_order("w_dnskey"))))
case("F06-c", "DNSSEC", "Missing DS group (wamason.com DS)", "UNVERIFIABLE", "DNS_EVIDENCE_MISSING",
     cite=["P:1224-1226", "P:538-539"], why="Omission is missing evidence.")(
    lambda: I.issue(adversarial=True, hooks=hk(dns_plan=_order("w_ds"))))
case("F06-d", "DNSSEC", "Missing root DNSKEY group", "UNVERIFIABLE", "NO_TRUSTED_KSK_USABLE",
     cite=["P:1224-1226"], why="Root omission.")(lambda: I.issue(adversarial=True, hooks=hk(dns_plan=_order("root"))))


@case("F06-e", "DNSSEC", "Wrong-owner TXT (_tessera-v2.wamason.com)", "INVALID", "DNS_OWNER",
      cite=["P:1231-1232", "P:504-505"], why="ENC 7 step 1.")
def _():
    def f(c):
        c.plan.g["txt"].owner = "_tessera-v2.wamason.com"
    return I.issue(adversarial=True, hooks=hk(dns_plan=f))


@case("F06-f", "DNSSEC", "Malformed TXT character-string (length byte runs past RDATA)", "INVALID", "DNS_RDATA",
      cite=["P:1239-1240", "ENC 7:557-558"], why="ENC 7 step 3.")
def _():
    def f(c):
        c.plan.g["txt"].rdatas = [bytes([200]) + c.value[:100]]
    return I.issue(adversarial=True, hooks=hk(dns_plan=f))


@case("F06-g", "DNSSEC", "TXT RDATA with two character-strings", "INVALID", "DNS_STRINGS", cite=["ENC 7:557-558"],
      why="ENC 7 step 4.")
def _():
    def f(c):
        c.plan.g["txt"].rdatas = [gen.dns_rdata(c.value[:100], c.value[100:])]
    return I.issue(adversarial=True, hooks=hk(dns_plan=f))


@case("F06-h", "DNSSEC", "Two TXT RRs at the owner", "INVALID", "DNS_RRSET", cite=["P:252", "ENC 7:557"],
      why="ENC 7 step 2 (the more-than-one case is reachable).")
def _():
    def f(c):
        c.plan.g["txt"].rdatas = [gen.dns_rdata(c.value), gen.dns_rdata(b"v=TEST-other")]
    return I.issue(adversarial=True, hooks=hk(dns_plan=f))


def _tie(sorted_ok):
    def f(c):
        g = c.plan.g["txt"]
        a = sig(c.zk["w_zsk"], c.inc, c.exp, signer="wamason.com")
        sigb = U.rrsig_rdata(g, a)[18 + len(U.name_wire("wamason.com")):]
        b = sig(c.zk["w_zsk"], c.inc, c.exp, signer="wamason.com", orig_ttl=g.ttl + 1, sig_bytes=sigb)
        g.sigs = [a, b] if sorted_ok else [b, a]
        g.sig_sort = sorted_ok
    return f


case("F07-b", "DNSSEC", "Primary-key tie (same tag/inception/expiration/signature), canonical RDATA order",
     "VALID_STRICT", "OK", cite=["P:1218-1221"], why="Final sort key is canonical RRSIG RDATA.")(
    lambda: I.issue(hooks=hk(dns_plan=_tie(True))))
case("F07-c", "DNSSEC", "Primary-key tie in the reverse order", "INVALID", "SNAPSHOT_FORMAT",
     cite=["P:1218-1221", "P:1237-1238"], why="Misordered witnesses.")(
    lambda: I.issue(adversarial=True, hooks=hk(dns_plan=_tie(False))))


@case("F07-d", "DNSSEC", "Duplicate TXT RRSIG", "INVALID", "SNAPSHOT_FORMAT", cite=["P:1220-1221"],
      why="Duplicate RR.")
def _():
    def f(c):
        c.plan.g["txt"].sigs = [TXT_OK(c), TXT_OK(c)]
    return I.issue(adversarial=True, hooks=hk(dns_plan=f))


@case("DNS-wlen", "DNS record", "Window of 90 days + 1 s in both channels", "INVALID", "DNS_WINDOW_LENGTH",
      cite=["P:583-584", "ENC 7:612"], why="ENC 7 step 15.")
def _(): return I.issue(window=("2026-11-01T00:00:00Z", rt(U.ts("2026-11-01T00:00:00Z") + 90 * DAY + 1)),
                        adversarial=True)


@case("DNS-wlen90", "DNS record", "Window of exactly 90 days (control)", "VALID_STRICT", "OK",
      cite=["P:583-584"], why="At most 90 days.")
def _(): return I.issue(window=("2026-11-01T00:00:00Z", rt(U.ts("2026-11-01T00:00:00Z") + 90 * DAY)))


@case("DNS-keys", "DNS record", "Both channels publish another kms fingerprint", "INVALID", "DNS_KEY_MISMATCH",
      cite=["P:684-691", "P:1393"], why="Row 15.1.")
def _():
    other = U.Keys.p256("unrelated-kms").fp_kms.split(":")[1]
    return I.issue(adversarial=True, hooks=hk(value=_value(lambda c: c.value.replace(
        c.kms.fp_kms.split(":")[1].encode(), other.encode()))))


@case("DNS-profile", "DNS record", "Both channels publish profile=tessera-v1-other", "INVALID", "DNS_PROFILE",
      cite=["ENC 7:609"], why="ENC 7 step 12.")
def _():
    return I.issue(adversarial=True, hooks=hk(value=_value(lambda c: c.value.replace(
        b"profile=tessera-v1-strict", b"profile=tessera-v1-strikt"))))


@case("CH-01", "DNS record", "Git blob carries a different window than DNS", "INVALID", "CHANNEL_VALUE_MISMATCH",
      cite=["P:646", "P:1394"], why="Row 15.2.")
def _():
    def f(c):
        c.blob = c.value.replace(c.window[0].encode(), b"2026-11-02T00:00:00Z")
    return I.issue(adversarial=True, hooks=hk(blob_value=f))


@case("CH-02", "DNS record", "Git blob = DNS value plus trailing LF", "INVALID", "CHANNEL_VALUE_MISMATCH",
      cite=["P:637-639", "P:1394"], amb=["EA-21"], amb_fields=["reason"], why="Framing: a trailing LF is rejected; the code that row 15.2 "
                                                        "gives is CHANNEL_VALUE_MISMATCH (EA-21).")
def _():
    def f(c):
        c.blob = c.value + b"\n"
    return I.issue(adversarial=True, hooks=hk(blob_value=f))


# ======================================================================================== snapshot / git proofs
@case("SNAP-stamp", "proofs", "Snapshot proof digest = SHA256(body), not of the ENC 6 envelope", "INVALID",
      "SNAPSHOT_STAMP_MISMATCH", cite=["P:1177-1179", "P:1381"], why="Row 13.4.")
def _():
    def f(c):
        c.snap_digest = hashlib.sha256(c.body).digest()
    return I.issue(adversarial=True, hooks=hk(digests=f))


case("SNAP-pending", "proofs", "Snapshot proof pending-only", "UNVERIFIABLE", "SNAPSHOT_NOT_ANCHORED",
     cite=["P:450-451", "P:744-745", "P:1381"], why="Row 13.4 unperformable.")(
    lambda: I.issue(snap_branches=[{"kind": "pending"}], adversarial=True))
case("SNAP-shape", "proofs", "Snapshot proof: digest double-hashed then a transaction (txid-subset shape fails)",
     "INVALID", "OTS_TX_SHAPE", cite=["P:753-757", "P:1203-1206"], why="Shape subset applies to the snapshot.")(
    lambda: I.issue(snap_branches=[{"h": HB + 12, "pre": "double"}], adversarial=True))
case("GIT-shape", "proofs", "Git proof: digest double-hashed then a transaction", "INVALID", "OTS_TX_SHAPE",
     cite=["P:753-757", "P:1390"], why="Shape subset applies to the git proof.")(
    lambda: I.issue(git_branches=[{"h": HB + 2, "pre": "double"}], adversarial=True))
case("GIT-pending", "proofs", "Git proof pending-only", "UNVERIFIABLE", "GIT_NOT_ANCHORED",
     cite=["P:744-745", "P:1390"], why="Row 14.6 unperformable; chain order unperformable.")(
    lambda: I.issue(git_branches=[{"kind": "pending"}], adversarial=True))


@case("GIT-stamp", "proofs", "Git proof digest over the commit id without LF", "INVALID", "GIT_STAMP_MISMATCH",
      cite=["P:629-630", "P:1179"], why="File digest must be SHA256(<40-hex id>\\n).")
def _():
    def f(c):
        c.git_digest = hashlib.sha256(c.git["id"].hex().encode()).digest()
    return I.issue(adversarial=True, hooks=hk(digests=f))


# ======================================================================================== OTS encoding
@case("L-83", "OTS", "receipt_anchor.txid != path-derived txid", "INVALID", "ANCHOR_TXID_MISMATCH",
      cite=["P:1189-1190", "P:1376", "RES L-83"], why="Row 11.5; T still reported.")
def _():
    def f(c):
        c.txid = "ab" * 32
    return I.issue(adversarial=True, hooks=hk(txid=f))


case("L-84", "OTS", "Codex F09 proof: digest double-hashed into a commitment, then a real transaction", "INVALID",
     "ANCHOR_TXID_MISMATCH", cite=["P:1184-1191", "RES L-84"],
     why="The first two consecutive sha256 ops take the digest, not a transaction.")(
    lambda: I.issue(receipt_branches=[{"h": HB + 24, "pre": "double"}], adversarial=True))
case("L-85", "OTS", "SegWit-serialized transaction preimage", "INVALID", "ANCHOR_TXID_MISMATCH",
     cite=["P:1186-1188", "RES L-85"], why="No SegWit marker.")(
    lambda: I.issue(receipt_branches=[{"h": HB + 24, "variant": "segwit"}], adversarial=True))
case("F09-a", "OTS", "Transaction with non-shortest CompactSize input count", "INVALID", "ANCHOR_TXID_MISMATCH",
     cite=["P:1188", "P:1192-1193"], why="Compact sizes shortest form.")(
    lambda: I.issue(receipt_branches=[{"h": HB + 24, "variant": "noncanon"}], adversarial=True))
case("F09-b", "OTS", "Multi-input / multi-output, non-125-byte transaction (control)", "VALID_STRICT", "OK",
     cite=["P:1184-1191"], why="Any non-witness transaction with the OP_RETURN output.")(
    lambda: I.issue(receipt_branches=[{"h": HB + 24, "variant": "multi"}]))
case("F09-c", "OTS", "Non-conventional merkle suffix (single sha256)", "INVALID", "ANCHOR_TXID_MISMATCH",
     cite=["P:1197-1200"], why="Part 4.")(
    lambda: I.issue(receipt_branches=[{"h": HB + 24, "suffix": "single"}], adversarial=True))
case("F08-a", "OTS", "Two paths at the selected height: one satisfies the txid subset, one does not",
     "VALID_STRICT", "OK", cite=["P:750-753", "P:1190-1191"], why="Any one path at h* may satisfy it.")(
    lambda: I.issue(receipt_branches=[{"h": HB + 24, "label": "good"}, {"h": HB + 24, "label": "bad", "pre": "double"}]))


def _ots_mut(name, fn):
    def f(c):
        c.ots[name] = fn(c, c.ots[name])
    return f


def _proof_mut(name, fn):
    def f(c):
        fn(c, c.proofs[name])
    return f


def _redundant_height(c, pr):
    for i, (ops, att) in enumerate(pr.paths):
        if att[1] == U.TAG_BTC:
            p = bytearray(att[2])
            p[-1] |= 0x80
            pr.paths[i] = (ops, (att[0], att[1], bytes(p) + b"\x00"))
            return


case("L-86", "OTS", "Redundant LEB128 (height varuint with an extra zero group)", "INVALID", "OTS_FORMAT", T=None,
     cite=["P:1173-1174", "RES L-86"], why="Row 11.1; T null (proof does not parse).")(
    lambda: I.issue(adversarial=True, hooks=hk(proof_objects=_proof_mut("receipt", _redundant_height))))
case("L-87a", "OTS", "SHA-1 op (0x02)", "INVALID", "OTS_FORMAT", T=None, cite=["P:1163", "P:1177", "RES L-87"],
     why="Any other op.")(lambda: I.issue(adversarial=True, receipt_branches=[
         {"h": HB + 24}, {"kind": "raw", "ops": [("raw", b"\x02")], "att": ("att", U.TAG_PENDING, U.pending_payload())}]))
case("L-87b", "OTS", "RIPEMD-160 op (0x03)", "INVALID", "OTS_FORMAT", T=None, cite=["P:1163", "P:1177", "RES L-87"],
     why="Any other op.")(lambda: I.issue(adversarial=True, receipt_branches=[
         {"h": HB + 24}, {"kind": "raw", "ops": [("raw", b"\x03")], "att": ("att", U.TAG_PENDING, U.pending_payload())}]))
case("L-87c", "OTS", "Unknown attestation tag", "INVALID", "OTS_FORMAT", T=None, cite=["P:1177", "RES L-87"],
     why="Any other tag.")(lambda: I.issue(adversarial=True, receipt_branches=[
         {"h": HB + 24}, {"kind": "raw", "ops": [("sha256",)], "att": ("att", b"TESTTAG!", b"\x00")}]))
case("L-87d", "OTS", "Depth bound exceeded (pending branch at depth 257)", "INVALID", "OTS_FORMAT", T=None,
     cite=["P:1170-1171", "P:1175", "RES L-87"], why="Depth <= 256.")(lambda: I.issue(adversarial=True, receipt_branches=[
         {"h": HB + 24}, {"kind": "raw", "ops": [("sha256",)] * 257, "att": ("att", U.TAG_PENDING, U.pending_payload())}]))
case("L-87e", "OTS", "Depth bound edge (pending branch at depth 256, control)", "VALID_STRICT", "OK",
     cite=["P:1170-1171", "P:1175"], amb=["EA-26"], why="Depth 256 allowed (python-opentimestamps 0.4.5 stops at 255).")(lambda: I.issue(receipt_branches=[
         {"h": HB + 24}, {"kind": "raw", "ops": [("sha256",)] * 256, "att": ("att", U.TAG_PENDING, U.pending_payload())}]))
case("F09-d", "OTS", "Bitcoin attestation message of 33 bytes", "INVALID", "OTS_FORMAT", T=None,
     cite=["P:1169-1170"], why="Independent of header availability.")(
    lambda: I.issue(adversarial=True, receipt_branches=[{"h": HB + 24}, {"h": HB + 31, "post": [("append", b"\x00")],
                                                                        "headers": False}]))
case("F09-e", "OTS", "Pending payload not consumed (extra byte after the URI)", "INVALID", "OTS_FORMAT", T=None,
     cite=["P:1167-1169"], why="Payloads consumed exactly.")(
    lambda: I.issue(adversarial=True, receipt_branches=[{"h": HB + 24}, {"kind": "pending", "args": {
        "payload": U.varbytes(b"https://test-calendar.invalid") + b"\x00"}}]))


def _bound_branches(target_ops=None, target_atts=None):
    """Extra pending branches so the receipt proof has exactly target_ops op items or target_atts attestations."""
    base = I.issue()
    ops0, atts0 = base.proofs["receipt"].counts()
    brs = [{"h": HB + 24}]
    if target_ops is not None:
        need = target_ops - ops0
        i = 0
        while need > 0:
            k = min(need - 1, 200)
            brs.append({"kind": "raw", "ops": [("append", b"B" + i.to_bytes(3, "big"))] + [("sha256",)] * k,
                        "att": ("att", U.TAG_PENDING, U.pending_payload())})
            need -= 1 + k
            i += 1
    if target_atts is not None:
        for i in range(target_atts - atts0):
            brs.append({"kind": "raw", "ops": [("append", b"A" + i.to_bytes(3, "big"))],
                        "att": ("att", U.TAG_PENDING, U.pending_payload())})
    return brs


def _bound_case(adv, **kw):
    def f():
        c = I.issue(receipt_branches=_bound_branches(**kw), adversarial=adv)
        o, a = c.proofs["receipt"].counts()
        assert (kw.get("target_ops") in (None, o)) and (kw.get("target_atts") in (None, a)), (o, a)
        return c
    return f


case("F09-f", "OTS", "Receipt proof with exactly 65536 op items (bound edge, control)", "VALID_STRICT", "OK",
     cite=["P:1171-1172", "P:1175"], why="<= 65536 ops.")(_bound_case(False, target_ops=65536))
case("F09-g", "OTS", "Receipt proof with 65537 op items", "INVALID", "OTS_FORMAT", T=None,
     cite=["P:1171-1172", "P:1175"], why="Bound exceeded; T null.")(_bound_case(True, target_ops=65537))
case("F09-h", "OTS", "Receipt proof with exactly 4096 attestations (bound edge, control)", "VALID_STRICT", "OK",
     cite=["P:1175"], why="<= 4096 attestations.")(_bound_case(False, target_atts=4096))
case("F09-i", "OTS", "Receipt proof with 4097 attestations", "INVALID", "OTS_FORMAT", T=None,
     cite=["P:1175"], why="Bound exceeded; T null.")(_bound_case(True, target_atts=4097))


@case("L-88", "OTS", "Receipt OTS digest != SHA256(a_sig): S_gpg re-serialized after stamping", "INVALID",
      "RECEIPT_ANCHOR_MISMATCH", T=None, cite=["P:1178-1179", "P:703-706", "P:291-293", "RES L-88"],
      why="A changed (still valid) signature fails the anchor; T null (file digest differs).")
def _():
    def f(c):
        s2 = tc.pgp_sign(c.F_gpg, c.gpg, c.sig_time,
                         unhashed=tc.gnupg_unhashed(c.gpg) + sp(20, b"\x80\x00\x00\x00\x00\x04\x00\x04TESTtest"))
        layer(c)["a_sig"] = b64(gen.encode_anchor(c.F_kms, c.S_kms, c.F_gpg, s2))
    return I.issue(adversarial=True, hooks=hk(layer=f))


@case("SNAP-otsfmt", "OTS", "Snapshot proof with redundant LEB128", "INVALID", "OTS_FORMAT",
      cite=["P:1173-1174", "P:1381"], why="Row 13.4 grammar; receipt T unaffected.")
def _(): return I.issue(adversarial=True, hooks=hk(proof_objects=_proof_mut("snap", _redundant_height)))


# ======================================================================================== git
def _git(fn):
    return lambda: I.issue(adversarial=True, hooks=hk(git=fn))


case("L-89", "git", "Merge commit with two distinct parents", "VALID_STRICT", "OK", cite=["P:1256", "RES L-89"],
     why="Allowed.")(lambda: I.issue(hooks=hk(git=lambda c: c.git.update(
         parents=c.git["parents"] + [hashlib.sha1(b"TEST second parent").hexdigest()]))))
case("L-90", "git", "Repeated identical parent", "INVALID", "GIT_COMMIT_FORMAT", cite=["P:1256-1258", "RES L-90"],
     why="Row 14.1.")(_git(lambda c: c.git.update(parents=c.git["parents"] * 2)))
case("L-91a", "git", "`encoding` header", "INVALID", "GIT_COMMIT_FORMAT", cite=["P:1257-1258", "RES L-91"],
     why="Any other header.")(_git(lambda c: c.git.update(extra_headers=[b"encoding ISO-8859-1\n"])))
case("L-91b", "git", "Second `gpgsig`", "INVALID", "GIT_COMMIT_FORMAT", cite=["P:1257-1258", "RES L-91"],
     why="Exactly one gpgsig.")(_git(lambda c: c.git.update(gpgsig_count=2)))
case("L-91c", "git", "Unsigned commit (no gpgsig)", "INVALID", "GIT_COMMIT_FORMAT", cite=["P:1255", "P:595"],
     why="Exactly one gpgsig.")(_git(lambda c: c.git.update(gpgsig_count=0)))
case("L-91d", "git", "`gpgsig-sha256` header", "INVALID", "GIT_COMMIT_FORMAT", cite=["P:1257"],
     why="Any other header.")(_git(lambda c: c.git.update(extra_headers=[b"gpgsig-sha256 TEST\n"])))
case("L-92a", "git", "Armor header line", "INVALID", "GIT_SIG_FORMAT", cite=["P:1263", "RES L-92"],
     why="No armor headers.")(_git(lambda c: c.git.update(armor_args={"header_lines": ["Comment: TEST"]})))
case("L-92b", "git", "Armor CRC mismatch", "INVALID", "GIT_SIG_FORMAT", cite=["P:1263-1264", "RES L-92"],
     why="A present CRC-24 must match.")(_git(lambda c: c.git.update(armor_args={"crc": "bad"})))
case("L-92c", "git", "77-character base64 line", "INVALID", "GIT_SIG_FORMAT", cite=["P:1261-1262", "RES L-92"],
     why="Lines of 1-76 characters.")(_git(lambda c: c.git.update(armor_args={"line_len": 77})))
case("L-92d", "git", "Armor without CRC line (control)", "VALID_STRICT", "OK", cite=["P:1262"],
     why="The CRC line is optional.")(lambda: I.issue(hooks=hk(git=lambda c: c.git.update(armor_args={"crc": "none"}))))


def _padbits(c):
    """Choose an unhashed-area size so the signature length is not a multiple of 3 (base64 padding present),
    then flip a pad bit in the armor."""
    for extra in (0, 1, 2, 3):
        un = tc.gnupg_unhashed(c.repo) + (sp(100, b"\x00" * extra) if extra else b"")
        c.git["sig_args"] = {"unhashed": un}
        I.finalize_git(c)
        if len(c.git["sig"]) % 3:
            c.git["armor_args"] = {"pad_mutation": True}
            return
    raise RuntimeError("no padded signature length")


case("L-92e", "git", "Armor base64 with nonzero pad bits", "INVALID", "GIT_SIG_FORMAT", cite=["P:1265-1266"],
     why="Strict RFC 4648 round trip.")(_git(_padbits))
case("L-92f", "git", "Git signature type 0x01 (text)", "INVALID", "GIT_SIG_FORMAT", cite=["P:1264", "P:625-627"],
     why="Type 0x00 required; codec violation maps to GIT_SIG_FORMAT.")(
    _git(lambda c: c.git.update(sig_args={"sig_type": 0x01})))
case("L-92g", "git", "Git signature with an unknown critical hashed subpacket", "INVALID", "GIT_SIG_FORMAT",
     cite=["P:625-627", "P:836-837"], why="Policy violation maps to GIT_SIG_FORMAT for git.")(
    _git(lambda c: c.git.update(sig_args={"hashed": tc.gnupg_hashed(c.repo, c.git["sig_created"])
                                          + sp(100, b"x", True)})))
def _unsorted_root(c):
    """Root tree with tessera-v1 before README (README < tessera-v1 in git order)."""
    readme = ("100644", "README", U.git_id("blob", b"TEST issuer repository for the Tessera V1 conformance universe.\n"))
    sub = U.tree_body(c.git["sub_entries"])
    c.git["root_override"] = U.tree_body([("40000", "tessera-v1", U.git_id("tree", sub)), readme], sort=False)


case("L-93a", "git", "Root tree entries not in git order", "INVALID", "GIT_TREE_FORMAT",
     cite=["P:1269-1271", "RES L-93"], why="Row 14.3.")(_git(_unsorted_root))


case("L-93b", "git", "Tree mode 040000", "INVALID", "GIT_TREE_FORMAT", cite=["P:1269", "RES L-93"],
     why="Modes without leading zero.")(_git(lambda c: c.git.update(root_dir_entry=(
         "040000", "tessera-v1", U.git_id("tree", U.tree_body(c.git["sub_entries"]))))))
case("L-95", "git", "Signer verifies, T_git outside a finalized interval", "INVALID", "GIT_SIGNER_OUTSIDE_INTERVAL",
     cite=["P:615-617", "P:618-622", "RES L-95"], why="Row 14.7.")(
    lambda: I.issue(adversarial=True, repo_entries=[U.repo_entry(U.Keys.p256("repository-key", 1759276800),
                                                                 end="2026-10-31T00:00:00Z")]))
case("L-96", "git", "No configured signer verifies (commit signed by another key)", "UNVERIFIABLE",
     "GIT_SIGNER_NOT_CONFIGURED", cite=["P:615-617", "RES L-96"], why="Row 14.7.")(
    _git(lambda c: c.git.update(sign_key=U.Keys.p256("unconfigured-repo-key", 1759276800))))
case("GIT-prefix", "git", "Git signature hash prefix wrong", "UNVERIFIABLE", "GIT_SIGNER_NOT_CONFIGURED",
     cite=["P:625-627", "P:855-857"], why="Failed mathematics incl. hash prefix is 'none verifies'.")(
    _git(lambda c: c.git.update(sig_args={"left16": b"\x00\x00"})))
case("GIT-path-a", "git", "Blob at tessera-v1/key-assertion.txt", "INVALID", "GIT_PATH", cite=["P:1272-1273"],
     why="Fixed path.")(_git(lambda c: c.git.update(sub_entries=[("100644", "key-assertion.txt",
                                                                   U.git_id("blob", c.git["blob"]))])))
case("GIT-path-b", "git", "Leaf mode 100755", "INVALID", "GIT_PATH", cite=["P:637-639", "P:1272-1273"],
     why="Leaf mode must be 100644.")(_git(lambda c: c.git.update(sub_entries=[("100755", "key-assertion",
                                                                                 U.git_id("blob", c.git["blob"]))])))
case("GIT-path-c", "git", "Commit names a tree id other than trees[0]", "INVALID", "GIT_PATH", cite=["P:1272-1273"],
     amb=["EA-22"], amb_fields=["reason"], why="Following commit -> tree fails (EA-22).")(
    _git(lambda c: c.git.update(commit_tree_id=hashlib.sha1(b"TEST other tree").hexdigest())))


@case("GIT-path-d", "git", "git.trees in the order [sub, root]", "INVALID", "GIT_PATH", cite=["P:1272-1273"],
      why="git.trees is exactly [root, sub].")
def _():
    def f(c):
        t = layer(c)["git"]["trees"]
        t.reverse()
    return I.issue(adversarial=True, hooks=hk(layer=f))


# ======================================================================================== signature profile
def _sig_case(hashed_fn=None, unhashed_fn=None, adversarial=True, **kw):
    def f(c):
        args = dict(kw)
        if hashed_fn:
            args["hashed"] = hashed_fn(c)
        if unhashed_fn:
            args["unhashed"] = unhashed_fn(c)
        resign("gpg", **args)(c)
    return lambda: I.issue(adversarial=adversarial, hooks=hk(sign=f))


FP = lambda c: c.gpg.v4_fpr_sha1  # noqa
case("L-97", "signature profile", "Hashed creation time marked critical", "VALID_STRICT", "OK",
     cite=["P:834-835", "RES L-97"], why="Critical or not.")(
    _sig_case(lambda c: sp(33, b"\x04" + FP(c)) + sp(2, ct(c), True), adversarial=False))
case("L-98", "signature profile", "Critical bit on the unhashed issuer key ID", "VALID_STRICT", "OK",
     cite=["P:838", "RES L-98"], why="Unhashed area ignored entirely.")(
    _sig_case(unhashed_fn=lambda c: sp(16, FP(c)[-8:], True), adversarial=False))
case("L-99", "signature profile", "Unknown critical hashed subpacket", "INVALID", "SIG_POLICY",
     cite=["P:836-837", "P:840", "RES L-99"], why="Row 9.1.")(
    _sig_case(lambda c: gnu_h(c) + sp(100, b"x", True)))
case("L-100", "signature profile", "Hashed signature-expiration (type 3)", "INVALID", "SIG_POLICY",
     cite=["P:835", "RES L-100"], why="No type 3.")(_sig_case(lambda c: gnu_h(c) + sp(3, b"\x00\x01\x00\x00")))
case("L-101", "signature profile", "Two type-2 subpackets", "INVALID", "SIG_POLICY", cite=["P:834", "RES L-101"],
     why="Exactly one.")(_sig_case(lambda c: gnu_h(c) + sp(2, ct(c))))
case("L-102a", "signature profile", "Type 2 with 3 data octets", "INVALID", "SIG_POLICY", cite=["P:834", "RES L-102"],
     why="Exactly four.")(_sig_case(lambda c: sp(33, b"\x04" + FP(c)) + sp(2, ct(c)[:3])))
case("L-102b", "signature profile", "Type 2 with 5 data octets", "INVALID", "SIG_POLICY", cite=["P:834", "RES L-102"],
     why="Exactly four.")(_sig_case(lambda c: sp(33, b"\x04" + FP(c)) + sp(2, ct(c) + b"\x00")))
case("L-103", "signature profile", "No type 2", "INVALID", "SIG_POLICY", cite=["P:834", "RES L-103"],
     why="Exactly one.")(_sig_case(lambda c: sp(33, b"\x04" + FP(c))))
case("L-104a", "signature profile", "Subpacket length 191, one-octet (shortest) form", "VALID_STRICT", "OK",
     cite=["P:869-873", "RES L-104"], why="Shortest form; non-critical unknown type ignored.")(
    _sig_case(lambda c: gnu_h(c) + sp(100, b"\x00" * 190), adversarial=False))
case("L-104b", "signature profile", "Subpacket length 192, two-octet (shortest) form", "VALID_STRICT", "OK",
     cite=["P:869-873", "RES L-104"], why="Shortest form.")(
    _sig_case(lambda c: gnu_h(c) + sp(100, b"\x00" * 191), adversarial=False))
case("L-104c", "signature profile", "Subpacket length 191 in five-octet form", "INVALID", "SIG_FORMAT",
     cite=["P:869-873", "P:1350", "RES L-104"], why="Non-shortest -> SIG_FORMAT at a_sig decoding (row 3.1).")(
    _sig_case(lambda c: gnu_h(c) + sp(100, b"\x00" * 190, form="five")))
case("L-104d", "signature profile", "Subpacket length 192 in five-octet form", "INVALID", "SIG_FORMAT",
     cite=["P:869-873", "P:1350", "RES L-104"], why="As L-104c.")(
    _sig_case(lambda c: gnu_h(c) + sp(100, b"\x00" * 191, form="five")))
case("F10-a", "signature profile", "Zero-data critical type 33", "INVALID", "SIG_POLICY", cite=["P:847-848"],
     why="Type 33 needs 21 octets.")(_sig_case(lambda c: sp(33, b"", True) + sp(2, ct(c))))
case("F10-b", "signature profile", "Two type-33 subpackets", "INVALID", "SIG_POLICY", cite=["P:845-846"],
     why="At most one.")(_sig_case(lambda c: gnu_h(c) + sp(33, b"\x04" + FP(c))))
case("F10-c", "signature profile", "Hashed type 16 inconsistent with type 33", "INVALID", "SIG_POLICY",
     cite=["P:846-847"], why="16 must equal the last 8 octets of 33.")(
    _sig_case(lambda c: gnu_h(c) + sp(16, b"\x01" * 8)))
case("F10-d", "signature profile", "Hashed type 16 with 7 octets", "INVALID", "SIG_POLICY", cite=["P:845"],
     why="Exactly 8.")(_sig_case(lambda c: sp(2, ct(c)) + sp(16, FP(c)[-7:])))
case("F10-e", "signature profile", "Type 33 whose first octet is 05", "INVALID", "SIG_POLICY", cite=["P:845-846"],
     why="First octet 04.")(_sig_case(lambda c: sp(33, b"\x05" + FP(c)) + sp(2, ct(c))))
case("F10-f", "signature profile", "Wrong hash-prefix octets on the gpg receipt signature", "INVALID", "SIG_INVALID",
     cite=["P:855-857", "P:1365"], why="Row 9.2.")(_sig_case(left16=b"\x00\x00"))
case("F10-g", "signature profile", "r = n in the gpg receipt signature", "INVALID", "SIG_POLICY",
     cite=["P:839-840"], amb=["EA-23"], amb_fields=["reason"], why="r outside [1, n-1]; listed in the rule-O policy (EA-23).")(
    _sig_case(r_override=gen.N))
case("SIG-type1", "signature profile", "Receipt signature type 0x01", "INVALID", "SIG_FORMAT",
     cite=["ENC 5.2:468", "P:1350"], why="Codec, row 3.1.")(_sig_case(sig_type=0x01))
case("SIG-newhdr", "signature profile", "Receipt signature with OpenPGP-format header 0xC2", "INVALID", "SIG_PACKET",
     cite=["ENC 5.2:447-451", "P:1350"], why="Codec, row 3.1.")(_sig_case(header="new"))


def _poss(slot, **kw):
    def f(c):
        doc = kw.pop("doc", None) if "doc" in kw else None
        key = c.kms if slot == "kms" else c.gpg
        s = tc.pgp_sign(doc if doc is not None else c.F_manifest, key, c.sig_time, **kw)
        setattr(c, "P_" + slot, s)
    return f


case("POS-a", "possession", "kms possession signature over another document", "INVALID", "POSSESSION_INVALID",
     cite=["P:840-842", "P:1368"], why="Row 9.5.")(
    lambda: I.issue(adversarial=True, hooks=hk(possession=_poss("kms", doc=b"TEST not the manifest"))))
case("POS-b", "possession", "gpg possession signature with hashed type 3", "INVALID", "SIG_POLICY",
     cite=["P:862-864", "P:1367"], why="Row 9.4.")(
    lambda: I.issue(adversarial=True, hooks=hk(possession=lambda c: _poss(
        "gpg", hashed=gnu_h(c) + sp(3, b"\x00\x01\x00\x00"))(c))))
case("POS-c", "possession", "gpg possession signature with header 0xC2", "INVALID", "SIG_PACKET",
     cite=["P:862-865", "P:1366"], why="Row 9.3 takes ENC's code.")(
    lambda: I.issue(adversarial=True, hooks=hk(possession=_poss("gpg", header="new"))))


# ======================================================================================== keys
def _keys_mut(slot, fn):
    def f(c):
        layer(c)["keys"][slot] = b64(fn(c))
    return lambda: I.issue(adversarial=True, hooks=hk(layer=f))


MLDSA65_SPKI = bytes.fromhex("308207b2300b0609608648016503040312038207a100") + tc.drbg("mldsa65-pub", 1952)

case("L-105", "keys", "ML-DSA-65 SPKI in keys.kms under the fallback", "INVALID", "KEY_FORMAT",
     cite=["P:826-830", "RES L-105"], amb=["EA-24"],
     why="Fallback half only; the hybrid half is not built (profile does not fully specify it; EA-24).")(
    _keys_mut("kms", lambda c: MLDSA65_SPKI))
case("KEY-a", "keys", "keys.gpg is another valid key", "INVALID", "KEY_MISMATCH", cite=["P:829-830", "P:1354"],
     why="Row 5.2.")(_keys_mut("gpg", lambda c: U.Keys.p256("other-gpg", 1790000000).pgp_body))
case("KEY-b", "keys", "keys.gpg with the 0x99 prefix", "INVALID", "KEY_FORMAT", cite=["P:825-826"],
     why="Bare v4 body.")(_keys_mut("gpg", lambda c: b"\x99" + struct.pack(">H", len(c.gpg.pgp_body)) + c.gpg.pgp_body))
case("KEY-c", "keys", "keys.gpg point off the curve", "INVALID", "KEY_FORMAT", cite=["P:858-861"],
     why="Public-key validation.")(_keys_mut("gpg", lambda c: c.gpg.pgp_body[:-1] + bytes([c.gpg.pgp_body[-1] ^ 1])))


@case("KEY-d", "keys", "Both slots carry other valid keys", "INVALID", "KEY_MISMATCH", cite=["P:1354", "P:1338"],
      why="Within-row tie: slot order kms, gpg; same reason.")
def _():
    def f(c):
        layer(c)["keys"]["kms"] = b64(U.Keys.p256("other-kms").spki)
        layer(c)["keys"]["gpg"] = b64(U.Keys.p256("other-gpg", 1790000000).pgp_body)
    return I.issue(adversarial=True, hooks=hk(layer=f))


# ======================================================================================== receipt consistency
@case("RC-a", "receipt consistency", "Frames disagree on content; manifest issuer also mismatches", "INVALID",
      "RECEIPT_COMMON_MISMATCH", cite=["P:694-699", "P:1356"], why="Row 6.2 precedes 6.3.")
def _():
    def f(c):
        c.common_gpg = dict(c.common, content={"TEST": "different content in the gpg frame"})
    return I.issue(manifest_issuer="other.example", adversarial=True, hooks=hk(common_slots=f))


@case("RC-b", "receipt consistency", "Bad common.manifest_sha256", "INVALID", "RECEIPT_MANIFEST_MISMATCH",
      cite=["P:696-698", "P:1352"], why="Row 4.2.")
def _():
    def f(c):
        c.common["manifest_sha256"] = "00" * 32
    return I.issue(adversarial=True, hooks=hk(common=f))


@case("RC-c", "receipt consistency", "Frames swapped between slots (each signed by its slot key)", "INVALID",
      "RECEIPT_SLOT", cite=["P:694-695", "P:1355"], why="Row 6.1.")
def _():
    def f(c):
        c.F_kms, c.F_gpg = c.F_gpg, c.F_kms
    return I.issue(adversarial=True, hooks=hk(frames=f))


case("RC-d", "receipt consistency", "Common issuer != manifest issuer", "INVALID", "RECEIPT_MANIFEST_MISMATCH",
     cite=["P:696", "P:1357"], why="Row 6.3.")(lambda: I.issue(manifest_issuer="other.example", adversarial=True))


# ======================================================================================== ENC codec in context
@case("CODEC-a", "codec", "Frame canonicalization version 2", "INVALID", "CV_UNKNOWN", cite=["P:218-219", "P:1350"],
      why="ENC 3.1.")
def _():
    def f(c):
        c.F_kms = gen.frame(gen.T_ATTEST, c.F_kms[24:], cv=2)
    return I.issue(adversarial=True, hooks=hk(frames=f))


@case("CODEC-b", "codec", "Anchor count byte 3", "INVALID", "ANCHOR_COUNT", cite=["ENC 5:383", "P:1350"],
      why="ENC 5.")
def _():
    def f(c):
        b = bytearray(c.A_sig)
        b[len(gen.header(gen.T_ANCHOR))] = 3
        c.A_sig = bytes(b)
    return I.issue(adversarial=True, hooks=hk(asig=f))


@case("CODEC-c", "codec", "Withdrawn frame-only anchor tag", "INVALID", "TAG_UNKNOWN", cite=["ENC 5.1", "P:218-219"],
      why="Not in T.")
def _():
    def f(c):
        c.A_sig = gen.encode_anchor_frames_only(c.F_kms, c.F_gpg)
    return I.issue(adversarial=True, hooks=hk(asig=f))


@case("CODEC-d", "codec", "Trailing byte after the second signature in a_sig", "INVALID", "TRAILING",
      cite=["ENC 5:391-392"], why="ENC 5 step 4.")
def _():
    def f(c):
        c.A_sig = c.A_sig + b"\x00"
    return I.issue(adversarial=True, hooks=hk(asig=f))


@case("CODEC-e", "codec", "Signed common.profile other than tessera-v1-strict", "INVALID", "SCHEMA",
      cite=["P:218-219"], why="Codec rejection after dispatch is INVALID.")
def _():
    def f(c):
        c.common["profile"] = "tessera-v1-other"
    return I.issue(adversarial=True, hooks=hk(common=f))


@case("CODEC-f", "codec", "First a_sig frame carries the manifest tag", "INVALID", "TAG_MISMATCH",
      cite=["P:235", "ENC 2:215-218"], why="Tag in T but not the expected one.")
def _():
    def f(c):
        c.F_kms = gen.frame(gen.T_MANIFEST, c.F_kms[24:])
    return I.issue(adversarial=True, hooks=hk(frames=f))


# ======================================================================================== aggregation
@case("L-106", "aggregation", "KEY_MISMATCH plus a bad git signature (CRC)", "INVALID", "KEY_MISMATCH",
      cite=["P:1354", "P:1386", "RES L-106"], why="Row 5.2 precedes 14.2.")
def _():
    def f(c):
        layer(c)["keys"]["gpg"] = b64(U.Keys.p256("other-gpg", 1790000000).pgp_body)
    return I.issue(adversarial=True, hooks=hk(layer=f, git=lambda c: c.git.update(armor_args={"crc": "bad"})))


case("L-107", "aggregation", "Unknown alg plus an independent failure (preamble altered)", "INVALID",
     "BUNDLE_OBJECT_HASH", cite=["P:263", "P:1396", "RES L-107"], why="INVALID dominates ALG_UNKNOWN.")(
    lambda: I.issue(alg="TEST-CANARY-ALG-X1", bundled_preamble=OTHER_PRE, adversarial=True))
case("L-108", "aggregation", "Bad attestation signature plus a usable receipt anchor", "INVALID", "SIG_INVALID",
     cite=["P:1365", "P:291-293", "RES L-108"], why="Row 9.2; T reported.")(
    lambda: I.issue(adversarial=True, hooks=hk(sign=lambda c: setattr(c, "S_gpg", tc.pgp_sign(b"TEST other", c.gpg,
                                                                                            c.sig_time)))))
case("L-109", "aggregation", "Receipt proof with a contradicted lower branch", "INVALID", "OTS_MERKLE_MISMATCH",
     T=None, cite=["P:291-293", "P:742-743", "RES L-109"], why="T null.")(
    lambda: I.issue(receipt_branches=[{"h": HB + 24}, {"h": HB + 21, "contradict": True, "headers": [HB + 21]}],
                    adversarial=True))


@case("AGG-a", "aggregation", "POSSESSION_INVALID + DNS_WILDCARD + GIT_PATH", "INVALID", "POSSESSION_INVALID",
      cite=["P:1368", "P:1380", "P:1389"], why="Row 9.5 first.")
def _():
    return I.issue(adversarial=True, hooks=hk(
        possession=_poss("kms", doc=b"TEST not the manifest"),
        dns_plan=_txt_sigs(lambda c: sig(c.zk["w_zsk"], c.inc, c.exp, signer="wamason.com", labels=2)),
        git=lambda c: c.git.update(sub_entries=[("100644", "key-assertion.txt", U.git_id("blob", c.git["blob"]))])))


case("AGG-b", "aggregation", "SNAPSHOT_TIME + GIT_COMMIT_FORMAT", "INVALID", "SNAPSHOT_TIME",
     cite=["P:1384", "P:1385"], why="Row 13.7 before 14.1.")(
    lambda: I.issue(times={HB + 17: TB + DELTA + 1}, adversarial=True,
                    hooks=hk(git=lambda c: c.git.update(extra_headers=[b"encoding ISO-8859-1\n"]))))
case("AGG-c", "aggregation", "SPEC_UNKNOWN + GIT_PATH", "INVALID", "GIT_PATH", cite=["P:263", "P:1389"],
     why="INVALID dominates.")(
    lambda: I.issue(spec_sha256=hashlib.sha256(OTHER_SPEC).hexdigest(), bundled_spec=OTHER_SPEC, adversarial=True,
                    hooks=hk(git=lambda c: c.git.update(sub_entries=[("100644", "key-assertion.txt",
                                                                       U.git_id("blob", c.git["blob"]))]))))


@case("AGG-d", "aggregation", "MEMBER_MISSING:git + ALG_UNKNOWN", "UNVERIFIABLE", "MEMBER_MISSING:git",
      cite=["P:1347", "P:1358"], why="First unperformable row (2.2 before 7.1).")
def _():
    def f(c):
        del layer(c)["git"]
    return I.issue(alg="TEST-CANARY-ALG-X1", adversarial=True, hooks=hk(container=f))


case("AGG-e", "aggregation", "TXT absent + git pending-only", "UNVERIFIABLE", "DNS_EVIDENCE_MISSING",
     cite=["P:1382-1383", "P:1390"], why="Row 13.5/13.6 before 14.6.")(
    lambda: I.issue(git_branches=[{"kind": "pending"}], adversarial=True, hooks=hk(dns_plan=_order("txt"))))
case("AGG-f", "aggregation", "ISSUANCE_WINDOW + BUNDLE_OBJECT_HASH", "INVALID", "ISSUANCE_WINDOW",
     cite=["P:1395", "P:1396"], why="Row 16.1 before 17.x.")(
    lambda: I.issue(window=(rt(TB + 1), rt(TB + 30 * DAY)), bundled_preamble=OTHER_PRE, adversarial=True))
case("AGG-g", "aggregation", "HEADER_CONFLICTS_PIN + SIG_INVALID", "INVALID", "SIG_INVALID",
     cite=["P:1365", "P:1369"], why="Row 9.2 before 10.1.")(
    lambda: I.issue(supply_extra=[HB + 33], adversarial=True, hooks=hk(
        sign=lambda c: setattr(c, "S_gpg", tc.pgp_sign(b"TEST other", c.gpg, c.sig_time)),
        pins=lambda c: c.header_bytes.__setitem__(HB + 33, c.chain.headers[HB + 33][:76] + b"\xff\xff\xff\xff"))))
case("AGG-h", "aggregation", "DNS_KEY_MISMATCH + CHANNEL_VALUE_MISMATCH + ISSUANCE_WINDOW", "INVALID",
     "DNS_KEY_MISMATCH", cite=["P:1393-1395"], why="Row 15.1 first.")(
    lambda: I.issue(window=(rt(TB + 1), rt(TB + 30 * DAY)), adversarial=True, hooks=hk(
        value=_value(lambda c: c.value.replace(c.kms.fp_kms.split(":")[1].encode(),
                                               U.Keys.p256("unrelated-kms").fp_kms.split(":")[1].encode())),
        blob_value=lambda c: setattr(c, "blob", c.value + b"\n"))))


# ======================================================================================== field grammars / numbers
case("L-110a", "field grammar", "declared_issue_time year 0000", "INVALID", "SCHEMA", cite=["P:938", "RES L-110"],
     why="Codec rejects (row 3.1).")(lambda: I.issue(declared="0000-01-01T00:00:00Z", adversarial=True))
case("L-110b", "field grammar", "declared_issue_time year 0001 (codec accepts)", "INVALID",
     "TIME_AFTER_DECLARED_DELTA", cite=["P:938", "P:720-722", "RES L-110"],
     why="Codec accepts; c1 holds, c2 fails first (row 12.2).")(
    lambda: I.issue(declared="0001-01-01T00:00:00Z", adversarial=True))
case("L-110c", "field grammar", "declared_issue_time year 9999 (codec accepts)", "INVALID",
     "TIME_BEFORE_DECLARED_EPSILON", cite=["P:938", "P:720-722", "RES L-110"], why="c1 fails (row 12.1).")(
    lambda: I.issue(declared="9999-12-31T23:59:59Z", adversarial=True))
case("L-110d", "field grammar", "Numeric top label in issuer (wamason.123)", "INVALID", "ISSUER_NOT_PINNED",
     cite=["P:938-941", "RES L-110"], why="Codec accepts; reason-only under G34.")(
    lambda: I.issue(issuer="wamason.123", adversarial=True))
case("L-111a", "numbers", "Content with ES-boundary numbers (1e21, 5e-324, 1.2345678901234568e20, 9.8, 100)",
     "VALID_STRICT", "OK", cite=["P:918-936", "RES L-111"], why="Value-preserving canonical numbers.")(
    lambda: I.issue(content={"a": 1e21, "b": 5e-324, "c": 1.2345678901234568e20, "d": 9.8, "e": 100, "f": 0.5}))


def _payload_sub(lit):
    def f(c):
        def patch(F):
            p = F[24:].replace(b'"__NUM__"', lit)
            return gen.frame(gen.T_ATTEST, p)
        c.F_kms, c.F_gpg = patch(c.F_kms), patch(c.F_gpg)
    return lambda: I.issue(content={"n": "__NUM__"}, adversarial=True, hooks=hk(frames=f))


case("L-111b", "numbers", "Payload number -0", "INVALID", "JSON_NUMBER", cite=["P:918-921", "ENC 1.2"],
     why="ENC 1.4 check 6 at row 3.1.")(_payload_sub(b"-0"))
case("L-111c", "numbers", "Payload number spelled 1E2 (value-preserving, non-canonical)", "INVALID",
     "JSON_NONCANONICAL", cite=["ENC 1.4 check 7", "P:1350"],
     why="Payload must equal JCS of its parse; ENC's code at row 3.1.")(_payload_sub(b"1E2"))


# ======================================================================================== hybrid routing (HS-04)
# formal/p8/HYBRID-CONFORMANCE-CASES.md cases (a)-(e), plus positive hybrid controls and hybrid-semantics negatives.
# Two installations (REPORT.md "Installations"): "classical" = the fallback catalog (alg OPENPGP4-ECDSA-P256-SHA256,
# pair id absent from the codec registry); "hybrid" = universe-catalog-hybrid.json (alg = the pair id, registered by
# the TEST supplement stand-in; spec object = baseline + supplement part). Citations "P:nnn" in this block are
# docs/V1-PROFILE.md line numbers of the 2026-10-14 revision after diff-1 (the revision in the tree on 2026-10-14);
# "HS §n" is formal/p8/HYBRID-SUPPLEMENT-DRAFT.md; "HC (x)" is formal/p8/HYBRID-CONFORMANCE-CASES.md.
PAIR = U.ALG_HYBRID
NEAR_MISS = "KMS-MLDSA65-PURE-GPG-OPENPGP4-ECDSA-P256-SHA384"          # P8 XHR-09
UNKNOWN_ID = "X-UNKNOWN-ALG-1"                                          # P8 A-02
NATIVE = {"classical": "p256", "hybrid": "mldsa65"}                     # the installation's kms key format (P:884-888)
INST_TAG = {"classical": "C", "hybrid": "H"}
ROUTE_CITE = ["P:114-119", "P:120-126", "P:1469"]
EA31 = "EA-31"


def _hy(inst, **kw):
    """A bundle for installation `inst`: its spec hash and catalog, kms key in the installation's format unless
    overridden (so row 5.1 passes under either EA-31 reading), adversarial (no honest-issuer refusals)."""
    kw.setdefault("kms_scheme", NATIVE[inst])
    kw.setdefault("adversarial", True)
    return I.issue(installation=inst, **kw)


def _mldsa_other(seed):
    return U.Keys.mldsa65(seed)


def _sign_slots(kms=None, gpg=None, pkms=None, pgpg=None):
    """sign / possession hooks replacing slot bytes (functions of c)."""
    hooks = {}
    if kms or gpg:
        def s(c):
            if kms:
                c.S_kms = kms(c)
            if gpg:
                c.S_gpg = gpg(c)
        hooks["sign"] = s
    if pkms or pgpg:
        def p(c):
            if pkms:
                c.P_kms = pkms(c)
            if pgpg:
                c.P_gpg = pgpg(c)
        hooks["possession"] = p
    return hooks


def _release_as(inst):
    """release hook: present the bundle to a verifier compiled for installation `inst`."""
    def f(c):
        c.release = U.make_release(c.trust_bytes, catalog_obj=U.catalog(inst))
    return f


# ---- (a) before registration (classical installation only)
case("HY-a1-C", "hybrid routing", "(a1) Pair id before registration: 3309-byte kms signature (genuine ML-DSA-65 "
     "bytes), rule-O gpg", "UNVERIFIABLE", "ALG_UNKNOWN", installation="classical",
     cite=ROUTE_CITE + ["P:127-130", "P:225-228", "P:280-283", "P:1461", "P:1475-1479", "P:741-750", "HC (a)"],
     why="Pair id is absent from the classical installation's codec registry (P:127-130): both slots use the opaque "
         "codec (nonempty, <= 65536) and accept. kms key is a valid P-256 SPKI with its manifest fingerprint "
         "(rows 5.1, 5.2 pass under either EA-31 reading). Rows 6.x pass (one alg everywhere). Row 7.1 "
         "unperformable: ALG_UNKNOWN; rows 9.1/9.2/9.4/9.5 are blocked by 7.1 (no SIG_*/POSSESSION_INVALID); M5's "
         "alg condition contributes ALG_UNKNOWN, not SCHEMA (P:748-750). No row fails; first unperformable = 7.1.")(
    lambda: _hy("classical", alg=PAIR, hooks=_sign_slots(kms=lambda c: _mldsa_other("hy-a1-other").sign(c.F_kms))))
case("HY-a2-C", "hybrid routing", "(a2) Pair id before registration: rule-O packets in both slots (kms 119-byte "
     "class)", "UNVERIFIABLE", "ALG_UNKNOWN", installation="classical",
     cite=ROUTE_CITE + ["P:127-130", "P:1461", "HC (a)"],
     why="As a1; the kms slot carries a rule-O packet, which rule R (HS §2) would reject as SIG_FORMAT, but the "
         "opaque codec accepts it (P:127-130). Reported: row 7.1 ALG_UNKNOWN.")(
    lambda: _hy("classical", alg=PAIR))
case("HY-a3-C", "hybrid routing", "(a3) Pair id before registration: arbitrary 1-byte kms and 65536-byte gpg "
     "signatures and possession proofs", "UNVERIFIABLE", "ALG_UNKNOWN", installation="classical",
     cite=ROUTE_CITE + ["P:127-130", "P:1461", "P:1477", "HC (a)"],
     why="Opaque codec bounds are 1..65536 (ENC 5.2); both boundary lengths accepted at rows 3.1 and 9.3; "
         "semantics blocked by 7.1. Reported: ALG_UNKNOWN.")(
    lambda: _hy("classical", alg=PAIR, hooks=_sign_slots(
        kms=lambda c: tc.drbg("hy-a3-kms", 1), gpg=lambda c: tc.drbg("hy-a3-gpg", 65536),
        pkms=lambda c: tc.drbg("hy-a3-pkms", 65536), pgpg=lambda c: tc.drbg("hy-a3-pgpg", 1))))
case("HY-a4-C", "hybrid routing", "(a) Pair id before registration: empty kms signature", "INVALID", "SIG_EMPTY",
     installation="classical", cite=["P:127-130", "P:225-226", "P:1461", "P:269-272", "HC (a)"],
     why="The opaque codec still rejects an empty signature at a_sig decoding (row 3.1, INVALID), which "
         "outranks ALG_UNKNOWN (row 7.1).")(
    lambda: _hy("classical", alg=PAIR, hooks=_sign_slots(kms=lambda c: b"")))
case("HY-a5-C", "hybrid routing", "(a) Pair id before registration: 65537-byte gpg signature", "INVALID",
     "LENGTH_CAP", installation="classical", cite=["P:127-130", "P:225-226", "P:1461", "P:269-272", "HC (a)"],
     why="Opaque cap 65536 (ENC 5.2) -> LENGTH_CAP at row 3.1; INVALID outranks ALG_UNKNOWN.")(
    lambda: _hy("classical", alg=PAIR, hooks=_sign_slots(gpg=lambda c: tc.drbg("hy-a5-gpg", 65537))))
EA31_DECISION = ("EA-31, 2026-10-14: unsupported well-formed alg gives UNVERIFIABLE / ALG_UNKNOWN; key format not "
                 "evaluated (profile §8 scope note, row 5.1)")
case("HY-ak-C", "hybrid routing", "(a) A genuine hybrid receipt (ML-DSA-65 SPKI in keys.kms, hybrid spec hash) "
     "presented to the classical installation", "UNVERIFIABLE", "ALG_UNKNOWN", installation="classical",
     cite=["P:892-899", "P:1472", "P:1477", "P:127-130", "HC (a)"], owner_decision=EA31_DECISION,
     why="The bundle is HY-V1's issue (pair id, ML-DSA-65 SPKI) under the classical release. The pair id is not the "
         "classical catalog id, so the installed-spec key rule does not apply (P:892-899, owner decision on EA-31): "
         "row 5.1 is available only when row 7.1's alg is catalog-supported (P:1472), and key format, fingerprint, "
         "signature and possession checks are not evaluated. No row fails; the first unperformable is row 7.1 "
         "(P:1477): ALG_UNKNOWN, before 8.3's SPEC_UNKNOWN. An examiner holding the wrong installation is told "
         "'cannot evaluate', not 'invalid'.")(
    lambda: I.issue(installation="hybrid", kms_scheme="mldsa65", kms_seed="hy-v1-kms", adversarial=True,
                    hooks=hk(release=_release_as("classical"))))

# ---- (b) after registration and selection: the classical id is still rule O (hybrid installation)
case("HY-b1-H", "hybrid routing", "(b) Classical-id receipt as a fallback issuer emits it (P-256 kms SPKI, valid "
     "rule-O signatures) under the hybrid installation", "UNVERIFIABLE", "ALG_UNKNOWN", installation="hybrid",
     cite=["P:892-899", "P:1472", "P:1477", "P:120-126", "HC (b)"], owner_decision=EA31_DECISION,
     why="Rule O decodes both slots (classical id is codec-known, P:120-122), row 3.1 passes. The classical id is "
         "not the hybrid catalog id, so the installed-spec key rule does not apply (P:892-899, owner decision on "
         "EA-31): row 5.1 is not evaluated (P:1472), so the P-256 kms SPKI is not KEY_FORMAT. Row 7.1 is "
         "unperformable (P:1477): ALG_UNKNOWN; signature and possession rows are blocked by 7.1.")(
    lambda: _hy("hybrid", alg=U.ALG_V1, kms_scheme="p256"))
case("HY-b2-H", "hybrid routing", "(b) Classical-id frames, rule-O signatures that do not verify, kms key in the "
     "installation's format (ML-DSA-65 SPKI)", "UNVERIFIABLE", "ALG_UNKNOWN", installation="hybrid",
     cite=["P:120-126", "P:884-888", "P:1461", "P:1464-1469", "P:1475-1479", "P:741-750", "HC (b)"],
     why="Both slots decode under rule O (codec-known, unselected: P:120-122); the kms slot carries a rule-O packet "
         "by an unrelated P-256 key, the gpg signature and possession are over other bytes. Row 5.1 passes under "
         "either EA-31 reading (installation format; or skipped), 5.2 passes (manifest fingerprint is the ML-DSA "
         "SPKI's). 6.x pass. Row 7.1 unperformable (classical id is not the catalog id). Rows 9.x blocked by 7.1, "
         "so no SIG_INVALID / POSSESSION_INVALID although none of the signatures would verify; M5 contributes "
         "ALG_UNKNOWN, not SCHEMA.")(
    lambda: _hy("hybrid", alg=U.ALG_V1, hooks=_sign_slots(
        kms=lambda c: tc.pgp_sign(c.F_kms, U.Keys.p256("hy-b2-unrelated"), c.sig_time),
        gpg=lambda c: tc.pgp_sign(b"TEST other bytes", c.gpg, c.sig_time),
        pkms=lambda c: tc.pgp_sign(c.F_manifest, U.Keys.p256("hy-b2-unrelated"), c.sig_time),
        pgpg=lambda c: tc.pgp_sign(b"TEST other bytes", c.gpg, c.sig_time))))

# ---- (c) codec-invalid classical signatures are INVALID in both installations
_C_DEFECTS = [
    ("c1", "XA-19 shape: kms packet under an OpenPGP-format 0xC2 header", "SIG_PACKET",
     lambda c: tc.pgp_sign(c.F_kms, c.kms, c.sig_time, header="new")),
    ("c2", "XA-22 shape: kms signature type 0x01", "SIG_FORMAT",
     lambda c: tc.pgp_sign(c.F_kms, c.kms, c.sig_time, sig_type=0x01)),
    ("c3", "XA-14 shape: kms signature of 1025 bytes (above the rule-O cap 1024)", "LENGTH_CAP",
     lambda c: tc.drbg("hy-c3-kms", 1025)),
    ("c4", "XA-11 shape: empty kms signature", "SIG_EMPTY", lambda c: b""),
]
for _inst in ("classical", "hybrid"):
    for _id, _what, _code, _fn in _C_DEFECTS:
        case(f"HY-{_id}-{INST_TAG[_inst]}", "hybrid routing", f"(c) Classical-id receipt, {_what} ({_inst} "
             "installation)", "INVALID", _code, installation=_inst,
             cite=["P:120-123", "P:225-226", "P:1461", "P:269-272", "HC (c)"],
             why="The classical id is codec-known in both installations, so rule O decodes the kms slot (P:120-122) "
                 f"and rejects it with ENC's code at row 3.1 ({_code}); INVALID outranks every later row, "
                 "including 5.1 (EA-31 does not matter) and the ALG_UNKNOWN of row 7.1 under the hybrid.")(
            (lambda f, i: lambda: _hy(i, alg=U.ALG_V1, kms_scheme="p256", hooks=_sign_slots(kms=f)))(_fn, _inst))

# ---- (d) a wholly unknown consistent id is opaque, ALG_UNKNOWN, in both installations
for _inst in ("classical", "hybrid"):
    for _id, _alg, _src in (("d1", NEAR_MISS, "near-miss pair id (P8 XHR-09)"), ("d2", UNKNOWN_ID, "P8 A-02")):
        case(f"HY-{_id}-{INST_TAG[_inst]}", "hybrid routing", f"(d) Frames and manifest all carry {_alg} ({_src}); "
             f"{_inst} installation", "UNVERIFIABLE", "ALG_UNKNOWN", installation=_inst,
             cite=["P:117", "P:120-126", "P:1461", "P:1469", "P:741-750", "HC (d)"],
             why="Absent from either registry: opaque codec, nonempty signatures accepted (row 3.1); kms key in the "
                 "installation's format with its manifest fingerprint (5.1, 5.2 pass under either EA-31 reading); "
                 "6.x pass; 7.1 ALG_UNKNOWN; 9.x blocked; no SCHEMA from M5.")(
            (lambda a, i: lambda: _hy(i, alg=a))(_alg, _inst))

# ---- (e) unequal frame and manifest alg values fail receipt consistency in both installations
def _e1(c):
    c.common_gpg = dict(c.common, alg=U.ALG_V1)


for _inst in ("classical", "hybrid"):
    case(f"HY-e1-{INST_TAG[_inst]}", "hybrid routing", "(e1) kms frame pair id, gpg frame classical id, manifest "
         f"pair id (M9 shape, P8 XHR-08); {_inst} installation", "INVALID", "RECEIPT_COMMON_MISMATCH",
         installation=_inst, cite=["P:123-124", "P:751-759", "P:1467", "P:269-272", "HC (e)"],
         why="Each slot decodes under its own frame's alg (P:120-121): kms pair id (opaque under classical, rule R "
             "under hybrid; a 3309-byte ML-DSA signature under hybrid), gpg classical (rule O); row 3.1 passes. The "
             "common byte substrings differ in alg: row 6.2 RECEIPT_COMMON_MISMATCH, INVALID whatever the support "
             "state of the ids (P:123-124), outranking 7.1.")(
        (lambda i: lambda: _hy(i, alg=PAIR, hooks=hk(common_slots=_e1)))(_inst))
    case(f"HY-e2-{INST_TAG[_inst]}", "hybrid routing", "(e2) Both frames pair id, manifest classical id; "
         f"{_inst} installation", "INVALID", "RECEIPT_MANIFEST_MISMATCH", installation=_inst,
         cite=["P:123-124", "P:751-759", "P:1468", "P:269-272", "HC (e)"],
         why="Row 6.3: common alg != manifest alg, checked for every syntactically valid id (P:123-124). The "
             "possession proofs follow the manifest's classical id (rule O), so row 9.3 does not also fail.")(
        (lambda i: lambda: _hy(i, alg=PAIR, manifest_alg=U.ALG_V1, hooks=_sign_slots(
            pkms=lambda c: tc.pgp_sign(c.F_manifest, U.Keys.p256("hy-e2-rule-o"), c.sig_time)) if i == "hybrid"
            else None))(_inst))
    case(f"HY-e3-{INST_TAG[_inst]}", "hybrid routing", "(e3) Both frames X-UNKNOWN-ALG-1, manifest "
         f"X-UNKNOWN-ALG-2; {_inst} installation", "INVALID", "RECEIPT_MANIFEST_MISMATCH", installation=_inst,
         cite=["P:123-124", "P:751-759", "P:1468", "HC (e)"],
         why="Row 6.3 for two unknown ids; INVALID outranks 7.1's ALG_UNKNOWN.")(
        (lambda i: lambda: _hy(i, alg=UNKNOWN_ID, manifest_alg="X-UNKNOWN-ALG-2"))(_inst))

# ---- positive hybrid controls (hybrid installation)
HY_POS_CITE = ["P:114-119", "P:134-136", "P:148", "P:878-880", "P:884-888", "P:905-907", "HS §1-§3",
               "A9.6 (A9:351-362)"]
case("HY-V1", "hybrid positive", "Full hybrid receipt through the issuer: kms ML-DSA-65 (rule R, EXTERNAL_MU), "
     "gpg P-256 (rule O); 779 / 778-byte frames", "VALID_STRICT", "OK", installation="hybrid", cite=HY_POS_CITE,
     why="Honest issue path (P§4) under the hybrid installation: the pair id is the catalog id, keys.kms is the "
         "supplement's DER SPKI (HS §3), S_kms and the kms possession proof are 3309-byte pure ML-DSA-65 signatures "
         "(empty context) obtained from mu = SHAKE256(SHAKE256(pk,64) || 00 00 || F, 64) (HS §1, the issuer's only "
         "path) and verified over F itself by `cryptography` before freezing. Every row passes.")(
    lambda: I.issue(installation="hybrid", kms_scheme="mldsa65", kms_seed="hy-v1-kms"))
case("HY-V2", "hybrid positive", "Full hybrid receipt with frames over 4096 bytes (6753 / 6752), signed by "
     "external mu", "VALID_STRICT", "OK", installation="hybrid", cite=HY_POS_CITE + ["A9:361-362"],
     why="As HY-V1 with content padded so both attestation frames exceed the 4096-byte KMS RAW limit (the genuine "
         "capture's F-G3 is 6753 bytes); the kms signature is made from mu, as A9.6's pass condition requires above "
         "4 KB, and is an ordinary signature over F.")(
    lambda: I.issue(installation="hybrid", kms_scheme="mldsa65", kms_seed="hy-v2-kms",
                    content={"TEST": "conformance universe: large hybrid frame", "pad": "p" * 5977}))

# ---- hybrid semantics are live under the hybrid installation (negative controls for HY-V1)
def _resign_kms(fn):
    return hk(sign=lambda c: setattr(c, "S_kms", fn(c)))


case("HY-N1", "hybrid semantics", "Pair id with a P-256 SPKI in keys.kms (fingerprints consistent; 3309-byte "
     "kms signature)", "INVALID", "KEY_FORMAT", installation="hybrid",
     cite=["P:884-889", "P:1464", "HS §3"],
     why="Under the hybrid, keys.kms must be the exact ML-DSA-65 SPKI (both EA-31 readings: installed spec, and the "
         "supported pair id). Row 5.1 KEY_FORMAT; rule R codec passes (3309 bytes).")(
    lambda: _hy("hybrid", kms_scheme="p256", hooks=hk(
        sign=lambda c: setattr(c, "S_kms", _mldsa_other("hy-n1-other").sign(c.F_kms)),
        possession=lambda c: setattr(c, "P_kms", _mldsa_other("hy-n1-other").sign(c.F_manifest)))))
case("HY-N2", "hybrid semantics", "kms ML-DSA-65 signature over another frame (anchor rebuilt)", "INVALID",
     "SIG_INVALID", installation="hybrid", cite=["P:1476", "HS §2"],
     why="A valid signature by the right key over different bytes, committed in A_sig and stamped: row 9.2.")(
    lambda: _hy("hybrid", hooks=_resign_kms(lambda c: c.kms.sign(c.F_kms + b" "))))
case("HY-N3", "hybrid semantics", "kms possession proof over other bytes", "INVALID", "POSSESSION_INVALID",
     installation="hybrid", cite=["P:905-907", "P:1479"],
     why="Possession uses rule R for kms under the hybrid (P:905-907): row 9.5.")(
    lambda: _hy("hybrid", hooks=hk(possession=lambda c: setattr(c, "P_kms", c.kms.sign(b"TEST not the manifest")))))
case("HY-N4", "hybrid semantics", "kms signature truncated to 3308 bytes", "INVALID", "SIG_FORMAT",
     installation="hybrid", cite=["P:134-136", "P:1461", "HS §2 (XH-01..04)"],
     why="Rule R: any length below 3309 other than 0 is SIG_FORMAT (HS §2), at row 3.1.")(
    lambda: _hy("hybrid", hooks=_resign_kms(lambda c: c.kms.sign(c.F_kms)[:-1])))
case("HY-N5", "hybrid semantics", "kms signature with a trailing byte (3310 bytes)", "INVALID", "LENGTH_CAP",
     installation="hybrid", cite=["P:134-136", "P:1461", "HS §2 (XH-01..04)"],
     why="Rule R cap is 3309; above it is LENGTH_CAP, never TRAILING (HS §2).")(
    lambda: _hy("hybrid", hooks=_resign_kms(lambda c: c.kms.sign(c.F_kms) + b"\x00")))


def _ctx_sign(c):
    """A valid ML-DSA-65 signature over F under the nonempty context "tessera-v1" (P8 XHR-13): wrong mode."""
    ctx = b"tessera-v1"
    mu = gen._mldsa_h(gen._mldsa_h(c.kms.pk, 64) + b"\x00" + bytes([len(ctx)]) + ctx + c.F_kms, 64)
    return gen.mldsa65_sign_mu(c.kms._gpriv, mu)


case("HY-N6", "hybrid semantics", "kms signature valid under the nonempty context 'tessera-v1' (XHR-13)",
     "INVALID", "SIG_INVALID", installation="hybrid", cite=["P:1476", "HS §1 (empty context)"],
     why="The registered context is empty (HS §1); a signature valid only under another context fails row 9.2.")(
    lambda: _hy("hybrid", hooks=_resign_kms(_ctx_sign)))


# ======================================================================================== authority isolation
# prototype/mutation/REPORT.md observation 3. In every attack case the attacker issues a fully self-consistent
# receipt through the issue path with its OWN two keys: manifest, frames, signatures (verified before freezing),
# possession proofs, A_sig, and a receipt OTS stamp committed into the case's synthetic chain under the pinned
# headers (any party can get a transaction into a block; the pins cover the real chain). Exactly one authority
# element is wrong. Its honest twin ("-T") is built by the same function with that one element made right, through
# the honest issuer's pre-ship refusals, and must be VALID_STRICT; selfcheck.py --all checks the twins and
# selfcheck.py --isolation checks that each attack fails exactly its named construction checks.
AUTH_COMMON_CITE = ["P:253-256", "P:269-272", "P:1442-1447", "A9:143", "A9:153"]
AW = "wamason.com"


def _auth_keys(tag):
    return dict(kms_seed=f"auth-{tag}-kms", gpg_seed=f"auth-{tag}-gpg")



def _plan_attacker_root(c):
    """(ii-root) the attacker's own DNS hierarchy from its own root (alg 13 throughout): no configured KSK."""
    G, S = U.Group, U.Sig
    rk, rz = U.zkey("attacker-root-KSK", 13, 257), U.zkey("attacker-root-ZSK", 13, 256)
    ck, cz = U.zkey("attacker-com-KSK", 13, 257), U.zkey("attacker-com-ZSK", 13, 256)
    wk, wz = U.zkey("attacker-wamason-KSK", 13, 257), U.zkey("attacker-wamason-ZSK", 13, 256)
    g = c.plan.g
    g["root"] = G(".", U.T_DNSKEY, [rk.rdata(), rz.rdata()], [S(rk, c.root_inc, c.root_exp, signer=".")], ttl=172800)
    g["com_ds"] = G("com", U.T_DS, [U.ds_rdata("com", ck.rdata(), 2)], [S(rz, c.inc, c.exp, signer=".")], ttl=86400)
    g["com_dnskey"] = G("com", U.T_DNSKEY, [ck.rdata(), cz.rdata()], [S(ck, c.inc, c.exp, signer="com")], ttl=86400)
    g["w_ds"] = G(AW, U.T_DS, [U.ds_rdata(AW, wk.rdata(), 2)], [S(cz, c.inc, c.exp, signer="com")], ttl=86400)
    g["w_dnskey"] = G(AW, U.T_DNSKEY, [wk.rdata(), wz.rdata()], [S(wk, c.inc, c.exp, signer=AW)], ttl=3600)
    g["txt"] = G("_tessera-v1." + AW, U.T_TXT, [gen.dns_rdata(c.value)], [S(wz, c.inc, c.exp, signer=AW)], ttl=300)


def _plan_attacker_zone_keys(c):
    """(ii-ds) honest root, com and wamason.com DS; the attacker's own wamason.com DNSKEY set, self-signed."""
    G, S = U.Group, U.Sig
    wk, wz = U.zkey("attacker-wamason-KSK", 13, 257), U.zkey("attacker-wamason-ZSK", 13, 256)
    honest = {c.zk["w_ksk"].tag, c.zk["w_zsk"].tag}
    assert not ({wk.tag, wz.tag} & honest)
    c.plan.g["w_dnskey"] = G(AW, U.T_DNSKEY, [wk.rdata(), wz.rdata()], [S(wk, c.inc, c.exp, signer=AW)], ttl=3600)
    c.plan.g["txt"].sigs = [S(wz, c.inc, c.exp, signer=AW)]


def _plan_txt_attacker_key(forge_tag):
    """(ii-zsk / ii-tag) honest chain down to the wamason.com DNSKEY set; the TXT is signed by an attacker key
    that is not in that set, carrying its own key tag (ii-zsk) or the honest ZSK's tag (ii-tag)."""
    def f(c):
        az = U.zkey("attacker-txt-signer", 13, 256)
        assert az.tag not in {c.zk["w_ksk"].tag, c.zk["w_zsk"].tag}
        kw = {"tag": c.zk["w_zsk"].tag} if forge_tag else {}
        c.plan.g["txt"].sigs = [U.Sig(az, c.inc, c.exp, signer=AW, **kw)]
    return f


ATTACKER_D = "wamason-attacker.com"


def _plan_other_domain(c):
    """(vi) the attacker's own registered domain under the honest com zone: com signs its DS (as a registry does for
    any registrant), so the chain to _tessera-v1.<attacker D> is a trusted path."""
    G, S = U.Group, U.Sig
    dk, dz = U.zkey("attacker-domain-KSK", 13, 257), U.zkey("attacker-domain-ZSK", 13, 256)
    g = c.plan.g
    g["w_ds"] = G(ATTACKER_D, U.T_DS, [U.ds_rdata(ATTACKER_D, dk.rdata(), 2)],
                  [S(c.zk["com_zsk"], c.inc, c.exp, signer="com")], ttl=86400)
    g["w_dnskey"] = G(ATTACKER_D, U.T_DNSKEY, [dk.rdata(), dz.rdata()], [S(dk, c.inc, c.exp, signer=ATTACKER_D)],
                      ttl=3600)
    g["txt"] = G("_tessera-v1." + ATTACKER_D, U.T_TXT, [gen.dns_rdata(c.value)],
                 [S(dz, c.inc, c.exp, signer=ATTACKER_D)], ttl=300)


def _publish_legit_keys(c):
    """(i) both channels publish the legitimate issuer's keys (the attacker holds no channel credential)."""
    _honest_value(c)


def _auth_pair(cid, title, verdict, reason, cite, why, holds, rows, sc_fails, attack, twin, twin_title, twin_why,
               amb=(), amb_fields=()):
    iso = {"attacker_holds": holds, "only_failing_rows": rows, "selfcheck_fails": sorted(sc_fails),
           "twin": cid + "-T"}
    case(cid, "authority isolation", title, verdict, reason, installation="classical", isolation=iso,
         cite=list(dict.fromkeys(list(cite) + AUTH_COMMON_CITE + ["prototype/mutation/REPORT.md obs. 3"])), why=why, amb=amb,
         amb_fields=amb_fields)(attack)
    case(cid + "-T", "authority isolation", "Honest twin of " + cid + ": " + twin_title, "VALID_STRICT", "OK",
         installation="classical", isolation={"twin_of": cid},
         cite=list(cite) + ["P:269-272"], why=twin_why)(twin)


# (i) keys not matching the DNS record
_auth_pair(
    "AUTH-i", "Attacker-keyed receipt, re-stamped; both channels publish the legitimate keys", "INVALID",
    "DNS_KEY_MISMATCH", ["P:741-750", "P:1504", "P:1038-1043"],
    "The attacker's receipt passes every receipt row (its own keys, manifest, possession, signatures, A_sig, a "
    "qualifying pinned stamp). DNS and git are the legitimate issuer's authentic evidence, consistent with each "
    "other (15.2 passes) but naming other keys: row 15.1 fails for the kms slot (M5). No earlier row fails.",
    "nothing (presents the legitimate issuer's DNS and git evidence)", ["15.1"], ["txt_keys"],
    lambda: I.issue(**_auth_keys("i"), adversarial=True, hooks=hk(value=_publish_legit_keys)),
    lambda: I.issue(**_auth_keys("i")),
    "the same attacker keys, published in DNS and git (the attacker holds both channel credentials)",
    "Same issue as AUTH-i with the record naming the keys that signed; every row passes.")

# (ii) DNS record signed under an attacker zone key with no trusted path (git channel valid: captured repo key)
_II = [
    ("root", "the attacker's own root, com and wamason.com zones (no configured root KSK)", "UNVERIFIABLE",
     "NO_TRUSTED_KSK_USABLE", ["P:466-469", "P:470-484", "P:557-561", "P:590-593", "P:1042-1043", "P:1493"],
     "Root group: no candidate is signed by a configured KSK -> 'no configured candidate' -> UNVERIFIABLE / "
     "NO_TRUSTED_KSK_USABLE (P:477-484). Every child RRset's parent is blocked and its candidates are locally valid "
     "(table row 4, P:590-593): unperformable with no reason of its own. The presented TXT parses (13.6), and its "
     "keys equal the manifest's (15.1 passes, P:1494, P:1504); git passes. No row fails; first unperformable 13.5.",
     _plan_attacker_root),
    ("ds", "honest root and com, the honest wamason.com DS, the attacker's own wamason.com DNSKEY set", "INVALID",
     "DNSKEY_DS_MISMATCH", ["P:578-600", "P:1493"],
     "Root, com DS, com DNSKEY and the wamason.com DS validate. The wamason.com DNSKEY RRset's only candidate "
     "verifies and is time-valid but no child DNSKEY matches the validated DS: row 5's DNSKEY_DS_MISMATCH "
     "(P:594-598). Whatever the TXT's own outcome, 13.5 reports in zone order (tie key, P:1493), so the "
     "wamason.com DNSKEY reason is first.",
     _plan_attacker_zone_keys),
    ("zsk", "honest chain to the wamason.com DNSKEY set; TXT signed by an attacker key outside it", "INVALID",
     "DNSSEC_KEY_MISMATCH", ["P:594-600", "P:604-605", "P:609-613", "P:1493"],
     "The TXT's only witness is a supported (alg 13) RRSIG whose signer name, algorithm and key tag match no "
     "DNSKEY in the validated wamason.com set: 'present supported witness with no matching eligible DNSKEY' -> "
     "INVALID / DNSSEC_KEY_MISMATCH (fail-closed unmatched selector, P:604-605; supported algorithm, so not the "
     "EA-11 rule of P:609-613).",
     _plan_txt_attacker_key(False)),
    ("tag", "as ii-zsk, but the attacker's RRSIG carries the honest ZSK's key tag", "INVALID",
     "DNSSEC_SIGNATURE_INVALID", ["P:594-598", "P:466-467", "P:1493"],
     "The selector matches the honest wamason.com ZSK, so the candidate is checked against it and fails "
     "cryptographically: INVALID / DNSSEC_SIGNATURE_INVALID (row 5). A key tag is a selector, not proof of "
     "authorship.",
     _plan_txt_attacker_key(True)),
]
for _v, _what, _verd, _code, _cite, _why, _plan in _II:
    _auth_pair(
        f"AUTH-ii-{_v}", f"Attacker-keyed receipt; DNS: {_what}; git assertion valid", _verd, _code,
        _cite + ["P:555-556", "A9:309-324"],
        "The attacker captured the repository key (the git assertion naming its keys verifies under the configured "
        "entry within its interval, chain order holds) but not the DNS credential. " + _why,
        "the repository key (git channel), not the DNS credential", ["13.5"], ["dnssec"],
        (lambda p, v: lambda: I.issue(**_auth_keys("ii-" + v), adversarial=True, hooks=hk(dns_plan=p)))(_plan, _v),
        (lambda v: lambda: I.issue(**_auth_keys("ii-" + v)))(_v),
        "the TXT signed under the trusted path (the honest wamason.com ZSK)",
        "Same issue with the TXT witness from the configured chain; every row passes.")

# (iii) git assertion signed by a non-configured repository key (DNS valid: captured DNS credential)
_auth_pair(
    "AUTH-iii", "Attacker-keyed receipt; DNS valid; git assertion signed by the attacker's own repository key",
    "UNVERIFIABLE", "GIT_SIGNER_NOT_CONFIGURED", ["P:668-670", "P:671-677", "P:1502", "A9:333-338"],
    "The attacker holds the DNS credential (the TXT naming its keys validates) and signs the key-assertion commit "
    "with its own repository key, not configured for D. Commit, path and git stamp are well formed and qualify; "
    "chain order holds. Row 14.7: no configured entry verifies -> UNVERIFIABLE / GIT_SIGNER_NOT_CONFIGURED "
    "('unknown material cannot establish this required check', A9.5). No row fails.",
    "the DNS credential, not the repository key", ["14.7"], ["repo_interval", "repo_signer"],
    lambda: I.issue(**_auth_keys("iii"), adversarial=True,
                    hooks=hk(git=lambda c: c.git.update(sign_key=U.Keys.p256("attacker-repo-key", 1759276800)))),
    lambda: I.issue(**_auth_keys("iii")),
    "the commit signed by the configured repository key",
    "Same issue with the configured repository key; every row passes. (selfcheck: repo_interval is blocked by "
    "repo_signer in the attack, so both are named.)")

# (iv) the right repository key outside its interval
_REPO = U.Keys.p256("repository-key", 1759276800)
_auth_pair(
    "AUTH-iv-end", "Attacker-keyed receipt; git assertion by the configured key after its finalized signing_end",
    "INVALID", "GIT_SIGNER_OUTSIDE_INTERVAL", ["P:668-677", "P:1502", "P:1419", "A9:333-338"],
    "The attacker holds the retired repository key and the DNS credential. The configured entry is finalized "
    "[2026-10-01, 2026-11-01T00:00:00Z]; T_git = 2026-11-02T00:20:00Z. The entry verifies but its interval "
    "excludes T_git: INVALID / GIT_SIGNER_OUTSIDE_INTERVAL (row 14.7).",
    "the DNS credential and the retired repository key", ["14.7"], ["repo_interval"],
    lambda: I.issue(**_auth_keys("iv-end"), adversarial=True,
                    repo_entries=[U.repo_entry(_REPO, end="2026-11-01T00:00:00Z")]),
    lambda: I.issue(**_auth_keys("iv-end"), repo_entries=[U.repo_entry(_REPO, end="2026-11-03T00:00:00Z")]),
    "the same finalized entry ending 2026-11-03T00:00:00Z (after T_git)",
    "Finalized interval contains T_git; every row passes.")
_auth_pair(
    "AUTH-iv-start", "Attacker-keyed receipt; git assertion by the configured key before its signing_start (open "
    "entry)", "INVALID", "GIT_SIGNER_OUTSIDE_INTERVAL", ["P:671-679", "P:519-521", "P:1502"],
    "The configured entry is open from 2026-11-03T00:00:00Z (<= as_of); T_git = 2026-11-02T00:20:00Z precedes it. "
    "A verifying entry with T_git before signing_start is INVALID / GIT_SIGNER_OUTSIDE_INTERVAL, open entries "
    "included (A08, P:677-679); the horizon covers only T_git > as_of.",
    "the DNS credential and the repository key, used before its registered start", ["14.7"], ["repo_interval"],
    lambda: I.issue(**_auth_keys("iv-start"), adversarial=True,
                    repo_entries=[U.repo_entry(_REPO, start="2026-11-03T00:00:00Z")]),
    lambda: I.issue(**_auth_keys("iv-start"), repo_entries=[U.repo_entry(_REPO, start="2026-11-01T00:00:00Z")]),
    "the open entry starting 2026-11-01T00:00:00Z (before T_git)", "Every row passes.")

# (v) chain-order pre-commitment violated
_auth_pair(
    "AUTH-v-eq", "Attacker-keyed receipt; git assertion anchored at h_receipt - 5 (not 6 blocks before)",
    "INVALID", "GIT_NOT_PRECOMMITTED", ["P:709-714", "P:1503", "A9:143"],
    "The attacker holds both channel credentials but publishes the assertion late: h_git = 900019, h_receipt = "
    "900024, so h_git + 5 = h_receipt and 'h_git + 5 < h_receipt' fails: row 14.8. T_git lies inside the open "
    "repository interval; DNS validates; no other row fails.",
    "both channel credentials (late publication)", ["14.8"], ["chain_order"],
    lambda: I.issue(**_auth_keys("v-eq"), h_git=HB + 19, adversarial=True),
    lambda: I.issue(**_auth_keys("v-eq"), h_git=HB + 18),
    "h_git = 900018 (h_git + 5 < h_receipt)", "Chain order holds at the boundary; every row passes.")
_auth_pair(
    "AUTH-v-after", "Attacker-keyed receipt; git assertion anchored after the receipt (h_git = h_receipt + 3)",
    "INVALID", "GIT_NOT_PRECOMMITTED", ["P:709-717", "P:1503", "A9:143"],
    "The assertion is anchored at 900027 > h_receipt = 900024 (T_git 12:50 after T 12:20). No clock comparison is "
    "made between T_git and declared (P:716-717); chain order fails: row 14.8.",
    "both channel credentials (publication after the receipt)", ["14.8"], ["chain_order"],
    lambda: I.issue(**_auth_keys("v-after"), h_git=HB + 27, adversarial=True),
    lambda: I.issue(**_auth_keys("v-after"), h_git=HB + 18),
    "the assertion anchored at 900018", "Every row passes.")

# (vi) issuer D not pinned
_auth_pair(
    "AUTH-vi", f"Attacker-keyed receipt for its own domain {ATTACKER_D}, with a trusted DNSSEC path and a git "
    "assertion under the configured repository key", "INVALID", "ISSUER_NOT_PINNED",
    ["P:697-708", "P:727-731", "P:549-550", "P:1470", "A9:32", "A9:68"],
    f"common.issuer = manifest issuer = {ATTACKER_D}, a domain the attacker legitimately controls: com signs its DS, "
    "so DNSSEC validates _tessera-v1.<issuer> (owner rebuilt from the signed issuer, P:549-550) and the TXT names "
    "the attacker's keys. The attacker also holds the repository key, so the commit verifies under the configured "
    "entry for D. Only the pinned-D gate fails: row 8.1 INVALID / ISSUER_NOT_PINNED (P:704-708). Under M2 "
    "(P:727-731) the git condition may also be read as unmet for D = common.issuer; that row is UNVERIFIABLE at "
    "worst and 8.1's INVALID is reported either way.",
    "its own domain's DNS and the repository key", ["8.1"], ["issuer_pinned"],
    lambda: I.issue(**_auth_keys("vi"), issuer=ATTACKER_D, adversarial=True, hooks=hk(dns_plan=_plan_other_domain)),
    lambda: I.issue(**_auth_keys("vi")),
    "issuer = wamason.com with the wamason.com chain", "Every row passes.")


# ======================================================================================== writer
def write_case(spec):
    cid = spec["id"]
    d = OUT / cid
    d.mkdir(parents=True, exist_ok=True)
    res = spec["fn"]()
    meta = {"id": cid, "group": spec["group"], "title": spec["title"], "cite": spec["cite"],
            "derivation": spec["why"], "ambiguities": spec["amb"], "ambiguous_fields": spec["amb_fields"],
            "kind": spec["kind"]}
    if spec["detail"]:
        meta["detail"] = spec["detail"]
    inst = spec["installation"]
    if inst is not None:
        meta["installation"] = inst
    if spec["isolation"] is not None:
        meta["isolation"] = spec["isolation"]
    if spec["alt"] is not None:
        meta["alternative"] = spec["alt"]
    if spec["owner_decision"] is not None:
        meta["owner_decision"] = spec["owner_decision"]
    if inst == "hybrid":
        (d / "catalog.json").write_text(json.dumps(U.catalog("hybrid"), indent=1, sort_keys=True) + "\n")
    if spec["kind"] == "release_check":
        (d / "previous.json").write_bytes(res["previous"])
        (d / "next.json").write_bytes(res["next"])
        exp = {"release_check": res["release_check"], "_meta": meta}
        (d / "expected.json").write_text(json.dumps(exp, indent=1, sort_keys=True) + "\n")
        return exp
    honest = None
    if isinstance(res, dict):
        if "recipe" in res:
            (d / "base.json").write_bytes(res["base"])
            (d / "bundle.recipe.json").write_text(json.dumps(res["recipe"], indent=1) + "\n")
            honest = honest or I.issue(installation=inst or "classical")
            trust_b, rel = honest.trust_bytes, honest.release
            Tval = res.get("T")
        elif "trust_bytes" in res:
            (d / "bundle.json").write_bytes(res["bundle"])
            trust_b, rel, Tval = res["trust_bytes"], res["release"], None
        else:
            (d / "bundle.json").write_bytes(res["bundle"])
            honest = I.issue(installation=inst or "classical")
            trust_b, rel, Tval = honest.trust_bytes, honest.release, None
    else:
        (d / "bundle.json").write_bytes(res.bundle)
        trust_b, rel, Tval = res.trust_bytes, res.release, res.T
        meta["issuer_preship"] = res.preship
    (d / "trust.json").write_bytes(trust_b)
    (d / "release.json").write_bytes(U.jcs(rel))
    if spec["request"]:
        (d / "request.txt").write_text(spec["request"] + "\n")
    if spec["refusal"]:
        exp = {"refusal": spec["refusal"], "_meta": meta}
    else:
        if spec["T"] == "auto":
            T = U.rfc3339(Tval) if Tval is not None else None
            if Tval is None:
                raise RuntimeError(f"{cid}: T auto but issuer computed none")
        else:
            T = spec["T"]
        exp = {"verdict": spec["verdict"], "reason": spec["reason"], "T": T, **STABLE, "_meta": meta}
    (d / "expected.json").write_text(json.dumps(exp, indent=1, sort_keys=True) + "\n")
    return exp


def main():
    only = None
    if len(sys.argv) > 2 and sys.argv[1] == "--only":
        only = set(sys.argv[2].split(","))
    ids = [c["id"] for c in CASES]
    dup = {i for i in ids if ids.count(i) > 1}
    assert not dup, dup
    OUT.mkdir(exist_ok=True)
    n = 0
    for spec in CASES:
        if only and spec["id"] not in only:
            continue
        write_case(spec)
        n += 1
        print(spec["id"], flush=True)
    U_pub = U.release_public()
    (HERE / "universe-release-key.json").write_text(json.dumps(U_pub, indent=1, sort_keys=True) + "\n")
    (HERE / "universe-catalog.json").write_text(json.dumps(U.catalog(), indent=1, sort_keys=True) + "\n")
    (HERE / "universe-catalog-hybrid.json").write_text(json.dumps(U.catalog("hybrid"), indent=1, sort_keys=True) + "\n")
    index = [{"id": s["id"], "group": s["group"], "title": s["title"], "kind": s["kind"],
              "expected": (s["refusal"] if s["refusal"] else f'{s["verdict"]} / {s["reason"]}'),
              "ambiguities": s["amb"], **({"installation": s["installation"]} if s["installation"] else {})}
             for s in CASES]
    (HERE / "cases-index.json").write_text(json.dumps(index, indent=1) + "\n")
    print(f"{n} cases written")


if __name__ == "__main__":
    main()
