### --- Variables in BOLD are required in the Django app, others are required for terraform --- ###

variable "env" {
  type        = string
  description = "Environment currently working in"
  default     = "staging"
}

variable "aws_region" {
  type        = string
  description = "Default AWS_REGION"
  default     = "us-west-2"
}

variable "users" {
  type        = list(string)
  description = "Names of IAM users to create"
  default     = ["zack"]
}

variable "product_name" {
  type        = string
  description = "Name of product that resources are being created for"
  default     = "timecard"
}

variable "db_instance_class" {
  type        = string
  description = "Determines size of database to be created - https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html"
  default     = "db.t3.micro"
}

variable "db_allocated_storage" {
  type        = number
  description = "Number in GB for database initial size"
  default     = 20
}

variable "db_max_storage" {
  type        = number
  description = "Max size for database in GB"
  default     = 100
}

variable "global_tags" {
  type        = map(string)
  description = "Map of tags to apply to all resources"
  default = {
    Environment = "staging"
    Terraform   = "true"
  }
}

variable "db_snapshot_name" {
  type        = string
  default     = ""
  description = "Defined in Cloud workspace"
}

variable "db_port" {
  type    = number
  default = 5432
}

variable "DEBUG" {
  type        = string
  description = "Turn on/off debug for apps"
  default     = "False"
}

variable "SECRET_KEY" {
  type        = string
  description = "Django secret key used in settings file - SENSITIVE, defined in Cloud workspace as a variable"
  sensitive   = true
}

variable "CORS_ALLOW_ALL_ORIGINS" {
  type    = string
  default = "False"
}

variable "CORS_ALLOWED_ORIGIN_REGEXES" {
  type        = string
  description = "Defined in Cloud workspace"
}

variable "SECURE_SSL_REDIRECT" {
  type    = string
  default = "True"
}

variable "DEFAULT_ADMIN_EMAIL" {
  type        = string
  description = "Email to send admin stuff to"
}

variable "AWS_ACCESS_KEY_ID" {
  type        = string
  description = "AWS account access id to login via IAM"
}

variable "AWS_SECRET_ACCESS_KEY" {
  type        = string
  description = "AWS login password"
  sensitive   = true
}

variable "ROOT_AWS_ACCESS_KEY_ID" {
  type        = string
  description = "AWS account access id for root account"
}

variable "ROOT_AWS_SECRET_ACCESS_KEY" {
  type        = string
  description = "AWS login password for root account"
  sensitive   = true
}

variable "USE_S3" {
  type        = string
  description = "Use S3 for static files"
  default     = true
}

variable "ghcr_base_url" {
  type = string
}

variable "web_version" {
  type    = string
  default = "latest"
}

variable "nginx_version" {
  type    = string
  default = "latest"
}

variable "github_token" {
  description = "Token for GitHub Container Registry"
  type        = string
  sensitive   = true
}

variable "route53_domain_name" {
  type = string
}

