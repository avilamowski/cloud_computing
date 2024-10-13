locals {
  frontend_bucket_name = module.s3["soul-pupils-spa"].bucket_name
  api_endpoint         = aws_apigatewayv2_api.api_gateway.api_endpoint
  stage                = aws_apigatewayv2_stage.api_stage.name
}

resource "terraform_data" "upload_build" {
  depends_on = [module.s3, aws_apigatewayv2_api.api_gateway]

  provisioner "local-exec" {
    command = "${path.cwd}/scripts/deploy_frontend.sh ${local.frontend_bucket_name} ${local.api_endpoint}/${local.stage} ${aws_cognito_user_pool_client.userpool_client.id} ${terraform_data.cognito_base_url.output} ${aws_lambda_function_url.redirect.function_url}"
  }

  triggers_replace = {
    always_run = "${timestamp()}" # TODO: Check hash?
  }
}
