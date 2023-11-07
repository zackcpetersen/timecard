# Create VPC
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "vpc-${var.env}"
  cidr = "10.0.0.0/16"

  azs                 = ["${var.aws_region}a", "${var.aws_region}b", "${var.aws_region}c"]
  private_subnets     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets      = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  elasticache_subnets = ["10.0.31.0/24", "10.0.32.0/24"]

  #  enable_vpn_gateway = true  # TODO maybe?
  #  enable_nat_gateway = true  # TODO maybe?

  tags = var.tags
}

# Create security group for RDS
resource "aws_security_group" "db_sg" {
  name        = "${var.name}_database_sg_${var.env}"
  description = "Allow incoming traffic to port ${var.db_port} from VPC CIDR blocks"
  vpc_id      = module.vpc.vpc_id

  ingress {
    description = "Allow traffic from private subnets into database"
    from_port   = var.db_port
    to_port     = var.db_port
    protocol    = "tcp"
    cidr_blocks = module.vpc.vpc_cidr_block[*]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = var.tags
}
