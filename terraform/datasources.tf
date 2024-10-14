data "aws_canonical_user_id" "current" {}

data "aws_availability_zones" "available" {}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

data "aws_iam_role" "lab_role" {
  name = "LabRole"
}

data "archive_file" "lambda_upload_image" {
  type        = "zip"
  source_file = "${path.cwd}/../backend/upload_image.py"
  output_path = "${path.cwd}/lambda_upload_image.zip"
}
