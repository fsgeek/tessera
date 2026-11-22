# Detection, step 4 (docs/V1-DETECTION-CONTRACT.md, the Arariwa item 0): the independent watcher (service/watcher).
# Every 10 minutes, under its own role, it reads the issuer's REQ#/SIGLOG# items, the results bucket (result/*) and the
# CloudTrail trail bucket, and writes only its own state bucket, its trace bucket, its log, the heartbeat metric and
# the alarm topic. It has no write access to any issuer store. D5, D6 (slot 1), D7 (IAM), D8, D9, trace records 0(a).

locals {
  # Trace records are kept until the window's issuance-not-after + 400 days (contract item 0(a)). Both numbers are
  # fixed here and in the watcher's code (lambda_app.TRACE_RETENTION_DAYS, which reads the window.json packaged in its
  # zip), not deploy inputs, so a later deploy cannot shorten either the writer's date or the policy's floor (M6).
  trace_retention_days = 400
  window               = jsondecode(file("${path.module}/../../issuer/config/window.json"))
  trace_retain_until   = timeadd(local.window.not_after, "${local.trace_retention_days * 24}h")
  trail_objects        = "${var.trail_prefix == "" ? "" : "${trimsuffix(var.trail_prefix, "/")}/"}AWSLogs/${local.account}/CloudTrail/"
  watcher_name         = "${var.name}-watcher"
}

data "aws_kms_key" "v1" {
  key_id = var.kms_key_id
}

data "aws_iam_role" "signer_kms" {
  name = var.signer_role_name
}

data "aws_dynamodb_table" "requests" {
  name = var.request_table
}

# ------------------------------------------------------------------------------------------ trace bucket, 0(a)
resource "aws_s3_bucket" "trace" {
  bucket_prefix       = "${local.watcher_name}-trace-"
  object_lock_enabled = true
}

resource "aws_s3_bucket_versioning" "trace" {
  bucket = aws_s3_bucket.trace.id
  versioning_configuration {
    status = "Enabled" # required by Object Lock
  }
}

# The watcher writes every record with an explicit COMPLIANCE retain-until date (local.trace_retain_until); the bucket
# policy refuses any put without it. The default retention (COMPLIANCE, fixed) is a floor for anything else. Once the
# bucket policy is in place it refuses PutBucketObjectLockConfiguration to every principal, so this cannot be
# changed by a later apply without first rewriting the policy (the stated operator residual).
resource "aws_s3_bucket_object_lock_configuration" "trace" {
  bucket = aws_s3_bucket.trace.id
  rule {
    default_retention {
      mode = "COMPLIANCE"
      days = local.trace_retention_days
    }
  }
  depends_on = [aws_s3_bucket_versioning.trace]
}

