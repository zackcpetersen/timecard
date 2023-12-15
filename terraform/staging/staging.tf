locals {
  force_destroy = true # false in production
  dev_database  = true # false in production
}

module "vpc" {
  source     = "../modules/vpc"
  name       = var.product_name
  env        = var.env
  aws_region = var.aws_region
  tags       = var.global_tags
  db_port    = var.db_port
}

module "iam" {
  source                       = "../modules/iam"
  name                         = var.product_name
  users                        = var.users
  tags                         = var.global_tags
  django_ecs_static_bucket_arn = module.s3.django_ecs_static_bucket_arn

  depends_on = [module.s3]
}

module "s3" {
  source        = "../modules/s3"
  name          = var.product_name
  env           = var.env
  tags          = var.global_tags
  force_destroy = local.force_destroy
}

module "rds" {
  source               = "../modules/rds"
  env                  = var.env
  private_subnets      = module.vpc.private_subnets
  vpc_id               = module.vpc.vpc_id
  rds_sg_id            = module.vpc.rds_sg_id
  tags                 = var.global_tags
  name                 = var.product_name
  db_port              = var.db_port
  db_instance_class    = var.db_instance_class
  db_allocated_storage = var.db_allocated_storage
  db_max_storage       = var.db_max_storage
  db_snapshot_name     = var.db_snapshot_name
  apply_immediately    = local.dev_database
  deletion_protection  = !local.dev_database
  skip_final_snapshot  = local.dev_database

  depends_on = [module.vpc]
}

module "ecs" {
  source                 = "../modules/ecs"
  env                    = var.env
  debug                  = var.DEBUG
  aws_region             = var.aws_region
  name                   = var.product_name
  github_repo            = var.github_repo
  tags                   = var.global_tags
  ecs_execution_role     = module.iam.ecs_execution_role
  ecs_task_role          = module.iam.ecs_task_role
  vpc_id                 = module.vpc.vpc_id
  public_subnets         = module.vpc.public_subnets
  private_subnets        = module.vpc.private_subnets
  s3_static_bucket_name  = module.s3.s3_static_bucket_name
  db_name                = module.rds.db_name
  db_user                = module.rds.db_user
  db_host                = module.rds.db_host
  db_port                = module.rds.db_port
  db_password            = module.rds.db_password
  django_secret_key      = var.SECRET_KEY
  ssl_redirect           = var.SECURE_SSL_REDIRECT
  cors_allowed_regexes   = var.CORS_ALLOWED_ORIGIN_REGEXES
  allowed_hosts          = var.ALLOWED_HOSTS
  cors_allow_all_origins = var.CORS_ALLOW_ALL_ORIGINS
  default_domain         = var.DEFAULT_DOMAIN
  frontend_url           = var.FRONTEND_URL
  gmail_client_id        = var.GMAIL_CLIENT_ID
  gmail_client_secret    = var.GMAIL_CLIENT_SECRET
  gmail_project_id       = var.GMAIL_PROJECT_ID
  ghcr_base_url          = var.ghcr_base_url
  github_username        = var.github_username
  github_token           = var.github_token
  image_tag              = var.image_tag

  depends_on = [
    module.iam,
    module.vpc,
    module.rds,
    module.s3,
  ]
}
