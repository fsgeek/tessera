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
  default     = ["tessera-v1-issuer-api", "tessera-v1-issuer-poller", "tessera-v1-signer-kms"]
}

variable "monthly_budget_usd" {
  description = "D10 budget. Spend has been ~0 under credits; the point is a runaway, as on GCP in early November."
  default     = "10"
}
