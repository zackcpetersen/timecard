variable "name" {
  type = string
}

variable "env" {
  type = string
}

variable "tags" {
  type = map(string)
}

variable "cloudfront_oai_arn" {
  type = string
}

variable "dev_env" {
  type    = bool
  default = false
}

