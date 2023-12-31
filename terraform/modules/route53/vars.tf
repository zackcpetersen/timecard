variable "route53_name" {
  type = string
}

variable "backend_domain_name" {
  type = string
}

variable "ecs_lb_name" {
  type = string
}

variable "frontend_domain_name" {
  type = string
}

variable "frontend_cloudfront_domain" {
  type = string
}

variable "frontend_acm_domain_validation_options" {
  type = set(object({
    domain_name           = string
    resource_record_name  = string
    resource_record_type  = string
    resource_record_value = string
  }))
}

variable "backend_acm_domain_validation_options" {
  type = set(object({
    domain_name           = string
    resource_record_name  = string
    resource_record_type  = string
    resource_record_value = string
  }))
}

variable "frontend_certificate_arn" {
  type = string
}

variable "backend_certificate_arn" {
  type = string
}

variable "aws_region" {
  type = string
}

variable "ROOT_AWS_ACCESS_KEY_ID" {
  type = string
}

variable "ROOT_AWS_SECRET_ACCESS_KEY" {
  type      = string
  sensitive = true
}
