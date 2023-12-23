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

# Gmail Client Secret
resource "aws_secretsmanager_secret" "gmail_client_secret" {
  name_prefix             = "gmail_client_secret"
  recovery_window_in_days = var.deletion_protection ? 7 : 0
}
resource "aws_secretsmanager_secret_version" "gmail_client_secret" {
  secret_id     = aws_secretsmanager_secret.gmail_client_secret.id
  secret_string = var.gmail_client_secret
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
