output "backend_lb" {
  value = module.ecs.api_testing_lb_url
}

output "frontend_bucket_url_regional" {
  value = module.s3.frontend_regional_domain_name
}

output "cf_distribution_domain_name" {
  value = module.cloudfront.cf_domain
}
