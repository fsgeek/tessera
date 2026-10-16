"""Track 3 step 11: full git path verification (INSTRUMENT code, A9.2; not evidence for any claim).
All in-memory: objects are built here and presented as archived bytes; no git, no gpg."""
import struct

import dns.rdata
import dns.rdataclass
import dns.rdatatype
import pytest

from tessera_proto.real import gitchannel as G

PATH = "keys/v1/key-assertion"          # a generic path for the path-walking helper
PPATH = G.PROFILE_KEY_PATH              # the fixed profile path (V1-PROFILE §6.3)
VALUE = (b"v=tessera1;profile=tessera-v1-strict;kms=" + b"ab" * 32 + b";gpg=" + b"cd" * 32 +
         b";issuance-not-before=2026-10-12T00:00:00Z;issuance-not-after=2027-01-10T00:00:00Z")


def mk(typ, body):
    return typ, G.object_id(typ, body), body


def tree(*ents):   # (mode, name, oid-hex)
    return mk("tree", b"".join(m.encode() + b" " + n.encode() + b"\0" + bytes.fromhex(o) for m, n, o in ents))


def build(blob=VALUE, path=PATH):
    parts = path.split("/")
    b = mk("blob", blob)
    objs, child, mode = [b], b[1], "100644"
    for name in reversed(parts):
        t = tree(("100644", "README", b[1]), (mode, name, child))
        objs.insert(0, t)
        child, mode = t[1], "40000"
    raw = f"tree {objs[0][1]}\nauthor a <a@b> 1 +0000\ncommitter a <a@b> 1 +0000\n\nmsg\n".encode()
    return G.object_id("commit", raw), raw, objs


def test_good():
    cid, raw, objs = build()
    r = G.verify_key_path(cid, raw, objs, PATH)
    assert r["kms"] == "ab" * 32 and r["gpg"] == "cd" * 32 and r["issuance_not_after"] == "2027-01-10T00:00:00Z"


def reason(cid, raw, objs, path=PATH):
    with pytest.raises(G.GitPathError) as e:
        G.verify_key_path(cid, raw, objs, path)
    return e.value.reason


def test_substituted_blob_at_path():
    # the tree names the real blob; a different (well-formed) blob is presented in its place
    cid, raw, objs = build()
    other = mk("blob", VALUE.replace(b"ab" * 32, b"ee" * 32))
    assert reason(cid, raw, objs[:-1] + [other]) == "BLOB_SUBSTITUTED"


def test_tree_entry_points_at_different_blob():
    # an attacker rewrites the leaf tree to name its blob and re-hashes upward only partway: chain must break
    cid, raw, objs = build()
    evil = mk("blob", VALUE.replace(b"ab" * 32, b"ee" * 32))
    leaf_tree = tree(("100644", "key-assertion", evil[1]))
    bad = objs[:-2] + [leaf_tree, evil]
    assert reason(cid, raw, bad) == "LINK_MISMATCH"   # parent tree still names the old leaf tree


def test_wrong_path_component():
    cid, raw, objs = build()
    assert reason(cid, raw, objs, "keys/v2/key-assertion") == "PATH_NOT_FOUND"
    assert reason(cid, raw, objs, "keys/../key-assertion") == "PATH_COMPONENT"


def test_tree_id_mismatch():
    cid, raw, objs = build()
    t, oid, body = objs[1]
    assert reason(cid, raw, objs[:1] + [(t, oid, body + b"x")] + objs[2:]) == "TREE_ID_MISMATCH"


def test_commit_id_mismatch():
    cid, raw, objs = build()
    assert reason(cid, raw + b"x", objs) == "COMMIT_ID_MISMATCH"
    assert reason("0" * 40, raw, objs) == "COMMIT_ID_MISMATCH"


def test_commit_names_other_root_tree():
    cid, raw, objs = build()
    other = tree(("100644", "x", objs[-1][1]))
    assert reason(cid, raw, [other] + objs[1:]) == "LINK_MISMATCH"