resource "aws_s3_bucket_public_access_block" "trace" {
  bucket                  = aws_s3_bucket.trace.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_ownership_controls" "trace" {
  bucket = aws_s3_bucket.trace.id
  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "trace" {
  bucket = aws_s3_bucket.trace.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

data "aws_iam_policy_document" "trace_bucket" {
  statement {
    sid       = "DenyInsecureTransport"
    effect    = "Deny"
    actions   = ["s3:*"]
    resources = [aws_s3_bucket.trace.arn, "${aws_s3_bucket.trace.arn}/*"]
    principals {
      type        = "*"
      identifiers = ["*"]
    }
    condition {
      test     = "Bool"
      variable = "aws:SecureTransport"
      values   = ["false"]
    }
  }
  statement {
    sid       = "DenyPutWithoutComplianceLock"
    effect    = "Deny"
    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.trace.arn}/*"]
    principals {
      type        = "*"
      identifiers = ["*"]
    }
    condition {
      test     = "StringNotEquals"
      variable = "s3:object-lock-mode"
      values   = ["COMPLIANCE"]
    }
  }
  statement {
    sid       = "DenyPutWithoutLockMode"
    effect    = "Deny"
    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.trace.arn}/*"]
    principals {
      type        = "*"
      identifiers = ["*"]
    }
    condition {
      test     = "Null"
      variable = "s3:object-lock-mode"
      values   = ["true"]
    }
  }
  statement {
    sid       = "DenyPutWithoutRetainUntil"
    effect    = "Deny"
    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.trace.arn}/*"]
    principals {
      type        = "*"
      identifiers = ["*"]
    }
    condition {
      test     = "Null"
      variable = "s3:object-lock-retain-until-date"
      values   = ["true"]
    }
  }
  statement {
    sid       = "DenyPutRetainedTooShort"
    effect    = "Deny"
    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.trace.arn}/*"]
    principals {
      type        = "*"
      identifiers = ["*"]
    }
    condition {
      test     = "DateLessThan"
      variable = "s3:object-lock-retain-until-date"
      values   = [local.trace_retain_until]
    }
  }
  # Only the watcher writes trace records.
  statement {
    sid       = "DenyPutByOthers"
    effect    = "Deny"
    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.trace.arn}/*"]
    principals {
      type        = "*"
      identifiers = ["*"]
    }
    condition {
      test     = "ArnNotEquals"
      variable = "aws:PrincipalArn"
      values   = [aws_iam_role.watcher.arn]
    }
  }
  # Nobody (the watcher included) places a delete marker over a record, deletes a version, or changes the lock
  # configuration: the current key stays the first record written (M6). An account administrator can still rewrite
  # this policy first (PutBucketPolicy, a D7 event); the locked versions survive even that.
  statement {
    sid       = "DenyDeleteAndLockChanges"
    effect    = "Deny"
    actions   = ["s3:DeleteObject", "s3:DeleteObjectVersion", "s3:PutBucketObjectLockConfiguration"]
    resources = [aws_s3_bucket.trace.arn, "${aws_s3_bucket.trace.arn}/*"]
    principals {
      type        = "*"
      identifiers = ["*"]
    }
  }
}

resource "aws_s3_bucket_policy" "trace" {
  bucket     = aws_s3_bucket.trace.id
  policy     = data.aws_iam_policy_document.trace_bucket.json
  depends_on = [aws_s3_bucket_public_access_block.trace, aws_s3_bucket_object_lock_configuration.trace]
}

# ------------------------------------------------------------------------------- state bucket (the cursor)
resource "aws_s3_bucket" "watcher_state" {
  bucket_prefix = "${local.watcher_name}-state-"
}

resource "aws_s3_bucket_versioning" "watcher_state" {
  bucket = aws_s3_bucket.watcher_state.id
  versioning_configuration {
    status = "Enabled" # earlier cursors stay readable for diagnosis
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "watcher_state" {
  bucket = aws_s3_bucket.watcher_state.id
  rule {
    id     = "old-cursors"
    status = "Enabled"
    filter {}
    noncurrent_version_expiration {
      noncurrent_days = 30
    }
  }
  depends_on = [aws_s3_bucket_versioning.watcher_state]
}

resource "aws_s3_bucket_public_access_block" "watcher_state" {
  bucket                  = aws_s3_bucket.watcher_state.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_ownership_controls" "watcher_state" {
  bucket = aws_s3_bucket.watcher_state.id
  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "watcher_state" {
  bucket = aws_s3_bucket.watcher_state.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

data "aws_iam_policy_document" "state_bucket" {
  statement {
    sid       = "DenyInsecureTransport"
    effect    = "Deny"
    actions   = ["s3:*"]
    resources = [aws_s3_bucket.watcher_state.arn, "${aws_s3_bucket.watcher_state.arn}/*"]
    principals {
      type        = "*"
      identifiers = ["*"]
    }
    condition {
      test     = "Bool"
      variable = "aws:SecureTransport"
      values   = ["false"]
    }
  }
  # Only the watcher writes or deletes its cursor and its finding outbox.
  statement {
    sid       = "DenyWritesByOthers"
    effect    = "Deny"
    actions   = ["s3:PutObject", "s3:DeleteObject", "s3:DeleteObjectVersion"]
    resources = ["${aws_s3_bucket.watcher_state.arn}/*"]
    principals {
      type        = "*"
      identifiers = ["*"]
    }
    condition {
      test     = "ArnNotEquals"
      variable = "aws:PrincipalArn"
      values   = [aws_iam_role.watcher.arn]
    }
  }
}

resource "aws_s3_bucket_policy" "watcher_state" {
  bucket     = aws_s3_bucket.watcher_state.id
  policy     = data.aws_iam_policy_document.state_bucket.json
  depends_on = [aws_s3_bucket_public_access_block.watcher_state]
}

# ------------------------------------------------------------------------------------------------- the role
data "aws_iam_policy_document" "watcher_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    condition {
      test     = "StringEquals"
      variable = "aws:SourceAccount"
      values   = [local.account]
    }
  }
}

resource "aws_iam_role" "watcher" {
  name               = local.watcher_name
  assume_role_policy = data.aws_iam_policy_document.watcher_assume.json
}

# Reads on the issuer's stores; writes only on the watcher's own. (Scan returns whole REQ# items, which include the
# plaintext request key; the watcher reads it to hash it and never writes or logs it.)
data "aws_iam_policy_document" "watcher" {
  statement {
    sid       = "IssuerTableRead"
    actions   = ["dynamodb:Scan", "dynamodb:GetItem", "dynamodb:DescribeTable"]
    resources = [data.aws_dynamodb_table.requests.arn]
  }
  statement {
    sid       = "ReceiptsRead"
    actions   = ["s3:GetObject"]
    resources = ["arn:aws:s3:::${var.results_bucket}/result/*"]
  }
  # Unconditional, so that GetObject on an absent receipt answers 404 (reported as RECEIPT_OBJECT_MISSING), not 403
  # (review H1). It lists keys only; it reads nothing outside result/*.
  statement {
    sid       = "ReceiptsList"
    actions   = ["s3:ListBucket"]
    resources = ["arn:aws:s3:::${var.results_bucket}"]
  }
  statement {
    sid       = "TrailList"
    actions   = ["s3:ListBucket"]
    resources = ["arn:aws:s3:::${var.trail_bucket}"]
  }
  statement {
    sid       = "TrailRead"
    actions   = ["s3:GetObject"]
    resources = ["arn:aws:s3:::${var.trail_bucket}/${local.trail_objects}*"]
  }
  statement {
    sid       = "StateReadWrite"
    actions   = ["s3:GetObject", "s3:PutObject"]
    resources = ["${aws_s3_bucket.watcher_state.arn}/state/*"]
  }
  statement {
    sid       = "FindingsOutbox"
    actions   = ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"]
    resources = ["${aws_s3_bucket.watcher_state.arn}/findings/*"]
  }
  statement {
    sid       = "StateList"
    actions   = ["s3:ListBucket"]
    resources = [aws_s3_bucket.watcher_state.arn]
  }
  statement {
    sid       = "TraceWrite"
    actions   = ["s3:GetObject", "s3:PutObject"]
    resources = ["${aws_s3_bucket.trace.arn}/trace/*"]
  }
  statement {
    sid       = "TraceList"
    actions   = ["s3:ListBucket"]
    resources = [aws_s3_bucket.trace.arn]
  }
  statement {
    sid       = "Findings"
    actions   = ["sns:Publish"]
    resources = [aws_sns_topic.alarms.arn]
  }
  statement {
    sid       = "Heartbeat"
    actions   = ["cloudwatch:PutMetricData"]
    resources = ["*"]
    condition {
      test     = "StringEquals"
      variable = "cloudwatch:namespace"
      values   = ["Tessera/Watcher"]
    }
  }
  statement {
    sid       = "Logs"
    actions   = ["logs:CreateLogStream", "logs:PutLogEvents"]
    resources = ["${aws_cloudwatch_log_group.watcher.arn}:*"]
  }
}

resource "aws_iam_role_policy" "watcher" {
  name   = "watcher"
  role   = aws_iam_role.watcher.id
  policy = data.aws_iam_policy_document.watcher.json
}

# ----------------------------------------------------------------------------------------------- the Lambda
resource "aws_cloudwatch_log_group" "watcher" {
  name              = "/aws/lambda/${local.watcher_name}"
  retention_in_days = var.watcher_log_retention_days
}

resource "aws_lambda_function" "watcher" {
  function_name                  = local.watcher_name
  role                           = aws_iam_role.watcher.arn
  runtime                        = var.lambda_runtime
  handler                        = "tessera_watch.lambda_app.handler"
  filename                       = var.watcher_zip
  source_code_hash               = filebase64sha256(var.watcher_zip)
  timeout                        = 600
  memory_size                    = 1024
  reserved_concurrent_executions = 1 # one run at a time; the state is also written with conditional puts
  environment {
    variables = {
      ACCOUNT_ID                  = local.account
      KMS_KEY_ARN                 = data.aws_kms_key.v1.arn
      KMS_ALIASES                 = join(",", [for a in [var.kms_key_id] : a if startswith(a, "alias/")])
      SIGNER_ROLE_ARN             = data.aws_iam_role.signer_kms.arn
      REQUEST_TABLE               = var.request_table
      RESULTS_BUCKET              = var.results_bucket
      TRAIL_BUCKET                = var.trail_bucket
      TRAIL_PREFIX                = var.trail_prefix
      STATE_BUCKET                = aws_s3_bucket.watcher_state.bucket
      STATE_KEY                   = "state/watcher.json"
      TRACE_BUCKET                = aws_s3_bucket.trace.bucket
      ALARM_TOPIC_ARN             = aws_sns_topic.alarms.arn
      EXPLORERS                   = jsonencode(var.explorers)
      CLIENT_KEY_IDS              = jsonencode(var.client_api_key_ids)
      TESSERA_VERIFY_INSTALL_JSON = "/var/task/tessera-verify/install.json"
      WATCHER_VERSION             = filesha256(var.watcher_zip)
    }
  }
  depends_on = [aws_cloudwatch_log_group.watcher, aws_iam_role_policy.watcher]
}

resource "aws_lambda_runtime_management_config" "watcher" {
  count               = var.runtime_version_arn == "" ? 0 : 1
  function_name       = aws_lambda_function.watcher.function_name
  update_runtime_on   = "Manual"
  runtime_version_arn = var.runtime_version_arn
}

resource "aws_cloudwatch_event_rule" "watcher" {
  name                = "${local.watcher_name}-schedule"
  description         = "The watcher's run (Arariwa item 0(b)): every 10 minutes"
  schedule_expression = "rate(10 minutes)"
}

resource "aws_cloudwatch_event_target" "watcher" {
  rule = aws_cloudwatch_event_rule.watcher.name
  arn  = aws_lambda_function.watcher.arn
}

resource "aws_lambda_permission" "watcher" {
  statement_id  = "AllowSchedule"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.watcher.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.watcher.arn
}

# ---------------------------------------------------------------------------------------------- D9: heartbeat
# One datapoint per committed, sound run (every 10 minutes; a run lasts at most its 600 s timeout). FILL(hb, 0) turns
# every 10-minute period without a heartbeat into an explicit 0, so the alarm does not depend on CloudWatch's
# missing-data look-back (review M7): it fires when three consecutive whole periods hold no heartbeat. With the last
# heartbeat anywhere in a period P0 and none in P1..P3, the alarm is evaluated at the end of P3: 30 to 40 minutes
# after that heartbeat, plus CloudWatch's evaluation delay (platform, typically a minute or two). It measures
# sustained silence: intermittent failures between sound runs do not fire it (Lambda errors and timeouts are the
# Errors alarm's, main.tf). treat_missing_data = breaching covers a metric that has never reported.
resource "aws_cloudwatch_metric_alarm" "watcher_heartbeat" {
  alarm_name          = "${local.watcher_name}-heartbeat"
  alarm_description   = "D9: no sound watcher run in three consecutive 10-minute periods (30-40 min of silence)"
  evaluation_periods  = 3
  datapoints_to_alarm = 3
  threshold           = 1
  comparison_operator = "LessThanThreshold"
  treat_missing_data  = "breaching"
  alarm_actions       = [aws_sns_topic.alarms.arn]
  ok_actions          = [aws_sns_topic.alarms.arn]

  metric_query {
    id          = "beats"
    expression  = "FILL(hb, 0)"
    label       = "Heartbeats per 10 minutes (missing as 0)"
    return_data = true
  }
  metric_query {
    id = "hb"
    metric {
      namespace   = "Tessera/Watcher"
      metric_name = "Heartbeat"
      period      = 600
      stat        = "Sum"
    }
  }
}
