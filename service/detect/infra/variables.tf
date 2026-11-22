variable "region" {
  default = "us-east-2"
}

variable "name" {
  default = "tessera-v1"
}

variable "alarm_email" {
  description = "Where every alarm goes (the author). Supplied at apply time; not kept in the repository."
  type        = string
}

variable "lambda_functions" {
  description = "Functions whose Errors metric is an alarm (D10)."
  default     = ["tessera-v1-issuer-api", "tessera-v1-issuer-poller", "tessera-v1-signer-kms", "tessera-v1-watcher"]
}

variable "monthly_budget_usd" {
  description = "D10 budget. Spend has been ~0 under credits; the point is a runaway, as on GCP in early November."
  default     = "10"
}

# ------------------------------------------------------------------------------------------ the watcher (watcher.tf)
variable "watcher_zip" {
  description = "The built watcher package (service/watcher/package.py); record its SHA-256 in the deploy run."
  type        = string
}

variable "lambda_runtime" {
  type    = string
  default = "python3.14"
}

variable "runtime_version_arn" {
  description = "The Lambda runtime version the watcher's verifier install record was made on. Empty only for the bootstrap deployment (every D8 check is then refused and reported)."
  type        = string
  default     = ""
}

variable "request_table" {
  description = "The issuer's request table (its request_table output). Read only."
  type        = string
  default     = "tessera-v1-issuer-requests"
}

variable "results_bucket" {
  description = "The issuer's result bucket (its result_bucket output). The watcher may read result/* only."
  type        = string
}

variable "trail_bucket" {
  description = "The CloudTrail trail bucket (service/signer-kms trail_bucket output). Read only."
  type        = string
}

variable "trail_prefix" {
  description = "The trail's S3 key prefix (empty for the v1 trail)."
  type        = string
  default     = ""
}

variable "kms_key_id" {
  description = "The window's kms-slot key, by alias or ARN. The watcher reconciles every kms:Sign on it (D6)."
  type        = string
  default     = "alias/tessera-v1-kms"
}

variable "signer_role_name" {
  description = "The KMS signer's role: the only principal whose kms:Sign is reconciled rather than alarmed."
  type        = string
  default     = "tessera-v1-signer-kms-role"
}

variable "client_api_key_ids" {
  description = "Client name -> API Gateway key id (the issuer's client_api_key_ids output): identifiers, not key values. Lets a trace record name the key id behind a credential digest."
  type        = map(string)
  default     = {}
}

variable "explorers" {
  description = "Block explorers for the relying-party header pins (D8); every one must agree."
  type        = list(string)
  default     = ["https://blockstream.info/api", "https://mempool.space/api"]
}

variable "watcher_log_retention_days" {
  type    = number
  default = 400
}
