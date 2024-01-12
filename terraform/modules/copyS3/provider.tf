provider "aws" {
  alias      = "source_account"
  region     = var.aws_region
  access_key = var.ROOT_AWS_ACCESS_KEY_ID
  secret_key = var.ROOT_AWS_SECRET_ACCESS_KEY
}

provider "aws" {
  alias      = "destination_account"
  region     = var.aws_region
  access_key = var.AWS_ACCESS_KEY_ID
  secret_key = var.AWS_SECRET_ACCESS_KEY
}
