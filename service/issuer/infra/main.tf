locals {
  slots     = ["kms", "gpg"]
  retention = 30
  lambda_env = {
    REQUEST_TABLE               = aws_dynamodb_table.requests.name
    RESULT_BUCKET               = aws_s3_bucket.results.bucket
    FREEZE_DIR                  = "/var/task/freeze-v1/objects"
    WINDOW_OBJECT               = "window.json"
    TESSERA_VERIFY_INSTALL_JSON = "/var/task/tessera-verify/install.json"
    KMS_REQUEST_QUEUE_URL       = aws_sqs_queue.requests["kms"].url
    KMS_RESPONSE_QUEUE_URL      = aws_sqs_queue.responses["kms"].url
    GPG_REQUEST_QUEUE_URL       = aws_sqs_queue.requests["gpg"].url
    GPG_RESPONSE_QUEUE_URL      = aws_sqs_queue.responses["gpg"].url
    KMS_WAKE_TOPIC_ARN          = aws_sns_topic.wake["kms"].arn
    GPG_WAKE_TOPIC_ARN          = aws_sns_topic.wake["gpg"].arn
    OTS_CALENDARS               = join(",", var.ots_calendars)
    EXPLORERS                   = join(",", var.explorers)
    DNS_RESOLVER                = var.dns_resolver
    CLOSING                     = tostring(var.closing)
    SIGNING_AVAILABLE           = tostring(var.signing_available)
  }
}

# ------------------------------------------------------------------------------------------------ request store
resource "aws_dynamodb_table" "requests" {
  name         = "${var.name}-requests"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"

  attribute {
    name = "pk"
    type = "S"
  }

  attribute {
    name = "pending_shard"
    type = "S"
  }

  global_secondary_index {
    name            = "pending-index"
    hash_key        = "pending_shard"
    projection_type = "KEYS_ONLY"
  }

  # S5/S6: records expire 30 days after the request ends; key tombstones after issuance closes.
  ttl {
    attribute_name = "expires_at"
    enabled        = true
  }

  point_in_time_recovery {
    enabled = true
  }

  server_side_encryption {
    enabled = false # AWS-owned key; the issuer has no KMS permissions
  }
}

# ------------------------------------------------------------------------------------------------ result store
resource "aws_s3_bucket" "results" {
  bucket_prefix = "${var.name}-results-"
}

resource "aws_s3_bucket_public_access_block" "results" {
  bucket                  = aws_s3_bucket.results.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_ownership_controls" "results" {
  bucket = aws_s3_bucket.results.id
  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "results" {
  bucket = aws_s3_bucket.results.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256" # SSE-S3, not SSE-KMS
    }
  }
}

resource "aws_s3_bucket_versioning" "results" {
  bucket = aws_s3_bucket.results.id
  versioning_configuration {
    status = "Disabled" # S6: no hidden copies outlive the 30-day deletion
  }
}

# S6: the poller deletes content, work files and frames when a request ends, and the receipt 30 days after the end,
# from persisted cleanup obligations it retries until the objects are gone (IS-07). These lifecycle rules are only a
# backstop: S3 expires objects asynchronously, from the next midnight after eligibility, so they cannot implement
# deletion at exactly 30 days. The 31-day backstop never removes a receipt the service still promises.
resource "aws_s3_bucket_lifecycle_configuration" "results" {
  bucket = aws_s3_bucket.results.id

  dynamic "rule" {
    for_each = ["content/", "work/", "frames/", "result/"]
    content {
      id     = "expire-${trimsuffix(rule.value, "/")}"
      status = "Enabled"
      filter {
        prefix = rule.value
      }
      expiration {
        days = local.retention + 1
      }
      abort_incomplete_multipart_upload {
        days_after_initiation = 1
      }
    }
  }
}

resource "aws_s3_bucket_policy" "results_tls_only" {
  bucket = aws_s3_bucket.results.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid       = "DenyInsecureTransport"
      Effect    = "Deny"
      Principal = "*"
      Action    = "s3:*"
      Resource  = [aws_s3_bucket.results.arn, "${aws_s3_bucket.results.arn}/*"]
      Condition = { Bool = { "aws:SecureTransport" = "false" } }
    }]
  })
}

# ------------------------------------------------------------------------------------------------ signer queues
resource "aws_sqs_queue" "requests" {
  for_each                   = toset(local.slots)
  name                       = "${var.name}-${each.key}-requests"
  message_retention_seconds  = 86400
  visibility_timeout_seconds = 120
  sqs_managed_sse_enabled    = true
}

resource "aws_sqs_queue" "responses" {
  for_each                   = toset(local.slots)
  name                       = "${var.name}-${each.key}-responses"
  message_retention_seconds  = 1209600 # 14 days: late answers stay until the poller logs and deletes them (E-02)
  visibility_timeout_seconds = 60
  sqs_managed_sse_enabled    = true
}

# E-01: the issuer wakes a slot's signer on demand; the signer side subscribes.
resource "aws_sns_topic" "wake" {
  for_each = toset(local.slots)
  name     = "${var.name}-${each.key}-wake"
}

