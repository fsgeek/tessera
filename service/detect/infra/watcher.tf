# Detection, step 4 (docs/V1-DETECTION-CONTRACT.md, the Arariwa item 0): the independent watcher (service/watcher).
# Every 10 minutes, under its own role, it reads the issuer's REQ#/SIGLOG# items, the results bucket (result/*) and the
# CloudTrail trail bucket, and writes only its own state bucket, its trace bucket, its log, the heartbeat metric and
# the alarm topic. It has no write access to any issuer store. D5, D6 (slot 1), D7 (IAM), D8, D9, trace records 0(a).

locals {
  # Trace records are kept until the window's issuance-not-after + trace_retention_days_after_window (contract: 400).
  window             = jsondecode(file("${path.module}/../../issuer/config/window.json"))
  trace_retain_until = timeadd(local.window.not_after, "${var.trace_retention_days_after_window * 24}h")
  trail_objects      = "${var.trail_prefix == "" ? "" : "${trimsuffix(var.trail_prefix, "/")}/"}AWSLogs/${local.account}/CloudTrail/"
  watcher_name       = "${var.name}-watcher"
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
# policy refuses any put without it. The default retention is a floor for nothing else.
resource "aws_s3_bucket_object_lock_configuration" "trace" {
  bucket = aws_s3_bucket.trace.id
  rule {
    default_retention {
      mode = "COMPLIANCE"
      days = var.trace_default_retention_days
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
}

resource "aws_s3_bucket_policy" "trace" {
  bucket     = aws_s3_bucket.trace.id
  policy     = data.aws_iam_policy_document.trace_bucket.json
  depends_on = [aws_s3_bucket_public_access_block.trace]
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
    sid       = "StateList"
    actions   = ["s3:ListBucket"]
    resources = [aws_s3_bucket.watcher_state.arn]
  }
  statement {
    sid       = "TraceWrite"
    actions   = ["s3:GetObject", "s3:PutObject", "s3:PutObjectRetention"]
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
      TRACE_RETAIN_UNTIL          = local.trace_retain_until
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
# One datapoint per committed run (every 10 minutes). Three empty 10-minute periods, i.e. 30 minutes without a
# committed run, is an alarm; missing data is breaching, so a dead, failing or deleted watcher alarms by silence.
resource "aws_cloudwatch_metric_alarm" "watcher_heartbeat" {
  alarm_name          = "${local.watcher_name}-heartbeat"
  alarm_description   = "D9: the watcher has not completed a run for 30 minutes"
  namespace           = "Tessera/Watcher"
  metric_name         = "Heartbeat"
  statistic           = "Sum"
  period              = 600
  evaluation_periods  = 3
  datapoints_to_alarm = 3
  threshold           = 1
  comparison_operator = "LessThanThreshold"
  treat_missing_data  = "breaching"
  alarm_actions       = [aws_sns_topic.alarms.arn]
  ok_actions          = [aws_sns_topic.alarms.arn]
}
