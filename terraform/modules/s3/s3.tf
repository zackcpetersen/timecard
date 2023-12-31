# Create S3 bucket for static assets in Django ECS tasks
resource "aws_s3_bucket" "django_ecs_static" {
  bucket        = "${var.env}-${var.name}-staticfiles"
  force_destroy = var.dev_env
  tags          = var.tags
}

# create s3 bucket for static website hosting
resource "aws_s3_bucket" "frontend_static_site" {
  bucket        = "${var.name}-${var.env}-web-frontend"
  force_destroy = var.dev_env
  tags          = var.tags
}
# allow versioning
resource "aws_s3_bucket_versioning" "static_site_versioning" {
  count  = var.dev_env ? 0 : 1
  bucket = aws_s3_bucket.frontend_static_site.id
  versioning_configuration {
    status = "Enabled"
  }
}
# add static website config
resource "aws_s3_bucket_website_configuration" "static_site_config" {
  bucket = aws_s3_bucket.frontend_static_site.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "index.html"
  }
}
resource "aws_s3_bucket_ownership_controls" "frontend" {
  bucket = aws_s3_bucket.frontend_static_site.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}
resource "aws_s3_bucket_public_access_block" "frontend" {
  bucket = aws_s3_bucket.frontend_static_site.id

  block_public_acls   = true
  block_public_policy = true
}

# Update your IAM policy on S3 to allow the OAI access
resource "aws_s3_bucket_policy" "allow_cloudfront" {
  bucket = aws_s3_bucket.frontend_static_site.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action   = "s3:GetObject",
        Effect   = "Allow",
        Resource = "${aws_s3_bucket.frontend_static_site.arn}/*",
        Principal = {
          AWS = var.cloudfront_oai_arn
        }
      }
    ]
  })
}
