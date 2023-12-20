# output to be used as variable in ECS module
output "ecs_execution_role" {
  description = "Task execution role for Timecard ECS tasks"
  value       = aws_iam_role.ecs_execution_role.arn
}
output "ecs_task_role" {
  description = "Task role for Timecard S3 access"
  value       = aws_iam_role.ecs_s3_access_role.arn
}
