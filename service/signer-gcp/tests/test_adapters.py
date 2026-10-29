"""The real adapters over fake transports: Cloud KMS REST integrity checks and the AWS web-identity exchange."""
import base64
import json

import pytest

from tessera_signer import gcp


def test_crc32c_check_value():
    assert gcp.crc32c(b"123456789") == 0xE3069283        # the CRC-32C (Castagnoli) check value


class Http:
    def __init__(self, reply):
        self.reply, self.calls = reply, []

    def __call__(self, method, url, headers, body=None, timeout=30):
        self.calls.append((method, url, headers, body))
        return json.dumps(self.reply(method, url, body)).encode()


KV = "projects/p/locations/l/keyRings/r/cryptoKeys/k/cryptoKeyVersions/1"
SIG = b"\x30\x06\x02\x01\x01\x02\x01\x01"


def sign_reply(name=KV, verified=True, sig=SIG, crc=None):
    return lambda m, u, b: {"name": name, "verifiedDigestCrc32c": verified,
                            "signature": base64.b64encode(sig).decode(),
                            "signatureCrc32c": str(gcp.crc32c(sig) if crc is None else crc)}


def test_kms_sign_sends_digest_and_crc():
    http = Http(sign_reply())
    k = gcp.GcpKms(KV, lambda: "tok", http)
    assert k.sign_digest(b"\x01" * 32) == SIG
    method, url, headers, body = http.calls[0]
    assert method == "POST" and url == gcp.KMS + KV + ":asymmetricSign"
    assert headers["Authorization"] == "Bearer tok"
    sent = json.loads(body)
    assert base64.b64decode(sent["digest"]["sha256"]) == b"\x01" * 32
    assert sent["digestCrc32c"] == str(gcp.crc32c(b"\x01" * 32))


@pytest.mark.parametrize("reply,match", [
    (sign_reply(name=KV.replace("/1", "/2")), "integrity"),
    (sign_reply(verified=False), "integrity"),
    (sign_reply(crc=1), "CRC32C"),
])
def test_kms_sign_integrity_failures_raise(reply, match):
    with pytest.raises(RuntimeError, match=match):
        gcp.GcpKms(KV, lambda: "tok", Http(reply)).sign_digest(b"\x01" * 32)


def test_kms_public_key_crc_checked():
    pem = "-----BEGIN PUBLIC KEY-----\n...\n"
    ok = gcp.GcpKms(KV, lambda: "t", Http(lambda m, u, b: {"pem": pem, "pemCrc32c": str(gcp.crc32c(pem.encode()))}))
    assert ok.public_key()["pem"] == pem
    bad = gcp.GcpKms(KV, lambda: "t", Http(lambda m, u, b: {"pem": pem, "pemCrc32c": "1"}))
    with pytest.raises(RuntimeError, match="CRC32C"):
        bad.public_key()


def test_metadata_id_token_requests_the_audience():
    seen = []

    def fetch(method, url, headers, body=None, timeout=30):
        seen.append((url, headers))
        return b"id-token"
    assert gcp.Metadata(fetch).id_token("tessera slot2/sqs") == "id-token"
    url, headers = seen[0]
    assert url == gcp.MD + "identity?audience=tessera%20slot2%2Fsqs&format=full"
    assert headers == {"Metadata-Flavor": "Google"}


class Sts:
    def __init__(self, log, creds):
        self.log, self.creds = log, creds

    def assume_role_with_web_identity(self, **kw):
        self.log.append(("web", kw, self.creds))
        return {"Credentials": {"AccessKeyId": "A1", "SecretAccessKey": "S1", "SessionToken": "T1"}}

    def assume_role(self, **kw):
        self.log.append(("chain", kw, self.creds))
        return {"Credentials": {"AccessKeyId": "A2", "SecretAccessKey": "S2", "SessionToken": "T2"}}


def make_factory(log):
    def make(service, region, creds):
        if service == "sts":
            return Sts(log, creds)
        log.append((service, region, creds))
        return service
    return make


def test_aws_web_identity_only():
    log = []
    sqs, s3 = gcp.aws_clients("arn:web", "aud", "us-east-2", lambda a: f"tok:{a}", make_factory(log))
    assert (sqs, s3) == ("sqs", "s3")
    web = log[0]
    assert web[0] == "web" and web[2] is None                       # no credential: the ID token is the proof
    assert web[1]["RoleArn"] == "arn:web" and web[1]["WebIdentityToken"] == "tok:aud"
    assert [e[2]["AccessKeyId"] for e in log[1:]] == ["A1", "A1"]


def test_aws_web_identity_then_chain():
    log = []
    gcp.aws_clients("arn:web", "aud", "us-east-2", lambda a: "tok", make_factory(log), chain_role_arn="arn:signer")
    assert log[1][0] == "chain" and log[1][1]["RoleArn"] == "arn:signer" and log[1][2]["AccessKeyId"] == "A1"
    assert [e[2]["AccessKeyId"] for e in log[2:]] == ["A2", "A2"]  # queues and frames on the chained role