# ------------------------------------------------------------------------------------------------ IAM
data "aws_iam_policy_document" "lambda_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "api" {
  name               = "${var.name}-api"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
}

resource "aws_iam_role" "poller" {
  name               = "${var.name}-poller"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
}

# No statement in either issuer policy grants any kms: action (tests/test_infra.py checks this).
data "aws_iam_policy_document" "api" {
  statement {
    sid       = "Requests"
    actions   = ["dynamodb:GetItem", "dynamodb:PutItem"]
    resources = [aws_dynamodb_table.requests.arn]
  }
  # IS-10: the API writes submitted content (and removes it if its request ended meanwhile) and reads receipts.
  statement {
    sid       = "WriteContent"
    actions   = ["s3:PutObject", "s3:DeleteObject"]
    resources = ["${aws_s3_bucket.results.arn}/content/*"]
  }
  statement {
    sid       = "ReadResults"
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.results.arn}/result/*"]
  }
  statement {
    sid       = "ListContent"
    actions   = ["s3:ListBucket"]
    resources = [aws_s3_bucket.results.arn]
    condition {
      test     = "StringLike"
      variable = "s3:prefix"
      values   = ["content/*"]
    }
  }
  statement {
    sid       = "Config"
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.results.arn}/config/*"]
  }
  statement {
    sid       = "Logs"
    actions   = ["logs:CreateLogStream", "logs:PutLogEvents"]
    resources = ["${aws_cloudwatch_log_group.api.arn}:*"]
  }
}

data "aws_iam_policy_document" "poller" {
  statement {
    sid       = "Requests"
    actions   = ["dynamodb:GetItem", "dynamodb:PutItem", "dynamodb:DeleteItem", "dynamodb:Query", "dynamodb:Scan"]
    resources = [aws_dynamodb_table.requests.arn, "${aws_dynamodb_table.requests.arn}/index/pending-index"]
  }
  # IS-10: mutation only in the operational namespaces; configuration is read-only.
  statement {
    sid       = "Objects"
    actions   = ["s3:PutObject", "s3:GetObject", "s3:DeleteObject"]
    resources = ["${aws_s3_bucket.results.arn}/content/*", "${aws_s3_bucket.results.arn}/work/*", "${aws_s3_bucket.results.arn}/frames/*", "${aws_s3_bucket.results.arn}/result/*"]
  }
  statement {
    sid       = "Config"
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.results.arn}/config/*"]
  }
  statement {
    sid       = "List"
    actions   = ["s3:ListBucket"]
    resources = [aws_s3_bucket.results.arn]
  }
  statement {
    sid       = "SignerRequests"
    actions   = ["sqs:SendMessage"]
    resources = [for q in aws_sqs_queue.requests : q.arn]
  }
  statement {
    sid       = "SignerResponses"
    actions   = ["sqs:ReceiveMessage", "sqs:DeleteMessage", "sqs:GetQueueAttributes"]
    resources = [for q in aws_sqs_queue.responses : q.arn]
  }
  statement {
    sid       = "Wake"
    actions   = ["sns:Publish"]
    resources = [for t in aws_sns_topic.wake : t.arn]
  }
  statement {
    sid       = "Logs"
    actions   = ["logs:CreateLogStream", "logs:PutLogEvents"]
    resources = ["${aws_cloudwatch_log_group.poller.arn}:*"]
  }
}

resource "aws_iam_role_policy" "api" {
  name   = "issuer-api"
  role   = aws_iam_role.api.id
  policy = data.aws_iam_policy_document.api.json
}

resource "aws_iam_role_policy" "poller" {
  name   = "issuer-poller"
  role   = aws_iam_role.poller.id
  policy = data.aws_iam_policy_document.poller.json
}

# The remote signers' queue access (each slot sees only its own queues). Their signing keys are elsewhere.
data "aws_iam_policy_document" "signer_assume" {
  for_each = var.signer_principals
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "AWS"
      identifiers = [each.value]
    }
  }
}

resource "aws_iam_role" "signer" {
  for_each           = var.signer_principals
  name               = "${var.name}-signer-${each.key}"
  assume_role_policy = data.aws_iam_policy_document.signer_assume[each.key].json
}

data "aws_iam_policy_document" "signer" {
  for_each = var.signer_principals
  statement {
    actions   = ["sqs:ReceiveMessage", "sqs:DeleteMessage", "sqs:GetQueueAttributes"]
    resources = [aws_sqs_queue.requests[each.key].arn]
  }
  statement {
    actions   = ["sqs:SendMessage"]
    resources = [aws_sqs_queue.responses[each.key].arn]
  }
  # IS-09: frames too large for a queue message are read by digest-bound reference.
  statement {
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.results.arn}/frames/*"]
  }
}

resource "aws_iam_role_policy" "signer" {
  for_each = var.signer_principals
  name     = "signer-queues"
  role     = aws_iam_role.signer[each.key].id
  policy   = data.aws_iam_policy_document.signer[each.key].json
}

# ------------------------------------------------------------------------------------------------ Lambda
resource "aws_cloudwatch_log_group" "api" {
  name              = "/aws/lambda/${var.name}-api"
  retention_in_days = 30
}

resource "aws_cloudwatch_log_group" "poller" {
  name              = "/aws/lambda/${var.name}-poller"
  retention_in_days = 30
}

resource "aws_lambda_function" "api" {
  function_name    = "${var.name}-api"
  role             = aws_iam_role.api.arn
  runtime          = var.lambda_runtime
  handler          = "tessera_issue.lambda_app.api_handler"
  filename         = var.lambda_zip
  source_code_hash = filebase64sha256(var.lambda_zip)
  timeout          = 29
  memory_size      = 512
  environment {
    variables = local.lambda_env
  }
  depends_on = [aws_cloudwatch_log_group.api]
}

resource "aws_lambda_function" "poller" {
  function_name                  = "${var.name}-poller"
  role                           = aws_iam_role.poller.arn
  runtime                        = var.lambda_runtime
  handler                        = "tessera_issue.lambda_app.poller_handler"
  filename                       = var.lambda_zip
  source_code_hash               = filebase64sha256(var.lambda_zip)
  timeout                        = 300
  memory_size                    = 1024
  reserved_concurrent_executions = 1 # one poller at a time; records are also compare-and-set
  environment {
    variables = local.lambda_env
  }
  depends_on = [aws_cloudwatch_log_group.poller]
}

resource "aws_cloudwatch_event_rule" "poll" {
  name                = "${var.name}-poll"
  schedule_expression = "rate(10 minutes)"
}

resource "aws_cloudwatch_event_target" "poll" {
  rule = aws_cloudwatch_event_rule.poll.name
  arn  = aws_lambda_function.poller.arn
}

resource "aws_lambda_permission" "poll" {
  statement_id  = "AllowSchedule"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.poller.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.poll.arn
}

# ------------------------------------------------------------------------------------------------ API Gateway
resource "aws_api_gateway_rest_api" "issuer" {
  name               = var.name
  binary_media_types = ["*/*"] # request bodies arrive base64-encoded, byte-exact
  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_api_gateway_resource" "v1" {
  rest_api_id = aws_api_gateway_rest_api.issuer.id
  parent_id   = aws_api_gateway_rest_api.issuer.root_resource_id
  path_part   = "v1"
}

