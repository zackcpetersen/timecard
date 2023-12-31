output "cf_domain" {
  value = aws_cloudfront_distribution.s3_distribution.domain_name
}

output "cloudfront_oai_arn" {
  value = aws_cloudfront_origin_access_identity.oai.iam_arn
}
