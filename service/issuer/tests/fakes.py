"""In-memory stand-ins for the boto3 clients the AWS adapters use, implementing exactly the calls and condition
expressions the adapters make (no AWS, no network)."""
import copy
import io

from tessera_issue.queues import InMemoryQueue


class ClientError(Exception):
    def __init__(self, code):
        super().__init__(code)
        self.response = {"Error": {"Code": code}}


DYNAMO_ITEM_LIMIT = 400 * 1024                        # DynamoDB's item size limit, attribute names included


def dynamo_item_size(item):
    """Item size as DynamoDB counts it for these attribute types: UTF-8 name bytes plus value bytes (S: UTF-8
    length; N: an upper bound of its digits)."""
    total = 0
    for name, value in item.items():
        (kind, v), = value.items()
        total += len(name.encode()) + len(str(v).encode())
    return total


class FakeDynamo:
    def __init__(self):
        self.tables = {}
        self.calls = []
        self.max_item = 0

    def _check_size(self, item):
        size = dynamo_item_size(item)
        if size > DYNAMO_ITEM_LIMIT:
            raise ClientError("ValidationException")       # "Item size has exceeded the maximum allowed size"
        self.max_item = max(self.max_item, size)

    def _t(self, name):
        return self.tables.setdefault(name, {})

    def get_item(self, TableName, Key, ConsistentRead=False):
        self.calls.append("get_item")
        it = self._t(TableName).get(Key["pk"]["S"])
        return {"Item": copy.deepcopy(it)} if it else {}

    def put_item(self, TableName, Item, ConditionExpression=None, ExpressionAttributeNames=None,
                 ExpressionAttributeValues=None):
        self.calls.append("put_item")
        self._check_size(Item)
        t, pk = self._t(TableName), Item["pk"]["S"]
        cur = t.get(pk)
        if ConditionExpression == "attribute_not_exists(pk)":
            if cur is not None:
                raise ClientError("ConditionalCheckFailedException")
        elif ConditionExpression is not None and ConditionExpression.startswith("#v = :v"):
            # the version compare-and-set, optionally AND-ed with the lifecycle guard ("#x = :x" terms only)
            assert ExpressionAttributeNames["#v"] == "version"
            for term in ConditionExpression.split(" AND "):
                n, eq, v = term.split(" ")
                assert eq == "=" and n.startswith("#") and v.startswith(":"), term
                if cur is None or cur.get(ExpressionAttributeNames[n]) != ExpressionAttributeValues[v]:
                    raise ClientError("ConditionalCheckFailedException")
        elif ConditionExpression is not None:
            raise AssertionError("unexpected condition " + ConditionExpression)
        t[pk] = copy.deepcopy(Item)
        return {}

    def transact_write_items(self, TransactItems):
        """All-or-nothing: every condition is checked before anything is written."""
        self.calls.append("transact_write_items")
        for op in TransactItems:
            self._check_size(op["Put"]["Item"])
        reasons, ok = [], True
        for op in TransactItems:
            put = op["Put"]
            cur = self._t(put["TableName"]).get(put["Item"]["pk"]["S"])
            cond = put.get("ConditionExpression")
            assert cond in (None, "attribute_not_exists(pk)")
            if cond and cur is not None:
                reasons.append({"Code": "ConditionalCheckFailed"})
                ok = False
            else:
                reasons.append({"Code": "None"})
        if not ok:
            e = ClientError("TransactionCanceledException")
            e.response["CancellationReasons"] = reasons
            raise e
        for op in TransactItems:
            put = op["Put"]
            self._t(put["TableName"])[put["Item"]["pk"]["S"]] = copy.deepcopy(put["Item"])
        return {}

    def delete_item(self, TableName, Key):
        self.calls.append("delete_item")
        self._t(TableName).pop(Key["pk"]["S"], None)
        return {}

    def query(self, TableName, IndexName, KeyConditionExpression, ExpressionAttributeNames,
              ExpressionAttributeValues, ExclusiveStartKey=None, Limit=None):
        assert IndexName == "pending-index" and ExpressionAttributeNames == {"#s": "pending_shard"}
        items = [{"pk": it["pk"], "pending_shard": it["pending_shard"]} for it in self._t(TableName).values()
                 if it.get("pending_shard") == ExpressionAttributeValues[":one"]]
        start = int(ExclusiveStartKey["n"]["N"]) if ExclusiveStartKey else 0
        page = items[start:start + 2]                     # tiny pages: the adapter must paginate
        out = {"Items": page}
        if start + 2 < len(items):
            out["LastEvaluatedKey"] = {"n": {"N": str(start + 2)}}
        return out

    def scan(self, TableName, FilterExpression, ExpressionAttributeValues, ExclusiveStartKey=None):
        assert FilterExpression == "begins_with(pk, :p)"
        p = ExpressionAttributeValues[":p"]["S"]
        return {"Items": [copy.deepcopy(it) for k, it in self._t(TableName).items() if k.startswith(p)]}

    def ttl_sweep(self, table, now):
        t = self._t(table)
        for k in [k for k, it in t.items() if "expires_at" in it and int(it["expires_at"]["N"]) <= now]:
            del t[k]


