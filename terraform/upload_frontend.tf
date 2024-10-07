locals {
  frontend_bucket_name = module.s3["soul-pupils-spa"].bucket_name
  api_endpoint         = aws_apigatewayv2_api.api_gateway.api_endpoint
}

resource "terraform_data" "upload_build" {
  depends_on = [module.s3, aws_apigatewayv2_api.api_gateway]

  provisioner "local-exec" {
    command = "${path.cwd}/scripts/deploy_frontend.sh ${local.frontend_bucket_name} ${local.api_endpoint}"
  }

  triggers_replace = {
    always_run = "${timestamp()}" # TODO: Check hash?
  }
}
