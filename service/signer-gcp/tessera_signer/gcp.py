"""The real adapters: the Google metadata server (access and ID tokens for the job's own service account), Cloud KMS
over REST with CRC32C integrity checks, and AWS credentials by web identity federation. No static credential of any
kind: the job runs as its service account, and AWS trusts a Google-issued ID token for that account.

AWS credentials (README "AWS credentials"): the metadata server mints an ID token for this service account with the
configured audience; STS AssumeRoleWithWebIdentity exchanges it for a role in the issuing AWS account whose trust
names accounts.google.com with this account's unique ID (sub, aud) and the audience (oaud). If a second role is
configured (chain_role_arn), those credentials then AssumeRole into it: that is how the issuer's Terraform signer
role (principal = the first role's ARN) is reached without a Terraform change. Sessions last 900 s; one run is far
shorter."""
import base64
import json
import urllib.error
import urllib.parse
import urllib.request

MD = "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/"
KMS = "https://cloudkms.googleapis.com/v1/"
SESSION_S = 900


def crc32c(data):
    crc = 0xFFFFFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            crc = (crc >> 1) ^ (0x82F63B78 & -(crc & 1))
    return crc ^ 0xFFFFFFFF


def http(method, url, headers, body=None, timeout=30):
    """-> response bytes; raises RuntimeError with the status on an HTTP error."""
    req = urllib.request.Request(url, method=method, data=body, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{method} {url.split('?')[0]}: HTTP {e.code} {e.read()[:300]!r}") from None


class Metadata:
    def __init__(self, fetch=http):
        self.fetch = fetch

    def _get(self, path):
        return self.fetch("GET", MD + path, {"Metadata-Flavor": "Google"}, timeout=10).decode()

    def access_token(self):
        return json.loads(self._get("token"))["access_token"]

    def id_token(self, audience):
        return self._get(f"identity?audience={urllib.parse.quote(audience, safe='')}&format=full")


class GcpKms:
    """One key version: its public key, and asymmetricSign over a SHA-256 digest with request and response
    CRC32C checks (Cloud KMS data integrity guidelines)."""

    def __init__(self, key_version, token, fetch=http):
        self.key_version, self.token, self.fetch = key_version, token, fetch

    def _call(self, method, suffix, body=None):
        data = None if body is None else json.dumps(body).encode()
        out = self.fetch(method, KMS + self.key_version + suffix,
                         {"Authorization": "Bearer " + self.token(), "Content-Type": "application/json"}, data)
        return json.loads(out)

    def public_key(self):
        pk = self._call("GET", "/publicKey")
        if "pemCrc32c" in pk and int(pk["pemCrc32c"]) != crc32c(pk.get("pem", "").encode()):
            raise RuntimeError("KMS public key CRC32C mismatch")
        return pk

    def sign_digest(self, digest):
        out = self._call("POST", ":asymmetricSign", {"digest": {"sha256": base64.b64encode(digest).decode()},
                                                     "digestCrc32c": str(crc32c(digest))})
        if out.get("name") != self.key_version or out.get("verifiedDigestCrc32c") is not True:
            raise RuntimeError(f"KMS response integrity: name={out.get('name')} "
                               f"verified={out.get('verifiedDigestCrc32c')}")
        der = base64.b64decode(out["signature"])
        if int(out["signatureCrc32c"]) != crc32c(der):
            raise RuntimeError("KMS signature CRC32C mismatch")
        return der


def aws_clients(role_arn, audience, region, id_token, make_client, chain_role_arn=None):
    """-> (sqs, s3) clients on federated credentials. make_client(service, region, credentials-or-None)."""
    sts = make_client("sts", region, None)
    creds = sts.assume_role_with_web_identity(RoleArn=role_arn, RoleSessionName="tessera-signer-gpg",
                                              WebIdentityToken=id_token(audience),
                                              DurationSeconds=SESSION_S)["Credentials"]
    if chain_role_arn:
        sts2 = make_client("sts", region, creds)
        creds = sts2.assume_role(RoleArn=chain_role_arn, RoleSessionName="tessera-signer-gpg",
                                 DurationSeconds=SESSION_S)["Credentials"]
    return make_client("sqs", region, creds), make_client("s3", region, creds)


def boto3_client(service, region, creds):
    import boto3
    if creds is None:
        return boto3.client(service, region_name=region)
    return boto3.client(service, region_name=region, aws_access_key_id=creds["AccessKeyId"],
                        aws_secret_access_key=creds["SecretAccessKey"], aws_session_token=creds["SessionToken"])