resource "aws_api_gateway_resource" "requests" {
  rest_api_id = aws_api_gateway_rest_api.issuer.id
  parent_id   = aws_api_gateway_resource.v1.id
  path_part   = "requests"
}

resource "aws_api_gateway_resource" "request" {
  rest_api_id = aws_api_gateway_rest_api.issuer.id
  parent_id   = aws_api_gateway_resource.requests.id
  path_part   = "{key}"
}

resource "aws_api_gateway_resource" "receipt" {
  rest_api_id = aws_api_gateway_rest_api.issuer.id
  parent_id   = aws_api_gateway_resource.request.id
  path_part   = "receipt"
}

locals {
  routes = {
    submit  = { resource = aws_api_gateway_resource.requests.id, method = "POST" }
    status  = { resource = aws_api_gateway_resource.request.id, method = "GET" }
    receipt = { resource = aws_api_gateway_resource.receipt.id, method = "GET" }
  }
}

resource "aws_api_gateway_method" "route" {
  for_each         = local.routes
  rest_api_id      = aws_api_gateway_rest_api.issuer.id
  resource_id      = each.value.resource
  http_method      = each.value.method
  authorization    = "NONE"
  api_key_required = true # API keys are the client credentials
}

resource "aws_api_gateway_integration" "route" {
  for_each                = local.routes
  rest_api_id             = aws_api_gateway_rest_api.issuer.id
  resource_id             = each.value.resource
  http_method             = aws_api_gateway_method.route[each.key].http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.api.invoke_arn
}

resource "aws_lambda_permission" "api" {
  statement_id  = "AllowApiGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.issuer.execution_arn}/*/*"
}

resource "aws_api_gateway_deployment" "issuer" {
  rest_api_id = aws_api_gateway_rest_api.issuer.id
  triggers = {
    redeploy = sha1(jsonencode([aws_api_gateway_method.route, aws_api_gateway_integration.route]))
  }
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "v1" {
  rest_api_id   = aws_api_gateway_rest_api.issuer.id
  deployment_id = aws_api_gateway_deployment.issuer.id
  stage_name    = "v1"
}

resource "aws_api_gateway_usage_plan" "clients" {
  name = "${var.name}-clients"
  api_stages {
    api_id = aws_api_gateway_rest_api.issuer.id
    stage  = aws_api_gateway_stage.v1.stage_name
  }
  throttle_settings {
    burst_limit = 20
    rate_limit  = 5
  }
}

resource "aws_api_gateway_api_key" "client" {
  for_each = toset(var.client_names)
  name     = "${var.name}-${each.key}"
}

resource "aws_api_gateway_usage_plan_key" "client" {
  for_each      = aws_api_gateway_api_key.client
  key_id        = each.value.id
  key_type      = "API_KEY"
  usage_plan_id = aws_api_gateway_usage_plan.clients.id
}
