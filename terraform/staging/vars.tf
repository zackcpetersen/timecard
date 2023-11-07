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

variable "debug" {
  type        = string
  description = "Turn on/off debug for apps"
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

variable "db_port" {
  type        = number
  description = "Port for database"
  default     = 5432
}

variable "global_tags" {
  type        = map(string)
  description = "Map of tags to apply to all resources"
  default = {
    Environment = "staging"
    Terraform   = "true"
  }
}

variable "email_host" {
  type        = string
  description = "Host for sending emails"
  default     = "smtp.gmail.com"
}

variable "email_port" {
  type        = number
  description = "Port for sending emails"
  default     = 587
}

variable "email_host_user" {
  type        = string
  description = "Email username to authenticate as"
  default     = "info@castlerockis.com"
}

variable "email_use_tls" {
  type        = string
  description = "Bool in string whether to use email TLS"
  default     = "True"
}

variable "default_from_email" {
  type        = string
  description = "Default `FROM:` email"
  default     = "info@castlerockis.com"
}

variable "django_secret_key" {
  type        = string
  description = "Django secret key used in settings file - SENSITIVE, defined in Cloud workspace as a variable"
}

variable "email_host_password" {
  type        = string
  description = "Password to login to email host - SENSITIVE, defined in Cloud workspace as variable"
}

variable "aws_access_key_id" {
  type        = string
  description = "AWS account access id to login via IAM"
}

variable "aws_secret_access_key" {
  type        = string
  description = "AWS login password"
}

variable "ssl_redirect" {
  type    = string
  default = "False"
}

variable "cors_allowed_origins_regexes" {
  type        = string
  description = "Add additional cors origins here - check settings.base.py CORS_ALLOWED_ORIGIN_REGEXES to see formatting"
  default     = ""
}

variable "allowed_hosts" {
  type        = string
  description = "Add additional cors origins here - check settings.base.py ALLOWED_HOSTS to see formatting"
  default     = ""
}

variable "db_name" {
  type        = string
  description = "Defined in Cloud workspace"
}

variable "db_user" {
  type        = string
  description = "Defined in Cloud workspace"
}
