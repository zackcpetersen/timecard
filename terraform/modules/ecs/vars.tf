# All variable descriptions live in base staging/production vars.tf file

variable "env" {
  type = string
}

variable "aws_region" {
  type = string
}

variable "name" {
  type = string
}

variable "github_repo" {
  type = string
}

variable "debug" {
  type = string
}

variable "ecs_task_execution_role" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "public_subnets" {
  type = list(string)
}

variable "private_subnets" {
  type = list(string)
}

variable "ecs_django_static_s3_access_creds" {
  type = map(string)
}

variable "s3_static_bucket_name" {
  type = string
}

variable "db_name" {
  type = string
}

variable "db_user" {
  type = string
}

variable "db_host" {
  type = string
}

variable "db_port" {
  type = number
}

variable "redis_primary_endpoint" {
  type = string
}

variable "redis_port" {
  type = number
}

#variable "opensearch_endpoint" {
#  type = string
#}

variable "tags" {
  type = map(string)
}

variable "django_secret_key" {
  type = string
}

variable "email_host_password" {
  type = string
}

variable "email_host" {
  type = string
}

variable "email_port" {
  type = number
}

variable "email_host_user" {
  type = string
}

variable "email_use_tls" {
  type = string
}

variable "default_from_email" {
  type = string
}

variable "ssl_redirect" {
  type = string
}

variable "cors_allowed_regexes" {
  type = string
}

variable "allowed_hosts" {
  type = string
}

variable "use_elastic" {
  type = string
}
