resource "terraform_data" "zip_lambda" {
  provisioner "local-exec" {
    command = "zip -j ${path.cwd}/lambda_upload_image.zip ${path.cwd}/../backend/upload_image.py"
  }
  triggers_replace = {
    always_run = "${timestamp()}" # TODO: Check hash?
  }
}

resource "aws_lambda_function" "this" {
  depends_on = [terraform_data.zip_lambda]

  function_name = "upload_image"
  timeout       = 60
  filename      = "${path.cwd}/lambda_upload_image.zip"
  handler       = "upload_image.lambda_handler"
  #   source_code_hash = filebase64sha256("${path.cwd}/lambda_upload_image.zip")
  runtime       = "python3.11"
  architectures = ["x86_64"]
  role          = data.aws_iam_role.lab_role.arn
}
