variable "lambda_name" {
  type = string
}

variable "lambda_role_arn" {
  type = string
}

variable "environment_variables" {
  type = object({})
}

variable "source_code_hash" {
  type = string
}
