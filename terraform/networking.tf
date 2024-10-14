module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = var.vpc.vpc_name
  cidr = var.vpc.vpc_cidr

  azs                  = slice(data.aws_availability_zones.available.names, 0, 2)
  private_subnets      = cidrsubnets(var.vpc.vpc_cidr, 8, 8, 8, 8)
  private_subnet_names = var.vpc.private_subnet_names

  tags = {
    Name = var.vpc.vpc_name
  }
}
