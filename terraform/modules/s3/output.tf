output "bucket_name" {
  value = aws_s3_bucket.this.bucket
}

output "bucket_id" {
  value = aws_s3_bucket.this.id
}

# TODO: Si no es util, sacar
output "bucket_arn" {
  value = aws_s3_bucket.this.arn
}
