resource "aws_s3_bucket_policy" "source_policy" {
  provider = aws.source_account
  bucket = data.aws_s3_bucket.source_bucket.id
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Sid" : "DelegateS3Access",
        "Effect" : "Allow",
        "Principal" : {
          "AWS" : aws_iam_role.destination_migration.arn,
        },
        "Action" : [
          "s3:ListBucket",
          "s3:GetObject",
          "s3:GetObjectTagging",
          "s3:GetObjectVersion",
          "s3:GetObjectVersionTagging"
        ],
        "Resource" : [
          data.aws_s3_bucket.source_bucket.arn,
          "${data.aws_s3_bucket.source_bucket.arn}/*",
        ]
      }
    ]
  })
}
