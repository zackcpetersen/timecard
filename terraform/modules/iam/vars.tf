# All variable descriptions live in base staging/production vars.tf file

variable "name" {
  type = string
}

variable "users" {
  type = list(string)
}

variable "tags" {
  type = map(string)
}

variable "django_ecs_static_bucket_arn" {
  type = string
}
