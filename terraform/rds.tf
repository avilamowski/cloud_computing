resource "aws_db_subnet_group" "default_subnet_group" {
  name       = "default_subnet_group"
  subnet_ids = module.vpc.private_subnets
}

resource "aws_db_instance" "default" {
  allocated_storage      = 20
  db_name                = var.rds.db_name
  engine                 = "postgres"
  engine_version         = "16.3"
  instance_class         = "db.t4g.micro"
  username               = var.rds.db_username
  password               = var.rds.db_password
  availability_zone      = "us-east-1a"
  multi_az               = false
  publicly_accessible    = false
  db_subnet_group_name   = aws_db_subnet_group.default_subnet_group.name
  vpc_security_group_ids = [aws_security_group.bd_sg.id]
}

module "rds_proxy" {
  source = "terraform-aws-modules/rds-proxy/aws"


  name                   = "bd-sql-proxy"
  create_iam_role        = false
  vpc_subnet_ids         = module.vpc.private_subnets
  vpc_security_group_ids = [aws_security_group.proxy_sg.id]
  role_arn               = data.aws_iam_role.lab_role.arn

  # endpoints = {
  #   read_write = {
  #     name                   = "read-write-endpoint"
  #     vpc_subnet_ids         = module.vpc.private_subnets
  #     vpc_security_group_ids = [module.rds_proxy_sg.security_group_id]
  #     #   tags                   = []
  #   },
  #   read_only = {
  #     name                   = "read-only-endpoint"
  #     vpc_subnet_ids         = module.vpc.private_subnets
  #     vpc_security_group_ids = []
  #     target_role            = "READ_ONLY"
  #     #   tags                   = []
  #   }
  # }


  auth = {
    (var.rds.db_username) = {
      description = aws_secretsmanager_secret.db_credentials.description
      secret_arn  = aws_secretsmanager_secret.db_credentials.arn
    }
  }

  engine_family = "POSTGRESQL"
  debug_logging = true

  target_db_instance     = true
  db_instance_identifier = aws_db_instance.default.identifier

  depends_on = [aws_db_instance.default]
}


resource "aws_secretsmanager_secret" "db_credentials" {
  name        = "db_credentials1"
  description = "RDS database credentials"
}


resource "aws_secretsmanager_secret_version" "db_credentials_version" {
  secret_id = aws_secretsmanager_secret.db_credentials.id
  secret_string = jsonencode({
    username = var.rds.db_username
    password = var.rds.db_password
  })
}

resource "aws_security_group" "bd_sg" {
  vpc_id = module.vpc.vpc_id
  name   = "bd_sg"
}

resource "aws_security_group" "proxy_sg" {
  vpc_id = module.vpc.vpc_id
  name   = "proxy_sg"
}

resource "aws_vpc_security_group_ingress_rule" "bd_sg_ingress" {
  security_group_id            = aws_security_group.bd_sg.id
  from_port                    = 5432
  to_port                      = 5432
  ip_protocol                  = "tcp"
  referenced_security_group_id = aws_security_group.proxy_sg.id
}

resource "aws_vpc_security_group_ingress_rule" "proxy_sg_ingress" {
  security_group_id            = aws_security_group.proxy_sg.id
  from_port                    = 5432
  to_port                      = 5432
  ip_protocol                  = "tcp"
  referenced_security_group_id = module.dockerized_lambdas.lambda_sg.id
}

resource "aws_vpc_security_group_egress_rule" "proxy_sg_egress" {
  security_group_id            = aws_security_group.proxy_sg.id
  from_port                    = 5432
  to_port                      = 5432
  ip_protocol                  = "tcp"
  referenced_security_group_id = aws_security_group.bd_sg.id
}
