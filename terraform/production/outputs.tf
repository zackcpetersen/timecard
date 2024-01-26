output "backend_lb" {
  value = module.ecs.api_testing_lb_url
}

output "cf_distribution_domain_name" {
  value = module.cloudfront.cf_domain
}
