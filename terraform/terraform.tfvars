vpc = {
  vpc_cidr     = "18.0.0.0/16"
  vpc_name     = "tp-vpc"
  subnet_names = ["backend1", "backend2"]
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
  db_name     = "bdsql"
  db_username = "postgres"
  db_password = "12345678"
  db_port     = 5432
}

lambda_names = ["get_publications", "get_comments", "create_publication", "create_comment", "init_db"]

api_endpoints = [
  {
    name                 = "get_publications"
    method               = "GET"
    path                 = "/get_publications"
    authorization_scopes = []
  },

  {
    name                 = "get_comments"
    method               = "GET"
    path                 = "/get_comments"
    authorization_scopes = []
  },
  {
    name                 = "create_publication"
    method               = "POST"
    path                 = "/create_publication"
    authorization_scopes = []
  },

  {
    name                 = "create_comment"
    method               = "POST"
    path                 = "/create_comment"
    authorization_scopes = []
  },


  {
    name                 = "upload_image"
    method               = "POST"
    path                 = "/upload_image"
    authorization_scopes = []
  }

]
