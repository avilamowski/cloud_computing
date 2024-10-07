locals {
  frontend_bucket_name = module.s3["soul-pupils-spa"].bucket_name
}

resource "terraform_data" "upload_build" {
  depends_on = [module.s3]

  provisioner "local-exec" {
    command = "${path.cwd}/scripts/deploy_frontend.sh ${local.frontend_bucket_name}"
  }

  triggers_replace = {
    always_run = "${timestamp()}" # TODO: Check hash?
  }
}
