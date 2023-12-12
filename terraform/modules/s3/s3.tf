# Create S3 bucket for static assets in Django ECS tasks
resource "aws_s3_bucket" "django_ecs_static" {
  bucket = "${var.env}-${var.name}-media"
  tags   = var.tags
}
# TODO why is this not working?
## Add public acl policy
#resource "aws_s3_bucket_acl" "static_public" {
#  bucket = aws_s3_bucket.django_ecs_static.id
#  acl    = "public-read"
#}

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
    suffix = "index.html" # TODO double check this
  }

  error_document {
    key = "index.html" # TODO double check this
  }
}

# TODO why is this not working?
## add custom bucket policy
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
