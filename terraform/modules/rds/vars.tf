# All variable descriptions live in base staging/production vars.tf file

variable "vpc_id" {
  type = string
}

variable "private_subnets" {
  type = list(string)
}

variable "env" {
  type = string
}

variable "tags" {
  type = map(string)
}

variable "name" {
  type = string
}

variable "db_instance_class" {
  type = string
}

variable "db_allocated_storage" {
  type = number
}

variable "db_max_storage" {
  type = number
}

variable "db_port" {
  type = number
}

variable "rds_sg_id" {
  type = string
}

variable "db_snapshot_name" {
  type = string
}
