output "frontend_certificate_arn" {
  value = aws_acm_certificate.frontend.arn
}

output "frontend_domain_validation_options" {
  value = aws_acm_certificate.frontend.domain_validation_options
}

output "backend_certificate_arn" {
  value = aws_acm_certificate.backend.arn
}

output "backend_domain_validation_options" {
  value = aws_acm_certificate.backend.domain_validation_options
}
