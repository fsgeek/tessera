"""AWS implementations of the store, queue and wake interfaces, over injected boto3-style clients (boto3 is
imported only by lambda_app.from_env). Nothing here calls KMS: the issuer holds no signing credential.

DynamoDB table (one table, partition key "pk"):
  REQ#<rid>      request record: "doc" (JSON), "version" (N), "pending_shard" = "1" while ACCEPTED (sparse GSI
                 "pending-index"), "expires_at" (N, the table's TTL attribute) = ended_at + 30 days (absent while the
                 request is live), and the lifecycle guard fields "lstate", "latt", "lastate" (request state, current
                 attempt id, current attempt state) that a guarded save conditions on with the version
  KEY#<rid>      content-free key tombstone, expires_at = after issuance closes
  SIGREQ#<id>    signer request id -> request, job, slot, frame hash; expires_at = 30 days after sending
  SIGLOG#<uuid>  one signer response as logged (E-02); no expiry. A "used" response is logged under the
                 deterministic key SIGLOG#USED#<signer request id>#<signature sha256> so sealing can require it (IS-01)
  CLEAN#<rid>    a cleanup obligation (IS-07), pending_shard = "2" in the same sparse index; no expiry
  POLLER#cursor  the poller's scheduling cursor (ILI-05): the request id it last started on
S3 bucket: content/<rid>/..., work/<rid>/..., frames/<rid>/<sha256> (large frames, read by the signers by reference),
result/<rid>/receipt.json, config/window.json. The poller deletes each request's objects itself (IS-07), first
tagging them cleanup-due; the bucket's lifecycle rule expires only tagged objects, as a backstop (5.3.1)."""
import json
import uuid

from .deadline import AWS_WORST_S, GuardedClient, guarded
from .stores import CLEANUP_TAG, NAMESPACES, RequestStore, ResultStore, lifecycle_guard


def _conditional_failed(exc):
    code = getattr(exc, "response", {}).get("Error", {}).get("Code")
    return code == "ConditionalCheckFailedException" or type(exc).__name__ == "ConditionalCheckFailedException"


def _transaction_conflict(exc):
    code = getattr(exc, "response", {}).get("Error", {}).get("Code")
    if code != "TransactionCanceledException" and type(exc).__name__ != "TransactionCanceledException":
        return False
    reasons = getattr(exc, "response", {}).get("CancellationReasons") or []
    return any(r.get("Code") == "ConditionalCheckFailed" for r in reasons)


def _not_found(exc):
    code = getattr(exc, "response", {}).get("Error", {}).get("Code")
    return code in ("NoSuchKey", "404", "NotFound") or type(exc).__name__ == "NoSuchKey"


