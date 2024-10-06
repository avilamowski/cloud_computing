module "s3" {
  source = "./modules/s3"

  for_each = var.s3_buckets

  s3_name       = each.key
  s3_is_website = each.value.website
  s3_versioning = each.value.versioning
}

locals {
  vpc_id      = module.vpc.vpc_id
  subnet_ids  = module.vpc.private_subnets
  lambda_role = data.aws_iam_role.lab_role
  lambda_env_vars = {
    DB_HOST = module.rds_proxy.proxy_endpoint
    DB_NAME = var.rds.db_name
    DB_USER = var.rds.db_username
    DB_PASS = var.rds.db_password
    DB_PORT = var.rds.db_port
  }
}

module "dockerized_lambdas" {
  source = "./modules/dockerized-lambdas"

  lambda_role_arn       = local.lambda_role.arn
  lambda_vpc_id         = local.vpc_id
  lambda_names          = var.lambda_names
  lambda_subnets        = local.subnet_ids
  lambda_env_vars       = local.lambda_env_vars
  lambda_aws_account_id = data.aws_caller_identity.current.account_id
}

resource "aws_vpc_security_group_egress_rule" "lambda_sg_egress" {
  depends_on                   = [module.dockerized_lambdas]
  security_group_id            = module.dockerized_lambdas.lambda_sg.id
  from_port                    = 5432
  to_port                      = 5432
  ip_protocol                  = "tcp"
  referenced_security_group_id = aws_security_group.proxy_sg.id
}
