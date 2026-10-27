variable "region" {
  type    = string
  default = "us-east-2"
}

variable "name" {
  description = "Resource name prefix."
  type        = string
  default     = "tessera-v1-issuer"
}

variable "lambda_zip" {
  description = "Path of the built Lambda package (tessera_issue, tessera_verify, the frozen objects, the SHA-1DC binary and its install.json). Built by a later step."
  type        = string
}

variable "lambda_runtime" {
  type    = string
  default = "python3.14"
}

variable "client_names" {
  description = "One API key (client credential) is created per name."
  type        = list(string)
  default     = []
}

variable "ots_calendars" {
  type    = list(string)
  default = ["https://alice.btc.calendar.opentimestamps.org", "https://bob.btc.calendar.opentimestamps.org", "https://finney.calendar.eternitywall.com"]
}

variable "explorers" {
  description = "Esplora-style explorers; every one must agree on every header."
  type        = list(string)
  default     = ["https://blockstream.info/api", "https://mempool.space/api"]
}

variable "dns_resolver" {
  type    = string
  default = "1.1.1.1"
}

variable "closing" {
  description = "Operator switch: refuse new requests with CLOSING."
  type        = bool
  default     = false
}

variable "signing_available" {
  description = "Operator switch: false refuses new requests with SIGNING_UNAVAILABLE."
  type        = bool
  default     = true
}

variable "signer_principals" {
  description = "Per slot (kms, gpg): the AWS principal ARN the remote signer runs as. Empty: no signer role is created for that slot."
  type        = map(string)
  default     = {}
}
