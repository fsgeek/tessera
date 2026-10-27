"""Message queues behind one interface: in memory (tests, local runs) and SQS (AWS). The in-memory queue enforces
SQS's message size limit."""
import itertools
from dataclasses import dataclass


@dataclass
class Message:
    id: str
    body: str
    handle: str


SQS_MAX_BYTES = 1048576              # SendMessage maximum message size


class Queue:
    def send(self, body):
        raise NotImplementedError

    def receive(self, max_messages=10, wait_s=0):
        raise NotImplementedError

    def delete(self, handle):
        raise NotImplementedError


class InMemoryQueue(Queue):
    """At-least-once queue with a visibility timeout, like SQS: a received message is hidden until it is deleted or
    its visibility timeout passes (measured on the given clock)."""

    def __init__(self, clock, visibility_s=300, max_bytes=SQS_MAX_BYTES):
        self.clock, self.visibility_s, self.max_bytes = clock, visibility_s, max_bytes
        self.msgs = {}                       # id -> {"body", "visible_at", "handle"}
        self._ids = itertools.count(1)

    def send(self, body):
        if len(body.encode()) > self.max_bytes:          # as SQS does (IS-09): the stand-in must not hide it
            raise ValueError(f"message of {len(body.encode())} bytes exceeds {self.max_bytes}")
        mid = f"m{next(self._ids)}"
        self.msgs[mid] = {"body": body, "visible_at": 0, "handle": None}
        return mid

    def receive(self, max_messages=10, wait_s=0):
        now, out = self.clock(), []
        for mid, m in self.msgs.items():
            if len(out) >= max_messages:
                break
            if m["visible_at"] <= now:
                m["visible_at"] = now + self.visibility_s
                m["handle"] = f"{mid}:{next(self._ids)}"
                out.append(Message(mid, m["body"], m["handle"]))
        return out

    def delete(self, handle):
        mid = handle.split(":")[0]
        m = self.msgs.get(mid)
        if m is not None and m["handle"] == handle:
            del self.msgs[mid]

    def __len__(self):
        return len(self.msgs)


class SqsQueue(Queue):
    """SQS through an injected boto3-style client (`boto3.client("sqs")`)."""

    def __init__(self, client, url):
        self.client, self.url = client, url

    def send(self, body):
        return self.client.send_message(QueueUrl=self.url, MessageBody=body)["MessageId"]

    def receive(self, max_messages=10, wait_s=0):
        r = self.client.receive_message(QueueUrl=self.url, MaxNumberOfMessages=max(1, min(10, max_messages)),
                                        WaitTimeSeconds=wait_s)
        return [Message(m["MessageId"], m["Body"], m["ReceiptHandle"]) for m in r.get("Messages", [])]

    def delete(self, handle):
        self.client.delete_message(QueueUrl=self.url, ReceiptHandle=handle)
