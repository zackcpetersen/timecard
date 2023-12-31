# Frontend lives in us-east-1 (required by cloudfront)
resource "aws_acm_certificate" "frontend" {
  provider = aws.east-1
  # TODO add a prod cert
  domain_name       = var.frontend_domain_name
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

# Backend lives in default region (us-west-2)
resource "aws_acm_certificate" "backend" {
  # TODO add a prod cert or variable for environment
  domain_name       = var.backend_domain_name
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}
