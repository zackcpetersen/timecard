provider "aws" {
  alias      = "root"
  region     = var.aws_region
  access_key = var.ROOT_AWS_ACCESS_KEY_ID
  secret_key = var.ROOT_AWS_SECRET_ACCESS_KEY
}

provider "aws" {
  alias  = "frontend"
  region = "us-east-1"
}

provider "aws" {
  alias  = "backend"
  region = var.aws_region
}
