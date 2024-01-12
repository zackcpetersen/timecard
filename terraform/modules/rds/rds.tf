# create subnet group with private subnets
resource "aws_db_subnet_group" "main" {
  name       = "main"
  subnet_ids = var.private_subnets

  tags = var.tags
}

# create db random password
resource "random_password" "db_password" {
  length           = 25
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

# create db
resource "aws_db_instance" "main_db" {
  #  snapshot_identifier   = var.db_snapshot_name
  allocated_storage          = var.db_allocated_storage
  max_allocated_storage      = var.db_max_storage
  engine                     = "postgres"
  engine_version             = var.rds_engine_version
  instance_class             = var.db_instance_class
  identifier                 = "${var.name}-${var.env}-db"
  db_name                    = var.name
  username                   = var.name
  password                   = random_password.db_password.result
  port                       = var.db_port
  parameter_group_name       = var.rds_parameter_group_name
  auto_minor_version_upgrade = true
  backup_retention_period    = 30
  db_subnet_group_name       = aws_db_subnet_group.main.name
  vpc_security_group_ids     = [var.rds_sg_id]
  #  storage_encrypted            = true
  deletion_protection          = var.deletion_protection
  skip_final_snapshot          = var.skip_final_snapshot
  final_snapshot_identifier    = "terraform-final-snapshot-${var.name}-${var.env}-db"
  apply_immediately            = var.apply_immediately
  performance_insights_enabled = var.performance_insights_enabled
  tags                         = var.tags

  lifecycle {
    ignore_changes = [
      snapshot_identifier,
      // any other attributes you want to ignore after creation
    ]
  }
}
