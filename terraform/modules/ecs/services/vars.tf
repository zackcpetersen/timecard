# All variable descriptions live in base staging/production vars.tf file

variable "cluster_id" {
  type = string
}

variable "cluster_name" {
  type = string
}

variable "env" {
  type = string
}

variable "debug" {
  type = string
}

variable "tags" {
  type = map(string)
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

variable "ecs_execution_role" {
  type = string
}

variable "ecs_task_role" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "public_subnets" {
  type = list(string)
}

variable "latest_tag" {
  type = string
}

variable "django_secret_key" {
  type      = string
  sensitive = true
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

variable "db_password" {
  type      = string
  sensitive = true
}

variable "s3_static_bucket_name" {
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

variable "cors_allow_all_origins" {
  type = string
}

variable "frontend_url" {
  type = string
}

variable "default_domain" {
  type = string
}

variable "gmail_project_id" {
  type = string
}

variable "gmail_client_id" {
  type = string
}

variable "gmail_client_secret" {
  type      = string
  sensitive = true
}

variable "ghcr_base_url" {
  type = string
}

variable "github_username" {
  type = string
}

variable "github_token" {
  description = "Token for GitHub Container Registry"
  type        = string
  sensitive   = true
}

variable "image_tag" {
  type = string
}

variable "deletion_protection" {
  type = bool
}

variable "api_task_cpu" {
  type = number
}

variable "api_task_memory" {
  type = number
}

variable "api_container_cpu" {
  type = number
}

variable "api_container_memory_reservation" {
  type = number
}

variable "backend_certificate_arn" {
  type = string
}

variable "default_admin_email" {
  type = string
}
