resource "aws_cloudfront_cache_policy" "main" {
  name        = "frontend-web"
  default_ttl = 50
  max_ttl     = 100
  min_ttl     = 1

  parameters_in_cache_key_and_forwarded_to_origin {
    cookies_config {
      cookie_behavior = "none"
    }
    headers_config {
      header_behavior = "none"
    }
    query_strings_config {
      query_string_behavior = "none"
    }
  }
}

resource "aws_cloudfront_distribution" "s3_distribution" {
  origin {
    domain_name = var.website_bucket_domain_name
    origin_id   = var.website_bucket_origin_id

    s3_origin_config {
      origin_access_identity = "origin-access-identity/cloudfront/${aws_cloudfront_origin_access_identity.oai.id}"
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"

  aliases = [var.frontend_domain_name]

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = var.website_bucket_origin_id
    cache_policy_id  = aws_cloudfront_cache_policy.main.id

    viewer_protocol_policy = "redirect-to-https"
  }

  viewer_certificate {
    acm_certificate_arn      = var.frontend_certificate_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }

  restrictions {
    geo_restriction {
      restriction_type = "whitelist"
      locations        = ["US", "CA"]
    }
  }

  # Custom Error Responses
  custom_error_response {
    error_code            = 404
    response_page_path    = "/index.html"
    response_code         = 200
    error_caching_min_ttl = 300
  }

  custom_error_response {
    error_code            = 403
    response_page_path    = "/index.html"
    response_code         = 200
    error_caching_min_ttl = 300
  }
}

resource "aws_cloudfront_origin_access_identity" "oai" {
  comment = "OAI for ${var.name}-${var.env}-web-frontend"
}
