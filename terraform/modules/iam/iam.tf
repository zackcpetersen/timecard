data "aws_partition" "current" {}

# ------------- #
### IAM USERS ###
# ------------- #

# create admin group
resource "aws_iam_group" "admins" {
  name = "admins"
}

# attach AWS managed AdministratorAccess policy to admin group
#  WARNING - running `terraform destroy` will remove admin access 
#   for ALL users/groups/roles, not just those managed in terraform
resource "aws_iam_policy_attachment" "admins-attach" {
  name       = "admins-attach"
  groups     = [aws_iam_group.admins.name]
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}

# add users
resource "aws_iam_user" "admin_users" {
  count = length(var.users)
  name  = var.users[count.index]
  tags  = var.tags
}

# add users to group
resource "aws_iam_group_membership" "admin_membership" {
  name  = "admins-users"
  users = var.users
  group = aws_iam_group.admins.name

  depends_on = [aws_iam_group.admins]
}

# ------------- #
### ECS ROLES ###
# ------------- #
# role for ecs task execution
resource "aws_iam_role" "ECSTaskExecutionRole" {
  name = "${var.name}ECSTaskExecutionRole"
  tags = var.tags

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com" # ecs.amazonaws.com
        }
      },
    ]
  })
}

# custom KMS decrypt policy
resource "aws_iam_policy" "kms_decrypt" {
  name        = "KMSDecrypt"
  description = "Used to decrypt KMS keys"
  tags        = var.tags
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Sid" : "VisualEditor0",
        "Effect" : "Allow",
        "Action" : [
          "kms:Decrypt"
        ],
        "Resource" : "*"
      }
    ]
    }
  )
}

# attach policies to ECS role
resource "aws_iam_role_policy_attachment" "ecs_task_execution" {
  role       = aws_iam_role.ECSTaskExecutionRole.id
  policy_arn = "arn:${data.aws_partition.current.partition}:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}
resource "aws_iam_role_policy_attachment" "ssm_read_only" {
  role       = aws_iam_role.ECSTaskExecutionRole.id
  policy_arn = "arn:${data.aws_partition.current.partition}:iam::aws:policy/AmazonSSMReadOnlyAccess"
}
resource "aws_iam_role_policy_attachment" "kms_decrypt" {
  role       = aws_iam_role.ECSTaskExecutionRole.id
  policy_arn = aws_iam_policy.kms_decrypt.arn
}

# ----------- #
### S3 USER ###
# ----------- #

# User to access S3 buckets from inside ECS api app
resource "aws_iam_user" "ecs_s3_access" {
  name = "${var.name}-ecs-s3-access"
  tags = var.tags
}
# custom S3 bucket policy for ecs_s3_access
resource "aws_iam_policy" "ecs_s3_access" {
  name        = "${var.name}-ecs-s3-access"
  description = "Allows ECS tasks to access S3 bucket contents for django-storages"
  tags        = var.tags
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : [
          "s3:PutObject",
          "s3:GetObjectAcl",
          "s3:GetObject",
          "s3:ListBucket",
          "s3:DeleteObject",
          "s3:PutObjectAcl"
        ],
        "Resource" : [
          "${var.django_ecs_static_bucket_arn}/*",
          var.django_ecs_static_bucket_arn
        ]
      }
    ]
  })
}
# attach policy to user
resource "aws_iam_user_policy_attachment" "ecs_s3_access" {
  user       = aws_iam_user.ecs_s3_access.id
  policy_arn = aws_iam_policy.ecs_s3_access.arn
}
# create access key and secret access key for IAM user to be used in ECS
resource "aws_iam_access_key" "ecs_s3_access_key" {
  user = aws_iam_user.ecs_s3_access.name
}
