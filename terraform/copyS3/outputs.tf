output "destination_migration_role" {
  value = module.copyS3.destination_migration_role
}

output "destination_bucket_name" {
  value = module.copyS3.destination_bucket_name
}

output "source_bucket_name" {
  value = module.copyS3.source_bucket_name
}
