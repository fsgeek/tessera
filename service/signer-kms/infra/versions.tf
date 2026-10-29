# Tessera V1 KMS-slot policy signer (docs/decisions/2026-10-27-v1-signer-placement.md). A separate root module from
# service/issuer/infra, in the same (issuing) AWS account, applied after it. Applied by a later step; never by the
# builder.
terraform {
  required_version = ">= 1.6"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.70"
    }
  }
}

provider "aws" {
  region = var.region
}
