data "aws_caller_identity" "current" {}
data "aws_partition" "current" {}

data "aws_sqs_queue" "requests" {
  name = "${var.issuer_name}-kms-requests"
}

data "aws_sqs_queue" "responses" {
  name = "${var.issuer_name}-kms-responses"
}

locals {
  account   = data.aws_caller_identity.current.account_id
  root      = "arn:${data.aws_partition.current.partition}:iam::${local.account}:root"
  trail_arn = "arn:${data.aws_partition.current.partition}:cloudtrail:${var.region}:${local.account}:trail/${var.name}-trail"
  signer_env = {
    KMS_KEY_ID         = data.aws_kms_key.signer.arn
    KEY_FP             = var.key_fp
    SIGN_UNTIL         = var.sign_until
    RESPONSE_QUEUE_URL = data.aws_sqs_queue.responses.url
    FRAMES_BUCKET      = var.frames_bucket
  }
}

# ------------------------------------------------------------------------------------------------ the key
# The window's kms key already exists (kms_key_id); this module never creates one. (The provider pinned here,
# hashicorp/aws 5.100, does not accept customer_master_key_spec = "ML_DSA_65", so a new key is made outside
# Terraform, and is a new window key: new key assertion, new DNS record.)
data "aws_kms_key" "signer" {
  key_id = var.kms_key_id
}

# The signer role is the only principal allowed kms:Sign (and kms:GetPublicKey). Account administration keeps the
# key manageable but holds neither; the Deny makes an IAM grant of kms:Sign to any other principal ineffective, so
# obtaining a signature otherwise needs PutKeyPolicy or a change to the signer role or its code: management events,
# recorded by the trail below. That an IAM administrator can do those is C3 (README "Who can cause a signature").
data "aws_iam_policy_document" "key" {
  statement {
    sid = "KeyAdministrationWithoutSign"
    actions = [
      "kms:CancelKeyDeletion", "kms:CreateAlias", "kms:DeleteAlias", "kms:DescribeKey", "kms:DisableKey",
      "kms:EnableKey", "kms:GetKeyPolicy", "kms:GetKeyRotationStatus", "kms:ListAliases", "kms:ListGrants",
      "kms:ListKeyPolicies", "kms:ListResourceTags", "kms:PutKeyPolicy", "kms:RetireGrant", "kms:RevokeGrant",
      "kms:ScheduleKeyDeletion", "kms:TagResource", "kms:UntagResource", "kms:UpdateAlias", "kms:UpdateKeyDescription",
    ]
    resources = ["*"]
    principals {
      type        = "AWS"
      identifiers = [local.root]
    }
  }
  statement {
    sid       = "SignerRoleOnly"
    actions   = ["kms:Sign", "kms:GetPublicKey"]
    resources = ["*"]
    principals {
      type        = "AWS"
      identifiers = [aws_iam_role.signer.arn]
    }
  }
  statement {
    sid       = "DenySignToEveryoneElse"
    effect    = "Deny"
    actions   = ["kms:Sign"]
    resources = ["*"]
    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
    condition {
      test     = "ArnNotEquals"
      variable = "aws:PrincipalArn"
      values   = [aws_iam_role.signer.arn]
    }
  }
}

resource "aws_kms_key_policy" "signer" {
  key_id = data.aws_kms_key.signer.id
  policy = data.aws_iam_policy_document.key.json
}

# ------------------------------------------------------------------------------------------------ signer role
data "aws_iam_policy_document" "lambda_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "signer" {
  name               = "${var.name}-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
}

# Queues, frames and logs only. Signing rights come from the key policy above, not from IAM.
data "aws_iam_policy_document" "signer" {
  statement {
    sid       = "Requests"
    actions   = ["sqs:ReceiveMessage", "sqs:DeleteMessage", "sqs:GetQueueAttributes"]
    resources = [data.aws_sqs_queue.requests.arn]
  }
  statement {
    sid       = "Responses"
    actions   = ["sqs:SendMessage"]
    resources = [data.aws_sqs_queue.responses.arn]
  }
  # IS-09: frames too large for a queue message are read by digest-bound reference.
  statement {
    sid       = "Frames"
    actions   = ["s3:GetObject"]
    resources = ["arn:${data.aws_partition.current.partition}:s3:::${var.frames_bucket}/frames/*"]
  }
  statement {
    sid       = "Logs"
    actions   = ["logs:CreateLogStream", "logs:PutLogEvents"]
    resources = ["${aws_cloudwatch_log_group.signer.arn}:*"]
  }
}

