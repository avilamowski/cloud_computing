resource "aws_ecr_repository" "repository" {
  for_each = toset(var.lambda_names)

  name = each.key

  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
}


resource "aws_lambda_function" "this" {
  for_each = toset(var.lambda_names)

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
    command = "${path.cwd}/deploy_all.sh ${var.lambda_aws_account_id}"
  }
}

resource "aws_security_group" "lambda_sg" {
  vpc_id = var.lambda_vpc_id
  name   = "lambda_sg"
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

