#module "vpc" {
#  source           = "../modules/vpc"
#  name             = var.product_name
#  env              = var.env
#  aws_region       = var.aws_region
#  tags             = var.global_tags
#  db_port          = var.db_port
#  elasticache_port = var.elasticache_port
#}
#
#module "iam" {
#  source                       = "../modules/iam"
#  name                         = var.product_name
#  users                        = var.users
#  tags                         = var.global_tags
#  django_ecs_static_bucket_arn = module.s3.django_ecs_static_bucket_arn
#
#  depends_on = [module.s3]
#}
#
#module "s3" {
#  source = "../modules/s3"
#  name   = var.product_name
#  env    = var.env
#  tags   = var.global_tags
#}
#
#module "rds" {
#  source               = "../modules/rds"
#  env                  = var.env
#  private_subnets      = module.vpc.private_subnets
#  vpc_id               = module.vpc.vpc_id
#  rds_sg_id            = module.vpc.rds_sg_id
#  tags                 = var.global_tags
#  name                 = var.product_name
#  db_port              = var.db_port
#  db_instance_class    = var.db_instance_class
#  db_allocated_storage = var.db_allocated_storage
#  db_max_storage       = var.db_max_storage
#  db_snapshot_name     = var.db_snapshot_name
#
#  depends_on = [module.vpc]
#}
#
#module "ecs" {
#  source                            = "../modules/ecs"
#  env                               = var.env
#  debug                             = var.debug
#  aws_region                        = var.aws_region
#  name                              = var.product_name
#  github_repo                       = var.github_repo
#  tags                              = var.global_tags
#  ecs_task_execution_role           = module.iam.ecs_task_execution_role
#  vpc_id                            = module.vpc.vpc_id
#  public_subnets                    = module.vpc.public_subnets
#  private_subnets                   = module.vpc.private_subnets
#  ecs_django_static_s3_access_creds = module.iam.ecs_django_static_s3_access_creds
#  s3_static_bucket_name             = module.s3.s3_static_bucket_name
#  db_name                           = var.db_name
#  db_user                           = var.db_user
#  db_host                           = module.rds.db_host
#  db_port                           = module.rds.db_port
#  redis_primary_endpoint            = module.elasticache.redis_primary_endpoint
#  redis_port                        = module.elasticache.redis_port
##  opensearch_endpoint               = module.opensearch.opensearch_endpoint
#  django_secret_key                 = var.DJANGO_SECRET_KEY
#  email_host_password               = var.EMAIL_HOST_PASSWORD
#  email_host                        = var.email_host
#  email_port                        = var.email_port
#  email_host_user                   = var.email_host_user
#  email_use_tls                     = var.email_use_tls
#  default_from_email                = var.default_from_email
#  ssl_redirect                      = var.ssl_redirect
#  cors_allowed_regexes              = var.cors_allowed_regexes
#  allowed_hosts                     = var.allowed_hosts
#  use_elastic                       = var.use_elastic
#
#  depends_on = [
#    module.iam,
#    module.vpc,
#    module.rds,
#    module.s3,
#  ]
#}
