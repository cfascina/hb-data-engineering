terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 0.14.9"
}

provider "aws" {
  profile = "andre_aws"
  region  = "us-east-1"
}

resource "aws_s3_bucket" "bucket-producao-belisco" {
    bucket = "bucket-do-belisco-producao"
    tags = {
      "Area" = "Produtos"
      "Enviroment" = "Production"
    }
}