resource "aws_iam_role_policy" "signer" {
  name   = "signer-kms"
  role   = aws_iam_role.signer.id
  policy = data.aws_iam_policy_document.signer.json
}

# ------------------------------------------------------------------------------------------------ Lambda
resource "aws_cloudwatch_log_group" "signer" {
  name              = "/aws/lambda/${var.name}"
  retention_in_days = var.log_retention_days
}

resource "aws_lambda_function" "signer" {
  function_name    = var.name
  role             = aws_iam_role.signer.arn
  runtime          = var.lambda_runtime
  handler          = "tessera_sign_kms.lambda_app.handler"
  filename         = var.lambda_zip
  source_code_hash = filebase64sha256(var.lambda_zip)
  timeout          = 60 # within the request queue's 120 s visibility timeout
  memory_size      = 512
  environment {
    variables = local.signer_env
  }
  depends_on = [aws_cloudwatch_log_group.signer, aws_iam_role_policy.signer]
}

resource "aws_lambda_event_source_mapping" "requests" {
  event_source_arn        = data.aws_sqs_queue.requests.arn
  function_name           = aws_lambda_function.signer.arn
  batch_size              = 10
  function_response_types = ["ReportBatchItemFailures"] # transient failures are redelivered, not dropped
  scaling_config {
    maximum_concurrency = 2
  }
}

# ------------------------------------------------------------------------------------------------ CloudTrail
# Management events, read and write, KMS not excluded: kms:Sign and kms:GetPublicKey are KMS management (read)
# events in CloudTrail, as are PutKeyPolicy, IAM and Lambda changes and StopLogging. Object Lock COMPLIANCE: what
# is written cannot be deleted or overwritten by anyone until its retention ends; stopping the trail is itself logged.
resource "aws_s3_bucket" "trail" {
  bucket_prefix       = "${var.name}-trail-"
  object_lock_enabled = true
}

resource "aws_s3_bucket_versioning" "trail" {
  bucket = aws_s3_bucket.trail.id
  versioning_configuration {
    status = "Enabled" # required by Object Lock
  }
}

resource "aws_s3_bucket_object_lock_configuration" "trail" {
  bucket = aws_s3_bucket.trail.id
  rule {
    default_retention {
      mode = "COMPLIANCE"
      days = var.trail_retention_days
    }
  }
  depends_on = [aws_s3_bucket_versioning.trail]
}

resource "aws_s3_bucket_public_access_block" "trail" {
  bucket                  = aws_s3_bucket.trail.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_ownership_controls" "trail" {
  bucket = aws_s3_bucket.trail.id
  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "trail" {
  bucket = aws_s3_bucket.trail.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256" # SSE-S3
    }
  }
}

data "aws_iam_policy_document" "trail_bucket" {
  statement {
    sid       = "CloudTrailAclCheck"
    actions   = ["s3:GetBucketAcl"]
    resources = [aws_s3_bucket.trail.arn]
    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }
    condition {
      test     = "StringEquals"
      variable = "aws:SourceArn"
      values   = [local.trail_arn]
    }
  }
  statement {
    sid       = "CloudTrailWrite"
    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.trail.arn}/AWSLogs/${local.account}/*"]
    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }
    condition {
      test     = "StringEquals"
      variable = "s3:x-amz-acl"
      values   = ["bucket-owner-full-control"]
    }
    condition {
      test     = "StringEquals"
      variable = "aws:SourceArn"
      values   = [local.trail_arn]
    }
  }
  statement {
    sid       = "DenyInsecureTransport"
    effect    = "Deny"
    actions   = ["s3:*"]
    resources = [aws_s3_bucket.trail.arn, "${aws_s3_bucket.trail.arn}/*"]
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

resource "aws_s3_bucket_policy" "trail" {
  bucket     = aws_s3_bucket.trail.id
  policy     = data.aws_iam_policy_document.trail_bucket.json
  depends_on = [aws_s3_bucket_public_access_block.trail]
}

resource "aws_cloudtrail" "signer" {
  name                          = "${var.name}-trail"
  s3_bucket_name                = aws_s3_bucket.trail.id
  is_multi_region_trail         = true
  include_global_service_events = true
  enable_log_file_validation    = true

  advanced_event_selector {
    name = "Management events, read and write, KMS included"
    field_selector {
      field  = "eventCategory"
      equals = ["Management"]
    }
  }

  depends_on = [aws_s3_bucket_policy.trail, aws_s3_bucket_object_lock_configuration.trail]
}
