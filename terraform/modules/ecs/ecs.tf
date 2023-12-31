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
  source                           = "./services"
  cluster_id                       = aws_ecs_cluster.cluster.id
  cluster_name                     = aws_ecs_cluster.cluster.name
  env                              = var.env
  debug                            = var.debug
  aws_region                       = var.aws_region
  name                             = var.name
  github_repo                      = var.github_repo
  ecs_execution_role               = var.ecs_execution_role
  ecs_task_role                    = var.ecs_task_role
  vpc_id                           = var.vpc_id
  public_subnets                   = var.public_subnets
  private_subnets                  = var.private_subnets
  tags                             = var.tags
  latest_tag                       = "latest"
  s3_static_bucket_name            = var.s3_static_bucket_name
  db_name                          = var.db_name
  db_user                          = var.db_user
  db_host                          = var.db_host
  db_port                          = var.db_port
  db_password                      = var.db_password
  django_secret_key                = var.django_secret_key
  ssl_redirect                     = var.ssl_redirect
  cors_allowed_regexes             = var.cors_allowed_regexes
  allowed_hosts                    = var.allowed_hosts
  cors_allow_all_origins           = var.cors_allow_all_origins
  default_domain                   = var.default_domain
  frontend_url                     = var.frontend_url
  gmail_client_id                  = var.gmail_client_id
  gmail_client_secret              = var.gmail_client_secret
  gmail_project_id                 = var.gmail_project_id
  ghcr_base_url                    = var.ghcr_base_url
  github_username                  = var.github_username
  github_token                     = var.github_token
  image_tag                        = var.image_tag
  deletion_protection              = var.deletion_protection
  api_container_cpu                = var.api_container_cpu
  api_task_cpu                     = var.api_task_cpu
  api_task_memory                  = var.api_task_memory
  api_container_memory_reservation = var.api_container_memory_reservation
  backend_certificate_arn          = var.backend_certificate_arn
}
