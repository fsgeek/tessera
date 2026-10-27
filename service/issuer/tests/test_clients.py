"""The network-protocol clients the deployed issuer uses (calendar, explorers, resolver), exercised against the
stand-ins' wire servers; plus OTS proof structure as the verifier reads it. No network."""
import pytest
from tessera_verify.anchors import parse_ots, select, tx_path
from tessera_verify.dnssec import parse_rrsig, parse_snapshot, validate_snapshot

from tessera_issue import ots
from tessera_issue.chain import ExplorerHeaders, HeaderError, pin_of
from tessera_issue.dns import QUERIES, DnsError, LiveDns, make_query, parse_answers
from tessera_issue.stand_in import StandInCalendar, StandInChain, StandInDns
from tessera_issue.preship import check_config
from tessera_issue.testkeys import P256Key
from tessera_issue.util import FakeClock, b64e, rfc3339, sha256

T0 = 1793500000


@pytest.fixture
def chain():
    return StandInChain(FakeClock(T0))


def test_http_calendar_stamp_upgrade_and_proof_shape(chain):
    cal = StandInCalendar(chain)
    http = ots.HttpCalendar(cal.uri, cal.serve)
    digests = [sha256(bytes([i])) for i in range(5)]
    proofs = [ots.stamp(d, [http], bytes(16)) for d in digests]     # five stamps share one block
    assert all(ots.lowest_btc_height(p) is None for p in proofs)
    assert ots.upgrade(proofs[0], [http]) == (proofs[0], False)      # still pending
    chain.clock.advance(600)
    chain.mine(6)
    for d, p in zip(digests, proofs):
        new, changed = ots.upgrade(p, [http])
        assert changed and ots.k6_ready(new, chain.tip()) == (True, chain.tip() - 5)
        proof = parse_ots(new)
        assert proof.digest == d and not proof.pending                # the pending attestation was replaced
        hdrs = chain.headers(range(chain.tip() - 5, chain.tip() + 1))
        sel, contradicted = select(proof, hdrs, {h: pin_of(v) for h, v in hdrs.items()})
        assert sel and not contradicted
        att = sel.paths[0]
        assert tx_path(att, ots.txid_of(att))                         # tx shape and conventional merkle suffix


def test_stamp_survives_one_calendar_down_and_fails_with_all_down(chain):
    cal = StandInCalendar(chain)
    down = ots.HttpCalendar("https://down.invalid", lambda m, u, b: (503, b""))
    p = ots.stamp(sha256(b"x"), [down, ots.HttpCalendar(cal.uri, cal.serve)], bytes(16))
    assert parse_ots(p).pending == [cal.uri.encode()]
    with pytest.raises(ots.OtsError):
        ots.stamp(sha256(b"x"), [down], bytes(16))


def test_calendar_answers_outside_the_grammar_are_rejected(chain):
    bad = ots.HttpCalendar("https://bad.invalid", lambda m, u, b: (200, b"\x02\x00"))   # unknown op 0x02
    with pytest.raises(ots.OtsError):
        ots.stamp(sha256(b"x"), [bad], bytes(16))


def test_explorers_must_agree(chain):
    chain.mine(8)
    ex = ExplorerHeaders(["https://a.invalid/api", "https://b.invalid/api"], chain.serve_esplora)
    assert ex.tip() == chain.tip()
    got = ex.headers(range(chain.tip() - 5, chain.tip() + 1))
    assert got == chain.headers(range(chain.tip() - 5, chain.tip() + 1))

    other = StandInChain(FakeClock(T0 + 1))
    other.mine(8)

    def split(method, url, body):
        return (other if "//b." in url else chain).serve_esplora(method, url, body)
    with pytest.raises(HeaderError, match="disagree"):
        ExplorerHeaders(["https://a.invalid/api", "https://b.invalid/api"], split).headers([chain.tip()])

    def lying(method, url, body):
        status, data = chain.serve_esplora(method, url, body)
        return (status, ("00" * 80).encode()) if url.endswith("/header") else (status, data)
    with pytest.raises(HeaderError, match="hash"):
        ExplorerHeaders(["https://a.invalid/api", "https://b.invalid/api"], lying).headers([chain.tip()])
    with pytest.raises(ValueError):
        ExplorerHeaders(["https://a.invalid/api"], chain.serve_esplora)


def test_live_dns_capture_over_the_wire_equals_the_canonical_body():
    clock = FakeClock(T0)
    value = b"v" * 255
    dns = StandInDns(value)
    wire, direct = LiveDns(dns.serve(clock)).capture(clock()), dns.capture(clock())

    def shape(body):                       # everything but the (randomized) ECDSA signature bytes
        snap = parse_snapshot(body)
        return [(g.owner, g.type, [r.data for r in g.rr], [r.ttl for r in g.rr + g.sigs],
                 [parse_rrsig(r.data).prefix for r in g.sigs]) for g in snap.groups]
    assert shape(wire) == shape(direct) and len(wire) == len(direct)
    repo = {"domain": "wamason.com", "key": b64e(P256Key("r").pgp_body), "signing_end": None,
            "signing_start": "2026-01-01T00:00:00Z", "sources": [{"description": "t", "sha256": "0" * 64, "uri": "t"}]}
    cfg = check_config({"root_ksks": dns.root_entries("2026-01-01T00:00:00Z"), "repository_keys": [repo]}, {},
                       rfc3339(clock()))
    assert all(a.status == "pass" for a in validate_snapshot(parse_snapshot(wire), cfg, clock()))


def test_live_dns_rejects_errors_and_unsigned_answers():
    clock = FakeClock(T0)
    dns = StandInDns(b"v" * 255)
    serve = dns.serve(clock)

    def servfail(q):
        r = bytearray(serve(q))
        r[3] = (r[3] & 0xF0) | 2
        return bytes(r)
    with pytest.raises(DnsError):
        LiveDns(servfail).capture(clock())
    q = make_query(*QUERIES[0])
    tc, rrs = parse_answers(serve(q))
    assert not tc and len(rrs) == 3                                   # two DNSKEYs and their RRSIG

    def no_sigs(q):                                                   # drop the RRSIG (the last answer)
        r = serve(q)
        _, rrs = parse_answers(r)
        sig = rrs[-1][3]
        cut = r[:-(len(sig) + 12)]
        return cut[:6] + (len(rrs) - 1).to_bytes(2, "big") + cut[8:]
    with pytest.raises(DnsError):
        LiveDns(no_sigs).capture(clock())
