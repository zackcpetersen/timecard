resource "aws_iam_role" "destination_migration" {
  provider = aws.destination_account
  name = "S3MigrationRole"
  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Principal" : {
          "AWS" : data.aws_iam_user.destination_user.arn
        },
        "Action" : "sts:AssumeRole",
        "Condition" : {}
      }
    ]
  })
}

resource "aws_iam_policy" "destination_migration" {
  provider = aws.destination_account
  name = "S3MigrationPolicy"
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : [
          "s3:ListBucket",
          "s3:GetObject",
          "s3:GetObjectTagging",
          "s3:GetObjectVersion",
          "s3:GetObjectVersionTagging"
        ],
        "Resource" : [
          data.aws_s3_bucket.source_bucket.arn,
          "${data.aws_s3_bucket.source_bucket.arn}/*"
        ]
      },
      {
        "Effect" : "Allow",
        "Action" : [
          "s3:ListBucket",
          "s3:PutObject",
          "s3:PutObjectAcl",
          "s3:PutObjectTagging",
          "s3:GetObjectTagging",
          "s3:GetObjectVersion",
          "s3:GetObjectVersionTagging"
        ],
        "Resource" : [
          data.aws_s3_bucket.destination_bucket.arn,
          "${data.aws_s3_bucket.destination_bucket.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "destination_migration" {
  provider   = aws.destination_account
  role       = aws_iam_role.destination_migration.name
  policy_arn = aws_iam_policy.destination_migration.arn

  depends_on = [
    aws_iam_policy.destination_migration,
    aws_iam_role.destination_migration,
  ]
}


