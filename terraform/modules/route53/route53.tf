data "aws_route53_zone" "primary" {
  provider     = aws.root
  name         = var.route53_name
  private_zone = false
}

# ---- FRONTEND ---- #
resource "aws_route53_record" "frontend" {
  provider = aws.root
  for_each = {
    for dvo in var.frontend_acm_domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  name    = each.value.name
  type    = each.value.type
  records = [each.value.record]
  ttl     = 60
  zone_id = data.aws_route53_zone.primary.zone_id
}

resource "aws_acm_certificate_validation" "frontend" {
  provider                = aws.frontend
  certificate_arn         = var.frontend_certificate_arn
  validation_record_fqdns = [for record in aws_route53_record.frontend : record.fqdn]
}

# ---- BACKEND ---- #
resource "aws_route53_record" "backend" {
  provider = aws.root
  for_each = {
    for dvo in var.backend_acm_domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  name    = each.value.name
  type    = each.value.type
  records = [each.value.record]
  ttl     = 60
  zone_id = data.aws_route53_zone.primary.zone_id
}

resource "aws_acm_certificate_validation" "backend" {
  provider                = aws.backend
  certificate_arn         = var.backend_certificate_arn
  validation_record_fqdns = [for record in aws_route53_record.backend : record.fqdn]
}

## record to point main domain to backend lb
resource "aws_route53_record" "alb_record" {
  count    = var.env == "staging" || var.env == "development" ? 1 : 0
  provider = aws.root
  zone_id  = data.aws_route53_zone.primary.zone_id
  name     = var.backend_domain_name
  type     = "CNAME"
  ttl      = "60"
  records  = [var.ecs_lb_name]
}

## record to point main domain to frontend
resource "aws_route53_record" "frontend_record" {
  count    = var.env == "staging" || var.env == "development" ? 1 : 0
  provider = aws.root
  zone_id  = data.aws_route53_zone.primary.zone_id
  name     = var.frontend_domain_name
  type     = "CNAME"
  ttl      = "60"
  records  = [var.frontend_cloudfront_domain]
}

