variable "region" {
  type    = string
  default = "us-east-2"
}

variable "name" {
  description = "Resource name prefix."
  type        = string
  default     = "tessera-v1-signer-kms"
}

variable "issuer_name" {
  description = "The issuer module's name prefix: its kms queues are <issuer_name>-kms-requests and -kms-responses."
  type        = string
  default     = "tessera-v1-issuer"
}

variable "frames_bucket" {
  description = "The issuer's result bucket (its result_bucket output). The signer may read frames/* only (IS-09)."
  type        = string
}

variable "lambda_zip" {
  description = "Path of the built signer package (tessera_sign_kms, tessera_verify, cryptography for Linux). Built by a later step."
  type        = string
}

variable "lambda_runtime" {
  type    = string
  default = "python3.14"
}

variable "kms_key_id" {
  description = "Id or ARN of the existing ML-DSA-65 KMS key for the kms slot (the window's key). Its key policy is REPLACED by this module."
  type        = string
  validation {
    condition     = var.kms_key_id != ""
    error_message = "kms_key_id is required: this module does not create keys."
  }
}

variable "key_fp" {
  description = "Pinned spki-sha256 fingerprint of the window's kms key. The signer does not start unless the KMS key matches it."
  type        = string
  validation {
    condition     = can(regex("^spki-sha256:[0-9a-f]{64}$", var.key_fp))
    error_message = "key_fp must be spki-sha256:<64 lowercase hex>."
  }
}

variable "sign_until" {
  description = "IS-03: the window's signing stop (issuance-not-after minus 96 h), RFC 3339 UTC second. The signer refuses past it."
  type        = string
  validation {
    condition     = can(regex("^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$", var.sign_until))
    error_message = "sign_until must be YYYY-MM-DDTHH:MM:SSZ."
  }
}

variable "trail_retention_days" {
  description = "Object Lock COMPLIANCE retention of every CloudTrail log object. Cannot be shortened or removed by anyone, the root user included, until it ends. No default: choose it."
  type        = number
  validation {
    condition     = var.trail_retention_days >= 1 && floor(var.trail_retention_days) == var.trail_retention_days
    error_message = "trail_retention_days must be a whole number of days, at least 1."
  }
}

variable "log_retention_days" {
  description = "CloudWatch retention of the signer's structured log lines."
  type        = number
  default     = 400
}