class DynamoRequestStore(RequestStore):
    request_worst_s = AWS_WORST_S
    INDEX = "pending-index"

    def __init__(self, client, table):
        self.c, self.t = GuardedClient(client, "dynamodb"), table      # ILC-I-02: every request guarded

    def _get(self, pk):
        it = self.c.get_item(TableName=self.t, Key={"pk": {"S": pk}}, ConsistentRead=True).get("Item")
        return it

    GUARD_ATTRS = (("state", "lstate"), ("attempt", "latt"), ("astate", "lastate"))

    def _item(self, rec):
        item = {"pk": {"S": "REQ#" + rec["rid"]}, "doc": {"S": json.dumps(rec, sort_keys=True)},
                "version": {"N": str(rec["version"])}}
        g = lifecycle_guard(rec)
        for field, attr in self.GUARD_ATTRS:
            item[attr] = {"S": str(g[field] or "")}
        if rec["state"] == "ACCEPTED":
            item["pending_shard"] = {"S": "1"}
        if rec.get("expires_at") is not None:
            item["expires_at"] = {"N": str(rec["expires_at"])}
        return item

    def get(self, rid):
        it = self._get("REQ#" + rid)
        return json.loads(it["doc"]["S"]) if it else None

    def create(self, rec, tombstone_until=None):
        """IS-04: the record and the key's tombstone are written in one transaction."""
        rec["version"] = 1
        items = [{"Put": {"TableName": self.t, "Item": self._item(rec),
                          "ConditionExpression": "attribute_not_exists(pk)"}}]
        if tombstone_until is not None:
            items.append({"Put": {"TableName": self.t, "Item": {"pk": {"S": "KEY#" + rec["rid"]},
                                                                "expires_at": {"N": str(tombstone_until)}}}})
        try:
            self.c.transact_write_items(TransactItems=items)
            return True
        except Exception as e:  # noqa: BLE001
            if _transaction_conflict(e):
                return False
            raise

    def save(self, rec, expect=None):
        old = rec["version"]
        rec["version"] = old + 1
        cond, names, values = "#v = :v", {"#v": "version"}, {":v": {"N": str(old)}}
        if expect is not None:                        # the lifecycle guard, evaluated atomically with the version
            for field, attr in self.GUARD_ATTRS:
                cond += f" AND #{attr} = :{attr}"
                names["#" + attr] = attr
                values[":" + attr] = {"S": str(expect[field] or "")}
        try:
            self.c.put_item(TableName=self.t, Item=self._item(rec), ConditionExpression=cond,
                            ExpressionAttributeNames=names, ExpressionAttributeValues=values)
            return True
        except Exception as e:  # noqa: BLE001
            rec["version"] = old
            if _conditional_failed(e):
                return False
            raise

    def _index_keys(self, shard):
        out, start = [], None
        while True:
            kw = {"TableName": self.t, "IndexName": self.INDEX, "KeyConditionExpression": "#s = :one",
                  "ExpressionAttributeNames": {"#s": "pending_shard"},
                  "ExpressionAttributeValues": {":one": {"S": shard}}}
            if start:
                kw["ExclusiveStartKey"] = start
            r = self.c.query(**kw)
            out += [it["pk"]["S"] for it in r.get("Items", [])]
            start = r.get("LastEvaluatedKey")
            if not start:
                return out

    def active(self):
        out = []
        for pk in self._index_keys("1"):
            rec = self.get(pk[4:])                            # the index is eventually consistent: re-read
            if rec is not None and rec["state"] == "ACCEPTED":
                out.append(rec)
        return out

    def tombstone_get(self, rid):
        it = self._get("KEY#" + rid)
        return {"rid": rid, "keep_until": int(it["expires_at"]["N"])} if it else None

    def tombstone_put(self, rid, keep_until):
        try:
            self.c.put_item(TableName=self.t, Item={"pk": {"S": "KEY#" + rid}, "expires_at": {"N": str(keep_until)}},
                            ConditionExpression="attribute_not_exists(pk)")
        except Exception as e:  # noqa: BLE001
            if not _conditional_failed(e):
                raise

    def sigreq_put(self, signer_rid, entry, keep_until):
        self.c.put_item(TableName=self.t, Item={"pk": {"S": "SIGREQ#" + signer_rid},
                                                "doc": {"S": json.dumps(entry, sort_keys=True)},
                                                "expires_at": {"N": str(keep_until)}})

    def sigreq_get(self, signer_rid):
        it = self._get("SIGREQ#" + signer_rid)
        return json.loads(it["doc"]["S"]) if it else None

    @staticmethod
    def _used_pk(request_id, signature_sha256):
        return f"SIGLOG#USED#{request_id}#{signature_sha256}"

    def siglog_add(self, entry):
        doc = {"S": json.dumps(entry, sort_keys=True)}
        if entry.get("disposition") == "used" and entry.get("request_id") and entry.get("signature_sha256"):
            try:                                      # append-only: a repeat of the same record gets its own key
                self.c.put_item(TableName=self.t, Item={"pk": {"S": self._used_pk(entry["request_id"],
                                                                                  entry["signature_sha256"])},
                                                        "doc": doc}, ConditionExpression="attribute_not_exists(pk)")
                return
            except Exception as e:  # noqa: BLE001
                if not _conditional_failed(e):
                    raise
        self.c.put_item(TableName=self.t, Item={"pk": {"S": "SIGLOG#" + uuid.uuid4().hex}, "doc": doc})

    def siglog_has(self, request_id, signature_sha256):
        return self._get(self._used_pk(request_id, signature_sha256)) is not None

    def cleanup_put(self, rid, doc):
        self.c.put_item(TableName=self.t, Item={"pk": {"S": "CLEAN#" + rid}, "pending_shard": {"S": "2"},
                                                "doc": {"S": json.dumps(doc, sort_keys=True)}})

    def cleanup_list(self):
        out = []
        for pk in self._index_keys("2"):
            it = self._get(pk)
            if it is not None:
                out.append((pk[len("CLEAN#"):], json.loads(it["doc"]["S"])))
        return out

    def cleanup_done(self, rid):
        self.c.delete_item(TableName=self.t, Key={"pk": {"S": "CLEAN#" + rid}})

    def active_page(self, token, limit):
        """ILC-I2-04: one page of the sparse pending index; the token is DynamoDB's LastEvaluatedKey."""
        kw = {"TableName": self.t, "IndexName": self.INDEX, "KeyConditionExpression": "#s = :one",
              "ExpressionAttributeNames": {"#s": "pending_shard"}, "ExpressionAttributeValues": {":one": {"S": "1"}},
              "Limit": limit}
        if token:
            kw["ExclusiveStartKey"] = token
        r = self.c.query(**kw)
        return [it["pk"]["S"][4:] for it in r.get("Items", [])], r.get("LastEvaluatedKey")

    def cursor_get(self):
        it = self._get("POLLER#cursor")
        return json.loads(it["doc"]["S"]) if it else None

    def cursor_put(self, position):
        self.c.put_item(TableName=self.t, Item={"pk": {"S": "POLLER#cursor"},
                                                "doc": {"S": json.dumps(position, sort_keys=True)}})

    def siglog(self):
        out, start = [], None
        while True:
            kw = {"TableName": self.t, "FilterExpression": "begins_with(pk, :p)",
                  "ExpressionAttributeValues": {":p": {"S": "SIGLOG#"}}}
            if start:
                kw["ExclusiveStartKey"] = start
            r = self.c.scan(**kw)
            out += [json.loads(it["doc"]["S"]) for it in r.get("Items", [])]
            start = r.get("LastEvaluatedKey")
            if not start:
                return out


