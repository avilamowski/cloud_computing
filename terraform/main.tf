module "s3" {
  source = "./modules/s3"

  for_each = var.s3_buckets

  s3_name       = each.key
  s3_is_website = each.value.website
  s3_versioning = each.value.versioning
}
