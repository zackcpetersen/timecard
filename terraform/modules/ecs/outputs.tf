output "web_ecr_endpoint" {
  value = aws_ecr_repository.web.repository_url
}

output "nginx_ecr_endpoint" {
  value = aws_ecr_repository.nginx.repository_url
}

output "api_testing_lb_url" {
  value = module.services.api_testing_lb_url
}