class FakeS3:
    def __init__(self):
        self.objects = {}
        self.tags = {}
        self.put_args = []

    def put_object(self, Bucket, Key, Body, ServerSideEncryption=None):
        self.put_args.append(ServerSideEncryption)
        self.objects[(Bucket, Key)] = bytes(Body)
        self.tags.pop((Bucket, Key), None)            # a new object version has no tags

    def put_object_tagging(self, Bucket, Key, Tagging):
        if (Bucket, Key) not in self.objects:
            raise ClientError("NoSuchKey")
        self.tags[(Bucket, Key)] = {t["Key"]: t["Value"] for t in Tagging["TagSet"]}

    def generate_presigned_url(self, op, Params, ExpiresIn):
        assert op == "get_object"
        self.presigned = getattr(self, "presigned", []) + [(Params["Bucket"], Params["Key"], ExpiresIn)]
        return f"https://s3.test/{Params['Bucket']}/{Params['Key']}?X-Amz-Expires={ExpiresIn}"

    def get_object(self, Bucket, Key, Range=None):
        if (Bucket, Key) not in self.objects:
            raise ClientError("NoSuchKey")
        data = self.objects[(Bucket, Key)]
        if Range is not None:
            a, b = Range[len("bytes="):].split("-")
            data = data[int(a):int(b) + 1]
        return {"Body": io.BytesIO(data)}

    def head_object(self, Bucket, Key):
        if (Bucket, Key) not in self.objects:
            raise ClientError("404")
        return {"ContentLength": len(self.objects[(Bucket, Key)])}

    def list_objects_v2(self, Bucket, Prefix, ContinuationToken=None):
        keys = sorted(k for b, k in self.objects if b == Bucket and k.startswith(Prefix))
        start = int(ContinuationToken or 0)
        out = {"Contents": [{"Key": k} for k in keys[start:start + 3]]}
        if start + 3 < len(keys):
            out["NextContinuationToken"] = str(start + 3)
        return out

    fail_delete = staticmethod(lambda key: None)      # -> an S3 error code to report for this key, or None

    def delete_objects(self, Bucket, Delete):
        """Like S3: per-object failures come back in "Errors" of a successful response (Quiet mode)."""
        errors = []
        for o in Delete["Objects"]:
            code = self.fail_delete(o["Key"])
            if code:
                errors.append({"Key": o["Key"], "Code": code, "Message": "injected"})
            else:
                self.objects.pop((Bucket, o["Key"]), None)
                self.tags.pop((Bucket, o["Key"]), None)
        return {"Errors": errors} if errors else {}



class FakeSqs:
    def __init__(self, clock):
        self.queues, self.clock = {}, clock

    def q(self, url):
        return self.queues.setdefault(url, InMemoryQueue(self.clock))

    def send_message(self, QueueUrl, MessageBody):
        return {"MessageId": self.q(QueueUrl).send(MessageBody)}

    def receive_message(self, QueueUrl, MaxNumberOfMessages, WaitTimeSeconds, AttributeNames=()):
        out = []
        for m in self.q(QueueUrl).receive(MaxNumberOfMessages):
            msg = {"MessageId": m.id, "Body": m.body, "ReceiptHandle": m.handle}
            attrs = {}
            if "SentTimestamp" in AttributeNames or "All" in AttributeNames:     # as SQS: epoch milliseconds
                attrs["SentTimestamp"] = str(int(m.sent * 1000))
            if "ApproximateReceiveCount" in AttributeNames or "All" in AttributeNames:
                attrs["ApproximateReceiveCount"] = str(m.receives)
            if attrs:
                msg["Attributes"] = attrs
            out.append(msg)
        return {"Messages": out}

    def delete_message(self, QueueUrl, ReceiptHandle):
        self.q(QueueUrl).delete(ReceiptHandle)


class FakeSns:
    def __init__(self):
        self.published = []

    def publish(self, TopicArn, Message):
        self.published.append((TopicArn, Message))


class FakeSession:
    def __init__(self, **clients):
        self.clients = clients

    def client(self, name):
        return self.clients[name]
