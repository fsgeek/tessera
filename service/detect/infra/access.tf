# Detection D1-D4 (docs/V1-DETECTION-CONTRACT.md): metric filters and alarms on the issuer API's access log
# (/aws/apigateway/tessera-v1-issuer-access, JSON lines; service/issuer/infra/main.tf access_log_settings).
# Values written by API Gateway as strings; an empty value is "-".

variable "access_log_group" {
  default = "/aws/apigateway/tessera-v1-issuer-access"
}

variable "invitations" {
  description = "The invitation record (D4): invited API key id -> expected requests per day. A request from any other key that succeeds, or a day above the expected volume, alarms."
  type        = map(object({ name = string, daily = number }))
  default = {
    g8plxeex43 = { name = "smoke-test", daily = 50 }     # busiest real day: 37 (first receipt, 2026-11-16)
    l5hkmlu1yd = { name = "yanantin-pilot", daily = 10 } # busiest real day: 5 (setup); normal night: 3
  }
}

locals {
  ns          = "Tessera/Access"
  not_invited = join(" && ", [for k in keys(var.invitations) : "($.apiKeyId != \"${k}\")"])
  # name => [filter pattern, threshold, period seconds, description]
  access_alarms = {
    d1-throttled = ["{ $.error = \"THROTTLED\" }", 50, 300, "D1: 50+ throttled requests in 5 min (flood)"]
    d2-bad-keys  = ["{ ($.error = \"INVALID_API_KEY\") || ($.error = \"MISSING_AUTHENTICATION_TOKEN\") }", 50, 300, "D2: 50+ missing or invalid API keys, or unknown routes, in 5 min (key guessing or probing)"]
    d4-quota     = ["{ $.error = \"QUOTA_EXCEEDED\" }", 0, 300, "D4: an observed quota rejection (the usage-plan quota is best-effort)"]
    d4-unknown-key-success = [
      length(var.invitations) == 0 ? "{ $.status = \"2*\" }" : "{ ($.status = \"2*\") && ${local.not_invited} }",
      0, 300, "D4: a request from a key not in the invitation record succeeded"
    ]
    d3-unknown-key-bad = [
      length(var.invitations) == 0 ? "{ ($.status = \"400\") || ($.status = \"413\") }" : "{ (($.status = \"400\") || ($.status = \"413\")) && ($.apiKeyId != \"-\") && ${local.not_invited} }",
      0, 300, "D3: a malformed or oversized request from a key not in the invitation record"
    ]
  }
}

resource "aws_cloudwatch_log_metric_filter" "access" {
  for_each       = local.access_alarms
  name           = "${var.name}-${each.key}"
  log_group_name = var.access_log_group
  pattern        = each.value[0]
  metric_transformation {
    name          = each.key
    namespace     = local.ns
    value         = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_metric_alarm" "access" {
  for_each            = local.access_alarms
  alarm_name          = "${var.name}-${each.key}"
  alarm_description   = each.value[3]
  namespace           = local.ns
  metric_name         = each.key
  statistic           = "Sum"
  period              = each.value[2]
  evaluation_periods  = 1
  threshold           = each.value[1]
  comparison_operator = each.value[1] == 0 ? "GreaterThanThreshold" : "GreaterThanOrEqualToThreshold"
  treat_missing_data  = "notBreaching"
  alarm_actions       = [aws_sns_topic.alarms.arn]
}

# D3 and D4 per invited key: malformed or oversized requests (400, 413) and daily volume.
resource "aws_cloudwatch_log_metric_filter" "per_key_bad" {
  for_each       = var.invitations
  name           = "${var.name}-d3-${each.value.name}"
  log_group_name = var.access_log_group
  pattern        = "{ ($.apiKeyId = \"${each.key}\") && (($.status = \"400\") || ($.status = \"413\")) }"
  metric_transformation {
    name          = "d3-${each.value.name}"
    namespace     = local.ns
    value         = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_metric_alarm" "per_key_bad" {
  for_each            = var.invitations
  alarm_name          = "${var.name}-d3-${each.value.name}"
  alarm_description   = "D3: 5+ malformed or oversized requests in 1 h from ${each.value.name}"
  namespace           = local.ns
  metric_name         = "d3-${each.value.name}"
  statistic           = "Sum"
  period              = 3600
  evaluation_periods  = 1
  threshold           = 5
  comparison_operator = "GreaterThanOrEqualToThreshold"
  treat_missing_data  = "notBreaching"
  alarm_actions       = [aws_sns_topic.alarms.arn]
}

resource "aws_cloudwatch_log_metric_filter" "per_key_volume" {
  for_each       = var.invitations
  name           = "${var.name}-d4-volume-${each.value.name}"
  log_group_name = var.access_log_group
  pattern        = "{ $.apiKeyId = \"${each.key}\" }"
  metric_transformation {
    name          = "d4-volume-${each.value.name}"
    namespace     = local.ns
    value         = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_metric_alarm" "per_key_volume" {
  for_each            = var.invitations
  alarm_name          = "${var.name}-d4-volume-${each.value.name}"
  alarm_description   = "D4: ${each.value.name} above its invited ${each.value.daily} requests per day"
  namespace           = local.ns
  metric_name         = "d4-volume-${each.value.name}"
  statistic           = "Sum"
  period              = 86400
  evaluation_periods  = 1
  threshold           = each.value.daily
  comparison_operator = "GreaterThanThreshold"
  treat_missing_data  = "notBreaching"
  alarm_actions       = [aws_sns_topic.alarms.arn]
}

# Backstop for D1/D3: API Gateway may omit access-log lines for excessive 429s and for its own 413/431 rejections, so
# the API's own metrics (emitted per API without detailed metrics) catch a flood the log filters undercount.
resource "aws_cloudwatch_metric_alarm" "api_backstop" {
  for_each = {
    count = ["Count", 300, "D1 backstop: 300+ requests to the issuer API in 5 min (normal: a few a day)"]
    "4xx" = ["4XXError", 50, "D1/D2/D3 backstop: 50+ 4XX responses from the issuer API in 5 min"]
  }
  alarm_name          = "${var.name}-api-${each.key}"
  alarm_description   = each.value[2]
  namespace           = "AWS/ApiGateway"
  metric_name         = each.value[0]
  dimensions          = { ApiName = "${var.name}-issuer" }
  statistic           = "Sum"
  period              = 300
  evaluation_periods  = 1
  threshold           = each.value[1]
  comparison_operator = "GreaterThanOrEqualToThreshold"
  treat_missing_data  = "notBreaching"
  alarm_actions       = [aws_sns_topic.alarms.arn]
}
