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
    DB_HOST     = module.rds_proxy.proxy_endpoint
    DB_NAME     = var.rds.db_name
    DB_USER     = var.rds.db_username
    DB_PASSWORD = var.rds.db_password
    DB_PORT     = var.rds.db_port
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

resource "aws_apigatewayv2_api" "api_gateway" {
  name          = "sp-api-gw"
  description   = "API Gateway for Soul Pupils"
  protocol_type = "HTTP"

  cors_configuration {
    allow_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
    allow_headers = ["*"]
    allow_origins = ["*"]
  }
}

locals {
  private_lambdas = module.dockerized_lambdas.lambdas
  regional_lambdas = {
    (aws_lambda_function.upload_file_lambda.function_name) = aws_lambda_function.upload_file_lambda
  }

  all_lambdas = merge(local.private_lambdas, local.regional_lambdas)
}


resource "aws_apigatewayv2_integration" "api_integration" {
  depends_on         = [aws_apigatewayv2_api.api_gateway]
  for_each           = { for endpoint in var.api_endpoints : endpoint.name => endpoint }
  api_id             = aws_apigatewayv2_api.api_gateway.id
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
  integration_uri    = local.all_lambdas[each.value.name].invoke_arn
}

resource "aws_apigatewayv2_route" "api_route" {
  depends_on = [aws_apigatewayv2_api.api_gateway, aws_apigatewayv2_integration.api_integration]
  for_each   = { for endpoint in var.api_endpoints : endpoint.name => endpoint }
  api_id     = aws_apigatewayv2_api.api_gateway.id
  route_key  = "${each.value.method} ${each.value.path}"
  target     = "integrations/${aws_apigatewayv2_integration.api_integration[each.value.name].id}"
}

resource "aws_apigatewayv2_stage" "api_stage" {
  depends_on  = [aws_apigatewayv2_route.api_route]
  api_id      = aws_apigatewayv2_api.api_gateway.id
  name        = "dev"
  auto_deploy = true
  lifecycle {
    create_before_destroy = true
  }
}

