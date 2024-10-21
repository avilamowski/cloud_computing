module "s3" {
  source = "./modules/s3"

  for_each = var.s3_buckets

  s3_name       = each.key
  s3_is_website = each.value.website
  s3_versioning = each.value.versioning
}

locals {
  vpc_id      = module.vpc.vpc_id
  subnet_ids  = slice(module.vpc.private_subnets, 0, 2) # First two private subnets are for lambdas
  lambda_role = data.aws_iam_role.lab_role
  lambda_env_vars = {
    DB_HOST     = module.rds_proxy.proxy_endpoint
    DB_NAME     = var.rds.db_name
    DB_PORT     = var.rds.db_port
    SECRET_NAME = aws_secretsmanager_secret.db_credentials.name
  }
}

module "dockerized_lambdas" {
  source = "./modules/dockerized_lambdas"

  lambda_role_arn       = local.lambda_role.arn
  lambda_vpc_id         = local.vpc_id
  lambda_names          = var.dockerized_lambda_names
  lambda_subnets        = local.subnet_ids
  lambda_env_vars       = local.lambda_env_vars
  lambda_aws_account_id = data.aws_caller_identity.current.account_id
  lambda_region_name    = data.aws_region.current.name
}


locals {
  environment_variables = {
    "upload_image" = {
      "BUCKET_NAME" = module.s3["uploaded-images"].bucket_name
    }
    "redirect" = {
      "FRONTEND_URL" = module.s3["soul-pupils-spa"].frontend_endpoint
    }
  }
}


module "zipped_lambda" {
  source                = "./modules/zipped_lambda"
  for_each              = toset(var.zipped_lambdas)
  lambda_name           = each.key
  environment_variables = local.environment_variables[each.key]
  lambda_role_arn       = data.aws_iam_role.lab_role.arn
  source_code_hash      = data.archive_file.zipped_lambdas[each.key].output_base64sha256
}

resource "aws_vpc_security_group_egress_rule" "lambda_sg_egress" {
  security_group_id            = module.dockerized_lambdas.lambda_sg.id
  from_port                    = 5432
  to_port                      = 5432
  ip_protocol                  = "tcp"
  referenced_security_group_id = aws_security_group.proxy_sg.id
  depends_on                   = [module.dockerized_lambdas]

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
  redirect_lambda     = module.zipped_lambda["redirect"]
  upload_image_lambda = module.zipped_lambda["upload_image"]
  private_lambdas     = module.dockerized_lambdas.lambdas
  regional_lambdas = {
    (local.upload_image_lambda.function_name) = local.upload_image_lambda
    (local.redirect_lambda.function_name)     = local.redirect_lambda
  }

  all_lambdas = merge(local.private_lambdas, local.regional_lambdas)
}

resource "aws_apigatewayv2_integration" "api_integration" {
  for_each           = { for endpoint in var.api_endpoints : endpoint.name => endpoint }
  api_id             = aws_apigatewayv2_api.api_gateway.id
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
  integration_uri    = local.all_lambdas[each.value.name].invoke_arn
}

resource "aws_lambda_permission" "apigw_lambda" {
  for_each      = { for endpoint in var.api_endpoints : endpoint.name => endpoint }
  statement_id  = each.value.name
  action        = "lambda:InvokeFunction"
  function_name = each.value.name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.api_gateway.execution_arn}/*/*/${each.value.name}"
  depends_on    = [aws_apigatewayv2_integration.api_integration]

}

resource "aws_apigatewayv2_authorizer" "soul_pupils" {
  api_id           = aws_apigatewayv2_api.api_gateway.id
  name             = "soul-pupils-authorizer"
  authorizer_type  = "JWT"
  identity_sources = ["$request.header.Authorization"]

  jwt_configuration {
    audience = [aws_cognito_user_pool_client.userpool_client.id]
    issuer   = format("%s%s", "https://", aws_cognito_user_pool.soul_pupils.endpoint)
  }
}

resource "aws_apigatewayv2_route" "api_route" {
  for_each             = { for endpoint in var.api_endpoints : endpoint.name => endpoint }
  api_id               = aws_apigatewayv2_api.api_gateway.id
  route_key            = "${each.value.method} ${each.value.path}"
  target               = "integrations/${aws_apigatewayv2_integration.api_integration[each.value.name].id}"
  authorizer_id        = each.value.require_authorization ? aws_apigatewayv2_authorizer.soul_pupils.id : null
  authorization_type   = each.value.require_authorization ? "JWT" : null
  authorization_scopes = each.value.authorization_scopes
}

resource "aws_apigatewayv2_stage" "api_stage" {
  api_id      = aws_apigatewayv2_api.api_gateway.id
  name        = "dev"
  auto_deploy = true
  lifecycle {
    create_before_destroy = true
  }
  depends_on = [aws_apigatewayv2_route.api_route]

}
