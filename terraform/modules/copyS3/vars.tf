variable "aws_region" {
  type = string
}

variable "env" {
  type = string
}

variable "AWS_ACCESS_KEY_ID" {
  type = string
}

variable "AWS_SECRET_ACCESS_KEY" {
  type      = string
  sensitive = true
}

variable "ROOT_AWS_ACCESS_KEY_ID" {
  type = string
}

variable "ROOT_AWS_SECRET_ACCESS_KEY" {
  type      = string
  sensitive = true
}

variable "source_account_id" {
  type = string
}

variable "source_bucket_name" {
  type = string
}

variable "destination_bucket_name" {
  type = string
}
