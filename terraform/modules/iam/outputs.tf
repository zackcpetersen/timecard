output "ecs_django_static_s3_access_creds" {
  value = {
    access_key        = aws_iam_access_key.ecs_s3_access_key.id
    secret_access_key = aws_iam_access_key.ecs_s3_access_key.secret
  }
  sensitive = true
}
# output to be used as variable in ECS module
output "ecs_task_execution_role" {
  description = "Task execution role for Timecard ECS tasks"
  value       = aws_iam_role.ECSTaskExecutionRole.arn
}
# Output all Terraform managed IAM users
output "iam_users" {
  value = aws_iam_user.admin_users[*].name
}
