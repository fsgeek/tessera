"""Request store and result store behind interfaces, with in-memory implementations (AWS ones in aws.py).

Request store: request records (state, content digest, timestamps, pipeline progress; never content), content-free
key tombstones kept until issuance closes, the signer-request index (signer request id -> request and job), and the
append-only signature log (E-02). Records carry a version; save() is a compare-and-set on it.

Result store: blobs in four namespaces: "content" (submitted bytes, deleted when the request ends), "work" (frames,
signatures, proofs; deleted when the request ends), "frames" (frames too large for a queue message, read by the
signers by digest-bound reference; deleted when the request ends) and "result" (completed receipts, deleted 30 days
after the end).

Cleanup obligations (IS-07) are kept apart from the request record, so a failed deletion is retried by the poller
whatever state the request is in, and the 30-day deletion of results does not depend on S3 lifecycle timing."""
import copy


class RequestStore:
    def get(self, rid):
        raise NotImplementedError

    def create(self, rec, tombstone_until=None):
        """Insert iff absent, together with the key's tombstone in the same atomic write (IS-04). -> bool."""
        raise NotImplementedError

    def save(self, rec):
        """Compare-and-set on rec["version"]; on success the stored and the passed record get version + 1."""
        raise NotImplementedError

    def active(self):
        raise NotImplementedError

    def tombstone_get(self, rid):
        raise NotImplementedError

    def tombstone_put(self, rid, keep_until):
        raise NotImplementedError

    def sigreq_put(self, signer_rid, entry, keep_until):
        raise NotImplementedError

    def sigreq_get(self, signer_rid):
        raise NotImplementedError

    def siglog_add(self, entry):
        raise NotImplementedError

    def siglog(self):
        raise NotImplementedError

    def siglog_has(self, request_id, signature_sha256):
        """Is there a durable "used" log record for this signature on this signer request? (IS-01)"""
        raise NotImplementedError

    def cleanup_put(self, rid, doc):
        raise NotImplementedError

    def cleanup_list(self):
        """-> [(rid, doc)] of outstanding cleanup obligations."""
        raise NotImplementedError

    def cleanup_done(self, rid):
        raise NotImplementedError


NAMESPACES = ("content", "work", "frames", "result")


class ResultStore:
    def put(self, ns, rid, name, data):
        raise NotImplementedError

    def get(self, ns, rid, name):
        raise NotImplementedError

    def delete(self, ns, rid):
        raise NotImplementedError

    def names(self, ns, rid):
        """-> names stored under (ns, rid)."""
        raise NotImplementedError

    def size(self, ns, rid, name):
        """-> length in bytes, or None."""
        data = self.get(ns, rid, name)
        return None if data is None else len(data)

    def presign(self, ns, rid, name, expires_in, now):
        """A fresh URL for one object, valid expires_in seconds. Callers mint one per request and never keep it."""
        raise NotImplementedError

    @staticmethod
    def ref(ns, rid, name):
        """The object reference a signer is given for a large frame (IS-09)."""
        if ns != "frames":
            raise ValueError(ns)
        return f"{ns}/{rid}/{name}"

    def get_ref(self, ref):
        ns, rid, name = ref.split("/")
        if ns != "frames":
            raise ValueError(ref)
        return self.get(ns, rid, name)


class InMemoryRequestStore(RequestStore):
    """Also models TTL deletion (expire(now)) so the tests can show lookups after the record itself is gone."""

    def __init__(self):
        self.recs, self.tombs, self.sigreqs, self.log, self.cleanups = {}, {}, {}, [], {}

    def get(self, rid):
        r = self.recs.get(rid)
        return copy.deepcopy(r) if r is not None else None

    def create(self, rec, tombstone_until=None):
        if rec["rid"] in self.recs:
            return False
        rec["version"] = 1
        self.recs[rec["rid"]] = copy.deepcopy(rec)
        if tombstone_until is not None:
            self.tombs.setdefault(rec["rid"], {"rid": rec["rid"], "keep_until": tombstone_until})
        return True

    def save(self, rec):
        cur = self.recs.get(rec["rid"])
        if cur is None or cur["version"] != rec["version"]:
            return False
        rec["version"] += 1
        self.recs[rec["rid"]] = copy.deepcopy(rec)
        return True

    def active(self):
        return [copy.deepcopy(r) for r in self.recs.values() if r["state"] == "ACCEPTED"]

    def tombstone_get(self, rid):
        return self.tombs.get(rid)

    def tombstone_put(self, rid, keep_until):
        self.tombs.setdefault(rid, {"rid": rid, "keep_until": keep_until})

    def sigreq_put(self, signer_rid, entry, keep_until):
        self.sigreqs[signer_rid] = dict(entry, keep_until=keep_until)

    def sigreq_get(self, signer_rid):
        return self.sigreqs.get(signer_rid)

    def siglog_add(self, entry):
        self.log.append(dict(entry))

    def siglog(self):
        return list(self.log)

    def siglog_has(self, request_id, signature_sha256):
        return any(e.get("disposition") == "used" and e.get("request_id") == request_id
                   and e.get("signature_sha256") == signature_sha256 for e in self.log)

    def cleanup_put(self, rid, doc):
        self.cleanups[rid] = copy.deepcopy(doc)

    def cleanup_list(self):
        return [(rid, copy.deepcopy(d)) for rid, d in self.cleanups.items()]

    def cleanup_done(self, rid):
        self.cleanups.pop(rid, None)

    def expire(self, now):
        """What DynamoDB TTL does, eventually: drop records past their expiry and tombstones past closure."""
        for rid, r in list(self.recs.items()):
            if r.get("expires_at") is not None and r["expires_at"] <= now:
                del self.recs[rid]
        for rid, t in list(self.tombs.items()):
            if t["keep_until"] <= now:
                del self.tombs[rid]


class InMemoryResultStore(ResultStore):
    def __init__(self):
        self.blobs = {}

    def put(self, ns, rid, name, data):
        if ns not in NAMESPACES:
            raise ValueError(ns)
        self.blobs[(ns, rid, name)] = bytes(data)

    def get(self, ns, rid, name):
        return self.blobs.get((ns, rid, name))

    def delete(self, ns, rid):
        for k in [k for k in self.blobs if k[0] == ns and k[1] == rid]:
            del self.blobs[k]

    def presign(self, ns, rid, name, expires_in, now):
        return f"memory://{ns}/{rid}/{name}?expires={int(now) + int(expires_in)}"

    def fetch_url(self, url, now):
        """Test stand-in for the GET of a minted URL: -> bytes, or None when expired or the object is gone."""
        path, _, q = url[len("memory://"):].partition("?expires=")
        if now > int(q):
            return None
        ns, rid, name = path.split("/")
        return self.get(ns, rid, name)

    def names(self, ns, rid):
        return sorted(k[2] for k in self.blobs if k[0] == ns and k[1] == rid)
