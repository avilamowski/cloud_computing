vpc = {
  vpc_cidr = "18.0.0.0/16"
  vpc_name = "tp-vpc"
  subnets = [
    {
      name       = "backend1"
      cidr_block = "18.0.0.0/24"
    },
    {
      name       = "backend2"
      cidr_block = "18.0.1.0/24"
    }
  ]
}


s3_buckets = {
  "soul-pupils-spa" : {
    website    = true
    versioning = false
  },
  "uploaded-images" : {
    website    = false
    versioning = true
  }
}

rds = {
  db_name     = "bd-sql"
  db_username = "postgres"
  db_password = "12345678"
  db_port     = 5432
}
