locals {
  dev_env                = false
  cors_allow_all_origins = "False"
  debug                  = "False"
  secure_ssl_redirect    = "True"
  github_username        = "zackcpetersen"
  frontend_domain_name   = "www.${var.route53_domain_name}"
  backend_domain_name    = "backend.${var.route53_domain_name}"
  env                    = "production"
}

module "vpc" {
  source     = "../modules/vpc"
  name       = var.product_name
  env        = local.env
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
}

module "s3" {
  source             = "../modules/s3"
  name               = var.product_name
  env                = local.env
  tags               = var.global_tags
  dev_env            = local.dev_env
  cloudfront_oai_arn = module.cloudfront.cloudfront_oai_arn
}

module "acm" {
  source               = "../modules/acm"
  frontend_domain_name = local.frontend_domain_name
  backend_domain_name  = local.backend_domain_name
}

module "root_route53" {
  source                                 = "../modules/route53"
  env                                    = local.env
  aws_region                             = var.aws_region
  frontend_acm_domain_validation_options = module.acm.frontend_domain_validation_options
  backend_acm_domain_validation_options  = module.acm.backend_domain_validation_options
  frontend_certificate_arn               = module.acm.frontend_certificate_arn
  backend_certificate_arn                = module.acm.backend_certificate_arn
  route53_name                           = var.route53_domain_name
  backend_domain_name                    = local.backend_domain_name
  ecs_lb_name                            = module.ecs.api_testing_lb_url
  ROOT_AWS_ACCESS_KEY_ID                 = var.ROOT_AWS_ACCESS_KEY_ID
  ROOT_AWS_SECRET_ACCESS_KEY             = var.ROOT_AWS_SECRET_ACCESS_KEY
  frontend_cloudfront_domain             = module.cloudfront.cf_domain
  frontend_domain_name                   = local.frontend_domain_name
}

module "cloudfront" {
  source                     = "../modules/cloudfront"
  frontend_certificate_arn   = module.acm.frontend_certificate_arn
  dev_env                    = local.dev_env
  website_bucket_domain_name = module.s3.frontend_regional_domain_name
  website_bucket_origin_id   = "myS3Origin"
  frontend_domain_name       = local.frontend_domain_name
  env                        = local.env
  name                       = var.product_name
}

module "rds" {
  source                       = "../modules/rds"
  env                          = local.env
  private_subnets              = module.vpc.private_subnets
  vpc_id                       = module.vpc.vpc_id
  rds_sg_id                    = module.vpc.rds_sg_id
  tags                         = var.global_tags
  name                         = var.product_name
  db_port                      = var.db_port
  db_instance_class            = var.db_instance_class
  db_allocated_storage         = var.db_allocated_storage
  db_max_storage               = var.db_max_storage
  db_snapshot_name             = var.db_snapshot_name
  apply_immediately            = local.dev_env
  deletion_protection          = !local.dev_env
  skip_final_snapshot          = local.dev_env
  performance_insights_enabled = !local.dev_env
  rds_engine_version           = "15.2"
  rds_parameter_group_name     = "default.postgres15"
}

module "ecs" {
  source                     = "../modules/ecs"
  env                        = local.env
  debug                      = local.debug
  aws_region                 = var.aws_region
  name                       = var.product_name
  tags                       = var.global_tags
  ecs_execution_role         = module.iam.ecs_execution_role
  ecs_task_role              = module.iam.ecs_task_role
  vpc_id                     = module.vpc.vpc_id
  public_subnets             = module.vpc.public_subnets
  s3_static_bucket_name      = module.s3.s3_static_bucket_name
  db_name                    = module.rds.db_name
  db_user                    = module.rds.db_user
  db_host                    = module.rds.db_host
  db_port                    = module.rds.db_port
  db_password                = module.rds.db_password
  root_aws_access_key_id     = var.ROOT_AWS_ACCESS_KEY_ID
  root_aws_secret_access_key = var.ROOT_AWS_SECRET_ACCESS_KEY
  django_secret_key          = var.SECRET_KEY
  ssl_redirect               = local.secure_ssl_redirect
  cors_allowed_regexes       = var.CORS_ALLOWED_ORIGIN_REGEXES
  allowed_hosts              = ".${var.route53_domain_name}"
  cors_allow_all_origins     = local.cors_allow_all_origins
  default_domain             = local.frontend_domain_name
  default_admin_email        = var.DEFAULT_ADMIN_EMAIL
  frontend_url               = "https://${local.frontend_domain_name}"
  ghcr_base_url              = var.ghcr_base_url
  github_username            = local.github_username
  github_token               = var.github_token
  web_version                = var.web_version
  nginx_version              = var.nginx_version
  backend_certificate_arn    = module.acm.backend_certificate_arn
  deletion_protection        = !local.dev_env
  api_task_cpu               = 256
  api_task_memory            = 512
}
