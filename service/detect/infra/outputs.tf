output "alarm_topic" {
  value = aws_sns_topic.alarms.arn
}

output "watcher_function" {
  value = aws_lambda_function.watcher.function_name
}

output "trace_bucket" {
  value = aws_s3_bucket.trace.bucket
}

output "watcher_state_bucket" {
  value = aws_s3_bucket.watcher_state.bucket
}

output "trace_retain_until" {
  value = local.trace_retain_until
}
