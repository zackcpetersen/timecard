data "aws_caller_identity" "target" {}

data "aws_s3_bucket" "source_bucket" {
  provider = aws.source_account
  bucket   = var.source_bucket_name
}

data "aws_s3_bucket" "destination_bucket" {
  provider = aws.destination_account
  bucket   = var.destination_bucket_name
}

data "aws_iam_user" "source_user" {
  provider  = aws.source_account
  user_name = "terraform"
}

data "aws_iam_user" "destination_user" {
  provider  = aws.destination_account
  user_name = "terraform"
}
