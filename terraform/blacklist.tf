resource "terraform_data" "upload_blacklists" {

  provisioner "local-exec" {
    command = "${path.cwd}/scripts/blacklist.sh ${module.s3["spam-filter-files"].bucket_name}"
  }

  triggers_replace = {
    always_run = "${timestamp()}"
  }
}
