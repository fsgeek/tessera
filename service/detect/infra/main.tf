# Detection, step 2 (docs/V1-DETECTION-CONTRACT.md): the alarm channel, D7 (control-plane tampering) and D10 (service
# faults, spend). Every alarm publishes to one topic per region with an email subscription to the author.

data "aws_caller_identity" "me" {}

locals {
  account = data.aws_caller_identity.me.account_id

  # D7, us-east-2: CloudTrail management write events (EventBridge receives these without a trail; read-only events
  # are not delivered, which is why kms:Sign is reconciled by the watcher, D6, not here).
  d7_regional = {
    kms        = { source = "aws.kms", names = ["PutKeyPolicy", "CreateGrant", "RetireGrant", "RevokeGrant", "DisableKey", "EnableKey", "ScheduleKeyDeletion", "CancelKeyDeletion", "CreateAlias", "UpdateAlias", "DeleteAlias", "CreateKey"] }
    cloudtrail = { source = "aws.cloudtrail", names = ["StopLogging", "DeleteTrail", "UpdateTrail", "PutEventSelectors", "PutInsightSelectors", "CreateTrail"] }
    s3         = { source = "aws.s3", names = ["PutBucketPolicy", "DeleteBucketPolicy", "PutObjectLockConfiguration", "PutBucketVersioning", "PutBucketLogging", "PutBucketLifecycle", "PutBucketLifecycleConfiguration", "DeleteBucketLifecycle", "PutBucketAcl", "PutBucketPublicAccessBlock", "DeleteBucketPublicAccessBlock", "PutBucketOwnershipControls", "DeleteBucket"] }
    apigateway = { source = "aws.apigateway", names = ["CreateApiKey", "UpdateApiKey", "DeleteApiKey", "CreateUsagePlan", "UpdateUsagePlan", "DeleteUsagePlan", "CreateUsagePlanKey", "DeleteUsagePlanKey", "UpdateStage", "DeleteStage", "CreateDeployment", "UpdateMethod", "UpdateRestApi", "PutRestApi", "UpdateAccount"] }
    sns        = { source = "aws.sns", names = ["Unsubscribe", "Subscribe", "DeleteTopic", "SetTopicAttributes", "SetSubscriptionAttributes", "RemovePermission", "AddPermission"] }
    events     = { source = "aws.events", names = ["DisableRule", "DeleteRule", "PutRule", "RemoveTargets", "PutTargets"] }
    cloudwatch = { source = "aws.monitoring", names = ["DeleteAlarms", "DisableAlarmActions", "PutMetricAlarm", "SetAlarmState"] }
    logs       = { source = "aws.logs", names = ["DeleteLogGroup", "PutRetentionPolicy", "DeleteRetentionPolicy", "DeleteMetricFilter", "PutMetricFilter"] }
    sqs        = { source = "aws.sqs", names = ["SetQueueAttributes", "AddPermission", "RemovePermission", "DeleteQueue", "PurgeQueue"] }
    dynamodb   = { source = "aws.dynamodb", names = ["DeleteTable", "UpdateTable", "UpdateTimeToLive", "UpdateContinuousBackups", "RestoreTableToPointInTime", "PutResourcePolicy"] }
  }
  # Lambda event names carry an API-version suffix (e.g. UpdateFunctionCode20150331v2), so they are prefix-matched.
  d7_lambda_prefixes = ["UpdateFunctionCode", "UpdateFunctionConfiguration", "PublishVersion", "DeleteFunction", "AddPermission", "RemovePermission", "PutRuntimeManagementConfig", "PutFunctionConcurrency", "DeleteFunctionConcurrency", "CreateEventSourceMapping", "UpdateEventSourceMapping", "DeleteEventSourceMapping", "UpdateAlias", "CreateFunctionUrlConfig"]
}

# ---------------------------------------------------------------------------------------------------- the channel

resource "aws_sns_topic" "alarms" {
  name = "${var.name}-alarms"
}


data "aws_iam_policy_document" "topic" {
  for_each = { use2 = aws_sns_topic.alarms.arn }
  statement {
    actions   = ["sns:Publish"]
    resources = [each.value]
    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com", "cloudwatch.amazonaws.com", "budgets.amazonaws.com"]
    }
    condition {
      test     = "StringEquals"
      variable = "aws:SourceAccount"
      values   = [local.account]
    }
  }
}

resource "aws_sns_topic_policy" "alarms" {
  arn    = aws_sns_topic.alarms.arn
  policy = data.aws_iam_policy_document.topic["use2"].json
}


resource "aws_sns_topic_subscription" "author" {
  topic_arn = aws_sns_topic.alarms.arn
  protocol  = "email"
  endpoint  = var.alarm_email
}


# ---------------------------------------------------------------------------------------------- D7: tampering

resource "aws_cloudwatch_event_rule" "d7" {
  for_each    = local.d7_regional
  name        = "${var.name}-d7-${each.key}"
  description = "D7: control-plane change (${each.value.source})"
  event_pattern = jsonencode({
    source        = [each.value.source]
    "detail-type" = ["AWS API Call via CloudTrail"]
    detail        = { eventName = each.value.names }
  })
}

resource "aws_cloudwatch_event_target" "d7" {
  for_each = local.d7_regional
  rule     = aws_cloudwatch_event_rule.d7[each.key].name
  arn      = aws_sns_topic.alarms.arn
}

resource "aws_cloudwatch_event_rule" "d7_lambda" {
  name        = "${var.name}-d7-lambda"
  description = "D7: control-plane change (aws.lambda)"
  event_pattern = jsonencode({
    source        = ["aws.lambda"]
    "detail-type" = ["AWS API Call via CloudTrail"]
    detail        = { eventName = [for p in local.d7_lambda_prefixes : { prefix = p }] }
  })
}

resource "aws_cloudwatch_event_target" "d7_lambda" {
  rule = aws_cloudwatch_event_rule.d7_lambda.name
  arn  = aws_sns_topic.alarms.arn
}

# IAM and STS are global: their events reach EventBridge only in us-east-1, which the organization's SCP closes to this
# account. IAM changes are therefore detected by the watcher from the multi-region trail (D7, latency up to ~1 h).


# ------------------------------------------------------------------------------------------- D10: service faults

resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  for_each            = toset(var.lambda_functions)
  alarm_name          = "${each.value}-errors"
  alarm_description   = "D10: any error in ${each.value}"
  namespace           = "AWS/Lambda"
  metric_name         = "Errors"
  dimensions          = { FunctionName = each.value }
  statistic           = "Sum"
  period              = 300
  evaluation_periods  = 1
  threshold           = 0
  comparison_operator = "GreaterThanThreshold"
  treat_missing_data  = "notBreaching"
  alarm_actions       = [aws_sns_topic.alarms.arn]
  ok_actions          = [aws_sns_topic.alarms.arn]
}

resource "aws_budgets_budget" "monthly" {
  name         = "${var.name}-monthly"
  budget_type  = "COST"
  limit_amount = var.monthly_budget_usd
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  notification {
    comparison_operator       = "GREATER_THAN"
    threshold                 = 50
    threshold_type            = "PERCENTAGE"
    notification_type         = "ACTUAL"
    subscriber_sns_topic_arns = [aws_sns_topic.alarms.arn]
  }
  notification {
    comparison_operator       = "GREATER_THAN"
    threshold                 = 100
    threshold_type            = "PERCENTAGE"
    notification_type         = "FORECASTED"
    subscriber_sns_topic_arns = [aws_sns_topic.alarms.arn]
  }
}
