output "signer_role_arn" {
  value = aws_iam_role.signer.arn
}

output "signer_function" {
  value = aws_lambda_function.signer.function_name
}

output "kms_key_arn" {
  value = data.aws_kms_key.signer.arn
}

output "trail_bucket" {
  value = aws_s3_bucket.trail.bucket
}

output "trail_arn" {
  value = aws_cloudtrail.signer.arn
}
