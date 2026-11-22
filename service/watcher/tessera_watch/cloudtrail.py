"""Reading the multi-region CloudTrail trail from its S3 bucket, and classifying the events the watcher acts on.

Layout (an account trail, not an organization trail): <prefix>AWSLogs/<account>/CloudTrail/<region>/YYYY/MM/DD/
<account>_CloudTrail_<region>_YYYYMMDDTHHMMZ_<random>.json.gz, each a gzipped {"Records": [...]}. Digest files live
under CloudTrail-Digest/ and are not read. Global IAM events are delivered in the us-east-1 files of a multi-region
trail; every region present in the bucket is read, so the reader does not depend on where an event lands.

Which file is new: every key whose timestamp is at or after the trail cursor is read once; the set of keys read is
part of the durable state. The cursor is the watcher's own clock minus an hour at its last commit, held back to the
oldest file it could not read (watcher.read_trail). A file that appears in the bucket more than that hour after its
key timestamp, while the cursor has moved past it, is never read (stated in README)."""
import calendar
import datetime as dt
import gzip
import json
import re

KEY_TS = re.compile(r"_CloudTrail_[a-z0-9-]+_(\d{8}T\d{4}Z)_[A-Za-z0-9]+\.json\.gz\Z")
KEY_PARTS = re.compile(r"_CloudTrail_([a-z]{2}(?:-[a-z]+)+-[0-9])_(\d{8}T\d{4}Z)_[A-Za-z0-9]+\.json\.gz\Z")
ACCESS_DENIED = {"AccessDenied", "AccessDeniedException"}


def key_time(key):
    m = KEY_TS.search(key)
    if not m:
        return None
    try:
        return calendar.timegm(dt.datetime.strptime(m.group(1), "%Y%m%dT%H%MZ").timetuple())
    except ValueError:
        return None


def safe_parts(key):
    """What a finding may say about a trail file: its region and key timestamp, from the fixed key pattern only."""
    m = KEY_PARTS.search(key) if isinstance(key, str) else None
    return {"region": m.group(1), "file_time": m.group(2)} if m else {"region": None, "file_time": None}


def event_time(rec):
    try:
        return calendar.timegm(dt.datetime.strptime(rec["eventTime"], "%Y-%m-%dT%H:%M:%SZ").timetuple())
    except (KeyError, TypeError, ValueError, OverflowError):
        return None


def base_prefix(prefix, account):
    p = (prefix or "").strip("/")
    return (p + "/" if p else "") + f"AWSLogs/{account}/CloudTrail/"


def _list(s3, bucket, prefix, delimiter=None):
    out, token = [], None
    while True:
        kw = {"Bucket": bucket, "Prefix": prefix}
        if delimiter:
            kw["Delimiter"] = delimiter
        if token:
            kw["ContinuationToken"] = token
        r = s3.list_objects_v2(**kw)
        out += [c["Prefix"] for c in r.get("CommonPrefixes", [])] if delimiter else \
               [o["Key"] for o in r.get("Contents", [])]
        token = r.get("NextContinuationToken")
        if not token:
            return out


def candidate_keys(s3, bucket, base, since, until):
    """Log-file keys with a timestamp in [since, until + 1 h], every region present under the trail prefix."""
    regions = _list(s3, bucket, base, delimiter="/")
    days, t = [], since - since % 86400
    while t <= until:
        days.append(dt.datetime.fromtimestamp(t, dt.UTC).strftime("%Y/%m/%d/"))
        t += 86400
    keys = []
    for rp in regions:
        for day in days:
            for k in _list(s3, bucket, rp + day):
                kt = key_time(k)
                if kt is not None and since <= kt <= until + 3600:
                    keys.append(k)
    return sorted(keys)


def parse(raw):
    """Gzipped CloudTrail log file -> list of records. Raises ValueError if it is not one."""
    try:
        doc = json.loads(gzip.decompress(raw))
    except (OSError, EOFError, ValueError) as e:
        raise ValueError(type(e).__name__) from None
    recs = doc.get("Records") if isinstance(doc, dict) else None
    if not isinstance(recs, list):
        raise ValueError("no Records")
    return [r for r in recs if isinstance(r, dict)]


def principal(rec):
    """The acting role's ARN for an assumed-role session, else the identity's ARN (or its type)."""
    ui = rec.get("userIdentity") or {}
    issuer = ((ui.get("sessionContext") or {}).get("sessionIssuer") or {})
    if ui.get("type") == "AssumedRole" and issuer.get("arn"):
        return issuer["arn"]
    return ui.get("arn") or ui.get("type") or "unknown"


class KeyRefs:
    """Every way an event can name the v1 key: its ARN, its id, an alias name or an alias ARN."""

    def __init__(self, key_arn, aliases=()):
        self.arn = key_arn
        key_id = key_arn.rsplit("/", 1)[-1]
        region_account = key_arn.split(":key/")[0]                  # arn:aws:kms:<region>:<account>
        names = {key_arn, key_id}
        for a in aliases:
            names.add(a)
            names.add(f"{region_account}:{a}")
        self.names = names

    def matches(self, rec):
        if any(isinstance(r, dict) and r.get("ARN") == self.arn for r in rec.get("resources") or []):
            return True
        return ((rec.get("requestParameters") or {}).get("keyId")) in self.names


def read_only(rec):
    v = rec.get("readOnly")
    return v is True or (isinstance(v, str) and v.lower() == "true")


def classify(rec, key, signer_role_arn):
    """-> list of (kind, detail) for one record. Kinds: "sign" (a successful kms:Sign on the key by the signer
    role, D6, reconciled), "foreign_sign" (a successful one by any other principal, D6, an alarm by itself), "access_denied" (any AccessDenied on the key, D6),
    "iam_write" (any IAM write event, D7)."""
    out = []
    src, name, err = rec.get("eventSource"), rec.get("eventName"), rec.get("errorCode")
    who = principal(rec)
    base = {"event_id": rec.get("eventID"), "event_time": rec.get("eventTime"), "event_name": name,
            "principal": who, "region": rec.get("awsRegion"), "error_code": err}
    if src == "kms.amazonaws.com" and key.matches(rec):
        if err in ACCESS_DENIED:
            out.append(("access_denied", base))
        elif name == "Sign" and not err:
            out.append(("sign" if who == signer_role_arn else "foreign_sign", base))
    if src == "iam.amazonaws.com" and not read_only(rec):
        out.append(("iam_write", base))
    return out
