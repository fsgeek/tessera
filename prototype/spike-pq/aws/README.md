# KMS spike permission set: scope and known limit

`kms-spike-permission-set.json` is an inline policy for an IAM Identity Center permission set. Replace `REGION`
and `ACCOUNT_ID` before use.

**Known limit (accepted).** The policy allows `kms:TagResource` because KMS requires that permission for
`CreateKey` to accept tags. A tag-based policy therefore can't fully stop this principal from tagging an *untagged*
pre-existing key `project=tessera` and so bringing it into scope. Keys tagged otherwise are protected by an explicit
deny, and untagging is denied.

**Why this is acceptable.** The policy is only for use in the dedicated Tessera account, which holds no keys except
those this principal creates. With no foreign key to escalate to, the gap can't be exploited.

**If the account ever holds other keys:** replace the tag conditions with explicit key ARNs once the spike's keys
exist, and remove `kms:CreateKey` and `kms:TagResource`.
