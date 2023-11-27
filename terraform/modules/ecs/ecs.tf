# Create ECS Cluster
resource "aws_ecs_cluster" "cluster" {
  name = "${var.name}-${var.env}"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# Create Elastic Container Repositories (ECR) 
resource "aws_ecr_repository" "web" {
  name                 = "${var.name}_web"
  image_tag_mutability = "MUTABLE"
  tags                 = var.tags
}
resource "aws_ecr_repository" "nginx" {
  name                 = "${var.name}_nginx"
  image_tag_mutability = "MUTABLE"
  tags                 = var.tags
}

# Create API Service 
module "services" {
  source                            = "./services"
  cluster_id                        = aws_ecs_cluster.cluster.id
  cluster_name                      = aws_ecs_cluster.cluster.name
  env                               = var.env
  debug                             = var.debug
  aws_region                        = var.aws_region
  aws_access_key_id                 = var.aws_access_key_id
  name                              = var.name
  github_repo                       = var.github_repo
  ecs_task_execution_role           = var.ecs_task_execution_role
  vpc_id                            = var.vpc_id
  public_subnets                    = var.public_subnets
  private_subnets                   = var.private_subnets
  tags                              = var.tags
  ecr_web_repo_name                 = aws_ecr_repository.web.name
  ecr_nginx_repo_name               = aws_ecr_repository.nginx.name
  latest_tag                        = "latest" # TODO want to version?
  ecs_django_static_s3_access_creds = var.ecs_django_static_s3_access_creds
  s3_static_bucket_name             = var.s3_static_bucket_name
  db_name                           = var.db_name
  db_user                           = var.db_user
  db_host                           = var.db_host
  db_port                           = var.db_port
  django_secret_key                 = var.django_secret_key
  ssl_redirect                      = var.ssl_redirect
  cors_allowed_regexes              = var.cors_allowed_regexes
  allowed_hosts                     = var.allowed_hosts
  cors_allow_all_origins            = false
  default_domain                    = var.default_domain
  frontend_url                      = var.frontend_url
  gmail_client_id                   = var.gmail_client_id
  gmail_client_secret               = var.gmail_client_secret
  gmail_project_id                  = var.gmail_project_id
}
