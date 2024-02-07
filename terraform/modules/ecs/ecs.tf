# Create ECS Cluster
resource "aws_ecs_cluster" "cluster" {
  name = "${var.name}-${var.env}"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# Create API Service 
module "services" {
  source                     = "./services"
  cluster_id                 = aws_ecs_cluster.cluster.id
  cluster_name               = aws_ecs_cluster.cluster.name
  env                        = var.env
  debug                      = var.debug
  aws_region                 = var.aws_region
  name                       = var.name
  ecs_execution_role         = var.ecs_execution_role
  ecs_task_role              = var.ecs_task_role
  vpc_id                     = var.vpc_id
  public_subnets             = var.public_subnets
  tags                       = var.tags
  latest_tag                 = "latest"
  s3_static_bucket_name      = var.s3_static_bucket_name
  db_name                    = var.db_name
  db_user                    = var.db_user
  db_host                    = var.db_host
  db_port                    = var.db_port
  db_password                = var.db_password
  root_aws_access_key_id     = var.root_aws_access_key_id
  root_aws_secret_access_key = var.root_aws_secret_access_key
  django_secret_key          = var.django_secret_key
  ssl_redirect               = var.ssl_redirect
  cors_allowed_regexes       = var.cors_allowed_regexes
  allowed_hosts              = var.allowed_hosts
  cors_allow_all_origins     = var.cors_allow_all_origins
  default_domain             = var.default_domain
  frontend_url               = var.frontend_url
  ghcr_base_url              = var.ghcr_base_url
  github_username            = var.github_username
  github_token               = var.github_token
  web_version                = var.web_version
  nginx_version              = var.nginx_version
  deletion_protection        = var.deletion_protection
  api_task_cpu               = var.api_task_cpu
  api_task_memory            = var.api_task_memory
  backend_certificate_arn    = var.backend_certificate_arn
  default_admin_email        = var.default_admin_email
}
