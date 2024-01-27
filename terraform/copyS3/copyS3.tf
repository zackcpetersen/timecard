module "copyS3" {
  source                     = "../modules/copyS3"
  AWS_ACCESS_KEY_ID          = var.AWS_ACCESS_KEY_ID
  AWS_SECRET_ACCESS_KEY      = var.AWS_SECRET_ACCESS_KEY
  ROOT_AWS_ACCESS_KEY_ID     = var.ROOT_AWS_ACCESS_KEY_ID
  ROOT_AWS_SECRET_ACCESS_KEY = var.ROOT_AWS_SECRET_ACCESS_KEY
  aws_region                 = var.aws_region
  source_bucket_name         = var.source_bucket_name
  destination_bucket_name    = var.destination_bucket_name
  env                        = var.env
}
