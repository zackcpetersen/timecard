locals {
  tags = merge(var.tags, { Name : "ECS" })
}

# Create SSM Parameters
# Django Secret Key
resource "aws_secretsmanager_secret" "django_secret_key" {
  name_prefix             = "django_secret_key"
  recovery_window_in_days = var.deletion_protection ? 7 : 0
}
resource "aws_secretsmanager_secret_version" "django_secret_key" {
  secret_id     = aws_secretsmanager_secret.django_secret_key.id
  secret_string = var.django_secret_key
}

# Root AWS Secret Access Key
resource "aws_secretsmanager_secret" "root_aws_secret_access_key" {
  name_prefix             = "root_aws_secret_access_key"
  recovery_window_in_days = var.deletion_protection ? 7 : 0
}
resource "aws_secretsmanager_secret_version" "root_aws_secret_access_key" {
  secret_id     = aws_secretsmanager_secret.root_aws_secret_access_key.id
  secret_string = var.root_aws_secret_access_key
}

# DB Password
resource "aws_secretsmanager_secret" "db_password" {
  name_prefix             = "db_password"
  recovery_window_in_days = var.deletion_protection ? 7 : 0
}
resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id     = aws_secretsmanager_secret.db_password.id
  secret_string = var.db_password
}

# Github Token
resource "aws_secretsmanager_secret" "github_token" {
  name_prefix             = "github_token"
  recovery_window_in_days = var.deletion_protection ? 7 : 0
}
resource "aws_secretsmanager_secret_version" "github_token" {
  secret_id = aws_secretsmanager_secret.github_token.id
  secret_string = jsonencode({
    username = var.github_username,
    password = var.github_token
  })
}