class S3ResultStore(ResultStore):
    request_worst_s = AWS_WORST_S                 # ILC-I2-03: what the poller reserves for one write
    """Receipt URLs (IS-06): short-lived (<= 300 s) pre-signed GETs, minted per request after the API's credential check."""

    def __init__(self, client, bucket):
        self.c, self.b = GuardedClient(client, "s3"), bucket             # ILC-I-02: every request guarded

    @staticmethod
    def key(ns, rid, name):
        if ns not in NAMESPACES:
            raise ValueError(ns)
        return f"{ns}/{rid}/{name}"

    def put(self, ns, rid, name, data):
        self.c.put_object(Bucket=self.b, Key=self.key(ns, rid, name), Body=bytes(data), ServerSideEncryption="AES256")

    def _read(self, key):
        """ILC-I2-01: get_object returns before the body is read; the request and its body read are ONE guarded
        request, so the body read runs under the deadline too."""
        raw = self.c._client
        return guarded(AWS_WORST_S, lambda: raw.get_object(Bucket=self.b, Key=key)["Body"].read(),
                       what="s3.get_object")

    def get(self, ns, rid, name):
        try:
            return self._read(self.key(ns, rid, name))
        except Exception as e:  # noqa: BLE001
            if _not_found(e):
                return None
            raise

    DELETE_ROUNDS = 20                                # CF-04: listing pages (<= 1000 keys each) per call

    def delete(self, ns, rid):
        """Delete everything under (ns, rid). Raises on any per-object error S3 reports inside a successful
        DeleteObjects response, and after DELETE_ROUNDS pages, so one obligation can never hold the poller (CF-04);
        the caller keeps the obligation and the next poll continues."""
        prefix = self.key(ns, rid, "")
        for _ in range(self.DELETE_ROUNDS):           # list from the start each round: deleting never skips keys
            keys = [{"Key": o["Key"]} for o in self.c.list_objects_v2(Bucket=self.b, Prefix=prefix).get("Contents", [])]
            if not keys:
                return
            r = self.c.delete_objects(Bucket=self.b, Delete={"Objects": keys, "Quiet": True}) or {}
            errors = r.get("Errors") or []
            if errors:
                e = errors[0]
                raise OSError(f"S3 could not delete {len(errors)} object(s) under {prefix}: "
                              f"{e.get('Key')} {e.get('Code')} {e.get('Message', '')}".rstrip())
        raise OSError(f"deletion under {prefix} not finished after {self.DELETE_ROUNDS} rounds; continued next poll")

    def names(self, ns, rid):
        prefix, out, token = self.key(ns, rid, ""), [], None
        while True:
            kw = {"Bucket": self.b, "Prefix": prefix}
            if token:
                kw["ContinuationToken"] = token
            r = self.c.list_objects_v2(**kw)
            out += [o["Key"][len(prefix):] for o in r.get("Contents", [])]
            token = r.get("NextContinuationToken")
            if not token:
                return sorted(out)

    def mark_due(self, ns, rid):
        """Tag every object under (ns, rid) cleanup-due (5.3.1); the lifecycle backstop expires only tagged objects.
        A per-object error raises, and the obligation is retried."""
        for name in self.names(ns, rid):
            self.c.put_object_tagging(Bucket=self.b, Key=self.key(ns, rid, name),
                                      Tagging={"TagSet": [{"Key": CLEANUP_TAG[0], "Value": CLEANUP_TAG[1]}]})

    def size(self, ns, rid, name):
        try:
            return int(self.c.head_object(Bucket=self.b, Key=self.key(ns, rid, name))["ContentLength"])
        except Exception as e:  # noqa: BLE001
            if _not_found(e):
                return None
            raise

    def presign(self, ns, rid, name, expires_in, now):
        return self.c.generate_presigned_url(
            "get_object", Params={"Bucket": self.b, "Key": self.key(ns, rid, name)}, ExpiresIn=int(expires_in))

    def get_config(self, name):
        return self._read("config/" + name)


class SnsWake:
    """E-01: wake a slot's signer on demand by publishing to its topic (the signer side subscribes)."""

    def __init__(self, client, topics):
        self.c, self.topics = GuardedClient(client, "sns"), topics      # ILC-I-02: every request guarded

    def __call__(self, slot):
        arn = self.topics.get(slot)
        if arn:
            self.c.publish(TopicArn=arn, Message=json.dumps({"slot": slot, "event": "requests-queued"}))
