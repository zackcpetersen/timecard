# Create S3 bucket for static assets in Django ECS tasks
resource "aws_s3_bucket" "django_ecs_static" {
  bucket        = "${var.env}-${var.name}-staticfiles"
  force_destroy = var.force_destroy
  tags          = var.tags
}

# create s3 bucket for static website hosting
resource "aws_s3_bucket" "frontend_static_site" {
  bucket = "${var.name}-${var.env}-web-frontend"
  tags   = var.tags
}
# allow versioning
resource "aws_s3_bucket_versioning" "static_site_versioning" {
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

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_acl" "frontend" {
  depends_on = [
    aws_s3_bucket_ownership_controls.frontend,
    aws_s3_bucket_public_access_block.frontend,
  ]

  bucket = aws_s3_bucket.frontend_static_site.id
  acl    = "public-read"
}

# add custom bucket policy # TODO test frontend bucket
#resource "aws_s3_bucket_policy" "public_read_access" {
#  bucket = aws_s3_bucket.frontend_static_site.id
#  policy = jsonencode({
#    "Version" : "2012-10-17",
#    "Statement" : [
#      {
#        "Sid" : "PublicReadGetObject",
#        "Effect" : "Allow",
#        "Principal" : "*",
#        "Action" : "s3:GetObject",
#        "Resource" : "${aws_s3_bucket.frontend_static_site.arn}/*"
#      }
#    ]
#  })
#}
