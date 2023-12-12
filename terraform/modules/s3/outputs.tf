output "frontend_static_site_bucket_arn" {
  value = aws_s3_bucket.frontend_static_site.arn
}

output "django_ecs_static_bucket_arn" {
  value = aws_s3_bucket.django_ecs_static.arn
}

output "s3_static_bucket_name" {
  value = split(".", aws_s3_bucket.django_ecs_static.bucket_domain_name)[0]
}
