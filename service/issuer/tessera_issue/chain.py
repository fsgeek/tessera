"""Bitcoin header source behind one interface: tip() and headers(heights) -> {height: 80 header bytes}.

ExplorerHeaders reads two or more Esplora-style explorers over an injected transport and accepts a header only
when every explorer returns the same block hash, the header hashes to it, and consecutive headers link. The
issuer pins exactly what it checked (pre-ship), so a header source that lies is caught there, not trusted."""
import json

from .util import sha256d


class HeaderError(Exception):
    pass


class HeaderSource:
    def tip(self):
        raise NotImplementedError

    def headers(self, heights):
        raise NotImplementedError


def pin_of(header):
    return sha256d(header)[::-1].hex()


def check_links(hdrs):
    for h in sorted(hdrs):
        if len(hdrs[h]) != 80:
            raise HeaderError(f"header {h} is not 80 bytes")
        if h - 1 in hdrs and hdrs[h][4:36] != sha256d(hdrs[h - 1]):
            raise HeaderError(f"header {h} does not link to {h - 1}")


class ExplorerHeaders(HeaderSource):
    def __init__(self, base_urls, transport):
        if len(base_urls) < 2:
            raise ValueError("at least two independent explorers")
        self.bases, self.transport = [u.rstrip("/") for u in base_urls], transport

    def _get(self, url):
        status, body = self.transport("GET", url, None)
        if status != 200:
            raise HeaderError(f"GET {url}: HTTP {status}")
        return body.decode("ascii").strip()

    def tip(self):
        return min(int(self._get(b + "/blocks/tip/height")) for b in self.bases)

    def headers(self, heights):
        out = {}
        for h in heights:
            hashes = {self._get(f"{b}/block-height/{h}") for b in self.bases}
            if len(hashes) != 1:
                raise HeaderError(f"explorers disagree at height {h}: {sorted(hashes)}")
            bh = hashes.pop()
            raws = {self._get(f"{b}/block/{bh}/header") for b in self.bases}
            if len(raws) != 1:
                raise HeaderError(f"explorers return different headers for {bh}")
            raw = bytes.fromhex(raws.pop())
            if pin_of(raw) != bh:
                raise HeaderError(f"header at {h} does not hash to {bh}")
            out[h] = raw
        check_links(out)
        return out


def headers_json(hdrs):
    return json.dumps({str(h): v.hex() for h, v in sorted(hdrs.items())}, sort_keys=True)
