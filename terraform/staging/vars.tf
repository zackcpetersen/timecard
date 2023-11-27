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

variable "github_repo" {
  type        = string
  description = "Name of GitHub repository, used for ECS container definition ENV variables"
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
  default     = 10
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
  description = "Defined in Cloud workspace"
}

variable "db_port" {
  type    = number
  default = 5432
}

variable "DEBUG" {
  type        = bool
  description = "Turn on/off debug for apps"
  default     = false
}

variable "SECRET_KEY" {
  type        = string
  description = "Django secret key used in settings file - SENSITIVE, defined in Cloud workspace as a variable"
}

variable "CORS_ALLOW_ALL_ORIGINS" {
  type    = bool
  default = false
}

variable "CORS_ALLOWED_ORIGIN_REGEXES" {
  type        = string
  description = "Defined in Cloud workspace"
  default     = ""
}

variable "ALLOWED_HOSTS" {
  type        = string
  description = "Defined in Cloud workspace"
  default     = ""
}

variable "SECURE_SSL_REDIRECT" {
  type    = bool
  default = false
}

variable "DEFAULT_DOMAIN" {
  type        = string
  description = "Defined in Cloud workspace"
}

variable "FRONTEND_URL" {
  type        = string
  description = "Defined in Cloud workspace"
}

variable "AWS_ACCESS_KEY_ID" {
  type        = string
  description = "AWS account access id to login via IAM"
}

variable "AWS_SECRET_ACCESS_KEY" {
  type        = string
  description = "AWS login password"
}

variable "USE_S3" {
  type        = bool
  description = "Use S3 for static files"
}

variable "STATICFILES_STORAGE" {
  type        = string
  description = "Defined in Cloud workspace"
}

variable "DEFAULT_FILE_STORAGE" {
  type        = string
  description = "Defined in Cloud workspace"
}

variable "GMAIL_CLIENT_ID" {
  type        = string
  description = "Defined in Cloud workspace"
}

variable "GMAIL_PROJECT_ID" {
  type        = string
  description = "Defined in Cloud workspace"
}

variable "GMAIL_CLIENT_SECRET" {
  type        = string
  description = "Defined in Cloud workspace"
}
