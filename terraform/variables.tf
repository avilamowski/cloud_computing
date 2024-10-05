variable "vpc" {
  type = object({
    vpc_cidr = string
    vpc_name = string
    subnets = list(object({
      name       = string
      cidr_block = string
    }))
  })
}

variable "s3_buckets" {
  type = map(object({
    website = bool
    versioning = bool
  }))
}