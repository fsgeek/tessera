output "api_url" {
  value = aws_api_gateway_stage.v1.invoke_url
}

output "result_bucket" {
  value = aws_s3_bucket.results.bucket
}

output "request_table" {
  value = aws_dynamodb_table.requests.name
}

output "signer_queues" {
  value = { for s in local.slots : s => { requests = aws_sqs_queue.requests[s].url, responses = aws_sqs_queue.responses[s].url, wake = aws_sns_topic.wake[s].arn } }
}

output "client_api_key_ids" {
  value = { for k, v in aws_api_gateway_api_key.client : k => v.id }
}
