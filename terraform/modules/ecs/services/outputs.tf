output "api_testing_lb_url" {
  value = aws_lb.ecs_api_lb.dns_name
}
