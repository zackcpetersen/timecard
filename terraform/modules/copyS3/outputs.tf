output "destination_migration_role" {
  value = aws_iam_role.destination_migration.arn
}

output "destination_bucket_name" {
  value = data.aws_s3_bucket.destination_bucket.id
}

output "source_bucket_name" {
  value = data.aws_s3_bucket.source_bucket.id
}
