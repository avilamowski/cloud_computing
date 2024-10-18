

resource "aws_cognito_user_pool" "soul-pupils" {
  name = "soul-pupils"

  email_configuration {
    email_sending_account = "COGNITO_DEFAULT"
  }

  auto_verified_attributes = ["email"]

  username_attributes = ["email"]

  lambda_config {
    post_confirmation = module.dockerized_lambdas.lambdas["create_user"].arn
  }
}

resource "aws_lambda_permission" "allow_cognito_to_invoke" {
  statement_id  = "AllowExecutionFromCognito"
  action        = "lambda:InvokeFunction"
  function_name = module.dockerized_lambdas.lambdas["create_user"].function_name
  principal     = "cognito-idp.amazonaws.com"
  source_arn    = aws_cognito_user_pool.soul-pupils.arn
}

resource "random_id" "random" {
  byte_length = 8
}

resource "aws_cognito_user_pool_domain" "soul-pupils" {
  domain       = "soul-pupils-app-auth-${random_id.random.hex}"
  user_pool_id = aws_cognito_user_pool.soul-pupils.id
}

resource "aws_cognito_user_pool_client" "userpool_client" {
  name                                 = "soul-pupils-client"
  user_pool_id                         = aws_cognito_user_pool.soul-pupils.id
  callback_urls                        = ["${aws_lambda_function_url.redirect.function_url}", "http://localhost:5173/callback"]
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_flows                  = ["code"]
  allowed_oauth_scopes                 = ["email", "openid"]
  supported_identity_providers         = ["COGNITO"]

  access_token_validity  = 1
  id_token_validity      = 1
  refresh_token_validity = 30
}

resource "terraform_data" "cognito_base_url" {
  input = "https://${aws_cognito_user_pool_domain.soul-pupils.domain}.auth.${data.aws_region.current.name}.amazoncognito.com/"
  triggers_replace = [
    aws_cognito_user_pool_domain.soul-pupils.domain,
    data.aws_region.current.name
  ]
}

resource "terraform_data" "zip_lambda_redirect" {
  provisioner "local-exec" {
    command = "zip -j ${path.cwd}/lambda_redirect.zip ${path.cwd}/../backend/redirect.py"
  }
  triggers_replace = {
    always_run = "${timestamp()}" # TODO: Check hash?
  }
}

resource "aws_lambda_function" "redirect" {
  depends_on = [terraform_data.zip_lambda_redirect]

  function_name = "redirect"
  timeout       = 60
  filename      = "${path.cwd}/lambda_redirect.zip"
  handler       = "redirect.lambda_handler"
  #   source_code_hash = filebase64sha256("${path.cwd}/lambda_redirect.zip")
  runtime       = "python3.11"
  architectures = ["x86_64"]
  role          = data.aws_iam_role.lab_role.arn
  environment {
    variables = {
      "frontend_url" = module.s3["soul-pupils-spa"].frontend_endpoint
    }
  }
}

resource "aws_lambda_function_url" "redirect" {
  function_name      = aws_lambda_function.redirect.function_name
  authorization_type = "NONE"

  cors {
    allow_credentials = true
    allow_origins     = ["*"]
    allow_methods     = ["*"]
    allow_headers     = ["date", "keep-alive"]
    expose_headers    = ["keep-alive", "date"]
    max_age           = 86400
  }
}
