locals {
  tags = merge(var.tags, { Name : "ECS" })
}

# Create SSM Parameters
resource "aws_ssm_parameter" "django_secret_key" {
  name        = "/${var.name}/${var.env}/SECRET_KEY"
  description = "Django secret key"
  type        = "SecureString"
  value       = var.django_secret_key

  tags = local.tags
}
resource "aws_ssm_parameter" "aws_secret_access_key" {
  name        = "/${var.name}/${var.env}/AWS_SECRET_ACCESS_KEY"
  description = "Password for AWS login"
  type        = "SecureString"
  value       = var.ecs_django_static_s3_access_creds["secret_access_key"]

  tags = local.tags
}
resource "aws_ssm_parameter" "gmail_client_secret" {
  name        = "/${var.name}/${var.env}/GMAIL_CLIENT_SECRET"
  description = "Gmail client secret"
  type        = "SecureString"
  value       = var.gmail_client_secret
}
