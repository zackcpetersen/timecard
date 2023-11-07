# All variable descriptions live in base staging/production vars.tf file

variable "env" {
  type = string
}

variable "aws_region" {
  type = string
}

variable "tags" {
  type = map(string)
}

variable "name" {
  type = string
}

variable "db_port" {
  type = number
}
