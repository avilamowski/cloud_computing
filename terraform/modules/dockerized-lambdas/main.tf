resource "aws_ecr_repository" "repository" {
  for_each = toset(var.lambda_names)

  name = each.key

  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
}


resource "aws_lambda_function" "this" {
  depends_on = [terraform_data.deploy_images]
  for_each   = toset(var.lambda_names)

  function_name = each.key
  timeout       = 60
  image_uri     = "${aws_ecr_repository.repository[each.key].repository_url}:latest"
  package_type  = "Image"
  architectures = ["x86_64"]
  vpc_config {
    security_group_ids = [aws_security_group.lambda_sg.id]
    subnet_ids         = var.lambda_subnets
  }
  environment {
    variables = var.lambda_env_vars
  }
  role = var.lambda_role_arn
}

resource "terraform_data" "deploy_images" {
  depends_on = [aws_ecr_repository.repository]

  provisioner "local-exec" {
    working_dir = "${path.cwd}/scripts"
    command     = "${path.cwd}/scripts/deploy_all.sh ${var.lambda_aws_account_id}"
  }
  triggers_replace = {
    always_run = "${timestamp()}"
  }
}

resource "aws_security_group" "lambda_sg" {
  vpc_id = var.lambda_vpc_id
  name   = "lambda_sg"
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "vpc_endpoint_sg" {
  vpc_id = var.lambda_vpc_id
  name   = "vpc_endpoint_sg"
  ingress {
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    security_groups = [aws_security_group.lambda_sg.id]
  }
  egress {
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    security_groups = [aws_security_group.lambda_sg.id]
  }
}

resource "aws_vpc_security_group_ingress_rule" "lambda_vpc_endpoint" {
  security_group_id            = aws_security_group.lambda_sg.id
  from_port                    = 443
  to_port                      = 443
  ip_protocol                  = "tcp"
  referenced_security_group_id = aws_security_group.vpc_endpoint_sg.id
}

resource "aws_vpc_security_group_egress_rule" "lambda_vpc_endpoint" {
  security_group_id            = aws_security_group.lambda_sg.id
  from_port                    = 443
  to_port                      = 443
  ip_protocol                  = "tcp"
  referenced_security_group_id = aws_security_group.vpc_endpoint_sg.id
}


resource "aws_vpc_endpoint" "secrets_manager" {
  vpc_id              = var.lambda_vpc_id
  service_name        = "com.amazonaws.${var.lambda_region_name}.secretsmanager"
  vpc_endpoint_type   = "Interface"
  security_group_ids  = [aws_security_group.vpc_endpoint_sg.id]
  subnet_ids          = var.lambda_subnets
  private_dns_enabled = true

  tags = {
    Name = "secrets_manager_vpc_endpoint"
  }
}