def test_blob_id_mismatch():
    cid, raw, objs = build()
    t, oid, body = objs[-1]
    assert reason(cid, raw, objs[:-1] + [(t, oid, body + b"\n")]) == "BLOB_ID_MISMATCH"


def test_object_count():
    cid, raw, objs = build(path="a/b")
    assert reason(cid, raw, objs, "a") == "PATH_OBJECTS_COUNT"


@pytest.mark.parametrize("blob,why", [
    (VALUE + b"\n", "KEY_SYNTAX"),
    (VALUE.replace(b"tessera1", b"tessera2"), "KEY_SYNTAX"),
    (VALUE.replace(b"ab" * 32, b"AB" * 32), "KEY_SYNTAX"),
    (VALUE + b";extra=1", "KEY_SYNTAX"),
    (VALUE.replace(b"2026-10-12T00", b"2026-13-12T00"), "KEY_VALUE"),
    (VALUE.replace(b"2027-01-10", b"2026-10-12"), "KEY_WINDOW"),
    (VALUE.replace(b"2027-01-10", b"2027-01-11"), "KEY_WINDOW_LENGTH"),
])
def test_exact_value(blob, why):
    cid, raw, objs = build(blob)
    assert reason(cid, raw, objs) == why


# --- profile composition: fixed path + DNS byte equality (docs/reviews/v1-profile/ F7) ---
def txt(value: bytes):
    """The character-strings of one TXT RR, parsed the way a validated DNS answer would carry them."""
    return dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.TXT, '"' + value.decode() + '"').strings


def preason(cid, raw, objs, strings):
    with pytest.raises(G.GitPathError) as e:
        G.verify_profile_key_assertion(cid, raw, objs, strings)
    return e.value.reason


def test_profile_path_constant():
    assert PPATH == "tessera-v1/key-assertion"
    assert len(VALUE) == 255     # the canonical value fits one character-string


def test_profile_good_dns_equal():
    cid, raw, objs = build(path=PPATH)
    strings = txt(VALUE)
    assert strings == (VALUE,)
    r = G.verify_profile_key_assertion(cid, raw, objs, strings)
    assert r["path"] == PPATH and r["dns_value_equal"] and r["kms"] == "ab" * 32


def test_profile_correct_record_at_wrong_path():
    cid, raw, objs = build(path=PATH)     # right bytes, generic path: not the profile's
    assert preason(cid, raw, objs, txt(VALUE)) in ("PATH_NOT_FOUND", "PATH_OBJECTS_COUNT")
    cid, raw, objs = build(path="tessera-v1/key-assertion.txt")
    assert preason(cid, raw, objs, txt(VALUE)) == "PATH_NOT_FOUND"


@pytest.mark.parametrize("dns_value", [
    VALUE.replace(b"ab" * 32, b"ee" * 32),                                  # different kms key
    VALUE.replace(b"cd" * 32, b"ce" * 32),                                  # different gpg key
    VALUE.replace(b"2027-01-10T00:00:00Z", b"2027-01-09T00:00:00Z"),          # different window
])
def test_profile_dns_git_mismatch(dns_value):
    cid, raw, objs = build(path=PPATH)
    assert preason(cid, raw, objs, txt(dns_value)) == "DNS_GIT_MISMATCH"


def test_profile_dns_shape():
    cid, raw, objs = build(path=PPATH)
    assert preason(cid, raw, objs, (VALUE[:100], VALUE[100:])) == "DNS_TXT_SHAPE"   # split across strings
    assert preason(cid, raw, objs, ()) == "DNS_TXT_SHAPE"


def test_profile_dns_framing_not_tolerated():
    # the DNS value with a trailing byte, or the blob with one, never compares equal
    cid, raw, objs = build(path=PPATH)
    assert preason(cid, raw, objs, (VALUE + b" ",)) == "DNS_GIT_MISMATCH"
    cid, raw, objs = build(blob=VALUE + b"\n", path=PPATH)
    assert preason(cid, raw, objs, (VALUE,)) == "KEY_SYNTAX"
